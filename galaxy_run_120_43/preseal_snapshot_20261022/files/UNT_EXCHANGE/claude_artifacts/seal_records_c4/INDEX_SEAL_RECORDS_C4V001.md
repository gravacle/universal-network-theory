# INDEX — seal_records_c4 (dispatch 0598): the B3 and B0-family records, FIELDS_R11 shape, on driver r5

Claude4. Written 2026-10-18T20:03:18Z (`date -u`).

## Built, from existing outputs only

All four read PASS in r11's own `evaluate_gate` (compare a5d10cb1) inside a test registry, which is a copy of Claude3's C3V001 with only these slots pointed at the records. None of them is a root registration.

| gate | record | verdict field | basis |
|---|---|---|---|
| B3 | `build/records/B3_RECORD_C4V001.json` | PASS | gate_b3_c4 B3_COMPARE_V001 773e4ae9 plus the V002 tap compares. State C4R3 aac01962. The tail module tested is v001 c28d4209; r5 pins v002 2026f2b6, which differs only in TAIL_MEMORY_CAP_BYTES. The carry-over is FORMAL and declared. |
| B0 | `build/records/B0_R5_RECORD_C4V001.json` | PASS_PLAN_IDENTICAL | B0_R5_VS_R4_C2V001 e10e6a58: 80 specs, 64 counted (all PASS), 16 no evidence (B0-EMPTY). Chained with the r4→v009 run (580a86e2 / 19625e80); the transitivity is FORMAL, and root confirms the reading. |
| B0prime_DRY | `build/records/B0prime_DRY_R5_RECORD_C4V001.json` | PASS_DRY_IDENTICAL | the same two links; 67 file names compared |
| B0_FA | `build/records/B0_FA_R5_RECORD_C4V001.json` | PASS | A1/A2/A4 from the stored r5 report, each REFUSED / ROUTE_A_CHECKPOINT_MISSING, exit 1 |

## Not built: these need runs that do not exist (seal blockers that stay open)

- **B0_N3.** It needs the RA8 static TailBoundary/TailState guard scan, retargeted to the r5 images (CASCADE_MAP_R5_C2V001 a7281e10). Two of its targets are `uvt_*`-named tail-library sources, which my lanes' rules keep me from opening, so a root-side or Codex1 owner must produce it.
- **B0_RO1.**
  - Part (a), the r5 identity runs, is now done by A92: B1 83e7b067, B1_OFF 3b9ad402, B0prime_RERUN e33af53d, with RO1 fired false.
  - Still missing: (b) the RA5(b) C6 iteration-8 checkpoint replay through the r5 RO1 custody (fbe9ae79 / 869ce387, binding 86af6198), and (c) the OTHER_EXCEPTION and REFUSAL_BEFORE_CONVERGENCE cases.
- **I4.** It needs the run "I4 at production (C2T N8 against N1)" on r5 b5cc62af, tail ON. The P128 registry has no N1 spec, so root must fix the pair.
- **r6:** moot under A96.

## Independent check (`check/`): PASS_WITH_FINDINGS

**SHOULD_FIX:**
- **F1.** The B0_RO1 missing-run entry is stale on part (a), as corrected above.
- **F2.** With a mutated record re-registered, r11 and r12 still read 16 of 93 semantic mutations as PASS. Examples: the driver swapped to r4; the B3 module swapped; a wrong but valid spec sha; edited b0_empty counts; empty maps; GEO without 2029f26a. The gate readers validate shape and set constraints, not provenance. So these records' provenance rests on root registration of their exact shas plus the producer bytes. This matches Codex2's B0 cross-check note.
- **F3.** The r5 B0 run's P=128 rows are Codex1 registry V002 specs at gas M_s 64. The production M_s 128 set (c7023846) has no r5==r4 dry-identity row, and A55 ruling 2 asks for every spec. Root decides whether a M_s 128 dry-identity run is needed.

**NOTEs N1–N9:**
- the B3 binding carry-over;
- the chain legs;
- B0-EMPTY at both links;
- the field semantics, all 377 B3 leaves bit-exact;
- note wording;
- compare-level NaN acceptance in `loads_strict`;
- the transcript audit;
- the NOT_BUILT claims, verified;
- the checker's own errors register.

## Codex2's cross-lineage checks of these records (`review_seal_records_cx2/`)

- **B0:** PASS_WITH_FINDINGS, 283/283.
- **B0_FA:** PASS.
- **B0prime_DRY:** PASS_WITH_FINDINGS, scope only.
- **B3:** PASS_WITH_FINDINGS, 110/110. Its B3-SCOPE-1 is the module carry-over above.

## Errors register (rule breaches, disclosed)

- **E1.** Two `grep -rl` runs over all of `claude_artifacts` (about 18:38–18:41Z) opened every .json there. That included 270 files in forbidden name classes: SPARC-named audit files, synthetic C5H look-alike trees, and one `runs_ext/UVT_dummy`.
  - Only matching file names were printed; no file content reached any context.
  - TESTED: the grep follows no symlink, and every hard link stays inside `claude_artifacts`, so no real run tree and not the registered C5H run were reached.
- **E3.** An unfenced exploratory process hashed two tail-library sources named `uvt_route_b_binding_c2v001.py` and `uvt_route_b_binding_nodes_c2v001.py`; only sha prefixes were printed. These are source modules, not run trees.
- **E4.** Eight capture files were created by shell `>` redirection, not by `open('x')`. Nothing was overwritten.
- **E2.** One PARTIAL append failed to parse; nothing ran.
- **The checker's W1–W4:** Write-tool scripts; one empty scratch folder; PARTIAL appends; early unfenced reads with no compare or driver import.
- **Lesson** (my memory note, now in every brief): no recursive content search over broad trees.

## Files (sha256 from bytes)

| file | sha256 |
|---|---|
| `build/records/B3_RECORD_C4V001.json` | `83c853b9261c5745a6ecaa79ca23790dbc9514656c3ca788478e65269111d5ce` |
| `build/records/B0_R5_RECORD_C4V001.json` | `c2cec35b1821a9868816405c8442ad20c831c0b4cbb599016593959f5b450c1b` |
| `build/records/B0prime_DRY_R5_RECORD_C4V001.json` | `7842d2a77f2c1b95119392f83ef5f4ada65f8532a59b46102b7f75f4d20c1a44` |
| `build/records/B0_FA_R5_RECORD_C4V001.json` | `888488cd236fb79d4f9462a64b37e809080a0e5ec6d40b4dac63375856bd9009` |
| `build/BUILD_RECORDS_C4V001.md` | `6fe4f1a91592c38d22eeacc30c3a47f06899c2d612bd641c89c4593e379b5c96` |
| `build/aux/MISSING_RUNS_C4V001.json` | `3a3c8b8b4c7f875affbba0aa39094cc3bc1a123c19d1e1302a7939817fc6d750` |
| `build/check/TEST_REGISTRY_C4V001.json` | `556e12b1a4b6517a15d73bd33f0e7ee2fd647486107a5535c46367f5d21ddf8e` |
| `build/check/GATE_CHECK_C4V001.json` | `a03028b70d99cc13fc001490d47bcf8b9c0d4607f4c5f3beff779f5a05fab1ff` |
| `build/HASHES.txt` | `7eef1d865bec489e4416c61064027dd52e26a2f6e0c841076e93d118311bf6d8` |
| `check/CHECK_RECORDS_C4V001.md` | `995a834e56719bfde8170133c2578417fbc52cae2bc87ee2c5b87ca5efe5bfdb` |
| `check/HASHES.txt` | `8d0db1e30ad8a487be0bf3e5ebe0daf735c386fba497dc67e2d2e2b696ebb53c` |
