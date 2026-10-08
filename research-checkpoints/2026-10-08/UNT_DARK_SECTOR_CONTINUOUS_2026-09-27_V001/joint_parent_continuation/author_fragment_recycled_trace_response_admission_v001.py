"""Definitions only. Globals bind/json/P.path/P.INPUTS; no payload/helper replay.
Select the actual refused71394 state, fixed four snapshots and earned72874 proof.
No old coefficient/basis/feature preparation or physical qualification is implied.
"""
def recycled_trace_admission():
 stem='CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001';source='cross_u_initial_york_trace_target_rate_response_v001.py'
 sh='23cbba6893b934236c8fff2c8ff4dda63f6808f589a04f701dcd536fdd31de27';ph='793cc56c47dabc8a7baa7838b57fd95b658d655242a71e112d0d64b932ba44f7'
 t=dict(pid=71394,result_sha256='6041c495ea6d837840d6f4bde687ba3dcf604131087c2ed7b395ae67fe284bb6',receipt_sha256='1aee74e2996755c644e242e78ecb488f2bc334dc63aa6568a5d3309f4c8235a3')
 proofn='READONLY_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_V001_RESULT.json';proofh='eb9c8fbe3736069d72b1be992e4637b33ff7b53408157a7f60ca510e7dcc4153'
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',t['result_sha256']),(stem+'_RECEIPT.json',t['receipt_sha256']),(proofn,proofh)):bind(n,h)
 r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text());proof=json.loads(P.path(proofn).read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==t['result_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==71394 and r['owner']['source_sha256']==sh
 assert r['status']=='NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED' and r['literal_original_response_admitted'] is False and r['old_frozen_inverse_numerically_admitted'] is False
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and r['physical_adoption'] is False and r['whole_grid_five_field_preparation'] is False and r['original_primitive_stationarity_mismatch_resolved'] is False
 assert len(r['controls'])==3 and [q['ordinal'] for q in r['controls']]==[0,1,2] and len(r['checkpoints'])==13 and all(q['passed'] and q['tolerance']==2e-11 for q in r['controls'])
 assert proof['status']=='SAVED_INITIAL_YORK_TRACE_TARGET_RESPONSE_CLOSURE_PASS' and proof['parent']==dict(t,error_sha256=None) and proof['controls']==3 and proof['committed_pairs']==13 and proof['physical_adoption'] is False and proof['literal_original_response_admitted'] is False and proof['frozen_numerical_inverse_admitted'] is False
 def selected(q,output):
  m=rc['output_sha256'] if output else rc['input_sha256']
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert m[n if output else str(P.path(n).resolve())]==h;bind(n,h)
  a=json.loads(P.path(q['commit_file']).read_text());assert a['file']==q['file'] and a['sha256']==q['sha256'] and (q.get('metadata') is None or a['metadata']==q['metadata'])
  out=dict(a,commit_file=q['commit_file'],commit_sha256=q['commit_sha256']);md=out['metadata'];assert md['failed'] is False and all(v['finite'] for v in md['schema'].values())
  if output:assert out in r['checkpoints'] and md['owner']==r['owner'] and md['qualification']==r['qualification']
  return out
 def schema(q,n,shape):assert q['metadata']['schema'][n]==dict(shape=list(shape),dtype='float64',finite=True),(q['file'],n)
 inp=selected(r['input'],True);approx=selected(r['numerical_approximation'],True);readout=selected(r['readout'],True);im=inp['metadata']
 assert im['kind']=='NEW_compact_total_trace_target_RHS_and_immutable_numerical_preconditioner' and len(im['schema'])==38 and im['configuration_unchanged'] is True and im['cap']==160 and im['cycles']==1 and im['zero_source_relative_ratio'] is None
 assert approx['metadata']['kind']=='NEW_target_frozen_signed_numerical_approximate_inverse' and approx['metadata']['frozen_original_scores']==r['numerical_approximation']['metadata']['frozen_original_scores'] and readout['metadata']['kind']=='NEW_current_literal_target_response_and_frozen_preconditioner_remainder'
 for n in ('NEW_trace_target_final_update_updated_nodes','NEW_trace_target_final_frozen_action','NEW_trace_target_final_frozen_residual','complete_rate_direction_literal_full_action'):
  for w in ('hi','lo'):schema(readout if n.startswith('complete_') else approx,n+'_'+w,(403340,))
 schema(approx,'NEW_trace_target_final_frozen_original_admission_scores',(3,2));schema(inp,'NEW_t_target_RHS_hi',(403340,));schema(inp,'NEW_t_target_RHS_lo',(403340,))
 snapshot_name='NEW_trace_target_frozen_approximate_inverse_original_iterate';iterations={}
 for k in (40,80,120,160):
  hits=[q for q in r['checkpoints'] if q['metadata']['kind']=='unqualified_restart_snapshot_signed_MINRES_iterate' and q['metadata']['iteration']==k];assert len(hits)==1
  q=selected(hits[0],True);schema(q,snapshot_name,(403340,));iterations[k]=q
 pilots=[selected(q,False) for q in im['pilot_columns']];prior=selected(im['prior_signed_primitive_readout'],False)
 assert len(pilots)==4 and [q['metadata']['owner']['pid'] for q in pilots]==[50104]*4 and [q['metadata']['column'] for q in pilots]==[0,1,2,3] and prior['metadata']['owner']['pid']==50104
 assert prior['metadata']['offsets_targets_or_state_refitted'] is False and readout['metadata']['prior_signed_primitive_readout']=={n:prior[n] for n in ('file','sha256','commit_file','commit_sha256')}
 return dict(P.INPUTS),dict(input=inp,approximation=approx,readout=readout,iterations=iterations,pilot_columns=pilots,prior_signed_primitive_readout=prior,fixed=im['fixed'],owned_background=im['owned_background'],original_controls=r['controls'],terminal=t,proof=dict(file=proofn,sha256=proofh,status=proof['status']),snapshot_operand_name=snapshot_name,source_qualification=dict(literal_original_response_admitted=False,frozen_numerical_inverse_admitted=False,canonical_or_Jacobian_direction_adopted=False,physical_adoption=False),physical_ports=None)
