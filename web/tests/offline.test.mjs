import {test} from 'node:test';
import assert from 'node:assert/strict';
import {offlineSnapshot,validateOfflineSnapshot,offlineWorker,offlineProgram} from '../worker/offline.js';
import {readFileSync} from 'node:fs';
const c=JSON.parse(readFileSync(new URL('../worker/case-study.json',import.meta.url)));
test('offline copies contain only reader projection and no editorial notes or identities',()=>{const x=offlineSnapshot({version:1,status:'research_preview',content:c,review:{assessment:'PRIVATE NOTE'},created_by:'PRIVATE ACTOR'},null,[]);assert.ok(!JSON.stringify(x).includes('PRIVATE'));assert.equal(validateOfflineSnapshot(x).id,c.id);assert.equal(x.state.content.timeline.length,c.timeline.length);assert.throws(()=>offlineSnapshot({content:c},null,[]));});
test('tampered local copies reject unsafe source links and changed identities',()=>{const x=offlineSnapshot({version:1,status:'published',content:c},null,[]);x.state.content.sources[0].url='javascript:alert(1)';assert.throws(()=>validateOfflineSnapshot(x));const y=offlineSnapshot({version:1,content:c},null,[]);y.id='other';assert.throws(()=>validateOfflineSnapshot(y));});
test('offline worker caches only an explicitly enabled app shell and bypasses API caching',()=>{new Function(offlineWorker);new Function(offlineProgram);assert.ok(offlineWorker.includes("u.pathname!=='/'"));assert.ok(offlineWorker.includes("X-EPSTMC-Shell"));assert.ok(offlineWorker.includes("ENABLE_OFFLINE"));assert.ok(!offlineWorker.includes('caches.addAll'));});
