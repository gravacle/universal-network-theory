"""Independent saved-only standard-library audit; root executes after final freeze."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import sys
import time

BASE=Path(__file__).resolve().parent
PARENT='CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001'
STEM=PARENT+'_SAVED_AUDIT_V002'
PINS={
 'constrained_u_saved_audit_rounding_diagnostic_v002.py':'8106778733866ff3fde3472d96606161f8f7a590fb3cd86d1c0cda854a10ba27',
 'CONSTRAINED_U_SAVED_AUDIT_ROUNDING_DIAGNOSTIC_V002_RESULT.json':'861a2dfcb48e7a75b2db21122fe33e407e8056f26f9b0d1fea9f9ebe944b8ead',
 PARENT+'_SAVED_AUDIT_V002_PROTOCOL.md':'133eab52424de49b63cb2effff5c88fa65a51c2d315971c43d9c61894ee17278',
 'constrained_u_clock_gradient_flrw_saved_audit_v001.py':'ea9f88e8b5b971c41bc9888b2b726966359c26b0e169d49f3495c87c3740cd1a',
 PARENT+'_SAVED_AUDIT_V001_ERROR.json':'4707e7e220687bbeb4fcfadebb9886a3e3195d476c39431b1a13d5d0201fb6e9',
 PARENT+'_SAVED_AUDIT_V001_PROTOCOL.md':'ba9ac2b72916f3e989208920630cb0258b430530023a90367314a0ff73e7e5ea',
 'constrained_u_clock_gradient_flrw_response_v001.py':'0d4961fd3ef20e3994e452a23913cf5956491d027769d171ccc23f78e821378a',
 PARENT+'.md':'5d4a7abceca7f005ac9efd95bc2638ae94dd8eb8b0992ea80793193a079c55b2',
 PARENT+'_RESULT.json':'0fbbf7a2dc89231da78f31b76e3325bb62e502adfb34ff916c03e81bb5c653f3',
 PARENT+'_RECEIPT.json':'01c3effb4ea9a793ca2f2cb9e996f39e343cdacb6803258f6fa58f4bd89f3afc',
}
CASES=[(k,o) for k in (.01,.1) for o in (.1,1.,10.,100.)]
ARMS=[('COARSE',65536,48),('FINE',131072,48),('MODES',131072,96)]
SEED,KB,C,CBAR,EPS=1e-8,.02,1.98,.99,sys.float_info.epsilon
FLUID=['Phi','delta_b','Hstar_v_b','delta_rad','Hstar_v_rad','Hstar_pi_U','delta_n_clock_over_n','Hstar_V_phi','Ptot','Z','Z_dot','n_U','sigma']
PHYSICAL=['comoving_delta_b','comoving_baryon_density','comoving_rad_density','comoving_clock_density','polarization_density','Weyl','normal_acceleration']
COUNT,MAX_ERROR=0,0.


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()


def check(ok,name):
    global COUNT
    COUNT+=1
    if not ok:raise AssertionError(name)


def close(got,want,name,scale=0.,atol=2e-18):
    global MAX_ERROR
    check(math.isfinite(got) and math.isfinite(want),name+' finite')
    err=abs(got-want);MAX_ERROR=max(MAX_ERROR,err/(1+abs(want)))
    check(err<=atol+2e-11*abs(want)+4096*EPS*abs(scale),name+' arithmetic')


def same_array(got,want,name,scale=0.):
    check(len(got)==len(want),name+' length')
    for a,b in zip(got,want):close(a,b,name,scale)


def finite_tree(v):
    if isinstance(v,dict):
        for x in v.values():finite_tree(x)
    elif isinstance(v,list):
        for x in v:finite_tree(x)
    elif isinstance(v,(int,float)) and not isinstance(v,bool):check(math.isfinite(v),'finite saved value')


def write(suffix,obj):
    path=BASE/(STEM+suffix)
    with path.open('x') as f:
        json.dump(obj,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
    path.chmod(0o444);return sha(path)


def saved_background(row,fixed):
    a,S=row['a'],row['s'];eps=fixed['eps'];N=1/eps-math.log1p(1/eps)
    d=fixed['d0']/a**3;qb=math.sqrt(1+eps*S/(1+S));dq=eps/(2*qb*(1+S)**2)
    p=(math.log1p(S)-S/(1+S))/N;coef=1.5*fixed['OA']/fixed['rG']
    b=1.5*fixed['OB']/fixed['rG']/a**3;r=1.5*fixed['OR']/fixed['rG']/a**4
    w=coef*qb*d;rho=coef*(1+qb*d-p);h=math.sqrt(2*(b+r+rho)/3)
    den=2+(4+3*eps)*S+2*(1+eps)*S*S;c=eps*S/den
    Sd=-3*h*S*qb/(qb+S*dq);cd=2*eps*(1-(1+eps)*S*S)*Sd/den**2
    Q=fixed['Q0_over_Hstar']*qb;hd=-b-4*r/3-w
    vals=dict(h=h,b=b,r=r,w=w,rho=rho,cs=c,qbar=qb,h_dt=hd,cs_dt=cd,Q=Q,charge=d,
              charge_error=abs(2*qb*S/(eps*N)/d-1))
    for k,v in vals.items():close(row[k],v,'saved background '+k,abs(v))
    close(fixed['Q0_over_Hstar']*dq*Sd,-3*h*c*Q,'proper Q derivative',abs(3*h*c*Q))
    cdenv=2*eps*(1+(1+eps)*S*S)*abs(Sd)/den**2
    return dict(a=a,S=S,eps=eps,h=h,b=b,r=r,w=w,c=c,cd=cd,cd_env=cdenv,Q=Q,hd=hd,qb=qb)


def contraction(state,bg,q,omega,nodes,weights):
    phi,db,ub,dr,ur,pi,d,V,P=state[:9];ns=len(nodes)
    z=state[9:9+ns];zd=state[9+ns:];check(len(zd)==ns,'complete mode column')
    Z=math.fsum(t*v for t,v in zip(weights,z));Zd=math.fsum(t*v for t,v in zip(weights,zd))
    Zabs=math.fsum(abs(t*v) for t,v in zip(weights,z));Zdabs=math.fsum(abs(t*v) for t,v in zip(weights,zd))
    alpha=omega**2*math.fsum(t*s*s for t,s in zip(weights,nodes))
    R1=omega**2*math.fsum(t*s*s*v for t,s,v in zip(weights,nodes,z))
    h,b,r,w,c,cd,Q,hd=(bg[k] for k in ('h','b','r','w','c','cd','Q','hd'))
    mom=math.fsum([b*ub,4*r*ur/3,w*V]);phid=mom-h*phi
    n=(P-CBAR*Z)/(.5*KB*q);Vd=phi+c*(d+3*h*V);v=V-pi;vd=n+c*(d+3*h*V)
    Ah=h*(1+3*c);Ahd=hd*(1+3*c)+3*h*cd;L=Q*q;Ld=-Ah*L
    nd0=-h*n-(C/KB)*(Zd+2*h*Z)/q;dd0=3*phid-q*q*V
    vd0=math.fsum([nd0,cd*(d+3*h*V),c*dd0,3*c*hd*V,3*c*h*Vd])
    Cterms=[L*vd0,-2*Ah*L*vd,(Ah*Ah-Ahd)*L*v]
    Bq=1+(bg['ell']*q)**2;Mterms=[-3*h*Zd,-Bq*R1,alpha*q*n]
    C0,M0=math.fsum(Cterms),math.fsum(Mterms)
    Delta=alpha+C*Q*Q/KB+CBAR*Q*Q*q*q/(w/c)
    check(Delta>0,'positive reaction denominator')
    sigma=(C0-M0)/Delta
    # Positive operation envelopes are formed BEFORE cancellation; no field/gate changes.
    Nenv=(abs(P)+CBAR*Zabs)/(.5*KB*abs(q));Genv=abs(d)+3*abs(h*V)
    venv=abs(V)+abs(pi);vdenv=Nenv+abs(c)*Genv
    momenv=b*abs(ub)+4*r*abs(ur)/3+w*abs(V);phidenv=momenv+abs(h*phi)
    Vdenv=abs(phi)+abs(c)*Genv
    nd0env=abs(h)*Nenv+(C/KB)*(Zdabs+2*abs(h)*Zabs)/abs(q)
    dd0env=3*phidenv+q*q*abs(V)
    vd0env=nd0env+bg['cd_env']*Genv+abs(c)*dd0env+3*abs(c*hd*V)+3*abs(c*h)*Vdenv
    Ahdenv=abs(hd)*(1+3*abs(c))+3*abs(h)*bg['cd_env']
    C0env=abs(L)*vd0env+2*abs(Ah*L)*vdenv+(Ah*Ah+Ahdenv)*abs(L)*venv
    R1env=omega**2*math.fsum(abs(t*s*s*v) for t,s,v in zip(weights,nodes,z))
    M0env=3*abs(h)*Zdabs+Bq*R1env+alpha*abs(q)*Nenv
    sigscale=(C0env+M0env)/Delta+abs(sigma)
    fluid=state[:9]+[Z,Zd,n,sigma]
    physical=[db+3*h*ub,b*(db+3*h*ub),r*(dr+4*h*ur),w*(d+3*h*V),-q*P,2*phi,q*n]
    normal=[q*q*phi,3*h*mom,b*db,r*dr,w*d,-q*P]
    floor=q*q*SEED*1e-10;nden=max(math.fsum(abs(t) for t in normal),floor)
    ct=[Z,-L*v];cfloor=L*SEED*1e-10;cden=max(math.fsum(abs(t) for t in ct),cfloor)
    jt=[Zd,-Ld*v,-L*vd];jfloor=cfloor*max(h,Q,100.);jden=max(math.fsum(abs(t) for t in jt),jfloor)
    amp=[abs(phi),abs(db),abs(dr),abs(d),abs(q*ub),abs(q*ur),abs(q*V),abs(q*pi),abs(q*v),abs(n)]
    eps,S,qb=(bg[k] for k in ('eps','S','qb'))
    lower=eps*S/((1+S)*qb*(qb+1));upper=eps/((1+S)*qb*(math.sqrt(1+eps)+qb));gap=min(lower,upper)
    domain=[c*d,lower,upper,abs(c*d)/gap,q*V,q*pi,q*v,(q*v)**2/(2*gap)]
    NORMenv=q*q*abs(phi)+3*abs(h)*momenv+b*abs(db)+r*abs(dr)+w*abs(d)+abs(q*P)
    Cenv=Zabs+abs(L)*venv;Jenv=Zdabs+abs(Ld)*venv+abs(L)*vdenv
    amp_scales=[abs(phi),abs(db),abs(dr),abs(d),abs(q*ub),abs(q*ur),abs(q*V),abs(q*pi),abs(q)*venv,Nenv]
    physical_scales=[abs(db)+3*abs(h*ub),b*(abs(db)+3*abs(h*ub)),
        r*(abs(dr)+4*abs(h*ur)),w*Genv,abs(q*P),2*abs(phi),abs(q)*Nenv]
    domain_scales=[abs(c*d),lower,upper,abs(c*d)/gap,abs(q*V),abs(q*pi),abs(q)*venv,q*q*venv*venv/(2*gap)]
    # Instantaneous Ward contractions from the independently derived reaction.
    dd=dd0-CBAR*Q*q*sigma/w;Pd=-2*h*P-CBAR*Q*sigma
    ed=-3*h*(1+c)*w*d+w*dd;pol=-q*P;pold=h*q*P-q*Pd
    erhs=3*w*phid-w*q*q*V
    escale=math.fsum(abs(t) for t in [ed,pold,3*h*w*d,3*h*pol,3*h*c*w*d,erhs])
    close(ed+pold+3*h*(w*d+pol+c*w*d),erhs,'phase-polarization Ward',escale)
    close(-3*h*(1+c)*w*V+w*Vd+3*h*w*V,w*phi+c*w*d,'clock momentum Ward',abs(w*phi)+abs(c*w*d)+abs(3*h*w*V))
    momd=-3*h*mom+(b+4*r/3+w)*phi+r*dr/3+c*w*d
    bd=3*phid-q*q*ub;rd=4*phid-4*q*q*ur/3
    rhod=-3*h*b*db+b*bd-4*h*r*dr+r*rd+ed+pold
    R=math.fsum(normal);Rd=-2*h*q*q*phi+q*q*phid+3*hd*mom+3*h*momd+rhod
    close(Rd,-3*h*R,'normal Ward',abs(2*h*q*q*phi)+abs(q*q*phid)+abs(3*hd*mom)+abs(3*h*momd)+abs(rhod))
    return dict(fluid=fluid,physical=physical,normal_terms=normal,normal_floor=floor,normal_error=abs(R)/nden,
        constraint_terms=ct,constraint_floor=cfloor,constraint_error=abs(math.fsum(ct))/cden,
        first_jet_terms=jt,first_jet_floor=jfloor,first_jet_error=abs(math.fsum(jt))/jden,
        reaction_denominator=Delta,amplitudes=amp,physical_domain=domain,
        fluid_scales=[0.]*9+[Zabs,Zdabs,Nenv,sigscale],physical_scales=physical_scales,
        array_scales=dict(normal_terms=[NORMenv]*6,constraint_terms=[Cenv]*2,
            first_jet_terms=[Jenv]*3,amplitudes=amp_scales,physical_domain=domain_scales),
        residual_envelopes=dict(normal_error=NORMenv,constraint_error=Cenv,first_jet_error=Jenv))


def paired_ratio_scale(stored_terms,fresh_terms,stored_floor,fresh_floor,stored_ratio,fresh_ratio,envelope):
    # |a/d-b/e| <= (|a-b|+max(ratios)*|d-e|)/min(d,e).
    # max(sumabs,floor) is 1-Lipschitz. Both numerator and denominator vary.
    sd=max(math.fsum(abs(t) for t in stored_terms),stored_floor)
    fd=max(math.fsum(abs(t) for t in fresh_terms),fresh_floor)
    check(sd>0 and fd>0,'positive paired residual denominators')
    ratio=max(abs(stored_ratio),abs(fresh_ratio));floorenv=max(stored_floor,fresh_floor)
    return ((1+ratio)*envelope+ratio*floorenv)/min(sd,fd)


def audit():
    start=time.monotonic();source_sha=sha(__file__)
    check(not any(h.startswith('PENDING_') for h in PINS.values()),'final closure/protocol pins mandatory')
    for n,h in PINS.items():check(sha(BASE/n)==h,'direct seal '+n)
    prior=json.loads((BASE/(PARENT+'_SAVED_AUDIT_V001_ERROR.json')).read_text())
    check(prior==dict(assertions=822610,error='first_jet_error arithmetic',error_type='AssertionError',source_sha256=PINS['constrained_u_clock_gradient_flrw_saved_audit_v001.py'],status='AUDIT_ERROR_PRESERVED'),'preserved V001 failure identity')
    diagnosis=json.loads((BASE/'CONSTRAINED_U_SAVED_AUDIT_ROUNDING_DIAGNOSTIC_V002_RESULT.json').read_text())
    check(diagnosis['source_sha256']==PINS['constrained_u_saved_audit_rounding_diagnostic_v002.py'] and diagnosis['rows']==3120 and diagnosis['old_bound_failures']==4 and diagnosis['corrected_bound_failures']==0 and diagnosis['all_corrected_bounds_pass'] is True,'preserved saved diagnosis identity')
    raw=json.loads((BASE/(PARENT+'_RESULT.json')).read_text());rec=json.loads((BASE/(PARENT+'_RECEIPT.json')).read_text())
    man=json.loads((BASE/(PARENT+'_MANIFEST.json')).read_text());report=(BASE/(PARENT+'_REPORT.md')).read_text()
    check(set(raw)=={'manifest','trials','numerical_gates','status','all_numerical_gates_passed','physical_names','fluid_names','endpoints','endpoint_effect_refinements','physical_fixture_flags','elapsed_seconds','scope'},'exact result schema')
    check(set(rec)=={'checkpoint_seals','journal_sha256','lineage','manifest_sha256','report_sha256','result_sha256','status'},'exact receipt schema')
    check(set(man)=={'lineage','fixed','cases','trials','seeds','numpy_version','prospective_action','extra_native_remainder','radiation','physical_domain_scope'},'exact manifest schema')
    tree=ast.parse((BASE/'constrained_u_clock_gradient_flrw_response_v001.py').read_text())
    assignments={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    direct=ast.literal_eval(assignments['PINS']);direct[PARENT+'.md']=ast.literal_eval(assignments['PROTOCOL_SHA'])
    check(direct[PARENT+'.md']==PINS[PARENT+'.md'],'producer protocol identity')
    inputs={str((BASE/n).resolve()):h for n,h in direct.items()}
    for n,h in inputs.items():check(sha(n)==h,'declared input '+n)
    cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    check(len(cal['hashes'])==18,'calibration ledger census')
    for n,h in cal['hashes'].items():
        check(n not in inputs or inputs[n]==h,'no conflicting historical seal');check(sha(n)==h,'historical seal');inputs[n]=h
    lineage=dict(inputs=inputs,source_sha256=PINS['constrained_u_clock_gradient_flrw_response_v001.py'])
    check(raw['manifest']==man and man['lineage']==rec['lineage']==lineage,'all exact lineage')
    check(rec['result_sha256']==PINS[PARENT+'_RESULT.json'],'receipt result identity')
    seals=dict(inputs);seals.update({str((BASE/n).resolve()):h for n,h in PINS.items()})
    for suffix,key in [('_MANIFEST.json','manifest_sha256'),('_REPORT.md','report_sha256'),('_JOURNAL.jsonl','journal_sha256')]:
        path=BASE/(PARENT+suffix);check(sha(path)==rec[key],'final artifact seal');seals[str(path)]=rec[key]
    check(man['cases']==[list(t) for t in CASES] and man['trials']==[list(t) for t in ARMS],'fixed case/arm census')
    check(man['seeds']==['constraint_consistent_fixed_Phi_zero_velocity','constraint_consistent_zero_Phi_fixed_velocity'],'fixed basis-seed chart')
    check(man['extra_native_remainder']=='absent' and man['prospective_action']=='uncompressed cTheta0 constrained polarization replacement','action inventory')
    fixed=man['fixed'];owned=cal['fixed'];selected=cal['selected'];ctx=cal['trials'][-1]['atomic_invocation']['context']
    check(fixed['rG']==.98/.99 and fixed['old_rG']==.98 and fixed['new_Gcos_over_GN']==.99,'bare gravity conversion')
    check(fixed['OA']==owned['omega_A'] and fixed['OB']==selected['OB'] and fixed['OR']==ctx['OR'] and fixed['d0']==owned['d0'] and fixed['eps']==owned['eps'],'actual physical density budget')
    check(fixed['Hunit']==selected['Hunit'] and fixed['Q0_over_Hstar']==100. and fixed['ell_pc']==100. and fixed['seed']==SEED,'proper units and seed')
    check((fixed['KB'],fixed['C'],fixed['Mbar'],fixed['Cbar'])==(.02,1.98,.5,.99) and fixed['density_unit']=='rho_star=2 M_bare^2 Hstar^2' and fixed['time_unit']=='Hstar proper_time','source-coefficient units')
    close(fixed['L'],1e-4*fixed['Hunit']/299792.458,'proper ell conversion')
    check(raw['fluid_names']==FLUID and raw['physical_names']==PHYSICAL,'readout dictionary')
    check(len(raw['trials'])==3,'three retained arms');finite_tree(raw)
    expected=[]

    def gate(name,error,tolerance,**ids):expected.append(dict(name=name,error=error,tolerance=tolerance,**ids))

    snapshot_keys={'n','x','state','background','fluids','physical','normal_terms','normal_error','normal_floor','constraint_terms','constraint_error','constraint_floor','first_jet_terms','first_jet_error','first_jet_floor','reaction_denominator','amplitudes','physical_domain'}
    for trial,(label,steps,ns) in zip(raw['trials'],ARMS):
        check(set(trial)=={'label','steps','ns','snodes','weights','snapshots'},'exact trial schema')
        check((trial['label'],trial['steps'],trial['ns'])==(label,steps,ns),'arm identity')
        nodes,weights=trial['snodes'],trial['weights'];check(len(nodes)==len(weights)==ns,'full mode count')
        check(all(0<s<1 and w>0 for s,w in zip(nodes,weights)) and all(a<b for a,b in zip(nodes[:-1],nodes[1:])),'positive ordered quadrature')
        check([s['n'] for s in trial['snapshots']]==list(range(0,steps+1,steps//64)),'65 ordered snapshots')
        for snap in trial['snapshots']:
            check(set(snap)==snapshot_keys,'snapshot exact schema')
            x=math.log(.01)+snap['n']*(-math.log(.01)/steps);close(snap['x'],x,'snapshot coordinate',abs(x))
            close(snap['background']['a'],math.exp(x),'snapshot a')
            bg=saved_background(snap['background'],fixed);bg['ell']=fixed['L']
            check(len(snap['state'])==8 and all(len(cs)==2 for cs in snap['state']),'state case/seed axes')
            for key in ['fluids','physical','normal_terms','normal_error','constraint_terms','constraint_error','first_jet_terms','first_jet_error','amplitudes','physical_domain']:
                check(len(snap[key])==8 and all(len(r)==2 for r in snap[key]),'readout case/seed axes '+key)
            for key in ['normal_floor','constraint_floor','first_jet_floor','reaction_denominator']:
                check(len(snap[key])==8 and all(len(r)==1 for r in snap[key]),'shared case/one axes '+key)
            for ci,(k,omega) in enumerate(CASES):
                q=k*299792.458/fixed['Hunit']/bg['a']
                for seed in range(2):
                    state=snap['state'][ci][seed];check(len(state)==9+2*ns,'full retained state')
                    calc=contraction(state,bg,q,omega,nodes,weights)
                    for key in ['normal_terms','constraint_terms','first_jet_terms','amplitudes','physical_domain']:
                        got,want=snap[key][ci][seed],calc[key];check(len(got)==len(want),'complete '+key)
                        for a,b,env in zip(got,want,calc['array_scales'][key]):close(a,b,key,env)
                    check(len(snap['fluids'][ci][seed])==13,'full fluid/source row')
                    for j,(got,want) in enumerate(zip(snap['fluids'][ci][seed],calc['fluid'])):
                        close(got,want,'all13 fluids',calc['fluid_scales'][j])
                    check(len(snap['physical'][ci][seed])==7,'full physical row')
                    for a,b,env in zip(snap['physical'][ci][seed],calc['physical'],calc['physical_scales']):close(a,b,'all7 physical',env)
                    for key in ['normal_floor','constraint_floor','first_jet_floor','reaction_denominator']:
                        close(snap[key][ci][0],calc[key],key,abs(calc[key]))
                    for key,terms,floor in [('normal_error','normal_terms','normal_floor'),('constraint_error','constraint_terms','constraint_floor'),('first_jet_error','first_jet_terms','first_jet_floor')]:
                        got=snap[key][ci][seed]
                        scale=paired_ratio_scale(snap[terms][ci][seed],calc[terms],snap[floor][ci][0],calc[floor],got,calc[key],calc['residual_envelopes'][key])
                        close(got,calc[key],key,scale)
                    if snap['n']==0:
                        phi,V=(SEED,0.) if seed==0 else (0.,SEED/bg['h']);B=bg['b']+4*bg['r']/3+bg['w']
                        d=-q*q*phi/(B+.5*KB*q*q*bg['c'])-3*bg['h']*V;n=-bg['c']*(d+3*bg['h']*V)
                        same_array(state,[phi,d,V,4*d/3,V,V,d,V,.5*KB*q*n]+[0.]*(2*ns),'both exact seeds')
        gate('spectral_normalization',abs(sum(weights)-1),1e-13,trial=label)
        gate('charge_root',max(s['background']['charge_error'] for s in trial['snapshots']),1e-13,trial=label)
        for ci in range(8):
            for seed in range(2):
                for key,tol in [('normal_error',1e-6),('constraint_error',1e-7),('first_jet_error',1e-7)]:gate(key,max(s[key][ci][seed] for s in trial['snapshots']),tol,trial=label,case=ci,seed=seed)
    fine=raw['trials'][1]
    for arm,name in [(0,'time'),(2,'spectral')]:
        comp=raw['trials'][arm]
        for ci in range(8):
            for seed in range(2):
                for j,variable in enumerate(FLUID):
                    diff=max(abs(a['fluids'][ci][seed][j]-b['fluids'][ci][seed][j]) for a,b in zip(comp['snapshots'],fine['snapshots']))
                    denom=max(max(abs(s['fluids'][ci][seed][j]) for s in fine['snapshots']),1e-16)
                    gate(name+'_refinement',diff/denom,1e-4,case=ci,seed=seed,variable=variable)
    bg=fine['snapshots'][-1]['background'];S=bg['s'];eps=fixed['eps'];pex=(math.log1p(S)-S/(1+S))/(1/eps-math.log1p(1/eps))
    gate('fixed_inventory_H_identity',abs(bg['h']**2*fixed['rG']-(fixed['OA']*(1+bg['qbar']*bg['charge']-pex)+fixed['OB']+fixed['OR'])),1e-13)
    check(len(expected)==len(raw['numerical_gates'])==567,'all567 gates')
    for got,want in zip(raw['numerical_gates'],expected):
        check(set(got)==set(want)|{'passed'},'gate schema');check(all(got[k]==v for k,v in want.items() if k!='error'),'ordered gate identity')
        close(got['error'],want['error'],'frozen gate error',abs(want['error']))
        check(got['passed'] is (math.isfinite(got['error']) and got['error']<=got['tolerance']),'exact original disposition')
    failed=[g for g in raw['numerical_gates'] if not g['passed']];status='ARITHMETIC_FAILED' if failed else 'ARITHMETIC_PASS'
    check(raw['status']==rec['status']==status and raw['all_numerical_gates_passed']==(not failed),'failure status preserved')
    check(len(raw['endpoints'])==len(raw['endpoint_effect_refinements'])==len(raw['physical_fixture_flags'])==16,'full endpoint census')
    for ci,(k,omega) in enumerate(CASES):
        ref=ci//4*4
        for seed in range(2):
            ix=2*ci+seed;ep=raw['endpoints'][ix];fx=raw['endpoint_effect_refinements'][ix];flag=raw['physical_fixture_flags'][ix]
            check((ep['case'],ep['k_Mpc_inverse'],ep['omega_over_Hstar'],ep['seed'])==(ci,k,omega,seed),'endpoint identity')
            paired=[[a-b for a,b in zip(tr['snapshots'][-1]['physical'][ci][seed],tr['snapshots'][-1]['physical'][ref][seed])] for tr in raw['trials']]
            same_array(ep['physical'],fine['snapshots'][-1]['physical'][ci][seed],'endpoint physical');same_array(ep['difference_from_fixed_omega_point1'],paired[1],'signed reference difference')
            dt=[a-b for a,b in zip(paired[0],paired[1])];ds=[a-b for a,b in zip(paired[2],paired[1])];margin=[3*max(abs(a),abs(b)) for a,b in zip(dt,ds)]
            for key,val in [('coarse_effect',paired[0]),('fine_effect',paired[1]),('spectral_effect',paired[2]),('time_change',dt),('spectral_change',ds),('three_change_margin',margin)]:same_array(fx[key],val,'paired '+key)
            check((fx['case'],fx['seed'])==(ci,seed) and fx['reference']=='omega=.1 same k and seed, not mode-off/GR','reference scope')
            check(fx['resolution']==['reference_zero' if ci==ref else ('resolved' if abs(v)>m else 'unresolved') for v,m in zip(paired[1],margin)],'all signed resolution labels')
            amp=max(max(s['amplitudes'][ci][seed]) for s in fine['snapshots']);phase=max(s['physical_domain'][ci][seed][3] for s in fine['snapshots'])
            rel=max(abs(s['physical_domain'][ci][seed][6]) for s in fine['snapshots']);relsq=max(s['physical_domain'][ci][seed][7] for s in fine['snapshots'])
            for key,val in [('maximum_linear_amplitude',amp),('maximum_linear_phase_domain_fraction',phase),('maximum_relative_velocity',rel),('maximum_relative_square_over_phase_gap',relsq),('sampled_basis_amplitude_ceiling',min(.01*SEED/amp if amp else 1.,SEED/phase if phase else 1.))]:close(flag[key],val,'sampled '+key,abs(val))
            check((flag['case'],flag['seed'])==(ci,seed) and flag['small_perturbation']==(amp<.01) and flag['inside_linear_phase_domain']==(phase<1) and flag['small_relative_velocity']==(rel<.01),'physical flags preserved')
            val=ep['physical'];line=f'| {k} | {omega} | {seed} | {val[0]:.12g} | {val[5]:.12g} | {val[4]:.12g} |';check(line in report,'all16 report rows')
    events=[json.loads(s) for s in (BASE/(PARENT+'_JOURNAL.jsonl')).read_text().splitlines()]
    check(len(events)==42 and events[0]['event']=='OWNER_START' and events[-1]['event']=='OWNER_COMPLETE','exact42 owner journal')
    check(events[0]['owner']=='root' and events[0]['source_sha256']==lineage['source_sha256'],'root ownership')
    check(events[-1]['status']==status and events[-1]['result_sha256']==PINS[PARENT+'_RESULT.json'] and events[-1]['gates']==567 and events[-1]['passed']==567-len(failed),'completion journal')
    cpseals={};ei=1
    for tr,(_,steps,ns) in zip(raw['trials'],ARMS):
        for n in range(8192,steps+1,8192):
            stem=PARENT+'_'+tr['label']+'_CP_'+str(n).zfill(6);payload=BASE/(stem+'.json');commit=BASE/(stem+'_COMMIT.json')
            c=json.loads(commit.read_text());check(set(c)=={'lineage','steps','ns','payload','sha256'},'commit schema')
            check(c['lineage']==lineage and c['steps']==steps and c['ns']==ns and c['payload']==payload.name,'commit census/lineage')
            ph,ch=sha(payload),sha(commit);check(ph==c['sha256'],'committed payload seal');cpseals[str(payload)]=ph;cpseals[str(commit)]=ch
            ev=events[ei];ei+=1;check(ev['event']=='CHECKPOINT' and ev['trial']==tr['label'] and ev['n']==n and ev['payload']==payload.name and ev['sha256']==ph and ev['commit_sha256']==ch,'unique ordered checkpoint event')
            obj=json.loads(payload.read_text());check(set(obj)=={'lineage','steps','ns','n','state','snapshots'},'payload schema')
            count=n//(steps//64)+1;prefix=tr['snapshots'][:count]
            check(obj['lineage']==lineage and (obj['steps'],obj['ns'],obj['n'])==(steps,ns,n),'payload metadata')
            check(obj['snapshots']==prefix and obj['state']==prefix[-1]['state'],'full exact saved-state prefix')
    check(ei==41 and len(cpseals)==80 and rec['checkpoint_seals']==cpseals,'all40 CP pairs')
    check(set(str(p) for p in BASE.glob(PARENT+'_*_CP_*.json'))==set(cpseals),'no orphan/extra checkpoint')
    check(not list(BASE.glob(PARENT+'_FAILED_*')),'no exceptional parent error')
    check(f'Status {status}: {567-len(failed)}/567 numerical gates PASS.' in report,'report disposition')
    seals.update(cpseals)
    for p,h in seals.items():check(sha(p)==h,'prepublication saved seal')
    check(sha(__file__)==source_sha,'audit source seal')
    result=dict(preserved_attempt=dict(source_sha256=PINS['constrained_u_clock_gradient_flrw_saved_audit_v001.py'],error_sha256=PINS[PARENT+'_SAVED_AUDIT_V001_ERROR.json'],error=prior),operation_roundoff_scope='Unchanged 4096*EPS coefficient with pre-cancellation source/mean/reaction envelopes and paired quotient denominator propagation; not directed intervals or parent-gate changes.',status='SAVED_ONLY_ARITHMETIC_ACCEPTED',assertions=COUNT,max_normalized_discrepancy=MAX_ERROR,inputs=seals,source_sha256=source_sha,parent_status=status,parent_numerically_qualified=not failed,parent_numerical_failures=failed,parent_numerical_gates=567,sampled_physical_flags=raw['physical_fixture_flags'],endpoint_effects=raw['endpoint_effect_refinements'],scope='Independent instantaneous saved-state arithmetic; no trajectory/root solve, producer import, failure promotion, primordial/observational or nonlinear-domain qualification.')
    rh=write('_RESULT.json',result);rp=BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:f.write('# Constrained-U saved-only audit V002\n\n'+str(COUNT)+' arithmetic/metadata checks PASS; parent '+status+', '+str(len(failed))+' original failed gates retained.\n\nV001 audit source/error remain sealed; its first-jet comparison failure is preserved. V002 uses pre-cancellation operation envelopes with the same4096*EPS/2e-11/2e-18 constants. All16 channels,195 snapshots,567 gates and40 checkpoint pairs authenticated. Independent (C0-M0)/Delta reaction, instantaneous Ward transfers, both seed constraints and complete source/readout/refinement/flag arithmetic checked. No trajectory, charge solve, producer import or observational/nonlinear qualification.\n')
    rp.chmod(0o444);write('_RECEIPT.json',dict(result_sha256=rh,report_sha256=sha(rp),source_sha256=source_sha,inputs=seals,assertions=COUNT,pid=os.getpid(),elapsed_seconds=time.monotonic()-start,finished=datetime.now(timezone.utc).isoformat()))
    if sha(__file__)!=source_sha or any(sha(p)!=h for p,h in seals.items()):raise ValueError('Postpublication seal changed; preserve outputs')
    print(json.dumps(dict(status=result['status'],assertions=COUNT,parent_status=status,parent_failed=len(failed),result_sha256=rh)))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:ap.error('Root-owned --execute required')
    if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json','_ERROR.json')):raise SystemExit('Existing audit files preserved; no replay/overwrite')
    try:audit()
    except Exception as error:
        write('_ERROR.json',dict(status='AUDIT_ERROR_PRESERVED',assertions=COUNT,error_type=type(error).__name__,error=str(error),source_sha256=sha(__file__)))
        raise
