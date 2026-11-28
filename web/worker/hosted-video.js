import {HttpError, must} from './model.js';
import {escapeXml, validateCaptions, validateUpload} from './media-model.js';

export const renderId = id => typeof id === 'string' && /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i.test(id);
export const videoStage = env => env.SHOTSTACK_ENV || 'stage';
const endpoint = stage => {
  must(['stage', 'v1'].includes(stage), 'Invalid Shotstack environment');
  return 'https://api.shotstack.io/edit/' + stage + '/render';
};
const stamp = seconds => new Date(seconds * 1000).toISOString().slice(11, 23);
const plain = text => String(text).replace(/[<>]/g, c => c === '<' ? '‹' : '›').replace(/https?:\/\/\S+/g, '[source link in story]');

// Split at word boundaries; never shorten away conditions, history limits or gaps.
export function videoEdit(script) {
  const pages = [];
  const add = text => {
    let page = '';
    for (const word of String(text).split(/\s+/)) {
      must(word.length <= 260, 'Video contains an overlong word; edit the story before rendering');
      if ((page + ' ' + word).trim().length > 260) { pages.push(page); page = ''; }
      page += (page ? ' ' : '') + word;
    }
    if (page) pages.push(page);
  };
  add(script.title);
  add('EPSTMC · Captioned evidence explainer. No soundtrack. Scenarios are conditional.');
  for (const scene of script.scenes) {
    add(scene.title + '. ' + scene.text);
    if (scene.source_ids.length) add('Source references: ' + scene.source_ids.join(', '));
  }
  must(pages.length > 0 && pages.length <= 60, 'Video is limited to 60 caption pages; use browser export for longer stories');
  let time = 0;
  const cues = [], clips = pages.map(text => {
    const length = Math.max(5, Math.ceil(text.split(/\s+/).length / 2.5));
    const start = time; time += length;
    cues.push(stamp(start) + ' --> ' + stamp(time) + '\n' + plain(text));
    return {asset:{type:'rich-text', text:escapeXml(text), padding:80,
      font:{family:'Open Sans',size:32,color:'#ffffff'}, align:{horizontal:'left',vertical:'middle'}}, start, length};
  });
  must(time <= 360, 'Hosted video is limited to six minutes; use browser export for longer stories');
  const captions = validateCaptions('WEBVTT\n\n' + cues.join('\n\n') + '\n');
  return {duration:time, captions, edit:{timeline:{background:'#102a35',tracks:[{clips}]},
    output:{format:'mp4',resolution:'hd',fps:25,quality:'medium',destinations:[{provider:'shotstack',exclude:true}]}}};
}

export async function readBounded(response, max) {
  const length = Number(response.headers.get('content-length'));
  if (length > max) { await response.body?.cancel(); throw new Error('Oversized provider response'); }
  const reader = response.body?.getReader(); if (!reader) throw new Error('Missing provider response');
  const chunks = []; let size = 0;
  try {
    while (true) {
      const {done,value} = await reader.read(); if (done) break;
      size += value.byteLength; if (size > max) throw new Error('Oversized provider response'); chunks.push(value);
    }
  } catch (e) { await reader.cancel().catch(()=>{}); throw e; }
  const bytes = new Uint8Array(size); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk,offset); offset += chunk.length; }
  return bytes;
}
async function provider(env, stage, path, body) {
  const response = await (env.TEST_MEDIA_FETCH || fetch)(endpoint(stage) + path, {
    method:body ? 'POST' : 'GET', redirect:'manual', signal:AbortSignal.timeout(20000),
    headers:{'x-api-key':env.SHOTSTACK_API_KEY,'Content-Type':'application/json'},
    ...(body ? {body:JSON.stringify(body)} : {})});
  if (!response.ok) throw new Error('Video provider unavailable');
  const data = JSON.parse(new TextDecoder().decode(await readBounded(response, 512 * 1024)));
  if (data.success !== true || !data.response) throw new Error('Invalid video provider response');
  return data.response;
}
export async function submitVideo(env, script) {
  const built = videoEdit(script), stage = videoStage(env);
  const result = await provider(env, stage, '', built.edit);
  if (!renderId(result.id)) throw new Error('Invalid render ID');
  return {provider_id:result.id,provider_environment:stage,provider_status:'queued',
    duration_seconds:built.duration,captions:built.captions,transcript:script.transcript,
    caption:'Source-linked captioned explainer · no soundtrack',credit:'EPSTMC · Shotstack render',
    rights:'Story-derived text; editorial rights review required',
    disclosure:'Rendered captioned explanation, not documentary footage' + (stage === 'stage' ? ' · sandbox output' : '')};
}
export async function checkVideo(env, metadata) {
  if (!env.SHOTSTACK_API_KEY) throw new HttpError(503,'Shotstack credentials are not configured');
  must(renderId(metadata.provider_id), 'Missing render reference');
  const result = await provider(env, metadata.provider_environment, '/' + metadata.provider_id);
  if (result.id !== metadata.provider_id) throw new Error('Render ID mismatch');
  return result;
}
export function outputURL(raw, metadata) {
  const stage = metadata.provider_environment;
  must(['stage','v1'].includes(stage) && renderId(metadata.provider_id),'Invalid render reference');
  const u = new URL(raw);
  const bucket = 'shotstack-api-' + stage + '-output';
  const hosts = [bucket + '.s3-ap-southeast-2.amazonaws.com', bucket + '.s3.ap-southeast-2.amazonaws.com'];
  if (u.protocol !== 'https:' || !hosts.includes(u.hostname) || u.username || u.password || u.port || u.hash ||
      !new RegExp('^/[A-Za-z0-9_-]+/' + metadata.provider_id + '\\.mp4$','i').test(u.pathname)) throw new Error('Untrusted render output');
  return u.href;
}
export async function downloadVideo(env, result, metadata) {
  const response = await (env.TEST_MEDIA_FETCH || fetch)(outputURL(result.url,metadata),{
    redirect:'manual', signal:AbortSignal.timeout(30000)});
  if (!response.ok) throw new Error('Video output is not available');
  const bytes = await readBounded(response,20*1024*1024);
  validateUpload(bytes,'video/mp4','video'); return bytes;
}
