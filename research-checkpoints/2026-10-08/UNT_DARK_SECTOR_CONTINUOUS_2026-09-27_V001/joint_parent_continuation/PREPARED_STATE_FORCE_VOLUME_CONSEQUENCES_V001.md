# Prepared-state force normalization and the retained energy ledger

2026-09-28. An additive consequence of the same conditional scalar mechanical parent. No galaxy fit, parameter change, new field solve, dissipative reset, or alteration of earlier frozen evidence.

## 1. A definite same-parameter response coefficient

The new quench/finite-ramp result concerns the infinite-time held-source mean of an initially resting conservative scalar continuum. It is not yet a coupled metric/clock solution. Retain all original parameters and write

\[
\nu(\delta)=A\delta,\quad 0<\delta<\Lambda,\qquad
K_b=A\kappa\Lambda^2/2,
\quad h(g)=\frac{g}{\sqrt{1+g^2/g_s^2}}.
\]

For each mode the held Hamiltonian, excluding the ordinary quadratic source contact, is

\[
\epsilon_\delta(p,y;h)=\frac{p^2}{2m_\delta}
 +\frac{\kappa\delta^2y^2}{2}+\frac{u_4y^4}{4}
 -\kappa\delta h y.
\tag{1}
\]

The source-conjugate mean polarization and normalized source force are

\[
\bar P(h)=\int\nu\kappa\delta\langle y\rangle\,d\delta,
\qquad \bar D(g)=g-\frac{h'(g)}{K_b}\bar P(h(g)).
\tag{2}
\]

The periodic mode equation implies

\[
\kappa\delta^2\langle y\rangle+u_4\langle y^3\rangle
 =\kappa\delta h,
\quad
\bar D=g-hh'+\frac{A u_4h'}{K_b}\int\langle y^3\rangle d\delta.
\tag{3}
\]

In the small-source continuum scaling,

\[
\delta=(u_4/\kappa)^{1/4}\sqrt h\,s,\qquad
y=(\kappa/u_4)^{1/4}\sqrt h\,Y,
\]

the scaled potential is \(V_s(Y)=s^2Y^2/2+Y^4/4-sY\). A zero-rest quench has energy zero and turning interval \([0,b]\), with \(b^3+2s^2b-4s=0\). The coefficient calculation gives

\[
C_q=\int_0^\infty\langle Y^3\rangle_s ds
 =0.951821896774069,
\quad C_{\rm rel}=3\pi/16=0.5890486225480862.
\]

Therefore

\[
\bar D(g)\sim\frac{A\sqrt{\kappa u_4}}{K_b}C_q g^2,
\quad D_{\rm rel}(g)\sim\frac{g^2}{a_{0,\rm rel}},
\]

\[
\boxed{\gamma=\frac{C_q}{C_{\rm rel}}=1.615863038023433,
\qquad a_{0,\rm mean}=\frac{a_{0,\rm rel}}\gamma
 =0.618864332229065\,a_{0,\rm rel}.}
\tag{4}
\]

The bounded-source contact \(g-hh'=2g^3/g_s^2+O(g^5/g_s^4)\) is subleading and does not change (4). The proved analytic bounds \(\sqrt2<\gamma<5\sqrt2/4\) independently fix the direction of the shift. For the unchanged inherited \(a_{0,\rm rel}=1.2\times10^{-10}\) m s\(^{-2}\), the conditional mean coefficient corresponds to approximately \(7.42637\times10^{-11}\) m s\(^{-2}\). This is an output of the stipulated preparation, **not permission to relabel or refit the frozen acceleration scale**. The original physical \(g_s\), cutoff and microscopic parameters stay unchanged.

The associated theorem extends the deep coefficient to zero-rest monotone ramps of any fixed bounded duration, followed by the infinite-time held mean, in its stated continuum domain. This extension uses the common positive inertia of the qualified scalar worker (\(m_\delta=1\) in its units). The quench orbit coefficient itself is independent of each positive inertia because the period factor cancels, but arbitrary gap-dependent inertias can change which modes are sudden and are not covered by that finite-ramp extension. The theorem does not say that every finite source value, finite observing time, gapped realization, or native state follows the quench curve. In particular, averaging time, vanishing source and vanishing gap limits must not be interchanged without the theorem's controls.

If a future coupled solution establishes this local mean law and reaches its ideal deep spherical window, it would imply \(v_\infty^4=GM_ba_{0,\rm mean}\), rather than the relaxed coefficient. That conditional scaling is not a calculation of either observed disk: no saved disk velocities or fields have been rescaled here. Disk geometry, the clock constraints and finite-field response must still be solved for the actual prepared state.

## 2. Why the vacuum endpoint cannot be recalculated from this mean curve

Define the scalar action of a periodic bound orbit by

\[
I_\delta=\frac1{2\pi}\oint p\,dy,
\qquad \omega_\delta=\left.\frac{\partial\epsilon_\delta}{\partial I_\delta}\right|_h.
\]

The exact fixed-action derivative is

\[
\left.\frac{\partial\epsilon_\delta}{\partial h}\right|_{I_\delta}
 =-\kappa\delta\langle y\rangle.
\tag{5}
\]

It follows by differentiating the action integral: \(\partial I/\partial\epsilon=T/(2\pi)\), and \(\partial I/\partial h|_\epsilon=(T/2\pi)\kappa\delta\langle y\rangle\). No bath, temperature or phase selection is used.

But a set of separately prepared ramps to different final amplitudes generally has **different actions** \(I_\delta(h)\). Put \(E(h)=\int\nu\epsilon_\delta(I_\delta(h),h)d\delta\). The exact chain rule is

\[
\frac{dE}{dh}=-\bar P(h)
 +\int\nu\omega_\delta\frac{dI_\delta}{dh}d\delta.
\tag{6}
\]

Consequently

\[
\int_0^{g_s}\bar P(h)dh
 =E(0)-E(g_s)
 +\int_0^{g_s}dh\int\nu\omega_\delta I'_\delta(h)d\delta.
\tag{7}
\]

The last term cannot be discarded. Integrating the force curve across a family of newly prepared states is not equivalent to differentiating one relaxed energy function or varying a fixed-action state. Along a smooth family it records the energy change caused by varying the actions; it is not automatically the mechanical work of a single physical trajectory through that family.

The exact quench is especially transparent. Immediately after each source jump, \(y=p=0\), so

\[
\epsilon_\delta(h,I_{q,\delta}(h))=0
\quad\hbox{for every final }h.
\]

Thus

\[
\kappa\delta\langle y\rangle
 =\omega_\delta I'_{q,\delta}(h),
\tag{8}
\]

and the nonzero mean-force area in (7) is entirely the action-family term, despite the equal zero energy of all these quenched Hamiltonians. Calling that area a new vacuum endpoint would be an exact accounting error.

The original relaxed matching remains

\[
E_{\min}(0)=0,\quad E_{\min}(g_s)=-\Delta U,
\quad \Delta U=\int_0^{g_s}P_{\rm rel}(h)dh.
\tag{9}
\]

For the quenched state, its positive excitation above the same minimum is

\[
E_{\rm exc}(h)=E_q(h)-E_{\min}(h)=-E_{\min}(h),
\quad E_{\rm exc}(g_s)=\Delta U.
\tag{10}
\]

The constant in the action is unchanged, but the state is no longer the ground state used for the high-source cancellation. Its energy and pressure must remain in the source/metric equations. At nonzero acceleration the full stress also contains the coupling, acceleration and polarization-divergence terms; it is not simply an isotropic vacuum density obtained by averaging (10). A retained ground baseline plus a populated state must not be described as vacuum-only stress.

## 3. Universal deep response is not a universal population

There is a concrete noncommuting-limits issue. A fixed finite ramp becomes sudden relative to the soft modes that determine the \(g\to0\) continuum coefficient. Conversely, at any fixed nonzero source, each individual \(\delta>0\) mode follows the minimum under a sufficiently slowly stretched smooth ramp. The excitation is bounded by the ground-energy lowering, which is integrable down to \(\delta=0\) with the fixed finite upper cutoff. Dominated convergence therefore gives vanishing integrated excitation for this adiabatic limit of the continuum itself. **Both limits in (11) refer to the zero-lower-cutoff continuum with fixed upper cutoff \(\Lambda\)** (equivalently, the lower gap is removed before the weak-field limit), with the held-time mean taken as stipulated:

\[
\lim_{g\to0}\lim_{T_{\rm ramp}\to\infty}\frac{\bar D}{g^2}
 =\frac1{a_{0,\rm rel}},
\qquad
\lim_{T_{\rm ramp}\to\infty}\lim_{g\to0}\frac{\bar D}{g^2}
 =\frac\gamma{a_{0,\rm rel}}.
\tag{11}
\]

Keeping any fixed \(\delta_{\min}>0\), with the contact matched to that retained band as in the existing finite-band worker, instead gives the strict weak-field behavior \(\bar D=O(g^3)\), hence \(\bar D/g^2\to0\). Keeping the excluded modes' old contact would introduce an unmatched linear floor, a different model again. Neither is the ordering in (11). The continuum statement requires the smooth stretched-ramp family and the stated scalar assumptions, not arbitrary increasingly irregular source histories. It explains why one robust deep-response coefficient can coexist with different excitation energies and finite-field responses. The coefficient alone does not specify \(I_\delta(h)\) or a cosmological mode abundance.

There is nevertheless a productive joint interface. At zero homogeneous acceleration, a finite scalar mode with a slowly evolving FLRW background has conserved comoving action \(a^3I_\delta\), and

\[
\rho_{\rm exc}=C\int\nu\epsilon_\delta(I_\delta,0)d\delta,
\quad
p_{\rm exc}=C\int\nu\left(I_\delta\omega_\delta-\epsilon_\delta\right)d\delta.
\tag{12}
\]

The same prepared actions then determine both this energy ledger and the fixed-action polarization (5). Quadratic and quartic limits reproduce dustlike and radiationlike pressures. This is the constructive way to couple the two sectors—derive a physical preparation, preserve its actions/energy where adiabaticity is justified, and calculate both outcomes. It is not a separate choice of a galaxy-response floor and a cosmological density.

The qualifications are substantive: adiabaticity is mode-by-mode and not uniform at a zero-gap endpoint; the scalar fixed-direction aligned subspace is not a proof of integrability for vector modes under a changing source direction; and the adopted fixed physical mode-density convention is not a native volume derivation. At nonzero homogeneous acceleration the simple isotropic pressure formula (12) must not replace the full metric variation. `FIXED_ACTION_MODE_INTERFACE_V001.md` supplies the complementary action-level derivation.

## 4. What can now be claimed

This calculation supplies a new, parameter-free **preparation-dependent coefficient of the specified Hamiltonian**, with a sign and magnitude that the relaxed minimum misses. It makes the conservative prepared-state program more predictive.

It is not yet a joint prediction of a galaxy curve and \(H(a)\). The actual clock/source/record preparation, its physical time and energy transfer, its cosmological occupation and its coupled gravitational response remain inputs to derive. The exact unexcited geodesic-clock branch and the homogeneous zero-production result in `COSMOLOGY_CLOSURE_TEST_V001.md` still hold. A clamped acceleration experiment does not itself populate a homogeneous universe.

No silent recalibration of \(a_0\), \(g_s/a_0\), \(\Delta U\), the stored galaxy fields, or the cosmological reference is warranted. The next scientifically useful calculation retains the common prepared state while solving the constraint and energy equations, rather than using the new coefficient as a velocity correction after the fact.

## Recorded numerical provenance

The coefficient and all four quadrature orders were read from the root's complete `QUENCH_MEAN_COEFFICIENT_V001.json`; no coefficient worker was rerun for this note. The source was read and its SHA-256 independently checked against the result's source field:

- Source: `428da77db4629d943a0ad65a6df62a82d2be19bfd6cff3c4e5bd66c72676015c`.
- Result bytes: `52252d655e366dde098072285b5673a680f44e98e9b551b9a827dc2ce005e749`.

The original relaxed endpoint relation and the action-family identities above are analytical. The finite-ramp universality theorem and independent coefficient check belong to the separate audit lane; this note records their same-parameter consequences without changing the frozen law or observational comparisons.
