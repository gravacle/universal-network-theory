# PRIMAT 2026 radiation interface: a qualified proxy, not an exact scalar map

2026-09-29. Additive source audit; no PRIMAT installation, import, nuclear
network, abundance interpolation or candidate scoring was executed here.
This qualifies the proposed interface in
`FINITE_GAP_BBN_DISCRIMINATOR_DESIGN_V001.md`, not its already fixed inputs.

## 1. Primary source and exact normalization

The [author's page](https://www2.iap.fr/users/pitrou/primat.htm) links both the
2026 abundance table and [official repository](https://github.com/CyrilPitrou/primat).
We inspected public commit `4bf97d5082eee54b9df50d88f43182bb651fea80`
(2026-09-01). Small source/data snapshots and their provenance are retained
under `bbn_inputs_v001/primat_source_reference/`; none is executed. The table
itself is separately pinned by SHA256
`48f864ecda028e7c7b4306c777bf694b9d3a214c920736894103d3163f7adec3`.
The current public generator passes column `DeltaN` directly to `DeltaNeff`.
Its current default Monte Carlo count differs from the published 1000-draw
receipt. Thus this is source/interface provenance, not a claim to have
reproduced the table's exact generating commit and invocation.

In the pinned Python `plasma.py` and C `plasma.c`, with temperature in MeV,

    sigma(T)=s_pl(T)/T^3,       sigma_inf=11 pi^2/45,
    T_dec(T)=[s_pl(T)/sigma_inf]^(1/3),
    rho_X,proxy=DeltaNeff (7 pi^2/120) T_dec^4.              (1)

After electron annihilation, sigma tends to sigma_gamma=4 pi^2/45. Hence

    rho_X,proxy/rho_gamma=DeltaNeff (7/8)(4/11)^(4/3).      (2)

This is the correct **late** normalization for these current sources. The
historical 2018 conversion slope between an old extra-neutrino parameter and
late effective neutrino number must not be substituted for (2).
The ordinary baseline is the table's 3.044, not an extra fitted offset.

## 2. Why the match is not exact during neutrino heating

Default `incomplete_decoupling=True` reads the fixed NEVO temperature/heating
and spectral-distortion tables. They do not depend on `DeltaNeff`.
Default `external_scale_factor=False` uses

    d ln a/d ln T=-(3 sigma+T sigma')/(3 sigma+N_heat).      (3)

The supplied heating table is linearly interpolated in T; negative numerical
tail samples are clipped to zero by the official implementation. Its own
comment documents this choice. We preserve the raw signed table and report
the clipping separately, rather than silently treating it as measured data.
Equations (1) and (3) imply

    d ln(a^3 s_pl)/d ln a=-N_heat/sigma,
    d ln(a^4 rho_X,proxy)/d ln a=-4 N_heat/(3 sigma).        (4)

The exactly conserved scalar radiation limit instead has a^4 rho_X constant.
With the same late normalization, define

    L(T)=(4/3) integral_[ln a(T)]^[ln a_end]
                         (N_heat/sigma) d ln a >=0.
    rho_X,proxy(T)=exp[L(T)] rho_X,conserved(T).            (5)

Thus the prescribed table history has *more* extra density before heating
than the conserved scalar with the same late density. This is not a sign
ambiguity or a neutrino free-streaming effect. The independently derived
scalar current a^3 I=constant and finite-gap energy bounds still stand.

The ordinary neutrino temperatures, spectral distortions and plasma heating
are also kept fixed while the added density changes H. This is an additional
fixed-neutrino-history approximation; the response of active-neutrino
decoupling to the changed expansion is not obtained by interpolating this
abundance table. Neither qualification proves that the correction is large.

## 3. A cheap conservative expansion-history certificate

No nuclear reaction calculation is needed to bound (5). The prospective
qualification reads only the official 600-row NEVO thermodynamic table,
2000-row electron table and two 500-row QED pressure tables. Reconstruct
their declared not-a-knot cubic interpolants using a standard tridiagonal
solve, with no imported PRIMAT code. Electron functions vanish below m_e/30
as in the source. The source's supplied derivative tables are independently
interpolated, so their derivative need not equal the derivative of the
interpolated entropy to machine precision. Do not erase that discrepancy.

Let C_t=T^(-2) d s_pl,interpolant/dT and C_s=T^(-2) ds_pl,supplied/dT.
For the actual supplied a(T) right-hand side, the exact log-ratio integrand is

    dL/d ln T=(4/3)[ N_heat C_t/{sigma(3sigma+N_heat)}
                              +3(C_t-C_s)/(3sigma+N_heat)]. (6)

The first term is heating; the second explicitly bounds thermodynamic
interpolation inconsistency. If E= rho_e+p_e, Q1=deltaP'_QED and
Q2=deltaP''_QED, all quantities in the following numerators are polynomials
on the union of the thermal-table intervals:

    T^4 sigma = sigma_gamma T^4+E+T Q1,
    T^4 C_t =3sigma_gamma T^4+T E'-E+T^2 Q1',
    T^4(C_t-C_s)=T(E'-D_e)+T^2(Q1'-Q2),                  (7)

where D_e is the supplied interpolation of rho'_e+p'_e. Polynomial
Bernstein convex-hull ranges and positive T^4 bounds give conservative
interval ranges, including cancellation in (7) *before* bounding. Integrate
these interval bounds in ln T; preserve both 4- and 8-subinterval results,
all signed drift and a declared floating-point padding. These are arithmetic
certificates for the pinned interpolants, not validated intervals for the
underlying QED calculation or experimental data. The pinned `constants.py`
sets s0bar=4 pi^2/45. The default `background.py` boundary is
a_end*T_end/T0=(sigma_end/s0bar)^(-1/3). Therefore the endpoint extra-density
factor (sigma_end/s0bar)^(4/3) cancels against the fourth power of that
scale-factor normalization. Both factors and their combined log are retained;
adding the entropy factor alone would double-count an endpoint correction.

At fixed ordinary history put q=rho_X,proxy/rho_ordinary. Then exactly

    H_proxy/H_conserved = sqrt[(1+q)/(1+q exp(-L))].        (8)

A certified lower bound on the positive plasma density, even without adding
positive ordinary neutrinos, bounds q from above. This yields a conservative
row-specific fractional H envelope. Finite-gap scalar energy adds its
independently bounded positive correction D/(Q A^2). In this inspected
thermal history A=(T/T0)(sigma/sigma_gamma)^(1/3)exp(-L/4), so the same
sigma/L bounds give a conservative A lower bound; do not call T/T0 an
exact scale factor while retaining neutrino heating elsewhere. The certificate must
not be translated into an abundance error by assuming that H and Yp or D/H
have the same fractional response. Their temperature-dependent kinetic
response has not been bounded here. Nor does (8) cover altered active-neutrino
reheating, unknown UV completion or changed ordinary nuclear rates.

## 4. What the next output will and will not claim

The root-authorized table comparison is explicitly a **fixed-heating table
proxy**, a separately prescribed expansion history. It retains all 360
source labels, all 18 conditional baryon/reference inputs and the matched
Delta=0 table comparator. Outside-grid rows remain unsupported; they are
neither extrapolated nor automatically excluded. The source energy/action
and late density coordinate are not adjusted to the abundance observations.

The exact conserved-scalar abundance prediction remains unqualified. The
output will show this limitation beside, not in place of, actual proxy
predictions and signed marginal residuals. A useful next repair is a
temperature-resolved BBN sensitivity/kernel or one explicitly altered
background calculation, together with a reheating-response qualification.
A uniformly small (8) alone is not a rigorous abundance-response theorem.

Cooke et al.'s [D/H product](https://arxiv.org/abs/1710.11129v3) is an exposed
calibration/consistency channel. Aver et al.'s
[helium regression, section 4.2](https://arxiv.org/html/2010.04180v1) is outside
that calibration but public, not blind. Their primordial nucleon-number
helium convention is paired with `Yp^BBN`, not atomic-mass `Yp`. No joint
covariance, joint significance or new baryon posterior is invented.
