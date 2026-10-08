# Compression of the same returned actions: exact positive bulk response

2026-09-28. Analytical result for the actual action spectra already saved in `PREPARED_ACTION_RETURN_V001_RESULTS.json`. No new population, trajectory, temperature, abundance normalization, force fit or numerical execution.

## Result

The already adopted common-current, zero-source adiabatic closure supplies a definite compression coefficient for the SAME prepared state:

\[
\boxed{c_{\rm ad}^2
 =\frac{\sum_jw_jI_j^2 e_{j,II}}{\sum_jw_jI_j\omega_j},
\qquad 0<c_{\rm ad}^2<\frac13.}
\tag{1}
\]

More directly answering whether a small pressure also implies a small restoring response, the mixed harmonic-plus-quartic potential obeys the rigorous bound

\[
\boxed{c_{\rm ad}^2\leq\frac{2P}{E+P}
 =\frac{2w_{\rm exc}}{1+w_{\rm exc}},\qquad w_{\rm exc}=P/E.}
\tag{2}
\]

Both bounds apply to positive-weight mixtures with nonzero excitation in the stipulated common compression. Thus low excitation pressure bounds this bulk restoring coefficient; it is not merely a name assigned to a dustlike energy scaling. The two quantities can be computed from every saved mode without selecting a new occupation.

These are **thermodynamic/adiabatic derivatives within the adopted common-current closure**, not a demonstration of a microscopic propagation speed, a new spatial-gradient term, cosmological abundance or successful clustering. In units where the metric light speed is one, (1) is dimensionless. Calling it an actual mode speed requires the coupled spatial constraint/principal-system calculation that the local orbit model has not supplied.

## 1. Derivative under an owned common compression

Use the scalar phase action in `FIXED_ACTION_MODE_INTERFACE_V001.md` at zero acceleration source. The conserved currents give \(\nabla_\mu(I_j u^\mu)=0\). In a common local volume compression by a factor \(q\), all the existing actions therefore change to \(qI_j\), with their ratios unchanged. The mode weights and the declared mechanical coefficients are held fixed, as stipulated by this comparison parent; this is not a derived native change of spectral density with volume.

Excluding the unchanged vacuum constant and the common positive factor \(C\), define

\[
E(q)=\sum_jw_j e_j(qI_j,0),\qquad
P(q)=\sum_jw_j[qI_j\omega_j(qI_j,0)-e_j(qI_j,0)],
\quad\omega_j=e_{j,I}.
\]

At \(q=1\),

\[
\frac{dE}{dq}=\sum_jw_jI_j\omega_j=E+P,
\qquad \frac{dP}{dq}=\sum_jw_jI_j^2 e_{j,II}.
\tag{3}
\]

Their ratio proves (1)'s formula. The constant \(\Delta U\) has zero derivative and must not be inserted into this enthalpy denominator. A low ratio of pressure to **vacuum-dominated total energy** would not establish a low excitation compression coefficient. Equation (2) uses \(P/E\) for the excitation itself.

## 2. Exact positive curvature from one period integral

For one mode, let \(k=\kappa\delta^2>0\), \(m>0\), \(u=u_4>0\), and

\[
V(y)=\frac{k y^2}{2}+\frac{u y^4}{4},\qquad
e=V(b),\quad b>0.
\]

Use \(y=b\sin\theta\), \(0\leq\theta\leq\pi/2\), and define

\[
Q(\theta)=k+\frac{u b^2}{2}(1+\sin^2\theta),
\quad J=\int_0^{\pi/2}Q^{-1/2}d\theta,
\]

\[
K=\int_0^{\pi/2}(1+\sin^2\theta)Q^{-3/2}d\theta,
\quad L=\int_0^{\pi/2}\cos^2\theta\sqrt Q\,d\theta.
\]

The exact period, frequency and action are

\[
T=4\sqrt m\,J,\quad \omega=\frac{\pi}{2\sqrt m\,J},
\quad I=\frac{2\sqrt m}{\pi}b^2L,
\quad I_e=1/\omega.
\tag{4}
\]

All integrands are smooth and positive, including the turning-point endpoints. Differentiation gives

\[
J_b=-\frac{ub}{2}K,\qquad
\frac{\omega_b}{\omega}=\frac{ubK}{2J},\qquad
e_b=b(k+ub^2).
\]

Therefore

\[
\boxed{e_{II}=\omega\frac{\omega_b}{e_b}
 =\frac{\omega^2uK}{2J(k+ub^2)}>0.}
\tag{5}
\]

This is a proof of hardening at zero source, not an inference merely from positive inertia. The earlier finite-source displaced potential can soften; no extension of (5)'s sign to that different background is asserted.

## 3. A proven modal upper bound, with inexpensive pointwise brackets

Set \(r=ub^2/k>0\) and

\[
t(\theta)=\frac{ub^2(1+\sin^2\theta)}{2Q(\theta)}.
\]

The logarithmic derivatives

\[
\alpha=\frac{d\ln\omega}{d\ln b},\qquad
\beta=\frac{d\ln L}{d\ln b}
\]

are respectively positive normalized averages of \(t\) with weights \(Q^{-1/2}\) and \(\cos^2\theta\sqrt Q\). Hence

\[
\frac r{r+2}\leq\alpha,\beta\leq\frac r{r+1}.
\]

Since \(d\ln I/d\ln b=2+\beta\), the modal logarithmic stiffness is

\[
\zeta\equiv\frac{Ie_{II}}\omega=\frac{d\ln\omega}{d\ln I}
 =\frac\alpha{2+\beta}.
\]

It consequently satisfies the explicit bounds

\[
\boxed{\frac{r(r+1)}{(r+2)(3r+2)}\leq\zeta
 \leq\frac{r(r+2)}{(r+1)(3r+4)}<\frac13.}
\tag{6}
\]

The strict final inequality follows directly because
\((r+1)(3r+4)-3r(r+2)=r+4>0\). Equation (1) is the positive enthalpy-weighted average of these modal \(\zeta\)'s, so it inherits the bounds \(0<c_{\rm ad}^2<1/3\) for occupied modes with finite positive \(k,u\). Zero-action modes contribute zero enthalpy and are omitted only from ratios, not replaced by a population; an entirely empty state has no excitation sound ratio to define.

## 4. Low pressure bounds the restoring response

The zero-source virial identity gives

\[
I\omega=2\langle T_{\rm osc}\rangle,
\quad p=I\omega-e=\frac u4\langle y^4\rangle
 =\frac{ub^4}{4}M_4(r),
\tag{7}
\]

where \(M_4(r)\) is the mean of \(\sin^4\theta\) under the normalized time weight
\([1+r(1+\sin^2\theta)/2]^{-1/2}d\theta\).

The derivative of a normalized mean is a covariance. The weight's logarithmic derivative with respect to \(r\) is

\[
-\frac{1+\sin^2\theta}{4[1+r(1+\sin^2\theta)/2]},
\]

which decreases with \(\sin^2\theta\), whereas \(\sin^4\theta\) increases. Their covariance is nonpositive, so \(M'_4(r)\leq0\). Consequently

\[
\frac{d\ln p}{d\ln b}=4+2r\frac{M'_4}{M_4}\leq4,
\qquad \frac{d\ln I}{d\ln b}=2+\beta\geq2.
\]

Using the positivity from (5),

\[
0<I\frac{dp}{dI}=I^2e_{II}\leq2p.
\tag{8}
\]

Summing (8) with the unchanged positive weights and dividing by \(E+P=\sum wI\omega\) proves (2). No modal population assumption beyond the saved positive-action state is required. Together,

\[
0<c_{\rm ad}^2\leq\min\left\{\frac13,\frac{2w_{\rm exc}}{1+w_{\rm exc}}\right\},
\]

with the strict finite-positive-gap qualification in (6).

The limiting checks are independent and useful. For \(\omega_0=\sqrt{k/m}\),

\[
e=\omega_0I+\frac{3u}{8mk}I^2+O(I^3),\qquad
p=\frac{3u}{8mk}I^2+O(I^3),\quad
\zeta\sim2p/e.
\]

For the pure quartic limit \(e\propto I^{4/3}\), one has \(p=e/3\) and \(\zeta=1/3\). Neither limit is substituted for the actual mixed-potential modes in the proposed calculation.

## 5. Source preflight and concrete next readout

The complete prospective `prepared_compression_v001.py` and `PREPARED_COMPRESSION_PROTOCOL_V001.md` were read before execution. Their period/action normalizations, curvature (5), preserved 36-case census, pressure/period crosschecks, and positive enthalpy weighting agree with this derivation. The independent logarithmic-amplitude derivative check correctly differences the cancellation-free frequency excess \(\omega-\delta\) in the inherited \(m=\kappa=u=1\) units, rather than nearly equal full frequencies. Its Richardson refinement is a numerical check, not a changed state.

The same saved zero-source actions therefore determine both \(P/E\) and (1). Comparing those two complete outputs will decide whether this stipulated returned state is not only low-pressure but also weakly restoring under the owned common compression. It will not demonstrate a native spatial propagation law, select the cosmological abundance, validate adiabaticity for all gapless modes, or solve the coupled metric/clock constraints. Those distinctions preserve the useful result: the restoring response is now a calculable state property with rigorous bounds, not an independently chosen sound-speed parameter.
