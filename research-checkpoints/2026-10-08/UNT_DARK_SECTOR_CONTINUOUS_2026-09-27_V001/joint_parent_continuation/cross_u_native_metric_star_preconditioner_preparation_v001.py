"""Held preparation only: older native STAR + NEW common-basis metric blocks."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NATIVE_METRIC_STAR_PRECONDITIONER_PREPARATION_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='0f92da042f3e878cd06fba6e8c2ba1ca809efa430dfaac2e028d2048615bd004'
PROVIDER='cross_u_initial_york_trace_target_rate_response_v001.py'
PROVIDER_SHA='23cbba6893b934236c8fff2c8ff4dda63f6808f589a04f701dcd536fdd31de27'
KERNEL='author_fragment_native_metric_star_preconditioner_v004.py'
KERNEL_SHA='076261aa0d8666182890418b7808f5149a3e59f77c0ceff4876875265700125a'
ADMISSION='author_fragment_native_star_preparation_admission_v001.py'
ADMISSION_SHA='267b058db47c26149c04ab8bc478778b0b428a5d9f61c4b64be76027b486997d'
P=T=np=None

def bind(n,h):
 p=Path(n);p=p if p.is_absolute() else BASE/p;assert h is not None and P.sha(p)==h,n
 key=str(p.resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h;return p

def keep(n,x):return ORIGINAL_CAPTURE(n,np.asarray(x).copy())
def arrays():
 out={**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})};return {n:np.asarray(x).copy() for n,x in out.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def reset(stage):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage)

def initialize():
 global P,T,np,ORIGINAL_CAPTURE
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('closed_trace_response_definitions_only_for_star',BASE/PROVIDER);T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T);T.initialize()
 P,np=T.P,T.np;ORIGINAL_CAPTURE=T.ORIGINAL_CAPTURE;P.capture=keep;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(literal_primitive_stationarity_prepared=False,finite_configuration_prepared=False,normal_constraints_qualified=False,initial_CMC_qualified=False,TT_free_data_admitted=False,physical_exterior_adopted=False,evolution_qualified=False,galaxy_velocity_qualified=False,physical_adoption=False)
 assert not P.RECORDS and not P.CHECKS and not P.OUTPUTS
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__)),('author_fragment_native_metric_star_preconditioner_v003.py','60b81485398aff4f4b6a37e3c0bacffab923e8911faf42bf155b87eba4598217')):bind(n,h)
 for n in (KERNEL,ADMISSION):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())
 assert NATIVE_METRIC_STAR_AUTHOR_DRAFT is True and NATIVE_METRIC_STAR_AUTHORING_IN_PROGRESS is False

def preparation_admission():
 star=native_star_preparation_admission();old='CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001'
 rh='6041c495ea6d837840d6f4bde687ba3dcf604131087c2ed7b395ae67fe284bb6';ch='1aee74e2996755c644e242e78ecb488f2bc334dc63aa6568a5d3309f4c8235a3'
 pn='READONLY_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_V001_RESULT.json';ph='eb9c8fbe3736069d72b1be992e4637b33ff7b53408157a7f60ca510e7dcc4153'
 for n,h in ((old+'_RESULT.json',rh),(old+'_RECEIPT.json',ch),(old+'.md','793cc56c47dabc8a7baa7838b57fd95b658d655242a71e112d0d64b932ba44f7'),(pn,ph)):bind(n,h)
 r=json.loads(P.path(old+'_RESULT.json').read_text());rc=json.loads(P.path(old+'_RECEIPT.json').read_text());proof=json.loads(P.path(pn).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==rh and rc['error_sha256'] is None and r['owner']==rc['owner'] and r['owner']['pid']==71394 and r['owner']['source_sha256']==PROVIDER_SHA
 assert r['status']=='NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED' and r['literal_original_response_admitted'] is False and r['original_primitive_stationarity_mismatch_resolved'] is False and r['zero_native_RHS_relative_ratio'] is None
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and len(r['checkpoints'])==13 and len(r['controls'])==3 and all(c['passed'] for c in r['controls'])
 assert proof['status']=='SAVED_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_PASS' and proof['parent']==dict(pid=71394,result_sha256=rh,receipt_sha256=ch,error_sha256=None) and proof['committed_pairs']==13 and proof['controls']==3 and proof['original_row_tolerance']==1e-10 and proof['physical_adoption'] is False and proof['literal_original_response_admitted'] is False
 q=r['input'];assert q==r['checkpoints'][0] and q['file']==old+'_00000_INPUT.npz' and q['sha256']=='d8b25d5b138e837a6913927ff5a7b659ec3913799d8d0557c60cf686ab68888d' and q['commit_sha256']=='fd6c7fa271f572cfd13b773e6d7e22d02fcd1cbc50851fd8f4ef42d85702367f'
 for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
 a=json.loads(P.path(q['commit_file']).read_text());assert a=={n:q[n] for n in ('file','sha256','metadata')} and a['metadata']['owner']==r['owner'] and a['metadata']['qualification']==r['qualification'] and a['metadata']['failed'] is False
 md=q['metadata'];assert md['kind']=='NEW_compact_total_trace_target_RHS_and_immutable_numerical_preconditioner' and md['native_conservative_reference_choice_fixed_before_solve'] is True and md['primitive_canonical_readout_admitted'] is False and md['NEW_native_target_exactly_zero'] is True and md['NEW_metric_target_nonzero'] is True and md['zero_source_relative_ratio'] is None
 assert thin(md['frozen_system_refs']['basis'])==thin(star['basis_source']['current_basis_metadata']) and len(md['schema'])==38
 for n,shape in (('frozen_metric_B',(15136,99,6)),('frozen_metric_T',(15136,6,6)),('frozen_metric_eB',(15136,99,6)),('frozen_metric_eT',(15136,6,6)),('original_basis_R',(4,3784)),('original_basis_dv',(4,3784)),('original_basis_hats',(4,4,3,86,44)),('original_basis_native_scale',(33,3,87,45)),('original_basis_metric_scale',(6,87,45)),('NEW_t_target_RHS_hi',(403340,)),('NEW_t_target_RHS_lo',(403340,))):assert md['schema'][n]==dict(shape=list(shape),dtype='float64',finite=True),n
 for n in ('original_basis_cell_i','original_basis_cell_j'):assert md['schema'][n]==dict(shape=[3784],dtype='int64',finite=True)
 return dict(star=star,input=q,parent_terminal=dict(pid=71394,source_sha256=PROVIDER_SHA,protocol_sha256='793cc56c47dabc8a7baa7838b57fd95b658d655242a71e112d0d64b932ba44f7',result_sha256=rh,receipt_sha256=ch,error_sha256=None),parent_proof=dict(file=pn,sha256=ph),primitive_readout_admitted=False,physical_adoption=False)

def preparation_packet(refs):
 reset('copy_closed_INPUT38_and_older_native_STAR_only');old=P.read_pair(refs['input'],tuple(refs['input']['metadata']['schema']))
 for n,x in old.items():keep(n,x.copy())
 prepnames=('preconditioner_D','preconditioner_B','preconditioner_Maxwell','preconditioner_basis_scale','kinetic_congruence_scale');saved=P.read_pair(refs['star']['preparation'],prepnames)
 cached=copy_saved_native_star(saved,'older_native_STAR');assert np.array_equal(cached['inherited_normscale'],old['original_basis_native_scale'])
 g={n:old['original_basis_'+n] for n in ('R','dv','hats','r','z','cell_i','cell_j')}
 inp=P.checkpoint('INPUT',arrays(),dict(kind='unchanged_closed_trace_target_INPUT_and_older_lumped_STAR',parent_input=thin(refs['input']),all38_original_INPUT_fields_bitcopied=True,older_native_preparation=thin(refs['star']['preparation']),older_native_terminal=refs['star']['terminal'],older_native_proof=refs['star']['proof'],basis_source=refs['star']['basis_source'],parent_terminal=refs['parent_terminal'],parent_proof=refs['parent_proof'],original_reference_metadata=refs['input']['metadata'],same_native_scale_bitwise=True,original_primitive_stationarity_mismatch_resolved=False,old_native_preparation_replayed=False))
 reset('NEW_correlated_and_inactive_coordinate_controls');fresh=fresh_correlated_native_metric_star_control();inactive=fresh_native_star_inactive_coordinate_control();assert len(P.CHECKS)==10
 fixture=P.checkpoint('FIXTURE',arrays(),dict(kind='NEW_two_independent_correlated_STAR_controls',correlated=fresh,inactive=inactive,controls=P.CHECKS.copy(),old_fixture_replayed=False))
 reset('NEW_common_basis_metric_cross_and_signed_T_self_node_blocks')
 new=assemble_new_metric_star_couplings(old['frozen_metric_B'],old['frozen_metric_T'],old['frozen_metric_eB'],old['frozen_metric_eT'],g,cached,'NEW_metric_star')
 for n,x in new.items():
  if isinstance(x,np.ndarray):keep('NEW_metric_star_result_'+n,x.copy())
 assembly=P.checkpoint('COMMON_BASIS',arrays(),dict(kind='NEW_common_basis_numerical_metric_couplings_only',input_ref=thin(inp),native_STAR_reused=True,all32_modes_retained=True,physical_six_density_offdiagonal_convention_unchanged=True,axis_identification_inside_hat_products=True,Fhat_rounding_bridge_retained=True,native_basis_scale_pullback='physical native cross divided by saved positive basis_scale',point_and_node_T_nonsymmetry_retained=True,exact_fine_diagonal_or_global_Schur_claimed=False,frozen_or_literal_operator_replayed=False,fine_action_or_RHS_changed=False))
 reset('NEW_resolved_signed_local_STAR_absolute_congruence_factors');pre=factor_native_metric_star(cached,new,'NEW_star_factor')
 for n,x in pre.items():
  if isinstance(x,np.ndarray):keep('NEW_star_preconditioner_'+n,x.copy())
 assert len(P.CHECKS)==14
 factor=P.checkpoint('FACTOR',arrays(),dict(kind='NEW_resolved_correlated_native_metric_numerical_congruence',input_ref=thin(inp),assembly_ref=thin(assembly),factor_control_count=4,controls=P.CHECKS[-4:],native_STAR_older_lumped_surrogate=True,all_C_and_signed_S_retained=True,coordinate_preserving_auxiliary_factor=True,inactive_identity_fillers_removed_by_original_masks=True,strict_resolved_spectra=True,jitter_clipping_or_drop=False,whole_preconditioner_only=True,global_inverse_or_coercivity_claimed=False,numerical_recurrence_not_selected=True,physical_adoption=False))
 assert len(P.RECORDS)==4
 return dict(status='NEW_NATIVE_METRIC_STAR_NUMERICAL_PRECONDITIONER_PREPARATION_PASS',input=inp,fixture=fixture,assembly=assembly,factor=factor,parent_terminal=refs['parent_terminal'],parent_proof=refs['parent_proof'],new_arithmetic_controls=14,committed_pairs=4,original_primitive_stationarity_mismatch_resolved=False,original_frozen_and_literal_gates_changed=False,fine_action_or_RHS_changed=False,new_response_computed=False,global_inverse_or_coercivity_claimed=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and '--root-run' in sys.argv,'Held full review and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();refs=preparation_admission();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_NEW_native_metric_STAR_numerical_preparation_only');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  case=preparation_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='NEW_native_metric_STAR_partial_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
