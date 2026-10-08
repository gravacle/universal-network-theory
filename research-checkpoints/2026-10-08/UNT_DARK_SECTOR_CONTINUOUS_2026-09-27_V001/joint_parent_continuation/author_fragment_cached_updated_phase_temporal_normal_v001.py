"""HELD updated-phase temporal-rate current/H and four-normal contact.
Globals np,P,N; reviewed fy_* and cached_phase_* helpers/maps from195.
Completed13764 EOS and15744 normal caches are copied/authenticated once by
caller. Only new direction arithmetic and original weak transposes execute.
A NEW113 mass action with current19724 H supplies its already evaluated scalar
rate and charge response. The staged current derivative remains a comparison;
it never replaces that literal mass action or suppresses stationarity epsilon.
No EOS/log/root/current/normal VALUE, mechanical action or old fixture replay.
"""
CACHED_UPDATED_PHASE_RATE_AUTHOR_DRAFT=True
CACHED_UPDATED_PHASE_RATE_AUTHORING_IN_PROGRESS=False

def cached_updated_phase_eos_temporal_rate(prepared,phase_rate,literal_mass_point,keep,label):
 assert not CACHED_UPDATED_PHASE_RATE_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_RATE_AUTHORING_IN_PROGRESS and prepared['physical_adoption'] is False
 v=prepared['values'];s=prepared['s'];c=prepared['c'];p=s['phi'][0].shape[0];put=lambda n,x:fy_keep(label+'_NEW_'+n,x,keep)
 z=lambda shape:P.a_dd(np.zeros(shape));add=P.a_add;mul=P.a_mul;scale=P.a_mul64;sl=P.a_slice;sub=lambda a,b:add(a,scale(-1.,b))
 expand=lambda x,key:(x[0][key],x[1][key]);neg=lambda x:scale(-1.,x);prod=cached_phase_product_direction;dot=cached_phase_dot_direction;mv=cached_phase_mv_direction
 zero=z((p,))
 for n,x in (('supplied_phase_temporal_rate',phase_rate),('supplied_NEW_literal_mass_point',literal_mass_point)):
  fy_keep(label+'_'+n,x,keep);assert isinstance(x,tuple) and len(x)==2 and all(w.shape==(p,) and w.dtype==np.float64 and np.all(np.isfinite(w)) for w in x)
 direction={n:z(pair[0].shape) for values in (s,c) for n,pair in values.items()}
 direction['phi']=P.a_stack([phase_rate,zero,zero,zero],1)
 put('supplied_temporal_phase_direction',direction['phi'])
 for values,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))), (c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for n,shape in shapes.items():
   fy_keep(label+'_configuration_direction_'+n,direction[n],keep);assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in direction[n])
 assert all(np.all(a==0) for n in ('hi','P','U','uc','N','mu','ih','u') for a in direction[n]),'All configuration fields are fixed in this phase-rate contact'
 assert all(np.array_equal(a,a.swapaxes(-1,-2)) for n in ('hi','ih') for a in direction[n])
 div=lambda key,den,dnum,dden:put(key+'_direction',cached_phase_division_direction(v[key],den,dnum,dden,keep,label+'_'+key))
 draised=put('raised_phi',mv(s['hi'],s['phi'],direction['hi'],direction['phi']))
 dX2=put('X2',neg(dot(s['phi'],v['raised'],direction['phi'],draised)))
 dX=put('X',fy_div(dX2,scale(2.,v['X']),keep,label+'_clock_root_NEW_direction'))
 fy_keep(label+'_NEW_clock_direction_square_residual',sub(scale(2.,mul(v['X'],dX)),dX2),keep)
 dq=div('q',v['X0'],dX,zero);du=put('u',sub(prod(v['q'],v['q'],dq,dq),zero));dd=put('distance_to_EOS_boundary',sub(zero,du))
 ds=div('s',v['d'],du,dd);dlog=put('logarithm',fy_div(ds,v['one_plus_s'],keep,label+'_log_NEW_analytic_direction'))
 dfraction=div('fraction',v['one_plus_s'],ds,add(zero,ds));dpressureq=div('pressure_quotient',v['norm'],sub(dlog,dfraction),zero)
 A0=prepared['constants']['A0'];dpressure=put('pressure',scale(A0,sub(dpressureq,zero)))
 dPXdimensionless=div('PX_dimensionless',v['epnorm'],prod(v['q'],v['s'],dq,ds),zero)
 dPX=div('PX',v['X0'],scale(2*A0,dPXdimensionless),zero)
 dfirst=div('PXX_first',v['epnorm'],scale(2.,ds),zero);dq2=prod(v['q'],v['q'],dq,dq);dd2=prod(v['d'],v['d'],dd,dd)
 # The constant normalization direction is exactly zero; retain source addition.
 dPXXden=add(zero,mul(v['norm'],dd2));dsecond=div('PXX_second',v['PXX_second_denominator'],scale(4.,dq2),dPXXden)
 dPXX=div('PXX',v['X0_squared'],scale(A0,add(dfirst,dsecond)),zero)
 chain={}
 for n,actual,expected in (('P',dpressure,mul(v['PX'],dX)),('PX',dPX,mul(v['PXX'],dX)),('PXX',dPXX,mul(v['PXXX'],dX))):
  fy_keep(label+'_NEW_'+n+'_analytic_chain_actual',actual,keep);fy_keep(label+'_NEW_'+n+'_analytic_chain_expected',expected,keep);chain[n]=put(n+'_analytic_chain_gap',sub(actual,expected))
 dclock=put('clock_velocity',cached_phase_division_direction(v['clock'],expand(v['X'],(Ellipsis,None)),draised,expand(dX,(Ellipsis,None)),keep,label+'_clock_normalization'))
 dpressureJ=put('pressure_current',neg(prod(expand(v['PX'],(Ellipsis,None)),v['clock'],expand(dPX,(Ellipsis,None)),dclock)))
 dr=put('relative_phase',mv(s['P'],s['phi'],direction['P'],direction['phi']));dhir=put('raised_relative_phase',mv(s['hi'],v['r'],direction['hi'],dr))
 drelative=put('literal_relative_current_negative',mv((s['P'][0].transpose(0,2,1),s['P'][1].transpose(0,2,1)),v['hi_r'],(direction['P'][0].transpose(0,2,1),direction['P'][1].transpose(0,2,1)),dhir))
 dJ=put('literal_current',sub(dpressureJ,drelative));dregisteredJ=put('registered_current',sub(dpressureJ,dhir));ddensity=put('density',prod(c['N'],c['mu'],direction['N'],direction['mu']))
 dp=put('literal_canonical_density',prod(v['density'],sl(v['J'],(slice(None),0)),ddensity,sl(dJ,(slice(None),0))))
 dregisteredp=put('registered_canonical_density',prod(v['density'],sl(v['registered_J'],(slice(None),0)),ddensity,sl(dregisteredJ,(slice(None),0))))
 n0=sl(v['clock'],(slice(None),0));dn0=sl(dclock,(slice(None),0));dn02=put('clock_time_square',prod(n0,n0,dn0,dn0));dPXoverX=div('PX_over_X',v['X'],dPX,dX)
 h00=sl(s['hi'],(slice(None),0,0));dh00=sl(direction['hi'],(slice(None),0,0))
 dpressureH=put('pressure_temporal_H',sub(prod(v['PXX'],v['n02'],dPXX,dn02),prod(v['PX_over_X'],add(h00,v['n02']),dPXoverX,add(dh00,dn02))))
 p0=sl(s['P'],(slice(None),slice(None),0));dp0=sl(direction['P'],(slice(None),slice(None),0));dhp0=put('inverse_projector_time_column',mv(s['hi'],p0,direction['hi'],dp0));dA00=put('literal_relative_temporal_coefficient',dot(p0,v['hp0'],dp0,dhp0))
 dH=put('literal_temporal_H',prod(v['density'],sub(v['pressureH'],v['A00']),ddensity,sub(dpressureH,dA00)))
 dregisteredH=put('registered_temporal_H',prod(v['density'],sub(v['pressureH'],sl(v['hp0'],(slice(None),0))),ddensity,sub(dpressureH,sl(dhp0,(slice(None),0)))))
 dIu=mv(c['ih'],c['u'],direction['ih'],direction['u']);db=put('spatial_native_norm_b',fy_sum(add(z((p,3)),mul(c['u'],dIu)),-1))
 dreducednum=prod(c['mu'],sub(v['PXX'],v['b']),direction['mu'],sub(dPXX,db));dreduced=div('reduced_H',c['N'],dreducednum,direction['N'])
 delta=dict(X2=dX2,X=dX,q=dq,u=du,s=ds,pressure=dpressure,PX=dPX,PXX=dPXX,J=dJ,registered_J=dregisteredJ,p=dp,registered_p=dregisteredp,H=dH,registered_H=dregisteredH,reduced_H=dreduced,density=ddensity,current_gap=sub(dJ,dregisteredJ),density_gap=sub(dp,dregisteredp),hessian_gap=sub(dH,dregisteredH),reduced_gap=sub(dH,dreduced))
 for n,a in delta.items():fy_keep(label+'_completed_NEW_delta_'+n,a,keep)
 fy_keep(label+'_NEW_clock_square_construction_contact',add(prod(v['X'],v['X'],dX,dX),dot(s['phi'],v['raised'],direction['phi'],draised)),keep)
 dconstructed=add(z((p,4,4)),prod(expand(s['uc'],(Ellipsis,slice(None),None)),expand(s['U'],(Ellipsis,None,slice(None))),expand(direction['uc'],(Ellipsis,slice(None),None)),expand(direction['U'],(Ellipsis,None,slice(None)))))
 fy_keep(label+'_NEW_supplied_minus_constructed_projector_contact',sub(direction['P'],dconstructed),keep)
 values={n:v[n] for n in delta};values.update(current_gap=v['current_gap'],density_gap=v['density_gap'],hessian_gap=v['hessian_gap'],reduced_gap=v['reduced_gap'])
 put('cached_stage_minus_literal_mass_point',sub(dp,literal_mass_point))
 return dict(phase_direction=direction['phi'],literal_mass_point=literal_mass_point,cached_stage_minus_literal_mass_point=sub(dp,literal_mass_point),value=values,delta=delta,PXXX=v['PXXX'],cached_intermediates=v,constants=prepared['constants'],chain_gaps=chain,candidate_pressure_recomputed_from_invariant=True,candidate_provenance=prepared['candidate_provenance'],new_direction_scope='independent temporal phase rate at updated paired phase',EOS_primal_log_or_current_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False)


def prepare_cached_updated_phase_normal_rate(data,prefix,s,c,eos_prepared,f,b,provenance,keep,label):
 assert not CACHED_UPDATED_PHASE_RATE_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_RATE_AUTHORING_IN_PROGRESS
 p=s['phi'][0].shape[0];v=eos_prepared['values'];assert provenance and eos_prepared['physical_adoption'] is False
 a={n:cached_phase_pair(data,prefix+NORMAL_NAMES[n],(p,)+shape,keep,label+'_copied_normal_'+n) for n,shape in NORMAL_FIELDS.items()}
 for values,shapes in ((s,dict(g=(p,4,4),hi=(p,4,4),U=(p,4),uc=(p,4),P=(p,4,4),phi=(p,4))), (c,dict(N=(p,),mu=(p,),h=(p,3,3),beta=(p,3)))):
  for n,shape in shapes.items():
   old=cached_phase_pair(data,prefix+'supplied_'+n,shape,keep,label+'_same_cached_normal_'+n)
   assert all(np.array_equal(x,y) for x,y in zip(old,values[n])),n
 assert f.shape==(p,) and b.shape==(p,3) and f.dtype==b.dtype==np.float64
 for n,test in (('fixed_test_lapse',f),('fixed_test_shift',b)):
  x=keep(label+'_same_'+n,data[prefix+n].copy());assert np.array_equal(x,test)
 for n in ('X','pressure','PX'):
  x=cached_phase_pair(data,prefix+'EOS_'+n,(p,),keep,label+'_same_cached_EOS_'+n);assert all(np.array_equal(x,y) for x,y in zip(x,v[n]))
 for n,shape in (('EOS_clock_square_contact',(p,)),('measure_test_trace_contact',(p,)),('unit_constraint',(p,)),('projector_construction_contact',(p,4,4))):cached_phase_pair(data,prefix+n,shape,keep,label+'_inherited_'+n)
 assert all(np.array_equal(x,y) for n,key in (('r','r'),('density','density')) for x,y in zip(a[n],v[key]))
 # These are NEW fixed coefficients of the rate derivative, not a scalar value
 # action. Compute once, retain them and reuse across phase inverse arguments.
 coeff={n:fy_keep(label+'_NEW_fixed_contact_coefficient_'+n,x,keep) for n,x in (
  ('It_phi',fy_mv(a['It'],s['phi'])),('It_r',fy_mv(a['It'],a['r'])),('hi_rt',fy_mv(s['hi'],a['rt'])))}
 return dict(test=a,s=s,c=c,f=f.copy(),b=b.copy(),contact_coefficients=coeff,cached_value_provenance=provenance,
             phase_normal_value_recomputed=False,physical_adoption=False)


def cached_updated_phase_normal_temporal_rate(prepared,eos,keep,label):
 assert not CACHED_UPDATED_PHASE_RATE_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_RATE_AUTHORING_IN_PROGRESS
 assert prepared['physical_adoption'] is False and eos['old_temporal_direction_reused'] is False
 assert eos['new_direction_scope']=='independent temporal phase rate at updated paired phase'
 a,s,c,k=prepared['test'],prepared['s'],prepared['c'],prepared['contact_coefficients'];p=s['phi'][0].shape[0];dphi=eos['phase_direction']
 put=lambda n,x:fy_keep(label+'_NEW_'+n,x,keep);add=P.a_add;mul=P.a_mul;scale=P.a_mul64;neg=lambda x:scale(-1.,x)
 z=lambda shape:P.a_dd(np.zeros(shape));zero=z((p,));prod=cached_phase_product_direction;dot=cached_phase_dot_direction
 assert all(np.all(w[:,1:]==0) for w in dphi),'Temporal phase direction only'
 dr=put('relative_phase',fy_mv(s['P'],dphi));drt=put('relative_phase_test',fy_mv(a['Pt'],dphi))
 dhi_r=fy_mv(s['hi'],dr);dr2=put('relative_phase_squared',dot(a['r'],eos['cached_intermediates']['hi_r'],dr,dhi_r))
 It_dphi=put('test_inverse_phase_direction',fy_mv(a['It'],dphi))
 # BOTH outer and inner phase contacts are required; geometry/test are fixed.
 dXnum=put('clock_test_numerator',scale(-.5,dot(s['phi'],k['It_phi'],dphi,It_dphi)))
 dXtest=put('clock_test',cached_phase_division_direction(a['Xtest'],eos['value']['X'],dXnum,eos['delta']['X'],keep,label+'_clock_test'))
 dIt_r=fy_mv(a['It'],dr);dhi_rt=fy_mv(s['hi'],drt)
 dabs=put('absolute_terms',P.a_stack([prod(eos['value']['PX'],a['Xtest'],eos['delta']['PX'],dXtest),prod(eos['value']['pressure'],a['lm'],eos['delta']['pressure'],zero)],1))
 drel=put('relative_terms',P.a_stack([scale(-.5,dot(a['r'],k['It_r'],dr,dIt_r)),neg(dot(a['r'],k['hi_rt'],dr,dhi_rt)),scale(-.5,prod(a['r2'],a['lm'],dr2,zero))],1))
 dabsolute=put('absolute',prod(a['density'],fy_sum(a['absolute_terms'],1),zero,fy_sum(dabs,1)))
 drelative=put('relative',prod(a['density'],fy_sum(a['relative_terms'],1),zero,fy_sum(drel,1)))
 daction=put('action',add(dabsolute,drelative));dHamiltonian=put('hamiltonian',neg(daction))
 for n,shape in (('metric_test',(p,4,4)),('inverse_metric_test',(p,4,4)),('native_test',(p,4)),('projector_test',(p,4,4)),('measure_test',(p,)),('density',(p,))):put(n+'_fixed_geometry_direction',z(shape))
 put('cached_phase_vs_EOS_relative_contact',P.a_sub(a['r'],eos['cached_intermediates']['r']))
 return dict(value={n:a[n] for n in ('absolute','relative','action','hamiltonian')},delta=dict(absolute=dabsolute,relative=drelative,action=daction,hamiltonian=dHamiltonian),
             cached_value_provenance=prepared['cached_value_provenance'],new_direction_scope='independent temporal phase at fixed geometry; all four normal value rows',
             test_first_derivative_coefficients_zero=True,normal_R_Z_t_test_jet_directions_zero_by_phase_action=True,relative_phase_included_once=True,
             cached_normal_value_action_recomputed=False,mechanical_canonical_temporal_crossblock_zero=True,CMC_phase_rate_crossblock_zero=True,physical_adoption=False)


def cached_updated_phase_rate_normal_action(columns,mass_cache,basis,mass_action,keep,label,column_complete=None):
 assert not CACHED_UPDATED_PHASE_RATE_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_RATE_AUTHORING_IN_PROGRESS
 assert len(columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert mass_cache['fresh_literal_candidate_H_used'] is True and mass_cache['reference_H_reused'] is False
 assert mass_cache['phase_space_dofs']==3870 and mass_cache['phase_outer_top_nodes_free'] is True and mass_cache['physical_adoption'] is False
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],mass_cache['basis'][n]),'Same original scalar and normal geometry'
 rate=mass_action['scalar_jets']['value'];point_mass=mass_action['point'];weak_mass=mass_action['weak']
 for n,x,shape in (('supplied_NEW_phase_value',rate,(15136,)),('supplied_NEW_literal_mass_point',point_mass,(15136,)),('supplied_NEW_literal_mass_weak',weak_mass,(87,45))):
  fy_keep(label+'_'+n,x,keep);assert isinstance(x,tuple) and len(x)==2 and all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x)
 assert all(np.all(a[0]==0) for a in weak_mass) and np.count_nonzero(P.scalar_mask())==3870
 assert mass_action['extra_N_or_mu_factor_inserted'] is False and mass_action['temporal_mechanical_crossblock_zero_scope']=='fixed configuration only'
 point=P.a_dd(np.zeros((15136,4,3)));primary=P.a_dd(np.zeros((15136,4)));stage=P.a_dd(np.zeros(15136));stage_minus_mass=P.a_dd(np.zeros(15136));completed=[]
 for iq,column in enumerate(columns):
  sl=slice(iq*3784,(iq+1)*3784);prepared=column['eos'];assert prepared['physical_adoption'] is False and len(column['normal_rows'])==4
  assert all(np.array_equal(a,b) for a,b in zip(prepared['values']['H'],P.a_slice(mass_cache['H'],sl))),'Updated13764 H must be the SAME current mass-cache representative'
  eos=cached_updated_phase_eos_temporal_rate(prepared,P.a_slice(rate,sl),P.a_slice(point_mass,sl),keep,label+'_column%d_EOS_rate'%iq)
  rows=[]
  for row,test in enumerate(column['normal_rows']):
   f=np.ones(3784) if row==0 else np.zeros(3784);b=np.zeros((3784,3))
   if row:b[:,row-1]=1.
   assert np.array_equal(test['f'],f) and np.array_equal(test['b'],b),'Original unit lapse/shift point-value rows required'
   normal=cached_updated_phase_normal_temporal_rate(test,eos,keep,label+'_column%d_row%d_rate'%(iq,row));rows.append(normal['delta']['hamiltonian'])
  values=P.a_stack(rows,1)
  for word in (0,1):point[word][sl,:,0]=values[word];stage[word][sl]=eos['delta']['p'][word];stage_minus_mass[word][sl]=eos['cached_stage_minus_literal_mass_point'][word]
  fy_keep(label+'_completed_phase_normal_inventory',point,keep);fy_keep(label+'_completed_staged_current_inventory',stage,keep);fy_keep(label+'_completed_stage_minus_mass_inventory',stage_minus_mass,keep)
  if column_complete is not None:completed.append(column_complete(iq,dict(eos=eos,point_Hamiltonian_normal=values,stage_current=eos['delta']['p'],literal_mass_point=P.a_slice(point_mass,sl),stage_minus_mass=eos['cached_stage_minus_literal_mass_point'],normal_provenance=[q['cached_value_provenance'] for q in column['normal_rows']])))
 weak_normal=N.paired_scatter_normal(point,basis,label+'_NEW_phase_rate_normal');weak_stage=P.dd_scalar_scatter(stage,basis,keep,label+'_NEW_staged_current')
 weak_gap=P.a_sub(weak_stage,weak_mass)
 for n,x in (('point_Hamiltonian_normal',point),('time_primary_action_coefficients',primary),('weak_Hamiltonian_normal',weak_normal),('staged_current_weak',weak_stage),('literal_mass_weak',weak_mass),('staged_current_minus_literal_mass_weak',weak_gap),('initial_CMC_phase_rate_zero',P.a_dd(np.zeros((87,45))))):fy_keep(label+'_'+n,x,keep)
 assert all(np.all(a[~N.normal_test_mask()]==0) for a in weak_normal)
 return dict(weak_normal=weak_normal,point_Hamiltonian_normal=point,time_primary_action_coefficients=primary,stage_current_weak=weak_stage,literal_mass_weak=weak_mass,stage_minus_literal_mass_weak=weak_gap,stage_minus_literal_mass_point=stage_minus_mass,
             completed_column_refs=completed,original_phase_mass_action_authoritative=True,stage_current_does_not_replace_M=True,stationarity_epsilon_required=True,
             reduced_RHS_requires_phase_epsilon_feedback=True,full_configuration_newton_decoupled=False,normal_relative_phase_count=1,
             CMC_phase_rate_contact_exact_zero=True,mechanical_canonical_phase_rate_contact_exact_zero=True,new_finite_state_or_charge_solution=False,physical_adoption=False)
