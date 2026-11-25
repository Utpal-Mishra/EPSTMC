# WEB-04 — Explicit offline saved-reading workflow

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | IMPLEMENTED / offline contract checks passed; browser QA pending |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Opt in to local story copies, cache only the app shell, read saved projections offline, show timestamps and allow clearing; never cache editorial data or credentials.

## Evidence and implementation

Pending. Future implementation, validation, source integration, deployment and editorial approval are separate events. The implementation commit subject contains this step ID.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.

## Implementation result — 25 November 2026

Added explicit IndexedDB saved-reader copies, shell-only service-worker opt-in, timestamped offline read views, bookmarks/copy distinction and removal controls. Saved data is validated and reader-projected; editorial metadata, credentials and media files are not persisted. Three focused offline contract tests passed; cold-start browser behavior is checked in the integrated QA step.

Affected files: web/worker/offline.js, web/worker/index.js, web/worker/ui.js, web/worker/media-ui.js, web/worker/reader-tools.js, web/tests/offline.test.mjs, web/tests/media.test.mjs. The implementation commit is identified by WEB-04 in its subject. Source synchronization and deployment are recorded under WEB-08.
