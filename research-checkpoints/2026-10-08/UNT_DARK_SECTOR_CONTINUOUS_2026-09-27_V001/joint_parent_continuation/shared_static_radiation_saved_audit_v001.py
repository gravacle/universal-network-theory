"""Authenticate and recombine saved certificate arithmetic; no producer import."""
import base64,hashlib,json,math,zlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
def encode(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    files={};seen=set();occurrences=0
    def manifest(path):
        nonlocal occurrences
        path=path.resolve();path.relative_to(ROOT)
        if path in seen:return
        seen.add(path);files[str(path.relative_to(ROOT))]=sha(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            occurrences+=1;q=Path(name)
            candidates={v.resolve() for v in ([q] if q.is_absolute() else [ROOT/q,path.parent/q]) if v.is_file() and v.resolve().is_relative_to(ROOT)}
            assert len(candidates)==1
            p=candidates.pop();assert sha(p)==digest;files[str(p.relative_to(ROOT))]=digest
            if p.name.endswith('_FROZEN.json'):manifest(p)
    def read(stem,transport=False):
        path=HERE/(stem+('_TRANSPORT.json' if transport else '_RESULTS.json'))
        obj=json.loads(path.read_text());meta={'file_sha256':sha(path)}
        if transport:
            raw=zlib.decompress(base64.b64decode(obj['data'],validate=True))
            assert len(raw)==obj['raw_bytes'] and hashlib.sha256(raw).hexdigest()==obj['raw_sha256']
            meta.update(raw_bytes=len(raw),raw_sha256=obj['raw_sha256']);obj=json.loads(raw)
        f=HERE/(stem+'_FROZEN.json');manifest(f)
        assert obj['freeze_sha256']==sha(f) and obj['payload_sha256']==hashlib.sha256(encode(obj['payload'])).hexdigest()
        meta.update(freeze_sha256=sha(f),payload_sha256=obj['payload_sha256'])
        return obj['payload'],meta
    p,meta=read('SHARED_STATIC_RADIATION_CERTIFICATE_V001',True)
    old,_=read('FINITE_GAP_SHARED_SCREEN_V002',True)
    photons,_=read('FINITE_GAP_PHOTON_BUDGET_V001')
    cal,_=read('GLOBAL_GAP_LIMIT_CALIBRATION_V001')
    assert p['configuration']==json.loads((HERE/'SHARED_STATIC_RADIATION_CERTIFICATE_V001_FROZEN.json').read_text())['configuration']
    cfg=p['configuration'];beta=cfg['beta'];c=cfg['c_m_s'];a=cfg['a_kpc']*1000*cfg['parsec_m'];d=cfg['small_square']
    C4=((3*math.sqrt(math.pi)/2)*math.gamma(.75)/math.gamma(.25))**(4/3)
    capmax=(1+3*d*d)*(1+3*d*d+d)/(1-d*d)
    count=0;maximum=0.;failures=[];status_counts={}
    def check(name,x,y,scale=None):
        nonlocal count,maximum
        count+=1;den=max(abs(x),abs(y),1e-300) if scale is None else max(abs(scale),1e-300)
        er=abs(x-y)/den;maximum=max(maximum,er)
        if not math.isfinite(er) or er>2e-11:failures.append(dict(name=name,error=er))
    check('C4',p['C4'],C4);check('uniform_Ecap',p['Ecap_small_domain_uniform'],capmax)
    assert len(p['rows'])==360 and len({(r['spectrum_index'],r['reference'],r['R']) for r in p['rows']})==360
    for r in p['rows']:
        i=r['source_row_index'];src=old['rows'][i];pr=photons['rows'][i];ref=cal['references'][r['reference']]
        assert (r['spectrum_index'],r['reference'],r['R'])==(src['spectrum_index'],src['reference'],src['R'])==(pr['spectrum_index'],pr['reference'],pr['R'])
        spec=cal['spectra'][r['spectrum_index']]['spectrum'];kb=math.fsum(spec['weights'])+beta
        R=r['R'];chi=src['E']/beta/R**4;eta=src['S']/R**2;H=ref['H0_s_inverse'];oe=ref['Omega_exc'];og=pr['Omega_gamma']
        b2=4*chi/(1+math.sqrt(1+4*chi));a1=(b2/2)/(1+math.sqrt(1+b2/2));a2=b2/(1+math.sqrt(1+b2))
        flo=(a1+a2)/2-(a1-a2)**2/(2*(2+a1+a2))
        fhi=(.75*b2)/(1+math.sqrt(1+.75*b2));ground=3*eta**2/(1+math.sqrt(1+3*eta**2))
        soft=math.fsum(w/(1+(src['S']/delta**2)**(2/3)) for delta,w in zip(spec['delta'],spec['weights']))
        cap=(1+3*eta**2)*(1+3*eta**2+eta)/(1-eta**2)
        values={'E':src['E'],'S':src['S'],'Kb':kb,'Omega_exc':oe,'Omega_gamma':og,'chi':chi,'eta_max':eta,
            'unit_turning_amplitude_squared':b2,'unit_action':src['I']/R**3,'frequency_excess_lower':flo,
            'frequency_excess_upper':fhi,'ground_frequency_excess_upper':ground,'radial_span_squared_upper':1.5*b2,
            'soft_B_over_S_lower':soft,'Tc_over_h2_lower':soft-5*beta,'Ecap':cap,
            'X':pr['Q']/src['E'],'X_area_lower':C4*(chi/math.sqrt(1+b2/2))**(4/3)/chi,
            'X_area_upper':min(1.,C4*chi**(1/3)),
            'saved_asymptotic_radiation_over_photons':pr['asymptote_over_photons']}
        for key,value in values.items():check(key,r[key],value)
        conditions={'global_hardening':eta*eta<1/12,'eta_small_square':eta<=d,
            'cosmic_span_small_square':1.5*b2<=d*d,'full_source_occupied':flo>ground,'soft_source_dominates':soft>=5*beta}
        assert r['input_conditions']==conditions and r['input_certificate_qualified']==all(conditions.values())
        assert set(r['failed_sufficient_conditions'])=={k for k,v in conditions.items() if not v}
        assert {v['L'] for v in r['domains']}=={1.,2.}
        eps=src['gstar']*a/c**2
        for dom in r['domains']:
            L=dom['L'];lam=(cfg['j01_upper']**2+math.pi**2/4)/L**2
            crit=chi*eps**2*beta*R**4/(kb*cap*lam)
            uniform=chi*eps**2*beta*R**4/(kb*capmax*lam)
            bc2=4*crit/(1+math.sqrt(1+4*crit));ilo=crit/math.sqrt(1+bc2/2)
            vv={'lambda_Lap_upper':lam,'epsilon_scale':eps,'H_a_L_over_c':H*a*L/c,'chi_critical':crit,
                'chi_over_critical':chi/crit,'uniform_small_domain_chi_critical':uniform,
                'conditional_R_ceiling':(lam*kb*capmax/(beta*eps**2))**.25,
                'conditional_minimum_asymptotic_radiation_over_photons':oe/og*C4*ilo**(4/3)/crit,
                'numerical_guard':cfg['arithmetic_tolerance']}
            for key,value in vv.items():check(key,dom[key],value)
            check('cosmological_critical',crit,3*oe*(H*a/c)**2/(2*cap*lam))
            ratio=chi/crit;status='INPUT_HYPOTHESES_NOT_CERTIFIED'
            if all(conditions.values()):
                status='VIOLATES_CONDITIONAL_NECESSITY' if ratio<1-2e-11 else 'PASSES_NECESSARY_NOT_SUFFICIENT_TEST' if ratio>1+2e-11 else 'NUMERICAL_BOUNDARY'
            assert dom['status']==status;status_counts[status]=status_counts.get(status,0)+1
    for group in p['summaries']:
        rr=[r for r in p['rows'] if r['R']==group['R']];dd=[next(v for v in r['domains'] if v['L']==group['L']) for r in rr]
        assert group['states']==len(rr)==72 and group['input_qualified']==sum(r['input_certificate_qualified'] for r in rr)
        assert group['statuses']=={s:sum(v['status']==s for v in dd) for s in {v['status'] for v in dd}}
        for key,limits in group['ranges'].items():
            for k,f in enumerate([min,max]):check('summary_'+key,limits[k],f(v[key] for v in dd))
    assert sum(status_counts.values())==720 and not p['failures']
    return dict(status='PASS' if not failures else 'FAIL',source_sha256=sha(Path(__file__)),input=meta,
        authenticated=dict(manifests=len(seen),unique_files=len(files),member_occurrences=occurrences),
        arithmetic_checks=count,max_scaled_error=maximum,failures=failures,
        producer_checks=sum(p['counts'].values()),producer_failures=p['failures'],states=360,domains=720,status_counts=status_counts,
        summaries=p['summaries'],producer_seconds=p['seconds'],producer_peak_self_rss_bytes=p['peak_self_rss_bytes'],
        scope='Saved-state arithmetic only; all conditional scientific statuses retained. No producer, orbit, quadrature, Bessel evaluation or PDE rerun. The certificate author performs this artifact audit; independent theorem/source preflight is separately bound.')
if __name__=='__main__':
    p=run();print(encode(dict(payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p)).decode())
