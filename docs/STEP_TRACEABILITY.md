# EPSTMC step-by-step traceability

Updated 25 November 2026 (Europe/Dublin). This is the entry point for tracing each planned outcome, the source change that delivered it, its acceptance evidence and what remains open.

## How to trace a step

Open its separate record below, then follow **Implementation and history** for the code or event commit. The **Recording commit** column points to the separate documentation commit created for that step. These are different facts: a retrospective record does not create a new historical implementation or rerun validation.

Planned dates, actual implementation/event dates and record dates are separate fields inside every record. Accelerated work is not spread across invented calendar days. A pending milestone has no completed implementation asserted.

## Existing history and rollback limits

- The seven website units W5-D1–D7 already have distinct implementation commits.
- HTP-D1–D7 were implemented together historically. Their records link to that shared commit.
- The media scope was implemented in one shared historical commit, `ea14e786`. MED-01–MED-14 are separate requirement/evidence records; their code was not originally split into independent commits.
- Published history has been preserved. No reset, squash, rebase or force push was used to make old work look granular. Do not revert a shared commit for just one feature; prepare a bounded fix with its dependencies instead.
- Connected GitHub synchronization creates new commit IDs. `Original-Commit` trailers retain local IDs; each uploaded tree is checked against its local tree.
- Each record below was added in its own new recording commit. Future implementation follows [the project instructions](../AGENTS.md): one planned step per implementation commit, with its record and relevant evidence updated alongside it.

## History to present

| Step | Separate record | Status | Implementation / event origin | Recording commit |
| --- | --- | --- | --- | --- |
| HTP-D1 | [Real source-backed story](steps/HTP-D1.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [b8ba95cf](https://github.com/Utpal-Mishra/EPSTMC/commit/b8ba95cf7e837f5892d1afb6338db45459c2b46d) |
| HTP-D2 | [Evidence chronology and provenance](steps/HTP-D2.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [7b1028d6](https://github.com/Utpal-Mishra/EPSTMC/commit/7b1028d6eeb6c7e0a2ca7696c884eacfbbf97432) |
| HTP-D3 | [Year and month timeline navigation](steps/HTP-D3.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [93722709](https://github.com/Utpal-Mishra/EPSTMC/commit/93722709ec7a595626d171b508764ef30af88007) |
| HTP-D4 | [Source intake and freshness](steps/HTP-D4.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [c83eb839](https://github.com/Utpal-Mishra/EPSTMC/commit/c83eb839c36bea018fb5059a63396ab010ca1bd5) |
| HTP-D5 | [Protected browser editorial review](steps/HTP-D5.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [931c1d83](https://github.com/Utpal-Mishra/EPSTMC/commit/931c1d835716471624adcec77a6ce00953221ad8) |
| HTP-D6 | [Durable story and version storage](steps/HTP-D6.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [be9b5d0d](https://github.com/Utpal-Mishra/EPSTMC/commit/be9b5d0d90232930b8a150f93c1eed9ac6dd467e) |
| HTP-D7 | [History-to-present validation](steps/HTP-D7.md) | IMPLEMENTED / historical release validated | [d59e9959](https://github.com/Utpal-Mishra/EPSTMC/commit/d59e9959f348929689323e66e16a1c5275d8cf61) (shared) | [14707ac0](https://github.com/Utpal-Mishra/EPSTMC/commit/14707ac05925acd03193c9db1590be5e630c4cb3) |

## Website expansion

| Step | Separate record | Status | Implementation / event origin | Recording commit |
| --- | --- | --- | --- | --- |
| W5-D1 | [Multiple stories and isolated publication](steps/W5-D1.md) | IMPLEMENTED / deployed in private Site v6 | [c3768e46](https://github.com/Utpal-Mishra/EPSTMC/commit/c3768e469ada757b094923d13f3016be4d16d629) | [09ed1b27](https://github.com/Utpal-Mishra/EPSTMC/commit/09ed1b2781f3e24e5141091aab5a677165b54634) |
| W5-D2 | [Region/category taxonomy and ordering](steps/W5-D2.md) | IMPLEMENTED / deployed in private Site v6 | [cdcb41c1](https://github.com/Utpal-Mishra/EPSTMC/commit/cdcb41c1093cd5c1abc5ecca5b5a4a839080a8be) | [447ef7f5](https://github.com/Utpal-Mishra/EPSTMC/commit/447ef7f55bc4caab9d730019ae37d0c7b1295bfc) |
| W5-D3 | [Feed and region/category filters](steps/W5-D3.md) | IMPLEMENTED / deployed in private Site v6 | [2577cba6](https://github.com/Utpal-Mishra/EPSTMC/commit/2577cba60310a1c1b2ae69503dcabbbbd0d63ff9) | [6fe6cadd](https://github.com/Utpal-Mishra/EPSTMC/commit/6fe6caddd97f254ece288af5fcdddc128ff67af7) |
| W5-D4 | [Search and event-date periods](steps/W5-D4.md) | IMPLEMENTED / deployed in private Site v6 | [3ca95793](https://github.com/Utpal-Mishra/EPSTMC/commit/3ca95793b230046afd304be488ae2f4b4a23edb5) | [556ced72](https://github.com/Utpal-Mishra/EPSTMC/commit/556ced72c65be12e9c91792671a047bff38300aa) |
| W5-D5 | [Saved reading on this browser](steps/W5-D5.md) | IMPLEMENTED / deployed in private Site v6 | [097fae9e](https://github.com/Utpal-Mishra/EPSTMC/commit/097fae9ef5e5800354702894ce6129d069d3c594) | [70943b5f](https://github.com/Utpal-Mishra/EPSTMC/commit/70943b5fcb33db83af334aab75526f523f3de2ff) |
| W5-D6 | [Deep links and research creation controls](steps/W5-D6.md) | IMPLEMENTED / deployed in private Site v6 | [78783c98](https://github.com/Utpal-Mishra/EPSTMC/commit/78783c989b694db5823e40364b8a4b4145542062) | [af3d9736](https://github.com/Utpal-Mishra/EPSTMC/commit/af3d9736cfc40666019207a73c65db50135a7d0b) |
| W5-D7 | [Website expansion validation](steps/W5-D7.md) | IMPLEMENTED / deployed in private Site v6 | [4a5a72f4](https://github.com/Utpal-Mishra/EPSTMC/commit/4a5a72f4bf66a112cc07aef545fd4dc735c4e689) | [7e4cc26b](https://github.com/Utpal-Mishra/EPSTMC/commit/7e4cc26b06571a3eaccf0ff0395b44fec5784828) |

## Two-week media scope

| Step | Separate record | Status | Implementation / event origin | Recording commit |
| --- | --- | --- | --- | --- |
| MED-01 | [Shared media records and private storage](steps/MED-01.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [8f048936](https://github.com/Utpal-Mishra/EPSTMC/commit/8f0489361d3cccd352224e8965b9a4933365d0a7) |
| MED-02 | [Story-derived narration and storyboard contract](steps/MED-02.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [4e35df6b](https://github.com/Utpal-Mishra/EPSTMC/commit/4e35df6bd3032944b8e398179cceb844142c97e4) |
| MED-03 | [Image-with-content and evidence diagrams](steps/MED-03.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [3a5706d7](https://github.com/Utpal-Mishra/EPSTMC/commit/3a5706d792cf110f6e3670b675ea7527d624a4c5) |
| MED-04 | [Optional provider image generation](steps/MED-04.md) | IMPLEMENTED / fixture-validated; PROVIDER ACTIVATION PENDING | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [55ce561b](https://github.com/Utpal-Mishra/EPSTMC/commit/55ce561b99478ff1fe661a867dcc142848f078a2) |
| MED-05 | [Browser listening, chapters and transcript](steps/MED-05.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [6e5a6c9e](https://github.com/Utpal-Mishra/EPSTMC/commit/6e5a6c9e7e9d1cd58d861f3caae6afcd5150a586) |
| MED-06 | [Optional provider narration and PCM assembly](steps/MED-06.md) | IMPLEMENTED / fixture-validated; PROVIDER ACTIVATION PENDING | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [1b9c54c0](https://github.com/Utpal-Mishra/EPSTMC/commit/1b9c54c0c973643f8cafdfaddacf971be1b8d7d4) |
| MED-07 | [Captioned interactive visual explanation](steps/MED-07.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [25622144](https://github.com/Utpal-Mishra/EPSTMC/commit/25622144e95a3b9469d6c5de2dadeb11f93b5ecb) |
| MED-08 | [Actual MP4 export and provenance sidecars](steps/MED-08.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [86bf1ae4](https://github.com/Utpal-Mishra/EPSTMC/commit/86bf1ae451774c6d02fe418ced497deabac55cf6) |
| MED-09 | [Private uploads and recording playback](steps/MED-09.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [220eae02](https://github.com/Utpal-Mishra/EPSTMC/commit/220eae028e0024014af47c5b42ad803ffe049ba0) |
| MED-10 | [Independent media review and withdrawal](steps/MED-10.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [8ef78e96](https://github.com/Utpal-Mishra/EPSTMC/commit/8ef78e968a4f4bb13adf1645a5170726dd73f712) |
| MED-11 | [Corrections, old versions and immutable media](steps/MED-11.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [de1151ef](https://github.com/Utpal-Mishra/EPSTMC/commit/de1151ef7932c216d9755356d81ed21fac461346) |
| MED-12 | [Generation quotas, idempotency and interruption](steps/MED-12.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [217c385b](https://github.com/Utpal-Mishra/EPSTMC/commit/217c385b09433bd50b41a81000a28f4987e3c8c3) |
| MED-13 | [Questions, corrections and source feedback](steps/MED-13.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [8cadae1f](https://github.com/Utpal-Mishra/EPSTMC/commit/8cadae1f923b815fce5e862c00cd5b34054a4c17) |
| MED-14 | [Opt-in aggregate interaction measurements](steps/MED-14.md) | IMPLEMENTED / release evidence recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [69442f2e](https://github.com/Utpal-Mishra/EPSTMC/commit/69442f2e9553874a8e9d3bc52cd4e42f6c6fbd03) |

## Release and synchronization

| Step | Separate record | Status | Implementation / event origin | Recording commit |
| --- | --- | --- | --- | --- |
| REL-01 | [Full local release checks](steps/REL-01.md) | COMPLETED / separately recorded | [ea14e786](https://github.com/Utpal-Mishra/EPSTMC/commit/ea14e786eb7599b77d788122523f168a19b11144) (shared) | [def51e3d](https://github.com/Utpal-Mishra/EPSTMC/commit/def51e3d5057bf08cb8d2e448e3af0aee3fbd6e2) |
| REL-02 | [Private Site version 6 deployment](steps/REL-02.md) | COMPLETED / separately recorded | [a80bbc3a](https://github.com/Utpal-Mishra/EPSTMC/commit/a80bbc3aff2f0a16dccc12cdc16be0d1ec29db47) | [be7350e6](https://github.com/Utpal-Mishra/EPSTMC/commit/be7350e69fa08fd4e888d065af8e488521f12732) |
| REL-03 | [Live reader and media-studio smoke checks](steps/REL-03.md) | COMPLETED / separately recorded | [7e840ff4](https://github.com/Utpal-Mishra/EPSTMC/commit/7e840ff4d27b8ec093db8caf551b215cfc790053) | [1377e680](https://github.com/Utpal-Mishra/EPSTMC/commit/1377e68094a718fbfa28f0fe385c66f997e933b4) |
| REL-04 | [Explicit GitHub transfer approval](steps/REL-04.md) | COMPLETED / separately recorded | [9d55d46c](https://github.com/Utpal-Mishra/EPSTMC/commit/9d55d46cec6af63f7a9ebc33163e12409987b478) | [2af4d67d](https://github.com/Utpal-Mishra/EPSTMC/commit/2af4d67d637d20614b8ce8bf8801c5aeb56d8a7a) |
| REL-05 | [Verified GitHub branch synchronization](steps/REL-05.md) | COMPLETED / separately recorded | [a25a2b7c](https://github.com/Utpal-Mishra/EPSTMC/commit/a25a2b7c55dfb771815bd30f00d31b087958b9ec) | [c44c4b8f](https://github.com/Utpal-Mishra/EPSTMC/commit/c44c4b8f542aac2c6ecf63f2c58f46e45317258c) |

## Remaining operational work

| Step | Separate record | Status | Implementation / event origin | Recording commit |
| --- | --- | --- | --- | --- |
| OPS-01 | [Configure and validate live providers](steps/OPS-01.md) | PENDING | None; pending | [1362e777](https://github.com/Utpal-Mishra/EPSTMC/commit/1362e777faed809257473777c6e680e1979d659a) |
| OPS-02 | [Actual owner editorial and media review](steps/OPS-02.md) | PENDING | None; pending | [90c28688](https://github.com/Utpal-Mishra/EPSTMC/commit/90c286883f489e6ed643848a1f2068f92bbcb018) |
| OPS-03 | [Physical-device and accessibility QA](steps/OPS-03.md) | PENDING | None; pending | [5eadfa6d](https://github.com/Utpal-Mishra/EPSTMC/commit/5eadfa6d7053266cf8302847e721925bb5a985a3) |
| OPS-04 | [Hosted video rendering worker](steps/OPS-04.md) | PENDING | None; pending | [f08679b9](https://github.com/Utpal-Mishra/EPSTMC/commit/f08679b9e38966a049d95e8796444d2701465d12) |
| OPS-05 | [Remote CI and main integration](steps/OPS-05.md) | PENDING | None; pending | [54c2eb42](https://github.com/Utpal-Mishra/EPSTMC/commit/54c2eb424783015e821428b0918c99c7fc3e0155) |
| OPS-06 | [Expand verified news coverage](steps/OPS-06.md) | PENDING | None; pending | [2ff489d6](https://github.com/Utpal-Mishra/EPSTMC/commit/2ff489d643a90a9dc620a1c52ce0d73f5283a0f2) |

## Original native and launch roadmap

| Step | Separate record | Status | Implementation / event origin | Recording commit |
| --- | --- | --- | --- | --- |
| ROAD-05 | [Native account-free mobile feed](steps/ROAD-05.md) | PENDING / original roadmap milestone | None; pending | [581913c1](https://github.com/Utpal-Mishra/EPSTMC/commit/581913c10023e5b5195972e17c4983e6de050683) |
| ROAD-06 | [Automatic refresh and offline reading](steps/ROAD-06.md) | PENDING / original roadmap milestone | None; pending | [72ff03c0](https://github.com/Utpal-Mishra/EPSTMC/commit/72ff03c0f585013e0aba43d64463323c8a4af762) |
| ROAD-07 | [Optional push alerts and analytics](steps/ROAD-07.md) | PENDING / original roadmap milestone | None; pending | [52c44a1b](https://github.com/Utpal-Mishra/EPSTMC/commit/52c44a1bd091d0c155b0c82f10c6905a5e94fe7b) |
| ROAD-08 | [Closed beta on physical devices](steps/ROAD-08.md) | PENDING / original roadmap milestone | None; pending | [6ef39cee](https://github.com/Utpal-Mishra/EPSTMC/commit/6ef39ceec577a627a607fe496b6faebac2ad8ae8) |
| ROAD-09 | [Release preparation and store submission](steps/ROAD-09.md) | PENDING / original roadmap milestone | None; pending | [c8abc508](https://github.com/Utpal-Mishra/EPSTMC/commit/c8abc50848f00970b0d6ff93dc65e398827a1d19) |
| ROAD-10 | [Launch decision](steps/ROAD-10.md) | PENDING / original roadmap milestone | None; pending | [3f5f8049](https://github.com/Utpal-Mishra/EPSTMC/commit/3f5f8049a2a86ce905cee2e0231340d2e965fb93) |

## Earlier Weeks 1–4

Keep the original dated evidence rather than inventing a new retrospective daily sequence.

| Milestone | Existing granular source | Evidence distinction |
| --- | --- | --- |
| Week 1 prototype, scope and source selection | [README daily entries](../README.md#daily-development-status) and [original scope](EDITORIAL_POLICY.md) | Includes pending/no-change days and the later source selection; planned dates are not automatic completion. |
| Week 2 source ingestion and storage | [README first intake and Postgres setup](../README.md#first-source-intake) and [project logs](PROJECT_LOGS.md) | Local/shared storage, hosted D1 and unconfigured hosted Postgres remain different environments. |
| Week 3 draft and editorial review | [Week 3 walkthrough](WEEK3.md) and [W3 log entries](PROJECT_LOGS.md) | Software approval controls do not mean that the owner approved a real story. |
| Week 4 publishing and corrections, D1–D7 | [Daily table with separate commit links](DAILY_DEVELOPMENT.md) and [Week 4 guide](WEEK4.md) | Each existing W4 unit retains its recorded commit; source integration, hosted deployment and real publication remain distinct. |

## Structured-log cross references

The separate step records extend the existing logs rather than replacing their history.

| Log | Relevant records |
| --- | --- |
| Business Learning | W5-D3, MED-03, MED-05, MED-07 |
| System | HTP-D4, HTP-D6, MED-01, MED-09 |
| Architecture | HTP-D2, HTP-D6, MED-01, MED-11 |
| Automation | HTP-D4, MED-12; schedules unchanged |
| Recommendation | OPS-01 through OPS-06; pending work is explicit |
| Experiment | REL-01, MED-04, MED-06, MED-08 |
| External Evidence | HTP-D1, HTP-D2, OPS-06 |
| Risk & Assumption | MED-10, MED-11, MED-12, OPS-01, OPS-03 |
| Data & Integration | W5-D1, MED-01, MED-02, MED-09 |
| Product / Feature | W5-D1 through W5-D6, MED-03 through MED-09 |
| Merchant & Fulfilment | Not applicable to this release; no purchase or commerce work |
| Expansion | W5-D1, OPS-06, ROAD-05 through ROAD-10 |
| Decision | REL-04, REL-05; AGENTS.md defines the future recording rule |

## Verification of this documentation change

All 45 IDs are unique, each has a separate file and recording commit, file links are checked, and shared historical origins are labelled. Runtime, dependencies, migrations and deployed behavior were not changed. The last recorded implementation checks remain 54 Python and 45 website tests; this documentation update is not a fresh runtime test, provider activation, deployment or editorial approval.

## Website completion phase — planned 25 November 2026

| Step | Separate record | Acceptance scope | Status |
| --- | --- | --- | --- |
| WEB-01 | [Connected workspace and readiness dashboard](steps/WEB-01.md) | Aggregate story/review/media/feedback health with actionable navigation; expose configuration presence without secrets. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-02 | [Guided story creation and revision](steps/WEB-02.md) | Create and edit the complete source-backed story through labelled fields and repeatable sections; keep JSON as an optional advanced mode and preserve review controls. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-03 | [Complete feed, filters and shareable navigation](steps/WEB-03.md) | Feature the latest covered story honestly, add recent filtering, persist filter state in URLs and preserve story/timeline context. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-04 | [Explicit offline saved-reading workflow](steps/WEB-04.md) | Opt in to local story copies, cache only the app shell, read saved projections offline, show timestamps and allow clearing; never cache editorial data or credentials. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-05 | [Browser video production and media handoff](steps/WEB-05.md) | Produce actual captioned video in supported browsers, download transcript/captions and upload output for separate media review; preserve source version and file validation. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-06 | [Reader preferences, notifications and help](steps/WEB-06.md) | Connect browser-local preferences, opt-in counts and open-site update alerts; provide privacy/help/setup status with honest provider and background-push limits. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-07 | [Navigation, unsaved work and failure handling](steps/WEB-07.md) | Protect editorial edits, avoid stale route rendering, preserve playback, handle offline/unavailable states and verify the integrated website journey. | IMPLEMENTED / GitHub main / private Site v7; per-step QA limits retained |
| WEB-08 | [Website release, GitHub integration and deployment](steps/WEB-08.md) | Run meaningful checks, synchronize separate commits, obtain actual CI evidence, integrate the website branch and deploy the existing owner-private Site; record external blockers separately. | DEPLOYED v7 / merged PR #6; remote CI unverified |


## Editorial US / Europe expansion — planned 25 November 2026

| Step | Record | Acceptance | Status |
| --- | --- | --- | --- |
| DESIGN-01 | [Selected editorial design](steps/DESIGN-01.md) | Playfair Display / DM Sans, reference layout 07 visual edition + 04 timeline journal + 08 navy/mint source-backed market monitor; responsive and readable. | IMPLEMENTED / private v8 / PR #7 merged; per-step limits retained |
| NEWS-01 | [Regional ingestion](steps/NEWS-01.md) | Bounded allowlisted RSS/Atom intake, dated attributed headlines across US/Europe, per-source freshness/failure, durable deduplication; no automatic editorial approval. | IMPLEMENTED / private v8 / PR #7 merged; per-step limits retained |
| NEWS-02 | [Regional news desk](steps/NEWS-02.md) | Working region/category/time/search controls, source links, source health, recent headlines, retained reviewed stories and actual ECB reference-rate chart. | IMPLEMENTED / private v8 / PR #7 merged; per-step limits retained |
| REL-09 | [Editorial regional release](steps/REL-09.md) | Build and relevant tests, browser QA, GitHub synchronization and existing private Site deployment with honest limits. | IMPLEMENTED / private v8 / PR #7 merged; per-step limits retained |


## 26 November 2026 bounded maintenance

| Step | Record | Acceptance | Status |
| --- | --- | --- | --- |
| D26 | [Release and freshness verification](steps/D26.md) | Verify v8 release checks and one durable unreviewed intake; correct stale present-tense release labels. | VERIFIED / documentation integration pending CI; no runtime change |


## 27 November 2026 bounded maintenance

| Step | Record | Acceptance | Status |
| --- | --- | --- | --- |
| D27 | [Private access and freshness](steps/D27.md) | Anonymous denial, supported private service, one persisted unreviewed intake; no editorial changes. | VERIFIED / documentation integration pending CI; code unchanged |


## INT-01 — media integrations, 28 November 2026

See [step record](steps/INT-01.md). Implemented and locally checked; live provider activation pending credentials. Hosted source commit: `449fe08`. GitHub integration and deployment recorded separately in INT-03.


## INT-02 — media integrations, 28 November 2026

See [step record](steps/INT-02.md). Implemented and locally checked; live provider activation pending credentials. Hosted source commit: `d243afe`. GitHub integration and deployment recorded separately in INT-03.


## INT-03 — verified media release, 28 November 2026

[Release evidence](steps/INT-03.md): CI run 46101660350 succeeded; PR #10 merged; private Site v9 deployed. Provider keys and real output QA remain pending.

## WEB-09 — timeline filter alignment, 28 November 2026

| Step | Record | Acceptance | Status |
| --- | --- | --- | --- |
| WEB-09 | [Timeline filter alignment](steps/WEB-09.md) | Align both buttons with the Year and Month dropdowns, with matching heights and a usable narrow layout. Preserve filter and link behavior. | Implemented and locally validated |
