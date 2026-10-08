"""Guarded saved-only DD residual/correction witnesses. No operator replay."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,localcontext
import argparse,hashlib,json,math,os,traceback
BASE=Path(__file__).resolve().parent
STEM='READONLY_GLOBAL_DD_REFINEMENT_SAVED_RESULT_AUDIT_V001'
PARENT='CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_REFINEMENT_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='6df6380712d9137fee0b0e0177ee8934f452a00376ef316dfb974c7dd1e1c838'
TERMINAL=dict(pid=None,source_sha256='7725619fd925c7fc91796b495a482d71fa24756a75537e72839d6090d7e774db',protocol_sha256='32f3abd7e056c29ab41474a3eb06ec1969f3a8de9aa1a8a160b9cf80414dd884',result_sha256=None,receipt_sha256=None)
np=None;INPUTS={};IDENTITIES=[];COUNTS=dict(numeric_arrays=0,finite_entries=0,negative_entries=0,boolean_arrays=0,boolean_entries=0,metadata_arrays=0)
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(p):
 h=hashlib.sha256()
 with path(p).open('rb') as f:
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
def pair_value(d,prefix):return d[prefix+'_hi']+d[prefix+'_lo']
def pair_bound(d,prefix):return abs(d[prefix+'_hi'])+abs(d[prefix+'_lo'])
def masks():
 n=np.ones((3,87,45),dtype=bool);n[:,0]=False;n[1,:,0]=False
 m=np.ones((6,87,45),dtype=bool);m[:,0]=False;m[3:5,:,0]=False
 return np.broadcast_to(n,(33,3,87,45)),m
def fields(x):
 n,m=masks();a=np.zeros(n.shape);b=np.zeros(m.shape);assert x.shape==(403340,)
 a[n]=x[:380292];b[m]=x[380292:];return a,b
def pack(a,b):
 n,m=masks();return np.concatenate((a[n],b[m]))
def ratios(r,t,s):
 out=np.array((np.linalg.norm(r)/np.linalg.norm(t),np.linalg.norm(r/s)/np.linalg.norm(t/s)))
 assert np.all(np.isfinite(out));return out
def read(rec,keep):
 assert sha(rec['file'])==rec['sha256'] and sha(rec['commit_file'])==rec['commit_sha256']
 assert json.loads(path(rec['commit_file']).read_text())=={k:v for k,v in rec.items() if k not in ('commit_file','commit_sha256')}
 out={}
 with np.load(path(rec['file']),allow_pickle=False) as f:
  assert set(f.files)==set(rec['metadata']['schema'])|{'metadata_json'} and json.loads(str(f['metadata_json']))==rec['metadata'];COUNTS['metadata_arrays']+=1
  for k,s in rec['metadata']['schema'].items():
   a=f[k];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True and np.all(np.isfinite(a)),(rec['file'],k)
   if a.dtype.kind=='b':COUNTS['boolean_arrays']+=1;COUNTS['boolean_entries']+=a.size
   else:assert a.dtype.kind in 'fiu';COUNTS['numeric_arrays']+=1;COUNTS['finite_entries']+=a.size;COUNTS['negative_entries']+=int(np.count_nonzero(a<0))
   if keep(k):out[k]=a.copy()
 return out
def admission():
 t=TERMINAL;assert all(x is not None for x in t.values()),'Actual natural closure required; no live outputs'
 for n,h in ((PARENT+'_RESULT.json',t['result_sha256']),(PARENT+'_RECEIPT.json',t['receipt_sha256']),('cross_u_canonical_nodal_metric_rate_dd_refinement_v001.py',t['source_sha256']),(PARENT+'.md',t['protocol_sha256'])):bind(n,h)
 r=json.loads(path(PARENT+'_RESULT.json').read_text());rc=json.loads(path(PARENT+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc['owner']==r['owner'] and r['owner']['owner']=='root' and r['owner']['pid']==t['pid'] and r['owner']['source_sha256']==t['source_sha256']
 assert rc['closed']>r['owner']['started'] and rc['result_sha256']==t['result_sha256'] and rc['error_sha256'] is None and r['qualification']==rc['qualification'] and all(q is False for q in r['qualification'].values())
 assert r['status'] in ('CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE','ORIGINAL_CANONICAL_ROWS_NOT_ADMITTED') and r['case']['status']==r['status'] and r['case']['trace_preparation'] is None
 assert r['case']['parent_nonadmission_preserved'] is True and r['case']['no_extra_iteration_cap'] is True and r['case']['physical_adoption'] is False
 for mapping in (rc['input_sha256'],rc['output_sha256']):
  for n,h in mapping.items():bind(n,h)
 recs=r['checkpoints'];cycles=r['case']['compatibility_corrections'];assert len(cycles)<=3 and len(r['controls'])==10+len(cycles) and all(c['passed'] for c in r['controls'])
 assert len(recs)==5+len(cycles)+sum(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' for q in recs)+(r['case']['rate_jets'] is not None)
 assert {p.name for p in BASE.glob(PARENT+'_*.npz')}=={q['file'] for q in recs} and {p.name for p in BASE.glob(PARENT+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in recs}
 for q in recs:
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256']
 return r,rc

def audit(result):
 recs=result['checkpoints'];kind=lambda name:next(q for q in recs if q['metadata']['kind']==name)
 inp=kind('inherited_closed_DD_and_geometry_proofs_and_selected_frozen_system');base=kind('exact_frozen_x1080_rhs_targets_and_rounded_affine_offsets')
 bd=read(base,lambda k:True);rhs=bd['original_rhs'];scales=(bd['native_scale'],bd['metric_scale'],bd['scalar_scale']);targets=(bd['current_Pn'],bd['current_Pm']);offsets=(bd['rounded_global_cn'],bd['rounded_global_cm'])
 read(inp,lambda k:False);initial=kind('new_accurate_original_action_on_unadmitted_x1080')
 need=lambda k:k.startswith(('initial_','saved_residual_minus_','saved_action_minus_','original_rhs64_minus_'))
 init=read(initial,need);reference=inp['metadata']['references']
 for c in result['controls'][6:10]:
  with localcontext() as ctx:
   ctx.prec=100;a=Decimal(c['actual']);e=Decimal(c['expected']);error=abs(a-e)/abs(e)
  assert e!=0 and c['tolerance']=='1e-10' and Decimal(c['error'])==error and c['passed']==(error<=Decimal('1e-10'))
 for row in inp['metadata']['rows']:
  index=row['packed_native_index'];group=row['group']
  for suffix,prefix,expected in (('action','initial_action',reference[str(group)]['action']),('original_residual','initial_residual',reference[str(group)]['original_rhs_residual'])):
   c=next(q for q in result['controls'] if q['name']=='selected_row%d_array_%s_accuracy'%(group,suffix))
   with localcontext() as ctx:ctx.prec=100;value=Decimal.from_float(float(init[prefix+'_hi'][index]))+Decimal.from_float(float(init[prefix+'_lo'][index]))
   assert str(value)==c['actual'] and expected==c['expected'] and rhs[index]==row['original_rhs']
 identity('saved_restart_residual_defect',bd['original_saved_residual']-pair_value(init,'initial_residual'),pair_value(init,'saved_residual_minus_DD_original_residual'),abs(bd['original_saved_residual'])+pair_bound(init,'initial_residual')+pair_bound(init,'saved_residual_minus_DD_original_residual'))
 identity('saved_action_readout_defect',bd['original_saved_action']-pair_value(init,'initial_action'),pair_value(init,'saved_action_minus_DD_original_action'),abs(bd['original_saved_action'])+pair_bound(init,'initial_action')+pair_bound(init,'saved_action_minus_DD_original_action'))
 identity('frozen_rhs_target_offset_defect',rhs,pack(targets[0],targets[1])-pack(offsets[0],offsets[1])+pair_value(init,'original_rhs64_minus_exact_saved_target_offset'),abs(rhs)+abs(pack(targets[0],targets[1]))+abs(pack(offsets[0],offsets[1]))+pair_bound(init,'original_rhs64_minus_exact_saved_target_offset'))
 consumed={q['file'] for q in (inp,base,initial)};previous=bd['x1080'];previous_res=pair_value(init,'initial_residual');witness=init;witness_prefix='initial'
 for rec in recs:
  if rec['metadata']['kind']!='bounded_float_MINRES_correction_with_DD_original_certificate':continue
  label='cycle_%03d'%rec['metadata']['cycle'];assert rec['metadata']['cap']==160
  d=read(rec,lambda k:k.startswith(label+'_'));consumed.add(rec['file']);new=d[label+'_final_update_actual_binary64_nodes'];low=d[label+'_final_update_exact_update_minus_actual_nodes'];delta=d[label+'_completed_correction']
  identity(label+'_binary64_node_update',new+low,previous+delta,abs(new)+abs(low)+abs(previous)+abs(delta))
  r=pair_value(d,label+'_final_residual');pred=pair_value(d,label+'_shifted_prediction');gap=pair_value(d,label+'_shifted_gap');bound=d[label+'_update_uncancelled_bound_through_node_low']
  identity(label+'_saved_shifted_gap',r-pred,gap,abs(r)+abs(pred)+pair_bound(d,label+'_shifted_gap')+bound)
  da=pair_value(d,label+'_accurate_delta_action');la=pair_value(d,label+'_accurate_node_rounding_action')
  identity(label+'_saved_shifted_residual',pred,previous_res-da+la,bound+abs(pred)+abs(previous_res)+abs(da)+abs(la))
  er=d[label+'_correction_rhs_rounding_defect_hi']+d[label+'_correction_rhs_rounding_defect_lo'];cr=d[label+'_correction_rhs_rounded_value']
  identity(label+'_correction_rhs_collapse_defect',previous_res,cr+er,abs(previous_res)+abs(cr)+abs(er))
  assert np.all(bound>=0) and d[label+'_history'][-1,0]<=160
  previous=new;previous_res=r;witness=d;witness_prefix=label+'_final'
 sol=result['case']['compatibility'];s=read(sol,lambda k:True);consumed.add(sol['file']);action=fields(pair_value(s,'original_action'));res=fields(pair_value(s,'original_residual'))
 for j,name in enumerate(('native','metric')):
  ratio=ratios(res[j],fields(rhs)[j],scales[j]);stored=s['original_affine_and_actual_target_ratios'][2*j]
  identity(name+'_original_norm_ratios',ratio,stored,abs(ratio)+abs(stored))
  prefix=witness_prefix+'_'+name+'_actual_target_residual';actual=pair_value(witness,prefix)
  identity(name+'_saved_actual_target_residual',actual,targets[j]-(offsets[j]+action[j]),pair_bound(witness,prefix)+abs(targets[j])+abs(offsets[j])+abs(action[j]))
  ratio=ratios(actual,targets[j],scales[j]);stored=s['original_affine_and_actual_target_ratios'][2*j+1]
  identity(name+'_actual_target_norm_ratios',ratio,stored,abs(ratio)+abs(stored))
  value=s['new_Pn' if j==0 else 'new_Pm'];identity(name+'_saved_actual_affine_momentum',value,offsets[j]+action[j],abs(value)+abs(offsets[j])+abs(action[j]))
 trace=witness[witness_prefix+'_weak_trace_action'];trace_res=witness[witness_prefix+'_weak_trace_residual'];trace_rhs=bd['weak_trace_rhs']
 identity('saved_weak_trace_residual',trace_res,trace-trace_rhs,abs(trace_res)+abs(trace)+abs(trace_rhs))
 tr=ratios(trace_res,trace_rhs,scales[2]);identity('saved_weak_trace_norm_ratios',tr,s['weak_trace_ratios'],abs(tr)+abs(s['weak_trace_ratios']))
 for c in result['controls'][10:]:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);identity(c['name'],s[prefix+'actual'],s[prefix+'expected'],s[prefix+'envelope']);assert IDENTITIES[-1]['error']==c['error']
 admitted=bool(np.all(s['original_affine_and_actual_target_ratios']<=1e-10) and np.all(s['weak_trace_ratios']<=1e-10))
 assert admitted==(result['status']=='CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE') and sol['metadata']['canonical_and_trace_admitted']==admitted and (result['case']['rate_jets'] is not None)==admitted
 for q in recs:
  if q['file'] not in consumed:
   d=read(q,lambda k:k.startswith('control_') or k.endswith('_history'))
   if q['metadata']['kind']=='six_fresh_array_EFT_and_full32_native99_signed_metric6_controls':
    for c in result['controls'][:6]:
     prefix='control_%03d_%s_'%(c['ordinal'],c['name']);identity(c['name'],d[prefix+'actual'],d[prefix+'expected'],d[prefix+'envelope']);assert IDENTITIES[-1]['error']==c['error']
   for k,a in d.items():
    if k.endswith('_history') and len(a):assert a[-1,0]<=160
 return dict(status='SAVED_GLOBAL_DD_REFINEMENT_AUDIT_PASS',pid=os.getpid(),closed=datetime.now(timezone.utc).isoformat(),parent_terminal=TERMINAL,controls=len(result['controls']),committed_pairs=len(recs),counts=COUNTS,identities=IDENTITIES,original_canonical_and_trace_admitted=admitted,qualification=result['qualification'],DD_EFT_FE_operator_or_solver_replayed=False,new_field_or_history_adopted=False)
def main():
 global np
 ap=argparse.ArgumentParser();ap.add_argument('--root-run',action='store_true');args=ap.parse_args()
 assert args.root_run and not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA and all(v is not None for v in TERMINAL.values()),'Guarded saved auditor; actual terminal and ROOT required'
 assert not list(BASE.glob(STEM+'_*'));bind(STEM+'.md',PROTOCOL_SHA);result,receipt=admission()
 try:
  import numpy as np_local
  np=np_local;out=audit(result)
  for n,h in INPUTS.items():assert sha(n)==h,n
  h=publish('RESULT',out);print(out['status'],h);return 0
 except BaseException:
  publish('ERROR',dict(status='SAVED_AUDIT_FAILED',traceback=traceback.format_exc(),parent_terminal=TERMINAL,identities=IDENTITIES,counts=COUNTS,numerical_functions_replayed=False));return 1
if __name__=='__main__':raise SystemExit(main())
