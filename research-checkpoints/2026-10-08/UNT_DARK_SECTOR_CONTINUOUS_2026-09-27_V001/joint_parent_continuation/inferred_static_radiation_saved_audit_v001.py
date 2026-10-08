"""Read-only saved arithmetic audit; no scientific producer is imported."""
import base64, hashlib, json, math, zlib
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
def encode(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    files = {}; seen = set(); occurrences = 0
    def manifest(path):
        nonlocal occurrences
        path = path.resolve(); path.relative_to(ROOT)
        if path in seen: return
        seen.add(path); files[str(path.relative_to(ROOT))] = sha(path)
        for name, digest in json.loads(path.read_text())['files'].items():
            occurrences += 1; q = Path(name)
            candidates = {v.resolve() for v in ([q] if q.is_absolute() else [ROOT/q, path.parent/q])
                          if v.is_file() and v.resolve().is_relative_to(ROOT)}
            assert len(candidates) == 1, name
            p = candidates.pop(); assert sha(p) == digest, str(p)
            files[str(p.relative_to(ROOT))] = digest
            if p.name.endswith('_FROZEN.json'): manifest(p)
    def read(stem, transport=False, pinned=None):
        path = HERE/(stem+('_TRANSPORT.json' if transport else '_RESULTS.json'))
        if pinned: assert sha(path) == pinned
        obj = json.loads(path.read_text()); meta = {'file_sha256': sha(path)}
        if transport:
            raw = zlib.decompress(base64.b64decode(obj['data'], validate=True))
            assert len(raw) == obj['raw_bytes'] and hashlib.sha256(raw).hexdigest() == obj['raw_sha256']
            meta.update(raw_bytes=len(raw), raw_sha256=obj['raw_sha256']); obj = json.loads(raw)
        f = HERE/(stem+'_FROZEN.json'); manifest(f)
        assert obj['freeze_sha256'] == sha(f)
        assert obj['payload_sha256'] == hashlib.sha256(encode(obj['payload'])).hexdigest()
        meta.update(freeze_sha256=sha(f), payload_sha256=obj['payload_sha256'])
        return obj['payload'], meta
    p, meta = read('INFERRED_STATIC_RADIATION_CERTIFICATE_V001', True,
                  '3d95c9235660f0cf6cc57b333794a7e4369d5a349f148d484bc9a00ae1013eb8')
    inverse, inverse_meta = read('BBN_SHARED_INVERSE_V001', pinned=
                  'e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0')
    cal, _ = read('GLOBAL_GAP_LIMIT_CALIBRATION_V001')
    cfg = p['configuration']; beta = cfg['beta']; c = cfg['c_m_s']
    a = cfg['a_kpc']*1000*cfg['parsec_m']; small = cfg['small_square']; tol = cfg['arithmetic_tolerance']
    assert cfg == json.loads((HERE/'INFERRED_STATIC_RADIATION_CERTIFICATE_V001_FROZEN.json').read_text())['configuration']
    assert p['status'] == 'COMPLETE_CONDITIONAL_INFERRED_CERTIFICATE' and not p['failures']
    assert inverse['status'] == 'COMPLETE_CONDITIONAL_PROXY_INVERSE' and not inverse['failures']
    assert p['table_points'] == inverse['table_points'] and p['backgrounds'] == inverse['backgrounds']
    assert p['reference_mapping'] == inverse['reference_mapping']
    points = {v['point_id']:v for v in inverse['table_points']}
    backgrounds = {v['background_id']:v for v in inverse['backgrounds']}
    constants = {(v['background_id'],v['spectrum_index']):v for v in inverse['constants']}
    assert len(p['rows']) == 1340 and len(points) == 67 and len(backgrounds) == 5
    expected = {(pi, bi, si) for pi in points for bi in backgrounds for si in range(4)}
    assert {(r['point_id'],r['background_id'],r['spectrum_index']) for r in p['rows']} == expected
    C4 = ((3*math.sqrt(math.pi)/2)*math.gamma(.75)/math.gamma(.25))**(4/3)
    capmax = (1+3*small**2)*(1+3*small**2+small)/(1-small**2)
    checks = 0; maximum = 0.; failures = []
    def check(name, x, y, scale=None):
        nonlocal checks, maximum
        checks += 1
        den = max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
        error = abs(x-y)/den; maximum = max(maximum,error)
        if not math.isfinite(error) or error > tol: failures.append({'check':name,'error':error})
    check('C4',p['C4'],C4); check('uniform_cap',p['Ecap_uniform'],capmax)
    for i, r in enumerate(p['rows']):
        src = inverse['state_rows'][i]; point = points[src['point_id']]
        bg = backgrounds[src['background_id']]; co = constants[(src['background_id'],src['spectrum_index'])]
        assert r['source_state_index'] == i
        for key in ['point_id','background_id','spectrum_index','omega_b','Delta']:
            assert r[key] == src[key]
        assert r['source_state_status'] == src['status']
        assert r['roles'] == point['roles'] and r['coarse_Delta_node'] == point['coarse_node']
        assert r['local_interpolation_qualified'] == point['prediction']['local_numerical_rectangle']
        assert r['old_reference_labels'] == bg['old_labels']
        assert r['soft_spectrum_metadata'] == inverse['soft_spectra_metadata'][src['spectrum_index']]
        assert {d['L'] for d in r['domains']} == {1.,2.}
        if src['status'] == 'INFINITE_GAP_STANDARD_LIMIT':
            assert src['Delta'] == 0 and r['R'] is None and not r['input_certificate_qualified']
            assert all(d['status']=='INFINITE_GAP_LIMIT_NOT_TESTED' for d in r['domains'])
            assert all('chi_over_critical' not in d for d in r['domains'])
            continue
        assert src['status'] == 'FINITE_HARD_STATE'
        spec = cal['spectra'][src['spectrum_index']]['spectrum']
        kb = math.fsum(spec['weights'])+beta
        R = src['R']; E = src['E']; S = src['S']; chi = E/(beta*R**4); eta = S/R**2
        oe = src['Omega_exc']; og = co['Omega_gamma']; H = bg['H0_s_inverse']
        b2 = 4*chi/(1+math.sqrt(1+4*chi))
        q1 = (b2/2)/(math.sqrt(1+b2/2)+1); q2 = b2/(math.sqrt(1+b2)+1)
        flo = (q1+q2)/2-(q1-q2)**2/(2*(2+q1+q2))
        fhi = .75*b2/(math.sqrt(1+.75*b2)+1)
        ground = 3*eta**2/(math.sqrt(1+3*eta**2)+1)
        soft = math.fsum(w/(1+(S/d**2)**(2/3)) for d,w in zip(spec['delta'],spec['weights']))
        cap = (1+3*eta**2)*(1+3*eta**2+eta)/(1-eta**2)
        ilo = chi/math.sqrt(1+b2/2)
        values = dict(R=R,E=E,I=src['I'],S=S,Kb=kb,Omega_exc=oe,Omega_gamma=og,chi=chi,
                      eta_max=eta,Ecap=cap,frequency_excess_lower=flo,frequency_excess_upper=fhi,
                      ground_frequency_excess_upper=ground,radial_span_squared_upper=1.5*b2,
                      soft_B_over_S_lower=soft,Tc_over_h2_lower=soft-5*beta,
                      X=src['Q']/E,X_area_lower=C4*ilo**(4/3)/chi,
                      X_area_upper=min(1.,C4*chi**(1/3)),
                      actual_asymptotic_radiation_over_photons=src['Delta']*inverse['fnu'])
        for key,value in values.items(): check(key,r[key],value)
        check('energy_mapping',E,1.5*kb*oe*(c*H/co['gstar'])**2)
        check('saved_cold_parameter',chi,src['cold_parameter'])
        check('photon_mapping',src['Q']/(co['L']*og),src['Delta']*inverse['fnu'])
        check('area_lower',max(values['X_area_lower']-values['X'],0.),0.,values['X'])
        check('area_upper',max(values['X']-values['X_area_upper'],0.),0.,values['X'])
        check('J_lower',max(beta*R**4/cap-src['J_static'],0.),0.,src['J_static'])
        conditions = dict(global_hardening=eta**2<1/12,eta_small_square=eta<=small,
                          cosmic_span_small_square=1.5*b2<=small**2,
                          full_source_occupied=flo>ground,soft_source_dominates=soft>=5*beta)
        assert r['input_conditions'] == conditions
        assert r['input_certificate_qualified'] == all(conditions.values())
        assert r['failed_sufficient_conditions'] == [k for k,v in conditions.items() if not v]
        eps = co['gstar']*a/c**2
        for dom in r['domains']:
            L = dom['L']; lam = (cfg['j01_upper']**2+math.pi**2/4)/L**2
            crit = chi*eps**2*beta*R**4/(kb*cap*lam)
            uniform = chi*eps**2*beta*R**4/(kb*capmax*lam)
            bc = 4*crit/(1+math.sqrt(1+4*crit)); ic = crit/math.sqrt(1+bc/2)
            vals = dict(lambda_Lap_upper=lam,epsilon_scale=eps,H_a_L_over_c=H*a*L/c,
                        chi_critical=crit,chi_over_critical=chi/crit,uniform_chi_critical=uniform,
                        conditional_R_ceiling=(lam*kb*capmax/(beta*eps**2))**.25,
                        conditional_minimum_asymptotic_radiation_over_photons=oe/og*C4*ic**(4/3)/crit)
            for key,value in vals.items(): check(key,dom[key],value)
            check('critical_cosmic',crit,3*oe*(H*a/c)**2/(2*cap*lam))
            status = 'INPUT_HYPOTHESES_NOT_CERTIFIED'
            if all(conditions.values()):
                status = ('VIOLATES_CONDITIONAL_NECESSITY' if chi/crit<1-tol else
                          'PASSES_NECESSARY_NOT_SUFFICIENT_TEST' if chi/crit>1+tol else 'NUMERICAL_BOUNDARY')
            assert dom['status'] == status
    def select(r,label):
        if label == 'all': return True
        prefix = 'central:' if label=='central' else 'joint:' if label=='joint_any' else 'joint:'+label[-1]+':'
        return any(role.startswith(prefix) for role in r['roles'])
    assert len(p['summaries']) == 240
    for s in p['summaries']:
        rr = [r for r in p['rows'] if (r['background_id'],r['spectrum_index'])==(s['background_id'],s['spectrum_index']) and select(r,s['role_group'])]
        dd = [next(d for d in r['domains'] if d['L']==s['L']) for r in rr]
        ff = [d for d in dd if 'chi_over_critical' in d]
        assert s['state_count']==len(rr) and s['finite_state_count']==len(ff)
        assert s['input_qualified']==sum(r['input_certificate_qualified'] for r in rr)
        assert s['statuses']==dict(Counter(d['status'] for d in dd))
        for key, limits in s['ranges'].items():
            assert limits is not None
            for n,fun in enumerate([min,max]): check('summary_'+key,limits[n],fun(d[key] for d in ff))
    status_counts = dict(Counter(d['status'] for r in p['rows'] for d in r['domains']))
    assert status_counts == p['overall_domain_statuses'] and sum(status_counts.values())==2680
    assert sum(r['source_state_status']=='FINITE_HARD_STATE' for r in p['rows'])==1180
    role_summaries=[]
    for bi in backgrounds:
        for label in ['all','central','joint_any','joint_1','joint_2','joint_3']:
            rr=[r for r in p['rows'] if r['background_id']==bi and select(r,label)]
            for L in [1.,2.]:
                dd=[next(d for d in r['domains'] if d['L']==L) for r in rr]
                ff=[d for d in dd if 'chi_over_critical' in d]
                role_summaries.append(dict(background_id=bi,role_group=label,L=L,
                    states_including_four_spectrum_labels=len(rr),statuses=dict(Counter(d['status'] for d in dd)),
                    chi_over_critical=[min(d['chi_over_critical'] for d in ff),max(d['chi_over_critical'] for d in ff)],
                    local_interpolation_unqualified=sum(not r['local_interpolation_qualified'] for r in rr)))
    return dict(status='PASS' if not failures else 'FAIL',source_sha256=sha(Path(__file__)),input=meta,
                inverse_input=inverse_meta,authenticated=dict(manifests=len(seen),unique_files=len(files),member_occurrences=occurrences),
                arithmetic_checks=checks,max_scaled_error=maximum,failures=failures,
                states=1340,finite_states=1180,singular_limit_states=160,domain_rows=2680,status_counts=status_counts,
                role_summaries=role_summaries,producer_checks=sum(p['counts'].values()),producer_failures=p['failures'],
                producer_seconds=p['seconds'],producer_peak_self_rss_bytes=p['peak_self_rss_bytes'],
                scope='Saved arithmetic/custody only, no producer import, quadrature, inverse root, material evaluation or PDE. Role groups and numerical copies overlap; conditional finite clamped-domain theorem, not isolated-galaxy or continuous-interpolation exclusion. Author audit with separate independent peer source preflight.')

if __name__ == '__main__':
    payload=run()
    print(encode(dict(payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())
