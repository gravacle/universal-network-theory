"""Guarded block-normalized warm correction of the refused original York rows."""
from pathlib import Path
import hashlib,importlib.util,json,os,sys,traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V002'
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
PROTOCOL_SHA='78e022ff4e932a3ba8aec731eea04b0154f79a95f1fcf7d0d25cac370f813cb3'
PARENT='CROSS_U_COMPACT_YORK_LONGITUDINAL_PROJECTION_V001'
PARENT_SOURCE='cross_u_compact_york_longitudinal_projection_v001.py'
PARENT_SOURCE_SHA='4b31ee0a5b0be690447c66ea8fd65ee00c7da83091e58f1090209e79dbf4a71d'
PARENT_PROTOCOL_SHA='5651cfdb3c6e9a47d1aa8f1a86e5c456bd0aed768012149868fff8ec413cee79'
TERMINAL=dict(pid=64681,result_sha256='5aa112f2f031fd5bc6ec2a58765ccac2926316eede516be3082dc94bfa7f2972',receipt_sha256='387382c097ceef6d671adedea054738b2a8bbb7aaabd9f76213063777bf143bf')
PROOF='READONLY_COMPACT_YORK_PROJECTION_CLOSURE_V001_RESULT.json'
PROOF_SHA='f88f612a6dea236ff77a2e4bd9571f634fac89608133356679443bf1d0d244c8'
KERNEL='author_fragment_york_block_normalized_correction_v001.py'
KERNEL_SHA='bdea5cfd994aa06d01440ecef3384b4e98a3e7c75ef05ed9dfcf82faa1e879d3'
Q=None;P=None;np=None

def keep(n,a):return Q.keep(n,np.asarray(a).copy())
def arrays():
 out={**P.RAW,**P.AVAILABLE};out.update(P.DD_ARRAY_CURRENT.get('arrays',{}));return {n:np.asarray(a).copy() for n,a in out.items()}
def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}
def initialize():
 global Q,P,np
 assert hashlib.sha256((BASE/PARENT_SOURCE).read_bytes()).hexdigest()==PARENT_SOURCE_SHA
 spec=importlib.util.spec_from_file_location('earned_york_projection_definitions',BASE/PARENT_SOURCE);Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q);Q.initialize()
 P=Q.P;np=Q.np;P.STEM=STEM;P.__file__=__file__;P.PROTOCOL_SHA=PROTOCOL_SHA
 for n,h in ((PARENT_SOURCE,PARENT_SOURCE_SHA),(PARENT+'.md',PARENT_PROTOCOL_SHA),(KERNEL,KERNEL_SHA),(STEM+'.md',PROTOCOL_SHA),(__file__,P.sha(__file__))):Q.bind(n,h)
 exec(compile((BASE/KERNEL).read_text(),str(BASE/KERNEL),'exec'),globals())

def warm_admission():
 for n,h in ((PARENT+'_RESULT.json',TERMINAL['result_sha256']),(PARENT+'_RECEIPT.json',TERMINAL['receipt_sha256']),(PROOF,PROOF_SHA)):Q.bind(n,h)
 r=json.loads(P.path(PARENT+'_RESULT.json').read_text());rc=json.loads(P.path(PARENT+'_RECEIPT.json').read_text());proof=json.loads(P.path(PROOF).read_text())
 assert rc['status']=='CLOSED' and rc['error_sha256'] is None and rc['result_sha256']==TERMINAL['result_sha256'] and rc['owner']==r['owner'] and r['owner']['pid']==TERMINAL['pid'] and r['owner']['source_sha256']==PARENT_SOURCE_SHA
 assert r['status']=='ORIGINAL_YORK_ROWS_NOT_ADMITTED' and r['original_rows_admitted'] is False and r['compact_weak_TT_original_rows_admitted'] is False and r['projection'] is None and r['vector_space_dimension']==11135
 assert r['qualification']==rc['qualification'] and all(v is False for v in r['qualification'].values()) and all(r[n] is False for n in ('original_primitive_bridge_resolved','continuum_TT_prepared','physical_exterior_adopted','physical_adoption'))
 assert len(r['controls'])==len(r['cycles'])==3 and len(r['checkpoints'])==18 and [c['ordinal'] for c in r['controls']]==[0,1,2] and all(c['passed'] and c['tolerance']==2e-11 for c in r['controls'])
 assert proof['status']=='SAVED_COMPACT_YORK_PROJECTION_CLOSURE_PASS' and proof['owner_pid']==65789 and proof['parent']==dict(TERMINAL,error_sha256=None) and proof['controls']==3 and proof['committed_pairs']==18 and proof['producer_status']==r['status'] and proof['original_rows_admitted'] is False and proof['compact_weak_TT_original_rows_admitted'] is False
 assert proof['York_geometry_action_scatter_solver_or_fixture_replayed'] is False and proof['physical_adoption'] is False and proof['original_row_tolerance']==1e-10 and proof['arithmetic_identity_tolerance']==2e-11
 for q in [r['input'],r['solution']]+r['cycles']:
  assert q in r['checkpoints'] and q['metadata']['owner']==r['owner'] and q['metadata']['qualification']==r['qualification'] and q['metadata']['failed'] is False
  for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h;Q.bind(n,h)
  assert json.loads(P.path(q['commit_file']).read_text())=={n:q[n] for n in ('file','sha256','metadata')}
 assert r['input']['metadata']['kind']=='exact_earned_york_maps_source_diagonal_and_prior_bridge' and r['solution']['metadata']['kind']=='bounded_auxiliary_york_original_row_result' and r['solution']['metadata']['original_rows_admitted'] is False and r['solution']['metadata']['max_cycles']==3 and r['solution']['metadata']['cap']==160
 for i,q in enumerate(r['cycles'],1):assert q['metadata']['cycle']==i and q['metadata']['cap']==160 and q['metadata']['controls']==r['controls'][i-1:i]
 return r,proof

def load_warm(r):
 names=('R','dv','hats','r','z','cell_i','cell_j','PiTF_hi','PiTF_lo','h','ih','sqrt_h','compact_vector_mask','L_maps_hi','L_maps_lo','L_map_operation_envelope','rhs_hi','rhs_lo','rhs_operation_envelope','diagonal_hi','diagonal_lo','diagonal_operation_envelope','positive_Jacobi_congruence_scale','diagonal_positivity_margin','prior_metric_primitive_momentum_hi','prior_metric_primitive_momentum_lo','prior_metric_original_target','prior_metric_primitive_minus_earned_bridge_hi','prior_metric_primitive_minus_earned_bridge_lo','prior_original_affine_and_actual_target_ratios','prior_bridge_rhs_and_target_ratios')
 a=P.read_pair(r['input'],names)
 for n,v in a.items():keep(n,v)
 mask=Q.york_vector_mask();assert np.array_equal(a['compact_vector_mask'],mask) and np.all(a['diagonal_positivity_margin'][mask]>0)
 d=dict(maps=(a['L_maps_hi'],a['L_maps_lo']),map_envelope=a['L_map_operation_envelope'],ih=a['ih'],sqrt_h=a['sqrt_h'],PiTF=(a['PiTF_hi'],a['PiTF_lo']),geometry={n:a[n] for n in ('R','dv','hats','r','z','cell_i','cell_j')},rhs=(a['rhs_hi'][mask],a['rhs_lo'][mask]),rhs_envelope=a['rhs_operation_envelope'][mask],scale=a['positive_Jacobi_congruence_scale'][mask])
 s=P.read_pair(r['solution'],tuple(n+'_'+w for n in ('final_potential_nodes','original_rhs','final_original_action','final_original_residual') for w in ('hi','lo'))+('final_original_raw_scaled_ratios','final_original_global_ratios','original_positive_scale'))
 for n,v in s.items():keep('parent_solution_'+n,v)
 nodes=(s['final_potential_nodes_hi'],s['final_potential_nodes_lo']);action=(s['final_original_action_hi'],s['final_original_action_lo']);residual=(s['final_original_residual_hi'],s['final_original_residual_lo'])
 assert nodes[0].shape==nodes[1].shape==(11135,) and np.array_equal(s['original_positive_scale'],d['scale']) and all(np.array_equal(s['original_rhs_'+w],d['rhs'][i]) for i,w in enumerate(('hi','lo')))
 assert np.array_equal(s['final_original_raw_scaled_ratios'],np.asarray(r['solution']['metadata']['original_ratios'])) and not np.all(s['final_original_raw_scaled_ratios']<=1e-10)
 current=dict(action=action,residual=residual,ratios=s['final_original_raw_scaled_ratios'],global_ratios=s['final_original_global_ratios'],admitted=False)
 for c,q in zip(r['controls'],r['cycles']):
  prefix='control_%03d_%s_'%(c['ordinal'],c['name']);raw=P.read_pair(q,tuple(prefix+n for n in ('actual','expected','envelope')))
  for n,v in raw.items():P.RAW[n]=v.copy()
 P.CHECKS.extend(r['controls']);scope=york_support_measurement(d);d['sufficient_component_targets']=york_block_sufficient_targets(d['rhs'][0]+d['rhs'][1],d['scale'])
 record=P.checkpoint('INPUT',arrays(),dict(kind='exact_refused_final_York_iterate_and_measured_independent_block_support',parent_input=thin(r['input']),parent_solution=thin(r['solution']),parent_cycles=[thin(q) for q in r['cycles']],preserved_parent_checkpoints=r['checkpoints'],preserved_parent_controls=r['controls'],old_final_seed_bitcopied=True,old_zero_start_and_480_iterations_replayed=False,old_geometry_source_or_fixture_replayed=False,old_original_rows_admitted=False,max_groups=2,cap_per_group=160,original_row_tolerance=1e-10,**scope))
 d['input_ref']=record;P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();return nodes,current,d,record

def warm_packet(parent,proof):
 nodes,current,d,inp=load_warm(parent);fixture_meta=york_fresh_block_control();fixture=P.checkpoint('FIXTURE',arrays(),dict(fixture_meta,controls=P.CHECKS[3:]))
 P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();nodes,current,blocks=york_measure_block_corrections(nodes,current,d)
 Q.york_pair_keep('final_potential_nodes',nodes,keep);Q.york_pair_keep('original_rhs',d['rhs'],keep);Q.york_pair_keep('final_original_action',current['action'],keep);Q.york_pair_keep('final_original_residual',current['residual'],keep);keep('final_original_raw_scaled_ratios',current['ratios']);keep('final_original_global_ratios',current['global_ratios']);keep('original_positive_scale',d['scale'])
 solution=P.checkpoint('SOLUTION',arrays(),dict(kind='block_normalized_warm_auxiliary_York_original_row_result',inputs=thin(inp),fixture=thin(fixture),blocks=[thin(q) for q in blocks],original_rows_admitted=current['admitted'],original_component_ratios=current['ratios'].tolist(),original_global_ratios=current['global_ratios'].tolist(),controls=P.CHECKS,max_groups=2,cap_per_group=160,physical_TT_prepared=False,potential_error_bound_claimed=False))
 projection=None;projection_admitted=False
 if current['admitted']:
  P.RAW.clear();P.AVAILABLE.clear();P.DD_ARRAY_CURRENT.clear();scope=Q.york_point_projection(nodes,current,d);projection_admitted=scope['compact_weak_TT_original_rows_admitted']
  projection=P.checkpoint('PROJECTION',arrays(),dict(kind='admitted_auxiliary_compact_weak_longitudinal_projection_and_TT_remainder',solution=thin(solution),input_ref=thin(inp),original_raw_scaled_ratios=current['ratios'].tolist(),**scope))
 status='AUXILIARY_COMPACT_YORK_LONGITUDINAL_PROJECTION_ADMITTED' if projection_admitted else ('COMPACT_TT_REMAINDER_READOUT_NOT_ADMITTED' if current['admitted'] else 'ORIGINAL_YORK_ROWS_NOT_ADMITTED')
 return dict(status=status,owner_pid=P.OWNER['pid'],input=inp,fixture=fixture,blocks=blocks,solution=solution,projection=projection,checkpoints=P.RECORDS,controls=P.CHECKS,preserved_parent_controls=parent['controls'],preserved_parent_checkpoints=parent['checkpoints'],parent_terminal=TERMINAL,parent_original_rows_admitted=False,original_rows_admitted=current['admitted'],compact_weak_TT_original_rows_admitted=projection_admitted,vector_space_dimension=11135,original_primitive_bridge_resolved=False,continuum_TT_prepared=False,physical_exterior_adopted=False,physical_adoption=False)

def outputs_recheck():
 assert P.sha(__file__)==P.OWNER['source_sha256']
 for n,h in P.OUTPUTS.items():assert P.sha(P.path(n))==h,n
def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and all(v is not None for v in TERMINAL.values()) and PROOF_SHA is not None,'Held mathematical reviews and actual refused parent closure required'
 assert not list(BASE.glob(STEM+'_*')),'Fresh exclusive namespace required'
 initialize();P.OWNER=dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=P.sha(__file__),started_utc=P.now(),execution='root_owned_block_normalized_warm_auxiliary_York_correction');P.json_file(STEM+'_OWNER_START.json',P.OWNER)
 try:
  parent,proof=warm_admission();case=warm_packet(parent,proof);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(case,owner=P.OWNER,qualification=P.FLAGS));outputs_recheck();P.json_file(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),result_sha256=rh,error_sha256=None,closed_utc=P.now(),qualification=P.FLAGS));outputs_recheck();print(json.dumps(dict(status=case['status'],controls=len(P.CHECKS),pairs=len(P.RECORDS))),flush=True);return 0 if case['compact_weak_TT_original_rows_admitted'] else 3
 except BaseException:
  current=arrays()
  if current:P.checkpoint('ERROR_RAW',current,dict(kind='available_new_block_York_operands',context=P.CONTEXT),failed=True)
  P.seal_actual();eh=P.json_file(STEM+'_ERROR.json',dict(status='FAILED',owner=P.OWNER,input_sha256=P.INPUTS,controls=P.CHECKS,checkpoints=P.RECORDS,context=P.CONTEXT,qualification=P.FLAGS,traceback=traceback.format_exc()));prior=BASE/(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(status='CLOSED_ERROR',owner=P.OWNER,input_sha256=P.INPUTS,output_sha256=P.OUTPUTS.copy(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,closed_utc=P.now(),qualification=P.FLAGS));raise
if __name__=='__main__':sys.exit(main())
