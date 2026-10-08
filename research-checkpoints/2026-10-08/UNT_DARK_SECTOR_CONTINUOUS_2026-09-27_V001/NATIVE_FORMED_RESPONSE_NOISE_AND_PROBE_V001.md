# Formed-link response, noise, and the carrier's missing mean-field term

2026-09-27. Exact analytic continuation of
`NATIVE_FORMED_NETWORK_RESPONSE_BRIDGE_V001.md`. Same BS one-link
formation endpoint, same coefficients, copying off, no bath and no new
interaction. This note adds fluctuation predictions; it does not replace
the finite-time carrier's native backreaction by a noise model.

## 1. Two-time fluctuations of the actual formed pure state

Keep H_hold=(C+epsilon)I-epsilon n-hX, initial |n=1>,
R=sqrt(epsilon^2+4h^2), omega_0=R/hbar, and L=4h^2/R^2.
Set

    z(t)=1-L+L cos(omega_0 t),
    m(t)=<n(t)>=[1+z(t)]/2.

The connected symmetrized correlation of this actual state is exactly

    S_F(t,t')=1/2<{n(t)-m(t),n(t')-m(t')}>
      =1/4{1-L+L cos[omega_0(t-t')]-z(t)z(t')}.             (1)

To derive (1), write n(t)=(I-v(t).sigma)/2. The vectors v(t) rotate
about the fixed Hamiltonian axis; their scalar product is
1-L+L cos[omega_0(t-t')], while the initial Bloch vector gives z(t).
The antisymmetric part is independently fixed by the retarded kernel:
for t>=t',

    <delta n(t) delta n(t')>
                  =S_F(t,t')-i hbar chi_F(t,t')/2.          (2)

Thus the same h and epsilon and the actual preparation age fix the full
connected two-point function, not merely a stationary susceptibility.
In particular S_F(t,0)=0 and chi_F(t,0)=0: the endpoint is an n eigenstate.
At equal times S_F(t,t)=m(t)[1-m(t)], as required by n^2=n.

## 2. An independently prepared phase mixture has a fixed noise spectrum

For a uniform, unrecorded formation-age phase on one hold period, the
stationary density matrix has energy populations

    p_g=(1+w)/2,       p_e=(1-w)/2,
    w=epsilon/R=sqrt(1-L)>0,
    m_bar=1-L/2.                                          (3)

In the energy basis, |n_ge|=h/R, and n_gg-n_ee=w. Direct spectral
expansion yields the unordered connected correlator

    Q_bar(u)=<delta n(u)delta n(0)>_bar
      =L(1-L)/4 +(L/4)[p_g exp(-i omega_0 u)
                                     +p_e exp(i omega_0 u)], (4)

and therefore

    S_bar(u)=L(1-L)/4 +(L/4)cos(omega_0 u),
    chi_bar(u)=theta(u)[L sqrt(1-L)/(2hbar)]sin(omega_0 u).
                                                               (5)

Equation (4) fixes both transition weights and their ratio:

    W_negative/W_positive=p_e/p_g
                  =[1-sqrt(1-L)]/[1+sqrt(1-L)],             (6)

where positive/negative refer to the Fourier convention
Q(omega)=integral exp(i omega u) Q(u) du. The sign convention is stated
to avoid identifying detector absorption/emission with an unstated one.
Both nonzero-frequency weights have total L/4 before the common Fourier
delta-function normalization; their difference is L sqrt(1-L)/4.

The constant L(1-L)/4 is the variance of the energy-diagonal part of n
under the mixture. It is a zero-frequency delta contribution in this
finite closed system, not a new slow resonance, damping mechanism, or
cosmological mode. A ground-state replacement would remove this term
and replace the population difference w by one. It would therefore
change both the independently testable response and the noise relation.

One may formally write p_e/p_g=exp(-beta_eff R) for this single gap,
but this introduces no bath and proves no common temperature across
different links or different gaps. Equations (3)-(6) need no temperature
interpretation.

The same unforced leakage and gap that fixed the response amplitude in
the bridge note now fix these noise weights. This is an additional
held-out prediction with no fitted noise strength or effective damping.

## 3. Phase averaging and connected subtraction do not commute

The stationary correlation (5) subtracts the stationary mean m_bar.
Averaging the correlations individually connected to each known-age
pure state instead gives

    average_w S_F(w+u,w)
      =L(1-L)/4 +[L(2-L)/8]cos(omega_0 u).                  (7)

Their difference is the classical covariance of the phase-dependent
means:

    S_bar(u)-average_w S_F(w+u,w)
      =average_w{[m(w+u)-m_bar][m(w)-m_bar]}
      =(L^2/8)cos(omega_0 u).                              (8)

For a known deterministic preparation age, use (1), not (5). For an
unrecorded phase mixture use (5), not (7). Retarded response is linear
in the state and needs no connected-mean subtraction, so its uniform
phase average is exactly the stationary response in (5).

## 4. The carrier curvature directly exposes the missing fluctuation

Inject a fresh localized carrier after waiting w. With all native flips
retained, the exact link-transfer curvature is

    kappa_exact(w)=t_hop^2 m(w)/hbar^2.                     (9)

A deterministic replacement n -> m(w) in the hopping amplitude would
predict kappa_mean=t_hop^2 m(w)^2/hbar^2. Their difference is exactly

    kappa_exact-kappa_mean
       =t_hop^2 Var[n(w)]/hbar^2
       =t_hop^2 S_F(w,w)/hbar^2.                          (10)

For the actual phase mixture replace m(w) by m_bar and use S_bar(0):
the missing term is t_hop^2 L(2-L)/(4hbar^2). This is not an adjustable
correction to the carrier Hamiltonian; it is the consequence of n^2=n
in the full quantum preparation. At the exact formation endpoint the
variance and this particular correction vanish, but they reappear
during a nontrivial hold or in the phase-mixed preparation.

Equations (1)-(10) give a small three-probe check: determine the hold
leakage/gap from one unforced experiment, then predict both the independent
source response and the carrier curvature/noise relation. No numerical
experiment is executed here. For finite carrier times use the exact
two-parity-sector overlap in the bridge note; two-point data alone do
not imply a Gaussian bath, a Markov reduction, or a common clock for all
carrier spectral lines.
