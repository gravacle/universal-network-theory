"""Definitions only: derivative of the registered134 normal-test contacts.
Caller supplies np, a_*, normal_action_reduce, normal_keep_pair and the three
paired_normal_{chart_jets,lift,metric_delta} definitions. No author evaluation.
N,beta and their test f,df_test,b,db are fixed; their coordinate first jets
still vary through the SAME algebraic inverse/DG chart. d includes dg and Ga.
df['configuration'] and df['paired'] are the complete supplied configuration
feature tangent. Every direction uses the raw binary64 test primal convention;
paired construction-versus-raw contacts remain saved, never fitted away.
Base test contractions are new derivative intermediates, not old weak rows.
No second metric jets, configuration update, source or temporal history chosen.
"""
def normal_contact_mm(x,y):
 product=a_mul(a_reshape(x,x[0].shape+(1,)),a_reshape(y,y[0].shape[:-2]+(1,)+y[0].shape[-2:]))
 return normal_action_reduce(product,(-2,))

def normal_contact_mv(x,y):
 value=normal_contact_mm(x,a_reshape(y,y[0].shape+(1,)))
 return a_reshape(value,value[0].shape[:-1])

def normal_contact_connection(hi,nq,keep,label):
 out=a_dd(np.zeros((hi[0].shape[0],4,4,4)))
 for a in range(4):
  for b in range(4):
   terms=a_sub(a_add(a_slice(nq,(slice(None),a,b,slice(None))),a_slice(nq,(slice(None),b,a,slice(None)))),a_slice(nq,(slice(None),slice(None),a,b)))
   value=a_mul64(.5,normal_contact_mv(hi,terms))
   for word in (0,1):out[word][:,:,a,b]=value[word]
   normal_keep_pair(label+'_partial',out,keep)
 return out

def normal_contact_test_derivatives(s,c,jets,feature,d,dc,df,f,df_test,b,db,keep,label):
 p=len(s['U']);N,h,beta,U,z,hi,g=c['N'],c['h'],c['beta'],s['U'],s['z'],s['hi'],s['g']
 assert d['g'][0].shape==(p,4,4) and d['dg'][0].shape==jets['dg'][0].shape==(p,4,4,4)
 cj=paired_normal_chart_jets(s,c,jets,keep,label+'_base_chart')
 base=paired_normal_lift(s,c,jets,cj,f,df_test,b,db,keep,label+'_base_lift')
 base_delta=paired_normal_metric_delta(s,jets,feature,base,keep,label+'_base_metric')
 dh=a_slice(d['g'],(slice(None),slice(1,None),slice(1,None)));H=a_dd(hi)
 # Differentiate -hi DG_a hi; explicit dN=dbeta=0 at configuration level.
 d_inverse_jet=[]
 for a in range(4):
  G=a_slice(jets['dg'],(slice(None),a));dG=a_slice(d['dg'],(slice(None),a))
  v=a_add(normal_contact_mm(normal_contact_mm(d['hi'],G),H),normal_contact_mm(normal_contact_mm(H,dG),H))
  v=a_add(v,normal_contact_mm(normal_contact_mm(H,G),d['hi']));d_inverse_jet.append((-v[0],-v[1]))
 d_inverse_jet=a_stack(d_inverse_jet,axis=1);normal_keep_pair(label+'_delta_inverse_jet',d_inverse_jet,keep)
 dn=a_mul64(N[:,None]**3/2,a_slice(d_inverse_jet,(slice(None),slice(None),0,0)))
 d_beta=a_mul64(2*N[:,None,None]*hi[:,None,0,1:],(dn[0][:,:,None],dn[1][:,:,None]))
 d_beta=a_add(d_beta,a_mul64(2*N[:,None,None],a_mul((cj['dN'][0][:,:,None],cj['dN'][1][:,:,None]),(d['hi'][0][:,None,0,1:],d['hi'][1][:,None,0,1:]))))
 d_beta=a_add(d_beta,a_mul64(N[:,None,None]**2,a_slice(d_inverse_jet,(slice(None),slice(None),0,slice(1,None)))))
 dcj=dict(dN=dn,dbeta=d_beta,dh=a_slice(d['dg'],(slice(None),slice(None),slice(1,None),slice(1,None))))
 for n,x in dcj.items():normal_keep_pair(label+'_delta_chart_'+n,x,keep)
 q=a_dd(np.zeros((p,4,4)));q00=a_dd(np.zeros(p))
 for i in range(3):
  for k in range(3):q00=a_add(q00,a_mul64(2*beta[:,i]*b[:,k],a_slice(dh,(slice(None),i,k))))
 q[0][:,0,0]=q00[0];q[1][:,0,0]=q00[1]
 for i in range(3):
  v=normal_action_reduce(a_mul(a_slice(dh,(slice(None),i,slice(None))),a_dd(b)),(-1,))
  for word in (0,1):q[word][:,0,i+1]=q[word][:,i+1,0]=v[word]
 normal_keep_pair(label+'_delta_lift_q',q,keep)
 u0=a_slice(d['U'],(slice(None),0));eta0=a_mul64(-f/N,u0);eta=a_dd(np.zeros_like(U))
 eta[0][:,0]=eta0[0];eta[1][:,0]=eta0[1]
 for i in range(3):
  v=a_sub(a_mul64(-b[:,i],u0),a_mul64(beta[:,i],eta0))
  for word in (0,1):eta[word][:,i+1]=v[word]
 normal_keep_pair(label+'_delta_lift_eta',eta,keep)
 ez=np.einsum('pa,jpa->jp',base['eta'],z);de=a_add(normal_action_reduce(a_mul64(z,(eta[0][None],eta[1][None])),(2,)),normal_action_reduce(a_mul64(base['eta'][None],d['z']),(2,)))
 z0=a_add(a_div64((-de[0],-de[1]),U[None,:,0],keep,label+'_delta_zeta_denominator'),a_mul64(ez/U[None,:,0]**2,(u0[0][None],u0[1][None])))
 zeta=a_dd(np.zeros_like(z));zeta[0][:,:,0]=z0[0];zeta[1][:,:,0]=z0[1]
 normal_keep_pair(label+'_delta_lift_zeta',zeta,keep)
 dq=a_dd(np.zeros((p,4,4,4)));dq00=a_mul64(-2*f[:,None],dn)
 for i in range(3):
  for k in range(3):
   dq00=a_add(dq00,a_mul64(2*beta[:,i,None]*db[:,:,k],(dh[0][:,None,i,k],dh[1][:,None,i,k])))
   dq00=a_add(dq00,a_mul64((2*b[:,k])[:,None],a_mul((dh[0][:,None,i,k],dh[1][:,None,i,k]),a_slice(cj['dbeta'],(slice(None),slice(None),i)))))
   dq00=a_add(dq00,a_mul64((2*h[:,i,k]*b[:,k])[:,None],a_slice(dcj['dbeta'],(slice(None),slice(None),i))))
   dq00=a_add(dq00,a_mul64((2*beta[:,i]*b[:,k])[:,None],a_slice(dcj['dh'],(slice(None),slice(None),i,k))))
 for word in (0,1):dq[word][:,:,0,0]=dq00[word]
 for i in range(3):
  v=a_dd(np.zeros((p,4)))
  for k in range(3):
   v=a_add(v,a_mul64(db[:,:,k],(dh[0][:,None,i,k],dh[1][:,None,i,k])))
   v=a_add(v,a_mul64(b[:,k,None],a_slice(dcj['dh'],(slice(None),slice(None),i,k))))
  for word in (0,1):dq[word][:,:,0,i+1]=dq[word][:,:,i+1,0]=v[word]
 normal_keep_pair(label+'_delta_lift_dq',dq,keep)
 du0=a_slice(jets['du'],(slice(None),slice(None),0));delta_du0=a_slice(d['du'],(slice(None),slice(None),0))
 deta0=a_add(a_mul64((-f/N)[:,None],delta_du0),a_mul64(-df_test/N[:,None],(u0[0][:,None],u0[1][:,None])))
 deta0=a_add(deta0,a_mul((a_mul64(f/N**2,u0)[0][:,None],a_mul64(f/N**2,u0)[1][:,None]),cj['dN']))
 deta0=a_add(deta0,a_mul64((f*U[:,0]/N**2)[:,None],dn));deta=a_dd(np.zeros_like(s['du']))
 for word in (0,1):deta[word][:,:,0]=deta0[word]
 for i in range(3):
  v=a_add(a_mul64(-b[:,i,None],delta_du0),a_mul64(-db[:,:,i],(u0[0][:,None],u0[1][:,None])))
  v=a_sub(v,a_mul((eta0[0][:,None],eta0[1][:,None]),a_slice(cj['dbeta'],(slice(None),slice(None),i))))
  v=a_sub(v,a_mul64(base['eta'][:,0,None],a_slice(dcj['dbeta'],(slice(None),slice(None),i))));v=a_sub(v,a_mul64(beta[:,i,None],deta0))
  for word in (0,1):deta[word][:,:,i+1]=v[word]
 normal_keep_pair(label+'_delta_lift_deta',deta,keep)
 dez=a_dd(np.zeros((32,p,4)));delta_dez=a_dd(np.zeros((32,p,4)))
 for a in range(4):
  be=a_slice(base['deta'],(slice(None),slice(None),a));de_a=a_slice(deta,(slice(None),slice(None),a))
  zz=a_slice(d['z'],(slice(None),slice(None),a));jz=a_slice(jets['dz'],(slice(None),slice(None),slice(None),a));djz=a_slice(d['dz'],(slice(None),slice(None),slice(None),a))
  dez=a_add(dez,a_add(a_mul64(z[:,:,a,None],be),a_mul64(base['eta'][None,:,a,None],jz)))
  delta_dez=a_add(delta_dez,a_mul64(z[:,:,a,None],de_a));delta_dez=a_add(delta_dez,a_mul((zz[0][:,:,None],zz[1][:,:,None]),(be[0][None],be[1][None])))
  delta_dez=a_add(delta_dez,a_mul((eta[0][None,:,a,None],eta[1][None,:,a,None]),jz));delta_dez=a_add(delta_dez,a_mul64(base['eta'][None,:,a,None],djz))
 dz0=a_div64((-delta_dez[0],-delta_dez[1]),U[None,:,0,None],keep,label+'_delta_dzeta_denominator')
 dz0=a_add(dz0,a_mul64(1/U[None,:,0,None]**2,a_mul(dez,(u0[0][None,:,None],u0[1][None,:,None]))))
 dz0=a_add(dz0,a_mul64(1/U[None,:,0,None]**2,a_mul((de[0][:,:,None],de[1][:,:,None]),(du0[0][None],du0[1][None]))))
 dz0=a_add(dz0,a_mul64(ez[:,:,None]/U[None,:,0,None]**2,(delta_du0[0][None],delta_du0[1][None])))
 dz0=a_sub(dz0,a_mul64(2*ez[:,:,None]/U[None,:,0,None]**3,a_mul((du0[0][None],du0[1][None]),(u0[0][None,:,None],u0[1][None,:,None]))))
 dzeta=a_dd(np.zeros_like(s['dz']));dzeta[0][:,:,:,0]=dz0[0];dzeta[1][:,:,:,0]=dz0[1]
 lift=dict(q=q,dq=dq,eta=eta,deta=deta,zeta=zeta,dzeta=dzeta)
 for n,x in lift.items():normal_keep_pair(label+'_delta_lift_'+n,x,keep)
 nq=[];dnq=[]
 for a in range(4):
  ga=a_slice(jets['Ga'],(slice(None),slice(None),a,slice(None)));dga=a_slice(d['Ga'],(slice(None),slice(None),a,slice(None)))
  connection=a_add(normal_contact_mm(a_transpose(ga,(0,2,1)),a_dd(base['q'])),normal_contact_mm(a_dd(base['q']),ga))
  delta_connection=a_add(normal_contact_mm(a_transpose(dga,(0,2,1)),a_dd(base['q'])),normal_contact_mm(a_transpose(ga,(0,2,1)),q))
  delta_connection=a_add(delta_connection,normal_contact_mm(q,ga));delta_connection=a_add(delta_connection,normal_contact_mm(a_dd(base['q']),dga))
  nq.append(a_sub(a_slice(base['dq'],(slice(None),a)),connection));dnq.append(a_sub(a_slice(dq,(slice(None),a)),delta_connection))
 nq=a_stack(nq,axis=1);dnq=a_stack(dnq,axis=1)
 dTestG=a_add(normal_contact_connection(d['hi'],nq,keep,label+'_inverse_contact_Gamma'),normal_contact_connection(H,dnq,keep,label+'_covariant_test_jet_contact_Gamma'))
 constructedG=normal_contact_connection(H,nq,keep,label+'_constructed_test_Gamma')
 normal_keep_pair(label+'_test_Gamma_construction_gap',a_sub(constructedG,base_delta['paired']['deltaG']),keep)
 F=feature['paired'];dF= df['paired'];cfg=df['configuration'];Gtest=base_delta['paired']['deltaG']
 dnu=deta;dnz=a_dd(np.zeros_like(s['dz']))
 for l in range(4):
  gu=a_transpose(a_slice(Gtest,(slice(None),slice(None),slice(None),l)),(0,2,1));dgu=a_transpose(a_slice(dTestG,(slice(None),slice(None),slice(None),l)),(0,2,1))
  ju=a_transpose(a_slice(jets['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1));dju=a_transpose(a_slice(d['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))
  dnu=a_add(dnu,a_mul((d['U'][0][:,l,None,None],d['U'][1][:,l,None,None]),gu));dnu=a_add(dnu,a_mul64(U[:,l,None,None],dgu))
  dnu=a_add(dnu,a_mul((eta[0][:,l,None,None],eta[1][:,l,None,None]),ju));dnu=a_add(dnu,a_mul64(base['eta'][:,l,None,None],dju))
  dnz=a_sub(dnz,a_mul((d['z'][0][:,:,l,None,None],d['z'][1][:,:,l,None,None]),a_slice(Gtest,(slice(None),l,slice(None),slice(None)))))
  dnz=a_sub(dnz,a_mul64(z[:,:,l,None,None],a_slice(dTestG,(slice(None),l,slice(None),slice(None)))))
 test_duc=np.einsum('pab,pb->pa',base['q'],U)+np.einsum('pab,pb->pa',g,base['eta'])
 testP=test_duc[:,:,None]*U[:,None,:]+s['uc'][:,:,None]*base['eta'][:,None,:]
 constructed=a_add(normal_contact_mv(a_dd(base['q']),a_dd(U)),normal_contact_mv(a_dd(g),a_dd(base['eta'])))
 normal_keep_pair(label+'_raw_test_duc_construction_gap',a_sub(constructed,a_dd(test_duc)),keep)
 constructedP=a_add(a_mul((a_dd(test_duc)[0][:,:,None],a_dd(test_duc)[1][:,:,None]),a_dd(U[:,None,:])),a_mul64(s['uc'][:,:,None],a_dd(base['eta'][:,None,:])))
 normal_keep_pair(label+'_raw_test_projector_construction_gap',a_sub(constructedP,a_dd(testP)),keep)
 dduc=a_add(normal_contact_mv(q,a_dd(U)),normal_contact_mv(a_dd(base['q']),d['U']))
 dduc=a_add(dduc,normal_contact_mv(d['g'],a_dd(base['eta'])));dduc=a_add(dduc,normal_contact_mv(a_dd(g),eta))
 dTestP=a_add(a_mul((dduc[0][:,:,None],dduc[1][:,:,None]),a_dd(U[:,None,:])),a_mul64(test_duc[:,:,None],(d['U'][0][:,None,:],d['U'][1][:,None,:])))
 dTestP=a_add(dTestP,a_mul((cfg['uc'][0][:,:,None],cfg['uc'][1][:,:,None]),a_dd(base['eta'][:,None,:])));dTestP=a_add(dTestP,a_mul64(s['uc'][:,:,None],(eta[0][:,None,:],eta[1][:,None,:])))
 normal_keep_pair(label+'_delta_test_projector',dTestP,keep)
 testqq=a_dd(np.zeros_like(F['q'][0]));dqq=a_dd(np.zeros_like(F['q'][0]));da=a_dd(np.zeros_like(F['a'][0]))
 for a in range(4):
  nz=a_slice(F['nz'],(slice(None),slice(None),a,slice(None)));dnz0=a_slice(base_delta['paired']['dnz'],(slice(None),slice(None),a,slice(None)))
  testqq=a_add(testqq,a_add(a_mul64(base['eta'][None,:,a,None],nz),a_mul64(U[None,:,a,None],dnz0)))
  dqq=a_add(dqq,a_mul((eta[0][None,:,a,None],eta[1][None,:,a,None]),nz));dqq=a_add(dqq,a_mul64(base['eta'][None,:,a,None],a_slice(dF['nz'],(slice(None),slice(None),a,slice(None)))))
  dqq=a_add(dqq,a_mul((d['U'][0][None,:,a,None],d['U'][1][None,:,a,None]),dnz0));dqq=a_add(dqq,a_mul64(U[None,:,a,None],a_slice(dnz,(slice(None),slice(None),a,slice(None)))))
  nu=a_slice(F['nu'],(slice(None),a,slice(None)));nu0=a_slice(base_delta['paired']['dnu'],(slice(None),a,slice(None)))
  da=a_add(da,a_mul((eta[0][:,a,None],eta[1][:,a,None]),nu));da=a_add(da,a_mul64(base['eta'][:,a,None],a_slice(dF['nu'],(slice(None),a,slice(None)))))
  da=a_add(da,a_mul((d['U'][0][:,a,None],d['U'][1][:,a,None]),nu0));da=a_add(da,a_mul64(U[:,a,None],a_slice(dnu,(slice(None),a,slice(None)))))
 dV=a_add(normal_contact_mv(dTestP,F['q']),normal_contact_mv(a_dd(testP),dF['q']))
 dV=a_add(dV,normal_contact_mv(cfg['P'],testqq));dV=a_add(dV,normal_contact_mv(a_dd(s['P']),dqq))
 A=a_dd(testP);At=a_transpose(A,(0,2,1));dAt=a_transpose(dTestP,(0,2,1));B=a_dd(s['P']);Bt=a_transpose(B,(0,2,1));dBt=a_transpose(cfg['P'],(0,2,1))
 dD=a_dd(np.zeros_like(F['D'][0]))
 for L,M,R in ((dTestP,F['nz'],Bt),(A,dF['nz'],Bt),(A,F['nz'],dBt),(cfg['P'],F['nz'],At),(B,dF['nz'],At),(B,F['nz'],dAt),(cfg['P'],base_delta['paired']['dnz'],Bt),(B,dnz,Bt),(B,base_delta['paired']['dnz'],dBt)):
  dD=a_add(dD,normal_contact_mm(normal_contact_mm(L,M),R));normal_keep_pair(label+'_delta_test_D_partial',dD,keep)
 lower=a_add(normal_contact_mm(dF['nu'],a_dd(base['q'])),normal_contact_mm(F['nu'],q))
 lower=a_add(lower,normal_contact_mm(dnu,a_dd(g)));lower=a_add(lower,normal_contact_mm(base_delta['paired']['dnu'],d['g']))
 dFF=a_sub(lower,a_transpose(lower,(0,2,1)))
 dTestHi=a_add(normal_contact_mm(normal_contact_mm(d['hi'],a_dd(base['q'])),H),normal_contact_mm(normal_contact_mm(H,q),H))
 dTestHi=a_add(dTestHi,normal_contact_mm(normal_contact_mm(H,a_dd(base['q'])),d['hi']));dTestHi=(-dTestHi[0],-dTestHi[1])
 primalHi=normal_contact_mm(normal_contact_mm(H,a_dd(base['q'])),H);primalHi=(-primalHi[0],-primalHi[1])
 normal_keep_pair(label+'_raw_test_inverse_construction_gap',a_sub(primalHi,a_dd(base_delta['dhi'])),keep)
 dr=normal_contact_mv(dTestP,a_dd(s['phi']));lm=a_mul64(.5,normal_action_reduce(a_add(a_mul(d['hi'],a_dd(base['q'].swapaxes(-1,-2))),a_mul64(hi,q)),(1,2)))
 out=dict(paired=dict(deltaG=dTestG,dnu=dnu,dnz=dnz,dV=dV,dD=dD,dF=dFF,da=da),dhi=dTestHi,dr=dr,lm=lm,test_projector=dTestP,test_contracted_mode_jet=dqq)
 for n,x in out['paired'].items():normal_keep_pair(label+'_delta_metric_'+n,x,keep)
 for n in ('dhi','dr','lm','test_projector','test_contracted_mode_jet'):normal_keep_pair(label+'_delta_metric_'+n,out[n],keep)
 return base,base_delta,lift,out,cj,dcj
