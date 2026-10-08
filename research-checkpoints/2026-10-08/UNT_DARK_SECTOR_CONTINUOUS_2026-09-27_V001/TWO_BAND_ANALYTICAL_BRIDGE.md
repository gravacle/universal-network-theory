# Exact two-band bridge for the actual native formed state

2026-09-27. Analytical derivation only; the root remains the sole numerical worker. Resident inputs read: [dressed protocol](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/dressed_probe/PROTOCOL.md>), [saved results](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/dressed_probe/RESULTS.json>), [diagnostic source](</Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/dressed_probe/compute_dressed_probe.py:63>), and the preceding dressed-bridge review. No new cosmological volume or physical cooling process is assumed.

The saved calculation reports lower-band weight \(0.8694500862561787\), upper-band weight \(0.1305499137438213\), and a positive global separating gap. Therefore the constructive next model keeps both bands and their coherences. Projection and renormalization into the lower band would change the state being explained.

## 1. Exact change of coordinates, with no population discarded

At fixed record occupation \(q\), the inherited hold Hamiltonian is
\[
H_q=C_qI-hX_a+(b_q-jX_C)n,\quad
h=1,\quad j=\tfrac12,\quad
b_q=\tfrac94-\tfrac12q,\quad C_q=3+q.
\]
Writer/content labels remain spectators with their existing multiplicities. For carrier-\(X\) eigenvalue \(s=\pm1\), define
\[
x_s=b_q-js,\qquad d_s=\sqrt{x_s^2+4h^2},\qquad
E_{\beta s}=C_q+\frac{x_s+\beta d_s}{2},\quad \beta=\pm1.
\]
Here \(\beta=-1\) is the lower link branch and \(\beta=+1\) the upper. Choose
\[
\theta_s=\operatorname{atan2}(2h,x_s),\qquad
|u_{-,s}\rangle=
\begin{pmatrix}\cos(\theta_s/2)\\ \sin(\theta_s/2)\end{pmatrix},
\quad
|u_{+,s}\rangle=
\begin{pmatrix}-\sin(\theta_s/2)\\ \cos(\theta_s/2)\end{pmatrix}.
\]
The full four-column map \(U_q|\beta,s\rangle=|u_{\beta,s}\rangle\otimes|s\rangle_X\) is unitary. Including every record/writer block yields an exact unitary coordinate change on the native 36-dimensional space. It gives
\[
\widetilde\rho_{\beta s,\gamma s'}(t)
=\widetilde\rho_{\beta s,\gamma s'}(0)
e^{-i(E_{\beta s}-E_{\gamma s'})t}.
\]
No assumption of ground-state formation, Markovian evolution, weak coupling, or decoherence enters this expression. Cross-record coherences can likewise be retained with their full energy differences; the two observables below commute with record occupation and do not read those coherences.

Let \(P_L,P_U\) be the full invariant lower/upper projectors and \(w_U=\eta\). Both weights are exactly constant during hold. The norm of the interband block is also constant:
\[
\|P_L\rho(t)P_U\|_1=\|P_L\rho(0)P_U\|_1.
\]
Thus waiting at a fixed time does not suppress this coherence in trace norm, and cannot reduce the existing upper-band population. Finite spectra produce oscillations and recurrences; no cooling or irreversible relaxation is implied.

## 2. Bare observables must also be transformed

For each \(s\), bare link occupation in the band basis is
\[
U_q^\dagger nU_q\big|_s=
\begin{pmatrix}
(1-x_s/d_s)/2 & h/d_s\\
h/d_s & (1+x_s/d_s)/2
\end{pmatrix}.
\]
Its oscillating expectation reads the lower–upper coherences at fixed \(s\), at frequency \(d_s\). Its diagonal contribution retains both band populations.

Use \(Z_C=|L\rangle\langle L|-|R\rangle\langle R|\), so \(P_R=(1-\langle Z_C\rangle)/2\). In the carrier-\(X\) basis, \(Z_C\) connects \(s=+\) to \(s=-\). Its band matrix elements are
\[
M_{\beta\gamma}=\langle u_{\beta,+}|u_{\gamma,-}\rangle
=\begin{pmatrix}\cos\delta&-\sin\delta\\
\sin\delta&\cos\delta\end{pmatrix}_{\beta\gamma},
\quad
\delta=\frac{\theta_--\theta_+}{2},
\]
where rows and columns are ordered lower, upper. Hence the exact contribution from a record sector, using its **unnormalized** density block, is
\[
\langle Z_C(t)\rangle_q
=2\operatorname{Re}\sum_{\beta,\gamma}
\widetilde\rho_{\beta,+;\gamma,-}(0)\,
M_{\beta\gamma}\,
e^{-i(E_{\beta,+}-E_{\gamma,-})t}.
\]
Sum these expressions over the actual record/writer blocks. The overlap factors are part of a physical bare-site readout; they cannot be discarded by calling the dressed labels physical carrier positions.

## 3. A falsifiable relation between link and carrier responses

At fixed \(q\), link occupation has only a constant term and the two possible positive frequencies \(d_+\) and \(d_-\). The allowed positive frequencies of the bare carrier \(Z_C\) response are
\[
\boxed{
\nu_L=j-\frac{d_--d_+}{2},\qquad
\nu_U=j+\frac{d_--d_+}{2},\qquad
\omega_{\rm lo}=\frac{d_-+d_+}{2}-j,\qquad
\omega_{\rm hi}=\frac{d_-+d_+}{2}+j.}
\]
They are respectively the same-lower-band, same-upper-band, and two cross-band carrier transitions. All four are positive for the inherited \(h,j,b_q\). In particular,
\[
\boxed{\nu_L+\nu_U=2j,\quad
\omega_{\rm hi}-\omega_{\rm lo}=2j,\quad
\nu_U-\nu_L=d_--d_+,\quad
\omega_{\rm hi}+\omega_{\rm lo}=d_-+d_+.}
\]
These relate two independently read observable responses with a single already fixed microscopic hopping parameter. At native \(j=1/2\), the first sum and the fast-line difference are exactly \(1\), in the existing Hamiltonian time units. The link gaps themselves are fixed radicals:
\[
(d_+,d_-)_{q=0}=(\sqrt{113},\sqrt{185})/4,\qquad
(d_+,d_-)_{q=1}=(\sqrt{89},\sqrt{145})/4.
\]
The proposed test therefore needs no additional frequency normalization, selected ground state, or abundance fit. It is more informative than comparing only a lower-band effective hopping.

These are allowed spectral lines, not promises that every line has nonzero amplitude. A particular initial coherence, or a matrix element, can vanish. The actual saved state's transformed density matrix fixes every amplitude and phase before the response is compared; upper-band population by itself does not guarantee a visible upper-band oscillation. Aggregating the two \(q\) sectors gives the union of their lines, and accidental coincidences must be combined rather than counted as independent peaks.

## 4. What time averaging can and cannot recover

Define a uniform, explicitly reported observation window
\[
\overline\rho_T(t_0)=\frac1T\int_{t_0}^{t_0+T}
e^{-iHt}\rho e^{iHt}\,dt.
\]
An energy coherence with \(\omega=E-E'\) receives the exact factor
\[
e^{-i\omega(t_0+T/2)}
\operatorname{sinc}(\omega T/2),\qquad
|\operatorname{sinc}(\omega T/2)|
\le \min\left(1,\frac{2}{T|\omega|}\right)
\quad(\omega\ne0).
\]
This is averaging, not a change in the microscopic hold dynamics. The infinite-window limit is
\[
\mathcal D_H(\rho)=\sum_E P_E\rho P_E.
\]
It preserves every energy population, including the full 13.05% upper-band weight, and preserves coherences **inside each exactly degenerate energy space**. Writer/content degeneracies already exist. Nonzero near-degenerate splittings require proportionately longer observation windows; no uniform finite-time claim should substitute a guessed gap for the actual spectrum.

For any observable, a directly checkable finite-window error bound is
\[
\left|\operatorname{Tr}O(\overline\rho_T-\mathcal D_H\rho)\right|
\le\sum_{E\ne E'}
\left|\operatorname{Tr}(O P_E\rho P_{E'})\right|
\min\left(1,\frac{2}{T|E-E'|}\right).
\]
Its coefficients come from the saved state, not a fitted relaxation rate. A looser state-independent bound is
\[
\|\overline\rho_T-\mathcal D_H\rho\|_1
\le\min\left(2,\frac{2(m-1)}{T\delta_*}\right),
\]
where \(m\) is the number of distinct energies and \(\delta_*\) their smallest nonzero separation. Native spectator multiplicities do not inflate \(m\); there are at most eight distinct \(q,\beta,s\) energies here.

For this native hold, the infinite-window bare-site probability is exactly
\[
\boxed{\overline P_R(\infty)=\tfrac12}
\]
for every initial state. The reason is that \(Z_C\) only connects opposite \(s\), and all its coupled energy differences are nonzero within a fixed \(q\); it has no surviving zero-frequency term. This does **not** imply a maximally mixed carrier: \(X_C\) is conserved. The averaged link occupation instead keeps the actual diagonal band weights:
\[
\overline{\langle n\rangle}(\infty)
=\sum_{q,\beta,s}w_{q\beta s}
\frac{1+\beta x_s/d_s}{2}.
\]
The first equality must not be promoted to a thermalization claim, and the second cannot be replaced by a ground-state occupation.

## 5. Bounded interband dephasing without ground projection

If only interband coherence is to be omitted, use
\[
\mathcal B(\rho)=P_L\rho P_L+P_U\rho P_U.
\]
This retains both populations and all intraband coherences. Comparing its **window-averaged** predictions with the full window-averaged state has a useful dimension-independent bound:
\[
\boxed{
\|\overline\rho_T-\overline{\mathcal B(\rho)}_T\|_1
\le2\|P_L\rho P_U\|_1
\min\left(1,\frac{2}{T\Gamma}\right)
\le2\sqrt{w_Lw_U}
\min\left(1,\frac{2}{T\Gamma}\right).}
\]
Here \(\Gamma=\min\operatorname{spec}H_U-\max\operatorname{spec}H_L>0\). The native value has the exact form
\[
\Gamma=\frac{\sqrt{113}+\sqrt{145}-10}{8},
\]
consistent with the saved result. To obtain the bound, integrate the interband block and invert the Sylvester map \(Y\mapsto H_LY-YH_U\); ordered band separation bounds that inverse in trace norm by \(1/\Gamma\). The endpoint difference contributes at most \(2\|P_L\rho P_U\|_1/T\). The Hermitian pair of cross-blocks doubles the norm.

Large \(T\) also averages intraband dynamics. Therefore this result does not justify comparing a long-window average to an instantaneous two-band trajectory. If that comparison is required at the window midpoint \(t_c\), a further valid bound is
\[
\|\overline{\mathcal B(\rho)}_T-
e^{-iHt_c}\mathcal B(\rho)e^{iHt_c}\|_1
\le \frac{T^2}{24}
\left(w_L\Delta_L^2+w_U\Delta_U^2\right),
\]
where \(\Delta_L,\Delta_U\) are the spectral widths of the two bands. It follows from the symmetric Taylor remainder and
\(\|[H_B,[H_B,\rho_B]]\|_1\le\Delta_B^2\|\rho_B\|_1\).
One needs a genuine separation of time scales to make both this smearing error and the interband averaging error small. The existence of a nonzero band gap alone does not establish such a window.

## Next exact test

Use the saved native formed density matrix without projection, apply the full two-band coordinate change, and predict both bare link occupation and bare carrier-right response from their fixed spectral coefficients. Verify the four frequency relations above and then check any declared finite averaging window against its sinc-weighted error bound. This tests whether the existing mechanism supplies a shared operational clock/propagation relation while retaining the actual excited population. It makes no cosmological volume assignment and does not establish a spacetime metric.
