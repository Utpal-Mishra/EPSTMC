import {test} from 'node:test';
import assert from 'node:assert/strict';
import {emptyStory,normalizeAuthoring,authoringProgram} from '../worker/authoring.js';
import {validateCase} from '../worker/model.js';
import {readFileSync} from 'node:fs';
const seed=JSON.parse(readFileSync(new URL('../worker/case-study.json',import.meta.url)));
test('new-story form starts blank rather than inventing researched content',()=>{const c=emptyStory();assert.equal(c.title,'');assert.equal(c.research_checked_at,'');assert.equal(c.sources[0].retrieved_at,'');assert.throws(()=>validateCase(c));});
test('guided form normalization preserves qualified story content and resolves cited lists',()=>{const raw=structuredClone(seed);for(const k of ['facts','history','scenarios','timeline'])for(const row of raw[k])row.source_ids=row.source_ids.join(', ');raw.gaps=raw.gaps.join('\n');const c=normalizeAuthoring(raw);validateCase(c);assert.deepEqual(c.facts,seed.facts);assert.deepEqual(c.history,seed.history);assert.deepEqual(c.scenarios,seed.scenarios);assert.deepEqual(c.gaps,seed.gaps);assert.ok(c.timeline.every(x=>x.date_precision==='day'));});
test('authoring browser program parses and does not embed researched defaults',()=>{new Function(authoringProgram);assert.ok(authoringProgram.includes('data-author-form'));assert.ok(!authoringProgram.includes(seed.title));});
