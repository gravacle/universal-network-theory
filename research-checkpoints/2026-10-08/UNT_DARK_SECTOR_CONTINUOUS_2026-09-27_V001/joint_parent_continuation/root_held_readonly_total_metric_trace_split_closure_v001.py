"""Saved tensor words and scalar identities; no h:Pi, FE or momentum replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_TOTAL_METRIC_MOMENTUM_TRACE_SPLIT_V001'
OUT='READONLY_TOTAL_METRIC_TRACE_SPLIT_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='52720974395a48eb012f7539c8f5c5e2095e2c3f9f1a99033995a2d7b41b56c2'
PROTOCOL_SHA='7d7055ca0fd8e314498fe29adca6349f07990aaabcc74b702eb6f47d895c4814'
TERMINAL=dict(pid=60485,result_sha256='f1eeef09b6184d651f3f668862ad41397c55362fe8bb4f00af113d8662f31ca5',receipt_sha256='ef21e630310b002abef69659a6997f012e158b56a96c03f130a11178dde1d122')
TOL=2e-11
def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def load_json(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and not path(OUT).exists()
 assert sha('cross_u_saved_total_metric_momentum_trace_split_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);r=load_json(STEM+'_RESULT.json',TERMINAL['result_sha256'])
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==TERMINAL['result_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and all(r[n] is False for n in ('canonical_primitive_readout_admitted','nominal_target_bridge_resolved','continuum_TT_prepared','physical_adoption'))
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 records=r['checkpoints'];controls=r['controls'];assert len(records)==5 and len(controls)==8 and [c['ordinal'] for c in controls]==list(range(8)) and all(c['passed'] and c['tolerance']==TOL and math.isfinite(c['error']) and c['error']<=TOL for c in controls)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256'] and load_json(q['commit_file'],q['commit_sha256'])=={n:q[n] for n in ('file','sha256','metadata')}
  assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and all(v['finite'] is True for v in q['metadata']['schema'].values())
 import numpy as np
 selected=[];identities=[];norms=[]
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def original(ref):
  for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert rc['input_sha256'].get(n,rc['input_sha256'].get(str(path(n).resolve())))==h and sha(n)==h,n
  q=load_json(ref['commit_file'],ref['commit_sha256']);assert q['file']==ref['file'] and q['sha256']==ref['sha256'];assert q['metadata']['owner']['pid']==50104
  return dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms):
  arrays=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(arrays);bound=np.add.reduce([abs(v) for v in arrays]);e=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert e<=TOL,(label,e);identities.append(dict(name=label,error=e))
 inp=records[0];assert inp['metadata']['kind']=='earned_literal_weak_Pm_and_unresolved_nominal_target_bridge' and inp['metadata']['canonical_primitive_readout_admitted'] is False and inp['metadata']['old_momentum_scatter_replayed'] is False
 ia=read(inp,tuple(inp['metadata']['schema']));prior=original(inp['metadata']['readout_ref']);old=read(prior,tuple(ia));assert all(np.array_equal(ia[n],old[n]) for n in ia)
 assert r['columns']==records[1:] and len(inp['metadata']['column_refs'])==4
 for iq,q in enumerate(r['columns']):
  md=q['metadata'];assert md['kind']=='new_paired_saved_total_canonical_metric_trace_decomposition' and md['column']==iq and md['parent_column_ref']==inp['metadata']['column_refs'][iq] and md['controls']==controls[2*iq:2*iq+2]
  assert all(md[n] is False for n in ('source_point_momentum_changed','reference_geometry_changed','nominal_target_bridge_resolved','canonical_trace_is_bare_EH_K','continuum_TT_prepared','physical_exterior_admitted'))
  a=read(q,tuple(md['schema']));parent=original(md['parent_column_ref']);names=('momentum_metric_total_density_hi','momentum_metric_total_density_lo','chart_h','chart_ih','chart_sqrt_h');oa=read(parent,names)
  assert parent['metadata']['column']==iq and all(np.array_equal(a['input_'+n],oa[n]) for n in names)
  p='column_%d'%iq;x=lambda n:pair(a,p+'_'+n);local=pair(oa,'momentum_metric_total_density');tensor=x('total_canonical_tensor_density')
  assert tensor[0].shape==tensor[1].shape==(3784,3,3) and all(np.array_equal(v,v.transpose(0,2,1)) for v in tensor)
  for k,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
   for w in (0,1):assert np.array_equal(tensor[w][:,i,j],local[w][:,k]*(1. if i==j else .5))
  for c in controls[2*iq:2*iq+2]:
   prefix='control_%03d_%s_'%(c['ordinal'],c['name']);actual,expected,envelope=(a[prefix+n] for n in ('actual','expected','envelope'));assert np.all(envelope>=0);e=float(np.max(abs(actual-expected)/np.maximum(envelope,1e-30),initial=0));assert e==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=e))
  identity(p+'_trace_subtraction',[(1,tensor),(-1,x('isotropic_canonical_density')),(-1,x('trace_subtracted_canonical_density'))])
  identity(p+'_reconstruction',[(1,x('trace_subtracted_canonical_density')),(1,x('isotropic_canonical_density')),(-1,x('reconstructed_total_density'))])
  identity(p+'_saved_reconstruction_gap',[(1,x('reconstructed_total_density')),(-1,tensor),(-1,x('reconstruction_gap'))])
  identity(p+'_stored_inverse_gap',[(1,x('h_contract_stored_ih')),(-1,(np.full(3784,3.),np.zeros(3784))),(-1,x('stored_inverse_trace_gap'))])
  identity(p+'_tau_third_division',[(1,x('total_canonical_trace_density')),(-1,tuple(3.*v for v in x('one_third_trace_density')))])
  third=x('one_third_trace_density');iso=(oa['chart_ih']*third[0][:,None,None],oa['chart_ih']*third[1][:,None,None]);identity(p+'_isotropic_scalar_product',[(1,x('isotropic_canonical_density')),(-1,iso)])
  product=(third[0]*x('h_contract_stored_ih')[0],third[0]*x('h_contract_stored_ih')[1],third[1]*x('h_contract_stored_ih')[0],third[1]*x('h_contract_stored_ih')[1]);identity(p+'_saved_trace_prediction',[(1,x('total_canonical_trace_density')),(-1,product),(-1,x('predicted_trace_from_stored_inverse_gap'))])
  identity(p+'_saved_trace_identity_gap',[(1,x('actual_trace_subtracted_trace')),(-1,x('predicted_trace_from_stored_inverse_gap')),(-1,x('trace_gap_identity'))])
  norms.append({n:dict(component_L2=float(np.linalg.norm(total(x(n)))),component_Linf=float(np.max(abs(total(x(n))),initial=0))) for n in ('total_canonical_trace_density','isotropic_canonical_density','trace_subtracted_canonical_density','stored_inverse_trace_gap','actual_trace_subtracted_trace','trace_gap_identity')})
 report=dict(status='SAVED_TOTAL_METRIC_TRACE_SPLIT_CLOSURE_PASS',owner_pid=os.getpid(),parent=TERMINAL,controls=8,committed_pairs=5,identities=identities,selected=selected,column_component_norms_descriptive=norms,old_weak_Pm_and_literal_point_inputs_bitcopied=True,tensor_cross_slot_half_factor_checked=True,independent_h_contract_Pi_or_h_contract_TF=False,scope_limit='Stored tensor/scalar words and triplets only; no new h:Pi/h:TF contraction, old momentum or FE scatter',canonical_primitive_bridge_resolved=False,continuum_TT_admitted=False,physical_adoption=False,old_EFT_FE_operator_momentum_or_fixture_replayed=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256']
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
