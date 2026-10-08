"""HELD actual saved-cache phase-rate numerical coefficient preparation.
One NEW point-unit direction per section; no old VALUE/preparation/action replay.
Original157 arbitrary direction and fresh finite constraints remain authoritative.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='SAVED_PHASE_RATE_UNIT_COEFFICIENT_PREPARATION_V001'
DRIVER_PROTOCOL='SAVED_PHASE_RATE_UNIT_COEFFICIENT_PREPARATION_V001.md'
PROTOCOL_SHA='a827fabf0281b2b9987cf42c0e6f717cde9c69ed4f2092bf899bf2052292b882'
CACHE_SOURCE=(None,None)
CACHE_RESULT=(None,None,'CACHED_UPDATED_PHASE_TEMPORAL_FOUR_NORMAL_CONTACTS_MEASURED')
CACHE_RECEIPT=(None,None,'CLOSED')
CACHE_PROOF=(None,None,None)
COUPLED_INVARIANT_CLOSURES={'phase_rate_cache':(None,None,None,None)}
np=P=N=K=None
SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={};REFERENCE_METADATA=[]
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
SUPPORT_SOURCE=('cross_u_cached_updated_phase_compact_chi_contact_v003.py','4f6f6c2db02bfe97e2c4132e16fc592050c3a3cd23876eaf96e4589b871dc2ab')
COMPONENT_PROTOCOL=('CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V001.md','14f9c9d3a8970bed81bdd771b9ba0c5030c280439a84c9506cf825bc1b567aa3')
RATE_COMPONENT_PROTOCOL=('CACHED_UPDATED_PHASE_TEMPORAL_NORMAL_V002.md','6c0ace7fede2f6dc6fe26b526fae3135bdc2df6669d7013f8e3c4cab1139d9d6')
MASS_SOURCE=('cross_u_updated_finite_phase_mass_preparation_v002.py','76a929447f2a0ed968825872e57ce2cf309fb49eeff13a1d8916ae3becb374cc')
MASS_RESULT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RESULT.json','9febbd8cd23e96efbec23ffb6d24323d8b2ac99aaef5e73ce903bf49660b47c5','UPDATED_FINITE_PHASE_LITERAL_MASS_CACHE_PREPARED_UNQUALIFIED')
MASS_RECEIPT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RECEIPT.json','69e25ed8a9c413f7c153a69e976a9f36cb3636fd67a8193eb3138514a2be2872','CLOSED')
MASS_PROOF=('ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_V001.json','2b6d27847c8b70d592209d117dbc18f7ee0e41f8ed454d684734ec03d92ed662','ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_VERIFIED')
POINT_CELLS=((42, 21), (42, 22), (43, 21), (43, 22))
SHAPES={'g': (4, 4), 'hi': (4, 4), 'U': (4,), 'uc': (4,), 'P': (4, 4), 'phi': (4,), 'N': (), 'mu': (), 'h': (3, 3), 'beta': (3,), 'ih': (3, 3), 'u': (3,)}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_fixed_geometry_phase_normal_join_v001.py': '7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_candidate_finite_phase_state_update_v001.py': 'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'author_fragment_cached_phase_chi_fraction_reference_v001.py': '414ed54d382a1e644a7a8ba9847881d1b53fa2e76d480de7b4c223cf00940b43', 'author_fragment_phase_literal_charge_hessian_v002.py': '293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143', 'author_fragment_candidate_literal_phase_mass_v001.py': '0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38', 'author_fragment_cached_updated_phase_temporal_normal_v002.py': 'b60d4bc3823439910843f10661dc960035bdad9af78ff3326cd4bc702474bf44', 'author_fragment_cached_phase_rate_fraction_reference_v001.py': '0a9dcc2f6caef474dc43766b44a5e43290734098c35c5b90669230f2e29a9af7'}
SUPPORT_NAMES={'selected_definitions','load_io','read_closed','clear_completed','seal_completed','initialize_helpers','reference_items','rational_control'}
PINS['cross_u_candidate_right_only_mechanical_response_v002.py']='cfd84a72031bd059b767a4be1b675c398685eed6620836dc9f716436192eab00'
INITIALIZER_SOURCE=('cross_u_cached_updated_phase_temporal_normal_controls_v002.py','e1449a16eae52f69494b03aa906a8e0d3ddda1c7c0f9fad060fa1fc80889f1ca')
FIXED_POINT_INDEX=(42*44+21,42*44+22,43*44+21,43*44+22)
EXPECTED_ROLES=['INPUT']+(['CACHE_COPY','UNIT_EOS']+['UNIT_NORMAL_ROW']*4+['UNIT_COLUMN'])*4+['PREPARATION']
EXPECTED_CONTROLS=['column%d_NEW_unit_fraction_%s'%(iq,n) for iq in range(4) for n in ('p','H','normal0','normal1','normal2','normal3')]


def load_support():
 assert hashlib.sha256((BASE/SUPPORT_SOURCE[0]).read_bytes()).hexdigest()==SUPPORT_SOURCE[1]
 tree=ast.parse((BASE/SUPPORT_SOURCE[0]).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in SUPPORT_NAMES];assert len(defs)==len(SUPPORT_NAMES)
 exec(compile(ast.Module(body=defs,type_ignores=[]),SUPPORT_SOURCE[0],'exec'),globals());load_io()

def initialize_rate_helpers():
 global K,RATE_EOS_NAMES,RATE_NORMAL_NAMES,RATE_CHAIN_NAMES
 initialize_helpers()
 file='author_fragment_phase_literal_charge_hessian_v002.py';names={'phase_pair_keep','phase_scalar_value'};scope=dict(np=np,P=P)
 exec(compile(selected_definitions(file,names),file,'exec'),scope);K=types.SimpleNamespace(**{n:scope[n] for n in names})
 for file,names,count in (('author_fragment_candidate_literal_phase_mass_v001.py',{'candidate_phase_mass_pair','candidate_phase_mass_spatial_jets','candidate_phase_mass_action'},3),('author_fragment_cached_updated_phase_temporal_normal_v002.py',None,4),('author_fragment_cached_phase_rate_fraction_reference_v001.py',None,1)):
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if names is None else names;assert len(names)==count
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(CACHED_UPDATED_PHASE_RATE_AUTHOR_DRAFT=False,CACHED_UPDATED_PHASE_RATE_AUTHORING_IN_PROGRESS=False,PHASE_RATE_FRACTION_AUTHOR_DRAFT=False,PHASE_RATE_FRACTION_AUTHORING_IN_PROGRESS=False)
 file='author_fragment_cached_updated_phase_temporal_normal_v002.py';defs={n.name:n for n in ast.parse((BASE/file).read_text()).body if isinstance(n,ast.FunctionDef)}
 eos=defs['cached_updated_phase_eos_temporal_rate'];delta=next(n.value for n in ast.walk(eos) if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='delta' for a in n.targets))
 assert isinstance(delta,ast.Call) and isinstance(delta.func,ast.Name) and delta.func.id=='dict' and not delta.args
 RATE_EOS_NAMES=tuple(k.arg for k in delta.keywords);assert len(set(RATE_EOS_NAMES))==len(RATE_EOS_NAMES) and all(RATE_EOS_NAMES)
 normal=next(n.value for n in ast.walk(defs['cached_updated_phase_normal_temporal_rate']) if isinstance(n,ast.Return));nd=next(k.value for k in normal.keywords if k.arg=='delta')
 RATE_NORMAL_NAMES=tuple(k.arg for k in nd.keywords);assert RATE_NORMAL_NAMES==('absolute','relative','action','hamiltonian')
 chain=next(n.iter for n in ast.walk(eos) if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and [q.id for q in n.target.elts if isinstance(q,ast.Name)]==['n','actual','expected'])
 RATE_CHAIN_NAMES=tuple(ast.literal_eval(q.elts[0]) for q in chain.elts);assert RATE_CHAIN_NAMES==('P','PX','PXX')

def admit_current_mass(refs):
 for ref in (MASS_SOURCE,MASS_RESULT,MASS_RECEIPT,MASS_PROOF):assert all(q is not None for q in ref);bind(ref[0],ref[1])
 result,receipt,proof=(json.loads(P.path(q[0]).read_text()) for q in (MASS_RESULT,MASS_RECEIPT,MASS_PROOF))
 assert [q['status'] for q in (result,receipt,proof)]==[MASS_RESULT[2],MASS_RECEIPT[2],MASS_PROOF[2]]
 assert result['owner']==receipt['owner']==proof['owner'] and result['owner']['pid']==19724 and result['owner']['source_sha256']==proof['source_sha256']==MASS_SOURCE[1]
 assert receipt['result_sha256']==proof['result_sha256']==MASS_RESULT[1] and proof['receipt_sha256']==MASS_RECEIPT[1] and receipt['error_sha256'] is None
 assert proof['naturally_closed'] is True and type(proof['exit_code']) is int and proof['exit_code']==0 and type(proof['input_seals_verified']) is int and proof['input_seals_verified']==len(receipt['input_sha256']) and type(proof['output_seals_verified']) is int and proof['output_seals_verified']==len(receipt['output_sha256']) and proof['all_success_role_seals_verified'] is True
 assert result['qualification']==receipt['qualification']==FLAGS and proof['physical_adoption'] is False and proof['strict_current_H_and_diagonal_positive'] is True
 stem=MASS_RESULT[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 case=result['case'];prep=bind_record(case['preparation']);assert len(result['checkpoints'])==6 and result['controls']==[] and prep in result['checkpoints']
 terminal=case['finite_terminal'];assert [terminal[k] for k in ('source','result','receipt','proof')]==json.loads(json.dumps(refs['finite_terminal']))
 assert case['basis']==thin(refs['basis']) and case['original_literal_phase_charge']==thin(refs['prior']) and case['updated_phase_H_p_used'] is case['new_diagonal_only'] is case['original_charge_target_unchanged'] is True
 assert case['compact_chi_contact_earned'] is case['linear_or_finite_response_admitted'] is case['physical_adoption'] is False
 md=prep['metadata'];assert md['owner']==result['owner'] and md['failed'] is False and md['current_H_and_p_tied_to_closed_finite_phase'] is md['point_H_strictly_positive'] is md['point_H_resolved_positive'] is True
 assert md['phase_space_dofs']==3870 and md['phase_outer_top_free'] is True and md['old_preupdate_H_or_diagonal_used'] is md['EOS_current_normal_CMC_action_or_solver_replayed'] is md['physical_adoption'] is False
 assert md['basis']==thin(refs['basis']) and md['prior_literal_weak_charge']==thin(refs['prior'])
 for q in result['checkpoints']:
  assert q['metadata']['owner']==result['owner'] and q['metadata']['failed'] is False
  for n,h in (('file','sha256'),('commit_file','commit_sha256')):assert receipt['output_sha256'][q[n]]==q[h]
 columns=[bind_record(q) for q in case['columns']];assert [q['metadata']['column'] for q in columns]==[0,1,2,3] and md['columns']==[thin(q) for q in columns]
 for iq,q in enumerate(columns):assert q['metadata']['finite_phase']==thin(refs['columns'][iq]['new'])
 for n,shape in [('updated_phase_mass_candidate_H_'+w,[15136]) for w in ('hi','lo')]+[('updated_phase_mass_uncancelled_H_envelope',[15136])]+[('updated_phase_mass_NEW_basis_'+n,shape) for n,shape in (('R',[4,3784]),('dv',[4,3784]),('hats',[4,4,3,86,44]))]:assert md['schema'][n]['shape']==shape and md['schema'][n]['dtype']=='float64'
 return dict(preparation=prep,terminal=(MASS_SOURCE,MASS_RESULT,MASS_RECEIPT,MASS_PROOF),source_qualification=result['qualification'])

def coupled_pair(label,x,shape):
 assert isinstance(x,tuple) and len(x)==2
 keep(label+'_both_words',np.stack(x).copy())
 for word,a in zip(('hi','lo'),x):
  keep(label+'_'+word,a.copy());assert a.dtype==np.float64 and a.shape==shape and np.all(np.isfinite(a))
 return tuple(a.copy() for a in x)

def coupled_saved_phase_names(iq):
 assert type(iq) is int and 0<=iq<4
 e='column%d_cached_EOS_'%iq;n=[]
 for key in {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}:n.extend(e+'copied_'+key+'_'+w for w in ('hi','lo'))
 for name in ('hi','P','phi','U','uc','N','mu','ih','u'):n.extend(e+'same_candidate_'+name+'_'+w for w in ('hi','lo'))
 n.extend(e+'inherited_'+name for name in ('elementary_low_over_high','elementary_log_high','elementary_log1p_low'))
 for name in ('P','PX','PXX'):
  for kind in ('actual','expected','gap'):n.extend(e+'inherited_temporal_chain_'+name+'_'+kind+'_'+w for w in ('hi','lo'))
 for name in EOS_DIVISION_GAPS:n.extend(e+'inherited_primal_division_gap_'+name+'_'+w for w in ('hi','lo'))
 n.extend(e+'inherited_primal_'+name for name in ('current_operation_envelope','H_operation_envelope'))
 for row in range(4):
  p='cache_column%d_row%d_'%(iq,row)
  for name in NORMAL_FIELDS:n.extend(p+'copied_normal_'+name+'_'+w for w in ('hi','lo'))
  for name in ('g','hi','U','uc','P','phi','N','mu','h','beta'):n.extend(p+'same_cached_normal_'+name+'_'+w for w in ('hi','lo'))
  for name in ('It_phi','It_r','hi_rt'):n.extend(p+'NEW_fixed_contact_coefficient_'+name+'_'+w for w in ('hi','lo'))
  n.extend(p+'same_'+name for name in ('fixed_test_lapse','fixed_test_shift'))
  for name in ('X','pressure','PX'):n.extend(p+'same_cached_EOS_'+name+'_'+w for w in ('hi','lo'))
  for name in ('EOS_clock_square_contact','measure_test_trace_contact','unit_constraint','projector_construction_contact'):n.extend(p+'inherited_'+name+'_'+w for w in ('hi','lo'))
 assert len(n)==len(set(n));return tuple(n)

def coupled_hydrate_phase_rate_column(ref,data,constants,normal_s,normal_c,current_H,expected,keep,label):
 # Data are selected immutable28110 cache operands, not a new EOS/row action.
 md=ref['metadata'];iq=md['column'];p=3784;e='column%d_cached_EOS_'%iq
 assert md['role']=='TEMPORAL_CACHE_COLUMN' and md['kind']=='copied_updated_EOS_normal_primal_and_NEW_fixed_rate_derivative_coefficients'
 assert md['failed'] is md['physical_adoption'] is False and md['owner']['pid']==28110
 assert md['owner']['source_sha256']=='5c595057f4311bce62f4b76345d38b578cc6295492b488a954028a04179a5c38'
 assert expected['naturally_closed'] is True and expected['all_selected_seals_verified'] is True and expected['source_rate_independent_operands_verified'] is True
 assert md['state']==expected['state'] and md['finite_phase_column']==expected['finite_phase_column'] and md['normal_rows']==expected['normal_rows']
 assert md['input']==expected['input'] and md['new_fixed_coefficients']==['It_phi','It_r','hi_rt'] and md['old_chi_and_temporal_step_not_used_as_rate_direction'] is True
 assert expected['closure']==COUPLED_INVARIANT_CLOSURES['phase_rate_cache'] and all(x is not None for q in expected['closure'] for x in q)
 assert set(data)==set(coupled_saved_phase_names(iq))
 pair=lambda name,shape:coupled_pair(label+'_copied_'+name,tuple(data[name+'_'+w].copy() for w in ('hi','lo')),shape)
 values={key:pair(e+'copied_'+key,(p,4,4) if key in EOS_MATRICES else (p,4) if key in EOS_VECTORS else (p,)) for key in {**EOS_SCALARS,**EOS_VECTORS,**EOS_MATRICES}}
 s={n:normal_s[n] for n in ('hi','P','phi','U','uc')};c={n:normal_c[n] for n in ('N','mu','ih','u')}
 for family,shapes in ((s,dict(hi=(p,4,4),P=(p,4,4),phi=(p,4),U=(p,4),uc=(p,4))),(c,dict(N=(p,),mu=(p,),ih=(p,3,3),u=(p,3)))):
  for name,shape in shapes.items():
   saved=pair(e+'same_candidate_'+name,shape);assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(saved,family[name]))
 assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(values['H'],current_H))
 assert constants['eps']==1e-5 and constants['C']==1.98 and constants['relative_phase_coefficient']==1. and constants['synthetic_control'] is False
 for n in ('X0','norm'):assert all(np.array_equal(a,b) for a,b in zip(values[n],P.a_dd(np.full(p,constants[n]))))
 assert np.all(values['X'][0]-abs(values['X'][1])>0) and np.all(values['u'][0]-abs(values['u'][1])>0) and np.all(constants['eps']-values['u'][0]-abs(values['u'][1])>0)
 inherited={}
 for n in ('elementary_low_over_high','elementary_log_high','elementary_log1p_low'):
  x=keep(label+'_inherited_'+n,data[e+'inherited_'+n].copy());assert x.dtype==np.float64 and x.shape==(p,) and np.all(np.isfinite(x));inherited[n]=x
 for n in ('P','PX','PXX'):
  for kind in ('actual','expected','gap'):inherited[n+'_'+kind]=pair(e+'inherited_temporal_chain_'+n+'_'+kind,(p,))
 for n in EOS_DIVISION_GAPS:inherited['division_'+n]=pair(e+'inherited_primal_division_gap_'+n,(p,4) if n=='clock_normalization' else (p,))
 for n,shape in (('current_operation_envelope',(p,4)),('H_operation_envelope',(p,))):
  x=keep(label+'_inherited_'+n,data[e+'inherited_primal_'+n].copy());assert x.dtype==np.float64 and x.shape==shape and np.all(np.isfinite(x)) and np.all(x>=0);inherited[n]=x
 eos=dict(values=values,s=s,c=c,constants=dict(constants),candidate_provenance=expected['phase_provenance'],EOS_values_recomputed=False,old_temporal_direction_reused=False,physical_adoption=False,inherited_stage_contacts=inherited)
 rows=[]
 for row in range(4):
  rp='cache_column%d_row%d_'%(iq,row);test={n:pair(rp+'copied_normal_'+n,(p,)+shape) for n,shape in NORMAL_FIELDS.items()}
  for family,shapes in ((normal_s,dict(g=(p,4,4),hi=(p,4,4),U=(p,4),uc=(p,4),P=(p,4,4),phi=(p,4))),(normal_c,dict(N=(p,),mu=(p,),h=(p,3,3),beta=(p,3)))):
   for n,shape in shapes.items():
    saved=pair(rp+'same_cached_normal_'+n,shape);assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(saved,family[n]))
  f=keep(label+'_row%d_fixed_lapse'%row,data[rp+'same_fixed_test_lapse'].copy());b=keep(label+'_row%d_fixed_shift'%row,data[rp+'same_fixed_test_shift'].copy());ef=np.ones(p) if row==0 else np.zeros(p);eb=np.zeros((p,3))
  if row:eb[:,row-1]=1.
  assert f.dtype==b.dtype==np.float64 and np.array_equal(f,ef) and np.array_equal(b,eb)
  for n in ('X','pressure','PX'):
   saved=pair(rp+'same_cached_EOS_'+n,(p,));assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(saved,values[n]))
  for n,shape in (('EOS_clock_square_contact',(p,)),('measure_test_trace_contact',(p,)),('unit_constraint',(p,)),('projector_construction_contact',(p,4,4))):pair(rp+'inherited_'+n,shape)
  for n in ('r','density'):assert all(np.array_equal(a.view(np.uint64),b.view(np.uint64)) for a,b in zip(test[n],values[n]))
  coeff={n:pair(rp+'NEW_fixed_contact_coefficient_'+n,(p,4)) for n in ('It_phi','It_r','hi_rt')}
  rows.append(dict(test=test,s=normal_s,c={n:normal_c[n] for n in ('N','mu','h','beta')},f=f,b=b,contact_coefficients=coeff,cached_value_provenance=dict(record=thin(ref),row=row,original_row=md['normal_rows'][row]),phase_normal_value_recomputed=False,physical_adoption=False))
 return dict(eos=eos,normal_rows=rows,source=thin(ref),literal_phase_mass_and_gauge_rate_independence_verified=True,EOS_primal_or_fixed_coefficient_or_normal_VALUE_replayed=False,physical_adoption=False)

def initialize_unit_reader():
 initialize_rate_helpers()
 file='cross_u_candidate_right_only_mechanical_response_v002.py';exec(compile(selected_definitions(file,{'closed_packet','selected_record'}),file,'exec'),globals())
 file='author_fragment_candidate_weak_mechanical_positive_v001.py';names={'mp_out','mp_add','mp_mul'};exec(compile(selected_definitions(file,names),file,'exec'),globals())


def phase_unit_admission():
 global COUPLED_INVARIANT_CLOSURES
 r,rc=closed_packet(CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF)
 assert r['owner']['pid']==28110 and r['owner']['source_sha256']=='5c595057f4311bce62f4b76345d38b578cc6295492b488a954028a04179a5c38'
 c=r['case'];assert c['EOS_primal_log_current_or_normal_value_replayed'] is c['old_temporal_or_compact_chi_direction_reused'] is c['physical_adoption'] is False
 assert c['stage_current_does_not_replace_literal_M'] is c['all_original_targets_and_epsilon_held'] is True
 assert len(c['cached_columns'])==4 and c['controls']==94 and c['roles']==57 and len(r['controls'])==94 and len(r['checkpoints'])==57
 inp=selected_record(c['input'],r,rc);md=inp['metadata'];assert md['kind']=='closed_updated_phase_temporal_component_sources' and md['physical_adoption'] is False
 refs=dict(finite_terminal=md['finite_terminal'],basis=bind_record(md['basis']),prior=bind_record(md['prior_literal_weak_charge']),columns=[dict(new=bind_record(q['finite'])) for q in md['columns']])
 mass=admit_current_mass(refs);assert md['mass_preparation']==thin(mass['preparation']) and md['mass_terminal']==json.loads(json.dumps(mass['terminal'])) and c['mass_terminal']==md['mass_terminal']
 cols=[selected_record(q,r,rc) for q in c['cached_columns']]
 for iq,q in enumerate(cols):
  cm=q['metadata'];assert cm['column']==iq and cm['input']==thin(inp) and cm['state']==md['columns'][iq]['state'] and cm['finite_phase_column']==md['columns'][iq]['finite'] and cm['normal_rows']==md['columns'][iq]['joined_rows']
  for n in coupled_saved_phase_names(iq):assert n in cm['schema'] and cm['schema'][n]['dtype']=='float64' and cm['schema'][n]['finite'] is True,n
 COUPLED_INVARIANT_CLOSURES={'phase_rate_cache':(CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF)}
 return dict(result=r,receipt=rc,input=inp,columns=cols,basis=refs['basis'],mass=mass,phase_terminal=md['finite_terminal'],normal_terminal=md['join_terminal'])


def phase_unit_stage(role,payload,metadata):
 clear_completed();capture_families('completed_'+role+'_',payload)
 return seal_completed(role,metadata)


def phase_unit_enclosure(pair,raw,keep,label):
 coupled_pair(label+'_signed_pair',pair,pair[0].shape);raw=keep(label+'_independent_source_unsigned',np.asarray(raw).copy())
 assert raw.dtype==np.float64 and raw.shape==pair[0].shape and np.all(np.isfinite(raw)) and np.all(raw>=0)
 gamma=(2048.*2.**-53)/(1.-2048.*2.**-53);keep(label+'_gamma2048',np.asarray(gamma))
 padded=mp_add(raw,mp_mul(raw,gamma,keep,label+'_padding'),keep,label+'_padded_source_unsigned')
 upper=mp_add(abs(pair[0]),abs(pair[1]),keep,label+'_outward_both_word_upper')
 keep(label+'_upper_minus_padded_readout',(upper-padded).copy());assert np.all(upper<=padded),'Actual point-unit words exceed predeclared padded source envelope; no floor or replacement'
 return padded


def phase_unit_packet(refs):
 basis=read_closed(refs['basis'],('R','dv','hats'));md=refs['mass']['preparation']['metadata'];constants=dict(md['constants'])
 names=tuple('updated_phase_mass_candidate_H_'+w for w in ('hi','lo'))+('updated_phase_mass_uncancelled_H_envelope',)+tuple('updated_phase_mass_NEW_basis_'+n for n in ('R','dv','hats'))
 mass=read_closed(refs['mass']['preparation'],names);H=tuple(mass['updated_phase_mass_candidate_H_'+w] for w in ('hi','lo'));eH=mass['updated_phase_mass_uncancelled_H_envelope']
 for n in basis:assert np.array_equal(basis[n],mass['updated_phase_mass_NEW_basis_'+n]);keep('copied_original_basis_'+n,basis[n])
 assert H[0].shape==H[1].shape==eH.shape==(15136,) and np.all(H[0]-abs(H[1])>0) and np.all(eH>=0)
 inp=phase_unit_stage('INPUT',dict(basis=basis,H=H,eH=eH),dict(cache_terminal=(CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF),cache_input=thin(refs['input']),mass_terminal=refs['mass']['terminal'],mass_preparation=thin(refs['mass']['preparation']),constants=constants,basis=thin(refs['basis']),point_units_not_nodal_directions=True,planned_role_inventory=EXPECTED_ROLES,expected_control_names=EXPECTED_CONTROLS,physical_adoption=False))
 columns=[];phase_tests=(1.,0.,0.,0.);shift_tests=((0.,0.,0.),(1.,0.,0.),(0.,1.,0.),(0.,0.,1.));index=np.asarray(FIXED_POINT_INDEX,dtype=np.int64)
 for iq,ref in enumerate(refs['columns']):
  CONTEXT.update(column=iq,stage='hydrate_saved_phase_operands');data=read_closed(ref,coupled_saved_phase_names(iq));rp='cache_column%d_row0_'%iq
  pair=lambda n:tuple(data[rp+'same_cached_normal_'+n+'_'+w].copy() for w in ('hi','lo'))
  ns={n:pair(n) for n in ('g','hi','U','uc','P','phi')};nc={n:pair(n) for n in ('N','mu','h','beta')};ep='column%d_cached_EOS_same_candidate_'%iq
  for n in ('ih','u'):nc[n]=tuple(data[ep+n+'_'+w].copy() for w in ('hi','lo'))
  cm=ref['metadata'];expect=dict(naturally_closed=True,all_selected_seals_verified=True,source_rate_independent_operands_verified=True,state=cm['state'],finite_phase_column=cm['finite_phase_column'],normal_rows=cm['normal_rows'],input=cm['input'],closure=COUPLED_INVARIANT_CLOSURES['phase_rate_cache'],phase_provenance=dict(closed_cache=thin(ref),current_finite_phase=cm['finite_phase_column'],fixed_geometry_and_phase_only=True))
  column=coupled_hydrate_phase_rate_column(ref,data,constants,ns,nc,P.a_slice(H,slice(iq*3784,(iq+1)*3784)),expect,keep,'column%d_saved_phase'%iq)
  copied=phase_unit_stage('CACHE_COPY',column,dict(column=iq,input=thin(inp),source=thin(ref),normal_VALUE_or_fixed_coefficient_or_EOS_recomputed=False,unit_direction_not_evaluated=True,physical_adoption=False))
  one=P.a_dd(np.ones(3784));eos=column['eos'];literal=eos['values']['H'];normal_cache=[q['test'] for q in column['normal_rows']]
  refs4=[phase_rate_fraction_reference(eos,one,normal_cache,phase_tests,shift_tests,point=int(k)) for k in index]
  unsigned=phase_rate_fraction_reference(eos,one,normal_cache,phase_tests,shift_tests,bounds=True,keep=keep,label='column%d_NEW_unit_unsigned'%iq)
  CONTEXT.update(column=iq,stage='NEW_point_unit_temporal_EOS');delta=cached_updated_phase_eos_temporal_rate(eos,one,literal,keep,'column%d_NEW_point_unit_EOS'%iq)
  for n in ('p','H'):rational_control('column%d_NEW_unit_fraction_%s'%(iq,n),tuple(w[index] for w in delta['delta'][n]),[q['eos'][n][1] for q in refs4])
  er=phase_unit_stage('UNIT_EOS',dict(direction=one,literal_unit_H=literal,result=delta,independent_unsigned={n:np.asarray(v[2]).copy() for n,v in unsigned['eos'].items() if not isinstance(v,list)}),dict(column=iq,input=thin(inp),cache=thin(copied),point_unit_phi0=True,nodal113_action_not_called=True,stage_minus_literal_H_comparison_retained=True,physical_adoption=False))
  coeff=P.a_dd(np.zeros((3784,4)));raw_bound=np.zeros((3784,4));bound=np.zeros((3784,4));rows=[]
  for row,prepared in enumerate(column['normal_rows']):
   CONTEXT.update(column=iq,row=row,jet=0,stage='NEW_point_unit_phase_normal');normal=cached_updated_phase_normal_temporal_rate(prepared,delta,keep,'column%d_row%d_NEW_point_unit'%(iq,row));value=normal['delta']['hamiltonian'];raw=np.asarray(unsigned['normals'][row]['hamiltonian'][2]).copy();padded=phase_unit_enclosure(value,raw,keep,'column%d_row%d_NEW_unit_enclosure'%(iq,row))
   rational_control('column%d_NEW_unit_fraction_normal%d'%(iq,row),tuple(w[index] for w in value),[q['normals'][row]['hamiltonian'][1] for q in refs4])
   for w in (0,1):coeff[w][:,row]=value[w]
   raw_bound[:,row]=raw;bound[:,row]=padded;coupled_pair('column%d_completed_normal_unit_prefix'%iq,coeff,(3784,4));keep('column%d_completed_unsigned_unit_prefix'%iq,bound.copy())
   rr=phase_unit_stage('UNIT_NORMAL_ROW',dict(result=normal,raw_unsigned=raw,padded_unsigned=padded,completed_normal_coefficients=coeff,completed_unsigned=bound),dict(column=iq,row=row,jet=0,input=thin(inp),cache=thin(copied),EOS=thin(er),original_normal_VALUE_row=ref['metadata']['normal_rows'][row],relative_phase_count=1,ordinary_direct_phase_rate_count=0,time_primary_and_CMC_direct_phase_rate_zero=True,physical_adoption=False));rows.append(thin(rr))
  cr=phase_unit_stage('UNIT_COLUMN',dict(normal_value_coefficient=coeff,raw_source_unsigned=raw_bound,represented_proxy_unsigned=bound,literal_unit_H=literal,stage_minus_literal_H=delta['cached_stage_minus_literal_mass_point']),dict(column=iq,input=thin(inp),cache=thin(copied),source_cache=thin(ref),EOS=thin(er),normal_rows=rows,point_unit_phi0=True,normal_coordinate_order=['value','R','Z','t'],only_value_coefficient_nonzero=True,time_primary_and_CMC_phase_rate_exact_zero=True,original157_whole_correction_required=True,arbitrary_DD_association_qualified=False,physical_adoption=False));columns.append(thin(cr));clear_completed()
 assert [q['name'] for q in CHECKS]==EXPECTED_CONTROLS and len(set(EXPECTED_CONTROLS))==24 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 prep=phase_unit_stage('PREPARATION',dict(columns=np.asarray(len(columns),dtype=np.int64)),dict(input=thin(inp),columns=columns,basis=thin(refs['basis']),cache_terminal=(CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF),mass_terminal=refs['mass']['terminal'],phase_and_normal_terminals=(refs['phase_terminal'],refs['normal_terminal']),counts=dict(columns=4,normal_ports=16,new_Fraction_comparisons=24),original157_whole_correction_unsigned_and_fresh_finite_normal_CMC_authority=True,NEW139_transfer_requires_exact_same_geometry_phi_H_and_source_transactions=True,conditional_represented_proxy_enclosure_only=True,uniform_DD_or_inverse_or_physical_adoption=False))
 assert [q['metadata']['role'] for q in RECORDS]==EXPECTED_ROLES and len(RECORDS)==34
 return dict(status='SAVED_CURRENT_PHASE_RATE_UNIT_COEFFICIENTS_PREPARED_UNQUALIFIED',input=thin(inp),columns=columns,preparation=thin(prep),cache_terminal=(CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF),mass_terminal=refs['mass']['terminal'],roles=len(RECORDS),controls=len(CHECKS),unit_ports=16,original157_whole_correction_and_fresh_finite_authority=True,old_VALUE_preparation_action_or_control_replayed=False,physical_adoption=False)


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root FULL review and release required'
 assert all(x is not None for ref in (CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF) for x in ref),'Natural cached phase closure required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(*INITIALIZER_SOURCE);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for file,h in PINS.items():bind(file,h)
  initialize_unit_reader();refs=phase_unit_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,cache_terminal=(CACHE_SOURCE,CACHE_RESULT,CACHE_RECEIPT,CACHE_PROOF),planned_roles=EXPECTED_ROLES,planned_controls=EXPECTED_CONTROLS,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=phase_unit_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_NEW_phase_unit_operands_and_completed_prefixes',context=dict(CONTEXT),Fraction_metadata=REFERENCE_METADATA),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
