"""HELD closed-candidate mechanical cache handoff; root numerical owner only.
Reuse reviewed135 admission and selective closed STATE words, never old physics.
Only four NEW147 cache preparations; no temporal action, factor or solve.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V003'
PROTOCOL='CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V003.md'
PROTOCOL_SHA='8cbb40efb388a2cace4c17122a40043582120f15d885fb9ae37ea3c90e63adc8'
RECOVERY_FILE='cross_u_finite0_state_normal_recovery_v005.py'
RECOVERY_SHA='8f9b528e1da5114b148585799e902cdaaa14a6ac2af60e7deff9a85375792be2'
RECOVERY_RESULT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RESULT.json',None,'FINITE0_NEW_ACTION_CURRENT_NORMAL_CMC_RESIDUAL_MEASURED')
RECOVERY_RECEIPT=('CROSS_U_FINITE0_STATE_NORMAL_RECOVERY_V005_RECEIPT.json',None,'CLOSED')
RECOVERY_CLOSURE_PROOF=(None,None,None)
RECOVERY_SUCCESS_PROOF_STATUS='ROOT_NATURAL_CLOSED_FINITE0_RECOVERY_SUCCESS_SEALS_VERIFIED'
PRIOR_PHASE_PRODUCER_SOURCE=('cross_u_phase_fixed_weak_charge_preparation_v003.py', 'ed18caa749cbbfef40956ee4764390d688aaf6a1567912317d6cc81c9851d079')
PRIOR_PHASE_PRODUCER_RESULT=('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003_RESULT.json', 'fefe9a83c871577653a3965d0c61ff869f6786ff0b1c9a943d9abf4fd6ee79d7', 'LITERAL_PHASE_HESSIAN_POSITIVE_AND_FIXED_WEAK_CHARGE_MASS_PREPARED')
PRIOR_PHASE_PRODUCER_RECEIPT=('CROSS_U_PHASE_FIXED_WEAK_CHARGE_PREPARATION_V003_RECEIPT.json', '9d2fb6e0a649976167144b0d428bc730800844d78670587ad8891b11ddfcca90', 'CLOSED')
PRIOR_PHASE_ANCESTRY_PROOF=('ROOT_CLOSED_PRIOR_PHASE_LOADS_ANCESTRY_SEALS_V001.json', 'cf5575e71d2c818d84da7fbb5e676bf60e9051ebed2917aab8e9a192e3884ed3', 'ROOT_CLOSED_PRIOR_PHASE_LOADS_ANCESTRY_SEALS_VERIFIED')
COMPONENT_PROOF=('CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json','5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9','CANDIDATE_LITERAL_PHASE_MASS_MANUFACTURED_COMPONENT_CONTROLS_PASS')
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
ADMISSION_PARENT='cross_u_completed_candidate_literal_phase_mass_preparation_v004.py'
ADMISSION_PARENT_SHA='18891223822037932792c117146c685b3e7a1c1632d45a122f9e05def8992e8f'
ADMISSION_PROTOCOL=('CROSS_U_COMPLETED_CANDIDATE_LITERAL_PHASE_MASS_PREPARATION_V004.md','b6930f9dca96687c7fb230e88087dba983dae9147df0aa30bb053107d72d2d1b')
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_finite0_completed_state_restore_v002.py':'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59'}
SNAMES=('g','hi','U','z','uc','P','Z','r','z2','f','phi','omega','xi','w','R','Z_coordinate')
CNAMES=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
MATERIAL=('B','GC','ALPHA','ELL','C')
CURRENT_PREFIXES=('value_native_current_','value_metric_current_','value_literal_phase_current_','delta_native_current_','delta_metric_current_','delta_literal_phase_current_','actual_native_canonical_target_residual_','actual_metric_canonical_target_residual_','actual_phase_canonical_target_residual_','prior_signed_bridge_','prior_phase_current_')
np=P=ADMISSION=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for file,h in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 tree=ast.parse((BASE/IO_PARENT).read_text());names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==10
 exec(compile(ast.Module(body=defs,type_ignores=[]),IO_PARENT,'exec'),globals());initialize_io()

def load_completed_admission():
 global ADMISSION
 bind(ADMISSION_PARENT,ADMISSION_PARENT_SHA);bind(*ADMISSION_PROTOCOL)
 names={'bind_record','completed_candidate_admission'};tree=ast.parse((BASE/ADMISSION_PARENT).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==2
 selected=('RECOVERY_FILE','RECOVERY_SHA','RECOVERY_RESULT','RECOVERY_RECEIPT','RECOVERY_CLOSURE_PROOF','RECOVERY_SUCCESS_PROOF_STATUS','COMPONENT_PROOF','IO_PARENT_SHA','FLAGS','PRIOR_PHASE_PRODUCER_SOURCE','PRIOR_PHASE_PRODUCER_RESULT','PRIOR_PHASE_PRODUCER_RECEIPT','PRIOR_PHASE_ANCESTRY_PROOF')
 scope={n:globals()[n] for n in selected};scope.update(P=P,bind=bind,thin=thin,json=json)
 exec(compile(ast.Module(body=defs,type_ignores=[]),ADMISSION_PARENT,'exec'),scope);ADMISSION=types.SimpleNamespace(**{n:scope[n] for n in names})

def initialize_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 files=list(PINS);trees=[ast.parse((BASE/n).read_text()) for n in files[:2]]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F'}
 defs=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(defs)==25
 exec(compile(ast.Module(body=defs,type_ignores=[]),files[1],'exec'),SCOPE)
 for n in base|primitive|set(MATERIAL):setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 compact={'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'}
 restore={'finite0_saved_pair','finite0_saved_raw_family','finite0_validate_saved_transaction_ownership'}
 for file,count,selected in ((files[2],11,None),(files[3],6,compact),(files[4],2,None),(files[5],6,None),(files[6],3,restore)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (selected is None or n.name in selected)];assert len(defs)==count,file
  for n in tree.body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('FINITE0_RESTORE_PARENT_SOURCE_SHA','FINITE0_RESTORE_RECOVERY_SOURCE_SHA'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_mechanical_cache_exact_exponent_product');globals()['a_prod']=P.a_prod

def mechanical_state_names(schema):
 required=tuple('completed_candidate_s_'+n for n in SNAMES)+tuple('completed_candidate_c_'+n for n in CNAMES)+tuple('candidate_raw_unchanged_material_'+n for n in MATERIAL)+('NEW_reference_input_reference_E0_hi','NEW_reference_input_reference_E0_lo')
 envelopes=tuple(n for n in schema if n.startswith('candidate_raw_coefficient_operation_'))
 prefixes=('candidate_raw_direct_minus_quotient_','candidate_raw_model_minus_new_raw_chart_first_','candidate_raw_new_candidate_minus_owned_reference_','candidate_raw_geometry_')
 extra=('candidate_raw_KGamma_minus_KADM_hi','candidate_raw_KGamma_minus_KADM_lo','candidate_raw_Ktrace_Gamma_minus_ADM_hi','candidate_raw_Ktrace_Gamma_minus_ADM_lo','candidate_raw_new_first_compatibility_minus_E0_hi','candidate_raw_new_first_compatibility_minus_E0_lo')
 diagnostics=tuple(n for n in schema if n.startswith(prefixes) or n in extra);names=required+envelopes+diagnostics
 assert len(envelopes)==29 and len(diagnostics)==54 and len(names)==len(set(names))==121 and all(n in schema for n in names)
 return names

def hydrate_mechanical_state(data,input_metadata,state_metadata,proof):
 assert state_metadata['kind']=='NEW_candidate_completed_configuration_features_momenta_EOS_and_mean' and state_metadata['failed'] is False
 assert state_metadata['new_candidate_coefficients_and_EOS_evaluated'] is True and state_metadata['all_configuration_inverse_E0_and_chart_gaps_retained'] is True and state_metadata['physical_adoption'] is False
 assert input_metadata['rho']==0. and input_metadata['compact_direction_node']==[43,22]
 ownership=finite0_validate_saved_transaction_ownership(input_metadata,state_metadata,proof);iq=state_metadata['column'];refs=input_metadata['refs']
 for name,field in (('pilot_reference','pilots'),('owned_spatial_reference','forces')):assert thin(state_metadata[name])==thin(refs[field][iq])
 assert thin(state_metadata['current_time_words'])==thin(refs['current_jets'])
 for n in MATERIAL:assert data['candidate_raw_unchanged_material_'+n].shape==() and data['candidate_raw_unchanged_material_'+n].item()==getattr(P,n),n
 s=finite0_saved_raw_family(data,'completed_candidate_s_');c=finite0_saved_raw_family(data,'completed_candidate_c_');envelopes=finite0_saved_raw_family(data,'candidate_raw_coefficient_operation_')
 assert len(c['N'])==3784 and set(s)==set(SNAMES) and set(c)==set(CNAMES)
 return dict(s=s,c=c,coefficient_envelopes=envelopes),dict(E0=finite0_saved_pair(data,'NEW_reference_input_reference_E0')),ownership

def mechanical_preparation_packet(refs):
 meta=refs['input']['metadata'];original=read(refs['input'],tuple(meta['schema']));basis=read(refs['basis'],tuple(refs['basis']['metadata']['schema']))
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 selected=tuple(n for n in refs['loads']['metadata']['schema'] if n.startswith(CURRENT_PREFIXES));current=read(refs['loads'],selected)
 assert all(n in current for n in ('value_native_current_hi','value_native_current_lo','value_metric_current_hi','value_metric_current_lo','prior_signed_bridge_native_original_target','prior_signed_bridge_metric_original_target','prior_phase_current_fixed_literal_weak_phase_charge_hi','prior_phase_current_fixed_literal_weak_phase_charge_lo'))
 for prefix,values in (('original_input_',original),('registered_basis_',basis),('completed_loads_',current)):
  for n,a in values.items():keep(prefix+n,a)
 input_record=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='bitcopied_completed_current_prior_targets_and_registered_mechanical_basis',original_input=thin(refs['input']),basis=thin(refs['basis']),loads=thin(refs['loads']),prior_literal_weak_charge=thin(refs['prior_phase_loads']),closed_candidate_proof=refs['closed_proof'],fixed=meta['fixed'],owned_background=meta['owned_background'],inherited_controls=refs['result']['controls'],stored_norms=refs['loads']['metadata']['norms'],new_current_or_target_scatter_performed=False,physical_adoption=False));clear_current();cache_refs=[];denominators=[]
 for state in refs['states']:
  iq=state['metadata']['column'];CONTEXT.update(stage='restore_completed_mechanical_state',column=iq,state=thin(state),completed_cache_refs=list(cache_refs))
  names=mechanical_state_names(state['metadata']['schema']);data=read(state,names)
  for n,a in data.items():keep('copied_STATE_'+n,a)
  candidate,reference,ownership=hydrate_mechanical_state(data,meta,state['metadata'],refs['closed_proof']);assert np.array_equal(candidate['s']['R'],basis['R'][iq])
  candidate['candidate_provenance']=dict(state=thin(state),input=thin(refs['input']),ownership=ownership,closed_candidate_proof=refs['closed_proof'])
  cache=candidate_temporal_prepare(candidate,reference,keep,'NEW_candidate_temporal_cache');assert cache['p']==3784 and cache['configuration_held'] is True
  gamma=cache['gamma_squared'];keep('NEW_candidate_temporal_cache_gamma_squared_denominator_both_words',np.stack(gamma).copy())
  for word,a in zip(('hi','lo'),gamma):keep('NEW_candidate_temporal_cache_gamma_squared_denominator_'+word,a)
  assert all(a.shape==(3784,) for a in gamma) and np.all(gamma[0]>0) and np.all(gamma[1]==0)
  for n in MATERIAL:keep('unchanged_declared_'+n,np.asarray(getattr(P,n)))
  record=P.checkpoint('CACHE',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_full_column_fixed_configuration_temporal147_cache_from_completed_STATE',column=iq,points=3784,candidate_provenance=candidate['candidate_provenance'],input=thin(input_record),state=thin(state),original_transaction_owner=state['metadata']['owner'],source_selector_names=list(names),cache_prefix='NEW_candidate_temporal_cache',gamma_squared_key='NEW_candidate_temporal_cache_gamma_squared_denominator',constants={n:getattr(P,n) for n in MATERIAL},primary_gap_scope='saved_current_chart_firstjets_and_NEW_formal_Iu_minus_raw_up_only',old_coefficients_features_momenta_EOS_current_or_action_replayed=False,configuration_held=True,global_inverse_or_action_qualified=False,physical_adoption=False));cache_refs.append(thin(record));denominators.append(tuple(a.copy() for a in gamma));del data,candidate,reference,cache;clear_current()
 assert len(cache_refs)==4
 for word,wi in (('hi',0),('lo',1)):keep('prepared_four_column_gamma_squared_'+word,np.stack([x[wi] for x in denominators]).copy())
 keep('full_column_point_counts',np.full(4,3784,dtype=np.int64));keep('unchanged_declared_material',np.asarray([getattr(P,n) for n in MATERIAL]))
 preparation=P.checkpoint('PREPARATION',arrays(AVAILABLE),dict(kind='completed_candidate_full_grid_mechanical_temporal_cache_handoff_only',caches=cache_refs,input=thin(input_record),basis=thin(refs['basis']),loads=thin(refs['loads']),closed_candidate_proof=refs['closed_proof'],quadrature_order=[0,1,2,3],material_order=list(MATERIAL),full_point_count=15136,only_NEW_temporal_cache_prepare=True,mechanical_action_or_nodal_factor_or_inverse_evaluated=False,phase_block_supplied_separately=True,canonical_York_target_transport_required_separately=True,uniform_DD_or_global_inverse_qualified=False,physical_adoption=False))
 assert len(RECORDS)==6 and CHECKS==[]
 return dict(status='COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED',input=input_record,caches=cache_refs,preparation=preparation,closed_candidate_proof=refs['closed_proof'],inherited_controls=12,new_controls=0,roles=6,full_points=15136,physics_action_evaluated=False,global_inverse_or_physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and all(x is not None for x in (PROTOCOL_SHA,RECOVERY_RESULT[1],RECOVERY_RECEIPT[1],*RECOVERY_CLOSURE_PROOF)),'Natural CLOSED recovery, proof and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(IO_PARENT,IO_PARENT_SHA)
  for name,h in tuple(PINS.items())+((PROTOCOL,PROTOCOL_SHA),):bind(name,h)
  load_completed_admission();refs=ADMISSION.completed_candidate_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,candidate_source=refs['closed_proof'],admission_source=dict(file=ADMISSION_PARENT,sha256=ADMISSION_PARENT_SHA),inherited_state_refs=[thin(q) for q in refs['states']],roles=6,new_temporal_cache_preparations=4,new_actions_factors_or_solves=0,physical_adoption=False));initialize_helpers()
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=mechanical_preparation_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='copied_completed_and_unfinished_NEW_mechanical_cache_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
