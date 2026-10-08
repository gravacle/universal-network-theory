# Independent review: native temporal kernel and record addition

2026-09-28. Read `NATIVE_TEMPORAL_KERNEL.md` completely and compared its
held block against `TWO_BAND_ANALYTICAL_BRIDGE.md` and the resident BS
Hamiltonian. Analytical review only; no new preparation, spectrum or worker.

## Verdict

**Accepted.** The current/sum-rule signs, conserved-charge response null,
addition energies, branch-curvature discriminator and conditional Legendre
normalization are correct. The proposed second endpoint is explicitly a
new declared native restriction, not a reinterpretation of the existing
one-record qutrit or its stored formation populations.

## Independent checks

### 1. Copy current and held record phase

On one correct-content blank/occupied target, `K=X`,
`q=(I-Z)/2`, and the note's `Y` is minus the usual Pauli `Y`.
Therefore `[K,q]=-iY` and `[q,[gK,q]]=-gK`, verifying both the production
current and negative-copy-energy initial response slope. The projectors
on distinct donors commute with the target occupation, so summing the
native carrier/writer copies introduces no extra cross term. The stated
operator-norm drift bound follows by the triangle inequality.

Copies using a record as control commute with its count. With all
record-target couplings off, each local record occupation is conserved,
not only their total. Hence every local record phase twist commutes with
the held Hamiltonian; its zero static energy cost is exact in this
restriction. This says nothing comparable about a composite carrier phase,
because carrier hopping does not conserve each local carrier occupation.
Noncommuting ports must contribute their actual commutators, as retained
by the note.

### 2. Conserved-charge response versus a density ensemble

For `[H0,C]=0`, the full source evolution factors as
`U_mu=U0 exp(i C integral mu/hbar)`. Thus the exact retarded `CC` commutator
is zero for every initial state, including charge coherences, and the
closed-time-path functional depends only on the integrated source
difference. Expansion of its characteristic function gives the displayed
mean term and **positive imaginary** variance term in `-i hbar log Z`.
That variance is not a common-source retarded susceptibility.

The distinction from equilibrium compressibility is essential and correct:
an ensemble allowed to exchange charge changes its populations, whereas
the isolated conserved-count source does not. At finite temperature,
`-Omega_mumu=Var(C)/Theta`; at zero temperature the finite-sector lower
envelope is piecewise linear. Neither is an independently earned state
law for the actual coherent formation protocol.

### 3. Addition energies and the new endpoint restriction

At `q=0`, carrier-X branches have detunings `7/4,11/4`; at `q=1` they are
`5/4,9/4`. Their link gaps are respectively
`sqrt(113)/4,sqrt(185)/4` and `sqrt(89)/4,sqrt(145)/4`.
The scalar-plus-linear increment is `1-(1/2)/2=3/4`, giving exactly the
four radicals in the reviewed equation (8). Since
`H1-H0=I-n/2`, min–max bounds lie in `[1/2,1]`; nonzero link mixing makes
the displayed same-labelled-band increments strict. Bare storage cost
alone would miss the binding contribution.

For an explicitly retained second endpoint record, the diagonal energy
and linear detuning drop out of the second count difference. The remaining
term is `beta/2` times a finite second difference of
`d(x)=sqrt(x^2+4h^2)`. Its second derivative is strictly positive for
`h>0`; the lower branch therefore has negative addition curvature and the
upper has positive curvature for nonzero feedback. The shown projector
`[I-beta(2X+xZ)/d]/2` has the correct sign for this Hamiltonian.

This is a state-sensitive local discriminator. It is not by itself a
compressibility of a physical-volume continuum or a proof that the actual
formed ensemble selects one branch. An instantaneous addition retaining
the same link state costs `1-<n>/2`, whereas following an eigenbranch also
changes that state. Keeping these two work protocols separate is necessary
and is done correctly.

The original 36-dimensional join contains one record with occupations
`0,1`, even though it has two distinguishable occupied contents. It cannot
supply an `R=2` sector. The proposed explicit second endpoint and its
preparation must remain visible in any forthcoming numerical test.

### 4. Conditional phase pressure and clock normalization

For an independently established smooth convex density energy,
`P(mu)=sup_n[mu n-epsilon(n)]` gives `P'=n` and
`P''=1/epsilon''`. With the additional physical identification `mu=m0 Q`,
the existing action convention has `M^2 K=P`, hence

    rho_K=M^2(QK_Q-K)=epsilon,
    a^3 K_Q=(m0/M^2) a^3 n,
    c_s^2=P'/(mu P'')=n epsilon''/mu.

All factors and signs check. The comoving integration constant represents
the same physical charge; counting it again would duplicate a population.
An exactly linear dust energy has singular Legendre curvature and does not
generically define a smooth finite clock susceptibility. A stable nearly
pressureless regime requires a derived state/window, not just a positive
bare record gap.

The note explicitly leaves the physical volume, phase/controller reference,
kinetic/stiffness limit and complete source work unbound. In particular,
the exact held record-phase null is not bypassed by postulating a canonical
finite-register phase. No extra dark abundance or arbitrary clock function
is introduced in these analytical results.

## Constructive next use

The three adjacent native record sectors offer a small, discriminating
calculation: retain the full formed state and every populated branch, then
measure its addition lines, source work and phase readout against these
exact identities. That can supply real incremental energy and state
information. Turning it into a cosmological clock pressure still requires
the same parent's physical volume and collective phase dynamics. The
present review validates the bridge calculation, not that final mapping.
