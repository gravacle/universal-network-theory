"""HELD value-only phase replacement on the CLOSED finite0 configuration.
Globals np,json,P,N,bind,bind_record,thin,fy_keep/fy_sum,fs_* and reviewed62
candidate_phase_normal_stress plus239 finite_candidate_test_polynomials.
No old native/EH/ordinary/current/CMC or EOS producer is called. All four
normal row VALUE coefficients change; R/Z/t test coefficients stay unchanged.
The finite116 temporal-step delta is NOT a compact-chi/configuration tangent.
Containing callbacks authenticate/read selected CLOSED members, seal numeric
partials and control triplets exclusively, then clear only completed captures.
"""
PHASE_NORMAL_JOIN_AUTHOR_DRAFT=True
PHASE_NORMAL_JOIN_AUTHORING_IN_PROGRESS=False
NORMAL_SOURCE=('cross_u_finite0_state_normal_recovery_v005.py','8f9b528e1da5114b148585799e902cdaaa14a6ac2af60e7deff9a85375792be2')
NORMAL_RESULT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RESULT.json','ea3c323511febbd278217e19ce8364d0e09186edc6d1d5c61bf87fb5fa211954','FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED')
NORMAL_RECEIPT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RECEIPT.json','9e26a9c77d2ec7f023344c8399645cb94dc3252f2ab0dd744e14469050a30955','CLOSED')
NORMAL_PROOF=('ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_V001.json','47ea566a93b34846c5861f7b184f80a73ac1ddd74f52bc891a7160b0a57fdab1','ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED')
FINITE_SOURCE=('cross_u_candidate_finite_phase_state_evaluation_v002.py','0fe81190f0968ce599a001e5c65459abc176da4f5c38684072cbc70c1a2ff54b')
FINITE_RESULT=('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_RESULT.json','4ac3ff59a1fb825151f603cb1422771cf8648c6e9b09062e7dba849cb28635ec','CANDIDATE_FINITE_PHASE_STATE_AND_LITERAL_CURRENT_MEASURED')
FINITE_RECEIPT=('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_RECEIPT.json','8e707d334fc62f1f9b585460aecb1bda3385f21515ea3a142b56acc3c8289278','CLOSED')
FINITE_PROOF=('ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_V001.json','f97d469bf7852bdd72b2abbc093669070b4081d24feb00c1373fce6279600ebc','ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_VERIFIED')

def phase_join_closed(source,result,receipt,proof):
 for ref in (source,result,receipt,proof):assert all(x is not None for x in ref);bind(ref[0],ref[1])
 r,rc,p=(json.loads(P.path(ref[0]).read_text()) for ref in (result,receipt,proof))
 assert r['status']==result[2] and rc['status']==receipt[2] and p['status']==proof[2]
 assert r['owner']==rc['owner']==p['owner'] and r['owner']['source_sha256']==p['source_sha256']==source[1]
 assert rc['result_sha256']==p['result_sha256']==result[1] and p['receipt_sha256']==receipt[1] and rc['error_sha256'] is None
 assert p['naturally_closed'] is True and type(p['exit_code']) is int and p['exit_code']==0 and p['all_input_seals_verified'] is p['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification']==p['qualification'] and all(x is False for x in r['qualification'].values())
 stem=result[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 return r,rc

def fixed_geometry_phase_normal_join_admission():
 assert not PHASE_NORMAL_JOIN_AUTHOR_DRAFT and not PHASE_NORMAL_JOIN_AUTHORING_IN_PROGRESS
 main,mrc=phase_join_closed(NORMAL_SOURCE,NORMAL_RESULT,NORMAL_RECEIPT,NORMAL_PROOF);finite,frc=phase_join_closed(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_PROOF)
 mc,fc=main['case'],finite['case'];assert len(mc['columns'])==len(fc['columns'])==4 and fc['configuration_unchanged'] is fc['instantaneous_spatial_phase_unchanged'] is fc['original_target_words_unchanged'] is True
 assert fc['linear_response_admitted'] is True and fc['finite_candidate_admitted'] is fc['phase_charge_restored'] is fc['physical_adoption'] is False
 original=bind_record(main['inherited_success_records'][0]);basis=bind_record(main['inherited_success_records'][1]);assert thin(original)==fc['original_input'] and original['metadata']['kind']=='owned_current_mechanical_time_words_reference_finite_candidate' and basis['metadata']['kind']=='unchanged_registered_E_F_normal_scalar_basis'
 loads=bind_record(mc['loads']);sheet=bind_record(mc['sheet']);current=bind_record(fc['current']);assert loads['metadata']['columns']==[thin(q) for q in mc['columns']] and loads['metadata']['sheet']==thin(sheet)
 assert loads['metadata']['relative_phase_count']==1 and loads['metadata']['ordinary_sheet_and_reference_mean_counted_once'] is True and current['metadata']['columns']==[thin(q) for q in fc['columns']]
 assert current['metadata']['charge_target_words_unchanged'] is True and current['metadata']['finite_charge_admission_performed'] is False and current['metadata']['unchanged_target']==fc['original_literal_phase_charge']==thin(original['metadata']['refs']['phase_loads'])
 columns=[]
 for iq,(old,new) in enumerate(zip(mc['columns'],fc['columns'])):
  old,new=bind_record(old),bind_record(new);state=bind_record(old['metadata']['candidate_state']);om,nm=old['metadata'],new['metadata']
  assert om['column']==nm['column']==state['metadata']['column']==iq and thin(state)==nm['state']==nm['candidate_provenance']['source_candidate']['state']
  assert nm['candidate_provenance']['source_candidate']['input']==thin(original) and nm['strict_EOS_domain_passed'] is True and nm['original_phase_targets_unchanged'] is True
  assert nm['candidate_provenance']['geometry_policy']=='saved raw225 geometry pairs with zero low words; paired phase update retained' and nm['candidate_provenance']['fresh_direction_scope']=='same temporal phase step only; all configuration directions zero'
  assert om['normal_coordinate_order']==['value','R','Z','t'] and om['relative_phase_count']==om['ordinary_mean_count']==1 and len(om['normal_test_refs'])==16
  rows=[]
  for row in range(4):
   q=bind_record(om['normal_test_refs'][4*row]);qm=q['metadata'];assert qm['column']==iq and qm['row']==row and qm['jet']==0 and qm['candidate_state']==thin(state) and qm['relative_phase_count']==qm['ordinary_mean_count']==1
   assert q in main['checkpoints'] and qm['owner']==main['owner'] and qm['failed'] is False;rows.append(q)
  assert old in main['checkpoints'] and new in finite['checkpoints'] and om['owner']==main['owner'] and nm['owner']==finite['owner'] and om['failed'] is nm['failed'] is False
  columns.append(dict(old=old,new=new,state=state,phase_rows=rows))
 for r,rc,refs in ((main,mrc,[loads,sheet]+[q['old'] for q in columns]+[v for q in columns for v in q['phase_rows']]),(finite,frc,[current]+[q['new'] for q in columns])):
  for ref in refs:assert rc['output_sha256'][ref['file']]==ref['sha256'] and rc['output_sha256'][ref['commit_file']]==ref['commit_sha256'] and ref['metadata']['physical_adoption'] is False
 return dict(columns=columns,input=original,basis=basis,loads=loads,sheet=sheet,current=current,prior=bind_record(fc['original_literal_phase_charge']),normal_terminal=(NORMAL_SOURCE,NORMAL_RESULT,NORMAL_RECEIPT,NORMAL_PROOF),finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_PROOF),physical_adoption=False)

def phase_join_pair(data,name,shape,keep,label):
 pair=(data[name+'_hi'].copy(),data[name+'_lo'].copy());keep(label+'_both_words',np.stack(pair).copy())
 assert all(a.shape==shape and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in pair);return fy_keep(label,pair,keep)

def phase_join_add(old,increment,keep,label):
 fy_keep(label+'_old',old,keep);fy_keep(label+'_increment',increment,keep);new=fy_keep(label+'_new',P.a_add(old,increment),keep);words=[]
 for ordinal,term in enumerate((old[0],old[1],increment[0],increment[1],-new[0],-new[1])):
  accumulator=term;next_words=[]
  for word in words:accumulator,low=P.a_sum(accumulator,word);next_words.append(low)
  words=next_words+[accumulator];keep(label+'_exact_addition_step%d'%ordinal,np.stack(words).copy())
 keep(label+'_exact_six_word_addition_defect',np.stack(words).copy());return new

def phase_join_phase_envelope(s,c,eos,f,b,keep,label):
 a=lambda pair:abs(pair[0])+abs(pair[1]);g,I,U,uc,Pj,phi=(a(s[n]) for n in ('g','hi','U','uc','P','phi'));N,mu,h,beta=(a(c[n]) for n in ('N','mu','h','beta'))
 nl=c['N'][0]-abs(c['N'][1]);xl=eos['X'][0]-abs(eos['X'][1]);assert np.all(nl>0) and np.all(xl>0)
 hb=np.einsum('pij,pj->pi',h,abs(b));q=np.zeros_like(g);q[:,0,0]=2*N*abs(f)+2*np.einsum('pi,pi->p',beta,hb);q[:,0,1:]=q[:,1:,0]=hb
 It=np.einsum('pai,pij,pjb->pab',I,q,I);eta0=U[:,0]*abs(f)/nl;eta=np.column_stack((eta0,U[:,0,None]*abs(b)+beta*eta0[:,None]))
 uct=np.einsum('pab,pb->pa',q,U)+np.einsum('pab,pb->pa',g,eta);Pt=uct[:,:,None]*U[:,None,:]+uc[:,:,None]*eta[:,None,:]
 r=np.einsum('pab,pb->pa',Pj,phi);rt=np.einsum('pab,pb->pa',Pt,phi);lm=abs(f)/nl;density=N*mu
 absolute=density*(a(eos['PX'])*np.einsum('pa,pab,pb->p',phi,It,phi)/(2*xl)+a(eos['pressure'])*lm)
 relative=density*(.5*np.einsum('pa,pab,pb->p',r,It,r)+np.einsum('pa,pab,pb->p',r,I,rt)+.5*np.einsum('pa,pab,pb->p',r,I,r)*lm)
 for n,x in (('metric_test',q),('inverse_test',It),('native_test',eta),('projector_test',Pt),('relative_phase',r),('relative_test',rt),('absolute',absolute),('relative',relative),('total',absolute+relative)):keep(label+'_positive_'+n,np.asarray(x).copy());assert np.all(x>=0)
 return absolute+relative

def phase_join_functional(point,weak,sheet,basis,test,tv,epoint,keep,check,label):
 terms=P.a_dd(np.zeros_like(weak[0]));direct=P.a_dd(np.zeros_like(point[0]));sheet_terms=P.a_dd(np.zeros_like(sheet[0]));nodal=test!=0;selected=(tv[0]!=0)|(tv[1]!=0)
 for n,array in (('test',test),('selected_point_mask',selected)):keep(label+'_'+n,np.asarray(array).copy())
 for name,target,left,right,mask,raw in (('nodal',terms,test,weak,nodal,True),('point',direct,point,tv,selected,False),('sheet',sheet_terms,test,sheet,nodal,True)):
  r=(right[0][mask],right[1][mask]);fy_keep(label+'_'+name+'_selected_right',r,keep)
  if raw:keep(label+'_'+name+'_selected_left',left[mask].copy());prod=P.a_mul64(left[mask],r)
  else:l=(left[0][mask],left[1][mask]);fy_keep(label+'_'+name+'_selected_left',l,keep);prod=P.a_mul(l,r)
  for word in (0,1):target[word][mask]=prod[word]
  fy_keep(label+'_'+name+'_product',target,keep)
 nodal_value=fy_sum(fy_sum(fy_sum(terms,2),1),0);sheet_value=fy_sum(fy_sum(fy_sum(sheet_terms,2),1),0);weight=(basis['dv']/basis['R']).reshape(15136)
 point_value=fy_sum(P.a_mul64(weight,fy_sum(fy_sum(direct,2),1)),0);expected=P.a_add(point_value,sheet_value);gap=P.a_sub(nodal_value,expected)
 en=N.scatter_normal_envelope(epoint,basis);bound=np.sum(abs(test)*(en+abs(sheet[0])+abs(sheet[1])))+np.sum(weight[:,None,None]*(abs(tv[0])+abs(tv[1]))*epoint)+np.sum(abs(test)*(abs(sheet[0])+abs(sheet[1])))
 for n,x in (('nodal',nodal_value),('direct_volume',point_value),('inherited_sheet_nodal',sheet_value),('gap',gap)):fy_keep(label+'_'+n,x,keep)
 keep(label+'_uncancelled_envelope',np.asarray(bound).copy());check(label+'_polynomial_transpose',(gap[0]+gap[1]).copy(),np.asarray(0.).copy(),np.asarray(bound).copy())
 return dict(nodal=nodal_value,direct_volume=point_value,inherited_sheet_nodal=sheet_value,gap=gap,envelope=np.asarray(bound).copy())

def join_fixed_geometry_phase_normal_values(admitted,read_closed,seal_completed,clear_completed,keep,check,label):
 assert not PHASE_NORMAL_JOIN_AUTHOR_DRAFT and not PHASE_NORMAL_JOIN_AUTHORING_IN_PROGRESS and admitted['physical_adoption'] is False
 assert admitted['normal_terminal']==(NORMAL_SOURCE,NORMAL_RESULT,NORMAL_RECEIPT,NORMAL_PROOF) and admitted['finite_terminal']==(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_PROOF)
 basis=read_closed(admitted['basis'],('R','dv','hats'));assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 for n,a in basis.items():keep(label+'_copied_basis_'+n,a.copy())
 header=seal_completed('JOIN_INPUT',dict(kind='closed_fixed_geometry_phase_replacement_sources',normal_terminal=admitted['normal_terminal'],finite_terminal=admitted['finite_terminal'],original_input=thin(admitted['input']),basis=thin(admitted['basis']),old_loads=thin(admitted['loads']),old_sheet=thin(admitted['sheet']),new_phase_current=thin(admitted['current']),old_columns=[thin(q['old']) for q in admitted['columns']],new_phase_columns=[thin(q['new']) for q in admitted['columns']],scope='normal values only; no new configuration derivative',physical_adoption=False));clear_completed()
 increments=[];joined=[];bounds=[];column_refs=[]
 for iq,source in enumerate(admitted['columns']):
  shapes=dict(g=(3784,4,4),hi=(3784,4,4),U=(3784,4),uc=(3784,4),P=(3784,4,4),phi=(3784,4),N=(3784,),mu=(3784,),h=(3784,3,3),beta=(3784,3));names={n:'completed_candidate_'+('s_' if n in ('g','hi','U','uc','P','phi') else 'c_')+('sqrt_h' if n=='mu' else n) for n in shapes}
  raw=read_closed(source['state'],tuple(names.values()));values={}
  for n,name in names.items():a=keep(label+'_column%d_copied_'%iq+name,raw[name].copy());assert a.shape==shapes[n] and a.dtype==np.float64;values[n]=P.a_dd(a)
  prefix='NEW_finite_phase_column%d_'%iq;f_names=tuple(prefix+'phase_covector_'+n+'_'+w for n in ('before','increment','updated') for w in ('hi','lo'))+tuple(prefix+'NEW_invariant_'+n+'_'+w for n in ('invariant_X','pressure','PX') for w in ('hi','lo'))+tuple(prefix+'saved_'+names[n] for n in ('hi','P','phi','U','uc','N','mu'))
  finite=read_closed(source['new'],f_names)
  for n in ('hi','P','phi','U','uc','N','mu'):a=keep(label+'_column%d_finite_geometry_copy_'%iq+n,finite[prefix+'saved_'+names[n]].copy());assert np.array_equal(a,raw[names[n]])
  before=phase_join_pair(finite,prefix+'phase_covector_before',(3784,4),keep,label+'_column%d_phi_before'%iq);step=phase_join_pair(finite,prefix+'phase_covector_increment',(3784,4),keep,label+'_column%d_phi_step'%iq);changed=phase_join_pair(finite,prefix+'phase_covector_updated',(3784,4),keep,label+'_column%d_phi_updated'%iq)
  assert all(np.array_equal(a,b) for a,b in zip(before,values['phi'])) and all(np.all(a[:,1:]==0) for a in step) and all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(before,changed));values['phi']=changed
  eos_values={n:phase_join_pair(finite,prefix+'NEW_invariant_'+('invariant_X' if n=='X' else n),(3784,),keep,label+'_column%d_fresh_EOS_'%iq+n) for n in ('X','pressure','PX')}
  eos=dict(value=eos_values,delta={n:P.a_dd(np.zeros(3784)) for n in eos_values},candidate_pressure_recomputed_from_invariant=True);direction={n:P.a_dd(np.zeros(shape)) for n,shape in shapes.items()};s={n:values[n] for n in ('g','hi','U','uc','P','phi')};c={n:values[n] for n in ('N','mu','h','beta')}
  saved=read_closed(source['old'],tuple(n+'_'+w for n in ('value_normal_coefficients','value_initial_CMC_density','NEW_current_momentum_native_density','NEW_current_momentum_metric_native_density','NEW_current_momentum_metric_EH_density','NEW_current_momentum_metric_total_density','NEW_current_momentum_K','NEW_current_momentum_Ktrace') for w in ('hi','lo')))
  old=phase_join_pair(saved,'value_normal_coefficients',(3784,4,4),keep,label+'_column%d_old_coefficients'%iq);out=tuple(a.copy() for a in old);increment=P.a_dd(np.zeros((3784,4,3)));envelope=np.zeros((3784,4,3));rows=[]
  for row,ref in enumerate(source['phase_rows']):
   rowlabel=label+'_column%d_row%d'%(iq,row);rprefix='row%d_jet0_phase_'%row
   rn=tuple(rprefix+n+'_'+w for n in ('absolute_action','relative_action','action_coefficient','EOS_X','EOS_pressure','EOS_PX') for w in ('hi','lo'))+tuple(n+'_'+w for n in ('completed_row%d_jet0_native_EH_value_action'%row,'completed_row%d_jet0_total_value_hamiltonian'%row,'row%d_jet0_total_once_counted_ordinary_Hamiltonian'%row) for w in ('hi','lo'))
   data=read_closed(ref,rn);old_actions={n:phase_join_pair(data,rprefix+n,(3784,),keep,rowlabel+'_old_phase_'+n) for n in ('absolute_action','relative_action','action_coefficient')};old_eos={n:phase_join_pair(data,rprefix+'EOS_'+n,(3784,),keep,rowlabel+'_old_EOS_'+n) for n in ('X','pressure','PX')}
   old_native=phase_join_pair(data,'completed_row%d_jet0_native_EH_value_action'%row,(3784,),keep,rowlabel+'_unchanged_native_EH_action');ordinary=phase_join_pair(data,'row%d_jet0_total_once_counted_ordinary_Hamiltonian'%row,(3784,),keep,rowlabel+'_unchanged_ordinary_Hamiltonian');old_H=phase_join_pair(data,'completed_row%d_jet0_total_value_hamiltonian'%row,(3784,),keep,rowlabel+'_old_total_H');assert all(np.array_equal(a,b[:,row,0]) for a,b in zip(old_H,old))
   f=np.ones(3784) if row==0 else np.zeros(3784);b=np.zeros((3784,3))
   if row>0:b[:,row-1]=1.
   old_s=dict(s,phi=before);eold=phase_join_phase_envelope(old_s,c,old_eos,f,b,keep,rowlabel+'_old_phase');enew=phase_join_phase_envelope(s,c,eos_values,f,b,keep,rowlabel+'_new_phase')
   new=candidate_phase_normal_stress(s,c,direction,eos,f,b,keep,rowlabel+'_NEW_literal_phase');assert new['relative_phase_included_once'] is new['test_first_derivative_coefficients_zero'] is True
   for n,a in new['value'].items():fy_keep(rowlabel+'_NEW_phase_'+n,a,keep)
   replacement=fy_keep(rowlabel+'_old_phase_action_minus_NEW_phase_action',P.a_sub(old_actions['action_coefficient'],new['value']['action']),keep);value=phase_join_add(old_H,replacement,keep,rowlabel+'_Hamiltonian_join')
   for word in (0,1):out[word][:,row,0]=value[word];increment[word][:,row,0]=replacement[word]
   envelope[:,row,0]=eold+enew;keep(rowlabel+'_uncancelled_replacement_envelope',envelope[:,row,0].copy())
   reconstructed=P.a_sub(P.a_add(tuple(-a for a in old_native),ordinary),new['value']['action']);fy_keep(rowlabel+'_joined_minus_reused_terms_and_NEW_phase_contact',P.a_sub(value,reconstructed),keep)
   fy_keep(rowlabel+'_completed_column_coefficients',out,keep);fy_keep(rowlabel+'_completed_column_increment',increment,keep)
   record=seal_completed('PHASE_NORMAL_ROW',dict(kind='NEW_literal_phase_all_four_normal_value_replacement',column=iq,row=row,jet=0,input=thin(header),old_normal_test=thin(ref),state=thin(source['state']),finite_phase_column=thin(source['new']),relative_phase_count=1,ordinary_mean_count=1,delta_EOS_used=False,new_configuration_contact=False,all_physical_qualifications_inherited_false=True,physical_adoption=False));rows.append(thin(record));clear_completed()
  assert all(np.array_equal(a[:,:,1:],b[:,:,1:]) for a,b in zip(out,old))
  for n,a in saved.items():keep(label+'_column%d_unchanged_'%iq+n,a.copy())
  fy_keep(label+'_column%d_NEW_normal_coefficients'%iq,out,keep);fy_keep(label+'_column%d_phase_replacement'%iq,increment,keep);keep(label+'_column%d_uncancelled_phase_replacement'%iq,envelope.copy())
  record=seal_completed('NORMAL_JOIN_COLUMN',dict(kind='NEW_phase_updated_normal_values_and_action_proven_unchanged_words',column=iq,input=thin(header),old_column=thin(source['old']),state=thin(source['state']),finite_phase_column=thin(source['new']),phase_normal_rows=rows,normal_coordinate_order=['value','R','Z','t'],test_R_Z_t_coefficients_bitwise_unchanged=True,initial_CMC_and_mechanical_momenta_bitwise_unchanged=True,old_compact_chi_contact_not_reused_as_new=True,relative_phase_count=1,ordinary_mean_count=1,physical_adoption=False));column_refs.append(thin(record));increments.append(increment);joined.append(out);bounds.append(envelope);clear_completed()
  # Successful row/column captures are sealed; only these small assembly operands persist.
 point=P.a_reshape(P.a_stack(increments,0),(15136,4,3));epoint=np.concatenate(bounds);fy_keep(label+'_NEW_phase_replacement_point',point,keep);keep(label+'_NEW_phase_replacement_uncancelled',epoint.copy());increment_weak=N.paired_scatter_normal(point,basis,label+'_NEW_phase_replacement');fy_keep(label+'_NEW_phase_replacement_weak',increment_weak,keep)
 load_names=tuple(n for n in admitted['loads']['metadata']['schema'] if n.startswith(('prior_signed_bridge_','prior_phase_current_')))+tuple(n+'_'+w for n in ('value_native_current','value_metric_current','value_initial_weak_CMC','value_total_weak_normal','actual_native_canonical_target_residual','actual_metric_canonical_target_residual','candidate_global_value_current_point_Hamiltonian_normal','candidate_global_value_time_primary_action_coefficients') for w in ('hi','lo'));old_loads=read_closed(admitted['loads'],load_names)
 for n,a in old_loads.items():keep(label+'_unchanged_load_'+n,a.copy())
 old_weak=phase_join_pair(old_loads,'value_total_weak_normal',(4,87,45),keep,label+'_old_total_weak_normal');new_weak=phase_join_add(old_weak,increment_weak,keep,label+'_total_weak_normal_join');old_point=phase_join_pair(old_loads,'candidate_global_value_current_point_Hamiltonian_normal',(15136,4,3),keep,label+'_old_point_normal');new_point=P.a_reshape(P.a_stack([P.a_slice(q,(slice(None),slice(None),slice(0,3))) for q in joined],0),(15136,4,3));fy_keep(label+'_NEW_joined_point_normal',new_point,keep);fy_keep(label+'_point_join_arithmetic_contact',P.a_sub(new_point,P.a_add(old_point,point)),keep)
 sheet_data=read_closed(admitted['sheet'],('sheet_value_weak_normal_hi','sheet_value_weak_normal_lo'));sheet=phase_join_pair(sheet_data,'sheet_value_weak_normal',(4,87,45),keep,label+'_unchanged_sheet_weak_normal')
 test=np.zeros((4,87,45));test[:,43,22]=(1.,2.,3.,4.);tv,_=finite_candidate_test_polynomials(test,np.zeros((87,45)),basis,keep,label+'_NEW_independent_polynomials')
 controls=dict(replacement=phase_join_functional(point,increment_weak,P.a_dd(np.zeros((4,87,45))),basis,test,tv,epoint,keep,check,label+'_phase_replacement'),joined=phase_join_functional(new_point,new_weak,sheet,basis,test,tv,abs(old_point[0])+abs(old_point[1])+epoint,keep,check,label+'_joined_normal'))
 current_names=tuple(n+'_'+w for n in ('NEW_finite_phase_NEW_finite_literal_weak','NEW_finite_phase_NEW_target_minus_finite_current','NEW_finite_phase_weak_nonlinear_and_scatter_association_remainder','NEW_finite_phase_finite_residual_identity_contact') for w in ('hi','lo'));current_data=read_closed(admitted['current'],current_names)
 for n,a in current_data.items():keep(label+'_copied_NEW_phase_current_'+n,a.copy())
 new_phase=phase_join_pair(current_data,'NEW_finite_phase_NEW_finite_literal_weak',(87,45),keep,label+'_NEW_literal_phase_current');phase_residual=phase_join_pair(current_data,'NEW_finite_phase_NEW_target_minus_finite_current',(87,45),keep,label+'_NEW_phase_target_minus_current');fy_keep(label+'_NEW_phase_current_minus_original_target',tuple(-a for a in phase_residual),keep)
 norms=dict(normal_L2=[float(np.linalg.norm(new_weak[0][i]+new_weak[1][i])) for i in range(4)])
 keep(label+'_descriptive_NEW_normal_norms',np.asarray(norms['normal_L2']).copy());readout=seal_completed('NORMAL_CANONICAL_VALUE_JOIN',dict(kind='NEW_fixed_geometry_phase_updated_four_normal_and_canonical_value_join',input=thin(header),columns=column_refs,unchanged_loads=thin(admitted['loads']),unchanged_sheet=thin(admitted['sheet']),new_phase_current=thin(admitted['current']),original_literal_phase_target=thin(admitted['prior']),normal_norms=norms,relative_phase_count=1,ordinary_mean_and_sheet_count=1,mechanical_current_and_CMC_copied_by_action_invariance=True,phase_current_exact_original_target_not_asserted=True,new_compact_chi_or_configuration_JVP=False,mixed_time_jet_or_evolution_admission=False,physical_adoption=False));clear_completed()
 return dict(columns=column_refs,readout=thin(readout),new_weak_normal=new_weak,new_literal_phase_current=new_phase,phase_target_minus_current=phase_residual,normal_controls=controls,value_only=True,new_configuration_JVP=False,physical_adoption=False)
