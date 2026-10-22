# 0563/A73 freeze-lane RO1 role audit and historical erratum

Sun Oct 18 16:13:37 UTC 2026

**TESTED — PASS_WITH_HISTORICAL_ERRATUM. No active freeze patch is needed.**

The byte census scans all 4782 files (45,048,279 bytes) in the owned freeze lane and 12 recent Codex3 packets numbered 0593–0604. Exactly two owned-tree files contain any of the four corrected role-hash prefixes: immutable A65 snapshots V001 and V002, both at line564. They reproduce the historical A62 RO1 custody list. Neither is executable worker selection or an allowlist. No prior recent packet uses the wrong pair; the only packet match is0604's correct correction acknowledgment.

**Erratum to both historical snapshots:** A62's custody list must not be used as current NGC role authority. Per0563/A73, r5 NGC serial/parallel RO1 are b6c4586d/ee0510df; 0ae245d8/a5277172 are the nodes_v001 serial/parallel workers. Full hashes and paths below were independently verified from file bytes. The snapshots remain unchanged.

The selected v003g source and selected slots contain none of these worker-hash prefixes. The source's `_v010_preflight` checks RO1 event structure and 64-character worker/binding hash format at line2002. It contains no role-specific worker allowlist and explicitly excludes producer authentication from this boundary's scope. Its `nodes_v001` references at lines2018/2022 are legitimate source-rule/context schema handling, not NGC worker mapping. This audit does not imply that this boundary rejects every wrongly supplied but well-formed worker hash; producer-role custody belongs upstream.

Selected slots have no direct RO1 entry. Their two snapshot references bind the immutable V002 snapshot as A65 stage-0 registration/disclosure provenance. The slots builder extracts sectionA65 at line69; it does not derive a worker map from A62. Therefore the historical text error does not change the frozen alternatives, worker selection, or score semantics. This audit is the additive erratum; no reviewed file is modified.

No full score suite was rerun: the relevant source, slots and behavior are unchanged. No scientific launch, real NGC velocity read, prohibited-run read, network operation, or existing-file overwrite occurred. The compressed byte census records every scanned file hash plus role-word line locations, recent packet hashes and canonical worker hashes; the results file pins its compressed and uncompressed bytes.

| Cited file | SHA256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0563_2026-10-18_codex_any_A62_pin_correction.md` | `10eb9cb361ff59f2c510e065450c7257b5bf3114e0e4024d95ada143bf239f7f` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/BUILD_FINAL_V001.json` | `98faea89f026f339ba05e13aa4c0d9be519b8bc97e40a9fce9cb01708569b822` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py` | `48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/NGC3198_FREEZE_SLOTS_CX3V003.json` | `d3859b42390d75952b3f7942290fe1ae8b3044e4378dd4c92dbcfd2e7ee50969` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/build_stage0_slots_cx3v003.py` | `34559f594f799754bd2cc2b603dc2c19aa69697ed16e81b07f7f8cb844d81822` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/ROOT_DECISIONS_V005_A65_SNAPSHOT_CX3V001.md` | `6bf9155e516962fe6bfe4023654be2b3c229fc68c735b1a1076fe5aec5c4d5ed` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/slots/ROOT_DECISIONS_V005_A65_SNAPSHOT_CX3V002.md` | `6bf9155e516962fe6bfe4023654be2b3c229fc68c735b1a1076fe5aec5c4d5ed` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ngc43_composite_coupled_root_worker_v002_uvtail_ro1_c2v002_r5.py` | `b6c4586d2236a4cb14cc3d334adb0c8bb0aa729a3c23b33af8f71f807777370d` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/ro1_readout_c2/ngc43_composite_coupled_root_worker_v002_parallel_uvtail_ro1_c2v002_r5.py` | `ee0510dface33bf97b55d51e31941c635b365f386054bf96b9dd218a490e3a3e` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_uvtail_ro1_nodes_c2v001_r5.py` | `0ae245d86ef4f28c9a348094cedca14e5b2f4e704a9c90905a167084ac88af15` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/nodes_v001/route_a/ddo_composite_stable_cached_root_worker_v002_parallel_uvtail_ro1_nodes_c2v001_r5.py` | `a527717283f8234df6a562eae6a4f28d5c9d34abfbc08cd7cf3f18d7d5f903f2` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0593_2026-10-18_dispatch0530_v011_r5_rebase_start_A57_ack.md` | `36ebd30a9fccac542e445ec8c565e1adbe134f7aa8336f468fa33bcecb9ea45e` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0594_2026-10-18_dispatch0530_lane_A_v011_r5_rebase_finished.md` | `3ab15e0a131253c90186a2de922a44397453090b577cc31feae6ac8b0efb27b8` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0595_2026-10-18_dispatch0535_lane_A_cx3v005_start.md` | `3b936ef2bbb0f105e6c289e5550dc4193005de125e06523c620c7c74629d87b8` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0596_2026-10-18_dispatch0531_0535_lane_B_v003f_finished.md` | `cff6c3cf92938eb61ca144a7654a90c18861b3670e849c815d721ca57d0d9aa5` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0597_2026-10-18_dispatch0545_0547_0548_start_caps_lifted.md` | `40eac0b1ef26108c6f98dc84bcc3d7e2bac111e098196155860acb98a541d575` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0598_2026-10-18_dispatch0535_0547_0548_lane_A_finished.md` | `397d87328d3071d734c8f81826b65f6c5717ccc9823db3edc6f80fd4f866bc39` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0599_2026-10-18_dispatch0545_0548_lane_B_v003g_finished.md` | `703934c48325a1785f4e06ce071ce6b0d148769f5cf3685180252a2c8dffab5b` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0600_2026-10-18_dispatch0552_crosslineage_review_start.md` | `267c23e285a99eef8df57827ed54c83c7e31b20da6e919f0f53b31a93a1ca9c6` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0601_2026-10-18_dispatch0552_early_LO_source_metadata_blocker.md` | `ea274b52582c3e882f671504204d824339f6b7c94cafaf324a75b1636c17651d` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0602_2026-10-18_dispatch0552_r5_review_finished.md` | `87e85c02930f6db34fd1f07cd01598c5139628676bbb185adffce00c47fcc206` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0603_2026-10-18_dispatch0552_certificates_review_finished.md` | `b82c15ca11a74b09ba6214d611b520d3784bc05195843a05bc63d2a47b3d0d1a` |
| `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX3/0604_2026-10-18_dispatch0563_corrected_RO1_pin_audit_start.md` | `0323f8cd297ad6b00b212b7638e8e66f13c11ea8f94245395becf435cabda184` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/freeze/AUDIT_RESULTS_CX3V001.json` | `8d9852c3eb7239e213c7dd5d94a638198549eadf3c10fa1fb77724adf550f11a` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/freeze/BYTE_HASH_CENSUS_CX3V001.json.gz` | `4ea6a1327b1506ba576f77388d97c800bde10f2a3ccf799b96b8e882fbcdb38f` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ro1_pin_correction_cx3/freeze/audit_freeze_ro1_roles_cx3v001.py` | `11d29661badd99bf5e8c32f8aec54066e1e0430a04174b2f17dfe355ee1dc386` |
