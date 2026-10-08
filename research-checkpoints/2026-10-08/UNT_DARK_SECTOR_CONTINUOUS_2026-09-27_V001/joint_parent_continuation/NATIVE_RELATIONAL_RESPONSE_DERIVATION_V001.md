# Native incidence response read at equal record phase

2026-09-28. Analytical continuation of the SAME saved held state, Hamiltonian, incidence source and writer-referenced observable. No new preparation, numerical worker, source term, passive-state replacement, or physical-time calibration.

## Result

The proposed equal-phase response is well defined wherever the original record amplitude is nonzero and its phase rate is nonzero. Its exact linear kernel is

\[
\boxed{\chi_{\rm rel}(\tau;w)=\chi_{nn}(\tau;w)
 -\frac{\dot m(w+\tau)}{\nu(w+\tau)}
 \operatorname{Im}\!\left[\frac{\chi_{An}(\tau;w)}{a(w+\tau)}\right].}
\tag{1}
\]

The incidence impulse leaves the record phase **and its first time derivative unchanged immediately**, even at finite impulse angle. Clock backreaction therefore begins only at second order in the delay. The native coherence sum-rule slope survives; expressed per increment of record phase it is

\[
\boxed{\left.\frac{\partial\chi_{\rm rel}}{\partial\Delta\phi}\right|_{0^+}
 =\frac{h\langle X_a\rangle_w}{\hbar^2\nu(w)}.}
\tag{2}
\]

There is one factor of the actual clock rate, not two. This is a falsifiable same-state relational response, not yet a relation between network coordinates and gravitational acceleration.

## 1. Keep the native operators and source sign

Use the factor order and actual formed vectors in `RECORD_ADDITION_RESULTS.json`, with

\[
n=(1-Z_a)/2,\quad R=q_L+q_R,\quad A=A_L+A_R,\quad A_i=|x\rangle\langle B|_i.
\]

The complete held Hamiltonian in this cell is

\[
H=3I+\epsilon_r R-hX_a+B n,\qquad
B=\frac94-\lambda_R R-\frac12X_C,
\tag{3}
\]

with inherited \(\epsilon_r=h=\hbar=1\), \(\lambda_R=1/2\) for native feedback, and \(\lambda_R=0\) for the feedback-off control. The link \(Y_a\) below is conventional Pauli Y; it must not be confused with the record quadrature's minus-Pauli-Y convention in `NATIVE_RECORD_PHASE_PATHWAY.md`.

Let \(\rho_w\) be the actual held state at age \(w\). Apply only the original diagnostic incidence impulse

\[
H_\eta(t)=H-\eta n\,\delta(t-w),\qquad
U_\eta=\exp(+i\eta n/\hbar).
\tag{4}
\]

Here \(\eta\) has units of action (energy times time), not the energy units of a constant source step. Equivalently use the dimensionless impulse angle \(\alpha=\eta/\hbar\). The response per \(\alpha\) is \(\hbar\) times the response per \(\eta\). This distinction is necessary when comparing an impulse with earlier finite-duration pulses.

For any, possibly non-Hermitian, readout \(O\),

\[
\chi_{On}(\tau;w)=\frac{i}{\hbar}\operatorname{Tr}\rho_w[O(\tau),n],
\quad O(\tau)=e^{iH\tau/\hbar}Oe^{-iH\tau/\hbar},\qquad \tau\geq0,
\]

\[
\langle O\rangle_\eta(w+\tau)
 =\langle O\rangle(w+\tau)+\eta\chi_{On}(\tau;w)+O(\eta^2).
\tag{5}
\]

No stationarity assumption is made. \(\chi_{nn}\) is real, whereas \(\chi_{An}\) is complex and both quadratures must remain.

## 2. Equal phase requires a readout-time correction

Use the same phase orientation and writer reference as `NATIVE_PHASE_CLOCK_CANDIDATE_V001.md`:

\[
m(t)=\langle n\rangle_t,\quad a(t)=\langle A\rangle_t,
\quad \phi(t)=\arg a(t)\text{ continuously lifted},\quad
\nu(t)=\operatorname{Im}[a^*(t)\dot a(t)]/|a(t)|^2.
\]

Fix the readout phase to the unperturbed value at \(t=w+\tau\), rather than adjusting the source phase or replacing \(A\) by its adjoint. The perturbed readout occurs at \(t+\delta t\). Linearizing the phase equality gives

\[
\delta\phi(t)=\eta\operatorname{Im}[\chi_{An}(\tau;w)/a(t)],\qquad
\delta t=-\frac{\eta}{\nu(t)}\operatorname{Im}[\chi_{An}(\tau;w)/a(t)].
\tag{6}
\]

The resulting incidence change is \(\eta\chi_{nn}+\dot m\delta t\), which proves (1). All the denominators and the drift \(\dot m\) in the exact expression are evaluated at the **readout endpoint**, not automatically at the impulse age. This is a local inverse-function construction; a zero signal, stationary phase point, or nonunique phase crossing invalidates this readout chart rather than defining a very large physical susceptibility.

The relative phase can equally be measured from \(\phi(w)\). The impulse commutes with \(A\), so it leaves that initial reference unchanged exactly. A constant writer-phase rotation cancels from \(\chi_{An}/a\); an independently time-rotated writer reference is not part of this experiment.

## 3. Clock backreaction vanishes through first order in delay

Put \(D=\epsilon_r-\lambda_R n\). The exact commutators are

\[
[H,n]=-ihY_a,\qquad [H,A]=DA,
\qquad [n,A]=[n,DA]=0.
\tag{7}
\]

Both \(a\) and \(\dot a=(i/\hbar)\langle DA\rangle\) are therefore unchanged by \(U_\eta\) at the instant of the kick, for **every** finite \(\eta\). Their amplitude derivative and phase rate are unchanged too, whenever the phase exists. This is an exact operator property of the specified held Hamiltonian, not a numerical cancellation or a general claim about arbitrary clock sources.

The next commutator does not vanish:

\[
[H,[H,A]]=D^2A+i\lambda_RhY_aA,
\qquad [[H,[H,A]],n]=\lambda_RhX_aA.
\]

Consequently the first clock response is

\[
\boxed{\chi_{An}(\tau;w)
 =-\frac{i\lambda_Rh}{2\hbar^3}\langle X_aA\rangle_w\,\tau^2+O(\tau^3),}
\]

\[
\operatorname{Im}\frac{\chi_{An}}{a(w+\tau)}
 =-\frac{\lambda_Rh}{2\hbar^3}
 \operatorname{Re}\frac{\langle X_aA\rangle_w}{a(w)}\,\tau^2+O(\tau^3).
\tag{8}
\]

This term can vanish for a particular state without changing the operator identity. It would then move the first phase correction to higher order, not justify assuming that correction away for other states.

For an optional exact finite-angle check,

\[
U_\eta^\dagger Y_aU_\eta=Y_a\cos\alpha+X_a\sin\alpha,
\]

so the immediate change in \(\ddot a\) is

\[
\ddot a_\eta-\ddot a
 =-\frac{i\lambda_Rh}{\hbar^2}
 \left\langle[(\cos\alpha-1)Y_a+\sin\alpha X_a]A\right\rangle_w.
\tag{9}
\]

It gives (8) upon differentiation in \(\eta\). The incidence drift, in contrast, changes immediately by
\(h\langle(\cos\alpha-1)Y_a+\sin\alpha X_a\rangle_w/\hbar\).

## 4. First and second short-delay incidence coefficients

Since \([H,[H,n]]=-2h^2Z_a+hBX_a\),

\[
\chi_{nn}(\tau;w)
 =\frac{h\langle X_a\rangle_w}{\hbar^2}\tau
 +\frac{h\langle B Y_a\rangle_w}{2\hbar^3}\tau^2+O(\tau^3).
\tag{10}
\]

Substitution into (1) yields the exact leading difference between the two readout conventions:

\[
\boxed{\chi_{\rm rel}-\chi_{nn}
 =\frac{\lambda_Rh}{2\hbar^3}
 \frac{\dot m(w)}{\nu(w)}
 \operatorname{Re}\frac{\langle X_aA\rangle_w}{a(w)}\,\tau^2
 +O(\tau^3).}
\tag{11}
\]

Here \(\dot m=h\langle Y_a\rangle/\hbar\). Thus the initial slope in the **external delay** remains \(h\langle X_a\rangle_w/\hbar^2\), including clock backreaction. Its sign is that of the actual coherence, not a substituted positive ground state. If \(\dot m(w)=0\), the leading equal-phase incidence correction vanishes even when the phase itself shifts quadratically.

For \(\theta=\phi(w+\tau)-\phi(w)=\nu(w)\tau+O(\tau^2)\), the slope becomes (2). For the defined phase-time \(T_{\rm phase}=\theta/\omega_{\rm ref}\), it is instead

\[
\left.\frac{\partial\chi_{\rm rel}}{\partial T_{\rm phase}}\right|_{0^+}
 =\frac{\omega_{\rm ref}h\langle X_a\rangle_w}{\hbar^2\nu(w)},
\qquad \omega_{\rm ref}=\epsilon_r/\hbar.
\tag{12}
\]

These are changes of the owned readout variable, not new physical seconds. There is no extra inverse-rate factor from the impulse: for an increasing local phase, \(\delta(t-w)=\nu(w)\delta(\phi-\phi_w)\), while the Hamiltonian generator per phase is divided by \(\nu\). Their factors cancel and leave the same integrated impulse action \(\eta\). More generally, relabeling time by a phase does not eliminate the measured endpoint shift (6); the clock is part of the responding system.

## 5. Keep all three prepared controls

- **Native, \(\lambda_R=1/2\):** use its saved complex vector and actual phase window. Both terms in (1) are predictions. The first slope is protected as above; the higher-delay correction depends on record–link coherences and incidence drift. No sign of that correction is selected beforehand.
- **Feedback-off, \(\lambda_R=0\):** \(A(\tau)=e^{i\epsilon_r\tau/\hbar}A\) exactly, so \(\chi_{An}=0\) at every delay. Its nonzero saved amplitude gives \(\nu=\omega_{\rm ref}\), \(T_{\rm phase}=\tau\), and \(\chi_{\rm rel}=\chi_{nn}\) exactly, not merely to second order.
- **Copying-off blank record:** incidence kicks and the held Hamiltonian preserve the entirely blank record sector. Therefore \(a=\chi_{An}=0\) at every age. Its unclocked incidence response remains reportable, but no division, phase unwrap or artificial relational rate is permitted.

These controls use their own already saved Hamiltonians and states. They do not identify feedback-off dynamics with the native case or change the blank control into a phase reference by adding coherence.

## 6. Smallest meaningful numerical follow-through

No new formation or lattice size is needed. Authenticate the existing record-addition and phase-clock artifacts, then retain the original three states and the already owned hold window/ages. A small full-matrix census can:

1. Evaluate (1) directly from commutators at each predeclared admissible impulse/readout pair, reporting \(a,\nu,\dot m,\chi_{nn},\chi_{An}\), the endpoint-time shift per impulse, and the signed relational correction. Clock admissibility is checked from the original phase bounds, not chosen from the response sign.
2. Independently verify all operator identities (7)–(10), the first slope (2)/(12), the feedback-off all-delay identity and the blank refusal. The real and imaginary parts of \(\chi_{An}\) must both be retained.
3. Check the derivative using symmetric small \(\pm\alpha\) kicks, both at fixed external time and at independently inverted equal record phase on the same local branch. Freeze impulse sizes, delay census and error tolerances before that numerical calculation; keep every result and the finite-difference convergence rather than choosing a favorable kick.

The equal-phase inversion is a diagnostic of this finite native model. It does not assert a covariant timelike clock field, a physical source-to-acceleration calibration, a passive inertia, or a gravitational force. What it establishes is narrower and useful: whether the SAME record phase supplies a consistent internal readout of the SAME incidence response, with the clock's own backreaction explicitly retained.
