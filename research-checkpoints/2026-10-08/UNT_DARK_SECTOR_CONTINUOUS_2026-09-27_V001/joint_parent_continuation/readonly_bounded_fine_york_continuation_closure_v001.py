"""Held saved V009 words only; no PCG/action/preconditioner/fixture replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V009'
OUT='READONLY_BOUNDED_FINE_YORK_CONTINUATION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='cbce8853b1acd073441bd436ec8d0bb04397ff4967a74ee88243e61318792662'
PROTOCOL_SHA='6c7566b4e50ed79949dc3311856ad9d0bd146dd62f12e870bfc6c9c86d1cf109'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V007'
PARENT_TERMINAL=dict(pid=76118,result_sha256='578759e107965e270912ebad70d3fc81511d14433da000ccbbd475ec40e49156',receipt_sha256='131c1305ec5972901e67210064040da4c362ffba6337a8a37d943cb9c46f8166',error_sha256=None)
PROOF=('READONLY_FINE_PCG_YORK_PROJECTION_CLOSURE_V002_RESULT.json','fba4af99b57959a4e136b21b6738c03a8f185a7ec0898822192af9ad9f8bd0b8')
TOL=2e-11;ROW_TOL=1e-10
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
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists(),'Reviewed natural closure required before I/O'
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_compact_york_longitudinal_projection_v009.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and r['owner']==rc['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 old=js(PARENT+'_RESULT.json',PARENT_TERMINAL['result_sha256']);oldrc=js(PARENT+'_RECEIPT.json',PARENT_TERMINAL['receipt_sha256']);proof=js(*PROOF)
 for n,h in ((PARENT+'_RESULT.json',PARENT_TERMINAL['result_sha256']),(PARENT+'_RECEIPT.json',PARENT_TERMINAL['receipt_sha256']),PROOF):assert rc['input_sha256'][str(path(n).resolve())]==h
 assert oldrc['status']=='CLOSED' and old['owner']==oldrc['owner'] and old['owner']['pid']==76118 and old['status']=='ORIGINAL_YORK_ROWS_NOT_ADMITTED' and old['original_rows_admitted'] is False and old['projection'] is None and len(old['controls'])==4 and len(old['checkpoints'])==8
 assert proof['status']=='SAVED_CACHED_FINE_PCG_YORK_CLOSURE_PASS' and proof['parent']==PARENT_TERMINAL and proof['iterations']==512 and proof['controls']==4 and proof['committed_pairs']==8 and proof['original_rows_admitted'] is False and proof['physical_adoption'] is False
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records) and {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 import numpy as np
 selected=[];identities=[]
 def seal(q,output=True):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert (rc['output_sha256'][n] if output else rc['input_sha256'][str(path(n).resolve())])==h and sha(n)==h,n
  commit=js(q['commit_file'],q['commit_sha256']);assert commit['file']==q['file'] and commit['sha256']==q['sha256'] and ('metadata' not in q or commit['metadata']==q['metadata'])
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and sc[n]['finite'] and np.all(np.isfinite(a)),n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(x):return x[0]+x[1]
 def identity(n,terms,envelope=None):
  words=[s*v for s,p in terms for v in p];gap=np.add.reduce(words);bound=np.add.reduce([abs(v) for v in words]) if envelope is None else envelope
  assert gap.shape==bound.shape and np.all(bound>=0);error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(n,error);identities.append(dict(name=n,error=error))
 def ratios(res,rhs,scale):
  cuts=(0,3740,7395,11135);scores=[]
  for i in range(3):
   s=slice(cuts[i],cuts[i+1]);a=np.linalg.norm(rhs[s]);b=np.linalg.norm(rhs[s]/scale[s]);assert a>0 and b>0;scores.append((np.linalg.norm(res[s])/a,np.linalg.norm(res[s]/scale[s])/b))
  return np.asarray(scores)
 for q in records:
  seal(q);assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False and all(s['finite'] for s in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=5 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_BOUNDED_FINE_YORK_CONTINUATION_FAILURE_PRESERVED',controls=len(controls),committed_pairs=len(records),context=r.get('context'),original_terminal_status='CLOSED_ERROR',saved_recurrence_contacts_audited=False)
 else:
  inp,fixture,sol=(r[n] for n in ('input','fixture','solution'));assert all(q in records for q in (inp,fixture,sol)) and len(controls)==5 and all(c['passed'] for c in controls)
  assert r['parent_terminal']==PARENT_TERMINAL and r['parent_proof']==dict(file=PROOF[0],sha256=PROOF[1],status=proof['status']) and r['preserved_parent_controls']==old['controls'] and r['preserved_parent_checkpoints']==[thin(q) for q in old['checkpoints']]
  assert r['vector_space_dimension']==11135 and r['coarse_dimension']==2730 and r['additional_cap']==64 and r['total_step_budget_upper']==576 and r['prior_512_original_nonadmission_preserved'] is True and r['all_full_coupled_map_entries_retained'] is True and all(r[n] is False for n in ('recursive_residual_replaced','automatic_restart','automatic_extension','original_primitive_bridge_resolved','continuum_TT_prepared','physical_adoption'))
  md=inp['metadata'];assert md['kind']=='selected_completed512_fine_system_and_exact_next_recurrence_state' and md['parent_input']==thin(old['input']) and md['parent_solution']==thin(old['solution']) and md['prior_solver']==old['solution']['metadata']['solver'] and md['selected_input_fields']==27 and md['selected_solution_fields']==38 and md['old_first_action_preconditioner_fixture_Gram_or_factor_replayed'] is False
  ia={};copies=0
  for q,prefix,count in ((old['input'],'continued_V007_INPUT_',27),(old['solution'],'continued_V007_SOLUTION_',38)):
   seal(q,False);names=[n for n in q['metadata']['schema'] if prefix+n in inp['metadata']['schema']];assert len(names)==count;original=read(q,names);copied=read(inp,[prefix+n for n in names])
   for n in names:assert inp['metadata']['schema'][prefix+n]==q['metadata']['schema'][n] and original[n].tobytes()==copied[prefix+n].tobytes();ia[prefix+n]=copied[prefix+n];copies+=1
  assert copies==65 and len(inp['metadata']['schema'])==65
  fm=fixture['metadata'];assert fm['kind']=='NEW_explicit_1_plus_5_vs_6_step_paired_PCG_continuation_known_solution' and fm['controls']==controls[:4] and fm['both_final_node_and_residual_words_exact'] is True and fm['old_fixture_or_original_action_replayed'] is False
  fn=('fresh_split_completed_uninterrupted_nodes','fresh_split_completed_uninterrupted_residual','fresh_split_final_nodes','fresh_split_suffix_fresh_original_residual');fa=read(fixture,tuple(n+'_'+w for n in fn for w in ('hi','lo')))
  for w in (0,1):assert np.array_equal(pair(fa,fn[0])[w],pair(fa,fn[2])[w]) and np.array_equal(pair(fa,fn[1])[w],pair(fa,fn[3])[w])
  assert fm['uninterrupted']['iterations']==fm['prefix']['iterations']+fm['suffix']['iterations'] and fm['prefix']['iterations']==1 and fm['prefix']['all_original_rows_admitted'] is False and fm['uninterrupted']['all_original_rows_admitted'] is True and fm['suffix']['all_original_rows_admitted'] is True
  label='continued_fine_york_PCG';up=label+'_node_update';warm=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale')
  bases=('start_nodes','start_original_residual','carried_recursive_residual','carried_previous_direction','carried_previous_Ap','current_nodes','recursive_residual');a=read(sol,tuple(label+'_'+n+'_'+w for n in bases for w in ('hi','lo'))+(label+'_carried_previous_Ap_envelope',label+'_carried_next_rho',label+'_worst_construction_actual_and_envelope',label+'_history',label+'_iterations_completed')+warm);p=lambda n:pair(a,label+'_'+n)
  mask=ia['continued_V007_INPUT_compact_vector_mask'];assert mask.dtype==np.dtype('bool') and mask.shape==(3,87,45) and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)));rhs=tuple(ia['continued_V007_INPUT_rhs_'+w][mask] for w in ('hi','lo'));f=total(rhs);scale=ia['continued_V007_INPUT_positive_Jacobi_congruence_scale'][mask];assert np.all(scale>0)
  for new,oldname in (('start_nodes','final_potential_nodes'),('start_original_residual','final_original_residual'),('carried_recursive_residual','fine_york_PCG_recursive_residual'),('carried_previous_direction','fine_york_PCG_previous_search_direction'),('carried_previous_Ap','fine_york_PCG_previous_Ap')):
   for w in (0,1):assert np.array_equal(p(new)[w],ia['continued_V007_SOLUTION_'+oldname+'_'+('hi','lo')[w]])
  assert np.array_equal(a[label+'_carried_previous_Ap_envelope'],ia['continued_V007_SOLUTION_fine_york_PCG_direction_action_positive_positive_scatter'][mask]) and np.array_equal(a[label+'_carried_next_rho'],ia['continued_V007_SOLUTION_fine_york_PCG_current_rz_inner_binary64_readout'])
  nodes=pair(a,'final_potential_nodes');res=pair(a,'final_original_residual');action=pair(a,'final_original_action')
  for w in (0,1):assert np.array_equal(nodes[w],p('current_nodes')[w]) and np.array_equal(pair(a,'original_rhs')[w],rhs[w])
  identity('final_original_rhs_action_residual',[(1,rhs),(-1,action),(-1,res)])
  has_update=up+'_updated_nodes_hi' in sol['metadata']['schema'];contact_error=None
  if has_update:
   ns=('new_recursive_residual','fresh_original_residual','fresh_minus_recursive_residual','completed_paired_increment','alpha_Ap','compression_original_action','original_residual_update_contact','before_update_original_residual','before_update_recursive_residual','fresh_original_original_action','fresh_original_original_residual')
   a.update(read(sol,tuple(label+'_'+n+'_'+w for n in ns for w in ('hi','lo'))+tuple(up+'_'+n+'_'+w for n in ('old_nodes','paired_increment','middle_nodes','updated_nodes','total_compression') for w in ('hi','lo'))+(up+'_high_compression',up+'_low_compression',label+'_original_update_contact_envelope',label+'_recursive_drift_norm')))
   for w in (0,1):assert np.array_equal(pair(a,up+'_updated_nodes')[w],nodes[w]) and np.array_equal(p('fresh_original_original_action')[w],action[w]) and np.array_equal(p('fresh_original_original_residual')[w],res[w]) and np.array_equal(p('fresh_original_residual')[w],res[w]) and np.array_equal(p('completed_paired_increment')[w],pair(a,up+'_paired_increment')[w]) and np.array_equal(p('recursive_residual')[w],p('new_recursive_residual')[w])
   oldnodes,middle,newnodes,delta=(pair(a,up+'_'+n) for n in ('old_nodes','middle_nodes','updated_nodes','paired_increment'));qh,ql=a[up+'_high_compression'],a[up+'_low_compression'];q=pair(a,up+'_total_compression')
   for n,words in (('high_word_insertion',(oldnodes[0],oldnodes[1],delta[0],middle[0],middle[1],qh)),('low_word_insertion',(middle[0],middle[1],delta[1],newnodes[0],newnodes[1],ql))):assert all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*words));identities.append(dict(name=n+'_exact_sum',error=0.))
   assert all(math.fsum((x,y,-hi,-lo))==0 for x,y,hi,lo in zip(qh,ql,q[0],q[1]));env=a[label+'_original_update_contact_envelope'];gap=p('original_residual_update_contact')
   identity('saved_original_residual_update',[(1,res),(-1,p('before_update_original_residual')),(1,p('alpha_Ap')),(-1,p('compression_original_action')),(-1,gap)],env)
   identity('saved_recursive_residual_update',[(1,p('recursive_residual')),(-1,p('before_update_recursive_residual')),(1,p('alpha_Ap')),(-1,p('compression_original_action'))],env+abs(total(p('recursive_residual')))+abs(total(p('before_update_recursive_residual'))))
   identity('saved_fresh_minus_recursive_drift',[(1,res),(-1,p('recursive_residual')),(-1,p('fresh_minus_recursive_residual'))]);assert np.allclose(np.linalg.norm(total(p('fresh_minus_recursive_residual'))),a[label+'_recursive_drift_norm'],rtol=TOL,atol=1e-300)
   contact_error=float(np.max(abs(total(gap))/np.maximum(env,1e-30),initial=0));assert contact_error<=TOL
  else:
   assert sol['metadata']['solver']['reason']=='nonpositive_or_null_numerical_curvature_with_unadmitted_original_rows'
   for w in (0,1):assert np.array_equal(nodes[w],p('start_nodes')[w]) and np.array_equal(res[w],p('start_original_residual')[w])
  worst=a[label+'_worst_construction_actual_and_envelope'];assert worst.shape==(3,2) and np.all(worst[:,1]>=0);c=controls[4];cp='control_004_'+c['name']+'_';trip=read(sol,tuple(cp+n for n in ('actual','expected','envelope')));assert c['name']==label+'_energy_adjoint_and_original_update_construction' and np.array_equal(trip[cp+'actual'],worst[:,0]) and np.all(trip[cp+'expected']==0) and np.array_equal(trip[cp+'envelope'],worst[:,1])
  stored=a['final_original_raw_scaled_ratios'];got=ratios(total(res),f,scale);global_scores=np.asarray((np.linalg.norm(total(res))/np.linalg.norm(f),np.linalg.norm(total(res)/scale)/np.linalg.norm(f/scale)));assert np.allclose(got,stored,rtol=TOL,atol=1e-300) and np.allclose(global_scores,a['final_original_global_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(sol['metadata']['original_component_ratios'])) and np.array_equal(a['original_positive_scale'],scale)
  admitted=bool(np.all(stored<=ROW_TOL));solver=sol['metadata']['solver'];iteration=int(a[label+'_iterations_completed']);history=a[label+'_history'];assert admitted==r['original_rows_admitted']==sol['metadata']['original_rows_admitted']==solver['all_original_rows_admitted'] and solver['cap']==solver['additional_cap']==64 and solver['parent_iterations']==512 and solver['total_iterations']==512+iteration and solver['iterations']==iteration and 1<=iteration<=64 and all(solver[n] is False for n in ('automatic_restart','recursive_residual_replaced','automatic_extension','potential_error_bound_claimed'))
  assert history.ndim==2 and history.shape[1]==11 and len(history)<=iteration and np.array_equal(history[:,0],np.arange(1,len(history)+1))
  if len(history):assert np.array_equal(history[-1,1:7],stored.ravel())
  assert sol['metadata']['input_ref']==thin(inp) and sol['metadata']['fresh_split_fixture']==thin(fixture) and sol['metadata']['controls']==controls and sol['metadata']['same_original_six_gates'] is True
  projection=r['projection'];projection_admitted=False
  if projection is not None:
   assert admitted and projection in records and projection['metadata']['solution']==thin(sol);pr=read(projection,('compact_weak_TT_original_component_ratios',))['compact_weak_TT_original_component_ratios'];assert pr.shape==(3,2) and np.array_equal(pr,np.asarray(projection['metadata']['compact_weak_TT_original_component_ratios']));projection_admitted=bool(np.all(pr<=ROW_TOL));assert projection_admitted==projection['metadata']['compact_weak_TT_original_rows_admitted'] and projection['metadata']['physical_exterior_adopted'] is False
  else:assert not admitted
  roles=[inp,fixture,sol]+([projection] if projection is not None else []);snapshots=[q for q in records if q not in roles];assert len(snapshots)<=3 and all(q['metadata']['kind']=='unqualified_fine_PCG_paired_iterate' and q['metadata']['iteration'] in (16,32,64) and q['metadata']['cap']==64 and q['metadata']['recursive_residual_is_not_admission'] is True for q in snapshots)
  expected='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if admitted else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED');assert r['status']==expected and r['compact_weak_TT_original_rows_admitted']==projection_admitted
  report=dict(status='SAVED_BOUNDED_FINE_YORK_CONTINUATION_CLOSURE_PASS',producer_status=r['status'],controls=5,committed_pairs=len(records),selected_parent_bitcopies=65,original_component_ratios=stored.tolist(),original_global_ratios=global_scores.tolist(),original_rows_admitted=admitted,compact_weak_TT_original_rows_admitted=projection_admitted,additional_iterations=iteration,total_iterations=512+iteration,snapshots=len(snapshots),actual_node_update_earned=has_update,stored_last_update_contact_error=contact_error,saved_recurrence_contacts_audited=has_update)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,original_V007_terminal=PARENT_TERMINAL,original_V007_proof=dict(file=PROOF[0],sha256=PROOF[1]),prior_512_nonadmission_preserved=True,selected=selected,identities=identities,arithmetic_tolerance=TOL,original_row_tolerance=ROW_TOL,automatic_extension=False,operator_preconditioner_PCG_energy_Gram_factorization_projection_FE_or_fixture_replayed=False,physical_adoption=False,scope_limit='Selected sealed words/copies, stored triplets, exact insertion sums, last residual-update/drift identities and original norms only. Carried next z/rz/rho/search direction are authenticated INPUT copies; saved start/carried previous direction/action and rho are tied separately. No start preconditioner, recurrence, point energy/adjoint, original action, projection or fresh fixture is rerun; energy/adjoint validity is retained through stored controls. No physical/rank/finite-preparation claim.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v009.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA and sha(PROOF[0])==PROOF[1]
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
