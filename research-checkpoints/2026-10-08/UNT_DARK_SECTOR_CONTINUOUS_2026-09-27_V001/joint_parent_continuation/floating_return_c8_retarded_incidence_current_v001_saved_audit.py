import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,hashlib,math,sys,time,traceback
from pathlib import Path
from fractions import Fraction
import numpy as np
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory');J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
NAME='FLOATING_RETURN_C8_RETARDED_INCIDENCE_CURRENT_V001';CP=J/'floating_return_c8_retarded_incidence_current_v001_checkpoints'
SOURCE=J/'floating_return_c8_retarded_incidence_current_v001.py';PROTO=J/(NAME+'.md')
AUDIT=J/(NAME+'_AUDIT.json');REPORT=J/(NAME+'_AUDIT.md');ERROR=J/(NAME+'_AUDIT_ERROR_V001.json')
FINAL_PINS={'source':'d828f3aaf6fcb0c452833c6d94813ec4de85b85be228afa4a701315443a13fd2','protocol':'6a4b32a76b16405871ffba37d86b2012862a4f8336ec5c8f34e258a2312fcd44','result':'8fc2e783d34ecf8071361afc2a659d32ea51452af018ea9c1054dccb0e45c963','receipt':'268b754c6a8fde585c44685fce716a64dc9e5245eb6d7b6fa59089717b14e49c'}
PARENTS=(('FLOATING_RETURN_C8_TAGGED_PROBE_REACTION_V001',J/'floating_return_c8_tagged_probe_reaction_v001_checkpoints'),('FLOATING_RETURN_C8_ENDPOINT_RECORD_ISOLATION_V001',J/'floating_return_c8_endpoint_record_isolation_v001_checkpoints'))
TIMES=('0','1/5','2','8');TP=tuple((i,k) for i in range(4) for k in range(i+1));CHANNELS=('retained_on','retained_reference','reset_on','reset_reference')
CYCLE=(0,4,3,7,2,6,1,5);EDGES=tuple((CYCLE[i],CYCLE[(i+1)%8]) for i in range(8));PAIRS=np.array([(a,b) for a in range(8) for b in range(8) if a!=b]);PI={tuple(v):k for k,v in enumerate(PAIRS)}
OCC=np.array([(PAIRS[:,0]==v).astype(int)+(PAIRS[:,1]==v).astype(int) for v in range(8)]);REST=(1,2,3,5,6,7)
TR=tuple((tuple((PI[(u,b)],PI[(v,b)]) for b in range(8) if b not in (u,v)),tuple((PI[(a,u)],PI[(a,v)]) for a in range(8) if a not in (u,v))) for u,v in EDGES)
N=0;FAIL=[];MAX={};INPUTS={};ACTIVE={};START=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def blob(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(name,ok):
 global N
 N+=1
 if not bool(ok):FAIL.append({'name':name})
def near(name,a,b,tol=1e-9):
 global N
 N+=1;a,b=np.asarray(a),np.asarray(b);valid=np.isfinite(a).all() and np.isfinite(b).all();err=float(np.max(abs(a-b))) if valid and a.size else 0. if valid else math.inf
 key=name.rsplit(':',1)[-1];MAX[key]=max(MAX.get(key,0.),err)
 if not valid or err>tol:FAIL.append({'name':name,'error':repr(err),'tolerance':tol})
def complex_value(v):
 a=np.asarray(v,float);return a[...,0]+1j*a[...,1]
def safe(v):
 if isinstance(v,dict):return {str(k):safe(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [safe(x) for x in v]
 if isinstance(v,float) and not math.isfinite(v):return {'nonfinite':repr(v)}
 return v
def write(p,v):
 with p.open('x') as f:json.dump(safe(v),f,sort_keys=True,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def add_pin(p,h=None):
 p=Path(p);actual=sha(p);check('pin:'+str(p),h is None or actual==h);INPUTS[str(p.relative_to(ROOT))]=actual
def authenticate(name,cp,parent=False):
 r=read(J/(name+'_RESULT.json'));rec=read(J/(name+'_RECEIPT.json'))
 for suffix in ('_RESULT.json','_RESULT.md','_RECEIPT.json'):add_pin(J/(name+suffix))
 check(name+':raw',sha(J/(name+'_RESULT.json'))==rec['result_raw_sha256']);check(name+':canonical',hashlib.sha256(blob(r)).hexdigest()==rec['result_canonical_sha256']);check(name+':report',sha(J/(name+'_RESULT.md'))==rec['report_sha256'])
 check(name+':input_map',r['input_sha256']==rec['input_sha256']);check(name+':controls',r['failed']==rec['failed']==0 and r['passed']==rec['passed']==len(r['checks']) and all(v['passed'] for v in r['checks']))
 for f,h in rec['input_sha256'].items():add_pin(ROOT/f,h)
 cmap=rec['checkpoint_sha256'];check(name+':CP_census',len(cmap)==(1146 if parent else 7594) and set(cmap)=={p.name for p in cp.iterdir() if p.name!='journal.jsonl'})
 for f,h in cmap.items():add_pin(cp/f,h)
 jb=(cp/'journal.jsonl').read_bytes();events=[json.loads(x) for x in jb.splitlines()];add_pin(cp/'journal.jsonl')
 check(name+':events',len(events)==(1149 if parent else 7597));check(name+':prefix',rec['journal_prefix_sha256']==hashlib.sha256(b'\n'.join(jb.splitlines()[:-1])+b'\n').hexdigest())
 check(name+':receipt_commit',events[-1]=={'event':'receipt_saved','sha256':sha(J/(name+'_RECEIPT.json'))})
 check(name+':result_commit',events[-3]=={'event':'result_saved','raw_sha256':rec['result_raw_sha256'],'canonical_sha256':rec['result_canonical_sha256']})
 check(name+':report_commit',events[-2]==({'event':'report_saved','sha256':rec['report_sha256'],'paired_data_rows':416} if parent else {'event':'report_saved','sha256':rec['report_sha256'],'data_rows':4160}))
 manifest=read(cp/'manifest.json');check(name+':manifest',events[0]['manifest_sha256']==r['manifest_sha256']==sha(cp/'manifest.json') and events[0]['input_sha256']==manifest['input_sha256']==rec['input_sha256'])
 check(name+':PID',events[0]['PID']==manifest['PID']==rec['original_manifest_PID' if parent else 'PID'])
 commits={'manifest.json':sha(cp/'manifest.json')}
 for e in events[1:-3]:check(name+':unique_commit',e['file'] not in commits);commits[e['file']]=e['sha256']
 check(name+':all_commits',commits==cmap)
 if parent:
  a=read(J/(name+'_AUDIT.json'));add_pin(J/(name+'_AUDIT.json'));add_pin(J/(name+'_AUDIT.md'));check(name+':audit',a['audit_status']=='PASS' and a['failed_assertions']==0 and a['result_raw_sha256']==rec['result_raw_sha256'] and a['receipt_sha256']==sha(J/(name+'_RECEIPT.json')))
 return r,rec
def action(a,kind,bits,ar,two):
 if kind=='n':out=np.zeros_like(a);out[:,1]=a[:,1];return out
 if kind=='I':return .2*np.stack((-1j*a[:,1],1j*a[:,0]),axis=1)
 if kind=='K':return .2*a[:,::-1]
 out=(8+(2 if two else 1)+ar*bits.sum(0))[:,None,None,None]*a;out[:,0]+=(2+.5*(bits[0]+bits[4]))[:,None,None]*a[:,0]
 for k,(u,v) in enumerate(EDGES):
  cd=OCC[u]+OCC[v]-2*OCC[u]*OCC[v] if two else (np.arange(8)==u).astype(int)+(np.arange(8)==v).astype(int)
  for e in ((1,) if k==0 else (0,1)):
   out[:,e]+=.25*cd[None,:,None]*a[:,e]
   for transitions in (TR[k] if two else (((u,v),),)):
    l,r=np.array(transitions).T;out[:,e,l]-=.1*a[:,e,r];out[:,e,r]-=.1*a[:,e,l]
 return out-.2*a[:,::-1]
def coeff(a,vec,s):
 af=a.reshape(a.shape[0],-1,a.shape[-1]);out=np.empty_like(af)
 for q in range(3):
  ids=np.flatnonzero(s==q)
  if len(ids):out[ids]=np.einsum('ij,qjc->qic',vec[q].conj().T,af[ids])
 return out
def clocks(a,ad,words):
 b=np.zeros(8,complex);d=np.zeros(8,complex);index={int(w):i for i,w in enumerate(words)}
 for v in REST:
  low=np.array([i for i,w in enumerate(words) if not int(w)&(1<<v)]);high=np.array([index[int(words[i])|(1<<v)] for i in low])
  b[v]=2*np.vdot(a[high],a[low]);d[v]=2*(np.vdot(ad[high],a[low])+np.vdot(a[high],ad[low]))
 return b,d
def inner(a,b,phase=None):return np.vdot(a,b if phase is None else b*phase[:,:,None])
def main():
 global ACTIVE
 if sys.argv[1:]!=['--execute']:raise SystemExit('exact --execute required; no audit/output created')
 if any(p.exists() for p in (AUDIT,REPORT,ERROR)):raise RuntimeError('preserve any prior audit')
 for key,p in [('source',SOURCE),('protocol',PROTO),('result',J/(NAME+'_RESULT.json')),('receipt',J/(NAME+'_RECEIPT.json'))]:
  if FINAL_PINS[key].startswith('PENDING'):raise RuntimeError('final parent pins pending')
  add_pin(p,FINAL_PINS[key])
 result,receipt=authenticate(NAME,CP);parents=[authenticate(*p,parent=True)[0] for p in PARENTS];input_id=hashlib.sha256(blob(result['input_sha256'])).hexdigest()
 check('104_preparations',len(result['preparations'])==104);check('report_rows',sum(x.startswith('|case') for x in (J/(NAME+'_RESULT.md')).read_text().splitlines())==4160)
 with np.load(CP/'reused_response_bases.npz',allow_pickle=False) as z:
  be,bv,re,rv=z['tagged_eigenvalues'],z['tagged_eigenvectors'],z['reference_eigenvalues'],z['reference_eigenvectors'];bi,ri=z['tagged_I_in_eigenbasis'],z['reference_I_in_eigenbasis'];meta=json.loads(str(z['metadata_json']))
 check('bases_metadata',meta['new_eigensolver_calls']==0 and meta['input_sha256']==result['input_sha256'] and all(c['passed'] for c in meta['checks']))
 with np.load(PARENTS[0][1]/'reaction_eigensystems.npz',allow_pickle=False) as z:
  for name,actual in [('tagged_base_eigenvalues',be),('tagged_base_eigenvectors',bv),('reference_base_eigenvalues',re),('reference_base_eigenvectors',rv)]:near('sealed_basis:'+name,actual,z[name],0)
  bm,rm=z['tagged_base_matrices'],z['reference_base_matrices']
 for ev,vec,im,mat,dim in ((be,bv,bi,bm,56),(re,rv,ri,rm,8)):
  nv=np.diag(np.r_[np.zeros(dim),np.ones(dim)]);iv=.2*np.kron(np.array([[0,-1j],[1j,0]]),np.eye(dim));kv=.2*np.kron(np.array([[0,1],[1,0]]),np.eye(dim))
  for s in range(3):
   near('basis:orthogonal',vec[s].conj().T@vec[s],np.eye(2*dim),5e-10);near('basis:residual',mat[s]@vec[s],vec[s]*ev[s],5e-10);near('basis:current_matrix',im[s],vec[s].conj().T@iv@vec[s],5e-10)
   near('basis:commutator_current',1j*(mat[s]@nv-nv@mat[s]),iv,5e-10);near('basis:double_contact',-(nv@(nv@mat[s]-mat[s]@nv)-(nv@mat[s]-mat[s]@nv)@nv),kv,5e-10)
 rows=0;frames=0;signed=[]
 for pi,p in enumerate(result['preparations']):
  name=f'case{pi//13:02d}_prep{pi%13:02d}';ACTIVE={'preparation':name};check(name+':label',p['preparation']==name);check(name+':complete',read(CP/(name+'_complete.json'))==p)
  check(name+':channel_census',tuple(c['channel'] for c in p['channels'])==CHANNELS);values=[];common=[]
  for ci,ch in enumerate(p['channels']):
   reset=ci>=2;two=ci%2==0;mode='tagged' if two else 'reference';parent=parents[int(reset)]['preparations'][pi];pcp=PARENTS[int(reset)][1];ev,vec=(be,bv) if two else (re,rv);dim=56 if two else 8
   ar=float(Fraction(parent['AR_rational']));words=np.array([sum(((r>>k)&1)<<v for k,v in enumerate(REST)) for r in range(64)]) if reset else np.arange(256);bits=((words[None,:]>>np.arange(8)[:,None])&1).astype(int);s=bits[0]+bits[4];energy=ev[s]+ar*bits.sum(0)[:,None]
   check(name+':channel_metadata',ch['preparation']==name and ch['AR_rational']==parent['AR_rational'] and ch['formation_gamma_rational']==parent['formation_gamma_rational'] and ch['preparation_x_rational']==parent['preparation_x_rational']);check(name+':ten_pairs',len(ch['rows'])==10 and len(parent['rows'])==4)
   sf=[];clock=[]
   for ti in range(4):
    ACTIVE={'preparation':name,'channel':ch['channel'],'source_time_index':ti};label=name+'/'+ch['channel']+'/'+str(ti);pr=parent['rows'][ti]
    with np.load(pcp/pr['state_file'],allow_pickle=False) as z:a=z['psi_'+mode]
    md=read(CP/(name+'_'+ch['channel']+'_source'+str(ti)+'.json'))
    with np.load(CP/(name+'_'+ch['channel']+'_source'+str(ti)+'.npz'),allow_pickle=False) as z:c,ic,nc,e=z['saved_state_spectral_coefficients'],z['I_source_coefficients'],z['n_source_coefficients'],z['absolute_eigenvalues'];zm=json.loads(str(z['metadata_json']))
    check(label+':source_metadata',zm=={k:md[k] for k in zm} and md['bundle_sha256']==sha(CP/(name+'_'+ch['channel']+'_source'+str(ti)+'.npz')) and md['parent_state_sha256']==pr['state_sha256']==sha(pcp/pr['state_file']) and md['source_time_index']==ti and md['source_x_rational']==TIMES[ti] and md['preparation']==name and md['channel']==ch['channel'])
    check(label+':source_input_identity',md['input_map_sha256']==input_id)
    near(label+':absolute_energies',e,energy,0);near(label+':saved_state_coefficients',c,coeff(a,vec,s),5e-10)
    na,ia,ka,ha=[action(a,k,bits,ar,two) for k in ('n','I','K','H')]
    near(label+':n_coefficients',nc,coeff(na,vec,s),5e-10);near(label+':I_coefficients',ic,coeff(ia,vec,s),5e-10);near(label+':H_coefficients',energy[:,:,None]*c,coeff(ha,vec,s),5e-10)
    for key,val in [('baseline_n',np.vdot(a,na).real),('baseline_I',np.vdot(a,ia).real),('baseline_K',np.vdot(a,ka).real),('baseline_I_dot',2*np.vdot(ia,ha).imag)]:near(label+':'+key,val,md[key],1e-8)
    near(label+':n_idempotence',np.vdot(nc,nc).real,md['baseline_n']);near(label+':current_square',np.vdot(ic,ic).real,.04*np.vdot(a,a).real)
    for cc,aa,scalar in ((c,a,1.),(ic,a,.04),(nc,na,1.)):
     cf=cc.reshape(-1,cc.shape[-1]);af=aa.reshape(-1,aa.shape[-1]);near(label+':full_Gram',cf.conj().T@cf,scalar*(af.conj().T@af))
    bp,bd=clocks(a,-1j*ha,words);near(label+':six_clock_beta',bp[list(REST)],complex_value(md['parent_Bplus_beta_global'])[list(REST)],5e-10);near(label+':six_clock_dot',bd[list(REST)],complex_value(md['parent_Bplus_dot_global'])[list(REST)],5e-10);clock.append(bp[list(REST)])
    if ti==0:near(label+':occupied_initial',na,a,5e-10)
    sf.append({'c':c,'I':ic,'n':nc,'H':energy[:,:,None]*c,'e':energy,'info':md});frames+=1
   common.append(np.array(clock));channel_values=[]
   for rowi,(ti,si) in enumerate(TP):
    ACTIVE={'preparation':name,'channel':ch['channel'],'target_time_index':ti,'source_time_index':si};label=name+'/'+ch['channel']+'/'+str(ti)+'_'+str(si);r=ch['rows'][rowi];f,g=sf[ti],sf[si];delta=float(Fraction(TIMES[ti])-Fraction(TIMES[si]));phase=np.exp(-1j*energy*delta)
    check(label+':pair_census',r['preparation']==name and r['channel']==ch['channel'] and r['target_time_index']==ti and r['source_time_index']==si and r['target_x_rational']==TIMES[ti] and r['source_x_rational']==TIMES[si]);check(label+':row_commit',read(CP/(name+'_'+ch['channel']+f'_pair{ti}_{si}.json'))==r)
    check(label+':pair_input_identity',r['input_map_sha256']==input_id)
    check(label+':baseline_metadata',r['target_baseline']=={k:f['info'][k] for k in r['target_baseline']} and r['source_baseline']=={k:g['info'][k] for k in r['source_baseline']})
    chi={k:-2*inner(f[k],g['I'],phase).imag for k in ('I','n','H')}
    # Independent exact boundary oracle. The producer integrates current via spectral sinc divided differences.
    boundary=f['n']-g['n']*phase[:,:,None];integral={k:-2*inner(f[k],boundary).imag for k in ('I','n','H')}
    cur=2*inner(f['I'],g['n'],phase).imag;charge=2*inner(f['n'],g['n'],phase).imag;contact=-f['info']['baseline_K'];econtact=-f['info']['baseline_I']
    vv={'chi_II':chi['I'],'chi_nI':chi['n'],'chi_HI_unperturbed':chi['H'],'integrated_chi_II':integral['I'],'integrated_chi_nI':integral['n'],'integrated_chi_HI_unperturbed':integral['H'],'current_direct_contact':contact,'complete_current_step_response':integral['I']+contact,'energy_direct_contact':econtact,'inclusive_switched_energy_step_work':integral['H']+econtact,'current_boundary_response':cur,'charge_boundary_response':charge}
    for key,value in vv.items():near(label+':'+key,value,r['values'][key],1e-8)
    near(label+':current_contact_boundary',vv['complete_current_step_response'],cur,1e-8);near(label+':charge_boundary',integral['n'],charge,1e-8);near(label+':energy_impulse',chi['H'],g['info']['baseline_I_dot'],1e-8);near(label+':energy_work',vv['inclusive_switched_energy_step_work'],-g['info']['baseline_I'],1e-8)
    if ti==si:near(label+':equal_current',chi['I'],0);near(label+':equal_charge_contact',chi['n'],contact);near(label+':equal_integral',boundary,0,1e-8)
    if si==0:near(label+':initial_occupied_current_null',vv['complete_current_step_response'],0,1e-8);near(label+':initial_occupied_charge_null',integral['n'],0,1e-8)
    channel_values.append(vv);rows+=1
   values.append(channel_values)
  for c in common[1:]:near(name+':six_common_clock_alignment',c,common[0],5e-10)
  check(name+':ten_contrasts',len(p['signed_four_channel_contrasts'])==10)
  for k,(ti,si) in enumerate(TP):
   cr=p['signed_four_channel_contrasts'][k];check(name+':contrast_time_census',cr['target_time_index']==ti and cr['source_time_index']==si)
   for key in values[0][k]:
    v=[c[k][key] for c in values];dd=(v[0]-v[1])-(v[2]-v[3]);vv={'source_presence_retained':v[0]-v[1],'source_presence_transferred':v[2]-v[3],'retained_minus_transferred_on':v[0]-v[2],'retained_minus_transferred_reference':v[1]-v[3],'difference_of_differences':dd}
    for ck,value in vv.items():near(name+':'+ck+':'+key,value,cr[ck][key],1e-8)
   signed.append({'preparation':name,'target_time_index':ti,'source_time_index':si,'record_DD_current_step':(values[0][k]['complete_current_step_response']-values[1][k]['complete_current_step_response'])-(values[2][k]['complete_current_step_response']-values[3][k]['complete_current_step_response'])})
  if pi%13==12:print(json.dumps({'preparations':pi+1,'source_frames':frames,'audited_pairs':rows,'assertions':N,'failed':len(FAIL)}),flush=True)
 check('full_census',rows==4160 and frames==1664)
 for f,h in INPUTS.items():check('unchanged:'+f,sha(ROOT/f)==h)
 out={'audit_status':'PASS' if not FAIL else 'FAILED','assertions':N,'failed_assertions':len(FAIL),'failures':FAIL,'maximum_absolute_errors':safe(MAX),'audited_preparations':104,'audited_source_frames':frames,'audited_channel_time_rows':rows,'result_raw_sha256':receipt['result_raw_sha256'],'receipt_sha256':sha(J/(NAME+'_RECEIPT.json')),'audit_script_sha256':sha(Path(__file__)),'input_sha256':INPUTS,'elapsed_seconds':time.monotonic()-START,'signed_current_DD':signed,'method':'Independent physical I/n/H source coefficient contractions and exact n-boundary integration oracle; no producer imports, eigensolver, sampler, RNG, time quadrature or baseline history propagation.'}
 write(AUDIT,out)
 text='# Independent prepared incidence response audit\n\n'+out['audit_status']+f': {N:,} assertions, {len(FAIL)} failed;104 preparations,1664 source frames and4160 ordered channel/time rows.\n\nAll signed impulses, contacts, inclusive work, occupied-initial step nulls and four-channel contrasts retained. Source current integral audited using the exact boundary identity independently of producer divided differences.\n\nAudit JSON SHA256: '+sha(AUDIT)+'\nParent raw SHA256: '+receipt['result_raw_sha256']+'\nParent receipt SHA256: '+sha(J/(NAME+'_RECEIPT.json'))+'\n'
 with REPORT.open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
 print(json.dumps({'audit_status':out['audit_status'],'assertions':N,'failed_assertions':len(FAIL),'json_sha256':sha(AUDIT),'md_sha256':sha(REPORT)}),flush=True)
 if FAIL:raise SystemExit(3)
if __name__=='__main__':
 try:main()
 except Exception as error:
  if not ERROR.exists():write(ERROR,{'error':repr(error),'traceback':traceback.format_exc(),'active':ACTIVE,'assertions':N,'failures':FAIL,'input_sha256':INPUTS,'audit_script_sha256':sha(Path(__file__))})
  raise
