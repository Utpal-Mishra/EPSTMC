# MED-09 — Private uploads and recording playback

| Field | Value |
| --- | --- |
| Step ID | MED-09 |
| Phase | Two-week media scope |
| Planned window | 1–4 December 2026 |
| Actual implementation/event | 24 November 2026 (accelerated implementation) |
| Record created | 25 November 2026 (Europe/Dublin) |
| Record type | Retrospective step record; implementation dates retained |
| Status | IMPLEMENTED / release evidence recorded |
| Dependencies | MED-01 |
| Owner | Utpal Mishra; implementation/recording by Codex |

## Scope and rationale

Private uploads and recording playback. Track this outcome independently so a planned requirement can be located without treating an entire release as one completed task.

## Affected files or evidence records

- [web/worker/media.js](../../web/worker/media.js)
- [web/worker/media-ui.js](../../web/worker/media-ui.js)

## Implementation and history

[Implementation ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144)

Shared historical implementation commit; this record isolates documentation and scope only. Its recording commit does not isolate the old runtime change.

## Acceptance evidence

Signature, credit, transcript, VTT and size checks; released audio byte-range tests, including invalid ranges.

Evidence above is from the existing implementation/release record or an identified requirement. Creating this step record does not rerun tests, create a new deployment, activate a provider or attest real editorial approval.

## Remaining work and limits

An owner must review actual uploaded rights and factual support.

## Rollback or recovery

Do not revert the shared implementation commit for this step alone: it also contains other features. Inspect the named files/dependencies and prepare a bounded corrective commit. Applied migrations and story/media history require forward recovery.

## Related records

- [Step index](../STEP_TRACEABILITY.md)
- [Daily development evidence](../DAILY_DEVELOPMENT.md)
- [Structured project logs](../PROJECT_LOGS.md)
