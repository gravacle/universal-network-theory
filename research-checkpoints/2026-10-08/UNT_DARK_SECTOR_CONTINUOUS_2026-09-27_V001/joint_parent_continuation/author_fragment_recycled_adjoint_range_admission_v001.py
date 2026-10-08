"""Definitions only; globals bind/json/P.path/P.INPUTS. Selected closed75215.
The adjoint/range calculation is NEW; no old map, payload or solver replay here.
Both original qualifications and finite literal/frozen mismatch remain separate.
"""
def adjoint_range_admission():
 stem='CROSS_U_RECYCLED_TRACE_TARGET_RATE_RESPONSE_V001';source='cross_u_recycled_trace_target_rate_response_v001.py'
 sh='18fb6bc3a3e3ce7bf47769c1e586cf77e2530d95fac05023f32201252638c414';ph='ea5d3d9c65e3250f90bf96a317651b7d2aeefc27789b8b74f6f5e5a08c1f3d6b'
 t=dict(pid=75215,result_sha256='4fa6fe13c1a32163cb9f867143389946eda19fc17e001834400346483417af0e',receipt_sha256='0a7a1c4b8c0d8f334b8404d41644955dd32e4305443b53c2125655d3c578e0cb',error_sha256=None)
 proofn='READONLY_RECYCLED_TRACE_RESPONSE_CLOSURE_V001_RESULT.json';proofh='dd392d8a8ea0dba45e418efa34d53f5c0e6f0ce1340f6c7e113f6a502f928055'
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',t['result_sha256']),(stem+'_RECEIPT.json',t['receipt_sha256']),(proofn,proofh)):assert h is not None;bind(n,h)
 r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text());proof=json.loads(P.path(proofn).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==t['result_sha256'] and rc.get('error_sha256') is None and r['owner']==rc['owner'] and r['owner']['pid']==75215 and r['owner']['source_sha256']==sh
 assert r['status']=='RECYCLED_LITERAL_TRACE_RESPONSE_NOT_ADMITTED' and r['frozen_original_response_admitted'] is False and r['literal_original_response_admitted'] is False and r['original_six_gates_unchanged'] is True and r['physical_adoption'] is False
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and len(r['checkpoints'])==14 and len(r['controls'])==6 and [c['ordinal'] for c in r['controls']]==list(range(6)) and all(c['passed'] and c['tolerance']==2e-11 for c in r['controls'])
 assert proof['status']=='SAVED_RECYCLED_TRACE_RESPONSE_CLOSURE_PASS' and proof['owner_pid']==76269 and proof['parent']==t and proof['controls']==6 and proof['committed_pairs']==14 and proof['physical_adoption'] is False and proof['frozen_original_response_admitted'] is False and proof['literal_original_response_admitted'] is False
 def selected(q):
  assert q in r['checkpoints']
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
  a=json.loads(P.path(q['commit_file']).read_text());assert a=={n:q[n] for n in ('file','sha256','metadata')} and a['metadata']['owner']==r['owner'] and a['metadata']['qualification']==r['qualification'] and a['metadata']['failed'] is False
  return dict(a,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 inp,response,readout=(selected(r[n]) for n in ('input','response','readout'));im,rm,lm=(q['metadata'] for q in (inp,response,readout))
 assert im['kind']=='cached_trace_response_with_four_fixed_snapshot_differences' and rm['kind']=='one_NEW_recycled_correction_to_authenticated_nonadmitted_trace_seed' and lm['kind']=='saved_old_literal_plus_only_NEW_exact_increment'
 assert im['parent_terminal']==r['parent_terminal'] and im['parent_canonical_response_admitted'] is False and im['zero_native_RHS_relative_ratio'] is None and lm['zero_native_RHS_relative_ratio'] is None and lm['configuration_changed'] is False and lm['primitive_stationarity_mismatch_resolved'] is False
 def schema(q,n,shape,dtype='float64'):assert q['metadata']['schema'][n]==dict(shape=list(shape),dtype=dtype,finite=True),(q['file'],n)
 for prefix,fields,shape in (('frozen_native_',('L','D','eL','eD'),(32,15136,3,3)),('frozen_native_',('M0','eM0'),(15136,3,3)),('frozen_metric_',('B','eB'),(15136,99,6)),('frozen_metric_',('T','eT'),(15136,6,6)),('frozen_metric_',('ih',),(15136,3,3)),('frozen_metric_',('N','mu'),(15136,))):
  for n in fields:schema(inp,prefix+n,shape)
 for n,shape in (('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44)),('r',(87,)),('z',(45,)),('native_scale',(33,3,87,45)),('metric_scale',(6,87,45)),('scalar_scale',(87,45))):schema(inp,'original_basis_'+n,shape)
 for n in ('cell_i','cell_j'):schema(inp,'original_basis_'+n,(3784,),'int64')
 for n in ('inherited_original_native_affine_reference','inherited_original_native_canonical_reference'):schema(inp,n,(33,3,87,45))
 for w in ('hi','lo'):
  schema(inp,'NEW_t_target_RHS_'+w,(403340,))
  for n in ('final_paired_response','unchanged_original_RHS','final_frozen_action','final_frozen_residual'):schema(response,n+'_'+w,(403340,))
  for n in ('new_literal_action','new_literal_residual','literal_minus_frozen_derivative'):schema(readout,'recycled_trace_literal_translation_'+n+'_'+w,(403340,))
 schema(response,'final_frozen_original_six_scores',(3,2));schema(response,'recycled_trace_warm_uncancelled_update_bound',(403340,));schema(readout,'recycled_trace_literal_translation_literal_original_scores',(3,2))
 original=dict(pid=71394,result_sha256='6041c495ea6d837840d6f4bde687ba3dcf604131087c2ed7b395ae67fe284bb6',receipt_sha256='1aee74e2996755c644e242e78ecb488f2bc334dc63aa6568a5d3309f4c8235a3');assert r['parent_terminal']==original and r['parent_original_nonadmission_preserved'] is True
 priorproof=im['saved_proof'];assert priorproof==dict(file='READONLY_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_V001_RESULT.json',sha256='eb9c8fbe3736069d72b1be992e4637b33ff7b53408157a7f60ca510e7dcc4153',status='SAVED_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_PASS')
 assert rc['input_sha256'][str(P.path(priorproof['file']).resolve())]==priorproof['sha256'];bind(priorproof['file'],priorproof['sha256'])
 refs=dict(input=inp,response=response,readout=readout,terminal=t,proof=dict(file=proofn,sha256=proofh,status=proof['status']),prior71394=dict(terminal=original,proof=priorproof,input=im['parent_input'],response=im['parent_approximation'],readout=im['parent_readout']),fixed=im['fixed'],owned_background=im['owned_background'],controls=r['controls'],source_qualification=dict(frozen_original_response_admitted=False,literal_original_response_admitted=False,canonical_or_Jacobian_direction_adopted=False,physical_adoption=False),latest_six_original_gates=dict(tolerance=1e-10,frozen=rm['solver']['original_six_scores'],literal=lm['literal_original_six_scores']),positive_envelopes=dict(native=('frozen_native_eL','frozen_native_eD','frozen_native_eM0'),metric=('frozen_metric_eB','frozen_metric_eT'),update_bound='recycled_trace_warm_uncancelled_update_bound'),physical_ports=None)
 return dict(P.INPUTS),refs
