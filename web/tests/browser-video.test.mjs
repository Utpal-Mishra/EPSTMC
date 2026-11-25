import {test} from 'node:test';
import assert from 'node:assert/strict';
import {
  browserVideo, chooseVideoMime, videoContainerForMime, paginateVideoText,
  buildBrowserVideoPlan, browserVideoTranscript, browserVideoMetadata, recordBrowserVideo
} from '../worker/browser-video.js';
import {validateCaptions} from '../worker/media-model.js';
const script = {
  title: 'Synthetic source-backed test only', story_id: 'test-story', story_version: 4,
  story_hash: 'story-hash', script_hash: 'new-script-hash', hash: 'legacy-hash', review_status: 'draft',
  scenes: [
    {title: 'Where the evidence stands', text: 'The sample records a fictional announcement, not an operational facility.', source_ids: ['test-source']},
    {title: '2026-01-01 · Announcement', text: 'The original document announced a plan. Approval and construction remain unverified.', source_ids: ['test-source']},
    {title: 'Historical context', text: 'A comparison has limited applicability and does not establish causation.', source_ids: ['test-source']},
    {title: 'Coverage limits', text: 'No operational facility or completed agreement has been verified.', source_ids: []}
  ]
};

test('chooses an actually supported MP4 or WebM and never renames WebM to MP4', () => {
  assert.deepEqual(chooseVideoMime(mime => mime === 'video/mp4'), {mime: 'video/mp4', extension: 'mp4'});
  assert.deepEqual(chooseVideoMime(mime => mime === 'video/webm;codecs=vp8'), {mime: 'video/webm;codecs=vp8', extension: 'webm'});
  assert.equal(videoContainerForMime('video/webm;codecs=vp9').extension, 'webm');
  assert.throws(() => chooseVideoMime(() => false), /cannot record/);
  assert.throws(() => videoContainerForMime('image/png'), /unsupported/);
});

test('pagination retains words, qualifications and long unbroken tokens without clipping', () => {
  const text = 'A qualified statement does not establish causation. ' + 'X'.repeat(80);
  const pages = paginateVideoText(text, {maxWidth: 20, maxLines: 2});
  assert.ok(pages.length > 1);
  assert.ok(pages.every(page => page.length <= 2 && page.every(line => line.length <= 20)));
  assert.equal(pages.flat().join('').replace(/\s/g, ''), text.replace(/\s/g, ''));
});

test('highlights retain complete summary and coverage limits; full transcript keeps omitted qualifications', () => {
  const plan = buildBrowserVideoPlan(script);
  assert.equal(plan.duration, 75);
  const visible = plan.pages.map(page => page.text).join(' ');
  assert.ok(visible.includes(script.scenes[0].text));
  assert.ok(visible.includes(script.scenes[3].text));
  assert.ok(visible.includes(script.scenes[1].title));
  assert.ok(visible.includes('Headline only.'));
  assert.ok(plan.transcript.includes(script.scenes[1].text));
  assert.ok(plan.transcript.includes(script.scenes[2].text));
  assert.match(plan.disclosure, /Silent highlights/);
  assert.match(plan.disclosure, /not documentary footage/);
});

test('timing is continuous, sums to requested duration and captions satisfy the hosted upload validator', () => {
  const modified = structuredClone(script);
  modified.scenes[0].text += ' Literal <markup> and https://example.test are text, not executable content.';
  const plan = buildBrowserVideoPlan(modified, {duration: 45});
  assert.equal(plan.pages[0].start, 0);
  assert.equal(plan.pages.at(-1).end, 45);
  plan.pages.forEach((page, index) => {
    assert.ok(page.end > page.start);
    if (index) assert.equal(page.start, plan.pages[index - 1].end);
  });
  assert.equal(validateCaptions(plan.captions), plan.captions);
  assert.ok(!plan.captions.replace(/-->/g, '').includes('>'));
  assert.ok(plan.transcript.includes('https://example.test'));
});

test('complete mode includes every supplied scene and preserves full transcript text exactly', () => {
  const plan = buildBrowserVideoPlan(script, {mode: 'complete', duration: 90});
  assert.equal(plan.selected_scene_indexes.length, script.scenes.length);
  for (const scene of script.scenes) {
    assert.ok(plan.pages.map(page => page.text).join(' ').includes(scene.text));
    assert.ok(browserVideoTranscript(script).includes(scene.title + '. ' + scene.text));
  }
});

test('metadata preserves immutable story lineage and never claims synthetic narration', () => {
  const plan = buildBrowserVideoPlan(script);
  const metadata = browserVideoMetadata(script, plan, 'video/webm;codecs=vp9');
  assert.equal(metadata.story_id, 'test-story');
  assert.equal(metadata.story_version, 4);
  assert.equal(metadata.story_hash, 'story-hash');
  assert.equal(metadata.script_hash, 'new-script-hash');
  assert.equal(metadata.input_review_status, 'draft');
  assert.equal(metadata.review_status, 'requires_editorial_review');
  assert.equal(metadata.has_narration, false);
  assert.equal(metadata.synthetic_narration, false);
  assert.equal(metadata.extension, 'webm');
  assert.deepEqual(metadata.source_ids, ['test-source']);
  const legacy = browserVideoMetadata({...script, story_version: undefined, script_hash: undefined, version: 2}, plan, 'video/mp4');
  assert.equal(legacy.story_version, 2);
  assert.equal(legacy.script_hash, 'legacy-hash');
});

test('bounds duration, script size and missing coverage limitations rather than silently deleting them', () => {
  for (const duration of [0, 91, NaN, Infinity]) assert.throws(() => buildBrowserVideoPlan(script, {duration}));
  const missing = structuredClone(script); missing.scenes.pop();
  assert.throws(() => buildBrowserVideoPlan(missing), /Coverage limits/);
  const huge = structuredClone(script); huge.scenes[3].text = 'Important limitation. '.repeat(900);
  assert.throws(() => buildBrowserVideoPlan(huge, {duration: 1}), /reading time/);
});

test('embedded helper parses without any import-time capture or DOM effects', () => {
  assert.doesNotThrow(() => new Function(browserVideo));
  const plan = new Function(browserVideo + '\nreturn buildBrowserVideoPlan(arguments[0]);')(script);
  assert.equal(plan.duration, 75);
});

test('Node cannot perform a browser recording and reports that limit honestly', async () => {
  await assert.rejects(recordBrowserVideo(script), /needs a browser/);
});
