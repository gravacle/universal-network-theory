# TIER2_CHECK_V001: independent check of RESULT_TIER2_V001 (k-grid fidelity, Phases 2 and 3)

**Verdict: CONFIRMED.** `NO_ADEQUATE_GRID` follows mechanically from the sealed rule (prereg `4c2eefeb`) with root errata A14 and A17. I re-derived every decision input with my own scripts, without importing aggregate_v002 or aggregate_v003.

Because of that, the decision no longer depends on the unreviewed v003 (deviation D1). The formal code-only review of v003 is still open; see N4.

Checked inputs (sha256 from bytes, 2026-10-18 ~00:15Z):

| File | sha256 |
|---|---|
| RESULT_TIER2_V001.md | `ba8ef623…` |
| RESULT_TIER2_V001.json | `245dbbc5…` |
| phase23/HASHES.txt | `70396483…` |
| prereg JSON | `4c2eefeb…` |
| AGG_V002_FINAL | `c1c289c5…` |
| AGG_V003_FINAL | `6f4c8933…` |
| aggregate_v002.py | `636490cd…` |
| aggregate_v003.py | `c0204d78…` |
| AGG_CHECK_V001.md | `0a8ef15c…` |
| check/CHECK_V001.md (H-OVR review) | `9d6d9408…` |
| root addendum V004 | `9f3ce6aa…` (current bytes; see N6) |

**Integrity.** Every one of the 1314 HASHES.txt entries verifies from bytes (`out/t2chk/HASHES_VERIFY_20261018.txt`). The file set under phase23/ outside check/ equals the HASHES set exactly.

**Hygiene.**
- Runtime: codex python `-I -B`, numpy only, `nice -n 10`, BLAS threads 1, at most 4 concurrent processes.
- Writes: only under `phase23/check/`, by exclusive create.
- Not opened: any target or velocity file, any result.json, any speed at query radii.
- No launch. The only operator use is iteration-0 lnN evaluations.
- Cost: about 1 CPU-h for this check, which is not counted in the lane total.

## 1. C3 and C2 re-derived independently (TESTED-POSITIVE)

Tool: `tools/t2chk_kf_v001.py`. It differs from `known_field_v001` in three ways:
- Gauss–Legendre nodes come from Golub–Welsch (eigh of the Jacobi matrix).
- It builds its own node tensor.
- Its K2 1D reference uses a different panelling: each T-table interval is split in two, at order 10.

It reads the 79-ring C2 set and the 175 C3 radii from the sealed definitions.

| Grid | own C2 max e2 | lane | own C3 max e3 (E12) | lane | Verdict |
|---|---|---|---|---|---|
| G96F | 0.008544 | 0.008544 | 6.22e-4 | 6.22e-4 | C2 P, C3 P |
| G96FL | 0.04752 | 0.04752 | 3.46e-3 | 3.46e-3 | C2 **F**, C3 P |
| T120L | 1.525e-3 | 1.525e-3 | 1.207e-4 | 1.207e-4 | P, P |
| G120L | 8.230e-5 | 8.230e-5 | 4.864e-5 | 4.864e-5 | P, P |
| T160L | 1.510e-3 | 1.510e-3 | 1.203e-4 | 1.203e-4 | P, P |
| G160L | 8.245e-5 | 8.245e-5 | 4.884e-5 | 4.884e-5 | P, P |

- **Agreement with the lane:** per field, my values agree to ≤ 1e-8 relative, which is the reference-integrator floor. Every PASS flag agrees. My K1 reference self-check is 4.8e-14.
- **The H-OVR operator k-set is the prereg candidate grid** (all six tier-2 grids):
  - `k_physical` equals the prep v001:146-152 formula bitwise;
  - `wavevectors` equals `k_physical` bitwise;
  - the `dk_weights` match: relative difference 0.0 against the prep formula, and ≤ 8e-13 against my Golub–Welsch weights.
  - So the known-field nodes are the operator's nodes.
- **G160L passes C2 and C3,** so its C4 counts.

## 2. C1, A17 C1′ and C4 re-derived from the raw ring files (TESTED)

Tool: `tools/t2chk_rings_v001.py`, output `out/t2chk/T2CHK_RINGS_V001.json`.
- **θ:** recomputed from hi v002, log1p(h0/c²), and equal to the sealed value bitwise.
- **Rings:** 100 rings with R ≤ 66.904 kpc, and ring R is identical across all ten grids.

Every number in the result's per-grid table is reproduced:
- C1 as written: max S/θ and 97 failing rings on each grid.
- C1(A17): the TS + C1′ failure counts 42, 26, 40, 35, 18, 25, 12, 12, 12, 12. Zero failures at GF_PASSES_C1 rings.
- C1′ maxima: 35.7 down to 0.0306.
- e4/θ against G160L: 35.61, 17.72, 30.75, 32.01, 3.815, 7.368, 0.04608, 0.02541, 0.02121; G160L against G120L: 0.02541.
- A14.C2 cross-checks against G120L: T120L 0.0289, T160L 0.0351, G160L 0.0254.
- A14.C5 at z = ±95 kpc: G96F 32.6, G96FL 14.5, T120L 21.0, G120L↔G160L 24.0, T160L 21.0.

**Spot re-evaluation of lnN** (`tools/t2chk_lnN_v001.py`). This is my own driver: the operator blobs are sha-checked against OPERATOR.json, and lnN goes through the pinned replay_c1 metric point.
- Rings checked: 2, 9, 12, 15 and 50, all 32 columns.
- G120L and G160L: all 7 heights reproduce the lane ring files **bitwise**.
- Sphere-masked G160L: z = 0 reproduces bitwise, with 2,722,800 nodes kept.

**Adopted/best grid.** Nothing is adopted. The cheapest grid whose only failures are at the TS rings is T120L:
- C3 1.21e-4 (pass);
- C2 1.53e-3 (pass);
- C4 0.046 θ (pass);
- C1 fails at exactly the 12 TS rings.

## 3. D-SPLIT re-derived (TESTED; final)

- **Grids used:** Gf = G160L and Gf-1 = G120L. These are the two finest evaluated isotropic grids, with distinct W.
- **Counts:** GF_PASSES_C1 3 (ordinals 0, 9, 11), TRUNCATION_SHAPE 12 (ordinals 1–8, 10, 13–15; 1.537–10.541 kpc), NOT_GRID 85 (ordinal 12 and 16–99), QUADRATURE_LIMITED 0. These are identical to the result.
- **Refinement drop:** the largest |S(G120L) − S(G160L)| is 0.018 θ, far below θ/4.
- **Sphere mask:** at the TS rings it brings S down to 0.025–1.020 θ.
- **Sample rings** (S/θ on G160L; sphere-masked S/θ; change S_sph − S, in θ):

| Ring | R (kpc) | S/θ | S_sph/θ | S_sph − S | Class |
|---|---|---|---|---|---|
| 2 | 2.19 | 3.654 | 0.051 | −3.60 | TS |
| 9 | 6.36 | 0.644 | n/a | n/a | GF_PASSES_C1 |
| 12 | 8.24 | 1.108 | 0.660 | −0.448 | NOT_GRID (N2) |
| 15 | 10.54 | 1.640 | 1.020 | −0.619 | TS |
| 50 | 33.93 | 5.578 | 5.587 | +0.009 | NOT_GRID |

  The values for rings 2, 9, 12, 15 and 50 were re-evaluated independently, as described in §2.
- **Harmonics** (`tools/t2chk_harm_v001.py`). At the TS rings the full G160L field has an m=4 amplitude of up to 1.81 θ. The sphere mask reduces it to 0.066 θ, and m=8 goes from 0.37 θ to 0.003 θ, while m=2 (0.50 θ) is unchanged. This confirms the cube-corner (m=4/8) attribution of the TS failures.
- **A14.C4 trend:** over all 100 rings, the median relative drop by R third is 9.1e-5, 2.3e-4 and 2.3e-4, with slope −3.3e-6 per kpc. The lane uses the 97 failing rings and gets 1.1e-4, 2.4e-4, 2.4e-4 and −3.6e-6. The two are consistent.

## 4. Decision walk (TESTED)

I applied the sealed rule myself: pass = V1–V5 ∧ C1(A17) ∧ C2 ∧ C3 ∧ C4, with the C4 reference required to pass C2/C3.
- **No candidate passes.**
- Under A17 the TS rings keep C1 as written, and every grid fails C1 there, with S/θ between 1.128 and 3.654. The spread across all ten grids at those rings is at most 0.0082 θ.
- **Outcome: `NO_ADEQUATE_GRID`.** It is not `_WITHIN_CAP`: all ten candidates were evaluated, none was counted out by the cap, and nothing was over the cap.

**Phase 3 order** (DAG logs plus file mtimes):
1. G160L, G120L, G96F and G96FL.
2. The stage-A aggregate at 23:38:23Z, showing no 96-level passer.
3. T120L, then the B1 aggregate at 23:50:54Z.
4. T160L.

Running G120L before T120L is not a violation. A14.C2 requires G120L because G160L is the C4 reference, and D-SPLIT needs it. With no passer, every W level had to be evaluated.

**Caps:**
- 11.06 CPU-h over Phases 2/3, my sum of the DAG `end` events.
- At most 6 concurrent jobs.
- Peak RSS 3.00 GiB.
- Every job exited rc 0.
- Last job end 00:12:06Z, within the 08:26:42Z wall cap.

**v003 freeze:** aggregate_v003 has mtime 22:05:29Z, the freeze record is 22:07:09Z, and the first tier-2 output (KF_G120L) is 22:07:25Z.

## 5. Notes (none changes the decision)

**N1. The m=4 structure at the NOT_GRID rings does not come from the cube corners or from an unrefined panel** (diagnostic, TESTED). Tool: `tools/t2chk_boxes_v001.py`, which evaluates lnN0 on inner tensor boxes B(c) = {max|k_i| < c}.
- **The [0, 0.01] panel is not refined between Gf-1 and Gf.** It is order 3 in both, and B(0.01) is bitwise identical in G120L and G160L (216 nodes, same wavevector and response sha). The D-SPLIT QL test therefore cannot see that panel.
- **Its φ-structure is small:** at most 0.73 θ spread at ring 99 and 0.012 θ at ring 12. It is m=2, with m=4 ≤ 0.007 θ. So it cannot by itself account for the NOT_GRID failures (S up to 11 θ).
- **Where the m=4 comes from:** an m=4 of about 1.9 θ at the outer NOT_GRID rings comes from the [0.03, 0.3] shells. Those shells are refined (G120L 5,8 vs G160L 6,10), and their contribution agrees between the two grids to ≤ 0.003 θ.
- **Reading:** the NOT_GRID φ-structure includes a grid-stable m=4 on top of the A17 C̄ m=2.
- **UNTESTED:** whether that m=4 is a property of the exact operator (cubic lattice) or a tensor-quadrature effect shared by both grids. That question belongs to the registered A18/H3 next step. NOT_GRID still reads "insensitive to refinement of panels ≥ 0.01/kpc and to the cube corners", not "insensitive to all quadrature".

**N2. Ring 12 (8.24 kpc) is a borderline NOT_GRID.**
- The sphere mask lowers S by 0.448 θ, against a θ/2 threshold, so the margin is 0.052 θ. S_sph = 0.66 θ < θ.
- **If it were TS:** C1 as written would fail on every grid, since S/θ = 1.107 everywhere. The decision would be unchanged and the TS range would be the same.

**N3. Two reported-only items differ from the result.**
- **(a) Per-ring e4/dL_ref (A14.C5).** The result normalises by max over (φ, z) of |dL_ref|, which gives T120L 0.0137, G120L/G160L 0.0063 and T160L 0.0055; I reproduce those values. Normalising per height gives larger values: T120L 0.027, G120L/G160L 0.023 and T160L 0.0055. A14.C5 does not fix the normalisation.
- **(b) Last job end.** The result's "last job ended 00:12:16Z" is 00:12:06Z in the DAG log. This is cosmetic.

**N4. aggregate_v003 code (a read only, not the formal review).**
- F1–F4, F6 and F7 are implemented as AGG_CHECK_V001 asked.
- **F5 is partial:** `load_sphere_v003` checks grid, W and scope, but not that every file carries the same `kept_nodes`, which F5 asked for. On these inputs all 10 sphere files carry 2,722,800, so this is TESTED harmless here.
- The formal v003 review remains UNTESTED. The decision does not rest on it (§2–§4).

**N5. A14.C3** (option (b) on an adopted grid) is moot because nothing is adopted. The registered limit of fallback (b) stands, since the TS rings lie at 1.5–10.5 kpc.

**N6. Root addendum.** V004 is now `9f3ce6aa`; A19–A26 were appended after `ffed3096`. I read A14 and A17 in the current bytes, and the result applies them as written. None of A19–A26 amends this prereg.

## Status ledger

| Status | Items |
|---|---|
| TESTED-POSITIVE | HASHES 1314/1314; C2/C3 per field on all six tier-2 grids; operator k-set equals the candidate definition; lnN bitwise on 5 rings × 32 columns (G120L, G160L, sphere G160L); C1, C1′, C4, A14.C2 and A14.C5 for all ten grids; D-SPLIT classes for all 100 rings; decision `NO_ADEQUATE_GRID`; Phase-3 order; caps |
| TESTED-NEGATIVE | Every candidate on C1(A17) at the 12 TS rings |
| UNTESTED | Formal aggregate_v003 review; C1 at the TS rings with kmax > 2 (deciding test: the NGC kmax 3–4 / sphere test); origin of the grid-stable m=4 at the NOT_GRID rings (N1); convergence of the shared [0, 0.01] panel (N1); 95 kpc profile convergence as a criterion |

## Files (this check)

- `check/TIER2_CHECK_V001.md`
- `check/tools/t2chk_rings_v001.py`, `t2chk_kf_v001.py`, `t2chk_lnN_v001.py`, `t2chk_harm_v001.py`, `t2chk_boxes_v001.py`
- `check/out/t2chk/`: T2CHK_RINGS_V001.json, T2CHK_HARM_V001.json, KFCHK_<G>.json (6), LNCHK_G120L_full.json, LNCHK_G160L_full.json, LNCHK_G160L_sphere.json, BOXES_G120L.json, BOXES_G160L.json, HASHES_VERIFY_20261018.txt, *.log
- `check/HASHES_TIER2_CHECK_V001.txt`: sha256 from bytes of all of the above, including this md
