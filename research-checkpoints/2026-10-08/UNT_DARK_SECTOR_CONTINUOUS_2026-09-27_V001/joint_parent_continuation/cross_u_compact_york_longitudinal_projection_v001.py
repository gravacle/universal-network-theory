"""Guarded bounded compact York W projection from earned maps and source."""
from pathlib import Path
import importlib.util,hashlib,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V001'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='5651cfdb3c6e9a47d1aa8f1a86e5c456bd0aed768012149868fff8ec413cee79'
PROVIDER='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PROVIDER_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
GEOMETRY_KERNEL='author_fragment_compact_york_longitudinal_geometry_v002.py'
GEOMETRY_KERNEL_SHA='a653fc7978d4246824e0970d3ab989f6f557c16ee395fff58e01f48b84042446'
SOLVER_KERNEL='author_fragment_compact_york_projection_solver_v001.py'
SOLVER_KERNEL_SHA='9053721ab0194ae58bdb7909b6a495e86b566da8f0469727943c81396cc98617'
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PREPARATION_V001'
PARENT_PINS={
 'cross_u_compact_york_longitudinal_preparation_v001.py':'5e5f8b472aa3294c50a89dd46ac5b38165116b2f0df6f104b0c2672d61b7d508',
 'CROSS_U_COMPACT_YORK_LONGITUDINAL_PREPARATION_V001.md':'15e7941d886096bdf6fcb7b50c087fe24990e2625ec79e0e2242b0adbc934d86',
 'CROSS_U_COMPACT_YORK_LONGITUDINAL_PREPARATION_V001_RESULT.json':'10a59cc1c6e8c838a5e3ea9042d57a6735accc55bb4e8aee5076fb01b6c1e00f',
 'CROSS_U_COMPACT_YORK_LONGITUDINAL_PREPARATION_V001_RECEIPT.json':'8cf681823315f5424f6bc6da778e43db83564c73d91a2ca7091407f16b91262f'}
PROOF='READONLY_COMPACT_YORK_PREPARATION_CLOSURE_V001_RESULT.json';PROOF_SHA='8304113b5af710c15f155a15e9be9bdec8f800dd497836241ea0844df0439ffa'
MAX_CYCLES=3;CAP=160;LINEAR_TOL=1e-10
P=None;np=None;ORIGINAL_CAPTURE=None

def bind(n,h):
 assert n is not None and h is not None and P.sha(P.path(n))==h,n
 key=str(P.path(n).resolve());assert key not in P.INPUTS or P.INPUTS[key]==h;P.INPUTS[key]=h

def keep(n,a):return ORIGINAL_CAPTURE(n,np.asarray(a).copy())

def arrays():
 out={**P.RAW,**P.AVAILABLE};out.update(P.DD_ARRAY_CURRENT.get('arrays',{}));return {n:np.asarray(a).copy() for n,a in out.items()}

def initialize():
 global P,np,ORIGINAL_CAPTURE
 assert hashlib.sha256((BASE/PROVIDER).read_bytes()).hexdigest()==PROVIDER_SHA
 spec=importlib.util.spec_from_file_location('compact_york_solver_provider',BASE/PROVIDER);P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
 import numpy as numpy_module
 np=numpy_module;P.np=np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA;ORIGINAL_CAPTURE=P.capture;P.capture=keep
 P.FLAGS=dict(original_primitive_bridge_resolved=False,physical_TT_prepared=False,physical_exterior_qualified=False,canonical_configuration_prepared=False,joint_constraints_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
 for n,h in ((PROVIDER,PROVIDER_SHA),(GEOMETRY_KERNEL,GEOMETRY_KERNEL_SHA),(SOLVER_KERNEL,SOLVER_KERNEL_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):bind(n,h)
 exec(compile((BASE/GEOMETRY_KERNEL).read_text(),str(BASE/GEOMETRY_KERNEL),'exec'),globals())
 exec(compile((BASE/SOLVER_KERNEL).read_text(),str(BASE/SOLVER_KERNEL),'exec'),globals())

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def projection_admission():
 for n,h in PARENT_PINS.items():bind(n,h)
 bind(PROOF,PROOF_SHA)
 r=json.loads(P.path(PARENT+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT+'_RECEIPT.json').read_text());proof=json.loads(P.path(PROOF).read_text())
 assert rc['status']=='CLOSED' and rc.get('error_sha256') is None and rc['result_sha256']==PARENT_PINS[PARENT+'_RESULT.json'] and rc['owner']==r['owner'] and r['owner']['pid']==63568 and r['owner']['source_sha256']==PARENT_PINS['cross_u_compact_york_longitudinal_preparation_v001.py']
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and r['physical_adoption'] is False and r['W_solved'] is False and r['canonical_primitive_bridge_resolved'] is False
 assert r['vector_space_dimension']==11135 and len(r['controls'])==6 and all(q['passed'] and q['tolerance']==2e-11 and q['ordinal']==i for i,q in enumerate(r['controls'])) and len(r['checkpoints'])==4
 # Final proof schema is bound after its actual root-owned saved-only closure.
 assert proof['status']=='SAVED_COMPACT_YORK_PREPARATION_CLOSURE_PASS' and proof['owner_pid']==64015 and proof['controls']==6 and proof['committed_pairs']==4 and proof['old_geometry_operator_FE_momentum_or_fixture_replayed'] is False and proof['W_solved'] is False and proof['global_spectral_coercivity_certified'] is False
 assert proof['parent']==dict(pid=63568,result_sha256=PARENT_PINS[PARENT+'_RESULT.json'],receipt_sha256=PARENT_PINS[PARENT+'_RECEIPT.json']) and proof['physical_adoption'] is False
 refs={}
 for role in ('input','geometry','loads'):
  q=r[role];assert q in r['checkpoints']
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;bind(n,h)
  assert json.loads(P.path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')} and q['metadata']['failed'] is False and q['metadata']['owner']==r['owner']
  refs[role]=q
 return refs,r

def load_projection(refs,parent):
 names=('R','dv','hats','r','z','cell_i','cell_j','PiTF_hi','PiTF_lo','h','ih','sqrt_h','compact_vector_mask','prior_metric_primitive_momentum_hi','prior_metric_primitive_momentum_lo','prior_metric_original_target','prior_metric_primitive_minus_earned_bridge_hi','prior_metric_primitive_minus_earned_bridge_lo','prior_original_affine_and_actual_target_ratios','prior_bridge_rhs_and_target_ratios')
 inp=P.read_pair(refs['input'],names)
 for n,a in inp.items():keep(n,a)
 geom={n:inp[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')};assert np.array_equal(inp['compact_vector_mask'],york_vector_mask())
 matrix=P.read_pair(refs['geometry'],('L_maps_hi','L_maps_lo','L_map_operation_envelope'))
 for n,a in matrix.items():keep(n,a)
 loads=P.read_pair(refs['loads'],('rhs_hi','rhs_lo','rhs_operation_envelope','diagonal_hi','diagonal_lo','diagonal_operation_envelope','positive_Jacobi_congruence_scale','diagonal_positivity_margin'))
 for n,a in loads.items():keep(n,a)
 mask=york_vector_mask();assert np.all(loads['diagonal_positivity_margin'][mask]>0)
 d=dict(maps=(matrix['L_maps_hi'],matrix['L_maps_lo']),map_envelope=matrix['L_map_operation_envelope'],ih=inp['ih'],sqrt_h=inp['sqrt_h'],PiTF=(inp['PiTF_hi'],inp['PiTF_lo']),geometry=geom,rhs=(york_pack(loads['rhs_hi']),york_pack(loads['rhs_lo'])),rhs_envelope=york_pack(loads['rhs_operation_envelope']),scale=york_pack(loads['positive_Jacobi_congruence_scale']))
 assert d['maps'][0].shape==d['maps'][1].shape==d['map_envelope'].shape==(15136,3,3,3,3) and np.all(d['scale']>0) and d['rhs'][0].shape==d['rhs'][1].shape==(11135,)
 rec=P.checkpoint('INPUT',arrays(),dict(kind='exact_earned_york_maps_source_diagonal_and_prior_bridge',source_refs={k:thin(q) for k,q in refs.items()},preparation_controls=parent['controls'],new_operator_coefficients_reconstructed=False,old_fixtures_or_source_replayed=False,canonical_primitive_bridge_resolved=False,max_cycles=MAX_CYCLES,cap=CAP,original_row_tolerance=LINEAR_TOL))
 d['input_ref']=rec;P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();return d,rec

def projection_packet(refs,parent):
 d,input_ref=load_projection(refs,parent);nodes,answer,initial,cycles=york_measure_and_solve(d,MAX_CYCLES,CAP)
 york_pair_keep('final_potential_nodes',nodes,keep);york_pair_keep('original_rhs',d['rhs'],keep);york_pair_keep('final_original_action',answer['action'],keep);york_pair_keep('final_original_residual',answer['residual'],keep);keep('final_original_raw_scaled_ratios',answer['ratios']);keep('final_original_global_ratios',answer['global_ratios']);keep('original_positive_scale',d['scale'])
 solution=P.checkpoint('SOLUTION',arrays(),dict(kind='bounded_auxiliary_york_original_row_result',inputs=thin(input_ref),cycles=[thin(q) for q in cycles],original_rows_admitted=answer['admitted'],original_ratios=answer['ratios'].tolist(),original_global_ratios=answer['global_ratios'].tolist(),max_cycles=MAX_CYCLES,cap=CAP,controls=P.CHECKS,physical_TT_prepared=False,potential_error_bound_claimed=False))
 projection=None;projection_admitted=False
 if answer['admitted']:
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();scope=york_point_projection(nodes,answer,d)
  projection_admitted=scope['compact_weak_TT_original_rows_admitted']
  projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(solution),input_ref=thin(input_ref),original_raw_scaled_ratios=answer['ratios'].tolist(),**scope))
 return dict(status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if answer['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED'),owner_pid=P.OWNER['pid'],controls=P.CHECKS,checkpoints=P.RECORDS,input=input_ref,initial_original_ratios=initial['ratios'].tolist(),cycles=cycles,solution=solution,projection=projection,original_rows_admitted=answer['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROOF is not None and PROOF_SHA is not None,'Full reviews and actual saved-proof closure required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_bounded_auxiliary_compact_York_projection');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  refs,parent=projection_admission();case=projection_packet(refs,parent);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  current=arrays()
  if current:P.checkpoint('ERROR_RAW',current,dict(kind='available_new_York_projection_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise

if __name__=='__main__':sys.exit(main())
