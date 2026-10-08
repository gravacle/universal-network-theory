"""Held NEW candidate coefficient/firstjet adapter into the registered action.
Globals np,P and reviewed fy_* helpers. Supplied callbacks are the exact767
affine feature/momentum definitions, evaluated only on this NEW candidate.
One raw h snapshot owns a freshly resolved physical inverse/volume; every ADM,
covector, chart, projector and material coefficient is rebuilt. Genuine time
and owned spatial/gauge firstjets retain both words. Paired169 model differences,
raw construction, Eq2 quotient representatives, E0 and KGamma/KADM gaps persist.
No EOS/source/weakrow/operator/solver, canonical refit or physical adoption here.
Callbacks require the exact767 globals ALPHA/ELL/C and the same fixed B/GC.
Positive envelopes disclose construction magnitude, not an all-action admission.
"""
FINITE_RAW_ACTION_AUTHOR_DRAFT=True
FINITE_RAW_ACTION_AUTHORING_IN_PROGRESS=False
FINITE_RAW_ACTION_PRIMITIVE_SOURCE_SHA='b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19'
FINITE_RAW_ACTION_GEOMETRY_SOURCE_SHA='12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70'
FINITE_RAW_ACTION_SPACETIME_SOURCE_SHA='aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d'

def fa_publish(label,value,envelope,keep):
 fy_keep(label+'_paired_input',value,keep);raw,last=P.a_sum(value[0],value[1])
 keep(label+'_binary64',np.asarray(raw).copy());keep(label+'_sum_rounding_word',np.asarray(last).copy())
 gap=P.a_sub(value,P.a_dd(raw));fy_keep(label+'_paired_minus_binary64',gap,keep)
 e=np.asarray(envelope);assert e.shape==raw.shape and np.all(np.isfinite(e)) and np.all(e>=0)
 bound=2*np.finfo(float).eps*(abs(value[0])+abs(value[1]));keep(label+'_quantization_bound',bound.copy());keep(label+'_operation_envelope',e.copy())
 assert np.all(abs(gap[0])+abs(gap[1])<=bound)
 assert raw.dtype==np.float64 and np.all(np.isfinite(raw));return raw.copy()

def fa_gap(label,value,raw,envelope,keep):
 fy_keep(label+'_paired_model',value,keep);keep(label+'_raw_representative',np.asarray(raw).copy())
 gap=P.a_sub(value,P.a_dd(raw));fy_keep(label+'_model_minus_raw',gap,keep);keep(label+'_operation_envelope',np.asarray(envelope).copy());return gap

def fa_input_pair(label,value,shape,keep):
 fy_keep(label,value,keep)
 assert len(value)==2 and all(isinstance(w,np.ndarray) and w.dtype==np.float64 and w.shape==shape and np.all(np.isfinite(w)) for w in value)
 return value

def fa_block(a00,a0i,aij):
 rows=[P.a_stack([a00]+[P.a_slice(a0i,(Ellipsis,i)) for i in range(3)],-1)]
 for i in range(3):rows.append(P.a_stack([P.a_slice(a0i,(Ellipsis,i))]+[P.a_slice(aij,(Ellipsis,i,j)) for j in range(3)],-1))
 return P.a_stack(rows,-2)

def fa_coefficient_construction_contacts(s,c,bounds,ki,keep,label):
 # Each contact evaluates that coefficient's algebra on its declared RAW inputs.
 # It is a local construction residual, not an independent correctness witness.
 h,I,N,beta,u,up,gamma=c['h'],c['ih'],c['N'],c['beta'],c['u'],c['up'],c['gamma'];zi=s['z'][:,:,1:];p=len(N)
 contact=lambda n,x:fa_gap(label+'_'+n,x,s[n] if n in s else c[n],bounds[n],keep)
 contact('up',fy_mv(P.a_dd(I),P.a_dd(u)))
 q=P.a_add(P.a_dd(np.ones(p)),fy_sum(P.a_prod(u,up),-1));contact('gamma',fy_sqrt(q,keep,label+'_gamma_root'))
 U0=P.a_div64(P.a_dd(gamma),N,keep,label+'_U0');Ui=P.a_sub(P.a_dd(up),P.a_mul64(beta,(U0[0][:,None],U0[1][:,None])))
 contact('U',P.a_stack([U0]+[P.a_slice(Ui,(slice(None),i)) for i in range(3)],1))
 A=fy_sum(P.a_prod(up[None],zi),-1);z0=P.a_sub(fy_sum(P.a_prod(beta[None],zi),-1),P.a_div64(P.a_mul64(N[None],A),gamma[None],keep,label+'_z0'))
 contact('z',P.a_stack([z0]+[P.a_dd(zi[:,:,i]) for i in range(3)],2))
 hb=fy_mv(P.a_dd(h),P.a_dd(beta));g00=P.a_sub(fy_sum(P.a_mul64(beta,hb),-1),P.a_prod(N,N));contact('g',fa_block(g00,hb,P.a_dd(h)))
 N2=P.a_prod(N,N);i00=fy_div(P.a_dd(-np.ones(p)),N2,keep,label+'_inverse_00');i0=fy_div(P.a_dd(beta),(N2[0][:,None],N2[1][:,None]),keep,label+'_inverse_0i')
 ii=P.a_sub(P.a_dd(I),fy_div(P.a_prod(beta[:,:,None],beta[:,None,:]),(N2[0][:,None,None],N2[1][:,None,None]),keep,label+'_inverse_ij'));contact('hi',fa_block(i00,i0,ii))
 contact('uc',fy_mv(P.a_dd(s['g']),P.a_dd(s['U'])));contact('P',P.a_add(P.a_dd(np.broadcast_to(np.eye(4),(p,4,4))),P.a_prod(s['uc'][:,:,None],s['U'][:,None,:])))
 Z=P.a_dd(np.zeros((p,4)))
 for j in range(32):Z=P.a_add(Z,P.a_prod(s['w'][j],s['z'][j]))
 contact('Z',Z);contact('r',fy_mv(P.a_dd(s['P']),P.a_dd(s['phi'])))
 z2=fy_sum(P.a_mul64(s['z'],fy_mv(P.a_dd(s['hi']),P.a_dd(s['z']))),-1);contact('z2',z2);contact('f',P.a_add(P.a_dd(np.ones((32,p))),P.a_div64(P.a_dd(s['z2']),ki[:,None],keep,label+'_f')))
 contact('dens',P.a_prod(N,c['sqrt_h']))
 e=np.zeros((6,3,3))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[a,i,j]=e[a,j,i]=1.
 Ng=P.a_prod(N,gamma);JU0=fy_div(P.a_dd(up),(Ng[0][:,None],Ng[1][:,None]),keep,label+'_JU0')
 JUsp=P.a_sub(P.a_dd(I),P.a_prod(beta[:,:,None],c['JU'][:,None,0,:]));contact('JU',P.a_stack([JU0]+[P.a_slice(JUsp,(slice(None),i)) for i in range(3)],1))
 contact('Jzz',P.a_sub(P.a_dd(beta),P.a_div64(P.a_prod(N[:,None],up),gamma[:,None],keep,label+'_Jzz')))
 g2=P.a_prod(gamma,gamma);g3=P.a_mul64(gamma,g2)
 term=P.a_sub(P.a_div64(fy_mv(P.a_dd(I),P.a_dd(zi)),gamma[None,:,None],keep,label+'_JzU_first'),fy_div(P.a_prod(np.einsum('pi,jpi->jp',up,zi)[:,:,None],up[None]),(g3[0][None,:,None],g3[1][None,:,None]),keep,label+'_JzU_second'));contact('JzU',P.a_mul64(-N[None,:,None],term))
 Eu=fy_mv(P.a_dd(e[None]),P.a_dd(up[:,None]));wh=P.a_mul64(-1.,fy_mv(P.a_dd(I[:,None]),Eu));gh=P.a_div64(P.a_mul64(-1.,fy_sum(P.a_mul64(up[:,None],Eu),-1)),2*gamma[:,None],keep,label+'_gh')
 U0h=P.a_div64(gh,N[:,None],keep,label+'_Uh0');Uih=P.a_sub(wh,P.a_mul64(beta[:,None],(U0h[0][:,:,None],U0h[1][:,:,None])));contact('Uh',P.a_stack([U0h]+[P.a_slice(Uih,(slice(None),slice(None),i)) for i in range(3)],2))
 whz=fy_sum(P.a_mul64(zi[:,:,None],(wh[0][None],wh[1][None])),-1)
 zhc=P.a_sub(P.a_div64(whz,gamma[None,:,None],keep,label+'_zh_first'),fy_div(P.a_mul64(np.einsum('pi,jpi->jp',up,zi)[:,:,None],(gh[0][None],gh[1][None])),(g2[0][None,:,None],g2[1][None,:,None]),keep,label+'_zh_second'));contact('zh',P.a_mul64(-N[None,:,None],zhc))
 eb=fy_mv(P.a_dd(e[None]),P.a_dd(beta[:,None]));emb=P.a_stack([fa_block(fy_sum(P.a_mul64(beta,P.a_slice(eb,(slice(None),a))),-1),P.a_slice(eb,(slice(None),a)),P.a_dd(np.broadcast_to(e[a],(p,3,3)))) for a in range(6)],1);contact('embed',emb)

def fa_new_first_jets(s,c,h_first,Na,ba,ua,za,E0,keep,label):
 p=len(c['N']);N,beta,h,I,u,up,gamma=c['N'],c['beta'],c['h'],c['ih'],c['u'],c['up'],c['gamma'];zi=s['z'][:,:,1:]
 hb=np.einsum('pij,pj->pi',h,beta);A=np.einsum('pi,jpi->jp',up,zi)
 dg=[];du=[];dz=[];Ia=[];wjets=[];gjets=[];edg=[];edu=[];edz=[];eIa=[]
 eI,eh,eb,eu,ez=abs(I),abs(h),abs(beta),abs(u),abs(zi);ew=np.einsum('pij,pj->pi',eI,eu);eA=np.einsum('pi,jpi->jp',ew,ez);ehb=np.einsum('pij,pj->pi',eh,eb)
 put=lambda n,x:fy_keep(label+'_'+n,x,keep)
 for a in range(4):
  H=P.a_slice(h_first,(slice(None),a));n=P.a_slice(Na,(slice(None),a));b=P.a_slice(ba,(slice(None),a));v=P.a_slice(ua,(slice(None),a));z=P.a_slice(za,(slice(None),slice(None),a))
  ia=P.a_mul64(-1.,fy_mm(fy_mm(P.a_dd(I),H),P.a_dd(I)));Ia.append(ia)
  w=P.a_add(fy_mv(ia,P.a_dd(u)),fy_mv(P.a_dd(I),v));wjets.append(w)
  numer=P.a_add(fy_sum(P.a_mul64(up,v),-1),fy_sum(P.a_mul64(u,w),-1));ga=P.a_div64(numer,2*gamma,keep,label+'_gamma_jet_'+str(a));gjets.append(ga)
  U0a=P.a_sub(P.a_div64(ga,N,keep,label+'_U0_jet_first_'+str(a)),P.a_div64(P.a_mul64(gamma,n),N*N,keep,label+'_U0_jet_second_'+str(a)))
  Uia=P.a_sub(P.a_sub(w,P.a_mul64(s['U'][:,0,None],b)),P.a_mul64(beta,(U0a[0][:,None],U0a[1][:,None])))
  du.append(P.a_stack([U0a]+[P.a_slice(Uia,(slice(None),i)) for i in range(3)],1))
  Aa=P.a_add(fy_sum(P.a_mul64(zi,(w[0][None],w[1][None])),-1),fy_sum(P.a_mul64(up[None],z),-1))
  numerator=P.a_add(P.a_mul64(A,(n[0][None],n[1][None])),P.a_mul64(N[None],Aa))
  z0a=P.a_mul64(-1.,P.a_div64(numerator,gamma[None],keep,label+'_z0_first_'+str(a)))
  z0a=P.a_add(z0a,P.a_div64(P.a_mul64(N[None]*A,(ga[0][None],ga[1][None])),gamma[None]**2,keep,label+'_z0_second_'+str(a)))
  z0a=P.a_add(z0a,P.a_add(fy_sum(P.a_mul64(zi,(b[0][None],b[1][None])),-1),fy_sum(P.a_mul64(beta[None],z),-1)))
  dz.append(P.a_stack([z0a]+[P.a_slice(z,(slice(None),slice(None),i)) for i in range(3)],2))
  hba=P.a_add(fy_mv(H,P.a_dd(beta)),fy_mv(P.a_dd(h),b))
  g00a=P.a_add(fy_sum(P.a_mul64(hb,b),-1),fy_sum(P.a_mul64(beta,hba),-1));g00a=P.a_sub(g00a,P.a_mul64(2*N,n));dg.append(fa_block(g00a,hba,H))
  eH=abs(H[0])+abs(H[1]);en=abs(n[0])+abs(n[1]);ebj=abs(b[0])+abs(b[1]);ev=abs(v[0])+abs(v[1]);ezj=abs(z[0])+abs(z[1])
  ei=np.einsum('pij,pjk,pkl->pil',eI,eH,eI);eIa.append(ei);ewa=np.einsum('pij,pj->pi',ei,eu)+np.einsum('pij,pj->pi',eI,ev)
  ega=(np.einsum('pi,pi->p',ev,ew)+np.einsum('pi,pi->p',eu,ewa))/(2*gamma)
  eU0=ega/N+gamma*en/(N*N);eUi=ewa+ebj*abs(s['U'][:,0,None])+eb*eU0[:,None];edu.append(np.column_stack((eU0,eUi)))
  eAa=np.einsum('pi,jpi->jp',ewa,ez)+np.einsum('pi,jpi->jp',ew,ezj)
  ez0=np.einsum('pi,jpi->jp',ebj,ez)+np.einsum('pi,jpi->jp',eb,ezj)+(en[None]*eA+N[None]*eAa)/gamma[None]+N[None]*eA*ega[None]/gamma[None]**2
  edz.append(np.concatenate((ez0[:,:,None],ezj),axis=2))
  eHB=np.einsum('pij,pj->pi',eH,eb)+np.einsum('pij,pj->pi',eh,ebj);eg00=2*N*en+np.einsum('pi,pi->p',ebj,ehb)+np.einsum('pi,pi->p',eb,eHB)
  eg=np.empty((p,4,4));eg[:,0,0]=eg00;eg[:,0,1:]=eg[:,1:,0]=eHB;eg[:,1:,1:]=eH;edg.append(eg)
  put('current_du',P.a_stack(du,1));put('current_dz',P.a_stack(dz,2));put('current_dg',P.a_stack(dg,1))
 out=dict(du=put('du',P.a_stack(du,1)),dz=put('dz',P.a_stack(dz,2)),dg=put('dg',P.a_stack(dg,1)))
 put('inverse_first',P.a_stack(Ia,1));put('up_first',P.a_stack(wjets,1));put('gamma_first',P.a_stack(gjets,1))
 Ga=P.a_dd(np.zeros((p,4,4,4)));Econtact=P.a_dd(np.zeros((p,4,4,4)));Genv=np.zeros_like(Ga[0]);eDG=np.stack(edg,1);eE=abs(E0[0])+abs(E0[1]);shifted=P.a_sub(out['dg'],E0)
 for a in range(4):
  for b in range(4):
   term=P.a_sub(P.a_add(P.a_slice(shifted,(slice(None),a,b,slice(None))),P.a_slice(shifted,(slice(None),b,a,slice(None)))),P.a_slice(shifted,(slice(None),slice(None),a,b)))
   v=P.a_mul64(.5,fy_mv(P.a_dd(s['hi']),term));Ga[0][:,:,a,b]=v[0];Ga[1][:,:,a,b]=v[1];put('current_Gamma',Ga)
   eterm=P.a_sub(P.a_add(P.a_slice(E0,(slice(None),a,b,slice(None))),P.a_slice(E0,(slice(None),b,a,slice(None)))),P.a_slice(E0,(slice(None),slice(None),a,b)))
   ev=P.a_mul64(-.5,fy_mv(P.a_dd(s['hi']),eterm));Econtact[0][:,:,a,b]=ev[0];Econtact[1][:,:,a,b]=ev[1]
   et=eDG[:,a,b]+eDG[:,b,a]+eDG[:,:,a,b]+eE[:,a,b]+eE[:,b,a]+eE[:,:,a,b];Genv[:,:,a,b]=np.einsum('plm,pm->pl',abs(s['hi']),et)/2
 out['Ga']=put('Ga',Ga);envelope=dict(du=np.stack(edu,1),dz=np.stack(edz,2),dg=eDG,Ga=Genv)
 for n,e in envelope.items():keep(label+'_operation_'+n,e.copy())
 compatibility=[];covread=[]
 for a in range(4):
  G=P.a_slice(Ga,(slice(None),slice(None),a,slice(None)));reaction=P.a_add(fy_mm((G[0].swapaxes(1,2),G[1].swapaxes(1,2)),P.a_dd(s['g'])),fy_mm(P.a_dd(s['g']),G))
  compatibility.append(P.a_sub(P.a_slice(out['dg'],(slice(None),a)),reaction))
  read=P.a_add(fy_mv(P.a_slice(out['dg'],(slice(None),a)),P.a_dd(s['U'])),fy_mv(P.a_dd(s['g']),P.a_slice(out['du'],(slice(None),a))))
  covread.append(P.a_sub(P.a_slice(read,(slice(None),slice(1,None))),P.a_slice(ua,(slice(None),a))))
 put('compatibility_minus_E0',P.a_sub(P.a_stack(compatibility,1),E0));put('covector_owned_first_readout_gap',P.a_stack(covread,1))
 put('fixed_E0_lowered_symmetry_gap',P.a_sub(E0,(E0[0].swapaxes(-1,-2),E0[1].swapaxes(-1,-2))))
 put('connection_torsion',P.a_sub(Ga,(Ga[0].swapaxes(-1,-2),Ga[1].swapaxes(-1,-2))))
 put('fixed_E0_minus_zero_E0_connection',Econtact)
 return out,envelope

def finite_candidate_raw_action_adapter(geometry,spacetime,gauge,covectors,mechanical,phase,material,reference,feature_fn,momentum_fn,keep,label):
 p=geometry['h'][0].shape[0];put=lambda n,x:fy_keep(label+'_'+n,x,keep)
 rawkeep=lambda n,x:(keep(label+'_completed_raw_'+n,np.asarray(x).copy()),x)[1]
 publish=lambda n,x,e:fa_publish(label+'_'+n,x,e,keep)
 for family,values,shapes in (('geometry',geometry,dict(h=(p,3,3),ih=(p,3,3),mu=(p,),h_spatial_jets=(p,2,3,3))),('gauge',gauge,dict(N=(p,),beta=(p,3),N_jets=(p,4),beta_jets=(p,4,3))),('covectors',covectors,dict(u=(p,3),z=(32,p,3),u_jets=(p,4,3),z_jets=(32,p,4,3))),('mechanical',mechanical,dict(h_dot=(p,3,3))),('phase',phase,dict(phi=(p,4))),('reference',reference,dict(E0=(p,4,4,4),g=(p,4,4),hi=(p,4,4),U=(p,4),z=(32,p,4),du=(p,4,4),dz=(32,p,4,4),dg=(p,4,4,4),Ga=(p,4,4,4)))):
  for n,shape in shapes.items():fa_input_pair(label+'_input_'+family+'_'+n,values[n],shape,keep)
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for w in mechanical['h_dot'])
 assert all(np.array_equal(w,w.swapaxes(-1,-2)) for w in geometry['h_spatial_jets'])
 h=publish('h',geometry['h'],abs(geometry['h'][0])+abs(geometry['h'][1]))
 Ipair,det=fy_physical_reference_inverse(P.a_dd(h),keep,label+'_new_published_geometry');mupair=fy_sqrt(det,keep,label+'_new_published_volume')
 I=publish('ih',Ipair,abs(Ipair[0])+abs(Ipair[1]));mu=publish('sqrt_h',mupair,abs(mupair[0])+abs(mupair[1]))
 N=publish('N',gauge['N'],abs(gauge['N'][0])+abs(gauge['N'][1]));beta=publish('beta',gauge['beta'],abs(gauge['beta'][0])+abs(gauge['beta'][1]))
 u=publish('u',covectors['u'],abs(covectors['u'][0])+abs(covectors['u'][1]));zi=publish('zi',covectors['z'],abs(covectors['z'][0])+abs(covectors['z'][1]));phi=publish('phi',phase['phi'],abs(phase['phi'][0])+abs(phase['phi'][1]))
 assert h.shape==I.shape==(p,3,3) and N.shape==mu.shape==(p,) and beta.shape==u.shape==(p,3) and zi.shape==(32,p,3) and phi.shape==(p,4)
 assert np.all(N>0) and np.all(mu>0)
 omega,xi,weight=material['omega'],material['xi'],material['w'];assert omega.shape==xi.shape==weight.shape==(32,)
 assert all(isinstance(a,np.ndarray) and a.dtype==np.float64 and np.all(np.isfinite(a)) for a in (omega,xi,weight)) and np.all(omega>0) and np.all(xi>0) and np.all(weight>=0)
 assert math_is_finite_positive(material['B']) and math_is_finite_positive(material['GC'])
 for n in ('B','GC','ALPHA','ELL','C'):
  assert math_is_finite_positive(material[n]) and getattr(P,n)==material[n]
 for n in ('omega','xi','w','B','GC','ALPHA','ELL','C','R','Z_coordinate'):keep(label+'_unchanged_material_'+n,np.asarray(material[n]).copy())
 assert material['R'].shape==material['Z_coordinate'].shape==(p,) and np.all(np.isfinite(material['R'])) and np.all(np.isfinite(material['Z_coordinate']))
 up=rawkeep('up',np.einsum('pij,pj->pi',I,u));eup=np.einsum('pij,pj->pi',abs(I),abs(u));q=1+np.einsum('pi,pi->p',u,up);eq=1+np.einsum('pi,pi->p',abs(u),eup)
 keep(label+'_gamma_square',q.copy());keep(label+'_gamma_square_envelope',eq.copy());assert np.all(q>2e-11*eq);gamma=rawkeep('gamma',np.sqrt(q))
 U=rawkeep('U',np.column_stack((gamma/N,up-beta*gamma[:,None]/N[:,None])));A=rawkeep('up_dot_zi',np.einsum('pi,jpi->jp',up,zi));zt=np.einsum('pi,jpi->jp',beta,zi)-N[None]*A/gamma[None]
 z=rawkeep('z',np.concatenate((zt[:,:,None],zi),axis=2))
 g=np.empty((p,4,4));g[:,1:,1:]=h;g[:,0,1:]=g[:,1:,0]=np.einsum('pij,pj->pi',h,beta);g[:,0,0]=-N*N+np.einsum('pi,pij,pj->p',beta,h,beta)
 hi=np.empty_like(g);hi[:,0,0]=-1/(N*N);hi[:,0,1:]=hi[:,1:,0]=beta/(N[:,None]**2);hi[:,1:,1:]=I-beta[:,:,None]*beta[:,None,:]/N[:,None,None]**2
 rawkeep('g',g);rawkeep('hi',hi)
 uc=np.einsum('pab,pb->pa',g,U);projector=np.eye(4)[None]+uc[:,:,None]*U[:,None,:];Z=np.einsum('j,jpa->pa',weight,z);r=np.einsum('pab,pb->pa',projector,phi)
 z2=np.einsum('jpa,pab,jpb->jp',z,hi,z);ki=(material['B']*material['GC'])**2*xi**4;assert np.all(np.isfinite(ki)) and np.all(ki>0);f=1+z2/ki[:,None]
 for n,v in (('uc',uc),('P',projector),('Z',Z),('r',r),('z2',z2),('ki',ki),('f',f)):rawkeep(n,v)
 e=np.zeros((6,3,3))
 for a,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):e[a,i,j]=e[a,j,i]=1.
 JU=np.empty((p,4,3));JU[:,0]=up/(N*gamma)[:,None];JU[:,1:]=I-beta[:,:,None]*JU[:,None,0]
 rawkeep('JU',JU)
 Jzz=beta-N[:,None]*up/gamma[:,None]
 rawkeep('Jzz',Jzz)
 JzU=-N[None,:,None]*(np.einsum('pab,mpb->mpa',I,zi)/gamma[None,:,None]-A[:,:,None]*up[None]/gamma[None,:,None]**3)
 rawkeep('JzU',JzU)
 wh=-np.einsum('pij,ajk,pk->pai',I,e,up);gh=-np.einsum('pi,aij,pj->pa',up,e,up)/(2*gamma[:,None])
 Uh=np.concatenate(((gh/N[:,None])[:,:,None],wh-beta[:,None,:]*(gh/N[:,None])[:,:,None]),axis=2)
 rawkeep('Uh',Uh)
 zh=-N[None,:,None]*(np.einsum('pai,jpi->jpa',wh,zi)/gamma[None,:,None]-A[:,:,None]*gh[None]/gamma[None,:,None]**2)
 rawkeep('zh',zh)
 embed=np.zeros((p,6,4,4));embed[:,:,1:,1:]=e[None];embed[:,:,0,1:]=embed[:,:,1:,0]=np.einsum('aij,pj->pai',e,beta);embed[:,:,0,0]=np.einsum('pi,aij,pj->pa',beta,e,beta)
 rawkeep('embed',embed)
 dens=N*mu;c=dict(h=h,ih=I,N=N,beta=beta,u=u,up=up,gamma=gamma,JU=JU,Jzz=Jzz,JzU=JzU,Uh=Uh,zh=zh,embed=embed,dens=dens,sqrt_h=mu)
 s=dict(g=g,hi=hi,U=U,z=z,uc=uc,P=projector,Z=Z,r=r,z2=z2,f=f,phi=phi,omega=omega,xi=xi,w=weight,R=material['R'],Z_coordinate=material['Z_coordinate'])
 eh=abs(h);eI=abs(I);eb=abs(beta);ehb=np.einsum('pij,pj->pi',eh,eb);eg=abs(g).copy();eg[:,0,0]=N*N+np.einsum('pi,pi->p',eb,ehb);eg[:,0,1:]=eg[:,1:,0]=ehb
 ehi=abs(hi).copy();ehi[:,1:,1:]=eI+eb[:,:,None]*eb[:,None,:]/N[:,None,None]**2
 eU=np.column_stack((gamma/N,eup+eb*gamma[:,None]/N[:,None]));eA=np.einsum('pi,jpi->jp',eup,abs(zi));ez=np.concatenate(((np.einsum('pi,jpi->jp',eb,abs(zi))+N[None]*eA/gamma[None])[:,:,None],abs(zi)),axis=2)
 euc=np.einsum('pab,pb->pa',eg,eU);eP=np.eye(4)[None]+euc[:,:,None]*eU[:,None,:];ez2=np.einsum('jpa,pab,jpb->jp',ez,ehi,ez)
 eJU=np.empty_like(JU);eJU[:,0]=eup/(N*gamma)[:,None];eJU[:,1:]=eI+eb[:,:,None]*eJU[:,None,0]
 ewh=np.einsum('pij,ajk,pk->pai',eI,abs(e),eup);egh=np.einsum('pi,aij,pj->pa',eup,abs(e),eup)/(2*gamma[:,None])
 eUh=np.concatenate(((egh/N[:,None])[:,:,None],ewh+eb[:,None,:]*(egh/N[:,None])[:,:,None]),axis=2)
 bounds=dict(h=eh,ih=eI,N=abs(N),beta=eb,u=abs(u),up=eup,gamma=np.sqrt(eq),dens=abs(dens),sqrt_h=abs(mu),g=eg,hi=ehi,U=eU,z=ez,uc=euc,P=eP,Z=np.einsum('j,jpa->pa',abs(weight),ez),r=np.einsum('pab,pb->pa',eP,abs(phi)),z2=ez2,f=1+ez2/ki[:,None],phi=abs(phi),omega=abs(omega),xi=abs(xi),w=abs(weight),JU=eJU,Jzz=eb+N[:,None]*eup/gamma[:,None],JzU=N[None,:,None]*(np.einsum('pab,mpb->mpa',eI,abs(zi))/gamma[None,:,None]+eA[:,:,None]*eup[None]/gamma[None,:,None]**3),Uh=eUh,zh=N[None,:,None]*(np.einsum('pai,jpi->jpa',ewh,abs(zi))/gamma[None,:,None]+eA[:,:,None]*egh[None]/gamma[None,:,None]**2),embed=abs(embed))
 for family,values in (('configuration',s),('chart',c)):
  for n,v in values.items():keep(label+'_'+family+'_'+n,np.asarray(v).copy())
 for n,b in bounds.items():keep(label+'_coefficient_operation_'+n,np.asarray(b).copy())
 fa_gap(label+'_local_raw_up_dot_zi',fy_sum(P.a_prod(up[None],zi),-1),A,eA,keep)
 fa_coefficient_construction_contacts(s,c,bounds,ki,keep,label+'_local_raw_coefficient_construction')
 for n in ('g','hi','U','z','uc','P','up','gamma','dens'):
  fa_gap(label+'_model_'+n,spacetime['value'][n],s[n] if n in s else c[n],bounds[n],keep)
 for n,actual in (('h',h),('ih',I),('mu',mu)):fa_gap(label+'_geometry_'+n,geometry[n],actual,bounds['sqrt_h' if n=='mu' else n],keep)
 for n,v in spacetime['delta'].items():put('retained_paired_model_direction_'+n,v)
 put('new_spatial_inverse_residual',P.a_sub(fy_mm(P.a_dd(h),P.a_dd(I)),P.a_dd(np.broadcast_to(np.eye(3),(p,3,3)))))
 put('new_spacetime_inverse_residual',P.a_sub(fy_mm(P.a_dd(g),P.a_dd(hi)),P.a_dd(np.broadcast_to(np.eye(4),(p,4,4)))))
 put('raw_unit_constraint',P.a_add(fy_sum(P.a_prod(U,uc),1),P.a_dd(np.ones(p))));put('raw_transverse_constraint',fy_sum(P.a_prod(U[None],z),2))
 put('direct_minus_quotient_Jzz',P.a_sub(P.a_dd(Jzz),P.a_div64(P.a_dd(-U[:,1:]),U[:,0,None],keep,label+'_quotient_Jzz')))
 for n,actual,matrix,denominator in (('JzU',JzU,JU,U[None,:,0,None]),('zh',zh,Uh.swapaxes(-1,-2),U[None,:,0,None])):
  numerator=P.a_dd(np.zeros(actual.shape))
  for a in range(4):numerator=P.a_sub(numerator,P.a_prod(z[:,:,a,None],matrix[None,:,a]))
  put('direct_minus_quotient_'+n,P.a_sub(P.a_dd(actual),P.a_div64(numerator,denominator,keep,label+'_quotient_'+n)))
 hfirst=P.a_stack([mechanical['h_dot'],P.a_slice(geometry['h_spatial_jets'],(slice(None),0)),P.a_slice(geometry['h_spatial_jets'],(slice(None),1)),P.a_dd(np.zeros((p,3,3)))],1)
 jets,op=fa_new_first_jets(s,c,hfirst,gauge['N_jets'],gauge['beta_jets'],covectors['u_jets'],covectors['z_jets'],reference['E0'],keep,label+'_new_first')
 for n,v in jets.items():put('model_minus_new_raw_chart_first_'+n,P.a_sub(spacetime['value'][n],v))
 for n in ('g','hi','U','z','du','dz','dg','Ga'):
  actual=P.a_dd(s[n]) if n in s else jets[n];put('new_candidate_minus_owned_reference_'+n,P.a_sub(actual,reference[n]))
 assert feature_fn is P.paired_current_affine_features and momentum_fn is P.paired_current_affine_momenta
 feature=feature_fn(s,c,jets,keep,label+'_NEW_feature')
 feature['candidate_configuration_rebuilt']=True
 for n,v in feature['paired'].items():put('completed_NEW_feature_'+n,v)
 momentum=momentum_fn(s,c,feature,jets,keep,label+'_NEW_momentum')
 for n,v in momentum.items():put('completed_NEW_momentum_'+n,v)
 Lie=P.a_dd(np.zeros((p,3,3)))
 for k in range(3):Lie=P.a_add(Lie,P.a_mul64(beta[:,k,None,None],P.a_slice(hfirst,(slice(None),k+1))))
 for i in range(3):
  for j in range(3):
   value=P.a_add(fy_sum(P.a_mul64(h[:,j],P.a_slice(gauge['beta_jets'],(slice(None),i+1))),1),fy_sum(P.a_mul64(h[:,i],P.a_slice(gauge['beta_jets'],(slice(None),j+1))),1))
   total=P.a_add(P.a_slice(Lie,(slice(None),i,j)),value);Lie[0][:,i,j]=total[0];Lie[1][:,i,j]=total[1];put('current_Lie_beta_h',Lie)
 KADM=P.a_div64(P.a_sub(mechanical['h_dot'],Lie),2*N[:,None,None],keep,label+'_KADM');KG=momentum['K'];put('Lie_beta_h',Lie);put('KADM',KADM);put('KGamma_minus_KADM',P.a_sub(KG,KADM))
 tadm=fy_contract(P.a_dd(I),KADM);put('Ktrace_Gamma_minus_ADM',P.a_sub(momentum['Ktrace'],tadm))
 return dict(s=s,c=c,jets=jets,features=feature,momenta=momentum,positive_first_jet_envelopes=op,coefficient_envelopes=bounds,KADM=KADM,canonical_target_references=reference['canonical_targets'],prior_bridge_references=reference['prior_bridge_references'],original_offsets_refitted=False,candidate_action_JVP_evaluated=False,phase_EOS_or_normal_weakrows_evaluated=False,physical_adoption=False)

def math_is_finite_positive(x):return type(x) in (int,float) and np.isfinite(x) and x>0
