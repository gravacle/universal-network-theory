# Prospective finite-band compensated-clock evolution

2026-09-29. Source and numerical choices fixed before outcomes. Root is the
sole producer executor. No new formation, fit, state selection or alteration
of frozen evidence.

## Owned physical question and complete inputs

Evolve the actual finite soft-memory equations of the newly declared
hard-limit averaged parent, including its hard contact beta=.005. This is
not a substitution of G/mu, the former coherent common pulse, or a complete
native-to-metric construction. The balanced/paired preparation, averaging and
common scalar sector are assumptions of the two source interface notes.

Use all four previously authenticated soft quadratures: epsilon=.001,.002
and 64,128 nodes, with their original positive weights. Old duration/time-step
duplicates are checked equal, not counted as new spectra. Use the already
exposed central reference index 0 of ORIGINAL_SPECTRUM_CALIBRATION_V001:
H0=73.6 km/s/Mpc, OmegaLambda=.666, Omegab=.03998552693761815 and
Omegaexc=.2940144730623818. Keep Omegab in Omegam=Omegab+Omegaexc. No choice
uses the clock outcome. The imported BBN normalization and old late-time
flat-reference qualifications remain inputs, not predictions.

Take common physical inertia m=tau_star^2, kappa=1, and the three illustrative
global eta=H0*tau_star values .001,.1,1. Acceleration calibration does not fix
eta. All 12 cases are mandatory. The background is deliberately dust+Lambda,
Hbar^2=Omegam*a^-3+OmegaLambda, over a=.001 to 2. Radiation is omitted: the
first scale factor is a synthetic initial epoch, not a validated recombination
history. No ordinary photon or acoustic calculation is performed.

## Equations and specified initial-data subspace

Let tbar=H0*t, p=k/a, u=p*v, z_j=delta_j*x_j/H0. With primes denoting tbar,

    u''+3Hbar*u'+[Hbar'+2Hbar^2
        -1.5Kb*Omegaexc*a^-3/beta]u
        +sum w_j(z_j'+2Hbar*z_j)/beta = 0,
    z_j''+3Hbar*z_j'+(delta_j/eta)^2*z_j
        =(delta_j/eta)^2*(u'+Hbar*u).

Kb=sum w+beta. Evolve in N=ln(a), with d=Hbar'/Hbar^2:

    u_NN=-(3+d)u_N-[d+2-1.5Kb*Omegaexc/(beta*a^3*Hbar^2)]u
          -sum w(z_N+2z)/(beta*Hbar),
    z_NN=-(3+d)z_N-(delta/(eta*Hbar))^2*z
          +(delta/(eta*Hbar))^2*Hbar*(u_N+u).

Co-evolve two columns: (u,u_N)=(1,0) and (0,1), both with every z=z_N=0
at the initial scale factor. They define a two-dimensional initial clock
subspace, NOT the full 2+2Nmode fundamental matrix. The unit amplitudes are
linear transfer normalizations, not physical unit velocities. Initial soft
quasistatics is not assumed or justified: H initially exceeds even the
largest soft frequency in these illustrative cases.

The metric is compensated: Phi=Psi=V=0. The ordinary baryon perturbations
are zero in Newtonian gauge. With Q=sum w*z+beta*Hbar*(u+u_N),

    Pcal=C*H0*Q,
    delta_H/(k/H0)=+2a^2*Q/(3Kb*Omegaexc),
    delta_pol/(k/H0)=-2a^2*Q/(3Kb*Omegaexc).

They are reconstructed, not both set independently to zero. Their direct
cancellation is labeled an algebraic reconstruction, not an independently
solved Einstein constraint. Check the exact
flux identity Q_N+2Q=1.5Kb*Omegaexc*a^-3*u/Hbar and the associated normal-current
continuity. Report ell/H0=Hbar*(u+u_N), n*(k/H0)=a*Hbar*(u+u_N), and
(H0*pi)*(k/H0)=-a*u. This retains the missing physical wave-number dependence
of lapse/density even though the tilt evolution itself is k-independent.

## Two numerical methods and prospective controls

SciPy is absent in both inspected Python runtimes. Use only existing NumPy,
single-threaded, without installation. Primary Dormand-Prince 5(4) has
rtol=2e-10, atol=2e-12; a tighter repeat has rtol=5e-11, atol=5e-13. Both cap
Delta N at .025 and each coupled-frequency-bound phase increment at .35. The adaptive
controller uses .9*error^(-1/5), clipped to [.2,5], rejecting error>1. No
wall deadline or outcome-dependent precision adjustment is introduced.

Independent fixed-step RK4 evolves Vc=a*u and Vc_N, with the same z,z_N:

    Vc_NN=-(1+d)Vc_N+1.5Kb*Omegaexc/(beta*a^3*Hbar^2)*Vc
            -a*sum w(z_N+2z)/(beta*Hbar),
    z_NN=-(3+d)z_N-(delta/(eta*Hbar))^2*z
            +(delta/(eta*Hbar))^2*Hbar*Vc_N/a.

Transform its outputs back to u=Vc/a and u_N=(Vc_N-Vc)/a. RK4 caps Delta N
at .0025 and the coupled-frequency-bound phase increment at .02; the endpoint Hbar
of each saved interval gives a conservative frequency bound. No shared
adaptive error estimator is used. Check this coordinate transformation's
RHS algebra independently at all five full-state output epochs.

The coupled frequency bound is

    Omega_bound^2/H0^2 = [max(delta_j^2)+sum w_j delta_j^2/beta]/eta^2,

not the largest bare soft frequency. For the frozen undamped zero-gravity
oscillatory sector, eliminating the conserved charge gives a z stiffness
similar to diag(omega_j^2)+a a^T/beta with a_j=sqrt(w_j)*omega_j.
The Rayleigh bound gives this expression. With a positive frozen gravitational
coefficient M, an above-band squared frequency y satisfies
beta+M/y=sum w_j omega_j^2/(y-omega_j^2), which has the same upper bound.
This does not prove a global expanding-system error estimate; the log-step
cap, adaptive control and independent solver comparisons remain necessary.

All state coordinates and both basis columns enter comparisons. Each error
is normalized by max(1, the largest absolute value of that coordinate/basis
over all saved epochs of either compared run). Retain each coordinate's
maximum error, not only the largest global value. Primary-versus-tighter
tolerance is 2e-7; independent transformed RK4 tolerance is 2e-5. These are
numerical targets, not bounds on the physical approximation. Arithmetic
identities use 2e-12, with explicit absolute-contribution scaling where
clock-flux cancellation occurs. Do not relax these after outcomes.

Before the full cases, check the Dormand-Prince table row/weight moments,
an exact two-dimensional harmonic oscillator, and the exact matter-era
physical-tilt power laws. The latter have F=Omegaexc/Omegam and roots
alpha=(-3 +/- sqrt(1+24F))/4, not the F=1 shortcut. Exact-oracle checks use
2e-7 with the same full-trajectory coordinate normalization. Also integrate
the two-dimensional slow-response reference on the actual dust+Lambda
background with all three methods. It is a descriptive comparison, not
an assumption that the finite soft modes follow it.

## Output and integrity

Preserve all 12 cases, all initial states, all modal deltas/weights, method
step/evaluation counts, all failed checks and measured resources. Outputs
are 61 logarithmically spaced scale factors plus all five fixed milestones
(.001,.01,.1,1,2). At every output retain both clock transfers and all
reconstructed physical scalars; at the milestones retain the full primary
modal state. Retain all-coordinate method-error arrays. No outputs are
selected by growth sign. All 64/128 comparisons are descriptive and retained.

Report the maximum sampled tilt and the initial normalization which would
keep that sampled tilt below the illustrative .01 display threshold. This
is only a tilt rescaling; it does not certify lapse/density perturbativity,
between-sample extrema or nonlinear evolution. Large amplification is a
scientific result, not a numerical failure or evidence of actual formation.

The stdout-only script supports freeze, run (all 12), or run-case INDEX
for the same prospectively enumerated cases. Root must retain all 12 even
if executed separately. Small cases may be rerun after interruption; no
new checkpoint infrastructure. The output target is 8MiB, flagged but never
met by deleting data. No source file is written by the worker.

The previously fully read custody helper's authenticate() alone verifies
original source/result wrappers, recursive manifests and old reference
metadata; its numerical run() is never invoked. Its pinned source, all
inherited files, the new worker/protocol and settled analytical interface
notes enter this prospective snapshot. Root saves the printed freeze before
any evolution. Runs require exact snapshot equality and return a payload
hash plus freeze hash. The unconditional hard-pair preparation and physical
averaging hypotheses are NOT authenticated by byte hashes.
