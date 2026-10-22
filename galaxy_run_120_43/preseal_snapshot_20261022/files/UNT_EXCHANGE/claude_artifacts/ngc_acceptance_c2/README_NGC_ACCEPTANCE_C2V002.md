# NGC per-state LO adapter and handoff, c2v002 (root build; V006 A153 + A155)

**Status.** Root build (Claude2 workflow), synthetic tests only. Nothing here is adopted until root rules on it and a distinct lane reviews it. No NGC per-state number exists, and none was computed.

**What c2v002 is.** The A155 "Builds" successor of c2v001. It closes the two blocking items raised against c2v001:
- **B1, fails open.** In c2v001, an empty row set read PASS and the handoff read ACCEPTED with `member_lo_ok` true.
- **B2, adoption.** c2v001 stored t_i as `t_km_s` with `t_rule_id`; A155 says a stored-t_i build is replaced.

c2v001 is not edited. Its files and its README stay as they were.

**Spec of record.**
- V006 A153, pinned by its section sha `aa079db7cc07c2973075514a5d359ff3941b69f414687f12827cc06dab94c51e`.
- V006 A155 (frozen as amended, closure 17:57:08Z), pinned by its section sha `ed6b144b66837069c4febf81a4feaf11c160f9be5f26d914d4c40041b60f3c9d`.
  - Both section shas were computed from bytes at build time and again after the record runs; both were unchanged.
  - The V006 file sha moved from `41fe5aa2` to `96489e9f` during the build, when root appended A160.
- Text of record `CLAUDE2/NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md` (`9916cb6f`), section 6: S1, S3 to S11 and S13. S2 is built as an interface.
- A155 text of record `CLAUDE2/NGC_LO_TI_RECOMMENDATION_WF_8FDF0C2E.md` (`cce91ae0`), section 3, for the MUST_FAIL additions. It is read only, never pinned in code.

## A153 scope disclosure (verbatim, V006 line 1091)

> - **Scope disclosure, required on every NGC LO record.** The indicator acts on route A's readout channel. It **does not bound** the omitted tail's contribution to the 43 route-B rows through the source: that contribution is UNTESTED, and its deciding test is the 10-component tail successor as a companion call. A PASS certifies the indicator only.

## E_A155_1 PASS meaning (verbatim, V006 A155)

> "at every consumed state, the route-A readout-channel indicator of the omitted tail is at most 0.5% per shell, and at most 5% summed, of the linearized velocity-response scale to a theta-sized change in dlnN/dlnR at row i, under the declared approximation R G' = 1."

How the code enforces both texts:
- **Carried on every record.** Every per-state record and every call record carries `scope_disclosure` (the A153 text, without the list marker) and `pass_meaning` (the quoted text above). The handoff's root summary carries both as well.
- **Checked against source bytes.** At every run the adapter checks the A153 text inside the A153 section bytes. It checks the PASS meaning, the rule id `TI_B_SCALE_R_V001` and the theta hex inside the pinned A155 section bytes. If any of them is missing, the call is refused: `NGC_LO_ADAPTER_NOT_ADMITTED`.
- **Guarded on read.** `guard_state_record` refuses a record that lacks either text, and the handoff re-reads and guards every record. The handoff also refuses a call record without the PASS meaning.
- **FAIL text.** A FAIL record also carries the section 3 FAIL text of the text of record, checked verbatim against `9916cb6f`.

## Files (sha256 from bytes)

| file | sha256 | role |
|---|---|---|
| `ngc_lo_state_adapter_c2v002.py` | `ce33b526c38490687744d6b9a4b383cb540c1af6a8da7d8d4f0298807ce43047` | S1, S3 to S8, S10, S12, S13 and the A155 rule; S2 as an interface. Pins the enumerator `607b7f66` and A155. |
| `ngc_acceptance_handoff_c2v002.py` | `ef3da6f556278872b266ce0d79fff17eed0254de0396487b2f1a0e1ed271b7d1` | S11. Route `NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE`. Pins adapter `ce33b526` and enumerator `607b7f66`. |
| `ngc_consumed_states_c2v001.py` (unchanged, c2v001 file) | `607b7f667dfa1612da3fd874ab2656dc5ca487285a28afb2e4b1bfe979bd3125` | S9 enumerator. A155 does not touch it, so no successor was made. |
| `test_ngc_acceptance_c2v002.py` | `ba96c828712688667a428424a2474e55ce65c186fc6aff5ab0c0f219bb249af6` | Synthetic suite: 24 MUST_PASS and 33 MUST_FAIL. |
| `mutation_ngc_acceptance_c2v002.py` | `b74f568f34d3472380ee2df73ed0ea6be057f9220faadb9679e0212ca3084da8` | Mutation harness: 43 mutants plus a control. |

Other pins are unchanged from c2v001:
- tail library v002 `2026f2b6`;
- driver cx3r008 `577f8c94`;
- S0 `1be5ed70`;
- launch pin `LO_NGC_K32_CERT_V001` `07745bbf` (hash-checked only, never parsed);
- manifest `a2936517` (read-only, for the radii and order cross-check).

## The c2v002 delta

| # | item (A155; c2v001 README delta plan) | where | built as |
|---|---|---|---|
| 1 | Pin the t_i entry | `T_I_ENTRY` | `{V006, '## A155', ed6b144b…}` (section sha from bytes). `root_gate` requires the rule id, the theta hex `0x1.ce9660bc22098p-29` and the PASS meaning to appear verbatim in the section. |
| 2 | Amend the row contract (S8) | `check_row_contract` | Schema `UNT_NGC_LO_ROW_CONTRACT_C2V002`. Exact keys: {schema, query_ids, manifest, manifest_radius_scale, R_m, rule_id, theta_hex, c_hex, binding}. `theta_hex` and `c_hex` must be canonical `float.hex` strings. The token scan also refuses `km_s`, `t_i`, `tolerance`, `eps` and `n_min`/`nmin` keys. A key outside the exact set (for example `t`, `N_min` or `per_shell_scale`) is refused: `NGC_ROW_CONTRACT_MISMATCH`. |
| 3 | Evaluate the ratio form | `aggregate` | `g = (v*1e3)**2 * R * rho * b1 / (2*c**2*theta)` per row and shell, then `g_s = max_i`, `G = Σ_s g_s`. `d = v*R*rho*b1/4` (the lo_core L165 numerator, km/s) is recorded beside it. The thresholds (0.005 per shell, 0.05 summed) and S4 are unchanged. θ is the module constant, which must equal the contract bits. c is the state record's `c_m_s`, which must equal the contract bits, which must equal the core C. |
| 4 | A155 edge cases | `aggregate`, `decide`, `_one_state`, `guard_state_record` | **\|v_i\| = 0:** exactly 0, no division by \|v\| anywhere. The per-state record lists `zero_speed_rows` with `diagnostic_flags: ['ZERO_SPEED_ROW']`.<br>**Empty row set** (no row INCLUDED or MISSING after S6): `aggregate` gives `G = None` and per-shell `max_g = None`, never 0.0. `decide` returns UNAVAILABLE `LO_ROW_SET_EMPTY` before any FAIL or PASS branch. A fallback refuses a PASS whenever `rows_in_arithmetic` is empty or G is not a number, and the guard refuses any PASS or FAIL record with an empty `rows_in_arithmetic`, no numeric G, or a rule id other than `TI_B_SCALE_R_V001`. **This closes B1.**<br>**θ or c bits differ:** UNAVAILABLE `NGC_LO_TOLERANCE_RULE_MISMATCH`, at the contract (θ, c) and per state (`c_m_s`). |
| 5 | Drop the per-row missing-t path | `decide`, `_adapt_call` | Done. No row carries a t, and `MONOTONE_CODES` is now `(READOUT_NOT_RECORDED,)`. **This closes B2:** no record, contract or row stores t_i, and the guard refuses any record with a `t_km_s` / `t_i` / `t_i_km_s` / … key. |
| 6 | Carry the E_A155_1 PASS meaning | records, guard, handoff | See above. |
| 7 | The A155 section 3 MUST_FAIL additions | F26 to F33 | See the table below. |

Schemas move to C2V002: the state record, the call record, the row contract, the row-policy review, the acceptance record and the root summary. The state-input, inventory and point identity/custody schemas are unchanged.

**Other A153 items (S1 to S10, S12).** These carry over from c2v001 unchanged.

## Tests

**Record runs.** Two runs, each 24/24 MUST_PASS and 33/33 MUST_FAIL, under `python3 -I -B` 3.12.14 with no ART patch:
- `synthetic_c2v002/record_run_1/SUITE_RESULTS_C2V002.json` `c3cbbac6038cceb9f400bb31ae715c8a812ebc288fb45c5d46fb813d294a126f`;
- `synthetic_c2v002/record_run_2/SUITE_RESULTS_C2V002.json` `d904707cb4e13f854a114bb47963555ca0fcb057e9837fdb85403053a2725eef`.

Ids, ok flags and details are identical once the run-directory names are normalized.

**Mutation check.** `synthetic_c2v002/mutation_c2v002/MUTATION_RESULTS_C2V002.json` `9c83835c701cc0ba6d834378093969ca4549c60f82e0306512997960e7cab1cb`. The control is clean. 43/43 mutants were killed, every one by its intended test.
- M01 to M25 are the c2v001 mutants, carried over. M06 is adapted because the missing-t path is gone. M01 is now killed by F10, which checks that nothing past the gate runs.
- M26 restores the c2v001 empty-row-set PASS (killed by F32).
- M27: the guard against a decided record with no arithmetic is off.
- M28 to M30: zero-speed rows dropped, the flag off, zero speed refused.
- M31 to M33: the θ and c bit checks off (contract θ, state c, contract c).
- M34 and M35: an N_min factor and a per-shell 1/k_s scale in g.
- M36: the km/s to m/s conversion dropped.
- M37: the A155 entry-text check off.
- M38 to M40: the PASS-meaning guard, the stored-t guard and the handoff PASS-meaning check off.
- M41: exact contract keys off.
- M42: T_I_ENTRY unpinned.
- M43: a foreign rule id accepted.

**Synthetic calibration.** Synthetic states are calibrated through the source scale (B1 is linear in it), so that state A's largest g is 0.001 under the ratio form. t_i is never computed for that.

**A153 S13 mapping** (each must fail closed). Carried from c2v001; codes are unchanged unless noted.

| S13 | test | result |
|---|---|---|
| ρ from a1dcdea8 | F01 | `NGC_RHO_RECORD_MISMATCH` |
| the certificate parsed as a ρ record | F02 | refused before any read |
| the cylinder-64 partition assumed at outer 32 without S4 | F03 | `STATE_GEOMETRY_MISMATCH` |
| nonzero B1 above 91 | F04 | `LO_SHELL_COVERAGE_INCOMPLETE` |
| outer ≠ 32, or kept ≠ {cube, 2.0} | F05, F24 | `STATE_GEOMETRY_MISMATCH` |
| γ bits differ | F06 | `NGC_GAMMA_ROUTE_BITS_DIFFER` |
| a row in X with a finite readout excluded | F07 | included; the state FAILs |
| a missing pass row list read as PASS | F08 | `READOUT_NOT_RECORDED` |
| σ or DDO τ in the row contract | F09 | `NGC_ROW_CONTRACT_MISMATCH` |
| t_i absent | F10: contract without the rule; a foreign rule id; no root entry (and nothing past the gate runs); an entry whose bytes lack the rule | `NGC_LO_TOLERANCE_NOT_DECLARED`; the last case `NGC_LO_ADAPTER_NOT_ADMITTED` |
| an anchor class emitted | F11 | refused |
| a FAIL record without the scope text | F12: also without the PASS meaning, and a call record without it at the handoff | refused |

**A155 section 3 MUST_FAIL additions.**

| A155 §3 | test | result |
|---|---|---|
| t_i values or any velocity in the contract | F26: `t_km_s`; `t_km_s = [None]*43` with all rows excluded (X01a); `v_reference_km_s`; the c2v001 contract shape; a `t` key; a record storing `t_km_s` | `NGC_ROW_CONTRACT_MISMATCH`; the record is refused |
| θ or c bits that differ from the contract | F27: contract θ +1 ulp; contract c +1 ulp; state `c_m_s` +1 ulp; a non-canonical hex; partial rule keys | `NGC_LO_TOLERANCE_RULE_MISMATCH`; the format cases `NGC_ROW_CONTRACT_MISMATCH` |
| an N_min factor present | F28: an `N_min` field; g equals an independent oracle | refused; no factor |
| a per-shell 1/k_s scale | F29: a `per_shell_scale` field; per-shell g equals the oracle in every state | refused; no scale |
| eps_km_s used as t_i | F30: an `eps_km_s` field; `eps_km_s` on every result row, never read | refused; g equals the oracle |
| \|v_i\| = 0 raising an error or producing a non-finite value | F31: 5 rows at 0.0 / -0.0; pure aggregate with every v = 0 | PASS, g exactly 0.0, `ZERO_SPEED_ROW` |
| an empty row set reading PASS | F32: all 43 rows in X with authorized reasons; the handoff (X01b); pure aggregate; no rows at all; the guard ×3 | `LO_ROW_SET_EMPTY`; handoff INCOMPLETE, `member_lo_ok` false; refused |
| a large R·ρ·B1 that does not FAIL | F33: state A ×1e6; pure aggregate with R = 1e21 m | FAIL / NON_LAPSE_TAIL_MATERIAL |

**MUST_PASS.** These carry over from c2v001:
- the S4 tiling cases P02 and P03;
- the S6 |v_i| cases P04 to P10;
- the readings P11 to P15;
- handoff end to end, P17 and P19;
- recorded diagnostics, P20 to P22.

These are new or changed in c2v002:
- **P16 and P18, the public entries on the REGISTERED registry.** The root gate passes on the real A153 and A155 sections, and `t_rule_id` reads `TI_B_SCALE_R_V001`. The fabricated call's label has no theta key, so S1 refuses it: every state reads `NGC_POINT_CUSTODY_MISMATCH` and the call reads INCOMPLETE. Nothing numeric runs, and no registered S0 point, manifest row or ρ is read.
- **P23.** Every per-row g equals an independent oracle at every row, shell and state, and d / g = c²θ/(2·10⁶·|v|). That is the A155 identity; the value is computed in the test only.
- **P24.** g grows exactly as |v|², so doubling v gives exactly 4×.

**Reproduction of B1 on c2v001.** This ran on a scratch copy, outside this folder. With all 43 rows in X, c2v001 reads PASS at every state, and its handoff reads ACCEPTED with `member_lo_ok` true. With the same fixture, c2v002 reads `LO_ROW_SET_EMPTY` at every state, and the handoff reads INCOMPLETE (F32).

## Builder choices (disclosed; each is root's to overrule)

1. **Codes for a contract that is not bound to the rule.** If the rule keys are absent as a group, or the rule id is another rule's, the contract reads `NGC_LO_TOLERANCE_NOT_DECLARED`, the A153 S13 "t_i absent" reading. Only θ or c bits that differ read `NGC_LO_TOLERANCE_RULE_MISMATCH`. Partial rule keys and non-canonical hex read `NGC_ROW_CONTRACT_MISMATCH`.
2. **θ is a module constant.** It is the A155 hex, checked verbatim against the A155 section bytes, and the contract's θ must equal it bit for bit. certsngc_common_c2v002 was not opened, because it is not a named path. A155 and E_A155_1 item 7 record the hex from bytes.
3. **The contract's c must equal the core C** (299792458.0; text of record: "must equal the core's C"). The state `c_m_s` must equal the contract c bits. The c2v001 lo_core L216 check stays after it and is now redundant for c.
4. **Arithmetic order.** g is evaluated as `(v*1e3)**2 * R * rho * b1 / (2*c**2*theta)`, left to right in numpy float64. The oracle's test tolerance is 1e-12 relative. In record run 1's P23 call, all 1,161 row-shell values were bit-equal to the oracle.
5. **d is still recorded** beside g in the per-state records (S12 value files). Together with v, d and g let t_i be derived inside those files. That is the same blinding class as v itself, and no t_i field is written. Root reads only verdicts, codes and coverage flags.
6. **Empty-row-set precedence.** Coverage comes first, then `LO_ROW_SET_EMPTY`, then FAIL, then `READOUT_NOT_RECORDED`, then PASS. Per-state custody failures (geometry, ρ, rule bits) come before all of these.
7. **The enumerator is not re-versioned.** It is the c2v001 file at `607b7f66`, because A155 does not touch S9.
8. Choices 1 to 8 of the c2v001 README carry over. Choice 7 there now lists two more A155 codes, which are codes of record and not additions.

## Open interfaces and UNTESTED items

**Open interfaces.** These are unchanged from c2v001, and each reads UNAVAILABLE or INCOMPLETE until supplied:
- S2 ρ: the approved slot-proof and ρ-producer shas;
- the route-A iterate list;
- the post-run rebuild export;
- the amended row contract and its S10 review, which root builds, freezes and pins before the first NGC acceptance (A155).

**UNTESTED, with deciding tests:**
- **U-b1, the NGC LO size.** Deciding test: the first NGC acceptance.
- **U-b2, the R·G′ = 1 remainder.** It is declared, not bounded (E_A155_1).
- **U-b3, whether S7's call radii equal `a2936517` bit for bit.** A155 assigns this comparison to "the builder", on one existing call's query support. It was **not run here**, because it needs a call's run tree, which this build is barred from opening. It stays UNTESTED. Deciding test: that comparison, by a lane allowed to read a call's column-mean output.
- **U1, the omitted tail through the source.** Deciding test: the 10-component successor.

## Conduct and deviations

**Read, by named path only:**
- V006 (the A153, A155 and A159 headings, and the A153-A159 text; A160's heading only);
- the A155 text of record `cce91ae0`, section 3, named by A155;
- the c2v001 files in this folder;
- lo_core `12d36305` L140-178, via the c3v003 adapter's `LO_CORE` constant.

**Not opened:**
- no run tree, nothing under `~/.codex`, `c5h_hull_c2` or `UVT_*`;
- no NGC3198 target, slots, sigma or observed-velocity file;
- manifest `a2936517` was not opened in this build (c2v002 reads it only at run time, inside the contract check that the synthetic tests replace).

**Deviations:**
- **Dev in scratchpad.** Development ran in the session scratchpad. The final files were written here by exclusive create from the last dev copies, with identical shas.
- **Real files read by tests.** The public-entry tests read the real V006 A153 and A155 sections and the text of record.
- **Test call names the real driver.** The test's fabricated result names the registered driver sha as a string.
- **Scratch reproduction.** The B1 reproduction on c2v001 used a scratch copy of the c2v001 modules. The originals were not modified.
- **Recomputing θ.** A naive recomputation of θ, `log1p((5/3)·11000²/(2/3)/c²)` in this operation order, gives `0x1.ce9660bc2209ap-29`, 2 ulp from the pinned `…098p-29`. It is not used. The pin is the A155 hex of record, whose producer chain Codex1 0150 item 7 verified. This is recorded only as a note.
- **HASHES_V002.txt.** It lists every c2v002 file in this folder, including the full `synthetic_c2v002/` tree, plus the unchanged enumerator. It excludes itself and the c2v001 files.
