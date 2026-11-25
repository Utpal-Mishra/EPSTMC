# MED-11 — Corrections, old versions and immutable media

| Field | Value |
| --- | --- |
| Step ID | MED-11 |
| Phase | Two-week media scope |
| Planned window | 5–7 December 2026 |
| Actual implementation/event | 24 November 2026 (accelerated implementation) |
| Record created | 25 November 2026 (Europe/Dublin) |
| Record type | Retrospective step record; implementation dates retained |
| Status | IMPLEMENTED / release evidence recorded |
| Dependencies | MED-10 |
| Owner | Utpal Mishra; implementation/recording by Codex |

## Scope and rationale

Corrections, old versions and immutable media. Track this outcome independently so a planned requirement can be located without treating an entire release as one completed task.

## Affected files or evidence records

- [web/worker/media.js](../../web/worker/media.js)
- [web/drizzle/0003_mighty_lifeguard.sql](../../web/drizzle/0003_mighty_lifeguard.sql)
- [web/drizzle/0004_media_integrity.sql](../../web/drizzle/0004_media_integrity.sql)

## Implementation and history

[Implementation ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144)

Shared historical implementation commit; this record isolates documentation and scope only. Its recording commit does not isolate the old runtime change.

## Acceptance evidence

Corrections isolate old assets; historical published versions retain their media; immutable-content guard test.

Evidence above is from the existing implementation/release record or an identified requirement. Creating this step record does not rerun tests, create a new deployment, activate a provider or attest real editorial approval.

## Remaining work and limits

Media must be regenerated/reviewed for changed story content.

## Rollback or recovery

Do not revert the shared implementation commit for this step alone: it also contains other features. Inspect the named files/dependencies and prepare a bounded corrective commit. Applied migrations and story/media history require forward recovery.

## Related records

- [Step index](../STEP_TRACEABILITY.md)
- [Daily development evidence](../DAILY_DEVELOPMENT.md)
- [Structured project logs](../PROJECT_LOGS.md)
