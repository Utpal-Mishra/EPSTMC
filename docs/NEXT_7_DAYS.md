# Seven website increments — original daily plan

**Superseded execution cadence:** the owner subsequently requested development
and integration of the full listed set in the current session. All seven units
are implemented in the history-to-present release; the original dated plan below
is retained as planning history. See [HISTORY_TO_PRESENT.md](HISTORY_TO_PRESENT.md).
The remaining seven scheduled runs check intake/reliability and make bounded
follow-up fixes rather than rebuilding these units.

Owner instruction recorded 23 November: develop and integrate the next seven
calendar days of updates, including the website, and update GitHub day by day.
Do not implement all seven units in advance and upload them together. This phase
prioritises one real story from historical evidence to the latest verified
update, ahead of native mobile delivery. The original ten-week roadmap is
retained as broader context; this is the next execution sequence.

Baseline: Weeks 1–4 merged through PR #1; private reader snapshot/export merged
through PR #2. There are 43 passing regression tests. Existing review site:
https://epstmc-reader-review.utpalmishra21.chatgpt.site/
Site ID: `appgprj_6b04bdf51930819196bfe67273bccb48`; preserve its owner-only audience.
The review site is currently a fictional static snapshot; do not describe it as
a live news service.

| Date | Unit | Planned development | Daily completion evidence | Status |
| --- | --- | --- | --- | --- |
| 24 Nov | HTP-D1 | Select one U.S. AI infrastructure/policy story; collect dated primary sources from history through the latest verifiable development. Add a clearly labelled private research preview using real source links. | Case-study data, per-claim source links, coverage/check dates, visible gaps and a tested private website preview. A draft is not editorially approved reporting. | PLANNED |
| 25 Nov | HTP-D2 | Add the evidence/event timeline contract with distinct event, publication and retrieval dates; chronology, provenance and duplicate checks. | Model/migration as needed, meaningful regression checks and dates visible on the site. | PLANNED |
| 26 Nov | HTP-D3 | Build connected yearly/monthly timeline navigation and a present-position summary for that story. | Working website navigation, original source links and explicit distinctions between fact, interpretation and scenario. | PLANNED |
| 27 Nov | HTP-D4 | Connect new-source intake to the story's update queue with safe retries, deduplication and last-successful-check status. | New evidence reaches review; repeat intake creates no duplicate; site displays truthful freshness/error states. | PLANNED |
| 28 Nov | HTP-D5 | Add protected browser review for the story's source-backed draft, comparisons and revisions. Keep real approval an explicit owner action. | Auth/access checks, review/change preview and unapproved-content isolation. A research preview remains labelled. | PLANNED |
| 29 Nov | HTP-D6 | Connect the private website to durable story/version data and refresh the reader from the approved projection. | Persistence across reload/restart, update/correction lineage and visible refresh time. If required credentials or hosting capabilities are absent, report the blocker and retain the labelled snapshot. | PLANNED |
| 30 Nov | HTP-D7 | Verify the history-to-present journey, corrections, source navigation, mobile layout, privacy and failure handling. Fix release blockers and document remaining coverage gaps. | End-to-end results, GitHub CI, private deployment version, release summary and next milestones. | PLANNED |

These are work targets, not guarantees. Do not invent recent events or fill a
missing historical period with generated facts. A verified historical source
alone does not establish present-day status. Human review and external setup may
remain pending independently of code completion.

## Execution and release rules

- Exactly one bounded unit per scheduled daily run, at most one newly completed
  HTP unit per Europe/Dublin calendar date. Inspect current branches and the
  date's entry before edits. A rerun may fix/retry that day's unit, not implement
  tomorrow's code. Never backdate commits or relabel one batch as seven days.
- Inspect current main, open PRs and this tracker; do not rebuild completed work.
  If dependencies block the planned unit, resolve the blocker or make an
  independent improvement within that unit. Do not mark it complete without
  evidence; the next run continues the earliest unfinished prerequisite.
- Build application changes and applicable website changes together. Run relevant
  local checks and GitHub SQLite/Python/Postgres CI. Use a dated branch/PR and
  merge after checks pass, preserving concurrent changes and without force push.
  Push that day's tested increment on that date; do not hold all seven for one
  release. Follow-up fixes may share the same daily PR.
- Update the existing private Site through its current source repository and
  manifest; use its owner-only deployment path. Do not create a duplicate Site,
  widen access, purchase services or expose credentials. GitHub integration and
  website deployment each need their own verified result.
- Research on public primary sources is allowed. Real source-backed drafts may
  appear only as clearly labelled private research previews until the owner
  explicitly reviews/approves them. Never fabricate reviewer attestations or
  automatically approve/publish a real story as reviewed reporting.
- Keep private conversations, personal data and secrets out of GitHub. Do not
  copy private audit archives into public source. Maintain the 13 structured
  project logs with implemented/tested/proposed/blocked distinctions.
- Record real date, unit ID, commit/PR links, tests, website version/link, blockers
  and next task. Update one README status entry per date between its markers.
- The existing task is configured for seven runs, 24–30 November, at its existing
  approximate morning slot (09:00 Europe/Dublin). It stops after those runs and
  does not silently extend this phase. No implementation code for these units is
  committed during setup on 23 November; only this plan and audit records change.

## Execution record

| Date | Unit | Commit / PR | Validation | Website result | Blocker / next action |
| --- | --- | --- | --- | --- | --- |
| 23 Nov | SETUP | Planning/configuration only | Baseline inspected; no new feature completion claimed | Existing private review retained | Begin HTP-D1 on 24 Nov. |


### Superseding implementation result

23 November 2026 — HTP-D1 through HTP-D7 implemented and integrated through
PR #3 (`3335c51`), with 45 Python and 18 Worker/D1 tests passing. The private
website is database-backed; live intake saved 20 pending candidates. The real
case stays unapproved until explicit owner review. Subsequent scheduled dates
perform reliability and source checks; they do not represent backdated feature
implementation. Physical-device QA and broader source coverage remain follow-up.
