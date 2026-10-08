"""HELD point-first finite TOTAL-rate refresh; root alone releases and executes."""
import ast,hashlib,json,math,os,traceback,types
from datetime import datetime,timezone
from pathlib import Path
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V002'
DRIVER_PROTOCOL='FIXED_GEOMETRY_TOTAL_RATE_STATE_EVALUATION_V002.md'
PROTOCOL_SHA='1daf7239a440a8de3e32309efe06c0f485aff0a469e832cf14e64182a8128fe1'
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
BASELINE_CLOSURE=((None,None),(None,None,None),(None,None,None),(None,None,None))
UPDATED_PHASE_CLOSURE=((None,None),(None,None,None),(None,None,None),(None,None,None))
JOIN_CLOSURE=((None,None),(None,None,None),(None,None,None),(None,None,None))
CORRECTION_CLOSURE=((None,None),(None,None,None),(None,None,None),(None,None,None))
SELECTED22_PROOF=(None,None,'ROOT_CLOSED_FIXED_RATE22_SELECTED_INPUT_SEALS_VERIFIED')
FIXED_BINDING=(None,None)
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
IO_ARITHMETIC_PARENT='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
PRIMITIVE_SOURCE='cross_u_paired_current_primitive_momentum_readout_v002.py'
NORMAL_SOURCE='cross_u_paired_current_normal_constraints_v002.py'
RECHECK_SOURCE='author_fragment_single_decode_recheck_v001.py'
PLAN_FILE='NATIVE_FIXED_GEOMETRY_TOTAL_RATE_STATE_MINIMAL_PACKET_V002.json'
PLAN_SHA='4c6312d4168c81e77208447da7ed58aa1904b98195eefd9ea1830a1eab103031'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_fixed_geometry_total_rate_state_v002.py': 'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d', 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py': 'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db'}
CORE_DEFINITION_COUNTS={'author_fragment_finite_york_geometry_target_v001.py': 11, 'author_fragment_finite_york_spacetime_first_jets_v001.py': 20, 'author_fragment_finite_candidate_raw_action_adapter_v001.py': 8, 'author_fragment_compact_metric_contact_momenta_v002.py': 7, 'author_fragment_finite_candidate_native_EH_normal_v003.py': 8, 'author_fragment_exact_exponent_two_product_v003.py': 2, 'author_fragment_fixed_geometry_total_rate_state_v002.py': 6}
FLAGS={'physical_adoption':False,'uniform_DD_or_global_inverse_qualified':False,'fresh_current_six_or_normal_CMC_admitted':False,'changed_spatial_geometry':False,'stationarity_feedback_or_new43_earned':False}
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};PLAN=None;BASIS=None;PROVENANCE=None

def bind(name,expected):
 assert isinstance(expected,str) and expected and P.sha(P.path(name))==expected,name
 key=str(P.path(name).resolve());assert key not in INPUTS or INPUTS[key]==expected;INPUTS[key]=expected
 return expected

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def keep(name,value):
 a=np.asarray(value);RAW[name]=a.copy()
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),name
 AVAILABLE[name]=a.copy();return a

def clear_current():
 RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear()

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)


def initialize():
 global P,SCOPE,np,N
 wanted={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'}
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 definitions(PRIMITIVE_SOURCE,wanted,SCOPE);P=types.SimpleNamespace(**{n:SCOPE[n] for n in wanted},INPUTS=INPUTS)
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter','lift_velocity','lift_metric','metric_R_matrix','pack_fields','unpack_fields','dd_native_node_value','dd_metric_node_value'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','paired_current_affine_features','paired_current_affine_momenta','native_mask','metric_mask','dd_native_scatter','dd_metric_F','dd_metric_scatter'}
 definitions(IO_ARITHMETIC_PARENT,base,SCOPE);definitions(PRIMITIVE_SOURCE,primitive,SCOPE)
 for n in base|primitive|{'B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|{'B','GC','C','ALPHA','ELL'}})
 normal={'normal_test_mask','extend_normal_tests','restrict_normal_rows','normal_hat_jet','normal_hat_operation_envelope','scatter_normal_envelope','paired_restrict_normal_rows','paired_scatter_normal'}
 ns=dict(SCOPE);definitions(NORMAL_SOURCE,normal,ns);N=types.SimpleNamespace(**{n:ns[n] for n in normal})
 for file,count in CORE_DEFINITION_COUNTS.items():
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)};assert len(names)==count,file;definitions(file,names,globals())
 tree=ast.parse((BASE/'author_fragment_fixed_geometry_total_rate_state_v002.py').read_text());meta=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIXED_RATE_STATE_SOURCE_PINS' for t in n.targets));globals()['FIXED_RATE_STATE_SOURCE_PINS']=ast.literal_eval(meta.value)
 definitions(RECHECK_SOURCE,{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 install_exact_exponent_product(SCOPE,P,keep,'NEW_fixed_rate_shared_exact_product');globals()['a_prod']=P.a_prod
 for n in ('a_dd','a_slice','a_add','a_mul','a_stack','normal_pair_sum','a_transpose'):globals()[n]=getattr(P,n)


def json_bound(q):
 bind(q[0],q[1]);r=json.loads(P.path(q[0]).read_text());assert r['status']==q[2];return r

def record(ref):
 bind(ref['commit_file'],ref['commit_sha256']);c=json.loads(P.path(ref['commit_file']).read_text())
 assert c['file']==ref['file'] and c['sha256']==ref['sha256'] and c['metadata']['failed'] is False
 assert all(v is False for v in c['metadata']['qualification'].values())
 return dict(thin(ref),metadata=c['metadata'])

def read_selected(q,names):
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names)
 bind(q['file'],q['sha256']);out={}
 with np.load(P.path(q['file']),allow_pickle=False) as f:
  for n in names:
   a=f[n].copy();s=q['metadata']['schema'][n];keep('selected_closed_'+n,a)
   assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a)),n;out[n]=a
 return out

def seal(kind,payload,metadata):
 def collect(prefix,x):
  if isinstance(x,np.ndarray):keep(prefix,x)
  elif isinstance(x,tuple) and len(x)==2 and all(isinstance(a,np.ndarray) for a in x):
   keep(prefix+'_both_words',np.stack(x).copy())
   for w,a in zip(('hi','lo'),x):keep(prefix+'_'+w,a)
  elif isinstance(x,dict):
   for n,a in x.items():collect(prefix+'_'+str(n),a)
 collect('completed_'+kind,payload)
 q=P.checkpoint(kind,{n:a.copy() for n,a in {**RAW,**AVAILABLE}.items()},dict(metadata,kind=kind,physical_adoption=False));clear_current();return thin(q)

def admission():
 global PLAN
 bind(PLAN_FILE,PLAN_SHA);PLAN=json.loads(P.path(PLAN_FILE).read_text());assert PLAN['source_only'] is True and PLAN['retrieval']['payload_archive_count']==22
 selected=json_bound(SELECTED22_PROOF);assert selected['all_selected_archive_bytes_verified'] is True and selected['all_selected_COMMIT_bytes_verified'] is True and selected['all_selected_owners_naturally_closed'] is True
 expected=PLAN['retrieval']['mandatory_payload_refs'];assert selected['selected_refs']==expected and len(expected)==22
 baseline=json_bound(BASELINE_CLOSURE[3]);phase=json_bound(UPDATED_PHASE_CLOSURE[3]);join=json_bound(JOIN_CLOSURE[3])
 for p in (baseline,phase,join):assert p['naturally_closed'] is True and p['exit_code']==0 and p['all_success_role_seals_verified'] is True
 assert tuple(selected['baseline_proof'])==BASELINE_CLOSURE[3] and tuple(selected['finite_phase_proof'])==UPDATED_PHASE_CLOSURE[3] and tuple(selected['join_proof'])==JOIN_CLOSURE[3]
 for closure in (BASELINE_CLOSURE,UPDATED_PHASE_CLOSURE,JOIN_CLOSURE,CORRECTION_CLOSURE):
  bind(*closure[0]);receipt=json_bound(closure[2]);proof=json_bound(closure[3])
  assert receipt['status']=='CLOSED' and receipt.get('error_sha256') is None and proof['naturally_closed'] is True and proof['exit_code']==0
  assert receipt['owner']==proof['owner'] and receipt['result_sha256']==closure[1][1]==proof['result_sha256'] and closure[0][1]==proof['source_sha256']==receipt['owner']['source_sha256']
  assert proof['receipt_sha256']==closure[2][1] and proof['all_success_role_seals_verified'] is True
 assert P.path(CORRECTION_CLOSURE[1][0]).stat().st_size<=32*1024*1024,'Correction RESULT needs a root-reviewed bounded projection if larger';correction_result=json_bound(CORRECTION_CLOSURE[1]);cc=correction_result['case'];assert cc['status']=='HYBRID_SEARCH_ORIGINAL_SIX_MECHANICAL_ROWS_ADMITTED' and np.asarray(cc['original_six_scores']).shape==(3,2) and np.all(np.asarray(cc['original_six_scores'])<=1e-10)
 solution=record(cc['solution']);assert solution['metadata']['physical_base_rates_reset'] is False
 original=record(PLAN['closed_metadata']['original_input_ref']);assert original['metadata']['owner']['pid']==94049 and original['metadata']['rho']==0.
 meta=original['metadata'];Hbar=meta['owned_background']['h']*meta['fixed']['Hunit']/299792458.;assert Hbar>0 and np.isfinite(Hbar)
 columns=[]
 for spec in PLAN['columns']:
  iq=spec['column'];state=record(spec['state']['ref']);assert state['metadata']['column']==iq and state['metadata']['owner']['pid']==spec['state']['expected_owner_pid']
  assert state['metadata']['current_time_words']==spec['state']['owned_TOTAL_time_ref']
  for n,s in PLAN['state_selected_schema'].items():assert state['metadata']['schema'][n]['shape']==s['shape'] and state['metadata']['schema'][n]['dtype']==s['dtype']
  rows=[record(v['ref']) for v in spec['phase_rows']]
  for row,q in enumerate(rows):assert q['metadata']['owner']['pid']==15744 and q['metadata']['column']==iq and q['metadata']['row']==row and q['metadata']['jet']==0 and thin(q['metadata']['state'])==thin(state)
  columns.append(dict(spec=spec,state=state,rows=rows))
 provenance=dict(baseline_closure=BASELINE_CLOSURE,correction_closure=CORRECTION_CLOSURE,updated_phase_closure=UPDATED_PHASE_CLOSURE,fixed_binding=FIXED_BINDING,source_pins=FIXED_RATE_STATE_SOURCE_PINS,all_source_seals_authenticated=True,correction_original_six_gates_admitted=True,original_fixed_references_verified=True,unchanged_sheet_value_identity_verified=True,unchanged_sheet_weak_normal=PLAN['unchanged_sheet']['ref'],original_owned_TOTAL_time_words=[thin(q['state']) for q in columns],unchanged_original_targets=PLAN['closed_metadata']['original_canonical_target_refs'],columns=[dict(column=q['spec']['column'],state=thin(q['state']),phase_rows=[thin(r) for r in q['rows']]) for q in columns],physical_adoption=False)
 globals().update(FIXED_RATE_STATE_AUTHOR_DRAFT=False,FIXED_RATE_STATE_AUTHORING_IN_PROGRESS=False,FIXED_RATE_STATE_BASELINE_CLOSURE=BASELINE_CLOSURE,FIXED_RATE_STATE_CORRECTION_CLOSURE=CORRECTION_CLOSURE,FIXED_RATE_STATE_UPDATED_PHASE_CLOSURE=UPDATED_PHASE_CLOSURE,FIXED_RATE_STATE_FIXED_BINDING=FIXED_BINDING)
 return dict(columns=columns,solution=solution,provenance=provenance,Hbar=Hbar,original_input=thin(original))

def hydrate_column(q):
 spec=q['spec'];iq=spec['column'];CONTEXT.clear();CONTEXT.update(stage='hydrate_authentic_TOTAL_baseline',column=iq,state=thin(q['state']));data=read_selected(q['state'],spec['state']['selected_fields']);raw=lambda prefix:{n[len(prefix):]:a for n,a in data.items() if n.startswith(prefix)}
 pair=lambda role:tuple(data[PLAN['paired_state_mapping'][role]['prefix']+'_'+w].copy() for w in ('hi','lo'))
 for n in ('B','GC','C','ALPHA','ELL'):assert data['candidate_raw_unchanged_material_'+n].shape==() and data['candidate_raw_unchanged_material_'+n].item()==getattr(P,n)
 phase_action=P.a_dd(np.zeros((3784,4,4)));ordinary=P.a_dd(np.zeros((3784,4,4)));updated=None
 for row,(r,rs) in enumerate(zip(q['rows'],spec['phase_rows'])):
  selectors=rs['selectors'];names=[n for v in selectors.values() for n in v.values()];d=read_selected(r,names)
  for role,target in (('phase_action',phase_action),('ordinary_Hamiltonian',ordinary)):
   for w,word in enumerate(('hi','lo')):target[w][:,row,0]=d[selectors[role][word]]
  if row==0:updated=tuple(d[selectors['updated_phase_covector'][w]].copy() for w in ('hi','lo'))
 s=raw('completed_candidate_s_');c=raw('completed_candidate_c_');assert np.array_equal(s['R'],BASIS['R'][iq])
 assert all(np.array_equal(a[:,1:].view(np.uint64),b[:,1:].view(np.uint64)) for a,b in zip(updated,P.a_dd(s['phi'])))
 keep('closed_raw225_Lie_beta_h_both_words',np.stack(pair('raw225_Lie_beta_h')).copy());keep('closed_formal160_Lie_beta_h_diagnostic_both_words',np.stack(pair('formal160_Lie_beta_h_diagnostic')).copy())
 column=dict(column=iq,candidate=dict(s=s,c=c),covectors=dict(u_jets=pair('u_jets'),z_jets=pair('z_jets')),mechanical=dict(h_dot=pair('h_dot')),gauge=dict(N_jets=pair('N_jets'),beta_jets=pair('beta_jets')),reference=dict(E0=pair('E0')),h_first=pair('h_first'),Lie_beta_h=pair('raw225_Lie_beta_h'),updated_phase_covector=updated,intrinsic_curvature=dict(Q=pair('intrinsic_Q'),V=pair('intrinsic_V')),fixed_terms=dict(phase_action=phase_action,ordinary_Hamiltonian=ordinary,relative_phase_count=1,ordinary_label_count=1),provenance=PROVENANCE['columns'][iq],fixed_geometry_identity_verified=True,updated_phase_identity_verified=True,unchanged_curvature_and_ordinary_identity_verified=True,owned_TOTAL_time_word_identity_verified=True)
 seal('BASELINE_COLUMN_INPUT',column,dict(column=iq,state=thin(q['state']),phase_rows=[thin(r) for r in q['rows']],raw225_Lie_authoritative_contact_Lie_retained=True,owned_TOTAL_time_words_copied_not_reconstructed=True))
 return column

class ColumnStream:
 def __init__(self,refs):self.refs=refs
 def __len__(self):return 4
 def __iter__(self):
  for q in self.refs:
   column=hydrate_column(q);yield column;del column

def packet(refs):
 global BASIS,PROVENANCE
 PROVENANCE=refs['provenance'];br=record(PLAN['basis']['ref']);BASIS=read_selected(br,PLAN['basis']['selectors'])
 sr=record(PLAN['unchanged_sheet']['ref']);ss=PLAN['unchanged_sheet']['selectors'];sd=read_selected(sr,list(ss.values()));sheet=tuple(sd[ss[w]].copy() for w in ('hi','lo'))
 d=read_selected(refs['solution'],('correction_hi','correction_lo','scores'));assert d['scores'].shape==(3,2) and np.all(d['scores']<=1e-10)
 fields=[P.unpack_fields(d['correction_'+w],False) for w in ('hi','lo')];native=tuple(q[0] for q in fields);metric=tuple(q[1] for q in fields)
 seal('INPUT',dict(native=native,metric=metric,scores=d['scores'],basis=BASIS,sheet=sheet),dict(original_input=refs['original_input'],correction=thin(refs['solution']),provenance=PROVENANCE,selected22_proof=SELECTED22_PROOF))
 stage=lambda kind,payload:seal(kind,payload,dict(provenance=PROVENANCE))
 increment=prepare_fixed_geometry_rate_increment(native,metric,BASIS,PROVENANCE,keep,'NEW_admitted_rate_increment',stage)
 normal_test=np.zeros((4,87,45));normal_test[:,43,22]=(1.,-2.,3.,4.);normal_test[:,43,0]=(1.,-2.,3.,4.);scalar_test=np.zeros((87,45));scalar_test[43,22]=1.
 def complete(iq,kind,payload):return seal(kind,payload,dict(column=iq,provenance=PROVENANCE['columns'][iq]))
 def row_complete(iq,row,jet,kind,payload):return seal(kind,payload,dict(column=iq,row=row,jet=jet,provenance=PROVENANCE['columns'][iq]))
 def column_complete(iq,part):return part['column_record']
 result=fixed_geometry_rate_state_packet(ColumnStream(refs['columns']),increment,sheet,refs['Hbar'],normal_test,scalar_test,keep,P.check,'NEW_FIXED_GEOMETRY_TOTAL_RATE',complete,row_complete,column_complete)
 readout=seal('READOUT',result,dict(kind_scope='fresh_point_first_TOTAL_rate_momenta_all16normal_CMC_at_unchanged_spatial_geometry',correction_original_six_admitted=True,new_current_original_six_admission_external=True,stationarity_feedback_and_geometry_solve_external=True,exact_geodesic_and_new43_external=True))
 expected=['NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_'+family+'_'+kind+'_polynomial_transpose' for family in ('value','delta') for kind in ('normal','CMC')];assert [c['name'] for c in CHECKS]==expected and all(c['passed'] is True for c in CHECKS)
 return dict(status='FIXED_GEOMETRY_ADMITTED_CORRECTION_TOTAL_RATE_VALUE_STATE_MEASURED_UNQUALIFIED',columns=result['columns'],readout=readout,original_targets=PROVENANCE['unchanged_original_targets'],correction=thin(refs['solution']),all16normal_ports_per_section=True,current99_and_physical6_fresh=True,spatial_geometry_unchanged=True,new_current_six_canonical_gates_or_normal_CMC_acceptance=False,stationarity_feedback_or_new43_earned=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and all(v is not None for q in (*BASELINE_CLOSURE,*UPDATED_PHASE_CLOSURE,*JOIN_CLOSURE,*CORRECTION_CLOSURE,SELECTED22_PROOF,FIXED_BINDING) for v in q),'Root FULL-reviewed selected-byte and admitted-correction release required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(IO_PARENT,IO_PARENT_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,selected22_proof=SELECTED22_PROOF,original_TOTAL_words=True,source_only_old_producer_replay=False,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  try:P.checkpoint('ERROR_RAW',{n:a.copy() for n,a in {**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}.items()},dict(context=dict(CONTEXT),kind='incomplete_TOTAL_rate_value_state'),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
