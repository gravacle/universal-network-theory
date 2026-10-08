#!/usr/bin/env python3
"""New network-port energy-lapse source on sealed preparations; root launches.
No eigensolver, baseline propagation, old producer import or preparation replay.
All reduced N contacts vanish in this declared fixed-code affine source class.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'
import sys,json,hashlib,math,time,resource,traceback,re
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001'
STEM='floating_return_c8_localized_lapse_response_v001'
CP=J/(STEM+'_checkpoints')
RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md');RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PROTOCOL_SHA='84a212a3da0fe97b1391dde1a8f6dd50db98a958f0e6ae8c676ef78bf2bfe70b'
OLDNAME='FLOATING_RETURN_C8_RETARDED_INCIDENCE_CURRENT_V001';OLDSTEM='floating_return_c8_retarded_incidence_current_v001'
PACKETS=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','floating_return_c8_tagged_probe_reaction_v001'),('FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001','floating_return_c8_endpoint_record_isolation_v001'))
TIMES=(F(0),F(1,5),F(2),F(8));PAIRTIMES=tuple((i,k) for i in range(4) for k in range(i+1))
H=.2;T=.1;JC=.25;LAM=.5
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple((CYCLE[k],CYCLE[(k+1)%8]) for k in range(8))
PAIRS=np.array([(a,b) for a in range(8) for b in range(8) if a!=b],dtype=np.int64)
PIND={tuple(p):i for i,p in enumerate(PAIRS)};OCC=np.array([[(int(a)==v)+(int(b)==v) for a,b in PAIRS] for v in range(8)])
TRANS=[]
for u,v in EDGES:
    TRANS.append((np.array([(PIND[(u,b)],PIND[(v,b)]) for b in range(8) if b not in (u,v)],dtype=np.int64),np.array([(PIND[(a,u)],PIND[(a,v)]) for a in range(8) if a not in (u,v)],dtype=np.int64)))
REST=(1,2,3,5,6,7);KINDS=('Vc','Vm','H')
OP_TOL=5e-10;OBS_TOL=1e-9;ENERGY_TOL=5e-9
CHECKS=[];INPUTS={};COMMITS={};APPEND_ALLOWED=False;ACTIVE={}
PHYSICAL_UNITS={'native_hbar':1,'native_age':'x=Eunit*t_physical/hbar','native_frequency':'omega_native=hbar*omega_physical/Eunit',
 'Phi_vertex_prefactor':'Eunit/c_p^2','Phi_causal_kernel_prefactor':'Eunit^2/(hbar*c_p^4)',
 'Phi_integrated_or_Fourier_kernel_prefactor':'Eunit/c_p^4','Eunit_selected':False,'c_p_selected':False,
 'source_scope':'modeled network plus assigned Crel charging/return cells; removed/reset apparatus are source-independent external references; their proper T00 is unowned'}


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


def cv(v):
    a=np.asarray(v,dtype=float);return a[...,0]+1j*a[...,1]


def input_id():return hashlib.sha256(blob(INPUTS)).hexdigest()


def recheck():
    for f,h in INPUTS.items():
        if sha(ROOT/f)!=h:raise RuntimeError('input changed: '+f)


def authenticate_packet(name,stem):
    cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'));a=read(J/(name+'_AUDIT.json'))
    if r['result_raw_sha256']!=sha(J/(name+'_RESULT.json')) or r['result_canonical_sha256']!=hashlib.sha256(blob(p)).hexdigest() or r['report_sha256']!=sha(J/(name+'_RESULT.md')):raise RuntimeError('parent result/canonical/report '+name)
    if p['input_sha256']!=r['input_sha256'] or p['passed']!=r['passed'] or p['failed']!=r['failed'] or p['failed']!=0 or not all(c['passed'] for c in p['checks']):raise RuntimeError('parent controls '+name)
    if a['audit_status']!='PASS' or a['failed_assertions']!=0 or a['result_raw_sha256']!=r['result_raw_sha256'] or a['receipt_sha256']!=sha(J/(name+'_RECEIPT.json')) or a['audited_preparations']!=104:raise RuntimeError('parent independent audit identity '+name)
    if name==PACKETS[0][0]:
        if a['audited_tagged_frames']!=416 or a['audited_paired_reference_frames']!=416:raise RuntimeError('tagged audit frame census')
    elif a['audited_reset_tagged_frames']!=416 or a['audited_reset_reference_frames']!=416 or a['retained_parent_pairs']!=416:raise RuntimeError('endpoint audit frame census')
    for f,h in r['input_sha256'].items():
        if sha(ROOT/f)!=h:raise RuntimeError('inherited input '+f)
        INPUTS[f]=h
    cmap=r['checkpoint_sha256'];actual={x.name for x in cp.iterdir() if x.name!='journal.jsonl'}
    if len(cmap)!=1146 or actual!=set(cmap):raise RuntimeError('parent1146 map '+name)
    for f,h in cmap.items():
        if sha(cp/f)!=h:raise RuntimeError('parent checkpoint '+f)
        INPUTS[str((cp/f).relative_to(ROOT))]=h
    jb=(cp/'journal.jsonl').read_bytes();es=[json.loads(x) for x in jb.splitlines()]
    if len(es)!=1149 or hashlib.sha256(b'\n'.join(jb.splitlines()[:-1])+b'\n').hexdigest()!=r['journal_prefix_sha256']:raise RuntimeError('parent journal '+name)
    if es[-1]!={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))} or es[-2]!={'event':'report_saved','sha256':r['report_sha256'],'paired_data_rows':416} or es[-3]!={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']}:raise RuntimeError('parent final commits '+name)
    m=read(cp/'manifest.json')
    if p['manifest_sha256']!=sha(cp/'manifest.json') or es[0]['manifest_sha256']!=sha(cp/'manifest.json') or m['input_sha256']!=r['input_sha256'] or es[0]['input_sha256']!=r['input_sha256'] or es[0]['PID']!=m['PID'] or m['PID']!=r['original_manifest_PID']:raise RuntimeError('parent manifest/start '+name)
    commits={'manifest.json':sha(cp/'manifest.json')}
    for e in es[1:-3]:
        if 'file' not in e or 'sha256' not in e or e['file'] in commits:raise RuntimeError('parent stage commit '+name)
        commits[e['file']]=e['sha256']
    if commits!=cmap or len(p['preparations'])!=104:raise RuntimeError('parent census '+name)
    for pi,prep in enumerate(p['preparations']):
        label='case%02d_prep%02d'%divmod(pi,13)
        if prep['preparation']!=label or len(prep['rows'])!=4 or read(cp/(label+'_complete.json'))!=prep:raise RuntimeError('parent104 completed rows')
        im=read(cp/(label+'_initial.json'))
        if im['initial_state_sha256']!=cmap[label+'_initial.npz'] or im['input_map_sha256']!=hashlib.sha256(blob(r['input_sha256'])).hexdigest() or not all(c['passed'] for c in im['checks']):raise RuntimeError('parent initial seal')
        for k,row in enumerate(prep['rows']):
            if row['forward_time_index']!=k or row['x_rational']!=str(TIMES[k]) or read(cp/row['row_file'])!=row or row['state_sha256']!=cmap[row['state_file']] or row['input_map_sha256']!=hashlib.sha256(blob(r['input_sha256'])).hexdigest() or not all(c['passed'] for c in row['checks']):raise RuntimeError('parent frame seal')
    INPUTS[str((cp/'journal.jsonl').relative_to(ROOT))]=sha(cp/'journal.jsonl')
    return p


def setup_mode(reset,two,ar):
    words=np.array([sum(((r>>k)&1)<<v for k,v in enumerate(REST)) for r in range(64)]) if reset else np.arange(256)
    bits=np.array([[(int(q)>>v)&1 for q in words] for v in range(8)]);s=bits[0]+bits[4]
    return {'reset':reset,'two':two,'ar':ar,'words':words,'bits':bits,'pop':bits.sum(0),'s':s,'groups':tuple(np.flatnonzero(s==k) for k in range(3)),'dim':56 if two else 8}


def literal_h(a,m):
    nc=2 if m['two'] else 1;out=(8+nc+m['ar']*m['pop'])[:,None,None,None]*a
    out[:,0]+=(2+LAM*m['s'])[:,None,None]*a[:,0]
    for k,(u,v) in enumerate(EDGES):
        for bit in ((1,) if k==0 else (0,1)):
            diag=OCC[u]+OCC[v]-2*OCC[u]*OCC[v] if m['two'] else np.eye(8,dtype=int)[u]+np.eye(8,dtype=int)[v]
            out[:,bit]+=JC*diag[None,:,None]*a[:,bit]
            if m['two']:
                for transitions in TRANS[k]:
                    l,r=transitions.T;out[:,bit,l]-=T*a[:,bit,r];out[:,bit,r]-=T*a[:,bit,l]
            else:out[:,bit,u]-=T*a[:,bit,v];out[:,bit,v]-=T*a[:,bit,u]
    return out-H*a[:,::-1]


def transform(a,vec,m,inverse=False):
    z=np.empty_like(a);d=a.shape[1];c=a.shape[2]
    for s,qs in enumerate(m['groups']):
        if len(qs)==0:continue
        v=vec[s].conj().T if inverse else vec[s];x=a[qs].transpose(1,0,2).reshape(d,-1)
        z[qs]=(v@x).reshape(d,len(qs),c).transpose(1,0,2)
    return z


def coefficients(a,vec,m):return transform(a.reshape(len(m['words']),2*m['dim'],a.shape[-1]),vec,m,True)


def source_column(c,ev,vec,m,delta):
    energy=ev[m['s']]+m['ar']*m['pop'][:,None]
    return transform(c*np.exp(-1j*energy*delta)[:,:,None],vec,m).reshape(len(m['words']),2,m['dim'],c.shape[-1])


def expectation(o,a):return float(np.vdot(a,o).real)

def register(path,digest):
    p=Path(path).resolve();key=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    if key in INPUTS:
        if INPUTS[key]!=digest:raise RuntimeError('inconsistent input seal '+key)
        return
    if sha(p)!=digest:raise RuntimeError('input seal '+str(p))
    INPUTS[key]=digest


def authenticate_old_response():
    p=read(J/(OLDNAME+'_RESULT.json'));r=read(J/(OLDNAME+'_RECEIPT.json'));a=read(J/(OLDNAME+'_AUDIT.json'));cp=J/(OLDSTEM+'_checkpoints')
    if r['result_raw_sha256']!=sha(J/(OLDNAME+'_RESULT.json')) or r['result_canonical_sha256']!=hashlib.sha256(blob(p)).hexdigest() or r['report_sha256']!=sha(J/(OLDNAME+'_RESULT.md')):raise RuntimeError('old response result/canonical/report')
    if p['input_sha256']!=r['input_sha256'] or p['passed']!=r['passed'] or p['failed']!=r['failed'] or p['failed'] or len(p['checks'])!=80331 or not all(c['passed'] for c in p['checks']):raise RuntimeError('old response80331 arithmetic')
    if a['audit_status']!='PASS' or a['failed_assertions'] or a['result_raw_sha256']!=r['result_raw_sha256'] or a['receipt_sha256']!=sha(J/(OLDNAME+'_RECEIPT.json')) or a['audited_preparations']!=104 or a['audited_source_frames']!=1664 or a['audited_channel_time_rows']!=4160:raise RuntimeError('accepted old response audit')
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    cmap=r['checkpoint_sha256']
    if len(cmap)!=7594 or set(cmap)!={x.name for x in cp.iterdir() if x.name!='journal.jsonl'}:raise RuntimeError('old response7594 checkpoints')
    for f,h in cmap.items():register(cp/f,h)
    jb=(cp/'journal.jsonl').read_bytes();lines=jb.splitlines();events=[json.loads(x) for x in lines]
    if len(events)!=7597 or hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()!=r['journal_prefix_sha256']:raise RuntimeError('old response7597 prefix')
    if events[-1]!={'event':'receipt_saved','sha256':sha(J/(OLDNAME+'_RECEIPT.json'))} or events[-2]!={'event':'report_saved','sha256':r['report_sha256'],'data_rows':4160} or events[-3]!={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']}:raise RuntimeError('old response final commits')
    manifest=read(cp/'manifest.json')
    if p['manifest_sha256']!=sha(cp/'manifest.json') or manifest['input_sha256']!=r['input_sha256'] or events[0]!={'event':'started','PID':p['PID'],'manifest_sha256':p['manifest_sha256'],'input_sha256':r['input_sha256']} or manifest['PID']!=r['PID']:raise RuntimeError('old response manifest/start')
    commits={'manifest.json':p['manifest_sha256']}
    for e in events[1:-3]:
        if 'file' not in e or 'sha256' not in e or e['file'] in commits:raise RuntimeError('old response unique commit')
        commits[e['file']]=e['sha256']
    if commits!=cmap or len(p['preparations'])!=104 or any(len(x['channels'])!=4 or any(len(c['rows'])!=10 for c in x['channels']) for x in p['preparations']):raise RuntimeError('old response fixed census')
    register(cp/'journal.jsonl',sha(cp/'journal.jsonl'))


def authenticate():
    protocol=J/(NAME+'.md')
    if sha(protocol)!=PROTOCOL_SHA:raise RuntimeError('unfrozen localized protocol')
    anchors=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',protocol.read_text(),re.M)
    if len(anchors)!=18:raise RuntimeError('required18 direct pins')
    for f,h in anchors:register(ROOT/f if f.startswith('program-worktree/') else J/f,h)
    register(protocol,PROTOCOL_SHA);register(__file__,sha(__file__))
    authenticate_old_response()
    parents=[authenticate_packet(*p) for p in PACKETS]
    # Current parent result/report/audit maps are explicit even if inherited.
    for name,stem in PACKETS:
        for suffix in ('_RESULT.json','_RESULT.md','_RECEIPT.json','_AUDIT.json','_AUDIT.md'):register(J/(name+suffix),sha(J/(name+suffix)))
    return parents


def local_vertex(a,m,node=0,midpoint=False):
    """Literal complete node source from local charging plus edge ownership."""
    bits=m['bits'];q=bits[node];d=m['dim'];occ=OCC if m['two'] else np.eye(8,dtype=int)
    out=(1+m['ar']*q)[:,None,None,None]*a
    if node in (0,4):out[:,0]+=(1+LAM*q)[:,None,None]*a[:,0]
    out+=occ[node][None,None,:,None]*a
    for k,(u,v) in enumerate(EDGES):
        if node not in (u,v):continue
        cut=occ[u]+occ[v]-2*occ[u]*occ[v]
        for bit in ((1,) if k==0 else (0,1)):
            out[:,bit]+=(JC/2)*cut[None,:,None]*a[:,bit]
            if m['two']:
                for moves in TRANS[k]:
                    l,r=moves.T;out[:,bit,l]-=(T/2)*a[:,bit,r];out[:,bit,r]-=(T/2)*a[:,bit,l]
            else:out[:,bit,u]-=(T/2)*a[:,bit,v];out[:,bit,v]-=(T/2)*a[:,bit,u]
            if midpoint:
                g=(LAM/2)*(bits[u]-bits[v])*(1 if node==u else -1)
                out[:,bit]+=g[:,None,None]*a[:,bit]
        if k==0:out-=(H/2)*a[:,::-1]
    return out


def compact_vertex0(a,m,midpoint=False):
    """Independent Eq4 construction; never defines the vertex through a Ward."""
    q0,q4,q5=m['bits'][[0,4,5]];occ=OCC if m['two'] else np.eye(8,dtype=int)
    out=(1+m['ar']*q0)[:,None,None,None]*a
    out[:,0]+=(1+q0/2)[:,None,None]*a[:,0];out+=occ[0][None,None,:,None]*a
    for k,v in ((0,4),(7,5)):
        cut=occ[0]+occ[v]-2*occ[0]*occ[v]
        for bit in ((1,) if k==0 else (0,1)):
            out[:,bit]+=(JC/2)*cut[None,:,None]*a[:,bit]
            if m['two']:
                for moves in TRANS[k]:
                    l,r=moves.T;out[:,bit,l]-=(T/2)*a[:,bit,r];out[:,bit,r]-=(T/2)*a[:,bit,l]
            else:out[:,bit,0]-=(T/2)*a[:,bit,v];out[:,bit,v]-=(T/2)*a[:,bit,0]
    out-=(H/2)*a[:,::-1]
    if midpoint:
        out+=(q0-q5)[:,None,None,None]*a/4
        out[:,1]+=(q0-q4)[:,None,None]*a[:,1]/4
    return out


def delta_vertex(a,m):
    out=-(m['bits'][0]-m['bits'][5])[:,None,None,None]*a/4
    out[:,1]-=(m['bits'][0]-m['bits'][4])[:,None,None]*a[:,1]/4
    return out


def record_beta(a,m):
    result=np.zeros(8,complex);lookup={int(q):i for i,q in enumerate(m['words'])}
    for v in range(8):
        low=[i for i,q in enumerate(m['words']) if not (int(q)>>v)&1 and (int(q)+(1<<v)) in lookup]
        high=[lookup[int(m['words'][i])+(1<<v)] for i in low]
        if low:result[v]=2*np.vdot(a[high],a[low])
    return result


def record_source_dot(a,va,m):
    result=np.zeros(8,complex);lookup={int(q):i for i,q in enumerate(m['words'])}
    for v in range(8):
        low=[i for i,q in enumerate(m['words']) if not (int(q)>>v)&1 and (int(q)+(1<<v)) in lookup]
        high=[lookup[int(m['words'][i])+(1<<v)] for i in low]
        if low:result[v]=2j*(np.vdot(va[high],a[low])-np.vdot(a[high],va[low]))
    return result


def predicted_clock_source(a,m,midpoint=False):
    beta=record_beta(a,m);result=np.zeros(8,complex)
    # Candidate derivative is localized at node0; actual empty-edge correlation.
    result[0]=1j*(m['ar']*beta[0]+LAM*record_beta(a*np.array([1,0])[None,:,None,None],m)[0])
    if midpoint:
        occupied_beta=record_beta(a*np.array([0,1])[None,:,None,None],m)
        result[0]+=1j*(beta[0]+occupied_beta[0])/4
        result[4]-=1j*occupied_beta[4]/4;result[5]-=1j*beta[5]/4
    return result


def bases():
    cp=J/(PACKETS[0][1]+'_checkpoints')
    with np.load(cp/'reaction_eigensystems.npz',allow_pickle=False) as z:
        values=tuple(z[k].copy() for k in ('tagged_base_eigenvalues','tagged_base_eigenvectors','reference_base_eigenvalues','reference_base_eigenvectors','tagged_base_matrices','reference_base_matrices'))
        gate('authentic_global_cycle',z['cycle_global_nodes'],CYCLE,0.)
        gate('authentic_ordered_tagged_pairs',z['ordered_tagged_pairs'],PAIRS,0.)
        gate('authentic_all_global_q_bits',z['global_record_bits'],np.array([[(q>>v)&1 for q in range(256)] for v in range(8)]),0.)
    be,bv,re,rv,bh,rh=values;integral_bases=[]
    for label,ev,vec,hs,d,two in (('tagged',be,bv,bh,56,True),('reference',re,rv,rh,8,False)):
        mm=setup_mode(False,two,0.)
        mm={**mm,'words':np.array([0]),'bits':np.zeros((8,1),int),'pop':np.array([0]),'s':np.array([0])}
        vb=compact_vertex0(np.eye(2*d,dtype=complex).reshape(1,2,d,2*d),mm).reshape(2*d,2*d)
        pe=np.diag(np.r_[np.ones(d),np.zeros(d)])
        integral_bases.append((np.array([v.conj().T@vb@v for v in vec]),np.array([v.conj().T@pe@v for v in vec])))
        for s,q in enumerate((0,1,17)):
            m=setup_mode(False,two,0.);m={**m,'words':np.array([q]),'bits':np.array([[(q>>v)&1] for v in range(8)]),'pop':np.array([q.bit_count()]),'s':np.array([s]),'groups':(np.array([0]) if s==0 else np.array([],int),np.array([0]) if s==1 else np.array([],int),np.array([0]) if s==2 else np.array([],int))}
            a=vec[s].reshape(1,2,d,2*d);ha=literal_h(a,m)
            gate(label+'_full_literal_saved_mode_action_%d'%s,ha.reshape(2*d,2*d),hs[s]@vec[s],OP_TOL)
            gate(label+'_all_reused_eigenmodes_%d'%s,hs[s]@vec[s],vec[s]*ev[s][None,:],OP_TOL)
            gate(label+'_mode_Gram_%d'%s,vec[s].conj().T@vec[s],np.eye(2*d),OP_TOL)
            gate(label+'_full_Hermitian_%d'%s,hs[s],hs[s].conj().T,OP_TOL)
        # Literal all-node sum for all256 words and all4 absolute AR shifts.
        for ar in (0.,.125,.175,.25):
            m=setup_mode(False,two,ar);a=np.broadcast_to(np.eye(2*d,dtype=complex).reshape(1,2,d,2*d),(256,2,d,2*d))
            ha=literal_h(a,m);summed=np.zeros_like(ha);mid=np.zeros_like(ha)
            for node in range(8):summed+=local_vertex(a,m,node);mid+=local_vertex(a,m,node,True)
            gate(label+'_allq_AR_%s_cap_sum_H'%ar,summed,ha,OP_TOL)
            gate(label+'_allq_AR_%s_mid_sum_H'%ar,mid,ha,OP_TOL)
            cc=compact_vertex0(a,m);cm=compact_vertex0(a,m,True)
            gate(label+'_allq_AR_%s_literal_Vc'%ar,cc,local_vertex(a,m),OP_TOL)
            gate(label+'_allq_AR_%s_literal_Vm'%ar,cm,local_vertex(a,m,0,True),OP_TOL)
            gate(label+'_allq_AR_%s_exact_allocation_difference'%ar,cc-cm,delta_vertex(a,m),OP_TOL)
            gate(label+'_allq_AR_%s_Vc_Hermitian'%ar,cc.reshape(256,2*d,2*d),cc.reshape(256,2*d,2*d).conj().transpose(0,2,1),OP_TOL)
            gate(label+'_allq_AR_%s_Vm_Hermitian'%ar,cm.reshape(256,2*d,2*d),cm.reshape(256,2*d,2*d).conj().transpose(0,2,1),OP_TOL)
            del a,ha,summed,mid,cc,cm
    commit_npz(CP/'reused_localized_response_bases.npz','bases_saved',tagged_eigenvalues=be,tagged_eigenvectors=bv,tagged_base_matrices=bh,
               reference_eigenvalues=re,reference_eigenvectors=rv,reference_base_matrices=rh,global_record_bits=np.array([[(q>>v)&1 for q in range(256)] for v in range(8)]),
               tagged_bare_Vc_eigenbasis=integral_bases[0][0],tagged_Pempty_eigenbasis=integral_bases[0][1],reference_bare_Vc_eigenbasis=integral_bases[1][0],reference_Pempty_eigenbasis=integral_bases[1][1],
               cycle_global_nodes=np.array(CYCLE),ordered_tagged_pairs=PAIRS,metadata_json=np.array(json.dumps(clean({'input_map_sha256':input_id(),'new_eigensolver_calls':0,'checks':list(CHECKS),'physical_units':PHYSICAL_UNITS}),sort_keys=True)))
    return ((be,bv,*integral_bases[0]),(re,rv,*integral_bases[1]))

def source_integrals(c,ev,bare,pe,m,delta):
    """Exact finite spectral divided differences, independent of time Ward."""
    base=np.empty_like(c);empty=np.empty_like(c)
    d=m['dim']
    for s,qs in enumerate(m['groups']):
        if not len(qs):continue
        omega=ev[s][:,None]-ev[s][None,:]
        f=delta*np.sinc(omega*delta/(2*np.pi))*np.exp(1j*omega*delta/2)
        gate('integral_exact_zero_gap',f[omega==0],delta,OP_TOL)
        x=c[qs].transpose(1,0,2).reshape(2*d,-1)
        for target,eigvertex in ((base,bare[s]),(empty,pe[s])):
            target[qs]=((eigvertex*f)@x).reshape(2*d,len(qs),c.shape[-1]).transpose(1,0,2)
    q0,q4,q5=m['bits'][[0,4,5]]
    cc=base+(LAM*q0)[:,None,None]*empty+(m['ar']*q0*delta)[:,None,None]*c
    cm=cc+((q0-q4)/4)[:,None,None]*(delta*c-empty)+((q0-q5)*delta/4)[:,None,None]*c
    energy=ev[m['s']]+m['ar']*m['pop'][:,None];phase=np.exp(-1j*energy*delta)[:,:,None]
    return {'Vc':cc*phase,'Vm':cm*phase,'H':delta*energy[:,:,None]*c*phase}


def run_channel(prep,reset,two,basis):
    ar=float(F(prep['AR_rational']));m=setup_mode(reset,two,ar);ev,vec,bare,pe=basis
    label=('reset' if reset else 'retained')+('_on' if two else '_reference');cpdir=J/(PACKETS[int(reset)][1]+'_checkpoints')
    pk='tagged_reset' if reset and two else 'paired_reference_reset' if reset else 'tagged' if two else 'paired_reference'
    name=prep['preparation'];frames=[];begin=len(CHECKS)
    for si,row in enumerate(prep['rows']):
        ACTIVE.update(preparation=name,channel=label,source_time_index=si,stage='new_complete_energy_source_columns')
        start=len(CHECKS)
        with np.load(cpdir/row['state_file'],allow_pickle=False) as z:
            a=z['psi_tagged' if two else 'psi_reference'].copy();meta=json.loads(str(z['metadata_json']))
        if meta['input_map_sha256']!=row['input_map_sha256'] or meta['preparation']!=name or meta['forward_time_index']!=si:raise RuntimeError('frame NPZ metadata')
        cols=32 if reset and two else 256 if reset else 8 if two else 64
        if a.shape!=(len(m['words']),2,m['dim'],cols):raise RuntimeError('complete frame dimensions')
        source={'Vc':compact_vertex0(a,m),'Vm':compact_vertex0(a,m,True),'H':literal_h(a,m)}
        gate(name+label+'_independent_full_node_Vc%d'%si,source['Vc'],local_vertex(a,m),OP_TOL)
        gate(name+label+'_independent_full_node_Vm%d'%si,source['Vm'],local_vertex(a,m,0,True),OP_TOL)
        gate(name+label+'_exact_source_difference%d'%si,source['Vc']-source['Vm'],delta_vertex(a,m),OP_TOL)
        c=coefficients(a,vec,m);energy=ev[m['s']]+ar*m['pop'][:,None]
        cs={k:coefficients(source[k],vec,m) for k in KINDS};ns=np.zeros_like(a);ns[:,1]=a[:,1];cn=coefficients(ns,vec,m)
        gate(name+label+'_absolute_saved_H_action%d'%si,cs['H'],energy[:,:,None]*c,OP_TOL)
        for k in KINDS:
            gate(name+label+'_'+k+'_new_column_resolution%d'%si,source_column(cs[k],ev,vec,m,0),source[k],OP_TOL)
            cf=cs[k].reshape(-1,cols);sf=source[k].reshape(-1,cols)
            gate(name+label+'_'+k+'_full_mixture_apparatus_Gram%d'%si,cf.conj().T@cf,sf.conj().T@sf,OP_TOL)
        o=row[pk];energies={k:expectation(source[k],a) for k in KINDS}
        rates={k:2*float(np.vdot(source[k],source['H']).imag) for k in KINDS}
        gate(name+label+'_complete_parent_energy%d'%si,energies['H'],o['full_energy'],ENERGY_TOL)
        beta=record_beta(a,m);bdot=record_source_dot(a,source['H'],m)
        gate(name+label+'_all8_joint_parent_clock%d'%si,beta,cv(o['Bplus_beta_global']),OBS_TOL)
        gate(name+label+'_all8_complete_clock_derivative%d'%si,bdot,cv(o['Bplus_dot_global']),OBS_TOL)
        clock_dot={k:record_source_dot(a,source[k],m) for k in KINDS}
        gate(name+label+'_candidate_local_clock_generator%d'%si,clock_dot['Vc'],predicted_clock_source(a,m),OBS_TOL)
        gate(name+label+'_midpoint_local_clock_generator%d'%si,clock_dot['Vm'],predicted_clock_source(a,m,True),OBS_TOL)
        gate(name+label+'_nonendpoint5_source_partition_clock%d'%si,clock_dot['Vc'][5]-clock_dot['Vm'][5],1j*beta[5]/4,OBS_TOL)
        denominators=abs(beta)**2
        phase_tangents={k:[None if den==0 else float((beta[v].conjugate()*clock_dot[k][v]).imag/den) for v,den in enumerate(denominators)] for k in KINDS}
        norm=float(np.vdot(a,a).real);difference=energies['Vc']-energies['Vm']
        if reset:
            gate(name+label+'_reset_conserved_source_difference_work%d'%si,difference,float(np.sum(m['bits'][5][:,None,None,None]*abs(a)**2))/4,OBS_TOL)
        if F(prep['formation_gamma_rational'])==0:
            gate(name+label+'_gamma0_source_allocation_columns%d'%si,source['Vc'],source['Vm'],OP_TOL)
        info={'preparation':name,'channel':label,'source_time_index':si,'source_x_rational':str(TIMES[si]),'parent_state_sha256':row['state_sha256'],'input_map_sha256':input_id(),
              'network_norm':norm,'source_energy_work_vertices':energies,'source_energy_time_derivatives':rates,
              'source_class_difference_energy_work':difference,'direct_second_additive_N_contacts':np.zeros((3,3)).tolist(),
              'fractional_chart_mixed_L_eta_contacts':{k:energies[k] for k in ('Vc','Vm')},
              'joint_clock_beta_global':clean(beta),'joint_clock_generator_derivative_global':clean(clock_dot),'joint_clock_phase_rate_tangent_global':phase_tangents,
              'parent_Bplus_rate_global':o['Bplus_rate_global'],'parent_ideal_clock_structural_null':row['ideal_clock_structural_null'],
              'inherited_network_controller_work':{k:row[k] for k in ('copy_off_work','insertion_work','source_removal_reference_work','network_reset_work_tagged','network_reset_work_reference') if k in row},
              'physical_units':PHYSICAL_UNITS,'proper_clock_calibration_adopted':False,'checks':CHECKS[start:].copy()}
        info['absolute_phase_generator']='sealed NETWORK base_eigenvalues + AR*network_record_population; endpoint apparatus labels are retained source-independent external references'
        info['external_apparatus_scope']='owned network transfer/removal work is retained; total actuator energy/cost and proper T00 localization are unowned, not assigned zero as a physical statement'
        bundle=CP/(name+'_'+label+'_source%d.npz'%si)
        nh=commit_npz(bundle,'source_coefficients_saved',Vc_source_coefficients=cs['Vc'],Vm_source_coefficients=cs['Vm'],H_source_coefficients=cs['H'],
                      saved_state_spectral_coefficients=c,absolute_eigenvalues=energy,global_record_words=m['words'],metadata_json=np.array(json.dumps(clean(info),sort_keys=True)))
        commit(CP/(name+'_'+label+'_source%d.json'%si),{**info,'bundle_sha256':nh},'source_metadata_saved')
        frames.append({'a':a,'source':source,'c':c,'cs':cs,'cn':cn,'n':ns,'info':info})
    rows=[]
    for ti,si in PAIRTIMES:
        ACTIVE.update(preparation=name,channel=label,target_time_index=ti,source_time_index=si,stage='new_nine_nonstationary_energy_kernels')
        start=len(CHECKS);delta=float(TIMES[ti]-TIMES[si]);f,g=frames[ti],frames[si]
        phase=np.exp(-1j*(ev[m['s']]+ar*m['pop'][:,None])*delta)[:,:,None]
        propagated={k:source_column(g['cs'][k],ev,vec,m,delta) for k in KINDS}
        chis={};integrated={};ints=source_integrals(g['c'],ev,bare,pe,m,delta)
        for b in KINDS:
            gate(name+label+'_'+b+'_source_norm_%d_%d'%(ti,si),np.vdot(propagated[b],propagated[b]).real,np.vdot(g['source'][b],g['source'][b]).real,OBS_TOL if b!='H' else ENERGY_TOL)
            for aa in KINDS:
                key=aa+'_'+b
                chis[key]=-2*float(np.vdot(f['cs'][aa],phase*g['cs'][b]).imag)
                direct=-2*float(np.vdot(f['source'][aa],propagated[b]).imag)
                gate(name+label+'_direct_spectral_chi_'+key+'_%d_%d'%(ti,si),chis[key],direct,OBS_TOL if 'H' not in (aa,b) else ENERGY_TOL)
                integrated[key]=-2*float(np.vdot(f['cs'][aa],ints[b]).imag)
                if ti==si:
                    gate(name+label+'_equal_time_antisymmetry_'+key+'_%d'%ti,chis[key],-(-2*float(np.vdot(f['cs'][b],g['cs'][aa]).imag)),OBS_TOL if 'H' not in (aa,b) else ENERGY_TOL)
                    gate(name+label+'_zero_time_integral_'+key+'_%d'%ti,integrated[key],0.,ENERGY_TOL)
        gate(name+label+'_chi_HH_%d_%d'%(ti,si),chis['H_H'],0.,ENERGY_TOL)
        for k in ('Vc','Vm'):
            gate(name+label+'_uniform_H_'+k+'_%d_%d'%(ti,si),chis['H_'+k],g['info']['source_energy_time_derivatives'][k],ENERGY_TOL)
            gate(name+label+'_'+k+'_uniform_H_%d_%d'%(ti,si),chis[k+'_H'],-f['info']['source_energy_time_derivatives'][k],ENERGY_TOL)
            change=f['info']['source_energy_work_vertices'][k]-g['info']['source_energy_work_vertices'][k]
            gate(name+label+'_independent_integral_H_'+k+'_%d_%d'%(ti,si),integrated['H_'+k],change,ENERGY_TOL)
        signed_delta=chis['Vc_Vc']-chis['Vc_Vm']-chis['Vm_Vc']+chis['Vm_Vm']
        un=source_column(g['cn'],ev,vec,m,delta);weight=(m['bits'][0]-m['bits'][4])**2
        delta_oracle=-2*float(np.vdot(weight[:,None,None,None]*f['n'],un).imag)/16
        gate(name+label+'_record_correlated_delta_delta_%d_%d'%(ti,si),signed_delta,delta_oracle,OBS_TOL)
        if reset or F(prep['formation_gamma_rational'])==0:
            for key in ('Vc_Vm','Vm_Vc','Vm_Vm'):gate(name+label+'_allocation_energy_kernel_null_'+key+'_%d_%d'%(ti,si),chis[key],chis['Vc_Vc'],OBS_TOL)
            gate(name+label+'_allocation_energy_kernel_null_H_%d_%d'%(ti,si),chis['H_Vc'],chis['H_Vm'],ENERGY_TOL)
            gate(name+label+'_allocation_energy_kernel_null_Hright_%d_%d'%(ti,si),chis['Vc_H'],chis['Vm_H'],ENERGY_TOL)
        inclusive={k:-integrated['H_'+k]+f['info']['source_energy_work_vertices'][k] for k in ('Vc','Vm')}
        for k in inclusive:gate(name+label+'_inclusive_positive_source_step_'+k+'_%d_%d'%(ti,si),inclusive[k],g['info']['source_energy_work_vertices'][k],ENERGY_TOL)
        values={**{'chi_'+k:v for k,v in chis.items()},**{'integrated_chi_'+k:v for k,v in integrated.items()},
                'chi_source_difference_source_difference':signed_delta,'chi_record_correlated_incidence_oracle':delta_oracle,
                **{'inclusive_switched_network_energy_step_work_'+k:v for k,v in inclusive.items()},
                **{'switched_energy_first_readout_contact_'+k:f['info']['source_energy_work_vertices'][k] for k in ('Vc','Vm')}}
        row={'preparation':name,'channel':label,'target_time_index':ti,'source_time_index':si,'target_x_rational':str(TIMES[ti]),'source_x_rational':str(TIMES[si]),
             'values':values,'zero_direct_second_contacts':np.zeros((3,3)).tolist(),'target_baseline':f['info'],'source_baseline':g['info'],'input_map_sha256':input_id(),'checks':CHECKS[start:].copy()}
        commit(CP/(name+'_'+label+'_pair%d_%d.json'%(ti,si)),row,'ordered_pair_saved');rows.append(row)
    return {'preparation':name,'channel':label,'AR_rational':prep['AR_rational'],'formation_gamma_rational':prep['formation_gamma_rational'],'preparation_x_rational':prep['preparation_x_rational'],'rows':rows,'checks_this_channel':CHECKS[begin:].copy()}

def main():
    global APPEND_ALLOWED
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute; no automatic restart, overwrite or resume.')
    if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)):raise RuntimeError('reserved outputs exist')
    parents=authenticate();begun=time.monotonic();CP.mkdir();APPEND_ALLOWED=True
    parameters={'AR_rational':['0','1/8','7/40','1/4'],'formation_gamma_rational':['0','1/10'],
                'formation_x_rational':[str(x) for x in (F(0),F(1,10),F(1,5),F(2,5),F(4,5),F(1),F(2),F(4),F(8),F(12),F(16),F(24),F(32))],
                'forward_x_rational':[str(x) for x in TIMES],'ordered_time_pairs':PAIRTIMES,'global_cycle':CYCLE,'source_nodes':[0],
                'source_classes':['fixed-charge Crel node charging plus other midpoint ports','all-midpoint control'],'native_hbar':1,
                'kernel_order':KINDS,'all104_four_channels':True,'frame_count':1664,'kernel_row_count':4160,'new_eigensolver_calls':0,
                'operator_tolerance':OP_TOL,'source_kernel_clock_tolerance':OBS_TOL,'complete_energy_tolerance':ENERGY_TOL,'physical_units':PHYSICAL_UNITS}
    mh=write_json(CP/'manifest.json',{'PID':os.getpid(),'input_sha256':dict(INPUTS),'parameters':parameters});COMMITS['manifest.json']=mh
    event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':dict(INPUTS)})
    bs=bases();preps=[];frame_count=0;pair_count=0
    for pi in range(104):
        name='case%02d_prep%02d'%divmod(pi,13);channels=[];case,ageindex=divmod(pi,13)
        ar=parameters['AR_rational'][case//2];gamma=parameters['formation_gamma_rational'][case%2];age=parameters['formation_x_rational'][ageindex]
        for reset in (False,True):
            p=parents[int(reset)]['preparations'][pi]
            if p['preparation']!=name or p['AR_rational']!=ar or p['formation_gamma_rational']!=gamma or p['preparation_x_rational']!=age:raise RuntimeError('all104 four-channel fixed preparation census')
            for two in (True,False):
                channel=run_channel(p,reset,two,bs[0 if two else 1]);channels.append(channel);frame_count+=4;pair_count+=10
        for si in range(4):
            clocks=[cv(c['rows'][next(k for k,(ti,sj) in enumerate(PAIRTIMES) if ti==si and sj==si)]['target_baseline']['joint_clock_beta_global'])[list(REST)] for c in channels]
            for value in clocks[1:]:gate(name+'_six_common_parent_clocks_%d'%si,value,clocks[0],OP_TOL)
        contrasts=[]
        for k,(ti,si) in enumerate(PAIRTIMES):
            values=[c['rows'][k]['values'] for c in channels];keys=values[0]
            sr={a:values[0][a]-values[1][a] for a in keys};sx={a:values[2][a]-values[3][a] for a in keys}
            on={a:values[0][a]-values[2][a] for a in keys};ref={a:values[1][a]-values[3][a] for a in keys};dd={a:sr[a]-sx[a] for a in keys}
            for a in keys:
                gate(name+'_four_channel_signed_DD_'+a+'_%d'%k,dd[a],on[a]-ref[a],ENERGY_TOL if 'H' in a or 'energy' in a else OBS_TOL)
                if F(gamma)==0:
                    gate(name+'_gamma0_record_contrast_on_'+a+'_%d'%k,on[a],0.,ENERGY_TOL if 'H' in a or 'energy' in a else OBS_TOL)
                    gate(name+'_gamma0_record_contrast_reference_'+a+'_%d'%k,ref[a],0.,ENERGY_TOL if 'H' in a or 'energy' in a else OBS_TOL)
            contrasts.append({'target_time_index':ti,'source_time_index':si,'source_presence_retained':sr,'source_presence_transferred':sx,'retained_minus_transferred_on':on,
                              'retained_minus_transferred_reference':ref,'difference_of_differences':dd})
        summary={'preparation':name,'AR_rational':ar,'formation_gamma_rational':gamma,'preparation_x_rational':age,'channels':channels,'signed_four_channel_contrasts':contrasts}
        commit(CP/(name+'_complete.json'),summary,'preparation_complete');preps.append(summary)
        print(json.dumps({'preparation':name,'frame_count_so_far':frame_count,'kernel_rows_so_far':pair_count,'checks':len(CHECKS),'failed':sum(not c['passed'] for c in CHECKS)}),flush=True)
    exact('full1664source4160pair_census',frame_count==1664 and pair_count==4160 and len(preps)==104 and all(len(p['channels'])==4 and all(len(c['rows'])==10 for c in p['channels']) for p in preps))
    recheck();passed=sum(c['passed'] for c in CHECKS);failed=sum(not c['passed'] for c in CHECKS)
    status='QUALIFIED_ARITHMETIC_PREPARED_NETWORK_ENERGY_SOURCE' if failed==0 else 'ARITHMETIC_FAILED'
    result={'status':status,'passed':passed,'failed':failed,'checks':CHECKS,'preparations':preps,'frame_count':frame_count,'ordered_pair_count':pair_count,
            'source_order':KINDS,'physical_units':PHYSICAL_UNITS,'input_sha256':dict(INPUTS),'manifest_sha256':mh,'PID':os.getpid(),
            'elapsed_seconds':time.monotonic()-begun,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'All signed prepared network-port energy-lapse kernels and owned network switching work. External apparatus proper T00 and total actuator cost are unowned. No thermal susceptibility substitution, total-instrument gravity, metric/source adoption or selected clock.'}
    raw=write_json(RESULT,result);canonical=hashlib.sha256(blob(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':canonical})
    lines=['# Localized network energy-lapse source V001','',status+': %d/%d arithmetic controls; all1664 sources and4160 unselected channel/time rows.'%(passed,len(CHECKS)),
           '', 'Sources are Vc, Vm and the complete coded NETWORK H. Removed/reset apparatus are external source-independent references; proper T00 and total actuator cost are unowned.',
           'Physical causal prefactor: Eunit²/(hbar c_p⁴); integrated/Fourier prefactor: Eunit/c_p⁴; x=Eunit t_physical/hbar. No physical unit or c_p was selected.',
           '', '| Preparation | Channel | t | source t | chi cc | chi cm | chi cH | chi mc | chi mm | chi mH | chi Hc | chi Hm | chi HH | c step work | m step work |',
           '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in preps:
        for c in p['channels']:
            for r in c['rows']:
                v=r['values'];vals=[v['chi_'+aa+'_'+b] for aa in KINDS for b in KINDS]+[v['inclusive_switched_network_energy_step_work_'+aa] for aa in ('Vc','Vm')]
                lines.append('|%s|%s|%s|%s|%s|'%(p['preparation'],c['channel'],r['target_x_rational'],r['source_x_rational'],'|'.join('%.10g'%x for x in vals)))
    if sum(x.startswith('|') for x in lines)!=4162:raise RuntimeError('report4160 rows')
    lines+=['','All nine signed kernels, zero additive-N second contacts, independent integral/step work and all four-channel contrasts remain in JSON. Full coherent source coefficients and absolute network q phases are in referenced lossless NPZ bundles.',
            'The reset energy-allocation null does not erase source-work differences or the R5 joint clock shift. Gamma0 allocation/record contrasts are null; ordinary body energy-source responses can remain nonzero.',
            'Cross-class entries are diagnostic contractions. Fractional N=L(1+eta delta0) has its compulsory mixed first vertex. No complete weak scalar constraint, inverse response, proper-clock calibration or gravity-success gate is claimed.',
            'Raw SHA256: '+raw,'Canonical SHA256: '+canonical]
    with REPORT.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    recheck();rh=sha(REPORT);event({'event':'report_saved','sha256':rh,'data_rows':4160})
    cmap={p.name:sha(p) for p in sorted(CP.iterdir()) if p.name!='journal.jsonl'}
    if cmap!=COMMITS:raise RuntimeError('complete NEW checkpoint commit map')
    if len(cmap)!=7594:raise RuntimeError('fixed7594 NEW checkpoint census')
    rr=write_json(RECEIPT,{'status':status,'passed':passed,'failed':failed,'input_sha256':dict(INPUTS),'checkpoint_sha256':cmap,'frame_count':frame_count,'ordered_pair_count':pair_count,
                         'result_raw_sha256':raw,'result_canonical_sha256':canonical,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'PID':os.getpid()})
    event({'event':'receipt_saved','sha256':rr});print(json.dumps({'status':status,'passed':passed,'failed':failed,'raw_sha256':raw,'receipt_sha256':rr}),flush=True)
    return 0 if failed==0 else 3


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        if APPEND_ALLOWED:
            v={'status':'ARITHMETIC_FAILED','error':repr(exc),'traceback':traceback.format_exc(),'active':dict(ACTIVE),'PID':os.getpid(),'checks':CHECKS,'input_sha256':dict(INPUTS),'committed_sha256':dict(COMMITS)}
            if not ERROR.exists():eh=write_json(ERROR,v);event({'event':'error','external_error_sha256':eh,'PID':os.getpid()})
        print(json.dumps({'status':'ERROR_PRESERVED' if APPEND_ALLOWED else 'PREFLIGHT_REJECTED_NO_MUTATION','error':repr(exc)}),flush=True);raise SystemExit(3)
