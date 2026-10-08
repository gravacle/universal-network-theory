from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PHASE_VELOCITY_FOUR_NORMAL_CONTACTS_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
PHASE_PAIR_KERNEL='author_fragment_phase_literal_charge_hessian_v002.py'
PHASE_PAIR_SHA='293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143'
CONTACT_KERNEL='author_fragment_phase_velocity_four_normal_contacts_v003.py'
CONTACT_SHA='b0977f2d73a9bf0ab99ef8e9f734ffaf95cded86337b5b2f5c4673d1f92fa4b4'
NORMAL_PARENT='cross_u_paired_current_normal_constraints_v002.py'
NORMAL_PARENT_SHA='a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40'
ADMISSION_FRAGMENT=None
ADMISSION_SHA=None
P=None;K=None;np=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def initialize():
 global P,K,np,capture,normal_keep_pair
 assert PROTOCOL_SHA is not None and ADMISSION_FRAGMENT is not None and ADMISSION_SHA is not None
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('phase_normal_pair_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(finite_phase_charge_restored=False,configuration_updated=False,normal_constraints_qualified=False,joint_constraints_qualified=False,physical_exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
 for n,h in ((PROVIDER,PROVIDER_SHA),(PHASE_PAIR_KERNEL,PHASE_PAIR_SHA),(CONTACT_KERNEL,CONTACT_SHA),(NORMAL_PARENT,NORMAL_PARENT_SHA),(ADMISSION_FRAGMENT,ADMISSION_SHA)):bind(n,h)
 spec=importlib.util.spec_from_file_location('phase_normal_pair_sum',BASE/PHASE_PAIR_KERNEL);K=importlib.util.module_from_spec(spec);spec.loader.exec_module(K);K.P=P;K.np=np
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS)
 for n in (CONTACT_KERNEL,ADMISSION_FRAGMENT):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())
 capture=P.capture;normal_keep_pair=phase_normal_keep
 for n in ('a_dd','a_add','a_sub','a_mul','a_mul64','a_slice','a_reshape'):globals()[n]=getattr(P,n)


def normal_test_mask():
 # All four coefficient fields are axis-even; betaR=R*coefficient is smooth.
 # betaZ is odd across the sheet. Outer test values vanish, not physical fields.
 m=np.ones((4,87,45),dtype=bool);m[:,0]=False;m[:,-1]=False;m[:,:,-1]=False;m[2,:,0]=False
 return m

def extend_normal_tests(a):
 assert a.shape==(4,87,45)
 out=a.copy();out[:,0]=out[:,1];out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 return out

def restrict_normal_rows(a):
 assert a.shape==(4,87,45)
 out=a.copy();out[:,1]+=out[:,0];out[:,0]=0;out[:,-1]=0;out[:,:,-1]=0;out[2,:,0]=0
 return out

def normal_hat_jet(geo,iq,corner,row):
 N,NR,NZ=geo['hats'][iq,corner];R=geo['R'][iq].reshape(86,44)
 if row==1:return (R*N,R*NR+N,R*NZ)
 return (N,NR,NZ)

def evaluate_normal_test(a,geo):
 a=extend_normal_tests(a);out=np.zeros((15136,4,3))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784)
  for corner,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    av=a[row,i:86+i,j:44+j]
    for jet,h in enumerate(normal_hat_jet(geo,iq,corner,row)):out[sl,row,jet]+=(av*h).reshape(3784)
 return out

def scatter_normal_envelope(coeff,geo):
 assert coeff.shape==(15136,4,3) and np.all(coeff>=0)
 out=np.zeros((4,87,45))
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);wq=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for corner,(i,j) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    val=sum(coeff[sl,row,k].reshape(86,44)*h for k,h in enumerate(normal_hat_operation_envelope(geo,iq,corner,row)))
    out[row,i:86+i,j:44+j]+=wq*val
 return restrict_normal_rows(out)

def paired_restrict_normal_rows(x):
 hi,lo=x[0].copy(),x[1].copy();joined=a_add((hi[:,1],lo[:,1]),(hi[:,0],lo[:,0]));hi[:,1]=joined[0];lo[:,1]=joined[1]
 hi[:,0]=lo[:,0]=0;hi[:,-1]=lo[:,-1]=0;hi[:,:,-1]=lo[:,:,-1]=0;hi[2,:,0]=lo[2,:,0]=0
 return hi,lo

def paired_scatter_normal(coeff,geo,label):
 assert coeff[0].shape==coeff[1].shape==(15136,4,3)
 out=a_dd(np.zeros((4,87,45)));normal_keep_pair(label+'_start',out,capture)
 for iq in range(4):
  sl=slice(iq*3784,(iq+1)*3784);weight=(geo['dv'][iq]/geo['R'][iq]).reshape(86,44)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   for row in range(4):
    value=a_dd(np.zeros((86,44)))
    for jet,hat in enumerate(normal_hat_jet(geo,iq,corner,row)):
     value=a_add(value,a_mul64(hat,a_reshape(a_slice(coeff,(sl,row,jet)),(86,44))));normal_keep_pair(label+'_corner_value',value,capture)
    value=a_mul64(weight,value);normal_keep_pair(label+'_weighted_corner_value',value,capture)
    idx=(row,slice(di,86+di),slice(dj,44+dj));joined=a_add(a_slice(out,idx),value);out[0][idx]=joined[0];out[1][idx]=joined[1];normal_keep_pair(label+'_partial',out,capture)
 out=paired_restrict_normal_rows(out);return normal_keep_pair(label+'_restricted',out,capture)

def phase_normal_operation_bound(s,c,f,b,w,keep,label):
 N,h,beta,U=c['N'],c['h'],c['beta'],s['U'];p=len(U);ew=abs(w[0])+abs(w[1]);ehi=abs(s['hi']);ephi=abs(s['phi'])
 eq=np.zeros((p,4,4));eq[:,0,0]=2*abs(N*f)+2*np.einsum('pi,pij,pj->p',abs(beta),abs(h),abs(b));eq[:,0,1:]=np.einsum('pij,pj->pi',abs(h),abs(b));eq[:,1:,0]=eq[:,0,1:]
 ee=np.empty_like(U);ee[:,0]=abs(U[:,0]*f/N);ee[:,1:]=abs(U[:,0,None])*abs(b)+abs(beta)*ee[:,0,None]
 euc=np.maximum(abs(s['uc']),np.einsum('pab,pb->pa',abs(s['g']),abs(U)));educ=np.einsum('pab,pb->pa',eq,abs(U))+np.einsum('pab,pb->pa',abs(s['g']),ee)
 ep=np.eye(4)[None]+euc[:,:,None]*abs(U)[:,None,:];edp=educ[:,:,None]*abs(U)[:,None,:]+euc[:,:,None]*ee[:,None,:]
 edhi=np.einsum('pac,pcd,pdb->pab',ehi,eq,ehi);elm=np.einsum('pab,pba->p',ehi,eq)/2;X=s['phase_X'];PX=abs(s['phase_PX']);PXX=abs(s['phase_PXX'])
 exn=np.einsum('pa,pab,pb->p',ephi,edhi,ephi)/(2*X);raised=np.einsum('pab,pb->pa',ehi,ephi);raisedT=np.einsum('pba,pb->pa',ehi,ephi)
 exv=np.maximum(raised[:,0],(raised[:,0]+raisedT[:,0])/2)*ew/X
 dm=np.einsum('pab,pb->pa',edhi,ephi);dmT=np.einsum('pba,pb->pa',edhi,ephi);emixed=.5*(dm[:,0]+dmT[:,0])*ew/X+exn*exv/X
 epressure=PXX*exn*exv+PX*emixed+elm*PX*exv
 er=np.maximum(abs(s['r']),np.einsum('pab,pb->pa',ep,ephi));edr=np.einsum('pab,pb->pa',edp,ephi);erv=ep[:,:,0]*ew[:,None];edrv=edp[:,:,0]*ew[:,None]
 dot=lambda x,A,y:np.einsum('pa,pab,pb->p',x,A,y)
 einverse=dot(erv,edhi,er)+dot(er,edhi,erv);emeasure=dot(erv,ehi,er)+dot(er,ehi,erv)
 registered=einverse+2*dot(erv,ehi,edr)+2*dot(er,ehi,edrv)
 literal=einverse+dot(edrv,ehi,er)+dot(edr,ehi,erv)+dot(erv,ehi,edr)+dot(er,ehi,edrv)
 out=abs(c['dens'])[:,None]*(epressure[:,None]+.5*np.column_stack((registered+elm*emeasure,literal+elm*emeasure)))
 keep(label+'_coefficient_operation_envelope',out);return out

def phase_normal_fixture():
 U=np.array(((1.,3/4,0.,0.),));g=np.diag((-25/16,1.,1.,1.))[None];hi=np.diag((-16/25,1.,1.,1.))[None];uc=np.einsum('pab,pb->pa',g,U);projector=np.eye(4)[None]+uc[:,:,None]*U[:,None,:];phi=np.array(((35/32,0.,0.,0.),))
 s=dict(g=g,hi=hi,U=U,uc=uc,P=projector,phi=phi,r=np.einsum('pab,pb->pa',projector,phi),phase_X=np.array((7/8,)),phase_PX=np.array((3/8,)),phase_PXX=np.array((2.,)))
 c=dict(N=np.array((5/4,)),h=np.eye(3)[None],beta=np.zeros((1,3)),dens=np.array((5/4,)));w=P.a_dd(np.array((1/4,)));answer=np.zeros((1,4,2));env=np.zeros_like(answer)
 for n,a in {**s,**{'chart_'+k:v for k,v in c.items()},'velocity_hi':w[0],'velocity_lo':w[1]}.items():P.capture('fixture_'+n,a)
 for row in range(4):
  f=np.ones(1) if row==0 else np.zeros(1);b=np.zeros((1,3))
  if row:b[:,row-1]=1
  lift=phase_normal_lift_values(s,c,f,b,P.capture,'fixture_lift_%d'%row);out=phase_velocity_normal_contact(s,c,lift,w,P.capture,'fixture_contact_%d'%row)
  for ci,n in enumerate(('registered_normal','literal_action')):answer[:,row,ci]=out[n][0]+out[n][1]
  env[:,row]=phase_normal_operation_bound(s,c,f,b,w,P.capture,'fixture_bound_%d'%row);P.capture('fixture_completed_contacts',answer);P.capture('fixture_completed_envelope',env)
 target=np.zeros_like(answer);target[:,0]=-161/640
 P.check('new_tilted_phase_velocity_four_normal_contact',answer,target,env+abs(target));return dict(lapse_contact=-161/640,shift_contacts=(0.,0.,0.),physical_parameters_selected=False)

def phase_normal_column(iq,ref,velocity):
 P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.clear();P.CONTEXT.update(stage='new_phase_velocity_four_normal_contacts',column=iq)
 names=('config_g','config_hi','config_U','config_uc','config_P','config_phi','config_r','config_phase_X','config_phase_PX','config_phase_PXX','chart_N','chart_h','chart_beta','chart_dens','chart_sqrt_h','chart_ih','chart_u')
 raw=P.read_pair(ref,names);s={n[7:]:a for n,a in raw.items() if n.startswith('config_')};c={n[6:]:a for n,a in raw.items() if n.startswith('chart_')};assert s['U'].shape==(3784,4) and c['N'].shape==(3784,)
 w=P.a_slice(velocity['value'],slice(iq*3784,(iq+1)*3784));contacts={n:P.a_dd(np.zeros((3784,4))) for n in ('registered_normal','literal_action','literal_minus_registered_normal_gap')};env=np.zeros((3784,4,2));measuregap=np.zeros((3784,4));reduced=P.a_dd(np.zeros((3784,4)))
 for row in range(4):
  P.RAW.clear();P.AVAILABLE.clear()
  for n,x in contacts.items():phase_normal_keep('completed_'+n,x,P.capture)
  P.capture('completed_operation_envelope',env);P.capture('completed_measure_lapse_gap',measuregap)
  f=np.ones(3784) if row==0 else np.zeros(3784);b=np.zeros((3784,3))
  if row:b[:,row-1]=1
  lift=phase_normal_lift_values(s,c,f,b,P.capture,'current_lift');out=phase_velocity_normal_contact(s,c,lift,w,P.capture,'current_contact')
  for n,x in contacts.items():
   for wi in (0,1):x[wi][:,row]=out[n][wi]
   phase_normal_keep('completed_'+n,x,P.capture)
  env[:,row]=phase_normal_operation_bound(s,c,f,b,w,P.capture,'current_bound');measuregap[:,row]=lift['measure_lapse_identity_gap'];P.capture('completed_operation_envelope',env);P.capture('completed_measure_lapse_gap',measuregap)
 up=P.a_matvec(c['ih'],P.a_dd(c['u']));norm_b=K.phase_pair_sum(P.a_mul(P.a_dd(c['u']),up),1,P.capture,'reduced_native_norm_b');phase_normal_keep('reduced_native_norm_b',norm_b,P.capture)
 exact_h=P.a_div64(P.a_mul64(c['sqrt_h'],P.a_sub(P.a_dd(s['phase_PXX']),norm_b)),c['N'],P.capture,'reduced_H');red=P.a_mul64(-s['phase_X'],P.a_mul(exact_h,w))
 for wi in (0,1):reduced[wi][:,0]=red[wi]
 phase_normal_keep('reduced_chart_contact',reduced,P.capture);literal_reduced=P.a_sub(contacts['literal_action'],reduced);phase_normal_keep('literal_minus_reduced_chart_contact',literal_reduced,P.capture)
 data=dict(coefficient_operation_envelope=env,measure_lapse_identity_gap=measuregap,inverse_symmetry_gap=s['hi']-s['hi'].transpose(0,2,1))
 for n,x in {**contacts,'reduced_chart_contact':reduced,'literal_minus_reduced_chart_contact':literal_reduced}.items():
  for wi,suffix in enumerate(('hi','lo')):data[n+'_'+suffix]=x[wi].copy()
 for n,x in velocity.items():
  for wi,suffix in enumerate(('hi','lo')):data['phase_velocity_'+n+'_'+suffix]=x[wi][iq*3784:(iq+1)*3784].copy()
 rec=P.checkpoint('COLUMN',data,dict(kind='paired_phase_velocity_only_four_normal_value_contacts',column=iq,current_configuration_parent=ref,normal_rows=['lapse','shift_R','shift_Z','shift_phi'],value_coefficients_only=True,normal_test_gradient_contact_zero=True,instantaneous_phi_i_unchanged=True,mixed_jets_preserved=True,configuration_or_source_updated=False,finite_charge_restored=False))
 return contacts,env,rec

def phase_normal_packet(phase):
 geo=P.read_pair(phase['input'],('R','dv','hats','cell_i','cell_j','r','z'));assert geo['R'].shape==geo['dv'].shape==(4,3784) and geo['hats'].shape==(4,4,3,86,44)
 j=P.read_pair(phase['jets'],tuple('phase_velocity_'+n+'_'+w for n in ('value','R','Z') for w in ('hi','lo')));velocity={n:(j['phase_velocity_'+n+'_hi'],j['phase_velocity_'+n+'_lo']) for n in ('value','R','Z')};assert all(x[0].shape==x[1].shape==(15136,) for x in velocity.values())
 P.checkpoint('INPUT',j,dict(kind='earned_same_scalar_phase_velocity_words_for_new_normal_contact',phase_refs=phase,prior_native_metric_and_phase_canonical_targets_unchanged=True,old_features_H_mass_or_normal_rows_replayed=False))
 P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='new_tilted_phase_normal_control');fixture=phase_normal_fixture();P.checkpoint('FIXTURE',{**P.AVAILABLE,**P.RAW},dict(kind='new_independent_nonzero_tilted_phase_normal_contact',fixture=fixture,controls=P.CHECKS.copy()))
 P.checkpoint('BASIS',geo,dict(kind='unchanged_regular_normal_Q1_test_basis_for_phase_contact',parent=phase['input'],normal_free_dimension=14875,outer_test_zero_is_not_physical_boundary=True))
 columns=[];bounds=[];refs=[]
 for iq,ref in enumerate(phase['pilot_columns']):
  contacts,env,rec=phase_normal_column(iq,ref,velocity);columns.append(contacts);bounds.append(env);refs.append(rec)
 P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.update(stage='new_phase_contact_weak_normal_rows');fields={};differences=[];fe_bounds=[];env=np.concatenate(bounds)
 test=(np.arange(4*87*45)%13-6).reshape(4,87,45)/37.;test*=normal_test_mask();testjet=evaluate_normal_test(test,geo);weight=(geo['dv']/geo['R']).reshape(15136)
 for ci,name in enumerate(('registered_normal','literal_action')):
  value=tuple(np.concatenate([col[name][wi] for col in columns]) for wi in (0,1));coeff=P.a_dd(np.zeros((15136,4,3)))
  for wi in (0,1):coeff[wi][:,:,0]=value[wi]
  action=paired_scatter_normal(coeff,geo,name+'_action');phase_normal_keep(name+'_weak_action',action,P.capture);ham=(-action[0],-action[1]);phase_normal_keep(name+'_weak_Hamiltonian_rows',ham,P.capture);fields[name]=ham
  nodal=K.phase_pair_sum(P.a_reshape(P.a_mul64(test,action),(-1,)),0,P.capture,name+'_nodal_functional');direct=K.phase_pair_sum(P.a_reshape(P.a_mul64(weight[:,None],P.a_mul64(testjet[:,:,0],value)),(-1,)),0,P.capture,name+'_direct_functional');difference=P.a_sub(nodal,direct);phase_normal_keep(name+'_functional_difference',difference,P.capture);differences.append(float(difference[0]+difference[1]))
  e=np.zeros((15136,4,3));e[:,:,0]=env[:,:,ci];nodal_envelope=scatter_normal_envelope(e,geo);P.capture(name+'_weak_operation_envelope',nodal_envelope);fe_bounds.append(float(np.sum(abs(test)*nodal_envelope)+np.sum(weight[:,None]*abs(testjet[:,:,0])*env[:,:,ci])))
 gap=P.a_sub(fields['literal_action'],fields['registered_normal']);phase_normal_keep('literal_minus_registered_weak_normal_gap',gap,P.capture)
 P.capture('functional_test',test);P.capture('functional_test_qpoint',testjet);P.check('new_phase_contact_regular_normal_Q1_functional',np.array(differences),np.zeros(2),np.array(fe_bounds))
 data={n:a for n,a in P.AVAILABLE.items() if n.startswith(('registered_normal_','literal_action_','literal_minus_registered_','functional_'))};data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 loads=P.checkpoint('LOADS',data,dict(kind='new_phase_velocity_four_same_action_weak_normal_contact',columns=refs,normal_row_sign='Hamiltonian_contact equals minus action_contact',phase_and_ordinary_canonical_priors_unchanged=True,ordinary_contact_zero=True,baseline_normal_and_mean_comparison_refs=phase['comparison_refs'],prior_signed_primitive_readout=phase['prior_readout'],baseline_rows_added_or_subtracted=False,primitive_legendre_bridge_resolved=False,temporal_improvement_ports=None,physical_outer_GHY=None,physical_exterior=None,finite_charge_restored=False,controls=P.CHECKS[-1:]))
 assert len(P.CHECKS)==2 and all(c['passed'] for c in P.CHECKS) and len(P.RECORDS)==8
 return dict(status='PHASE_VELOCITY_FOUR_NORMAL_LINEAR_CONTACT_COMPLETE',columns=refs,loads=loads,controls=P.CHECKS,checkpoints=P.RECORDS,phase_linear_response_admitted=True,normal_constraints_qualified=False,finite_phase_charge_restored=False,configuration_updated=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root and distinct FULL reviews required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA);P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_phase_velocity_normal_contact');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,phase=phase_normal_admission()
  for n,h in pins.items():bind(n,h)
  case=phase_normal_packet(phase);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=2,pairs=8)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_new_phase_normal_contact_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
