"""HELD represented gauge-port fullweak transpose and negative feedback.
Globals np,P,N, reviewed ct_pair/ct_matvec/candidate_original_scatter_transpose,
fy_sum and the separate outward companion. No current, port, action, EOS,
adjoint solve, old fixture or producer runs. C=S_current Cpoint T_normal;
S* already includes original rounded dv/R, hence T_normal* is unweighted.
"""
GAUGE_TRANSPOSE_AUTHOR_DRAFT=True
GAUGE_TRANSPOSE_AUTHORING_IN_PROGRESS=False
GAUGE_TRANSPOSE_SOURCE=(None,None)
GAUGE_TRANSPOSE_RESULT=(None,None,None)
GAUGE_TRANSPOSE_RECEIPT=(None,None,'CLOSED')
GAUGE_TRANSPOSE_PROOF=(None,None,None)
GAUGE_MECHANICAL_ADJOINT_SOURCE=(None,None)
GAUGE_MECHANICAL_ADJOINT_RESULT=(None,None,None)
GAUGE_MECHANICAL_ADJOINT_RECEIPT=(None,None,'CLOSED')
GAUGE_MECHANICAL_ADJOINT_PROOF=(None,None,None)
GAUGE_PHASE_ADJOINT_SOURCE=(None,None)
GAUGE_PHASE_ADJOINT_RESULT=(None,None,None)
GAUGE_PHASE_ADJOINT_RECEIPT=(None,None,'CLOSED')
GAUGE_PHASE_ADJOINT_PROOF=(None,None,None)


def prepare_candidate_gauge_fullweak_transpose(columns,basis,closed,keep,label):
 assert not GAUGE_TRANSPOSE_AUTHOR_DRAFT and not GAUGE_TRANSPOSE_AUTHORING_IN_PROGRESS
 refs=(GAUGE_TRANSPOSE_SOURCE,GAUGE_TRANSPOSE_RESULT,GAUGE_TRANSPOSE_RECEIPT,GAUGE_TRANSPOSE_PROOF)
 assert all(x is not None for ref in refs for x in ref),'Authentic natural gauge closure required before any reader call'
 assert [closed[n] for n in ('source','result','receipt','proof')]==list(refs)
 assert closed['naturally_closed'] is True and closed['natural_exit_code']==0 and closed['all_selected_seals_verified'] is True
 assert closed['physical_adoption'] is False and closed['same_candidate_provenance'] and len(columns)==4
 assert closed['original_current_targets_unchanged'] is closed['gauge_target_derivative_zero'] is closed['same_updated_phase_and_mechanical_candidate'] is True
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and basis['closed_provenance']
 for iq,q in enumerate(columns):
  assert q['column']==iq and q['gauge_row_order']==('N','beta_R','beta_Z','beta_phi') and q['gauge_coordinate_order']==('value','R','Z','t')
  assert q['all16_gauge_ports_earned'] is True and q['gauge_target_derivative_zero'] is True and q['record'] and q['test_refs'] and len(q['test_refs'])==16
  assert q['same_candidate_provenance']==closed['same_candidate_provenance'][iq] and q['basis_provenance']==basis['closed_provenance']
 copy={n:np.asarray(basis[n]).copy() for n in ('R','dv','hats')}
 for n,a in copy.items():keep(label+'_copied_original_basis_'+n,a.copy());assert a.dtype==np.float64 and np.all(np.isfinite(a))
 assert np.all(copy['R']>0) and np.all(copy['dv']>0)
 weight=keep(label+'_original_rounded_weight64',(copy['dv']/copy['R']).reshape(15136));assert np.all(weight>0)
 return dict(columns=list(columns),basis=copy,weight=weight,closed=closed,same_candidate_provenance=closed['same_candidate_provenance'],gauge_target_derivative_zero=True,physical_adoption=False,coefficient_transpose_only=True,arbitrary286_association_qualified=False)


def candidate_gauge_scalar_scatter_transpose(dual,basis,keep,label):
 assert dual[0].shape==dual[1].shape==(3870,);ct_pair(label+'_supplied_scalar_dual',dual,keep)
 mask=P.scalar_mask();nodes=P.a_dd(np.zeros((87,45)))
 for w in (0,1):nodes[w][mask]=dual[w]
 lift=ct_pair(label+'_original_scalar_axis_lift',tuple(P.scalar_lift(a) for a in nodes),keep);out=P.a_dd(np.zeros((4,86,44)))
 for iq in range(4):
  weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   value=P.a_slice(lift,(slice(di,86+di),slice(dj,44+dj)));hat=basis['hats'][iq,corner,0]
   term=ct_pair(label+'_original_hat_product',P.a_mul64(hat,value),keep);term=ct_pair(label+'_original_weight_product',P.a_mul64(weight,term),keep)
   update=P.a_add(P.a_slice(out,iq),term)
   for w in (0,1):out[w][iq]=update[w]
   ct_pair(label+'_point_partial',out,keep)
 return ct_pair(label+'_scalar_point_weighted',P.a_reshape(out,(15136,)),keep)


def candidate_gauge_point_coefficient_transpose(block,dual,group,keep,label):
 assert group in ('mechanical','phase');p=block['paired']['phase'][0].shape[0]
 shapes=dict(native=(p,99,4,4),metric=(p,6,4,4),phase=(p,4,4))
 for n,shape in shapes.items():assert block['paired'][n][0].shape==block['paired'][n][1].shape==shape;ct_pair(label+'_copied_Cpoint_'+n,block['paired'][n],keep)
 if group=='mechanical':
  out=P.a_dd(np.zeros((p,16)))
  for n,width in (('native',99),('metric',6)):
   assert dual[n][0].shape==dual[n][1].shape==(p,width)
   matrix=tuple(a.reshape(p,width,16).swapaxes(1,2) for a in block['paired'][n])
   out=ct_pair(label+'_'+n+'_port_partial',P.a_add(out,ct_matvec(matrix,dual[n],keep,label+'_'+n+'_coefficient_star')),keep)
  return ct_pair(label+'_weighted_gauge_ports',P.a_reshape(out,(p,4,4)),keep)
 assert dual['phase'][0].shape==dual['phase'][1].shape==(p,)
 return ct_pair(label+'_weighted_gauge_ports',P.a_mul(block['paired']['phase'],tuple(a[:,None,None] for a in dual['phase'])),keep)


def candidate_gauge_normal_registration_transpose(ports,basis,keep,label):
 assert ports[0].shape==ports[1].shape==(15136,4,4);ct_pair(label+'_already_weighted_point_ports',ports,keep)
 out=P.a_dd(np.zeros((4,87,45)))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    value=P.a_dd(np.zeros((86,44)))
    for jet,hat in enumerate(N.normal_hat_jet(basis,iq,corner,row)):
     keep(label+'_literal_registered_hat',np.asarray(hat).copy());selected=hat!=0;field=P.a_reshape(P.a_slice(ports,(sl,row,jet)),(86,44));term=P.a_dd(np.zeros((86,44)))
     for w,a in enumerate(P.a_mul64(hat[selected],tuple(x[selected] for x in field))):term[w][selected]=a
     value=ct_pair(label+'_unweighted_corner_value',P.a_add(value,term),keep)
    key=(row,slice(di,86+di),slice(dj,44+dj));update=P.a_add(P.a_slice(out,key),value)
    for w in (0,1):out[w][key]=update[w]
    ct_pair(label+'_normal_corner_partial',out,keep)
 out=ct_pair(label+'_original_normal_axis_boundary_restriction',N.paired_restrict_normal_rows(out),keep)
 return dict(weak_normal=out,time_coefficient_point=ct_pair(label+'_weighted_time_primary_covector',P.a_slice(ports,(slice(None),slice(None),3)),keep),point_coefficients_weighted=ports,
             original_normal_order=('N','beta_R','beta_Z','beta_phi'),original_jet_order=('value','R','Z','t'),spatial_weight_count=1,time_covector_contains_original_weight=True,raw_time_density_not_substituted=True)


def candidate_gauge_fullweak_transpose(prepared,dual,group,read_closed_column,keep,label,column_complete=None):
 assert group in ('mechanical','phase') and callable(read_closed_column) and prepared['coefficient_transpose_only'] is True
 if group=='mechanical':
  n,m=candidate_original_scatter_transpose(dual,prepared['basis'],keep,label+'_original_Sstar')
  point=dict(native=tuple(a.transpose(1,0,2).reshape(15136,99) for a in n),metric=m)
 else:point=dict(phase=candidate_gauge_scalar_scatter_transpose(dual,prepared['basis'],keep,label+'_original_scalar_Sstar'))
 ports=P.a_dd(np.zeros((15136,4,4)));completed=[]
 for descriptor in prepared['columns']:
  iq=descriptor['column'];sl=slice(iq*3784,(iq+1)*3784);block=read_closed_column(descriptor,('native','metric','phase'))
  assert block['record']==descriptor['record'] and block['source_provenance']==descriptor['same_candidate_provenance']
  local={n:P.a_slice(a,sl) for n,a in point.items()};part=candidate_gauge_point_coefficient_transpose(block,local,group,keep,label+'_column%d_Cpointstar'%iq)
  for w in (0,1):ports[w][sl]=part[w]
  ct_pair(label+'_completed_weighted_port_prefix',ports,keep)
  if column_complete is not None:completed.append(column_complete(descriptor,part))
 result=candidate_gauge_normal_registration_transpose(ports,prepared['basis'],keep,label+'_original_Tstar')
 return dict(**result,column_refs=completed,same_candidate_provenance=prepared['same_candidate_provenance'],gauge_target_derivative_zero=True,group=group,coefficient_transpose_only=True,arbitrary286_association_qualified=False,C_equals_minus_Rv_or_Schwarz_assumed=False,physical_adoption=False)


def candidate_gauge_negative_feedback(prepared,lambda_mechanical,lambda_phase,adjoints,read_closed_column,keep,label,column_complete=None):
 for group,stem,dual in (('mechanical','GAUGE_MECHANICAL_ADJOINT_',lambda_mechanical),('phase','GAUGE_PHASE_ADJOINT_',lambda_phase)):
  refs=tuple(globals()[stem+n] for n in ('SOURCE','RESULT','RECEIPT','PROOF'));assert all(x is not None for ref in refs for x in ref)
  proof=adjoints[group];assert [proof[n] for n in ('source','result','receipt','proof')]==list(refs) and proof['naturally_closed'] is True and proof['all_selected_seals_verified'] is True
  assert proof['same_candidate_provenance']==prepared['same_candidate_provenance'] and proof['stationarity_rhs']=='e_L_target_minus_literal' and proof['canonical_epsilon_not_substituted'] is True
  assert proof['adjoint_equation']==('Astar_lambda=e_L' if group=='mechanical' else 'Mstar_lambda=e_L')
  ct_pair(label+'_copied_'+group+'_adjoint',dual,keep)
 mechanical=candidate_gauge_fullweak_transpose(prepared,lambda_mechanical,'mechanical',read_closed_column,keep,label+'_mechanical_Cstar',column_complete)
 ct_pair(label+'_completed_mechanical_weak_before_phase',mechanical['weak_normal'],keep);ct_pair(label+'_completed_mechanical_weighted_time_before_phase',mechanical['time_coefficient_point'],keep)
 phase=candidate_gauge_fullweak_transpose(prepared,lambda_phase,'phase',read_closed_column,keep,label+'_phase_Cstar',column_complete)
 weak=ct_pair(label+'_negative_gauge_feedback',P.a_mul64(-1.,P.a_add(mechanical['weak_normal'],phase['weak_normal'])),keep)
 time=ct_pair(label+'_negative_weighted_time_primary_feedback',P.a_mul64(-1.,P.a_add(mechanical['time_coefficient_point'],phase['time_coefficient_point'])),keep)
 return dict(weak_normal=weak,time_coefficient_point=time,mechanical=mechanical,phase=phase,adjoint_provenance=adjoints,feedback_sign='minus Cmechanical_star lambda_m minus Cphase_star lambda_p',
             baseline_scope='current registered-canonical graph feedback diagnostic; canonical graph and inverse accuracy remain external',epsilon_and_e_L_distinct=True,exact_reduced_Newton=False,second_directional_A_M_C_eL_terms_earned=False,
             time_covector_contains_original_weight=True,original_unweighted_time_density_unchanged=True,CMC_feedback_added=False,CMC_rate_response_remains_separate=True,physical_adoption=False)


def candidate_gauge_registered_test_jets(normal_probe,temporal_probe,basis,keep,label):
 assert normal_probe[0].shape==normal_probe[1].shape==temporal_probe[0].shape==temporal_probe[1].shape==(4,87,45)
 mask=N.normal_test_mask()
 for name,pair in (('normal',normal_probe),('temporal',temporal_probe)):
  ct_pair(label+'_NEW_'+name+'_test_coefficients',pair,keep);assert all(np.all(a[~mask]==0) for a in pair)
 spatial=tuple(N.extend_normal_tests(a) for a in normal_probe);temporal=tuple(N.extend_normal_tests(a) for a in temporal_probe);out=P.a_dd(np.zeros((15136,4,4)))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    hats=N.normal_hat_jet(basis,iq,corner,row)
    for jet in range(4):
     nodes=temporal if jet==3 else spatial;hat=hats[0] if jet==3 else hats[jet]
     node=tuple(a[row,di:86+di,dj:44+dj] for a in nodes);term=P.a_reshape(P.a_mul64(hat,node),(3784,));update=P.a_add(P.a_slice(out,(sl,row,jet)),term)
     for w in (0,1):out[w][sl,row,jet]=update[w]
     ct_pair(label+'_separate_registered_polynomial_partial',out,keep)
 return dict(physical_gauge_jets=out,physical_time_probe=ct_pair(label+'_physical_time_probe',P.a_slice(out,(slice(None),slice(None),3)),keep),
             temporal_test_basis_only=True,physical_gauge_time_ports_admitted=False,spatial_and_time_beta_R_factor_exact_original_Rhat=True)


def candidate_gauge_new_port_forward(prepared,test_jets,group,read_closed_column,keep,label,column_complete=None):
 assert group in ('mechanical','phase') and test_jets['temporal_test_basis_only'] is True
 jets=test_jets['physical_gauge_jets'];assert jets[0].shape==jets[1].shape==(15136,4,4)
 families=('native','metric') if group=='mechanical' else ('phase',);widths=dict(native=99,metric=6,phase=None)
 point={n:P.a_dd(np.zeros((15136,) if widths[n] is None else (15136,widths[n]))) for n in families};completed=[]
 for descriptor in prepared['columns']:
  iq=descriptor['column'];sl=slice(iq*3784,(iq+1)*3784);block=read_closed_column(descriptor,('native','metric','phase'))
  assert block['record']==descriptor['record'] and block['source_provenance']==descriptor['same_candidate_provenance']
  for row in range(4):
   for jet in range(4):
    value=P.a_slice(jets,(sl,row,jet))
    for n in families:
     coefficient=P.a_slice(block['paired'][n],(slice(None),row,jet) if n=='phase' else (slice(None),slice(None),row,jet));multiplier=value if n=='phase' else tuple(a[:,None] for a in value)
     update=P.a_add(P.a_slice(point[n],sl),P.a_mul(coefficient,multiplier))
     for w in (0,1):point[n][w][sl]=update[w]
     ct_pair(label+'_'+n+'_separate_forward_point_prefix',point[n],keep)
  if column_complete is not None:completed.append(column_complete(descriptor,{n:P.a_slice(a,sl) for n,a in point.items()}))
 if group=='mechanical':
  modes=tuple(a.reshape(15136,33,3).transpose(1,0,2) for a in point['native']);native=ct_pair(label+'_original_native_S',P.dd_native_scatter(modes,prepared['basis'],keep),keep);metric=ct_pair(label+'_original_metric_S',P.dd_metric_scatter(point['metric'],prepared['basis'],keep),keep);packed=ct_pair(label+'_packed',P.pack_dd(native,metric),keep)
 else:
  scalar=ct_pair(label+'_original_scalar_S',P.dd_scalar_scatter(point['phase'],prepared['basis'],keep,label),keep);packed=ct_pair(label+'_packed',tuple(a[P.scalar_mask()].copy() for a in scalar),keep)
 return dict(packed=packed,point=point,column_refs=completed,forward_scope='NEW_represented_port_forward',same_candidate_provenance=prepared['same_candidate_provenance'],new_registered_gauge_direction=True,
             old_current_port_action_or_fixture_replayed=False,arbitrary286_association_qualified=False,physical_adoption=False)


def gauge_transpose_pair_dot(a,b,keep,label):
 assert a[0].shape==a[1].shape==b[0].shape==b[1].shape
 terms=ct_pair(label+'_coefficient_products',P.a_mul(tuple(x.reshape(-1) for x in a),tuple(x.reshape(-1) for x in b)),keep)
 while len(terms[0])>1:
  n=len(terms[0]);m=n-n%2;out=P.a_add(tuple(x[:m:2] for x in terms),tuple(x[1:m:2] for x in terms))
  if n%2:out=tuple(np.concatenate((out[w],terms[w][-1:])) for w in (0,1))
  terms=ct_pair(label+'_tree_partial',out,keep)
 return ct_pair(label+'_scalar',tuple(np.asarray(x[0]).copy() for x in terms),keep)


def candidate_gauge_transpose_pairing_contact(normal_probe,time_probe,dual,new_forward,transpose,forward_bound,transpose_bound,provenance,keep,check,label):
 assert provenance['genuinely_NEW_registered_gauge_direction'] is True and provenance['old_current_port_action_or_fixture_replayed'] is False
 assert provenance['same_candidate_provenance']==transpose['same_candidate_provenance'] and provenance['forward_scope'] in ('NEW_represented_port_forward','NEW_authoritative286_direction')
 left=gauge_transpose_pair_dot(dual,new_forward,keep,label+'_dual_forward')
 spatial=gauge_transpose_pair_dot(normal_probe,transpose['weak_normal'],keep,label+'_normal_transpose');time=gauge_transpose_pair_dot(time_probe,transpose['time_coefficient_point'],keep,label+'_time_transpose')
 right=ct_pair(label+'_spatial_plus_time_pairing',P.a_add(spatial,time),keep);gap=ct_pair(label+'_source_and_transpose_pairing_gap',P.a_sub(left,right),keep)
 mag=lambda x:mp_add(abs(x[0]),abs(x[1]),keep,label+'_magnitude');total=lambda x:mp_sum(x.reshape(-1),0,keep,label+'_sum')
 for n,a,shape in (('NEW_forward_operation_bound',forward_bound,dual[0].shape),('transpose_weak_bound',transpose_bound['weak_normal'],(4,87,45)),('transpose_weighted_time_bound',transpose_bound['time_coefficient_point'],(15136,4))):keep(label+'_'+n,np.asarray(a).copy());assert a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) and np.all(a>=0)
 bound=np.asarray(mp_add(total(mp_mul(mag(dual),forward_bound,keep,label+'_left_bound')),mp_add(total(mp_mul(mag(normal_probe),transpose_bound['weak_normal'],keep,label+'_spatial_bound')),total(mp_mul(mag(time_probe),transpose_bound['time_coefficient_point'],keep,label+'_time_bound')),keep,label+'_right_bound'),keep,label+'_uncancelled_bound')).copy()
 keep(label+'_uncancelled_bound',bound)
 if bound==0:assert all(np.all(x==0) for x in gap),'Exact both-word zero with zero construction envelope'
 check(label,np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),bound)
 return dict(gap=gap,bound=bound,forward_scope=provenance['forward_scope'],single_NEW_pairing_only=True,uniform_adjoint_or_Schwarz_or_physical_admission=False)
