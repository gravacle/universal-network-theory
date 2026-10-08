#!/usr/bin/env python3
"""Distinct-method authored saved-data acceptance; root alone executes.
Peer-reviewed arithmetic acceptance, not independent authorship/synthesis.
No sampler, old producer import, RNG draw, worldline replay or Hamiltonian job.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
import sys,json,hashlib,math,time,traceback,itertools
from pathlib import Path
import numpy as np
J=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory/UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation')
NAME='LOCAL_RECORD_FEEDBACK_3D_LOCAL_ENERGY_SOURCE_RESPONSE_V001';STEM='local_record_feedback_3d_local_energy_source_response_v001';CP=J/(STEM+'_checkpoints')
PARENT='LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001';PCP=J/'local_record_feedback_3d_pair_coordination_response_v001_checkpoints'
PINS={STEM+'.py':'cc10b0836b9105192e210a5e17d877044fa2a64fa0ba826863bebcb521924167',NAME+'.md':'ed426216edd6788537c3149d0a85c5d26d670ac1d7279a085bdf387435059f58',NAME+'_RESULT.json':'389df141d19e496c5989d114b67025605f248c4b1aad80f145400e2395a5cfca',NAME+'_RECEIPT.json':'7e67d3ce3c2f9f4cb8f76d6f3f69dfad1427dd550a2e99339067051292148e33',PARENT+'_RESULT.json':'74042b5f40401085c151b10b4e32cda5257ca09c86a831f1ef98965abf4649a8',PARENT+'_RECEIPT.json':'36de22839fba41a440f78d14ef24bb1930e2c1cebe0e9a9f8e1220bbc47a81c8'}
OUT=J/(NAME+'_AUTHORED_ACCEPTANCE_V002.json');MD=J/(NAME+'_AUTHORED_ACCEPTANCE_V002.md');RECEIPT=J/(NAME+'_AUTHORED_ACCEPTANCE_RECEIPT_V002.json');ERROR=J/(NAME+'_AUTHORED_ACCEPTANCE_ERROR_V002.json')
OLD_FAILURE_PINS={'/private/tmp/unt_3d_local_energy_saved_acceptance_20261005_v001.py':'99ec2495928421b9352051cf8e3a0f1bd0e10573156d0a30e4b953c0a6b1d4d6',str(J/'local_record_feedback_3d_local_energy_source_response_v001_saved_authored_acceptance.py'):'99ec2495928421b9352051cf8e3a0f1bd0e10573156d0a30e4b953c0a6b1d4d6',str(J/(NAME+'_AUTHORED_ACCEPTANCE_ERROR.json')):'2670e2d68c69cf88e02f2c4693febbc7cf7973b0cf46b9353fcdf9966b1ed323'}
RECOVERY_SCOPE='V001 stopped at 2243 custody assertions before numerical reconstruction: parent journal has manifest stage at index0 and exactly one started at index1. V002 authenticates exact indices/PIDs and parent manifest commit; all arithmetic methods, 3e-11 criteria and qualifications unchanged.'
COORD=np.array(list(itertools.product(range(3),repeat=3)));PORTS=np.array(((0,0,0),(1,0,0),(0,1,0),(0,0,1)));INDEX={tuple(r):i for i,r in enumerate(COORD)}
KS=np.array(((0,0,0),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)))
PHASE=np.exp(-2j*np.pi*KS@COORD.T/3);OWNPAIRS=tuple(itertools.combinations(range(4),2));P=np.eye(4)-np.ones((4,4))/4
PAIRB=np.array([np.outer(P[:,a],P[:,b])+np.outer(P[:,b],P[:,a]) for a,b in OWNPAIRS]);EPS=(1/16,1/32);M=(64,128);BETA=4;H=.2
INC=np.zeros((54,108));FM=np.zeros((7,2,54),complex)
for r in range(27):
 for a in range(4):INC[r,4*r+a]=1;INC[27+INDEX[tuple((COORD[r]+PORTS[a])%3)],4*r+a]=1
FM[:,0,:27]=PHASE/math.sqrt(27);FM[:,1,27:]=PHASE/math.sqrt(27);EDGE_FOURIER=FM@INC
INPUTS={};CHECKS=[];ACTIVE={};ASSERTIONS=0;MAX_RATIO=0.;STARTED=False

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def clean(o):
 if isinstance(o,np.ndarray):return clean(o.tolist())
 if isinstance(o,np.generic):return clean(o.item())
 if isinstance(o,complex):return clean([o.real,o.imag])
 if isinstance(o,dict):return {str(k):clean(v) for k,v in o.items()}
 if isinstance(o,(list,tuple)):return [clean(v) for v in o]
 if isinstance(o,float) and not math.isfinite(o):return {'nonfinite':repr(o)}
 return o
def write(p,o):
 with Path(p).open('xb') as f:f.write(json.dumps(clean(o),indent=2,sort_keys=True,allow_nan=False).encode()+b'\n');f.flush();os.fsync(f.fileno())
 return sha(p)
def val(o):return np.asarray(o['real'])+1j*np.asarray(o['imag']) if isinstance(o,dict) and set(o)=={'real','imag'} else np.asarray(o)
def pin(p,h):
 p=str(Path(p).resolve())
 if p in INPUTS:exact('consistent input alias '+p,INPUTS[p]==h)
 else:exact('input seal '+p,sha(p)==h);INPUTS[p]=h
def exact(label,ok):
 global ASSERTIONS
 ASSERTIONS+=1;CHECKS.append({'label':label,'passed':bool(ok)})
 if not ok:raise AssertionError(label)
def close(label,a,b):
 global ASSERTIONS,MAX_RATIO
 a,b=np.asarray(a),np.asarray(b);finite=bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)));error=float(np.linalg.norm(a-b)) if finite else math.inf;allowance=3e-11*max(1,float(np.linalg.norm(b)))
 ASSERTIONS+=max(a.size,b.size,1);MAX_RATIO=max(MAX_RATIO,error/allowance);CHECKS.append({'label':label,'passed':finite and error<=allowance,'Frobenius_error':error,'allowance':allowance})
 if not finite or error>allowance:raise AssertionError((label,error,allowance))
def packet(name,stem,count,events):
 cp=J/(stem+'_checkpoints');p=read(J/(name+'_RESULT.json'));r=read(J/(name+'_RECEIPT.json'))
 for suffix in ('_RESULT.json','_RESULT.md','_RECEIPT.json'):pin(J/(name+suffix),sha(J/(name+suffix)))
 exact(name+' raw/canonical/report',r['result_sha256']==sha(J/(name+'_RESULT.json')) and r['result_canonical_sha256']==hashlib.sha256(canonical(p)).hexdigest() and r['report_sha256']==sha(J/(name+'_RESULT.md')))
 exact(name+' arithmetic',p['failed']==r['failed']==0 and p['passed']==r['passed']==p['check_count']==r['check_count']==len(p['checks']) and all(x['passed'] for x in p['checks']) and p['input_sha256']==r['input_sha256'])
 for f,h in r['input_sha256'].items():
  if f=='core_identity_canonical_sha256':exact('parent core hash',h==hashlib.sha256(canonical(read(cp/'manifest.json')['preserved_core_identity'])).hexdigest());continue
  path=J/('local_record_feedback_3d_pair_coordination_response_v001.py' if f=='source' else PARENT+'.md' if f=='protocol' else f);pin(path,h)
 cm=r['checkpoint_sha256'];exact(name+' CP census',len(cm)==count and set(cm)=={f.name for f in cp.iterdir() if f.name!='journal.jsonl'})
 for f,h in cm.items():pin(cp/f,h)
 jp=cp/'journal.jsonl';ls=jp.read_bytes().splitlines(keepends=True);es=[json.loads(x) for x in ls];pin(jp,sha(jp))
 exact(name+' journal count/prefix',len(es)==events and hashlib.sha256(b''.join(ls[:-1])).hexdigest()==r['journal_prefix_sha256'])
 exact(name+' final commits',es[-1]['event']=='receipt_complete' and es[-1]['sha256']==sha(J/(name+'_RECEIPT.json')) and es[-2]['event']=='report_complete' and es[-2]['sha256']==r['report_sha256'] and es[-3]['event']=='result_complete' and es[-3]['sha256']==r['result_sha256'] and es[-3].get('canonical_sha256',r['result_canonical_sha256'])==r['result_canonical_sha256'])
 manifest=read(cp/'manifest.json');start_index,expected_pid=(0,73342) if name==NAME else (1,49433)
 exact(name+' unique expected started index',[i for i,e in enumerate(es) if e.get('event')=='started']==[start_index])
 start=es[start_index]
 exact(name+' manifest/start/input/PID identities',manifest['input_sha256']==r['input_sha256']==p['input_sha256']==start['input_sha256'] and start['manifest_sha256']==cm['manifest.json'] and manifest['pid']==r['pid']==start['pid']==expected_pid and all(e['pid']==expected_pid for e in es))
 if name==PARENT:
  exact(name+' preceding manifest stage commit',es[0]['event']=='stage_complete' and es[0]['filename']=='manifest.json' and es[0]['sha256']==cm['manifest.json'] and es[0]['pid']==expected_pid)
 else:exact(name+' result PID identity',p['pid']==expected_pid)
 commits=[(e.get('filename'),e.get('sha256')) for e in es]
 exact(name+' every checkpoint commit',all((f,h) in commits or (name==NAME and f=='manifest.json') for f,h in cm.items()))
 return p,r

def reconstruct(z,index):
 q=z['bar_Q_every_production_measurement'];ke=z['K_e_every_production_measurement'];n=len(q);m=M[index];eps=EPS[index]
 exact('paired K/Q shapes',q.shape==(n,7,14) and ke.shape==(n,27,4) and ke.dtype==np.int64)
 exact('periodic K parity/range',bool(np.all(ke%2==0) and np.all((ke>=0)&(ke<=m))))
 x=eps*H;t=np.array(((math.cosh(x),math.sinh(x)),(math.sinh(x),math.cosh(x))));flip=np.array(((0,1),(1,0)));dt=(eps*H/2)*(flip@t);ddt=(eps*H/2)**2*t
 first=dt/t;second=ddt/t-first*first;kflat=ke.reshape(n,108)
 se=(m-kflat)*first[0,0]+kflat*first[0,1];sse=(m-kflat)*second[0,0]+kflat*second[0,1]
 d=np.stack((q[:,:,:6].sum(axis=2)/2-q[:,:,12]/2,q[:,:,6:12].sum(axis=2)/2-q[:,:,13]/2),axis=2)+PHASE.sum(axis=1)[None,:,None]/math.sqrt(27)
 e=d-np.einsum('kse,pe->pks',EDGE_FOURIER,se,optimize=True)/BETA
 c2=np.einsum('kse,kte,pe->pkst',EDGE_FOURIER,EDGE_FOURIER.conj(),sse,optimize=True)
 spin=-2*z['mean_z'][:,0].real/math.sqrt(27);spin=np.repeat(spin[:,None,:],2,axis=1);pairs=q[:,0,:12].real.reshape(n,2,6)/math.sqrt(27)
 tq=np.stack((q[:,0,:12].sum(axis=1),q[:,0,12:].sum(axis=1)),axis=1).real/math.sqrt(2)
 raw={'mean_Q':q,'second_Q':q[:,:,:,None]*q[:,:,None,:].conj(),'mean_D':d,'second_D':d[:,:,:,None]*d[:,:,None,:].conj(),
  'second_Dc':d[:,:,:,None]*q[:,:,None,12:].conj(),'local_spin_mean':spin,'local_pair_mean':pairs,'local_X_mean':spin@P,
  'local_XX_second':P[None,None]+np.einsum('psj,jab->psab',pairs,PAIRB,optimize=True),'local_c2_mean':pairs.sum(axis=2)/2+1,
  'mean_TQ_density_scaled':tq,'second_TQ_density':tq[:,:,None]*tq[:,None,:],
  'mean_E_dynamic':e,'second_E_dynamic':e[:,:,:,None]*e[:,:,None,:].conj(),'second_QE_dynamic':q[:,:,:,None]*e[:,:,None,:].conj(),
  'score_contact_C2':c2,'mean_K_edges':ke.astype(float),'mean_F_edges':se.reshape(n,27,4)/(eps*H/2),'mean_G_edges':sse.reshape(n,27,4)/(eps*H/2)**2}
 close('all local E modes',e,z['E_dynamic_every_production_measurement']);close('uniform path energy',e[:,0].sum(axis=1).real/(2*math.sqrt(27)),z['scalar'][:,0])
 exact('global K trace',np.array_equal(ke.sum(axis=(1,2)),z['scalar'][:,7]))
 pm=z['mean_d']@np.array(((1,1),(1,-1)))/math.sqrt(2)
 old=np.column_stack((z['scalar'][:,:3],z['scalar'][:,8:11],np.stack([np.stack((np.trace(z['second_z_ET'][:,k],axis1=1,axis2=2).real,np.sum(abs(z['mean_z'][:,k])**2,axis=1),abs(pm[:,k,0])**2,abs(pm[:,k,1])**2),axis=1) for k in range(7)],axis=1).reshape(n,28)))
 jd=[];ed=[]
 for k in (0,1,3,5):
  v=np.concatenate((q[:,0,:12],q[:,0,12:].sum(axis=1,keepdims=True)/math.sqrt(2)),axis=1) if k==0 else q[:,k]
  jd.extend([v.real]+([v.imag] if k else [])+[abs(v)**2])
  for s in range(2):ed.extend([e[:,k,s].real]+([e[:,k,s].imag] if k else [])+[abs(e[:,k,s])**2])
 joint=np.column_stack(jd+[tq[:,0]*tq[:,1]]);energy=np.column_stack(ed);diagnostic=np.concatenate((old,joint,energy),axis=1)
 exact('209 full primitives',diagnostic.shape==(n,209));close('all209 primitive traces',diagnostic,z['diagnostic_traces'])
 return raw,diagnostic

def estimate(raw):
 e,q=raw['mean_E_dynamic'],raw['mean_Q'];ee=raw['second_E_dynamic']-e[:,:,None]*e[:,None,:].conj();qq=raw['second_Q']-q[:,:,None]*q[:,None,:].conj();qe=raw['second_QE_dynamic']-q[:,:,None]*e[:,None,:].conj();c=raw['score_contact_C2'];r=-BETA*ee-c/BETA
 a,b,d=r[:,0,0].real,(r[:,0,1]+r[:,1,0].conj())/2,r[:,1,1].real;mid=(a+d)/2;spread=np.sqrt(((a-d)/2)**2+abs(b)**2)
 return {'mean_E_dynamic':e,'mean_Q':q,'mean_D':raw['mean_D'],'mean_K_edges':raw['mean_K_edges'],'mean_F_edges':raw['mean_F_edges'],'mean_G_edges':raw['mean_G_edges'],
  'energy_covariance':ee,'chi_EE':BETA*ee,'chi_QQ':BETA*qq,'chi_QE':BETA*qe,'chi_EQ':BETA*qe.conj().transpose(0,2,1),'score_contact_C2':c,'R_NN':r,'R_NN_eigenvalues':np.stack((mid-spread,mid+spread),axis=1),
  'uniform_R_density':r[0].sum().real/2,'uniform_contact_density':c[0].sum().real/2,'uniform_energy_susceptibility_density':BETA*ee[0].sum().real/2,'mean_dynamic_energy_density':e[0].sum().real/(2*math.sqrt(27))}
def summary(blocks):
 n=len(blocks['mean_Q']);central=estimate({k:v.mean(axis=0) for k,v in blocks.items()});rep={k:[] for k in central}
 for omit in range(n):
  keep=np.arange(n)!=omit
  for k,v in estimate({k:a[keep].mean(axis=0) for k,a in blocks.items()}).items():rep[k].append(v)
 errors={}
 for k,vs in rep.items():
  a=np.asarray(vs);re=np.sqrt((n-1)/n*np.sum((a.real-a.real.mean(axis=0))**2,axis=0));errors[k]={'real_se':re,'imag_se':np.sqrt((n-1)/n*np.sum((a.imag-a.imag.mean(axis=0))**2,axis=0))} if np.iscomplexobj(a) else {'se':re}
 return central,errors

def check_summary(row,blocks):
 central,errors=summary(blocks)
 exact('complete estimate/error field census',set(central)==set(row['estimates'])==set(row['component_errors']))
 for k,v in central.items():
  close('central '+k,v,val(row['estimates'][k]))
  exact('component error fields '+k,set(errors[k])==set(row['component_errors'][k]))
  for part,se in errors[k].items():close('replica SE '+k+part,se,val(row['component_errors'][k][part]))
 return central,errors

def ess(values):
 x=np.asarray(values,float);x=x-x.mean();n=len(x);s=np.correlate(x,x,mode='full')[n-1:n+510];c=s/np.arange(n,n-511,-1)
 if c[0]==0:return {'status':'UNDEFINED_CONSTANT','tau':None,'ESS':None}
 pairs=0;total=0.
 for i in range(1,511,2):
  pair=c[i]+c[i+1]
  if pair<=0:break
  total+=pair;pairs+=1
 tau=max(1.,1+2*total/c[0]);return {'status':'SHORT_CHAIN_IPP_ESTIMATE','tau':tau,'ESS':n/tau,'positive_pairs':pairs}
def rhat(x):
 a=np.array(x).reshape(8,512);means=a.mean(axis=1);w=np.mean(np.sum((a-means[:,None])**2,axis=1)/511);b=512*np.sum((means-means.mean())**2)/7
 if w==0:return {'status':'UNDEFINED_ZERO_WITHIN_VARIANCE','Rhat':None,'W':w,'B':b}
 return {'status':'UNRANKED_SHORT_SPLIT_ESTIMATE','Rhat':math.sqrt((511*w/512+b/512)/w),'W':w,'B':b}
def compare_diag(a,b):
 exact('diagnostic status',a['status']==b['status'])
 for k in a:
  if k in ('status','name'):continue
  if a[k] is None:exact('diagnostic undefined '+k,b[k] is None)
  elif k=='positive_pairs':exact('positive-pair cutoff',a[k]==b[k])
  else:close('diagnostic '+k,a[k],b[k])
def old_estimate(raw):
 zm,dm=raw['mean_z'],raw['mean_d'];et=raw['second_z_ET']-zm[:,:,None]*zm[:,None,:].conj();zero=raw['second_z_zero']-zm[:,:,None]*zm[:,None,:].conj();chi=BETA*(raw['second_d_zero']-dm[:,:,None]*dm[:,None,:].conj());rotation=np.array(((1,1),(1,-1)))/math.sqrt(2)
 even=np.array([rotation.T@a@rotation for a in chi]);hist=raw['hist_degree'];oriented=raw['hist_oriented_charge']
 return {'S_ET':et,'S_zero':zero,'chi_coord':chi,'chi_evenodd':even,'mean_z':zm,'mean_d':dm,
  'degree_histogram':hist,'all_vertex_degree_histogram':hist.mean(0),'coordination_delta_histogram':hist,'all_vertex_delta_histogram':hist.mean(0),
  'oriented_charge_histogram':oriented,'all_vertex_oriented_charge_histogram':oriented.mean(0),'cut_flux_histogram':raw['hist_flux'],'scalars':raw['scalar'],
  'S_ET_trace':np.trace(et,axis1=1,axis2=2),'S_zero_trace':np.trace(zero,axis1=1,axis2=2)}
def old_summary(blocks):
 n=len(blocks['scalar']);central=old_estimate({k:a.mean(0) for k,a in blocks.items()});rep={k:[] for k in central}
 for omit in range(n):
  for k,v in old_estimate({k:a[np.arange(n)!=omit].mean(0) for k,a in blocks.items()}).items():rep[k].append(v)
 errors={}
 for k,vs in rep.items():
  a=np.asarray(vs);re=np.sqrt((n-1)/n*np.sum((a.real-a.real.mean(0))**2,axis=0));errors[k]={'real_se':re,'imag_se':np.sqrt((n-1)/n*np.sum((a.imag-a.imag.mean(0))**2,axis=0))} if np.iscomplexobj(a) else {'se':re}
 return central,errors

def compare_old(row,blocks):
 central,errors=old_summary(blocks);exact('all old fields',set(central)==set(row['old_estimates'])==set(row['old_component_errors']))
 for k,v in central.items():
  close('old central '+k,v,val(row['old_estimates'][k]))
  for part,se in errors[k].items():close('old replica error '+k+part,se,val(row['old_component_errors'][k][part]))
 return central,errors

def compare_segments(row,old,central,errors,oldcentral,olderrors):
 c=row['old_new_segment_comparison'];exact('correlated segment statuses',c['old_status']==old['status'] and c['new_status']==row['status'] and c['interpretation']=='CORRELATED_SUCCESSIVE_SEGMENTS_SEPARATE_ERRORS_NO_INDEPENDENT_COMBINATION')
 exact('old/new comparison field census',set(c['quantities'])==set(oldcentral))
 for k,v in oldcentral.items():
  a=c['quantities'][k];close('old/new signed '+k,val(a['signed_new_minus_old']),v-val(old['estimates'][k]));exact('old SE preserved '+k,a['old_component_se']==old['component_errors'][k])
  for part,se in olderrors[k].items():close('new old-sector SE '+k+part,val(a['new_component_se'][part]),se)
 c=row['old_new_pair_coordination_comparison'];exact('pair segment statuses',c['old_status']==old['status'] and c['new_status']==row['status'] and c['old_spatial_energy_response']=='UNAVAILABLE_NOT_BACKFILLED')
 for k,pk in (('mean_Q','mean_Q'),('mean_D','mean_D'),('chi_QQ','chi_joint')):
  a=c['quantities'][k];close('pair signed '+k,val(a['signed_new_minus_old']),central[k]-val(old['joint_estimates'][pk]));exact('old pair SE '+k,a['old_component_se']==old['joint_component_errors'][pk])
  for part,se in errors[k].items():close('new pair SE '+k+part,val(a['new_component_se'][part]),se)

def compare_difference(stored,a,ae,b,be):
 exact('difference field census',set(stored['quantities'])==set(a))
 for k,v in a.items():
  close('signed grid/start '+k,val(stored['quantities'][k]['signed_first_minus_second']),v-b[k])
  for part,se in ae[k].items():close('grid/start combined SE '+k+part,val(stored['quantities'][k]['component_errors'][part]),np.sqrt(se**2+be[k][part]**2))

def trace_hist(a):
 return [{'values':v.tolist(),'counts':c.tolist()} for v,c in (np.unique(a[:,i],return_counts=True) for i in range(3))]

def main():
 global STARTED
 if sys.argv[1:]!=['--execute']:raise SystemExit('Requires exact root --execute.')
 if any(p.exists() for p in (OUT,MD,RECEIPT,ERROR)):raise SystemExit('Exclusive authored-acceptance output exists.')
 STARTED=True;began=time.monotonic()
 for f,h in OLD_FAILURE_PINS.items():pin(f,h)
 previous=read(J/(NAME+'_AUTHORED_ACCEPTANCE_ERROR.json'))
 exact('preserved V001 pre-numerical failure',previous['audit_status']=='FAILED_PRESERVED' and previous['assertions_reached']==2243 and previous['source_sha256']=='99ec2495928421b9352051cf8e3a0f1bd0e10573156d0a30e4b953c0a6b1d4d6' and previous['active']=={} and previous['error']=="AssertionError('LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001 manifest/start')" and previous['checks'][-1]['passed'] is False)
 for f,h in PINS.items():pin(J/f,h)
 p,r=packet(NAME,STEM,172,191);old,oldreceipt=packet(PARENT,'local_record_feedback_3d_pair_coordination_response_v001',342,378)
 exact('final197470/197470',p['passed']==197470 and p['status']=='FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED')
 exact('old aggregate and beta8 retained',old['status']=='MIXING_UNQUALIFIED' and p['parent_status']==old['status'] and p['parent_condition_statuses']==[{'condition':x['condition'],'status':x['status']} for x in old['conditions']])
 exact('fixed census/sole null/no inverse',len(p['chains'])==8 and len(p['conditions'])==2 and len(p['diagnostic_names'])==209 and p['diagnostic_names'][9]=='k0_coord_odd2' and p['covariance_inverse'] is None)
 exact('no c0 fit',p['C0_scope']['numerical_AR_or_self_choice'] is None and p['C0_scope']['sampled_constant']==0 and p['physical_scope']['inverse_computed'] is False)
 exact('full report10/70',sum(x.startswith('|c') for x in (J/(NAME+'_RESULT.md')).read_text().splitlines())==10 and (J/(NAME+'_RESULT.md')).read_text().count('```json')==70)
 records=[]
 for order,row in enumerate(p['chains']):
  index=order//4;cid=f'c{index}_'+('I01','I02','B','R')[order%4];ACTIVE.update(dataset=cid);exact('ordered eight chain census',row['id']==cid and row['condition']==index and row['beta']==4 and row['epsilon']==EPS[index] and row['M']==M[index] and row['production_sweeps']==1024 and row['burn_sweeps']==64)
  exact('chain saved commit duplicate',row==read(CP/(cid+'_complete.json')));exact('ten chain checkpoints',len(row['checkpoints'])==10)
  terminal=row['checkpoints'][-1];meta=read(CP/terminal['metadata'])
  with np.load(CP/terminal['bundle'],allow_pickle=False) as f:z={k:f[k].copy() for k in f.files}
  oldrow=next(a for a in old['chains'] if a['id']==cid);source=row['source_terminal_reference'];parentmeta=read(J/source['metadata'])
  oldref=oldrow['checkpoints'][-1];exact('authenticated named parent terminal',source=={**oldref,'metadata':str((PCP/oldref['metadata']).relative_to(J)),'bundle':str((PCP/oldref['bundle']).relative_to(J))})
  exact('full209 chain diagnostics',len(row['ESS_diagnostics'])==209 and row['diagnostic_names']==p['diagnostic_names'])
  with np.load(J/source['bundle'],allow_pickle=False) as f:oldbits=f['bits'].copy()
  for ci,ref in enumerate(row['checkpoints']):
   m=read(CP/ref['metadata']);n=0 if ci<2 else 128*(ci-1);burn=0 if ci==0 else 64;phase='segment_initial' if ci==0 else 'burn64' if ci==1 else 'production'+str(n)
   exact('CP ordered counters '+phase,m['id']==cid and m['phase']==phase and m['completed_burn_sweeps']==burn and m['completed_production_sweeps']==n and m['partial_block_count']==0 and m['complete_block_count']==n//32 and m['rng_state']['bit_generator']=='PCG64' and set(m['rng_state'])=={'bit_generator','state','has_uint32','uinteger'})
   exact('CP original/configuration '+phase,m['original_completed_counters']=={'burn_sweeps':64,'production_sweeps':1024} and m['configuration']=={k:row[k] for k in ('seed','beta','epsilon','M','start')} and set(m['rng_state']['state'])=={'state','inc'})
   exact('CP hashes/configuration '+phase,m['bundle']==ref['bundle'] and m['bundle_sha256']==ref['bundle_sha256']==r['checkpoint_sha256'][ref['bundle']] and ref['metadata_sha256']==r['checkpoint_sha256'][ref['metadata']] and m['input_sha256']==r['input_sha256'] and m['source_terminal_reference']==source)
   with np.load(CP/ref['bundle'],allow_pickle=False) as f:
    exact('binary snapshot '+phase,f['bits'].dtype==np.uint8 and f['bits'].shape==(M[index],27,4) and np.all((f['bits']==0)|(f['bits']==1)))
    for key in ('diagnostic_traces','bar_Q_every_production_measurement','E_dynamic_every_production_measurement','K_e_every_production_measurement','production_cycle_acceptance_traces'):
     exact('unaltered prefix '+phase+key,np.array_equal(f[key],z[key][:n]))
    exact('NPZ metadata shapes '+phase,set(f.files)==set(m['array_shapes']) and all(list(f[k].shape)==m['array_shapes'][k] for k in f.files))
    for key in f.files:
     if key.startswith(('source_block_sufficient_sums_','old_block_sufficient_sums_')):exact('immutable complete-block prefix '+phase+key,np.array_equal(f[key],z[key][:n//32]))
     elif key.startswith('source_partial_block_sufficient_sum_'):exact('completed CP has no partial source block',False)
    exact('complete32 counts '+phase,np.array_equal(f['complete_block_counts'],np.full(n//32,32)))
    if ci==0:exact('authentic initial bits/FULLPCG',np.array_equal(f['bits'],oldbits) and m['rng_state']==parentmeta['rng_state'])
  raw,diagnostic=reconstruct(z,index);blocks={k:a.reshape(32,32,*a.shape[1:]).mean(axis=1) for k,a in raw.items()}
  exact('serialized scalar/diagnostic/cycle traces',np.array_equal(row['scalar_traces'],z['scalar']) and np.array_equal(row['diagnostic_traces'],z['diagnostic_traces']) and np.array_equal(row['production_cycle_acceptance_traces'],z['production_cycle_acceptance_traces']))
  exact('full raw block fields',set(blocks)==set(row['block_raw_moments'])==set(row['block_sufficient_sums']))
  for k,v in blocks.items():
   close('raw32 block '+k,v,val(row['block_raw_moments'][k]));close('raw32 sufficient '+k,32*v,val(row['block_sufficient_sums'][k]));close('bundle32 sufficient '+k,32*v,z['source_block_sufficient_sums_'+k])
  central,errors=check_summary(row,blocks);oblocks={k:z[k].reshape(32,32,*z[k].shape[1:]).mean(axis=1) for k in row['old_block_raw_moments']}
  for k,v in oblocks.items():close('old raw32 '+k,v,val(row['old_block_raw_moments'][k]));close('old sums32 '+k,32*v,val(row['old_block_sufficient_sums'][k]))
  oc,oe=compare_old(row,oblocks);close('Q/old coordination response',central['chi_QQ'][:,12:,12:],oc['chi_coord'])
  for i,stored in enumerate(row['ESS_diagnostics']):compare_diag({'status':'STRUCTURAL_NULL','ESS':None,'tau':None} if i==9 else ess(diagnostic[:,i]),stored)
  phi,pt=z['scalar'][:,11:14],z['scalar'][:,8:11];ice=z['scalar'][:,14].astype(bool);changes=np.count_nonzero(np.diff(phi,axis=0),axis=0).tolist();tc=np.count_nonzero(np.diff(pt,axis=0),axis=0).tolist();w,c=np.unique(phi[ice],axis=0,return_counts=True)
  exact('all unconditional cut traces',changes==row['base_cut_change_counts'] and tc==row['time_averaged_cut_change_counts'] and trace_hist(phi)==row['base_cut_histograms'] and trace_hist(pt)==row['time_averaged_cut_histograms'] and row['ice_labeled_base_cut_histogram']=={'vectors':w.tolist(),'counts':c.tolist()} and row['ice_slice_count']==int(ice.sum()) and row['undefined_winding_slice_count']==int((~ice).sum()))
  exact('consecutive ice winding',row['consecutive_ice_winding_changes']==sum(bool(np.any(phi[i]!=phi[i-1])) for i in range(1,1024) if ice[i] and ice[i-1]))
  mix=all(x['ESS'] is not None and x['ESS']>=32 for i,x in enumerate(row['ESS_diagnostics']) if i!=9) and all(a>0 for a in changes+tc)
  exact('chain qualification',row['status']==('CHAIN_DIAGNOSTICS_PASSED_ONLY' if mix else 'MIXING_UNQUALIFIED'))
  exact('literal cycle attempts/acceptances',np.array_equal(z['cycle_attempts_burn_production'],np.tile(np.array((64,1024))[:,None],(1,54))) and np.all(z['cycle_acceptances_burn_production']>=0) and np.all(z['cycle_acceptances_burn_production']<=z['cycle_attempts_burn_production']) and np.array_equal(z['production_cycle_acceptance_traces'].sum(0),z['cycle_acceptances_burn_production'][1]))
  exact('all54 ordered cycle rows',len(row['cycle_acceptance_rows'])==54 and [cr['cycle'] for cr in row['cycle_acceptance_rows']]==list(range(54)))
  for cr in row['cycle_acceptance_rows']:
   for ii,label in enumerate(('burn','production')):
    actual=cr[label];a=int(z['cycle_attempts_burn_production'][ii,cr['cycle']]);b=int(z['cycle_acceptances_burn_production'][ii,cr['cycle']]);exact('cycle census',actual=={'attempts':a,'accepted':b,'rate':b/a})
  exact('six canonical pair rows',len(row['pair_acceptance_rows'])==6 and [x['pair'] for x in row['pair_acceptance_rows']]==[list(x) for x in OWNPAIRS])
  for pi,pr in enumerate(row['pair_acceptance_rows']):
   for ii,label in enumerate(('burn','production')):
    a=int(z['cycle_attempts_burn_production'][ii,9*pi:9*pi+9].sum());b=int(z['cycle_acceptances_burn_production'][ii,9*pi:9*pi+9].sum());exact('pair acceptance census',pr[label]=={'attempts':a,'accepted':b,'rate':b/a})
  compare_segments(row,oldrow,central,errors,oc,oe)
  records.append({'row':row,'blocks':blocks,'oldblocks':oblocks,'central':central,'errors':errors,'diagnostic':diagnostic})
 pooled=[]
 for index,row in enumerate(p['conditions']):
  ACTIVE.update(dataset='condition'+str(index));group=records[4*index:4*index+4];blocks={k:np.concatenate([x['blocks'][k] for x in group]) for k in group[0]['blocks']};oblocks={k:np.concatenate([x['oldblocks'][k] for x in group]) for k in group[0]['oldblocks']}
  exact('pooled condition order',row['condition']==index and row['chain_ids']==[x['row']['id'] for x in group] and row==read(CP/('condition'+str(index)+'_complete.json')) and row['pooled_block_counts']==[32]*128)
  for k,v in blocks.items():close('pooled128 raw '+k,v,val(row['pooled_block_raw_moments'][k]));close('pooled128 sum '+k,32*v,val(row['pooled_block_sufficient_sums'][k]))
  central,errors=check_summary(row,blocks);oc,oe=compare_old(row,oblocks)
  exact('full209 pooled diagnostics',len(row['split_Rhat'])==209 and [a['name'] for a in row['split_Rhat']]==p['diagnostic_names'])
  for i,stored in enumerate(row['split_Rhat']):compare_diag({'status':'STRUCTURAL_NULL','Rhat':None} if i==9 else rhat([x['diagnostic'][:,i] for x in group]),stored)
  mix=all(x['row']['status']=='CHAIN_DIAGNOSTICS_PASSED_ONLY' for x in group) and all(a['Rhat'] is not None and a['Rhat']<=1.1 for i,a in enumerate(row['split_Rhat']) if i!=9)
  exact('pooled qualification',row['status']==('FINITE_GRID_LOCAL_ENERGY_SOURCE_DIAGNOSTICS_PASSED' if mix else 'MIXING_UNQUALIFIED'))
  compare_segments(row,old['conditions'][index],central,errors,oc,oe);exact('six between-start comparisons',len(row['between_chain_differences'])==6)
  for stored,(a,b) in zip(row['between_chain_differences'],itertools.combinations(range(4),2)):
   exact('between-start order',stored['first']==group[a]['row']['id'] and stored['second']==group[b]['row']['id']);compare_difference(stored,group[a]['central'],group[a]['errors'],group[b]['central'],group[b]['errors'])
  pooled.append({'central':central,'errors':errors})
 compare_difference(p['grid_comparison'],pooled[0]['central'],pooled[0]['errors'],pooled[1]['central'],pooled[1]['errors'])
 controls=read(CP/'controls.json');exact('proper-bath and constant guards',controls['diagnostic_count']==209 and controls['qualified_nonstructural_count']==208 and controls['C0_scope']==p['C0_scope'] and len(controls['proper_bath_controls'])==6 and all(a['complete_second_uniform_curvature']==0 and a['weight_invariant'] for a in controls['proper_bath_controls']))
 for path,h in INPUTS.items():exact('after input '+path,sha(path)==h)
 result={'audit_status':'PASS','failed_assertions':0,'assertions':ASSERTIONS,'check_count':len(CHECKS),'maximum_fraction_of_frozen_allowance':MAX_RATIO,'source_sha256':sha(__file__),'result_sha256':r['result_sha256'],'parent_receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'input_sha256':INPUTS,'datasets':10,'chains':8,'conditions':2,'paired_new_measurements':8192,'modes':7,'replicas':512,'old_beta8_and_inverse_refusals':'preserved; none requalified','recovery_scope':RECOVERY_SCOPE,'preserved_failed_attempt_sha256':OLD_FAILURE_PINS,'authorship_scope':'Distinct literal-transfer/graph and direct omitted-block authored arithmetic acceptance, independently peer-reviewed/root-executed. Same author as the producer; not independent authorship or Stage3 synthesis.','scope':'finite beta4/twoM/L3 network NN contribution; no complete gravitational polarization, continuum/ground phase, field or metric adoption','checks':CHECKS,'elapsed_seconds':time.monotonic()-began,'PID':os.getpid()}
 rh=write(OUT,result)
 with MD.open('x') as f:f.write('# Authored distinct-method bulk acceptance V002\n\nThe V001 custody guard failure remains preserved. V002 corrects the exact parent/new journal start indices and authenticates the parent manifest commit and original PID/input identities; numerical methods, criteria and qualifications are unchanged.\n\nPASS: all eight lineages, two pooled conditions, 8192 paired production measurements, seven modes and 512 correlated block replicas. Literal transfer-entry derivatives and graph incidence reproduce every local energy and required second score; response/error, all 209 diagnostic and status/custody checks pass at unchanged 3e-11 Frobenius criteria.\n\nThis is distinct-method authored arithmetic acceptance with independent peer review and root execution, not independent authorship or independent physical synthesis. Old beta8/inverse refusals remain, symbolic AR/self stays unselected, and the proper-bath uniform guard is distinct from fixed-coordinate response.\n\nAssertions: %d. Largest fraction of frozen allowance: %.12g. Accepted raw result: %s. Audit SHA256: %s.\n'%(ASSERTIONS,MAX_RATIO,r['result_sha256'],rh));f.flush();os.fsync(f.fileno())
 for path,h in INPUTS.items():
  if sha(path)!=h:raise AssertionError('post-output input changed '+path)
 rr=write(RECEIPT,{'audit_status':'PASS','audit_sha256':rh,'report_sha256':sha(MD),'source_sha256':sha(__file__),'input_sha256':INPUTS,'result_sha256':r['result_sha256'],'assertions':ASSERTIONS,'preserved_failed_attempt_sha256':OLD_FAILURE_PINS,'recovery_scope':RECOVERY_SCOPE,'PID':os.getpid()});print(json.dumps({'status':'PASS','assertions':ASSERTIONS,'audit_sha256':rh,'receipt_sha256':rr}),flush=True)
if __name__=='__main__':
 try:main()
 except Exception as e:
  if STARTED and not ERROR.exists():write(ERROR,{'audit_status':'FAILED_PRESERVED','error':repr(e),'traceback':traceback.format_exc(),'active':ACTIVE,'checks':CHECKS,'source_sha256':sha(__file__),'input_sha256':INPUTS,'assertions_reached':ASSERTIONS})
  print(traceback.format_exc(),file=sys.stderr);sys.exit(3)
