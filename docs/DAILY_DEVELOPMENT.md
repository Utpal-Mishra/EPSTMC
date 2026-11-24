# EPSTMC daily development tracker

Each row is a bounded milestone work unit, not a claim that seven calendar days
have elapsed. The original Week 4 planning window is 28 November–4 December
2026. The owner requested accelerated Week 4 development on 23 November; all
local work below was performed on that date. Commits retain the Day 1–7 work
unit in their titles for granular Git history. Local completion, GitHub
integration and production verification are separate statuses.

| Unit | Planned outcome | Local evidence / status | GitHub / operational status (all units merged via PR #1) |
| --- | --- | --- | --- |
| W4-D1 | Approved publication data and service | IMPLEMENTED: migration 003, `publishing.py`; version/sequence checks, immutable publications and audit transaction. | GitHub commit `28c742d`; uploaded in PR #1; approval recorded 23 Nov. |
| W4-D2 | Publication boundaries and corrections | VALIDATED locally: unpublished approvals hidden, prior versions retained, private fields filtered, concurrent publication checked. | GitHub commit `5718cea`; Postgres 16 CI passed. |
| W4-D3 | Public read API | IMPLEMENTED: feed, story, versions, readiness, GET/HEAD, cache validation and sanitized failures. | GitHub commit `e445d07`; hosted endpoint not deployed. |
| W4-D4 | Connected reader application | IMPLEMENTED: evidence desk, source links, historical comparison limits, scenario signals and publication history. | GitHub commit `bab11fc`; browser visual QA pending. |
| W4-D5 | End-to-end correction demonstration | VALIDATED locally: real WSGI interface tests and isolated fictional demo database with two published versions. | GitHub commit `aadeb42`; no real editorial story approved or published. |
| W4-D6 | Regression and integration checks | VALIDATED locally: rollback, stale approved version, real read connections and demo safeguards; CI matrix prepared. | GitHub commit `322eccc`; CI runs on GitHub; all release CI jobs passed; merged via PR #1. |
| W4-D7 | Release documentation and daily tracking | IMPLEMENTED: runbook, API contract, audit logs, truthful milestone statuses and daily task update. | GitHub commit `b2ff7c6`; merged into main via PR #1 (`04f136e`). |

## Next run procedure

1. Fetch current GitHub state and inspect relevant local/remote branches before
   selecting work. Never discard or recreate already completed units just because
   a push is blocked or a planned date has arrived.
2. Publication of the combined Weeks 1–4 changes was explicitly authorised on
   23 November 2026. The branch is uploaded; the earlier approval blocker is
   resolved. PR #1 merged into main on 23 November (`04f136e`); all release
   CI jobs passed. Continue with the next genuinely incomplete work unit.
3. Fix any failing required CI checks before integration. Preserve concurrent
   upstream work and use fast-forward branch updates; never force push. Code
   integration does not imply a hosted deployment or real editorial publication.
4. Follow [NEXT_7_DAYS.md](NEXT_7_DAYS.md) for 24–30 November: one real story
   from history to present, with one tested website/code increment each day.
   The owner subsequently requested the complete seven-unit set in the current
   session; see HISTORY_TO_PRESENT.md for the implemented release. Follow-up
   daily runs check reliability, source intake and bounded fixes. Do not rebuild
   completed units or backdate the implementation.
5. Record real date, task ID, commit/PR, tests, files, blockers and next task. Use
   the README status markers for one idempotent entry per calendar date. Keep
   proposed, implemented, validated, integrated and deployed distinct. Preserve
   the structured audit logs. No invented progress, production approvals or
   deployment claims.

The existing daily task was updated on 23 November 2026 to implement a bounded next task rather
than only maintain the README. The same task now has seven dated runs for 24–30 November; no duplicate
recurring task is needed. Its approximate morning slot is retained. If execution, credentials or authorization are missing,
report the blocker and perform only independently authorized work.


## 24 November 2026 — Freshness verification

Bounded follow-up: one live Federal Register intake and independent durable-status
verification. No observed release failure or incomplete seven-unit requirement
justified an application change. No code/website rebuild, approval or publication.

- Baseline main: [6223a45](https://github.com/Utpal-Mishra/EPSTMC/commit/6223a458538e55d38819888b35f6b2cec9ed36cf).
  [PR #3](https://github.com/Utpal-Mishra/EPSTMC/pull/3) merged on
  23 November at `3335c51`. Its head and current main both have successful
  website, Python 3.9/SQLite, Python 3.12/SQLite and Postgres checks.
  [Current main CI](https://github.com/Utpal-Mishra/EPSTMC/actions/runs/45291255600).
- `get_site` confirmed active version 5, custom owner-only access, no viewers,
  editors or groups. Existing URL and source repository retained. Supported
  private service access succeeded; no access or credential change.
- POST `/api/service/intake`: HTTP 200; attempt `2026-11-24T09:48:40.662Z`,
  successful completion `2026-11-24T09:48:40.952Z`, 20 matches processed.
  These are unreviewed search candidates, not 20 new records or story developments.
  Only one intake was requested; the one-minute throttle was respected.
- Subsequent GET `/api/service/status`: HTTP 200; the last attempt and last
  successful intake match those timestamps. Persisted story is research preview,
  draft version 1, publication sequence 0, five events, no publication.
- Latest covered event: **6 November 2026**. Original-source publications span
  17 January 2025–6 November 2026; source retrieval and full research check remain
  `2026-11-23T22:59:31+00:00`. Today's search does not reverify those sources.
  The unverified agency response and operational-status gaps remain explicit.
- Validation: 45 local Python/SQLite tests passed. No application changes;
  Worker and Postgres behavior are supported by the passing baseline CI above.
  Documentation PR checks/merge are recorded at the follow-up PR link below.
- Deployment: version 5 unchanged at
  https://epstmc-reader-review.utpalmishra21.chatgpt.site. No redeployment needed
  for this documentation-only record. Implemented/merged code, deployed runtime
  and editorial approval remain separate.
- Blockers: no service/release blocker observed. Owner editorial review and
  physical-device QA remain pending. Next: review queued candidate relevance or
  an observed coverage/access/mobile regression; do not fabricate a daily fix.
- Schedule: existing 24–30 November run window retained; no schedule changes.


Follow-up: [PR #4](https://github.com/Utpal-Mishra/EPSTMC/pull/4), initial evidence
commit [3405e34](https://github.com/Utpal-Mishra/EPSTMC/commit/3405e34dc1e76be4091302ae87ddaf3b86e15d04).
The PR provides the authoritative check and merge status; no application files changed.
