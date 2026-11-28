# INT-03 — Media integration release

Planned: 2026-11-28. Actual deployment and source integration: 2026-11-28. Record date: 2026-11-28.

Dependencies: INT-01 and INT-02. Scope: meaningful verification, traceable source integration and private deployment. No schema, sharing or schedule changes.

Acceptance evidence:
- Website suite: 93/93 passed. Focused media checks after final fixes: 33/33 passed. Fixtures cover OpenAI image/audio, Shotstack render/import, shared cap, idempotency, scope, output URLs and editorial approval.
- Browser: Workspace setup names and disabled media buttons verified in local preview. Deployed site reached sign-in gate; authenticated production UI and real paid output were not re-tested.
- GitHub workflow run 46101660350 completed successfully for e7c63963a28d90b34531ce3ca3ddb4511ff7e089.
- PR #10 merged: https://github.com/Utpal-Mishra/EPSTMC/pull/10 ; merge commit 7545b9991be46145ee8a7db34c4218740e3f9215.
- Native deployment succeeded at 2026-11-28T03:12:36.523661Z; existing owner-private Site version 9, source 4cbab3c005d5b0b0483c6fb19ea37f591af3aa05.

Implementation mapping:
- INT-01 hosted source 449fe08 → GitHub https://github.com/Utpal-Mishra/EPSTMC/commit/96554b8686805284af9120276cd290351d39040e
- INT-02 hosted source d243afe → GitHub https://github.com/Utpal-Mishra/EPSTMC/commit/e7c63963a28d90b34531ce3ca3ddb4511ff7e089
- Hosted release preparation 6e2b759; packaged release 4cbab3c005d5b0b0483c6fb19ea37f591af3aa05. The Site source repository contains the deployable web subtree; GitHub retains the full project and original histories.

Status: implemented, locally validated, CI verified, GitHub merged and deployed privately. Provider activation and paid-output QA remain pending server-side keys and available OpenAI model selections. No live provider calls, approvals or publications occurred.

Rollback: deploy previous Site version 8. No data migration; prior story/media versions and review history remain intact. Closing an interrupted job does not cancel remote rendering or billing.
