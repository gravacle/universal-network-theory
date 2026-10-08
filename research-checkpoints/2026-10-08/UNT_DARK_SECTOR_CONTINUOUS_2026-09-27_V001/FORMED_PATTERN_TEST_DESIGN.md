# Prospective formed-pattern test — 256-dimensional ceiling

2026-09-27. Design only: no numerical experiment has been executed for this
document. Freeze the choices below before a later implementation runs.

## Recommendation and source boundary

The next useful test is whether two arrangements of *actual writable registers*
produce different carrier/path responses after writing stops, with their
formed record counts and interaction energies independently checked. Use two
fixed-content writers and two initially blank record qubits, four dynamical
incidence bits, and one carrier on four labelled vertices. This is small enough
for a 256-dimensional formation calculation and exact 64-dimensional hold
blocks. It need not produce a successful matched arrangement comparison.

The resident sources inspected are
[Appendix B of the constructive adversarial review](../UNT_CONSTRUCTIVE_ADVERSARIAL_REVIEW_2026-09-27_V001.md)
and [the one-link implementation](../UNT_RECORD_TO_GEOMETRY_MINIMAL_JOIN_2026-09-27_V001/compute_join.py).
The original `MICRO_ACTION.md` is a dataless placeholder and was not read.
Consequently this document reconstructs a finite restriction from the resident
Hamiltonian equation and working one-link write operator; it does not certify
every convention or stability condition of the unavailable original action.

## Explicit new restriction

Label vertices `(L0,L1 | R0,R1)` and possible edges
`(00,01,10,11)`, where `ij` joins `Li` and `Rj`. No physical positions, lengths,
metric, or spacetime embedding are attached to these labels. An edge occupation
is `n_e=(I-Z_e)/2`, its flip is `X_e`, and

\[
d_v=\sum_{e\ni v}n_e.
\]

The carrier has basis `|L0>,|L1>,|R0>,|R1>` and exactly one conserved particle.
Define

\[
N_v=|v\rangle\langle v|,\quad
T_{uv}=|u\rangle\langle v|+|v\rangle\langle u|,\quad
J_{uv}=-i|u\rangle\langle v|+i|v\rangle\langle u|.
\]

Thus `J_e^2=N_u+N_v`, not the identity on the four-site carrier space. It
cannot be dropped or replaced by the one-link scalar simplification.

Each writable register has basis `|B>,|c>` and occupation `q=|c><c|`, with the
same fixed symbol `c` in both writers. Two target-location choices are

\[
W_P=(L0,L1),\qquad W_Q=(L0,R0).
\]

The familiar masks `P=(1,1|0,0)` and `Q=(1,0|1,0)` now label **write targets**,
not occupied post-write records. Write-target occupancy is not imposed at any
time. For pattern `M`, assign `q_v` to its corresponding writable qubit, or
zero for a nontarget vertex. Nontarget records stay in an invariant blank
sector because their writers are blank and no write term acts there.

The Hilbert space is

\[
\mathcal H=\mathbb C^2_{r_1}\otimes\mathbb C^2_{r_2}
\otimes(\mathbb C^2)^{\otimes4}_{a}\otimes\mathbb C^4_c,
\qquad \dim\mathcal H=256.
\]

Two writer registers in fixed `|c>` sectors are suppressed exactly. The
one-link operator `|c><c|_w tensor (|c><B|+|B><c|)_r` becomes `X_r` on this
sector. Omitting the other content symbol is a new fixed-content restriction,
not a demonstration of arbitrary-symbol readability or authenticated semantic
memory. The sources are externally prepared and writing is externally
switched. Positive record storage energy remains.

## Complete finite Hamiltonian

With tensor identities understood, use

\[
\begin{aligned}
H_M(g)={}&-h\sum_eX_e+\Delta\sum_en_e
+U_d\sum_{v}(d_v-d_*)^2
+\epsilon_\psi\sum_vN_v
+\epsilon_r\sum_vq_v+2\epsilon_w I\\
&-t_{\rm hop}\sum_{e=(u,v)}n_eT_e
+\lambda_J\sum_{e=(u,v)}n_eJ_e^2
-\lambda_R\sum_{e=(u,v)}n_e(q_u+q_v)
+g(X_{r_1}+X_{r_2}).
\end{aligned}
\]

All four vertex degree penalties appear once. Do not sum a complete endpoint
penalty independently for every edge, which would double count it on this
graph. As a direct audit against Appendix B, isolating incidence bit `e` gives

\[
F_e=\Delta+U_d[2(d_u^{(\neg e)}+d_v^{(\neg e)})+2-4d_*]
-t_{\rm hop}T_e+\lambda_JJ_e^2-\lambda_R(q_u+q_v),
\]

in `H=-hX_e+n_eF_e+H^(e)`. This recovers the documented edge equation. The
carrier storage term equals `epsilon_psi I` in the one-carrier sector, but it
stays in the energy ledger. The two writer energies are retained symbolically,
even though the inherited coefficient is zero.

Inherit the one-link numerical values exactly:

| Parameter | Value |
|---|---:|
| `h, U_d, d_star, epsilon_psi, epsilon_r` | 1 each |
| `Delta` | 4 |
| `epsilon_w` | 0 |
| `t_hop, lambda_R` | 0.5 each |
| `lambda_J` | 0.25 |
| `g` during writing / hold | 1 / 0 |

No rescaling by graph degree is introduced. Finite-dimensional Hermiticity
implies a bounded spectrum here; this does not verify the unavailable parent
action's wider stability domain or any large-system limit.

## Native preparation, fixed schedule, and accounting

Both arrangements start from

\[
|\Psi_0\rangle=|B,B\rangle_r\otimes|0000\rangle_a\otimes|L0\rangle_c.
\]

Evolve with `H_M(1)` for duration 1. Keep the entire resulting pure state,
including the blank, singly written, and doubly written amplitudes and all
their correlations. Source-off hold uses `H_M(0)`, with no measurement,
postselection, repinning, reset, or removal of a state component. A pure global
state is consistent with keeping all outcomes; no writing result is selected.

Read hold times `0, .25, .5, 1, 2`; primary endpoint is **1**. Numerical
tolerance is `1e-11`; an effect requires absolute size greater than `1e-10`
and all checks passing. There is no parameter/time fit or adaptive extra time.

Initially both total energies are exactly

\[
E_0=4U_dd_*^2+\epsilon_\psi+2\epsilon_w=5.
\]

Writing-on expectation work is zero in the blank preparation. Writing-off work
is

\[
W_{\rm off,M}=-g\langle X_{r_1}+X_{r_2}\rangle_{\Psi_M(1)}.
\]

Report every Hamiltonian term before and after switching and throughout hold,
with `E_hold,M=5+W_off,M`. Equal initial energy and two equal writing durations
do **not** imply equal formed energy, formed occupation, or switching work.
The storage counts commute with the hold generator; the interaction energy
itself generally need not be constant during hold.

## Predeclared comparability gate

Independently calculate for each arrangement at hold zero:

1. Both site record means and total formed mean `R=<q_r1+q_r2>`; the full
   unconditioned count probabilities for counts 0, 1, and 2; the complete
   two-record reduced density; and blank/correct-symbol probabilities.
2. All edge means, degree statistics, carrier probabilities, and the complete
   incidence/carrier state needed for cross-checks. Initial carrier and network
   states after writing need not match across arrangements.
3. Total hold energy, record storage energy, interaction energy
   `E_R=-lambda_R sum_e <n_e(q_u+q_v)>`, and external writing-off work.

An arrangement contrast can be described as matched in mean count and energy
only if the separately calculated differences in **R, total hold energy, and
E_R** are each at most `1e-10`, after numerical checks pass. Equal numbers of
writing targets are insufficient. If any gate fails, retain and report all
outputs as a mismatched native formation comparison; do not claim to have
isolated arrangement from record count or interaction energy. No normalization
by formed count, time adjustment, parameter adjustment, or successful-sector
selection may repair the gate in this experiment.

Also report discrepancies in the complete count distribution and other energy
terms. Matching the three means alone does not equalize energy distributions,
all correlations, or all possible material explanations; it licenses only the
stated limited comparison. A failed gate is a useful preparation result, not
permission to manufacture matched histories or discard the test.

## Exact graph-walk diagnostic and its native-state limitation

For either hold Hamiltonian define carrier blocks

\[
K_{vu}(\tau)=\langle v|e^{-iH_M(0)\tau}|u\rangle,
\]

which act on records and incidences. Consider the opposite same-side vertices
`u=L0, v=L1`. They have two two-edge paths. Put

\[
A=n_{00}n_{10},\quad B=n_{01}n_{11},\quad S=A+B.
\]

There is no direct `L0`–`L1` hop. Only two carrier-hopping factors can connect
them in `H^2`; all storage, write-off, degree, current-squared and incidence-flip
terms are carrier diagonal. Therefore the exact leading operator identity is

\[
K_{L1,L0}(\tau)=-\frac{t_{\rm hop}^2\tau^2}{2}S+O(\tau^3),
\qquad S^2=A+B+2AB.
\]

The `2AB` term is coherent two-route interference and uses the four-edge
occupation correlation. It cannot generally be inferred from four independent
edge means. Freeze this identity as an independent operator audit, including
the normalization `1/2` and the current-squared term's diagonality.

If a carrier were separately prepared at `L0` with network state `sigma`, the
resulting probability would begin

\[
p_{L1}(\tau)=\frac{t_{\rm hop}^4\tau^4}{4}
\operatorname{Tr}(\sigma S^2)+O(\tau^5).
\]

That is a conditional statement about a **different preparation**. The actual
post-write carrier is generally correlated and already spread across vertices.
Do not reset it, postselect `L0`, or identify this fresh-carrier expression with
the native hold probability.

Instead retain every subnormalized post-write carrier block
`rho_ij=<i|rho_M|j>` and use the exact unconditioned relation

\[
p_v(\tau)=\sum_{i,j}\operatorname{Tr}
\left[K_{vi}(\tau)\rho_{ij}K_{vj}(\tau)^\dagger\right].
\]

The `i=j=L0` block contributes
`t_hop^4 tau^4 Tr(rho_L0,L0 S^2)/4` at order four for `v=L1`, but all other
blocks and cross terms remain in the total. These are algebraic summands, not
selected experimental outcomes. For a second independent short-time check,
predict derivatives `k=0,1,2,3,4` directly from

\[
D_{k,v}=i^k\operatorname{Tr}
\left[\rho_M\,\operatorname{ad}_{H_M(0)}^k(N_v)\right],
\qquad p_v(\tau)=\sum_{k=0}^4D_{k,v}\tau^k/k!+O(\tau^5).
\]

Compare these derivatives with the fully inclusive block expansion, without
fitting finite-difference coefficients. At the primary time 1 use exact hold
evolution; the fourth-order truncation has no claimed accuracy there.

Report the unconditioned incidence descriptor
`W=<S^2>=<A>+<B>+2<AB>` for each actually formed state and the actual `L1`
probability change from hold zero, together with all four carrier occupations.
This tests whether a native incidence-path description correctly participates
in predicting carrier dynamics. It is an internal geometry-related check,
not an independently established physical metric or force law. Do not import
Appendix B's pinned-storage `lambda_R^2/(8h^2)` contrast into these formed,
correlated states; its preparation and averaging assumptions differ.

## Controls and bounded future implementation

Use one sequential numerical worker with single-thread BLAS/OpenMP, no SciPy,
no remote work, no installations, maximum dimension 256, a 30-second wall
alarm and 30-second CPU limit. If the bound is hit, stop and preserve the
partial diagnostic; do not increase the limit or launch additional workers.
This document authorizes no execution by itself.

Suggested implementation architecture:

- Build all basis indices explicitly, assemble the full Hamiltonian from its
  separate terms, and audit the edge-wise `F_e` expansion and `J_e^2` identity.
  Form each native pure state with a Hermitian eigensolver. Independently check
  vector propagation with a scaled Taylor action, rather than a second shared
  diagonalization. Do not allocate a larger Hilbert space for spectator writers.
- During hold, decompose the *same* 256-vector into four unnormalized record
  sectors, evolve their 64-vectors with their exact conditional Hamiltonians,
  and retain all storage phases. Reassemble for complete-state checks and
  sum all sectors for carrier/incidence observations. Cross-record coherences
  are retained when evaluating record density, never silently dephased.
- **Feedback-zero whole-schedule control:** set only `lambda_R=0` for writing
  and hold. The locations decouple from record dynamics and both arrangements
  must have identical active states and formed count statistics, after mapping
  the two record labels. The identical record evolution is analytically the
  product of two one-link two-level write evolutions. All other terms remain.
- **Feedback-zero hold-only control:** for each pattern copy its complete main
  post-write state and remove only hold feedback. Report added switching work
  `+lambda_R sum_e <n_e(q_u+q_v)>`. Cross-pattern equality is not expected here:
  the native formation differences persist in the starting states.
- As a construction-level negative check, setting `t_hop=0` makes each `N_v`
  commute with the generator even with current-squared feedback present. An
  additional numerical sweep is unnecessary for this exact identity.

Required checks: Hermiticity, norms, complete density positivity when assembled,
record-population retention on hold, separate write/hold energy conservation,
the external work ledger, whole-schedule feedback-zero equality, full-versus-
block holds, and the short-time carrier identities above. Report each arm and
every frozen time, including null results and sign changes. Source/protocol
hashes must precede execution, and successful outputs must be retained.

Even a successful matched comparison establishes only native formation,
retention, and arrangement-dependent response inside this assumed finite
Hamiltonian. It supplies no dark-sector abundance, cosmological expansion,
gravity, universal matter/clock coupling, metric reconstruction, equivalence
principle, continuum limit, or evidence against ordinary interacting quantum
matter. Those are missing physical claims, not conclusions licensed by this
test.
