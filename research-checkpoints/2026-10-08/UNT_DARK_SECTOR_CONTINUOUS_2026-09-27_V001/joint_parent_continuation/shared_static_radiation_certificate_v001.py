"""Inert saved-state theorem certificate; stdlib arithmetic, stdout only."""
import base64
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import zlib

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE/'SHARED_STATIC_RADIATION_CERTIFICATE_V001_FROZEN.json'
CONFIG = dict(beta=.005, R=[32,128,512,2048,8192], L=[1.,2.],
              a_kpc=3.2, parsec_m=3.085677581491367e16, c_m_s=299792458.,
              small_square=.01, j01_upper=2.404825558,
              arithmetic_tolerance=2e-11, expected_states=360,
              expected_domain_rows=720)
PINNED = {
    'FINITE_GAP_SHARED_SCREEN_V002_TRANSPORT.json':'11d5898717488b1ab3fb75e3294e55e5674f2b3f2d623f15cc9bb2e9a54c4db4',
    'FINITE_GAP_PHOTON_BUDGET_V001_RESULTS.json':'23feee802337320fde647fe87ff3ff24b1006c935cc3f31d9cf6a4a9574dba10',
    'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json':'11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628',
    'SHARED_STATIC_RADIATION_NECESSITY_V001.md':'190882b4f19f21756b00212a709bf7983a402f32fae90fb992c5617fd026c970',
    'clamped_common_phase_patch_v001.py':'c4279bb3690174f2158eb46c46b23adfed008c9585e5f2bf381e0eb04744a3b3',
    'CLAMPED_COMMON_PHASE_PATCH_PROTOCOL_V001.md':'b867a6db67d8bfcc1746bbf14830acd8a10c36bfbaa31dc049bb045f21bb7daa',
}

def encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inputs():
    files,seen={},set()
    def add(path,expected=None):
        path=path.resolve(strict=True);path.relative_to(ROOT)
        digest=sha(path)
        if expected is not None and digest!=expected:raise RuntimeError('Input changed: '+str(path))
        files[str(path.relative_to(ROOT))]=digest
        return path
    def manifest(path):
        path=add(path)
        if path in seen:return
        seen.add(path)
        for name,digest in json.loads(path.read_text())['files'].items():
            q=Path(name);candidates=set()
            for option in ([q] if q.is_absolute() else [ROOT/q,path.parent/q]):
                if not option.is_file():continue
                option=option.resolve()
                if option.is_relative_to(ROOT):candidates.add(option)
            if len(candidates)!=1:raise RuntimeError('Missing/ambiguous member: '+name)
            q=add(candidates.pop(),digest)
            if q.name.endswith('_FROZEN.json'):manifest(q)
    for name,digest in PINNED.items():add(HERE/name,digest)
    def wrapper(stem,transport=False):
        suffix='_TRANSPORT.json' if transport else '_RESULTS.json'
        path=add(HERE/(stem+suffix))
        packet=json.loads(path.read_text())
        if transport:
            raw=zlib.decompress(base64.b64decode(packet['data'],validate=True))
            if len(raw)!=packet['raw_bytes'] or hashlib.sha256(raw).hexdigest()!=packet['raw_sha256']:
                raise RuntimeError('Transport mismatch')
            packet=json.loads(raw)
        f=HERE/(stem+'_FROZEN.json');manifest(f)
        p=packet['payload']
        if packet['freeze_sha256']!=sha(f) or packet['payload_sha256']!=hashlib.sha256(encode(p)).hexdigest():
            raise RuntimeError('Wrapper mismatch: '+stem)
        if p['status']!='COMPLETE' or p['failures']:raise RuntimeError('Inherited numerical qualification failed')
        return p
    old=wrapper('FINITE_GAP_SHARED_SCREEN_V002',True)
    photons=wrapper('FINITE_GAP_PHOTON_BUDGET_V001')
    calibration=wrapper('GLOBAL_GAP_LIMIT_CALIBRATION_V001')
    for name in [Path(__file__).name,'SHARED_STATIC_RADIATION_CERTIFICATE_PROTOCOL_V001.md']:
        add(HERE/name)
    expected={(s,r,R) for s in range(4) for r in range(18) for R in CONFIG['R']}
    for p in [old,photons]:
        if len(p['rows'])!=360 or {(r['spectrum_index'],r['reference'],r['R']) for r in p['rows']}!=expected:
            raise RuntimeError('Inherited state census changed')
    return old,photons,calibration,dict(configuration=CONFIG,files=files)

def amplitude2(chi):
    return 4*chi/(1+math.sqrt(1+4*chi))

def curvature_cap(eta):
    return (1+3*eta*eta+eta)*(1+3*eta*eta)/(1-eta*eta)

def frequency_bounds(b2):
    # Convex-period chord / Jensen, with rationalized small excesses.
    a=(b2/2)/(math.sqrt(1+b2/2)+1)
    b=b2/(math.sqrt(1+b2)+1)
    lower=(a+b+2*a*b)/(2+a+b)
    upper=(3*b2/4)/(math.sqrt(1+3*b2/4)+1)
    return lower,upper

def j0_series(x):
    term=1.;terms=[term]
    for n in range(1,41):
        term*=-(x*x/4)/(n*n);terms.append(term)
    return math.fsum(terms)

def run(old,photons,calibration):
    start=time.perf_counter();counts={};maxima={};failures=[];rows=[]
    tol=CONFIG['arithmetic_tolerance'];beta=CONFIG['beta'];c=CONFIG['c_m_s']
    a=CONFIG['a_kpc']*1000*CONFIG['parsec_m'];d=CONFIG['small_square']
    def check(name,got,wanted,scale=None):
        den=max(abs(got),abs(wanted),1e-300) if scale is None else max(abs(scale),1e-300)
        error=abs(got-wanted)/den
        counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),error)
        if not math.isfinite(error) or error>tol:failures.append(dict(check=name,state=len(rows),error=error))
    C4=(math.pi/(math.gamma(.25)*math.gamma(1.5)/math.gamma(1.75)))**(4/3)
    check('quartic_constant',C4,photons['C'])
    check('j01_upper_sign',int(j0_series(CONFIG['j01_upper'])<0),1,1)
    check('j01_lower_sign',int(j0_series(2.404825557)>0),1,1)
    # This is a known first-zero bracket, not a new eigenproblem.
    for chi in [1e-16,1e-8,.01,1.,100.]:
        b2=amplitude2(chi);check('turning_energy',b2/2+b2*b2/4,chi)
        lo,hi=frequency_bounds(b2)
        check('frequency_bound_positive',int(lo>0 and hi>0),1,1)
        check('frequency_bound_order',max(lo-hi,0.),0.,max(lo,hi))
        lower=C4*chi**(1/3)/(1+b2/2)**(2/3)
        upper=min(1.,C4*chi**(1/3))
        check('area_bound_order',int(0<lower<=upper),1,1)
    cap_uniform=curvature_cap(d)
    pr={r['source_row_index']:r for r in photons['rows']}
    for index,src in enumerate(old['rows']):
        ref=calibration['references'][src['reference']]
        spectrum=calibration['spectra'][src['spectrum_index']]['spectrum']
        ds=spectrum['delta'];ws=spectrum['weights'];kb=math.fsum(ws)+beta
        if len(ds)!=len(ws) or not all(x>0 for x in ds+ws):raise RuntimeError('Invalid inherited soft measure')
        p=pr[index]
        if (p['spectrum_index'],p['reference'],p['R'])!=(src['spectrum_index'],src['reference'],src['R']):
            raise RuntimeError('Photon row association changed')
        R=src['R'];E=src['E'];S=src['S'];H=ref['H0_s_inverse'];oe=ref['Omega_exc'];og=p['Omega_gamma']
        chi=E/(beta*R**4);eta=S/R**2;b2=amplitude2(chi)
        check('source_E',p['E_present'],E);check('source_excitation',p['Omega_exc'],oe)
        check('calibration_energy',E,3*kb*oe*(c*H)**2/(2*src['gstar']**2))
        lower_om,upper_om=frequency_bounds(b2)
        ground_upper=3*eta*eta/(math.sqrt(1+3*eta*eta)+1)
        radial_span2_upper=1.5*b2
        # No small saved omega/R-1 subtraction is used for any certificate.
        check('saved_frequency_lower',max(1+lower_om-src['omega']/R,0.),0.,1)
        check('saved_frequency_upper',max(src['omega']/R-1-upper_om,0.),0.,1)
        soft_terms=[w*x*x/(x*x+(x*S)**(2/3)) for x,w in zip(ds,ws)]
        soft_lower=math.fsum(soft_terms)
        conditions=dict(global_hardening=eta*eta<1/12,
            eta_small_square=eta<=d,
            cosmic_span_small_square=radial_span2_upper<=d*d,
            full_source_occupied=lower_om>ground_upper,
            soft_source_dominates=soft_lower>=5*beta)
        qualified=all(conditions.values())
        ecap=curvature_cap(eta) if eta<1 else None
        if conditions['eta_small_square']:check('uniform_Ecap',max(ecap-cap_uniform,0.),0.,cap_uniform)
        i=src['I']/R**3;X=C4*i**(4/3)/chi
        Xlo=C4*chi**(1/3)/(1+b2/2)**(2/3);Xhi=min(1.,C4*chi**(1/3))
        check('unit_action_lower',max(chi/math.sqrt(1+b2/2)-i,0.),0.,i)
        check('unit_action_upper',max(i-chi,0.),0.,chi)
        check('radiation_ratio',X,p['Q_over_E'])
        check('radiation_lower',max(Xlo-X,0.),0.,X)
        check('radiation_upper',max(X-Xhi,0.),0.,X)
        if conditions['global_hardening']:
            check('saved_J_lower',max(beta*R**4/ecap-src['J_static'],0.),0.,src['J_static'])
        domains=[]
        for L in CONFIG['L']:
            lam=(CONFIG['j01_upper']**2+math.pi**2/4)/L**2
            critical=3*oe*(H*a/c)**2/(2*ecap*lam) if ecap is not None else None
            eps=src['gstar']*a/c**2
            reaction_lower=eps*eps*beta*R**4/(kb*ecap) if ecap is not None else None
            if critical is not None:check('necessary_normalization',reaction_lower/lam,critical/chi)
            uniform_critical=3*oe*(H*a/c)**2/(2*cap_uniform*lam)
            R_ceiling=(E/(beta*uniform_critical))**.25
            crit_b2=amplitude2(critical) if critical is not None else None
            radiation_lower=(oe/og*C4*critical**(1/3)/(1+crit_b2/2)**(2/3)) if critical is not None else None
            ratio=chi/critical if critical is not None else None
            status='INPUT_HYPOTHESES_NOT_CERTIFIED'
            if qualified:
                status=('VIOLATES_CONDITIONAL_NECESSITY' if ratio<1-tol else
                        'PASSES_NECESSARY_NOT_SUFFICIENT_TEST' if ratio>1+tol else 'NUMERICAL_BOUNDARY')
            domains.append(dict(L=L,lambda_Lap_upper=lam,epsilon_scale=eps,
                H_a_L_over_c=H*a*L/c,chi_critical=critical,chi_over_critical=ratio,
                uniform_small_domain_chi_critical=uniform_critical,
                conditional_R_ceiling=R_ceiling,
                conditional_minimum_asymptotic_radiation_over_photons=radiation_lower,
                numerical_guard=tol,status=status,
                interpretation='Conditional on an everywhere attractive, occupied, elliptic weak-metric solution with the unchanged positive sheet and prescribed mixed clamps; no exterior or existence assertion.'))
        rows.append(dict(source_row_index=index,spectrum_index=src['spectrum_index'],reference=src['reference'],R=R,
            E=E,S=S,Kb=kb,Omega_exc=oe,Omega_gamma=og,chi=chi,eta_max=eta,
            unit_turning_amplitude_squared=b2,unit_action=i,
            frequency_excess_lower=lower_om,frequency_excess_upper=upper_om,
            ground_frequency_excess_upper=ground_upper,radial_span_squared_upper=radial_span2_upper,
            soft_B_over_S_lower=soft_lower,Tc_over_h2_lower=soft_lower-5*beta,
            Ecap=ecap,input_conditions=conditions,input_certificate_qualified=qualified,
            failed_sufficient_conditions=[k for k,v in conditions.items() if not v],
            X=X,X_area_lower=Xlo,X_area_upper=Xhi,
            saved_asymptotic_radiation_over_photons=p['asymptote_over_photons'],domains=domains))
    check('state_census',len(rows),CONFIG['expected_states'],1)
    check('domain_census',sum(len(r['domains']) for r in rows),CONFIG['expected_domain_rows'],1)
    summaries=[]
    for R in CONFIG['R']:
        states=[r for r in rows if r['R']==R]
        for L in CONFIG['L']:
            dd=[next(d for d in r['domains'] if d['L']==L) for r in states]
            statuses={s:sum(d['status']==s for d in dd) for s in sorted({d['status'] for d in dd})}
            summaries.append(dict(R=R,L=L,states=len(states),input_qualified=sum(r['input_certificate_qualified'] for r in states),
                statuses=statuses,ranges={k:[min(d[k] for d in dd if d[k] is not None),max(d[k] for d in dd if d[k] is not None)]
                for k in ['chi_over_critical','conditional_R_ceiling','conditional_minimum_asymptotic_radiation_over_photons']}))
    return dict(status='FAILED_NUMERICAL_CONTROLS' if failures else 'COMPLETE_CONDITIONAL_CERTIFICATE',
        configuration=CONFIG,C4=C4,Ecap_small_domain_uniform=cap_uniform,
        counts=counts,maxima=maxima,failures=failures,rows=rows,summaries=summaries,
        seconds=time.perf_counter()-start,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),
        scope='Saved-state algebraic necessary-condition screen, no quadrature, orbit root, spatial solve, new fit or abundance threshold. Insufficient input certificates and violated conditional necessities are scientific statuses, not numerical failures. Passing necessity does not prove existence; no finite clamp is identified with a galaxy exterior.')

def main():
    old,photons,calibration,snapshot=inputs()
    if sys.argv[1:]==['freeze']:
        print(encode(snapshot).decode());return 0
    if sys.argv[1:]!=['run']:raise RuntimeError('Use freeze or run')
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Frozen inputs differ')
    p=run(old,photons,calibration)
    raw=encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p))
    print(encode(dict(encoding='zlib_base64_canonical_json',raw_sha256=hashlib.sha256(raw).hexdigest(),raw_bytes=len(raw),
        data=base64.b64encode(zlib.compress(raw,9)).decode(),
        summary={k:p[k] for k in ['status','counts','maxima','failures','summaries','seconds','peak_self_rss_bytes']})).decode())
    return 2 if p['failures'] else 0

if __name__=='__main__':sys.exit(main())
