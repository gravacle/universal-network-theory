"""HELD fixed-configuration specialization of the declared NEW160 map.
Globals np,P,fy_* and compact_contact_* paired contraction definitions only.
The containing provider installs the exact-exponent a_prod into its arithmetic
globals. No raw225/160/123 producer, old frozen action or primal replay is called.
Raw candidate values are held; formal inverse/time contacts retain C-versus-L
primary gaps. All99 native and six physical symmetric metric rates participate.
This is a linear temporal derivative, not a finite candidate or inverse proof.
"""
SPECIALIZED_TEMPORAL_AUTHOR_DRAFT=True
SPECIALIZED_TEMPORAL_AUTHORING_IN_PROGRESS=False

def ft_keep(label,x,keep):
 keep(label+'_both_words',np.stack(x).copy())
 return fy_keep(label,x,keep)

def candidate_temporal_prepare(candidate,reference,keep,label):
 s0,c0=candidate['s'],candidate['c'];p=len(c0['N'])
 snames=('g','hi','U','z','P','w','omega');cnames=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
 s={n:np.asarray(s0[n]).copy() for n in snames};c={n:np.asarray(c0[n]).copy() for n in cnames}
 for family,values in (('raw_configuration',s),('raw_chart',c)):
  for n,a in values.items():keep(label+'_'+family+'_'+n,a.copy());assert a.dtype==np.float64 and np.all(np.isfinite(a)),n
 assert c['ih'].shape==(p,3,3) and s['z'].shape==(32,p,4) and s['U'].shape==(p,4) and s['hi'].shape==(p,4,4)
 assert np.all(c['N']>0) and np.all(c['gamma']>0) and np.all(s['omega']>0) and np.all(s['w']>=0)
 assert np.array_equal(c['ih'],c['ih'].swapaxes(-1,-2)) and np.array_equal(s['g'],s['g'].swapaxes(-1,-2))
 A=ft_keep(label+'_anchored_raw_up_dot_zi',P.a_dd(np.einsum('pi,jpi->jp',c['up'],s['z'][:,:,1:])),keep)
 N=P.a_dd(c['N']);NA=ft_keep(label+'_paired_N_times_anchored_A',P.a_mul((N[0][None],N[1][None]),A),keep)
 E0=tuple(a.copy() for a in reference['E0']);assert E0[0].shape==E0[1].shape==(p,4,4,4);ft_keep(label+'_fixed_lowered_E0',E0,keep)
 raw_Iu=ft_keep(label+'_formal_I_times_u',fy_mv(P.a_dd(c['ih']),P.a_dd(c['u'])),keep)
 ft_keep(label+'_formal_Iu_minus_raw_up',P.a_sub(raw_Iu,P.a_dd(c['up'])),keep)
 envelopes={n:np.asarray(a).copy() for n,a in candidate['coefficient_envelopes'].items()}
 for n,a in envelopes.items():keep(label+'_copied_positive_coefficient_'+n,a);assert np.all(np.isfinite(a)) and np.all(a>=0),n
 return dict(s=s,c=c,p=p,A=A,NA=NA,gamma_squared=P.a_dd(c['gamma']**2),fixed_E0=E0,envelopes=envelopes,constants={n:getattr(P,n) for n in ('ALPHA','ELL','C')},candidate_provenance=candidate.get('candidate_provenance'),configuration_held=True,old_coefficients_or_primal_features_replayed=False)

def candidate_temporal_jet_envelopes(cache,physical,keep,label):
 c,e,p=cache['c'],cache['envelopes'],cache['p'];v=(abs(physical['native'][0])+abs(physical['native'][1])).reshape(p,33,3);u=v[:,0];zt=v[:,1:].transpose(1,0,2)
 q=abs(physical['metric'][0])+abs(physical['metric'][1]);Q=np.zeros((p,3,3))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):Q[:,i,j]=Q[:,j,i]=q[:,slot]
 It=np.einsum('pij,pjk,pkl->pil',e['ih'],Q,e['ih']);wt=np.einsum('pij,pj->pi',It,e['u'])+np.einsum('pij,pj->pi',e['ih'],u)
 gt=(np.einsum('pi,pi->p',u,e['up'])+np.einsum('pi,pi->p',e['u'],wt))/(2*c['gamma']);U0t=gt/c['N'];Ut=np.column_stack((U0t,wt+e['beta']*U0t[:,None]))
 A=np.einsum('pi,jpi->jp',e['up'],e['z'][:,:,1:]);At=np.einsum('pi,jpi->jp',wt,e['z'][:,:,1:])+np.einsum('pi,jpi->jp',e['up'],zt)
 z0t=np.einsum('pi,jpi->jp',e['beta'],zt)+c['N'][None]*A*gt[None]/c['gamma'][None]**2+c['N'][None]*At/c['gamma'][None]
 Zt=np.concatenate((z0t[:,:,None],zt),2);DU=np.zeros((p,4,4));DZ=np.zeros((32,p,4,4));DG=np.zeros((p,4,4,4));DU[:,0]=Ut;DZ[:,:,0]=Zt;DG[:,0,1:,1:]=Q
 qb=np.einsum('pij,pj->pi',Q,e['beta']);DG[:,0,0,1:]=DG[:,0,1:,0]=qb;DG[:,0,0,0]=np.einsum('pi,pi->p',e['beta'],qb);Ga=np.zeros((p,4,4,4))
 for a in range(4):
  for b in range(4):Ga[:,:,a,b]=.5*np.einsum('plm,pm->pl',e['hi'],DG[:,a,b]+DG[:,b,a]+DG[:,:,a,b])
 K=c['N'][:,None,None]*Ga[:,0,1:,1:];KADM=Q/(2*c['N'][:,None,None]);primaryU=Ut+np.einsum('pab,pb->pa',e['JU'],u)+np.einsum('pqa,pq->pa',e['Uh'],q)
 primaryZ=Zt.copy();primaryZ[:,:,0]+=np.einsum('jpa,pa->jp',e['JzU'],u)+np.einsum('pa,jpa->jp',e['Jzz'],zt)+np.einsum('jpq,pq->jp',e['zh'],q)
 out=dict(du=DU,dz=DZ,dg=DG,Ga=Ga,formal_U_time=Ut,formal_inverse_time=It,formal_up_time=wt,gamma_time=gt,primary_U=primaryU,primary_z=primaryZ,KGamma_minus_KADM=K+KADM,Ktrace_Gamma_minus_ADM=np.einsum('pij,pij->p',e['ih'],K+KADM))
 for n,a in out.items():keep(label+'_'+n,np.asarray(a).copy());assert np.all(np.isfinite(a)) and np.all(a>=0),n
 return out

def candidate_temporal_jets(cache,physical,keep,label):
 s,c,p=cache['s'],cache['c'],cache['p'];put=lambda n,x:ft_keep(label+'_'+n,x,keep)
 for n,shape in (('native',(p,99)),('metric',(p,6))):
  assert len(physical[n])==2 and all(a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a)) for a in physical[n]);put('input_'+n,physical[n])
 v=tuple(a.reshape(p,33,3) for a in physical['native']);u=tuple(a[:,0] for a in v);zt=tuple(a[:,1:].transpose(1,0,2) for a in v)
 Q=P.a_dd(np.zeros((p,3,3)))
 for slot,(i,j) in enumerate(((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))):
  for word in (0,1):Q[word][:,i,j]=Q[word][:,j,i]=physical['metric'][word][:,slot]
 put('physical_symmetric_hdot',Q);I=P.a_dd(c['ih']);up=P.a_dd(c['up']);ucov=P.a_dd(c['u']);beta=P.a_dd(c['beta']);N=P.a_dd(c['N']);zi=P.a_dd(s['z'][:,:,1:])
 It=put('formal_inverse_time_direction',P.a_mul64(-1.,fy_mm(fy_mm(I,Q),I)))
 wt=put('formal_up_time_direction',P.a_add(fy_mv(It,ucov),fy_mv(I,u)))
 gn=put('gamma_time_numerator',P.a_add(fy_sum(P.a_mul(u,up),-1),fy_sum(P.a_mul(ucov,wt),-1)))
 gt=put('gamma_time_direction',fy_div(gn,P.a_dd(2*c['gamma']),keep,label+'_gamma_time_quotient'))
 U0t=put('U0_time_direction',fy_div(gt,N,keep,label+'_U0_time_quotient'))
 Uit=P.a_sub(wt,P.a_mul(beta,(U0t[0][:,None],U0t[1][:,None])))
 Ut=put('formal_U_time_direction',P.a_stack([U0t]+[P.a_slice(Uit,(slice(None),i)) for i in range(3)],1))
 At=put('anchored_A_time_direction',P.a_add(fy_sum(P.a_mul((wt[0][None],wt[1][None]),zi),-1),fy_sum(P.a_mul((up[0][None],up[1][None]),zt),-1)))
 first=fy_div(P.a_mul((N[0][None],N[1][None]),At),P.a_dd(c['gamma'][None]),keep,label+'_z0_time_first_quotient')
 second=fy_div(P.a_mul(cache['NA'],(gt[0][None],gt[1][None])),(cache['gamma_squared'][0][None],cache['gamma_squared'][1][None]),keep,label+'_z0_time_second_quotient')
 shift=fy_sum(P.a_mul((beta[0][None],beta[1][None]),zt),-1)
 z0t=put('formal_z0_time_direction',P.a_add(shift,P.a_sub(second,first)))
 Zt=put('formal_z_time_direction',P.a_stack([z0t]+[P.a_slice(zt,(slice(None),slice(None),i)) for i in range(3)],2))
 qb=fy_mv(Q,beta);g00t=fy_sum(P.a_mul(beta,qb),-1)
 row0=P.a_stack([g00t]+[P.a_slice(qb,(slice(None),i)) for i in range(3)],-1)
 rows=[row0]+[P.a_stack([P.a_slice(qb,(slice(None),i))]+[P.a_slice(Q,(slice(None),i,j)) for j in range(3)],-1) for i in range(3)]
 DG=P.a_dd(np.zeros((p,4,4,4)));DU=P.a_dd(np.zeros((p,4,4)));DZ=P.a_dd(np.zeros((32,p,4,4)))
 block=P.a_stack(rows,-2)
 for word in (0,1):DG[word][:,0]=block[word];DU[word][:,0]=Ut[word];DZ[word][:,:,0]=Zt[word]
 put('dg',DG);put('du',DU);put('dz',DZ);Ga=P.a_dd(np.zeros((p,4,4,4)))
 for a in range(4):
  for b in range(4):
   term=P.a_sub(P.a_add(P.a_slice(DG,(slice(None),a,b,slice(None))),P.a_slice(DG,(slice(None),b,a,slice(None)))),P.a_slice(DG,(slice(None),slice(None),a,b)))
   slot=P.a_mul64(.5,fy_mv(P.a_dd(s['hi']),term))
   for word in (0,1):Ga[word][:,:,a,b]=slot[word]
  put('connection_completed_row_partial',Ga)
 put('Ga',Ga);put('connection_torsion_direction',P.a_sub(Ga,tuple(a.swapaxes(-1,-2) for a in Ga)))
 chartU=P.a_add(P.a_matvec(c['JU'],u),P.a_matvec(c['Uh'].transpose(0,2,1),physical['metric']))
 put('formal_minus_canonical_primary_U_time',P.a_sub(Ut,chartU));chartz=P.a_dd(np.zeros((32,p)))
 for n,coef,arg in (('JzU',c['JzU'],tuple(a[None] for a in u)),('Jzz',c['Jzz'][None],zt),('zh',c['zh'],tuple(a[None] for a in physical['metric']))):
  chartz=P.a_add(chartz,fy_sum(P.a_mul64(coef,arg),2));put('canonical_z_time_'+n+'_partial',chartz)
 chartZ=P.a_stack([chartz]+[P.a_slice(zt,(slice(None),slice(None),i)) for i in range(3)],2)
 put('formal_minus_canonical_primary_z_time',P.a_sub(Zt,chartZ))
 compatibility=[]
 for a in range(4):
  G=P.a_slice(Ga,(slice(None),slice(None),a,slice(None)));reaction=P.a_add(fy_mm(tuple(w.swapaxes(-1,-2) for w in G),P.a_dd(s['g'])),fy_mm(P.a_dd(s['g']),G))
  compatibility.append(P.a_sub(P.a_slice(DG,(slice(None),a)),reaction))
 put('fixed_E0_compatibility_direction',P.a_stack(compatibility,1))
 return dict(du=DU,dz=DZ,dg=DG,Ga=Ga,Ut=Ut,Zt=Zt,Q=Q,formal_inverse_time=It,formal_up_time=wt,gamma_time=gt)

def candidate_temporal_canonical(cache,jets,keep,label):
 s,c,p=cache['s'],cache['c'],cache['p'];put=lambda n,x:ft_keep(label+'_'+n,x,keep);U,z,hi=s['U'],s['z'],s['hi'];H=P.a_dd(hi);G=P.a_dd(s['g']);proj=P.a_dd(s['P'])
 nu=jets['du'];nz=jets['dz']
 for l in range(4):
  ga=P.a_transpose(P.a_slice(jets['Ga'],(slice(None),slice(None),slice(None),l)),(0,2,1))
  nu=P.a_add(nu,P.a_mul64(U[:,l,None,None],ga));nz=P.a_sub(nz,P.a_mul64(z[:,:,l,None,None],P.a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None)))))
 put('nu',nu);put('nz',nz);q=P.a_dd(np.zeros((32,p,4)))
 for a in range(4):q=P.a_add(q,P.a_mul64(U[None,:,a,None],P.a_slice(nz,(slice(None),slice(None),a,slice(None)))))
 put('q',q);V=put('V',compact_momentum_matvec(proj,q));D=put('D',compact_contact_right(compact_contact_left(proj,nz),compact_contact_swap(proj)))
 lower=compact_contact_right(nu,G);F=put('F',P.a_sub(lower,compact_contact_swap(lower)));Fu=put('Fup',compact_contact_right(compact_contact_left(H,F),H))
 Vu=put('V_raised',compact_momentum_matvec(H,V));Du=put('D_raised',compact_contact_right(compact_contact_left(H,D),H))
 Pi=P.a_div64(compact_contact_outer(P.a_dd(U[None]),Vu),s['omega'][:,None,None,None]**2,keep,label+'_Pi_frequency')
 Pi=put('Pi',P.a_mul64(s['w'][:,None,None,None],P.a_sub(Pi,P.a_mul64(P.ELL**2,Du))))
 PiU=put('PiU',P.a_mul64(-P.ALPHA,compact_contact_left(H,F)));sym=P.a_mul64(.5,P.a_add(Pi,compact_contact_swap(Pi)));rows=[]
 for l in range(4):
  row=P.a_dd(np.zeros((p,4,4)))
  for j in range(32):row=P.a_sub(row,P.a_mul64(z[j,:,l,None,None],P.a_slice(sym,j)))
  rows.append(row);put('connection_Klo_completed_row_partial',P.a_stack(rows,1))
 Klo=put('connection_Klo',P.a_stack(rows,1));Kup=P.a_dd(np.zeros((p,4,4,4)))
 for m in range(4):Kup=P.a_add(Kup,P.a_mul64(hi[:,:,m,None,None],(Klo[0][:,None,m],Klo[1][:,None,m])))
 put('connection_raised_Klo',Kup);CCn=P.a_mul64(.5,P.a_sub(P.a_add(P.a_transpose(Kup,(0,2,1,3)),P.a_transpose(Kup,(0,2,3,1))),Kup))
 MX=P.a_add(P.a_mul64(U[:,None,None,:],(Fu[0][:,:,:,None],Fu[1][:,:,:,None])),P.a_mul64(U[:,None,:,None],(Fu[0][:,:,None,:],Fu[1][:,:,None,:])))
 CC=put('connection_momentum',P.a_add(CCn,P.a_mul64(-P.ALPHA/2,MX)));PU=P.a_slice(PiU,(slice(None),0,slice(None)));P00=P.a_slice(Pi,(slice(None),slice(None),0,0))
 pu=P.a_dd(np.zeros((p,3)))
 for a in range(4):pu=P.a_add(pu,P.a_mul64(c['JU'][:,a],(PU[0][:,a,None],PU[1][:,a,None])))
 for j in range(32):pu=P.a_add(pu,P.a_mul64(c['JzU'][j],(P00[0][j,:,None],P00[1][j,:,None])))
 pz=P.a_add(P.a_slice(Pi,(slice(None),slice(None),0,slice(1,None))),P.a_mul64(c['Jzz'][None],(P00[0][:,:,None],P00[1][:,:,None])))
 native=put('native_density',P.a_mul64(c['dens'][:,None],P.a_stack([P.a_slice(pu,(slice(None),i)) for i in range(3)]+[P.a_slice(pz,(j,slice(None),i)) for j in range(32) for i in range(3)],-1)))
 pm=P.a_dd(np.zeros((p,6)));C0=P.a_slice(CC,(slice(None),0,slice(None),slice(None)))
 for a in range(4):
  pm=P.a_add(pm,P.a_mul64(c['Uh'][:,:,a],(PU[0][:,a,None],PU[1][:,a,None])))
  for b in range(4):pm=P.a_add(pm,P.a_mul64(c['embed'][:,:,a,b],(C0[0][:,a,b,None],C0[1][:,a,b,None])))
 for j in range(32):pm=P.a_add(pm,P.a_mul64(c['zh'][j],(P00[0][j,:,None],P00[1][j,:,None])))
 metric_native=put('metric_native_density',P.a_mul64(c['dens'][:,None],pm))
 K=put('K',P.a_mul64(c['N'][:,None,None],P.a_slice(jets['Ga'],(slice(None),0,slice(1,None),slice(1,None)))))
 trace=put('Ktrace',compact_contact_reduce(P.a_mul64(c['ih'],K),(1,2)));I=P.a_dd(c['ih'])
 numerator=P.a_sub(compact_contact_right(compact_contact_left(I,K),I),P.a_mul64(c['ih'],(trace[0][:,None,None],trace[1][:,None,None])))
 EH=put('metric_EH_tensor',P.a_div64(P.a_mul64(c['sqrt_h'][:,None,None],numerator),2*P.C,keep,label+'_EH_division'))
 metric_EH=put('metric_EH_density',P.a_stack([P.a_mul64(1. if i==j else 2.,P.a_slice(EH,(slice(None),i,j))) for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1))
 metric_total=put('metric_total_density',P.a_add(metric_native,metric_EH));KADM=fy_div(jets['Q'],P.a_dd(2*c['N'][:,None,None]),keep,label+'_KADM_direction')
 put('KGamma_minus_KADM_direction',P.a_sub(K,KADM));put('Ktrace_Gamma_minus_ADM_direction',P.a_sub(trace,fy_contract(I,KADM)))
 return dict(native=native,metric_native=metric_native,metric_EH=metric_EH,metric_total=metric_total)

def candidate_specialized_temporal_action(cache,physical,keep,label):
 assert cache['configuration_held'] and all(cache['constants'][n]==getattr(P,n) for n in cache['constants'])
 jets=candidate_temporal_jets(cache,physical,keep,label+'_NEW_linear_jets');point=candidate_temporal_canonical(cache,jets,keep,label+'_NEW_linear_canonical')
 return dict(point=point,jets=jets,fixed_configuration_temporal_derivative=True,phase_mechanical_rate_crosszero_scope='declared action at fixed configuration',modal_head_structure='U3+physical_metric6 head;32 modal3 arms;offdiagonal arms zero in source algebra',C_equals_L_or_symmetry_assumed=False,old_frozen_or_general160_action_replayed=False,finite_candidate_or_inverse_qualified=False,physical_adoption=False)
