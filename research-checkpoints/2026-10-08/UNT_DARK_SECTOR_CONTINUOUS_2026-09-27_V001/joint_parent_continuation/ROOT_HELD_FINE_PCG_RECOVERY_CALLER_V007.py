"""Held recovery before the unearned weighted first energy; same fine-PCG budget."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V007'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='8401b39d223fe99df8b0814b09788a6bff99128f563b8ed5e3b903fe211fbbcd'
PROVIDER='cross_u_compact_york_longitudinal_projection_v006.py'
PROVIDER_SHA='a4c442fa10a50fe63e5cc5c70984786d23e171cd936b5aa6f7313f4ac412b6ef'
KERNEL='author_fragment_fine_paired_york_pcg_v003.py'
KERNEL_SHA='0b44ede743259b83a786d72259143f8fce06c1fec9a6d0e9d13049970b4252b0'
ADMISSION='author_fragment_failed_fine_pcg_selected_admission_v002.py'
ADMISSION_SHA='5642fca082501fa357c904057d4583937a6ed7e081eaf906f28cf0308f581f23'
CAP=512
D=C=Q=P=np=None

def keep(n,a):return Q.keep(n,np.asarray(a).copy())
def arrays():return {n:np.asarray(a).copy() for n,a in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def bind(n,h):return Q.bind(n,h)
def initialize():
 global D,C,Q,P,np
 assert ADMISSION is not None and ADMISSION_SHA is not None and hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('failed_fine_PCG_definitions_only',BASE/PROVIDER);D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D);D.initialize()
 C,Q,P,np=D.C,D.Q,D.P,D.np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),('author_fragment_fine_paired_york_pcg_v002.py','9d13ec971ad50f81cc40c93de16ddf077e269319e04cf73ebb65b047a1b66ea7'),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 for n in (KERNEL,ADMISSION):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def load_recovery(refs):
 raw=P.read_pair(refs['raw'],tuple(refs['raw']['metadata']['schema']));assert len(raw)==59
 for n,a in raw.items():keep('cached_V006_RAW_'+n,a)
 fixture=P.read_pair(refs['fixture'],tuple(refs['fixture']['metadata']['schema']));assert len(fixture)==178
 for n,a in fixture.items():keep('cached_V006_FIXTURE_'+n,a)
 old=P.read_pair(refs['input'],tuple(refs['input']['metadata']['schema']));assert len(old)==478 and not any(n.startswith(('cached_V006_RAW_','cached_V006_FIXTURE_')) for n in old)
 for n,a in old.items():keep(n,a)
 P.CHECKS[:]=[dict(c) for c in refs['controls']];assert len(P.CHECKS)==2
 for c in P.CHECKS:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name'])
  for suffix in ('actual','expected','envelope'):keep(prefix+suffix,fixture[prefix+suffix])
 mask=old['compact_vector_mask'];assert mask.shape==(3,87,45) and mask.dtype==np.dtype('bool') and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740)))
 d=dict(maps=(old['L_maps_hi'],old['L_maps_lo']),map_envelope=old['L_map_operation_envelope'],ih=old['ih'],sqrt_h=old['sqrt_h'],PiTF=(old['PiTF_hi'],old['PiTF_lo']),geometry={n:old[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')},rhs=(old['rhs_hi'][mask],old['rhs_lo'][mask]),rhs_envelope=old['rhs_operation_envelope'][mask],scale=old['positive_Jacobi_congruence_scale'][mask])
 pair=lambda n:(raw[n+'_hi'],raw[n+'_lo']);nodes=pair('fine_york_PCG_current_nodes');residual=pair('fine_york_PCG_recursive_residual')
 action=tuple(old['fine_pcg_seed_final_original_action_'+w] for w in ('hi','lo'));scores=old['fine_pcg_seed_final_original_raw_scaled_ratios'];global_scores=old['fine_pcg_seed_final_original_global_ratios']
 for i,w in enumerate(('hi','lo')):
  assert np.array_equal(nodes[i],old['fine_pcg_seed_final_potential_nodes_'+w]) and np.array_equal(nodes[i],raw['fine_york_PCG_start_nodes_'+w])
  assert np.array_equal(residual[i],old['fine_pcg_seed_final_original_residual_'+w]) and np.array_equal(residual[i],raw['fine_york_PCG_start_original_residual_'+w]) and np.array_equal(d['rhs'][i],old['fine_pcg_seed_original_rhs_'+w])
  assert np.array_equal(raw['fine_york_PCG_preconditioned_residual_'+w],raw['fine_york_PCG_search_direction_'+w])
 assert np.array_equal(old['fine_pcg_seed_original_positive_scale'],d['scale']) and not np.all(scores<=1e-10)
 first=dict(action=pair('fine_york_PCG_direction_action_completed_action'),L=pair('fine_york_PCG_direction_action_trial_longitudinal_partial'),density=pair('fine_york_PCG_direction_action_trial_raised_longitudinal_density_partial'),envelope=raw['fine_york_PCG_direction_action_positive_positive_scatter'][mask],L_envelope=raw['fine_york_PCG_direction_action_positive_L_operation_envelope'],density_envelope=raw['fine_york_PCG_direction_action_positive_density_operation_envelope'])
 for w in ('hi','lo'):assert np.array_equal(raw['fine_york_PCG_direction_action_action_restricted_'+w][mask],raw['fine_york_PCG_direction_action_completed_action_'+w])
 initial=dict(z=pair('fine_york_PCG_preconditioned_residual'),rz=pair('fine_york_PCG_rz'),rho=float(raw['fine_york_PCG_initial_rz_inner_binary64_readout']),direction=pair('fine_york_PCG_search_direction'),start_residual_envelope=raw['fine_york_PCG_start_original_residual_envelope'],first_action=lambda label:fine_pcg_cached_direction_action(first,d,label))
 assert initial['rho']>0 and np.all(initial['start_residual_envelope']>=0) and all(np.all(first[n]>=0) for n in ('envelope','L_envelope','density_envelope'))
 c=lambda n:old['continued_coarse_new_coarse_'+n]
 plan=dict(ci=c('fine_to_coarse_i'),cj=c('fine_to_coarse_j'),node_weights=c('physical_node_interpolation_weights'),corner_coefficients=c('coarse_hat_values_at_fine_cell_corners'),indices=c('coarse_global_local_indices'),mask=c('coarse_mask'))
 pre=dict(plan=plan,coarse_scale=c('coarse_positive_scale'),coarse_factor=c('normalized_coarse_Cholesky'),fine_scale=d['scale'],prolong=lambda x:C.york_coarse_prolong(x,plan),adjoint=lambda x:C.york_coarse_adjoint(x,plan))
 current=dict(action=action,residual=residual,ratios=scores,global_ratios=global_scores,admitted=False)
 inp=P.checkpoint('INPUT',arrays(),dict(kind='all_failed_V006_INPUT_and_first_direction_words_before_unearned_energy',failed_terminal=refs['terminal'],failed_input=thin(refs['input']),failed_fixture=thin(refs['fixture']),failed_raw=thin(refs['raw']),preserved_failed_controls=refs['controls'],preserved_failed_checkpoints=refs['records'],all_478_input_fields_bitcopied=True,all_178_fixture_fields_bitcopied=True,all_59_failed_raw_fields_bitcopied=True,fixture_prefix='cached_V006_FIXTURE_',raw_prefix='cached_V006_RAW_',initial_B_and_first_A_and_positive_bounds_replayed=False,original_fixture_replayed=False,same_original_cap=512,new_node_updates_previously_earned=0,physical_adoption=False))
 earned=P.checkpoint('FIXTURE',{n:np.asarray(a).copy() for n,a in fixture.items()},dict(kind='earned_failed_V006_fresh_fixture_wordcopies',failed_fixture=thin(refs['fixture']),controls=P.CHECKS.copy(),fixture_called=False))
 d['input_ref']=inp;P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear()
 for c in P.CHECKS:
  prefix='control_%03d_%s_'%(c['ordinal'],c['name'])
  for suffix in ('actual','expected','envelope'):keep(prefix+suffix,fixture[prefix+suffix])
 return nodes,current,d,pre,initial,inp,earned

def recovery_packet(refs):
 nodes,current,d,pre,initial,inp,earned=load_recovery(refs)
 meta=fresh_reassociated_weighted_energy_control();association=P.checkpoint('ASSOCIATION',arrays(),dict(meta,controls=P.CHECKS.copy()))
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear()
 nodes,current,solver=york_fine_pcg_warm(nodes,current,d,pre,'fine_york_PCG',CAP,initial)
 for n,a in (('final_potential_nodes',nodes),('original_rhs',d['rhs']),('final_original_action',current['action']),('final_original_residual',current['residual'])):Q.york_pair_keep(n,a,keep)
 keep('final_original_raw_scaled_ratios',current['ratios']);keep('final_original_global_ratios',current['global_ratios']);keep('original_positive_scale',d['scale']);assert len(P.CHECKS)==4
 solution=P.checkpoint('SOLUTION',arrays(),dict(kind='same_fine_PCG_after_cached_first_direction_weight_association_repair',input_ref=thin(inp),earned_fixture=thin(earned),association=thin(association),solver=solver,original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),original_global_ratios=current['global_ratios'].tolist(),controls=P.CHECKS.copy(),cap=512,physical_TT_prepared=False,potential_error_bound_claimed=False))
 projection=None;projection_admitted=False
 if current['admitted']:
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();scope=Q.york_point_projection(nodes,current,d);projection_admitted=scope['compact_weak_TT_original_rows_admitted'];projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(solution),input_ref=thin(inp),original_raw_scaled_ratios=current['ratios'].tolist(),**scope))
 status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if current['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED')
 return dict(status=status,input=inp,earned_fixture=earned,association=association,solution=solution,projection=projection,checkpoints=P.RECORDS,controls=P.CHECKS,failed_terminal=refs['terminal'],original_failed_publication_preserved=True,preserved_failed_controls=refs['controls'],preserved_failed_checkpoints=refs['records'],initial_B_or_first_A_or_old_fixture_replayed=False,original_rows_admitted=current['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,coarse_dimension=2730,cap=512,automatic_restart=False,all_full_coupled_map_entries_retained=True,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and ADMISSION is not None and ADMISSION_SHA is not None,'FULL root/distinct reviews required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_cached_first_fine_PCG_energy_recovery');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  refs=fine_pcg_failure_admission();case=recovery_packet(refs);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  raw=arrays()
  if raw:P.checkpoint('ERROR_RAW',raw,dict(kind='available_cached_recovery_and_NEW_fine_PCG_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
