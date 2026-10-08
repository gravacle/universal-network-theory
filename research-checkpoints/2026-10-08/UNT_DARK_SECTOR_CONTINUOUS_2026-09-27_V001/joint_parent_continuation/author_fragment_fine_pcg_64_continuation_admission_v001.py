# Definitions only. Globals bind/json/P.path. Proof must pass before any payload load.
def fine_pcg_64_continuation_admission():
 stem='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V007';source='cross_u_compact_york_longitudinal_projection_v007.py'
 sh='25a96063c97b691440401a2b32f6b1b93919f3211d9d5f3747fd67d0a93d038b';ph='97e1277e87e41fcd9c93c00754eae08d645948b906e8aa80a99cc61919845266'
 rh='578759e107965e270912ebad70d3fc81511d14433da000ccbbd475ec40e49156';ch='131c1305ec5972901e67210064040da4c362ffba6337a8a37d943cb9c46f8166'
 pn='READONLY_FINE_PCG_YORK_PROJECTION_CLOSURE_V002_RESULT.json';ps='fba4af99b57959a4e136b21b6738c03a8f185a7ec0898822192af9ad9f8bd0b8'
 bind(pn,ps);proof=json.loads(P.path(pn).read_text());terminal=dict(pid=76118,result_sha256=rh,receipt_sha256=ch,error_sha256=None)
 assert proof['status']=='SAVED_CACHED_FINE_PCG_YORK_CLOSURE_PASS' and proof['parent']==terminal and proof['controls']==4 and proof['committed_pairs']==8 and proof['iterations']==512 and proof['actual_node_update_earned'] is True and proof['original_rows_admitted'] is False and proof['physical_adoption'] is False
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',rh),(stem+'_RECEIPT.json',ch)):bind(n,h)
 r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==rh and rc.get('error_sha256') is None and r['owner']==rc['owner'] and r['owner']['pid']==76118 and r['owner']['source_sha256']==sh
 assert r['status']=='ORIGINAL_YORK_ROWS_NOT_ADMITTED' and r['cap']==512 and r['projection'] is None and r['original_rows_admitted'] is False and r['compact_weak_TT_original_rows_admitted'] is False and r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values())
 assert r['automatic_restart'] is False and r['all_full_coupled_map_entries_retained'] is True and r['vector_space_dimension']==11135 and r['coarse_dimension']==2730 and len(r['checkpoints'])==8 and len(r['controls'])==4 and all(c['ordinal']==i and c['passed'] and c['tolerance']==2e-11 for i,c in enumerate(r['controls']))
 def selected(q):
  assert q in r['checkpoints']
  for n,k in ((q['file'],'sha256'),(q['commit_file'],'commit_sha256')):assert rc['output_sha256'][n]==q[k];bind(n,q[k])
  cm=json.loads(P.path(q['commit_file']).read_text());assert cm=={n:q[n] for n in ('file','sha256','metadata')} and cm['metadata']['owner']==r['owner'] and cm['metadata']['qualification']==r['qualification'] and cm['metadata']['failed'] is False
  return dict(cm,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 inp=selected(r['input']);sol=selected(r['solution']);md=sol['metadata'];assert md['input_ref']=={n:inp[n] for n in ('file','sha256','commit_file','commit_sha256')} and md['solver']['cap']==md['solver']['iterations']==512 and md['solver']['reason']=='iteration_cap' and md['solver']['recursive_residual_replaced'] is False and md['solver']['automatic_restart'] is False and md['original_component_ratios']==proof['original_component_ratios']
 def schema(q,n,shape,dtype='float64'):assert q['metadata']['schema'][n]==dict(shape=list(shape),dtype=dtype,finite=True),(q['file'],n)
 for n in ('final_potential_nodes','final_original_action','final_original_residual','original_rhs','fine_york_PCG_current_nodes','fine_york_PCG_recursive_residual','fine_york_PCG_new_recursive_residual','fine_york_PCG_preconditioned_residual','fine_york_PCG_search_direction','fine_york_PCG_previous_search_direction','fine_york_PCG_previous_Ap','fine_york_PCG_Ap','fine_york_PCG_fresh_original_residual'):
  for w in ('hi','lo'):schema(sol,n+'_'+w,(11135,))
 for n in ('fine_york_PCG_rz','fine_york_PCG_current_rz_paired_inner_product'):
  for w in ('hi','lo'):schema(sol,n+'_'+w,())
 for n in ('fine_york_PCG_current_rz_inner_binary64_readout','fine_york_PCG_beta'):schema(sol,n,())
 schema(sol,'fine_york_PCG_iterations_completed',(),'int64');schema(sol,'fine_york_PCG_direction_action_positive_positive_scatter',(3,87,45));schema(sol,'fine_york_PCG_fresh_original_original_residual_operation_envelope',(11135,));schema(sol,'final_original_raw_scaled_ratios',(3,2));schema(sol,'final_original_global_ratios',(2,));schema(sol,'original_positive_scale',(11135,))
 for n,shape in (('L_maps_hi',(15136,3,3,3,3)),('L_maps_lo',(15136,3,3,3,3)),('L_map_operation_envelope',(15136,3,3,3,3)),('ih',(15136,3,3)),('sqrt_h',(15136,)),('PiTF_hi',(15136,3,3)),('PiTF_lo',(15136,3,3)),('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44)),('r',(87,)),('z',(45,)),('rhs_hi',(3,87,45)),('rhs_lo',(3,87,45)),('rhs_operation_envelope',(3,87,45)),('positive_Jacobi_congruence_scale',(3,87,45))):schema(inp,n,shape)
 for n in ('cell_i','cell_j'):schema(inp,n,(3784,),'int64')
 schema(inp,'compact_vector_mask',(3,87,45),'bool')
 for n,shape,dtype in (('fine_to_coarse_i',(87,),'int64'),('fine_to_coarse_j',(45,),'int64'),('physical_node_interpolation_weights',(4,87,45),'float64'),('coarse_hat_values_at_fine_cell_corners',(4,4,3784),'float64'),('coarse_global_local_indices',(3784,12),'int64'),('coarse_mask',(3,44,23),'bool'),('coarse_positive_scale',(2730,),'float64'),('normalized_coarse_Cholesky',(2730,2730),'float64')):schema(inp,'continued_coarse_new_coarse_'+n,shape,dtype)
 return dict(input=inp,solution=sol,terminal=terminal,proof=dict(file=pn,sha256=ps,status=proof['status']),original_controls=r['controls'],original_checkpoints=[{n:q[n] for n in ('file','sha256','commit_file','commit_sha256')} for q in r['checkpoints']],prior_solver=md['solver'],source_qualification=r['qualification'],additional_cap=64,prior_512_nonadmission_preserved=True,automatic_extension=False)
