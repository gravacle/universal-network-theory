# Native source-feedback response: exact scaling bounds

2026-09-27. Analytical bounds independently checked against the native
commutators. No numerical execution, changed microscopic interaction,
ground preparation, or universal gravity exclusion.

Source: resident recovered `recovered_sources/BS_MICRO_ACTION.md`, SHA256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`,
BS06 and BS09–BS11. N is the width of each layer in one BS slab, with N²
possible links and h_N=Ω/N. Ω is fixed in the size limits below. N is not
the remote L6 label or an identified physical volume.

## 1. Same-state source ablation and its assumptions

Work in a source-off hold: all formation/copy couplings g=0 and no ports.
Retain the native carrier terms, degree penalties, storage, other record
feedback and all link flips. For one source vertex s define

    d_s=Σ_(e incident s) n_e,
    F_s=−λ_R q_s d_s,
    H_1=H_native,          H_0=H_1−F_s.

Both evolutions start from the SAME complete joint density matrix ρ. Every
record occupation q_v is conserved, but ρ may contain superpositions and
correlations between occupation sectors. A fixed bounded Hermitian readout
O is used in both arms. Carrier observables and occupation-weighted carrier
observables commute with F_s.

Removing F_s is a term-specific analytical intervention, not deleting the
record or its storage energy. A physical sudden removal would require work
λ_R⟨q_s d_s⟩≥0 and an owned controller. These are not energy-matched arms.
The following bounds require no small λ_R, spectral gap or energy condition.
Unlisted incidence-changing or q-mixing ports are outside their premises.

## 2. Arbitrary initial graph state: one-source bound

Let E_s be the N possible links incident on s. Remove only their native
flip terms to define reference Hamiltonians:

    V_s=−h_N Σ_(e∈E_s) X_e,          H'_a=H_a−V_s.

All remaining native terms commute with d_s and q_s. Therefore

    [H'_a,d_s]=[H'_a,q_s]=0,
    [H'_0,F_s]=0,                  H'_1=H'_0+F_s.

For [O,F_s]=0 the two reference expectations are exactly identical at every
time, even for an initially entangled state with record-sector coherences.
Indeed U'_1=U'_0 exp(−iF_sT/ℏ), and the extra factor commutes with both
U'_0 and O. No projection onto a fixed q sector is needed for this result.

Define link lowering operators σ^-_e=|0⟩⟨1|_e, where n_e=|1⟩⟨1|_e,
and A_s=Σ_(e∈E_s)σ^-_e. Vector Cauchy–Schwarz gives the operator inequality

    A_s† A_s ≤ N d_s.

Also [A_s,A_s†]=N−2d_s, hence

    A_s A_s† ≤ N(d_s+1).

For any normalized joint vector ψ with z=⟨d_s⟩ this yields

    ||Σ_(e∈E_s)X_e ψ||
       ≤ ||A_sψ||+||A_s†ψ||
       ≤ √N [√z+√(z+1)].                              (1)

Reference evolution conserves z=z_0=Tr(ρd_s). Duhamel's identity, with
the perturbation acting on the reference-evolved vector, therefore gives

    ||(U_a(T)−U'_a(T))ψ||
       ≤ Ω|T|[√z_0+√(z_0+1)]/(ℏ√N).                  (2)

Each normalized-state expectation changes by at most twice the operator
norm times this vector distance. Comparing both arms through their equal
reference expectations proves

    |Δ⟨O(T)⟩|
      ≤ min{2||O||,
             4||O|| Ω|T|[√z_0+√(z_0+1)]/(ℏ√N)}.       (3)

Here Δ means H_1 minus H_0. A mixed state is handled by purification;
all operators above act trivially on the purifying factor, and z_0 remains
Tr(ρd_s). Thus no product-state, real-state or classical-graph assumption
is hidden in (3).

For a family with uniformly bounded initial expected source degree z_0,
fixed Ω, fixed T and uniformly bounded ||O||, (3) is O(N^−1/2).
A global O(N) incidence bound alone does not guarantee this local premise:
incidence might concentrate at the selected source. No sign of the response
is inferred, and the bound need not be sharp as λ_R→0.

## 3. Prepared source incidence: sharper bound and several sources

First fix a record-occupation sector. Let a fixed source set R contain r
vertices, and remove the sum of their endpoint feedback terms:

    F_R=−λ_R Σ_(s∈R)q_s d_s.

Let E_R be the UNION of their incident possible links and b=|E_R|≤min(N²,rN).
An edge with two source endpoints contributes twice to F_R as the native
endpoint law requires, but appears only once in E_R's flip count.

Suppose the initial state is supported on P, the projector fixing every
link in E_R to a declared computational pattern G. Other links and matter
may be arbitrary. A fully prepared classical graph is sufficient, but not
necessary. This is an initial-state assumption, not a postselection step.

Within P the two Hamiltonians differ by the constant

    P F_R P = c P,          c=−λ_R Σ_(s∈R)q_s d_s(G).

Their compressed reference evolutions therefore differ only by a global
phase. The only P-to-Q coupling, with Q=I−P, comes from the b union-edge
flips. Distinct single-flip patterns are orthogonal, giving exactly

    (QH_aP)†(QH_aP)=b h_N² P,
    κ=||QH_aP||/ℏ=Ω√b/(Nℏ).                           (4)

For ψ_0 supported in P, write u_a=P U_aψ_0 and v_a=Q U_aψ_0. Let
φ_a=exp(−i(PH_aP)|_P T/ℏ)ψ_0 be the normalized compressed reference state.
Two Duhamel integrals give

    ||v_a(T)||≤κ|T|,
    ||u_a(T)−φ_a(T)||≤κ²T²/2.                           (5)

For [O,P]=0, the P–Q expectation cross terms vanish. Since ||u_a||≤1,

    |⟨O⟩_(U_aψ_0)−⟨O⟩_(φ_a)|
       ≤2||O||||u_a−φ_a||+||O||||v_a||²
       ≤2||O||κ²T².

The two reference expectations agree, so

    |Δ⟨O(T)⟩| ≤ min{2||O||, 4||O||Ω²T² b/(N²ℏ²)}
               ≤ min{2||O||, 4||O||Ω²T² r/(Nℏ²)}.       (6)

The mixed-state extension again follows by purification. A single prepared
source star has b=N and therefore an O(1/N) fixed-time bound. The result
uses neither graph locality nor a sparse maximum-degree assumption.

### Conserved quantum source occupations

If the initial q_v are in superposition rather than a fixed sector, c above
is NOT a scalar: it becomes C_q=−λ_RΣ_(s∈R)q_s d_s(G). The references still
commute with C_q because all occupations are conserved. Thus (6) continues
to hold for readouts commuting with C_q, in addition to P. All carrier and
occupation-weighted carrier readouts satisfy this condition. A readout
mixing record sectors need not: it can detect the relative record phase
even with the source links frozen. That case is not covered by (6).

For r proportional to N, (6) no longer enforces vanishing response. This
only removes suppression by THIS bound; it is not a demonstration of an
order-one collective response or an escape from other locality/preparation
bounds applicable to the same state and observable.

## 4. Exact occupation-dephasing control

Let P_q be the joint spectral projectors of every retained record occupation,
and Γ(ρ)=Σ_q P_qρP_q. For a hold commuting with all P_q and a readout
commuting with all P_q,

    Tr[ρ U†OU]=Tr[Γ(ρ) U†OU].                           (7)

The hold energy is unchanged as well: Tr[HΓ(ρ)]=Tr[Hρ]. This removes only
coherences BETWEEN occupation sectors. The unnormalized conditional
graph/carrier blocks P_qρP_q, including their internal correlations, remain
unchanged. Replacing the state by products of its marginals is a different
operation and can change both feedback energy and transport.

Equation (7) is an exact analytical negative control, not a claim that a
physical dephasing apparatus costs nothing. Inter-occupation-sector phase
alone cannot change these hold readouts; later q-mixing formation or read
interactions would require a different analysis.

## 5. Scientific boundary

These bounds constrain a SAME-INITIAL-STATE feedback ablation over a fixed
hold interval. They do not compare differently prepared, record-dressed
initial geometries. They do not establish ground-state tracking, permanent
capture, or the absence of earlier formation effects. Longer N-dependent
holds, different source-degree scaling, collective sources, or added
interventions require their own complete premises and work accounting;
none is automatically a successful alternative.

The native carrier remains mobile while the records are conserved. Neither
the response bounds nor an energy coefficient identifies physical distance,
inertial/gravitational mass, pressure, dark abundance, or a continuum metric.
They are concrete checks on native transport mechanisms and size limits,
not a universal no-go theorem for Universal Network Theory or gravity.
