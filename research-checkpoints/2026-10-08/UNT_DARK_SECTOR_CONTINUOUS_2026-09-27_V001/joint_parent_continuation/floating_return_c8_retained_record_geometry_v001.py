#!/usr/bin/env python3
"""NEW single-bond release; root-owned exact --execute or manual --resume only."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
import sys, json, hashlib, math, time, resource, traceback
from pathlib import Path
from fractions import Fraction as F
import numpy as np

J=Path(__file__).resolve().parent
ROOT=J.parent.parent
NAME='FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001'
PARENT='FLOATING_RETURN_C8_FORMATION_CLOCK_V001'
PCP=J/'floating_return_c8_formation_clock_v001_checkpoints'
CP=J/'floating_return_c8_retained_record_geometry_v001_checkpoints'
RESULT=J/(NAME+'_RESULT.json'); REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json'); ERROR=J/(NAME+'_ERROR.json')
PINS={
    NAME+'.md':'8f3dc32381e76a4e6badfe23fff6c8bdd4830cb32ed0aff99b1aef57eba5ce5b',
    PARENT+'.md':'eb04c848f360295df81c18240a2617c18a152190c1b6caa1a38abba3d2a08cbc',
    'floating_return_c8_formation_clock_v001.py':'7a6b06343be8258370274f250b6d72a08bcb60cff000bbc090a98c4f093521df',
    PARENT+'_RESULT.json':'08ec6908d430536cf64fa5d1445e8ae95831515a5dfbdb9c318c029ab6409a43',
    PARENT+'_RESULT.md':'ea04a83997cfef4aac580cdb31d6c3469a9a16ee7b7f6771feaa1e9b440940d8',
    PARENT+'_RECEIPT.json':'a01f7b80aeb90c2fa568536279607d1e514c3f4922db475220eeae7c9357f6ef',
    PARENT+'_AUDIT.json':'cbf95d3678aff4ba91ad8ca2acff196394d38174fd8cb746b425d69bdce39d6b',
    'FLOATING_RETURN_C8_LOCAL_CLOCK_COROLLARY_V001.md':'33db858f6d30f721c0c15d536a7432c206eb1a6964b2814aa25e3a4f28a8ce34',
    'FLOATING_RETURN_FORMED_RECORD_CLOCK_V001.md':'c83417ce29e8ea89be71c78510e27a0eff3d8a0bfacfcc507118ccb618ab449d',
}
ARS=(F(0),F(1,8),F(7,40),F(1,4))
TIMES=(F(0),F(1,10),F(1,5),F(2,5),F(4,5),F(1),F(2),F(4),F(8),F(12),F(16),F(24),F(32))
CYCLE=(0,4,3,7,2,6,1,5)
HFLIP=F(1,5); THOP=F(1,10); JCUR=F(1,4); LAM=F(1,2); BASE=F(19,2)
WORDS=np.arange(256,dtype=np.int64)
BITS=np.array([[(int(r)>>v)&1 for r in WORDS] for v in range(8)],dtype=np.int64)
POP=BITS.sum(0); END_SUM=BITS[0]+BITS[4]
QFLIP=np.array([WORDS^(1<<v) for v in range(8)])
CYCTOGLOBAL=np.array([sum(((int(r)>>j)&1)<<CYCLE[j] for j in range(8)) for r in WORDS])
GLOBALTOCYC=np.argsort(CYCTOGLOBAL)
GLOBALTOPOS=np.argsort(CYCLE)
ETA=np.array([1,1,1,1,-1,-1,-1,-1]); KWORD=ETA@BITS
ENDMASK=np.array([1,0,0,0,1,0,0,0],dtype=np.int64)
CHECKS=[]; INPUTS={}; COMMITS={}; APPEND_ALLOWED=False
ACTIVE={'preparation':None,'release_time':None,'stage':'unstarted'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text())
def clean(v):
    if isinstance(v,np.ndarray): return clean(v.tolist())
    if isinstance(v,np.generic): return clean(v.item())
    if isinstance(v,dict): return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [clean(x) for x in v]
    if isinstance(v,complex): return [clean(float(v.real)),clean(float(v.imag))]
    if isinstance(v,float) and not math.isfinite(v): return {'nonfinite':repr(v)}
    return v
def blob(v): return json.dumps(clean(v),sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def write_json(p,v):
    with Path(p).open('xb') as f:
        f.write(json.dumps(clean(v),sort_keys=True,indent=2,allow_nan=False).encode()+b'\n'); f.flush(); os.fsync(f.fileno())
    return sha(p)
def save_npz(p,**a):
    with Path(p).open('xb') as f:
        np.savez_compressed(f,**a); f.flush(); os.fsync(f.fileno())
    return sha(p)
def event(v):
    with (CP/'journal.jsonl').open('ab') as f:
        f.write(blob(v)+b'\n'); f.flush(); os.fsync(f.fileno())
def commit(p,v,event_name):
    h=write_json(p,v); event({'event':event_name,'file':Path(p).name,'sha256':h}); COMMITS[Path(p).name]=h; return h
def commit_npz(p,event_name,**arrays):
    h=save_npz(p,**arrays); event({'event':event_name,'file':Path(p).name,'sha256':h}); COMMITS[Path(p).name]=h; return h
def gate(name,a,b=0.,tol=1e-9):
    a,b=np.asarray(a),np.asarray(b); ok=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
    e=float(np.max(abs(a-b))) if ok else float('inf')
    CHECKS.append({'name':name,'error':clean(e),'tolerance':tol,'passed':ok and e<=tol})
def exact(name,b): CHECKS.append({'name':name,'passed':bool(b),'exact':True})
def rate(b,bd):
    d=float(abs(b)**2); return None if d==0 else float((np.conj(b)*bd).imag/d)
def input_identity(): return hashlib.sha256(blob(INPUTS)).hexdigest()
def complex_value(v):
    a=np.asarray(v,dtype=float); return a[...,0]+1j*a[...,1]

def authenticate_parent():
    for f,h in PINS.items():
        if sha(J/f)!=h: raise RuntimeError('frozen direct input mismatch: '+f)
        INPUTS[str((J/f).relative_to(ROOT))]=h
    pr=read(J/(PARENT+'_RESULT.json')); rr=read(J/(PARENT+'_RECEIPT.json'))
    if rr['result_raw_sha256']!=sha(J/(PARENT+'_RESULT.json')) or rr['result_canonical_sha256']!=hashlib.sha256(blob(pr)).hexdigest():
        raise RuntimeError('parent result raw/canonical mismatch')
    if rr['report_sha256']!=sha(J/(PARENT+'_RESULT.md')) or pr['passed']!=6205 or pr['failed']!=0 or rr['passed']!=6205 or rr['failed']!=0:
        raise RuntimeError('parent report/status mismatch')
    if pr['input_sha256']!=rr['input_sha256'] or not all(c['passed'] for c in pr['checks']): raise RuntimeError('parent checks/inputs')
    for f,h in rr['input_sha256'].items():
        if sha(ROOT/f)!=h: raise RuntimeError('parent inherited input mismatch: '+f)
        INPUTS[f]=h
    if len(rr['checkpoint_sha256'])!=225 or set(rr['checkpoint_sha256'])!={p.name for p in PCP.iterdir() if p.name!='journal.jsonl'}:
        raise RuntimeError('parent checkpoint census')
    for f,h in rr['checkpoint_sha256'].items():
        if sha(PCP/f)!=h: raise RuntimeError('parent checkpoint mismatch: '+f)
        INPUTS[str((PCP/f).relative_to(ROOT))]=h
    jr=(PCP/'journal.jsonl').read_bytes(); es=[json.loads(x) for x in jr.splitlines()]
    if len(es)!=124 or hashlib.sha256(b'\n'.join(jr.splitlines()[:-1])+b'\n').hexdigest()!=rr['journal_prefix_sha256']:
        raise RuntimeError('parent journal prefix/census')
    if es[-1]!={'event':'receipt_saved','sha256':sha(J/(PARENT+'_RECEIPT.json'))}:
        raise RuntimeError('parent receipt commit')
    if es[-3]!={'event':'result_saved','raw_sha256':rr['result_raw_sha256'],'canonical_sha256':rr['result_canonical_sha256']} or es[-2]!={'event':'report_saved','sha256':rr['report_sha256'],'data_rows':104}:
        raise RuntimeError('parent result/report commits')
    pm=read(PCP/'manifest.json')
    if es[0]['manifest_sha256']!=sha(PCP/'manifest.json') or es[0]['input_sha256']!=rr['input_sha256'] or pm['input_sha256']!=rr['input_sha256'] or pm['PID']!=rr['PID'] or pr['manifest_sha256']!=sha(PCP/'manifest.json'):
        raise RuntimeError('parent manifest/start')
    ei=1
    for ci,c in enumerate(pr['cases']):
        label='case%02d'%ci
        if c['case']!=label or len(c['rows'])!=13 or c['input_sha256']!=rr['input_sha256'] or read(PCP/(label+'_complete.json'))!=c:
            raise RuntimeError('parent case custody')
        if es[ei]!={'event':'eigensystem_saved','case':label,'file':label+'_eigensystem.npz','sha256':c['eigensystem_sha256']}:
            raise RuntimeError('parent eigen commit')
        ei+=1
        for ti,row in enumerate(c['rows']):
            fn=label+'_frame%02d.json'%ti
            if row['time_index']!=ti or row['x_rational']!=str(TIMES[ti]) or row['input_sha256']!=rr['input_sha256'] or read(PCP/fn)!=row:
                raise RuntimeError('parent frame metadata')
            expected={'event':'frame_saved','case':label,'time_index':ti,'state':row['state_file'],'state_sha256':row['state_sha256'],'row':fn,'row_sha256':sha(PCP/fn)}
            if es[ei]!=expected or sha(PCP/row['state_file'])!=row['state_sha256']: raise RuntimeError('parent frame commit')
            ei+=1
        if es[ei]!={'event':'case_complete','case':label,'file':label+'_complete.json','sha256':sha(PCP/(label+'_complete.json'))}: raise RuntimeError('parent case commit')
        ei+=1
    if ei!=121: raise RuntimeError('parent journal order')
    INPUTS[str((PCP/'journal.jsonl').relative_to(ROOT))]=sha(PCP/'journal.jsonl')
    INPUTS[str(Path(__file__).resolve().relative_to(ROOT))]=sha(__file__)
    return pr

def recheck_inputs():
    for f,h in INPUTS.items():
        if sha(ROOT/f)!=h: raise RuntimeError('live input changed: '+f)

def resume_preflight():
    if not CP.is_dir() or not (CP/'manifest.json').exists() or not (CP/'journal.jsonl').exists(): raise RuntimeError('no recoverable checkpoint')
    if any(p.exists() for p in (RESULT,REPORT,RECEIPT)): raise RuntimeError('completed outcome exists; recover report separately if needed')
    m=read(CP/'manifest.json')
    if m['input_sha256']!=INPUTS or m['parameters']!=parameters(): raise RuntimeError('resume input/source/protocol/parameter mismatch')
    es=[json.loads(x) for x in (CP/'journal.jsonl').read_text().splitlines()]
    if not es or es[0]['event']!='started' or es[0]['manifest_sha256']!=sha(CP/'manifest.json'): raise RuntimeError('resume manifest commit')
    runs=[e for e in es if e['event'] in ('started','resume_started')]
    last_pid=runs[-1]['PID']
    try: os.kill(last_pid,0)
    except ProcessLookupError: pass
    except PermissionError: raise RuntimeError('prior execution ownership uncertain')
    else: raise RuntimeError('prior recorded execution PID still live; do not duplicate')
    COMMITS['manifest.json']=sha(CP/'manifest.json')
    external_errors=[e for e in es if e['event']=='error' and e.get('external_error_sha256')]
    if ERROR.exists() and not external_errors: raise RuntimeError('uncommitted failed-attempt bytes require manual recovery')
    for e in es:
        if 'file' in e and 'sha256' in e:
            f=e['file']
            if f in COMMITS and COMMITS[f]!=e['sha256']: raise RuntimeError('conflicting checkpoint commits')
            COMMITS[f]=e['sha256']
        if e['event']=='error' and e.get('external_error_sha256'):
            if sha(ERROR)!=e['external_error_sha256']: raise RuntimeError('failed-attempt bytes changed')
            if any(not c['passed'] for c in read(ERROR).get('checks',[])): raise RuntimeError('failed arithmetic attempt preserved; cannot resume it')
    actual={p.name for p in CP.iterdir() if p.is_file() and p.name!='journal.jsonl'}
    if actual!=set(COMMITS): raise RuntimeError('uncommitted bytes require separate manual recovery; do not rerun')
    for f,h in COMMITS.items():
        if sha(CP/f)!=h: raise RuntimeError('committed bytes changed: '+f)
        if f.endswith('.json'):
            v=read(CP/f)
            if any(not c['passed'] for c in v.get('checks',[])): raise RuntimeError('failed arithmetic checkpoint preserved; cannot resume past it')
    return m

def parameters():
    return {'AR_rational':[str(a) for a in ARS],'release_x_rational':[str(x) for x in TIMES],
            'cycle_global_nodes':list(CYCLE),'anchor_global_nodes':[0,4],'edge_basis':['empty','occupied'],
            'h_rational':str(HFLIP),'t_rational':str(THOP),'j_rational':str(JCUR),'lambda_rational':str(LAM),
            'base_rational':str(BASE),'all_case_count':8,'all_preparation_count':104,'all_frame_count':1352,
            'clock_queries':['X-iY (joint dressed formed phase)','Z-iY (original query retained)']}

def physical_apply(a,ar):
    # Independently assembled global-node action; shape q,edge,carrier,column.
    out=(float(BASE)+ar*POP)[:,None,None,None]*a
    out[:,0]+=((2+float(LAM)*END_SUM)[:,None,None]-float(JCUR)*ENDMASK[None,:,None])*a[:,0]
    for k in range(8):
        u,v=CYCLE[k],CYCLE[(k+1)%8]
        if k==0:
            out[:,1,u]-=float(THOP)*a[:,1,v]; out[:,1,v]-=float(THOP)*a[:,1,u]
        else:
            out[:,:,u]-=float(THOP)*a[:,:,v]; out[:,:,v]-=float(THOP)*a[:,:,u]
    out-=float(HFLIP)*a[:,::-1]
    return out

def base_matrix(s):
    h=np.eye(16)*float(BASE)
    h[:8,:8]+=np.diag(2+float(LAM)*s-float(JCUR)*ENDMASK)
    for bit in range(2):
        for k in range(8):
            if k==0 and bit==0: continue
            u,v=CYCLE[k]+8*bit,CYCLE[(k+1)%8]+8*bit
            h[u,v]-=float(THOP); h[v,u]-=float(THOP)
    h[:8,8:]-=float(HFLIP)*np.eye(8); h[8:,:8]-=float(HFLIP)*np.eye(8)
    return h

def eigen_packet():
    p=CP/'release_eigensystems.npz'
    if p.name in COMMITS:
        with np.load(p,allow_pickle=False) as z:
            meta=json.loads(str(z['metadata_json'])); ev=z['absolute_eigenvalues_all_AR']; vv=z['eigenvectors_q']; bases=z['base_matrices']
        if meta['input_sha256']!=INPUTS or meta['parameters']!=parameters() or not all(c['passed'] for c in meta['checks']): raise RuntimeError('eigen recovery metadata')
        CHECKS.extend(meta['checks']); return ev,vv,COMMITS[p.name]
    ACTIVE.update(stage='new_three_16D_eigensystems')
    exact('global_q_word_permutation',len(set(CYCTOGLOBAL.tolist()))==256 and np.array_equal(CYCTOGLOBAL[GLOBALTOCYC],WORDS))
    exact('carrier_node_permutation',sorted(CYCLE)==list(range(8)) and CYCLE[:2]==(0,4))
    ce={tuple(sorted((CYCLE[k],CYCLE[(k+1)%8]))) for k in range(8)}
    exact('literal_C8_K44',ce==({(i,4+i) for i in range(4)}|{(i,4+(i+1)%4) for i in range(4)}))
    exact('only_anchor_released',len(ce)==8 and (0,4) in ce and all(sum(v in e for e in ce)==2 for v in range(8)))
    bases=np.stack([base_matrix(s) for s in range(3)])
    be=np.empty((3,16)); bv=np.empty((3,16,16))
    for s in range(3):
        gate('base_Hermitian_%d'%s,bases[s],bases[s].T,tol=5e-10)
        be[s],bv[s]=np.linalg.eigh(bases[s])
        gate('base_eigen_residual_%d'%s,bases[s]@bv[s],bv[s]*be[s][None,:],5e-10)
        gate('base_eigen_orthogonal_%d'%s,bv[s].T@bv[s],np.eye(16),5e-10)
    vv=bv[END_SUM]; ev=np.array([be[END_SUM]+float(ar)*POP[:,None] for ar in ARS])
    for ai,ar in enumerate(ARS):
        full=vv.reshape(256,2,8,16)
        gate('all256_physical_block_residual_AR%d'%ai,physical_apply(full,float(ar)),(vv*ev[ai,:,None,:]).reshape(full.shape),5e-10)
    meta={'input_sha256':dict(INPUTS),'parameters':parameters(),'checks':list(CHECKS),'new_eigensolver_calls':3}
    digest=commit_npz(p,'eigensystems_saved',base_matrices=bases,base_eigenvalues=be,base_eigenvectors=bv,
                      eigenvectors_q=vv,absolute_eigenvalues_all_AR=ev,global_record_bits=BITS,
                      cyclic_to_global_record_words=CYCTOGLOBAL,global_to_cyclic_record_words=GLOBALTOCYC,
                      cycle_global_nodes=np.array(CYCLE),metadata_json=np.array(json.dumps(clean(meta),sort_keys=True)))
    return ev,vv,digest

def full_clock(a,ad):
    beta=[]; bd=[]; empty=[]; X=[]; Y=[]; Z=[]; old=[]; oldd=[]; Zdot=[]
    prob=np.sum(abs(a)**2,axis=(1,2,3)); n=prob.sum(); q=BITS@prob
    probdot=2*np.real(np.sum(np.conj(a)*ad,axis=(1,2,3))); nd=probdot.sum(); qd=BITS@probdot
    for v in range(8):
        lo=WORDS[BITS[v]==0]; hi=lo|(1<<v)
        b=2*np.vdot(a[hi],a[lo])
        db=2*(np.vdot(ad[hi],a[lo])+np.vdot(a[hi],ad[lo]))
        eb=2*np.vdot(a[hi,0],a[lo,0])
        x,y,z=b.real,-b.imag,n-2*q[v]
        zd=nd-2*qd[v]
        beta.append(b); bd.append(db); empty.append(eb); X.append(x); Y.append(y); Z.append(z)
        old.append(z-1j*y); oldd.append(zd+1j*db.imag); Zdot.append(zd)
    dots={'X':np.real(bd),'Y':-np.imag(bd),'Z':np.array(Zdot)}
    return np.asarray(beta),np.asarray(bd),np.asarray(empty),{'X':np.array(X),'Y':np.array(Y),'Z':np.array(Z)},np.asarray(old),np.asarray(oldd),dots

def observables(a,ad,ar,initial_clock,label,expected_energy):
    pr=np.sum(abs(a)**2,3); prd=2*np.real(np.sum(np.conj(a)*ad,3))
    qprob=pr.sum((1,2)); qp_dot=prd.sum((1,2)); norm=qprob.sum()
    car=pr.sum((0,1)); card=prd.sum((0,1)); emptyprob=pr[:,0].sum(); emptydot=prd[:,0].sum()
    q=BITS@qprob; qq=(BITS*qprob[None,:])@BITS.T
    carrho=np.einsum('qbci,qbdi->cd',a,np.conj(a))
    edgeoff=np.vdot(a[:,1],a[:,0]); edot=np.vdot(ad[:,1],a[:,0])+np.vdot(a[:,1],ad[:,0])
    ex,ey,ez=2*edgeoff.real,-2*edgeoff.imag,2*emptyprob-norm
    exd,eyd,ezd=2*edot.real,-2*edot.imag,2*emptydot-qp_dot.sum()
    hops=[]; currents=[]; div=np.zeros(8)
    for k in range(8):
        u,v=CYCLE[k],CYCLE[(k+1)%8]
        cross=np.vdot(a[:,1,u],a[:,1,v]) if k==0 else np.vdot(a[:,:,u],a[:,:,v])
        hops.append(2*cross.real); curr=2*float(THOP)*cross.imag; currents.append(curr); div[u]-=curr; div[v]+=curr
    sectors=[]
    for qa,qb in ((0,0),(0,1),(1,0),(1,1)):
        sel=(BITS[0]==qa)&(BITS[4]==qb); w=float(qprob[sel].sum()); joint=float(pr[sel,0].sum())
        sectors.append({'q0':qa,'q4':qb,'weight':w,'empty_joint_probability':joint,
                        'conditional_empty_probability':None if w==0 else joint/w,
                        'empty_joint_carrier_probability':pr[sel,0].sum(0)})
    bp,bpd,epb,pauli,old,oldd,pauli_dot=full_clock(a,ad)
    charging=ar*float(POP@qprob); degree=2*emptyprob
    feedback=float(LAM)*float(END_SUM@pr[:,0].sum(1))
    removed_current=-float(JCUR)*float(pr[:,0,[0,4]].sum())
    hopping=-float(THOP)*sum(hops); flip=-float(HFLIP)*ex
    energy=float(BASE)*norm+charging+degree+feedback+removed_current+hopping+flip
    gate(label+'_norm',norm,1); gate(label+'_record_words_static',qp_dot,0.)
    gate(label+'_carrier_continuity',card,div); gate(label+'_empty_link_current',emptydot,-float(HFLIP)*ey)
    gate(label+'_energy',energy,expected_energy,5e-9)
    gate(label+'_operator_energy',np.vdot(a,1j*ad).real,energy,5e-9)
    gate(label+'_full_H_derivative',np.linalg.norm(ad+1j*physical_apply(a,ar)),0.,5e-10)
    gate(label+'_energy_derivative',2*np.vdot(ad,physical_apply(a,ar)).real,0.,5e-9)
    gate(label+'_q_qq_diagonal',np.diag(qq),q)
    gate(label+'_clock_commutator_all8',bpd,1j*ar*bp+1j*float(LAM)*epb*np.array([1,0,0,0,1,0,0,0]),5e-10)
    other=np.array([1,2,3,5,6,7]); x=ACTIVE['release_time']
    gate(label+'_six_nonendpoint_clock_phase',bp[other],initial_clock[other]*np.exp(1j*ar*x),5e-10)
    gate(label+'_six_nonendpoint_clock_amplitude',abs(bp[other]),abs(initial_clock[other]),5e-10)
    return {'norm':norm,'empty_edge_probability':emptyprob,'empty_edge_probability_dot':emptydot,
            'incidence_Pauli':{'X':ex,'Y':ey,'Z':ez},'incidence_Pauli_dot':{'X':exd,'Y':eyd,'Z':ezd},
            'carrier_p_global':car,'carrier_p_dot_global':card,'carrier_density_global':carrho,
            'empty_joint_carrier_probability':pr[:,0].sum(0),'edge_T_occupied_cycle':hops,
            'edge_current_forward_cycle':currents,'carrier_current_divergence_global':div,
            'endpoint_record_conditioning':sectors,'record_word_probability':qprob,'record_q_global':q,
            'record_q_dot_global':BITS@qp_dot,'record_qq_global':qq,'mean_endpoint_degree':2-emptyprob,'total_degree_defect_square':2*emptyprob,
            'occupied_edge_count':8-emptyprob,'supplied_single_deleted_cycle_connected_probability':norm,
            'return_charge_number_probability':np.array([qprob[KWORD==-k].sum() for k in range(-4,5)]),
            'record_Pauli_global':pauli,'record_Pauli_dot_global':pauli_dot,'Bplus_beta_global':bp,'Bplus_dot_global':bpd,
            'Bplus_amplitude_global':abs(bp),'Bplus_rate_x_global':[rate(b,d) for b,d in zip(bp,bpd)],
            'empty_joint_Bplus_global':epb,'Bplus_dot_charging_piece':1j*ar*bp,
            'Bplus_dot_endpoint_feedback_piece':1j*float(LAM)*epb*np.array([1,0,0,0,1,0,0,0]),
            'original_Z_minus_iY_beta_global':old,'original_Z_minus_iY_dot_global':oldd,
            'original_Z_minus_iY_rate_x_global':[rate(b,d) for b,d in zip(old,oldd)],
            'bare_return_traced_X_global':np.zeros(8),'bare_return_traced_Y_global':np.zeros(8),
            'field_self_energy':8*norm,'carrier_storage_current_base_energy':1.5*norm,
            'retained_record_charging_energy':charging,'degree_defect_energy':degree,
            'record_feedback_change_energy':feedback,'removed_occupied_current_energy':removed_current,
            'actual_occupied_hopping_energy':hopping,'incidence_flip_energy':flip,'full_energy':energy,
            'initial_release_flip_mean_work':0.,'readout_scope':'Full coherent code; q-diagonal conditioning and cross-q dressed queries explicitly separated.'}

def get_preparation(case,ti,vv,eigen_sha):
    name=case['case']+'_prep%02d'%ti; file=CP/(name+'_initial.npz'); jf=CP/(name+'_initial.json')
    if file.name in COMMITS or jf.name in COMMITS:
        if file.name not in COMMITS or jf.name not in COMMITS: raise RuntimeError('partial preparation commit requires manual recovery')
        meta=read(jf)
        if meta['input_sha256']!=INPUTS or meta['eigensystem_sha256']!=eigen_sha or meta['preparation']!=name or meta['initial_state_sha256']!=COMMITS[file.name]: raise RuntimeError('preparation recovery metadata')
        with np.load(file,allow_pickle=False) as z:
            a0=z['psi_initial']; coeff=z['spectral_coefficients']; nm=json.loads(str(z['metadata_json']))
        if nm!=meta['npz_metadata'] or not all(c['passed'] for c in meta['checks']): raise RuntimeError('preparation recovery state/checks')
        CHECKS.extend(meta['checks']); return name,a0,coeff,meta
    begin=len(CHECKS); row=case['rows'][ti]
    with np.load(PCP/row['state_file'],allow_pickle=False) as z:
        old=z['psi']; nm=json.loads(str(z['metadata_json']))
    expected={k:v for k,v in row.items() if k not in ('observables','state_file','state_sha256')}
    if nm!=expected or old.shape!=(2048,8): raise RuntimeError('parent saved state metadata')
    cyc=old.reshape(8,256,8); a0=np.zeros((256,2,8,8),dtype=np.complex128)
    for j,v in enumerate(CYCLE): a0[CYCTOGLOBAL,1,v,:]=cyc[j]
    restored=np.stack([a0[CYCTOGLOBAL,1,v,:] for v in CYCLE])
    gate(name+'_parent_full_state_permutation',restored,cyc,5e-10)
    gate(name+'_initial_Gram',a0.reshape(4096,8).conj().T@a0.reshape(4096,8),np.eye(8)/8)
    gate(name+'_initial_empty_support',np.linalg.norm(a0[:,0]),0.,5e-10)
    qp=np.sum(abs(a0)**2,axis=(1,2,3)); q=BITS@qp; qq=(BITS*qp[None,:])@BITS.T
    gate(name+'_parent_retained_q',q,np.array(row['observables']['record_q'])[GLOBALTOPOS])
    gate(name+'_parent_retained_qq',qq,np.asarray(row['observables']['record_qq'])[np.ix_(GLOBALTOPOS,GLOBALTOPOS)])
    ar=float(F(case['AR_rational'])); ad0=-1j*physical_apply(a0,ar)
    initial_clock=full_clock(a0,ad0)[0]
    parentplus=(np.asarray(row['observables']['record_Pauli']['X'])-1j*np.asarray(row['observables']['record_Pauli']['Y']))[GLOBALTOPOS]
    gate(name+'_parent_full_cross_q_clock',initial_clock,parentplus,5e-10)
    expected_energy=row['observables']['all_age_post_quench_energy']
    gate(name+'_initial_release_mean_work',np.vdot(a0,physical_apply(a0,ar)).real,expected_energy,5e-9)
    coeff=np.einsum('qim,qic->qmc',np.conj(vv),a0.reshape(256,16,8))
    gate(name+'_spectral_initial_resolution',np.einsum('qim,qmc->qic',vv,coeff),a0.reshape(256,16,8),5e-10)
    npmeta={'preparation':name,'case':case['case'],'preparation_time_index':ti,'preparation_x_rational':row['x_rational'],
            'AR_rational':case['AR_rational'],'formation_gamma_rational':case['gamma_rational'],
            'parent_state_sha256':row['state_sha256'],'eigensystem_sha256':eigen_sha,'input_sha256':dict(INPUTS)}
    ah=commit_npz(file,'preparation_state_saved',psi_initial=a0,spectral_coefficients=coeff,
                  metadata_json=np.array(json.dumps(npmeta,sort_keys=True)))
    meta={**npmeta,'initial_state_file':file.name,'initial_state_sha256':ah,'npz_metadata':npmeta,
          'copy_off_work':row['observables']['all_age_copy_off_work'],'pre_switch_energy':row['observables']['full_energy'],
          'expected_post_switch_energy':expected_energy,'initial_clock_Bplus_global':clean(initial_clock),
          'record_word_probability':clean(qp),'initial_mean_release_flip_work':0.,
          'ideal_Bplus_structural_null':case['gamma_rational']=='0' or ti==0,
          'checks':list(CHECKS[begin:])}
    commit(jf,meta,'preparation_metadata_saved'); return name,a0,coeff,meta

def preparation_run(case,ti,ev,vv,eigen_sha):
    name,a0,coeff,meta=get_preparation(case,ti,vv,eigen_sha)
    complete=CP/(name+'_complete.json')
    if complete.name in COMMITS:
        s=read(complete)
        if s['input_sha256']!=INPUTS or s['initial_state_sha256']!=meta['initial_state_sha256'] or len(s['rows'])!=13:
            raise RuntimeError('completed preparation custody')
        for row in s['rows']:
            if row['input_map_sha256']!=input_identity() or row['row_file'] not in COMMITS or row['state_file'] not in COMMITS or read(CP/row['row_file'])!=row: raise RuntimeError('completed frame custody')
            if row['state_sha256']!=COMMITS[row['state_file']] or not all(c['passed'] for c in row['checks']): raise RuntimeError('completed frame checks')
            CHECKS.extend(row['checks'])
        return s
    ai=next(i for i,a in enumerate(ARS) if str(a)==case['AR_rational']); ar=float(ARS[ai]); initial_clock=complex_value(meta['initial_clock_Bplus_global'])
    rows=[]; begin=time.monotonic()
    for ri,xf in enumerate(TIMES):
        ACTIVE.update(preparation=name,release_time=float(xf),stage='new_release_frame')
        jf=CP/(name+'_release%02d.json'%ri); nf=CP/(name+'_release%02d.npz'%ri)
        if jf.name in COMMITS or nf.name in COMMITS:
            if jf.name not in COMMITS or nf.name not in COMMITS: raise RuntimeError('partial frame commit requires manual recovery')
            row=read(jf)
            if row['input_map_sha256']!=input_identity() or row['preparation']!=name or row['release_time_index']!=ri or row['x_rational']!=str(xf) or row['state_sha256']!=COMMITS[nf.name]: raise RuntimeError('frame recovery metadata')
            if not all(c['passed'] for c in row['checks']): raise RuntimeError('failed frame preserved; cannot rerun')
            CHECKS.extend(row['checks']); rows.append(row); continue
        ckstart=len(CHECKS)
        amp=np.exp(-1j*ev[ai]*float(xf))[:,:,None]*coeff
        a=np.einsum('qim,qmc->qic',vv,amp).reshape(256,2,8,8)
        ad=np.einsum('qim,qmc->qic',vv,-1j*ev[ai,:,:,None]*amp).reshape(a.shape)
        if ri==0:
            gate(name+'_release0_initial_resolution',a,a0,5e-10); a=a0.copy()
        values=observables(a,ad,ar,initial_clock,name+'_release%02d'%ri,meta['expected_post_switch_energy'])
        gate(name+'_record_word_conservation_%d'%ri,values['record_word_probability'],meta['record_word_probability'])
        gate(name+'_all8_mixture_Gram_%d'%ri,a.reshape(4096,8).conj().T@a.reshape(4096,8),np.eye(8)/8)
        recovered=np.einsum('qim,qic->qmc',np.conj(vv),a.reshape(256,16,8))
        gate(name+'_saved_spectral_probability_%d'%ri,abs(recovered)**2,abs(coeff)**2,5e-10)
        if meta['ideal_Bplus_structural_null']:
            gate(name+'_ideal_blank_clock_null_%d'%ri,values['Bplus_beta_global'],0.,5e-10)
        if case['gamma_rational']=='0':
            gate(name+'_blank_record_q_%d'%ri,values['record_q_global'],0.)
        fm={'preparation':name,'case':case['case'],'preparation_time_index':ti,
            'preparation_x_rational':meta['preparation_x_rational'],'release_time_index':ri,'x_rational':str(xf),
            'AR_rational':case['AR_rational'],'formation_gamma_rational':case['gamma_rational'],
            'eigensystem_sha256':eigen_sha,'initial_state_sha256':meta['initial_state_sha256'],'input_map_sha256':input_identity()}
        ah=commit_npz(nf,'release_frame_state_saved',psi=a,psi_dot_x=ad,
                      metadata_json=np.array(json.dumps(fm,sort_keys=True)))
        row={**fm,'x':float(xf),'state_file':nf.name,'state_sha256':ah,'row_file':jf.name,'observables':clean(values),
             'copy_off_work':meta['copy_off_work'],'initial_mean_release_flip_work':0.,
             'ideal_Bplus_structural_null':meta['ideal_Bplus_structural_null'],
             'clock_status':'RAW_FULL_DRESSED_QUERY_WITH_EXACT_IDEAL_NULL_QUALIFICATION_NO_PROPER_CALIBRATION',
             'checks':list(CHECKS[ckstart:])}
        commit(jf,row,'release_frame_metadata_saved'); rows.append(row)
        del a,ad,amp,recovered
    s={'preparation':name,'case':case['case'],'AR_rational':case['AR_rational'],
       'formation_gamma_rational':case['gamma_rational'],'preparation_time_index':ti,
       'preparation_x_rational':meta['preparation_x_rational'],'initial_state_sha256':meta['initial_state_sha256'],
       'eigensystem_sha256':eigen_sha,'copy_off_work':meta['copy_off_work'],'expected_post_switch_energy':meta['expected_post_switch_energy'],
       'input_sha256':dict(INPUTS),'rows':rows,'elapsed_seconds_this_preparation':time.monotonic()-begin,
       'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    commit(complete,s,'preparation_complete')
    print(json.dumps({'preparation':name,'frames':13,'completed_checks':len(CHECKS),'failed':sum(not c['passed'] for c in CHECKS)},sort_keys=True),flush=True)
    return s

def blank_census_controls(preps):
    reference=preps[0]['rows']
    keys=('empty_edge_probability','incidence_Pauli','carrier_p_global','carrier_density_global','full_energy')
    for p in preps:
        if p['formation_gamma_rational']!='0': continue
        for ri,row in enumerate(p['rows']):
            for k in keys:
                actual=row['observables'][k]; expected=reference[ri]['observables'][k]
                if k=='incidence_Pauli':
                    for kind in ('X','Y','Z'): gate(p['preparation']+'_blank_same_'+kind+'_%d'%ri,actual[kind],expected[kind])
                elif k=='carrier_density_global': gate(p['preparation']+'_blank_same_density_%d'%ri,complex_value(actual),complex_value(expected))
                else: gate(p['preparation']+'_blank_same_'+k+'_%d'%ri,actual,expected)

def main():
    global APPEND_ALLOWED
    if sys.argv[1:] not in (['--execute'],['--resume']): raise SystemExit('Requires exact --execute or root-authorized manual --resume; no calculation performed.')
    parent=authenticate_parent(); mode=sys.argv[1]; begun=time.monotonic()
    if mode=='--execute':
        if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)): raise RuntimeError('reserved output exists; preserve/recover first')
        CP.mkdir(); APPEND_ALLOWED=True
        manifest={'PID':os.getpid(),'argv':['--execute'],'input_sha256':dict(INPUTS),'parameters':parameters(),
                  'Python':sys.version,'NumPy':np.__version__,'threads':{k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}}
        mh=write_json(CP/'manifest.json',manifest); COMMITS['manifest.json']=mh
        event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':dict(INPUTS)})
    else:
        manifest=resume_preflight(); mh=sha(CP/'manifest.json'); APPEND_ALLOWED=True
        event({'event':'resume_started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':dict(INPUTS)})
    ev,vv,eigen_sha=eigen_packet(); preps=[]
    for case in parent['cases']:
        for ti in range(13): preps.append(preparation_run(case,ti,ev,vv,eigen_sha))
    blank_census_controls(preps)
    exact('complete_unselected_104_by13_census',len(preps)==104 and all(len(p['rows'])==13 for p in preps))
    recheck_inputs(); passed=sum(c['passed'] for c in CHECKS); failed=sum(not c['passed'] for c in CHECKS)
    status='QUALIFIED_ARITHMETIC_FIXED_SUPPORTED_RELEASE_NO_METRIC_OR_PHASE_ADOPTION' if failed==0 else 'ARITHMETIC_FAILED'
    result={'status':status,'passed':passed,'failed':failed,'checks':list(CHECKS),'preparations':preps,
            'input_sha256':dict(INPUTS),'manifest_sha256':mh,'PID':os.getpid(),'original_manifest_PID':manifest['PID'],
            'elapsed_seconds_this_execution':time.monotonic()-begun,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'All1352 full coherent frames; one native bond released after accounted copy-off. Fixed15 other bits, declared physical code, no selection, 3D phase, metric, gravity or proper-clock adoption.'}
    raw=write_json(RESULT,result); canonical=hashlib.sha256(blob(result)).hexdigest()
    event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':canonical})
    lines=['# Floating-return retained records and released bond V001','',
           '%s: %d/%d arithmetic checks;104 preparations,1352 full coherent frames.'%(status,passed,len(CHECKS)),
           '','All record values remain conserved. Empty-edge/carrier dynamics and endpoint conditioning are actual correlated readouts.',
           'Nonendpoint Bplus has its declared exact charging frequency when its formed amplitude is nonzero. Raw roundoff/null rates are not clocks.',
           'The original Z-iY query, all works and all other held bits remain explicit; no proper calibration or autonomous support is inferred.','',
           '| Preparation | AR | prep x | release x | empty edge | q0=0,q4=0 conditional | q0=1,q4=1 conditional | energy | Woff | Bplus global1 amplitude | Bplus global1 raw rate |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    def fmt(x): return 'undefined' if x is None else '%.10g'%x
    for p in preps:
        for row in p['rows']:
            o=row['observables']; s=o['endpoint_record_conditioning']
            lines.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |'%(p['preparation'],p['AR_rational'],p['preparation_x_rational'],row['x_rational'],fmt(o['empty_edge_probability']),fmt(s[0]['conditional_empty_probability']),fmt(s[3]['conditional_empty_probability']),fmt(o['full_energy']),fmt(p['copy_off_work']),fmt(o['Bplus_amplitude_global'][1]),fmt(o['Bplus_rate_x_global'][1])))
    lines+=['','Raw result SHA256: '+raw,'Canonical result SHA256: '+canonical,
            'No physical density, gravitational mass, stiffness success, galaxy/expansion fit, autonomous permanence or geometry selection is inferred.']
    with REPORT.open('x') as f:
        f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    recheck_inputs(); rh=sha(REPORT); event({'event':'report_saved','sha256':rh,'data_rows':1352})
    cpmap={p.name:sha(p) for p in sorted(CP.iterdir()) if p.name!='journal.jsonl'}
    receipt={'status':status,'passed':passed,'failed':failed,'input_sha256':dict(INPUTS),'checkpoint_sha256':cpmap,
             'result_raw_sha256':raw,'result_canonical_sha256':canonical,'report_sha256':rh,
             'journal_prefix_sha256':sha(CP/'journal.jsonl'),'PID':os.getpid(),'original_manifest_PID':manifest['PID'],
             'elapsed_seconds_this_execution':result['elapsed_seconds_this_execution'],'peakRSS_bytes':result['peakRSS_bytes']}
    rr=write_json(RECEIPT,receipt); event({'event':'receipt_saved','sha256':rr})
    print(json.dumps({'status':status,'passed':passed,'failed':failed,'raw_sha256':raw,'receipt_sha256':rr,
                      'elapsed_seconds_this_execution':result['elapsed_seconds_this_execution']},sort_keys=True),flush=True)
    return 0 if failed==0 else 3

if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as exc:
        if not APPEND_ALLOWED:
            print(json.dumps({'status':'PREFLIGHT_REJECTED_NO_OUTPUT_MUTATION','error':repr(exc)}),flush=True);raise SystemExit(3)
        error={'error':repr(exc),'traceback':traceback.format_exc(),'active':dict(ACTIVE),'PID':os.getpid(),
               'checks':list(CHECKS),'input_sha256':dict(INPUTS),'committed_sha256':dict(COMMITS)}
        if not ERROR.exists():
            eh=write_json(ERROR,error); event({'event':'error','external_error_sha256':eh,'PID':os.getpid(),'active':dict(ACTIVE)})
        else:
            ix=sum(1 for p in CP.glob('error_attempt_*.json'))+1
            commit(CP/('error_attempt_%03d_PID%d.json'%(ix,os.getpid())),error,'error_attempt_saved')
        print(json.dumps({'status':'ERROR_PRESERVED','error':repr(exc),'active':ACTIVE},sort_keys=True),flush=True);raise SystemExit(3)
