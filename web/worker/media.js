import {HttpError,must,cleanText,identifier,hash} from './model.js';
import {scriptFor,timelineSvg,validateUpload,validateCaptions,speechChunks,pcmWav} from './media-model.js';
const q=(db,sql,...a)=>db.prepare(sql).bind(...a);
const first=(db,sql,...a)=>q(db,sql,...a).first();
const all=async(db,sql,...a)=>(await q(db,sql,...a).all()).results;
const now=()=>new Date().toISOString();
const json=(v,status=200)=>Response.json(v,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
async function bounded(request,max){const reader=request.body?.getReader();if(!reader)return new Uint8Array();let size=0;const chunks=[];while(true){const r=await reader.read();if(r.done)break;size+=r.value.byteLength;if(size>max){await reader.cancel();throw new HttpError(413,'Media request exceeds the size limit');}chunks.push(r.value);}const output=new Uint8Array(size);let offset=0;for(const c of chunks){output.set(c,offset);offset+=c.length;}return output;}
async function input(request){must((request.headers.get('content-type')||'').includes('application/json'),'Use application/json');try{return JSON.parse(new TextDecoder().decode(await bounded(request,16384)));}catch(e){if(e instanceof HttpError)throw e;throw new HttpError(400,'Invalid JSON');}}
async function version(db,id,n){const r=await first(db,'SELECT v.*,s.latest FROM htp_versions v JOIN htp_stories s ON v.story_id=s.id WHERE v.story_id=? AND v.version=?',id,n);if(!r)throw new HttpError(404,'Story version not found');r.payload=JSON.parse(r.payload);must(await hash(r.payload)===r.hash,'Story content hash mismatch');return r;}
async function selected(db,id,requested){
 if(requested!=null){must(/^[1-9]\d{0,8}$/.test(requested),'Invalid media version');const r=await version(db,id,Number(requested));const pub=await first(db,'SELECT version FROM htp_publications WHERE story_id=? AND version=?',id,r.version);if(!pub&&r.version!==r.latest)throw new HttpError(404,'Version is not available to readers');return r;}
 const pub=await first(db,'SELECT version FROM htp_publications WHERE story_id=? ORDER BY sequence DESC LIMIT 1',id);const head=await first(db,'SELECT latest FROM htp_stories WHERE id=?',id);if(!head)throw new HttpError(404,'Save the research story first');return version(db,id,pub?.version||head.latest);
}
const publicJob=j=>({id:j.id,story_id:j.story_id,version:j.version,kind:j.kind,method:j.method,status:j.status,attempts:j.attempts,error:j.error,created_at:j.created_at,updated_at:j.updated_at,metadata:JSON.parse(j.metadata),url:j.object_key?'/api/media/file/'+j.id:null,script_hash:j.script_hash});
function cap(env){const n=Number(env.EPSTMC_MEDIA_DAILY_LIMIT||6);return Number.isInteger(n)&&n>=0&&n<=50?n:6;}
async function reserve(db,r,kind,method,actor,key,limit){
 must(identifier(key),'Provide a unique request_key');const script=await scriptFor(r.payload);const existing=await first(db,'SELECT * FROM htp_media WHERE story_id=? AND request_key=?',r.story_id,key);if(existing){if(existing.version!==r.version||existing.method!==method)throw new HttpError(409,'Request key belongs to different content');return {job:existing,reused:true,script};}
 const id=crypto.randomUUID(),time=now();
 const rows=await q(db,`INSERT INTO htp_media (id,story_id,version,story_hash,script_hash,kind,method,status,metadata,created_by,created_at,updated_at,request_key,attempts) SELECT ?,?,?,?,?,?,?,'queued','{}',?,?,?,?,0 WHERE (SELECT COUNT(*) FROM htp_media WHERE created_at>=? AND method IN ('openai-tts','openai-image'))<?`,id,r.story_id,r.version,r.hash,script.hash,kind,method,actor,time,time,key,time.slice(0,10),limit).run();
 if(!rows.meta.changes)throw new HttpError(429,'Daily generation limit reached; retry another day or upload an existing asset');return {job:await first(db,'SELECT * FROM htp_media WHERE id=?',id),reused:false,script};
}
async function reviewJob(db,env,id,action,note,actor){
 must(cleanText(note),'Record your media review');const j=await first(db,'SELECT * FROM htp_media WHERE id=?',id);if(!j)throw new HttpError(404,'Media not found');if(!['review','ready'].includes(j.status))throw new HttpError(409,'Only completed media can be reviewed');const r=await version(db,j.story_id,j.version);
 if(action==='approve'){if(r.status!=='approved'||r.latest!==j.version||r.hash!==j.story_hash)throw new HttpError(409,'Approve the latest story version before releasing its media');if(j.status!=='review')throw new HttpError(409,'Media is already released');must(j.object_key,'Media file is missing');if(!await env.BUCKET?.head(j.object_key))throw new HttpError(409,'Stored media file is unavailable');}
 must(['approve','reject'].includes(action),'Invalid media review action');const token=crypto.randomUUID(),status=action==='approve'?'ready':'rejected',time=now();
 const result=await db.batch([q(db,`UPDATE htp_media SET status=?,reviewed_by=?,review_note=?,updated_at=?,decision_token=? WHERE id=? AND status=?`,status,actor,note,time,token,id,j.status),q(db,'INSERT INTO htp_audit (id,story_id,version,action,actor,note,created_at) SELECT ?,?,?,?,?,?,? WHERE EXISTS (SELECT 1 FROM htp_media WHERE decision_token=?)',token,j.story_id,j.version,'media_'+action,actor,note,time,token)]);if(!result[0].meta.changes)throw new HttpError(409,'Media review changed; reload');return publicJob(await first(db,'SELECT * FROM htp_media WHERE id=?',id));
}
async function generate(db,env,r,data,actor){
 const method=data.method;must(['diagram','openai-image','openai-tts','storyboard'].includes(method),'Choose a supported media method');
 if(!env.BUCKET)throw new HttpError(503,'Media storage is not connected');
 if(method.startsWith('openai-')){if(env.EPSTMC_MEDIA_GENERATION!=='enabled'||!env.OPENAI_API_KEY)throw new HttpError(503,'Provider generation is not configured; use the evidence diagram, browser listening or upload');if(method==='openai-tts'&&!env.EPSTMC_TTS_MODEL)throw new HttpError(503,'Choose an available speech model in server configuration');if(method==='openai-image'&&!env.EPSTMC_IMAGE_MODEL)throw new HttpError(503,'Choose an available image model in server configuration');}
 const kind=method==='openai-tts'?'audio':method==='storyboard'?'storyboard':'image';
 const {job,reused,script}=await reserve(db,r,kind,method,actor,data.request_key,method.startsWith('openai-')?cap(env):1000000);if(reused)return publicJob(job);
 const key='media/'+r.story_id+'/'+r.version+'/'+job.id;let mime,bytes,metadata;
 await q(db,"UPDATE htp_media SET status='generating',attempts=1,updated_at=? WHERE id=?",now(),job.id).run();
 try{
 if(method==='diagram'){mime='image/svg+xml';bytes=new TextEncoder().encode(timelineSvg(r.payload));metadata={caption:'Selected dated evidence; thematic connections do not establish causation.',alt:'Evidence timeline for '+r.payload.title,credit:'EPSTMC · rendered from the attached source-backed timeline',rights:'Original evidence diagram',disclosure:'Evidence diagram; not a photograph'};}
 else if(method==='storyboard'){mime='application/json';bytes=new TextEncoder().encode(JSON.stringify(script));metadata={caption:'Source-linked visual explainer with captions and transcript',credit:'EPSTMC · extractive storyboard',rights:'Story-derived explanation',disclosure:'Interactive storyboard, not generated footage'};}
 else{
 const speech=method==='openai-tts';const fetcher=env.TEST_MEDIA_FETCH||fetch;const signal=AbortSignal.timeout(90000);let model;
 if(speech){
 model=env.EPSTMC_TTS_MODEL;const chunks=speechChunks(script.transcript),pcm=[];
 for(let i=0;i<chunks.length;i++){
 await q(db,'UPDATE htp_media SET attempts=?,updated_at=? WHERE id=?',i+1,now(),job.id).run();
 const response=await fetcher('https://api.openai.com/v1/audio/speech',{method:'POST',headers:{Authorization:'Bearer '+env.OPENAI_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({model,voice:env.EPSTMC_TTS_VOICE||'alloy',input:chunks[i],response_format:'pcm'}),signal});if(!response.ok)throw new Error('Provider failed');pcm.push(await bounded(response,8*1024*1024));if(pcm.reduce((n,b)=>n+b.byteLength,0)>24*1024*1024)throw new Error('Audio too large');
 }
 bytes=pcmWav(pcm);mime='audio/wav';
 }else{
 model=env.EPSTMC_IMAGE_MODEL;
 const response=await fetcher('https://api.openai.com/v1/images/generations',{method:'POST',headers:{Authorization:'Bearer '+env.OPENAI_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({model,n:1,size:'1024x1024',output_format:'png',prompt:'Create an editorial illustration without text, charts, maps or claimed documentary evidence. No photorealism. Subject: '+r.payload.title+'. Context: '+r.payload.summary.slice(0,1200)}),signal});if(!response.ok)throw new Error('Provider failed');
 const raw=JSON.parse(new TextDecoder().decode(await bounded(response,16*1024*1024)));const b64=raw.data?.[0]?.b64_json;must(typeof b64==='string'&&b64.length<=12*1024*1024,'Provider image bytes are unavailable');bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));mime='image/png';validateUpload(bytes,mime,'image');
 }
 metadata={caption:speech?'Narration of this story version':'AI-generated editorial illustration; not documentary evidence',alt:speech?'':'Illustration for '+r.payload.title,credit:'OpenAI · '+model,rights:'Generated media; editorial review required',disclosure:speech?'AI-generated voice':'AI-generated illustration',...(speech?{transcript:script.transcript,duration_seconds:(bytes.byteLength-44)/48000}:{})};
 }
 await env.BUCKET.put(key,bytes,{httpMetadata:{contentType:mime}});
 const saved=await q(db,"UPDATE htp_media SET status='review',object_key=?,mime=?,size=?,metadata=?,updated_at=? WHERE id=? AND status='generating'",key,mime,bytes.byteLength,JSON.stringify(metadata),now(),job.id).run();if(!saved.meta.changes){await env.BUCKET.delete(key);throw new Error('Job was closed');}return publicJob(await first(db,'SELECT * FROM htp_media WHERE id=?',job.id));
 }catch{await env.BUCKET.delete(key).catch(()=>{});await q(db,"UPDATE htp_media SET status='failed',error='Generation failed; no file was released. Check provider configuration before a new attempt.',updated_at=? WHERE id=?",now(),job.id).run();throw new HttpError(502,'Media generation failed; no asset was released. This request will not be charged again by automatic retry.');}
}
async function upload(db,env,request,story,actor){
 if(!env.BUCKET)throw new HttpError(503,'Media storage is not connected');must((request.headers.get('content-type')||'').startsWith('multipart/form-data'),'Use a multipart file upload');
 const raw=await bounded(request,24*1024*1024);const form=await new Response(raw,{headers:{'Content-Type':request.headers.get('content-type')}}).formData();const file=form.get('file');must(file&&typeof file.arrayBuffer==='function','Choose a media file');const kind=form.get('kind');must(['image','audio','video'].includes(kind),'Invalid upload kind');const r=await version(db,story,Number(form.get('expected_version')));if(r.latest!==r.version)throw new HttpError(409,'Upload against the latest story version');const bytes=await file.arrayBuffer();must(bytes.byteLength<=20*1024*1024,'Files must be at most 20 MiB');validateUpload(bytes,file.type,kind);
 const metadata={caption:form.get('caption'),credit:form.get('credit'),rights:form.get('rights'),disclosure:form.get('disclosure')||'Uploaded editorial media',alt:form.get('alt')||'',transcript:form.get('transcript')||'',captions:form.get('captions')||''};for(const key of ['caption','credit','rights','disclosure'])must(cleanText(metadata[key]),'Provide '+key);if(kind==='image')must(cleanText(metadata.alt),'Image requires alternative text');if(kind!=='image')must(cleanText(metadata.transcript),'Audio/video requires a transcript');if(kind==='video')validateCaptions(metadata.captions);
 const id=crypto.randomUUID(),key='media/'+story+'/'+r.version+'/'+id,time=now(),script=await scriptFor(r.payload);
 await env.BUCKET.put(key,bytes,{httpMetadata:{contentType:file.type}});
 try{await q(db,"INSERT INTO htp_media (id,story_id,version,story_hash,script_hash,kind,method,status,metadata,object_key,mime,size,created_by,created_at,updated_at,request_key,attempts) VALUES (?,?,?,?,?,?, 'upload','review',?,?,?,?,?,?,?,?,0)",id,story,r.version,r.hash,(kind==='image'?script.hash:await hash({transcript:metadata.transcript})),kind,JSON.stringify(metadata),key,file.type,bytes.byteLength,actor,time,time,id).run();}catch(e){await env.BUCKET.delete(key);throw e;}
 return publicJob(await first(db,'SELECT * FROM htp_media WHERE id=?',id));
}
async function fileResponse(request,db,env,id,preview,captions=false){
 const j=await first(db,'SELECT * FROM htp_media WHERE id=?',id);if(!j||!j.object_key)throw new HttpError(404,'Media not found');
 if(preview){if(!['review','ready'].includes(j.status))throw new HttpError(404,'Preview unavailable');}
 else{const r=await selected(db,j.story_id,null);const old=new URL(request.url).searchParams.get('version');const selectedVersion=old?await selected(db,j.story_id,old):r;if(j.status!=='ready'||j.version!==selectedVersion.version||j.story_hash!==selectedVersion.hash)throw new HttpError(404,'Media is not released for this story version');}
 if(captions){const c=JSON.parse(j.metadata).captions;if(!c)throw new HttpError(404,'Captions not found');return new Response(request.method==='HEAD'?null:c,{headers:{'Content-Type':'text/vtt; charset=utf-8','Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff'}});}
 if(!env.BUCKET)throw new HttpError(503,'Media storage unavailable');
 const range=request.headers.get('range');if(range&&(!/^bytes=\d*-\d*$/.test(range)||range==='bytes=-'))return new Response(null,{status:416});
 if(range){const head=await env.BUCKET.head(j.object_key);if(!head)throw new HttpError(404,'Media file unavailable');const parts=range.slice(6).split('-');if((parts[0]&&Number(parts[0])>=head.size)||(parts[0]&&parts[1]&&Number(parts[0])>Number(parts[1]))||(!parts[0]&&Number(parts[1])===0))return new Response(null,{status:416,headers:{'Content-Range':'bytes */'+head.size}});}
 const obj=await env.BUCKET.get(j.object_key,range?{range:request.headers}:undefined);if(!obj)throw new HttpError(404,'Media file unavailable');const headers=new Headers({'Content-Type':j.mime,'Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff','Accept-Ranges':'bytes','Content-Security-Policy':"default-src 'none'; sandbox"});let status=200;if(range&&obj.range){const start=obj.range.offset||0;const length=obj.range.length||obj.size-start;headers.set('Content-Range','bytes '+start+'-'+(start+length-1)+'/'+obj.size);headers.set('Content-Length',String(length));status=206;}else headers.set('Content-Length',String(obj.size));return new Response(request.method==='HEAD'?null:obj.body,{status,headers});
}
export async function mediaRoute(request,env,story,actor){
 const db=env.DB,u=new URL(request.url),path=u.pathname;must(actor,'Editor identity is required');
 if(['GET','HEAD'].includes(request.method)){
 const match=path.match(/^\/api\/media\/(file|captions)\/([a-f0-9-]{36})$/);if(match)return fileResponse(request,db,env,match[2],u.searchParams.get('preview')==='1',match[1]==='captions');
 if(path==='/api/media/export'){const head=await first(db,'SELECT latest FROM htp_stories WHERE id=?',story);if(!head)throw new HttpError(404,'Save the story first');const r=await version(db,story,head.latest),script=await scriptFor(r.payload);return new Response(JSON.stringify({...script,story_id:story,story_version:r.version,story_hash:r.hash,script_hash:script.hash,review_status:r.status,sources:r.payload.sources},null,2),{headers:{'Content-Type':'application/json','Content-Disposition':'attachment; filename="'+story+'-v'+r.version+'-storyboard.json"','Cache-Control':'private, no-store'}});}
 if(path==='/api/media/diagram'){const r=await selected(db,story,u.searchParams.get('version'));return new Response(request.method==='HEAD'?null:timelineSvg(r.payload),{headers:{'Content-Type':'image/svg+xml','Cache-Control':'private, no-store','X-Content-Type-Options':'nosniff','Content-Security-Policy':"default-src 'none'; sandbox"}});}
 if(path==='/api/media/config')return json({storage:!!env.BUCKET,image_generation:!!env.OPENAI_API_KEY&&!!env.EPSTMC_IMAGE_MODEL&&env.EPSTMC_MEDIA_GENERATION==='enabled',audio_generation:!!env.OPENAI_API_KEY&&!!env.EPSTMC_TTS_MODEL&&env.EPSTMC_MEDIA_GENERATION==='enabled',daily_generation_limit:cap(env),upload_limit_bytes:20*1024*1024});
 if(path==='/api/media/review'){const head=await first(db,'SELECT latest FROM htp_stories WHERE id=?',story);if(!head)throw new HttpError(404,'Save the story first');const r=await version(db,story,head.latest);const jobs=await all(db,'SELECT * FROM htp_media WHERE story_id=? ORDER BY created_at DESC LIMIT 100',story);return json({version:r.version,story_status:r.status,jobs:jobs.map(j=>({...publicJob(j),stale:j.version!==r.version||j.story_hash!==r.hash})),script:await scriptFor(r.payload)});}
 if(path==='/api/media'){const r=await selected(db,story,u.searchParams.get('version'));const jobs=await all(db,"SELECT * FROM htp_media WHERE story_id=? AND version=? AND story_hash=? AND status='ready' ORDER BY created_at DESC",story,r.version,r.hash);return json({version:r.version,assets:jobs.map(publicJob),script:await scriptFor(r.payload),research:r.status!=='approved'});}
 throw new HttpError(404,'Media endpoint not found');
 }
 if(request.method!=='POST')return json({error:'Method not allowed'},405);
 if(path==='/api/media/upload')return json(await upload(db,env,request,story,actor),201);
 const data=await input(request);
 if(path==='/api/media/generate'){must(Number.isInteger(data.expected_version),'Specify the story version');const r=await version(db,story,data.expected_version);if(r.latest!==r.version)throw new HttpError(409,'Story changed; reload before generating');return json(await generate(db,env,r,data,actor),201);}
 if(path==='/api/media/abandon'){const j=await first(db,"SELECT * FROM htp_media WHERE id=? AND story_id=? AND status IN ('queued','generating')",data.id,story);if(!j||Date.now()-Date.parse(j.updated_at)<300000)throw new HttpError(409,'Only an unfinished job older than five minutes can be closed');await q(db,"UPDATE htp_media SET status='failed',error='Operator closed an interrupted job. Provider charges may already have occurred; no automatic retry.',updated_at=? WHERE id=? AND status IN ('queued','generating')",now(),j.id).run();return json({status:'failed'});}
 if(path==='/api/media/decision'){const j=await first(db,'SELECT story_id FROM htp_media WHERE id=?',data.id);if(!j||j.story_id!==story)throw new HttpError(404,'Media not found for this story');return json(await reviewJob(db,env,data.id,data.action,data.note,actor));}
 throw new HttpError(404,'Media endpoint not found');
}
