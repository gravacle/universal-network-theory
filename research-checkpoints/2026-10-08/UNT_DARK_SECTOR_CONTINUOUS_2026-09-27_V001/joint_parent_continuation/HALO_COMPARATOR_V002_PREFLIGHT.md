# Independent same-source halo-comparator preflight

2026-09-29. Read-only review of the complete helper, both wrapper versions and prospective execution criteria. **No blocking mathematical, extraction or implementation defect found.** No halo fit or field solve was executed by this reviewer.

Reviewed SHA-256 identities:

| File | SHA-256 |
|---|---|
| `halo_profile_fitter_v001.py` | `e8bc0d90c68fd81a5a78525870c19f4d97b3e1bf8bebb1820fa40b4098201df1` |
| `halo_comparator_v001.py` | `94d8cee705a1fe41bca8dc7b509ec637b2160d0b936142722a75c0c15075c8ee` |
| `halo_comparator_v002.py` | `e83cc1f456056b31c273e7dba54553572be6bc899f31499ddd01c0bb04fdb653` |
| `HALO_COMPARATOR_EXECUTION_V001.md` | `c132d8b016830162ef611c1890b8a080fdaf84d2b46f1330c3310a2e5ff55057` |
| `HALO_COMPARATOR_PROPOSAL_V001.md` | `0a4df12fd4f557e818da36b06039f0298818548a7669f1ae8a0e451a045bfea6` |
| `HALO_COMPARATOR_V002_REPAIR.md` | `519f69b4a08d4bdf923430bdd7761a35683f0fc9962f2638d29821040a8a038a` |
| `HALO_COMPARATOR_V002_FROZEN.json` | `12e1f8e99f8d64e67fcdc639c475402c8f4fcf28cadc0bf088621deb333e1727` |

All 147 files in the published freeze match their recorded bytes. The V001-to-V002 diff is confined to accepting the exact existing `COMPLETE_DESCRIPTIVE_COMPARISON` status for `ROTATION_COMPARISON.json`, preserving V001/error evidence in ancestry, and using successor output identities. It does not relax an observational or numerical criterion.

The small-x NFW and ISO series have the correct coefficients and leading powers. The direct logarithmic kernels and their slopes agree algebraically with the positive spherical-density integrals. Normalization at a fixed pivot and `dF/dell=F(slope_pivot-slope_radius)` are correct, including both explicit scale asymptotes. Positive observed velocities give the stated strictly convex fixed-shape velocity-SSE amplitude problem; `max(y²/F)` safely brackets its derivative zero without an astrophysical prior. Zero-amplitude and scale-limit solutions remain explicit.

The wrapper passes each source's all-radius median as the fixed pivot for both fitting masks. It uses saved Newtonian baryonic squared speeds, unchanged network predictions and the exact same observed velocity/error/radius rows. It neither substitutes SPARC component forces nor uses the earlier fitted-distance curves. NGC3198 retains all 43 rows, DDO154 all 12, with the predeclared 37/9-row R≥2 fitting sensitivity. Every selected fit is reconstructed over its full original row set; source variants are not optimized or discarded.

Both grid resolutions, finite endpoints, exact size limits, all sampled local-minimum brackets and the A=0 control are checked or retained. The 128-node mass-integral controls are genuinely different from subtracting the closed-form kernels against themselves. Synthetic recovery is separate from observed fits. Digests summarize regenerable grid evaluations while selected full curves and candidate parameters survive publication. Grid agreement remains a practical search convergence test, not a rigorous global-minimum or statistical model-selection certificate.

This review author also drafted the prospective source-census proposal; independence here is from the helper and wrapper implementation, not from that protocol design. The resulting comparison remains exposed-data, fixed-source and descriptive, with no new conclusion about observational covariance, native gravity binding or joint-program completion implied by a numerical pass.
