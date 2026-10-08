# Compact-dwarf bound for direct bounded contact plus mode stiffness

2026-10-05 UTC. New conditional bound for the unadopted direct bounded-h
plus positive MODE-gradient hybrid in BOUNDED_MODE_GRADIENT_CONTACT_GATE_V001.
It is not the already tested filtered-INPUT parent and no old solve is rerun.
The hybrid retains the bounded uniform energy endpoint but its unsmoothed
field contact already has an unfavorable Solar linear-anisotropy gate.
This note checks an independent isolated compact-source consequence.

## Branch conditions and a continuum-safe comparison

Use positive normalized spectral measure dnu, isolated regular radial
outward force g>=0 tending to zero, positive modal quartic a_delta, and
bounded modal variables z_delta>=0 with Z=integral z_delta dnu. Require
0<=h'(g)<=1 and h(g)<=g, true for the stated bounded h. The equations are

    -ell^2 L1 z_delta+z_delta+a_delta z_delta^3=h(g),
    L1=d_R^2+2/R d_R-2/R^2,
    g=gN+h'(g)Z, 0<=gN<=GM_total/R^2.

Put C=GM_total/(2ell^2). Since 2ell^2 C/R^2>=gN,

    -ell^2 L1(z_delta-C)+(z_delta-Z)+a_delta z_delta^3<=0.

Do not assume an attained maximum over a soft continuum. Instead multiply
by w_delta=(z_delta-C)_+, integrate radial R^2dR and normalized spectral
measure, and take the declared regular/isolated boundary limits. Gradient
and radial-vector angular terms are nonnegative. With W=integral w dnu,
Z-C<=W and

    integral w_delta(z_delta-Z)dnu
       >=integral w_delta^2 dnu-W^2>=0.

The quartic term is nonnegative on w>0. Thus w=0, z_delta,Z<=C and

    0<=g-gN<=GM_total/(2ell^2).

This requires finite positive-part Sobolev integrals/vanishing boundary work,
or a regular cutoff proof with a bounded convergent soft-limit solution.
The estimate is uniform; it does not establish solution existence, branch
selection, an arbitrary sign-changing field, external-field boundary,
nonspherical source or non-equilibrium stars. Delta=0 is not evaluated as
a finite mode. Independent analytical review checked this stronger
positive-part proof, including its continuum and sign qualifications.

## Same exposed stellar benchmark, declared arithmetic

Use the existing ordinary Plummer source and tracer a=28pc, nominal masses
340/1020/3400 solar masses, ell=100pc and aperture67pc. GM_nominal_sun=
1.3271244e20m^3/s^2, pc=648000*149597870700/pi metres. These are exposed
stellar population choices, not a current measured mass posterior. No
additional dark, central, gas or external mass is inserted. The historical
3.7km/s reference is an exposed comparison, not an updated confidence test.

Stationary integrated stress with vanishing surface flux gives
<v^2>=<Rg>. Existing authenticated Plummer identities <R>=2a and
<R gN>=3piGM/(32a) therefore give, with arbitrary anisotropy,

    <v^2><=GM[3pi/(32a)+a/ell^2],
    sigma_LOS,ap^2<=<v^2>/Fap,
    Fap=Rap^2/(Rap^2+a^2).

No favorable isotropic factor1/3 is used. Positive kinetic moments imply
the aperture bound; actual tracer/source geometry, stationarity, binaries,
selection, aperture population and boundary stresses remain qualifications.

If D=Fap sigma_star^2-3piGM/(32a)>0, a necessary upper length ceiling is
ell<=sqrt(GM a/D). If D<=0, this bound gives no finite ceiling. It is not
a sufficient fit or length adoption. This differs by sqrt2 from the old
filtered-INPUT ceiling at identical inputs because the force bound is twice
as large. That exact comparison is a control, not a replay of old science.

Freeze before arithmetic: authenticate the old FAILED V001 raw result
6fe41c1fdb3f971a449ad34ec58adcd9c4fdb062659e174d306f9e55e4e26bd9 and
read its saved rows; retain the Decimal80 V002 repair as qualified reference,
never execute old code or repeat kernel/Plummer quadratures. Controls at
2e-12: dimensionless/dimensional velocity, anomalous term2aC, aperture
identity, exact mass/speed scaling, inversion in the original inequality,
and sqrt2 comparison. Preserve all checks and failed attempts in exclusive
new outputs with source/protocol/input hashes and canonical seal. No
Solar-length scan, dispersion fit or model selection follows this arithmetic.
