"""Held recovery of completed comparison words from authentic CLOSED_ERROR; no replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_REGISTERED_NORMAL_RATE_SPECIALIZATION_COMPARISON_V001'
OUT='READONLY_REGISTERED_RATE_COMPARISON_RECOVERY_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='f673882b19c2684edddc7b96a79c17300585ab54eac58c1b143a5c9d508b8875'
PROTOCOL_SHA='0d5c4fa85592f8de3f452f8a9a06841f5dce1e972ad5758698883194b88f5afe'
TERMINAL={'pid': 72762, 'result_sha256': None, 'receipt_sha256': '31273b94f9ab52839fc1dcc36688dc53822cf02adfae5a79f6a104896b145e48', 'error_sha256': 'ec42297bdeaccc9d64696b49065dbbcf5266fefc466709b5dfadf5b3b476e4ec'}
TOL=2e-11
RECOVERED_ALIASES={}
for _p in range(3):
 for _f in ('specialized','full'):
  for _w in ('hi','lo'):
   for _n in ('density','weak'):RECOVERED_ALIASES['patch_%d_%s_CMC_%s_%s'%(_p,_f,_n,_w)]='completed_patch_%d_%s_CMC_%s_%s'%(_p,_f,_n,_w)
   for _n in ('nodal','direct','gap'):RECOVERED_ALIASES['patch_%d_%s_CMC_functional_%s_%s'%(_p,_f,_n,_w)]='patch_%d_%s_CMC_%s_%s'%(_p,_f,_n,_w)

def path(n):
 p=Path(n);return p if p.is_absolute() else BASE/p
def sha(n):
 h=hashlib.sha256()
 with path(n).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def js(n,h):
 assert h is not None and sha(n)==h,n
 return json.loads(path(n).read_text())
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def main():
 assert AUTHOR_DRAFT is False and all(TERMINAL[n] is not None for n in ('pid','receipt_sha256')) and not path(OUT).exists(),'Reviewed actual natural closure required before I/O'
 assert TERMINAL['result_sha256'] is None and TERMINAL['error_sha256'] is not None
 assert sha('cross_u_registered_normal_rate_specialization_comparison_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=False;assert rc['status']=='CLOSED_ERROR'
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid']==72762 and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values());records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h and sha(n)==h,n
  assert js(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  assert all(s['finite'] for s in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=26 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 import numpy as np
 selected=[];identities=[];triplets={}
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    key=RECOVERED_ALIASES.get(n,n) if q['metadata']['kind']=='bounded_same_response_comparison_partial_operands' else n
    a=f[key].copy();assert list(a.shape)==sc[key]['shape'] and str(a.dtype)==sc[key]['dtype'] and sc[key]['finite'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms,envelope):
  values=[sign*x for sign,p in terms for x in p];gap=np.add.reduce(values);assert gap.shape==envelope.shape and np.all(envelope>=0)
  error=float(np.max(abs(gap)/np.maximum(envelope,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def control(name):
  hits=[c for c in controls if c['name']==name];assert len(hits)==1,name
  return triplets[hits[0]['ordinal']]
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;raw=read(found[0],names)
  for q in found[1:]:
   copy=read(q,names);assert all(np.array_equal(raw[n],copy[n]) for n in names)
  actual,expected,envelope=(raw[n] for n in names);assert np.all(envelope>=0);error=float(np.max(abs(actual-expected)/np.maximum(envelope,1e-30),initial=0));assert error==c['error'];triplets[c['ordinal']]=(actual,expected,envelope);identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if rc['status']=='CLOSED_ERROR':
  picks=lambda kind:[q for q in records if q['metadata']['kind']==kind]
  inputs=picks('predeclared_three_owned_geometry_patches');cols=sorted(picks('bounded_same_response_all_sixteen_registered_rate_test_comparison'),key=lambda q:q['metadata']['column']);raw=picks('bounded_same_response_comparison_partial_operands');assert len(inputs)==len(raw)==1 and len(cols)==4 and len(records)==6 and len(controls)==26 and all(c['passed'] for c in controls)
  inp,loads=inputs[0],raw[0];assert not inp['metadata']['failed'] and all(not q['metadata']['failed'] for q in cols) and loads['metadata']['failed'] and len(loads['metadata']['schema'])==312 and not any(q['file'].endswith('_LOADS.npz') for q in records)
  assert r['status']=='FAILED' and r['context']==dict(control='patch_2_specialized_full_weak_CMC',ordinal=25,stage='bounded_patch_new_normal_and_CMC_functionals') and 'assert isinstance(a,np.ndarray)' in r['traceback'] and not path(STEM+'_RESULT.json').exists()
  im=inp['metadata'];lm=loads['metadata'];nodes=[[43,22],[21,11],[64,33]];sq=im['source_qualification'];assert im['patch_nodes']==nodes and im['point_count']==48 and lm['kind']=='bounded_same_response_comparison_partial_operands' and lm['context']==r['context']
  assert sq['implementation_test_operands_only'] is True and sq['canonical_or_Jacobian_direction_adopted'] is False and sq['zero_native_RHS_relative_ratio'] is None and im['physical_ports'] is None
  assert sq['status'] in ('NEW_LITERAL_TRACE_TARGET_RESPONSE_ADMITTED','NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED') and sq['literal_original_response_admitted']==(sq['status']=='NEW_LITERAL_TRACE_TARGET_RESPONSE_ADMITTED')
  for q in im['current_refs']+im['response_refs']:
   for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['input_sha256'][str(path(n).resolve())]==h
  ia=read(inp,('predeclared_patch_nodes','predeclared_patch_point_indices'));take=ia['predeclared_patch_point_indices'];assert ia['predeclared_patch_nodes'].dtype==take.dtype==np.dtype('int64') and np.array_equal(ia['predeclared_patch_nodes'],np.asarray(nodes)) and take.shape==(12,) and len(set(take.tolist()))==12 and np.all((take>=0)&(take<3784))
  shapes=dict(native_metric_terms=(12,4,4,7),mode_compensation_terms=(12,4,4,7),absolute_phase_terms=(12,4,4,2),EH_terms=(12,4,4,3),component_densities=(12,4,4,4),coefficient=(12,4,4));column_data=[]
  for iq,q in enumerate(cols):
   md=q['metadata'];assert md['kind']=='bounded_same_response_all_sixteen_registered_rate_test_comparison' and md['column']==iq and md['patch_nodes']==nodes and md['pilot_ref']==im['current_refs'][iq] and md['rate_ref']==im['response_refs'][iq] and md['literal_response_qualification']==sq and md['all_primary_test_directions_retained'] and md['whole_grid_arithmetic_qualified'] is False and md['physical_ports'] is None
   names=['point_indices']+[n+'_'+w for n in ('CMC_Gamma_density','CMC_ADM_density','CMC_Gamma_chain_minus_affine81','CMC_actual_affine81_density') for w in ('hi','lo')]+['CMC_implementation_envelope']
   names+= [family+'_'+n+'_'+w for n in shapes for family in ('specialized','full') for w in ('hi','lo')]+[n+'_implementation_envelope' for n in shapes];a=read(q,names);assert np.array_equal(a['point_indices'],take)
   for row in range(4):
    for jet in range(4):
     for n in ('raw_test_duc','raw_test_projector','raw_test_inverse','test_Gamma'):
      for w in ('hi','lo'):assert 'direction_%d_%d_%s_gap_%s'%(row,jet,n,w) in md['schema'] and md['schema']['direction_%d_%d_%s_gap_%s'%(row,jet,n,w)]['finite']
   actual,expected,envelope=control('bounded_same_operand_rate_families_column_%d'%iq);assert np.all(expected==0);offset=0;bounds=[]
   for n,shape in shapes.items():
    x,y=pair(a,'specialized_'+n),pair(a,'full_'+n);e=a[n+'_implementation_envelope'];assert x[0].shape==x[1].shape==y[0].shape==y[1].shape==e.shape==shape;size=e.size;v=actual[offset:offset+size].reshape(shape);identity('column_%d_%s_stored_difference'%(iq,n),[(1,x),(-1,y),(-1,(v,np.zeros(shape)))],e);offset+=size;bounds.append(e.ravel())
   assert offset==actual.size and np.array_equal(envelope,np.concatenate(bounds))
   ca,ce,cb=control('bounded_CMC_Gamma_chain_against_same_affine81_column_%d'%iq);cg=pair(a,'CMC_Gamma_chain_minus_affine81');assert np.array_equal(ca,total(cg)) and np.all(ce==0) and np.array_equal(cb,a['CMC_implementation_envelope']);identity('column_%d_CMC_Gamma_minus_same81'%iq,[(1,pair(a,'CMC_Gamma_density')),(-1,pair(a,'CMC_actual_affine81_density')),(-1,cg)],cb);column_data.append(a)
  names=[]
  for patch in range(3):
   for family in ('specialized','full'):
    names += ['patch_%d_%s_%s_%s'%(patch,family,n,w) for n in ('weak_normal','functional_nodal','functional_direct','functional_gap') for w in ('hi','lo')]
    names += ['patch_%d_%s_CMC_%s_%s'%(patch,family,n,w) for n in ('density','weak','functional_nodal','functional_direct','functional_gap') for w in ('hi','lo')]
   names += ['patch_%d_weak_%s_difference_%s'%(patch,n,w) for n in ('normal','CMC') for w in ('hi','lo')]
  a=read(loads,names);summaries=[]
  for patch in range(3):
   for kind,weakname in (('normal','weak_normal'),('CMC','CMC_weak')):
    for family in ('specialized','full'):
     base='patch_%d_%s_'%(patch,family)+('CMC_' if kind=='CMC' else '');nodal=pair(a,base+'functional_nodal');direct=pair(a,base+'functional_direct');gap=pair(a,base+'functional_gap');actual,expected,envelope=control('patch_%d_%s_exact_%s_%s_functional'%(patch,family,'scalar' if kind=='CMC' else 'normal','CMC' if kind=='CMC' else 'polynomial'))
     assert np.array_equal(actual,total(gap)) and np.all(expected==0);identity(base+'nodal_direct_saved_gap',[(1,nodal),(-1,direct),(-1,gap)],envelope)
    diff=pair(a,'patch_%d_weak_%s_difference'%(patch,kind));x=pair(a,'patch_%d_specialized_%s'%(patch,weakname));y=pair(a,'patch_%d_full_%s'%(patch,weakname));actual,expected,envelope=control('patch_%d_specialized_full_weak_%s'%(patch,kind));assert np.array_equal(actual,total(diff)) and np.all(expected==0);identity('patch_%d_%s_saved_weak_difference'%(patch,kind),[(1,x),(-1,y),(-1,diff)],envelope);summaries.append(dict(patch=patch,kind=kind,specialized_L2=float(np.linalg.norm(total(x))),full_L2=float(np.linalg.norm(total(y))),difference_L2=float(np.linalg.norm(total(diff)))))
   for family,source in (('specialized','CMC_Gamma_density'),('full','CMC_actual_affine81_density')):
    density=pair(a,'patch_%d_%s_CMC_density'%(patch,family));ids=np.concatenate([iq*3784+take[patch*4:patch*4+4] for iq in range(4)]);mask=np.ones(15136,bool);mask[ids]=False
    for w in (0,1):assert np.all(density[w][mask]==0) and np.array_equal(density[w][ids],np.concatenate([pair(q,source)[w][patch*4:patch*4+4] for q in column_data]))
  report=dict(status='SAVED_REGISTERED_RATE_COMPARISON_RECOVERY_PASS',original_terminal_status='CLOSED_ERROR',original_producer_status=r['status'],controls=26,committed_pairs=6,completed_numerical_evidence_recovered_from_saved_words=True,original_LOADS_publication_missing=True,original_ERROR_RAW_fields=312,recovered_logical_aliases=RECOVERED_ALIASES,patches=nodes,owned_contacts=48,source_qualification=sq,whole_grid_arithmetic_qualified=False,canonical_target_response_qualified=False,weak_patch_diagnostics=summaries,publication_limit='Original LOADS and RESULT remain absent; authentic failed source/receipt/ERROR_RAW are preserved. This new verifier certifies selected completed words only and neither publishes a replacement producer packet nor relabels its CLOSED_ERROR.')
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_tolerance=TOL,normal_CMC_features_scatter_operator_solver_or_fixtures_replayed=False,physical_adoption=False,scope_limit='Stored differences, copies, triplets and norm summaries only. No phase/native/EH formula, point action, CMC contraction, FE scatter or functional is reevaluated. Aliases select only normalized completed ERROR_RAW operands. This is a bounded implementation test, not whole-grid or canonical/physical admission.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_registered_normal_rate_specialization_comparison_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
