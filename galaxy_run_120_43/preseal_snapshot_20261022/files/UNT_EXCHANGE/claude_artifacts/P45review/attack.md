# P45 attack: sixth-order uniform diagonal and the light-ratio consequence

Reviewer: Claude (independent refutation attempt). Date: 2026-10-12.
Target: `lanes/P45_CODEX2/P45_SIXTH_ORDER_UNIFORM_DIAGONAL_AND_ENDPOINTS_V001.txt` (sha in manifest 93435398…), sources `uniform_sixth_order_clusters_v001.py` and `formal_endpoint_handoff_v002.py`, announcement `FROM_CODEX2/0043_…`.
I read the Codex sources as text only. I did not import or execute them. All numbers below come from my own code in this folder, using exact `fractions` unless a line says otherwise.

## Verdict

**The theorem survives the attack.** At uniform q on a 4-regular graph of girth ≥ 6, the h^6 diagonal of H_eff on the ice space is one constant for every ice configuration. Through h^6 the operator is c_b(h)·I − K_b·R, with K_b = h^6 T(x_b)/(2Ud)^5. I found no error in the proof, the counts or the c6 expression.

**The light-ratio consequence is correct only as a leading-order, conditional statement.** The P45 text frames it that way ("formal in h", "+O(h^8)", "if R has a qualified photon"). An unqualified reading, "the velocity ratio is T(x1)/T(x0)", is false at finite h. The corrections are O((h/2Ud)^2) and differ between the endpoints. They come from two sources:
- a dressing of the hexagon amplitude;
- a new 8-cycle ring operator that is not proportional to R. Diamond has 3 elementary 8-cycles per vertex.

They do not come from an RK potential (section 3).

## 1. Independent tests of the diagonal claim

### 1a. Brute-force whole-graph RS (`brute_rs.py`, `run_brute.py`)

The test does not use any cluster or inclusion–exclusion logic:
- It keeps every flip subset up to Hamming distance 3, connected or not.
- It keeps every folded term E^(j)·ψ^(k−j).
- It computes excitation energies straight from the vertex degrees, so it also tests the pairwise D(S) formula.

Ud = 1 throughout.

| graph | V / E / girth / 6-cycles | ice states | α values | h², h⁴, h⁶ identical across states? |
|---|---|---|---|---|
| PG(2,3) incidence = (4,6)-cage | 26 / 52 / 6 / 234 | 12 (flippable-hex counts 33–46) | 0, 1/4, −3/10 | yes (exact) |
| diamond, primitive torus L=3 | 54 / 108 / 6 / 162 | 8, polarizations (36,−12,−12), (12,12,12), (0,12,0), (−12,−24,0), … | 0, 1/4, −3/10 | yes |
| diamond, conventional torus L=2 | 64 / 128 / 6 / 128 | 6, polarizations (0,64,−16), (−16,0,−16), (16,0,0), … | 0, ±1/4 | yes |

The test states span different flux sectors and different flippable-hexagon counts: 14 to 27 on conventional L=2, 25 to 31 on primitive L=3.

Per-vertex coefficients, with all odd orders exactly 0:
- **α = 0:** c2/N = −1, c4/N = −7/12, **c6/N = −893/540**. In general units this is c6/N = −893 h^6 / (540 Ud^5). The Ud-scaling ratio of 32 between Ud=1 and Ud=2 was checked.
- **α = ±1/4:** c2/N = −64/63; c4/N = −6768640/11918907; c6/N = −584223680005892145152/315618003222506159175. The values are equal at +α and −α, as the global particle–hole symmetry requires.
- **α = −3/10:** c6/N = −8769311136861861104000000/4503848104132708064826807.

My own Möbius-inverted support formula (`cluster_and_ring.py`) reproduces every one of these values exactly. It has the P45 structure: edge, pair 1/4/1, star 2/2, path m_s(u)m_s(v). The P45 text says it gives no numeric c6 target; −893/540 can serve as one for root's reconstruction.

### 1b. Sensitivity control (`sensitivity_control.py`)

This checks that the harness can see a configuration-dependent h^6 diagonal when one is present. I used the 4-regular circulant C10(1,2), which has girth 3; its triangles are 3-edge supports whose sign counts depend on the configuration.
- E2 = −10 and E4 = −35/6 in all 8 sampled states.
- E6 takes **3 distinct values**: −251/18, −15331/1080 and −7801/540. They track the occupied-count census of the triangles.

So the zero on girth-6 graphs is not a blind spot of the method.

### 1c. Census of the count claims on real ice states (`cluster_and_ring.py`)

On diamond primitive L=3 (N=54), identical in 4 random states:

| support | sign pattern | count |
|---|---|---|
| edges | − / + | 54 / 54 |
| adjacent pairs | ++ / +− / −− | 54 / 216 / 54 (= 1 / 4 / 1 per vertex) |
| stars | ++− / +−− | 108 / 108 (= 2 / 2 per vertex) |
| paths (end, centre, end) | −−− / −−+ / −+− / −++ / +−+ / +++ | 54 / 216 / 216 / 216 / 216 / 54 |

The path counts equal m_s(u)·m_s(v) per central edge, 18 per vertex in total. PG(2,3) gives the same per-vertex numbers.

Disconnected supports, including all folds, have connected weight exactly 0 at every order. I tested a disjoint triple and a pair plus a separate edge.

## 2. Item-by-item attack

**(a) Folds, renormalization and convention dependence: no loophole.**
- H_eff^(k) for k ≤ 5 is diagonal, because two distinct ice states differ by an alternating even subgraph of length ≥ 6.
- H_eff^(2) and H_eff^(4) are scalars.
- Bloch, des Cloizeaux and Schrieffer–Wolff/direct rotation differ by P-space similarity transforms S = 1 + S2 + S4 + …. The order-6 change is a sum of commutators [S^(k), H^(6−k)], and every H^(j<6) is scalar, so all three conventions give the same H^(6), diagonal and ring parts alike.
- Take the coefficient of a monomial ∏h_e^{k_e} with support C, |C| ≤ 3. Setting h_e = 0 off C isolates a cube that contains one ice state, so that coefficient equals the exact cube energy in every convention.
- Products of order-2 and order-4 pieces that are "constant only after summation" are unlinked products of global scalars. They cancel against disconnected supports, which 1a confirms numerically.
- P45 step 2 states this in compressed form ("…in the common direct-rotation frame"). It is correct, but the commutator argument above should be written out.

**(b) Sign-pattern counts for paths and stars: correct.** Every vertex has two + and two − edges. Given the sign of the edge used to enter a vertex, the other three edges there have fixed signs: one the same, two opposite. Girth ≥ 6 rules out any coincidence among the chosen edges. The census in 1c confirms the counts directly.

**(c) Hexagon processes in the h^6 diagonal: none.**
- A word that flips each hexagon edge once is off-diagonal.
- A diagonal word on a hexagon needs at least 12 flips.
- A non-alternating hexagon flip does not land on an ice state.

**(d) The velocity ratio.**
- Through h^6, the constant c_b drops out of every gap.
- No other off-diagonal term exists at h^6: an alternating even subgraph with 6 edges on a girth-6 graph is a single 6-cycle.
- K = h^6·T/(2Ud)^5 checks out:
  - T(0) = 252 by enumerating all 720 orderings.
  - T is even: T(±1/16) = 92255964626944/359401303125 and T(±1/8) = 89792708608/330812181.
  - The value is the same on all 82 flippable hexagons tested across 6 states (degree-based energies, α = 1/4).
  - The P39 closed form (my transcription) agrees at x = 0, 1/16, 1/8 and 1/4.
  - Exact diagonalization of the 64-state hexagon cube gives split/(2K) = 0.98989, 0.99748, 0.99937 at h = 0.08, 0.04, 0.02, converging to 1.
- So the ratio v1/v0 = T(x1)/T(x0) holds at leading order, given that the pure ring operator has a photon. The limits are in section 3.

**(e) The diamond lattice.** The infinite diamond lattice qualifies: it is 4-regular, has girth 6, and has 2N hexagons. Finite tori need care:
- **Primitive L=2 torus (16 vertices):** girth 4. The theorem does not apply, because square ring exchange already enters at h^4.
- **Primitive L=3 torus:** girth 6, but 162 six-cycles: 108 local hexagons plus 54 winding six-cycles, made of alternating pairs of bond directions around 3·a_i. Those winding cycles are elementary six-cycles, so they belong to R and connect flux sectors. This is a finite-size artifact.
- **Primitive L ≥ 4 and conventional L = 2 tori:** clean. For example, 256 = 2V six-cycles at primitive L=4.

The existence of a photon in pure R (V = 0, stoquastic sign) is supported by the published QMC literature on quantum ice. It is not derived in P45, which says so.

## 3. Weakest step, and what limits the consequence

1. **The first non-R structure appears at h^8, and it is off-diagonal.**
   - I extended the brute force to h^8 on PG(2,3) (`run_order8.py`). The h^8 diagonal is still a single constant: c8/N = −209966173/27216000 at α = 0, identical over 5 distinct states with flippable-hex counts 34, 39, 33, 38 and 46. It is also constant at α = 1/4.
   - The reason is general. A diagonal word at order 2k has support of at most k edges. Below the girth, that support is a forest, and forest sign-counts are fixed by the 2+/2− rule. So the diagonal is scalar through h^10 on girth-6 graphs, and the first RK or flippability potential can appear only at h^12. h^8 was verified; h^10 rests on this argument alone.
   - At h^8, H becomes c + K6·(1 + κ(x)(h/2Ud)^2)·R6 + K8·R8.
   - **R8 (8-cycles):** diamond has 3 elementary 8-cycles per vertex (750 on primitive L=5), and about 8% of them are flippable in random ice states (55–74 of 750). K8 = h^8·T8/(2Ud)^7, with T8(0) = 3432 and T8(±1/8) = 15015814881083392/3938980639167. T8/T6 = 13.619 at x = 0 and 14.044 at x = 1/8. So R8 enters with relative weight about 14·(h/2Ud)^2, and that weight depends on the endpoint.
   - **Dressing of the hexagon amplitude:** the in-cube part alone is κ ≈ −6.29 at x = 0 and −6.85 at x = 1/8. This comes from exact-diagonalization fits; the dressing from external edges is not included.
   - **Consequence:** v1/v0 = τ·[1 + O((h/2Ud)^2)], with a correction coefficient of order 0.5–1 that differs between the endpoints. Against the P43 equivalence margin of 1/100, the leading-order τ decides the question only when (h/2Ud)^2 ≪ 10^−2. At h/2Ud ≈ 0.1 the correction is already comparable to the margin.
   - The P45 text says "formal in h" but does not name R8. The h^8 operator is not "one fixed ring operator".
2. **Proof step 2** is correct but compressed (see 2a).
3. **Proof step 1** says "Nonconstant terms at other orders are not excluded by this observation alone." That is true, but it can be sharpened: the diagonal is scalar through h^10 (section 3, item 1).
4. **Code portability.** `connected_weights` uses `int.bit_count()`, which needs Python ≥ 3.10. `/usr/bin/python3` here is 3.9.6 and raises `AttributeError`. The root runtime recorded in P30 is 3.12.14, so this is a custody note, not a scientific defect. The same call appears in a later file in the same folder, `carrier_defect_resolvent_words_v001.py`.

## 4. Spot checks on the other sections (all pass)

- **Local quartic (C, F):** a=3, e=r=10, g=4, κ=3. Poles at b=0: 5.479203, 10, 13, 17.520797. Poles at b=1: the same minus 3.
- **C_b residues:** (0.525189, 0, 0.264706, 0.210105) at b=0 and (0.210105, 0.264706, 0, 0.525189) at b=1. The selected residue is Z = (59+3√145)/(145+3√145) = (129+25√145)/(68√145) = 0.5251892, the same on both selected branches.
- **Clock h^2 shift (D):** for α = 1/4, λ_R = 1/8, the brute-force E2(adjacent word) − E2(uniform) = 128/5355, which equals the formula d2 exactly.
- **Adjacent-word diagonal:** with one Record flip, the diagonal stays scalar through h^6 (1 distinct value over 6 states). This matches the text: only the ring amplitudes of hexagons through v change.

## Files (mine, in this folder)

`graphs.py`, `brute_rs.py`, `run_brute.py` (logs: `pg23_run.log`, `prim3_run.log`, `conv2_run.log`), `cluster_and_ring.py` with `cluster_and_ring.out.json`, `ed_hexagon.py` with `.out`, `run_order8.py` with `order8.out`, `ring8.py` with `.out`, `flippable8.py` with `.out`, `sensitivity_control.py` with `.out`, `check_closed_T.py`.

The other `p45_*` and `*_output.json` files in this folder belong to a different reviewer. They were not used here.
