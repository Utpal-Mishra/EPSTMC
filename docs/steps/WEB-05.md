# WEB-05 — Browser video production and media handoff

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | IMPLEMENTED / nine contract checks passed; capture QA pending |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Produce actual captioned video in supported browsers, download transcript/captions and upload output for separate media review; preserve source version and file validation.

## Evidence and implementation

Pending. Future implementation, validation, source integration, deployment and editorial approval are separate events. The implementation commit subject contains this step ID.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.

## Implementation result — 25 November 2026

Connected an explicitly invoked browser canvas recorder to the media studio, correct MP4/WebM format selection, progress/cancel controls, transcript/VTT/provenance downloads and a version/hash-bound upload-for-review action. Added WebM validation and playback MIME handling. Nine video planning/contract checks passed; actual browser capture is recorded in WEB-07 rather than claimed by Node tests.

Affected files: web/worker/browser-video.js, web/worker/video-studio.js, web/worker/media.js, web/worker/media-model.js, web/worker/media-ui.js, web/worker/ui.js, web/worker/index.js, web/tests/browser-video.test.mjs, web/tests/media.test.mjs. The implementation commit is identified by WEB-05 in its subject. Source synchronization and deployment are recorded under WEB-08.
