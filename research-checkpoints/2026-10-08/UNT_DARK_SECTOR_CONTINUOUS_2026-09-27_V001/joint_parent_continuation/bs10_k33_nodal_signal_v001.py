#!/usr/bin/env python3
"""New saved-state whole-node response recurrence; no old producer/propagator."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import gc,hashlib,importlib.util,json,math,os,resource,socket,sys,time,traceback
from pathlib import Path

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=J/'BS10_K33_NODAL_SIGNAL_V001.md';SOURCE=J/'bs10_k33_nodal_signal_v001.py'
RESULT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.json';REPORT=J/'BS10_K33_NODAL_SIGNAL_V001_RESULT.md'
CP=J/'bs10_k33_nodal_signal_v001_checkpoints'
OLD_SOURCE=J/'bs10_k33_unclamped_formation_v001.py'
OLD_PROTOCOL=J/'BS10_K33_UNCLAMPED_FORMATION_V001.md'
OLD_RESULT=J/'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.json'
OLD_REPORT=J/'BS10_K33_UNCLAMPED_FORMATION_V001_RESULT.md'
OLD_CP=J/'bs10_k33_unclamped_formation_v001_checkpoints'
ANCHORS={str(OLD_SOURCE):'2a6d6326592dee5fb04ba47776ea495df68c0acdf7dce22f26f4be0eae0a1b6c',str(OLD_PROTOCOL):'8391edb0b3ac88268605f30d6e9589c05871fd570f48bee18ae845fcaec060c6',str(OLD_RESULT):'21bf1c0abaf548364665aee7d5e4559f3a0457899fcb25f3f7e35cc52d7c317b',str(OLD_REPORT):'7b3227c19e810aa0f588817e066eaa16665e153f8f99d013fc437c0df7f7cb5f'}
GS=(0.,.1);STARTS=(0,413);AGES=(0.,5.,20.,50.);DELAYS=(0.,.1,.5,1.,2.,5.)
FD_STEP=1e-4;FD_DELAYS=(.1-FD_STEP,.1+FD_STEP)
DEGREE=192;FFT_N=2048;TAYLOR_DEGREE=80;CENTER=16.25;KICK=1e-5
ENV_KEYS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','PYTHONDONTWRITEBYTECODE')

def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def exclusive(p,o):
    with p.open('x',encoding='utf-8') as f:json.dump(o,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def event(kind,**values):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(dict(event=kind,pid=os.getpid(),utc=utc(),**values),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def rss():return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
def check(c,name,ok,e=None):c.append(dict(name=name,passed=bool(ok),**({} if e is None else {'evidence':e})))
def close(np,c,name,a,b,tol=3e-8):
    err=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));lim=tol*max(1.,float(np.max(np.abs(a))),float(np.max(np.abs(b))))
    check(c,name,err<=lim,dict(error=err,tolerance=lim))
def canonical(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def authenticate():
    paths={str(PROTOCOL):sha(PROTOCOL),str(SOURCE):sha(SOURCE)}
    for p,h in ANCHORS.items():
        if sha(Path(p))!=h:raise RuntimeError('Sealed K3 anchor changed: '+p)
        paths[p]=h
    receipt=json.loads(OLD_RESULT.read_text())
    if receipt['status']!='QUALIFIED_ARITHMETIC' or receipt['failed_count']:raise RuntimeError('Original native receipt unqualified')
    for p,h in receipt['input_sha256'].items():
        if sha(Path(p))!=h:raise RuntimeError('Original input changed: '+p)
        paths[p]=h
    events=[json.loads(s) for s in (OLD_CP/'events.jsonl').read_text().splitlines() if s]
    old_manifest=json.loads((OLD_CP/'manifest.json').read_text())
    if old_manifest['input_sha256']!=receipt['input_sha256'] or old_manifest['inputs']!=receipt['inputs']:raise RuntimeError('Original manifest/receipt inputs mismatch')
    for p in (OLD_CP/'manifest.json',OLD_CP/'events.jsonl'):paths[str(p)]=sha(p)
    groups=[]
    for gi,g in enumerate(GS):
        h=next(x for x in receipt['Hamiltonians'] if x['g']==g);hp=OLD_CP/f'g{gi}.json'
        if json.loads(hp.read_text())!=h or not any(e.get('event')=='Hamiltonian_complete' and e.get('key')==f'g{gi}' and e.get('sha256')==sha(hp) and e.get('failed')==0 for e in events):raise RuntimeError('Original Hamiltonian seal mismatch')
        paths[str(hp)]=sha(hp);selected=[]
        for n in STARTS:
            for age in AGES:
                row=next(x for x in h['states'] if x['start']==n and x['tau']==age and not x['auxiliary_early_arm'])
                key=f'g{gi}_n{n}_'+row['time_key'];rp=OLD_CP/(key+'.json');bp=Path(row['bundle_path'])
                if row['failed_count'] or json.loads(rp.read_text())!=row or row['input_sha256']!=receipt['input_sha256']:raise RuntimeError('Original selected state metadata mismatch')
                if not any(e.get('event')=='state_complete' and e.get('key')==key and e.get('sha256')==sha(rp) and e.get('failed')==0 for e in events):raise RuntimeError('Original selected state journal mismatch')
                if sha(bp)!=row['bundle_sha256'] or not any(e.get('event')=='bundle_saved' and e.get('key')==f'g{gi}_n{n}' and e.get('sha256')==row['bundle_sha256'] for e in events):raise RuntimeError('Original full-state bundle seal mismatch')
                paths[str(rp)]=sha(rp);paths[str(bp)]=sha(bp);selected.append(row)
        groups.append((h,selected))
    return paths,groups

def logtail(z,k):return math.log(2)+abs(z)*math.sinh(1)-k-math.log1p(-math.exp(-1))
def coefficients(np,a,checks):
    rows=[];controls=[]
    for t in DELAYS+FD_DELAYS:
        if t==0:cn=np.zeros(DEGREE+1,dtype=complex);cn[0]=1;bound=ref=0.;lt=la=None
        else:
            z=a*t;c1=np.fft.fft(np.exp(-1j*z*np.cos(2*np.pi*np.arange(FFT_N)/FFT_N)))/FFT_N
            c2=np.fft.fft(np.exp(-1j*z*np.cos(2*np.pi*np.arange(2*FFT_N)/(2*FFT_N))))/(2*FFT_N)
            one=c1[:DEGREE+1].copy();cn=c2[:DEGREE+1].copy();one[1:]*=2;cn[1:]*=2
            ref=float(np.sum(np.abs(one-cn)));lt=logtail(z,DEGREE+1);la=math.log(2*DEGREE+1)+logtail(z,FFT_N-DEGREE)
            hi=max(lt,la);bound=math.exp(hi)* (math.exp(lt-hi)+math.exp(la-hi))
        check(checks,f'delay{t}_certified_coefficients',bound<1e-12 and ref<2e-11,dict(exact_error_ceiling=bound,coefficient_refinement_l1=ref,truncation_log=lt,alias_log=la))
        controls.append(dict(delay=t,exact_error_ceiling=bound,coefficient_refinement_l1=ref,truncation_log=lt,alias_log=la));rows.append(cn*np.exp(-1j*CENTER*t))
    return np.array(rows),controls

def propagate(np,apply,inputs,a,coeff):
    """Own recurrence: six main delays/three sources plus two psi FD controls."""
    v0=inputs.copy();v1=np.stack([(apply(v)-CENTER*v)/a for v in v0])
    main=np.empty((len(DELAYS),3,len(v0[0])),dtype=complex)
    fd=np.empty((2,len(v0[0])),dtype=complex)
    for j in range(len(DELAYS)):main[j]=coeff[j,0]*v0+coeff[j,1]*v1
    for j in range(2):fd[j]=coeff[j+len(DELAYS),0]*v0[0]+coeff[j+len(DELAYS),1]*v1[0]
    for k in range(2,DEGREE+1):
        v2=np.stack([2*(apply(v)-CENTER*v)/a for v in v1])-v0
        for j in range(len(DELAYS)):main[j]+=coeff[j,k]*v2
        for j in range(2):fd[j]+=coeff[j+len(DELAYS),k]*v2[0]
        v0,v1=v1,v2
    main[0]=inputs
    return main,fd
def taylor(np,apply,inputs):
    out=inputs.copy();terms=inputs.copy()
    for k in range(1,TAYLOR_DEGREE+1):terms=np.stack([(-1j*.1/k)*(apply(v)-CENTER*v) for v in terms]);out+=terms
    return out*np.exp(-1j*CENTER*.1)
def source_diagonal(np,f):
    d=(f['d'][:,0]-2)**2+f['q'][:,0]+f['p'][:,0]
    d=d.astype(float)
    for e,(u,v) in enumerate(((i,3+j) for i in range(3) for j in range(3))):
        if u==0 or v==0:d+=.5*f['nb'][:,e]*(.25*(f['p'][:,u]+f['p'][:,v])-.5*(f['q'][:,u]+f['q'][:,v]))
    return d
def h0_bound(np,f,d):
    off=np.full(len(d),3*.2/2)
    mids=np.array([.5 if u==0 or v==0 else 0 for u,v in ((i,3+j) for i in range(3) for j in range(3))])
    for active,edge in zip(f['activity'],f['hop_edges']):off+=.1*active*mids[edge]
    off+=f['g']*(f['c']==0)
    return float(np.max(np.abs(d)+off))

def readouts(np,psi,Hpsi,hpsi,diags):
    vectors=[d*psi for _,d,_ in diags]+[Hpsi,hpsi]
    means=np.array([np.vdot(psi,v).real for v in vectors])
    return vectors,means
def kick_vectors(np,cols,norms,sign):return (cols[0]-sign*1j*KICK*cols[1]-.5*KICK*KICK*cols[2])/norms[sign]
def kick_norms(np,cols):return {sign:float(np.linalg.norm(cols[0]-sign*1j*KICK*cols[1]-.5*KICK*KICK*cols[2])) for sign in (1,-1)}
def kick_controls(np,c,prefix,cols,Hcols,hcols,diags,norms,kernels,initial_energy,initial_kick_energy,Gbound):
    plus=kick_vectors(np,cols,norms,1);minus=kick_vectors(np,cols,norms,-1)
    hp=(Hcols[0]-1j*KICK*Hcols[1]-.5*KICK*KICK*Hcols[2])/norms[1]
    hm=(Hcols[0]+1j*KICK*Hcols[1]-.5*KICK*KICK*Hcols[2])/norms[-1]
    qp=(hcols[0]-1j*KICK*hcols[1]-.5*KICK*KICK*hcols[2])/norms[1]
    qm=(hcols[0]+1j*KICK*hcols[1]-.5*KICK*KICK*hcols[2])/norms[-1]
    _,mplus=readouts(np,plus,hp,qp,diags);_,mminus=readouts(np,minus,hm,qm,diags)
    derivative=(mplus-mminus)/(2*KICK);bounds=[z[2] for z in diags]+[HBND_CURRENT,GBND_CURRENT]
    tail=math.exp(KICK*Gbound)*(KICK*Gbound)**3/6
    for i,(name,bnd) in enumerate(zip([z[0] for z in diags]+['H','h0'],bounds)):
        lim=5e-7*max(1.,bnd)+bnd*(2*Gbound)**3*KICK*KICK/6+4*bnd*tail/KICK
        err=abs(float(derivative[i]-kernels[i]));check(c,prefix+'_'+name+'_plus_kick_sign',err<=lim,dict(error=err,tolerance=lim,analytic_Taylor_remainder=tail))
    ep=float(np.vdot(plus,hp).real);em=float(np.vdot(minus,hm).real)
    close(np,c,prefix+'_plus_norm',float(np.vdot(plus,plus).real),1.,2e-9);close(np,c,prefix+'_minus_norm',float(np.vdot(minus,minus).real),1.,2e-9)
    close(np,c,prefix+'_plus_energy_after_pulse_constant',ep,initial_kick_energy[1],2e-9)
    close(np,c,prefix+'_minus_energy_after_pulse_constant',em,initial_kick_energy[-1],2e-9)
    return dict(plus_source_off_energy=ep,minus_source_off_energy=em,plus_owned_work=ep-initial_energy,minus_owned_work=em-initial_energy,centered_complete_work=(ep-em)/(2*KICK),analytic_Taylor_remainder=tail)

def run_row(np,old,f,a,coeff,controls,original,psi,diags,t0,key,custody):
    global HBND_CURRENT,GBND_CURRENT
    c=[];apply=lambda v:old.apply(np,f,v);unit=np.array([1.,0.,0.,0.,0.,0.]);h0=lambda v:old.weighted(np,f,v,unit)
    hp=apply(psi);qp=h0(psi);q2=h0(qp);inputcols=np.stack([psi,qp,q2]);n0=float(np.vdot(psi,psi).real)
    close(np,c,'saved_norm',n0,1.,2e-8)
    close(np,c,'saved_complete_energy',float(np.vdot(psi,hp).real),original['complete_energy'],2e-8)
    close(np,c,'saved_node0_energy',float(np.vdot(psi,qp).real),original['complete_owned_node_energy'][0],2e-8)
    _,initialmeans=readouts(np,psi,hp,qp,diags)
    close(np,c,'saved_carrier_means',initialmeans[:6],original['carrier_mean'],2e-8)
    close(np,c,'saved_record_means',initialmeans[6:12],original['record_mean'],2e-8)
    close(np,c,'saved_M',initialmeans[12],original['graph']['edge_mean'],2e-8)
    close(np,c,'saved_connection',initialmeans[13],original['graph']['connected_probability'],2e-8)
    expected_energy_kernel=float(np.real(-1j*np.vdot(psi,apply(qp)-h0(hp))))
    initial_local_rate=float(2*np.real(np.vdot(-1j*hp,qp)))
    close(np,c,'initial_complete_impulse_work_sign',expected_energy_kernel,-initial_local_rate)
    main,fd=propagate(np,apply,inputcols,a,coeff)
    gram=inputcols.conj()@inputcols.T
    input_column_names=('psi','h0psi','h0_squared_psi')
    input_column_norms=dict(zip(input_column_names,np.sqrt(np.real(np.diag(gram))).tolist()))
    vector_error_ceilings=[dict(delay=v['delay'],exact_operator_error_ceiling=v['exact_error_ceiling'],exact_vector_error_ceilings={name:v['exact_error_ceiling']*norm for name,norm in input_column_norms.items()},propagated_columns=list(input_column_names) if i<len(DELAYS) else ['psi']) for i,v in enumerate(controls)]
    if original['tau']==0:
        independent=taylor(np,apply,inputcols);close(np,c,'NEW_independent_Taylor_delay_point1',independent,main[1],3e-8)
        del independent
    norms_local=kick_norms(np,inputcols);H2=apply(hp);uniform_input=np.stack([psi,hp,H2]);norms_uniform=kick_norms(np,uniform_input)
    initial_energy=float(np.vdot(psi,hp).real)/n0
    init_local={};init_uniform={}
    for sign in (1,-1):
        v=kick_vectors(np,inputcols,norms_local,sign);init_local[sign]=float(np.vdot(v,apply(v)).real)
        v=kick_vectors(np,uniform_input,norms_uniform,sign);init_uniform[sign]=float(np.vdot(v,apply(v)).real)
    rows=[];names=[z[0] for z in diags]+['H','h0'];obounds=[z[2] for z in diags]+[HBND_CURRENT,GBND_CURRENT]
    for j,delay in enumerate(DELAYS):
        cols=main[j];Hcols=np.stack([apply(v) for v in cols]);hcols=np.stack([h0(v) for v in cols]);vectors,means=readouts(np,cols[0],Hcols[0],hcols[0],diags)
        local=np.array([2*np.imag(np.vdot(v,cols[1])) for v in vectors]);uniform=np.array([2*np.imag(np.vdot(v,Hcols[0])) for v in vectors])
        direct_dt=np.array([2*np.real(np.vdot(-1j*Hcols[0],v)) for v in vectors])
        close(np,c,f't{delay}_uniform_actual_time_derivative',uniform,direct_dt)
        close(np,c,f't{delay}_uniform_complete_energy_zero',uniform[14],0.)
        close(np,c,f't{delay}_local_complete_energy_constant',local[14],expected_energy_kernel)
        close(np,c,f't{delay}_sumcarrier_response_zero',float(local[:6].sum()),0.)
        close(np,c,f't{delay}_uniform_sumcarrier_zero',float(uniform[:6].sum()),0.)
        close(np,c,f't{delay}_raw_Gram_conservation',cols.conj()@cols.T,gram,2e-9)
        close(np,c,f't{delay}_raw_complete_energy_conservation',means[14],initialmeans[14],2e-9)
        close(np,c,f't{delay}_source_H_secondmoment',float(np.vdot(Hcols[0],Hcols[0]).real),float(np.vdot(hp,hp).real),2e-9)
        if f['g']==0:close(np,c,f't{delay}_g0_record_response_null',local[6:12],np.zeros(6))
        kw=kick_controls(np,c,f't{delay}_local',cols,Hcols,hcols,diags,norms_local,local/n0,initial_energy,init_local,GBND_CURRENT)
        Hu2=apply(Hcols[0]);ucols=np.stack([cols[0],Hcols[0],Hu2]);uH=np.stack([Hcols[0],Hu2,apply(Hu2)]);uh=np.stack([hcols[0],h0(Hcols[0]),h0(Hu2)])
        uw=kick_controls(np,c,f't{delay}_uniform',ucols,uH,uh,diags,norms_uniform,uniform/n0,initial_energy,init_uniform,HBND_CURRENT)
        close(np,c,f't{delay}_uniform_plus_energy_work_zero',uw['plus_owned_work'],0.)
        close(np,c,f't{delay}_uniform_minus_energy_work_zero',uw['minus_owned_work'],0.)
        rows.append(dict(delay=delay,means=dict(zip(names,means.tolist())),local_plus_kernel=dict(zip(names,local.tolist())),uniform_H_kernel=dict(zip(names,uniform.tolist())),local_kick=kw,uniform_kick=uw))
        del Hcols,hcols,vectors,ucols,uH,uh
    fm=[]
    for v in fd:_,means=readouts(np,v,apply(v),h0(v),diags);fm.append(means)
    derivative=(fm[1]-fm[0])/(2*FD_STEP);target=np.array([rows[1]['uniform_H_kernel'][name] for name in names])
    for i,(name,bnd) in enumerate(zip(names,obounds)):
        trunc=bnd*(2*a)**3*FD_STEP**2/6;fp=bnd*4e-9/FD_STEP;err=abs(float(derivative[i]-target[i]));check(c,name+'_NEW_FD_time_derivative',err<=trunc+fp,dict(error=err,truncation_allowance=trunc,floating_allowance=fp,tolerance=trunc+fp))
    bundle=CP/(key+'.bundle.npz')
    with bundle.open('xb') as out:np.savez(out,propagated_main_columns=main,control_psi=fd,input_columns=inputcols,delays=np.array(DELAYS),FD_delays=np.array(FD_DELAYS),metadata_json=json.dumps(dict(g=f['g'],start=original['start'],age=original['tau'],original_bundle_sha256=original['bundle_sha256'],input_norm=n0,input_column_norms=input_column_norms,certified_vector_error_ceilings=vector_error_ceilings,input_sha256=custody),sort_keys=True));out.flush();os.fsync(out.fileno())
    event('bundle_saved',key=key,path=str(bundle),sha256=sha(bundle))
    row=dict(g=f['g'],start=original['start'],age=original['tau'],original_bundle_sha256=original['bundle_sha256'],bundle_path=str(bundle),bundle_sha256=sha(bundle),input_sha256=custody,input_norm=n0,input_column_norms=input_column_norms,certified_vector_error_ceilings=vector_error_ceilings,initial_local_energy_age_derivative=initial_local_rate,complete_local_impulse_work_derivative=expected_energy_kernel,coefficient_controls=controls,observables=names,response=rows,checks=c,failed_count=sum(not x['passed'] for x in c),elapsed_seconds=time.monotonic()-t0,peak_RSS_bytes=rss())
    rp=CP/(key+'.json');exclusive(rp,row);event('row_complete',key=key,path=str(rp),sha256=sha(rp),failed=row['failed_count'],peak_RSS_bytes=row['peak_RSS_bytes'])
    print(json.dumps(dict(checkpoint=key,failed=row['failed_count'],elapsed_seconds=row['elapsed_seconds'],peak_RSS_bytes=row['peak_RSS_bytes'])),flush=True)
    return row

def execute():
    global HBND_CURRENT,GBND_CURRENT
    if sys.platform!='darwin':raise RuntimeError('Same Mac only')
    if any(p.exists() for p in (CP,RESULT,REPORT)):raise RuntimeError('Exclusive outputs exist; no replay/resume authorized')
    if any(os.environ.get(k)!='1' for k in ENV_KEYS):raise RuntimeError('One-thread environment must be set before NumPy import')
    hashes,groups=authenticate();CP.mkdir();t0=time.monotonic()
    manifest=dict(pid=os.getpid(),ppid=os.getppid(),host=socket.gethostname(),utc=utc(),input_sha256=hashes,environment={k:os.environ[k] for k in ENV_KEYS},inputs=dict(g=GS,starts=STARTS,ages=AGES,delays=DELAYS,FD_delays=FD_DELAYS,degree=DEGREE,FFT_N=FFT_N,Taylor_degree=TAYLOR_DEGREE,source_node=0,kick=KICK,one_row_resident=True,no_old_producer_or_propagation=True))
    exclusive(CP/'manifest.json',manifest);event('started',manifest_sha256=sha(CP/'manifest.json'));print(json.dumps(dict(pid=os.getpid(),ppid=os.getppid(),status='started')),flush=True)
    try:
        import numpy as np
        spec=importlib.util.spec_from_file_location('sealed_k33_operator_helpers',OLD_SOURCE);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
        allrows=[];checks=[];Hcontrols=[]
        for gi,(meta,selected) in enumerate(groups):
            g=GS[gi];f=old.fields(np,g);a=float(np.nextafter(14.75+9*.2+3*.1+g+1e-12,np.inf))
            close(np,checks,f'g{gi}_sealed_center',CENTER,meta['center']);close(np,checks,f'g{gi}_sealed_halfwidth',a,meta['halfwidth'])
            rowbound=float(np.max((np.abs(f['D']-CENTER)+9*.2+.1*f['d'][f['rows'],f['c']]+g)/a));check(checks,f'g{gi}_complete_H_spectral_row_bound',rowbound<=1,dict(rowbound=rowbound))
            d0=source_diagonal(np,f);GBND_CURRENT=h0_bound(np,f,d0);HBND_CURRENT=abs(CENTER)+a
            check(checks,f'g{gi}_h0_diagonal_bound',float(np.max(np.abs(d0)))<=6.)
            check(checks,f'g{gi}_h0_complete_row_bound',GBND_CURRENT<=6.45+g+1e-12,dict(maximum=GBND_CURRENT))
            coef,controls=coefficients(np,a,checks);tail_log=a*.1+81*math.log(a*.1)-math.lgamma(82)
            check(checks,f'g{gi}_NEW_Taylor_remainder',tail_log<math.log(1e-12),dict(log_bound=tail_log))
            probe=np.exp(1j*(np.arange(old.DIM)%257)/257)/math.sqrt(old.DIM);other=np.exp(1j*(np.arange(old.DIM)%193)/193)/math.sqrt(old.DIM)
            hp=old.apply(np,f,probe);hq=old.weighted(np,f,probe,np.eye(6)[0]);hother=old.weighted(np,f,other,np.eye(6)[0])
            close(np,checks,f'g{gi}_h0_Hermitian_probe',np.vdot(other,hq),np.vdot(hother,probe),3e-10)
            close(np,checks,f'g{gi}_whole_node_sum_probe',old.weighted(np,f,probe,np.ones(6)),hp,3e-10)
            close(np,checks,f'g{gi}_uniform_complete_probe',old.weighted(np,f,probe,np.full(6,.93)),.93*hp,3e-10)
            pp=CP/f'g{gi}_preflight.json';pcheck=[x for x in checks if x['name'].startswith(f'g{gi}_') or x['name'].startswith('delay')]
            exclusive(pp,dict(g=g,input_sha256=hashes,center=CENTER,halfwidth=a,h0_norm_bound=GBND_CURRENT,H_norm_bound=HBND_CURRENT,checks=pcheck,coefficient_controls=controls));event('preflight_saved',key=f'g{gi}',sha256=sha(pp))
            if any(not x['passed'] for x in pcheck):raise ArithmeticError('Frozen numerical preflight failed; no prepared-row calculation')
            diags=[(f'carrier{v}',f['p'][:,v],1.) for v in range(6)]+[(f'record{v}',f['q'][:,v],1.) for v in range(6)]
            diags += [('M',f['graph']['M'][f['ns']],9.),('connected',f['graph']['connected'][f['ns']],1.)]
            Hcontrols.append(dict(g=g,center=CENTER,halfwidth=a,h0_norm_bound=GBND_CURRENT,H_norm_bound=HBND_CURRENT,coefficient_controls=controls,Taylor_remainder_log=tail_log))
            for start in STARTS:
                orig=next(x for x in selected if x['start']==start)
                with np.load(orig['bundle_path'],allow_pickle=False) as z:
                    if json.loads(str(z['input_sha256_json']))!=meta['input_sha256'] or float(z['g'])!=g or int(z['start'])!=start:raise RuntimeError('Saved array metadata changed')
                    if json.loads(str(z['schedule_json']))!=[list(s) for s in old.SCHEDULE]:raise RuntimeError('Saved schedule metadata changed')
                    saved=z['full_states']
                if saved.shape!=(len(old.SCHEDULE),old.DIM) or not np.all(np.isfinite(saved)):raise RuntimeError('Saved array shape/finite gate failed')
                for original in (x for x in selected if x['start']==start):
                    schedule=old.SCHEDULE[original['bundle_index']]
                    if schedule[0]!=original['time_key'] or schedule[1]!=original['tau'] or schedule[2]:raise RuntimeError('Selected state schedule index mismatch')
                    psi=saved[original['bundle_index']].copy();key=f'g{gi}_n{start}_age{int(original["tau"])}'
                    allrows.append(run_row(np,old,f,a,coef,controls,original,psi,diags,t0,key,hashes));del psi;gc.collect()
                del saved;gc.collect()
            del f,probe,other,hp,hq,hother,diags,coef;gc.collect()
        after,_=authenticate();check(checks,'input_bytes_unchanged',hashes==after);check(checks,'complete_16_snapshot_96_delay_census',len(allrows)==16 and sum(len(r['response']) for r in allrows)==96)
        combined=checks+[z for r in allrows for z in r['checks']];failed=[z for z in combined if not z['passed']]
        payload=dict(status='QUALIFIED_ARITHMETIC' if not failed else 'FAILED_ARITHMETIC',qualification='Actual prepared-state complete nodal-energy commutator response and owned ideal pulse work only; no geometry/gravity/physical clock/continuum/observational or formation acceptance',manifest=manifest,Hamiltonian_controls=Hcontrols,checks=checks,rows=allrows,passed_count=len(combined)-len(failed),failed_count=len(failed),failed_checks=failed,runtime_seconds=time.monotonic()-t0,peak_RSS_bytes=rss(),pid=os.getpid())
        payload['canonical_payload_sha256']=canonical(payload);exclusive(RESULT,payload);event('result_saved',sha256=sha(RESULT),canonical_payload_sha256=payload['canonical_payload_sha256'])
        lines=['# K3,3 nodal energy-to-signal V001: sealed result','',f"{payload['status']}; {payload['passed_count']}/{len(combined)} controls; {len(allrows)} snapshots/{sum(len(r['response']) for r in allrows)} source delays.",'',payload['qualification'],'',f"Runtime{payload['runtime_seconds']:.6f}s; peakRSS{payload['peak_RSS_bytes']}bytes; PID{os.getpid()}.",'','All complete source, record/support energy, complex phases and signed responses retained. Local h0 total-energy impulse work is generally nonzero and delay-independent; uniformH kernel is actual conditional-time derivative and uniform energy work is zero. No static susceptibility or physical propagation speed is inferred.','', '| g | start | age | local complete energy impulse derivative |','|---|---:|---:|---:|']
        for r in allrows:lines.append(f"|{r['g']}|{r['start']}|{r['age']}|{r['complete_local_impulse_work_derivative']:.12g}|")
        lines += ['',f'Raw result SHA256:{sha(RESULT)}',f"Canonical payloadSHA256:{payload['canonical_payload_sha256']}",f'ProtocolSHA256:{hashes[str(PROTOCOL)]}',f'SourceSHA256:{hashes[str(SOURCE)]}','', 'Every completed snapshot has an exclusive complete-phase bundle, JSON and journal seal. This process ends here; no automatic continuation or replay is installed. Parent owns continuation log/ledger integration.']
        with REPORT.open('x',encoding='utf-8') as out:out.write('\n'.join(lines)+'\n');out.flush();os.fsync(out.fileno())
        event('report_saved',sha256=sha(REPORT));print(json.dumps(dict(status=payload['status'],passed=payload['passed_count'],failed=payload['failed_count'],result_sha256=sha(RESULT),report_sha256=sha(REPORT),runtime_seconds=payload['runtime_seconds'],peak_RSS_bytes=payload['peak_RSS_bytes'])),flush=True)
        return 0 if not failed else 2
    except BaseException as e:
        error=dict(status='INTERRUPTED_OR_FAILED',error=repr(e),traceback=traceback.format_exc(),pid=os.getpid(),runtime_seconds=time.monotonic()-t0,peak_RSS_bytes=rss())
        exclusive(CP/'error.json',error);event('error',sha256=sha(CP/'error.json'));print(json.dumps(error),flush=True);return 3

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    if args.execute:return execute()
    print('Prospective source only. Root preflight, sealed receipt and ownership approval required.');return 0
if __name__=='__main__':sys.exit(main())
