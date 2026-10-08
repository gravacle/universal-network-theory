"""Definitions only: Frechet product rules for the SAME paired normal134.
Inputs are saved current features/momenta and NEW test/contact derivatives.
No primal feature, old normal producer, frozen operator or solver is called.
Caller supplies np, admitted a_*, normal_pair_*, compact_contact_* products,
normal_action_reduce/dot, constants C/ALPHA/ELL/B/GC and keep(name,array).
All tensors/vectors named as contacts are pairs, including configuration ones.
The registered normal134 doubling convention is differentiated literally;
no inverse/projector/unit compatibility identity is imposed or repaired.
Every reduction keeps only its current partial/final, not scalar-index keys.
Fixed phi jets in this kernel; the earned phase-velocity normal rows are added
separately by the caller. No finite preparation, induced solve or adoption.
"""

def combined_normal_put(keep,label,name,x):
 normal_keep_pair(label+'_'+name,x,keep);return x

def combined_normal_dot_contact(x,y,dx,dy,axes):
 return a_add(normal_action_dot(dx,y,axes),normal_action_dot(x,dy,axes))

def combined_normal_sandwich_contact(A,x,B,dA,dx,dB):
 left=compact_contact_left
 right=compact_contact_right
 return a_add(a_add(right(left(dA,x),B),right(left(A,dx),B)),right(left(A,x),dB))

def combined_normal_native_contact(s,feature,test,d,df,dtest,keep,label):
 F=feature['paired'];F1=df['paired'];T=test['paired'];T1=dtest['paired']
 I=a_dd(s['hi']);I1=d['hi'];It=a_dd(test['dhi']);It1=dtest['dhi']
 z=a_dd(s['z']);z1=d['z'];r=a_dd(s['r']);r1=df['configuration']['r']
 z2=a_dd(s['z2']);z21=df['configuration']['z2'];om=s['omega'][:,None]**2;kj=(B*GC)**2*s['xi'][:,None]**4
 dot=normal_action_dot;contact=combined_normal_dot_contact
 mv=compact_momentum_matvec;left=compact_contact_left;right=compact_contact_right
 V2=dot(F['V_raised'],F['V'],(2,));D2=dot(F['D_raised'],F['D'],(2,3));F2=dot(F['Fup'],F['F'],(1,2))
 V21=contact(F['V_raised'],F['V'],F1['V_raised'],F1['V'],(2,))
 D21=contact(F['D_raised'],F['D'],F1['D_raised'],F1['D'],(2,3));F21=contact(F['Fup'],F['F'],F1['Fup'],F1['F'],(1,2))
 tv=mv(It,F['V']);tv1=a_add(mv(It1,F['V']),mv(It,F1['V']))
 tV21=a_add(contact(tv,F['V'],tv1,F1['V'],(2,)),a_mul64(2.,contact(F['V_raised'],T['dV'],F1['V_raised'],T1['dV'],(2,))))
 tD21=a_mul64(2.,contact(F['D_raised'],T['dD'],F1['D_raised'],T1['dD'],(2,3)))
 tF21=a_mul64(2.,contact(F['Fup'],T['dF'],F1['Fup'],T1['dF'],(1,2)))
 for A,B0,A1,B1 in ((It,I,It1,I1),(I,It,I1,It1)):
  td=right(left(A,F['D']),B0);td1=combined_normal_sandwich_contact(A,F['D'],B0,A1,F1['D'],B1)
  tf=right(left(A,F['F']),B0);tf1=combined_normal_sandwich_contact(A,F['F'],B0,A1,F1['F'],B1)
  tD21=a_add(tD21,contact(td,F['D'],td1,F1['D'],(2,3)));tF21=a_add(tF21,contact(tf,F['F'],tf1,F1['F'],(1,2)))
  combined_normal_put(keep,label,'delta_test_D_squared_partial',tD21);combined_normal_put(keep,label,'delta_test_F_squared_partial',tF21)
 az=dot(z,(F['a'][0][None],F['a'][1][None]),(2,))
 az1=contact(z,(F['a'][0][None],F['a'][1][None]),z1,(F1['a'][0][None],F1['a'][1][None]),(2,))
 taz1=contact(z,(T['da'][0][None],T['da'][1][None]),z1,(T1['da'][0][None],T1['da'][1][None]),(2,))
 iz=mv(It,z);iz1=a_add(mv(It1,z),mv(It,z1));tz2=a_dd(np.einsum('jpa,pab,jpb->jp',s['z'],test['dhi'],s['z']));tz21=contact(z,iz,z1,iz1,(2,))
 modal_primal=a_stack((a_div64(V2,2*om,keep,label+'_V_frequency'),a_dd(-s['z2']/2),a_dd(-s['z2']*s['z2']/(4*kj)),a_mul64(-ELL**2/2,D2),az),axis=-1)
 modal_contact=a_stack((a_div64(V21,2*om,keep,label+'_delta_V_frequency'),a_mul64(-.5,z21),a_div64(a_mul64(-.5,a_mul(z2,z21)),kj,keep,label+'_delta_quartic'),a_mul64(-ELL**2/2,D21),az1),axis=-1)
 modal_test_contact=a_stack((a_div64(tV21,2*om,keep,label+'_mixed_V_frequency'),a_mul64(-.5,tz21),a_div64(a_mul64(-.5,a_add(a_mul(z21,tz2),a_mul(z2,tz21))),kj,keep,label+'_mixed_quartic'),a_mul64(-ELL**2/2,tD21),taz1),axis=-1)
 modal=[normal_pair_sum(a_mul64(s['w'][:,None,None],x),0) for x in (modal_primal,modal_contact,modal_test_contact)]
 r2=a_dd(np.einsum('pa,pab,pb->p',s['r'],s['hi'],s['r']))
 ir=mv(I,r);ir1=a_add(mv(I1,r),mv(I,r1));r21=contact(r,ir,r1,ir1,(1,))
 itr=mv(It,r);itr1=a_add(mv(It1,r),mv(It,r1));tr=a_dd(test['dr']);tr1=dtest['dr']
 itr2=mv(I,tr);itr21=a_add(mv(I1,tr),mv(I,tr1))
 tr21=a_add(contact(r,itr,r1,itr1,(1,)),a_mul64(2.,contact(r,itr2,r1,itr21,(1,))))
 p=a_stack([a_mul64(-ALPHA/4,F2),a_mul64(-.5,r2)]+[a_slice(modal[0],(slice(None),i)) for i in range(5)],axis=-1)
 p1=a_stack([a_mul64(-ALPHA/4,F21),a_mul64(-.5,r21)]+[a_slice(modal[1],(slice(None),i)) for i in range(5)],axis=-1)
 tp1=a_stack([a_mul64(-ALPHA/4,tF21),a_mul64(-.5,tr21)]+[a_slice(modal[2],(slice(None),i)) for i in range(5)],axis=-1)
 out=a_add(tp1,a_add(a_mul((dtest['lm'][0][:,None],dtest['lm'][1][:,None]),p),a_mul64(test['lm'][:,None],p1)))
 for name,x in (('primal_for_measure_contact',p),('delta_primal',p1),('delta_test_variation',tp1),('terms',out)):combined_normal_put(keep,label,name,x)
 return out

def combined_normal_z0_contact(s,jets,feature,lift,d,df,dlift,keep,label):
 F=feature['paired'];F1=df['paired'];P=a_dd(s['P']);P1=df['configuration']['P'];U=a_dd(s['U']);U1=d['U']
 z=a_dd(s['z']);z1=d['z'];I=a_dd(s['hi']);I1=d['hi'];zt=a_dd(lift['zeta']);zt1=dlift['zeta']
 nz=lift['dzeta'];nz1=dlift['dzeta'];dot=normal_action_dot;contact=combined_normal_dot_contact;mv=compact_momentum_matvec
 for l in range(4):
  gl=a_slice(jets['Ga'],(slice(None),l,slice(None),slice(None)));gl1=a_slice(d['Ga'],(slice(None),l,slice(None),slice(None)))
  zl=a_slice(zt,(slice(None),slice(None),l));zl1=a_slice(zt1,(slice(None),slice(None),l))
  nz=a_sub(nz,a_mul((zl[0][:,:,None,None],zl[1][:,:,None,None]),gl))
  nz1=a_sub(nz1,a_add(a_mul((zl1[0][:,:,None,None],zl1[1][:,:,None,None]),gl),a_mul((zl[0][:,:,None,None],zl[1][:,:,None,None]),gl1)))
 q=a_dd(np.zeros_like(F['q'][0]));q1=a_dd(np.zeros_like(F['q'][0]))
 for a in range(4):
  ua=a_slice(U,(slice(None),a));ua1=a_slice(U1,(slice(None),a));na=a_slice(nz,(slice(None),slice(None),a,slice(None)));na1=a_slice(nz1,(slice(None),slice(None),a,slice(None)))
  q=a_add(q,a_mul((ua[0][None,:,None],ua[1][None,:,None]),na));q1=a_add(q1,a_add(a_mul((ua1[0][None,:,None],ua1[1][None,:,None]),na),a_mul((ua[0][None,:,None],ua[1][None,:,None]),na1)))
 Vt=mv(P,q);Vt1=a_add(mv(P1,q),mv(P,q1))
 Dt=compact_contact_right(compact_contact_left(P,nz),compact_contact_swap(P));Dt1=combined_normal_sandwich_contact(P,nz,compact_contact_swap(P),P1,nz1,compact_contact_swap(P1))
 kinetic=a_div64(contact(F['V_raised'],Vt,F1['V_raised'],Vt1,(2,)),s['omega'][:,None]**2,keep,label+'_frequency')
 izt=mv(I,zt);izt1=a_add(mv(I1,zt),mv(I,zt1));zz=a_dd(np.einsum('jpa,pab,jpb->jp',s['z'],s['hi'],lift['zeta']));zz1=contact(z,izt,z1,izt1,(2,))
 quartic=a_div64(a_mul64(-1.,a_add(a_mul(df['configuration']['z2'],zz),a_mul64(s['z2'],zz1))),(B*GC)**2*s['xi'][:,None]**4,keep,label+'_quartic')
 gradient=a_mul64(-ELL**2,contact(F['D_raised'],Dt,F1['D_raised'],Dt1,(2,3)))
 acceleration=contact(zt,(F['a'][0][None],F['a'][1][None]),zt1,(F1['a'][0][None],F1['a'][1][None]),(2,))
 modal=normal_pair_sum(a_mul64(s['w'][:,None,None],a_stack((kinetic,a_mul64(-1.,zz1),quartic,gradient,acceleration),axis=-1)),0)
 zero=a_dd(np.zeros(len(s['U'])));out=a_stack([zero,zero]+[a_slice(modal,(slice(None),i)) for i in range(5)],axis=-1)
 for name,x in (('delta_compensation_covariant_jet',nz1),('delta_compensation_V',Vt1),('delta_compensation_D',Dt1),('terms',out)):combined_normal_put(keep,label,name,x)
 return out

def combined_normal_absolute_phase_contact(s,c,test,d,dc,dtest,keep,label):
 phi=a_dd(s['phi']);dot=normal_action_dot;mv=compact_momentum_matvec
 X1=a_div64(a_mul64(-.5,dot(phi,mv(d['hi'],phi),(1,))),s['phase_X'],keep,label+'_delta_X')
 Xt=a_dd(-np.einsum('pa,pab,pb->p',s['phi'],test['dhi'],s['phi'])/(2*s['phase_X']))
 Xt1=a_sub(a_div64(a_mul64(-.5,dot(phi,mv(dtest['dhi'],phi),(1,))),s['phase_X'],keep,label+'_mixed_X_first'),a_div64(a_mul(Xt,X1),s['phase_X'],keep,label+'_mixed_X_second'))
 pressure=a_add(a_mul64(s['phase_PXX'],a_mul(X1,Xt)),a_mul64(s['phase_PX'],Xt1))
 measure=a_add(a_mul64(s['phase_PX']*test['lm'],X1),a_mul64(s['phase_P'],dtest['lm']))
 out=a_stack((pressure,measure),axis=-1)
 for name,x in (('delta_X',X1),('mixed_test_X',Xt1),('terms',out)):combined_normal_put(keep,label,name,x)
 return out

def combined_normal_EH_contact(s,c,cj,moments,curvature,d,dc,dcj,dm,dcurvature,f,df,b,db,keep,label):
 dot=normal_action_dot;contact=combined_normal_dot_contact;I=a_dd(c['ih']);I1=dc['ih'];K=moments['K'];K1=dm['K'];tau=moments['Ktrace'];tau1=dm['Ktrace']
 Ku=compact_contact_right(compact_contact_left(I,K),I);Ku1=combined_normal_sandwich_contact(I,K,I,I1,K1,I1)
 kinetic=a_sub(a_mul(tau,tau),dot(K,Ku,(1,2)))
 kinetic1=a_sub(a_mul64(2.,a_mul(tau,tau1)),contact(K,Ku,K1,Ku1,(1,2)))
 kt=a_div64(a_add(a_mul64(f*c['sqrt_h'],kinetic1),a_mul64(f,a_mul(dc['sqrt_h'],kinetic))),2*C,keep,label+'_kinetic')
 cv=a_mul64(f,dcurvature['Q'])
 for i in range(3):cv=a_sub(cv,a_mul64(df[:,i+1],a_slice(dcurvature['V'],(slice(None),i))))
 cv=a_div64(cv,2*C,keep,label+'_curvature');Lie=a_dd(np.zeros_like(c['h']));Lie1=a_dd(np.zeros_like(c['h']))
 for i in range(3):
  Lie=a_add(Lie,a_mul64(b[:,i,None,None],a_slice(cj['dh'],(slice(None),i+1,slice(None),slice(None)))))
  Lie1=a_add(Lie1,a_mul64(b[:,i,None,None],a_slice(dcj['dh'],(slice(None),i+1,slice(None),slice(None)))))
 Lie=a_add(Lie,a_dd(np.einsum('pik,pjk->pij',c['h'],db[:,1:])+np.einsum('pkj,pik->pij',c['h'],db[:,1:])))
 dh=a_slice(d['g'],(slice(None),slice(1,None),slice(1,None)))
 for i in range(3):
  for j in range(3):
   part=a_dd(np.zeros(len(s['U'])))
   for k in range(3):part=a_add(part,a_add(a_mul64(db[:,j+1,k],a_slice(dh,(slice(None),i,k))),a_mul64(db[:,i+1,k],a_slice(dh,(slice(None),k,j)))))
   value=a_add(a_slice(Lie1,(slice(None),i,j)),part);Lie1[0][:,i,j]=value[0];Lie1[1][:,i,j]=value[1]
 shift=a_mul64(-1.,contact(moments['metric_EH_tensor'],Lie,dm['metric_EH_tensor'],Lie1,(1,2)))
 out=a_stack((cv,kt,shift),axis=-1)
 for name,x in (('delta_kinetic_invariant',kinetic1),('delta_test_Lie_h',Lie1),('terms',out)):combined_normal_put(keep,label,name,x)
 return out

def combined_normal_density_contact(c,dc,base_terms,native,mode,phase,EH,keep,label):
 # Supplied base terms are earned normal51682 values, not recalculated targets.
 terms=[]
 for name,current,delta in (('native',base_terms['native_metric_terms'],native),('mode',base_terms['mode_compensation_terms'],mode),('phase',base_terms['absolute_phase_terms'],phase)):
  row=a_add(a_mul64(c['dens'],normal_pair_sum(delta,1)),a_mul(dc['dens'],normal_pair_sum(current,1)))
  terms.append(row);combined_normal_put(keep,label,name+'_density',row)
 terms.append(normal_pair_sum(EH,1));components=a_stack(terms,axis=-1);coefficient=normal_pair_sum(components,1)
 combined_normal_put(keep,label,'components',components);combined_normal_put(keep,label,'coefficient',coefficient)
 return dict(component_densities=components,coefficient=coefficient,physical_adoption=False)
