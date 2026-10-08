# Native source bridge: what is fixed, and the smallest remaining variation

2026-09-28. Analytical continuation using resident source files only. No new
physical worker, source rule, fitting, or change to sealed evidence.

## Decision

The original BS record equations do constrain more than an arbitrary spectral
ansatz: **their link-flip coherence fixes an exact source-response moment**.
This supplies a native oscillator-strength normalization, and a possible
inertial-scale matching condition for the mechanical comparison parent. It
holds for the actual prepared state, not just a substituted passive ground
state. The derivation below is new; the one-link result is an exact check
against existing evidence, not a new numerical run.

The remaining contact and absolute-volume questions have a different status.
For the frozen diagnostic source `H(f)=H0-sum f_e n_e`, the contact is already
exactly zero. For the prospective *physical* strain/metric source, BS20a
explicitly leaves its second contact uninstantiated. Existing normalized
record dynamics cannot identify its identity part. Likewise, the program
already has an adopted metric/volume action, but the BS-to-action matching
does not yet determine its absolute volume coefficient. These are precise
missing source derivatives, not merely calculations that have run too slowly.

## 1. Exact native sum rule, without a passive-state assumption

Take the ports-off BS Hamiltonian, with all its listed bulk terms retained.
For each incidence qubit,

\[
n_e=(1-Z_e)/2,\qquad H_{\rm flip}=-h_N\sum_eX_e,
\qquad h_N=\Omega/N.
\]

The degree penalty, onsite/formation terms, and the incidence-weighted carrier,
record and current terms all commute with every `n_e`. Consequently

\[
[H,n_f]=-ih_NY_f,\qquad
\boxed{[n_e,[H,n_f]]=h_N\delta_{ef}X_e.}                 \tag{1}
\]

This does not assume that formation is inactive: its listed onsite copy
generators commute with incidence occupations. If an instantiated port fails
to commute, its explicit term `[n_e,[H_port,n_f]]` must be added. An unspecified
port cannot silently be discarded in applying the identity to another run.

For real frozen source weights `v,w`, define `B_v=sum v_e n_e`. The response
to the sign convention `H(f)=H0-f B_w` is

\[
\chi_{vw}(t+\tau,t)=\frac{i}{\hbar}\theta(\tau)
 \langle[B_v(t+\tau),B_w(t)]\rangle.
\]

Since the `n_e` commute at equal time, its right-hand initial value and slope
are exactly

\[
\chi_{vw}(t,t)=0,\qquad
\boxed{\partial_\tau\chi_{vw}(t+\tau,t)|_{0^+}
 =\frac{h_N}{\hbar^2}\sum_ev_ew_e\langle X_e\rangle_t.} \tag{2}
\]

Equation (2) is valid for a nonstationary formed state. No phase mixing,
thermalization, equilibrium replacement, or frequency-domain approximation
is required. It connects an actual native coherence to an impulse-response
coefficient with no fitted normalization.

For a stationary state diagonal in `H0`, let `Delta_ab=E_b-E_a>0`, and define
the signed measure

\[
dM_{vw}(\Delta)=\sum_{E_a<E_b}(p_a-p_b)
 \operatorname{Re}[(B_v)_{ab}(B_w)_{ba}]
 \delta(\Delta-\Delta_{ab})\,d\Delta.
\]

The symmetric cross-response `chi^S_vw=(chi_vw+chi_wv)/2` obeys

\[
\chi^S_{vw}(\omega)=2\int
 \frac{\Delta\,dM_{vw}(\Delta)}
 {\Delta^2-\hbar^2(\omega+i0)^2},\qquad
\boxed{2\int\Delta\,dM_{vw}
 =h_N\sum_ev_ew_e\langle X_e\rangle.}                 \tag{3}
\]

For a self-response the symmetrization is unnecessary. Keeping it for cross
channels avoids silently assuming all transition matrix elements are real.
Degenerate zero-energy channels need their own static treatment; they do not
alter this first-moment identity. At finite dimension the corresponding
large-frequency coefficient is

\[
\chi^S_{vw}(\omega)=
 -\frac{h_N\sum_ev_ew_e\langle X_e\rangle}
 {\hbar^2\omega^2}+O(\omega^{-4}).                     \tag{4}
\]

Thus different-edge first moments vanish exactly, even when their static
responses and individual transitions do not. The actual populations and
`<X_e>` need not have passive signs. The inverse-gap moment
`chi(0)=2 integral dM/Delta` is not fixed by (3); neither is a source contact.

### Exact check from the already solved formed link

For the existing one-link held Hamiltonian
`H=(C+epsilon)I-epsilon n-hX`, energy conservation from the prepared occupied
link gives

\[
h\langle X\rangle_w=\epsilon[1-m(w)],\qquad
m(w)=1-\frac{4h^2}{R^2}\sin^2\!\frac{Rw}{2\hbar},
\quad R^2=\epsilon^2+4h^2.
\]

The exact two-time response in `NATIVE_FORMED_NETWORK_RESPONSE_BRIDGE_V001.md`
therefore has
`partial_tau chi|0+=epsilon[1-m(w)]/hbar^2`, as (2) requires. At `w=0` its
zero slope is consistent with its identically zero initial impulse response;
high occupation alone is not response strength. This check uses the original
formation energy ledger, not a chosen density-of-states model.

## 2. One adopted input can become a matching output: the inertial scale

The recent mechanical comparison parent has positive mode weights `w_j`,
coordinates `y_j`, and source-linear insertion

\[
B_{\rm mech}=\sum_jw_j\kappa\delta_jy_j.
\]

The kinetic normalization must be specified as well. For
`L_kin=sum_j w_j m_j ydot_j^2/2`, canonical momentum is `p_j=w_j m_j ydot_j`
and kinetic energy is `sum_j p_j^2/(2w_j m_j)`. Canonical commutation then gives

\[
\boxed{[B_{\rm mech},[H,B_{\rm mech}]]
 =\hbar^2\sum_j\frac{w_j\kappa^2\delta_j^2}{m_j}.}       \tag{5}
\]

It is independent of the quartic potential and of the mechanical state.
Its classical Poisson-bracket impulse coefficient is the same. The bounded
source has `h'(0)=1`, so (5) is its zero-background insertion as well. Its
finite-background insertion must retain the actual Jacobian of `h`.

If—and only if—the native source is calibrated to this same physical source
by `f=gamma g`, the same degrees of freedom and per-cell/per-volume convention
are matched, and no extra source sectors are omitted, (3) requires

\[
\sum_j\frac{w_j\kappa^2\delta_j^2}{m_j}
 =\frac{\gamma^2h_N}{\hbar^2}\sum_ev_e^2\langle X_e\rangle.
                                                               \tag{6}
\]

For the declared continuum kinetic measure
`L_kin=integral_0^Lambda A delta m(delta) ydot_delta^2/2 ddelta`, a constant
mass has the especially simple constraint

\[
\boxed{\frac{A\kappa^2\Lambda^4}{4m}
 =\frac{\gamma^2h_N}{\hbar^2}\sum_ev_e^2\langle X_e\rangle.} \tag{7}
\]

After the source and spectral normalization are independently bound, (7)
fixes `m` instead of fitting it. This matters because the quantum floor and
response-time window depend on precisely that mass. If the native right side
is zero or negative, a nonzero finite-positive-mass mechanical channel cannot
match it; changing the native signs to force a fit is not allowed. That would
reject this identification at that state, not the network theory.

Equation (7) does not already prove `nu=A delta`, constant mass, the source
conversion `gamma`, or a physical volume density. It supplies a new exact
constraint on those claims. Repeating the same source calibration at two
prepared ages also tests whether a state-independent inertial identification
is possible: changing native strength cannot be represented by a fixed (5)
without additional retained state/source structure.

## 3. Which remaining quantities are calculations, and which need new input?

| Quantity | What the original specification actually determines |
|---|---|
| Finite source-weighted spectrum | Once the finite matrices, state and insertion are fixed, all transition weights and gaps are calculable. The current held-state measure has already been computed; it is signed, not a passive ground measure. Other justified sizes/phases are calculation questions, not a no-identification theorem. |
| Continuum mode-density law | No selected lattice, continuum dimension, thermodynamic state or physical-volume normalization is fixed by the BS seed. Its mean-incidence Laplacian is a declared spectral diagnostic, not automatically the Hamiltonian transition spectrum. A specified native limit may derive a useful weighted window; raw mode counts alone do not. Equation (3) constrains its normalization. |
| Diagnostic source contact | For the already frozen `H0-sum f_e n_e`, `C=partial_f^2 H=0` exactly. Its regular fixed-population curvature is `-chi(0)`. Adding a new bare stiffness would change that source problem. |
| Physical strain contact | BS20a retains `H_contact[j]=O(j^2)` and all identity/seagull/boundary contributions. Its source-to-physical-metric conversion and those contact matrices are not yet supplied by the BS record equations. This is a missing part of the physical completion, not an unperformed evaluation of a fully specified matrix. |
| Bounded record feedback | BS11 already gives a bounded per-edge shift `lambda_R(q_u+q_v)`, with eigenvalues `0,lambda_R,2lambda_R`. Bounded native amplitude is therefore real. It does not determine the mechanical function `g/sqrt(1+g^2/g_s^2)`, its derivative, the physical acceleration argument, or the crossover scale. Actual record responses can be oscillatory and preparation-dependent. |
| Absolute volume coefficient | The adopted metric action already contains matched `C0` and `CR`; total Newton calibration fixes `CR`, not `C0`. The BS finite energy and fixed-background correlators do not specify the complete physical-volume derivative or its reference/matching term. |

The fixed finite held system also has analytic isolated eigenbranches near
zero analytic source. Its exact zero-field energy is therefore not a cubic
absolute-value law. A controlled intermediate window or nonuniform limit is
the constructive route; this is not a claim that all native scaling limits
have already been calculated and rejected.

## 4. A rigorous minimal discriminating variation

Let a candidate physical completion have
`H(g)=H0-gB+g^2 C/2+...`. With fixed adiabatically transported stationary
populations, its total source-work curvature is

\[
E_{\rm ad}''(0)=\operatorname{Tr}(\rho C)-\chi_B(0).       \tag{8}
\]

An absolute source-energy second difference at `+dg,0,-dg`, or the equivalent
source-conjugate work measurement, determines the left side in its controlled
small-step limit. Combining that with the commutator susceptibility determines
the complete averaged contact. All actuator, boundary, identity and matching
terms must enter once. Measuring `<B>` alone misses an added identity contact.
For a nonstationary state, use the complete two-time response and work history
instead of treating (8) as an equilibrium formula; preparation/ramp rates are
part of the source experiment.

Why is this new information necessary? The family

\[
H_c(g)=H(g)+\tfrac12c g^2I
\]

preserves `H0`, the first insertion and every normalized prescribed-source
trajectory, for all prepared states and histories. It changes (8) by `c`.
Thus no number of extra normalized trajectories can select its physical
contact. Absolute source work, a fully owned contact derivation, or coherent
controller-relative phases can distinguish them. The family illustrates the
unbound physical-completion slot; it does not authorize changing a previously
frozen diagnostic or adding a contact to rescue its result.

For the volume channel, the equally explicit extension
`H(g,V)+alpha(V-V0)I` preserves the known reference Hamiltonian and normalized
evolution while changing pressure by `-alpha`. The narrow remaining datum is
the **absolute volume-sensitive derivative at independently calibrated
physical volume**, including the same state/current/creation and boundary
protocol. In the adopted strict constant-volume-action class, subtracting
other owned pressure contributions fixes its one constant `C0`. A calibrated
absolute second metric contact with a nonzero volume component is an
alternative, as already derived in `VACUUM_STRESS_IDENTIFIABILITY_V001.md`.

The mechanical force law fixes an energy *difference* between its source
endpoints. Setting its high-field gravitational volume term to zero would
turn that difference into a low-field vacuum term, but that physical matching
condition is not implied by (1)–(8). A constant absolute volume shift leaves
every one of these incidence response moments unchanged.

## Concrete next use

Use (2) or (3) as the normalization constraint when deriving one native
source channel, before promoting its spectrum to the mechanical continuum.
Keep the native source's actual populations and signs. Then obtain the
complete source-work Hessian and one calibrated absolute volume insertion
from the *same* explicit controller/source completion. Those two derivatives
distinguish the otherwise identical critical/noncritical and vacuum-shifted
completions. Larger source-free lattice examples cannot substitute for them.

This is a finite constructive target: **bind the source, its oscillator
strength, its absolute work curvature, and its volume work in one parent**.
The exact strength identity already removes one independent freedom from
that matching problem; it neither presupposes extra dark matter/energy nor
chooses a function from a desired astronomical curve.

## Evidence and independent check

- `recovered_sources/BS_MICRO_ACTION.md`, especially BS05–BS12 and BS20a–BS21.
- `NATIVE_FORMED_NETWORK_RESPONSE_BRIDGE_V001.md`, exact formed-link response
  and energy ledger.
- `soft_mode_constitutive_screen/NATIVE_ELIGIBILITY_AND_JOINT_CLOSURE.md`,
  signed native spectrum, fixed source and inequivalent contact completions.
- `joint_parent_dynamics/CRITICAL_RESPONSE_CLOSURE.md` and
  `MECHANICAL_STATE_AND_RATE.md`, complete mechanical energy, kinetic/state
  assumptions and the role of its inertial scale.
- `ADOPTED_ACTION_DARK_CONSEQUENCES_V001.md` and
  `VACUUM_STRESS_IDENTIFIABILITY_V001.md`, existing metric/volume action and
  exact identity/contact ambiguity.

The independent mathematical lane checked the Pauli signs, retarded slope,
signed symmetric first moment, and finite canonical mass/weight factors in
(1)–(7). This is analytical evidence; no new measured native moment or
astronomical validation is claimed.
