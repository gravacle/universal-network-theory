# Native incidence formation: exact size-dependent speed bound

2026-09-27. Analytical result only; no numerical execution, new interaction,
ground-state assumption, physical speed limit, or cosmological clock claim.

Source: resident recovered `recovered_sources/BS_MICRO_ACTION.md`, SHA256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
Resident flags were checked before reading BS06, BS09–BS11 and BS13.
Here **N is the BS width of each adjacent layer**: there are N+N nodes and
N² possible links in one slab. It is neither the remote calculation label
L6 nor an identified physical volume or spatial size.

## 1. Exact assumptions and source commutators

Use the native link projectors n_e=(I−Z_e)/2, total incidence
M=Σ_e n_e, and BS06 flip scaling h_N=Ω/N, with Ω>0 fixed across sizes:

    H(t)=−(Ω/N)Σ_e X_e + H_rest(t).

For the global result require [H_rest(t),M]=0 at every time. Arbitrary
time dependence, correlations with records/carriers/ports, and mixed states
are allowed under the declared unitary evolution. No link reset, graph
postselection, or unlisted incidence-changing intervention is included.

The native degree and incidence-storage energies commute with every n_e.
BS09's n_e T_e carrier hopping and BS11's n_e J_e² and record feedback do
also: T_e and J_e act on carrier factors. BS10's local record/writer/reservoir
storage and copy generators act on nongraph factors. Thus even a switched,
time-dependent native record-formation schedule has these commutators.
Writing records can change the subsequent state without bypassing the
incidence flip that creates or removes a link.

The stronger local-degree result below separately requires
[H_rest(t),d_v]=0 for each stated vertex. The listed native terms satisfy
this because they commute with every n_e. Total-incidence conservation alone
would not suffice: a number-conserving edge-exchange port could redistribute
degree arbitrarily fast. Unspecified BS12 ports are therefore not silently
included in either theorem; their required commutators must be checked.

## 2. Global bound for arbitrary joint states

Let p_e(t)=Tr[ρ(t)n_e] and m(t)=Tr[ρ(t)M]=Σ_e p_e(t). A link's reduced
two-state density matrix is positive, irrespective of entanglement elsewhere,
so

    |⟨Y_e⟩| ≤ 2√[p_e(1−p_e)].

With [X_e,n_e]=iY_e, the exact global equation and Cauchy–Schwarz give

    dm/dt = (Ω/(Nℏ))Σ_e ⟨Y_e⟩,
    |dm/dt| ≤ (2Ω/(Nℏ))Σ_e √[p_e(1−p_e)]
            ≤ (2Ω/(Nℏ))√[m(N²−m)]
            ≤ (2Ω/ℏ)√m.                                      (1)

This is not a mean-link replacement inside the Hamiltonian. It bounds the
exact first moment of M in the complete state; no energy estimate is used.

For ε>0, differentiation of √(m+ε) gives an absolute derivative bounded by
Ω/ℏ, including at m=0. Integrate and take ε→0:

    |√m(t)−√m(s)| ≤ (Ω/ℏ)|t−s|.                         (2)

Consequently an initially empty graph obeys, at every elapsed time τ≥0,

    m(τ) ≤ (Ωτ/ℏ)².                                      (3)

Piecewise-smooth switching of H_rest does not change the result: the state
and m are continuous across a finite Hamiltonian quench, and the inequality
holds on each interval. The conclusion assumes the same fixed Ω; a separate
time-dependent flip amplitude would instead require its own integrated bound.

### Optional sharper finite-occupancy form

The middle inequality in (1) implies

    |d/dt arcsin√(m/N²)| ≤ Ω/(Nℏ).                     (4)

Endpoint values follow by continuity/regularization. For example, integrate
the derivative of
½∫_0^m dz/√[(z+ε)(N²+ε−z)], then take ε→0. From m(0)=0 this yields

    m(τ) ≤ N² sin²[Ωτ/(Nℏ)]
       for 0≤Ωτ/(Nℏ)≤π/2.                              (5)

After that interval use m≤N², not the periodically decreasing sine expression.
Equation (3) remains valid for all τ and follows directly from (2).

## 3. Local-degree bound and the formation-time consequence

Under the separately stated local commutator premise, let
z_v(t)=⟨d_v⟩, where d_v sums the N possible links incident on v. The same
reduced-link inequality gives

    |dz_v/dt| ≤ (2Ω/(Nℏ))√[z_v(N−z_v)]
              ≤ (2Ω/(ℏ√N))√z_v,
    |√z_v(t)−√z_v(s)| ≤ Ω|t−s|/(ℏ√N).                 (6)

Thus a graph-blank start gives z_v(τ)≤(Ωτ/ℏ)²/N at every vertex. A desired
mean incidence m≥Nd, where d>0 is the intended mean degree and d≤N, requires

    τ ≥ (ℏ/Ω)√(Nd).                                    (7)

The sharper version is τ≥(Nℏ/Ω)arcsin√(d/N). Both are necessary conditions,
not sufficient preparation times or guarantees of reaching any graph family.
They concern unconditional means, not a claim that every realized graph is
regular or that conditioning on rare dense outcomes is permitted.

At fixed Ω and fixed finite elapsed time, a blank-start family therefore has
m=O(1) and average degree m/N=O(1/N). Record occupation may still change on
that schedule; writing many records is not the same as forming an extensive
number of links. Preparing a mean Nd with fixed d>0 from blank requires
an elapsed clock interval at least proportional to √N under these assumptions.
A nonblank initial graph is
instead governed by (2), so a previously prepared sparse network is not
excluded. Nor does this establish its persistence or energy affordability.

## 4. Scientific interpretation

This is a native regime diagnostic across BS layer widths, not another
fixed-size fitted example. A successful small finite-time formation experiment
cannot simply be promoted to a fixed-duration large-N formation route while
retaining Ω and all stated initial conditions. Keeping h fixed as N grows
would change Ω=Nh and would be a different scaling family.

The bound applies during carrier transport, occupation-dependent feedback,
and native record copying without assuming graph cooling or a ground state.
It leaves open longer controlled formation, appropriately owned initial
incidence, and complete ports whose verified action changes the premises.
Their scientific and energy costs cannot be erased by the bound.

No physical metric, signal cone, spatial propagation speed, dark-matter
transport, dark-energy pressure, or interpretation of increasing N as cosmic
expansion follows. Sparse incidence alone also does not prove locality or a
geometric phase. The result instead identifies a concrete time-and-size
constraint that any proposed native formation pathway must satisfy.
