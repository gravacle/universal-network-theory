from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_SAVED_TOTAL_METRIC_MOMENTUM_TRACE_SPLIT_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='7d7055ca0fd8e314498fe29adca6349f07990aaabcc74b702eb6f47d895c4814'
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
KERNEL='author_fragment_saved_metric_momentum_trace_split_v001.py'
KERNEL_SHA='173117bcb92b92510cf5c5954648d5ea62b0dfd3ff3891c88dff495a48cbd653'
PARENT='CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002'
PARENT_PINS={
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002.md':'0ccd71e96ff40c8105256fd9cce17b68ff06ad0292a726bd1ecac458d8bff30a',
 'CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002_RESULT.json':'7289a181e37a8f3277dfc7a587f09bf9078e1d20381eb0c0c371aac2511203be',
 'CROSS_U_PAIRED_CURRENT_PRIMITIVE_MOMENTUM_READOUT_V002_RECEIPT.json':'293295534b3c32ea152641ee4bd54b4cf224a171e3de9e14f2833759787eadaa',
 'READONLY_PAIRED_PRIMITIVE_CLOSURE_V002_RESULT.json':'5c3eba7c11f65c6c9449325f24683c8f3fde04a55dd684729d759431c7e771cf'}
P=None;np=None

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def initialize():
 global P,np
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('saved_Pi_pair_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 P.FLAGS=dict(canonical_bridge_resolved=False,finite_configuration_adopted=False,physical_TT_prepared=False,physical_exterior_qualified=False,joint_constraints_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
 bind(PROVIDER,PROVIDER_SHA);bind(KERNEL,KERNEL_SHA);bind(STEM+'.md',PROTOCOL_SHA);bind(__file__,P.sha(__file__))
 exec(compile((BASE/KERNEL).read_text(),str(BASE/KERNEL),'exec'),globals())

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def point_split_admission():
 for n,h in PARENT_PINS.items():bind(n,h)
 r=json.loads(P.path(PARENT+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT+'_RECEIPT.json').read_text());proof=json.loads(P.path('READONLY_PAIRED_PRIMITIVE_CLOSURE_V002_RESULT.json').read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==PARENT_PINS[PARENT+'_RESULT.json'] and rc['owner']==r['owner'] and r['owner']['pid']==50104 and r['owner']['source_sha256']==PARENT_PINS['cross_u_paired_current_primitive_momentum_readout_v002.py']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and len(r['controls'])==18 and all(c['passed'] and c['tolerance']==2e-11 for c in r['controls'])
 assert len(r['checkpoints'])==7 and r['case']['physical_adoption'] is False and r['case']['canonical_primitive_readout_admitted'] is False
 assert proof['status']=='SAVED_PAIRED_PRIMITIVE_CLOSURE_PASS' and proof['controls']==18 and proof['committed_pairs']==7 and proof['canonical_primitive_readout_admitted'] is False and proof['old_input_maps_or_feature_EFT_scatter_operator_solver_replayed'] is False
 assert proof['parent_terminal']['pid']==50104 and proof['parent_terminal']['result_sha256']==PARENT_PINS[PARENT+'_RESULT.json'] and proof['parent_terminal']['receipt_sha256']==PARENT_PINS[PARENT+'_RECEIPT.json']
 def selected(q):
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
  assert json.loads(P.path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')};return q
 columns=[selected(q) for q in r['case']['columns']];readout=selected(r['case']['readout']);assert len(columns)==4 and all(q in r['checkpoints'] for q in columns) and readout in r['checkpoints']
 for iq,q in enumerate(columns):
  assert q['metadata']['column']==iq and q['metadata']['source_configuration_changed'] is False
  for n,sh in (('momentum_metric_total_density_hi',[3784,6]),('momentum_metric_total_density_lo',[3784,6]),('chart_h',[3784,3,3]),('chart_ih',[3784,3,3]),('chart_sqrt_h',[3784])):assert q['metadata']['schema'][n]==dict(dtype='float64',finite=True,shape=sh)
 assert readout['metadata']['canonical_primitive_readout_admitted'] is False and readout['metadata']['physical_adoption'] is False
 return columns,readout,r

def point_split_packet(columns,readout,parent):
 prior_names=('metric_primitive_momentum_hi','metric_primitive_momentum_lo','metric_original_target','metric_primitive_minus_earned_bridge_hi','metric_primitive_minus_earned_bridge_lo','original_affine_and_actual_target_ratios','bridge_rhs_and_target_ratios')
 prior=P.read_pair(readout,prior_names)
 P.checkpoint('INPUT',prior,dict(kind='earned_literal_weak_Pm_and_unresolved_nominal_target_bridge',parent_owner=parent['owner'],readout_ref=thin(readout),column_refs=[thin(q) for q in columns],source_target='actual_saved_literal_point_metric_total_density',nominal_target_retained=True,canonical_primitive_readout_admitted=False,old_momentum_scatter_replayed=False))
 outputs=[]
 for iq,ref in enumerate(columns):
  P.RAW.clear();P.AVAILABLE.clear();P.CONTEXT.clear();P.CONTEXT.update(stage='new_saved_point_total_metric_trace_split',column=iq)
  raw=P.read_pair(ref,('momentum_metric_total_density_hi','momentum_metric_total_density_lo','chart_h','chart_ih','chart_sqrt_h'))
  for n,a in raw.items():P.capture('input_'+n,a)
  local=(raw['momentum_metric_total_density_hi'],raw['momentum_metric_total_density_lo']);h=raw['chart_h'];ih=raw['chart_ih'];mu=raw['chart_sqrt_h']
  off=np.ones((3,3),bool);np.fill_diagonal(off,False)
  assert np.all(h[:,off]==0) and np.all(ih[:,off]==0) and np.all(np.diagonal(h,axis1=1,axis2=2)>0) and np.all(np.diagonal(ih,axis1=1,axis2=2)>0)
  answer=york_point_split(local,h,ih,mu,P.capture,'column_%d'%iq)
  P.check('column_%d_total_metric_density_reconstruction'%iq,answer['reconstruction_gap'][0]+answer['reconstruction_gap'][1],np.zeros((3784,3,3)),answer['reconstruction_envelope'])
  P.check('column_%d_stored_inverse_trace_contact_identity'%iq,answer['trace_identity_gap'][0]+answer['trace_identity_gap'][1],np.zeros(3784),answer['trace_identity_envelope'])
  rec=P.checkpoint('COLUMN',{**P.AVAILABLE,**P.RAW},dict(kind='new_paired_saved_total_canonical_metric_trace_decomposition',column=iq,parent_column_ref=thin(ref),controls=P.CHECKS[-2:],source_point_momentum_changed=False,reference_geometry_changed=False,nominal_target_bridge_resolved=False,canonical_trace_is_bare_EH_K=False,continuum_TT_prepared=False,physical_exterior_admitted=False))
  outputs.append(rec)
 assert len(P.CHECKS)==8 and all(c['passed'] for c in P.CHECKS) and len(P.RECORDS)==5
 return dict(status='CONDITIONAL_CURRENT_POINT_METRIC_TRACE_SPLIT_COMPLETE',source_owner_pid=50104,point_count=15136,columns=outputs,controls=P.CHECKS,checkpoints=P.RECORDS,source_target='actual_saved_literal_point_metric_total_density',canonical_primitive_readout_admitted=False,nominal_target_bridge_resolved=False,continuum_TT_prepared=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False,'Root and distinct FULL reviews required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_new_saved_point_metric_trace_decomposition');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  columns,readout,parent=point_split_admission();case=point_split_packet(columns,readout,parent);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=8,pairs=5)),flush=True);return 0
 except BaseException:
  arrays={**P.RAW,**P.AVAILABLE};arrays.update(P.DD_ARRAY_CURRENT.get('arrays',{}))
  if arrays:P.checkpoint('ERROR_RAW',arrays,dict(kind='available_new_saved_point_trace_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
