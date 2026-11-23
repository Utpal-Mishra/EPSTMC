import {spawnSync} from 'node:child_process';
import {mkdirSync,copyFileSync,rmSync} from 'node:fs';
rmSync('dist',{recursive:true,force:true});
const r=spawnSync(process.execPath,['node_modules/wrangler/bin/wrangler.js','deploy','--dry-run','--outdir','dist/server'],{stdio:'inherit'});
if(r.status!==0)process.exit(r.status||1);
mkdirSync('dist/.openai',{recursive:true});copyFileSync('.openai/hosting.json','dist/.openai/hosting.json');
