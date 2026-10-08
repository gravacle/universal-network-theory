#!/usr/bin/env python3
"""Independent original-stream audit; no producer, H, RNG or evolution import."""
import hashlib,json,math,os,pathlib,time,traceback
import numpy as np
J=pathlib.Path(__file__).resolve().parent
N='LOCAL_RECORD_FEEDBACK_3D_CHARGING_JUNCTION_RESPONSE_V001'
S='local_record_feedback_3d_charging_junction_response_v001'
C=J/(S+'_checkpoints'); A=J/(N+'_AUDIT.json'); M=J/(N+'_AUDIT.md')
ERR=J/(N+'_AUDIT_ERROR.json'); ASSERTIONS=0; MAX=0.; ACTIVE='custody'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rd(p):return json.loads(p.read_bytes())
def cb(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def exact(v,label):
 global ASSERTIONS
 ASSERTIONS+=1
 if not v:raise AssertionError(label)
def un(v):return np.array(v['real'])+1j*np.array(v['imag']) if isinstance(v,dict) else np.asarray(v)
def near(a,b,label):
 global ASSERTIONS,MAX
 a,b=np.asarray(a),np.asarray(b);e=float(np.linalg.norm(a-b));tol=3e-11*max(1,float(np.linalg.norm(b)))
 ASSERTIONS+=1;MAX=max(MAX,e)
 if not np.isfinite(e) or e>tol:raise AssertionError((label,e,tol))
def out(p,v):
 with p.open('xb') as f:f.write(cb(v)+b'\n');f.flush();os.fsync(f.fileno())
def run():
 global ACTIVE
 begin=time.monotonic();exact(not any(p.exists() for p in (A,M,ERR)),'exclusive audit outputs')
 p=rd(J/(N+'_RESULT.json'));r=rd(J/(N+'_RECEIPT.json'))
 exact(sha(J/(N+'_RESULT.json'))==r['result_sha256']=='35a60052709129899de2e870e4d8801376b593c59a7139020b8647925d950998','raw')
 exact(hashlib.sha256(cb(p)).hexdigest()==r['result_canonical_sha256'],'canonical')
 exact(sha(J/(N+'_REPORT.md'))==r['report_sha256'],'report') if (J/(N+'_REPORT.md')).exists() else exact(sha(J/(N+'_RESULT.md'))==r['report_sha256'],'report')
 exact(p['passed']==r['passed']==16046 and p['failed']==r['failed']==0 and all(x['passed'] for x in p['checks']),'status')
 exact(p['input_sha256']==r['input_sha256'],'input map')
 inputs={f:sha(J/(S+'.py' if f=='source' else N+'.md' if f=='protocol' else f)) for f in r['input_sha256']}
 exact(inputs==r['input_sha256'],'every current input')
 exact(len(r['checkpoint_sha256'])==21 and {x.name for x in C.iterdir() if x.name!='journal.jsonl'}==set(r['checkpoint_sha256']),'21 checkpoint census')
 for f,h in r['checkpoint_sha256'].items():exact(sha(C/f)==h,'checkpoint '+f)
 jb=(C/'journal.jsonl').read_bytes();es=[json.loads(x) for x in jb.splitlines()]
 exact(hashlib.sha256(b'\n'.join(jb.splitlines()[:-1])+b'\n').hexdigest()==r['journal_prefix_sha256'],'prefix')
 exact(es[-1]['event']=='receipt_complete' and es[-1]['sha256']==sha(J/(N+'_RECEIPT.json')),'receipt event')
 manifest=rd(C/'manifest.json');exact(manifest['input_sha256']==inputs,'manifest')
 exact(any(e['event']=='started' and e['input_sha256']==inputs and e['manifest_sha256']==sha(C/'manifest.json') for e in es),'start')
 commits=[(e['filename'],e['sha256']) for e in es if e['event']=='stage_complete']
 exact(len(commits)==21 and dict(commits)==r['checkpoint_sha256'],'stage commits')
 joint=rd(J/'LOCAL_RECORD_FEEDBACK_3D_PAIR_COORDINATION_RESPONSE_V001_RESULT.json')
 strain=rd(J/'LOCAL_RECORD_FEEDBACK_3D_SIX_STRAIN_CHARGING_STIFFNESS_V001_RESULT.json')
 models=strain['models']; old={x['id']:x for x in joint['chains']};old.update({'condition'+str(x['condition']):x for x in joint['conditions']})
 expected=[x['id'] for x in joint['chains']]+['condition'+str(x['condition']) for x in joint['conditions']]
 exact([x['id'] for x in p['rows']]==expected,'all20 ordered rows')
 V=54.;ncell=27.;h=.2;vec=np.r_[np.ones(12),-1,-1]/2;uniform=np.array([1,1,1,0,0,0]);block={};replicas=0
 for ch in joint['chains']:
  ACTIVE=ch['id'];cp=J/'local_record_feedback_3d_pair_coordination_response_v001_checkpoints'/ch['checkpoints'][-1]['bundle']
  with np.load(cp,allow_pickle=False) as z:sc=z['scalar'];q=z['bar_Q_every_production_measurement'][:,0,:];di=z['diagnostic_traces']
  exact(sc.shape==(1024,15) and q.shape==(1024,14),'1024 paired samples')
  e,k=sc[:,6],sc[:,7];eps=ch['epsilon'];beta=ch['beta'];total=ch['M']*108.;x=eps*h
  near(e,sc[:,0]-sc[:,1],'scalar energy');near(e,di[:,0]-di[:,1],'diagnostic energy')
  sh=eps*((total-k)*np.tanh(x)+k/np.tanh(x))
  shh=eps**2*((total-k)/np.cosh(x)**2-k/np.sinh(x)**2)
  near(sh,-beta*V*e/h,'independent score identity')
  rr=q@vec;dd=1+np.sqrt(ncell)*rr/V;near(dd,sc[:,1],'diagonal source')
  raw={'q':q,'qE':q*e[:,None],'rr':rr*np.conj(rr),'e':e,'k':k,'sh':sh,'sh2':sh**2,'shh':shh,'D':dd}
  block[ch['id']]={a:b.reshape((32,32)+b.shape[1:]).sum(1) for a,b in raw.items()}
 for co in joint['conditions']:
  block['condition'+str(co['condition'])]={a:np.concatenate([block[c][a] for c in co['chain_ids']]) for a in block[co['chain_ids'][0]]}
 def val(raw,beta,model):
  q,e=raw['q'],raw['e'];rbar=q@vec
  # Independent log-partition derivative representation; keep contact separate.
  svar=raw['sh2']-raw['sh']*raw['sh'];scontact=raw['shh'];hh=(svar+scontact)/(beta*V)
  mixed=beta*np.sqrt(ncell)/h*(un(model['source_rows'])@(raw['qE']-e*q));u=uniform@mixed
  dd=beta*ncell/V*(raw['rr']-rbar*np.conj(rbar));jm=raw['D']+model['AR']+model['alpha'];ct=2*jm;cap=ct-dd
  c=np.array([cap+2*e+2*h*u-h*h*hh,4*e/h+2*u-2*h*hh,-hh])
  return {'mean_transverse_energy_density':e,'mean_kinks':raw['k'],'mean_h_score':raw['sh'],'variance_h_score':svar,'mean_direct_log_weight_hh_contact':scontact,'score_variance_density':svar/(beta*V),'score_contact_density':scontact/(beta*V),'chi_hh_density':hh,'chi_Ah_six_density':mixed,'chi_uniform_h_density':u,'mean_D_density':raw['D'],'mean_Jcap_density':jm,'charging_contact_density':ct,'chi_DD_density':dd,'Kcap_uniform_density':cap,'symbolic_hT_polynomial_coefficients':c}
 for row in p['rows']:
  ACTIVE=row['id'];b=block[ACTIVE];cnt=len(b['e']);exact(cnt==row['block_count'] and row['parent_status']==old[ACTIVE]['status'],'block/status')
  for k,x in b.items():near(x,un(row['raw_block_sufficient_sums'][k]),'original paired blocks '+k)
  total={k:x.sum(0) for k,x in b.items()};raw={k:x/(cnt*32) for k,x in total.items()}
  for model,branch in zip(models,row['branches']):
   exact(model['AR_fraction']==branch['AR_fraction'],'branch');v=val(raw,row['beta'],model)
   for k,x in v.items():near(x,un(branch['values'][k]),'central '+k)
   calc=[]
   for i in range(cnt):
    vv=val({k:(x-b[k][i])/((cnt-1)*32) for k,x in total.items()},row['beta'],model);calc.append(vv);replicas+=1
    for k,x in vv.items():near(x,un(branch['leave_one_complete_block_replicas'][i][k]),'replica '+k)
   for k in v:
    z=np.array([q[k] for q in calc])
    for part in ('real','imag'):
     a=getattr(z,part);jk=np.sqrt((cnt-1)/cnt*np.sum((a-np.mean(a,0))**2,0));near(jk,branch['component_errors'][k][part+'_se'],'SE '+k+part)
  exact(rd(C/(ACTIVE+'.json'))==row,'completed stage row')
 exact(replicas==3072,'all3072 replicas')
 for f,hsh in inputs.items():exact(sha(J/(S+'.py' if f=='source' else N+'.md' if f=='protocol' else f))==hsh,'unchanged input')
 result={'audit_status':'PASS','assertions':ASSERTIONS,'maximum_norm_residual':MAX,'datasets':20,'branches':60,'joint_replicas':replicas,'parent_result_sha256':r['result_sha256'],'parent_receipt_sha256':sha(J/(N+'_RECEIPT.json')),'audit_source_sha256':sha(pathlib.Path(__file__)),'elapsed_seconds':time.monotonic()-begin,'PID':os.getpid(),'method':'Independent original paired NPZ streams, raw blocks, score/contact and complete joint replicas; no producer/H/RNG/evolution import.'}
 out(A,result)
 with M.open('x') as f:f.write('# Independent saved charging/junction audit V001\n\nPASS: all20 datasets,60 branches and3072 paired block replicas.\n\nOriginal paired e/K/Q streams, signed score/contact, all six mixed responses, complete polynomial coefficients and real/imaginary errors were reconstructed. No producer or history replay. Parent scientific statuses unchanged.\n\nAudit JSON SHA256: '+sha(A)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(result),flush=True)
if __name__=='__main__':
 try:run()
 except Exception as exc:
  if not ERR.exists():out(ERR,{'audit_status':'FAIL_PRESERVED','error':repr(exc),'traceback':traceback.format_exc(),'active':ACTIVE,'assertions_before_failure':ASSERTIONS,'maximum_norm_residual':MAX})
  raise
