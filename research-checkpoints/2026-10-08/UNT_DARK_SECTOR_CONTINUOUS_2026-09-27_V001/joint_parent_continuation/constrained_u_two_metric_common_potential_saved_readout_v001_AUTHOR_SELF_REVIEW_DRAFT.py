"""Saved-data only common-potential readout. Root alone executes; no scientific imports."""
from pathlib import Path
from decimal import Decimal,localcontext
from datetime import datetime,timezone
import argparse,hashlib,json,os,time
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_TWO_METRIC_COMMON_POTENTIAL_SAVED_READOUT_V001'
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V002'
PROTOCOL_SHA='32fa157078bc1446719b22fd734381a7f288c6d96a0a85c5a598d499883914d1'
PINS={'constrained_u_clock_gradient_two_metric_finite_rate_v002.py': '1bc69c6bf56a6b08e13702e1730ec93a686ecb05e86a2d1823fb54d435d5d48a', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V002.md': '321dbb055024acc3d638cd6a7f2eb47a5ed001adcea95ac2ce9b265da784f581', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V002_RESULT.json': '0cf7c380575924aa2a2228e85a4caefe8b7dd402b1ff5c880e92b1a0645fb405', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V002_RECEIPT.json': 'af775fbeb06e9d4519566b2ac874a5d3a49522f1bfb0feed20b9ace872f6c050', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V002_REPORT.md': '65b4486b7734000b2b439baa57f1bf18e62c122abe8275b67f5948fdc6411ae8', 'CONSTRAINED_U_TWO_METRIC_LOCAL_EINSTEIN_FEEDBACK_BOUND_V002.md': 'f44920ccde0178c7fdf5187d6884eb14b62135a0a37449b38fb16ff3337c44b1', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V001_RESULT.json': '5561bee978a98ebbaa9af8fd83e0c965f0e24a9abf0ee1a68c6f6e48ba4a3574'}
TOL=Decimal('2e-11');FLOOR=Decimal('1e-30')
SEALS={};CREATED={};CHECKS=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(n):return json.loads((BASE/n).read_text())
def D(x):return Decimal(str(x))
def require(ok,name):
    if not ok:raise AssertionError(name)
def seal(p,h):
    p=Path(p).resolve();require(sha(p)==h,'Input changed '+str(p))
    require(str(p) not in SEALS or SEALS[str(p)]==h,'Conflicting seal')
    SEALS[str(p)]=h

def rehash(source):
    for p,h in dict(SEALS,**CREATED).items():require(sha(p)==h,'Seal changed '+p)
    require(sha(__file__)==source,'Source changed')
def serial(x):
    if isinstance(x,Decimal):return str(x)
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def write(n,x,raw=False):
    p=BASE/n;data=x if raw else (json.dumps(serial(x),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);h=sha(p);CREATED[str(p.resolve())]=h;return h

def close(name,a,b,scale=None):
    den=max(abs(a)+abs(b) if scale is None else scale,FLOOR)
    err=abs(a-b)/den
    CHECKS.append(dict(name=name,error=err,tolerance=TOL,passed=err.is_finite() and err<=TOL))

def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    p=read(PARENT+'_RESULT.json');r=read(PARENT+'_RECEIPT.json');m=p['manifest']
    require(p['status']==r['status']=='ARITHMETIC_PASS','Parent arithmetic status')
    require(len(p['numerical_gates'])==2058 and all(g['passed'] for g in p['numerical_gates']),'Parent2058 gates')
    old=read('CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V001_RESULT.json')
    bad=[g for g in old['numerical_gates'] if not g['passed']]
    require(old['status']=='ARITHMETIC_FAILED' and len(bad)==18 and p['preserved_old_failed_controls']==bad,'Preserved18 failures')
    require(r['result_sha256']==PINS[PARENT+'_RESULT.json'] and r['report_sha256']==PINS[PARENT+'_REPORT.md'],'Receipt result/report')
    require(r['source_sha256']==m['source_sha256']==PINS['constrained_u_clock_gradient_two_metric_finite_rate_v002.py'],'Source identity')
    require(r['inputs']==m['inputs'],'Input map equality')
    for n,h in m['inputs'].items():seal(n,h)
    seal(BASE/(PARENT+'_MANIFEST.json'),r['manifest_sha256']);require(read(PARENT+'_MANIFEST.json')==m,'Manifest equality')
    seal(BASE/(PARENT+'_JOURNAL.jsonl'),r['journal_sha256'])
    events=[json.loads(x) for x in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    require([e['event'] for e in events]==['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'],'Six-event journal')
    require(events[0]['owner']=='root' and events[0]['source_sha256']==m['source_sha256'],'Owner/source')
    require(events[-1]['result_sha256']==r['result_sha256'] and events[-1]['gates']==2058 and events[-1]['passed']==2058,'Closure census')
    require(len(r['checkpoint_seals'])==8,'Eight checkpoint seals')
    for n,h in r['checkpoint_seals'].items():seal(n,h)
    for i,e in enumerate(events[1:5]):
        cp=PARENT+'_CP_'+str(i).zfill(2)+'.json';co=cp[:-5]+'_COMMIT.json'
        commit=read(co);require(commit['checkpoint']==cp and commit['sha256']==sha(BASE/cp),'Checkpoint commit')
        require(e['commit_sha256']==sha(BASE/co),'Journal commit')
    require(len(p['rows'])==128 and len(p['modal_points'])==64,'Full row census')
    return p,r,bad

def diagnostics(x,bg,q):
    gap=min(bg['lower_gap'],bg['upper_gap']);s=bg['cs']
    heads=dict(phase_rate=s*x['clock_d'],phase_gap=gap,phase_rate_fraction=abs(s*x['clock_d'])/gap,
      phase_velocity=q*x['V_phi'],U_tilt=q*x['pi_U'],relative_velocity=q*x['relative_v'],
      phase_square_over_gap=(q*x['V_phi'])**2/(2*gap),relative_square_over_gap=(q*x['relative_v'])**2/(2*gap))
    heads['maximum_linear_amplitude']=max(abs(x[k]) for k in ('Phi','Psi','clock_d','n_U'))
    heads['maximum_linear_amplitude']=max(heads['maximum_linear_amplitude'],abs(heads['phase_velocity']),abs(heads['U_tilt']),abs(heads['relative_velocity']))
    return heads,dict(phase_rate=heads['phase_rate_fraction']<1,amplitude=heads['maximum_linear_amplitude']<D('.01'),relative_velocity=abs(heads['relative_velocity'])<D('.01'))

def main():
    start=time.monotonic();source=sha(__file__)
    require(not list(BASE.glob(STEM+'_*')),'Existing prefix preserved; no overwrite/resume')
    p,r,bad=authenticate();combined=[];basis=[]
    linear=('Phi','Psi','n_U','relative_v','clock_d','V_phi','pi_U','sigma','Ptot','Z','delta_rho_clock','delta_rho_polarization','delta_rho_total','delta_pressure','linear_H1')
    expected=[(length,t,omega) for length in (.1,1.,10.,100.) for t in (1.,10.,100.,1000.) for omega in (.1,1.,10.,100.)]
    for i,(length,t,omega) in enumerate(expected):
        a,b=p['rows'][2*i:2*i+2];point=p['modal_points'][i]
        require([(z['point'],z['source_basis'],z['length_kpc'],z['e_fold_Myr'],z['omega_over_Hstar']) for z in (a,b)]==[(i,k,length,t,omega) for k in (0,1)],'Ordered128 rows')
        require(a['displayed_inputs']|{'Phi':'0.0','Psi':'0.0'}==b['displayed_inputs']|{'Phi':'0.0','Psi':'0.0'},'Paired displayed inputs')
        require(a['displayed_background']==b['displayed_background'],'Paired background')
        bg={k:D(v) for k,v in a['displayed_background'].items()};inp={k:D(v) for k,v in a['displayed_inputs'].items()}
        q,lam,F,K,V=(inp[k] for k in ('q','lambda_over_Hstar','F','K','V'));w,s,Q=(bg[k] for k in ('w','cs','Q'))
        ar=D('1.98')*Q*Q/F+D('.02')*lam*lam
        nr=ar+D('.5')*D('1.98')*Q*Q/w*s*q*q*(D('1.98')+D('.02')/F);seff=s*ar/nr
        require(ar>0 and nr>0 and 0<seff<=s,'Positive algebraic factors')
        dec=[{k:D(z['decimal_response'][k]) for k in linear} for z in (a,b)]
        for k,z in enumerate(dec):
            U=q*q*z['Phi']-3*lam*lam*z['Psi'];actual=w*z['clock_d']-q*z['Ptot']
            close('basis_density_collapse',actual,-w*U/(lam*lam+seff*q*q))
            close('saved_total_density',actual,z['delta_rho_total'])
            close('saved_clock_density',w*z['clock_d'],z['delta_rho_clock'])
            close('saved_polarization_density',-q*z['Ptot'],z['delta_rho_polarization'])
            close('saved_pressure',s*w*z['clock_d'],z['delta_pressure'])
            basis.append(dict(point=i,source_basis=k,signed_response=(a,b)[k]['decimal_response'],sampled_flags=(a,b)[k]['sampled_linear_flags']))
        x={k:dec[0][k]+dec[1][k] for k in linear};require(x['Phi']==x['Psi']==D('1e-8'),'Fixed equal common source')
        density=w*x['clock_d']-q*x['Ptot'];close('common_density_collapse',density,-w*(q*q-3*lam*lam)*x['Phi']/(lam*lam+seff*q*q))
        close('common_density_sum',density,x['delta_rho_total'])
        mu=1+density/(q*q*x['Phi']);ceiling=w/(lam*lam)
        violation=max(D(0),-(1-mu),1-mu-ceiling) if q*q>=3*lam*lam else max(D(0),1-mu)
        CHECKS.append(dict(name='analytic_mu_bound',error=violation,tolerance=TOL,passed=violation<=TOL))
        force=q*x['n_U']+x['sigma'];dd=w/s;mb=D('.5');kb=D('.02');cc=D('1.98');phi=x['Phi'];psi=x['Psi']
        Ef=(dd*(lam*x['V_phi'])**2+w*(q*x['V_phi'])**2+mb*kb*q*q*(lam*x['pi_U'])**2+mb*cc*(K+V)*force*force)/2
        H2=Ef-(dd+mb*kb*q*q)*phi*phi/2-mb*cc*q*phi*x['Z']-3*w*phi*psi+bg['p0']*(3*phi*psi-D('1.5')*psi*psi)
        lapse=dd*(phi-lam*x['V_phi'])+3*bg['rho']*psi+q*x['Ptot'];spatial=-3*w*(lam*x['V_phi']-phi)+3*bg['p0']*(psi-phi)
        power=-lam*(phi*lapse+psi*spatial)
        close('common_lapse_vertex',lapse,-density+3*bg['rho']*psi)
        close('common_spatial_vertex',spatial,-3*x['delta_pressure']+3*bg['p0']*(psi-phi))
        close('common_inclusive_source_work',2*lam*H2,power,2*abs(lam*Ef)+abs(power)+abs(lam*(dd+mb*kb*q*q)*phi*phi)+2*abs(lam*mb*cc*q*phi*x['Z'])+6*abs(lam*w*phi*psi)+6*abs(lam*bg['p0']*phi*psi)+3*abs(lam*bg['p0']*psi*psi))
        heads,flags=diagnostics(x,bg,q)
        combined.append(dict(point=i,length_kpc=length,e_fold_Myr=t,omega_over_Hstar=omega,signed_response=x,
          independent_A=ar,independent_Nrho=nr,s_eff=seff,mu_normal=mu,Gresponse_over_GN=D('.99')/mu if mu else 'NOT_DEFINED',
          positive_feedback_ceiling=ceiling,Einstein_shortscale_omitted_term=3*bg['h']*(lam+bg['h'])/(q*q),H_over_lambda=bg['h']/lam,
          static_mu=cc/2*(1-1/(1+bg['ell_q']**2))-dd/(q*q),source_free_norm=Ef,inclusive_H2=H2,
          metric_vertices=dict(lapse=lapse,spatial=spatial),quadratic_source_power=power,domain_heads=heads,sampled_flags=flags))
    require(len(combined)==64 and len(basis)==128,'Complete output census')
    ranges={k:dict(min=min(z[k] for z in combined),max=max(z[k] for z in combined)) for k in ('mu_normal','Gresponse_over_GN','positive_feedback_ceiling','Einstein_shortscale_omitted_term','H_over_lambda','static_mu') if all(isinstance(z[k],Decimal) for z in combined)}
    status='SAVED_COMMON_RESPONSE_ARITHMETIC_PASS' if all(c['passed'] for c in CHECKS) else 'SAVED_COMMON_RESPONSE_ARITHMETIC_FAILED'
    result=dict(status=status,scope='Equal common-potential local constitutive readout; no actual field/halo/history',source_sha256=source,inputs=SEALS,
      arithmetic_scope='Decimal60 exact displayed-data strings',common_points=combined,original_source_bases=basis,ranges=ranges,
      checks=CHECKS,parent_gates=p['numerical_gates'],preserved_old18failures=bad,elapsed_seconds=time.monotonic()-start)
    rehash(source);rh=write(STEM+'_RESULT.json',result)
    lines=['# Common-potential saved readout V001','',status,f'{len(combined)} complete points; {len(basis)} signed source bases; {sum(c["passed"] for c in CHECKS)}/{len(CHECKS)} arithmetic checks.','',
      '| 1/k kpc | e-fold Myr | omega/Hstar | mu relative bare | .99/mu | ceiling | H/lambda | sampled flags |','|---|---|---|---|---|---|---|---|']
    for z in combined:lines.append('| '+ ' | '.join(str(z[k]) for k in ('length_kpc','e_fold_Myr','omega_over_Hstar','mu_normal','Gresponse_over_GN','positive_feedback_ceiling','H_over_lambda','sampled_flags'))+' |')
    lines+=['','All signed bases, mixed full-energy/source contacts and heads remain in JSON; all18 original failures remain unchanged.','This arithmetic does not solve the full conserved metric source or qualify a halo/incoming history.']
    rp=write(STEM+'_REPORT.md',('\n'.join(lines)+'\n').encode(),True);rehash(source)
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=source,inputs=SEALS,result_sha256=rh,report_sha256=rp,outputs=CREATED))
    rehash(source);print(json.dumps(dict(status=status,result_sha256=rh,points=64,checks=len(CHECKS))),flush=True)
    return 0 if status.endswith('_PASS') else 3
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root-owned explicit --execute only')
    try:
        with localcontext() as ctx:ctx.prec=60;raise SystemExit(main())
    except Exception as e:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_ERROR_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(e),source_sha256=sha(__file__),pid=os.getpid()))
        raise
