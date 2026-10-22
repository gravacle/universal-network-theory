# TAIL_SCHEME_DESIGN_V002_R1: CHECK_V001 edits applied, and the module lane's implementation amendments

tail_scheme_design_c2/v002/r1, 2026-10-18 (UTC). Design revision record. It does not edit any reviewed file.

**Base:** TAIL_SCHEME_DESIGN_V002 (`.md` cdb16d1c, `.json` d3888233, prereg draft 357c0738), unchanged on disk.
**Check applied:** v002/check/CHECK_V001.md (ca4c480d), VERDICT REVISE, findings L1-L10 ("small edits; no redesign").
**Machine-readable prereg successor:** `KMAX_TAIL_PREREG_V007_DRAFT_R1.json`, built by `tools/make_prereg_r1_v001.py` from the V002 draft (pins checked from bytes). The JSON is authoritative for every prereg edit below.
**Decision pins:** frozen V002 `17c26616`, V003 `5bef6552`; the V004 addendum (A21-A30) is cited by name only.

Everything in V002 not named here stands as written, as the check found: §2, §3, B0, B0-FA, B1 apart from its exception list, B2, EPS, LO (DDO), M_T, the quadrature table, and the classification once L5's terms are added.

---

## Part 1. The check's edits L1-L10 (applied)

| # | V002 place | edit applied (wording in the R1 prereg JSON) |
|---|---|---|
| L1 | §5.2, prereg `pairing_and_decidability_rule` | `decidable_iff` = E_i(P) + E^A_i(P) ≤ τ_i/8 on every row. E^A_i(run) = per-row form of M_K at the accepted route-A iteration, in km/s: max over the 8 column azimuths of R_i c² \|∂_R packet_K[updated_acc − gas_acc](R_i, φ_j, 0)\| / (2 v_i^ref). Route-A accepted iteration and Picard pass counts are recorded as diagnostics, not compared. R-PAIR: the route-A branch (seed source_rtol/10) applies when E^A > E on the failing row, otherwise the Picard branch. T1 is not under the rule: its D̂ pairs follow V005 as sealed. |
| L2 | §5.5, prereg `outcomes_first_applicable` | New order: NO_RUN; NUMERICS_UNCERTIFIED / NON_LAPSE_TAIL_MATERIAL; UNDECIDABLE_ROUTE_A_TAIL; UNDECIDABLE_AT_ITERATION_FLOOR; IMPLEMENTATION_DEFECT; SOURCE_RULE_MATERIAL; KBIG_NOT_CONVERGED; BOUND_INSUFFICIENT; FLOOR_LIKE (precedes the two T1-fail readings); NOT_UV_RESIDUAL; SOURCE_REPRESENTATION_K_DEPENDENT; HIGHER_K_DISAGREEMENT; SHAPE_DISAGREEMENT; **FLAG_PENDING_RULING** (new: every test passes but a flag stays unruled; no adoption); ADOPT_TAIL. A flagged run's test is read only as undecidable. The md §5.5 list is replaced by this one. Branch tests are required, one per outcome (`outcome_branch_tests_required`). |
| L3 | §4.2 | B0′-SIM is withdrawn (not executable: v009-EXT has only `run`/`dry-run`; result.json is written only by `cmd_run`). It is replaced by **B0′-DRY**: DRYRUN_REPORT.json and DRYRUN_PLAN.txt identical under the declared maps (gal_c2v005 CHECK CMP_DRY method). Result assembly is identity-gated **only** by B0′-RERUN, B1 and Z2-OFF, on DDO154. NGC result assembly under v010 is UNTESTED (deciding test: the first NGC route-B result under v010 against a v009 parent). B0′-RERUN and B1 exception lists add (i) every string value beginning with the run's outdir path, compared after prefix substitution, and (ii) `elapsed_seconds` at top level and in `stage_records[]`. |
| L4 | §4.5 | B3 gains a **cylinder-O case**: O = cylinder K_big = 8 over cube 4, same points and tolerances; the independent lane integrates in (k⊥, ψ, k_z) with the corner zone handled by its ψ limits. (The module lane already runs this case in its pre-gate, test (e).) |
| L5 | §1.4, §7, §8 | δn_T,K = Φ_∞[S_T] + b_K + r_K + g_K + **o_K** + **ℓ_K**. o_K = −∫_{ℝ³∖O} T S_T e^{ik·x} (K_big truncation), measured by T3 (DDO) and N3 (NGC). ℓ_K = the omitted non-lapse components, measured by LO (DDO) and LO-NGC. §7 point 2 adds both. §8 adds the rows "o_K: T3/N3" and "ℓ_K: LO/LO-NGC". |
| L6 | §5.3-5.4 | The SR term in u_i and in the SOURCE_QUADRATURE_MATERIAL flag is max(\|Δ_i^SR(4)\|, \|Δ_i^SR(4)\|·A_i), A_i = \|∂v_i/∂λ\| / \|ΔV_i^static,tail\| from the AMP run (DECLARED, UNTESTED). It is labelled "static only; fixed-point UNTESTED", with C4T-SR as its deciding test. |
| L7 | §5.2 T2 numerics | `route_a.column_workers` is exempt from C4T-D6's byte-equality. C4T-D6 runs serial route A (A23 wave 1). The exemption rests on COMPARE_DECIDING_II `e1d3c072` (parallel N8 ≡ serial bitwise at A2F10) and is a declared difference. |
| L8 | §1.6, §8 | New certificate **LO-NGC** on the saved T120L state: shells (2,3], (3,4], (4,6], (6,8], (8,12], (12,16] in θ units; pass ≤ 0.005θ per shell and ≤ 0.05θ summed. Until it runs, the NGC lapse-only omission over (2,16] is UNTESTED (new §8 row), and N-test readings wait for it. |
| L9 | §1.5 | ∂v_i/∂λ := (\|v_i(C4T-A) − v_i(C4T)\| + E_i(C4T-A, C4T))/0.05, conservative. The noise contribution 2κ_i·ε·E_i/0.05 is recorded. |
| L10 | §5.3 T1 | Literal V005 text: "Pass iff cases C2T, C3T, C4T are valid AND D̂_T(3,4) ≤ 1 AND D̂_T(3,4) ≤ 0.5·D̂_T(2,3)". |

---

## Part 2. Implementation amendments found while implementing the library (module lane)

Each of these was found by a test in `tail_scheme_impl_c2/module/` and is applied in the module. Each one changes or specifies a V002 sentence. They need review with the module.

### IA1. Corner-zone quadrature in α = arccos(L/k⊥) on phase-limited panels (V002 §1.2, "uniform panels")

- **Defect 1 (TESTED-NEGATIVE for the V002 wording).** On K < k⊥ ≤ √2K the weight 8α(k⊥), and every sin(4jα), has a square-root endpoint singularity at k⊥ = K⁺. Uniform-panel GL then converges only as w^1.5 (module test (h), H1–H2):
  - GL8 on one panel of ∫√x has relative error 2.5e-4.
  - The DDO K=4 corner zone at w = 0.05 has error 1.4e-6 with uniform-k GL, against 1.3e-15 in α.
  - The design prototype's tail value at R = 0.4 kpc is off by 7.07e-7, 2.49e-7 and 8.8e-8 (the tail is 0.0755) at w = 0.25, 0.125 and 0.0625. The ratio is 2.83 ≈ 2^1.5.
- **Defect 2 (found in this lane, TESTED).** Mapping to α inside k-uniform panels alone (the first form of this fix) leaves the corner harmonics sin(4jα) under-resolved in the first panels: with 4j up to √2·L·R + 40, the first DDO K=4 panel spans 0.157 rad of α.
  - The lane's first final run (module `out/*_V001.json`) failed test (b) `NGC_cyl4_stars_H2_value` at 5.7e-8 of max\|t\|.
  - At R = 134.7 kpc the error was 9.4e-6 of the local value; plain uniform-k GL gives 5.0e-5 (H4).
- **Fix (rule `alpha_phase`).** An interval that starts at a cube corner L is integrated in α, with k = L/cos α and dk = L sin α/cos²α dα. Panels are marched from α = 0 with α_next = min(α + 1.5/(√2·L·R_eval,max + 40), arccos(L/(L/cos α + w⊥)), arccos(L/b)). So every panel keeps k-width ≤ w⊥, and the highest harmonic phase is ≤ 1.5 rad.
- **Node counts** (module grid builder):

  | | design V002 N⊥ | IA1 N⊥ |
  |---|---|---|
  | DDO K = 2 | 5128 | 5336 |
  | DDO K = 3 | 5128 | 5360 |
  | DDO K = 4 | 5128 | 5376 |
  | DDO K = 6 | 5128 | 5440 |
  | NGC K = 2 | 25608 | 26304 |

  N_z⁺ is unchanged (12800 / 18288).
- **Memory.** The NGC tail estimate stays under the 0.6 GiB cap (module test (f)).
- **Prereg wording.** The R1 prereg JSON (`production_tail.quadrature.corner_zone_rule`) names IA1. The exact panel-marching rule is the one stated here, implemented in the module's `_alpha`. The JSON's `N_perp` entry defers to this table.
- **Result (TESTED).**
  - The library is converged: w 0.1/o8 vs 0.05/o12 differ by 1.5e-15 (H2), and at H4 by 1.7e-15.
  - The w^1.5 Richardson extrapolation of the prototype agrees with it to 1.2e-8 of max\|t\| (test a).
  - The independent implementation (geometric grading, ψ-brute force, no α map) agrees to ≤ 6.6e-13 of max\|t\| on the DDO rows and NGC rings (test b) and to ≤ 3.2e-15 on the C4R3 column points (test e). Values are in `TEST_B_INDEPENDENT_V002.json` and `TEST_E_B3_LAPSE_PAIR_V002.json`.

### IA2. Stellar exponential tail rule (V002 §1.3, "u-map exponential tail with 256 nodes", "doubling-certified to 1e-10")

- **Defect (TESTED-NEGATIVE; module test (h), H3).** With the u = exp(−(R−R_last)/a) map and 256 GL nodes, the declared doubling certificate fails.
  - DDO at k⊥ up to 32 /kpc: max\|ΔP\|/max\|P\| = 8.6e-6 (256 → 512 nodes); 512 → 1024 gives 2.2e-6.
  - NGC (stars + H₂) at 16 /kpc: 5.5e-6 and 1.5e-6.
  - J0(kR) oscillates without bound as u → 0, so GL in u converges only algebraically.
- **Fix (rule `t_panels_40a_phase1p5_gl12`).** R = R_last + a·t with t ∈ [0, 40]; the omitted weight is e^{−40}. Uniform t panels with phase k_max·a·Δt ≤ 1.5 rad, GL order 12 per panel. Segments keep `max16_ceil_kdr_plus8`.
- **Result (TESTED).** Doubling change 4.0e-16 (DDO, 32 /kpc) and 4.8e-16 (NGC, 16 /kpc). An independent composite-GL20 transform agrees to ≤ 6.5e-16 (test b).
- **Config key.** `stars.tail_nodes` is replaced by `stars.tail_rule`; the V002 key is refused.
- **Cost.** The NGC stellar + H₂ transform at 16 /kpc is the largest single build item; it is measured in module test (f) and is an UNTESTED estimate otherwise.

### IA3. Sphere C (V002 §1.2: "Sphere and cylinder C give full rings only"; the curved boundary's quadrature was not specified)

- The tensor part treats the sphere as the cylinder (K, K).
- The piece cyl(K,K) ∖ sphere(K) is added on a smooth map: k⊥ = K cos γ, k_z = K sin γ + K(1 − sin γ)u, panels by the same phase rule. Its entries are scattered in k_z and evaluated by direct sum, so the per-point cost grows with its entry count.
- **TESTED** on the synthetic source (test a, A4): the sphere-C and cylinder-C tails equal the whole-space field minus an independently integrated inside region to ≤ 5e-15 of max\|t\|.
- Production cost and memory for sphere C (S4T, NGC N2) are UNTESTED. The build refuses above the 0.6 GiB cap.

### IA4. One source family

`lapse_pair` refuses ns ≠ 1 (`UV_TAIL_SINGLE_SOURCE_FAMILY_REQUIRED`). The tail is the field of the total source; the route-A facade already requires ns = 1.

### IA5. File names

- The library file is `owned_uv_tail_lapse_v001.py` (the commissioned name), not V002 §3.1's `lib/owned_uv_tail_lapse_c2v001.py`. The roster is `uv_tail_source_roster_c2v001.py` and the provider is `posix_libm_bessel_jn_provider_c2v001.py`, all in `tail_scheme_impl_c2/module/`.
- Successors pin these files by sha256.

### IA6. Certificates and admissibility

- `eps_certificate` / `lo_certificate` take either {path, sha256}, verified from the file's bytes at build (`UV_TAIL_CERTIFICATE_MISSING` / `_MISMATCH`), or the sentinel `NONE_TEST_ONLY`.
- A state built with the sentinel, or with a synthetic roster, carries `production_admissible: false`. Successor stages must refuse such a state.
- The I1-T record must have verdict PASS; NOT_APPLICABLE_SYNTHETIC is accepted only for a roster whose kind is `synthetic`.

### IA7. Interfaces made explicit

- Roster interface: `radial_factors(k⊥, j0)`, `vertical_factors(k_z, c)`, `extent()`, `record()`, `digest()`; S_T = P @ Fᵀ.
- `stars_registered` takes `units` {kpc_m, solar_mass_kg}.
- `roster_route_a` mirrors solver L215 (gas = (1−r)gas + r·updated) with coefficients built by the same recursion, and collapses azimuthal elements onto their column radius. This is the declared m = 0 projection.
- Radius snapping: a query radius within 8 ε of a declared radius uses that radius's table. Any other radius gets an on-demand table (counted in `diagnostics.on_demand_radius_builds`, LRU of 16).
- `field_bound` uses node-assigned unit shells from min K. It is an estimate; ε is EPS's estimate.
- `monitor_MT` takes v_ref and τ in km/s.

### IA8. Packet-transform replicas

`packet_transform` implements the cited formulas: ring J0 for prep analytic and feedback v002/v004; the Cartesian forward sum for `physical_source_fourier` and the offset. It does not replicate the stages' batching byte for byte. T2-I (≤ 1e-12 against the stored C6 sources) is the deciding test. I1-T on the saved C2R3/C3R3/C4R3 states, for stars plus the le3 source gas rings, passes at ≤ 7.8e-15 (module test (d)). The route-A mixture and body rosters (`roster_route_a`, `roster_body`) are implemented from the cited formulas but are not exercised against saved packets here (UNTESTED; deciding test: I1-T in the route-A and body successors).

---

## Status (TESTED / UNTESTED)

- TESTED here: IA1 (both defects) and IA2, by the module tests named (`tail_scheme_impl_c2/module/out/TEST_*_V002.json`).
- Unchanged from V002/CHECK_V001 and still UNTESTED, each with its deciding test:
  - all T outcomes (the V007 runs);
  - b_K (SR-K);
  - RB-FP (AMP run);
  - ε above 6.9 /kpc (EPS);
  - LO and LO-NGC;
  - B3 by an independent lane (the module lane ran a pre-gate only);
  - gal_c2v005 ≡ gal_c2v004 at 4.04 Mpc (deciding (i));
  - NQ;
  - costs;
  - NGC result assembly under v010;
  - sphere-C production cost.
