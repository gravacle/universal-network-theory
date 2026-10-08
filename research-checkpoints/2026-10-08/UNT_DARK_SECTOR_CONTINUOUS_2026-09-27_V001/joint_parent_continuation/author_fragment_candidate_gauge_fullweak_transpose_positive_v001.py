"""HELD outward source-port coefficient propagation for gauge C*.
Globals np/P/N and seven reviewed mp_* primitives. The coefficients are the
completed paired286 gauge ports, never nodal inverse factors or R_v. Magnitudes
include both words; every new lift/coefficient/sum/test-map operation is outward.
This bounds the represented coefficient contractions, not upstream source error
before cancellation inside each286 port or a uniform arbitrary286 derivative.
"""
GAUGE_TRANSPOSE_POSITIVE_AUTHOR_DRAFT=True
GAUGE_TRANSPOSE_POSITIVE_AUTHORING_IN_PROGRESS=False


def candidate_gauge_fullweak_transpose_positive(prepared,dual,group,read_closed_column,keep,label):
 assert not GAUGE_TRANSPOSE_POSITIVE_AUTHOR_DRAFT and not GAUGE_TRANSPOSE_POSITIVE_AUTHORING_IN_PROGRESS
 assert group in ('mechanical','phase') and prepared['coefficient_transpose_only'] is True
 mag=lambda x:mp_add(abs(x[0]),abs(x[1]),keep,label+'_bothword_magnitude');add=lambda a,b:mp_add(a,b,keep,label);mul=lambda a,b:mp_mul(a,b,keep,label);summ=lambda a,axis:mp_sum(a,axis,keep,label)
 basis=prepared['basis'];ports=np.zeros((15136,4,4));x=mag(dual)
 if group=='mechanical':
  assert x.shape==(403340,);nh,mh,_=P.unpack_fields(x,False);n=P.lift_velocity(nh);m=P.lift_metric(mh);sn=np.zeros((33,4,86,44,3));sm=np.zeros((4,86,44,6))
  for iq in range(4):
   R=basis['R'][iq].reshape(86,44);weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);F=P.dd_metric_F(R)
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2
    nv=np.moveaxis(n[:,:,di:86+di,dj:44+dj],1,-1);sn[:,iq]=add(sn[:,iq],mul(weight[...,None],mul(abs(factor),nv)))
    mv=np.moveaxis(m[:,di:86+di,dj:44+dj],0,-1);sm[iq]=add(sm[iq],mp_mv(abs(F),mul(weight[...,None],mul(abs(hat[...,None]),mv)),keep,label+'_Fmap'))
   keep(label+'_native_Sstar_positive_prefix',sn.copy());keep(label+'_metric_Sstar_positive_prefix',sm.copy())
  point=dict(native=sn.transpose(1,2,3,0,4).reshape(15136,99),metric=sm.reshape(15136,6))
 else:
  assert x.shape==(3870,);nodes=np.zeros((87,45));nodes[P.scalar_mask()]=x;lift=P.scalar_lift(nodes);scalar=np.zeros((4,86,44))
  for iq in range(4):
   weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44)
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):scalar[iq]=add(scalar[iq],mul(weight,mul(abs(basis['hats'][iq,corner,0]),lift[di:86+di,dj:44+dj])))
   keep(label+'_scalar_Sstar_positive_prefix',scalar.copy())
  point=dict(phase=scalar.reshape(15136))
 for descriptor in prepared['columns']:
  iq=descriptor['column'];sl=slice(iq*3784,(iq+1)*3784);block=read_closed_column(descriptor,('native','metric','phase'))
  assert block['record']==descriptor['record'] and block['source_provenance']==descriptor['same_candidate_provenance']
  part=np.zeros((3784,4,4))
  for n,coeff in block['paired'].items():
   magnitude=mag(coeff);keep(label+'_completed_source_port_magnitude_'+n,magnitude.copy())
   if n not in point:continue
   q=mul(magnitude,point[n][sl,None,None] if n=='phase' else point[n][sl,:,None,None]);part=add(part,q if n=='phase' else summ(q,1))
  ports[sl]=part;keep(label+'_Cpointstar_positive_prefix',ports.copy())
 out=np.zeros((4,87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    value=np.zeros((86,44))
    for jet,hat in enumerate(N.normal_hat_jet(basis,iq,corner,row)):value=add(value,mul(abs(hat),ports[sl,row,jet].reshape(86,44)))
    key=(row,slice(di,86+di),slice(dj,44+dj));out[key]=add(out[key],value)
    keep(label+'_unweighted_Tstar_positive_prefix',out.copy())
 out[:,1]=add(out[:,1],out[:,0]);out[:,0]=0;out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 keep(label+'_original_restricted_positive_weak',out.copy());keep(label+'_already_weighted_positive_time',ports[:,:,3].copy())
 return dict(weak_normal=out,time_coefficient_point=ports[:,:,3].copy(),point_coefficients_weighted=ports,spatial_weight_count=1,source_port_coefficient_envelope_only=True,upstream286_cancellation_error_bound=False,physical_adoption=False)


def candidate_gauge_new_port_forward_positive(prepared,test_jets,group,read_closed_column,keep,label):
 assert not GAUGE_TRANSPOSE_POSITIVE_AUTHOR_DRAFT and not GAUGE_TRANSPOSE_POSITIVE_AUTHORING_IN_PROGRESS
 assert group in ('mechanical','phase') and prepared['coefficient_transpose_only'] is True
 mag=lambda x:mp_add(abs(x[0]),abs(x[1]),keep,label+'_word_magnitude');add=lambda a,b:mp_add(a,b,keep,label);mul=lambda a,b:mp_mul(a,b,keep,label)
 jets=mag(test_jets['physical_gauge_jets']);families=('native','metric') if group=='mechanical' else ('phase',);widths=dict(native=99,metric=6,phase=None)
 point={n:np.zeros((15136,) if widths[n] is None else (15136,widths[n])) for n in families}
 for descriptor in prepared['columns']:
  iq=descriptor['column'];sl=slice(iq*3784,(iq+1)*3784);block=read_closed_column(descriptor,('native','metric','phase'))
  assert block['record']==descriptor['record'] and block['source_provenance']==descriptor['same_candidate_provenance']
  for row in range(4):
   for jet in range(4):
    for n in families:
     coefficient=mag(block['paired'][n]);a=coefficient[:,row,jet] if n=='phase' else coefficient[:,:,row,jet];b=jets[sl,row,jet] if n=='phase' else jets[sl,row,jet,None];point[n][sl]=add(point[n][sl],mul(a,b))
  for n,a in point.items():keep(label+'_'+n+'_uncancelled_point_prefix',a.copy())
 basis=prepared['basis']
 if group=='mechanical':
  nf=point['native'].reshape(4,86,44,33,3).transpose(3,0,1,2,4);mf=point['metric'].reshape(4,86,44,6);no=np.zeros((33,3,87,45));mo=np.zeros((6,87,45))
  for iq in range(4):
   R=basis['R'][iq].reshape(86,44);weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);F=P.dd_metric_F(R)
   nw=mul(weight[...,None],nf[:,iq]);mw=mul(weight[...,None],mp_mv(abs(F.swapaxes(-1,-2)),mf[iq],keep,label+'_original_Fstar'))
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    hat=basis['hats'][iq,corner,0];factor=np.broadcast_to(hat[...,None],(86,44,3)).copy();factor[...,2]*=R**2;key=(slice(None),slice(None),slice(di,86+di),slice(dj,44+dj));no[key]=add(no[key],mul(abs(factor),nw).transpose(0,3,1,2))
    key=(slice(None),slice(di,86+di),slice(dj,44+dj));mo[key]=add(mo[key],mul(abs(hat[...,None]),mw).transpose(2,0,1))
    keep(label+'_original_native_S_positive_prefix',no.copy());keep(label+'_original_metric_S_positive_prefix',mo.copy())
  for component in (1,2):no[:,component,1]=add(no[:,component,1],no[:,component,0])
  no[:,:,0]=0;no[:,1,:,0]=0;mo[:,1]=add(mo[:,1],mo[:,0]);mo[:,0]=0;mo[3:5,:,0]=0;packed=P.pack_fields(no,mo)
 else:
  scalar=point['phase'].reshape(4,86,44);out=np.zeros((87,45))
  for iq in range(4):
   weight=(basis['dv'][iq]/basis['R'][iq]).reshape(86,44);weighted=mul(weight,scalar[iq])
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    key=(slice(di,86+di),slice(dj,44+dj));out[key]=add(out[key],mul(abs(basis['hats'][iq,corner,0]),weighted));keep(label+'_original_scalar_S_positive_prefix',out.copy())
  out[1]=add(out[1],out[0]);out[0]=0;packed=out[P.scalar_mask()].copy()
 keep(label+'_completed_uncancelled_forward_envelope',packed.copy());return packed
