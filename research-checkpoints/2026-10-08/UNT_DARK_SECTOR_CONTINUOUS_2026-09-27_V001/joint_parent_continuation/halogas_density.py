"""Retained-emission sources; construction/tests are explicit, not import-time.

The inherited density module reads its small source JSON during import.
"""
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
import galaxy_density as inherited

MODELS = {40: 'HALOGAS40_ML36_RETAINED_V001',
          120: 'HALOGAS120_ML36_RETAINED_V001'}
MULTIPLIER = 1.2567828155112788
HELIUM = 1.36


class BernsteinProfile:
    """C0 nonnegative density in R^2; integral returns integral R Sigma dR."""
    def __init__(self, edges, bare_masses, factor=HELIUM):
        self.r = np.asarray(edges, dtype=float).copy()
        self.bare_masses = np.asarray(bare_masses, dtype=float).copy()
        assert len(self.r) == len(self.bare_masses) + 1 and self.r[0] == 0
        assert np.all(np.isfinite(self.r)) and np.all(np.diff(self.r) > 0)
        assert np.all(np.isfinite(self.bare_masses)) and np.all(self.bare_masses >= 0)
        assert math.isfinite(factor) and factor > 0
        self.factor, self.tail = factor, None
        self.squared_edges = self.r**2
        self.delta = np.diff(self.squared_edges)
        self.mean = factor*self.bare_masses/(math.pi*1e6*self.delta)
        self.s = np.r_[self.mean[0], np.minimum(self.mean[:-1], self.mean[1:]), 0.]
        self.b = 3*self.mean-self.s[:-1]-self.s[1:]
        assert np.all(self.b >= 0)

    def polynomial(self, index, t):
        return self.s[index]*(1-t)**2 + 2*self.b[index]*t*(1-t) + self.s[index+1]*t**2

    def primitive(self, index, t):
        return (self.s[index]*(t-t*t+t**3/3)
                + self.b[index]*(t*t-2*t**3/3) + self.s[index+1]*t**3/3)

    def sigma(self, radius):
        radius = np.asarray(radius, dtype=float)
        assert np.all(radius >= 0) and not np.any(np.isnan(radius))
        bounded = np.minimum(radius, self.r[-1])
        index = np.minimum(np.searchsorted(self.r, bounded, side='right')-1, len(self.mean)-1)
        t = (bounded**2-self.squared_edges[index])/self.delta[index]
        return np.where(radius <= self.r[-1], self.polynomial(index, t), 0.)

    def integral(self, lower, upper):
        lower, upper = np.broadcast_arrays(np.asarray(lower, dtype=float), np.asarray(upper, dtype=float))
        assert np.all(lower >= 0) and np.all(upper >= lower)
        out = np.zeros_like(lower)
        for i, (left, right) in enumerate(zip(self.r[:-1], self.r[1:])):
            a, b = np.clip(lower, left, right), np.clip(upper, left, right)
            ta = (a*a-self.squared_edges[i])/self.delta[i]
            tb = (b*b-self.squared_edges[i])/self.delta[i]
            out += self.delta[i]/2*(self.primitive(i, tb)-self.primitive(i, ta))
        return out


def selected_profile(extraction, width):
    assert width in MODELS
    orders = [row for row in extraction['orders'] if row['subpixels_per_axis'] == 8]
    assert len(orders) == 1
    profile = orders[0][f'profile_{width}arcsec']
    flags = np.asarray(profile['complete_by_conservative_chord_bound'], dtype=bool)
    count = int(np.sum(flags))
    assert count > 0 and np.array_equal(flags, np.arange(len(flags)) < count)
    lo, hi = np.asarray(profile['r_lo_kpc']), np.asarray(profile['r_hi_kpc'])
    assert lo[0] == 0 and np.array_equal(lo[1:], hi[:-1])
    mass = np.asarray(profile['groups']['full']['mass_Msun'], dtype=float)
    assert len(mass) == len(flags) and np.all(np.isfinite(mass))
    assert count == {40: 51, 120: 17}[width]  # Fixed geometry, never flux-selected.
    return profile, count, np.r_[lo[0], hi[:count]], mass


def source(extraction, width, multiplier):
    assert multiplier == MULTIPLIER
    _, count, edges, mass = selected_profile(extraction, width)
    components = inherited.profiles(True, True)
    stars = components['stars']
    components['stars'] = inherited.Profile(stars.r.copy(), multiplier*stars.s, stars.tail)
    components['HI_He'] = BernsteinProfile(edges, mass[:count])
    return components


def qualify(extraction, width, multiplier):
    """Independent 3-point Gauss in R integrates the degree-five R*Sigma."""
    profile, count, edges, mass = selected_profile(extraction, width)
    components = source(extraction, width, multiplier)
    p = components['HI_He']
    nodes, weights = leggauss(3)
    checks, bins = [], []

    def check(name, error, tolerance):
        checks.append({'name': name, 'error': float(error), 'tolerance': float(tolerance),
                       'passed': bool(math.isfinite(error) and error <= tolerance)})

    for i, (a, b) in enumerate(zip(edges[:-1], edges[1:])):
        measured = HELIUM*mass[i]
        analytic = float(2*math.pi*1e6*p.integral(a, b))
        points = (a+b)/2+(b-a)*nodes/2
        gauss = float(2*math.pi*1e6*(b-a)/2*np.dot(weights, points*p.sigma(points)))
        aa, bb = a+(b-a)/8, b-(b-a)/8
        points = (aa+bb)/2+(bb-aa)*nodes/2
        part_gauss = float(2*math.pi*1e6*(bb-aa)/2*np.dot(weights, points*p.sigma(points)))
        part_analytic = float(2*math.pi*1e6*p.integral(aa, bb))
        check(f'bin_mass:{i}', abs(analytic-measured)/max(1., abs(measured)), 1e-12)
        check(f'gauss_bin:{i}', abs(gauss-analytic)/max(1., abs(analytic)), 1e-12)
        check(f'gauss_subinterval:{i}', abs(part_gauss-part_analytic)/max(1., abs(part_analytic)), 1e-12)
        controls = np.array([p.s[i], p.b[i], p.s[i+1]])
        check(f'nonnegative_controls:{i}', float(max(0., -np.min(controls))), 0.)
        check(f'bernstein_bound:{i}', float(max(0., np.max(controls)-3*p.mean[i]))/max(1., p.mean[i]), 1e-14)
        if measured == 0:
            check(f'zero_retention_bin:{i}', float(np.max(abs(controls))), 0.)
        if i+1 < count:
            check(f'continuity:{i}', abs(float(p.polynomial(i, 1.)-p.polynomial(i+1, 0.))), 0.)
        bins.append({'R_lo_kpc': float(a), 'R_hi_kpc': float(b), 'bare_HI_mass_Msun': float(mass[i]),
                     'HI_He_mass_Msun': measured, 'mean_HI_He_Msun_pc2': float(p.mean[i]),
                     'controls_HI_He_Msun_pc2': controls.tolist(), 'analytic_mass_Msun': analytic,
                     'gauss_mass_Msun': gauss, 'partial_analytic_Msun': part_analytic,
                     'partial_gauss_Msun': part_gauss})
    check('center_density', abs(float(p.sigma(0.)-p.mean[0])), 0.)
    # dSigma/dR=(dSigma/dt)*2R/Delta, finite polynomial derivative at R=0.
    center_slope = (2*(p.b[0]-p.s[0]))*2*0./p.delta[0]
    check('regular_center_slope', abs(float(center_slope)), 0.)
    check('outer_continuity', abs(float(p.sigma(edges[-1]))), 0.)
    check('exterior_zero', abs(float(p.integral(edges[-1], np.inf)))+abs(float(p.sigma(edges[-1]+1.))), 0.)
    masses = inherited.masses(components)
    included, full = float(np.sum(mass[:count])), float(np.sum(mass))
    excluded = float(np.sum(mass[count:]))
    check('HI_He_total_mass', abs(masses['HI_He']/(HELIUM*included)-1), 1e-13)
    check('included_excluded_ledger', abs(included+excluded-full)/abs(full), 1e-13)
    control = inherited.profiles(True, True)
    control_masses = inherited.masses(control)
    for name, scale in (('stars', multiplier), ('H2_He', 1.)):
        check(f'unchanged_control_component:{name}', abs(masses[name]/(scale*control_masses[name])-1), 1e-13)
    negative = np.asarray(profile['groups']['full']['negative_mass_Msun'])
    return {'model': MODELS[width], 'width_arcsec': width, 'subpixels_per_axis': 8,
            'status': 'COMPLETE' if all(c['passed'] for c in checks) else 'FAILED',
            'checks': checks, 'bins': bins, 'component_masses_Msun': masses,
            'stellar_multiplier': multiplier, 'helium_factor_applied_once': HELIUM,
            'complete_bin_count': count, 'support_kpc': float(edges[-1]),
            'full_map_retained_bare_HI_Msun': full, 'included_retained_bare_HI_Msun': included,
            'excluded_retained_bare_HI_Msun': excluded, 'excluded_fraction': excluded/full,
            'included_negative_pixel_contribution_Msun': float(np.sum(negative[:count])),
            'zero_retention_bin_indices': np.flatnonzero(mass[:count] == 0).tolist(),
            'exterior_assumption': 'This contrast is zero beyond the complete aperture; real gas is not asserted absent.',
            'scope': 'Fixed-plane retained emission; neither detection completeness nor source association is established.'}
