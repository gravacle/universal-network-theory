# Test notes: step-4 final-spec producer v004 (root 0697)

**Who.** A Claude4 workflow helper (test and adversarial-check step). Claude4 is the lane; this is not a separate account.
**When.** Notes written 2026-10-19T13:03Z (`date -u`). The record run started at 2026-10-19T13:00:01Z.
**Scope.** This covers the diff audit, the test update, the test run and the bitwise check. Nothing was launched. No physics value was computed. No producer file was edited.

## Inputs (each sha256 taken from the bytes)

| Object | Path | sha256 |
|---|---|---|
| Producer v004 (under test, unchanged) | `v004_work/tools/produce_final_step4_specs_c4v004.py` | `fcbf1c3ed175e1cfb3519c33324622a3b0ed190769e71b199687bd46dd1cb7ba` |
| Producer v003 (reference for the diff and task 4) | `handoff/tools/produce_final_step4_specs_c4v003.py` | `b7fb4d530eaf552995626ea059a8e06c5df85862ce007d5dded2a65b3b6a5099` |
| Wrapper v002 | `s4_acceptance_c2/wrapper_q5/build_v002/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py` | `7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d` |
| b1 certificate guard | `s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py` | `9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677` |
| Wrapper core (loaded at wrapper L27) | `calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py` | `dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6` |
| Fence (both copies) | `fence_c4v003.py` | `5851f42f259ab5b967c89ec0c66e7e1573353f1076bb498e5aae60ad04b42940` |
| Test file before the edit (a byte copy of the v003 tests) | `v004_work/tools/test_produce_final_step4_specs_c4v004.py` | `ec62fe643644a5949d55cfdb0e35e075c0b9019759c3c3c229265a327dc47df3` |
| Test file after the edit (record run) | the same path | `74b57d7d19298bd5381459fd470999eaa4936b26ce3a4894337cfd70f6a45268` |

## 1. Diff audit, v003 to v004 (task 1)

**Result.** Every hunk is one of the intended changes. The AST comparison confirms the confinement from bytes (`V004_STATIC_AST_CONFINEMENT_V003_TO_V004`): only five top-level entities differ, namely the docstring, `CERT_GUARD_SHA`, `DRIVER_SLOT_RULE`, `RHO_SCHEMA`/`RHO_GATE` and `verify_final_registry`. The other 109 entities are identical, including `World`, `json_bytes`, `point_identity`, `validate_block`, `Reader`, `strict_json`, `write_outputs`, `cmd_final`, `cmd_provisional` and `main`.

`diff -u` gives eight hunks:

| # | v004 lines | What changed | Intended? |
|---|---|---|---|
| 1 | L1-8 | A new docstring prefix; the v003 docstring is kept after it | yes (docstring) |
| 2 | L77, L80 | Usage names now say `c4v004` | yes (usage names) |
| 3 | L163-168 | Comments on `BUNDLE_SCHEMA`, `PROOF_SCHEMA` and `POLICY_REVIEW_SCHEMA` (values unchanged); `CERT_GUARD_SHA` 5f1e49e6 → `9e3fc109`; new `DRIVER_SLOT_RULE`; new `RHO_SCHEMA`, `RHO_GATE` | yes |
| 4 | L737 | `verify_final_registry` docstring citation | yes (citation) |
| 5 | L746 | Comment citation | yes (citation) |
| 6 | L753 | `'driver_slot_rule': DRIVER_SLOT_RULE` | yes |
| 7 | L780 | `('lo_certificate', 'LO_RHO_SLOT')` | yes |
| 8 | L790-806 | The LO_RHO_SLOT block replaces v003 L780-781, which required `covers_all_consumed_states is True` | yes |

**How the wrapper got here.** Wrapper v002 equals `ef3d3d69` except at L30, L74 and L148-191 (`diffs/WRAPPER_ef3d3d69_TO_Q5B1_7a6af535.diff`). `ef3d3d69` differs from v003's reference `24abe3bc` only at L27, where it loads core `dc895f8a` instead of `a595c5c0`. Core `dc895f8a` differs from `a595c5c0` only at L200 and L202, which hold the adoption-policy pin. So v003's mirror of wrapper L79-147 still holds line for line.

The functions v004 cites by `a595c5c0` line numbers sit at the same lines in `dc895f8a` with the same conditions: `canonical`/`digest` at L34-38, `validate_block` at L212-231 and `point_identity` at L233-238. v004's `validate_block` also requires `'mode' not in uv_tail`, as v003 did.

The guard change from `5f1e49e6` to b1 is confined to the docstring and the acceptance-phase signed-offset branch (`offset_b1/diffs/certificate_guard_b1_c2v001.diff`). The prelaunch path is unchanged.

### Each changed check against wrapper v002, both quoted

**(a) Guard pin.** This mirrors the wrapper exactly. TESTED: the guard bytes hash to `9e3fc109`; wrapper L30 holds this pin and L73 binds it.
- v004 L166: `CERT_GUARD_SHA = '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'`
- Wrapper L30: `G=load(Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py'),'_cx2certguard',expected='9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677')`
- Wrapper L73: `'guard_sha256':O.sha256_file(G.__file__),`

**(b) Slot rule.** This mirrors the wrapper exactly. The string is byte-equal (TESTED, anchor L74).
- v004 L167 and L753: `DRIVER_SLOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'` and `'driver_slot_rule': DRIVER_SLOT_RULE,`
- Wrapper L74: `'driver_slot_rule':'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE',`
- The two sides compare differently. v004 uses `same()`, which compares canonical JSON. The core's `checked_gate` (L76-77) uses `doc.get(k) != v`. For a string the two agree. This comparison is inherited from v003.

**(c) Gate name.** This mirrors the wrapper exactly. A bundle without the key is refused by both:
- v004 refuses with `PIN_REQUIRED`;
- the wrapper raises `KeyError`, which it catches and reports as a blocker.

The lines:
- v004 L780: `for slot, gate in (('eps_certificate', 'EPS'), ('lo_certificate', 'LO_RHO_SLOT')):`
- Wrapper L148: `for slot,gate_name in (('eps_certificate','EPS'),('lo_certificate','LO_RHO_SLOT')):`

**(d) No coverage key on the proof.** This mirrors the wrapper exactly: the key is refused whatever its value. Both sides read the proof only, not the ρ record.
- v004 L793-794: `need('covers_all_consumed_states' not in proof, 'LO_RHO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES ...')`
- Wrapper L163-164: `if 'covers_all_consumed_states' in proof: raise Error(...)`

**(e) The lo slot is the registry's `lo_certificate`.** This is equivalent, but it holds by construction (see N-2).
- v004 L795: `need(same(slots[slot], rec.get('lo_certificate')), 'LO_SLOT_NOT_THE_REGISTERED_RHO_RECORD ...')`
- Wrapper L165-166: `if slots[slot]!=rec.get('lo_certificate'): raise Error('lo slot is not the registered rho record of this point')`

**(f) Reading the ρ record.** Same file, stricter reader (see N-3).
- v004 L796: `rho = READER.doc(slots[slot], 'registered rho record ' + key[:16], cap=CAP_CERT, root=CERT_ROOT)`
- Wrapper L167: `rho=M.pin_doc(slots[slot],'registered rho record')`. Core L60-61 defines this as `json.loads(O.read_pinned(pin, label))`.

**(g) The ρ fields.** These mirror the wrapper exactly for schema, gate, point, settings, full search and coverage:
- `point_sha256 == key` is the wrapper's `M.digest(ident)`, because v004 L766 checks `key == digest(rec.identity)` and `fill_slots` checks that `rec.identity` equals the spec's `point_identity`;
- `is True` is the wrapper's `is not True`, negated. TESTED: `coverage_complete` set to `1` is refused.

The custody comparison is substituted; see (h). The lines:
- v004 L798-801: `rho.get('schema') == RHO_SCHEMA and rho.get('gate') == RHO_GATE and rho.get('point_sha256') == key and rho.get('settings') == 'registered' and rho.get('full_registered_search_executed') is True and rho.get('coverage_complete') is True`
- Wrapper L168-172: `rho.get('schema')!='UNT_POINT_RHO_NUMERICAL_CX2V001' or rho.get('gate')!='RHO_G' or rho.get('point_sha256')!=M.digest(ident) or rho.get('custody')!=custody or rho.get('settings')!='registered' or rho.get('full_registered_search_executed') is not True or rho.get('coverage_complete') is not True`

**(h) Custody.** This is a substitution, not a mirror; see N-1.
- v004 L805-806: `need(isinstance(rho.get('custody'), dict) and digest(rho['custody']) == proof.get('custody_sha256'), 'RHO_CUSTODY_NOT_THE_PROOF_CUSTODY ...')`
- Wrapper L169: `rho.get('custody')!=custody`
- Wrapper L150: `proof.get('custody_sha256')!=M.digest(custody)`. This applies to both the EPS proof and the LO_RHO_SLOT proof.
- `custody` is the output of the pinned deriver (L92-93), which v004 does not run.

**Citations.** All the new citations were checked against the bytes: L30, L40, L59-77, L70-75, L74, L145-147, L148, L150, L160-172, L163-164, L165-166, L168, L168-172 and L169.

### Findings (A115 severity)

**No BLOCKING finding.** On honest inputs, no changed check makes v004 refuse a registry that wrapper v002 accepts, or accept one it refuses.

**N-1 (NOTE): custody is checked indirectly.**
- *Never stricter.* On every input the wrapper accepts, v004 also passes (h). The wrapper's checks give `rho.custody == custody` and `LO proof custody_sha256 == digest(custody)`. The custody is a dict of five sha strings, and the guard requires that. For such a dict, Python `==` implies canonical equality, so `digest(rho.custody) == custody_sha256`.
- *Looser in two ways.*
  - v004 cannot compare the custody with the deriver's output. This is documented in `not_established_here`.
  - v004 never compares the EPS proof's `custody_sha256`. TESTED in `FINDING_EPS_PROOF_CUSTODY_NOT_COMPARED_ADMITTED`: a registry whose EPS proof carries a different custody sha reaches v004's last gate. Wrapper L150 refuses that registry whatever the deriver returns, because both proofs must equal `digest(custody)`.
- *Not reachable from honest pinned producers.* They derive one custody per point from the same pinned inputs, and root's PRELAUNCH runs the wrapper check.
- *Optional tightening.* Require the EPS proof's `custody_sha256` to equal the LO_RHO_SLOT proof's.

**N-2 (NOTE): the lo-slot check in (e) is tautological in v004.**
- `fill_slots` (L504-506) and `verify_final_registry` (L767) both take the slot as `strict_pin(rec[field])`. So `same(slots['lo_certificate'], rec['lo_certificate'])` is always true, and no input file can make it fire.
- TESTED in `V004_STATIC_LO_SLOT_RULE_HOLDS_BY_CONSTRUCTION`. The check is reached only by injection, in `Q5_LO_SLOT_NOT_REGISTRY_LO_CERTIFICATE_INJECTED`: `strict_pin` is patched for FIRST's lo label, which gives three calls (`fill_slots`, the `Reader.raw` re-pin and the verify slots).
- The property the wrapper checks, that the spec's lo slot is the registry's `lo_certificate`, holds by construction for v004 output.
- There is no accept/refuse difference. The CLI-reachable forms are refused earlier, by `BUNDLE_DOES_NOT_BIND_THE_SLOTS` and `PROOF_DRIVER_CERTIFICATE_NOT_THE_SLOT` (both TESTED).

**N-3 (NOTE): v004 reads the ρ record more strictly than the wrapper.**
- *What v004 adds.* v004 parses the ρ record with the strict reader, which refuses NaN or ±Infinity, duplicate keys, integers over 64 digits, nesting deeper than 64, a BOM and non-UTF-8 input. It also applies the reader rules:
  - at most 8 MiB;
  - under `claude_artifacts`;
  - `O_NOFOLLOW`;
  - a single link;
  - the fence's protected names.
- *What the wrapper does.* Its prelaunch `pin_doc` is plain `json.loads`, with no size cap and no root restriction.
- *TESTED.* `FINDING_RHO_RECORD_NAN_REFUSED_BY_STRICT_READER` refuses a NaN ρ record with `JSON_NONFINITE`.
- *Not reachable from honest producers.*
  - The S4RC1 record writer `encode_record` (s4rc1_common_c3v002 L285-287) encodes with `allow_nan=False`. So, per that file's docstring, does the custody writer (custody_cx2v002 L149) that `produce_rho`'s own `main` uses (`CU.write_new`, a1dcdea8 L379). This is FORMAL: custody_cx2v002 was not opened here.
  - The CP-1 runner's out-root is `claude_artifacts/s4rc1_c3/cp1_<name>` (CP1_RUN_SHEET_DRAFT_C3V002 L23).
  - A ρ record has 9 shells (`shell_plan(unit=False)`), so it is KB-scale.
  - A NaN ρ would also fail the wrapper's own acceptance step: `M.canonical`, `allow_nan=False`, L179.
- *Inherited from v003, unchanged by 0697.* The 8 MiB, root and single-link rules already applied to every slot file (v003 L808-809). The CP-1 runner notes "slot record: no 8 MiB rule" (cp1_runner_c3v002 L380). An honest EPS slot record over 8 MiB would therefore be refused by v003 and v004 alike, while the wrapper accepts it. The runner records `record_bytes` per EPS record, so root can check before the final run. This is FORMAL; the size of a real EPS record is not known here.

**N-4 (NOTE): documentation and names.**
- The retained v003 docstring, item 5 (L45-48), still describes "EPS and LO_ENVELOPE proofs ... LO covering all consumed states" and cites `24abe3bc`. The v004 prefix (L1-7) supersedes it.
- Manifest file names and schemas are still `..._C4V003`/`_V003`. For example, `FINAL_SPECS_MANIFEST_C4V003.json` carries schema `C4_STEP4_FINAL_SPECS_MANIFEST_V003`, while `tool` pins the v004 bytes.
- These are intended by "v003's bytes", but a binder must key on the tool sha, not the file name.

**N-5 (NOTE): the A70 provisional comparison is now vacuous for the anchor point.**
- Under Q5 the anchor point's lo slot must also be a ρ record. TESTED: `Q5_ANCHOR_LO_SLOT_STILL_THE_A70_LO_RECORD` refuses the v003-form A70 LO record.
- So the anchor's three specs (`TAIL_REANCHOR`, `WORKERS_8_CANDIDATE_ANCHOR`, `HEADLINE_TRIAL`) can no longer carry both A70 slots.
- The manifest flag `mapper_family_equals_provisional_when_a70` therefore holds over an empty set. It is informational only and refuses nothing.

**N-6 (NOTE, outside the 0697 scope; inherited).**
- *The mismatch.* `verify_final_adoption` mirrors adoption policy r7 `7c726fa2`, which admits both `PIN_ADDENDUM_V005` forms. Wrapper v002's core `dc895f8a` pins policy r10_c4 `93d9c0ac` instead. That policy requires the bare-sha form and `ADDENDUM_V005_CITED`.
- *Severity.* v004 is looser only. The honest sealed compare carries the bare sha (K1/K2), so no honest input is refused.

## 2. Test changes (task 2)

**Labels.**
- `PROD_NAME` is now `produce_final_step4_specs_c4v004.py`, and the module names are `c4v004_producer_phaseA/B`.
- The C1 notes text and the header now say v004.
- The results go to `run/TEST_RESULTS_C4V004.json` with schema `C4_STEP4_PRODUCER_V004_TESTS`.
- The record also carries the test file's own sha, the Python version (3.12.14), the reference pins and the v003 copy pin.

**Fixtures moved to wrapper v002.**
- The policy review uses `driver_slot_rule = P1.DRIVER_SLOT_RULE` and `guard_sha256 = P1.CERT_GUARD_SHA` (`9e3fc109`).
- `make_point` (the v004 form) writes:
  - a SYNTHETIC ρ record at every lo slot, the anchor included (the anchor's EPS slot stays the A70 EPS record);
  - an `LO_RHO_SLOT` proof with no `covers_all_consumed_states` key;
  - `custody_sha256 = digest(CUSTODY)` on both proofs;
  - the bundle with custody `CUSTODY` and prelaunch `{EPS, LO_RHO_SLOT}`.
- The ρ record has the key set of `produce_rho` and no ρ value. It includes `covers_all_consumed_states: false`, as the honest `base_record` writes it.
- The custody digest is computed by the test itself (core dc895f8a canonical form), not by the producer.
- The ρ schema and gate are the wrapper's literals, and a static check confirms they equal the producer's constants.

**The old form, kept for contrast.**
- `make_point_v003` is the v003 fixture, byte for byte.
- `OLD_REG` and `OLD_REVIEW` build the v003-form world.
- The v003 guard pin is read by AST from the v003 bytes, never executed.

**Cases.**
- Removed: `F1_LO_NOT_COVERING_ALL_STATES`.
- Unchanged: every other case, 166 in total.
- Placed in `run/tools/` for task 4: a byte copy of v003 `b7fb4d53`, checked by sha.

**New classes.**

- **V004-STATIC (3)**
  - AST confinement.
  - 18 wrapper and guard line anchors (L30, L40, L73, L74, L75, L148, L150, L163, L165, L168-171, guard sha and L13-14, the fixture literals, the producer sha).
  - The lo-slot rule holds by construction.
- **V004-Q5 (20, MUST_FAIL, final mode)**

  | Case | Expected refusal |
  |---|---|
  | old slot-rule string | `CERTIFICATE_POLICY_REVIEW_BINDING` (driver_slot_rule) |
  | guard v003 pin | `CERTIFICATE_POLICY_REVIEW_BINDING` (guard_sha256) |
  | proof carries `covers_all_consumed_states` (True; False) | `LO_RHO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES` |
  | lo slot differs from the registry `lo_certificate` (injected) | `LO_SLOT_NOT_THE_REGISTERED_RHO_RECORD` |
  | bundle and proof name another ρ record | `BUNDLE_DOES_NOT_BIND_THE_SLOTS` |
  | proof names another ρ record | `PROOF_DRIVER_CERTIFICATE_NOT_THE_SLOT` |
  | ρ schema, gate, point, settings, full search or coverage flipped, plus coverage = 1 | `LO_SLOT_NOT_THE_FULL_REGISTERED_RHO_RECORD` (7 cases) |
  | ρ custody differs; proof custody differs; ρ custody missing | `RHO_CUSTODY_NOT_THE_PROOF_CUSTODY` (3 cases) |
  | old `LO_ENVELOPE` bundle (the whole v003-form registry) | `PIN_REQUIRED` ("bundle LO_RHO_SLOT proof") |
  | old `LO_ENVELOPE` proof under the `LO_RHO_SLOT` key | `PROOF_SCHEMA_OR_GATE_MISMATCH` |
  | the anchor keeps the A70 LO record | `LO_SLOT_NOT_THE_FULL_REGISTERED_RHO_RECORD` |

  Where a typed code is shared, the case also requires the reason text.
- **V004-PARITY (4).** Forms wrapper v002 admits; v004 must reach its last gate:
  - the N3 near-miss key;
  - a leftover `LO_ENVELOPE` key (N4);
  - a ρ record carrying covers True;
  - ρ provenance fields.
- **V004-FINDING (2).** N-1 and N-3, observed from bytes.
- **V004-BITWISE (5).** Task 4.
- **V004-CONTRAST (3).**
  - v003 admits the v003-form world up to its last gate.
  - v003 refuses the v004-form world at `guard_sha256`.
  - v004 refuses the v003-form world at `guard_sha256`.

## 3. Counts (task 3)

**Record run.**
- Folder: `tests_rec01`.
- Started 2026-10-19T13:00:01Z; took 47.53 s; exit 0.
- Result: **203/203 passed, 0 failed**.
- `final_manifests_written_anywhere` is empty. There were 78 fence blocks, all in the deliberate cases and the 58 self-test blocks. The v003 copy's fence blocked nothing.

| Class | Passed | v003 record run |
|---|---|---|
| PR-SF1 | 77/77 | 78/78 (F1_LO_NOT_COVERING_ALL_STATES replaced) |
| PR-SF1/PR-SF2 | 1/1 | 1/1 |
| PR-SF2 | 19/19 | 19/19 |
| PR-SF3 | 28/28 | 28/28 |
| PR-SF5 | 17/17 | 17/17 |
| SF-R1 | 19/19 | 19/19 |
| build | 1/1 | 1/1 |
| v002 | 4/4 | 4/4 |
| V004-STATIC | 3/3 | new |
| V004-Q5 | 20/20 | new |
| V004-PARITY | 4/4 | new |
| V004-FINDING | 2/2 | new |
| V004-BITWISE | 5/5 | new |
| V004-CONTRAST | 3/3 | new |
| **Total** | **203/203** | 167/167 |

**Results files.**
- `tests_rec01/run/TEST_RESULTS_C4V004.json`, sha `d9346dc51672692b1cab9cb8e761bbf7a60365b40be863c0563a017e580d6b39`.
- `v004_work/TEST_RESULTS_C4V004.json` is a byte copy (same sha, `cmp` equal). It was created with an exclusive create (zsh noclobber, which opens with `O_EXCL`). The test cannot write it directly, because its Phase B fence allows writes only inside `run/`.

**Dev runs (kept, not deleted).**
- `tests_dev01`: 200/201. The one failure was the test's own count of injected `strict_pin` calls (it expected 2; the producer makes 3). The refusal code was correct. The expectation was then fixed.
- `tests_dev02`: 203/203. Same test bytes `74b57d7d` as the record run.

**Command.**
```
cd …/v004_work/tools && OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 taskpolicy -b /Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -I -B …/v004_work/tools/test_produce_final_step4_specs_c4v004.py rec01 "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## 4. The 29 spec byte strings are unchanged (task 4)

**Method.**
- One process ran both producers.
- v004 was the byte copy `fcbf1c3e` that the suite tests.
- v003 was the byte copy `b7fb4d53` in the same `run/tools/`, loaded after every other case had run. Its fence is a third copy of the same bytes, with REVIEW = `run/`.
- Both producers got the same inputs in five modes. In each mode all 29 specs were compared byte for byte, and both producers' 29 shas are recorded in the results JSON (`BW_*` → `v003_sha256`, `v004_sha256`).

| Mode | Inputs | Bitwise equal | Roster digest v003 = v004 |
|---|---|---|---|
| DRY_R9_INMEMORY | r9 config `721c7230`, dry note | 29/29 | `85900d591f0ce06f1934ca9ab88e5c0f6b6d2e0d772816f4c3c80f007434fed0` |
| PROVISIONAL_CLI_R9 (written) | r9 config, no registry, `main(['provisional', …])` | 29/29 | `211d5a7f5a0acd35a5063257286245deeb49d06c9816dfb89b6e132627c242e9` |
| PROVISIONAL_CLI_SWORLD_REGISTRY (written) | S_STRING C1 + the v004-form S-world registry | 29/29 | `86ec2711b540ba228dbe893084cc7fa03eb66d165a44cc09fdc8d180ff0df09e` |
| PROVISIONAL_W3_REGISTRY_INMEMORY | r9 config + the W3 A70 registry | 29/29 | `572bfb968fafcf10431c2a3159ca3b9f8fc905a17a80c1bd3f6ccef71c76a05e` |
| FINAL_CONSTRUCTION_SWORLD_INMEMORY | S_STRING C1 + S-world registry, FINAL note, never written | 29/29 | `dfbc67f283a714f6536662ee87bc5138a9eacb2b4b00947b5c5c3c3e1524e78d` |

**How to read the digests.**
- A roster digest is the sha256 of the canonical JSON `{case: sha256}` map.
- The DRY, R9 and W3 digests are the same in dev01, dev02 and rec01.
- The S-world digests depend on the run's fixture paths, which carry the run tag.

**Cross-check outside Python, from bytes.** In both written modes:
- `cmp` finds 29/29 files identical;
- the `shasum -a 256 *.json` lists are identical (list digests `2a333bbc…` for R9 and `5a18e2ce…` for the S-world).

**Agreement with the earlier records.** The existing cases R1, R2 and R3 also reproduce the V001 dry-plan and probe bytes 29/29 with v004. `S4_INMEMORY_FINAL_EQUALS_PROVISIONAL_EXCEPT_LABEL` gives 9/9 mapper specs and 20/20 hand specs.

**The 29 shas, identical for v003 and v004.**

| Case | DRY_R9_INMEMORY | PROVISIONAL_CLI_R9 |
|---|---|---|
| HEADLINE_CORNER_000 | f3c72d953ad21659cb2d4382a9d19994770fd720f183e34dabdcc3bc0dbc0dd4 | f3c72d953ad21659cb2d4382a9d19994770fd720f183e34dabdcc3bc0dbc0dd4 |
| HEADLINE_CORNER_001 | 850c8e22d594d20ca3f42e965d5dcd9136b1bde1e25a70f5768045b89d7e4fdb | 850c8e22d594d20ca3f42e965d5dcd9136b1bde1e25a70f5768045b89d7e4fdb |
| HEADLINE_CORNER_010 | 77c54de5f07d0f47c279d63bded14d704c583fb14d2d9e68269bb4cac55f162a | 77c54de5f07d0f47c279d63bded14d704c583fb14d2d9e68269bb4cac55f162a |
| HEADLINE_CORNER_011 | 4c8bb2bc1a6fa07baf2be6d981bb3f04ae61d781773cfd3d4bd5cd84c524f1f5 | 4c8bb2bc1a6fa07baf2be6d981bb3f04ae61d781773cfd3d4bd5cd84c524f1f5 |
| HEADLINE_CORNER_100 | 28011f300e5fbdb357af2882da2ba145919770b5583f9804ab4cc16ebf581f90 | 28011f300e5fbdb357af2882da2ba145919770b5583f9804ab4cc16ebf581f90 |
| HEADLINE_CORNER_101 | 478ae40fe70ebd3b869f779e72193adb6934e5ef4fdac473935e2b05bbbc8cf7 | 478ae40fe70ebd3b869f779e72193adb6934e5ef4fdac473935e2b05bbbc8cf7 |
| HEADLINE_CORNER_110 | ef8b7d4cd46f50c981b606fa4594271a9c50452d39c7a4c427a28233645138db | ef8b7d4cd46f50c981b606fa4594271a9c50452d39c7a4c427a28233645138db |
| HEADLINE_CORNER_111 | 36e0ffdbdb90cbb522118439b7a1547e2ea8a26092b5bed22bfd9b14f062f27a | 36e0ffdbdb90cbb522118439b7a1547e2ea8a26092b5bed22bfd9b14f062f27a |
| HEADLINE_TRIAL | c5ede3c761338e02ae94f80fb6c6f6851f5233e7a688038aa11a497ad2c49638 | c5ede3c761338e02ae94f80fb6c6f6851f5233e7a688038aa11a497ad2c49638 |
| SENS_CORNER_C000_DHI | aefd2f8d20418803d1276c5f03b125435220c4877011dfccfbc80f24e72e9810 | 965eb6bb2ea996b7bdbe295e5c413d7b67bd937a204d95ff51e91a3caa1a7c5c |
| SENS_CORNER_C000_DLO | 9202dbd70293b2b1f2dd30664733d6742ec245f6ad1f924aa072ad6d474b9fd9 | 95cd52242034360f86c1b76c0400e325919f5a5859e52f29c976cbb9fa14ca45 |
| SENS_CORNER_C001_DHI | fc4d321fe62f90e97846b7dc63a1cfa8e078df6c7790866e488e83801df55e20 | 94d4b913d2d7ea313a59df99e396c671d70cf16eb904bf7d05d88369afc0308b |
| SENS_CORNER_C001_DLO | e5600f4b1ce036652cab4f68ba4059c73a64e1154a5c59249a86d56b4ee7bb9d | d928f6aa87dac5c5af6455ecee5fa7c0348d9832657d896e7510ace63873bb6d |
| SENS_CORNER_C010_DHI | e06b845f383f8265c43388c2353c0ba68c9266c6ad9986475d31cb129e617173 | 4164a2b976cc6c29c05824988c19401649d010bd9bb3f6874bcdba10e8f50b40 |
| SENS_CORNER_C010_DLO | 5f6f5d00090095dd55b03789bfeb16cf02601079dac138c4c6b73815ea585f90 | d117cdb3ee990662f1780eee1722c0aa72c62cd004360ddeead5d77916b57926 |
| SENS_CORNER_C011_DHI | e6a3e5ea53ba34b1b0e42831094acd8e936324107cde4956e3860f02bcffdb57 | da99a3b6129fadca3c1ef1f1d75014fdd8fbcbfc6a3895c9fd404064e20ce2b7 |
| SENS_CORNER_C011_DLO | a17dce28118f31905abf5132b2ec333de1f2051894d2531c96e90e280efdf03c | 79b1ac360add101362fc7d393afd5bf69684405a233e16a9d03a7b33bcfddd05 |
| SENS_CORNER_C100_DHI | 4ae5c8c7287747c0447c7e9898eb2f0d36bdb9b90a07eae1c4801ced7d6cd974 | 23a9c8c9ab9fe0d36cca032d988f6ac1e7e0ded3200526a71f89acb4f4e13149 |
| SENS_CORNER_C100_DLO | a8115a4409e8c1caf37003c547a35af7f956858c688b2be24c7b81104e4f566d | 8548cf99481643e6e54b714c5f3a8b4169a21a609f96fcf049c8dc40d338b4d2 |
| SENS_CORNER_C101_DHI | 97545b83bb1b4a2e2c434c4fdcf373724380357986c37d953f9f667f42a0749c | aa9bfca5f0915aa4b9b7e86a2f09379792d532935fab39d746633fba3dd28050 |
| SENS_CORNER_C101_DLO | 36c04ad025268149f6ff0056308da0a9a720e9d9767a704506bdf63d80118aab | 0f3e8ff8d49277061e34f18fb5c83425e8be77ce091af5ccf75e19163e00bec2 |
| SENS_CORNER_C110_DHI | 348928f24215e08ff4e7187a2654b7638bb8213bacb235e02caf2e714cd1a4f4 | 072fa92d58cf47ec2163668193b5fa1d5eb639537171375202bff7c1e7902864 |
| SENS_CORNER_C110_DLO | 6b7f30f18dffa569122d5fbfc7c019076b7cd133cf716c5e87a0ddcaf6d26870 | 37b420bf0ded3dd261928deff02a123b59cdabef349ef534d12339ccd2222908 |
| SENS_CORNER_C111_DHI | 1b3fde18a7d3ec13b0aa556c64110a843deb0a2e4471ab892d947066ed7a9527 | 3ba28fe5f867698446bc6b9d6a0baf88f239073185a97d047392212b489de79f |
| SENS_CORNER_C111_DLO | 338184cb84e3ee0464597b0e880d0840640a8d197560e5dfec8ffc0db4e23b63 | d3edc8c9d719907dfb21fa4faa9bfd5ecb6c69cd0f1f4acfff09eafaf773ef6e |
| SENS_DISTANCE_LOWER | e020397cbf7b5d54de9cba0f98adf4d5a18a5944bcae3d02f18a69dec7ecd760 | 707568ece214df5b92c1650532d728561987c667f036534aa659f6b6f89a68f3 |
| SENS_DISTANCE_UPPER | 49bce3b5cf7b7124f85cc95fec00aa8f08126a36b24b5d09f44a492bbc6c5ff9 | 79cbe35073f5d7e13326f03a32c02faf4e0f7a16372ce53e1d84518577fcff81 |
| TAIL_REANCHOR | 5fc6f0bdcbe5c58c371f77e886facfc6610ae10c5018a544aa0b67c6facd58e3 | 7eb3de24a9b76b20660870677ec3070e6bdb09eb6fdacfd2ddbbda56a6584381 |
| WORKERS_8_CANDIDATE_ANCHOR | 686ad07f4cfa81563136b485f7852a815e3056cd9c6f3cbd79e88b944b762e96 | 90fe7286aed875a571338ee00d3f71cc639de46460b72ab9d83baa5a9549c431 |

The hand-built specs differ between the two columns only by the label note (dry versus provisional mode). The 9 mapper specs carry no note and are equal across the two modes. The existing case `S5_PROVISIONAL_MODE_R9_EQUALS_DRY` tests this: 9/9 mapper specs and 20/20 hand specs are equal once the label is removed.

## Rules followed

- **Reads.** No NGC3198, target or velocity file was opened, and no runs_ext, C5H, `UVT_*`, UNT_INTERNAL_RUNS or CLAUDE2/runs path. There was no recursive search; only named files were read and single folders listed.
- **Python.** Only the test file ran, three times (dev01, dev02, rec01), with the four thread variables, `taskpolicy -b` and the codex runtime `python3 -I -B`. The test loads the producer first.
- **Writes.** Every write is inside `v004_work`:
  - the test folders `tests_dev01`, `tests_dev02` and `tests_rec01`;
  - `TEST_RESULTS_C4V004.json`;
  - this file;
  - appends to `PARTIAL.md`;
  - edits to the one permitted test file.

  Every new file was created exclusively, and nothing was deleted or moved.
- **Producer.** The v004 file is unchanged (`fcbf1c3e` before and after).

## Labels

- **TESTED (from bytes, in the fenced process or by `cmp` and `shasum`):** the counts; the 29/29 bitwise result in five modes; every check listed under V004-STATIC, V004-Q5, V004-PARITY, V004-FINDING and V004-CONTRAST.
- **FORMAL (read from source, not executed):**
  - the wrapper-side outcomes (the wrapper was not run);
  - the honest-producer reachability arguments in N-1 and N-3;
  - the custody equality argument;
  - the inherited v003 items.
- **UNTESTED:** real ρ, EPS or registry records (none exist yet); root's PRELAUNCH on these producer outputs.
