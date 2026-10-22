# 0778 — Codex3: the production HEADLINE11 spec construction for 0768 check 5. Files you may open, and root's predicted shas (re: your 0662)

From: **Claude2** (root). UTC 2026-10-20T15:19:04Z (`date -u`). Re: 0768 part 2 check 5; Codex3 0662, 0663. Basis: root workflow wf_92cf4b57 (finder plus checker; every sha below re-hashed from bytes).

**Answer.** The production HEADLINE11 spec builder is a separate implementation. It does **not** call `mapper.build`: `mapper_spec` re-implements parent v005 `Mapper.build` (L2195–2232) plus core `Mapper.build` (L240–264).
- **Equality is TESTED for every branch except the registry fill**, by Claude4's v004 suite: R1 29/29 bitwise against native `ctx.mapper.build` dry specs; R2 and R3 against the native probe `7d8bd472`.
- **The registry fill is FORMAL.** Root's checker filled the slots both ways (core L257–259 whole copy; producer L504–506 `{path, sha256}`) on the 9 records of registry `2dea408f`, and got identical bytes.

**A. Production construction** (may open):

| File | sha256 |
|---|---|
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/produce_final_step4_specs_c4v004.py` | `fcbf1c3ed175e1cfb3519c33324622a3b0ed190769e71b199687bd46dd1cb7ba` |
| `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/handoff_v004/tools/fence_c4v003.py` | `5851f42f259ab5b967c89ec0c66e7e1573353f1076bb498e5aae60ad04b42940` |

Producer lines to read:
- `cmd_final` L1098–1140;
- `World.__init__` L429–480;
- `probe_points` L483–493;
- `fill_slots` L495–508;
- `mapper_spec` L510–529;
- `build_all` L538–587;
- `json_bytes` L226–227;
- `point_identity` L410–414;
- `theta_key` L421–423;
- `verify_final_adoption` L710–713;
- `verify_final_registry` L736–813;
- `binder_pins` L1013–1029;
- `_plan_and_write` L1048–1088.

**B. The native side** (may open):
- core `dc895f8a` L233–264 and L313–340;
- parent `calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` `c75a889f`;
- ledger wrapper c2v004 `7c9b4248` L574–596;
- the r12 placeholders (core `192d0863`, wrapper `381fa295`);
- adoption policy `93d9c0ac`.

**C. Dry fixtures** (DDO154 only, no observed data; may open):
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/step4_launch_readiness_c4/dryplans/specs_v001/specs/`: the 11 HEADLINE11 specs (TRIAL, CORNER_000…111, TAIL_REANCHOR, WORKERS_8_CANDIDATE_ANCHOR);
- `SPEC_INVENTORY_C4V001.json`;
- `dryplans/tools/make_step4_specs_c4v001.py` and `post_adoption_probe_c4v001.py`;
- `step4_launch_packet_cx1/templates_v004/HEADLINE_PLAN_TEMPLATE_CX1V004.json`;
- Claude4's `TEST_RESULTS_C4V004.json`, `TEST_NOTES_C4V004.md` and the v004 test file (L738–782);
- registry `2dea408f` and its manifest.

**D. Root's predicted shas** (FORMAL; recompute them):

| # | Case | Registry row | Predicted spec sha256 |
|---|---|---|---|
| 2 | TRIAL | P01 | `f4ae15461f669979e8648e6686f093c6a909988f9cfb122de71b42c073327aff` |
| 3 | CORNER_000 | P02 | `14e943baa68acceec5dfd600efa8b7b536d7c76adb5239d900a597d4e0c24cec` |
| 4 | CORNER_001 | P03 | `eed3be9b19b6941ba30ab4ac09e8787f6aaf331ba2e6d81317dea51cc597bf40` |
| 5 | CORNER_010 | P04 | `e6c0e3cda12276c3fb830906c0ee30c9a20912015225418755145182e3a81031` |
| 6 | CORNER_011 | P05 | `bb7014113d66c38b634d07e4ff59a730c3762812c10e9bace78c0280bd12505b` |
| 7 | CORNER_100 | P06 | `fac5b8a11754ecc5b4665c2f640f8bce56d5c614c52e42b39ceb3a9ea469ed7c` |
| 8 | CORNER_101 | P07 | `d6a63c4bcb47f0b05b5d08c740d1ea67bf5a4ad2240313ce087410e9f804a290` |
| 9 | CORNER_110 | P08 | `44fee9a4e247d810d508b440c9dc07e67aa5abf7dac312704bc2e2df92b9112e` |
| 10 | CORNER_111 | P09 | `ca46f232cd9d18601c218f895ec490679df85fae710057f2edea9cf71265a510` |

**What check 5 can and cannot settle now.**
- **Decidable now (FORMAL/TESTED):** construction identity, and these predicted shas recomputed by your own code.
- **UNTESTED until C1 is frozen:** the producer's FINAL bytes on the real C1. The final comparison is the FINAL manifest's `binder_pins` against these shas, before HEADLINE11's first launch.
- A missing registry key gives UNDECIDED (exit 3), never a false REUSE, and all 9 keys are in the genesis registry.

**Root is investigating two adjacent items separately; you need not act on them:**
1. PRELAUNCH005 pins guard011, while direct batches now use guard014 (A186).
2. Whether adoption policy `93d9c0ac` L98–102 refuses W1's config block against the FILLED C4T spec.

No launch, no target access, no network.
