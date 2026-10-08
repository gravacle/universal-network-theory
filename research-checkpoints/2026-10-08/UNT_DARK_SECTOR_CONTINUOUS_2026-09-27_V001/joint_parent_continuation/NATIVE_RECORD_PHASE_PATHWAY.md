# Native writer-referenced record phase: exact lines and prepared response

2026-09-28. Source-only derivation using the authenticated saved 16-state
record-addition result and its fixed held matrices. No new propagation,
equilibrium replacement, coefficient fit, source change or frozen-file edit.
The few numerical coefficients below are arithmetic from saved expectations
and energy gaps; the audit agent independently checked the principal ones
directly from the saved complex formed vector.

## The concrete prediction

The held record **density** has zero retarded self-response, but the owned
writer-copy operator does not. Its response has finite addition frequencies
and is active-state dependent. For the actual native formed state, a weak
positive copying pulse changes its copy readout initially as

    delta<K> = +0.433690926622 delta_g tau² + higher orders,

relative to the unpulsed evolution at the same age, in the inherited
hbar=1 units. The blank-record control has the opposite sign,
`delta<K>=-1.562987789144 delta_g tau²+...`.

This sign reversal is a falsifiable native source-response prediction, not
a chosen continuum susceptibility. There is also a stored neutral relative
phase between the two one-record configurations. It does not supply a
zero-frequency pole of the uniform copying response, a positive dust
background, or a physical clock kinetic term by itself.

## 1. Use the writer source which is already in the Hamiltonian

Keep the factor order `(record_L,record_R,link,carrier)` and the same
fixed-content writer controls as `RECORD_ADDITION_PROTOCOL.md`. Define

\[
A_i=|x\rangle\langle B|_i,\qquad
X_i=A_i+A_i^\dagger,\qquad
Y_i=i(A_i^\dagger-A_i),\quad i=L,R.
\]

Thus `A_i=(X_i+iY_i)/2`; this Y is minus conventional Pauli Y in the
`|B>,|x>` ordering. The actual native writer interaction restricts to
`g(X_L+X_R)`. Its uniform probe is

\[
K=X_L+X_R,\qquad H(t)=H_{\rm hold}+\delta g(t)K.       \tag{1}
\]

No new interaction type is needed to define (1). Independently addressed
endpoint sources would additionally declare the corresponding port control.
Raising/lowering operators below resolve the same copying matrix into its
complex amplitudes. An independently rotated Y drive would require an
explicit phase-controlled port; it is not asserted to have been run. The
occupied writer projectors specify content, not a hidden continuous clock
phase. The real copying generator and its declared switching/calibration
supply the phase reference actually used here.

The held Hamiltonian is exactly

\[
H=3I+R-X_a+(\tfrac94-\tfrac12R-\tfrac12X_C)n,
\qquad R=q_L+q_R.                                    \tag{2}
\]

The fixed record value x and carrier content remain spectators with their
previously declared multiplicities. The following energies are not a
projection onto a ground state.

## 2. All adjacent-record addition lines, including different bands

At count R and carrier-X eigenvalue `s=+/-1`, put

\[
x_{Rs}=\tfrac94-\tfrac12R-\tfrac12s,\quad
d_{Rs}=\sqrt{x_{Rs}^2+4},\quad
E_{\beta s}(R)=3+R+\frac{x_{Rs}+\beta d_{Rs}}2.
\]

Here beta=- is lower and beta=+ upper. A record addition preserves s but
need not preserve beta. Its signed energy change is

\[
\boxed{\Delta_{\gamma\beta}^{Rs}
=E_{\gamma s}(R+1)-E_{\beta s}(R)
=\tfrac34+\frac{\gamma d_{R+1,s}-\beta d_{Rs}}2,}
\quad R=0,1.                                         \tag{3}
\]

The corresponding angular frequency is Delta/hbar; lowering has the
opposite signed line. The complete inherited values are:

| R to R+1 | s | Lower to lower | Upper to upper | Lower to upper | Upper to lower |
|---|---:|---:|---:|---:|---:|
| 0 to 1 | +1 | 0.899520585085 | 0.600479414915 | 3.258015868099 | -1.758015868099 |
| 1 to 2 | +1 | 0.861247173342 | 0.638752826658 | 2.997248109672 | -1.497248109672 |
| 0 to 1 | -1 | 0.944984491243 | 0.555015508757 | 3.955383135941 | -2.455383135941 |
| 1 to 2 | -1 | 0.926431095757 | 0.573568904243 | 3.583967548941 | -2.083967548941 |

The negative entries are important: adding a record while dropping from
an excited link branch can release energy. The earlier positive
same-branch addition costs did not include these cross-band processes.
This is release of existing excitation, not production of free energy.

For the link eigenvectors choose the same analytic gauge as the two-band
bridge,

\[
\theta_{Rs}=\operatorname{atan2}(2,x_{Rs}),\quad
u_-=(\cos\tfrac\theta2,\sin\tfrac\theta2),\quad
u_+=(-\sin\tfrac\theta2,\cos\tfrac\theta2).
\]

When an endpoint is blank, its raising matrix between link branches is

\[
T^{Rs}_{\gamma\beta}
=\langle u_{\gamma s}(R+1)|u_{\beta s}(R)\rangle
=\begin{pmatrix}\cos\delta&\sin\delta\\
                 -\sin\delta&\cos\delta\end{pmatrix}_{\gamma\beta},
\quad\delta=(\theta_{R+1,s}-\theta_{Rs})/2.             \tag{4}
\]

All these entries are fixed by the old coefficients. In particular,

\[
\sin^2\delta=\frac12\left[1-
\frac{4+x_{Rs}x_{R+1,s}}{d_{Rs}d_{R+1,s}}\right].       \tag{5}
\]

The actual state or source symmetry can still make a line's net amplitude
zero. The table lists allowed matrix transitions, not a claim that every
line must appear with positive absorption weight. In the feedback-off
control, (4) becomes the identity: cross-band lines vanish and every
allowed same-band addition costs exactly one.

## 3. The complete kernel uses the saved state, including its phases

Let `rho0=|psi_formed><psi_formed|` be the saved native vector, not its
ground projection or an imposed thermal state. Let w be elapsed hold age.
For endpoint copying sources define

\[
\chi_{ij}(\tau;w)=\frac{i}{\hbar}\theta(\tau)
\operatorname{Tr}\rho_0[X_i(w+\tau),X_j(w)].          \tag{6}
\]

Here `X_i(t)=exp(iHt/hbar) X_i exp(-iHt/hbar)`. The plus-sign coupling
in (1) gives `delta<X_i(t)>=-integral chi_ij(t,t') delta_g_j(t')dt'`.
This sign is kept consistent with the actual copying switch work.

In any full energy basis, retaining degeneracies and all 16 states, (6) is
the explicit finite sum

\[
\boxed{\chi_{ij}(\tau;w)=\frac{i\theta(\tau)}\hbar
\sum_{a,b,c}(\rho_0)_{ca}e^{i(E_a-E_c)w/\hbar}
\left[(X_i)_{ab}(X_j)_{bc}e^{i(E_a-E_b)\tau/\hbar}
 -(X_j)_{ab}(X_i)_{bc}e^{i(E_b-E_c)\tau/\hbar}\right].} \tag{7}
\]

Equations (3)--(5), the record raising action and the saved complex vector
fix every coefficient. Projector versions of (7) are equivalent and avoid
arbitrary eigenvector choices inside the R=1 degeneracy. Cross-carrier-s
coherences do not enter these kernels because the copying operators preserve
s; their omission from this readout is exact, not a discarded population.

The one-point phase signal is equally explicit:

\[
\langle A_i(w)\rangle=
\sum_{f,b}e^{i(E_f-E_b)w/\hbar}
\operatorname{Tr}(\rho_0 P_f A_i P_b),                \tag{8}
\]

where f,b are the allowed final/initial energy projectors. Thus the writer
readout is `2 Re sum_i<A_i>`, and its Y quadrature is
`2 Im sum_i<A_i>`. At the actual saved switch,

\[
\langle K\rangle=-1.12798401232428,\quad
\langle Y_L+Y_R\rangle=1.50439712323881,
\]

so

\[
\langle A_L+A_R\rangle
=-0.563992006162142+i\,0.752198561619406.              \tag{9}
\]

These numbers follow from the already stored copy-work and production
current; the endpoint contributions are equal by the exact record-exchange
symmetry. They exhibit substantial retained phase coherence, not merely
occupied record probabilities.

## 4. A directly testable short-pulse response and its active sign

Put `D=epsilon_r-lambda_R n`. The held Hamiltonian's record-dependent part
is `D R`, while its other terms commute with K. Consequently

\[
[R,K]=i(Y_L+Y_R),\qquad
\boxed{[K,[H,K]]=4D(1-R).}                            \tag{10}
\]

Thus the actual waiting-age slope, with no stationary-state assumption, is

\[
\boxed{\partial_\tau\chi_{KK}(0^+;w)
=\frac4{\hbar^2}\langle(\epsilon_r-\lambda_Rn)(1-R)\rangle_w.} \tag{11}
\]

The stored term expectations determine it without propagating again:
`4[1-<R>-lambda_R<n>-E_record_feedback]` at hbar=1.
At the switch the three prepared cases give

| Actual preparation | Copy-source initial slope |
|---|---:|
| Native two-record state | -0.867381853244 |
| Feedback-off formed state | -1.175273204663 |
| Copying-off blank-record state | +3.125975578287 |

These are not the record-density-source slopes reported before the copying
quench; they concern a different, explicitly defined source K during hold.
In the native case the slope changes with held link correlations: the
stored ages 0,.25,.5,1,2 give respectively
`-.867381853244,-.813079785075,-.825188048941,-1.014395843298,-1.169355919004`,
despite exactly constant record probabilities.

For a small constant copying pulse starting at age w, comparison to the
unpulsed evolution gives

\[
\delta\langle K\rangle(w+\tau)
=-\frac{\delta g\,\tau^2}{2\hbar^2}
 \langle[K,[H,K]]\rangle_w+O(\delta g\tau^3,\delta g^2\tau^3). \tag{12}
\]

This yields the sign reversal stated at the start. Record number can respond
to this copying source even though its response to a source proportional
to R itself is zero:

\[
\delta\langle R\rangle(w+\tau)
=\frac{\delta g\tau}{\hbar}\langle Y_L+Y_R\rangle_w
 +O(\delta g\tau^2,\delta g^2\tau^2).                 \tag{13}
\]

At the native switch its linear coefficient is `1.504397123239`. The
relative phase already present in the records therefore controls the
initial writing response. No claim of monotonic growth at every hold age
follows; (8) fixes its subsequent phase dependence.

A negative (11) diagnoses a nonpassive prepared source response, not a
negative microscopic kinetic norm or instability of finite unitary
evolution. Replacing the actual state by the lower band would erase the
response being explained rather than repair it.

## 5. Gapped copying response and a separate neutral relative phase

Every nonzero matrix element of K connects adjacent counts with the same s.
The smallest absolute coupled energy gap in this held cell is exactly

\[
\Delta_{\min}=\frac{6+\sqrt{145}-\sqrt{185}}8
=0.555015508757107>0.                                 \tag{14}
\]

Thus no zero response-frequency line is hidden in (7) for K or either
endpoint's single-copy quadrature. Waiting-age beats and degenerate initial
coherences do not change that statement: each exponential in response delay
tau contains a gap of the copying operator. The isolated finite system has
oscillatory memory, not a derived relaxation or thermalization time.

There nevertheless is a genuine neutral operator inside count one:

\[
C=A_L^\dagger A_R,\qquad [H,C]=0.
\]

It exchanges the two endpoint arrangements without changing R. Identical
writer formation confines the prepared R=1 record state to
`(|10>+|01>)/sqrt(2)`, so the saved state has

\[
\langle C\rangle=P(R=1)/2=0.224792172308619.           \tag{15}
\]

The two configurations have identical held energies. Their relative phase
can be changed by a declared differential source with no static held
phase-twist energy. This is a neutral degeneracy, not a propagating clock
mode or positive phase stiffness. The uniform K annihilates the antisymmetric
record combination and connects the symmetric ladder only between counts.
Consequently (15) does not generate a zero-frequency K pole. Local endpoint
probes can access the antisymmetric intermediate states, but their
single-addition gaps remain (3); the full 16-state version (7) retains them.

## 6. Actual spectral weights, without pretending the state equilibrates

For the uniform source, the symmetric count ladder has raising matrix
element `sqrt(2) T_gamma,beta` between R and R+1. Its actual diagonal
populations are the saved `spectrum_and_actual_weights`, not Boltzmann
weights. For example, at s=+1 the lower-band populations for R=0,1,2 are
`0.052386858134,0.189898526327,0.170198703437`.
At s=-1 they are `0.056139654796,0.208312356864,0.193615559212`.
The full upper population `0.129448341230` remains present.

If one **explicitly averages the hold age**, rather than changes the
microscopic preparation, the off-energy coherences receive the ordinary
sinc factors and vanish in the infinite-window limit while degenerate
coherences remain. Only for that declared averaged diagnostic is the
stationary expression

\[
\overline\chi_{KK}(\omega)=
\sum_{R,s,\beta,\gamma}
\frac{4\Delta_{\gamma\beta}^{Rs}
 (p_{R\beta s}-p_{R+1,\gamma s})|T_{\gamma\beta}^{Rs}|^2}
 {(\Delta_{\gamma\beta}^{Rs})^2-\hbar^2(\omega+i0)^2}  \tag{16}
\]

appropriate. Each adjacent pair is included once with its signed Delta;
this is equivalent to ordering each pair by energy. The larger populated
R=1 lower state than R=0 lower state already produces negative absorption
weight on their positive-frequency line. Other pairs have different signs.
The nonstationary prediction remains (7), not (16).

The gap (14) makes a formal low-frequency expansion of (16) possible; its
coefficients involve actual signed inverse-gap moments. It neither proves
a passive positive clock inertia nor licenses identifying those coefficients
with a freely selected cosmological `K(Q)`. A controlled drive/observation
window and the source-to-clock/volume normalization still belong to the
physical completion. The new result is stronger than a generic missing-input
statement: (3), (7), (11)--(13) already predict the complete observable
line family and a state-sensitive response-sign test of that completion.

## 7. Source work cannot be separated from the phase measurement

For the physical plus-sign drive in (1), inclusive source work is

\[
W=\int dt\,\dot{\delta g}(t)\langle K\rangle_{\rm driven}(t).
\]

A sudden turn-on changes energy by `delta_g<K>`; turning off a coupling
g changes it by `-g<K>`. The saved copying quench therefore supplies
`+1.12798401232428`, exactly as (9) requires. A positive weak turn-on at
that same phase initially lowers the driven system's Hamiltonian energy;
the controller receives the corresponding work. The complete pulse's
turn-off and dynamical work must also be retained. Neither stimulated
record writing nor a negative spectral weight is a new unowned energy
source.

The immediate useful test is therefore a **writer-referenced phase/source
experiment with the predicted lines and short-pulse signs**, not another
record-count propagation or a ground-state replacement. All matrices and
the actual state required for its exact postprocessing now exist in
`RECORD_ADDITION_RESULTS.json`; no enlarged lattice is required to test
these predictions.

## Read-only review and custody

The stored result remains
`2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a`
under its repaired, matching frozen-source manifest. No file in that
freeze was edited here. The audit agent independently evaluated (11),
(14) and (15) from the authenticated saved vector/matrices, with no new
time evolution, and confirmed the reported signs and numerical values.
The full DE note `FULL_RESPONSE_PRESSURE.md` was also independently read:
its separate matched-stress `J>u` and `-1<=w_trace<-5/9` identities pass;
they are not inferred from this finite record-phase calculation.
