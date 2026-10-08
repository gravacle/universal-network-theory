"""HELD direction-only updated-phase EOS/current/H and normal contact.
Globals np,P,fy_keep/fy_sum/fy_div/fy_mv/fy_mm from reviewed arithmetic.
All value operands and quotient/log intermediates come from completed116.
The direction is the original compact-chi geometry contact, with phi/N/u held.
No EOS value, square root, logarithm, current, normal or old producer is called.
The containing owner authenticates closed finite116 and new62 row caches before
using this component. New62 row caches have no authority until natural closure.
"""
CACHED_UPDATED_PHASE_CHI_AUTHOR_DRAFT=True
CACHED_UPDATED_PHASE_CHI_AUTHORING_IN_PROGRESS=False
EOS_SCALARS={
 'X2':'invariant_X_squared','X':'invariant_X','q':'invariant_q','u':'clock_pressure_u','s':'EOS_s','d':'distance_to_EOS_boundary',
 'pressure':'pressure','PX':'PX','PXX':'PXX','PXXX':'PXXX','density':'candidate_density','b':'spatial_native_norm_b',
 'n02':'clock_time_square','pressureH':'pressure_temporal_H','A00':'literal_relative_temporal_coefficient',
 'p':'literal_canonical_density','registered_p':'registered_canonical_density','H':'literal_temporal_H','registered_H':'registered_temporal_H','reduced_H':'reduced_ADM_H',
 'one_plus_s':'log1p_s_one_plus_argument','logarithm':'EOS_log1p_s','fraction':'EOS_s_over_one_plus_s',
 'pressure_quotient':'pressure_norm_value_quotient','PX_dimensionless':'PX_dimensionless_value_quotient',
 'PXX_first':'PXX_first_term','PXX_second':'PXX_second_term','PX_over_X':'PX_over_X_value_quotient',
 'X0':'q_value_denominator','norm':'pressure_norm_value_denominator','epnorm':'PX_dimensionless_value_denominator',
 'X0_squared':'PXX_units_value_denominator','PXX_second_denominator':'PXX_second_value_denominator',
 'log_ratio_product_gap':'log1p_s_ratio_readout_product_defect','clock_square_gap':'clock_square_construction_gap',
 'density_gap':'density_gap','hessian_gap':'hessian_gap','reduced_gap':'reduced_gap'}
EOS_VECTORS={'raised':'raised_phi','clock':'clock_velocity','pressure_J':'pressure_current','r':'literal_projected_phase','hi_r':'raised_relative_phase','relative':'literal_relative_current_negative','J':'literal_current','registered_J':'registered_current','hp0':'inverse_projector_time_column','current_gap':'current_gap'}
EOS_MATRICES={'projector_gap':'supplied_minus_constructed_projector_gap'}
EOS_DIVISION_GAPS=('q','s','s_fraction','pressure_norm','PX_dimensionless','PX_units','PXX_first','PXX_second','PXX_units','clock_normalization','PX_over_X','reduced_H')
NORMAL_FIELDS={'q':(4,4),'It':(4,4),'eta':(4,),'uct':(4,),'Pt':(4,4),'r':(4,),'rt':(4,),'r2':(),'Xtest':(),'lm':(),'absolute_terms':(2,),'relative_terms':(3,),'density':(),'absolute':(),'relative':(),'action':(),'hamiltonian':()}
NORMAL_NAMES=dict(q='metric_test',It='inverse_metric_test',eta='native_test',uct='lowered_native_test',Pt='projector_test',r='relative_phase',rt='relative_phase_test',r2='relative_phase_squared',Xtest='clock_test',lm='measure_test',absolute_terms='absolute_terms',relative_terms='relative_terms',density='density',absolute='absolute_action',relative='relative_action',action='action_coefficient',hamiltonian='Hamiltonian_coefficient')

def cached_phase_pair(data,name,shape,keep,label):
 pair=(data[name+'_hi'].copy(),data[name+'_lo'].copy());keep(label+'_both_words',np.stack(pair).copy())
 assert all(w.shape==shape and w.dtype==np.float64 and np.all(np.isfinite(w)) for w in pair)
 return fy_keep(label,pair,keep)

def cached_phase_product_direction(a,b,da,db):
 # Exact fs_mul direction association; neither primal product is evaluated.
 return P.a_add(P.a_mul(da,b),P.a_mul(a,db))

def cached_phase_dot_direction(a,b,da,db):
 return fy_sum(cached_phase_product_direction(a,b,da,db),-1)

def cached_phase_mv_direction(A,x,dA,dx):
 return fy_sum(cached_phase_product_direction(A,(x[0][...,None,:],x[1][...,None,:]),dA,(dx[0][...,None,:],dx[1][...,None,:])),-1)

def cached_phase_mm_direction(A,B,dA,dB):
 return P.a_stack([cached_phase_mv_direction(A,P.a_slice(B,(Ellipsis,slice(None),j)),dA,P.a_slice(dB,(Ellipsis,slice(None),j))) for j in range(B[0].shape[-1])],-1)

def cached_phase_division_direction(quotient,denominator,dnumerator,ddenominator,keep,label):
 fy_keep(label+'_cached_quotient',quotient,keep);fy_keep(label+'_cached_denominator',denominator,keep)
 fy_keep(label+'_new_numerator_direction',dnumerator,keep);fy_keep(label+'_new_denominator_direction',ddenominator,keep)
 numerator=fy_keep(label+'_direction_numerator',P.a_sub(dnumerator,P.a_mul(quotient,ddenominator)),keep)
 delta=fy_div(numerator,denominator,keep,label+'_NEW_direction')
 fy_keep(label+'_direction_division_residual',P.a_sub(P.a_add(P.a_mul(denominator,delta),P.a_mul(ddenominator,quotient)),dnumerator),keep)
 return delta

def cached_updated_phase_contact_names(prefix,normal=False):
 mapping=NORMAL_NAMES if normal else {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}
 names=[prefix+n+'_'+w for n in mapping.values() for w in ('hi','lo')]
 if normal:
  names += [prefix+'supplied_'+n+'_'+w for n in ('g','hi','U','uc','P','phi','N','mu','h','beta') for w in ('hi','lo')]
  names += [prefix+n for n in ('fixed_test_lapse','fixed_test_shift')]
  names += [prefix+'EOS_'+n+'_'+w for n in ('X','pressure','PX') for w in ('hi','lo')]
  names += [prefix+n+'_'+w for n in ('EOS_clock_square_contact','measure_test_trace_contact','unit_constraint','projector_construction_contact') for w in ('hi','lo')]
 else:
  names += [prefix+'supplied_'+n+'_'+w for n in ('hi','P','phi','U','uc','N','mu','ih','u') for w in ('hi','lo')]
  names += [prefix+'log1p_s_'+n for n in ('elementary_low_over_high','elementary_log_high','elementary_log1p_low')]
  names += [prefix+n+'_'+w for n in ('P_analytic_chain_actual','P_analytic_chain_expected','P_analytic_chain_gap','PX_analytic_chain_actual','PX_analytic_chain_expected','PX_analytic_chain_gap','PXX_analytic_chain_actual','PXX_analytic_chain_expected','PXX_analytic_chain_gap') for w in ('hi','lo')]
  names += [prefix+n+'_value_final_division_residual_'+w for n in EOS_DIVISION_GAPS for w in ('hi','lo')]
  names += [prefix+n for n in ('current_operation_envelope','H_operation_envelope')]
 return tuple(names)

def prepare_cached_updated_phase_contact(data,prefix,s,c,constants,provenance,keep,label):
 assert not CACHED_UPDATED_PHASE_CHI_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_CHI_AUTHORING_IN_PROGRESS
 p=s['phi'][0].shape[0];cache={}
 for key,name in {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}.items():cache[key]=cached_phase_pair(data,prefix+name,(p,4,4) if key in EOS_MATRICES else (p,4) if key in EOS_VECTORS else (p,),keep,label+'_copied_'+key)
 for values,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))), (c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for n,shape in shapes.items():
   supplied=cached_phase_pair(data,prefix+'supplied_'+n,shape,keep,label+'_same_candidate_'+n)
   assert all(np.array_equal(a,b) for a,b in zip(supplied,values[n])),'Cached EOS must match the actual updated phase and shared geometry'
 for n in ('elementary_low_over_high','elementary_log_high','elementary_log1p_low'):
  x=keep(label+'_inherited_'+n,data[prefix+'log1p_s_'+n].copy());assert x.shape==(p,) and x.dtype==np.float64
 for n in ('P','PX','PXX'):
  for kind in ('actual','expected','gap'):cached_phase_pair(data,prefix+n+'_analytic_chain_'+kind,(p,),keep,label+'_inherited_temporal_chain_'+n+'_'+kind)
 for n in EOS_DIVISION_GAPS:cached_phase_pair(data,prefix+n+'_value_final_division_residual',(p,4) if n=='clock_normalization' else (p,),keep,label+'_inherited_primal_division_gap_'+n)
 for n,shape in (('current_operation_envelope',(p,4)),('H_operation_envelope',(p,))):
  a=keep(label+'_inherited_primal_'+n,data[prefix+n].copy());assert a.shape==shape and a.dtype==np.float64 and np.all(a>=0)
 assert constants['relative_phase_coefficient']==1. and constants['synthetic_control'] is False and constants['eps']==1e-5 and constants['C']==1.98
 for n,key in (('X0','X0'),('norm','norm')):
  assert all(np.array_equal(a,b) for a,b in zip(cache[key],P.a_dd(np.full(p,constants[n]))))
 assert np.all(cache['X'][0]-abs(cache['X'][1])>0) and np.all(cache['u'][0]-abs(cache['u'][1])>0) and np.all(constants['eps']-cache['u'][0]-abs(cache['u'][1])>0)
 assert provenance and provenance['fresh_direction_scope']=='same temporal phase step only; all configuration directions zero'
 return dict(values=cache,s=s,c=c,constants=dict(constants),candidate_provenance=provenance,EOS_values_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False)

def cached_updated_phase_eos_compact_chi(prepared,direction,keep,label):
 assert not CACHED_UPDATED_PHASE_CHI_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_CHI_AUTHORING_IN_PROGRESS and prepared['physical_adoption'] is False
 v=prepared['values'];s=prepared['s'];c=prepared['c'];p=s['phi'][0].shape[0];put=lambda n,x:fy_keep(label+'_NEW_'+n,x,keep)
 z=lambda shape:P.a_dd(np.zeros(shape));add=P.a_add;mul=P.a_mul;scale=P.a_mul64;sl=P.a_slice;sub=lambda a,b:add(a,scale(-1.,b))
 expand=lambda x,key:(x[0][key],x[1][key]);neg=lambda x:scale(-1.,x);prod=cached_phase_product_direction;dot=cached_phase_dot_direction;mv=cached_phase_mv_direction
 zero=z((p,))
 for values,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))), (c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for n,shape in shapes.items():
   fy_keep(label+'_configuration_direction_'+n,direction[n],keep);assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in direction[n])
 assert all(np.all(a==0) for n in ('N','u','phi') for a in direction[n]),'This is the original compact-chi geometry direction, not a phase-rate step'
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
 return dict(value=values,delta=delta,PXXX=v['PXXX'],cached_intermediates=v,constants=prepared['constants'],chain_gaps=chain,candidate_pressure_recomputed_from_invariant=True,candidate_provenance=prepared['candidate_provenance'],new_direction_scope='original compact-chi geometry at updated paired phase',EOS_primal_log_or_current_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False)

def cached_updated_phase_normal_compact_chi(data,prefix,s,c,direction,eos,f,b,provenance,keep,label):
 assert not CACHED_UPDATED_PHASE_CHI_AUTHOR_DRAFT and not CACHED_UPDATED_PHASE_CHI_AUTHORING_IN_PROGRESS
 p=s['phi'][0].shape[0];a={n:cached_phase_pair(data,prefix+NORMAL_NAMES[n],(p,)+shape,keep,label+'_copied_NEW_phase_normal_'+n) for n,shape in NORMAL_FIELDS.items()}
 assert provenance and eos['old_temporal_direction_reused'] is False and eos['new_direction_scope']=='original compact-chi geometry at updated paired phase'
 assert f.shape==(p,) and b.shape==(p,3) and f.dtype==b.dtype==np.float64
 assert all(np.all(w==0) for n in ('N','beta','phi') for w in direction[n])
 for values,shapes in ((s,dict(g=(p,4,4),hi=(p,4,4),U=(p,4),uc=(p,4),P=(p,4,4),phi=(p,4))), (c,dict(N=(p,),mu=(p,),h=(p,3,3),beta=(p,3)))):
  for n,shape in shapes.items():
   old=cached_phase_pair(data,prefix+'supplied_'+n,shape,keep,label+'_same_cached_phase_test_'+n)
   assert all(np.array_equal(x,y) for x,y in zip(old,values[n]))
   fy_keep(label+'_compact_chi_direction_'+n,direction[n],keep);assert all(x.shape==shape and x.dtype==np.float64 and np.all(np.isfinite(x)) for x in direction[n])
 for n,test in (('fixed_test_lapse',f),('fixed_test_shift',b)):
  value=keep(label+'_same_'+n,data[prefix+n].copy());assert np.array_equal(value,test)
 for n in ('X','pressure','PX'):
  old=cached_phase_pair(data,prefix+'EOS_'+n,(p,),keep,label+'_same_cached_phase_test_EOS_'+n);assert all(np.array_equal(x,y) for x,y in zip(old,eos['value'][n]))
 for n,shape in (('EOS_clock_square_contact',(p,)),('measure_test_trace_contact',(p,)),('unit_constraint',(p,)),('projector_construction_contact',(p,4,4))):cached_phase_pair(data,prefix+n,shape,keep,label+'_inherited_phase_test_'+n)
 put=lambda n,x:fy_keep(label+'_NEW_'+n,x,keep);add=P.a_add;scale=P.a_mul64;sl=P.a_slice;mul=P.a_mul;neg=lambda x:scale(-1.,x);sub=lambda a,b:add(a,neg(b))
 z=lambda shape:P.a_dd(np.zeros(shape));expand=lambda x,key:(x[0][key],x[1][key]);prod=cached_phase_product_direction;dot=cached_phase_dot_direction;mv=cached_phase_mv_direction;mm=cached_phase_mm_direction
 ft=P.a_dd(f);bt=P.a_dd(b);zero=z((p,));zeros3=z((p,3));zeros4=z((p,4))
 dhb=mv(c['h'],bt,direction['h'],zeros3);hb=sl(a['q'],(slice(None),0,slice(1,None)))
 dq00=add(scale(-2.,prod(c['N'],ft,direction['N'],zero)),scale(2.,dot(c['beta'],hb,direction['beta'],dhb)))
 dq=P.a_stack([P.a_stack([dq00]+[sl(dhb,(slice(None),i)) for i in range(3)],-1)]+[P.a_stack([sl(dhb,(slice(None),i))]+[zero]*3,-1) for i in range(3)],-2);put('metric_test',dq)
 # These small compositions are coefficients of the new product-rule contact,
 # not an EOS/current/value action replay. Their associations match fs_mm.
 Iq=fy_keep(label+'_NEW_contact_coefficient_inverse_times_test',fy_mm(s['hi'],a['q']),keep)
 dIq=mm(s['hi'],a['q'],direction['hi'],dq);dIt=put('inverse_test',neg(mm(Iq,s['hi'],dIq,direction['hi'])))
 qeta=neg(sl(a['eta'],(slice(None),0)));deta0=neg(cached_phase_division_direction(qeta,c['N'],prod(sl(s['U'],(slice(None),0)),ft,sl(direction['U'],(slice(None),0)),zero),direction['N'],keep,label+'_eta_time'))
 detai=sub(neg(prod(expand(sl(s['U'],(slice(None),0)),(Ellipsis,None)),bt,expand(sl(direction['U'],(slice(None),0)),(Ellipsis,None)),zeros3)),prod(c['beta'],expand(sl(a['eta'],(slice(None),0)),(Ellipsis,None)),direction['beta'],expand(deta0,(Ellipsis,None))))
 deta=put('native_test',P.a_stack([deta0]+[sl(detai,(slice(None),i)) for i in range(3)],1))
 duct=put('lowered_native_test',add(mv(a['q'],s['U'],dq,direction['U']),mv(s['g'],a['eta'],direction['g'],deta)))
 dPt=put('projector_test',add(prod(expand(a['uct'],(Ellipsis,slice(None),None)),expand(s['U'],(Ellipsis,None,slice(None))),expand(duct,(Ellipsis,slice(None),None)),expand(direction['U'],(Ellipsis,None,slice(None)))),prod(expand(s['uc'],(Ellipsis,slice(None),None)),expand(a['eta'],(Ellipsis,None,slice(None))),expand(direction['uc'],(Ellipsis,slice(None),None)),expand(deta,(Ellipsis,None,slice(None))))))
 dr=put('relative_phase',mv(s['P'],s['phi'],direction['P'],direction['phi']));drt=put('relative_phase_test',mv(a['Pt'],s['phi'],dPt,direction['phi']))
 assert all(np.array_equal(x,y) for x,y in zip(a['r'],eos['cached_intermediates']['r'])), 'Cached phase test and EOS must have the same literal projected phase'
 hi_r=eos['cached_intermediates']['hi_r'];fy_keep(label+'_copied_same_EOS_inverse_relative',hi_r,keep)
 dhi_r=mv(s['hi'],a['r'],direction['hi'],dr);dr2=put('relative_squared',dot(a['r'],hi_r,dr,dhi_r))
 It_phi_delta=mv(a['It'],s['phi'],dIt,direction['phi']);dXtestnum=scale(-.5,fy_sum(add(zeros4,mul(s['phi'],It_phi_delta)),-1))
 dXtest=put('clock_test',cached_phase_division_direction(a['Xtest'],eos['value']['X'],dXtestnum,eos['delta']['X'],keep,label+'_clock_test'))
 dlm=put('measure_test',cached_phase_division_direction(a['lm'],c['N'],zero,direction['N'],keep,label+'_measure_test'))
 It_r=fy_keep(label+'_NEW_contact_coefficient_test_inverse_relative',fy_mv(a['It'],a['r']),keep);dIt_r=mv(a['It'],a['r'],dIt,dr)
 hi_rt=fy_keep(label+'_NEW_contact_coefficient_inverse_relative_test',fy_mv(s['hi'],a['rt']),keep);dhi_rt=mv(s['hi'],a['rt'],direction['hi'],drt)
 dabs=P.a_stack([prod(eos['value']['PX'],a['Xtest'],eos['delta']['PX'],dXtest),prod(eos['value']['pressure'],a['lm'],eos['delta']['pressure'],dlm)],1)
 drel=P.a_stack([scale(-.5,dot(a['r'],It_r,dr,dIt_r)),neg(dot(a['r'],hi_rt,dr,dhi_rt)),scale(-.5,prod(a['r2'],a['lm'],dr2,dlm))],1)
 put('absolute_terms',dabs);put('relative_terms',drel);ddensity=put('density',prod(c['N'],c['mu'],direction['N'],direction['mu']))
 dabsolute=put('absolute',prod(a['density'],fy_sum(a['absolute_terms'],1),ddensity,fy_sum(dabs,1)))
 drelative=put('relative',prod(a['density'],fy_sum(a['relative_terms'],1),ddensity,fy_sum(drel,1)));daction=put('action',add(dabsolute,drelative));dHamiltonian=put('hamiltonian',neg(daction))
 fy_keep(label+'_cached_phase_vs_EOS_relative_coefficient_contact',sub(a['r'],eos['cached_intermediates']['r']),keep)
 trace_delta=fy_sum(fy_sum(prod(s['hi'],(a['q'][0].transpose(0,2,1),a['q'][1].transpose(0,2,1)),direction['hi'],(dq[0].transpose(0,2,1),dq[1].transpose(0,2,1))),2),1)
 put('measure_test_trace_contact',sub(dlm,scale(.5,trace_delta)));put('unit_constraint',add(dot(s['U'],s['uc'],direction['U'],direction['uc']),zero))
 dprojector=add(z((p,4,4)),prod(expand(s['uc'],(Ellipsis,slice(None),None)),expand(s['U'],(Ellipsis,None,slice(None))),expand(direction['uc'],(Ellipsis,slice(None),None)),expand(direction['U'],(Ellipsis,None,slice(None)))))
 put('projector_construction_contact',sub(direction['P'],dprojector));assert all(np.array_equal(x,y) for x,y in zip(a['density'],eos['value']['density']))
 return dict(value={n:a[n] for n in ('absolute','relative','action','hamiltonian')},delta=dict(absolute=dabsolute,relative=drelative,action=daction,hamiltonian=dHamiltonian),cached_value_provenance=provenance,new_direction_scope='original compact-chi at updated phase; normal value-test contact only',all_four_value_rows_require_separate_calls=True,test_first_derivative_coefficients_zero=True,relative_phase_included_once=True,cached_normal_value_action_recomputed=False,normal_R_Z_t_test_jet_directions_zero_by_phase_action=True,old_compact_chi_phase_contact_reused=False,physical_adoption=False)
