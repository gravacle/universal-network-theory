# Closed holds cannot supply the missing cold-graph preparation

2026-09-27. Exact native energy/spectral bounds, independently checked by the
root and GPT-6 Astra Ultra inverse-response agent. No numerical worker,
microscopic modification, physical-temperature assumption or cooling protocol.

This addresses the actual preparation question left open by the preferred-
arrangement calculation. It is stronger than a finite-time speed bound:
waiting arbitrarily long in the stated closed hold does not remove the
obstruction. It is NOT a statement about formation with energy-absorbing
records/reservoirs, nor an exclusion of prepared connected networks.

## 1. Complete native energy and a conserved spectral measure

Use one carrier-free, source-off slab with fixed binary record occupations,
no nongraph energy sink or time-dependent ports, and the same native action

    H=Hdiag+V,
    Hdiag=epsilon_r D_rec+sum_v[U(d_v-d_*)^2
                                     +(Delta/2-lambda q_v)d_v]+C_spec,
    V=-(Omega/N)sum_(N^2 edges) X_e.                     (1)

Every storage and spectator constant is retained. For ANY initial graph
basis vector |G>, write E_G=<G|Hdiag|G>. Single-edge flipped states are
orthogonal, so exactly

    <H>_G=E_G,
    Var_G(H)=||(H-E_G)|G>||^2=N^2(Omega/N)^2=Omega^2.   (2)

The spectral measure of H, not just its mean, is invariant under exp(-iHt/hbar).
For the full Hamiltonian's projector Pi_{<=E_cut}, if E_G>E_cut,

    <Pi_{<=E_cut}>_t <= Omega^2/(E_G-E_cut)^2            (3)

at EVERY time. This follows by applying the positive operator inequality
(H-E_G)^2 >= (E_G-E_cut)^2 Pi_{<=E_cut} in the initial state. One may cap
the bound by one. The slightly sharper one-sided bound is
Omega^2/[Omega^2+(E_G-E_cut)^2], obtained by minimizing the expectation of
(H-E_G-b)^2/(E_G-E_cut+b)^2 over b>0. Neither bound assumes perturbation
theory, dephasing or a factorized evolved state.

## 2. Empty incidence versus a nonempty preferred regular sector

Let d0>0 be a feasible common preferred degree with

    c=Delta+4U(d0-d_*),
    g=U-max(|c/2|,|c/2-lambda|)>0,
    K=sum_v(d_v-d0)^2,
    Ecl=2NU(d0-d_*)^2+Delta N d0
                               +(epsilon_r-lambda d0)D_rec+C_spec.

An initially empty graph has the SAME fixed record sector and energy
E_empty=2NU d_*^2+epsilon_r D_rec+C_spec. The exact difference is

    Delta_E=E_empty-Ecl
           =N d0(2U d0-c)+lambda d0 D_rec
           >=2g N d0^2.                                (4)

The inequality follows from Hdiag-Ecl>=gK and K_empty=2N d0^2.
For any fixed energy allowance C, the probability of finding the evolving
state in the exact energy window H<=Ecl+C is therefore at most

    Omega^2/[2g N d0^2-C]^2=O(N^-2)                    (5)

once the denominator is positive. In particular the low-energy regular
band identified under the separate weak-Omega condition cannot acquire
order-one occupation merely through a longer closed hold. The actual
ground energy is <=Ecl by a regular basis trial.

Equation (5) is a spectral-window statement, not an equality between that
window and a measurement of bare graph degree. Those observables differ.
The next bound addresses degree deviations directly.

## 3. All-time lower bound on the actual squared degree defects

Define

    Gcoef=U+max(|c/2|,|c/2-lambda|),
    beta=min(d0,N-d0),       b_N=1+2d0(1-d0/N).

For integer k, |k|<=k^2. Thus the complete diagonal difference also obeys
the UPPER bound Hdiag-Ecl<=Gcoef K. The independently proved statewise
native flip estimate is

    |<V>| <=Omega sqrt(2b_N <K>)
                       +Omega sqrt[(beta+1)/N] <K>.     (6)

It is valid for every state, not only a ground state. If the conserved
initial excess energy is Delta_E>=0, put

    A_N=Gcoef+Omega sqrt[(beta+1)/N],
    B_N=Omega sqrt(2b_N),
    kappa(t)=<K>_t.

Energy conservation and (6) yield Delta_E<=A_N kappa+B_N sqrt(kappa), hence

    kappa(t)>=[(sqrt(B_N^2+4A_N Delta_E)-B_N)/(2A_N)]^2. (7)

This holds for all times and every fixed Omega; the small-Omega isolation
condition and the ground theorem's a_N>0 are NOT required for (7).
For an empty start, Delta_E is linear in N. At fixed d0,g,Omega,

    liminf_N kappa(t_N)/N
      >=liminf_N (Delta_E/N)/Gcoef
      >=2g d0^2/Gcoef>0                                (8)

for ANY sequence of times t_N, including times increasing arbitrarily fast.
Consequently this closed hold cannot produce the O(1)-defect regime of the
preferred ground family from empty incidence. The earlier formation speed
bound alone did not show this all-time obstruction.

K is a SUM OF SQUARED deviations. Equation (8) does not imply that a fixed
fraction of vertices is defective: energy/defects could concentrate in a
small number of high-degree vertices or rare high-degree outcomes. It also
does not by itself bound all carrier readouts or rule out other hot,
nonequilibrium graph families. Those distinctions are essential.

## 4. Where the missing energy could go in a formation protocol

The source already includes record/writer/reservoir formation couplings.
Allowing these to change occupations or absorb energy changes the premises
of Sections 1-3. One must then track the COMPLETE energy rather than assume
graph-only cooling. This is a constructive route, not a license to discard
released degree energy.

For an explicit endpoint ledger, take the same coefficients, initially empty
incidence AND blank records, and formation couplings zero at both endpoints.
Compare with a final common-degree reference containing D_rec records. Define

    A=d0(2U d0-c),        mu=epsilon_r-lambda d0.

The reference's exact graph-plus-record energy change is

    E_ref,final-E_initial=-A N+mu D_rec.                 (9)

Let delta_E be the actual final graph/record energy in excess of that complete
reference, Delta E_other the separately owned change in carriers, writers,
reservoirs and other included factors, and W the total applied work. Then

    mu D_rec=A N+W-delta_E-Delta E_other.                (10)

All crossing interactions must be assigned once in this ledger. If using a
driven formation coupling g(t), its work belongs in W through
integral <partial_t H> dt; setting g to zero is not automatically free.
If ports remain interacting at an endpoint, their interaction energies must
be retained in the explicit endpoint assignment as well.

For mu>0, (10) constrains the record fraction D_rec/(2N). Only under the
ADDITIONAL assumptions W=0, Delta E_other=0 and delta_E=o(N) does it reduce
to A/(2mu). That number must lie in [0,1] and meet the degree feasibility
conditions. It is an energy-compatibility relation, NOT a dynamical abundance
prediction, proof of reachability, or a selected initial population.

The ledger demonstrates precisely why record formation/energy transfer
could evade the closed-hold obstruction and what must be calculated next.
Unproved equilibration, a chosen final population, or an unexplained energy
sink cannot be hidden in the word 'history'. No statement about cosmological
dark abundance, physical volume or gravitational stress follows without
the corresponding same-parent maps and an actual formation mechanism.

## Sources and independent checks

The resident recovered BS source supplies (1), with SHA256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
`NATIVE_UNIFORM_REGULAR_DEGREE_BOUND_V001.md` supplies the fully checked
statewise (6), not an extrapolated numerical scaling. Root reread the resident
formation-speed, prepared-transfer and correlation/preparation notes to
distinguish their earlier results from the new all-time energy constraints.
The inverse-response agent independently checked (2)-(8) and their scope.
Equation (10) is the complete endpoint energy balance, not an added force law.
