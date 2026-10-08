# Native retained occupations: exact dynamical-density screen

2026-09-27. Analytical consequence of inspected resident sources, not a new Hamiltonian or numerical run. No physical embedding of register labels is assumed.

Units: \(\hbar=1\) in the evolution and response equations.

## 1. Source boundary and actual terms

The BS original MICRO_ACTION.md is compressed,dataless and was skipped. So were the checked one-link protocol, hold-structure note and two implementations. This result is therefore tied to the explicitly reconstructed finite BS-family restriction, not a fresh authentication of every term of the unavailable original action.

The resident [formed-pattern design](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/FORMED_PATTERN_TEST_DESIGN.md:75>) and [implementation, build function](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/formed_pattern/compute_formed_pattern.py:51>) agree on:
\[
\begin{aligned}
H(g)={}&-h\sum_eX_e+\Delta\sum_en_e+U_d\sum_v(d_v-d_*)^2
+\epsilon_\psi\sum_vN_v+\epsilon_r\sum_vq_v\\
&-t_{\rm hop}\sum_{e=(u,v)}n_eT_{uv}
+\lambda_J\sum_en_eJ_e^2
-\lambda_R\sum_en_e(q_u+q_v)+g\sum_{\rm targets}X_{r_v}
+\text{writer constant}.
\end{aligned}
\]
Here \(q_v\) is record occupation, \(n_e\) incidence occupation and \(N_v\) carrier occupation. They are different operators. In the implementation every \(g=0\) matrix entry preserves the record index; only the local write entry at line 71 flips it. The [hold construction](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/formed_pattern/compute_formed_pattern.py:250>) explicitly uses the full record blocks and retains the complete formed state. No program was executed in this audit.

Inspected implementation SHA256: b208a85c11061f5f2b34bcc786a3ef16b88d8f1de9fa8dde0eddb3dd901c7bfa. Design SHA256: ca82885f0133efe88bedef5740d77f2a960412b9f016bda4c8002a0dc86839ba.

## 2. Exact theorem for any record-diagonal hold

Let the mutually commuting fixed register projectors be \(q_v\). Suppose
\[
[H(t),q_v]=0\quad\text{for every }v,t .
\]
This includes arbitrary prescribed time-dependent coefficients of the displayed source-off terms, even when \(H(t)\) does not commute with \(H(t')\). The time-ordered evolution obeys
\[
[U(t,t_0),q_v]=0,\qquad q_v(t)=q_v.
\]
Consequently every joint occupation projector \(P_{\boldsymbol q}\), all its probabilities, and every correlation \(\langle q_{v_1}\cdots q_{v_k}\rangle\) are constant. This holds for arbitrary initial states, including record–background entanglement and coherences between occupation sectors.

For any fixed complex c-number weights \(f_v\), define
\[
Q_f=\sum_v f_vq_v.
\]
A Fourier labeling is an optional choice of these weights; it does not identify them with physical spatial momentum. The exact retarded commutator kernel is
\[
\boxed{\chi^R_{fg}(t,t')
=-i\Theta(t-t')\langle[Q_f(t),Q_g^\dagger(t')]\rangle=0.}
\]
There is no equal-time contact from varying a fixed operator \(Q_f\). The result holds at zero temperature, at finite temperature, and for the actual formed state; it needs no equilibrium assumption.

Define \(\delta Q_f=Q_f-\langle Q_f\rangle\) and
\[
C_{fg}=\langle\delta Q_f\delta Q_g^\dagger\rangle.
\]
With the full-time Fourier convention \(\int d\tau\,e^{i\omega\tau}\), both the connected unsymmetrized correlator and the symmetrized one have only elastic support:
\[
\begin{aligned}
S^>_{fg}(\omega)
&=\int d\tau\,e^{i\omega\tau}
 \langle\delta Q_f(\tau)\delta Q_g^\dagger(0)\rangle,\\
S^{\rm sym}_{fg}(\omega)
&=\frac12\int d\tau\,e^{i\omega\tau}
 \langle\{\delta Q_f(\tau),\delta Q_g^\dagger(0)\}\rangle,\\
\boxed{S^>_{fg}=S^{\rm sym}_{fg}
&=2\pi C_{fg}\delta(\omega).}
\end{aligned}
\]
For a state sharp in every \(q_v\), even this connected elastic weight vanishes. Finite observation windows broaden the elastic line mathematically; they do not establish inelastic transport.

### Stronger prescribed-chemical-field control

For real prescribed c-number functions \(\mu_v(t)\), add
\[
\delta H(t)=-\sum_v\mu_v(t)q_v.
\]
Because this source commutes with every unperturbed \(H(t')\),
\[
U_\mu(t,t_0)=
\exp\!\left[i\sum_vq_v\int_{t_0}^t\mu_v(s)\,ds\right]U_0(t,t_0).
\]
It changes only relative occupation-sector phases. Every observable commuting with all \(q_v\)—including record-diagonal carrier/link observables—has the same expectation as without this source, for the same initial state. Off-diagonal record observables can detect the changed phases.

This statement does **not** cover \(\mu_v\) that is an operator depending on dynamical positions, links or carriers. Such a coupling can change background dynamics while still conserving the \(q_v\). Nor does it cover general metric variations of the complete interaction energy.

## 3. Static statistical response is a different operation

For a mathematically specified Gibbs family
\[
\rho_\mu=Z^{-1}\exp[-\beta(H_0-\sum_v\mu_vq_v)],
\]
commutation gives
\[
\frac{\partial\langle q_v\rangle_{\rho_\mu}}{\partial\mu_w}
=\beta\,\operatorname{Cov}_{\rho_\mu}(q_v,q_w).
\]
This derivative can be nonzero because it compares differently weighted occupation sectors. A closed source-off hold cannot implement that redistribution. It is not the zero-frequency limit of the identically zero retarded kernel above. A bath or preparation rule would need actual occupation-changing transitions to equilibrate those sector weights; the Gibbs formula alone does not supply them. The zero-temperature version also requires handling sector selection/crossings, not replacing a dynamical susceptibility by this finite-temperature covariance formula.

## 4. “Static occupations” is not “nothing moves”

For the resident carrier hopping and the design's convention
\[
J_{uv}=-i|u\rangle\langle v|+i|v\rangle\langle u|,
\]
the carrier has the genuine label-space continuity equation
\[
\dot N_u=-\sum_{v:\,(u,v)}t_{\rm hop}n_{uv}J_{uv}.
\]
The opposite endpoint receives the opposite current. In contrast, every fixed register cut \(A\) has \(\partial_t\sum_{v\in A}q_v=0\). These are distinct conserved objects.

The record-associated allocation
\[
H_{\rm rec}=\sum_vq_v(\epsilon_r-\lambda_Rd_v)
\]
still exchanges energy:
\[
\frac{d\langle H_{\rm rec}\rangle}{dt}
=-\lambda_Rh\sum_{e=(u,v)}
 \langle(q_u+q_v)Y_e\rangle
\]
for the fixed-coefficient hold. Link and interaction dynamics, not only carriers, can carry energy changes. A moving or changing complete stress source therefore cannot be identified with the record-count operator by name.

In the occupation basis,
\[
H=\bigoplus_{\boldsymbol q}H_{\boldsymbol q},\qquad
\langle O_{\rm bg}(t)\rangle
=\sum_{\boldsymbol q}
\operatorname{Tr}\!\left[
 U_{\boldsymbol q}\rho_{\boldsymbol q\boldsymbol q}
 U_{\boldsymbol q}^\dagger O_{\rm bg}\right].
\]
For record-blind observations this is an exact fixed-weight ensemble of occupation-conditioned background evolutions, including the actual conditional initial states. It resembles frozen configuration disorder in register space. It is **not fundamental superselection**: off-diagonal record coherences remain allowed, and the native write operation connects sectors.

## 5. The owned evasion—and the unresolved physical transport question

The actual write term is an evasion already present in the finite parent. With the fixed-content convention \(q=(I-Z)/2\),
\[
i[gX_r,q]=-gY_r.
\]
It creates or reverses local occupation, and in general does not conserve the total retained count. The displayed term is local write/erase dynamics, not an inter-register hopping term. Its externally selected source and switching work must remain in the ledger. Formation can establish correlated patterns before hold; hold does not subsequently redistribute their probabilities.

No additional record-transport term was found in the inspected resident restriction. The inaccessible original does not license an exhaustive claim about every BS extension.

Finally, fixed labels are not independently fixed physical positions. If the same parent earns probe-defined, record-commuting region weights \(w_v(t)\), a relational count can be
\[
Q_{\mathcal R}=\sum_vq_vw_v,\qquad
\dot Q_{\mathcal R}=\sum_vq_v
  \left(i[H,w_v]+\partial_tw_v\right).
\]
It need not be conserved. No such operational region/current map was supplied by the inspected Hamiltonian. Consequently the label-space null response is not a Bullet Cluster exclusion or a universal no-clustering result. Gravity-driven relational motion could coexist with conserved material labels, but it must be demonstrated through that map and the complete stress.

## Exact next decision

A claimed dynamical record-density response in the source-off model must identify either an actual occupation-changing generator or an independently calibrated dynamical relational density operator. For the existing fixed-label \(Q_f\), the exact benchmark is zero retarded response and purely elastic structure. Any nonzero inelastic result for that same operator and generator would be an implementation/definition mismatch, not evidence of dark-matter transport.
