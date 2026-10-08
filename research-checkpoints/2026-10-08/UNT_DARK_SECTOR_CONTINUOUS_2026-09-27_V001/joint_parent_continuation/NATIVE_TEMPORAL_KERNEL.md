# Native charges, temporal response, and the missing clock functional

2026-09-28. Analytical continuation of the resident BS seed and the actual
held two-band model. No new numerical worker, equilibrium replacement,
clock action, physical-volume assignment, or source contact is adopted.

## Decision

The native model already supplies **record-production currents and
state-dependent record-addition energies**. Those are useful ingredients
for an emergent clock/matter response, not arbitrary phenomenological
parameters. But neither a conserved carrier count nor a frozen record count
alone determines the homogeneous clock function `K(Q)`.

There is a precise distinction. A uniform source coupled to an exactly
conserved charge has zero connected retarded charge response in the closed
system. A collective phase action can nevertheless arise from an owned
energy-versus-density family, with its pressure obtained by a Legendre
transform. These are different response questions and different limiting
procedures. The native source/volume/phase identification needed for the
second construction has not yet been supplied.

The narrow next datum is therefore the **complete adjacent-record-sector
addition spectrum and its second difference at fixed calibrated volume,
with the actual formation population and phase reference retained**. The
algebra below both constrains that calculation and shows why substituting
the lowest link band would change its answer.

## 1. Exact native charges and the record-production ledger

Resident inputs read in full: `recovered_sources/BS_MICRO_ACTION.md`,
`TWO_BAND_ANALYTICAL_BRIDGE.md`, `NATIVE_TWO_CHANNEL_CLOCK_SCREEN_V001.md`,
`joint_parent_continuation/NATIVE_SOURCE_BRIDGE_DECISION.md`, and the
conditional clock/FLRW notes. BS04--BS12 define the Hamiltonian used here.
The following statements concern the ports-off bulk. A port not commuting
with a displayed charge contributes its explicit commutator.

For carrier occupation and content counts,

\[
N_\psi=\sum_v q^\psi_v,\qquad
N_{\psi,x}=\sum_v |x\rangle\langle x|^\psi_v,\quad x=0,1,
\]

every listed bulk term commutes with each total. Transfer preserves the
content while moving an occupied carrier; carrier-to-record copying uses
the carrier only as a diagonal control. The current-squared term also
preserves these counts. Writer content projectors are individually
conserved spectators in this bulk Hamiltonian. These conservation laws
continue across the scheduled slabs when the counts include all nodes and
the applied ports preserve them.

In contrast the retained-record count

\[
R=\sum_v q^r_v
\]

is not conserved during native formation. Define the Hermitian copy current

\[
Y_{a\to b}=i\sum_{x=0}^1|x\rangle\langle x|_a\otimes
 (|B\rangle\langle x|-|x\rangle\langle B|)_b.
\]

With the native sign `+g K`, direct finite-matrix commutation gives

\[
[K_{a\to b},q_b]=-iY_{a\to b},\qquad
\boxed{\frac{d\langle R\rangle}{dt}
=\frac1\hbar\sum_v\left[
g_{\psi r}\langle Y_{\psi_v\to r_v}\rangle+
g_{wr}\langle Y_{w_v\to r_v}\rangle\right].}           \tag{1}
\]

Record-to-reservoir copies commute with record count because the record is
their control, not their target. Noncommuting ports add
`i<[H_port,R]>/hbar` to (1). Thus the produced count is the initial count
plus the integral of an actual coherent source current. It is not an
independent abundance parameter. The Hermitian copying dynamics does not
make this current nonnegative at all times.

Since each `Y` has norm at most one, residual record-target couplings obey
the state-independent drift bound

\[
|\langle R(t)\rangle-\langle R(0)\rangle|
\le\frac1\hbar\int_0^t ds\sum_v
(|g_{\psi r}(s)|+|g_{wr}(s)|),                         \tag{2}
\]

with the port bound added when needed. This can qualify approximate charge
retention over a specified physical interval; it does not create an exact
chemical-potential symmetry while copying remains active.

When the record-target copies are switched off, every local `q^r_v`
commutes with the held bulk Hamiltonian, even if the listed record-controlled
reservoir copies remain. The independent phase twists

\[
U_\theta=\exp(i\sum_v\theta_v q^r_v)
\]

then commute with `H_hold`. Their energy cost is exactly zero for any held
state. Frozen record occupation by itself therefore has no static
record-phase twist stiffness. This is stronger than merely conserving total
record number. It does not exclude a collective phase involving carriers,
links and explicit controller processes: carrier transfer, for example,
preserves its total charge but not every local carrier charge.

The discrete content swap BS02 is not a continuous clock symmetry. Likewise
constant band populations in a fixed finite Hamiltonian are not automatically
an extensive local Noether charge or a physical proper-time variable.

## 2. A native temporal sum rule, and an exact hold null

For the diagnostic source `H(f)=H0-f R`, use the same retarded convention as
the incidence-source note,

\[
\chi_{RR}(t+\tau,t)=\frac{i}{\hbar}\theta(\tau)
 \langle[R(t+\tau),R(t)]\rangle.
\]

The equal-time double commutator is

\[
\boxed{[R,[H,R]]=-\sum_v\left[
g_{\psi r}K_{\psi_v\to r_v}+g_{wr}K_{w_v\to r_v}\right].} \tag{3}
\]

The second commutator acts only on the record target. Therefore, for the
actual possibly nonstationary state,

\[
\boxed{\partial_\tau\chi_{RR}(t+\tau,t)|_{0^+}
=-\frac1{\hbar^2}\sum_v\left[
g_{\psi r}\langle K_{\psi_v\to r_v}\rangle_t+
g_{wr}\langle K_{w_v\to r_v}\rangle_t\right].}         \tag{4}
\]

Its sign is an actual-state question, not a passive-state assumption. This
is the record/temporal counterpart of the incidence strength
`h_N sum v_e^2<X_e>/hbar^2`; the operators and mechanisms differ. Ports add
their own double commutator to (3)--(4). In the held record sector the full
retarded record-density response is zero, not just its initial slope:
all the local record occupations are constants and mutually commute.

More generally, suppose `[H0,C]=0` for an exact charge `C`, and impose only
`H_mu(t)=H0-mu(t) C`. Then

\[
\chi^R_{CC}(t,t')=0.                                  \tag{5}
\]

This holds for any initial state, including coherences between charge
sectors. The source changes their relative phases, not their probabilities.
The finite-time closed-time-path functional can be evaluated exactly:

\[
Z[\mu_+,\mu_-]
=\operatorname{Tr}\rho\exp\left[
 \frac{iC}{\hbar}\int dt(\mu_+-\mu_-)\right].           \tag{6}
\]

It depends on the difference source and not on the common physical source.
Writing `I_Delta=integral(mu_+-mu_-)dt`,

\[
-i\hbar\log Z
=\langle C\rangle I_\Delta+
 \frac{i}{2\hbar}\operatorname{Var}(C) I_\Delta^2+\cdots. \tag{7}
\]

Charge variance here is a difference-source/noise cumulant, not a retarded
kinetic coefficient. In the stationary Lehmann representation all
nonzero-gap matrix elements of `C` vanish; degeneracies do not change (5).
A time-dependent basis change `exp(i theta C)` can produce the term
`-hbar thetadot C` in the transformed Hamiltonian, but transforming the
state and readout as well does not manufacture a new physical clock source.

Consequently longer source-free hold evolution cannot turn this particular
zero kernel into an owned homogeneous `K`. BS21--BS23 permit a Legendre
transform only on an invertible retained quotient; a conserved null
response is not to be inverted by hand.

## 3. Real native addition energies, including a curvature discriminator

The already solved held block is

\[
H_q=C_qI-hX_a+(b_q-jX_C)n,\qquad
h=1,\quad j=\tfrac12,\quad C_q=3+q,\quad b_q=\tfrac94-\tfrac12q.
\]

At fixed carrier-X eigenvalue `s=+/-1`, its lower/upper link energies are

\[
E_{\beta s}(q)=C_q+\frac{b_q-js+
 \beta\sqrt{(b_q-js)^2+4h^2}}2,\qquad\beta=\pm1.
\]

The same-labelled-branch record-addition costs are exactly

\[
\boxed{\begin{aligned}
\Delta E_{\beta,+}&=\tfrac34+
 \tfrac\beta8(\sqrt{89}-\sqrt{113}),\\
\Delta E_{\beta,-}&=\tfrac34+
 \tfrac\beta8(\sqrt{145}-\sqrt{185}).
\end{aligned}}                                         \tag{8}
\]

All four lie strictly between `1/2` and `1` in the inherited energy units.
The operator identity `H_1-H_0=I-n/2` gives the non-strict bounds directly
by the min--max principle. The lower branch costs more than `3/4`, while
the upper costs less. These are owned record addition energies with link
binding retained, not the bare storage gap alone.

Equation (8) is not the whole spectrum of a record-raising readout. Such a
readout also connects different link branches with the corresponding state
overlaps; the actual formed density matrix fixes its amplitudes. A carrier
or controller phase reference and an allowed preparation/readout are needed
to observe a charge-sector relative phase. The finite qutrit does not have
an exact canonical angle satisfying `[theta,q]=i I` (the finite trace of a
commutator is zero).

There is also an exact prospective curvature test directly within the BS
hold family, requiring no spectrum computation. In a two-node, one-link
reduction with both endpoint records retained, all formation copies and
ports off, fixed carrier count and fixed carrier-X branch, let their total
occupation be `R=0,1,2`. The same native terms give

\[
H_R=C+\epsilon_r R-hX+
 (b-\lambda_R R-js)n.
\]

Here `C,b` include the common record-independent terms; no new record
interaction has been added. Put `d(x)=sqrt(x^2+4h^2)` and `x=b-js`. Then

\[
\boxed{E_\beta(2)-2E_\beta(1)+E_\beta(0)
=\frac\beta2[d(x-2\lambda_R)-2d(x-\lambda_R)+d(x)].}  \tag{9}
\]

Since `d''(x)=4h^2/d(x)^3>0`, this is strictly negative in the lower link
branch and strictly positive in the upper branch for `h,lambda_R>0`.
Equivalently a formal continuous detuning gives
`d^2 E_beta/dR^2=2 beta h^2 lambda_R^2/d(x-lambda_R R)^3`.
The finite difference (9), not the formal continuous coordinate, is the
native discrete statement. It is a symbolic comparison of the stated
three-sector hold restriction, not a new preparation or a claim that the
existing formed state occupies these sectors with prescribed weights.

Thus lower-band relaxation alone favors successively cheaper record
addition in this local motif. Treating that branch as an already stable
uniform positive-compressibility fluid would be unjustified. Correlated
geometries, other retained modes, actual excited populations and explicit
source work can change a collective equation of state; they must be kept.
The sign result is a sharp state/sector discriminator, not an exclusion of
the full network theory. Bare `epsilon_r>0` by itself never fixed the full
many-record addition energy, which also depends on incident links.

For implementation, the existing frozen 36-dimensional join has only one
active record qutrit: its occupied contents both have `q=1`, not `q=1,2`.
The three-count comparison in (9) requires an explicit second endpoint
record factor from BS. It is not an analytic continuation of that qutrit's
occupation. Keeping the inherited writer qutrit as well would give 108
states; a declared fixed-content invariant restriction can be smaller.
The inherited coefficients give, in that two-endpoint hold restriction,

\[
H_R=(3+R)I-X_a+(\tfrac94-\tfrac12R)n
       -\tfrac12 nX_C,\qquad R=0,1,2.                  \tag{9a}
\]

All endpoint/configuration/content multiplicities remain. The currently
stored formed state supplies no nonblank second-record population. A new
formation protocol would have to declare that register, its local writer
and initial state explicitly before scoring its actual populations.

For any specified full formed state, a ground replacement is unnecessary.
With `x_Rs=9/4-R/2-s/2`, `d_Rs=sqrt(x_Rs^2+4)`, the link/carrier projectors
at fixed count are

\[
P_{\beta s}(R)=
\frac{I-\beta(2X_a+x_{Rs}Z_a)/d_{Rs}}2\otimes
\frac{I+sX_C}2.
\]

If `Pi_R` is the complete count projector, retain every weight
`w_R,beta,s=Tr(rho_formed Pi_R P_beta,s)`; then
`<H_hold>=sum w_R,beta,s E_beta,s(R)` exactly. Cross-record coherences
do not enter that diagonal energy but remain essential to a phase readout.
An instantaneous record addition with unchanged link/carrier state has
energy change `1-<n>/2`, not generally the followed-band gap (8).
The latter includes the change of link eigenstate. Preparation, switching
and controller work distinguish the two experiments; their energies cannot
be interchanged when constructing a density functional.

## 4. What a legitimate phase/clock Legendre construction would require

Equation (5) does **not** prove that an exactly conserved charge can never
support a collective phase action. A fixed-charge connected retarded
response, an equilibrium compressibility across charge sectors, and a
one-particle-irreducible phase action are not the same object. Their
thermodynamic, zero-wavenumber, zero-frequency and equilibration limits
must be declared. No equilibrium bath is part of the existing hold simply
because a grand potential can be written down.

For a fully specified finite volume and complete sector energies
`E_{c,alpha}(V)`, the passive zero-temperature grand potential is

\[
\Omega(\mu,V)=\min_c[E_c(V)-\mu c].                    \tag{10}
\]

It is piecewise linear and concave, with charge plateaus and crossings;
a single finite gapped block does not generically produce a smooth
quadratic clock functional. At an independently justified thermal energy
`Theta=k_B T>0`,

\[
\Omega_\Theta=-\Theta\log\sum_{c,\alpha}
e^{-[E_{c,\alpha}(V)-\mu c]/\Theta},\qquad
-\partial_\mu^2\Omega_\Theta=\operatorname{Var}(C)/\Theta\ge0. \tag{11}
\]

This changes sector populations under the chosen ensemble and is not the
zero retarded response of the original isolated preparation. The actual
formed state is not established as either ensemble in (10)--(11).

If a native limiting state and operational volume actually supply a smooth
convex energy density `epsilon(n)`, then the constructive relation is

\[
P(\mu)=\sup_n[\mu n-\epsilon(n)],\quad
\mu=\epsilon'(n),\quad n=P'(\mu),\quad
P''(\mu)=1/\epsilon''(n)>0.                            \tag{12}
\]

This is a derivation from the specified density family, not permission to
choose `P` to fit a background. Metastable active ensembles require their
own fixed-state functional and stability test instead of replacing their
populations with the supremum in (12).

Under the **additional** owned phase/metric identification
`mu=m_0 Q`, where `Q=sqrt(-partial T squared)` in `c=1` units and `m_0`
is the independently calibrated energy per unit clock rate, the convention
of the adopted covariant interface would read

\[
M^2 K(Q)=P(m_0Q),\quad M^2=(8\pi G)^{-1},\qquad
\rho_K=M^2(QK_Q-K)=\epsilon(n),\quad p_K=P.             \tag{13}
\]

The familiar conditional clock conservation law is then just

\[
a^3K_Q=I_0=\frac{m_0}{M^2}a^3 n.                     \tag{14}
\]

It is the same comoving physical charge, not a second freely tunable
population. If native production (1) is active, the corresponding current
has its derived source; constant `I_0` is no longer automatic. All source,
controller and reservoir energy must be included in the stress once.

For this single isentropic phase description, where justified, the sound
coefficient would be

\[
c_s^2=\frac{P'}{\mu P''}=\frac{n\epsilon''(n)}\mu.     \tag{15}
\]

The inherited lower-branch curvature in (9) illustrates why its sign needs
derivation. An exactly linear dust energy `epsilon=m n` has zero curvature
and a singular Legendre relation, not a generic smooth finite `K_QQ`.
An approximate pressureless regime would require a native positive
rest-energy term dominating a small, stable interaction pressure over an
owned state/volume window.

Equations (13)--(15) state only the necessary conditional mapping, using
the `K` convention already read in
[Blanchet and Skordis (2024), sections 2 and 4](https://arxiv.org/html/2404.06584v2).
They do not identify a BS register phase with that covariant clock. The
earlier two-channel native spectrum already excludes a pure common lapse
rescaling with fixed intrinsic dispersions; a broader composite clock must
account for that exact result as well.

## 5. Nonidentifiability and the single smallest useful native bridge

BS05 supplies a boundary-clock calibration, while BS12 and BS20a leave the
complete physical source/controller, volume map and contacts to be
instantiated. None is fixed by a conserved count or by copying alone.
For a proposed physical temporal source, adding `c mu^2 I/2` to its
Hamiltonian preserves the source-free Hamiltonian, first charge insertion
and every normalized prescribed-source trajectory, but changes the
absolute temporal source-work curvature. As in the incidence audit, this
exhibits an unbound physical-completion slot; it does not authorize adding
a contact to the frozen diagnostic `H0-mu C`, whose contact is exactly zero.
A complete source/phase/controller variation can distinguish these cases.

Even a determined finite charge-sector spectrum does not provide its
physical-volume dependence, a smooth density limit, or a readout defining
the spacetime clock. There is consequently no unique native `K(Q)` from
the present evidence. This is narrower than saying that UNT cannot produce
one, or that any desired function can be appended without a test.

The next useful native calculation is a **record-addition/phase-response
experiment, not more propagation of an unchanged hold**:

1. Keep one common geometry, full Hamiltonian/controller and physical
   volume convention; retain at least three adjacent record-count sectors
   and all populated link/carrier branches. Derive the allowed record
   addition lines and the second addition difference. Equation (9) is an
   exact local check, not a replacement for the actual state.
2. Use the existing copying current and frozen preparation to fix sector
   weights, rather than fitting them to a desired dust abundance. If a
   charge-sector phase is to be read, supply its explicit writer/controller
   reference and include that source's complete work. For a mobile
   collective charge, compare the small nonzero-wavenumber temporal
   response before taking any hydrodynamic limit; the exactly uniform
   conserved-charge null must remain intact.

These are two parts of one discriminating bridge: **does the actual native
record ensemble own a stable energy-versus-density curvature and a usable
relative phase, with the same source/volume calibration?** The symbolic
local answer already warns against selecting the lower band; the full
formed-state answer is not known from the stored response spectra alone.

The ordinary carrier charge cannot be counted twice. Its carrier onsite
energy, transport energy and binding already belong to the parent's matter
ledger. Rebranding the same `m n` as an additional clock fluid would add
energy without a new native difference. A distinct record contribution
must instead come from its actual incremental energy, binding and owned
production/current history, as constrained above.

Finally, the `K=0` FLRW result remains unchanged: its existing linear
`a^-3` clock-density perturbation is signed with zero bulk mean under the
stated boundary conditions, whereas the leading weak averaged clock excess
is radiationlike. Neither is the positive dust background of (13)--(14).
Such a background must be derived from a real population and its complete
stress, not inferred merely from a matching power of `a`.
