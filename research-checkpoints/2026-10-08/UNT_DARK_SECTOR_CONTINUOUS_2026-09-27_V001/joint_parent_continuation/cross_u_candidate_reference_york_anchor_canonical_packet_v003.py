"""HELD NEW reference-branch York target and canonical epsilon packet.
At rho/W/t=0 the owned literal Pi remains the authoritative target. Four NEW
FY128 evaluations are numerical reconstruction contacts, not new free priors.
No old current/EOS/action/normal/CMC/York projection or solver is replayed.
Root alone binds the future CLOSED phase-normal join and executes a successor.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V003'
DRIVER_PROTOCOL='CROSS_U_CANDIDATE_REFERENCE_YORK_ANCHOR_CANONICAL_PACKET_V001.md'
PROTOCOL_SHA='4a0d26b049aa5999d7dfdc58d09410a5f81f14c6757710cb3f4dbd93f46fceb7'
JOIN_SOURCE=('cross_u_fixed_geometry_phase_normal_canonical_value_join_v002.py', '28e8cb501975c4fd20660ce022a54c0ab9c677dc00108399e76fe023f870755b')
JOIN_RESULT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RESULT.json', 'd382c372ac74e581beee2a491ae4a143cf24a6c73dd87fd0565044a6041fd9ed', 'FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED')
JOIN_RECEIPT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RECEIPT.json', '2f331b3a45b1e5dfe25114ab4d3f0d90528029b9d3d060c2809c1d691f7d31b6', 'CLOSED')
JOIN_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_V001.json', '3bc8ea72625fbcda04440f9bc80dfde01b1aeb30804a555b84771c2b899651ae', 'ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_VERIFIED')
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_candidate_shared_canonical_action_blocks_v001.py':'4ffdbf60dde14d9b87a7cb947dca7f61ec7e4ffe456653aed5298de27dbd59ee',
 'author_fragment_initial_york_five_field_target_admission_v001.txt':'bfe2cb3e201dd5fb1ce23c59a269055bc91be03614a76bdc8f92946b708eb31e',
 'author_fragment_fixed_geometry_phase_normal_join_v001.py':'7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9',
 'cross_u_candidate_literal_phase_charge_response_v002.py':'887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6',
 'author_fragment_initial_york_trace_target_response_v001.py':'71fda02b76e03c5ac4fe917f0514a3f13e60ec15b9aad21610045fbe40fe71e1',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d'}
REFERENCE_RESULT=('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001_RESULT.json','6979db89e7612ddda54e9b4cadaa565263b99d02c2eca24324a695e0fc92a2bc')
REFERENCE_RECEIPT=('CROSS_U_CANONICAL_NODAL_METRIC_RATE_DD_COORDINATES_V001_RECEIPT.json','a11e491baa8950d8dbedf5a0470aea1604cc0366e008fed8fc6154fd649f123d')
REFERENCE_PROOF=('READONLY_DD_NODE_COORDINATE_WORDS_V001_RESULT.json','ce19e353075341a82b475f019cd3fb6ca6f630868001b479b5aee1760c9bb8fc')
CANONICAL_PREFIX='NEW_reference_anchor'
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert h is not None and hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(IO_PARENT,names),IO_PARENT,'exec'),globals());initialize_io()
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,{'recheck'}),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']

def initialize_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','pack_fields','unpack_fields','collapse','fields_from_pair'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','native_mask','metric_mask','dd_metric_F','dd_metric_scatter'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
  for n in names:setattr(P,n,SCOPE[n])
 SCOPE.update(C=1.98,ALPHA=.02/1.98,ELL=.1);P.C=1.98;P.LINEAR_TOL=1e-10
 choices=(('author_fragment_finite_york_geometry_target_v001.py',None),('author_fragment_candidate_shared_canonical_action_blocks_v001.py',{'cs_keep','cs_york_covector_six'}),('author_fragment_initial_york_five_field_target_admission_v001.txt',{'five_field_target_admission'}),('author_fragment_fixed_geometry_phase_normal_join_v001.py',{'phase_join_closed','fixed_geometry_phase_normal_join_admission'}),('cross_u_candidate_literal_phase_charge_response_v002.py',{'bind_record'}),('author_fragment_initial_york_trace_target_response_v001.py',{'trace_target_reference_scores'}),('author_fragment_exact_exponent_two_product_v003.py',None))
 for file,names in choices:
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if names is None else names
  if file=='author_fragment_fixed_geometry_phase_normal_join_v001.py':
   for n in tree.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith(('NORMAL_','FINITE_')):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals()['PHASE_NORMAL_JOIN_AUTHOR_DRAFT']=False;globals()['PHASE_NORMAL_JOIN_AUTHORING_IN_PROGRESS']=False
 install_exact_exponent_product(SCOPE,P,keep,'NEW_anchor_exact_exponent_product')

def anchor_admission():
 assert all(x is not None for q in (JOIN_SOURCE,JOIN_RESULT,JOIN_RECEIPT,JOIN_CLOSURE_PROOF) for x in q)
 join,jrc=phase_join_closed(JOIN_SOURCE,JOIN_RESULT,JOIN_RECEIPT,JOIN_CLOSURE_PROOF);jc=join['case'];sources=fixed_geometry_phase_normal_join_admission();_,owned=five_field_target_admission()
 assert jc['normal_terminal']==json.loads(json.dumps(sources['normal_terminal'])) and jc['finite_phase_terminal']==json.loads(json.dumps(sources['finite_terminal']))
 assert jc['mechanical_current_CMC_and_test_R_Z_t_words_copied_by_action_invariance'] is True and jc['original_targets_and_epsilon_unchanged'] is True and jc['new_compact_chi_or_configuration_JVP'] is False
 assert jc['original_input']==thin(sources['input']) and jc['original_basis']==thin(sources['basis']) and jc['old_loads']==thin(sources['loads']) and jc['new_phase_current']==thin(sources['current'])
 joined=bind_record(jc['readout']);assert joined in join['checkpoints'] and joined['metadata']['owner']==join['owner'] and joined['metadata']['kind']=='NEW_fixed_geometry_phase_updated_four_normal_and_canonical_value_join'
 for n in ('file','commit_file'):assert jrc['output_sha256'][joined[n]]==joined['sha256' if n=='file' else 'commit_sha256']
 assert sources['basis']['metadata']['reference']==sources['input']['metadata']['refs']['basis'] and thin(sources['input']['metadata']['refs']['basis'])==owned['shared_basis_ref']
 assert [thin(x['state']) for x in sources['columns']]==[q['metadata']['candidate_state'] for q in json.loads(P.path(NORMAL_RESULT[0]).read_text())['case']['columns']]
 assert sources['input']['metadata']['rho']==0 and [thin(x) for x in sources['input']['metadata']['refs']['pilots']]==owned['pilot_refs']
 for q in (REFERENCE_RESULT,REFERENCE_RECEIPT,REFERENCE_PROOF):bind(*q)
 r=json.loads(P.path(REFERENCE_RESULT[0]).read_text());rc=json.loads(P.path(REFERENCE_RECEIPT[0]).read_text());proof=json.loads(P.path(REFERENCE_PROOF[0]).read_text())
 assert r['owner']==rc['owner'] and r['owner']['pid']==47969 and r['owner']['source_sha256']==PINS[list(PINS)[0]]
 assert rc['status']=='CLOSED' and rc['result_sha256']==REFERENCE_RESULT[1] and rc['error_sha256'] is None and proof['status']=='SAVED_DD_NODE_COORDINATE_WORDS_PASS' and proof['canonical_and_weak_trace_admitted'] is True
 assert proof['parent_terminal']['pid']==47969 and proof['parent_terminal']['result_sha256']==REFERENCE_RESULT[1] and proof['parent_terminal']['receipt_sha256']==REFERENCE_RECEIPT[1]
 compatibility=bind_record(r['case']['compatibility']);basis=bind_record(compatibility['metadata']['basis_ref']);assert thin(basis)==owned['shared_basis_ref']
 for n in ('file','commit_file'):assert rc['output_sha256'][compatibility[n]]==compatibility['sha256' if n=='file' else 'commit_sha256']
 assert compatibility['metadata']['canonical_and_trace_admitted'] is True and compatibility['metadata']['physical_adoption'] is False
 return dict(sources=sources,owned=owned,join=joined,join_terminal=(JOIN_SOURCE,JOIN_RESULT,JOIN_RECEIPT,JOIN_CLOSURE_PROOF),compatibility=compatibility,reference_basis=basis)

def anchor_pair(data,name,label):
 x=tuple(data[name+'_'+w].copy() for w in ('hi','lo'));keep(label+'_both_words',np.stack(x).copy());return fy_keep(label,x,keep)

def anchor_scores(residual,native_reference,canonical_reference,metric_reference,scales,label):
 scores,norms,zero=trace_target_reference_scores(residual,native_reference,canonical_reference,metric_reference,scales,label)
 fields=[P.unpack_fields(a,False) for a in residual]
 for row,field in ((0,0),(1,0),(2,1)):
  if zero[row] and any(np.any(f[field]!=0) for f in fields):scores[row]=1.
 keep(label+'_exact_zero_reference_authoritative_scores',scores.copy());return scores,norms,zero

def anchor_packet(refs):
 src,owned=refs['sources'],refs['owned'];basis=read(src['basis'],('R','dv','hats'));old_geometry=read(owned['input'],('R','dv','hats'))
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 for n in basis:keep('original_basis_'+n,basis[n]);keep('owned_reference_basis_'+n,old_geometry[n]);assert np.array_equal(basis[n],old_geometry[n])
 original=read(refs['compatibility'],('original_rhs','current_Pn'));scale_data=read(refs['reference_basis'],('native_scale','metric_scale'))
 for n,a in original.items():keep('original_reference_'+n,a)
 for n,a in scale_data.items():keep('original_reference_'+n,a);assert np.all(a>0)
 maps=read(owned['maps'],('L_maps_hi','L_maps_lo','L_map_operation_envelope'))
 for n,a in maps.items():keep('owned_reference_'+n,a)
 inp=P.checkpoint('INPUT',arrays(AVAILABLE),dict(kind='fixed_literal_owned_reference_York_anchor_sources',join=thin(refs['join']),join_terminal=refs['join_terminal'],original_input=thin(src['input']),basis=thin(src['basis']),reference_trace_columns=[thin(q) for q in owned['columns']],reference_maps=thin(owned['maps']),owned_reference_prior_readout=owned['prior_readout_ref'],old_weak_Pm_nominal_bridge_not_refitted=True,original_compatibility=thin(refs['compatibility']),original_reference_basis=thin(refs['reference_basis']),rho_W_t_all_exact_zero=True,authoritative_target='unchanged Pi_owned exact reference branch',TT_or_exterior_prior_refitted=False,physical_adoption=False));clear_current();targets=[];comparisons=[];point_bounds=[];phase_carries=[];columns=[]
 for iq,(trace,source) in enumerate(zip(owned['columns'],src['columns'])):
  CONTEXT.update(stage='NEW_reference_anchor_column',column=iq);prefix='column_%d_'%iq
  names=tuple(prefix+n+'_'+w for n in ('total_canonical_tensor_density','trace_subtracted_canonical_density','total_canonical_trace_density') for w in ('hi','lo'))+('input_chart_h','input_chart_ih','input_chart_sqrt_h')
  data=read(trace,names);state=read(source['state'],('completed_candidate_c_h','NEW_reference_input_geometry_h_spatial_jets_hi','NEW_reference_input_geometry_h_spatial_jets_lo'))
  for n,a in data.items():keep('unchanged_owned_'+n,a)
  for n,a in state.items():keep('unchanged_STATE_'+n,a)
  assert np.array_equal(data['input_chart_h'],state['completed_candidate_c_h'])
  phase_prefix='NEW_finite_phase_column%d_NEW_invariant_'%iq;phase_names=tuple(phase_prefix+n+'_'+w for n in ('literal_canonical_density','literal_temporal_H') for w in ('hi','lo'))+(phase_prefix+'H_operation_envelope',)
  phase=read(source['new'],phase_names)
  assert source['new']['metadata']['new_H_strictly_positive'] is source['new']['metadata']['new_H_resolved_positive'] is True
  for n,a in phase.items():keep('copied_updated_phase_'+n,a)
  phase_carries.append(dict(p=anchor_pair(phase,phase_prefix+'literal_canonical_density','copied_updated_phase_p'),H=anchor_pair(phase,phase_prefix+'literal_temporal_H','copied_updated_phase_H'),eH=phase[phase_prefix+'H_operation_envelope'].copy()))
  Pi=anchor_pair(data,prefix+'total_canonical_tensor_density','NEW_anchor_Pi_owned');T=anchor_pair(data,prefix+'trace_subtracted_canonical_density','NEW_anchor_T_owned');tau=anchor_pair(data,prefix+'total_canonical_trace_density','NEW_anchor_tau_owned')
  sl=slice(iq*3784,(iq+1)*3784);L=tuple(maps['L_maps_'+w][sl].copy() for w in ('hi','lo'));fy_keep('NEW_anchor_L_maps',L,keep);keep('NEW_anchor_L_map_operation_envelope',maps['L_map_operation_envelope'][sl].copy())
  reference=dict(h=data['input_chart_h'],h_spatial_jets=tuple(state['NEW_reference_input_geometry_h_spatial_jets_'+w] for w in ('hi','lo')),ih_owned=data['input_chart_ih'],mu_owned=data['input_chart_sqrt_h'],target_raising_inverse=data['input_chart_ih'],Pi_owned=Pi,T_owned=T,tau_owned=tau,L_maps=L)
  rho=P.a_dd(np.zeros(3784));gradient=P.a_dd(np.zeros((3784,2)));W=P.a_dd(np.zeros((3784,3,3)));t=P.a_dd(np.zeros(3784));direction=dict(rho=rho,rho_gradient=gradient,W_jet=W,t=t)
  out=finite_york_geometry_target(reference,rho,gradient,W,t,direction,keep,'NEW_FY_reference_anchor');assert all(np.array_equal(a,b) for a,b in zip(out['h'],P.a_dd(reference['h'])))
  assert all(np.all(a==0) for n in ('delta_h','delta_ih','delta_mu','delta_target','delta_tau') for a in out[n])
  target=tuple(a.copy() for a in Pi);FY=out['target'];bridge=fy_keep('NEW_FY_target_minus_authoritative_owned_Pi',P.a_sub(FY,target),keep)
  mag=lambda a:abs(a[0])+abs(a[1]);hmag=abs(reference['h']);Im=mag(out['ih']);kappa=tuple(AVAILABLE['NEW_FY_reference_anchor_candidate_inverse_trace_'+w].copy() for w in ('hi','lo'));klo=kappa[0]-abs(kappa[1]);keep('NEW_FY_envelope_denominator_lower',klo.copy());assert np.all(klo>0)
  # At the exact reference branch lambda=1. Bound every base/anchor/T/trace
  # operation before cancellation; this is a construction contact only.
  tau_bound=np.sum(hmag*mag(Pi),axis=(1,2));base_bound=mag(T)+Im*((tau_bound+np.sum(hmag*mag(T),axis=(1,2)))/klo)[:,None,None]
  anchor_bound=mag(Pi)+base_bound;Tbound=mag(T)+anchor_bound;envelope=mag(Pi)+Tbound+Im*((tau_bound+np.sum(hmag*Tbound,axis=(1,2)))/klo)[:,None,None]
  keep('NEW_FY_reference_anchor_uncancelled_envelope',envelope.copy());P.check('NEW_FY_reference_anchor_point_'+str(iq),bridge[0]+bridge[1],np.zeros_like(envelope),envelope)
  fy_keep('authoritative_exact_reference_target',target,keep);columns.append(P.checkpoint('TARGET_COLUMN',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_FY128_zero_coordinate_reconstruction_with_unchanged_owned_Pi_target',column=iq,input=thin(inp),state=thin(source['state']),current_finite_phase=thin(source['new']),updated_phase_H_p_eH_copied_only=True,new_phase_diagonal_or_cache_prepared=False,trace_reference=thin(trace),reference_maps=thin(owned['maps']),rho_W_t_exact_zero=True,target_authority='Pi_owned both original words unchanged',FY_reconstruction_is_comparison_only=True,owned_T_is_fixed_total_trace_subtracted_data_not_new_TT_prior=True,new_configuration_JVP=False,physical_adoption=False)));targets.append(target);comparisons.append(FY);point_bounds.append(envelope);clear_current()
 point=tuple(np.concatenate([a[w] for a in targets]) for w in (0,1));FYpoint=tuple(np.concatenate([a[w] for a in comparisons]) for w in (0,1));fy_keep('NEW_owned_reference_full_Pi_target',point,keep);fy_keep('NEW_FY_full_comparison_target',FYpoint,keep)
 six=cs_york_covector_six(point,keep,'NEW_authoritative_reference_six');FYsix=cs_york_covector_six(FYpoint,keep,'NEW_FY_comparison_six');target_metric=fy_keep('NEW_authoritative_prepared_metric_weak_target',P.dd_metric_scatter(six,basis,keep),keep);FYmetric=fy_keep('NEW_FY_comparison_metric_weak_target',P.dd_metric_scatter(FYsix,basis,keep),keep)
 weak_bridge=fy_keep('NEW_FY_metric_weak_target_bridge',P.a_sub(FYmetric,target_metric),keep)
 e=np.concatenate(point_bounds);esix=np.stack([e[:,i,j] if i==j else e[:,i,j]+e[:,j,i] for i,j in ((0,0),(1,1),(2,2),(0,1),(0,2),(1,2))],-1);ew=P.dd_metric_scatter(P.a_dd(esix),basis,keep);bound=abs(ew[0])+abs(ew[1]);keep('NEW_FY_weak_target_bridge_operation_envelope',bound);P.check('NEW_FY_reference_anchor_weak_bridge',weak_bridge[0]+weak_bridge[1],np.zeros_like(bound),bound)
 phase_current=read(src['current'],tuple('NEW_finite_phase_NEW_finite_literal_point_density_'+w for w in ('hi','lo')))
 for n in ('p','H'):
  carried=tuple(np.concatenate([q[n][w] for q in phase_carries]) for w in (0,1));fy_keep('copied_updated_phase_full_'+n,carried,keep)
  if n=='p':assert all(np.array_equal(carried[w],phase_current['NEW_finite_phase_NEW_finite_literal_point_density_'+word]) for w,word in enumerate(('hi','lo')))
 keep('copied_updated_phase_full_eH',np.concatenate([q['eH'] for q in phase_carries]));phase_carries.clear()
 current_names=tuple(n+'_'+w for n in ('value_native_current','value_metric_current','actual_native_canonical_target_residual','actual_metric_canonical_target_residual') for w in ('hi','lo'))+tuple(n for n in src['loads']['metadata']['schema'] if n.startswith('prior_signed_bridge_'));current=read(src['loads'],current_names)
 joined=read(refs['join'],tuple(refs['join']['metadata']['schema']))
 for n,a in joined.items():keep('copied_phase_normal_join_'+n,a)
 for n,a in current.items():keep('copied_completed_load_'+n,a);assert np.array_equal(a,joined['NEW_phase_normal_join_unchanged_load_'+n])
 native_prior=P.a_dd(original['current_Pn']);assert np.array_equal(current['prior_signed_bridge_native_original_target'],original['current_Pn'])
 values=dict(native=anchor_pair(current,'value_native_current',CANONICAL_PREFIX+'_current_candidate_weak_native'),metric=anchor_pair(current,'value_metric_current',CANONICAL_PREFIX+'_current_candidate_weak_metric'))
 priors=dict(native=native_prior,metric=target_metric);epsilon={}
 for n in ('native','metric'):
  fy_keep(CANONICAL_PREFIX+'_unchanged_or_prepared_target_'+n,priors[n],keep);epsilon[n]=fy_keep(CANONICAL_PREFIX+'_target_minus_current_epsilon_'+n,P.a_sub(priors[n],values[n]),keep);fy_keep(CANONICAL_PREFIX+'_current_minus_target_'+n,P.a_sub(values[n],priors[n]),keep)
 nominal=P.a_dd(current['prior_signed_bridge_metric_original_target']);fy_keep(CANONICAL_PREFIX+'_current_minus_original_nominal_metric_target',P.a_sub(values['metric'],nominal),keep);fy_keep(CANONICAL_PREFIX+'_prepared_minus_original_nominal_metric_target',P.a_sub(target_metric,nominal),keep)
 rhs=tuple(P.pack_fields(epsilon['native'][w],epsilon['metric'][w]) for w in (0,1));fy_keep(CANONICAL_PREFIX+'_packed_target_minus_current_RHS',rhs,keep);metric_ref=epsilon['metric'][0]+epsilon['metric'][1];keep('NEW_metric_RHS_norm_only_reference',metric_ref);fy_keep('NEW_metric_reference_readout_defect',P.a_sub(epsilon['metric'],P.a_dd(metric_ref)),keep)
 nref=P.unpack_fields(original['original_rhs'],False)[0];scales=(scale_data['native_scale'],scale_data['metric_scale']);scores,norms,zero=anchor_scores(rhs,nref,original['current_Pn'],metric_ref,scales,'NEW_initial_zero_correction_original_six')
 canonical=P.checkpoint('CANONICAL',arrays({**RAW,**AVAILABLE}),dict(kind='NEW_exact_reference_prepared_target_and_current_canonical_epsilon',input=thin(inp),columns=[thin(q) for q in columns],phase_normal_canonical_join=thin(refs['join']),canonical_prefix=CANONICAL_PREFIX,target_authority='Pi_owned exact reference branch rho0/W0/t0',original_native_affine_and_canonical_reference=thin(refs['compatibility']),reference_basis=thin(refs['reference_basis']),six_reference_scores=scores.tolist(),reference_norms_thresholds=norms.tolist(),zero_reference_flags=zero,initial_mechanical_original_six_rows_admitted=bool(np.all(scores<=P.LINEAR_TOL)),mechanical_current_unchanged_under_phase_update=True,configuration_contact_and_varying_York_target_JVP_earned=False,current_finite_phase_columns=[thin(q['new']) for q in src['columns']],updated_phase_H_p_eH_copied_only=True,new_phase_diagonal_or_cache_prepared=False,nominal_metric_prior_is_comparison_only=True,original_native_and_literal_phase_targets_unchanged=True,canonical_or_normal_CMC_physical_adoption=False,physical_adoption=False))
 assert len(RECORDS)==6 and len(CHECKS)==5 and all(c['passed'] for c in CHECKS)
 return dict(status='REFERENCE_YORK_ANCHOR_TARGET_AND_CANONICAL_EPSILON_MEASURED',input=inp,columns=columns,canonical=canonical,phase_normal_join=thin(refs['join']),original_basis=thin(src['basis']),original_input=thin(src['input']),old_loads=thin(src['loads']),original_canonical_target_refs=src['input']['metadata']['refs']['canonical_columns'],canonical_prefix=CANONICAL_PREFIX,original_six_reference_scores=scores.tolist(),initial_mechanical_original_six_rows_admitted=bool(np.all(scores<=P.LINEAR_TOL)),prepared_metric_target_is_exact_owned_reference=True,free_prior_or_target_refitted=False,new_varying_target_JVP=False,updated_phase_H_p_eH_copied_only=True,new_phase_diagonal_or_cache_prepared=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(x is not None for q in (JOIN_SOURCE,JOIN_RESULT,JOIN_RECEIPT,JOIN_CLOSURE_PROOF) for x in q),'Root release and naturally CLOSED join required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  initialize_helpers();refs=anchor_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,join_terminal=refs['join_terminal'],reference_authority='Pi_owned at rho/W/t exactly zero',new_FY_reconstructions=4,new_mechanical_action_or_solver_calls=0,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=anchor_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],case['original_six_reference_scores'],rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_reference_anchor_target_and_canonical_operands',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
