"""Read-only independent saved arithmetic; no roots, fits or propagation."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    result = HERE/'ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json'
    freeze = HERE/'ORIGINAL_SPECTRUM_CALIBRATION_V001_FROZEN.json'
    wrapper = json.loads(result.read_text())
    frozen = json.loads(freeze.read_text())
    p = wrapper['payload']
    assert wrapper['freeze_sha256'] == sha(freeze)
    assert wrapper['payload_sha256'] == hashlib.sha256(encode(p)).hexdigest()
    for name, expected in frozen['files'].items():
        path = Path(name) if Path(name).is_absolute() else ROOT/name
        path.resolve().relative_to(ROOT.resolve())
        assert sha(path) == expected, name
    assert p['status'] == 'COMPLETE' and p['checks']['failed'] == 0
    assert not p['checks']['failure_names']
    assert p['checks']['count'] == 36*5+18+648*11+1
    returned = json.loads((HERE/'PREPARED_ACTION_RETURN_V001_RESULTS.json').read_text())['payload']
    history = json.loads((HERE/'COMMON_HISTORY_MECHANISM_V001_RESULTS.json').read_text())['payload']
    old_refs = json.loads((HERE/'COSMOLOGY_CLOSURE_ARITHMETIC.json').read_text())
    cases = {(c['gap'],c['order'],c['dt'],c['duration']):c for c in history['cases']}
    maxima, count = {}, 0

    def check(name, actual, expected, scale=None):
        nonlocal count
        error = abs(actual-expected)/(max(abs(expected),1e-300) if scale is None else scale)
        assert math.isfinite(error) and error <= 2e-12, (name, error)
        maxima[name] = max(maxima.get(name,0.), error)
        count += 1

    assert len(p['templates']) == 36 and len(p['references']) == 18
    for ti, t in enumerate(p['templates']):
        r = returned['rows'][ti]
        case = cases[(r['gap'],r['mode_order'],r['dt'],r['duration'])]
        w = case['weights']; md = r['mode_data']
        assert t['template'] == ti
        for key, field in (('gap','gap'),('mode_order','mode_order'),('dt','dt'),
                           ('duration','duration'),('prepared_source','g')):
            assert t[key] == r[field]
        assert t['actions_sha256'] == hashlib.sha256(encode(md['action'])).hexdigest()
        assert t['spectrum_sha256'] == hashlib.sha256(encode(dict(delta=case['delta'],weights=w))).hexdigest()
        check('I0',t['I0'],math.fsum(w))
        check('E',t['energy'],math.fsum(a*b for a,b in zip(w,md['zero_source_energy'])))
        check('P',t['pressure'],math.fsum(a*b for a,b in zip(w,md['zero_source_pressure'])))
        check('P_over_E',t['pressure_over_energy'],t['pressure']/t['energy'])
        check('cycle_energy',t['complete_cycle_work'],t['energy'])
    for ri, ref in enumerate(p['references']):
        old = old_refs['rows'][ri]
        assert ref['reference'] == ri
        assert ref['inherited_reference_input'] == old['reference_input']
        assert ref['bbn'] == old['bbn']
        h0 = old['reference_input']['H0_km_s_Mpc']
        ob = old['bbn']['omega_b']/(h0/100)**2
        check('H0_SI',ref['H0_s_inverse'],h0/3.085677581491367e19)
        check('Omega_b',ref['Omega_b'],ob)
        check('Omega_exc',ref['Omega_exc'],1-old['reference_input']['Omega_Lambda_ref']-ob)
    assert len(p['rows']) == 648
    assert {(r['template'],r['reference']) for r in p['rows']} == {(i,j) for i in range(36) for j in range(18)}
    ranges = {}
    fields = ('gstar_m_s2','S','gs_m_s2','d','pressure_over_energy','delta_q0',
              'relaxed_reference_a0_m_s2','relaxed_window_upper_over_cutoff_squared',
              'root_relative_condition')
    duplicate_groups = {}
    for r in p['rows']:
        assert r['status'] == 'POSITIVE_CALIBRATION'
        t = p['templates'][r['template']]; ref = p['references'][r['reference']]
        e,i0,S = t['energy'],t['I0'],r['S']
        oe,ol = ref['Omega_exc'],ref['Omega_Lambda']
        ch = 299792458*ref['H0_s_inverse']
        gstar = ch*math.sqrt(3*i0*oe/(2*e)); a0 = 16*i0/(3*math.pi)
        check('gstar_SI',r['gstar_m_s2'],gstar)
        check('endpoint_target',r['Q_target'],e*ol/oe)
        check('Q_target',r['Q'],r['Q_target'])
        check('Q_contact',r['Q'],i0*S*S*(1-r['d'])/2)
        check('gs_SI',r['gs_m_s2'],gstar*S)
        check('gs_baseline_bound',r['gs_lower_m_s2'],ch*math.sqrt(3*ol))
        check('gs_contact_identity',r['gs_m_s2'],ch*math.sqrt(3*ol/(1-r['d'])))
        check('Omega_exc_reconstruction',r['Omega_exc_reconstructed'],2*gstar*gstar*e/(3*i0*ch*ch))
        check('Omega_vac_reconstruction',r['Omega_vac_reconstructed'],2*gstar*gstar*r['Q']/(3*i0*ch*ch))
        check('retained_w',r['pressure_over_energy'],t['pressure']/e)
        check('delta_q0',r['delta_q0'],1.5*oe*t['pressure']/e)
        check('relaxed_a0_reference',r['relaxed_reference_a0_m_s2'],gstar*a0)
        check('window',r['relaxed_quadratic_window_upper_G'],S*S/(2*a0))
        check('window_vs_cutoff',r['relaxed_window_upper_over_cutoff_squared'],S*S/(2*a0*t['gap']**2))
        check('S_vs_cutoff',r['S_over_cutoff_squared'],S/t['gap']**2)
        check('root_condition',r['root_relative_condition'],r['Q_target']*r['dS_dQ']/S)
        check('continuum_d_bound',r['continuum_only_d_upper'],math.pi*S/(4*(1-t['gap']**2)))
        assert 0 <= r['d'] < 1 and r['d'] <= r['discrete_d_upper']+2e-12
        assert r['dS_dQ'] > 0 and r['gs_m_s2'] >= r['gs_lower_m_s2']
        if r['gs_discrete_upper_m_s2'] is not None:
            check('discrete_gs_bound',r['gs_discrete_upper_m_s2'],r['gs_lower_m_s2']/math.sqrt(1-r['discrete_d_upper']))
            assert r['gs_m_s2'] <= r['gs_discrete_upper_m_s2']+1e-22
        for key in fields:
            ranges.setdefault(key,[]).append(r[key])
        ranges.setdefault('quadratic_window_upper_physical_m_s2',[]).append(gstar*S*S/(2*a0))
        ranges.setdefault('cutoff_squared_physical_m_s2',[]).append(gstar*t['gap']**2)
        group=(r['template'],ref['H0_s_inverse'],oe,ol)
        if group in duplicate_groups:
            other=duplicate_groups[group]
            for field in ('gstar_m_s2','S','gs_m_s2','Q','delta_q0'):
                check('historical_a0_not_target',r[field],other[field])
        else:
            duplicate_groups[group]=r
    return dict(status='ACCEPTED_SAVED_ARITHMETIC',script_sha256=sha(Path(__file__)),
        result_sha256=sha(result),freeze_sha256=sha(freeze),payload_sha256=wrapper['payload_sha256'],
        frozen_members=len(frozen['files']),producer_checks=p['checks']['count'],
        independent_arithmetic_checks=count,maximum_relative_errors=maxima,
        ranges={k:dict(minimum=min(v),maximum=max(v)) for k,v in ranges.items()},
        distinct_template_reference_calibrations=len(duplicate_groups),
        representative=next(r for r in p['rows'] if r['template']==6 and r['reference']==0),
        producer_seconds=p['seconds'],producer_self_RSS_bytes_on_Darwin=p['max_rss_platform_units'],
        limitations=['No roots, quadrature, propagation or fitting repeated.',
                     'New modal roots are not saved: their independent numerical check is producer evidence, not reconstructed here.',
                     'Reference density matching does not independently validate cosmology or recalibrate existing galaxy fields.'])


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2,allow_nan=False))
