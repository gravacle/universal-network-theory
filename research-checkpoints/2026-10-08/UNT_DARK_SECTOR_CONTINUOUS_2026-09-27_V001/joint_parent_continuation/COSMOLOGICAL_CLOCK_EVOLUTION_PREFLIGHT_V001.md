# Independent preflight: finite-band compensated-clock evolution

2026-09-29. Complete source/protocol read plus independent algebra; no module
import, producer execution, ODE solve or outcome inspection by this reviewer.

Accepted reviewed identities:

* cosmological_clock_evolution_v001.py:
  `95f91f63ff15a55e648a2b9dc0a09f50b454dc7ffd61390489c3915f97d8f705`.
* COSMOLOGICAL_CLOCK_EVOLUTION_PROTOCOL_V001.md:
  `66966161b00f0f919bc1d3aac726e965e646797ac337970d3aca4383bcca1ac6`.

## Physics and normalization

The physical-time and logarithmic-scale-factor generators follow from the
retained clock equations. With p=k/a, u=pv and S=sum w delta x,

    p(vddot+H vdot)=uddot+3H udot+(Hdot+2H^2)u.

Common inertia m=tau_star^2, z=delta*x/H0 and eta=H0*tau_star give exactly
the displayed soft frequencies delta/eta and source u'+Hbar*u. The driving
density coefficient is rho/(C H0^2)=1.5Kb Omegaexc a^-3. Ordinary pressureless
baryons enter H and Hdot, not this hard-density coefficient. All four owned
quadratures and three illustrative eta values remain; eta is not determined
by the acceleration calibration.

For the compensated Newtonian branch Phi=Psi=V=0, the code's

    Q=sum w z+beta Hbar(u+u_N)

correctly reconstructs Pcal=C H0 Q and hard/polarization contrasts
plus/minus (k/H0)*2a^2 Q/(3Kb Omegaexc). The lapse, acceleration and clock
phase factors also check. The two (u,u_N) initial columns with zero soft
data are a defined two-dimensional initial subspace, not the full state
transition matrix or evidence of actual preparation. Their unit amplitudes
are normalized linear responses; physical tilt, lapse and density need
their own small overall perturbation amplitude.

The exact independent generator identity is

    Q_N+2Q=1.5Kb Omegaexc a^-3 u/Hbar.

Its implementation checks algebra on the generator. The separately named
compensated_density_reconstruction is an identity by construction, not an
independent solution or verification of Einstein constraints. Those physical
constraints were derived in the bound analytical interface notes.

## Algorithms and the pre-outcome cap correction

The Dormand-Prince 5(4) tableau, embedded estimate, rejection logic, endpoint
handling and per-coordinate error scales are consistent. The independent
RK4 transformation Vc=a*u gives exactly the separately written generator;
its initial data and inverse transform include the derivative term.
The exact oscillator and matter-power-law controls have the correct signs.
The matter tilt roots (-3 +/- sqrt(1+24F))/4 use the actual hard fraction
F=Omegaexc/(Omegab+Omegaexc), not the single-component shortcut.

Before any outcomes, the root identified that the phase cap must include
the collective mode rather than only the largest bare soft frequency.
The corrected code uses

    Omega_bound^2/H0^2=[max(delta^2)+sum w delta^2/beta]/eta^2.

Independent check: for a frozen undamped above-band stable squared frequency
y, beta+M/y=sum w omega_j^2/(y-omega_j^2), M>=0. The positive left side is
at least beta, and the right side is at most
sum w omega_j^2/(y-max omega_j^2). This proves the stated upper bound.
For M=0 the same result is the Rayleigh bound on the positive diagonal-plus-
rank-one stiffness. Both numerical methods now use this bound prospectively.
It is not itself an expanding-background global error bound; adaptive
refinement, the logarithmic step cap and cross-method comparisons remain.

All state coordinates and both basis columns enter the tighter-repeat and
independent comparisons, each with its own declared full-sample scale.
All fixed milestones use the same math.log construction/lookup. The finite
state census, source/read-only helper authentication, snapshot comparison
and stdout-only publication are consistent. No outcome-based parameter,
growth cutoff or tolerance selection is present.

## Interpretation boundary

The dust-plus-vacuum background omits radiation deliberately. The initial
a=.001 is therefore a synthetic epoch, not a qualified recombination model.
The early soft modes are not assumed quasistatic. Large, small, sign-changing
or decaying clock response is an output, not a scientific pass condition.
Numerical pass means the specified linear initial-value problem meets its
prospective controls; it does not certify the adopted hard-state preparation,
the native clock dictionary, nonlinear stability or an observed cosmology.

No remaining source/protocol blocker was found at the identities above.
