// Presence checks only: configured does not attest account access or output quality.
export function integrationConfig(env) {
  const storage = !!env.BUCKET;
  const enabled = env.EPSTMC_MEDIA_GENERATION === 'enabled';
  const limit = Number(env.EPSTMC_MEDIA_DAILY_LIMIT ?? 6);
  const daily = Number.isInteger(limit) && limit >= 0 && limit <= 50 ? limit : 6;
  const specs = [
    ['image', 'OpenAI illustrations', ['OPENAI_API_KEY', 'EPSTMC_IMAGE_MODEL']],
    ['audio', 'OpenAI narration', ['OPENAI_API_KEY', 'EPSTMC_TTS_MODEL']],
    ['video', 'Shotstack captioned MP4', ['SHOTSTACK_API_KEY']]
  ];
  const integrations = specs.map(([id, label, keys]) => {
    const missing = keys.filter(key => !env[key]);
    if (!storage) missing.push('BUCKET');
    if (!enabled) missing.push('EPSTMC_MEDIA_GENERATION=enabled');
    if (!daily) missing.push('EPSTMC_MEDIA_DAILY_LIMIT>0');
    if (id === 'video' && !['stage', 'v1'].includes(env.SHOTSTACK_ENV || 'stage')) missing.push('SHOTSTACK_ENV=stage or v1');
    return {id, label, configured: missing.length === 0, missing,
      environment: id === 'video' ? (env.SHOTSTACK_ENV || 'stage') : undefined,
      verification: 'Configuration presence only; live provider test pending'};
  });
  return {storage, image_generation: integrations[0].configured,
    audio_generation: integrations[1].configured, video_generation: integrations[2].configured,
    daily_generation_limit: daily, upload_limit_bytes: 20 * 1024 * 1024, integrations};
}
