# Finite-gap shared-state screen, prospectively fixed V001

2026-09-29. One small stdout-only worker; no galaxy evolution, fit, new pulse,
external data, remote dispatch or previous result modification.

## Named conditional construction

Use the scalar alpha=1 macroscopic candidate, soft ground modes and one occupied
hard atom of weight beta=.005. This is a newly specified macroscopic state,
not an actual finite-R common-pulse output or an asserted native derivation.
Retain all four saved soft quadratures and all 18 inherited late-time reference
alternatives. Retain exposed a0=1.2e-10 m/s2 and the same conditional
radiation-omitted present-day reference normalization. No preferred reference
is selected from the outcomes.

Prospectively fix R={32,128,512,2048,8192}, giving 360 branches. At each branch
gstar=a0/[16 Kb/(3 pi)], Ereq=3 Kb Omega_exc (c H0)^2/(2 gstar^2), and
eH=Ereq/beta. The hard action is calculated from this finite-R energy, not
held fixed while changing R. This labels distinct globally calibrated designs.
The formal a0 coefficient is an exposed calibration, not a certificate that
its finite-field asymptotic window applies in a galaxy.

Solve the exact finite-R vacuum condition

    Qsoft(S)+beta*(R^2 ys^2/2+3 ys^4/4)=Ereq Omega_Lambda/Omega_exc,
    R^2 ys+ys^3=R S.

Use the old S_infinity as a starting lower value, monotone upper doubling,
and 80 bisections. The old harmonic hard upper bracket is not valid at finite
R. The same cubic hyperbolic-sine solution is independently checked against
80 root bisections. Include the hard elastic term in the contact/energy ledger.
No independently adjustable vacuum offset or local abundance is introduced.

## Orbit and static readouts

Use the endpoint-safe positive angular quadratures of the reviewed
central_static_response_v001.py, reimplemented here without executing any
ancestral producer. GL128 is primary; GL64 and Simpson1024 are comparisons.
Positive pressure is <y^4>/4, never a cancellation of I*omega minus e.
The stable turning amplitude is b^2=4e/(R^2+sqrt(R^4+4e)).

For the occupied hard mode compute

    cI2=I eII/omega, q=3(e+p)/(R^4+4e), K0=beta q,
    J=beta*(omega^2/eII+3 I omega),
    ell=(c^2/gstar)*sqrt(K0/J),
    K0/J=3 cI2/[(R^4+4e)(1+3cI2)].

The independent cosmic normalization identity is
(H0 ell/c)^2=2(beta/Kb)(e/R^4)cI2 /
[Omega_exc(1+4e/R^4)(1+3cI2)]. Empty soft modes contribute no occupied J.
Report ell in parsecs, K0/Kb, J and cI2. Ell is a local static Helmholtz scale,
not a fitted or predicted halo radius, equilibration time or stability proof.
The linear density response requires |Phi| much less than cI2; report that
potential scale. Source-frequency corrections begin at quadratic acceleration
and must return in a nonlinear galaxy calculation.

Conserve the same action to A=1101 by exact monotone inversion of
f(r_A)=A^3 f(r_1), with r=b^2/R^2 and the known bound r_A<=2 A^3 f(r_1).
Also report A=1. This epoch is an already exposed diagnostic, not a new
observational selection. Report pressure/energy, the ratio to calibrated dust
energy Ereq A^3, and present deceleration change 1.5 Omega_exc p/e. Do not
label any pressure, length or radiation ratio an observational pass/fail.

## Controls, custody and limits

Freeze source/protocol, inherited 72-branch result and its recursive frozen
lineage, the reviewed BVP and prior exact static formulas before execution.
Algebra, cubic, root and reconstruction tolerance: 2e-11 normalized by the
stated positive quantity. Zero/contact cancellations use max(1, contributions).
Orbit comparisons use 2e-8 relative to positive action, frequency, pressure,
curvature or mean square. At exactly empty action pressure is zero and
eII=3/(4 R^2); harmonic and pure-quartic analytic controls remain separate.
All branches and all control failures remain in the output.

The worker writes no files and uses one numerical thread. It emits a lossless
zlib/base64 transport with raw canonical JSON and payload SHA-256 identities;
root publishes the returned bytes with apply_patch. Resource measurements
cover self RSS and elapsed worker time, not a hard whole-job cap. A small
interrupted worker may be rerun; no long-job checkpoint architecture is needed.
Independent review must inspect saved output without repeating the science.
