"""HELD same-state mechanical-rate derivative of four normal rows and CMC.
Globals np,P,N, reviewed fy_* and finite160/native-EH239 definitions.
The caller authenticates SAME225 configuration/mechanical rates, original
basis and CLOSED intrinsic-curvature Q/V words. Only NEW rate directions
execute. No EOS, phase/ordinary VALUE, current, target, mass, factor or solve.
Phase and ordinary direct rate contacts vanish at fixed instantaneous fields;
their separate configuration/phase contacts and epsilon feedback remain.
"""
MECHANICAL_RATE_NORMAL_AUTHOR_DRAFT=True
MECHANICAL_RATE_NORMAL_AUTHORING_IN_PROGRESS=False


def candidate_mechanical_rate_normal_column(column,native_rate,metric_rate,Hbar,keep,label,row_complete=None):
 assert not MECHANICAL_RATE_NORMAL_AUTHOR_DRAFT and not MECHANICAL_RATE_NORMAL_AUTHORING_IN_PROGRESS
 assert column['provenance']['same_candidate_geometry_and_current_mechanical_rates'] is True
 p=len(column['candidate']['c']['N']);zero=lambda shape:P.a_dd(np.zeros(shape))
 for n,x,shape in (('native',native_rate,(p,99)),('metric',metric_rate,(p,6))):
  fy_keep(label+'_supplied_'+n+'_rate',x,keep)
  assert isinstance(x,tuple) and len(x)==2 and all(w.shape==shape and w.dtype==np.float64 and np.all(np.isfinite(w)) for w in x)
 hdot=zero((p,3,3));ujets=zero((p,4,3));zjets=zero((32,p,4,3))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for w in (0,1):hdot[w][:,i,j]=hdot[w][:,j,i]=metric_rate[w][:,slot]
 for w in (0,1):
  rates=native_rate[w].reshape(p,33,3);ujets[w][:,0]=rates[:,0];zjets[w][:,:,0]=rates[:,1:].transpose(1,0,2)
 direction=dict(h=zero((p,3,3)),h_spatial_jets=zero((p,2,3,3)),h_dot=hdot,u_jets=ujets,z_jets=zjets)
 for n,x in direction.items():fy_keep(label+'_NEW_direction_'+n,x,keep)
 contact=finite_candidate_configuration_contact(column['candidate'],column['geometry'],column['gauge'],column['covectors'],column['mechanical'],direction,column['reference'],keep,label+'_NEW_rate_contact')
 for fields,names in ((contact['d'],('g','hi','U','z','uc','P','phi')),(contact['dc'],('h','ih','N','beta','u','up','gamma','dens','sqrt_h'))):
  for n in names:
   fy_keep(label+'_fixed_instantaneous_'+n,fields[n],keep);assert all(np.all(w==0) for w in fields[n]),n
 # Fixed h and all spatial h jets imply exact zero curvature direction. Reuse
 # the authenticated value words, rather than rebuilding an old curvature.
 assert column['curvature_provenance'] and column['intrinsic_curvature']['physical_adoption'] is False
 curvature={}
 for n,shape in (('Q',(p,)),('V',(p,3))):
  x=column['intrinsic_curvature'][n];fy_keep(label+'_copied_closed_intrinsic_'+n,x,keep)
  assert isinstance(x,tuple) and len(x)==2 and all(w.shape==shape and w.dtype==np.float64 and np.all(np.isfinite(w)) for w in x)
  curvature[n]=(x,zero(shape));fy_keep(label+'_zero_intrinsic_direction_'+n,curvature[n][1],keep)
 coeff=zero((p,4,4));theta=None;rows=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   tag=label+'_row%d_jet%d'%(row,jet)
   result=finite_candidate_native_EH_normal(column['candidate'],contact,curvature,f,df,b,db,Hbar,column['reference'],keep,tag+'_NEW_native_EH_rate')
   assert result['relative_phase_included'] is False and result['all_four_coordinate_test_jets_retained'] is True
   for w in (0,1):coeff[w][:,row,jet]=result['delta']['hamiltonian'][w]
   if theta is None:theta=tuple(w.copy() for w in result['delta']['initial_CMC_density'])
   else:assert all(np.array_equal(a,bw) for a,bw in zip(theta,result['delta']['initial_CMC_density']))
   fy_keep(tag+'_completed_normal_rate_inventory',coeff,keep);fy_keep(tag+'_same_CMC_rate_contact',theta,keep)
   if row_complete is not None:rows.append(row_complete(row,jet,dict(normal_rate=result['delta'],normal_coefficients=coeff,initial_CMC_density=theta)))
 fy_keep(label+'_completed_four_normal_rate_coefficients',coeff,keep);fy_keep(label+'_completed_CMC_rate_density',theta,keep)
 return dict(normal_coefficients=coeff,initial_CMC_density=theta,completed_row_refs=rows,
             mechanical_rate_direction=direction,mechanical_point_contact=contact['delta_momenta'],normal_coordinate_order=('value','R','Z','t'),
             direct_phase_normal_rate_zero=True,direct_ordinary_normal_rate_zero=True,sheet_direct_mechanical_rate_zero=True,
             intrinsic_curvature_direction_zero_by_fixed_spatial_geometry=True,stationarity_epsilon_required=True,
             finite_state_normal_or_canonical_restoration=False,physical_adoption=False)


def candidate_whole_mechanical_rate_normal_contact(columns,basis,native_nodes,metric_nodes,Hbar,normal_test,scalar_test,keep,check,label,row_complete=None,column_complete=None):
 assert not MECHANICAL_RATE_NORMAL_AUTHOR_DRAFT and not MECHANICAL_RATE_NORMAL_AUTHORING_IN_PROGRESS
 assert len(columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert np.isfinite(Hbar) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 for n,x,shape,mask in (('native',native_nodes,(33,3,87,45),np.broadcast_to(P.native_mask(),(33,3,87,45))),('metric',metric_nodes,(6,87,45),P.metric_mask())):
  fy_keep(label+'_supplied_original_'+n+'_nodes',x,keep)
  assert isinstance(x,tuple) and len(x)==2 and all(w.shape==shape and w.dtype==np.float64 and np.all(np.isfinite(w)) and np.all(w[~mask]==0) for w in x)
 native=fy_keep(label+'_NEW_original_native_value_lift',P.dd_native_node_value(native_nodes,basis,keep,jet=0),keep)
 metric=fy_keep(label+'_NEW_original_physical_metric_value_lift',P.dd_metric_node_value(metric_nodes,basis,keep,jet=0),keep)
 parts=[];completed=[]
 for iq,column in enumerate(columns):
  assert np.array_equal(column['candidate']['s']['R'],basis['R'][iq]);sl=slice(iq*3784,(iq+1)*3784)
  nr=tuple(w[:,sl].transpose(1,0,2).reshape(3784,99).copy() for w in native);mr=tuple(w[sl].copy() for w in metric)
  callback=None if row_complete is None else lambda row,jet,result:row_complete(iq,row,jet,result)
  part=candidate_mechanical_rate_normal_column(column,nr,mr,Hbar,keep,label+'_column%d'%iq,callback);parts.append(part)
  if column_complete is not None:completed.append(column_complete(iq,part))
 # Reader's independently reviewed delta-only original normal/CMC assembler.
 assembled=candidate_configuration_normal_CMC_direction(parts,basis,normal_test,scalar_test,keep,check,label+'_NEW_weak_normal_CMC')
 return dict(weak_normal=assembled['weak_normal'],weak_initial_CMC=assembled['weak_initial_CMC'],
             time_primary_action_coefficients=assembled['time_primary_action_coefficients'],normal_CMC=assembled,
             compact_column_parts=parts,completed_column_refs=completed,normal_rate_dofs=14875,CMC_rate_dofs=3870,
             relative_phase_and_ordinary_direct_rate_zero=True,mechanical_epsilon_feedback_required=True,
             phase_epsilon_feedback_supplied_separately=True,reduced_configuration_operator_assembled=False,
             original_six_canonical_gates_not_evaluated=True,finite_state_or_physical_adoption=False,physical_adoption=False)
