# WEB-08 — Website release, GitHub integration and deployment

| Field | Value |
| --- | --- |
| Planned | Website completion phase, 25 November 2026 |
| Actual implementation | 25 November 2026 |
| Record date | 25 November 2026 (Europe/Dublin) |
| Status | LOCAL VALIDATION PASSED / GitHub release in progress |
| Dependencies | Existing version 6 website and earlier WEB steps where applicable |

## Scope and acceptance

Run meaningful checks, synchronize separate commits, obtain actual CI evidence, integrate the website branch and deploy the existing owner-private Site; record external blockers separately.

## Evidence and implementation

Local release evidence: Worker build, 74 website tests and 54 Python tests passed on 25 November 2026; browser smoke covered guided creation, unsaved navigation, workspace, story reading and offline saving. GitHub PR #6 contains the release. Terminal Git write authentication is unavailable; separate commits are transferred through the connected GitHub Git-data API. Local origin SHAs are preserved in remote commit messages.

The merge preserves both the media/website development records and the 25 November morning verification from main. Deployment and remote CI results will be appended only after actual returned success. No changes to audience, schedules or editorial approval.

Recovery: redeploy prior private Site version 6 for code rollback; retain existing D1/R2 data. No new migration is required for WEB-01–WEB-07.

## Recovery and limits

Use a bounded forward fix; preserve existing content and applied migrations. Provider credentials, actual editorial approval, physical-device testing and native apps are not fabricated by this step.
