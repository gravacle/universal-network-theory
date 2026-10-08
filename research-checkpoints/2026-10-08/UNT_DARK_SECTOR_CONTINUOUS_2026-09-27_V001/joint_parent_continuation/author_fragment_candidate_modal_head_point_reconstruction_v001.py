"""HELD generic point-chunk reconstruction for a NEW numerical preconditioner.
Globals np,P,compact_contact_swap,ft_keep and positive finite keep. The NEW
point basis is exact(1.,0.), unlike the separate four-point rank experiment.
Original109 contractions/order and post-Pi association checks are retained.
No Fraction normalization, old action, inverse or global operator claim.
The containing provider authenticates CLOSED caches and seals each NEW action.
"""
MODAL_HEAD_POINT_AUTHOR_DRAFT=True
MODAL_HEAD_POINT_AUTHORING_IN_PROGRESS=False

def mh_pair(name,x,shape,keep):
 keep(name+'_both_words',np.stack(x).copy());assert x[0].shape==x[1].shape==shape
 assert all(a.dtype==np.float64 and np.all(np.isfinite(a)) for a in x)
 return ft_keep(name,(x[0].copy(),x[1].copy()),keep)

def mh_real_readout(x,keep,label):
 mh_pair(label+'_represented_pair',x,x[0].shape,keep)
 real=keep(label+'_real_binary64_readout',x[0]+x[1]);bv=real-x[0]
 error=keep(label+'_two_sum_readout_error',(x[0]-(real-bv))+(x[1]-bv))
 gap=P.a_sub(x,P.a_dd(real));mh_pair(label+'_represented_pair_minus_real',gap,x[0].shape,keep)
 return dict(pair=x,real=real,readout_gap=gap,two_sum_error=error,exact_real_normalization_claimed=False)

def mh_construction_contact(gap,envelope,keep,check,label):
 mh_pair(label+'_difference',gap,envelope.shape,keep);keep(label+'_uncancelled_envelope',envelope.copy())
 assert np.all(np.isfinite(envelope)) and np.all(envelope>=0)
 zero=envelope==0;keep(label+'_zero_envelope_mask',zero.copy());assert all(np.all(a[zero]==0) for a in gap)
 denominator=np.where(zero,1.,envelope);keep(label+'_positive_original_denominator_or_exact_zero_branch',denominator.copy())
 ratio=P.a_div64(gap,denominator,keep,label+'_dimensionless_division');mh_pair(label+'_dimensionless_ratio',ratio,envelope.shape,keep)
 check(label,ratio[0]+ratio[1],np.zeros_like(envelope),np.ones_like(envelope))

def reconstruct_modal_head_blocks(cache,columns,keep,describe,check,label):
 s,c,p=cache['s'],cache['c'],cache['p'];assert 1<=p<=128 and cache['configuration_held'] and len(columns)==3
 for family,values in (('configuration',s),('chart',c)):
  for n,a in values.items():keep(label+'_fixed_'+family+'_'+n,np.asarray(a).copy())
 assert s['z'].shape==(32,p,4) and s['hi'].shape==(p,4,4) and np.all(c['dens']>0)
 B=P.a_dd(np.zeros((32,p,9,3)));envelope=np.zeros_like(B[0]);aggregates=[];actuals=[]
 for axis,column in enumerate(columns):
  prefix=label+'_modal_axis%d'%axis;assert column['amplitude_words']==(1.,0.) and isinstance(column['completed_provenance'],dict) and column['completed_provenance']
  ni=mh_pair(prefix+'_completed_physical_native_input',column['physical_native'],(p,99),keep);mi=mh_pair(prefix+'_completed_physical_metric_input',column['physical_metric'],(p,6),keep)
  expected=P.a_dd(np.zeros((p,99)))
  for mode in range(32):expected[0][:,3+3*mode+axis]=1.;expected[1][:,3+3*mode+axis]=0.
  assert all(np.array_equal(a,b) for a,b in zip(ni,expected)) and all(np.all(a==0) for a in mi)
  Pi=mh_pair(prefix+'_completed_Pi',column['Pi'],(32,p,4,4),keep)
  native=mh_pair(prefix+'_completed_native_density',column['native'],(p,99),keep);metric=mh_pair(prefix+'_completed_metric_total_density',column['metric_total'],(p,6),keep)
  actual=P.a_stack([P.a_slice(native,(slice(None),i)) for i in range(3)]+[P.a_slice(metric,(slice(None),i)) for i in range(6)],1);mh_pair(prefix+'_actual_simultaneous_head',actual,(p,9),keep)
  total=P.a_dd(np.zeros((p,9)));bound=np.zeros((p,9))
  for mode in range(32):
   tag=prefix+'_mode%02d'%mode;pi=P.a_slice(Pi,mode);sym=P.a_mul64(.5,P.a_add(pi,compact_contact_swap(pi)));mh_pair(tag+'_symPi',sym,(p,4,4),keep)
   rows=[]
   for l in range(4):
    term=P.a_mul64(s['z'][mode,:,l,None,None],sym);mh_pair(tag+'_Klo_l%d_product'%l,term,(p,4,4),keep)
    row=P.a_sub(P.a_dd(np.zeros((p,4,4))),term);mh_pair(tag+'_Klo_l%d'%l,row,(p,4,4),keep);rows.append(row)
   Klo=P.a_stack(rows,1);mh_pair(tag+'_Klo',Klo,(p,4,4,4),keep);Kup=P.a_dd(np.zeros((p,4,4,4)))
   for m in range(4):
    term=P.a_mul64(s['hi'][:,:,m,None,None],(Klo[0][:,None,m],Klo[1][:,None,m]));mh_pair(tag+'_raised_product_m%d'%m,term,(p,4,4,4),keep)
    Kup=P.a_add(Kup,term);mh_pair(tag+'_raised_partial_m%d'%m,Kup,(p,4,4,4),keep)
   CC=P.a_mul64(.5,P.a_sub(P.a_add(P.a_transpose(Kup,(0,2,1,3)),P.a_transpose(Kup,(0,2,3,1))),Kup));mh_pair(tag+'_connection_D',CC,(p,4,4,4),keep)
   P00=P.a_slice(pi,(slice(None),0,0));u=P.a_mul64(c['JzU'][mode],(P00[0][:,None],P00[1][:,None]));mh_pair(tag+'_head_U_before_density',u,(p,3),keep)
   pm=P.a_dd(np.zeros((p,6)));C0=P.a_slice(CC,(slice(None),0,slice(None),slice(None)))
   for a in range(4):
    for b in range(4):
     cv=P.a_slice(C0,(slice(None),a,b));term=P.a_mul64(c['embed'][:,:,a,b],(cv[0][:,None],cv[1][:,None]));mh_pair(tag+'_metric_product_a%d_b%d'%(a,b),term,(p,6),keep)
     pm=P.a_add(pm,term);mh_pair(tag+'_metric_partial_a%d_b%d'%(a,b),pm,(p,6),keep)
   term=P.a_mul64(c['zh'][mode],(P00[0][:,None],P00[1][:,None]));mh_pair(tag+'_metric_zh_product',term,(p,6),keep)
   pm=P.a_add(pm,term);mh_pair(tag+'_head_metric_before_density',pm,(p,6),keep)
   head=P.a_stack([P.a_slice(u,(slice(None),i)) for i in range(3)]+[P.a_slice(pm,(slice(None),i)) for i in range(6)],1)
   head=P.a_mul64(c['dens'][:,None],head);mh_pair(tag+'_head_density',head,(p,9),keep)
   for word in (0,1):B[word][mode,:,:,axis]=head[word]
   # Positive NEW post-Pi operation envelope, before all mode/connection cancellations.
   ep=abs(pi[0])+abs(pi[1]);es=.5*(ep+ep.swapaxes(-1,-2));ek=abs(s['z'][mode])[:,:,None,None]*es[:,None]
   er=np.einsum('plm,pmab->plab',abs(s['hi']),ek);ec=.5*(er.transpose(0,2,1,3)+er.transpose(0,2,3,1)+er)
   eu=abs(c['JzU'][mode])*ep[:,0,0,None];em=np.einsum('pqab,pab->pq',abs(c['embed']),ec[:,0])+abs(c['zh'][mode])*ep[:,0,0,None]
   eb=abs(c['dens'])[:,None]*np.concatenate((eu,em),axis=1);keep(tag+'_positive_post_Pi_envelope',eb.copy());assert np.all(np.isfinite(eb)) and np.all(eb>=0)
   envelope[mode,:,:,axis]=eb;total=P.a_add(total,head);mh_pair(tag+'_aggregate_head_partial',total,(p,9),keep);bound+=eb;keep(tag+'_aggregate_envelope_partial',bound.copy())
  gap=P.a_sub(total,actual);mh_construction_contact(gap,2*bound,keep,check,prefix+'_distributed_vs_original_association')
  aggregates.append(total);actuals.append(actual)
 mh_pair(label+'_head_from_arm_scaled_columns',B,(32,p,9,3),keep);keep(label+'_post_Pi_operation_envelope',envelope.copy())
 normalized=mh_real_readout(B,keep,label+'_head_from_arm')
 return dict(B_scaled=B,B=normalized['pair'],B_real=normalized['real'],B_readout_gap=normalized['readout_gap'],B_two_sum_error=normalized['two_sum_error'],post_Pi_envelope=envelope,aggregate_reconstructed=aggregates,actual_simultaneous_heads=actuals,canonical_left_C_vs_formal_right_L_preserved=True,PiU_Maxwell_EH_zero_scope='pure modal temporal inputs at fixed configuration',uniform_DD_operator_or_global_inverse_qualified=False,physical_adoption=False)

def collect_directed_head_blocks(cache,columns,keep,describe,label):
 p=cache['p'];assert 1<=p<=128 and cache['configuration_held'] and len(columns)==9
 H=P.a_dd(np.zeros((p,9,9)));E=P.a_dd(np.zeros((32,p,3,9)))
 for slot,column in enumerate(columns):
  assert column['amplitude_words']==(1.,0.) and column['head_coordinate']==slot and isinstance(column['new_provenance'],dict) and column['new_provenance']
  ni=mh_pair(label+'_NEW_head_column%d_physical_native_input'%slot,column['physical_native'],(p,99),keep);mi=mh_pair(label+'_NEW_head_column%d_physical_metric_input'%slot,column['physical_metric'],(p,6),keep)
  en=P.a_dd(np.zeros((p,99)));em=P.a_dd(np.zeros((p,6)));expected=en if slot<3 else em;coordinate=slot if slot<3 else slot-3
  expected[0][:,coordinate]=1.;expected[1][:,coordinate]=0.
  assert all(np.array_equal(a,b) for supplied,target in ((ni,en),(mi,em)) for a,b in zip(supplied,target))
  prefix=label+'_NEW_head_column%d'%slot;native=mh_pair(prefix+'_native_density',column['native'],(p,99),keep);metric=mh_pair(prefix+'_metric_total_density',column['metric_total'],(p,6),keep)
  head=P.a_stack([P.a_slice(native,(slice(None),i)) for i in range(3)]+[P.a_slice(metric,(slice(None),i)) for i in range(6)],1);mh_pair(prefix+'_head_response',head,(p,9),keep)
  arm=tuple(a[:,3:].reshape(p,32,3).transpose(1,0,2) for a in native);mh_pair(prefix+'_arm_response',arm,(32,p,3),keep)
  for word in (0,1):H[word][:,:,slot]=head[word];E[word][:,:,:,slot]=arm[word]
  mh_pair(prefix+'_H_scaled_partial',H,(p,9,9),keep);mh_pair(prefix+'_E_scaled_partial',E,(32,p,3,9),keep)
 h=mh_real_readout(H,keep,label+'_H9');e=mh_real_readout(E,keep,label+'_arm_from_head')
 return dict(H_scaled=H,H=h['pair'],H_real=h['real'],H_readout_gap=h['readout_gap'],H_two_sum_error=h['two_sum_error'],E_scaled=E,E=e['pair'],E_real=e['real'],E_readout_gap=e['readout_gap'],E_two_sum_error=e['two_sum_error'],directed_crossblocks_transpose_not_assumed=True,physical_metric_six_order='RR,ZZ,phiphi,RZ,Rphi,Zphi; no additional offdiagonal multiplicity',uniform_DD_operator_or_global_inverse_qualified=False,physical_adoption=False)
