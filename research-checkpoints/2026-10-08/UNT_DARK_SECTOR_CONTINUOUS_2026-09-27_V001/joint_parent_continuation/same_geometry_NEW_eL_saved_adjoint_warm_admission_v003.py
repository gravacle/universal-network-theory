"""HELD bounded NEW-eL warm measurement; root execution only, zero actions.
Read closed solution/candidate/bound and fresh WEAK_BRIDGE, never old result,
K/chunks/factors/basis or producer bodies. Nonadmission is a measured outcome.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_WARM_ADMISSION_V003'
DRIVER_PROTOCOL='SAME_GEOMETRY_NEW_E_L_SAVED_ADJOINT_WARM_ADMISSION_V001.md'
PROTOCOL_SHA='b2e660c55cf3acfa426984334198bc941332edba92842ef80315b7bb8c72efea'
OLD_SOURCE=('saved_prefix_coefficient_adjoint_continuation_v003.py','eee8a878e3646ee9217166a3f8af8fa369805105a0566a33740046b4d5aac70c')
OLD_RESULT=('SAVED_PREFIX_COEFFICIENT_ADJOINT_CONTINUATION_V003_RESULT.json','36480a114571fb7f976f591eab6cf779bcf7ac3467e2d2ccb0073590d264f4ed','SAVED_PREFIX_COEFFICIENT_ADJOINT_SOURCE_ROWS_ADMITTED')
OLD_RECEIPT=('SAVED_PREFIX_COEFFICIENT_ADJOINT_CONTINUATION_V003_RECEIPT.json','09084a79011d7720d7ce3c48bb16dc2d15b61e5da0229e6e417b76e26c7c7160','CLOSED')
OLD_PROOF=('ROOT_NATURAL_CLOSED_SAVED_PREFIX_COEFFICIENT_ADJOINT_SUCCESS_SEALS_V001.json','acdfed26b8b05bf966644e40036363e61502fd9c329e83b0de816d7618931cbd','ROOT_NATURAL_CLOSED_SAVED_PREFIX_COEFFICIENT_ADJOINT_SUCCESS_SEALS_VERIFIED')
NEW_E_L_SOURCE=('cross_u_refreshed_total_rate_literal_gradient_contacts_v004.py', 'ea5707d13eb7ab78fba13db6a40ce67768c206a69d47e46643e9545fdb696fa1')
NEW_E_L_RESULT=('CROSS_U_REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_CONTACTS_V004_RESULT.json', '64d063bd4e1266e16a1d0fb60efa5e43b7bd69f40d801561540228f8fc3e691e', 'REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_AND_eL_CONTACTS_PASS')
NEW_E_L_RECEIPT=('CROSS_U_REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_CONTACTS_V004_RECEIPT.json', '869dbf59a4f3d2e5a0f5e1ae31b07964dd4b942401404af17ac8327dfc5c2ea6', 'CLOSED')
NEW_E_L_PROOF=('READONLY_NATURAL_CLOSED_REFRESHED_TOTAL_RATE_LITERAL_EL_SUCCESS_SEALS_V001.json', '1c705d3a9326f500b43bb4bb3096fd3102655f9104af59d522c7c45be88f280a', 'READONLY_NATURAL_CLOSED_REFRESHED_LITERAL_EL_SEALS_VERIFIED')
OLD_INPUT_COMMIT='CROSS_U_CANDIDATE_RIGHT_ONLY_MECHANICAL_ADJOINT_RESPONSE_V003_00000_INPUT.npz.COMMIT.json'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
WARM_HELPER='author_fragment_same_geometry_NEW_eL_adjoint_warmstart_v002.py'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18','cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19','author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d','author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235','author_fragment_native_metric_star_paired_gmres_resume_v002.py':'73b15a0e0512295aed41389a80c20ec6cf50ddef634497c805ada69c8ed738ee','author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py':'25747c25adfeda383c2f862352f0066010abefb79a2c06bdd1e6e6172dedb35c','author_fragment_candidate_fullweak_transpose_stationarity_v003.py':'3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871','author_fragment_candidate_directed_nodal_factor_apply_v001.py':'4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b','author_fragment_same_geometry_NEW_eL_adjoint_warmstart_v002.py':'31fe8dec87da94c2f429aa479173ea2e2485c534f5144b173c82a136d3061f29'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)

def metadata(file,checksum,limit=16*1024*1024):
 bind(file,checksum);path=P.path(file);assert path.stat().st_size<=limit,file
 return json.loads(path.read_text())

def constants(file,names):
 out={}
 for n in ast.parse(P.path(file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names:out[n.targets[0].id]=ast.literal_eval(n.value)
 assert set(out)==set(names),file;return out

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','keep','read','arrays','thin','clear_current','initialize_io'},globals());initialize_io()
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']

def bounded_keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 while len(AVAILABLE)>12:AVAILABLE.pop(next(iter(AVAILABLE)))
 return a

def initialize_arithmetic():
 global np,keep
 import numpy as numpy
 np=numpy;keep=bounded_keep;SCOPE.update(np=np,capture=keep)
 names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 definitions(list(PINS)[0],names,SCOPE)
 for n in names:setattr(P,n,SCOPE[n])
 definitions('author_fragment_exact_exponent_two_product_v003.py',{'exact_exponent_two_product','install_exact_exponent_product'},globals());install_exact_exponent_product(SCOPE,P,keep,'NEW_warm_norm_exact_product')
 definitions('author_fragment_native_metric_star_paired_gmres_resume_v002.py',{'native_metric_gmres_put','native_metric_gmres_tree','native_metric_gmres_dot','native_metric_gmres_norm'},globals())
 definitions('author_fragment_candidate_right_only_mechanical_adjoint_gmres_v002.py',{'mechanical_adjoint_reference','mechanical_adjoint_scores'},globals())
 definitions(WARM_HELPER,{'same_geometry_adjoint_pair','prepare_same_geometry_adjoint_warmstart'},globals())
 globals().update(constants(WARM_HELPER,{'SAME_GEOMETRY_ADJOINT_SOURCE_PINS'}));globals().update(SAME_GEOMETRY_ADJOINT_AUTHOR_DRAFT=False,SAME_GEOMETRY_ADJOINT_AUTHORING_IN_PROGRESS=False,SAME_GEOMETRY_ADJOINT_OLD_SOURCE=OLD_SOURCE,SAME_GEOMETRY_ADJOINT_OLD_RESULT=OLD_RESULT,SAME_GEOMETRY_ADJOINT_OLD_RECEIPT=OLD_RECEIPT,SAME_GEOMETRY_ADJOINT_OLD_PROOF=OLD_PROOF,SAME_GEOMETRY_ADJOINT_NEW_E_L_SOURCE=NEW_E_L_SOURCE,SAME_GEOMETRY_ADJOINT_NEW_E_L_RESULT=NEW_E_L_RESULT,SAME_GEOMETRY_ADJOINT_NEW_E_L_RECEIPT=NEW_E_L_RECEIPT,SAME_GEOMETRY_ADJOINT_NEW_E_L_PROOF=NEW_E_L_PROOF)
 P.LINEAR_TOL=1e-10

def closed(terminal,result_read=False):
 source,result,receipt,proof=terminal;assert all(v is not None for q in terminal for v in q),'Natural closed tuple required before payload selection'
 bind(*source);rc=metadata(*receipt[:2]);pr=metadata(*proof[:2])
 assert rc['status']==receipt[2] and rc['error_sha256'] is None and pr['status']==proof[2] and rc['owner']==pr['owner'] and rc['owner']['source_sha256']==source[1]==pr['source_sha256']
 assert rc['result_sha256']==result[1]==pr['result_sha256'] and pr['receipt_sha256']==receipt[1] and pr['naturally_closed'] is True and pr['exit_code']==0
 assert pr['all_success_role_seals_verified'] is True and rc['qualification']==FLAGS and pr.get('physical_adoption',False) is False
 if result_read:
  r=metadata(*result[:2]);assert r['status']==result[2] and r['owner']==rc['owner'] and r['qualification']==FLAGS and all(c['passed'] is True and c['tolerance']==2e-11 for c in r['controls'])
 else:r=None
 return r,rc,pr

def record(ref,rc,owner):
 q=metadata(ref['commit_file'],ref['commit_sha256']);assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 md=q['metadata'];assert md['owner']==owner and md['failed'] is False and md['qualification']==FLAGS
 assert all(rc['output_sha256'][ref[n]]==ref[h] for n,h in (('file','sha256'),('commit_file','commit_sha256')))
 return dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def admission():
 old_terminal=(OLD_SOURCE,OLD_RESULT,OLD_RECEIPT,OLD_PROOF);new_terminal=(NEW_E_L_SOURCE,NEW_E_L_RESULT,NEW_E_L_RECEIPT,NEW_E_L_PROOF)
 _,orc,opr=closed(old_terminal);new,nrc,npr=closed(new_terminal,True)
 assert opr['all_input_seals_verified'] is npr['all_input_seals_verified'] is True and opr['source_relative_adjoint_rows_admitted'] is True and opr['success_roles']==5771
 assert opr['history']['iterations']==40 and opr['history']['cap']==80 and opr['history']['operator']=='represented_directed_original244_coefficient_Astar' and opr['history']['uniform_adjoint_or_global_inverse_qualified'] is False
 old={}
 for role,ordinal,expected_role in (('solution',5770,'SOLUTION'),('candidate',5768,'CANDIDATE'),('positive',5525,'NEW_ASTAR_POSITIVE')):
  rows=[q for q in opr['records'] if q['ordinal']==ordinal];assert len(rows)==1 and rows[0]['role']==expected_role;old[role]=record(rows[0],orc,orc['owner'])
 assert thin(old['solution'])==opr['solution'] and old['candidate']['metadata']['iteration']==40 and old['candidate']['metadata']['admitted'] is True
 assert old['positive']['metadata']['context']['label']=='resumed_mechanical_adjoint_GMRES_candidate_040_new_positive' and old['positive']['metadata']['original244_unsigned_scope'] is True
 old_input_path=str(P.path(OLD_INPUT_COMMIT).resolve());assert old_input_path in orc['input_sha256'];old_input=metadata(OLD_INPUT_COMMIT,orc['input_sha256'][old_input_path]);prior=old_input['metadata']['closed_provenance']
 assert old_input['metadata']['failed'] is False and old_input['metadata']['owner']['pid']==37897 and old_input['metadata']['owner']['source_sha256']=='720ab9f4bad4a39a1c44e93acb22a8c4dd5ead032598503bec93774c6cab969b' and old_input['metadata']['qualification']==FLAGS
 case=new['case'];assert case['status']=='REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_AND_eL_CONTACTS_PASS' and case['roles']==23 and case['new_controls']==26 and case['source_polynomial_only'] is True and case['normal_feedback_or_geometry_correction_admitted'] is case['physical_adoption'] is False
 newer={n:record(case[n],nrc,nrc['owner']) for n in ('input','stationarity_bridge')};assert newer['input']['metadata']['anchor_input']==old_input['metadata']['anchor_input']
 assert newer['stationarity_bridge']['metadata']['canonical']==case['canonical_copy'] and newer['stationarity_bridge']['metadata']['same_new_state_adjoint_required'] is True
 terminal_names={'MECHANICAL_SOURCE','MECHANICAL_RESULT','MECHANICAL_RECEIPT','MECHANICAL_CLOSURE_PROOF'};new_constants=constants(NEW_E_L_SOURCE[0],terminal_names)
 mec=[new_constants[n] for n in ('MECHANICAL_SOURCE','MECHANICAL_RESULT','MECHANICAL_RECEIPT','MECHANICAL_CLOSURE_PROOF')];assert json.loads(json.dumps(mec))==[prior['mechanical'][n] for n in ('source','result','receipt','proof')]
 mr=metadata(*mec[1][:2]);assert mr['owner']==prior['mechanical']['owner'] and mr['status']==mec[1][2] and mr['qualification']==FLAGS
 assert newer['input']['metadata']['same_basis_from']==thin(mr['case']['input']) and json.loads(json.dumps(case['anchor_terminal']))==prior['anchor'] and len(case['transactions'])==4
 transactions=[]
 for iq,ref in enumerate(case['transactions']):
  q=record(ref,nrc,nrc['owner']);m=q['metadata'];assert m['column']==iq and m['fixed147_cache']==thin(mr['case']['caches'][iq]) and m['same_raw_configuration_and_E0_words_verified'] is True and m['old_rate_dependent_current_contacts_reused'] is False;transactions.append(thin(q))
 old_pins=constants(OLD_SOURCE[0],{'PINS'})['PINS'];new_pins=constants(NEW_E_L_SOURCE[0],{'PINS'})['PINS']
 for n in tuple(PINS)[:2]+('author_fragment_candidate_fullweak_transpose_stationarity_v003.py',):assert old_pins[n]==new_pins[n]==PINS[n]
 return dict(old=old,new=newer,old_owner=orc['owner'],new_owner=nrc['owner'],transactions=transactions,old_factor=old['solution']['metadata']['original_factor'],old_terminal=old_terminal,new_terminal=new_terminal,old_input=OLD_INPUT_COMMIT,old_positive_argument_association='source170 role new uses updated; label040; candidate↔solution word checks required',same_original_anchor=old_input['metadata']['anchor_input'])

def selected(q,names,label):
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names);bind(q['file'],q['sha256']);data=read(q,names)
 for n,a in data.items():RAW[label+'_'+n]=a;keep(label+'_'+n,a);s=q['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True and a.shape==(403340,)
 return data

def complete_stage(role,data,md):
 q=P.checkpoint(role,arrays(data),dict(md,context=dict(CONTEXT)));ref=thin(q);clear_current();return ref

def measurement(refs):
 CONTEXT.update(stage='closed_warm_argument_word_links');s=selected(refs['old']['solution'],tuple(n+'_'+w for n in ('lambda','action') for w in ('hi','lo')),'old_solution');c=selected(refs['old']['candidate'],tuple(n+'_'+w for n in ('nodes','action') for w in ('hi','lo')),'old_candidate')
 ties={n:all(np.array_equal(c[a+'_'+w].view(np.uint64),s[b+'_'+w].view(np.uint64)) for w in ('hi','lo')) for n,a,b in (('lambda','nodes','lambda'),('action','action','action'))}
 keep('completed_candidate_solution_word_ties',np.asarray(list(ties.values()),dtype=np.bool_));assert all(ties.values()),'Saved final candidate and solution must name identical total lambda/action'
 link=complete_stage('WORD_LINKS',dict(exact_word_ties=np.asarray(list(ties.values()),dtype=np.bool_)),dict(candidate=thin(refs['old']['candidate']),solution=thin(refs['old']['solution']),positive=thin(refs['old']['positive']),argument_association=refs['old_positive_argument_association'],physical_adoption=False));del c
 e=selected(refs['old']['positive'],('envelope',),'old_positive')['envelope'];n=selected(refs['new']['stationarity_bridge'],('NEW_literal_stationarity_eL_packed_hi','NEW_literal_stationarity_eL_packed_lo','NEW_literal_original_scale_packed'),'NEW_eL')
 adm=dict(terminals=list(refs['old_terminal'])+list(refs['new_terminal']),source_pins=SAME_GEOMETRY_ADJOINT_SOURCE_PINS,operator='represented_directed_original244_coefficient_Astar',all_selected_seals_verified=True,old_solution_and_action_argument_words_verified=True,same_paired_point_descriptors_and_original_basis_verified=True,same_147_raw_configuration_and_E0_words_verified=True,same_right_factor_and_original_coordinate_scale_verified=True,new_eL_copied_from_fresh139_literal142_bridge=True,callbacks_publish_completed_operands_without_mutation=True,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False,old_positive_bound_at_exact_warm_lambda_verified=True,old_positive_record=thin(refs['old']['positive']),old_solution_record=thin(refs['old']['solution']),new_eL_record=thin(refs['new']['stationarity_bridge']),old_source_rows_admitted=True)
 CONTEXT.update(stage='NEW_source_reference_and_saved_action_residual');packet=prepare_same_geometry_adjoint_warmstart((n['NEW_literal_stationarity_eL_packed_hi'],n['NEW_literal_stationarity_eL_packed_lo']),n['NEW_literal_original_scale_packed'],(s['lambda_hi'],s['lambda_lo']),(s['action_hi'],s['action_lo']),e,adm,keep,'NEW_eL_saved_warm',complete_stage)
 del s,e,n;ref=packet['reference'];groups=('native','metric','packed');admitted=packet['current']['admitted'];state=complete_stage('MEASURED_ADMISSION',dict(scores=packet['current']['scores'].copy(),new_source_norms=np.asarray([ref['groups'][g]['norms'] for g in groups]),new_source_exact_both_word_zero=np.asarray([ref['groups'][g]['zero_source_both_words'] for g in groups],dtype=np.bool_)),dict(context=packet['context'],word_links=link,admission=adm,refinement_required=not admitted,source_relative_adjoint_rows_admitted=admitted,old_actions_factors_unsigned_or_basis_replayed=False,physical_adoption=False))
 assert len(RECORDS)==3 and not CHECKS
 return dict(status='NEW_E_L_SAVED_WARM_SOURCE_ROWS_ADMITTED_ZERO_ACTIONS' if admitted else 'NEW_E_L_SAVED_WARM_RESIDUAL_MEASURED_REFINEMENT_REQUIRED',word_links=link,warm_context=packet['context'],measured_admission=state,source_relative_scores=packet['current']['scores'].tolist(),source_relative_adjoint_rows_admitted=admitted,refinement_required=not admitted,roles=3,construction_controls=0,new_point_actions=0,new_factor_applications=0,old_actions_factors_unsigned_or_basis_replayed=False,new_cycle_cap_if_refined=80,old_RHS_iterations_not_relabelled=True,normal_phase_or_gauge_feedback_evaluated=False,uniform_adjoint_or_global_inverse_qualified=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for q in (NEW_E_L_SOURCE,NEW_E_L_RESULT,NEW_E_L_RECEIPT,NEW_E_L_PROOF) for v in q),'Root review plus future220 natural closure required'
 assert not list(BASE.glob(STEM+'_*'));load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,old_terminal=refs['old_terminal'],new_terminal=refs['new_terminal'],selected_old_payload_roles=3,selected_new_payload_roles=1,old_result_not_parsed=True,point_or_factor_actions_scheduled=False,physical_adoption=False));initialize_arithmetic()
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=measurement(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_source_warm_norm_or_word_link',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
