"""Inert extension of the unchanged static theorem to all inferred states."""
import base64,hashlib,importlib.util,json,math,resource,sys,time,zlib
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/'INFERRED_STATIC_RADIATION_CERTIFICATE_V001_FROZEN.json'
CONFIG=dict(beta=.005,L=[1.,2.],a_kpc=3.2,parsec_m=3.085677581491367e16,
    c_m_s=299792458.,small_square=.01,j01_upper=2.404825558,
    arithmetic_tolerance=2e-11,expected_points=67,expected_states=1340,
    expected_finite_states=1180,expected_domain_rows=2680)
SOURCE_HASH='783a37190e6c7f5f296089d97b01525596365fbc18a9ca03ddb4dc9e09b0aef4'
INVERSE_HASH='e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0'

def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def inputs():
    files={};seen=set()
    def add(p,expected=None):
        p=p.resolve(strict=True);p.relative_to(ROOT);digest=sha(p)
        if expected is not None and digest!=expected:raise RuntimeError('Changed input: '+str(p))
        files[str(p.relative_to(ROOT))]=digest;return p
    def manifest(p):
        p=add(p)
        if p in seen:return
        seen.add(p)
        for name,digest in json.loads(p.read_text())['files'].items():
            q=Path(name);candidates={x.resolve() for x in ([q] if q.is_absolute() else [ROOT/q,p.parent/q]) if x.is_file() and x.resolve().is_relative_to(ROOT)}
            if len(candidates)!=1:raise RuntimeError('Missing/ambiguous member: '+name)
            q=add(candidates.pop(),digest)
            if q.name.endswith('_FROZEN.json'):manifest(q)
    def wrapper(stem,expected):
        path=add(HERE/(stem+'_RESULTS.json'),expected);w=json.loads(path.read_text());f=HERE/(stem+'_FROZEN.json');manifest(f)
        if w['freeze_sha256']!=sha(f) or w['payload_sha256']!=hashlib.sha256(encode(w['payload'])).hexdigest():raise RuntimeError('Wrapper mismatch')
        return w['payload']
    inverse=wrapper('BBN_SHARED_INVERSE_V001',INVERSE_HASH)
    if inverse['status']!='COMPLETE_CONDITIONAL_PROXY_INVERSE' or inverse['failures'] or inverse['inherited_table_controls']['failures']:
        raise RuntimeError('Inverse not qualified')
    cal=wrapper('GLOBAL_GAP_LIMIT_CALIBRATION_V001','11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628')
    if cal['status']!='COMPLETE' or cal['failures']:raise RuntimeError('Calibration changed')
    oldsource=add(HERE/'shared_static_radiation_certificate_v001.py',SOURCE_HASH)
    manifest(HERE/'SHARED_STATIC_RADIATION_CERTIFICATE_V001_FROZEN.json')
    oldconfig=json.loads((HERE/'SHARED_STATIC_RADIATION_CERTIFICATE_V001_FROZEN.json').read_text())['configuration']
    for key in ['beta','L','a_kpc','parsec_m','c_m_s','small_square','j01_upper','arithmetic_tolerance']:
        if CONFIG[key]!=oldconfig[key]:raise RuntimeError('Theorem/geometry control changed: '+key)
    # Authenticate then import only definitions; call three pure scalar formulas.
    spec=importlib.util.spec_from_file_location('owned_static_certificate_math',oldsource)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    for name in [Path(__file__).name,'INFERRED_STATIC_RADIATION_CERTIFICATE_PROTOCOL_V001.md',
        'BBN_SHARED_INVERSE_V001_REVIEW.md','BBN_SHARED_INVERSE_V001_SAVED_AUDIT.json']:
        add(HERE/name)
    points=inverse['table_points'];states=inverse['state_rows']
    if len(points)!=CONFIG['expected_points'] or len(states)!=CONFIG['expected_states']:
        raise RuntimeError('Inverse census changed')
    if sum(r['status']=='FINITE_HARD_STATE' for r in states)!=CONFIG['expected_finite_states']:
        raise RuntimeError('Finite census changed')
    expected={(p['point_id'],bg['background_id'],si) for p in points for bg in inverse['backgrounds'] for si in range(4)}
    if {(r['point_id'],r['background_id'],r['spectrum_index']) for r in states}!=expected or len(expected)!=len(states):
        raise RuntimeError('Incomplete state associations')
    return helper,inverse,cal,dict(configuration=CONFIG,files=files)

def run(helper,inverse,cal):
    start=time.perf_counter();counts={};maxima={};failures=[];rows=[]
    tol=CONFIG['arithmetic_tolerance'];beta=CONFIG['beta'];c=CONFIG['c_m_s']
    a=CONFIG['a_kpc']*1000*CONFIG['parsec_m'];small=CONFIG['small_square'];capmax=helper.curvature_cap(small)
    points={p['point_id']:p for p in inverse['table_points']};backgrounds={b['background_id']:b for b in inverse['backgrounds']}
    constants={(v['background_id'],v['spectrum_index']):v for v in inverse['constants']}
    C4=(math.pi/(math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)))**(4/3)
    def check(name,x,y,scale=None):
        den=max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
        er=abs(x-y)/den;counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),er)
        if not math.isfinite(er) or er>tol:failures.append(dict(check=name,state=len(rows),error=er))
    check('C4',C4,inverse['C4'])
    for index,src in enumerate(inverse['state_rows']):
        point=points[src['point_id']];bg=backgrounds[src['background_id']];co=constants[(src['background_id'],src['spectrum_index'])]
        row=dict(source_state_index=index,point_id=src['point_id'],background_id=src['background_id'],
            old_reference_labels=bg['old_labels'],spectrum_index=src['spectrum_index'],
            soft_spectrum_metadata=inverse['soft_spectra_metadata'][src['spectrum_index']],
            roles=point['roles'],coarse_Delta_node=point['coarse_node'],
            local_interpolation_qualified=point['prediction']['local_numerical_rectangle'],
            omega_b=src['omega_b'],Delta=src['Delta'],source_state_status=src['status'])
        if src['status']!='FINITE_HARD_STATE':
            label='INFINITE_GAP_LIMIT_NOT_TESTED' if src['status']=='INFINITE_GAP_STANDARD_LIMIT' else 'UNSUPPORTED_SOURCE_STATE_NOT_TESTED'
            row.update(input_certificate_qualified=False,R=src.get('R'),
                domains=[dict(L=L,status=label) for L in CONFIG['L']],
                interpretation='Not a finite-state violation or an assumed empty copy. The singular limit requires a separate analysis.')
            rows.append(row);continue
        R=src['R'];E=src['E'];S=src['S'];kb=co['Kb'];oe=src['Omega_exc'];og=co['Omega_gamma'];H=bg['H0_s_inverse']
        spec=cal['spectra'][src['spectrum_index']]['spectrum'];ds=spec['delta'];ws=spec['weights']
        check('soft_contact',kb,math.fsum(ws)+beta)
        check('shared_energy',E,1.5*kb*oe*(c*H/co['gstar'])**2)
        check('photon_coordinate',src['Q']/(co['L']*og*inverse['fnu']),src['Delta'])
        chi=E/(beta*R**4);eta=S/R**2;b2=helper.amplitude2(chi)
        flo,fhi=helper.frequency_bounds(b2);ground=3*eta**2/(math.sqrt(1+3*eta**2)+1)
        soft=math.fsum(w*d*d/(d*d+(d*S)**(2/3)) for d,w in zip(ds,ws))
        conditions=dict(global_hardening=eta*eta<1/12,eta_small_square=eta<=small,
            cosmic_span_small_square=1.5*b2<=small*small,
            full_source_occupied=flo>ground,soft_source_dominates=soft>=5*beta)
        qualified=all(conditions.values());cap=helper.curvature_cap(eta) if eta<1 else None
        X=C4*(src['I']/R**3)**(4/3)/chi
        Xlo=C4*chi**(1/3)/(1+b2/2)**(2/3);Xhi=min(1.,C4*chi**(1/3))
        check('saved_chi',chi,src['cold_parameter']);check('saved_X',X,src['Q_over_E'])
        check('X_lower',max(Xlo-X,0.),0.,X);check('X_upper',max(X-Xhi,0.),0.,X)
        check('saved_frequency_lower',max(1+flo-src['omega']/R,0.),0.,1)
        check('saved_frequency_upper',max(src['omega']/R-1-fhi,0.),0.,1)
        if conditions['global_hardening']:check('J_lower',max(beta*R**4/cap-src['J_static'],0.),0.,src['J_static'])
        if conditions['eta_small_square']:check('uniform_cap',max(cap-capmax,0.),0.,capmax)
        domains=[];eps=co['gstar']*a/c**2
        for L in CONFIG['L']:
            lam=(CONFIG['j01_upper']**2+math.pi**2/4)/L**2
            critical=3*oe*(H*a/c)**2/(2*cap*lam) if cap is not None else None
            ratio=chi/critical if critical is not None else None
            if critical is not None:check('necessary_normalization',critical/chi,eps**2*beta*R**4/(kb*cap*lam))
            uniform=3*oe*(H*a/c)**2/(2*capmax*lam);ceiling=(E/(beta*uniform))**.25
            if critical is not None:
                bc=helper.amplitude2(critical)
                photon_floor=oe/og*C4*critical**(1/3)/(1+bc/2)**(2/3)
            else:photon_floor=None
            status='INPUT_HYPOTHESES_NOT_CERTIFIED'
            if qualified:status='VIOLATES_CONDITIONAL_NECESSITY' if ratio<1-tol else 'PASSES_NECESSARY_NOT_SUFFICIENT_TEST' if ratio>1+tol else 'NUMERICAL_BOUNDARY'
            domains.append(dict(L=L,status=status,lambda_Lap_upper=lam,epsilon_scale=eps,H_a_L_over_c=H*a*L/c,
                chi_critical=critical,chi_over_critical=ratio,uniform_chi_critical=uniform,
                conditional_R_ceiling=ceiling,conditional_minimum_asymptotic_radiation_over_photons=photon_floor))
        row.update(R=R,E=E,I=src['I'],S=S,Kb=kb,Omega_exc=oe,Omega_gamma=og,
            chi=chi,eta_max=eta,Ecap=cap,frequency_excess_lower=flo,frequency_excess_upper=fhi,
            ground_frequency_excess_upper=ground,radial_span_squared_upper=1.5*b2,
            soft_B_over_S_lower=soft,Tc_over_h2_lower=soft-5*beta,
            input_conditions=conditions,input_certificate_qualified=qualified,
            failed_sufficient_conditions=[k for k,v in conditions.items() if not v],
            X=X,X_area_lower=Xlo,X_area_upper=Xhi,
            actual_asymptotic_radiation_over_photons=src['Q']/(co['L']*og),domains=domains)
        rows.append(row)
    check('state_census',len(rows),CONFIG['expected_states'],1)
    check('domain_census',sum(len(r['domains']) for r in rows),CONFIG['expected_domain_rows'],1)
    summaries=[]
    for bi in sorted(backgrounds):
        for si in range(4):
            for label in ['all','central','joint_any','joint_1','joint_2','joint_3']:
                def selected(r):
                    if r['background_id']!=bi or r['spectrum_index']!=si:return False
                    if label=='all':return True
                    prefix='central:' if label=='central' else 'joint:' if label=='joint_any' else 'joint:'+label[-1]+':'
                    return any(role.startswith(prefix) for role in r['roles'])
                subset=[r for r in rows if selected(r)]
                for L in CONFIG['L']:
                    dom=[next(d for d in r['domains'] if d['L']==L) for r in subset]
                    finite=[d for d in dom if 'chi_over_critical' in d]
                    statuses={s:sum(d['status']==s for d in dom) for s in sorted({d['status'] for d in dom})}
                    summaries.append(dict(background_id=bi,spectrum_index=si,role_group=label,L=L,
                        state_count=len(subset),finite_state_count=len(finite),input_qualified=sum(r['input_certificate_qualified'] for r in subset),statuses=statuses,
                        ranges={key:([min(d[key] for d in finite if d[key] is not None),max(d[key] for d in finite if d[key] is not None)] if finite else None)
                            for key in ['chi_over_critical','conditional_R_ceiling','conditional_minimum_asymptotic_radiation_over_photons']}))
    overall={}
    for r in rows:
        for d in r['domains']:overall[d['status']]=overall.get(d['status'],0)+1
    return dict(status='FAILED_NUMERICAL_CONTROLS' if failures else 'COMPLETE_CONDITIONAL_INFERRED_CERTIFICATE',
        configuration=CONFIG,counts=counts,maxima=maxima,failures=failures,C4=C4,Ecap_uniform=capmax,
        table_points=inverse['table_points'],backgrounds=inverse['backgrounds'],reference_mapping=inverse['reference_mapping'],
        rows=rows,summaries=summaries,overall_domain_statuses=overall,
        seconds=time.perf_counter()-start,peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        scope='Unchanged finite-domain necessary theorem on ALL sampled inferred finite states; root-calibration data already exposed. Role groups overlap and are not independent tests. No continuous interslice or isolated-galaxy exclusion; singular Delta=0 limit not tested as a finite state; no new BBN abundance threshold.')

def main():
    helper,inverse,cal,snapshot=inputs()
    if sys.argv[1:]==['freeze']:print(encode(snapshot).decode());return 0
    if sys.argv[1:]!=['run']:raise RuntimeError('Use freeze or run')
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Frozen input mismatch')
    p=run(helper,inverse,cal);raw=encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p))
    print(encode(dict(encoding='zlib_base64_canonical_json',raw_sha256=hashlib.sha256(raw).hexdigest(),raw_bytes=len(raw),
        data=base64.b64encode(zlib.compress(raw,9)).decode(),summary={k:p[k] for k in ['status','counts','maxima','failures','overall_domain_statuses','seconds','peak_self_rss_bytes']})).decode())
    return 2 if p['failures'] else 0
if __name__=='__main__':sys.exit(main())
