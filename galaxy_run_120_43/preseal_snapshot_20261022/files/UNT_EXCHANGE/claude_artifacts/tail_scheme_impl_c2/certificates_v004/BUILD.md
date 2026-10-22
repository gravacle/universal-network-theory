# certificates_v004: successor certificate records with an explicit source M_s (root A68 "Records")

tail_scheme_impl_c2/certificates_v004, 2026-10-18, about 15:00Z. Successor of certificates_v003, which is unchanged. Hashes are in `HASHES.txt`, computed from bytes.

**Hygiene.**
- No number was recomputed and nothing was launched. No dry run, no forward/route-A/route-B call.
- Not read: `runs_ext/KMAX_A2F10_C5H_RUN_V001`, `runs_ext/UVT_*` (the identity runs are not needed here), NGC targets.
- Writes only under this directory, by exclusive create. Nothing outside was edited, moved or deleted.
- `python3 -I -B`, stdlib only, single-thread BLAS, `nice 10`.
- The compare r7 is loaded in-process and only its `build_context`, `validate_case_block`, `load_producer_registry` and `evaluate_gate` are called.

**Inputs pinned from bytes.** LO_CERT_V003_MS128 `9fdb897a`, GQ_CERT_V005_MS128 `fbceefe6`, EPS_CERT_V006 `598c8fa3`, compare r7 `528dd23a` with FIELDS_R7 `438dc9ca`, and the ten launch-packet `*_P128_MS128_CX1V003.TEMPLATE.json` (shas in `out/CERT_VALIDATION_R7_V001.json`). The V005 addendum (A57, A58 RI-06, A67, A68, A69) is cited, not pinned, because it is still being appended. It read `097563c7` first and `1c368948` at the LO build; the second value is recorded in `decisions_v004`. A69 note 1 (the registry carries producer paths, and the compare hashes producer bytes) is met: `producer.path` is the absolute path of the successor tool. **No compare r8 exists**, so r7 is the latest compare.

## New slot pair (P128 MS128 specs)

| slot | file | sha256 |
|---|---|---|
| `eps_certificate` | `certificates_v002/gates/EPS_CERT_V006.json` (unchanged) | `598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192` |
| `lo_certificate` | `certificates_v004/gates/LO_CERT_V004_MS128.json` | `1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a` |
| GQ gate record | `certificates_v003/gates/GQ_CERT_V005_MS128.json` (unchanged) | `fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21` |

The only change from the certificates_v003 slot pair is the LO slot: `9fdb897a` → `1c384f76`. The EPS slot and the GQ record are the same bytes.

## (1) LO_CERT_V004_MS128 (built)

Tool: `tools/build_lo_v004_c2v001.py`. Diff record: `out/LO_V004_SUCCESSOR_DIFF_V001.json`.

- It is V003 with **`source_gas_M_s: 128`** added. This is the only LO field FIELDS_R7 requires that V003 lacked (Codex1 0023, Codex3 0601, r7 NEW-48).
- The value is read, not asserted. V003 records the source M_s in three places: `gas_M_s`, `tail_config_gas.M_s` and `build.roster_gas.M_s`. The tool refuses unless all three are the integer 128.
- **Numbers unchanged (checked).** 35 of V003's 36 keys are canonical-JSON equal. The only changed key is `producer`, which now names the successor tool (`b8837e0d`). The computing tool, `lo_cert_c2v003_ms128.py` `ba475ef6`, is kept as `numbers_producer`.
- Added keys: `source_gas_M_s`, `numbers_producer`, `successor_of`, `successor_change`, `source_gas_M_s_evidence`, `decisions_v004`.
- Shells, sum, rho, B1 and envelope are V003's: largest shell 3.95e-4 τ at (128,256], sum 8.88e-4 τ.
- Other LO fields FIELDS_R7 requires were already present and are carried: `state_result_sha256` = C4R3, the ten-shell RI-06 partition, and `summed_max_over_tau`.

## (2) GQ: no successor needed (the M_s field is present)

FIELDS_R7 GQ requires `rosters[].M_s` (128 on every DDO roster, 96 on NGC_T120L), `M_s_doubled` = 2 M_s, and `rosters[].all_nodes`. GQ_CERT_V005_MS128 carries all of them:
- 10 DDO rosters at M_s 128 / 256;
- 2 NGC_T120L rosters at 96 / 192;
- top-level `gas_M_s_DDO` 128 and `gas_M_s_NGC` 96.

FIELDS_R7 has no top-level `source_gas_M_s` for GQ. A GQ record certifies M_s against 2·M_s for two sources with different M_s, so one scalar would not describe it.

**DECLARED:** A68's "GQ/EPS records state M_s where they depend on it" is met by the per-roster `M_s`. If the post-r8 compare contract adds a GQ-level field, a GQ successor is built to that contract.

**A67 SF1 (TESTED, reported).** Every DDO roster's `all_nodes.nodes` equals its gq_full part record's `full_domain.nodes`, and each part sha checks. None is the 4096 sample (`a67_sf1_gq_all_nodes_counts`).

## (3) EPS: no successor needed (no M_s field is wanted)

FIELDS_R7 EPS has no M_s field. EPS does not depend on M_s, which is TESTED in `certificates_v003/out/EPS_MS_INDEPENDENCE_V001.json` (verdict EPS_UNCHANGED_M_S_INDEPENDENT, cited by sha in the validation record): the per-shell eps vector is bitwise equal between M_s 64 and 128 builds at K_big 128 and 256. EPS_CERT_V006 stays the EPS slot.

## (4) Validation under compare r7 (TESTED)

Tool: `tools/validate_r7_c2v001.py`. Record: `out/CERT_VALIDATION_R7_V001.json`. All 24 expectations hold (`all_expectations_hold` true).

**Context.**
- `PRODUCTION_K_BIG_A55` is **already 128.0 in r7**, so it was asserted and not modified. `PRODUCTION_GAS_M_S_A57` = 128.
- The probe case block (not a registration) has every T-case `/numerics.uv_tail` set to the real P128 MS128 template, with the slots filled by the new pair. r7 `validate_case_block` accepts it (no reasons).
- TEST producer registry `out/TEST_PRODUCER_REGISTRY_V001.json`: the producer shas of the records read. **It is not a root registration.**

| record | P128 MS128 | codes |
|---|---|---|
| EPS_CERT_V006 | **PASS** | – (envelope readable for SRB_ROT) |
| **LO_CERT_V004_MS128** | **PASS** | – |
| GQ_CERT_V005_MS128 | **PASS** | – |
| LO_CERT_V003_MS128 | RECORD_DEFECT | FIELD_MISSING:LO:source_gas_M_s |
| LO_CERT_V002 (M_s 64) | RECORD_DEFECT | FIELD_MISSING:LO:source_gas_M_s |
| synthetic LO_V004_SRC_MS64 | RECORD_DEFECT | LO_SOURCE_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S |
| synthetic LO_V002_SRC_MS64 (real M_s 64 numbers + its true M_s) | RECORD_DEFECT | LO_SOURCE_GAS_M_S_NOT_THE_A57_PRODUCTION_M_S |
| GQ_CERT_V002, GQ_CERT_V003_KB128 (M_s 64) | RECORD_DEFECT | FIELD_MISSING all_nodes (raised before the M_s codes return) |
| synthetic GQ_V005_DDO_MS64; v003-check canary GQ_MS64_LABELS | RECORD_DEFECT | GQ_DDO_*_M_S_NOT_THE_A57_PRODUCTION_M_S |
| GQ_CERT_V003_KB256_MS128 (sampled only) | RECORD_DEFECT | FIELD_MISSING all_nodes |
| GQ_CERT_V004_MS128 (A67 SF2 FAIL control) | FAIL | GQ_REQUIRED_ROSTER_ABSENT_OR_SHORT:DDO_C4T |

**Regression canaries.**
- Synthetic, on V004:
  - `source_gas_M_s` absent, the string "128", the float 128.0 or `true` → all RECORD_DEFECT (FIELD_MISSING / FIELD_TYPE_int);
  - top shell dropped → RECORD_DEFECT;
  - a shell at 0.006 or a sum of 0.06 under a PASS verdict → RECORD_DEFECT VERDICT_PASS_CONTRADICTS_DATA;
  - wrong state sha → RECORD_DEFECT.
- The seven certificates_v003 check canaries are re-read under r7 and none reads PASS. Their three LO canaries now refuse first on the missing `source_gas_M_s`, so their own mutations are exercised again only by the V004-based canaries above.
- **Empty context:** every slot record is RECORD_DEFECT (P unreadable).
- **No registry:** RECORD_DEFECT PRODUCER_REGISTRY_ABSENT_A62_2.
- **Registry without `b8837e0d` for LO:** V004 is RECORD_DEFECT PRODUCER_NOT_ROOT_REGISTERED_A62_2.

**M_s 64 records under an MS128 context: TESTED, they refuse.** The binding is **not** the A68 CHK-1 form:
- The M_s 64 case block (every T-case gas.M_s = 64) is refused by r7 `validate_case_block` ("C4T: registered uv_tail gas.M_s must be the A57 production M_s 128").
- Passed straight to `evaluate_gate` anyway, it still gives V004 PASS, GQ_V005 PASS and the M_s 64 records DEFECT.
- So r7's g_LO and g_GQ compare the certificate M_s with the **compare constant** `PRODUCTION_GAS_M_S_A57 = 128`, not with the case block's registered gas.M_s. The case-block side is held separately, by validate_case_block.
- **The A68 CHK-1 binding is absent in r7, and no r8 exists.** Under the current sealed constant the effect is the same, but the binding is UNTESTED until the post-r8 compare implements it. Its deciding test is this validator's MS64_UNVALIDATED context: the M_s 128 records must then refuse there.

## UNTESTED / open, each with its deciding step

| item | owner and deciding step |
|---|---|
| Root producer registration of the LO successor tool `b8837e0d…` for gate LO (A62.2). Without it, V004 reads RECORD_DEFECT under any registry. | Root: add it to PIN_PRODUCER_REGISTRY. Per A67 N2, also register the record sha `1c384f76…`. |
| A68 CHK-1 (certificate M_s bound to the case block's gas.M_s) not in r7 | The compare round after r8. Rerun `tools/validate_r7_c2v001.py`'s MS64 context against it. |
| P128 MS128 specs re-filled with the new LO slot and dry-run on r5 | Codex1. Fill `lo_certificate` = {path above, `1c384f76…`}, keep EPS `598c8fa3`. The probe block's normalized uv_tail config shas for this pair are in the validation record (informational; the registered ones come from the real fill). |
| A GQ-level M_s field, if the post-r8 contract adds one | Compare author: name the field. Then a GQ successor is built from V005 with numbers unchanged. |
