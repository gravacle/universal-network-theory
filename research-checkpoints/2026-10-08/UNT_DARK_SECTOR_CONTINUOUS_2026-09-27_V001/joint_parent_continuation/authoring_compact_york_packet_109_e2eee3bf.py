"""Guarded NEW compact York geometry, source and diagonal; no W solve."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PREPARATION_V001'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
PROTOCOL_SHA=None
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
KERNEL='author_fragment_compact_york_longitudinal_geometry_v001.py'
KERNEL_SHA=None
ADMISSION='author_fragment_compact_york_preparation_admission_v001.txt'
ADMISSION_SHA=None
P=None;np=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def keep(n,a):return P.capture(n,np.asarray(a).copy())

def initialize():
 global P,np
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('compact_york_pair_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(original_primitive_bridge_resolved=False,physical_TT_prepared=False,physical_exterior_qualified=False,canonical_configuration_prepared=False,joint_constraints_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
 for n,h in ((PROVIDER,PROVIDER_SHA),(KERNEL,KERNEL_SHA),(ADMISSION,ADMISSION_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 exec(compile((BASE/KERNEL).read_text(),str(BASE/KERNEL),'exec'),globals())
 exec(compile((BASE/ADMISSION).read_text(),str(BASE/ADMISSION),'exec'),globals())

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def scratch(stage):
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();P.CONTEXT.clear();P.CONTEXT.update(stage=stage)

def load_york_inputs(admitted):
 scratch('copy_earned_point_PiTF_and_saved_spatial_metric_jets')
 geometry=P.read_pair(admitted['geometry'],('R','dv','hats','cell_i','cell_j','r','z'))
 for n,a in geometry.items():keep(n,a)
 assert geometry['R'].shape==geometry['dv'].shape==(4,3784) and geometry['hats'].shape==(4,4,3,86,44)
 assert geometry['cell_i'].dtype==geometry['cell_j'].dtype==np.dtype('int64') and geometry['r'].shape==(87,) and geometry['z'].shape==(45,)
 assert np.all(geometry['R']>0) and np.all(geometry['dv']>0)
 prior_names=('metric_primitive_momentum_hi','metric_primitive_momentum_lo','metric_original_target','metric_primitive_minus_earned_bridge_hi','metric_primitive_minus_earned_bridge_lo','original_affine_and_actual_target_ratios','bridge_rhs_and_target_ratios')
 prior=P.read_pair(admitted['trace_input'],prior_names)
 for n,a in prior.items():keep('prior_'+n,a)
 fields={n:[] for n in ('PiTF_hi','PiTF_lo','h','ih','sqrt_h','dh_hi','dh_lo')}
 for iq,(ref,primitive) in enumerate(zip(admitted['trace_columns'],admitted['primitive_columns'])):
  names=('column_%d_trace_subtracted_canonical_density_hi'%iq,'column_%d_trace_subtracted_canonical_density_lo'%iq,'input_chart_h','input_chart_ih','input_chart_sqrt_h')
  point=P.read_pair(ref,names);jets=P.read_pair(primitive,('first_jet_dg_hi','first_jet_dg_lo'))
  for n,a in point.items():keep('copied_%d_'%iq+n,a)
  for n,a in jets.items():keep('copied_%d_'%iq+n,a)
  for n,key in (('PiTF_hi',names[0]),('PiTF_lo',names[1]),('h','input_chart_h'),('ih','input_chart_ih'),('sqrt_h','input_chart_sqrt_h')):fields[n].append(point[key])
  for word in ('hi','lo'):
   assert jets['first_jet_dg_'+word].shape==(3784,4,4,4)
   fields['dh_'+word].append(jets['first_jet_dg_'+word][:,1:,1:,1:])
 out={n:np.concatenate(a,axis=0) for n,a in fields.items()}
 for n,a in out.items():keep(n,a)
 assert out['h'].shape==out['ih'].shape==(15136,3,3) and out['dh_hi'].shape==out['dh_lo'].shape==(15136,3,3,3)
 off=np.ones((3,3),bool);np.fill_diagonal(off,False)
 assert np.all(out['h'][:,off]==0) and np.all(out['ih'][:,off]==0) and np.all(np.diagonal(out['h'],axis1=1,axis2=2)>0) and np.all(np.diagonal(out['ih'],axis1=1,axis2=2)>0) and np.all(out['sqrt_h']>0)
 mask=york_vector_mask();keep('compact_vector_mask',mask)
 rec=P.checkpoint('INPUT',{**P.AVAILABLE,**P.RAW},dict(kind='exact_earned_PiTF_geometry_and_spatial_metric_jets',trace_column_refs=[thin(q) for q in admitted['trace_columns']],primitive_spatial_jet_refs=[thin(q) for q in admitted['primitive_columns']],geometry_ref=thin(admitted['geometry']),trace_input_ref=thin(admitted['trace_input']),canonical_primitive_bridge_resolved=False,old_momentum_or_geometry_reconstructed=False,auxiliary_boundary='W_zero_at_outer_R_and_top_Z_with_sheet_parity',physical_exterior_boundary_adopted=False))
 return out,geometry,rec

def york_packet(admitted):
 inputs,g,input_ref=load_york_inputs(admitted)
 scratch('new_independent_local_york_controls');fixture=york_fresh_controls(keep)
 fixture_ref=P.checkpoint('FIXTURE',{**P.AVAILABLE,**P.RAW},dict(fixture,controls=P.CHECKS.copy(),old_fixtures_replayed=False))
 h=inputs['h'];ih=inputs['ih'];mu=inputs['sqrt_h'];dh=(inputs['dh_hi'],inputs['dh_lo']);pi_tf=(inputs['PiTF_hi'],inputs['PiTF_lo'])
 scratch('new_actual_york_geometry_maps')
 maps,emap=york_geometry_maps(h,ih,dh,keep,'actual_york');keep('L_maps_hi',maps[0]);keep('L_maps_lo',maps[1]);keep('L_map_operation_envelope',emap)
 actual,predicted,trace_bound=york_inverse_trace_contacts(h,ih,dh,maps,emap,keep,'actual_york')
 P.check('serialized_inverse_L_map_trace_contact_identity',actual[0]+actual[1],predicted[0]+predicted[1],trace_bound)
 R=g['R'].reshape(15136);A=h[:,0,0]
 keep('conformal_component_contact',np.stack((h[:,1,1]-A,h[:,2,2]-A*R**2),axis=-1));keep('spatial_phi_metric_jet_contact_hi',dh[0][:,2]);keep('spatial_phi_metric_jet_contact_lo',dh[1][:,2])
 geometry_ref=P.checkpoint('GEOMETRY',{**P.AVAILABLE,**P.RAW},dict(kind='new_paired_coordinate_Lie_divergence_maps',inputs_ref=thin(input_ref),vector_space_dimension=11135,serialized_inverse_trace_contact_retained=True,continuum_conformal_Killing_identity_not_imposed=True,global_coercivity_not_inferred_from_diagonal=True,controls=P.CHECKS[-1:]))
 scratch('new_york_source_diagonal_and_original_functionals')
 rhs=york_weak_source(pi_tf,maps,g,keep,'actual_york');keep('rhs_hi',rhs[0]);keep('rhs_lo',rhs[1])
 erhs=york_source_envelope(pi_tf,emap,g,keep,'actual_york');keep('rhs_operation_envelope',erhs)
 diagonal,ediagonal=york_local_diagonal(maps,emap,ih,mu,g,keep,'actual_york');keep('diagonal_hi',diagonal[0]);keep('diagonal_lo',diagonal[1]);keep('diagonal_operation_envelope',ediagonal)
 mask=york_vector_mask();lower=diagonal[0]-abs(diagonal[1]);margin=lower-P.TOL*ediagonal;keep('diagonal_resolved_lower',lower);keep('diagonal_positivity_margin',margin)
 P.check('compact_york_resolved_positive_local_diagonal',np.asarray(margin[mask]<=0,dtype=float),np.zeros(11135),np.ones(11135))
 scale=np.ones((3,87,45));scale[mask]=np.sqrt(diagonal[0][mask]+diagonal[1][mask]);keep('positive_Jacobi_congruence_scale',scale)
 trial=np.zeros((3,87,45));trial[0]=1./8.;trial[1]=(np.indices((87,45)).sum(axis=0)%3-1)/16.;trial[2]=-1./16.;trial[~mask]=0
 x=P.a_dd(trial);keep('test_nodal_coefficients_hi',x[0]);keep('test_nodal_coefficients_lo',x[1])
 functional=york_functional_controls(x,rhs,erhs,maps,emap,pi_tf,ih,mu,g,keep,'actual_york_functional')
 loads_ref=P.checkpoint('LOADS',{**P.AVAILABLE,**P.RAW},dict(kind='new_compact_York_rhs_exact_axis_diagonal_and_original_functionals',geometry_ref=thin(geometry_ref),input_ref=thin(input_ref),diagonal_is_preconditioner_only=True,global_operator_spectral_coercivity_certified=False,controls=P.CHECKS[3:],**functional))
 assert len(P.CHECKS)==6 and all(q['passed'] for q in P.CHECKS) and len(P.RECORDS)==4
 return dict(status='CONDITIONAL_COMPACT_YORK_GEOMETRY_SOURCE_AND_DIAGONAL_PREPARED',controls=P.CHECKS,checkpoints=P.RECORDS,input=input_ref,fixture=fixture_ref,geometry=geometry_ref,loads=loads_ref,point_count=15136,vector_space_dimension=11135,total_point_prior='actual_literal_50104_metric_total_density_trace_split_60485',canonical_primitive_bridge_resolved=False,W_solved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False,'Root and distinct FULL review required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_compact_York_geometry_source_diagonal');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  admitted=york_preparation_admission();case=york_packet(admitted);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=6,pairs=4)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_new_york_geometry_source_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
