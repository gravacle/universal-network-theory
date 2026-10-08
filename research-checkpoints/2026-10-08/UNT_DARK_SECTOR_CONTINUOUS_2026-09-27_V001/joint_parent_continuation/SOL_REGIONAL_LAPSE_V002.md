# The regional clock rate is fixed by constraint preservation

2026-10-05 UTC. Same action and Sol seed as SOL_REGIONAL_STATE_V001.
Two independent internal derivations now close the previously omitted
instantaneous lapse-rate contribution. No new response function or fitted
clock history is introduced. No full time evolution is claimed.

V001's sentence calling a positive kinematic budget necessary for dust
acceleration was too broad. It is necessary only for acceleration attributed
to that displayed contribution alone. With an unspecified lapse-rate term
it is neither necessary nor sufficient for total domain acceleration. The
V001 receipt and prospective text remain preserved; this note supersedes
that wording, without changing its numerical criteria or results.

## Exact instantaneous lapse equation

At N=1, A=B=lambda=0, the action's lapse energy derivative is

    rho_A_dot=2M^2 div L_1^-2 grad Ndot.

Metric/time derivatives of the filter multiply vanishing background
auxiliaries here. Let X=Kij Kij-(1+beta)K^2. Spatial evolution, the momentum
constraint and ordinary matter conservation give

    Rdot=-2 Rij Kij+2beta Delta K,
    Xdot=-2 Rij Kij-K X+K R+2Kij Sij/M^2,
    rho_dot+K rho+Kij Sij=0.

Preservation of R-X-2(rho+rho_A)/M^2=0 therefore requires

    2 div L_1^-2 grad Ndot=beta Delta K.

An independent canonical derivation agrees: pi=-M^2 F sqrt(gamma) K and
H_lambda-H_GR=beta pi^2/[2F M^2 sqrt(gamma)]. The anomalous curvature
bracket is -beta M^2 Delta K, canceled by rho_A_dot. All statements concern
the instantaneous constraint surface and include ordinary conservation.

On a connected closed slice this fixes Ndot up to a spatial constant. Choose
the mean proper-lapse time, <N>=1, so <Ndot>=0 at this uniform-lapse instant.
This specifies the domain clock convention; it is not an observer distance
or redshift prescription.

For the Sol z-mode, the rough one-form Laplacian gives
D^2 grad cos(kz)=-(k^2+2a^2)grad cos(kz), and hence

    f=[1+ell^2(k^2+2a^2)]^-1,
    Ndot=beta (K-K0)/(2f^2),
    <K Ndot>/H^2=beta t^2/(4f^2),
    3 addot_D/(a_D H^2)=[q+beta/(4f^2)]t^2-r/(2F).

The final line now includes the full instantaneous dust-domain equation
for this seed and mean-lapse clock. It is not a sustained accelerating
solution. On general curved slices the two scalar operators need not
commute; do not assume a universally positive quadratic form from this
single eigenmode.

## Saved state extension and fixed checks

Reuse the V001 density endpoints and all frozen state choices. Set the
DEVELOPMENT scale H=100 km/s/Mpc and retain ell=100 pc. Thus ell H/c is
3.33564095198e-8; this scale setting is not a fitted Hubble measurement.
The source acceleration normalization has no role on this initial B=0 slice.

Evaluate the exact lapse term and a rigorous all-amplitude upper bound.
For any integer trace T>=3 and any admissible 0<=t<3, r>=0,

    a^2/H^2 <= 4.5F,
    (k^2+2a^2)/H^2 <=4.5F[2+(2pi/acosh(3/2))^2],
    f^-2 <= [1+(ell H/c)^2 * preceding bound]^2.

Together with the V001 all-trace density bound, this bounds the COMPLETE
instantaneous acceleration, including clock rate, for the same minimum-
shear, sinusoidal, initially uniform-lapse Sol family. Extra shear,
different profiles/geometries and different initial lapse are not excluded.

No previous trajectory or density search is rerun. New arithmetic controls
are source-receipt SHA verification, exact lapse equation residual and
phase-averaged clock term against the analytic expression at <=1e-11,
and positivity/upper-bound checks with <=1e-11 arithmetic allowance. Keep
the physical acceleration sign and margin distinct from these error gates.
