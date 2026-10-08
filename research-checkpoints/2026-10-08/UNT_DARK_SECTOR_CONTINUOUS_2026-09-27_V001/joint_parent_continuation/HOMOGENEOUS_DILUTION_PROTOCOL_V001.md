# Same-action homogeneous dilution: prospective census V001

2026-09-29. An additive zero-source orbit calculation, not a new preparation,
fit, ODE, FLRW solution or physical clock calibration. The parent owns freeze,
execution and publication. The worker only prints JSON in `freeze` or `run`
mode; no older file is altered.

## Fixed state and interpretation

Keep ALL 36 original returned-action templates, including their two cutoffs,
two ramp durations, three amplitudes and three old numerical resolutions.
Read `mode_data.action` from authenticated
`PREPARED_ACTION_RETURN_V001_RESULTS.json`; obtain the identical spectral
nodes/weights from its common-history ancestor. Separately keep ALL six fine
high-gap pulse states in `HIGH_GAP_PULSE_V001_RESULTS.json`: its
`fine_end_state` already contains action, delta, weights, energy, pressure and
frequency, with 128 soft nodes plus its one hard atom. Do not recompute a pulse
or replace its saved action by harmonic action. The soft-only and soft-plus-hard
parents have different Kb and matching constants and remain separately labeled.

At the six fixed inverse scale factors

    A=a^-1 in {1,2,4,11,101,1101},  I_j(A)=A^3 I_j(1),

use the existing common-current adiabatic action invariant. A=1101 is only a
recombination-like reference expansion factor, not a claim of a derived
observed-redshift/time/native-volume identification. The outputs are intrinsic
excitation E and P; the unchanged DeltaU contributes +C DeltaU to density and
-C DeltaU to pressure, not to these excitation ratios. No vacuum rematching,
new abundance or thermal state is introduced.

For the scalar pulse, homogeneous isotropic stress is a CONDITIONAL ensemble
or triad readout of its retained orbit energies/actions. The calculation does
not prove that its actual collinear coherent state isotropized, that its clock
is geodesic, or that its phase average can replace the full metric constraints.
It uses neither a spatial sound interpretation nor the scalar response as an
isotropic-vector susceptibility.

## Exact zero-source kernel

In the inherited m=kappa=u4=1 units,

    U=delta^2 y^2/2+y^4/4,  e=delta^2 b^2/2+b^4/4,
    q(theta)=delta^2+b^2(1+sin^2 theta)/2,
    J=int_0^(pi/2) q^-1/2 dtheta,
    I=(2/pi)b^2 int_0^(pi/2) cos^2 theta sqrt(q) dtheta,
    omega=pi/(2J),
    P=<y^4>/4,  <y^n>=b^n int sin^n theta/sqrt(q) / J.

I grows strictly with b. For a positive target action use the independent
analytic upper bracket

    b_hi=min[sqrt(2I/delta), (2sqrt(2) I)^(1/3)],

because respectively I>=delta b^2/2 and I>=b^3/(2sqrt(2)). Use 72 bisections
and independently evaluate 64- and 128-point Gauss angle rules. The kernel
follows the already qualified `prepared_action_return_v001.py`,
`prepared_compression_v001.py`, and `high_gap_pulse_v001.py`; these sources
are frozen as ancestry, not imported to launch their producers.

For the conditional clock ledger also compute

    K=int (1+sin^2 theta) q^-3/2 dtheta,
    e_II=omega^2 K/[2J(delta^2+b^2)],
    zeta=I e_II/omega,  0<=zeta<=1/3.

Then dE/dln A=3(E+P), with E=sum w e and P=sum w P_j. The common-compression
coefficient is sum w I^2 e_II / sum w I omega; it is not independently proved
to be a microscopic propagation speed. Report E(A)/[E(1) A^3] to expose
departures from dust dilution without fitting a power law. All input states,
including all old resolutions, remain in the result.

Physical angular frequencies would be omega_j/tau_star. The result reports
max_j(1/omega_j), max_j(6pi/omega_j), and max_j(3 zeta_j/omega_j).
Multiplication by H tau_star gives respectively H/omega_phys, fractional
action change during one period, and |omega_dot_phys|/omega_phys^2. These must
be small for every mode claimed to be rapidly averaged; no physical H(a),
tau_star or all-modes-fast assertion is supplied. H variation and the full
metric/clock evolution are additional domain conditions, not numerical gates.

## Prospective numerical controls, unchanged by outcomes

Check all modes for the target action, bracket, virial e=delta^2<y^2>+3P,
I omega=e+P, positive frequency/energy, 0<=P/e<=1/3, and 0<=zeta<=1/3.
Both angle rules must agree on energy, frequency and pressure, with pressure
differences scaled by energy to avoid imposing spurious relative accuracy on
nearly harmonic pressure. At A=1 compare every modal energy, pressure and
frequency with its saved input; original saved pressure may use I omega-e,
so its comparison is also scaled by energy.

All these qualified-orbit/inherited comparisons use normalized tolerance
2e-8, retained from the original action-return controls. Exact algebra and
synthetic scaling use 2e-12. No pressure value constitutes scientific success
or failure. Check the rigorous finite-band energy envelope

    E(1) A^3 <= E(A) <= E(1) A^4,

and conservation identity above with a separate central difference in ln A at
fixed steps 1e-3 and 5e-4 and Richardson extrapolation, tolerance 2e-7. This
derivative control uses only an additional two pairs of amplitude/action
inversions at each A, not a new physical state or trajectory.

Synthetic controls are fixed before execution: delta=.1,1,128 with b=0,.01,1,100
for inversion, plus exactly harmonic and exactly quartic kernels to check
their I-to-e scaling, pressure and frequency identities. The synthetic quartic
action constant is independently evaluated using Euler Gamma functions.
These synthetic limits do not add modes to either physical input spectrum.

## Compact evidence and resource scope

One state and scale factor at a time, at most129 modes times128 angle nodes.
Retain all252 state/scale rows, every modal frequency, all aggregate E/P/ratio,
clock coefficients, 64/128 differences, check maxima/counts and EVERY failed
check identifier. Full inherited action arrays remain authenticated inputs;
no modal frequency or state is dropped for output size. The output-size target
is 2MiB; excess is reported without truncation. Keep all24 original-resolution
comparisons at all six factors as descriptive evidence (144 comparisons), not
a new source-selection gate. Pulse coarse histories are not rerun here.

Authentication checks both payload wrappers and their recursive frozen members;
freeze includes this source/protocol, the exact action-interface and kernel
sources and every actual input dependency. No new packages or external data,
no numerical worker outside the parent's sequential queue, and no arbitrary
wall deadline or checkpoint design are needed for this small postprocess.
