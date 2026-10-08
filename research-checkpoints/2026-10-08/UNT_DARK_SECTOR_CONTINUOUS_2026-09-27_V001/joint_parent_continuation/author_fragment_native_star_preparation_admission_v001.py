"""Definitions only; globals bind/json/P.path. Authentic preparation owner28469.
Saved lumped native star only; neither a fine diagonal nor a global Schur claim.
No old preparation, coefficient, geometry or numeric helper is evaluated here.
"""
def native_star_preparation_admission():
 stem='CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001';source='cross_u_weak_nodal_native_legendre_v001.py'
 sh='e7b06d179d89b69c6136964266825c36b77425292f723fa65c134efa254cbe70';ph='2c9da869068cf3d2ae9269395b111ec1d0e71f26e0ffef6ff0afb50e40995a0e'
 rh='e5a8f065a865245a430a2b23fe1c69a20ae2dd542071e5804a216f2f604f8fe5';ch='00478e51c5ae07c31707ca8ec548bef193d33b2f76dc4b09361efd6e281727ae'
 proofn='READONLY_CROSS_U_WEAK_NODAL_NATIVE_LEGENDRE_V001_SAVED_AUDIT.json';proofh='af16bda38df395882c54ca2b57bd7d9ed36cc3aae39b437687bc35930423d56d'
 for n,h in ((source,sh),(stem+'.md',ph),(stem+'_RESULT.json',rh),(stem+'_RECEIPT.json',ch),(proofn,proofh)):bind(n,h)
 r=json.loads(P.path(stem+'_RESULT.json').read_text());rc=json.loads(P.path(stem+'_RECEIPT.json').read_text());proof=json.loads(P.path(proofn).read_text())
 assert rc['status']=='CLOSED' and rc['result_sha256']==rh and rc.get('error_sha256') is None and r['owner']==rc['owner'] and r['owner']['pid']==28469 and r['owner']['source_sha256']==sh
 assert r['status']=='CONDITIONAL_WEAK_NATIVE_LEGENDRE_ARITHMETIC_PASS' and len(r['cases'])==1 and r['cases'][0]['sigma']==1. and r['cases'][0]['status']=='CONDITIONAL_WEAK_NATIVE_LEGENDRE_PASS'
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and len(r['checkpoints'])==10 and len(r['controls'])==21 and all(c['passed'] for c in r['controls'])
 assert proof['status']=='SAVED_PACKET_AUDIT_PASS' and proof['pair_count']==10 and proof['control_count']==21 and proof['terminal']['owner_pid']==28469 and proof['terminal']['source_sha256']==sh and proof['terminal']['protocol_sha256']==ph and proof['terminal']['result_sha256']==rh and proof['terminal']['receipt_sha256']==ch and proof['terminal']['error_sha256'] is None
 def one(kind):
  hits=[q for q in r['checkpoints'] if q['metadata']['kind']==kind];assert len(hits)==1;q=hits[0]
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
  a=json.loads(P.path(q['commit_file']).read_text());assert a=={n:q[n] for n in ('file','sha256','metadata')} and a['metadata']['owner']==r['owner'] and a['metadata']['qualification']==r['qualification'] and a['metadata']['failed'] is False
  return dict(a,commit_file=q['commit_file'],commit_sha256=q['commit_sha256'])
 prep=one('preconditioner_only_positive_node_block');coeff=one('complete_fixed_metric_native99_mass_coefficients');geo=one('genuine_affine_native_temporal_basis')
 assert prep['metadata']['actual_operator_mass_lumped'] is False and prep['metadata']['actual_operator_Maxwell_substitution'] is False and coeff['metadata']['sigma']==1. and geo['metadata']['independent_native_coefficients']==380292 and geo['metadata']['nodes']==[87,45] and geo['metadata']['covector_phi']=='R² times even scalar coefficient'
 def schema(q,n,shape,dtype='float64'):assert q['metadata']['schema'][n]==dict(shape=list(shape),dtype=dtype,finite=True),(q['file'],n)
 for n,shape in (('preconditioner_D',(32,3915,3,3)),('preconditioner_B',(32,3915,3,3)),('preconditioner_Maxwell',(3915,3,3)),('preconditioner_basis_scale',(3915,3)),('kinetic_congruence_scale',(33,3,87,45))):schema(prep,n,shape)
 for n,shape in (('mixing_L',(32,15136,3,3)),('modal_D',(32,15136,3,3)),('Maxwell_M0',(15136,3,3))):schema(coeff,n,shape)
 for n,shape in (('geometry_R',(4,3784)),('geometry_dv',(4,3784)),('geometry_hats',(4,4,3,86,44))):schema(geo,n,shape)
 for n in ('geometry_cell_i','geometry_cell_j'):schema(geo,n,(3784,),'int64')
 schema(geo,'native_independent_mask',(3,87,45),'bool')
 cn='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_00007_BASIS.npz.COMMIT.json';cs='36d13345fc78b0afbad152f3f6e03ff381eaa8915b0b84cc4e2c333e00599c11';bind(cn,cs)
 current=json.loads(P.path(cn).read_text());assert current['file']=='CROSS_U_CANONICAL_NODAL_METRIC_RATE_SOLVE_V001_00007_BASIS.npz' and current['sha256']=='28bb1ba976b88bfa6b96a7d614524f5760faa79a111da8f75fcaacc7ca95f93f' and current['metadata']['owner']['pid']==39611 and current['metadata']['kind']=='unchanged_E_F_S_bases_and_positive_solver_congruences' and current['metadata']['native_dofs']==380292 and current['metadata']['axis_reflection'] is True
 bs='f84b8a9bea9d45ac1370985401172621d93d59dc814bedda785206188b3c2c4b';bind('cross_u_canonical_nodal_metric_rate_solve_v001.py',bs);assert current['metadata']['owner']['source_sha256']==bs
 for n,shape in (('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44)),('native_scale',(33,3,87,45)),('r',(87,)),('z',(45,))):schema(current,n,shape)
 basis=dict(record=geo,current_basis_metadata=dict(current,commit_file=cn,commit_sha256=cs),mask_field='native_independent_mask',scale_record=prep,scale_field='preconditioner_basis_scale',normscale_field='kinetic_congruence_scale',native_covector_phi='R^2 times even scalar coefficient',scale_convention='(1,1,r_node^2), dummy axis phi=1; mask axis all components and Z at sheet',same_grid_provenance='authenticated 39611 source copies this geometry and kinetic_congruence_scale, checks native_mask, then publishes unchanged BASIS',native_star_convention='B is U<-mode; Ublock=Maxwell+sum(B D^-1 B^T); original-coordinate local surrogate=Sbasis Hstar Sbasis',local_star_is_older_lumped_surrogate=True,current_physical_coefficient_identity_claimed=False,exact_fine_diagonal_or_global_Schur_claimed=False,current_basis_payload_loaded=False)
 return dict(preparation=prep,coefficient=coeff,geometry=geo,basis_source=basis,terminal=dict(pid=28469,source_sha256=sh,protocol_sha256=ph,result_sha256=rh,receipt_sha256=ch,error_sha256=None),proof=dict(file=proofn,sha256=proofh,status=proof['status']),source_qualification=r['qualification'],physical_adoption=False)
