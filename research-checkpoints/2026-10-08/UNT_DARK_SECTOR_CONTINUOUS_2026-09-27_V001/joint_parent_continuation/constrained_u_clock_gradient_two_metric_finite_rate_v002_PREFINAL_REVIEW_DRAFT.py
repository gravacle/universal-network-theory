"""NEW externally forced H=0 two-metric discriminator. Root alone executes."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,time
import numpy as np
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V002'
PROTOCOL_SHA='07b6ec81051782f823a2b18f8709df364ec8a74a7748ded48a1de8beba28f9df'
PINS={'INVARIANT_CLOCK_GRADIENT_CONSTRAINED_U_REDUCED_CHART_AND_RETARDED_RESPONSE_V001.md': '0a15eee6701a4a9230202141422e428e772d57dbfb395a386721f8ea289e0a54', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'constrained_u_clock_gradient_flrw_reduced_chart_v002.py': '6d9878bb854bc7147aefcdcd358c6cecd16087a9577960f10686f5c4d17094b9', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md': '5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002_RESULT.json': '2b80278ce64b89ff21397b466bbbf9a01967501c715e50797cb0168efd8ed8d4', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002_RECEIPT.json': '78508ce15a2c342d5031e4974c1573bb1e912ef2e9f4492853f0abe2d7077615', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001_RESULT.json': '0fbbf7a2dc89231da78f31b76e3325bb62e502adfb34ff916c03e81bb5c653f3', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001_RECEIPT.json': '01c3effb4ea9a793ca2f2cb9e996f39e343cdacb6803258f6fa58f4bd89f3afc', 'constrained_u_clock_gradient_two_metric_finite_rate_v001.py': '2603bbe9fcb716c64ed081cf7e69bf30e7675ce10f5523611910682d492fc0f7', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V001.md': 'dc7d7ed26c1f96f23cd3ebd1f74ff4790f6e20fca84c14648f5d571e73c454d4', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V001_RESULT.json': '5561bee978a98ebbaa9af8fd83e0c965f0e24a9abf0ee1a68c6f6e48ba4a3574', 'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V001_RECEIPT.json': '5b81b98a72306ae5552526fa552865e988917046f75ed49b8d2a9022a58fb492'}
LENGTHS=(.1,1.,10.,100.)
TIMES=(1.,10.,100.,1000.)
OMEGAS=(.1,1.,10.,100.)
SEED,KB,C,MBAR=1e-8,.02,1.98,.5
CP_KMS,MPC_M,YEAR_S=299792.458,3.0856775814913673e22,365.25*86400
CREATED={}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(name,obj):
    p=BASE/name
    with p.open('x') as f:json.dump(obj,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
    p.chmod(0o444);CREATED[str(p)]=sha(p);return CREATED[str(p)]
def journal(event,**kw):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(json.dumps(dict(event=event,time=now(),**kw),sort_keys=True)+'\n')
def integral(A,B):
    r=B/A
    if r<=.125:
        terms=[(-r)**j/(j+2)/A for j in range(40)]
        F=math.fsum(terms);K=math.fsum((j+1)*x for j,x in enumerate(terms))
        V=math.fsum(-j*x for j,x in enumerate(terms))
    else:
        lg=math.log1p(r)
        F=(B-A*lg)/(B*B)
        K=A*(lg-B/(A+B))/(B*B)
        V=F-K
    return F,K,V

def decimal_number(x):
    return Decimal(str(x))
def float_tree(x):
    if isinstance(x,Decimal):return float(x)
    if isinstance(x,dict):return {k:float_tree(v) for k,v in x.items()}
    if isinstance(x,list):return [float_tree(v) for v in x]
    return x
def decimal_tree(x):
    if isinstance(x,Decimal):return str(x)
    if isinstance(x,dict):return {k:decimal_tree(v) for k,v in x.items()}
    if isinstance(x,list):return [decimal_tree(v) for v in x]
    return x

def response(q,lam,om,F,K,V,bg,phi,psi):
    q,lam,om,F,K,V,phi,psi=map(decimal_number,(q,lam,om,F,K,V,phi,psi))
    bg={k:decimal_number(v) for k,v in bg.items()}
    mb,kb,cc,seed=map(decimal_number,(MBAR,KB,C,SEED))
    w,s,Q,p0,rho=(bg[k] for k in ('w','cs','Q','p0','rho'))
    D=w/s;gamma=mb*cc*Q*Q/w;U=q*q*phi-3*lam*lam*psi
    ar=cc*Q*Q/F+kb*lam*lam;tr=cc*Q*(lam+Q/F)
    Dp=ar*(lam*lam+s*q*q)+gamma*s*q*q*lam*lam*(cc+kb/F)
    n=s*tr*U/Dp;v=s*(cc*Q-kb*lam)*U/Dp;d=-ar*U/Dp
    vf=(phi+s*d)/lam;pi=(phi-n)/lam
    sigma=-s*Q*q*lam*(cc+kb/F)*U/Dp
    P=mb*q*s*cc*Q*Q*(cc+kb/F)*U/Dp;Z=Q*q*v
    force=q*n+sigma;kin=K*force*force;pot=V*force*force
    Ef=(D*(lam*vf)**2+w*(q*vf)**2+mb*kb*q*q*(lam*pi)**2+mb*cc*(kin+pot))/2
    Efcompact=(D*(lam*vf)**2+w*(q*vf)**2+mb*kb*q*q*(lam*pi)**2+mb*cc*Q*Q*q*q*v*v/F)/2
    H2=Ef-(D+mb*kb*q*q)*phi*phi/2-mb*cc*q*phi*Z-3*w*phi*psi+p0*(3*phi*psi-Decimal('1.5')*psi*psi)
    Lphi=D*(phi-lam*vf)+3*(w-p0)*psi+mb*kb*q*q*n+mb*cc*q*Z
    Lpsi=-3*w*(lam*vf-phi)+3*p0*(psi-phi)
    work=-lam*(phi*Lphi+psi*Lpsi);H1=rho*phi+3*p0*psi
    eqs={
      'phase_kinematic':[lam*vf,-phi,-s*d],
      'relative_kinematic':[lam*v,-n,-s*d],
      'clock_current':[lam*d,-3*lam*psi,q*q*vf,mb*cc*Q*q*sigma/w],
      'modal_collective':[Z,-F*force],
      'holonomic':[Z,-Q*q*v],
      'normal_current':[lam*P,mb*cc*Q*sigma],
      'maxwell_source':[P,-mb*q*kb*n,-mb*cc*Z],
      'inclusive_source_work':[-lam*phi*D*(phi-lam*vf),-3*lam*phi*(w-p0)*psi,
        -lam*phi*mb*kb*q*q*n,-lam*phi*mb*cc*q*Z,
        3*lam*psi*w*(lam*vf-phi),-3*lam*psi*p0*(psi-phi),
        -2*lam*Ef,lam*(D+mb*kb*q*q)*phi*phi,2*lam*mb*cc*q*phi*Z,
        6*lam*w*phi*psi,-6*lam*p0*phi*psi,3*lam*p0*psi*psi],
      'free_norm_modal_identity':[Ef,-Efcompact],
      'lapse_contact_identity':[Lphi,w*d,-q*P,-3*rho*psi],
      'pressure_identity':[s*w*d,-w*(lam*vf-phi)],
    }
    lower,upper=(bg[k] for k in ('lower_gap','upper_gap'));gap=min(lower,upper)
    heads=dict(linear_phase_rate=s*d,phase_gap_lower=lower,phase_gap_upper=upper,
      phase_rate_fraction=abs(s*d)/gap,phase_velocity=q*vf,U_tilt=q*pi,relative_velocity=q*v,
      phase_square_over_gap=(q*vf)**2/(2*gap),relative_square_over_gap=(q*v)**2/(2*gap),
      maximum_linear_amplitude=max(abs(phi),abs(psi),abs(d),abs(n),abs(q*vf),abs(q*pi),abs(q*v)))
    static=dict(n=phi,d=-phi/s,v=phi/(Q*(1+bg['ell_q']**2)),
                P=mb*q*(kb+cc/(1+bg['ell_q']**2))*phi)
    return dict(Phi=phi,Psi=psi,U=U,Dp=Dp,n_U=n,relative_v=v,clock_d=d,V_phi=vf,pi_U=pi,
      sigma=sigma,Ptot=P,Z=Z,modal_force=force,modal_kinetic=kin,modal_potential=pot,
      delta_rho_clock=w*d,delta_rho_polarization=-q*P,delta_rho_total=w*d-q*P,
      delta_pressure=s*w*d,normal_acceleration=q*n,
      source_free_quadratic_norm=Ef,inclusive_quadratic_H2=H2,
      background_clock_energy=rho,background_clock_pressure=p0,linear_H1=H1,
      quadratic_source_power=work,linear_source_power=lam*H1,
      quadratic_metric_vertices=dict(lapse=Lphi,spatial=Lpsi),
      static_lapse_limit=static,signed_difference_from_static={k:x-static[k] for k,x in [('n',n),('d',d),('v',v),('P',P)]},
      signed_per_unit_source={k:x/seed for k,x in [('n_U',n),('relative_v',v),('clock_d',d),('sigma',sigma),('Ptot',P),('delta_rho_total',w*d-q*P),('delta_pressure',s*w*d)]},
      domain_heads=heads,sampled_linear_flags=dict(phase_rate=heads['phase_rate_fraction']<1,
        amplitude=heads['maximum_linear_amplitude']<Decimal('.01'),relative_velocity=abs(q*v)<Decimal('.01')),
      equation_terms=eqs)

def main():
    start=time.monotonic();source=sha(__file__)
    if (any((BASE/(STEM+x)).exists() for x in ('_RESULT.json','_REPORT.md','_RECEIPT.json','_MANIFEST.json','_JOURNAL.jsonl'))
        or list(BASE.glob(STEM+'_CP_*')) or list(BASE.glob(STEM+'_ERROR_*'))):
        raise RuntimeError('Existing output/prefix preserved; no replay/resume/overwrite')
    inputs={str((BASE/n).resolve()):h for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items()}
    for p,h in inputs.items():
        if sha(p)!=h:raise RuntimeError('Direct input seal mismatch '+p)
    cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    for p,h in cal['hashes'].items():
        if p in inputs and inputs[p]!=h:raise RuntimeError('Conflicting historical seal')
        if sha(p)!=h:raise RuntimeError('Historical seal mismatch '+p)
        inputs[p]=h
    old=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_RESPONSE_V001_RESULT.json').read_text())
    new=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002_RESULT.json').read_text())
    if old['status']!='ARITHMETIC_FAILED' or new['status']!='ARITHMETIC_PASS':raise RuntimeError('Parent status provenance mismatch')
    oldfinite=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_TWO_METRIC_FINITE_RATE_V001_RESULT.json').read_text())
    oldfailed=[g for g in oldfinite['numerical_gates'] if not g['passed']]
    if (oldfinite['status']!='ARITHMETIC_FAILED' or len(oldfailed)!=18
        or sum(g['name']=='pressure_identity' for g in oldfailed)!=15
        or sum(g['name']=='lapse_contact_identity' for g in oldfailed)!=3):
        raise RuntimeError('Original finite-rate failed controls provenance mismatch')
    fixed=old['manifest']['fixed'];saved=old['trials'][1]['snapshots'][-1]['background']
    if saved['a']!=1 or fixed['rG']!=.98/.99 or fixed['KB']!=KB or fixed['C']!=C:raise RuntimeError('Fixed present/source state mismatch')
    sel,owned=cal['selected'],cal['fixed'];ctx=cal['trials'][-1]['atomic_invocation']['context']
    if any(fixed[k]!=v for k,v in {'Hunit':sel['Hunit'],'OA':owned['omega_A'],'OB':sel['OB'],'OR':ctx['OR'],'d0':owned['d0'],'eps':owned['eps'],'Q0_over_Hstar':100.}.items()):raise RuntimeError('Physical calibration identity mismatch')
    eps,S=fixed['eps'],saved['s'];norm=1/eps-math.log1p(1/eps);qb=math.sqrt(1+eps*S/(1+S))
    pex=(math.log1p(S)-S/(1+S))/norm;coef=1.5*fixed['OA']/fixed['rG'];d0=fixed['d0']
    bg=dict(b=1.5*fixed['OB']/fixed['rG'],r=1.5*fixed['OR']/fixed['rG'],
      w=coef*qb*d0,rho=coef*(1+qb*d0-pex),cs=eps*S/(2+(4+3*eps)*S+2*(1+eps)*S*S),Q=100*qb)
    bg['h']=math.sqrt(2*(bg['b']+bg['r']+bg['rho'])/3);bg['p0']=bg['w']-bg['rho']
    bg.update(lower_gap=eps*S/((1+S)*qb*(qb+1)),upper_gap=eps/((1+S)*qb*(math.sqrt(1+eps)+qb)))
    gates=[]
    def check(name,error,tol,**ids):
        gates.append(dict(name=name,error=float(error),tolerance=tol,passed=bool(math.isfinite(error) and error<=tol),**ids))
    for key in ('b','r','w','rho','cs','Q','h'):check('present_'+key,abs(bg[key]-saved[key])/max(abs(bg[key]),1e-30),1e-13)
    check('present_charge_relation',abs(2*qb*S/(eps*norm)/d0-1),1e-13)
    quadratures={}
    for order in (64,128):
        nodes,weights=np.polynomial.legendre.leggauss(order);s=(nodes+1)/2;w=weights*(nodes+1)/2
        quadratures[order]=(s,w);check('mode_measure',abs(float(sum(w))-1),1e-13,order=order)
    manifest=dict(source_sha256=source,inputs=inputs,fixed=fixed,present_background=bg,
      inverse_wavenumber_lengths_kpc=LENGTHS,e_fold_times_Myr=TIMES,omega_over_Hstar=OMEGAS,
      source_bases=[[SEED,0],[0,SEED]],point_count=64,row_count=128,
      units=dict(density='rho_star=2Mbare^2 Hstar^2',time='Hstar proper_time',Mpc_m=MPC_M,year_seconds=YEAR_S),
      scope='Externally forced zero-incoming local H=0 quadratic sector, not self-gravity/FLRW/merger',
      original_status=old['status'],reduced_status=new['status'],numpy_version=np.__version__,
      response_arithmetic='Decimal60 from exact displayed float strings, before cast',
      old_finite_rate_status=oldfinite['status'],old_finite_rate_failed_controls=18)
    mh=write(STEM+'_MANIFEST.json',manifest);journal('OWNER_START',owner='root',pid=os.getpid(),source_sha256=source)
    rows,points=[],[];Hsi=fixed['Hunit']*1000/MPC_M
    for li,length in enumerate(LENGTHS):
        group=[];gstart=len(gates)
        q=CP_KMS/(fixed['Hunit']*length*.001);local=dict(bg,ell_q=.1/length)
        B=1+local['ell_q']**2
        for ti,tmyr in enumerate(TIMES):
            lam=1/(Hsi*tmyr*1e6*YEAR_S)
            for oi,om in enumerate(OMEGAS):
                A=(lam/om)**2;F,K,V=integral(A,B);pid=(li*4+ti)*4+oi
                for order,(s,w) in quadratures.items():
                    den=A+B*s*s
                    vals=[float(np.dot(w,s*s/den)),float(np.dot(w,A*s*s/(den*den))),float(np.dot(w,B*s**4/(den*den)))]
                    for name,got,want in zip(('F','kinetic','potential'),vals,(F,K,V)):
                        check('modal_integral_'+name,abs(got-want)/want,1e-10,point=pid,order=order)
                check('modal_partition',abs(K+V-F)/F,1e-13,point=pid)
                check('positive_modal_integrals',0 if min(F,K,V)>0 else 1,0,point=pid)
                bound=min(1/B,1/(2*A));check('modal_upper_bound',max(0,F-bound)/bound,1e-13,point=pid)
                point=dict(point=pid,length_kpc=length,e_fold_Myr=tmyr,omega_over_Hstar=om,q=q,lambda_over_Hstar=lam,
                  F=F,kinetic_integral=K,potential_integral=V,static_F=1/B,modal_response_fraction=B*F,
                  frozen_background_H_over_lambda=bg['h']/lam,frozen_background_ratio_below_point1=bg['h']/lam<.1)
                points.append(point)
                for seed,(phi,psi) in enumerate(((SEED,0),(0,SEED))):
                    exact=response(q,lam,om,F,K,V,local,phi,psi)
                    if seed==0:check('positive_response_denominator',0 if exact['Dp']>0 else 1,0,point=pid)
                    for name,terms in exact['equation_terms'].items():
                        residual=abs(sum(terms,Decimal(0)))
                        denominator=max(sum((abs(x) for x in terms),Decimal(0)),Decimal('1e-30'))
                        check(name,residual/denominator,2e-11,point=pid,source_basis=seed)
                    row=float_tree(exact)
                    row['decimal_response']=decimal_tree(exact)
                    row['displayed_inputs']={k:str(v) for k,v in dict(q=q,lambda_over_Hstar=lam,omega_over_Hstar=om,F=F,K=K,V=V,Phi=phi,Psi=psi).items()}
                    row['displayed_background']={k:str(v) for k,v in local.items()}
                    row.update(point=pid,source_basis=seed,length_kpc=length,e_fold_Myr=tmyr,omega_over_Hstar=om)
                    rows.append(row);group.append(row)
        name=STEM+'_CP_'+str(li).zfill(2)+'.json';seal=write(name,dict(length_index=li,length_kpc=length,source_sha256=source,inputs=inputs,rows=group,gates=gates[gstart:]))
        ch=write(STEM+'_CP_'+str(li).zfill(2)+'_COMMIT.json',dict(payload=name,sha256=seal,source_sha256=source,length_index=li))
        journal('CHECKPOINT',length_index=li,payload=name,sha256=seal,commit_sha256=ch)
    if len(rows)!=128 or len(points)!=64 or len(gates)!=2058:raise RuntimeError('Frozen row/point/gate census mismatch')
    def rehash():
        for p,h in dict(inputs,**CREATED).items():
            if sha(p)!=h:raise RuntimeError('Sealed bytes changed '+p)
        if sha(__file__)!=source:raise RuntimeError('Source bytes changed')
    rehash();status='ARITHMETIC_PASS' if all(g['passed'] for g in gates) else 'ARITHMETIC_FAILED'
    result=dict(status=status,manifest=manifest,rows=rows,modal_points=points,numerical_gates=gates,
      all_numerical_gates_passed=status=='ARITHMETIC_PASS',preserved_old_failed_controls=oldfailed,
      arithmetic_scope=manifest['response_arithmetic'],elapsed_seconds=time.monotonic()-start)
    rh=write(STEM+'_RESULT.json',result)
    lines=['# TWO-metric finite-rate constrained response V002','',f'{status}: {sum(g["passed"] for g in gates)}/2058 controls PASS.',
      'Externally forced H=0 local quadratic sector; no actual merger/FLRW/self-gravitating field prediction.','',
      '| 1/k kpc | e-fold Myr | omega/Hstar | source | n/source | density/source | modal/static F |','|---|---|---|---|---|---|---|']
    for row in rows:
        point=points[row['point']];g=row['signed_per_unit_source']
        lines.append(f'| {row["length_kpc"]} | {row["e_fold_Myr"]} | {row["omega_over_Hstar"]} | {"Phi" if row["source_basis"]==0 else "Psi"} | {g["n_U"]:.10g} | {g["delta_rho_total"]:.10g} | {point["modal_response_fraction"]:.10g} |')
    lines+=['','All signed rows and failures retained. Efree is a source-free norm; H2 and source work retain actual metric contacts.',
      'Static lapse comparison includes Maxwell and charge loading; Psi static response is zero, with no zero-denominator ratio.',
      'All18 original V001 failed controls remain sealed; Decimal60 response/contact arithmetic is evaluated before rounded float readouts.']
    rp=BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:f.write('\n'.join(lines)+'\n')
    rp.chmod(0o444);report_sha=sha(rp);rehash()
    journal('OWNER_COMPLETE',status=status,result_sha256=rh,gates=len(gates),passed=sum(g['passed'] for g in gates))
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=source,inputs=inputs,result_sha256=rh,report_sha256=report_sha,manifest_sha256=mh,
      journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),checkpoint_seals={p:h for p,h in CREATED.items() if '_CP_' in p}))
    print(json.dumps(dict(status=status,passed=sum(g['passed'] for g in gates),total=len(gates),elapsed_seconds=result['elapsed_seconds'],result_sha256=rh)),flush=True)
    return 0 if status=='ARITHMETIC_PASS' else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root-owned explicit --execute required')
    try:
        with localcontext() as context:
            context.prec=60
            raise SystemExit(main())
    except Exception as e:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_ERROR_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(e),source_sha256=sha(__file__),pid=os.getpid(),time=now()))
        raise
