# Testing the kinetic restriction without a standard-model q0 target

2026-10-04. Pre-execution analytic/data protocol. This is a new consequence
of the shared action, not a rerun of the previous DESI expansion fit. Data
are exposed development evidence. The calculation removes reliance on the
LCDM-derived q0 used in the earlier kinetic example.

The normalized finite constant-shear/rescaling family obeys

    lambda_eff = 1/3 + sum_i[(1+w_i) Omega_i]/(q+1).

Use the same physical metric, measured G_N, conserved ordinary sources and
regular principal-operator window as the derivation. Write X=H^2 and
B=(8pi G_N/3)rho_ordinary. Conservation gives

    lambda_eff = 1/3 + (2/3) B'(z)/X'(z).

Necessary positive scalar kinetic sign has two regular branches:

    lambda_eff>1:    0<X'<B',
    lambda_eff<1/3:  X'<0<B'.

Consequently every regular interval obeys

    H2^2-H1^2 < 100^2 {omega_b[(1+z2)^3-(1+z1)^3]
                       +omega_r[(1+z2)^4-(1+z1)^4]}.

H is in km/s/Mpc. This is necessary, not sufficient, stability. A smooth
transition between the two regular branches must encounter a ghost,
degeneracy, or leave the assumed constitutive window. A proposed separate
constraint/cutoff completion would require its own analysis; the displayed
inequality is not a theorem for every possible network theory.

For the increasing branch throughout [0,z2], H1>=H0. Radial BAO gives
R=H2/H1=Y1/Y2, Y=D_H/r_d, assuming one conserved common acoustic ruler and
the stated metric distance dictionary. Therefore

    R <= Rmax = sqrt(1+D/h0^2),
    D=omega_b Delta(1+z)^3+omega_r Delta(1+z)^4, h0=H0/100.

The unknown ruler cancels. A positive *H* alone does not imply H1>=H0; the
increasing-branch premise is essential. The decreasing branch instead has
R<=1. Both branches can be tested without a fitted interpolation of H(z).

For fixed Rmax the constraint is linear in the measured Y vector:

    Y1-Rmax Y2 <= 0,
    Q_bound = max(Y1-Rmax Y2,0)^2 /
              [C11+Rmax^2 C22-2Rmax C12].

This is the squared Mahalanobis distance to one half-space, a lower bound
on the full released Gaussian BAO quadratic mismatch of ANY model satisfying
it. It is not a new chi-square fit, a posterior probability or a sigma claim.
It remains valid with correlations to omitted measurements because the
linear-combination covariance is the marginal covariance. Do not sum bounds
from overlapping pairs.

Select the lowest and highest radial redshifts (.51,2.33; original indices
2,11) as the primary pair by fixed endpoint rule. Report all fifteen radial
pairs as diagnostics, not a post-selected headline. Read the exact pinned
13-vector/covariance, preserving the final DH/DM ordering. The observations
retain the survey's template, reconstruction and covariance assumptions;
they are not raw-photon, assumption-free measurements.
[Primary DESI release paper](https://arxiv.org/html/2503.14738v3).

Use omega_b=.02166 and .02235, inherited BBN-conditional benchmarks, and
omega_r in {0,4.18e-5}; the latter is an explicit illustrative standard
relativistic inventory, not a newly inferred neutrino mass budget. Report
fixed H0={60,70,73.6,80}. These are exposed sensitivity values, not a newly
adopted H0 prior. Also report the central required minimum omega_b at each
H0, central H0 ceiling, and necessary r_d floor from the integrated bound:

    H0_max=100 sqrt[D/(R^2-1)],
    omega_b_min=[h0^2(R^2-1)-omega_r Delta(1+z)^4]/Delta(1+z)^3,
    r_d_min=(c/100) sqrt[(1/Y2^2-1/Y1^2)/D].

The last quantities are transformed central values, not confidence bounds.
They retain their density/calibration assumptions. No uncertainty is fitted
away; no standard q0, DE density, independently selected r_d or halo is used.
All cases are retained. No BAO data download, solver, new fit or installation.

Before reporting target scores check input hashes, labels, covariance symmetry
and Cholesky recovery (2e-12 relative); verify the half-space projection against
direct Mahalanobis evaluation (1e-10 scaled) and arbitrary common-ruler
rescalings of synthetic H pairs (1e-12 relative). Independently check the
derivative/integral on synthetic H^2=H0^2+s*B_increment with s=.2,.8,1.2:
the first two satisfy the increasing-branch bound and the last violates it.
Check exact synthetic endpoint arithmetic at 1e-12 relative. Preserve failed
controls before scoring. Independent algebra review accepted the identity,
the monotonicity qualification and the endpoint covariance before execution.
