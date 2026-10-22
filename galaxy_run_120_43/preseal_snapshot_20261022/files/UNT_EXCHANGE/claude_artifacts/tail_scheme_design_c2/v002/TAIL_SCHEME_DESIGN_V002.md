# TAIL_SCHEME_DESIGN_V002: the tail-corrected lapse, revised against CHECK_V001 (design only)

tail_scheme_design_c2/v002, 2026-10-18 (UTC). **Design only.** Nothing here is adopted or reviewed, and no production code exists.

**What this is.** The successor of TAIL_SCHEME_DESIGN_V001 (`.md` 3b61201d, `.json` d3261fa4, both unchanged). It resolves every finding of CHECK_V001 (006e8463: K1–K16 and note N1). §0 maps each finding to its resolution. Where the check found V001 sound, V001's text stands and is cited, not repeated.

**Scope and hygiene.**
- Nothing was launched. No NGC3198 observed or target velocity was opened.
- I read program bytes only, and wrote only under `tail_scheme_design_c2/v002/`.
- One synthetic script ran (`tools/synthetic_zero_checks_v001.py`; numpy, nice 10, single-thread BLAS, one process). It reads no program bytes.
- Hashes are computed from bytes (`HASHES.txt`). The machine twin is `TAIL_SCHEME_DESIGN_V002.json`. The prereg draft is `KMAX_TAIL_PREREG_V007_DRAFT.json`.

**Decision pins.**
- Frozen: V002 addendum `17c26616`, V003 addendum `5bef6552`.
- Open, cited by name only: ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V004_ADDENDUM (A21–A30).
- Sealed prereg: KMAX V005 `dbddc02c` (τ_i, D̂, `shape_pass`, gates V1–V6).
- V006 R1 (`807fc5bf`) is a draft, not sealed, and is cited by name. T2 uses whichever V006 version is sealed.

**Driver naming (A29).**
- **v009-EXT** = `kmax_prereg_v005_c2/extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py` `999331af`.
- **v009-GEO** = `stage_successor_gal_c2v005/driver/galaxy_m0_forward_c2v009.py` `237ef3d4`.
- **v010** (planned) = v009-EXT bytes + v009-GEO's gal_c2v005 stage pins + the R-A F-A fix + the `uv_tail` block (§3.6). Every record cites the sha.

**Inputs read (sha256 prefixes, from bytes).**
- UV_TAIL_STUDY_V001 `41c2dfac`/`63c3f62c`, with its CHECK `10492597`.
- Claude3:
  - 0041 RESULT_SHELL_RESOLVED V003 `81d92656`;
  - followup RESULT_ORIGIN V002 `9e8cc888`;
  - RESULT_SOURCE_REPRESENTATION V001 `1d30ead1`.
- QINF_DEPENDENCE_V001 `32a6858a`.
- gal_c2v005 CHECK_V001 `a3008e93` (finding F1).
- REVIEW_DRIVER_V008_C4_V001 `f0987f41` §6 (F-A, V8c-F1).
- NGC k-grid prereg `4c2eefeb` and tier-2 result `245dbbc5`.

Every code file cited below is pinned with its full sha256 in the JSON twin (`code_pins`).

---

## Answer in brief

1. **Every finding has a resolution (§0).**
   - The three blockers:
     - K1: T1 is now V005 `shape_pass` verbatim, contraction clause included. A higher-K tail-corrected comparison is added (C6T against C4T), and T2c becomes pass/fail.
     - K2: the limit object is restated as the field of the registered smooth source, Φ_∞[S_T]. The in-cube source-representation bias b_K gets its own measurement (SR-K).
     - K3: a new gate B3 tests E1 jets, the lapse pair and the column potential against an independent Cartesian implementation.
   - K4: five NGC N-test evaluator sites are added, each with a successor.
   - K5: T2's nodes_v001 source at the fs stages is now the offset's own Cartesian forward sum.
2. **The definition is kept** (V001 §1.1–1.3), with five changes:
   - The tail output is real by construction.
   - bd(z=0) is exactly 0.0 by an expm1 form; this is a stated requirement (K11), and a synthetic check confirms it.
   - The phase rule now holds with real numbers (K12). Production widths are revised to DDO w⊥ 0.05, w_z 0.02 and NGC w⊥ 0.0050, w_z 0.0070 per kpc.
   - Corner tables are streamed per radius (K15).
   - The offset's kept region is the stage mask (N1).
3. **The remainder now has three bounds (K6).**
   - SRB-ROT: the static rotation-channel bound, renamed. It is necessary, not sufficient.
   - RB-FP: an empirical full-chain bound. It is ε_cert × a measured fixed-point sensitivity (AMP run) × a measured cross-shell cancellation factor × 2.
   - ε_cert: a sampled-with-refinement certificate, labelled as an estimate, not a proven sup.
4. **Two new certificates.**
   - LO extends the TESTED lapse-only omission from (2,4] to [4, K_big] (K14).
   - A route-A tail-source monitor M_T is recorded each iteration, with a pre-named threshold of 1/4 (K13).
5. **Module list (§3).** The full file list with signatures, inputs, outputs and the file:line of every insertion slot:
   - library and source roster;
   - libm Jₙ provider;
   - certificates;
   - 9 route-A successors;
   - 8 route-B successors, now based on **gal_c2v005** (lines re-based +7, read from bytes);
   - driver v010;
   - 4 NGC evaluator successors;
   - gate tools.
6. **Gates B0–B3 (§4).**
   - B0: planning identity against both v009 parents.
   - B0′: result-byte identity of v010's post-processing (K9).
   - B0-FA: the F-A deciding test.
   - B1: empty-domain identity against a gal_c2v004-lineage reference, conditional on gal_c2v005 deciding (i), with a same-lineage fallback (K10).
   - B2: static rows against an independent implementation.
   - B3: lapse pair, jets and column potential (K3, K11).
7. **Prereg V007 draft (§5, JSON authoritative).**
   - Comparison thresholds are separated from the Picard gate by a decidability rule and a pre-named pair refinement (K7).
   - Outcome readings require T2c and SR-K before NOT_UV_RESIDUAL (K8).
   - NGC N0–N4 name their sites and run as replays on the saved T120L operator.
8. **Cost (§6).** About 77 CPU-h of V007 runs plus replays, and up to about 93 CPU-h with the pre-named contingencies. Effort is about 4 lane-days to implement and 2–3 to review. All estimates are UNTESTED.

---

## 0. Finding → resolution map

| finding | sev | resolution (where) | status after V002 |
|---|---|---|---|
| **K1** T1 drops V005 contraction; no C4T vs higher-K tail run | MATERIAL | (a) T1 = V005 `criterion.shape_pass` verbatim on (C2T, C3T, C4T): D̂_T(3,4) ≤ 1 AND D̂_T(3,4) ≤ 0.5·D̂_T(2,3). D14 handled explicitly as the pre-named FLOOR_LIKE outcome (no floor clause). (b) New T1-H: C6T (grid G6, K = 6, production tail) vs C4T, per row \|Δv_i\| ≤ τ_i/2 under the decidability rule. (c) T2c promoted to pass/fail at τ_i/2 (§5.3) | design closed; outcome UNTESTED |
| **K2** "same K→∞ limit" contradicted by V-c2 | MATERIAL | §1.4 states the limit object Φ_∞[S_T] = the field of the registered smooth source (stars: f5becd45 profile; gas: the declared rule), with the exact decomposition Φ_K = Φ_∞ + b_K + r_K. b_K (in-cube discrete-minus-smooth source, true symbol) is measured by SR-K (static, K = 2, 3, 4 on saved R3 states; deciding test as the check asked). §7 classification is re-argued from Φ_∞, not from a packet limit | argument restated; b_K magnitude UNTESTED (SR-K) |
| **K3** lapse pair ungated | SIGNIFICANT | Gate B3 (§4.5) against an independent Cartesian implementation by a different lane: E1 jets and lapse pair at route-A column points (8 azimuths, z to 32 kpc); reference and body angular reads, taken by tap on the real successor stages; column `potential(z)`; the facade's midplane ratio; bd(0) ≡ 0. A B3 failure is IMPLEMENTATION_DEFECT before any T run | gate specified; UNTESTED |
| **K4** NGC N-test evaluator missed | MODERATE | §2.4 lists five sites (replay_c1 `c4a8cd02` L79–93/105–106, kg_lib `06333714` L193–201, ringeval `5149ea29` L23/31, dsplit_sphere `a4390c6a` L34/46, launcher run_p23 `3578e83c` L19/59–70); §3.7 gives the four successors; §6 costs them | design closed |
| **K5** nodes_v001 source wrong at fs stages | MODERATE | §1.3: at fs columns v001 and fs rotation v001, S_pkt(G6∖G4) = prep analytic J₀ stars + the offset's Cartesian forward sum of body16 (gal_c2v005 offset L238–246 arithmetic, m = 16 included). New gate T2-I checks the transform replicas against C6's own stored packet sources | design closed; T2-I UNTESTED |
| **K6** RB not a row bound; ε sampled | MODERATE | §1.5: RB renamed **SRB-ROT** (static rotation channel, necessary, not sufficient). New **RB-FP** = 2·ε_cert·\|∂v_i/∂λ\|·κ_i (AMP run C4T-A measures the full fixed-point sensitivity through column, K0 and Picard channels; κ_i is the static cross-shell cancellation factor). ε_cert is a refined sample, labelled an estimate | gate specified; UNTESTED |
| **K7** τ/4 at Picard tolerance; numerics mismatch | MODERATE | §5.2 pairing rule: (i) C4T-D6 numerics byte-equal to the C6 call actually admitted (brackets incl. any D7 recovery block, Picard, route_a); (ii) each paired test is DECIDABLE only if the pair noise allowance E_i ≤ τ_i/8 on every row and the route-A accepted iteration and Picard pass counts match; (iii) otherwise the pre-named R-PAIR refinement (both members rerun with their own prefixes, Picard passes 12, bound 0.0025 km/s; for count mismatch, both with route-A source_rtol/10). Thresholds themselves are unchanged (A28's τ/4 for T2) | design closed |
| **K8** outcome 2 over-reads | MODERATE | NOT_UV_RESIDUAL requires T1 fail AND T2c ≤ τ_i/4 AND SR-K K-dependence ≤ τ_i/4. Otherwise SOURCE_REPRESENTATION_K_DEPENDENT, next step the fixed-point SR runs under their own prereg (§5.5) | design closed |
| **K9** tail-OFF identity gated only at planning | MINOR–MODERATE | B0′ (§4.2): v010 tail-OFF **simulate** on saved outdirs, and one prefix-admitted rerun of the v009-GEO deciding-(i) spec `4ac5527a`. Result bytes must equal each parent's, except a declared per-parent difference list | gate specified |
| **K10** B1 reference from another lineage | MINOR | §4.3: the B1 reference is DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001 (result `883b37a0`). It is gal_c2v004 lineage, its SPEEDS are rows-equal to A2F10, and its RA arrays are bitwise equal to the serial anchor (COMPARE_DECIDING_II `e1d3c072`, PASS_BITWISE_EQUAL). Precondition: gal_c2v005 deciding (i) PASS against v008's `b76f7afc`. Fallback: run Z2-OFF (v010 tail OFF, same spec) as a same-lineage reference | design closed |
| **K11** extra exact-zero refusal | MINOR | §1.2 requirement R0: bd = Σ G·expm1(ik_z z), so bd(0) ≡ 0.0. HI v003:67–68 and facade L38–40 are listed as refusal sites (§2.1). Unit test in B3. Synthetic check S1/S2 (TESTED): 0/2000 nonzero with expm1. A reordered plain difference was nonzero in 1554/2000 trials, so the requirement is load-bearing | requirement TESTED synthetic; in-code UNTESTED |
| **K12** NGC quadrature violates the phase rule | MINOR | §1.2: R_src,max and z_src,max are defined (gas support; stellar last node + 12a; sech² 24h; discrete gas element heights bounded by the search limit, checked fail-closed at build). Revised widths: DDO w⊥ 0.05, w_z 0.02 (1.415 / 1.34 rad); NGC w⊥ 0.0050, w_z 0.0070 (1.365 / 1.40 rad). V001's NGC w⊥ also violated the rule (0.0055 × 272.98 = 1.501; Errors register) | arithmetic TESTED here |
| **K13** route-A tail source not monitored | MINOR | §1.7: per-iteration M_T (the static rotation-channel effect of t[S_T(updated_n)] − t[S_T(gas_n)] at the 12 row radii × 8 azimuths, in τ units) is written to the sidecar. Threshold M_T(accepted) ≤ 1/4, else the pre-named flag TAIL_SOURCE_UNDERCONVERGED. The stopping rule is unchanged | design closed |
| **K14** lapse-only TESTED only on (2,4] | MINOR | §1.6: the claim is restated as TESTED to 4 /kpc and UNTESTED beyond. Certificate LO on shells (4,5], (5,6], (6,8], (8,12], (12,16], (16,32] (and (32,64] for T3) on the saved C4R3 state, using Claude3's method (origin_c3v001 `37412b9a`, shell_resolved_c4_c3v001 `1566f24c`). Pass: ≤ 0.005τ per shell and ≤ 0.05τ summed | gate specified |
| **K15** NGC memory | MINOR | §1.2 streaming: corner tables per radius, LRU of 16 radii (NGC ≤ 0.19 GB, DDO ≤ 0.04 GB). Ring tables ≤ 0.23 GB. Tail cap 0.6 GiB per process. Jₙ calls ≈ 3e7 (NGC route A) | estimate (UNTESTED) |
| **K16** NGC_CODE lineage | MINOR | §3.6: tail OFF keeps v009's NGC_CODE (v001 `1b95a4ff`/`9e9caf83`), so B0 stays identical. Tail ON plans NGC_CODE_UVT (successors of worker v002 `42bdd23e`, parallel `5f16525a`, binding v002 `cc5db369`, the lineage of the live packet `ngc_f10_c2/route_a_f10/LAUNCH.json` `d70cbcfe`) and writes the declared plan difference `ngc_code_lineage_swap` | design closed |
| **N1** offset tail is diagnostic; its C is the mask | note | §1.1: the per-stage C table now names the offset (D = O ∖ mask), body (O ∖ cube) | closed |

---

## 1. The tail-corrected lapse

### 1.1 Definition (V001 §1.1 kept; per-stage C restated, N1)

The definition is V001's, unchanged:

  δn_T(x) = packet_K(x) + t(x),  t(x) = ∫_D T∞(k) S_T(k) e^{ik·x} d³k/(2π)³,  T∞ = 1/(4γ_eff|k|²),  D = O ∖ C.

**Per-stage kept region C** (derived by the driver, never supplied by the caller):

| stage | C | reason |
|---|---|---|
| route A, reference, body | cube [−K, K]³, always | v009-EXT L483–491: these run unmasked |
| offset t[Δ] | the stage mask: cube, sphere \|k\| ≤ K, or cylinder | the offset response is masked (`_wrap_cache`, L629). N1: diagnostic only, since nothing downstream reads its real-space total |
| fs/rfs/LE columns and rotations | the stage mask | `truncation_mask` L478 |

**O, the outer region.**
- Production: the cylinder {k⊥ ≤ K_big, |k_z| ≤ K_big}.
- T2c and B2/B3: the cube [−K_out, K_out]³, declared per test.

### 1.2 Evaluator E1 (V001 §1.2 kept), with five changes

**(a) Real output.** k_z ≥ 0 is stored. Every ring and corner contraction returns t = G(0) + 2·Re Σ_{k_z>0} G e^{ik_z z} as float64.
- The imaginary part is exactly 0, so the reality guards at line v002 L54–59 and L89–92 see nothing new.

**(b) R0: the lapse-pair requirement (K11).**
- b0 = t(x, y, 0).
- bd = 2·Re Σ_{k_z>0} G·expm1(ik_z z), plus the k_z = 0 node, whose expm1(0) term is exactly 0.
- Therefore bd(z = 0) ≡ 0.0. The facade's midplane log ratio (line v002 L86–97) is then exactly 0.0, and HI v003 L67–68 does not raise.
- t(z) − t(0) as a subtraction of separately evaluated sums is forbidden.
- TESTED synthetically (S1, S2: 0 of 2000 trials nonzero). The in-code unit test is part of B3.

**(c) Phase rule with defined source extents (K12).** The panels must satisfy:

  w⊥·(R_eval,max + R_src,max) ≤ 1.5,  w_z·(z_eval,max + z_src,max) ≤ 1.5

**Source extents:**
- R_src,max = max(gas support radius; stellar or H₂ last node + 12a), where a is the outer exponential scale. The weight beyond that point is e^{−12} = 6e-6.
- z_src,max = max(the declared bound on discrete gas element |z|; 24h for sech²).
- Gas element heights are checked at every build against the declared bound. Exceeding it raises `UV_TAIL_SOURCE_OUTSIDE_DECLARED_EXTENT`, so a column outside it becomes a recorded failure, never a silent value.
- Panels per interval = ⌈length / w_max⌉, uniform within the interval.
- The panel breaks are as in V001.

| galaxy | K | O | o | w⊥,max | w_z,max | R_eval,max / R_src,max (kpc) | z_eval,max / z_src,max (kpc) | phase ⊥ / z (rad) | N⊥ × N_z⁺ |
|---|---|---|---|---|---|---|---|---|---|
| DDO154 | 2, 3, 4, 6 | cyl K_big = 32 | 8 | 0.05 | 0.02 | 14.2 / 14.102 (gas support; stars 1.501 + 12·0.358 = 5.80) | 35 / 32 (route-A search limit; stars 24h = 1.18) | 1.415 / 1.34 | 5,128 × 12,800 |
| NGC3198 | 2 | cyl K_big = 16 | 8 | 0.0050 | 0.0070 | 136.5 / 136.485 (gas support; stars/H₂ 21.42 + 12·3.398 = 62.2) | 105 / 95 (free-boundary end; sech² 24h = 11.2) | 1.365 / 1.40 | 25,608 × 18,288 |

- The source extents were read from GALAXY_RADIAL_SOURCE_REFERENCE_V001 `f5becd45` (TESTED arithmetic).
- Doubling certificate, prereg-fixed:
  - (w/2, o + 4) changes the static rows on the saved C4R3 le3 state by ≤ τ_i/20 (DDO);
  - the same change moves the lnN reads on saved T120L by ≤ θ/20 (NGC).

**(d) Streaming of the corner tables (K15).**
- The corner harmonics G_{R,j}^{(d)}(k_z) live only on |k_z| ≤ K. They are built per evaluation radius on first use and held in an LRU of 16 radii.
- The corner source block M_c (N_c × N_kz,K) is built once per state.

| item | DDO (K = 4, reference 360 R) | NGC (K = 2, 205 R) |
|---|---|---|
| ring tables G_R^{(0,1,2)}, all radii | 360 × 12,800 × 3 × 16 B = 0.22 GB | 205 × 18,288 × 3 × 16 B = 0.18 GB |
| corner table per radius (j_max at R_max) | 31 × 1,600 × 3 × 16 B = 2.4 MB | 107 × 2,288 × 3 × 16 B = 11.8 MB |
| LRU of 16 radii | ≤ 0.04 GB | ≤ 0.19 GB |
| M_c | 272 × 1,600 × 16 B = 7 MB | 1,328 × 2,288 × 16 B = 49 MB |
| Jₙ libm calls per state | ≈ 4e5 | ≈ 3e7 |

- Cap: tail memory ≤ 0.6 GiB per process. The per-call RSS cap is v009's plus 1 GiB.

**(e) Jet order.** Route A and the NGC N-tests use order 1. Their Hessian slot gets exact zeros, because the only consumers read the fields and gradient: solver L129–150, prediction v005 L62–83 and replay_c1 L79–93. Route B uses order 2.

### 1.3 Tail source rule (V001 §1.3 kept), with the T2 node transforms fixed (K5)

`continuum_v001` (production, T1, T3, NGC) is unchanged: stars from the registered profile, plus the declared cubic-in-s gas rule (M_s 64 DDO, 96 NGC).

**`nodes_v001` (T2 only).** On G6 ∖ G4, S_pkt is computed with the transform the stage's own packet used. Each transform is an exact replica of the cited arithmetic:

| stage | packet source | transform replica (base bytes) |
|---|---|---|
| route A iteration n | fixed + gas_n | stars: prep v007 analytic GL4 J₀ rings (`ac905597` L237–240); gas: `physical_source_fourier` on the iteration's elements (solver `44d9c23c` L187–195), with the mixture coefficients of L215 |
| reference, body | route-A mixture at IT | the same as route A at IT |
| **fs columns v001, fs rotation v001** | amps + offset = stars + **body16** | stars as above + **the offset's Cartesian forward sum** of body `base_integrated_source_J` at `physical_positions_m` (gal_c2v005 offset `1ee18dcd` L238–246: phase e^{−ik·x}, the same wave and position batches). This carries the m = 16 content |
| rfs v003, LE1 v005, LE1 rotation v005 | feedback v002 → stars + rings | the feedback ring J₀ transform (gal_c2v005 feedback v002 `77ac5587`, arithmetic of L231–240 as in V001) |
| LE(n ≥ 2) | feedback v004 → stars + latest rings | feedback v004 (`b3a8424e`) ring transform |

**Gate T2-I.** Each replica is applied to the C6 run's own rosters and compared with the C6 run's stored packet sources on G6 ∖ G4:
- route-A `updated` gas at each iteration (checkpoint);
- offset `new_body_fourier_J`;
- feedback `gas_source_feedback.npz`.

Required: ≤ 1e-12 relative per stage, or the refusal `UV_TAIL_TRANSFORM_REPLICA_MISMATCH`. This replaces the claim that T2 is "exact" with a test.

**I1-T custody** at every build is unchanged from V001 (4096 seeded nodes, ≤ 1e-12, otherwise `UV_TAIL_SOURCE_MISMATCH`).

### 1.4 The limit object and the exact error decomposition (K2)

Define the registered tail source S_T: the f5becd45 stellar (and NGC H₂) profile transformed exactly, plus the declared gas rule on the stage's own column masses and heights. Its field, with the operator's true symbol T(k), is:

  Φ_∞[S_T](x) = ∫_{ℝ³} T(k) S_T(k) e^{ik·x} d³k/(2π)³.

At kept region C (cube K) the scheme is exactly:

  δn_T,K = Φ_∞[S_T] + b_K + r_K + g_K

where:
- **b_K** = Σ_{k∈G_K} w_k U(k)·(S_pkt − S_T)(k) e^{ik·x}. This is the in-cube **source-representation bias**: the discrete roster minus the smooth source, with the true per-node response U.
- **r_K** = ∫_D (T∞ − T) S_T e^{ik·x}. This is the remainder (§1.5).
- **g_K** = Σ_{G_K} w_k U S_T e^{ik·x} − ∫_C T S_T e^{ik·x}. This is the kept-grid quadrature error of the smooth field.
  - Its inner-panel part is what V005's R/C2 inner control measures (D̂_R = 0.0003753, carried).
  - Its outer-panel part is V005 scope S3, UNTESTED. Its deciding test is the order-8 outer-panel case.

**Consequences, stated without the false claim.**
- As K → ∞, δn_T,K does **not** converge at the column nodes, because b_K inherits the discrete roster's missing UV limit (study V-c2). The scheme is a fixed-K hybrid, and K is part of its definition.
- The scheme's target is Φ_∞[S_T]. Its error at the used K is b_K + r_K + g_K.
- T1 tests the K-dependence of the whole hybrid.
- SR-K measures b_K directly (static, §5.4).
- RB-FP and SRB-ROT bound r_K.
- V005's inner control bounds the inner-panel part of g_K. The outer-panel part stays UNTESTED (V005 S3).
- **SR-K** (the deciding test the check asked for):
  - On each saved R3 state (C2R3 `1f6b32a4`, C3R3 `c9c802f4`, C4R3 `aac01962`) and for K ∈ {2, 3, 4}, compute the static rows from packet_K(S_pkt) + t_K and from packet_K(S_T) + t_K.
  - The per-node unit response comes from each case's own saved `01_offset/unit_response.npz`. It depends only on the grid and the frozen background.
  - Report Δ_i(K) and the K-dependence Δ_i(K₂) − Δ_i(K₁) in τ units.
  - The fixed-point SR runs are the pre-named next step if SR-K is material (§5.5).

### 1.5 Remainder: field bound, ε certificate, SRB-ROT and RB-FP (K6)

**Field level (V001 §1.4 kept).** |∂^a r(x)| ≤ Σ_s ε_s B_s^{(a)}, uniform in x (TESTED-POSITIVE by the check).

**ε certificate EPS** (an estimate, not a proven sup):
- Sample q(k) = 4γ_eff|k|²T(k) through the reviewed symbol path: QINF evaluator `f58de0dc`, with the pinned inverse cache `7b9816ae` as cross-check.
- Directions: the 13 lattice-symmetric ones plus 13 midpoint directions. |k|: 64 per decade over each unit shell of [K, K_big].
- Refine (128 per decade, 26 + 26 directions) and require ε_s(refined) ≤ 1.1·ε_s(base). After two failed refinements the certificate is EPS_UNCERTIFIED, which blocks all T runs.
- Coverage: [2, 64] DDO (T3 needs 64); [2, 32] NGC.
- The certificate's sha256 enters each tail config.

**SRB-ROT** (the renamed RB): the static rotation-law channel bound of V001 §1.4. It is **necessary, not sufficient**. Pass: ≤ τ_i/10 on C4T.

**RB-FP** (the full-chain empirical bound):

  RB-FP_i = 2 · ε_max · |∂v_i/∂λ| · κ_i

- **∂v_i/∂λ** = [v_i(C4T-A) − v_i(C4T)]/0.05. C4T-A is C4T with every stage's tail multiplied by λ = 1.05. It is a full fixed point with route A computed, so the column channel, the K0 channel (reference logN0 → body K0, CHECK F1) and Picard amplification are all inside it.
- **κ_i** = Σ_s |ΔV^static_{i,s}| / |Σ_s ΔV^static_{i,s}|. This is the cross-shell cancellation factor of the static tail, from a shell-split static replay on the saved C4T state, in the same shells as EPS. κ_i ≥ 1.
- **The factor 2** is the declared allowance for the fixed-point cancellation pattern differing from the static one.
- **Assumption (DECLARED, UNTESTED):** first-order response in a perturbation of relative size ≤ ε_max (≈6e-4). Pass: RB-FP_i ≤ τ_i/10.
- **Noise:** the AMP pair noise enters as ε·E_i/0.05 ≈ 3e-4 km/s for E_i = 0.025, so the decidability rule is met trivially. It is still recorded.

### 1.6 Lapse-only omission (K14)

- **Status:** TESTED to 4 /kpc. Claude3 measured ≤ 0.005τ per shell on (2,3] and (3,4] (source representation L44; origin V002 L35–38). Beyond 4 /kpc it is UNTESTED.
- **Certificate LO:** the non-lapse tail (components 1–9 of the asymptotic response) is evaluated on the saved C4R3 le3 state:
  - Shells: (4,5], (5,6], (6,8], (8,12], (12,16], (16,32], and (32,64] for T3.
  - Method: Claude3's (origin_c3v001 `37412b9a`, shell_resolved_c4_c3v001 `1566f24c`), extended to these shells.
  - Pass: ≤ 0.005τ per shell and ≤ 0.05τ summed.
  - Fail → NON_LAPSE_TAIL_MATERIAL. A design successor then carries all 10 components, and no T run starts.

### 1.7 Route-A tail-source monitor (K13)

**At each iteration n (solver successor, after L194–196):**

  M_T(n) = max_{i ≤ 12, j ≤ 8} R_i c² |∂_R(t[S_T(updated_n)] − t[S_T(gas_n)])(R_i, φ_j, 0)| / (2 v_i^ref τ_i)

- The probe set is the 12 row radii and the 8 column azimuths.
- v_i^ref is the route-A row speed of A2F10 (`bcd2f64e`, `route_a_rows`), a forward-model output.
- The kept analogue M_K (the same formula on packet_K[updated_n − gas_n]) is recorded next to it.
- Both go to `uv_tail/iteration_%04d.json` in the checkpoint sidecar.

**Threshold and flag.**
- Required: M_T(accepted) ≤ 1/4. Otherwise the run carries the flag TAIL_SOURCE_UNDERCONVERGED.
- A T result from a flagged run cannot produce IMPLEMENTATION_DEFECT or NOT_UV_RESIDUAL readings. It is read as UNDECIDABLE_ROUTE_A_TAIL, with the next step: rerun that case with the route-A seed source_rtol/10.
- The solver's stopping rule (L196–209) is unchanged.

---

## 2. Sites that read the lapse (V001 §2 kept; route B re-based; NGC N-tests added)

### 2.1 Route A (V001 table A1–A17 stands; lines confirmed from bytes where shown)

| # | file (sha8) | lines (read) | slot | what the successor does |
|---|---|---|---|---|
| A1 | DDO prep v007 `ac905597` (v008 `bb05f974`, v009 `b4b27a1d`) | 214–218 zero `boundary` closure | `data['boundary']` | replaced by the binding successor; prep bytes unchanged |
| A3 | DDO binding `d81b24b7` | 38–39 `make_modules`; 86–89, `boundary_jet_at_positions=data['boundary']` at L88 | facade, ca dict | `uv_tail=` into make_modules; L88 receives the TailBoundary; the solver is passed as a `bind_uv_tail` view |
| A4 | facade v001 `2caca496` | **16–19 refusal**; 38–40 zeros into `lapse_difference` | refusal; lapse pair | 16–19 → equality with `tb.jet_for_line(line, z)`; 38–39 → `tb.lapse_pair(line['x_m'], line['y_m'], z, ns)` (R0) |
| A5 | solver `44d9c23c` | 110–112 (`current=fixed+gas` L111, `prepare` L112) | – | `tb.set_state(builder.state(iteration))` between L111 and L112 |
| A6 | solver | 129–150 `metric_point` | `boundary_jet_at_positions` | none (slot) |
| A8 | solver | 187–195 elements; 196 residual; 209–214 return; 215 relaxation | – | collect roster_n at L190–193; M_T after L196; mirror L215; result record at L210–214 |
| A9 | parallel solver `aed4dd59` | 159 `pool.start(column_environment=…)`; 197 current; 216 `pool.begin_iteration`; 313 relax; 784 `start`; 887–893 (V8c-F1); 898 `begin_iteration` | env, per iteration | TailBoundary in env at L159; `uv_tail_state=state.to_arrays()` at L216/L898; V8c-F1 fix verbatim (R-A §6) |
| A10 | HI v003 `b176c7a6` | **67–68 midplane log ratio must be exactly 0.0** | refusal | none; satisfied by R0 |
| A11 | prediction v005 `54136c71` | 62–83 | `boundary(pos)` | none; reads the final bound state |
| A13 | NGC prep v001 `c54c7cc9` | 269–273 closure; 183–250 stars + H₂; 290–295 initial gas | – | as A1, A2 |
| A14 | NGC binding v002 `cc5db369` | 80–83 (L82 `boundary_jet_at_positions`); 110 vertical line | ca dict | as A3, with no facade |
| A15 | line v002 `3a47419d` / v001 `5c0ab4f6` | 46–61 add once; 64–101 `lapse_difference` | the slots | unchanged |
| A16 | HI v002 `665b5589` | 53–61 | – | via A14 |
| A17 | inverse cache `7b9816ae` | 84–86, 114–116 | – | none |

Workers (insertion lines):
- DDO serial `c4cb6826`: argv L36–41; `numerical_controls` L56; identity L95–97.
- DDO parallel `9dbdaf11`: argv L43; L60; L101.
- NGC v002 `42bdd23e`: argv L42; L62; L103.

### 2.2 Route B, re-based on **gal_c2v005** (v010's stage lineage)

Line numbers below were read from the gal_c2v005 bytes. Every slot is the gal_c2v004 line + 7: the gal_c2v004 → gal_c2v005 diffs add +4, +1, 0, +2 and 0 lines in their five hunks, all before line ~130 (TESTED by diff and grep).

| # | stage gal_c2v005 (sha8; v004 base) | read / slot lines | how t enters |
|---|---|---|---|
| B1 | reference worker `cdf155e8` (`dbdbfba1`) | prepared L230–231; zero `boundary` L261–263; `evaluate_radius` L278, boundary arg L281 | build the tail after L231; L261–263 → `TailBoundary(state)` (order 2) |
| B3 | body `7387493b` (`0bf1c4cb`) | prepared L220; zero boundary L248–249; `evaluate_saved_radius` L255; **K0 assembly L261** (F1) | the same roster; refuses unless state digest == reference's (logN0 consistency, body base L65–82); L248–249 → TailBoundary |
| B5 | offset `1ee18dcd` (`e821ae42`) | Cartesian forward sum L238–246; offset inverse L248–256; `fields` reshape and `total` L258; potential L267 | split L258: `if not state.empty: fields[...,0] += t[Δ](pos)` before `total`; C = stage mask (N1) |
| B6 | fs columns v001 `2699cc76` (`bb936834`) | prepared L199; lines L209–210; `potential` L211; `evaluate_line` zeros L214; metric guard L218; `lapse_difference` zeros L219; return L221; `solve_column` L224 | state after L210; L214 jets; L219 `lapse_pair` |
| B7 | rfs columns v003 `1f473e39` (`b20c5152`) | prepared L205; L219; L220; L223; L227; L228; L230; L235 | as B6 (L223, L228) |
| B8 | LE columns v005 `99fab285` (`0fdf435a`) | prepared L206; L220; L221; L224; L228; L229; L231; L236 | as B6 (L224, L229) |
| B9 | fs rotation v001 `a49085e9` (`fd9f51d4`) | prepared L236; `prepare_line` L242; `evaluate_line` zeros L244; metric L248; N L249; Φ L251; Φ_R L252; means L256; rotation law L257 | L244 jets (N, Φ and Φ_R all include t) |
| B10 | LE rotation v005 `be1c913f` (`9b2ded4f`) | prepared L251; L259; L261; L265; L268; L273; L274 | L261 jets |
| B11 | feedback v002 `77ac5587`, v004 `b3a8424e` | no lapse read | no successor |
| B12 | column mean v004 `ae78b012` | no lapse read; producer pin is per-call config | no successor |

### 2.3 Refusals of a nonzero or inexact slot (K11, complete list)

| site | condition | what satisfies it |
|---|---|---|
| facade v001 `2caca496` L16–19 | any nonzero boundary jet | replaced in the facade successor by equality with the tail jet |
| HI v003 `b176c7a6` L67–68 | midplane `log_lapse_ratio_from_midplane != 0.` | R0, bd(0) ≡ 0.0 |
| line v002 L56–59, L84–92 | shape, finiteness, reality | the real float64 tail (§1.2a) |
| line v002 L95–96 | N0 ≤ 0 or ratio ≤ −1 | physical (t ≪ 1); fail-closed as today |

### 2.4 NGC N-test evaluator sites (K4, new)

| # | file (sha8) | lines (read) | what it does | successor |
|---|---|---|---|---|
| NE1 | checker replay_c1 `c4a8cd02` | 79–93 `metric_point` (zero `boundary_*` L81–82, `evaluate_line` L86); 105–106 `lnN` | lnN of the operator at a point | subclass `TailCtx` in `ngc_ring_tail_ctx_c2v001.py`; replay_c1 unchanged |
| NE2 | kg_lib v001 `06333714` | 163–173 `checker` (pins); 193–201 `ctx_with` | builds Ctx with the candidate operator | `ctx_with_tail(cid, label, state)` in the same new file; kg_lib unchanged |
| NE3 | ringeval v001 `5149ea29` | 12 ZK; 23 `ctx_with`; 24 roster; 31 `ctx.lnN` | ring reads at 7 heights | `ringeval_uvt_c2v001.py` (ZK + ±95 for N4) |
| NE4 | dsplit_sphere v001 `a4390c6a` (mask as sphere_info `4f616b14` L22) | 34 `ctx_with`; 46 lnN0 | sphere-masked lnN0 | `sphere_eval_uvt_c2v001.py` (all heights; sphere C) |
| NE5 | launcher run_p23 v001 `3578e83c` | 19 ALLOWED; 59–70 verify and dispatch | allowlist and pins | `run_ntests_c2v001.py` (own allowlist and pins) |
| – | sweep_c1 `b4f7ed62` | `roster(ctx)` | 156 × 32 column positions | unchanged (positions only) |

The saved operator `ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr/` (OPERATOR.json `e6453d52`) is the N-test state. Its stored fixed and initial-gas sources are the I1-T reference. The N-tests are replays: they need no NGC prep successor.

### 2.5 Driver v010 sites (v009-EXT line numbers; the base bytes of v010)

| what | EXT lines | source |
|---|---|---|
| docstring head | 2–15 | merged text naming both parents by sha |
| BIND7 constant | after 150 | GEO hunk `150a143` |
| SCRIPTS route-B pins → gal_c2v005 | 160–170 | GEO hunk `160,170c153,164` |
| SCRIPTS_UVT, AUX_UVT, PARALLEL_ROUTE_A_UVT (new) | after 243 | uv_tail |
| truncation_mask, _install_hooks, _wrap_cache | 478, 568, 629 | read only: `kept_region_for_stage` derives C |
| normalize_route_a_numerics | 708–723 | EXT; `normalize_uv_tail` added after it |
| numerics strict keys | 776 | + `uv_tail` (present only when declared) |
| probe-rule text | 1190–1194 | GEO hunk |
| harmonic diagnostic | 1629–1642 | unchanged (D-m4) |
| GC_SCHEMA V005, galaxy-config pins | 1651–1652, 1658–1661 | GEO hunks |
| ADMISSION_HEAD | 1681 | GEO hunk |
| route_a_custody | 1444ff | + the `uv_tail` digest comparison (UVT_ADMISSION_MISMATCH) |
| D ≠ 4.04 refusal text | 2224–2228 | GEO hunk (the only text conflict with EXT's hunk) |
| route-A request | 2252–2286 | tail ON: worker/solver from AUX_UVT, plus the tail argv |
| **F-A fix** | **between 2309 (`else:`) and 2310** | R-A §6, verbatim: `ROUTE_A_CHECKPOINT_MISSING` Refusal (admitted DDO154, no IDENTITY.json); `ROUTE_A_RESULT_WITHOUT_CHECKPOINT` StageFailed (computed, run mode, outcome present) |
| reference / body / offset requests | 2360 / 2375 / 2383 | + tail argv + route-A sidecar manifest |
| column_pass, fs rotation, fs feedback, RFS, LE loop | 2409–2423, 2489, 2495, 2521, 2529ff | + tail argv for column and rotation kinds |
| result diagnostics / report | 2897, 3036 | + `result['uv_tail']` |
| NGC_CODE | 3598–3606 | unchanged; NGC_CODE_UVT added (K16) |
| ngc_stage_plan | 4033–4043 | tail ON → NGC_CODE_UVT and the `ngc_code_lineage_swap` record |

---

## 3. Final module and file list, with interfaces

**Location.** All new code goes under `claude_artifacts/tail_scheme_impl_c2/` (the implementation lane). Subdirectories: `lib/`, `route_a/`, `stages/`, `driver/`, `ngc_eval/`, `gates/`, `prereg/`, `tests/`.

**Rules.**
- No reviewed byte is edited.
- Every successor is its base bytes plus guarded blocks. With `uv_tail` absent or None, the reviewed body runs unchanged.
- Every module pins its imports by sha256, read from bytes at import.

### 3.1 `lib/owned_uv_tail_lapse_c2v001.py` (≈800 lines; numpy plus the Jₙ provider)

```python
CONFIG_SCHEMA = 'UNT_UV_TAIL_CONFIG_C2V001'
def normalize_config(raw: dict) -> dict
    # strict keys: enabled, outer{shape:'cylinder'|'cube', K_big|K_out (1/kpc)}, source_rule{'continuum_v001'|'nodes_v001'
    # (+ext_grid)}, gas{interp:'lagrange3_s_gl4', M_s}, stars{segment_rule, tail_nodes}, quadrature{order, w_perp_max,
    # w_z_max}, domain{R_eval_max_kpc, z_eval_max_kpc, z_src_max_kpc}, asymptote:'EH_exact_minus_quarter',
    # lapse_only:true, jet_order{route_a:1, route_b:2, ngc_eval:1}, lambda_scale (1.0 except AMP: 1.05),
    # eps_certificate{path, sha256}, lo_certificate{path, sha256}; returns canonical dict; raises Refusal on any other key
def kept_region(stage_kind: str, truncation: dict, K_inverse_m: float) -> dict   # §1.1 table; {'shape','K'}
def domain_is_empty(kept: dict, outer: dict) -> bool                             # cylinder K_big=K over cube K -> True
def build(*, config: dict, kept: dict, roster: 'Roster', gamma_eff: float, c_m_s: float,
          eval_radii_m: np.ndarray, jn_provider, i1t: dict) -> 'TailState'
    # empty domain -> TailState(empty=True), no arithmetic; else ring tables + M_c; checks the phase rule (§1.2c),
    # z_src extent, I1-T record present; raises UV_TAIL_UNRESOLVED_POINT / UV_TAIL_SOURCE_OUTSIDE_DECLARED_EXTENT
class TailState:
    empty: bool; digest: str; record: dict      # config sha, roster digest, kept/outer, quadrature, lambda, eps sha
    def jet(self, pos: np.ndarray, order: int) -> dict    # keys boundary_fields (n,10,1), boundary_gradient (n,10,1,3),
        # boundary_hessian (n,10,1,3,3); float64; component 0 only; order 1 -> hessian exact zeros; empty -> np.zeros
        # with exactly the reviewed shapes/dtypes (prep v007 L214-218)
    def jet_for_line(self, line: dict, z_m: float, order: int) -> dict   # pos = (line['x_m'], line['y_m'], z_m)
    def lapse_pair(self, x_m: float, y_m: float, z_m: float, ns: int = 1) -> tuple   # (b0 (ns,), bd (ns,)); R0
    def value(self, pos) -> np.ndarray; def gradient(self, pos) -> np.ndarray
    def to_arrays(self) -> dict; @classmethod from_arrays(cls, arrays: dict, record: dict) -> 'TailState'
class TailBoundary:                              # picklable; replaces the zero closures
    def __init__(self, state: 'TailState | None' = None, order: int = 2, tap: int = 0)
    def set_state(self, state: 'TailState') -> None
    def __call__(self, pos) -> dict              # == state.jet(pos, order); tap>0 records the first `tap` (pos, jet) (B3 only)
    def jet_for_line(self, line, z_m) -> dict; def lapse_pair(self, x_m, y_m, z_m, ns=1) -> tuple
def field_bound(state, eps_certificate: dict) -> dict      # per-shell B_s^(a), a=0,1,2 (V001 §1.4)
def srb_rot(state, eps_certificate, rows: dict) -> dict    # SRB-ROT per row (§1.5)
def monitor_MT(state_new, state_old, probes: dict, v_ref, tau) -> float   # §1.7
```

### 3.2 `lib/uv_tail_source_roster_c2v001.py` (≈450 lines)

```python
class Roster: stars: 'StarsProfile'; gas: 'GasColumns'; provenance: dict; def digest(self) -> str
def stars_registered(profile_record: dict, galaxy: str, components: tuple, *, segment_nodes_rule, tail_nodes) -> 'StarsProfile'
    # f5becd45 via galaxy_baryonic_source_forward_v002 (e9be043b) L43-58; NGC H2 = prep v001 L212-241 radial form without the
    # GL4 tail-mass normalization; P_*(k_perp) doubling-certified to 1e-10
def gas_columns(positions_m, integrated_J, *, radial_nodes_m, rdr_weights_m2, s_edges_kpc2, M_s) -> 'GasColumns'
def roster_route_a(stars, init_rings, element_rosters: list, mixture: list) -> Roster   # mirrors solver L215
def roster_body(body_arrays: dict, stars) -> Roster                                       # body_arrays base_integrated_source_J
def roster_rotation(rotation_arrays: dict, stars, rule: 'feedback_v002'|'feedback_v004') -> Roster
def source_continuum(roster, k_perp, k_z) -> np.ndarray        # S_T (continuum_v001)
def packet_transform(roster, waves, kind: str) -> np.ndarray   # kind in {'prep_analytic_j0','physical_source_fourier',
    # 'offset_cartesian_v003','feedback_ring_j0_v002','feedback_ring_j0_v004'} -- exact replicas (§1.3)
def check_represented(roster, waves_sample, packet_sample, kind, rtol=1e-12) -> dict    # I1-T; UV_TAIL_SOURCE_MISMATCH
```

### 3.3 `lib/posix_libm_bessel_jn_provider_c2v001.py` (≈70 lines)

- Successor pattern of `posix_libm_bessel_j0_provider_v001` (`c7c93416`).
- Functions: `j0(x)`, `j1(x)`, `jn(n, x)`, vectorized over float64 arrays.
- `custody()` returns the libm path, its sha256 and the platform.

### 3.4 Certificates and replays: `gates/`

| file | signature | inputs → outputs |
|---|---|---|
| `cert_eps_c2v001.py` | `main(--K, --K-big, --galaxy, --coefficients, --out)` | QINF evaluator `f58de0dc`, A2 grid `2e3a36d8` → `EPS_CERT_*.json` (ε_s per shell, base and refined, verdict) |
| `cert_lo_c2v001.py` | `main(--state C4R3, --shells, --out)` | the saved C4R3 le3 state, the asymptotic full response → `LO_CERT.json` (per-shell τ, sum, verdict) |
| `sr_k_static_c2v001.py` | `main(--states C2R3,C3R3,C4R3, --K 2,3,4, --out)` | saved unit_response.npz and le3 states → `SR_K.json` (Δ_i(K) and pairwise) |
| `shell_split_static_c2v001.py` | `main(--state, --shells, --out)` | the saved C4T state → κ_i (RB-FP) |
| `rb_fp_c2v001.py` | `main(--c4t, --c4t-a, --kappa, --eps, --out)` | → `RB_FP.json` |
| `t2i_transform_replica_c2v001.py` | `main(--c6-run, --out)` | C6 rosters and stored sources → `T2I.json` |
| `b0_plan_identity_c2v001.py`, `b0p_result_identity_c2v001.py`, `b0_fa_cases_c2v001.py`, `b1_empty_domain_compare_c2v001.py`, `b2_static_rows_c2v001.py`, `b3_lapse_pair_independent_c2v001.py` (independent lane), `doubling_cert_c2v001.py` | §4 | each gate's JSON record |

### 3.5 Route-A successors (`route_a/`)

| file | base (sha8) | interface change | insertion slots (base lines) |
|---|---|---|---|
| `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py` | `44d9c23c` | `solve(**reviewed, uv_tail=None, uv_tail_builder=None, uv_tail_sidecar=None)`; `bind_uv_tail(module, tb, builder, sidecar) -> view` (`__file__` = successor file) | L111/112 set_state; L190–193 roster collect; after L196 M_T; L210–214 result `uv_tail`; L215 mixture mirror; resume: sidecar digest == rebuilt (UV_TAIL_RESUME_MISMATCH) |
| `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py` | `aed4dd59` | as above, plus `pool.begin_iteration(..., uv_tail_state=…)` | L159, L197, L216, L313, L784, L898; **V8c-F1 fix at L887–893** (R-A §6 text) |
| `owned_stable_lapse_hi_facade_uvtail_c2v001.py` | `2caca496` | `make_modules(*, line_module, hi_module, reality_atol, reality_rtol, uv_tail=None)` | L16–19 equality check; L38–39 lapse pair |
| `ddo_composite_stable_cached_binding_v002_uvtail_c2v001.py` | `d81b24b7` | `+ uv_tail_config, eps/lo certificates`; builds TailBoundary and builder | L38–39, L88, L30 (solver pin = successor) |
| `ddo_composite_stable_cached_root_worker_v002_uvtail_c2v001.py` | `c4cb6826` | argv `--uv-tail-config/-sha256 --eps-certificate/-sha256 --lo-certificate/-sha256` (required) | L36–41, L56 (`numerical_controls['uv_tail']` = digest), L95–97 |
| `…_root_worker_v002_parallel_uvtail_c2v001.py` | `9dbdaf11` | the same | L43, L60, L101 |
| `ngc_composite_full_coupled_binding_v002_uvtail_c2v001.py` | `cc5db369` | as the DDO binding, no facade | L80–83 |
| `ngc43_composite_coupled_root_worker_v002_uvtail_c2v001.py`, `…_parallel_uvtail_c2v001.py` | `42bdd23e`, `5f16525a` | the same argv | L42, L62, L103 |

Unchanged: prep v007/v008/v009, NGC prep v001, composite adapter `75092cf6`, line v001/v002, HI v002/v003, checkpoint `069b3935`, prediction v005, inverse cache.

### 3.6 Route-B successors (`stages/`, 8 files, `<base>_gal_c2v005_uvt_c2v001.py`)

- **Bases:** reference `cdf155e8`, body `7387493b`, offset `1ee18dcd`, columns v001 `2699cc76`, v003 `1f473e39`, v005 `99fab285`, rotation v001 `a49085e9`, v005 `be1c913f`.
- **Slots:** the §2.2 lines.
- **New required argv:** `--uv-tail-config/-sha256 --eps-certificate/-sha256 --lo-certificate/-sha256`. Reference, body and offset also take `--route-a-tail-manifest/-sha256`.
- **start.json** adds `uv_tail`: config sha, roster digest, I1-T record, kept/outer and state digest.
- **finish.json** adds the state digest, plus SRB-ROT for the rotation stages and `eval_domain_max`.
- **Refusal:** a successor refuses to run without a tail config.

### 3.7 Driver v010 (`driver/galaxy_m0_forward_c2v010.py`)

- **Base:** v009-EXT `999331af`.
- **Merge:** the v008 → v009-GEO hunks (`stage_successor_gal_c2v005/driver/DIFF_V008_V009.diff`) are re-applied at the §2.5 EXT lines. The only overlap is the docstring and the D ≠ 4.04 text.
- **Added:** the F-A fix (§2.5) and the `uv_tail` block (V001 §3.4 keys plus `lo_certificate`, `jet_order`, `lambda_scale`).
- **Tail OFF:** normalization and planning are exactly the merged v009 (B0).
- **Tail ON:**
  - writes and pins `inputs/uv_tail_config.json`;
  - SCRIPTS_UVT / AUX_UVT;
  - threads the route-A tail manifest;
  - refuses admission of any route A or prefix with a different `uv_tail` digest;
  - `result['uv_tail']`;
  - the dry-run tail table;
  - NGC: NGC_CODE_UVT and the `ngc_code_lineage_swap` record `{from: NGC_CODE v001 pins, to: v002-based successors, evidence: route_a_f10/LAUNCH.json d70cbcfe}`.

### 3.8 NGC evaluator successors (`ngc_eval/`)

```python
# ngc_ring_tail_ctx_c2v001.py  (imports replay_c1/sweep_c1 only through kg_lib.checker(), pins verified)
class TailCtx(replay_c1.Ctx):
    def __init__(self, tail_boundary: TailBoundary)            # order 1
    def metric_point(self, R, phi, z)  # = replay_c1 L79-93 with b = self.tb(pos); the line cache L83-85 unchanged
def ctx_with_tail(cid: str, label: str, state: TailState, mask: 'cube'|'sphere' = 'cube') -> tuple   # kg_lib L193-201 + sphere mask (sphere_info L22)
def ngc_iter0_roster(prep_json: dict, ops_dir) -> Roster      # stars+H2 registered + razor-thin initial gas; I1-T vs ops fixed/initial sources
# ringeval_uvt_c2v001.py  GRID LABEL RS RE --tail-config CFG --tail-sha SHA [--z95] [--store-kept]   (ringeval L23-35 loops)
# sphere_eval_uvt_c2v001.py  same argv, sphere-masked operator and sphere C
# run_ntests_c2v001.py  allowlist {ringeval_uvt, sphere_eval_uvt}; verifies every pin from bytes; writes ngc_eval/out/
```

### 3.9 Prereg tools (`prereg/`)

- `make_kmax_tail_prereg_v007.py` builds the sealed JSON from the draft.
- `kmax_tail_compare_c2v007.py` implements §5 mechanically: statistics, decidability, outcomes, carried u_i.
- `tests_kmax_tail_compare_c2v007.py` exercises every outcome branch on synthetic results.

---

## 4. Identity and validity gates (all before any T result is read)

### 4.1 B0: planning identity against both parents

- v010 runs with the tail OFF in dry-run on:
  - the v009-EXT spec set: V005 and V006 R1 specs, G5/G6, `max_iterations`;
  - the v009-GEO set: the D test specs, `2029f26a`, `4ac5527a`, A2F10, A2F10_RA8;
  - the NGC templates.
- **Against EXT:** requests, inputs and normalized specs must be byte-identical after the declared GEO pin-substitution map (11 stage pins, schema V005, 3 galaxy configs, admission head, 2 record texts).
- **Against GEO:** byte-identical after the declared EXT map (G5/G6 acceptance, prep v009 selection, `max_iterations`).
- The method is gal_c2v005 CHECK's CMP_DRY. The verdict is PASS_PLAN_IDENTICAL, with the two maps recorded.

### 4.2 B0′: result identity of post-processing (K9), and B0-FA

**B0′-SIM.**
- v010 (tail OFF) and each parent run in **simulate** mode on the saved outdirs:
  - A2_ANCHOR_F10 (`bcd2f64e`);
  - DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008 (`883b37a0`);
  - KMAX C4R3 (`aac01962`);
  - the deciding-(i) outdir once it is complete.
- result.json must be byte-equal to the parent's, except for the declared driver-custody field list (driver path and sha, stage-pin custody under the substitution map).
- This covers result assembly, comparators, the harmonic diagnostic and `ngc_route_b_table`.

**B0′-RERUN.**
- One prefix-admitted rerun of spec `4ac5527a` under v010, tail OFF. It admits CODEX1 V002 route A, reference and body; that pair is IDENTITY-bearing, so F-A is not reached.
- result.json must equal v009-GEO's deciding-(i) result, except the declared custody fields.
- Cost: about 1.2 h, route-B only.

**B0-FA.**
- R-A's F-A cases A1, A2 and A4 (review_driver_v008_c4 verify tree) end REFUSED (`ROUTE_A_CHECKPOINT_MISSING`) under v010.
- The D = 4.04 default-path identity is unchanged: B0 against GEO.

### 4.3 B1: code-path identity on an empty domain (K10)

- **Run Z2:** v010, tail ON, `outer.K_big = K = 2` (cylinder over cube, so D is empty). A2F10 C2, serial route A (A23), gal_c2v005-uvt successors.
- **Reference:** DDO154_A2F10_ROUTE_A_PARALLEL_N8_C2V008_DECIDING_RUN_V001.
  - result `883b37a0`, gal_c2v004 lineage, driver v008;
  - COMPARE_DECIDING_II `e1d3c072`: PASS_BITWISE_EQUAL, with RA_ARRAYS equal to the serial A2F10 and SPEEDS rows-equal.
- **Precondition L:** gal_c2v005 deciding (i) (DDO154_ROUTE_B_C2V009_DECIDING_ADMIT_PREFIX_RUN_V001, spec `4ac5527a`) is PASS_BITWISE against v008's `b76f7afc`. It is running now, so this is UNTESTED.
- **Compare:** the method of compare_deciding_ii_c2v008 (`b122b8e6`), extended to every route-B stage's arrays.
  - All route-A blobs, records and arrays must be equal, and every stage npz equal.
  - Rows and speeds equal.
  - Differences allowed only in the declared custody list: stage script pins → uvt successors, worker/solver pins, `numerical_controls.uv_tail`, driver sha, and the `uv_tail` records.
- **Empty-domain rule** (TESTED synthetically, S3: −0.0 + 0.0 changes bytes): where the reviewed code passes zeros (every slot), the empty state returns the reviewed np.zeros exactly. Where the reviewed code performs no addition (the offset `fields`, L258), the successor skips the addition.
- **Fallback when L fails or is unavailable:** Z2-OFF (v010, tail OFF, same spec, about 2 h) becomes the same-lineage reference, and L's failure is reported separately.

### 4.4 B2: static rows against an independent implementation

- On the saved C2R3, C3R3 and C4R3 le3 inputs, the rotation-v005 successor with the unchanged column mean gives static rows. The tail config is continuum_v001 with O = cube K_out = 12, so that a Cartesian check is affordable.
- Those rows must equal a checker's Cartesian tensor-GL implementation (box(12) ∖ cube(K), full box with no symmetry reduction, at the 16 azimuths) to ≤ 1e-4 km/s per row.
- **Sanity:** within the m = 16 alias plus the star-roster difference (≤ 0.05 km/s) of the study's ADV_TAIL_CHECK KB12 rows (`adv_tail_check_v001` `67a6eeb6`).

### 4.5 B3: lapse pair, jets and column potential, independent (K3, K11)

**Independence.**
- The implementation is written by another lane (Claude3 or Claude4).
- It may not import the tail library or roster module.
- It rebuilds S_T from the registered profile and the saved roster.
- It integrates on the full Cartesian box(K_out = 8) ∖ cube(4) with tensor GL, doubling-converged to ≤ 1e-10 relative.
- E1 is configured with O = cube 8.

**State:** the saved C4R3. Its route-A accepted iteration and le3 rotation inputs supply the roster and points.

| check | points | tolerance |
|---|---|---|
| value, gradient, Hessian | route-A column points: 72 R × 8 φ × z ∈ {0, 0.01, 0.05, 0.2, 1, 5, 20, 32} kpc | 1e-8, 1e-7, 1e-6 × the max of the respective tail quantity |
| lapse pair (b0, bd) | the same points | 1e-8 × max\|t\| |
| **bd(z = 0)** | all column points at z = 0 | **== 0.0 exactly** |
| facade midplane ratio | the facade successor driven on 8 columns with the real solver `metric_point` | == 0.0 exactly at z = 0; HI v003 L67 passes |
| reference and body angular reads | taken by `TailBoundary(tap=4096)` on the real reference/body successors replayed on the saved C4R3 prefix | 1e-7 × max\|∇t\| |
| column `potential(z)` | fs-columns successor potential at 72 columns × 8 z | 1e-7 × max\|tail potential difference\| |
| imaginary part | all | == 0.0 exactly |

A B3 failure is IMPLEMENTATION_DEFECT. No T case is launched.

### 4.6 Other pre-run certificates

- **EPS** (§1.5) and **LO** (§1.6).
- **Doubling certificate** (§1.2c).
- **I1-T** at every build, and **T2-I** before T2 is read.
- **SRB-ROT** ≤ τ_i/10 on C4T.

---

## 5. Prereg V007 draft (summary; `KMAX_TAIL_PREREG_V007_DRAFT.json` is authoritative)

### 5.1 Fixed for all tests

- Anchor A2F10 and the DDO seed of V005; grids G2/G3/G4 as in V005, and G6 as in V006 R1.
- τ_i, D̂ and the V005 gates V1–V6, all from V005 `dbddc02c`.
- The Picard **validity** gate is V005 V2: final-pass max_abs_change ≤ 0.0125 km/s.
- Brackets: the D7 R3 block `7946b857`, with the pre-named W1 widening applied at most once.
- Route A is computed in every T run, serial in wave 1.
- Production tail: continuum_v001, cylinder K_big = 32, the §1.2c DDO quadrature, M_s = 64. EPS and LO shas go in the config.

### 5.2 Pairing and decidability rule (K7: thresholds separated from the Picard gate)

For any paired comparison P = (a, b), the rule is applied per row.

**Noise allowance.**
- E_i(run) = |Δ_i,last|·q̂/(1 − q̂), where q̂ = min(0.9, |Δ_i,last|/|Δ_i,prev|) is taken from the run's last two Picard passes (observe_every_pass), and E_i = |Δ_i,last| if there is only one pass.
- E_i(P) = E_i(a) + E_i(b).

**Decidability.**
- P is **DECIDABLE** iff E_i(P) ≤ τ_i/8 on every row, the route-A accepted iterations are equal, and the Picard pass counts are equal.
- When decidable, the test's own threshold applies unchanged.

**Otherwise R-PAIR.**
- Both members are rerun admitting their own route A, reference and body, with picard.passes 12 and bound 0.0025 km/s.
- For an iteration-count mismatch, both are rerun from route A with the seed source_rtol/10.
- This happens at most once. Still undecidable → UNDECIDABLE_AT_ITERATION_FLOOR, reported, and the test does not pass.

**T2 numerics.** C4T-D6's numerics are byte-equal (canonical JSON) to those of the C6 call admitted under V006: brackets including any D7 block, picard, route_a and column_workers. Only `composite_grid_spec` and `uv_tail` differ.

### 5.3 Tests

| test | runs | statistic | pass |
|---|---|---|---|
| **T1** (V005 `shape_pass`, verbatim) | C2T, C3T, C4T | D̂_T(2,3), D̂_T(3,4) | D̂_T(3,4) ≤ 1 **AND** D̂_T(3,4) ≤ 0.5·D̂_T(2,3) |
| **T1-H** (higher K) | C6T vs C4T | per row \|Δv_i\|/τ_i | ≤ 1/2 on every row (decidable) |
| T1-S (shape) | S4T vs C4T | max \|Δv_i\|/τ_i | ≤ 2 (V005 `tau_shape_agreement`) |
| **T2** (wiring and Q∞ substitution) | C4T-D6 (nodes_v001 on G6∖G4) vs direct C6 | per row \|Δv_i\|/τ_i | ≤ 1/4 (A28), decidable; needs T2-I |
| **T2c** (rule effect) | C4T-C6c (continuum, O = cube 6) vs C4T-D6 | per row | ≤ 1/2, **pass/fail**; fail → SOURCE_RULE_MATERIAL |
| T3 (K_big) | C4T-K16, C4T-K64 vs C4T | per row, each pair | ≤ 1/4, decidable |
| RB-FP | C4T-A vs C4T, plus κ, ε | RB-FP_i | ≤ τ_i/10 |
| SR-K (reported, enters readings and u_i) | static replays | Δ_i(K), pairwise | reported; flag SOURCE_QUADRATURE_MATERIAL if max_i \|Δ_i(4)\| > τ_i |
| D-m4 (reported) | C4T vs C4R3 | v009 harmonic diagnostic m4 | reported |

### 5.4 Decision rule

ADOPT_TAIL (cube, K = 4, C4T) requires all of:
- B0, B0′, B0-FA, B1, B2, B3 pass;
- EPS, LO, doubling and I1-T/T2-I pass;
- SRB-ROT and RB-FP pass;
- T1, T1-H, T1-S, T2, T2c and T3 pass;
- no flag left unruled.

Carried uncertainty, reported with the adoption:

  u_i = |v_i(C4T) − v_i(C3T)| + |v_i(C6T) − v_i(C4T)| + |v_i(S4T) − v_i(C4T)| + |Δ_i^SR(4)| + RB-FP_i

### 5.5 Pre-named outcomes (first that applies)

1. **Any of B0, B0′, B0-FA, B1, B2, B3 fails** → NO_RUN; the failure is IMPLEMENTATION_DEFECT for B2/B3. Next: fix and re-review.
2. **EPS uncertified, LO fails or doubling fails** → NUMERICS_UNCERTIFIED (respectively NON_LAPSE_TAIL_MATERIAL). Next: the named successor.
3. **T2 decidable and fails** → IMPLEMENTATION_DEFECT. Stop; T1 and T3 are not read as physics.
4. **T2c fails** → SOURCE_RULE_MATERIAL. Root ruling on the gas rule before adoption.
5. **T3 fails** → KBIG_NOT_CONVERGED. Production moves to K_big 64 under T3′ (32/64/128); needs EPS and LO to 128.
6. **RB-FP or SRB-ROT fails** → BOUND_INSUFFICIENT. Next: a q-corrected shell (the second asymptotic order) under a design successor.
7. **T1 fails:**
   - **NOT_UV_RESIDUAL** only if T2c ≤ τ_i/4 on every row AND max_i |Δ_i^SR(K₂) − Δ_i^SR(K₁)| ≤ τ_i/4 for (2,3) and (3,4) AND no TAIL_SOURCE_UNDERCONVERGED flag. Next: the column/Picard map, with its own prereg.
   - **SOURCE_REPRESENTATION_K_DEPENDENT** otherwise. Next: the fixed-point SR runs C2T-SR, C3T-SR and C4T-SR. These use packets over the smooth source, so that both routes carry one registered representation (A25 direction). They need their own design and prereg.
   - **FLOOR_LIKE** (D14): T1 fails only by the contraction clause, with D̂_T(2,3) ≤ 1 and D̂_T(3,4) ≤ 1. A floor clause needs a new prereg version, decided before any further case runs.
8. **T1 passes, T1-H fails** → HIGHER_K_DISAGREEMENT. Next: adopt nothing; C6T becomes the candidate under a V007 amendment sealed before further results.
9. **T1-S fails** → SHAPE_DISAGREEMENT. Review the per-stage C wiring.
10. **Any test undecidable after R-PAIR** → UNDECIDABLE_AT_ITERATION_FLOOR for that test. No adoption.

### 5.6 NGC3198 N-tests (iteration-0 replays on the saved T120L operator; sites §2.4)

- **State:** `phase23/ops/T120L_hovr` (OPERATOR `e6453d52`), 32 azimuths, θ = 3.3657664138980042e-9.
- **Tail:** continuum_v001, cylinder K_big = 16, the §1.2c NGC quadrature, M_s = 96.
- **K7 does not apply here:** the reads are deterministic, on one operator, with no iteration. The tail quadrature noise is certified ≤ θ/20 (NQ), so θ/4 is five times the certified noise.

| test | evaluator | statistic | pass |
|---|---|---|---|
| NQ | ringeval_uvt at (w/2, o + 4) | Δ of lnN0 and dL | ≤ θ/20 |
| N0 | ringeval_uvt, K_big = K | lnN at the 7 heights, all rings | bitwise equal to `phase23/out/rings/T120L_hovr/*.json` |
| N1 | ringeval_uvt | S = max_φ lnN0 − min_φ lnN0 | S < θ on the 12 TRUNCATION_SHAPE rings (ordinals 1–8, 10, 13–15), C1 as written; C1′ still passes; all 100 reported |
| N2 | sphere_eval_uvt vs ringeval_uvt | per ring and azimuth: lnN0, dL(±10, ±20, ±30) | ≤ θ/4 |
| N3 | ringeval_uvt `--store-kept`, K_big 8 and 32 vs 16 | S/θ and dL | changes ≤ θ/4 |
| N4 | ringeval_uvt `--z95` | e4 at ±95 kpc, cube + tail vs sphere + tail | reported |

N3 reuses the stored kept packet: N = 1. + (n_kept + t), the same arithmetic order as evaluate_line then metric v002 L76. It is therefore exact. NGC fixed points with the tail wait for a valid NGC route-A base (UNTESTED).

### 5.7 Run list

| group | runs |
|---|---|
| DDO gates | Z2 (+ Z2-OFF fallback), B0′-RERUN |
| DDO tests | C2T, C3T, C4T, C6T, S4T, C4T-D6, C4T-C6c, C4T-K16, C4T-K64, C4T-A |
| replays | B2, B3, EPS, LO, SR-K, shell split, doubling, T2-I |
| NGC | NQ, N0, N1, N2, N3, N4 |
| contingent | R-PAIR (≤ 4 pairs) |

- Direct C6 comes from V006.
- Limits: at most 4 processes, serial route A, RSS cap = v009 per-call cap + 1 GiB.

---

## 6. Cost (estimates; UNTESTED)

### 6.1 Tail cost at the revised quadrature

The model is V001 §5.2, at 2 GMAC/s assumed; 30–45 measured in V001's P5.

| item | DDO | NGC |
|---|---|---|
| build per route-B stage | 5,128 × 12,800 × 145 = 9.5e9 MAC ≈ 5 s | – |
| build, reference (360 R) | 2.8e10 ≈ 14 s | – |
| route A per iteration (state + M_T) | ≈ 10 s | 25,608 × 18,288 × 410 = 1.9e11 ≈ 96 s (≈ 6 s at the measured rate) |
| corner tables | per radius ≤ 4e7 MAC | per radius ≈ 1e9 MAC (≈ 0.5 s), 205 radii |
| per evaluation | ≈ 60–150 µs vs 4.4 ms existing (≤ 3.5%) | ≈ 100–250 µs |

### 6.2 Per call and total

| run | estimate |
|---|---|
| C2T / C3T / C4T | ≈ 7,600 / 18,300 / 22,300 s |
| C6T | ≈ 8–15.5 h (C6 7–14 h, A28, + 10%) |
| C4T-D6 | ≈ 7 h (the node packet adds line preparation) |
| C4T-K64 | ≈ 7.1 h |
| other C4T variants | ≈ 6.2 h each |
| Z2, B0′-RERUN | 2.1 h, 1.2 h |
| replays | ≈ 6 CPU-h |
| NGC | ≈ 3 CPU-h (4,992 lines × 0.53 s ≈ 0.74 h per configuration; N3/NQ reuse the stored kept packet) |
| **total** | ≈ 77 CPU-h; ≈ 93 CPU-h with the R-PAIR and Z2-OFF contingencies; ≈ 1.5–2.5 days wall at 4 processes |

**Effort.**
- Library 800 lines, roster 450, provider 70, route-A successors 550, stage successors 480, driver v010 merge about 700 changed lines, NGC evaluator 250, gate tools 1,300, prereg comparator 600, tests 1,800.
- About 4 lane-days to implement.
- About 2–3 lane-days for independent review, including B3's independent implementation.

---

## 7. Classification (restated from Φ_∞, K2; UNTESTED until review)

**What the scheme computes.** At kept K it computes Φ_∞[S_T] + b_K + r_K + g_K (§1.4).

**The case for counted numerics.**
1. **The target is the registered source's field under the operator's own symbol.**
   - The stars use the exact registered profile.
   - The gas rule is exact on the registered quadratic Bernstein Σ at k_z = 0.
   - Nothing is imported: G cancels, there is no Newtonian law and no fitted constant.
   - T∞ is the operator's exact large-k entry (A21).
2. **Each deviation from the target is a numerical error of a named kind, and each is measured:**
   - b_K, the source quadrature of the discrete roster: SR-K, then u_i;
   - r_K, the symbol remainder: EPS, SRB-ROT, RB-FP;
   - g_K, the kept-grid quadrature: the V005 inner control for the inner panels; the outer panels are V005 S3, UNTESTED;
   - the lapse-only omission: LO.
3. **The kept-region symbol is unchanged.** No packet, cache, unit-response or kernel byte changes.
4. **Not the rejected splice.** The asymptote is applied only where |1 − q| ≤ ε_cert.

**The claim withdrawn.** "Same K → ∞ limit as the packet" (V001 §6.1) is withdrawn: the hybrid has no K → ∞ limit at the column nodes, because of V-c2. Convergence in K is replaced by:
- T1/T1-H, which test the K-dependence over 2–6;
- the direct measurement of b_K.

**Declared choices that need review:**
- the gas rule (T2c pass/fail);
- the route-A m = 8j azimuthal projection above K (T2c on DDO; NGC H3 audit);
- the slot semantics: the `boundary_*` slots carry the UV-tail jet, the physical boundary stays zero, and route A records this in its `boundary_prescription`.

**What would make it a model change** (the reviewer's falsifiers):
- b_K material at the adopted K (SR-K > τ without a ruling);
- |1 − q| on D beyond the certificate;
- the gas rule altering column-integrated Σ beyond the mass residual;
- any kept-region byte changing;
- T2 failing.

---

## 8. UNTESTED register (each with its deciding test)

| item | deciding test |
|---|---|
| T1, T1-H, T2, T2c, T3, T1-S outcomes | the V007 runs |
| b_K magnitude and K-dependence | SR-K |
| full-chain remainder | RB-FP (AMP run) |
| ε over [K, K_big], including 6.9–64 /kpc | EPS |
| non-lapse tail beyond 4 /kpc | LO |
| E1 correctness of jets, pair and corner harmonics | B3 (B2 for rows) |
| gal_c2v005 ≡ gal_c2v004 at D = 4.04 | deciding (i) (running) |
| v010 post-processing identity | B0′ |
| tail-source convergence in route A | M_T record |
| razor-thin initial-iterate sheet term (~1/K_big at z ≈ 0) | T3, N3 |
| NGC quadrature at 136 kpc | NQ |
| costs and memory | the first builds (recorded RSS) |
| NGC fixed points with the tail | wait for a valid NGC route-A base |
| outer-panel part of g_K (V005 S3) | order-8 outer-panel case (V005 S3 deciding test) |

---

## 9. Errors register

1. **V001 NGC w⊥ also violated the phase rule.** CHECK K12 named w_z (0.0143 × 105 = 1.5015). Recomputing here with the gas support R_src = 136.485 kpc gives 0.0055 × (136.5 + 136.485) = 1.5014 > 1.5 for w⊥ as well. Both are revised (§1.2c). V001 is unchanged.
2. **V001 named gal_c2v004 stage bases.** v010 carries gal_c2v005 (A29/A30), so every route-B successor and line citation is re-based (§2.2). The +7 offset was read from bytes, not assumed.
3. **V001 placed the implementation lane at `uv_tail_impl_c2/`.** The commissioned lane is `tail_scheme_impl_c2/` (§3).
4. **V001 errors 1–3** carry over unchanged. Its error 3 (lapse-pair check not performed) is now closed by requirement R0 (synthetic S1/S2 TESTED), with the in-code check in B3.
