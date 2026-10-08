#!/usr/bin/env python3
"""NEW tagged insertion/reaction; root --execute or manual --resume only."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
import sys,json,hashlib,math,time,resource,traceback
from pathlib import Path
from fractions import Fraction as F
import numpy as np

J=Path(__file__).resolve().parent; ROOT=J.parent.parent
NAME='FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001'
PARENT='FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001'
PCP=J/'floating_return_c8_retained_record_geometry_v001_checkpoints'
CP=J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints'
RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md')
RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PINS={
    NAME+'.md':'68b4a61ded02e9e6ecdfcf1819680d519f794eb8e3ba08b5b7a1ba329ed1aab9',
    PARENT+'.md':'8f3dc32381e76a4e6badfe23fff6c8bdd4830cb32ed0aff99b1aef57eba5ce5b',
    'floating_return_c8_retained_record_geometry_v001.py':'49f2684fe46bce5d46e8e86782f82d73a0293e304d617a46eb5b84e98638396a',
    PARENT+'_RESULT.json':'4104ec10a4c0a6a9183e9943743d80ce847dff4bad8b82013c0f2594bc581eac',
    PARENT+'_RESULT.md':'f209ad41386602049bb51b9310e0224d95f2c52a07c8768f9560b846b6264288',
    PARENT+'_RECEIPT.json':'2151436c1ce895c6fb577c72c673faefed184c1c011b57c98368c33dbf0663d5',
    PARENT+'_AUDIT.json':'5c519d1bef61c0e4b2cdf71424de9df08fa0d7f926b26c6ab9496c986d97e84f',
    'NATIVE_SPATIAL_MATTER_SOURCE_CORRESPONDENCE_V001.md':'6d626c6d9716aae6b951da7efecd0d8fe56f29c250b0575c9282dec63843ff6a',
    'NATIVE_REVISED_CARRIER_FIXED_CENSUS_CONSTRAINT_V001.md':'000afae908131ffd5db78cfa472c66c9f3e0db05b9efb53fbf6abb04bf461de7',
    'FLOATING_RETURN_FORMED_RECORD_CLOCK_V001.md':'c83417ce29e8ea89be71c78510e27a0eff3d8a0bfacfcc507118ccb618ab449d',
}
ARS=(F(0),F(1,8),F(7,40),F(1,4)); TIMES=(F(0),F(1,5),F(2),F(8))
CYCLE=(0,4,3,7,2,6,1,5); EDGES=tuple((CYCLE[k],CYCLE[(k+1)%8]) for k in range(8))
T=.1; JC=.25; LAM=.5; HF=.2
WORDS=np.arange(256,dtype=np.int64)
BITS=np.array([[(int(q)>>v)&1 for q in WORDS] for v in range(8)],dtype=np.int64)
POP=BITS.sum(0); ESUM=BITS[0]+BITS[4]
PAIRS=np.array([(a,b) for a in range(8) for b in range(8) if a!=b],dtype=np.int64)
PAIRINDEX={(int(a),int(b)):i for i,(a,b) in enumerate(PAIRS)}
POS=np.argsort(CYCLE); DIST=np.array([min(abs(int(POS[a])-int(POS[b])),8-abs(int(POS[a])-int(POS[b]))) for a,b in PAIRS])
ADJ=(DIST==1).astype(np.int64)
OCC=np.array([[(int(a)==v)+(int(b)==v) for a,b in PAIRS] for v in range(8)],dtype=np.int64)
EDGE_C=np.array([OCC[u]+OCC[v]-2*OCC[u]*OCC[v] for u,v in EDGES])
ENDM=np.array([1,0,0,0,1,0,0,0],dtype=np.int64)
TRANS=[]
for u,v in EDGES:
    source=np.array([(PAIRINDEX[(u,b)],PAIRINDEX[(v,b)]) for b in range(8) if b not in (u,v)],dtype=np.int64)
    probe=np.array([(PAIRINDEX[(a,u)],PAIRINDEX[(a,v)]) for a in range(8) if a not in (u,v)],dtype=np.int64)
    TRANS.append((source,probe))
GROUPS=tuple(np.flatnonzero(ESUM==s) for s in range(3))
ETA=np.array([1,1,1,1,-1,-1,-1,-1]); KWORD=ETA@BITS
CHECKS=[];INPUTS={};COMMITS={};APPEND_ALLOWED=False
ACTIVE={'preparation':None,'forward_time':None,'stage':'unstarted'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def clean(v):
    if isinstance(v,np.ndarray):return clean(v.tolist())
    if isinstance(v,np.generic):return clean(v.item())
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    if isinstance(v,complex):return [clean(float(v.real)),clean(float(v.imag))]
    if isinstance(v,float) and not math.isfinite(v):return {'nonfinite':repr(v)}
    return v
def blob(v):return json.dumps(clean(v),sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def write_json(p,v):
    with Path(p).open('xb') as f:
        f.write(json.dumps(clean(v),sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def save_npz(p,**a):
    with Path(p).open('xb') as f:
        np.savez_compressed(f,**a);f.flush();os.fsync(f.fileno())
    return sha(p)
def event(v):
    with (CP/'journal.jsonl').open('ab') as f:f.write(blob(v)+b'\n');f.flush();os.fsync(f.fileno())
def commit(p,v,kind):
    h=write_json(p,v);event({'event':kind,'file':Path(p).name,'sha256':h});COMMITS[Path(p).name]=h;return h
def commit_npz(p,kind,**a):
    h=save_npz(p,**a);event({'event':kind,'file':Path(p).name,'sha256':h});COMMITS[Path(p).name]=h;return h
def gate(name,a,b=0.,tol=1e-9):
    a,b=np.asarray(a),np.asarray(b);ok=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
    e=float(np.max(abs(a-b))) if ok else float('inf')
    CHECKS.append({'name':name,'error':clean(e),'tolerance':tol,'passed':ok and e<=tol})
def exact(name,ok):CHECKS.append({'name':name,'passed':bool(ok),'exact':True})
def rate(b,bd):
    d=float(abs(b)**2);return None if d==0 else float((np.conj(b)*bd).imag/d)
def cv(v):
    a=np.asarray(v,dtype=float);return a[...,0]+1j*a[...,1]
def input_id():return hashlib.sha256(blob(INPUTS)).hexdigest()
def parameters():
    return {'AR_rational':[str(a) for a in ARS],'forward_x_rational':[str(x) for x in TIMES],
            'all_preparations':104,'tagged_frames':416,'paired_reference_frames':416,
            'global_cycle':list(CYCLE),'anchor':[0,4],'ordered_tagged_pairs':PAIRS.tolist(),
            'h':str(F(1,5)),'t':str(F(1,10)),'j':str(F(1,4)),'lambda':str(F(1,2)),
            'insertion':'coherent vacancy I/√7','reference':'exact source-position apparatus trace',
            'new_eigensystems':3,'new_base_dimension':112,'reference_base_dimension':16,
            'full_states_saved':True,'full_state_derivatives_saved':False}

def authenticate():
    for f,h in PINS.items():
        if sha(J/f)!=h:raise RuntimeError('direct frozen input mismatch: '+f)
        INPUTS[str((J/f).relative_to(ROOT))]=h
    p=read(J/(PARENT+'_RESULT.json'));r=read(J/(PARENT+'_RECEIPT.json'))
    if r['result_raw_sha256']!=sha(J/(PARENT+'_RESULT.json')) or r['result_canonical_sha256']!=hashlib.sha256(blob(p)).hexdigest():raise RuntimeError('parent raw/canonical')
    if r['report_sha256']!=sha(J/(PARENT+'_RESULT.md')) or p['passed']!=27370 or r['passed']!=27370 or p['failed']!=0 or r['failed']!=0 or not all(c['passed'] for c in p['checks']):raise RuntimeError('parent result/report/status')
    if p['input_sha256']!=r['input_sha256']:raise RuntimeError('parent result input map')
    for f,h in r['input_sha256'].items():
        if sha(ROOT/f)!=h:raise RuntimeError('inherited input mismatch: '+f)
        INPUTS[f]=h
    cmap=r['checkpoint_sha256'];actual={x.name for x in PCP.iterdir() if x.name!='journal.jsonl'}
    if len(cmap)!=3018 or actual!=set(cmap):raise RuntimeError('parent3018 checkpoint census')
    for f,h in cmap.items():
        if sha(PCP/f)!=h:raise RuntimeError('parent checkpoint mismatch: '+f)
        INPUTS[str((PCP/f).relative_to(ROOT))]=h
    jb=(PCP/'journal.jsonl').read_bytes();es=[json.loads(x) for x in jb.splitlines()]
    if len(es)!=3021 or hashlib.sha256(b'\n'.join(jb.splitlines()[:-1])+b'\n').hexdigest()!=r['journal_prefix_sha256']:raise RuntimeError('parent journal prefix')
    if es[-1]!={'event':'receipt_saved','sha256':sha(J/(PARENT+'_RECEIPT.json'))} or es[-2]!={'event':'report_saved','sha256':r['report_sha256'],'data_rows':1352} or es[-3]!={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']}:raise RuntimeError('parent final commits')
    m=read(PCP/'manifest.json')
    if es[0]['manifest_sha256']!=sha(PCP/'manifest.json') or p['manifest_sha256']!=sha(PCP/'manifest.json') or es[0]['PID']!=m['PID'] or m['PID']!=r['original_manifest_PID'] or es[0]['input_sha256']!=r['input_sha256'] or m['input_sha256']!=r['input_sha256']:raise RuntimeError('parent manifest/start')
    commits={'manifest.json':sha(PCP/'manifest.json')}
    for e in es[1:-3]:
        if 'file' not in e or 'sha256' not in e or e['file'] in commits:raise RuntimeError('parent unexpected/duplicate stage commit')
        commits[e['file']]=e['sha256']
    if commits!=cmap:raise RuntimeError('parent complete stage map')
    if len(p['preparations'])!=104:raise RuntimeError('parent preparation census')
    for pi,prep in enumerate(p['preparations']):
        ci,ti=divmod(pi,13);label='case%02d_prep%02d'%(ci,ti)
        if prep['preparation']!=label or prep['preparation_time_index']!=ti or len(prep['rows'])!=13 or read(PCP/(label+'_complete.json'))!=prep:raise RuntimeError('parent complete preparation custody')
        meta=read(PCP/(label+'_initial.json'))
        if meta['initial_state_sha256']!=cmap[label+'_initial.npz'] or meta['input_sha256']!=r['input_sha256'] or not all(c['passed'] for c in meta['checks']):raise RuntimeError('parent initial custody')
        for ri,row in enumerate(prep['rows']):
            if row['release_time_index']!=ri or read(PCP/row['row_file'])!=row or row['state_sha256']!=cmap[row['state_file']] or row['input_map_sha256']!=hashlib.sha256(blob(r['input_sha256'])).hexdigest() or not all(c['passed'] for c in row['checks']):raise RuntimeError('parent row custody')
    audit=read(J/(PARENT+'_AUDIT.json'))
    if audit['audit_status']!='PASS' or audit['failed_assertions']!=0 or audit['assertions']!=173778:raise RuntimeError('parent independent audit status')
    INPUTS[str((PCP/'journal.jsonl').relative_to(ROOT))]=sha(PCP/'journal.jsonl')
    INPUTS[str(Path(__file__).resolve().relative_to(ROOT))]=sha(__file__)
    return p
def recheck():
    for f,h in INPUTS.items():
        if sha(ROOT/f)!=h:raise RuntimeError('input changed: '+f)
def resume_preflight():
    if not CP.is_dir() or not (CP/'manifest.json').exists() or not (CP/'journal.jsonl').exists():raise RuntimeError('no resumable checkpoint')
    if any(p.exists() for p in (RESULT,REPORT,RECEIPT)):raise RuntimeError('completed outcome exists; report recovery is separate')
    m=read(CP/'manifest.json');es=[json.loads(x) for x in (CP/'journal.jsonl').read_text().splitlines()]
    if m['input_sha256']!=INPUTS or m['parameters']!=parameters() or not es or es[0]['manifest_sha256']!=sha(CP/'manifest.json'):raise RuntimeError('resume input/manifest mismatch')
    runs=[e for e in es if e['event'] in ('started','resume_started')]
    try:os.kill(runs[-1]['PID'],0)
    except ProcessLookupError:pass
    except PermissionError:raise RuntimeError('prior execution ownership uncertain')
    else:raise RuntimeError('prior recorded execution PID is live')
    COMMITS['manifest.json']=sha(CP/'manifest.json')
    errors=[e for e in es if e['event']=='error' and e.get('external_error_sha256')]
    if ERROR.exists() and not errors:raise RuntimeError('uncommitted failure bytes require manual recovery')
    for e in es:
        if 'file' in e and 'sha256' in e:
            f=e['file']
            if f in COMMITS and COMMITS[f]!=e['sha256']:raise RuntimeError('conflicting commit')
            COMMITS[f]=e['sha256']
        if e['event']=='error' and e.get('external_error_sha256'):
            if sha(ERROR)!=e['external_error_sha256'] or any(not c['passed'] for c in read(ERROR).get('checks',[])):raise RuntimeError('failed attempt changed or arithmetic failure preserved')
    actual={p.name for p in CP.iterdir() if p.is_file() and p.name!='journal.jsonl'}
    if actual!=set(COMMITS):raise RuntimeError('uncommitted checkpoint bytes require separate recovery')
    for f,h in COMMITS.items():
        if sha(CP/f)!=h:raise RuntimeError('committed checkpoint changed: '+f)
        if f.endswith('.json') and any(not c['passed'] for c in read(CP/f).get('checks',[])):raise RuntimeError('failed checkpoint cannot be rerun')
    return m

def action(a,ar,two):
    # Literal physical edge/current/hop assembly, independent of base formula.
    nc=2 if two else 1;out=(8+nc+ar*POP)[:,None,None,None]*a
    out[:,0]+=(2+LAM*ESUM)[:,None,None]*a[:,0]
    for k,(u,v) in enumerate(EDGES):
        bits=(1,) if k==0 else (0,1)
        for bit in bits:
            diag=EDGE_C[k] if two else np.eye(8,dtype=int)[u]+np.eye(8,dtype=int)[v]
            out[:,bit]+=JC*diag[None,:,None]*a[:,bit]
            if two:
                for transitions in TRANS[k]:
                    l,r=transitions.T;out[:,bit,l]-=T*a[:,bit,r];out[:,bit,r]-=T*a[:,bit,l]
            else:out[:,bit,u]-=T*a[:,bit,v];out[:,bit,v]-=T*a[:,bit,u]
    out-=HF*a[:,::-1]
    return out
def base_matrix(s):
    h=np.diag(np.tile(11-2*JC*ADJ,2).astype(float))
    h[:56,:56]+=np.diag(2+LAM*s-JC*EDGE_C[0])
    for bit in range(2):
        for k in range(8):
            if bit==0 and k==0:continue
            for transitions in TRANS[k]:
                for a,b in transitions:h[bit*56+a,bit*56+b]-=T;h[bit*56+b,bit*56+a]-=T
    h[:56,56:]-=HF*np.eye(56);h[56:,:56]-=HF*np.eye(56)
    return h
def transform(a,basis,inverse=False):
    # All q blocks retained; three batched GEMMs avoid hundreds of tiny calls.
    b=np.empty_like(a);dim=a.shape[1];cols=a.shape[2]
    for s,qs in enumerate(GROUPS):
        mat=basis[s].conj().T if inverse else basis[s]
        merged=np.transpose(a[qs],(1,0,2)).reshape(dim,-1)
        b[qs]=np.transpose((mat@merged).reshape(dim,len(qs),cols),(1,0,2))
    return b
def eigensystems():
    fn=CP/'reaction_eigensystems.npz'
    if fn.name in COMMITS:
        with np.load(fn,allow_pickle=False) as z:
            meta=json.loads(str(z['metadata_json']));be=z['tagged_base_eigenvalues'];bv=z['tagged_base_eigenvectors'];re=z['reference_base_eigenvalues'];rv=z['reference_base_eigenvectors']
        if meta['input_sha256']!=INPUTS or meta['parameters']!=parameters() or not all(c['passed'] for c in meta['checks']):raise RuntimeError('eigensystem recovery custody')
        CHECKS.extend(meta['checks']);return be,bv,re,rv,COMMITS[fn.name]
    ACTIVE['stage']='three_new_112D_eigensystems';begin=len(CHECKS)
    exact('ordered_pairs_56',len(PAIRINDEX)==56 and all(a!=b for a,b in PAIRS))
    exact('literal_cycle_anchor',len(set(map(frozenset,EDGES)))==8 and EDGES[0]==(0,4) and all(sum(v in e for e in EDGES)==2 for v in range(8)))
    exact('two_tag_current_XOR',np.all((EDGE_C==0)|(EDGE_C==1)))
    exact('tagged_hop_vacancy',all(len(x)==6 for row in TRANS for x in row))
    bases=np.stack([base_matrix(s) for s in range(3)]);be=np.empty((3,112));bv=np.empty((3,112,112))
    for s in range(3):
        gate('tagged_Hermitian_%d'%s,bases[s],bases[s].T,5e-10)
        be[s],bv[s]=np.linalg.eigh(bases[s])
        gate('tagged_eigen_residual_%d'%s,bases[s]@bv[s],bv[s]*be[s][None,:],5e-10)
        gate('tagged_eigen_orthogonal_%d'%s,bv[s].T@bv[s],np.eye(112),5e-10)
    with np.load(PCP/'release_eigensystems.npz',allow_pickle=False) as z:
        re=z['base_eigenvalues'];rv=z['base_eigenvectors'];rb=z['base_matrices'];rm=json.loads(str(z['metadata_json']))
    if rm['input_sha256']!=read(J/(PARENT+'_RECEIPT.json'))['input_sha256'] or rm['new_eigensolver_calls']!=3 or not all(c['passed'] for c in rm['checks']):raise RuntimeError('reused reference eigen custody')
    for s in range(3):
        gate('saved_reference_orthogonal_%d'%s,rv[s].T@rv[s],np.eye(16),5e-10)
        gate('saved_reference_residual_%d'%s,rb[s]@rv[s],rv[s]*re[s][None,:],5e-10)
    for ai,ar in enumerate(ARS):
        for two,ev,vec,dim in ((True,be,bv,56),(False,re,rv,8)):
            full=vec[ESUM].reshape(256,2,dim,2*dim);abse=ev[ESUM]+float(ar)*POP[:,None]
            gate(('tagged' if two else 'reference')+'_all256_physical_AR%d'%ai,action(full,float(ar),two),(vec[ESUM]*abse[:,None,:]).reshape(full.shape),5e-10)
    # Exact two-site mismatch spectrum and occupied-C8 insertion identity controls.
    gate('direct_current_mismatch_eigenvalues',np.array([JC-T,JC+T]),[.15,.35],5e-10)
    adjacency=np.zeros((8,8))
    for u,v in EDGES:adjacency[u,v]=adjacency[v,u]=1
    iso=np.zeros((56,8))
    for k,(a,b) in enumerate(PAIRS):iso[k,a]=1/math.sqrt(7)
    k2=bases[0][56:,56:]-8*np.eye(56)
    k1=rb[0][8:,8:]-8*np.eye(8)
    gate('complete_insertion_compression',iso.T@k2@iso-k1,83/70*np.eye(8)+adjacency/70,5e-10)
    meta={'input_sha256':dict(INPUTS),'parameters':parameters(),'new_eigensolver_calls':3,'reference_eigensolver_calls':0,'checks':list(CHECKS[begin:])}
    h=commit_npz(fn,'eigensystems_saved',tagged_base_matrices=bases,tagged_base_eigenvalues=be,tagged_base_eigenvectors=bv,
                 tagged_absolute_eigenvalues_all_AR=np.array([be[ESUM]+float(ar)*POP[:,None] for ar in ARS]),
                 reference_base_matrices=rb,reference_base_eigenvalues=re,reference_base_eigenvectors=rv,
                 reference_absolute_eigenvalues_all_AR=np.array([re[ESUM]+float(ar)*POP[:,None] for ar in ARS]),
                 ordered_tagged_pairs=PAIRS,global_record_bits=BITS,cycle_global_nodes=np.array(CYCLE),metadata_json=np.array(json.dumps(clean(meta),sort_keys=True)))
    return be,bv,re,rv,h

def clocks(a,ad):
    qp=np.sum(abs(a)**2,axis=(1,2,3));qpd=2*np.real(np.sum(np.conj(a)*ad,axis=(1,2,3)))
    n=qp.sum();nd=qpd.sum();q=BITS@qp;qd=BITS@qpd
    bp=[];bd=[];empty=[];old=[];oldd=[]
    for v in range(8):
        lo=WORDS[BITS[v]==0];hi=lo|(1<<v)
        b=2*np.vdot(a[hi],a[lo]);d=2*(np.vdot(ad[hi],a[lo])+np.vdot(a[hi],ad[lo]));e=2*np.vdot(a[hi,0],a[lo,0])
        bp.append(b);bd.append(d);empty.append(e);old.append(n-2*q[v]+1j*b.imag);oldd.append(nd-2*qd[v]+1j*d.imag)
    return np.asarray(bp),np.asarray(bd),np.asarray(empty),np.asarray(old),np.asarray(oldd)
def carriers(a,two):
    if two:
        expanded=np.zeros((256,2,8,8,a.shape[-1]),complex)
        expanded[:,:,PAIRS[:,0],PAIRS[:,1],:]=a
        source=np.einsum('qeabc,qedbc->ad',expanded,np.conj(expanded))
        probe=np.einsum('qeabc,qeafc->bf',expanded,np.conj(expanded))
        return source,probe
    return None,np.einsum('qebc,qefc->bf',a,np.conj(a))
def obs(a,ad,ar,two,initial_clock,expected,label,x):
    prob=np.sum(abs(a)**2,3);pd=2*np.real(np.sum(np.conj(a)*ad,3))
    qp=prob.sum((1,2));qpd=pd.sum((1,2));norm=qp.sum();empty=prob[:,0].sum();emptyd=pd[:,0].sum()
    q=BITS@qp;qq=(BITS*qp[None,:])@BITS.T
    rho0,rho1=carriers(a,two);p1=np.real(np.diag(rho1));p0=None if rho0 is None else np.real(np.diag(rho0))
    if two:pc=prob.sum((0,1));p0d=np.bincount(PAIRS[:,0],weights=pd.sum((0,1)),minlength=8);p1d=np.bincount(PAIRS[:,1],weights=pd.sum((0,1)),minlength=8)
    else:pc=prob.sum((0,1));p0d=None;p1d=pd.sum((0,1))
    edgecross=np.vdot(a[:,1],a[:,0]);ecdot=np.vdot(ad[:,1],a[:,0])+np.vdot(a[:,1],ad[:,0])
    ex,ey,ez=2*edgecross.real,-2*edgecross.imag,2*empty-norm
    currents=[[],[]] if two else [None,[]];divs=[np.zeros(8),np.zeros(8)] if two else [None,np.zeros(8)]
    thop=0.;currentone=0.;direct=0.;adj_actual=0.
    for k,(u,v) in enumerate(EDGES):
        bits=(1,) if k==0 else (0,1)
        for tag in ((0,1) if two else (1,)):
            if two:
                left,right=TRANS[k][tag].T
                cross=sum(np.vdot(a[:,bit,left],a[:,bit,right]) for bit in bits)
            else:cross=sum(np.vdot(a[:,bit,u],a[:,bit,v]) for bit in bits)
            thop+=2*cross.real;cu=2*T*cross.imag;currents[tag].append(cu);divs[tag][u]-=cu;divs[tag][v]+=cu
        if two:
            one=OCC[u]+OCC[v];both=OCC[u]*OCC[v]
            currentone+=JC*sum(float(one@prob[:,bit].sum(0)) for bit in bits)
            direct-=2*JC*sum(float(both@prob[:,bit].sum(0)) for bit in bits)
            adj_actual+=sum(float(both@prob[:,bit].sum(0)) for bit in bits)
        else:currentone+=JC*sum(float(prob[:,bit,[u,v]].sum()) for bit in bits)
    bp,bd,eb,old,oldd=clocks(a,ad);charging=ar*float(POP@qp)
    degree=2*empty;feedback=LAM*float(ESUM@prob[:,0].sum(1));hopping=-T*thop;flip=-HF*ex
    nc=2 if two else 1;energy=(8+nc)*norm+charging+degree+feedback+currentone+direct+hopping+flip
    sectors=[]
    for qa,qb in ((0,0),(0,1),(1,0),(1,1)):
        sel=(BITS[0]==qa)&(BITS[4]==qb);weight=float(qp[sel].sum());joint=float(prob[sel,0].sum())
        position_joint=prob[sel].sum((0,1));empty_position_joint=prob[sel,0].sum(0)
        sector={'q0':qa,'q4':qb,'weight':weight,'empty_joint':joint,'empty_conditional':None if weight==0 else joint/weight,
                'position_joint_probability':position_joint,'position_conditional_probability':None if weight==0 else position_joint/weight,
                'empty_position_joint_probability':empty_position_joint}
        if two:
            aj=float(ADJ@position_joint);dj=float(DIST@position_joint)
            sector.update(tagged_reference_adjacency_joint=aj,tagged_reference_adjacency_conditional=None if weight==0 else aj/weight,
                          tagged_reference_separation_joint=dj,tagged_reference_separation_conditional=None if weight==0 else dj/weight)
        sectors.append(sector)
    gate(label+'_norm',norm,1);gate(label+'_record_words_conserved',qpd,0.)
    gate(label+'_probe_continuity',p1d,divs[1]);gate(label+'_empty_current',emptyd,-HF*ey)
    if two:gate(label+'_source_continuity',p0d,divs[0])
    gate(label+'_energy',energy,expected,1e-8);gate(label+'_full_operator_energy',np.vdot(a,1j*ad).real,energy,1e-8)
    gate(label+'_spectral_derivative_vs_literal_action',ad,-1j*action(a,ar,two),5e-10)
    gate(label+'_q_qq',np.diag(qq),q)
    gate(label+'_clock_commutator',bd,1j*ar*bp+1j*LAM*eb*ENDM,5e-10)
    other=np.array([1,2,3,5,6,7]);gate(label+'_six_clock_phase',bp[other],initial_clock[other]*np.exp(1j*ar*x),5e-10)
    o={'norm':norm,'empty_edge_probability':empty,'empty_edge_dot':emptyd,
       'incidence_Pauli':{'X':ex,'Y':ey,'Z':ez},'incidence_Pauli_dot':{'X':2*ecdot.real,'Y':-2*ecdot.imag,'Z':2*emptyd-qpd.sum()},
       'source_p_global':p0,'probe_p_global':p1,'source_p_dot_global':p0d,'probe_p_dot_global':p1d,
       'source_density_global':rho0,'probe_density_global':rho1,'source_edge_current_cycle':currents[0],
       'probe_edge_current_cycle':currents[1],'source_current_divergence':divs[0],'probe_current_divergence':divs[1],
       'record_word_probability':qp,'record_q_global':q,'record_qq_global':qq,'endpoint_record_conditioning':sectors,
       'record_Pauli_global':{'X':bp.real,'Y':-bp.imag,'Z':norm-2*q},
       'record_Pauli_dot_global':{'X':bd.real,'Y':-bd.imag,'Z':qpd.sum()-2*(BITS@qpd)},
       'return_charge_number_probability':np.array([qp[KWORD==-k].sum() for k in range(-4,5)]),
       'Bplus_beta_global':bp,'Bplus_dot_global':bd,'Bplus_amplitude_global':abs(bp),'Bplus_rate_global':[rate(b,d) for b,d in zip(bp,bd)],
       'empty_joint_Bplus_global':eb,'Bplus_dot_charging':1j*ar*bp,'Bplus_dot_endpoint_feedback':1j*LAM*eb*ENDM,
       'original_Z_minus_iY_beta_global':old,'original_Z_minus_iY_dot_global':oldd,'original_Z_minus_iY_rate_global':[rate(b,d) for b,d in zip(old,oldd)],
       'bare_return_traced_X_global':np.zeros(8),'bare_return_traced_Y_global':np.zeros(8),
       'field_self_energy':8*norm,'carrier_storage_energy':nc*norm,'retained_record_charging_energy':charging,
       'degree_defect_energy':degree,'record_feedback_change_energy':feedback,'current_onebody_energy':currentone,
       'direct_current_cross_energy':direct,'actual_occupied_hopping_energy':hopping,'incidence_flip_energy':flip,'full_energy':energy}
    if two:
        o.update(ordered_pair_probability=pc,tagged_cycle_reference_separation_probability=np.array([pc[DIST==d].sum() for d in range(5)]),
                 tagged_cycle_reference_mean_separation=float(DIST@pc),tagged_cycle_reference_adjacency=float(ADJ@pc),actual_occupied_pair_adjacency=adj_actual,
                 empty_joint_ordered_pair_probability=prob[:,0].sum(0),empty_joint_source_probability=np.bincount(PAIRS[:,0],weights=prob[:,0].sum(0),minlength=8),
                 empty_joint_probe_probability=np.bincount(PAIRS[:,1],weights=prob[:,0].sum(0),minlength=8))
    else:
        apparatus=np.sum(abs(a.reshape(256,2,8,8,8))**2,axis=(0,1,4)).T
        dist=np.array([[min(abs(int(POS[u])-int(POS[v])),8-abs(int(POS[u])-int(POS[v]))) for v in range(8)] for u in range(8)])
        o.update(apparatus_position_probe_joint_probability=apparatus,apparatus_marker_reference_separation_probability=np.array([apparatus[dist==d].sum() for d in range(5)]),
                 apparatus_marker_reference_mean_separation=float(np.sum(dist*apparatus)),apparatus_marker_scope='Stored initial source position in the traced preparation apparatus; no moving absent source.')
        o['empty_joint_probe_probability']=prob[:,0].sum(0)
    return o

def prepare(parent_p,be,bv,re,rv,eigensha):
    name=parent_p['preparation'];nf=CP/(name+'_initial.npz');jf=CP/(name+'_initial.json')
    if nf.name in COMMITS or jf.name in COMMITS:
        if nf.name not in COMMITS or jf.name not in COMMITS:raise RuntimeError('partial initial commit requires manual recovery')
        m=read(jf)
        if m['input_map_sha256']!=input_id() or m['eigensystem_sha256']!=eigensha or m['initial_state_sha256']!=COMMITS[nf.name] or not all(c['passed'] for c in m['checks']):raise RuntimeError('initial recovery custody')
        with np.load(nf,allow_pickle=False) as z:
            on=z['psi_tagged_initial'];ref=z['psi_reference_initial'];co=z['tagged_spectral_coefficients'];cr=z['reference_spectral_coefficients'];nm=json.loads(str(z['metadata_json']))
        if nm!=m['npz_metadata']:raise RuntimeError('initial NPZ metadata')
        CHECKS.extend(m['checks']);return on,ref,co,cr,m
    begin=len(CHECKS);pm=read(PCP/(name+'_initial.json'))
    with np.load(PCP/(name+'_initial.npz'),allow_pickle=False) as z:old=z['psi_initial'];nm=json.loads(str(z['metadata_json']))
    if nm!=pm['npz_metadata'] or old.shape!=(256,2,8,8):raise RuntimeError('parent initial schema')
    on=old[:,:,PAIRS[:,0],:]/math.sqrt(7)
    expanded=np.zeros((256,2,8,8,8),complex);expanded[:,:,PAIRS[:,0],PAIRS[:,1],:]=on
    ref=np.transpose(expanded,(0,1,3,2,4)).reshape(256,2,8,64)
    gate(name+'_insertion_isometry_Gram',on.reshape(28672,8).conj().T@on.reshape(28672,8),old.reshape(4096,8).conj().T@old.reshape(4096,8))
    gate(name+'_paired_reference_exact_channel',ref.reshape(256,2,8,8,8),np.transpose(expanded,(0,1,3,2,4)),5e-10)
    rhos,rhop=carriers(on,True);_,rhor=carriers(ref,False);_,rho_old=carriers(old,False)
    gate(name+'_initial_probe_marginal',rhop,rhor)
    disturbed=rho_old*(6/7);np.fill_diagonal(disturbed,np.diag(rho_old))
    gate(name+'_source_preparation_coherence_disturbance',rhos,disturbed)
    ar=float(F(parent_p['AR_rational']));ado=-1j*action(on,ar,True);adr=-1j*action(ref,ar,False)
    bpo=clocks(on,ado)[0];bpr=clocks(ref,adr)[0];oldbp=cv(pm['initial_clock_Bplus_global'])
    gate(name+'_record_clock_preserved_by_insertion',bpo,oldbp);gate(name+'_record_clock_preserved_by_reference_channel',bpr,bpo)
    eon=float(np.vdot(on,1j*ado).real);eref=float(np.vdot(ref,1j*adr).real);eold=pm['expected_post_switch_energy']
    adjacency=np.zeros((8,8))
    for u,v in EDGES:adjacency[u,v]=adjacency[v,u]=1
    predicted=83/70+float(np.trace(rho_old@adjacency).real)/70
    gate(name+'_insertion_work_complete',eon-eold,predicted,1e-8)
    exact(name+'_insertion_work_bounds',81/70-1e-8<=eon-eold<=85/70+1e-8)
    gate(name+'_occupied_anchor_initial',np.linalg.norm(on[:,0])+np.linalg.norm(ref[:,0]),0.)
    co=transform(on.reshape(256,112,8),bv,True);cr=transform(ref.reshape(256,16,64),rv,True)
    gate(name+'_tagged_initial_resolution',transform(co,bv),on.reshape(256,112,8),5e-10)
    gate(name+'_reference_initial_resolution',transform(cr,rv),ref.reshape(256,16,64),5e-10)
    meta={'preparation':name,'case':parent_p['case'],'preparation_time_index':parent_p['preparation_time_index'],
          'preparation_x_rational':parent_p['preparation_x_rational'],'AR_rational':parent_p['AR_rational'],
          'formation_gamma_rational':parent_p['formation_gamma_rational'],'eigensystem_sha256':eigensha,
          'parent_initial_state_sha256':parent_p['initial_state_sha256'],'input_map_sha256':input_id()}
    nh=commit_npz(nf,'preparation_state_saved',psi_tagged_initial=on,psi_reference_initial=ref,
                  tagged_spectral_coefficients=co,reference_spectral_coefficients=cr,metadata_json=np.array(json.dumps(meta,sort_keys=True)))
    m={**meta,'npz_metadata':meta,'initial_state_sha256':nh,'initial_clock_Bplus_global':clean(bpo),
       'record_word_probability':clean(np.sum(abs(on)**2,axis=(1,2,3))),'source_preparation_density_global':clean(rhos),
       'probe_preparation_density_global':clean(rhop),'copy_off_work':pm['copy_off_work'],'parent_post_copy_off_energy':eold,
       'insertion_work':eon-eold,'source_removal_reference_work':eref-eon,'net_reference_preparation_work':eref-eold,
       'initial_tagged_energy':eon,'initial_reference_energy':eref,'ideal_clock_structural_null':pm['ideal_Bplus_structural_null'],
       'initial_release_flip_mean_work':0.,'checks':list(CHECKS[begin:])}
    commit(jf,m,'preparation_metadata_saved');return on,ref,co,cr,m

def evolve(coeff,ev,vec,ar,x,dim):
    absolute=ev[ESUM]+ar*POP[:,None];amp=coeff*np.exp(-1j*absolute*x)[:,:,None]
    a=transform(amp,vec).reshape(256,2,dim,coeff.shape[-1])
    ad=transform(-1j*absolute[:,:,None]*amp,vec).reshape(a.shape)
    return a,ad
def run_preparation(p,be,bv,re,rv,eigensha):
    name=p['preparation'];complete=CP/(name+'_complete.json')
    on0,ref0,co,cr,m=prepare(p,be,bv,re,rv,eigensha)
    if complete.name in COMMITS:
        s=read(complete)
        if s['input_map_sha256']!=input_id() or s['initial_state_sha256']!=m['initial_state_sha256'] or len(s['rows'])!=4:raise RuntimeError('completed prep recovery')
        for row in s['rows']:
            if row['state_sha256']!=COMMITS.get(row['state_file']) or read(CP/row['row_file'])!=row or not all(c['passed'] for c in row['checks']):raise RuntimeError('completed frame custody')
            CHECKS.extend(row['checks'])
        return s
    ar=float(F(p['AR_rational']));b0=cv(m['initial_clock_Bplus_global']);rows=[];begun=time.monotonic()
    for ri,xf in enumerate(TIMES):
        ACTIVE.update(preparation=name,forward_time=float(xf),stage='new_tagged_and_reference_frame')
        nf=CP/(name+'_forward%02d.npz'%ri);jf=CP/(name+'_forward%02d.json'%ri)
        if nf.name in COMMITS or jf.name in COMMITS:
            if nf.name not in COMMITS or jf.name not in COMMITS:raise RuntimeError('partial frame commit requires separate recovery')
            row=read(jf)
            if row['input_map_sha256']!=input_id() or row['preparation']!=name or row['forward_time_index']!=ri or row['x_rational']!=str(xf) or row['state_sha256']!=COMMITS[nf.name] or not all(c['passed'] for c in row['checks']):raise RuntimeError('frame recovery mismatch/failure')
            CHECKS.extend(row['checks']);rows.append(row);continue
        begin=len(CHECKS);x=float(xf)
        on,ond=evolve(co,be,bv,ar,x,56);ref,refd=evolve(cr,re,rv,ar,x,8)
        if ri==0:
            gate(name+'_forward0_tagged',on,on0,5e-10);gate(name+'_forward0_reference',ref,ref0,5e-10)
            on=on0.copy();ref=ref0.copy()
        label=name+'_forward%02d'%ri
        oo=obs(on,ond,ar,True,b0,m['initial_tagged_energy'],label+'_on',x)
        ro=obs(ref,refd,ar,False,b0,m['initial_reference_energy'],label+'_ref',x)
        gate(label+'_tagged_record_probability',oo['record_word_probability'],m['record_word_probability'])
        gate(label+'_reference_record_probability',ro['record_word_probability'],m['record_word_probability'])
        gate(label+'_six_common_formed_clocks',oo['Bplus_beta_global'][[1,2,3,5,6,7]],ro['Bplus_beta_global'][[1,2,3,5,6,7]],5e-10)
        gate(label+'_tagged_spectral_probability',abs(transform(on.reshape(256,112,8),bv,True))**2,abs(co)**2,5e-10)
        gate(label+'_reference_spectral_probability',abs(transform(ref.reshape(256,16,64),rv,True))**2,abs(cr)**2,5e-10)
        gate(label+'_tagged_Gram',on.reshape(28672,8).conj().T@on.reshape(28672,8),on0.reshape(28672,8).conj().T@on0.reshape(28672,8))
        gate(label+'_reference_Gram',ref.reshape(4096,64).conj().T@ref.reshape(4096,64),ref0.reshape(4096,64).conj().T@ref0.reshape(4096,64))
        if m['ideal_clock_structural_null']:
            gate(label+'_on_structural_clock_null',oo['Bplus_beta_global'],0.,5e-10);gate(label+'_ref_structural_clock_null',ro['Bplus_beta_global'],0.,5e-10)
        diff={'probe_p_global':np.asarray(oo['probe_p_global'])-np.asarray(ro['probe_p_global']),
              'probe_density_global':np.asarray(oo['probe_density_global'])-np.asarray(ro['probe_density_global']),
              'probe_edge_current_cycle':np.asarray(oo['probe_edge_current_cycle'])-np.asarray(ro['probe_edge_current_cycle']),
              'empty_edge_probability':oo['empty_edge_probability']-ro['empty_edge_probability'],
              'endpoint_Bplus_difference':np.asarray(oo['Bplus_beta_global'])[[0,4]]-np.asarray(ro['Bplus_beta_global'])[[0,4]]}
        if ri==0:gate(label+'_matched_probe_initial_difference',diff['probe_density_global'],0.)
        meta={'preparation':name,'case':p['case'],'preparation_time_index':p['preparation_time_index'],
              'preparation_x_rational':p['preparation_x_rational'],'AR_rational':p['AR_rational'],
              'formation_gamma_rational':p['formation_gamma_rational'],'forward_time_index':ri,'x_rational':str(xf),
              'input_map_sha256':input_id(),'initial_state_sha256':m['initial_state_sha256'],'eigensystem_sha256':eigensha}
        nh=commit_npz(nf,'paired_frame_state_saved',psi_tagged=on,psi_reference=ref,metadata_json=np.array(json.dumps(meta,sort_keys=True)))
        row={**meta,'state_file':nf.name,'state_sha256':nh,'row_file':jf.name,'tagged':clean(oo),'paired_reference':clean(ro),
             'source_presence_difference':clean(diff),'copy_off_work':m['copy_off_work'],'insertion_work':m['insertion_work'],
             'source_removal_reference_work':m['source_removal_reference_work'],'ideal_clock_structural_null':m['ideal_clock_structural_null'],
             'scope':'Source presence with recoil, hard core and accounted channel; direct current and retained-record effects not identified as gravity.',
             'checks':list(CHECKS[begin:])}
        commit(jf,row,'paired_frame_metadata_saved');rows.append(row);del on,ond,ref,refd
    s={**{k:m[k] for k in ('preparation','case','preparation_time_index','preparation_x_rational','AR_rational','formation_gamma_rational','initial_state_sha256','input_map_sha256','copy_off_work','insertion_work','source_removal_reference_work','initial_tagged_energy','initial_reference_energy')},
       'rows':rows,'elapsed_seconds_this_preparation':time.monotonic()-begun,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    commit(complete,s,'preparation_complete')
    print(json.dumps({'preparation':name,'paired_frames':4,'checks':len(CHECKS),'failed':sum(not c['passed'] for c in CHECKS)},sort_keys=True),flush=True)
    return s

def main():
    global APPEND_ALLOWED
    if sys.argv[1:] not in (['--execute'],['--resume']):raise SystemExit('Requires exact --execute or root-authorized manual --resume; no calculation performed.')
    parent=authenticate();begun=time.monotonic()
    if sys.argv[1]=='--execute':
        if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)):raise RuntimeError('reserved output exists; preserve/recover first')
        CP.mkdir();APPEND_ALLOWED=True
        manifest={'PID':os.getpid(),'input_sha256':dict(INPUTS),'parameters':parameters(),'Python':sys.version,'NumPy':np.__version__,
                  'threads':{k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}}
        mh=write_json(CP/'manifest.json',manifest);COMMITS['manifest.json']=mh;event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':dict(INPUTS)})
    else:
        manifest=resume_preflight();mh=sha(CP/'manifest.json');APPEND_ALLOWED=True
        event({'event':'resume_started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':dict(INPUTS)})
    be,bv,re,rv,eh=eigensystems();preps=[run_preparation(p,be,bv,re,rv,eh) for p in parent['preparations']]
    exact('whole_unselected_104_by4_paired_census',len(preps)==104 and all(len(p['rows'])==4 for p in preps))
    # Identical blank controls must match without imposing their measured values.
    baseline=preps[0]
    for p in preps:
        if p['formation_gamma_rational']!='0':continue
        for ri,row in enumerate(p['rows']):
            for branch in ('tagged','paired_reference'):
                for k in ('probe_p_global','empty_edge_probability','full_energy'):
                    gate(p['preparation']+'_blank_'+branch+'_'+k+'_%d'%ri,row[branch][k],baseline['rows'][ri][branch][k])
    recheck();passed=sum(c['passed'] for c in CHECKS);failed=sum(not c['passed'] for c in CHECKS)
    status='QUALIFIED_ARITHMETIC_MATCHED_TAGGED_REACTION_NO_GRAVITY_ADOPTION' if failed==0 else 'ARITHMETIC_FAILED'
    result={'status':status,'passed':passed,'failed':failed,'checks':list(CHECKS),'preparations':preps,
            'input_sha256':dict(INPUTS),'manifest_sha256':mh,'PID':os.getpid(),'original_manifest_PID':manifest['PID'],
            'elapsed_seconds_this_execution':time.monotonic()-begun,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'All104 matched channels and416 paired frames; no physical distance, universal force, metric, proper clock, phase or observational comparison adopted.'}
    raw=write_json(RESULT,result);canonical=hashlib.sha256(blob(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':canonical})
    lines=['# Floating-return tagged probe reaction V001','',status+': %d/%d arithmetic checks;104 preparations,416 tagged and416 paired reference frames.'%(passed,len(CHECKS)),
           '','Signed source-presence differences include direct current, exclusion, recoil and retained-record geometry. Binding is not a gravity-success gate.',
           'Pair separation uses the supplied cycle coordinate; the absent-source reference marker is the stored apparatus coordinate. Full work and clock nulls remain.',
           '','| Preparation | AR | prep x | forward x | tagged adjacency | tagged mean steps | probe density difference norm | on empty | ref empty | insertion work | removal work |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in preps:
        for row in p['rows']:
            d=cv(row['source_presence_difference']['probe_density_global']);o=row['tagged'];r=row['paired_reference']
            lines.append('|%s|%s|%s|%s|%.10g|%.10g|%.10g|%.10g|%.10g|%.10g|%.10g|'%(p['preparation'],p['AR_rational'],p['preparation_x_rational'],row['x_rational'],o['tagged_cycle_reference_adjacency'],o['tagged_cycle_reference_mean_separation'],np.linalg.norm(d),o['empty_edge_probability'],r['empty_edge_probability'],p['insertion_work'],p['source_removal_reference_work']))
    if sum(x.startswith('|') for x in lines)!=418:raise RuntimeError('report fixed416 data-row guard')
    lines+=['','Raw result SHA256: '+raw,'Canonical result SHA256: '+canonical,'No favorable reaction direction, retained-record mediation or gravitational law is inferred from arithmetic qualification.']
    with REPORT.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    recheck();rh=sha(REPORT);event({'event':'report_saved','sha256':rh,'paired_data_rows':416})
    cmap={p.name:sha(p) for p in sorted(CP.iterdir()) if p.name!='journal.jsonl'}
    receipt={'status':status,'passed':passed,'failed':failed,'input_sha256':dict(INPUTS),'checkpoint_sha256':cmap,
             'result_raw_sha256':raw,'result_canonical_sha256':canonical,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),
             'PID':os.getpid(),'original_manifest_PID':manifest['PID'],'elapsed_seconds_this_execution':result['elapsed_seconds_this_execution'],'peakRSS_bytes':result['peakRSS_bytes']}
    rr=write_json(RECEIPT,receipt);event({'event':'receipt_saved','sha256':rr})
    print(json.dumps({'status':status,'passed':passed,'failed':failed,'raw_sha256':raw,'receipt_sha256':rr},sort_keys=True),flush=True)
    return 0 if failed==0 else 3

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        if not APPEND_ALLOWED:
            print(json.dumps({'status':'PREFLIGHT_REJECTED_NO_OUTPUT_MUTATION','error':repr(exc)}),flush=True);raise SystemExit(3)
        v={'error':repr(exc),'traceback':traceback.format_exc(),'active':dict(ACTIVE),'PID':os.getpid(),'checks':list(CHECKS),'input_sha256':dict(INPUTS),'committed_sha256':dict(COMMITS)}
        if not ERROR.exists():eh=write_json(ERROR,v);event({'event':'error','external_error_sha256':eh,'PID':os.getpid(),'active':dict(ACTIVE)})
        else:
            ix=sum(1 for p in CP.glob('error_attempt_*.json'))+1;commit(CP/('error_attempt_%03d_PID%d.json'%(ix,os.getpid())),v,'error_attempt_saved')
        print(json.dumps({'status':'ERROR_PRESERVED','error':repr(exc),'active':ACTIVE},sort_keys=True),flush=True);raise SystemExit(3)
