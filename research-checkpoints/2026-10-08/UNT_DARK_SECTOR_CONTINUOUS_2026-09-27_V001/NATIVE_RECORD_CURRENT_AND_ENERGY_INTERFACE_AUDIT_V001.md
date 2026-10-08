# Native record continuity and the material/energy-current interface

2026-09-27. Focused analytic audit, not a new microscopic law, physical
motion claim, numerical run, or universal record-fluid no-go.

Resident flags were checked before reading the relevant BS06--BS12 source
and the complete `NATIVE_SOURCE_RESPONSE_SCALING_V001.md` and
`NATIVE_RECORD_ANCHORED_CARRIER_ACCESS_V001.md`. The recovered source is
`recovered_sources/BS_MICRO_ACTION.md`, SHA256
`00eba581b90fb9f0b25e3fad1362b055049824897433ba06e356ab9b1f6c76ec`.
`NATIVE_FIXED_SOURCE_CARRIER_CURRENT_V001.md` and
`I0_NATIVE_COMPLETE_EXCESS_WORK_V001.md` were compressed,dataless and skipped
without hydration. No conclusion below depends on rereading those files.

## 1. What the native Hamiltonian conserves at each register

In a source-off hold with all formation couplings g=0 and ports absent or
separately verified to preserve the occupations,

\[
 [H,q_v^r]=0\quad\hbox{for every vertex }v.             \tag{1}
\]

This is stronger than conservation of their sum. BS06 acts on links; BS09
transfers **psi carriers**, not retained r registers; BS11 contains only
the diagonal record occupation in
-lambda_R sum_e n_e(q_u^r+q_v^r). The storage terms are diagonal as well.
There is no native bond operator T^r_uv transferring an occupied retained
register into a neighboring blank register.

The Hamiltonian bond-current commutator for q_v^r is therefore identically
zero on every edge. All joint retained-occupation probabilities are fixed
during the hold, for arbitrary initial correlations and coherences. Writing
an artificial divergence-free current into a continuity equation would not
create the missing occupation-transfer matrix elements.

During native formation the only occupation-changing contributions are
local targets:

\[
 \dot q_v^r=\frac{i}{\hbar}
 \left[g_{\psi r}K_{\psi_v\to r_v}
       +g_{wr}K_{w_v\to r_v},q_v^r\right].             \tag{2}
\]

Copying r_v into its local reservoir fragments commutes with q_v^r.
Equation (2) is a local writing/reversal source, not a bond record current.
The copy control is not depleted, so local writing cannot be interpreted
as conservation of one shared carrier-plus-record occupation count.

## 2. The existing transported charge is the carrier occupation

Orient an edge e from u to v as in BS07. Direct commutation of BS09 gives

\[
 I^\psi_{u\to v}=\frac{t_{\rm hop}}{\hbar}n_eJ^\psi_{uv},
 \qquad
 \dot q_v^\psi=\sum_{e\,\mathrm{into}\,v}I_e^\psi
              -\sum_{e\,\mathrm{out\ of}\,v}I_e^\psi. \tag{3}
\]

This is an operator continuity equation, not a mean-link approximation.
The current-squared term contributes no direct occupation current because

\[
 (J^\psi_{uv})^2=q_u^\psi+q_v^\psi-2q_u^\psi q_v^\psi
\]

commutes with each endpoint occupation. It can nevertheless change later
current evolution. The native local copy K_(psi->r) also commutes with
q^psi because psi is its control, so (3) remains valid with those formation
couplings on, in the absence of additional carrier-changing ports.

Thus the source already owns mobile content-bearing carriers which can
write records locally and provide record-conditioned transport readouts.
It does not identify that mobile carrier charge with the retained-record
charge in (1). Nor does it include a bulk r->psi copy/emission operator:
using an old retained record as a newly mobile carrier source would require
an owned additional port or interaction.

The resident anchored-access calculation illustrates this distinction:
carrier access changes even though every retained q_v^r stays fixed.
Its two admissible opposite bias signs also show that feedback alone does
not imply a universal attractive response.

## 3. Exact energy exchange exists without record-number transport

An explicit complete hold partition is

\[
 h_v=U(d_v-d_*)^2+\epsilon_\psi q_v^\psi
        +\epsilon_rq_v^r+\epsilon_wq_v^w
        +\sum_k\epsilon_{bk}q_v^{b_k},
\]
\[
 h_e=-h_NX_e+\Delta n_e-t_{\rm hop}n_eT_e^\psi
       -\lambda_Rn_e(q_u^r+q_v^r)+\lambda_Jn_e(J_e^\psi)^2,
 \qquad H=\sum_vh_v+\sum_eh_e.                        \tag{4}
\]

For any such declared Hermitian term assignment H=sum_alpha h_alpha,
define the Hermitian energy-transfer operator

\[
 I^E_{\alpha\to\beta}=\frac{i}{\hbar}[h_\alpha,h_\beta]
       =-I^E_{\beta\to\alpha}.
\]

Then, exactly,

\[
 \frac{d}{dt}\langle h_\beta\rangle
 =\left\langle\partial_t h_\beta\right\rangle
       +\sum_\alpha\langle I^E_{\alpha\to\beta}\rangle. \tag{5}
\]

All internal transfers cancel in the total. Explicit switching contributes
work through partial_t h_beta, and any ports must be retained once.
Degree terms in (4) act on whole graph stars, so this is an exact
term-overlap energy ledger, not already a physical spatial flux law.

Two specific pieces expose what moves:

- Bare record storage epsilon_r q_v^r commutes with every hold term. Its
  energy does not move or change in this hold.
- In an alternative allocation, assign each endpoint's complete feedback
  once to its record and define
  E_v^r=q_v^r(epsilon_r-lambda_R d_v). Remove those same terms from (4)
  before using this alternative; it is not an extra energy contribution.
  Since dot n_e=(h_N/hbar)Y_e,

\[
 \frac{d E_v^r}{dt}
 =-\frac{\lambda_Rh_N}{\hbar}q_v^r
                  \sum_{e\,\mathrm{incident}\,v}Y_e.  \tag{6}
\]

This interaction share exchanges energy directly with the incidence-flip
term. It commutes directly with both carrier hopping and current-squared
feedback. Carriers can affect its later evolution through the full coupled
state, but (6) is not a record-energy current carried by hopping records or
a direct carrier transport of this chosen energy share.

Bare carrier onsite energy, in contrast, has the continuity contribution
epsilon_psi I_e^psi from (3). That is only one part of the full energy
ledger: bond, current-feedback, degree and storage-interaction energies
must not be discarded. A native onsite gap is also not yet an identified
inertial or gravitational mass.

Redistributing bond energy between endpoint assignments changes local
energies and their currents while leaving H and its exact total balance
unchanged. A physical regional energy flux needs an owned boundary,
deformation/transport interface and allocation convention. Equation (5)
is a concrete computable starting point, not a uniquely defined stress
tensor or material current.

## 4. Fixed register labels do not prove zero physical motion

The BS labels are composition-layer labels, not supplied material worldlines.
If a separate same-parent map derives physical cell worldlines X_v(tau),
a fixed q_v^r can be advected with its cell. For example, such a map would
permit a distributional record current

\[
 j_r^\mu(x)=\sum_v q_v^r\int d\tau\,
 \dot X_v^\mu(\tau)
 \frac{\delta^{(4)}(x-X_v(\tau))}{\sqrt{-g(x)}}.        \tag{7}
\]

Constant weights make this current divergence-free away from worldline
endpoints, despite zero inter-register hopping. Equation (7) is conditional
on the missing physical map; it is not extracted from label order.

Likewise a derived material cell volume V_v would allow
n_v=<q_v^r>/V_v and, in a hold, dot n_v=-n_v dot V_v/V_v.
To turn that algebra into a continuum material continuity equation one
must identify the moving/glued cell boundaries, their velocity and the
physical clock/metric. A changing incidence pattern, scalar F, or a
geometry from another parent cannot silently supply those identifications.
This permits a comoving interpretation when earned; it neither proves
physical immobility nor already establishes comoving dust, mass or pressure.

## 5. Constructive disposition

The listed terms supply a transported **carrier** current and an exact
complete energy ledger. They do not yet supply the transported retained-
record material current assumed by the one-density A/M perturbation test.
There are two distinguishable next interfaces:

1. Test an active component built from the already mobile psi sector,
   retaining its hopping, feedback and interaction energies. Derive its
   long-scale dispersion and complete stress rather than identifying it
   with r storage or calling its bare gap a dust mass.
2. For retained-record matter, derive an advected-cell/worldline map or
   explicitly own a record-transport/formation mechanism. Then check its
   number source, energy exchange and stress against the A/M equations.

Neither route is a general network-fluid no-go. The present native hold
does, however, supply exact controls: retained count has no growth, bare
record storage has no current, and record-conditioned carrier response
need not have an attractive sign. Consequently these terms alone do not
derive a low-acceleration scale, flat rotation curve, or record-growth-driven
cosmic acceleration. The user’s broader proposal must be tested through
the missing owned current/stress/geometry interface, not rejected or
accepted merely from the persistence of local register labels.
