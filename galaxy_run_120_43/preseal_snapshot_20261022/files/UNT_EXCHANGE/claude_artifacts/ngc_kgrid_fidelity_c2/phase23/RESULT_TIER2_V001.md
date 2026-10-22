# RESULT_TIER2_V001: NGC3198 k-grid fidelity, Phases 2 and 3 (sealed prereg 4c2eefeb)

**Decision (mechanical): `NO_ADEQUATE_GRID`.** It is not `_WITHIN_CAP`: all ten candidates were evaluated, and none was counted not-passing because of the cap.
- aggregate_v002 (`636490cd`), as instructed, gives `NO_ADEQUATE_GRID` (`out/aggregate/AGG_V002_FINAL_20261018T001222Z.json`, `c1c289c5…`).
- aggregate_v003 gives the same decision (`AGG_V003_FINAL_…`, `6f4c8933…`).
  - v003 is v002 plus the AGG_CHECK_V001 F1–F7 corrections (`c0204d78…`).
  - It was frozen at 22:07:09Z, before any tier-2 output file existed (`aggregate/FREEZE_V003_PRE_TIER2_READ.json`).
  - Its tests pass 10/10 (`aggregate/test_out/TEST_RESULTS_V003_20261017T233807Z.json`).
  - It is **UNREVIEWED**.
- D-SPLIT is FINAL (Gf = G160L, Gf-1 = G120L, sphere reads present), so AGG_CHECK F1 cannot change the decision on these inputs. F2 and F3 also do not apply, because G160L was evaluated.
- Machine twin: `RESULT_TIER2_V001.json`. Hashes: `HASHES.txt`.

**The deciding fact (TESTED).** Every candidate fails C1 on exactly the same 12 rings: ordinals 1–8, 10 and 13–15, at R = 1.537–10.54 kpc.
- D-SPLIT classes these rings TRUNCATION_SHAPE, where A17 keeps C1 as written.
- On them S/θ ranges from 1.128 to 3.654. It is the same on all ten grids to about 3 decimals; for example ring 2 gives 3.654 on every grid. The sphere mask on G160L drops it to 0.025–1.02.
- So the residual inner failure is the kmax = 2 cube-corner truncation. No grid at fixed kmax removes it.
- At NOT_GRID rings, C1′ passes on T120L, G120L, T160L and G160L.

## Per-grid table

θ = 3.3657664138980042e-9. C1′ applies at the 85 NOT_GRID rings (reference G160L; for G160L, G120L). C1 as written applies at the 12 TRUNCATION_SHAPE rings. The C4 pass bound is e4 < θ/2.

| Grid | W | C1 as written: max S/θ, rings failing | C1(A17): rings failing (TS + C1′) | C1′ max spread/θ | C2 max e2 | C3 max e3 | C4 e4/θ (ref) | Verdict |
|---|---|---|---|---|---|---|---|---|
| G80C | 512,000 | 44.96, 97 | 42 (12 + 30) | 35.70 | 0.926 F | 0.202 F | 35.6 (G160L) F | FAIL C1, C2, C3, C4 |
| G80E14 | 512,000 | 22.18, 97 | 26 (12 + 14) | 18.01 | 0.0594 F | 0.0101 F | 17.7 F | FAIL C1, C2, C3, C4 |
| G80L | 512,000 | 36.72, 97 | 40 (12 + 28) | 31.05 | 0.911 F | 0.204 F | 30.7 F | FAIL C1, C2, C3, C4 |
| G80EL | 512,000 | 42.26, 97 | 35 (12 + 23) | 32.09 | 0.197 F | 0.0243 F | 32.0 F | FAIL C1, C2, C3, C4 |
| G96F | 884,736 | 14.00, 97 | 18 (12 + 6) | 3.864 | 0.00854 P | 0.000622 P | 3.815 F | FAIL C1, C4 |
| G96FL | 884,736 | 14.53, 97 | 25 (12 + 13) | 7.373 | 0.0475 F | 0.00346 P | 7.368 F | FAIL C1, C2, C4 |
| T120L | 1,152,000 | 10.955, 97 | 12 (12 + 0) | 0.0485 | 0.00153 P | 0.000121 P | 0.0461 P | FAIL C1 (TS rings only) |
| G120L | 1,728,000 | 10.969, 97 | 12 (12 + 0) | 0.0381 | 8.23e-5 P | 4.86e-5 P | 0.0254 P | FAIL C1 (TS rings only) |
| T160L | 2,048,000 | 10.981, 97 | 12 (12 + 0) | 0.0306 | 0.00151 P | 0.000120 P | 0.0212 P | FAIL C1 (TS rings only) |
| G160L | 4,096,000 | 10.986, 97 | 12 (12 + 0) | 0.0381 (vs G120L) | 8.24e-5 P | 4.88e-5 P | 0.0254 (G120L) P | FAIL C1 (TS rings only) |

- C2 and C3 are recomputed by v003 from the per-field values (F4), and agree with the stored flags.
- C4 passes only where its reference passes C2/C3. G160L does, so its C4 counts.
- **A14.C2 cross-check (e4/θ against G120L, reported only):**

| Grid | e4/θ vs G120L |
|---|---|
| G80C | 35.6 |
| G80E14 | 17.7 |
| G80L | 30.7 |
| G80EL | 32.0 |
| G96F | 3.83 |
| G96FL | 7.38 |
| T120L | 0.0289 |
| T160L | 0.0351 |
| G160L | 0.0254 |

  No adoption exists, so the `C4_REFERENCE_UNCHECKED` and `CHECK_DISAGREES` labels are moot.
- **A14.C5 (reported only).** e4/θ at z = ±95 kpc:

| Grid | e4/θ at ±95 kpc |
|---|---|
| G96F | 32.6 |
| G96FL | 14.5 |
| T120L | 21.0 |
| G120L ↔ G160L | 24.0 |
| T160L | 21.0 |

  Tier-1 grids have no z95 reads. The per-ring maximum of e4/dL_ref is 0.0055–0.014 on the T and G120/160 grids, and 1.1–9.6 on the others.
  The ±10/20/30 kpc profile is converged to 0.025θ, but the profile at 95 kpc differs between the two finest grids by 24θ. That is UNTESTED as a criterion, and it is the height where the free-boundary search ends.
- **R1 replays (reported only; confined columns of 32 at 95 kpc):**

| Grid | Ring 2496 | Ring 2560 | Ring 3360 |
|---|---|---|---|
| G96F | 32 | 26 | 0 |
| G96FL | 32 | 26 | 4 |
| T120L | 32 | 26 | 4 |
| G120L | 32 | 26 | 4 |
| T160L | 32 | 26 | 0 |
| G160L | 32 | 26 | 0 |

  The count at 136.5 kpc is identical in every case. Confinement at 81 kpc still flips with grid choice (0 vs 4 columns).
- **R2, max S/θ beyond 66.904 kpc:** G96F 91.2, G96FL 77.0, T120L 36.9, G120L 36.9, T160L 28.1, G160L 28.2.

## D-SPLIT (TESTED; Gf = G160L, Gf-1 = G120L, sphere mask keeps 2,722,800 of 4,096,000 nodes)

| Class | Rings | Ordinals / R |
|---|---|---|
| GF_PASSES_C1 | 3 | 0, 9, 11 |
| TRUNCATION_SHAPE | 12 | 1–8, 10, 13–15 (1.537–10.54 kpc) |
| NOT_GRID | 85 | 12 (8.24 kpc), and 16–99 (10.91–66.72 kpc) |
| QUADRATURE_LIMITED | 0 | — |

- **A14.C4.** The relative drop S(G120L) → S(G160L) is tiny. Its median by R third is 1.1e-4, 2.4e-4 and 2.4e-4. The OLS slope is −3.6e-6 per kpc.
- Premise P1 is falsified at the NOT_GRID rings, which is its pre-registered deciding observation.

## Next steps by class (prereg decision_rule; A11 option (b) is the counted fallback)

- **TRUNCATION_SHAPE:** run the A1-numerics truncation test for NGC3198 (kmax 3–4, or a sphere at fixed source), which KMAX does not cover (NG2 F4). This is the only class that blocks adoption here. T120L, G120L, T160L and G160L fail nothing else.
- **NOT_GRID:** register in-plane response anisotropy as an operator property. The per-azimuth versus m=0 columns question (audit H3) becomes the next deciding item.
- **Fallback (b):** its registered limit stands. The TS failures lie at 1.5–10.5 kpc, inside any roster cut.
- No QUADRATURE_LIMITED rings and no C2/C3/C4-only failures exist, so the "≥ 200-node axes" step is not triggered.

## Cost (P2; measured, under machine load average 16–22)

| Grid | Iteration-0 prep CPU-s (prep_inputs + response) | Peak RSS, any process | Line prep + 9 reads, s per column | Lane CPU-s, all jobs |
|---|---|---|---|---|
| G96F | 614 | 0.92 GiB | 0.381 | 2,720 |
| G96FL | 609 | 0.92 GiB | 0.372 | 2,671 |
| T120L | 424 | 1.09 GiB | 0.530 | 3,258 |
| G120L | 1,050 | 1.50 GiB | 0.878 | 5,815 |
| T160L | 754 | 1.68 GiB | 0.949 | 5,825 |
| G160L | 2,248 | 3.00 GiB | 2.418 | 19,518 (incl. sphere 4,327) |

- **P2:**
  - Per-column cost is close to linear in W: G160L takes 2.42 s against the 2.25 s projected (0.281 × 8).
  - Iteration-0 preparation is sublinear: 2,248 s against 3,032 s.
  - RSS is far below the probe: 3.0 GiB against 8.98 GB projected.
  - All six tier-2 grids passed the memory pre-probe (`out/MEMPROBE_*.json`).
- **CPU:**
  - Phase 2/3 jobs used 11.06 CPU-h. Phases 0–1 used 2.68 CPU-h, for a lane total of 13.74 of 36 CPU-h. Checker and aggregate runs are not counted.
  - Wall: started 22:03:48Z, last job ended 00:12:16Z. The cap is 08:26:42Z.
- **Concurrency:** at most 6 compute processes (`dag_queue_v001`, watchdog). No per-process cap kill occurred. The idle queue scheduler is one extra process, as with E3.

## Hygiene and deviations

- **Preparation:** tier-2 preparation went through `prep_v001.py <G> hovr --hovr-review check/CHECK_V001.md 9d6d9408…`.
  - Each compute/tools file was run unchanged, with its bytes verified against compute/HASHES.txt, through `tools/run_p23_v001.py`.
  - The launcher redirects output roots to phase23/ and writes JSON by exclusive create, not by tmp + rename.
  - `--z95` adds z = ±95 kpc to the ring reads, which are reported only.
- **D-SPLIT sphere reads:** these come from `tools/dsplit_sphere_v001.py`. Its arithmetic is the same as `sphere_info_v001`. Its scope names D-SPLIT, and it records grid and W (F5).
- **What was not done:**
  - No route-A or forward run.
  - No target or velocity file was opened, and no `result.json`.
  - Nothing was deleted, moved or renamed.
  - ~/.codex was not touched.
- **Deviation D1: tier-2 criteria were read through an aggregate whose corrections are unreviewed.**
  - AGG_CHECK_V001 requires a reviewed aggregate_v003 before any tier-2 criterion is read. The workflow ordered aggregate_v002.
  - Mitigation:
    - v003 was written and frozen before any tier-2 output existed;
    - both versions give the identical decision;
    - the F1 failure scenario cannot arise on these inputs, because D-SPLIT is final.
  - **The decision stands provisional until v003 is reviewed** (code-only review).
- **Phase 3 order:** Phase 3 ran in stages: G160L, G120L, G96F and G96FL, then T120L after the 96-level aggregate showed no passer, then T160L. This follows the prereg stop rule.
- **E1:** one aggregate command failed under zsh word splitting before running anything. Only the empty dir `out/aggregate` had been created.

## UNTESTED

| Item | Deciding test |
|---|---|
| Review of aggregate_v003 (F1–F7, I13) | Independent code-only check |
| Whether any grid passes C1 at TS rings with kmax > 2 | A1-numerics kmax 3–4 / sphere test for NGC3198 |
| 95 kpc vertical-profile convergence (24θ between G120L and G160L) as a fidelity criterion | Not in the prereg; needs root ruling or a successor prereg |
| Physical outer-gas confinement | Never decided by replays |
| Equilibrium origin of the C̄ in-plane anisotropy (A18) | Sampler lineage tests |
| Iterations ≥ 1 cost | No iteration ≥ 1 exists |
| A14/A17 text as read at `f925989b` | V004 is now `ffed3096`, with A18 appended; checked against the current A14 and A17 |
