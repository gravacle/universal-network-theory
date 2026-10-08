# Material controls pass; the declared source-zero branch is anisotropically supercritical

2026-10-05 UTC. Exact anisotropic extension of the same conditional surface
band, using the frozen prospective protocol and source. All 763/763
arithmetic checks passed. The scientific source-zero positive-stiffness gate
FAILED: every tested nonconformal shape has a supercritical susceptibility
axis. These are separate outcomes. This receipt must not be relabeled as a
successful joint galaxy-and-expansion model.

Root approved the source/protocol before execution, including the tangent
metric, exact stable kernel, all 81 prestress-inclusive material Hessian
entries, susceptibility tensor and source-cusp extrapolation. Root also
accepted the independent nonconformal proof stated below. The immutable
receipt retains its prospective pending-root-review arithmetic status;
post-execution qualification is limited to the checks actually performed.

## Execution and custody

- One owned numerical worker on this Mac; PID 23065, PPID 11865.
- Exec session 68107 completed with exit 0. No numerical worker remains
  active on behalf of observer_cosmography.
- Receipt start: 2026-10-05T11:15:32.521497+00:00.
- Recorded runtime, including initialization: 3.4365522090811282 seconds.
- Peak resident memory: 39,747,584 bytes, approximately 37.91 MiB.
- NumPy 2.3.5; OPENBLAS_NUM_THREADS, OMP_NUM_THREADS, MKL_NUM_THREADS and
  VECLIB_MAXIMUM_THREADS were all 1. PYTHONDONTWRITEBYTECODE was 1.
- No failed attempt, repeat, repaired tolerance, new fit or extended worker.
  The only numerical receipt is the exclusively created V001 JSON.

SHA-256 custody:

| Artifact | SHA-256 |
|---|---|
| Source anchor, SURFACE_BAND_SHARED_ACTION_PROPOSAL_V001.md | 1228f453e5bb568014346fb4d55cd11a389da7da3486ba49c8d4d4ad7748e9cd |
| Frozen protocol, SURFACE_BAND_ANISOTROPIC_GATE_V001.md | f76c7f05fc2783c64375a78d847fd7120ea6c0efd333a7820ef94bd3183c0a72 |
| Worker, surface_band_anisotropic_gate_v001.py | 450921db2163f15271e081bc89f4bb89d21845d98e7ab8452a53d65931d36190 |
| Raw JSON receipt | 2ecf65f2ca2402372a535931cac307e9ea1df356cde0e59f38b859079f0f7bf3 |
| Canonical receipt payload | 4d2c88657701e1185657f300920b77a56792580a840b41e75d3f8702ee7b47db |

The canonical hash was independently recomputed from the parsed receipt,
omitting only its own canonical hash field, using sorted compact JSON and
disallowing nonfinite values. It matches. Protocol, source and anchor hashes
still match the receipt; none was changed after execution.

## Exact band and material result

The declared reference-material tangent metric and source port are

    a = sqrt(u^T(E^T F^T F E)^-1u),
    x = (d0/Lambda0)|F^T b|,
    E_band = -B <[(a^2+x^2)^(3/2)-|x|^3]/a^2>.

The source-off energy remains -B<a>. No negative ground energy was reset,
and no physical-angle reweighting was introduced after deformation. Two
independently shifted SO(3) product grids contained 2048 and 16384 reference
frames. All frozen shape, source, stress and material controls were retained.

Both grids confirm the prospective isochoric coefficient 1/15 in <a> and
<1/a>. Extrapolated high-grid coefficients were 0.06666666666784356 and
0.06666666666636327. The full prestress-inclusive band Hessian confirms

    A_band,ij,kl = -B/(15s^3)
       [delta_ij delta_kl+delta_ik delta_jl+6delta_il delta_jk],
    G_band = -B/(15Vs),
    K_band = -4B/(9Vs),
    M_band = -8B/(15Vs),
    h_band = -4B/(3Vs).

The full physical area Hessian also agrees with its independent analytic
formula. In the combined area-plus-band-plus-R material block,

    M>0 iff Sigma s^3>4B,
    G<=h iff 15Rs+Sigma s^3>=19B,
    M<=h follows from R>=0 and Sigma s^3>4B.

These are the declared frozen-material checks. For example, dimensionless
B=V0=s=1, Sigma=8 and R=1 have energy 8, active energy -9, h=7/3,
G=31/15 and M=8/15. Hence the material speed squares are 31/35 and 8/35.
That formal block passes its material positivity/causality requirements.
The same source-zero branch still fails the independent anisotropic field
test, and no complete clock, gravity or internal-mode front is inferred
from this example.

Maximum recorded errors:

| Check family | Maximum error | Frozen tolerance |
|---|---:|---:|
| Normalized material Hessian entries | 9.080157378771325e-8 | 2e-7 |
| Normalized material gradients | 6.662337348473102e-12 | 2e-7 |
| Shape cross-grid agreement | 1.1546319456101628e-13 | 2e-11 |
| Angular-series coefficient | 6.72800704037968e-12 | 2e-7 |
| Normalized directional source Hessian | 1.714317828434794e-8 | 2e-7 |

## Source-zero failure and an exact wider proof

The source tensor of this actual anisotropic energy is

    chi(F) = F F^T <1/a>/det F,  A_ref=1.

Uniform scaling preserves chi=I, as previously derived. It does not preserve
criticality under anisotropic shape. For epsilon=.02 and
F=diag(exp(epsilon),exp(-epsilon),1), the receipt gives

    eig(chi) = [0.9608406793038494,
                1.0000533313017799,
                1.0408662819858825],

    eig(I-chi) = [-0.04086628198588249,
                  -0.00005333130177986867,
                   0.03915932069615058].

All twelve frozen nonzero strains, epsilon=+/- .001,.002,.005,.01,.02,.05,
have a negative bare quadratic field direction. This is consistent with
the independent first-order result chi_max=1+2|epsilon|+O(epsilon^2).

The failure extends exactly to every nonconformal F under the declared
continuous isotropic reference-frame census. Let its positive singular
values obey lambda_max>=lambda_mid>=lambda_min. The restricted tangent
metric obeys C_t>=lambda_min^2 I, so a<=1/lambda_min and
<1/a>>lambda_min for nonconformal F. Therefore

    lambda_max(chi)
      = lambda_max^2 <1/a>/(lambda_max lambda_mid lambda_min)
      > lambda_max/lambda_mid >= 1.

Uniform scale times rotation gives equality. No choice of new dipole matrix,
shape-dependent G, identity reference, occupation or angular measure was
made to avoid this consequence.

The failed requirement concerns the b=0 branch at a held anisotropic shape.
It is not a proof against every nonzero stationary branch, every physical
surface action or UNT. If a different branch is investigated, this original
receipt and its scientific failure must remain intact.

## Exact next action and limits of the possible alternative

For a fixed F the exact finite-source polarization is

    P = (A_ref/detF) F F^T b
        <1/(sqrt(a^2+x^2)+x)>.

Along the largest left singular axis, define

    f(x) = (A_ref lambda_max^2/detF)
           <1/(sqrt(a^2+x^2)+x)>.

For this failed source-zero branch f(0)>1, f decreases strictly, and
f(infinity)=0. Thus there is a unique positive held-shape stationary root
f(x*)=1. At that root the bare-plus-band field Hessian, with shape held
fixed, has transverse factors 1-lambda_i^2/lambda_max^2 and positive
longitudinal factor -b partial_b f. Degenerate largest singular values give
flat transverse directions. This is a new analytic branch observation,
not a numerical extension of the frozen worker or a success reinterpretation.

The exact next action is to freeze a separate nonzero-branch gate that
retains the same action and solves this stationary root, then tests the
joint material-plus-source Schur/Hessian rather than just the held-shape
field block. Actual acceleration/clock compatibility, formation, full
kinetic positivity, boundaries and ordinary observations must remain owned.
A spontaneously selected acceleration is not automatically the galaxy
solution or a homogeneous cosmology. No new branch worker is active here.

The independently counted tension normalization, native 2D carrier and
source port, absolute-energy formation, finite-gap crossover, constant
large-field residual, internal q.a kinetic bound and clock/gravity closure
remain unresolved. This result does not close lensing, growth, mergers,
early-universe/CMB, thermal-origin, fair joint-comparison or URM work.
