"""Held NEW64 fine-PCG steps from the exact completed512 recurrence; no restart."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V008'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='42be809061ac846fa3e0072cf6f1e464e38d3f31715026d6a8843408ce78ab93'
PROVIDER='cross_u_compact_york_longitudinal_projection_v007.py'
PROVIDER_SHA='25a96063c97b691440401a2b32f6b1b93919f3211d9d5f3747fd67d0a93d038b'
FRAGMENTS={'author_fragment_fine_paired_york_pcg_v004.py': 'adb02a4af198e38030865abe9aaba5757a4942038dee2640d847448338deecd8', 'author_fragment_fine_pcg_split_continuation_control_v001.py': 'ca2e7c7b6e1ef6860d498dca059967f8bfe1e4946ee9422eb5de902e2a77c373', 'author_fragment_fine_pcg_64_continuation_admission_v001.py': '42837b18d6d0b28562829da3256525cc325ad13bbab5b5c3ab2a3e2c355862be'}
CAP=64
D=C=Q=P=np=None

def keep(n,a):return Q.keep(n,np.asarray(a).copy())
def arrays():return {n:np.asarray(a).copy() for n,a in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def bind(n,h):return Q.bind(n,h)
def reset(stage):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage)
def initialize():
 global D,C,Q,P,np
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('completed_fine_PCG_definitions_only',BASE/PROVIDER);D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D);D.initialize()
 C,Q,P,np=D.C,D.Q,D.P,D.np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((PROVIDER,PROVIDER_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__)),*FRAGMENTS.items()):bind(n,h)
 for n in FRAGMENTS:exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def load_continuation(refs):
 reset('copy_completed512_system_and_exact_recurrence_state')
 coarse=('fine_to_coarse_i','fine_to_coarse_j','physical_node_interpolation_weights','coarse_hat_values_at_fine_cell_corners','coarse_global_local_indices','coarse_mask','coarse_positive_scale','normalized_coarse_Cholesky')
 names=('L_maps_hi','L_maps_lo','L_map_operation_envelope','ih','sqrt_h','PiTF_hi','PiTF_lo','R','dv','hats','r','z','cell_i','cell_j','rhs_hi','rhs_lo','rhs_operation_envelope','positive_Jacobi_congruence_scale','compact_vector_mask')+tuple('continued_coarse_new_coarse_'+n for n in coarse)
 old=P.read_pair(refs['input'],names)
 bases=('final_potential_nodes','final_original_action','final_original_residual','original_rhs','fine_york_PCG_current_nodes','fine_york_PCG_recursive_residual','fine_york_PCG_new_recursive_residual','fine_york_PCG_preconditioned_residual','fine_york_PCG_search_direction','fine_york_PCG_previous_search_direction','fine_york_PCG_previous_Ap','fine_york_PCG_Ap','fine_york_PCG_fresh_original_residual','fine_york_PCG_rz','fine_york_PCG_current_rz_paired_inner_product')
 scalars=('fine_york_PCG_current_rz_inner_binary64_readout','fine_york_PCG_beta','fine_york_PCG_iterations_completed','fine_york_PCG_direction_action_positive_positive_scatter','fine_york_PCG_fresh_original_original_residual_operation_envelope','final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale')
 saved=P.read_pair(refs['solution'],tuple(n+'_'+w for n in bases for w in ('hi','lo'))+scalars)
 data={}
 for prefix,a in (('continued_V007_INPUT_',old),('continued_V007_SOLUTION_',saved)):
  for n,x in a.items():data[prefix+n]=np.asarray(x).copy();keep(prefix+n,x)
 mask=old['compact_vector_mask'];assert mask.shape==(3,87,45) and mask.dtype==np.dtype('bool') and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
 d=dict(maps=(old['L_maps_hi'],old['L_maps_lo']),map_envelope=old['L_map_operation_envelope'],ih=old['ih'],sqrt_h=old['sqrt_h'],PiTF=(old['PiTF_hi'],old['PiTF_lo']),geometry={n:old[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')},rhs=(old['rhs_hi'][mask],old['rhs_lo'][mask]),rhs_envelope=old['rhs_operation_envelope'][mask],scale=old['positive_Jacobi_congruence_scale'][mask])
 pair=lambda n:(saved[n+'_hi'],saved[n+'_lo']);nodes=pair('final_potential_nodes');scores=saved['final_original_raw_scaled_ratios'];assert int(saved['fine_york_PCG_iterations_completed'])==512 and scores.shape==(3,2) and scores[0,0]>1e-10 and np.count_nonzero(scores>1e-10)==1
 for w in (0,1):
  assert np.array_equal(nodes[w],pair('fine_york_PCG_current_nodes')[w]) and np.array_equal(pair('final_original_residual')[w],pair('fine_york_PCG_fresh_original_residual')[w]) and np.array_equal(pair('fine_york_PCG_recursive_residual')[w],pair('fine_york_PCG_new_recursive_residual')[w])
  assert np.array_equal(pair('fine_york_PCG_previous_Ap')[w],pair('fine_york_PCG_Ap')[w]) and np.array_equal(pair('fine_york_PCG_rz')[w],pair('fine_york_PCG_current_rz_paired_inner_product')[w]) and np.array_equal(pair('original_rhs')[w],d['rhs'][w])
 assert np.array_equal(saved['original_positive_scale'],d['scale'])
 current=dict(action=pair('final_original_action'),residual=pair('final_original_residual'),ratios=scores,global_ratios=saved['final_original_global_ratios'],admitted=False,residual_envelope=saved['fine_york_PCG_fresh_original_original_residual_operation_envelope'])
 state=dict(recursive_residual=pair('fine_york_PCG_recursive_residual'),z=pair('fine_york_PCG_preconditioned_residual'),rz=pair('fine_york_PCG_rz'),rho=float(saved['fine_york_PCG_current_rz_inner_binary64_readout']),direction=pair('fine_york_PCG_search_direction'),previous_direction=pair('fine_york_PCG_previous_search_direction'),previous_result=dict(action=pair('fine_york_PCG_previous_Ap'),envelope=saved['fine_york_PCG_direction_action_positive_positive_scatter'][mask]))
 assert state['rho']>0 and state['rho']==float(state['rz'][0]+state['rz'][1]) and np.all(state['previous_result']['envelope']>=0) and np.all(current['residual_envelope']>=0)
 c=lambda n:old['continued_coarse_new_coarse_'+n]
 plan=dict(ci=c('fine_to_coarse_i'),cj=c('fine_to_coarse_j'),node_weights=c('physical_node_interpolation_weights'),corner_coefficients=c('coarse_hat_values_at_fine_cell_corners'),indices=c('coarse_global_local_indices'),mask=c('coarse_mask'))
 pre=dict(plan=plan,coarse_scale=c('coarse_positive_scale'),coarse_factor=c('normalized_coarse_Cholesky'),fine_scale=d['scale'],prolong=lambda x:C.york_coarse_prolong(x,plan),adjoint=lambda x:C.york_coarse_adjoint(x,plan))
 inp=P.checkpoint('INPUT',data,dict(kind='selected_completed512_fine_system_and_exact_next_recurrence_state',parent_terminal=refs['terminal'],parent_proof=refs['proof'],parent_input=thin(refs['input']),parent_solution=thin(refs['solution']),preserved_parent_controls=refs['original_controls'],preserved_parent_checkpoints=refs['original_checkpoints'],prior_solver=refs['prior_solver'],selected_input_fields=len(old),selected_solution_fields=len(saved),prior_512_original_nonadmission_preserved=True,additional_cap=64,total_step_budget_upper=576,recursive_residual_replaced=False,automatic_restart=False,old_first_action_preconditioner_fixture_Gram_or_factor_replayed=False,physical_adoption=False))
 d['input_ref']=inp;return nodes,current,d,pre,state,inp

def continuation_packet(refs):
 nodes,current,d,pre,state,inp=load_continuation(refs)
 reset('NEW_small_explicit_split_recurrence_control');control=fresh_fine_pcg_split_continuation_control();assert len(P.CHECKS)==4
 fixture=P.checkpoint('FIXTURE',arrays(),dict(control,controls=P.CHECKS.copy()))
 reset('NEW_explicit64_continued_steps_after512')
 nodes,current,solver=fine_paired_pcg(nodes,current,lambda x,l:york_fine_pcg_action(x,d,l),lambda r,l:york_fine_pcg_precondition(r,pre,l),lambda x,l:york_fine_pcg_certificate(x,d,l),'continued_fine_york_PCG',64,(16,32,64),continuation=state)
 solver.update(parent_iterations=512,additional_cap=64,total_iterations=512+solver['iterations'],automatic_extension=False)
 for n,a in (('final_potential_nodes',nodes),('original_rhs',d['rhs']),('final_original_action',current['action']),('final_original_residual',current['residual'])):Q.york_pair_keep(n,a,keep)
 keep('final_original_raw_scaled_ratios',current['ratios']);keep('final_original_global_ratios',current['global_ratios']);keep('original_positive_scale',d['scale']);assert len(P.CHECKS)==5
 sol=P.checkpoint('SOLUTION',arrays(),dict(kind='explicit_NEW64_continuation_of_completed512_fine_PCG',input_ref=thin(inp),fresh_split_fixture=thin(fixture),solver=solver,original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),controls=P.CHECKS.copy(),same_original_six_gates=True,recursive_residual_replaced=False,automatic_extension=False,potential_error_bound_claimed=False,physical_TT_prepared=False))
 projection=None;projection_admitted=False
 if current['admitted']:
  reset('newly_admitted_compact_weak_projection_readout');scope=Q.york_point_projection(nodes,current,d);projection_admitted=scope['compact_weak_TT_original_rows_admitted'];projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(sol),input_ref=thin(inp),original_raw_scaled_ratios=current['ratios'].tolist(),**scope))
 status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if current['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED')
 return dict(status=status,input=inp,fixture=fixture,solution=sol,projection=projection,checkpoints=P.RECORDS,controls=P.CHECKS,parent_terminal=refs['terminal'],parent_proof=refs['proof'],preserved_parent_controls=refs['original_controls'],preserved_parent_checkpoints=refs['original_checkpoints'],prior_512_original_nonadmission_preserved=True,original_rows_admitted=current['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,coarse_dimension=2730,additional_cap=64,total_step_budget_upper=576,recursive_residual_replaced=False,automatic_restart=False,automatic_extension=False,all_full_coupled_map_entries_retained=True,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and CAP==64,'Root/distinct FULL review and explicit64 cap required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive output namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_explicit64_step_continuation_of_completed512_fine_PCG');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  refs=fine_pcg_64_continuation_admission();case=continuation_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='completed512_state_and_NEW_bounded64_continuation_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
