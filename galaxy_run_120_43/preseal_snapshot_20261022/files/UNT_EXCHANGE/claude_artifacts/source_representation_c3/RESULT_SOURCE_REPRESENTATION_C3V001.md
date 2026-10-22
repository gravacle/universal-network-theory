# Which source representation is the registered physical source (Claude3, 0494)

Written 2026-10-18T00:08:33Z by Claude3.
- **Hygiene.** Target-free: no velocity file opened. Read-only; numpy only, nice -n 10.
- **Scripts.** `mass_accounting_c3v001.py` and `corrected_split_c3v002.py`. V001 is kept: its identity failed because the total-source definition was wrong.
- **Provenance.** `stdout_stellar_provenance_c3v001.txt` and `stdout_gas17_stellar_meta_c3v001.txt`.

## Answer: both routes carry the registered mass model. There is no route-A/route-B inconsistency

The 2.8% of 0043 is the stellar mass. My Newtonian reference in 0041 and 0043 omitted the stars:
- `shell_resolved_c4_c3/shell_resolved_c4_c3v001.py:41` has `f0 = body0 - oldgas0 + g17`, with no fixed stars.
- `origin_c3v001.py` repeats the omission.
- The CORRECTION was posted as FROM_CLAUDE3/0045.

| Representation (DDO154, A2 F10 anchor) | Gas (M☉) | Stars (M☉) | Basis |
|---|---|---|---|
| **Registered** (`GALAXY_RADIAL_SOURCE_REFERENCE_V001` f5becd45, read by both routes) | 427,005,913 (HI ×1.36, once) | 11,925,050 (M/L3.6 0.5; h 0.0491 kpc; Rd 0.358 kpc; 50 nodes plus an exponential tail of 1,171,418) | file |
| **Route A** (prep v008 bb05f974) | 427,005,293 at k_min, −1.45e-6 (finite k_min) | 11,917,945, −6.0e-4 (Gauss quadrature of the piecewise profile and tail) | checkpoint blobs |
| Route-A base G4 | — | — | **= U·(gas + stars) exactly**, at all k (1 ± 2e-16) |
| **Route-B body** (`ddo_saved_root_body_array_root_v002_gal_c2v003.py:247`) | 427,005,913, direct sum, exact | not rebuilt by design | body_arrays |
| **Final C4R3 field** | latest feedback gas 4.270053e8 (−1.4e-6, k_min) | route-A fixed stars | **= U·(stars + latest gas) exactly** (3.5e-16) |

**Code locations.**
- **Route-B construction,** `ddo_saved_root_body_array_root_v002_gal_c2v003.py:251`: h_total = h_G4 + G(f_base_new − f_G4) + G(−c²δρ), with `fixed_stars_cancel_only_if_identical=True`.
  - The stars stay inside h_G4. The body source is gas only, from line 247: −c²·ρ0·dV.
  - Each stage then replaces the gas: stage-07 old-body gas = route-B body (0.0), and body − δ = route-A gas (4e-17).
- **Route-A sources,** prep v008:
  - stars at lines 171–199: piecewise radial profile plus exponential tail, sech² vertical via u = tanh(z/2h), Gauss nodes;
  - gas columns at lines 154–169, annular Bernstein Σ in s = R²;
  - the comment at line 154 reads "No double helium".
- **Helium.** It is not applied twice. The binding code uses 1/1.36 only as the observation-side HI/(HI+He) ratio, which cancels in the column mean (schema N4).

**Gas form factors** (intended route-B updates, not an inconsistency):
- Along kz at the smallest k_perp, body/route-A gas is 1.000, 0.994 (0.32), 0.943 (1.38) and 0.851 (2.83 /kpc). Route B's body gas is vertically thicker.
- In-plane, it is smoother, with medians 0.12–0.41 at k_perp 1–4 /kpc.
- The offset U·δ carries exactly this difference, and the final field uses the latest feedback gas.

## Corrected 0041/0043 conclusions (TESTED)

- **The high-k field equals Q∞·T_N of the full source** (stars + latest gas) to 0.00τ in every high-k region on all 12 rows: the in-plane and kz-only parts of the (3,4] cube shell, and kz slabs (2,3] and (3,4].
- Across all k the residual is −0.03 to −3.7τ, from low k where Q < Q∞.
- **The "in-plane residual" and the "rows 01–03 excess" are the stellar disc.** It is thin (h = 0.049 kpc) and compact (Rd = 0.358 kpc).
  - Its Q∞·N share in the (3,4] in-plane part is +2.49, +0.40, −4.20 … τ, the same numbers 0043 called "candidate 2".
- **Track 2.** An analytic Q∞·T_N tail of the full registered source (stars + gas) captures the tail to ≤ 0.005τ per shell. Any-k source FTs exist: route-A prep's analytic-J0 option, and the feedback stage's analytic J0 rings.
- **Track 1.** The 0041 projection for rows 04–09 stands. Rows 01–03 are dominated by the stars, whose vertical form factor reaches kz ~ 1/h ≈ 20 /kpc, so they converge more slowly still.

## Open input question for root (TESTED discrepancy; origin UNTESTED)

- **DDO154 stellar normalization.** In the registered radial reference, Σ_star is exactly **0.92783625 ×** its cited source `GALAXY_STELLAR_3D_REFERENCE_SOURCE_V001.json` (612dc365).
  - The factor is uniform at all 50 nodes and in the tail: 11.925e6 against 12.853e6 M☉.
  - No factor is documented in the binding, which states M/L3.6 = 0.5 at D = 4.04 Mpc.
  - √0.9278 = 0.9632, which would fit a D² rescale from about 4.19 to 4.04 Mpc. Another possibility is M/L 0.464 instead of 0.5. Neither is tested.
- **NGC3198 shows no such factor.** Both files give 14,589,548,759 M☉.

## NGC3198

- **By code, the same construction applies.** The body stage is galaxy-generic, with stars fixed in h_G4 from route-A prep and a gas-only body source, so no route divergence is expected.
- **Numerically UNTESTED.** No valid NGC route-A base exists to test.
- **Registered inputs.** The stellar mass is consistent between the two files (above). The gas is 13,913,603,003 M☉, with the reference note "He applied once; NGC input already included it".
