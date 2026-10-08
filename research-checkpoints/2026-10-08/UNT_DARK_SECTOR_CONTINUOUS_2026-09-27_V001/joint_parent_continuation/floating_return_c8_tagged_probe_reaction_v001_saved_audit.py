#!/usr/bin/env python3
"""Independent SAVED-state audit: no propagation, eigensolver or producer import."""
import os, sys, json, hashlib, time, math, traceback, resource
from pathlib import Path
from fractions import Fraction
import numpy as np

J=Path(__file__).resolve().parent; ROOT=J.parent.parent
NAME='FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001'
CP=J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints'
PCP=J/'floating_return_c8_retained_record_geometry_v001_checkpoints'
AJ=J/(NAME+'_AUDIT.json'); AM=J/(NAME+'_AUDIT.md'); AE=J/(NAME+'_AUDIT_ERROR.json')
PIN={'_RESULT.json':'d7e4e759b357dd8154567a8a103c433f72236d5b0799123a67b6d40c628baae4',
     '_RESULT.md':'18541d435152d6022cd1ea35285ed339015a7df8f19012cfbfd3a8a54aad4a23',
     '_RECEIPT.json':'7896e0b78db294fe3b66886449d088afee4a6a413ee27056d09b6dde5ed05669'}
CYCLE=(0,4,3,7,2,6,1,5); EDGES=list(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
PAIRS=[(a,b) for a in range(8) for b in range(8) if a!=b]; INDEX={p:i for i,p in enumerate(PAIRS)}
W=np.arange(256); Q=((W[None,:]>>np.arange(8)[:,None])&1).astype(int); POP=Q.sum(0)
K=-np.array([1]*4+[-1]*4)@Q; ES=Q[0]+Q[4]
POS={v:i for i,v in enumerate(CYCLE)}; DIST=np.array([min(abs(POS[a]-POS[b]),8-abs(POS[a]-POS[b])) for a,b in PAIRS]); ADJ=(DIST==1)
T=.1; JC=.25; LAM=.5; H=.2; COUNT=0; MAXERR=0.; ACTIVE='preflight'; START=time.monotonic()

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def blob(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def exact(ok,label):
    global COUNT
    COUNT+=1
    if not ok:raise AssertionError(label)
def near(a,b,label,tol=2e-9):
    global COUNT,MAXERR
    a,b=np.asarray(a),np.asarray(b)
    exact(a.shape==b.shape,label+' shape')
    exact(np.all(np.isfinite(a)) and np.all(np.isfinite(b)),label+' finite')
    e=float(np.max(np.abs(a-b))) if a.size else 0.;MAXERR=max(MAXERR,e);COUNT+=a.size
    if e>tol:raise AssertionError(label+' error='+repr(e)+' tolerance='+repr(tol))
def cx(x):
    a=np.asarray(x);return a[...,0]+1j*a[...,1]
def compare(stored,expected,label):
    if expected is None:exact(stored is None,label+' null');return
    if isinstance(expected,dict):
        exact(set(stored)==set(expected),label+' fields')
        for k,v in expected.items():compare(stored[k],v,label+'.'+k)
        return
    if isinstance(expected,str):exact(stored==expected,label);return
    if isinstance(expected,(list,tuple)) and any(x is None or isinstance(x,dict) for x in expected):
        exact(len(stored)==len(expected),label+' length')
        for i,v in enumerate(expected):compare(stored[i],v,label+'.'+str(i))
        return
    z=np.asarray(expected)
    near(cx(stored) if np.iscomplexobj(z) else stored,z,label)
def save(p,obj):
    with Path(p).open('xb') as f:f.write(json.dumps(obj,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)

def custody():
    exact(not any(p.exists() for p in (AJ,AM,AE)),'exclusive audit output absence')
    for s,h in PIN.items():exact(sha(J/(NAME+s))==h,'frozen '+s)
    r=read(J/(NAME+'_RESULT.json'));rec=read(J/(NAME+'_RECEIPT.json'))
    exact(hashlib.sha256(blob(r)).hexdigest()==rec['result_canonical_sha256']=='bcd1ee7a77176a54fe80f0e235279587fb16fff92ebc7807f569e1b3d4cc3061','canonical')
    exact(rec['result_raw_sha256']==PIN['_RESULT.json'] and rec['report_sha256']==PIN['_RESULT.md'],'raw/report')
    exact(r['input_sha256']==rec['input_sha256'],'input maps')
    exact(r['passed']==rec['passed']==14830 and r['failed']==rec['failed']==0 and all(c['passed'] for c in r['checks']),'producer checks')
    exact(r['PID']==rec['PID']==57084 and r['original_manifest_PID']==rec['original_manifest_PID']==57084,'one execution PID')
    for f,h in rec['input_sha256'].items():exact(sha(ROOT/f)==h,'input '+f)
    cmap=rec['checkpoint_sha256'];actual={p.name for p in CP.iterdir() if p.name!='journal.jsonl'}
    exact(len(cmap)==1146 and actual==set(cmap),'checkpoint census')
    for f,h in cmap.items():exact(sha(CP/f)==h,'checkpoint '+f)
    jb=(CP/'journal.jsonl').read_bytes();events=[json.loads(b) for b in jb.splitlines()]
    exact(hashlib.sha256(b'\n'.join(jb.splitlines()[:-1])+b'\n').hexdigest()==rec['journal_prefix_sha256']=='f6efcde9e163e858de53076d4b929d454ee16fbad65bca89dd9365cdebc278f0','journal prefix')
    exact(events[-1]=={'event':'receipt_saved','sha256':PIN['_RECEIPT.json']},'receipt commit')
    exact(events[-2]=={'event':'report_saved','sha256':PIN['_RESULT.md'],'paired_data_rows':416},'report commit')
    exact(events[-3]=={'event':'result_saved','raw_sha256':PIN['_RESULT.json'],'canonical_sha256':rec['result_canonical_sha256']},'result commit')
    m=read(CP/'manifest.json');exact(m['input_sha256']==rec['input_sha256'] and m['PID']==57084,'manifest')
    exact(events[0]['event']=='started' and events[0]['PID']==57084 and events[0]['input_sha256']==rec['input_sha256'] and events[0]['manifest_sha256']==sha(CP/'manifest.json')==r['manifest_sha256'],'start seal')
    cm={'manifest.json':sha(CP/'manifest.json')}
    for e in events[1:-3]:
        exact('file' in e and 'sha256' in e and e['file'] not in cm,'unique stage commit');cm[e['file']]=e['sha256']
    exact(cm==cmap,'complete checkpoint commits')
    exact(len(r['preparations'])==104 and sum(len(p['rows']) for p in r['preparations'])==416,'full 104x4 census')
    exact(sum(x.startswith('|') for x in (J/(NAME+'_RESULT.md')).read_text().splitlines())==418,'report whole table')
    return r,rec,hashlib.sha256(blob(rec['input_sha256'])).hexdigest()

def maps(two):
    configs=PAIRS if two else [(a,) for a in range(8)]
    occ=np.array([[int(v in cfg) for v in range(8)] for cfg in configs])
    moves=[]
    for u,v in EDGES:
        per=[]
        for tag in range(2 if two else 1):
            lr=[]
            for i,cfg in enumerate(configs):
                if cfg[tag]!=u or v in cfg:continue
                c=list(cfg);c[tag]=v;lr.append((i,INDEX[tuple(c)] if two else v))
            per.append(lr)
        moves.append(per)
    return occ,moves
O2,M2=maps(True);O1,M1=maps(False)
def apply_saved_action(a,ar,two):
    """Independent instantaneous native sparse action; never evolves a state."""
    occ,moves=(O2,M2) if two else (O1,M1);nc=2 if two else 1
    diag=np.broadcast_to((8+nc+ar*POP)[:,None,None],a.shape[:3]).copy()
    diag[:,0,:]+=2+LAM*ES[:,None]
    for ei,(u,v) in enumerate(EDGES):
        xor=occ[:,u]+occ[:,v]-2*occ[:,u]*occ[:,v]
        for bit in (range(2) if ei else (1,)):diag[:,bit,:]+=JC*xor
    out=diag[:,:,:,None]*a-H*a[:,[1,0],:,:]
    for ei in range(8):
        for bit in (range(2) if ei else (1,)):
            for pairs in moves[ei]:
                for left,right in pairs:
                    out[:,bit,left,:]-=T*a[:,bit,right,:];out[:,bit,right,:]-=T*a[:,bit,left,:]
    return out
def marginals(a,two):
    if not two:
        mat=np.moveaxis(a,2,0).reshape(8,-1);return None,mat@mat.conj().T
    rho=[np.zeros((8,8),complex),np.zeros((8,8),complex)]
    for tag in range(2):
        for other in range(8):
            mat=np.zeros((8,256*2*a.shape[-1]),complex)
            for pos in range(8):
                if pos==other:continue
                i=INDEX[(pos,other) if tag==0 else (other,pos)];mat[pos]=a[:,:,i,:].reshape(-1)
            rho[tag]+=mat@mat.conj().T
    return rho
def observables(a,ar,two):
    ha=apply_saved_action(a,ar,two);ad=-1j*ha;occ,moves=(O2,M2) if two else (O1,M1)
    prob=np.einsum('qeil,qeil->qei',a.conj(),a).real
    pd=2*np.einsum('qeil,qeil->qei',a.conj(),ad).real
    qp=prob.sum((1,2));qpd=pd.sum((1,2));n=qp.sum();nd=qpd.sum();q=Q@qp;qd=Q@qpd;qq=(Q*qp)@Q.T
    empty=prob[:,0].sum();emptyd=pd[:,0].sum();edgez=2*empty-n
    edgec=np.sum(a[:,1].conj()*a[:,0]);edged=np.sum(ad[:,1].conj()*a[:,0]+a[:,1].conj()*ad[:,0])
    b=[];bd=[];eb=[]
    for v in range(8):
        lo=W[Q[v]==0];hi=lo+2**v
        b.append(2*np.sum(a[hi].conj()*a[lo]));bd.append(2*np.sum(ad[hi].conj()*a[lo]+a[hi].conj()*ad[lo]));eb.append(2*np.sum(a[hi,0].conj()*a[lo,0]))
    b=np.array(b);bd=np.array(bd);eb=np.array(eb);old=n-2*q+1j*b.imag;oldd=nd-2*qd+1j*bd.imag
    rho0,rho1=marginals(a,two);pc=prob.sum((0,1));pdconfig=pd.sum((0,1))
    curr=[[],[]] if two else [None,[]];div=[np.zeros(8),np.zeros(8)] if two else [None,np.zeros(8)];hop=0.;one=0.;direct=0.;adjactual=0.
    for ei,(u,v) in enumerate(EDGES):
        for tag,lr in enumerate(moves[ei]):
            cross=0j
            for bit in (range(2) if ei else (1,)):
                for left,right in lr:cross+=np.sum(a[:,bit,left].conj()*a[:,bit,right])
            itag=tag if two else 1;cu=2*T*cross.imag;curr[itag].append(cu);div[itag][u]-=cu;div[itag][v]+=cu;hop-=2*T*cross.real
        for bit in (range(2) if ei else (1,)):
            p=prob[:,bit].sum(0);both=occ[:,u]*occ[:,v];one+=JC*((occ[:,u]+occ[:,v])@p);direct-=2*JC*(both@p);adjactual+=both@p
    if two:
        sourcep=np.diag(rho0).real;p0d=np.array([pdconfig[[i for i,(s,p) in enumerate(PAIRS) if s==v]].sum() for v in range(8)])
        p1d=np.array([pdconfig[[i for i,(s,p) in enumerate(PAIRS) if p==v]].sum() for v in range(8)])
    else:sourcep=None;p0d=None;p1d=pdconfig
    charge=ar*(POP@qp);feedback=LAM*(ES@prob[:,0].sum(1));flip=-2*H*edgec.real;nc=2 if two else 1
    energy=(8+nc)*n+charge+2*empty+feedback+one+direct+hop+flip
    near(np.vdot(a,ha).real,energy,'independent full/term energy',1e-8);near(qpd,np.zeros(256),'all q derivative');near(p1d,div[1],'probe continuity');near(emptyd,2*H*edgec.imag,'edge continuity')
    if two:near(p0d,div[0],'source continuity')
    near(bd,1j*ar*b+1j*LAM*eb*np.array([1,0,0,0,1,0,0,0]),'full record commutator')
    sectors=[]
    for qa,qb in ((0,0),(0,1),(1,0),(1,1)):
        sel=(Q[0]==qa)&(Q[4]==qb);weight=qp[sel].sum();joint=prob[sel,0].sum();pos=prob[sel].sum((0,1));ep=prob[sel,0].sum(0)
        sec={'q0':qa,'q4':qb,'weight':weight,'empty_joint':joint,'empty_conditional':None if weight==0 else joint/weight,'position_joint_probability':pos,'position_conditional_probability':None if weight==0 else pos/weight,'empty_position_joint_probability':ep}
        if two:sec.update(tagged_reference_adjacency_joint=ADJ@pos,tagged_reference_adjacency_conditional=None if weight==0 else (ADJ@pos)/weight,tagged_reference_separation_joint=DIST@pos,tagged_reference_separation_conditional=None if weight==0 else (DIST@pos)/weight)
        sectors.append(sec)
    o={'norm':n,'empty_edge_probability':empty,'empty_edge_dot':emptyd,'incidence_Pauli':{'X':2*edgec.real,'Y':-2*edgec.imag,'Z':edgez},'incidence_Pauli_dot':{'X':2*edged.real,'Y':-2*edged.imag,'Z':2*emptyd-nd},'source_p_global':sourcep,'probe_p_global':np.diag(rho1).real,'source_p_dot_global':p0d,'probe_p_dot_global':p1d,'source_density_global':rho0,'probe_density_global':rho1,'source_edge_current_cycle':curr[0],'probe_edge_current_cycle':curr[1],'source_current_divergence':div[0],'probe_current_divergence':div[1],'record_word_probability':qp,'record_q_global':q,'record_qq_global':qq,'endpoint_record_conditioning':sectors,'record_Pauli_global':{'X':b.real,'Y':-b.imag,'Z':n-2*q},'record_Pauli_dot_global':{'X':bd.real,'Y':-bd.imag,'Z':nd-2*qd},'return_charge_number_probability':np.array([qp[K==k].sum() for k in range(-4,5)]),'Bplus_beta_global':b,'Bplus_dot_global':bd,'Bplus_amplitude_global':abs(b),'empty_joint_Bplus_global':eb,'Bplus_dot_charging':1j*ar*b,'Bplus_dot_endpoint_feedback':1j*LAM*eb*np.array([1,0,0,0,1,0,0,0]),'original_Z_minus_iY_beta_global':old,'original_Z_minus_iY_dot_global':oldd,'bare_return_traced_X_global':np.zeros(8),'bare_return_traced_Y_global':np.zeros(8),'field_self_energy':8*n,'carrier_storage_energy':nc*n,'retained_record_charging_energy':charge,'degree_defect_energy':2*empty,'record_feedback_change_energy':feedback,'current_onebody_energy':one,'direct_current_cross_energy':direct,'actual_occupied_hopping_energy':hop,'incidence_flip_energy':flip,'full_energy':energy}
    if two:
        ep=prob[:,0].sum(0)
        o.update(ordered_pair_probability=pc,tagged_cycle_reference_separation_probability=np.array([pc[DIST==d].sum() for d in range(5)]),tagged_cycle_reference_mean_separation=DIST@pc,tagged_cycle_reference_adjacency=ADJ@pc,actual_occupied_pair_adjacency=adjactual,empty_joint_ordered_pair_probability=ep,empty_joint_source_probability=np.array([ep[[i for i,(s,p) in enumerate(PAIRS) if s==v]].sum() for v in range(8)]),empty_joint_probe_probability=np.array([ep[[i for i,(s,p) in enumerate(PAIRS) if p==v]].sum() for v in range(8)]))
    else:
        app=np.sum(abs(a.reshape(256,2,8,8,8))**2,axis=(0,1,4)).T;dist=np.array([[min(abs(POS[u]-POS[v]),8-abs(POS[u]-POS[v])) for v in range(8)] for u in range(8)])
        o.update(apparatus_position_probe_joint_probability=app,apparatus_marker_reference_separation_probability=np.array([app[dist==d].sum() for d in range(5)]),apparatus_marker_reference_mean_separation=np.sum(dist*app),apparatus_marker_scope='Stored initial source position in the traced preparation apparatus; no moving absent source.',empty_joint_probe_probability=prob[:,0].sum(0))
    return o,ha

def ratecheck(stored,label):
    for stem in ('Bplus','original_Z_minus_iY'):
        b=cx(stored[stem+'_beta_global']);d=cx(stored[stem+'_dot_global']);rates=stored[stem+'_rate_global']
        for v in range(8):
            z=abs(b[v])**2
            if z==0:exact(rates[v] is None,label+' exact zero raw rate')
            else:
                r=(b[v].conjugate()*d[v]).imag/z;near(rates[v],r,label+' raw transparent rate',2e-10*(1+abs(r)))

def run():
    global ACTIVE
    r,rec,imap=custody();cmap=rec['checkpoint_sha256']
    with np.load(CP/'reaction_eigensystems.npz',allow_pickle=False) as z:
        nm=json.loads(str(z['metadata_json']));bm=z['tagged_base_matrices'];be=z['tagged_base_eigenvalues'];bv=z['tagged_base_eigenvectors'];rm=z['reference_base_matrices'];re=z['reference_base_eigenvalues'];rv=z['reference_base_eigenvectors']
        near(z['ordered_tagged_pairs'],PAIRS,'ordered map');near(z['global_record_bits'],Q,'record bit map');near(z['cycle_global_nodes'],CYCLE,'cycle')
        for ai,ar in enumerate((0,.125,.175,.25)):
            near(z['tagged_absolute_eigenvalues_all_AR'][ai],be[ES]+ar*POP[:,None],'all tagged scalar phases');near(z['reference_absolute_eigenvalues_all_AR'][ai],re[ES]+ar*POP[:,None],'all reference scalar phases')
    exact(nm['input_sha256']==rec['input_sha256'] and nm['new_eigensolver_calls']==3 and nm['reference_eigensolver_calls']==0 and all(c['passed'] for c in nm['checks']),'saved eigensystem metadata')
    for two,mat,ev,vec,dim in ((True,bm,be,bv,56),(False,rm,re,rv,8)):
        for s,qword in enumerate((0,1,17)):
            template=np.zeros((256,2,dim,2*dim),complex);template[qword]=np.eye(2*dim).reshape(2,dim,2*dim)
            near(apply_saved_action(template,0,two)[qword].reshape(2*dim,2*dim),mat[s],'literal small saved matrix');near(mat[s],mat[s].T,'Hermitian')
            near(mat[s]@vec[s],vec[s]*ev[s][None,:],'saved eigen residual');near(vec[s].T@vec[s],np.eye(2*dim),'saved eigen Gram')
            del template
    diagnostics=[];parent=read(J/'FLOATING_RETURN_C8_RETAINED_RECORD_GEOMETRY_V001_RESULT.json')
    for pi,p in enumerate(r['preparations']):
        ACTIVE=p['preparation'];name=p['preparation'];exact(name=='case%02d_prep%02d'%divmod(pi,13),'preparation ordering')
        exact(read(CP/(name+'_complete.json'))==p,'complete data equality');meta=read(CP/(name+'_initial.json'));ar=float(Fraction(p['AR_rational']))
        exact(meta['input_map_sha256']==imap and meta['initial_state_sha256']==cmap[name+'_initial.npz'] and meta['eigensystem_sha256']==cmap['reaction_eigensystems.npz'],'initial custody')
        with np.load(CP/(name+'_initial.npz'),allow_pickle=False) as z:
            on0=z['psi_tagged_initial'];ref0=z['psi_reference_initial'];co=z['tagged_spectral_coefficients'];cr=z['reference_spectral_coefficients'];exact(json.loads(str(z['metadata_json']))==meta['npz_metadata'],'initial NPZ metadata')
        with np.load(PCP/(name+'_initial.npz'),allow_pickle=False) as z:old=z['psi_initial']
        near(on0,old[:,:,np.array(PAIRS)[:,0],:]/math.sqrt(7),'vacancy amplitude identity')
        shaped=ref0.reshape(256,2,8,8,8)
        for a in range(8):
            for b in range(8):near(shaped[:,:,b,a,:],np.zeros((256,2,8)) if a==b else on0[:,:,INDEX[(a,b)],:],'factored channel full q coherence')
        near(on0.reshape(-1,8).conj().T@on0.reshape(-1,8),old.reshape(-1,8).conj().T@old.reshape(-1,8),'isometry Gram')
        rhos,rhop=marginals(on0,True);_,rhor=marginals(ref0,False);_,rhoold=marginals(old,False)
        near(rhop,rhor,'initial complete probe marginal');disturbed=(6/7)*rhoold;np.fill_diagonal(disturbed,np.diag(rhoold));near(rhos,disturbed,'source coherence 6/7')
        o0,hon=observables(on0,ar,True);f0,href=observables(ref0,ar,False)
        near(o0['record_word_probability'],f0['record_word_probability'],'initial full record marginal');near(o0['Bplus_beta_global'],f0['Bplus_beta_global'],'initial cross q clock marginal')
        near(o0['Bplus_beta_global'],cx(meta['initial_clock_Bplus_global']),'initial stored clock');near(meta['initial_tagged_energy'],o0['full_energy'],'initial tagged energy');near(meta['initial_reference_energy'],f0['full_energy'],'initial reference energy')
        near(meta['record_word_probability'],o0['record_word_probability'],'initial stored q');near(cx(meta['source_preparation_density_global']),rhos,'initial source density');near(cx(meta['probe_preparation_density_global']),rhop,'initial probe density')
        pm=read(PCP/(name+'_initial.json'));near(meta['copy_off_work'],pm['copy_off_work'],'accounted Woff');near(meta['parent_post_copy_off_energy'],pm['expected_post_switch_energy'],'parent full energy')
        adjacency=np.zeros((8,8))
        for u,v in EDGES:adjacency[u,v]=adjacency[v,u]=1
        cost=83/70+np.trace(rhoold@adjacency).real/70
        near(o0['full_energy']-pm['expected_post_switch_energy'],cost,'matched complete insertion',1e-8);near(meta['insertion_work'],cost,'stored insertion work',1e-8)
        near(meta['source_removal_reference_work'],f0['full_energy']-o0['full_energy'],'actual removal work',1e-8);near(meta['net_reference_preparation_work'],f0['full_energy']-pm['expected_post_switch_energy'],'reference net work',1e-8)
        exact(81/70-1e-8<=cost<=85/70+1e-8,'insertion bounds');near(on0[:,0],np.zeros_like(on0[:,0]),'initial occupied anchor');near(ref0[:,0],np.zeros_like(ref0[:,0]),'reference occupied anchor')
        for qword in range(256):
            near(co[qword],bv[ES[qword]].T@on0[qword].reshape(112,8),'initial saved tagged coefficients');near(cr[qword],rv[ES[qword]].T@ref0[qword].reshape(16,64),'initial saved reference coefficients')
        for ti,row in enumerate(p['rows']):
            ACTIVE=name+'/forward'+str(ti);x=float(Fraction(row['x_rational']));exact(row['forward_time_index']==ti and row['x_rational']==('0','1/5','2','8')[ti],'forward census')
            exact(read(CP/row['row_file'])==row and row['state_sha256']==cmap[row['state_file']] and row['initial_state_sha256']==meta['initial_state_sha256'] and row['input_map_sha256']==imap,'row custody')
            with np.load(CP/row['state_file'],allow_pickle=False) as z:
                on=z['psi_tagged'];ref=z['psi_reference'];nmeta=json.loads(str(z['metadata_json']))
            for k,v in nmeta.items():exact(row[k]==v,'frame metadata '+k)
            oo,hon=observables(on,ar,True);ff,href=observables(ref,ar,False)
            for branch,obs in (('tagged',oo),('paired_reference',ff)):
                raw=row[branch];expected=dict(obs);expectedkeys=set(expected)|{'Bplus_rate_global','original_Z_minus_iY_rate_global'};exact(set(raw)==expectedkeys,'complete observation schema')
                for k,v in expected.items():compare(raw[k],v,ACTIVE+'/'+branch+'/'+k)
                ratecheck(raw,ACTIVE+'/'+branch);near(obs['norm'],1.,'norm');near(obs['record_word_probability'],o0['record_word_probability'],'all conserved words')
                near(obs['full_energy'],meta['initial_tagged_energy' if branch=='tagged' else 'initial_reference_energy'],'whole branch conserved energy',1e-8)
            other=np.array([1,2,3,5,6,7]);near(oo['Bplus_beta_global'][other],o0['Bplus_beta_global'][other]*np.exp(1j*ar*x),'six exact formed phases');near(ff['Bplus_beta_global'][other],oo['Bplus_beta_global'][other],'same six clocks')
            near(on.reshape(-1,8).conj().T@on.reshape(-1,8),on0.reshape(-1,8).conj().T@on0.reshape(-1,8),'tagged complete mixture Gram');near(ref.reshape(-1,64).conj().T@ref.reshape(-1,64),ref0.reshape(-1,64).conj().T@ref0.reshape(-1,64),'reference complete mixture Gram')
            if ti==0:near(on,on0,'saved forward zero tagged');near(ref,ref0,'saved forward zero reference')
            diff={'probe_p_global':oo['probe_p_global']-ff['probe_p_global'],'probe_density_global':oo['probe_density_global']-ff['probe_density_global'],'probe_edge_current_cycle':np.array(oo['probe_edge_current_cycle'])-np.array(ff['probe_edge_current_cycle']),'empty_edge_probability':oo['empty_edge_probability']-ff['empty_edge_probability'],'endpoint_Bplus_difference':oo['Bplus_beta_global'][[0,4]]-ff['Bplus_beta_global'][[0,4]]}
            compare(row['source_presence_difference'],diff,ACTIVE+'/signed paired difference')
            for k in ('copy_off_work','insertion_work','source_removal_reference_work'):near(row[k],meta[k],'row accounted '+k)
            exact(row['ideal_clock_structural_null']==meta['ideal_clock_structural_null'],'structural clock flag')
            diagnostics.append({'preparation':name,'AR':p['AR_rational'],'prep_x':p['preparation_x_rational'],'forward_x':row['x_rational'],'probe_density_difference_norm':float(np.linalg.norm(diff['probe_density_global'])),'empty_difference':float(diff['empty_edge_probability']),'tagged_adjacency':float(oo['tagged_cycle_reference_adjacency']),'tagged_mean_steps':float(oo['tagged_cycle_reference_mean_separation']),'apparatus_mean_steps':float(ff['apparatus_marker_reference_mean_separation']),'insertion_work':float(meta['insertion_work']),'removal_work':float(meta['source_removal_reference_work'])})
            del on,ref,hon,href,oo,ff
        del on0,ref0,old,co,cr,shaped,rhos,rhop,rhor,rhoold,o0,f0
        if (pi+1)%13==0:print(json.dumps({'audited_preparations':pi+1,'assertions':COUNT,'maximum_absolute_residual':MAXERR}),flush=True)
    for f,h in rec['input_sha256'].items():exact(sha(ROOT/f)==h,'final input recheck '+f)
    for s,h in PIN.items():exact(sha(J/(NAME+s))==h,'final seal '+s)
    out={'audit_status':'PASS','assertions':COUNT,'failed_assertions':0,'maximum_absolute_residual':MAXERR,'audited_preparations':104,'audited_tagged_frames':416,'audited_paired_reference_frames':416,'producer_passed':14830,'result_raw_sha256':PIN['_RESULT.json'],'receipt_sha256':PIN['_RECEIPT.json'],'audit_source_sha256':sha(__file__),'PID':os.getpid(),'elapsed_seconds':time.monotonic()-START,'peakRSS_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'method':'Independent instantaneous literal H action on saved amplitudes and factored partial traces; no propagation, eigensolver or producer import. All current and inherited seals checked. Raw null-clock phase rates are transparent ratios without clock qualification.','diagnostics_all416':diagnostics,'scope':'Accounted supplied-C8 tagged reaction, direct current, exclusion, recoil and retained-record geometry; no universal gravity, physical ruler, phase or proper-clock adoption.'}
    h=save(AJ,out)
    text='# Independent saved-state tagged reaction audit\n\nPASS: %d assertions, 104 preparations and 416 paired frames. Maximum absolute residual %.6g.\n\nThe independent audit verified all input/checkpoint/journal seals, full vacancy/channel amplitudes, reduced density matrices, currents, instantaneous action derivatives, energies and preparation work, conserved record/return distributions, endpoint-conditioned geometry, cross-q clocks and signed probe comparisons. No propagation, eigensolver or producer was replayed. Raw structurally null clock rates remain unqualified.\n\nThis is an accounted reaction on the supplied C8; apparatus-marker steps are distinct from distance to the moving tagged source. No gravitational or physical-ruler conclusion follows.\n\nAudit JSON SHA256: %s\n'%(COUNT,MAXERR,h)
    with AM.open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
    print(json.dumps({'status':'PASS','assertions':COUNT,'maximum_absolute_residual':MAXERR,'audit_sha256':h,'report_sha256':sha(AM),'PID':os.getpid(),'elapsed_seconds':time.monotonic()-START}),flush=True)

if __name__=='__main__':
    if sys.argv[1:]!=['--audit']:raise SystemExit('Exact --audit required; no calculation performed.')
    print(json.dumps({'audit_PID':os.getpid(),'method':'saved amplitudes only; no propagation/eigh/producer import'}),flush=True)
    try:run()
    except Exception as e:
        v={'audit_status':'FAIL_PRESERVED','error':repr(e),'active':ACTIVE,'assertions_before_failure':COUNT,'maximum_absolute_residual':MAXERR,'PID':os.getpid(),'traceback':traceback.format_exc()}
        if not AE.exists():save(AE,v)
        print(json.dumps(v),flush=True);raise SystemExit(3)
