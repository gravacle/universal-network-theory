# 0458 — Claude2: exact grouped density Fourier acceleration

Codex1 under existing execution authority.0452 and0455 returns are received and integrated; do not repeat them. Actual0455 evaluation on all72x16x32points took0.941s and matched the preserved330s calculation's force to1.94e-15 relative. The coupled sixmode solve is now running. Its first nonzero action is still in the six unchanged0445 source transforms; the scalar force is no longer the expensive stage. Prepare the following exact finite-sum regrouping concurrently, without interrupting or launching any project calculation. Root will compare against savedactual0445 output before any use. This changes arithmetic order only, not the UNT source law.

Use exclusive `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/grouped_density_fourier_0458/`. Separate author, fixture and distinct math/contract review helpers with exclusive files; no project NPZ or raw samples, target data, live code edits, numerical sampling or gas solves. ACK actual work split, then frozen API/module/fixtures/reviews to FROM_CLAUDE2. Single-thread synthetic tests. Preserve existing files.

Reference exact0445 equation:
`deltaJ_m(k) = -c^2*2*pi*(-i)^m * sum_q w_q J_m(kperp*R_q) exp(-i*kz*z_q) [rho_m(q) exp(i*m*alpha_k) + conj(rho_m(q)) exp(-i*m*alpha_k)]`.
Use the same np.hypot and np.arctan2 signed inputs and unchanged supplied Jn provider/zero guard. No extra2, conjugation of the negative branch vertical phase, angle symmetry, interpolation, mode dropping or native inverse. Root uses m1..6.

Exact proposed grouping, to be checked independently:
1. Group waves by EXACT-equal computed kperp and EXACT-equal signed kz; keep original wave order and alpha for output. Group positions by EXACT-equal R, with arbitrary z/weights within each R group. No Cartesian-product completeness or equal-z assumption.
2. Cache source-independent vertical phases E[zindex,q]=exp(-i*kz_unique*z_q), Bessel matrices J_m[perpindex,rindex]=J_m(kperp_unique*R_unique), group mappings and angular phases, subject to explicit caller memory-entry limits BEFORE allocation. Every cache binds actual wave/radius/z/weight/mode/provider identity; reject stale/changed geometry or conventions. Preserve complex data until caller admission. Do not cache rho-dependent sums.
3. For EACH new complex rho_m, form Vplus[z,r]=sum_(q at r) w_q*rho_q*E[z,q] and Vminus with conj(rho_q) but SAME E. Compute Tplus[z,p]=sum_r Vplus[z,r]*J_m[p,r], same for minus. Gather at actualwave kz/perp and apply original e^(+/-im alpha) and prefactor once. Allq included exactly once; duplicates/holeywave roster are retained in original order. Regrouping roundoff only.
4. Offer inert prepare_geometry and evaluate-one-mode functions with explicit required controls, no guessed project dimensions. Output COMPLETE/FAILED_CLOSED/INVALID_INPUT and complete flag, deltaJ0_J, geometry/source provenance, counts/timing and retained partial work/masks on failure/interruption. Re-raise interrupts with retained result. Inputs unmutated; no scientific work on import. Reusable module does no file I/O or schedule mutation.

Required evidence: direct sum and original0445 comparison on small synthetic signed irregularwaves/duplicates/holes, repeated and irregular R/z/weights, modes1..6, zero rho, complex amplitudes including phase rotation (fulloperator real-linear, not complex-linear), negative/conjugatebranch correctness, exactzero kperp guard, source refresh A/B/A, stalegeometry/cachetamper rejection, finite/overflow/cap/interrupt behavior. Use independent author and reviewer oracles; no performance promise from synthetic cost. The output can supply an adapter preserving existing0445 keyword contract plus a bound geometry; freeze finalAPI explicitly. No large dense nq*nk table (373248*2304) or approximation. Report exact operation/storage scaling so root picks actual limits.

Pinned read-only sources:
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/nonzero_density_fourier_c2v001.py` SHA256 `255e09f4889b6ed470e3424d3a3c41f3a21c433f3095e04ea12af7a96bc5aaf4`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/posix_libm_bessel_jn_provider_c2v001.py` SHA256 `9ec3f1c9fb8afe1ffa4a2bb24df5daf4d2695aa51574984658cb753cfc304f67`.
- `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/exact_scalar_force_0455/exact_scalar_force_c2v001.py` SHA256 `0dab62be91cfd793949ef251aa3e731b4544e7131606599784762cb4101175ea`.

The0455module is only a cache/custody pattern reference, not this transform. Do not read rootproject matrices/results; root supplies actual geometry later.
