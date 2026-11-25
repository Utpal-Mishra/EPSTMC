# REL-09 — Editorial regional release

Planned and recorded: 25 November 2026 (Europe/Dublin). Actual implementation: 25 November 2026. Status: DEPLOYED v8 / MERGED PR #7.

Scope and acceptance: see STEP_TRACEABILITY.md. Dependencies: private v7 website; NEWS-02 depends on NEWS-01 and DESIGN-01; REL-09 depends on all three.

Evidence and implementation: pending. Per-step implementation commit retains the step ID.

Recovery: revert the bounded code step; preserve story history and editorial gates. New ingestion storage is additive. No schedule or audience change. Provider activation, publication and exhaustive coverage are not implied.

## Release checks — 25 November 2026

Implemented and locally validated. Worker build passed; 82 website and 54 Python tests passed. Browser verified the actual editorial page, Europe filter (78 past-month headlines), combined Europe/Economy filter (15), shareable route state, exact 64-row ECB table and computed Playfair Display / DM Sans fonts. Source snapshot: 244 records, 223 unique URLs, eleven successful source feeds, 64 market points; retrieval timestamps retained. Recent wording distinguishes publication windows from event dates. No synthetic story approval or public access change.

The command environment could not connect to the daemon preview over its loopback address; browser preview worked. This is not a live deployment or production refresh validation. Native/mobile QA and authenticated live-browser validation remain separate. GitHub transfer and deployment result will be appended after confirmation.

Recovery: deploy prior v7 for runtime rollback; preserve additive news tables and existing editorial data. No changes to existing schedules or audience.

Source-status correction during release: a failed first runtime refresh now retains the bundled snapshot’s previous successful timestamp and count. Regression assertion verifies it. No provider error details or credentials are displayed.

## Confirmed release — 25 November 2026

- GitHub [PR #7](https://github.com/Utpal-Mishra/EPSTMC/pull/7) merged into main at `b0df4eb18f1f50e2708ebf92ca5c215847a5e527`.
- Exact local/GitHub runtime tree match verified: `dc8dadeefde083e3d378680518aa2aa5b029588c`.
- Existing owner-private Site version **8** deployed successfully at https://epstmc-reader-review.utpalmishra21.chatgpt.site .
- Deployment `appgdep_6b06f8c828dc8191b899a79e4a20e8d0`; hosted source `baf3e2aca3afd9295e2638d49e1a7ad8e1e7554d`; environment revision 1.
- Release checks: Worker build, **82 website tests**, **54 Python tests** passed; browser styling, regional/category URL filtering and exact rate table verified in preview.
- Initial snapshot: **244 imported records / 223 unique article URLs / 11 successful feeds / 64 ECB observations**. Retrieval and publication dates remain distinct.
- GitHub returned no workflow-run evidence for the revision; remote CI remains unverified. The live browser requires owner sign-in, so authenticated production smoke and live refresh were not validated in that session.
- Recent production Worker error-log query returned no events; this alone is not proof of all authenticated workflows.
- No publication approval, source exhaustiveness, public audience change, native-device QA or schedule modification is claimed.
- Rollback remains previous private Site v7. Preserve additive regional tables and existing D1/R2 data.

### Separate implementation provenance

| Local implementation | GitHub commit |
| --- | --- |
| `0dfd70162ab9e38aa7b652c6c000e44b2e3328f9` | [`7ab583ed`](https://github.com/Utpal-Mishra/EPSTMC/commit/7ab583ede555dc78f923d2db9b403787188660b5) |
| `4b2481fc002dbbc2dc070a938298502c1ceb677f` | [`00ca3001`](https://github.com/Utpal-Mishra/EPSTMC/commit/00ca30012588f07d62ac08bc09c7c6b3a11659d8) |
| `1890c0b720275a28386c32b712528e8dfbe3967e` | [`f9b67de6`](https://github.com/Utpal-Mishra/EPSTMC/commit/f9b67de6f79c3d512a12773f1af804d45d0d2698) |
| `ac7ccd37024129c99291c68452fd1f1984764805` | [`a49d4614`](https://github.com/Utpal-Mishra/EPSTMC/commit/a49d46140b93baa57f535706b7c25ba96d647b66) |
| `b3907956df2746d0e8d9abdec1f4930c223a37e6` | [`d4674642`](https://github.com/Utpal-Mishra/EPSTMC/commit/d467464272925fde7f191bfb00032bbddf40a320) |
| `de57d1722193e1568006a96412b895e118a38989` | [`6d95a39e`](https://github.com/Utpal-Mishra/EPSTMC/commit/6d95a39ebe96b3ceeef790f62efd40e8856fa4c3) |

Connected GitHub APIs preserved each planned implementation step and local origin; no published history was rewritten.
