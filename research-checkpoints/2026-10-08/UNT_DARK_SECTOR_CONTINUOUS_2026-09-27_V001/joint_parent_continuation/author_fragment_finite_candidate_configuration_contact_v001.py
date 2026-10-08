"""Held NEW configuration/rate contact on the published225 candidate.
Globals np,P, reviewed fy_*/fs_* and compact_contact_momenta definitions.
Raw s/c and completed paired jets/features/momenta come from the SAME NEW
adapter transaction. Its binary64 publication is held as a representative;
this differentiates its declared algebra, not the discontinuous rounding map.
All raw-child and paired-jet construction gaps and their inverse/volume/chart
representative contacts remain explicit. N,beta,covariant u_i,z_ji and gauge
jets are fixed. Physical hdot and native time-rate directions are independent.
No EOS/source/old coefficients/operator/solve/finite adoption is evaluated.
"""
FINITE_CANDIDATE_CONTACT_AUTHOR_DRAFT=True
FINITE_CANDIDATE_CONTACT_AUTHORING_IN_PROGRESS=False

def fc_anchor(label,expression,value,keep):
 anchor=P.a_dd(value) if isinstance(value,np.ndarray) else value
 fs_keep(label+'_constructed',expression,keep);fy_keep(label+'_owned_representative',anchor,keep)
 fy_keep(label+'_construction_gap',P.a_sub(expression[0],anchor),keep)
 return anchor,expression[1]

def fc_quotient(label,numerator,denominator,value,keep):
 anchor=P.a_dd(value) if isinstance(value,np.ndarray) else value
 constructed=fy_div(numerator[0],denominator[0],keep,label+'_primal')
 top=P.a_sub(numerator[1],P.a_mul(anchor,denominator[1]));fy_keep(label+'_direction_numerator',top,keep)
 delta=fy_div(top,denominator[0],keep,label+'_direction')
 fy_keep(label+'_division_contact_residual',P.a_sub(P.a_add(P.a_mul(denominator[0],delta),P.a_mul(denominator[1],anchor)),numerator[1]),keep)
 return fc_anchor(label,(constructed,delta),anchor,keep)

def fc_square_root(label,square,value,keep):
 anchor=P.a_dd(value);constructed=fy_sqrt(square[0],keep,label+'_primal')
 delta=P.a_div64(square[1],2*value,keep,label+'_direction')
 fy_keep(label+'_square_contact_residual',P.a_sub(P.a_mul64(2*value,delta),square[1]),keep)
 return fc_anchor(label,(constructed,delta),anchor,keep)

def fc_symmetric_contact(label,value,keep):
 # The analytic symmetric direction is serialized with one shared triangle.
 # Preserve the pre-copy rounding/asymmetry contact, never reset a base field.
 fy_keep(label+'_unshared_triangle',value,keep);out=(value[0].copy(),value[1].copy())
 for i in range(value[0].shape[-1]):
  for j in range(i):
   for word in (0,1):out[word][...,i,j]=out[word][...,j,i]
 fy_keep(label+'_triangle_copy_contact',P.a_sub(out,value),keep);return fy_keep(label+'_shared_triangle',out,keep)

def finite_candidate_configuration_contact(candidate,geometry,gauge,covectors,mechanical,direction,reference,keep,label):
 s,c=candidate['s'],candidate['c'];jets=candidate['jets'];p=len(c['N'])
 put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 anchor=lambda n,x,v:fc_anchor(label+'_'+n,x,v,keep)
 quotient=lambda n,a,b,v:fc_quotient(label+'_'+n,a,b,v,keep)
 for name,shape in (('h',(p,3,3)),('h_spatial_jets',(p,2,3,3)),('h_dot',(p,3,3)),('u_jets',(p,4,3)),('z_jets',(32,p,4,3))):
  assert all(isinstance(w,np.ndarray) and w.dtype==np.float64 and w.shape==shape and np.all(np.isfinite(w)) for w in direction[name])
  fy_keep(label+'_input_direction_'+name,direction[name],keep)
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for name in ('h','h_spatial_jets','h_dot') for w in direction[name])
 assert all(np.all(w[:,1:]==0) for w in direction['u_jets']) and all(np.all(w[:,:,1:]==0) for w in direction['z_jets'])
 h=put('h',fs_dual(P.a_dd(c['h']),direction['h']));I0=P.a_dd(c['ih'])
 dI=fc_symmetric_contact(label+'_inverse_direction',P.a_mul64(-1.,fy_mm(fy_mm(I0,direction['h']),I0)),keep);I=put('ih',fs_dual(I0,dI))
 fractional=P.a_mul64(.5,fy_contract(I0,direction['h']));mu=put('sqrt_h',fs_dual(P.a_dd(c['sqrt_h']),P.a_mul64(c['sqrt_h'],fractional)))
 N=fs_dual(P.a_dd(c['N']));beta=fs_dual(P.a_dd(c['beta']));u=fs_dual(P.a_dd(c['u']));zi=fs_dual(P.a_dd(s['z'][:,:,1:]))
 Na=fs_dual(gauge['N_jets']);ba=fs_dual(gauge['beta_jets']);ua=fs_dual(covectors['u_jets'],direction['u_jets']);za=fs_dual(covectors['z_jets'],direction['z_jets'])
 ht=fs_dual(mechanical['h_dot'],direction['h_dot']);zero=fs_dual(P.a_dd(np.zeros((p,3,3))))
 ha=put('h_first',fs_stack([ht,fs_dual(P.a_slice(geometry['h_spatial_jets'],(slice(None),0)),P.a_slice(direction['h_spatial_jets'],(slice(None),0))),fs_dual(P.a_slice(geometry['h_spatial_jets'],(slice(None),1)),P.a_slice(direction['h_spatial_jets'],(slice(None),1))),zero],1))
 put('inverse_residual',fs_sub(fs_mm(h,I),fs_dual(P.a_dd(np.broadcast_to(np.eye(3),(p,3,3))))))
 put('volume_square_contact',fs_mul(mu,mu))
 if 'ih' in direction:fy_keep(label+'_supplied_geometry_minus_raw_formal_inverse_contact',P.a_sub(direction['ih'],dI),keep)
 if 'mu' in direction:fy_keep(label+'_supplied_geometry_minus_raw_volume_contact',P.a_sub(direction['mu'],mu[1]),keep)
 up=put('up',anchor('up',fs_mv(I,u),c['up']))
 gamma=put('gamma',fc_square_root(label+'_gamma',fs_add(fs_dual(P.a_dd(np.ones(p))),fs_dot(u,up)),c['gamma'],keep))
 U0=quotient('U0',gamma,N,s['U'][:,0]);Ui=anchor('Ui',fs_sub(up,fs_mul(beta,fs_expand(U0,(Ellipsis,None)))),s['U'][:,1:])
 U=put('U',fs_stack([U0]+[fs_slice(Ui,(slice(None),i)) for i in range(3)],1))
 A=anchor('up_dot_zi',fs_dot(fs_expand(up,(None,Ellipsis)),zi),np.einsum('pi,jpi->jp',c['up'],s['z'][:,:,1:]))
 zquot=quotient('z0_quotient',fs_mul(fs_expand(N,(None,Ellipsis)),A),fs_expand(gamma,(None,Ellipsis)),c['N'][None]*A[0][0]/c['gamma'][None])
 z0=anchor('z0',fs_sub(fs_dot(fs_expand(beta,(None,Ellipsis)),zi),zquot),s['z'][:,:,0]);z=put('z',fs_stack([z0]+[fs_slice(zi,(slice(None),slice(None),i)) for i in range(3)],2))
 N2=anchor('N_squared',fs_mul(N,N),c['N']**2);g2=anchor('gamma_squared',fs_mul(gamma,gamma),c['gamma']**2);g3=anchor('gamma_cubed',fs_mul(g2,gamma),c['gamma']**3)
 hb=anchor('h_beta',fs_mv(h,beta),np.einsum('pij,pj->pi',c['h'],c['beta']))
 g=put('g',anchor('g',fs_block(fs_sub(fs_dot(beta,hb),N2),hb,h),s['g']))
 bb=fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(beta,(Ellipsis,None,slice(None))))
 hi00=fs_dual(P.a_dd(s['hi'][:,0,0]));hi0i=fs_dual(P.a_dd(s['hi'][:,0,1:]))
 hij=anchor('hi_spatial',fs_sub(I,fs_div(bb,fs_expand(N2,(Ellipsis,None,None)),keep,label+'_shift_inverse')),s['hi'][:,1:,1:])
 hi=put('hi',fs_block(hi00,hi0i,hij));dens=put('dens',anchor('dens',fs_mul(N,mu),c['dens']))
 uc=put('uc',anchor('uc',fs_mv(g,U),s['uc']))
 projector=put('P',anchor('P',fs_add(fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4)))),fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None))))),s['P']))
 Z=fs_dual(P.a_dd(np.zeros((p,4))))
 for j in range(32):Z=fs_add(Z,fs_scale(s['w'][j],fs_slice(z,j)));put('current_Z',Z)
 Z=put('Z',anchor('Z',Z,s['Z']))
 phi=fs_dual(P.a_dd(s['phi']),direction.get('phi',P.a_dd(np.zeros_like(s['phi']))));put('phi',phi)
 put('r',anchor('r',fs_mv(projector,phi),s['r']))
 z2=put('z2',anchor('z2',fs_dot(z,fs_mv(hi,z)),s['z2']))
 kj=(P.B*P.GC)**2*s['xi'][:,None]**4;put('f',anchor('f',fs_add(fs_dual(P.a_dd(np.ones_like(s['f']))),fs_scale(1/kj,z2)),s['f']))
 e=np.zeros((6,3,3))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[a,i,j]=e[a,j,i]=1.
 E=fs_dual(P.a_dd(e[None]));Ng=anchor('N_gamma',fs_mul(N,gamma),c['N']*c['gamma'])
 JU0=quotient('JU0',up,fs_expand(Ng,(Ellipsis,None)),c['JU'][:,0])
 JUsp=anchor('JUsp',fs_sub(I,fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(JU0,(Ellipsis,None,slice(None))))),c['JU'][:,1:])
 JU=put('JU',fs_stack([JU0]+[fs_slice(JUsp,(slice(None),i)) for i in range(3)],1))
 Jzz=put('Jzz',anchor('Jzz',fs_sub(beta,fs_div(fs_mul(fs_expand(N,(Ellipsis,None)),up),fs_expand(gamma,(Ellipsis,None)),keep,label+'_Jzz_quotient')),c['Jzz']))
 term=fs_sub(fs_div(fs_mv(I,zi),fs_expand(gamma,(None,Ellipsis,None)),keep,label+'_JzU_first'),fs_div(fs_mul(fs_expand(A,(Ellipsis,None)),fs_expand(up,(None,Ellipsis))),fs_expand(g3,(None,Ellipsis,None)),keep,label+'_JzU_second'))
 JzU=put('JzU',anchor('JzU',fs_mul(fs_expand(fs_neg(N),(None,Ellipsis,None)),term),c['JzU']))
 Eu=fs_mv(E,fs_expand(up,(Ellipsis,None,slice(None))));wh=anchor('wh',fs_neg(fs_mv(fs_expand(I,(Ellipsis,None,slice(None),slice(None))),Eu)),-np.einsum('pij,ajk,pk->pai',c['ih'],e,c['up']))
 gh=quotient('gh',fs_neg(fs_dot(fs_expand(up,(Ellipsis,None,slice(None))),Eu)),fs_expand(fs_scale(2.,gamma),(Ellipsis,None)),-np.einsum('pi,aij,pj->pa',c['up'],e,c['up'])/(2*c['gamma'][:,None]))
 Uh0=quotient('Uh0',gh,fs_expand(N,(Ellipsis,None)),c['Uh'][:,:,0]);Uhi=fs_sub(wh,fs_mul(fs_expand(beta,(Ellipsis,None,slice(None))),fs_expand(Uh0,(Ellipsis,None))))
 Uh=put('Uh',anchor('Uh',fs_stack([Uh0]+[fs_slice(Uhi,(slice(None),slice(None),i)) for i in range(3)],2),c['Uh']))
 whz=fs_dot(fs_expand(zi,(Ellipsis,None,slice(None))),fs_expand(wh,(None,Ellipsis)))
 zh=put('zh',anchor('zh',fs_mul(fs_expand(fs_neg(N),(None,Ellipsis,None)),fs_sub(fs_div(whz,fs_expand(gamma,(None,Ellipsis,None)),keep,label+'_zh_first'),fs_div(fs_mul(fs_expand(A,(Ellipsis,None)),fs_expand(gh,(None,Ellipsis))),fs_expand(g2,(None,Ellipsis,None)),keep,label+'_zh_second'))),c['zh']))
 embed=put('embed',fs_dual(P.a_dd(c['embed'])))
 dgrows=[];durows=[];dzrows=[];Iarows=[];warows=[];garows=[]
 for a in range(4):
  H=fs_slice(ha,(slice(None),a));n=fs_slice(Na,(slice(None),a));b=fs_slice(ba,(slice(None),a));v=fs_slice(ua,(slice(None),a));zz=fs_slice(za,(slice(None),slice(None),a))
  ia=fs_neg(fs_mm(fs_mm(I,H),I));Iarows.append(ia)
  wa=fs_add(fs_mv(ia,u),fs_mv(I,v));warows.append(wa)
  ga=fs_div(fs_add(fs_dot(v,up),fs_dot(u,wa)),fs_scale(2.,gamma),keep,label+'_gamma_first_'+str(a));garows.append(ga)
  U0a=fs_sub(fs_div(ga,N,keep,label+'_U0_first_'+str(a)),fs_div(fs_mul(gamma,n),N2,keep,label+'_U0_second_'+str(a)))
  Uia=fs_sub(fs_sub(wa,fs_mul(fs_expand(U0,(Ellipsis,None)),b)),fs_mul(beta,fs_expand(U0a,(Ellipsis,None))))
  durows.append(fs_stack([U0a]+[fs_slice(Uia,(slice(None),i)) for i in range(3)],1))
  Aa=fs_add(fs_dot(fs_expand(wa,(None,Ellipsis)),zi),fs_dot(fs_expand(up,(None,Ellipsis)),zz))
  numerator=fs_add(fs_mul(fs_expand(n,(None,Ellipsis)),A),fs_mul(fs_expand(N,(None,Ellipsis)),Aa))
  second=fs_div(fs_mul(fs_mul(fs_expand(N,(None,Ellipsis)),A),fs_expand(ga,(None,Ellipsis))),fs_expand(g2,(None,Ellipsis)),keep,label+'_z0_second_'+str(a))
  shift=fs_add(fs_dot(fs_expand(b,(None,Ellipsis)),zi),fs_dot(fs_expand(beta,(None,Ellipsis)),zz))
  z0a=fs_add(shift,fs_sub(second,fs_div(numerator,fs_expand(gamma,(None,Ellipsis)),keep,label+'_z0_first_'+str(a))))
  dzrows.append(fs_stack([z0a]+[fs_slice(zz,(slice(None),slice(None),i)) for i in range(3)],2))
  hba=fs_add(fs_mv(H,beta),fs_mv(h,b));g00a=fs_sub(fs_add(fs_dot(b,hb),fs_dot(beta,hba)),fs_scale(2.,fs_mul(N,n)))
  dgrows.append(fs_block(g00a,hba,H));put('current_dg',fs_stack(dgrows,1));put('current_du',fs_stack(durows,1));put('current_dz',fs_stack(dzrows,2))
 dg=put('dg',anchor('dg',fs_stack(dgrows,1),jets['dg']));du=put('du',anchor('du',fs_stack(durows,1),jets['du']));dz=put('dz',anchor('dz',fs_stack(dzrows,2),jets['dz']))
 Ia=put('inverse_first',fs_stack(Iarows,1));wa=put('up_first',fs_stack(warows,1));ga=put('gamma_first',fs_stack(garows,1))
 Ga=put('Ga',anchor('Ga',fs_connection(hi,dg,reference['E0'],keep,label+'_fixed_E0'),jets['Ga']))
 put('spacetime_inverse_residual',fs_sub(fs_mm(g,hi),fs_dual(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4))))))
 put('unit_constraint',fs_add(fs_dot(U,uc),fs_dual(P.a_dd(np.ones(p)))));put('transverse_constraint',fs_dot(fs_expand(U,(None,Ellipsis)),z))
 compatibility=[]
 for a in range(4):
  G=fs_slice(Ga,(slice(None),slice(None),a,slice(None)))
  compatibility.append(fs_sub(fs_slice(dg,(slice(None),a)),fs_add(fs_mm(fs_transpose(G,(0,2,1)),g),fs_mm(g,G))))
 put('compatibility_minus_fixed_E0',fs_sub(fs_stack(compatibility,1),fs_dual(reference['E0'])))
 put('connection_torsion',fs_sub(Ga,fs_transpose(Ga,(0,1,3,2))))
 d={n:x[1] for n,x in dict(g=g,hi=hi,U=U,z=z,uc=uc,P=projector,phi=phi,dg=dg,du=du,dz=dz,Ga=Ga).items()}
 dc={n:x[1] for n,x in dict(h=h,ih=I,N=N,beta=beta,u=u,up=up,gamma=gamma,JU=JU,Jzz=Jzz,JzU=JzU,Uh=Uh,zh=zh,embed=embed,dens=dens,sqrt_h=mu,mu=mu).items()}
 dc['log_dens']=fy_div(dc['dens'],P.a_dd(c['dens']),keep,label+'_fractional_density_contact')
 df,dm=compact_contact_momenta(s,c,jets,candidate['features'],candidate['momenta'],d,dc,keep,label+'_NEW_action_contact')
 spatial_fraction=fy_div(dc['sqrt_h'],P.a_dd(c['sqrt_h']),keep,label+'_fractional_spatial_volume_contact')
 fy_keep(label+'_spatial_minus_4D_density_fraction_gap',P.a_sub(spatial_fraction,dc['log_dens']),keep)
 # NEW EH contact uses its own sqrt_h product/division, not the 4D fraction.
 Kdual=fs_dual(candidate['momenta']['K'],dm['K']);taudual=fs_dual(candidate['momenta']['Ktrace'],dm['Ktrace'])
 pinum=fs_mul(fs_expand(mu,(Ellipsis,None,None)),fs_sub(fs_mm(fs_mm(I,Kdual),I),fs_mul(fs_expand(taudual,(Ellipsis,None,None)),I)))
 pi=anchor('metric_EH_tensor',(P.a_div64(pinum[0],2*P.C,keep,label+'_EH_value_division'),P.a_div64(pinum[1],2*P.C,keep,label+'_EH_contact_division')),candidate['momenta']['metric_EH_tensor'])
 fy_keep(label+'_new_EH_minus_123_density_measure_contact',P.a_sub(pi[1],dm['metric_EH_tensor']),keep);dm['metric_EH_tensor']=pi[1]
 dm['metric_EH_density']=P.a_stack([P.a_mul64(1. if i==j else 2.,P.a_slice(pi[1],(slice(None),i,j))) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1)
 dm['metric_total_density']=P.a_add(dm['metric_native_density'],dm['metric_EH_density'])
 for family,values in (('configuration',d),('chart',dc),('feature',df['paired']),('momentum',dm)):
  for n,x in values.items():fy_keep(label+'_completed_'+family+'_'+n,x,keep)
 Lie=fs_dual(P.a_dd(np.zeros((p,3,3))))
 for k in range(3):Lie=fs_add(Lie,fs_mul(fs_expand(fs_slice(beta,(slice(None),k)),(Ellipsis,None,None)),fs_slice(ha,(slice(None),k+1))))
 columns=[]
 for i in range(3):
  rows=[]
  for j in range(3):
   rows.append(fs_add(fs_slice(Lie,(slice(None),i,j)),fs_add(fs_dot(fs_slice(h,(slice(None),j)),fs_slice(ba,(slice(None),i+1))),fs_dot(fs_slice(h,(slice(None),i)),fs_slice(ba,(slice(None),j+1))))))
  columns.append(fs_stack(rows,-1))
 Lie=put('Lie_beta_h',fs_stack(columns,-2));KADM=put('KADM',fs_div(fs_sub(ht,Lie),fs_expand(fs_scale(2.,N),(Ellipsis,None,None)),keep,label+'_KADM'))
 KG=fs_dual(candidate['momenta']['K'],dm['K']);put('KGamma_minus_KADM',fs_sub(KG,KADM))
 put('Ktrace_Gamma_minus_ADM',fs_sub(fs_dual(candidate['momenta']['Ktrace'],dm['Ktrace']),fs_sum(fs_sum(fs_mul(I,KADM),2),1)))
 # compact123 fixes phase jets; its r derivative is a comparison when phi varies.
 fy_keep(label+'_phase_direction_omitted_from_native_r_contact',fy_mv(P.a_dd(s['P']),phi[1]),keep)
 state=dict(h=h,ih=I,mu=mu,N=N,beta=beta,up=up,gamma=gamma,A=A,U=U,z=z,g=g,hi=hi,uc=uc,P=projector,phi=phi,Z=Z,z2=z2,dens=dens,h_first=ha,inverse_first=Ia,up_first=wa,gamma_first=ga,N_first=Na,beta_first=ba,z_spatial_first=za,du=du,dz=dz,dg=dg,Ga=Ga,KADM=KADM)
 return dict(d=d,dc=dc,delta_features=df,delta_momenta=dm,state=state,h_first=ha[0],delta_h_first=ha[1],inverse_first=Ia[0],delta_inverse_first=Ia[1],geometry_rounding_map_differentiated=False,phase_relative_owned_by_separate_literal_core=True,old_coefficients_transported=False,physical_adoption=False)
