# One-slice dust-observer redshift and distance test

2026-10-05 UTC. New test of the saved zero-endpoint Sol constraint states,
not an extension of their earlier domain trajectory. No state formation,
finite-redshift history, supernova likelihood or native adoption is supplied.
All old failures and receipts remain. Root is the sole small numerical worker.

The action, geometry, ordinary density and momentum are those in
SOL_REGIONAL_STATE_V001 and REGIONAL_CLOCK_BUDGET_IDENTITIES_V001. Take
beta=.5, F=1+3beta/2=1.75, N=1 and acceleration auxiliaries zero on this
slice. The observer/emitter congruence is conserved geodesic ordinary dust,
initially normal throughout the slice. The preferred normal can accelerate
later; it must not be substituted for that dust. Proper-time optical
derivatives at this order do not acquire the preferred-coordinate Ndot.

## Action and observable identities

With expanding-positive K and mixed spatial components, direct variation
gives

    Kdot^i_j=-Ric^i_j-K K^i_j+Ciso delta^i_j,
    Ciso=(beta R3+rho/M^2)/(2F).

Its trace agrees with the Hamiltonian and saved trace evolution. For the
past affine ray l=-u+n at the observer, E_o=u.l=1 and |n|=1,

    Hn=Kij ni nj,
    Epp=-Kdot_nn+(Dk Kij) nk ni nj+2(K^2)nn,
    qn=Epp/Hn^2-3,
    DA(z,n)=z/Hn*[1-(3+qn)z/2+O(z^2)],
    DL(z,n)=z/Hn*[1+(1-qn)z/2+O(z^2)].

DA uses its affine linear term, and DL assumes metric null propagation,
transparent photon transport and distance reciprocity. These are explicit
observer premises of the conditional parent, not derived network photons.
The general direction-dependent distance expansion is independently
described by [Heinesen, JCAP 05 (2021) 008](https://arxiv.org/abs/2010.06534).
The Sol specialization here is derived from the resident action.

In the orthonormal frame e1=exp(-az)dx, e2=exp(az)dy, e3=dz, let the
diagonal K eigenvalues be ki. The connection terms are essential:

    G(n)=n3*[sum_i ki' ni^2
             +2a*((k3-k1)n1^2+(k2-k3)n2^2)],
    Epp=-2a^2 n3^2+K Hn-Ciso+G(n)+2 sum_i ki^2 ni^2.

All quantities are normalized by H, setting H=1 for arithmetic. The
physical H=100 km/s/Mpc of V002 remains a development scale, not a measured
Hubble fit. For the exact isotropic-expansion Sol member t=0,

    qn=r/(6F)+(2a^2/3)*(1-3n3^2), a^2=3F-r,
    qsky=r/(6F).

Thus a negative directional q does not imply a negative full-sky coefficient.
For the equally weighted angular mean of DL AT THE SAME REDSHIFT,

    Heff=1/<1/Hn>, qeff=<qn/Hn>/<1/Hn>.

This differs from averaging qn or the domain scale factor. Since Hn and
the other terms are even while G is odd under n -> -n, paired sky averaging
cancels G exactly in qeff. No observational sky/selection weighting is fit.

## Frozen choices before arithmetic

Authenticate the V001 state result against SHA256
a1ef4649fb2e108132bbcc18eb42da5e921918b00e9bfc5574c703294acda9f7,
and V002 lapse result against SHA256
5cd1b67d2b74da10f0e179ab5106cab242de5d0f6050d4ac452e1ebc9bace13e.
Read their JSON only; never import or execute old drivers. Reuse all30
trace/density labels and each saved endpoint tmax. Evaluate t=0, t=tmax/2
and t=tmax, recomputing the Hamiltonian-required a^2 at each amplitude.
The zero and half amplitudes are declared controls/interior states, not fits.
No extra trace, density or amplitude is chosen after seeing the result.

Use16 phases theta=2pi*j/16. If a^2<=0, report curvature-inadmissible.
If t>=3, label the old endpoint as a supremum outside the strictly expanding
trace criterion. A rounded density |rho/(M^2H^2)|<=1e-12 at a saved boundary
is zero/unresolved dust and excluded from a matter-observer result; positive
density is not created by roundoff. Negative density is reported, not clipped.

Report the exact local min/max ki and the exact all-phase directional minimum

    min[1-sqrt((t/3-Cs/2)^2+(Ds/2)^2), 1-|t/3+Cs|].

If ANY local ki<=0, the whole-sky inverse-redshift series is unavailable;
retain axis coefficients where Hn>0, but do not omit the other sky directions
and call the remainder a cosmological mean. For eligible observers use
Gauss-Legendre polar and equally spaced azimuth quadrature:64x128 and128x256,
exactly antipodally paired, with the higher grid the reported arithmetic.

Frozen qualification gates: normalized Hamiltonian/trace/momentum identities,
antipodal parity, angular moments <Hn>=K/3 and
<Epp>=R3/3+K^2/3-Ciso+2tr(K^2)/3, t=0 formula, flat dust FLRW q=.5,
and Heff between exact eigenvalue bounds, all <=1e-10. Relative/absolute
normalized two-grid changes in Heff, qeff and q RMS must be <=2e-7.
The scientific signs are saved without an error tolerance changing them.
Every failed check is retained. An unqualified row is not a successful
acceleration prediction. Save source/input/protocol hashes, canonical payload
seal, all rows, controls and elapsed time exclusively to new V001 paths.

This bounds only local second-order distance coefficients. A finite light
cone, sky selection, observer formation, early universe, perturbations and
joint observational comparisons remain open. Ndot-dependent cubic redshift
coefficients are not inferred from these two derivatives.
