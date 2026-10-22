# 0034 — Claude3 DONE 0485 item 2: target-free NGC3198 freeze inputs

From **Claude3** (Claude Opus 5.5). UTC 2026-10-17T21:26:39Z. Output: `claude_artifacts/ngc_freeze_inputs_c3/` (read-only, hashes in `HASHES_NGC_FREEZE_INPUTS_C3V001.txt`, notes in `NOTES_NGC_FREEZE_INPUTS_C3V001.md`). No NGC3198 velocity, σ or velocity-derived value opened; no launches.

**(a) `NGC3198_FREEZE_SLOTS_C3V001.json`** (`0f6482c4240fd5553b61f184c08bf117a95ffa0912dd6b42bcc95645680710c7`):
- **`ngc3198_slots`**, for the orchestrator's `cfg['ngc3198_slots']`:
  - distance: reference and trial 13.8 Mpc, log, box 12.545–15.18, box_ends;
  - inclination: physical 72° as reference and trial, linear, box 69–75, box_ends.
- **Query block:** 43 rows in manifest order.
  - Under GL4, Q01 and Q02 are INVALID (QUERY_INSIDE_INNERMOST_NODE; innermost node 0.70517 kpc).
  - Under GL10, all rows are supported (0.30568 kpc).
  - All rows are inside N2 (66.90428799311597).
- **Pins:**
  - projection: route-B v006 config, physical 72° / released 73°, 13.8 Mpc, observation rule;
  - truncation: reducer 746980f2, edge, dropped fraction;
  - frozen decision files V001 / V002 / V003.
- **Alternatives:** the coordinate-spec declaration plus GL10_SOURCE_GAUSS_ORDER (approximation, NOT_EVALUATED_BEFORE_FREEZE). It validates under the freeze module's D9 rule.

**(b) BH-T1a** (`F_STAR_BH_T1A_PREREG_C3V001.json` `8e24ef7f5dcd4d876691255c938fe260e556f1717e90989f5cae07a97e65e2c9`, `fstar_c3v001.py`, `bh_t1a_analysis_c3v001.py`):
- **Definition:** f★ is built from the forward route's own star, HI+He and H2 profiles. PRIMARY is the enclosed share, SECONDARY the local share, and M/L 0.4 and 0.6 are carried as variants. Q43 gives f★_enc = 0.504, which matches A10's ≈ 0.51.
- **Analysis script:**
  - It refuses unless the pinned freeze module verifies the manifest and registration, and the manifest sha equals the registered expectation.
  - It reports Spearman ρ with a permutation p, and the OLS slope with its SE and a bootstrap 95 % interval.
  - It covers the reference member, plus min/median/max over members.

**(c)** SA-BH-01 and SA-REACH-01 are taken verbatim, by regex, from the frozen V003 bytes, each with its pre-declared miss reading. They go under `notes.structural_assumptions`, and the block has no forbidden field.

**Tests 15/15 PASS (synthetic):**
- The freeze module accepts the slots.
- `engine_coordinates` are byte-identical to the placeholders and to the spec record, which is the orchestrator's check.
- A wrong distance reference is refused.
- The alternatives and notes blocks are valid, and the query order matches.
- The f★ mass identities hold.
- On the freeze module's synthetic root-call-order run, the analysis recovers a planted slope of +2.000 and refuses tampering.

**Needs root:**
1. **Ratify the declared slot boxes.** The program has no NGC3198 distance or inclination uncertainty. The boxes affect only the box-limited sensitivity band.
2. **Confirm forward_ngc can evaluate D ≠ 13.8 and i ≠ 72 for the sensitivity band.** PC-5 says inclination is not exposed, and the A13 stage bindings refuse non-registered DDO geometry. If not, decide before step 5.
3. **ORIGINAL_K** stays EVALUATED_BEFORE_FREEZE, as declared.

Checking FROM_CODEX every minute.
