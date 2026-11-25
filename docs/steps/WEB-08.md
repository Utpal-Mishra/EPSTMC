# WEB-08 — Website release, GitHub integration and deployment

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | DEPLOYED / MERGED TO MAIN; remote CI unverified |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Run meaningful checks, synchronize separate commits, obtain actual CI evidence, integrate the website branch and deploy the existing owner-private Site; record external blockers separately.

## Evidence and implementation

Local release evidence: Worker build, 74 website tests and 54 Python tests passed on 25 November 2026; browser smoke covered guided creation, unsaved navigation, workspace, story reading and offline saving. GitHub PR #6 contains the release. Terminal Git write authentication is unavailable; separate commits are transferred through the connected GitHub Git-data API. Local origin SHAs are preserved in remote commit messages.

The merge preserves both the media/website development records and the 25 November morning verification from main. Deployment and remote CI results will be appended only after actual returned success. No changes to audience, schedules or editorial approval.

Recovery: redeploy prior private Site version 6 for code rollback; retain existing D1/R2 data. No new migration is required for WEB-01–WEB-07.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.


## Verified release result — 25 November 2026

- GitHub PR #6 merged successfully into main at `617216ee57fb01ed55356667b6f7387d12f21305`: https://github.com/Utpal-Mishra/EPSTMC/pull/6 .
- Local merged tree and GitHub main tree are identical: `bd66f6f8ab1135b9b83bd113b9df6558879f1d93`.
- Private Site **version 7** deployed successfully at https://epstmc-reader-review.utpalmishra21.chatgpt.site .
- Deployment ID: `appgdep_6b06b7c799d881919e5df0d0baa6274b`; hosted source `f699111929e9dca8a0f8a3921e7779537940e539`; environment revision 1.
- Deployment archive SHA-256: `692dc382c12aef50585e0f9abc03f5ad33497d52ca31e08d50ca084d20589d21`.
- Local release validation: 74 website tests, 54 Python tests, Worker build, browser guided-form/unsaved-dialog/workspace/reader/offline-save smoke checks.
- GitHub returned no workflow runs or combined statuses for the revision. Remote CI is **unverified**, not successful. The workflow remains configured for SQLite 3.9/3.12, Postgres 16, website and video export.
- Live browser reached the owner-private ChatGPT sign-in gate. The current cloud session is not signed in; authenticated live application behavior was not re-tested. Deployment succeeded according to the publishing service. Recent Worker error-log query returned no events.
- No provider credentials were configured, no real story approved/published, and no audience or schedule changed. Browser recording capture, offline cold-start behavior and physical devices remain incompletely verified.

### Preserved local-to-GitHub implementation mapping

Terminal push could not authenticate, so connected GitHub Git-data APIs created the separate commits without rewriting any published history. Remote messages preserve local origins.

| Local commit | GitHub commit |
| --- | --- |
| `b06d54ed75bc7d133eb27e3077abd3272746fe0d` | [`c4923dea`](https://github.com/Utpal-Mishra/EPSTMC/commit/c4923dea906429f76213289b4222b900f45e120b) |
| `3554cc5d028a700deadb1856a83397c2a68f7d7b` | [`72b1f768`](https://github.com/Utpal-Mishra/EPSTMC/commit/72b1f7687ec8cdca35b78f2a625e5e3245c95fa2) |
| `a6e73370e178634567cbe54ff37d51d6c8d0acb6` | [`efb780bc`](https://github.com/Utpal-Mishra/EPSTMC/commit/efb780bc0e835783ef539347554cf349016047f3) |
| `97a85ccead1c8199f3d8203ec94361a1c8c04e52` | [`5b2f032d`](https://github.com/Utpal-Mishra/EPSTMC/commit/5b2f032dc1e3d1ab4f10e4c8adcc42b06ce69353) |
| `f26e1d7d8e1fd6d71e4ce510b59dbb08711c41c6` | [`c6b7a904`](https://github.com/Utpal-Mishra/EPSTMC/commit/c6b7a904dfe8e85cfc7787e114cbb0272592fdba) |
| `f738276e5ca717e81ef25fbf62436f8c63d5439a` | [`2e9bab36`](https://github.com/Utpal-Mishra/EPSTMC/commit/2e9bab365c0fa4326b88d20890bb381a65baf310) |
| `015e0649bf2df7e95dc3db2a3d3a4f340888493d` | [`374b5665`](https://github.com/Utpal-Mishra/EPSTMC/commit/374b5665344e79ab7fc16a9ed592134f529c3670) |
| `12b456f3ded2a0ca94dcf67b3161ebb38a627467` | [`9d06e661`](https://github.com/Utpal-Mishra/EPSTMC/commit/9d06e6616e426460b0f609f663229dcead219774) |

The local merge origin `97b07df` maps to GitHub `c73768ca28cb6e76fca714297463a330006873e1`; PR integration is a subsequent merge event.
