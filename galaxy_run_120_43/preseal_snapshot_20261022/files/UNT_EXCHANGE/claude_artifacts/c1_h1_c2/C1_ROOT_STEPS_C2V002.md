# C1 (H1): root steps (c2v002, after A209)

Helper draft for root. It supersedes `C1_ROOT_STEPS.md` (`e85148b5`).

Nothing here has been run against claude_artifacts except the c3v005 build (written in `s4rc1_c3/build_c3v005_c2/`). Nothing has been published. Take every stamp from `date -u`; times for the principal are in CDT.

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
TP=/usr/sbin/taskpolicy
ART=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts
C1D=$ART/c1_h1_c2
B5=$ART/s4rc1_c3/build_c3v005_c2
SCR=/private/tmp/claude-501/-Users-bgm-MB-Work/04dac55c-b963-46a5-9ea4-74afb63af51b/scratchpad/c1_h1
REG=$ART/s4rc1_c3/registry_c2v001/REGISTRY_31pts_20261020T140004Z.json
REG_SHA=2dea408ff698e265a41bac1ef2562737ae98ffd4583477632e7a79507a15e319
DRAFT_SHA=3a9299a343bb0a54d90b9e92d2814e78ce44def846adf5a37a890d80a4cf0320
FILL_SHA=3faf4a6c423ecc14f330329e9495c4d79786b8bcfe66a2ae339dbf88440305ec
```

## 0. Before the dispatches

### 0.1 c3v005 is built (A209 item 3). Codex1 reviews it, then root adopts it

- Folder: `$B5`.
  - `HASHES_C3V005_C2.txt` `3f51c7a24b945f1b2ae2d8373b536865f5fb1f59e652fc5724cc452077bad6ce` checks 8121/8121 with `cd $B5 && shasum -a 256 -c HASHES_C3V005_C2.txt`.
  - `CHANGES_C3V005_C2.md` `f262103d…` maps every hunk to A209.
- Common c3v005 `2308a47ce3c758b6befa0aa954fa7e2b6ad7f4cb41ed73d4b8cd1d257021e7c5` = c3v004 plus:
  - three PINS lines (L77-79: `211a3220`, `08e9ac0a`, `7044e131`);
  - `CANONICAL_APPROVED_PRODUCERS` grown to the six in A209 order (L93).
- Assembler c3v005 `7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310` = c3v004 with only COMMON_PATH, COMMON_SHA (L48-49) and the docstring changed.
- **Suite of record:** 310/310 (295 c3v004 cases + 15 A209 cases), results `3a779494…`.
- **Mutation of record:** 9/9 caught, `ee32363d…`.
- **Codex1 (distinct lineage) reviews** `$B5`: the two module diffs, the suite and the mutation check.
  - The review is a delta on c3v004. It needs no producer run and no real input.
- **After Codex1's review, root adopts c3v005 in V006.** This comes before C1 is frozen.
  - It supersedes A207's "registry_assembler_c3v004 verify against C1".
  - The registry `2dea408f`, bundles and producer pins stay byte-identical. c3v005 never rebuilds them.

### 0.2 Publish the draft and the freeze tool

Use exclusive create.
```
mkdir $C1D
cp -n $SCR/C1_H1_DRAFT_C2V002.json $C1D/
cp -n $SCR/fill_c1_pin_c2v002.py $C1D/
shasum -a 256 $C1D/C1_H1_DRAFT_C2V002.json $C1D/fill_c1_pin_c2v002.py
# must read $DRAFT_SHA and $FILL_SHA
```

- Draft v002 changes nothing in `tail_readiness`. Its digest without the review is still `6dc87838…`.
- It moves the verifier references to c3v005, records A209, and adds N1 and N6 (below).
- The c2v001 draft and freeze tool are not published.

### 0.3 Post the Codex3 dispatch

- Fill `<NNNN>` in `$SCR/CERT_POLICY_REVIEW_REQUEST_C2V002.md`. It already applies A209 item 5:
  - V006 is the named exception;
  - `a1dcdea8` and `lo_producer_cx2v004` `5db60d0f` are on the may-open list;
  - no `synthetic` key;
  - Codex3's own check script goes under `cert_policy_reviews_cx3/`.
- Write it by exclusive create as `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/<NNNN>_2026-10-20_codex3_C1_certificate_policy_review.md`.
- The review is a C1 prerequisite before HEADLINE11.

## 1. After Codex3 posts

```
REV=$ART/cert_policy_reviews_cx3/DDO154_CERTIFICATE_POLICY_REVIEW_C1_H1_CX3V001.json
CHK=$ART/cert_policy_reviews_cx3/check_c1_h1_policy_cx3v001.py
REV_SHA=$(shasum -a 256 "$REV" | cut -c1-64); echo $REV_SHA      # must equal the sha in Codex3's post
shasum -a 256 "$CHK"                                             # must equal the post and the review's check_script
```

If `ok` is false, `blocking_findings` is not empty, or any check reads FAIL, stop. Root rules on the findings. Any fix is a new review file, never an edit.

## 2. Fill the review pin into C1 (freeze tool v002, A209 item 6)

The tool checks, from bytes:
- the draft pin and schema C2V002;
- the placeholder;
- the tail_readiness digest without the review, which must be `6dc87838…` (a constant in the tool);
- the guard bytes;
- the review:
  - path under claude_artifacts, no symlink component, no `ngc3198`/`uvt_` component, a regular single-link file of at most 8 MiB;
  - strict JSON;
  - the ten binding fields as canonical JSON bytes (`ok` must be `true`, not `1`; producer order exact);
  - the custody fields: `reviewed_c1_draft` as a whole pin, the digest, the registry pin, the two trusted lists, `blocking_findings == []`, `distinct_from_producer_lane` `true`;
  - `reviewer_lane == "Codex3"`, `signed_utc`;
  - all twelve checks PASS;
  - no `synthetic` key at any depth;
- the check script pin, under `cert_policy_reviews_cx3/`, with the same file checks.

It then changes only `tail_readiness.certificate_policy_review` and writes by exclusive create.
```
cd / && $PY -I -B $C1D/fill_c1_pin_c2v002.py --draft $C1D/C1_H1_DRAFT_C2V002.json --draft-sha256 $DRAFT_SHA \
    --review "$REV" --review-sha256 $REV_SHA --out $C1D/C1_H1_C2V001.json --utc "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
C1_SHA=$(shasum -a 256 $C1D/C1_H1_C2V001.json | cut -c1-64); echo $C1_SHA
```

- **Exit 0** means WRITTEN: schema `UNT_DDO154_C1_TAIL_READINESS_H1_C2V001`, and it prints the C1 pin and `c1_tail_readiness_digest`. It is the frozen C1 only after step 3 passes and step 4 records it (A209 item 4, Q9(b)3).
- **Exit 2** means REFUSED, and nothing was written. Root rules (A50).
- **Tested on synthetic inputs: 41/41 as expected** (`synthetic_gate_test_v002/FILL_TEST_RESULTS_C2V002.json` `f7f1fca570a514f2830b1bf00496f8bf8ab20271eccaf89d9599c8eaa5825c50`).
  - This includes `ok=1`, `"true"`, reordered producers, symlinked, hard-linked and >8 MiB reviews, `ngc3198`/`uvt_` components, outside-root paths, duplicate keys, NaN, a failed check, and a v001 draft.
  - The synthetic fill output passes the c3v005 policy gate (G01) and is refused by c3v004 with exactly the three A209 blockers (G02).
  - Synthetic outputs carry schema `UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002`, and the tool never writes one under claude_artifacts.

## 3. The real-gate run of record: c3v005 verify, under `taskpolicy -b` (A209 item 4)

The out-root must be `s4rc1_c3/registry_<name>` and must already exist (assembler c3v005 L472-480).
```
cd $B5 && shasum -a 256 -c HASHES_C3V005_C2.txt | grep -vc ': OK$'     # must print 0
mkdir $ART/s4rc1_c3/registry_c1verify_c2v001
cd / && $TP -b $PY -I -B $B5/registry_assembler_c3v005.py verify --registry $REG --registry-sha256 $REG_SHA \
    --c1 $C1D/C1_H1_C2V001.json --c1-sha256 $C1_SHA --out-root $ART/s4rc1_c3/registry_c1verify_c2v001
```

- **Expected:** exit 0, `{"ok": true, "n_ok": 31, "n": 31, "c1_policy_gate_blockers": []}`. It writes `VERIFY_2dea408ff698_<UTC>.json`; re-hash it from bytes.
- **This is the run of record** (A209 item 4). Claude4 is at 100 % until Fri 23-Oct 19:00Z (A208). The distinct checks are Codex3's certificate_policy_review and Codex1's c3v005 review. Disclose this in the seal entry.
- **Status: UNTESTED on real inputs.** This run is the deciding test.
  - TESTED so far:
    - c3v005 policy gate on the synthetic filled C1 (fill test G01);
    - six-pin verify on synthetic registries, including the end-to-end registry from the real slot proof (suite T_C5_03, T_C5_03b);
    - three-pin C1 still passes (T_C5_07);
    - a seventh pin, an aliased pin and `ok=1` are refused (T_C5_04-06).
  - Not run:
    - the per-point real custody derivation for 31 points at background QoS (its time is not measured);
    - the verify CLI's real custody loader.
- c3v004 needs no run: A209 records its three F3 blockers, both lenses re-ran it in-process, and suite T_C5_09 and fill test G02 reproduce them.
- **Any refusal stops the H1 path.** Root rules (A50).

## 4. Record in V006 (C1 frozen after step 3; before HEADLINE11's first PRELAUNCH)

- **C1 (H1) frozen:** `$C1D/C1_H1_C2V001.json` `<C1_SHA>`, from draft v002 `3a9299a3…`, filled by `fill_c1_pin_c2v002.py` `3faf4a6c…`.
  - tail_readiness digest: `<printed>`. Without the review: `6dc87838…`.
- **Review:** `$REV` `<REV_SHA>` and check script `<CHK sha>`, Codex3 (A205 4(i)), with the disclosure.
- **Verify of record:** c3v005 `<VERIFY sha>`, 31/31 (A209 item 4). Verifier c3v005 as adopted (common `2308a47c`, assembler `7df1c481`), with Codex1's review pin.
- **Contents:**
  - registry `2dea408f`;
  - custody `6810b7c3`;
  - enumerator b1 `4ca7f364`;
  - the six approved producers (A209 ruling 1);
  - `trusted_source_producers` [`67fddd24`, `7044e131`];
  - `trusted_row_policy_review_sha256` [`07eee40b`, `6c9475e1`, `f5b6c66e`];
  - `row_policy_reviews`.
- **Rule:** never edited (A134 Q9). A later change is a successor C1, and the registry pins stay byte-identical.

## 5. At H1, after the verdict (from code; reminders)

1. **H1 run config.**
   - Set its `tail_readiness` to C1's `tail_readiness` exactly.
   - Check it with: `$PY -I -B -c "import json,sys;a=json.load(open(sys.argv[1]))['tail_readiness'];b=json.load(open(sys.argv[2]))['tail_readiness'];sys.exit(0 if a==b else 1)" "$CFG" $C1D/C1_H1_C2V001.json`.
   - The direct adapter (L11) refuses any extra top-level config key, so C1's other keys stay out of the config.
2. **Final-spec producer v004 `fcbf1c3e`.** It runs on that config and reads the review bindings (L747-756).
3. **Step-4 admission `sources`.** It maps path → sha, and the source review's `approved_sources` must equal it exactly (guard011 L116). Inside the guard011 fence, every `/Research/` .py that is compiled or imported must be listed (guard011 L136-145, L159-160, L174-179: `UNPINNED_PREFLIGHT_SOURCE`).
   - **Existing map (A131, A139):**
     - the six producers;
     - custody `6810b7c3` and enumerator `4ca7f364` (guard011 L243-245);
     - guard011 `eb97e303`, launcher012 `59c00707`, the tail library `2026f2b6`, and the q5b1 wrapper `7a6af535` as `context_module`;
     - `direct_context` `bdedb83e`.
   - **N1 additions (A209 item 6),** sha256 from bytes at 14:54Z (also in draft v002 `h1_requirements_outside_c1.admission_sources_must_include.A209_N1`):
     - guard b1 (wrapper L30): `$ART/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py` `9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677`;
     - core (wrapper L27): `$ART/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6`;
     - parent v005 (core L23-24, L41-47): `$ART/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py` `c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d`;
     - sensitivity policy (wrapper L29): `$ART/calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py` `8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f`;
     - custody's imports (custody L19-22, L60-67, loaded at `derive_custody`, wrapper L92-93):
       - driver r5 `$ART/tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py` `b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6`;
       - `$ART/calib_tail_readiness_cx2/certificates_per_point/certs_common_r5_cx2v001.py` `c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7`;
     - the adoption policy: the `adoption_policy` pin of root's step-4 admission config (guard011 L203 loads it inside the fence). **Not located by this helper.**
   - **Transitive closure: UNTESTED.** Whatever these modules load in turn inside the fence must also be listed, for example the driver r5 stage modules pinned at driver L190-217. Deciding test: a fence-only admission check before the first HEADLINE11 PRELAUNCH, or that PRELAUNCH itself. Its refusal names the unlisted path.
4. **PRELAUNCH005 `117b3520`.**
5. **Per-call acceptance.** The policy comes from C1, as in the draft's `acceptance_policy_inputs_from_c1`:
   - the approved list exactly (h3_accept_call L274-277 requires it to equal the config list);
   - `trusted_source_producers`;
   - `row_policy_reviews`;
   - `root_ruling_refs` = [`56774ba7`, `bcb6df8e`];
   - `approved_evidence_producer_sha256` [`7044e131`];
   - `approved_uniform_producer_sha256` [`2832ceb9`];
   - **N6 (A209 item 6):** `prelaunch_bundle` = the registry record's `bundle` pin, registry `2dea408f` `points[<point key>]["bundle"]` (exact `{path, sha256}`). This is what `h3_accept_call_c2v004` `eb895263` L281 does: `policy = dict(..., receipt=receipt, prelaunch_bundle=rec['bundle'])`.

## Notes (not on the HEADLINE11 path)

- **SENS (A209 item 8).** SENS (D ≠ 4.04) needs `tail_readiness.sensitivity_deciding_iii`, which is null here, so SENS needs a successor C1. It is ruled when SENS is scheduled.
- **S1 C1 (A209 item 7).** It has the same three-pin defect: KS6′ `c8dc59a1` L766 and G2 `7eb456cd` L463 check their own approval, and G6b `65834e9b` is likely the GQ_SIGNED producer. This goes to the S1 C1 policy review (A205 item 4(iii)) and the KS4′ verifier. Root rules the S1 list before the S1 C1 is frozen (step S8).

## UNTESTED, with the deciding test

1. c3v005 verify on the real registry with the real C1: step 3.
2. The freeze tool in real mode, with every path under claude_artifacts. Its real-mode content checks are unit-tested (U01-U07), and its path checks pass on the real guard path in every synthetic run. Deciding test: step 2.
3. The N1 transitive closure and the adoption-policy pin. Deciding test: step 5.3.
4. Codex1's c3v005 review: step 0.1.
