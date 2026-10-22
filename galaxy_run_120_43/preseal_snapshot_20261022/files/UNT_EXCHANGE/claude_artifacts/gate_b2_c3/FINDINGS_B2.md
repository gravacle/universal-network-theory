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
* C4R3 (19:40Z): path 1b digest == stage (c15f202c...), I1-T 6.0e-15; stars-only production vs own 7.1e-15, gas-only 1.6e-13;
  z0 proxy 2.8e-13; linear channel vs stage 1.3e-7. Sanity stars-only vs ADV box_stars_cont_only: P16 4.46e-5, m0 2.63e-2 ->
  reported 2.63e-2 <= 0.05. Full-source vs box_discrete: P16 0.108, m0 0.071 km/s (> 0.05); own discrete source reproduces ADV
  box_discrete P16 to 1.4e-12 km/s; gas-rule difference 0.111, star-rule 0.038 km/s.
* JUDGEMENT CALL (flag for root): under a full-source reading of the sanity clause (B2 rows vs ADV KB12 box_discrete), the
  clause would read > 0.05 km/s for every state at P16 (0.082 / 0.096 / 0.108) and for C4R3 at m0 (0.071). That excess is the
  discrete-vs-continuum GAS rule (0.079 / 0.095 / 0.111 km/s), which the clause does not name; the implementations agree (own
  discrete rows = ADV rows to 1e-11..1e-12 km/s, C3R3 5.5e-4 because ADV used le4). The record gates the stars-only reading.
* REFINED table (w 0.2, o 14, nR 36, star rule x2; 1680 nodes/axis, 353220 distinct kp) written 19:39Z (606 s); the three
  REFINED state runs launched 19:39:50Z.

## 10. A94 applied (2026-10-18 19:45Z) -- SUPERSEDES sections 5 and 5a and the "JUDGEMENT CALL" bullet of section 9

Received from the coordinator: ROOT RULING A94 (dispatch FROM_CODEX/0612_2026-10-18_claude3_B2_follows_text_A94.md, sha256
00c2147117aaee7059533a03cbd42fd71d5a0617323114150610a933ab506750, from bytes; the ruling text is in the V005 addendum, section
"A94: B2 follows its controlling text exactly (Codex2 0480) (2026-10-18 19:40Z)"). Sections 5 / 5a (stars-only primary reading,
max-of-P16-and-m0 value) are SUPERSEDED and are not used in the record; they stay above unedited as the record of what was
first proposed.

Applied:
1. Gated per-row clause: full static rows (continuum_v001 stars + the REGISTERED continuum_v001 gas) on saved le3 of all three
   states, production (path 1) vs independent full-box tensor GL (path 2): unchanged (BASE <= 6.5e-12 km/s).
2. Gated sanity, per state: max_i |full B2 production row (P16) - ADV_TAIL_CHECK KB12 box_discrete row (P16)|, tolerance
   0.05 km/s, no allowance subtracted. box_discrete = the only full-component variant on box(12)\cube(K) (disk_discrete has the
   cylinder domain; box_gas_only and box_stars_cont_only are component subsets). Statistic P16 (the text's); m0 supplementary.
3. C3R3: B2 rows are on saved le3 (complete); ADV KB12 C3R3 was computed on le4 (its final pass) -> the C3R3 sanity clause is
   INCOMPLETE ("no le3 KB12 reference; ADV C3R3 is le4"); the le4-based reading is supplementary only.
4. Decompositions (gas rule, star rule, own-discrete vs ADV, stars-only, m0, z0 proxy) go to a DIAGNOSTIC section only; never
   subtracted, never relabelled as allowed.
5. Every interpretive step -> ROOT_ITEMS (record + here). Verdict follows the gate; a FAIL on any state dominates.
Expected from BASE numbers: sanity C2R3 0.082, C4R3 0.108 km/s > 0.05 -> B2 FAIL (C3R3 sanity INCOMPLETE).
Record producer: a NEW script b2_record_c3v002.py (b2_record_c3v001.py was never run; it is superseded before use and kept).
(Timestamp note: section 10 was written at 19:42:47Z by `date -u`; its heading's "19:45Z" is wrong.)

## 11. FINAL (A94 applied; 2026-10-18 19:52Z)

**Record:** out/B2_GATE_RECORD_C3V002.json, sha256 d4b41ffcab00a05bf0bead8c943b8f3555fdeb91beda2cba430efa65431315d7,
verdict **FAIL** (producer scripts/b2_record_c3v002.py aae742cb...; numbers_producer scripts/b2_independent_c3v001.py 6c013801...;
input map out/B2_RECORD_INPUT_MAP_C3V002.json 63bb1190...).

| state | rows clause: max_row_diff (km/s) | gated sanity, P16 vs ADV KB12 box_discrete (km/s) | clause status |
|---|---|---|---|
| C2R3 | 6.47e-12 (PASS) | 0.0821 (row 08) | FAIL (> 0.05) |
| C3R3 | 6.44e-12 (PASS) | not gated (field omitted) | INCOMPLETE: no le3 KB12 reference; ADV C3R3 is le4 (le4-based supplementary 0.0979 rows / 0.0956 shifts) |
| C4R3 | 3.12e-12 (PASS) | 0.1083 (row 08) | FAIL (> 0.05) |

Supplementary (not gated): m0 readings 0.0422 / - / 0.0711 km/s. Convergence of the independent lane: REFINED - BASE <= 4.3e-14 km/s,
BASE - COARSE <= 3.6e-11 km/s, production - REFINED <= 6.5e-12 km/s (all states). Diagnostics (never subtracted): gas rule
0.079 / 0.095 / 0.111, star rule 0.030 / 0.036 / 0.038 km/s; own discrete source vs ADV box_discrete 1.1e-11 / 5.5e-4 (le3 vs le4) /
1.4e-12 km/s; force level stage vs independent <= 9e-13 relative; stage tail digest == in-process rebuild (all).

**r11 (a5d10cb1) evaluate_gate('B2') via the guarded loader, TEST registry** (out/r11_test/B2_R11_EVALUATE_C3V002.json 4e0895f7...):
record -> RECORD_DEFECT [GATE_RECORD_FIELD_MISSING:B2:per_state/C3R3/sanity_vs_KB12_km_s] (the INCOMPLETE C3R3 clause; the
producer/registry/record-sha checks pass); probe p1 (NOT a record; C3R3 field = the le4 supplementary value) -> FAIL
[VERDICT:B2:FAIL, B2_C2R3_SANITY_GT_0.05, B2_C3R3_SANITY_GT_0.05, B2_C4R3_SANITY_GT_0.05], no ROWS code; n1/n2 negative controls
RECORD_DEFECT as expected; guard refused 0.

ROOT_ITEMS B2-RI-1 .. B2-RI-10 are in the record (root_items) and in scripts/b2_make_inputs_c3v002.py.

## 12. A97 (started 2026-10-18 20:07Z): decompose the B2 sanity miss by computation

Task from the coordinator: ROOT RULING A97 (V005 addendum "A97: the B2 sanity clause fails as written. Diagnose it before
anything else (2026-10-18 20:02Z, before any T result)"; dispatch FROM_CODEX/0618_2026-10-18_claude3_codex2_B2_sanity_decomposition_A97.md,
sha256 78ba2e9a645cbdf3d31e2dc4dcc35b552e2af323500383bd81b3a0b8d9ab9d01, from bytes). The B2 record d4b41ffc is NOT modified.
Plan: (1) inventory of every ADV-vs-B2 difference with file:line on both sides; (2) a variant matrix computed with my own
in-process independent code (reusing b2_independent_c3v001 functions by import), switching one difference at a time from B2
toward ADV and from ADV toward B2, P16 and m0 (own J1), exact and linear readout, my quadrature and ADV's axis rule (o6, w0.25);
(3) C3R3 on le3 (ADV-equivalent) and on le4 vs ADV's actual C3R3 rows; (4) named-only residual under readings (i) roster only,
(ii) roster + star representation; (5) shared-input checks. Outputs: out/B2_SANITY_DECOMPOSITION_A97_C3V001.json, scripts, manifest.

### 12a. A97 partial results (20:19Z; COARSE and ADVQ matrices; BASE spot checks running)

Tools: scripts/b2_a97_variants_c3v001.py (variant matrix; imports b2_independent_c3v001 6c013801 by pin), b2_a97_inputs_check_c3v001.py,
b2_a97_inventory_c3v001.py (out/a97/INVENTORY_A97_C3V001.json 92e2201c, file:line on both sides), b2_a97_decompose_c3v001.py.
Checks: own J1 vs libm 3.6e-15; my replicas of ADV's star rosters equal ADV's own stars_from_prep (loaded from its pinned bytes)
exactly in R (and z, w) and to 2e-16 in mass, for the continuum 48/200 roster and the discrete GL4 rings.
Equivalence: my code at ADV's axis rule (ADVQ: GL6, 0.25 /kpc, mirrored full box) reproduces ADV's SAVED box_discrete rows
EXACTLY (P16 0.0, m0 <= 7e-15 km/s) for C2R3 and C4R3, box_gas_only to 7e-15, box_stars_cont_only to 0.0; on C3R3 le4 inputs
(ADV's state) at COARSE to 1.6e-11 km/s (all variants).
Inputs check (out/a97/INPUTS_CHECK_A97_C3V001.json 7fc1beb0): C2R3 / C4R3 -- ADV used le3, the same tail gas source file
(15_le2_rotation; masses bitwise equal), the same columns, units, K, profile (f5becd45), forward_v002 (e9be043b), binding,
adapter, observation and gamma; the production replay argv differs from the saved le3 request only in the declared keys,
module patches equal, and its evaluation geometry is bitwise the saved le3 arrays. C3R3 -- ADV used le4 (source 19_le3_rotation,
masses differ up to 7.6e-4 rel). No production or shared-input error found.
COARSE numbers (km/s, max over rows; P16 unless stated): C2R3 / C3R3(le3) / C4R3
  gas rule (continuum -> discrete, one switch from B2)      0.0790 / 0.0954 / 0.1114
  star representation incl. roster (continuum -> GL4)        0.0301 / 0.0356 / 0.0384
  star radial roster only (production -> ADV 48/200)          3.93e-5 / 4.42e-5 / 4.46e-5
  named-only residual (i)  P16 / m0                           3.93e-5 / 0.0104 ; 4.42e-5 / 0.0210 ; 4.46e-5 / 0.0260
  named-only residual (ii) P16 / m0                           0.0301 / 0.0318 ; 0.0356 / 0.0379 ; 0.0384 / 0.0427
  C3R3 le3 sanity computed the same way (vs own ADV-equivalent on le3): 0.0951
Correction to my earlier citations (FINDINGS sections 3/6 and the B2 record text, not edited): in the r5 rotation successor the
azimuth is L277, N = 1+f0 L284, PR L287, the 16-azimuth mean L291 and the rotation-law call L292 (I had cited L281 / L289 / L292).
* 20:22Z: C3R3 le4 at ADV's axis rule: my ADV-equivalent reproduces ADV's actual C3R3 rows exactly -- box_discrete P16 0.0 / m0
  7e-15, box_gas_only 0.0 / 0.0, box_stars_cont_only 0.0 / 0.0 km/s (the saved le4 rows equal ADV's rows_saved bitwise). So the
  method is ADV's to the last bit on every state ADV computed. Attribution at the argmax row 08 (COARSE, P16, km/s; exact telescoping
  closes to 0.0): C2R3 total 0.08214 = gas rule 0.07899 + star representation 0.00314 + star roster 4.7e-6 + readout 2.9e-8 + quadrature
  -1.1e-11 + implementation 1.0e-11 + interaction 4.9e-6; C4R3 total 0.10833 = gas 0.11138 - star rep 0.00306 + roster 1.06e-5 + readout
  2.3e-9 + interaction -6.8e-6; C3R3 (le3, vs own ADV-equivalent) total 0.09506 = gas 0.09537 - star rep 0.00032 + roster 6.7e-6 +
  readout 1.5e-8 + interaction -1.3e-6. BASE spot checks running (C2R3, C4R3, C3R3 le3).

### 12b. A97 decomposition of record (2026-10-18 20:38Z)

out/B2_SANITY_DECOMPOSITION_A97_C3V001.json, sha256 ca1c53eb803fb2726a52ff33c898009992c9007b425ca88a3c635bc3465f13ef (producer
scripts/b2_a97_decompose_c3v001.py 79c9db31...). Its summary values are identical to the dry run DRYRUN_PARTIAL a8ecc26e (posted as
0082); it adds the BASE spot checks for all three states (BASE - COARSE <= 3.6e-11 km/s on every headline term), the primary rows
clause copied from C3V002, the C3R3 le4 facts and the reading (ii) reference at ADV's own axis rule (ADVQ: exact readout differs from
the value of record by <= 5e-11 km/s; linear readout by <= 7.4e-8 km/s).

## 13. A100 applied (2026-10-18 20:39Z): B2 re-issued as C3V003

ROOT RULING A100 (V005 addendum "A100: B2 is disposed under A97(a)"; dispatch FROM_CODEX/0622_2026-10-18_claude3_codex2_B2_disposed_A100.md
sha256 e6ae0c32632bfd77c8898d4bf598336941f237dfb22324bfbae0291d4bdd0509).
* Record: out/B2_GATE_RECORD_C3V003.json, sha256 915fbcda4f4a2cb5f61b257ff83494738144e177401c11c94e254c322df2411c, verdict PASS
  (computed); producer scripts/b2_record_c3v003.py 97b79bc8...; numbers_producer = the decomposition producer 79c9db31...; every one
  of its 57 numbers is quoted from the decomposition of record by JSON key path (quoted_values; all 57 re-read equal).
* Values of record (reading (ii), P16, against the unchanged 0.05): C2R3 0.030115451795659, C3R3 (le3) 0.03562258130412488, C4R3
  0.03835729098290841 km/s; rows clause 6.473e-12 / 6.445e-12 / 3.119e-12 km/s (C3V002 values).
* Reference basis as computed (A97/A100: unnamed differences switched to production): gas -> continuum_v001, readout -> the stage's
  form, quadrature -> the converged COARSE rule, inputs -> le3; stars = ADV's GL4 rings (named under (ii)); box(12)\cube(K); P16. The
  coordinator's 0622 relay mentioned ADV's axis rule GL6/0.25; the record carries both evaluations (C3V003-RI-1).
* Method wording fixed per Codex2 B2-METHOD-SCOPE (FINDINGS_CX2V001 e43dc88d): mean-coefficient method stated; no per-phase claim;
  per-phase equivalence UNTESTED; the linear diagnostics are not an ordering-error bound.
* Disclosure: raw misses 0.0821 / 0.0951 (le3, vs ADV-equivalent) / 0.1083; gas rule at row 08 = max over rows 0.0790 / 0.0954 /
  0.1114; reading (i) P16 3.93e-5 / 4.42e-5 / 4.46e-5, m0 0.0104 / 0.0210 / 0.0260; reading (ii) m0 0.0318 / 0.0379 / 0.0427; ADV's
  C3R3 = le4 (rows 2.31e-3 km/s, source masses 7.6e-4 rel); shared physical correctness NOT proven.
* r11 a5d10cb1 and r12 4bd7b262 (guarded loaders, TEST registries): main PASS [] on both; negative controls n1-n7 as expected on
  both (out/r11r12_test_c3v003/B2_C3V003_EVALUATE_R11.json 00d7cdee..., _R12.json 167a61a7...); guard refused 0.
* C3V002 (d4b41ffc) is untouched; C3V003 supersedes it.

## 14. ERRORS REGISTER (2026-10-18 20:43Z)

**E1 (process; raised by the coordinator after A100): scripts/b2_a97_decompose_c3v001.py was modified in place after it had produced an output.**
* c84df31a4930e27c1145f73a98a73afcc59e107701b4ae0f04e52e84e2a46dfa = the bytes that produced out/a97/DRYRUN_PARTIAL_DECOMPOSITION_A97_C3V001.json
  (a8ecc26e, 20:19:55Z; the values the coordinator cited in 0082). 79c9db314916c2d30280bf6e2c7d5715471dd8168b02a7991a27f08548569c3e = the bytes
  on disk now (mtime 20:34:40Z), which produced the decomposition of record out/B2_SANITY_DECOMPOSITION_A97_C3V001.json (ca1c53eb, 20:38:31Z;
  its producer field records 79c9db31, and the file was written by that run).
* What changed (from the session transcript; confirmed from bytes, below): two ADDITIVE in-place edits, no line removed or altered:
  (4) ~20:23Z: a 19-line block before `out['summary'] = summ` -- the BASE spot-check comparison (summary.<state>.BASE_spot_check);
  (5) 20:34:40Z: 3 lines before `out['c3r3'] = c3` (C3R3 numeric fields: ADV le4 baseline minus le3 rows, tail-source masses) and a 24-line
      block after `out['inputs_check'] = inputs_check` (reference_at_ADV_axis_rule; primary_rows_clause_of_record copied from C3V002).
  Why: to put every value the C3V003 record quotes into the decomposition file (A100 step 1), and the BASE spot checks. Neither edit
  touches any computation that produced the dry-run values; the final file's summary equals the dry run's summary key for key (checked
  20:38Z: "all dryrun summary keys equal: True" for C2R3, C3R3, C4R3), so the 0082 values are unchanged in ca1c53eb.
  Earlier in-place edits of the same file (~20:15Z: the ADV C3C4 pin placeholder replaced by the sha from bytes plus its check; ~20:18Z
  and 20:19:44Z: inventory / variant tables / ROOT_ITEMS embedding and the attribution table) were made BEFORE the dry run, before any output.
* Recovery: the c84df31a bytes are recovered bit for bit by removing the 3 + 24 + 19 inserted lines from the current file (sha256 of the
  reconstruction = c84df31a...). Saved under NEW names (nothing recreated at the old path): out/a97/RECOVERED_b2_a97_decompose_c3v001_AS_OF_c84df31a.py.txt
  (c84df31a...) and the unified diff out/a97/DIFF_b2_a97_decompose_c3v001_c84df31a_to_79c9db31.diff (7f74f482...; 46 lines added, 0 removed).
* Audit of every other file (scripts/b2_hygiene_inplace_audit_c3v001.py -> out/a97/HYGIENE_INPLACE_AUDIT_C3V001.json 6e18ea4a..., from bytes):
  since the C3V002 manifest (6e24c614) the only changed file is FINDINGS_B2.md (append-only notes); for every script, every output records
  its current sha, except DRYRUN_PARTIAL (the case above). No output was ever rewritten (all exclusive create).
  Other in-place edits, all BEFORE the script's first use (no output affected): b2_independent_c3v001.py (5 patches 19:05-19:10Z, first use
  19:17:30Z), b2_path1b_module_components_c3v001.py (19:03:29Z, first run 19:29:28Z), b2_record_c3v001.py (3 patches; never run),
  b2_make_inputs_c3v001.py (19:29:45Z; never run), b2_a97_inventory_c3v001.py (20:18:10Z, same command as its only run),
  b2_record_c3v003.py (20:37:17Z, before its only run 20:38:38Z). FINDINGS_B2.md line 56 (19:30Z; disclosed in section 8).
* From now on: new versioned filenames only (e.g. _c3v002.py); no re-edit of an existing file.
