# HTP-D3 — Year and month timeline navigation

| Field | Value |
| --- | --- |
| Step ID | HTP-D3 |
| Phase | History to present |
| Planned window | 26 November 2026 (original target; superseded) |
| Actual implementation/event | 23 November 2026 (historical implementation record) |
| Record created | 25 November 2026 (Europe/Dublin) |
| Record type | Retrospective step record; implementation dates retained |
| Status | IMPLEMENTED / historical release validated |
| Dependencies | Previous HTP unit |
| Owner | Utpal Mishra; implementation/recording by Codex |

## Scope and rationale

Year and month timeline navigation. Track this outcome independently so a planned requirement can be located without treating an entire release as one completed task.

## Affected files or evidence records

- [web/worker/ui.js](../../web/worker/ui.js)

## Implementation and history

[Implementation d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61)

Shared historical implementation commit; this record isolates documentation and scope only. Its recording commit does not isolate the old runtime change.

## Acceptance evidence

Recorded browser check selected 2026/November and displayed one matching event.

Evidence above is from the existing implementation/release record or an identified requirement. Creating this step record does not rerun tests, create a new deployment, activate a provider or attest real editorial approval.

## Remaining work and limits

Physical-device QA remains separate.

## Rollback or recovery

Do not revert the shared implementation commit for this step alone: it also contains other features. Inspect the named files/dependencies and prepare a bounded corrective commit. Applied migrations and story/media history require forward recovery.

## Related records

- [Step index](../STEP_TRACEABILITY.md)
- [Daily development evidence](../DAILY_DEVELOPMENT.md)
- [Structured project logs](../PROJECT_LOGS.md)
