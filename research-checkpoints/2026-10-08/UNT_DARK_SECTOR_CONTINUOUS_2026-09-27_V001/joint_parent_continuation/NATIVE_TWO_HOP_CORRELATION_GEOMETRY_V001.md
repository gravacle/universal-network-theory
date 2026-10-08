# A two-hop geometry test that retains native correlations

2026-10-03. Exact finite-parent derivation and prospective formed-state test.
This asks what an operational geometry must retain, not whether one coefficient
can be renamed a scale factor. No interaction, volume law or photon is added.

## Exact native signal

Use one BS slab, one carrier initially localized at u, and an arbitrary
environment density matrix. Let w differ from u on the SAME bipartition.
All native terms except the carrier hopping are position-diagonal, including
the current-square term. Hence, as an environment-operator identity,

    <w|H|u>=0,
    <w|H^2|u>=t_hop^2 M_uw,
    M_uw=sum_v n_uv n_wv,
    P_w(s)=t_hop^4 <M_uw^2> s^4/(4 hbar^4)+O(s^5).

Link flips, onsite energies and recording cannot make two carrier moves in
two Hamiltonian insertions. The two path amplitudes are added as operators
BEFORE squaring; replacing link operators by their means is not exact.
The statement retains all native terms but excludes additional carrier-moving
ports. If a nonzero initial reference clock rate is nu, theta=nu*s+O(s^2),

    K_uv=lim P_v/theta^2=t_hop^2 <n_uv>/(hbar^2 nu^2),
    L_uw=lim P_w/theta^4=t_hop^4 <M_uw^2>/(4 hbar^4 nu^4).

Every one-hop calibration used here must refer to the SAME clock, not a
silently different rate at each sender. Relocalizing the carrier is an
intervention with owned work; it is not the unperturbed trajectory.

## What a scalar hopping surrogate would have to predict

A deterministic scalar hopping Hamiltonian using only the original edges has
one-hop magnitudes fixed by |G_uv|^2=K_uv. Even permitting arbitrary complex
edge phases, its two-hop coefficient satisfies

    L_scalar <= (sum_v sqrt(K_uv K_wv))^2/4.

Consequently, at a defined common clock, the native ratio

    R_path=<M_uw^2>/(sum_v sqrt(<n_uv><n_wv>))^2

above one rules out EVERY such scalar surrogate at that state/readout. This
is an exact upper-bound test, not a fitted acceptance threshold. A value at
or below one does not establish a scalar model: phases, further paths,
multi-time memory and other responses still need independent tests. If the
denominator vanishes, report an undefined ratio, not a successful closure.

This is not an exclusion of every metric or coarse-grained description.
Internal channels, retained stochastic/quantum environments and memory can
carry the extra correlations. A physically justified coarse-graining may
also produce a controlled metric in another scale window.

## Prepared finite witnesses, including equal-energy controls

Take K2,2: left nodes u,w, right nodes v1,v2; order its bits
(a,b,c,d)=(n_uv1,n_uv2,n_wv1,n_wv2). All ensembles below have each edge mean1/2.
Records start blank, writers are fixed in the same content, g_wr=g>0 remains
on, and carrier-record/fragment copying is off. No record-count difference
or extra mass substance is inserted.

Set epsilon_1=epsilon_r-lambda_R, Delta_1=sqrt(epsilon_1^2+4g^2), and read the
fixed dressed record observable B_1 from the active-clock note. Its exact
initial amplitude is g/Delta_1. Since each mean degree is1 and the initial
record state factors from incidence, its initial rate is Delta_1/hbar in
EVERY ensemble, even those without a definite degree. This is an initial
derivative, not a finite clock-window certificate for these mixed graphs.

Here M=ac+bd and M^2=ac+bd+2abcd. Exact values are:

| Incidence ensemble | <M^2> = R_path | sum_v <d_v^2> | Energy above matching ensemble |
| --- | ---: | ---: | ---: |
| Equal mixture of the two perfect matchings | 0 | 4 | 0 |
| Four independent fair bits | 5/8 | 6 | 2 U_d |
| Equal blank/full mixture | 2 | 8 | 4 U_d |
| Uniform mixture of the eight even-parity strings | 3/4 | 6 | 2 U_d |
| Uniform mixture of the eight odd-parity strings | 1/2 | 6 | 2 U_d |

The scalar positive-edge prediction is1, and1 is also the maximum over all
phases. The blank/full witness exceeds it. A matching witness with zero
leading coefficient can still have later arrivals after incidence changes.

Even and odd parity have IDENTICAL every proper (one-, two-, three-edge)
marginal. Therefore they share each local degree distribution, all one-hop
coefficients, the initial clock, and the complete initial BS energy, yet have
different two-hop signals. This is a same-energy higher-correlation witness,
not merely an effect of loading more energy into the graph. Their four-edge
products differ because1111 has probability1/8 in even parity and zero in odd.

The energy table includes the full identity/degree baseline. In every arm,
sum<n_e>=2, sum<d_v>=4, record occupation/feedback and link-X expectations
vanish initially, carrier hopping vanishes in the localized state, and
current-square energy is lambda_J<d_u>=lambda_J. Fixed writer/carrier storage
is identical. Thus the complete initial energy is

    E0=epsilon_psi+4 epsilon_w+2 Delta+lambda_J
       +U_d[sum<d_v^2>-8d_*+4d_*^2].

These are legal PREPARED states; their generation, entropy/correlation custody
and preparation apparatus are not supplied by this witness. They are not
claims that the native blank state naturally forms any of these ensembles.
Root derived these identities; source-only review by handoff_plan_review_v005
checked the full-H^2 identity, scalar phase bound, clock and energy accounting.

## Prospective next test: correlations actually formed by the parent

Do not run another arbitrary ensemble or a scaling grid. The smallest next
question is whether the native blank-link/blank-record preparation develops
a scalar-bound violation on K2,2. This is a1024D sector: four carrier positions,
four link qubits and four fixed-content record qubits. Fixed writers are
occupied, fragments absent, g_psi_r=g_rb=0. All full incidence, record copying,
feedback, carrier storage, hopping and current-square terms remain.

Use the inherited microscopic coefficients, with the ORIGINAL N-dependent
flip scaling: N=2, Omega=1 gives h=1/2, not the N=1 cell's h=1.
Delta=4, U_d=d_*=epsilon_psi=epsilon_r=g_wr=1, epsilon_w=0,
t_hop=1/2, lambda_R=1/2 and lambda_J=1/4. The native initial state is all
blank links/records and carrier at u; complete initial energy is5.
Continue writer formation without a switch at the fixed ages0,.25,.5,1,2.
Use the same two causal controls as the earlier record experiment: feedback
off, and copying off, otherwise unchanged. This is a NEW four-node active
protocol, not a rerun of the two-node formation/hold history.

For each age, the ideal carrier-pointer SWAP transfers all old carrier
correlations into a fresh degenerate four-level pointer and leaves the
environment marginal intact. Localize the probe carrier at each required
sender, with the SAME record clock at u. The owned bulk work for sender u is

    W_swap(u)=lambda_J[<d_u>-<sum_v d_v P_v>]
              +t_hop sum_e <n_e T_e>.

This keeps the term absent in the two-node work formula: current-square
energy generally changes on a larger graph. All environment terms remain
unchanged and carrier number stays one. Pointer preparation/control/reuse
and a finite-duration implementation are not free or yet instantiated.
No SWAP propagation is required to calculate its exact initial derivatives.

Use fixed B_0 defined by epsilon_r,g_wr and Delta_0, not an instantaneous
moving-degree basis. Compute its ACTUAL complex expectation and derivative.
Because g_psi_r=0, its initial rate after the ideal carrier relocalization
is unchanged. Report undefined clocks explicitly, especially copying off.
The path-moment ratio can still be reported as a clock-free diagnostic, but
is not promoted to a phase-clock measurement when the clock is undefined.

Before execution, retain the complete source/inputs and fixed ages. Compare
the existing sparse exponential route with a separately implemented bounded
Taylor propagator, full-H reconstruction/Hermiticity, conservation and the
exact finite-ensemble oracles above. Use the inherited1e-10 absolute numerical
allowance; do not move it after the sign/size is seen. A ratio close enough to
one to depend on numerical uncertainty is inconclusive. Save complete states,
moments, all terms, work and undefined statuses, not only favorable examples.
This remains a finite candidate-mechanism test, not a galaxy or expansion fit.

There is a prospective short-time check that does NOT presume a violation.
From the declared all-blank graph, each edge has
p_e(s)=h_N^2 s^2/hbar^2+O(s^4). Each distinct two-edge path has joint
occupation h_N^4 s^4/hbar^4+O(s^6), so

    <M^2>=2 h_N^4 s^4/hbar^4+O(s^6),
    S^2=4 h_N^4 s^4/hbar^4+O(s^6),
    F=<M^2>-S^2=-2 h_N^4 s^4/hbar^4+O(s^6).

The common leading term holds in all three controls. Real initial data and
real Hamiltonians give even-time probabilities for this initial expansion;
that does not replace the generic O(probe_time^5) remainder after aging.
Initially formed links therefore satisfy this necessary scalar bound. Any
later violation must be an evolved effect, not a guaranteed output of the test.

## Relation to physical geometry and expansion

A changing one-hop K is already demonstrated at fixed record count. It does
not alone define length. If an independent continuum probe has a FIXED
dispersion coefficient D_z and a native homogeneous band has coefficient
c_z=t_eff*b/(hbar*nu), the adopted matching c_z=D_z/a_op^z yields
a_op=(D_z/c_z)^(1/z). The quadratic carrier band gives z=2, not a derived
linear photon branch. Without the independent probe law, this is a convention.
The two-hop test instead asks for a second prediction from an already
calibrated local observable. It makes the next geometry claim falsifiable
without inserting an expanding scale factor or treating records as dark mass.
