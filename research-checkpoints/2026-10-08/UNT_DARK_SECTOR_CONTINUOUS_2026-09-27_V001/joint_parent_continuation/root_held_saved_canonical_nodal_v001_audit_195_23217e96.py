"""Guarded saved-only audit/recovery loader; no producer/operator reconstruction."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
PARENT='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001'
STEM='OBSERVER_SAVED_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_AUDIT'
AUTHOR_DRAFT=True
RESULT_SHA='efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82'
ERROR_SHA=None
RECEIPT_SHA='8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473'
EXPECTED_PID=39611
SOURCE_SHA='f84b8a9bea9d45ac1370985401172621d93d59dc814bedda785206188b3c2c4b'
PROTOCOL_SHA='426cc5a3c12cce7557118903379bfc69e2d1afa935cc76a3bb315e8e2598beea'
np=None
STAT=dict(comparisons=0,max_scaled_gap=0.,pairs=0,numeric_arrays=0,numeric_entries=0,nonfinite_entries=0)

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p

def same(a,b,label,envelope=None):
 a=np.asarray(a);b=np.asarray(b);assert a.shape==b.shape,label
 assert np.all(np.isfinite(a)) and np.all(np.isfinite(b)),label
 e=abs(a)+abs(b) if envelope is None else np.asarray(envelope)
 assert e.shape==a.shape and np.all(np.isfinite(e)) and np.all(e>=0),label
 gap=float(np.max(abs(a-b)/np.maximum(e,1e-300),initial=0))
 STAT['comparisons']+=a.size;STAT['max_scaled_gap']=max(STAT['max_scaled_gap'],gap)
 assert gap<=2e-11,(label,gap)

def exact(a,b,label):
 assert a.shape==b.shape and a.dtype==b.dtype and np.array_equal(a,b,equal_nan=True),label
 STAT['comparisons']+=a.size

def norm(a):
 a=np.asarray(a);return float(np.sqrt(np.sum(a*a)))

def ratios(res,rhs,scale):
 r=norm(res);d=norm(rhs);wr=norm(res/scale);wd=norm(rhs/scale)
 if d==0:return np.array((0.,0.)) if r==wr==0 else np.array((math.inf,math.inf))
 assert wd>0;return np.array((r/d,wr/wd))

def publish(n,obj):
 raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();p=BASE/n
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;return sha(p)

def admit_terminal():
 assert RECEIPT_SHA and EXPECTED_PID and (RESULT_SHA is None)!=(ERROR_SHA is None)
 rcpath=BASE/(PARENT+'_RECEIPT.json');assert sha(rcpath)==RECEIPT_SHA
 rc=json.loads(rcpath.read_text());assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 owner=rc['owner'];assert owner['owner']=='root' and owner['pid']==EXPECTED_PID and rc['closed']>owner['started']
 assert owner['source_sha256']==SOURCE_SHA and sha(BASE/'cross_u_canonical_nodal_metric_rate_solve_v001.py')==SOURCE_SHA
 assert sha(BASE/(PARENT+'.md'))==PROTOCOL_SHA and all(v is False for v in rc['qualification'].values())
 n=PARENT+('_RESULT.json' if rc['status']=='CLOSED' else '_ERROR.json')
 h=RESULT_SHA if rc['status']=='CLOSED' else ERROR_SHA
 assert h and rc['result_sha256' if rc['status']=='CLOSED' else 'error_sha256']==h and sha(BASE/n)==h
 doc=json.loads((BASE/n).read_text());assert doc['owner']==owner
 assert all(v is False for v in doc['qualification'].values())
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for name,digest in mapping.items():assert sha(path(name))==digest,('changed actual binding',name)
 records=doc['checkpoints']
 assert {p.name for p in BASE.glob(PARENT+'_*.npz')}=={r['file'] for r in records}
 assert {p.name for p in BASE.glob(PARENT+'_*.npz.COMMIT.json')}=={r['commit_file'] for r in records}
 for rec in records:
  assert rc['output_sha256'][rec['file']]==rec['sha256'] and rc['output_sha256'][rec['commit_file']]==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
  assert rec['metadata']['owner']==owner and all(v is False for v in rec['metadata']['qualification'].values())
 return rc,doc,records,n,h

def wanted(name,kind):
 if name.startswith('control_'):return True
 if kind=='unchanged_E_F_S_bases_and_positive_solver_congruences':return name in ('native_scale','metric_scale','scalar_scale')
 if kind=='actual_current_weak_targets_and_owned_H_trace_rhs':return name in ('Pn','Pm','cn','cm','trace_rhs')
 if kind in ('actual_canonical_compatibility_test','trace_constrained_preparation'):
  return name in ('native_nodal_rate','metric_nodal_rate','current_Pn','current_Pm','new_Pn','new_Pm','metric_momentum_change','trace_original_action','trace_rhs','trace_gap','trace_original_ratios','canonical_original_ratios','trace_multiplier','trace_reaction') or name.endswith(('_original_action','_original_residual','_original_rhs','_original_ratios','_actual_target_ratios','_trace_compatibility_ratios','_momentum_change_original_metric_residual'))
 if kind=='signed_action_adjoint_and_trace_full_rank_restriction':return name in ('operator_metric_test','operator_scalar_test','trace_forward_test','trace_adjoint_test','scalar_C_positive_restriction_weight','cell_Q1_value_determinants')
 return False

def pair(rec):
 out={};md=rec['metadata'];kind=md['kind']
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(md['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==md
  for name,spec in md['schema'].items():
   a=f[name];assert list(a.shape)==spec['shape'] and str(a.dtype)==spec['dtype'],(rec['file'],name)
   assert a.dtype.kind in 'fiub';bad=int(np.count_nonzero(~np.isfinite(a)))
   assert (bad==0)==spec['finite'] and (md['failed'] or bad==0),(rec['file'],name)
   STAT['numeric_arrays']+=1;STAT['numeric_entries']+=a.size;STAT['nonfinite_entries']+=bad
   if wanted(name,kind):out[name]=a.copy()
 STAT['pairs']+=1;return out

def controls_in(a,checks,seen):
 for c in checks:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=[prefix+s for s in ('actual','expected','envelope')]
  if not all(n in a for n in names):continue
  x,y,e=(a[n] for n in names);assert x.shape==y.shape==e.shape and np.all(e>=0)
  error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0))
  same(np.array(error),np.array(c['error']),prefix+'saved componentwise ratio')
  assert c['tolerance']==2e-11 and c['passed']==(error<=2e-11)
  if c['ordinal'] in seen:
   for old,new in zip(seen[c['ordinal']],(x,y,e)):exact(old,new,prefix+'duplicate operands')
  else:seen[c['ordinal']]=(x.copy(),y.copy(),e.copy())

def unpack(packed,trace=False):
 nm=np.ones((3,87,45),dtype=bool);nm[:,0]=False;nm[1,:,0]=False
 mm=np.ones((6,87,45),dtype=bool);mm[:,0]=False;mm[3:5,:,0]=False
 sm=np.ones((87,45),dtype=bool);sm[0]=False
 v=np.zeros((33,3,87,45));k=np.zeros((6,87,45));m=np.broadcast_to(nm,v.shape)
 assert int(m.sum())==380292 and int(mm.sum())==23048 and int(sm.sum())==3870
 assert packed.size==380292+23048+(3870 if trace else 0)
 v[m]=packed[:380292];k[mm]=packed[380292:403340]
 if not trace:return (v,k)
 lam=np.zeros((87,45));lam[sm]=packed[403340:];return (v,k,lam)

def audit_solution(a,md,basis,targets):
 constrained=md['kind']=='trace_constrained_preparation';stage='trace_preparation' if constrained else 'compatibility'
 scale=[basis['native_scale'],basis['metric_scale'],basis['scalar_scale']]
 same(a['trace_gap'],a['trace_original_action']-a['trace_rhs'],stage+' trace gap',abs(a['trace_original_action'])+abs(a['trace_rhs'])+abs(a['trace_gap']))
 same(a['trace_rhs'],targets['trace_rhs'],stage+' unchanged trace target')
 same(a['metric_momentum_change'],a['new_Pm']-a['current_Pm'],stage+' actual canonical change',abs(a['new_Pm'])+abs(a['current_Pm'])+abs(a['metric_momentum_change']))
 exact(a['current_Pn'],targets['Pn'],stage+' current native target')
 exact(a['current_Pm'],targets['Pm'],stage+' current metric target')
 trace_ratio=ratios(a['trace_gap'],a['trace_rhs'],scale[2]);same(trace_ratio,a['trace_original_ratios'],stage+' trace ratios')
 assert md['trace_row_admitted']==bool(np.all(trace_ratio<=1e-10))
 res=a[stage+'_original_residual'];rhsfields=tuple(a[stage+'_'+n+'_original_rhs'] for n in ('native','metric','trace')[:3 if constrained else 2])
 # Stored packed action/residual is checked against independently packed nodal rhs.
 nm=np.ones((3,87,45),dtype=bool);nm[:,0]=False;nm[1,:,0]=False
 mm=np.ones((6,87,45),dtype=bool);mm[:,0]=False;mm[3:5,:,0]=False
 sm=np.ones((87,45),dtype=bool);sm[0]=False
 parts=[rhsfields[0][np.broadcast_to(nm,rhsfields[0].shape)],rhsfields[1][mm]]
 if constrained:parts.append(rhsfields[2][sm])
 packedrhs=np.concatenate(parts)
 same(res,packedrhs-a[stage+'_original_action'],stage+' original linear residual',abs(packedrhs)+abs(a[stage+'_original_action'])+abs(res))
 rf=unpack(res,constrained);calculated=[]
 for i,(name,rhsfield,rr) in enumerate(zip(('native','metric','trace'),rhsfields,rf)):
  exact(rr,a[stage+'_'+name+'_original_residual'],stage+' packed '+name+' residual')
  ratio=ratios(rr,rhsfield,scale[i]);same(ratio,a[stage+'_'+name+'_original_ratios'],stage+' '+name+' rhs ratios');calculated.append(ratio)
  if i<2:
   actual=ratios(rr,targets['Pn' if i==0 else 'Pm'],scale[i]);same(actual,a[stage+'_'+name+'_actual_target_ratios'],stage+' '+name+' actual-target ratios');calculated.append(actual)
 calculated=np.stack(calculated);same(calculated,a['canonical_original_ratios'],stage+' complete independent ratios')
 assert md['canonical_rows_admitted']==bool(np.all(calculated<=1e-10))
 actionfields=unpack(a[stage+'_original_action'],constrained)
 same(a['new_Pn'],targets['cn']+actionfields[0],stage+' affine native momentum',abs(a['new_Pn'])+abs(targets['cn'])+abs(actionfields[0]))
 if constrained:
  same(a['new_Pm'],targets['cm']+actionfields[1]-a['trace_reaction'],stage+' affine metric momentum with separate reaction',abs(a['new_Pm'])+abs(targets['cm'])+abs(actionfields[1])+abs(a['trace_reaction']))
  same(a['metric_momentum_change']+a[stage+'_momentum_change_original_metric_residual'],-a['trace_reaction'],stage+' finite-residual reaction identity',abs(a['new_Pm'])+abs(a['current_Pm'])+abs(a[stage+'_momentum_change_original_metric_residual'])+abs(a['trace_reaction']))
 else:same(a['new_Pm'],targets['cm']+actionfields[1],stage+' affine metric momentum',abs(a['new_Pm'])+abs(targets['cm'])+abs(actionfields[1]))
 return dict(stage=stage,canonical_rows_admitted=md['canonical_rows_admitted'],weak_CMC_admitted=md['trace_row_admitted'],original_ratios=calculated.tolist(),trace_ratios=trace_ratio.tolist(),native_target_change_norm=norm(a['new_Pn']-a['current_Pn']),metric_target_change_norm=norm(a['metric_momentum_change']),trace_gap_norm=norm(a['trace_gap']),solver_reason=md['solver_reason'],physical_Cauchy_adoption=False)

def main():
 global np
 ap=argparse.ArgumentParser();ap.add_argument('--root-audit',action='store_true');args=ap.parse_args()
 assert args.root_audit and not AUTHOR_DRAFT,'Held saved-only auditor; bind CLOSED seals and root release first'
 assert not list(BASE.glob(STEM+'_*.json'));started=datetime.now(timezone.utc).isoformat();selfhash=sha(__file__)
 rc,doc,records,terminal_name,terminal_hash=admit_terminal()
 import numpy as np_local
 np=np_local;checks=doc['controls'];seen={};basis=targets=None;solutions=[];summaries=[];kinds=[]
 assert [c['ordinal'] for c in checks]==list(range(len(checks)))
 try:
  for rec in records:
   kind=rec['metadata']['kind'];a=pair(rec);controls_in(a,checks,seen);kinds.append(kind)
   if kind=='unchanged_E_F_S_bases_and_positive_solver_congruences':
    basis=a;assert all(np.all(a[n]>0) for n in ('native_scale','metric_scale','scalar_scale'))
   elif kind=='actual_current_weak_targets_and_owned_H_trace_rhs':targets=a
   elif kind in ('actual_canonical_compatibility_test','trace_constrained_preparation'):
    assert basis is not None and targets is not None;solutions.append((a,rec['metadata']))
   elif kind=='signed_action_adjoint_and_trace_full_rank_restriction':
    assert np.all(a['scalar_C_positive_restriction_weight']>0) and np.all(a['cell_Q1_value_determinants']!=0)
    left=np.sum(a['operator_scalar_test']*a['trace_forward_test']);right=np.sum(a['operator_metric_test']*a['trace_adjoint_test'])
    c=next(c for c in checks if c['name']=='trace_original_weak_adjoint');prefix='control_%03d_%s_'%(c['ordinal'],c['name'])
    same(np.array((left,)),a[prefix+'actual'],'saved trace contraction left');same(np.array((right,)),a[prefix+'expected'],'saved trace contraction right')
  assert set(seen)=={c['ordinal'] for c in checks},'Every recorded control needs complete raw operands'
  for a,md in solutions:summaries.append(audit_solution(a,md,basis,targets))
  if rc['status']=='CLOSED':
   assert len(checks)==17+(1 if doc['case'].get('trace_preparation') is not None else 0) and all(c['passed'] for c in checks)
   assert len(summaries)==1+(1 if doc['case'].get('trace_preparation') is not None else 0)
   assert doc['status']==doc['case']['status']
   if doc['status']=='DISCLOSED_TRACE_PREPARATION_ADMITTED':assert all(summaries[-1][k] for k in ('canonical_rows_admitted','weak_CMC_admitted')) and summaries[0]['weak_CMC_admitted'] is False
   if doc['status']=='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE':assert all(summaries[0][k] for k in ('canonical_rows_admitted','weak_CMC_admitted'))
  else:assert ERROR_SHA and doc['status']=='FAILED'
  for mapping in (rc['input_sha256'],rc['output_sha256']):
   for name,digest in mapping.items():assert sha(path(name))==digest,('closing actual binding',name)
  assert sha(__file__)==selfhash and sha(BASE/terminal_name)==terminal_hash and sha(BASE/(PARENT+'_RECEIPT.json'))==RECEIPT_SHA
  summary=dict(status='SAVED_ONLY_AUDIT_PASS',parent_terminal_status=rc['status'],parent_result_status=doc.get('case',{}).get('status'),parent_result_sha256=RESULT_SHA,parent_error_sha256=ERROR_SHA,parent_receipt_sha256=RECEIPT_SHA,parent_owner_pid=EXPECTED_PID,started=started,closed=datetime.now(timezone.utc).isoformat(),audit_source_sha256=selfhash,input_bindings=len(rc['input_sha256']),output_bindings=len(rc['output_sha256']),controls=len(checks),passed_controls=sum(c['passed'] for c in checks),pair_kinds=kinds,statistics=STAT,solutions=summaries,qualification=rc['qualification'],operator_replay=False,solve_replay=False,physical_curve_claim=False,recovery_scope='Exact existing pairs and raw operands only; no iteration or operator reconstruction')
  h=publish(STEM+'_RESULT.json',summary);print(json.dumps(dict(status=summary['status'],sha256=h,controls=len(checks),pairs=STAT['pairs'],solutions=summaries),separators=(',',':')))
 except BaseException:
  failure=dict(status='AUDITOR_FAILURE',traceback=traceback.format_exc(),audit_source_sha256=selfhash,parent_receipt_sha256=RECEIPT_SHA,statistics=STAT)
  publish(STEM+'_ERROR.json',failure);raise

if __name__=='__main__':main()
