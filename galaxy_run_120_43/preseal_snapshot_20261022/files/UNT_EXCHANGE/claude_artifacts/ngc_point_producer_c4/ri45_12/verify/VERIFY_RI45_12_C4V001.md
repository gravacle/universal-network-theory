# VERIFY RI45-12(i): adversarial check of the NGC K_big 32 / T120L point estimate (Claude4, C4V001)

From the Claude4 adversarial-verifier helper (workflow `ri45_12/verify`), for root dispatch 0677 item 2. Drafted 2026-10-19T10:24:57Z (`date -u`).

**Object under test** (hashes re-computed from bytes this session; all equal the estimator's reported values):
- `estimate/ESTIMATE_RI45_12_NGC_K32_C4V001.md` `0546b3ea5563b1d70faa47f84de853ea39463eac7c3ec3381148a4b91b16c733`
- `estimate/ESTIMATE_RI45_12_NGC_K32_C4V001.json` `a3498b307741ed7c785451bdb7fb027b070a28a4b04ed1edec9d923b004483e1`
- `estimate/calc/estimate_c4v001.awk` `1f0a3656e8049b8e688bb6c126bb82491eeb59edb224163094dbc9bcea272dcc`
- `estimate/calc/NUMBERS_C4V001.json` `76e5782670ef31f38d32b2ced143a9f3862828b3df4aae1eaa78d0a89fdd2866`

**My arithmetic** is an independent awk script, `calc/verify_c4v001.awk` (`ccb7f162cf8d4fc57a0ce96ae77f3e19aca98b22e7b1e5beb9a8628c51a1ccca`). It re-derives every number below from the byte-level inputs; it does not reuse the estimator's script. No Python was run and nothing was launched (§7).

E/U = expected/upper. GB = 1e9 B, GiB = 2^30 B. Labels as in the estimate: TESTED, FORMAL, ASSUMED, UNKNOWN, plus INFERENCE for a reading I did not trace to the last line of code.

## 0. Verdict: CONFIRMED_WITH_CORRECTIONS

- **The memory model and the RSS cap stand.** I reproduced q = 17, the TailState formula, the vf growth of 636,715,008 B per state index, the per-phase peaks (7.73 / 14.06 / 20.11 GB) and the steady footprint. The serial template spawns nothing, so the A130 spike belongs only to the parallel row. The 32 GiB cap meets A61 under every reading I can build from bytes, **provided** the step-5 seed keeps hi_panels_per_side 8 and source_azimuth_count 32 (N4).
- **The wall is under-stated by one whole term (C1).** Stage 01 runs the 43-query readout in the same process after route A converges: 12,900 HI column solves plus 2,580 line preparations. That adds **+2.90 h (E) / +4.90 h (U)**. Corrected route-A tree: **19.06 h (E) / 55.33 h (U)**. Corrected point: **31.90 h (E) / 84.77 h (U)**.
- **The parallel-8 gain in hours is unchanged, but the speedup ratio falls** from 2.77-2.88x to **2.18-2.47x**, because the readout is serial in the N8 parent too (C2).
- **The 360,000 s wall cap no longer has the stated 1.25x headroom.** It is 1.18x the corrected U. It does not false-stop the corrected U path, but the estimate's own rule gives **381,452 s (106 h)** (C3).
- Everything else I checked held, apart from small items (C4, N1-N11).

## 1. Corrections table

| id | item | estimate says | corrected | basis (file:line, sha) | effect on caps |
|---|---|---|---|---|---|
| C1 | **Stage-01 post-convergence readout (missing term)** | not modelled; stage 01 = start-up + cold build + Σ T_iter | **+10,427 s E (2.90 h); +17,635 s U (4.90 h)**. 43 queries x 12 observation azimuths x 25 distinct midplane HI column solves = **12,900** solves at the estimate's own column cost (0.7181 / 1.1867 s), plus **2,580** extra `prepare_line` calls (one per `local()` call, for `metric(R,phi,0.)` after the line key moved) at 0.4508 s E / 0.9017 s U | worker `ee27227c` L145 → binding `9b5ce82a` L189-194 (12 azimuths from `observation_azimuth_count`, 43 queries required) → prediction `7ae28901` L55-58 (solve, then readout only if converged), L85-102 (`midplane` cache keyed by exact (R,phi); one `solve_hi_column` per key), L107, L122-141 (`local`: 5 radii R, R±step, R±step/2, then L131 `metric(R,phi,0.)`), L142, L159 (4 more `local` calls at phi±astep, phi±astep/2). No outer gas cut: `apply_cut` `5d037291` L80-81 returns None, so all 43 queries run. FORMAL count; unit cost ASSUMED equal to a route-A column; 12 azimuths TESTED for the T120L replay (u4 §1.8), ASSUMED for the fenced seed | wall only |
| C1a | Route-A tree (stage 01 + readout + stage 02) | 16.17 h E / 50.44 h U | **19.06 h E (68,608 s) / 55.33 h U (199,204 s)** | C1 + C4 | wall |
| C1b | Whole serial interface-A point | 29.02 h E / 79.88 h U | **31.90 h E (114,855 s) / 84.77 h U (305,162 s)**, route B unchanged (12.85 / 29.43 h UNKNOWN bracket) | C1a + estimate route B | wall |
| C2 | Parallel-8 row (successor only) | tree 5.85 / 17.53 h; gain 10.32 / 32.92 h (2.77x / 2.88x); point 18.70 / 46.96 h; N8 wall cap 211,319 s | tree **8.74 h E / 22.42 h U**; gain unchanged **10.32 / 32.92 h** but speedup **2.18x / 2.47x**; point **21.58 / 51.85 h**; 1.25 x U = **233,326 s** | the parallel worker `293a417f` L28, L32, L149-152 pins the same binding and prediction module; only the solver is bound to column_workers, so the readout stays serial in the parent | N8 wall only |
| C3 | Serial wall cap | 360,000 s "about 1.25 x U" | 360,000 s = **1.18 x** corrected U. Not a false stop (U 305,162 s), but under the estimate's own 1.25x rule the cap is **381,452 s (106.0 h)**. The iteration-1 re-forecast must add the readout: 12,900 x (measured column cost) + 2,580 x (line cost) | C1b | wall |
| C4 | Stage 02 rebuilds which state | the state built at the last iteration, m = I (7 E, 16 U) | the **accepted** state = state of the converged iteration n_c = **I - 1** (6 E, 15 U). Stage 02 E 3,235 → **3,209 s**; U 5,691 → **5,663 s**; its vf at m 6 / 15 | manifest writer `b9247b1a` L151-159 (`rebuild_state` → `_build(n, _i1t(n, gas))` with `elements[:n]`), L219 (n is the accepted, converged iteration), L232 | none (stage-02 U peak about 18.1 GB < 32 GiB) |
| C5 | Scheduling note (§10, F7) | 7.3 h per point for 4 concurrent serial points vs 18.7 h per N8 point | **8.0 h** vs **21.6 h** per point (E). The conclusion (concurrent serial beats N8 for throughput) is unchanged | C1b, C2 | none |

## 2. Independent re-derivation (all reproduced unless marked)

| quantity | estimate | verifier (awk) | status |
|---|---|---|---|
| q, HI nodes per column | 17 | 17: `zs` = p lower + (p+1) upper nodes (HI `665b5589` L92-93), one element per node (quadrature `a67b526b` L69-71), panels from prep `8681da84` L125 | CONFIRMED |
| elements per iteration | 84,864 | 4,992 x 17 = 84,864 | CONFIRMED |
| n_z_col(m) | 1 + 544m | `roster_route_a` (`4366e3d6` L355-381) and `gas_columns_from_rings` (L281-292) keep every element, zero-mass endpoints included; no filter or merge | CONFIRMED |
| TailState S | 232,598,248 + 1,755,656·nR; 883,946,624 B at 371 | same; 1,755,656 = 48·N_z + 8 | CONFIRMED |
| vf per m (32 B/pair) | 636,715,008 B | 636,715,008; vf(16) 10,188,610,560 | CONFIRMED. The 32 B/pair peak follows from L217: 8 B outer, then 16 + 8 during `-1j*`, then 16 + 16 during `exp` |
| C_max | 365,924,352 B | 64·64·N_z + 16·48·107·2,288 + 16·48·N_z = 365,924,352 | CONFIRMED |
| Peak E (m 7) / U code (m 16) / U excess (m 16) | 7,732,524,416 / 14,062,959,488 / 20,112,447,008 B | identical | CONFIRMED (N1-N3 qualify) |
| Ring phase E | 4,759,399,296 B | reproduced. Block temporaries 14 x 57 x N_z x 8 and ring temporaries 32 B·nR·N_z match lib L745-751 (`(Bd@Ar)+1j*(Bd@Ai)`: 108.6 + 108.6 + 217 MB live) | CONFIRMED |
| Steady E / U | 3.12 / 3.72 GB | reproduced | CONFIRMED |
| Column cost E / U | 0.7181 / 1.1867 s | 0.7181 / 1.1867 | CONFIRMED (N11) |
| Source update E / U | 2,768.5 / 2,990.5 s | 9.776e10 pairs x 28.32 / 30.59 ns; the module `81af8715` L136-208 is the 64 x 256 chunked dense loop, the same chunking as at DDO, so a per-pair rate transfer is reasonable | CONFIRMED (DDO module identity still ASSUMED) |
| Iteration E / U | 7,310.8 + 26.73m / 10,428.5 + 28.02m s | 7,310.8 + 26.73m / 10,428.3 + 28.02m | CONFIRMED |
| Cold build E / U | 2,910.8 / 4,967.7 s | same | CONFIRMED (N6) |
| Stage 01 E / U | 54,973 / 175,907 s | 54,973 / 175,906 | CONFIRMED, but incomplete (C1) |
| Route B E / U | 46,247 / 105,958 s | same | arithmetic CONFIRMED; bracket remains UNKNOWN (N7) |
| N8 memory (it ≥ 1 transfer E / U) | 45.2 / 61.3 GB | 45.22 / 61.29 GB | CONFIRMED (A130 model) |
| Identity-test replica / verdict E | 1.98 h / 4.93 h | 7,135 s / 17,750 s | CONFIRMED (no readout before iteration 1) |
| Old caps | 5 GiB crossed at the build of state 4 (5.82 GB); 43,200 s crossed during iteration 5 | m = 4 (5.822 GB); iteration index n = 5, i.e. the 6th iteration | CONFIRMED. "Iteration 5" is 0-based |
| A61 minimum for the serial cap | 30.17 GB | 1.5 x 20,112,447,008 = 30,168,670,512 B; 32 GiB = 34,359,738,368 B = 1.708x the U peak | CONFIRMED |

## 3. Missing-term audit (the list the task named)

| term | in the estimate? | verifier finding |
|---|---|---|
| Other stage-process transients during the build (`updated`, `g_next`, Python position, column and solution lists) | U only (+0.4 GB on B) | **N1.** About 0.57 GB alive in `complete_iteration` (solver L215, L223; controller L475-484) that is absent from the prepare-phase replay peak B. E peak about 8.3 GB if nothing in B is released. Partly offset, because base `prepare` (L92-128) builds about 0.5 GB of per-node lists inside B and frees them before the columns. No cap change |
| Stage 02 cold rebuild in a new process | yes (time); memory said "below" | **C4** (state I-1). Stage-02 U peak about 18.1 GB (B0 + S + P + F + vf51(15)). The state `savez` + `from_arrays` reload (`b9247b1a` L162-176) is about 3S + B0 ≈ 4 GB, below its vf phase. Under 32 GiB |
| I1-T point transform (~0.43 GB) | no | **Harmless.** It runs inside `_i1t`, which completes before `_build` starts (controller L484: the argument is evaluated first), so it is never concurrent with the vf peak (roster `point_transform`: 128 x 84,864 pairs at about 32-40 B) |
| Ring-table update temporaries (~0.43 GB) | yes (32 B E, 40 B U) | CONFIRMED (lib L745-751) |
| Stars radial transform | yes, cold builds only | CONFIRMED: warm builds hit the per-object cache (roster L121-127). The transient is ASSUMED (1.34 / 2.7 GB) and never at the run peak |
| Allocator retention | no | Not modelled. The 51 B/pair U excess is the only cover (N3). The vf blocks are about 5 GB each, so they are large allocations returned on free; retention matters mainly for the small-object lists |
| Digest-phase locals | partly | **N2.** `Fr`/`Fi` (91.9 MB) and the `Mc` list (74.1 MB) are still live in `build()` when `TailState()` hashes (lib L342-358, L725-790): 4.82 GB, not 4.65 GB (E) |
| Post-convergence readout (wall) | **no** | **C1**, the largest correction |
| Route-B offset stage roster | no | **N5** (INFERENCE): the Δ roster carries every accumulated route-A element. U about 13.3-19.4 GB, under 32 GiB (A61 29.1 GB) |
| Double counting | none found | B (replay peak) and S, C, P, F are separate objects. B contains `prepared`, so the extra 0.212 GB in the prepare phase (the old `prepared` still bound at solver L133) is correct, not a double count |
| Units (GB vs GiB) | consistent | GB = 1e9 everywhere in the tables. The cap is stated in GiB with its byte value. The u4 KHI sampler columns are GiB-units, and the estimate quotes them as such |

## 4. Notes (non-blocking; A115 NOTE class, no physics reading changed)

- **N1. E build-phase base (memory).** See §3. The U basis (B + 0.4 GB) covers most of it.
- **N2. Digest phase (memory).** For m ≤ 2 the build maximum is 4.82 GB (E). See §3.
- **N3. The U excess attribution is not established.**
  - The KBIG K128 rows (n=0: 1.53 GiB, n=6: 2.70 GiB, `60bf9954` §6) do not discriminate, because the n=0 peak sits in the cold stars-transform phase.
  - Both readings fit the two DDO cases: 51 B/pair (non-vf base equal to the code model) and a constant ~0.8-1.1 GB.
  - So the watch-profile line "+1.01 GB per iteration with the DDO excess" should read "+0.64 GB (code) to +1.01 GB (excess-in-vf reading)".
  - The cap uses the larger reading, which is safe.
- **N4. The cap depends on two fenced seed values. This is the most important cap note.**
  - The A61 check holds only if hi_panels_per_side = 8 (q = 17) and source_azimuth_count = 32. Both are TESTED in the T120L replay record and ASSUMED for the fenced step-5 seed.
  - At panels 12 (q = 25), the U-excess peak would be 27.75 GB, and A61 would need 41.6 GB, more than 32 GiB.
  - vf scales linearly with q x azimuths.
  - Root (who may read the seed) should confirm both values before launch, or re-derive the cap with the vf term scaled by (2p+1)·N_az / 544.
- **N5. Route-B offset stage (INFERENCE).**
  - Sources: manifest docstring L21 (offset Δ = body gas − route-A gas_IT) and TIMING_V003 §2 ("gas-only difference roster").
  - The route-B binding is a `uvt_*.py` source and was not read (H4).
  - Its vf is about 32-51 B x 36,576 x (545 + 544·n_c): U 13.3-19.4 GB at n_c 15.
  - The estimate's "route-B pairs ≤ 10 GB and stage 02 stay below" should add this single-stage peak. It is still under 32 GiB.
- **N6. Inconsistent contention in the U builds.**
  - The U cold build carries the K64 spread (x1.7172), but the U warm builds do not. Applying it to the 16 warm builds adds +7,005 s (+1.95 h) at U.
  - The U lumped fit also has no Bessel term: W0 U is 46 s against 94.8 s at E, though NGC has 194 M gas-radial Bessel calls per build.
  - Both effects are small against the 10,400-s iteration.
- **N7. Route-B U is not an upper bound.**
  - The x3.0 factor on the DDO tail-off receipts does not cover the 43-vs-12 row ratio: x4.67 if the stages are row-dominated.
  - U also excludes the route-B jet-order-2 evaluations.
  - The estimate labels route B UNKNOWN, so this is a caution for the wall cap, not an arithmetic error.
- **N8. The U path presupposes convergence at the 16th iteration.**
  - If route A has not converged by max_iterations 16, three things follow:
    - `prediction.evaluate` returns `predictions_available False` with no readout (`7ae28901` L56-58);
    - the manifest refuses (`b9247b1a` L219);
    - route B never runs.
  - The point then fails at about 50-55 h.
- **N9. Readout memory is below the peak.**
  - About d + B + 2S + C + 0.3-0.5 GB: the `columns` cache of 12,900 HI results, with two TailStates live (the boundary holds state n_c and `_pending` holds state n_c+1, controller L424, L522).
  - That is about 4.5-5.2 GB (E), well under the last build's vf phase.
- **N10. Disk.** `result.json` gains the 12,900 readout columns and the per-query details (size unmeasured), on top of the estimate's 580.6 MB per iteration (`ee27227c` ARRAY_KEYS L36; reproduced: 3 x 184,320,000 + 27,648,000 B) and the node logs. The old 32 GiB output cap is tighter than the estimate says.
- **N11. The E column cost may be low.**
  - `prepare_line` (`5c0ab4f6` L11-44) does a full `np.unique` over all waves, 80 full-length `group==n` scans and 10 einsums per kz group.
  - Its share of the G80C column may exceed the ASSUMED 50 %. At 60-80 %, c_off is about 0.70-0.80 s, against 0.65 s at E.
  - That is still inside [E, U]. The first point's `column_completed` events settle it.

## 5. Caps: do they false-stop or under-protect?

| cap | verdict |
|---|---|
| **RSS 32 GiB (34,359,738,368 B), physical footprint of the process tree, serial** | **Keep.** It meets A61 for every reading built from bytes: route A U-excess 20.11 GB (A61 30.17 GB); stage 02 about 18.1 GB; inferred route-B offset ≤ 19.4 GB (A61 29.1 GB); route-B pairs ≤ 10.0 GB. A false stop would need a peak above 34.36 GB. That would take q of 21 or more (hi_panels_per_side ≥ 10; q 19 still passes at 33.0 GB) or vf above about 60 B/pair at q 17; the first is a seed change (N4) and the second is beyond any DDO evidence. It under-protects nothing that a 1.5x rule is meant to cover. Machine-level risk is root's 95 GB watch with step-2 spikes coinciding |
| **Wall 360,000 s, serial** | **Raise to ≥ 381,500 s (106 h)** to keep the estimate's own 1.25 x U rule after C1. Or keep 360,000 s (1.18 x U) only together with the iteration-1 re-forecast that now includes the readout. Route-B evaluations remain outside U (N7), so extend deliberately rather than auto-stop |
| Old 5 GiB / 43,200 s | Contradicted, as the estimate says (reproduced) |
| N8 successor: RSS ≥ 91.9 GB; wall 211,319 s | RSS unchanged. **Wall 233,326 s** (1.25 x the corrected N8 point U) |

## 6. Source lines and hashes checked this session

| object | sha256 (from bytes) | lines read | result |
|---|---|---|---|
| serial solver | 8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469 | all 283 | L132/L133/L173/L208-214/L215/L223/L234 as cited; also L129 (`current`), L240 (relaxation) |
| controller r5 | c5bdd0553968e3f00b61db89f7944cebe51166006f58b727a7aed2a9b6a434fc | L176-285, L366-535 | g_next L483, `_build` L484, `_pending` L522, sidecar `savez`+`fsync` L519 as cited; I1-T before build (L484) |
| tail library v002 | 2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54 | L38, L342-358, L470-600, L600-800, L816-821 | CORNER_LRU 16; per-array `tobytes` digest; build order P → F → block loop; ring update; `__call__` → `jet` |
| roster | 4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2 | L95-232, L232-430 | stars cache L121-127; vf L209-219 (L217); `roster_route_a` with no element filter |
| worker (serial) | ee27227c2cee3093589ae6b6546a0d88a1bbe20c47ba4dacff497ad7cc80189f | all 162 | ARRAY_KEYS L36; binding.evaluate L145 |
| worker (parallel) | 293a417f493fee2b59176bc60873fa3cdea5e586f375efbe51cbd10651e045b1 | grep | same binding and prediction (L28, L32) |
| binding | 9b5ce82adea46c8e660f44b0fc91e8dbe5d0616cc1de1fd4467878ef3b5c0668 | L104-205 | analytic initial source required (L106); facade L118-120; prediction readout L189-194 |
| prediction | 7ae28901023974005fac9a5dc4126941371b1522837b02c81cdb5811573c1e98 | L55-180 (+grep) | **the readout (C1)** |
| manifest writer | b9247b1aef0d9c3c05757bd27d68a9964a22d078ce8189311f11e0e2ad6b4c7c | grep, docstring | accepted state n (C4) |
| prep | 8681da84bbd2b6858f5334d724b4e22e10c191e68f305b6e29df841571bf712b | L36-46, L96-130, L170-316 | panels L125; analytic fixed and initial source in the prep, so there is no dense fixed-term transform at solve start |
| streaming adapter / base v005 | cbbc4b968fc189440ddd4f516fb53f07d04a97b638fdf90fd90f50422afb928e / 7167a264aace95b0dd0732799534a39e9a271dbd9bf09abec16d02e6f647d491 | all / L84-140 | per-node Python loop; per-node JSONL with flush per record |
| HI solver / quadrature / source / line | 665b5589… / a67b526b… / 81af8715… / 5c0ab4f6… (full values in PARTIAL.md) | L86-110 / L55-75 / L136-208 / L1-60 | as cited |
| grid cut | 5d037291c8d683d7921f38365640bf41502216a67a5ed6ca84986aa671faf353 | L80-86 | no pin gives cut None |
| driver cx3r008 | 577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377 | L5058-5061, L5080, L5561-5564 (+grep of pins) | serial iff ra_workers == 1 (critic V6 confirmed) |
| TIMING_V003.md / KBIG_PROXY_V002.md / projection py, json | 4d4cac0c… / 60bf9954… / b3c678b5… , cffa3150… | all / L150-200 / all | the inputs as quoted by the estimate |

## 7. Conduct and rule notes

- **No Python.** `tools/run_fenced_c4st2.py` (`fe904509…`, the same bytes as the estimate's copy) opens 64 B of the open-name V005 and the V004 addenda and of a `uvt_*.py` before any script (L24-29, L47-53, read as text). The two-addenda rule forbids those opens. Arithmetic was done in awk only.
- **No addendum read.** Neither V006 nor V005_FROZEN was opened by me; I relied on the maps.
- **Not opened, listed or statted:** no target or velocity data, `runs_ext`, C5H, `UVT_*`, UNT_INTERNAL_RUNS, CLAUDE2/runs tree, or non-`.py` path containing ngc3198.
- **Seed path.** The NGC seed path appeared only as text inside the driver's pin table; it was not opened.
- **No project module imported.**
- **Directory reads:**
  - `ls` of my own folder, the estimate folder, and `tail_scheme_impl_c2/kbig_timing_v003/` (no NGC entries);
  - `test -f` probes of four named KBIG paths;
  - one one-level glob, `parallel_route_a_c2/*/projection_c2v001.py`. It surfaced only the single matching `.py` path, and no other entry was displayed or statted. I record it as a low-grade possible incident in the same class as the estimate's self-report.
- **Writes**, all inside this folder and new:
  - `PARTIAL.md` (created with noclobber, then appended);
  - `calc/verify_c4v001.awk`;
  - this file.
