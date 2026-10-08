from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PHASE_VELOCITY_FOUR_NORMAL_CONTACTS_V002'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='7351c4c6c3ef32882e7620d213b7fa2ef3779bac5eb85911305fd9d3a2e0c57a'
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
PHASE_PAIR_KERNEL='author_fragment_phase_literal_charge_hessian_v002.py'
PHASE_PAIR_SHA='293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143'
CONTACT_KERNEL='author_fragment_phase_velocity_four_normal_contacts_v003.py'
CONTACT_SHA='b0977f2d73a9bf0ab99ef8e9f734ffaf95cded86337b5b2f5c4673d1f92fa4b4'
NORMAL_PARENT='cross_u_paired_current_normal_constraints_v002.py'
NORMAL_PARENT_SHA='a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40'
ADMISSION_FRAGMENT='author_fragment_failed_phase_four_normal_admission_v001.txt'
ADMISSION_SHA='5e484efc6e088b89aacce89c9f4aa97cf3ab0226fb836a735636e1ac57552945'
P=None;K=None;np=None;RAW_CAPTURE=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def phase_normal_numeric_capture(name,a):
 # Numeric scalars are zero-dimensional arrays; values/precision are unchanged.
 array=np.asarray(a).copy();assert array.dtype.kind in 'fiub',name
 RAW_CAPTURE(name,array);return a

def phase_normal_copy_completed(tag,ref,arrays):
 md={n:v for n,v in ref['metadata'].items() if n not in ('owner','qualification','schema','failed')}
 md.update(recovered_completed_parent={n:ref[n] for n in ('file','sha256','commit_file','commit_sha256')},completed_fixture_or_point_contact_replayed=False)
 return P.checkpoint(tag,arrays,md)

def initialize():
 global P,K,np,capture,normal_keep_pair,RAW_CAPTURE
 assert PROTOCOL_SHA is not None and ADMISSION_FRAGMENT is not None and ADMISSION_SHA is not None
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('phase_normal_pair_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 RAW_CAPTURE=P.capture;P.capture=phase_normal_numeric_capture
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

def normal_hat_operation_envelope(geo,iq,corner,row):
 N,NR,NZ=geo['hats'][iq,corner];R=geo['R'][iq].reshape(86,44)
 if row==1:return (R*abs(N),R*abs(NR)+abs(N),R*abs(NZ))
 return (abs(N),abs(NR),abs(NZ))

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

def phase_normal_packet(failed):
 phase=failed['phase'];assert failed['completed_fixture_and_point_contacts_replay_allowed'] is False and failed['uncommitted_weak_assembly_and_functional_control_only'] is True
 inp=P.read_pair(failed['input'],tuple(failed['input']['metadata']['schema']));phase_normal_copy_completed('INPUT',failed['input'],inp)
 fixtures=P.read_pair(failed['fixture'],tuple(failed['fixture']['metadata']['schema']));assert P.CHECKS==[];P.CHECKS.extend(failed['controls']);phase_normal_copy_completed('FIXTURE',failed['fixture'],fixtures)
 geo=P.read_pair(failed['basis'],tuple(failed['basis']['metadata']['schema']));assert geo['R'].shape==geo['dv'].shape==(4,3784) and geo['hats'].shape==(4,4,3,86,44) and np.all(geo['R']>0) and np.all(geo['dv']>0);phase_normal_copy_completed('BASIS',failed['basis'],geo)
 columns=[];bounds=[];refs=[]
 for iq,ref in enumerate(failed['columns']):
  raw=P.read_pair(ref,tuple(ref['metadata']['schema']));contacts={n:(raw[n+'_hi'],raw[n+'_lo']) for n in ('registered_normal','literal_action','literal_minus_registered_normal_gap')};env=raw['coefficient_operation_envelope']
  assert all(x[0].shape==x[1].shape==(3784,4) for x in contacts.values()) and env.shape==(3784,4,2) and np.all(env>=0)
  rec=phase_normal_copy_completed('COLUMN',ref,raw);columns.append(contacts);bounds.append(env);refs.append(rec)
 assert len(P.RECORDS)==7 and len(P.CHECKS)==1
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
 loads=P.checkpoint('LOADS',data,dict(kind='new_phase_velocity_four_same_action_weak_normal_contact',columns=refs,normal_row_sign='Hamiltonian_contact equals minus action_contact',phase_and_ordinary_canonical_priors_unchanged=True,ordinary_contact_zero=True,baseline_normal_and_mean_comparison_refs=dict(normal=phase['normal_loads'],mean=phase['mean_loads']),prior_signed_primitive_readout=phase['prior_readout'],baseline_rows_added_or_subtracted=False,primitive_legendre_bridge_resolved=False,temporal_improvement_ports=None,physical_outer_GHY=None,physical_exterior=None,finite_charge_restored=False,controls=P.CHECKS[-1:]))
 assert len(P.CHECKS)==2 and all(c['passed'] for c in P.CHECKS) and len(P.RECORDS)==8
 return dict(recovered_failed_owner_proof=failed['terminal_proof_ref'],completed_fixture_and_four_point_columns_replayed=False,status='PHASE_VELOCITY_FOUR_NORMAL_LINEAR_CONTACT_COMPLETE',columns=refs,loads=loads,controls=P.CHECKS,checkpoints=P.RECORDS,phase_linear_response_admitted=True,normal_constraints_qualified=False,finite_phase_charge_restored=False,configuration_updated=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root and distinct FULL reviews required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA);P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_recovered_phase_velocity_normal_contact');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,failed=phase_normal_failed_admission()
  for n,h in pins.items():bind(n,h)
  case=phase_normal_packet(failed);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=2,pairs=8)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  arrays={n:np.asarray(a).copy() for n,a in arrays.items()}
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_new_phase_normal_contact_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
