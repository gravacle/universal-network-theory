#!/usr/bin/env python3
"""Complete relative-energy projector control on sealed C8 preparations.
Root alone executes. No eigensolver, baseline propagation, producer import,
RNG, thermal/passive state adoption or favorable signed-response selection.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[k]='1'
import sys,json,hashlib,math,time,resource,traceback
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(100000)
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_RELATIVE_ENERGY_SPECTRAL_RESPONSE_V001';STEM='floating_return_c8_relative_energy_spectral_response_v001'
CP=J/(STEM+'_checkpoints');RESULT=J/(NAME+'_RESULT.json');REPORT=J/(NAME+'_RESULT.md');RECEIPT=J/(NAME+'_RECEIPT.json');ERROR=J/(NAME+'_ERROR.json')
PROTOCOL_SHA='b8337f327c8503e505f2099c38bd61550ae005ca369a886fce076b9be802ed6a'
LOCAL='FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001';LSTEM='floating_return_c8_localized_lapse_response_v001';LCP=J/(LSTEM+'_checkpoints')
CERT='FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001';CSTEM='floating_return_c8_relative_energy_projector_certificate_v001'
PINS={
 'FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001_RESULT.json':'584ce7064f7f388df6d1ddcd6465adb91c72c0098a86116d1cb289de533def9a',
 'FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001_RECEIPT.json':'99b96af6ba34e39cab489edfd1c898dca5dafe2d2ab2d8c38b2e70afdfc48fcb',
 'FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001_RESULT.json':'d773bbc65029acf287f0008db77dd1a897079988c7c766c955e4438383b860a8',
 'FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001_RECEIPT.json':'4bc0cf0c6ccca2657e886fe6f4d5a1328c5afa4027b17d3358c58374b6775fd9',
 'FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001_AUDIT.json':'1b06f159ddbd9f2f6fee74ec50c502b5b481bc4b5eebda3bcdb70131a595a020',
 'FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001_AUDIT.md':'2eb0620fc8ce3b26d9c4e795369a5e2fb2de51389f4e795b6dcb223cc6d37e86'}
PACKETS=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','floating_return_c8_tagged_probe_reaction_v001'),('FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001','floating_return_c8_endpoint_record_isolation_v001'))
H=.2;T=.1;JC=.25;LAM=.5;Z=1j/5;BAND=1e-9
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple(zip(CYCLE,CYCLE[1:]+CYCLE[:1]));REST=(1,2,3,5,6,7)
PAIRS=np.array([(a,b) for a in range(8) for b in range(8) if a!=b],dtype=np.int64);PIND={tuple(p):i for i,p in enumerate(PAIRS)}
OCC=np.array([[(int(a)==v)+(int(b)==v) for a,b in PAIRS] for v in range(8)])
TRANS=[]
for u,v in EDGES:
 TRANS.append((np.array([(PIND[(u,b)],PIND[(v,b)]) for b in range(8) if b not in (u,v)],dtype=np.int64),np.array([(PIND[(a,u)],PIND[(a,v)]) for a in range(8) if a not in (u,v)],dtype=np.int64)))
OPS=('Vc','Vm','H','n','I');CHANNELS=('retained_on','retained_reference','reset_on','reset_reference');OPPAIRS=tuple((a,b) for a in range(5) for b in range(a,5))
AGES=('0','1/10','1/5','2/5','4/5','1','2','4','8','12','16','24','32');ARS=('0','1/8','7/40','1/4')
OP_TOL=5e-10;OBS_TOL=1e-9;ENERGY_TOL=5e-9
WORK_BUDGET={'fixed_controls':416,'fixed_operator_pairs':25,'loading_spectra_per_control':3,'tagged_body_dimension':112,'reference_body_dimension':16,'maximum_lossless_packed_complex_weights':208*3*15*(112*111//2+16*15//2),'fixed_checkpoint_count':938,'fixed_final_journal_events':941,'runtime_estimate_seconds':[60,300],'estimate_scope':'One-thread fixed saved-data contractions/compression/rehash; estimate only, no adaptive physics or runtime-selected census.'}
CHECKS=[];INPUTS={};COMMITS={};ACTIVE={};STARTED=False;PARENT_ROWS={};LOCAL_INPUT_MAP_SHA=None
PHYSICAL_UNITS={'native_hbar':1,'native_age':'x=Eunit*t_physical/hbar','native_frequency':'omega_native=hbar*omega_physical/Eunit','Phi_vertex_prefactor':'Eunit/c_p^2','Phi_causal_kernel_prefactor':'Eunit^2/(hbar*c_p^4)','Phi_integrated_or_Fourier_kernel_prefactor':'Eunit/c_p^4','Eunit_selected':False,'c_p_selected':False,'source_scope':'network and assigned Crel cells; held apparatus energies/work external, proper T00 and dephasing actuator cost unowned'}

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

def register(p,h):
    p=Path(p).resolve();key=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    if sha(p)!=h:raise RuntimeError('input seal '+str(p))
    if key in INPUTS and INPUTS[key]!=h:raise RuntimeError('inconsistent input '+key)
    INPUTS[key]=h

def authenticate_packet(name,stem,count,events_count,data_rows=None):
    cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'))
    if r['result_raw_sha256']!=sha(J/(name+'_RESULT.json')) or r['result_canonical_sha256']!=hashlib.sha256(blob(p)).hexdigest() or r['report_sha256']!=sha(J/(name+'_RESULT.md')):raise RuntimeError('parent result/canonical/report '+name)
    if p['failed']!=r['failed'] or p['failed']!=0 or p['passed']!=r['passed'] or p['passed']!=len(p['checks']) or not all(x['passed'] for x in p['checks']) or p['input_sha256']!=r['input_sha256']:raise RuntimeError('parent arithmetic '+name)
    for f,h in r['input_sha256'].items():register(ROOT/f,h)
    for suffix in ('_RESULT.json','_RESULT.md','_RECEIPT.json'):register(J/(name+suffix),sha(J/(name+suffix)))
    cm=r['checkpoint_sha256']
    if len(cm)!=count or set(cm)!={x.name for x in cp.iterdir() if x.name!='journal.jsonl'}:raise RuntimeError('parent checkpoint census '+name)
    for f,h in cm.items():register(cp/f,h)
    raw=(cp/'journal.jsonl').read_bytes();lines=raw.splitlines();es=[json.loads(x) for x in lines]
    report={'event':'report_saved','sha256':r['report_sha256']}
    if data_rows is not None:report['data_rows']=data_rows
    if len(es)!=events_count or hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()!=r['journal_prefix_sha256'] or es[-1]!={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))} or es[-2]!=report or es[-3]!={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']}:raise RuntimeError('parent final journal '+name)
    m=read(cp/'manifest.json');mh=sha(cp/'manifest.json')
    if p['manifest_sha256']!=mh or es[0]!={'event':'started','PID':p['PID'],'manifest_sha256':mh,'input_sha256':r['input_sha256']} or m['PID']!=r['PID'] or m['input_sha256']!=r['input_sha256']:raise RuntimeError('parent manifest/start '+name)
    got={'manifest.json':mh}
    for e in es[1:-3]:
        if e['file'] in got:raise RuntimeError('duplicate parent commit')
        got[e['file']]=e['sha256']
    if got!=cm:raise RuntimeError('parent commit map '+name)
    register(cp/'journal.jsonl',sha(cp/'journal.jsonl'));return p,r

def authenticate():
    global LOCAL_INPUT_MAP_SHA
    for f,h in PINS.items():register(J/f,h)
    register(J/(NAME+'.md'),PROTOCOL_SHA);register(__file__,sha(__file__))
    local,lr=authenticate_packet(LOCAL,LSTEM,7594,7597,4160)
    cert,cr=authenticate_packet(CERT,CSTEM,21,24)
    for stage in cert['sector_census']:
        if stage!=read(J/(CSTEM+'_checkpoints')/(stage['sector']+'_root_census.json')):raise RuntimeError('certificate duplicate sector summary')
    audit=read(J/(LOCAL+'_AUDIT.json'))
    if audit['audit_status']!='PASS' or audit['failed_assertions'] or audit['result_raw_sha256']!=lr['result_raw_sha256'] or audit['receipt_sha256']!=sha(J/(LOCAL+'_RECEIPT.json')) or (audit['audited_preparations'],audit['audited_source_frames'],audit['audited_channel_time_rows'])!=(104,1664,4160):raise RuntimeError('accepted localized audit identity/census')
    if local['frame_count']!=1664 or local['ordered_pair_count']!=4160 or len(local['preparations'])!=104 or cert['component_count']!=18 or cert['saved_mode_count']!=384 or len(cert['sector_census'])!=2:raise RuntimeError('complete parent census')
    for i,p in enumerate(local['preparations']):
        if p['preparation']!='case%02d_prep%02d'%divmod(i,13) or p['AR_rational']!=ARS[i//26] or p['preparation_x_rational']!=AGES[i%13] or len(p['channels'])!=4:raise RuntimeError('fixed104 parent labels')
    LOCAL_INPUT_MAP_SHA=hashlib.sha256(blob(lr['input_sha256'])).hexdigest()
    for reset,(name,stem) in enumerate(PACKETS):
        parent=read(J/(name+'_RESULT.json'));rows=[]
        for i,p in enumerate(parent['preparations']):
            if p['preparation']!=local['preparations'][i]['preparation'] or p['rows'][0]['x_rational']!='0':raise RuntimeError('fixed inherited age-zero row')
            rows.append(p['rows'][0])
        PARENT_ROWS[reset]=rows
    return local,cert

def certificate(cert,sector,ev):
    stage=next(x for x in cert['sector_census'] if x['sector']==sector)
    roots={x['root_ID']:x for x in stage['root_intervals']};rows=stage['loading_rows'];answer=[];all_ids=[]
    for s,row in enumerate(rows):
        ids=row['mode_exact_root_ID'];n=len(ev[s])
        if row['s']!=s or row['dimension']!=n or len(ids)!=n or len(set(ids))!=n:raise RuntimeError('earned simple complete loading certificate')
        gate(sector+'_certificate_sorted_saved_modes_'+str(s),row['saved_native_eigenvalues'],ev[s],0.)
        intervals=np.array([[float(F(v)) for v in roots[r]['native_interval']] for r in ids])
        if any(roots[r]['multiplicity_by_loading'][s]!=1 for r in ids):raise RuntimeError('simple loading multiplicity')
        exact(sector+'_ordered_disjoint_root_intervals_'+str(s),bool(np.all(intervals[:-1,1]<=intervals[1:,0])))
        gate(sector+'_root_midpoint_alignment_'+str(s),intervals.mean(1),ev[s],OP_TOL)
        answer.append({'ids':ids,'intervals':intervals});all_ids+=ids
    exact(sector+'_all_loading_root_sets_disjoint',len(set(all_ids))==len(all_ids))
    if len(set(all_ids))!=len(all_ids):raise RuntimeError('fixed certificate cross-loading witness unavailable')
    return answer

def build_bases(cert):
    with np.load(LCP/'reused_localized_response_bases.npz',allow_pickle=False) as z:
        exact('cycle map',z['cycle_global_nodes'].tolist()==list(CYCLE));gate('ordered pair map',z['ordered_tagged_pairs'],PAIRS,0.)
        values={k:z[k].copy() for k in ('tagged_eigenvalues','tagged_eigenvectors','tagged_base_matrices','reference_eigenvalues','reference_eigenvectors','reference_base_matrices','tagged_bare_Vc_eigenbasis','reference_bare_Vc_eigenbasis','tagged_Pempty_eigenbasis','reference_Pempty_eigenbasis')}
        meta=json.loads(str(z['metadata_json']));exact('accepted source-basis controls',all(c['passed'] for c in meta['checks']))
    result={};arrays={}
    for sector,two in (('tagged',True),('reference',False)):
        ev,vec,hs=(values[sector+'_'+k] for k in ('eigenvalues','eigenvectors','base_matrices'));d=56 if two else 8;n=2*d
        roots=certificate(cert,sector,ev);bare=values[sector+'_bare_Vc_eigenbasis'];pe=values[sector+'_Pempty_eigenbasis']
        nphys=np.diag(np.r_[np.zeros(d),np.ones(d)]);xphys=np.kron(np.array([[0,1],[1,0]]),np.eye(d));iphys=H*np.kron(np.array([[0,-1j],[1j,0]]),np.eye(d))
        ne=np.array([v.conj().T@nphys@v for v in vec]);ie=np.array([v.conj().T@iphys@v for v in vec]);xe=np.array([v.conj().T@xphys@v for v in vec])
        metrics=[];residual_norms=[];vector_norms=[]
        for s in range(3):
            gate(sector+'_mode_Gram_'+str(s),vec[s].conj().T@vec[s],np.eye(n),OP_TOL)
            gate(sector+'_complete_saved_action_'+str(s),hs[s]@vec[s],vec[s]*ev[s][None,:],OP_TOL)
            gram=vec[s].conj().T@vec[s]-np.eye(n);complete=vec[s]@vec[s].conj().T-np.eye(n);res=hs[s]@vec[s]-vec[s]*ev[s][None,:]
            vnorm=np.sqrt(np.sum(abs(vec[s])**2,axis=0));rnorm=np.sqrt(np.sum(abs(res)**2,axis=0));idem=abs(vnorm**2-1)*vnorm**2
            gate(sector+'_complete_projector_resolution_'+str(s),complete,0.,OP_TOL);gate(sector+'_rankone_projector_idempotence_'+str(s),idem,0.,OP_TOL)
            gate(sector+'_projector_commutator_bound_'+str(s),2*rnorm*vnorm,0.,OP_TOL)
            phase=np.exp(1j*np.arange(n)*np.pi/7);rebased=vec[s]*phase[None,:]
            gate(sector+'_numerical_phase_projector_rebasing_'+str(s),rebased@rebased.conj().T,vec[s]@vec[s].conj().T,OP_TOL)
            for mode in range(n):gate(sector+'_phase_rebased_individual_projector_'+str((s,mode)),np.outer(rebased[:,mode],rebased[:,mode].conj()),np.outer(vec[s][:,mode],vec[s][:,mode].conj()),OP_TOL)
            phase_ops=(bare[s],pe[s],ne[s],ie[s],np.diag(ev[s]));rephase_ops=[phase.conj()[:,None]*o*phase[None,:] for o in phase_ops]
            for ai,o in enumerate(phase_ops):
                for bi,v in enumerate(phase_ops):gate(sector+'_phase_rebased_source_products_'+str((s,ai,bi)),rephase_ops[ai]*rephase_ops[bi].T,o*v.T,OP_TOL)
            metrics.append({'s':s,'Gram_max':float(np.max(abs(gram))),'Gram_Frobenius':float(np.sqrt(np.sum(abs(gram)**2))),'action_max':float(np.max(abs(res))),'action_Frobenius':float(np.sqrt(np.sum(abs(res)**2))),'completeness_max':float(np.max(abs(complete))),'completeness_Frobenius':float(np.sqrt(np.sum(abs(complete)**2))),'projector_idempotence_Frobenius_each':idem,'projector_commutator_upper_each':2*rnorm*vnorm,'scope':'Floating evaluation of rank-one/complete projector witnesses; nondirected, inherited tolerance. Full q/app replicas tensor the exact identity.'})
            residual_norms.append(rnorm);vector_norms.append(vnorm)
            gate(sector+'_source_n_partition_'+str(s),ne[s]+pe[s],np.eye(n),OP_TOL)
            gate(sector+'_independent_I_continuity_'+str(s),ie[s],1j*(ev[s][:,None]-ev[s][None,:])*ne[s],OP_TOL)
            for q0 in (0,1):
                if q0>s or s-q0>1:continue
                q=(1 if q0 else 0)+(16 if s-q0 else 0)
                for ar in (0.,.125,.175,.25):
                    m=setup_mode(False,two,ar);m={**m,'words':np.array([q]),'bits':np.array([[(q>>v)&1] for v in range(8)]),'pop':np.array([q.bit_count()]),'s':np.array([s]),'groups':tuple(np.array([0]) if k==s else np.array([],int) for k in range(3))}
                    a=vec[s].reshape(1,2,d,n)
                    gate(sector+'_literal_H_'+str((s,q0,ar)),literal_h(a,m).reshape(n,n),vec[s]*(ev[s]+ar*q.bit_count())[None,:],OP_TOL)
                    for q5 in (0,1):
                        m['bits'][5,0]=q5;m['pop'][0]=q.bit_count()+q5
                        oc=bare[s]+LAM*q0*pe[s]+ar*q0*np.eye(n)
                        om=bare[s]-s*ne[s]/4+(q0/2+(q0-q5)/4+ar*q0)*np.eye(n)
                        for label,op,mid in (('Vc',oc,False),('Vm',om,True)):
                            actual=coefficients(local_vertex(a,m,0,mid),vec,m)[0]
                            gate(sector+'_literal_'+label+str((s,q0,q5,ar)),actual,op,OP_TOL)
            gate(sector+'_phase_contact_commutator_'+str(s),-(hs[s]@nphys@nphys-2*nphys@hs[s]@nphys+nphys@nphys@hs[s]),H*xphys,OP_TOL)
        result[sector]={'ev':ev,'vec':vec,'hs':hs,'bare':bare,'pe':pe,'n':ne,'I':ie,'X':xe,'roots':roots,'dim':d,'projector_metrics':metrics,'residual_norms':np.array(residual_norms),'vector_norms':np.array(vector_norms)}
        for key in ('ev','vec','bare','pe','n','I','X'):arrays[sector+'_'+key]=result[sector][key]
        arrays[sector+'_mode_exact_root_ID']=np.array([r['ids'] for r in roots])
    commit_npz(CP/'relative_response_bases.npz','bases_saved',**arrays,metadata_json=np.array(json.dumps(clean({'input_map_sha256':input_id(),'certificate_status':'complete exact simple loading spectra, disjoint across s; coherent replicas retained','numerical_accuracy_scope':'inherited action/Gram/projector tolerance only; no directed response error','projector_metrics':{k:v['projector_metrics'] for k,v in result.items()},'replica_projector_identity':'P_root=|v_root><v_root| tensor identity on ALL fixed-s q words and held apparatus; arbitrary unitary rebasing of replicas changes neither projector nor coherent factor density','checks':CHECKS.copy()}),sort_keys=True)))
    return result

def probe_marginal(rho,two):
    if not two:return rho
    out=np.zeros((16,16),complex)
    for a in range(8):
        bs=[b for b in range(8) if b!=a];old=np.array([bit*56+PIND[(a,b)] for bit in (0,1) for b in bs]);new=np.array([bit*8+b for bit in (0,1) for b in bs])
        out[np.ix_(new,new)]+=rho[np.ix_(old,old)]
    return out

def dephased_beta(c,m,root_ids):
    lookup={int(q):i for i,q in enumerate(m['words'])};beta=np.zeros(8,complex)
    for v in range(8):
        for low,q in enumerate(m['words']):
            if (int(q)>>v)&1 or int(q)+(1<<v) not in lookup:continue
            high=lookup[int(q)+(1<<v)];sl,sh=int(m['s'][low]),int(m['s'][high])
            # Complete root projector: distinct loading sets give exactly no common block.
            if sl==sh:
                exact('same-loading complete replica root IDs',root_ids[sl]==root_ids[sh])
                beta[v]+=2*np.vdot(c[high],c[low])
            else:exact('endpoint disjoint exact loading roots',set(root_ids[sl]).isdisjoint(root_ids[sh]))
    return beta

def stationary_response(pop,m,b):
    """Full signed numerator in the earned simple physical-body spectrum.
    Q/app replicas retain their factors/coherences. Q-diagonal operators see
    only diagonal same-word populations; scalar source terms cancel exactly.
    """
    arrays={};abel=np.zeros((5,5),complex);formal_static=np.zeros((5,5),complex);unresolved=0;contact=0.;zero_gap=np.zeros((5,5),complex)
    for s in range(3):
        n=len(b['ev'][s]);iu,ju=np.triu_indices(n,1);e=b['ev'][s];delta=e[ju]-e[iu];weights=np.zeros((5,5,len(iu)),complex)
        for q0 in (0,1):
            qs=np.flatnonzero((m['s']==s)&(m['bits'][0]==q0))
            if not len(qs):continue
            p=pop[qs].sum(0)
            operators=(b['bare'][s]+LAM*q0*b['pe'][s],b['bare'][s]-s*b['n'][s]/4,np.diag(e),b['n'][s],b['I'][s])
            diff=p[iu]-p[ju]
            for a in range(5):
                for k in range(5):weights[a,k]+=diff*operators[a][iu,ju]*operators[k][ju,iu]
            contact+=float(np.dot(p,np.diag(H*b['X'][s]).real))
        gate('signed numerator operator Hermiticity s'+str(s),weights,weights.conj().transpose(1,0,2),OBS_TOL)
        gate('independent spectral continuity left s'+str(s),weights[4],-1j*delta[None,:]*weights[3],OBS_TOL)
        gate('independent spectral continuity right s'+str(s),weights[:,4],1j*delta[None,:]*weights[:,3],OBS_TOL)
        gate('complete uniform energy numerator s'+str(s),weights[2],0.,ENERGY_TOL);gate('complete uniform energy numerator transpose s'+str(s),weights[:,2],0.,ENERGY_TOL)
        intervals=b['roots'][s]['intervals'];separation=intervals[ju,0]-intervals[iu,1];near=separation<=BAND;unresolved+=int(near.sum())
        if len(delta) and not np.all(delta>0):raise RuntimeError('strict sorted simple energies')
        ab=np.sum(weights/(delta-Z)[None,None,:]+weights.conj()/(delta+Z)[None,None,:],axis=2)
        st=np.sum((weights+weights.conj())/delta[None,None,:],axis=2)
        # Independent ordered-pair expression uses both pole orientations.
        signed=np.concatenate((weights,-weights.conj()),axis=2);gaps=np.r_[delta,-delta]
        gate('independent complete signed pole contraction s'+str(s),ab,np.sum(signed/(gaps-Z)[None,None,:],axis=2),OBS_TOL)
        abel+=ab;formal_static+=st
        arrays['s%d_upper_energy_mode_i'%s]=iu;arrays['s%d_upper_energy_mode_j'%s]=ju;arrays['s%d_packed_operator_pairs'%s]=np.array(OPPAIRS)
        arrays['s%d_signed_weights_operator_upper'%s]=np.array([weights[a,k] for a,k in OPPAIRS])
        arrays['s%d_native_pole_gap_positive'%s]=delta;arrays['s%d_unresolved_pair_mask'%s]=near;arrays['s%d_exact_native_intervals'%s]=intervals;arrays['s%d_mode_exact_root_ID'%s]=np.array(b['roots'][s]['ids']);arrays['s%d_numerical_native_modes'%s]=e
    gate('stationary self-phase contact identity',formal_static[4,4],contact,ENERGY_TOL)
    gate('stationary analytic reality at imaginary Abel point',abel.imag,0.,OBS_TOL)
    return arrays,{'Abel_z_native':[0.,.2],'chi_Abel':abel,'formal_static_candidate':formal_static,'true_static_numerical_evaluation':formal_static if unresolved==0 else None,'static_status':'FINITE_STATIONARY_STATIC_NUMERICAL_EVALUATION' if unresolved==0 else 'REFUSED_UNRESOLVED_NEAR_POLES','zero_gap_numerators':zero_gap,'zero_gap_certificate':'all five operators conserve each q/app word; every exact physical-body loading mode is simple, so same-root restrictions are word-diagonal scalars and commute','unresolved_energy_pair_count':unresolved,'phase_contact_hX_mean':contact,'phase_readout_theta_contact':-contact,'response_source_sign':'positive additive eta V responds as minus chi; phase theta vertex is minus I','thermal_or_passive_adoption':False,'numerical_scope':'exact root labels; finite numerical response with inherited tolerances, no directed accuracy certificate'}

def run_channel(prep,label,b):
    reset=label.startswith('reset');two=label.endswith('_on');ar=float(F(prep['AR_rational']));m=setup_mode(reset,two,ar);d=b['dim'];n=2*d
    path=LCP/(prep['preparation']+'_'+label+'_source0.npz');info=read(path.with_suffix('.json'))
    with np.load(path,allow_pickle=False) as z:
        c=z['saved_state_spectral_coefficients'].copy();cs={key:z[key+'_source_coefficients'].copy() for key in ('Vc','Vm','H')};meta=json.loads(str(z['metadata_json']))
        gate('absolute full-network scalar phases',z['absolute_eigenvalues'],b['ev'][m['s']]+ar*m['pop'][:,None],0.);gate('full coherent q word map',z['global_record_words'],m['words'],0.)
    if meta['preparation']!=prep['preparation'] or meta['channel']!=label or meta['source_time_index']!=0 or meta['input_map_sha256']!=LOCAL_INPUT_MAP_SHA or info['bundle_sha256']!=sha(path):raise RuntimeError('accepted age-zero source factor seal')
    cols=32 if reset and two else 256 if reset else 8 if two else 64
    if c.shape!=(len(m['words']),n,cols):raise RuntimeError('full initial factor census')
    a=source_column(c,b['ev'],b['vec'],m,0.)
    old=PARENT_ROWS[int(reset)][int(prep['preparation'][4:6])*13+int(prep['preparation'][-2:])]
    oldpath=J/(PACKETS[int(reset)][1]+'_checkpoints')/old['state_file']
    if info['parent_state_sha256']!=sha(oldpath):raise RuntimeError('initial authentic physical frame seal')
    with np.load(oldpath,allow_pickle=False) as z:gate('independent authentic physical factor',a,z['psi_tagged' if two else 'psi_reference'],OP_TOL)
    for key,actual in (('Vc',local_vertex(a,m)),('Vm',local_vertex(a,m,0,True)),('H',literal_h(a,m))):
        gate('independent initial '+key+' source coefficients',coefficients(actual,b['vec'],m),cs[key],OP_TOL)
    pop=np.sum(abs(c)**2,axis=2);qmass=pop.sum(1);norm=float(qmass.sum());beforebeta=record_beta(a,m);afterbeta=dephased_beta(c,m,[r['ids'] for r in b['roots']])
    gate('authentic full initial mixture normalization',norm,1.,OBS_TOL)
    gate('all q-word probabilities preserved',qmass,np.sum(abs(a)**2,axis=(1,2,3)),OBS_TOL)
    commutator_bound=0.;replica_checks=[];u=np.array([[1,1j],[1j,1]],complex)/np.sqrt(2);readouts=(np.array([[0,0],[2,0]],complex),np.diag([0,1]))
    for s,qs in enumerate(m['groups']):
        if not len(qs):continue
        p=pop[qs].sum(0);commutator_bound+=float(2*np.sum(p*b['residual_norms'][s]*b['vector_norms'][s]))
        pair=qs[:2]
        for mode in range(n):
            f=c[pair,mode];rho=f@f.conj().T;rot=u@f;rr=rot@rot.conj().T
            gate('deterministic full-replica unitary density witness',rr,u@rho@u.conj().T,OP_TOL)
            for o in readouts:gate('replica clock/charge trace invariant',np.trace(rr@(u@o@u.conj().T)),np.trace(rho@o),OP_TOL)
        replica_checks.append({'s':s,'fixed_replica_indices':pair.tolist(),'body_modes_checked':n,'unitary':u,'readouts':'complex dressed raising query and charge projector; transform readout with basis, never discard replica coherence'})
    gate('weighted full-q/app H_rel rhoD commutator bound',commutator_bound,0.,OP_TOL)
    gate('all six full coherent formed amplitudes preserved',afterbeta[list(REST)],beforebeta[list(REST)],OBS_TOL)
    gate('complete initial parent clock amplitudes',beforebeta,cv(meta['joint_clock_beta_global']),OBS_TOL)
    gate('endpoints erased by disjoint loading roots',afterbeta[[0,4]],0.,0.)
    flat=a.reshape(len(m['words']),n,cols).transpose(1,0,2).reshape(n,-1);rho_before=flat@flat.conj().T;rho_after=np.zeros((n,n),complex)
    for s,qs in enumerate(m['groups']):
        p=pop[qs].sum(0);rho_after+=(b['vec'][s]*p[None,:])@b['vec'][s].conj().T
    gate('complete projection norm',np.trace(rho_after),norm,OBS_TOL);gate('projected carrier-edge Hermiticity',rho_after,rho_after.conj().T,OP_TOL)
    energy=float(np.sum(pop*(b['ev'][m['s']]+ar*m['pop'][:,None])));gate('full H/AR energy invariant',energy,meta['source_energy_work_vertices']['H'],ENERGY_TOL)
    means={}
    for key in ('Vc','Vm','H'):
        before=float(np.vdot(c,cs[key]).real);after=0.
        for s,qs in enumerate(m['groups']):
            if not len(qs):continue
            if key=='H':diagonal=b['ev'][s][None,:]+ar*m['pop'][qs,None]
            elif key=='Vc':diagonal=np.diag(b['bare'][s]).real[None,:]+LAM*m['bits'][0,qs,None]*np.diag(b['pe'][s]).real[None,:]+ar*m['bits'][0,qs,None]
            else:diagonal=np.diag(b['bare'][s]).real[None,:]-s*np.diag(b['n'][s]).real[None,:]/4+(m['bits'][0,qs]/2+(m['bits'][0,qs]-m['bits'][5,qs])/4+ar*m['bits'][0,qs])[:,None]
            after+=float(np.sum(pop[qs]*diagonal))
        gate('source mean before matches parent '+key,before,meta['source_energy_work_vertices'][key],ENERGY_TOL if key=='H' else OBS_TOL)
        means[key]={'before':before,'after':after,'change':after-before}
    arrays,response=stationary_response(pop,m,b)
    if reset:
        gate('reset allocation response exact null',response['chi_Abel'][0],response['chi_Abel'][1],OBS_TOL);gate('reset allocation response transpose null',response['chi_Abel'][:,0],response['chi_Abel'][:,1],OBS_TOL)
        gate('reset allocation source work preserved',means['Vc']['after']-means['Vm']['after'],float(np.dot(qmass,m['bits'][5]))/4,OBS_TOL)
    afterdot=1j*ar*afterbeta;clock_eta_c=np.zeros(8,complex);clock_eta_m=np.zeros(8,complex);clock_eta_m[5]=-1j*afterbeta[5]/4
    qmean=m['bits']@qmass;probe_before=probe_marginal(rho_before,two);probe_after=probe_marginal(rho_after,two)
    contacts={'additive_HNN':np.zeros((3,3)),'fractional_H_Leta':{k:means[k]['after'] for k in ('Vc','Vm')},'H_theta_theta':response['phase_contact_hX_mean'],'H_eta_theta':{k:-float(np.sum(pop*np.diagonal(b['I'],axis1=1,axis2=2)[m['s']]).real)/2 for k in ('Vc','Vm')},'H_Ltheta':-float(np.sum(pop*np.diagonal(b['I'],axis1=1,axis2=2)[m['s']]).real),'I_theta_readout_theta_contact':response['phase_readout_theta_contact'],'I_theta_readout_eta_contact':float(np.sum(pop*np.diagonal(b['I'],axis1=1,axis2=2)[m['s']]).real)/2}
    row={'preparation':prep['preparation'],'channel':label,'AR_rational':prep['AR_rational'],'formation_gamma_rational':prep['formation_gamma_rational'],'formation_age_rational':prep['preparation_x_rational'],'chosen_control':'complete exact H_rel projector; not natural relaxation','network_norm':norm,'complete_network_energy':energy,'Q_word_populations_preserved':True,'network_q_means_global':qmean,'before_joint_beta_global':beforebeta,'after_joint_beta_global':afterbeta,'after_joint_beta_dot_global':afterdot,'after_local_source_clock_dot':{'Vc':clock_eta_c,'Vm':clock_eta_m,'H':afterdot},'parent_phase_chart_eligible_global':meta['parent_phase_chart_eligible_global'],'parent_clock_refusals_preserved':True,'endpoint_clock_change':afterbeta[[0,4]]-beforebeta[[0,4]],'source_energy_work_vertices':means,'full_owned_contacts':contacts,'inherited_network_controller_work':meta['inherited_network_controller_work'],'external_instrument_and_dephasing_control_cost':'unowned, not physical zero','response':response,'input_factor_source_file':str(path.relative_to(ROOT)),'input_factor_sha256':sha(path),'complete_density_representation':'rho_D(q,i;qprime,j)=sum_cols c(q,i,col) conj(c(qprime,j,col)) only if exact root_ID(s,i)=root_ID(sprime,j); full original c retained in sealed source bundle','spectral_weight_reconstruction':'operator upper a<=b and energy upper i<j lossless; W_ba(i,j)=conj(W_ab(i,j)); W_ab(j,i)=-conj(W_ab(i,j)); exact zero-gap W=0; cross-loading q-diagonal response zero','numerical_projector_accuracy':'complete reused Gram/action checks; exact labels do not direct-round eigenvectors or response','physical_units':PHYSICAL_UNITS,'post_control_marginal_scope':'channel-specific chosen twirls need not commute with original source trace/reset; old matched carrier-edge marginal is not reasserted'}
    row['after_phase_rate_raw_global']=[None if abs(v)**2==0 else ar for v in afterbeta]
    row['parent_ideal_clock_structural_null']=meta['parent_ideal_clock_structural_null'];row['parent_Bplus_rate_global']=meta['parent_Bplus_rate_global']
    row['after_phase_chart_eligible_global']=[bool(meta['parent_phase_chart_eligible_global'][v] and not meta['parent_ideal_clock_structural_null'] and v in REST and abs(afterbeta[v])**2!=0) for v in range(8)]
    row['phase_ratio_scope']='Exact model AR orientation at mathematical nonzero denominator only; inherited tiny-amplitude/parent refusals stay. No proper clock or new empirical threshold.'
    row['q_diagonal_only_stationarity']=True;row['full_H_stationary_state_claimed']=False;row['six_record_analytic_clock_law']='beta_v(x)=beta_v(0)*exp(i AR x), v in {1,2,3,5,6,7}; only inherited eligible nonnull charts'
    row['relative_density_commutator_trace_norm_upper_estimate']=commutator_bound;row['relative_commutator_scope']='2 sum_(s,i) pop_(s,i) ||(Hbar_s-E_i)v_i|| ||v_i|| bounds the complete coherent-q/app factor commutator with H_rel; floating evaluation, not directed and not full-H stationarity'
    row['complete_replica_basis_rotation_controls']=replica_checks;row['body_projector_numerical_witnesses']=b['projector_metrics']
    arrays.update(q_mode_probability=pop,global_record_words=m['words'],network_q_word_probability=qmass,carrier_edge_rho_before=rho_before,carrier_edge_rho_after=rho_after,probe_edge_rho_before=probe_before,probe_edge_rho_after=probe_after)
    npz=CP/(prep['preparation']+'_'+label+'.npz');nh=commit_npz(npz,'channel_arrays_saved',**arrays,metadata_json=np.array(json.dumps(clean(row),sort_keys=True)))
    row['bundle_file']=npz.name;row['bundle_sha256']=nh;row['input_map_sha256']=input_id();row['checks']=CHECKS[ACTIVE['check_start']:].copy()
    commit(CP/(prep['preparation']+'_'+label+'.json'),row,'channel_saved');return row,{'before':probe_before,'after':probe_after}

def main():
    global STARTED
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute.')
    if any(p.exists() for p in (CP,RESULT,REPORT,RECEIPT,ERROR)):raise SystemExit('Exclusive reserved path exists.')
    started=time.monotonic();local,cert=authenticate();recheck();CP.mkdir();STARTED=True
    mh=write_json(CP/'manifest.json',{'PID':os.getpid(),'input_sha256':INPUTS,'work_budget':WORK_BUDGET,'fixed_parameters':{'Abel_z':[0.,.2],'energy_unresolved_band':BAND,'OP':OP_TOL,'OBS':OBS_TOL,'energy':ENERGY_TOL,'control_census':416,'preparation_census':104,'forward_ages_consumed':[0],'new_eigensolver_calls':0,'new_preparation_or_trajectory_calls':0,'response_census':'25 functions per control; all exact poles/weights/near masks; all loading sectors','basis_certificate':'earned 336tagged/48reference distinct roots; simple per loading; all q/app replicas glued'}});COMMITS['manifest.json']=mh;event({'event':'started','PID':os.getpid(),'manifest_sha256':mh,'input_sha256':INPUTS})
    bases=build_bases(cert);preparations=[]
    for i,prep in enumerate(local['preparations']):
        rows=[];probes=[]
        for label in CHANNELS:
            ACTIVE.update(preparation=prep['preparation'],channel=label,stage='exact_relative_projector_and_complete_signed_response',check_start=len(CHECKS))
            row,probe=run_channel(prep,label,bases['tagged' if label.endswith('_on') else 'reference']);rows.append(row);probes.append(probe)
        for row in rows[1:]:gate('all six common formed amplitudes after chosen control',cv(clean(row['after_joint_beta_global']))[list(REST)],cv(clean(rows[0]['after_joint_beta_global']))[list(REST)],OBS_TOL)
        mat=[np.asarray(r['response']['chi_Abel']) for r in rows];contrast={'source_presence_retained':mat[0]-mat[1],'source_presence_transferred':mat[2]-mat[3],'retained_minus_transferred_on':mat[0]-mat[2],'retained_minus_transferred_reference':mat[1]-mat[3],'difference_of_differences':mat[0]-mat[1]-mat[2]+mat[3]}
        st=[np.asarray(r['response']['formal_static_candidate']) for r in rows];static_contrast={'source_presence_retained':st[0]-st[1],'source_presence_transferred':st[2]-st[3],'retained_minus_transferred_on':st[0]-st[2],'retained_minus_transferred_reference':st[1]-st[3],'difference_of_differences':st[0]-st[1]-st[2]+st[3]}
        dispositions={r['channel']:{'status':r['response']['static_status'],'unresolved_pair_count':r['response']['unresolved_energy_pair_count'],'parent_clock_eligibility':r['parent_phase_chart_eligible_global'],'parent_structural_clock_null':r['parent_ideal_clock_structural_null']} for r in rows}
        for p in probes[1:]:gate('old matched initial probe-edge marginal',p['before'],probes[0]['before'],OBS_TOL)
        post=[p['after'] for p in probes]
        marginal={'retained_on_minus_reference':post[0]-post[1],'transferred_on_minus_reference':post[2]-post[3],'difference_of_differences':post[0]-post[1]-post[2]+post[3]}
        if prep['formation_gamma_rational']=='0':
            gate('gamma0 chosen-control record contrast on',mat[0],mat[2],OBS_TOL);gate('gamma0 chosen-control record contrast reference',mat[1],mat[3],OBS_TOL)
        complete={'preparation':prep['preparation'],'AR_rational':prep['AR_rational'],'formation_gamma_rational':prep['formation_gamma_rational'],'formation_age_rational':prep['preparation_x_rational'],'channels':rows,'signed_Abel_four_channel_contrasts':contrast,'formal_static_four_channel_contrasts':static_contrast,'true_static_four_channel_contrasts':static_contrast if all(r['response']['true_static_numerical_evaluation'] is not None for r in rows) else None,'inherited_row_refusal_dispositions':dispositions,'post_control_probe_edge_marginal_differences':marginal,'old_initial_isolation_marginal_reasserted':False,'input_map_sha256':input_id()}
        commit(CP/(prep['preparation']+'_complete.json'),complete,'preparation_saved');preparations.append(complete)
        print(json.dumps({'preparation':prep['preparation'],'controls_completed':4*(i+1),'failed':sum(not c['passed'] for c in CHECKS)}),flush=True)
    exact('fixed104 preparations416 controls',len(preparations)==104 and sum(len(p['channels']) for p in preparations)==416);exact('fixed938 checkpoints',len(COMMITS)==938);recheck()
    failed=sum(not c['passed'] for c in CHECKS);result={'status':'ARITHMETIC_FAILED' if failed else 'QUALIFIED_ARITHMETIC_CHOSEN_RELATIVE_PROJECTOR_RESPONSE','failed':failed,'passed':len(CHECKS)-failed,'checks':CHECKS,'preparation_count':104,'control_count':416,'operator_order':OPS,'preparations':preparations,'physical_units':PHYSICAL_UNITS,'input_sha256':INPUTS,'manifest_sha256':mh,'PID':os.getpid(),'elapsed_seconds':time.monotonic()-started,'scope':'chosen exact-label projector control; six coherent record amplitudes retained, q-diagonal algebra stationary; signed numerical spectral response, no thermal/passive/metric/gravity alias; complete old controller work and unowned actuator cost retained'}
    raw=write_json(RESULT,result);ch=hashlib.sha256(blob(result)).hexdigest();event({'event':'result_saved','raw_sha256':raw,'canonical_sha256':ch})
    with REPORT.open('x') as f:
        f.write('# Relative-energy projector response V001\n\nStatus: '+result['status']+'. All104 preparations/four channels and all25 signed response functions are retained. Six formed coherent rest-record amplitudes are preserved; endpoint amplitudes are removed by the declared chosen control. This is stationary only on the q-diagonal source algebra. It is not natural relaxation, a passive/thermal state, a proper-clock calibration or gravitational Pi.\n\n|Preparation|Channel|AR|Formation age|Norm|Energy|Static status|Near pairs|chi_VcVc(i/5)|chi_VmVm(i/5)|\n|---|---|---|---|---:|---:|---|---:|---:|---:|\n')
        for p in preparations:
            for r in p['channels']:
                x=r['response'];f.write('|%s|%s|%s|%s|%.12g|%.12g|%s|%d|%.12g|%.12g|\n'%(p['preparation'],r['channel'],r['AR_rational'],r['formation_age_rational'],r['network_norm'],r['complete_network_energy'],x['static_status'],x['unresolved_energy_pair_count'],x['chi_Abel'][0,0].real,x['chi_Abel'][1,1].real))
        f.write('\nAll signed poles/packed weights, q-mode probabilities and full reduced marginals remain in referenced lossless NPZ; complete coherent input factors remain in sealed parent source bundles with the exact root projection rule. Full25 Abel/static candidates, contacts/work, clocks and post-control channel-matching changes remain in JSON. Physical units are symbolic as stated; source-independent apparatus stress and dephasing-control cost are unowned. Result SHA256: '+raw+'\n');f.flush();os.fsync(f.fileno())
    recheck();rh=sha(REPORT);event({'event':'report_saved','sha256':rh,'data_rows':416})
    cm={p.name:sha(p) for p in CP.iterdir() if p.name!='journal.jsonl'}
    if cm!=COMMITS or len(cm)!=938:raise RuntimeError('complete938 checkpoint seal')
    receipt={'status':result['status'],'failed':failed,'passed':result['passed'],'input_sha256':INPUTS,'checkpoint_sha256':cm,'result_raw_sha256':raw,'result_canonical_sha256':ch,'report_sha256':rh,'journal_prefix_sha256':sha(CP/'journal.jsonl'),'manifest_sha256':mh,'PID':os.getpid(),'preparation_count':104,'control_count':416};rr=write_json(RECEIPT,receipt);event({'event':'receipt_saved','sha256':rr})
    print(json.dumps({'status':result['status'],'passed':result['passed'],'failed':failed,'result_raw_sha256':raw,'receipt_sha256':rr}),flush=True)
    if failed:raise SystemExit(3)

if __name__=='__main__':
    try:main()
    except Exception as e:
        if STARTED and not ERROR.exists():
            h=write_json(ERROR,{'status':'EXECUTION_ERROR_PRESERVED','error':repr(e),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'input_sha256':INPUTS,'committed_sha256':COMMITS,'source_sha256':sha(__file__),'PID':os.getpid()});event({'event':'error','sha256':h})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
