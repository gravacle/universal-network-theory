# H3 campaign launch path, c2v001 (V006 A188): built now, finalized at the verdict

Claude2 for root. Stamp (`date -u` before writing): Tue Oct 20 01:37:48 UTC 2026 (Mon 20:37 CDT).
Nothing real was launched. The only runs used the SYNTHETIC mock driver under the real root monitor and campaign c2v005, inside `test_runs/` and `dev_runs/`. No step-2 tree was opened, no NGC3198 file was opened, and from V006 (`7dcc4b17`) only A126, A129, A131, A134, A137, A139, A140, A143, A147, A158, A166, A172, A177, A187 and A188 were read. Labels: TESTED (ran), FORMAL (from code), UNTESTED (forecast or not run).

Shorthand:
```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts;  H3=$ART/h3_campaign_path_c2;  CX2=$ART/calib_tail_readiness_cx2
C2D="/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2"
W1S="$C2D/W1_RUN_SHEET";  RX="$C2D/runs_ext";  S45=$ART/sched_s45_c2;  O=$ART/calibration_orchestrator_c2/v005
R="$C2D/H3_AT_VERDICT"      # root's folder for the records it fills at the verdict (root creates it)
```

## 1. What was built

| piece | file | what it is |
|---|---|---|
| generator | `make_campaign_cascade_c2v001.py` | minimal successor of Claude4's `make_b1_cascade_c4v002` (`a7a5fe58`). The policy and core rules are v002's, byte for byte. Only the wrapper source changes, to the q5b1 wrapper `7a6af535` (MAP F1). It adds a 4th output, the entry, and a `--publish-root`. |
| entry | `h3_campaign_entry_c2v001.py` | successor of `w1_campaign_entry_v001` (`6a6957f2`). `plan`, `status`, `run` and `resolve` are the parent's `main(argv)`, unchanged. New: `reingest --wave W --call-index I --bundle B --bundle-sha256 H`, which calls the wrapper's own reingest (q5b1 L335-358) after these guards: all gates pass; the wave plan has this config sha and gate digest; the bundle verifies from bytes. |
| regenerate | `regenerate_h3_c2v001.py` | `fill`: writes the one seal tuple record from bytes. `build`: refuses unless the tuple equals the report bytes and the sealed bytes, then writes the re-pinned chain and checks it from bytes. |
| apply | `apply_h3_fields_c2v001.py` | successor of apply v002 (`2a18b280`). Its ALLOWED_SET holds only the gate fields (section 4). With `--seal-record`, `numerics.{verdict_artifact, compare, sealed_prereg}` are derived from the seal record. |
| derivation | `build_adoption_derivation_c2v001.py` | the C4-6 adoption derivation and `measured_per_call_bytes`, read from a candidate config's bytes and root's source receipts. |
| acceptance step | `h3_accept_call_c2v001.py` | per finished call: acceptance_q2 v004 (`5ff464cc`, A158), then the entry's reingest. |
| storage | `storage_check_h3_c2v001.py` | `wave`: the parent's per-wave disk rule, with the campaign's own measured outputs. `move`: whether a directory may leave by a verified move. Read-only. |
| records | `SEAL_TUPLE_RECORD_H3_C2V001_PLACEHOLDER.json`, `H3_FIELDS_RECORD_C2V001_TEMPLATE.json`, `ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json` | the seal placeholder (empty tuple); the H3 fields with their values of record and citations; the acceptance deps from C1. |
| placeholder chain | `placeholder_chain/v006r12_c4/` | the generator's output with no tuple, for review only. **Do not publish it.** Policy = `93d9c0ac` (identical to r10_c4), core `192d0863`, wrapper `7ac07851`, entry `48fd45ef`. |
| tests | `tests/test_h3_campaign_path_c2v001.py` + `tests/synthetic/` | 84 rows: 41 MUST_PASS, 43 MUST_FAIL (section 8). |

**SUB = `v006r12_c4`.** A129 reserves `v006r11_c4` for the direct batches' policy-only finalization. The policy bytes do not depend on SUB, so at the verdict the two policy files will be byte-identical.

**Diffs** (all `DIFF_*.diff`):
- **Wrapper:** the placeholder wrapper differs from q5b1 at L27 only.
- **Core:** it differs from core r10_c4 at L200 only (the SUB path), and from core r9 at L200 and L202.
- **Entry:** it differs from its template in the 2 WRAPPER lines.
- **Generator:** against v002, the changes are W1, E1 and M1 in its header.

## 2. Findings (MAP F1-F6), now tested

- **F1. The campaign wrapper comes from the q5b1 line, not R9. TESTED.**
  - Synthetic test EB10: a Q5-form post-state bundle (`parent_prelaunch_bundle` plus per-state LO) is accepted end to end by q5b1's L148-191 check and the real b1 guard.
  - The R9 wrapper's LO_ENVELOPE rule would refuse it (FORMAL).
- **F2. The re-pinned chain needs only the tuple. TESTED.**
  - G01: with SUB `v006r10_c4` and no tuple, the generator reproduces the published `93d9c0ac`, `dc895f8a` and `7a6af535` and the entry template, byte for byte.
  - R09: with a tuple, each file differs from the no-tuple build in exactly policy 2 lines, core 1, wrapper 1 and entry 1.
- **F3. Erratum to run sheet §0 item 1 bullet 3 and §7 B2. TESTED (synthetic).**
  - Core r9's "adoption fails whatever the config says" (L300-311) is never reached. The wrapper's `check_adoption` calls the parent's L1828-1926 directly.
  - EB01: the adoption gate passes on core `192d0863`, which is r9's text plus C1/C2. No core logic change is needed.
- **F4. Erratum to run sheet §4 item 1: the cache id is not `878d612a`. TESTED.**
  - On real v004a, R9 gives `878d612a46e57f19` (K02B) and the placeholder chain gives `e750632dd937e89e` (K02). The parent cache id is the same in both, `1ce0ef418d918e7f`.
  - The wrapper key (q5b1 L52-55) changes again with the regenerated wrapper bytes and with the H3 `tail_readiness` fields (EB01B: parent id unchanged, wrapper id changed).
  - The W1 cache id is therefore known only from the final W1 config. The work dir has never been created, so C4-2 is not touched. The W1 record states the new id.
- **F5. BLOCKING for wave 2 and later, not for W1. TESTED (synthetic).**
  - Every planned point needs a registry record, because the wrapper's `prelaunch_check` (q5b1 L202-211) runs for every call.
  - The registry pin is in the config. The config is frozen from W1 to march0 (A137 N-C), the pin enters the cache key, and a work dir holds one cache id (C4-2).
  - EA15: with only W1's 10 points registered, after acceptance the wave-2 plan refuses `CERTIFICATE_PREFLIGHT ... CERTIFICATE_POINT_MISSING_OR_MISMATCHED`.
  - EB15/EB16: when wave 2's points (3 jacobian points in the synthetic world) were registered before W1, the wave plans and runs.
  - Root rules this (open item 1).
- **F6. Readings other than ACCEPTED have no ruling. FORMAL.**
  - The acceptance step then stops with exit 13 (`NOT_ACCEPTED`) and reingests nothing (EB09). The call stays INFRA.
  - `resolve retry` reruns the same spec deterministically, and `invalid` is disabled (EB14).

## 3. Root steps at the verdict (exact commands)

**Now, before the verdict.**
- Reviews: Codex1 reviews `DIFF_make_b1_cascade_c4v002__make_campaign_cascade_c2v001.diff` (A129 ownership). Claude4 reviews the entry, acceptance step, apply tool, derivation builder, storage tool and test suite (A188).
- Wall: when C4T's receipt is in, run run sheet §2 unchanged. The result is `CFG_W=$S45/v005/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V005A.json`, which carries only the wall, the orphan wait and the notes against v004a.

**V1. Fill the one record.** Run this after the sealed V007 report exists and reads ADOPT_TAIL.
```
mkdir "$R"
cd /tmp && $PY -I -B $H3/regenerate_h3_c2v001.py fill --report "<sealed V007 report path>" \
    --filled-by "root (Claude2)" --ruling "<V007 / V006 entry of the verdict>" --out "$R/SEAL_TUPLE_RECORD_H3_FILLED.json"
SEAL_SHA=$(shasum -a 256 "$R/SEAL_TUPLE_RECORD_H3_FILLED.json" | cut -c1-64)
```
- `fill` reads C, P, A and SCHEMA from the sealed compare, the way the generator reads them, and V from the report bytes.
- It refuses before writing unless the report's schema, `script_sha256`, `prereg.sha256` and `pins_verified.V005_addendum` equal the tuple and the report reads the sealed ADOPT_TAIL (R11-R13).
- Expected prefixes (from the MAP; not re-opened here): C `a99105a1`, P `b2989012`, A `c01b3c51`, SCHEMA `UNT_KMAX_TAIL_COMPARISON_C2V007_R11`.

**V2. Regenerate, review, publish.**
```
mkdir "$R/chain"
cd /tmp && $PY -I -B $H3/regenerate_h3_c2v001.py build --seal-record "$R/SEAL_TUPLE_RECORD_H3_FILLED.json" \
    --seal-record-sha256 $SEAL_SHA --out-dir "$R/chain"
for f in adoption_policy_cx2v006r12_c4.py calibration_core_cx2v006r12_c4.py calibration_orchestrator_cx2v006r12_c4_q5b1.py \
         h3_campaign_entry_cx2v006r12_c4.py; do diff -u "$H3/placeholder_chain/v006r12_c4/$f" "$R/chain/v006r12_c4/$f"; done
mkdir "$CX2/v006r12_c4"
for f in adoption_policy_cx2v006r12_c4.py calibration_core_cx2v006r12_c4.py calibration_orchestrator_cx2v006r12_c4_q5b1.py; do
  cp -n "$R/chain/v006r12_c4/$f" "$CX2/v006r12_c4/"; done
shasum -a 256 "$CX2/v006r12_c4/"*.py      # must equal "outputs" in $R/chain/REGENERATE_RECORD_v006r12_c4.json
ENTRY="$R/chain/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py";  ENTRY_SHA=$(shasum -a 256 "$ENTRY" | cut -c1-64)
```
- The four diffs against the placeholder are the A126 small diffs: policy P5/P6 (2 lines), core L202, wrapper L27 and entry WRAPPER_SHA. The reviewers check those.
- The publish path must be exactly `$CX2/v006r12_c4`: the entry pins it, the core loads the policy relative to it, and the wrapper loads the `v006r8` sibling.
- The entry stays in `$R/chain`.

**V3. H3 fields, then a candidate config.** These inputs come from other lanes and must exist first:
- the certificate registry: the EPS/ρ producers, A134 Q5/Q8. It covers the 9 probe points and the seed, plus every later point (F5);
- the signed policy review;
- the C1 producer list;
- the deciding evidence: two fresh r5 runs, `reanchor` and `workers_8`;
- the capability evidence: 9 probe runs at the post-registry spec shas.

Root writes `$R/H3_DELTA_CANDIDATE.json` as `{"set": {...}, "append": {"notes": " | H3 (V006 A188) ..."}}`. Its `set` holds every field in section 4 except `adoption_derivation`, `disk_guard.measured_per_call_bytes` and the three seal-derived numerics pins.
```
cd /tmp && $PY -I -B $H3/apply_h3_fields_c2v001.py "$CFG_W" "$R/H3_DELTA_CANDIDATE.json" "$R/RUN_CONFIG_H3_CANDIDATE.json" \
    "$R/APPLY_REPORT_CANDIDATE.json" --seal-record "$R/SEAL_TUPLE_RECORD_H3_FILLED.json" --seal-record-sha256 $SEAL_SHA
```

**V4. Adoption derivation, then the W1 config.** The wall record is the FINAL wall rule record from run sheet §2. The `--source-receipt` list gives the C4T case and any `numerics.source_results` case on C4T's grid.
```
CAND="$R/RUN_CONFIG_H3_CANDIDATE.json"
cd /tmp && $PY -I -B $H3/build_adoption_derivation_c2v001.py --entry "$ENTRY" --entry-sha256 $ENTRY_SHA \
    --config "$CAND" --config-sha256 $(shasum -a 256 "$CAND" | cut -c1-64) \
    --wall-rule-record "$W1S/W1_WALL_RULE_FINAL_<UTC>.json" --wall-rule-record-sha256 <sha> \
    --source-receipt C4T "<C4T top-level receipt path>" <sha> [--source-receipt <CASE> <path> <sha> ...] --out-dir "$R/ADOPTION"
cd /tmp && $PY -I -B $H3/apply_h3_fields_c2v001.py "$CAND" "$R/ADOPTION/ADOPTION_DELTA_H3.json" "$R/RUN_CONFIG_W1_H3.json" \
    "$R/APPLY_REPORT_W1.json"
CFG="$R/RUN_CONFIG_W1_H3.json"
cd /tmp && $PY -I -B "$ENTRY" plan --config "$CFG"      # gates_ok true; next wave 1 call, key 968c915bece706ea
cd /tmp && $PY -I -B "$ENTRY" status --config "$CFG"    # read-only, no lock
```
- The builder refuses unless the numerics, deciding, capability and certificate gates already pass.
- It writes `TIMING_MODEL_H3.json`, `ADOPTION_DERIVATION_H3.json` and `ADOPTION_DELTA_H3.json`. The delta sets `adoption_derivation` and the same `measured_per_call_bytes` in one step (parent L1919-1922).

**V5. W1 record and launch.** Use run sheet §4 and §5 unchanged, with two substitutions: `$ENTRY` replaces `$W1S/w1_campaign_entry_v001.py`, and `$CFG` is the config.
- The W1 record also carries: the seal record sha, the REGENERATE_RECORD sha, both apply reports, the new cache id (`status` prints it), and the leaf diff of `$CFG` against v004a. That diff may contain only the wall, the orphan wait, the notes and the section 4 paths.
- After the verdict S4T has finished, so the line carries no `nice` (A187).

**V6. Accept each finished call.** By design, W1 returns `HALTED_INFRA` (exit 4) with one item `CERTIFICATE_ACCEPTANCE_REFUSED: ... TAIL_CERTIFICATE_ACCEPTANCE.json` (TESTED, EB04). Then:
```
cd /tmp && $PY -I -B "$ENTRY" status --config "$CFG"                       # halts: wave, call items, tokens
DEPS="$R/ACCEPT_DEPS_RECORD_H3_FILLED.json"    # root fills from ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json + C1
cd /tmp && $PY -I -B $H3/h3_accept_call_c2v001.py --entry "$ENTRY" --entry-sha256 $ENTRY_SHA --config "$CFG" \
    --wave 1 --call-index 0 --deps "$DEPS" --deps-sha256 $(shasum -a 256 "$DEPS" | cut -c1-64) \
    --records-dir "$ART/campaign_acceptance_records_c2/W0001_C0000_A01"
cd /tmp && $PY -I -B "$ENTRY" status --config "$CFG"                       # n_cached 1
```
- **Exit codes:** 0 = ACCEPTED (or ACCEPTED_PASS_FLAGGED) and reingested VALID; 13 = NOT_ACCEPTED, nothing reingested, root rules (F6); 3 = refused, nothing written; 8 = a run holds the lock.
- **Records:** the records dir must be new and under `claude_artifacts`, the handoff's Store rule. It receives the acceptance record, the POST_STATE_BUNDLE and `ACCEPT_STEP_RECORD_W0001_C0000.json`.
- **Writes into the call dir:** the handoff writes its replay inputs and `ACCEPTANCE_TAILSTATES_*` there, as for every direct call. `reingest` writes `TAIL_CERTIFICATE_ACCEPTANCE.json` under the orchestrator lock.
- **For a wave of n calls:** run the step once per halt item whose reason starts with `CERTIFICATE_ACCEPTANCE_REFUSED`, using that item's `call_index`.
- **Next wave:** relaunch the run sheet §5 line without `--new-campaign`, with a new TAG and with or without `--max-waves`. No `resolve` is needed: the accepted keys are cached, so the probe moves on (TESTED, EB16).
- **First:** run the disk check (section 6). F5 decides whether that wave can plan.

## 4. H3 config fields: what each gate needs, values of record

The fields come from the parent/core/wrapper bytes. Every path already exists in v004a as null or `[]`. The template `H3_FIELDS_RECORD_C2V001_TEMPLATE.json` carries the same table.

| gate | config field | value of record | citation |
|---|---|---|---|
| numerics | `numerics.verdict_artifact` | the sealed report `{path, V}` (derived from the seal record) | A126, A129, A188; policy L46-57 |
| numerics | `numerics.compare` | the sealed compare `{path, C}` (derived) | A126; generator SEALED_COMPARE |
| numerics | `numerics.sealed_prereg` | the report's own `prereg` object (derived; compared exactly, policy L63) | policy L59-64 |
| numerics | `numerics.block_source` | C4T call spec; its numerics must equal `numerics.block`, and `admit` must be `{}` | A187 ("adopts the C4T tail"); policy L98, L102-105 |
| numerics | `numerics.adopted_result` | C4T `result.json`; its sha must equal `report.inputs.C4T.result_sha256` | policy L95-101 |
| numerics | `numerics.source_results` | `[]`, or other cases on C4T's grid | policy L121-132 |
| numerics | `numerics.block` | **unchanged** (the tool refuses it) | A137 N-C |
| deciding | `deciding_test` | evidence document: runs `reanchor` + `workers_8`, r5, workers 8 | core L114-197. MEASURED; no permitted section commissions the runs |
| deciding | `anchor.{result, receipt, spec_sha256}` | the reanchor row's pins; `anchor.use` stays false | core L101-102, L152-157 |
| capability | `capability_evidence` | rows for the 9 probe spec shas taken after the registry | core L313-340. MEASURED |
| certificate | `tail_readiness.certificate_registry` | per-point `{identity, bundle, eps_certificate, lo_certificate}` | A134 Q5, Q8; q5b1 L86-90. COMPUTED |
| certificate | `tail_readiness.certificate_policy_review` | schema `DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001`, binding the driver, deriver, enumerator, the exact producer list, guard `9e3fc109`, the q5b1 slot rule and handoff | q5b1 L59-77. Signed by the reviewer |
| certificate | `tail_readiness.approved_certificate_producers` | C1's list, including slot proof `cd10cd59` | A139, A158 |
| certificate | `tail_readiness.state_enumerator` | **b1 enumerator** `s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py` `4ca7f364…` (FIXED; v004a has `e48cca3c`) | A139 ("name the b1 enumerator (A138)"); acceptance v004 L29-30 |
| certificate | `tail_readiness.custody_deriver` | unchanged: custody_cx2v002 `6810b7c3` | no permitted ruling changes it |
| adoption | `adoption_derivation` | COMPUTED by `build_adoption_derivation_c2v001` | parent L1828-1926; q5b1 L213-227 |
| adoption | `disk_guard.measured_per_call_bytes` | the largest output over the derivation's source receipts. The run sheet's 17,442,511,906 holds only if C4T_C5c is a source case on C4T's grid (UNTESTED) | parent L1905-1908, L1919-1922 |
| adoption | caps (already set as scheduling leaves) | wall = FINAL wall rule (provisional 133,200 s); RSS = RAM 137,438,953,472; output 80 GiB; guard = cap; reserve 20 GiB; orphan wait = wall + 600 s. The derivation's `per_call` must equal these, and each must be above the measured values | A140 N4/N5, A177, A166, A147 L3-01, A143, A172 |
| u_i | `u_i_carrier.{carrier, declared_by, basis}` | `NOT_CARRIED_DECLARED` (v004a default) or `FROZEN_BANDS_ONLY`; root signs `declared_by` and `basis`. A140 "V2 is decided at H3" is not explained in the permitted sections | parent L1797-1826 |

- **Cache id:** none of these paths enters the parent key (L1774-1780). `tail_readiness` enters the wrapper key, together with the wrapper and guard bytes (q5b1 L52-55). So the wrapper cache id changes (EB01B, A10).
- **Apply v002 cannot set any of these fields** (A09).

## 5. The per-call acceptance step

Section 3 V6 gives the commands. The step does the following, in order:
1. It reads the gates, the wave plan (config sha, gate digest, cache id) and the planned spec.
2. It checks that the call FINISHED: the receipt verifies, status FINISHED/COMPLETED, the result is bound and finish.json is bound (`CALL_NOT_FINISHED` otherwise). It checks that the call is not cached already (`ALREADY_ACCEPTED`).
3. It checks the deps record: the enumerator equals the config's `state_enumerator` (A139); the guard is the wrapper's own `9e3fc109`; the approved producers equal the config list exactly (`DEPS_DIFFER_FROM_CONFIG` otherwise).
4. It sets `prelaunch_bundle` to the registered point's bundle and `receipt` to the call's own receipt.
5. Under the work-dir lock, it runs acceptance_q2 v004's `accept_call(mode='guard')`.
6. If the reading is ACCEPTED or ACCEPTED_PASS_FLAGGED (with `outputs_are_evidence`, guard ok, a bundle, and no anchor stop), it runs the entry's `reingest`. That call writes `TAIL_CERTIFICATE_ACCEPTANCE.json`, re-verifies, classifies and caches.

It never writes a proof, never chooses a producer, and changes no reading.

## 6. Storage plan (for root to rule before wave 9; nothing was moved)

**Facts**, from run sheet §3 and A147 unless marked:
- External1: 3,726 GiB in all, 2,877.5 GiB free, 848 GiB of other data.
- Internal disk: 953 GiB free (`df`, 01:37Z today).
- Campaign: 120 calls (the ENGINE_SHAPED list). The parent admits a wave of n calls only if free ≥ n × 80 GiB + 20 GiB.
- At the measured 16.24 GiB per call, wave 15 (24 calls) is short by 508.3 GiB with the campaign alone, and by 878.8 GiB with HEADLINE11 and S0 ×4 on External1 (forecasts, UNTESTED).
- In general, the amount to move before wave 15 is M ≥ 1,940 − 2,877.5 + 89·b + O GiB, where b is the per-call output and O is the other output on External1.

**Constraints:**
- The campaign work dir can never move: the cache re-hashes by path (L2302-2341) and SF1 pins its identity.
- Nothing pinned by the W1 config, the seal record, the V007 report, prereg or case block, the registry or its bundles and proofs may move. `storage_check move` refuses such a directory (S03, S04).
- Verified moves only (A147): `ditto SRC DST`; then a sha256 manifest of both trees, compared equal; then the source is removed. Never a plain `mv` across volumes.

**Plan:**
1. **HEADLINE11, S0 and NGC outputs go to the internal disk** (about 48 GiB for HEADLINE11 + S0 ×4, ASSUMED in the run sheet).
   - Even with all 848 GiB of other data moved, keeping them on External1 leaves wave 15 short by about 31 GiB (878.8 − 848).
   - This amends A140 N3 ("NGC outputs go to External1"), so it needs a root ruling.
2. **Move at least 600 GiB of non-pinned other data from External1 to the internal disk by verified move**, after W1's re-forecast and before wave 9. This is 508.3 GiB plus margin; recompute M with the measured b.
   - Candidates: root lists `du -sk /Volumes/External1/*` (not listed here) and checks each with `$PY -I -B $H3/storage_check_h3_c2v001.py move --candidate DIR --work-dir "$RX/DDO154_CALIBRATION_ORCH_CX2V006R9_P128_MS128" --pins-from "$CFG" --pins-from "$R/SEAL_TUPLE_RECORD_H3_FILLED.json" --follow`. Exit 0 means MOVABLE.
   - The internal disk keeps about 300 GiB after steps 1 and 2.
3. **Before every relaunch**, run `$PY -I -B $H3/storage_check_h3_c2v001.py wave --work-dir "$RX/DDO154_CALIBRATION_ORCH_CX2V006R9_P128_MS128" --next-calls N --out "$R/STORAGE_WAVE_<W>.json"`.
   - It uses the campaign's own receipts (largest final or peak output) and the parent rule. Exit 5 means the wave would halt HALTED_DISK: move data first, then relaunch without `--new-campaign`.
4. **Decision rule at W1.** The volume choice becomes irreversible at W1, because the work dir cannot move.
   - If W1's measured output projects 120 × b above External1's capacity minus its non-movable data, the campaign does not fit on External1 at any amount moved. At the 32-iteration projection of 57 GiB per call, the total is 6,840 GiB against 3,726 GiB.
   - In that case, stop before wave 2 and re-plan the volume. A new work dir means a new cache, so W1 reruns.
   - The deciding measurement is W1's `final_output_bytes` (UNTESTED).

## 7. Open items for root

1. **F5 (blocks wave 2 onward; W1 is not affected).** The registry must hold every planned point before that point plans, yet the frozen config pins it in the cache key.
   - Fact: the predicted points can run. In the synthetic world, wave 2's 3 jacobian points were pre-registered and the wave planned and ran.
   - Two ways forward:
     - pre-register before W1 every point up to march0. Whether the real jacobian points are independent of the seed's forward values is UNTESTED; the deciding test is a dry probe with a placeholder seed forward, compared with the actual seed.
     - a reviewed wrapper successor whose cache key does not carry the registry pin, with an append-only registry. Each cache entry already binds its own bundle and handoff and re-verifies them on open (q5b1 L259-272), so this would not weaken entry custody. It is a code change, reviewed under A137 N-C.
2. **F6.** A ruling is needed for a campaign call that reads INCOMPLETE, LO_UNCERTIFIED_TRANSIENT, NON_LAPSE_TAIL_MATERIAL, BOUND_INSUFFICIENT or UNDECIDABLE_FLAGGED. The step stops with exit 13.
3. **The measured H3 inputs exist in no lane yet.** These are the deciding runs (reanchor, workers_8) and the 9 capability runs, all real r5 calls. They need certificate slots, and so the registry, first.
4. **C1 contents for the deps record:** the producer list, `lo_core`, the SRB-ROT adapter, the row-policy and packet reviews, and `root_ruling_refs`. They were not in the permitted reads, so the template leaves them null.
5. **Not tested on a real campaign call dir.** The real writer (`808cfe6a`) writes into the campaign call dir. The synthetic run showed that cache re-verification ignores the `ACCEPTANCE_TAILSTATES_*` dirs (EB11, EB16), but the real writer's files are UNTESTED there.
6. **Errata to the run sheet:** §0 item 1 bullet 3 and §7 B2 (F3); §4 item 1, the cache id (F4); the §5 launch line now uses `$ENTRY`.
7. **The storage rulings of section 6:** A140 N3, the amount and destination, and the W1 decision rule.

## 8. Tests

Two record runs from this folder, each 84/84: 41 MUST_PASS, 43 MUST_FAIL, 0 audit denials in the test process and in the 26 child processes. The test process started only the pinned python, 50 times (monitors and children). The children's audit allows only the pinned python and `ps`. The rows are identical, by id, expectation and pass, across the two runs.
- `test_runs/RUN_20261020T013507Z_33648`: TEST_RESULTS `29a96d62ab92f9833df95918b12a585a09c4858fed5f8f3d5358e8d4a6fdda16`.
- `test_runs/RUN_20261020T013535Z_36257`: TEST_RESULTS `f5140ccfdb17ff48be908b1dbf59d879d0df0c9e719194ad668c16a53416d4c8`.
- The stdouts are `test_runs/TEST_STDOUT_RUN1.txt` and `_RUN2.txt`. The lines are identical apart from the run-dir paths and the hashes that depend on them.

**Row groups:**
- **G01-G07, generator:** the regression above; the shipped placeholder; same policy and core as v002; the diff-line positions; refusals.
- **R01-R14, regenerate:**
  - MUST_FAIL: the placeholder record (**empty tuple**); an empty field; **V not the report bytes**; SCHEMA not the report's; P not the report's; a non-ADOPT_TAIL report; a compare that is not the sealed one; the generator's own sealed-bytes cross-check; a second write; `fill` on bad reports; the CLI on the placeholder.
  - MUST_PASS: the written chain and `fill`.
- **A01-A11, apply tool:** only H3 fields and notes change (46 leaves); MUST_FAIL on null template values, numerics.block, scheduling, the driver, a bad pin, ADMISSION_RECTANGLES, a seal mismatch, and apply v002 itself; deterministic bytes; the CLI.
- **K01-K14, real chain, dry** (real r5 normalize in process; the work dir is local and never created):
  - W1 plans 1 call, key `968c915bece706ea`, spec `3958aed3…`, with the six gates pending;
  - the cache ids;
  - through the entry: `run` refuses GATES_NOT_PASSED (exit 3), `resolve invalid` and `resolve retry` refuse, `reingest` refuses, `status` and `plan` exit 0;
  - the acceptance, builder and regenerate CLIs refuse;
  - ported suites: the R9 static-dry (26 normalizations; exact-distance gate) and v004a K03/K04/K06.
- **EA/EB/EC, end to end, synthetic, through the generated entry** (`run` in its own session):
  - gates: all six pass with the synthetic tuple; the placeholder chain refuses;
  - W1: one mock call FINISHED, then HALTED_INFRA awaiting acceptance; acceptance ACCEPTED; reingest VALID; status n_cached 1; wave 2 plans and runs (EB15/EB16);
  - MUST_FAIL: **missing bundle** (EB06); **wrong producer**, at reingest (EB07) and at the acceptance step (EB09, reads INCOMPLETE, exit 13); deps that differ from the config (EB08); accepting twice; resolve on a cached key; resolve invalid; **acceptance and reingest of a non-finished call** (EC02, EC03);
  - `resolve retry` through the entry, with the relaunch consuming its token (EC04);
  - the F5 contrast (EA15).
- **S01-S05, storage tool. Z01-Z02, A01-A02:** every named input unchanged; nothing published under `calib_tail_readiness_cx2`; the audits.

**Declared synthetic substitutions (TOY_SEPARATION):**
- After the generated wrapper and core are loaded and sha-checked, three module globals are set: core `DRIVER_SHA` and wrapper `DRIVER_SHA` to the mock driver's sha, and core `BASE` to the world's `SYNTHETIC_BASE`, so that core L134's normalizer path names the mock copy.
- The handoff's `LO_ADAPTER` is set to the synthetic module.
- The test config is v004a with the work dir, driver, taxonomy (a copy whose driver field is the mock's) and `anchor.driver_sha256` replaced. Every H3 field is then set by `apply_h3_fields_c2v001` itself.
- The sealed V007 world, the certificates, the deciding and capability evidence, and the C1 dependencies are synthetic (`tests/synthetic/syn_h3_c2v001.py`).
- The real b1 guard, wrapper, core, parent, campaign, monitor, policy and acceptance handoff v004 run unchanged.

**Not ported, because they are outside the permitted reads:** the wrapper_q5 suite, generator v002's own tests and the parent v005 suite. The R9 static-dry `cmd_dry_run` (r5's dry-run planner) was not run.

**Process note:** `dev_runs/` holds 5 development runs (71/75, 75, 79, 83 and 84/84). In the first, row S05's `--follow` traversal tried to open 5 pinned files under `CLAUDE2/runs/` and `/Volumes/External1/.../runs/`. These are old A2 DDO154 anchor runs pinned by `DDO154_COORDINATES_CX2V006.json`; none is step-2 and none is NGC3198. The test audit refused all 5 opens, so no byte was read. The storage tool now never follows pins into run trees, volumes, NGC3198, C5H, UVT_ or .codex paths; it checks them by path only.

## 9. Files

`HASHES_H3_CAMPAIGN_PATH_C2V001.txt` lists every file in this folder except itself (sha256 from bytes). Main objects:

| file | sha256 |
|---|---|
| make_campaign_cascade_c2v001.py | 65a701449bd72d654ec3ad59b01e30d3c89c8025988c9d0ce435c25ca1fa5358 |
| h3_campaign_entry_c2v001.py | 08068e93904fa12bd7d6bb9ceaca6b37b85cc884fa8091d8a7d59900e5a0c4bd |
| regenerate_h3_c2v001.py | 1706da776372191f619d02937b4388025b113fcb023b7da83a4300e410e3cc8f |
| apply_h3_fields_c2v001.py | 2e4a5393b5a1624b61c91424eaa90a61ce16cf2ef17dec60118158486e97877f |
| h3_accept_call_c2v001.py | 05651663cfa2e9159068c9f7aa939a0cefc749b6acc79d4a677cf87f7c2af2ba |
| build_adoption_derivation_c2v001.py | 01a4cbae729a0c44df2ea1f4cc500ae95669cb9ff6a7541bc94621c23c2294bd |
| storage_check_h3_c2v001.py | e0b3a89a4a2930311c393cd62d2f51b0b343fe705736d8083a45628c8a75706d |
| SEAL_TUPLE_RECORD_H3_C2V001_PLACEHOLDER.json | d43419be3cfe61684b68643e2edd1b199740c478a606f946d7bd5bf8d114cadf |
| H3_FIELDS_RECORD_C2V001_TEMPLATE.json | d3568d0653e988ab52a2d18fd2dda697f62c433e368b96d77c064ffe608c3dbb |
| ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json | 48ec0e010cd4228f6b3a7eab78940e956465af32d3d3e796efb41f4a7ca3bfa5 |
| tests/test_h3_campaign_path_c2v001.py | 9777e2b2ff489f00394c42bf666f150cbe87ffef48bf93ee0ea593bb3a1759a8 |
| tests/synthetic/mock_driver_h3_c2v001.py | 374c508e83a6c6a8714be0e4cf25c08fe6d8325671603decdd36c75f5165f57c |
| tests/synthetic/syn_h3_c2v001.py | a59486143ae7723d13b9a566dd2dd94fb82672ccda6e3f1d72e0e2055638cf44 |
| placeholder_chain/v006r12_c4/adoption_policy_cx2v006r12_c4.py | 93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3 |
| placeholder_chain/v006r12_c4/calibration_core_cx2v006r12_c4.py | 192d086348fed9307da99732c0ef146bb336a3d605afc1e9e56b6ce959ad1a73 |
| placeholder_chain/v006r12_c4/calibration_orchestrator_cx2v006r12_c4_q5b1.py | 7ac0785126d8b188b9d06c072e0583a03a182f3643910d1a2e5e24b9f61e3f06 |
| placeholder_chain/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py | 48fd45ef92820770438255713eb6fe606370ece948a9956da0f73c4b6e19f3cb |
