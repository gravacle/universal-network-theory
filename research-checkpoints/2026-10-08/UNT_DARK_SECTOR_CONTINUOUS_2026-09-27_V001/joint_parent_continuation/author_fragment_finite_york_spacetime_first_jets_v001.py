"""Held definitions: new finite ADM/covector firstjets and full product-rule JVP.
Globals np,P and reviewed fy_* paired helpers; no import, caller or invocation.
Each dual is (paired value,paired direction). This supplies new geometry only,
not EOS, features, canonical momentum, constraints, a solve or physical adoption.
The genuine physical Fk and covector time words are independent of intrinsic rho.
Owned all4 gauge/covector jets are authoritative; no raw chart recovery replaces
them. Spatial inverse jets use the analytic conformal policy and retain formal
inverse-jet gaps. Fixed lowered E0 is supplied from the sealed reference; no
zero-compatibility reset or old connection/firstjet producer is replayed.
"""
FINITE_SPACETIME_AUTHOR_DRAFT=True
FINITE_SPACETIME_AUTHORING_IN_PROGRESS=False

def fs_dual(value,delta=None):
 return value,P.a_dd(np.zeros_like(value[0])) if delta is None else delta

def fs_add(a,b):return P.a_add(a[0],b[0]),P.a_add(a[1],b[1])
def fs_neg(a):return P.a_mul64(-1.,a[0]),P.a_mul64(-1.,a[1])
def fs_sub(a,b):return fs_add(a,fs_neg(b))
def fs_mul(a,b):return P.a_mul(a[0],b[0]),P.a_add(P.a_mul(a[1],b[0]),P.a_mul(a[0],b[1]))
def fs_scale(c,a):return P.a_mul64(c,a[0]),P.a_mul64(c,a[1])
def fs_slice(a,key):return P.a_slice(a[0],key),P.a_slice(a[1],key)
def fs_stack(rows,axis):return P.a_stack([a[0] for a in rows],axis),P.a_stack([a[1] for a in rows],axis)
def fs_expand(a,key):return (a[0][0][key],a[0][1][key]),(a[1][0][key],a[1][1][key])
def fs_sum(a,axis):return fy_sum(a[0],axis),fy_sum(a[1],axis)
def fs_dot(a,b):return fs_sum(fs_mul(a,b),-1)
def fs_mv(A,x):return fs_sum(fs_mul(A,fs_expand(x,(Ellipsis,None,slice(None)))),-1)
def fs_mm(A,B):return fs_stack([fs_mv(A,fs_slice(B,(Ellipsis,slice(None),j))) for j in range(B[0][0].shape[-1])],-1)
def fs_transpose(a,axes):return (a[0][0].transpose(axes),a[0][1].transpose(axes)),(a[1][0].transpose(axes),a[1][1].transpose(axes))

def fs_keep(label,a,keep):
 fy_keep(label,a[0],keep);fy_keep(label+'_delta',a[1],keep);return a

def fs_div(a,b,keep,label):
 q=fy_div(a[0],b[0],keep,label+'_value')
 numerator=P.a_sub(a[1],P.a_mul(q,b[1]));fy_keep(label+'_direction_numerator',numerator,keep)
 dq=fy_div(numerator,b[0],keep,label+'_direction')
 fy_keep(label+'_direction_division_residual',P.a_sub(P.a_add(P.a_mul(b[0],dq),P.a_mul(b[1],q)),a[1]),keep)
 return q,dq

def fs_sqrt(a,keep,label):
 root=fy_sqrt(a[0],keep,label+'_value');delta=fy_div(a[1],P.a_mul64(2.,root),keep,label+'_direction')
 fy_keep(label+'_direction_square_residual',P.a_sub(P.a_mul64(2.,P.a_mul(root,delta)),a[1]),keep)
 return root,delta

def fs_block(a00,a0i,aij):
 row0=fs_stack([a00]+[fs_slice(a0i,(Ellipsis,i)) for i in range(3)],-1)
 rows=[row0]
 for i in range(3):rows.append(fs_stack([fs_slice(a0i,(Ellipsis,i))]+[fs_slice(aij,(Ellipsis,i,j)) for j in range(3)],-1))
 return fs_stack(rows,-2)

def fs_connection(hi,dg,E0,keep,label):
 shifted=fs_sub(dg,fs_dual(E0));rows=[]
 for a in range(4):
  columns=[]
  for b in range(4):
   terms=fs_sub(fs_add(fs_slice(shifted,(slice(None),a,b,slice(None))),fs_slice(shifted,(slice(None),b,a,slice(None)))),fs_slice(shifted,(slice(None),slice(None),a,b)))
   columns.append(fs_keep(label+'_current_connection_slot',fs_scale(.5,fs_mv(hi,terms)),keep))
  rows.append(fs_stack(columns,-1))
 return fs_keep(label+'_Gamma',fs_stack(rows,-2),keep)

def finite_york_spacetime_first_jets(geometry,conformal,gauge,covectors,mechanical,direction,reference,keep,label):
 # Slots: point; coordinate t/R/Z/phi; vector component. Modal arrays lead mode.
 p=geometry['h'][0].shape[0];put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 h=fs_dual(geometry['h'],geometry['delta_h']);I=fs_dual(geometry['ih'],geometry['delta_ih']);mu=fs_dual(geometry['mu'],geometry['delta_mu'])
 N=fs_dual(gauge['N']);beta=fs_dual(gauge['beta']);Na=fs_dual(gauge['N_jets']);ba=fs_dual(gauge['beta_jets'])
 u=fs_dual(covectors['u']);zsp=fs_dual(covectors['z']);ua=fs_dual(covectors['u_jets'],direction['u_jets']);za=fs_dual(covectors['z_jets'],direction['z_jets'])
 ht=fs_dual(mechanical['h_dot'],direction['h_dot'])
 lam=fs_dual(conformal['lambda'],P.a_mul(P.a_mul64(4.,direction['rho']),conformal['lambda']))
 rg=fs_dual(conformal['rho_gradient'],direction['rho_gradient']);I0=fs_dual(reference['physical_spatial_inverse']);h0a=fs_dual(reference['h_spatial_jets'])
 assert h[0][0].shape==h[0][1].shape==I[0][0].shape==I[0][1].shape==(p,3,3)
 expected=((h,(p,3,3)),(I,(p,3,3)),(mu,(p,)),(N,(p,)),(beta,(p,3)),(Na,(p,4)),(ba,(p,4,3)),(u,(p,3)),(zsp,(32,p,3)),(ua,(p,4,3)),(za,(32,p,4,3)),(ht,(p,3,3)),(lam,(p,)),(rg,(p,2)))
 for value,shape in expected:
  assert all(w.shape==shape for pair in value for w in pair)
  assert all(np.all(np.isfinite(w)) for pair in value for w in pair)
 assert I0[0][0].shape==I0[0][1].shape==(p,3,3) and h0a[0][0].shape==h0a[0][1].shape==(p,2,3,3)
 assert reference['E0'][0].shape==reference['E0'][1].shape==(p,4,4,4)
 assert np.all(N[0][0]-abs(N[0][1])>0)
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for a in (h,ht) for pair in a for w in pair)
 assert all(np.all(w[:,1:]==0) for w in direction['u_jets']) and all(np.all(w[:,:,1:]==0) for w in direction['z_jets'])
 for n,x in (('owned_gauge_N',N),('owned_gauge_beta',beta),('owned_gauge_N_jets',Na),('owned_gauge_beta_jets',ba),('owned_covector_u',u),('owned_covector_z',zsp),('genuine_covector_u_jets',ua),('genuine_covector_z_jets',za),('genuine_mechanical_h_dot',ht),('conformal_weight',lam),('rho_gradient',rg)):put(n,x)
 put('new_physical_reference_inverse',I0);put('owned_h_reference_spatial_jets',h0a)
 fy_keep(label+'_fixed_lowered_E0',reference['E0'],keep)
 zero_matrix=fs_dual(P.a_dd(np.zeros((p,3,3))))
 hR=fs_dual(P.a_slice(geometry['h_spatial_jets'],(slice(None),0)),P.a_slice(geometry['delta_h_spatial_jets'],(slice(None),0)))
 hZ=fs_dual(P.a_slice(geometry['h_spatial_jets'],(slice(None),1)),P.a_slice(geometry['delta_h_spatial_jets'],(slice(None),1)))
 ha=put('h_first',fs_stack([ht,hR,hZ,zero_matrix],1));inverse_jets=[]
 inverse_jets.append(fs_neg(fs_mm(fs_mm(I,ht),I)))
 for a in range(2):
  I0a=fs_neg(fs_mm(fs_mm(I0,fs_slice(h0a,(slice(None),a))),I0))
  inside=fs_sub(I0a,fs_mul(fs_expand(fs_scale(4.,fs_slice(rg,(slice(None),a))),(Ellipsis,None,None)),I0))
  inverse_jets.append(fs_div(inside,fs_expand(lam,(Ellipsis,None,None)),keep,label+'_spatial_inverse_jet_'+str(a)))
 inverse_jets.append(zero_matrix);Ia=put('inverse_first',fs_stack(inverse_jets,1))
 formal=[]
 for a in range(4):formal.append(fs_neg(fs_mm(fs_mm(I,fs_slice(ha,(slice(None),a))),I)))
 put('analytic_minus_formal_inverse_first',fs_sub(Ia,fs_stack(formal,1)))
 put('physical_reference_inverse_transport_gap',fs_sub(I0,fs_mul(fs_expand(lam,(Ellipsis,None,None)),I)))
 # ADM metric and inverse: fixed N/beta, complete paired spatial geometry.
 one=fs_dual(P.a_dd(np.ones(p)));N2=fs_mul(N,N);invN2=fs_div(one,N2,keep,label+'_inverse_N_squared')
 hb=fs_mv(h,beta);g00=fs_sub(fs_dot(beta,hb),N2);g=put('g',fs_block(g00,hb,h))
 bb=fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(beta,(Ellipsis,None,slice(None))))
 hi=put('hi',fs_block(fs_neg(invN2),fs_mul(fs_expand(invN2,(Ellipsis,None)),beta),fs_sub(I,fs_mul(fs_expand(invN2,(Ellipsis,None,None)),bb))))
 density=put('density',fs_mul(N,mu));w=put('up',fs_mv(I,u))
 gamma=put('gamma',fs_sqrt(fs_add(one,fs_dot(u,w)),keep,label+'_gamma_root'))
 U0=fs_div(gamma,N,keep,label+'_U0');Ui=fs_sub(w,fs_mul(beta,fs_expand(U0,(Ellipsis,None))))
 U=put('U',fs_stack([U0]+[fs_slice(Ui,(slice(None),i)) for i in range(3)],1))
 A=fs_dot(fs_expand(w,(None,Ellipsis)),zsp)
 z0=fs_sub(fs_dot(fs_expand(beta,(None,Ellipsis)),zsp),fs_div(fs_mul(fs_expand(N,(None,Ellipsis)),A),fs_expand(gamma,(None,Ellipsis)),keep,label+'_z0'))
 z=put('z',fs_stack([z0]+[fs_slice(zsp,(slice(None),slice(None),i)) for i in range(3)],2))
 dgrows=[];dhirows=[];durows=[];dzrows=[];uprows=[];gammarows=[]
 for a in range(4):
  haj=fs_slice(ha,(slice(None),a));iaj=fs_slice(Ia,(slice(None),a));naj=fs_slice(Na,(slice(None),a));baj=fs_slice(ba,(slice(None),a))
  uaj=fs_slice(ua,(slice(None),a));zaj=fs_slice(za,(slice(None),slice(None),a))
  hba=fs_add(fs_mv(haj,beta),fs_mv(h,baj))
  g00a=fs_sub(fs_add(fs_dot(baj,hb),fs_dot(beta,hba)),fs_scale(2.,fs_mul(N,naj)))
  dgrows.append(fs_block(g00a,hba,haj))
  invNa=fs_div(fs_scale(2.,naj),fs_mul(N2,N),keep,label+'_inverse_N_jet_'+str(a))
  hi0a=fs_sub(fs_mul(fs_expand(invN2,(Ellipsis,None)),baj),fs_mul(fs_expand(invNa,(Ellipsis,None)),beta))
  bba=fs_add(fs_mul(fs_expand(baj,(Ellipsis,slice(None),None)),fs_expand(beta,(Ellipsis,None,slice(None)))),fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(baj,(Ellipsis,None,slice(None)))))
  spatial=fs_add(fs_sub(iaj,fs_mul(fs_expand(invN2,(Ellipsis,None,None)),bba)),fs_mul(fs_expand(invNa,(Ellipsis,None,None)),bb))
  dhirows.append(fs_block(invNa,hi0a,spatial))
  wa=fs_add(fs_mv(iaj,u),fs_mv(I,uaj));uprows.append(wa)
  ga=fs_div(fs_add(fs_dot(uaj,w),fs_dot(u,wa)),fs_scale(2.,gamma),keep,label+'_gamma_jet_'+str(a));gammarows.append(ga)
  U0a=fs_sub(fs_div(ga,N,keep,label+'_U0_first_'+str(a)),fs_div(fs_mul(gamma,naj),N2,keep,label+'_U0_second_'+str(a)))
  Uia=fs_sub(fs_sub(wa,fs_mul(baj,fs_expand(U0,(Ellipsis,None)))),fs_mul(beta,fs_expand(U0a,(Ellipsis,None))))
  durows.append(fs_stack([U0a]+[fs_slice(Uia,(slice(None),i)) for i in range(3)],1))
  Aa=fs_add(fs_dot(fs_expand(wa,(None,Ellipsis)),zsp),fs_dot(fs_expand(w,(None,Ellipsis)),zaj))
  numerator=fs_add(fs_mul(fs_expand(naj,(None,Ellipsis)),A),fs_mul(fs_expand(N,(None,Ellipsis)),Aa))
  first=fs_div(numerator,fs_expand(gamma,(None,Ellipsis)),keep,label+'_z0_jet_first_'+str(a))
  second=fs_div(fs_mul(fs_mul(fs_expand(N,(None,Ellipsis)),A),fs_expand(ga,(None,Ellipsis))),fs_expand(fs_mul(gamma,gamma),(None,Ellipsis)),keep,label+'_z0_jet_second_'+str(a))
  shift=fs_add(fs_dot(fs_expand(baj,(None,Ellipsis)),zsp),fs_dot(fs_expand(beta,(None,Ellipsis)),zaj))
  z0a=fs_add(shift,fs_sub(second,first));dzrows.append(fs_stack([z0a]+[fs_slice(zaj,(slice(None),slice(None),i)) for i in range(3)],2))
  put('current_dg',fs_stack(dgrows,1));put('current_dhi',fs_stack(dhirows,1));put('current_du',fs_stack(durows,1));put('current_dz',fs_stack(dzrows,2))
 dg=put('dg',fs_stack(dgrows,1));dhi=put('dhi',fs_stack(dhirows,1));du=put('du',fs_stack(durows,1));dz=put('dz',fs_stack(dzrows,2))
 formal_hi_first=fs_stack([fs_neg(fs_mm(fs_mm(hi,fs_slice(dg,(slice(None),a))),hi)) for a in range(4)],1)
 put('ADM_minus_formal_spacetime_inverse_first',fs_sub(dhi,formal_hi_first))
 put('up_first',fs_stack(uprows,1));put('gamma_first',fs_stack(gammarows,1))
 uc=put('uc',fs_mv(g,U));projector=put('projector',fs_add(fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4)))),fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None))))))
 put('spacetime_inverse_gap',fs_sub(fs_mm(g,hi),fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4))))))
 put('unit_constraint',fs_add(fs_dot(U,uc),one));put('transverse_constraint',fs_dot(fs_expand(U,(None,Ellipsis)),z))
 put('covector_spatial_value_readout_gap',fs_sub(fs_slice(uc,(slice(None),slice(1,None))),u))
 unit_first=[];trans_first=[];cov_first=[]
 for a in range(4):
  ga=fs_slice(dg,(slice(None),a));Ua=fs_slice(du,(slice(None),a));zaa=fs_slice(dz,(slice(None),slice(None),a))
  unit_first.append(fs_add(fs_add(fs_dot(Ua,uc),fs_dot(U,fs_mv(g,Ua))),fs_dot(U,fs_mv(ga,U))))
  trans_first.append(fs_add(fs_dot(fs_expand(Ua,(None,Ellipsis)),z),fs_dot(fs_expand(U,(None,Ellipsis)),zaa)))
  recovered=fs_add(fs_mv(ga,U),fs_mv(g,Ua));cov_first.append(fs_sub(fs_slice(recovered,(slice(None),slice(1,None))),fs_slice(ua,(slice(None),a))))
 put('unit_first_constraint',fs_stack(unit_first,1));put('transverse_first_constraint',fs_stack(trans_first,2));put('covector_spatial_first_readout_gap',fs_stack(cov_first,1))
 Ga=fs_connection(hi,dg,reference['E0'],keep,label+'_fixed_E0')
 compatibility=[];zero_E_connection=[]
 for a in range(4):
  G=fs_slice(Ga,(slice(None),slice(None),a,slice(None)))
  reaction=fs_add(fs_mm(fs_transpose(G,(0,2,1)),g),fs_mm(g,G))
  compatibility.append(fs_sub(fs_slice(dg,(slice(None),a)),reaction))
 for a in range(4):
  columns=[]
  for b in range(4):
   e=reference['E0'];terms=P.a_sub(P.a_add(P.a_slice(e,(slice(None),a,b,slice(None))),P.a_slice(e,(slice(None),b,a,slice(None)))),P.a_slice(e,(slice(None),slice(None),a,b)))
   columns.append(fs_scale(-.5,fs_mv(hi,fs_dual(terms))))
  zero_E_connection.append(fs_stack(columns,-1))
 put('compatibility_minus_fixed_E0',fs_sub(fs_stack(compatibility,1),fs_dual(reference['E0'])))
 put('fixed_E0_lowered_symmetry_gap',fs_sub(fs_dual(reference['E0']),fs_transpose(fs_dual(reference['E0']),(0,1,3,2))))
 put('fixed_E0_minus_zero_E0_connection',fs_stack(zero_E_connection,-2));put('connection_torsion',fs_sub(Ga,fs_transpose(Ga,(0,1,3,2))))
 out=dict(g=g,hi=hi,U=U,z=z,uc=uc,P=projector,up=w,gamma=gamma,dens=density,mu=mu,du=du,dz=dz,dg=dg,dhi=dhi,Ga=Ga,h_first=ha,inverse_first=Ia,up_first=fs_stack(uprows,1),gamma_first=fs_stack(gammarows,1))
 for n in ('g','hi','U','z','du','dz','dg','Ga'):
  assert reference[n][0].shape==reference[n][1].shape==out[n][0][0].shape
  put('candidate_minus_owned_reference_'+n,fs_sub(out[n],fs_dual(reference[n])))
 put('owned_reference_torsion',fs_sub(fs_dual(reference['Ga']),fs_transpose(fs_dual(reference['Ga']),(0,1,3,2))))
 return dict(value={n:x[0] for n,x in out.items()},delta={n:x[1] for n,x in out.items()},fixed_lowered_E0=reference['E0'],owned_reference_anchors_retained=True,phase_EOS_evaluated=False,candidate_features_evaluated=False,physical_adoption=False)
