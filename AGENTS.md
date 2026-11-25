# EPSTMC development records

- Follow the owner instruction to keep every planned update separately traceable.
- Before implementation, assign a stable step ID and identify dependencies and acceptance criteria in docs/steps/ and docs/STEP_TRACEABILITY.md.
- Use one planned implementation step per commit; include its ID in the subject. Keep that step's code, meaningful checks and record update together. Do not combine unrelated image, audio, video, storage, review, analytics or release work in one implementation commit.
- Record planned date, actual implementation date and record/update date separately. Never backdate accelerated work or imply that work-unit labels represent elapsed days.
- Each step record must state scope, rationale, files, implementation commit links, evidence, status, dependencies, remaining work and rollback/recovery implications.
- Keep implemented, locally validated, remotely integrated, deployed, provider activated and editorially approved distinct.
- Update the relevant structured project logs; retain the existing 13 log categories. Use the step ID to cross-reference entries rather than merging distinct steps into one summary.
- Preserve published history. For older combined implementations, add clearly labelled retrospective per-step records that reference the shared original commit. A documentation commit is not a separately isolated code change or a historical test rerun.
- Do not rewrite, squash, reset or force-push published history merely to make past work look granular. Preserve the original/local-to-remote commit relationship when synchronization remaps IDs.
- Release, deployment, QA, source/provider activation and source-control integration each require their own event record and actual evidence. Pending operational steps must not be marked complete because software exists.
- Keep project conversations, secrets and personal data out of source and records. Preserve the current Site audience. Do not change schedules unless requested.
