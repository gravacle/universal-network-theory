"""Held one-pass coupled two-level numerical correction of original York rows."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V004'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='12b0275f4144d134a4300d98779a9d6c735671cd7760a82171a41233216b32e3'
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V003'
PARENT_SOURCE='cross_u_compact_york_longitudinal_projection_v003.py'
PARENT_SOURCE_SHA='4b32c89ca18e9816e16a3ab5fb1516dede0698f470cc510a2523369270a957e8'
PARENT_PROTOCOL_SHA='738471e1eaa0449bd1f09615c4622c203809cd0bfa87dcbce2d4930898d66b65'
TERMINAL=dict(pid=68504,result_sha256='3238ef464e0fde1b66de2a7e1135d57da1d9264e07cdea033cd2e58850059a4e',receipt_sha256='e49439ec7f6f225851b0777ce0b4f887215721c285530415c1a01a836152683c')
PROOF='READONLY_COUPLED_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
PROOF_SHA='ddebaf456ddc8a190f88032620607660e887d8e8050577d841926f4375070f5a'
FINE_DEFINITIONS='cross_u_compact_york_longitudinal_projection_v001.py'
FINE_DEFINITIONS_SHA='4b31ee0a5b0be690447c66ea8fd65ee00c7da83091e58f1090209e79dbf4a71d'
KERNEL='author_fragment_coupled_york_twolevel_preconditioner_v003.py'
KERNEL_SHA='66fd633d99d9372f73035cad51471164fdeb0ae56de8e3cd87edc9210b15f11d'
ANCESTORS=(('author_fragment_coupled_york_twolevel_preconditioner_v001.py','25caeb2bd5a60ac4bb5112ecae430e59f9aca5bd9c1c50ae91e5d105ebce114d'),('author_fragment_coupled_york_twolevel_preconditioner_v002.py','f72ac3b9b461a036966158354cbf898ea4d49f4471afa3748589bd6b568154ae'))
CAP=160
Q=None;P=None;np=None

def keep(n,a):return Q.keep(n,np.asarray(a).copy())
def arrays():
 out={**P.RAW,**P.AVAILABLE};out.update(P.DD_ARRAY_CURRENT.get('arrays',{}));return {n:np.asarray(a).copy() for n,a in out.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def initialize():
 global Q,P,np
 assert hashlib.sha256((BASE/FINE_DEFINITIONS).read_bytes()).hexdigest()==FINE_DEFINITIONS_SHA
 spec=importlib.util.spec_from_file_location('earned_york_definitions_for_new_coarse_basis',BASE/FINE_DEFINITIONS);Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q);Q.initialize()
 P=Q.P;np=Q.np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((FINE_DEFINITIONS,FINE_DEFINITIONS_SHA),(PARENT_SOURCE,PARENT_SOURCE_SHA),(PARENT+'.md',PARENT_PROTOCOL_SHA),(KERNEL,KERNEL_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__)))+ANCESTORS:Q.bind(n,h)
 exec(compile((BASE/KERNEL).read_text(),str(BASE/KERNEL),'exec'),globals())

def warm_admission():
 for n,h in ((PARENT+'_RESULT.json',TERMINAL['result_sha256']),(PARENT+'_RECEIPT.json',TERMINAL['receipt_sha256']),(PROOF,PROOF_SHA)):Q.bind(n,h)
 r=json.loads(P.path(PARENT+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT+'_RECEIPT.json').read_text());proof=json.loads(P.path(PROOF).read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==TERMINAL['result_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==PARENT_SOURCE_SHA
 assert r['status']=='ORIGINAL_YORK_ROWS_NOT_ADMITTED' and r['original_rows_admitted'] is False and r['compact_weak_TT_original_rows_admitted'] is False and r['projection'] is None and r['vector_space_dimension']==11135
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
 assert r['all_full_coupled_map_entries_retained'] is True and r['independent_block_claimed'] is False and 4<=len(r['controls'])<=6 and all(c['passed'] and c['tolerance']==2e-11 for c in r['controls'])
 assert proof['status']=='SAVED_COUPLED_YORK_CLOSURE_PASS' and proof['parent']==dict(TERMINAL,error_sha256=None) and proof['controls']==len(r['controls']) and proof['committed_pairs']==len(r['checkpoints']) and proof['producer_status']==r['status'] and proof['original_rows_admitted'] is False and proof['compact_weak_TT_original_rows_admitted'] is False
 assert proof['all_104_cache_fields_and_full_maps_bitcopied'] is True and proof['York_operator_solver_fixture_or_projection_replayed'] is False and proof['physical_adoption'] is False and proof['original_row_tolerance']==1e-10 and proof['arithmetic_identity_tolerance']==2e-11
 for q in (r['input'],r['solution']):
  assert q in r['checkpoints'] and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;Q.bind(n,h)
  assert json.loads(P.path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')}
 assert r['input']['metadata']['kind']=='exact_failed_support_cache_and_full_coupled_final_York_iterate' and r['solution']['metadata']['kind']=='full_coupled_principal_coordinate_warm_York_original_row_result' and r['solution']['metadata']['original_rows_admitted'] is False and r['solution']['metadata']['cap_per_group']==160
 return r,proof

def load_warm(r):
 a=P.read_pair(r['input'],tuple(r['input']['metadata']['schema']))
 for n,v in a.items():keep(n,v)
 mask=a['compact_vector_mask'];assert mask.shape==(3,87,45) and mask.dtype==np.dtype('bool') and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
 assert not np.any(mask[:,0,:]) and not np.any(mask[:,-1,:]) and not np.any(mask[:,:,-1]) and not np.any(mask[1,:,0]) and np.all(a['diagonal_positivity_margin'][mask]>0)
 d=dict(maps=(a['L_maps_hi'],a['L_maps_lo']),map_envelope=a['L_map_operation_envelope'],ih=a['ih'],sqrt_h=a['sqrt_h'],PiTF=(a['PiTF_hi'],a['PiTF_lo']),geometry={n:a[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')},rhs=(a['rhs_hi'][mask],a['rhs_lo'][mask]),rhs_envelope=a['rhs_operation_envelope'][mask],scale=a['positive_Jacobi_congruence_scale'][mask],sufficient_component_targets=a['original_component_sufficient_white_targets'])
 assert d['sufficient_component_targets'].shape==(3,) and np.all(d['sufficient_component_targets']>0) and np.all(d['scale']>0)
 s=P.read_pair(r['solution'],tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale'))
 for n,v in s.items():keep('parent_solution_'+n,v)
 nodes=(s['final_potential_nodes_hi'],s['final_potential_nodes_lo']);action=(s['final_original_action_hi'],s['final_original_action_lo']);residual=(s['final_original_residual_hi'],s['final_original_residual_lo'])
 assert nodes[0].shape==nodes[1].shape==(11135,) and np.array_equal(s['original_positive_scale'],d['scale']) and all(np.array_equal(s['original_rhs_'+w],d['rhs'][i]) for i,w in enumerate(('hi','lo')))
 assert np.array_equal(s['final_original_raw_scaled_ratios'],np.asarray(r['solution']['metadata']['original_component_ratios'])) and not np.all(s['final_original_raw_scaled_ratios']<=1e-10)
 current=dict(action=action,residual=residual,ratios=s['final_original_raw_scaled_ratios'],global_ratios=s['final_original_global_ratios'],admitted=False)
 inp=P.checkpoint('INPUT',arrays(),dict(kind='exact_refused_coupled_York_final_seed_and_frozen_operator',parent_input=thin(r['input']),parent_solution=thin(r['solution']),preserved_parent_controls=r['controls'],preserved_parent_checkpoints=r['checkpoints'],all_parent_input_fields_bitcopied=True,final_paired_seed_bitcopied=True,old_original_rows_admitted=False,old_geometry_source_fixture_support_or_iterations_replayed=False,new_control_ordinals_are_separate=True,cap=CAP,original_row_tolerance=1e-10))
 d['input_ref']=inp;P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();return nodes,current,d,inp

def warm_packet(parent,proof):
 nodes,current,d,inp=load_warm(parent);fixture_meta=york_fresh_twolevel_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(fixture_meta,controls=P.CHECKS))
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();plan=york_coarse_plan(d['geometry'],'new_coarse');pre=york_new_coarse_gram(d,plan,'new_coarse')
 coarse=P.checkpoint('COARSE',arrays(),dict(kind='new_coupled_coarse_basis_Gram_and_strict_factor',input_ref=thin(inp),coarse_dimension=2730,extended_dimension=13865,coarse_Gram_is_approximate_preconditioner=True,full_map_cross_terms_retained=True,axis_duplicates_combined_in_canonical_upper=True,jitter_added=False,positive_Cholesky_required=True,coarse_global_coercivity_claimed=False,physical_boundary_adopted=False))
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.update(stage='new_coupled_twolevel_warm_correction',cap=CAP);nodes,current,solver=york_twolevel_warm_correction(nodes,current,d,pre,'twolevel_york',CAP)
 Q.york_pair_keep('final_potential_nodes',nodes,keep);Q.york_pair_keep('original_rhs',d['rhs'],keep);Q.york_pair_keep('final_original_action',current['action'],keep);Q.york_pair_keep('final_original_residual',current['residual'],keep);keep('final_original_raw_scaled_ratios',current['ratios']);keep('final_original_global_ratios',current['global_ratios']);keep('original_positive_scale',d['scale'])
 solution=P.checkpoint('SOLUTION',arrays(),dict(kind='one_bounded_coupled_twolevel_York_original_row_result',input_ref=thin(inp),fixture=thin(fixture),coarse=thin(coarse),solver=solver,original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),original_global_ratios=current['global_ratios'].tolist(),controls=P.CHECKS,cap=CAP,max_new_cycles=1,physical_TT_prepared=False,potential_error_bound_claimed=False))
 projection=None;projection_admitted=False
 if current['admitted']:
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();scope=Q.york_point_projection(nodes,current,d);projection_admitted=scope['compact_weak_TT_original_rows_admitted'];projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(solution),input_ref=thin(inp),original_raw_scaled_ratios=current['ratios'].tolist(),**scope))
 status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if current['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED')
 return dict(status=status,input=inp,fixture=fixture,coarse=coarse,solution=solution,projection=projection,checkpoints=P.RECORDS,controls=P.CHECKS,preserved_parent_controls=parent['controls'],preserved_parent_checkpoints=parent['checkpoints'],parent_terminal=TERMINAL,parent_original_rows_admitted=False,original_rows_admitted=current['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,coarse_dimension=2730,extended_dimension=13865,max_new_cycles=1,cap=CAP,all_full_coupled_map_entries_retained=True,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and all(v is not None for v in TERMINAL.values()) and PROOF_SHA is not None,'Held reviews and actual refused coupled closure required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_one_pass_coupled_twolevel_York_correction');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  parent,proof=warm_admission();case=warm_packet(parent,proof);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  current=arrays()
  if current:P.checkpoint('ERROR_RAW',current,dict(kind='available_new_coupled_coarse_or_twolevel_York_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
