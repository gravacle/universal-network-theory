"""Guarded selected saved-word ties and certificates; no EFT/FE/operator replay."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='READONLY_DD_NODE_COORDINATE_WORDS_V001'
PARENT='CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='1a6e5ed45ce5238f995a8b2fb70416b55858c8d61e7f27ef3253f0c07def9219'
TERMINAL=dict(pid=47969,source_sha256='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',protocol_sha256='1f3c5afbb26dd9f43fcea053f92bfad073fdeb75221265d6212772125445e23e',result_sha256='6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc',receipt_sha256='a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d')
np=None;INPUTS={};IDENTITIES=[];SELECTED=dict(pairs=0,arrays=0,finite_entries=0)
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def bind(n,h):
 key=str(path(n).resolve());assert key not in INPUTS or INPUTS[key]==h
 assert sha(n)==h,n;INPUTS[key]=h
def publish(tag,obj):
 p=path(STEM+'_'+tag+'.json');raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
 with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 p.chmod(0o444);assert p.read_bytes()==raw;return sha(p)
def identity(label,a,b,e):
 a=np.asarray(a);b=np.asarray(b);e=np.asarray(e);assert a.shape==b.shape==e.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b)) and np.all(np.isfinite(e)) and np.all(e>=0)
 error=float(np.max(abs(a-b)/np.maximum(e,1e-30),initial=0));row=dict(name=label,error=error,tolerance=2e-11,passed=error<=2e-11);IDENTITIES.append(row);assert row['passed'],row
def value(d,p):return d[p+'_hi']+d[p+'_lo']
def bound(d,p):return abs(d[p+'_hi'])+abs(d[p+'_lo'])
def masks():
 n=np.ones((3,87,45),dtype=bool);n[:,0]=False;n[1,:,0]=False
 m=np.ones((6,87,45),dtype=bool);m[:,0]=False;m[3:5,:,0]=False
 return np.broadcast_to(n,(33,3,87,45)),m
def pack(v,k):
 n,m=masks();return np.concatenate((v[n],k[m]))
def fields(x):
 n,m=masks();assert x.shape==(403340,);v=np.zeros(n.shape);k=np.zeros(m.shape);v[n]=x[:380292];k[m]=x[380292:];return v,k
def ratios(r,t,s):
 den=float(np.linalg.norm(t));wd=float(np.linalg.norm(t/s));assert math.isfinite(den) and math.isfinite(wd) and den>0 and wd>0
 out=np.array((np.linalg.norm(r)/den,np.linalg.norm(r/s)/wd));assert np.all(np.isfinite(out));return out
def read(rec,keep):
 bind(rec['file'],rec['sha256']);bind(rec['commit_file'],rec['commit_sha256']);assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={}
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata'];SELECTED['pairs']+=1
  for k in rec['metadata']['schema']:
   if not keep(k):continue
   a=f[k].copy();s=rec['metadata']['schema'][k];assert s==dict(shape=list(a.shape),dtype=str(a.dtype),finite=True) and a.dtype.kind in 'fiu' and np.all(np.isfinite(a)),k
   SELECTED['arrays']+=1;SELECTED['finite_entries']+=a.size;out[k]=a
 return out
def admission():
 t=TERMINAL;assert all(v is not None for v in t.values()),'Actual natural CLOSED terminal required; no live reads'
 for n,h in ((PARENT+'_RESULT.json',t['result_sha256']),(PARENT+'_RECEIPT.json',t['receipt_sha256']),('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py',t['source_sha256']),(PARENT+'.md',t['protocol_sha256'])):bind(n,h)
 r=json.loads(path(PARENT+'_RESULT.json').read_text());rc=json.loads(path(PARENT+'_RECEIPT.json').read_text());case=r['case'];recs=r['checkpoints'];cycles=case['compatibility_corrections']
 assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and r['owner']['owner']=='root' and r['owner']['pid']==t['pid'] and r['owner']['source_sha256']==t['source_sha256'] and rc['closed']>r['owner']['started'] and rc['result_sha256']==t['result_sha256'] and rc['error_sha256'] is None
 assert r['qualification']==rc['qualification'] and len(r['qualification'])==7 and all(v is False for v in r['qualification'].values())
 assert r['status'] in ('CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE','ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED') and case['status']==r['status'] and case['trace_preparation'] is None and case['physical_adoption'] is False
 assert case['parent_nonadmission_preserved'] is True and case['no_extra_iteration_cap'] is True and case['targets_unchanged'] is True and case['precision']=='two_word_nodal_coordinates'
 assert len(cycles)<=3 and [c['cycle'] for c in cycles]==list(range(1,len(cycles)+1)) and all(c['cap']==160 for c in cycles)
 assert len(r['controls'])==3+len(cycles) and all(c['passed'] for c in r['controls'])
 assert len(recs)==5+len(cycles)+sum(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' for q in recs)+(case['rate_jets'] is not None)
 assert {p.name for p in BASE.glob(PARENT+'_*.npz')}=={q['file'] for q in recs} and {p.name for p in BASE.glob(PARENT+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in recs}
 for q in recs:assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256']
 return r

def audit(r):
 recs=r['checkpoints'];case=r['case']
 def one(kind):
  found=[q for q in recs if q['metadata']['kind']==kind];assert len(found)==1;return found[0]
 seed=one('disclosed_two_word_candidate_final_high_plus_actual_last_discarded_low');assert case['seed']==seed
 sd=read(seed,lambda n:n in ('seed_nodes_hi','seed_nodes_lo','original_rhs','current_Pn','current_Pm','rounded_global_cn','rounded_global_cm','weak_trace_rhs','native_scale','metric_scale','scalar_scale'))
 rhs=sd['original_rhs'];targets=(sd['current_Pn'],sd['current_Pm']);offsets=(sd['rounded_global_cn'],sd['rounded_global_cm']);scales=(sd['native_scale'],sd['metric_scale'],sd['scalar_scale']);previous=(sd['seed_nodes_hi'],sd['seed_nodes_lo'])
 assert np.array_equal(rhs,pack(targets[0]-offsets[0],targets[1]-offsets[1]))
 assert seed['metadata']['proof']['original_nonadmission_preserved'] is True and seed['metadata']['state_adopted'] is False and seed['metadata']['source_or_coefficients_changed'] is False
 prefix='initial_dd_nodes';initial=one('new_full_two_word_node_candidate_original_certificate');witness=read(initial,lambda n:n.startswith(prefix+'_'));previous_res=value(witness,prefix+'_residual')
 identity('initial_residual_frozen_rhs_minus_action',previous_res,rhs-value(witness,prefix+'_action'),abs(rhs)+bound(witness,prefix+'_action')+bound(witness,prefix+'_residual'))
 for rec in recs:
  if rec['metadata']['kind']!='bounded_float_correction_with_unrounded_two_word_node_certificate':continue
  label='cycle_%03d'%rec['metadata']['cycle'];assert rec['metadata']['cap']==160
  d=read(rec,lambda n:n.startswith(label+'_'));new=(d[label+'_final_update_updated_nodes_hi'],d[label+'_final_update_updated_nodes_lo']);q=d[label+'_final_update_exact_update_minus_two_word_nodes'];delta=d[label+'_completed_correction'];positive=d[label+'_uncancelled_bound_through_compression'];assert np.all(positive>=0)
  identity(label+'_node_update_disclosed_third_word',new[0]+new[1]+q,previous[0]+previous[1]+delta,abs(new[0])+abs(new[1])+abs(q)+abs(previous[0])+abs(previous[1])+abs(delta))
  identity(label+'_residual_frozen_rhs_minus_action',value(d,label+'_final_residual'),rhs-value(d,label+'_final_action'),abs(rhs)+bound(d,label+'_final_action')+bound(d,label+'_final_residual'))
  identity(label+'_saved_prediction',value(d,label+'_prediction'),previous_res-value(d,label+'_delta_action')+value(d,label+'_compression_defect_action'),positive+abs(previous_res)+bound(d,label+'_prediction')+bound(d,label+'_delta_action')+bound(d,label+'_compression_defect_action'))
  identity(label+'_saved_update_gap',value(d,label+'_final_residual')-value(d,label+'_prediction'),value(d,label+'_update_identity_gap'),positive+bound(d,label+'_final_residual')+bound(d,label+'_prediction')+bound(d,label+'_update_identity_gap'))
  identity(label+'_correction_rhs_collapse_defect',previous_res,d[label+'_correction_rhs_rounded_value']+value(d,label+'_rhs_rounding_defect'),abs(previous_res)+abs(d[label+'_correction_rhs_rounded_value'])+bound(d,label+'_rhs_rounding_defect'))
  if len(d[label+'_history']):assert d[label+'_history'][-1,0]<=160
  previous=new;previous_res=value(d,label+'_final_residual');witness=d;prefix=label+'_final'
 sol=case['compatibility'];assert sol in recs and sol['metadata']['kind']=='two_word_actual_canonical_compatibility_test';s=read(sol,lambda n:True)
 for word,index in (('hi',0),('lo',1)):
  assert np.array_equal(pack(s['native_nodal_rate_'+word],s['metric_nodal_rate_'+word]),previous[index])
  for name in ('action','residual'):assert np.array_equal(s['original_'+name+'_'+word],witness[prefix+'_'+name+'_'+word])
 assert np.array_equal(s['original_rhs'],rhs) and np.array_equal(s['current_Pn'],targets[0]) and np.array_equal(s['current_Pm'],targets[1]) and np.array_equal(s['trace_rhs'],sd['weak_trace_rhs'])
 identity('solution_residual_frozen_rhs_minus_action',value(s,'original_residual'),rhs-value(s,'original_action'),abs(rhs)+bound(s,'original_action')+bound(s,'original_residual'))
 act=fields(value(s,'original_action'));res=fields(value(s,'original_residual'))
 for j,name in enumerate(('native','metric')):
  actual=value(witness,prefix+'_'+name+'_actual_target_residual');moment='new_Pn' if j==0 else 'new_Pm'
  identity(name+'_original_norm_ratios',ratios(res[j],fields(rhs)[j],scales[j]),s['original_affine_and_actual_target_ratios'][2*j],abs(s['original_affine_and_actual_target_ratios'][2*j])+abs(ratios(res[j],fields(rhs)[j],scales[j])))
  identity(name+'_actual_target_residual',actual,targets[j]-(offsets[j]+act[j]),bound(witness,prefix+'_'+name+'_actual_target_residual')+abs(targets[j])+abs(offsets[j])+abs(act[j]))
  ra=ratios(actual,targets[j],scales[j]);identity(name+'_actual_target_norm_ratios',ra,s['original_affine_and_actual_target_ratios'][2*j+1],abs(ra)+abs(s['original_affine_and_actual_target_ratios'][2*j+1]))
  identity(name+'_actual_affine_momentum_pair',value(s,moment),offsets[j]+act[j],bound(s,moment)+abs(offsets[j])+fields(bound(s,'original_action'))[j])
 tr=value(witness,prefix+'_weak_trace_residual');ta=value(witness,prefix+'_weak_trace_action');target=sd['weak_trace_rhs'];identity('trace_residual_saved_words',tr,ta-target,bound(witness,prefix+'_weak_trace_residual')+bound(witness,prefix+'_weak_trace_action')+abs(target))
 rt=ratios(tr,target,scales[2]);identity('trace_norm_ratios',rt,s['weak_trace_ratios'],abs(rt)+abs(s['weak_trace_ratios']))
 fixture=one('three_fresh_DD_node_update_and_non_dyadic_division_controls');fd=read(fixture,lambda n:n.startswith('control_') or n.startswith('fresh_dd_nodes_division_'))
 assert fixture['metadata']['controls']==r['controls'][:3]
 for c in r['controls'][:2]+r['controls'][3:]:
  d=fd if c['ordinal']<2 else s;p='control_%03d_%s_'%(c['ordinal'],c['name']);identity(c['name'],d[p+'actual'],d[p+'expected'],d[p+'envelope']);assert IDENTITIES[-1]['error']==c['error']
 c=r['controls'][2]
 with localcontext() as ctx:
  ctx.prec=100;a=Decimal(c['actual']);expected=Decimal(c['expected']);error=abs(a-expected)/abs(expected)
 assert Decimal(c['error'])==error and c['tolerance']=='1e-30' and c['passed']==(error<=Decimal('1e-30')) and c['quotient_words_exact'] and c['remainder_words_exact']
 for name in ('quotient','remainder'):assert np.array_equal(fd['fresh_dd_nodes_division_actual_'+name+'_words'],fd['fresh_dd_nodes_division_expected_'+name+'_words'])
 admitted=bool(np.all(s['original_affine_and_actual_target_ratios']<=1e-10) and np.all(s['weak_trace_ratios']<=1e-10));assert admitted==sol['metadata']['canonical_and_trace_admitted']==(r['status']=='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE')==(case['rate_jets'] is not None)
 if admitted:
  rate=case['rate_jets'];bind(rate['file'],rate['sha256']);bind(rate['commit_file'],rate['commit_sha256']);assert json.loads(path(rate['commit_file']).read_text())=={k:v for k,v in rate.items() if k not in ('commit_file','commit_sha256')}
  md=rate['metadata'];assert rate in recs and md['kind']=='genuine_fixed_Q1_two_word_rate_value_and_spatial_jets' and md['canonical_rows_admitted'] and md['weak_trace_admitted'] and md['collapse_to_binary64_adopted'] is False and md['pointwise_CMC_claim'] is False
  assert set(md['schema'])=={name+'_jet_'+axis+'_'+word for name in ('native','metric') for axis in ('value','R','Z') for word in ('hi','lo')}
  for key,shape in md['schema'].items():assert shape==dict(shape=[33,15136,3] if key.startswith('native') else [15136,6],dtype='float64',finite=True)
 return dict(status='SAVED_DD_NODE_COORDINATE_WORDS_PASS',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),parent_terminal=TERMINAL,controls=len(r['controls']),committed_pairs=len(recs),selected_payload=SELECTED,identities=IDENTITIES,canonical_and_weak_trace_admitted=admitted,paired_RATE_JETS_schema_checked_only=admitted,qualification=r['qualification'],EFT_FE_operator_solver_or_fixture_replayed=False,physical_state_or_history_adopted=False)
def main():
 global np
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA and all(v is not None for v in TERMINAL.values()),'Actual CLOSED terminal and ROOT guard required'
 assert not list(BASE.glob(STEM+'_*'));bind(STEM+'.md',PROTOCOL_SHA)
 try:
  r=admission();import numpy as np_local
  np=np_local;out=audit(r)
  for n,h in INPUTS.items():assert sha(n)==h
  h=publish('RESULT',out);print(out['status'],h);return 0
 except BaseException:
  publish('ERROR',dict(status='SAVED_WORD_CHECK_FAILED',traceback=traceback.format_exc(),parent_terminal=TERMINAL,identities=IDENTITIES,selected_payload=SELECTED,EFT_FE_operator_solver_or_fixture_replayed=False));return 1
if __name__=='__main__':raise SystemExit(main())
