# 0817(A) — W1 before the drive: FORMAL conditional External1 option; migration path FAIL

Wed Oct 21 11:46:04 UTC 2026

**FORMAL answer.** Starting the campaign internally and then moving or spanning its work directory onto the new volume does **not** preserve the registered identity in the current stack. The compliant early-start option is a campaign that starts on External1 and remains on External1, with enough capacity made available there. This is a conditional option, not a launch readiness approval. If the campaign itself must inhabit the new drive, wait for that drive or begin a separately registered fresh campaign there; the existing cache cannot be silently transplanted.

The potential 12–18 h saving in 0817 is UNTESTED and survives only if the permanent External1 plan remains sufficient. HEADLINE11 must already be FINISHED and ACCEPTED and supply the exact H11 evidence; storage does not waive that dependency (V006 A192 item 4).

**What refuses (FORMAL from code; identity/ledger branches also TESTED on inert records).**

- STORAGE delegates `move` unchanged to STORAGE_PARENT. Its lines 121–151 resolve the candidate/work-dir paths and reject the campaign directory, any ancestor and any descendant, and every candidate containing a path pinned by the supplied pin sources. `move` is a checker, not a migration facility. It does not perform a move and does not establish that every file on a volume is movable.
- ORCH lines 631–718 bind the resolved path, crossed symlinks, mount point and VolumeUUID. A moved path raises WORK_DIR_REPOINTED; a replacement volume raises WORK_DIR_VOLUME_IDENTITY_MISMATCH. A same-spelling symlink or a disk mounted under the old name does not preserve these identities.
- ORCH lines 3022–3060 bind the configured/resolved spelling and work-directory inode in `WORK_DIR.json`; copying the directory fails even if its file bytes match. SF1 rechecks at each wave and ingest (3114 onward). SF2 refuses a populated or uninitialized tree; deleting/replacing that record is not a remedy. Cache entries re-read their pinned paths (2295 onward); the review did not open any such entry.
- WRAPPER lines 365–375 require `tail_readiness.certificate_ledger.path` to equal the configured work directory plus `CERTIFICATE_LEDGER.jsonl`. Moving that path requires changed config/policy review and ledger-genesis identity. The entire tail-readiness block feeds the wrapper's cache id (133–143), and ORCH C4-2 refuses committed plans from another cache id (3086–3104).
- A143 D1's proposal to lower the guard was **withdrawn by A147 L3-01**. The current guard is at least the 80 GiB per-call output cap, plus a 20 GiB reserve. ORCH 1742–1749 rejects a smaller guard and 2163–2182 reads free space only on the work directory's volume. Spreading subtrees or counting the new drive's free bytes while retaining the old work directory is not an admitted extension. STORAGE_PARENT also rejects moving those subtrees.

**Capacity (TESTED filesystem metadata; FORMAL arithmetic; UNTESTED output forecast).**

At EVIDENCE's `date -u`, **Wed Oct 21 11:43:22 UTC 2026**, `df -k` on only `/System/Volumes/Data` and `/Volumes/External1` returned **928.707 GiB** and **2877.480 GiB free**, respectively. No run tree was listed. Reserve **397,867,631,966 B = 370.543 GiB** for HEADLINE11 + S0×4, the corrected ERRATUM figure, rather than 48 GiB. This conservatively reserves the whole old forecast against current free space; some bytes could already be in `df` used space, which this read-only review cannot reconcile without prohibited run reads. Additional twin output, other NGC calls, certificates and an operating-system margin are a separate nonnegative reserve Y, not silently zero in a launch decision.

Use `need(k) = H + Y + calls_before(k) × b + next_calls(k) × 80 + 20` GiB on the campaign volume. **b is total retained call-directory bytes after acceptance**, including tail-state exports (A192 item 5), not merely receipt output. The old measured receipt figure **16.244605 GiB** is only a scenario until that complete total is measured. The old **57.19 GiB** high case is a scenario, not a bound.

Two different wave assumptions must be kept separate:

| Conditional internal-disk case, with H = 370.543 and Y = 0 | Need at b = 16.244605 GiB | Need at b = 57.19 GiB |
|---|---:|---:|
| W1 seed, 1 call | 470.54 GiB | 470.54 GiB |
| W2 nominal 3 plus, after seed | 646.79 GiB | 687.73 GiB |
| W3 nominal 3 minus, after 4 calls | 695.52 GiB | 859.30 GiB |
| All 7 at once, 7-cap admission | 950.54 GiB | 950.54 GiB |

The expected `[1,3,3]` prefix fits through W3 in both scenarios, with **233.19 GiB / 69.40 GiB** left in the inequality at W3 for Y. All seven together fail the conservative present internal budget by **21.84 GiB**, before Y. These are arithmetic cases matching 0817's context and the adjacent concurrent-Jacobian proposal, not proof of actual wave cardinalities or authority to implement 0816. The engine's invalid/halving/repair path can change requests. The precise stopping wave beyond this prefix is UNTESTED without its actual plan.

By contrast, STORAGE_PARENT's explicitly **ASSUMED** 120-call shape is `[1,8,2,1,1,1,10,10,24,8,2,1,10,10,24,7]`. Under that shape and the same H, the internal disk first fails at wave 2 (8-call guard). Do not report that historical shape's wave 2 as the three-plus wave. The reusable, shape-independent statement is that internal capacity remaining after H is about **558.16 GiB**, so an empty-campaign admission can reserve at most **6 calls** at once when Y = 0, with fewer as retained bytes accumulate. Internal storage cannot cover any 24-call wave's 1940 GiB guard even if campaign outputs took zero bytes.

**External1 from the start (FORMAL conditional alternative).** Keep HEADLINE11/S0 and other planned outputs on separately approved volumes; select the External1 work-dir identity and ledger path before W1's config/policy freeze. The existing campaign family already supports this volume; no scientific value changes merely by selecting its final work directory before initialization.

For the historical 120-call shape with H on internal storage and Y = 0 on External1:

- At b = 16.244605, External1 fits through wave 14 and first fails at wave 15. Requirement **R = 3385.77 GiB**; current deficit **508.29 GiB**. Free that much plus Y on External1 by root-authorized verified relocation of genuinely non-pinned other data, potentially to the arriving drive. Leave the campaign and its referenced evidence at their pinned identities. Whether enough such data exists is UNTESTED; no candidate inventory was opened.
- At b = 57.19, it first fails at wave 9, and the full shape needs about **7043.0 GiB**. Even clearing External1's entire roughly 3725.83 GiB capacity cannot suffice. A new-drive campaign would be required, with a fresh work directory/cache and newly bound policy; no existing approved mechanism preserves this campaign's initialized identity across that change.
- The old two-volume threshold **17.08 GiB/call** came from the old 953.0 + 2877.5 GiB free snapshot. Recomputed with the current metadata and the same H it is **16.80 GiB/call**, with only **49.87 GiB** spare at b = 16.244605, before Y. This threshold is not a measurement of b.
- If the new drive receives eligible noncampaign bytes and External1 were otherwise empty, its theoretical threshold is about **20.07 GiB/call**, also before Y. This is a capacity ceiling, not evidence that all existing External1 bytes may move.

**Smallest compliant decision before W1 (FORMAL).** Root can choose permanent External1 and document the current-volume budget, accepted-byte measurement/next-wave check, non-pinned offload capacity and the H/Y allocation before freezing the config and ledger policy. That can remove the drive-arrival wait only on the low-output path. If capacity cannot be secured, the no-custody-change choice is to wait for the final campaign volume. Starting internally as a throwaway pilot then replaying W1 would be a different authorization and loses the claimed identity-preserving time saving; it is not recommended as a silent workaround.


TESTED scope: 37 checks total across both lanes: byte pins, source AST parsing, inert work-directory identity and ledger guards, the actual P112 fill validator on synthetic metadata, and budget arithmetic. No production Context, driver, solver, comparator, campaign command, launch, run tree, step-2 output or NGC data was executed/opened. Files named as future runtime records describe required interfaces; they are not claimed existing evidence. No network, deletion, move, rename or existing-file write occurred.

Evidence: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/EVIDENCE_CX3V001.json` — SHA256 `a68f3987debaa227c3300059da728804cb9efa515ab1590289b55aaf899573cf`.
Full byte-pin register: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/SOURCE_PINS_CX3V001.json` — SHA256 `f3d907e2e1254ded9f24fe6415194b718f1385ade8e5f9b52c46d96706c80628`.
Selected historical V006 sections, preserved under the whole-source pin: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/V006_EXCERPTS_CX3V001.md` — SHA256 `c3a968369c77280cadeebd4f0517e018d9407b15bd61947cf91dd9850b1cd19f`.


Source register (SHA256 from bytes at the recorded read; source IDs above refer here):

- **DISPATCH**: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0817_2026-10-21_codex3_W1_before_drive_and_cw8_phase1.md` — SHA256 `d31288b8641d6cb1737ab8f2bf36429c349fa5a3e034280d9a0433080332078b`.
- **V006**: `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md` — SHA256 `1e70df1e53b74446ee33d002dd3bc0725519a1cd39f13b99a56b9c2d43c26531`.
- **STORAGE**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/storage_check_h3_c2v003.py` — SHA256 `8eee1f68ac7395c11be0046ccc11f1a24efbec1e4d62bc064111de099c8a01aa`.
- **STORAGE_PARENT**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/storage_check_h3_c2v001.py` — SHA256 `e0b3a89a4a2930311c393cd62d2f51b0b343fe705736d8083a45628c8a75706d`.
- **ERRATUM**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/STORAGE_PLAN_ERRATUM_C2V001.md` — SHA256 `5ce908d0e3eb732a4ea07d9a8a24ecf7557b0d62321f3003c202776505c6eb3c`.
- **ORCH**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` — SHA256 `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d`.
- **WRAPPER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py` — SHA256 `7c9b42483773a9e95fa8b3af9aaef972025fda2cfe071ada8d0092393fbda229`.
- **ENTRY**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/h3_campaign_path_c2/h3_campaign_entry_c2v004.py` — SHA256 `cbdf0d49b8bfa09bccf8ba1ebfb518f8c00b663c2564db7c3a02c8b7a86e116d`.
- **ENGINE**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py` — SHA256 `6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3`.
- **CHECKER**: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/accel_w1disk_cw8_cx3/check_accel_cx3v001.py` — SHA256 `2ef79fed5ed2f962f76ab74cbdeb2c55ffa6d7969639931ff4295e11c6018f62`.
