"""Definitions only; globals bind/json/P.path/P.INPUTS. Authentic failed74275.
Select three earned records and first direction cache, never replay B/A/fixture.
The saved failure checker proof is not presumed earned; original failure stays.
"""
def fine_pcg_failure_admission():
 stem='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V006';source='cross_u_compact_york_longitudinal_projection_v006.py'
 sh='a4c442fa10a50fe63e5cc5c70984786d23e171cd936b5aa6f7313f4ac412b6ef';ph='5ecfa2446693b60e669a16e6cf2dfb954fd4b67731a30b1a98c412b676287f2d'
 t=dict(pid=74275,result_sha256=None,error_sha256='3b0418ecfc32f540e50bc7220c5f4748e5e16b910dfedaf273789c2c0449b627',receipt_sha256='73db4994b09f24d11b6d7aa4951c5e320ae7fb97fe372a825908df6119e05860')
 proofn='READONLY_WARM_TWOLEVEL_YORK_PROJECTION_CLOSURE_V001_RESULT.json';proofh='9ba456c04cb20263bf43a5a04325531a727ae5f93a04bbe5608b1deb6c53771b'
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_ERROR.json',t['error_sha256']),(stem+'_RECEIPT.json',t['receipt_sha256']),(proofn,proofh)):bind(n,h)
 r=json.loads(P.path(stem+'_ERROR.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text());proof=json.loads(P.path(proofn).read_text())
 assert rc['status']=='CLOSED_ERROR' and r['status']=='FAILED' and rc.get('result_sha256') is None and rc['error_sha256']==t['error_sha256'] and not P.path(stem+'_RESULT.json').exists()
 assert rc['owner']==r['owner'] and r['owner']['pid']==74275 and r['owner']['source_sha256']==sh and r['owner']['source_file']==source
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 records=r['checkpoints'];controls=r['controls'];assert len(records)==3 and len(controls)==2 and [c['ordinal'] for c in controls]==[0,1] and all(c['passed'] and c['tolerance']==2e-11 for c in controls)
 assert r['context']['stage']=='new_fine_paired_PCG' and r['context']['iteration']==1 and r['context']['cap']==512 and 'york_fine_pcg_action' in r['traceback'] and 'Dekker safe high/low operand domain' in r['traceback']
 def selected(q,output):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert (rc['output_sha256'][n] if output else rc['input_sha256'][str(P.path(n).resolve())])==h;bind(n,h)
  a=json.loads(P.path(q['commit_file']).read_text());assert a['file']==q['file'] and a['sha256']==q['sha256'] and ('metadata' not in q or a['metadata']==q['metadata'])
  out=dict(a,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
  if output:assert out in records and out['metadata']['owner']==r['owner'] and out['metadata']['qualification']==r['qualification']
  return out
 inp,fixture,raw=[selected(q,True) for q in records];im,fm,rm=(q['metadata'] for q in (inp,fixture,raw))
 assert (im['kind'],fm['kind'],rm['kind'])==('all_V005_INPUT_and_latest_paired_seed_for_direct_fine_PCG','fresh_coupled_anisotropic_fine_PCG_with_same_generic_loop','available_NEW_fine_PCG_vectors_contacts_and_history')
 assert [len(m['schema']) for m in (im,fm,rm)]==[478,178,59] and [m['failed'] for m in (im,fm,rm)]==[False,False,True] and all(v['finite'] for m in (im,fm,rm) for v in m['schema'].values())
 assert rm['context']==r['context'] and fm['controls']==controls and fm['cap']==12 and fm['original_rows_admitted'] is True and fm['old_York_or_twolevel_fixture_replayed'] is False
 assert im['all_360_parent_input_fields_bitcopied'] is True and im['new_latest_solution_prefix']=='fine_pcg_seed_' and im['latest_SOLUTION_loaded_before_INPUT'] is True and im['coarse_Gram_factor_fixture_or_old_iterations_replayed'] is False and im['direct_fine_dimension']==11135 and im['cap']==512 and im['original_row_tolerance']==1e-10
 assert not any(n.startswith('fine_york_PCG_node_update_') for n in rm['schema'])
 def schema(q,n,shape):assert q['metadata']['schema'][n]==dict(shape=list(shape),dtype='float64',finite=True),(q['file'],n)
 vectors=('preconditioned_residual','recursive_residual','current_nodes','search_direction','start_nodes','start_original_residual','direction_action_completed_action')
 tensors=('direction_action_trial_longitudinal_partial','direction_action_trial_raised_longitudinal_density_partial')
 for suffix in vectors+tensors+('rz','initial_rz_paired_inner_product'):
  for w in ('hi','lo'):schema(raw,'fine_york_PCG_'+suffix+'_'+w,(15136,3,3) if suffix in tensors else (() if suffix in ('rz','initial_rz_paired_inner_product') else (11135,)))
 for suffix,shape in (('initial_rz_inner_binary64_readout',()),('initial_rz_inner_operation_envelope',()),('start_original_residual_envelope',(11135,)),('direction_action_positive_positive_scatter',(3,87,45)),('direction_action_positive_L_operation_envelope',(15136,3,3)),('direction_action_positive_density_operation_envelope',(15136,3,3))):schema(raw,'fine_york_PCG_'+suffix,shape)
 for w in ('hi','lo'):schema(raw,'fine_york_PCG_direction_action_action_restricted_'+w,(3,87,45))
 prior_t=dict(pid=71992,result_sha256='a3aaf3f4b938b621d6491d3fc9fcc4b4a5d2b05e71bf0b4a588eab08d8547ccb',receipt_sha256='eefef813468b05e23aa47a872c3128916d3a93cb45fc55b10cf180244aa3ff5c',error_sha256=None)
 assert proof['status']=='SAVED_WARM_TWOLEVEL_YORK_CLOSURE_PASS' and proof['parent']==prior_t and proof['controls']==1 and proof['committed_pairs']==6 and proof['original_rows_admitted'] is False and proof['physical_adoption'] is False
 assert rc['input_sha256'][str(P.path(proofn).resolve())]==proofh
 prior={n:selected(im[n],False) for n in ('parent_input','parent_solution','earned_coarse_ref')}
 assert prior['parent_input']['metadata']['owner']['pid']==71992 and prior['parent_solution']['metadata']['owner']['pid']==71992 and prior['earned_coarse_ref']['metadata']['owner']['pid']==70321
 assert len(prior['parent_input']['metadata']['schema'])==360 and prior['parent_solution']['metadata']['original_rows_admitted'] is False
 return dict(input=inp,fixture=fixture,raw=raw,terminal=t,controls=controls,records=records,prior=prior,warm_proof=dict(file=proofn,sha256=proofh,status=proof['status']),failure_checker_proof=None,actual_node_updates_earned=0,physical_adoption=False)
