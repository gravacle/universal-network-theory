"""HELD NEW literal Rv/Tv point coefficients and two saved-direction contacts.
Only CLOSED words hydrate. Root alone binds/releases/executes; no old physics
body runs. The source-associated primitive306 polynomial remains an approximate
coefficient consumer; original87/147 direction authority is not transferred.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_LITERAL_RATE_NORMAL_COEFFICIENT_PREPARATION_V001'
DRIVER_PROTOCOL='CANDIDATE_LITERAL_RATE_NORMAL_COEFFICIENT_PREPARATION_V001.md'
PROTOCOL_SHA='0c5e0b2a2dfc7091f82899bafa30722a26b5b1f2d7cfad76b11253dcf1122d0d'
RATE_DEFINITION_PARENT=('cross_u_candidate_mechanical_rate_normal_controls_v002.py', '2631ad5e878e27ac45cb3cc4b514481cd5bac81d412edc7c1862b62daecad206')
LITERAL_DEFINITION_PARENT=('cross_u_candidate_literal_temporal_gradient_contacts_v002.py', '4e65631f487b3576e0eb69ee6aa8b7a66c82e00d6c5952a5f86b551df9fa2b21')
PARENT_PINS={name:dict(source=(None,None),result=(None,None,None),receipt=(None,None,None),proof=(None,None,None)) for name in ('tests','literal','temporal')}
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
SUPPORT_SOURCE=('cross_u_cached_updated_phase_compact_chi_contact_v003.py', '4f6f6c2db02bfe97e2c4132e16fc592050c3a3cd23876eaf96e4589b871dc2ab')
SUPPORT_NAMES={'read_closed', 'initialize_helpers', 'cached_chi_admission', 'selected_definitions', 'seal_completed', 'load_io', 'clear_completed'}
JOIN_SOURCE=('cross_u_fixed_geometry_phase_normal_canonical_value_join_v002.py', '28e8cb501975c4fd20660ce022a54c0ab9c677dc00108399e76fe023f870755b')
JOIN_RESULT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RESULT.json', 'd382c372ac74e581beee2a491ae4a143cf24a6c73dd87fd0565044a6041fd9ed', 'FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED')
JOIN_RECEIPT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RECEIPT.json', '2f331b3a45b1e5dfe25114ab4d3f0d90528029b9d3d060c2809c1d691f7d31b6', 'CLOSED')
JOIN_PROOF=('ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_V001.json', '3bc8ea72625fbcda04440f9bc80dfde01b1aeb30804a555b84771c2b899651ae', 'ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_VERIFIED')
POINT_CELLS=((42, 21), (42, 22), (43, 21), (43, 22))
SHAPES={'g': (4, 4), 'hi': (4, 4), 'U': (4,), 'uc': (4,), 'P': (4, 4), 'phi': (4,), 'N': (), 'mu': (), 'h': (3, 3), 'beta': (3,), 'ih': (3, 3), 'u': (3,)}
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'cross_u_paired_current_normal_constraints_v002.py': 'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_finite_york_spacetime_first_jets_v001.py': 'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d', 'author_fragment_candidate_phase_normal_stress_v001.py': 'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd', 'author_fragment_finite_candidate_native_EH_normal_v003.py': '5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499', 'author_fragment_fixed_geometry_phase_normal_join_v001.py': '7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'cross_u_candidate_literal_phase_charge_response_v002.py': '887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6', 'author_fragment_finite_candidate_raw_action_adapter_v001.py': '9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_finite_fixed_canonical_ordinary_v001.py': '2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a', 'author_fragment_candidate_invariant_phase_eos_current_v001.py': 'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae', 'author_fragment_candidate_finite_phase_state_update_v001.py': 'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b', 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py': 'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10', 'author_fragment_cached_phase_chi_fraction_reference_v001.py': '414ed54d382a1e644a7a8ba9847881d1b53fa2e76d480de7b4c223cf00940b43', 'author_fragment_phase_literal_charge_hessian_v002.py': '293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143', 'author_fragment_candidate_literal_phase_mass_v001.py': '0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38', 'author_fragment_cached_updated_phase_temporal_normal_v002.py': 'b60d4bc3823439910843f10661dc960035bdad9af78ff3326cd4bc702474bf44', 'author_fragment_cached_phase_rate_fraction_reference_v001.py': '0a9dcc2f6caef474dc43766b44a5e43290734098c35c5b90669230f2e29a9af7', 'author_fragment_finite_candidate_configuration_contact_v001.py': '7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41', 'author_fragment_finite0_completed_state_restore_v002.py': 'af97b20f30e4b83580d8cda678ec78ccae12255ed83b0e6dc07ecd9d7c992c59', 'author_fragment_candidate_whole_configuration_york_contact_v001.py': '0fda623d1ac2e684d2a28c67e19c613b545ec9f9dd5c886f33c3ccb1c72e9ebd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_mechanical_rate_normal_contact_v001.py': 'db9e749646132e7db23184b9ec22086a9654d1537d1768c8f11298ecbd5b6aad'}
PINS.update({'author_fragment_candidate_literal_rate_normal_coefficients_v001.py': 'd9b7953600bf41de36d562f19adaa25f94674ad3234c74cad4ef0b527cf7adbb', 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py': '880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50'})
COMPONENT_PROTOCOL=('CANDIDATE_LITERAL_RATE_NORMAL_COEFFICIENTS_V001.md','dcf64485561f6d9c1ff35eeec693248e36390c4fad756459d551a76a33fd82a2')
SNAMES=('g','hi','U','z','uc','P','Z','r','z2','f','phi','omega','xi','w','R','Z_coordinate')
CNAMES=('h','ih','N','beta','u','up','gamma','dens','sqrt_h','JU','JzU','Jzz','Uh','zh','embed')
FEATURES=('F','Fup','V','V_raised','D','D_raised','Pi','PiU')
MOMENTA=('K','Ktrace','native_density','metric_native_density','metric_EH_tensor','metric_EH_density','metric_total_density')
TEST_ALIASES={'q':'metric_test','It':'inverse_metric_test','eta':'native_test','zeta':'modal_test','Pt':'projector_test','Ft':'F_test','Vt':'V_test','Dt':'D_test','Kt':'KGamma_test','lm':'measure_test'}
LITERAL_ALIASES={'F':'literal_F_adjoint','V':'literal_V_adjoint','D':'literal_D_adjoint','nu':'literal_nu_adjoint','nz':'literal_nz_adjoint','Z':'literal_acceleration_Z_partial'}
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def load_containing_io():
 assert hashlib.sha256((BASE/RATE_DEFINITION_PARENT[0]).read_bytes()).hexdigest()==RATE_DEFINITION_PARENT[1]
 tree=ast.parse((BASE/RATE_DEFINITION_PARENT[0]).read_text());names={'load_support','initialize_mechanical_rate_helpers'};defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==2
 exec(compile(ast.Module(body=defs,type_ignores=[]),RATE_DEFINITION_PARENT[0],'exec'),globals());load_support()


def initialize_containing():
 bind(*RATE_DEFINITION_PARENT);bind(*LITERAL_DEFINITION_PARENT);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL)
 for n,h in PINS.items():bind(n,h)
 initialize_mechanical_rate_helpers()
 for file,names in (('author_fragment_candidate_literal_temporal_gradient_bridge_v001.py',{'lg_six'}),('author_fragment_candidate_literal_rate_normal_coefficients_v001.py',None)):
  tree=ast.parse((BASE/file).read_text());names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if names is None else names
  exec(compile(selected_definitions(file,names),file,'exec'),globals())
 globals().update(RATE_COEFFICIENT_AUTHOR_DRAFT=False,RATE_COEFFICIENT_AUTHORING_IN_PROGRESS=False,RATE_COEFFICIENT_PARENT_PINS=PARENT_PINS)
 tree=ast.parse((BASE/LITERAL_DEFINITION_PARENT[0]).read_text());names={'closed_packet','selected_record'};defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==2
 exec(compile(ast.Module(body=defs,type_ignores=[]),LITERAL_DEFINITION_PARENT[0],'exec'),globals())
 assert SCOPE['a_prod'] is P.a_prod and SCOPE['a_mul'].__globals__ is SCOPE


def admission():
 packets={};receipts={};closed={}
 for name,pins in PARENT_PINS.items():
  r,rc=closed_packet(**pins);packets[name]=r;receipts[name]=rc;closed[name]=dict(**pins,naturally_closed=True,natural_exit_code=0,all_selected_seals_verified=True)
 assert PARENT_PINS['tests']['source']==RATE_DEFINITION_PARENT and PARENT_PINS['literal']['source']==LITERAL_DEFINITION_PARENT
 r=packets['tests'];c=r['case'];assert r['status']=='CANDIDATE_MECHANICAL_RATE_FOUR_NORMAL_CMC_COMPONENT_CONTACTS_MEASURED' and c['controls']==40 and c['roles']==153 and len(c['cached_columns'])==4 and len(c['readouts'])==2
 expected=['direction%d_NEW_mechanical_rate_column%d_%s_160_vs147'%(case,iq,name) for case in range(2) for iq in range(4) for name in ('native','metric_native','metric_EH','metric_total')]
 expected=[n for case in range(2) for n in expected[case*16:(case+1)*16]+['direction%d_NEW_mechanical_rate_'%case+n+'_polynomial_transpose' for n in ('native','metric')]+['direction%d_NEW_mechanical_rate_normal_CMC_'%case+n+'_polynomial_transpose' for n in ('normal','CMC')]]
 assert c['expected_control_names']==expected==[q['name'] for q in r['controls']] and len(set(expected))==40
 t=packets['temporal']['case'];assert len(t['caches'])==4 and t['roles']==6 and t['new_controls']==0 and t['physics_action_evaluated'] is False
 l=packets['literal']['case'];assert len(l['columns'])==4
 q=lambda group,ref:selected_record(ref,packets[group],receipts[group])
 oldinput=q('tests',c['input']);caches=[q('tests',x) for x in c['cached_columns']];readouts=[q('tests',x) for x in c['readouts']];temporal=[q('temporal',x) for x in t['caches']];literal=[q('literal',x) for x in l['columns']]
 prov=[]
 for iq,(a,b,z) in enumerate(zip(caches,temporal,literal)):
  md=b['metadata'];assert a['metadata']['column']==md['column']==z['metadata']['column']==iq and a['metadata']['temporal_cache']==thin(b) and a['metadata']['state']==md['state']==md['candidate_provenance']['state']
  assert md['configuration_held'] is True and md['physical_adoption'] is False and z['metadata']['physical_adoption'] is False
  transaction=q('literal',z['metadata']['transaction']);assert transaction['metadata']['temporal_cache']==thin(b) and transaction['metadata']['state']==a['metadata']['state'] and md['candidate_provenance']['input']==oldinput['metadata']['original_input']
  assert a['metadata']['input']==thin(oldinput);prov.append(md['candidate_provenance'])
 basisref=bind_record(oldinput['metadata']['basis']);assert thin(basisref)==thin(q('temporal',t['preparation'])['metadata']['basis'])
 for case,readout in enumerate(readouts):
  md=readout['metadata'];assert md['direction']==case and md['input']==thin(oldinput) and len(md['normal_tests'])==64 and len(md['columns'])==4
  direction=q('tests',md['direction_record']);assert direction['metadata']['direction']==case and direction['metadata']['input']==thin(oldinput) and direction['metadata']['entries']==c['directions'][case]
  for iq in range(4):
   col=q('tests',md['columns'][iq]);assert (col['metadata']['direction'],col['metadata']['column'])==(case,iq) and col['metadata']['normal_tests']==md['normal_tests'][16*iq:16*iq+16]
   for serial,ref in enumerate(col['metadata']['normal_tests']):
    row,jet=divmod(serial,4);m=q('tests',ref)['metadata'];assert (m['direction'],m['column'],m['row'],m['jet'])==(case,iq,row,jet) and m['cache']==thin(caches[iq]) and m['matching_action']==md['matching_actions'][iq]
 return dict(packets=packets,receipts=receipts,closed=closed,input=oldinput,basis=basisref,caches=caches,readouts=readouts,temporal=temporal,literal=literal,provenance=prov)


def selected_words(q,names,label):
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names)
 data=read_closed(q,names)
 for n,a in data.items():keep(label+'_'+n,a.copy())
 return data


def seal(role,metadata):
 q=seal_completed(role,dict(metadata,physical_adoption=False));clear_completed();return thin(q)


def copied_pair(data,root):return tuple(data[root+'_'+w].copy() for w in ('hi','lo'))


def slice_words(x,lo,hi):
 if isinstance(x,dict):return {k:slice_words(v,lo,hi) for k,v in x.items()}
 if isinstance(x,tuple):return tuple(slice_words(v,lo,hi) for v in x)
 if isinstance(x,list):return [slice_words(v,lo,hi) for v in x]
 if isinstance(x,np.ndarray):
  axes=[i for i,n in enumerate(x.shape) if n==3784];assert len(axes)<=1
  if axes:
   key=[slice(None)]*x.ndim;key[axes[0]]=slice(lo,hi);return x[tuple(key)].copy()
  return x.copy()
 return x


def hydrate_column(refs,iq):
 q=refs['caches'][iq];prefix='column%d_copied_STATE_'%iq;cprefix='column%d_copied13576_NEW_candidate_temporal_cache_'%iq
 roots=tuple(prefix+'completed_candidate_s_'+n for n in SNAMES)+tuple(prefix+'completed_candidate_c_'+n for n in CNAMES)+tuple(prefix+'completed_candidate_'+family+'_'+n+'_'+w for family,items in (('features',FEATURES),('momenta',MOMENTA)) for n in items for w in ('hi','lo'))
 cnames=tuple(n for n in q['metadata']['schema'] if n.startswith(cprefix));data=selected_words(q,roots+cnames,'copied_column%d'%iq)
 candidate=dict(s={n:data[prefix+'completed_candidate_s_'+n].copy() for n in SNAMES},c={n:data[prefix+'completed_candidate_c_'+n].copy() for n in CNAMES},features=dict(paired={n:copied_pair(data,prefix+'completed_candidate_features_'+n) for n in FEATURES}),momenta={n:copied_pair(data,prefix+'completed_candidate_momenta_'+n) for n in MOMENTA},candidate_provenance=refs['provenance'][iq])
 pair=lambda n:copied_pair(data,cprefix+n);ep=cprefix+'copied_positive_coefficient_'
 temporal=refs['temporal'][iq];cache=dict(s={n:data[cprefix+'raw_configuration_'+n].copy() for n in POINT_S},c={n:data[cprefix+'raw_chart_'+n].copy() for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a.copy() for n,a in data.items() if n.startswith(ep)},constants=temporal['metadata']['constants'],candidate_provenance=refs['provenance'][iq],configuration_held=True)
 state=bind_record(q['metadata']['state']);bridge_names=tuple(n for n in state['metadata']['schema'] if n.startswith(('candidate_raw_direct_minus_quotient_','candidate_raw_model_minus_new_raw_chart_first_','candidate_raw_geometry_')) or n in tuple('candidate_raw_'+root+'_'+w for root in ('KGamma_minus_KADM','Ktrace_Gamma_minus_ADM','new_first_compatibility_minus_E0') for w in ('hi','lo')))
 assert bridge_names;bridges=selected_words(state,bridge_names,'copied_original_primary_column%d'%iq);cache['source_primary_contacts']=dict(state=thin(state),words=bridges,fixed_E0=cache['fixed_E0'])
 lq=refs['literal'][iq];lp='NEW_literal_gradient_q%d_'%iq;lnames=tuple(lp+n+'_'+w for n in LITERAL_ALIASES.values() for w in ('hi','lo'))
 marks=('formal_Iu_minus_raw_up','literal_nz_adjoint_minus_registered_Pi','literal_acceleration_Z_minus_raw_Z','registered_current_PiU_minus_literal_nu_adjoint','matrix_chain_minus_factored_formal_metric_adjoint','formal_right_minus_raw_left_gradient','literal_left_minus_registered_gradient','literal_minus_registered_gradient')
 ln=tuple(n for n in lq['metadata']['schema'] if n.startswith(lp) and any(mark in n for mark in marks));assert ln
 ld=selected_words(lq,lnames+ln,'copied_literal_column%d'%iq);literal={n:copied_pair(ld,lp+alias) for n,alias in LITERAL_ALIASES.items()};literal.update(same_candidate_provenance=refs['provenance'][iq],closed_literal_ref=thin(lq),primitive_adjoints_are_literal142=True,source_association_contacts=dict(record=thin(lq),words={n:ld[n] for n in ln}))
 tests=[]
 for serial,ref in enumerate(refs['readouts'][0]['metadata']['normal_tests'][16*iq:16*iq+16]):
  row,jet=divmod(serial,4);tq=selected_record(ref,refs['packets']['tests'],refs['receipts']['tests']);tp='direction0_NEW_mechanical_rate_column%d_row%d_jet%d_NEW_native_EH_rate_'%(iq,row,jet)
  names=tuple(tp+alias+'_'+w for alias in TEST_ALIASES.values() for w in ('hi','lo'))+(tp+'fixed_test_f',tp+'fixed_test_b');tm=tuple(n for n in tq['metadata']['schema'] if n.startswith(tp) and ('primary_test_contact' in n or 'minus_' in n) and n.endswith(('_hi','_lo')));td=selected_words(tq,names+tm,'copied_source_test_q%d_r%d_j%d'%(iq,row,jet))
  test={n:copied_pair(td,tp+alias) for n,alias in TEST_ALIASES.items()};test.update(f=td[tp+'fixed_test_f'].copy(),b=td[tp+'fixed_test_b'].copy(),row=row,jet=jet,value_only=True,jet_order=('value','R','Z','t'),source_ref=thin(tq),same_candidate_provenance=refs['provenance'][iq],source_association_contacts={n:td[n] for n in tm});tests.append(test)
 for family in ('s','c'):
  for n,a in cache[family].items():assert np.array_equal(a,candidate[family][n])
 return candidate,cache,literal,tests


def prepare_coefficients(refs,basis,header):
 chunks=[];columns=[]
 for iq in range(4):
  CONTEXT.update(stage='hydrate_source_column',column=iq);candidate,cache,literal,tests=hydrate_column(refs,iq)
  assert np.array_equal(candidate['s']['R'],basis['R'][iq]);source=seal('SOURCE_COLUMN',dict(column=iq,input=header,source_cache=thin(refs['caches'][iq]),literal=thin(refs['literal'][iq]),tests=[x['source_ref'] for x in tests],candidate_provenance=refs['provenance'][iq],old_action_test_or_current_replayed=False))
  for lo in range(0,3784,128):
   hi=min(lo+128,3784);CONTEXT.update(stage='NEW_primitive_coefficient',column=iq,lo=lo,hi=hi);tag='NEW_literal_rate_coefficients_q%d_chunk%d'%(iq,lo)
   cc,tc,lc,tt=(slice_words(x,lo,hi) for x in (candidate,cache,literal,tests));tc['p']=hi-lo
   closed=dict(refs['closed'],same_candidate_provenance=refs['provenance'][iq])
   def port_complete(row,jet,part):
    capture_families('completed_NEW_port_',part);return seal('PORT',dict(column=iq,lo=lo,hi=hi,row=row,jet=jet,source_column=source,source_test=part['test_ref'],source_literal=part['literal_ref'],same_candidate_provenance=refs['provenance'][iq],represented_coefficient_only=True,uniform_original87_bound_earned=False))
   block=prepare_candidate_literal_rate_normal_point_coefficients(cc,tc,lc,tt,closed,keep,tag,port_complete);capture_families('completed_NEW_coefficient_',block)
   ref=seal('COEFFICIENT_CHUNK',dict(column=iq,lo=lo,hi=hi,source_column=source,port_refs=block['port_refs'],same_candidate_provenance=refs['provenance'][iq],normal_jet_order=['value','R','Z','t'],coefficient_scope=block['coefficient_scope'],uniform_original87_association_bound_earned=False,original87_whole_direction_authority_required=True))
   chunks.append(dict(column=iq,lo=lo,hi=hi,point_coefficients_ref=ref,same_candidate_provenance=refs['provenance'][iq],basis_provenance=thin(refs['basis'])))
  columns.append(seal('COEFFICIENT_COLUMN',dict(column=iq,source_column=source,chunks=chunks[-30:],all_six_physical_metric_components=True,uniform_source_rounding_or_inverse_qualified=False)))
 return chunks,columns


def comparison(label,actual,target,source_envelope,represented_envelope):
 rnc_pair(label+'_actual',actual,keep);rnc_pair(label+'_saved_original_target',target,keep)
 gap=rnc_pair(label+'_paired_difference',P.a_sub(actual,target),keep);keep(label+'_original_source_uncancelled_bound',source_envelope.copy());keep(label+'_represented_proxy_uncancelled_bound',represented_envelope.copy())
 bound=mp_add(source_envelope,represented_envelope,keep,label+'_comparison_bound');upper=mp_add(abs(gap[0]),abs(gap[1]),keep,label+'_gap_word_upper')
 assert bound.shape==upper.shape and np.all(bound>=0);ratio=np.zeros_like(bound);positive=bound>0;ratio[positive]=np.nextafter(upper[positive]/bound[positive],np.inf)
 exactzero=(gap[0]==0)&(gap[1]==0);ratio[~positive & ~exactzero]=np.inf
 keep(label+'_no_floor_component_ratios',ratio.copy());P.check(label,ratio,np.zeros_like(ratio),np.ones_like(ratio))


def validate_saved_direction(refs,basis,chunks,case):
 readout=refs['readouts'][case];direction=selected_record(readout['metadata']['direction_record'],refs['packets']['tests'],refs['receipts']['tests']);dp='direction%d_NEW_mechanical_rate_'%case
 names=tuple(dp+'NEW_original_'+n+'_lift_'+w for n in ('E','F') for w in ('hi','lo'))+tuple(dp+'NEW_nodes_'+n+'_'+w for n in ('native','metric') for w in ('hi','lo'))
 data=selected_words(direction,names,'copied_direction%d'%case);nv=copied_pair(data,dp+'NEW_original_E_lift');mv=copied_pair(data,dp+'NEW_original_F_lift');rnc_pair(dp+'copied_original_physical99',tuple(w.transpose(1,0,2).reshape(15136,99) for w in nv),keep,(15136,99));rnc_pair(dp+'copied_original_physical6',mv,keep,(15136,6))
 direction_copy=seal('DIRECTION_COPY',dict(direction=case,original=thin(direction),both_input_words=True,original_lifts_copied_not_replayed=True));coeff=P.a_dd(np.zeros((15136,4,4)));theta=P.a_dd(np.zeros(15136));en=np.zeros((15136,4,4));et=np.zeros(15136);column_refs=[]
 for iq in range(4):
  for d in chunks[30*iq:30*iq+30]:
   lo,hi=d['lo'],d['hi'];sl=slice(iq*3784+lo,iq*3784+hi);q=P.resolve_record(d['point_coefficients_ref']);names=tuple('completed_NEW_coefficient_'+n+'_'+w for n in ('normal_native','normal_metric','CMC_metric') for w in ('hi','lo'))+tuple('completed_NEW_coefficient_'+n for n in ('e_native','e_metric','e_CMC_metric'));bd=selected_words(q,names,'copied_new_coefficient_case%d_q%d_chunk%d'%(case,iq,lo))
   block={n:copied_pair(bd,'completed_NEW_coefficient_'+n) for n in ('normal_native','normal_metric','CMC_metric')};block.update({n:bd['completed_NEW_coefficient_'+n].copy() for n in ('e_native','e_metric','e_CMC_metric')});block['physical_adoption']=False
   native=tuple(w[:,sl].transpose(1,0,2).reshape(hi-lo,99).copy() for w in nv);metric=tuple(w[sl].copy() for w in mv);part=candidate_literal_rate_normal_point_apply(block,native,metric,keep,'NEW_saved_direction%d_q%d_chunk%d'%(case,iq,lo))
   for w in (0,1):coeff[w][sl]=part['normal_coefficients'][w];theta[w][sl]=part['initial_CMC_density'][w]
   en[sl]=part['normal_operation_envelope'];et[sl]=part['CMC_operation_envelope'];capture_families('completed_NEW_application_',part)
   seal('APPLICATION_CHUNK',dict(direction=case,column=iq,lo=lo,hi=hi,coefficient=d['point_coefficients_ref'],direction_record=direction_copy,source_direction=thin(direction),original_action_or_lift_replayed=False))
  col=slice(iq*3784,(iq+1)*3784);rnc_pair('completed_NEW_application_column_normal',P.a_slice(coeff,col),keep);rnc_pair('completed_NEW_application_column_CMC',P.a_slice(theta,col),keep);keep('completed_NEW_application_column_normal_envelope',en[col]);keep('completed_NEW_application_column_CMC_envelope',et[col]);column_refs.append(seal('APPLICATION_COLUMN',dict(direction=case,column=iq,same_candidate_provenance=refs['provenance'][iq],source_column=readout['metadata']['columns'][iq])))
 rd=selected_words(readout,tuple('completed_NEW_normal_CMC_'+n+'_'+w for n in ('weak_normal','weak_initial_CMC','time_primary_action_coefficients') for w in ('hi','lo'))+(dp+'full_uncancelled_normal_coefficients',dp+'full_uncancelled_CMC_density'),'copied_source_readout%d'%case)
 original_normal=[];original_CMC=[]
 for iq,ref in enumerate(readout['metadata']['columns']):
  q=selected_record(ref,refs['packets']['tests'],refs['receipts']['tests']);cd=selected_words(q,tuple('completed_NEW_column_'+n+'_'+w for n in ('normal_coefficients','initial_CMC_density') for w in ('hi','lo')),'copied_source_direction%d_column%d'%(case,iq));original_normal.append(copied_pair(cd,'completed_NEW_column_normal_coefficients'));original_CMC.append(copied_pair(cd,'completed_NEW_column_initial_CMC_density'))
 target=tuple(np.concatenate([q[w] for q in original_normal]) for w in (0,1));ctarget=tuple(np.concatenate([q[w] for q in original_CMC]) for w in (0,1));source_n=rd[dp+'full_uncancelled_normal_coefficients'];source_t=rd[dp+'full_uncancelled_CMC_density'];tag='NEW_saved_direction%d_association'%case
 comparison(tag+'_point_normal',coeff,target,source_n,en);rnc_pair(tag+'_point_CMC_descriptive_difference',P.a_sub(theta,ctarget),keep)
 spatial=P.a_slice(coeff,(slice(None),slice(None),slice(0,3)));weak=rnc_pair(tag+'_NEW_original_normal_Tstar',N.paired_scatter_normal(spatial,basis,tag+'_NEW_normal_Tstar'),keep);cmc=rnc_pair(tag+'_NEW_original_scalar_Tstar',P.dd_scalar_scatter(theta,basis,keep,tag+'_NEW_scalar_Tstar'),keep);primary=rnc_pair(tag+'_NEW_time_primary',P.a_mul64(-1.,P.a_slice(coeff,(slice(None),slice(None),3))),keep)
 ew,ec=rnc_positive_normal_CMC_scatter(en,et,basis,keep,tag+'_represented_Tstar_bound');sw,sc=rnc_positive_normal_CMC_scatter(source_n,source_t,basis,keep,tag+'_original_source_Tstar_bound')
 comparison(tag+'_weak_normal',weak,copied_pair(rd,'completed_NEW_normal_CMC_weak_normal'),sw,ew);comparison(tag+'_time_primary',primary,copied_pair(rd,'completed_NEW_normal_CMC_time_primary_action_coefficients'),source_n[:,:,3],en[:,:,3]);comparison(tag+'_weak_CMC',cmc,copied_pair(rd,'completed_NEW_normal_CMC_weak_initial_CMC'),sc,ec)
 capture_families('completed_NEW_readout_',dict(normal_coefficients=coeff,initial_CMC_density=theta,weak_normal=weak,weak_initial_CMC=cmc,time_primary_action_coefficients=primary,point_normal_envelope=en,point_CMC_envelope=et))
 return seal('READOUT',dict(direction=case,original_readout=thin(readout),original_direction=thin(direction),direction_copy=direction_copy,new_columns=column_refs,controls=CHECKS[-4:],sampled_association_only=True,uniform_source_rounding_or_fullweak_inverse_qualified=False))


def packet(refs):
 basis=selected_words(refs['input'],tuple('copied_original_basis_'+n for n in ('R','dv','hats','cell_i','cell_j')),'copied_source_INPUT');basis={n:basis['copied_original_basis_'+n].copy() for n in ('R','dv','hats','cell_i','cell_j')};assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 header=seal('INPUT',dict(kind='CLOSED_literal142_original247_tests_and147_temporalcache_only',parent_pins=PARENT_PINS,original_input=thin(refs['input']),basis=thin(refs['basis']),original_targets_current_and_epsilon_unchanged=True,construction_tolerance=2e-11))
 chunks,columns=prepare_coefficients(refs,basis,header);readouts=[validate_saved_direction(refs,basis,chunks,case) for case in range(2)]
 expected_roles=['INPUT']+sum((['SOURCE_COLUMN']+(['PORT']*16+['COEFFICIENT_CHUNK'])*30+['COEFFICIENT_COLUMN'] for _ in range(4)),[])+(['DIRECTION_COPY']+(['APPLICATION_CHUNK']*30+['APPLICATION_COLUMN'])*4+['READOUT'])*2+['PREPARATION']
 names=['NEW_saved_direction%d_association_'%case+n for case in range(2) for n in ('point_normal','weak_normal','time_primary','weak_CMC')]
 assert [q['name'] for q in CHECKS]==names and len(set(names))==8 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 q=seal('PREPARATION',dict(kind='NEW_literal_Rv_Tv_coefficients_and_sampled_saved_direction_associations',chunks=chunks,columns=columns,readouts=readouts,parent_pins=PARENT_PINS,same_candidate_provenance=refs['provenance'],basis=thin(refs['basis']),expected_control_names=names,controls=8,represented_coefficient_enclosure_only=True,uniform_original87_association_bound_earned=False,original87_whole_direction_authority_required=True,fullweak_global_inverse_or_physical_qualified=False))
 assert [q['metadata']['role'] for q in RECORDS]==expected_roles
 return dict(status='NEW_LITERAL_RATE_NORMAL_COEFFICIENTS_AND_SAVED_DIRECTION_ASSOCIATIONS_MEASURED',input=header,preparation=q,chunks=chunks,columns=columns,readouts=readouts,parent_pins=PARENT_PINS,expected_control_names=names,controls=len(names),roles=len(expected_roles),paired_point_count=15136,paired105_coordinate_consumption=True,old_action_test_EOS_current_or_lift_replayed=False,registered_Cstar_or_Schwarz_substituted=False,original_six_canonical_gates_not_evaluated=True,uniform_original87_association_bound_earned=False,original87_whole_direction_authority_required=True,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False,'Root FULL review and guarded release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace'
 load_containing_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);initialize_containing();refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,parent_pins=PARENT_PINS,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_literal_Rv_Tv_coefficients_or_association',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
