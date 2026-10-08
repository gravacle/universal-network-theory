#!/usr/bin/env python3
"""New all-six-record BS10 matrix-free witness; no old producer or eigensolver."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import gc
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=HERE/'BS10_SIX_RECORD_FORMATION_V001.md';SOURCE=HERE/'bs10_six_record_formation_v001.py'
OLD=HERE/'BS10_TWO_RECORD_FORMATION_V001_RESULT.json'
RESULT=HERE/'BS10_SIX_RECORD_FORMATION_V001_RESULT.json';REPORT=HERE/'BS10_SIX_RECORD_FORMATION_V001_RESULT.md'
CP=HERE/'bs10_six_record_formation_v001_checkpoints'
UD,ER,EP,LR,LJ,HFLIP,THOP=1.,1.,1.,.5,.25,.1,.1
GS=(0.,.1);STARTS=(21,42);TIMES=(0.,1.,2.,5.,10.,20.,50.);TINY=(.001,.002)
SCHEDULE=[('main'+str(i),t,False) for i,t in enumerate(TIMES)]
SCHEDULE += [('early'+str(i)+'_'+sign,sgn*t,True) for i,t in enumerate(TINY) for sign,sgn in [('plus',1),('minus',-1)]]
DIM,M,N,ALPHA=24576,400,4096,1.
CENTER,PAD=11.875,1e-12
OP_TOL,OBS_TOL,PSD_TOL=1e-11,2e-8,1e-11
MAX_RSS,MAX_SECONDS=512*1024*1024,60.

def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def exclusive(path,value):
    with path.open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def event(kind,**values):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=kind,utc=utc(),pid=os.getpid(),**values),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def check(items,name,passed,evidence=None):
    item=dict(name=name,passed=bool(passed))
    if evidence is not None:item['evidence']=evidence
    items.append(item)
def cjson(a):return dict(real=a.real.tolist(),imag=a.imag.tolist())
def msha(np,a):return hashlib.sha256(np.ascontiguousarray(a,dtype='<f8').tobytes()).hexdigest()
def inputs():return dict(dimension=DIM,Nc=1,dynamic_records='all6',U_d=UD,Delta=0,d_star=2,
    epsilon_r=ER,epsilon_psi=EP,lambda_R=LR,lambda_J=LJ,h=HFLIP,t=THOP,g=list(GS),
    starts=list(STARTS),carrier_start=0,record_start='allblank',times=list(TIMES),tiny=list(TINY),
    Chebyshev_degree=M,FFT_N=N,refinement_FFT_N=2*N,tail_alpha=ALPHA,center=CENTER,
    outward_halfwidth_pad=PAD,certified_truncation_alias_limit=1e-12,
    coefficient_refinement_l1_limit=2e-11,source_tolerance=OP_TOL,observable_tolerance=OBS_TOL,
    PSD_tolerance=PSD_TOL,BLAS_threads=1,source='complete12node affine operational source',
    conditional_coherent_content_witness='same pure spatial/incidence seed,content|+>',
    peak_RSS_limit_bytes=MAX_RSS,Hamiltonian_time_limit_seconds=MAX_SECONDS)
def anchors():
    old=json.loads(OLD.read_text());paths=[PROTOCOL,SOURCE,OLD]
    paths += [Path(p) for p in old['input_sha256']]
    for h in old['Hamiltonians']:
        paths.append(Path(h['eigensystem_path']))
        paths += [Path(r['state_path']) for r in h['states']]
    hashes={str(p):sha(p) for p in paths}
    if old['status']!='QUALIFIED_ARITHMETIC' or len(old['Hamiltonians'])!=2:raise RuntimeError('Old witness unqualified')
    for p,digest in old['input_sha256'].items():
        if hashes[p]!=digest:raise RuntimeError('Old source/native anchor changed')
    for h in old['Hamiltonians']:
        if hashes[h['eigensystem_path']]!=h['eigensystem_sha256']:raise RuntimeError('Old eigensystem changed')
        for r in h['states']:
            if hashes[r['state_path']]!=r['state_sha256']:raise RuntimeError('Old state changed')
    return old,hashes

def fields(np,g):
    rows=np.arange(DIM);ns=rows//384;c=(rows//64)%6;r=rows%64
    bits=np.array([[(mask>>v)&1 for v in range(6)] for mask in range(64)],dtype=float)
    p=np.eye(6)[c];q=bits[r];nb=bits[ns]
    pos=np.array([(np.cos(2*np.pi*v/6),np.sin(2*np.pi*v/6)) for v in range(6)])
    mid=(pos+np.roll(pos,-1,axis=0))/2
    d=1+nb+np.roll(nb,1,axis=1)
    D=np.zeros(DIM);gd=np.zeros((DIM,2));parts={
        'active_degree':UD*np.sum((d-2)**2,axis=1),'exterior_degree':np.full(DIM,6*UD),
        'carrier_storage':np.full(DIM,EP),'external_current_square':np.full(DIM,LJ),
        'record_storage':ER*q.sum(axis=1),'external_record_feedback':-LR*q.sum(axis=1),
        'internal_current_square':np.zeros(DIM),'internal_record_feedback':np.zeros(DIM)}
    for v in range(6):
        onsite=UD*(d[:,v]-2)**2+ER*q[:,v]+EP*p[:,v];ext=LJ*p[:,v]-LR*q[:,v]
        D+=onsite+UD+ext;gd+=(onsite+2*UD+1.5*ext)[:,None]*pos[v]
    for e in range(6):
        nxt=(e+1)%6;current=LJ*nb[:,e]*(p[:,e]+p[:,nxt]);rec=-LR*nb[:,e]*(q[:,e]+q[:,nxt])
        parts['internal_current_square']+=current;parts['internal_record_feedback']+=rec
        D+=current+rec;gd+=(current+rec)[:,None]*mid[e]
    flips=[((ns^(1<<e))*6+c)*64+r for e in range(6)]
    right=(ns*6+(c+1)%6)*64+r;left=(ns*6+(c-1)%6)*64+r;copy=(ns*6+c)*64+(r^(1<<c))
    nr=nb[rows,c];nl=nb[rows,(c-1)%6]
    reflection_n=np.array([sum(((n>>e)&1)<<((-e-1)%6) for e in range(6)) for n in range(64)])
    reflection_r=np.array([sum(((mask>>v)&1)<<((-v)%6) for v in range(6)) for mask in range(64)])
    ref=(reflection_n[ns]*6+(-c)%6)*64+reflection_r[r]
    return dict(rows=rows,ns=ns,c=c,r=r,p=p,q=q,nb=nb,pos=pos,mid=mid,d=d,D=D,gd=gd,
                parts=parts,flips=flips,right=right,left=left,copy=copy,nr=nr,nl=nl,ref=ref,g=g)
def apply(np,f,v,coordinate=None):
    if coordinate is None:
        out=f['D']*v
        for idx in f['flips']:out-=HFLIP*v[idx]
        out-=THOP*(f['nr']*v[f['right']]+f['nl']*v[f['left']])
        out+=f['g']*v[f['copy']]
    else:
        i=coordinate;out=f['gd'][:,i]*v
        for e,idx in enumerate(f['flips']):out-=HFLIP*f['mid'][e,i]*v[idx]
        out-=THOP*(f['nr']*f['mid'][f['c'],i]*v[f['right']]
                     +f['nl']*f['mid'][(f['c']-1)%6,i]*v[f['left']])
        out+=f['g']*f['pos'][f['c'],i]*v[f['copy']]
    return out
def weighted(np,f,v,Nv):
    diagonal=np.zeros(DIM)
    for node in range(6):
        diagonal+=Nv[node]*(UD*(f['d'][:,node]-2)**2+ER*f['q'][:,node]+EP*f['p'][:,node])
        diagonal+=Nv[node+6]*UD+(Nv[node]+Nv[node+6])/2*(LJ*f['p'][:,node]-LR*f['q'][:,node])
    mid=(Nv[:6]+np.roll(Nv[:6],-1))/2
    for edge in range(6):
        nxt=(edge+1)%6
        diagonal+=mid[edge]*f['nb'][:,edge]*(LJ*(f['p'][:,edge]+f['p'][:,nxt])-LR*(f['q'][:,edge]+f['q'][:,nxt]))
    out=diagonal*v
    for edge,idx in enumerate(f['flips']):out-=HFLIP*mid[edge]*v[idx]
    out-=THOP*(f['nr']*mid[f['c']]*v[f['right']]+f['nl']*mid[(f['c']-1)%6]*v[f['left']])
    out+=f['g']*Nv[f['c']]*v[f['copy']]
    return out

def logtail(z,K):return math.log(2)+abs(z)*math.sinh(ALPHA)-K*ALPHA-math.log1p(-math.exp(-ALPHA))
def coefficient_table(np,a):
    coeff=[];controls=[]
    for key,tau,early in SCHEDULE:
        z=a*tau
        if tau==0:
            cn=np.zeros(M+1,dtype=complex);cn[0]=1;error=0.;lt=la=-math.inf
        else:
            first=np.fft.fft(np.exp(-1j*z*np.cos(2*np.pi*np.arange(N)/N)))/N
            second=np.fft.fft(np.exp(-1j*z*np.cos(2*np.pi*np.arange(2*N)/(2*N))))/(2*N)
            c1=first[:M+1].copy();cn=second[:M+1].copy();c1[1:]*=2;cn[1:]*=2
            error=float(np.sum(np.abs(c1-cn)));lt=logtail(z,M+1);la=math.log(2*M+1)+logtail(z,N-M)
        if tau==0:total_log=None;bound=0.
        else:
            hi=max(lt,la);total_log=hi+math.log(math.exp(lt-hi)+math.exp(la-hi))
            bound=math.exp(total_log) if total_log>-690 else 1e-300
        controls.append(dict(key=key,tau=tau,truncation_log=None if tau==0 else lt,
            alias_log=None if tau==0 else la,certified_total_log=total_log,certified_error_ceiling=bound,
            coefficient_refinement_l1=error,passed=bound<1e-12 and error<2e-11))
        coeff.append(cn*np.exp(-1j*CENTER*tau))
    return np.array(coeff),controls
def propagate(np,matvec,dim,seed,a,coeff):
    v0=np.zeros(dim,dtype=complex);v0[seed]=1
    states=coeff[:,0,None]*v0[None,:]
    v1=(matvec(v0)-CENTER*v0)/a;states+=coeff[:,1,None]*v1[None,:]
    for m in range(2,M+1):
        v2=2*(matvec(v1)-CENTER*v1)/a-v0;states+=coeff[:,m,None]*v2[None,:];v0,v1=v1,v2
    return states

def core(np,f):
    rows=np.arange(1536);n=rows//24;c=(rows//4)%6;rtwo=rows%4
    rmap=np.array([0,1,8,9]);sub=(n*6+c)*64+rmap[rtwo]
    lookup=np.full(DIM,-1,dtype=np.int64);lookup[sub]=rows
    mappings=[lookup[idx[sub]] for idx in f['flips']]+[lookup[f['right'][sub]],lookup[f['left'][sub]],lookup[f['copy'][sub]]]
    H=np.zeros((1536,1536));Gs=[np.zeros_like(H),np.zeros_like(H)]
    H[rows,rows]=f['D'][sub]
    for i in range(2):Gs[i][rows,rows]=f['gd'][sub,i]
    for e,target in enumerate(mappings[:6]):
        H[rows,target]-=HFLIP
        for i in range(2):Gs[i][rows,target]-=HFLIP*f['mid'][e,i]
    for j,activity,edge in [(6,f['nr'][sub],c),(7,f['nl'][sub],(c-1)%6)]:
        H[rows,mappings[j]]-=THOP*activity
        for i in range(2):Gs[i][rows,mappings[j]]-=THOP*activity*f['mid'][edge,i]
    allowed=mappings[8]>=0;src=rows[allowed];dst=mappings[8][allowed]
    H[src,dst]+=f['g']
    for i in range(2):Gs[i][src,dst]+=f['g']*f['pos'][c[allowed],i]
    def matvec(v):
        out=f['D'][sub]*v
        for idx in mappings[:6]:out-=HFLIP*v[idx]
        out-=THOP*(f['nr'][sub]*v[mappings[6]]+f['nl'][sub]*v[mappings[7]])
        out[allowed]+=f['g']*v[mappings[8][allowed]]
        return out
    return sub,H,Gs,matvec
def preflight(np,f,a,old,coeff):
    checks=[];g=f['g'];R=.6+THOP*(f['nr']+f['nl'])+g
    check(checks,'six_flip_maps_involutive',all(np.array_equal(idx[idx],f['rows']) for idx in f['flips']))
    check(checks,'copy_map_involutive',np.array_equal(f['copy'][f['copy']],f['rows']))
    check(checks,'carrier_hop_maps_adjoint',np.array_equal(f['right'][f['left']],f['rows'])
          and np.array_equal(f['nr'],f['nl'][f['right']]))
    check(checks,'exact_diagonal_range',float(f['D'].min())==7.5 and float(f['D'].max())==16.25)
    rowbound=float(np.max((np.abs(f['D']-CENTER)+R)/a))
    check(checks,'absolute_rescaled_row_bound',rowbound<=1,dict(maximum=rowbound))
    probe=np.exp(1j*(np.arange(DIM)%257)/257)/np.sqrt(DIM)
    eta=np.array([1e-6,-2e-6]);allpos=np.vstack([f['pos'],2*f['pos']]);Nv=1+allpos@eta
    hp=apply(np,f,probe);gx=apply(np,f,probe,0);gy=apply(np,f,probe,1)
    check(checks,'positive_lapse_arm',Nv.min()>0)
    check(checks,'whole_node_ownership',np.max(np.abs(weighted(np,f,probe,np.ones(12))-hp))<=OP_TOL)
    check(checks,'affine_source',np.max(np.abs(weighted(np,f,probe,Nv)-hp-eta[0]*gx-eta[1]*gy))<=OP_TOL)
    check(checks,'uniform_lapse',np.max(np.abs(weighted(np,f,probe,np.full(12,.93))-.93*hp))<=OP_TOL)
    ref=f['ref'];rprobe=probe[ref]
    check(checks,'reflection_H',np.max(np.abs(apply(np,f,rprobe)-hp[ref]))<=OP_TOL)
    check(checks,'reflection_Gx_even',np.max(np.abs(apply(np,f,rprobe,0)-gx[ref]))<=OP_TOL)
    check(checks,'reflection_Gy_odd',np.max(np.abs(apply(np,f,rprobe,1)+gy[ref]))<=OP_TOL)
    for start in STARTS:
        seed=np.zeros(DIM);seed[start*384]=1;action=apply(np,f,seed)
        coefficients=f['q'].T@(np.abs(action)**2)
        check(checks,'positive_original_copy_sign_'+str(start),abs(float(action[start*384+1])-g)<=OP_TOL)
        check(checks,'early_action_q0_'+str(start),abs(float(coefficients[0])-g*g)<=OP_TOL)
        check(checks,'early_action_otherq_'+str(start),np.max(np.abs(coefficients[1:]))<=OP_TOL)
    sub,H,G,matvec=core(np,f)
    with np.load(old['eigensystem_path'],allow_pickle=False) as data:E=data['complete_eigenvalues'];V=data['eigenvectors_columns']
    error=float(np.max(np.abs(H-(V*E)@V.T)))
    check(checks,'sealed_two_record_H_reconstruction',error<=OP_TOL,dict(maximum=error))
    for i,key in enumerate(('Gx','Gy')):check(checks,'sealed_projected_'+key+'_hash',msha(np,G[i])==old['matrix_sha256'][key])
    for start in STARTS:
        validation=propagate(np,matvec,1536,start*24,a,coeff)
        for j,(key,tau,early) in enumerate(SCHEDULE):
            previous=next(r for r in old['states'] if r['start']==start and r['tau']==tau and r['auxiliary_early_arm']==early)
            with np.load(previous['state_path'],allow_pickle=False) as data:psi=data['complete_state']
            error=float(np.max(np.abs(validation[j]-psi)))
            check(checks,'clamped_algorithm_old_state_'+str(start)+'_'+key,error<=2e-8,dict(maximum=error))
            for i in range(2):
                mean=float(np.real(np.vdot(psi,G[i]@psi)))
                check(checks,'projected_source_old_mean_'+str(start)+'_'+key+'_'+str(i),abs(mean-previous['complete_source_mean'][i])<=OBS_TOL)
    return checks

def sqrt_density(np,rho):
    vals,V=np.linalg.eigh(rho)
    if vals[0]<-PSD_TOL:raise ArithmeticError('Record density violates PSD tolerance')
    root=(V*np.sqrt(np.maximum(vals,0)))@V.conj().T
    return root,vals,dict(negative_clip_count=int(np.sum(vals<0)),minimum=float(vals[0]),
                        square_root_residual=float(np.max(np.abs(root@root-rho))))
def record_labels(np):
    masks=np.arange(64);zero=sum(((masks>>v)&1)*(3**v) for v in range(6));return zero,2*zero
def observe(np,f,start,tau,early,psi):
    checks=[];prob=np.abs(psi)**2;rho=psi.reshape(384,64).T@psi.reshape(384,64).conj()
    root,eigs,info=sqrt_density(np,rho);P=float(np.real(rho[0,0]));gamma=P*P
    labels0,labels1=record_labels(np);overlap=(labels0[:,None]==labels1[None,:]).astype(float)
    direct=complex(np.sum(overlap*rho));product=root@overlap@root
    sv=np.linalg.svd(product,compute_uv=False);independent=float(np.sum(sv)**2)
    check(checks,'physical_alphabet_overlap_only_blank',int(overlap.sum())==1 and overlap[0,0]==1)
    check(checks,'full_state_norm',abs(float(prob.sum())-1)<=OBS_TOL)
    check(checks,'density_trace',abs(complex(np.trace(rho))-1)<=OBS_TOL)
    check(checks,'density_Hermitian',np.max(np.abs(rho-rho.conj().T))<=2e-10)
    check(checks,'density_PSD',float(eigs[0])>=-PSD_TOL)
    check(checks,'density_sqrt_residual',info['square_root_residual']<=OBS_TOL)
    check(checks,'physical729_fidelity_via_isometries',abs(independent-gamma)<=OBS_TOL,
          dict(independent=independent,probability_gamma=gamma,difference=independent-gamma))
    check(checks,'direct_content_overlap',abs(direct-P)<=OBS_TOL)
    content=np.array([[1,direct],[direct.conjugate(),1]],dtype=complex)/2
    purity=float(np.real(np.trace(content@content)));check(checks,'content_purity_relation',abs(purity-(1+gamma)/2)<=OBS_TOL)
    content_eigs=np.array([(1+abs(direct))/2,(1-abs(direct))/2]);positive_content=content_eigs[content_eigs>0]
    content_entropy=float(-np.sum(positive_content*np.log(positive_content)))
    q=prob@f['q'];p=prob@f['p'];n=prob@f['nb'];d=prob@f['d']
    energy={k:float(prob@a) for k,a in f['parts'].items()}
    energy['incidence_flip']=-HFLIP*sum(float(np.real(np.vdot(psi,psi[idx]))) for idx in f['flips'])
    energy['carrier_hopping']=-THOP*float(np.real(np.vdot(psi,f['nr']*psi[f['right']]+f['nl']*psi[f['left']])))
    energy['record_copy']=f['g']*float(np.real(np.vdot(psi,psi[f['copy']])))
    total=float(np.real(np.vdot(psi,apply(np,f,psi))));initial=float(f['D'][start*384])
    check(checks,'complete_energy_components',abs(sum(energy.values())-total)<=OBS_TOL*max(1.,abs(total)))
    check(checks,'unitary_energy_conserved',abs(total-initial)<=OBS_TOL*max(1.,abs(initial)))
    check(checks,'fixed_carrier_number',abs(float(p.sum())-1)<=OBS_TOL)
    if f['g']==0:
        check(checks,'null_records_blank',float(q.sum())<=OBS_TOL and abs(P-1)<=OBS_TOL)
        check(checks,'null_visibility_gamma_one',abs(gamma-1)<=OBS_TOL)
    if early and f['g']!=0:
        leading=f['g']**2*tau**2
        for key,ratio in [('q0',float(q[0])/leading),('Pblank',(1-P)/leading),('gamma',(1-gamma)/(2*leading))]:
            check(checks,'early_coefficient_'+key,abs(ratio-1)<=1e-5,dict(ratio=ratio))
        check(checks,'early_otherrecords_no_tau_squared',float(q[1:].sum())<=1e-7*leading+1e-20)
    positive=eigs[eigs>0];entropy=float(-np.sum(positive*np.log(positive)))
    return dict(g=f['g'],start=start,tau=tau,auxiliary_early_arm=early,P_allblank=P,gamma_rec=gamma,
        gamma_independent_physical_fidelity=independent,record_mean=q.tolist(),carrier_mean=p.tolist(),
        incidence_mean=n.tolist(),degree_mean=d.tolist(),record_total=float(q.sum()),
        record_density64=cjson(rho),record_density_eigenvalues=eigs.tolist(),record_entropy=entropy,
        fidelity_square_root_diagnostic=info,fidelity_singular_values=sv.tolist(),
        physical729_content0_indices=labels0.tolist(),physical729_content1_indices=labels1.tolist(),
        coherent_content_density=cjson(content),direct_content_overlap=dict(real=direct.real,imag=direct.imag),
        fringe_visibility=abs(direct),coherent_content_purity=purity,coherent_content_entropy=content_entropy,
        coherent_content_scope='same pure spatial/incidence seed; content-exchange paired branches only',
        complete_energy=total,initial_complete_energy=initial,complete_energy_components=energy,
        complete_source_mean=[float(np.real(np.vdot(psi,apply(np,f,psi,i)))) for i in range(2)],
        checks=checks,failed_count=sum(not c['passed'] for c in checks))

def finish(receipt):
    checks=receipt['checks'][:]
    for h in receipt['Hamiltonians']:
        checks+=h['checks']
        for r in h['states']:checks+=r['checks']
    receipt['check_count']=len(checks);receipt['passed_count']=sum(c['passed'] for c in checks);receipt['failed_count']=len(checks)-receipt['passed_count']
    receipt['completed_utc']=utc();payload=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with RESULT.open('xb') as f:f.write(payload)
    digest=hashlib.sha256(payload).hexdigest()
    lines=['# BS10 six-record formation V001: saved result','',f"Status {receipt['status']}; checks {receipt['passed_count']}/{receipt['check_count']}; failures {receipt['failed_count']}.",'',receipt['qualification'],'',
        '| g | seed | tau | total records | P_allblank | gamma_rec | content visibility | record entropy |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for h in receipt['Hamiltonians']:
        for r in h['states']:
            if not r['auxiliary_early_arm']:lines.append(f"| {r['g']:.2f} | {r['start']} | {r['tau']:.6g} | {r['record_total']:.12g} | {r['P_allblank']:.12g} | {r['gamma_rec']:.12g} | {r['fringe_visibility']:.12g} | {r['record_entropy']:.9g} |")
    lines+=['','The derived content visibility uses the explicitly stated pure paired-content witness. Native copy/feedback, energy/source ownership, reversible record histories, density/fidelity diagnostics and all mathematical/numerical propagator controls remain qualified as a supported finite realization.','',
        f'Result JSON SHA256: {digest}',f"Runtime {receipt['runtime_seconds']:.6g}s; peak RSS {receipt['peak_RSS_bytes']} bytes; PID {receipt['pid']}.",'',f"Exact unfinished work: {receipt.get('next_unfinished')}"]
    with REPORT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(status=receipt['status'],Hamiltonians=len(receipt['Hamiltonians']),states=sum(len(h['states']) for h in receipt['Hamiltonians']),
        checks=receipt['check_count'],passed=receipt['passed_count'],failed=receipt['failed_count'],runtime_seconds=receipt['runtime_seconds'],peak_RSS_bytes=receipt['peak_RSS_bytes'],
        json_sha256=digest,json_path=str(RESULT),markdown_path=str(REPORT),next_unfinished=receipt.get('next_unfinished'),exception=receipt.get('exception')),indent=2))

def execute(resume):
    if sys.platform!='darwin' or Path(__file__).resolve()!=SOURCE.resolve():raise RuntimeError('Wrong local context')
    if RESULT.exists() or REPORT.exists():raise FileExistsError('Final receipt exists; no overwrite')
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
    old,custody=anchors();frozen=inputs();previous=[];mp=CP/'manifest.json'
    if resume:
        manifest=json.loads(mp.read_text());previous=[json.loads(s) for s in (CP/'events.jsonl').read_text().splitlines()]
        if manifest['inputs']!=frozen or manifest['input_sha256']!=custody or manifest['host']!=socket.gethostname():raise RuntimeError('Resume custody mismatch')
        starts=[e for e in previous if e['event']=='run_start'];pid=starts[-1]['pid'] if starts else manifest['pid']
        try:os.kill(pid,0)
        except ProcessLookupError:pass
        else:raise RuntimeError('Latest PID exists; ownership uncertain')
    else:CP.mkdir();exclusive(mp,dict(inputs=frozen,input_sha256=custody,host=socket.gethostname(),pid=os.getpid(),utc=utc()))
    began=time.perf_counter();receipt=dict(status='RUNNING',started_utc=utc(),pid=os.getpid(),host=socket.gethostname(),inputs=frozen,input_sha256=custody,Hamiltonians=[],checks=[],resume=resume,
        qualification='Supported reversible full-six BS10/BS11 record interaction and special pure content-coherence witness. No autonomous bath, irreversible sealing, extensive stability, physical clock/ruler/volume or gravitational/cosmological normalization.')
    event('run_start',resume=resume)
    def authenticated(path,kind,key):
        commits=[e for e in previous if e['event']==kind and e['key']==key]
        return bool(commits and commits[-1]['sha256']==sha(path))
    try:
        import numpy as np
        for ig,g in enumerate(GS):
            label='g'+str(ig);hp=CP/(label+'.json');receipt['next_unfinished']=dict(Hamiltonian=label,state='controls')
            if hp.exists():
                if not authenticated(hp,'Hamiltonian_complete',label):raise RuntimeError('Hamiltonian receipt mismatch')
                h=json.loads(hp.read_text())
                if h['input_sha256']!=custody:raise RuntimeError('Hamiltonian input mismatch')
                for bundle_name in {r['bundle_path'] for r in h['states']}:
                    references=[r for r in h['states'] if r['bundle_path']==bundle_name]
                    bundle=Path(bundle_name);key=label+'_n'+str(references[0]['start'])
                    if bundle.parent!=CP or not authenticated(bundle,'bundle_saved',key):
                        raise RuntimeError('Completed Hamiltonian bundle commit mismatch')
                    digest=sha(bundle)
                    if any(r['input_sha256']!=custody or r['bundle_sha256']!=digest for r in references):
                        raise RuntimeError('Completed Hamiltonian bundle input/hash mismatch')
                receipt['Hamiltonians'].append(h)
                if h['failed_count']:raise RuntimeError('Preserved failure forbids rerun')
                continue
            hbegan=time.perf_counter();f=fields(np,g);a=float(np.nextafter(4.375+.8+g+PAD,np.inf));coeff,coefficient_checks=coefficient_table(np,a)
            oldh=next(h for h in old['Hamiltonians'] if h['g']==g)
            controls=preflight(np,f,a,oldh,coeff)
            for item in coefficient_checks:check(controls,'certified_coefficients_'+item['key'],item['passed'],item)
            h=dict(g=g,input_sha256=custody,center=CENTER,halfwidth=a,coefficient_controls=coefficient_checks,checks=controls,states=[])
            cache={}
            for start in STARTS:
                bundle=CP/(label+'_n'+str(start)+'.bundle.npz')
                if bundle.exists():
                    commits=[e for e in previous if e['event']=='bundle_saved' and e['key']==label+'_n'+str(start)]
                    if not commits or commits[-1]['sha256']!=sha(bundle):
                        raise RuntimeError('Bundle lacks matching journal commit; manual recovery required')
                    with np.load(bundle,allow_pickle=False) as data:
                        if json.loads(str(data['input_sha256_json']))!=custody or float(data['g'])!=g or int(data['start'])!=start:raise RuntimeError('Bundle metadata mismatch')
                        states=data['full_states']
                    if states.shape!=(len(SCHEDULE),DIM) or not np.all(np.isfinite(states)):raise RuntimeError('Partial bundle')
                else:
                    states=propagate(np,lambda v:apply(np,f,v),DIM,start*384,a,coeff)
                    with bundle.open('xb') as out:
                        np.savez(out,full_states=states,input_sha256_json=json.dumps(custody,sort_keys=True),g=g,start=start,
                                 schedule_json=json.dumps(SCHEDULE));out.flush();os.fsync(out.fileno())
                    event('bundle_saved',key=label+'_n'+str(start),sha256=sha(bundle))
                for j,(timekey,tau,early) in enumerate(SCHEDULE):
                    key=label+'_n'+str(start)+'_'+timekey;rp=CP/(key+'.json');psi=states[j];cache[(start,timekey)]=psi.copy()
                    receipt['next_unfinished']=dict(Hamiltonian=label,state=key)
                    if rp.exists():
                        if not authenticated(rp,'state_complete',key):raise RuntimeError('State receipt mismatch')
                        row=json.loads(rp.read_text())
                        if row['input_sha256']!=custody or row['bundle_sha256']!=sha(bundle):raise RuntimeError('State input/bundle changed')
                    else:
                        row=observe(np,f,start,tau,early,psi)
                        row.update(input_sha256=custody,bundle_path=str(bundle),bundle_sha256=sha(bundle),bundle_index=j)
                        exclusive(rp,row);event('state_complete',key=key,sha256=sha(rp),failed=row['failed_count'])
                    h['states'].append(row)
                    if start==42:
                        error=float(np.max(np.abs(psi-cache[(21,timekey)][f['ref']])))
                        check(h['checks'],'trajectory_reflection_'+timekey,error<=OBS_TOL,dict(maximum=error))
                for j,tiny in enumerate(TINY):
                    plus=cache[(start,'early'+str(j)+'_plus')];minus=cache[(start,'early'+str(j)+'_minus')]
                    check(h['checks'],'time_reversal_'+str(start)+'_'+str(j),np.max(np.abs(minus-plus.conj()))<=OBS_TOL)
                del states
            elapsed=time.perf_counter()-hbegan;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            check(h['checks'],'Hamiltonian_under_60seconds',elapsed<MAX_SECONDS,dict(seconds=elapsed,limit=MAX_SECONDS))
            check(h['checks'],'peak_under_512MiB',peak<MAX_RSS,dict(peak_bytes=peak,limit_bytes=MAX_RSS))
            h.update(elapsed_seconds=elapsed,peak_RSS_bytes=peak);h['failed_count']=sum(not c['passed'] for c in h['checks'])+sum(r['failed_count'] for r in h['states'])
            exclusive(hp,h);event('Hamiltonian_complete',key=label,sha256=sha(hp),failed=h['failed_count']);receipt['Hamiltonians'].append(h)
            print(json.dumps(dict(event='Hamiltonian_complete',g=g,states=len(h['states']),failed=h['failed_count'],seconds=elapsed)),flush=True)
            del f,coeff,cache;gc.collect()
            if h['failed_count']:break
        _,final=anchors();check(receipt['checks'],'input_bytes_unchanged',final==custody)
        check(receipt['checks'],'two_Hamiltonians_44_states',len(receipt['Hamiltonians'])==2 and sum(len(h['states']) for h in receipt['Hamiltonians'])==44)
        failed=any(not c['passed'] for c in receipt['checks']) or any(h['failed_count'] for h in receipt['Hamiltonians'])
        receipt['status']='FAILED' if failed else 'QUALIFIED_ARITHMETIC';receipt['next_unfinished']=None if len(receipt['Hamiltonians'])==2 else dict(Hamiltonian='g1',state='controls')
    except Exception:
        receipt['status']='ERROR';receipt['exception']=traceback.format_exc();event('error',exception=receipt['exception'],next_unfinished=receipt.get('next_unfinished'))
    receipt['runtime_seconds']=time.perf_counter()-began;receipt['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;event('run_complete',status=receipt['status']);finish(receipt)
    return 0 if receipt['status']=='QUALIFIED_ARITHMETIC' else 1
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');p.add_argument('--resume',action='store_true');args=p.parse_args()
    if args.resume and not args.execute:p.error('--resume requires --execute and separate approval')
    if args.execute:return execute(args.resume)
    _,custody=anchors();print(json.dumps(dict(mode='describe_only',inputs=inputs(),input_sha256=custody),indent=2));return 0
if __name__=='__main__':sys.exit(main())
