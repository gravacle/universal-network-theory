# External-field quadrupole of the linearized gradient parent

2026-10-04. Prospective arithmetic protocol. This extends the explicitly
changed candidate in GRADIENT_RESPONSE_COMPATIBILITY_V001, not the previously
failed bounded-source parent. It is NOT the full nonlinear Solar solution.

Freeze the inherited a0=1.0059833281731022e-10 m/s^2 and primary external
acceleration ge=2.32e-10 m/s^2, with fixed sensitivity values 2.16/2.48e-10.
gc=(3pi/8)a0. No galaxy or Solar refit. Use common J_delta=kappa delta^2 ell^2,
positive quartic modes and linear source; s=delta/Lambda on (0,1).
The external equilibrium t(s) satisfies t+t^3=ge/(gc s^2), and

    aT=1+t^2, aL=1+3t^2,
    KT,L(q)=1-integral_0^1 2s ds/[aT,L+q^2], q=k ell.

The Fourier Green denominator is KT+(KL-KT)u^2, u=cos(angle(k,ge)).
At fixed nonzero ge, 0<KT<KL; the longitudinal projection must be retained.
The potential convention remains deltaPhi=-Q2 R^2 P2(cos theta)/3.
After subtracting the isotropic high-k cusp +GM R/(2 ell^2),

    Q2_lin = GM/ell^3 * Cq(ge/gc),
    Cq = -1/pi integral_0^infinity q^2 dq
                 integral_-1^1 P2(u) du/[KT+(KL-KT)u^2].

The angular integral is negative, so Cq>0. Its exact expression uses
beta=(KL-KT)/KT:

    I2=(1/KT)[3/beta-(3/beta+1)atan(sqrt(beta))/sqrt(beta)].

For small beta evaluate the stable series
I2=(1/KT) sum_n>=1 (-beta)^n 4n/[(2n+1)(2n+3)], not a cancellation of
nearly equal terms. Compute KL-KT by its positive integral
integral 2s(2t^2)/[(aT+q^2)(aL+q^2)] ds, not subtraction of two KT values.
The first spectral moment of a is finite despite a~s^(-4/3). At high q,
the anisotropic correction is O(q^-4), so the Q integral converges. At fixed
nonzero ge the infrared is also finite. No raw origin Hessian is finite
before the isotropic cusp is separated.

## Numerical gates fixed before scoring

Gauss-Legendre integrate s on (0,1) and map q=x/(1-x), x in (0,1).
Primary (Ns,Nx)=(64,64),(128,128),(256,256),(128,256),(256,128).
All values positive and finite; primary B/C and each independently varied
finest pair must differ by <1e-3 relative to (256,256). If this fails, retain
an unqualified diagnostic without promoting a coefficient. No mesh retuning
or length search. Two ge sensitivities use (256,256) only after qualification.
Lengths 1/10/100 pc remain round illustrations, not fitted model parameters.

Controls: t+t^3 residual <1e-12 scaled at the saved nodes; normalized positive
spectral weights to <1e-13; analytic angular integral agrees with an independent
Gauss integral of the constant-subtracted integrand to <1e-10 relative for
beta=1e-12,1e-6,.01,.125,.5,2,10; zero-anisotropy integral exactly zero.
Check positivity of KT and KL-KT and the integrated sign. The asymptotic
check uses the SAME finite spectral quadrature: at q=1e6, q^4(KL-KT) agrees
with integral 2s(2t^2) ds to <1e-5 relative, and q^2(1-KT) with 1 to <1e-5.
This is a numerical identity control, not a continuum-tail proof.
Every case is short, single-threaded, no solver or physical fit. Save inputs,
source/protocol hashes, controls, quadrature cases and coefficients once.

## Scope and next decision

Linearizing polarization about the fixed Galactic equilibrium is distinct
from assuming the Sun's acceleration is everywhere small. ell>>rM makes
the perturbation near R~ell small, but uniform control through the central
region and the soft modes is not proved. A qualified numerical integral thus
establishes the LINEARIZED prediction only. It must not be described as
passing the Cassini test of the full theory. The formerly computed isolated
monopole bound and this linearized external quadrupole are different controlled
reductions; their combination needs nonlinear matching, not simple addition
by declaration. Formation, causal evolution, photon metric and cosmological
vacuum/charge selection remain unresolved. Removing source saturation lost
the old endpoint work relation. No previous galaxy score is inherited as a
verified finite-gradient prediction.
