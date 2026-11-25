import {test} from 'node:test';
import assert from 'node:assert/strict';
import {knownRoute,navigationProgram} from '../worker/navigation.js';
import {page} from '../worker/ui.js';
test('website routes accept expected views and reject malformed or invented story paths',()=>{for(const route of ['#/','', '#/workspace','#/new','#/settings','#/help','#/saved','#/review?story=one','#/story/one?format=watch'])assert.equal(knownRoute(route),true);for(const route of ['#/unknown','#/story/../secret','#/story/%3Cscript%3E'])assert.equal(knownRoute(route),false);});
test('integrated navigation program parses and includes an explicit unsaved-work decision',()=>{new Function(navigationProgram);const script=page.match(/<script>([\s\S]*)<\/script>/)[1];new Function(script);assert.ok(script.includes('Discard local changes and leave'));assert.ok(script.includes('aria-modal'));assert.ok(script.includes('queuedLoad'));assert.ok(!script.includes('/*NAVIGATION_TOOLS*/'));});
