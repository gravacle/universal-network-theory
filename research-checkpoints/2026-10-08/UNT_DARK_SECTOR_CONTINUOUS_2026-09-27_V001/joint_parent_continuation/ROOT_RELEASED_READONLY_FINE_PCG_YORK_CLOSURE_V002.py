"""Held stored fine-PCG words/contacts only; no producer or operator replay."""
from pathlib import Path
import ast,hashlib,json,math,os,struct,zipfile
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V007'
OUT='READONLY_FINE_PCG_YORK_PROJECTION_CLOSURE_V002_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='25a96063c97b691440401a2b32f6b1b93919f3211d9d5f3747fd67d0a93d038b'
PROTOCOL_SHA='97e1277e87e41fcd9c93c00754eae08d645948b906e8aa80a99cc61919845266'
TERMINAL={'pid': 76118, 'result_sha256': '578759e107965e270912ebad70d3fc81511d14433da000ccbbd475ec40e49156', 'receipt_sha256': '131c1305ec5972901e67210064040da4c362ffba6337a8a37d943cb9c46f8166', 'error_sha256': None}
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V006'
PARENT_ERROR_SHA='3b0418ecfc32f540e50bc7220c5f4748e5e16b910dfedaf273789c2c0449b627'
PARENT_RECEIPT_SHA='73db4994b09f24d11b6d7aa4951c5e320ae7fb97fe372a825908df6119e05860'
PARENT_PROOF=('READONLY_FINE_PCG_YORK_PROJECTION_CLOSURE_V001_RESULT.json','c50f785638cd9f3130d6e4d6ce1898780c160324cecc3327563082044136ab6f')
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
 assert sha('cross_u_compact_york_longitudinal_projection_v007.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 receipt=STEM+('_ERROR_RECEIPT.json' if TERMINAL['error_sha256'] is not None and path(STEM+'_ERROR_RECEIPT.json').exists() else '_RECEIPT.json');rc=js(receipt,TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=js(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256']);assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256']
 assert rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 import numpy as np
 selected=[];identities=[]
 def seal(q,output=True):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert (rc['output_sha256'][n] if output else rc['input_sha256'][str(path(n).resolve())])==h and sha(n)==h,n
  commit=js(q['commit_file'],q['commit_sha256']);assert commit['file']==q['file'] and commit['sha256']==q['sha256'] and ('metadata' not in q or commit['metadata']==q['metadata'])
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
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=4 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 for c in controls:
  p='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(p+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,c;a=read(found[0],names)
  for q in found[1:]:
   b=read(q,names);assert all(np.array_equal(a[n],b[n]) for n in names)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_CACHED_FINE_PCG_YORK_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'),original_terminal_status='CLOSED_ERROR')
 else:
  inp,earned,association,sol=(r[n] for n in ('input','earned_fixture','association','solution'));assert all(q in records for q in (inp,earned,association,sol)) and len(controls)==4 and all(c['passed'] for c in controls)
  assert r['vector_space_dimension']==11135 and r['coarse_dimension']==2730 and r['cap']==512 and r['automatic_restart'] is False and r['all_full_coupled_map_entries_retained'] is True and r['initial_B_or_first_A_or_old_fixture_replayed'] is False and r['original_failed_publication_preserved'] is True
  assert all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
  for n,h in ((PARENT+'_ERROR.json',PARENT_ERROR_SHA),(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA),PARENT_PROOF):assert rc['input_sha256'][str(path(n).resolve())]==h
  old=js(PARENT+'_ERROR.json',PARENT_ERROR_SHA);oldrc=js(PARENT+'_RECEIPT.json',PARENT_RECEIPT_SHA);proof=js(*PARENT_PROOF)
  prior_t=dict(pid=74275,result_sha256=None,error_sha256=PARENT_ERROR_SHA,receipt_sha256=PARENT_RECEIPT_SHA)
  assert old['owner']==oldrc['owner'] and old['owner']['pid']==74275 and oldrc['status']=='CLOSED_ERROR' and oldrc['error_sha256']==PARENT_ERROR_SHA and oldrc.get('result_sha256') is None and proof['status']=='SAVED_FINE_PCG_YORK_FAILURE_PRESERVED' and proof['parent']==prior_t and proof['actual_node_update_earned'] is False
  oldinp,oldfixture,oldraw=old['checkpoints'];assert [len(q['metadata']['schema']) for q in (oldinp,oldfixture,oldraw)]==[478,178,59] and len(old['controls'])==2
  assert inp['metadata']['kind']=='all_failed_V006_INPUT_and_first_direction_words_before_unearned_energy' and inp['metadata']['failed_terminal']==r['failed_terminal']==prior_t and inp['metadata']['failed_input']==thin(oldinp) and inp['metadata']['failed_fixture']==thin(oldfixture) and inp['metadata']['failed_raw']==thin(oldraw)
  assert all(inp['metadata'][n] is True for n in ('all_478_input_fields_bitcopied','all_178_fixture_fields_bitcopied','all_59_failed_raw_fields_bitcopied')) and inp['metadata']['fixture_prefix']=='cached_V006_FIXTURE_' and inp['metadata']['raw_prefix']=='cached_V006_RAW_' and inp['metadata']['initial_B_and_first_A_and_positive_bounds_replayed'] is False and inp['metadata']['original_fixture_replayed'] is False and inp['metadata']['same_original_cap']==512 and inp['metadata']['new_node_updates_previously_earned']==0
  assert r['preserved_failed_controls']==inp['metadata']['preserved_failed_controls']==old['controls']==controls[:2] and r['preserved_failed_checkpoints']==inp['metadata']['preserved_failed_checkpoints']==old['checkpoints']
  assert earned['metadata']['kind']=='earned_failed_V006_fresh_fixture_wordcopies' and earned['metadata']['failed_fixture']==thin(oldfixture) and earned['metadata']['controls']==controls[:2] and earned['metadata']['fixture_called'] is False
  assert association['metadata']['kind']=='new_exact_dyadic_weighted_energy_association' and association['metadata']['old_unweighted_product_exponent']==-455 and association['metadata']['exact_weighted_energy_exponent']==-435 and association['metadata']['exact_words_required'] is True and association['metadata']['old_fixture_replayed'] is False and association['metadata']['controls']==controls[:3]
  assert sol['metadata']['kind']=='same_fine_PCG_after_cached_first_direction_weight_association_repair' and sol['metadata']['input_ref']==thin(inp) and sol['metadata']['earned_fixture']==thin(earned) and sol['metadata']['association']==thin(association) and sol['metadata']['controls']==controls and sol['metadata']['cap']==512 and sol['metadata']['physical_TT_prepared'] is False and sol['metadata']['potential_error_bound_claimed'] is False
  for q in (oldinp,oldfixture,oldraw):seal(q,False)
  with np.load(path(inp['file']),allow_pickle=False) as new,np.load(path(earned['file']),allow_pickle=False) as copiedfixture:
   for q,prefix in ((oldinp,''),(oldfixture,'cached_V006_FIXTURE_'),(oldraw,'cached_V006_RAW_')):
    with np.load(path(q['file']),allow_pickle=False) as original:
     for n,sc in q['metadata']['schema'].items():assert inp['metadata']['schema'][prefix+n]==sc and original[n].tobytes()==new[prefix+n].tobytes(),prefix+n
     if q==oldfixture:
      assert earned['metadata']['schema']==oldfixture['metadata']['schema']
      for n in q['metadata']['schema']:assert original[n].tobytes()==copiedfixture[n].tobytes(),n
  tiny=read(association,tuple('fresh_reassociated_'+n for n in ('exact_expected','exact_normalized_energy'))+tuple('fresh_reassociated_point_energy_'+w for w in ('hi','lo')))
  assert np.array_equal(tiny['fresh_reassociated_point_energy_hi'],tiny['fresh_reassociated_exact_expected']) and np.all(tiny['fresh_reassociated_point_energy_lo']==0) and float(tiny['fresh_reassociated_exact_expected'])==2.**-435 and float(tiny['fresh_reassociated_exact_normalized_energy'])==1.
  assert controls[2]['name']=='fresh_reassociated_tiny_weighted_energy_exact_words';identities.append(dict(name='saved_tiny_weighted_energy_exact_words',error=0.,denominator_floor_used=False))
  warm=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale')
  ia=read(inp,tuple('fine_pcg_seed_'+n for n in warm)+('rhs_hi','rhs_lo','positive_Jacobi_congruence_scale','compact_vector_mask'));mask=ia['compact_vector_mask'];assert mask.dtype==np.dtype('bool') and mask.shape==(3,87,45) and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
  rhs=tuple(v[mask] for v in pair(ia,'rhs'));f=total(rhs);scale=ia['positive_Jacobi_congruence_scale'][mask];assert np.all(scale>0) and np.array_equal(scale,ia['fine_pcg_seed_original_positive_scale']) and all(np.array_equal(rhs[i],ia['fine_pcg_seed_original_rhs_'+w]) for i,w in enumerate(('hi','lo')))
  label='fine_york_PCG';up=label+'_node_update';has_update=up+'_updated_nodes_hi' in sol['metadata']['schema']
  names=tuple(label+'_'+n+'_'+w for n in ('start_nodes','start_original_residual','current_nodes','recursive_residual') for w in ('hi','lo'))+(label+'_worst_construction_actual_and_envelope',label+'_history',label+'_iterations_completed')+warm
  a=read(sol,names);p=lambda n:pair(a,label+'_'+n);nodes=pair(a,'final_potential_nodes');res=pair(a,'final_original_residual');action=pair(a,'final_original_action')
  for w in (0,1):assert np.array_equal(p('start_nodes')[w],ia['fine_pcg_seed_final_potential_nodes_'+('hi','lo')[w]]) and np.array_equal(p('start_original_residual')[w],ia['fine_pcg_seed_final_original_residual_'+('hi','lo')[w]]) and np.array_equal(p('current_nodes')[w],nodes[w]) and np.array_equal(pair(a,'original_rhs')[w],rhs[w])
  identity('final_rhs_action_residual',[(1,rhs),(-1,action),(-1,res)])
  if has_update:
   bases=('new_recursive_residual','fresh_original_residual','fresh_minus_recursive_residual','completed_paired_increment','alpha_Ap','compression_original_action','original_residual_update_contact','before_update_original_residual','before_update_recursive_residual','fresh_original_original_action','fresh_original_original_residual')
   names=tuple(label+'_'+n+'_'+w for n in bases for w in ('hi','lo'))+tuple(up+'_'+n+'_'+w for n in ('old_nodes','paired_increment','middle_nodes','updated_nodes','total_compression') for w in ('hi','lo'))+(up+'_high_compression',up+'_low_compression',label+'_original_update_contact_envelope',label+'_recursive_drift_norm')
   a.update(read(sol,names))
   for w in (0,1):assert np.array_equal(pair(a,up+'_updated_nodes')[w],nodes[w]) and np.array_equal(p('fresh_original_original_action')[w],action[w]) and np.array_equal(p('fresh_original_original_residual')[w],res[w]) and np.array_equal(p('fresh_original_residual')[w],res[w]) and np.array_equal(p('completed_paired_increment')[w],pair(a,up+'_paired_increment')[w]) and np.array_equal(p('recursive_residual')[w],p('new_recursive_residual')[w])
   oldnodes,middle,newnodes,delta=(pair(a,up+'_'+n) for n in ('old_nodes','middle_nodes','updated_nodes','paired_increment'));qh,ql=a[up+'_high_compression'],a[up+'_low_compression'];q=pair(a,up+'_total_compression')
   for name,words in (('high_word_insertion',(oldnodes[0],oldnodes[1],delta[0],middle[0],middle[1],qh)),('low_word_insertion',(middle[0],middle[1],delta[1],newnodes[0],newnodes[1],ql))):assert all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*words));identities.append(dict(name=name+'_exact_sum',error=0.))
   assert all(math.fsum((x,y,-hi,-lo))==0 for x,y,hi,lo in zip(qh,ql,q[0],q[1]));identities.append(dict(name='total_compression_exact_pair',error=0.))
   gap=p('original_residual_update_contact');env=a[label+'_original_update_contact_envelope'];assert np.all(env>=0)
   identity('independent_saved_original_update_contact',[(1,res),(-1,p('before_update_original_residual')),(1,p('alpha_Ap')),(-1,p('compression_original_action')),(-1,gap)],env)
   identity('saved_recursive_update',[(1,p('recursive_residual')),(-1,p('before_update_recursive_residual')),(1,p('alpha_Ap')),(-1,p('compression_original_action'))],env+abs(total(p('recursive_residual')))+abs(total(p('before_update_recursive_residual'))))
   identity('stored_fresh_minus_recursive_drift',[(1,res),(-1,p('recursive_residual')),(-1,p('fresh_minus_recursive_residual'))]);assert np.allclose(np.linalg.norm(total(p('fresh_minus_recursive_residual'))),a[label+'_recursive_drift_norm'],rtol=TOL,atol=1e-300)
   contact_error=float(np.max(abs(total(gap))/np.maximum(env,1e-30),initial=0));assert contact_error<=TOL;identities.append(dict(name='stored_last_original_update_contact_score',error=contact_error,independent_previous_residual_recontraction=True))
  else:
   assert sol['metadata']['solver']['reason']=='nonpositive_or_null_numerical_curvature_with_unadmitted_original_rows'
   for w in (0,1):assert np.array_equal(nodes[w],p('start_nodes')[w]) and np.array_equal(res[w],p('start_original_residual')[w])
   contact_error=None
  worst=a[label+'_worst_construction_actual_and_envelope'];assert worst.shape==(3,2) and np.all(worst[:,1]>=0);c=controls[3];cp='control_%03d_%s_'%(c['ordinal'],c['name']);trip=read(sol,tuple(cp+n for n in ('actual','expected','envelope')));assert c['name']==label+'_energy_adjoint_and_original_update_construction' and np.array_equal(trip[cp+'actual'],worst[:,0]) and np.all(trip[cp+'expected']==0) and np.array_equal(trip[cp+'envelope'],worst[:,1])
  stored=a['final_original_raw_scaled_ratios'];got=row_ratios(total(res),f,scale);assert stored.shape==(3,2) and np.allclose(got,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(sol['metadata']['original_component_ratios'])) and np.array_equal(a['original_positive_scale'],scale)
  global_ratios=np.asarray((np.linalg.norm(total(res))/np.linalg.norm(f),np.linalg.norm(total(res)/scale)/np.linalg.norm(f/scale)));assert np.allclose(global_ratios,a['final_original_global_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(a['final_original_global_ratios'],np.asarray(sol['metadata']['original_global_ratios']))
  admitted=bool(np.all(stored<=ROW_TOL));solver=sol['metadata']['solver'];assert admitted==r['original_rows_admitted']==sol['metadata']['original_rows_admitted']==solver['all_original_rows_admitted'] and solver['cap']==512 and solver['automatic_restart'] is False and solver['recursive_residual_replaced'] is False and solver['potential_error_bound_claimed'] is False
  iteration=int(a[label+'_iterations_completed']);history=a[label+'_history'];assert 1<=iteration<=512 and iteration==solver['iterations'] and history.ndim==2 and history.shape[1]==11 and len(history)<=iteration and np.array_equal(history[:,0],np.arange(1,len(history)+1))
  if len(history):assert np.array_equal(history[-1,1:7],stored.ravel()) and np.allclose(history[-1,-1],a[label+'_recursive_drift_norm'],rtol=TOL,atol=1e-300)
  projection=r['projection'];projection_admitted=False
  if projection is not None:
   assert admitted and projection in records and projection['metadata']['solution']==thin(sol);pa=read(projection,('compact_weak_TT_original_component_ratios',));pr=pa['compact_weak_TT_original_component_ratios'];assert pr.shape==(3,2) and np.array_equal(pr,np.asarray(projection['metadata']['compact_weak_TT_original_component_ratios']));projection_admitted=bool(np.all(pr<=ROW_TOL));assert projection_admitted==projection['metadata']['compact_weak_TT_original_rows_admitted'] and projection['metadata']['physical_exterior_adopted'] is False
  else:assert not admitted
  assert projection_admitted==r['compact_weak_TT_original_rows_admitted'];roles=[inp,earned,association,sol]+([projection] if projection is not None else []);snapshots=[q for q in records if q not in roles];assert len(snapshots)<=4 and all(q['metadata']['kind']=='unqualified_fine_PCG_paired_iterate' and q['metadata']['iteration'] in (64,128,256,512) and q['metadata']['recursive_residual_is_not_admission'] is True for q in snapshots)
  expected='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if admitted else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED');assert r['status']==expected
  report=dict(status='SAVED_CACHED_FINE_PCG_YORK_CLOSURE_PASS',producer_status=r['status'],controls=4,committed_pairs=len(records),immutable_parent_INPUT_fields=478,copied_earned_fixture_fields=178,copied_failed_RAW_fields=59,all_immutable_parent_fields_bitcopied=True,original_component_ratios=stored.tolist(),original_global_ratios=global_ratios.tolist(),original_rows_admitted=admitted,compact_weak_TT_original_rows_admitted=projection_admitted,iterations=iteration,snapshots=len(snapshots),actual_node_update_earned=has_update,stored_last_update_contact_error=contact_error,independent_previous_residual_update_recontraction=has_update)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_identity_tolerance=TOL,original_row_tolerance=ROW_TOL,L_point_energy_Gram_triangle_preconditioner_operator_PCG_FE_or_fixture_replayed=False,physical_adoption=False,scope_limit='Stored words, exact insertion sums, bitcopies, triplets and norms only. Before-update original/recursive residuals independently reconstruct published update and drift contacts. Energy/adjoint controls are authenticated saved triplets, not recontracted. Optional projection uses only stored weak ratios/flags. Original finite primitive mismatch, physical normal/CMC/exterior/evolution and galaxy readout remain unqualified.')
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(receipt)==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v007.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
