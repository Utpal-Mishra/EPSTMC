// Pure planning helpers plus an explicitly invoked, provider-free browser recorder.
// Nothing captures media, creates a canvas, starts a timer or downloads on import.
export function validateVideoScript(script) {
  if (!script || typeof script !== 'object' || typeof script.title !== 'string' || !script.title.trim() || script.title.length > 2000) {
    throw new TypeError('Choose a story script with a title of at most 2000 characters.');
  }
  if (!Array.isArray(script.scenes) || !script.scenes.length || script.scenes.length > 100) {
    throw new TypeError('The video script needs 1–100 scenes.');
  }
  let characters = script.title.length;
  for (const scene of script.scenes) {
    if (!scene || typeof scene.title !== 'string' || !scene.title.trim() || scene.title.length > 20000 ||
        typeof scene.text !== 'string' || !scene.text.trim() || scene.text.length > 20000) {
      throw new TypeError('Every scene needs a title and explanation of at most 20000 characters each.');
    }
    if (!Array.isArray(scene.source_ids) || scene.source_ids.length > 100 ||
        scene.source_ids.some(id => typeof id !== 'string' || !/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,119}$/.test(id))) {
      throw new TypeError('Every scene must have a valid source_ids list, which may be empty for coverage limits.');
    }
    characters += scene.title.length + scene.text.length;
  }
  if (characters > 200000) throw new RangeError('This script is too large for a browser video. Use the offline renderer.');
  return script;
}

export function chooseVideoMime(isSupported) {
  if (typeof isSupported !== 'function') throw new TypeError('Video recording is unavailable in this browser.');
  const options = [
    ['video/mp4;codecs=avc1.42E01E', 'mp4'],
    ['video/mp4', 'mp4'],
    ['video/webm;codecs=vp9', 'webm'],
    ['video/webm;codecs=vp8', 'webm'],
    ['video/webm', 'webm']
  ];
  for (const [mime, extension] of options) {
    let supported = false;
    try { supported = isSupported(mime); } catch { /* Try the next supported container. */ }
    if (supported) return { mime, extension };
  }
  throw new Error('This browser cannot record MP4 or WebM. Try a current desktop browser or use the offline video exporter.');
}

export function videoContainerForMime(mime) {
  if (typeof mime !== 'string') throw new TypeError('The browser did not return a video type.');
  const match = mime.trim().match(/^video\/(mp4|webm)(?:\s*;|$)/i);
  if (!match) throw new TypeError('The browser returned an unsupported video container.');
  return { mime, extension: match[1].toLowerCase() };
}

export function paginateVideoText(text, options = {}) {
  if (typeof text !== 'string') throw new TypeError('Slide text must be a string.');
  const maxLines = options.maxLines ?? 7;
  const maxWidth = options.maxWidth ?? 68;
  const measure = options.measure ?? (value => [...value].length);
  if (!Number.isInteger(maxLines) || maxLines < 1 || maxLines > 12 || !Number.isFinite(maxWidth) || maxWidth < 1) {
    throw new RangeError('Invalid slide page dimensions.');
  }
  const lines = [];
  let line = '';
  const push = () => { if (line) lines.push(line); line = ''; };
  for (const word of text.split(/\s+/).filter(Boolean)) {
    if (measure(word) > maxWidth) {
      push();
      for (const character of [...word]) {
        if (line && measure(line + character) > maxWidth) push();
        line += character;
      }
      continue;
    }
    const next = line ? line + ' ' + word : word;
    if (line && measure(next) > maxWidth) push();
    line += (line ? ' ' : '') + word;
  }
  push();
  if (!lines.length) lines.push('');
  const pages = [];
  for (let index = 0; index < lines.length; index += maxLines) pages.push(lines.slice(index, index + maxLines));
  return pages;
}

export function videoCaptionEscape(text) {
  return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/(https?|javascript):/gi, (_, scheme) => scheme + '：');
}

export function videoTimestamp(seconds) {
  const total = Math.round(seconds * 1000);
  const hours = Math.floor(total / 3600000);
  const minutes = Math.floor(total % 3600000 / 60000);
  const wholeSeconds = Math.floor(total % 60000 / 1000);
  const milliseconds = total % 1000;
  return [hours, minutes, wholeSeconds].map(value => String(value).padStart(2, '0')).join(':') + '.' + String(milliseconds).padStart(3, '0');
}

export function browserVideoTranscript(script) {
  validateVideoScript(script);
  return script.title + '\n\n' + script.scenes.map(scene =>
    scene.title + '. ' + scene.text + '\nSources: ' + (scene.source_ids.join(', ') || 'See coverage limitations')
  ).join('\n\n') + '\n';
}

export function buildBrowserVideoPlan(script, options = {}) {
  validateVideoScript(script);
  const duration = options.duration ?? 75;
  if (!Number.isFinite(duration) || duration < 1 || duration > 90) {
    throw new RangeError('Browser video duration must be between 1 and 90 seconds.');
  }
  const mode = options.mode ?? 'highlights';
  if (!['highlights', 'complete'].includes(mode)) throw new TypeError('Choose highlights or complete video mode.');
  const limitIndexes = script.scenes.map((scene, index) => /coverage limits|coverage gaps|what remains unknown|limitations/i.test(scene.title) ? index : -1).filter(index => index >= 0);
  if (mode === 'highlights' && !limitIndexes.length) {
    throw new TypeError('A highlights video needs a Coverage limits scene so important qualifications remain visible.');
  }
  const full = new Set([0, ...limitIndexes]);
  const candidates = script.scenes.map((scene, index) => ({ scene, index })).filter(item => !full.has(item.index));
  const dated = candidates.filter(item => /^\d{4}-\d{2}-\d{2}\b/.test(item.scene.title));
  const eventCandidates = dated.length ? dated : candidates;
  const highlights = eventCandidates.length <= 6 ? eventCandidates : [...eventCandidates.slice(0, 3), ...eventCandidates.slice(-3)];
  const selected = mode === 'complete' ? script.scenes.map((_, index) => index) : [...new Set([...full, ...highlights.map(item => item.index)])].sort((a, b) => a - b);
  const pages = [];
  for (const index of selected) {
    const scene = script.scenes[index];
    const complete = mode === 'complete' || full.has(index);
    const text = scene.title + '\n\n' + (complete ? scene.text : 'Headline only. The full transcript contains the explanation, context and qualifications.');
    const split = paginateVideoText(text, { measure: options.measure, maxWidth: options.maxWidth ?? (options.measure ? 1120 : 68), maxLines: 7 });
    split.forEach((lines, pageIndex) => pages.push({
      sceneIndex: index, title: scene.title, lines, text: lines.join(' '), source_ids: scene.source_ids.slice(),
      edition: complete ? 'full scene' : 'headline only', pageInScene: pageIndex + 1, pagesInScene: split.length
    }));
  }
  if (pages.length > 90 || duration / pages.length < 0.75) {
    throw new RangeError('The summary and coverage limits need more reading time than a 90-second browser video allows. Use the offline exporter for a longer complete explanation.');
  }
  const weights = pages.map(page => Math.max(10, page.text.split(/\s+/).filter(Boolean).length));
  const totalWeight = weights.reduce((sum, weight) => sum + weight, 0);
  const minimum = Math.min(1, duration / pages.length / 2);
  const remaining = duration - minimum * pages.length;
  let position = 0;
  pages.forEach((page, index) => {
    page.start = position;
    position += minimum + remaining * weights[index] / totalWeight;
    page.end = index === pages.length - 1 ? duration : position;
  });
  const disclosure = mode === 'highlights'
    ? 'Silent highlights edition: exact selected event titles, the full opening summary and all coverage-limit scenes. Full context and other qualifications remain in the accompanying transcript. Source-linked slides, not documentary footage; no narration.'
    : 'Silent captioned storyboard of the complete supplied script. Source-linked slides, not documentary footage; no narration.';
  const captions = 'WEBVTT\n\n' + pages.map(page =>
    videoTimestamp(page.start) + ' --> ' + videoTimestamp(page.end) + '\n' + videoCaptionEscape(page.text) + '\n'
  ).join('\n');
  if (captions.length >= 100000) throw new RangeError('Captions exceed the media upload limit.');
  const totalWords = pages.reduce((sum, page) => sum + page.text.split(/\s+/).filter(Boolean).length, 0);
  return {
    mode, duration, pages, captions, disclosure, transcript: browserVideoTranscript(script),
    selected_scene_indexes: selected, total_scene_count: script.scenes.length,
    recommended_reading_seconds: Math.ceil(totalWords / 3), reading_speed_warning: totalWords / duration > 3,
    source_ids: [...new Set(script.scenes.flatMap(scene => scene.source_ids))]
  };
}

export function browserVideoMetadata(script, plan, mime) {
  const container = videoContainerForMime(mime);
  return {
    mime: container.mime, extension: container.extension,
    story_id: script.story_id ?? script.id ?? null,
    story_version: script.story_version ?? script.version ?? null,
    story_hash: script.story_hash ?? null,
    script_hash: script.script_hash ?? script.hash ?? null,
    input_review_status: script.review_status ?? null,
    review_status: 'requires_editorial_review', has_narration: false, synthetic_narration: false,
    edition: plan.mode, duration_seconds: plan.duration,
    source_ids: plan.source_ids.slice(),
    disclosure: plan.disclosure,
    caption: plan.mode === 'highlights' ? 'Silent source-linked highlights; read the full transcript for context and qualifications.' : 'Silent source-linked captioned explanation.',
    credit: 'EPSTMC · browser-rendered source-linked storyboard',
    rights: 'Story-derived editorial visualization; source provenance and permissions require review.',
    reading_speed_warning: plan.reading_speed_warning,
    recommended_reading_seconds: plan.recommended_reading_seconds
  };
}

export async function recordBrowserVideo(script, options = {}) {
  if (typeof document === 'undefined' || typeof MediaRecorder === 'undefined') {
    throw new Error('Video recording needs a browser with MediaRecorder and canvas capture support.');
  }
  if (document.hidden) throw new Error('Keep this tab visible while recording the video.');
  const signal = options.signal;
  if (signal?.aborted) throw new DOMException('Video recording cancelled.', 'AbortError');
  const choice = chooseVideoMime(type => MediaRecorder.isTypeSupported(type));
  const canvas = document.createElement('canvas');
  canvas.width = 1280;
  canvas.height = 720;
  if (typeof canvas.captureStream !== 'function') {
    canvas.width = 0; canvas.height = 0;
    throw new Error('This browser cannot capture a canvas video. Use the offline exporter.');
  }
  const context = canvas.getContext('2d', { alpha: false });
  if (!context) { canvas.width = 0; canvas.height = 0; throw new Error('The video drawing surface could not be created.'); }
  context.font = '29px sans-serif';
  let plan;
  try { plan = buildBrowserVideoPlan(script, { duration: options.duration ?? 75, mode: options.mode ?? 'highlights', measure: text => context.measureText(text).width, maxWidth: 1120 }); }
  catch (error) { canvas.width = 0; canvas.height = 0; throw error; }
  const maximumBytes = 20 * 1024 * 1024;
  let stream, recorder, animationFrame = 0, timeout = 0, start = 0, byteLength = 0, settled = false;
  const chunks = [];
  let failRecording = () => {};
  const onAbort = () => failRecording(new DOMException('Video recording cancelled.', 'AbortError'));
  const onVisibility = () => { if (document.hidden) failRecording(new Error('Recording stopped because this tab became hidden. Keep it visible and retry.')); };
  const cleanup = () => {
    cancelAnimationFrame(animationFrame);
    clearTimeout(timeout);
    signal?.removeEventListener('abort', onAbort);
    document.removeEventListener('visibilitychange', onVisibility);
    if (recorder) {
      recorder.ondataavailable = recorder.onerror = recorder.onstop = recorder.onstart = null;
      if (recorder.state !== 'inactive') { try { recorder.stop(); } catch { /* Already stopped. */ } }
    }
    stream?.getTracks().forEach(track => track.stop());
    canvas.width = 0; canvas.height = 0;
  };
  const draw = (elapsed, pageIndex) => {
    const page = plan.pages[pageIndex];
    context.fillStyle = '#f4f7f3'; context.fillRect(0, 0, 1280, 720);
    context.fillStyle = '#226645'; context.fillRect(0, 0, 1280, 12);
    context.font = '20px sans-serif'; context.fillStyle = '#52695c';
    context.fillText('EPSTMC · ' + (plan.mode === 'highlights' ? 'SILENT HIGHLIGHTS' : 'SILENT VISUAL EXPLANATION'), 65, 58);
    context.font = '21px sans-serif';
    context.fillText('Chapter ' + (page.sceneIndex + 1) + ' of ' + plan.total_scene_count + ' · ' + page.edition, 65, 112);
    context.font = '29px sans-serif'; context.fillStyle = '#173d2e';
    page.lines.forEach((line, index) => context.fillText(line, 65, 172 + index * 49));
    context.font = '17px sans-serif'; context.fillStyle = '#52695c';
    const sources = page.source_ids.length ? page.source_ids.slice(0, 3).join(', ') + (page.source_ids.length > 3 ? ' · more in full transcript' : '') : 'See coverage limitations';
    const sourceLines = paginateVideoText('Sources: ' + sources, { measure: text => context.measureText(text).width, maxWidth: 1120, maxLines: 2 })[0];
    sourceLines.forEach((line, index) => context.fillText(line, 65, 578 + index * 23));
    context.fillText('Source-linked slides · no narration · full transcript accompanies this video', 65, 659);
    context.fillStyle = '#d4dfd7'; context.fillRect(65, 690, 1150, 4);
    context.fillStyle = '#226645'; context.fillRect(65, 690, 1150 * Math.min(1, elapsed / plan.duration), 4);
  };
  try {
    draw(0, 0);
    stream = canvas.captureStream(15);
    recorder = new MediaRecorder(stream, { mimeType: choice.mime, videoBitsPerSecond: 1000000 });
    const blob = await new Promise((resolve, reject) => {
      failRecording = error => {
        if (settled) return;
        settled = true;
        chunks.length = 0;
        cleanup();
        reject(error);
      };
      recorder.onerror = event => failRecording(event.error || new Error('The browser could not record this video.'));
      recorder.ondataavailable = event => {
        if (settled || !event.data?.size) return;
        byteLength += event.data.size;
        if (byteLength > maximumBytes) { failRecording(new Error('The recording exceeded the 20 MiB upload limit. Try a shorter duration.')); return; }
        chunks.push(event.data);
      };
      recorder.onstop = () => {
        if (settled) return;
        try {
          if (!byteLength) { failRecording(new Error('The browser returned an empty recording.')); return; }
          const actual = videoContainerForMime(recorder.mimeType || chunks.find(chunk => chunk.type)?.type || choice.mime);
          const blob = new Blob(chunks, { type: actual.mime });
          settled = true;
          resolve(blob);
        } catch (error) { failRecording(error); }
      };
      recorder.onstart = () => {
        start = performance.now();
        const tick = () => {
          if (settled) return;
          const elapsed = Math.min(plan.duration, (performance.now() - start) / 1000);
          let pageIndex = plan.pages.findIndex(page => elapsed < page.end);
          if (pageIndex < 0) pageIndex = plan.pages.length - 1;
          draw(elapsed, pageIndex);
          try { options.onProgress?.({ elapsed, duration: plan.duration, fraction: elapsed / plan.duration, page: pageIndex + 1, pageCount: plan.pages.length, message: 'Recording silent video. Keep this tab visible.' }); } catch { /* UI progress must not corrupt the recording. */ }
          if (elapsed >= plan.duration) { recorder.stop(); return; }
          animationFrame = requestAnimationFrame(tick);
        };
        tick();
      };
      signal?.addEventListener('abort', onAbort, { once: true });
      document.addEventListener('visibilitychange', onVisibility);
      timeout = setTimeout(() => failRecording(new Error('Recording timed out. Keep this tab visible and retry.')), plan.duration * 1000 + 15000);
      if (signal?.aborted) { onAbort(); return; }
      recorder.start(1000);
    });
    cleanup();
    const marker = new Uint8Array(await blob.slice(0, 16).arrayBuffer());
    const actual = videoContainerForMime(blob.type);
    const valid = actual.extension === 'mp4'
      ? String.fromCharCode(...marker.slice(4, 8)) === 'ftyp'
      : marker[0] === 0x1a && marker[1] === 0x45 && marker[2] === 0xdf && marker[3] === 0xa3;
    if (!valid) throw new Error('The browser returned an invalid video container. No file was prepared for upload.');
    if (signal?.aborted) throw new DOMException('Video recording cancelled.', 'AbortError');
    const metadata = browserVideoMetadata(script, plan, blob.type);
    const safeId = String(metadata.story_id || 'story').replace(/[^a-zA-Z0-9-]/g, '-').slice(0, 100);
    const filename = 'epstmc-' + safeId + '-v' + (Number.isInteger(metadata.story_version) ? metadata.story_version : 'draft') + '.' + metadata.extension;
    const file = typeof File === 'function' ? new File([blob], filename, { type: metadata.mime }) : blob;
    return { ...metadata, metadata, file, blob, filename, transcript: plan.transcript, captions: plan.captions };
  } finally {
    cleanup();
  }
}

export const browserVideo = [
  validateVideoScript, chooseVideoMime, videoContainerForMime, paginateVideoText,
  videoCaptionEscape, videoTimestamp, browserVideoTranscript, buildBrowserVideoPlan,
  browserVideoMetadata, recordBrowserVideo
].map(helper => helper.toString()).join('\n');
