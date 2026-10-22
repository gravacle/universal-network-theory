# V006 pre-launch pin entry, draft for root (s0_launch_kit_c2 C2V003)

**Who and what.** A Claude2 root-workflow lane built this at Mon Oct 19 17:58:16 UTC 2026 for root (Claude2, UNT Galaxy Run 120/43). It is the text root pastes into V006 before the seed serial's M-15 record: the 15 `GATE_PIN` lines, `ROOT_LISTED_ROW_GATES NONE`, and the RI45-14 list pin. Nothing is adopted until root writes V006. Nothing was launched, and V006 was not written.

**Labels.** TESTED: run here, result shown. FORMAL: read from the cited bytes. CHOICE: a decision this draft made, which root may overrule.

## Bottom line

- **Paste the block in section 2 at the very end of V006, after its last byte** (FB-3: V006 entries are appended at the end only; RI45-27, ROOT_ITEMS L778). It must be in V006 before the M-15 record, which the seed serial launch writes as its first action (V006 L712, A142 item 6).
- **Replace every placeholder first:** `<n>`, `<DATE_U_STAMP>`, the three RI45-14 fields, and the RI45-24 section line (or delete that line if the RI45-24 entry is not written yet).
- **TESTED, dry, on a scratch copy of V006** (`73663c84`) with the RI45-24 draft appended as A156 and this entry as A157, parsed by the kit's own `s0_kit_c2v002.py` (`0ba823f3`) through its pinned record writer (`a10965b7`):
  - 15 `GATE_PIN` lines extracted, each equal to the draft (name, sha256, path), all under A157;
  - `ROOT_LISTED_ROW_GATES NONE` under A157; no `HANDOFF_PIN`, `SPEC_PIN`, `WATCH_PIN` or `ROOT_LISTED_ROW_GATE` line;
  - `verify_gates`: 15/15 re-hash from bytes; `check_required` against `GATE_DOCUMENT_PINS_V002.json` (`5e688882`): pass;
  - the record writer CLI with `--check-only`: exit 0, `CHECK_ONLY_PASS`, 15 gate documents, row gates `[]`, no file written;
  - the `RI45_14_LIST_PIN` line: its sha256 equals the bytes of `FREEZE_EXPECTED_INPUTS_C2V003.json`, and the kit parser ignores it (CHOICE P1);
  - the RI45-24 draft adds no pin line.
- **Control (TESTED):** pasted with a literal `<n>`, the parser files every pin under the previous `## A<digits>` heading (A108; V006 ends with `## A108 continued`). Replace `<n>`.
- **Every sha256 below was recomputed from bytes at this build** and equals the `GATE_DOCUMENT_PINS_V002.json` row, the file the C2V002 kit pins (`GATE_PINS` constant).
- **Still owed for the seed launch, not in this entry:** `HANDOFF_PIN S0_SEED` (RI45-09), `SPEC_PIN S0_SEED_SERIAL` (RI45-13; V006 L565), `WATCH_PIN MEMORY_WATCH` (A135.5) and the V007 pin (RI45-05). The kit refuses `--launch` without the first three (C2V002 tests Z01/Z01b).

## 1. The 15 gate documents (sha256 from bytes at this build)

| Name | sha256 | Class |
|---|---|---|
| NTEST_K32_COMPARE_COMPLETE | `6f095f64` | N_GATE_AND_M7_TSR_PIN |
| NTEST_N1_RING_RADII | `8867c376` | N_GATE_INPUT_AND_M7_TSR_PIN |
| ROUTE_B_GL4_NODES | `ec1dcca5` | ROW_RULE_INPUT_AND_M7_TSR_PIN |
| GQ_NGC_91_MS96 | `be148bab` | NUMERICS_CONDITION_I6 |
| LO_NGC_K32 | `07745bbf` | LAUNCH_CUSTODY_PIN |
| EPS_NGC91_ANCHOR | `1d5eef1b` | ENVELOPE_SOURCE |
| I1T_NGC_T120L | `3ae7981a` | NUMERICS_CONDITION_I6_D4 |
| S0_POINT_EPS_SEED | `efdc430a` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 |
| S0_POINT_EPS_J0 | `8270b6b3` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 |
| S0_POINT_EPS_J1 | `bfac8f57` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 |
| S0_POINT_EPS_J2 | `5dd9900a` | PER_POINT_CERTIFICATE_NUMERICS_I6_D4 |
| S0_GQ_BINDING_SEED | `903a7d6c` | PER_POINT_CERTIFICATE_CUSTODY_D4 |
| S0_GQ_BINDING_J0 | `cc6113ce` | PER_POINT_CERTIFICATE_CUSTODY_D4 |
| S0_GQ_BINDING_J1 | `4fc1d744` | PER_POINT_CERTIFICATE_CUSTODY_D4 |
| S0_GQ_BINDING_J2 | `934c0a47` | PER_POINT_CERTIFICATE_CUSTODY_D4 |

## 2. Text for root to paste

````
## A<n>: pre-launch pins: the 15 gate documents (M-15 (a)+(1)), root-listed row gates none, and the RI45-14 list (<DATE_U_STAMP>)

Pinned before the first step-5 NGC launch receipt (A142 item 6; M-15 (a)+(1); A133 section 2 row 1). Each sha256 below was computed from the file bytes at Mon Oct 19 17:58:16 UTC 2026 (s0_launch_kit_c2 C2V003). The 15 GATE_PIN rows equal GATE_DOCUMENT_PINS_V002.json (`5e688882`), the file the launch kit pins. Root-listed row gates known at launch: none (FORMAL: no REGISTERED_INVALID_ROW_GATE_CX3V001 document exists; a row gate first adopted at RUNBOOK step 4 is LATE).

```
GATE_PIN NTEST_K32_COMPARE_COMPLETE 6f095f64a1f1acc2ad2910af12f645e18acdf16fb62bfd936386a61c47ef30e9 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json
GATE_PIN NTEST_N1_RING_RADII 8867c3766cc08585286ca969d4aa3fdec47fd9b15a8fe815d466346119c95c70 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json
GATE_PIN ROUTE_B_GL4_NODES ec1dcca572f295dab24e343650a519b6c96e3557e6ccc603f453dea490cb717d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json
GATE_PIN GQ_NGC_91_MS96 be148bab4d80ef412d55d2011cac2e3a1d44725a0ba21a4d2bf43c7ffbdc1a76 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_ntest_eval_cx/out/GQ_NGC_91_MS96_V001.json
GATE_PIN LO_NGC_K32 07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json
GATE_PIN EPS_NGC91_ANCHOR 1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json
GATE_PIN I1T_NGC_T120L 3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json
GATE_PIN S0_POINT_EPS_SEED efdc430a561ae936d860f85ec050f22a10f17c03aad7ad17fc2150744dcde563 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_968c915bece706ea_C4V002_s0seed.json
GATE_PIN S0_POINT_EPS_J0 8270b6b3eb9daddd01e32f7c6cc0fd143afd6b751ff9ced310ac92ca365586da /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_3d7785669b549d6f_C4V002_s0j0.json
GATE_PIN S0_POINT_EPS_J1 bfac8f57233e904aed30f68594645b5b9c97697e47ce088e9d18e7a8fe4aff1e /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_ab7bf95317b37652_C4V002_s0j1.json
GATE_PIN S0_POINT_EPS_J2 5dd9900a7db31003cb1b1054c156f6ac73b062375bae3a423990e782a2ccfdfc /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_POINT_EPS_4b9b4ec88eb2d94c_C4V002_s0j2.json
GATE_PIN S0_GQ_BINDING_SEED 903a7d6c88804bb99175ec78927184f210fa1fb07c32c985c294ef0546d0b979 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_968c915bece706ea_C4V002_gqseedA.json
GATE_PIN S0_GQ_BINDING_J0 cc6113ce39adaa3b24154848d099fec693aec15b91f09c3f9ca74299448d5f27 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_3d7785669b549d6f_C4V002_gqj0A.json
GATE_PIN S0_GQ_BINDING_J1 4fc1d744f2d0cb38a08d086aa8c20603bbd3b43c7c27a9a0d0d83665091402ca /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_ab7bf95317b37652_C4V002_gqj1A.json
GATE_PIN S0_GQ_BINDING_J2 934c0a4774b9153e7fbe25d72c743eff529079644f3fdc03ab060dc25833f3e0 /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ngc_point_producer_c4/s0/build_c4v001/out/S0_GQ_BINDING_4b9b4ec88eb2d94c_C4V002_gqj2A.json
ROOT_LISTED_ROW_GATES NONE
```

**RI45-14 list of record** (A133 section 1.4 L78 and section 2 row 1; reviewer Claude4):

```
RI45_14_LIST_PIN FREEZE_EXPECTED_INPUTS_C2V003 454dd3ccb6f9d1056981aa44b24237e12066c43ef8a37753606b783fa3383e9d /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2/FREEZE_EXPECTED_INPUTS_C2V003.json
```

The list leaves three fields to root, stated here with the pin:
- interior_count = <ROOT_STATES_A_NON_NEGATIVE_INTEGER> (the list records no registered value; its interior_count block lists the sources searched and the unregistered literals, none chosen).
- spec = <CX2V006 | V002/V005A> (write_freeze_manifest_inputs.spec; both admitted, engine coordinates byte-equal).
- notes.A16.1 = <TEXT_COPIED_FROM_THE_DECISIONS_FILE_OF_RECORD>.

RI45-24 entry cited by its section sha256 (RI45-24 recommendation (a)): A<m> <SECTION_SHA256_64_HEX>
````

## 3. After pasting: a check that writes nothing

The kit's record writer, `--check-only`, reads the real V006 and prints `CHECK_ONLY_PASS` with 15 gate documents and row gates `[]`, or `REFUSED` with the reason. Set `RUNROOT` to the run root root uses (see `S0_RUN_ROOT_C2V001.md`):

```
PY=/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
KIT=/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s0_launch_kit_c2
V006='/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
$PY -I -B $KIT/s0_prelaunch_record_c2v001.py --v006 "$V006" --out /tmp/M15_CHECK_ONLY_NOT_WRITTEN.json \
  --require-pins $KIT/GATE_DOCUMENT_PINS_V002.json --require-pins-sha256 5e688882451824931f964e610cf17597d82ee0eb246fb0dce528ec0c6e148042 \
  --first-call S0_SEED_SERIAL --driver-sha256 577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377 \
  --monitor-sha256 ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107 \
  --outdir "$RUNROOT/NGC_P1_S0_SEED_SERIAL_RUN_C2V002_A1" --receipt "$RUNROOT/NGC_P1_S0_SEED_SERIAL_RUN_C2V002_A1.receipt.json" \
  --check-only --allow-pending-first-spec
```

## 4. CHOICES (root may overrule each)

- **P1. The RI45-14 list is pinned with its own keyword, `RI45_14_LIST_PIN`, not `GATE_PIN`.** The list is not an r3a section-4 gate document. As a `GATE_PIN` line it would enter the M-15 record's gate list and its ON-TIME rule. The line keeps the kit's field syntax (column 0, name, 64 hex, absolute path last), and the kit parser ignores it (TESTED).
- **P2. The three RI45-14 fields root owns are stated in the same entry** (interior_count, spec, notes.A16.1). The list is due at the same moment as the pins (A133 section 2 row 1, L185), and A133 section 1.4 (L78) takes interior_count from the list. `FREEZE_EXPECTED_INPUTS_C2V003.json` records no registered interior_count value; its `interior_count` block lists every source searched and the unregistered literals (5 in steps 6-7 rehearsal (Codex1); 5 in v003g review harness; 0 in phase1 v003a tests; 6 in phase1 v003a tests). This draft chooses none.
- **P3. The RI45-24 section sha256 is recorded here**, because RI45-24 asks that its entry be cited by its own section sha, which cannot be inside that section. Delete the line if this entry is written before the RI45-24 entry, and record the sha in the next entry instead.

## 5. Sources (sha256 from bytes at this build)

- V006 at build: `73663c8448bde9ea1bd382b64050d8c2445d58d0930b04d36da22b2ebbbda8a9` (read once, read-only). A142 item 6 L712; A135 item 9 L565.
- `GATE_DOCUMENT_PINS_V002.json` `5e688882`; `s0_kit_c2v002.py` `0ba823f3`; `s0_prelaunch_record_c2v001.py` `a10965b7`.
- `FREEZE_EXPECTED_INPUTS_C2V003.json` `454dd3ccb6f9d1056981aa44b24237e12066c43ef8a37753606b783fa3383e9d`; `PRELAUNCH_CHECKS_C2V003.json` (the full parse record, `dry_parse`).
- ROOT_ITEMS_STEP45_V002.md `417de6fe`: RI45-14 L273; RI45-27 (FB-3) L778. A133_TWO_PHASE_PROTOCOL_V001.md `cd92ef91`: L78, L185.
