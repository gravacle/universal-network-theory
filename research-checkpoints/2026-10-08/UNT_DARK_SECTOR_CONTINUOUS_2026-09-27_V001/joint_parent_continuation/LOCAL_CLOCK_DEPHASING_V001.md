# Local force settling does not require individual modes to damp

2026-10-05 UTC. Analytical extension of COMMON_FILTER_CLOCK_EVOLUTION_V001.
Root and an internal reviewer verified the common-filter result. This
corrects the possible inference that undamped Fourier ringing precludes
all local settling; it does not change the saved single-mode solution.

## Exact linear probe

Use an infinite flat domain, a regular held Gaussian ordinary source of
mass M and width sigma, compatible initial zero clock response, and fixed
ell,beta>0. The common-filter frequency is

    omega(k)=c k sqrt{ beta[(1+ell^2 k^2)^2-1]
                          /[2(1+ell^2 k^2)^2+3beta] }.

For fixed r the extra force is

    g_extra(r,t)=(2GM/pi) integral_0^infinity dk
      k j1(kr) exp(-sigma^2 k^2/2) [1-cos(omega t)]
      /[ell^2 k^2(ell^2 k^2+2)].

The static-minus-time-dependent integral has low-k amplitude
r/(6ell^2)+O(k^2), and omega=Dwave k^2+O(k^4), where
Dwave=c ell sqrt[2beta/(2+3beta)]. There are no other stationary points;
the Gaussian controls the UV endpoint. Endpoint stationary phase gives

    g_static(r)-g(r,t)
      =GM r/[6ell^2 sqrt(2pi Dwave t)]+O(t^(-3/2)).

This is a fixed-r late-time asymptotic at fixed positive parameters;
roughly sqrt(Dwave t) must exceed r, sigma and ell. Every mode rings,
but a localized superposition settles by dispersive dephasing. No extra
phenomenological friction was needed for this particular observable.

## Scope

Not thermalization, monotonic relaxation at all times, irreversible loss,
or a proof of nonlinear galaxy formation. Finite reflecting boxes recur.
The critical linear static field has extra force approaching GM/(4ell^2)
at infinity; it is not a globally isolated finite-energy static solution.
The affected region continues spreading. Uniform late-time weak-field
validity is not proved; low-k response can leave the linear regime.
The held source's support/work and physical global clock remain required.

The independent reviewer also verified the constant unfiltered trace
extension: omega=c sqrt[beta/(2+3beta)] ell k^2 sqrt(2+ell^2 k^2)
is strictly increasing and has the SAME low-k Dwave. Its Gaussian endpoint
therefore has the same leading t^(-1/2) coefficient and qualifications.
This is analytically checked, not numerically tested. Neither version
supplies a homogeneous matter abundance merely by this local force result.
