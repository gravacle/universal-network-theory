"""Guarded saved-only audit/recovery loader; no producer/operator reconstruction."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
PARENT='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002'
ORIGINAL_PARENT='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001'
STEM='OBSERVER_SAVED_CANONICAL_NODAL_METRIC_RATE_SOLVE_V002_AUDIT'
AUTHOR_DRAFT=False
RESULT_SHA='6759a9c44574bfd75865d1867c4467df18deca79a162979b89f1546ba9e417b7'
ERROR_SHA=None
RECEIPT_SHA='2b6603b36ef3596c419d76e2ce82ac9c50dae31d150fb850f2d4179a56e3ff70'
EXPECTED_PID=41181
SOURCE_SHA='f662ade49c204ba116049fa7de6b303575ef219dc8dd6313df5c3fbd453b6ea0'
PROTOCOL_SHA='0128d1613b8f43f8dce40ed5cb2c5a72b974104da3e838deff6cfec4345b0465'
REVIEWED_ANCESTOR=('authoring_observer_saved_canonical_nodal_metric_rate_solve_v002_audit_292_aa0a1597.py','aa0a1597b56995cf8f33bc9d132cd7d5c287502b56b789bf8a8ff735d9db9403')
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
 assert owner['source_sha256']==SOURCE_SHA and sha(BASE/'cross_u_canonical_nodal_metric_rate_solve_v002.py')==SOURCE_SHA
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
 if kind=='exact_saved_600_iterate_original_targets_and_rows':return True
 if kind in ('shifted_residual_correction_against_original_rows','separate_disclosed_trace_preparation_after_canonical_admission'):return True
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
  suffix='trace_preparation_metric_change_plus_original_residual_equals_minus_CTlambda_actual'
  prefixes=[n[:-len('_actual')] for n in a if n.startswith('control_') and n.endswith(suffix)]
  assert len(prefixes)==1,'Unique saved reaction-control operands required'
  prefix=prefixes[0];actual=a[prefix+'_actual'];expected=a[prefix+'_expected'];envelope=a[prefix+'_envelope']
  assert np.all(envelope>=0);envelope=np.maximum(envelope,1e-30)
  same(a['new_Pm'],targets['cm']+actionfields[1]-a['trace_reaction'],stage+' affine metric momentum with separate reaction',envelope)
  same(actual,a['metric_momentum_change']+a[stage+'_momentum_change_original_metric_residual'],stage+' saved reaction actual origin',envelope)
  same(expected,-a['trace_reaction'],stage+' saved reaction expected origin',envelope)
  same(actual,expected,stage+' finite-residual reaction identity with admitted operation bound',envelope)
 else:same(a['new_Pm'],targets['cm']+actionfields[1],stage+' affine metric momentum',abs(a['new_Pm'])+abs(targets['cm'])+abs(actionfields[1]))
 return dict(stage=stage,canonical_rows_admitted=md['canonical_rows_admitted'],weak_CMC_admitted=md['trace_row_admitted'],original_ratios=calculated.tolist(),trace_ratios=trace_ratio.tolist(),native_target_change_norm=norm(a['new_Pn']-a['current_Pn']),metric_target_change_norm=norm(a['metric_momentum_change']),trace_gap_norm=norm(a['trace_gap']),solver_reason=md['solver_reason'],physical_Cauchy_adoption=False)


def pack(v,k,lam=None):
 nm=np.ones((3,87,45),dtype=bool);nm[:,0]=False;nm[1,:,0]=False
 mm=np.ones((6,87,45),dtype=bool);mm[:,0]=False;mm[3:5,:,0]=False
 sm=np.ones((87,45),dtype=bool);sm[0]=False
 parts=[v[np.broadcast_to(nm,v.shape)],k[mm]]
 if lam is not None:parts.append(lam[sm])
 return np.concatenate(parts)


def original_control_origin(doc,seen):
 oldpath=BASE/(ORIGINAL_PARENT+'_RESULT.json');oldreceipt=BASE/(ORIGINAL_PARENT+'_RECEIPT.json')
 assert sha(oldpath)=='efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82'
 assert sha(oldreceipt)=='8f306769022830cb0762e735308f493b072b58320fbdffabf46898c5a180f473'
 old=json.loads(oldpath.read_text());rc=json.loads(oldreceipt.read_text())
 assert rc['status']=='CLOSED' and rc['owner']['pid']==39611 and old['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED'
 assert len(old['checkpoints'])==25 and len(old['controls'])==17
 assert doc['controls'][:17]==old['controls'] and all(c['passed'] for c in old['controls'])
 if 'parent_result_sha256' in doc:assert doc['parent_result_sha256']=='efffd53fc12abd68daf723a418de8c58b05374e5ad117c260ad2cbde73fbae82'
 if 'reused_control_count' in doc:assert doc['reused_control_count']==17
 for rec in old['checkpoints']:
  assert sha(path(rec['file']))==rec['sha256'] and sha(path(rec['commit_file']))==rec['commit_sha256']
  assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
  if any(n.startswith('control_') for n in rec['metadata']['schema']):controls_in(pair(rec),old['controls'],seen)
 return old


def origin_arrays(rec,names):
 assert sha(path(rec['file']))==rec['sha256'] and sha(path(rec['commit_file']))==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={}
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata']
  for n in names:
   a=f[n];s=rec['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a))
   out[n]=a.copy()
 return out


def recovered_origin(a,md,old):
 refs=[{n:r[n] for n in ('file','sha256','commit_file','commit_sha256')} for r in old['checkpoints']]
 assert md['reused_checkpoint_refs']==refs and md['reused_controls']==old['controls']
 assert md['original_nonadmission_preserved'] is True and md['temporal_or_physical_state_changed'] is False
 oldsol=old['case']['compatibility'];oldarrays=origin_arrays(oldsol,('compatibility_original_iterate','compatibility_original_residual','compatibility_original_action','canonical_original_ratios','compatibility_native_original_rhs','compatibility_metric_original_rhs'))
 for new,previous in (('original_iterate','compatibility_original_iterate'),('original_residual','compatibility_original_residual'),('original_action','compatibility_original_action'),('original_ratios','canonical_original_ratios')):exact(a[new],oldarrays[previous],'recovered exact '+new)
 exact(a['original_rhs'],pack(oldarrays['compatibility_native_original_rhs'],oldarrays['compatibility_metric_original_rhs']),'recovered original packed rhs')
 previous_basis=origin_arrays(md['basis_ref'],('native_scale','metric_scale','scalar_scale'))
 previous_affine=origin_arrays(md['affine_ref'],('Pn','Pm','cn','cm','trace_rhs'))
 for n in previous_basis:exact(a[n],previous_basis[n],'recovered unchanged '+n)
 for new,previous in (('current_Pn','Pn'),('current_Pm','Pm'),('native_affine','cn'),('metric_affine','cm'),('trace_rhs','trace_rhs')):exact(a[new],previous_affine[previous],'recovered exact '+new)
 return previous_basis,previous_affine


def cycle_products(a,md,basis,targets,previous,checks):
 stage=md['stage'];constrained=stage.startswith('trace_preparation')
 key=lambda suffix:a[stage+'_'+suffix]
 exact(key('base_iterate'),previous['iterate'],stage+' saved restart base')
 exact(key('correction_rhs'),previous['residual'],stage+' saved restart residual')
 exact(key('base_original_action'),previous['action'],stage+' saved restart action')
 exact(key('original_rhs'),previous['rhs'],stage+' original rhs unchanged')
 same(key('updated_iterate'),key('base_iterate')+key('correction'),stage+' shifted update',abs(key('updated_iterate'))+abs(key('base_iterate'))+abs(key('correction')))
 same(key('original_residual'),key('original_rhs')-key('original_action'),stage+' fresh original residual',abs(key('original_rhs'))+abs(key('original_action'))+abs(key('original_residual')))
 same(key('residual_update_prediction'),key('correction_rhs')-key('correction_action'),stage+' residual update prediction',abs(key('correction_rhs'))+abs(key('correction_action'))+abs(key('residual_update_prediction')))
 same(key('residual_update_defect'),key('original_residual')-key('residual_update_prediction'),stage+' raw update defect',abs(key('original_residual'))+abs(key('residual_update_prediction'))+abs(key('residual_update_defect')))
 bound=key('residual_update_operation_envelope');assert np.all(bound>=0)
 # Check the saved positive envelope covers the already saved action terms;
 # constructing either coupled action envelope here would replay the operator.
 minimum=abs(key('original_rhs'))+abs(key('correction_rhs'))+2*abs(key('correction_action'))+abs(key('original_residual'))+abs(key('base_original_action'))
 dominance=float(np.max(np.maximum(minimum-bound,0)/np.maximum(minimum+bound,1e-300),initial=0));assert dominance<=2e-11
 c=next(c for c in checks if c['name']==stage+'_fresh_original_residual_update_identity')
 error=float(np.max(abs(key('residual_update_defect'))/np.maximum(bound,1e-30),initial=0));same(np.array(error),np.array(c['error']),stage+' independently stored update-gate ratio')
 assert c['passed']==(error<=2e-11) and c['tolerance']==2e-11
 raw=a[stage+'_original_residual'];rhs=unpack(a[stage+'_original_rhs'],constrained);res=unpack(raw,constrained);calculated=[]
 scales=[basis['native_scale'],basis['metric_scale'],basis['scalar_scale']]
 for i,(name,r,rh) in enumerate(zip(('native','metric','trace'),res,rhs)):
  exact(r,key(name+'_original_residual'),stage+' packed '+name+' residual')
  exact(rh,key(name+'_original_rhs'),stage+' packed '+name+' rhs')
  ra=ratios(r,rh,scales[i]);same(ra,key(name+'_original_ratios'),stage+' '+name+' original rhs ratios');calculated.append(ra)
  if i<2:
   ra=ratios(r,targets['Pn' if i==0 else 'Pm'],scales[i]);same(ra,key(name+'_actual_target_ratios'),stage+' '+name+' actual-target ratios');calculated.append(ra)
 admitted=bool(np.all(np.stack(calculated)<=1e-10));assert admitted==md['canonical_rows_admitted']
 assert md['original_rhs_and_actual_targets_unchanged'] is True and md['correction_rhs_is_saved_previous_residual'] is True and md['physical_Cauchy_adoption'] is False
 nextbase=dict(iterate=key('updated_iterate'),residual=key('original_residual'),action=key('original_action'),rhs=key('original_rhs'))
 report=dict(stage=stage,cycle=md['cycle'],original_ratios=np.stack(calculated).tolist(),original_rows_admitted=admitted,update_error=error,saved_operation_bound_dominance_gap=dominance,update_defect_norm=norm(key('residual_update_defect')),correction_norm=norm(key('correction')),solver_reason=md['solver_reason'])
 return nextbase,report


def main():
 global np
 ap=argparse.ArgumentParser();ap.add_argument('--root-audit',action='store_true');args=ap.parse_args()
 assert args.root_audit and not AUTHOR_DRAFT and SOURCE_SHA and PROTOCOL_SHA,'Held future-bound saved-only auditor; no operator/solve replay'
 assert sha(BASE/REVIEWED_ANCESTOR[0])==REVIEWED_ANCESTOR[1]
 assert not list(BASE.glob(STEM+'_*.json'));started=datetime.now(timezone.utc).isoformat();selfhash=sha(__file__)
 rc,doc,records,terminal_name,terminal_hash=admit_terminal()
 import numpy as np_local
 np=np_local;checks=doc['controls'];seen={};old=original_control_origin(doc,seen)
 basis=targets=base=None;solutions=[];summaries=[];cycles=[];kinds=[];previous={}
 assert [c['ordinal'] for c in checks]==list(range(len(checks)))
 try:
  for rec in records:
   md=rec['metadata'];kind=md['kind'];a=pair(rec);controls_in(a,checks,seen);kinds.append(kind)
   if kind=='exact_saved_600_iterate_original_targets_and_rows':
    basis,targets=recovered_origin(a,md,old);base=a
    previous['compatibility']=dict(iterate=a['original_iterate'],residual=a['original_residual'],action=a['original_action'],rhs=a['original_rhs'])
   elif kind=='separate_disclosed_trace_preparation_after_canonical_admission':
    assert summaries and summaries[0]['canonical_rows_admitted'] and summaries[0]['weak_CMC_admitted'] is False
    same(a['original_residual'],a['original_rhs']-a['original_action'],'trace initial residual',abs(a['original_rhs'])+abs(a['original_action'])+abs(a['original_residual']))
    original=unpack(base['original_rhs']);tr=unpack(a['original_rhs'],True)
    exact(tr[0],original[0],'trace preparation native original rhs');exact(tr[1],original[1],'trace preparation metric original rhs');exact(tr[2],targets['trace_rhs'],'trace preparation original trace rhs')
    assert np.all(unpack(a['seed'],True)[2]==0)
    previous['trace_preparation']=dict(iterate=a['seed'],residual=a['original_residual'],action=a['original_action'],rhs=a['original_rhs'])
   elif kind=='shifted_residual_correction_against_original_rows':
    prefix='trace_preparation' if md['stage'].startswith('trace_preparation') else 'compatibility'
    assert basis is not None and prefix in previous
    previous[prefix],report=cycle_products(a,md,basis,targets,previous[prefix],checks);cycles.append(report)
   elif kind in ('actual_canonical_compatibility_test','trace_constrained_preparation'):
    assert basis is not None;solutions.append((a,md))
    summaries=[audit_solution(x,m,basis,targets) for x,m in solutions]
  assert set(seen)=={c['ordinal'] for c in checks},'Original17 paired operands and all new raw operands required'
  summaries=[audit_solution(a,md,basis,targets) for a,md in solutions]
  if rc['status']=='CLOSED':
   prep=doc['case'].get('trace_preparation');assert len(checks)==18+len(cycles)+(1 if prep is not None else 0) and all(c['passed'] for c in checks)
   assert len(summaries)==1+(1 if prep is not None else 0) and doc['case']['parent_nonadmission_preserved'] is True
   if doc['status']=='ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED':assert summaries[0]['canonical_rows_admitted'] is False and prep is None
   if doc['status']=='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE':assert all(summaries[0][n] for n in ('canonical_rows_admitted','weak_CMC_admitted')) and prep is None
   if doc['status']=='DISCLOSED_TRACE_PREPARATION_ADMITTED':assert summaries[0]['canonical_rows_admitted'] and summaries[0]['weak_CMC_admitted'] is False and all(summaries[-1][n] for n in ('canonical_rows_admitted','weak_CMC_admitted'))
  else:assert ERROR_SHA and doc['status']=='FAILED'
  for mapping in (rc['input_sha256'],rc['output_sha256']):
   for name,digest in mapping.items():assert sha(path(name))==digest,('closing actual binding',name)
  assert sha(__file__)==selfhash and sha(BASE/terminal_name)==terminal_hash and sha(BASE/(PARENT+'_RECEIPT.json'))==RECEIPT_SHA
  report=dict(status='SAVED_ONLY_CORRECTION_AUDIT_PASS',parent_terminal_status=rc['status'],parent_result_status=doc.get('case',{}).get('status'),parent_result_sha256=RESULT_SHA,parent_error_sha256=ERROR_SHA,parent_receipt_sha256=RECEIPT_SHA,parent_owner_pid=EXPECTED_PID,audit_source_sha256=selfhash,started=started,closed=datetime.now(timezone.utc).isoformat(),statistics=STAT,controls=len(checks),original17_exact=True,original_nonadmission_preserved=True,original_parent_status=old['status'],new_cycles=cycles,solutions=summaries,qualification=rc['qualification'],operator_replay=False,solve_replay=False,physical_curve_claim=False,pair_kinds=kinds)
  h=publish(STEM+'_RESULT.json',report);print(json.dumps(dict(status=report['status'],sha256=h,parent_status=report['parent_result_status'],controls=len(checks),cycles=len(cycles),solutions=summaries),separators=(',',':')))
 except BaseException:
  publish(STEM+'_ERROR.json',dict(status='AUDITOR_FAILURE',traceback=traceback.format_exc(),audit_source_sha256=selfhash,parent_receipt_sha256=RECEIPT_SHA,statistics=STAT));raise

if __name__=='__main__':main()
