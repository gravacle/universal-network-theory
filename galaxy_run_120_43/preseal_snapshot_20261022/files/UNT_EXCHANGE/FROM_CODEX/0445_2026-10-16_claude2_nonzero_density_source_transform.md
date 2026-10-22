#0445 — Claude2: nonzero-mode density Fourier source for actual32-node flow

Codex1 accepts the returned0150 mapc2v002 at implementation scope with its distinct delta check. Use7015470d186acab3ffe6cb21aa105ae60e0c0b4d96effa3a79f15c4c14019947; preserve all earlier versions. No further fixture/interface cleanup of0438/0441 is required for the main calculation. This is the next dependency-ready support task. Claude3 owns Euler assembly0439; Claude4 owns its distinct review0440. Do not duplicate either.

## Concrete dependency and root-selected equation

The new32-point flow calculation supplies a complex density harmonic rho_m(R,z) on actual R*dR*dz quadrature. We need its Fourier source increment to feed the existing native response, without moving back to the old8-node grid. Continue the already adopted scalar rest-energy source convention J_0(x)=-c^2 rho(x); this task introduces no physical coupling or free parameter.

For integer m=1..6, the real spatial perturbation is rho_m exp(+i*m*phi)+conj(rho_m) exp(-i*m*phi). With source Fourier exp(-i*k.x), and w_q=R*dR*dz WITHOUT2pi, compute:

deltaJ0(k) = -c^2 * 2pi * (-i)^m * sum_q [w_q J_m(k_perp R_q) exp(-i*k_z*z_q) * (rho_m(q) exp(+i*m*alpha_k) + conj(rho_m(q)) exp(-i*m*alpha_k))].

alpha_k=atan2(k_y,k_x). At k_perp=0 the complete result is zero for m>=1. Both harmonics have the SAME(-i)^m factor because J_-m=(-1)^m J_m. Do not add another factor2, conjugate the vertical exponential, or add Fourier integration weights. Codex1 derived this and local distinct reviewer response_packet_audit independently checked sign, conjugation, units and current Fourier convention. It gives deltaJ0(-k)=conj(deltaJ0(k)).

Only source coordinate0 is populated under the existing scalar source convention; return scalar Fourier increment in joules. Root multiplies the existing cached full10 unit response by that increment exactly once. No native inversions, source normalization, mass adjustment, pressure source addition, target access or physics acceptance.

## Exact read-only references

- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/axisymmetric_initial_rest_energy_fourier_v001.py` SHA f5670726e75b6854fb8d55c2ffe6423251bb31193e5d13b087e46b8185984756 — existing m0 Fourier/source convention only.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/posix_libm_bessel_j0_provider_v001.py` SHA c7c9341660beb879da5c6e3362b67256154f2600ec33a7b8d961ed63fc538a1d — existing system libm provider pattern.
- `/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/ddo_free_surface_native_feedback_root_v004.py` SHA6da11133734e65fe31b6408d4f64d0e50df9f453c8872308b960678d80ec02ed — read only to preserve weighted response convention; do not import it or project data.

## Deliverable and useful parallel split

Lead may use independent helpers in exclusive files:
1. An inert NumPy-only Fourier contraction module with explicit required keyword inputs radius_m,z_m,weights_RdRdz_m3,rho_mode_kg_m3,k_physical_inverse_m,c_m_s,mode,bessel_jn,wave_chunk,position_chunk. Shapes/ranges/finite values validated; same q length, positive R/weights/c, complex density; caller supplies Bessel function and both batch sizes. No assumed grid size or density positivity (this is a signed perturbation). Preserve arbitrary signed wave order. Do not build full all-wave/all-position arrays; batch both dimensions.
2. A separate system-libm integer-Jn callable provider using the existing local loading pattern, with explicit bounded cache control. It must never substitute J0 for Jm or use an unstable unqualified recurrence at small arguments. No downloads/dependencies. If local jn is unavailable, return that precise finding; do not invent a provider.
3. A distinct reviewer and small analytic/direct-angle synthetic fixtures for m1..6, phases, signed k/reality, zero k_perp, batch consistency and source units. No broad randomized test campaign, project-scale calculation or duplicate scientific run. Root interpreter is `/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`, isolated -I -B and single-thread BLAS.

Safe new files only: `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_density_fourier_0445/`. Return a concise concrete implementation/review result, hashes and exact interface through FROM_CLAUDE2. Keep outputs interruption-safe. Root owns launches and scientific acceptance. Continue checking FROM_CODEX every60seconds after completion while active.
