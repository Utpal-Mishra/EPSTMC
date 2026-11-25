# REL-01 — Full local release checks

| Field | Value |
| --- | --- |
| Step ID | REL-01 |
| Phase | Release and synchronization |
| Planned window | 24 November 2026 |
| Actual implementation/event | 24 November 2026 |
| Record created | 25 November 2026 (Europe/Dublin) |
| Record type | Retrospective step record; implementation dates retained |
| Status | COMPLETED / separately recorded |
| Dependencies | MED-01 through MED-14 |
| Owner | Utpal Mishra; implementation/recording by Codex |

## Scope and rationale

Full local release checks. Track this outcome independently so a planned requirement can be located without treating an entire release as one completed task.

## Affected files or evidence records

- [web/tests/media.test.mjs](../../web/tests/media.test.mjs)
- [tests/test_render_explainer.py](../../tests/test_render_explainer.py)
- [.github/workflows/editorial.yml](../../.github/workflows/editorial.yml)

## Implementation and history

[Implementation ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144)

Original unit has its own implementation/event commit.

## Acceptance evidence

54 Python and 45 website tests passed locally; Worker build passed.

Evidence above is from the existing implementation/release record or an identified requirement. Creating this step record does not rerun tests, create a new deployment, activate a provider or attest real editorial approval.

## Remaining work and limits

These are historical check results, not a fresh rerun or a remote CI claim.

## Rollback or recovery

This is an event/evidence record. Reverting this document cannot undo a deployment, approval or synchronization. Any operational reversal requires a separately recorded authorized action.

## Related records

- [Step index](../STEP_TRACEABILITY.md)
- [Daily development evidence](../DAILY_DEVELOPMENT.md)
- [Structured project logs](../PROJECT_LOGS.md)
