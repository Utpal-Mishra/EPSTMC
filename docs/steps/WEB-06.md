# WEB-06 — Reader preferences, notifications and help

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | IMPLEMENTED / preference and alert-contract checks passed |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Connect browser-local preferences, opt-in counts and open-site update alerts; provide privacy/help/setup status with honest provider and background-push limits.

## Evidence and implementation

Pending. Future implementation, validation, source integration, deployment and editorial approval are separate events. The implementation commit subject contains this step ID.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.

## Implementation result — 25 November 2026

Added browser-local text preferences, explicit opt-in aggregate counts, optional notifications limited to publication changes while the site is open, a same-origin web manifest/icon, and connected settings/help/privacy pages. Three focused checks passed for safe defaults, publication-change detection and same-site manifest/browser parsing. No background push subscription, provider credential or native app release is claimed.

Affected files: web/worker/preferences.js, web/worker/site-assets.js, web/worker/index.js, web/worker/ui.js, web/worker/reader-tools.js, web/tests/preferences.test.mjs. The implementation commit is identified by WEB-06 in its subject. Source synchronization and deployment are recorded under WEB-08.
