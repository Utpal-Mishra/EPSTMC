import {test} from 'node:test';
import assert from 'node:assert/strict';
import {integrationConfig} from '../worker/integrations.js';
test('readiness names missing settings without disclosing credentials', () => {
  const c = integrationConfig({BUCKET:{}, OPENAI_API_KEY:'secret-fixture'});
  assert.equal(c.image_generation, false);
  assert.deepEqual(c.integrations[0].missing, ['EPSTMC_IMAGE_MODEL','EPSTMC_MEDIA_GENERATION=enabled']);
  assert.ok(!JSON.stringify(c).includes('secret-fixture'));
});
test('storage, explicit enablement, positive budget and valid video environment gate all providers', () => {
  const env = {BUCKET:{}, OPENAI_API_KEY:'test', EPSTMC_IMAGE_MODEL:'image', EPSTMC_TTS_MODEL:'speech',
    SHOTSTACK_API_KEY:'test', EPSTMC_MEDIA_GENERATION:'enabled'};
  assert.ok(integrationConfig(env).integrations.every(x=>x.configured));
  for (const patch of [{BUCKET:null}, {EPSTMC_MEDIA_GENERATION:'disabled'}, {EPSTMC_MEDIA_DAILY_LIMIT:'0'}])
    assert.ok(integrationConfig({...env,...patch}).integrations.every(x=>!x.configured));
  assert.equal(integrationConfig({...env,SHOTSTACK_ENV:'https://evil.invalid'}).video_generation,false);
});
