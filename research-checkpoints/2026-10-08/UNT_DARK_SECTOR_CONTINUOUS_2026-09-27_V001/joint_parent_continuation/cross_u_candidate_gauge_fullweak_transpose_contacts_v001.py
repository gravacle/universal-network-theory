"""HELD NEW represented gauge C/Cstar contacts; root numerical ownership.
Only completed64-port coefficients and original basis are reused. No gauge,
current, EOS, mechanical action, old fixture or adjoint solve is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_GAUGE_FULLWEAK_TRANSPOSE_CONTACTS_V001'
PROTOCOL='CANDIDATE_GAUGE_FULLWEAK_TRANSPOSE_CONTACTS_V001.md'
PROTOCOL_SHA='d6375ab6dd2cdd74cee35b5c65d43a9f21642288fd18fd9bda63153e0f3c1d33'
GAUGE_SOURCE=(None,None)
GAUGE_RESULT=(None,None,'CANDIDATE_GAUGE_REGISTERED_CURRENT_FORWARD_CONTACTS_MEASURED')
GAUGE_RECEIPT=(None,None,'CLOSED')
GAUGE_PROOF=(None,None,None)
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'cross_u_finite0_candidate_action_residual_v007.py':'ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'author_fragment_candidate_fullweak_transpose_stationarity_v003.py':'3a1180531be32d317fd018264ee220ee61981357f828ad7dba7afb8e1bc54871',
 'author_fragment_candidate_gauge_fullweak_transpose_v003.py':'a35bb8085710aff9ec5a88e44fe146cd6fe3fc700db485b44ab5aecea4ce35d7',
 'author_fragment_candidate_gauge_fullweak_transpose_positive_v001.py':'0edfe32328977955234de838c91ccf47087393ec948dfaaa4929f4eed60910be',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94'}
COMPONENT_PROTOCOL=('CANDIDATE_GAUGE_FULLWEAK_TRANSPOSE_AND_FEEDBACK_V003.md','142c2694f88473c397660495c7ba37422a978b0d5c0744c0258ab8c47d4090cf')
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)


def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])


def initialize():
 global np,N
 for file,h in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 io='cross_u_finite0_candidate_action_residual_v007.py';names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(io,names),io,'exec'),globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','scalar_mask','scalar_lift','dd_scalar_scatter'}
 primitive={'a_matvec','a_transpose','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter','pack_fields','unpack_fields','pack_dd'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 for n in base|primitive|{'B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n])
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,None),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL'];assert P.TOL==2e-11
 names={'normal_test_mask','extend_normal_tests','normal_hat_jet','paired_restrict_normal_rows'};file=list(PINS)[2]
 exec(compile(selected_definitions(file,names),file,'exec'),SCOPE);N=types.SimpleNamespace(**{n:SCOPE[n] for n in names})
 choices=(('author_fragment_exact_exponent_two_product_v003.py',None),('author_fragment_candidate_fullweak_transpose_stationarity_v003.py',{'ct_pair','ct_matvec','candidate_original_scatter_transpose'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv'}),('author_fragment_candidate_gauge_fullweak_transpose_v003.py',None),('author_fragment_candidate_gauge_fullweak_transpose_positive_v001.py',None))
 for file,names in choices:exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(GAUGE_TRANSPOSE_AUTHOR_DRAFT=False,GAUGE_TRANSPOSE_AUTHORING_IN_PROGRESS=False,GAUGE_TRANSPOSE_POSITIVE_AUTHOR_DRAFT=False,GAUGE_TRANSPOSE_POSITIVE_AUTHORING_IN_PROGRESS=False)
 for suffix,ref in (('SOURCE',GAUGE_SOURCE),('RESULT',GAUGE_RESULT),('RECEIPT',GAUGE_RECEIPT),('PROOF',GAUGE_PROOF)):globals()['GAUGE_TRANSPOSE_'+suffix]=ref
 for group in ('MECHANICAL','PHASE'):
  for suffix in ('SOURCE','RESULT','RECEIPT','PROOF'):globals()['GAUGE_'+group+'_ADJOINT_'+suffix]=(None,None)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_gauge_contact_exact_product_scope');assert SCOPE['a_mul'].__globals__ is SCOPE and SCOPE['a_prod'] is P.a_prod


def bind_record(ref):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);cm=json.loads(P.path(ref['commit_file']).read_text())
 assert cm['file']==ref['file'] and cm['sha256']==ref['sha256']
 if 'metadata' in ref:assert cm['metadata']==ref['metadata']
 return dict(file=ref['file'],sha256=ref['sha256'],commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'],metadata=cm['metadata'])


def gauge_admission():
 refs=(GAUGE_SOURCE,GAUGE_RESULT,GAUGE_RECEIPT,GAUGE_PROOF)
 assert all(x is not None for q in refs for x in q),'Natural64-port gauge proof required before any payload'
 for q in refs:bind(q[0],q[1])
 r=json.loads(P.path(GAUGE_RESULT[0]).read_text());rc=json.loads(P.path(GAUGE_RECEIPT[0]).read_text());proof=json.loads(P.path(GAUGE_PROOF[0]).read_text())
 assert r['status']==GAUGE_RESULT[2] and rc['status']==GAUGE_RECEIPT[2] and proof['status']==GAUGE_PROOF[2]
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['source_sha256']==proof['source_sha256']==GAUGE_SOURCE[1]
 assert rc['result_sha256']==proof['result_sha256']==GAUGE_RESULT[1] and proof['receipt_sha256']==GAUGE_RECEIPT[1] and rc['error_sha256'] is None
 assert type(proof['exit_code']) is int and proof['exit_code']==0 and proof['naturally_closed'] is proof['all_success_role_seals_verified'] is True
 assert type(proof['input_seals_verified']) is int and proof['input_seals_verified']==len(rc['input_sha256']) and type(proof['output_seals_verified']) is int and proof['output_seals_verified']==len(rc['output_sha256'])
 stem=GAUGE_RESULT[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 assert r['qualification']==rc['qualification']==FLAGS and len(r['checkpoints'])==78 and len(r['controls'])==80
 assert len({q['name'] for q in r['controls']})==80 and all(q['passed'] is True and q['tolerance']==2e-11 for q in r['controls'])
 records=[bind_record(q) for q in r['checkpoints']]
 for q in records:
  assert q['metadata']['owner']==r['owner'] and q['metadata']['failed'] is False
  for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert rc['output_sha256'][q[n]]==q[h]
 c=r['case'];header=bind_record(c['input']);prep=bind_record(c['preparation']);cols=[bind_record(q) for q in c['columns']];tests=[bind_record(q) for q in c['tests']];caches=[bind_record(q) for q in c['cache_columns']]
 assert len(cols)==len(caches)==4 and len(tests)==64 and c['registered_mechanical_literal_phase_current_only'] is True
 assert c['original_targets_epsilon_and_physical_flags_unchanged'] is True and c['stationarity_feedback_and_global_inverse_unearned'] is True and c['C_equals_minus_Rv_or_Schwarz_assumed'] is False
 md=prep['metadata'];assert md['all64_ports_earned'] is md['original_current_targets_unchanged'] is True and md['global_inverse_rank_or_physical_adoption'] is False
 assert md['input']==thin(header) and md['columns']==[thin(q) for q in cols] and md['tests']==[thin(q) for q in tests] and md['cache_columns']==[thin(q) for q in caches]
 assert header['metadata']['gauge_row_order']==['N','beta_R','beta_Z','beta_phi'] and header['metadata']['gauge_jet_order']==['value','R','Z','t'] and header['metadata']['current_targets_and_epsilon_unchanged'] is True
 basis=bind_record(header['metadata']['basis']);original_input=bind_record(header['metadata']['original_input'])
 for q in (basis,original_input):
  for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str(P.path(q[n]).resolve())]==q[h]
 descriptors=[];provenance=[]
 for iq,(col,cache) in enumerate(zip(cols,caches)):
  assert col in records and cache in records and col['metadata']['column']==cache['metadata']['column']==iq and col['metadata']['cache']==thin(cache) and col['metadata']['input']==thin(header)
  assert col['metadata']['test_refs']==[thin(q) for q in tests[iq*16:(iq+1)*16]]
  for ordinal,q in enumerate(tests[iq*16:(iq+1)*16]):
   m=q['metadata'];assert m['column']==iq and (m['row'],m['jet'])==divmod(ordinal,4) and m['target_derivative_zero'] is m['all_primary_time_jets_retained'] is True and m['cache']==thin(cache)
   assert m['phase_firstjet_port_bothwords_zero'] is (m['jet']>0)
  state=bind_record(cache['metadata']['state']);phase=bind_record(cache['metadata']['updated_phase']);temporal=bind_record(cache['metadata']['temporal_cache'])
  assert state['metadata']['column']==phase['metadata']['column']==temporal['metadata']['column']==iq and state['metadata']['owner']['pid']==(94049 if iq==0 else 97585) and phase['metadata']['owner']['pid']==13764 and temporal['metadata']['owner']['pid']==13576
  for q in (state,phase,temporal):
   for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str(P.path(q[n]).resolve())]==q[h]
  p=dict(original_state=thin(state),updated_phase=thin(phase),temporal_cache=thin(temporal),gauge_cache=thin(cache),original_state_owner=state['metadata']['owner'],updated_phase_owner=phase['metadata']['owner'],temporal_cache_owner=temporal['metadata']['owner'],gauge_terminal_owner=r['owner'])
  provenance.append(p);descriptors.append(dict(column=iq,record=thin(col),test_refs=col['metadata']['test_refs'],gauge_row_order=('N','beta_R','beta_Z','beta_phi'),gauge_coordinate_order=('value','R','Z','t'),all16_gauge_ports_earned=True,gauge_target_derivative_zero=True,same_candidate_provenance=p,basis_provenance=thin(basis),resolved_column=col))
 closed=dict(source=GAUGE_SOURCE,result=GAUGE_RESULT,receipt=GAUGE_RECEIPT,proof=GAUGE_PROOF,naturally_closed=True,natural_exit_code=0,all_selected_seals_verified=True,physical_adoption=False,same_candidate_provenance=provenance,original_current_targets_unchanged=True,gauge_target_derivative_zero=True,same_updated_phase_and_mechanical_candidate=True)
 return dict(header=header,preparation=prep,columns=descriptors,basis=basis,original_input=original_input,closed=closed,proof=proof,inherited_source_controls=r['controls'])


def seal(role,metadata):
 ref=P.checkpoint(role,arrays({**AVAILABLE,**RAW}),dict(metadata,role=role));clear_current();return thin(ref)


def read_gauge_column(descriptor,families):
 assert tuple(families)==('native','metric','phase');ref=descriptor['resolved_column'];md=ref['metadata'];names=tuple('completed_NEW_gauge_column_coefficients_'+n+'_'+w for n in families for w in ('hi','lo'))
 for n,shape in (('native',[3784,99,4,4]),('metric',[3784,6,4,4]),('phase',[3784,4,4])):
  for w in ('hi','lo'):assert md['schema']['completed_NEW_gauge_column_coefficients_'+n+'_'+w]['shape']==shape and md['schema']['completed_NEW_gauge_column_coefficients_'+n+'_'+w]['dtype']=='float64'
 data=read(ref,names);paired={n:pair_from(data,'completed_NEW_gauge_column_coefficients_'+n) for n in families}
 return dict(paired=paired,record=descriptor['record'],source_provenance=descriptor['same_candidate_provenance'])


def declared_probe(case):
 assert case in (0,1);mask=N.normal_test_mask();assert np.count_nonzero(mask)==14875
 index=np.arange(mask.size,dtype=np.int64).reshape(mask.shape);sgn=1. if case==0 else -1.
 normal=(np.where(mask,sgn*((index+3*case)%11-5)/16.,0.),np.where(mask,((index+case)%3-1)*2.**-60,0.))
 time=(np.where(mask,((2*index+case)%13-6)/32.,0.),np.where(mask,sgn*((index+2*case)%5-2)*2.**-61,0.))
 mi=np.arange(403340,dtype=np.int64);pi=np.arange(3870,dtype=np.int64)
 mechanical=(sgn*((3*mi+case)%17-8)/32.,((mi+case)%3-1)*2.**-60)
 phase=(((5*pi+2*case)%19-9)/16.,sgn*((pi+case)%5-2)*2.**-61)
 for n,x in (('normal',normal),('time',time),('mechanical_dual',mechanical),('phase_dual',phase)):ct_pair('NEW_direction%d_'%case+n,x,keep)
 return normal,time,mechanical,phase


def gauge_contact_packet(refs):
 basis=read(refs['basis'],('R','dv','hats'));basis['closed_provenance']=thin(refs['basis'])
 for n in ('R','dv','hats'):keep('copied_closed_original_basis_'+n,basis[n].copy())
 prepared=prepare_candidate_gauge_fullweak_transpose(refs['columns'],basis,refs['closed'],keep,'NEW_original_gauge_transpose_preparation')
 names=['NEW_gauge_Cstar_direction%d_%s_pairing'%(case,group) for case in range(2) for group in ('mechanical','phase')]
 expected=['INPUT'];header=seal('INPUT',dict(kind='closed64_gauge_ports_original_maps_and_same_updated_candidate',basis=thin(refs['basis']),original_input=thin(refs['original_input']),gauge_header=thin(refs['header']),gauge_preparation=thin(refs['preparation']),gauge_terminal=refs['closed'],inherited_source_controls=refs['inherited_source_controls'],inherited_controls_are_ancestry_only=True,expected_NEW_control_names=names,negative_feedback_or_adjoint_execution=False,physical_adoption=False));cases=[]
 for case in range(2):
  CONTEXT.update(stage='NEW_registered_normal_time_probes',direction=case);normal,time,mechanical,phase=declared_probe(case)
  jets=candidate_gauge_registered_test_jets(normal,time,prepared['basis'],keep,'NEW_direction%d_original_gauge_test'%case)
  direction=seal('DIRECTION_INPUT',dict(kind='NEW_two_word_independent_normal_time_and_current_dual_polynomials',direction=case,input=header,normal_active_dofs=14875,mechanical_dual_dofs=403340,phase_dual_dofs=3870,temporal_test_basis_only=True,physical_gauge_time_ports_admitted=False,low_words_retained=True,physical_adoption=False));expected.append('DIRECTION_INPUT')
  for group,dual in (('mechanical',mechanical),('phase',phase)):
   label='NEW_gauge_direction%d_%s'%(case,group);progress=[]
   def complete_forward(descriptor,point):
    capture_families(label+'_completed_forward_column_',point);q=seal('FORWARD_COLUMN',dict(kind='NEW_materialized64_port_coefficient_forward_column',direction=case,group=group,column=descriptor['column'],direction_input=direction,source_column=descriptor['record'],same_candidate_provenance=descriptor['same_candidate_provenance'],old_port_action_replayed=False,physical_adoption=False));progress.append(q);return q
   CONTEXT.update(stage='NEW_coefficient_port_forward',direction=case,group=group)
   forward=candidate_gauge_new_port_forward(prepared,jets,group,read_gauge_column,keep,label+'_separate_forward',complete_forward);capture_families(label+'_completed_forward_',forward)
   fref=seal('FORWARD',dict(kind='NEW_original_S_times_completed_Cpoint_times_registered_polynomial',direction=case,group=group,columns=progress,direction_input=direction,forward_scope=forward['forward_scope'],physical_adoption=False));expected+=['FORWARD_COLUMN']*4+['FORWARD']
   CONTEXT.update(stage='NEW_coefficient_forward_positive',direction=case,group=group);fb=candidate_gauge_new_port_forward_positive(prepared,jets,group,read_gauge_column,keep,label+'_forward_positive')
   fbref=seal('FORWARD_BOUND',dict(kind='NEW_uncancelled_completed_port_forward_envelope',direction=case,group=group,forward=fref,upstream286_port_formula_error_bound=False,physical_adoption=False));expected.append('FORWARD_BOUND');progress=[]
   def complete_transpose(descriptor,point):
    ct_pair(label+'_completed_transpose_column_ports',point,keep);q=seal('TRANSPOSE_COLUMN',dict(kind='NEW_directed_coefficient_transpose_column',direction=case,group=group,column=descriptor['column'],direction_input=direction,source_column=descriptor['record'],same_candidate_provenance=descriptor['same_candidate_provenance'],weighted_Sstar_once=True,physical_adoption=False));progress.append(q);return q
   CONTEXT.update(stage='NEW_directed_gauge_Cstar',direction=case,group=group);transpose=candidate_gauge_fullweak_transpose(prepared,dual,group,read_gauge_column,keep,label+'_transpose',complete_transpose);capture_families(label+'_completed_transpose_',transpose)
   tref=seal('TRANSPOSE',dict(kind='NEW_original_weighted_Sstar_Cpointstar_unweighted_Tstar',direction=case,group=group,columns=progress,direction_input=direction,spatial_weight_count=1,time_covector_already_weighted=True,C_equals_minus_Rv_or_Schwarz_assumed=False,physical_adoption=False));expected+=['TRANSPOSE_COLUMN']*4+['TRANSPOSE']
   CONTEXT.update(stage='NEW_directed_gauge_Cstar_positive',direction=case,group=group);tb=candidate_gauge_fullweak_transpose_positive(prepared,dual,group,read_gauge_column,keep,label+'_transpose_positive');capture_families(label+'_completed_transpose_bound_',tb)
   tbref=seal('TRANSPOSE_BOUND',dict(kind='NEW_outward_bothword_completed_port_transpose_envelope',direction=case,group=group,transpose=tref,upstream286_port_formula_error_bound=False,physical_adoption=False));expected.append('TRANSPOSE_BOUND')
   provenance=dict(genuinely_NEW_registered_gauge_direction=True,old_current_port_action_or_fixture_replayed=False,same_candidate_provenance=prepared['same_candidate_provenance'],forward_scope=forward['forward_scope'])
   CONTEXT.update(stage='NEW_independent_fullweak_pairing',direction=case,group=group);contact=candidate_gauge_transpose_pairing_contact(normal,jets['physical_time_probe'],dual,forward['packed'],transpose,fb,tb,provenance,keep,P.check,names[len(CHECKS)])
   capture_families(label+'_completed_contact_',contact);cref=seal('CONTACT',dict(kind='NEW_pairing_of_independent_dual_with_port_forward_and_original_Tstar',direction=case,group=group,forward=fref,forward_bound=fbref,transpose=tref,transpose_bound=tbref,control=CHECKS[-1],coefficient_association_only=True,arbitrary286_or_uniform_adjoint_qualified=False,physical_adoption=False));expected.append('CONTACT');cases.append(dict(direction=case,group=group,direction_input=direction,forward=fref,transpose=tref,contact=cref))
 assert [q['name'] for q in CHECKS]==names and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 assert [q['metadata']['role'] for q in RECORDS]==expected
 readout=seal('READOUT',dict(kind='completed_NEW_directed_gauge_fullweak_coefficient_contacts',cases=cases,controls=CHECKS,physical_adoption=False));expected.append('READOUT');assert [q['metadata']['role'] for q in RECORDS]==expected
 return dict(status='CANDIDATE_GAUGE_FULLWEAK_REPRESENTED_COEFFICIENT_CONTACTS_PASS',input=header,cases=cases,readout=readout,gauge_terminal=refs['closed'],expected_control_names=names,NEW_control_count=len(names),current_role_count=len(expected),inherited_source_controls_ancestry_only=True,negative_feedback_or_adjoint_executed=False,authoritative286_arbitrary_direction_identity_earned=False,global_inverse_or_Schwarz_or_stationarity_or_physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and all(x is not None for q in (GAUGE_SOURCE,GAUGE_RESULT,GAUGE_RECEIPT,GAUGE_PROOF) for x in q),'Root release and natural64-port closure required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL)
  for name,h in PINS.items():bind(name,h)
  refs=gauge_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,gauge_proof=refs['proof'],qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=gauge_contact_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_gauge_coefficient_contacts',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
