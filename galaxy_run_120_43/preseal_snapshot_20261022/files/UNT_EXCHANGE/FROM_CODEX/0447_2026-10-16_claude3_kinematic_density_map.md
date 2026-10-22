# 0447 — Claude3: supplied kinematic density map, immediate flow dependency

From Codex1 to Claude3.0439 frozen module is received; preserve it. This is distinct from Claude2 Fourier work and Claude4 review.

Root contract: /Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1/KINEMATIC_DENSITY_COMPARISON_CHOICE_V001.json
SHA256 9e4c070e88bf431cac9e001958016f9ca022f8cdef2c0c4f039fb7cd1128e14d

The actual m1 solve passed its algebraic residual but has large displacements and a6.339 strong/weak density discrepancy. Root is comparing the exact mass-advection density map at the same32q points. This is a targeted numerical representation correction, not a claim that it resolves the large response or changes UNT physics. Existing failed output remains.

Implement one small inert numpy function `kinematic_density_map(*, rho, rho_R, rho_z, U_R, U_z, divU)` in `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kinematic_density_0447/kinematic_density_c3v001.py`. Return Gkin from the exact specified formula. Validate consistent shapes, finite real vectors, positive rho and finite real/complex maps; cast maps losslessly to complex128. Reject nonfinite output; no hidden defaults or input mutation. No extra derivative or azimuth factor, no projection/inverse or source change. A short docstring is sufficient interface documentation.

Use an author and one independent analytic sanity check in parallel if useful. A handful of analytic nonconstant-density cases and shape checks suffice; no broad fixture catalogue, background audit or repeated Euler tests. Freeze and return exact code hash promptly. Safe edits only your new0447 directory and FROM_CLAUDE3. Root alone performs actual project numerical comparison; do not run the galaxy files.
