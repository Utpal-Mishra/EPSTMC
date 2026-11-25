import {test} from 'node:test';
import assert from 'node:assert/strict';
import {workspaceSummary} from '../worker/workspace.js';
import {parseRoute} from '../worker/reader-tools.js';
test('workspace separates draft, published, media review and feedback totals',()=>{const w=workspaceSummary([{id:'one',version:2,status:'draft',published_version:1},{id:'two',version:1,status:'approved',published_version:null}],3,[{story_id:'one',status:'review'},{story_id:'two',status:'ready'}],[{story_id:'one',state:'pending'}]);assert.equal(w.totals.published,1);assert.equal(w.totals.drafts,1);assert.equal(w.totals.approved,1);assert.equal(w.totals.source_candidates,3);assert.equal(w.stories[0].review_media,1);assert.equal(w.stories[1].pending_feedback,0);assert.equal(parseRoute('#/workspace').view,'workspace');});
