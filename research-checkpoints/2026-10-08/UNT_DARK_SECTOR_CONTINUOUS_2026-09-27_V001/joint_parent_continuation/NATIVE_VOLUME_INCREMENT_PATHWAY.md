# Native volume increments: a constructive growth pathway and its missing work

2026-09-28. Analytical continuation of the resident BS microscopic seed.
No numerical worker, new fitted constant, change to frozen files or claim
that node count already measures physical volume.

## Result

The BS family gives an exact energy ledger for adding a blank node on each
side of one slab. It retains both the new degree-baseline energy and the
work caused by changing the old links' coupling `h_N=Omega/N`. In a stated
blank-register parameter regime, its lowest energy can also be bounded
sharply enough to derive a controlled large-N asymptotic without a worker.

These results make a native growth experiment possible. They do not yet
turn node-creation energy into vacuum pressure. Even knowing every absolute
energy along a proposed `V=2N v_cell` sequence fixes only a combination of
creation chemical work and volume work. An explicit counterexample below
preserves the entire sequence while changing pressure.

The smallest constructive extension is therefore a number-changing
source/controller term plus an operational volume-conjugate variation,
with their energies counted once. It need not introduce a dark particle or
fit a new vacuum term. But it must predict a growth current and its stress,
not merely declare that accumulating nodes is accelerating expansion.

## 1. Exact blank-pair inclusion, with no energy zero discarded

Work in one ports-off BS slab with N nodes on each side and N squared
possible links. The full register Hamiltonian is BS04--BS11 of
`recovered_sources/BS_MICRO_ACTION.md`; keep all its coefficients fixed
except for the already prescribed `h_N=Omega/N`. This is a single-slab
statement, not a new counting convention for the overlapping multislab
schedule.

Let `I_N:H_Nspace -> H_(N+1)space` denote the isometric preparation below
(written `mathcal I_N` in the equations, not a physical volume):

- retains every old register, state and correlation;
- adds one node on each side with all carrier, record, writer and reservoir
  registers in their unique blanks;
- adds all `2N+1` new incidence qubits in `n=0`.

The appended labels identify a prospective inclusion experiment. Physical
ports or a separately supplied covariant/symmetrized inclusion must own
that anchoring; it is not new evidence for a preferred node labeling.

Put `S_X=sum_old_edges X_e`. Compressing the new Hamiltonian onto the
prepared subspace gives the exact operator identity

\[
\boxed{\mathcal I_N^\dagger H_{N+1}\mathcal I_N-H_N
=2U_d d_*^2 I+\frac{\Omega}{N(N+1)}S_X.}               \tag{1}
\]

Old-node degrees are unchanged by blank new links. Each new zero-degree
node contributes `U_d d_*^2`. New onsite occupancies and all new copy
expectations vanish; the new blank donors annihilate their copy operators.
New incidence-weighted hopping/current/feedback terms vanish on the blank
links. The remaining change is the weakening of **every old** link-flip
coefficient from `Omega/N` to `Omega/(N+1)`.

For any retained old density matrix, the instantaneous prepared energy
increment is therefore

\[
\Delta E_{\rm incl}
=2U_d d_*^2+\frac{\Omega}{N(N+1)}\langle S_X\rangle,
\qquad
|\Delta E_{\rm incl}-2U_d d_*^2|
\le\frac{\Omega N}{N+1}.                             \tag{2}
\]

An all-blank old incidence state has zero coherence correction; a general
formed state does not. Existing record-storage energies are retained, not
subtracted again. Preparing new occupied registers instead of blanks adds
their actual onsite/source energies and subsequent binding work; it is a
different inclusion preparation.

Compression is not an exact energy-eigenstate embedding. At operator level

\[
H_{N+1}\mathcal I_N-\mathcal I_N H_N
=\mathcal I_N\left(2U_dd_*^2I+\frac{\Omega S_X}{N(N+1)}\right)
 -\frac{\Omega}{N+1}\sum_{e\,\rm new}X_e\mathcal I_N. \tag{3}
\]

The last term leaves the prepared subspace. The new one-flip states are
mutually orthogonal, giving leakage norm

\[
\|(I-\mathcal I_N\mathcal I_N^\dagger)H_{N+1}\mathcal I_N\|
=\frac{\Omega\sqrt{2N+1}}{N+1}.                     \tag{4}
\]

For any normalized old state its contribution to the new Hamiltonian
variance is `(2N+1)Omega^2/(N+1)^2`, in addition to the variance of
`H_N+Omega S_X/[N(N+1)]` in the old state. Thus a coherent number-changing
controller must account for a transition spectrum, not only its mean cost.

Equation (1) also identifies a hidden implementation obligation in a
growth proposal: the old size normalization changes globally. Either an
autonomous count-dependent interaction derives that change, or its work
belongs to a controller. Holding all old couplings fixed while appending
nodes would be a different Hamiltonian family.

## 2. A controlled large-N energy result from the native blank sector

There is an exact invariant sector with every carrier, record, writer and
reservoir register blank and no ports. All content-transfer/copy terms
annihilate it. Its Hamiltonian is precisely the incidence Hamiltonian; this
is **not** asserted to be the ground state of the full register theory or
the actual formed state used in the other experiments.

Let `M=sum n_e`, assume `U_d>=0`, and define the fixed positive edge cost

\[
\kappa_0=\Delta+2U_d(1-2d_*)>0.
\]

Using `d_v^2=d_v+2 sum_(e<f incident v)n_e n_f`, the exact blank-sector
Hamiltonian is

\[
H_N^{B}=2NU_d d_*^2 I+\kappa_0M
 +2U_d\sum_v\sum_{e<f\ni v}n_en_f
 -\frac{\Omega}{N}\sum_eX_e.                         \tag{5}
\]

The pair term is positive. Dropping it gives independent two-level edges
with lowest energy

\[
\ell_N=\frac{N^2}{2}\left[
\kappa_0-\sqrt{\kappa_0^2+4\Omega^2/N^2}\right]
=-\frac{2\Omega^2}{\kappa_0+\sqrt{\kappa_0^2+4\Omega^2/N^2}}.
\]

Use that independent-edge ground product as a variational trial state for
the complete (5). Each edge has probability

\[
p_N=\frac12\left(1-\frac{\kappa_0}
 {\sqrt{\kappa_0^2+4\Omega^2/N^2}}\right).
\]

There are `N^2(N-1)` unordered incident edge pairs across the `2N` nodes.
Consequently the true lowest energy **within this blank sector** obeys

\[
\boxed{
2NU_dd_*^2+\ell_N\ \le E_B(N)\ \le
2NU_dd_*^2+\ell_N+2U_dN^2(N-1)p_N^2.}                 \tag{6}
\]

At fixed positive `kappa_0`, `p_N=Omega^2/(kappa_0^2 N^2)+O(N^-4)`.
The final upper-bound term is `O(N^-1)`, while
`ell_N=-Omega^2/kappa_0+O(N^-2)`. Thus

\[
\boxed{E_B(N)=2NU_dd_*^2-\frac{\Omega^2}{\kappa_0}
 +O(N^{-1}),\qquad
E_B(N+1)-E_B(N)=2U_dd_*^2+O(N^{-1}).}                 \tag{7}
\]

No thermodynamic fit or numerical extrapolation enters (6)--(7). For the
inherited one-link coefficients `Delta=4,U_d=1,d_*=1`, `kappa_0=2`.
Other coefficients must satisfy the displayed condition; the result is not
uniform as `kappa_0` approaches zero or changes with N.

There is an important structural consequence. For any state,

\[
|\langle S_X\rangle|\le
2\sqrt{\langle M\rangle(N^2-\langle M\rangle)}.
\]

The blank-sector ground energy is no higher than the all-blank product
baseline. Combining this with the lower bound in (5) gives

\[
\boxed{\langle M\rangle_B
\le\frac{4\Omega^2N^2}{\kappa_0^2N^2+4\Omega^2}=O(1).} \tag{8}
\]

An incidence-graph measurement connected on all `2N` nodes requires at
least `2N-1` occupied edges. Its probability is therefore at most
`<M>_B/(2N-1)=O(N^-1)`. This positive-cost blank ground branch does not
already supply a connected macroscopic geometry. Its extensive energy is
dominated by the degree baseline of largely isolated nodes, not an
extensive population of quantum link fluctuations.

Active/record-bearing states, different native parameter regimes or a
controlled critical scaling can alter that conclusion. The result instead
identifies a useful requirement: newly created blank cells must become
operationally incorporated into a connected record/carrier geometry before
their count can be interpreted as additional spatial volume. Assuming
that incorporation would bypass the mechanism being sought.

## 3. Why an absolute node increment still does not fix vacuum pressure

Now **propose**, without adopting as native fact, that one slab represents

\[
V_N=2N v_{\rm cell},\qquad v_{\rm cell}>0
\]

in independently calibrated physical units. Equation (7) would give the
on-path energy density

\[
\frac{E_B(N)}{V_N}
\longrightarrow\frac{U_dd_*^2}{v_{\rm cell}}.
\]

This is a positive constant if `U_d d_*^2>0`. It is not yet a stress tensor.
In a thermodynamic description with distinct volume and pair number, the
work differential, at fixed entropy and other specified variables, is

\[
dE=-p\,dV+\mu_{\rm pair}\,dN,
\qquad
\left.\frac{dE}{dN}\right|_{V=2Nv_{\rm cell}}
=\mu_{\rm pair}-2v_{\rm cell}p.                      \tag{9}
\]

For a driven coherent preparation the corresponding complete source-work
ledger replaces the equilibrium differential; it does not remove the two
independent physical variations.

For example, with `epsilon_cell=U_d d_*^2`, the extensive energy along the
entire proposed sequence is compatible with both

    E(V,N)=2 epsilon_cell N:    p=0, mu_pair=2 epsilon_cell,
    E(V,N)=epsilon_cell V/v_cell: p=-epsilon_cell/v_cell, mu_pair=0.

They agree at every `V=2Nv_cell`. More sharply, for any completion that
agrees with all known `H_N`, the physical-source family

\[
H_{\alpha}(V,N)=H(V,N)+\alpha(V-2Nv_{\rm cell})I        \tag{10}
\]

has exactly the same on-path Hamiltonian, absolute spectra and normalized
states for **every** N. Yet it changes

\[
p\to p-\alpha,\qquad
\mu_{\rm pair}\to\mu_{\rm pair}-2\alpha v_{\rm cell},
\]

leaving (9) unchanged. This is not permission to modify the frozen seed or
fit alpha; it proves that more on-path energies alone cannot identify the
unbound physical-volume insertion.

If volume and count are instead fundamentally constrained to be the same
single variable, that constraint and its coupling to the metric must be
derived in an action. One cannot then add a separate independent creation
chemical work and also count the full derivative as vacuum pressure. A
covariant constant-volume term is one possible completion, but not implied
by the number of states or the energy sequence.

Were the constant density above actually given the vacuum stress
`p=-epsilon`, with the same absolute matching and physical units derived,
it would predict `Lambda=8*pi*G*epsilon/c^4` and
`H_vac^2=8*pi*G*epsilon/(3c^2)`. The conditional scale could be fixed by
native coefficients and `v_cell`, rather than fitted as a new `C0`. At
present neither that volume calibration nor that stress follows from (7).

## 4. More occupied links at fixed N is a different experiment

The original fixed-N Hamiltonian has no node-creation term. It can change
link occupation, but `0<=M<=N^2`. With conventional link Pauli Y,

\[
\frac{d\langle M\rangle}{dt}
=\frac{h_N}{\hbar}\sum_e\langle Y_e\rangle,\qquad
|\dot{\langle M\rangle}|\le\frac{\Omega N}{\hbar}.     \tag{11}
\]

All other displayed bulk terms commute with each link occupation; ports
would add their explicit terms. In a finite closed held system this
expectation is a finite sum of energy-gap oscillations, with recurrences,
not an indefinitely increasing node count. Extra connectivity can also
shorten operational routes, rather than increase measured distances.

Declaring `V proportional to M` therefore neither reproduces the blank-pair
inclusion nor demonstrates physical expansion. It requires its own ruler,
clock and volume test. The new record-addition calculation confirms that
occupation, coherence and energy change differently; using any one as a
universal volume variable would ignore those native distinctions.

## 5. The minimal autonomous extension and decisive equations

A physically meaningful node-growth theory must put the different-N
sectors in one declared state space, rather than identify an external
sequence of calculations with time evolution. A schematic construction is

\[
\mathcal H=\bigoplus_N\mathcal H_N\otimes\mathcal H_{\rm supply},
\qquad
H_{\rm total}=\bigoplus_N H_N+H_{\rm supply}
 +\sum_N\gamma_N(\mathcal I_N\otimes B_N+
                 \mathcal I_N^\dagger\otimes B_N^\dagger).
                                                               \tag{12}
\]

Take real `gamma_N` and a finite declared number window initially, so the
expression does not assert an unproved infinite-sector operator domain.
An unbounded growth limit would need its own self-adjointness and energy
control. Equation (12) names the missing element; its supply operators, rates,
initial state and physical embedding are **not** derived or selected here.
The count-dependent diagonal Hamiltonian must implement the old-link
normalization change in (1). The creation channel must own the transition
energies and the nonzero off-subspace term (3), not discard either. Its
Hermitian reverse process remains present; permanent directed creation
would need a derived supply/history condition, not a deleted reverse term.

This narrow extension has discriminating, non-fitted targets:

1. Its first creation work moment must reproduce (1)--(2), with all record,
   carrier, source and switching energies retained. A closed autonomous
   realization conserves the total energy of (12), not just `H_N`.
2. Its actual creation current must satisfy
   `Ndot=i<[H_total,N]>/hbar`. Record copying alone changes R, not N;
   a relationship between the two must be generated by the specified
   interaction and initial state.
3. Its independently calibrated volume source must give the actual work
   `p=-<partial H_total/partial V>` under the stated variation, or derive
   the constrained covariant stress instead. One such independent source
   variation distinguishes the otherwise identical families (10).

Even under the proposed volume assignment and a valid physical time,
define `a proportional to <N>^(1/3)` only as a homogeneous coarse-grained
description with controlled count fluctuations. It obeys

\[
H=\frac{\dot N}{3N},\qquad
\frac{\ddot a}{a}=\frac{\ddot N}{3N}
 -\frac{2\dot N^2}{9N^2}.                            \tag{13}
\]

Thus accelerating expansion requires `3N Nddot>2 Ndot^2`. A constant
positive creation rate produces `a proportional to t^(1/3)` at late time
and decelerates; more cells alone is insufficient. No growth rate or
Hubble history is supplied by the fixed-N BS action.

The constructive target is now specific: **derive the number-changing
source, its absolute work and its operational volume stress in the same
network parent that already supplies record-dependent response**. The
baseline and normalization costs are known constraints, not free dark
energy. A successful completion could link local dynamics and uniform
expansion through one parent; claiming it now would skip the very
creation/volume equation which this derivation has isolated.

## Independent analytical check

The audit agent independently checked the inclusion identity, incident-pair
count, variational squeeze, edge-count bound and pressure/chemical-work
counterexample before this note was saved. The connected-graph probability
bound was supplied in that review. No numerical sample, parameter search
or passive replacement of an existing formed state was used.
