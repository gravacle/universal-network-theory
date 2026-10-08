"""Held direct fine paired-PCG; same map/target/factor, fresh original gates."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V006'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='5ecfa2446693b60e669a16e6cf2dfb954fd4b67731a30b1a98c412b676287f2d'
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V005'
PARENT_SOURCE='cross_u_compact_york_longitudinal_projection_v005.py'
PARENT_SOURCE_SHA='04ed2f9547d20c5ed177c96b53f9a060cc7d74b6f62d818c783fd78192ceee05'
PARENT_PROTOCOL_SHA='c57d6307466b2e04675e7bbe19783b4db734d9a505b6f45ccf98f5194f464924'
TERMINAL=dict(pid=71992,result_sha256='a3aaf3f4b938b621d6491d3fc9fcc4b4a5d2b05e71bf0b4a588eab08d8547ccb',receipt_sha256='eefef813468b05e23aa47a872c3128916d3a93cb45fc55b10cf180244aa3ff5c')
PROOF='READONLY_WARM_TWOLEVEL_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
PROOF_SHA='9ba456c04cb20263bf43a5a04325531a727ae5f93a04bbe5608b1deb6c53771b'
KERNEL='author_fragment_fine_paired_york_pcg_v001.py'
KERNEL_SHA='3b459e80228dba51c20fcde5780d5db0d676e39646d146bfdba4c8f47011c181'
CAP=512
D=C=Q=P=np=None

def keep(n,a):return Q.keep(n,np.asarray(a).copy())
def arrays():return {n:np.asarray(a).copy() for n,a in {**P.RAW,**P.AVAILABLE,**P.DD_ARRAY_CURRENT.get('arrays',{})}.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def initialize():
 global D,C,Q,P,np
 assert hashlib.sha256((BASE/PARENT_SOURCE).read_bytes()).hexdigest()==PARENT_SOURCE_SHA
 spec=importlib.util.spec_from_file_location('same_factor_warm_york_definitions_only',BASE/PARENT_SOURCE);D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D);D.initialize()
 C,Q,P,np=D.C,D.Q,D.P,D.np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((PARENT_SOURCE,PARENT_SOURCE_SHA),(PARENT+'.md',PARENT_PROTOCOL_SHA),(KERNEL,KERNEL_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):Q.bind(n,h)
 for n,h in (('authoring_fine_york_pcg_caller_94_bed6ae03.py','bed6ae03f1bb2fe1469187ee149866dd42ceade562e4727e1d056e473ad01314'),('authoring_fine_york_pcg_protocol_12_d70f0482.md','d70f0482539a722d6cc4be6eb938204c9fdbdf7852fb12be5d0efce7e2437cc5')):Q.bind(n,h)
 exec(compile((BASE/KERNEL).read_text(),str(BASE/KERNEL),'exec'),globals())

def warm_admission():
 for n,h in ((PARENT+'_RESULT.json',TERMINAL['result_sha256']),(PARENT+'_RECEIPT.json',TERMINAL['receipt_sha256']),(PROOF,PROOF_SHA)):Q.bind(n,h)
 r=json.loads(P.path(PARENT+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT+'_RECEIPT.json').read_text());proof=json.loads(P.path(PROOF).read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==TERMINAL['result_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==PARENT_SOURCE_SHA
 assert r['status']=='ORIGINAL_YORK_ROWS_NOT_ADMITTED' and r['original_rows_admitted'] is False and r['compact_weak_TT_original_rows_admitted'] is False and r['projection'] is None and r['vector_space_dimension']==11135 and r['coarse_dimension']==2730
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
 assert r['all_full_coupled_map_entries_retained'] is True and r['coarse_Gram_or_fixture_replayed'] is False and r['cap']==160 and len(r['controls'])==1 and len(r['checkpoints'])==6 and all(c['passed'] and c['tolerance']==2e-11 for c in r['controls'])
 assert proof['status']=='SAVED_WARM_TWOLEVEL_YORK_CLOSURE_PASS' and proof['parent']==dict(TERMINAL,error_sha256=None) and proof['controls']==1 and proof['committed_pairs']==6 and proof['original_rows_admitted'] is False and proof['compact_weak_TT_original_rows_admitted'] is False
 assert proof['all_immutable_parent_INPUT_fields_bitcopied'] is True and proof['selected_earned_coarse_fields_bitcopied']==8 and proof['distinct_latest_final_solution_fields']==11 and proof['earned_coarse_plan_and_factor_word_copies_authenticated_only'] is True and proof['L_action_Gram_factorization_triangular_MINRES_projection_FE_or_fixture_replayed'] is False and proof['physical_adoption'] is False
 for q in (r['input'],r['solution']):
  assert q in r['checkpoints'] and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;Q.bind(n,h)
  assert json.loads(P.path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')}
 assert r['input']['metadata']['kind']=='unchanged_V004_INPUT_and_latest_paired_seed_and_earned_coarse_factor' and len(r['input']['metadata']['schema'])==360 and not any(n.startswith('fine_pcg_seed_') for n in r['input']['metadata']['schema'])
 assert r['solution']['metadata']['kind']=='one_warm_correction_with_earned_coupled_twolevel_factor' and r['solution']['metadata']['original_rows_admitted'] is False and r['solution']['metadata']['earned_coarse_ref']==r['earned_coarse_ref']
 coarse=r['earned_coarse_ref']
 for n,h in ((coarse['file'],coarse['sha256']),(coarse['commit_file'],coarse['commit_sha256'])):assert rc['input_sha256'][str(P.path(n).resolve())]==h;Q.bind(n,h)
 cm=json.loads(P.path(coarse['commit_file']).read_text());assert cm['file']==coarse['file'] and cm['sha256']==coarse['sha256'] and cm['metadata']['kind']=='new_coupled_coarse_basis_Gram_and_strict_factor' and cm['metadata']['owner']['pid']==70321 and cm['metadata']['jitter_added'] is False
 return r,proof

def load_warm(r):
 s=P.read_pair(r['solution'],tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale'))
 for n,v in s.items():keep('fine_pcg_seed_'+n,v)
 a=P.read_pair(r['input'],tuple(r['input']['metadata']['schema']))
 for n,v in a.items():keep(n,v)
 mask=a['compact_vector_mask'];assert mask.shape==(3,87,45) and mask.dtype==np.dtype('bool') and np.array_equal(np.sum(mask,axis=(1,2)),np.asarray((3740,3655,3740))) and np.all(a['diagonal_positivity_margin'][mask]>0)
 d=dict(maps=(a['L_maps_hi'],a['L_maps_lo']),map_envelope=a['L_map_operation_envelope'],ih=a['ih'],sqrt_h=a['sqrt_h'],PiTF=(a['PiTF_hi'],a['PiTF_lo']),geometry={n:a[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')},rhs=(a['rhs_hi'][mask],a['rhs_lo'][mask]),rhs_envelope=a['rhs_operation_envelope'][mask],scale=a['positive_Jacobi_congruence_scale'][mask])
 nodes=(s['final_potential_nodes_hi'],s['final_potential_nodes_lo']);action=(s['final_original_action_hi'],s['final_original_action_lo']);residual=(s['final_original_residual_hi'],s['final_original_residual_lo'])
 assert nodes[0].shape==nodes[1].shape==(11135,) and np.all(d['scale']>0) and np.array_equal(s['original_positive_scale'],d['scale']) and all(np.array_equal(s['original_rhs_'+w],d['rhs'][i]) for i,w in enumerate(('hi','lo')))
 assert np.array_equal(s['final_original_raw_scaled_ratios'],np.asarray(r['solution']['metadata']['original_component_ratios'])) and not np.all(s['final_original_raw_scaled_ratios']<=1e-10)
 current=dict(action=action,residual=residual,ratios=s['final_original_raw_scaled_ratios'],global_ratios=s['final_original_global_ratios'],admitted=False)
 c=lambda n:a['continued_coarse_new_coarse_'+n]
 plan=dict(ci=c('fine_to_coarse_i'),cj=c('fine_to_coarse_j'),node_weights=c('physical_node_interpolation_weights'),corner_coefficients=c('coarse_hat_values_at_fine_cell_corners'),indices=c('coarse_global_local_indices'),mask=c('coarse_mask'))
 scale=c('coarse_positive_scale');factor=c('normalized_coarse_Cholesky');assert scale.shape==(2730,) and factor.shape==(2730,2730) and np.all(scale>0) and np.all(np.diag(factor)>0) and np.array_equal(plan['mask'],C.york_coarse_mask())
 pre=dict(plan=plan,coarse_scale=scale,coarse_factor=factor,fine_scale=d['scale'],prolong=lambda x:C.york_coarse_prolong(x,plan),adjoint=lambda x:C.york_coarse_adjoint(x,plan))
 inp=P.checkpoint('INPUT',arrays(),dict(kind='all_V005_INPUT_and_latest_paired_seed_for_direct_fine_PCG',parent_input=thin(r['input']),parent_solution=thin(r['solution']),earned_coarse_ref=r['earned_coarse_ref'],preserved_parent_controls=r['controls'],preserved_parent_checkpoints=r['checkpoints'],all_360_parent_input_fields_bitcopied=True,new_latest_solution_prefix='fine_pcg_seed_',latest_SOLUTION_loaded_before_INPUT=True,coarse_Gram_factor_fixture_or_old_iterations_replayed=False,direct_fine_dimension=11135,cap=CAP,no_automatic_restart=True,original_row_tolerance=1e-10))
 d['input_ref']=inp;P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();return nodes,current,d,pre,inp

def warm_packet(parent,proof):
 nodes,current,d,pre,inp=load_warm(parent);fm=fresh_fine_pcg_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(fm,controls=P.CHECKS.copy()))
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();nodes,current,solver=york_fine_pcg_warm(nodes,current,d,pre,'fine_york_PCG',CAP)
 Q.york_pair_keep('final_potential_nodes',nodes,keep);Q.york_pair_keep('original_rhs',d['rhs'],keep);Q.york_pair_keep('final_original_action',current['action'],keep);Q.york_pair_keep('final_original_residual',current['residual'],keep);keep('final_original_raw_scaled_ratios',current['ratios']);keep('final_original_global_ratios',current['global_ratios']);keep('original_positive_scale',d['scale']);assert len(P.CHECKS)==3
 solution=P.checkpoint('SOLUTION',arrays(),dict(kind='bounded_direct_fine_PCG_original_York_rows',input_ref=thin(inp),fixture=thin(fixture),earned_coarse_ref=parent['earned_coarse_ref'],solver=solver,original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),original_global_ratios=current['global_ratios'].tolist(),controls=P.CHECKS.copy(),cap=CAP,physical_TT_prepared=False,potential_error_bound_claimed=False))
 projection=None;projection_admitted=False
 if current['admitted']:
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();scope=Q.york_point_projection(nodes,current,d);projection_admitted=scope['compact_weak_TT_original_rows_admitted'];projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(solution),input_ref=thin(inp),original_raw_scaled_ratios=current['ratios'].tolist(),**scope))
 status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if current['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED')
 return dict(status=status,input=inp,fixture=fixture,solution=solution,projection=projection,earned_coarse_ref=parent['earned_coarse_ref'],checkpoints=P.RECORDS,controls=P.CHECKS,preserved_parent_controls=parent['controls'],preserved_parent_checkpoints=parent['checkpoints'],parent_terminal=TERMINAL,parent_original_rows_admitted=False,original_rows_admitted=current['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,coarse_dimension=2730,solver='direct_fine_paired_PCG',cap=CAP,automatic_restart=False,coarse_Gram_or_fixture_replayed=False,all_full_coupled_map_entries_retained=True,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'FULL root/distinct reviews required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_direct_fine_paired_York_PCG');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  parent,proof=warm_admission();case=warm_packet(parent,proof);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  current=arrays()
  if current:P.checkpoint('ERROR_RAW',current,dict(kind='available_NEW_fine_PCG_vectors_contacts_and_history',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
