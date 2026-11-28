import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {videoEdit, outputURL, readBounded} from '../worker/hosted-video.js';
import {scriptFor} from '../worker/media-model.js';
const id='12345678-1234-1234-1234-123456789012';
const metadata={provider_environment:'stage',provider_id:id};
test('video preserves full conditions, historical limits and gaps across readable caption pages',async()=>{
  const c=JSON.parse(readFileSync('worker/case-study.json','utf8'));
  const script=await scriptFor(c), v=videoEdit(script);
  const text=v.edit.timeline.tracks[0].clips.map(x=>x.asset.text).join(' ');
  for(const original of [c.scenarios[0].condition,c.history[0].limitations,...c.gaps])
    assert.ok(text.includes(original),original);
  assert.ok(v.duration<=360); assert.match(v.captions,/WEBVTT/);
  assert.deepEqual(v.edit.output.destinations,[{provider:'shotstack',exclude:true}]);
  assert.ok(!JSON.stringify(v.edit).includes('callback'));
});
test('overlong videos reject before any render request rather than dropping coverage',()=>{
  assert.throws(()=>videoEdit({title:'Title',scenes:[{title:'Long',text:'word '.repeat(10000),source_ids:[]}]}));
});
test('render downloads accept only matching output bucket, environment and render ID',()=>{
  const valid='https://shotstack-api-stage-output.s3-ap-southeast-2.amazonaws.com/owner/'+id+'.mp4';
  assert.equal(outputURL(valid,metadata),valid);
  for(const invalid of ['https://evil.invalid/'+id+'.mp4',valid.replace('stage-output','v1-output'),
    valid.replace(id,'00000000-0000-0000-0000-000000000000'),valid.replace('https:','http:'),
    valid.replace('https://','https://key@'),valid.replace('.mp4','.mp4/redirect'),valid+'#fragment'])
    assert.throws(()=>outputURL(invalid,metadata));
});
test('bounded downloads reject declared and streamed oversized responses',async()=>{
  await assert.rejects(readBounded(new Response('12345'),4));
  await assert.rejects(readBounded(new Response('12',{headers:{'Content-Length':'999'}}),4));
  assert.equal((await readBounded(new Response('1234'),4)).byteLength,4);
});
