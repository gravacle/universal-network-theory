"""HELD updated-phase literal H/cache and NEW diagonal preparation.
Only naturally CLOSED13764 primal words and unchanged original scalar basis are
consumed. Original targets/current remain bitcopied. No EOS/log/root/current,
normal/CMC/action/old diagonal or solver is replayed. Root alone executes after
full root and distinct peer review. The copied temporal delta is evidence only.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002'
PROTOCOL='CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V001.md'
PROTOCOL_SHA='647a96b115eb3365a006e9faed59a6e1adf1b4f8d7c18687c76d45cda101202c'
FINITE_SOURCE=('cross_u_candidate_finite_phase_state_evaluation_v002.py','0fe81190f0968ce599a001e5c65459abc176da4f5c38684072cbc70c1a2ff54b')
FINITE_RESULT=('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_RESULT.json','4ac3ff59a1fb825151f603cb1422771cf8648c6e9b09062e7dba849cb28635ec','CANDIDATE_FINITE_PHASE_STATE_AND_LITERAL_CURRENT_MEASURED')
FINITE_RECEIPT=('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_RECEIPT.json','8e707d334fc62f1f9b585460aecb1bda3385f21515ea3a142b56acc3c8289278','CLOSED')
FINITE_PROOF=('ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_V001.json','f97d469bf7852bdd72b2abbc093669070b4081d24feb00c1373fce6279600ebc','ROOT_NATURAL_CLOSED_FINITE_PHASE_STATE_SUCCESS_SEALS_VERIFIED')
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_phase_literal_charge_hessian_v002.py': '293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143', 'author_fragment_candidate_literal_phase_mass_v001.py': '0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38', 'author_fragment_finite0_completed_state_restore_v002.py': 'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235'}
PINS['CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V002_RESULT.json']='5f632a9927d41e36a40c7f2e0988997905ff99ac8dfef985307ce7723f63d4f9'
np=P=K=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for file,checksum in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==checksum,file
 tree=ast.parse((BASE/IO_PARENT).read_text());names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==10
 exec(compile(ast.Module(body=defs,type_ignores=[]),IO_PARENT,'exec'),globals());initialize_io()

def initialize_phase_helpers():
 global np,K
 import numpy as numpy
 np=numpy;SCOPE['np']=np;files=list(PINS);names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_reshape','scalar_mask','scalar_lift','dd_scalar_scatter'}
 tree=ast.parse((BASE/files[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==15;SCOPE['capture']=keep;exec(compile(ast.Module(body=defs,type_ignores=[]),files[0],'exec'),SCOPE)
 for name in names:setattr(P,name,SCOPE[name])
 tree=ast.parse((BASE/files[2]).read_text());names={'phase_pair_keep','phase_scalar_value','phase_mass_diagonal'};scope=dict(np=np,P=P);defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==3;exec(compile(ast.Module(body=defs,type_ignores=[]),files[2],'exec'),scope);K=types.SimpleNamespace(**{n:scope[n] for n in names})
 for file,count in ((files[3],5),(files[6],2)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count
  for n in tree.body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('FINITE0_RESTORE_PARENT_SOURCE_SHA','FINITE0_RESTORE_RECOVERY_SOURCE_SHA'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 tree=ast.parse((BASE/files[5]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate_phase_registered_constants'];assert len(defs)==1;exec(compile(ast.Module(body=defs,type_ignores=[]),files[5],'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_phase_mass_exact_exponent_product')

def bind_record(ref):
 bind(ref['file'],ref['sha256']);bind(ref['commit_file'],ref['commit_sha256']);cm=json.loads(P.path(ref['commit_file']).read_text())
 assert cm['file']==ref['file'] and cm['sha256']==ref['sha256']
 if 'metadata' in ref:assert cm['metadata']==ref['metadata']
 return dict(file=ref['file'],sha256=ref['sha256'],commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'],metadata=cm['metadata'])

def updated_phase_admission():
 bind(*FINITE_SOURCE)
 for n,h,status in (FINITE_RESULT,FINITE_RECEIPT,FINITE_PROOF):bind(n,h);assert json.loads(P.path(n).read_text())['status']==status
 r=json.loads(P.path(FINITE_RESULT[0]).read_text());rc=json.loads(P.path(FINITE_RECEIPT[0]).read_text());proof=json.loads(P.path(FINITE_PROOF[0]).read_text())
 assert r['owner']==rc['owner']==proof['owner'] and r['owner']['pid']==13764 and r['owner']['source_sha256']==FINITE_SOURCE[1]
 assert proof['source_sha256']==FINITE_SOURCE[1] and proof['result_sha256']==FINITE_RESULT[1] and proof['receipt_sha256']==FINITE_RECEIPT[1]
 assert type(proof['exit_code']) is int and proof['exit_code']==0 and proof['naturally_closed'] is True and proof['all_success_role_seals_verified'] is True
 assert rc['result_sha256']==FINITE_RESULT[1] and rc['error_sha256'] is None and r['qualification']==rc['qualification']==FLAGS
 assert not P.path('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_ERROR.json').exists()
 assert not P.path('CROSS_U_CANDIDATE_FINITE_PHASE_STATE_EVALUATION_V002_ERROR_RECEIPT.json').exists()
 c=r['case'];assert len(r['checkpoints'])==6 and r['controls']==[] and c['configuration_unchanged'] is c['original_target_words_unchanged'] is c['strict_EOS_domain_passed'] is True
 assert c['new_phase_mass_diagonal_constructed'] is c['finite_candidate_admitted'] is c['physical_adoption'] is False
 for ref in r['checkpoints']:
  assert ref['metadata']['owner']==r['owner'] and ref['metadata']['failed'] is False
  for n,key in (('file','sha256'),('commit_file','commit_sha256')):assert rc['output_sha256'][ref[n]]==ref[key]
 refs=[bind_record(q) for q in r['checkpoints']];inp,current=bind_record(c['input']),bind_record(c['current']);cols=[bind_record(q) for q in c['columns']]
 assert refs==[inp]+cols+[current] and [q['metadata']['column'] for q in cols]==[0,1,2,3]
 assert current['metadata']['columns']==[thin(q) for q in cols] and current['metadata']['input']==thin(inp)
 basis=bind_record(inp['metadata']['basis']);original=bind_record(inp['metadata']['original_input']);prior=bind_record(inp['metadata']['prior_literal_weak_charge'])
 assert thin(original)==c['original_input'] and thin(prior)==c['original_literal_phase_charge'] and inp['metadata']['unchanged_intrinsic_configuration'] is True
 for ref in (basis,original,prior):
  for n,key in (('file','sha256'),('commit_file','commit_sha256')):assert rc['input_sha256'][str(P.path(ref[n]).resolve())]==ref[key]
 for iq,q in enumerate(cols):
  md=q['metadata'];assert md['input']==thin(inp) and md['column']==iq and md['original_phase_targets_unchanged'] is True
  assert md['new_H_strictly_positive'] is md['new_H_resolved_positive'] is md['strict_EOS_domain_passed'] is True
 return dict(input=inp,current=current,columns=cols,basis=basis,original=original,prior=prior,terminal=dict(source=FINITE_SOURCE,result=FINITE_RESULT,receipt=FINITE_RECEIPT,proof=FINITE_PROOF,owner=r['owner']))

def updated_phase_packet(refs):
 basis=read(refs['basis'],('R','dv','hats'));saved_basis=read(refs['input'],tuple('NEW_finite_phase_unchanged_basis_'+n for n in basis)+tuple('NEW_finite_phase_unchanged_original_target_'+w for w in ('hi','lo')))
 for n in basis:keep('unchanged_registered_basis_'+n,basis[n]);assert np.array_equal(basis[n],saved_basis['NEW_finite_phase_unchanged_basis_'+n])
 current_names=tuple(n for n in refs['current']['metadata']['schema'] if n.startswith(('NEW_finite_phase_NEW_finite_literal_point_density_','NEW_finite_phase_NEW_finite_literal_weak_','NEW_finite_phase_NEW_target_minus_finite_current_','NEW_finite_phase_finite_residual_identity_contact_','NEW_finite_phase_weak_nonlinear_and_scatter_association_remainder_')))
 current=read(refs['current'],current_names);target=read(refs['prior'],('fixed_literal_weak_phase_charge_hi','fixed_literal_weak_phase_charge_lo'))
 for w in ('hi','lo'):assert np.array_equal(target['fixed_literal_weak_phase_charge_'+w],saved_basis['NEW_finite_phase_unchanged_original_target_'+w])
 for n,a in {**current,**{'original_'+n:x for n,x in target.items()}}.items():keep('copied_updated_'+n,a)
 current_ref=P.checkpoint('CURRENT',arrays(AVAILABLE),dict(kind='bitcopied_updated_phase_current_and_unchanged_literal_target',input=thin(refs['input']),basis=thin(refs['basis']),current=thin(refs['current']),prior_literal_weak_charge=thin(refs['prior']),terminal=refs['terminal'],EOS_current_or_scatter_replayed=False,physical_adoption=False));clear_current()
 constants=candidate_phase_registered_constants(refs['original']['metadata']['fixed']);columns=[];column_refs=[]
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(stage='copy_closed_updated_phase_H_and_current',column=iq)
  prefix='NEW_finite_phase_column%d_NEW_invariant_'%iq
  names=tuple(prefix+n+'_'+w for n in ('literal_temporal_H','literal_temporal_H_delta','literal_canonical_density','literal_canonical_density_delta','clock_pressure_u') for w in ('hi','lo'))+(prefix+'H_operation_envelope',)
  data=read(source,names)
  for n,a in data.items():keep('copied_finite_phase_'+n,a)
  pair=lambda n:tuple(data[prefix+n+'_'+w].copy() for w in ('hi','lo'))
  eos=dict(value=dict(H=pair('literal_temporal_H'),p=pair('literal_canonical_density'),u=pair('clock_pressure_u')),delta=dict(H=pair('literal_temporal_H_delta'),p=pair('literal_canonical_density_delta')),H_operation_envelope=data[prefix+'H_operation_envelope'].copy(),constants=constants,candidate_pressure_recomputed_from_invariant=True,owned_pressure_u_used=False,paired_input_collapsed=False)
  column=dict(eos=eos,candidate_provenance=dict(source['metadata']['candidate_provenance'],current_finite_phase=thin(source),updated_phase_primal_used=True,copied_temporal_delta_is_evidence_only=True),prior_literal_weak_charge=refs['prior']);columns.append(column)
  ref=P.checkpoint('PHASE_COLUMN',arrays(AVAILABLE),dict(kind='bitcopied_current_finite_phase_H_p_u_envelope_and_inherited_temporal_delta',column=iq,finite_phase=thin(source),candidate_provenance=column['candidate_provenance'],delta_scope='completed same temporal phase step only; not compact-chi',old_preupdate_H_or_diagonal_used=False,physical_adoption=False));column_refs.append(ref);clear_current()
 CONTEXT.update(stage='NEW_updated_phase_diagonal')
 cache=prepare_candidate_phase_mass(columns,basis,keep,'updated_phase_mass')
 saved_point=tuple(current['NEW_finite_phase_NEW_finite_literal_point_density_'+w] for w in ('hi','lo'))
 for a,b in zip(cache['current_point_density'],saved_point):assert np.array_equal(a,b),'Updated H/p mass cache must match the completed finite current'
 assert cache['strictly_positive_H'] is cache['resolved_positive_H'] is cache['strictly_positive_diagonal'] is True
 ref=P.checkpoint('PREPARATION',arrays(AVAILABLE),dict(kind='NEW_updated_finite_phase_literal_H_mass_diagonal_and_cache',columns=[thin(q) for q in column_refs],current=thin(current_ref),basis=thin(refs['basis']),prior_literal_weak_charge=thin(refs['prior']),terminal=refs['terminal'],constants=constants,phase_space_dofs=3870,phase_outer_top_free=True,current_H_and_p_tied_to_closed_finite_phase=True,old_preupdate_H_or_diagonal_used=False,copied_delta_scope='completed temporal step only; no geometry contact supplied',point_H_strictly_positive=cache['strictly_positive_H'],point_H_resolved_positive=cache['resolved_positive_H'],diagonal_strictly_positive=cache['strictly_positive_diagonal'],new_diagonal_only=True,EOS_current_normal_CMC_action_or_solver_replayed=False,inverse_response_or_physical_admission=False,physical_adoption=False))
 assert len(RECORDS)==6 and CHECKS==[]
 return dict(status='UPDATED_FINITE_PHASE_LITERAL_MASS_CACHE_PREPARED_UNQUALIFIED',preparation=ref,current=current_ref,columns=column_refs,finite_terminal=refs['terminal'],basis=thin(refs['basis']),original_literal_phase_charge=thin(refs['prior']),updated_phase_H_p_used=True,new_diagonal_only=True,original_charge_target_unchanged=True,compact_chi_contact_earned=False,linear_or_finite_response_admitted=False,physical_adoption=False)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Natural closed recovery, earned proof and root release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(IO_PARENT,IO_PARENT_SHA)
  for name,h in tuple(PINS.items())+((PROTOCOL,PROTOCOL_SHA),):bind(name,h)
  refs=updated_phase_admission();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256'];P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,finite_terminal=refs['terminal'],updated_phase_H_only=True,physical_adoption=False))
  initialize_phase_helpers()
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=updated_phase_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_candidate_phase_mass_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
