# Native coordinate interface crosswalk — 0401 V001

- Author role: author, Claude helper. A different checker is required (task 0401 l.11).
- Task: `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0401_2026-10-15_native_coordinate_interface_crosswalk.md` SHA256 `2cc708dbe42c3a27c887d5ecc02f415219c2c82314e51d6f309e92a0fffc68b8`
- Status: **source transcription only.** No new physics, coordinate count, value, phase choice, state-family restriction, schema, code or numerical execution. C178 is not altered.
- All seven source hashes were computed from bytes before reading and matched:
  - S1 `33a4f1adfa74986e510630f15dc30551fbbe78e05497cc954e9eec5a5753c3f6`
  - R1 `1a82af99a201b83d10bcd5d5a7bbbbc7ddbd1db6b526a26716e8d24dc8585f6c`
  - S2 `604cc21f716623786f7db3c9083d47c7299882befd3b76cff1dfa974c3745398`
  - R2 `9406114b0ca787b1e8f89257afb94a0211d4b84d7c4a55618c73ab1935d26372`
  - S3 `66d71e9c0a53b498b5e105796fc52656fcc7b7917d5ca88789f25018605645db`
  - R3 `f7da66721f8ba845adf4c4e9a333c9d6c672254da1b0304135f0ee39e6b479a0`
  - C178 `122c26bd59b92014ace41bf2822cd7bc2100d91a5fd428820a7f2f9cf2b98ebb`
  (Full paths are in the citations list.)

## Chart being transcribed

The sector is the P26_CONCURRENT_BIRTH_V002_OWNED_READY owned-Ready invariant sector of the all-Ready, empty-slot preparation. It has V0 original vertices, K owned slots (K=V0 in the adopted finite control), N active slots and V=V0+2N existing vertices. M_i=R_i+S_i=1 holds at every existing graph site, donors are RR (absent slot) or II (active slot), and total Q=M. The global identities are Nc=Sg, Rg=V0+2N−Sg and Rd=2K−2N. The sector includes the full incidence cube, the eight-state internal factors, all q bits and all N blocks. It also requires uniform coefficients and amplitudes, a fixed finite domain, native basis and dstar convention, and a fixed, compatible, unit-modulus hopping-edge phase profile in which no holonomy is set to zero (S1 l.7–13, 17; S2 l.14; S3 l.7; C178 l.454). On this sector, the full Hamiltonian is the diagonal chart (S1 l.26–28; S2 l.9–12) plus the unchanged native off-diagonal owners (S1 l.40; S3 l.7, 15–19):

H = C·I + Ud·D + mu0·S + lambdaJ·P_s − lambdaR·Q_s + r·Q_q + delta_cell·S_g + nu·N + [h, t, g, abs(kappa), abs(epsilon_B) owners below], with the phases phi_kappa and phi_eps and the hopping profile held fixed.

Notation:
- s_i=d_i−2, where d_i is the incidence degree of graph vertex i and Σ_i d_i=2Σ_e n_e.
- p_i is the carrier bit, q_i the record bit and Spent_i the cell label.
- Σ_i runs over all V=V0+2N existing graph vertices of each N block.
- T(a→b) is a unit-entry transition from local label a to b, with every other label fixed.

| Coordinate | Operator multiplying it (= ∂H/∂coordinate, with the other eleven, C and the fixed phases/profile held fixed) | Sign | Support | Source |
|---|---|---|---|---|
| Ud | D = Σ_i (d_i−2)² = Σ_i s_i² | + | diagonal; every existing graph vertex; incidence degree | S1 l.26; S2 l.9–10; C178 l.486 |
| mu0 | S = Σ_i (d_i−2) = Σ_i s_i | + | diagonal; same as Ud | S1 l.26, 32; S2 l.9–10; C178 l.497 |
| lambdaJ | P_s = Σ_i (d_i−2) p_i | + | diagonal; degree × carrier bit | S1 l.27; S2 l.9, 11; C178 l.508 |
| lambdaR | −Q_s = −Σ_i (d_i−2) q_i | − | diagonal; degree × record bit | S1 l.27; S2 l.9, 11; C178 l.519 |
| r | Q_q = Σ_i q_i | + | diagonal; graph-site record bits | S1 l.28, 33; S2 l.9, 12; C178 l.530 |
| delta_cell | S_g = Σ_i Spent_i (= Sg) | + | diagonal; graph cells; the raw epsc·Nc term enters here only via the GLOBAL identity Nc=Sg | S1 l.11, 13, 28, 34; S2 l.12; R1 l.5; C178 l.541 |
| nu | N (count of active owned slots, i.e. II pairs; V=V0+2N) | + | diagonal; varies under Birth. A relative contact between N blocks, retained (not dropped as a per-level offset) | S1 l.28, 35, 38, 44; S2 l.9, 40; R1 l.9; C178 l.552 |
| h | −Σ_e F_e, where F_e is the unit transition between states differing only in incidence bit e | − | one supporting-graph edge bit; all other labels fixed | S3 l.15; S2 l.44; R3 l.5; C178 l.563 |
| t | −Σ over occupied edges ij of phi_(i←j)·T(p_i,p_j: 0,1→1,0), summed over both orientations; phi is the fixed unit-modulus oriented edge phase | − (× edge phase) | two endpoint carriers of an occupied edge; cells, records and incidence fixed; exits with local Q=2/0 retained | S3 l.7, 18; S2 l.44; R3 l.5; C178 l.574 |
| g | Σ_i P(p_i=1)·[T_i(q0→q1)+T_i(q1→q0)] | + | one record bit at a site with p_i=1; all else fixed | S3 l.16; S2 l.44; R3 l.5; C178 l.585 |
| abs(kappa) | Σ_i [e^{i·phi_kappa}·T_i(Ready,p0→Spent,p1) + e^{−i·phi_kappa}·T_i(Spent,p1→Ready,p0)], q_i fixed; kappa = abs(kappa)·e^{i·phi_kappa} | + (× phase) | one site's cell plus carrier; forward step raises S_graph by 1; other sites unchanged | S3 l.7, 17, 25, 29; R3 l.5, 9; C178 l.596 |
| abs(epsilon_B) | Σ_c m_c·[e^{i·phi_eps}·B_c + e^{−i·phi_eps}·B_c†]. B_c is the owned Birth transition of listed channel c: it copies old internals, inserts two labelled Ready/p=q=0 stars, sends donor pair RR→II and sends N→N+1. B_c† is its exact adjoint; failed reverse images are zero and retained. m_c is a positive integer multiplicity of identical listed transitions | + (× phase × m_c) | supporting graph and active labels, donor pair and newborn factors; across N→N+1 blocks | S3 l.7, 19, 27, 29; S2 l.44; R3 l.5, 9; C178 l.607 |

**Global identity, not local.** The operator equality uses the global identity Nc=Sg, which follows from total Q=M. It does not use local p_i=S_i, and local Q_i=1 does not follow. Local Q_i=0 and Q_i=2 states remain in the domain, including the hopping exit (S1 l.13; R1 l.5; R3 l.5).

**Phase/read transformations used by the sources (not adopted here).**
- **abs(kappa):** U_S(theta)=exp(i·theta·S_graph), with H→U_S H U_S†. This sends kappa→e^{i·theta}·kappa and leaves the diagonal, Bind, flip, hopping and Birth owners unchanged. theta=−arg kappa makes kappa real and positive (S3 l.25; R3 l.9).
- **abs(epsilon_B):** U_N(psi)=exp(i·psi·N). Because [N,B]=B, this sends epsilon→e^{i·psi}·epsilon on every forward owned channel, with adjoints transformed conjugately. psi=−arg epsilon makes it real and positive (S3 l.27; R3 l.9).
- U_S and U_N commute. Neither changes hopping holonomies.
- Both are basis equivalences ONLY when initial states, source operations and read effects are conjugated consistently. A fixed coherent apparatus can retain relative phase information. A zero amplitude has an undefined phase. Relative channel phases, incompatible profiles and alternative donor laws are not covered (S3 l.29, 31).
- This crosswalk keeps phi_kappa and phi_eps explicit and adopts no zero phase.

## Raw-parameter derivatives vs derivatives holding the reparameterized coordinates fixed

**(A) Reparameterized coordinates held fixed** (the twelve coordinates plus C):
- ∂H/∂delta_cell = S_g, ∂H/∂mu0 = S and ∂H/∂nu = N.
- C appears only as the separate common-identity coefficient, so ∂H/∂C = I (S1 l.17, 26–28; S2 l.7; S3 l.7).

**(B) Raw parameters, with the other raw parameters fixed and dstar a fixed convention.**
- Original diagonal (S1 l.19–22): Delta Σ_e n_e + Ud Σ_i(d_i−dstar)² + epsc Nc + epsr Σq_i + lambdaJ Σ d_i p_i − lambdaR Σ d_i q_i + ER Rg + ES Sg + eR Rd + eI(2K−Rd).
- Map (S1 l.32–36):
  - mu0 = Delta/2 + 2Ud(2−dstar)
  - r = epsr − 2lambdaR
  - delta_cell = ES + epsc + 2lambdaJ − ER
  - nu = 2[ER + Delta + Ud(2−dstar)² + (eI−eR)]
  - C = V0[ER + Delta + Ud(2−dstar)²] + 2K·eR

| Raw | Raw operator (S1 l.19–22) | Enters (∂coordinate/∂raw) | Same derivative written in chart operators (author check) |
|---|---|---|---|
| ER | Rg | delta_cell −1; nu +2; C +V0 | −S_g + 2N + V0·I (= Rg via S1 l.11) |
| ES | Sg | delta_cell +1 | S_g |
| epsc | Nc | delta_cell +1 | S_g (equals Nc only via the global identity Nc=Sg) |
| lambdaJ | Σ d_i p_i | lambdaJ +1; delta_cell +2 | P_s + 2S_g (= Σ d_i p_i via the global identity Nc=Sg) |
| Delta | Σ_e n_e | mu0 +1/2; nu +2; C +V0 | S/2 + 2N + V0·I (= V + Σ s_i/2, S1 l.24) |
| Ud | Σ_i(d_i−dstar)² | Ud +1; mu0 +2(2−dstar); nu +2(2−dstar)²; C +V0(2−dstar)² | D + 2(2−dstar)S + 2(2−dstar)²N + V0(2−dstar)²·I |
| eR | Rd | nu −2; C +2K | −2N + 2K·I (= Rd via S1 l.11) |
| eI | 2K−Rd | nu +2 | 2N |

The same distinction applies to r. Raw ∂/∂epsr gives Q_q. Raw ∂/∂lambdaR gives −Q_s − 2Q_q (= −Σ d_i q_i), whereas the reparameterized ∂H/∂lambdaR at fixed r is −Q_s.

The sources state these raw facts directly:
- In the sector, with every other parameter fixed, ES→ES+z with epsc→epsc−z leaves H unchanged because Sg=Nc. More general offset changes must preserve the displayed combinations and account for C (S1 l.44; R1 l.9).
- Raw parameters related by the reparameterization must not be added again to the coordinates (S3 l.39). The raw categories in C178 are not added to the coordinate dimension (C178 l.649).
- C·I is one global reference and cannot be subtracted per N block (S1 l.44; R1 l.9; S2 l.40).

The right-hand column is the author's manual chain-rule check of S1's displayed decomposition. It agrees with R1's independent expansion (R1 l.7). It is not a new source statement.

## Qualifications

**Domain.** The chart holds only on the stated sector:
- the owned-Ready invariant sector of the all-Ready, empty-slot preparation, with every N block, the full incidence cube and the eight-state factors;
- uniform coefficients and amplitudes, a fixed domain, basis, dstar and a compatible hopping-phase profile;
- for positive magnitudes, the interior of the amplitude cone (zero-amplitude boundaries need their own phase chart).

It is not restricted to ice, local grounds, local Q_i=1, r=0 or a single N (S2 l.14; S3 l.7). It does not extend unchanged to nonuniform profiles, graph I cells, another Q−M sector or other donor/slot invariants (S1 l.46; R1 l.9). Restrictions change the rank: on ice D, S, P_s and Q_s vanish, at fixed N the operator N is a constant, and r=0 is a diagnostic restriction. None of these licenses erasing a full-domain owner (S2 l.40; R2 l.11; C178 l.460).

**Common identity.** There is exactly one common identity, C·I. The nu·N term is a genuine relative diagonal contact. nu is not pressure, a spectral gap or a calibrated volume/energy density (S1 l.38, 44; R1 l.9).

**Second derivatives.** With the phases and profile fixed, H is linear in the twelve coordinates, so its second derivatives in this chart vanish. That does NOT eliminate physical-source, nonlinear-coefficient, preparation or metric contacts.

**Count status.** The dimension of 12 modulo one global identity is an operator-coordinate rank. It is not a fitted-parameter count, a set of measured constants, a ratio count or a postulate total. The common multiplicative energy scale is not removed, and the native-to-physical clock/read map is still required (S3 l.21, 35–37; R3 l.11; C178 l.455–459). The physical calibrated count remains unpopulated and uncertified:
- `required_shared_fitted_coordinate_count` is null (C178 l.209);
- `physical_family_adopted_by_this_entry` is false (l.457);
- every coordinate row has physical_value and calibration_source null, NOT_CALIBRATED status and empirical_identifiability OPEN (l.484–616).

**What the chart does not supply.** It supplies no primitive local energy allocation and no proper-time rule; proper time remains pending (0401 l.3, 9).

**Review corrections.** R1, R2 and R3 are each PASS SCOPED with no mandatory correction. Their scope qualifications are applied above:
- R1: C·I versus nu·N; the ES/epsc compensation holds only with the other parameters fixed; the old backend two-level Birth dispatch is not substituted.
- R2: restricted-sector rank changes.
- R3: Q=2/0 hopping exits are retained; the phase maps are simultaneous state/read/source equivalences.

## Ambiguities / unresolved (recorded, not resolved)

1. **Off-diagonal operators.** These are transcribed at the matrix-element and support level stated in S2 l.44, S3 l.15–19 and R3 l.5. Their literal owner definitions are pinned by S1 (l.50–53) and S3 (l.43–51) but were not opened, because transcription at the stated level was possible. The following stay open here:
   - exchange or ordering signs for hopping beyond the "fixed oriented edge phase", and how the reverse-orientation phase relates to the forward one;
   - any further selection rule inside the flip, Bind or admission sums;
   - the exact Birth channel list and multiplicities m_c (S3 l.19 says the canonical convention "ordinarily gives one").
2. **Hopping phase values.** The phases phi_(i←j) are fixed but not stated in the sources, so ∂H/∂t depends on that unstated profile.
3. **Names.** The C178 names abs(kappa), abs(epsilon_B), lambda_J and lambda_R are identified with S3's k=|kappa| and e=|epsilon| and with S1/S2's lambdaJ and lambdaR. The identification rests on C178 citing S2/R2/S3/R3 (C178 l.461–481). The subscript B is not used in S3.
4. **Test letters in S2.** In S2 l.22–24 the letters a…g are test numbers. That g is not the Bind coordinate g.
5. **dstar.** dstar enters mu0, nu and C but is a fixed convention, and no derivative with respect to it is given or taken.
6. **Derived combinations in C178.** The current C178 section also lists derived combinations (l.618–635: beta, r_B and rho_B_ring, each with additional_free_coordinate false). The symbols "D" and "p" in beta = nu − 2 D p are undefined in the section read and may not be S2's D. Their sources were not opened, and these combinations are not transcribed.
7. **Author check.** The chain-rule column in block (B) is author algebra and needs verification by the checker.

## Citations

- S1 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_UNIFORM_RESOURCE_SECTOR_EXACT_DIAGONAL_COORDINATES_PROPOSED_V001.md` SHA256 `33a4f1adfa74986e510630f15dc30551fbbe78e05497cc954e9eec5a5753c3f6` (full text read).
- R1 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/OWNED_UNIFORM_RESOURCE_DIAGONAL_COORDINATES_DISTINCT_REVIEW_V001.md` SHA256 `1a82af99a201b83d10bcd5d5a7bbbbc7ddbd1db6b526a26716e8d24dc8585f6c` (full text read).
- S2 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_UNIFORM_DIAGONAL_SEVEN_COORDINATE_OPERATOR_RANK_PROPOSED_V001.md` SHA256 `604cc21f716623786f7db3c9083d47c7299882befd3b76cff1dfa974c3745398` (full text read).
- R2 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_DIAGONAL_SEVEN_COORDINATE_RANK_DISTINCT_REVIEW_V001.md` SHA256 `9406114b0ca787b1e8f89257afb94a0211d4b84d7c4a55618c73ab1935d26372` (full text read).
- S3 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/OWNED_FIXED_PROFILE_OFFDIAGONAL_INDEPENDENCE_AND_TWELVE_COORDINATES_PROPOSED_V001.md` SHA256 `66d71e9c0a53b498b5e105796fc52656fcc7b7917d5ca88789f25018605645db` (full text read).
- R3 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/response_packet_audit/OWNED_FIXED_PROFILE_TWELVE_COORDINATES_DISTINCT_REVIEW_V001.md` SHA256 `f7da66721f8ba845adf4c4e9a333c9d6c672254da1b0304135f0ee39e6b479a0` (full text read).
- C178 `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/READINESS_C178_SHARED_CALIBRATION_EXTENSION_V002.json` SHA256 `122c26bd59b92014ace41bf2822cd7bc2100d91a5fd428820a7f2f9cf2b98ebb`. Read: the current coordinate section, l.448–657, plus the keys kind (l.2) and required_shared_fitted_coordinate_count (l.209), located with grep/jq. Legacy-ledger and target links were not followed.
- Task 0401 `/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0401_2026-10-15_native_coordinate_interface_crosswalk.md` SHA256 `2cc708dbe42c3a27c887d5ecc02f415219c2c82314e51d6f309e92a0fffc68b8`.
- No other primary source was opened.
