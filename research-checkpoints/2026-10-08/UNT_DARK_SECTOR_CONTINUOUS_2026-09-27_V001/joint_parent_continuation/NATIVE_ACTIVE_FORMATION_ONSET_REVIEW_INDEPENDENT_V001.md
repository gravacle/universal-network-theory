# Active formation onset — independent analytical review

Verdict: **PASS for the stated conditional finite-system identities and error
bounds.** The root note `NATIVE_ACTIVE_FORMATION_ONSET_ROOT_V001.md` was read
in full at SHA-256
`7edfc2cedb4a74613fd9ae0ddb553c524b5e295447e11df481ca988555045822`.
This review supplies no numerical outcome, preparation selection or execution
authority. No project code, matrix calculation, solver or numerical worker was
run; the checks below are hand algebra against the original source and notes.

## Conditional support and leading terms

The original BS07–11 operators preserve the stated single-content support,
total carrier number and individually fixed writer projectors. Here writer
bit zero means B and writer bit one means the same chosen content x; it does
not mean that writers of both distinct contents are allowed in this binary
target space. Opposite-content writers or nonpreserving ports require the
larger space. The initial pure blank link/record/fragment factors imply their
product with the arbitrary fixed-P carrier density; no hidden correlation with
a pure blank factor has been discarded.

For the blank-support projector Pi0, projecting H onto an occupied record
leaves precisely `G_v X_rv Pi0`. A fragment cannot be occupied after one H
action. After two actions its only surviving path is record write followed
by that fragment's conditional write, giving
`b_vk H^2 Pi0 = g_rbk G_v X_bvk X_rv Pi0`. The reverse order annihilates
the initial state. Diagonal energy, current-square and feedback terms, and
the initially blank-gated carrier hopping, cannot supply either target flip.
Incidence creation does not create a fragment in two actions.

Squaring the first projected amplitude gives the record coefficient in (2).
The second-order state amplitude is
`-tau^2 g_rbk G_v X_bvk X_rv Pi0/(2 hbar^2)`, giving the fragment coefficient
`g_rbk^2 <G_v^2> tau^4/(4 hbar^4)`. The stated generic remainders O(tau^3)
and O(tau^5) are valid. For real H, real initial density and these real
occupation projectors, complex conjugation relates plus/minus time and makes
the expectations even, allowing O(tau^4) and O(tau^6). The density matrix itself
need not have an even series.

Because `p_v^2=p_v`, `w_v^2=w_v` and w is a fixed scalar, (3) follows exactly.
The cross term is interference of two amplitudes writing the same target and
content. It is absent from an independent-additive-rate replacement, but is
not evidence of writer-content superposition, monotonic production or cooling.
Zero leading amplitudes remain included. The homogeneous sum uses only
`sum_v <p_v>=P`; it makes no claim that local carrier occupations are fixed.

## Ancestry: the sequential writer-only onset was already present

`NATIVE_FINITE_FRAGMENT_SOURCE_CURRENT_V001.md`, SHA-256
`1116b37f9cbd35a10abc55632f4d21230cdee5a27c5122e0d70d138881b4324b`,
equation (11), already states, with `u=t/hbar`, `f_j=s_j^-1` for A and
`f_j=1` for B,

```
<R>(t) = 2 g^2 f_j^2 u^2 + O(u^4),
<q_bL+q_bR>(t) = g^2 lambda^2 f_j^4 u^4/2 + O(u^6).
```

It also explicitly gives the endpoint record-then-copy amplitude
`-g lambda f_j^2 u^2/2`. Thus sequential quadratic/quartic onset is not a new
discovery here. At the level of these leading amplitudes, two identical
endpoints with `G_v=g f_j` and `g_rbk=lambda f_j` recover that equation.
This identification does not equate its complete 384D A/B apparatus,
controllers, source dictionary or initial state with the present ports-off
sector. The useful extension is simultaneous carrier/writer interference,
arbitrary fixed-P carrier density and the explicit finite-window controls.

## Finite-window proof

For a finite time-independent Hermitian `K=H-cI`, the spectral norm of its
unitary exponential is one. The integral Taylor remainder after degree one
therefore has norm at most `z^2/2`, and after degree two at most `z^3/6`, where
`z=kappa |tau|/hbar` and `kappa>=||K||`. No exponential factor is needed.
Both signs in the displayed remainder differences in (4) are correct.

For mixed rho0, apply the projected remainders to `sqrt(rho0)` in
Hilbert–Schmidt norm. Normalization gives `||sqrt(rho0)||_HS=1`; the leading
norms are exactly a_r and a_b. The elementary inequality
`abs(||A+E||_HS^2-||A||_HS^2) <= 2||A||_HS||E||_HS+||E||_HS^2`
then proves both bounds in (5). Scalar centering leaves the leading record
and fragment projections unchanged because `r Pi0=b Pi0=b H Pi0=0`.
It removes neither an absolute energy nor a physical source derivative.

The norm bound must cover the complete retained Hamiltonian. These are fixed
finite-system absolute bounds, including vanishing leading coefficients, not
relative bounds or uniform-in-size formation guarantees. A time-dependent
envelope or newly active port would require its appropriate separate bound;
the note does not claim this time-independent Taylor argument covers it.

## Sector size and the genuinely different next discriminator

For V nodes, E incidence qubits, K fragments per node, one content and fixed
carrier count P, the full formation-inclusive sector has dimension
`binom(V,P) 2^[E+V(1+K)]`. With V=2, E=1, P=1, K=1 this is 64. The fixed
writers contribute their absolute energies, not extra dynamical dimensions.
Any retained dynamical controller or additional port factor must enlarge this
dimension rather than disappear in a trace.

The earlier `NATIVE_CARRIER_RULER_PATHWAY_V001.md` (SHA-256
`4277871cd49f7e45169f3fd7db0b5d49b9b66651f6b4ac257d794a5230254db8`)
has a different N=2 held space: four possible edges and four one-carrier
positions, `2^4*4=64`, with records held and copying off. Equal dimensions do
not identify bases, preparations, source insertions or completed tests.
Likewise `RECORD_ADDITION_PROTOCOL.md` (SHA-256
`2021e117b74d760cd3d731018cd91f3cba6ef92415beda9d951f9d6a42daff49`)
uses a 16D two-record/link/carrier space with writer copying only, explicitly
without the newly active carrier-to-record or fragment copies.

A concrete next discriminator is the carrier-swap conservation used in
`NATIVE_ORDERED_FRAGMENT_SECTORS_AND_COLLISION_LIMIT_V001.md`, equation (2),
SHA-256 `db905c9315a4918d18c55703b8c3ca31f16807df61944db05ba14e1cf978a7db`.
In the carrier basis `(|L>,|R>)`, take standard Pauli matrices
`X_c=[[0,1],[1,0]]`, `Y_c=[[0,-i],[i,0]]`, `Z_c=diag(1,-1)`, and
`p_L=(I+Z_c)/2`, `p_R=(I-Z_c)/2`. For the homogeneous, ports-off two-node
BS sector, all other terms commute with X_c, whereas

```
[H,X_c] = i g_psi_r Y_c (X_rL-X_rR).
```

Thus full carrier-controlled formation does not inherit the earlier
apparatus's X_c conservation. This does not eliminate other symmetries:
with symmetric writer data a simultaneous exchange of carrier, records and
fragments may still be a symmetry. Nor does the nonzero commutator prove
mixing, cooling, a unique state or ground preparation. It identifies a real
operator difference worth retaining in the proposed exact sector embedding,
without selecting an age or favorable coefficients.

BS source checked: `../recovered_sources/BS_MICRO_ACTION.md`, SHA-256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
The onset note correctly leaves physical preparation, controller work,
clock/ruler/volume mappings and source-preserving completion unresolved.
No old outcome is replaced and no physical qualification follows.
