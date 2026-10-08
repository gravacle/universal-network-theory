"""Conditional MOND-branch scales for the existing calibrated K(X) action.

No fitted profile, numerical evolution or new physical assumption is adopted.
Use the original Q100 eps1e-6 constants and declared kappa*L point-source
normalization. The MOND target is a comparison branch, NOT a derived formed
galaxy. Its high-acceleration normalization assumes negligible charge/stress
corrections. Actual enclosed clock energy, current and cap remain required.

J_req=m H R is ONLY the stationary-excess, homogeneous-background example.
Actual J must follow the retarded charge history. Frozen m,d and p=aM/R
are local scale diagnostics, not a radial solution. The large-R clock-mass
estimate assumes zero outer density contrast, negligible inner/gradient
terms and linearized constitutive law; it is not a predicted turnover.

Numerical controls (1e-11) check identities, the analytic annular integral
against Gauss quadrature, and the original background energy calibration.
No observational acceptance gate or post-result physical criterion.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
import invariant_clock_polar_source_v005 as inherited

BASE = Path(__file__).resolve().parent
OUT = BASE / 'INVARIANT_CLOCK_MOND_COMPATIBILITY_V001_RESULT.json'


def main():
    model = inherited.Polar(json.loads(inherited.prev.inherited.SOURCE.read_text()), 32, .012)
    a, s, X, m, K, H, hx, qr = model.bg0
    d = float(model.constitutive(s)[2])
    C, KB, lam = model.C, model.KB, model.lam
    a0 = model.bs / (1 + lam)
    mu = m / X
    L, Mb = model.L, model.kappa * model.L
    f = lam / (1 + lam)
    ratio = 2 * (1 + lam) / (C * lam)
    aM = math.sqrt(2 * Mb * a0 / (C * f))
    Rj = math.sqrt(aM / (H * X))
    Rmu = math.sqrt(2 * aM / (m * X))
    susceptibility = X * X * d
    Rcomp = (18 * Mb / (susceptibility * aM)) ** (1/3)
    depth = .5 * math.log1p(model.eps / (1 + s) / (1 + model.eps * s / (1 + s)))
    controls = []

    def check(name, error):
        controls.append(dict(name=name, error=float(error), tolerance=1e-11,
                             passed=bool(error <= 1e-11)))

    check('background_energy', abs((X*m-K)/3-(model.OA+model.p['omega_clock_excess'])))
    check('MOND_target_normalization', abs(aM*aM/(ratio*Mb*a0)-1))
    rows = []
    for radius in (5., 10., 20., 30., 100., 300., 500.):
        R = radius * L
        p = aM / R
        J = m * H * R
        divZ = 2 * p / R
        sigma = (J + mu*p) / (m + divZ/X)
        factor = (1 + H*X*R*R/aM) / (1 + m*X*R*R/(2*aM))
        check(f'current_identity_{radius}', abs(sigma*(m+divZ/X)-J-mu*p)/max(abs(J)+abs(mu*p), 1e-30))
        check(f'flow_formula_{radius}', abs(sigma/(m*R/2*factor)-1))
        rows.append(dict(radius_over_L=radius, ideal_point_target_p=p,
                         illustrative_matched_J=J, required_sigma=sigma,
                         sigma_over_HR=sigma/(H*R),
                         cosmic_current_over_mu_p=J/(mu*p),
                         denominator_correction=m*X*R*R/(2*aM)))

    # A dimensionless check of the analytic mass formula; no matching radius
    # is chosen as a physical galaxy boundary by this algebraic check.
    Rs, R, Rm = .2, .8, 1.
    density_boundary, Dstar, amp, dd = .17, 2.3, .4, .2
    def F(r):
        return r**3/3*math.log(Rm/r)+r**3/9
    exact = (density_boundary*(R**3-Rs**3)/6
             +Dstar*amp/2*(F(R)-F(Rs))
             -dd*amp**2/4*(R-Rs-(R**3-Rs**3)/(3*Rm**2)))
    xx, ww = np.polynomial.legendre.leggauss(128)
    rr = (Rs+R)/2+(R-Rs)*xx/2
    rho = density_boundary+Dstar*amp*np.log(Rm/rr)-dd*amp**2/2*(1/rr**2-1/Rm**2)
    numeric = (R-Rs)/2*float(np.dot(ww, rr**2*rho/2))
    check('annular_clock_mass_integral', abs(numeric-exact)/max(abs(exact), 1e-30))
    result = dict(protocol=__doc__, constants=dict(X=X, m=m, d=d, mu=mu, H=H,
                  KB=KB, C=C, lambda_s=lam, a0_H0c=a0, L_H0= L, kappa=model.kappa,
                  point_Mb=Mb, conditional_GN_over_Gcos=ratio, target_aM=aM,
                  target_vflat_km_s=299792.458*math.sqrt(aM),
                  clock_susceptibility=susceptibility, maximum_log_lapse_depth=depth),
                  conditional_scales=dict(current_radius_over_L=Rj/L,
                    denominator_radius_over_L=Rmu/L,
                    linearized_mass_warning_radius_over_L=Rcomp/L,
                    flat_segment_maximum_log_span_ignoring_outer_gradient=depth/aM),
                  illustrative_flow_rows=rows, controls=controls,
                  all_controls_passed=all(row['passed'] for row in controls),
                  identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                    (Path(__file__), Path(inherited.__file__), Path(inherited.prev.__file__),
                     Path(inherited.prev.inherited.__file__), inherited.prev.inherited.SOURCE)})
    with OUT.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
    print(json.dumps(result, allow_nan=False))


if __name__ == '__main__':
    main()
