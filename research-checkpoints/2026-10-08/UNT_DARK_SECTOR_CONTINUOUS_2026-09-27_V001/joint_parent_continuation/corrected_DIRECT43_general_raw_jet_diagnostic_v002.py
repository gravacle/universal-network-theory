"""HELD corrected DIRECT43 receiver: genuine139 words -> exact205 -> general161.
Root owns actual accepted-finite/selected-input bindings and every execution.
No old producer, finite residual, operator, circle or catalogue fit is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
from math import isqrt
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CORRECTED_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V002'
PROTOCOL='CORRECTED_DIRECT43_GENERAL_RAW_JET_DIAGNOSTIC_V002.md'
PROTOCOL_SHA='551f561014419221eea06eccbb781f9ad88048e7d9b9df070c6ffc7a5232a85c'
TERMINALS={n:((None,None),(None,None,None),(None,None,'CLOSED'),(None,None,None)) for n in ('direct_baseline','coupled_correction','finite_trial','selected_inputs')}
SELECTED_DATA_MAP=(None,None,'ROOT_CORRECTED_DIRECT43_SELECTED_OPERANDS_AND_CASES_VERIFIED_HELD')
FINITE_METRIC_ADMISSION=(None,None,'ROOT_CHANGED_FINITE_ORIGINAL_AUTHORITIES_AND_FEEDBACK_CONDITIONAL_ADMISSION_VERIFIED')
# The finite196 measurement itself does not supply this external acceptance.
SOURCE=RESULT=RECEIPT=PROOF=None
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_finite_conformal_circle_event_v001.py': 'b607fcf3346d83e012771e75d9b658cef9ad51aeac4de09ad0a69bb3d75489b1', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_baseline_DIRECT43_raw_jet_pair_v001.py': '07cbcd0af964ba2531c12878e629b9c58ce56bff23fa94bd5471d83162ab2dd9', 'author_fragment_conformal_DIRECT43_uncertainty_primitives_v003.py': '0027662008c236628ffd8b82e7202a24153ea6dadc8d1beeaeec9f7d2d31cd83', 'author_fragment_general_raw_jet_instantaneous_geodesic_v001.py': 'b357de459494d9bad5bb0963ee2c3236ca8265872ebaf583062e54b03b40602b', 'direct43_original_baseline_preparation_v003.py': '68fff180edacd39e1d88c828201f6ea6c5018eaec78bbdd2e4bb90f4528ae336', 'author_fragment_direct43_owned_baseline_field_law_v004.py': '99ea2904f4b699764f0e186b9cb7d05db691bb5dc91a5019ee7199bb850ce7b1', 'author_fragment_direct_TOTAL43_finite_event_v001.py': '9458f530b2d15beb9138d806749a42ef1192df9215292a3b39280b63d7f50e59', 'author_fragment_model_metric_si_circle_readout_v002.py': '245685583f389bb7b8379fc27b8ea31301b3c26f4aa63032f3d8959822fecdd8', 'cross_u_full_metric_geodesic_and_rotating_material_v001.py': '53bc39888adeff33fffb13e04182fc9ee23d93233b15e0c533d02e24345137aa', 'author_fragment_full_dynamic_metric_circle_v002.py': '3be37b2181ff154067ccd0d01587266ce64a58a118bd6dbd331fca1f49001c6b', 'author_fragment_conformal_DIRECT43_uncertainty_primitives_v002.py': '138c24243842734bddcfb0c83c3f2ca79202a4dafbab57ed3a9a976b57cc03e6', 'author_fragment_corrected_DIRECT43_general_raw_metric_v001.py': '8b97f48e8ea0f6fb9f6df9a0a249bae92366358ab655a7bdb87163729828d3d1', 'cross_u_NEW139_coupled425955_correction_v006.py': '10fc2d6d41a711258111b78c7d2fec5eaffc37bb1a52c77567521414118a632c', 'cross_u_coupled_point_TOTAL_finite_continuation_v003.py': '36c0847f7a7aa256d5f5fe3c3e7932a87978f9261a376b284fc4e19c7a655873'}
np=P=H=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};EVENT_CONTEXT={};SAMP={};SAMPLE_PREFIX=''
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
SAMPLE_SUFFIXES={'positive_sheet_value_R_Z_weights'}|{'original_rounded_Fhat_corner%d'%i for i in range(4)}|{n+'_'+w for n in ['chi_corner%d'%i for i in range(4)]+['chi_jet%d_partial'%i for i in range(3)]+['CORRECTION_corner%d'%i for i in range(4)]+['CORRECTION_time_partial'] for w in ('hi','lo')}


def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert {n.name for n in nodes}==set(names),file
 exec(compile(ast.Module(body=nodes,type_ignores=[]),file,'exec'),scope)

def constants(file,names):
 out={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse((BASE/file).read_text()).body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names}
 assert set(out)==set(names),file;return out

def metadata(file,checksum):
 bind(file,checksum);p=P.path(file);assert p.stat().st_size<=16*1024*1024,file;return json.loads(p.read_text())

def retain(name,value):
 CONTEXT['active_capture']=name
 a=keep(name,value)
 if SAMPLE_PREFIX and name.startswith(SAMPLE_PREFIX) and name[len(SAMPLE_PREFIX):] in SAMPLE_SUFFIXES:SAMP[name[len(SAMPLE_PREFIX):]]=a.copy()
 return a

def initialize():
 global np,P,H
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','keep','read','thin','clear_current','initialize_io'},globals());initialize_io()
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=retain)
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','scalar_mask','scalar_lift','native_mask','metric_mask','lift_metric','dd_metric_F','unpack_fields'}
 definitions(list(PINS)[0],names,SCOPE);definitions(list(PINS)[1],{'a_matvec'},SCOPE)
 for n in names|{'a_matvec'}:setattr(P,n,SCOPE[n])
 definitions('author_fragment_exact_exponent_two_product_v003.py',{'exact_exponent_two_product','install_exact_exponent_product'},globals());install_exact_exponent_product(SCOPE,P,retain,'corrected_raw_shared_exact_product')
 definitions('author_fragment_finite_conformal_circle_event_v001.py',{'fce_pair','fce_block'},globals())
 definitions('author_fragment_finite_york_geometry_target_v001.py',{'fy_keep','fy_sum','fy_mv','fy_mm','fy_scale_matrix','fy_div','fy_sqrt','fy_physical_reference_inverse'},globals())
 q=dict(np=np,math=math);definitions('author_fragment_model_metric_si_circle_readout_v002.py',{'q1_radial_readout_contact'},q);H=types.SimpleNamespace(**q)
 definitions('author_fragment_direct_TOTAL43_finite_event_v001.py',{'direct_TOTAL43_sample_correction'},globals())
 helper='author_fragment_corrected_DIRECT43_general_raw_metric_v001.py';names={n.name for n in ast.parse((BASE/helper).read_text()).body if isinstance(n,ast.FunctionDef)};assert len(names)==4;definitions(helper,names,globals());globals().update(constants(helper,{'CORRECTED_DIRECT43_SOURCE_PINS'}))
 helper='author_fragment_conformal_DIRECT43_uncertainty_primitives_v003.py';names={n.name for n in ast.parse((BASE/helper).read_text()).body if isinstance(n,ast.FunctionDef)};assert len(names)==23;definitions(helper,names,globals());globals().update(constants(helper,{'CONFORMAL_UNCERTAINTY_SOURCE_PINS'}))
 helper='author_fragment_general_raw_jet_instantaneous_geodesic_v001.py';definitions(helper,{'grg_pair','grg_interval_event','general_raw_jet_instantaneous_geodesic'},globals());globals().update(constants(helper,{'GENERAL_RAW_GEODESIC_SOURCE_PINS','GENERAL_RAW_GEODESIC_ROOT_BITS'}))

def terminal(name,projection):
 source,result,receipt,proof=TERMINALS[name]
 assert all(v is not None for pin in (source,result,receipt,proof) for v in pin),name
 for pin in (source,result,receipt,proof):bind(*pin[:2])
 rc=metadata(*receipt[:2]);p=metadata(*proof[:2])
 assert rc['status']==receipt[2]=='CLOSED' and rc.get('error_sha256') is None and p['status']==proof[2]
 owner=rc['owner'];assert owner==p['owner'] and owner['source_sha256']==p['source_sha256']==source[1]
 assert rc['result_sha256']==p['result_sha256']==result[1] and p['receipt_sha256']==receipt[1]
 assert p['naturally_closed'] is True and type(p['exit_code']) is int and p['exit_code']==0
 assert p['all_input_seals_verified'] is p['all_output_seals_verified'] is p['all_success_role_seals_verified'] is True
 assert rc['qualification'] and all(v is False for v in rc['qualification'].values())
 assert projection['owner']==owner and projection['status']==result[2] and projection['qualification']==rc['qualification']
 stem=result[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 if name=='direct_baseline':
  actual=metadata(*result[:2]);assert projection=={n:actual[n] for n in ('owner','status','qualification','case')}
  assert actual['qualification']==FLAGS and len(actual['checkpoints'])==actual['case']['roles']==87 and not actual['controls'] and len(actual['case']['events'])==43
  assert actual['case']['baseline_only'] is True and actual['case']['physical_adoption'] is False
 else:actual=None
 packet=dict(source=source,result=result,receipt=receipt,proof=proof,naturally_closed=True,exit_code=0,all_selected_seals_verified=True,all_input_seals_verified=True,all_success_role_seals_verified=True,owner=owner)
 return dict(packet=packet,owner=owner,receipt=rc,proof=p,result=actual,projection=projection)

def selected_record(item,groups):
 ref=item['reference'];group=groups[item['terminal']]
 for key,digest in (('file','sha256'),('commit_file','commit_sha256')):bind(ref[key],ref[digest])
 q=metadata(ref['commit_file'],ref['commit_sha256']);assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 md=q['metadata'];assert md['owner']==group['owner']==item['scientific_owner'] and md['failed'] is False and md['qualification']==FLAGS
 assert item['success_role_and_exact_case_reference_verified'] is True
 for key,digest in (('file','sha256'),('commit_file','commit_sha256')):assert group['receipt']['output_sha256'][ref[key]]==ref[digest]
 if item['case_path']==['$checkpoint_INPUT0']:
  assert item['terminal']=='finite_trial' and group['projection']['selected_INPUT0']==ref and ref['file'].endswith('_00000_INPUT.npz')
 else:
  case=group['projection']['case']
  for key in item['case_path']:case=case[key]
  assert thin(case)==ref
 return dict(ref,metadata=md)

def admission():
 global SOURCE,RESULT,RECEIPT,PROOF
 assert all(v is not None for v in SELECTED_DATA_MAP+FINITE_METRIC_ADMISSION)
 m=metadata(*SELECTED_DATA_MAP[:2]);a=metadata(*FINITE_METRIC_ADMISSION[:2])
 assert m['status']==SELECTED_DATA_MAP[2] and a['status']==FINITE_METRIC_ADMISSION[2]
 assert json.loads(json.dumps(m['terminals']))==json.loads(json.dumps(TERMINALS)) and tuple(m['finite_metric_admission_proof'])==FINITE_METRIC_ADMISSION
 for n in ('all_selected_archive_commit_bytes_owners_and_headers_verified','exact_terminal_status_owner_and_case_projections_verified','original_mesh_and_basis_words_verified','genuine_point_TOTAL_baseline_source_association_verified','total_chi_and_coupled_metric_match_accepted_finite_words','all_reference_gauge_time_phi_words_preserved','released_parent_function_ASTs_match_templates','first_finite_trial_original1071_baseline_ancestry_verified'):assert m[n] is True
 assert m['physical_adoption'] is False
 groups={n:terminal(n,m['terminal_projections'][n]) for n in TERMINALS}
 source,result,receipt,proof=TERMINALS['direct_baseline'];SOURCE,RESULT,RECEIPT,PROOF=source,result,receipt,proof
 assert source==('direct43_original_baseline_preparation_v003.py',PINS['direct43_original_baseline_preparation_v003.py'])
 assert groups['coupled_correction']['projection']['status']=='NEW139_COUPLED425955_PROXY_CORRECTION_NUMERICALLY_MEASURED_UNQUALIFIED'
 assert groups['finite_trial']['projection']['status']=='COUPLED_POINT_TOTAL_FRESH_NONLINEAR_FINITE_RESIDUAL_MEASURED_UNQUALIFIED'
 assert groups['finite_trial']['projection']['case']['original_six_measured_admitted'] is True
 assert groups['finite_trial']['projection']['case']['fresh_feedback_required'] is True
 assert json.loads(json.dumps(groups['finite_trial']['projection']['case']['closures']['coupled_correction']))==json.loads(json.dumps(TERMINALS['coupled_correction']))
 assert json.loads(json.dumps(groups['finite_trial']['projection']['case']['closures']['baseline139']))==json.loads(json.dumps(groups['coupled_correction']['projection']['case']['closures']['finite139']))
 for n in ('direct_baseline','coupled_correction','finite_trial'):assert json.loads(json.dumps(a[n]))==json.loads(json.dumps(TERMINALS[n]))
 assert a['all_required_original_gates_admitted'] is True and a['physical_adoption'] is False
 closure=a['metric_admission'];assert closure==m['metric_admission']
 for n in ('finite_constraint_solution_admitted','finite_domains_admitted','original_whole_correction_source_unsigned_authority_verified','fresh_nonlinear_canonical_phase_normal_CMC_and_stationarity_feedback_admitted','fixed_original_reference_denominators_verified'):assert closure[n] is True
 assert closure['finite_physical_metric_admitted'] is False and closure['provenance'] and closure['reference_provenance'] and closure['declared_conditional_boundary']
 assert set(m['records'])=={'baseline_input','coupled_solution','finite_trial_fields','finite_input'}
 records={n:selected_record(v,groups) for n,v in m['records'].items()}
 assert m['records']['baseline_input']['terminal']=='direct_baseline' and m['records']['baseline_input']['case_path']==['input']
 assert m['records']['coupled_solution']['terminal']=='coupled_correction' and m['records']['coupled_solution']['case_path']==['solution']
 assert m['records']['finite_trial_fields']['terminal']==m['records']['finite_input']['terminal']=='finite_trial' and m['records']['finite_trial_fields']['case_path']==['trial_fields']
 assert m['records']['finite_input']['case_path']==['$checkpoint_INPUT0']
 globals().update(CORRECTED_DIRECT43_AUTHOR_DRAFT=False,CORRECTED_DIRECT43_AUTHORING_IN_PROGRESS=False,CORRECTED_DIRECT43_PARENT_PINS={n:{k:pin for k,pin in zip(('source','result','receipt','proof'),TERMINALS[g])} for n,g in (('direct_baseline','direct_baseline'),('coupled','coupled_correction'),('finite','finite_trial'))},CONFORMAL_UNCERTAINTY_AUTHOR_DRAFT=False,CONFORMAL_UNCERTAINTY_AUTHORING_IN_PROGRESS=False,CONFORMAL_UNCERTAINTY_TERMINALS=TERMINALS,GENERAL_RAW_GEODESIC_AUTHOR_DRAFT=False,GENERAL_RAW_GEODESIC_AUTHORING_IN_PROGRESS=False)
 fs,fr,fc,fp=TERMINALS['finite_trial'];globals().update(GENERAL_RAW_GEODESIC_EVENT_SOURCE=fs,GENERAL_RAW_GEODESIC_EVENT_RESULT=fr,GENERAL_RAW_GEODESIC_EVENT_RECEIPT=fc,GENERAL_RAW_GEODESIC_EVENT_PROOF=fp,GENERAL_RAW_GEODESIC_INTERVAL_SOURCE=('author_fragment_conformal_DIRECT43_uncertainty_primitives_v003.py',PINS['author_fragment_conformal_DIRECT43_uncertainty_primitives_v003.py']))
 return dict(map=m,admission=a,closure=closure,groups=groups,records=records,result=groups['direct_baseline']['result'],receipt=groups['direct_baseline']['receipt'],proof=groups['direct_baseline']['proof'])

def record(ref,refs,ordinal,role,index):
 assert ref['file']==SOURCE[0].replace('direct43_original_baseline_preparation_v003.py','DIRECT43_ORIGINAL_BASELINE_PREPARATION_V003')+'_%05d_%s.npz'%(ordinal,role)
 q=metadata(ref['commit_file'],ref['commit_sha256']);assert set(q)=={'file','sha256','metadata'} and q['file']==ref['file'] and q['sha256']==ref['sha256']
 md=q['metadata'];assert md['owner']==refs['result']['owner'] and md['failed'] is md['physical_adoption'] is False and md['qualification']==FLAGS and md['index']==index
 assert thin(refs['result']['checkpoints'][ordinal])==ref
 for f,h in (('file','sha256'),('commit_file','commit_sha256')):assert refs['receipt']['output_sha256'][ref[f]]==ref[h];bind(ref[f],ref[h])
 return dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def load(ref,names,label):
 assert all(n in ref['metadata']['schema'] for n in names);data=read(ref,names)
 for n,a in data.items():RAW[label+'_'+n]=a.copy();retain(label+'_'+n,a);s=ref['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True
 return data

def serial(value):
 if isinstance(value,Fraction):return dict(numerator=str(value.numerator),denominator=str(value.denominator))
 if isinstance(value,np.ndarray):return serial(value.tolist())
 if isinstance(value,np.generic):return serial(value.item())
 if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
 if isinstance(value,(tuple,list)):return [serial(v) for v in value]
 if value is None or type(value) in (str,bool,int) or type(value)is float and math.isfinite(value):return value
 raise TypeError(type(value).__name__)

def complete(role,data):
 def numeric(x,prefix):
  if isinstance(x,np.ndarray):return {prefix:x.copy()}
  if isinstance(x,dict):return {k:a for n,v in x.items() for k,a in numeric(v,prefix+str(n)+'_').items()}
  if isinstance(x,(tuple,list)):return {k:a for n,v in enumerate(x) for k,a in numeric(v,prefix+str(n)+'_').items()}
  return {}
 CONTEXT.update(EVENT_CONTEXT,stage=role);q=P.checkpoint(role,dict(RAW,**AVAILABLE,**numeric(data,'completed_')),dict(role=role,context=dict(CONTEXT),completed_payload=serial(data),baseline_only=False,physical_adoption=False))
 ref=thin(q);clear_current();CONTEXT.update(EVENT_CONTEXT,completed_stage=role);return ref

def word_tree(pair):
 hi,lo=pair;assert hi.shape==lo.shape and hi.dtype==lo.dtype==np.float64 and np.all(np.isfinite(hi)) and np.all(np.isfinite(lo))
 def build(a,b):
  if a.shape==():return (Fraction.from_float(float(a)),Fraction.from_float(float(b)))
  return [build(x,y) for x,y in zip(a,b)]
 return build(hi,lo)

def dyadic_tree(array):
 if array.shape==():return Fraction.from_float(float(array))
 return [dyadic_tree(a) for a in array]

def correction_inputs(refs):
 q=refs['records'];assert q['baseline_input']['metadata']['admission']['basis_record']==refs['map']['original_basis_record']
 b=load(q['baseline_input'],('R_mesh','Z_mesh'),'DIRECT_baseline_mesh')
 f=load(q['finite_trial_fields'],('completed_POINT_TOTAL_TRIAL_FIELDS_nodes_chi_hi','completed_POINT_TOTAL_TRIAL_FIELDS_nodes_chi_lo','completed_POINT_TOTAL_TRIAL_FIELDS_basis_r','completed_POINT_TOTAL_TRIAL_FIELDS_basis_z'),'accepted_finite_TOTAL')
 s=load(q['coupled_solution'],('completed_SOLUTION_mechanical_hi','completed_SOLUTION_mechanical_lo'),'NEW_coupled_solution')
 k=load(q['finite_input'],('completed_INPUT_correction_metric_hi','completed_INPUT_correction_metric_lo'),'accepted_finite_metric_increment')
 r,z=b['R_mesh'],b['Z_mesh'];assert r.shape==(87,) and z.shape==(45,)
 for a,b in ((r,f['completed_POINT_TOTAL_TRIAL_FIELDS_basis_r']),(z,f['completed_POINT_TOTAL_TRIAL_FIELDS_basis_z'])):assert a.shape==b.shape and a.dtype==b.dtype==np.dtype('float64') and np.array_equal(a.view(np.uint64),b.view(np.uint64))
 chi=tuple(f['completed_POINT_TOTAL_TRIAL_FIELDS_nodes_chi_'+w].copy() for w in ('hi','lo'));packed=tuple(s['completed_SOLUTION_mechanical_'+w].copy() for w in ('hi','lo'));assert all(a.shape==(403340,) for a in packed)
 metric=tuple(P.unpack_fields(a,False)[1] for a in packed)
 for w,a in zip(('hi','lo'),metric):
  target=k['completed_INPUT_correction_metric_'+w];assert a.shape==target.shape==(6,87,45) and a.dtype==target.dtype==np.dtype('float64') and np.array_equal(a.view(np.uint64),target.view(np.uint64))
 assert all(a.shape==(87,45) for a in chi)
 return dict(r=r,z=z,total_chi=chi,metric_correction=metric)

def event_inputs(refs,event):
 i=event['index'];rr=record(event['reference_event'],refs,1+2*i,'REFERENCE_EVENT',i);br=record(event['baseline_event'],refs,2+2*i,'BASELINE_EVENT',i)
 shapes={'h':(3,3),'h_spatial_jets':(2,3,3),'N':(),'beta':(3,),'N_jets':(4,),'beta_jets':(4,3),'g':(4,4),'dg':(4,4,4)}
 d=load(rr,tuple(n+'_'+w for n in shapes for w in ('hi','lo')),'reference');reference={n:tuple(d[n+'_'+w] for w in ('hi','lo')) for n in shapes};md=rr['metadata']
 reference.update(R=md['R'],Z=md['Z'],radial_side=md['radial_side'],provenance=md['reference_event_provenance'],same_reference_as_finite_candidate=refs['closure']['reference_provenance'],direct_event_data_not_Gauss_interpolation=True)
 assert md['R']==br['metadata']['R']==event['R'] and md['finite_reference_provenance']==refs['map']['baseline_finite_reference_provenance']
 associations=refs['map']['event_source_associations'];assert len(associations)==43
 tie=associations[i];assert tie['index']==i and tie['R']==event['R'] and tie['reference_event']==thin(rr) and tie['baseline_event']==thin(br)
 b=load(br,('baseline_TOTAL_hdot_hi','baseline_TOTAL_hdot_lo'),'authentic_DIRECT_TOTAL_baseline');ht=tuple(b['baseline_TOTAL_hdot_'+w].copy() for w in ('hi','lo'))
 for n,shape in shapes.items():assert all(a.shape==shape for a in reference[n])
 assert all(a.shape==(3,3) for a in ht)
 packets={n:dict(refs['groups'][g]['packet']) for n,g in (('direct_baseline','direct_baseline'),('coupled','coupled_correction'),('finite','finite_trial'))};packets['finite']['metric_admission']=refs['closure']
 adm=dict(packets,source_pins=CORRECTED_DIRECT43_SOURCE_PINS,scope='conditional_accepted_finite_trial',basis_record=refs['map']['original_basis_record'],total_chi_record=thin(refs['records']['finite_trial_fields']),metric_correction_record=thin(refs['records']['coupled_solution']),direct_baseline_reference_record=thin(rr),direct_baseline_event_record=thin(br),baseline_reference_metadata=md,baseline_event_metadata=br['metadata'],coordinate_event=[0.,event['R'],0.,0.],event_provenance=dict(accepted_finite=refs['closure']['provenance'],reference=md['reference_event_provenance'],coordinate=[0.,event['R'],0.,0.],baseline_reference=thin(rr),baseline_TOTAL=thin(br),chi=thin(refs['records']['finite_trial_fields']),metric_correction=thin(refs['records']['coupled_solution'])))
 for n in ('original_mesh_and_basis_words_verified','point_TOTAL_addition_after_original_lift','baseline_event_TOTAL_hdot_matches_finite_BASELINE_before_correction','total_chi_matches_finite_TOTAL_nodes','metric_correction_matches_coupled_increment','selected_record_words_and_metadata_authenticated','geometric_h_phi_zero_source_law_verified'):assert tie[n] is True;adm[n]=True
 adm['original_input_word_hex']=dict(reference={n:{w:[float(x).hex() for x in a.flat] for w,a in zip(('hi','lo'),reference[n])} for n in shapes},baseline_TOTAL_hdot={w:[float(x).hex() for x in a.flat] for w,a in zip(('hi','lo'),ht)})
 return reference,ht,adm

def sampling_words(raw,baseline_hdot):
 assert set(SAMP)==SAMPLE_SUFFIXES,'Source103 exact sampling captures missing; no reconstruction'
 def pair(n):return tuple(SAMP[n+'_'+w] for w in ('hi','lo'))
 return dict(chi_corners=[word_tree(pair('chi_corner%d'%i)) for i in range(4)],weights=dyadic_tree(SAMP['positive_sheet_value_R_Z_weights']),rho_words=[word_tree(pair('chi_jet%d_partial'%i)) for i in range(3)],metric_corners=[word_tree(pair('CORRECTION_corner%d'%i)) for i in range(4)],Fhat=[dyadic_tree(SAMP['original_rounded_Fhat_corner%d'%i]) for i in range(4)],delta_six_words=word_tree(pair('CORRECTION_time_partial')),baseline_hdot_words=word_tree(baseline_hdot),total_hdot_words=word_tree(raw['event_TOTAL_hdot']))

def prepare(refs):
 global SAMPLE_PREFIX
 data=correction_inputs(refs);header=complete('INPUT',dict(terminals=TERMINALS,selected_map=SELECTED_DATA_MAP,finite_metric_admission=FINITE_METRIC_ADMISSION,correction=data,events=refs['result']['case']['events'],interval_limits=dict(bits=128,max_terms=256,max_squarings=16),orientation=1,physical_adoption=False));events=[]
 for index,event in enumerate(refs['result']['case']['events']):
  assert event['index']==index;EVENT_CONTEXT.clear();EVENT_CONTEXT.update(index=index,R=event['R'],radial_side='left',vertical_side='upper',source_reference_event=event['reference_event'],source_baseline_event=event['baseline_event']);CONTEXT.update(EVENT_CONTEXT,stage='authentic_closed_corrected_event_words')
  reference,ht,adm=event_inputs(refs,event);label='EVENT_%02d_CORRECTED'%index;SAMPLE_PREFIX=label+'_original_Q1_';SAMP.clear()
  before=len(RECORDS);raw=corrected_DIRECT43_general_raw_event(reference,ht,data['r'],data['z'],data['total_chi'],data['metric_correction'],R=event['R'],radial_side='left',admission=adm,keep=retain,label=label,stage_complete=complete);assert len(RECORDS)-before==14
  sampling=sampling_words(raw,ht)
  ia=dict(terminals=TERMINALS,source_pins=CONFORMAL_UNCERTAINTY_SOURCE_PINS,input_scope='accepted_conditional_finite_metric',all_selected_dyadic_inputs_authenticated=True,original_masks_lifts_Fhat_corner_order_verified=True,point_TOTAL_addition_after_lift_verified=True,same_event_reference_and_radial_side_verified=True,all_original_word_hex_and_gauge_time_phi_retained=True,physical_metric_admitted=False,finite_constraint_solution_admitted=True,sampling_refs=dict(corrected_sampling=raw['source_stage_refs'][label+'_SAMPLING'],corrected_TOTAL=raw['source_stage_refs'][label+'_TOTAL_RATE'],baseline_reference=adm['direct_baseline_reference_record'],baseline_TOTAL=adm['direct_baseline_event_record'],accepted_chi=adm['total_chi_record'],coupled_metric=adm['metric_correction_record']))
  before=len(RECORDS);box=conformal_DIRECT43_primitive_enclosure(dict(words={n:word_tree(reference[n]) for n in ('h','h_spatial_jets','N','beta','N_jets','beta_jets')}),sampling,ia,dict(bits=128,max_terms=256,max_squarings=16),complete,'EVENT_%02d_INTERVAL'%index);assert len(RECORDS)-before==11
  rawref=raw['source_stage_refs'][label+'_general_ADM_RAW_PAIR'];words=dict(g=word_tree(raw['g']),dg=word_tree(raw['dg']),all_output_dyadic_words_authenticated=True,all_original_word_hex_preserved=True,word_hex={n:{w:[float(x).hex() for x in a.flat] for w,a in zip(('hi','lo'),raw[n])} for n in ('g','dg')},completed_raw_pair=rawref)
  before=len(RECORDS);bounds=attach_completed_DIRECT43_words(box,words,complete,'EVENT_%02d_ATTACH'%index);assert len(RECORDS)-before==2
  ip=box['completed'][-1];globals()['GENERAL_RAW_GEODESIC_INTERVAL_PROOF']=(ip['commit_file'],ip['commit_sha256'],'same_owner_completed_exact_primitive_box')
  source,result,receipt,proof=TERMINALS['finite_trial'];ga=dict(source_pins=GENERAL_RAW_GEODESIC_SOURCE_PINS,source=source,result=result,receipt=receipt,proof=proof,interval_source=GENERAL_RAW_GEODESIC_INTERVAL_SOURCE,interval_proof=GENERAL_RAW_GEODESIC_INTERVAL_PROOF,naturally_closed=True,exit_code=0,all_selected_byte_owner_and_header_seals_verified=True,physical_metric_admitted=False,input_scope='accepted_conditional_finite_metric',finite_constraint_solution_admitted=True,finite_domains_admitted=True,finite_physical_metric_admitted=False,coordinate_event=raw['coordinate'],radial_side='left',vertical_side='upper',interval_event_provenance=box['provenance'],event_provenance=adm['event_provenance'])
  before=len(RECORDS);answer=general_raw_jet_instantaneous_geodesic(raw['g'],raw['dg'],bounds=bounds,orientation=1,admission=ga,keep=retain,label='EVENT_%02d_GENERAL'%index,stage_complete=complete);count=len(RECORDS)-before;assert 2<=count<=6
  events.append(dict(index=index,R=event['R'],corrected_stages=raw['source_stage_refs'],interval_stages=box['completed'],attachment_stages=bounds['completed'],general_stages=answer['completed_stage_refs'],general_role_count=count,readout=serial(answer),source_association_gaps=serial(raw['geometry']['source_association_gaps']),accepted_finite_condition=refs['closure'],physical_adoption=False))
 assert len(events)==43 and len(RECORDS)==1+43*27+sum(e['general_role_count'] for e in events) and not CHECKS
 return dict(status='CORRECTED_DIRECT43_GENERAL_INSTANTANEOUS_RADIAL_DIAGNOSTICS_MEASURED_CONDITIONAL',input=header,events=events,roles=len(RECORDS),controls=0,baseline_only=False,accepted_finite_condition=refs['closure'],new_coupled_or_corrected_finite_metric_evaluated=True,source_or_installed_rounding_accuracy_admitted=False,full_circle_or_galaxy_prediction_admitted=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Independent FULL review and actual accepted-finite bindings required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=dict(INPUTS),terminals=TERMINALS,selected_map=SELECTED_DATA_MAP,finite_metric_admission=FINITE_METRIC_ADMISSION,events=43,roles='1+43*(14corrected+11primitive+2attachment)+sum(general2to6)',controls=0,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=prepare(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,checkpoints=RECORDS,controls=CHECKS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',dict(RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}),dict(kind='unfinished_corrected_general_diagnostic',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
