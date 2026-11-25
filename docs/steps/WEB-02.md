# WEB-02 — Guided story creation and revision

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | IMPLEMENTED / focused authoring checks passed |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Create and edit the complete source-backed story through labelled fields and repeatable sections; keep JSON as an optional advanced mode and preserve review controls.

## Evidence and implementation

Pending. Future implementation, validation, source integration, deployment and editorial approval are separate events. The implementation commit subject contains this step ID.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.

## Implementation result — 25 November 2026

Added a guided creation/revision form for all story fields, sources, qualified historical comparisons, conditional scenarios, timeline events and gaps. New forms begin with blank research attestations; advanced JSON remains available. Three focused tests passed for blank-state honesty, round-trip contract normalization and browser program parsing.

Affected files: web/worker/authoring.js, web/worker/ui.js, web/worker/workspace-ui.js, web/worker/reader-tools.js, web/tests/authoring.test.mjs. The implementation commit is identified by WEB-02 in its subject. Source synchronization and deployment are recorded under WEB-08.
