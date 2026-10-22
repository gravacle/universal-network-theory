# NGC per-state LO adapter, enumerator and handoff, c2v001 (root build; V006 A153)

**Status.** Root build (Claude2 workflow), synthetic tests only. Nothing here is adopted until root rules on it and a distinct lane reviews it. No NGC per-state number exists, and none was computed.

**Spec of record.**
- V006 A153. The adapter pins the A153 *section*, not the whole file, because root keeps appending to V006. Section sha from bytes: `aa079db7cc07c2973075514a5d359ff3941b69f414687f12827cc06dab94c51e`. File sha at first read was `f1c5f657`; it was `b7e0ae2b` at README time, after A154 to A157 were appended. The A153 section is unchanged.
- Text of record `CLAUDE2/NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md` (`9916cb6f`), section 6: S1, S3 to S11 and S13. S2 is built as an interface.

## A153 scope disclosure (verbatim, V006 line 1091)

> - **Scope disclosure, required on every NGC LO record.** The indicator acts on route A's readout channel. It **does not bound** the omitted tail's contribution to the 43 route-B rows through the source: that contribution is UNTESTED, and its deciding test is the 10-component tail successor as a companion call. A PASS certifies the indicator only.

How the code enforces it:
- Every per-state record, call record and root summary carries this text, without the list marker, as `scope_disclosure`.
- At every run the adapter checks that the text appears verbatim in the A153 section bytes.
- `guard_state_record` refuses any record that lacks it. The handoff re-reads each record and refuses one without it.
- A FAIL record also carries the text of record's section 3 FAIL text, checked verbatim against `9916cb6f`.

## Files (sha256 from bytes)

| file | sha256 | role |
|---|---|---|
| `ngc_consumed_states_c2v001.py` | `607b7f667dfa1612da3fd874ab2656dc5ca487285a28afb2e4b1bfe979bd3125` | S9 enumerator and the Q5 class map |
| `ngc_lo_state_adapter_c2v001.py` | `6e004a5fa963275b1e52cf5990ad600127ee26f565cfca8ea7ed44da5a185ff5` | S1, S3 to S8, S10, S12, S13; S2 interface. Pins the enumerator `607b7f66`. |
| `ngc_acceptance_handoff_c2v001.py` | `2ed50410d0ae3963623812a73090f8083d9392ffb155bb50ea2631f549b5e8b1` | S11. Route `NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE`. Pins adapter `6e004a5f` and enumerator `607b7f66`. |
| `test_ngc_acceptance_c2v001.py` | `a5d65963ae6437475c553ddeed5d54ab14c71af1c5a58104563ed76270dfa373` | synthetic suite: 22 MUST_PASS, 25 MUST_FAIL |
| `mutation_ngc_acceptance_c2v001.py` | `34eb8bb05026ef345ee0f70e45d3d94eb92af150b4ad9c19e982abf77bdc8078` | mutation harness: 25 mutants plus a control |

Other pins:
- Tail library v002 `2026f2b6`, the one the driver pins, for the TailState digest and `_c0_D`.
- Driver cx3r008 `577f8c94`, S0 `1be5ed70`, launch pin `LO_NGC_K32_CERT_V001` `07745bbf`. The launch pin is hash-checked only; it is never parsed.
- Manifest `a2936517`, read-only, for the radii and order cross-check.

## t_i, and the A155 supersession

**As commissioned:** t_i is a pinned row-contract field (`t_km_s`) with a `t_rule_id` that must equal the root entry pinned in the module.
- `T_I_ENTRY = None`. Every NGC state therefore reads UNAVAILABLE `NGC_LO_TOLERANCE_NOT_DECLARED`, and every call reads INCOMPLETE. That is UNTESTED, not a null.
- The gate runs before anything numeric. No speed is read, no B1 is rebuilt and no rho is recomputed (freeze before pin).
- Tests P16 and P18 prove this on the public entries with the REGISTERED registry.

**A155 (frozen 17:57:08Z, after this build was commissioned) supersedes the stored-t_i design.** It declares rule `TI_B_SCALE_R_V001` in ratio form:

g_s = max_i (|v_i|·1e3)² · R_i · ρ_s · B1_s / (2 c² θ)

A155 says that if the current build used a stored t_i, a successor replaces it. The c2v002 delta:
1. Pin `T_I_ENTRY = {V006, '## A155', ed6b144b66837069c4febf81a4feaf11c160f9be5f26d914d4c40041b60f3c9d}`. That is the A155 section sha from bytes now. It changes if root adds an erratum.
2. Amend the row contract. Drop `t_km_s`. Add θ's float.hex (expected `0x1.ce9660bc22098p-29`, the certsngc_common_c2v002 L45 constant) and c's float.hex. Rule id `TI_B_SCALE_R_V001`.
3. Evaluate the ratio form in `aggregate`. Thresholds and S4 are unchanged.
4. Add the A155 edge cases: |v_i| = 0 contributes 0 with flag `ZERO_SPEED_ROW`; an empty row set reads `LO_ROW_SET_EMPTY`; θ or c bits that differ from the contract read `NGC_LO_TOLERANCE_RULE_MISMATCH`.
5. Drop the per-row missing-t path.
6. Carry the E_A155_1 PASS meaning text.
7. Add the MUST_FAIL additions from A155's text of record (`NGC_LO_TI_RECOMMENDATION_WF_8FDF0C2E.md` `cce91ae0` §3). This build has not read that file.

S1 to S10 and S12 carry over unchanged.

## How each spec item is built

| item | where | notes |
|---|---|---|
| S1 point custody | `point_custody` | Inputs: driver + S0 θ key + spec sha. The θ key is recomputed from `theta_hex`. The spec's physical block is checked bitwise against the θ mapping (filler L294 order). The spec slot must be the launch pin, outer must be {cylinder, 32}, and `result.call_spec_sha256` must be the spec sha. |
| S2 ρ | `check_slot_proof`, `check_rho_record`, per-state `rho_recompute` | Interface on Claude3's schemas (`UNT_NGC_POINT_LO_SLOT_PROOF_C3V001`, `UNT_NGC_POINT_RHO_NUMERICAL_C3V001`). The proof producer and the ρ producer must be in root's approved lists. a1dcdea8 is refused as producer and as schema. A ρ_record pin equal to the launch pin is refused before any read. The recompute must equal the slot ρ under the 10-key canonical comparison. G4 is the proof's `bitwise_equal_10_key`. Single-thread BLAS is required. |
| S3 geometry, γ | `check_state_geometry`; C4b in `_one_state` | Checked on every state: kept {cube, 2.0}, outer {cylinder, 32}, edges[0] = 2, and the library's unit edges 2..47 (E_top = 47). C4b: the state's γ_eff, the spec route s·γ and the θ route s·ge·EB must share one bit pattern, else `NGC_GAMMA_ROUTE_BITS_DIFFER`. |
| S4 tiling | `aggregate` | hi ≤ E_top: exact tiling. lo < E_top < hi: (lo, E_top]. lo ≥ E_top: B1 = 0, r = 0, `NOT_IN_STATE_DOMAIN`. ρ_s is the full shell's registered `rho_used`. All 9 shells are kept and G sums all 9. A nonzero unit shell outside exactly one ρ shell, or above 91, reads `LO_SHELL_COVERAGE_INCOMPLETE`. |
| S5 B1 | `_one_state`, `recompute_b1` | The accepted state comes from the call's ROUTE_A_TAIL_MANIFEST arrays and record. Every other state comes from a rebuild export, admitted only if its TailState digest equals the recorded digest. Then lo_core L109-139 arithmetic: max(stored, recomputed), with the 1e-10 check. |
| S6 \|v_i\| | `own_call_readouts`, `decide` | The S6 table is implemented as written: X-row exclusion, X-row inclusion, MISSING with a lower bound, and the monotone-FAIL rule. The per-pass `invalid_rows == X` check and the per-pass row-list status are diagnostics only. |
| S7 R_i | `own_call_radii` | The final pass's column-mean `query_support[].radius_m`, bitwise equal to the contract. The contract is cross-checked against `a2936517`: ids and order exact, radii to 1e-12 relative. |
| S8 row contract | `check_row_contract` | Exact keys. Any key containing sigma, tau, err, v_obs, observed, velocity, speed or target is refused. |
| S9 inventory | `ngc_consumed_states_c2v001.enumerate_call`; `_inventory` | The adapter re-derives the classes from the occurrences and requires an exact match. |
| S10 review | `check_review` | Without a review: `ROW_REFERENCE_POLICY_NOT_REVIEWED`. |
| S11 handoff | `accept_call_ngc` | FINISHED receipt; accepted-state input from the manifest; adoption that re-reads and guards each record; readings recomputed and compared with the adapter's. `member_lo_ok` is true for ACCEPTED or LO_UNCERTIFIED_TRANSIENT (A152 W-3). The high-Q∞ flag is recorded. |
| S12 blinding | call record, `ROOT_SUMMARY.json`, CLI output | Verdicts, codes and coverage flags only. The values (v, d, ratios, G) are only in the per-state record files. The suite checks for no float outside `coverage_flags`. |
| S13 | tests F01 to F12 | One test per item on the minimum list (table below). |

Driver lines confirmed from bytes (cx3r008, for S6):
- The strict-clone passes are at L8915-8966, where rows are recorded only when `observe` holds (L8941: `len(cols) == 1 and (last or bound or observe_every_pass)`).
- The final rows are at L9037-9041.
- The scope wrapping is at L9183-9191 (the `_CX3R007_STRICT_BY_LINE` map) and L6544-6553 (`_ngc_scoped_callable_cx3r007`).
- `uvt_stage_records` is at L6657-6671, `route_a_record` at L8693 and the manifest `state_digest` at L8706.

## Tests

- **Record runs.** Two runs, each 22/22 MUST_PASS and 25/25 MUST_FAIL:
  - `synthetic/record_run_1/SUITE_RESULTS_C2V001.json` `eeb34128f23f536c3bffaa6ecb5357665ea32cb48b0652a7b40ced66f6403048`;
  - `synthetic/record_run_2/SUITE_RESULTS_C2V001.json` `36b43e9de32a0d28cd719dcd061858d2055a8eb4c9e8c4dca4b4c6943579d213`.
  - Both used `python3 -I -B`. Ids, ok flags and details are identical once the run-directory names are normalized. No ART patch applied.
- **Mutation check.** `synthetic/mutation_c2v001/MUTATION_RESULTS_C2V001.json` `61052c643844569842fc00656dc6cee40746e5a0d3b3bbcaf112d948e33e3e43`. The control is clean. 25/25 mutants were killed, and every one by its intended test. The mutants cover:
  - the t_i gate;
  - the S4 partial shell, and strict lo_core tiling;
  - the S6 X-row exclusion, an ignored missing pass list, and the monotone rule;
  - threshold 0.005 changed to 0.05;
  - C4b, unit edges, 10-key ρ, certificate-as-ρ, the contract token scan;
  - the anchor and scope guards, the TRANSIENT condition, the review gate;
  - two enumerator mutants and three handoff mutants;
  - the S7 radius check, B1 reproduction, the S5 digest, and single-thread BLAS.

S13 mapping (each must fail closed):

| S13 | test | result |
|---|---|---|
| ρ from a1dcdea8 | F01 (slot schema, proof producer, recompute) | `NGC_RHO_RECORD_MISMATCH` |
| the certificate parsed as a ρ record | F02 | refused before any read |
| the cylinder-64 partition assumed at outer 32 without S4 | F03 (unit edges to 91 at outer 32; outer 64) | `STATE_GEOMETRY_MISMATCH` |
| nonzero B1 above 91 | F04 (also a straddling unit shell) | `LO_SHELL_COVERAGE_INCOMPLETE` |
| outer ≠ 32, or kept ≠ {cube, 2.0} | F05, F24 | `STATE_GEOMETRY_MISMATCH` |
| γ bits differ | F06 (state 1 ulp; spec route vs θ route) | `NGC_GAMMA_ROUTE_BITS_DIFFER` |
| a row in X with a finite readout excluded | F07 (included; the state FAILs) | NON_LAPSE_TAIL_MATERIAL, not PASS |
| a missing pass row list read as PASS | F08 | `READOUT_NOT_RECORDED`, INCOMPLETE |
| σ or DDO τ in the row contract | F09 | `NGC_ROW_CONTRACT_MISMATCH` (token scan) |
| t_i absent | F10 (no t; a foreign rule id; no root entry) | `NGC_LO_TOLERANCE_NOT_DECLARED` |
| an anchor class emitted | F11 (guard ×3, handoff) | refused |
| a FAIL record without the scope text | F12 (guard ×3, writer, handoff adoption) | refused |

MUST_PASS cover:
- the S4 tiling cases: P02 (E_top 47) and P03 (E_top 64 and 91);
- the S6 |v_i| cases: P04 to P10;
- the readings ACCEPTED, NON_LAPSE_TAIL_MATERIAL, LO_UNCERTIFIED_TRANSIENT and INCOMPLETE: P11 to P15;
- the REGISTERED public entries at NOT_DECLARED: P16 and P18;
- handoff end to end: P17 and P19;
- recorded diagnostics: P20 to P22.

## Builder choices (disclosed; each is root's to overrule)

1. **ρ is recomputed for every consumed state** (the lo_core precedent), although it is state-independent according to the interface's FORMAL reading. On U4 cost, it may need a per-call scope.
2. **A NOT_OBSERVED pass reads as a missing row list** (S6 and U3 as written). If NGC calls observe only the final pass, every non-FAIL state reads `READOUT_NOT_RECORDED`. The per-pass status is recorded so that U3 can be decided.
3. **An X row with any missing pass reads MISSING**, with a lower bound or none, rather than excluded (A48).
4. **R_i for X rows** comes from the column-mean row's own `radius_m`, because `query_support` covers valid rows only.
5. **Manifest radius cross-check.** R_i = float(Rad_text) · `manifest_radius_scale` · KPC_M, to 1e-12 relative. The scale is a contract field because the call geometry may scale by distance (U-b3).
6. **Carried beyond S1-S13:**
   - the lo_core L250 I1-T PASS check;
   - `record.lo_certificate` equals the launch pin;
   - c = 299792458.0 and λ equals the spec value (lo_core L216);
   - the single-thread BLAS requirement for the ρ recompute;
   - the handoff CLI sets the six thread variables to 1 before numpy loads.
7. **Five custody codes added beyond A153's seven:** `NGC_POINT_CUSTODY_MISMATCH`, `NGC_ROW_CONTRACT_MISMATCH`, `NGC_STATE_INPUT_UNAVAILABLE`, `NGC_STATE_CLASS_UNAVAILABLE` and `NGC_LO_ADAPTER_NOT_ADMITTED`.
8. **Synthetic test path.** Arithmetic tests run the same functions as the record module under a `SYNTHETIC_TEST` registry. That registry declares a synthetic t_i entry and is refused at every registered input. The public entries take the REGISTERED registry only.

## Open interfaces (each reads UNAVAILABLE or INCOMPLETE until supplied)

1. **S2 ρ.** Claude3's `ngc_rho_c3v001` (producer `c8604b2d`, slot proof `45a757b3`) exists, but its verify was in progress at build time. Root supplies the approved slot-proof and ρ-producer shas, the slot proof pin and the ρ producer pin.
2. **Route-A pre-acceptance iterates.** These live in the route-A sidecar, whose format this build did not read. Root supplies a pinned list (`UNT_NGC_ROUTE_A_ITERATE_STATES_C2V001`) from an approved reader. Without it the inventory is incomplete.
3. **Post-run rebuild export** of each non-accepted state (S5; U4 timing), from an approved producer.
4. **The row contract and its S10 review.** Root builds and pins them, amended per A155 for c2v002.
5. **The A138 V01(b) execution facts** (fresh, not resumed, not retried) are not carried, because S1-S13 do not name them. The handoff requires the FINISHED receipt, and the finish record must be bound to the result.
6. **GQ and SRB-ROT** are outside this handoff, which covers LO acceptance only.

## Conduct and deviations

**Read, named paths only:**
- V006, the text of record, the c3v003 adapter, lo_core, `acceptance_handoff_c2v004` and the b1 enumerator.
- `values_writer_c2v002`, the tail library v002 and Claude3's ngc_rho folder (interface, producer, slot proof).
- Driver cx3r008, at the cited line ranges only.
- The column-mean stage source, by grep, for the `query_support` layout.

**Not opened:** no run tree, nothing under `~/.codex`, `c5h_hull_c2` or `UVT_*`, and no NGC3198 target, slots, sigma or observed-velocity file. The registered S0 record was never read.

**Two NGC3198-named files were opened, and only these two:**
- The V006 addendum.
- Manifest `a2936517`, as a structure-only listing: keys, 43 rows, row keys, schema, units, and an id prefix. No radius value was printed or used.

**Deviations:**
- **Dev in scratchpad.** Development iterations ran in the session scratchpad. The final files here were written by exclusive create from the last dev copy (identical shas).
- **Real files read by tests.** The public-entry tests read the real V006 A153 section and the text of record, both named in the brief.
- **Test synthetic call names the real driver.** Its fabricated result names the registered driver sha as a string.
- **HASHES.** It lists every file under this folder. That includes all synthetic run and mutant trees, about 45k entries.
