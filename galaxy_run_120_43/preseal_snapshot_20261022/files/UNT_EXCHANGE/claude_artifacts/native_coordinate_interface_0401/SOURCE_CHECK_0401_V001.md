# Source check: 0401 native coordinate interface crosswalk (V001)

- Role: distinct checker, not author. I did not write the crosswalk or any of the sources.
- **Verdict: CONFIRMED.** There are no errata. Four notes follow that require no change.
- Target: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/NATIVE_COORDINATE_INTERFACE_CROSSWALK_0401_V001.md` SHA256 `d0a45f1c2768134e27421c5b35abe6ddfd2c45e0dfe21af2bfa3669f3eb3a422`
- Task: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0401_2026-10-15_native_coordinate_interface_crosswalk.md` SHA256 `2cc708dbe42c3a27c887d5ecc02f415219c2c82314e51d6f309e92a0fffc68b8`
- Method:
  - Manual reading and manual algebra only.
  - No code, no numerical execution, no network access and no project or Codex script.
  - Nothing was written under `/Users/bgm/Research/Universal Network Theory`.
- C178 read scope:
  - Read: l.453–657 (operator_coordinate_accounting, current_uniform_energy_coordinates, derived_combination_register, raw_category_register_role, unresolved_count_owners).
  - Read: the top-level key `required_shared_fitted_coordinate_count` (l.209; the jq path is the top-level `["required_shared_fitted_coordinate_count"]` and its value is null) and `kind` (l.2), both located with grep/jq.
  - Shown as context in the same read but not used: l.440–452, which include a supersedes_status path.
  - Not opened: any linked file, whether legacy ledger, target, derived-combination source or reading pin.
- No primitive owner definition was opened. None was needed, because the sources give the off-diagonal owners at matrix-element/support level and the crosswalk transcribes them at that level.

## Hashes (recomputed from bytes by this checker)

| Id | Path | SHA256 | Pin match |
|---|---|---|---|
| target | `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/native_coordinate_interface_0401/NATIVE_COORDINATE_INTERFACE_CROSSWALK_0401_V001.md` | `d0a45f1c2768134e27421c5b35abe6ddfd2c45e0dfe21af2bfa3669f3eb3a422` | yes (author report) |
| 0401 | `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0401_2026-10-15_native_coordinate_interface_crosswalk.md` | `2cc708dbe42c3a27c887d5ecc02f415219c2c82314e51d6f309e92a0fffc68b8` | yes |
| S1 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_UNIFORM_RESOURCE_SECTOR_EXACT_DIAGONAL_COORDINATES_PROPOSED_V001.md` | `33a4f1adfa74986e510630f15dc30551fbbe78e05497cc954e9eec5a5753c3f6` | yes |
| R1 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/OWNED_UNIFORM_RESOURCE_DIAGONAL_COORDINATES_DISTINCT_REVIEW_V001.md` | `1a82af99a201b83d10bcd5d5a7bbbbc7ddbd1db6b526a26716e8d24dc8585f6c` | yes |
| S2 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_UNIFORM_DIAGONAL_SEVEN_COORDINATE_OPERATOR_RANK_PROPOSED_V001.md` | `604cc21f716623786f7db3c9083d47c7299882befd3b76cff1dfa974c3745398` | yes |
| R2 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_DIAGONAL_SEVEN_COORDINATE_RANK_DISTINCT_REVIEW_V001.md` | `9406114b0ca787b1e8f89257afb94a0211d4b84d7c4a55618c73ab1935d26372` | yes |
| S3 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_FIXED_PROFILE_OFFDIAGONAL_INDEPENDENCE_AND_TWELVE_COORDINATES_PROPOSED_V001.md` | `66d71e9c0a53b498b5e105796fc52656fcc7b7917d5ca88789f25018605645db` | yes |
| R3 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_FIXED_PROFILE_TWELVE_COORDINATES_DISTINCT_REVIEW_V001.md` | `f7da66721f8ba845adf4c4e9a333c9d6c672254da1b0304135f0ee39e6b479a0` | yes |
| C178 | `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/READINESS_C178_SHARED_CALIBRATION_EXTENSION_V002.json` | `122c26bd59b92014ace41bf2822cd7bc2100d91a5fd428820a7f2f9cf2b98ebb` | yes |

The C178 byte pins for S2, R2, S3 and R3 (C178 l.465, 470, 475, 480: 7814, 2593, 8560 and 2274) also match the byte counts on disk.

## Per-row results

All twelve rows PASS: the operator, sign, factors, support and sector match the sources.

1. **Ud: PASS.**
   - S1 l.26: "C I + Ud sum_i s_i^2 + mu0 sum_i s_i".
   - S2 l.10: "D=sum_i(d_i−2)^2".
   - The sum runs over all V graph vertices, consistent with S1 l.24: "sum_e n_e=V+sum_i s_i/2".
   - C178 l.486: "coordinate": "Ud".
2. **mu0: PASS.**
   - S1 l.26 (as above).
   - S2 l.10: "S=sum_i(d_i−2)".
   - S1 l.32: "mu0 = Delta/2 + 2Ud(2-dstar)".
   - C178 l.497.
3. **lambdaJ: PASS.**
   - S1 l.27: "lambdaJ sum_i s_i p_i".
   - S2 l.11: "P_s=sum_i(d_i−2)p_i".
   - C178 l.508: "lambda_J".
4. **lambdaR: PASS.**
   - S1 l.27: "- lambdaR sum_i s_i q_i".
   - S2 l.9: "− lambdaR Q_s".
   - The operator is −Q_s and the sign is −.
   - C178 l.519: "lambda_R".
5. **r: PASS.**
   - S1 l.28: "+ r sum_i q_i".
   - S2 l.12: "Q_q=sum_i q_i".
   - S1 l.33: "r = epsr - 2lambdaR".
   - C178 l.530.
6. **delta_cell: PASS.**
   - S1 l.28: "delta_cell Sg".
   - S2 l.12: "S_g=sum_i Spent_i".
   - S1 l.13: "The first identity is GLOBAL. Neither p_i=S_i nor local Q_i=1 follows."
   - R1 l.5: "gives Nc=Sg, not p_i=S_i. Thus the arbitrary local Q_i=0/2 pairs remain."
   - C178 l.541.
   - See note N1.
7. **nu: PASS, and the relative term is retained.**
   - S1 l.28: "+ nu N".
   - S1 l.44: "nu multiplies a nonconserved count and is a genuine relative diagonal contact in the model".
   - R1 l.9: "N varies under Birth, so per-level subtraction would alter the generator".
   - S2 l.40: "a global reference shift is not permission to subtract different constants at each N".
   - C178 l.552.
8. **h: PASS at matrix-element/support level.**
   - S3 l.15: "two states differing only in one edge bit. Their matrix element is −h".
   - R3 l.5: "edge-only flip -h".
   - S2 l.44: "an incidence flip changes one edge bit".
   - C178 l.563.
9. **t: PASS at matrix-element/support level.**
   - S3 l.18: "The matrix element is −t times its fixed nonzero oriented edge phase".
   - S3 l.18: "The final local Q values are2 and0 ... the exit is in the full eight-state sector".
   - R3 l.5: "must not be excluded by a local-Q=1 truncation".
   - S2 l.44: "hopping changes two endpoint carriers at fixed cells/incidence".
   - The author's direction, T(p_i,p_j: 0,1→1,0) with the carrier moving j→i, matches the S3 witness (i Ready/p0, j Spent/p1 → i Ready/p1, j Spent/p0).
   - The relation between the reverse-orientation phase and the forward one, and any exchange signs, are not stated in S1–S3 or R1–R3. The author leaves them open (ambiguity 1), which is the correct transcription.
   - C178 l.574.
10. **g: PASS.**
    - S3 l.16: "compare q0 with q1 there. Their matrix element is g".
    - S2 l.44: "Bind changes one q at occupied p".
    - R3 l.5: "q-only Bind g at p=1".
    - The author correctly separates the test letter g in S2 l.22–24 from this coordinate (S2 l.24: "test numbers, not native Bind g").
    - C178 l.585.
11. **abs(kappa): PASS.**
    - S3 l.17: "Their forward matrix element is kappa=k exp(i phi_kappa), with the conjugate reverse".
    - S3 l.7: "k=|kappa|".
    - The author's T(a→b) convention places e^{iφκ} on the entry that raises S_graph. This agrees with S3 l.25: "Admission increases S_graph by one in its forward direction, so conjugation H→U_S H U_S† sends kappa→exp(i theta)kappa". Manual check: U_S|S,p1⟩⟨R,p0|U_S† = e^{iθ}|S,p1⟩⟨R,p0|.
    - The phase choice θ=−arg κ is the one in S3 l.25.
    - Its condition is S3 l.29: "These are basis equivalences ONLY when initial states, source operations and read effects are conjugated consistently". R3 l.9 says the same.
    - The author reports this transformation and does not adopt it.
    - C178 l.596.
12. **abs(epsilon_B): PASS.**
    - S3 l.19: "Old internal factors are copied, two labelled Ready/p=q0 stars are inserted, the pair becomes II and N increases by one".
    - S3 l.19: "epsilon times a positive integer channel multiplicity".
    - S3 l.19: "Exact adjoints and all failed images remain in the operator".
    - S3 l.27: "U_N(psi)=exp(i psi N) ... sends epsilon→exp(i psi)epsilon for every forward owned channel, because [N,B]=B. Its adjoint transforms conjugately".
    - S3 l.27: "U_S and U_N commute".
    - The name e ↔ abs(epsilon_B) rests on C178 l.473–481 citing S3 and R3. The author flags this (ambiguity 3), and I agree.
    - C178 l.607.

**Completeness: PASS.**
- The table has twelve rows, the same set in the same order as C178 l.486–607. jq lists 12 entries: Ud, mu0, lambda_J, lambda_R, r, delta_cell, nu, h, t, g, abs(kappa), abs(epsilon_B).
- Nothing extra is presented as a coordinate:
  - C is treated as the single identity coefficient (S3 l.7, "one common identity reference"; S3 l.21, "dimension13 including identity, or dimension12 modulo ONE global identity").
  - The C178 derived combinations (l.618–635, each "additional_free_coordinate": false) are not tabulated.
  - Raw parameters are not added to the coordinates (S3 l.39; C178 l.649).

## Cross-cutting checks

- **Sector (author l.18): PASS.** It matches S1 l.7–13, S2 l.14, S3 l.7 and C178 l.454.
- **Global Nc=Sg, local Q_i=0/2 retained (author l.43): PASS.**
  - It matches S1 l.9–13, R1 l.5 and R3 l.5.
  - Nc=Sg follows from Q=Nc+Rg+Rd and M=Rg+Sg+Rd (S1 l.9).
- **Common identity: PASS.**
  - There is one C·I, and it is not subtracted per N block. S1 l.44: "cannot be independently subtracted on each N block". Author l.83 and l.96.
  - It is not counted as a thirteenth coordinate.
- **Raw versus reparameterized derivatives: PASS. The two are not mixed.**
  - Block (A) holds the twelve coordinates and C fixed: ∂H/∂delta_cell=S_g, ∂H/∂mu0=S, ∂H/∂nu=N, ∂H/∂C=I.
  - Block (B) holds the other raw parameters and dstar fixed.
  - The map in S1 l.32–36 is transcribed exactly.
  - Block (B)'s right column is labelled as the author's check, not a source statement (author l.85).
  - The ES/epsc statement keeps S1 l.44's qualifier, "with every other parameter fixed".
  - I recomputed the chain-rule column by hand:
    - ER: Rg=V0+2N−Sg (S1 l.11) = −S_g+2N+V0·I. The chain rule gives (−1)S_g+(2)N+(V0)I. ✓
    - ES: S_g. epsc: Nc, which equals S_g only through the global identity. ✓
    - lambdaJ: Σd_ip_i=Σ(s_i+2)p_i=P_s+2Nc=P_s+2S_g. The chain rule gives (1)P_s+(2)S_g. ✓
    - Delta: Σ_e n_e=V+S/2=V0·I+2N+S/2. The chain rule gives (1/2)S+(2)N+(V0)I. ✓
    - Ud: Σ(s_i+2−dstar)²=D+2(2−dstar)S+(2−dstar)²(V0+2N). The chain rule gives the same four terms. ✓
    - eR: Rd=2K−2N. The chain rule gives (−2)N+(2K)I. ✓
    - eI: 2K−Rd=2N. The chain rule gives (2)N. ✓
    - epsr: Q_q. lambdaR: −Σd_iq_i=−Q_s−2Q_q. The chain rule gives (1)(−Q_s)+(−2)Q_q. ✓
    - Summed, these reproduce R1 l.7: C=V0·A+2K·eR and nu=2[A+eI−eR], with A=ER+Delta+Ud(2−dstar)².
- **R1–R3 applied: PASS.**
  - The three verdicts:
    - R1 l.3: "PASS SCOPED, no mandatory correction".
    - R2 l.3: "PASS_SCOPED, no correction".
    - R3 l.3: "PASS_SCOPED; no mandatory correction".
  - The scope items are carried:
    - R1 l.9: C·I versus nu·N; ES/epsc only with other parameters fixed; nu is not pressure.
    - R1 l.11: the backend two-level Birth dispatch is not substituted.
    - R2 l.11: restriction changes the rank.
    - R3 l.5: the Q=2/0 exit.
    - R3 l.9: the transformations are simultaneous state/read/source equivalences.
    - R3 l.11: fixed domain, uniform amplitudes and fixed profiles; zero-amplitude charts and absolute scale stay separate; the clock/read map is not retired.
- **C178 scope: PASS (by citation footprint).**
  - The author cites only C178 l.2, l.209 and l.454–649. Nothing is drawn from l.448–452 (supersedes_status).
  - A checker cannot observe what the author opened. The footprint is consistent with no legacy or target link having been followed.
- **Forbidden-claim scan of the qualifications: PASS on every item.**
  - New count: none. The 12 is restated from S3 l.21 and C178 l.456 as an operator rank, "not a fitted-parameter count".
  - Chosen values: none.
  - State-family shrinkage: none. The file says the chart is "not restricted to ice, local grounds, local Q_i=1, r=0 or a single N".
  - Zero-phase adoption: none. The file says it "adopts no zero phase", and φκ and φε stay explicit.
  - C178 alteration: none. The C178 hash is unchanged.
  - Contact elimination: none. The file says zero second derivatives do "NOT eliminate physical-source, nonlinear-coefficient, preparation or metric contacts".
  - Local energy allocation and proper-time rule: neither is supplied.
  - Calibrated count: still unpopulated and uncertified. I confirmed with jq that `required_shared_fitted_coordinate_count` is null (C178 l.209) and `physical_family_adopted_by_this_entry` is false (l.457). Every row in l.484–616 has physical_value and calibration_source null, NOT_CALIBRATED and OPEN.

## Errata

None.

## Notes (no change required)

- **N1.** In the main table, row 6's support cell says that only epsc·Nc reaches delta_cell through Nc=Sg.
  - The 2lambdaJ·Nc part of the raw term lambdaJ·Σd_ip_i also reaches delta_cell only through that global identity (S1 l.34; R1 l.7).
  - Block (B)'s lambdaJ row already states this, so the main table is incomplete on this point but not wrong.
- **N2.** Author l.94 says "on ice" where S2 l.40 says "on strict ice". The meaning is the same in context.
- **N3.** Brief 0401 l.9 asks for one short table and a short qualifications paragraph. The file has two tables and several qualification paragraphs. The second table carries the raw-versus-reparameterized separation that the brief requires at l.7.
- **N4.** Ambiguities 1, 2, 3 and 6 are correctly left open. They concern:
  - the hopping reverse-orientation phase and exchange signs;
  - selection rules inside the owner sums;
  - the Birth channel list and m_c;
  - the hopping phase values;
  - the name identifications;
  - the beta symbols.

  Settling any of them would need sources outside this check's read set. This check does not resolve them.

## Non-claims

This check does not:
- derive a coordinate count;
- choose values;
- restrict the state family;
- adopt a phase;
- alter C178;
- eliminate any contact;
- supply a primitive local energy allocation or a proper-time rule.

The physical calibrated count remains unpopulated and uncertified.
