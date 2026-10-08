"""HELD NEW139 VALUE→literal306 Rv/Tv/time-primary refresh; definitions only.
Globals np,P,rnc_pair/rnc_box,mp_mul,RATE_COEFFICIENT_PARENT_PINS and reviewed306 preparation. No247/87,
EOS/current, 105 basis action, gauge Cstar or nodalTOTAL producer is invoked.
The containing reader authenticates closed parents and decodes selected words.
"""
NEW139_RV_AUTHOR_DRAFT=True
NEW139_RV_AUTHORING_IN_PROGRESS=False
NEW139_RV_SOURCE=(None,None)
NEW139_RV_RESULT=(None,None,None)
NEW139_RV_RECEIPT=(None,None,None)
NEW139_RV_PROOF=(None,None,None)
NEW139_RV_PARENT_PINS={
 'tests':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'literal':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)},
 'temporal':{'source':(None,None),'result':(None,None,None),'receipt':(None,None,None),'proof':(None,None,None)}}
NEW139_RV_SOURCE_PINS={
 'author_fragment_candidate_literal_rate_normal_coefficients_v001.py':'d9b7953600bf41de36d562f19adaa25f94674ad3234c74cad4ef0b527cf7adbb',
 'author_fragment_fixed_geometry_total_rate_state_v002.py':'aa5994d83b61ead93545f6f061a74be670d896af788d00a46a79798a442f2a8d',
 'cross_u_refreshed_total_rate_literal_gradient_contacts_v002.py':'5d1b4b30c01616c0514446b9546f9a6c434423c0723891fa8fec487d4dff0080',
 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py':'880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_weak_mechanical_positive_v001.py':'8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94'}
NEW139_RV_TEST_ALIASES={'q':'metric_test','It':'inverse_metric_test','eta':'native_test','zeta':'modal_test','Pt':'projector_test','Ft':'F_test','Vt':'V_test','Dt':'D_test','Kt':'KGamma_test','lm':'measure_test'}
NEW139_RV_TEST_SHAPES={'q':(4,4),'It':(4,4),'eta':(4,),'zeta':(32,4),'Pt':(4,4),'Ft':(4,4),'Vt':(32,4),'Dt':(32,4,4),'Kt':(3,3),'lm':()}
NEW139_RV_CURRENT_CONTACTS={'NEW_KGamma_minus_KADM':(3,3),'NEW_Ktrace_Gamma_minus_ADM':(),'NEW_raw225_first_jets_compatibility_minus_E0':(4,4,4),'NEW_raw225_first_jets_fixed_E0_minus_zero_E0_connection':(4,4,4)}
NEW139_RV_LITERAL_MARKS=('formal_Iu_minus_raw_up','literal_nz_adjoint_minus_registered_Pi','literal_acceleration_Z_minus_raw_Z','registered_current_PiU_minus_literal_nu_adjoint','matrix_chain_minus_factored_formal_metric_adjoint','formal_right_minus_raw_left_gradient','literal_left_minus_registered_gradient','literal_minus_registered_gradient')

def NEW139_rate_test_selectors(record):
 md=record['metadata'];assert md['failed'] is False and md['kind']=='RATE_STATE_NORMAL_TEST'
 iq,row,jet=(md[n] for n in ('column','row','jet'));assert all(isinstance(n,int) and 0<=n<4 for n in (iq,row,jet))
 schema=md['schema'];suffix='_NEW_native_EH_value_metric_test_hi';roots=[n[:-len('_metric_test_hi')] for n in schema if n.endswith(suffix)]
 assert len(roots)==1;root=roots[0];assert root.endswith('_column%d_row%d_jet%d_NEW_native_EH_value'%(iq,row,jet))
 pairs={n:tuple(root+'_'+alias+'_'+w for w in ('hi','lo')) for n,alias in NEW139_RV_TEST_ALIASES.items()}
 for n,names in pairs.items():
  tail=NEW139_RV_TEST_SHAPES[n];shape=(32,3784)+tail[1:] if n in ('zeta','Vt','Dt') else (3784,)+tail
  for key in names:assert schema[key]==dict(shape=list(shape),dtype='float64',finite=True),key
 fixed={n:root+'_fixed_test_'+n for n in ('f','b','df','db')}
 for n,shape in (('f',(3784,)),('b',(3784,3)),('df',(3784,4)),('db',(3784,4,3))):assert schema[fixed[n]]==dict(shape=list(shape),dtype='float64',finite=True)
 values={n:tuple('completed_RATE_STATE_NORMAL_TEST_'+n+'_'+w for w in ('hi','lo')) for n in ('total_action','total_Hamiltonian')}
 for names in values.values():
  for n in names:assert schema[n]==dict(shape=[3784],dtype='float64',finite=True)
 contacts=tuple(n for n in schema if n.startswith(root+'_') and ('primary_test_contact' in n or 'minus_' in n) and n.endswith(('_hi','_lo')))
 assert contacts and all(schema[n]['dtype']=='float64' and schema[n]['finite'] is True for n in contacts)
 return dict(label=root,pairs=pairs,fixed=fixed,current_values=values,source_contacts=contacts,column=iq,row=row,jet=jet,value_only=True,added_value_suffix=False)

def NEW139_rate_test_from_selected(record,data,selection,provenance,keep,label):
 assert not NEW139_RV_AUTHOR_DRAFT and not NEW139_RV_AUTHORING_IN_PROGRESS
 s=NEW139_rate_test_selectors(record);lo,hi=selection;assert 0<=lo<hi<=3784 and hi-lo<=128
 p=hi-lo;out={}
 for n,names in s['pairs'].items():
  axis=1 if n in ('zeta','Vt','Dt') else 0;key=(slice(None),slice(lo,hi)) if axis==1 else slice(lo,hi)
  pair=tuple(data[k][key].copy() for k in names);rnc_pair(label+'_copied_'+n,pair,keep);out[n]=pair
 for n,key in s['fixed'].items():out[n]=data[key][lo:hi].copy();keep(label+'_copied_fixed_test_'+n,out[n]);assert out[n].dtype==np.float64 and np.all(np.isfinite(out[n]))
 row,jet=s['row'],s['jet'];f=np.zeros(p);df=np.zeros((p,4));b=np.zeros((p,3));db=np.zeros((p,4,3));coordinate=(None,1,2,0)[jet]
 if row==0:
  if coordinate is None:f[:]=1.
  else:df[:,coordinate]=1.
 elif coordinate is None:b[:,row-1]=1.
 else:db[:,coordinate,row-1]=1.
 for n,expected in (('f',f),('df',df),('b',b),('db',db)):assert np.array_equal(out[n].view(np.uint64),expected.view(np.uint64)),n
 for n,names in s['current_values'].items():out['current_'+n]=rnc_pair(label+'_copied_current_'+n,tuple(data[k][lo:hi].copy() for k in names),keep,(p,))
 contacts={}
 for n in s['source_contacts']:
  a=data[n];axes=[i for i,size in enumerate(a.shape) if size==3784];assert len(axes)<=1;key=[slice(None)]*a.ndim
  if axes:key[axes[0]]=slice(lo,hi)
  contacts[n]=a[tuple(key)].copy();keep(label+'_source_test_contact_'+n,contacts[n])
 out.update(row=row,jet=jet,value_only=True,jet_order=('value','R','Z','t'),source_ref={n:record[n] for n in ('file','sha256','commit_file','commit_sha256')},same_candidate_provenance=provenance,source_value_label=s['label'],selection=[lo,hi],source_primitive_aliases=NEW139_RV_TEST_ALIASES.copy(),source_association_contacts=contacts,source_test_delta_words_are_value_evaluation_placeholders=True,configuration_test_JVP_earned=False)
 return out

def prepare_NEW139_literal_rate_normal_refresh(candidate,cache,literal,tests,baseline,closed,keep,label,port_complete,block_complete,CMC_carry=None):
 assert not NEW139_RV_AUTHOR_DRAFT and not NEW139_RV_AUTHORING_IN_PROGRESS and callable(port_complete) and callable(block_complete)
 assert closed['source_pins']==NEW139_RV_SOURCE_PINS and closed['physical_adoption'] is False and RATE_COEFFICIENT_PARENT_PINS==NEW139_RV_PARENT_PINS
 for group,pins in NEW139_RV_PARENT_PINS.items():
  for n,pin in pins.items():assert all(v is not None for v in pin) and tuple(closed[group][n])==pin
  assert closed[group]['naturally_closed'] is True and closed[group]['natural_exit_code']==0 and closed[group]['all_selected_seals_verified'] is True
 p=cache['p'];assert 0<p<=128 and len(tests)==16;prov=closed['same_candidate_provenance'];iq=closed['column'];lo,hi=closed['selection'];assert hi-lo==p and 0<=iq<4
 assert all(isinstance(n,int) for n in (iq,lo,hi)) and 0<=lo<hi<=3784 and lo%128==0 and hi==min(lo+128,3784)
 chunk_ordinal=30*iq+lo//128;assert closed['chunk_count']==120 and closed['chunk_ordinal']==chunk_ordinal
 assert candidate['candidate_provenance']==cache['candidate_provenance']==literal['same_candidate_provenance']==prov
 assert tuple(tuple(q) for q in prov['finite_terminal'])==tuple(NEW139_RV_PARENT_PINS['tests'][n] for n in ('source','result','receipt','proof')) and prov['point_TOTAL_time_words']==prov['fresh_stages']['RATE_STATE_INPUT'] and prov['nodal_TOTAL_equivalence_earned'] is False
 assert closed['fresh_literal_column']==literal['closed_literal_ref'] and closed['fixed147_cache_ref'] and closed['same_raw_configuration_and_E0_words_verified'] is True
 assert closed['old_rate_dependent_operands_reused'] is False and closed['old87_controls_transferred_to_NEW_state'] is False and closed['registered_Cstar_substituted'] is False
 contacts=cache['source_primary_contacts'];assert contacts['NEW139_state_refs']==prov['fresh_stages'] and contacts['words'] and literal['source_association_contacts']
 assert contacts['records']['RATE_STATE_FIRST_JETS']==prov['fresh_stages']['RATE_STATE_FIRST_JETS'] and contacts['records']['FIRST_NORMAL_TEST']==tests[0]['source_ref']
 for n,tail in NEW139_RV_CURRENT_CONTACTS.items():
  root='NEW_FIXED_GEOMETRY_TOTAL_RATE_column%d_'%iq+n;rnc_pair(label+'_fresh_current_contact_'+n,tuple(contacts['words'][root+'_'+w] for w in ('hi','lo')),keep,(p,)+tail)
 assert literal['closed_literal_ref']==closed['literal']['column_refs'][iq] and literal['source_association_contacts']['record']==literal['closed_literal_ref']
 for marker in NEW139_RV_LITERAL_MARKS:
  names=[n for n in literal['source_association_contacts']['words'] if n.startswith('NEW_refreshed_literal_q%d_'%iq) and marker in n and n.endswith('_hi')];assert names,marker
  for name in names:rnc_pair(label+'_fresh_literal_contact_'+name[:-3],tuple(literal['source_association_contacts']['words'][name[:-3]+'_'+w] for w in ('hi','lo')),keep)
 rnc_pair(label+'_owned_NEW139_normal_value',baseline['normal_value_hamiltonian'],keep,(p,4,4));rnc_pair(label+'_owned_NEW139_time_primary_value',baseline['time_primary_action'],keep,(p,4));rnc_pair(label+'_owned_NEW139_CMC_value',baseline['initial_CMC_density'],keep,(p,))
 assert baseline['readout_ref']==closed['tests']['readout_ref'] and baseline['column_ref']==closed['tests']['column_refs'][iq] and baseline['time_primary_semantics']=='unweighted minus Hamiltonian t; original collector sign association retained'
 for serial,test in enumerate(tests):
  row,jet=divmod(serial,4);assert (test['row'],test['jet'])==(row,jet) and test['selection']==[lo,hi] and test['source_ref']==closed['tests']['normal_test_refs'][16*iq+serial] and test['same_candidate_provenance']==prov
  assert test['source_value_label'].endswith('_column%d_row%d_jet%d_NEW_native_EH_value'%(iq,row,jet)) and test['source_primitive_aliases']==NEW139_RV_TEST_ALIASES and test['source_association_contacts']
  assert test['source_test_delta_words_are_value_evaluation_placeholders'] is True and test['configuration_test_JVP_earned'] is False
  for w in (0,1):assert np.array_equal(test['current_total_Hamiltonian'][w].view(np.uint64),baseline['normal_value_hamiltonian'][w][:,row,jet].view(np.uint64))
 def completed(row,jet,part):
  part=dict(part,current_total_action=tests[4*row+jet]['current_total_action'],current_total_Hamiltonian=tests[4*row+jet]['current_total_Hamiltonian'],NEW139_baseline_readout=baseline['readout_ref'],fresh_literal_ref=literal['closed_literal_ref'],source_test_contact_ref=tests[4*row+jet]['source_ref'],source_test_association_contacts=tests[4*row+jet]['source_association_contacts'],column=iq,selection=[lo,hi],chunk_ordinal=chunk_ordinal,old87_direction_contacts_not_transferred=True)
  ref=port_complete(row,jet,part);assert isinstance(ref,dict) and all(ref.get(n) for n in ('file','sha256','commit_file','commit_sha256'));return ref
 block=prepare_candidate_literal_rate_normal_point_coefficients(candidate,cache,literal,tests,closed,keep,label+'_NEW306',completed)
 carry_used=False
 if CMC_carry is not None:
  assert CMC_carry['source_sha256']==NEW139_RV_SOURCE_PINS['author_fragment_candidate_literal_rate_normal_coefficients_v001.py'] and CMC_carry['all_selected_seals_verified'] is True and CMC_carry['record']
  geom=dict(N=cache['c']['N'],hi00=cache['s']['hi'][:,0,0],I=cache['c']['ih'],mu=cache['c']['sqrt_h'])
  for n,x in geom.items():keep(label+'_CMC_raw_geometry_'+n,x.copy());assert np.array_equal(x.view(np.uint64),CMC_carry['geometry_words'][n].view(np.uint64)),n
  rnc_pair(label+'_saved_geometric_CMC',CMC_carry['CMC_metric'],keep,(p,6));keep(label+'_saved_geometric_CMC_unsigned',CMC_carry['e_CMC_metric'].copy())
  for w in (0,1):assert np.array_equal(block['CMC_metric'][w].view(np.uint64),CMC_carry['CMC_metric'][w].view(np.uint64))
  assert np.array_equal(block['e_CMC_metric'].view(np.uint64),CMC_carry['e_CMC_metric'].view(np.uint64));carry_used=True
 for n,e in (('native','e_native'),('metric','e_metric')):
  source=P.a_slice(block['normal_'+n],(slice(None),slice(None),3));time=rnc_pair(label+'_NEW_time_primary_rate_'+n,P.a_mul64(-1.,source),keep,(p,4,99 if n=='native' else 6))
  bound=mp_mul(np.ones_like(block[e][:,:,3]),block[e][:,:,3],keep,label+'_NEW_time_primary_rate_unsigned_'+n);rnc_box(label+'_NEW_time_primary_rate_box_'+n,time,keep,bound);block['time_primary_rate_'+n]=time;block['e_time_primary_rate_'+n]=bound
 block.update(column=iq,selection=[lo,hi],chunk_ordinal=chunk_ordinal,chunk_count=120,current_normal_value=baseline['normal_value_hamiltonian'],current_time_primary_action=baseline['time_primary_action'],current_initial_CMC_density=baseline['initial_CMC_density'],NEW139_baseline_readout=baseline['readout_ref'],fresh_literal_ref=literal['closed_literal_ref'],current_time_primary_refreshed_by_saved_VALUE=True,CMC_geometric_carry_words_checked=carry_used,old87_association_controls_transferred=False,source_unsigned_scope='306 reverse polynomial conditional on authentic NEW139 test/feature and NEW220 primitive-adjoint seeds',upstream_test_producer_or_uniform87_error_bound_qualified=False,normal_feedback_or_configuration_step_admitted=False,physical_adoption=False)
 ref=block_complete(block);assert isinstance(ref,dict) and all(ref.get(n) for n in ('file','sha256','commit_file','commit_sha256'));block['completed_refresh_ref']=ref
 return block
