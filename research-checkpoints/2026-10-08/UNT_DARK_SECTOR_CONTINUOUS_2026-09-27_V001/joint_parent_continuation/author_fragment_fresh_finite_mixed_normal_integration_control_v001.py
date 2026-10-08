"""HELD one NEW shared225/160 phase+ordinary+EH integration control.
Globals np,math,P,Fraction,Decimal,localcontext,EXACT_TARGETS and reviewed
225/160/239/116/62/49 definitions. No invocation or old fixture replay.
Synthetic A0=X0=1 is a declared unit test, with unchanged epsilon=1e-5.
Independent Decimal100 references use the published raw inverse hi00;
they never replace a serialized inverse/connection by an ideal ADM identity.
"""
FINITE_MIXED_CONTROL_AUTHOR_DRAFT=True
FINITE_MIXED_CONTROL_AUTHORING_IN_PROGRESS=False

def mixed_pair(value):
 h=np.asarray(value,dtype=np.float64);return h.copy(),np.zeros_like(h)

def mixed_capture(prefix,value,keep):
 if isinstance(value,dict):
  for n,x in value.items():mixed_capture(prefix+'_'+n,x,keep)
 elif isinstance(value,(tuple,list)):
  if len(value)==2 and all(isinstance(w,np.ndarray) for w in value):keep(prefix+'_hi',value[0]);keep(prefix+'_lo',value[1])
  else:
   for i,x in enumerate(value):mixed_capture(prefix+'_'+str(i),x,keep)
 elif isinstance(value,(np.ndarray,float,int,bool)):keep(prefix,np.asarray(value).copy())

def mixed_independent_inputs():
 # h=dR^2+dZ^2+R^2 dphi^2 at R=1; E0=0, owned gauge jets zero.
 N0=5/4;q=1+2.**-20;h=np.eye(3)[None];hdot=np.diag([5/2,5.,-5/2])[None]
 hr=np.zeros((1,2,3,3));hr[0,0,2,2]=2.;Q=np.diag([2.,1.,3.])[None];Qr=np.zeros_like(hr);Qr[0,0,2,2]=6.
 geometry=dict(h=mixed_pair(h),ih=mixed_pair(h),mu=mixed_pair([1.]),h_spatial_jets=mixed_pair(hr))
 gauge=dict(N=mixed_pair([N0]),beta=mixed_pair(np.zeros((1,3))),N_jets=mixed_pair(np.zeros((1,4))),beta_jets=mixed_pair(np.zeros((1,4,3))))
 covectors=dict(u=mixed_pair(np.zeros((1,3))),z=mixed_pair(np.zeros((32,1,3))),u_jets=mixed_pair(np.zeros((1,4,3))),z_jets=mixed_pair(np.zeros((32,1,4,3))))
 mechanical=dict(h_dot=mixed_pair(hdot));phase=dict(phi=mixed_pair([[25/16*q,3/4*q,0.,0.]]))
 g=np.diag([-N0*N0,1.,1.,1.])[None];hi=np.diag([-1/(N0*N0),1.,1.,1.])[None]
 dg=np.zeros((1,4,4,4));dg[:,0,1:,1:]=hdot;dg[0,1,3,3]=2.;Ga=np.zeros_like(dg)
 for i in range(3):Ga[0,0,i+1,i+1]=-hi[0,0,0]*hdot[0,i,i]/2;Ga[0,i+1,0,i+1]=Ga[0,i+1,i+1,0]=hdot[0,i,i]/2
 Ga[0,1,3,3]=-1.;Ga[0,3,1,3]=Ga[0,3,3,1]=1.
 value=dict(g=mixed_pair(g),hi=mixed_pair(hi),U=mixed_pair([[1/N0,0.,0.,0.]]),uc=mixed_pair([[-N0,0.,0.,0.]]),P=mixed_pair(np.diag([0.,1.,1.,1.])[None]),z=mixed_pair(np.zeros((32,1,4))),up=mixed_pair(np.zeros((1,3))),gamma=mixed_pair([1.]),dens=mixed_pair([N0]),du=mixed_pair(np.zeros((1,4,4))),dz=mixed_pair(np.zeros((32,1,4,4))),dg=mixed_pair(dg),Ga=mixed_pair(Ga))
 spacetime=dict(value=value,delta={n:mixed_pair(np.zeros_like(a[0])) for n,a in value.items()})
 reference={n:value[n] for n in ('g','hi','U','z','du','dz','dg','Ga')};reference.update(E0=mixed_pair(np.zeros_like(dg)),canonical_targets=dict(kind='NEW_manufactured_only',physical_prior_selected=False),prior_bridge_references=dict(kind='NEW_manufactured_only',physical_stationarity_admitted=False))
 material=dict(omega=np.ones(32),xi=np.ones(32),w=np.ones(32),B=P.B,GC=P.GC,ALPHA=P.ALPHA,ELL=P.ELL,C=P.C,R=np.array([1.]),Z_coordinate=np.array([1.]))
 direction=dict(h=mixed_pair(Q),h_spatial_jets=mixed_pair(Qr),h_dot=mixed_pair(np.zeros_like(hdot)),u_jets=mixed_pair(np.zeros((1,4,3))),z_jets=mixed_pair(np.zeros((32,1,4,3))))
 labels=dict(existing_once_counted_branch_registered=True,provenance='NEW positive manufactured canonical labels; not a physical galaxy/source branch',galaxy_mass_weight=mixed_pair([2.]),galaxy_specific_covector=mixed_pair([[3/4,0.,0.]]),reference_dust_energy_weight=mixed_pair([1/4]),radiation_weights=mixed_pair([[1/2],[1/4],[1/8]]),radiation_covectors=mixed_pair([[[1.,0.,0.]],[[0.,2.,0.]],[[0.,0.,4.]]]))
 constants=dict(eps=1e-5,norm=1/1e-5-math.log1p(1/1e-5),X0=1.,A0=1.,synthetic_control=True,relative_phase_coefficient=1.)
 return (geometry,spacetime,gauge,covectors,mechanical,phase,material,reference),direction,labels,constants

def mixed_decimal_pair(name,rows,keep):
 shape=(len(rows),len(rows[0]));values=[x for row in rows for x in row];hi=[];lo=[];remainders=[]
 for x in values:
  h=float(x);l=float(x-Decimal.from_float(h));hi.append(h);lo.append(l);remainders.append(str(x-Decimal.from_float(h)-Decimal.from_float(l)))
 EXACT_TARGETS[name]=dict(shape=shape,decimal100_values=[str(x) for x in values],two_word_conversion_remainders=remainders)
 out=(np.array(hi).reshape(shape),np.array(lo).reshape(shape));mixed_capture('independent_'+name,out,keep);return out

def mixed_independent_references(candidate,constants,keep):
 with localcontext() as ctx:
  ctx.prec=100;D=Decimal;F=Fraction;zero=D(0);one=D(1)
  raw=lambda x:D.from_float(float(x));a=raw(-candidate['s']['hi'][0,0,0]);N=raw(candidate['c']['N'][0]);t=raw(candidate['s']['phi'][0,0]);p=raw(candidate['s']['phi'][0,1]);C=raw(P.C)
  X=(a*t*t-p*p).sqrt();dX=p*p/X;eps,norm,X0,A0=(raw(constants[n]) for n in ('eps','norm','X0','A0'));q=X/X0;u=q*q-one;d=eps-u;ss=u/d
  assert zero<u<eps
  logarithm=(one+ss).ln();pressure=A0*((logarithm-ss/(one+ss))/norm-one)
  PX=A0*2*q*ss/(eps*norm*X0);PXX=A0*(2*ss/(eps*norm)+4*q*q/(norm*d*d))/(X0*X0)
  PXXX=A0*(12*q/(norm*d*d)+16*q*q*q/(norm*d*d*d))/(X0*X0*X0)
  EXACT_TARGETS['independent_EOS']=dict(precision=100,raw_inverse_00=str(-a),raw_phi_time=str(t),raw_phi_radial=str(p),u=str(u),d=str(d),log1p_s=str(logarithm),norm=str(norm),mathematical_norm_minus_binary_norm=str(one/eps-(one+one/eps).ln()-norm),PXXX=str(PXXX))
  A=N*N*a*a*t*t;B=N*a*t*p;w=p*p;chain=(PXX/X-PX/(X*X))*dX;t0=N*N*a
  absH=[A*PX/X-pressure,B*PX/X,zero,zero];dabs=[3*absH[0]+A*chain-PX*dX,3*absH[1]+B*chain,zero,zero]
  relH=[w/2,zero,zero,zero];drel=[w/2,zero,zero,zero]
  # Fixed hdot, actual KGamma=t0*diag(1,2,-1), not ideal KADM.
  EH=[t0*t0*(4*t0-3)/C,-3*t0*t0/C,zero,zero];dEH=[-4*EH[0],-5*t0*t0/C,zero,zero]
  ordinary=[D(F(17,4).numerator)/D(F(17,4).denominator),-D(2),-one/2,-one/2];dordinary=[-D(12)/5,zero,zero,zero]
  total=[EH[i]+absH[i]+relH[i]+ordinary[i] for i in range(4)];dtotal=[dEH[i]+dabs[i]+drel[i]+dordinary[i] for i in range(4)]
  rows=dict(EOS=[[X,pressure,PX,PXX],[dX,PX*dX,PXX*dX,PXXX*dX]],ordinary=[ordinary,dordinary],EH=[EH,dEH],phase_absolute=[absH,dabs],phase_relative=[relH,drel],total=[total,dtotal],action=[[-x for x in total],[-x for x in dtotal]])
  # Bounds are sums of upstream uncancelled terms, never abs(final defect).
  eabs=[abs(A*PX/X)+abs(pressure)+abs(B*PX/X)+w,3*sum(map(abs,absH))+abs(A*chain)+abs(B*chain)+abs(PX*dX)+w]
  eEH=[(abs(t0*t0*(4*t0-3))+3*t0*t0+20*t0*t0)/C,(4*abs(t0*t0*(4*t0-3))+5*t0*t0+80*t0*t0)/C]
  eord=[D(17)/4+D(2)+one,D(12)/5+D(2)+one];erel=[w,w]
  envelopes=dict(EOS=[sum(map(abs,r)) for r in rows['EOS']],ordinary=eord,EH=eEH,phase_absolute=eabs,phase_relative=erel,total=[eabs[i]+eEH[i]+eord[i]+erel[i] for i in range(2)])
  envelopes['action']=envelopes['total']
  targets={n:mixed_decimal_pair(n,r,keep) for n,r in rows.items()};bounds={n:np.broadcast_to(np.array([float(x) for x in v])[:,None],(2,4)).copy() for n,v in envelopes.items()}
  for n,v in bounds.items():keep('independent_'+n+'_upstream_operation_envelope',v)
  EXACT_TARGETS['analytical_ordinary']=dict(energy='17/4',momentum=['2','1/2','1/2'],stress_diagonal=['7/5','1/2','1/2'],delta_energy='-12/5',fixed_canonical_weights_no_extra_mu=True)
  EXACT_TARGETS['analytical_EH']=dict(t0=str(t0),K_Gamma_diagonal=[str(t0),str(2*t0),str(-t0)],delta_mu='3',delta_trace=str(-t0),relative_phase_coefficient='1',native_Maxwell_and_modal_terms_identically_zero=True)
  return targets,bounds

def fresh_finite_mixed_normal_integration_control(keep,check):
 inputs,direction,labels,constants=mixed_independent_inputs();names=('geometry','spacetime','gauge','covectors','mechanical','phase','material','reference')
 mixed_capture('fresh_input',dict(zip(names,inputs)),keep);mixed_capture('fresh_direction',direction,keep);mixed_capture('fresh_labels',labels,keep);mixed_capture('fresh_constants',constants,keep)
 candidate=finite_candidate_raw_action_adapter(*inputs,P.paired_current_affine_features,P.paired_current_affine_momenta,keep,'mixed_NEW_raw');mixed_capture('completed_candidate',candidate,keep)
 contact=finite_candidate_configuration_contact(candidate,inputs[0],inputs[2],inputs[3],inputs[4],direction,inputs[7],keep,'mixed_NEW_contact');mixed_capture('completed_contact',contact,keep)
 targets,bounds=mixed_independent_references(candidate,constants,keep)
 s={n:P.a_dd(candidate['s'][n]) for n in ('g','hi','U','uc','P','phi')};c={n:P.a_dd(candidate['c'][n]) for n in ('N','h','beta','ih','u')};c['mu']=P.a_dd(candidate['c']['sqrt_h'])
 d={n:contact['d'][n] if n in contact['d'] else contact['dc'][n] for n in set(s)|set(c)};d['mu']=contact['dc']['sqrt_h']
 eos=candidate_invariant_phase_eos_current(s,c,d,constants,keep,'mixed_NEW_invariant_EOS');mixed_capture('completed_EOS',eos,keep)
 ordinary=finite_fixed_canonical_ordinary_point(dict(h=c['h'],ih=c['ih'],delta_h=d['h'],delta_ih=d['ih']),dict(N=c['N'],beta=c['beta']),labels,keep,'mixed_NEW_ordinary');mixed_capture('completed_ordinary',ordinary,keep)
 curvature=finite_candidate_intrinsic_curvature(candidate,contact,keep,'mixed_NEW_curvature');mixed_capture('completed_curvature',curvature,keep)
 actual=dict(EOS=P.a_stack([P.a_stack([P.a_slice(eos[family][n],0) for n in ('X','pressure','PX','PXX')],0) for family in ('value','delta')],0),ordinary=P.a_stack([ordinary[family]['normal_density'] for family in ('value','delta')],0));actual['ordinary']=(actual['ordinary'][0][:,0,:],actual['ordinary'][1][:,0,:]);records=[]
 for row in range(4):
  f=np.array([float(row==0)]);b=np.zeros((1,3));df=np.zeros((1,4));db=np.zeros((1,4,3))
  if row:b[0,row-1]=1.
  mixed_capture('test%d_input'%row,dict(f=f,b=b,df=df,db=db),keep)
  native=finite_candidate_native_EH_normal(candidate,contact,curvature,f,df,b,db,0.,inputs[7],keep,'mixed_NEW_test%d_native_EH'%row);mixed_capture('completed_test%d_native_EH'%row,native,keep)
  phase=candidate_phase_normal_stress(s,c,d,eos,f,b,keep,'mixed_NEW_test%d_phase'%row);mixed_capture('completed_test%d_phase'%row,phase,keep)
  total=finite_candidate_total_normal(native,phase,ordinary,f,b,keep,'mixed_NEW_test%d_total'%row);mixed_capture('completed_test%d_total'%row,total,keep)
  assert total['relative_phase_count']==total['ordinary_label_count']==1 and not total['finite_candidate_physically_admitted']
  records.append((native,phase,total))
 for name,index,key,sign in (('EH',0,'EH',-1.),('phase_absolute',1,'absolute',-1.),('phase_relative',1,'relative',-1.),('total',2,'hamiltonian',1.),('action',2,'action',1.)):
  actual[name]=P.a_stack([P.a_stack([P.a_mul64(sign,P.a_slice(record[index][family][key],0)) for record in records],0) for family in ('value','delta')],0);mixed_capture('completed_all_four_'+name,actual[name],keep)
 for name in targets:check('mixed_independent_'+name,actual[name],targets[name],bounds[name])
 native=P.a_stack([P.a_stack([P.a_slice(record[0][family]['native'],0) for record in records],0) for family in ('value','delta')],0);mixed_capture('completed_native_identically_zero',native,keep)
 assert all(np.all(w==0) for w in native),'NEW rest native Maxwell/modal control must be exactly zero in both words'
 keep('mixed_native_zero_and_once_counts_exact_predicate',np.asarray(True))
 return dict(status='NEW_SHARED_CANDIDATE_MIXED_FOUR_NORMAL_CONTROL_PASS',independent_decimal_precision=100,normal_rows=4,value_and_configuration_direction=True,relative_phase_count=1,ordinary_label_count=1,native_terms_exactly_zero=True,synthetic_EOS_units=True,physical_epsilon=constants['eps'],same_raw225_candidate_and160_contact=True,old_fixture_operator_solver_or_source_replayed=False,physical_adoption=False)
