"""Definitions only; a complete closed NEW t response is an implementation-test operand.
Caller supplies bind/json/P.path/P.INPUTS and one RESPONSE_TERMINAL dictionary.
Literal admission is preserved separately; neither outcome adopts a physical state.
"""
def rate_comparison_admission():
 t=RESPONSE_TERMINAL
 assert all(t.get(k) is not None for k in ('pid','result_sha256','receipt_sha256')),'Natural complete response closure required before I/O'
 stem='CROSS_U_INITIAL_YORK_TRACE_TARGET_RATE_RESPONSE_V001';source='cross_u_initial_york_trace_target_rate_response_v001.py'
 sh='23cbba6893b934236c8fff2c8ff4dda63f6808f589a04f701dcd536fdd31de27';ph='793cc56c47dabc8a7baa7838b57fd95b658d655242a71e112d0d64b932ba44f7'
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',t['result_sha256']),(stem+'_RECEIPT.json',t['receipt_sha256'])):bind(n,h)
 r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==t['result_sha256'] and r['owner']==rc['owner'] and r['owner']['pid']==t['pid'] and r['owner']['source_sha256']==sh
 assert r['status'] in ('NEW_LITERAL_TRACE_TARGET_RESPONSE_ADMITTED','NEW_LITERAL_TRACE_TARGET_RESPONSE_NOT_ADMITTED') and r['literal_original_response_admitted']==(r['status']=='NEW_LITERAL_TRACE_TARGET_RESPONSE_ADMITTED')
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and r['physical_adoption'] is False and r['whole_grid_five_field_preparation'] is False and r['original_primitive_stationarity_mismatch_resolved'] is False
 assert len(r['controls'])==3 and [q['ordinal'] for q in r['controls']]==[0,1,2] and all(q['passed'] and q['tolerance']==2e-11 for q in r['controls'])
 def thin(q):return {k:q[k] for k in ('file','sha256','commit_file','commit_sha256')}
 def selected(q,output):
  m=rc['output_sha256'] if output else rc['input_sha256']
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert m[n if output else str(P.path(n).resolve())]==h;bind(n,h)
  a=json.loads(P.path(q['commit_file']).read_text());assert a['file']==q['file'] and a['sha256']==q['sha256'] and (q.get('metadata') is None or q['metadata']==a['metadata'])
  out=dict(a,commit_file=q['commit_file'],commit_sha256=q['commit_sha256']);md=out['metadata'];assert md['failed'] is False and all(v['finite'] for v in md['schema'].values())
  if output:assert out in r['checkpoints'] and md['owner']==r['owner'] and md['qualification']==r['qualification']
  return out
 def schema(q,n,shape,dtype='float64'):assert q['metadata']['schema'][n]==dict(shape=list(shape),dtype=dtype,finite=True),(q['file'],n)
 inp=selected(r['input'],True);cols=[selected(q,True) for q in r['columns']];ro=selected(r['readout'],True);approx=selected(r['numerical_approximation'],True);jets=selected(r['rate_jets'],True)
 im=inp['metadata'];assert im['kind']=='NEW_compact_total_trace_target_RHS_and_immutable_numerical_preconditioner' and im['configuration_unchanged'] and im['cap']==160 and im['cycles']==1 and im['zero_source_relative_ratio'] is None
 assert len(cols)==4 and [q['metadata']['column'] for q in cols]==[0,1,2,3] and ro['metadata']['columns']==[thin(q) for q in cols] and ro['metadata']['rate_jets']==thin(jets)
 assert ro['metadata']['literal_original_response_admitted']==r['literal_original_response_admitted'] and ro['metadata']['literal_original_reference_scores']==r['literal_original_scores'] and r['zero_native_RHS_relative_ratio'] is None
 pilots=[selected(q,False) for q in im['pilot_columns']];prior=selected(im['prior_signed_primitive_readout'],False)
 assert len(pilots)==4 and [q['metadata']['owner']['pid'] for q in pilots]==[50104]*4 and [q['metadata']['column'] for q in pilots]==[0,1,2,3] and [q['metadata']['pilot_ref'] for q in cols]==[thin(q) for q in pilots]
 assert prior['metadata']['owner']['pid']==50104 and prior['metadata']['offsets_targets_or_state_refitted'] is False and thin(prior)==ro['metadata']['prior_signed_primitive_readout']
 for n,shape,dtype in (('R',(4,3784),'float64'),('dv',(4,3784),'float64'),('hats',(4,4,3,86,44),'float64'),('cell_i',(3784,),'int64'),('cell_j',(3784,),'int64'),('r',(87,),'float64'),('z',(45,),'float64')):schema(inp,'original_basis_'+n,shape,dtype)
 assert jets['metadata']['basis_ref']==im['frozen_system_refs']['basis'] and jets['metadata']['frozen_operator_ref']==im['frozen_system_refs']
 first=dict(du=(3784,4,4),dz=(32,3784,4,4),dg=(3784,4,4,4),Ga=(3784,4,4,4))
 feature=dict(du=(3784,4,4),dz=(32,3784,4,4),Ga=(3784,4,4,4),nu=(3784,4,4),nz=(32,3784,4,4),q=(32,3784,4),V=(32,3784,4),D=(32,3784,4,4),lower_nu=(3784,4,4),F=(3784,4,4),Fup=(3784,4,4),a=(3784,4),V_raised=(32,3784,4),D_raised=(32,3784,4,4),Pi=(32,3784,4,4),PiU=(3784,4,4))
 moments=dict(connection_Klo=(3784,4,4,4),connection_raised_Klo=(3784,4,4,4),connection_D=(3784,4,4,4),connection_Maxwell=(3784,4,4,4),connection_momentum=(3784,4,4,4),native_density=(3784,99),metric_native_density=(3784,6),K=(3784,3,3),Ktrace=(3784,),metric_EH_tensor=(3784,3,3),metric_EH_density=(3784,6),metric_total_density=(3784,6))
 for q in cols:
  md=q['metadata'];assert md['kind']=='NEW_literal_complete_and_uncancelled_block_temporal_derivatives' and md['configuration_unchanged'] and md['affine_constant_derivative_zero'] and md['original_primitive_mismatch_resolved'] is False
  for prefix,fields in (('NEW_rate_first_jet_',first),('NEW_rate_feature_',feature),('NEW_rate_momentum_',moments)):
   for n,shape in fields.items():
    for w in ('hi','lo'):schema(q,prefix+n+'_'+w,shape)
  for n,shape in (('NEW_local_native_rate_values',(3784,99)),('NEW_local_physical_metric_rate_values',(3784,6))):
   for w in ('hi','lo'):schema(q,n+'_'+w,shape)
 qualification=dict(status=r['status'],literal_original_response_admitted=r['literal_original_response_admitted'],literal_original_scores=r['literal_original_scores'],frozen_numerical_inverse_admitted=r['old_frozen_inverse_numerically_admitted'],implementation_test_operands_only=True,canonical_or_Jacobian_direction_adopted=False,zero_native_RHS_relative_ratio=None)
 gaps=dict(primitive_legendre=thin(prior),frozen_rate_certificate=thin(approx),owned_vs_reconstructed_jets=[thin(q) for q in pilots],metric_compatibility=[thin(q) for q in pilots],registered_vs_literal_normal=None,primary_gauge=[thin(q) for q in pilots],physical_ports=None)
 return dict(P.INPUTS),dict(input=inp,rate_columns=cols,pilot_columns=pilots,prior_primitive_readout=prior,source_qualification=qualification,fixed=im['fixed'],bg=im['owned_background'],gap_refs=gaps)
