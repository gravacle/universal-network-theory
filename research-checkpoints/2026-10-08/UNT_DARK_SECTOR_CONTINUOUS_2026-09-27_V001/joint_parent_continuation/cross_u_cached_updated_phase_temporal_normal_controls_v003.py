"""HELD actual updated-phase temporal current/H and four-normal action controls.
Two NEW scalar3870 directions consume CLOSED13764/15744 caches and current19724 H.
Only113 mass actions,157 direction stages and original weak transposes are new.
No EOS value/log/root/current/normal/mechanical/ordinary/CMC producer is replayed.
Each completed cache, EOS/normal row and direction readout is sealed separately.
Root alone releases and executes after full source/protocol and metadata review.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CACHED_UPDATED_PHASE_TEMPORAL_NORMAL_CONTROLS_V003'
DRIVER_PROTOCOL='CROSS_U_CACHED_UPDATED_PHASE_TEMPORAL_NORMAL_CONTROLS_V001.md'
PROTOCOL_SHA='fee8e3922c8473a7baf5de7cb017d584d50feb7cafae3aaaf0440fee778328ae'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
SUPPORT_SOURCE=('cross_u_cached_updated_phase_compact_chi_contact_v003.py','4f6f6c2db02bfe97e2c4132e16fc592050c3a3cd23876eaf96e4589b871dc2ab')
SUPPORT_NAMES={'selected_definitions','load_io','read_closed','clear_completed','seal_completed','initialize_helpers','cached_chi_admission','hydrate_chi_column','reference_items','rational_control'}
COMPONENT_PROTOCOL=('CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V001.md','14f9c9d3a8970bed81bdd771b9ba0c5030c280439a84c9506cf825bc1b567aa3')
RATE_COMPONENT_PROTOCOL=('CACHED_UPDATED_PHASE_TEMPORAL_NORMAL_V002.md','6c0ace7fede2f6dc6fe26b526fae3135bdc2df6669d7013f8e3c4cab1139d9d6')
MASS_SOURCE=('cross_u_updated_finite_phase_mass_preparation_v002.py','76a929447f2a0ed968825872e57ce2cf309fb49eeff13a1d8916ae3becb374cc')
MASS_RESULT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RESULT.json','9febbd8cd23e96efbec23ffb6d24323d8b2ac99aaef5e73ce903bf49660b47c5','UPDATED_FINITE_PHASE_LITERAL_MASS_CACHE_PREPARED_UNQUALIFIED')
MASS_RECEIPT=('CROSS_U_UPDATED_FINITE_PHASE_MASS_PREPARATION_V002_RECEIPT.json','69e25ed8a9c413f7c153a69e976a9f36cb3636fd67a8193eb3138514a2be2872','CLOSED')
MASS_PROOF=('ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_V001.json','2b6d27847c8b70d592209d117dbc18f7ee0e41f8ed454d684734ec03d92ed662','ROOT_NATURAL_CLOSED_UPDATED_FINITE_PHASE_MASS_SUCCESS_SEALS_VERIFIED')
DIRECTION_NODES=(((43,22,1.,2.**-60),),((43,22,-.5,-2.**-61),(86,44,.25,2.**-62),(43,0,.125,-2.**-63)))
REFERENCE_METADATA=[]
np=P=N=K=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_fixed_geometry_phase_normal_join_v001.py': '7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_candidate_finite_phase_state_update_v001.py': 'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'author_fragment_cached_phase_chi_fraction_reference_v001.py': '414ed54d382a1e644a7a8ba9847881d1b53fa2e76d480de7b4c223cf00940b43', 'author_fragment_phase_literal_charge_hessian_v002.py': '293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143', 'author_fragment_candidate_literal_phase_mass_v001.py': '0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38', 'author_fragment_cached_updated_phase_temporal_normal_v002.py': 'b60d4bc3823439910843f10661dc960035bdad9af78ff3326cd4bc702474bf44', 'author_fragment_cached_phase_rate_fraction_reference_v001.py': '0a9dcc2f6caef474dc43766b44a5e43290734098c35c5b90669230f2e29a9af7'}
JOIN_SOURCE=('cross_u_fixed_geometry_phase_normal_canonical_value_join_v002.py', '28e8cb501975c4fd20660ce022a54c0ab9c677dc00108399e76fe023f870755b')
JOIN_RESULT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RESULT.json', 'd382c372ac74e581beee2a491ae4a143cf24a6c73dd87fd0565044a6041fd9ed', 'FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED')
JOIN_RECEIPT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RECEIPT.json', '2f331b3a45b1e5dfe25114ab4d3f0d90528029b9d3d060c2809c1d691f7d31b6', 'CLOSED')
JOIN_PROOF=('ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_V001.json', '3bc8ea72625fbcda04440f9bc80dfde01b1aeb30804a555b84771c2b899651ae', 'ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_VERIFIED')
POINT_CELLS=((42, 21), (42, 22), (43, 21), (43, 22))
SHAPES={'g': (4, 4), 'hi': (4, 4), 'U': (4,), 'uc': (4,), 'P': (4, 4), 'phi': (4,), 'N': (), 'mu': (), 'h': (3, 3), 'beta': (3,), 'ih': (3, 3), 'u': (3,)}


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


def temporal_control_names(case):
 stem='direction%d_four_point_'%case;out=[stem+'cached_EOS_'+n for n in RATE_EOS_NAMES]
 out += [stem+n+'_chain_'+k for n in RATE_CHAIN_NAMES for k in ('actual','expected','gap')]
 out += [stem+'row%d_'%row+n for row in range(4) for n in RATE_NORMAL_NAMES]
 return out+['direction%d_NEW_phase_rate_normal_functional_polynomial_transpose'%case,'direction%d_NEW_phase_rate_staged_current_functional'%case]


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


def scalar_temporal_functional(point,weak,epoint,basis,test,sv,label):
 left=test!=0;selected=(sv[0]!=0)|(sv[1]!=0);nodal=P.a_dd(np.zeros((87,45)));direct=P.a_dd(np.zeros(15136))
 fy_keep(label+'_selected_weak',(weak[0][left],weak[1][left]),keep);fy_keep(label+'_selected_point',(point[0][selected],point[1][selected]),keep);fy_keep(label+'_selected_polynomial',(sv[0][selected],sv[1][selected]),keep)
 a=P.a_mul64(test[left],(weak[0][left],weak[1][left]));b=P.a_mul((sv[0][selected],sv[1][selected]),(point[0][selected],point[1][selected]))
 for w in (0,1):nodal[w][left]=a[w];direct[w][selected]=b[w]
 nv=fy_sum(fy_sum(nodal,1),0);dv=fy_sum(P.a_mul64((basis['dv']/basis['R']).reshape(15136),direct),0);gap=P.a_sub(nv,dv)
 bound=2*np.sum((basis['dv']/basis['R']).reshape(15136)*(abs(sv[0])+abs(sv[1]))*epoint)
 for n,q in (('nodal',nv),('direct',dv),('gap',gap)):fy_keep(label+'_'+n,q,keep)
 keep(label+'_uncancelled_positive_bound',np.asarray(bound));P.check(label,(gap[0]+gap[1]).copy(),np.asarray(0.),np.asarray(bound));return dict(nodal=nv,direct=dv,gap=gap)


def phase_temporal_packet(refs,mass):
 global REFS
 REFS=refs;basis=read_closed(refs['basis'],('R','dv','hats','cell_i','cell_j'));assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert np.all(basis['R']>0) and np.all(basis['dv']>0) and np.array_equal(basis['cell_i'],np.repeat(np.arange(86),44)) and np.array_equal(basis['cell_j'],np.tile(np.arange(44),86))
 for n,a in basis.items():keep('closed_original_basis_'+n,a.copy())
 fields=read_closed(mass['preparation'],tuple('updated_phase_mass_candidate_H_'+w for w in ('hi','lo'))+('updated_phase_mass_uncancelled_H_envelope',)+tuple('updated_phase_mass_NEW_basis_'+n for n in ('R','dv','hats')))
 H=cached_phase_pair(fields,'updated_phase_mass_candidate_H',(15136,),keep,'copied_current19724_H');eH=keep('copied_current19724_eH',fields['updated_phase_mass_uncancelled_H_envelope'].copy());assert np.all(eH>=0)
 for n in ('R','dv','hats'):assert np.array_equal(basis[n],fields['updated_phase_mass_NEW_basis_'+n])
 cache=dict(H=H,eH=eH,basis={n:basis[n] for n in ('R','dv','hats')},fresh_literal_candidate_H_used=True,reference_H_reused=False,phase_space_dofs=3870,phase_outer_top_nodes_free=True,physical_adoption=False)
 assert np.count_nonzero(P.scalar_mask())==3870 and np.all(H[0]-abs(H[1])>0)
 header=seal_completed('TEMPORAL_INPUT',dict(kind='closed_updated_phase_temporal_component_sources',normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],mass_terminal=mass['terminal'],mass_preparation=thin(mass['preparation']),original_input=thin(refs['input']),basis=thin(refs['basis']),prior_literal_weak_charge=thin(refs['prior']),columns=[dict(state=thin(q['state']),old=thin(q['old']),finite=thin(q['new']),joined=thin(q['joined']),joined_rows=[thin(v) for v in q['joined_rows']]) for q in refs['columns']],four_point_control_cells=[list(q) for q in POINT_CELLS],directions=DIRECTION_NODES,expected_control_names=[n for case in range(len(DIRECTION_NODES)) for n in temporal_control_names(case)],EOS_primal_or_log_replayed=False,physical_adoption=False));clear_completed()
 prepared_columns=[];cache_refs=[]
 f=(1.,0.,0.,0.);b=((0.,0.,0.),(1.,0.,0.),(0.,1.,0.),(0.,0.,1.))
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(column=iq,stage='hydrate_closed_updated_cache');prepared,old_chi,rows,nc,index=hydrate_chi_column(source,iq);tests=[]
  assert all(np.array_equal(a,q) for a,q in zip(prepared['values']['H'],P.a_slice(H,slice(iq*3784,(iq+1)*3784))))
  for row,(rp,data) in enumerate(rows):
   test=prepare_cached_updated_phase_normal_rate(data,rp,prepared['s'],prepared['c'],prepared,np.full(3784,f[row]),np.tile(np.asarray(b[row]),(3784,1)),dict(closed_new_phase_row=thin(source['joined_rows'][row]),updated_phase_column=thin(source['new'])),keep,'cache_column%d_row%d'%(iq,row));tests.append(test)
  rec=seal_completed('TEMPORAL_CACHE_COLUMN',dict(kind='copied_updated_EOS_normal_primal_and_NEW_fixed_rate_derivative_coefficients',column=iq,input=thin(header),state=thin(source['state']),finite_phase_column=thin(source['new']),normal_rows=[thin(q) for q in source['joined_rows']],new_fixed_coefficients=['It_phi','It_r','hi_rt'],old_chi_and_temporal_step_not_used_as_rate_direction=True,physical_adoption=False));cache_refs.append(thin(rec));prepared_columns.append(dict(eos=prepared,normal_rows=tests,reference_normal=nc,point_index=index));clear_completed()
 results=[]
 for case,node_entries in enumerate(DIRECTION_NODES):
  CONTEXT.update(direction=case,stage='NEW_current19724_mass_action');nodes=P.a_dd(np.zeros((87,45)))
  for i,j,h,l in node_entries:nodes[0][i,j]=h;nodes[1][i,j]=l
  fy_keep('direction%d_NEW_independent_phase_nodes'%case,nodes,keep);assert all(np.all(a[~P.scalar_mask()]==0) for a in nodes)
  action=candidate_phase_mass_action(cache,basis,nodes,keep,'direction%d_NEW_current_phase_mass'%case)
  assert action['extra_N_or_mu_factor_inserted'] is False and action['temporal_mechanical_crossblock_zero_scope']=='fixed configuration only'
  massref=seal_completed('TEMPORAL_MASS_ACTION',dict(kind='NEW_updated13764_H_original113_mass_action',direction=case,input=thin(header),mass_preparation=thin(mass['preparation']),phase_space_dofs=3870,outer_top_free=True,original_literal_mass_authoritative=True,physical_adoption=False));clear_completed()
  point=P.a_dd(np.zeros((15136,4,3)));stage=P.a_dd(np.zeros(15136));egroups=[];ep=[];column_refs=[]
  for iq,column in enumerate(prepared_columns):
   CONTEXT.update(direction=case,column=iq,stage='NEW_cached_temporal_EOS_contact');sl=slice(iq*3784,(iq+1)*3784);prepared=column['eos'];rate=P.a_slice(action['scalar_jets']['value'],sl);literal=P.a_slice(action['point'],sl);index=column['point_index']
   references=[reference_items(phase_rate_fraction_reference(prepared,rate,column['reference_normal'],f,b,point=int(i))) for i in index] if iq==0 else None
   unsigned=phase_rate_fraction_reference(prepared,rate,column['reference_normal'],f,b,bounds=True,keep=keep,label='direction%d_column%d_NEW_unsigned_rate'%(case,iq));envelope={n:np.asarray(q[2]).copy() for n,q in unsigned['eos'].items() if not isinstance(q,list)}
   eos=cached_updated_phase_eos_temporal_rate(prepared,rate,literal,keep,'direction%d_column%d_NEW_cached_rate_EOS'%(case,iq));assert tuple(eos['delta'])==RATE_EOS_NAMES and tuple(eos['chain_gaps'])==RATE_CHAIN_NAMES
   for n,q in eos['delta'].items():fy_keep('direction%d_column%d_NEW_rate_delta_'%(case,iq)+n,q,keep)
   for n,a in envelope.items():keep('direction%d_column%d_NEW_rate_positive_'%(case,iq)+n,a)
   if iq==0:
    for n,q in eos['delta'].items():rational_control('direction%d_four_point_cached_EOS_'%case+n,(q[0][index],q[1][index]),[r[n] for r in references])
    for n,gap in eos['chain_gaps'].items():
     for kind,q in (('actual',eos['delta'][{'P':'pressure','PX':'PX','PXX':'PXX'}[n]]),('expected',P.a_mul(prepared['values'][{'P':'PX','PX':'PXX','PXX':'PXXX'}[n]],eos['delta']['X'])),('gap',gap)):rational_control('direction%d_four_point_'%case+n+'_chain_'+kind,(q[0][index],q[1][index]),[r[n+'_chain_'+kind] for r in references])
   er=seal_completed('TEMPORAL_EOS_CONTACT',dict(kind='NEW_cached_updated_phase_temporal_current_H_contact',direction=case,column=iq,input=thin(header),cache=cache_refs[iq],mass_action=thin(massref),old_temporal_step_or_chi_direction_used=False,stage_minus_analytic_chain_and_literal_M_gaps_retained=True,four_point_Fraction_targets=[q for q in REFERENCE_METADATA if q['name'].startswith('direction%d_four_point_'%case)] if iq==0 else [],physical_adoption=False));clear_completed();rowrefs=[];bound=np.zeros((3784,4,3))
   for row,test in enumerate(column['normal_rows']):
    CONTEXT.update(direction=case,column=iq,row=row,jet=0,stage='NEW_cached_phase_rate_normal_contact');normal=cached_updated_phase_normal_temporal_rate(test,eos,keep,'direction%d_column%d_row%d_NEW_rate_normal'%(case,iq,row));assert tuple(normal['delta'])==RATE_NORMAL_NAMES
    if iq==0:
     for n,q in normal['delta'].items():rational_control('direction%d_four_point_row%d_'%(case,row)+n,(q[0][index],q[1][index]),[r['row%d_'%row+n] for r in references])
    for w in (0,1):point[w][sl,row,0]=normal['delta']['hamiltonian'][w]
    en=np.asarray(unsigned['normals'][row]['hamiltonian'][2]);assert en.shape==(3784,) and np.all(en>=0) and np.all(np.isfinite(en));bound[:,row,0]=en
    keep('direction%d_column%d_row%d_NEW_rate_normal_positive'%(case,iq,row),en.copy());fy_keep('direction%d_completed_normal_point_inventory'%case,point,keep)
    rr=seal_completed('TEMPORAL_NORMAL_ROW',dict(kind='NEW_updated_phase_independent_temporal_four_normal_value_contact',direction=case,column=iq,row=row,jet=0,input=thin(header),eos_contact=thin(er),closed_value_row=thin(refs['columns'][iq]['joined_rows'][row]),relative_phase_count=1,mechanical_ordinary_CMC_phase_temporal_crossblock_zero_at_fixed_configuration=True,phase_R_Z_t_test_coefficients_zero_by_action=True,four_point_Fraction_targets=[q for q in REFERENCE_METADATA if q['name'].startswith('direction%d_four_point_row%d_'%(case,row))] if iq==0 else [],physical_adoption=False));rowrefs.append(thin(rr));clear_completed()
   for w in (0,1):stage[w][sl]=eos['delta']['p'][w]
   for n,q in (('staged_current',eos['delta']['p']),('literal_mass_point',literal),('staged_minus_literal_mass',eos['cached_stage_minus_literal_mass_point'])):fy_keep('direction%d_column%d_completed_'%(case,iq)+n,q,keep)
   fy_keep('direction%d_column%d_completed_normal_value'%(case,iq),P.a_slice(point,(sl,slice(None),0)),keep);keep('direction%d_column%d_positive_normal'%(case,iq),bound.copy());keep('direction%d_column%d_positive_current'%(case,iq),envelope['p'].copy())
   rec=seal_completed('TEMPORAL_COLUMN',dict(kind='NEW_fixed_geometry_updated_phase_current_and_four_normal_rate_column',direction=case,column=iq,input=thin(header),cache=cache_refs[iq],eos_contact=thin(er),normal_contacts=rowrefs,original_literal_mass_action_authoritative=True,staged_current_is_comparison_only=True,normal_coordinate_order=['value','R','Z'],physical_adoption=False));column_refs.append(thin(rec));egroups.append(bound);ep.append(envelope['p']);clear_completed()
  CONTEXT.update(direction=case,stage='NEW_rate_weak_transpose_assembly');weak=N.paired_scatter_normal(point,basis,'direction%d_NEW_phase_rate_normal'%case);stageweak=P.dd_scalar_scatter(stage,basis,keep,'direction%d_NEW_phase_rate_staged_current'%case)
  for n,q in (('normal_point',point),('normal_weak',weak),('staged_current_point',stage),('staged_current_weak',stageweak),('literal_mass_point',action['point']),('literal_mass_weak',action['weak']),('staged_minus_literal_mass_point',P.a_sub(stage,action['point'])),('staged_minus_literal_mass_weak',P.a_sub(stageweak,action['weak'])),('time_primary_action_exact_zero',P.a_dd(np.zeros((15136,4)))),('initial_CMC_phase_rate_exact_zero',P.a_dd(np.zeros((87,45))))):fy_keep('direction%d_NEW_'%case+n,q,keep)
  assert all(np.all(a[:,:,1:]==0) for a in point) and all(np.all(a[~N.normal_test_mask()]==0) for a in weak)
  enormal=np.concatenate(egroups);epoint=np.concatenate(ep);normaltest=np.zeros((4,87,45));normaltest[:,43,22]=(1.,2.,3.,4.);scalartest=np.zeros((87,45));scalartest[43,22]=1.;scalartest[86,44]=.5;scalartest[43,0]=-.25
  tv,sv=finite_candidate_test_polynomials(normaltest,scalartest,basis,keep,'direction%d_NEW_independent_transpose_polynomials'%case)
  normalcheck=phase_join_functional(point,weak,P.a_dd(np.zeros((4,87,45))),basis,normaltest,tv,enormal,keep,P.check,'direction%d_NEW_phase_rate_normal_functional'%case)
  scalarcheck=scalar_temporal_functional(stage,stageweak,epoint,basis,scalartest,sv,'direction%d_NEW_phase_rate_staged_current_functional'%case)
  keep('direction%d_NEW_positive_normal'%case,enormal);keep('direction%d_NEW_positive_staged_current'%case,epoint)
  rr=seal_completed('TEMPORAL_READOUT',dict(kind='NEW_updated_phase_temporal_four_normal_and_literal_current_implementation_readout',direction=case,input=thin(header),columns=column_refs,mass_action=thin(massref),normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],mass_terminal=mass['terminal'],original_targets_and_epsilon_unchanged=True,literal_M_authoritative_and_stage_gap_descriptive=True,stationarity_epsilon_feedback_required=True,mechanical_canonical_and_CMC_phase_rate_contact_exact_zero_fixed_configuration_only=True,new_finite_solution_or_physical_admission=False,physical_adoption=False));results.append(thin(rr));clear_completed()
 expected_roles=['TEMPORAL_INPUT']+['TEMPORAL_CACHE_COLUMN']*4+(['TEMPORAL_MASS_ACTION']+(['TEMPORAL_EOS_CONTACT']+['TEMPORAL_NORMAL_ROW']*4+['TEMPORAL_COLUMN'])*4+['TEMPORAL_READOUT'])*len(DIRECTION_NODES)
 expected_names=[n for case in range(len(DIRECTION_NODES)) for n in temporal_control_names(case)]
 assert [q['metadata']['role'] for q in RECORDS]==expected_roles and [q['name'] for q in CHECKS]==expected_names and len(set(expected_names))==len(expected_names)
 assert all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 return dict(status='CACHED_UPDATED_PHASE_TEMPORAL_FOUR_NORMAL_CONTACTS_MEASURED',input=thin(header),cached_columns=cache_refs,readouts=results,normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],mass_terminal=mass['terminal'],directions=DIRECTION_NODES,controls=len(expected_names),roles=len(expected_roles),expected_control_names=expected_names,control_inventory=dict(EOS=len(RATE_EOS_NAMES),chain=3*len(RATE_CHAIN_NAMES),normal=4*len(RATE_NORMAL_NAMES),weak_per_direction=2,directions=len(DIRECTION_NODES)),EOS_primal_log_current_or_normal_value_replayed=False,old_temporal_or_compact_chi_direction_reused=False,stage_current_does_not_replace_literal_M=True,all_original_targets_and_epsilon_held=True,global_convenience_rate_body_not_called=True,full_configuration_Jacobian_finite_state_or_physical_admission=False,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root reviewed guard/protocol release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_support();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(*SUPPORT_SOURCE);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL);bind(*RATE_COMPONENT_PROTOCOL)
  for name,h in PINS.items():bind(name,h)
  initialize_rate_helpers();refs=cached_chi_admission();mass=admit_current_mass(refs);names=[n for case in range(len(DIRECTION_NODES)) for n in temporal_control_names(case)]
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],mass_terminal=mass['terminal'],directions=DIRECTION_NODES,expected_control_names=names,controls=len(names),qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=phase_temporal_packet(refs,mass)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_cached_updated_phase_temporal_contact',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
