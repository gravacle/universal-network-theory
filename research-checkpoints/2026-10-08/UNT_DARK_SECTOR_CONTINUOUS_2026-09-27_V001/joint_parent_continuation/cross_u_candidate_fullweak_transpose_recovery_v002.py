"""HELD continuation of CLOSED31059 from earned case0 signed E/F lifts.
No completed direction, lift, point/current/factor/fixture action is replayed.
Root alone authenticates closure, releases and executes this new namespace.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_FULLWEAK_TRANSPOSE_RECOVERY_V002'
RECOVERY_PROTOCOL='CANDIDATE_FULLWEAK_TRANSPOSE_RECOVERY_V001.md'
RECOVERY_PROTOCOL_SHA='d9a423f1b10dd842c96a48e2a16d84d0a9babdb74b412be1c4cd8cf5f5c9fd67'
FAILED_SOURCE=('cross_u_candidate_fullweak_transpose_contacts_v003.py','6f27f665577203642f6f70b8a8932de0edda87597f25e3f874d70af76b7cc722')
FAILED_ERROR=('CROSS_U_CANDIDATE_FULLWEAK_TRANSPOSE_CONTACTS_V003_ERROR.json','23b882b255b9a73393e6f4e4d1403f65bc423505f918178d1ec53771c46bd2ca')
FAILED_RECEIPT=('CROSS_U_CANDIDATE_FULLWEAK_TRANSPOSE_CONTACTS_V003_RECEIPT.json','2022158be566bc573a6b1b2d0150b274828e1d76ea84f2b2ca2e633bd9b30f1b')
FAILED_PROOF=('ROOT_NATURAL_CLOSED_FULLWEAK_TRANSPOSE_PARTIAL_SEALS_V001.json','d2c0eaa0967bb840fdbb9da225fa3e7dfaaa967a1302d6030296fb4d44d9675c','ROOT_NATURAL_CLOSED_FULLWEAK_TRANSPOSE_PARTIAL_SUCCESS_AND_ERROR_SEALS_VERIFIED')
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)


def load_parent_definitions():
 assert hashlib.sha256((BASE/FAILED_SOURCE[0]).read_bytes()).hexdigest()==FAILED_SOURCE[1]
 tree=ast.parse((BASE/FAILED_SOURCE[0]).read_text());wanted={'selected_definitions','load_io','initialize_helpers','closed_packet','selected_record','seal','transpose_admission','read_point_coefficients','new_original_direction'}
 declarations={'DRIVER_PROTOCOL','PROTOCOL_SHA','IO_PARENT','IO_PARENT_SHA','NODAL_SOURCE','NODAL_RESULT','NODAL_RECEIPT','NODAL_PROOF','MECHANICAL_SOURCE','MECHANICAL_RESULT','MECHANICAL_RECEIPT','MECHANICAL_CLOSURE_PROOF','PINS'}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in declarations:globals()[n.targets[0].id]=ast.literal_eval(n.value)
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted];assert {n.name for n in defs}==wanted
 exec(compile(ast.Module(body=defs,type_ignores=[]),FAILED_SOURCE[0]+'_definitions_only','exec'),globals());load_io()


def initialize_recovery_helpers():
 initialize_helpers()
 for n,v in dict(B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8).items():SCOPE[n]=globals()[n]=v;setattr(P,n,v)
 file='author_fragment_candidate_specialized_weak_mechanical_action_v002.py';old=next(n for n in ast.parse((BASE/file).read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='specialized_weak_mechanical_action')
 start=next(i for i,n in enumerate(old.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='native_parts' for t in n.targets))
 template=ast.parse("def resume_saved_first_lifts(blocks,basis,saved_native,saved_metric,keep,label,column_complete=None):\n native=saved_native;metric=saved_metric\n masks=dict(native=np.broadcast_to(P.native_mask(),(33,3,87,45)),metric=P.metric_mask())") .body[0]
 template.body+=old.body[start:]
 assert [ast.dump(n,include_attributes=False) for n in template.body[3:]]==[ast.dump(n,include_attributes=False) for n in old.body[start:]]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[template],type_ignores=[])),file+'_unearned_point_and_scatter_suffix','exec'),globals())


def failed_admission():
 for q in (FAILED_SOURCE,FAILED_ERROR,FAILED_RECEIPT,FAILED_PROOF):bind(q[0],q[1])
 e=json.loads(P.path(FAILED_ERROR[0]).read_text());rc=json.loads(P.path(FAILED_RECEIPT[0]).read_text());pr=json.loads(P.path(FAILED_PROOF[0]).read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==FAILED_ERROR[1] and rc['prior_receipt_sha256'] is None
 assert e['owner']==rc['owner']==pr['owner'] and e['owner']['pid']==31059 and e['owner']['source_sha256']==FAILED_SOURCE[1]
 assert e['qualification']==rc['qualification']==pr['qualification']==FLAGS and e['raw_preservation_traceback'] is e['closing_traceback'] is None
 assert pr['status']==FAILED_PROOF[2] and pr['source_sha256']==FAILED_SOURCE[1] and pr['error_sha256']==FAILED_ERROR[1] and pr['receipt_sha256']==FAILED_RECEIPT[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==1 and pr['all_input_seals_verified'] is pr['all_output_seals_verified'] is pr['all_success_role_seals_verified'] is pr['failed_role_seal_verified'] is True
 assert pr['input_seals_verified']==len(rc['input_sha256'])==517 and pr['output_seals_verified']==len(rc['output_sha256'])==19
 assert pr['completed_original_controls']==len(e['controls'])==0 and pr['recover_case0_original_directions_all_four_E_F_lifts_and_first_physical_inputs'] is True
 assert "AttributeError: 'types.SimpleNamespace' object has no attribute 'B'" in e['traceback'] and 'candidate_specialized_temporal_action' in e['traceback']
 assert not P.path(FAILED_ERROR[0].removesuffix('_ERROR.json')+'_RESULT.json').exists()
 roles=e['checkpoints'];assert len(roles)==8 and [thin(q) for q in roles[:7]]==pr['successful_roles'] and thin(roles[-1])==pr['failed_role']
 for i,q in enumerate(roles):
  for key,h in (('file','sha256'),('commit_file','commit_sha256')):bind(q[key],q[h]);assert rc['output_sha256'][q[key]]==q[h]
  assert json.loads(P.path(q['commit_file']).read_text())=={k:v for k,v in q.items() if k not in ('commit_file','commit_sha256')}
  assert q['metadata']['owner']==e['owner'] and q['metadata']['qualification']==FLAGS and q['metadata']['failed'] is (i==7)
 for n,h in rc['input_sha256'].items():bind(n,h)
 return dict(error=e,receipt=rc,proof=pr,success=roles[:7],raw=roles[-1])


def restore_completed_packet(failed,refs):
 roles=failed['success'];copies=[];data_sets=[]
 for i,q in enumerate(roles+[failed['raw']]):
  CONTEXT.update(stage='inherited_words_only',original_role=i);data=read(q,tuple(q['metadata']['schema']));RAW.clear()
  for n,a in data.items():keep(n,a)
  copy=thin(seal('INHERITED_COPY',dict(kind='verbatim_closed31059_words_without_action_replay',original_role=i,original=thin(q),original_metadata=q['metadata'],failed_source=FAILED_SOURCE,failed_error=FAILED_ERROR,failed_receipt=FAILED_RECEIPT,failed_proof=FAILED_PROOF,physical_adoption=False)));copies.append(copy);data_sets.append(data)
 inp=roles[0];md=inp['metadata'];canonical=lambda x:json.loads(P.encode(x).decode())
 assert md['nodal_input']==thin(refs['input']) and md['closed_nodal']==canonical(refs['closed']) and md['mechanical']==canonical(refs['mechanical']['closed_provenance']) and md['point_descriptors']==canonical(refs['chunks'])
 basis={n:data_sets[0]['copied_nodal_original_basis_'+n].copy() for n in ('R','dv','hats')}
 for n in basis:assert np.array_equal(basis[n],data_sets[0]['copied_mechanical_registered_basis_'+n]) and np.array_equal(basis[n],data_sets[5]['NEW_fullweak_transpose_prepared_original_basis_'+n])
 basis['closed_provenance']=refs['basis_provenance'];caches=[]
 for iq,q in enumerate(roles[1:5]):
  original=refs['mechanical']['caches'][iq];assert q['metadata']['column']==iq and q['metadata']['source']==thin(original)
  prefix='copied_cache%d_'%iq+POINT_CACHE_PREFIX;data=data_sets[1+iq];pair=lambda n:tuple(data[prefix+n+'_'+w].copy() for w in ('hi','lo'));ep=prefix+'copied_positive_coefficient_'
  expected=set('copied_cache%d_'%iq+n for n in candidate_point_cache_names(original['metadata']));assert set(data)==expected and len(data)==117
  cache=dict(s={n:data[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:data[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a.copy() for n,a in data.items() if n.startswith(ep)},constants=original['metadata']['constants'],candidate_provenance=original['metadata']['candidate_provenance'],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
  assert all(cache['constants'][n]==getattr(P,n) for n in cache['constants']);caches.append(cache)
 assert roles[5]['metadata']['input']==thin(inp) and roles[5]['metadata']['cache_copies']==[thin(q) for q in roles[1:5]] and roles[5]['metadata']['closed_nodal']==canonical(refs['closed'])
 assert roles[6]['metadata']['case']==0 and roles[6]['metadata']['input']==thin(inp)
 direction=data_sets[6];probe=tuple(direction['NEW_fullweak_transpose_case0_probe_original_packed_both_words_'+w].copy() for w in ('hi','lo'));dual=tuple(direction['NEW_fullweak_transpose_case0_dual_original_packed_both_words_'+w].copy() for w in ('hi','lo'))
 raw=data_sets[7];prefix='NEW_fullweak_transpose_case0_authoritative67_';pair=lambda n:tuple(raw[prefix+n+'_'+w].copy() for w in ('hi','lo'));native=pair('original_lift_native_values');metric=pair('original_lift_physical_metric_values')
 assert len(raw)==22 and not any('_linear_jets_' in n or '_linear_canonical_' in n for n in raw)
 assert native[0].shape==native[1].shape==(33,15136,3) and metric[0].shape==metric[1].shape==(15136,6)
 for q in ('probe','dual'):
  name='NEW_fullweak_transpose_case0_'+q+'_original_packed_both_words';assert np.array_equal(direction[name+'_both_words'],np.stack((probe if q=='probe' else dual)))
 fields=[P.unpack_fields(a,False) for a in probe]
 for n,index in (('native',0),('metric',1)):
  for word in (0,1):assert np.array_equal(raw[prefix+'supplied_'+n+'_nodes_'+('hi','lo')[word]],fields[word][index])
 blocks=dict(columns=caches,basis={n:basis[n] for n in ('R','dv','hats')},all_four_actual_columns_required=True,global_inverse_earned=False,physical_adoption=False)
 prepared=dict(chunks=list(refs['chunks']),basis={n:basis[n].copy() for n in ('R','dv','hats')},closed=refs['closed'],physical_adoption=False,coefficient_transpose_only=True,authoritative147_association_measured=False,global_inverse_qualified=False)
 return dict(input=thin(inp),cache_refs=[thin(q) for q in roles[1:5]],prepared_ref=thin(roles[5]),direction_ref=thin(roles[6]),blocks=blocks,basis=basis,prepared=prepared,probe=probe,dual=dual,native_lift=native,metric_lift=metric,copies=copies)


def recovered_transpose_packet(restored,refs,failed):
 basis=restored['basis'];blocks=restored['blocks'];prepared=restored['prepared'];inp=restored['input'];cache_refs=restored['cache_refs'];cases=[]
 for case in (0,1):
  CONTEXT.update(stage='NEW_unearned_case',case=case,column=0);label='NEW_fullweak_transpose_case%d'%case
  if case==0:probe=restored['probe'];dual=restored['dual'];direction=restored['direction_ref']
  else:
   probe=new_original_direction(case,False,keep,label+'_probe');dual=new_original_direction(case,True,keep,label+'_dual');direction=thin(seal('DIRECTION',dict(kind='genuinely_NEW_predeclared_same_candidate_paired_original_coordinates',case=case,input=inp,old_basis_or_action_replayed=False,physical_adoption=False)))
  columns=[];chunks=[]
  def column_complete(iq,data):
   CONTEXT.update(stage='NEW_completed_authoritative_column',case=case,column=iq);capture_families('completed_column_',data);ref=thin(seal('ACTION_COLUMN',dict(kind='NEW_authoritative147_fixed_configuration_temporal_column',case=case,column=iq,cache=cache_refs[iq],direction=direction,physical_adoption=False)));columns.append(ref);return ref
  if case==0:result=resume_saved_first_lifts(blocks,basis,restored['native_lift'],restored['metric_lift'],keep,label+'_authoritative67',column_complete)
  else:
   fields=[P.unpack_fields(a,False) for a in probe];result=specialized_weak_mechanical_action(blocks,basis,tuple(q[0] for q in fields),tuple(q[1] for q in fields),keep,label+'_authoritative67',column_complete)
  forward=ct_pair(label+'_NEW_authoritative_weak',P.pack_dd(result['weak']['native'],result['weak']['metric']),keep);forward_ref=thin(seal('ACTION_WEAK',dict(kind='NEW_all_four_original_weak67_forward',case=case,columns=columns,direction=direction,physical_adoption=False)))
  forward_bound=candidate_weak_mechanical_positive(blocks,basis,probe,keep,label+'_authoritative_positive124');positive_ref=thin(seal('ACTION_POSITIVE',dict(kind='NEW_separate_unsigned147_original_lift_and_scatter_bound',case=case,direction=direction,represented_factor_bound_used=False,physical_adoption=False)))
  def chunk_complete(descriptor,part):
   ct_pair(label+'_completed_chunk_native',part[0],keep);ct_pair(label+'_completed_chunk_metric',part[1],keep)
   ref=thin(seal('TRANSPOSE_CHUNK',dict(kind='NEW_directed_point_coefficient_transpose',case=case,column=descriptor['column'],selection=[descriptor['lo'],descriptor['hi']],source=descriptor['point_block_ref'],direction=direction,completed_point_partials_retained_before_clear=True,physical_adoption=False)));chunks.append(ref);return ref
  trans=candidate_measured_coefficient_fullweak_transpose(prepared,dual,read_point_coefficients,keep,label+'_coefficient_transpose',chunk_complete);transpose_ref=thin(seal('TRANSPOSE_WEAK',dict(kind='NEW_original_Sstar_directed_Kstar_rounded_Estar',case=case,direction=direction,chunks=chunks,uniform_adjoint_or_inverse_qualified=False,physical_adoption=False)))
  trans_bound=candidate_fullweak_coefficient_positive(prepared,dual,read_point_coefficients,keep,label+'_coefficient_positive');transpose_positive_ref=thin(seal('TRANSPOSE_POSITIVE',dict(kind='NEW_saved_padded_point_bound_reverse_original_maps',case=case,direction=direction,raw_or_nodal_moment_envelope_substituted=False,physical_adoption=False)))
  provenance=dict(genuinely_NEW_same_candidate_forward_direction=True,old_point_basis_or_action_replayed=False,same_candidate_provenance=refs['closed']['same_candidate_provenance'],forward=forward_ref,transpose=transpose_ref,closed_nodal=refs['closed'])
  contact=candidate_new_fullweak_transpose_pairing_contact(probe,dual,forward,trans['packed'],forward_bound,trans_bound,provenance,keep,P.check,label+'_pairing')
  pairing=thin(seal('PAIRING',dict(kind='NEW_wholeweak_direction_pair_and_source_association_contact',case=case,direction=direction,forward=forward_ref,forward_positive=positive_ref,transpose=transpose_ref,transpose_positive=transpose_positive_ref,controls=list(CHECKS[-1:]),literal_action_gradient_or_gauge_block_tested=False,physical_adoption=False)))
  cases.append(dict(case=case,direction=direction,forward=forward_ref,transpose=transpose_ref,pairing=pairing,association_gap=[np.asarray(w).item() for w in contact['gap']],uncancelled_envelope=float(contact['envelope'])))
 assert len(CHECKS)==2 and len(RECORDS)==267 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 assert [q['name'] for q in CHECKS]==['NEW_fullweak_transpose_case%d_pairing'%case for case in (0,1)]
 final=thin(seal('PREPARATION',dict(kind='two_NEW_fullweak_forward_coefficient_transpose_contacts_only',input=inp,prepared=restored['prepared_ref'],cases=cases,original2e11_implementation_gates_unchanged=True,literal_LV_bridge_earned=False,gauge_mixed_block_earned=False,stationarity_feedback_earned=False,canonical_six_rows_tested=False,global_inverse_or_uniform_adjoint_qualified=False,old_component_inverse_failure_repaired=False,physical_adoption=False)))
 assert len(RECORDS)==268;logical=failed['success']+RECORDS[8:];assert len(logical)==267
 return dict(status='NEW_FULLWEAK_COEFFICIENT_TRANSPOSE_DIRECTION_CONTACTS_PASS',input=inp,prepared=restored['prepared_ref'],preparation=final,cases=cases,closed_nodal=refs['closed'],roles=267,current_roles=268,new_controls=2,inherited_original_roles=7,new_original_roles=260,auxiliary_inherited_copy_roles=8,inherited_copy_records=restored['copies'],original_failed_source=FAILED_SOURCE,original_failed_error=FAILED_ERROR,original_failed_receipt=FAILED_RECEIPT,original_failed_proof=FAILED_PROOF,original_failure_preserved=True,old_case0_directions_signed_lifts_point_basis_current_factor_or_solver_replayed=False,literal_LV_or_gauge_or_adjoint_solve_earned=False,uniform_DD_adjoint_or_global_inverse_qualified=False,original_six_or_normal_or_CMC_physical_admitted=False,old_component_inverse_failure_repaired=False,physical_adoption=False),logical


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and RECOVERY_PROTOCOL_SHA is not None,'Root release required'
 assert all(x is not None for q in (FAILED_SOURCE,FAILED_ERROR,FAILED_RECEIPT,FAILED_PROOF) for x in q),'Natural failed closure/proof required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive recovery namespace required';load_parent_definitions();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(RECOVERY_PROTOCOL,RECOVERY_PROTOCOL_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_recovery_helpers();failed=failed_admission();refs=transpose_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,original_failure=FAILED_ERROR,partial_proof=FAILED_PROOF,logical_original_roles=267,current_roles=268,inherited_original_roles=7,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):restored=restore_completed_packet(failed,refs);case,logical=recovered_transpose_packet(restored,refs,failed)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=logical,current_checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW_fullweak_transpose_recovery',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
