# Exact dynamic instantaneous circular readout V001

This guarded arithmetic component extends the resident supplied-metric interface. It does not select or change a source, solve a physical metric, certify stability or infer a galaxy history. Root numerical release remains required.

For an axisymmetric metric in coordinates (t, meridional coordinates, phi), write a=g_tt, b=g_tphi, c=g_phiphi, D=a+2b Omega+c Omega^2, J=b+c Omega and C=a c-b^2. A timelike constant-coordinate circle requires c>0 and C<0; each root still must satisfy D<0.

Let f=d(log u^t)/dt and G=Omega_dot+Omega f. Normalization and the azimuthal geodesic give the two-by-two system:

    (a+b Omega) f+(b+c Omega) G=-(a_t+2b_t Omega+c_t Omega^2)/2
    b f+c G=-b_t-c_t Omega.

Its exact solution is quadratic in Omega:

    f=[2b b_t-c a_t+2b c_t Omega+c c_t Omega^2]/(2C)
    G=[b a_t-2a b_t-2a c_t Omega-b c_t Omega^2]/(2C).

The meridional balance is

    E_m=(g_mt)_t+Omega (g_mphi)_t+g_mt f+g_mphi G-(a_m+2b_m Omega+c_m Omega^2)/2.

Hence even the full dynamic radial equation is a quadratic. The familiar radial derivative of D alone is sufficient only when the other terms vanish. Solve all roots without observational selection, derive Omega_dot=G-Omega f, and retain the full vertical and azimuthal residuals from the existing independent dynamic_circle_residual. Exact normal-observer projection gives the local velocity. Meridional normal motion need not vanish when the coordinate circle is fixed.

Polynomial discriminant sign is evaluated exactly for serialized binary64 coefficients with standard-library fractions after reversible power-two scaling; no clipping, near-zero replacement or fitted branch is used. Missing, degenerate and nontimelike cases remain explicit. Fresh analytic controls will use time-dependent rotating coordinates, a nonzero radial-azimuthal metric term and a lapse potential with independently known physical circular frequencies. No former fixture or live producer is rerun.

A local instantaneous43 comparison requires the actual solved metric and its complete first jets at all declared radii and a fixed rotation orientation. Persistent stability, evolved tracers and fully synthetic spectral observations are separate statuses; the formatter must state which prediction is supplied.
