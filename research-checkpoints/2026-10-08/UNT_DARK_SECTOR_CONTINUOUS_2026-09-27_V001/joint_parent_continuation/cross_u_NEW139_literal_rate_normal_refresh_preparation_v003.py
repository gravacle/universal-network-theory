"""HELD executable NEW139/220→115/306 coefficient refresh; root only.
Selected authenticated CLOSED operands, no old producer/action replay.
"""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_NEW139_LITERAL_RATE_NORMAL_REFRESH_PREPARATION_V003'
DRIVER_PROTOCOL='NEW139_LITERAL_RATE_NORMAL_REFRESH_PREPARATION_V003.md'
PROTOCOL_SHA='a0e511ef0a86b0b6ef8e9ed8237fe24402762272bf0614933a40836ffedca5f4'
SELECTED_MAP=(None,None)
PARENT_PINS={name:dict(source=(None,None),result=(None,None,None),receipt=(None,None,None),proof=(None,None,None)) for name in ('tests','literal','temporal')}
MAP_STATUS='ROOT_CLOSED_NEW139_LITERAL_RATE_NORMAL_REFRESH_SELECTED_RECORDS_VERIFIED'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d', 'author_fragment_candidate_literal_temporal_gradient_bridge_v001.py': '880d9689965e7f66a159178cbec13b0a1e03e3929c7796e90c4370a9919f4d50', 'author_fragment_candidate_weak_mechanical_positive_v001.py': '8cf1755229239145abb1ce89afd8f450044e3fd0a69d2c7a62f769e850076b94', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_candidate_literal_rate_normal_coefficients_v001.py': 'd9b7953600bf41de36d562f19adaa25f94674ad3234c74cad4ef0b527cf7adbb', 'author_fragment_NEW139_literal_rate_normal_refresh_v001.py': '096b8d3a6d0ec7fa17f15d4e7ad57f45710ee1eb66cba888c74897425b220231', 'cross_u_refreshed_total_rate_literal_gradient_contacts_v002.py': '5d1b4b30c01616c0514446b9546f9a6c434423c0723891fa8fec487d4dff0080'}
PINS['author_fragment_fixed_rate_inherited_success_admission_v001.py']='8da980eeb2c429b8612cd0c69be37490b3efa661978ecbedb859f03bce761687'
SNAMES=('g', 'hi', 'U', 'z', 'uc', 'P', 'Z', 'r', 'z2', 'f', 'phi', 'omega', 'xi', 'w', 'R', 'Z_coordinate')
CNAMES=('h', 'ih', 'N', 'beta', 'u', 'up', 'gamma', 'dens', 'sqrt_h', 'JU', 'JzU', 'Jzz', 'Uh', 'zh', 'embed')
FEATURE_NAMES=('F', 'Fup', 'V', 'V_raised', 'D', 'D_raised', 'Pi', 'PiU')
MOMENT_NAMES=('K', 'Ktrace', 'native_density', 'metric_native_density', 'metric_EH_tensor', 'metric_EH_density', 'metric_total_density')
MATERIAL=('B', 'GC', 'ALPHA', 'ELL', 'C')
LITERAL_ALIASES={'F':'literal_F_adjoint','V':'literal_V_adjoint','D':'literal_D_adjoint','nu':'literal_nu_adjoint','nz':'literal_nz_adjoint','Z':'literal_acceleration_Z_partial'}
COLUMN_ROLES=('BASELINE_COLUMN_INPUT','RATE_STATE_INPUT','RATE_STATE_FIRST_JETS','RATE_STATE_FEATURES','RATE_STATE_MOMENTA','RATE_STATE_COLUMN')
np=P=None;SCOPE={};RAW={};AVAILABLE={};BALANCED={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def definitions(file,names,scope):
 tree=ast.parse((BASE/file).read_text());items=[n for n in tree.body if isinstance(n,ast.FunctionDef) and (names is None or n.name in names)]
 assert names is None or {n.name for n in items}==set(names),file
 exec(compile(ast.Module(body=items,type_ignores=[]),file,'exec'),scope)

def keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a
 if 'exact_product' in name:BALANCED[name]=a
 while len(AVAILABLE)>32:AVAILABLE.pop(next(iter(AVAILABLE)))
 while len(BALANCED)>16:BALANCED.pop(next(iter(BALANCED)))
 CONTEXT['last_capture']=name;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));return a

def initialize():
 global np
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for n,h in PINS.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
 definitions(IO_PARENT,{'bind','read','arrays','thin','initialize_io'},globals());initialize_io()
 definitions('author_fragment_single_decode_recheck_v001.py',{'recheck'},SCOPE);P.recheck=SCOPE['recheck']
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_sum'}
 definitions(list(PINS)[0],base,SCOPE);definitions(list(PINS)[1],primitive,SCOPE)
 for n in base|primitive|set(MATERIAL):setattr(P,n,SCOPE[n])
 globals().update({n:SCOPE[n] for n in base|primitive|set(MATERIAL)})
 choices=(('author_fragment_finite_york_geometry_target_v001.py',{'fy_keep','fy_sum','fy_mv','fy_mm','fy_contract','fy_div'}),('author_fragment_exact_exponent_two_product_v003.py',None),('author_fragment_candidate_literal_temporal_gradient_bridge_v001.py',{'lg_six'}),('author_fragment_candidate_weak_mechanical_positive_v001.py',{'mp_out','mp_add','mp_mul','mp_div','mp_sum','mp_mm','mp_mv'}),('author_fragment_candidate_chunk_point_block_provider_v001.py',{'candidate_point_cache_names'}),('author_fragment_candidate_literal_rate_normal_coefficients_v001.py',{'rnc_pair','rnc_box','rnc_view','rnc_transpose','rnc_expand','rnc_algebra','rnc_outer','rnc_gamma_time_reverse','rnc_DG_pullback','rnc_Gamma_adjoint','rnc_chart_reverse','rnc_primitive_rate_reverse','rnc_test_rate_reverse','rnc_test_primitive_adjoint','rnc_EH_coefficients','prepare_candidate_literal_rate_normal_point_coefficients'}),('author_fragment_NEW139_literal_rate_normal_refresh_v001.py',None),('cross_u_refreshed_total_rate_literal_gradient_contacts_v002.py',{'hydrate'}),('author_fragment_fixed_rate_inherited_success_admission_v001.py',{'fixed_rate_inherited_success_admission','fixed_rate_record_seals'}))
 for file,names in choices:definitions(file,names,globals())
 for file,prefixes in (('author_fragment_candidate_chunk_point_block_provider_v001.py',('POINT_',)),('author_fragment_NEW139_literal_rate_normal_refresh_v001.py',('NEW139_RV_',))):
  for n in ast.parse((BASE/file).read_text()).body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id.startswith(prefixes):globals()[n.targets[0].id]=ast.literal_eval(n.value)
 globals().update(NEW139_RV_AUTHOR_DRAFT=False,NEW139_RV_AUTHORING_IN_PROGRESS=False,NEW139_RV_PARENT_PINS=PARENT_PINS,RATE_COEFFICIENT_AUTHOR_DRAFT=False,RATE_COEFFICIENT_AUTHORING_IN_PROGRESS=False,RATE_COEFFICIENT_PARENT_PINS=PARENT_PINS)
 globals().update(FINITE_SOURCE=PARENT_PINS['tests']['source'],FINITE_RESULT=PARENT_PINS['tests']['result'],FINITE_RECEIPT=PARENT_PINS['tests']['receipt'],FINITE_CLOSURE_PROOF=PARENT_PINS['tests']['proof'])
 install_exact_exponent_product(SCOPE,P,keep,'NEW139_Rv_exact_product');globals()['a_prod']=P.a_prod
 assert SCOPE['a_prod'] is P.a_prod and SCOPE['a_mul'].__globals__ is SCOPE

def canonical(v):return json.loads(json.dumps(v,sort_keys=True))

def closed_group(name):
 pins=PARENT_PINS[name];assert all(v is not None for q in pins.values() for v in q)
 for q in pins.values():bind(q[0],q[1])
 rc=json.loads(P.path(pins['receipt'][0]).read_text());proof=json.loads(P.path(pins['proof'][0]).read_text())
 assert rc['status']==pins['receipt'][2]=='CLOSED' and proof['status']==pins['proof'][2]
 assert rc['owner']==proof['owner'] and rc['owner']['source_sha256']==pins['source'][1]==proof['source_sha256']
 assert rc['result_sha256']==pins['result'][1]==proof['result_sha256'] and proof['receipt_sha256']==pins['receipt'][1] and rc.get('error_sha256') is None
 assert proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is True and proof['all_success_role_seals_verified'] is True
 assert rc['qualification'] and all(v is False for v in rc['qualification'].values())
 stem=pins['result'][0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 if name=='tests':
  assert P.path(pins['result'][0]).stat().st_size<=128*1024*1024
  r=json.loads(P.path(pins['result'][0]).read_text());assert r['status']==pins['result'][2] and r['owner']==rc['owner'] and r['qualification']==rc['qualification']
  rc=dict(rc,_fixed_rate_inherited_success=fixed_rate_inherited_success_admission(r,rc,bind))
 return dict(**pins,naturally_closed=True,natural_exit_code=0,all_selected_seals_verified=True,owner=rc['owner'],receipt_data=rc)

def admitted_record(group,ref):
 bind(ref['commit_file'],ref['commit_sha256']);q=json.loads(P.path(ref['commit_file']).read_text());assert q['file']==ref['file'] and q['sha256']==ref['sha256']
 q=dict(q,commit_file=ref['commit_file'],commit_sha256=ref['commit_sha256']);md=q['metadata'];seals=fixed_rate_record_seals(dict(owner=group['owner']),group['receipt_data'],q);assert md['failed'] is False and md['qualification'] and all(v is False for v in md['qualification'].values())
 for n,h in ((q['file'],q['sha256']),(q['commit_file'],q['commit_sha256'])):assert seals[n]==h
 return q

def selected(q,names,label):
 assert len(names)==len(set(names)) and all(n in q['metadata']['schema'] for n in names),label
 bind(q['file'],q['sha256']);bind(q['commit_file'],q['commit_sha256']);data=read(q,names)
 for n,a in data.items():
  s=q['metadata']['schema'][n];assert list(a.shape)==s['shape'] and str(a.dtype)==s['dtype'] and s['finite'] is True,n
 RAW.clear();return data

def saved_pair(data,prefix):return tuple(data[prefix+'_'+w].copy() for w in ('hi','lo'))

def clear():
 RAW.clear();AVAILABLE.clear();BALANCED.clear();DD_ARRAY_CURRENT.clear()

def publish_payload(out,prefix,value):
 if isinstance(value,dict):
  for n,x in value.items():publish_payload(out,prefix+n+'_',x)
 elif isinstance(value,tuple) and len(value)==2 and all(isinstance(a,np.ndarray) for a in value):
  for w,a in zip(('hi','lo'),value):out[prefix+w]=np.asarray(a).copy()
 elif isinstance(value,np.ndarray):out[prefix.removesuffix('_')]=value.copy()

def seal(role,metadata,payload=None):
 values={};publish_payload(values,'completed_',payload or {})
 values.update({'last_capture_'+n:a.copy() for n,a in AVAILABLE.items()});values.update({'last_balance_'+n:a.copy() for n,a in BALANCED.items()});values.update({'last_DD_'+n:a.copy() for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()})
 if not values:values['completed_role_ordinal']=np.asarray(len(RECORDS),dtype=np.int64)
 q=P.checkpoint(role,values,dict(metadata,context=dict(CONTEXT),physical_adoption=False));clear();return thin(q)

def admission():
 assert all(v is not None for v in SELECTED_MAP);bind(*SELECTED_MAP);m=json.loads(P.path(SELECTED_MAP[0]).read_text())
 assert m['status']==MAP_STATUS and m['all_selected_seals_verified'] is True and m['all_source_roles_schema_associations_verified'] is True and m['physical_adoption'] is False
 assert m['terminals']==canonical(PARENT_PINS) and m['result_statuses']=={n:pins['result'][2] for n,pins in PARENT_PINS.items()};groups={n:closed_group(n) for n in PARENT_PINS}
 assert m['owners']=={n:g['owner'] for n,g in groups.items()} and len(m['columns'])==4
 fi=admitted_record(groups['tests'],m['finite_input']);out=admitted_record(groups['tests'],m['readout']);assert fi['metadata']['kind']=='INPUT' and out['metadata']['kind']=='READOUT'
 assert out['metadata']['kind_scope']=='fresh_point_first_TOTAL_rate_momenta_all16normal_CMC_at_unchanged_spatial_geometry'
 br=P.resolve_record(m['original_basis']);bind(br['file'],br['sha256']);bind(br['commit_file'],br['commit_sha256']);assert br['metadata']['failed'] is False
 cols=[];caches=[];literals=[];normal=[]
 for iq,spec in enumerate(m['columns']):
  assert spec['column']==iq and set(spec['stages'])==set(COLUMN_ROLES) and len(spec['normal_tests'])==16
  q={n:admitted_record(groups['tests'],r) for n,r in spec['stages'].items()}
  for n,r in q.items():assert r['metadata']['kind']==n and r['metadata']['column']==iq
  tests=[admitted_record(groups['tests'],r) for r in spec['normal_tests']]
  for serial,r in enumerate(tests):assert (r['metadata']['column'],r['metadata']['row'],r['metadata']['jet'])==(iq,*divmod(serial,4)) and r['metadata']['kind']=='RATE_STATE_NORMAL_TEST'
  cache=admitted_record(groups['temporal'],spec['cache']);literal=admitted_record(groups['literal'],spec['literal']);tx=admitted_record(groups['literal'],spec['literal_transaction'])
  assert cache['metadata']['column']==literal['metadata']['column']==tx['metadata']['column']==iq and cache['metadata']['points']==3784 and cache['metadata']['configuration_held'] is True
  assert cache['metadata']['state']==q['BASELINE_COLUMN_INPUT']['metadata']['state']==fi['metadata']['provenance']['original_owned_TOTAL_time_words'][iq]
  assert literal['metadata']['transaction']==thin(tx) and tx['metadata']['fresh_stages']=={n:thin(r) for n,r in q.items()} and tx['metadata']['fixed147_cache']==thin(cache) and tx['metadata']['same_raw_configuration_and_E0_words_verified'] is True
  cols.append(q);caches.append(cache);literals.append(literal);normal.append(tests)
 return dict(groups=groups,finite_input=fi,finite_readout=out,basis=br,columns=cols,literals=literals,normal=normal,mechanical=dict(caches=caches),selected_map=SELECTED_MAP)

def slice_words(x,lo,hi):
 if isinstance(x,dict):return {n:slice_words(a,lo,hi) for n,a in x.items()}
 if isinstance(x,tuple):return tuple(slice_words(a,lo,hi) for a in x)
 if isinstance(x,np.ndarray):
  axes=[i for i,n in enumerate(x.shape) if n==3784];assert len(axes)<=1
  if axes:
   key=[slice(None)]*x.ndim;key[axes[0]]=slice(lo,hi);return x[tuple(key)].copy()
  return x.copy()
 return x

def column_inputs(refs,iq,readout):
 candidate,cache,tx=hydrate(refs,iq);q=refs['columns'][iq];prov=candidate['candidate_provenance'];p='NEW_FIXED_GEOMETRY_TOTAL_RATE_column%d_'%iq
 words={};records={'RATE_STATE_FIRST_JETS':thin(q['RATE_STATE_FIRST_JETS']),'FIRST_NORMAL_TEST':thin(refs['normal'][iq][0])}
 for kind,names in (('RATE_STATE_FIRST_JETS',('NEW_raw225_first_jets_compatibility_minus_E0','NEW_raw225_first_jets_fixed_E0_minus_zero_E0_connection')),('FIRST_NORMAL_TEST',('NEW_KGamma_minus_KADM','NEW_Ktrace_Gamma_minus_ADM'))):
  r=q[kind] if kind in q else refs['normal'][iq][0];d=selected(r,tuple(p+n+'_'+w for n in names for w in ('hi','lo')),'fresh_primary_'+kind);words.update(d)
 cache['source_primary_contacts']=dict(NEW139_state_refs=prov['fresh_stages'],records=records,words=words)
 lq=refs['literals'][iq];lp='NEW_refreshed_literal_q%d_'%iq;names=tuple(lp+n+'_'+w for n in LITERAL_ALIASES.values() for w in ('hi','lo'));marks=NEW139_RV_LITERAL_MARKS
 bridges=tuple(n for n in lq['metadata']['schema'] if n.startswith(lp) and any(mark in n for mark in marks) and n.endswith(('_hi','_lo')));assert bridges
 data=selected(lq,names+bridges,'fresh_literal');literal={n:saved_pair(data,lp+a) for n,a in LITERAL_ALIASES.items()};literal.update(same_candidate_provenance=prov,closed_literal_ref=thin(lq),primitive_adjoints_are_literal142=True,source_association_contacts=dict(record=thin(lq),words={n:data[n] for n in bridges}))
 cq=q['RATE_STATE_COLUMN'];cp='completed_RATE_STATE_COLUMN_value_';d=selected(cq,tuple(cp+n+'_'+w for n in ('normal_coefficients','initial_CMC_density') for w in ('hi','lo')),'fresh_column_VALUES');normal_value=saved_pair(d,cp+'normal_coefficients');theta=saved_pair(d,cp+'initial_CMC_density');sl=slice(iq*3784,(iq+1)*3784)
 time=tuple(a[sl].copy() for a in saved_pair(readout,'completed_READOUT_normal_CMC_value_time_primary_action_coefficients'));rd=saved_pair(readout,'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_value_current_point_Hamiltonian_normal');rt=saved_pair(readout,'NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_value_current_initial_CMC_density')
 for w in (0,1):assert np.array_equal(normal_value[w][:,:,:3].view(np.uint64),rd[w][sl].view(np.uint64)) and np.array_equal(theta[w].view(np.uint64),rt[w][sl].view(np.uint64))
 baseline=dict(normal_value_hamiltonian=normal_value,time_primary_action=time,initial_CMC_density=theta,readout_ref=thin(refs['finite_readout']),column_ref=thin(cq),time_primary_semantics='unweighted minus Hamiltonian t; original collector sign association retained')
 tests=[]
 for r in refs['normal'][iq]:
  selector=NEW139_rate_test_selectors(r);names=tuple(n for pair in selector['pairs'].values() for n in pair)+tuple(selector['fixed'].values())+tuple(n for pair in selector['current_values'].values() for n in pair)+selector['source_contacts'];tests.append((r,selected(r,names,'fresh_VALUE_test')))
 return candidate,cache,literal,baseline,tests,tx

def packet(refs):
 basis=selected(refs['basis'],('R','dv','hats'),'original_registered_basis');fb=selected(refs['finite_input'],tuple('completed_INPUT_basis_'+n for n in basis),'fresh139_basis')
 for n,shape in (('R',(4,3784)),('dv',(4,3784)),('hats',(4,4,3,86,44))):assert basis[n].shape==shape
 for n,a in basis.items():assert np.array_equal(a.view(np.uint64),fb['completed_INPUT_basis_'+n].view(np.uint64)),n
 readout=selected(refs['finite_readout'],tuple(n+'_'+w for n in ('NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_value_current_point_Hamiltonian_normal','completed_READOUT_normal_CMC_value_time_primary_action_coefficients','NEW_FIXED_GEOMETRY_TOTAL_RATE_NEW_value_normal_CMC_value_current_initial_CMC_density') for w in ('hi','lo')),'fresh_READOUT_VALUES')
 inp=seal('INPUT',dict(selected_map=SELECTED_MAP,terminals=PARENT_PINS,original_basis=thin(refs['basis']),finite_input=thin(refs['finite_input']),readout=thin(refs['finite_readout']),new_controls=0),dict(readout=readout,basis=basis))
 columns=[];allchunks=[];transactions=[]
 for iq in range(4):
  candidate,cache,literal,baseline,tests,tx=column_inputs(refs,iq,readout);transactions.append(tx);prov=candidate['candidate_provenance'];chunks=[]
  for lo in range(0,3784,128):
   hi=min(lo+128,3784);ordinal=30*iq+lo//128;CONTEXT.update(stage='NEW306_reverse_chunk',column=iq,selection=[lo,hi],chunk_ordinal=ordinal)
   c=slice_words(candidate,lo,hi);k=slice_words(cache,lo,hi);k['p']=hi-lo;l=slice_words(literal,lo,hi);b=slice_words(baseline,lo,hi)
   local=[NEW139_rate_test_from_selected(r,d,(lo,hi),prov,keep,'q%d_chunk%d_test%d'%(iq,ordinal,j)) for j,(r,d) in enumerate(tests)]
   closed={n:{key:v for key,v in g.items() if key!='receipt_data'} for n,g in refs['groups'].items()};closed['tests'].update(readout_ref=thin(refs['finite_readout']),column_refs=[thin(q['RATE_STATE_COLUMN']) for q in refs['columns']],normal_test_refs=[thin(r) for rows in refs['normal'] for r in rows]);closed['literal']['column_refs']=[thin(q) for q in refs['literals']]
   closed.update(source_pins=NEW139_RV_SOURCE_PINS,physical_adoption=False,same_candidate_provenance=prov,column=iq,selection=[lo,hi],chunk_count=120,chunk_ordinal=ordinal,fresh_literal_column=l['closed_literal_ref'],fixed147_cache_ref=thin(refs['mechanical']['caches'][iq]),same_raw_configuration_and_E0_words_verified=True,old_rate_dependent_operands_reused=False,old87_controls_transferred_to_NEW_state=False,registered_Cstar_substituted=False)
   def port_complete(row,jet,part):
    CONTEXT.update(row=row,jet=jet,stage='seal_NEW306_reverse_port');payload={n:part[n] for n in ('native','metric','e_native','e_metric','current_total_action','current_total_Hamiltonian')}
    return seal('REFRESH_PORT',dict(column=iq,selection=[lo,hi],chunk_ordinal=ordinal,row=row,jet=jet,test_ref=part['test_ref'],literal_ref=part['literal_ref'],readout=b['readout_ref'],same_candidate_provenance=prov,represented_coefficient_only=True,original87_association_earned=False),payload)
   def block_complete(block):
    payload={n:block[n] for n in ('normal_native','normal_metric','CMC_metric','e_native','e_metric','e_CMC_metric','time_primary_rate_native','time_primary_rate_metric','e_time_primary_rate_native','e_time_primary_rate_metric','current_normal_value','current_time_primary_action','current_initial_CMC_density')}
    return seal('REFRESH_CHUNK',dict(column=iq,selection=[lo,hi],chunk_ordinal=ordinal,chunk_count=120,port_refs=block['port_refs'],same_candidate_provenance=prov,original_basis=thin(refs['basis']),readout=b['readout_ref'],column_ref=b['column_ref'],literal=l['closed_literal_ref'],fixed147_cache=thin(refs['mechanical']['caches'][iq]),normal_jet_order=['value','R','Z','t'],time_primary_semantics=b['time_primary_semantics'],source_unsigned_scope=block['source_unsigned_scope'],original87_association_earned=False),dict(refresh=payload))
   block=prepare_NEW139_literal_rate_normal_refresh(c,k,l,local,b,closed,keep,'NEW139_Rv_q%d_chunk%d'%(iq,ordinal),port_complete,block_complete);chunks.append(block['completed_refresh_ref']);allchunks.append(block['completed_refresh_ref'])
   del c,k,l,b,local,block
  assert len(chunks)==30;columns.append(seal('COLUMN_INDEX',dict(column=iq,chunks=chunks,transaction=tx,same_candidate_provenance=prov,readout=thin(refs['finite_readout']),source_arrays_not_recopied=True)))
  del candidate,cache,literal,baseline,tests
 assert len(allchunks)==120 and len(RECORDS)==2049 and CHECKS==[]
 final=seal('PREPARATION',dict(input=inp,columns=columns,chunks=allchunks,transactions=transactions,original_basis=thin(refs['basis']),readout=thin(refs['finite_readout']),terminals=PARENT_PINS,selected_map=SELECTED_MAP,reverse_ports=1920,new_controls=0,original87_controls_transferred=False,normal_feedback_or_configuration_step_admitted=False));assert len(RECORDS)==2050
 return dict(status='NEW139_LITERAL_RATE_NORMAL_COEFFICIENTS_REFRESHED_UNQUALIFIED',input=inp,columns=columns,chunks=allchunks,preparation=final,terminals=PARENT_PINS,selected_map=SELECTED_MAP,reverse_ports=1920,roles=2050,new_controls=0,represented_coefficient_only=True,original87_association_earned=False,normal_feedback_or_configuration_step_admitted=False,physical_adoption=False)

def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and all(v is not None for q in PARENT_PINS.values() for pin in q.values() for v in pin) and all(v is not None for v in SELECTED_MAP),'Root closure binding and FULL review required'
 assert not list(BASE.glob(STEM+'_*'));initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,selected_map=SELECTED_MAP,terminals=PARENT_PINS,planned_roles=2050,new_controls=0,physical_adoption=False))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**BALANCED,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='unfinished_NEW139_Rv_refresh',context=dict(CONTEXT)),failed=True)
  except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
