#!/usr/bin/env python3
"""Independent saved-only acceptance of the declared D_rel control.
Root alone executes after closure. No producer import, H reconstruction,
eigensolver, propagation, RNG replay or changed response criterion.
Exact-S/R nearby-mode conditioning is a separate diagnostic, not acceptance.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
import sys,json,hashlib,math,time,traceback
from pathlib import Path
from fractions import Fraction
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_RELATIVE_ENERGY_SPECTRAL_RESPONSE_V001';STEM='floating_return_c8_relative_energy_spectral_response_v001';CP=J/(STEM+'_checkpoints')
LOCAL='FLOATING_RETURN_C8_LOCALIZED_LAPSE_RESPONSE_V001';LSTEM='floating_return_c8_localized_lapse_response_v001';LCP=J/(LSTEM+'_checkpoints')
CERT='FLOATING_RETURN_C8_RELATIVE_ENERGY_PROJECTOR_CERTIFICATE_V001';CSTEM='floating_return_c8_relative_energy_projector_certificate_v001'
OLD=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001','floating_return_c8_tagged_probe_reaction_v001'),('FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001','floating_return_c8_endpoint_record_isolation_v001'))
PINS={NAME+'_RESULT.json':'af4e377e6a5fa3713509156c2266406f56822f0d2e8cac65eb2a578c7cc850da',NAME+'_RECEIPT.json':'bdb5df80ed6db1cfc164b02a966fad7dbf30bb96ee36928f0e29405c9e54efe1',STEM+'.py':'0a65a698096facdccde5b8a027115e6bf00e62182d42fad309277b09d13341e9',NAME+'.md':'b8337f327c8503e505f2099c38bd61550ae005ca369a886fce076b9be802ed6a',LOCAL+'_RESULT.json':'d773bbc65029acf287f0008db77dd1a897079988c7c766c955e4438383b860a8',LOCAL+'_RECEIPT.json':'4bc0cf0c6ccca2657e886fe6f4d5a1328c5afa4027b17d3358c58374b6775fd9',LOCAL+'_AUDIT.json':'1b06f159ddbd9f2f6fee74ec50c502b5b481bc4b5eebda3bcdb70131a595a020',LOCAL+'_AUDIT.md':'2eb0620fc8ce3b26d9c4e795369a5e2fb2de51389f4e795b6dcb223cc6d37e86',CERT+'_RESULT.json':'584ce7064f7f388df6d1ddcd6465adb91c72c0098a86116d1cb289de533def9a',CERT+'_RECEIPT.json':'99b96af6ba34e39cab489edfd1c898dca5dafe2d2ab2d8c38b2e70afdfc48fcb'}
OUT=J/(NAME+'_AUDIT.json');MD=J/(NAME+'_AUDIT.md');RECEIPT=J/(NAME+'_AUDIT_RECEIPT.json');ERROR=J/(NAME+'_AUDIT_ERROR.json')
OP=5e-10;OBS=1e-9;EN=5e-9;BAND=1e-9;Z=1j/5;H=.2;T=.1;JC=.25
LABELS=('retained_on','retained_reference','reset_on','reset_reference');REST=(1,2,3,5,6,7);ARS=('0','1/8','7/40','1/4');AGES=('0','1/10','1/5','2/5','4/5','1','2','4','8','12','16','24','32')
CYCLE=(0,4,3,7,2,6,1,5);PAIRS=tuple((a,b) for a in range(8) for b in range(8) if a!=b);PIND={p:i for i,p in enumerate(PAIRS)}
OPS=('Vc','Vm','H','n','I');PACKED=tuple((a,b) for a in range(5) for b in range(a,5))
INPUTS={};CHECKS=[];ASSERTIONS=0;MAXERR=0.;ACTIVE={};STARTED=False
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def blob(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(k):return Path(k) if Path(k).is_absolute() else ROOT/k
def pin(p,h):
    p=Path(p).resolve();k=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
    if k not in INPUTS:
        if sha(p)!=h:raise AssertionError('seal '+k)
        INPUTS[k]=h
    elif INPUTS[k]!=h:raise AssertionError('conflicting seal '+k)
def exact(name,ok):
    global ASSERTIONS
    ASSERTIONS+=1;CHECKS.append({'name':name,'passed':bool(ok)})
    if not ok:raise AssertionError(name)
def close(name,a,b,tol=OBS):
    global ASSERTIONS,MAXERR
    a,b=np.asarray(a),np.asarray(b);finite=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)));err=float(np.max(np.abs(a-b))) if finite else math.inf
    ASSERTIONS+=max(a.size,b.size,1);MAXERR=max(MAXERR,err);CHECKS.append({'name':name,'passed':finite and err<=tol,'error':err,'tolerance':tol})
    if not finite or err>tol:raise AssertionError((name,err,tol))
def cv(x):
    a=np.asarray(x,dtype=float);return a[...,0]+1j*a[...,1]
def clean(x):
    if isinstance(x,np.ndarray):return clean(x.tolist())
    if isinstance(x,np.generic):return clean(x.item())
    if isinstance(x,complex):return [float(x.real),float(x.imag)]
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    if isinstance(x,float) and not math.isfinite(x):return {'nonfinite':repr(x)}
    return x
def write(p,x):
    with Path(p).open('xb') as f:f.write(json.dumps(clean(x),sort_keys=True,indent=2,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
    return sha(p)
def packet(name,stem,nfiles,nevents,nrows=None,row_key='data_rows'):
    cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'))
    for suffix in ('_RESULT.json','_RECEIPT.json','_RESULT.md'):pin(J/(name+suffix),sha(J/(name+suffix)))
    exact(name+' raw/canonical/report',r['result_raw_sha256']==sha(J/(name+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(blob(p)).hexdigest() and r['report_sha256']==sha(J/(name+'_RESULT.md')))
    exact(name+' arithmetic/status',p['failed']==r['failed']==0 and p['passed']==r['passed']==len(p['checks']) and all(c['passed'] for c in p['checks']) and p['input_sha256']==r['input_sha256'])
    for k,h in r['input_sha256'].items():pin(path(k),h)
    cm=r['checkpoint_sha256'];exact(name+' checkpoint census',len(cm)==nfiles and set(cm)=={f.name for f in cp.iterdir() if f.name!='journal.jsonl'})
    for f,h in cm.items():pin(cp/f,h)
    raw=(cp/'journal.jsonl').read_bytes();lines=raw.splitlines();es=[json.loads(v) for v in lines];pin(cp/'journal.jsonl',sha(cp/'journal.jsonl'))
    report={'event':'report_saved','sha256':r['report_sha256']}
    if nrows is not None:report[row_key]=nrows
    exact(name+' final journal',len(es)==nevents and hashlib.sha256(b'\n'.join(lines[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'] and es[-1]=={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))} and es[-2]==report and es[-3]=={'event':'result_saved','raw_sha256':r['result_raw_sha256'],'canonical_sha256':r['result_canonical_sha256']})
    mh=sha(cp/'manifest.json');m=read(cp/'manifest.json');exact(name+' manifest/start',p['manifest_sha256']==mh and m['PID']==p['PID']==r['PID'] and m['input_sha256']==r['input_sha256'] and es[0]=={'event':'started','PID':p['PID'],'manifest_sha256':mh,'input_sha256':r['input_sha256']})
    committed={'manifest.json':mh}
    for event in es[1:-3]:
        exact(name+' unique commit '+event['file'],event['file'] not in committed);committed[event['file']]=event['sha256']
    exact(name+' complete commit map',committed==cm);return p,r
def physical(d,two):
    """Only literal source/readout operators; Hamiltonians remain saved inputs."""
    carriers=PAIRS if two else tuple((a,) for a in range(8));index={p:i for i,p in enumerate(carriers)}
    occ=np.array([[int(v in p) for p in carriers] for v in range(8)]);empty=np.diag(np.r_[np.ones(d),np.zeros(d)]);n=np.eye(2*d)-empty
    x=np.zeros((2*d,2*d));x[:d,d:]=np.eye(d);x[d:,:d]=np.eye(d);current=1j*H*(n@x-x@n)
    bare=np.eye(2*d)+empty+np.diag(np.tile(occ[0],2))
    for u,v in ((0,4),(0,5)):
        cut=occ[u]+occ[v]-2*occ[u]*occ[v]
        for bit in ((1,) if v==4 else (0,1)):
            start=bit*d;bare[start:start+d,start:start+d]+=np.diag(JC*cut/2)
            for col,p in enumerate(carriers):
                for species,node in enumerate(p):
                    if node not in (u,v):continue
                    dest=v if node==u else u
                    if dest in p:continue
                    q=list(p);q[species]=dest;bare[start+index[tuple(q)],start+col]-=T/2
    bare-=H*x/2;return bare,empty,n,current,x
def words(reset):return np.array([sum(((r>>k)&1)<<v for k,v in enumerate(REST)) for r in range(64)]) if reset else np.arange(256)
def partial_probe(rho,two):
    if not two:return rho
    padded=np.zeros((128,128),complex);indices=np.array([bit*64+8*a+b for bit in (0,1) for a,b in PAIRS]);padded[np.ix_(indices,indices)]=rho
    return np.einsum('iabjad->ibjd',padded.reshape(2,8,8,2,8,8)).reshape(16,16)
def beta_raw(a,ws):
    lookup={int(q):i for i,q in enumerate(ws)};b=np.zeros(8,complex)
    for v in range(8):
        for lo,q in enumerate(ws):
            if not int(q)&(1<<v) and int(q)+(1<<v) in lookup:b[v]+=2*np.vdot(a[lookup[int(q)+(1<<v)]],a[lo])
    return b
def contrasts(m):return {'source_presence_retained':m[0]-m[1],'source_presence_transferred':m[2]-m[3],'retained_minus_transferred_on':m[0]-m[2],'retained_minus_transferred_reference':m[1]-m[3],'difference_of_differences':m[0]-m[1]-m[2]+m[3]}
def main():
    global STARTED
    if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute.')
    if 'PENDING_NATURAL_CLOSURE' in PINS.values():raise SystemExit('Natural closure pins are pending.')
    if any(p.exists() for p in (OUT,MD,RECEIPT,ERROR)):raise SystemExit('Exclusive audit output exists.')
    STARTED=True;start=time.monotonic()
    for f,h in PINS.items():pin(J/f,h)
    p,r=packet(NAME,STEM,938,941,416);local,lr=packet(LOCAL,LSTEM,7594,7597,4160);cert,cr=packet(CERT,CSTEM,21,24)
    old=[packet(a,b,1146,1149,416,'paired_data_rows')[0] for a,b in OLD]
    accepted=read(J/(LOCAL+'_AUDIT.json'));exact('accepted localized audit',accepted['audit_status']=='PASS' and not accepted['failed_assertions'] and accepted['result_raw_sha256']==lr['result_raw_sha256'] and accepted['receipt_sha256']==sha(J/(LOCAL+'_RECEIPT.json')) and (accepted['audited_preparations'],accepted['audited_source_frames'],accepted['audited_channel_time_rows'])==(104,1664,4160))
    exact('full response census',p['preparation_count']==104 and p['control_count']==416 and p['operator_order']==list(OPS) and len(p['preparations'])==104)
    exact('report 416 rows',sum(line.startswith('|case') for line in (J/(NAME+'_RESULT.md')).read_text().splitlines())==416)
    with np.load(LCP/'reused_localized_response_bases.npz',allow_pickle=False) as f:saved={k:f[k].copy() for k in f.files if k!='metadata_json'}
    with np.load(CP/'relative_response_bases.npz',allow_pickle=False) as f:new={k:f[k].copy() for k in f.files if k!='metadata_json'};basemeta=json.loads(str(f['metadata_json']))
    exact('basis metadata seals/checks',basemeta['input_map_sha256']==hashlib.sha256(blob(r['input_sha256'])).hexdigest() and all(c['passed'] for c in basemeta['checks']))
    bs={}
    for sector,two in (('tagged',True),('reference',False)):
        ev=saved[sector+'_eigenvalues'];v=saved[sector+'_eigenvectors'];hs=saved[sector+'_base_matrices'];d=56 if two else 8;bare,empty,n,current,x=physical(d,two)
        stage=next(t for t in cert['sector_census'] if t['sector']==sector);exact('certificate duplicate '+sector,stage==read(J/(CSTEM+'_checkpoints')/(sector+'_root_census.json')))
        roots={t['root_ID']:t for t in stage['root_intervals']};ids=[t['mode_exact_root_ID'] for t in stage['loading_rows']];intervals=np.array([[[float(Fraction(a)) for a in roots[t]['native_interval']] for t in row] for row in ids]);exact('simple/disjoint exact roots '+sector,len(set(sum(ids,[])))==3*2*d)
        for s in range(3):
            close('sorted certified modes '+sector+str(s),stage['loading_rows'][s]['saved_native_eigenvalues'],ev[s],0.);exact('ordered modes '+sector+str(s),bool(np.all(np.diff(ev[s])>0)))
            close('saved Gram '+sector+str(s),v[s].conj().T@v[s],np.eye(2*d),OP);close('saved H action '+sector+str(s),hs[s]@v[s],v[s]*ev[s][None,:],OP)
            gram=v[s].conj().T@v[s]-np.eye(2*d);complete=v[s]@v[s].conj().T-np.eye(2*d);res=hs[s]@v[s]-v[s]*ev[s][None,:];vn=np.sqrt(np.sum(abs(v[s])**2,axis=0));rn=np.sqrt(np.sum(abs(res)**2,axis=0));metric=basemeta['projector_metrics'][sector][s]
            close('complete body resolution '+sector+str(s),complete,0.,OP);close('rank-one idempotence '+sector+str(s),abs(vn**2-1)*vn**2,metric['projector_idempotence_Frobenius_each'],OP);close('rank-one commutator bounds '+sector+str(s),2*rn*vn,metric['projector_commutator_upper_each'],OP)
            for key,value in (('Gram_max',np.max(abs(gram))),('Gram_Frobenius',np.linalg.norm(gram)),('action_max',np.max(abs(res))),('action_Frobenius',np.linalg.norm(res)),('completeness_max',np.max(abs(complete))),('completeness_Frobenius',np.linalg.norm(complete))):close('saved projector metric '+sector+str(s)+key,metric[key],value,OP)
        projected={key:np.array([u.conj().T@operator@u for u in v]) for key,operator in (('bare',bare),('pe',empty),('n',n),('I',current),('X',x))}
        for k,oracle in (('ev',ev),('vec',v),*projected.items()):close('literal basis '+sector+k,new[sector+'_'+k],oracle,OP)
        exact('complete replicated root IDs '+sector,new[sector+'_mode_exact_root_ID'].tolist()==ids)
        bs[sector]={'ev':ev,'v':v,'hs':hs,'d':d,'two':two,'bare':bare,'empty':empty,'n':n,'I':current,'x':x,'projected':projected,'ids':ids,'intervals':intervals}
    summaries=[]
    for j,prep in enumerate(p['preparations']):
        ACTIVE.update(preparation=j);name='case%02d_prep%02d'%divmod(j,13);exact('ordered case/age '+name,prep['preparation']==name and prep['AR_rational']==ARS[j//26] and prep['formation_gamma_rational']==('0' if (j//13)%2==0 else '1/10') and prep['formation_age_rational']==AGES[j%13])
        exact('preparation duplicate '+name,prep==read(CP/(name+'_complete.json')));exact('four channel labels '+name,[q['channel'] for q in prep['channels']]==list(LABELS));ab=[];st=[];probes=[];betas=[]
        for row in prep['channels']:
            label=row['channel'];ACTIVE['channel']=label;reset=label.startswith('reset');two=label.endswith('_on');sector='tagged' if two else 'reference';b=bs[sector];v=b['v'];ev=b['ev'];d=b['d'];ws=words(reset);bits=np.array([[(int(q)>>k)&1 for k in range(8)] for q in ws]);load=bits[0]+bits[4];popq=bits.sum(0);ar=float(Fraction(prep['AR_rational']));nmode=2*d
            exact('row duplicate '+label,row==read(CP/(name+'_'+label+'.json')));exact('row/bundle/input seals '+label,row['bundle_file']==name+'_'+label+'.npz' and row['bundle_sha256']==sha(CP/row['bundle_file']) and row['input_map_sha256']==hashlib.sha256(blob(r['input_sha256'])).hexdigest() and row['input_factor_sha256']==sha(path(row['input_factor_source_file'])))
            with np.load(CP/row['bundle_file'],allow_pickle=False) as f:out={k:f[k].copy() for k in f.files if k!='metadata_json'};meta=json.loads(str(f['metadata_json']))
            exact('bundle metadata duplicate '+label,meta=={k:value for k,value in row.items() if k not in ('bundle_file','bundle_sha256','input_map_sha256','checks')})
            parentrow=old[int(reset)]['preparations'][j]['rows'][0];rawpath=J/(OLD[int(reset)][1]+'_checkpoints')/parentrow['state_file'];exact('old raw state seal '+label,sha(rawpath)==parentrow['state_sha256'])
            with np.load(rawpath,allow_pickle=False) as f:raw=f['psi_tagged' if two else 'psi_reference'].copy()
            a=raw.reshape(len(ws),nmode,raw.shape[-1]);c=np.stack([v[int(s)].conj().T@a[q] for q,s in enumerate(load)]);prob=np.sum(c.real*c.real+c.imag*c.imag,axis=2);mass=prob.sum(1)
            with np.load(path(row['input_factor_source_file']),allow_pickle=False) as f:close('raw physical-to-mode transform '+label,c,f['saved_state_spectral_coefficients'],OP);parentmeta=json.loads(str(f['metadata_json']));coeffs={k:f[k+'_source_coefficients'].copy() for k in ('Vc','Vm','H')}
            close('all q/mode probabilities '+label,out['q_mode_probability'],prob,OBS);close('all q-word mass '+label,out['network_q_word_probability'],mass,OBS);close('word map '+label,out['global_record_words'],ws,0.);close('initial norm '+label,prob.sum(),1.,OBS);close('row norm '+label,row['network_norm'],prob.sum(),OBS)
            close('q means '+label,row['network_q_means_global'],bits@mass,OBS)
            rho0=np.einsum('qic,qjc->ij',a,a.conj());rho1=np.zeros((nmode,nmode),complex);matrixops=[];beforemeans=np.zeros(3);aftermeans=np.zeros(3);fullenergy=0.
            for q,s0 in enumerate(load):
                s=int(s0);q0,q4,q5=bits[[0,4,5],q];vc=b['bare']+.5*q0*b['empty']+ar*q0*np.eye(nmode);vm=vc+((q0-q4)*b['n']+(q0-q5)*np.eye(nmode))/4;ham=b['hs'][s]+ar*popq[q]*np.eye(nmode)
                physicalops=(vc,vm,ham,b['n'],b['I']);proj=b['projected'];vc_mode=proj['bare'][s]+.5*q0*proj['pe'][s]+ar*q0*np.eye(nmode);vm_mode=vc_mode+((q0-q4)*proj['n'][s]+(q0-q5)*np.eye(nmode))/4
                op=[vc_mode,vm_mode,np.diag(ev[s]+ar*popq[q]),proj['n'][s],proj['I'][s]];matrixops.append(op)
                for k in range(3):close('literal parent source coefficients '+label+str((q,k)),v[s].conj().T@physicalops[k]@a[q],coeffs[OPS[k]][q],OP);beforemeans[k]+=float(np.vdot(a[q],physicalops[k]@a[q]).real);aftermeans[k]+=float(np.dot(prob[q],np.diag(op[k]).real))
                rho1+=np.einsum('i,ai,bi->ab',prob[q],v[s],v[s].conj());fullenergy+=float(np.dot(prob[q],ev[s]+ar*popq[q]))
            close('carrier-edge before '+label,out['carrier_edge_rho_before'],rho0,OBS);close('carrier-edge after '+label,out['carrier_edge_rho_after'],rho1,OBS)
            probe0,probe1=partial_probe(rho0,two),partial_probe(rho1,two);close('probe-edge before '+label,out['probe_edge_rho_before'],probe0,OBS);close('probe-edge after '+label,out['probe_edge_rho_after'],probe1,OBS);probes.append((probe0,probe1))
            close('full H/AR energy '+label,row['complete_network_energy'],fullenergy,EN);close('old complete energy '+label,fullenergy,parentmeta['source_energy_work_vertices']['H'],EN)
            for k in range(3):close('source before/after/change '+label+OPS[k],[row['source_energy_work_vertices'][OPS[k]][x] for x in ('before','after','change')],[beforemeans[k],aftermeans[k],aftermeans[k]-beforemeans[k]],EN if k==2 else OBS)
            exact('owned work/ineligible-clock provenance '+label,row['inherited_network_controller_work']==parentmeta['inherited_network_controller_work'] and row['parent_phase_chart_eligible_global']==parentmeta['parent_phase_chart_eligible_global'] and row['parent_Bplus_rate_global']==parentmeta['parent_Bplus_rate_global'] and row['parent_ideal_clock_structural_null']==parentmeta['parent_ideal_clock_structural_null'])
            beta0=beta_raw(a,ws);beta1=np.zeros(8,complex);dots=np.zeros((3,8),complex);lookup={int(q):i for i,q in enumerate(ws)}
            for node in range(8):
                for lo,qword in enumerate(ws):
                    if int(qword)&(1<<node) or int(qword)+(1<<node) not in lookup:continue
                    hi=lookup[int(qword)+(1<<node)];sl,sh=int(load[lo]),int(load[hi]);same=np.equal(np.asarray(b['ids'][sl])[:,None],np.asarray(b['ids'][sh])[None,:]);ii,jj=np.nonzero(same)
                    if not len(ii):continue
                    coh=np.sum(c[lo,ii]*c[hi,jj].conj(),axis=1);body_overlap=np.einsum('ai,ai->i',v[sh][:,jj].conj(),v[sl][:,ii]);beta1[node]+=2*np.dot(coh,body_overlap)
                    for k in range(3):dots[k,node]+=2j*np.dot(coh,np.diag(matrixops[hi][k])[jj]-np.diag(matrixops[lo][k])[ii])
            close('before dressed clocks '+label,cv(row['before_joint_beta_global']),beta0,OBS);close('complete-root coherent clocks '+label,cv(row['after_joint_beta_global']),beta1,OBS);close('six preserved clocks '+label,beta1[list(REST)],beta0[list(REST)],OBS);close('endpoints annihilated '+label,beta1[[0,4]],0.,0.);betas.append(beta1)
            for k in range(3):close('literal projected clock source '+label+OPS[k],cv(row['after_local_source_clock_dot'][OPS[k]]),dots[k],OBS)
            close('full AR clock derivative '+label,cv(row['after_joint_beta_dot_global']),1j*ar*beta1,OBS);close('endpoint clock changes '+label,cv(row['endpoint_clock_change']),beta1[[0,4]]-beta0[[0,4]],OBS)
            exact('clock chart/refusal preserved '+label,row['after_phase_chart_eligible_global']==[bool(parentmeta['parent_phase_chart_eligible_global'][k] and not parentmeta['parent_ideal_clock_structural_null'] and k in REST and abs(cv(row['after_joint_beta_global'])[k])**2!=0) for k in range(8)] and row['after_phase_rate_raw_global']==[None if abs(cv(row['after_joint_beta_global'])[k])**2==0 else ar for k in range(8)] and row['q_diagonal_only_stationarity'] and not row['full_H_stationary_state_claimed'])
            response=np.zeros((5,5),complex);static=np.zeros((5,5),complex);nearcount=0;phasecontact=float(np.trace(H*b['x']@rho1).real);currentmean=float(np.trace(b['I']@rho1).real)
            for s in range(3):
                energy=ev[s];gap=energy[None,:]-energy[:,None];weight=np.zeros((5,5,nmode,nmode),complex)
                for q in np.flatnonzero(load==s):
                    diff=prob[q][:,None]-prob[q][None,:]
                    for k in range(5):
                        for l in range(5):weight[k,l]+=diff*matrixops[q][k]*matrixops[q][l].T
                iu,ju=np.triu_indices(nmode,1);packed=np.array([weight[k,l,iu,ju] for k,l in PACKED]);prefix='s%d_'%s
                close('literal signed numerator '+label+str(s),out[prefix+'signed_weights_operator_upper'],packed,OBS);close('positive pole gaps '+label+str(s),out[prefix+'native_pole_gap_positive'],gap[iu,ju],0.)
                exact('packed indices/IDs '+label+str(s),out[prefix+'packed_operator_pairs'].tolist()==[list(k) for k in PACKED] and out[prefix+'upper_energy_mode_i'].tolist()==iu.tolist() and out[prefix+'upper_energy_mode_j'].tolist()==ju.tolist() and out[prefix+'mode_exact_root_ID'].tolist()==b['ids'][s])
                close('all exact intervals '+label+str(s),out[prefix+'exact_native_intervals'],b['intervals'][s],0.);close('all numeric modes '+label+str(s),out[prefix+'numerical_native_modes'],energy,0.)
                mask=b['intervals'][s][ju,0]-b['intervals'][s][iu,1]<=BAND;exact('unchanged unresolved mask '+label+str(s),np.array_equal(out[prefix+'unresolved_pair_mask'],mask));nearcount+=int(mask.sum())
                response+=np.sum(weight/(gap-Z)[None,None,:,:],axis=(2,3));den=np.where(np.eye(nmode,dtype=bool),1.,gap);static+=np.sum(weight/den[None,None,:,:],axis=(2,3))
                close('spectral incidence left '+label+str(s),weight[4],-1j*gap[None,:,:]*weight[3],OBS);close('spectral incidence right '+label+str(s),weight[:,4],1j*gap[None,:,:]*weight[:,3],OBS)
            resp=row['response'];close('25 ordered Abel functions '+label,cv(resp['chi_Abel']),response,OBS);close('25 signed static candidates '+label,cv(resp['formal_static_candidate']),static,EN);close('zero-gap numerators '+label,cv(resp['zero_gap_numerators']),0.,0.)
            exact('static disposition preserved '+label,resp['unresolved_energy_pair_count']==nearcount and resp['static_status']==('REFUSED_UNRESOLVED_NEAR_POLES' if nearcount else 'FINITE_STATIONARY_STATIC_NUMERICAL_EVALUATION') and (resp['true_static_numerical_evaluation'] is None)==bool(nearcount) and not resp['thermal_or_passive_adoption'])
            if not nearcount:close('eligible static numerical value '+label,cv(resp['true_static_numerical_evaluation']),static,EN)
            close('complete phase contact '+label,resp['phase_contact_hX_mean'],phasecontact,EN);close('static/current contact Ward '+label,static[4,4],phasecontact,EN);close('readout phase contact '+label,resp['phase_readout_theta_contact'],-phasecontact,EN)
            contacts=row['full_owned_contacts'];close('additive direct contacts '+label,contacts['additive_HNN'],0.,0.);close('theta/theta contact '+label,contacts['H_theta_theta'],phasecontact,EN);close('Ltheta/eta/readout contacts '+label,[contacts['H_Ltheta'],contacts['I_theta_readout_theta_contact'],contacts['I_theta_readout_eta_contact']],[-currentmean,-phasecontact,currentmean/2],EN)
            for k in ('Vc','Vm'):close('mixed source contacts '+label+k,[contacts['fractional_H_Leta'][k],contacts['H_eta_theta'][k]],[aftermeans[OPS.index(k)],-currentmean/2],OBS)
            if reset:close('reset source allocation response '+label,response[0],response[1],OBS);close('reset transposed allocation response '+label,response[:,0],response[:,1],OBS);close('conserved reset work '+label,aftermeans[0]-aftermeans[1],float(bits[5]@mass)/4,OBS)
            close('stationary uniform energy kernels '+label,np.r_[response[2],response[:,2]],0.,EN)
            residual=b['hs']@b['v']-b['v']*b['ev'][:,None,:];rnorm=np.sqrt(np.sum(abs(residual)**2,axis=1));vnorm=np.sqrt(np.sum(abs(b['v'])**2,axis=1));bound=float(2*np.sum(prob*rnorm[load]*vnorm[load]));close('weighted coherent Hrel bound '+label,row['relative_density_commutator_trace_norm_upper_estimate'],bound,OP)
            exact('projector metric provenance '+label,row['body_projector_numerical_witnesses']==basemeta['projector_metrics'][sector]);ab.append(response);st.append(static);summaries.append({'preparation':name,'channel':label,'near_pairs':nearcount,'static_status':resp['static_status'],'network_energy':fullenergy,'chi_cc_Abel':response[0,0],'chi_mm_Abel':response[1,1]})
        for key,value in contrasts(ab).items():close('all signed Abel contrasts '+name+key,cv(prep['signed_Abel_four_channel_contrasts'][key]),value,OBS)
        for key,value in contrasts(st).items():close('all signed static contrasts '+name+key,cv(prep['formal_static_four_channel_contrasts'][key]),value,EN)
        eligible=all(q['response']['true_static_numerical_evaluation'] is not None for q in prep['channels']);exact('static contrast refusal '+name,(prep['true_static_four_channel_contrasts'] is not None)==eligible)
        if eligible:
            for key,value in contrasts(st).items():close('eligible four-channel static '+name+key,cv(prep['true_static_four_channel_contrasts'][key]),value,EN)
        for k in range(1,4):close('initial isolation marginal '+name+str(k),probes[k][0],probes[0][0],OBS);close('all six common clock envelopes '+name+str(k),betas[k][list(REST)],betas[0][list(REST)],OBS)
        marginal={'retained_on_minus_reference':probes[0][1]-probes[1][1],'transferred_on_minus_reference':probes[2][1]-probes[3][1],'difference_of_differences':probes[0][1]-probes[1][1]-probes[2][1]+probes[3][1]}
        for key,value in marginal.items():close('post-control matching changes '+name+key,cv(prep['post_control_probe_edge_marginal_differences'][key]),value,OBS)
        exact('no false post-control matching '+name,not prep['old_initial_isolation_marginal_reasserted'])
        dispositions={q['channel']:{'status':q['response']['static_status'],'unresolved_pair_count':q['response']['unresolved_energy_pair_count'],'parent_clock_eligibility':q['parent_phase_chart_eligible_global'],'parent_structural_clock_null':q['parent_ideal_clock_structural_null']} for q in prep['channels']};exact('all inherited dispositions '+name,prep['inherited_row_refusal_dispositions']==dispositions)
        if prep['formation_gamma_rational']=='0':close('gamma0 retained/reset on '+name,ab[0],ab[2],OBS);close('gamma0 retained/reset reference '+name,ab[1],ab[3],OBS)
    exact('audited all 416 controls',len(summaries)==416)
    for k,h in INPUTS.items():exact('after seal '+k,sha(path(k))==h)
    result={'audit_status':'PASS','failed_assertions':0,'assertions':ASSERTIONS,'checks':len(CHECKS),'maximum_absolute_comparison_residual':MAXERR,'source_sha256':sha(__file__),'result_raw_sha256':r['result_raw_sha256'],'receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'input_sha256':INPUTS,'PID':os.getpid(),'elapsed_seconds':time.monotonic()-start,'audited_preparations':104,'audited_controls':416,'operator_pairs_per_control':25,'tolerances':{'operator':OP,'observable':OBS,'energy':EN,'static_unresolved_band':BAND},'scope':'Acceptance of saved numerical method and custody only. Exact root labels do not certify near-pole eigenvector or response accuracy; static outputs remain nondirected candidates. Separate exact-S/R projected-vector conditioning diagnostic neither deletes odd modes nor modifies these results. No thermal/passive/metric or natural-relaxation claim.','controls':summaries,'checks_detail':CHECKS}
    rh=write(OUT,result)
    with MD.open('x') as f:f.write('# Relative-energy saved acceptance audit\n\nPASS: all 104 preparations, 416 age-zero controls and 25 signed functions per control. Independent raw-state mode projections, literal source/readout contractions, full ordered pole sums, q/app root coherence, six formed clocks, energies/work, contacts, marginals and all contrasts agree at frozen criteria.\n\nStatic numbers remain nondirected numerical candidates; exact root IDs do not earn near-pole vector accuracy. The separate symmetry diagnostic retains every original mode and refusal. No eigensolver, H reconstruction, evolution, producer import or RNG replay was used.\n\nAssertions: %d. Maximum absolute comparison residual: %.12g. Result SHA256: %s. Audit SHA256: %s.\n'%(ASSERTIONS,MAXERR,r['result_raw_sha256'],rh));f.flush();os.fsync(f.fileno())
    for k,h in INPUTS.items():
        if sha(path(k))!=h:raise AssertionError('post-output input changed '+k)
    rr=write(RECEIPT,{'audit_status':'PASS','audit_sha256':rh,'report_sha256':sha(MD),'source_sha256':sha(__file__),'input_sha256':INPUTS,'result_raw_sha256':r['result_raw_sha256'],'parent_receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'assertions':ASSERTIONS,'PID':os.getpid()});print(json.dumps({'status':'PASS','assertions':ASSERTIONS,'audit_sha256':rh,'receipt_sha256':rr}),flush=True)
if __name__=='__main__':
    try:main()
    except Exception as exc:
        if STARTED and not ERROR.exists():write(ERROR,{'audit_status':'FAILED_PRESERVED','error':repr(exc),'traceback':traceback.format_exc(),'active':ACTIVE,'source_sha256':sha(__file__),'input_sha256':INPUTS,'assertions_reached':ASSERTIONS,'checks':CHECKS})
        print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
