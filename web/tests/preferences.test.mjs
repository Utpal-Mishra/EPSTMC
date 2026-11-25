import {test} from 'node:test';
import assert from 'node:assert/strict';
import {normalizePreferences,publishedChanges,preferencesProgram} from '../worker/preferences.js';
import {siteAssets} from '../worker/site-assets.js';
test('preferences default safely and keep opt-in alerts off unless explicitly true',()=>{assert.deepEqual(normalizePreferences(null),{font:'standard',alerts:false});assert.deepEqual(normalizePreferences({font:'script',alerts:'true'}),{font:'standard',alerts:false});assert.deepEqual(normalizePreferences({font:'large',alerts:true}),{font:'large',alerts:true});});
test('alerts ignore the first load and draft changes but detect actual publication changes',()=>{const items=[{id:'one',version:2,status:'published'},{id:'two',version:4,status:'research_preview'}];assert.deepEqual(publishedChanges(null,items),[]);assert.deepEqual(publishedChanges({one:{version:1,status:'published'}},items).map(x=>x.id),['one']);assert.deepEqual(publishedChanges({one:{version:2,status:'published'}},items),[]);});
test('manifest uses only same-site assets and browser program parses',()=>{const m=JSON.parse(siteAssets['/manifest.webmanifest'].body);assert.equal(m.scope,'/');assert.ok(m.icons.every(x=>x.src.startsWith('/')));new Function(preferencesProgram);assert.ok(!preferencesProgram.includes('pushManager.subscribe'));});
