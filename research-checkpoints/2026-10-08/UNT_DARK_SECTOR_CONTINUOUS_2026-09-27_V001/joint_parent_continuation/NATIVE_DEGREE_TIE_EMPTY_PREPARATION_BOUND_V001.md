# Empty-edge preparation is not the degree-tie response ground

2026-09-30. Root-authored exact analytic note, pending independent review.
No numerical calculation, new preparation rule or alteration of the parent.
This explicitly tests one proposed preparation, not every admissible native
initial condition and not a full UNT formation law.

## Fixed family and explicitly conditional initial state

Use the complete first-degree-tie parent of the reviewed coupling and
opposite-layer response notes, at N>=2 and fixed U,Omega>0:

    H=C_N+2U(C_L+C_R)-h sum_e X_e,   h=Omega/N.

Records are held uniform, carriers blank and ports off, as in those notes.
In addition choose the initial edge register to be the empty graph |empty>.
Blank carriers alone do not imply empty edges; this is a separate explicit
preparation hypothesis. It does not account for making the held record state.
Let |0> be the unique complete-parent ground with energy E0.

The ground has the static response established in the other notes. To use
that response for this preparation, one must establish formation or show
the relevant response remains valid in the actually evolving state. Merely
waiting under this fixed closed H cannot establish ground preparation.

## Exact initial mean and variance

The empty graph has no degree violation. Each of the N^2 flips produces a
distinct orthogonal one-edge graph, so

    (H-C_N)|empty> = -h sum_e |one edge e>,
    <H>_empty = C_N,
    Var_empty(H) = h^2 N^2 = Omega^2.                 (1)

This uses the complete Hamiltonian, not a projected energy estimate. Neither
the mean nor the variance changes under exp(-iHt/hbar). The result is
independent of the unknown absolute value of C_N, but that constant has not
been deleted from physical energy or uniform clock/volume work.

## A complete-parent ground energy separation

The matching-subspace trial ground gives the Rayleigh upper bound

    E0 <= C_N-h lambda0,

where lambda0 is the Perron eigenvalue of the projected singlet adjacency
with a_m=(N-m)sqrt(m+1). This is a valid full-parent trial vector, whether
or not P is invariant. The reviewed two-level trial bound gives

    lambda0 >= N^(3/2)/(2 sqrt(2)),
    Delta:=C_N-E0 >= Omega sqrt(N)/(2 sqrt(2)) > 0.   (2)

An energy-only comparison already excludes exact closed relaxation to |0>.
The variance supplies a stronger preparation constraint without calculating
any spectrum or waiting for a long trajectory.

## Uniform ground-population bound

Let p=|<0|empty>|^2. If p=1 the variance would be zero, contrary to (1).
The spectral distribution of H in |empty> has mean C_N. Conditional on the
complement of its ground atom, its mean must be

    E_rest = C_N + p Delta/(1-p).

The conditional variance in that complement is nonnegative. Decomposing
the total variance by these two populations therefore gives

    Omega^2 >= p Delta^2 +(1-p)[p Delta/(1-p)]^2
            = p Delta^2/(1-p),
    p <= Omega^2/(Omega^2+Delta^2) <= 8/(N+8).        (3)

For p=0 the inequality holds directly. Under the exact fixed-H unitary,

    |<0|exp(-iHt/hbar)|empty>|^2 = p

at every time, not just on average. Thus this ground fidelity is bounded
above by a quantity tending to zero with increasing N. Waiting longer or
dephasing in the energy eigenbasis does not prepare the response ground.
This says nothing comparable about individual local observables becoming
approximately stationary or about a non-ground response kernel.

## Any cooling claim must own the energy destination

For a process that starts with the preparation above and ends exactly in
the same-H ground, the edge system's mean energy drops by Delta. If no
external work is done, other explicitly modeled degrees of freedom must
gain that energy (including final interaction/boundary energy where relevant).
The required transfer is at least the lower bound in (2). This is not a
heat-spectrum prediction, a lower bound on entropy, or a claim that the
energy must appear as photons. For driven formation, work must instead be
included in the balance; changing H in time is not the ports-off evolution
used in (1)--(3).

An environment, growing record register, carrier population or other native
port may in principle change the preparation. Such a model must specify
its dynamics, incoming state, energy/work accounting and subsequent source
response. Inserting an unexplained cooling/reset map would just replace the
missing formation assumption. This note neither prohibits an in-scope
formation construction nor authorizes changing the frozen parent silently.

## Scientific decision

Keep the positive finite-N opposite-layer response as a conditional
ground-state property. For an empty-edge, closed held-parent hypothesis,
the required stationary ground is not an autonomous late-time result; the
exact bound (3) makes that failure uniform rather than a finite-time numerical
observation. It is not a no-go theorem for all network cosmologies, other
initial states, local equilibration, or a source response of the actual
nonstationary state. It does not select physical length, volume or density,
and it does not establish a galaxy law or cosmic negative pressure.

The next formation question is therefore explicit: evaluate the response
of the actually prepared state, or supply a native energy-accounted formation
mechanism that changes its spectral populations. A new projected-ground
histogram or an arbitrary evolution age would answer neither question.

Ancestry: NATIVE_DEGREE_TIE_PROJECTED_STATIC_BOUND_V001.md equations (3),(9),
SHA 57530e06b99ad9608dc8afde899804884947402eafb7d7860813b875ac1887de;
NATIVE_DEGREE_TIE_FULL_PARENT_COUPLING_V001.md,
SHA def8c842be9bd1bbd21ae8cd0a6338160ac28d81aaab2851371b519b75205390;
NATIVE_DEGREE_TIE_FULL_PARENT_ODD_RESPONSE_V001.md,
SHA ac17bd126aa2f05032b674180b36caa72faa6164879aa3ab8b9960e57b86a815.
