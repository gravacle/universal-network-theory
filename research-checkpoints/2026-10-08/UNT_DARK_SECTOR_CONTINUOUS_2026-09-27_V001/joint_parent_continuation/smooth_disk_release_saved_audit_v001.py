"""Authenticate/recombine saved initial coefficients. No producer import."""
import base64, hashlib, json, math, zlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    seen=set();files={};occurrences=0
    def manifest(path):
        nonlocal occurrences
        path=path.resolve();path.relative_to(ROOT)
        if path in seen:return
        seen.add(path);files[str(path.relative_to(ROOT))]=sha(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            occurrences+=1;q=Path(name)
            candidates={p.resolve() for p in ([q] if q.is_absolute() else [ROOT/q,path.parent/q]) if p.is_file() and p.resolve().is_relative_to(ROOT)}
            assert len(candidates)==1
            p=candidates.pop();assert sha(p)==digest;files[str(p.relative_to(ROOT))]=digest
            if p.name.endswith('_FROZEN.json'):manifest(p)
    def read(stem,transport=False):
        path=HERE/(stem+('_TRANSPORT.json' if transport else '_RESULTS.json'));obj=json.loads(path.read_text())
        meta={'file_sha256':sha(path)}
        if transport:
            raw=zlib.decompress(base64.b64decode(obj['data'],validate=True))
            assert len(raw)==obj['raw_bytes'] and hashlib.sha256(raw).hexdigest()==obj['raw_sha256']
            meta.update(raw_sha256=obj['raw_sha256']);obj=json.loads(raw)
        f=HERE/(stem+'_FROZEN.json');manifest(f)
        assert obj['freeze_sha256']==sha(f) and obj['payload_sha256']==hashlib.sha256(encode(obj['payload'])).hexdigest()
        meta.update(freeze_sha256=sha(f),payload_sha256=obj['payload_sha256'])
        return obj['payload'],meta
    p,meta=read('SMOOTH_DISK_RELEASE_CERTIFICATE_V001')
    assert meta['file_sha256']=='773a3b57065e9c4fb6894064b6402e31f761dfe1de8beeb0754701c29ef24a04'
    old,_=read('FINITE_GAP_SHARED_SCREEN_V002',True)
    cal,_=read('GLOBAL_GAP_LIMIT_CALIBRATION_V001')
    assert p['status']=='COMPLETE' and not p['failures'] and p['checks']==881
    cfg=p['configuration'];assert cfg==json.loads((HERE/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_FROZEN.json').read_text())['configuration']
    states={r['R']:r for r in old['rows'] if r['spectrum_index']==1 and r['reference']==0 and r['R'] in [128,8192]}
    ref=cal['references'][0];assert p['reference']==ref
    G=cfg['G_m3_kg_s2'];c=cfg['c_m_s'];a=cfg['a_kpc']*1000*cfg['parsec_m'];beta=cfg['beta']
    kb=math.fsum(cal['spectra'][1]['spectrum']['weights'])+beta
    count=0;maximum=0.;failures=[]
    def check(name,x,y,scale=None,tol=2e-11):
        nonlocal count,maximum
        count+=1;den=max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
        er=abs(x-y)/den;maximum=max(maximum,er)
        if not math.isfinite(er) or er>tol:failures.append(dict(name=name,error=er))
    assert len(p['geometries'])==2 and len(p['cases'])==4
    for geo in p['geometries']:
        b=geo['b_over_a'];assert b in cfg['thickness_over_a']
        check('Dmax',geo['density_max'],(1+3*b)/(4*math.pi*b*(1+b)**3))
        check('tidal_bound',geo['tidal_bound'],1/(b*(1+b)**2))
        expected={(x,z) for x in cfg['radial_witnesses'] for z in cfg['vertical_witnesses']}
        assert len(geo['points'])==16 and {(v['x'],v['z']) for v in geo['points']}==expected
        for q in geo['points']:
            check('Poisson_trace',sum(q['potential_hessian'][i][i] for i in range(3)),4*math.pi*q['density'],geo['tidal_bound'])
            check('density_cylindrical_laplacian',q['density_laplacian'],q['density_hessian'][0][0]+q['density_hessian'][1][1]+(q['density_gradient'][0]/q['x'] if q['x'] else q['density_hessian'][0][0]))
            assert q['density']>0 and q['density']<=geo['density_max']*(1+2e-14)
            assert q['tidal_norm']<=geo['tidal_bound']*(1+2e-14)
            assert len(q['fd'])==4
            for f in q['fd']:
                which=f['field'];assert f['step'] in cfg['fd_steps']
                grad=q['density_gradient'] if which=='density' else q['potential_gradient']
                hess=q['density_hessian'] if which=='density' else [[q['potential_hessian'][i][j] for j in [0,2]] for i in [0,2]]
                ge=max(abs(f['gradient'][i]-grad[i])/max(f['gradient_scale'],abs(grad[i])) for i in range(2))
                he=max(abs(f['hessian'][i][j]-hess[i][j])/max(f['hessian_scale'],abs(hess[i][j])) for i in range(2) for j in range(2))
                check('saved_FD_gradient_error',f['gradient_scaled_error'],ge,1.)
                check('saved_FD_hessian_error',f['hessian_scaled_error'],he,1.)
                assert max(ge,he)<=cfg['fd_tolerance']
        for f in geo['finite_radius_mass_flux_controls']:
            rr=f['radius'];check('flux_lower',f['lower'],(rr/(rr+1+b))**3);check('flux_upper',f['upper'],1+1/rr)
            assert f['lower']<=f['normalized_radial_flux']<=f['upper']
    summaries=[]
    assert {(q['gap'],q['geometry_index']) for q in p['cases']}=={(R,i) for R in states for i in range(2)}
    for case in p['cases']:
        src=states[case['gap']];geo=p['geometries'][case['geometry_index']]
        assert case['source_state']=={k:src[k] for k in case['source_state']}
        b=a*geo['b_over_a'];GM=src['gstar']*a*a;M=GM/G;U=GM/(2*c*c*(a+b))
        ci=src['I']*src['eII']/src['omega'];cs2=c*c*ci
        rho=3*ref['H0_s_inverse']**2*ref['Omega_exc']/(8*math.pi*G)
        dm=M/a**3*geo['density_max'];ell=(M/(2*math.pi*dm))**(1/3);bp=3*math.pi*G*dm*ell/c**2
        tide=GM/a**3*geo['tidal_bound']
        fields=dict(Kb=kb,hard_weight=beta,a_m=a,b_m=b,GM_m3_s2=GM,rest_mass_kg=M,
            hard_mass_density_kg_m3=rho,hard_pressure_Pa=rho*c*c*src['w'],
            vacuum_energy_J_m3=3*ref['H0_s_inverse']**2*ref['Omega_Lambda']*c*c/(8*math.pi*G),
            background_H_s_inverse=ref['H0_s_inverse'],intrinsic_cs2_m2_s2=cs2,compactness_U=U,
            contraction_factor_upper=U,first_metric_iterate_uniform_error_upper=U**2,
            Dmax_kg_m3=dm,green_split_radius_m=ell,metric_gradient_bound_m_inverse=bp,
            frozen_source_tidal_bound_s2=tide,frozen_source_rest_caustic_sufficient_seconds=math.acosh(2)/math.sqrt(tide),
            frozen_source_central_vertical_caustic_seconds=math.pi/(2*math.sqrt(tide)))
        for key,value in fields.items():check(key,case[key],value)
        check('original_cI2',ci,src['cI2']);check('weighted_virial',beta*src['I']*src['omega'],src['E']+src['pressure'])
        assert 0<U<1 and len(case['points'])==16
        for q,g in zip(case['points'],geo['points']):
            assert (q['x'],q['z'])==(g['x'],g['z'])
            D=M/a**3*g['density'];grad=[M/a**4*v for v in g['density_gradient']];lap=M/a**5*g['density_laplacian']
            pot=GM/a*g['potential'];u=-pot/(2*c*c);lo=1+u/(1+U);hi=1+u
            A=4*math.pi*G*D;ag=[4*math.pi*G*v for v in grad];al=4*math.pi*G*lap
            eg=4*math.pi*G*(8*U*math.hypot(*grad)+6*D*bp)
            el=4*math.pi*G*(10*U*abs(lap)+10*bp*math.hypot(*grad)+30*D*bp*bp+12*math.pi*G*D*D/c**2)
            f=dict(D_kg_m3=D,potential_m2_s2=pot,psi_lower=lo,psi_upper=hi,
                focusing_gradient_error_bound_s2_m1=eg,focusing_laplacian_flat_s2_m2=al,
                focusing_laplacian_error_bound_s2_m2=el,orthonormal_velocity_tau3_norm_error_m_s4=cs2*eg/6,
                canonical_current_tau4_s4_leading=cs2*al/24,
                first_metric_iterate_constraint_residual_m2=2*math.pi*G*D/c**2*u/(1+u))
            for key,value in f.items():check(key,q[key],value)
            intervals={'focusing_s2_interval':[A/hi**6,A], 'fractional_density_tau2_interval':[A/hi**6/2,A/2],
                'hard_density_tau2_kg_m3_s2_interval':[rho*(1+src['w'])*v/2 for v in [A/hi**6,A]],
                'canonical_current_tau4_s4_interval':[cs2*(al-el)/24,cs2*(al+el)/24]}
            intervals['hard_pressure_tau2_Pa_s2_interval']=[cs2*v for v in intervals['hard_density_tau2_kg_m3_s2_interval']]
            intervals['potential_gradient_m_s2']=[GM/a**2*v for v in g['potential_gradient']]
            intervals['focusing_gradient_flat_s2_m1']=ag
            intervals['orthonormal_velocity_tau3_m_s4_leading']=[-cs2*v/6 for v in ag]
            for key,values in intervals.items():
                for actual,value in zip(q[key],values):check(key,actual,value)
            for i in range(3):
                for j in range(3):check('SI_tidal_tensor',q['potential_hessian_s2'][i][j],GM/a**3*g['potential_hessian'][i][j])
            assert q['first_metric_iterate_constraint_residual_m2']>0
        summaries.append(dict(gap=case['gap'],b_over_a=geo['b_over_a'],compactness_U=U,
            intrinsic_cI2=ci,source_rest_mass_kg=M,metric_gradient_bound=bp,
            current_sign_counts={sign:sum((v['canonical_current_tau4_s4_interval'][0]>0 if sign=='positive' else
                    v['canonical_current_tau4_s4_interval'][1]<0 if sign=='negative' else
                    v['canonical_current_tau4_s4_interval'][0]<=0<=v['canonical_current_tau4_s4_interval'][1]) for v in case['points']) for sign in ['positive','negative','includes_zero']},
            focusing_interval_global=[min(v['focusing_s2_interval'][0] for v in case['points']),max(v['focusing_s2_interval'][1] for v in case['points'])],
            maximum_velocity_coefficient= max(math.hypot(*v['orthonormal_velocity_tau3_m_s4_leading']) for v in case['points']),
            central_current_tau4=case['points'][0]['canonical_current_tau4_s4_interval'],
            frozen_source_caustic_seconds=case['frozen_source_central_vertical_caustic_seconds']))
    return dict(status='PASS' if not failures else 'FAIL',source_sha256=sha(Path(__file__)),input=meta,
        authenticated=dict(manifests=len(seen),unique_files=len(files),member_occurrences=occurrences),
        arithmetic_checks=count,max_scaled_error=maximum,failures=failures,cases=4,readouts=64,
        case_summaries=summaries,producer_checks=p['checks'],producer_worst_errors=p['worst_scaled_errors'],
        producer_seconds=p['elapsed_seconds'],producer_peak_self_rss_bytes=p['peak_bytes'],
        scope='Saved geometry/FD arrays and coefficient arithmetic only; no producer, Jet/FD reevaluation, metric/ODE solve or orbit calculation. Initial coefficient bounds, not finite-time evolution or candidate viability.')

if __name__=='__main__':
    p=run();print(encode(dict(payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())
