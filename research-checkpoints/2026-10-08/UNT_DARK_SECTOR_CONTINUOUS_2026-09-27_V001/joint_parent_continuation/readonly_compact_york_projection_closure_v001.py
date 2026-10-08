"""Guarded saved W words only; no York map/action/scatter/solver replay."""
from pathlib import Path
import hashlib,json,math,os
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V001'
OUT='READONLY_COMPACT_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
AUTHOR_DRAFT=False
SOURCE_SHA='4b31ee0a5b0be690447c66ea8fd65ee00c7da83091e58f1090209e79dbf4a71d'
PROTOCOL_SHA='5651cfdb3c6e9a47d1aa8f1a86e5c456bd0aed768012149868fff8ec413cee79'
TERMINAL={'pid': 64681, 'result_sha256': '5aa112f2f031fd5bc6ec2a58765ccac2926316eede516be3082dc94bfa7f2972', 'receipt_sha256': '387382c097ceef6d671adedea054738b2a8bbb7aaabd9f76213063777bf143bf', 'error_sha256': None}
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
 assert sha('cross_u_compact_york_longitudinal_projection_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 rc=load_json(STEM+'_RECEIPT.json',TERMINAL['receipt_sha256']);closed=rc['status']=='CLOSED';assert rc['status'] in ('CLOSED','CLOSED_ERROR')
 r=load_json(STEM+('_RESULT.json' if closed else '_ERROR.json'),TERMINAL['result_sha256'] if closed else TERMINAL['error_sha256'])
 assert rc.get('result_sha256')==TERMINAL['result_sha256'] and rc.get('error_sha256')==TERMINAL['error_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==SOURCE_SHA
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 for n,h in rc['input_sha256'].items():assert sha(n)==h,n
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 records=r['checkpoints'];controls=r['controls'];assert len({q['file'] for q in records})==len(records)
 assert {p.name for p in BASE.glob(STEM+'_*.npz')}=={q['file'] for q in records} and {p.name for p in BASE.glob(STEM+'_*.npz.COMMIT.json')}=={q['commit_file'] for q in records}
 for q in records:
  assert rc['output_sha256'][q['file']]==q['sha256'] and rc['output_sha256'][q['commit_file']]==q['commit_sha256'] and load_json(q['commit_file'],q['commit_sha256'])=={k:q[k] for k in ('file','sha256','metadata')}
  assert q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification']
  if closed:assert q['metadata']['failed'] is False and all(s['finite'] is True for s in q['metadata']['schema'].values())
 assert [c['ordinal'] for c in controls]==list(range(len(controls))) and len(controls)<=3 and all(c['tolerance']==TOL and math.isfinite(c['error']) and c['passed']==(c['error']<=TOL) for c in controls)
 import numpy as np
 selected=[];identities=[]
 def read(q,names):
  sc=q['metadata']['schema'];out={}
  with np.load(path(q['file']),allow_pickle=False) as f:
   assert set(f.files)==set(sc)|{'metadata_json'} and json.loads(str(f['metadata_json']))==q['metadata']
   for n in names:
    a=f[n].copy();assert list(a.shape)==sc[n]['shape'] and str(a.dtype)==sc[n]['dtype'] and bool(np.all(np.isfinite(a)))==sc[n]['finite'] and sc[n]['finite'],n;out[n]=a
  selected.append(dict(file=q['file'],fields=len(names)));return out
 def pair(a,n):return a[n+'_hi'],a[n+'_lo']
 def total(p):return p[0]+p[1]
 def close(label,actual,expected,envelope=None):
  assert actual.shape==expected.shape
  bound=abs(actual)+abs(expected) if envelope is None else envelope;assert bound.shape==actual.shape and np.all(bound>=0)
  error=float(np.max(abs(actual-expected)/np.maximum(bound,1e-30),initial=0));assert error<=TOL,(label,error);identities.append(dict(name=label,error=error))
 def identity(label,terms,envelope=None):
  parts=[sign*v for sign,p in terms for v in p];gap=np.add.reduce(parts);bound=np.add.reduce([abs(v) for v in parts]) if envelope is None else envelope
  close(label,gap,np.zeros_like(gap),bound)
 def ratios(res,rhs,scale):
  cuts=(0,3740,7395,11135);out=[]
  for i in range(3):
   sl=slice(cuts[i],cuts[i+1]);den=float(np.linalg.norm(rhs[sl]));wd=float(np.linalg.norm(rhs[sl]/scale[sl]));raw=float(np.linalg.norm(res[sl]));white=float(np.linalg.norm(res[sl]/scale[sl]));assert den>0 and wd>0;out.append((raw/den,white/wd))
  return np.asarray(out)
 def stored_ratios(label,a,res_name,rhs,scale,ratio_name,metadata_ratios):
  got=ratios(total(pair(a,res_name)),rhs,scale);stored=a[ratio_name];assert got.shape==stored.shape==(3,2) and np.allclose(got,stored,rtol=TOL,atol=1e-300) and np.array_equal(stored,np.asarray(metadata_ratios)),label
  return bool(np.all(stored<=ROW_TOL))
 def original(ref,names):
  for n,h in ((ref['file'],ref['sha256']),(ref['commit_file'],ref['commit_sha256'])):assert rc['input_sha256'].get(n,rc['input_sha256'].get(str(path(n).resolve())))==h and sha(n)==h,n
  q=load_json(ref['commit_file'],ref['commit_sha256']);assert q['file']==ref['file'] and q['sha256']==ref['sha256'];return read(dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256']),names)
 def role(kind):
  found=[q for q in records if q['metadata']['kind']==kind];assert len(found)==1,kind;return found[0]
 for c in controls:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);names=tuple(prefix+n for n in ('actual','expected','envelope'));found=[q for q in records if all(n in q['metadata']['schema'] for n in names)];assert found,(c['ordinal'],names)
  witnesses=[read(q,names) for q in found];a=witnesses[0];assert all(all(np.array_equal(a[n],b[n]) for n in names) for b in witnesses)
  x,y,e=(a[n] for n in names);assert np.all(e>=0);error=float(np.max(abs(x-y)/np.maximum(e,1e-30),initial=0));assert error==c['error'];identities.append(dict(name=c['name']+'_stored_triplet',error=error))
 if not closed:report=dict(status='SAVED_COMPACT_YORK_PROJECTION_FAILURE_PRESERVED',controls=controls,committed_pairs=len(records),context=r.get('context'))
 else:
  inp=role('exact_earned_york_maps_source_diagonal_and_prior_bridge');ini=role('new_zero_potential_original_York_certificate');sol=role('bounded_auxiliary_york_original_row_result')
  assert r['input']==inp and r['solution']==sol and r['vector_space_dimension']==11135 and len(r['cycles'])==len(controls)<=3 and all(c['passed'] for c in controls)
  assert all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
  assert inp['metadata']['max_cycles']==sol['metadata']['max_cycles']==3 and inp['metadata']['cap']==sol['metadata']['cap']==160 and inp['metadata']['original_row_tolerance']==ROW_TOL and inp['metadata']['old_fixtures_or_source_replayed'] is False and inp['metadata']['new_operator_coefficients_reconstructed'] is False and sol['metadata']['potential_error_bound_claimed'] is False
  mask=np.ones((3,87,45),bool);mask[:,0]=False;mask[:,-1]=False;mask[:,:,-1]=False;mask[1,:,0]=False;assert np.count_nonzero(mask)==11135
  names=('rhs_hi','rhs_lo','rhs_operation_envelope','positive_Jacobi_congruence_scale','compact_vector_mask','PiTF_hi','PiTF_lo');ia=read(inp,names);assert np.array_equal(ia['compact_vector_mask'],mask)
  old=original(inp['metadata']['source_refs']['loads'],names[:4]);assert all(np.array_equal(ia[n],old[n]) for n in names[:4])
  rhs=(ia['rhs_hi'][mask],ia['rhs_lo'][mask]);f=total(rhs);scale=ia['positive_Jacobi_congruence_scale'][mask];assert np.all(scale>0)
  initial_names=tuple(n+'_'+w for n in ('initial_original_rhs','initial_york_original_action','initial_york_original_residual') for w in ('hi','lo'))+('initial_original_positive_scale','initial_york_original_raw_scaled_ratios','original_rhs_norms','original_rhs_component_norms','sufficient_original_white_target')
  za=read(ini,initial_names);assert all(np.array_equal(pair(za,'initial_original_rhs')[w],rhs[w]) for w in (0,1)) and np.array_equal(za['initial_original_positive_scale'],scale)
  assert all(np.all(v==0) for v in pair(za,'initial_york_original_action'))
  identity('initial_original_rhs_action_residual',[(1,rhs),(-1,pair(za,'initial_york_original_action')),(-1,pair(za,'initial_york_original_residual'))])
  assert stored_ratios('initial',za,'initial_york_original_residual',f,scale,'initial_york_original_raw_scaled_ratios',r['initial_original_ratios'])==ini['metadata']['original_rows_admitted']
  cuts=(0,3740,7395,11135);norms=np.asarray([(np.linalg.norm(f[cuts[i]:cuts[i+1]]),np.linalg.norm(f[cuts[i]:cuts[i+1]]/scale[cuts[i]:cuts[i+1]])) for i in range(3)])
  assert np.allclose(norms,za['original_rhs_component_norms'],rtol=TOL,atol=1e-300)
  sufficient=ROW_TOL*min(min(norms[i,0]/float(np.max(scale[cuts[i]:cuts[i+1]])),norms[i,1]) for i in range(3));assert math.isclose(sufficient,float(za['sufficient_original_white_target']),rel_tol=TOL,abs_tol=1e-300)
  previous_nodes=(np.zeros(11135),np.zeros(11135));previous_action=pair(za,'initial_york_original_action');previous_residual=pair(za,'initial_york_original_residual');cycle_summaries=[]
  for cycle,q in enumerate(r['cycles'],1):
   assert q in records and q['metadata']['kind']=='new_auxiliary_york_original_row_correction' and q['metadata']['cycle']==cycle and q['metadata']['cap']==160 and q['metadata']['controls']==controls[cycle-1:cycle] and q['metadata']['physical_TT_prepared'] is False
   label='york_cycle_%03d'%cycle;up=label+'_final_update';n=lambda suffix:label+'_'+suffix
   bases=('before_nodes','before_action','before_residual','solver_rhs_readout_defect','updated_original_action','updated_original_residual','original_residual_update_identity')
   names=tuple(n(b)+'_'+w for b in bases for w in ('hi','lo'))+tuple(up+s for s in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes'))+(n('solver_rhs_binary64'),n('completed_correction'),n('updated_original_raw_scaled_ratios'),n('residual_update_operation_envelope'))
   names+=tuple(n(b)+'_'+w for b in ('correction_action_action_restricted','compression_action_action_restricted') for w in ('hi','lo'))
   a=read(q,names);s=lambda suffix:pair(a,n(suffix));nodes=pair(a,up+'_updated_nodes')
   for w in (0,1):assert np.array_equal(s('before_nodes')[w],previous_nodes[w]) and np.array_equal(s('before_action')[w],previous_action[w]) and np.array_equal(s('before_residual')[w],previous_residual[w]) and np.array_equal(pair(a,up+'_old_nodes')[w],previous_nodes[w])
   assert np.array_equal(a[n('completed_correction')],a[up+'_float_correction']) and np.array_equal(a[n('solver_rhs_binary64')],total(previous_residual))
   word_arrays=[a[up+s] for s in ('_old_nodes_hi','_old_nodes_lo','_float_correction','_updated_nodes_hi','_updated_nodes_lo','_exact_update_minus_two_word_nodes')];assert all(v.shape==(11135,) for v in word_arrays)
   assert all(math.fsum((v[0],v[1],v[2],-v[3],-v[4],-v[5]))==0 for v in zip(*word_arrays));identities.append(dict(name=n('exact_node_update_with_third_word'),error=0.))
   identity(n('solver_rhs_readout_defect'),[(1,previous_residual),(-1,(a[n('solver_rhs_binary64')],np.zeros(11135))),(-1,s('solver_rhs_readout_defect'))])
   identity(n('updated_original_rhs_action_residual'),[(1,rhs),(-1,s('updated_original_action')),(-1,s('updated_original_residual'))])
   adelta=tuple(v[mask] for v in s('correction_action_action_restricted'));aq=tuple(v[mask] for v in s('compression_action_action_restricted'));envelope=a[n('residual_update_operation_envelope')]
   identity(n('saved_residual_update_contact'),[(1,s('updated_original_residual')),(-1,previous_residual),(1,adelta),(-1,aq),(-1,s('original_residual_update_identity'))],envelope)
   c=controls[cycle-1];prefix='control_%03d_%s_'%(c['ordinal'],c['name']);triplet=read(q,tuple(prefix+v for v in ('actual','expected','envelope')))
   assert np.array_equal(triplet[prefix+'actual'],total(s('original_residual_update_identity'))) and np.all(triplet[prefix+'expected']==0) and np.array_equal(triplet[prefix+'envelope'],envelope)
   admitted=stored_ratios(label,a,n('updated_original_residual'),f,scale,n('updated_original_raw_scaled_ratios'),q['metadata']['original_ratios']);assert admitted==q['metadata']['original_rows_admitted']
   previous_nodes=nodes;previous_action=s('updated_original_action');previous_residual=s('updated_original_residual');cycle_summaries.append(dict(cycle=cycle,original_ratios=q['metadata']['original_ratios'],original_rows_admitted=admitted,solver_return_admitted=q['metadata']['solver_return_admitted']))
  names=tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('original_positive_scale','final_original_raw_scaled_ratios','final_original_global_ratios');sa=read(sol,names)
  for w in (0,1):assert np.array_equal(pair(sa,'final_potential_nodes')[w],previous_nodes[w]) and np.array_equal(pair(sa,'original_rhs')[w],rhs[w]) and np.array_equal(pair(sa,'final_original_action')[w],previous_action[w]) and np.array_equal(pair(sa,'final_original_residual')[w],previous_residual[w])
  assert np.array_equal(sa['original_positive_scale'],scale) and sol['metadata']['controls']==controls and sol['metadata']['cycles']==[{k:q[k] for k in ('file','sha256','commit_file','commit_sha256')} for q in r['cycles']]
  admitted=stored_ratios('final',sa,'final_original_residual',f,scale,'final_original_raw_scaled_ratios',sol['metadata']['original_ratios']);assert admitted==sol['metadata']['original_rows_admitted']==r['original_rows_admitted']
  global_ratios=np.asarray((np.linalg.norm(total(previous_residual))/np.linalg.norm(f),np.linalg.norm(total(previous_residual)/scale)/np.linalg.norm(f/scale)));assert np.allclose(global_ratios,sa['final_original_global_ratios'],rtol=TOL,atol=1e-300) and np.array_equal(sa['final_original_global_ratios'],np.asarray(sol['metadata']['original_global_ratios']))
  projection=r['projection'];projection_admitted=False;projection_diagnostics=None
  if admitted:
   assert projection in records and projection['metadata']['kind']=='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder' and projection['metadata']['solution']=={k:sol[k] for k in ('file','sha256','commit_file','commit_sha256')}
   names=tuple(n+'_'+w for n in ('auxiliary_potential_nodes','projected_longitudinal_tensor','projected_longitudinal_density','compact_weak_TT_remainder_density','point_density_decomposition_identity','compact_weak_TT_remainder','weak_TT_equals_original_residual_contact') for w in ('hi','lo'))+('compact_weak_TT_original_component_ratios',);pa=read(projection,names);p=lambda n:pair(pa,n)
   assert all(np.array_equal(p('auxiliary_potential_nodes')[w],previous_nodes[w]) for w in (0,1))
   identity('point_density_decomposition_saved_contact',[(1,p('compact_weak_TT_remainder_density')),(1,p('projected_longitudinal_density')),(-1,pair(ia,'PiTF')),(-1,p('point_density_decomposition_identity'))])
   identity('weak_TT_original_residual_saved_contact',[(1,p('compact_weak_TT_remainder')),(-1,previous_residual),(-1,p('weak_TT_equals_original_residual_contact'))])
   projection_admitted=stored_ratios('compact_weak_TT',pa,'compact_weak_TT_remainder',f,scale,'compact_weak_TT_original_component_ratios',projection['metadata']['compact_weak_TT_original_component_ratios']);assert projection_admitted==projection['metadata']['compact_weak_TT_original_rows_admitted']==r['compact_weak_TT_original_rows_admitted']
   assert all(projection['metadata'][n] is True for n in ('potential_unique_not_claimed','longitudinal_projection_original_rows_admitted','continuum_divergence_free_TT_not_claimed')) and projection['metadata']['physical_exterior_adopted'] is False
   projection_diagnostics={n:dict(L2=float(np.linalg.norm(total(p(n)))),Linf=float(np.max(abs(total(p(n))),initial=0))) for n in ('projected_longitudinal_tensor','compact_weak_TT_remainder_density','point_density_decomposition_identity','weak_TT_equals_original_residual_contact')}
  else:assert projection is None and r['compact_weak_TT_original_rows_admitted'] is False
  expected_status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if admitted else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED');assert r['status']==expected_status
  roles=[inp,ini,sol]+r['cycles']+([projection] if projection is not None else []);snapshots=[q for q in records if q not in roles];assert all(q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' and q['metadata']['iteration'] in (40,80,120,160) for q in snapshots) and len(snapshots)<=12
  report=dict(status='SAVED_COMPACT_YORK_PROJECTION_CLOSURE_PASS',producer_status=r['status'],controls=len(controls),committed_pairs=len(records),cycles=cycle_summaries,iteration_snapshots=len(snapshots),original_component_ratios=sa['final_original_raw_scaled_ratios'].tolist(),original_global_ratios=global_ratios.tolist(),original_rows_admitted=admitted,compact_weak_TT_original_rows_admitted=projection_admitted,sufficient_original_white_target=sufficient,original_rhs_component_norms=norms.tolist(),projection_diagnostics_descriptive=projection_diagnostics,original_primitive_bridge_resolved=False,auxiliary_boundary_is_physical_wall=False,continuum_TT_admitted=False)
 report.update(owner_pid=os.getpid(),parent=TERMINAL,selected=selected,identities=identities,arithmetic_identity_tolerance=TOL,original_row_tolerance=ROW_TOL,scope_limit='Saved words, triplets, norms and algebra contacts only; no independent L, raised density, York action, FE scatter, fixture or solve',York_geometry_action_scatter_solver_or_fixture_replayed=False,physical_adoption=False)
 for n,h in rc['input_sha256'].items():assert sha(n)==h,n
 for n,h in rc['output_sha256'].items():assert sha(n)==h,n
 assert sha(STEM+'_RECEIPT.json')==TERMINAL['receipt_sha256'] and sha('cross_u_compact_york_longitudinal_projection_v001.py')==SOURCE_SHA and sha(STEM+'.md')==PROTOCOL_SHA
 with path(OUT).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 path(OUT).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),sha256=sha(OUT))),flush=True)
if __name__=='__main__':main()
