#!/usr/bin/env python3
"""NEW prepared response columns and complete incidence-phase contact; root only."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import sys,json,hashlib,math,time,resource,traceback,re
from pathlib import Path
from fractions import Fraction as F
import numpy as np
J=Path(__file__).resolve().parent;ROOT=J.parent.parent
NAME='FLOATING_RETURN_C8_RETARDED_INCIDENCE_CURRENT_V001'
CP=J/'floating_return_c8_retarded_incidence_current_v001_checkpoints'
RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md');RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PROTOCOL_SHA='6a4b32a76b16405871ffba37d86b2012862a4f8336ec5c8f34e258a2312fcd44'
PACKETS=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','floating_return_c8_tagged_probe_reaction_v001'),('FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001','floating_return_c8_endpoint_record_isolation_v001'))
TIMES=(F(0),F(1,5),F(2),F(8));PAIRTIMES=tuple((i,k) for i in range(4) for k in range(i+1))
H=.2;T=.1;JC=.25;LAM=.5
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple((CYCLE[k],CYCLE[(k+1)%8]) for k in range(8))
PAIRS=np.array([(a,b) for a in range(8) for b in range(8) if a!=b],dtype=np.int64)
PIND={tuple(p):i for i,p in enumerate(PAIRS)};OCC=np.array([[(int(a)==v)+(int(b)==v) for a,b in PAIRS] for v in range(8)])
TRANS=[]
for u,v in EDGES:
    TRANS.append((np.array([(PIND[(u,b)],PIND[(v,b)]) for b in range(8) if b not in (u,v)],dtype=np.int64),np.array([(PIND[(a,u)],PIND[(a,v)]) for a in range(8) if a not in (u,v)],dtype=np.int64)))
REST=(1,2,3,5,6,7)
CHECKS=[];INPUTS={};COMMITS={};APPEND_ALLOWED=False;ACTIVE={}

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

def authenticate():
    if sha(J/(NAME+'.md'))!=PROTOCOL_SHA:raise RuntimeError('unfrozen protocol')
    anchors=re.findall(r'^\| (.+?) \| ([0-9a-f]{64}) \|$',(J/(NAME+'.md')).read_text(),re.M)
    if len(anchors)!=17:raise RuntimeError('required17 final direct pins')
    for f,h in anchors:
        if sha(J/f)!=h:raise RuntimeError('direct input '+f)
        INPUTS[str((J/f).relative_to(ROOT))]=h
    INPUTS[str((J/(NAME+'.md')).relative_to(ROOT))]=PROTOCOL_SHA
    INPUTS[str(Path(__file__).resolve().relative_to(ROOT))]=sha(__file__)
    return [authenticate_packet(*p) for p in PACKETS]

def setup_mode(reset,two,ar):
    words=np.array([sum(((r>>k)&1)<<v for k,v in enumerate(REST)) for r in range(64)]) if reset else np.arange(256)
    bits=np.array([[(int(q)>>v)&1 for q in words] for v in range(8)]);s=bits[0]+bits[4]
    return {'reset':reset,'two':two,'ar':ar,'words':words,'pop':bits.sum(0),'s':s,'groups':tuple(np.flatnonzero(s==k) for k in range(3)),'dim':56 if two else 8}

def vertex(a,kind):
    if kind=='n':
        z=np.zeros_like(a);z[:,1]=a[:,1];return z
    if kind=='I':return H*np.stack((-1j*a[:,1],1j*a[:,0]),axis=1)
    if kind=='K':return H*a[:,::-1]
    raise ValueError(kind)

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

def bases():
    cp=J/(PACKETS[0][1]+'_checkpoints')
    with np.load(cp/'reaction_eigensystems.npz',allow_pickle=False) as z:
        be=z['tagged_base_eigenvalues'];bv=z['tagged_base_eigenvectors'];re=z['reference_base_eigenvalues'];rv=z['reference_base_eigenvectors'];bh=z['tagged_base_matrices'];rh=z['reference_base_matrices']
    matrices=[];ie=[]
    for label,ev,vec,hs,d in (('tagged',be,bv,bh,56),('reference',re,rv,rh,8)):
        n=np.diag(np.r_[np.zeros(d),np.ones(d)]);iv=H*np.kron(np.array([[0,-1j],[1j,0]]),np.eye(d));kv=H*np.kron(np.array([[0,1],[1,0]]),np.eye(d));inds=[]
        for s in range(3):
            gate(label+'_I_Hermitian_%d'%s,iv,iv.conj().T,5e-10);gate(label+'_K_Hermitian_%d'%s,kv,kv.conj().T,5e-10)
            gate(label+'_n_dot_%d'%s,1j*(hs[s]@n-n@hs[s]),iv,5e-10)
            gate(label+'_phase_second_contact_%d'%s,-(n@(n@hs[s]-hs[s]@n)-(n@hs[s]-hs[s]@n)@n),kv,5e-10)
            gate(label+'_reused_residual_%d'%s,hs[s]@vec[s],vec[s]*ev[s][None,:],5e-10)
            gate(label+'_reused_orthogonal_%d'%s,vec[s].conj().T@vec[s],np.eye(2*d),5e-10)
            # Prospective algebra-only phase1/20 control; no new evolution or fit.
            u=np.diag(np.exp(1j*n.diagonal()/20));phase=hs[s].astype(complex).copy();phase[:d,d:]=-H*np.exp(-1j/20)*np.eye(d);phase[d:,:d]=-H*np.exp(1j/20)*np.eye(d)
            gate(label+'_complete_phase_family_%d'%s,phase,u@hs[s]@u.conj().T,5e-10)
            inds.append(vec[s].conj().T@iv@vec[s])
        matrices.append(inds)
    meta={'input_sha256':dict(INPUTS),'new_eigensolver_calls':0,'checks':list(CHECKS)}
    commit_npz(CP/'reused_response_bases.npz','bases_saved',tagged_eigenvalues=be,tagged_eigenvectors=bv,reference_eigenvalues=re,reference_eigenvectors=rv,
               tagged_I_in_eigenbasis=np.array(matrices[0]),reference_I_in_eigenbasis=np.array(matrices[1]),metadata_json=np.array(json.dumps(clean(meta),sort_keys=True)))
    return ((be,bv,np.array(matrices[0])),(re,rv,np.array(matrices[1])))

def integral_column(cp,ev,vec,ie,m,delta):
    out=np.empty_like(cp);dim=cp.shape[1];cols=cp.shape[-1]
    for s,qs in enumerate(m['groups']):
        if len(qs)==0:continue
        omega=ev[s][:,None]-ev[s][None,:]
        f=delta*np.sinc(omega*delta/(2*np.pi))*np.exp(1j*omega*delta/2)
        gate('divided_difference_zero_gap',f[omega==0],delta,5e-10)
        x=cp[qs].transpose(1,0,2).reshape(dim,-1);y=((ie[s]*f)@x).reshape(dim,len(qs),cols).transpose(1,0,2)
        energy=ev[s][None,:]+m['ar']*m['pop'][qs,None]
        out[qs]=y*np.exp(-1j*energy*delta)[:,:,None]
    return transform(out,vec,m).reshape(len(m['words']),2,m['dim'],cols)

def expectation(o,a):return float(np.vdot(a,o).real)

def run_channel(prep,reset,two,basis):
    ar=float(F(prep['AR_rational']));m=setup_mode(reset,two,ar);ev,vec,ie=basis
    label=('reset' if reset else 'retained')+('_on' if two else '_reference');cpdir=J/(PACKETS[int(reset)][1]+'_checkpoints')
    pk='tagged_reset' if reset and two else 'paired_reference_reset' if reset else 'tagged' if two else 'paired_reference'
    name=prep['preparation'];frames=[];begin=len(CHECKS)
    for si,row in enumerate(prep['rows']):
        ACTIVE.update(preparation=name,channel=label,source_time_index=si,stage='new_response_coefficients')
        with np.load(cpdir/row['state_file'],allow_pickle=False) as z:
            a=z['psi_tagged' if two else 'psi_reference'];meta=json.loads(str(z['metadata_json']))
        if meta['input_map_sha256']!=row['input_map_sha256'] or meta['preparation']!=name or meta['forward_time_index']!=si:raise RuntimeError('frame NPZ metadata')
        if a.shape!=(len(m['words']),2,m['dim'],32 if reset and two else 256 if reset else 8 if two else 64):raise RuntimeError('frame schema')
        ia=vertex(a,'I');na=vertex(a,'n');ka=vertex(a,'K');ha=literal_h(a,m)
        c=coefficients(a,vec,m);ci=coefficients(ia,vec,m);cn=coefficients(na,vec,m)
        gate(name+label+'_n_column_resolution%d'%si,source_column(cn,ev,vec,m,0),na,5e-10)
        gate(name+label+'_I_column_resolution%d'%si,source_column(ci,ev,vec,m,0),ia,5e-10)
        energy=ev[m['s']]+ar*m['pop'][:,None]
        gate(name+label+'_saved_H_action%d'%si,source_column(energy[:,:,None]*c,ev,vec,m,0),ha,5e-10)
        gate(name+label+'_I_norm%d'%si,np.vdot(ia,ia).real,H*H*np.vdot(a,a).real)
        af=a.reshape(-1,a.shape[-1]);nn=na.reshape(-1,a.shape[-1])
        gate(name+label+'_I_full_column_Gram%d'%si,ci.reshape(-1,a.shape[-1]).conj().T@ci.reshape(-1,a.shape[-1]),H*H*(af.conj().T@af))
        gate(name+label+'_n_full_column_Gram%d'%si,cn.reshape(-1,a.shape[-1]).conj().T@cn.reshape(-1,a.shape[-1]),nn.conj().T@nn)
        gate(name+label+'_n_norm%d'%si,np.vdot(na,na).real,expectation(na,a))
        o=row[pk];nv=expectation(na,a);iv=expectation(ia,a);kv=expectation(ka,a);idot=2*float(np.vdot(ia,ha).imag)
        gate(name+label+'_parent_n%d'%si,nv,o['norm']-o['empty_edge_probability'])
        gate(name+label+'_parent_I%d'%si,iv,H*o['incidence_Pauli']['Y'])
        gate(name+label+'_parent_K%d'%si,kv,H*o['incidence_Pauli']['X'])
        info={'preparation':name,'channel':label,'source_time_index':si,'source_x_rational':str(TIMES[si]),'parent_state_sha256':row['state_sha256'],'input_map_sha256':input_id(),
              'baseline_n':nv,'baseline_I':iv,'baseline_K':kv,'baseline_I_dot':idot,
              'parent_Bplus_beta_global':o['Bplus_beta_global'],'parent_Bplus_dot_global':o['Bplus_dot_global'],
              'parent_Bplus_rate_global':o['Bplus_rate_global'],'parent_ideal_clock_structural_null':row['ideal_clock_structural_null'],
              'physical_clock_calibration_adopted':False}
        nh=commit_npz(CP/(name+'_'+label+'_source%d.npz'%si),'source_coefficients_saved',I_source_coefficients=ci,n_source_coefficients=cn,saved_state_spectral_coefficients=c,
                      absolute_eigenvalues=energy,metadata_json=np.array(json.dumps(info,sort_keys=True)))
        commit(CP/(name+'_'+label+'_source%d.json'%si),{**info,'bundle_sha256':nh},'source_metadata_saved')
        frames.append({'a':a,'I':ia,'n':na,'H':ha,'c':c,'ci':ci,'cn':cn,'info':info})
    rows=[]
    for ti,si in PAIRTIMES:
        ACTIVE.update(preparation=name,channel=label,target_time_index=ti,source_time_index=si,stage='new_nonstationary_kernel')
        start=len(CHECKS);delta=float(TIMES[ti]-TIMES[si]);f,g=frames[ti],frames[si]
        ui=source_column(g['ci'],ev,vec,m,delta);un=source_column(g['cn'],ev,vec,m,delta)
        wi=integral_column(g['c'],ev,vec,ie,m,delta)
        gate(name+label+'_integral_boundary_%d_%d'%(ti,si),wi,f['n']-un,1e-8)
        chi={k:-2*float(np.vdot(f[k],ui).imag) for k in ('I','n','H')}
        integrated={k:-2*float(np.vdot(f[k],wi).imag) for k in ('I','n','H')}
        bcur=2*float(np.vdot(f['I'],un).imag);bn=2*float(np.vdot(f['n'],un).imag)
        netcur=integrated['I']-f['info']['baseline_K'];stepenergy=integrated['H']-f['info']['baseline_I']
        gate(name+label+'_current_Ward_%d_%d'%(ti,si),netcur,bcur,1e-8)
        gate(name+label+'_charge_Ward_%d_%d'%(ti,si),integrated['n'],bn,1e-8)
        gate(name+label+'_unperturbed_energy_impulse_%d_%d'%(ti,si),chi['H'],g['info']['baseline_I_dot'],1e-8)
        gate(name+label+'_unperturbed_energy_integral_%d_%d'%(ti,si),integrated['H'],f['info']['baseline_I']-g['info']['baseline_I'],1e-8)
        gate(name+label+'_inclusive_switched_energy_work_%d_%d'%(ti,si),stepenergy,-g['info']['baseline_I'],1e-8)
        gate(name+label+'_source_I_column_norm_%d_%d'%(ti,si),np.vdot(ui,ui).real,np.vdot(g['I'],g['I']).real)
        gate(name+label+'_source_n_column_norm_%d_%d'%(ti,si),np.vdot(un,un).real,np.vdot(g['n'],g['n']).real)
        if ti==si:
            gate(name+label+'_diagonal_chiII%d'%ti,chi['I'],0.)
            gate(name+label+'_diagonal_chinI%d'%ti,chi['n'],-f['info']['baseline_K'])
            gate(name+label+'_diagonal_integral%d'%ti,wi,0.,1e-8)
        if si==0:
            gate(name+label+'_initial_occupied_step_current%d'%ti,netcur,0.,1e-8)
            gate(name+label+'_initial_occupied_step_charge%d'%ti,integrated['n'],0.,1e-8)
        vals={'chi_II':chi['I'],'chi_nI':chi['n'],'chi_HI_unperturbed':chi['H'],
              'integrated_chi_II':integrated['I'],'integrated_chi_nI':integrated['n'],'integrated_chi_HI_unperturbed':integrated['H'],
              'current_direct_contact':-f['info']['baseline_K'],'complete_current_step_response':netcur,
              'energy_direct_contact':-f['info']['baseline_I'],'inclusive_switched_energy_step_work':stepenergy,
              'current_boundary_response':bcur,'charge_boundary_response':bn}
        row={'preparation':name,'channel':label,'target_time_index':ti,'source_time_index':si,'target_x_rational':str(TIMES[ti]),'source_x_rational':str(TIMES[si]),
             'values':vals,'target_baseline':f['info'],'source_baseline':g['info'],'input_map_sha256':input_id(),'checks':CHECKS[start:].copy()}
        commit(CP/(name+'_'+label+'_pair%d_%d.json'%(ti,si)),row,'ordered_pair_saved');rows.append(row)
    return {'preparation':name,'channel':label,'AR_rational':prep['AR_rational'],'formation_gamma_rational':prep['formation_gamma_rational'],'preparation_x_rational':prep['preparation_x_rational'],'rows':rows,'checks_this_channel':CHECKS[begin:].copy()}

def main():
    global APPEND_ALLOWED
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute; no automatic retry or resume.')
    if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)):raise RuntimeError('reserved outputs exist')
    parents=authenticate();begun=time.monotonic();CP.mkdir();APPEND_ALLOWED=True
    mh=write_json(CP/'manifest.json',{'PID':os.getpid(),'input_sha256':dict(INPUTS),'ordered_time_pairs':PAIRTIMES,'all104_four_channels':True,'new_eigensolver_calls':0});COMMITS['manifest.json']=mh
    event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':dict(INPUTS)})
    bs=bases();preps=[]
    for pi in range(104):
        name=parents[0]['preparations'][pi]['preparation'];channels=[]
        for reset in (False,True):
            p=parents[int(reset)]['preparations'][pi]
            if p['preparation']!=name:raise RuntimeError('four-channel preparation alignment')
            for two in (True,False):channels.append(run_channel(p,reset,two,bs[0 if two else 1]))
        for si in range(4):
            clocks=[cv(c['rows'][next(k for k,(ti,sj) in enumerate(PAIRTIMES) if ti==si and sj==si)]['target_baseline']['parent_Bplus_beta_global'])[list(REST)] for c in channels]
            for v in clocks[1:]:gate(name+'_six_common_parent_clocks_%d'%si,v,clocks[0],5e-10)
        contrasts=[]
        for k,(ti,si) in enumerate(PAIRTIMES):
            v=[c['rows'][k]['values'] for c in channels];keys=v[0]
            sr={a:v[0][a]-v[1][a] for a in keys};sx={a:v[2][a]-v[3][a] for a in keys}
            on={a:v[0][a]-v[2][a] for a in keys};ref={a:v[1][a]-v[3][a] for a in keys};dd={a:sr[a]-sx[a] for a in keys}
            for a in keys:gate(name+'_four_channel_DD_'+a+'_%d'%k,dd[a],on[a]-ref[a])
            contrasts.append({'target_time_index':ti,'source_time_index':si,'source_presence_retained':sr,'source_presence_transferred':sx,'retained_minus_transferred_on':on,'retained_minus_transferred_reference':ref,'difference_of_differences':dd})
        summary={'preparation':name,'channels':channels,'signed_four_channel_contrasts':contrasts};commit(CP/(name+'_complete.json'),summary,'preparation_complete');preps.append(summary)
        print(json.dumps({'preparation':name,'channel_pairs':40,'checks':len(CHECKS),'failed':sum(not c['passed'] for c in CHECKS)}),flush=True)
    exact('all104_by4_by10_census',len(preps)==104 and all(len(p['channels'])==4 and all(len(c['rows'])==10 for c in p['channels']) for p in preps))
    recheck();passed=sum(c['passed'] for c in CHECKS);failed=sum(not c['passed'] for c in CHECKS);status='QUALIFIED_ARITHMETIC_PREPARED_CURRENT_CONTACT_PRIMITIVE' if failed==0 else 'ARITHMETIC_FAILED'
    result={'status':status,'passed':passed,'failed':failed,'checks':CHECKS,'preparations':preps,'input_sha256':dict(INPUTS),'manifest_sha256':mh,'PID':os.getpid(),
            'elapsed_seconds':time.monotonic()-begun,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'Prepared two-time native incidence phase response with complete contact. No frequency fit, physical charge/speed, common metric, galaxy/expansion or gravity adoption.'}
    raw=write_json(RESULT,result);canonical=hashlib.sha256(blob(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':canonical})
    lines=['# Prepared incidence current and contact V001','',status+': %d/%d arithmetic controls;4160 unselected channel/time rows.'%(passed,len(CHECKS)),
           '','| Preparation | Channel | t | source t | chi II | chi nI | chi HI | direct current contact | complete current step | charge step | switched energy work |',
           '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for p in preps:
        for c in p['channels']:
            for r in c['rows']:
                v=r['values'];lines.append('|%s|%s|%s|%s|%.10g|%.10g|%.10g|%.10g|%.10g|%.10g|%.10g|'%(p['preparation'],c['channel'],r['target_x_rational'],r['source_x_rational'],v['chi_II'],v['chi_nI'],v['chi_HI_unperturbed'],v['current_direct_contact'],v['complete_current_step_response'],v['integrated_chi_nI'],v['inclusive_switched_energy_step_work']))
    if sum(x.startswith('|') for x in lines)!=4162:raise RuntimeError('report4160 rows')
    lines+=['','All signed kernels/contacts and four-channel contrasts remain in JSON. Nonstationary current response is not an equilibrium covariance, optical calibration or gravity-success gate.','Raw SHA256: '+raw,'Canonical SHA256: '+canonical]
    with REPORT.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    recheck();rh=sha(REPORT);event({'event':'report_saved','sha256':rh,'data_rows':4160})
    cmap={p.name:sha(p) for p in sorted(CP.iterdir()) if p.name!='journal.jsonl'}
    rr=write_json(RECEIPT,{'status':status,'passed':passed,'failed':failed,'input_sha256':dict(INPUTS),'checkpoint_sha256':cmap,'result_raw_sha256':raw,'result_canonical_sha256':canonical,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'PID':os.getpid()})
    event({'event':'receipt_saved','sha256':rr});print(json.dumps({'status':status,'passed':passed,'failed':failed,'raw_sha256':raw,'receipt_sha256':rr}),flush=True)
    return 0 if failed==0 else 3

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        if APPEND_ALLOWED:
            v={'error':repr(exc),'traceback':traceback.format_exc(),'active':dict(ACTIVE),'PID':os.getpid(),'checks':CHECKS,'input_sha256':dict(INPUTS),'committed_sha256':dict(COMMITS)}
            if not ERROR.exists():eh=write_json(ERROR,v);event({'event':'error','external_error_sha256':eh,'PID':os.getpid()})
        print(json.dumps({'status':'ERROR_PRESERVED' if APPEND_ALLOWED else 'PREFLIGHT_REJECTED_NO_MUTATION','error':repr(exc)}),flush=True);raise SystemExit(3)
