# FINDINGS_B2 (Claude3 builder B2, root dispatch 0597) -- working notes, appended as work proceeds

Started 2026-10-18T18:35Z (`date -u`). Lane: Claude3 (review lane), builder B2. Nothing posted to FROM_*.
Read-only outside `claude_artifacts/gate_b2_c3/`.

## 1. Definition as read (texts cited)

* V007 final draft (r1 file, `v007_final_prereg_c4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT.md` L141; JSON
  `gates_before_any_T_result.B2`, sources ["R1"]); text identical in r1 prereg draft
  `tail_scheme_design_c2/v002/r1/KMAX_TAIL_PREREG_V007_DRAFT_R1.json` L120 (sha c691cab6.., = r11 PIN_DRAFT_R1):
  > static rows on saved C2R3/C3R3/C4R3 le3 (rotation_v005 uvt successor + unchanged column mean; continuum_v001,
  > O = cube 12) equal to an independent Cartesian tensor-GL implementation (box(12)\cube(K), 16 azimuths, no symmetry
  > reduction) to <= 1e-4 km/s per row; sanity vs study ADV_TAIL_CHECK KB12 within the m16 alias + star-roster
  > difference (<= 0.05 km/s)
* Design text behind R1: `tail_scheme_design_c2/v002/TAIL_SCHEME_DESIGN_V002.md` §4.4 (L559-563): production rows =
  rotation-v005 successor + unchanged column mean on saved C2R3/C3R3/C4R3 le3 inputs, tail config continuum_v001 with
  O = cube K_out = 12 "so that a Cartesian check is affordable"; checker = Cartesian tensor GL on box(12)\cube(K), full
  box, no symmetry reduction, 16 azimuths, <= 1e-4 km/s per row; sanity within m=16 alias + star-roster difference
  (<= 0.05 km/s) of ADV_TAIL_CHECK KB12 rows (adv_tail_check_v001 67a6eeb6). §1.1 (L110-127): δn_T = packet_K + t,
  t(x) = ∫_D T∞(k) S_T(k) e^{ik·x} d³k/(2π)³, T∞ = 1/(4γ_eff|k|²), D = O\C; for B2/B3 O = cube [-K_out,K_out]^3.
* Root rulings: V005 addendum A87 (CLAUDE2/ROOT_DECISIONS_..._V005_ADDENDUM.md L905-913): B2 owner Claude3, 0597,
  "A FIELDS-shape record from an independent lane". No other ruling in V004/V005 changes the B2 text (grep of both
  addenda for B2: V004 hits are unrelated item labels; V005 L276/L689/L696 are unrelated compare-review item labels).
* Gate: r11 compare `g_B2` (kmax_tail_compare_c2v007_r11.py a5d10cb1.., L3007-3018) + FIELDS_R11 §6 B2 + common
  fields (schema, gate, verdict, producer{path,sha256} root-registered, record sha root-registered in gate_records).

## 2. Plan

1. Locate the production static-row path (rotation_v005 uvt successor, column mean, continuum_v001 roster,
   O = cube 12) in tail_scheme_impl_c2 (module / driver_r5 / certificates_v001 SavedR3 / doubling_v001 proxy).
2. Path 1 = production rows via the production library on the saved R3 le3 inputs (static replay only).
3. Path 2 = own Cartesian tensor-GL tail over box(12)\cube(K), full (kx,ky,kz) box, no symmetry reduction, 16
   azimuths, z = 0 ... column points, own source rebuild from saved arrays + registered stellar profile, own
   rotation-law/row assembly through the pinned column-mean adapter. No import of the tail library.
4. Per-row diffs, max per state; sanity vs ADV_TAIL_CHECK KB12 (W025_O6) rows; explain allowance.
5. Convergence: refine GL order / panel widths for path 2.
6. Record (exclusive create) + TEST-registry check with r11's evaluate_gate('B2', ...) via the Claude3 guarded loader.

## 3. Production path and static-row quantity (determined from bytes; 19:05Z)

* **Production stage** (driver v010 r5 `galaxy_m0_forward_c2v010.py` b5cc62af, SCRIPTS_UVT L323): rotation-v005 uvt successor
  `driver_r5/cascade/tail_scheme_impl_c2/route_b/stages/ddo_free_surface_rotation_root_v005_gal_c2v005_uvt_c2v001_r5.py`
  (8459ce3c), shared binding `uvt_route_b_binding_c2v001_r5.py` (1e27430c), library `driver_r5/module/owned_uv_tail_lapse_v002.py`
  (2026f2b6), roster 4366e3d6, Jn provider d6c55b55 (UVT_LIB L316-319). Static diffs: the r5 successor differs from
  route_b/stages/..._uvt_c2v001.py only in the UVT_BINDING pin line (L189); the r5 binding only in the lib pin (L40); lib v002
  differs from v001 c28d4209 only in TAIL_MEMORY_CAP_BYTES (L37).
* **Unchanged column mean**: gal_c2v005 `ddo12_lower_entropy_column_mean_root_v004_gal_c2v005.py` (ae78b012; driver r5 SCRIPTS
  L203), rows = adapter v002 on speed = R*Omega, weights = col weights_m*rho0*HI ratio (L208-227).
* **Static row quantity** (rotation successor L279-293 + `owned_free_surface_rotation_v001.py` e1b354ec): per column node and
  azimuth phi_j = 2 pi j/16 the field is the kept packet plus the tail jet in the additive boundary slot (L282
  `evaluate_line(..., **uvt.line_jets(line,z))`); PR = c^2 (g_R)/(1+f0) incl. tail (L289); pr = 16-azimuth mean (L292);
  rotation law Omega^2 = (C_R - h k/gamma)/R with C_R = ((gamma-1)Sigma_R + k Sigma + B)/A, B = sum_l w rho/h pr: LINEAR in pr,
  Phi_z does not enter Omega^2. Rows = column mean of R*Omega. "Static" = the tail is added to the saved le3 field with no
  column re-solve or feedback.
* **le3** = stages 17_le2_feedback (field + gas source), 18_le3_columns_00, 19_le3_rotation, 20_le3_column_mean of each saved
  R3 run. NOTE: C3R3's final pass is le4 (4 passes reported; le3 vs le4 saved rows differ <= 2.3e-3 km/s); ADV_TAIL_CHECK and module TEST_D used the final pass (le4 for C3R3);
  the route-B lane test and this gate use le3 for every state (R1 wording).
* **Tail source for le_rotation** (binding L455-470): stars_registered (f5becd45) + roster_rotation of the le2 rotation the le2
  feedback transformed (--uv-tail-source-rotation-directory), continuum_v001 (design V001 sec 1.3: stars P_* x/sinh x; gas
  cubic-in-s Lagrange through each annulus' 4 GL4 nodes, M_s Gauss nodes per annulus).
* **Interpretation chosen for the uv_tail block of the production replay**: the registered production C4T block (template
  C4T_P128_MS128_CX1V003 088902fb numerics.uv_tail: order 8, w_perp 0.05, w_z 0.02, domain 14.2/35/32 kpc, M_s 128, stars
  rules, lambda 1) with exactly two declared changes: outer -> cube K_out 12 (B2's O) and certificates -> NONE_TEST_ONLY
  (static replay, --uv-tail-admit-test-only). Reason: B2 checks the production implementation; only the O named by B2 is
  changed. (The route-B lane's own pre-check used the module test-(d) w_z rule and M_s 64; its rows are a cross-reference.)
* **Driver/shim**: the replays run the r5 driver's own single-stage shim (`galaxy_m0_forward_c2v010.py _stage request.json`,
  stage_main L791-814: module patches, stage globals, argv, stage main). No `run`/`dry-run` command, no route A, no driver run.
* r6 (if adopted for the seal) pins owned_uv_tail_lapse_v003 (e733eb1e) = v002 + an optional table cache (default off
  executes the v002 statements, per its header). Not re-tested here.

## 4. Path 1 launched 18:53:35Z (3 ROT_ON stage replays under taskpolicy -b, then 3 CM_ON); script
`scripts/b2_path1_replay_c3v001.py` (8344c998). Path 2 = `scripts/b2_independent_c3v001.py` (own J0, own sources, full-box
Cartesian GL, 16 azimuths). Path 1b = `scripts/b2_path1b_module_components_c3v001.py` (production library in-process, per source
component, for the sanity clause and the z = 0 row-radius proxy).

## 5. Sanity clause: reading (judgement call, to be confirmed by root)

ADV_TAIL_CHECK KB12 (adv_tail_check_v001 67a6eeb6) has, per state, variants box_discrete, disk_discrete, box_gas_only,
box_stars_cont_only, each with P16 (16-azimuth) and m0 (J1) readings; its gas is always the DISCRETE ring roster, its only
continuum source is the stars (own 48/200-node roster). B2's production source is continuum_v001 (continuum stars AND the
cubic-in-s continuum gas). The clause names exactly two allowed differences, "the m16 alias + star-roster difference". The only
ADV variant whose difference from B2 consists of exactly those two is box_stars_cont_only (same O = box 12 \ cube K, same
continuum star physics, different star radial roster; P16 vs m0 = the m16 alias). The R1 author's own module test (TEST_D D3,
module/tests/test_d_b2_replay_v001.py) implemented the clause the same way (stars-only vs box_stars_cont_only P16).
Primary reading: sanity_vs_KB12 = max_i |dv_i(stars-only, B2 production, P16) - dv_i(ADV box_stars_cont_only, P16)|, with the
m0 reading reported too (the alias is then inside the difference). A full-source comparison against box_discrete also contains
the discrete-vs-continuum GAS rule difference, which the clause does not name; it is computed and reported separately.

### 5a. Origin of the sanity wording (found 19:10Z)

TAIL_SCHEME_DESIGN_V001.md sec 4 L390-392 (the design R1 extends): B2 "must equal a checker's independent Cartesian
implementation (CHECK sec 2 method, 16-azimuth P16, the same declared rule and K_big) to <=1e-4 km/s per row. Sanity check only:
they must equal the study's m = 0 rows to within the measured m = 16 alias plus the star-roster difference (<=0.05 km/s)."
The study's continuum rule (UV_TAIL_STUDY_V001 V-c3: gas cubic-in-s per annulus, stars exact sech2 with a 64/256 roster) is
continuum_v001 up to the star roster, so in V001 the two named terms were exactly the two differences (P16 vs m0; star roster).
V002 sec 4.4 / R1 re-pointed the sanity at ADV_TAIL_CHECK KB12 (box outer, to match O = cube 12), whose gas is the DISCRETE
ring roster. Hence: primary reading = stars-only (the one ADV KB12 variant with continuum physics), value reported = the
larger of its P16 and m0 readings (conservative); full-source readings (box_discrete) are reported with an explicit
decomposition (gas rule, star rule, alias) and are not the gated number. Root should confirm or re-word the clause.

## 6. Path 2 (independent) method, as implemented in scripts/b2_independent_c3v001.py

* Imports: numpy, stdlib; the pinned observation module 8e30897e and adapter 6790e28e (the unchanged row pipeline the column-mean
  stage calls); libm j0 via ctypes ONLY to cross-check the own J0. Not imported: owned_uv_tail_lapse_*, uv_tail_source_roster_*,
  the Jn provider, any stage/binding, independent_tail_c2v001 (module lane), Claude4's b3 tools. The record carries a runtime
  scan of sys.modules for those names (forbidden_modules_loaded must be []).
* Own J0: periodic trapezoid of (1/2pi) int cos(x sin t) dt with N = 4 ceil((xmax+96)/4) nodes (error 2 J_N(x), < 1e-18), the
  4-fold node symmetry used inside the J0 evaluation only.
* Sources: stars P_* = 2 pi int Sigma J0 R dR with my own nodes (GL8 core, GL12 per linear segment, exponential tail on
  t in [0,44], panels dt <= 0.5, GL12), V = x/sinh x; gas P_i = int 2 pi R J0(kR) L_i(R^2) dR with GL(24) in R per annulus (the
  production integrates in s with M_s nodes), sigma_i = E_i/(2 pi w_i) from the le2 source rotation masses; discrete variants
  (ADV analogues): gas rings J0(k R_i) E_i, star GL4 rings (prep v007 analytic branch as described in design/ADV).
* Quadrature: one exactly symmetric axis rule on [-12,12] (GL order o on panels <= w between +-{0,2,3,4,12}), used for kx, ky,
  kz; full box; nodes with |kx|,|ky|,|kz| <= K masked out; P(kp) memoized per distinct kx^2+ky^2 value.
* Evaluation: all 72 x 32 le3 column nodes (R_i, z_il) of the saved le3 rotation + the 12 row radii at z = 0; 16 azimuths;
  value and d/dR, 16-azimuth means; then sum over kz with e^{i kz z}; real part (imag reported).
* Rows: Omega^2 = saved + sum_l w rho/h dpr/(A R), dpr = mean_j c^2[(g_R+t_R)/(1+f0+t) - g_R/(1+f0)] with the saved le3 per-azimuth
  f0, g_R; rows via the pinned adapter exactly as column-mean v004 L208-227. Controls: zero correction reproduces the saved le3
  rows bitwise; A vs saved rotation_A; Phi_R recomputed from the saved fields vs saved Phi_R_full.
* Custody: own discrete gas rings vs the le2 feedback new_gas_fourier_J, own GL4 star rings vs the route-A fixed_source_fourier_J
  (3000 packet nodes each); source columns vs GL4 annulus nodes.
* Convergence plan: COARSE (w 0.5, o 8, nR 16) / BASE (w 0.25, o 12, nR 24, star rule x1) / REFINED (w 0.2, o 14, nR 36, star
  rule x2: segment GL24, tail dt 0.25).

## 7. First results (19:19Z)

* PATH 1 C2R3 done (ROT_ON 1388 s, CM_ON 10 s, exit 0). Stage tail record: state ff5ca4e1..., non-empty, I1-T 6.25e-15 PASS,
  kept cube K 2, outer cube 12, quadrature order 8 / N_perp 3432 / N_z+ 4800 (w_z 0.02), production_admissible false,
  test_only_admitted true, 36864 jet calls. Rows equal the route-B lane's own c2v001-successor replay (M_s 64, w_z 0.0816) to
  1.0e-13 km/s, and the module-lane "independent" to 2.7e-7 km/s.
* PATH 2 smoke test COARSE (w 0.5, o 8, nR 16; 384 nodes/axis, 56.6M box nodes, 56.4M in D): C2R3 rows vs PATH 1 = 3.8e-11 km/s
  (exact-form dpr); the purely linear dpr differs by 2.7e-7 km/s (the 1/(1+f0+t) factor). Controls: zero correction reproduces
  the saved le3 rows bitwise, A and Phi_R reproduce exactly (0.0). Custody: own gas rings vs new_gas_fourier_J 6.4e-15, own
  GL4 star rings vs fixed_source_fourier_J 1.4e-15. Imag/real <= 4e-17. No forbidden module loaded. Own J0 vs libm j0: 4.9e-15
  abs over 220k points in [0, 300].
* Decomposition (COARSE, C2R3): gas rule (continuum minus discrete gas, continuum stars both) up to 0.079 km/s (row 08); star
  rule up to 0.030 km/s; own discrete source reproduces ADV box_discrete P16 to ~5e-4; own stars-only reproduces ADV
  box_stars_cont_only P16 to ~1e-4.

(Correction 19:30Z: section 3 originally said "C3R3 ... (5 passes)"; the run reports 4 passes, le4 final; line 56 was edited
in place to say so. Saved le3 vs le4 rows of C3R3 differ by <= 2.3e-3 km/s; C2R3 and C4R3 final pass = le3.)

## 8. Path 1 complete (19:28:43Z, 2106 s); BASE path 2 for C2R3/C3R3

* PATH 1 all 6 jobs exit 0; summary out/B2_PATH1_REPLAY_C2R3_C3R3_C4R3_C3V001.json (9720404b...). Stage tail digests:
  C2R3 ff5ca4e1..., C3R3 6b9c5702..., C4R3 c15f202c...; I1-T 6.2e-15 / 7.4e-15 / 6.0e-15 PASS. Rows vs the route-B lane's own
  c2v001-successor replay (different quadrature config): 1.03e-13 / 1.21e-13 / 1.35e-13 km/s.
* PATH 2 BASE (w 0.25, o 12, nR 24; 1152 nodes/axis; 1.529e9 box nodes, 1.522e9 in D for C2R3): rows vs PATH 1:
  C2R3 6.47e-12, C3R3 6.45e-12 km/s; BASE vs COARSE (C2R3) 3.6e-11 km/s.

## 9. BASE results all states + path 1b (19:36Z)

* PATH 2 BASE vs PATH 1 (gate quantity, max over 12 rows): C2R3 6.47e-12, C3R3 6.45e-12, C4R3 3.12e-12 km/s.
* PATH 1b (production library in-process): rebuilt full-roster state digest == the stage's digest (C2R3, C3R3); stars-only
  production vs own stars-only 0.0 / 7.1e-15 km/s; gas-only 1.3e-13 / 1.4e-13 km/s; z = 0 row-radius proxy production vs own
  2.8e-13 / 2.7e-13 km/s; production linear channel vs the stage 2.7e-7 / 2.0e-7 km/s (the 1/(1+f0+t) factor).
* Sanity (C2R3 / C3R3): primary stars-only vs ADV box_stars_cont_only: P16 reading 3.98e-5 / 6.07e-5, m0 reading 1.32e-2 /
  2.39e-2 km/s -> reported value (the larger) 1.32e-2 / 2.39e-2 <= 0.05.
* Other readings (C2R3 / C3R3): full B2 vs ADV box_discrete P16 0.082 / 0.096, m0 0.042 / 0.046 km/s. Decomposition: own
  DISCRETE-source rows reproduce ADV box_discrete P16 to 1.1e-11 km/s for C2R3 (5.5e-4 for C3R3, where ADV used le4); the
  continuum-minus-discrete GAS rule difference is 0.079 / 0.095 km/s and the STAR rule difference 0.030 / 0.036 km/s. So the
  full-source gap is the unnamed gas-rule term, not an implementation difference.
