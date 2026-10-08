from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_PHASE_FIXED_WEAK_CHARGE_LINEAR_RESPONSE_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='816e73375cfdcbba92d4f7d913b4c76c03b6902bc908512898612dda3e741edf'
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
KERNEL='author_fragment_phase_literal_charge_hessian_v002.py'
KERNEL_SHA='293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143'
CORE='author_fragment_phase_fixed_weak_charge_response_core_v001.py'
CORE_SHA='331fb805f572de4257f76e879ba28ceef5e20d4cb4898260e712c95efb553c2c'
ADMISSION_FRAGMENT='author_fragment_positive_phase_response_admission_v002.txt'
ADMISSION_SHA='07a12d2aa1a4098b640880c599cfa22cd0f24175637baec1730469b826c5de93'
FIXTURE_FRAGMENT='author_fragment_fresh_scalar_phase_response_fixture_v001.py'
FIXTURE_SHA='e9fe4c8399112fc53743f9cb4630e7c1d086a1c215878186a14bd88dfa43b9b9'
P=None;K=None;np=None

def bind(name,h):
 assert h is not None and P.sha(P.path(name))==h,name
 full=str(P.path(name).resolve());assert full not in P.INPUTS or P.INPUTS[full]==h;P.INPUTS[full]=h

def initialize():
 global P,K,np
 assert PROTOCOL_SHA is not None and FIXTURE_FRAGMENT is not None and FIXTURE_SHA is not None
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('phase_response_DD_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(finite_configuration_adopted=False,finite_phase_charge_restored=False,global_I0_profile_determined=False,joint_constraints_qualified=False,evolution_qualified=False,physical_exterior_qualified=False,galaxy_velocity_qualified=False)
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(CORE,CORE_SHA),(ADMISSION_FRAGMENT,ADMISSION_SHA),(FIXTURE_FRAGMENT,FIXTURE_SHA)):bind(n,h)
 spec=importlib.util.spec_from_file_location('phase_response_mass_kernel',BASE/KERNEL);K=importlib.util.module_from_spec(spec);spec.loader.exec_module(K);K.P=P;K.np=np
 globals().update(path=P.path,sha=P.sha,INPUTS=P.INPUTS)
 for n in (CORE,ADMISSION_FRAGMENT,FIXTURE_FRAGMENT):exec(compile((BASE/n).read_text(),str(BASE/n),'exec'),globals())

def scalar_action_bound(nodes,H,g):
 # Positive construction bound for the NEW fixed mass, before FE cancellations.
 field=P.scalar_lift(abs(nodes[0])+abs(nodes[1]));value=np.zeros((4,86,44))
 assert np.all(g['hats'][:,:,0]>=0) and np.all(g['dv']/g['R']>0)
 for iq in range(4):
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):value[iq]+=g['hats'][iq,corner,0]*field[di:86+di,dj:44+dj]
 return P.scalar_scatter((abs(H[0])+abs(H[1]))*value.reshape(15136),g)

def phase_response_packet(phase):
 geo=P.read_pair(phase['input'],('R','dv','hats','cell_i','cell_j','r','z'))
 names=tuple(n+'_'+w for n in ('literal_Hessian','new_phase_mass_diagonal','fixed_weak_phase_velocity_rhs','fixed_literal_weak_phase_charge') for w in ('hi','lo'))
 raw=P.read_pair(phase['loads'],names);pair=lambda n:(raw[n+'_hi'],raw[n+'_lo']);H=pair('literal_Hessian');diag=pair('new_phase_mass_diagonal');rhs=pair('fixed_weak_phase_velocity_rhs');prior=pair('fixed_literal_weak_phase_charge')
 assert geo['R'].shape==geo['dv'].shape==(4,3784) and geo['hats'].shape==(4,4,3,86,44) and H[0].shape==H[1].shape==(15136,)
 assert diag[0].shape==diag[1].shape==rhs[0].shape==rhs[1].shape==prior[0].shape==prior[1].shape==(87,45)
 assert np.all(H[0]>abs(H[1])) and np.all(diag[0][P.scalar_mask()]>abs(diag[1][P.scalar_mask()])) and np.count_nonzero(rhs[0])+np.count_nonzero(rhs[1])>0
 P.checkpoint('INPUT',{**geo,**raw},dict(kind='earned_positive_literal_phase_mass_and_original_compact_minus_Q_RHS',phase_refs=phase,scalar_free_dimension=3870,actual_budget=dict(cycles=1,cap=160),prior_current_literal_weak_charge_unchanged=True,old_H_or_basis_or_features_replayed=False))
 P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.clear();P.CONTEXT.update(stage='new_manufactured_scalar_solver_control')
 fixture=fresh_phase_response_control();P.checkpoint('FIXTURE',{**P.AVAILABLE,**P.RAW},dict(kind='independent_uniform_Q1_scalar_mass_solver_control',fixture=fixture,controls=P.CHECKS.copy(),physical_state_selected=False))
 P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.clear();P.CONTEXT.update(stage='new_compact_fixed_weak_phase_charge_response')
 label='actual_phase_response';answer=phase_response_solve(H,diag,rhs,geo,P.capture,label,cap=160,max_cycles=1)
 assert len(answer['history'])==1 and answer['history'][0]['cap']==160
 action=(P.AVAILABLE[label+'_cycle_001_final_original_action_hi'],P.AVAILABLE[label+'_cycle_001_final_original_action_lo']);res=answer['original_residual'];packed_rhs=phase_response_pack(rhs)
 configuration=(-packed_rhs[0],-packed_rhs[1]);combined=P.a_add(configuration,action);phase_response_keep('linearized_total_weak_charge_contact',combined,P.capture)
 gap=P.a_add(combined,res);phase_response_keep('linearized_charge_residual_identity_gap',gap,P.capture)
 bound=phase_response_pack(P.a_dd(scalar_action_bound(answer['nodal_pair'],H,geo)))[0]+abs(packed_rhs[0])+abs(packed_rhs[1])+abs(res[0])+abs(res[1]);P.capture('weak_charge_identity_upstream_bound',bound)
 P.check('new_phase_response_original_charge_balance_identity',gap[0]+gap[1],np.zeros(3870),bound)
 data={n:a for n,a in P.AVAILABLE.items() if n.startswith(label+'_') or n.startswith(('linearized_total_','linearized_charge_','weak_charge_identity_'))};data.update({n:a for n,a in P.RAW.items() if n.startswith('control_')})
 for name,pair_value in dict(phase_velocity_nodal=answer['nodal_pair'],original_residual=res,original_action=action,original_rhs=packed_rhs).items():
  for w,suffix in enumerate(('hi','lo')):data[name+'_'+suffix]=pair_value[w]
 data['original_raw_and_scaled_ratios']=answer['original_ratios'];data['original_positive_scale']=P.AVAILABLE[label+'_new_phase_positive_scale']
 solution=P.checkpoint('SOLUTION',data,dict(kind='paired_scalar_3870_linearized_fixed_weak_charge_response',history=answer['history'],original_rhs=phase['loads'],literal_prior=phase['loads'],response_admitted=answer['linearized_weak_charge_response_admitted'],actual_budget=dict(cycles=1,cap=160),finite_charge_restored=False,configuration_updated=False,physical_adoption=False,controls=P.CHECKS[-1:]))
 jetdata={n+'_'+w:pair_value[iw] for n,pair_value in answer['jet_pairs'].items() for iw,w in enumerate(('hi','lo'))}
 jets=P.checkpoint('RATE_JETS',jetdata,dict(kind='same_Q1_scalar_phase_velocity_increment_value_and_spatial_jets',solution=solution,response_admitted=answer['linearized_weak_charge_response_admitted'],baseline_phi_t_and_spatial_gradients_not_replaced=True,mixed_jet_rule='delta_partial_t_phi_i equals partial_i_delta_phi_t',instantaneous_phi_i_unchanged=True,finite_charge_restored=False))
 assert len(P.CHECKS)==2 and all(c['passed'] for c in P.CHECKS)
 return dict(status='LINEARIZED_FIXED_WEAK_PHASE_CHARGE_RESPONSE_ADMITTED' if answer['linearized_weak_charge_response_admitted'] else 'LINEARIZED_FIXED_WEAK_PHASE_CHARGE_RESPONSE_NONADMITTED',response_rows_admitted=answer['linearized_weak_charge_response_admitted'],original_raw_and_scaled_ratios=answer['original_ratios'].tolist(),actual_budget=dict(cycles=1,cap=160),history=answer['history'],solution=solution,rate_jets=jets,controls=P.CHECKS,checkpoints=P.RECORDS,finite_phase_charge_restored=False,configuration_updated=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root full review and release required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();bind(STEM+'.md',PROTOCOL_SHA)
 P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_scalar_phase_linearized_charge_response');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  pins,phase=phase_response_admission()
  for n,h in pins.items():bind(n,h)
  case=phase_response_packet(phase);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],ratios=case['original_raw_and_scaled_ratios'])),flush=True);return 0 if case['response_rows_admitted'] else 3
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_new_phase_scalar_response_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
