# TAIL_SCHEME_DESIGN_V001: the tail-corrected lapse for route A and route B, DDO154 and NGC3198 (design only)

tail_scheme_design_c2 lane, 2026-10-18 (UTC). **Design only.** Nothing here is adopted or reviewed, and no production code exists.

**Scope and hygiene.**
- Nothing was launched. No NGC3198 observed or target velocity was opened.
- I read program bytes only, and wrote only under this directory.
- Two synthetic prototypes are in `tools/` (numpy and libm, nice 10, single-thread BLAS, one process). They read no program bytes.
- Hashes are computed from bytes (`HASHES.txt`). The machine twin is `TAIL_SCHEME_DESIGN_V001.json`.

**Decision pins.**
- Frozen decision files: V002 addendum `17c26616`, V003 addendum `5bef6552`.
- The open V004 addendum (A21–A28) is cited by name only. It is not pinned.
- Sealed prereg used: KMAX V005 `dbddc02c` (τ_i and the D̂ statistic).
- V006 is cited by name. At write time the files are the draft `f90ab96c` and R1 `807fc5bf`. T2 pins whichever is sealed.

**Inputs (sha256 prefixes, from bytes).**
- UV_TAIL_STUDY_V001 `41c2dfac` (.md), `63c3f62c` (.json); its CHECK_V001 `10492597` (finding F1 and F2–F8).
- Claude3: 0041 V003 `81d92656`, followup V002 `9e8cc888`, source representation `1d30ead1`.
- QINF_DEPENDENCE_V001 `32a6858a`.
- NGC tier-2 result `ba8ef623` and its prereg `4c2eefeb`.
- Every code file cited in §2 is listed with its sha256 in the JSON twin (`code_pins`).

---

## Answer in brief

1. **Definition (§1).** The corrected lapse is the existing finite packet sum plus t(x).
   - t(x) is the operator's own asymptotic lapse symbol T∞ = 1/(4γ_eff k²) (A21: [pinv Ê]_nn = −1/4 exactly), integrated over the omitted region D = O∖C and applied to the source the field actually carries.
   - It is evaluated pointwise at the true azimuth: m = 0 rings plus the closed-form m = 4j cube-corner harmonics. This makes CHECK F2 (the m = 16 alias) cancel by construction.
   - The source rule: the registered stellar (and NGC H₂) profile, transformed by quadrature of that profile; plus one new gas rule, a cubic-in-s Lagrange interpolant through the four GL4 columns of each annulus. That rule is exact on the registered quadratic Bernstein Σ at k_z = 0. Its numbers are fixed in the prereg.
   - The remainder bound is uniform in x, so it holds at every evaluation point. That fixes CHECK F3.
2. **Every lapse read (§2).** 30 site rows, 17 in route A and 13 in route B. They cover route A (solver, HI facade, prediction, DDO and NGC preparation and boundary closures, both free-boundary HI modules), reference, body (K0, the F1 site), offset, fs/rfs/LE columns, and rotations v001/v005.
   - Feedback v002/v004 and column mean v004 read no lapse. They need no successor; their real-space rings are rebuilt from pinned bytes.
   - All insertions go through additive slots that already exist and already receive zeros: `boundary_*` in `evaluate_line`, `boundary_lapse_*` in `lapse_difference`, and the `boundary_jet_at_positions` callbacks. The only code that refuses a nonzero slot today is the route-A stable facade (v001:16–19).
3. **Modules (§3).**
   - New: the tail library `owned_uv_tail_lapse_v001` and a libm Jₙ provider.
   - Successors: route A (2 solvers, 1 facade, 2 bindings, 4 workers), 8 route-B stages, and driver v010 (successor of v009 `999331af`).
   - Bitwise identity is preserved in two layers. With the tail OFF the plan contains only today's reviewed bytes (test B0). With the tail ON over an empty domain (K_big = K), every successor performs exactly the reviewed arithmetic (x + 0.0) (test B1).
4. **Prereg V007 draft (§4).** Gates T0 (B0, B1, B2) and RB, then tests T1, T2, T3, T1-S and T2c, then the NGC tests N0–N4. Pre-named outcomes are in §4.
5. **Cost (§5).**
   - The tail adds about 5–10% per DDO call: C2T ≈ 2.1 h, C3T ≈ 5.0 h, C4T ≈ 6.1 h, each serial with route A computed.
   - NGC T120L+tail at iteration 0 is about 0.6 h at 4 processes.
   - Parallel route A at N=8 adds ≤ 3% per iteration.
   - Effort: about 3 lane-days to implement plus 2 to review. The V007 runs total about 70 CPU-h (§5.4).
6. **Classification (§6).** The k > K completion with the operator's own exact asymptote is counted numerics: the scheme has the same continuum limit, and no law or constant is imported.
   - The gas interpolation is a declared source-quadrature rule, not a law change. It must be preregistered with numbers and its effect measured (T2c).
   - Status stays UNTESTED until review.

---

## 1. The tail-corrected lapse

### 1.1 Definition

  δn_T(x) = Σ_{k∈G} a(k) e^{ik·x} + t(x),  where a = unit(k)·S_pkt(k) is the existing packet, unchanged (cache v001:84–86)

  t(x) = ∫_D d³k/(2π)³ T∞(k) S_T(k) e^{ik·x},  T∞(k) = 1/(4γ_eff |k|²),  D = O ∖ C

**C, the kept region of the packet the stage reads.**
- The cube [−K, K]³ by default.
- The driver mask (driver v009 `truncation_mask` L478) if one applies: the sphere |k| ≤ K, or the cylinder k⊥ ≤ K with |k_z| ≤ K.
- Route A, reference and body always run the unmasked cube (v009 L478ff docstring), so their C is the cube even in a sphere or cylinder call.
- The tail config is therefore set per stage, by the driver.

**O, the outer region.**
- Production: the cylinder {k⊥ ≤ K_big, |k_z| ≤ K_big}.
- T2 validation: the cube [−K_out, K_out]³.

**S_T = −c²ρ̂_T.** This is the transform of the stage's tail source roster (§1.3), which is the source its packet carries (I1: ≤3.5e-16). The conventions are the packet's: field e^{+ik·x}, source e^{−ik·x}.

**Lapse only.** t is added to field component 0 and to its gradient and Hessian. Components 1–9 are not corrected:
- They enter only the spatial metric and volume factors (metric v002:76–80, which feed g_cyl and the route-A proper volumes). Their size there is O(field) ≈ 10⁻⁸ relative. They also enter the reference residual diagnostics.
- The non-lapse tail contributes ≤ 0.005τ per shell (Claude3 0043/0046, A25). That is a TESTED bound on the omission.

**The equivalent Newtonian form** is Q∞·[Φ_N(D)]/c² with Q∞ = c⁴/(16πGγ_eff). G cancels.

### 1.2 Exact pointwise evaluation (E1, the production evaluator)

**Cylindrical reduction.** For an axisymmetric S_T(k⊥, k_z) the tail reduces to a 2-D integral, with the azimuthal factor W_D taken over the part of the circle (k⊥, ψ, k_z) that lies in D:

  t(R,φ,z) = [4γ_eff (2π)³]⁻¹ ∫∫ k⊥ dk⊥ dk_z S_T/k² e^{ik_z z} W_D(k⊥,k_z;R,φ),  W_D = ∫_{ψ∈D} e^{ik⊥R cos(ψ−φ)} dψ

**Square-arc harmonics** (exact). Let Q(K) be the square |k_x|, |k_y| ≤ K and α = arccos(K/k⊥). The azimuth set of Q(K) at radius k⊥ has Fourier coefficients c_m:
- k⊥ ≤ K: c₀ = 2π, and every other c_m is 0.
- K < k⊥ ≤ √2K: c₀ = 2π − 8α. For m ≡ 0 (mod 4), m ≠ 0, c_m = −8 sin(mα)/m. All other c_m are 0.
- k⊥ > √2K: every c_m is 0.

Then W = c₀^D J₀(k⊥R) + Σ_{j≥1} 2 c_{4j}^D J_{4j}(k⊥R) cos(4jφ), where c^D = c^O − c^C for each (k⊥, k_z).

For the cube C and the cylinder O this gives three cases:
- **Full ring**, 2πJ₀, wherever |k_z| > K or k⊥ > √2K.
- **Corner**, wherever K < k⊥ ≤ √2K and |k_z| ≤ K: W = 8αJ₀ + Σ_j (4 sin 4jα / j) J_{4j} cos 4jφ.
- **Zero** wherever k⊥ ≤ K and |k_z| ≤ K.

Sphere and cylinder C give full rings only. For the cube O used in T2, c^D = c^{Q(K_out)}·1[|k_z| ≤ K_out] − c^{Q(K)}·1[|k_z| ≤ K].

Harmonic truncation: j ≤ ⌈(√2·K·R + 40)/4⌉. Prototype P1 matches brute-force ψ quadrature to 4.4e-16.

**Jets.**
- R-derivatives use J_m′ = (J_{m−1} − J_{m+1})/2 and J_m″ = (J_{m−2} − 2J_m + J_{m+2})/4.
- φ-derivatives act on cos 4jφ. z-derivatives multiply by ik_z.
- Cartesian gradient: (c f_R − s f_φ/R, s f_R + c f_φ/R, f_z), with c = cos φ, s = sin φ.
- Cartesian Hessian:
  - f_xx = c² f_RR + (s²/R) f_R + (s²/R²) f_φφ − (2cs/R) f_Rφ + (2cs/R²) f_φ
  - f_yy = s² f_RR + (c²/R) f_R + (c²/R²) f_φφ + (2cs/R) f_Rφ − (2cs/R²) f_φ
  - f_xy = cs f_RR − (cs/R) f_R − (cs/R²) f_φφ + ((c² − s²)/R) f_Rφ − ((c² − s²)/R²) f_φ
  - f_xz = c f_Rz − (s/R) f_φz,  f_yz = s f_Rz + (c/R) f_φz
- Prototype P4: the Hessian agrees with finite differences of the gradient to 2.8e-8.

**Why per azimuth.**
- Route B reads 16 azimuths and route A reads 8 (DDO) or 32 (NGC). t is evaluated at each actual φ, so kept(φ) + t(φ) is the continuum field pointwise.
- The cube's m = 4j error therefore cancels, including the m = 16 alias that survives the 16-point mean (CHECK F2: ≤0.27τ).
- Prototype P2: the relative φ-spread falls from 0.141 to 2.3e-5 at R = 2 kpc. The residual is the in-cube grid quadrature, not the tail.

**Line representation**, mirroring line v002 prepare_line/evaluate_line (L11–61). For each evaluation radius R the library precomputes complex k_z-vectors:
- G_R^{(d)}(k_z) for d = 0, 1, 2 (the value and two R-derivatives of the ring part);
- G_{R,j}^{(d)}(k_z) on |k_z| ≤ K for the corner harmonics.

An evaluation at (φ, z) is then one dot product per jet with e^{ik_z z}. k_z ≥ 0 is stored and Hermitian symmetry is used: S_T(k⊥, −k_z) = conj S_T(k⊥, k_z) for a real source.

**Lapse pair** for `lapse_difference`:
- b0 = t(R,φ,0).
- bd = Σ G·(e^{ik_z z} − 1), evaluated with expm1(ik_z z). This is the "accurate difference" that line v002 L68–70 asks the caller to supply.

**Quadrature.**
- Tensor Gauss–Legendre, order o = 8, on uniform panels of widths w⊥ and w_z.
- Panel breaks at K, √2K, K_out, √2K_out, ±K and ±K_out.
- The quadrature never touches k = 0. (Prototype V001 → V002: the E2 cross-check needed geometric panels toward k = 0. E1 does not.)

**Phase rule (fail-closed).**
- The panels must satisfy w⊥·(R_eval,max + R_src,max) ≤ 1.5 rad and w_z·(z_eval,max + z_src,max) ≤ 1.5 rad.
- Any evaluation outside the declared (R_eval,max, z_eval,max) raises `ValueError('UV_TAIL_UNRESOLVED_POINT')`.
- Inside an HI column try-block, that becomes a recorded column failure, never a silent value.

**Production quadrature (prereg-fixed; doubling certificate (w/2, o+4) ≤ τ_i/20 per row).**

| galaxy | K (/kpc) | O | o | w⊥ (/kpc) | w_z (/kpc) | declared domain | N⊥ × N_z⁺ |
|---|---|---|---|---|---|---|---|
| DDO154 | 2, 3, 4 (case) | cylinder, K_big = 32 | 8 | 0.05 | 0.04 | R ≤ 14.2 kpc; \|z\| ≤ 35 kpc (route-A search limit 32 + layer) | 5120 × 6400 |
| NGC3198 | 2 | cylinder, K_big = 16 | 8 | 0.0055 | 0.0143 | R ≤ 136.5 kpc; \|z\| ≤ 105 kpc (free-boundary end at 95 kpc + layer) | 23,300 × 8,950 |

The study's DDO static rows were unchanged to ≤1e-3 km/s from (w 0.25, o 8) to (0.125, 12/16) at K_big 8/16/32/64 (T4 runs). The finer widths above are required by the route-A search heights, not by the row window.

**Blocked contraction.**
- S_T has rank r: S_T(k⊥, k_z) = Σ_i P_i(k⊥) F_i(k_z), with r = number of gas columns + 1. DDO r = 73; NGC r ≈ 205.
- For each k⊥ block (512 rows), the library forms M = P F ⊙ k⊥w/(k²) and contracts it with J₀, J₁ and J₂ at every evaluation radius of the stage at once.
- Cost: N⊥·N_z⁺·(r + N_R) MAC per field state.

### 1.3 Tail source rule

Two variants are registered:
- `continuum_v001`, evaluated by E1, for production, T1, T3 and the NGC tests;
- `nodes_v001` for T2 only.

**Stars (DDO: stars; NGC: stars + H₂, which share the sech² height).**
- The registered profile is f5becd45: Σ(R) linear between nodes, a constant core, and an exponential tail (galaxy_baryonic_source_forward_v002:43–58), with vertical profile sech²(z/2h)/(4h).
- S_*(k⊥, k_z) = −c² P_*(k⊥)·x/sinh x, with x = πh|k_z|. The vertical factor is exact.
- P_*(k⊥) = 2π ∫ Σ(R) J₀(k⊥R) R dR, computed by Gauss–Legendre per linear segment and core with n = max(16, ⌈k⊥,max Δr⌉ + 8) nodes, plus the u-map exponential tail with 256 nodes.
- The radial transform is doubling-certified to a relative change ≤ 1e-10. It is quadrature of the registered profile, not a new rule.
- The NGC H₂ prep normalization factor (prep v001, tail-mass rescale) is a GL4 artifact and is not applied.

**Gas (new rule, declared).**
- For each represented radial column i: E_i(k_z) = Σ_l m_il e^{−ik_z z_il}. The sum runs over all of the column's mass elements at all azimuths, which is the m = 0 projection. Masses are taken from the source J; nothing is re-derived.
- Per-area transform: σ_i(k_z) = E_i/(2π w_i), with w_i the column's ∫R dR weight (Δs·w_GL4/4).
- In each annulus, σ_a(s, k_z) is the cubic Lagrange interpolant in s through its four GL4 nodes.
- S_gas = −c² Σ_a Σ_q π w_q J₀(k⊥√s_q) σ_a(s_q, k_z), with M_s Gauss nodes per annulus: M_s = 64 for DDO, 96 for NGC. M_s → 2M_s must change rows by ≤ τ_i/20.
- A column absent from the roster (Σ = 0 nodes skipped, prep v007:164) enters as σ = 0.
- Nothing is placed outside the represented annuli (the registered support; no extension).

**Properties of the gas rule.**
- (i) At k_z = 0 the interpolant equals the registered quadratic Bernstein Σ(s) exactly. A cubic interpolant is exact for a quadratic (kernel V002 docstring), up to each column's mass residual.
- (ii) It has a finite UV limit at the column nodes: V-c3 measured ≤ 0.05 km/s from K_big 16 to 64, and ≤ 0.14τ for 16 vs 64 statically (§8).
- (iii) It is a new radial interpolation rule above K (CHECK §4). Its numbers are fixed here and its effect is measured by T2c.

**`nodes_v001` (the T2 variant only).** The tail is an explicit packet over the nodes of the declared extension grid outside the kept grid, G_ext ∖ G_K. For T2 that is G6 ∖ G4: prep v009 G6 contains G4 node for node and weight for weight, and the bitwise C2–C4 prefix reproduction in V006 confirms it.
- The packet amplitude is dk_w/(2π)³ · T∞(k) · S_pkt(k) on component 0 only.
- S_pkt is computed with the stage's own source transforms:
  - prep analytic J₀ for the stars and the initial gas;
  - `physical_source_fourier` for route A's per-azimuth points, so their m = 8j harmonics are included;
  - the feedback ring transform for route B.
- The packet is evaluated by the unchanged line v002 (`prepare_line`/`evaluate_line`).
- C4T-D6 and direct C6 then share nodes, weights and source. They differ only by T∞ versus T on G6 ∖ G4. That is exactly what T2 needs.
- A ring-only discrete variant would omit route A's 8-azimuth self-alias, which the route-A columns see fully, because cos 8φ_j = 1 at every column azimuth. It is therefore not used. It is also ill-posed above about 12 /kpc (V-c2).

**Azimuthal projection in `continuum_v001`.** Route A's per-azimuth gas columns enter through their m = 0 projection. The registered source is axisymmetric, and the 8 (DDO) or 32 (NGC) columns are an azimuthal quadrature of it. This is part of the declared rule. T2c measures it together with the radial interpolation.

**Roster per stage.** Every roster is rebuilt from bytes the stage already pins.

| stage | field it reads | tail roster |
|---|---|---|
| route A, iteration n | fixed + gas_n (solver v005 L111) | stars + relaxed mixture Σ_m c_{n,m}·(roster_m), mirroring L215 exactly; roster_init = prep v007 L202–211 rings at z = 0; roster_m = L187–193 elements of iteration m |
| reference, body | route-A accepted iteration (ref L223, body L213) | stars + route-A mixture at that iteration (route-A sidecar, §3) |
| offset | body fields + U·(body gas − G4 gas) | add t[stars + body gas] − t[stars + G4 mixture] (body fields already carry t of the route-A source) |
| fs columns v001, fs rotation v001 | G4 + offset (v001 L192, rot v001 L229) | stars + body gas (body_arrays base_integrated_source_J, 72×16×8) |
| rfs v003, LE1 columns v005, LE1 rotation v005 | fs feedback refreshed (v003 L198, v005 L199, rot L244) | stars + rings of the fs rotation arrays (feedback v002 start.json → rotation arrays; arithmetic of feedback v002 L210) |
| LE(n) columns/rotation, n ≥ 2 | LE(n−1) feedback refreshed | stars + rings of the LE(n−1) rotation arrays (feedback v004 L231) |

**I1-T custody gate (required at every tail build).**
- Before any evaluation, the successor transforms the represented discrete roster at 4096 seeded nodes of the stage's own grid.
- It compares the result with the packet source (fixed_source_fourier_J plus the gas packet) and requires agreement to ≤ 1e-12 relative. Otherwise it refuses with `UV_TAIL_SOURCE_MISMATCH`.
- The study measured I1 at ≤3.5e-16, and its ring rebuilds at ≤7.3e-15.

### 1.4 Remainder bound per point (fixes CHECK F3)

The remainder is r(x) = ∫_D (q(k) − 1) T∞ S_T e^{ik·x}, with q = 4γ_eff|k|²T(k).

**Uniform pointwise bound.** For any jet order a:

  |∂^a r(x)| ≤ Σ_s ε_s B_s^{(a)},  B_s^{(a)} = [4γ_eff(2π)³]⁻¹ ∫∫_{D∩shell s} k⊥ |k|^{a−2} |S_T| c₀^D dk⊥ dk_z

- The bound is independent of x, so it holds at every evaluation point. There is no ratio of maxima across columns, which was the F3 objection.
- The shells s are K–K+1, K+1–K+2, …, up to K_big.

**ε_s, the symbol certificate.**
- ε_s = max |1 − q| over a declared symbol sample: 13 directions × 64 |k| per decade in each shell, through the reviewed symbol path (QINF V001 evaluator).
- It is a pre-run certificate whose sha256 enters the call.
- Measured so far: 5.9e-4 on |k| ≥ 2, and 1.4e-4 on 4–5 /kpc. Above 6.9 /kpc there are only the point checks at 30 and 1000 /kpc (A21). The certificate must cover [K, K_big]. That coverage is UNTESTED until it is run.

**Outer truncation.** The region beyond O is bounded by B_out (the same form, over ℝ³ ∖ (C ∪ O)) and measured by T3.

**Propagation to rows (static channel, exact algebra).**
- Rotation law v001:16–20: δ(v_c²) = R·δC_R, and δC_R is the mean of δΦ_R with weights wρ/h ≥ 0.
- So |δv_c(R)| ≤ R·c²·Σ_s ε_s B_s^{(1)} / (2 N_min v_c(R)).
- A row's bound is the maximum over the columns the adapter combines for that row (nonnegative weights).
- Column potential: |δ potential| ≤ 2c²·Σ_s ε_s B_s^{(0)} / N_min.
- **Gate RB:** the static row bound must be ≤ τ_i/10.
- The fixed-point amplification of r is not bounded analytically. T2 measures it, because direct C6 carries the true q on [4, 6].

---

## 2. Every code site that evaluates the lapse or its derivatives

Lines refer to the bytes pinned in the JSON twin. "Slot" means an additive argument that receives zeros today.

### 2.1 Route A (DDO154: serial c4cb6826 / parallel 9dbdaf11 worker; NGC3198: 42bdd23e / 5f16525a, driver NGC_CODE v001 1b95a4ff)

| # | file (sha8) | lines | what is read | how t enters |
|---|---|---|---|---|
| A1 | DDO prep v007 `ac905597` (v008 `bb05f974`, v009 `b4b27a1d`: same lines) | 214–218 | `boundary(pos)` closure returns zeros, passed as `data['boundary']` | replaced by the binding successor with a stateful `TailBoundary` callable (component-0 jet of the current iteration's tail); prep bytes unchanged |
| A2 | DDO prep v007 | 202–211, 237–240 | initial razor-thin gas rings at z = 0 and analytic GL4 star rings | roster_init and the I1-T stars check |
| A3 | DDO binding `d81b24b7` | 34–41, 86–89 | facade built; `ca.boundary_jet_at_positions = data['boundary']` | binding successor: `data['boundary'] = tail.boundary`; `make_modules(..., tail=tail)`; solver passed as `bind_uv_tail(tail)` view (pin of `__file__` unchanged, the parallel-solver pattern) |
| A4 | stable facade v001 `2caca496` | 14–22, 38–40 | refuses nonzero boundary; `lapse_difference` with b0 = bd = 0 | facade successor: admits boundary arrays only if `array_equal` to `tail.jet(pos)`; passes `tail.lapse_pair` as b0/bd |
| A5 | solver fixedsrc `44d9c23c` | 111–112 | `current = fixed + gas`; `prepare` | before L112: `tail.set_state(build(stars + mixture_n, radii))` |
| A6 | solver | 129–150 (132) | `metric_point`: `boundary_jet_at_positions(pos)` → `evaluate_line` (L142) or `evaluate_prepared` (L134) | through the slot; no solver arithmetic change |
| A7 | solver | 155–165 | free-boundary HI column `solve_hi_column(at_z)` | via A4/A6 (N and the stable log ratio both include t) |
| A8 | solver | 187–195, 215 | per-column source elements, updated transform, relaxation | collect roster_n from the same elements; mirror L215 on the roster coefficients; sidecar `uv_tail/iteration_%04d.npz` plus I1 check against the stored gas iterate on resume |
| A9 | parallel solver `aed4dd59` | 159–165, 197–198, 220–233, 290, 313, 625–645, 669ff | `pool.start(column_environment=boundary…)` is shipped once; prepared shipped per iteration; worker `metric_point` | successor ships the per-iteration tail state with `pool.begin_iteration` and sets it in the worker's `TailBoundary` before columns; parent-side identical to A5–A8 |
| A10 | HI free boundary v003 `b176c7a6` (DDO) | 56–74 | N and `log_lapse_ratio_from_midplane` | none (consumes A4) |
| A11 | prediction v005 `54136c71` | 62–83 (75), 85–101 | route-A rows: `evaluate_line(**boundary(pos))` plus HI midplane columns | none; reads the final state left bound by the solver (= converged `prepared`) |
| A12 | composite adapter `75092cf6` | 57–64 | passes `prepared['boundary']` to `solver.solve` | none |
| A13 | NGC prep v001 `c54c7cc9` | 269–273; 183–250, 256–263, 290–295 | boundary closure; stars + H₂ GL4 rings; razor-thin initial gas | as A1/A2 (NGC binding successor) |
| A14 | NGC binding v002 `cc5db369` (v001 `9e9caf83` L52–54) | 80–82, 110 | `ca.boundary_jet_at_positions = data['boundary']`; vertical line = line v001 | binding successor as A3; there is no facade in NGC |
| A15 | line v001 `5c0ab4f6` (NGC) / line v002 `3a47419d` (DDO, route B) | v001 46–61; v002 46–61, 64–101 | additive `boundary_fields/gradient/hessian`; `boundary_lapse_at_zero/difference` | unchanged; these are the slots |
| A16 | HI free boundary v002 `665b5589` (NGC) | 53–61 | N only (log N − log N0 vs θ) | via A14 |
| A17 | inverse cache `7b9816ae` | 84–86, 114–116 | packet = unit × source (no real-space read) | none |

### 2.2 Route B (gal_c2v004 stages, `ngc_f10_c2/route_b_v006/stages`; the same bytes for DDO154 and NGC3198)

| # | stage (sha8) | lines | read | how t enters | successor |
|---|---|---|---|---|---|
| B1 | reference worker `dbdbfba1` | 223, 254–256, 271 | route-A prepared field; `boundary(pos)` zeros → `ref.evaluate_radius` | boundary callback returns t-jet of stars + route-A mixture | yes |
| B2 | reference module `1b00add9` (stages2) | 44, 51, 55–60, 63–69, 74, 106 | lines; `evaluate_line(**boundary_jet_at_positions(pos))`; log1p f₀, dlnN; column roots, logN0, K_SI; u(z); Φ_R/Φ_z | none (consumes B1 callback) | no |
| B3 | body stage `0bf1c4cb` | 213, 241–242, 248, **254 (K0 assembly: F1)** | route-A prepared; boundary zeros → `evaluate_saved_radius` | boundary callback = t-jet (same roster as B1) | yes |
| B4 | body base `d540fd7c` (stages2) | 43, 48, 57, 65, 75–77 | lines; `evaluate_line(**boundary…)`; mean0, Φ_R0, Ω; u(z) with saved logN0; shape integral → A → **K** | none (consumes B3). The logN0 consistency requires B1 and B3 to share one tail | no |
| B5 | offset `e821ae42` | 229–230, 244–251, 252–265 | unit response (none); direct phase sum of offset fields at body mesh; totals, guards, Φ0, r0; K0 passthrough | add t[Δ] (Δ = body gas − route-A mixture) to component 0 of `fields` before L251 | yes |
| B6 | fs columns v001 `bb936834` | 192, 199, 203, 207, 211, 212–214, 217 | G4+offset packet; K0; lines; `evaluate_line` zeros; metric guard; `lapse_difference` zeros → potential(z); `solve_column` | t-line per (R,φ) next to L203; jets in L207 slots; `lapse_pair` in L212 slots | yes |
| B7 | rfs columns v003 `b20c5152` | 198, 208, 212, 216, 220, 221–223, 228 | refreshed (fs feedback); K0; as B6 | as B6 | yes |
| B8 | LE columns v005 `0fdf435a` | 189, 199, 211, 213, 217, 221, 222–224, 229 | refreshed; scaled K0; as B6 | as B6 | yes |
| B9 | fs rotation v001 `fd9f51d4` | 229, 235, 237, 241, 244–246, 249, 250 | G4+offset; lines; `evaluate_line` zeros; metric; Φ, Φ_R = c²g_R/N, Φ_z; m = 0 means; rotation law | t-jets in L237 slots (N and g both include t) | yes |
| B10 | LE rotation v005 `9b2ded4f` | 244, 252, 254, 258, 261–263, 266, 267 | as B9 | t-jets in L254 slots | yes |
| B11 | feedback v002 `4bf84ce4` / v004 `938fb974` | v002 210, 231–240; v004 231, 251–259 | ring roster from rotation arrays; analytic J₀ transform; unit × Δ (no real-space read) | none; rings are rebuilt downstream from pinned arrays and verified by I1-T | no |
| B12 | column mean v004 `11d6f8b8` | 201–220 | rotation arrays (Ω, ρ, z, K0), column weights; no lapse read | none; the producer pin `rotation_worker` is per-call config (L129–137) and accepts the successor | no |
| B13 | rotation law `e1b354ec`, metric `8f01bd5b`, join `0a7f5314`, column solver `54e56f7b`, leading column `022ed7f1` | – | consume values passed in | none | no |

### 2.3 Driver v009 `999331af` (planning sites a v010 successor touches)

| what | lines |
|---|---|
| SCRIPTS / AUX / PARALLEL_ROUTE_A pins | 157, 218, 238 |
| `truncation_mask` (the per-stage C) and `_install_hooks` | 478, 568 |
| `numerics` strict keys | 776 (+ `uv_tail`) |
| route-A request | ≈2255–2286 |
| reference, body, offset requests | 2360, 2375, 2383 |
| column requests, fs rotation, fs feedback | 2423, 2489, 2495 |
| FS / RFS / LE passes | 2466, 2502, 2523 |
| harmonic diagnostic (reads Φ_R_full; its m4 should drop with t) | 1628–1642 |
| NGC_CODE and NGC numerics | 3599ff, 3766 |

---

## 3. Module plan

All new files go in a new implementation lane (proposed `claude_artifacts/uv_tail_impl_c2/`). No reviewed byte is edited.

### 3.1 New modules

**`owned_uv_tail_lapse_v001.py`** (≈700 lines, pure numpy plus the Jₙ provider). API:

- **Roster builders**, each an exact replica of the cited arithmetic:
  - `stars_registered(profile, galaxy, components)`, plus `stars_gl4(...)` for the I1-T check (prep v007:172–190; NGC prep v001:183–250);
  - `nodes_packet(ext_grid, kept_grid, source_transform)` for the T2 variant, evaluated by line v002;
  - `roster_route_a(elements, init_rings, coefficients)`;
  - `roster_body(body_arrays)`;
  - `roster_rotation(rotation_arrays)` (feedback v004 L231).
- **`check_represented(roster, waves_sample, packet_sample)`**: the I1-T gate.
- **`build(config, roster, gamma_eff, c, radii_m)` → `TailState`**:
  - blocked contraction, with plain shippable arrays;
  - empty domain returns zeros with no arithmetic;
  - carries the digest of its config, roster and arrays.
- **Evaluation:**
  - `jet(state, pos)` returns shapes (n,10,1), (n,10,1,3), (n,10,1,3,3), component 0 only;
  - `lapse_pair(state, x, y, z)` returns (b0, bd) via expm1;
  - `TailBoundary`, a picklable callable with `set_state`.
- **`remainder_bound(state, eps_certificate)`** and **`digest(state)`**.

**`posix_libm_bessel_jn_provider_v001.py`** (≈60 lines). This is the successor pattern of the pinned `posix_libm_bessel_j0_provider_v001`. It provides J₀, J₁ and Jₙ from libm and records libm custody.

### 3.2 Route-A successors (each is the reviewed bytes plus one guarded block; with `uv_tail=None` the reviewed body runs)

| successor | base | minimal diff |
|---|---|---|
| `coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py` | 44d9c23c | `bind_uv_tail(tail)` view; `set_state` before L112; roster collect at L187–193; mirror L215; sidecar plus resume I1 check; result `uv_tail` record |
| `…_parallel_uvtail_c2v001.py` | aed4dd59 | the same, plus the tail state shipped in `begin_iteration` (A9); keeps the V8c-F1 fix requirement (A23) |
| `owned_stable_lapse_hi_facade_uvtail_v001.py` | 2caca496 | L16–19 zero-check becomes the equality-to-`tail.jet` check; L38–39 b0/bd come from `tail.lapse_pair` |
| `ddo_composite_stable_cached_binding_v002_uvtail_c2v001.py` | d81b24b7 | `uv_tail` argument; replace `data['boundary']`; bind facade and solver views; append the tail declaration to `identity['boundary_prescription']` |
| `ngc_composite_full_coupled_binding_v002_uvtail_c2v001.py` | cc5db369 | the same, with no facade |
| DDO worker serial/parallel `…_uvtail_c2v001.py` | c4cb6826 / 9dbdaf11 | required `--uv-tail-config`, `--uv-tail-config-sha256` and `--eps-certificate`; `numerical_controls['uv_tail']` = config digest, so a tail-ON checkpoint identity can never resume or admit a tail-OFF one |
| NGC worker serial/parallel `…_uvtail_c2v001.py` | 42bdd23e / 5f16525a | the same |

Unchanged: prep v007/v008/v009, NGC prep v001, composite adapter, line v001/v002, HI v002/v003, checkpoint module c2v003, prediction v005, inverse cache.

### 3.3 Route-B stage successors (`*_gal_c2v004_uvt_c2v001.py`; 8 files, ≈40–60 changed lines each)

- **Successors:** reference worker, body, offset, columns v001/v003/v005, rotations v001/v005.
- **Common diff:**
  - new argv `--uv-tail-config/--uv-tail-config-sha256` plus the upstream roster pins (route-A sidecar manifest for reference, body and offset);
  - after the field is loaded: roster rebuild, I1-T, `build`;
  - the slots at the lines listed in §2.2 receive t;
  - start/finish records carry the config sha, roster digest, tail digest, I1-T record and remainder bound.
- **Refusal:** a successor refuses to run without a tail config. Tail OFF never plans it.
- **Not needed:** feedback v002/v004 and column mean v004 need no successor. Producer pins are per-call config, so they accept successor producers unchanged.

### 3.4 Driver v010 (`galaxy_m0_forward_c2v010.py`, successor of v009 999331af; ≈400–600 changed lines)

**The `numerics.uv_tail` block:**

    {enabled, outer:{shape:'cylinder',K_big_inverse_kpc} | {shape:'cube',K_out_inverse_kpc},
     source_rule:'continuum_v001'|'nodes_v001'(+ext_grid), gas:{interp:'lagrange3_s_gl4',M_s},
     stars:{segment_rule,tail_nodes}, quadrature:{order,w_perp,w_z}, domain:{R_eval_max_kpc,z_eval_max_kpc},
     asymptote:'EH_exact_minus_quarter', lapse_only:true, eps_certificate:{path,sha256}}

- The kept region C is derived per stage, not supplied: cube K for route A, reference and body; the mask shape for route B.
- If the block is absent or `enabled:false`, normalization and planning are exactly v009's.

**When enabled, the driver:**
- writes `inputs/uv_tail_config.json` and pins it;
- swaps in `SCRIPTS_UVT` and `AUX_UVT`;
- sets producer pins to the successor shas;
- threads the route-A sidecar manifest into reference, body and offset;
- refuses admission of any route A or prefix whose identity lacks the same `uv_tail` digest (`UVT_ADMISSION_MISMATCH`);
- adds `result['uv_tail']` with per-stage digests, I1-T records and bounds;
- lists the tail plan in its dry-run output.

### 3.5 How bitwise identity is preserved when the tail is OFF

- **B0, planning identity.** v010 with no `uv_tail` must give requests, inputs and normalized specs byte-identical to v009 on the full v009 spec set, the V005/V006 specs and the NGC templates. This is the same mechanical compare as v008's D1.
- **B1, code-path identity.** Tail ON over an empty domain (cylinder K_big = K; the corner ∩ {k⊥ ≤ K_big} is empty):
  - every slot receives exact zeros, which are produced without arithmetic;
  - x + 0.0 is the operation the reviewed code already performs;
  - so arrays and rows must equal A2_ANCHOR_F10_RUN_V001 bitwise, apart from a declared list of custody fields that name successor pins.
  - The precedent is the v008 deciding II comparator, which gave PASS_BITWISE_EQUAL on 13/13 checks.
- **Structural.** No reviewed file is edited. Tail-OFF calls cannot reach successor code, because successors refuse without a config and v010 never plans them with the tail off.

---

## 4. Prereg V007 draft (to be sealed before any tail result exists)

**Fixed for all tests.**
- Anchor A2F10 and the DDO seed of V005; grids G2/G3/G4 (the cube) as V005.
- τ_i and D̂ from V005 dbddc02c: D̂(K1,K2) = max_i |v_i(K2) − v_i(K1)|/τ_i.
- The V005 validity gates V1–V6.
- Brackets: the V005 D7 R3 block `7946b857`, with the pre-named W1 widening (V005 d7_recovery.later_invocations), applied at most once and recorded.
- Route A is computed in every T-run. Admission of any tail-OFF route A is refused.
- Production tail: continuum_v001, cylinder K_big = 32, the §1.2 DDO quadrature, M_s = 64.

**Gates (all must pass before any T result is read).**
- **B0:** planning identity (§3.5).
- **B1:** code-path identity, on run Z2 = A2F10 C2 with K_big = K (§3.5).
- **B2:** independent re-implementation, a static replay on saved states. On the saved C2R3/C3R3/C4R3 le3 columns, the rotation_v005 successor plus the unchanged column mean gives static rows.
  - These must equal a checker's independent Cartesian implementation (CHECK §2 method, 16-azimuth P16, the same declared rule and K_big) to ≤1e-4 km/s per row.
  - Sanity check only: they must equal the study's m = 0 rows to within the measured m = 16 alias plus the star-roster difference (≤0.05 km/s).
- **RB:** the static remainder row bound (§1.4) must be ≤ τ_i/10 on C4T, with an ε certificate covering [4, 32].

**Tests.**

| test | runs | statistic | pass |
|---|---|---|---|
| T1 (internal convergence) | C2T, C3T, C4T | D̂_T(2,3), D̂_T(3,4) | both ≤ 1 |
| T1-S (shape) | S4T (route-B sphere mask with sphere tail; route A, reference and body cube with cube tail) vs C4T | max_i \|Δv_i\|/τ_i | ≤ 2 (V005's shape threshold; expected ≤ 0.5, UNTESTED) |
| T2 (ground truth for the implementation) | C4T-D6: `nodes_v001` on G6 ∖ G4, vs direct C6 under V006 | max_i \|Δv_i\|/τ_i | ≤ 1/4 |
| T2c (rule effect, reported) | C4T-C6c: `continuum_v001` with E1 and outer cube 6, vs C4T-D6 | max_i \|Δv_i\|/τ_i | reported; > 1 sets the flag SOURCE_RULE_MATERIAL (review before adoption) |
| T3 (UV completion) | C4T-K16, C4T-K64 vs C4T (K_big = 32) | max_i \|Δv_i\|/τ_i, each pair | ≤ 1/4 |
| D-m4 (reported) | C4T vs C4R3 | v009 harmonic diagnostic, m4 | reported; expected ≪ C4R3 by construction (magnitude UNTESTED) |

**What the tests rest on.**
- T2: C4T-D6 and C6 share nodes, weights and source. They differ only by T∞ versus T on G6 ∖ G4, where |1 − q| ≤ 1.4e-4 on 4–5 /kpc (CHECK F3). T2 is therefore an exact equivalence test of the stage wiring and the Q∞ substitution.
- E1 itself is tested by B2 and by the prototype. T2c measures E1 plus `continuum_v001` on [4, 6].
- T3: the static study values give 16 vs 64 at ≤0.14τ (C2) and ≤0.12τ (C4); 32 vs 64 at ≤0.12τ / 0.09τ (§8). The fixed-point value is UNTESTED.

**Decision rule.** ADOPT_TAIL at K = 4 (cube, C4T as specified) requires all of: B0, B1, B2, RB, T1, T2 and T3 pass; T1-S pass; and no SOURCE_RULE_MATERIAL flag, or else a root ruling on it.

**Pre-named outcomes.**
1. **T2 fails → IMPLEMENTATION_DEFECT.** Stop. T1 and T3 are not read as physics.
2. **T2 passes, T1 fails → NOT_UV_RESIDUAL.** Route A, reference and body carry the tail, so the K0 channel (F1) is closed and the reading "not UV" is now valid. Next: the column/Picard map, with its own prereg.
3. **T3 fails → KBIG_NOT_CONVERGED.** Rerun production at K_big = 64 under T3′ (32/64/128), which needs the ε certificate to 128.
4. **T1 passes, T1-S fails → SHAPE_DISAGREEMENT.** Review the per-stage C wiring.
5. **RB fails → BOUND_INSUFFICIENT.** Tighten ε per shell, or add a q-corrected shell to the tail (V002 design).
6. **B0, B1 or B2 fails → NO_RUN.** No T case is launched.

**NGC3198 analogue.** It uses the k-grid prereg 4c2eefeb machinery: iteration-0 operator, 100 roster rings, 32 azimuths, θ = log1p(h0/c²) = 3.3657664e-9, T120L kept region (cube K = 2), and tail continuum_v001 with K_big = 16, the §1.2 NGC quadrature and M_s = 96.

| test | statistic | pass |
|---|---|---|
| N0 (identity) | K_big = K on T120L | lnN0 and C4 reads bitwise equal to the tier-2 T120L reads |
| N1 (C1 with the tail) | S = max_φ lnN0 − min_φ lnN0 | S < θ on the 12 TRUNCATION_SHAPE rings (ordinals 1–8, 10, 13–15), with C1 as written; C1′ (A17, open V004 addendum) still passes at the NOT_GRID rings; reported on all 100 |
| N2 (shape invariance; NGC has no k_max ground truth) | sphere-masked T120L + sphere tail vs cube T120L + cube tail, per ring and azimuth: lnN0 and dL(±10, 20, 30 kpc) | ≤ θ/4 |
| N3 (UV completion) | K_big 8 and 32 vs 16: S/θ and e4 | changes ≤ θ/4 |
| N4 (reported) | e4 at ±95 kpc (A14.C5) for cube+tail vs sphere+tail | reported |

- N1 is insensitive to K_big by construction: the m = 4j terms live only at |k_z| ≤ K.
- NGC route-B fixed points with the tail wait for a valid NGC route-A base (UNTESTED).
- NGC tests need a reviewed NGC prep successor for tier-2 grids (prep v001:142 caps nk ≤ 80; :155 uses one axis).

**Run list and caps.**
- DDO: Z2, C2T, C3T, C4T, S4T, C4T-D6, C4T-C6c, C4T-K16, C4T-K64. C6 comes from V006.
- NGC: NZ, N1C, N1S, N3a, N3b.
- RSS cap: v009 per-call cap plus 1 GiB. At most 4 processes. Serial route A for wave 1 (A23).

---

## 5. Cost

### 5.1 Measured baselines (progress.jsonl; machine load varied)

| run | route A | reference | body | offset | route-B passes | total |
|---|---|---|---|---|---|---|
| A2F10 C2 (G2, serial route A) | 1,619 | 947 | 169 | 266 | ≈3,723 | 6,724 s |
| KMAX C3 (V005 prefix) + C3R3 | 3,854 | 1,631 | 296 | 553 | 10,422 wall (R3) | ≈16,700 s |
| KMAX C4 (V005 prefix) + C4R3 | 5,939 | 2,786 | 600 | 1,564 | 10,700 − 1,206 | ≈20,400 s |
| A2F10 parallel N=8 (v008 deciding) | 1,542 | 1,323 | 221 | 405 | – | 8,924 s (under load) |

### 5.2 Tail cost model

- **Build per field state:** N⊥·N_z⁺·(r + N_R) MAC.
  - DDO route-B stage: 5120 × 6400 × (73 + 72) = 4.8e9.
  - DDO reference: N_R = 360, so 1.4e10.
  - NGC: 23,300 × 8,950 × (205 + 205) = 8.5e10.
- **Throughput:** measured 30–45 G complex MAC/s with BLAS threads = 1 (P5, Accelerate on this machine). A conservative 2 GMAC/s is assumed below.
- **Build time:** 2.4–7 s per DDO stage; up to 43 s per NGC state.
- **Corner tables:** up to ≈10⁶ libm Jₙ calls, about 1 s.
- **Per evaluation:** N_z⁺ complex exponentials plus about 4 dot products, ≈30–80 µs. The existing cost is ≈4.4 ms per metric call (G80C measured 4.378 ms), so the tail adds ≤2%.
- **Memory:** a 512-row k⊥ block is 52 MB (DDO) / 73 MB (NGC). The lines are 22 MB (DDO, 72 R) / 88 MB (NGC). Allow ≤0.5 GiB per process.

### 5.3 Per call with the tail (estimates; route-A and Picard iteration counts with the tail are UNTESTED)

| call | estimate |
|---|---|
| DDO C2T (G2) | ≈7,500 s (≈2.1 h), serial route A |
| DDO C3T (G3) | ≈18,000 s (≈5.0 h) |
| DDO C4T (G4) | ≈22,000 s (≈6.1 h); C4T-K64 adds ≈10% (N_z⁺ doubles; evaluations are still ≪ the cube) |
| DDO route A, parallel N=8 | +1–3% per iteration: parent build ≤10 s, plus shipping 22 MB per worker per iteration (≈0.2 GB in total) |
| NGC T120L+tail, iteration 0 (N1) | prep 424 s + build ≤43 s + 3200 midplane line reads × 0.53 s ≈ 2,200 CPU-s, about 0.6 h at 4 processes |
| NGC N2 sphere + N3 | N2 doubles N1; N3 reuses the kept-line reads (t is additive), only minutes |

### 5.4 Implementation and review effort (estimate)

- **Code:** library ≈700 lines; provider 60; route-A successors ≈450; stage successors ≈400; driver v010 ≈500; V007 builder and comparator ≈500; tests ≈1,500.
- **Implementation:** about 3 lane-days.
- **Independent review:** about 2 lane-days, covering the classification, the gas rule, I1-T, slot semantics, B0/B1 evidence and a Cartesian re-implementation as in CHECK §2.
- **V007 runs:**
  - DDO: Z2 2 h, C2T 2 h, C3T 5 h, C4T, S4T, C4T-D6, C4T-C6c, C4T-K16 at 6 h each, C4T-K64 7 h. That is about 51 CPU-h, plus C6 from V006.
  - NGC: about 3 CPU-h.
  - Total about 54 CPU-h (≈70 CPU-h with margin). At ≤4 processes that is about 1.5–2 days of wall time.

---

## 6. Classification: counted numerics or model change (argued; UNTESTED until review)

**The case for counted numerics (the k > K symbol completion).**
1. **Same object.** t completes the continuum integral that the packet discretizes, over the domain it omits.
   - As K → ∞, t → 0 and δn_T → the same continuum field.
   - The scheme has no limit of its own and adds no parameter that survives the limit.
2. **The operator's own asymptote.**
   - T∞ is the exact large-k lapse entry of the reviewed kernel: [pinv Ê]_nn = −1/4 for all 13 directions and all 4 backgrounds (A21, QINF V001), and the native sector drops out.
   - Nothing is imported: G cancels, there is no Newtonian far-field law, and no fitted constant.
3. **Bounded deviation.** q − 1 is measured (≤5.9e-4 for |k| ≥ 2, 1.4e-4 on 4–5) and propagated by a pointwise bound (§1.4). T2 compares against an independently computed truth that contains the true q.
4. **The kept-region symbol is unchanged.** No packet, cache, unit response or kernel byte changes.
5. **Unlike the rejected splice.** "8.06·T_N at low k" imposed a far-field law where the symbol is not at its asymptote, and was classed as a model change. Here the replacement applies only where |1 − q| ≤ 6e-4.

**The two declared choices that need explicit review.**
- **Stars.** The tail uses the exact transform of the registered analytic profile. The GL4 cube rings are themselves a quadrature of that profile. This is counted quadrature, with no new rule.
- **Gas.** The cubic-in-s interpolant is a new radial source-quadrature rule above K.
  - It changes neither Σ (it is exact at k_z = 0) nor the solved vertical structure, the equation of state or the operator.
  - It is needed because the discrete roster has no finite UV limit at its own nodes (V-c2). Its influence vanishes as K → ∞.
  - Classed as counted numerics with a preregistered rule (M_s, family, support) and a measured effect (T2c), as CHECK §4 required.
- **Lapse only.** This is a counted omission with a TESTED bound (≤0.005τ, A25).
- **Slot semantics.** The `boundary_*` slots are documented as "boundary perturbations". Each successor declares that they carry the UV-tail jet of the current source while the physical boundary stays zero, and records this in route A's `boundary_prescription`. This is a declared semantics change, not a new boundary condition.

**What would make it a model change** (the reviewer's falsifiers):
- the K → ∞ limit of δn_T differs from the packet's;
- |1 − q| on D exceeds the certificate;
- the gas rule alters column-integrated Σ beyond the column mass residual;
- any kept-region symbol entry changes;
- T2 fails beyond the implementation-defect reading.

---

## 7. Risks and UNTESTED items (each with its deciding test)

| item | status | deciding test |
|---|---|---|
| Fixed-point D̂_T ≤ 1 | UNTESTED | T1 |
| Route-A/Picard iteration counts and D7 brackets with deeper inner wells (the study's static well/h0 up to 2.56 at C2) | UNTESTED | T1 runs (W1 pre-named) |
| ε over [K, K_big] above 6.9 /kpc | UNTESTED (point checks at 30 and 1000 only) | pre-run certificate |
| Razor-thin initial-iterate gas (weight (1 − r)ⁿ = 6% at n = 4): its sheet term converges only ~1/K_big at z ≈ 0 | UNTESTED | T3 / N3; option V002: analytic k_z integral of full-ring regions |
| Gas rule effect on [4, 6] | UNTESTED | T2c |
| Static discrete vs continuum over [2, 8] reaches 0.52τ (C2 row 06), so in-cube source quadrature enters T1 | TESTED (study T4) as a magnitude | T1, T2c |
| NGC kp/kz resolution at R and z ≈ 100 kpc | UNTESTED | doubling certificate |
| Route-A azimuthal discreteness: the m = 8j (DDO) / 32j (NGC) source harmonics are dropped above K by the continuum rule | declared rule | T2c (DDO); audit H3 (NGC) |
| T2 C4T-D6 cost: the G6 ∖ G4 node packet (≈840k nodes) roughly doubles line preparation in that run only | estimate | – |

---

## 8. Prototype evidence (synthetic; `out/PROTO_TAIL_V002.json`)

Test source: a Gaussian disc (a = 0.35, b = 0.12 kpc), K = 2, K_big = 60; kept cube on a G2-like grid (373,248 nodes); 45 points (R ≤ 2, three heights, five azimuths).

| check | result |
|---|---|
| P1 corner series vs brute-force ψ | 4.4e-16 |
| kept + t vs whole space: value / gradient / Hessian (kept alone) | 6.9e-5 / 4.4e-5 / 1.2e-4 (0.41 / 0.95 / 1.26) |
| E1 vs E2 (whole space − continuum cube), value / gradient | 2.1e-6 / 2.6e-13 |
| discrete kept grid vs continuum cube (the residual source of the first row) | 6.5e-5 |
| φ-spread R = 0.4 / 1 / 2 kpc: kept → kept + t | 1.6e-4 → 1.9e-8; 1.1e-2 → 1.3e-6; 0.141 → 2.3e-5 |
| Hessian vs finite differences | 2.8e-8 |
| complex matmul throughput | 30 / 45 GMAC/s |

**Study static K_big convergence** (continuum, recomputed from UV `out/T4_*`; max_i |Δv_i|/τ_i against K_big = 64):

| K_big | 16 | 24 | 32 | 48 |
|---|---|---|---|---|
| C2 | 0.14 | 0.13 | 0.12 | 0.11 |
| C4 | 0.12 | 0.15 | 0.09 | 0.03 |

The discrete rule stays at 3.3–23τ for K_big ≥ 16 (V-c2).

## Errors register

1. **E2 cross-check under-resolved (prototype V001).** The value check was limited to 5% by the k = 0 point singularity on width-0.25 panels. V002 adds geometric panels toward k = 0 and agrees to 2e-6. V001 and its output are kept unchanged. E1, the production evaluator, never reaches k = 0.
2. **T2 variant replaced during drafting.** The first draft's ring-only `represented_discrete` variant would have dropped route A's 8-azimuth source harmonics, which direct C6 contains, so T2 would not have been exact. It was replaced by `nodes_v001` (G6 ∖ G4 node packet, line v002) before the twin and hashes were written. G6 ⊃ G4 was confirmed from the V006 C6 spec breaks.
3. **P4 lapse-pair check not performed.** Prototype P4 recorded t(z = 0) and t(z = 0.6) but did not compare the expm1 pair against the plain difference. No claim is made from it. It is left to the implementation's unit tests.
