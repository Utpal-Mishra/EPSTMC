// Local QA adapter only. This file is never bundled into the deployed Worker.
import {Miniflare} from 'miniflare';
import {createServer} from 'node:http';
import {readFileSync,readdirSync} from 'node:fs';
const mf=new Miniflare({modules:true,scriptPath:'dist/server/index.js',compatibilityDate:'2026-05-01',d1Databases:{DB:'preview-db'}});
const db=await mf.getD1Database('DB');
for(const file of readdirSync('drizzle').filter(f=>f.endsWith('.sql')).sort())for(const sql of readFileSync('drizzle/'+file,'utf8').split(/-->\s*statement-breakpoint/))if(sql.trim())await db.prepare(sql.trim()).run();
await mf.dispatchFetch('http://127.0.0.1:4173/api/initialize',{method:'POST',headers:{'oai-authenticated-user-id':'local-preview-only',Origin:'http://127.0.0.1:4173'}});
const server=createServer(async(req,res)=>{try{const buffers=[];for await(const chunk of req)buffers.push(chunk);const headers=new Headers(req.headers);headers.set('oai-authenticated-user-id','local-preview-only');const r=await mf.dispatchFetch('http://127.0.0.1:4173'+req.url,{method:req.method,headers,...(['GET','HEAD'].includes(req.method)?{}:{body:Buffer.concat(buffers)})});res.writeHead(r.status,Object.fromEntries(r.headers));res.end(Buffer.from(await r.arrayBuffer()));}catch{res.writeHead(500);res.end('Local preview failed');}});
server.listen(Number(process.env.PORT||4173),'0.0.0.0',()=>console.log('Local QA: http://127.0.0.1:4173/'));
async function stop(){server.close();await mf.dispose();process.exit(0);}process.on('SIGTERM',stop);process.on('SIGINT',stop);
