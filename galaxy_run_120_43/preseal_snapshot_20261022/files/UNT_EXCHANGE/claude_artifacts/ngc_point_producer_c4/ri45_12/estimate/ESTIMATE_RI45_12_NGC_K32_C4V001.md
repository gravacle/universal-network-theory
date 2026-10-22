# RI45-12(i) estimate: one NGC step-5 point at interface A, K_big 32 / T120L (Claude4, C4V001)

From the Claude4 estimator helper (workflow `ri45_12/estimate`), for root dispatch 0677 item 2 (`e68feff083954a45fd1ccafa63cb2f117dbf990e3a4f9a784f9bd5faf9da7e17`) and its 0685 addition (`92d9943c764cb212305ad7200c4ff8e533f14f8446f0714c5a41777845b4d3cb`: the per-point wall at column_workers 8 alongside serial, the gain, and the identity-test cost). Drafted 2026-10-19T09:55:10Z (`date -u`).

This is target-free. No target or observed-velocity data, no run tree, and no runs_ext, C5H, `UVT_*` or UNT_INTERNAL_RUNS path was opened. Nothing was launched. No project code was imported or run, and no Python at all was run (§13). The numbers are arithmetic on values read from bytes, done in awk: `calc/estimate_c4v001.awk` (`1f0a3656e8049b8e688bb6c126bb82491eeb59edb224163094dbc9bcea272dcc`) writes `calc/NUMBERS_C4V001.json` (`76e5782670ef31f38d32b2ced143a9f3862828b3df4aae1eaa78d0a89fdd2866`). The JSON twin of this file carries the same numbers.

**How to read it.**
- E/U means expected/upper (the working reading, critic S7).
- Footprints are physical footprint, the quantity top MEM reports, never `memory_pressure` free %. GB = 1e9 B and GiB = 2^30 B.
- **TESTED**: read from saved bytes (a record, log or file size), or an arithmetic identity that reproduces saved bytes.
- **FORMAL**: read from code or a document, or arithmetic on FORMAL inputs.
- **ASSUMED**: a declared modelling choice, with its basis.
- **UNKNOWN**: no basis in bytes; a bracket only.

## 0. Bottom line

| quantity | E | U | where |
|---|---|---|---|
| Route-A tree, serial as the template runs it (stage 01 `route_a` + stage 02 `route_a_tail_manifest`) | **16.17 h** (58,208 s), I = 7 | **50.44 h** (181,598 s), I = 16 | §6 |
| Route B, stages 03-11+ | 12.85 h | 29.43 h | §8, an UNKNOWN bracket |
| Whole interface-A point, serial | **29.02 h** (104,455 s) | **79.88 h** (287,556 s) | §6 + §8 |
| Peak physical footprint of the process tree, serial | **7.73 GB** (build of state 7) | **14.06 GB** from code terms (build of state 16); **20.11 GB** with the DDO-measured excess | §6.3 |
| Steady footprint during the column phase, serial | 3.12 GB | 3.72 GB | §6.3 |
| Parallel-8 route A (needs a successor template and a TESTED identity) | 5.85 h, a gain of 10.32 h (2.77x) | 17.53 h, a gain of 32.92 h (2.88x) | §7 |
| Parallel-8 tree peak (the per-iteration transfer spike) | 45.2 GB | 61.3 GB | §7 |
| Recommended first-point caps, serial | RSS (physical footprint, process tree) **32 GiB** = 34,359,738,368 B (the A61 minimum is 30.17 GB); wall **360,000 s** (100 h) | | §9 |

What the bytes settle:
1. **q = 17 HI nodes per column at NGC.** The rule is q = 2 x hi_panels_per_side + 1 = 2 x 8 + 1. It is no longer an assumption (§2).
2. **Serial route A pays a source update every iteration** over 84,864 elements x 1,152,000 waves: about **2,770 s per iteration** (E). The old NGC plan has no such term (§5.2).
3. **The per-iteration `prepare` is a per-node Python solve at all 1,152,000 nodes**, about **575 s** (E). NGC goes through the streaming per-node Fourier facade. It does not use DDO's cached binding, whose prepare takes 7 s (§5.1).
4. **The template spawns no workers, so the A130 transfer spike does not apply to it.** Its spike is in-process instead: the build's vf transient grows by 0.637 GB per iteration (code terms), so **the last build is the run's peak** (§6.3).
5. **The old plan caps would stop the headline.** At E, the 5 GiB cap is crossed at the build of state 4 (the end of iteration 3), and the 43,200 s cap is crossed during iteration 5 (§9).

## 1. Inputs

| id | quantity | value | label | source (file:line) | sha256 |
|---|---|---|---|---|---|
| I1 | Template route-A mode | serial in-driver, column_workers 1, max_iterations 16; serial solver has no multiprocessing | FORMAL | driver cx3r008 L5058-5061, L5080, L5561-5564 (critic V6); solver grep 0 (critic V7) | driver 577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377; solver 8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469 |
| I2 | Per-iteration order in the serial solver | `begin_iteration` (tail state) L132, then `prepare` L133, the columns in roster order L173, the source update L215, `complete_iteration` (builds the next state) L223, then the convergence return L234 | FORMAL | solver 8ef3079b | as I1 |
| I3 | N_perp, N_z (K 2, K_big 32, order 8) | 51,904; 36,576 | TESTED | MODULE_ACCEPT_K32_V001 (u4 §2.3, u2 R5) | 18e4b8147cede8da7b9d50b6bf0a15c4180e2672997485c5129da3391559ad6f |
| I4 | Rank r | 157 (156 gas columns + stars) | TESTED identity | u4 §2.3 | map e793a32a20d4f4751b2c8cb720e46230697d6e5acb1257246d41188aa273be58 |
| I5 | TailState S | 232,598,248 + 1,755,656·nR B. That is 883,946,624 B at nR 371 and 506,480,584 B at nR 156 | FORMAL formula, TESTED constants | lib `build` L645-796, estimate L720 (u4 §2.2-2.3) | lib 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54 |
| I6 | nR (route-A eval radii) | 371 nominal; range 156 to 371+ | FORMAL; exact count BLOCKED_BY_FENCE | u4 §2.4 | |
| I7 | HI columns per iteration and their order | 4,992 = 156 radii x 32 azimuths, radius-major (all 32 azimuths of a radius in a row) | TESTED count; FORMAL order | PREP.json n_gas_columns (u4 §1.7); prep L179-189 | PREP 8d60a60b47aa2d7c62a76f70c894bc8042976cdf5a2aa2be227f93ab380715c8; prep 8681da84bbd2b6858f5334d724b4e22e10c191e68f305b6e29df841571bf712b |
| I8 | q, the HI nodes (= elements) per column | 17 | FORMAL rule x TESTED input | §2 | §2 |
| I9 | Process baseline B | 1,767,407,616 B | TESTED (the T120L iteration-0 replay peak) | u4 §7.4 (record 7922bb53, prefix as in u4) | |
| I10 | Stage start-up (prep) | 137.54 s; peak 1,172,307,968 B | TESTED | PREP.json timing (u4 §7.4) | 8d60a60b… (as I7) |
| I11 | Per-iteration `prepare` | E 574.82 s (the replay wall); U 941.55 s (2.25 x G80C prep 418.467 s) | E: TESTED value, FORMAL attribution. U: FORMAL | §5.1 | §5.1 |
| I12 | G80C tail-off column | 0.400747 s per column; 91.53 metric calls per column | TESTED | ADMITTED_POINT_RESOURCE_PLAN `measured_saved_G80C` | 4de87df93a56a5d996e6ce0e5652e81e2142e1b8e154c9cb58a5c2b98832ef77 |
| I13 | Tail unit cost per kz node | 11.33 ns (DDO K32-K128 `lapse_pair`, linear in N_z); 38.09 ns (K256 under load) | TESTED | KBIG_PROXY_V002.md §6; TIMING_V003.md §1 | 60bf995416b1d92c3945ba95390b8a02d384fa23489165b0f5b898078138da9b; 4d4cac0c275c40d4a149eca2b3bc3a9c519d7f8927864b85e6b33b077a443ec9 |
| I14 | Source-update rate | E 28.32 ns per (wave, element) pair (DDO F10: 103.5 s per iteration at 9,792 x 373,248); U 30.59 ns (DDO C4: 265 s at 9,792 x 884,736) | FORMAL record. The C4 wave count and the DDO module identity are ASSUMED | projection_c2v001.json, .py L19-24 | json cffa3150a2aac120bad1fdb045a93f645b938f76f22c3e8ff0bce56f387eaad2; py b3c678b5c93f68822922311cee5d441d779749dc53e623b818d173f801662209 |
| I15 | NGC source module | `baryonic_metric_source_columns_v003.py`, a dense chunked transform (wave_chunk 64, source_chunk 256), L136-208, loop L194-202 | TESTED sha; FORMAL code | prep L102; parallel solver L401-404 admits exactly this sha as row-separable | 81af8715eab45b8e34ca90b8db5c6c34ba471563fb9a9ecbbb5198a90b9081bc |
| I16 | NGC K32 cold build | 2,702.9 s (eval radii [], iteration-0 roster, at most 3 processes, nice 10) | TESTED | MODULE_ACCEPT_K32 `build_seconds` | 18e4b814… (as I3) |
| I17 | Contention spread | 1.7172 (the same K64 quadrature took 12,984.5 s once and 7,561.5 s once) | TESTED | u2 R4/R5 (MODULE_ACCEPT_K64 d5c0ece5, log 20818eb8; prefixes as in u2) | map 3b4c7db66195d714b5b1d1fdc9f762da9b14754672370c6e42be38c2a16cbebb |
| I18 | Warm-build calibration | E: 4.797e-11 s per MAC, 25.68 ns per (kp, kz) element, 0.09 µs per Bessel call. U: 7.722e-11 s per MAC, lumped | FORMAL fit to TESTED DDO rows (§3) | TIMING_V003.md §1; KBIG §6 | as I13 |
| I19 | vf time rate | 8.1-8.8 ns per (kz, element) pair, giving 26.23 s (E) or 27.32 s (U) per state index m | TESTED-derived | u4 §9.3; KBIG §6 | as I13 |
| I20 | vf bytes per pair | E 32 (code); U 51 (implied by DDO measured peaks) | E FORMAL; U TESTED-derived | roster L217; §6.3 | roster 4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2 |
| I21 | Caches C_max | 365,924,352 B | FORMAL | u4 §3 | |
| I22 | Stars cold-build transient | E 1.341 GB (DDO K128 n=0 peak 1.53 GiB, less the 0.29 GB test base and P); U 2.7 GB | E TESTED-derived. U ASSUMED: the NGC stars node count needs the fenced profile | KBIG §6; u4 §5.2 (before-build 289,636,352 B) | |
| I23 | Parallel worker model | it 0: b + 3S + max(A_max, P). it ≥ 1: b + 4S + C + P + A_max. Steady: b + S + P + C. b ≤ 0.27 GB. Unexplained residual 1.4-1.8 GiB per worker | FORMAL code; TESTED bound and residual | solver 7667025b L735-819 (u4 §6.3); u4 §7.1, §7.6 | 7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db |
| I24 | Parallel time model | T(N) = prep + cols/(0.9·C) + upd/(0.95·C) + overhead, with C(N) = min(N,6) + r·min(max(N-6,0),12). r = 0.52 was measured with a background QoS clamp | FORMAL | projection_c2v001.py L1-16 | as I14 |
| I25 | Route-B structure | 6 + 2P tail builds, 4 + 2P on the critical path. Each stage is its own process and builds cold. DDO tail-off receipts: reference 2,786 s + body 600 s + offset..le3 10,702 s = 14,088 s (P = 3), plus 2,117 s per extra pass | FORMAL | TIMING_V003.md §2-§4; dry plan 6eaf864c (critic V11); roster L121-127 (cache per object) | as I13 |

## 2. E8: q, the HI vertical nodes per column (resolved)

- The HI column solver places `panels_per_side` nodes on the lower side and `panels_per_side + 1` on the upper side (`zs`, L92-93). That is 2p + 1 nodes, and one node record per z (L94-105).
  - Source: `hi_two_sided_free_boundary_v002.py` `665b55897248eb571914faa9936b975a2f6343f79d1491e2407e75ce4da6bc33`.
- The column quadrature returns one element per node (`zip(nodes, w, J, f)`, L69-71).
  - Source: `general_column_mass_quadrature_v002.py` `a67b526b378390fa91ccd030efb9ff1c868d379986ff3321335780c485ef0d04`.
- The solver appends one source element per (node, element) pair (solver L208).
- NGC passes `panels_per_side=hi_panels_per_side` (prep 8681da84 L120-125). The value is **8** in the T120L replay record's numerical inputs (TESTED, u4 §1.8).
- **So q = 17 (FORMAL rule x TESTED input).**
- DDO cross-check: 58,752 elements / (6 x 576 columns) = 17 (TESTED, u4 §5.1), which is what panels 8 gives.
- **Residual assumption.** The step-5 value comes from the NGC seed, which is fenced. The template sets no HI-panel field (TESTED: jq on TEMPLATE_A_K32_A2_HEADLINE `f130e6dfff74d3a0ff568a33f4128fa6f7d485785daa5ac302dc4c3512aea2e8`). That the step-5 call keeps 8 is therefore ASSUMED.

Consequences:
- 84,864 elements per iteration (4,992 x 17).
- The roster column at state m holds n_z_col = 1 + 32·17·m elements (roster `roster_route_a` L355-381: init ring plus every earlier iteration, azimuths collapsed).
- vf(m) = 32 x 36,576 x (1 + 544m) B, which is **636,715,008 B per m** (u4's figure, now with q confirmed).

## 3. E7: K32 tail build times at production nR

What a build does (lib `build` L645-796; roster L100-219):
1. P: the stars radial transform (cold only), plus the gas radial factors for every build. The gas radial factors are 39 annuli x 51,904 x 96 Bessel arguments, with no cache (roster L188-206).
2. F: the vertical factors, including the vf transient (L209-219).
3. The kp block loop, in blocks of 57 rows (L614-616): the Sr/Si matmuls (2·N_perp·N_z·r MAC), elementwise shell work (N_perp·N_z elements), and the ring-table update (6·nR·N_perp·N_z MAC, plus 3·nR·N_perp Bessel calls; L745-756).
4. The digest at construction: one `tobytes` copy per array (L350-358).

Calibration on TESTED DDO builds:
- **E (split fit).**
  - y = 11 s / (36 extra radii x 6 x 20,736 x 51,200 MAC) = **4.797e-11 s/MAC**. Source: TIMING_V003 §1, K128 solo warm builds: le_rotation 72 radii 61 s, columns 36 radii 50 s.
  - The remainder of the 36-radius warm build gives **25.68 ns per (kp, kz) element**, with Bessel calls at 0.09 µs (ASSUMED).
  - Check: the same model gives 76.6 s for KBIG's K128 n=0 warm build, against 76.9 s measured (TESTED KBIG §6).
- **U (lumped fit).** 76.9 s / (2·73 + 6·132)·20,736·51,200 = **7.722e-11 s/MAC**, with everything lumped onto the MACs.

NGC (FORMAL arithmetic, nR 371):

| term | E | U |
|---|---|---|
| Fixed warm part W0 (Sr/Si 28.6 s + elementwise 48.8 s + gas radial 17.5 s) | 94.8 s | 46.0 s, inside the lumped total |
| Ring tables per radius | 0.5604 s | 0.8796 s |
| Warm build, state m (nR 371) | 302.8 + 26.73·m s | 372.4 + 28.02·m s |
| Cold build at iteration 0 (state 0) | 2,702.9 + 207.9 = **2,910.8 s** | 2,702.9 x 1.7172 + 326.3 = **4,967.7 s** |
| Route-B cold build (nR_B = 156, ASSUMED) | 2,790 s | 4,779 s |

Notes:
- **vf time.** The vf term is 26.23 s (E) or 27.32 s (U) per m (I19). The roster rebuild, a Python loop over every element (roster L366-377), adds 0.5-0.7 s per m (FORMAL estimate).
- **What dominates the cold build.** It is the stars transform (FORMAL inference):
  - the measured cold build at nR 0 is 2,702.9 s, while W0 is about 95 s;
  - DDO shows the same pattern (KBIG §6: the stars transform is "about 97%" of a cold build in its proxy, and grows about 3.7x per K_big doubling).
- **Where the transform cache lives.** It is a per-process, per-object dict (roster L121-127). Route A pays it once in stage 01 and once in stage 02, and each route-B stage process pays it again (§8).
- **Basis of E.** E keeps the measured contended value (2,702.9 s), so it is conservative for a solo build. A warm NGC build has never been measured (u4 §9.1).

## 4. E9: the tail-ON cost per column at NGC K32

- **Per metric call.** The tail boundary is `TailBoundary.__call__` → `jet(pos, order 1)` (lib L816-821). At a cached line (`cyl_jets` with `_cache`, L480-516), each call costs:
  - one complex `exp` over N_z;
  - one complex scale;
  - eight real dot products over N_z.

  By operation count this is 1.5-2.0x a `lapse_pair` (one `expm1` and two dots, L557-580) (FORMAL).
  - E: 1.5 x 11.33 ns x 36,576 = **0.622 ms**.
  - U: 2.0 x 38.09 ns x 36,576 = **2.786 ms**. This uses the K256 under-load rate.
- **Per column.** One line build plus a corner share. Corners are built once per radius per iteration, because the columns are radius-major (I7) and `CORNER_LRU` is 16 (lib L38, L414-441). At NGC a corner build is about 0.06-0.22 s for jm 10-107 (FORMAL). That adds 0.010 s (E) or 0.030 s (U) per column.
- **c_tail** = 91.53 calls x the per-call cost + the line share = **0.0669 s (E)** or **0.2850 s (U)** per column.
- **Tail-off column at T120L (c_off).**
  - U = 0.4007 x 2.25 = **0.9017 s**. This is the old linear-in-waves factor (FORMAL).
  - E = **0.6512 s** (ASSUMED split). `prepare_line` is linear in the waves (80 kz groups x 10 einsums over the transverse nodes, line module `5c0ab4f6dcd14b79d5ec012f3eee6f58704b8e2982657ac58862b94b9429dfb4` L11-44). By operation count it is about 50 % of the G80C column. The 91.5 per-call evaluations are not linear in the waves.
- **Tail-ON column.** E **0.718 s**, U **1.187 s**.
- **Cross-checks.**
  - KHI tail-ON measured **0.8-0.95 s per column per worker** at K256 with 8 workers (u4 §9.4). That lies inside [E, U].
  - The tail increment is small at NGC K32 (N_z 36,576), against 102,400 at KHI. The column cost is dominated by the tail-off Fourier line and the HI search.

## 5. The other per-iteration terms

### 5.1 `prepare`: a per-node solve every iteration
- The NGC binding installs the streaming facade (`make_fourier_module`, binding L118-120). Binding: `ngc_composite_full_coupled_binding_uvtail_ro1_cx3v011.py` `9b5ce82adea46c8e660f44b0fc91e8dbe5d0616cc1de1fd4467878ef3b5c0668`.
- The facade's `prepare` (L44-60) calls base `prepare` with a per-node JSONL callback. Facade: `owned_streamed_fourier_per_run_adapter_v001.py` `cbbc4b968fc189440ddd4f516fb53f07d04a97b638fdf90fd90f50422afb928e`.
- Base `prepare` loops in Python over all nodes (L96-126). For each node it runs `bind_symbol` and `solve_symbol` and emits one node record. Base: `owned_physical_fourier_metric_quadrature_v005.py` `7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491`.
- The record scope says "rebuild when either changes", and the source changes every iteration (FORMAL).
- **E = 574.82 s.** This is the T120L iteration-0 replay wall, with status `TESTED_PASS_ALL_1152000_NODES_BITWISE` (u4 §7.4). It is an upper reading for E, because it may include about 137 s of input preparation. The saved operator's response took 329.96 s of CPU (OPERATOR.json).
- **U = 941.55 s.** This is the old plan's per-iteration basis.
- **Why DDO is faster.** DDO's binding is the "stable cached" one, and its prepare takes **7 s** (projection basis). That figure does not transfer.

### 5.2 Source update: missing from the old plan
- `updated = physical_source_fourier(positions, columns, waves)` runs every iteration (solver L215). Module 81af8715 (I15) does a dense double loop over 64-wave by 256-element blocks.
- NGC per iteration: 84,864 x 1,152,000 = 9.776e10 pairs. At the DDO-measured rate that is **2,768.5 s (E)** or **2,990.5 s (U)**.
- DDO F10 measured 103-104 s per iteration in its saved progress (projection basis, FORMAL). The rate transfer is FORMAL; that DDO used the same module is ASSUMED (the parallel solver admits only this sha as row-separable).
- The projection's own NGC estimate (1,225 s at 80³ waves) scales to 2,756 s at T120L, which agrees.

### 5.3 Per-iteration overheads

E 80 s, U 200 s (ASSUMED), covering:
- I1-T at 4,096 waves per iteration (controller `_i1t` L372-393);
- the M_T/M_K monitors (`_rows_T` L429-438, which builds corners at the probe radii for both states; `_rows_K` L440-458, an exp over all waves per probe);
- the progress and checkpoint array writes with sha read-back (worker ARRAY_KEYS L36);
- the sidecar `savez` + `fsync` (controller L519).

Controller: `route_a_uv_tail_controller_c2v001_r5.py` `c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc`.

## 6. (A) Headline: serial route A as the template runs it

### 6.1 Wall per iteration

The state m = n + 1 is built at the end of iteration n.

T_iter(n) = prepare + 4,992 x (c_off + c_tail) + update + overheads + warm(m)

- **E** = 574.82 + 3,584.8 + 2,768.5 + 80 + (302.8 + 26.73m) = **7,310.8 + 26.73m s**. That is 7,338 s at n = 0 and 7,498 s at n = 6.
- **U** = 941.55 + 5,924.0 + 2,990.5 + 200 + (372.4 + 28.02m) = **10,428.5 + 28.02m s**. That is 10,456 s at n = 0 and 10,877 s at n = 15.

Share of one E iteration: columns 49 %, source update 38 %, prepare 8 %, tail build 4-7 %.

### 6.2 Totals
- **Stage 01 (route A).**
  - E: start-up 137.54 + cold 2,910.8 + sum over n = 0..6 of T_iter = **54,973 s (15.27 h)**.
  - U: start-up 275.08 + cold 4,967.7 + sum over n = 0..15 of T_iter = **175,907 s (48.86 h)**.
  - Both include the build at the converged or last iteration (u4 §5.1).
- **Stage 02 (manifest).** One cold rebuild of the accepted state in a new process: **3,235 s (E, m = 7)** and **5,691 s (U, m = 16)**.
- **Route-A tree:** **58,208 s = 16.17 h (E)** and **181,598 s = 50.44 h (U)**.
- **Mixed brackets.**
  - E unit costs with I = 16: 35.31 h.
  - U unit costs with I = 7: 23.46 h.
  - With nR 156: E 15.87 h, U 49.50 h.

### 6.3 Memory: peak and steady

Every phase includes the driver: 0.1 GB (E) or 0.3 GB (U), ASSUMED. The dry-process RSS observed was ≤ 89,751,552 B (u1 §8).

| phase (serial, nR 371) | E | U | terms |
|---|---|---|---|
| Iteration-0 cold build (stars transform, then the ring loop) | 2.91 GB | 4.57 GB | B0 1.172 GB (PREP peak) + max(stars 1.34/2.7 GB, ring phase) |
| `prepare` (old prepared still alive) | 3.33 GB | | B + S + C + 0.212 GB |
| Columns (steady) | **3.12 GB** | **3.72 GB** | B + S + C (U: B + 0.4 GB for updated, g_next and lists) |
| Source update | 3.45 GB | | steady + 0.33 GB of Python lists and the result |
| Build, ring phase | 4.76 GB | | B + S_now + C + P + F + Fr/Fi + ring zeros + corner + block temporaries (57 x N_z x 14 arrays) + ring temporaries 32 B·nR·N_z |
| Build, digest phase | 4.65 GB | | B + 2S + C + A_max (`tobytes` copy, lib L353-358) |
| Build, vf phase, state m | 3.276 + 0.6367m GB | 3.876 + 1.0148m GB | B + S_now + C + P + F + vf(m) |
| **Run peak** | **7.73 GB** (m = 7) | **14.06 GB** (code, m = 16); **20.11 GB** (excess, m = 16) | |

**The DDO check behind U.** The code-term model under-predicts the measured DDO route-A peaks (awk, this session):

| case | model | measured | excess | implied vf bytes per pair |
|---|---|---|---|---|
| K128 n=6 (KBIG §6) | 2.111 GB | 2.899 GB | +37.3 % | 50.84 |
| K256 n=6 (TIMING_V003 row, cold + warm + eval) | 3.919 GB | 5.057 GB | +29.1 % | 45.61 |

- U uses 51 B per pair. That attributes the excess to vf and is the conservative reading.
- If the excess is instead a constant 1.14 GB, the U peak is 15.20 GB.
- The attribution is UNTESTED, like KHI's per-worker residual.

### 6.4 Per-iteration profile: what root's watch should see

Each row assumes the run reaches that iteration. Cumulative times include start-up and the cold build. The spike is the build of state m at the end of iteration n.

| n | m | iteration E / U (s) | cumulative E / U (h) | spike E / U (GB) | vf plateau E (s) |
|---|---|---|---|---|---|
| 0 | 1 | 7,338 / 10,456 | 2.88 / 4.36 | 4.76 / 5.47 | 26 |
| 1 | 2 | 7,364 / 10,484 | 4.93 / 7.27 | 4.76 / 5.91 | 53 |
| 2 | 3 | 7,391 / 10,512 | 6.98 / 10.19 | 5.19 / 6.92 | 79 |
| 3 | 4 | 7,418 / 10,540 | 9.04 / 13.12 | 5.82 / 7.94 | 105 |
| 4 | 5 | 7,445 / 10,568 | 11.11 / 16.06 | 6.46 / 8.95 | 131 |
| 5 | 6 | 7,471 / 10,596 | 13.19 / 19.00 | 7.10 / 9.97 | 157 |
| 6 | 7 | 7,498 / 10,624 | 15.27 / 21.95 | **7.73** / 10.98 | 184 |
| 7 | 8 | 7,525 / 10,652 | 17.36 / 24.91 | 8.37 / 11.99 | 210 |
| 8 | 9 | 7,551 / 10,681 | 19.46 / 27.88 | 9.01 / 13.01 | 236 |
| 9 | 10 | 7,578 / 10,709 | 21.56 / 30.85 | 9.64 / 14.02 | 262 |
| 10 | 11 | 7,605 / 10,737 | 23.68 / 33.83 | 10.28 / 15.04 | 289 |
| 11 | 12 | 7,632 / 10,765 | 25.80 / 36.82 | 10.92 / 16.05 | 315 |
| 12 | 13 | 7,658 / 10,793 | 27.92 / 39.82 | 11.55 / 17.07 | 341 |
| 13 | 14 | 7,685 / 10,821 | 30.06 / 42.83 | 12.19 / 18.08 | 367 |
| 14 | 15 | 7,712 / 10,849 | 32.20 / 45.84 | 12.83 / 19.10 | 393 |
| 15 | 16 | 7,739 / 10,877 | 34.35 / 48.86 | 13.46 / **20.11** | 420 |

How to read the timeline:
- **Start.** The first 0.85 h (E) or 1.46 h (U) is start-up and the cold build, with its stars-transform plateau at 2.9 GB (E) or 4.6 GB (U).
- **Inside each iteration:** prepare, then the columns at the steady 3.1-3.7 GB, then the source update.
- **The spike.** It comes about **1.9 h (E) or 2.7 h (U) after the iteration starts**, once per iteration, and closes the iteration. It is a plateau of vf(m) lasting about 26·m s (E), followed by the ring and digest phases (about 4.7-4.8 GB E) for about 5 min, after which the footprint falls back to steady.
- **The spike grows with n:** +0.64 GB per iteration from code terms, or +1.01 GB with the DDO excess. For m ≤ 2 the ring and digest phases are the build's maximum.
- **Sampling.** A 30-s footprint sampler catches the vf plateau from m = 2 onward.

## 7. (B) Parallel-8 row: only meaningful with a successor template

This uses the A130 model on solver 7667025b (I23, I24).
- Workers are spawned, and each holds a private TailState with its own caches.
- At every iteration the parent pickles the state (inner plus outer) and `prepared`, and sends them to each worker in turn.
- The source update is split by wave blocks, because 81af8715 is admitted as row-separable (parallel solver L401-404).
- The per-node `prepare`, the tail builds and the transfer stay serial in the parent.

**Wall.** C(8) = 7.04 at r = 0.52.
- Per iteration (E) = 574.82 + warm(m) + 60 (transfer; KHI's footprint fell from 40.70 to 14.94 GiB-units in about 51 s, u4 §7.1) + 3,584.8/(0.9 x 7.04) + 2,768.5/(0.95 x 7.04) + 6 + 80 = **2,030 s at n = 0**. U: 3,470 s at n = 15.
- Route-A tree:
  - E: **5.85 h** (21,056 s; 5.76 h at r = 0.70).
  - U: **17.53 h** (63,097 s).
- **Gain:** **10.32 h (E, 2.77x)** and **32.92 h (U, 2.88x)** per point on route A.
- The parent's serial floor (prepare + build + transfer + overheads), about 1,050-1,210 s per iteration at E and 1,670-2,090 s at U, caps the speedup near 3x.
- Whole point: E 18.70 h, U 46.96 h.

**Memory (FORMAL code model plus the TESTED KHI residual):**

| | E | U |
|---|---|---|
| Worker at it 0 / it ≥ 1 / steady (b = 0.27 GB) | 3.57 / 5.04 / 1.73 GB | +1.8 GiB residual at transfer |
| Parent at transfer (B + 3S + 2·prepared) | 4.84 GB | 5.24 GB |
| **Tree at the it ≥ 1 transfer** (all 8 workers hold the new state before `prepared` follows) | **45.2 GB** | **61.3 GB** |
| Tree at the it 0 transfer | 33.5 GB | 49.6 GB |
| Tree steady | 17.0 GB | 17.6 GB |
| Parent's m = 16 vf build while the workers are steady | | 34.0 GB |
| nR 156 instead of 371 (it ≥ 1 transfer) | 29.0 GB | 45.1 GB |
| N = 4 (it ≥ 1 transfer) | 25.1 GB | 33.4 GB; route A E 7.30 h, U 22.20 h |

- The KHI check passes: this model gives 3.07 GB per KHI worker at it 0 (u4: 3.1). The measured 4.5 GiB per worker is the source of the residual.
- **The A61 minimum cap for N8 is 1.5 x 61.3 = 91.9 GB.** That is effectively the whole machine under root's 95 GB watch threshold. N = 4 keeps most of the gain at about 55 % of the memory.

**Identity test.** A132 and the I4 precedent ask for a TESTED serial = parallel bitwise identity on the NGC operator with the tail on (V005F L27, L153: DDO's CHECK_V001 found tail-ON serial == parallel bitwise). It should cover iteration 0 (the cold state) and iteration 1 (the first warm-state transfer).
- **Option 1, recommended: piggyback on the first point.**
  - Start the serial headline together with a parallel-8 replica of the same call, which differs only in `route_a.column_workers` 8. Stop the replica after iteration 1.
  - Compare bitwise: the per-column checkpoint records, the updated gas arrays of iterations 0-1, and the sidecar state digests.
  - The replica costs **1.98 h (E) or 3.16 h (U)** of 9-process wall, plus its 45-61 GB transfer spikes.
  - The verdict is ready when the serial run finishes iteration 1: **4.93 h (E) or 7.27 h (U)** after launch.
  - The serial run is the headline, so a failed identity wastes nothing but the replica.
- **Option 2: a standalone test before the first point.** The same two runs, 4.9-7.3 h of wall, and the serial half is thrown away.
- **Either option** also needs a reviewed template successor with a `route_a` block (the driver accepts 1..8, L5058-5061) and root's ruling.

## 8. (C) Route B: an explicit UNKNOWN bracket

**Stages** (dry plan 6eaf864c, critic V11): 03 reference, 04 body, 05 offset, 06-07 fs_columns_00/01, 08 fs_rotation, 09 fs_feedback, 10 rfs_columns, 11 le1_columns, then the further LE passes. Picard passes: 4 is the template maximum; the passes stop early at the 0.01 km/s bound.

| part | E | U | label |
|---|---|---|---|
| Critical-path cold tail builds (4 + 2P) | 10 x 2,790 = 27,903 s | 12 x 4,779 = 57,343 s | FORMAL count (TIMING_V003 §2, same r5 stage structure) x TESTED NGC cold unit; nR_B 156 ASSUMED |
| Tail-OFF stage work | 14,088 x 1.302 = 18,344 s | 16,205 x 3.0 = 48,615 s | UNKNOWN for NGC. Scaled from the DDO receipts by the wave ratio (E) and by the wave ratio x a node ratio of up to 156/72 (U). ASSUMED |
| Route-B tail evaluations (jet order 2) | not included | not included | UNKNOWN. DDO K256 unit costs are 85 ms per point (rotation) and 25 ms per point (columns); the NGC counts are unmeasured |
| **Route B** | **12.85 h** | **29.43 h** + the unknown evaluations | |
| Concurrent stage pair (route-B column_workers 2), memory | 3.78 GB | 10.03 GB | B_stage 0.5 GB (E) or 2.17 GB (U), ASSUMED, + the cold-build stars transient |

**What is unknown:**
- the NGC route-B radial-node counts and rosters, which set nR_B and any route-B vf;
- the NGC tail-off stage costs (no NGC route B has ever completed; PLAN `full_route_B_wall_time` UNTESTED);
- the evaluation counts;
- P ≤ 4;
- the B_stage baselines.

**Every route-B stage process pays a fresh stars transform**, about 2,700 s each. A cross-process cache would remove most of the tail-build part (TIMING_V003 §4 measured the DDO analog; UNTESTED here).

## 9. (D) Recommended caps for the first NGC point under A61

- **RSS.** Physical footprint of the call's process tree: the driver plus the active stage process or processes.
  - The modelled peak is 20.11 GB (U with the excess), so the A61 minimum is 1.5 x 20.11 = **30.17 GB**.
  - **Recommend 32 GiB (34,359,738,368 B).** That is 1.71x the U peak with the excess, 2.44x the code-term U peak and 4.44x E.
  - Route B's concurrent pairs (≤ 10 GB) and stage 02 stay below it.
  - If the enforcing monitor sums ps RSS (A130), the shared-page difference for a 2-3 process serial tree is small.
- **Wall.**
  - The point is E 29.02 h and U 79.88 h, and route B is an UNKNOWN bracket. **Recommend 360,000 s (100 h), about 1.25 x U** (359,445 s).
  - A cap derived from E alone (the "about 2x" plan rule, about 58 h) would cut the U path.
  - **Re-forecast after iteration 1.** Take the measured iteration period x the remaining iterations, plus the measured route-B stage walls.
  - Under the principal's direction, extend deliberately rather than letting a fixed cap stop a run near completion. Route A is checkpointed and resumable.
- **Unchanged:** max route-A iterations 16; Picard passes 4; no automatic retry.
- **For the N8 successor only:** RSS ≥ 91.9 GB (U), which means near-exclusive use of the machine; wall 211,319 s (about 59 h).
- **The old plan caps are contradicted.**
  - 5 GiB serial: crossed at the build of state 4 (5.82 GB E).
  - 43,200 s: crossed during iteration 5 (E). Route A alone is 16.2-50.4 h.

## 10. Scheduling note (for root's step-5 schedule; operational, A115 NOTE class)

- **A serial point** is a 1-core process. Its spikes are E 7.7 GB or U 20.1 GB, each lasting minutes once every 2-3 h. Route B has 2 processes at times.
- **Running serial points side by side.** Four at once reach about 80 GB only if all their U spikes coincide, which is unlikely because each spike lasts at most 7 min. That gives about **7.3 h per point at E** (29.0/4) before any co-load slowdown.
- **N8.** One N8 point at a time (45-61 GB) gives **18.7 h per point**.
- **So:** for a multi-point campaign, concurrent serial points give more throughput than N8, without the identity test. N8 shortens one point's latency by about 10 h at E.
- **Open inputs.** The number of step-5 points is NOT DETERMINED (u1 §2). The co-load slowdown is UNTESTED; TIMING_V003 measured wall ratios of 1.7-3.0x at load average 20-60.

## 11. What would move these numbers most

1. **The tail-off column cost at T120L:** 0.65 s (E) against 0.90 s (U), worth ±1,250 s per iteration. The first point's iteration 0 measures it (`column_completed` events).
2. **The source update:** 2,770 s per iteration, from the DDO rate. Measured from iteration_prepared → iteration_completed on the first point.
3. **The iteration count:** I = 16 at E unit costs gives route A 35.31 h and the point 48.16 h.
4. **nR** (BLOCKED_BY_FENCE): small effect. At nR 156: E 15.87 h and peak 7.36 GB.
5. **vf bytes per pair** (32 against 51): the U peak is 14.06 GB or 20.11 GB.
6. **Route B:** the largest UNKNOWN after route A.
7. **Contention:** every unit cost comes from a shared machine.

**Disk** (NOTE, UNTESTED):
- Per iteration the worker writes 580.6 MB of progress arrays: current, wavevectors, weighted responses and the reconstructed gas (worker ARRAY_KEYS L36; solver L141, L231).
- On top of that come 1,152,000 node records (streaming adapter L44-57; size per record unmeasured) and the checkpoint records (module not read).
- So at least 4.1 GB at I = 7 and 9.3 GB at I = 16 before node logs. The old 32 GiB output cap may bind at U if a node record is about 1 KB.

## 12. Findings for root (A115: all are operational NOTE class; none changes a physics reading)

- **F1.** q = 17 at NGC, from code (TESTED input 8). The vf transient is confirmed at 0.637 GB per iteration from code terms.
- **F2.** Serial route A has an unmodelled **source update of about 2,770 s per iteration**, and a **per-node prepare of about 575 s**. The old plan's 25.07 h for 16 iterations omits the first and uses a different prepare basis. The E iteration is 2.04 h.
- **F3.** The serial peak is **7.73 GB (E) or 14.1-20.1 GB (U)** at the last tail build; the steady footprint is 3.1-3.7 GB.
- **F4.** The old caps (5 GiB, 43,200 s) would stop the headline at E. Recommended: 32 GiB and 360,000 s, with a re-forecast after iteration 1.
- **F5.** Parallel-8 cuts route A by **10.3 h (E) or 32.9 h (U)** per point, but its transfer spike is **45-61 GB**: the A61 cap is about 92 GB. The identity can piggyback on the first point at a marginal cost of **about 2-3.2 h** of the replica.
- **F6.** Route B is 12.9-29.4 h as an UNKNOWN bracket. It is dominated by 10-12 cold tail builds of about 2,800 s each, because the stars transform is per process. A cross-process cache is the lever (UNTESTED).
- **F7.** For throughput across many points, concurrent serial points beat N8 (§10).

## 13. Conduct, rule notes and files

**Python.** None was run.
- The mandated runner `tools/run_fenced_c4st2.py` (`fe904509c7d2d6300042589aaa02d839e82b436680d293b65c5c7d4cf69f6d25`; fence `c993d34c185d785d77c443a00033e8efeea10cd02f1a547a99af458c0f698eb5`) opens 64 B of the open-name V005 and V004 addenda and of a `uvt_*.py` before any script runs (critic V5).
- This task's rule allows only the V006 and V005_FROZEN addenda. All arithmetic was therefore done in awk, jq and shell.

**Read as text:**
- the maps;
- 0677, 0685 and post 0172 (`feb8e2d5c03fb8429b62af4bae3654c9169ef4517d92f2545ef084149a7e9a84`);
- the V006 addendum, now `d4084175b98e55104d0f891a5aaee32b59bc7661eda9ccd1d8ed40ce1dc87e12` (461 lines; A131-A132 appended; A132 records the cw8 lever);
- V005_FROZEN `c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1` (L27, L145-160, L1185-1215);
- TIMING_V003.md;
- KBIG_PROXY_V002.md;
- the PLAN;
- projection_c2v001 (json, py);
- the `.py` sources named above. No `uvt_*.py` was read, and none of them was imported.

**A possible rule incident, self-reported.**
- What ran: `ls` of the single folder `ngc_route_tail_readiness_cx3/`, and a glob listing of `parallel_route_a_c2/*/`, each piped through `grep -v -i ngc3198`.
- What was exposed: those listings enumerate directory entries. Any NGC3198-named entry was filtered out before display, and none was opened or statted.
- Since then, no folder that may hold NGC3198-named entries has been listed.

**Writes, all inside this folder by exclusive create:** `PARTIAL.md` (append-only), `calc/estimate_c4v001.awk`, `calc/NUMBERS_C4V001.json`, `calc/META_C4V001.json`, this file and its JSON twin `ESTIMATE_RI45_12_NGC_K32_C4V001.json`.
