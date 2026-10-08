"""HELD NEW139 mechanical gauge64 preparation; root execution only.
Authentic point TOTAL inputs are hydrated from CLOSED saved stages. Exactly64
NEW mechanical ports; no old producer/current/EOS/port or nodal TOTAL replay.
Fullweak/phase inheritance/adjoint feedback and physical qualification external.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_NEW139_MECHANICAL_GAUGE_CURRENT_PREPARATION_V005'
DRIVER_PROTOCOL='NEW139_MECHANICAL_GAUGE_CURRENT_PREPARATION_V004.md'
PROTOCOL_SHA='3fb3ad16f9a9a23c9e9cf0e8d79f72756ab82b2d2f2d11b8dba09b4a2d973c56'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
FINITE_SOURCE=('saved_fixed_geometry_total_rate_column_readout_recovery_v002.py', '06e5ea35f657ee14624740435bf9e36f1ee84e812dad9adb28304bd623c59075')
FINITE_RESULT=('SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V002_RESULT.json', 'd12115e9b21dca3af5b9be9655385153864752f2364274817ff10e84472d9390', 'FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED')
FINITE_RECEIPT=('SAVED_FIXED_GEOMETRY_TOTAL_RATE_COLUMN_READOUT_RECOVERY_V002_RECEIPT.json', '54866112b1ffc45629d08b6c3bda09339184349b46178ad0584966f6dfcc4b21', 'CLOSED')
FINITE_CLOSURE_PROOF=('READONLY_NATURAL_CLOSED_SAVED_TOTAL_RATE_READOUT_RECOVERY_SUCCESS_SEALS_V001.json', 'a12ae17f08257468eea1740316c3a8da269abcec822d0cfb650d155f902c24bc', 'READONLY_NATURAL_CLOSED_SAVED_TOTAL_RATE_READOUT_RECOVERY_SUCCESS_SEALS_VERIFIED')
LITERAL_SOURCE=('cross_u_refreshed_total_rate_literal_gradient_contacts_v004.py', 'ea5707d13eb7ab78fba13db6a40ce67768c206a69d47e46643e9545fdb696fa1')
LITERAL_RESULT=('CROSS_U_REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_CONTACTS_V004_RESULT.json', '64d063bd4e1266e16a1d0fb60efa5e43b7bd69f40d801561540228f8fc3e691e', 'REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_AND_eL_CONTACTS_PASS')
LITERAL_RECEIPT=('CROSS_U_REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_CONTACTS_V004_RECEIPT.json', '869dbf59a4f3d2e5a0f5e1ae31b07964dd4b942401404af17ac8327dfc5c2ea6', 'CLOSED')
LITERAL_PROOF=('READONLY_NATURAL_CLOSED_REFRESHED_TOTAL_RATE_LITERAL_EL_SUCCESS_SEALS_V001.json', '1c705d3a9326f500b43bb4bb3096fd3102655f9104af59d522c7c45be88f280a', 'READONLY_NATURAL_CLOSED_REFRESHED_LITERAL_EL_SEALS_VERIFIED')
FINITE_STATUS='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED'
SELECTED22_PROOF=('NATIVE_CLOSED_FIXED_RATE22_SELECTED_INPUT_SEALS_V001.json','b92fdceb198abded8421d146910347408f00873ce74e7b8ea5d828cc4d0e1291','ROOT_CLOSED_FIXED_RATE22_SELECTED_INPUT_SEALS_VERIFIED')
FIXED_BINDING=('NATIVE_FIXED_GEOMETRY_TOTAL_RATE_STATE_MINIMAL_PACKET_V002.json','4c6312d4168c81e77208447da7ed58aa1904b98195eefd9ea1830a1eab103031')
DECLARED_CELLS=((1,0),(30,17),(85,21),(41,43))
CHART_FAMILIES=('g','hi','U','z','dg','du','dz','Ga','dens','K','metric_EH_density')
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};DESCRIPTIONS={};REFERENCE_METADATA=[]
SNAMES=('g', 'hi', 'U', 'z', 'uc', 'P', 'Z', 'r', 'z2', 'f', 'phi', 'omega', 'xi', 'w', 'R', 'Z_coordinate')
CNAMES=('h', 'ih', 'N', 'beta', 'u', 'up', 'gamma', 'dens', 'sqrt_h', 'JU', 'JzU', 'Jzz', 'Uh', 'zh', 'embed')
MATERIAL=('B', 'GC', 'ALPHA', 'ELL', 'C')
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py', '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json', '49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e', 'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json', 'c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64', 'CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json', '2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9', 'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_candidate_gauge_registered_current_contact_v001.py': 'ac0502f41c6ad04208f5ef5610d43b3e11064a4b66eb73d076d43c959ffb0cdd', 'author_fragment_NEW139_mechanical_gauge_preparation_v003.py': '244a0d50f89b72dbc2447eba66939ddcd5cd6a2b94483bb7595c0a1e41249dc7', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_gauge_chart_firstjet_fraction_reference_v001.py': '7f844b6bb2bf0f8e63b151b0d35c3e936f42f3ed0d8c23ae550191719ac6d854', 'cross_u_candidate_gauge_registered_current_controls_v001.py': '298adc0381958db05c5c5276ded929b6ad7bdb948f828166d007ace27be29896', 'author_fragment_fixed_geometry_total_rate_state_v002.py': 'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d'}
PINS['author_fragment_fixed_rate_inherited_success_admission_v001.py']='8da980eeb2c429b8612cd0c69be37490b3efa661978ecbedb859f03bce761687'

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)

def closed(source,result,receipt,proof):
 assert all(x is not None for q in (source,result,receipt,proof) for x in q),'Natural closure must be bound by root before any packet read'
 for q in (source,result,receipt,proof):bind(q[0],q[1])
 assert P.path(result[0]).stat().st_size<=128*1024*1024,'Larger result needs a separately reviewed bounded projection'
 r=json.loads(P.path(result[0]).read_text());rc=json.loads(P.path(receipt[0]).read_text());pr=json.loads(P.path(proof[0]).read_text())
 assert r['status']==result[2] and rc['status']==receipt[2] and pr['status']==proof[2]
 assert r['owner']==rc['owner']==pr['owner'] and r['owner']['source_sha256']==source[1]==pr['source_sha256']
 assert rc['result_sha256']==result[1]==pr['result_sha256'] and rc.get('error_sha256') is None and pr['receipt_sha256']==receipt[1]
 assert pr['naturally_closed'] is True and pr['exit_code']==0 and pr['all_success_role_seals_verified'] is True
 assert r['qualification']==rc['qualification'] and r['qualification'] and all(v is False for v in r['qualification'].values())
 assert all(c['passed'] is True for c in r['controls'])
 return r,dict(rc,_fixed_rate_inherited_success=fixed_rate_inherited_success_admission(r,rc,bind))

def record(r,rc,ref):
 bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text());assert q['file']==ref['file'] and q['sha256']==ref['sha256']
 q=dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256']);md=q['metadata']
 seals=fixed_rate_record_seals(r,rc,q);assert md['failed'] is False and md['qualification'] and all(v is False for v in md['qualification'].values())
 assert any(thin(x)==thin(q) for x in r['checkpoints']) and ('metadata' not in ref or ref['metadata']==md)
 for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert seals[n]==h
 return q

def stage(r,rc,kind,column=None):
 found=[q for q in r['checkpoints'] if q['metadata']['kind']==kind and (column is None or q['metadata'].get('column')==column)]
 assert len(found)==1,(kind,column);return record(r,rc,found[0])

def selected(q,names,label):
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names),label
 bind(q['file'],q['sha256']);bind(q['commit_file'],q['commit_sha256']);data=read(q,names)
 for n,a in data.items():keep(label+'_'+n,a);s=q['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True
 return data

def saved_pair(data,prefix):return tuple(data[prefix+'_'+w].copy() for w in ('hi','lo'))

def seal(role,metadata):
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)));clear_current();DESCRIPTIONS.clear();return thin(q)

def initialize():
 global np
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'},globals());initialize_io()
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum'}
 definitions(list(PINS)[0],base,SCOPE);definitions(list(PINS)[1],primitive,SCOPE)
 for n in base|primitive|set(MATERIAL):setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|set(MATERIAL)})
 choices=(('author_fragment_finite_york_geometry_target_v001.py',None),('author_fragment_exact_exponent_two_product_v003.py',None),('author_fragment_finite_york_spacetime_first_jets_v001.py',None),('author_fragment_finite_candidate_configuration_contact_v001.py',{'fc_anchor','fc_quotient','fc_square_root','fc_symmetric_contact'}),('author_fragment_compact_metric_contact_momenta_v002.py',None),('author_fragment_candidate_gauge_registered_current_contact_v001.py',{'fgc_connection','candidate_gauge_raw_action_contact'}),('author_fragment_NEW139_mechanical_gauge_preparation_v003.py',None),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_provider_admission','candidate_point_cache_names'}),('author_fragment_gauge_chart_firstjet_fraction_reference_v001.py',None),('cross_u_candidate_gauge_registered_current_controls_v001.py',{'rational_control','gauge_rational_control','select_gauge_points'}),('author_fragment_fixed_rate_inherited_success_admission_v001.py',{'fixed_rate_inherited_success_admission','fixed_rate_record_seals'}))
 for file,names in choices:definitions(file,names,globals())
 for file,prefixes in (('author_fragment_candidate_chunk_point_block_provider_v001.py',('POINT_',)),('author_fragment_NEW139_mechanical_gauge_preparation_v003.py',('NEW139_GAUGE_SOURCE_PINS','NEW139_GAUGE_ROLES'))):
  for n in ast.parse((BASE/file).read_text()).body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith(prefixes):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(POINT_PROVIDER_AUTHOR_DRAFT=False,POINT_PROVIDER_AUTHORING_IN_PROGRESS=False,GAUGE_CURRENT_AUTHOR_DRAFT=False,GAUGE_CURRENT_AUTHORING_IN_PROGRESS=False,NEW139_GAUGE_AUTHOR_DRAFT=False,NEW139_GAUGE_AUTHORING_IN_PROGRESS=False,GAUGE_CHART_REFERENCE_AUTHOR_DRAFT=False,GAUGE_CHART_REFERENCE_AUTHORING_IN_PROGRESS=False,NEW139_GAUGE_FINITE_CLOSURE=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),NEW139_GAUGE_MECHANICAL_CACHE_CLOSURE=(MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF),NEW139_GAUGE_LITERAL_CLOSURE=(LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF))
 globals()['GAUGE_MECHANICAL_CORE']=candidate_gauge_raw_action_contact;globals()['candidate_gauge_raw_action_contact']=gauge_contact_with_context
 install_exact_exponent_product(SCOPE,P,keep,'NEW139_gauge_exact_product');globals()['a_prod']=P.a_prod
 assert P.a_mul.__globals__ is SCOPE and SCOPE['a_prod'] is P.a_prod
 for n in ('a_dd','a_slice','a_add','a_mul','a_stack','normal_pair_sum','a_transpose'):assert globals()[n] is SCOPE[n]
 for n in MATERIAL:assert getattr(P,n)==SCOPE[n]==globals()[n]


def gauge_contact_with_context(candidate,geometry,gauge,covectors,mechanical,direction,reference,keep,label):
 prefix,port=label.rsplit('_row',1);row,jet=port.removesuffix('_NEW_mechanical').split('_jet');iq=int(prefix.rsplit('column',1)[1])
 assert 0<=iq<4 and 0<=int(row)<4 and 0<=int(jet)<4
 CONTEXT.update(stage='NEW139_mechanical_gauge_arithmetic',column=iq,row=int(row),jet=int(jet),label=label)
 return GAUGE_MECHANICAL_CORE(candidate,geometry,gauge,covectors,mechanical,direction,reference,keep,label)


def admission():
 finite,frc=closed(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF);literal,lrc=closed(LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF)
 fc,lc=finite['case'],literal['case'];assert fc['status']==FINITE_STATUS and fc['spatial_geometry_unchanged'] is fc['current99_and_physical6_fresh'] is fc['all16normal_ports_per_section'] is True and fc['physical_adoption'] is False
 assert lc['status']=='REFRESHED_TOTAL_RATE_LITERAL_GRADIENT_AND_eL_CONTACTS_PASS' and tuple(tuple(q) for q in lc['finite_terminal'])==(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF)
 fi=stage(finite,frc,'INPUT');out=record(finite,frc,fc['readout']);bridge=record(literal,lrc,lc['stationarity_bridge']);assert bridge['metadata']['finite_readout']==thin(out)
 for q in (SELECTED22_PROOF,FIXED_BINDING):bind(q[0],q[1])
 support=json.loads(P.path(SELECTED22_PROOF[0]).read_text());plan=json.loads(P.path(FIXED_BINDING[0]).read_text());assert support['status']==SELECTED22_PROOF[2] and support['plan']==dict(file=FIXED_BINDING[0],sha256=FIXED_BINDING[1])
 for n in ('all_selected_archive_bytes_verified','all_selected_COMMIT_bytes_verified','all_selected_owners_naturally_closed','all_selected_embedded_metadata_equal','all_selected_member_names_and_selected_headers_verified'):assert support[n] is True,n
 assert support['original_STATE0_failure'] and support['scientific_or_helper_functions_invoked'] is False
 mechanical=candidate_point_provider_admission(bind);pr=fi['metadata']['provenance'];assert pr['all_source_seals_authenticated'] is pr['original_fixed_references_verified'] is pr['correction_original_six_gates_admitted'] is True
 assert fc['original_targets']==pr['unchanged_original_targets'] and plan['closed_metadata']['original_canonical_target_refs']==pr['unchanged_original_targets']
 assert mechanical['original_basis']==plan['basis']['ref']
 cols=[]
 for iq in range(4):
  q={n:stage(finite,frc,n,iq) for n in NEW139_GAUGE_ROLES};state=plan['columns'][iq]['state']['ref'];assert state==q['BASELINE_COLUMN_INPUT']['metadata']['state']==pr['original_owned_TOTAL_time_words'][iq]==mechanical['caches'][iq]['metadata']['state']
  assert thin(q['RATE_STATE_COLUMN'])==fc['columns'][iq] and q['RATE_STATE_COLUMN']['metadata']['provenance']==pr['columns'][iq]
  rows=[r for r in support['records'] if r['role']=='STATE' and r['ref']==state];assert len(rows)==1 and rows[0]['failed'] is False and rows[0]['qualification_all_false'] is True
  bind(state['commit_file'],state['commit_sha256']);original=json.loads(P.path(state['commit_file']).read_text());assert original['file']==state['file'] and original['sha256']==state['sha256'] and original['metadata']['owner']==rows[0]['owner'] and original['metadata']['column']==iq and original['metadata']['failed'] is False
  original=dict(original,commit_file=state['commit_file'],commit_sha256=state['commit_sha256']);q['fixed_state']=original;cols.append(q)
 fb=selected(fi,tuple('completed_INPUT_basis_'+n for n in ('R','dv','hats')),'NEW139_fixed_basis');mb=selected(mechanical['input'],tuple('registered_basis_'+n for n in ('R','dv','hats')),'same147_registered_basis')
 for n in ('R','dv','hats'):assert np.array_equal(fb['completed_INPUT_basis_'+n].view(np.uint64),mb['registered_basis_'+n].view(np.uint64))
 return dict(finite=finite,finite_receipt=frc,finite_input=fi,finite_readout=out,literal_bridge=bridge,mechanical=mechanical,columns=cols,fixed_support=SELECTED22_PROOF,original_state0_failure=support['original_STATE0_failure'],provenance=pr)


def hydrate_NEW139_mechanical_column(refs,iq):
 assert 0<=iq<4;q=refs['columns'][iq];tag='NEW139_mechanical_gauge_column%d'%iq;CONTEXT.update(stage='hydrate_NEW139_point_TOTAL',column=iq)
 names=tuple('completed_BASELINE_COLUMN_INPUT_candidate_'+f+'_'+n for f,ns in (('s',SNAMES),('c',CNAMES)) for n in ns)
 names+=tuple('completed_BASELINE_COLUMN_INPUT_'+f+'_'+n+'_'+w for f,ns in (('covectors',('u_jets','z_jets')),('gauge',('N_jets','beta_jets')),('reference',('E0',))) for n in ns for w in ('hi','lo'))
 names+=tuple('completed_BASELINE_COLUMN_INPUT_'+n+'_'+w for n in ('h_first','updated_phase_covector') for w in ('hi','lo'))
 data=selected(q['BASELINE_COLUMN_INPUT'],names,tag+'_baseline');s={n:data['completed_BASELINE_COLUMN_INPUT_candidate_s_'+n].copy() for n in SNAMES};c={n:data['completed_BASELINE_COLUMN_INPUT_candidate_c_'+n].copy() for n in CNAMES}
 gd=selected(q['fixed_state'],tuple('NEW_reference_input_geometry_h_'+w for w in ('hi','lo')),tag+'_true_fixed_h');h=saved_pair(gd,'NEW_reference_input_geometry_h');assert all(a.shape==(3784,3,3) for a in h)
 hf=saved_pair(data,'completed_BASELINE_COLUMN_INPUT_h_first');geometry=dict(h=h,h_spatial_jets=tuple(a[:,1:3].copy() for a in hf))
 fixed=dict(candidate=dict(s=s,c=c),geometry=geometry,gauge={n:saved_pair(data,'completed_BASELINE_COLUMN_INPUT_gauge_'+n) for n in ('N_jets','beta_jets')},covectors={n:saved_pair(data,'completed_BASELINE_COLUMN_INPUT_covectors_'+n) for n in ('u_jets','z_jets')},reference=dict(E0=saved_pair(data,'completed_BASELINE_COLUMN_INPUT_reference_E0')),updated_phase_pair=saved_pair(data,'completed_BASELINE_COLUMN_INPUT_updated_phase_covector'))
 prefixes={'RATE_STATE_INPUT':('completed_RATE_STATE_INPUT_',),'RATE_STATE_FIRST_JETS':('completed_RATE_STATE_FIRST_JETS_jets_','completed_RATE_STATE_FIRST_JETS_envelopes_'),'RATE_STATE_FEATURES':('completed_RATE_STATE_FEATURES_features_paired_',),'RATE_STATE_MOMENTA':('completed_RATE_STATE_MOMENTA_momenta_',),'RATE_STATE_COLUMN':('completed_RATE_STATE_COLUMN_new_TOTAL_time_words_','completed_RATE_STATE_COLUMN_new_point_current_')}
 packets={'BASELINE_COLUMN_INPUT':dict(ref=thin(q['BASELINE_COLUMN_INPUT']),metadata=q['BASELINE_COLUMN_INPUT']['metadata'],data=data)}
 for role,pre in prefixes.items():
  names=tuple(n for n in q[role]['metadata']['schema'] if n.startswith(pre));packets[role]=dict(ref=thin(q[role]),metadata=q[role]['metadata'],data=selected(q[role],names,tag+'_fresh_'+role))
 cache_ref=refs['mechanical']['caches'][iq];cd=selected(cache_ref,candidate_point_cache_names(cache_ref['metadata']),tag+'_same147');prefix=POINT_CACHE_PREFIX;pair=lambda n:saved_pair(cd,prefix+n);ep=prefix+'copied_positive_coefficient_'
 cache=dict(s={n:cd[prefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:cd[prefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),formal_Iu=pair('formal_I_times_u'),envelopes={n[len(ep):]:a.copy() for n,a in cd.items() if n.startswith(ep)},constants=cache_ref['metadata']['constants'],configuration_held=True,candidate_provenance=cache_ref['metadata']['candidate_provenance'])
 provenance=dict(column=iq,finite_closure=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),mechanical_cache_closure=(MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF),literal_closure=(LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF),finite_owner=refs['finite']['owner'],inherited_scientific_stage_context=refs['finite_receipt'].get('_fixed_rate_inherited_success'),selected_records={n:thin(q[n]) for n in NEW139_GAUGE_ROLES},source_pins=NEW139_GAUGE_SOURCE_PINS,material_constants={n:getattr(P,n) for n in MATERIAL},all_selected_NEW139_seals_authenticated=True,all_original_support_seals_authenticated=True,same_original_basis_verified=True,same_fixed_geometry_and_gauge_verified=True,same_fixed_mechanical_raw_E0_verified=True,original_targets_unchanged=True,fixed_state=thin(q['fixed_state']),fixed_support=SELECTED22_PROOF,literal_bridge=thin(refs['literal_bridge']),physical_adoption=False)
 def completed(kind,payload):
  capture_families('completed_MECHANICAL_GAUGE_INPUT_',dict(payload,geometry=geometry,updated_phase_pair=fixed['updated_phase_pair']))
  return seal('MECHANICAL_GAUGE_INPUT',dict(kind=kind,column=iq,source_records=provenance['selected_records'],fixed_state=provenance['fixed_state'],same_candidate_provenance=provenance,prepared_before_any_gauge_port=True,point_TOTAL_not_nodal_TOTAL=True,physical_adoption=False))
 column=prepare_NEW139_mechanical_gauge_column(fixed,packets,cache,provenance,keep,tag,completed);column['constants']={n:getattr(P,n) for n in MATERIAL};return column


def chart_controls(column,row,jet,payload,label):
 if (row,jet)!=(0,0):return
 indices=np.asarray([44*i+j for i,j in DECLARED_CELLS],dtype=np.int64);small=select_gauge_points(column,indices);result=select_gauge_points({'mechanical':payload['mechanical']},indices);direction=select_gauge_points(payload['direction'],indices);root=label+'_NEW_mechanical_'
 suffix={'h_beta':'h_beta_owned_representative','z0_quotient':'z0_quotient_owned_representative','shift_inverse':'shift_inverse_value_quotient','current_dg':'current_dg','current_du':'current_du'}
 for a in range(4):
  for n in ('U0_first','U0_second','z0_first','z0_second'):suffix[n+'_'+str(a)]=n+'_'+str(a)+'_value_quotient'
 locks=select_gauge_points({n:tuple(AVAILABLE[root+s+'_'+w].copy() for w in ('hi','lo')) for n,s in suffix.items()},indices)
 targets=[gauge_chart_firstjet_fraction_reference(small,direction,result,locks,k) for k in range(len(indices))]
 for n in CHART_FAMILIES:
  actual=result['mechanical']['delta_momenta']['K' if n=='K' else 'metric_EH_density'] if n in ('K','metric_EH_density') else result['mechanical']['dc']['dens'] if n=='dens' else result['mechanical']['d'][n]
  actual=tuple(np.moveaxis(w,1,0).copy() for w in actual) if n in ('z','dz') else actual
  gauge_rational_control(label+'_Fraction_'+n,actual,[t[n] for t in targets])


def packet(refs):
 inp=seal('INPUT',dict(kind='fresh_NEW139_mechanical_gauge64_source_coefficient_preparation',finite_input=thin(refs['finite_input']),finite_readout=thin(refs['finite_readout']),literal_bridge=thin(refs['literal_bridge']),mechanical_cache=refs['mechanical']['closed_provenance'],fixed_support=SELECTED22_PROOF,original_state0_failure=refs['original_state0_failure'],original_targets=refs['provenance']['unchanged_original_targets'],physical_adoption=False));inputs=[];columns=[];ports=[]
 for iq in range(4):
  column=hydrate_NEW139_mechanical_column(refs,iq);inputs.append(column['input_record']);tag='NEW139_mechanical_gauge_column%d'%iq
  def test_complete(row,jet,kind,payload):
   label=tag+'_row%d_jet%d'%(row,jet);CONTEXT.update(stage='NEW139_mechanical_gauge_port',column=iq,row=row,jet=jet)
   capture_families('completed_MECHANICAL_GAUGE_TEST_',payload);chart_controls(column,row,jet,payload,label)
   q=seal('MECHANICAL_GAUGE_TEST',dict(kind=kind,column=iq,row=row,jet=jet,input=column['input_record'],source_records=column['source_records'],same_candidate_provenance=column['same_candidate_provenance'],phase_branch_evaluated=False,fullweak_and_global_association_controls_external=True,rational_reference=list(REFERENCE_METADATA),physical_adoption=False));REFERENCE_METADATA.clear();ports.append(q);return q
  def column_complete(kind,payload):
   capture_families('completed_MECHANICAL_GAUGE_COLUMN_',payload);return seal('MECHANICAL_GAUGE_COLUMN',dict(kind=kind,column=iq,input=column['input_record'],tests=payload['completed_test_refs'],gauge_row_order=payload['gauge_row_order'],gauge_coordinate_order=payload['gauge_coordinate_order'],source_records=column['source_records'],phase_coefficients_require_separate_exact_operand_inheritance=True,source_uncancelled_enclosure_and_fullweak_transpose_external=True,C_equals_minus_Rv_transpose_assumed=False,physical_adoption=False))
  result=prepare_NEW139_mechanical_gauge_coefficients(column,keep,tag,test_complete,column_complete);columns.append(result['column_record']);del result,column
 expected=['NEW139_mechanical_gauge_column%d_row0_jet0_Fraction_'%iq+n for iq in range(4) for n in CHART_FAMILIES]
 assert [c['name'] for c in CHECKS]==expected and all(c['passed'] is True and c['tolerance']==2e-11 for c in CHECKS)
 assert len(ports)==64 and len(inputs)==len(columns)==4 and len(RECORDS)==1+4*(1+16+1)
 final=seal('PREPARATION',dict(input=inp,prepared_inputs=inputs,columns=columns,tests=ports,new_controls=len(expected),fullweak_gauge_contacts_earned=False,negative_stationarity_feedback_earned=False,source_scope='registered mechanical gauge derivative only',physical_adoption=False));assert len(RECORDS)==74
 return dict(status='NEW139_MECHANICAL_GAUGE64_POINT_COEFFICIENTS_PREPARED_UNQUALIFIED',input=inp,prepared_inputs=inputs,columns=columns,ports=ports,preparation=final,finite_terminal=(FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF),literal_terminal=(LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF),mechanical_cache_terminal=(MECHANICAL_SOURCE,MECHANICAL_RESULT,MECHANICAL_RECEIPT,MECHANICAL_CLOSURE_PROOF),roles=len(RECORDS),new_ports=64,new_controls=len(expected),original_targets_and_rates_preserved=True,phase_coefficients_inherited_only_by_future_exact_operand_proof=True,fullweak_gauge_contacts_earned=False,Cstar_equals_minus_Rv_assumed=False,normal_feedback_or_geometry_correction_admitted=False,physical_adoption=False)


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None and all(v is not None for q in (FINITE_SOURCE,FINITE_RESULT,FINITE_RECEIPT,FINITE_CLOSURE_PROOF,LITERAL_SOURCE,LITERAL_RESULT,LITERAL_RECEIPT,LITERAL_PROOF) for v in q),'Root FULL review and both natural NEW closures required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,new_ports=64,new_controls=len(CHART_FAMILIES)*4,roles=74,source_scope='mechanical registered gauge derivative',physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW139_mechanical_gauge_port',context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS),rational_reference=list(REFERENCE_METADATA)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())

