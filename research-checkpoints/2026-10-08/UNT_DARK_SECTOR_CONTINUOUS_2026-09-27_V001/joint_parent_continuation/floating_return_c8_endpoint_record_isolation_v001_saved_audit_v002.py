import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import ast,json,hashlib,math,sys,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory');J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001';PN='FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001'
CP=J/'floating_return_c8_endpoint_record_isolation_v001_checkpoints';PCP=J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints'
AJSON=J/(NAME+'_AUDIT.json');AMD=J/(NAME+'_AUDIT.md');AERROR=J/(NAME+'_AUDIT_ERROR_V002.json')
GUARD_PINS={'/private/tmp/unt_endpoint_saved_audit_20261005_v001.py':'75ec2fc3c8defa5deff37fe0eb129b64d3af58aca12846f513df7fb3c7741141',str(J/(NAME+'_AUDIT_ERROR_V001.json')):'45181faad5af7c5521add06cba065e65cbfbcdf449272d68045e040431ced6e5'}
SOURCE=J/'floating_return_c8_endpoint_record_isolation_v001.py';PROTO=J/(NAME+'.md')
N=0;FAIL=[];MAX={};ACTIVE=None;INITIAL={};START=time.monotonic()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def blob(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def ck(label,ok):
 global N
 N+=1
 if not bool(ok):FAIL.append({'name':label})
def close(label,a,b,tol=1e-9):
 global N
 N+=1;a,b=np.asarray(a),np.asarray(b);finite=np.isfinite(a).all() and np.isfinite(b).all()
 error=float(np.max(abs(a-b))) if finite and a.size else (0. if finite else math.inf)
 group=label.split(':')[-1];MAX[group]=max(MAX.get(group,0.),error)
 if not finite or error>tol:FAIL.append({'name':label,'error':repr(error),'tolerance':tol})
def dec(v):
 a=np.asarray(v,dtype=float);return a[...,0]+1j*a[...,1]
def nullclose(label,a,b,tol=1e-9):
 ck(label+'_none',(a is None)==(b is None))
 if a is not None and b is not None:close(label,a,b,tol)
def rate(b,d):return None if abs(b)**2==0 else float(np.imag(np.conj(b)*d)/abs(b)**2)
def write(p,v):
 with p.open('x') as f:json.dump(v,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def safe(v):
 if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)):return [safe(x) for x in v]
 if isinstance(v,float) and not math.isfinite(v):return {'nonfinite':repr(v)}
 return v
def packet(name,cp,count):
 r,rec=read(J/(name+'_RESULT.json')),read(J/(name+'_RECEIPT.json'))
 for suffix in ('_RESULT.json','_RESULT.md','_RECEIPT.json'):INITIAL[str((J/(name+suffix)).relative_to(ROOT))]=sha(J/(name+suffix))
 ck(name+':raw',rec['result_raw_sha256']==sha(J/(name+'_RESULT.json')));ck(name+':canonical',rec['result_canonical_sha256']==hashlib.sha256(blob(r)).hexdigest())
 ck(name+':report',rec['report_sha256']==sha(J/(name+'_RESULT.md')));ck(name+':inputmap',rec['input_sha256']==r['input_sha256'])
 for f,h in rec['input_sha256'].items():ck(name+':input_'+f,sha(ROOT/f)==h);INITIAL[f]=h
 cm=rec['checkpoint_sha256'];ck(name+':1146cp',len(cm)==1146 and set(cm)=={p.name for p in cp.iterdir() if p.name!='journal.jsonl'})
 for f,h in cm.items():ck(name+':cp_'+f,sha(cp/f)==h);INITIAL[str((cp/f).relative_to(ROOT))]=h
 jb=(cp/'journal.jsonl').read_bytes();es=[json.loads(x) for x in jb.splitlines()];INITIAL[str((cp/'journal.jsonl').relative_to(ROOT))]=sha(cp/'journal.jsonl')
 ck(name+':1149events',len(es)==1149);ck(name+':prefix',rec['journal_prefix_sha256']==hashlib.sha256(b'\n'.join(jb.splitlines()[:-1])+b'\n').hexdigest())
 ck(name+':receiptcommit',es[-1]=={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))});ck(name+':reportcommit',es[-2]=={'event':'report_saved','sha256':rec['report_sha256'],'paired_data_rows':416})
 ck(name+':resultcommit',es[-3]=={'event':'result_saved','raw_sha256':rec['result_raw_sha256'],'canonical_sha256':rec['result_canonical_sha256']})
 m=read(cp/'manifest.json');ck(name+':manifest',es[0]['manifest_sha256']==sha(cp/'manifest.json')==r['manifest_sha256'] and m['input_sha256']==es[0]['input_sha256']==rec['input_sha256'])
 ck(name+':PID',m['PID']==es[0]['PID']==r['original_manifest_PID']==rec['original_manifest_PID'])
 commits={'manifest.json':sha(cp/'manifest.json')}
 for e in es[1:-3]:
  ck(name+':uniquecommit',e['file'] not in commits);commits[e['file']]=e['sha256']
 ck(name+':allcommits',commits==cm);ck(name+':controls',r['passed']==rec['passed']==len(r['checks'])==count and r['failed']==rec['failed']==0 and all(c['passed'] for c in r['checks']))
 ck(name+':reportrows',sum(x.startswith('|case') for x in (J/(name+'_RESULT.md')).read_text().splitlines())==416)
 return r,rec
REST=(1,2,3,5,6,7);RW=np.arange(64);GW=np.array([sum(((int(r)>>k)&1)<<v for k,v in enumerate(REST)) for r in RW]);RB=((GW[None,:]>>np.arange(8)[:,None])&1).astype(int)
OW=np.arange(256);OB=((OW[None,:]>>np.arange(8)[:,None])&1).astype(int);ETA=np.array([1,1,1,1,-1,-1,-1,-1]);KW=ETA@RB
EL=np.array([(c&1,c>>1) for c in range(4)],dtype=int);EP=EL.sum(1);EK=EL[:,0]-EL[:,1]
CYCLE=np.array([0,4,3,7,2,6,1,5]);EDGES=[(int(CYCLE[k]),int(CYCLE[(k+1)%8])) for k in range(8)]
PAIRS=np.array([(a,b) for a in range(8) for b in range(8) if a!=b]);INDEX={tuple(p):i for i,p in enumerate(PAIRS)}
OCC=np.array([((PAIRS[:,0]==v).astype(int)+(PAIRS[:,1]==v).astype(int)) for v in range(8)],dtype=int)
POS=np.argsort(CYCLE);DIST=np.array([min(abs(int(POS[a])-int(POS[b])),8-abs(int(POS[a])-int(POS[b]))) for a,b in PAIRS]);ADJ=(DIST==1).astype(int)
TRANS=[[(np.array([INDEX[(u,b)] for b in range(8) if b not in (u,v)]),np.array([INDEX[(v,b)] for b in range(8) if b not in (u,v)])),
        (np.array([INDEX[(a,u)] for a in range(8) if a not in (u,v)]),np.array([INDEX[(a,v)] for a in range(8) if a not in (u,v)]))] for u,v in EDGES]
h=.2;t=.1;j=.25;lam=.5
def ham(a,ar,two):
 nc=2 if two else 1;out=(8+nc+ar*RB.sum(0))[:,None,None,None]*a
 out[:,0]+=2*a[:,0]
 for k,(u,v) in enumerate(EDGES):
  bits=[1] if k==0 else [0,1]
  cd=OCC[u]+OCC[v]-2*OCC[u]*OCC[v] if two else np.eye(8,dtype=int)[u]+np.eye(8,dtype=int)[v]
  for bit in bits:
   out[:,bit]+=j*cd[None,:,None]*a[:,bit]
   tr=TRANS[k] if two else [(np.array([u]),np.array([v]))]
   for left,right in tr:out[:,bit,left]-=t*a[:,bit,right];out[:,bit,right]-=t*a[:,bit,left]
 out-=h*a[:,::-1];return out
def density(a,two):
 if two:
  z=np.zeros((a.shape[0],2,8,8,a.shape[-1]),complex);z[:,:,PAIRS[:,0],PAIRS[:,1],:]=a
  return np.einsum('qeabc,qedbc->ad',z,z.conj()),np.einsum('qeabc,qeafc->bf',z,z.conj())
 return None,np.einsum('qebc,qefc->bf',a,a.conj())
def carrieredge(a):
 z=a.reshape(a.shape[0],-1,a.shape[-1]);return np.einsum('qic,qjc->ij',z,z.conj())
def audit_obs(a,o,ar,two,label,initialbp,x,expected,initialjoint):
 ad=-1j*ham(a,ar,two);prob=np.sum(abs(a)**2,3);pd=2*np.real(np.sum(a.conj()*ad,3));qp=prob.sum((1,2));qpd=pd.sum((1,2));norm=qp.sum();nd=qpd.sum()
 q=RB@qp;qq=(RB*qp[None,:])@RB.T;qd=RB@qpd;empty=prob[:,0].sum();emptyd=pd[:,0].sum();rs,rp=density(a,two)
 vals={'norm':norm,'record_word_probability':qp,'record_q_global':q,'record_qq_global':qq,'empty_edge_probability':empty,'empty_edge_dot':emptyd,'probe_p_global':np.diag(rp).real}
 for key,v in vals.items():close(label+':'+key,v,o[key])
 close(label+':exactnorm',norm,1);close(label+':qconservation',qpd,0);close(label+':probe_density',rp,dec(o['probe_density_global']))
 close(label+':endpointsblank',q[[0,4]],0);close(label+':returndistribution',[qp[KW==-k].sum() for k in range(-4,5)],o['return_charge_number_probability'])
 if two:close(label+':source_density',rs,dec(o['source_density_global']));close(label+':source_p',np.diag(rs).real,o['source_p_global'])
 ec=np.vdot(a[:,1],a[:,0]);ed=np.vdot(ad[:,1],a[:,0])+np.vdot(a[:,1],ad[:,0]);ex,ey,ez=2*ec.real,-2*ec.imag,2*empty-norm
 for k,v in zip(('X','Y','Z'),(ex,ey,ez)):close(label+':incidence'+k,v,o['incidence_Pauli'][k])
 for k,v in zip(('X','Y','Z'),(2*ed.real,-2*ed.imag,2*emptyd-nd)):close(label+':incidence_dot'+k,v,o['incidence_Pauli_dot'][k])
 close(label+':incidencecontinuity',emptyd,-h*ey)
 currents=[[],[]];divs=[np.zeros(8),np.zeros(8)];hops=0;curr=0;cross=0;actualadj=0
 for k,(u,v) in enumerate(EDGES):
  bits=[1] if k==0 else [0,1]
  for tag in ([0,1] if two else [1]):
   if two:l,r=TRANS[k][tag];cr=sum(np.vdot(a[:,bit,l],a[:,bit,r]) for bit in bits)
   else:cr=sum(np.vdot(a[:,bit,u],a[:,bit,v]) for bit in bits)
   cu=2*t*cr.imag;currents[tag].append(cu);divs[tag][u]-=cu;divs[tag][v]+=cu;hops+=2*cr.real
  if two:
   ps=OCC[u]+OCC[v];pb=OCC[u]*OCC[v]
   for bit in bits:pp=prob[:,bit].sum(0);curr+=j*float(ps@pp);cross-=2*j*float(pb@pp);actualadj+=float(pb@pp)
  else:curr+=j*sum(float(prob[:,bit,[u,v]].sum()) for bit in bits)
 for tag,key in [(1,'probe')]+([(0,'source')] if two else []):
  close(label+':'+key+'currents',currents[tag],o[key+'_edge_current_cycle']);close(label+':'+key+'divergence',divs[tag],o[key+'_current_divergence'])
  dd=np.bincount(PAIRS[:,tag],weights=pd.sum((0,1)),minlength=8) if two else pd.sum((0,1));close(label+':'+key+'dot',dd,o[key+'_p_dot_global']);close(label+':'+key+'continuity',dd,divs[tag])
 bp=np.zeros(8,complex);bd=np.zeros(8,complex);eb=np.zeros(8,complex)
 for k,v in enumerate(REST):
  lo=RW[(RW&(1<<k))==0];hi=lo|(1<<k);bp[v]=2*np.vdot(a[hi],a[lo]);bd[v]=2*(np.vdot(ad[hi],a[lo])+np.vdot(a[hi],ad[lo]));eb[v]=2*np.vdot(a[hi,0],a[lo,0])
 old=norm-2*q+1j*bp.imag;oldd=nd-2*qd+1j*bd.imag
 for key,v in [('Bplus_beta_global',bp),('Bplus_dot_global',bd),('empty_joint_Bplus_global',eb),('Bplus_dot_charging',1j*ar*bp),('Bplus_dot_endpoint_feedback',np.zeros(8,complex)),('original_Z_minus_iY_beta_global',old),('original_Z_minus_iY_dot_global',oldd)]:close(label+':'+key,v,dec(o[key]),5e-10)
 for kind,seq in [('record_Pauli_global',(bp.real,-bp.imag,norm-2*q)),('record_Pauli_dot_global',(bd.real,-bd.imag,nd-2*qd))]:
  for key,v in zip(('X','Y','Z'),seq):close(label+':'+kind+key,v,o[kind][key])
 close(label+':clockamplitude',abs(bp),o['Bplus_amplitude_global']);close(label+':sixphase',bp[list(REST)],initialbp[list(REST)]*np.exp(1j*ar*x),5e-10)
 for v in range(8):nullclose(label+':Bplusrate',rate(bp[v],bd[v]),o['Bplus_rate_global'][v]);nullclose(label+':originalrate',rate(old[v],oldd[v]),o['original_Z_minus_iY_rate_global'][v])
 close(label+':bareX',o['bare_return_traced_X_global'],0,0);close(label+':bareY',o['bare_return_traced_Y_global'],0,0)
 fields={'field_self_energy':8*norm,'carrier_storage_energy':(2 if two else 1)*norm,'retained_record_charging_energy':ar*float(RB.sum(0)@qp),'degree_defect_energy':2*empty,'record_feedback_change_energy':0.,'current_onebody_energy':curr,'direct_current_cross_energy':cross,'actual_occupied_hopping_energy':-t*hops,'incidence_flip_energy':-h*ex}
 for key,v in fields.items():close(label+':'+key,v,o[key],1e-8)
 energy=sum(fields.values());close(label+':fullenergy',energy,o['full_energy'],1e-8);close(label+':energyconserved',energy,expected,1e-8);close(label+':literalHenergy',np.vdot(a,1j*ad).real,energy,1e-8)
 shape=a.reshape(64,2,a.shape[2],4,a.shape[-1]//4);ap=np.sum(abs(shape)**2,4);joint=ap.sum((1,2));close(label+':apparatus_joint',joint,o['apparatus_endpoint_joint_probability']);close(label+':apparatusconserved',joint,initialjoint)
 close(label+':app_pop',joint.sum(0)@EP,o['transferred_endpoint_pop']);close(label+':app_signed',joint.sum(0)@EK,o['transferred_record_signed_charge_number']);close(label+':app_return',-joint.sum(0)@EK,o['transferred_return_charge_number'])
 close(label+':app_returnhist',[joint[:,EK==-k].sum() for k in range(-1,2)],o['apparatus_return_charge_number_probability'])
 for c,(qa,qb) in enumerate(EL):
  z=o['transferred_endpoint_conditioning'][c];weight=joint[:,c].sum();jp=ap[:,0,:,c].sum();pos=ap[:,:,:,c].sum((0,1));emp=ap[:,0,:,c].sum(0)
  ck(label+':app_labels',z['apparatus_label']==c and z['original_q0']==qa and z['original_q4']==qb);close(label+':app_weight',weight,z['weight']);close(label+':app_empty',jp,z['empty_joint']);close(label+':app_pos',pos,z['position_joint_probability']);close(label+':app_emptypos',emp,z['empty_position_joint_probability'])
  nullclose(label+':app_cond',None if weight==0 else jp/weight,z['empty_conditional'])
  ck(label+':app_pos_none',(z['position_conditional_probability'] is None)==(weight==0))
  if weight!=0:close(label+':app_pos_cond',pos/weight,z['position_conditional_probability'])
  if two:
   close(label+':app_adj',ADJ@pos,z['tagged_reference_adjacency_joint']);close(label+':app_dist',DIST@pos,z['tagged_reference_separation_joint']);nullclose(label+':app_adjcond',None if weight==0 else ADJ@pos/weight,z['tagged_reference_adjacency_conditional']);nullclose(label+':app_distcond',None if weight==0 else DIST@pos/weight,z['tagged_reference_separation_conditional'])
 for si,(qa,qb) in enumerate(((0,0),(0,1),(1,0),(1,1))):
  z=o['network_endpoint_record_conditioning'][si];sel=(RB[0]==qa)&(RB[4]==qb);w=qp[sel].sum();jp=prob[sel,0].sum();pos=prob[sel].sum((0,1));epos=prob[sel,0].sum(0)
  ck(label+':networklabels',z['q0']==qa and z['q4']==qb);close(label+':networkweight',w,z['weight']);close(label+':networkempty',jp,z['empty_joint']);close(label+':networkpos',pos,z['position_joint_probability']);close(label+':networkemptypos',epos,z['empty_position_joint_probability']);nullclose(label+':networkcond',None if w==0 else jp/w,z['empty_conditional'])
 pos=prob.sum((0,1))
 if two:
  close(label+':pairprob',pos,o['ordered_pair_probability']);close(label+':pairdist',[pos[DIST==d].sum() for d in range(5)],o['tagged_cycle_reference_separation_probability']);close(label+':pairmean',DIST@pos,o['tagged_cycle_reference_mean_separation']);close(label+':pairadj',ADJ@pos,o['tagged_cycle_reference_adjacency']);close(label+':occupiedadj',actualadj,o['actual_occupied_pair_adjacency'])
  close(label+':empty_pair',prob[:,0].sum(0),o['empty_joint_ordered_pair_probability']);close(label+':empty_source',np.bincount(PAIRS[:,0],weights=prob[:,0].sum(0),minlength=8),o['empty_joint_source_probability']);close(label+':empty_probe',np.bincount(PAIRS[:,1],weights=prob[:,0].sum(0),minlength=8),o['empty_joint_probe_probability'])
 else:
  app=np.sum(abs(a.reshape(64,2,8,4,8,8))**2,axis=(0,1,3,5)).T;di=np.array([[min(abs(int(POS[u])-int(POS[v])),8-abs(int(POS[u])-int(POS[v]))) for v in range(8)] for u in range(8)])
  close(label+':markerjoint',app,o['apparatus_position_probe_joint_probability']);close(label+':markerdist',[app[di==d].sum() for d in range(5)],o['apparatus_marker_reference_separation_probability']);close(label+':markermean',np.sum(di*app),o['apparatus_marker_reference_mean_separation'])
 return {'probe_p_global':np.diag(rp).real,'probe_density_global':rp,'probe_edge_current_cycle':np.array(currents[1]),'empty_edge_probability':empty},bp

def main():
 global ACTIVE
 if sys.argv[1:]!=['--execute']:raise RuntimeError('exact --execute required')
 if any(p.exists() for p in (AJSON,AMD,AERROR)):raise RuntimeError('preserve existing audit output/error')
 for f,hsh in GUARD_PINS.items():ck('preserved_guard_attempt:'+f,sha(Path(f))==hsh)
 guard_error=read(J/(NAME+'_AUDIT_ERROR_V001.json'));ck('guard_attempt_zero_assertions',guard_error['assertions']==0 and guard_error['active'] is None and guard_error['error']=="RuntimeError('exact --execute required')" and guard_error['failures']==[] and guard_error['input_sha256']=={})
 ck('source',sha(SOURCE)=='d030200d5f6924b0576623c3ac667dff28991243e3ab6fbec2704e263a83c147');ck('protocol',sha(PROTO)=='123e780366ce78bc6abeb8f26ce707ff30f852857e78909cbe24400269fe9ca2')
 ck('new_raw_pin',sha(J/(NAME+'_RESULT.json'))=='e963da6e5cdf2e2e551821475c318201870c56943bb6e1bb07a8bfa1bb5a1c7c');ck('new_receipt_pin',sha(J/(NAME+'_RECEIPT.json'))=='f1461f28512a0a978632f5eeb6764af69fb451816ab165f8d9e168f4a5ac22e8')
 env={}
 def val(n):
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Name):return env[n.id]
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return val(n.left)+val(n.right)
  if isinstance(n,ast.Dict):return {val(k):val(v) for k,v in zip(n.keys,n.values)}
  raise ValueError('literal metadata only')
 for n in ast.parse(SOURCE.read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('NAME','PARENT','PINS'):env[n.targets[0].id]=val(n.value)
 for f,hsh in env['PINS'].items():ck('direct_'+f,sha(J/f)==hsh);INITIAL[str((J/f).relative_to(ROOT))]=hsh
 r,rec=packet(NAME,CP,24473);pr,prec=packet(PN,PCP,14830)
 ck('104preps',len(r['preparations'])==len(pr['preparations'])==104)
 ck('unique_preparation_census',{p['preparation'] for p in r['preparations']}=={f'case{c:02d}_prep{i:02d}' for c in range(8) for i in range(13)})
 with np.load(CP/'reused_eigensystems.npz',allow_pickle=False) as z:
  be,bv,re,rv=z['tagged_base_eigenvalues'],z['tagged_base_eigenvectors'],z['reference_base_eigenvalues'],z['reference_base_eigenvectors'];bm,rm=z['tagged_base_matrices'],z['reference_base_matrices']
  close('restwords',z['rest_global_words'],GW,0);close('networkbits',z['network_global_record_bits'],RB,0);close('apparatuslabels',z['apparatus_endpoint_bits'],EL,0)
  em=json.loads(str(z['metadata_json']));ck('no_new_solver',em['new_eigensolver_calls']==0 and em['input_sha256']==r['input_sha256'])
 for e,v,m in [(be,bv,bm),(re,rv,rm)]:close('saved_basis:orthogonal',v.conj().T@v,np.eye(len(e)),5e-10);close('saved_basis:eigenresidual',m@v,v*e,5e-10)
 total=0;stats=[]
 for pi,p in enumerate(r['preparations']):
  ACTIVE=p['preparation'];name=p['preparation'];old=pr['preparations'][pi];ck(name+':identity',name==old['preparation']);ck(name+':complete',read(CP/(name+'_complete.json'))==p)
  ck(name+':matched_preparation_metadata',all(p[k]==old[k] for k in ('case','preparation_time_index','preparation_x_rational','AR_rational','formation_gamma_rational')))
  ck(name+':ordered_preparation_census',p['case']==f'case{pi//13:02d}' and p['preparation_time_index']==pi%13 and name==f"{p['case']}_prep{pi%13:02d}")
  ck(name+':four_rows',len(p['rows'])==len(old['rows'])==4)
  im=read(CP/(name+'_initial.json'));ck(name+':initialseal',im['initial_state_sha256']==p['initial_state_sha256']==sha(CP/(name+'_initial.npz')))
  ar=float(p['AR_rational'].split('/')[0])/float(p['AR_rational'].split('/')[1]) if '/' in p['AR_rational'] else float(p['AR_rational'])
  with np.load(CP/(name+'_initial.npz'),allow_pickle=False) as z:a0=z['psi_tagged_initial'];b0=z['psi_reference_initial'];co=z['tagged_spectral_coefficients'];cr=z['reference_spectral_coefficients'];ck(name+':initialmeta',json.loads(str(z['metadata_json']))==im['npz_metadata'])
  with np.load(PCP/(name+'_initial.npz'),allow_pickle=False) as z:oa=z['psi_tagged_initial'];ob=z['psi_reference_initial']
  for c,(qa,qb) in enumerate(EL):
   qs=GW+int(qa)+(int(qb)<<4);close(name+':on_transfer',a0[:,:,:,c*8:(c+1)*8],oa[qs],0);close(name+':ref_transfer',b0[:,:,:,c*64:(c+1)*64],ob[qs],0)
  close(name+':on_initialcarrieredge',carrieredge(a0),carrieredge(oa));close(name+':ref_initialcarrieredge',carrieredge(b0),carrieredge(ob))
  ex=np.zeros((64,2,8,8,4,8),complex);ex[:,:,PAIRS[:,0],PAIRS[:,1],:,:]=a0.reshape(64,2,56,4,8)
  close(name+':transfer_trace_commutes',b0.reshape(64,2,8,4,8,8),np.transpose(ex,(0,1,3,4,2,5)))
  joint=np.sum(abs(a0.reshape(64,2,56,4,8))**2,axis=(1,2,4));close(name+':initialjoint',joint,im['rest_apparatus_joint_probability']);pop=joint.sum(0)@EP
  close(name+':reset_on',p['initial_tagged_energy']-old['initial_tagged_energy'],-ar*pop,1e-8);close(name+':reset_ref',p['initial_reference_energy']-old['initial_reference_energy'],-ar*pop,1e-8)
  close(name+':reset_work_tagged',p['network_reset_work_tagged'],-ar*pop,1e-8);close(name+':reset_work_reference',p['network_reset_work_reference'],-ar*pop,1e-8)
  for k in ('copy_off_work','insertion_work','source_removal_reference_work'):close(name+':'+k,p[k],old[k],0)
  initialbp=dec(im['initial_clock_Bplus_global']);close(name+':clock_transfer',initialbp[list(REST)],dec(read(PCP/(name+'_initial.json'))['initial_clock_Bplus_global'])[list(REST)],5e-10)
  for ri,row in enumerate(p['rows']):
   ACTIVE=name+'/'+str(ri);total+=1;lab=ACTIVE;ck(lab+':rowJSON',read(CP/row['row_file'])==row);ck(lab+':stateSHA',sha(CP/row['state_file'])==row['state_sha256'])
   oldrow=old['rows'][ri]
   ck(lab+':matched_row_metadata',all(row[k]==p[k]==oldrow[k] for k in ('case','preparation','preparation_time_index','preparation_x_rational','AR_rational','formation_gamma_rational')))
   ck(lab+':fixed_forward_census',row['forward_time_index']==oldrow['forward_time_index']==ri and row['x_rational']==oldrow['x_rational']==('0','1/5','2','8')[ri])
   ck(lab+':retained_parent_state_pin',row['retained_parent_state_sha256']==oldrow['state_sha256']==sha(PCP/oldrow['state_file']))
   with np.load(CP/row['state_file'],allow_pickle=False) as z:a=z['psi_tagged'];b=z['psi_reference'];nm=json.loads(str(z['metadata_json']))
   ck(lab+':metadata',nm=={k:row[k] for k in nm});ck(lab+':shapes',a.shape==(64,2,56,32) and b.shape==(64,2,8,256))
   x=float(row['x_rational'].split('/')[0])/float(row['x_rational'].split('/')[1]) if '/' in row['x_rational'] else float(row['x_rational'])
   for aa,init,coeff,vec,ev,dim in [(a,a0,co,bv,be,56),(b,b0,cr,rv,re,8)]:
    z=np.einsum('ij,qjc->qic',vec.conj().T,aa.reshape(64,2*dim,aa.shape[-1]));close(lab+':saved_spectral_phase',z*np.exp(1j*(ev[None,:]+ar*RB.sum(0)[:,None])*x)[:,:,None],coeff,5e-10)
    close(lab+':Gram',aa.reshape(-1,aa.shape[-1]).conj().T@aa.reshape(-1,aa.shape[-1]),init.reshape(-1,init.shape[-1]).conj().T@init.reshape(-1,init.shape[-1]))
   av,abp=audit_obs(a,row['tagged_reset'],ar,True,lab+'/on',initialbp,x,p['initial_tagged_energy'],joint);bv_,bbp=audit_obs(b,row['paired_reference_reset'],ar,False,lab+'/ref',initialbp,x,p['initial_reference_energy'],joint)
   with np.load(PCP/oldrow['state_file'],allow_pickle=False) as z:oa=z['psi_tagged'];ob=z['psi_reference']
   def oldvalues(z,two,o):
    rs,rp=density(z,two);cross=np.vdot(z[:,1],z[:,0]);cu=[]
    for k,(u,v) in enumerate(EDGES):
     bits=[1] if k==0 else [0,1]
     if two:lft,rgt=TRANS[k][1];w=sum(np.vdot(z[:,bit,lft],z[:,bit,rgt]) for bit in bits)
     else:w=sum(np.vdot(z[:,bit,u],z[:,bit,v]) for bit in bits)
     cu.append(2*t*w.imag)
    v={'probe_p_global':np.diag(rp).real,'probe_density_global':rp,'probe_edge_current_cycle':np.array(cu),'empty_edge_probability':np.sum(abs(z[:,0])**2)}
    for key,value in v.items():close(lab+':parent_'+key,value,dec(o[key]) if key=='probe_density_global' else o[key])
    return v
   ov=oldvalues(oa,True,oldrow['tagged']);rv_=oldvalues(ob,False,oldrow['paired_reference'])
   for k in av:
    vals={'source_presence_difference_reset':av[k]-bv_[k],'source_presence_difference_retained':ov[k]-rv_[k],'retained_minus_reset_tagged':ov[k]-av[k],'retained_minus_reset_reference':rv_[k]-bv_[k],
      'record_isolation_difference_of_differences':(ov[k]-rv_[k])-(av[k]-bv_[k])}
    for key,v in vals.items():close(lab+':'+key+'_'+k,v,dec(row[key][k]) if k=='probe_density_global' else row[key][k])
   for bp_,oldobs in [(abp,oldrow['tagged']),(bbp,oldrow['paired_reference'])]:close(lab+':six_common_vs_retained',bp_[list(REST)],dec(oldobs['Bplus_beta_global'])[list(REST)],5e-10)
   dd=(ov['probe_density_global']-rv_['probe_density_global'])-(av['probe_density_global']-bv_['probe_density_global'])
   stats.append({'preparation':name,'forward_time_index':ri,'AR':p['AR_rational'],'gamma':p['formation_gamma_rational'],'preparation_time_index':p['preparation_time_index'],
     'record_DD_probe_density_norm':float(np.linalg.norm(dd)),'record_DD_empty':float((ov['empty_edge_probability']-rv_['empty_edge_probability'])-(av['empty_edge_probability']-bv_['empty_edge_probability']))})
  if pi%13==12:print(json.dumps({'preparations':pi+1,'pairedframes':total,'assertions':N,'failed':len(FAIL)}),flush=True)
 ck('all416pairs',total==416)
 for f,hsh in INITIAL.items():ck('unchanged:'+f,sha(ROOT/f)==hsh)
 for f,hsh in GUARD_PINS.items():ck('unchanged_guard_attempt:'+f,sha(Path(f))==hsh)
 out={'audit_status':'PASS' if not FAIL else 'FAILED','assertions':N,'failed_assertions':len(FAIL),'failures':FAIL,'maximum_absolute_errors':safe(MAX),'audited_preparations':104,
   'audited_reset_tagged_frames':416,'audited_reset_reference_frames':416,'retained_parent_pairs':416,'result_raw_sha256':rec['result_raw_sha256'],'receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),
   'input_sha256':INITIAL,'preserved_guard_attempt':{'source_and_error_sha256':GUARD_PINS,'assertions':0,'reason':'V001 invocation omitted required --execute; guard exited before any contraction.'},'audit_script_sha256':sha(Path(__file__)),'elapsed_seconds':time.monotonic()-START,'signed_readout_rows':stats,
   'method':'Independent saved-state and literal instantaneous native action contractions, all coherence/apparatus labels and four channels; stored spectral-phase identity only. No propagation, eigensolver, producer import, RNG or sampler.'}
 write(AJSON,out)
 lines=['# Independent endpoint-isolation saved-state audit','',out['audit_status']+f': {N:,} assertions, {len(FAIL)} failed; all104 preparations and416 paired reset frames plus416 retained parent pairs.',
  '', 'Full coherent rest/apparatus transfer, current/charge/energy/work, all six held clocks, original query nulls and all signed four-channel differences were checked independently. Spectral phases were inspected without propagating a baseline state. No physical force, metric or calibration is inferred.',
  '', 'Audit JSON SHA256: '+sha(AJSON),'Source result SHA256: '+rec['result_raw_sha256'],'Source receipt SHA256: '+sha(J/(NAME+'_RECEIPT.json'))]
 with AMD.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps({'audit_status':out['audit_status'],'assertions':N,'failed_assertions':len(FAIL),'AUDIT_json_SHA':sha(AJSON),'AUDIT_md_SHA':sha(AMD)}),flush=True)
 if FAIL:print(json.dumps(FAIL[:20]),flush=True);raise SystemExit(3)

if __name__=='__main__':
 try:main()
 except Exception as error:
  if not AERROR.exists():write(AERROR,safe({'error':repr(error),'traceback':traceback.format_exc(),'active':ACTIVE,'assertions':N,'failures':FAIL,'input_sha256':INITIAL,'audit_script_sha256':sha(Path(__file__))}))
  raise
