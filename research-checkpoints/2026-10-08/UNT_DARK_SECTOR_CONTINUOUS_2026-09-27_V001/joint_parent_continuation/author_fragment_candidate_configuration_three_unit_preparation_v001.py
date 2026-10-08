"""HELD three NEW unit conformal-jet responses and independent source majorants.
Definitions only. Globals np,P,FY/FS/FC160/FN253/CP195/OG49, reviewed mp_*.
Same closed candidate/current rates and updated phase values are supplied once;
only NEW direction algebra is evaluated. W/trace targets and sheet remain external.
This is a frozen coefficient proxy, never an exact DD Jacobian assertion.
"""
CONFIGURATION_UNIT_AUTHOR_DRAFT=True
CONFIGURATION_UNIT_AUTHORING_IN_PROGRESS=False

def qu_pair(label,x,keep):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):
  keep(label+'_'+word,np.asarray(a).copy());assert a.dtype==np.float64 and a.shape==x[0].shape and np.all(np.isfinite(a))
 return x

def qu_slice_column(value,selection):
 if isinstance(value,np.ndarray):
  axes=[i for i,n in enumerate(value.shape) if n==3784];assert len(axes)<=1
  key=[slice(None)]*value.ndim
  if axes:key[axes[0]]=selection
  return value[tuple(key)].copy()
 if isinstance(value,dict):return {n:qu_slice_column(x,selection) for n,x in value.items()}
 if isinstance(value,tuple):return tuple(qu_slice_column(x,selection) for x in value)
 if isinstance(value,list):return [qu_slice_column(x,selection) for x in value]
 return value

def candidate_configuration_unit_response(column,jet,Hbar,keep,check,label,stage_complete,test_complete):
 assert not CONFIGURATION_UNIT_AUTHOR_DRAFT and not CONFIGURATION_UNIT_AUTHORING_IN_PROGRESS
 assert callable(stage_complete) and callable(test_complete) and jet in (0,1,2)
 p=len(column['candidate']['c']['N']);assert 1<=p<=128
 provenance=dict(new_unit_response=True,old_q22_or_direction_action_replayed=False,same_candidate_provenance=column['provenance'],configuration_jet=jet,physical_adoption=False)
 unit=P.a_dd(np.zeros((p,3)));unit[0][:,jet]=1.;qu_pair(label+'_NEW_chi_unit',unit,keep)
 rho=P.a_slice(unit,(slice(None),0));grad=P.a_slice(unit,(slice(None),slice(1,None)))
 h,hj,I,mu=(column['york'][n] for n in ('h','h_spatial_jets','ih','mu'))
 four=P.a_mul64(4.,rho);gfour=P.a_mul64(4.,grad)
 direction=dict(h=fy_scale_matrix(four,h),ih=fy_scale_matrix(P.a_mul64(-4.,rho),I),mu=P.a_mul(P.a_mul64(6.,rho),mu),
  h_spatial_jets=P.a_add(P.a_mul(tuple(w[:,None,None,None] for w in four),hj),P.a_mul(tuple(w[...,None,None] for w in gfour),tuple(w[:,None] for w in h))),
  h_dot=P.a_dd(np.zeros((p,3,3))),u_jets=P.a_dd(np.zeros((p,4,3))),z_jets=P.a_dd(np.zeros((32,p,4,3))))
 for n,x in direction.items():qu_pair(label+'_NEW_direction_'+n,x,keep)
 stage_complete('DIRECTION',dict(chi_jets=unit,direction=direction),provenance)
 contact=finite_candidate_configuration_contact(column['candidate'],column['geometry'],column['gauge'],column['covectors'],column['mechanical'],direction,column['reference'],keep,label+'_NEW_configuration')
 stage_complete('CONTACT',dict(contact=contact),provenance)
 D={**contact['d'],**contact['dc']};D['mu']=contact['dc']['sqrt_h']
 eos=cached_updated_phase_eos_compact_chi(column['phase'],D,keep,label+'_updated_phase_direction')
 stage_complete('EOS',dict(eos=eos),provenance)
 if jet>0:assert all(np.all(w==0) for w in eos['delta']['p']),'Phase spatial-jet structural zero must hold in both words'
 curvature=finite_candidate_intrinsic_curvature(column['candidate'],contact,keep,label+'_NEW_intrinsic_curvature')
 stage_complete('CURVATURE',dict(curvature=curvature),provenance)
 roots=dict(galaxy_gamma=[None,None],radiation_energy=[]);ordinary_label=label+'_same_label_mean_direction'
 def root_keep(name,value):
  a=keep(name,value)
  for w,suffix in enumerate(('hi','lo')):
   if name==ordinary_label+'_galaxy_gamma_'+suffix:roots['galaxy_gamma'][w]=a.copy()
   if name==ordinary_label+'_radiation_current_energy_'+suffix:
    if w==0:roots['radiation_energy'].append([a.copy(),None])
    else:
     assert roots['radiation_energy'] and roots['radiation_energy'][-1][1] is None
     roots['radiation_energy'][-1][1]=a.copy()
  return a
 c=column['normal_c']
 ordinary=finite_fixed_canonical_ordinary_point(dict(h=c['h'],ih=c['ih'],delta_h=D['h'],delta_ih=D['ih']),dict(N=c['N'],beta=c['beta']),column['mean_labels'],root_keep,ordinary_label)
 assert len(roots['radiation_energy'])==column['mean_labels']['radiation_weights'][0].shape[0]
 assert all(isinstance(a,np.ndarray) and a.shape==(p,) for row in [roots['galaxy_gamma'],*roots['radiation_energy']] for a in row)
 roots=dict(galaxy_gamma=tuple(roots['galaxy_gamma']),radiation_energy=tuple(np.stack([a[w] for a in roots['radiation_energy']]) for w in (0,1)))
 for n,x in roots.items():qu_pair(label+'_NEW_ordinary_root_'+n,x,keep)
 stage_complete('ORDINARY',dict(ordinary=ordinary,ordinary_roots=roots),provenance)
 unsigned=candidate_configuration_current_CMC_unsigned(column['candidate'],contact,column['phase'],eos,Hbar,keep,label+'_source_current_CMC')
 stage_complete('CURRENT_UNSIGNED',dict(source_unsigned=unsigned),provenance)
 coefficients=P.a_dd(np.zeros((p,4,4)));normal_envelope=np.zeros((p,4,4));theta=None;rowrefs=[]
 for row in range(4):
  for test_jet,coordinate in enumerate((None,1,2,0)):
   f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3))
   if row==0:
    if coordinate is None:f[:]=1.
    else:df[:,coordinate]=1.
   elif coordinate is None:b[:,row-1]=1.
   else:db[:,coordinate,row-1]=1.
   tag=label+'_row%d_jet%d'%(row,test_jet)
   native=finite_candidate_native_EH_normal(column['candidate'],contact,curvature,f,df,b,db,Hbar,column['reference'],keep,tag+'_native_EH')
   if coordinate is None:
    phase=cached_updated_phase_normal_compact_chi(column['phase_normal_data'],column['phase_normal_prefixes'][row],column['normal_s'],c,D,eos,f,b,column['phase_normal_provenance'],keep,tag+'_updated_phase')
    prefix=column['phase_normal_prefixes'][row];phase_test={n:tuple(column['phase_normal_data'][prefix+NORMAL_NAMES[n]+'_'+w] for w in ('hi','lo')) for n in NORMAL_FIELDS}
    own=ordinary;mean_roots=roots
   else:
    phase=dict(value=dict(action=P.a_dd(np.zeros(p))),delta=dict(action=P.a_dd(np.zeros(p))),relative_phase_included_once=True)
    own=dict(value=dict(normal_density=P.a_dd(np.zeros((p,4)))),delta=dict(normal_density=P.a_dd(np.zeros((p,4)))))
    phase_test=None;mean_roots=None
   total=finite_candidate_total_normal(native,phase,own,f,b,keep,tag+'_once_counted_total')
   bound=candidate_configuration_normal_unsigned(column['candidate'],contact,native,curvature,column['phase'],eos,phase_test,mean_roots,column['mean_labels'],f,df,b,db,keep,tag+'_source_unsigned')
   for w in (0,1):coefficients[w][:,row,test_jet]=total['delta']['hamiltonian'][w]
   normal_envelope[:,row,test_jet]=bound['normal']
   current_theta=native['delta']['initial_CMC_density']
   if theta is None:theta=current_theta
   else:assert all(np.array_equal(a,bw) for a,bw in zip(theta,current_theta))
   qu_pair(tag+'_completed_normal_column',coefficients,keep);keep(tag+'_completed_normal_source_envelope',normal_envelope.copy())
   rowrefs.append(test_complete(row,test_jet,dict(native_value=native['value'],native_delta=native['delta'],phase_value=phase['value'],phase_delta=phase['delta'],total=total,source_unsigned=bound),provenance))
 dm=contact['delta_momenta'];compact=dict(native_density=dm['native_density'],metric_total_density=dm['metric_total_density'])
 response=dict(chi_jets=unit,direction={n:direction[n] for n in ('h_dot','u_jets','z_jets')},contact=dict(delta_momenta=compact),eos=dict(delta=dict(p=eos['delta']['p'])),normal_coefficients=coefficients,initial_CMC_density=theta,provenance=provenance)
 fields={**unsigned['fields'],'normal':normal_envelope}
 envelope=dict(fields=fields,same_unit_response_provenance=provenance,source_terms_before_output_cancellation=True,signed_response_magnitude_used_as_bound=False,upstream_EFT_error_bound_qualified=False,physical_adoption=False)
 signed=dict(mechanical=tuple(np.concatenate((compact['native_density'][w],compact['metric_total_density'][w]),axis=1) for w in (0,1)),phase=eos['delta']['p'],normal=coefficients,CMC=theta)
 for n,x in signed.items():
  qu_pair(label+'_completed_unit_'+n,x,keep);keep(label+'_completed_unit_source_unsigned_'+n,fields[n].copy())
  magnitude=mp_add(abs(x[0]),abs(x[1]),keep,label+'_'+n+'_signed_word_magnitude')
  gap=np.maximum(magnitude-fields[n],0.);keep(label+'_'+n+'_source_unsigned_enclosure_excess',gap.copy())
  check(label+'_'+n+'_source_unsigned_enclosure',gap,np.zeros_like(gap),fields[n])
 stage_complete('UNIT',dict(response=response,source_envelope=envelope),provenance)
 return dict(response=response,source_envelope=envelope,normal_test_records=rowrefs,W_trace_York_target_and_sheet_external=True,source_coefficient_law_only=True,exact_DD_Jacobian_or_uniform_association_qualified=False,physical_adoption=False)
