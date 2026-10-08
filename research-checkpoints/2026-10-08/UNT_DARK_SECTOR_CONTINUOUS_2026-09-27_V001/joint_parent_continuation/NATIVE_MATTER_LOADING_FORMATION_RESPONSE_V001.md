# Native matter loading changes formation before any geometry assignment

2026-10-03. Analytic derivation followed by an independent exact-series check.
No trajectory, new physical coupling, imposed dilation or fit was introduced.
The sixth-order and fifth-order clock coefficients were recorded as provisional
before execution; root's independent Fraction-polynomial calculation now
verifies them, with **29/29 exact identities passing**. The earlier quartic
block identity also has an independent root derivation.

## 1. The matter interaction is already in BS, not a new gravity source

For the original tensor-site qutrit transfers, write carrier occupations as
`p_v`. BS07 gives the exact full-register identity

    J_uv^2=p_u+p_v-2p_u p_v.

This identity and its invariant fixed-content sector are already recorded in
`NATIVE_FORMATION_CLOSURE_ALGEBRA_PROPOSED_V001.md`, equations5 and11, and in
the subdivision-work notes. They are not newly discovered here. In that
sector the complete carrier energy includes

    epsilon_psi sum_v p_v
      +lambda_J sum_v d_v p_v
      -2lambda_J sum_(uv) n_uv p_u p_v
      -t_hop sum_(uv) n_uv T_uv.

Thus there is an owned attractive adjacent-occupation energy as well as
hopping, exclusion and a degree-dependent one-body energy. These are local
hard-core register matrices, not assumed fermionic CAR: no Jordan--Wigner
exchange signs may be inserted into the two-carrier sector.

For the SAME environment density and separately localized carrier loadings,
the exact initial connected energy is

    E_{u,v}-E_u-E_v+E_empty=-2lambda_J <n_uv>.

The hopping expectation vanishes in those localized preparations; carrier
storage and the terms linear in carrier occupation cancel. There is no such
direct term for a nonedge. This comparison retains preparation costs and
does not assert a ground-state binding energy, distance-dependent force or
free carrier clamp. Free evolution can change all ensuing correlations.

## 2. An exact initial link-response coefficient with all native terms

Take one BS slab, N nodes on each side and h=Omega/N. Prepare all links and
records blank, all writers occupied in the same content, and a definite
localized carrier occupation pattern S in that content. Keep g_wr=g>0 on;
set g_psi_r=g_rb=0 as an explicit writer-only protocol. No source port is
added. This changes the preparation/protocol from the old pulse-then-hold
experiment; it does not reinterpret its saved states.

For an edge e=(u,v), let d_u^bar,d_v^bar count its other incident links,
and define

    kappa0=Delta+2U_d(1-2d_*),
    C_e=p_u+p_v-2p_u p_v,
    D_e=kappa0 I+2U_d(d_u^bar+d_v^bar)
        -lambda_R(Q_u+Q_v)+lambda_J C_e-t_hop T_e.

Relative to the edge bit, the full Hamiltonian is exactly

    H=[[A,-h I],[-h I,A+D_e]].

A retains every other link flip, degree term, writer, record, carrier and
identity energy. It need not commute with D_e. For an initially blank edge
and any environment state, direct state-series multiplication gives

    <n_e>(tau)=h^2 tau^2/hbar^2
       -h^2[<D_e^2>+4h^2]tau^4/(12hbar^4)+O(tau^5).

There is no cubic term. The specified real blank product preparation makes
the probability even, improving the displayed remainder to O(tau^6).
For that preparation, C_e has eigenvalue c_e=0 or1, <T_e>=0, T_e^2=C_e,
and the other-degree/record terms annihilate the input. Therefore

    <D_e^2>=kappa0^2+c_e A_load,
    A_load=2kappa0 lambda_J+lambda_J^2+t_hop^2,

    <n_e>(tau)=h^2 tau^2/hbar^2
       -h^2[kappa0^2+4h^2+c_e A_load]tau^4/(12hbar^4)
       +O(tau^6).                                           (1)

This is a genuine native matter-loading effect without a fitted source.
It is not yet a record-feedback effect: lambda_R and g do not enter (1).
The t_hop^2 contribution is virtual carrier transfer and must not be assigned
to lambda_J. The loading variable is endpoint XOR: zero and two occupied
endpoints have c_e=0, one occupied endpoint has c_e=1. This is not a monotone
law of ordinary density or total carrier mass.

## 3. The same blank-degree record clock does not erase the difference

Fix the local readout once, with Q=diag(0,1) and conventional Pauli matrices:

    Delta0=sqrt(epsilon_r^2+4g^2),
    B0=[(epsilon_r X+2g Z)/Delta0-iY]/2,
    beta(0)=<B0>=g/Delta0>0.

For the actual full parent,

    [H,B0]=Delta0 B0-lambda_R d_v[Q_v,B0].

Put C=[Q_v,B0] and gamma=<d_v C>. On this initial product state,
gamma(0)=gamma'(0)=gamma''(0)=0: d_v annihilates the blank incidence input,
its first derivative is a sum of link-Y operators, and <C>_blank=0.
Thus beta agrees with beta(0)exp(i Delta0 tau/hbar) through cubic order.
Reality makes its first possible fourth-order correction real. The locally
unwrapped measured phase consequently satisfies

    theta(tau)=Delta0 tau/hbar+O(tau^5),

for every localized carrier loading. Nonzero amplitude and positive initial
rate give a local invertible clock by continuity, not a certified long-time
window. Equation(1) becomes

    <n_e>(theta)=h^2 theta^2/Delta0^2
       -h^2[kappa0^2+4h^2+c_e A_load]theta^4/(12Delta0^4)
       +O(theta^6).                                         (2)

For the inherited N=2 coefficients, h=1/2, kappa0=2, lambda_J=1/4,
t_hop=1/2, epsilon_r=g=1: the common leading term is theta^2/20, and the
one-loaded-endpoint minus zero-loaded-endpoint contrast is
`-7 theta^4/6400+O(theta^6)`. The two-carrier case must not use a one-carrier
current-square identity.

## 4. Smallest new record-mediated discriminator: the N=1 exact series

No new 1536D trajectory is necessary. In the N=1 continuing-writer cell,
the zero-, one- and two-carrier sectors have dimensions8,16,8. For g_psi_r=0,
zero and two carriers have IDENTICAL link/record evolution at all times:
hopping is blocked and their Hamiltonians differ only by 2epsilon_psi I.
The one-carrier initial left state gives equal weights to the two conserved
carrier-X bands. All required link/record readouts reduce to one eight-state
Hamiltonian,

    H_k=E_base I+epsilon_r(Q_L+Q_R)+g(X_L+X_R)
          -h X_a+n[k-lambda_R(Q_L+Q_R)].

Use k=kappa0 for P=0 or2; for P=1 average the k=kappa0+lambda_J-t_hop and
k=kappa0+lambda_J+t_hop results. This is an exact invariant decomposition,
not a static clamp, passive-state substitution or mean-link approximation.

Define the protocol-time double contrast

    D_time=[n_1(lambda_R)-n_0(lambda_R)]
                -[n_1(0)-n_0(0)].

Hand multiplication of the state series predicts

    D_time=h^2 g^2 lambda_J lambda_R tau^6/(10hbar^6)
                +O(tau^8).                                (3, verified)

For one endpoint record the intermediate contribution is
`h^2 g^2[k lambda_R/20-lambda_R^2/45]tau^6/hbar^6` to
`n(lambda_R)-n(0)`; the two record contributions add. Averaging the two
one-carrier bands cancels their t_hop split at this order. Equation(3)
therefore isolates joint matter/current and record feedback beyond (1).
Its sign and order are predictions to check, not correctness assumptions.

With x=tau/hbar, the same hand calculation gives, for either endpoint,

    <n[Q,B0]>=i h^2 g epsilon_r x^3/Delta0
                +h^2 g(-epsilon_r/2+lambda_R/3)x^4+O(x^5),
    theta(x)=Delta0 x
          -lambda_R h^2 Delta0(epsilon_r/10+lambda_R/15)x^5
          +O(x^7).                                    (4, verified)

These independently confirmed terms are independent of k and hence carrier
loading. Equal-phase comparison preserves (3) with tau^6/hbar^6 replaced
by theta^6/Delta0^6. At the inherited N=1 coefficients, h=1 and otherwise
as in section3, the predictions are

    n_1(theta)-n_0(theta)=-7 theta^4/1600+O(theta^6),
    D_phase=theta^6/10000+O(theta^8).                  (5, verified)

Root's sole calculation used exact Fraction-polynomial multiplication of
these 8D matrices, with a direct original 16D carrier-band check, through the
necessary finite order. No selected observation time, trajectory fit, new
coupling or thermal reset was needed. The question and coefficients above
preceded that check. The g=0 control has valid protocol-time coefficients but
beta=0: its record clock and equal-phase quantities are UNDEFINED.

The polynomial identities hold with h,g,k,epsilon_r,lambda_R,lambda_J,t_hop
left symbolic, not merely at a few selected parameter values. Root checked
the same fourth-order result directly from the noncommuting block expansion.
Agent endpoint_equations_check separately reviewed the original register
indexing, conventional Pauli-Y signs, carrier-band equivalence and phase
extraction, and independently derived the displayed gamma coefficients.
The worker's 29 checks include the full versus band-reduced result and all
prospectively stated sixth-order and clock identities. This is exact finite
algebra checked by code and hand derivations, not a long-time series-error
certificate, laboratory observation or proof of a macroscopic phase change.

- Source `native_matter_loading_series_v001.py` SHA256:
  `606ce802d5b24b67f58661a604eda9b5850a21213b6c3f2e277ccebbabf1c92c`.
- Result `native_matter_loading_series_v001_results.json` SHA256:
  `e5ef11d9edde62b251464f08dd1478932ca17f1e226d3affd2ed17e0c78d0301`.
- Runtime: 0.0214958 seconds; 22,462,464 bytes peak self RSS. No floating-point
  allowance enters the polynomial equalities. Runtime measurements are not
  part of their proof.

## 5. Energy and the next physical boundary

Initial complete energy is `2N U_d d_*^2+P epsilon_psi+2N epsilon_w` for the
stated blank-link/record preparations. Copy and hopping expectations vanish
initially, not as operator identities. The subsequent full energy is conserved;
writer/record, incidence and carrier currents exchange it. In particular,
`E_2(t)-2E_1(t)+E_0(t)=0` here at every time. This does not remove the
interactions; it prevents interpreting redistribution as newly supplied
binding energy. Loading, localization and readout require an owned preparation
port before being advertised as an autonomous laboratory cycle.

The inherited energy-dipole experiments test an adopted external weak lapse;
they do not calculate this endogenous carrier-loading response. The previous
formation-closure note owns its operators and onset hierarchy, but the checked
resident notes do not already contain (1)--(5) as a common-clock matter-loading
discriminator. Root independently derives/checks the new coefficients rather
than rerunning the old pulse/hold experiment.

This is a constructive intermediate for an actual matter-source model. It is
not a long-range attractive force, equivalence principle, metric volume,
spatial dimension, accelerating expansion or dark-sector closure. N=1 cannot
test separation dependence. With the exact series now verified, the next
substantive question is whether spatially separated loading alters another native probe
through the SAME formed link/record state beyond hard-core exclusion and the
explicit adjacent pair term, retaining full preparation energy. Do not infer
that answer from count, the sign of (3), or a separately chosen dilation q(t).
All eleven mandatory lanes remain OPEN.

The user's intended explanation is a change in effective gravitational
behavior of the network, not a halo made of accumulated records. This note
supports investigating an endogenous matter-dependent response and isolates
where record feedback enters; it assigns no fraction of the inferred dark
mass or energy to records. The fourth-order effect exists before the
record-feedback contribution. Neither effect is yet a gravitational coupling.
The full physical energy must still be retained: avoiding a record halo does
not justify dropping record or identity terms from an eventual source law.
