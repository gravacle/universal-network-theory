"""HELD whole-grid fixed-rate configuration and fixed-reference York JVP.
Definitions only. The containing caller authenticates four completed SAME225
columns, updated13764 EOS/normal caches, the current FY128 target cache, immutable
labels, basis, priors and epsilon before supplying any operands. No I/O, runner,
producer, current replay, inverse solve or finite-state adoption is provided.
Globals: np,P,N; exact selected FY128/FC160/FN247/CP195/OG49 definitions.
All new direction words and completed products pass through stack-first keep.
The action differentiates the declared continuous raw/formal chart, retaining
its true-geometry/serialization/anchor defects; binary64 rounding is not JVPed.
"""
WHOLE_CONFIGURATION_YORK_AUTHOR_DRAFT=True
WHOLE_CONFIGURATION_YORK_AUTHORING_IN_PROGRESS=False
WHOLE_CONFIGURATION_YORK_SOURCE_PINS={
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py':'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_fixed_label_finite_sheet_geometry_v002.py':'556bac0713c74947b0abece865bf7e74c3d3b212029af1248aa7dd0af525a661',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40'}

def cq_keep(name,pair,keep):
 assert isinstance(pair,tuple) and len(pair)==2
 keep(name+'_both_words',np.stack(pair).copy())
 for word,a in zip(('hi','lo'),pair):
  keep(name+'_'+word,np.asarray(a).copy());assert a.dtype==np.float64 and a.shape==pair[0].shape and np.all(np.isfinite(a))
 return pair

def cq_zero(shape):return P.a_dd(np.zeros(shape))

def cq_join(parts,axis=0):return tuple(np.concatenate([x[w] for x in parts],axis=axis) for w in (0,1))

def cq_six(tensor,keep,label):
 assert tensor[0].shape==tensor[1].shape==(15136,3,3)
 cq_keep(label+'_tensor',tensor,keep)
 cq_keep(label+'_serialized_asymmetry',P.a_sub(tensor,tuple(w.swapaxes(-1,-2) for w in tensor)),keep)
 rows=[]
 for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)):
  x=P.a_slice(tensor,(slice(None),i,j));rows.append(x if i==j else P.a_add(x,P.a_slice(tensor,(slice(None),j,i))))
 return cq_keep(label+'_covector_six',P.a_stack(rows,-1),keep)

def prepare_candidate_whole_configuration_york(columns,basis,sheet,current,priors,epsilon,provenance,keep,label):
 assert not WHOLE_CONFIGURATION_YORK_AUTHOR_DRAFT and not WHOLE_CONFIGURATION_YORK_AUTHORING_IN_PROGRESS
 assert len(columns)==4 and provenance and provenance['updated_phase_state_owner']==13764
 assert provenance['fixed_reference_longitudinal_chart'] is True and provenance['physical_adoption'] is False
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 masks=N.normal_test_mask();assert [int(np.count_nonzero(m)) for m in masks]==[3740,3740,3655,3740] and np.count_nonzero(P.scalar_mask())==3870
 for iq,col in enumerate(columns):
  assert col['provenance']['updated_phase_state_owner']==13764 and col['provenance']['same_candidate_geometry_and_current_mechanical_rates'] is True
  assert col['provenance']['fixed_reference_longitudinal_chart'] is True and col['provenance']['physical_adoption'] is False
  assert np.array_equal(col['candidate']['s']['R'],basis['R'][iq]) and len(col['phase_normal_prefixes'])==4
  y=col['york'];shapes=dict(h=(3784,3,3),ih=(3784,3,3),mu=(3784,),h_spatial_jets=(3784,2,3,3),T=(3784,3,3),kappa=(3784,),trace_part=(3784,),inverse_lam=(3784,),FY_target=(3784,3,3),target=(3784,3,3),tau=(3784,))
  for n,shape in shapes.items():assert y[n][0].shape==y[n][1].shape==shape;cq_keep(label+'_column%d_cached_York_'%iq+n,y[n],keep)
  for n in ('h','h_spatial_jets'):assert all(np.array_equal(a,b) for a,b in zip(y[n],col['geometry'][n]))
  cq_keep(label+'_column%d_owned_minus_FY_target_bridge'%iq,P.a_sub(y['target'],y['FY_target']),keep)
  kbound=np.sum((abs(y['h'][0])+abs(y['h'][1]))*(abs(y['ih'][0])+abs(y['ih'][1])),axis=(1,2));keep(label+'_column%d_kappa_envelope'%iq,kbound.copy())
  assert np.all(y['kappa'][0]-abs(y['kappa'][1])>2e-11*kbound)
  ref=col['york_reference'];assert ref['L_maps'][0].shape==ref['L_maps'][1].shape==(3784,3,3,3,3)
  assert ref['target_raising_inverse'].shape==(3784,3,3) and ref['mu_owned'].shape==(3784,) and np.all(ref['mu_owned']>0)
  s=col['phase']['s'];c=col['phase']['c']
  for n in ('g','hi','U','uc','P'):
   raw=P.a_dd(col['candidate']['s'][n]);assert all(np.array_equal(a,b) for a,b in zip(col['normal_s'][n],raw))
   if n in s:assert all(np.array_equal(a,b) for a,b in zip(col['normal_s'][n],s[n]))
  assert all(np.array_equal(a,b) for a,b in zip(col['normal_s']['phi'],s['phi']))
  for n in ('N','mu','ih','u'):assert all(np.array_equal(a,b) for a,b in zip(col['normal_c'][n],c[n]))
  for n in ('N','beta','h','ih','u','mu'):
   raw=P.a_dd(col['candidate']['c']['sqrt_h' if n=='mu' else n]);assert all(np.array_equal(a,b) for a,b in zip(col['normal_c'][n],raw))
  for n in ('p','H'):assert col['phase']['values'][n][0].shape==col['phase']['values'][n][1].shape==(3784,)
 for n,shape,mask in (('native',(33,3,87,45),np.broadcast_to(P.native_mask(),(33,3,87,45))),('metric',(6,87,45),P.metric_mask()),('phase',(87,45),P.scalar_mask())):
  for family,words in (('current',current),('prior',priors),('epsilon',epsilon)):
   assert words[n][0].shape==words[n][1].shape==shape and all(np.all(w[~mask]==0) for w in words[n]);cq_keep(label+'_unchanged_'+family+'_'+n,words[n],keep)
  cq_keep(label+'_epsilon_bookkeeping_gap_'+n,P.a_sub(P.a_sub(priors[n],current[n]),epsilon[n]),keep)
 assert sheet['provenance']['same_fixed_positions_and_labels'] is True and sheet['provenance']['physical_adoption'] is False
 return dict(columns=columns,basis=basis,sheet=sheet,current=current,priors=priors,epsilon=epsilon,provenance=provenance,
             configuration_dimension=18745,fixed_rate_partial_only=True,Legendre_test_response_feedback_included=False,physical_adoption=False)

def candidate_configuration_york_direction_jets(direction,basis,keep,label):
 mask=N.normal_test_mask();shapes=dict(chi=(87,45),W=(3,87,45),t=(87,45));masks=dict(chi=mask[0],W=mask[1:],t=P.scalar_mask())
 for n,shape in shapes.items():
  cq_keep(label+'_nodes_'+n,direction[n],keep);assert direction[n][0].shape==direction[n][1].shape==shape
  assert all(np.all(w[~masks[n]]==0) for w in direction[n]),'Inactive original coordinates must be zero in both words'
 normal=P.a_stack([direction['chi']]+[P.a_slice(direction['W'],i) for i in range(3)],0)
 extended=tuple(N.extend_normal_tests(w) for w in normal);trace=tuple(P.scalar_lift(w) for w in direction['t'])
 cq_keep(label+'_axis_and_boundary_extended_configuration',extended,keep);cq_keep(label+'_axis_extended_trace',trace,keep)
 sections=[]
 for iq in range(4):
  values=cq_zero((3784,4,3));tvalue=cq_zero((3784,))
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    nodal=P.a_slice(extended,(row,slice(di,86+di),slice(dj,44+dj)));nodal=tuple(w.reshape(3784) for w in nodal)
    for jet,hat in enumerate(N.normal_hat_jet(basis,iq,corner,row)):
     term=cq_keep(label+'_column%d_corner%d_row%d_jet%d_product'%(iq,corner,row,jet),P.a_mul64(hat.reshape(3784),nodal),keep)
     val=P.a_add(P.a_slice(values,(slice(None),row,jet)),term)
     for w in (0,1):values[w][:,row,jet]=val[w]
   nodal=P.a_slice(trace,(slice(di,86+di),slice(dj,44+dj)));nodal=tuple(w.reshape(3784) for w in nodal)
   tvalue=P.a_add(tvalue,P.a_mul64(basis['hats'][iq,corner,0].reshape(3784),nodal));cq_keep(label+'_column%d_current_trace_value'%iq,tvalue,keep)
   cq_keep(label+'_column%d_current_configuration_jets'%iq,values,keep)
  sections.append(dict(rho=P.a_slice(values,(slice(None),0,0)),rho_gradient=P.a_slice(values,(slice(None),0,slice(1,None))),W_jet=P.a_slice(values,(slice(None),slice(1,None),slice(None))),t=tvalue))
 return sections

def candidate_cached_york_target_direction(cache,reference,direction,keep,check,label):
 h,I,mu,hj,T,k,part,ilam=(cache[n] for n in ('h','ih','mu','h_spatial_jets','T','kappa','trace_part','inverse_lam'))
 dr,drg=direction['rho'],direction['rho_gradient'];put=lambda n,x:cq_keep(label+'_'+n,x,keep)
 dh=put('delta_h',fy_scale_matrix(P.a_mul64(4.,dr),h));dI=put('delta_ih',fy_scale_matrix(P.a_mul64(-4.,dr),I));dm=put('delta_mu',P.a_mul(P.a_mul64(6.,dr),mu))
 d4=P.a_mul64(4.,dr);g4=P.a_mul64(4.,drg)
 dhj=put('delta_h_spatial_jets',P.a_add(P.a_mul(tuple(w[:,None,None,None] for w in d4),hj),P.a_mul(tuple(w[...,None,None] for w in g4),tuple(w[:,None] for w in h))))
 dBW=fy_longitudinal_increment(reference,direction['W_jet'],keep,label+'_new_fixed_reference_W')
 dT=put('delta_T',P.a_add(fy_scale_matrix(P.a_mul64(-4.,dr),T),fy_scale_matrix(ilam,dBW)))
 dtau=put('delta_tau',P.a_mul64(reference['mu_owned'],direction['t']))
 dc=put('delta_h_T',P.a_add(fy_contract(dh,T),fy_contract(h,dT)));dk=put('delta_h_I',P.a_add(fy_contract(dh,I),fy_contract(h,dI)))
 numerator=put('trace_quotient_direction_numerator',P.a_sub(P.a_sub(dtau,dc),P.a_mul(part,dk)))
 dpart=fy_div(numerator,k,keep,label+'_new_trace_quotient_direction')
 delta=put('delta_target',P.a_add(P.a_add(dT,fy_scale_matrix(part,dI)),fy_scale_matrix(dpart,I)))
 trace=put('actual_trace_JVP',P.a_add(fy_contract(dh,cache['FY_target']),fy_contract(h,delta)));gap=put('actual_trace_JVP_minus_delta_tau',P.a_sub(trace,dtau))
 e=lambda a:abs(a[0])+abs(a[1]);bound=np.sum(e(dh)*e(cache['FY_target'])+e(h)*e(delta),axis=(1,2))+e(dtau)
 keep(label+'_actual_trace_JVP_uncancelled_envelope',bound.copy());check(label+'_actual_trace_JVP',gap[0]+gap[1],np.zeros(3784),bound)
 put('analytic_minus_formal_inverse_JVP',P.a_sub(dI,P.a_mul64(-1.,fy_mm(fy_mm(I,dh),I))))
 put('analytic_minus_formal_volume_JVP',P.a_sub(dm,P.a_mul(P.a_mul64(.5,mu),fy_contract(I,dh))))
 put('owned_target_anchor_trace_JVP_bridge',fy_contract(dh,P.a_sub(cache['target'],cache['FY_target'])))
 return dict(h=dh,ih=dI,mu=dm,h_spatial_jets=dhj,target=delta,tau=dtau,fixed_reference_B_varied=False,raw_TT_certificate_transferred=False)

def candidate_configuration_york_column(column,direction,Hbar,keep,check,label,test_complete=None):
 yd=candidate_cached_york_target_direction(column['york'],column['york_reference'],direction,keep,check,label+'_York')
 mechanical_direction={n:yd[n] for n in ('h','ih','mu','h_spatial_jets')}
 mechanical_direction.update(h_dot=cq_zero((3784,3,3)),u_jets=cq_zero((3784,4,3)),z_jets=cq_zero((32,3784,4,3)))
 contact=finite_candidate_configuration_contact(column['candidate'],column['geometry'],column['gauge'],column['covectors'],column['mechanical'],mechanical_direction,column['reference'],keep,label+'_NEW_configuration')
 D={**contact['d'],**contact['dc']};D['mu']=contact['dc']['sqrt_h']
 eos=cached_updated_phase_eos_compact_chi(column['phase'],D,keep,label+'_updated_phase_direction')
 curvature=finite_candidate_intrinsic_curvature(column['candidate'],contact,keep,label+'_NEW_intrinsic_curvature')
 c=column['normal_c'];ordinary=finite_fixed_canonical_ordinary_point(dict(h=c['h'],ih=c['ih'],delta_h=D['h'],delta_ih=D['ih']),dict(N=c['N'],beta=c['beta']),column['mean_labels'],keep,label+'_same_label_mean_direction')
 coeff=cq_zero((3784,4,4));theta=None;tests=[]
 for row in range(4):
  for jet,coordinate in enumerate((None,1,2,0)):
   f=np.zeros(3784);df=np.zeros((3784,4));b=np.zeros((3784,3));db=np.zeros((3784,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   tag=label+'_row%d_jet%d'%(row,jet)
   native=finite_candidate_native_EH_normal(column['candidate'],contact,curvature,f,df,b,db,Hbar,column['reference'],keep,tag+'_native_EH')
   if coordinate is None:
    phase=cached_updated_phase_normal_compact_chi(column['phase_normal_data'],column['phase_normal_prefixes'][row],column['normal_s'],c,D,eos,f,b,column['phase_normal_provenance'],keep,tag+'_updated_phase')
    own=ordinary
   else:
    phase=dict(value=dict(action=cq_zero((3784,))),delta=dict(action=cq_zero((3784,))),relative_phase_included_once=True)
    own=dict(value=dict(normal_density=cq_zero((3784,4))),delta=dict(normal_density=cq_zero((3784,4))))
   total=finite_candidate_total_normal(native,phase,own,f,b,keep,tag+'_once_counted_total')
   for w in (0,1):coeff[w][:,row,jet]=total['delta']['hamiltonian'][w]
   if theta is None:theta=native['delta']['initial_CMC_density']
   else:assert all(np.array_equal(a,bw) for a,bw in zip(theta,native['delta']['initial_CMC_density']))
   cq_keep(tag+'_completed_normal_coefficients',coeff,keep)
   tests.append(test_complete(row,jet,dict(native=native,phase=phase,ordinary=own,total=total)) if test_complete is not None else None)
 return dict(direction=mechanical_direction,contact=contact,eos=eos,target_direction=yd,curvature=curvature,normal_coefficients=coeff,initial_CMC_density=theta,
             tests=tests,relative_phase_count=1,ordinary_mean_count=1,normal_coordinate_order=('value','R','Z','t'),fixed_rate_partial_only=True,physical_adoption=False)

def candidate_configuration_sheet_direction(sheet,chi,normal_test,keep,check,label):
 indices=sheet['indices'];right=sheet['right_weight'];R=sheet['R'];n=len(R)
 assert indices.dtype==np.int64 and indices.shape==right.shape==R.shape==(n,) and np.all((indices>=0)&(indices<86)) and np.all((right>=0)&(right<=1))
 assert np.all(sheet['Z']==0) and np.all(R>0)
 rho=tuple(P.scalar_lift(w) for w in chi);dr=cq_zero((n,))
 for side,hat in ((0,1-right),(1,right)):
  operand=tuple(w[indices+side,0] for w in rho);cq_keep(label+'_side%d_fixed_label_chi'%side,operand,keep)
  dr=P.a_add(dr,P.a_mul64(hat,operand));cq_keep(label+'_current_fixed_label_direction',dr,keep)
 g=sheet['geometry'];dh=fy_scale_matrix(P.a_mul64(4.,dr),g['h']);dI=fy_scale_matrix(P.a_mul64(-4.,dr),g['ih']);dm=P.a_mul(P.a_mul64(6.,dr),g['mu'])
 for name,x in (('h',dh),('ih',dI),('mu',dm)):cq_keep(label+'_delta_'+name,x,keep)
 own=finite_fixed_canonical_ordinary_point(dict(h=g['h'],ih=g['ih'],delta_h=dh,delta_ih=dI),sheet['gauge'],sheet['labels'],keep,label+'_unchanged_sheet_labels')
 force=own['delta']['normal_density'];out=cq_zero((4,87,45));env=np.zeros((4,87,45));poly=cq_zero((n,4))
 for side,hat in ((0,1-right),(1,right)):
  for row in range(4):
   scale=R if row==1 else np.ones(n);val=cq_keep(label+'_side%d_row%d_force'%(side,row),P.a_mul64(hat,P.a_mul64(scale,P.a_slice(force,(slice(None),row)))),keep)
   ev=abs(hat*scale)*(abs(force[0][:,row])+abs(force[1][:,row]));mult=normal_test[row,indices+side,0]
   pv=P.a_add(P.a_slice(poly,(slice(None),row)),P.a_prod(hat*scale,mult))
   for w in (0,1):poly[w][:,row]=pv[w]
   for node in range(87):
    take=np.flatnonzero(indices+side==node)
    if len(take):
     subtotal=fy_sum(tuple(w[take] for w in val),0);joined=P.a_add(P.a_slice(out,(row,node,0)),subtotal)
     for w in (0,1):out[w][row,node,0]=joined[w]
     env[row,node,0]+=np.sum(ev[take]);cq_keep(label+'_current_sheet_nodal',out,keep)
 out=N.paired_restrict_normal_rows(out);env=N.restrict_normal_rows(env)
 selected=normal_test!=0;pn=(poly[0]!=0)|(poly[1]!=0)
 nodal_terms=cq_zero(out[0].shape);point_terms=cq_zero(force[0].shape)
 nt=P.a_mul64(normal_test[selected],tuple(w[selected] for w in out));pt=P.a_mul(tuple(w[pn] for w in poly),tuple(w[pn] for w in force))
 for w in (0,1):nodal_terms[w][selected]=nt[w];point_terms[w][pn]=pt[w]
 cq_keep(label+'_completed_nodal_terms',nodal_terms,keep);cq_keep(label+'_completed_point_terms',point_terms,keep)
 nodal=fy_sum(fy_sum(fy_sum(nodal_terms,2),1),0);direct=fy_sum(fy_sum(point_terms,1),0);gap=P.a_sub(nodal,direct)
 bound=np.asarray(np.sum(abs(normal_test)*env)+np.sum((abs(poly[0])+abs(poly[1]))*(abs(force[0])+abs(force[1])))).copy()
 for name,x in (('weak_normal',out),('functional_nodal',nodal),('functional_direct',direct),('functional_gap',gap)):cq_keep(label+'_'+name,x,keep)
 keep(label+'_functional_envelope',bound);check(label+'_polynomial_transpose',np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),bound)
 return dict(weak_normal=out,ordinary_direction=own,geometry_direction=dict(h=dh,ih=dI,mu=dm),fixed_labels_unchanged=True,initial_CMC_direct_zero=True)

def candidate_configuration_normal_CMC_direction(parts,basis,normal_test,scalar_test,keep,check,label):
 assert len(parts)==4 and basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 for part in parts:assert part['normal_coefficients'][0].shape==part['normal_coefficients'][1].shape==(3784,4,4) and part['initial_CMC_density'][0].shape==part['initial_CMC_density'][1].shape==(3784,)
 tv,sv=finite_candidate_test_polynomials(normal_test,scalar_test,basis,keep,label+'_independent_polynomials')
 value=cq_join([P.a_slice(p['normal_coefficients'],(slice(None),slice(None),slice(0,3))) for p in parts]);primary=cq_join([P.a_slice(p['normal_coefficients'],(slice(None),slice(None),3)) for p in parts]);density=cq_join([p['initial_CMC_density'] for p in parts]);weight=(basis['dv']/basis['R']).reshape(15136)
 for n,a in (('normal_point',value),('time_primary_action',P.a_mul64(-1.,primary)),('initial_CMC_density',density)):cq_keep(label+'_'+n,a,keep)
 weak=cq_keep(label+'_weak_normal',N.paired_scatter_normal(value,basis,label+'_NEW_normal'),keep);trace=cq_keep(label+'_weak_initial_CMC',P.dd_scalar_scatter(density,basis,keep,label+'_NEW_CMC'),keep)
 scalars={}
 for kind,test,nodal,point,polynomial in (('normal',normal_test,weak,value,tv),('CMC',scalar_test,trace,density,sv)):
  ns=test!=0;ps=(polynomial[0]!=0)|(polynomial[1]!=0)
  nt=cq_keep(label+'_'+kind+'_selected_nodal_product',P.a_mul64(test[ns],tuple(w[ns] for w in nodal)),keep)
  pt=cq_keep(label+'_'+kind+'_selected_point_product',P.a_mul(tuple(w[ps] for w in point),tuple(w[ps] for w in polynomial)),keep)
  nterms=cq_zero(nodal[0].shape);pterms=cq_zero(point[0].shape)
  for w in (0,1):nterms[w][ns]=nt[w];pterms[w][ps]=pt[w]
  cq_keep(label+'_'+kind+'_completed_nodal_terms',nterms,keep);cq_keep(label+'_'+kind+'_completed_point_terms',pterms,keep)
  node=fy_sum(fy_sum(fy_sum(nterms,2),1),0) if kind=='normal' else fy_sum(fy_sum(nterms,1),0)
  reduced=fy_sum(fy_sum(pterms,2),1) if kind=='normal' else pterms
  direct=fy_sum(P.a_mul64(weight,reduced),0);gap=P.a_sub(node,direct)
  magnitude=abs(point[0])+abs(point[1]);env=N.scatter_normal_envelope(magnitude,basis) if kind=='normal' else P.scalar_scatter(magnitude,basis)
  factor=weight[:,None,None] if kind=='normal' else weight
  bound=np.asarray(np.sum(abs(test)*env)+np.sum(factor*(abs(polynomial[0])+abs(polynomial[1]))*magnitude)).copy()
  for name,x in (('nodal',node),('direct',direct),('gap',gap)):scalars[kind+'_'+name]=cq_keep(label+'_'+kind+'_'+name,x,keep)
  keep(label+'_'+kind+'_uncancelled_envelope',bound);check(label+'_'+kind+'_polynomial_transpose',np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),bound)
 return dict(weak_normal=weak,weak_initial_CMC=trace,time_primary_action_coefficients=P.a_mul64(-1.,primary),functionals=scalars)

def candidate_configuration_canonical_functional(kind,field,weak,test,basis,keep,check,label):
 shape=field[0].shape;u=test.copy();poly=cq_zero(shape);envelope=np.zeros(shape)
 if kind=='native':
  assert shape==(33,15136,3) and u.shape==(33,3,87,45) and np.all(u[:,~P.native_mask()]==0)
  u[:,0,0,:]=0.;u[:,1,0,:]=u[:,1,1,:];u[:,1,:,0]=0.;u[:,2,0,:]=u[:,2,1,:]
 elif kind=='metric':
  assert shape==(15136,6) and u.shape==(6,87,45) and np.all(u[~P.metric_mask()]==0);u[:,0,:]=u[:,1,:];u[3:5,:,0]=0.
 else:
  assert kind=='phase' and shape==(15136,) and u.shape==(87,45) and np.all(u[~P.scalar_mask()]==0);u[0]=u[1]
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);R=basis['R'][iq]
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hat=basis['hats'][iq,corner,0].reshape(3784)
   if kind=='native':
    local=u[:,:,di:86+di,dj:44+dj].reshape(33,3,3784).transpose(0,2,1);factor=np.ones((3784,3));factor[:,2]=R**2
    term=P.a_mul64(factor,P.a_prod(hat[:,None],local));key=(slice(None),sl);eb=abs(local)*abs(hat[:,None])*abs(factor)
   elif kind=='metric':
    a,b,c,d,e,f=u[:,di:86+di,dj:44+dj].reshape(6,3784)
    local=P.a_stack([P.a_add(P.a_dd(a),P.a_prod(R**2,b)),P.a_dd(f),P.a_prod(R**2,a),P.a_prod(R,d),P.a_prod(R**3,c),P.a_prod(R**2,e)],1)
    term=P.a_mul64(hat[:,None],local);key=sl;eb=abs(hat[:,None])*np.stack((abs(a)+abs(R**2*b),abs(f),abs(R**2*a),abs(R*d),abs(R**3*c),abs(R**2*e)),1)
   else:
    local=u[di:86+di,dj:44+dj].reshape(3784);term=P.a_prod(hat,local);key=sl;eb=abs(hat*local)
   updated=P.a_add(P.a_slice(poly,key),term)
   for w in (0,1):poly[w][key]=updated[w]
   envelope[key]+=eb;cq_keep(label+'_current_independent_polynomial',poly,keep)
 weight=(basis['dv']/basis['R']).reshape(15136);scale=weight[None,:,None] if kind=='native' else weight[:,None] if kind=='metric' else weight
 ns=test!=0;ps=envelope>0
 for name,x in (('selected_nodal_operand',tuple(w[ns] for w in weak)),('selected_point_operand',tuple(w[ps] for w in field)),('selected_point_polynomial',tuple(w[ps] for w in poly))):cq_keep(label+'_'+name,x,keep)
 node=fy_sum(P.a_mul64(test[ns],tuple(w[ns] for w in weak)),0)
 product=cq_keep(label+'_selected_point_product',P.a_mul(tuple(w[ps] for w in poly),tuple(w[ps] for w in field)),keep)
 direct=fy_sum(P.a_mul64(np.broadcast_to(scale,shape)[ps],product),0);gap=P.a_sub(node,direct)
 bound=np.asarray(np.sum(abs(test)*(abs(weak[0])+abs(weak[1])))+np.sum(scale*envelope*(abs(field[0])+abs(field[1])))).copy()
 for name,x in (('nodal',node),('direct',direct),('gap',gap)):cq_keep(label+'_'+name,x,keep)
 keep(label+'_uncancelled_envelope',bound);check(label,np.asarray(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),bound)
 return dict(nodal=node,direct=direct,gap=gap,envelope=bound)

def candidate_whole_configuration_york_contact(prepared,direction,Hbar,probes,keep,check,label,column_complete=None,test_complete=None):
 assert not WHOLE_CONFIGURATION_YORK_AUTHOR_DRAFT and not WHOLE_CONFIGURATION_YORK_AUTHORING_IN_PROGRESS and prepared['physical_adoption'] is False
 basis=prepared['basis'];jets=candidate_configuration_york_direction_jets(direction,basis,keep,label+'_direction');parts=[];completed=[]
 assert np.isfinite(Hbar) and Hbar>0 and callable(keep) and callable(check)
 for n,shape in (('normal',(4,87,45)),('CMC',(87,45)),('native',(33,3,87,45)),('metric',(6,87,45)),('phase',(87,45))):
  a=keep(label+'_predeclared_probe_'+n,np.asarray(probes[n]).copy());assert a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a))
 assert np.all(probes['normal'][~N.normal_test_mask()]==0) and np.all(probes['CMC'][~P.scalar_mask()]==0)
 for iq,col in enumerate(prepared['columns']):
  callback=(lambda row,jet,data:test_complete(iq,row,jet,data)) if test_complete is not None else None
  part=candidate_configuration_york_column(col,jets[iq],Hbar,keep,check,label+'_column%d'%iq,callback)
  completed.append(column_complete(iq,part) if column_complete is not None else None)
  # Only row/action outputs survive the column boundary; detailed construction
  # operands are retained by keep and the containing stage callbacks.
  parts.append(dict(direction=part['direction'],contact=dict(delta_momenta=part['contact']['delta_momenta']),eos=dict(value={n:part['eos']['value'][n] for n in ('p','H')},delta={n:part['eos']['delta'][n] for n in ('p','H')}),target_direction=part['target_direction'],normal_coefficients=part['normal_coefficients'],initial_CMC_density=part['initial_CMC_density'],test_refs=part['tests']))
 native99=cq_join([p['contact']['delta_momenta']['native_density'] for p in parts]);native=tuple(w.reshape(15136,33,3).transpose(1,0,2) for w in native99)
 metric=cq_join([p['contact']['delta_momenta']['metric_total_density'] for p in parts]);phase=cq_join([p['eos']['delta']['p'] for p in parts]);target=cq_six(cq_join([p['target_direction']['target'] for p in parts]),keep,label+'_varying_target')
 weak=dict(native=cq_keep(label+'_Dchi_native_current',P.dd_native_scatter(native,basis,keep),keep),metric=cq_keep(label+'_Dchi_metric_current',P.dd_metric_scatter(metric,basis,keep),keep),phase=cq_keep(label+'_Dchi_literal_phase_current',P.dd_scalar_scatter(phase,basis,keep,label+'_literal_phase'),keep))
 target_weak=cq_keep(label+'_Dchi_W_t_metric_target',P.dd_metric_scatter(target,basis,keep),keep)
 canonical={**weak,'metric':cq_keep(label+'_D_metric_current_minus_varying_target',P.a_sub(weak['metric'],target_weak),keep)}
 delta_epsilon={n:cq_keep(label+'_D_target_minus_current_epsilon_'+n,P.a_mul64(-1.,a),keep) for n,a in canonical.items()}
 functions={}
 for name,kind,point,row,test in (('native','native',native,weak['native'],probes['native']),('metric','metric',metric,weak['metric'],probes['metric']),('phase','phase',phase,weak['phase'],probes['phase']),('York_target','metric',target,target_weak,probes['metric'])):
  functions[name]=candidate_configuration_canonical_functional(kind,point,row,test,basis,keep,check,label+'_'+name+'_polynomial_transpose')
 normal=candidate_configuration_normal_CMC_direction(parts,basis,probes['normal'],probes['CMC'],keep,check,label+'_normal_CMC')
 sheet=candidate_configuration_sheet_direction(prepared['sheet'],direction['chi'],probes['normal'],keep,check,label+'_fixed_label_sheet')
 total_normal=cq_keep(label+'_D_total_weak_normal',P.a_add(normal['weak_normal'],sheet['weak_normal']),keep)
 return dict(canonical_configuration_JVP=canonical,canonical_epsilon_configuration_JVP=delta_epsilon,current_configuration_JVP=weak,prepared_metric_target_JVP=target_weak,
             weak_normal_JVP=total_normal,weak_initial_CMC_JVP=normal['weak_initial_CMC'],time_primary_action_coefficients_JVP=normal['time_primary_action_coefficients'],
             phase_point_density_JVP=phase,mechanical_point_JVP=dict(native=native99,metric=metric),prepared_target_point_JVP=target,
             configuration_parts=parts,completed_column_refs=completed,normal_CMC=normal,sheet=sheet,functional_controls=functions,
             unchanged_current=prepared['current'],unchanged_priors=prepared['priors'],unchanged_epsilon=prepared['epsilon'],
             dimensions=dict(chi=3740,W=11135,total_canonical_trace=3870,configuration=18745,normal=14875,initial_CMC=3870),
             fixed_rate_partial_only=True,Legendre_test_response_feedback_included=False,mechanical_and_phase_temporal_actions_external=True,
             reference_B_or_fixed_charge_varied=False,all_four_sections_and_all_16_test_coefficients_present=True,
             global_inverse_rank_or_canonical_restoration_qualified=False,normal_CMC_or_physical_adoption=False)
