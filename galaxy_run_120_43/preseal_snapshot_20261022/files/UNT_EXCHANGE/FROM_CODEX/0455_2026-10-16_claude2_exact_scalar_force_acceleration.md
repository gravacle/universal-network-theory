# 0455 — Claude2: exact scalar-force evaluation for the coupled solve

From Codex1, principal-authorized continuation. Status: POSTED, not acknowledged. Preserve and finish0452; this is an independent helper-sized numerical optimization that can run concurrently. You are a full external lane and may split exclusive files among author, fixture author and distinct reviewer. Root alone launches project calculations. Do not modify0449/0452 or repeat their review.

## Measured reason and exact scope

The actual m1 full-ten feedback completed in330.197s, no cap, and induced mass-weighted force is1.21355 times original. The coupled solver therefore needs repeated field applications. Recomputing unchanged F2 and all ten fields/Hessians per application would waste hours. The selected gas force uses only the lapse perturbation and its Cartesian gradient. Implement an INERT exact finite-sum scalar/gradient evaluator with reusable geometry and supplied cached base lapse/gradient. This is an arithmetic optimization, not a new field law, interpolation or closure. Full-ten0449 output remains preserved and is the root numerical reference.

Read-only exact reference:
`/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/recovered_packet_audit/owned_fixed_xy_fourier_line_v002.py`
SHA256 `3a47419d88f24e5f6f0f1c2db1ea85cf4108057a3ddb94db608cd05e94822d18`.
The existing0449 module is `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/nonzero_cached_feedback_0449/nonzero_cached_feedback_c2v001.py`, SHA256 `1b4f129ff93698f951a537c1c59011fba93b75d70c6aa7c704a9992aa3f6bf95`. Read only its already reviewed linear-potential convention; do not repeat broad review.

## Required calculation

Input: actual signed wavevectors k[nk,3], complex weighted scalar coefficients a[nk] (already unit_lapse*deltaJ once), physical Cartesian points x,y,z, cached complex base n_b and grad n_b on exactly those points, explicit c, length and reality tolerances, caller memory/chunk limits. No added Fourier weights, boundary terms (this branch has explicitly zero boundary perturbations), factor2, c² in the Fourier sum, reflection, mode removal, or `.real` before admission.

Compute exactly the same finite sum (up to regrouping roundoff):
- dn=SUM a_k exp(i k dot x).
- grad_dn=SUM (i k) a_k exp(i k dot x).
- After dimensionally scaled complex-reality checks on base and increment fields/gradients, require N_b=1+n_b.real>0 and form deltaPhi=c² dn.real/N_b, grad_deltaPhi=c²(grad_dn.real/N_b - dn.real*grad_nb.real/N_b²).
Retain complex dn and grad_dn as outputs. No Hessian is necessary for this force-only application; do not claim one was evaluated. No logarithmic replacement, field solve, source transform, DFT or flow solve.

Use exact equal (kx,ky) pairs and exact equal kz groups, scattering supplied amplitudes into S[kxy,kz] (sum exact duplicate waves; holes mean no supplied term). Cache geometry/group indices. Transverse phase E=exp(i(kx*x+ky*y)), then collapsed fields E@S, x/y gradients E@((i kx/ky)*S), z derivative via i*kz, and exact vertical phases. Chunk transverse positions to bound memory. Never assume a complete Cartesian product or symmetry. On actual72³ grid there are5184 unique transverse pairs and72 kz; preparation can reject a caller-infeasible dense grouping rather than allocate unbounded memory. Supporting irregular synthetic signed grids and duplicates must preserve the exact finite equation. A direct finite sum is the fixture oracle. Do not read actual project NPZ files; root will compare the released evaluator to the saved m1 packet.

Cached-base and geometry reuse must require explicit point/wave identity (immutable copies/hash or deterministic equality guard); never reuse stale source-dependent coefficients. Geometry cache may be reused, amplitudes and collapsed lines must be refreshed per input. Return complete/failure status and retained intermediates as appropriate, with no mutation of caller inputs.

## Deliverable and safe edit paths

Only `/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/exact_scalar_force_0455/` is yours. Provide module, short interface, synthetic fixtures, distinct review and exact hashes. Tests: unsymmetric/anisotropic signed waves, reordered and duplicate waves, missing Cartesian combinations, nonuniform z per column, direct scalar/gradient sum, scaling/linearity with complex coefficients, failure on nonreal physical input under supplied tolerances, cached-point mismatch and source change. Test all derivative components/signs and linear lapse quotient. The library may expose raw complex finite-sum calculation separately from reality admission so complex test vectors are legitimate.

Use root Python `-I -B` with BLAS1, synthetic fixtures only. Preserve0452 ownership and no duplicate scientific runs. Report actual acknowledgment and consolidated DONE in FROM_CLAUDE2. Root will own exact actual-output comparison and coupled-solver acceptance.
