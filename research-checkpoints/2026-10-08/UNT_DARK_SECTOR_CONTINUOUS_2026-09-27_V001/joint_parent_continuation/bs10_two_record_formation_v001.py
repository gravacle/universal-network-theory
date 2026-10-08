#!/usr/bin/env python3
"""New supported two-record BS10 unitary witness; see prospective protocol."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import gc
import hashlib
import json
import os
from pathlib import Path
import resource
import socket
import sys
import time
import traceback

ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
HERE=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
PROTOCOL=HERE/'BS10_TWO_RECORD_FORMATION_V001.md'
SOURCE=HERE/'bs10_two_record_formation_v001.py'
RESULT=HERE/'BS10_TWO_RECORD_FORMATION_V001_RESULT.json'
REPORT=HERE/'BS10_TWO_RECORD_FORMATION_V001_RESULT.md'
CP=HERE/'bs10_two_record_formation_v001_checkpoints'
COLD=HERE/'BS11_DYNAMIC_CARRIER_SOURCE_V001_RESULT.json'
THERMAL=HERE/'BS11_DYNAMIC_CARRIER_THERMAL_V001_RESULT.json'
NATIVE=ROOT/'program-worktree/LANE_GRA_BS_F3_QIRN_MICRO_ACTION_V001/MICRO_ACTION.md'
GS=(0.,.1);STARTS=(21,42);TIMES=(0.,1.,2.,5.,10.,20.,50.);TINY=(.001,.002)
UD,LR,LJ,ER,EP,HFLIP,THOP=1.,.5,.25,1.,1.,.1,.1
DIM=1536;OP_TOL,EIG_TOL,OBS_TOL,PSD_TOL=1e-11,2e-10,2e-10,1e-12
MAX_RSS,MAX_SECONDS=512*1024*1024,60.

def utc():return datetime.now(timezone.utc).isoformat()
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def exclusive(path,obj):
    with path.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def journal(kind,**data):
    with (CP/'events.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(event=kind,pid=os.getpid(),utc=utc(),**data),sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
def matrix_sha(np,a):return hashlib.sha256(np.ascontiguousarray(a,dtype='<f8').tobytes()).hexdigest()
def complex_json(a):return dict(real=a.real.tolist(),imag=a.imag.tolist())
def check(checks,name,ok,evidence=None):
    item=dict(name=name,passed=bool(ok))
    if evidence is not None:item['evidence']=evidence
    checks.append(item)
def inputs():return dict(dimension=DIM,U_d=UD,bare_Delta=0,d_star=2,Nc=1,
    dynamic_record_nodes=[0,3],record_bit_order='r0 bit0,r3 bit1; BB,xB,Bx,xx',
    epsilon_r=ER,epsilon_psi=EP,h=HFLIP,t=THOP,Omega=6*HFLIP,lambda_R=LR,lambda_J=LJ,
    g=list(GS),starts=list(STARTS),carrier_start=0,record_start='BB',times=list(TIMES),
    tiny_times=list(TINY),tiny_both_signs=True,early_relative_tolerance=1e-5,
    early_q3_bound='1e-8*g^2*tau^2+1e-20',all_other_copy_couplings=0,
    exterior_flips_hops='clamped off',exterior_carrier_record='blank',
    source='whole12node halfedge inclhop; local copy owned by its node',
    gamma='squared Uhlmann fidelity of9D two-content record states',
    operator_tolerance=OP_TOL,eigen_tolerance=EIG_TOL,observable_tolerance=OBS_TOL,
    density_PSD_tolerance=PSD_TOL,BLAS_threads=1,peak_RSS_limit_bytes=MAX_RSS,
    Hamiltonian_seconds_limit=MAX_SECONDS)
def anchors():
    cold=json.loads(COLD.read_text());old=next(r for r in cold['rows'] if r['case']['name']=='Nc1_q0')
    paths=[PROTOCOL,SOURCE,NATIVE,COLD,THERMAL,Path(old['array_path'])]
    paths += [Path(p) for p in cold['input_sha256']]
    result={str(p):sha(p) for p in paths}
    if result[str(Path(old['array_path']))]!=old['array_sha256']:raise RuntimeError('Cold Nc1 array custody changed')
    for p,h in cold['input_sha256'].items():
        if result[p]!=h:raise RuntimeError('Cold anchor changed: '+p)
    if cold['status']!='QUALIFIED_ARITHMETIC':raise RuntimeError('Cold reference unqualified')
    if json.loads(THERMAL.read_text())['status']!='QUALIFIED_ARITHMETIC':raise RuntimeError('Thermal reference unqualified')
    return result,old

def basis(np):
    rows=np.arange(DIM);ns=rows//24;carrier=(rows//4)%6;r=rows%4
    nb=np.array([[(n>>e)&1 for e in range(6)] for n in range(64)],dtype=float)
    p=np.eye(6)[carrier];q=np.zeros((DIM,6));q[:,0]=r&1;q[:,3]=(r>>1)&1
    pos=np.array([(np.cos(2*np.pi*v/6),np.sin(2*np.pi*v/6)) for v in range(6)])
    reflected_n=np.array([sum(((int(n)>>e)&1)<<((-e-1)%6) for e in range(6)) for n in ns])
    reflection=(reflected_n*6+((-carrier)%6))*4+r
    links={};transfers={};copies={}
    for e in range(6):
        links[e]=(rows,((ns^(1<<e))*6+carrier)*4+r)
        use=(nb[ns,e]==1)&((carrier==e)|(carrier==(e+1)%6));src=rows[use]
        newcarrier=np.where(carrier[use]==e,(e+1)%6,e)
        transfers[e]=(src,(ns[use]*6+newcarrier)*4+r[use])
    for bit,v in enumerate((0,3)):
        src=rows[carrier==v];copies[v]=(src,(ns[src]*6+carrier[src])*4+(r[src]^(1<<bit)))
    return dict(rows=rows,ns=ns,carrier=carrier,r=r,nb=nb,p=p,q=q,pos=pos,
                allpos=np.vstack([pos,2*pos]),reflection=reflection,
                links=links,transfers=transfers,copies=copies)

def build(np,g,s):
    H=np.zeros((DIM,DIM));G=[np.zeros_like(H),np.zeros_like(H)]
    diagonal=np.zeros(DIM);gd=np.zeros((DIM,2));parts={}
    degree=np.array([1+s['nb'][s['ns'],(v-1)%6]+s['nb'][s['ns'],v] for v in range(6)]).T
    parts['active_degree']=UD*np.sum((degree-2)**2,axis=1)
    parts['exterior_degree']=np.full(DIM,6*UD)
    parts['carrier_storage']=np.full(DIM,EP)
    parts['external_current_square']=np.full(DIM,LJ)
    parts['record_storage']=ER*s['q'].sum(axis=1)
    parts['external_record_feedback']=-LR*s['q'].sum(axis=1)
    parts['internal_current_square']=np.zeros(DIM);parts['internal_record_feedback']=np.zeros(DIM)
    for v in range(6):
        onsite=UD*(degree[:,v]-2)**2+ER*s['q'][:,v]+EP*s['p'][:,v]
        ext=LJ*s['p'][:,v]-LR*s['q'][:,v]
        diagonal+=onsite+UD+ext
        gd+=(onsite+2*UD+1.5*ext)[:,None]*s['pos'][v]
    for e in range(6):
        nxt=(e+1)%6;w=(s['pos'][e]+s['pos'][nxt])/2;n=s['nb'][s['ns'],e]
        a=s['p'][:,e]+s['p'][:,nxt]-2*s['p'][:,e]*s['p'][:,nxt]
        current=LJ*n*a;records=-LR*n*(s['q'][:,e]+s['q'][:,nxt])
        parts['internal_current_square']+=current;parts['internal_record_feedback']+=records
        diagonal+=current+records;gd+=(current+records)[:,None]*w
        for mapping,coefficient in [(s['links'][e],-HFLIP),(s['transfers'][e],-THOP)]:
            src,dst=mapping;H[src,dst]+=coefficient
            for i in range(2):G[i][src,dst]+=coefficient*w[i]
    for v,mapping in s['copies'].items():
        src,dst=mapping;H[src,dst]+=g
        for i in range(2):G[i][src,dst]+=g*s['pos'][v,i]
    H[s['rows'],s['rows']]=diagonal
    for i in range(2):G[i][s['rows'],s['rows']]=gd[:,i]
    return H,G,parts,degree

def weighted(np,g,s,lapses):
    value=np.zeros((DIM,DIM));diag=np.zeros(DIM)
    for v in range(6):
        degree=1+s['nb'][s['ns'],(v-1)%6]+s['nb'][s['ns'],v]
        diag+=lapses[v]*(UD*(degree-2)**2+ER*s['q'][:,v]+EP*s['p'][:,v])
        diag+=lapses[v+6]*UD+(lapses[v]+lapses[v+6])/2*(LJ*s['p'][:,v]-LR*s['q'][:,v])
    for e in range(6):
        nxt=(e+1)%6;weight=(lapses[e]+lapses[nxt])/2;n=s['nb'][s['ns'],e]
        a=s['p'][:,e]+s['p'][:,nxt]-2*s['p'][:,e]*s['p'][:,nxt]
        diag+=weight*n*(LJ*a-LR*(s['q'][:,e]+s['q'][:,nxt]))
        for mapping,coefficient in [(s['links'][e],-HFLIP),(s['transfers'][e],-THOP)]:
            src,dst=mapping;value[src,dst]+=weight*coefficient
    for v,(src,dst) in s['copies'].items():value[src,dst]+=g*lapses[v]
    value[s['rows'],s['rows']]=diag
    return value

def preflight(np,g,s,H,G,E,V,old):
    checks=[];scale=max(1.,float(np.max(np.sum(np.abs(H),axis=1))))
    # Independent original qutrit-copy/content-exchange controls, before the
    # closed {B,x} restriction used by either content trajectory.
    content_swap=np.array([[1.,0.,0.],[0.,0.,1.],[0.,1.,0.]])
    swap=np.kron(content_swap,content_swap);copy=np.zeros((9,9));transfer=np.zeros((9,9))
    for x in (1,2):
        copy[3*x+x,3*x]=copy[3*x,3*x+x]=1.
        transfer[x,3*x]=transfer[3*x,x]=1.
    check(checks,'physical_BS08_content_exchange',np.max(np.abs(swap@copy@swap.T-copy))<=OP_TOL)
    check(checks,'physical_BS07_content_exchange',np.max(np.abs(swap@transfer@swap.T-transfer))<=OP_TOL)
    for n in STARTS:
        seed=n*24;action=H[:,seed]
        q0_coefficient=float(s['q'][:,0]@(action**2))
        q3_coefficient=float(s['q'][:,3]@(action**2))
        unblank_coefficient=float((s['r']!=0).astype(float)@(action**2))
        check(checks,'seed_copy_positive_sign_'+str(n),abs(float(H[seed+1,seed])-g)<=OP_TOL)
        check(checks,'seed_q0_exact_quadratic_'+str(n),abs(q0_coefficient-g*g)<=OP_TOL)
        check(checks,'seed_q3_exact_quadratic_null_'+str(n),abs(q3_coefficient)<=OP_TOL)
        check(checks,'seed_PBB_exact_quadratic_'+str(n),abs(unblank_coefficient-g*g)<=OP_TOL)
    for name,a in [('H',H),('Gx',G[0]),('Gy',G[1])]:check(checks,name+'_Hermitian',np.max(np.abs(a-a.T))<=OP_TOL)
    check(checks,'node_source_sum',np.max(np.abs(weighted(np,g,s,np.ones(12))-H))<=OP_TOL)
    eta=np.array([1e-6,-2e-6]);lapses=1+s['allpos']@eta
    check(checks,'positive_source_arm',np.min(lapses)>0)
    check(checks,'affine_weighted_source',np.max(np.abs(weighted(np,g,s,lapses)-H-eta[0]*G[0]-eta[1]*G[1]))<=OP_TOL)
    check(checks,'uniform_lapse',np.max(np.abs(weighted(np,g,s,np.full(12,.93))-.93*H))<=OP_TOL)
    ref=s['reflection']
    check(checks,'reflection_H',np.max(np.abs(H[np.ix_(ref,ref)]-H))<=OP_TOL)
    check(checks,'reflection_Gx_even',np.max(np.abs(G[0][np.ix_(ref,ref)]-G[0]))<=OP_TOL)
    check(checks,'reflection_Gy_odd',np.max(np.abs(G[1][np.ix_(ref,ref)]+G[1]))<=OP_TOL)
    check(checks,'reflection_swaps_fixed_starts',int(ref[21*24])==42*24 and int(ref[42*24])==21*24)
    residual=orth=0.
    for start in range(0,DIM,128):
        stop=min(start+128,DIM);block=V[:,start:stop]
        residual=max(residual,float(np.max(np.abs(H@block-block*E[start:stop]))))
        product=V.T@block;product[np.arange(start,stop),np.arange(stop-start)]-=1
        orth=max(orth,float(np.max(np.abs(product))))
    check(checks,'full_new_eigen_residual',residual<=EIG_TOL*scale,dict(maximum=residual,tolerance=EIG_TOL*scale))
    check(checks,'full_orthonormality',orth<=EIG_TOL,dict(maximum=orth))
    with np.load(old['array_path'],allow_pickle=False) as saved:ov=saved['eigenvectors_columns'];oe=saved['complete_eigenvalues']
    oldH=(ov*oe)@ov.T;select=np.arange(384)*4
    difference=float(np.max(np.abs(H[np.ix_(select,select)]-oldH)))
    check(checks,'sealed_dynamic_Nc1_BB_block',difference<=OP_TOL,dict(maximum=difference))
    oldt=np.array(old['all_excited_source_transition_vectors']);oldmean=np.array(old['ground_source_mean'])
    for i in range(2):
        expected=ov[:,1:]@oldt[:,i]+oldmean[i]*ov[:,0]
        difference=float(np.max(np.abs(G[i][np.ix_(select,select)]@ov[:,0]-expected)))
        check(checks,'sealed_dynamic_source_action_'+str(i),difference<=OBS_TOL,dict(maximum=difference))
    return checks,scale

def expectation(np,psi,mapping):
    src,dst=mapping;return float(np.real(np.vdot(psi[src],psi[dst])))
def density(np,psi):
    a=psi.reshape(384,4);return a.T@a.conj()
def embedded(np,rho,x):
    occupied=x+1;targets=[0,3*occupied,occupied,4*occupied]
    value=np.zeros((9,9),dtype=complex);value[np.ix_(targets,targets)]=rho
    return value
def sqrt_density(np,rho):
    vals,V=np.linalg.eigh(rho)
    if vals[0]<-PSD_TOL:raise ArithmeticError('Density violates frozen PSD tolerance')
    root=(V*np.sqrt(np.maximum(vals,0)))@V.conj().T
    return root,dict(all_eigenvalues=vals.tolist(),negative_clip_count=int(np.sum(vals<0)),minimum=float(vals[0]),
                     square_root_residual=float(np.max(np.abs(root@root-rho))))

def observe(np,g,n,tau,psi,s,H,G,parts,degree,early):
    checks=[];prob=np.abs(psi)**2;rho=density(np,psi);p_record=np.real(np.diag(rho));PBB=float(p_record[0])
    check(checks,'full_state_normalized',abs(float(prob.sum())-1)<=OBS_TOL)
    check(checks,'record_density_trace',abs(complex(np.trace(rho))-1)<=OBS_TOL)
    check(checks,'record_density_Hermitian',np.max(np.abs(rho-rho.conj().T))<=OBS_TOL)
    eig=np.linalg.eigvalsh(rho);check(checks,'record_density_PSD',float(eig[0])>=-PSD_TOL)
    rhos=[embedded(np,rho,x) for x in (0,1)];roots=[];details=[]
    for rr in rhos:
        root,info=sqrt_density(np,rr);roots.append(root);details.append(info)
        check(checks,'density_root_residual_'+str(len(details)),info['square_root_residual']<=OBS_TOL)
    singular=np.linalg.svd(roots[0]@roots[1],compute_uv=False)
    fidelity=float(np.sum(singular)**2);gamma=PBB**2
    check(checks,'9D_squared_fidelity_equals_PBB_squared',abs(fidelity-gamma)<=OBS_TOL,
          dict(independent=fidelity,exact_probability=gamma,difference=fidelity-gamma))
    qmean=prob@s['q'];pmean=prob@s['p'];nmean=prob@s['nb'][s['ns']]
    dmean=prob@degree;energies={name:float(prob@a) for name,a in parts.items()}
    energies['incidence_flip']=-HFLIP*sum(expectation(np,psi,a) for a in s['links'].values())
    energies['carrier_hopping']=-THOP*sum(expectation(np,psi,a) for a in s['transfers'].values())
    energies['record_copy']=g*sum(expectation(np,psi,a) for a in s['copies'].values())
    total=float(np.real(np.vdot(psi,H@psi)));initial=float(H[n*24,n*24])
    check(checks,'complete_energy_components',abs(sum(energies.values())-total)<=OBS_TOL*max(1.,abs(total)))
    check(checks,'unitary_energy_conserved',abs(total-initial)<=OBS_TOL*max(1.,abs(initial)))
    check(checks,'carrier_count_conserved',abs(float(pmean.sum())-1)<=OBS_TOL)
    check(checks,'record_probability_bounds',float(p_record.min())>=-OBS_TOL and float(p_record.max())<=1+OBS_TOL)
    if g==0:
        check(checks,'null_copy_records_blank',float(qmean.sum())<=OBS_TOL and abs(PBB-1)<=OBS_TOL)
        check(checks,'null_copy_gamma_one',abs(gamma-1)<=OBS_TOL)
    if early and g!=0:
        leading=g*g*tau*tau
        for label,ratio in [('q0',float(qmean[0])/leading),('PBB',(1-PBB)/leading),('gamma',(1-gamma)/(2*leading))]:
            check(checks,'early_'+label+'_coefficient',abs(ratio-1)<=1e-5,dict(ratio=ratio,tolerance=1e-5))
        check(checks,'early_q3_no_tau_squared',float(qmean[3])<=1e-8*leading+1e-20,
              dict(q3=float(qmean[3]),limit=1e-8*leading+1e-20))
    positive=eig[eig>0];entropy=float(-np.sum(positive*np.log(positive)))
    return dict(g=g,start=n,tau=tau,auxiliary_early_arm=early,record_probabilities=p_record.tolist(),
        record_mean=qmean.tolist(),carrier_mean=pmean.tolist(),incidence_mean=nmean.tolist(),degree_mean=dmean.tolist(),
        P_BB=PBB,gamma_rec_probability=gamma,gamma_rec_independent_9D=fidelity,
        record_density4=complex_json(rho),physical_record_density9_content0=complex_json(rhos[0]),
        physical_record_density9_content1=complex_json(rhos[1]),record_density_eigenvalues=eig.tolist(),
        record_reduced_entropy=entropy,fidelity_square_root_diagnostics=details,
        fidelity_singular_values=singular.tolist(),complete_energy=total,initial_complete_energy=initial,
        complete_energy_components=energies,complete_source_mean=[float(np.real(np.vdot(psi,a@psi))) for a in G],
        checks=checks,passed_count=sum(c['passed'] for c in checks),failed_count=sum(not c['passed'] for c in checks))

def finish(receipt):
    checks=receipt['checks'][:]
    for h in receipt['Hamiltonians']:
        checks+=h['checks']
        for row in h['states']:checks+=row['checks']
    receipt['check_count']=len(checks);receipt['passed_count']=sum(c['passed'] for c in checks)
    receipt['failed_count']=len(checks)-receipt['passed_count'];receipt['completed_utc']=utc()
    payload=(json.dumps(receipt,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with RESULT.open('xb') as f:f.write(payload)
    digest=hashlib.sha256(payload).hexdigest()
    lines=['# BS10 two-record formation V001: saved result','',f"Status {receipt['status']}; checks {receipt['passed_count']}/{receipt['check_count']}; failures {receipt['failed_count']}.",'',receipt['qualification'],'',
        '| g | ice start | tau | q0 | q3 | PBB | gamma_rec | reduced entropy |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for h in receipt['Hamiltonians']:
        for r in h['states']:
            if r['auxiliary_early_arm']:continue
            lines.append(f"| {r['g']:.2f} | {r['start']} | {r['tau']:.6g} | {r['record_mean'][0]:.12g} | {r['record_mean'][3]:.12g} | {r['P_BB']:.12g} | {r['gamma_rec_probability']:.12g} | {r['record_reduced_entropy']:.9g} |")
    lines+=['','Complete unrounded densities, all states, native energy/source decomposition, null-copy controls, independent9D fidelity and early-time/reflection checks are saved. Gamma is record-subsystem squared fidelity, not an inserted energy or proof of irreversible sealing.','',
        f"Runtime {receipt['runtime_seconds']:.6g}s; peak RSS {receipt['peak_RSS_bytes']} bytes; PID {receipt['pid']}.",'',f'Result JSON SHA256: {digest}','',f"Exact unfinished work: {receipt.get('next_unfinished')}",'','Input SHA256 custody:']
    lines+=['- '+p+': '+h for p,h in receipt['input_sha256'].items()]
    with REPORT.open('x',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
    print(json.dumps(dict(status=receipt['status'],Hamiltonians=len(receipt['Hamiltonians']),
        states=sum(len(h['states']) for h in receipt['Hamiltonians']),checks=receipt['check_count'],
        passed=receipt['passed_count'],failed=receipt['failed_count'],runtime_seconds=receipt['runtime_seconds'],
        peak_RSS_bytes=receipt['peak_RSS_bytes'],json_sha256=digest,json_path=str(RESULT),markdown_path=str(REPORT),
        next_unfinished=receipt.get('next_unfinished'),exception=receipt.get('exception')),indent=2))

def execute(resume):
    if sys.platform!='darwin' or SOURCE.resolve()!=Path(__file__).resolve():raise RuntimeError('Wrong Mac/source context')
    if RESULT.exists() or REPORT.exists():raise FileExistsError('Final output exists; no overwrite/replay')
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
    custody,old=anchors();frozen=inputs();previous=[];mp=CP/'manifest.json'
    if resume:
        manifest=json.loads(mp.read_text());previous=[json.loads(x) for x in (CP/'events.jsonl').read_text().splitlines()]
        if manifest['input_sha256']!=custody or manifest['inputs']!=frozen or manifest['host']!=socket.gethostname():raise RuntimeError('Manifest custody mismatch')
        starts=[e for e in previous if e['event']=='run_start'];pid=starts[-1]['pid'] if starts else manifest['pid']
        try:os.kill(pid,0)
        except ProcessLookupError:pass
        else:raise RuntimeError('Latest worker PID exists; ownership uncertain')
    else:CP.mkdir();exclusive(mp,dict(input_sha256=custody,inputs=frozen,host=socket.gethostname(),pid=os.getpid(),utc=utc()))
    began=time.perf_counter();receipt=dict(status='RUNNING',started_utc=utc(),pid=os.getpid(),host=socket.gethostname(),
        input_sha256=custody,inputs=frozen,Hamiltonians=[],checks=[],resume=resume,
        qualification='Prepared supported reversible BS10 record formation with the original label-blind BS11 feedback; records are content-distinguishable only within this finite witness. No irreversible sealing, derived bath, extensive stability, physical clock/ruler/volume, gravity or cosmological phase.')
    journal('run_start',resume=resume)
    def authenticated(path,kind,key):
        commits=[e for e in previous if e['event']==kind and e['key']==key]
        return bool(commits and commits[-1]['sha256']==sha(path))
    try:
        import numpy as np
        s=basis(np)
        for ig,g in enumerate(GS):
            label='g'+str(ig);receipt['next_unfinished']=dict(Hamiltonian=label,state='eigensystem')
            hp=CP/(label+'.json');ep=CP/(label+'.eigensystem.npz');sp=CP/(label+'.started.json')
            if hp.exists():
                if not authenticated(hp,'Hamiltonian_complete',label):raise RuntimeError('Hamiltonian commit mismatch')
                h=json.loads(hp.read_text())
                if h['input_sha256']!=custody or h['eigensystem_sha256']!=sha(ep):raise RuntimeError('Hamiltonian custody mismatch')
                receipt['Hamiltonians'].append(h)
                if h['failed_count']:raise RuntimeError('Preserved failure forbids rerun')
                continue
            if sp.exists() and not ep.exists():raise RuntimeError('Begun Hamiltonian lacks recoverable eigensystem; parent decision needed')
            if not sp.exists():exclusive(sp,dict(g=g,input_sha256=custody,pid=os.getpid(),utc=utc()))
            hbegan=time.perf_counter();H,G,parts,degree=build(np,g,s)
            matrices={name:matrix_sha(np,a) for name,a in [('H',H),('Gx',G[0]),('Gy',G[1])]}
            if ep.exists():
                commits=[e for e in previous if e['event']=='eigensystem_saved' and e['key']==label]
                if commits and commits[-1]['sha256']!=sha(ep):raise RuntimeError('Eigensystem journal mismatch')
                with np.load(ep,allow_pickle=False) as data:
                    if json.loads(str(data['input_sha256_json']))!=custody or json.loads(str(data['matrix_sha256_json']))!=matrices:raise RuntimeError('Eigensystem metadata mismatch')
                    E=data['complete_eigenvalues'];V=data['eigenvectors_columns']
            else:
                journal('new_solve_start',key=label,g=g,matrix_sha256=matrices)
                H[s['rows'],s['rows']]-=7.25;centered,V=np.linalg.eigh(H);H[s['rows'],s['rows']]+=7.25;E=centered+7.25
                with ep.open('xb') as f:
                    np.savez(f,complete_eigenvalues=E,eigenvectors_columns=V,
                             input_sha256_json=json.dumps(custody,sort_keys=True),matrix_sha256_json=json.dumps(matrices,sort_keys=True),g=g)
                    f.flush();os.fsync(f.fileno())
                journal('eigensystem_saved',key=label,sha256=sha(ep))
            controls,scale=preflight(np,g,s,H,G,E,V,old)
            h=dict(g=g,input_sha256=custody,matrix_sha256=matrices,eigensystem_path=str(ep),eigensystem_sha256=sha(ep),checks=controls,states=[])
            state_cache={}
            for n in STARTS:
                coefficients=V[n*24,:]
                schedule=[('main'+str(j),tau,False) for j,tau in enumerate(TIMES)]
                schedule += [('early'+str(j)+'_'+sign,sgn*tau,True) for j,tau in enumerate(TINY) for sign,sgn in [('plus',1),('minus',-1)]]
                for timekey,tau,early in schedule:
                    key=label+'_n'+str(n)+'_'+timekey;rp=CP/(key+'.json');ap=CP/(key+'.state.npz')
                    receipt['next_unfinished']=dict(Hamiltonian=label,state=key)
                    if rp.exists():
                        if not authenticated(rp,'state_complete',key):raise RuntimeError('State journal mismatch')
                        row=json.loads(rp.read_text())
                        if row['input_sha256']!=custody or row['state_sha256']!=sha(ap):raise RuntimeError('State source custody mismatch')
                        with np.load(ap,allow_pickle=False) as data:psi=data['complete_state']
                    else:
                        if ap.exists():
                            with np.load(ap,allow_pickle=False) as data:
                                if json.loads(str(data['input_sha256_json']))!=custody or str(data['eigensystem_sha256'])!=h['eigensystem_sha256'] \
                                    or float(data['tau'])!=tau or int(data['start'])!=n:raise RuntimeError('Orphan state custody mismatch')
                                psi=data['complete_state']
                        else:
                            psi=V@(coefficients*np.exp(-1j*E*tau))
                            with ap.open('xb') as f:
                                np.savez(f,complete_state=psi,input_sha256_json=json.dumps(custody,sort_keys=True),
                                         eigensystem_sha256=h['eigensystem_sha256'],tau=tau,start=n,g=g)
                                f.flush();os.fsync(f.fileno())
                        row=observe(np,g,n,tau,psi,s,H,G,parts,degree,early)
                        row.update(input_sha256=custody,state_path=str(ap),state_sha256=sha(ap),eigensystem_sha256=h['eigensystem_sha256'])
                        exclusive(rp,row);journal('state_complete',key=key,sha256=sha(rp),failed=row['failed_count'])
                    h['states'].append(row);state_cache[(n,timekey)]=psi
                    if n==42:
                        error=float(np.max(np.abs(psi-state_cache[(21,timekey)][s['reflection']])))
                        check(h['checks'],'trajectory_reflection_'+timekey,error<=OBS_TOL,dict(maximum=error))
                for j,tau in enumerate(TINY):
                    positive=state_cache[(n,'early'+str(j)+'_plus')];negative=state_cache[(n,'early'+str(j)+'_minus')]
                    check(h['checks'],'real_H_time_reversal_n'+str(n)+'_'+str(j),np.max(np.abs(negative-positive.conj()))<=OBS_TOL)
                    check(h['checks'],'diagonal_evenness_n'+str(n)+'_'+str(j),np.max(np.abs(np.abs(negative)**2-np.abs(positive)**2))<=OBS_TOL)
            elapsed=time.perf_counter()-hbegan;peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            check(h['checks'],'Hamiltonian_under_60seconds',elapsed<MAX_SECONDS,dict(seconds=elapsed,limit=MAX_SECONDS))
            check(h['checks'],'peak_under_512MiB',peak<MAX_RSS,dict(peak_bytes=peak,limit_bytes=MAX_RSS))
            h.update(elapsed_seconds=elapsed,peak_RSS_bytes=peak)
            h['failed_count']=sum(not c['passed'] for c in h['checks'])+sum(r['failed_count'] for r in h['states'])
            exclusive(hp,h);journal('Hamiltonian_complete',key=label,sha256=sha(hp),failed=h['failed_count'])
            receipt['Hamiltonians'].append(h)
            print(json.dumps(dict(event='Hamiltonian_complete',g=g,states=len(h['states']),failed=h['failed_count'],seconds=elapsed,peak_RSS_bytes=peak)),flush=True)
            del H,G,E,V,parts,degree,state_cache;gc.collect()
            if h['failed_count']:break
        finalanchors,_=anchors();check(receipt['checks'],'input_bytes_unchanged',finalanchors==custody)
        check(receipt['checks'],'two_Hamiltonians_44_states',len(receipt['Hamiltonians'])==2 and sum(len(h['states']) for h in receipt['Hamiltonians'])==44)
        failed=any(not c['passed'] for c in receipt['checks']) or any(h['failed_count'] for h in receipt['Hamiltonians'])
        receipt['status']='FAILED' if failed else 'QUALIFIED_ARITHMETIC'
        receipt['next_unfinished']=None if len(receipt['Hamiltonians'])==2 else dict(Hamiltonian='g1',state='eigensystem')
    except Exception:
        receipt['status']='ERROR';receipt['exception']=traceback.format_exc();journal('error',exception=receipt['exception'],next_unfinished=receipt.get('next_unfinished'))
    receipt['runtime_seconds']=time.perf_counter()-began;receipt['peak_RSS_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    journal('run_complete',status=receipt['status']);finish(receipt)
    return 0 if receipt['status']=='QUALIFIED_ARITHMETIC' else 1

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');p.add_argument('--resume',action='store_true');args=p.parse_args()
    if args.resume and not args.execute:p.error('--resume requires --execute and separate approval')
    if args.execute:return execute(args.resume)
    custody,_=anchors();print(json.dumps(dict(mode='describe_only',inputs=inputs(),input_sha256=custody),indent=2));return 0
if __name__=='__main__':sys.exit(main())
