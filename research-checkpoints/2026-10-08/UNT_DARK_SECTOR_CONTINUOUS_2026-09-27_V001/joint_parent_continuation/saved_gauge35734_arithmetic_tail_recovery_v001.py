"""HELD35734 saved quotient continuation and43 unstarted gauge ports.
Original immutable caches only; no old20 ports/80 controls or EOS/current primal.
Root alone releases after FULL review and fresh owner absence. Inherited30 remain
outside current RECORDS. All original failures and damaged bytes stay unchanged.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,io,json,math,os,re,stat,types,traceback,zipfile
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='SAVED_GAUGE35734_ARITHMETIC_TAIL_RECOVERY_V001'
PROTOCOL='SAVED_GAUGE35734_ARITHMETIC_TAIL_RECOVERY_V001.md'
PROTOCOL_SHA='5e12e213ad7ef87e234fb7726abb33eda2b2da315589af53092722dabbd4f3d8'
ROOT_ADMISSION_PROOF=('ROOT_CLOSED_GAUGE35734_ARITHMETIC_TAIL_RECOVERY_ADMISSION_V001.json','ff21178b8484343d84bf48ce2769d4519055ab979c8b42e76c51a00f2dc028f9','ROOT_CLOSED_GAUGE35734_SELECTED_ARITHMETIC_TAIL_RECOVERY_ADMITTED_HELD')
EARNED_ROLE_PROOF=('ROOT_CLOSED_GAUGE35734_PARTIAL_SUCCESS_BYTE_SEALS_V001.json','66eb1d867f22fa09ab51ee0b3e5690a3a77d7ba398a9af6d7369d3cc7fd87961','ROOT_CLOSED_GAUGE35734_ALL30_SUCCESS_BYTE_SEALS_VERIFIED')
PHASE_CONSTANTS_COMMIT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_00005_PREPARATION.npz.COMMIT.json','38046436fac26fff119ef29f47165752db6f183ef8f819e9493cf14cffbffd5b')
TAIL_PROTOCOL=('SAVED_GAUGE35734_ARITHMETIC_TAIL_V001.md','aec6851aabd67cb20d90072a7d911accd0032688860a8dd09ac94694b43a2cbc')
np=P=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};ACTIVE_ARGUMENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_finite0_completed_state_restore_v002.py': 'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'author_fragment_candidate_gauge_registered_current_contact_v001.py': 'ac0502f41c6ad04208f5ef5610d43b3e11064a4b66eb73d076d43c959ffb0cdd', 'author_fragment_saved_gauge35734_arithmetic_tail_v003.py': '695fb232a1bc4dc8fc8a4dc0f935c4ab6e2eb32ce8c6a7ff372d5b2c4bc1a16d'}

def selected_definitions(file,names):
 assert PINS.get(file) is not None and hashlib.sha256((BASE/file).read_bytes()).hexdigest()==PINS[file]
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==len(names)
 return ast.Module(body=defs,type_ignores=[])

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 tree=ast.parse((BASE/IO_PARENT).read_text());names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==10
 exec(compile(ast.Module(body=defs,type_ignores=[]),IO_PARENT,'exec'),globals());initialize_io()
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,{'recheck'}),file,'exec'),SCOPE);P.recheck=SCOPE['recheck']

def initialize_tail_helpers():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum'}
 for file,names in ((list(PINS)[0],base),(list(PINS)[1],primitive)):exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 SCOPE.update(B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 for n in base|primitive|{'B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n]);globals()[n]=SCOPE[n]
 files=(('author_fragment_finite_york_geometry_target_v001.py',11),('author_fragment_finite_york_spacetime_first_jets_v001.py',20),('author_fragment_exact_exponent_two_product_v003.py',2),('author_fragment_compact_metric_contact_momenta_v002.py',7),('author_fragment_finite_candidate_configuration_contact_v001.py',5),('author_fragment_candidate_gauge_registered_current_contact_v001.py',6),('author_fragment_saved_gauge35734_arithmetic_tail_v003.py',8))
 for file,count in files:
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)};assert len(names)==count
  for n in tree.body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):globals()[n.targets[0].id]=ast.literal_eval(n.value)
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_cached_updated_phase_compact_chi_contact_v001.py';names={'cached_phase_product_direction','cached_phase_dot_direction','cached_phase_mv_direction','cached_phase_division_direction'}
 for n in ast.parse((BASE/file).read_text()).body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('EOS_SCALARS','EOS_VECTORS','EOS_MATRICES'):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 exec(compile(selected_definitions(file,names),file,'exec'),globals())
 file='author_fragment_finite0_completed_state_restore_v002.py';exec(compile(selected_definitions(file,{'finite0_saved_pair','finite0_saved_pair_family','finite0_saved_raw_family'}),file,'exec'),globals())
 globals().update(FINITE_YORK_AUTHOR_DRAFT=False,FINITE_SPACETIME_AUTHOR_DRAFT=False,FINITE_CANDIDATE_CONTACT_AUTHOR_DRAFT=False,EXACT_EXPONENT_PRODUCT_AUTHOR_DRAFT=False,GAUGE_CURRENT_AUTHOR_DRAFT=False,GAUGE_CURRENT_AUTHORING_IN_PROGRESS=False,GAUGE35734_TAIL_AUTHOR_DRAFT=False,GAUGE35734_ROOT_ADMISSION_PROOF=ROOT_ADMISSION_PROOF)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_saved_gauge_tail_exact_exponent_product')
 globals()['a_prod']=SCOPE['a_prod'];assert P.a_mul.__globals__ is SCOPE and SCOPE['a_prod'] is P.a_prod

def resolve_original(ref,owner):
 bind(ref['commit_file'],ref['commit_sha256']);r=json.loads(P.path(ref['commit_file']).read_text());assert r['file']==ref['file'] and r['sha256']==ref['sha256']
 md=r['metadata'];assert md['owner']==owner and md['failed'] is False and md['physical_adoption'] is False and md['qualification']==FLAGS
 return dict(r,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256'])

def read_selected(ref,names):
 bind(ref['file'],ref['sha256']);schema=ref['metadata']['schema'];assert len(names)==len(set(names)) and set(names)<=set(schema)
 out={}
 with np.load(P.path(ref['file']),allow_pickle=False) as f:
  assert set(f.files)==set(schema)|{'metadata_json'} and json.loads(str(f['metadata_json']))==ref['metadata']
  for n in names:
   a=f[n].copy();ACTIVE_ARGUMENT['loaded_'+n]=a;keep('loaded_'+n,a);s=schema[n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and np.all(np.isfinite(a));out[n]=a
 return out

def recovery_admission():
 for q in (ROOT_ADMISSION_PROOF,EARNED_ROLE_PROOF,PHASE_CONSTANTS_COMMIT,TAIL_PROTOCOL):bind(q[0],q[1])
 admitted=gauge35734_tail_admission();earned=json.loads(P.path(EARNED_ROLE_PROOF[0]).read_text());proof=admitted['proof']
 assert proof['earned_role_proof']==dict(file=EARNED_ROLE_PROOF[0],sha256=EARNED_ROLE_PROOF[1]) and earned['status']==EARNED_ROLE_PROOF[2]
 assert earned['owner']==proof['owner'] and earned['verified_roles']==30 and earned['all30_committed_role_seals_verified'] is True and earned['pending']==[]
 assert earned['controls']==proof['original80_control_descriptors'] and len(earned['controls'])==80 and all(q['passed'] is True and q['tolerance']==2e-11 for q in earned['controls'])
 refs=[resolve_original(q,proof['owner']) for q in earned['records']];assert len(refs)==30
 assert [r['metadata']['role'] for r in refs]==['INPUT','CACHE_COLUMN','COMPONENT_INPUT','COMPONENT_CONTACT','COMPONENT_INPUT','COMPONENT_CONTACT','CACHE_COLUMN','CACHE_COLUMN','CACHE_COLUMN']+['GAUGE_TEST']*16+['COLUMN']+['GAUGE_TEST']*4
 assert [thin(refs[j]) for j in (1,6,7,8)]==proof['cache_by_column']
 im=refs[0]['metadata'];assert [q['name'] for q in earned['controls']]==im['expected_control_names'] and im['current_targets_and_epsilon_unchanged'] is True
 cm=json.loads(P.path(PHASE_CONSTANTS_COMMIT[0]).read_text())['metadata'];assert cm['owner']['pid']==19724 and cm['failed'] is False and cm['physical_adoption'] is False and cm['old_preupdate_H_or_diagonal_used'] is False
 constants=dict(cm['constants']);assert constants['eps']==1e-5 and constants['synthetic_control'] is False and constants['relative_phase_coefficient']==1. and constants['physical_constants_selected_or_fitted'] is False
 return admitted,refs,constants

def hydrate_closed_cache(ref,iq,constants,owner):
 md=ref['metadata'];assert md['column']==iq and md['input']==thin(INHERITED[0]) and md['EOS_primal_or_action_replayed'] is False
 prefix='column%d_copied_STATE_'%iq;families=('completed_candidate_s_','completed_candidate_c_','completed_candidate_jets_','completed_candidate_features_','completed_candidate_momenta_','completed_candidate_KADM_','candidate_raw_coefficient_operation_','candidate_raw_new_first_operation_','NEW_reference_input_geometry_','NEW_reference_input_gauge_','NEW_reference_input_covectors_','NEW_reference_input_mechanical_','NEW_reference_input_reference_','candidate_raw_unchanged_material_')
 names=[n for n in md['schema'] if n.startswith(tuple(prefix+x for x in families)) or n.startswith('column%d_cached_EOS_'%iq) and not n.endswith('_both_words') or n in ('column%d_phase_updated_hi'%iq,'column%d_phase_updated_lo'%iq)]
 data=read_selected(ref,tuple(names));state={n[len(prefix):]:a for n,a in data.items() if n.startswith(prefix)};raw=lambda q:finite0_saved_raw_family(state,q);pairs=lambda q:finite0_saved_pair_family(state,q)
 s=raw('completed_candidate_s_');c=raw('completed_candidate_c_');assert len(c['N'])==3784 and np.array_equal(s['R'],BASIS['R'][iq])
 for n in ('B','GC','ALPHA','ELL','C'):assert state['candidate_raw_unchanged_material_'+n].item()==getattr(P,n)
 candidate=dict(s=s,c=c,jets=pairs('completed_candidate_jets_'),features=dict(constants={n:s[n] for n in ('g','hi','U','z','P','uc','Z','r','z2','f','phi','omega','xi','w')},paired=pairs('completed_candidate_features_'),configuration_changed=False,candidate_configuration_rebuilt=True),momenta=pairs('completed_candidate_momenta_'),KADM=finite0_saved_pair(state,'completed_candidate_KADM'),coefficient_envelopes=raw('candidate_raw_coefficient_operation_'),positive_first_jet_envelopes=raw('candidate_raw_new_first_operation_'),physical_adoption=False)
 tr=md['temporal_cache'];bind(tr['commit_file'],tr['commit_sha256']);tm=json.loads(P.path(tr['commit_file']).read_text());assert tm['file']==tr['file'] and tm['sha256']==tr['sha256'] and tm['metadata']['state']==md['state'] and tm['metadata']['column']==iq
 fm=md['updated_phase'];bind(fm['commit_file'],fm['commit_sha256']);fd=json.loads(P.path(fm['commit_file']).read_text());assert fd['file']==fm['file'] and fd['sha256']==fm['sha256'] and fd['metadata']['owner']['pid']==13764 and fd['metadata']['state']==md['state']
 ep='column%d_cached_EOS_'%iq;pair=lambda q:(data[ep+q+'_hi'].copy(),data[ep+q+'_lo'].copy());phase_s={n:pair('same_candidate_'+n) for n in ('hi','P','phi','U','uc')};phase_c={n:pair('same_candidate_'+n) for n in ('N','mu','ih','u')};values={n:pair('copied_'+n) for n in {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}}
 phi=finite0_saved_pair(data,'column%d_phase_updated'%iq);assert all(np.array_equal(a,b) for a,b in zip(phi,phase_s['phi'])) and all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(phi,P.a_dd(s['phi'])))
 for n in ('hi','P','U','uc'):assert all(np.array_equal(a,b) for a,b in zip(phase_s[n],P.a_dd(s[n])))
 for n,q in (('N','N'),('mu','sqrt_h'),('ih','ih'),('u','u')):assert all(np.array_equal(a,b) for a,b in zip(phase_c[n],P.a_dd(c[q])))
 for n in ('X0','norm'):assert all(np.array_equal(a,b) for a,b in zip(values[n],P.a_dd(np.full(3784,constants[n]))))
 assert np.all(values['X'][0]-abs(values['X'][1])>0) and np.all(values['u'][0]-abs(values['u'][1])>0) and np.all(constants['eps']-values['u'][0]-abs(values['u'][1])>0)
 provenance=dict(same_candidate_geometry_and_current_mechanical_rates=True,original_state=md['state'],updated_phase=fm,ownership=tm['metadata']['candidate_provenance']['ownership'],phi_only_update_leaves_native_EH_mechanical_action_invariant=True,physical_adoption=False)
 phase=dict(s=phase_s,c=phase_c,values=values,constants=dict(constants),candidate_provenance=fd['metadata']['candidate_provenance'],EOS_values_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False)
 column=dict(candidate=candidate,phase=phase,constants=tm['metadata']['constants'],provenance=provenance,same_candidate_provenance=provenance,updated_phase_pair=phi,recovery_closed_cache_ref=thin(ref),gauge_target_derivative_zero=True,physical_adoption=False)
 for key in ('geometry','gauge','covectors','mechanical','reference'):column[key]=pairs('NEW_reference_input_'+key+'_')
 ACTIVE_ARGUMENT.clear();AVAILABLE.clear();RAW.clear();DD_ARRAY_CURRENT.clear();return column

def survivor_member_reader(file,row):
 assert file==ADMITTED['audit']['orphan_file'] and row in ADMITTED['audit']['selected_members']
 if not ORPHAN_VERIFIED:
  st=P.path(file).stat();assert stat.S_IMODE(st.st_mode)==0o444 and st.st_size==ADMITTED['audit']['orphan_bytes'];bind(file,ADMITTED['audit']['orphan_sha256']);ORPHAN_VERIFIED.append(True)
 with zipfile.ZipFile(P.path(file)) as z:
  info=z.getinfo(row['member']);assert info.file_size==row['uncompressed_bytes'] and info.CRC==row['CRC32'];raw=z.read(info)
 assert len(raw)==row['uncompressed_bytes'] and hashlib.sha256(raw).hexdigest()==row['member_sha256']
 stream=io.BytesIO(raw);version=np.lib.format.read_magic(stream);shape,fortran,dtype=np.lib.format._read_array_header(stream,version);assert list(shape)==row['shape'] and fortran is False and dtype.str==row['dtype']
 a=np.load(io.BytesIO(raw),allow_pickle=False);ACTIVE_ARGUMENT['selected_'+row['member']]=a;assert a.dtype==np.float64 and np.all(np.isfinite(a));return a

def flat_words(prefix,value,out):
 if isinstance(value,dict):
  for n,x in value.items():flat_words(prefix+n+'_',x,out)
 elif isinstance(value,tuple) and len(value)==2 and all(isinstance(x,np.ndarray) for x in value):out[prefix+'hi']=value[0].copy();out[prefix+'lo']=value[1].copy()
 elif isinstance(value,tuple) and len(value)==2 and all(isinstance(x,tuple) for x in value):flat_words(prefix+'value_',value[0],out);flat_words(prefix+'delta_',value[1],out)
 elif isinstance(value,np.ndarray):out[prefix[:-1]]=value.copy()
 return out

def compact_seal(role,data,meta):
 rec=P.checkpoint(role,data,dict(meta,role=role,root_admission=ROOT_ADMISSION_PROOF,physical_adoption=False));saved_context=dict(CONTEXT)
 AVAILABLE.clear();RAW.clear();DD_ARRAY_CURRENT.clear();CONTEXT.clear();CONTEXT.update(saved_context);return thin(rec)

def selection_complete(data,meta):
 ref=compact_seal('SURVIVOR_SELECTION',{n[:-4]:a.copy() for n,a in data.items()},dict(meta,kind='copied118_CRC_complete_survivors_not_original_orphan_COMMIT'));ACTIVE_ARGUMENT.clear();return ref

def tail_complete(stage,value):
 data=flat_words('completed_'+stage+'_',value,{})
 if stage=='resumed_first_division':data.update({n:a.copy() for n,a in AVAILABLE.items()})
 ref=compact_seal('DIVISION_TAIL' if stage=='resumed_first_division' else 'RAW_MECHANICAL_TAIL',data,dict(kind=stage,original_port=[1,1,0],selection=SELECTION_REF[0],recomputed_unserialized_suffix=True,original_lost_tail_bitwise_equality_NOT_claimed=True));TAIL_REFS.append(ref);return ref

def test_complete(iq,row,jet,part,out):
 data=flat_words('completed_NEW_gauge_',part,{});direction=gauge35734_unit_direction(3784,row,jet);flat_words('supplied_gauge_',direction,data)
 for n,x in part['canonical_point_contact'].items():
  index=(slice(None),row,jet) if n=='phase' else (slice(None),slice(None),row,jet)
  assert all(np.array_equal(out[n][w][index],x[w]) for w in (0,1))
 if jet>0:assert all(np.all(a==0) for a in part['canonical_point_contact']['phase'])
 ref=compact_seal('GAUGE_TEST',data,dict(kind='NEW_gauge_registered_mechanical_and_UPDATED_literal_phase_point_contact',column=iq,row=row,jet=jet,input=thin(INHERITED[0]),cache=thin(INHERITED[(1,6,7,8)[iq]]),coordinate_order=('value','R','Z','t'),genuine99_and_physical6=True,all_primary_time_jets_retained=True,phase_firstjet_port_bothwords_zero=jet>0,target_derivative_zero=True,C_equals_minus_Rv_or_Schwarz_assumed=False,tail_refs=TAIL_REFS.copy() if (iq,row,jet)==(1,1,0) else []));ACTIVE_ARGUMENT.clear();return ref

def column_complete(iq,part):
 data=flat_words('completed_NEW_gauge_column_',{'coefficients':part['coefficients']},{})
 return compact_seal('COLUMN',data,dict(kind='NEW_all16_gauge_current_coefficient_inventory',column=iq,input=thin(INHERITED[0]),cache=thin(INHERITED[(1,6,7,8)[iq]]),test_refs=part['completed_test_refs'],native_shape=(3784,99,4,4),metric_shape=(3784,6,4,4),phase_shape=(3784,4,4),native_E_metric_F_scalar_left_scatter_and_normal_test_transpose_external=True))

def recovery_packet(admitted,refs,constants):
 global ADMITTED,INHERITED,BASIS
 ADMITTED=admitted;INHERITED=refs;basis=read_selected(refs[0],tuple(refs[0]['metadata']['schema']));BASIS={n.removeprefix('copied_original_basis_'):a for n,a in basis.items()};assert BASIS['R'].shape==BASIS['dv'].shape==(4,3784) and BASIS['hats'].shape==(4,4,3,86,44) and np.all(BASIS['R']>0) and np.all(BASIS['dv']>0)
 columns=[dict(recovery_closed_cache_ref=thin(refs[1]))]+[hydrate_closed_cache(refs[(1,6,7,8)[iq]],iq,constants,admitted['proof']['owner']) for iq in (1,2,3)]
 inventories=[{}];tag='NEW_actual_gauge_current_column1_completed_';names=tuple(tag+n+'_gauge_coefficient_inventory_'+w for n in ('native','metric','phase') for w in ('hi','lo'));old=read_selected(refs[29],names);inventories.append({n:pair_from(old,tag+n+'_gauge_coefficient_inventory') for n in ('native','metric','phase')})
 for iq in (2,3):inventories.append({n:P.a_dd(np.zeros(shape)) for n,shape in (('native',(3784,99,4,4)),('metric',(3784,6,4,4)),('phase',(3784,4,4)))})
 tests=[[thin(r) for r in refs[9:25]],[thin(r) for r in refs[26:30]],[],[]]
 CONTEXT.update(column=1,row=1,jet=0,stage='selected_survivor_restore');restored=gauge35734_restore_tail_selection(admitted,columns[1],survivor_member_reader,selection_complete,keep,'NEW_saved_gauge35734');SELECTION_REF.append(restored['selection_ref'])
 # Persistent active arguments survive every compact checkpoint clear.
 ACTIVE_ARGUMENT.update(saved_frame=flat_words('frame_',restored['frame'],{}),saved_division=flat_words('division_',restored['division'],{}))
 result=gauge35734_continue_remaining_ports(admitted,columns,restored,inventories,tests,thin(refs[25]),keep,'NEW_actual_gauge_current',test_complete,column_complete,tail_complete)
 prep=compact_seal('PREPARATION',{},dict(kind='NEW_candidate_gauge_registered_current_forward_block',input=thin(refs[0]),cache_columns=[thin(refs[j]) for j in (1,6,7,8)],component_refs=[dict(input=thin(refs[2]),contact=thin(refs[3])),dict(input=thin(refs[4]),contact=thin(refs[5]))],columns=result['completed_column_refs'],tests=result['completed_test_refs'],controls=80,all64_ports_retained=True,original_E_F_scalar_scatter_and_normal_test_transpose_external=True,canonical_targets_and_current_values_unchanged=True,represented_forward_only=True,C_equals_minus_Rv_assumed=False,all_time_primary_coefficients_retained=True,fullweak_Cstar_or_feedback_external=True))
 assert len(RECORDS)==51 and not CHECKS and len(TAIL_REFS)==2
 assert [r['metadata']['role'] for r in RECORDS].count('GAUGE_TEST')==44 and [r['metadata']['role'] for r in RECORDS].count('COLUMN')==3
 return dict(result,status='CANDIDATE_GAUGE_REGISTERED_CURRENT_FORWARD_CONTACTS_MEASURED',input=thin(refs[0]),cache_columns=[thin(refs[j]) for j in (1,6,7,8)],component_refs=[dict(input=thin(refs[2]),contact=thin(refs[3])),dict(input=thin(refs[4]),contact=thin(refs[5]))],columns=result['completed_column_refs'],tests=result['completed_test_refs'],preparation=prep,inherited_checkpoints=[thin(r) for r in refs],controls=80,new_controls=0,current_roles=51,new_scientific_roles=48,inherited_scientific_roles=30,logical_scientific_roles=78,auxiliary_roles=3,original_control_descriptors=admitted['proof']['original80_control_descriptors'])

def keep_tail(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a
 match=re.search(r'_column(\d+)_row(\d+)_jet(\d+)',name)
 if match:CONTEXT.update(column=int(match[1]),row=int(match[2]),jet=int(match[3]),stage=name)
 if '_supplied_gauge_' in name:ACTIVE_ARGUMENT[name]=a.copy()
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));return a

ADMITTED=None;INHERITED=[];BASIS={};ORPHAN_VERIFIED=[];SELECTION_REF=[];TAIL_REFS=[]

def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None and all(x is not None for x in ROOT_ADMISSION_PROOF)
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();globals()['keep']=keep_tail;SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(PROTOCOL,PROTOCOL_SHA)
  for name,h in PINS.items():bind(name,h)
  initialize_tail_helpers();admitted,refs,constants=recovery_admission()
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,admission=ROOT_ADMISSION_PROOF,inherited30=[thin(r) for r in refs],original_controls=admitted['proof']['original80_control_descriptors'],current_roles=51,logical_scientific_roles=78,new_controls=0,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=recovery_packet(admitted,refs,constants)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=admitted['proof']['original80_control_descriptors'],new_controls=CHECKS,checkpoints=RECORDS,inherited_checkpoints=[thin(r) for r in refs],qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(RECORDS),80,rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',flat_words('active_',ACTIVE_ARGUMENT,{**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_selected_gauge35734_arithmetic_tail_only',context=dict(CONTEXT),inherited30=[thin(r) for r in INHERITED]),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),checkpoints=RECORDS,inherited_checkpoints=[thin(r) for r in INHERITED],input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise

if __name__=='__main__':raise SystemExit(main())
