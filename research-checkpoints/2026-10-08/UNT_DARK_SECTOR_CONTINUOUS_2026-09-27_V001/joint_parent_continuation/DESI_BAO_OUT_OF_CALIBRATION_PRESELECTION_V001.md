# Prospective out-of-calibration expansion-shape test

2026-09-29. Root selection before computing any new distance prediction or
score. This is a next observational calculation, not a completed test. It
does not replace the joint galaxy, physical acoustic-scale or full CMB tests.

## Fixed candidate and data version

Carry the newly reviewed balanced hard-limit scalar parent into a late-time
flat expansion-shape test. Its ideal background has
E(z)=H(z)/H0=sqrt[Omega_m(1+z)^3+Omega_Lambda], with the SAME18 inherited
reference alternatives, Omega_m=Omega_b+Omega_exc and Omega_Lambda=1-Omega_m.
No shared coefficient is refitted to the new expansion observations. The
four soft quadratures give identical expansion shapes for each reference;
they are not72 independent cosmological predictions.

Use the COMPLETE13-value DESI DR2 BAO distance vector and its supplied
covariance corresponding to the March2025 BAO release, paper2503.14738v3.
The public release/version has a compact reproducible likelihood and covers
both transverse/radial and isotropic distance measurements. Do not choose
bins by residual, switch to another release after scoring or combine it
as independent of its overlapping2026 follow-up. All observations, labels,
redshifts and covariance entries must be authenticated to primary sources.
If the expected public vector differs, reconcile the census before scoring.

Primary entry points already located:
https://arxiv.org/html/2503.14738v3
https://data.desi.lbl.gov/doc/papers/dr2/
https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/
https://github.com/CobayaSampler/bao_data

## Exposure and independence

The existing galaxy curves and Pantheon+/BBN-derived calibration references
were already exposed. Root's data-location search additionally displayed the
DR2 Ly-alpha z=2.33 distance means/errors, a qualitative consistency summary,
and existence of the2026 follow-up. No prediction or score against the new
vector has been computed. The parent and its calibration were frozen before
this search. This is therefore OUT-OF-CALIBRATION data, not a fully blinded
preregistration or proof of complete statistical independence. No publication
or optimal-model-selection claim follows. Preserve this exposure history.

## Forward map and transparent nuisance freedom

For each inherited shape compute

    dM(z)=integral_0^z dz'/E(z'),  dH(z)=1/E(z),
    dV(z)=[z*dM(z)^2*dH(z)]^(1/3).

The predicted vector is A times the appropriate dM,dH or dV, where the ONE
common positive scale A=c/(H0*r_d) is profiled analytically over all13 entries.
This is an explicitly counted nuisance parameter: the network acoustic ruler
r_d has not been calculated. Profiling it tests the expansion SHAPE without
claiming the absolute ruler was predicted. It is not an independent function
of redshift or a correction to the galaxy force.

With vector d, observed y and supplied covariance C, use
A=max(0,d^T C^-1 y/(d^T C^-1 d)); retain an active boundary if encountered.
Report the complete residual vector and quadratic form (y-Ad)^T C^-1(y-Ad),
the profiled A, individual pair covariance and derived AP ratios where both
distances exist. The primary score uses the original vector/covariance, NOT
ratios with a silently Gaussianized distribution.

Also compute a flat pressureless-plus-vacuum comparator with BOTH Omega_m
in[0,1] and A free. Keep endpoints, all sampled local minima and a converged
one-dimensional profile; no hidden cosmological concentration or CMB prior.
At any identical Omega_m and A, this comparator and the declared ideal
network limit MUST predict identical distances: test that identity. A lower
best-fit comparator score is not a predictive defeat given its extra locally
adjusted shape freedom. Preserve all18 fixed-reference results, not only the
closest one. Their discrete range is not a posterior or uncertainty integral.

No success/failure threshold, likelihood-ratio significance, AIC/BIC or joint
evidence claim is adopted from these descriptive scores. Radiation omission
over the stated low-redshift interval and the BAO template assumptions must
be quantified/disclosed before assigning a precision interpretation. Ordinary
photon/ruler physics is conditionally retained; the continuous-network-CMB
hypothesis is a DIFFERENT construct and cannot borrow this forward map.

## Implementation and review before scoring

Use independent fixed-order distance quadratures and synthetic recovery/
covariance checks, then freeze the exact source, data and scoring protocol.
Do not run an observational score before those checks and a separate review.
This is a small local calculation, with root as the sole numerical producer.
An output-based code/tolerance change is an explicitly preserved technical
revision; a change to the physical candidate is a new construct.
