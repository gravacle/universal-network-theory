"""Read-only saved-output audit. No producer, quadrature, roots or evolution."""
import base64
import hashlib
import json
import math
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def enc(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    transport_path = HERE/'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json'
    freeze_path = HERE/'FINITE_GAP_SHARED_SCREEN_V002_FROZEN.json'
    transport_bytes = transport_path.read_bytes()
    t = json.loads(transport_bytes)
    compressed = base64.b64decode(t['data'], validate=True)
    decoder = zlib.decompressobj()
    raw = decoder.decompress(compressed)+decoder.flush()
    assert decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail
    assert len(raw) == t['raw_bytes'] and sha(raw) == t['raw_sha256']
    assert sha(raw) == '822dd216b33ff4ce08cdcd8b5f1ad5e3e27c583b7833107cef58b158cb3f9cc0'
    v = json.loads(raw)
    p = v['payload']
    assert raw == enc(v) and sha(enc(p)) == v['payload_sha256']
    frozen_bytes = freeze_path.read_bytes()
    f = json.loads(frozen_bytes)
    assert sha(frozen_bytes) == v['freeze_sha256'] == 'e2d80308d159f7d7b0ec4217e6082c1157eda6cc81000ac4d83c4b6255b989cb'
    assert f['configuration'] == p['configuration']
    assert p['status'] == 'COMPLETE' and p['failures'] == []
    assert t['summary'] == {k:p[k] for k in t['summary']}
    actual_files = {}
    for name, expected in f['files'].items():
        path = (ROOT/name).resolve(strict=True)
        path.relative_to(ROOT)
        assert sha(path.read_bytes()) == expected
        actual_files[path] = expected
    assert len(actual_files) == 52
    ancestry_occurrences = 0
    for path in actual_files:
        if not path.name.endswith('_FROZEN.json'):
            continue
        ancestor = json.loads(path.read_bytes())
        for name, expected in ancestor['files'].items():
            q = Path(name)
            candidates = [q] if q.is_absolute() else [ROOT/q, path.parent/q]
            found = set()
            for candidate in candidates:
                candidate = candidate.resolve()
                if candidate.is_relative_to(ROOT) and candidate.is_file():
                    found.add(candidate)
            assert len(found) == 1
            member = found.pop()
            assert actual_files[member] == expected
            ancestry_occurrences += 1
    old_path = HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json'
    old_raw = old_path.read_bytes()
    old_wrapper = json.loads(old_raw)
    old = old_wrapper['payload']
    assert sha(old_raw) == '11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628'
    assert sha(enc(old)) == old_wrapper['payload_sha256']
    assert sha((HERE/'GLOBAL_GAP_LIMIT_CALIBRATION_V001_FROZEN.json').read_bytes()) == old_wrapper['freeze_sha256']
    assert old['status'] == 'COMPLETE' and not old['failures']
    keys = [(r['spectrum_index'], r['reference']) for r in old['rows']]
    assert len(keys) == 72 and set(keys) == {(s,r) for s in range(4) for r in range(18)}
    lookup = dict(zip(keys, old['rows']))
    cfg = p['configuration']
    expected = [(s,r,R) for s,r in keys for R in cfg['R']]
    assert [(r['spectrum_index'],r['reference'],r['R']) for r in p['rows']] == expected
    assert len(p['rows']) == 360
    counts, maxima = {}, {}

    def check(name, got, want, scale=None):
        scale = max(abs(got), abs(want), 1e-300) if scale is None else scale
        err = abs(got-want)/scale
        assert math.isfinite(err) and err <= 2e-11, (name,got,want,err)
        counts[name] = counts.get(name,0)+1
        maxima[name] = max(maxima.get(name,0.),err)

    beta,c,A = cfg['beta'],cfg['c'],cfg['inverse_scale_factor']
    cancellation = []
    for r in p['rows']:
        s,j,R = r['spectrum_index'],r['reference'],r['R']
        ref = old['references'][j]
        prior = lookup[s,j]
        kb = math.fsum(old['spectra'][s]['spectrum']['weights'])+beta
        gs = cfg['exposed_a0_m_s2']*3*math.pi/(16*kb)
        H,oe,ol = ref['H0_s_inverse'],ref['Omega_exc'],ref['Omega_Lambda']
        E = 3*kb*oe*(c*H)**2/(2*gs**2)
        e,pr = r['E']/beta,r['pressure']/beta
        I,om,cur = r['I'],r['omega'],r['eII']
        ci = I*cur/om
        q = 3*(e+pr)/(R**4+4*e)
        K = beta*q
        J = beta*(om**2/cur+3*I*om)
        ratio = 3*ci/((R**4+4*e)*(1+3*ci))
        length = c*c/gs*math.sqrt(ratio)
        for name,got,want in (
            ('gstar',r['gstar'],gs),('energy',r['E'],E),
            ('inherited_energy',r['E'],prior['E_required']),
            ('vacuum_mapping',r['DeltaU'],E*ol/oe),
            ('excitation_density',2*gs**2*r['E']/(3*kb*(c*H)**2),oe),
            ('vacuum_density',2*gs**2*r['DeltaU']/(3*kb*(c*H)**2),ol),
            ('action_enthalpy',I*om,e+pr),('w',r['w'],pr/e),
            ('cI2',r['cI2'],ci),('linear_domain',r['phase_linear_potential_scale'],ci),
            ('q',r['q_hard'],q),('K0',r['K0'],K),('mu0',r['mu0'],K/kb),
            ('J',r['J_static'],J),('J_enthalpy',J,beta*(e+pr)*(1/ci+3)),
            ('static_ratio',K/J,ratio),('length_pc',r['static_length_pc'],length/cfg['parsec_m']),
            ('cosmic_units',(H*length/c)**2,2*(beta/kb)*(e/R**4)*ci/(oe*(1+4*e/R**4)*(1+3*ci))),
            ('cold_length',r['cold_length_pc'],1.5*c*c/gs*math.sqrt(e)/R**4/cfg['parsec_m']),
            ('deceleration',r['delta_deceleration'],1.5*oe*pr/e),
            ('infinite_S',r['S_infinity'],prior['S']),
            ('S_difference',r['S_minus_limit'],r['S']-prior['S']),
            ('early_action_target',r['early_action_target'],I*A**3),
            ('early_action',r['early_I'],I*A**3),
            ('early_enthalpy',r['early_I']*r['early_omega'],r['early_E']/beta+r['early_p']),
            ('early_pressure_ratio',r['early_w'],r['early_p']/(r['early_E']/beta)),
            ('early_cI2',r['early_cI2'],r['early_I']*r['early_eII']/r['early_omega']),
            ('early_dust_ratio',r['early_dust_ratio'],r['early_E']/(r['E']*A**3))):
            check(name,got,want)
        assert 0 < ci < 1/3 and 0 < r['early_cI2'] < 1/3
        assert 0 < r['w'] <= r['early_w'] < 1/3
        assert r['early_dust_ratio'] >= 1 and K > 0 and J > 0
        assert r['S'] >= prior['S'] and r['S_minus_limit'] > 0
        cancellation.append(dict(R=R,shift=r['S_minus_limit'],
                                 shift_in_ulps=r['S_minus_limit']/math.ulp(r['S'])))
    for group in p['ranges']:
        selected = [r for r in p['rows'] if r['R'] == group['R']]
        assert len(selected) == group['rows'] == 72
        for name, extrema in group['ranges'].items():
            assert extrema == [min(r[name] for r in selected),max(r[name] for r in selected)]
    for name,error in p['maxima'].items():
        quadrature = any(name.startswith(prefix) for prefix in ('GL64_','Simpson1024_','early_GL64_','early_Simpson1024_'))
        assert error <= cfg['quadrature_tolerance' if quadrature else 'arithmetic_tolerance']
    out = dict(status='PASS_SAVED_ARITHMETIC',scope='No orbit quadrature, roots, dynamics or producer import',
        source_sha256=sha(Path(__file__).read_bytes()),transport_sha256=sha(transport_bytes),
        raw_result_sha256=sha(raw),payload_sha256=v['payload_sha256'],freeze_sha256=sha(frozen_bytes),
        frozen_members=52,nested_manifest_member_occurrences=ancestry_occurrences,
        rows=360,independent_arithmetic_checks=sum(counts.values()),counts=counts,maxima=maxima,
        producer_check_count=sum(p['counts'].values()),producer_maximum_normalized_error=max(p['maxima'].values()),
        producer_seconds=p['seconds'],producer_peak_self_rss_bytes=p['peak_self_rss_bytes'],ranges=p['ranges'],
        S_shift_precision=[dict(R=R,min_ulps=min(x['shift_in_ulps'] for x in cancellation if x['R']==R),
            max_ulps=max(x['shift_in_ulps'] for x in cancellation if x['R']==R)) for R in cfg['R']],
        limitations=['Saved mean-square and endpoint roots are absent: virial, contact and vacuum-integral controls remain source-reviewed producer evidence, not independently repeated numerical integrals.',
                     'Small S minus S_infinity is a difference of two rounded roots; no relative-precision certificate for this difference is inferred.',
                     'Static length is not a halo radius or a dynamical instability rate; no observational criterion applied.'])
    print(json.dumps(out,sort_keys=True,indent=2,allow_nan=False))


if __name__ == '__main__':
    main()
