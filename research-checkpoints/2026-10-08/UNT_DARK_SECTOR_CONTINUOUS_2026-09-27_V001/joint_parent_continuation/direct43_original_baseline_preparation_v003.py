"""HELD early DIRECT baseline fields only; root execution after FULL review.
NEW event arithmetic on authentic original coefficients, no old operator/body
replay, Gauss-rate interpolation, coupled solve or physical circle admission.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003'
DRIVER_PROTOCOL='DIRECT43_ORIGINAL_BASELINE_PREPARATION_V002.md'
PROTOCOL_SHA='ce2e03b589ff81c17bf2c988f8a93195305333f502c084a7f677e2b08627acbe'
SELECTED_PROOF=('ROOT_DIRECT43_ORIGINAL_BASELINE_SELECTED_INPUTS_VERIFIED_V001.json', '222a7afa2f2a34b32bde77334a686fbfbfc29e2506e6ddc599d5e19d2c76cb0e', 'ROOT_DIRECT43_ORIGINAL_BASELINE_SELECTED_INPUTS_VERIFIED')
TERMINALS={'admitted_rate_correction': {'proof': ('ROOT_NATURAL_CLOSED_HYBRID_MECHANICAL_SUCCESS_SEALS_V001.json', 'f40136768810c0efc28a4c699a7aca4d953cb3aae4acb9cfa5382bc498921dca', 'ROOT_NATURAL_CLOSED_HYBRID_MECHANICAL_SUCCESS_SEALS_VERIFIED'), 'receipt': ('SAVED_PREFIX_HYBRID_MECHANICAL_CONTINUATION_V007_RECEIPT.json', 'dfdb509109bde4a14fe6bc29bb6756f07a15be3f76cc71417845dac34627bb6c', 'CLOSED'), 'result': ('SAVED_PREFIX_HYBRID_MECHANICAL_CONTINUATION_V007_RESULT.json', 'd926e9b800a426dddd663db5b6530ca70f1424c00b50f9cdefe66a944e0bcec1', 'HYBRID_SEARCH_ORIGINAL_SIX_MECHANICAL_ROWS_ADMITTED'), 'source': ('saved_prefix_hybrid_mechanical_continuation_v007.py', 'd2ef156021ae94c25e523a3e5e3329d3c9687ff8a8df74df7c10ac30a40dd076')}, 'nodal_current': {'proof': ('READONLY_DD_NODE_COORDINATE_WORDS_V001_RESULT.json', 'ce19e353075341a82b475f019cd3fb6ca6f630868001b479b5aee1760c9bb8fc', 'SAVED_DD_NODE_COORDINATE_WORDS_PASS'), 'receipt': ('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001_RECEIPT.json', 'a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d', 'CLOSED'), 'result': ('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001_RESULT.json', '6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc', 'CURRENT_CANONICAL_AND_WEAK_CMC_COMPATIBLE'), 'source': ('cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py', '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18')}, 'point_TOTAL_baseline': {'proof': ('READONLY_NATURAL_CLOSED_SAVED_TOTAL_RATE_READOUT_RECOVERY_SUCCESS_SEALS_V001.json', 'a12ae17f08257468eea1740316c3a8da269abcec822d0cfb650d155f902c24bc', 'READONLY_NATURAL_CLOSED_SAVED_TOTAL_RATE_READOUT_RECOVERY_SUCCESS_SEALS_VERIFIED'), 'receipt': ('SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V002_RECEIPT.json', '54866112b1ffc45629d08b6c3bda09339184349b46178ad0584966f6dfcc4b21', 'CLOSED'), 'result': ('SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V002_RESULT.json', 'd12115e9b21dca3af5b9be9655385153864752f2364274817ff10e84472d9390', 'FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'), 'source': ('saved_fixed_geometry_total_rate_column_readout_recovery_v002.py', '06e5ea35f657ee14624740435bf9e36f1ee84e812dad9adb28304bd623c59075')}, 'reference_fields': {'proof': ('CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json', '88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9', 'CLOSED'), 'receipt': ('CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RECEIPT.json', '88f07cad6b1db07d2e10ee4f9c77a3da9aa08fa0416a0d57632dd8c50660c4a9', 'CLOSED'), 'result': ('CROSS_U_WHOLE_SLICE_CAUCHY_DATA_V002_RESULT.json', 'af0365e378a46c727108c7df57f527994a22b7428d72b1f67c6f1bbac93667ed', 'CONDITIONAL_WHOLE_SLICE_CAUCHY_INVENTORY_PASS'), 'source': ('cross_u_whole_slice_cauchy_data_v002.py', '6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7')}}
CATALOGUE=('NGC3198_FINE_Q3_43_POINT_SAVED_RECAP_V001.json','ea6e41a879bab1ed43fa556031ad96ae3535779707af62d30eff061b191fc024')
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'cross_u_whole_slice_cauchy_data_v002.py':'6d5a994584d1967965c72e9b0568e67c14610078832c9b40f4cbd04336b19df7',
 'cross_u_whole_slice_q1_adm_residual_v001.py':'c66c86c06d16c22209b95bde8e18a9bba4d336674da5389c777408534d205e8a',
 'cross_u_weak_canonical_spatial_euler_loads_v003.py':'4f239074b5345709f493b3633f7dd376fa7ac97dbb23bf20825eabde2ed56b79',
 'saved_prefix_hybrid_mechanical_continuation_v007.py':'d2ef156021ae94c25e523a3e5e3329d3c9687ff8a8df74df7c10ac30a40dd076',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d',
 'author_fragment_point_TOTAL_trial_fields_v001.py':'96925b148cb7c1b3660e76867e5c499e9b10868bc737209b194d9c667adc46ef',
 'author_fragment_model_metric_si_circle_readout_v002.py':'245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8',
 'author_fragment_finite_conformal_circle_event_v001.py':'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1',
 'author_fragment_direct_TOTAL43_finite_event_v001.py':'9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59',
 'author_fragment_direct43_owned_baseline_field_law_v004.py':'99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1'}
np=P=H=W=Q=D43=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==set(names),file
 exec(compile(ast.Module(body=nodes,type_ignores=[]),file,'exec'),scope)

def constants(file,names):
 out={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse((BASE/file).read_text()).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names}
 assert set(out)==set(names),file;return out

def metadata(file,checksum):
 bind(file,checksum);p=P.path(file);assert p.stat().st_size<=16*1024*1024,file;return json.loads(p.read_text())

def initialize():
 global np,P,H,W,Q,D43
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','keep','read','arrays','thin','clear_current','initialize_io'},globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','scalar_mask','scalar_lift','native_mask','metric_mask','lift_metric','dd_metric_F','unpack_fields'}
 definitions(list(PINS)[0],base,SCOPE);definitions(list(PINS)[1],{'a_matvec'},SCOPE)
 for n in base|{'a_matvec'}:setattr(P,n,SCOPE[n])
 definitions('author_fragment_exact_exponent_two_product_v003.py',{'exact_exponent_two_product','install_exact_exponent_product'},globals());install_exact_exponent_product(SCOPE,P,keep,'DIRECT_baseline_shared_exact_product')
 scopes={}
 for tag,file,names in (('H','author_fragment_model_metric_si_circle_readout_v002.py',{'q1_radial_readout_contact'}),('W','cross_u_whole_slice_cauchy_data_v002.py',{'metric'}),('Q','cross_u_whole_slice_q1_adm_residual_v001.py',{'metric_basis','connection_from_jet','metric_partial'}),('D43','author_fragment_direct_TOTAL43_finite_event_v001.py',{'direct_TOTAL43_sample_correction'})):
  scope=dict(np=np,math=math,P=P,RAW=RAW);definitions(file,names,scope);scopes[tag]=scope
 H=types.SimpleNamespace(**scopes['H']);W=types.SimpleNamespace(**scopes['W']);Q=types.SimpleNamespace(**scopes['Q']);D43=types.SimpleNamespace(**scopes['D43'])
 definitions('author_fragment_finite_conformal_circle_event_v001.py',{'fce_pair'},scopes['D43']);scopes['D43']['H']=H
 helper='author_fragment_direct43_owned_baseline_field_law_v004.py';definitions(helper,{'direct43_baseline_require','direct43_original_owned_reference','direct43_baseline_TOTAL_rate'},globals());globals().update(constants(helper,{'DIRECT43_BASELINE_SOURCE_PINS'}))
 globals().update(DIRECT43_BASELINE_AUTHOR_DRAFT=False,DIRECT43_BASELINE_AUTHORING_IN_PROGRESS=False,DIRECT43_BASELINE_PARENT_PINS=TERMINALS)

def admission():
 selected=metadata(*SELECTED_PROOF[:2]);assert selected['status']==SELECTED_PROOF[2] and selected['all_selected_bytes_headers_and_owner_links_verified'] is True and selected['no_Gauss_rate_interpolation_or_KADM_Lie_inverse'] is True
 assert selected['terminal_bindings']==json.loads(json.dumps(TERMINALS)) and selected['source_pins']==DIRECT43_BASELINE_SOURCE_PINS and selected['catalogue']==list(CATALOGUE)
 groups={};receipts={}
 for group,terminal in TERMINALS.items():
  for n,pin in terminal.items():assert all(v is not None for v in pin);bind(*pin[:2])
  rc=metadata(*terminal['receipt'][:2]);pr=metadata(*terminal['proof'][:2]);witness=selected['terminal_identities'][group]
  assert rc['status']==terminal['receipt'][2] and rc.get('error_sha256') is None and rc['result_sha256']==terminal['result'][1] and pr['status']==terminal['proof'][2]
  assert rc['owner']==witness['owner'] and rc['owner']['source_sha256']==terminal['source'][1] and all(v is False for v in rc['qualification'].values())
  assert witness['result_status']==terminal['result'][2] and witness['all_selected_seals_verified'] is True
  if witness['closure_kind']=='observed_natural_success':assert witness['naturally_closed'] is True and witness['exit_code']==0
  else:
   assert group in ('reference_fields','nodal_current') and witness['closure_kind']=='historical_source_success_publications'
   assert witness['naturally_closed'] is witness['exit_code'] is None
   assert witness['authenticated_source_success_publications'] is witness['original_process_absent'] is witness['original_ERROR_and_ERROR_RECEIPT_absent'] is True
  groups[group]=dict(terminal,**{n:witness[n] for n in ('closure_kind','naturally_closed','exit_code','all_selected_seals_verified')})
  if witness['closure_kind']=='historical_source_success_publications':groups[group].update({n:witness[n] for n in ('authenticated_source_success_publications','original_process_absent','original_ERROR_and_ERROR_RECEIPT_absent')})
  receipts[group]=rc
 assert selected['terminal_identities']['point_TOTAL_baseline']['inherited_scientific_owner_preserved'] is True;groups['point_TOTAL_baseline']['inherited_scientific_owner_preserved']=True
 refs={}
 assert set(selected['records'])=={'reference_fields','current_metric_nodes','current_RATE_JETS','rate_correction','basis'}
 for name,row in selected['records'].items():
  ref=row['record'];q=metadata(ref['commit_file'],ref['commit_sha256']);assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256'];bind(q['file'],q['sha256'])
  md=q['metadata'];assert md['owner']==row['scientific_owner'] and md['failed'] is False and all(v is False for v in md['qualification'].values())
  rc=receipts[row['terminal_group']];seals=rc['output_sha256'] if row['receipt_seal_map']=='output_sha256' else rc['input_sha256'];assert row['receipt_seal_map'] in ('output_sha256','input_sha256')
  for k,h in (('file','sha256'),('commit_file','commit_sha256')):assert seals.get(ref[k],seals.get(str(P.path(ref[k]).resolve())))==ref[h]
  refs[name]=dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])
 current=refs['current_metric_nodes']['metadata'];jets=refs['current_RATE_JETS']['metadata'];assert current['canonical_and_trace_admitted'] is True and current['targets_unchanged'] is True and current['metric_momentum_preparation'] is False
 assert jets['kind']=='genuine_fixed_Q1_two_word_rate_value_and_spatial_jets' and jets['canonical_rows_admitted'] is jets['weak_trace_admitted'] is True and current['basis_ref']==jets['basis_ref']==refs['basis']
 assert refs['rate_correction']['metadata']['physical_base_rates_reset'] is False and refs['rate_correction']['metadata']['physical_adoption'] is False
 for name in ('reference_nodes_and_sigma1_shift_owned_by_original24903','current47969_solution_and_RATE_JETS_same_coefficients','correction60363_is_original139_point_increment','same_original_mesh_basis_and_fixed_materials','point_TOTAL_baseline_law_matches_original139_ancestry','mesh_arrays_word_tied_to_registered_basis'):assert selected['source_links'][name] is True
 assert refs['reference_fields']['metadata']['owner']==receipts['reference_fields']['owner'] and refs['current_metric_nodes']['metadata']['owner']==refs['current_RATE_JETS']['metadata']['owner']==receipts['nodal_current']['owner'] and refs['rate_correction']['metadata']['owner']==receipts['admitted_rate_correction']['owner']
 return dict(selected=selected,groups=groups,records=refs)

def selected_words(ref,names,label):
 assert all(n in ref['metadata']['schema'] for n in names);data=read(ref,names)
 for n,a in data.items():
  RAW[label+'_'+n]=a.copy();keep(label+'_'+n,a);s=ref['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True
 return data

def complete(role,data,md):
 q=P.checkpoint(role,dict(RAW,**AVAILABLE,**arrays(data)),dict(md,context=dict(CONTEXT)));ref=thin(q);clear_current();return ref

def prepare(refs):
 records=refs['records'];CONTEXT.update(stage='authentic_original_coefficient_words')
 source=selected_words(records['reference_fields'],('r_kpc','z_kpc','final_state','sigma1_physical_beta_chi'),'original_reference');assert source['final_state'].shape==(65,87,45) and source['sigma1_physical_beta_chi'].shape==(2,87,45)
 current=selected_words(records['current_metric_nodes'],('metric_nodal_rate_hi','metric_nodal_rate_lo'),'original47969');correction=selected_words(records['rate_correction'],('correction_hi','correction_lo'),'original60363')
 basis=selected_words(records['basis'],('R','dv','hats','r','z'),'original_registered_basis');assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 r,z=source['r_kpc'],source['z_kpc'];potential=source['final_state'][0].copy();shift=source['sigma1_physical_beta_chi'][0].copy();metric=tuple(current['metric_nodal_rate_'+w].copy() for w in ('hi','lo'))
 assert r.shape==basis['r'].shape==(87,) and z.shape==basis['z'].shape==(45,) and np.array_equal(r.view(np.uint64),basis['r'].view(np.uint64)) and np.array_equal(z.view(np.uint64),basis['z'].view(np.uint64))
 assert all(correction['correction_'+w].shape==(403340,) for w in ('hi','lo'));increment=tuple(P.unpack_fields(correction['correction_'+w],False)[1] for w in ('hi','lo'))
 original=records['reference_fields']['metadata'];fixed=original['fixed'];background=original['owned_EPS5_background'];B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2;Hbar=fixed['Hunit']/299792458.*background['h'];finite_Hbar=background['h']*fixed['Hunit']/299792458.
 assert refs['selected']['fixed_materials']==dict(B=B,Hunit=fixed['Hunit'],background_h=background['h']) and math.isfinite(Hbar) and Hbar>0
 adm=dict(refs['groups'],source_pins=DIRECT43_BASELINE_SOURCE_PINS,fixed=dict(B=B,Hbar=Hbar,finite_normal_Hbar=finite_Hbar),owned_K_Hbar_uses_original_q1_operation_order=True,**{n:refs['selected']['source_links'][n] for n in ('reference_nodes_and_sigma1_shift_owned_by_original24903','current47969_solution_and_RATE_JETS_same_coefficients','correction60363_is_original139_point_increment','same_original_mesh_basis_and_fixed_materials','point_TOTAL_baseline_law_matches_original139_ancestry')})
 adm.update(reference_fields_record=thin(records['reference_fields']),current_metric_nodes_record=thin(records['current_metric_nodes']),rate_correction_record=thin(records['rate_correction']),basis_record=thin(records['basis']),reference_event_provenance=refs['selected']['reference_event_provenance'],finite_reference_provenance=refs['selected']['finite_reference_provenance'])
 catalogue=metadata(*CATALOGUE);rows=catalogue['rows'];assert len(rows)==43;Rvalues=[float(q['R_kpc']) for q in rows];assert all(math.isfinite(q) and q>0 for q in Rvalues)
 header=complete('INPUT',dict(R_mesh=r,Z_mesh=z,original_potential_nodes=potential,original_shift_nodes=shift,current_metric_hi=metric[0],current_metric_lo=metric[1],correction_metric_hi=increment[0],correction_metric_lo=increment[1],catalogue_R=np.asarray(Rvalues),owned_K_Hbar=np.asarray(Hbar),finite_normal_Hbar=np.asarray(finite_Hbar)),dict(admission=adm,selected_records={n:thin(q) for n,q in records.items()},catalogue=CATALOGUE,physical_adoption=False))
 events=[]
 for index,R in enumerate(Rvalues):
  CONTEXT.update(stage='NEW_direct_original_reference',index=index,R=R,radial_side='left',vertical_side='upper')
  reference=direct43_original_owned_reference(r,z,potential,shift,R=R,radial_side='left',admission=adm,keep=keep,label='DIRECT_reference_%02d'%index)
  words={n+'_'+w:a for n,pair in reference['reference'].items() if isinstance(pair,tuple) for w,a in zip(('hi','lo'),pair)}
  axisym=all(np.all(pair[w][3]==0) for pair in (reference['reference']['N_jets'],reference['reference']['beta_jets']) for w in (0,1));words['axisymmetric_gauge_phi_exact_zero']=np.asarray(axisym,dtype=np.bool_)
  ref=complete('REFERENCE_EVENT',words,dict(index=index,R=R,Z=0.,radial_side='left',vertical_side='upper',radius_contact={n:v.tolist() if isinstance(v,np.ndarray) else v for n,v in reference['radius_contact'].items()},reference_event_provenance=adm['reference_event_provenance'],finite_reference_provenance=adm['finite_reference_provenance'],axisymmetric_gauge_phi_exact_zero=axisym,stationary_seed_adopted_as_current=False,physical_adoption=False))
  CONTEXT.update(stage='NEW_direct_baseline_TOTAL_rate',index=index,R=R,radial_side='left',reference_event=ref)
  rate=direct43_baseline_TOTAL_rate(r,z,metric,increment,R=R,radial_side='left',admission=adm,keep=keep,label='DIRECT_rate_%02d'%index)
  payload={n+'_'+w:a for n,pair in (('baseline_TOTAL_hdot',rate['h_dot']),('original47969_hdot',rate['original_current_hdot']),('original60363_correction_hdot',rate['original_admitted_increment'])) for w,a in zip(('hi','lo'),pair)}
  event=complete('BASELINE_EVENT',payload,dict(index=index,R=R,Z=0.,radial_side='left',vertical_side='upper',reference_event=ref,original_point_first_order=True,node_sum_then_lift_equivalence_claimed=False,Gauss_rate_interpolated=False,KADM_plus_Lie_inverse_used=False,physical_adoption=False));events.append(dict(index=index,R=R,reference_event=ref,baseline_event=event))
 assert len(RECORDS)==87 and not CHECKS
 return dict(status='DIRECT43_ORIGINAL_BASELINE_FIELDS_PREPARED_UNQUALIFIED',input=header,events=events,roles=87,controls=0,baseline_only=True,coupled_or_finite_correction_required_for_baseline_preparation=False,new_coupled_increment_not_evaluated=True,physical_circle_or_new43_prediction_earned=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for v in SELECTED_PROOF) and all(v is not None for q in TERMINALS.values() for pin in q.values() for v in pin),'Independent FULL review and root-selected original seals required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=dict(INPUTS),terminal_bindings=TERMINALS,selected_proof=SELECTED_PROOF,events=43,planned_roles=87,controls=0,source_law_changed=False,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=prepare(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}),dict(kind='unfinished_direct_original_baseline_fields',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
