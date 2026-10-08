"""Held stored fine-PCG words/contacts only; no producer or operator replay."""
from pathlib import Path
import ast,hashlib,json,math,os,struct,zipfile
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V006'
OUT='READONLY_FINE_PCG_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=True
SOURCE_SHA='a4c442fa10a50fe63e5cc5c70984786d23e171cd936b5aa6f7313f4ac412b6ef'
PROTOCOL_SHA='5ecfa2446693b60e669a16e6cf2dfb954fd4b67731a30b1a98c412b676287f2d'
TERMINAL=dict(pid=None,result_sha256=None,receipt_sha256=None,error_sha256=None)
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V005'
PARENT_RESULT_SHA='a3aaf3f4b938b621d6491d3fc9fcc4b4a5d2b05e71bf0b4a588eab08d8547ccb'
PARENT_RECEIPT_SHA='eefef813468b05e23aa47a872c3128916d3a93cb45fc55b10cf180244aa3ff5c'
PARENT_PROOF=('READONLY_WARM_TWOLEVEL_YORK_PROJECTION_CLOSURE_V001_RESULT.json','9ba456c04cb20263bf43a5a04325531a727ae5f93a04bbe5608b1deb6c53771b')
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
 assert AUTHOR_DRAFT is False and TERMINAL['pid'] is not None and TERMINAL['receipt_sha256'] is not None and not path(OUT).exists(),'Reviewed actual natural closure required before I/O'
 assert (TERMINAL['result_sha256'] is None)!=(TERMINAL['error_sha256'] is None)
 assert sha('cross_u_compact_york_longitudinal_projection_v006.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 import numpy as np
 selected=[];identities=[]
 def seal(q,output=True):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert (rc['output_sha256'][n] if output else rc['input_sha256'][str(path(n).resolve())])==h and sha(n)==h,n
  assert js(q['commit_file'],q['commit_sha256'])=={n:q[n] for n in ('file','sha256','metadata')}
 def headers(q):
  with zipfile.ZipFile(path(q['file'])) as z:
   assert set(z.namelist())=={n+'.npy' for n in q['metadata']['schema']}|{'metadata_json.npy'}
   for n,s in q['metadata']['schema'].items():
    with z.open(n+'.npy') as f:
     assert f.read(6)==b'\x93NUMPY';v=f.read(2);assert v in (b'\x01\x00',b'\x02\x00',b'\x03\x00');h=struct.unpack('<H' if v[0]==1 else '<I',f.read(2 if v[0]==1 else 4))[0];hd=ast.literal_eval(f.read(h).decode('utf8' if v[0]==3 else 'latin1'))
    assert list(hd['shape'])==s['shape'] and str(np.dtype(hd['descr']))==s['dtype'] and np.dtype(hd['descr']).kind in 'fiub',n
  if closed:assert all(s['finite'] is True for s in q['metadata']['schema'].values())
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
  assert gap.shape==bound.shape and np.all(bound>=0);error=float(np.max(abs(gap)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def row_ratios(res,rhs,scale):
  cuts=(0,3740,7395,11135);out=[]
  for i in range(3):
   s=slice(cuts[i],cuts[i+1]);a=np.linalg.norm(rhs[s]);b=np.linalg.norm(rhs[s]/scale[s]);assert a>0 and b>0;out.append((np.linalg.norm(res[s])/a,np.linalg.norm(res[s]/scale[s])/b))
  return np.asarray(out)
 for q in records:
  seal(q);headers(q);assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=3 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 for c in controls:
  p='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(p+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_FINE_PCG_YORK_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'),original_terminal_status='CLOSED_ERROR')
 else:
  inp,fixture,sol=(r[n] for n in ('input','fixture','solution'));assert all(q in records for q in (inp,fixture,sol)) and len(controls)==3 and all(c['passed'] for c in controls)
  assert r['vector_space_dimension']==11135 and r['coarse_dimension']==2730 and r['cap']==512 and r['solver']=='direct_fine_paired_PCG' and r['automatic_restart'] is False and r['all_full_coupled_map_entries_retained'] is True and r['coarse_Gram_or_fixture_replayed'] is False
  assert all(r[n] is False for n in ('parent_original_rows_admitted','original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
  for n,h in ((PARENT+'_RESULT.json',PARENT_RESULT_SHA),(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA),PARENT_PROOF):assert rc['input_sha256'][str(path(n).resolve())]==h
  old=js(PARENT+'_RESULT.json',PARENT_RESULT_SHA);oldrc=js(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA);proof=js(*PARENT_PROOF)
  assert old['owner']==oldrc['owner'] and old['owner']['pid']==71992 and oldrc['status']=='CLOSED' and oldrc['error_sha256'] is None and oldrc['result_sha256']==PARENT_RESULT_SHA and old['original_rows_admitted'] is False and proof['status']=='SAVED_WARM_TWOLEVEL_YORK_CLOSURE_PASS' and proof['parent']==dict(pid=71992,result_sha256=PARENT_RESULT_SHA,receipt_sha256=PARENT_RECEIPT_SHA,error_sha256=None)
  assert proof['all_immutable_parent_INPUT_fields_bitcopied'] and proof['selected_earned_coarse_fields_bitcopied']==8 and proof['distinct_latest_final_solution_fields']==11
  assert inp['metadata']['kind']=='all_V005_INPUT_and_latest_paired_seed_for_direct_fine_PCG' and inp['metadata']['parent_input']==thin(old['input']) and inp['metadata']['parent_solution']==thin(old['solution']) and inp['metadata']['earned_coarse_ref']==r['earned_coarse_ref']==sol['metadata']['earned_coarse_ref']==old['earned_coarse_ref']
  assert inp['metadata']['all_360_parent_input_fields_bitcopied'] and inp['metadata']['new_latest_solution_prefix']=='fine_pcg_seed_' and inp['metadata']['latest_SOLUTION_loaded_before_INPUT'] and inp['metadata']['coarse_Gram_factor_fixture_or_old_iterations_replayed'] is False and inp['metadata']['cap']==512 and inp['metadata']['no_automatic_restart'] and inp['metadata']['original_row_tolerance']==ROW_TOL
  assert r['preserved_parent_controls']==inp['metadata']['preserved_parent_controls']==old['controls'] and r['preserved_parent_checkpoints']==inp['metadata']['preserved_parent_checkpoints']==old['checkpoints']
  assert fixture['metadata']['kind']=='fresh_coupled_anisotropic_fine_PCG_with_same_generic_loop' and fixture['metadata']['cap']==12 and fixture['metadata']['original_rows_admitted'] and fixture['metadata']['old_York_or_twolevel_fixture_replayed'] is False
  assert sol['metadata']['kind']=='bounded_direct_fine_PCG_original_York_rows' and sol['metadata']['input_ref']==thin(inp) and sol['metadata']['fixture']==thin(fixture) and sol['metadata']['controls']==controls and sol['metadata']['cap']==512 and sol['metadata']['physical_TT_prepared'] is False and sol['metadata']['potential_error_bound_claimed'] is False
  for q in (old['input'],old['solution'],old['earned_coarse_ref']):seal(q,False)
  warm=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale')
  coarse=tuple('new_coarse_'+n for n in ('fine_to_coarse_i','fine_to_coarse_j','physical_node_interpolation_weights','coarse_hat_values_at_fine_cell_corners','coarse_global_local_indices','coarse_mask','coarse_positive_scale','normalized_coarse_Cholesky'))
  assert len(old['input']['metadata']['schema'])==360 and not any(n.startswith('fine_pcg_seed_') for n in old['input']['metadata']['schema'])
  with np.load(path(inp['file']),allow_pickle=False) as new,np.load(path(old['input']['file']),allow_pickle=False) as previous,np.load(path(old['solution']['file']),allow_pickle=False) as latest,np.load(path(old['earned_coarse_ref']['file']),allow_pickle=False) as factor:
   for n,s in old['input']['metadata']['schema'].items():assert inp['metadata']['schema'][n]==s and previous[n].tobytes()==new[n].tobytes(),n
   assert {n for n in inp['metadata']['schema'] if n.startswith('fine_pcg_seed_')}=={'fine_pcg_seed_'+n for n in warm}
   for n in warm:assert inp['metadata']['schema']['fine_pcg_seed_'+n]==old['solution']['metadata']['schema'][n] and latest[n].tobytes()==new['fine_pcg_seed_'+n].tobytes(),n
   for n in coarse:assert factor[n].tobytes()==new['continued_coarse_'+n].tobytes(),n
  ia=read(inp,tuple('fine_pcg_seed_'+n for n in warm)+('rhs_hi','rhs_lo','positive_Jacobi_congruence_scale','compact_vector_mask'));mask=ia['compact_vector_mask'];assert mask.dtype==np.dtype('bool') and mask.shape==(3,87,45) and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
  rhs=tuple(v[mask] for v in pair(ia,'rhs'));f=total(rhs);scale=ia['positive_Jacobi_congruence_scale'][mask];assert np.all(scale>0) and np.array_equal(scale,ia['fine_pcg_seed_original_positive_scale']) and all(np.array_equal(rhs[i],ia['fine_pcg_seed_original_rhs_'+w]) for i,w in enumerate(('hi','lo')))
  label='fine_york_PCG';up=label+'_node_update';bases=('start_nodes','start_original_residual','current_nodes','recursive_residual','new_recursive_residual','fresh_original_residual','fresh_minus_recursive_residual','completed_paired_increment','alpha_Ap','compression_original_action','original_residual_update_contact','fresh_original_original_action','fresh_original_original_residual')
  names=tuple(label+'_'+n+'_'+w for n in bases for w in ('hi','lo'))+tuple(up+'_'+n+'_'+w for n in ('old_nodes','paired_increment','middle_nodes','updated_nodes','total_compression') for w in ('hi','lo'))+(up+'_high_compression',up+'_low_compression',label+'_original_update_contact_envelope',label+'_worst_construction_actual_and_envelope',label+'_history',label+'_iterations_completed',label+'_recursive_drift_norm')+warm
  a=read(sol,names);p=lambda n:pair(a,label+'_'+n);nodes=pair(a,'final_potential_nodes');res=pair(a,'final_original_residual');action=pair(a,'final_original_action')
  for w in (0,1):assert np.array_equal(p('start_nodes')[w],ia['fine_pcg_seed_final_potential_nodes_'+('hi','lo')[w]]) and np.array_equal(p('start_original_residual')[w],ia['fine_pcg_seed_final_original_residual_'+('hi','lo')[w]]) and np.array_equal(p('current_nodes')[w],nodes[w]) and np.array_equal(pair(a,up+'_updated_nodes')[w],nodes[w]) and np.array_equal(p('fresh_original_original_action')[w],action[w]) and np.array_equal(p('fresh_original_original_residual')[w],res[w]) and np.array_equal(p('fresh_original_residual')[w],res[w]) and np.array_equal(pair(a,'original_rhs')[w],rhs[w]) and np.array_equal(p('completed_paired_increment')[w],pair(a,up+'_paired_increment')[w]) and np.array_equal(p('recursive_residual')[w],p('new_recursive_residual')[w])
  oldnodes,middle,newnodes,delta=(pair(a,up+'_'+n) for n in ('old_nodes','middle_nodes','updated_nodes','paired_increment'));qh,ql=a[up+'_high_compression'],a[up+'_low_compression'];q=pair(a,up+'_total_compression')
  for name,words in (('high_word_insertion',(oldnodes[0],oldnodes[1],delta[0],middle[0],middle[1],qh)),('low_word_insertion',(middle[0],middle[1],delta[1],newnodes[0],newnodes[1],ql))):assert all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*words));identities.append(dict(name=name+'_exact_sum',error=0.))
  assert all(math.fsum((x,y,-hi,-lo))==0 for x,y,hi,lo in zip(qh,ql,q[0],q[1]));identities.append(dict(name='total_compression_exact_pair',error=0.))
  identity('final_rhs_action_residual',[(1,rhs),(-1,action),(-1,res)]);identity('stored_fresh_minus_recursive_drift',[(1,res),(-1,p('recursive_residual')),(-1,p('fresh_minus_recursive_residual'))]);assert np.allclose(np.linalg.norm(total(p('fresh_minus_recursive_residual'))),a[label+'_recursive_drift_norm'],rtol=TOL,atol=1e-300)
  gap=p('original_residual_update_contact');env=a[label+'_original_update_contact_envelope'];assert np.all(env>=0);contact_error=float(np.max(abs(total(gap))/np.maximum(env,1e-30),initial=0));assert contact_error<=TOL;identities.append(dict(name='stored_last_original_update_contact_score',error=contact_error,independent_previous_residual_recontraction=False))
  worst=a[label+'_worst_construction_actual_and_envelope'];assert worst.shape==(3,2) and np.all(worst[:,1]>=0);c=controls[2];cp='control_%03d_%s_'%(c['ordinal'],c['name']);trip=read(sol,tuple(cp+n for n in ('actual','expected','envelope')));assert c['name']==label+'_energy_adjoint_and_original_update_construction' and np.array_equal(trip[cp+'actual'],worst[:,0]) and np.all(trip[cp+'expected']==0) and np.array_equal(trip[cp+'envelope'],worst[:,1])
  stored=a['final_original_raw_scaled_ratios'];got=row_ratios(total(res),f,scale);assert stored.shape==(3,2) and np.allclose(got,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(sol['metadata']['original_component_ratios'])) and np.array_equal(a['original_positive_scale'],scale)
  global_ratios=np.asarray((np.linalg.norm(total(res))/np.linalg.norm(f),np.linalg.norm(total(res)/scale)/np.linalg.norm(f/scale)));assert np.allclose(global_ratios,a['final_original_global_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(a['final_original_global_ratios'],np.asarray(sol['metadata']['original_global_ratios']))
  admitted=bool(np.all(stored<=ROW_TOL));solver=sol['metadata']['solver'];assert admitted==r['original_rows_admitted']==sol['metadata']['original_rows_admitted']==solver['all_original_rows_admitted'] and solver['cap']==512 and solver['automatic_restart'] is False and solver['recursive_residual_replaced'] is False and solver['potential_error_bound_claimed'] is False
  iteration=int(a[label+'_iterations_completed']);history=a[label+'_history'];assert 1<=iteration<=512 and iteration==solver['iterations'] and history.ndim==2 and history.shape[1]==11 and len(history)<=iteration and np.array_equal(history[:,0],np.arange(1,len(history)+1))
  if len(history):assert np.array_equal(history[-1,1:7],stored.ravel()) and np.allclose(history[-1,-1],a[label+'_recursive_drift_norm'],rtol=TOL,atol=1e-300)
  projection=r['projection'];projection_admitted=False
  if projection is not None:
   assert admitted and projection in records and projection['metadata']['solution']==thin(sol);pa=read(projection,('compact_weak_TT_original_component_ratios',));pr=pa['compact_weak_TT_original_component_ratios'];assert pr.shape==(3,2) and np.array_equal(pr,np.asarray(projection['metadata']['compact_weak_TT_original_component_ratios']));projection_admitted=bool(np.all(pr<=ROW_TOL));assert projection_admitted==projection['metadata']['compact_weak_TT_original_rows_admitted'] and projection['metadata']['physical_exterior_adopted'] is False
  else:assert not admitted
  assert projection_admitted==r['compact_weak_TT_original_rows_admitted'];roles=[inp,fixture,sol]+([projection] if projection is not None else []);snapshots=[q for q in records if q not in roles];assert len(snapshots)<=4 and all(q['metadata']['kind']=='unqualified_fine_PCG_paired_iterate' and q['metadata']['iteration'] in (64,128,256,512) and q['metadata']['recursive_residual_is_not_admission'] is True for q in snapshots)
  expected='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if admitted else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED');assert r['status']==expected
  report=dict(status='SAVED_FINE_PCG_YORK_CLOSURE_PASS',producer_status=r['status'],controls=3,committed_pairs=len(records),immutable_parent_INPUT_fields=360,all_immutable_parent_INPUT_fields_bitcopied=True,distinct_latest_final_solution_fields=11,selected_earned_coarse_fields_bitcopied=8,original_component_ratios=stored.tolist(),original_global_ratios=global_ratios.tolist(),original_rows_admitted=admitted,compact_weak_TT_original_rows_admitted=projection_admitted,iterations=iteration,snapshots=len(snapshots),stored_last_update_contact_error=contact_error,independent_previous_residual_update_recontraction=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_identity_tolerance=TOL,original_row_tolerance=ROW_TOL,L_point_energy_Gram_triangle_preconditioner_operator_PCG_FE_or_fixture_replayed=False,physical_adoption=False,scope_limit='Stored words, exact insertion sums, copies, triplets and norms only. Energy/adjoint controls are authenticated saved triplets, not recontracted. The last prior original/recursive residual operands are not separately published; its stored update contact score is checked, not independently rederived. Recursive drift is independently checked from saved final residual words. Optional projection uses only stored ratios/flags.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v006.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
