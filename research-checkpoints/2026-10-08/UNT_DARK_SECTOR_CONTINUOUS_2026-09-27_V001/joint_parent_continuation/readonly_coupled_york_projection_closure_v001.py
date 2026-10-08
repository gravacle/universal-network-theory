"""Guard-held saved coupled York words; no map/action/solver/fixture/FE replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V003'
OUT='READONLY_COUPLED_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='4b32c89ca18e9816e16a3ab5fb1516dede0698f470cc510a2523369270a957e8'
PROTOCOL_SHA='738471e1eaa0449bd1f09615c4622c203809cd0bfa87dcbce2d4930898d66b65'
TERMINAL={'pid': 68504, 'result_sha256': '3238ef464e0fde1b66de2a7e1135d57da1d9264e07cdea033cd2e58850059a4e', 'receipt_sha256': 'e49439ec7f6f225851b0777ce0b4f887215721c285530415c1a01a836152683c', 'error_sha256': None}
FAILED_PROOF=('ROOT_YORK_PROJECTION_V002_NATURAL_ERROR_CLOSURE.json','fc4a1fd1eb167f611cebb861aeb724f05a0d3a0abd0fd9833db0ca5b1fd088d2')
PARENT_PROOF=('READONLY_COMPACT_YORK_PROJECTION_CLOSURE_V001_RESULT.json','f88f612a6dea236ff77a2e4bd9571f634fac89608133356679443bf1d0d244c8')
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

def main():
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists()
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_compact_york_longitudinal_projection_v003.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=load_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'])
 assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h and sha(n)==h,n
  assert load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')} and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False and all(s['finite'] is True for s in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=6 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 import numpy as np
 selected=[];identities=[]
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(x):return x[0]+x[1]
 def identity(label,terms,envelope=None):
  parts=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(parts);bound=np.add.reduce([abs(v) for v in parts]) if envelope is None else envelope
  assert gap.shape==bound.shape and np.all(bound>=0);error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def ratios(res,rhs,scale):
  cuts=(0,3740,7395,11135);out=[]
  for i in range(3):
   sl=slice(cuts[i],cuts[i+1]);den=np.linalg.norm(rhs[sl]);wd=np.linalg.norm(rhs[sl]/scale[sl]);assert den>0 and wd>0;out.append((np.linalg.norm(res[sl])/den,np.linalg.norm(res[sl]/scale[sl])/wd))
  return np.asarray(out)
 def stored_ratios(label,a,resname,rhs,scale,name,meta):
  got=ratios(total(pair(a,resname)),rhs,scale);stored=a[name];assert got.shape==stored.shape==(3,2) and np.allclose(got,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(meta)),label
  return bool(np.all(stored<=ROW_TOL))
 def role(kind):
  found=[q for q in records if q['metadata']['kind']==kind];assert len(found)==1,kind;return found[0]
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c
  a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_COUPLED_YORK_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  inp=role('exact_failed_support_cache_and_full_coupled_final_York_iterate');fix=role('fresh_full_coupled_three_by_three_warm_principal_MINRES_control');sol=role('full_coupled_principal_coordinate_warm_York_original_row_result')
  assert r['input']==inp and r['fixture']==fix and r['solution']==sol and 4<=len(controls)<=6 and all(c['passed'] for c in controls)
  assert r['all_full_coupled_map_entries_retained'] is True and r['independent_block_claimed'] is False and r['parent_original_rows_admitted'] is False and r['vector_space_dimension']==11135
  assert all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
  for n,h in (FAILED_PROOF,PARENT_PROOF):assert rc['input_sha256'][str(path(n).resolve())]==h
  failed=load_json(*FAILED_PROOF);parent=load_json(*PARENT_PROOF);assert failed['owner_pid']==66432 and failed['actual_exit_code']==1 and parent['owner_pid']==65789 and parent['original_rows_admitted'] is False
  cache=failed['error_raw_ref'];assert inp['metadata']['failed_cache']=={k:cache[k] for k in ('file','sha256','commit_file','commit_sha256')} and len(cache['metadata']['schema'])==104 and inp['metadata']['all_104_failed_fields_bitcopied'] is True
  for n,h in ((cache['file'],cache['sha256']),(cache['commit_file'],cache['commit_sha256'])):assert rc['input_sha256'][str(path(n).resolve())]==h and sha(n)==h
  assert load_json(cache['commit_file'],cache['commit_sha256'])=={k:cache[k] for k in ('file','sha256','metadata')}
  with np.load(path(cache['file']),allow_pickle=False) as old,np.load(path(inp['file']),allow_pickle=False) as new:
   for n in cache['metadata']['schema']:assert n in inp['metadata']['schema'] and inp['metadata']['schema'][n]==cache['metadata']['schema'][n] and np.array_equal(old[n],new[n]),n
  assert controls[:3]==inp['metadata']['preserved_parent_controls']==r['preserved_parent_controls']==r['preserved_failed_controls'] and fix['metadata']['controls']==controls[3:4]
  names=('rhs_hi','rhs_lo','positive_Jacobi_congruence_scale','compact_vector_mask')+tuple('parent_solution_'+n+'_'+w for n in ('final_potential_nodes','final_original_action','final_original_residual') for w in ('hi','lo'))
  ia=read(inp,names);mask=ia['compact_vector_mask'];assert mask.dtype==np.dtype('bool') and mask.shape==(3,87,45) and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
  rhs=tuple(ia['rhs_'+w][mask] for w in ('hi','lo'));f=total(rhs);scale=ia['positive_Jacobi_congruence_scale'][mask];assert np.all(scale>0)
  previous_nodes=pair(ia,'parent_solution_final_potential_nodes');previous_action=pair(ia,'parent_solution_final_original_action');previous_residual=pair(ia,'parent_solution_final_original_residual');identity('warm_original_rhs_action_residual',[(1,rhs),(-1,previous_action),(-1,previous_residual)])
  blocks=r['blocks'];assert len(blocks)<=2 and len({q['metadata']['group'] for q in blocks})==len(blocks) and len(controls)==4+len(blocks);block_summaries=[]
  for i,q in enumerate(blocks):
   m=q['metadata'];assert q in records and m['kind']=='new_full_coupled_principal_coordinate_York_correction' and m['cap']==160 and m['controls']==controls[4+i:5+i]
   group=m['group'];assert group in ('R_Z','phi') and (i==0 or group=='phi');active=np.arange(7395) if group=='R_Z' else np.arange(7395,11135);rows=np.asarray((0,1)) if group=='R_Z' else np.asarray((2,));label='block_york_'+group;up=label+'_final_update';n=lambda s:label+'_'+s
   bases=('before_nodes','before_action','before_residual','correction_rhs_readout_defect','updated_original_action','updated_original_residual','original_residual_update_identity','correction_action_action_restricted','compression_action_action_restricted')
   names=tuple(n(b)+'_'+w for b in bases for w in ('hi','lo'))+tuple(up+s for s in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes','_full_updated_nodes_hi','_full_updated_nodes_lo','_full_compression_word'))+tuple(n(b) for b in ('active_indices','active_component_rows','completed_block_correction','completed_full_correction','correction_rhs_binary64','updated_original_raw_scaled_ratios','residual_update_operation_envelope'))
   a=read(q,names);s=lambda b:pair(a,n(b));nodes=pair(a,up+'_full_updated_nodes');assert np.array_equal(a[n('active_indices')],active) and np.array_equal(a[n('active_component_rows')],rows)
   inactive=np.ones(11135,bool);inactive[active]=False
   for w in (0,1):assert np.array_equal(s('before_nodes')[w],previous_nodes[w]) and np.array_equal(s('before_action')[w],previous_action[w]) and np.array_equal(s('before_residual')[w],previous_residual[w]) and np.array_equal(pair(a,up+'_old_nodes')[w],previous_nodes[w][active]) and np.array_equal(nodes[w][inactive],previous_nodes[w][inactive]) and np.array_equal(nodes[w][active],pair(a,up+'_updated_nodes')[w])
   delta=a[n('completed_full_correction')];compression=a[up+'_full_compression_word'];assert np.all(delta[inactive]==0) and np.all(compression[inactive]==0) and np.array_equal(delta[active],a[n('completed_block_correction')]) and np.array_equal(delta[active],a[up+'_float_correction']) and np.array_equal(compression[active],a[up+'_exact_update_minus_two_word_nodes'])
   words=[a[up+s] for s in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes')];assert all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*words));identities.append(dict(name=n('exact_active_node_update'),error=0.))
   assert np.array_equal(a[n('correction_rhs_binary64')],total(previous_residual)[active]);identity(n('rhs_readout_defect'),[(1,tuple(v[active] for v in previous_residual)),(-1,(a[n('correction_rhs_binary64')],np.zeros(len(active)))),(-1,s('correction_rhs_readout_defect'))])
   identity(n('original_rhs_action_residual'),[(1,rhs),(-1,s('updated_original_action')),(-1,s('updated_original_residual'))]);ad=tuple(v[mask] for v in s('correction_action_action_restricted'));aq=tuple(v[mask] for v in s('compression_action_action_restricted'));env=a[n('residual_update_operation_envelope')]
   identity(n('stored_full_residual_update_contact'),[(1,s('updated_original_residual')),(-1,previous_residual),(1,ad),(-1,aq),(-1,s('original_residual_update_identity'))],env)
   c=controls[4+i];prefix='control_%03d_%s_'%(c['ordinal'],c['name']);trip=read(q,tuple(prefix+b for b in ('actual','expected','envelope')));assert np.array_equal(trip[prefix+'actual'],total(s('original_residual_update_identity'))) and np.all(trip[prefix+'expected']==0) and np.array_equal(trip[prefix+'envelope'],env)
   admitted=stored_ratios(label,a,n('updated_original_residual'),f,scale,n('updated_original_raw_scaled_ratios'),m['original_component_ratios']);assert admitted==m['original_rows_admitted'];previous_nodes=nodes;previous_action=s('updated_original_action');previous_residual=s('updated_original_residual');block_summaries.append(dict(group=group,original_component_ratios=m['original_component_ratios'],all_original_rows_admitted=admitted))
  names=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('original_positive_scale','final_original_raw_scaled_ratios','final_original_global_ratios');sa=read(sol,names)
  for w in (0,1):assert np.array_equal(pair(sa,'final_potential_nodes')[w],previous_nodes[w]) and np.array_equal(pair(sa,'original_rhs')[w],rhs[w]) and np.array_equal(pair(sa,'final_original_action')[w],previous_action[w]) and np.array_equal(pair(sa,'final_original_residual')[w],previous_residual[w])
  assert np.array_equal(sa['original_positive_scale'],scale) and sol['metadata']['controls']==controls and sol['metadata']['max_groups']==2 and sol['metadata']['cap_per_group']==160
  admitted=stored_ratios('final',sa,'final_original_residual',f,scale,'final_original_raw_scaled_ratios',sol['metadata']['original_component_ratios']);assert admitted==sol['metadata']['original_rows_admitted']==r['original_rows_admitted'];projection=r['projection'];projection_admitted=False
  global_ratios=np.asarray((np.linalg.norm(total(previous_residual))/np.linalg.norm(f),np.linalg.norm(total(previous_residual)/scale)/np.linalg.norm(f/scale)));assert np.allclose(global_ratios,sa['final_original_global_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(sa['final_original_global_ratios'],np.asarray(sol['metadata']['original_global_ratios']))
  if projection is not None:
   assert admitted and projection in records and projection['metadata']['solution']=={k:sol[k] for k in ('file','sha256','commit_file','commit_sha256')};pa=read(projection,('compact_weak_TT_remainder_hi','compact_weak_TT_remainder_lo','compact_weak_TT_original_component_ratios'))
   projection_admitted=stored_ratios('saved_projection',pa,'compact_weak_TT_remainder',f,scale,'compact_weak_TT_original_component_ratios',projection['metadata']['compact_weak_TT_original_component_ratios']);assert projection_admitted==projection['metadata']['compact_weak_TT_original_rows_admitted']==r['compact_weak_TT_original_rows_admitted']
  else:assert not admitted and r['compact_weak_TT_original_rows_admitted'] is False
  roles=[inp,fix,sol]+blocks+([projection] if projection is not None else []);snapshots=[q for q in records if q not in roles];assert len(snapshots)<=8 and all(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' and q['metadata']['iteration'] in (40,80,120,160) for q in snapshots)
  expected='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if admitted else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED');assert r['status']==expected
  report=dict(status='SAVED_COUPLED_YORK_CLOSURE_PASS',producer_status=r['status'],controls=len(controls),committed_pairs=len(records),blocks=block_summaries,iteration_snapshots=len(snapshots),all_104_cache_fields_and_full_maps_bitcopied=True,original_component_ratios=sa['final_original_raw_scaled_ratios'].tolist(),original_global_ratios=global_ratios.tolist(),original_rows_admitted=admitted,compact_weak_TT_original_rows_admitted=projection_admitted,original_primitive_bridge_resolved=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_identity_tolerance=TOL,original_row_tolerance=ROW_TOL,scope_limit='Saved words, exact copies, triplets and norms only; no L/raised tensor/action/solver/fixture/projection/scatter replay; optional projection only stored weak ratios',York_operator_solver_fixture_or_projection_replayed=False,physical_adoption=False)
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v003.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
