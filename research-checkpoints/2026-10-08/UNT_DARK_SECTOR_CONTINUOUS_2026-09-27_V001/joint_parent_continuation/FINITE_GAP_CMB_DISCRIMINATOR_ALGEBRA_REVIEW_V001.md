# Same-state CMB interface: independent algebra review V001

2026-09-29. Read-only mathematical review; no transfer solver, spectrum,
likelihood, numerical producer or photon-origin calculation was run.

Reviewed `FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md`, SHA256
`b93c98db76147725badf8a1a3cc5256be0cd44f3132ae4d782eaf0015920a403`,
together with the complete `ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md` and
the declared common action in `MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md`.

The Q=0 scalar-sector algebra is accepted. Specifically, rho_dot=-3H(rho+p),
p_dot=cI2 rho_dot and w=p/rho give

    w'=-3 Hcal(1+w)(cI2-w).

With theta_H=k^2 V/a, conformal differentiation of the reviewed cosmic-time
current/Euler equations gives exactly

    delta_H'=-(1+w)(theta_H-3Psi')-3Hcal(cI2-w)delta_H,
    theta_H'=-Hcal(1-3cI2)theta_H
                          +k^2[Phi+cI2 delta_H/(1+w)].

Thus there is no omitted w' term: it has already combined with the Euler
friction coefficient. Pressure and sound speed belong to the same retained
state. At nonzero Q the conserved signed polarization density produces
nonadiabatic pressure, so the Q=0 fluid transfer cannot be reused unchanged.

The stated free-streaming fraction follows algebraically from ordinary
massless-neutrino density and an additional fluid-radiation coefficient.
It is explicitly restricted to the post-annihilation, pre-transition thermal
regime. It does not identify the changing hard population with added
free-streaming neutrinos, or replace its finite-epoch density by a constant
Delta template. The hard sound-horizon integrand is also dimensionally
correct with cI2 dimensionless and physical H.

One domain qualification should remain explicit in any numerical continuation:
the rapid-mode/phase-averaging validity is independent of the formal background
continuation I proportional to a^-3. In the formal quartic radiation limit,
omega is proportional to a^-1 while H is proportional to a^-2, so taking an
integral to a=0 is not automatically inside the oscillator averaging regime.
One needs a valid early endpoint and qualified tail or a separately declared
fundamental macroscopic-fluid assumption. Physical clock/inertia calibration
has not been established by the present algebra. This is a scope addition,
not a sign or normalization correction to the displayed equations.

Ordinary radiation, neutrino stress, recombination and initial mode data are
separate retained inputs. This review establishes neither their empirical
likelihood nor the cited papers' numerical bounds; it verifies the local
same-action equations and the explicit distinction from photon production.
