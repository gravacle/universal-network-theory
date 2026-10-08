"""Definitions only: three independent controls for NEW normal derivatives.
No previous fixture, primitive, FE or operator is replayed. Caller supplies
np,P,keep, admitted a_* and the new stress/curvature contact definitions.
Current/expected words are captured before gates. No numerical author calls.
"""
def fresh_combined_normal_contact_controls():
 eps=2.**-30;zero=lambda shape:a_dd(np.zeros(shape));I=np.eye(3)[None]
 K0=np.diag((1.,-2.,3.))[None];K1=np.diag((2.,1.,-1.))[None]
 K=(K0,eps*K1);tau=(np.array([2.]),np.array([2*eps]));Kcontact=a_dd(K1)
 s=dict(U=np.zeros((1,4)));c=dict(ih=I,h=I,N=np.ones(1),sqrt_h=np.ones(1))
 cj=dict(dh=zero((1,4,3,3)));dcj=dict(dh=zero((1,4,3,3)));dc=dict(ih=zero((1,3,3)),sqrt_h=zero((1,)))
 moments=dict(K=K,Ktrace=tau,metric_EH_tensor=zero((1,3,3)));dm=dict(K=Kcontact,Ktrace=a_dd(np.array([2.])),metric_EH_tensor=zero((1,3,3)))
 d=dict(g=zero((1,4,4)));curvature=dict(Q=np.zeros(1),V=np.zeros((1,3)));dcurvature=dict(Q=zero((1,)),V=zero((1,3)))
 eh=combined_normal_EH_contact(s,c,cj,moments,curvature,d,dc,dcj,dm,dcurvature,np.ones(1),np.zeros((1,4)),np.zeros((1,3)),np.zeros((1,4,3)),keep,'fresh_EH_contact')
 expected=a_div64((np.array([14.]),np.array([-4*eps])),2*C,keep,'fresh_EH_expected_units');actual=a_slice(eh,(slice(None),1));error=a_sub(actual,expected)
 for n,x in (('actual',actual),('expected',expected),('error',error)):normal_keep_pair('fresh_EH_'+n,x,keep)
 P.check('new_EH_kinetic_contact_retains_current_low_word',error[0]+error[1],np.zeros(1),np.full(1,128/(2*abs(C))))
 shapes=dict(V=(32,1,4),V_raised=(32,1,4),D=(32,1,4,4),D_raised=(32,1,4,4),F=(1,4,4),Fup=(1,4,4),a=(1,4))
 F={n:zero(sh) for n,sh in shapes.items()};F1={n:zero(sh) for n,sh in shapes.items()}
 for n in ('V','V_raised'):F[n][0][0,0,0]=2.;F[n][1][0,0,0]=eps;F1[n][0][0,0,0]=1.
 T={n:zero(shapes[k]) for n,k in (('dV','V'),('dD','D'),('dF','F'),('da','a'))};T1={n:zero(shapes[k]) for n,k in (('dV','V'),('dD','D'),('dF','F'),('da','a'))}
 T['dV'][0][0,0,0]=3.;T1['dV'][0][0,0,0]=4.
 w=np.zeros(32);w[0]=1.;s=dict(hi=np.eye(4)[None],z=np.zeros((32,1,4)),r=np.zeros((1,4)),z2=np.zeros((32,1)),omega=np.ones(32),xi=np.ones(32),w=w)
 d=dict(hi=zero((1,4,4)),z=zero((32,1,4)));df=dict(paired=F1,configuration=dict(r=zero((1,4)),z2=zero((32,1))))
 test=dict(paired=T,dhi=np.zeros((1,4,4)),dr=np.zeros((1,4)),lm=np.zeros(1));dtest=dict(paired=T1,dhi=zero((1,4,4)),dr=zero((1,4)),lm=zero((1,)))
 out=combined_normal_native_contact(s,dict(paired=F),test,d,df,dtest,keep,'fresh_modal_contact')
 expected=zero((1,7));expected[0][0,2]=11.;expected[1][0,2]=4*eps;error=a_sub(out,expected)
 for n,x in (('actual',out),('expected',expected),('error',error)):normal_keep_pair('fresh_modal_'+n,x,keep)
 P.check('new_native_kinetic_mixed_contact_retains_all_products',error[0]+error[1],np.zeros((1,7)),np.full((1,7),128.))
 R=np.array([1.5]);h=np.array([np.diag((1.,1.,R[0]**2))]);ih=np.array([np.diag((1.,1.,R[0]**-2))]);dh=np.zeros((1,4,3,3));dh[0,1,2,2]=2*R[0]
 grad=np.array((1/7.,-1/9.,0.));delta_dh=np.zeros_like(dh)
 for a in range(3):delta_dh[:,a+1]=4*grad[a]*h
 bar=np.zeros((1,3,3,3));bar[:,0,2,2]=-R;bar[:,2,0,2]=bar[:,2,2,0]=1/R
 ec=2*abs(bar);curvature=dict(C3=np.zeros_like(bar),envelope_C3=ec,Q=np.zeros(1),V=np.zeros((1,3)),envelope_Q=np.full(1,32.),envelope_V=np.full((1,3),16.))
 dc=dict(ih=zero((1,3,3)),sqrt_h=zero((1,)),log_dens=zero((1,)));envelopes=dict(delta_ih=np.zeros((1,3,3)),dh=abs(dh[:,1:]),delta_dh=abs(delta_dh[:,1:]),delta_sqrt_h=np.zeros(1))
 cv=combined_curvature_contact(dict(R=R),dict(ih=ih,sqrt_h=R),dict(dh=a_dd(dh)),curvature,dc,dict(dh=a_dd(delta_dh)),envelopes,keep,'fresh_flat_curvature_contact')
 actual=a_stack((cv['Q'],a_slice(cv['V'],(slice(None),0)),a_slice(cv['V'],(slice(None),1)),a_slice(cv['V'],(slice(None),2))),axis=-1)
 expected=a_dd(np.array([[0.,-8*R[0]*grad[0],-8*R[0]*grad[1],0.]]));error=a_sub(actual,expected)
 env=np.column_stack((cv['envelope_Q'],cv['envelope_V']))
 for n,x in (('actual',actual),('expected',expected),('error',error)):normal_keep_pair('fresh_curvature_'+n,x,keep)
 P.check('new_flat_conformal_reference_curvature_contact',error[0]+error[1],np.zeros((1,4)),env)
 return dict(kind='new_EH_native_and_flat_reference_first_contact_controls',controls=3,old_fixtures_replayed=False)
