"""Held warm York correction with the same earned two-level factor; no assembly."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V005'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='c57d6307466b2e04675e7bbe19783b4db734d9a505b6f45ccf98f5194f464924'
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V004'
PARENT_SOURCE='cross_u_compact_york_longitudinal_projection_v004.py'
PARENT_SOURCE_SHA='738d9b72949ab43380a66206ff35779774a916f404867558116ecb7263603f57'
PARENT_PROTOCOL_SHA='be86443151be254fd794e0e12948d17dde0d2af29ead2ff31739ab7bb488abbc'
TERMINAL=dict(pid=70321,result_sha256='1346fba37e498bf6caeda3412d502611a573ff5bd792c174848dabc4700a1111',receipt_sha256='2dc6266a4aecfe3f7890edb18437deb54065707cb32fdd24565f4efc284e146c')
PROOF='READONLY_TWOLEVEL_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
PROOF_SHA='02562b78ed315384d90cabad973e7e862b40c452e6968832ba43b5ee15ff97c0'
KERNEL='author_fragment_coupled_york_twolevel_preconditioner_v004.py'
KERNEL_SHA='4c9c61fc68dae085fd9a4309f749809a1415efb67e4562dee57b98fac832201e'
CAP=160
C=Q=P=np=None

def keep(n,a):return Q.keep(n,np.asarray(a).copy())
def arrays():
 out={**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})};return {n:np.asarray(a).copy() for n,a in out.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def initialize():
 global C,Q,P,np
 assert hashlib.sha256((BASE/PARENT_SOURCE).read_bytes()).hexdigest()==PARENT_SOURCE_SHA
 spec=importlib.util.spec_from_file_location('earned_coupled_twolevel_definitions_only',BASE/PARENT_SOURCE);C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C);C.initialize()
 Q,P,np=C.Q,C.P,C.np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((PARENT_SOURCE,PARENT_SOURCE_SHA),(PARENT+'.md',PARENT_PROTOCOL_SHA),(KERNEL,KERNEL_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):Q.bind(n,h)

def warm_admission():
 for n,h in ((PARENT+'_RESULT.json',TERMINAL['result_sha256']),(PARENT+'_RECEIPT.json',TERMINAL['receipt_sha256']),(PROOF,PROOF_SHA)):Q.bind(n,h)
 r=json.loads(P.path(PARENT+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT+'_RECEIPT.json').read_text());proof=json.loads(P.path(PROOF).read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==TERMINAL['result_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==PARENT_SOURCE_SHA
 assert r['status']=='ORIGINAL_YORK_ROWS_NOT_ADMITTED' and r['original_rows_admitted'] is False and r['compact_weak_TT_original_rows_admitted'] is False and r['projection'] is None and r['vector_space_dimension']==11135 and r['coarse_dimension']==2730 and r['extended_dimension']==13865
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
 assert r['all_full_coupled_map_entries_retained'] is True and r['cap']==160 and r['max_new_cycles']==1 and len(r['controls'])==2 and len(r['checkpoints'])==8 and all(c['passed'] and c['tolerance']==2e-11 for c in r['controls'])
 assert proof['status']=='SAVED_TWOLEVEL_YORK_CLOSURE_PASS' and proof['parent']==dict(TERMINAL,error_sha256=None) and proof['controls']==2 and proof['committed_pairs']==8 and proof['producer_status']==r['status'] and proof['original_rows_admitted'] is False and proof['compact_weak_TT_original_rows_admitted'] is False
 assert proof['all_immutable_parent_INPUT_fields_bitcopied'] is True and proof['coarse_payload_byte_and_schema_authenticated_only'] is True and proof['L_action_Gram_factorization_triangular_MINRES_projection_FE_or_fixture_replayed'] is False and proof['physical_adoption'] is False and proof['original_row_tolerance']==1e-10 and proof['arithmetic_identity_tolerance']==2e-11
 for q in (r['input'],r['coarse'],r['solution']):
  assert q in r['checkpoints'] and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;Q.bind(n,h)
  assert json.loads(P.path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')}
 assert r['input']['metadata']['kind']=='exact_refused_coupled_York_final_seed_and_frozen_operator' and len(r['input']['metadata']['schema'])==253
 cm=r['coarse']['metadata'];sm=r['solution']['metadata']
 assert cm['kind']=='new_coupled_coarse_basis_Gram_and_strict_factor' and cm['input_ref']==thin(r['input']) and cm['positive_Cholesky_required'] is True and cm['jitter_added'] is False and cm['full_map_cross_terms_retained'] is True and cm['coarse_global_coercivity_claimed'] is False
 assert sm['kind']=='one_bounded_coupled_twolevel_York_original_row_result' and sm['input_ref']==thin(r['input']) and sm['coarse']==thin(r['coarse']) and sm['original_rows_admitted'] is False and sm['cap']==160 and sm['max_new_cycles']==1
 return r,proof

def load_warm(r):
 # Read new seed/factor first. Restore EVERY old INPUT alias last, unchanged.
 s=P.read_pair(r['solution'],tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale'))
 for n,v in s.items():keep('continued_final_solution_'+n,v)
 cn=('fine_to_coarse_i','fine_to_coarse_j','physical_node_interpolation_weights','coarse_hat_values_at_fine_cell_corners','coarse_global_local_indices','coarse_mask','coarse_positive_scale','normalized_coarse_Cholesky')
 coarse=P.read_pair(r['coarse'],tuple('new_coarse_'+n for n in cn))
 for n,v in coarse.items():keep('continued_coarse_'+n,v)
 a=P.read_pair(r['input'],tuple(r['input']['metadata']['schema']))
 for n,v in a.items():keep(n,v)
 mask=a['compact_vector_mask'];assert mask.shape==(3,87,45) and mask.dtype==np.dtype('bool') and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
 assert not np.any(mask[:,0,:]) and not np.any(mask[:,-1,:]) and not np.any(mask[:,:,-1]) and not np.any(mask[1,:,0]) and np.all(a['diagonal_positivity_margin'][mask]>0)
 d=dict(maps=(a['L_maps_hi'],a['L_maps_lo']),map_envelope=a['L_map_operation_envelope'],ih=a['ih'],sqrt_h=a['sqrt_h'],PiTF=(a['PiTF_hi'],a['PiTF_lo']),geometry={n:a[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')},rhs=(a['rhs_hi'][mask],a['rhs_lo'][mask]),rhs_envelope=a['rhs_operation_envelope'][mask],scale=a['positive_Jacobi_congruence_scale'][mask],sufficient_component_targets=a['original_component_sufficient_white_targets'])
 assert d['sufficient_component_targets'].shape==(3,) and np.all(d['sufficient_component_targets']>0) and np.all(d['scale']>0)
 nodes=(s['final_potential_nodes_hi'],s['final_potential_nodes_lo']);action=(s['final_original_action_hi'],s['final_original_action_lo']);residual=(s['final_original_residual_hi'],s['final_original_residual_lo'])
 assert nodes[0].shape==nodes[1].shape==(11135,) and np.array_equal(s['original_positive_scale'],d['scale']) and all(np.array_equal(s['original_rhs_'+w],d['rhs'][i]) for i,w in enumerate(('hi','lo')))
 assert np.array_equal(s['final_original_raw_scaled_ratios'],np.asarray(r['solution']['metadata']['original_component_ratios'])) and not np.all(s['final_original_raw_scaled_ratios']<=1e-10)
 current=dict(action=action,residual=residual,ratios=s['final_original_raw_scaled_ratios'],global_ratios=s['final_original_global_ratios'],admitted=False)
 plan=dict(ci=coarse['new_coarse_fine_to_coarse_i'],cj=coarse['new_coarse_fine_to_coarse_j'],node_weights=coarse['new_coarse_physical_node_interpolation_weights'],corner_coefficients=coarse['new_coarse_coarse_hat_values_at_fine_cell_corners'],indices=coarse['new_coarse_coarse_global_local_indices'],mask=coarse['new_coarse_coarse_mask'])
 scale=coarse['new_coarse_coarse_positive_scale'];factor=coarse['new_coarse_normalized_coarse_Cholesky']
 assert plan['ci'].dtype==plan['cj'].dtype==plan['indices'].dtype==np.dtype('int64') and plan['ci'].shape==(87,) and plan['cj'].shape==(45,) and plan['indices'].shape==(3784,12)
 assert plan['node_weights'].shape==(4,87,45) and plan['corner_coefficients'].shape==(4,4,3784) and np.array_equal(plan['mask'],C.york_coarse_mask())
 assert scale.shape==(2730,) and factor.shape==(2730,2730) and np.all(scale>0) and np.all(np.diag(factor)>0) and np.all(np.triu(factor,1)==0)
 pre=dict(plan=plan,coarse_scale=scale,coarse_factor=factor,fine_scale=d['scale'],prolong=lambda x:C.york_coarse_prolong(x,plan),adjoint=lambda x:C.york_coarse_adjoint(x,plan),coarse_Gram_is_new_approximate_preconditioner=False,earned_coarse_factor_reused=True,full_coupled_features_retained=True,global_coercivity_claimed=False,jitter_added=False)
 inp=P.checkpoint('INPUT',arrays(),dict(kind='unchanged_V004_INPUT_and_latest_paired_seed_and_earned_coarse_factor',parent_input=thin(r['input']),parent_solution=thin(r['solution']),earned_coarse_ref=thin(r['coarse']),preserved_parent_controls=r['controls'],preserved_parent_checkpoints=r['checkpoints'],all_parent_input_fields_bitcopied=True,latest_solution_prefix='continued_final_solution_',selected_coarse_prefix='continued_coarse_',latest_SOLUTION_and_COARSE_loaded_before_INPUT_to_preserve_aliases=True,final_paired_seed_bitcopied=True,old_original_rows_admitted=False,coarse_Gram_factor_fixture_geometry_or_old_iterations_replayed=False,new_control_ordinals_are_separate=True,cap=CAP,original_row_tolerance=1e-10))
 d['input_ref']=inp;P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();return nodes,current,d,pre,inp

def warm_packet(parent,proof):
 nodes,current,d,pre,inp=load_warm(parent);P.CONTEXT.update(stage='continued_coupled_twolevel_warm_correction',cap=CAP)
 nodes,current,solver=C.york_twolevel_warm_correction(nodes,current,d,pre,'continued_twolevel_york',CAP)
 Q.york_pair_keep('final_potential_nodes',nodes,keep);Q.york_pair_keep('original_rhs',d['rhs'],keep);Q.york_pair_keep('final_original_action',current['action'],keep);Q.york_pair_keep('final_original_residual',current['residual'],keep);keep('final_original_raw_scaled_ratios',current['ratios']);keep('final_original_global_ratios',current['global_ratios']);keep('original_positive_scale',d['scale']);assert len(P.CHECKS)==1
 solution=P.checkpoint('SOLUTION',arrays(),dict(kind='one_warm_correction_with_earned_coupled_twolevel_factor',input_ref=thin(inp),earned_coarse_ref=thin(parent['coarse']),solver=solver,original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),original_global_ratios=current['global_ratios'].tolist(),controls=P.CHECKS,cap=CAP,max_new_cycles=1,physical_TT_prepared=False,potential_error_bound_claimed=False))
 projection=None;projection_admitted=False
 if current['admitted']:
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();scope=Q.york_point_projection(nodes,current,d);projection_admitted=scope['compact_weak_TT_original_rows_admitted'];projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(solution),input_ref=thin(inp),original_raw_scaled_ratios=current['ratios'].tolist(),**scope))
 status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if current['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED')
 return dict(status=status,input=inp,solution=solution,projection=projection,earned_coarse_ref=thin(parent['coarse']),checkpoints=P.RECORDS,controls=P.CHECKS,preserved_parent_controls=parent['controls'],preserved_parent_checkpoints=parent['checkpoints'],parent_terminal=TERMINAL,parent_original_rows_admitted=False,original_rows_admitted=current['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,coarse_dimension=2730,extended_dimension=13865,max_new_cycles=1,cap=CAP,coarse_Gram_or_fixture_replayed=False,all_full_coupled_map_entries_retained=True,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Held root and distinct review required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_warm_York_correction_same_earned_coarse_factor');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  parent,proof=warm_admission();case=warm_packet(parent,proof);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  current=arrays()
  if current:P.checkpoint('ERROR_RAW',current,dict(kind='available_NEW_warm_York_earned_factor_correction_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
