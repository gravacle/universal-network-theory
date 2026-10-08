"""Pre-execution consequence of EVERY frozen extended-gas benchmark.

No new fitting: Mh/Rh and both type assignments are inherited exactly.
Adopt fully ionized gas with mu_e=1.14 and proton mass1.67262192369e-27kg.
For b<Rh, Sigma=Mh acos(b/Rh)/(2pi Rh b); DM_rest=Sigma/(mu_e mp PC*1e6).
DM_obs=DM_rest/(1+z_l). Output all30 cases at their saved lensing radii and
fixed impact b={20,30,50,75,90,100,150}kpc, z_l={0,.03,.2}. NoFRBdatafit,
no reinterpretation of absent gas as a measured column. Stars/cold gas and
foreground/host/correlated LSS electron columns are not included here.
The cusp at b=0 is deliberately not evaluated. Truncation beyond100kpc is
the existing hypothetical profile, not a claim that real CGM ends there.

Before outputs, compare analytic column to independent line-of-sight
quadrature at b/Rh={.1,.2,.3,.5,.75,.9,.99} at32/64nodes,1e-10relative;
recover Mh by projected annular integration to1e-12; assert exact zero
differentialcolumn for equal-gas controls, linear mass scaling and (1+z)
redshiftscaling to1e-12. Preserve failure before results. One small worker.
This script docstring is the short frozen specification; script/input hashes
are recorded in the exclusive output, so no separate process framework.
"""
import json
import math
import pathlib
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from disk_solver import sha, save_new
from effective_esd_forward_v001 import PC, MSUN

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT/'EXTENDED_GAS_ESD_V001_RESULT.json'
MP, MU, RH = 1.67262192369e-27, 1.14, 100000*PC
UNIT_COLUMN = PC*1e6


def sigma(impact, mass):
    impact = np.asarray(impact)
    assert np.all(impact > 0)
    return mass/(2*math.pi*RH*impact)*np.arccos(np.minimum(impact/RH, 1.))


def line_column(b, mass, order):
    nodes, weights = leggauss(order)
    length = math.sqrt(RH*RH-b*b)
    los = (nodes+1)*length/2
    return mass/(4*math.pi*RH)*length*np.sum(weights/(b*b+los*los))


def main():
    start = time.perf_counter()
    assert sha(SOURCE) == '0f55e92215203985cda1345d59917319f2846e66498e3e9602069c14461f145e'
    source = json.loads(SOURCE.read_text())
    controls = {}

    def check(name, error, tolerance):
        controls[name] = {'value': float(error), 'tolerance': tolerance, 'pass': bool(error <= tolerance)}

    mass = 10**10.5*MSUN
    for b in RH*np.array([.1,.2,.3,.5,.75,.9,.99]):
        exact = float(sigma(b, mass))
        for order in (32,64):
            check(f'los_{b/RH}_{order}', abs(line_column(b,mass,order)/exact-1), 1e-10)
    nodes, weights = leggauss(64)
    theta = (nodes+1)*math.pi/4
    impact = RH*np.sin(theta)
    projected_mass = np.sum(weights*math.pi/4*2*math.pi*impact*sigma(impact,mass)*RH*np.cos(theta))
    check('projected_mass', abs(projected_mass/mass-1), 1e-12)
    check('linear_mass', abs(float(sigma(.5*RH, 3*mass)/sigma(.5*RH,mass))-3), 1e-12)
    curve = []
    fixed = np.array([20.,30.,50.,75.,90.,100.,150.])
    for case in source['cases']:
        low_mh = case['low_hot_to_stellar']*case['nominal_stellar_msun']*MSUN
        high_mh = case['high_hot_msun']*MSUN
        targets = {'fixed_impact_kpc': fixed, 'lensing_impact_kpc': np.array(case['radius_kpc'])}
        record = {'id': case['id'], 'source_high_hot_msun': high_mh/MSUN,
                  'source_low_hot_msun': low_mh/MSUN, 'profiles': {}}
        for name, b_kpc in targets.items():
            lo = sigma(b_kpc*1000*PC,low_mh)/(MU*MP*UNIT_COLUMN)
            hi = sigma(b_kpc*1000*PC,high_mh)/(MU*MP*UNIT_COLUMN)
            record['profiles'][name] = {'impact_kpc': b_kpc.tolist(), 'rest_low_DM': lo.tolist(),
                'rest_high_DM': hi.tolist(), 'rest_difference_DM': (hi-lo).tolist(),
                'observer_differences': {str(z): ((hi-lo)/(1+z)).tolist() for z in (0.,.03,.2)}}
            if 'equal_hot' in case['id']:
                check(case['id']+name+'_equal_column', np.max(abs(hi-lo))/max(1.,np.max(abs(hi))),1e-12)
            check(case['id']+name+'_redshift', np.max(abs(((hi-lo)/1.2)*1.2-(hi-lo)))/max(1.,np.max(abs(hi-lo))),1e-12)
        curve.append(record)
    if not all(c['pass'] for c in controls.values()):
        save_new(ROOT/'EXTENDED_GAS_DISPERSION_V001_FAILURE.json', {'controls':controls})
        raise RuntimeError('Column controls failed.')
    result={'script_sha256':sha(pathlib.Path(__file__)), 'source_sha256':sha(SOURCE),
            'controls':controls, 'mu_e':MU, 'proton_mass_kg':MP, 'rh_kpc':100.,
            'DM_unit':'pc cm^-3', 'cases':curve,
            'single_msun_pc2_rest_DM':MSUN/PC**2/(MU*MP*UNIT_COLUMN),
            'middle_unshifted_50kpc_rest_DM':float(sigma(50000*PC,mass)/(MU*MP*UNIT_COLUMN)),
            'seconds':time.perf_counter()-start,
            'limits':['fully ionized adopted gas', 'not observed gas or matched FRB catalogue prediction',
                      'not network excess electrons', 'no host/foreground/environment subtraction fitted']}
    save_new(ROOT/'EXTENDED_GAS_DISPERSION_V001_RESULT.json',result)
    print(json.dumps({k:result[k] for k in ('seconds','single_msun_pc2_rest_DM','middle_unshifted_50kpc_rest_DM')},indent=2))
    print('controls',len(controls),'cases',len(curve))


if __name__ == '__main__':
    main()
