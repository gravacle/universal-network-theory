"""HELD saved-word certification of NEW total-rate native/metric currents.
Original anchor targets, references, masks, scales and six 1e-10 gates remain.
No action, EOS, normal/CMC, scatter, solver or producer body is selected.
Root alone binds a naturally closed finite evaluation and releases a successor.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CLOSED_FIXED_GEOMETRY_TOTAL_RATE_ORIGINAL_SIX_V002'
DRIVER_PROTOCOL='CLOSED_FIXED_GEOMETRY_TOTAL_RATE_ORIGINAL_SIX_V001.md'
PROTOCOL_SHA='7ff422ce9340b9605446366000633d9041920b8d171bb43e020c7e988b2b07e6'
FINITE_SOURCE=(None,None)
FINITE_RESULT=(None,None,None)
FINITE_RECEIPT=(None,None,None)
FINITE_CLOSURE_PROOF=(None,None,None)
FINITE_STATUS='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'
ANCHOR_SOURCE=('cross_u_candidate_reference_york_anchor_canonical_packet_v004.py','184d850aee263a6d4957c7df632c7bd928d6804d9c43978489c5b6abda02b5d7')
ANCHOR_RESULT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RESULT.json','94220e4f2c37e16239a261143ef498b9d935ed234a91d9c95b3119fce75d3352','REFERENCE_YORK_ANCHOR_TARGET_AND_CANONICAL_EPSILON_MEASURED')
ANCHOR_RECEIPT=('CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V004_RECEIPT.json','2aa42aef8e9a8a45f7f902f223092640f461703dac71b8bf103918f4425abeee','CLOSED')
ANCHOR_PROOF=('ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_V001.json','1b43fc07b4c51c64b1798575f1f1aec48005761bf744f6d981d37b52071d2e4a','ROOT_NATURAL_CLOSED_REFERENCE_YORK_ANCHOR_CANONICAL_SUCCESS_SEALS_VERIFIED')
UPDATED_PHASE_CLOSURE=(('cross_u_candidate_finite_phase_state_evaluation_v002.py','0fe81190f0968ce599a001e5c65459abc176da4f5c38684072cbc70c1a2ff54b'),('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_RESULT.json','4ac3ff59a1fb825151f603cb1422771cf8648c6e9b09062e7dba849cb28635ec','CANDIDATE_FINITE_PHASE_STATE_AND_LITERAL_CURRENT_MEASURED'),('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_RECEIPT.json','8e707d334fc62f1f9b585460aecb1bda3385f21515ea3a142b56acc3c8289278','CLOSED'),('ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_V001.json','f97d469bf7852bdd72b2abbc093669070b4081d24feb00c1373fce6279600ebc','ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_VERIFIED'))
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_initial_york_trace_target_response_v001.py':'71fda02b76e03c5ac4fe917f0514a3f13e60ec15b9aad21610045fbe40fe71e1',
 'cross_u_candidate_reference_york_anchor_canonical_packet_v004.py':ANCHOR_SOURCE[1],
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d'}
FLAGS=dict(physical_adoption=False,normal_constraints_qualified=False,initial_CMC_solved=False,CMC_preservation_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};FIXED_RATE_SOURCE_PINS=None

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)

def initialize():
 global np,P,SCOPE,FIXED_RATE_SOURCE_PINS
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 wanted={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'}
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 definitions(list(PINS)[1],wanted,SCOPE);P=types.SimpleNamespace(**{n:SCOPE[n] for n in wanted},INPUTS=INPUTS,LINEAR_TOL=1e-10)
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 arithmetic={'a_keep','a_sum','a_dd','a_add','a_sub','pack_fields','unpack_fields','collapse','fields_from_pair'};masks={'native_mask','metric_mask'}
 definitions(list(PINS)[0],arithmetic,SCOPE);definitions(list(PINS)[1],masks,SCOPE)
 for n in arithmetic|masks:setattr(P,n,SCOPE[n])
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 definitions('author_fragment_initial_york_trace_target_response_v001.py',{'trace_target_reference_scores'},globals());definitions(ANCHOR_SOURCE[0],{'anchor_scores'},globals())
 tree=ast.parse((BASE/'author_fragment_fixed_geometry_total_rate_state_v002.py').read_text());meta=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIXED_RATE_STATE_SOURCE_PINS' for t in n.targets));FIXED_RATE_SOURCE_PINS=ast.literal_eval(meta.value)

def bind(name,checksum):
 assert isinstance(checksum,str) and P.sha(P.path(name))==checksum,name
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==checksum;INPUTS[key]=checksum

def keep(name,value):
 a=np.asarray(value).copy();RAW[name]=a;AVAILABLE[name]=a.copy()
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 return a

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def closed(source,result,receipt,proof):
 bind(*source);pack=[]
 for q in (result,receipt,proof):bind(q[0],q[1]);v=json.loads(P.path(q[0]).read_text());assert v['status']==q[2];pack.append(v)
 r,rc,p=pack;assert r['owner']==rc['owner']==p['owner'] and r['owner']['source_sha256']==source[1]
 assert rc['status']=='CLOSED' and rc['result_sha256']==result[1]==p['result_sha256'] and rc.get('error_sha256') is None
 assert p['source_sha256']==source[1] and p['receipt_sha256']==receipt[1] and p['naturally_closed'] is True and p['exit_code']==0 and p['all_success_role_seals_verified'] is True
 assert r['qualification'] and rc['qualification'] and all(v is False for x in (r['qualification'],rc['qualification']) for v in x.values())
 assert all(q['passed'] is True for q in r['controls'])
 return r,rc

def record(r,rc,ref):
 bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text());assert q['file']==ref['file'] and q['sha256']==ref['sha256']
 q=dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256']);md=q['metadata']
 assert md['owner']==r['owner'] and md['failed'] is False and md['qualification'] and all(v is False for v in md['qualification'].values())
 assert any(thin(x)==thin(q) for x in r['checkpoints']) and ('metadata' not in ref or ref['metadata']==md)
 for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert rc['output_sha256'][n]==h
 return q

def admission():
 a,arc=closed(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF);f,frc=closed(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF);ac,fc=a['case'],f['case']
 assert f['status']==fc['status']==FINITE_STATUS and ac['free_prior_or_target_refitted'] is False and ac['prepared_metric_target_is_exact_owned_reference'] is True
 ai=record(a,arc,ac['input']);can=record(a,arc,ac['canonical']);out=record(f,frc,fc['readout'])
 ins=[q for q in f['checkpoints'] if q['metadata']['kind']=='INPUT'];assert len(ins)==1;fi=record(f,frc,ins[0]);pr=fi['metadata']['provenance']
 assert can['metadata']['input']==thin(ai) and ai['metadata']['rho_W_t_all_exact_zero'] is True and ai['metadata']['TT_or_exterior_prior_refitted'] is False
 assert fc['spatial_geometry_unchanged'] is True and fc['current99_and_physical6_fresh'] is True and fc['all16normal_ports_per_section'] is True and fc['physical_adoption'] is False
 assert pr['all_source_seals_authenticated'] is pr['correction_original_six_gates_admitted'] is pr['original_fixed_references_verified'] is pr['unchanged_sheet_value_identity_verified'] is True
 assert [thin(q) for q in fc['original_targets']]==[thin(q) for q in ac['original_canonical_target_refs']]==[thin(q) for q in pr['unchanged_original_targets']]
 assert pr['original_owned_TOTAL_time_words']==[q['metadata']['state'] for q in ac['columns']]
 assert pr['updated_phase_closure']==json.loads(json.dumps(UPDATED_PHASE_CLOSURE)) and pr['source_pins']==FIXED_RATE_SOURCE_PINS
 assert out['metadata']['correction_original_six_admitted'] is True and out['metadata']['new_current_original_six_admission_external'] is True
 assert out['metadata']['kind_scope']=='fresh_point_first_TOTAL_rate_momenta_all16normal_CMC_at_unchanged_spatial_geometry'
 return dict(anchor_input=ai,anchor_canonical=can,finite_input=fi,finite_readout=out,finite_provenance=pr)

def selected(q,names,role):
 for n,shape in names.items():assert q['metadata']['schema'][n]==dict(shape=shape,dtype='float64',finite=True),(role,n)
 data=P.read_pair(q,tuple(names))
 for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):INPUTS[str(P.path(n).resolve())]=h
 for n,a in data.items():keep(role+'_'+n,a)
 return data

def pair(data,prefix,label):
 x=tuple(data[prefix+'_'+w].copy() for w in ('hi','lo'));keep(label+'_both_words',np.stack(x));return x

def packet(refs):
 CONTEXT.update(stage='read_CLOSED_current_and_fixed_references');shapes=dict(native=[33,3,87,45],metric=[6,87,45])
 original=selected(refs['anchor_input'],dict(original_reference_original_rhs=[403340],original_reference_current_Pn=shapes['native'],original_reference_native_scale=shapes['native'],original_reference_metric_scale=shapes['metric']),'anchor_INPUT')
 target_names={n+'_'+w:s for role,s in shapes.items() for n in ('NEW_reference_anchor_unchanged_or_prepared_target_'+role,) for w in ('hi','lo')};target_names.update({'NEW_reference_anchor_target_minus_current_epsilon_metric_'+w:shapes['metric'] for w in ('hi','lo')})
 target=selected(refs['anchor_canonical'],target_names,'anchor_CANONICAL');current=selected(refs['finite_readout'],{'completed_READOUT_current_'+role+'_'+w:s for role,s in shapes.items() for w in ('hi','lo')},'finite_READOUT')
 scales=(original['original_reference_native_scale'],original['original_reference_metric_scale'])
 for s in scales:assert np.all(s>0)
 inp=P.checkpoint('INPUT',{n:a.copy() for n,a in AVAILABLE.items()},dict(kind='closed_NEW139_current_and_unchanged_anchor_targets_references_scales',sources={n:thin(refs[n]) for n in ('anchor_input','anchor_canonical','finite_input','finite_readout')},anchor_terminal=(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF),finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),original_metric_epsilon_reference_is_fixed=True,physical_adoption=False));RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear()
 residual={};CONTEXT.update(stage='NEW_saved_word_target_minus_current_and_original_six')
 for role in shapes:
  t=pair(target,'NEW_reference_anchor_unchanged_or_prepared_target_'+role,'unchanged_target_'+role);v=pair(current,'completed_READOUT_current_'+role,'NEW_finite_current_'+role)
  residual[role]=P.a_sub(t,v);keep('NEW_target_minus_current_'+role+'_both_words',np.stack(residual[role]))
 packed=tuple(P.pack_fields(residual['native'][w],residual['metric'][w]) for w in (0,1));keep('NEW_original_masked_residual_both_words',np.stack(packed))
 metric_pair=pair(target,'NEW_reference_anchor_target_minus_current_epsilon_metric','unchanged_original_metric_epsilon_reference');metric_reference=P.collapse(metric_pair,'original_metric_reference_norm_readout')
 defect=P.a_sub(metric_pair,P.a_dd(metric_reference));keep('original_metric_reference_norm_readout_defect_both_words',np.stack(defect))
 scores,norms,zero=anchor_scores(packed,P.unpack_fields(original['original_reference_original_rhs'],False)[0],original['original_reference_current_Pn'],metric_reference,scales,'FRESH_TOTAL_RATE_ORIGINAL_SIX')
 readout=P.collapse(packed,'NEW_residual_norm_readout');defect=P.a_sub(packed,P.a_dd(readout));keep('NEW_residual_norm_readout_defect_both_words',np.stack(defect))
 assert scores.shape==(3,2) and np.all(np.isfinite(scores)) and np.all(scores>=0)
 roles=('native_original_affine','native_original_canonical','metric_NEW_target');expected=[role+'_'+norm for role in roles for norm in ('raw','scaled')]
 for i,role in enumerate(roles):
  for j,norm in enumerate(('raw','scaled')):CHECKS.append(dict(ordinal=len(CHECKS),name=role+'_'+norm,score=float(scores[i,j]),tolerance=P.LINEAR_TOL,passed=bool(scores[i,j]<=P.LINEAR_TOL),relative_ratio_defined=not zero[i],exact_zero_reference_rule=bool(zero[i])))
 assert [q['name'] for q in CHECKS]==expected and len(CHECKS)==6;admitted=all(q['passed'] for q in CHECKS)
 cert=P.checkpoint('CERTIFICATE',{n:a.copy() for n,a in AVAILABLE.items()},dict(kind='fresh_finite_current_six_original_reference_measurements',input=thin(inp),six_gate_names=expected,scores=scores.tolist(),norms_references_thresholds=norms.tolist(),zero_reference_flags=zero,original_six_admitted=admitted,metric_denominator_is_original_anchor_epsilon=True,no_action_EOS_solver_or_scatter_replay=True,normal_CMC_or_physical_acceptance=False));RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear()
 return dict(status='FRESH_TOTAL_RATE_ORIGINAL_SIX_ADMITTED' if admitted else 'FRESH_TOTAL_RATE_ORIGINAL_SIX_MEASURED_NOT_ADMITTED',input=thin(inp),certificate=thin(cert),original_six_admitted=admitted,scores=scores.tolist(),norms_references_thresholds=norms.tolist(),zero_reference_flags=zero,anchor_terminal=(ANCHOR_SOURCE,ANCHOR_RESULT,ANCHOR_RECEIPT,ANCHOR_PROOF),finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),normal_CMC_stationarity_evolution_and_new43_acceptance=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for q in (FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF) for v in q),'Root release after natural finite closure required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,closed_sources={n:thin(refs[n]) for n in ('anchor_input','anchor_canonical','finite_input','finite_readout')},new_scientific_producer_calls=0,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',{n:a.copy() for n,a in {**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}.items()},dict(context=dict(CONTEXT),kind='fresh_six_available_saved_inputs_and_readouts'),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
