"""Held NEW native+EH action normal and common-configuration JVP.
Globals np,P and reviewed fs_*/fy_* helpers; no invocation or saved payload.
Consumes the SAME225 raw candidate/NEW contact. Every native normal test is
derived from owned gauge/covector firstjets and the fixed lowered-E0 algebraic
connection, retaining all t/R/Z/phi testjet coefficients. No Noether, old134
covariant-connection or KADM identity substitutes for the actual test contact.
Relative phase belongs to root's62 core once; it is absent from this action.
NEW intrinsic curvature is rebuilt from candidate h/inverse/spatial jets;
the reference cylindrical connection, constants and integration basis stay fixed.
The old simplified EH normal is a comparison; primary/boundary physical ports
and finite candidate/canonical admission remain separate and unevaluated.
"""
FINITE_CANDIDATE_NORMAL_AUTHOR_DRAFT=True
FINITE_CANDIDATE_NORMAL_AUTHORING_IN_PROGRESS=False

def fn_abs(pair):return abs(pair[0])+abs(pair[1])

def fn_contract(A,B):return fs_sum(fs_sum(fs_mul(A,B),-1),-1)

def fn_divide_constant(value,denominator,keep,label):
 out=(P.a_div64(value[0],denominator,keep,label+'_value'),P.a_div64(value[1],denominator,keep,label+'_direction'))
 fs_keep(label+'_result',out,keep)
 fs_keep(label+'_division_contact_residual',fs_sub(fs_scale(denominator,out),value),keep);return out

def finite_candidate_intrinsic_curvature(candidate,contact,keep,label):
 S=contact['state'];I,hfirst,mu=S['ih'],S['h_first'],S['mu'];p=len(candidate['c']['N']);R=candidate['s']['R']
 assert R.shape==(p,) and np.all(np.isfinite(R)) and np.all(R>0)
 put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 dh=fs_slice(hfirst,(slice(None),slice(1,None)));rows=[]
 eI=abs(candidate['c']['ih']);eI1=fn_abs(I[1]);eh=fn_abs(dh[0]);eh1=fn_abs(dh[1]);eG=np.zeros((p,3,3,3));eG1=np.zeros_like(eG)
 for i in range(3):
  columns=[]
  for j in range(3):
   cycle=fs_sub(fs_add(fs_slice(dh,(slice(None),i,j,slice(None))),fs_slice(dh,(slice(None),j,i,slice(None)))),fs_slice(dh,(slice(None),slice(None),i,j)))
   columns.append(fs_scale(.5,fs_mv(I,cycle)))
   ec=eh[:,i,j]+eh[:,j,i]+eh[:,:,i,j];ec1=eh1[:,i,j]+eh1[:,j,i]+eh1[:,:,i,j]
   eG[:,:,i,j]=.5*np.einsum('pkl,pl->pk',eI,ec);eG1[:,:,i,j]=.5*(np.einsum('pkl,pl->pk',eI1,ec)+np.einsum('pkl,pl->pk',eI,ec1))
  rows.append(fs_stack(columns,-1));put('current_Gamma3',fs_stack(rows,-2))
 G=put('Gamma3',fs_stack(rows,-2));bar=np.zeros((p,3,3,3));bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 keep(label+'_fixed_cylindrical_reference_connection',bar.copy());C3=put('C3',fs_sub(G,fs_dual(P.a_dd(bar))))
 eC=eG+abs(bar);q=fs_dual(P.a_dd(np.zeros(p)));v=fs_dual(P.a_dd(np.zeros((p,3))));eq=np.zeros(p);eq1=np.zeros(p);ev=np.zeros((p,3));ev1=np.zeros_like(ev)
 for i in range(3):
  for j in range(3):
   for k in range(3):
    for l in range(3):
     for sign,a,b in ((1.,(k,i,l),(l,j,k)),(-1.,(k,i,j),(l,k,l))):
      ca=fs_slice(C3,(slice(None),*a));cb=fs_slice(C3,(slice(None),*b));ii=fs_slice(I,(slice(None),i,j))
      q=fs_add(q,fs_scale(sign,fs_mul(ii,fs_mul(ca,cb))))
      ea=eC[:,a[0],a[1],a[2]];eb=eC[:,b[0],b[1],b[2]];ea1=eG1[:,a[0],a[1],a[2]];eb1=eG1[:,b[0],b[1],b[2]]
      eq+=eI[:,i,j]*ea*eb;eq1+=eI1[:,i,j]*ea*eb+eI[:,i,j]*(ea1*eb+ea*eb1)
    for sign,ii,jj,a in ((1.,i,j,(k,i,j)),(-1.,i,k,(j,i,j))):
     ca=fs_slice(C3,(slice(None),*a));term=fs_scale(sign,fs_mul(fs_slice(I,(slice(None),ii,jj)),ca))
     updated=fs_add(fs_slice(v,(slice(None),k)),term)
     for word in (0,1):v[0][word][:,k]=updated[0][word];v[1][word][:,k]=updated[1][word]
     ea=eC[:,a[0],a[1],a[2]];ea1=eG1[:,a[0],a[1],a[2]];ev[:,k]+=eI[:,ii,jj]*ea;ev1[:,k]+=eI1[:,ii,jj]*ea+eI[:,ii,jj]*ea1
   put('current_Q_polynomial',q);put('current_V_polynomial',v)
 Q=put('Q',fs_mul(mu,q));V=put('V',fs_mul(fs_expand(mu,(Ellipsis,None)),v))
 em=fn_abs(mu[0]);em1=fn_abs(mu[1]);bounds=dict(Gamma3=eG,delta_Gamma3=eG1,C3=eC,delta_C3=eG1,Q=em*eq,delta_Q=em1*eq+em*eq1,V=em[:,None]*ev,delta_V=em1[:,None]*ev+em[:,None]*ev1)
 for n,x in bounds.items():keep(label+'_uncancelled_operation_'+n,np.asarray(x).copy())
 return dict(Q=Q,V=V,Gamma3=G,C3=C3,operation_envelopes=bounds,old_curvature_transported=False)

def finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,Hbar,reference,keep,label):
 s,c=candidate['s'],candidate['c'];S=contact['state'];p=len(c['N']);put=lambda n,x:fs_keep(label+'_'+n,x,keep)
 for x,shape in ((f,(p,)),(df,(p,4)),(b,(p,3)),(db,(p,4,3))):assert x.dtype==np.float64 and x.shape==shape and np.all(np.isfinite(x))
 for n,x in (('f',f),('df',df),('b',b),('db',db)):keep(label+'_fixed_test_'+n,x.copy())
 N,beta,h,I,g,hi,U,z,uc,projector,ha,Na,ba=(S[n] for n in ('N','beta','h','ih','g','hi','U','z','uc','P','h_first','N_first','beta_first'))
 ft,bt=fs_dual(P.a_dd(f)),fs_dual(P.a_dd(b));zero=fs_dual(P.a_dd(np.zeros((p,3,3))))
 hb=fs_mv(h,bt);q=put('metric_test',fs_block(fs_add(fs_scale(-2.,fs_mul(N,ft)),fs_scale(2.,fs_dot(beta,hb))),hb,zero))
 It=put('inverse_metric_test',fs_neg(fs_mm(fs_mm(hi,q),hi)))
 invN2=fs_div(fs_dual(P.a_dd(np.ones(p))),fs_mul(N,N),keep,label+'_inverse_N2')
 invN3=fs_div(invN2,N,keep,label+'_inverse_N3')
 i00=fs_scale(2.,fs_mul(ft,invN3));i0=fs_sub(fs_mul(fs_expand(invN2,(Ellipsis,None)),bt),fs_mul(fs_expand(fs_scale(2.,fs_mul(ft,invN3)),(Ellipsis,None)),beta))
 bb=fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(beta,(Ellipsis,None,slice(None))))
 dbb=fs_add(fs_mul(fs_expand(bt,(Ellipsis,slice(None),None)),fs_expand(beta,(Ellipsis,None,slice(None)))),fs_mul(fs_expand(beta,(Ellipsis,slice(None),None)),fs_expand(bt,(Ellipsis,None,slice(None)))))
 iij=fs_sub(fs_mul(fs_expand(fs_scale(2.,fs_mul(ft,invN3)),(Ellipsis,None,None)),bb),fs_mul(fs_expand(invN2,(Ellipsis,None,None)),dbb))
 ADMIt=put('direct_ADM_inverse_metric_test',fs_block(i00,i0,iij))
 put('formal_minus_direct_ADM_inverse_metric_test',fs_sub(It,ADMIt))
 put('inverse_matrix_primary_test_contact',fs_add(fs_mm(q,hi),fs_mm(g,It)))
 eta0=fs_neg(fs_div(fs_mul(fs_slice(U,(slice(None),0)),ft),N,keep,label+'_eta0'))
 etai=fs_sub(fs_neg(fs_mul(fs_expand(fs_slice(U,(slice(None),0)),(Ellipsis,None)),bt)),fs_mul(beta,fs_expand(eta0,(Ellipsis,None))))
 eta=put('native_test',fs_stack([eta0]+[fs_slice(etai,(slice(None),i)) for i in range(3)],1))
 zi=fs_slice(z,(slice(None),slice(None),slice(1,None)));A=S['A'];gamma=S['gamma']
 zt0=fs_sub(fs_dot(fs_expand(bt,(None,Ellipsis)),zi),fs_div(fs_mul(fs_expand(ft,(None,Ellipsis)),A),fs_expand(gamma,(None,Ellipsis)),keep,label+'_z0_test'))
 zt=put('modal_test',fs_stack([zt0]+[fs_dual(P.a_dd(np.zeros((32,p)))) for _ in range(3)],2))
 numerator=fs_dot(fs_expand(eta,(None,Ellipsis)),z)
 ztquot=fs_div(fs_neg(numerator),fs_expand(fs_slice(U,(slice(None),0)),(None,Ellipsis)),keep,label+'_registered_quotient_z0_test')
 put('direct_minus_registered_quotient_z0_test',fs_sub(zt0,ztquot))
 qrows=[];etarows=[];ztrows=[];quotient_zrows=[];recovered_n=[];recovered_b=[]
 for a in range(4):
  n=fs_slice(Na,(slice(None),a));baj=fs_slice(ba,(slice(None),a));H=fs_slice(ha,(slice(None),a));dfa=fs_dual(P.a_dd(df[:,a]));dba=fs_dual(P.a_dd(db[:,a]))
  q0a=fs_add(fs_scale(-2.,fs_add(fs_mul(n,ft),fs_mul(N,dfa))),fs_scale(2.,fs_add(fs_add(fs_dot(baj,hb),fs_dot(beta,fs_mv(H,bt))),fs_dot(beta,fs_mv(h,dba)))))
  qrows.append(fs_block(q0a,fs_add(fs_mv(H,bt),fs_mv(h,dba)),zero))
  U0a=fs_slice(S['du'],(slice(None),a,0));U0=fs_slice(U,(slice(None),0))
  e0a=fs_add(fs_neg(fs_div(fs_add(fs_mul(U0a,ft),fs_mul(U0,dfa)),N,keep,label+'_eta_first_'+str(a))),fs_div(fs_mul(fs_mul(U0,ft),n),fs_mul(N,N),keep,label+'_eta_second_'+str(a)))
  eia=fs_sub(fs_sub(fs_neg(fs_add(fs_mul(fs_expand(U0a,(Ellipsis,None)),bt),fs_mul(fs_expand(U0,(Ellipsis,None)),dba))),fs_mul(baj,fs_expand(eta0,(Ellipsis,None)))),fs_mul(beta,fs_expand(e0a,(Ellipsis,None))))
  etarows.append(fs_stack([e0a]+[fs_slice(eia,(slice(None),i)) for i in range(3)],1))
  za=fs_slice(S['z_spatial_first'],(slice(None),slice(None),a));wa=fs_slice(S['up_first'],(slice(None),a));ga=fs_slice(S['gamma_first'],(slice(None),a))
  Aa=fs_add(fs_dot(fs_expand(wa,(None,Ellipsis)),zi),fs_dot(fs_expand(S['up'],(None,Ellipsis)),za))
  numerator_a=fs_add(fs_mul(fs_expand(dfa,(None,Ellipsis)),A),fs_mul(fs_expand(ft,(None,Ellipsis)),Aa))
  z0a=fs_add(fs_sub(fs_add(fs_dot(fs_expand(dba,(None,Ellipsis)),zi),fs_dot(fs_expand(bt,(None,Ellipsis)),za)),fs_div(numerator_a,fs_expand(gamma,(None,Ellipsis)),keep,label+'_ztest_first_'+str(a))),fs_div(fs_mul(fs_mul(fs_expand(ft,(None,Ellipsis)),A),fs_expand(ga,(None,Ellipsis))),fs_expand(fs_mul(gamma,gamma),(None,Ellipsis)),keep,label+'_ztest_second_'+str(a)))
  ztrows.append(fs_stack([z0a]+[fs_dual(P.a_dd(np.zeros((32,p)))) for _ in range(3)],2))
  efirst=fs_add(fs_dot(fs_expand(etarows[-1],(None,Ellipsis)),z),fs_dot(fs_expand(eta,(None,Ellipsis)),fs_slice(S['dz'],(slice(None),slice(None),a))))
  zr=fs_add(fs_div(fs_neg(efirst),fs_expand(U0,(None,Ellipsis)),keep,label+'_quotient_test_first_'+str(a)),fs_div(fs_mul(numerator,fs_expand(U0a,(None,Ellipsis))),fs_expand(fs_mul(U0,U0),(None,Ellipsis)),keep,label+'_quotient_test_second_'+str(a)))
  quotient_zrows.append(zr)
  inverse_jet=fs_neg(fs_mm(fs_mm(hi,fs_slice(S['dg'],(slice(None),a))),hi))
  nr=fs_scale(c['N']**3/2,fs_slice(inverse_jet,(slice(None),0,0)));recovered_n.append(nr)
  br=fs_add(fs_mul(fs_scale(2.,fs_mul(fs_expand(N,(Ellipsis,None)),fs_slice(hi,(slice(None),0,slice(1,None))))),fs_expand(nr,(Ellipsis,None))),fs_mul(fs_expand(fs_mul(N,N),(Ellipsis,None)),fs_slice(inverse_jet,(slice(None),0,slice(1,None)))))
  recovered_b.append(br)
  put('current_metric_test_first',fs_stack(qrows,1));put('current_native_test_first',fs_stack(etarows,1));put('current_modal_test_first',fs_stack(ztrows,2))
 qt=put('metric_test_first',fs_stack(qrows,1));etat=put('native_test_first',fs_stack(etarows,1));ztt=put('modal_test_first',fs_stack(ztrows,2))
 put('direct_minus_registered_quotient_modal_test_first',fs_sub(fs_slice(ztt,(slice(None),slice(None),slice(None),0)),fs_stack(quotient_zrows,2)))
 put('owned_minus_inverse_recovered_gauge_N_first',fs_sub(Na,fs_stack(recovered_n,1)));put('owned_minus_inverse_recovered_gauge_beta_first',fs_sub(ba,fs_stack(recovered_b,1)))
 nabla=[]
 for a in range(4):
  G=fs_slice(S['Ga'],(slice(None),slice(None),a,slice(None)))
  nabla.append(fs_sub(fs_slice(qt,(slice(None),a)),fs_add(fs_mm(fs_transpose(G,(0,2,1)),q),fs_mm(q,G))))
 nabla=put('covariant_metric_test_first',fs_stack(nabla,1))
 shifted=fs_sub(S['dg'],fs_dual(reference['E0']));Grows=[];covrows=[]
 for a in range(4):
  columns=[];covcolumns=[]
  for k in range(4):
   cycle=fs_sub(fs_add(fs_slice(shifted,(slice(None),a,k,slice(None))),fs_slice(shifted,(slice(None),k,a,slice(None)))),fs_slice(shifted,(slice(None),slice(None),a,k)))
   cyclet=fs_sub(fs_add(fs_slice(qt,(slice(None),a,k,slice(None))),fs_slice(qt,(slice(None),k,a,slice(None)))),fs_slice(qt,(slice(None),slice(None),a,k)))
   columns.append(fs_scale(.5,fs_add(fs_mv(It,cycle),fs_mv(hi,cyclet))))
   covcycle=fs_sub(fs_add(fs_slice(nabla,(slice(None),a,k,slice(None))),fs_slice(nabla,(slice(None),k,a,slice(None)))),fs_slice(nabla,(slice(None),slice(None),a,k)))
   covcolumns.append(fs_scale(.5,fs_mv(hi,covcycle)))
  Grows.append(fs_stack(columns,-1));covrows.append(fs_stack(covcolumns,-1));put('current_algebraic_connection_test',fs_stack(Grows,-2))
 Gt=put('algebraic_connection_test',fs_stack(Grows,-2));put('algebraic_minus_covariant_connection_test',fs_sub(Gt,fs_stack(covrows,-2)))
 F={n:fs_dual(x,contact['delta_features']['paired'][n]) for n,x in candidate['features']['paired'].items() if n in contact['delta_features']['paired']}
 nut=etat;nzt=ztt
 for l in range(4):
  Gtl=fs_transpose(fs_slice(Gt,(slice(None),slice(None),slice(None),l)),(0,2,1));Gl=fs_transpose(fs_slice(S['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))
  nut=fs_add(nut,fs_add(fs_mul(fs_expand(fs_slice(U,(slice(None),l)),(Ellipsis,None,None)),Gtl),fs_mul(fs_expand(fs_slice(eta,(slice(None),l)),(Ellipsis,None,None)),Gl)))
  nzt=fs_sub(nzt,fs_add(fs_mul(fs_expand(fs_slice(z,(slice(None),slice(None),l)),(Ellipsis,None,None)),fs_slice(Gt,(slice(None),l))),fs_mul(fs_expand(fs_slice(zt,(slice(None),slice(None),l)),(Ellipsis,None,None)),fs_slice(S['Ga'],(slice(None),l)))))
  put('current_covariant_native_test',nut);put('current_covariant_modal_test',nzt)
 qmodal=fs_dual(P.a_dd(np.zeros((32,p,4))));at=fs_dual(P.a_dd(np.zeros((p,4))))
 for a in range(4):
  qmodal=fs_add(qmodal,fs_add(fs_mul(fs_expand(fs_slice(eta,(slice(None),a)),(None,Ellipsis,None)),fs_slice(F['nz'],(slice(None),slice(None),a))),fs_mul(fs_expand(fs_slice(U,(slice(None),a)),(None,Ellipsis,None)),fs_slice(nzt,(slice(None),slice(None),a)))))
  at=fs_add(at,fs_add(fs_mul(fs_expand(fs_slice(eta,(slice(None),a)),(Ellipsis,None)),fs_slice(F['nu'],(slice(None),a))),fs_mul(fs_expand(fs_slice(U,(slice(None),a)),(Ellipsis,None)),fs_slice(nut,(slice(None),a)))))
 uct=fs_add(fs_mv(q,U),fs_mv(g,eta));Pt=put('projector_test',fs_add(fs_mul(fs_expand(uct,(Ellipsis,slice(None),None)),fs_expand(U,(Ellipsis,None,slice(None)))),fs_mul(fs_expand(uc,(Ellipsis,slice(None),None)),fs_expand(eta,(Ellipsis,None,slice(None))))))
 put('native_unit_primary_test_contact',fs_add(fs_dot(eta,uc),fs_dot(U,uct)));put('modal_transversality_primary_test_contact',fs_add(fs_dot(fs_expand(eta,(None,Ellipsis)),z),fs_dot(fs_expand(U,(None,Ellipsis)),zt)))
 Vt=put('V_test',fs_add(fs_mv(Pt,F['q']),fs_mv(projector,qmodal)))
 Dt=put('D_test',fs_add(fs_add(fs_mm(fs_mm(Pt,F['nz']),fs_transpose(projector,(0,2,1))),fs_mm(fs_mm(projector,nzt),fs_transpose(projector,(0,2,1)))),fs_mm(fs_mm(projector,F['nz']),fs_transpose(Pt,(0,2,1)))))
 lowert=fs_add(fs_mm(nut,g),fs_mm(F['nu'],q));Ft=put('F_test',fs_sub(lowert,fs_transpose(lowert,(0,2,1))))
 Vut=fs_add(fs_mv(It,F['V']),fs_mv(hi,Vt));Dut=fs_add(fs_add(fs_mm(fs_mm(It,F['D']),hi),fs_mm(fs_mm(hi,Dt),hi)),fs_mm(fs_mm(hi,F['D']),It))
 Fut=fs_add(fs_add(fs_mm(fs_mm(It,F['F']),hi),fs_mm(fs_mm(hi,Ft),hi)),fs_mm(fs_mm(hi,F['F']),It))
 V2=fs_dot(F['V_raised'],F['V']);V2t=fs_add(fs_dot(Vut,F['V']),fs_dot(F['V_raised'],Vt))
 D2=fn_contract(F['D_raised'],F['D']);D2t=fs_add(fn_contract(Dut,F['D']),fn_contract(F['D_raised'],Dt))
 F2=fn_contract(F['Fup'],F['F']);F2t=fs_add(fn_contract(Fut,F['F']),fn_contract(F['Fup'],Ft))
 z2t=put('z_squared_test',fs_add(fs_dot(zt,fs_mv(hi,z)),fs_dot(z,fs_add(fs_mv(It,z),fs_mv(hi,zt)))))
 az=fs_dot(z,fs_expand(F['a'],(None,Ellipsis)));azt=fs_add(fs_dot(zt,fs_expand(F['a'],(None,Ellipsis))),fs_dot(z,fs_expand(at,(None,Ellipsis))))
 om=s['omega'][:,None]**2;kj=(P.B*P.GC)**2*s['xi'][:,None]**4
 modal=fs_stack([fn_divide_constant(V2,2*om,keep,label+'_primal_frequency'),fs_scale(-.5,S['z2']),fn_divide_constant(fs_neg(fs_mul(S['z2'],S['z2'])),4*kj,keep,label+'_primal_quartic'),fs_scale(-P.ELL**2/2,D2),az],-1)
 modalt=fs_stack([fn_divide_constant(V2t,2*om,keep,label+'_test_frequency'),fs_scale(-.5,z2t),fn_divide_constant(fs_neg(fs_mul(S['z2'],z2t)),2*kj,keep,label+'_test_quartic'),fs_scale(-P.ELL**2/2,D2t),azt],-1)
 modal=fs_sum(fs_scale(s['w'][:,None,None],modal),0);modalt=fs_sum(fs_scale(s['w'][:,None,None],modalt),0)
 primal=put('native_primal_terms',fs_stack([fs_scale(-P.ALPHA/4,F2)]+[fs_slice(modal,(slice(None),i)) for i in range(5)],1))
 variation=put('native_test_terms',fs_stack([fs_scale(-P.ALPHA/4,F2t)]+[fs_slice(modalt,(slice(None),i)) for i in range(5)],1))
 lm=put('measure_test',fs_div(ft,N,keep,label+'_lapse_measure'))
 put('measure_test_minus_inverse_trace',fs_sub(lm,fs_scale(.5,fn_contract(hi,fs_transpose(q,(0,2,1))))))
 native=put('native_action',fs_mul(S['dens'],fs_sum(fs_add(variation,fs_mul(fs_expand(lm,(Ellipsis,None)),primal)),1)))
 K=fs_dual(candidate['momenta']['K'],contact['delta_momenta']['K']);tau=fs_dual(candidate['momenta']['Ktrace'],contact['delta_momenta']['Ktrace'])
 Kt=put('KGamma_test',fs_add(fs_mul(fs_expand(ft,(Ellipsis,None,None)),fs_slice(S['Ga'],(slice(None),0,slice(1,None),slice(1,None)))),fs_mul(fs_expand(N,(Ellipsis,None,None)),fs_slice(Gt,(slice(None),0,slice(1,None),slice(1,None))))))
 Kup=fs_mm(fs_mm(I,K),I);Ktu=fs_mm(fs_mm(I,Kt),I);taut=fn_contract(I,Kt)
 kin=fs_sub(fn_contract(K,Kup),fs_mul(tau,tau));kint=fs_sub(fs_add(fn_contract(Kt,Kup),fn_contract(K,Ktu)),fs_scale(2.,fs_mul(tau,taut)))
 EHkin=put('EH_direct_kinetic_action',fn_divide_constant(fs_add(fs_mul(fs_mul(ft,S['mu']),kin),fs_mul(S['dens'],kint)),2*P.C,keep,label+'_EH_kinetic_division'))
 EHcurv=fs_mul(ft,curvature['Q'])
 for i in range(3):EHcurv=fs_sub(EHcurv,fs_scale(df[:,i+1],fs_slice(curvature['V'],(slice(None),i))))
 EHcurv=put('EH_curvature_action',fn_divide_constant(EHcurv,2*P.C,keep,label+'_EH_curvature_division'));EH=put('EH_action',fs_add(EHkin,EHcurv))
 Lie=fs_dual(P.a_dd(np.zeros((p,3,3))))
 for i in range(3):Lie=fs_add(Lie,fs_scale(b[:,i,None,None],fs_slice(ha,(slice(None),i+1))))
 Lcols=[]
 for i in range(3):Lcols.append(fs_stack([fs_add(fs_slice(Lie,(slice(None),i,j)),fs_add(fs_dot(fs_slice(h,(slice(None),i)),fs_dual(P.a_dd(db[:,j+1]))),fs_dot(fs_slice(h,(slice(None),j)),fs_dual(P.a_dd(db[:,i+1]))))) for j in range(3)],-1))
 Lie=put('Lie_test_h',fs_stack(Lcols,-2));KADMtest=put('KADM_test',fs_sub(fs_neg(fs_mul(fs_expand(lm,(Ellipsis,None,None)),S['KADM'])),fs_div(Lie,fs_expand(fs_scale(2.,N),(Ellipsis,None,None)),keep,label+'_KADM_test_division')))
 put('KGamma_minus_KADM_test',fs_sub(Kt,KADMtest))
 pi=fs_dual(candidate['momenta']['metric_EH_tensor'],contact['delta_momenta']['metric_EH_tensor'])
 simplified=fs_sub(fn_divide_constant(fs_neg(fs_mul(fs_mul(ft,S['mu']),kin)),2*P.C,keep,label+'_EH_registered_kinetic_division'),fn_contract(pi,Lie))
 put('EH_direct_minus_registered_kinetic_shift',fs_sub(EHkin,simplified))
 theta=put('initial_CMC_density',fs_mul(S['mu'],fs_sub(tau,fs_dual(P.a_dd(np.full(p,3*Hbar))))))
 action=put('native_EH_action',fs_add(native,EH));hamiltonian=put('native_EH_Hamiltonian',fs_neg(action))
 return dict(value=dict(native=native[0],EH=EH[0],action=action[0],hamiltonian=hamiltonian[0],initial_CMC_density=theta[0]),delta=dict(native=native[1],EH=EH[1],action=action[1],hamiltonian=hamiltonian[1],initial_CMC_density=theta[1]),tests=dict(q=q,eta=eta,zeta=zt,q_first=qt,eta_first=etat,zeta_first=ztt,Gamma=Gt),relative_phase_included=False,all_four_coordinate_test_jets_retained=True,global_weak_rows_assembled=False,physical_primary_or_boundary_ports_admitted=False,finite_candidate_physically_admitted=False)

def finite_candidate_total_normal(native_EH,phase,ordinary,f,b,keep,label):
 # Same published geometry transaction and original once-counted labels required.
 assert native_EH['relative_phase_included'] is False and phase['relative_phase_included_once'] is True
 action=fs_dual(native_EH['value']['action'],native_EH['delta']['action'])
 phase_action=fs_dual(phase['value']['action'],phase['delta']['action'])
 ordinary_normal=fs_dual(ordinary['value']['normal_density'],ordinary['delta']['normal_density'])
 tests=np.column_stack((f,b));ordinary_H=fs_sum(fs_scale(tests,ordinary_normal),1)
 fs_keep(label+'_once_counted_ordinary_Hamiltonian',ordinary_H,keep)
 total=fs_keep(label+'_total_action',fs_sub(fs_add(action,phase_action),ordinary_H),keep);H=fs_keep(label+'_total_Hamiltonian',fs_neg(total),keep)
 return dict(value=dict(action=total[0],hamiltonian=H[0]),delta=dict(action=total[1],hamiltonian=H[1]),relative_phase_count=1,ordinary_label_count=1,finite_candidate_physically_admitted=False)

def finite_candidate_test_polynomials(normal_test,scalar_test,basis,keep,label):
 # N supplies only the unchanged registered normal hats/masks/scatter definitions.
 assert normal_test.shape==(4,87,45) and scalar_test.shape==(87,45)
 assert np.all(normal_test[~N.normal_test_mask()]==0) and np.all(scalar_test[~P.scalar_mask()]==0)
 t=N.extend_normal_tests(normal_test);u=P.scalar_lift(scalar_test)
 tv=P.a_dd(np.zeros((15136,4,3)));sv=P.a_dd(np.zeros(15136))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    for jet,hat in enumerate(N.normal_hat_jet(basis,iq,corner,row)):
     term=P.a_prod(t[row,di:86+di,dj:44+dj],hat);term=(term[0].reshape(3784),term[1].reshape(3784))
     value=P.a_add(P.a_slice(tv,(sl,row,jet)),term)
     for word in (0,1):tv[word][sl,row,jet]=value[word]
     fy_keep(label+'_current_normal_polynomial',tv,keep)
   term=P.a_prod(u[di:86+di,dj:44+dj],basis['hats'][iq,corner,0]);term=(term[0].reshape(3784),term[1].reshape(3784));value=P.a_add(P.a_slice(sv,sl),term)
   for word in (0,1):sv[word][sl]=value[word]
   fy_keep(label+'_current_CMC_polynomial',sv,keep)
 return tv,sv

def finite_candidate_global_normal_CMC(columns,basis,normal_test,scalar_test,keep,check,label):
 assert len(columns)==4 and basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert np.all(basis['R']>0) and np.all(basis['dv']>0)
 tv,sv=finite_candidate_test_polynomials(normal_test,scalar_test,basis,keep,label+'_independent_test');weight=(basis['dv']/basis['R']).reshape(15136);result={}
 for family in ('value','delta'):
  value=P.a_dd(np.zeros((15136,4,3)));primary=P.a_dd(np.zeros((15136,4)));density=P.a_dd(np.zeros(15136));data={}
  for iq,q in enumerate(columns):
   assert q['normal_coordinate_order']==('value','R','Z','t') and q['relative_phase_count']==q['ordinary_label_count']==1
   coefficients=q[family]['normal_coefficients'];trace=q[family]['initial_CMC_density'];assert coefficients[0].shape==coefficients[1].shape==(3784,4,4) and trace[0].shape==trace[1].shape==(3784,)
   sl=slice(iq*3784,(iq+1)*3784)
   for word in (0,1):value[word][sl]=coefficients[word][:,:,:3];primary[word][sl]=coefficients[word][:,:,3];density[word][sl]=trace[word]
   for n,x in (('point_Hamiltonian_normal',value),('time_primary_action_coefficients',P.a_mul64(-1.,primary)),('initial_CMC_density',density)):fy_keep(label+'_'+family+'_current_'+n,x,keep)
  weak=N.paired_scatter_normal(value,basis,label+'_'+family+'_NEW_normal');trace=P.dd_scalar_scatter(density,basis,keep,label+'_'+family+'_NEW_CMC')
  normal_nodal_terms=P.a_dd(np.zeros(weak[0].shape));normal_point_terms=P.a_dd(np.zeros(value[0].shape));CMC_nodal_terms=P.a_dd(np.zeros(trace[0].shape));CMC_point_terms=P.a_dd(np.zeros(density[0].shape))
  for name,terms,left,right,selected,raw_left in (('normal_nodal',normal_nodal_terms,normal_test,weak,normal_test!=0,True),('normal_point',normal_point_terms,value,tv,(tv[0]!=0)|(tv[1]!=0),False),('CMC_nodal',CMC_nodal_terms,scalar_test,trace,scalar_test!=0,True),('CMC_point',CMC_point_terms,density,sv,(sv[0]!=0)|(sv[1]!=0),False)):
   selected_right=(right[0][selected],right[1][selected]);fy_keep(label+'_'+family+'_'+name+'_selected_right',selected_right,keep)
   if raw_left:keep(label+'_'+family+'_'+name+'_selected_left',np.asarray(left[selected]).copy());product=P.a_mul64(left[selected],selected_right)
   else:
    selected_left=(left[0][selected],left[1][selected]);fy_keep(label+'_'+family+'_'+name+'_selected_left',selected_left,keep);product=P.a_mul(selected_left,selected_right)
   for word in (0,1):terms[word][selected]=product[word]
   fy_keep(label+'_'+family+'_'+name+'_completed_product',terms,keep)
  normal_nodal=fy_sum(fy_sum(fy_sum(normal_nodal_terms,2),1),0)
  normal_direct=fy_sum(P.a_mul64(weight,fy_sum(fy_sum(normal_point_terms,2),1)),0)
  CMC_nodal=fy_sum(fy_sum(CMC_nodal_terms,1),0);CMC_direct=fy_sum(P.a_mul64(weight,CMC_point_terms),0)
  ng=P.a_sub(normal_nodal,normal_direct);cg=P.a_sub(CMC_nodal,CMC_direct)
  for n,x in (('weak_normal',weak),('weak_initial_CMC',trace),('normal_functional_nodal',normal_nodal),('normal_functional_direct',normal_direct),('normal_functional_gap',ng),('CMC_functional_nodal',CMC_nodal),('CMC_functional_direct',CMC_direct),('CMC_functional_gap',cg),('time_primary_action_coefficients',P.a_mul64(-1.,primary))):data[n]=fy_keep(label+'_'+family+'_'+n,x,keep)
  # These positive bounds certify the NEW scatter operands and transpose test,
  # not the upstream field/action calculation or physical constraint residual.
  ev=fn_abs(value);ec=fn_abs(density);en=N.scatter_normal_envelope(ev,basis);es=P.scalar_scatter(ec,basis)
  nb=np.sum(abs(normal_test)*en)+np.sum(weight[:,None,None]*fn_abs(tv)*ev);cb=np.sum(abs(scalar_test)*es)+np.sum(weight*fn_abs(sv)*ec)
  for n,x in (('normal_functional_envelope',nb),('CMC_functional_envelope',cb)):keep(label+'_'+family+'_'+n,np.asarray(x).copy());data[n]=np.asarray(x).copy()
  check(label+'_'+family+'_normal_polynomial_transpose',np.asarray(ng[0]+ng[1]).copy(),np.asarray(0.).copy(),np.asarray(nb).copy())
  check(label+'_'+family+'_CMC_polynomial_transpose',np.asarray(cg[0]+cg[1]).copy(),np.asarray(0.).copy(),np.asarray(cb).copy())
  result[family]=data
 return dict(value=result['value'],delta=result['delta'],all_time_primary_coefficients_retained=True,normal_scatter_functional_controls_evaluated=True,canonical_current_residuals_supplied_here=False,physical_primary_or_boundary_ports_admitted=False,finite_candidate_physically_admitted=False)
