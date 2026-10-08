"""HELD NEW139 wholeweak configuration coefficient consumer.
Globals np,P,N and selected91/290/126/49/124/306 scalar/paired definitions.
No old configuration, current, EOS or normal producer is called. Three copied
chi-jet columns are a represented numerical proxy; complete cached FY chi/W/t
is varied by its unchanged quotient law. Sheet has one NEW unit derivative,
then a separate represented coefficient contraction at fixed original labels.
Original290 whole correction/unsigned and94->138->158 finite state remain
external authorities. Frozen feedback is not an exact reduced Newton derivative.
"""
Q_WHOLEWEAK_AUTHOR_DRAFT=True
Q_WHOLEWEAK_AUTHORING_IN_PROGRESS=False
Q_THREE_UNIT_CLOSURE=((None,None),(None,None,None),(None,None,'CLOSED'),(None,None,None))
Q_FINITE_CLOSURE=((None,None),(None,None,None),(None,None,'CLOSED'),(None,None,None))
Q_WHOLEWEAK_SOURCE_PINS={
 'author_fragment_candidate_configuration_jet_coefficient_v001.py':'f17c10f18e707529a589b1aae36704c423360fc4a92bbc7069972eb3e319d73b',
 'author_fragment_candidate_whole_configuration_york_contact_v001.py':'0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd',
 'author_fragment_candidate_shared_canonical_action_blocks_v001.py':'4ffdbf60dde14d9b87a7cb947dca7f61ec7e4ffe456653aed5298de27dbd59ee',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94',
 'author_fragment_candidate_literal_rate_normal_coefficients_v001.py':'d9b7953600bf41de36d562f19adaa25f94674ad3234c74cad4ef0b527cf7adbb'}


def qwc_pair(label,pair,keep,shape=None):
 assert isinstance(pair,tuple) and len(pair)==2
 keep(label+'_both_words',np.stack(pair).copy())
 for word,a in zip(('hi','lo'),pair):
  keep(label+'_'+word,a.copy());assert a.dtype==np.float64 and a.shape==pair[0].shape and np.all(np.isfinite(a)) and (shape is None or a.shape==shape)
 return pair


def qwc_positive_scalar_scatter(point,basis,keep,label):
 assert point.shape==(15136,) and np.all(np.isfinite(point)) and np.all(point>=0)
 out=np.zeros((87,45))
 for iq in range(4):
  weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);source=mp_mul(abs(weight),point[iq*3784:(iq+1)*3784].reshape(86,44),keep,label+'_q%d_weight'%iq)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   term=mp_mul(abs(basis['hats'][iq,corner,0]),source,keep,label+'_q%d_corner%d_term'%(iq,corner));key=(slice(di,86+di),slice(dj,44+dj))
   out[key]=mp_add(out[key],term,keep,label+'_q%d_corner%d_scatter'%(iq,corner));keep(label+'_completed_scalar_partial',out.copy())
 out[1]=mp_add(out[1],out[0],keep,label+'_axis_fold');out[0]=0
 keep(label+'_completed_scalar_unsigned',out.copy());return out


def qwc_york_unsigned(cache,reference,direction,keep,label):
 counter=0
 def tag(n):
  nonlocal counter
  counter+=1;return label+'_%05d_'%counter+n
 def mag(pair,n):
  qwc_pair(tag(n),pair,keep);return mp_add(abs(pair[0]),abs(pair[1]),keep,tag(n+'_magnitude'))
 add=lambda a,b:mp_add(a,b,keep,tag('add'));mul=lambda a,b:mp_mul(a,b,keep,tag('mul'));sum_=lambda a,k:mp_sum(a,k,keep,tag('sum'));mm=lambda a,b:mp_mm(a,b,keep,tag('mm'))
 h,I,T,part,ilam=(mag(cache[n],n) for n in ('h','ih','T','trace_part','inverse_lam'));r=mag(direction['rho'],'rho');W=mag(direction['W_jet'],'W_jet');t=mag(direction['t'],'t')
 maps=mag(reference['L_maps'],'fixed_L_maps');L=sum_(sum_(mul(maps,W[...,None,None]),2),1)
 raw=abs(reference['target_raising_inverse']);keep(tag('source_raw_raising_inverse'),raw.copy());keep(tag('source_raw_mu_owned'),reference['mu_owned'].copy())
 assert raw.shape==(3784,3,3) and np.all(np.isfinite(raw)) and np.all(reference['mu_owned']>0)
 BW=mul(abs(reference['mu_owned'])[:,None,None],mm(mm(raw,L),raw));dh=mul(mul(4.,r)[:,None,None],h);dI=mul(mul(4.,r)[:,None,None],I)
 dT=add(mul(mul(4.,r)[:,None,None],T),mul(ilam[:,None,None],BW));dtau=mul(abs(reference['mu_owned']),t)
 dc=add(sum_(sum_(mul(dh,T),2),1),sum_(sum_(mul(h,dT),2),1));dk=add(sum_(sum_(mul(dh,I),2),1),sum_(sum_(mul(h,dI),2),1))
 qwc_pair(tag('cached_kappa'),cache['kappa'],keep);lower=np.nextafter(cache['kappa'][0]-abs(cache['kappa'][1]),-np.inf);keep(tag('kappa_positive_lower'),lower.copy());assert np.all(np.isfinite(lower)) and np.all(lower>0)
 numerator=add(add(dtau,dc),mul(part,dk));dpart=mp_div(numerator,lower,keep,tag('trace_quotient_direction'))
 tensor=add(add(dT,mul(part[:,None,None],dI)),mul(dpart[:,None,None],I));six=[]
 for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2)):six.append(tensor[:,i,j] if i==j else add(tensor[:,i,j],tensor[:,j,i]))
 out=keep(label+'_completed_six_source_unsigned',np.stack(six,-1));assert out.shape==(3784,6) and np.all(np.isfinite(out)) and np.all(out>=0)
 return dict(tensor=tensor,six=out,source_operands_before_cancellation=True,actual_cached_kappa_and_quotient_retained=True,upstream_EFT_or_uniform_JVP_bound_qualified=False)


def qwc_prepare_sheet_unit(sheet,provenance,keep,label,complete_stage):
 assert not Q_WHOLEWEAK_AUTHOR_DRAFT and not Q_WHOLEWEAK_AUTHORING_IN_PROGRESS and callable(complete_stage)
 assert provenance['same_fixed_geometry_gauge_labels_and_positions'] is True and provenance['all_selected_seals_verified'] is True and provenance['physical_adoption'] is False
 g=sheet['geometry'];n=len(sheet['R']);dh=fy_scale_matrix(P.a_dd(np.full(n,4.)),g['h']);dI=fy_scale_matrix(P.a_dd(np.full(n,-4.)),g['ih'])
 roots=dict(galaxy_gamma=[None,None],radiation_energy=[]);ordinary_label=label+'_NEW_fixed_label_unit_direction'
 def root_keep(name,value):
  a=keep(name,value)
  for word,suffix in enumerate(('hi','lo')):
   if name==ordinary_label+'_galaxy_gamma_'+suffix:roots['galaxy_gamma'][word]=a.copy();keep(label+'_completed_galaxy_gamma_'+suffix,a.copy())
   if name==ordinary_label+'_radiation_current_energy_'+suffix:
    if word==0:roots['radiation_energy'].append([a.copy(),None])
    else:assert roots['radiation_energy'] and roots['radiation_energy'][-1][1] is None;roots['radiation_energy'][-1][1]=a.copy()
    keep(label+'_completed_radiation_energy_%d_'%(len(roots['radiation_energy'])-1)+suffix,a.copy())
  return a
 ordinary=finite_fixed_canonical_ordinary_point(dict(h=g['h'],ih=g['ih'],delta_h=dh,delta_ih=dI),sheet['gauge'],sheet['labels'],root_keep,ordinary_label)
 coefficient=qwc_pair(label+'_NEW_sheet_unit_force',ordinary['delta']['normal_density'],keep,(n,4));assert all(np.all(w[:,1:]==0) for w in coefficient)
 assert len(roots['radiation_energy'])==sheet['labels']['radiation_weights'][0].shape[0] and all(isinstance(a,np.ndarray) and a.shape==(n,) for row in [roots['galaxy_gamma'],*roots['radiation_energy']] for a in row)
 def mag(pair,nm):qwc_pair(label+'_unsigned_'+nm,pair,keep);return mp_add(abs(pair[0]),abs(pair[1]),keep,label+'_unsigned_'+nm+'_magnitude')
 def lower(pair,nm):qwc_pair(label+'_denominator_'+nm,pair,keep);v=np.nextafter(pair[0]-abs(pair[1]),-np.inf);keep(label+'_positive_lower_'+nm,v.copy());assert np.all(np.isfinite(v)) and np.all(v>0);return v
 cov=mag(sheet['labels']['galaxy_specific_covector'],'covector');edI=mag(dI,'unit_inverse_direction')
 quad=mp_sum(mp_mul(cov,mp_mv(edI,cov,keep,label+'_galaxy_mv'),keep,label+'_galaxy_product'),1,keep,label+'_galaxy_sum')
 gamma=tuple(roots['galaxy_gamma']);energy=mp_mul(mag(sheet['labels']['galaxy_mass_weight'],'mass'),mp_div(quad,2*lower(gamma,'gamma'),keep,label+'_galaxy_root_direction'),keep,label+'_galaxy_energy_direction')
 rays=mag(sheet['labels']['radiation_covectors'],'radiation_covectors');weights=mag(sheet['labels']['radiation_weights'],'radiation_weights')
 for j,root in enumerate(roots['radiation_energy']):
  quad=mp_sum(mp_mul(rays[j],mp_mv(edI,rays[j],keep,label+'_radiation_mv%d'%j),keep,label+'_radiation_product%d'%j),1,keep,label+'_radiation_sum%d'%j)
  term=mp_mul(weights[j],mp_div(quad,2*lower(tuple(root),'radiation%d'%j),keep,label+'_radiation_root_direction%d'%j),keep,label+'_radiation_energy_direction%d'%j);energy=mp_add(energy,term,keep,label+'_radiation_partial%d'%j)
 raw=np.zeros((n,4));raw[:,0]=energy;padded=mp_mul(raw,1.+(2048.*2.**-53)/(1.-2048.*2.**-53),keep,label+'_unit_proxy_padding');upper=mag(coefficient,'completed_unit_force')
 keep(label+'_unit_upper_minus_padded',upper-padded);assert np.all(upper<=padded),'Unit force exceeds predeclared independent source envelope'
 packet=dict(coefficient=coefficient,raw_source_unsigned=raw,represented_proxy_unsigned=padded,ordinary_roots=roots,provenance=provenance,original_positions_labels_and_budgets_unchanged=True,new_unit_not_old_sheet_action_replay=True,physical_adoption=False)
 seal=complete_stage('SHEET_UNIT',packet);assert isinstance(seal,dict) and seal.get('committed') is True;packet['committed_unit']=seal;return packet


def qwc_sheet_apply(sheet,unit,chi,keep,label):
 assert unit['physical_adoption'] is False and unit['committed_unit']['committed'] is True
 qwc_pair(label+'_chi_nodes',chi,keep,(87,45));assert all(np.all(w[~N.normal_test_mask()[0]]==0) for w in chi)
 indices=sheet['indices'];right=sheet['right_weight'];R=sheet['R'];n=len(R);rho=tuple(P.scalar_lift(w) for w in chi);dr=P.a_dd(np.zeros(n));er=np.zeros(n)
 assert indices.shape==right.shape==(n,) and indices.dtype==np.int64 and np.all((indices>=0)&(indices<86)) and np.all((right>=0)&(right<=1)) and np.all(sheet['Z']==0) and np.all(np.isfinite(R)) and np.all(R>0)
 for side,hat in ((0,1-right),(1,right)):
  operand=tuple(w[indices+side,0] for w in rho);qwc_pair(label+'_side%d_chi'%side,operand,keep,(n,));term=qwc_pair(label+'_side%d_product'%side,P.a_mul64(hat,operand),keep,(n,));dr=qwc_pair(label+'_side%d_partial'%side,P.a_add(dr,term),keep,(n,))
  magnitude=mp_add(abs(operand[0]),abs(operand[1]),keep,label+'_side%d_input_upper'%side);er=mp_add(er,mp_mul(abs(hat),magnitude,keep,label+'_side%d_unsigned_product'%side),keep,label+'_side%d_unsigned_add'%side)
 force=qwc_pair(label+'_NEW_unit_contracted_force',P.a_mul(unit['coefficient'],tuple(w[:,None] for w in dr)),keep,(n,4));ef=mp_mul(unit['represented_proxy_unsigned'],er[:,None],keep,label+'_uncancelled_force');out=P.a_dd(np.zeros((4,87,45)));envelope=np.zeros((4,87,45))
 for side,hat in ((0,1-right),(1,right)):
  for row in range(4):
   scale=R if row==1 else np.ones(n);val=qwc_pair(label+'_side%d_row%d_scatter_term'%(side,row),P.a_mul64(hat,P.a_mul64(scale,P.a_slice(force,(slice(None),row)))),keep,(n,));ev=mp_mul(abs(hat),mp_mul(abs(scale),ef[:,row],keep,label+'_row%d_scale'%row),keep,label+'_row%d_hat'%row)
   for node in range(87):
    take=np.flatnonzero(indices+side==node)
    if len(take):
     subtotal=fy_sum(tuple(w[take] for w in val),0);joined=P.a_add(P.a_slice(out,(row,node,0)),subtotal)
     for word in (0,1):out[word][row,node,0]=joined[word]
     envelope[row,node,0]=mp_add(envelope[row,node,0],mp_sum(ev[take],0,keep,label+'_source_scatter_sum'),keep,label+'_source_scatter_add');qwc_pair(label+'_completed_sheet_partial',out,keep)
 out=N.paired_restrict_normal_rows(out);envelope[:,1]=mp_add(envelope[:,1],envelope[:,0],keep,label+'_outward_axis_fold');envelope[:,0]=0;envelope[:,-1]=0;envelope[:,:,-1]=0;envelope[2,:,0]=0;keep(label+'_completed_sheet_unsigned',envelope.copy())
 return dict(weak_normal=out,positive=envelope,initial_CMC_and_time_primary_zero=True,MEAN_included=False,SHEET_included_once=True,source_coefficient_law_only=True,whole290_sheet_association_required=True)


def candidate_configuration_coefficient_wholeweak(prepared,direction,keep,check,label,chunk_loader,chunk_complete,column_complete):
 assert not Q_WHOLEWEAK_AUTHOR_DRAFT and not Q_WHOLEWEAK_AUTHORING_IN_PROGRESS and prepared['physical_adoption'] is False
 assert all(x is not None for closure in (Q_THREE_UNIT_CLOSURE,Q_FINITE_CLOSURE) for pin in closure for x in pin)
 assert prepared['unit_closure']==Q_THREE_UNIT_CLOSURE and prepared['finite_closure']==Q_FINITE_CLOSURE and prepared['all_selected_seals_verified'] is True
 assert prepared['same_NEW139_geometry_FULL_rates_updated_phase_and_fixed_reference'] is True and len(prepared['chunks'])==120 and len(prepared['york_columns'])==4
 assert callable(chunk_loader) and callable(chunk_complete) and callable(column_complete)
 basis=prepared['basis'];sections=candidate_configuration_york_direction_jets(direction,basis,keep,label+'_direction');fields={n:P.a_dd(np.zeros(shape)) for n,shape in dict(native=(15136,99),metric_current=(15136,6),phase=(15136,),normal=(15136,4,4),CMC=(15136,)).items()};bounds={n:np.zeros(x[0].shape) for n,x in fields.items()};targets=[];etargets=[];chunk_refs=[];column_refs=[]
 for ordinal,descriptor in enumerate(prepared['chunks']):
  iq,lo=divmod(ordinal,30);lo*=128;hi=min(lo+128,3784);part=chunk_loader(descriptor,iq,lo,hi);p=hi-lo;md=part['metadata'];q=part['prepared']
  assert md['column']==iq and md['lo']==lo and md['hi']==hi and md['chunk_ordinal']==ordinal and md['configuration_jet_order']==['rho','rho_R','rho_Z']
  assert md['same_candidate_provenance']==prepared['column_provenance'][iq] and md['original290_whole_correction_authority'] is True and md['exact_DD_linearity_or_uniform_association_qualified'] is False
  assert part['all_selected_seals_verified'] is True and q['points']==p and q['global_inverse_or_physical_adoption'] is False
  for name,shape in dict(mechanical=(p,105,3),phase=(p,3),normal=(p,4,4,3),CMC=(p,3)).items():qwc_pair(label+'_chunk%d_copied_'%ordinal+name,q['coefficients'][name],keep,shape);assert q['envelopes'][name].shape==shape
  rho=P.a_slice(sections[iq]['rho'],slice(lo,hi));gradient=P.a_slice(sections[iq]['rho_gradient'],slice(lo,hi));value=candidate_configuration_jet_point_action(q,rho,gradient,keep,label+'_chunk%d'%ordinal);positive=candidate_configuration_jet_point_positive(q,rho,gradient,keep,label+'_chunk%d_unsigned'%ordinal);positive['point']['native']=positive['point']['mechanical'][:,:99];positive['point']['metric_current']=positive['point']['mechanical'][:,99:]
  sl=slice(iq*3784+lo,iq*3784+hi)
  for name in fields:
   qwc_pair(label+'_chunk%d_completed_'%ordinal+name,value['point'][name],keep,fields[name][0][sl].shape)
   for word in (0,1):fields[name][word][sl]=value['point'][name][word]
   bounds[name][sl]=positive['point'][name]
  ref=chunk_complete(ordinal,dict(value=value,positive=positive,source=descriptor));assert isinstance(ref,dict) and ref.get('committed') is True;chunk_refs.append(ref)
  if hi==3784:
   yc=prepared['york_columns'][iq];target=candidate_cached_york_target_direction(yc['york'],yc['york_reference'],sections[iq],keep,check,label+'_column%d_NEW_full_York'%iq);e=qwc_york_unsigned(yc['york'],yc['york_reference'],sections[iq],keep,label+'_column%d_York_unsigned'%iq);targets.append(target['target']);etargets.append(e['six'])
   ref=column_complete(iq,dict(York=target,York_positive=e,chunk_refs=chunk_refs[30*iq:30*(iq+1)],same_candidate_provenance=prepared['column_provenance'][iq]));assert isinstance(ref,dict) and ref.get('committed') is True;column_refs.append(ref)
 for name,pair in fields.items():qwc_pair(label+'_completed_point_'+name,pair,keep);keep(label+'_completed_point_source_unsigned_'+name,bounds[name].copy())
 tensor=tuple(np.concatenate([x[word] for x in targets]) for word in (0,1));six=cs_york_covector_six(tensor,keep,label+'_full_York_target');target_weak=qwc_pair(label+'_varying_York_weak',P.dd_metric_scatter(six,basis,keep),keep)
 native=tuple(w.reshape(15136,33,3).transpose(1,0,2) for w in fields['native']);current=dict(native=qwc_pair(label+'_current_native_weak',P.dd_native_scatter(native,basis,keep),keep),metric=qwc_pair(label+'_current_metric_weak',P.dd_metric_scatter(fields['metric_current'],basis,keep),keep),phase=qwc_pair(label+'_current_phase_weak',P.dd_scalar_scatter(fields['phase'],basis,keep,label+'_phase'),keep))
 canonical={**current,'metric':qwc_pair(label+'_current_minus_full_York_target',P.a_sub(current['metric'],target_weak),keep)};epsilon={n:qwc_pair(label+'_epsilon_direction_'+n,P.a_mul64(-1.,x),keep) for n,x in canonical.items()}
 point=P.a_slice(fields['normal'],(slice(None),slice(None),slice(0,3)));normal=N.paired_scatter_normal(point,basis,label+'_normal');CMC=P.dd_scalar_scatter(fields['CMC'],basis,keep,label+'_CMC');primary=P.a_mul64(-1.,P.a_slice(fields['normal'],(slice(None),slice(None),3)))
 enative=bounds['native'].reshape(15136,33,3).transpose(1,0,2);enw,emw=candidate_mechanical_positive_scatter(enative,bounds['metric_current'],basis,keep,label+'_current_positive');_,eyw=candidate_mechanical_positive_scatter(np.zeros((33,15136,3)),np.concatenate(etargets),basis,keep,label+'_target_positive');epw=qwc_positive_scalar_scatter(bounds['phase'],basis,keep,label+'_phase_positive');enormal,eCMC=rnc_positive_normal_CMC_scatter(bounds['normal'],bounds['CMC'],basis,keep,label+'_normal_CMC_positive')
 sheet=qwc_sheet_apply(prepared['sheet'],prepared['sheet_unit'],direction['chi'],keep,label+'_sheet');normal=qwc_pair(label+'_normal_plus_sheet_once',P.a_add(normal,sheet['weak_normal']),keep,(4,87,45));enormal=mp_add(enormal,sheet['positive'],keep,label+'_normal_plus_sheet_unsigned')
 metric_positive=mp_add(emw,eyw,keep,label+'_metric_current_plus_target_unsigned');packed=qwc_pair(label+'_canonical_packed',P.pack_fields(canonical['native'],canonical['metric']),keep,(403340,))
 return dict(canonical=canonical,canonical_epsilon_JVP=epsilon,mechanical_packed=packed,phase=canonical['phase'],normal=normal,CMC=CMC,time_primary=primary,positive=dict(native=enw,metric=metric_positive,phase=epw,normal=enormal,CMC=eCMC,time_primary=bounds['normal'][:,:,3]),current_only_configuration_JVP=current,varying_metric_target_JVP=target_weak,point_fields=fields,completed_chunks=chunk_refs,completed_columns=column_refs,MEAN_in_q3_once=True,SHEET_once=True,W_t_direct_current_normal_CMC_time_primary_zero=True,full_chi_W_t_York_included=True,frozen_feedback_derivative=True,original290_whole_correction_unsigned_and_fresh_finite_authority_required=True,arbitrary_DD_association_or_reduced_Newton_or_physical_adoption=False)
