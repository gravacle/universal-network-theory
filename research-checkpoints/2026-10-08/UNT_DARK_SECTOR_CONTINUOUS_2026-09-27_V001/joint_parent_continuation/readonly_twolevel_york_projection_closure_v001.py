"""Guard-held stored V004 York words; no numerical producer or operator replay."""
from pathlib import Path
import ast,hashlib,json,math,os,struct,zipfile
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V004'
OUT='READONLY_TWOLEVEL_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='738d9b72949ab43380a66206ff35779774a916f404867558116ecb7263603f57'
PROTOCOL_SHA='be86443151be254fd794e0e12948d17dde0d2af29ead2ff31739ab7bb488abbc'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V003'
PARENT_RESULT_SHA='3238ef464e0fde1b66de2a7e1135d57da1d9264e07cdea033cd2e58850059a4e'
PARENT_RECEIPT_SHA='e49439ec7f6f225851b0777ce0b4f887215721c285530415c1a01a836152683c'
PARENT_PROOF=('READONLY_COUPLED_YORK_PROJECTION_CLOSURE_V001_RESULT.json','ddebaf456ddc8a190f88032620607660e887d8e8050577d841926f4375070f5a')
TOL=2e-11;ROW_TOL=1e-10

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
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists()
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_compact_york_longitudinal_projection_v004.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=load_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'])
 assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 import numpy as np
 selected=[];identities=[]
 def seal(q,output=True):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert (rc['output_sha256'][n] if output else rc['input_sha256'][str(path(n).resolve())])==h and sha(n)==h,n
  assert load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')}
 def headers(q):
  sc=q['metadata']['schema']
  with zipfile.ZipFile(path(q['file'])) as z:
   assert set(z.namelist())=={n+'.npy' for n in sc}|{'metadata_json.npy'}
   for n,s in sc.items():
    with z.open(n+'.npy') as f:
     assert f.read(6)==b'\x93NUMPY';v=f.read(2);assert v in (b'\x01\x00',b'\x02\x00',b'\x03\x00');h=struct.unpack('<H' if v[0]==1 else '<I',f.read(2 if v[0]==1 else 4))[0];hd=ast.literal_eval(f.read(h).decode('utf8' if v[0]==3 else 'latin1'))
    assert list(hd['shape'])==s['shape'] and str(np.dtype(hd['descr']))==s['dtype'] and np.dtype(hd['descr']).kind in 'fiub',n
  if closed:assert all(s['finite'] is True for s in sc.values())
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def identity(label,terms,envelope=None):
  parts=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(parts);bound=np.add.reduce([abs(v) for v in parts]) if envelope is None else envelope
  assert gap.shape==bound.shape and np.all(bound>=0);e=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert e<=TOL,(label,e);identities.append(dict(name=label,error=e))
 def ratios(res,rhs,scale):
  cuts=(0,3740,7395,11135);out=[]
  for i in range(3):
   s=slice(cuts[i],cuts[i+1]);a=np.linalg.norm(rhs[s]);b=np.linalg.norm(rhs[s]/scale[s]);assert a>0 and b>0;out.append((np.linalg.norm(res[s])/a,np.linalg.norm(res[s]/scale[s])/b))
  return np.asarray(out)
 for q in records:
  seal(q);headers(q);assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=2 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 for c in controls:
  p='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(p+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_TWOLEVEL_YORK_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  inp,fix,coarse,sol=(r[n] for n in ('input','fixture','coarse','solution'));assert all(q in records for q in (inp,fix,coarse,sol)) and len(controls)==2 and all(c['passed'] for c in controls)
  assert [q['metadata']['kind'] for q in (inp,fix,coarse,sol)]==['exact_refused_coupled_York_final_seed_and_frozen_operator','fresh_alias_triangular_and_redundant_rectangular_congruence_control','new_coupled_coarse_basis_Gram_and_strict_factor','one_bounded_coupled_twolevel_York_original_row_result']
  assert r['vector_space_dimension']==11135 and r['coarse_dimension']==2730 and r['extended_dimension']==13865 and r['cap']==160 and r['max_new_cycles']==1 and r['parent_original_rows_admitted'] is False and r['all_full_coupled_map_entries_retained'] is True
  assert all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
  for n,h in ((PARENT+'_RESULT.json',PARENT_RESULT_SHA),(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA),PARENT_PROOF):assert rc['input_sha256'][str(path(n).resolve())]==h
  old=load_json(PARENT+'_RESULT.json',PARENT_RESULT_SHA);oldrc=load_json(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA);proof=load_json(*PARENT_PROOF)
  assert old['owner']==oldrc['owner'] and old['owner']['pid']==68504 and oldrc['status']=='CLOSED' and oldrc['error_sha256'] is None and proof['status']=='SAVED_COUPLED_YORK_CLOSURE_PASS' and proof['original_rows_admitted'] is False
  assert proof['parent']==dict(pid=68504,result_sha256=PARENT_RESULT_SHA,receipt_sha256=PARENT_RECEIPT_SHA,error_sha256=None) and proof['controls']==6 and proof['committed_pairs']==13
  assert inp['metadata']['parent_input']==thin(old['input']) and inp['metadata']['parent_solution']==thin(old['solution']) and inp['metadata']['all_parent_input_fields_bitcopied'] and inp['metadata']['final_SOLUTION_loaded_before_INPUT_to_preserve_aliases'] and inp['metadata']['warm_final_solution_prefix']=='warm_final_solution_'
  assert r['preserved_parent_controls']==inp['metadata']['preserved_parent_controls']==old['controls'] and r['preserved_parent_checkpoints']==inp['metadata']['preserved_parent_checkpoints']==old['checkpoints'] and fix['metadata']['controls']==controls[:1] and sol['metadata']['controls']==controls
  for q in (old['input'],old['solution']):
   seal(q,False);assert q in old['checkpoints'] and all(oldrc['output_sha256'][n]==h for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])))
  warm=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale')
  with np.load(path(inp['file']),allow_pickle=False) as new,np.load(path(old['input']['file']),allow_pickle=False) as original,np.load(path(old['solution']['file']),allow_pickle=False) as previous:
   for n,s in old['input']['metadata']['schema'].items():assert inp['metadata']['schema'][n]==s and original[n].tobytes()==new[n].tobytes(),n
   assert {n for n in inp['metadata']['schema'] if n.startswith('warm_final_solution_')}=={'warm_final_solution_'+n for n in warm}
   for n in warm:assert inp['metadata']['schema']['warm_final_solution_'+n]==old['solution']['metadata']['schema'][n] and previous[n].tobytes()==new['warm_final_solution_'+n].tobytes(),n
  ia=read(inp,tuple('warm_final_solution_'+n for n in warm)+('rhs_hi','rhs_lo','positive_Jacobi_congruence_scale','compact_vector_mask'));mask=ia['compact_vector_mask'];assert mask.dtype==np.dtype('bool') and mask.shape==(3,87,45) and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
  rhs=pair(ia,'rhs');rhs=tuple(v[mask] for v in rhs);f=total(rhs);scale=ia['positive_Jacobi_congruence_scale'][mask];assert np.all(scale>0) and np.array_equal(scale,ia['warm_final_solution_original_positive_scale']) and all(np.array_equal(rhs[i],ia['warm_final_solution_original_rhs_'+w]) for i,w in enumerate(('hi','lo')))
  start=pair(ia,'warm_final_solution_final_potential_nodes');before=pair(ia,'warm_final_solution_final_original_residual');identity('warm_rhs_action_residual',[(1,rhs),(-1,pair(ia,'warm_final_solution_final_original_action')),(-1,before)])
  label='twolevel_york';up=label+'_final_update';bases=('before_nodes','before_original_residual','fine_rhs_readout_defect','final_original_original_action','final_original_original_residual','original_residual_update_identity','completed_correction_action_action_restricted','compression_action_action_restricted')
  names=tuple(label+'_'+n+'_'+w for n in bases for w in ('hi','lo'))+tuple(up+s for s in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes'))+(label+'_fine_rhs_binary64',label+'_residual_update_operation_envelope')+warm
  a=read(sol,names);p=lambda n:pair(a,label+'_'+n);nodes=pair(a,'final_potential_nodes')
  for w in (0,1):assert np.array_equal(p('before_nodes')[w],start[w]) and np.array_equal(p('before_original_residual')[w],before[w]) and np.array_equal(pair(a,up+'_old_nodes')[w],start[w]) and np.array_equal(pair(a,up+'_updated_nodes')[w],nodes[w]) and np.array_equal(pair(a,'original_rhs')[w],rhs[w]) and np.array_equal(p('final_original_original_action')[w],pair(a,'final_original_action')[w]) and np.array_equal(p('final_original_original_residual')[w],pair(a,'final_original_residual')[w])
  words=[a[up+s] for s in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes')];assert all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*words));identities.append(dict(name='exact_old_plus_delta_equals_new_plus_q',error=0.))
  identity('fine_rhs_readout_defect',[(1,before),(-1,(a[label+'_fine_rhs_binary64'],np.zeros(11135))),(-1,p('fine_rhs_readout_defect'))]);identity('final_rhs_action_residual',[(1,rhs),(-1,pair(a,'final_original_action')),(-1,pair(a,'final_original_residual'))])
  env=a[label+'_residual_update_operation_envelope'];ad=tuple(v[mask] for v in p('completed_correction_action_action_restricted'));aq=tuple(v[mask] for v in p('compression_action_action_restricted'));identity('stored_residual_update_contact',[(1,pair(a,'final_original_residual')),(-1,before),(1,ad),(-1,aq),(-1,p('original_residual_update_identity'))],env)
  c=controls[1];cp='control_%03d_%s_'%(c['ordinal'],c['name']);trip=read(sol,tuple(cp+n for n in ('actual','expected','envelope')));assert np.array_equal(trip[cp+'actual'],total(p('original_residual_update_identity'))) and np.all(trip[cp+'expected']==0) and np.array_equal(trip[cp+'envelope'],env)
  stored=a['final_original_raw_scaled_ratios'];got=ratios(total(pair(a,'final_original_residual')),f,scale);assert stored.shape==(3,2) and np.allclose(got,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(sol['metadata']['original_component_ratios'])) and np.array_equal(a['original_positive_scale'],scale)
  admitted=bool(np.all(stored<=ROW_TOL));assert admitted==r['original_rows_admitted']==sol['metadata']['original_rows_admitted']==sol['metadata']['solver']['all_original_rows_admitted'];global_ratios=np.asarray((np.linalg.norm(total(pair(a,'final_original_residual')))/np.linalg.norm(f),np.linalg.norm(total(pair(a,'final_original_residual'))/scale)/np.linalg.norm(f/scale)));assert np.allclose(global_ratios,a['final_original_global_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(a['final_original_global_ratios'],np.asarray(sol['metadata']['original_global_ratios']))
  projection=r['projection'];projection_admitted=False
  if projection is not None:
   assert admitted and projection in records and projection['metadata']['solution']==thin(sol);pa=read(projection,('compact_weak_TT_original_component_ratios',));pr=pa['compact_weak_TT_original_component_ratios'];assert pr.shape==(3,2) and np.array_equal(pr,np.asarray(projection['metadata']['compact_weak_TT_original_component_ratios']));projection_admitted=bool(np.all(pr<=ROW_TOL));assert projection_admitted==projection['metadata']['compact_weak_TT_original_rows_admitted'] and projection['metadata']['physical_exterior_adopted'] is False
  else:assert not admitted
  assert projection_admitted==r['compact_weak_TT_original_rows_admitted'];roles=[inp,fix,coarse,sol]+([projection] if projection is not None else []);snaps=[q for q in records if q not in roles];assert len(snaps)<=4 and all(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' and q['metadata']['iteration'] in (40,80,120,160) for q in snaps)
  expected='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if admitted else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED');assert r['status']==expected
  report=dict(status='SAVED_TWOLEVEL_YORK_CLOSURE_PASS',producer_status=r['status'],controls=2,committed_pairs=len(records),all_immutable_parent_INPUT_fields_bitcopied=True,distinct_warm_final_solution_fields=11,original_component_ratios=stored.tolist(),original_global_ratios=global_ratios.tolist(),original_rows_admitted=admitted,compact_weak_TT_original_rows_admitted=projection_admitted,iteration_snapshots=len(snaps),coarse_payload_byte_and_schema_authenticated_only=True)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_identity_tolerance=TOL,original_row_tolerance=ROW_TOL,coarse_matrix_products_or_payload_scan=False,L_action_Gram_factorization_triangular_MINRES_projection_FE_or_fixture_replayed=False,physical_adoption=False,scope_limit='Stored words, bitcopies, triplets and norms only; COARSE matrices unopened. Optional projection checks only its stored ratios/flags, not a new weak contraction.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v004.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
