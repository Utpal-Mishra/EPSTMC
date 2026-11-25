# WEB-07 — Navigation, unsaved work and failure handling

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | IMPLEMENTED / locally validated |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Protect editorial edits, avoid stale route rendering, preserve playback, handle offline/unavailable states and verify the integrated website journey.

## Evidence and implementation

Implemented in the WEB-07 commit: guarded navigation and unsaved-work dialog, serialized queued route loads, unknown-route and failure states, accessible current navigation, invalid-field expansion, bounded offline shell activation and bundled browser helper compatibility. Files: web/worker/{navigation,ui,authoring,media-ui,offline,workspace-ui}.js; web/tests/{navigation,media}.test.mjs.

Validation on 25 November: Worker build succeeded; 74 website tests and 54 Python tests passed. Cloud-browser local preview verified feed, blank guided story creation, dirty-title navigation prompt, discard-and-leave to Workspace, story reading and successful offline-copy saving. No synthetic test story was persisted. Provider activation, full recording capture, offline cold start and physical-device QA are not established by these checks.

GitHub integration and deployment are tracked separately under WEB-08. Revert the WEB-07 code commit to recover prior navigation; durable story data and migrations are unchanged.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.
