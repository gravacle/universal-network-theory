"""HELD cached updated-phase compact-chi contact measurement.
Only direction stages and required weak assembly are new. EOS values/logs,
geometry/mechanical/ordinary/CMC producers and old phase actions are not called.
Root releases after complete source/protocol review; all physical flags false.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CROSS_U_CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V004'
DRIVER_PROTOCOL='CROSS_U_CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V001.md'
PROTOCOL_SHA='dc13b3930661e8d1780b3d73fc524babc9366f9851822f4e86a61fb81efc8821'
IO_PARENT='cross_u_finite0_candidate_action_residual_v007.py'
IO_PARENT_SHA='ab8f320aa42d86987a24381ad7db949e2c561d577d7b2434fb3f667954960c58'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'cross_u_paired_current_normal_constraints_v002.py':'a4c33e69147ca1b848d647e7946c6eaad9081bc9fd389015f1cdcd9132b89b40',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_candidate_phase_normal_stress_v001.py':'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd',
 'author_fragment_finite_candidate_native_EH_normal_v003.py':'5c608d018a06b0f2b7e3947c9d37baa249317036c1a3f5f067815b51bf8a7499',
 'author_fragment_fixed_geometry_phase_normal_join_v001.py':'7cf77563d0f0c5011f06119017a313df79cb9bf865a2e207c20167ca566cfbb9',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d',
 'cross_u_candidate_literal_phase_charge_response_v002.py':'887f10ba067e7ed20176e1c9a0fc609ce390947d42ec07fd53c1d31761a96db6',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_candidate_finite_phase_state_update_v001.py':'a23dcf9d462b90877129a8d75da55df3ec7c5df0038c8ccda1a82440450b640b'}
PINS.update({
 'author_fragment_cached_updated_phase_compact_chi_contact_v001.py':'ba1f599b85c367320d601fee9d58ea885c17f08452a7935666472fccc2eafa10',
 'author_fragment_cached_phase_chi_fraction_reference_v001.py':'414ed54d382a1e644a7a8ba9847881d1b53fa2e76d480de7b4c223cf00940b43',
})
COMPONENT_PROTOCOL=('CACHED_UPDATED_PHASE_COMPACT_CHI_CONTACT_V001.md','14f9c9d3a8970bed81bdd771b9ba0c5030c280439a84c9506cf825bc1b567aa3')
JOIN_SOURCE=('cross_u_fixed_geometry_phase_normal_canonical_value_join_v002.py','28e8cb501975c4fd20660ce022a54c0ab9c677dc00108399e76fe023f870755b')
JOIN_RESULT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RESULT.json','d382c372ac74e581beee2a491ae4a143cf24a6c73dd87fd0565044a6041fd9ed','FIXED_GEOMETRY_PHASE_UPDATED_FOUR_NORMAL_CANONICAL_VALUES_MEASURED')
JOIN_RECEIPT=('CROSS_U_FIXED_GEOMETRY_PHASE_NORMAL_CANONICAL_VALUE_JOIN_V002_RECEIPT.json','2f331b3a45b1e5dfe25114ab4d3f0d90528029b9d3d060c2809c1d691f7d31b6','CLOSED')
JOIN_PROOF=('ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_V001.json','3bc8ea72625fbcda04440f9bc80dfde01b1aeb30804a555b84771c2b899651ae','ROOT_NATURAL_CLOSED_FIXED_PHASE_NORMAL_JOIN_SUCCESS_SEALS_VERIFIED')
POINT_CELLS=((42,21),(42,22),(43,21),(43,22))
SHAPES=dict(g=(4,4),hi=(4,4),U=(4,),uc=(4,),P=(4,4),phi=(4,),N=(),mu=(),h=(3,3),beta=(3,),ih=(3,3),u=(3,))
REFERENCE_METADATA=[]
np=P=N=None;SCOPE={};RAW={};AVAILABLE={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DD_ARRAY_CURRENT={}
FLAGS=dict(physical_metric_qualified=False,canonical_currents_restored=False,normal_constraints_qualified=False,initial_CMC_solved=False,phase_charge_restored=False,CMC_preservation_qualified=False,exterior_qualified=False,evolution_qualified=False,galaxy_velocity_qualified=False)

def selected_definitions(file,names):
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 assert {n.name for n in defs}==set(names);return ast.Module(body=defs,type_ignores=[])

def load_io():
 assert hashlib.sha256((BASE/IO_PARENT).read_bytes()).hexdigest()==IO_PARENT_SHA
 for name,h in PINS.items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h,name
 names={'bind','keep','read','arrays','thin','put_pair','capture_families','clear_current','initialize_io','pair_from'}
 exec(compile(selected_definitions(IO_PARENT,names),IO_PARENT,'exec'),globals());initialize_io()
 file='author_fragment_single_decode_recheck_v001.py';exec(compile(selected_definitions(file,{'recheck'}),file,'exec'),SCOPE);P.recheck=SCOPE['recheck'];P.TOL=SCOPE['TOL']

def read_closed(ref,names):
 data=read(ref,names);RAW.clear();return data

def clear_completed():
 context=dict(CONTEXT);clear_current();CONTEXT.update(context)

def seal_completed(role,metadata):
 CONTEXT.update(stage='seal_'+role,role=role)
 record=P.checkpoint(role,arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(metadata,role=role))
 CONTEXT.update(last_completed_role=thin(record));return record

def initialize_helpers():
 global np,N
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 file=list(PINS)[0];names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','scalar_mask','scalar_lift','dd_scalar_scatter'}
 assert len(names)==16;exec(compile(selected_definitions(file,names),file,'exec'),SCOPE)
 for name in names:setattr(P,name,SCOPE[name])
 file=list(PINS)[1];exec(compile(selected_definitions(file,{'normal_keep_pair'}),file,'exec'),SCOPE)
 selections=(('author_fragment_finite_york_geometry_target_v001.py',11,None),('author_fragment_exact_exponent_two_product_v003.py',2,None),('author_fragment_fixed_geometry_phase_normal_join_v001.py',5,{'phase_join_closed','fixed_geometry_phase_normal_join_admission','phase_join_pair','phase_join_add','phase_join_functional'}),('author_fragment_finite_candidate_native_EH_normal_v003.py',1,{'finite_candidate_test_polynomials'}),('cross_u_candidate_literal_phase_charge_response_v002.py',1,{'bind_record'}),('author_fragment_cached_updated_phase_compact_chi_contact_v001.py',10,None),('author_fragment_cached_phase_chi_fraction_reference_v001.py',2,None))
 for file,count,chosen in selections:
  tree=ast.parse((BASE/file).read_text());chosen={n.name for n in tree.body if isinstance(n,ast.FunctionDef)} if chosen is None else chosen;assert len(chosen)==count,file
  if file in ('author_fragment_fixed_geometry_phase_normal_join_v001.py','author_fragment_cached_updated_phase_compact_chi_contact_v001.py','author_fragment_cached_phase_chi_fraction_reference_v001.py'):
   for node in tree.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
     if isinstance(node.value,ast.Call):
      assert node.targets[0].id=='NORMAL_NAMES' and isinstance(node.value.func,ast.Name) and node.value.func.id=='dict' and not node.value.args and all(q.arg is not None for q in node.value.keywords)
      globals()[node.targets[0].id]={q.arg:ast.literal_eval(q.value) for q in node.value.keywords}
     else:globals()[node.targets[0].id]=ast.literal_eval(node.value)
  exec(compile(selected_definitions(file,chosen),file,'exec'),globals())
 globals().update(PHASE_NORMAL_JOIN_AUTHOR_DRAFT=False,CACHED_UPDATED_PHASE_CHI_AUTHOR_DRAFT=False,CHI_FRACTION_REFERENCE_AUTHOR_DRAFT=False)
 install_exact_exponent_product(SCOPE,P,keep,'NEW_cached_chi_exact_exponent_product')
 normal={'normal_test_mask','extend_normal_tests','restrict_normal_rows','normal_hat_jet','normal_hat_operation_envelope','scatter_normal_envelope','paired_restrict_normal_rows','paired_scatter_normal'};normal_scope=dict(SCOPE);file=list(PINS)[2]
 assert len(normal)==8;exec(compile(selected_definitions(file,normal),file,'exec'),normal_scope);N=types.SimpleNamespace(**{n:normal_scope[n] for n in normal})

def cached_chi_admission():
 refs=fixed_geometry_phase_normal_join_admission();joined,jrc=phase_join_closed(JOIN_SOURCE,JOIN_RESULT,JOIN_RECEIPT,JOIN_PROOF);jc=joined['case']
 assert jc['normal_terminal']==json.loads(json.dumps(refs['normal_terminal'])) and jc['finite_phase_terminal']==json.loads(json.dumps(refs['finite_terminal']))
 assert jc['original_input']==thin(refs['input']) and jc['original_basis']==thin(refs['basis']) and jc['old_loads']==thin(refs['loads'])
 assert jc['all_four_phase_normal_value_rows_recomputed'] is jc['mechanical_current_CMC_and_test_R_Z_t_words_copied_by_action_invariance'] is jc['original_targets_and_epsilon_unchanged'] is True
 assert jc['new_compact_chi_or_configuration_JVP'] is jc['physical_adoption'] is jc['canonical_normal_CMC_or_physical_admission'] is False and len(jc['columns'])==4 and len(jc['normal_rows'])==16
 for iq,source in enumerate(refs['columns']):
  om=source['old']['metadata'];assert om['direction']=='true_conformal_scalar_hat43_22_at_reference_mechanical_rates_fixed' and om['geometry_reference_rho']==0. and om['phase_charge_direction_restored'] is False
  source['joined']=bind_record(jc['columns'][iq]);m=source['joined']['metadata'];assert m['column']==iq and m['old_column']==thin(source['old']) and m['state']==thin(source['state']) and m['finite_phase_column']==thin(source['new'])
  source['joined_rows']=[bind_record(q) for q in jc['normal_rows'][4*iq:4*iq+4]]
  for row,q in enumerate(source['joined_rows']):
   m=q['metadata'];assert (m['column'],m['row'],m['jet'])==(iq,row,0) and m['old_normal_test']==thin(source['phase_rows'][row]) and m['state']==thin(source['state']) and m['finite_phase_column']==thin(source['new']) and m['delta_EOS_used'] is m['new_configuration_contact'] is False
   assert q in joined['checkpoints'] and q['metadata']['owner']==joined['owner'] and q['metadata']['failed'] is False
   for name in cached_updated_phase_contact_names('NEW_phase_normal_join_column%d_row%d_NEW_literal_phase_'%(iq,row),True):assert name in q['metadata']['schema'],name
  for q in [source['joined']]+source['joined_rows']:assert jrc['output_sha256'][q['file']]==q['sha256'] and jrc['output_sha256'][q['commit_file']]==q['commit_sha256']
  for name in cached_updated_phase_contact_names('NEW_finite_phase_column%d_NEW_invariant_'%iq):assert name in source['new']['metadata']['schema'],name
  for n in SHAPES:
   root='completed_contact_'+('d_' if n in ('g','hi','U','uc','P','phi') else 'dc_')+n
   for w in ('hi','lo'):assert source['state']['metadata']['schema'][root+'_'+w]['shape']==[3784]+list(SHAPES[n])
 refs.update(join_terminal=(JOIN_SOURCE,JOIN_RESULT,JOIN_RECEIPT,JOIN_PROOF),joined_readout=bind_record(jc['readout']));return refs

def hydrate_chi_column(source,iq):
 names={n:'completed_candidate_'+('s_' if n in ('g','hi','U','uc','P','phi') else 'c_')+('sqrt_h' if n=='mu' else n) for n in SHAPES}
 dnames={n:'completed_contact_'+('d_' if n in ('g','hi','U','uc','P','phi') else 'dc_')+n for n in SHAPES}
 wanted=tuple(names.values())+tuple(n+'_'+w for n in dnames.values() for w in ('hi','lo'))+('predeclared_true_conformal_chi','predeclared_true_conformal_gradient')
 raw=read_closed(source['state'],wanted);values={};direction={}
 for n,name in names.items():
  a=keep('column%d_closed_raw_'%iq+n,raw[name].copy());assert a.shape==(3784,)+SHAPES[n] and a.dtype==np.float64;values[n]=P.a_dd(a)
  direction[n]=cached_phase_pair(raw,dnames[n],a.shape,keep,'column%d_original_chi_'%iq+n)
 for n in ('N','beta','u','phi'):assert all(np.all(a==0) for a in direction[n])
 index=np.asarray([44*i+j for i,j in POINT_CELLS],dtype=np.int64);off=np.ones(3784,dtype=bool);off[index]=False
 for n in SHAPES:assert all(np.all(a[off]==0) for a in direction[n]),'Original compact direction must have exactly its declared four-cell support'
 for n in ('predeclared_true_conformal_chi','predeclared_true_conformal_gradient'):keep('column%d_unchanged_'%iq+n,raw[n].copy());assert np.all(raw[n][off]==0)
 prefix='NEW_finite_phase_column%d_'%iq;wanted=cached_updated_phase_contact_names(prefix+'NEW_invariant_')+tuple(prefix+'phase_covector_'+n+'_'+w for n in ('before','increment','updated') for w in ('hi','lo'))
 finite=read_closed(source['new'],wanted);before=cached_phase_pair(finite,prefix+'phase_covector_before',(3784,4),keep,'column%d_phase_before'%iq);step=cached_phase_pair(finite,prefix+'phase_covector_increment',(3784,4),keep,'column%d_phase_step'%iq);updated=cached_phase_pair(finite,prefix+'phase_covector_updated',(3784,4),keep,'column%d_phase_updated'%iq)
 assert all(np.array_equal(a,b) for a,b in zip(before,values['phi'])) and all(np.all(a[:,1:]==0) for a in step) and all(np.array_equal(a[:,1:],b[:,1:]) for a,b in zip(before,updated));values['phi']=updated
 s={n:values[n] for n in ('g','hi','U','uc','P','phi')};c={n:values[n] for n in ('N','mu','h','beta','ih','u')}
 fixed=REFS['input']['metadata']['refs']['fixed'];assert fixed['eps']==1e-5 and fixed['Q0_over_Hstar']==100
 norm=cached_phase_pair(finite,prefix+'NEW_invariant_pressure_norm_value_denominator',(3784,),keep,'column%d_copied_registered_norm'%iq);X0=cached_phase_pair(finite,prefix+'NEW_invariant_q_value_denominator',(3784,),keep,'column%d_copied_registered_X0'%iq)
 for a in (norm,X0):assert np.all(a[1]==0) and np.all(a[0]==a[0][0])
 eta=fixed['Hunit']/299792458.;fac=2*eta*eta/1.98;Abar=1.5*fixed['OA']/fixed['rG'];A0=fac*Abar;assert X0[0][0]==100*eta
 constants=dict(eps=1e-5,norm=float(norm[0][0]),X0=float(X0[0][0]),A0=A0,C=1.98,eta=eta,synthetic_control=False,Hunit=fixed['Hunit'],OA=fixed['OA'],rG=fixed['rG'],relative_phase_coefficient=1.,physical_constants_selected_or_fitted=False)
 prepared=prepare_cached_updated_phase_contact(finite,prefix+'NEW_invariant_',s,c,constants,source['new']['metadata']['candidate_provenance'],keep,'column%d_cached_EOS'%iq)
 rows=[];caches=[]
 for row,ref in enumerate(source['joined_rows']):
  rp='NEW_phase_normal_join_column%d_row%d_NEW_literal_phase_'%(iq,row);data=read_closed(ref,cached_updated_phase_contact_names(rp,True));rows.append((rp,data));caches.append({n:pair_from(data,rp+NORMAL_NAMES[n]) for n in NORMAL_FIELDS})
 return prepared,direction,rows,caches,index

def reference_items(reference):
 out={n:q for n,q in reference['eos'].items()}
 for n,group in reference['chain'].items():
  for k,q in group.items():out[n+'_chain_'+k]=q
 for row,group in enumerate(reference['normals']):
  for n,q in group.items():out['row%d_'%row+n]=q
 return out

def rational_control(name,actual,targets):
 shape=actual[0].shape;eh=np.empty(shape);el=np.empty(shape);error=np.empty(shape);envelope=np.empty(shape);entries=[]
 def flatten(tree):
  if isinstance(tree,list):return [x for q in tree for x in flatten(q)]
  return [tree]
 for ordinal,q in enumerate([x for target in targets for x in flatten(target)]):
  key=np.unravel_index(ordinal,shape);value,bound=q[1],q[2];assert isinstance(value,Fraction) and isinstance(bound,Fraction)
  h=float(value);l=float(value-Fraction.from_float(h));remainder=value-Fraction.from_float(h)-Fraction.from_float(l);observed=Fraction.from_float(float(actual[0][key]))+Fraction.from_float(float(actual[1][key]));difference=abs(observed-value)
  eh[key]=h;el[key]=l;error[key]=0. if difference==0 else math.nextafter(float(difference),math.inf);envelope[key]=0. if bound==0 else math.nextafter(float(bound),math.inf)
  entries.append(dict(index=list(key),numerator=str(value.numerator),denominator=str(value.denominator),conversion_remainder_numerator=str(remainder.numerator),conversion_remainder_denominator=str(remainder.denominator),bound_numerator=str(bound.numerator),bound_denominator=str(bound.denominator),actual_error_numerator=str(difference.numerator),actual_error_denominator=str(difference.denominator)))
  CONTEXT['rational_reference_partial']=dict(name=name,entries=entries.copy())
 fy_keep(name+'_exact_Fraction_converted_target',(eh,el),keep);fy_keep(name+'_actual_selected_words',actual,keep);keep(name+'_exact_rational_error',error);keep(name+'_positive_rational_bound',envelope)
 REFERENCE_METADATA.append(dict(name=name,entries=entries));P.check(name,error,np.zeros(shape),envelope)


def scalar_contact_functional(point,weak,epoint,basis,sv,keep,label):
 test=np.zeros((87,45));test[43,22]=1.;left=test!=0;selected=(sv[0]!=0)|(sv[1]!=0);nodal=P.a_dd(np.zeros((87,45)));direct=P.a_dd(np.zeros(15136))
 fy_keep(label+'_selected_weak',(weak[0][left],weak[1][left]),keep);fy_keep(label+'_selected_point',(point[0][selected],point[1][selected]),keep);fy_keep(label+'_selected_polynomial',(sv[0][selected],sv[1][selected]),keep)
 a=P.a_mul64(test[left],(weak[0][left],weak[1][left]));b=P.a_mul((sv[0][selected],sv[1][selected]),(point[0][selected],point[1][selected]))
 for word in (0,1):nodal[word][left]=a[word];direct[word][selected]=b[word]
 nv=fy_sum(fy_sum(nodal,1),0);dv=fy_sum(P.a_mul64((basis['dv']/basis['R']).reshape(15136),direct),0);gap=P.a_sub(nv,dv)
 bound=2*np.sum((basis['dv']/basis['R']).reshape(15136)*(abs(sv[0])+abs(sv[1]))*epoint)
 for n,q in (('nodal',nv),('direct',dv),('gap',gap)):fy_keep(label+'_'+n,q,keep)
 keep(label+'_uncancelled_positive_bound',np.asarray(bound));P.check(label,(gap[0]+gap[1]).copy(),np.asarray(0.),np.asarray(bound));return dict(nodal=nv,direct=dv,gap=gap)


def cached_chi_packet(refs):
 global REFS
 REFS=refs;basis=read_closed(refs['basis'],('R','dv','hats','cell_i','cell_j'));assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44)
 assert np.all(basis['R']>0) and np.all(basis['dv']>0) and np.array_equal(basis['cell_i'],np.repeat(np.arange(86),44)) and np.array_equal(basis['cell_j'],np.tile(np.arange(44),86))
 for n,a in basis.items():keep('closed_original_basis_'+n,a.copy())
 header=seal_completed('CACHED_CHI_INPUT',dict(kind='closed_updated_phase_original_compact_chi_sources',normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],original_input=thin(refs['input']),basis=thin(refs['basis']),columns=[dict(state=thin(q['state']),old=thin(q['old']),finite=thin(q['new']),joined=thin(q['joined']),joined_rows=[thin(v) for v in q['joined_rows']]) for q in refs['columns']],four_point_control_cells=[list(q) for q in POINT_CELLS],chi_node=[43,22],all_primitive_targets_held=True,EOS_primal_or_log_replayed=False,physical_adoption=False));clear_completed()
 columns=[];coefficients=[];increments=[];bounds=[];point_p=[];point_eH=[];point_ep=[]
 for iq,source in enumerate(refs['columns']):
  CONTEXT.update(column=iq,stage='hydrate_closed_values_and_original_chi_contact');prepared,direction,rows,caches,index=hydrate_chi_column(source,iq)
  f=(1.,0.,0.,0.);b=((0.,0.,0.),(1.,0.,0.),(0.,1.,0.),(0.,0.,1.));references=[reference_items(chi_cached_contact_reference(prepared,direction,caches,f,b,point=int(i),bounds=False)) for i in index] if iq==0 else None
  unsigned=chi_cached_contact_reference(prepared,direction,caches,f,b,bounds=True,keep=keep,label='column%d_NEW_unsigned_chi'%iq);envelope={n:np.asarray(q[2]).copy() for n,q in unsigned['eos'].items() if not isinstance(q,list)}
  eos=cached_updated_phase_eos_compact_chi(prepared,direction,keep,'column%d_NEW_cached_chi_EOS'%iq)
  for n,q in eos['delta'].items():fy_keep('column%d_NEW_chi_EOS_delta_'%iq+n,q,keep)
  for n,a in envelope.items():keep('column%d_NEW_chi_EOS_positive_'%iq+n,a)
  if iq==0:
   for n,q in eos['delta'].items():rational_control('four_point_cached_EOS_'+n,(q[0][index],q[1][index]),[qref[n] for qref in references])
   for n,actual in eos['chain_gaps'].items():
    for kind,q in (('actual',eos['delta'][{'P':'pressure','PX':'PX','PXX':'PXX'}[n]]),('expected',P.a_mul(prepared['values'][{'P':'PX','PX':'PXX','PXX':'PXXX'}[n]],eos['delta']['X'])),('gap',actual)):
     rational_control('four_point_'+n+'_chain_'+kind,(q[0][index],q[1][index]),[qref[n+'_chain_'+kind] for qref in references])
  eosref=seal_completed('EOS_CHI_CONTACT',dict(kind='NEW_cached_updated_phase_EOS_current_H_original_chi_contact',column=iq,input=thin(header),state=thin(source['state']),finite_phase_column=thin(source['new']),original_geometry_direction='true_conformal_scalar_hat43_22_at_reference_mechanical_rates_fixed',EOS_values_and_logs_recomputed=False,old_temporal_delta_reused=False,stage_vs_analytic_chain_gaps_retained=True,four_point_Fraction_targets=REFERENCE_METADATA.copy() if iq==0 else [],physical_adoption=False));clear_completed()
  saved=read_closed(source['old'],tuple(n+'_'+w for n in ('delta_normal_coefficients','delta_initial_CMC_density','NEW_delta_momentum_native_density','NEW_delta_momentum_metric_native_density','NEW_delta_momentum_metric_EH_density','NEW_delta_momentum_metric_total_density','NEW_delta_momentum_K','NEW_delta_momentum_Ktrace') for w in ('hi','lo')));old=phase_join_pair(saved,'delta_normal_coefficients',(3784,4,4),keep,'column%d_unchanged_mechanical_chi_coefficients'%iq)
  out=tuple(a.copy() for a in old);inc=P.a_dd(np.zeros((3784,4,3)));bound=np.zeros((3784,4,3));rowrefs=[]
  for row,(rp,data) in enumerate(rows):
   CONTEXT.update(column=iq,row=row,jet=0,stage='NEW_cached_phase_chi_normal_contact');fr=np.full(3784,f[row]);br=np.tile(np.asarray(b[row]),(3784,1));normal=cached_updated_phase_normal_compact_chi(data,rp,prepared['s'],prepared['c'],direction,eos,fr,br,dict(closed_new_phase_row=thin(source['joined_rows'][row]),original_chi_state=thin(source['state'])),keep,'column%d_row%d_NEW_cached_chi_phase_normal'%(iq,row))
   if iq==0:
    for n,q in normal['delta'].items():rational_control('four_point_row%d_'%row+n,(q[0][index],q[1][index]),[qref['row%d_'%row+n] for qref in references])
   names=('row%d_jet0_phase_action_coefficient_delta'%row,'completed_row%d_jet0_native_EH_delta_action'%row,'row%d_jet0_total_once_counted_ordinary_Hamiltonian_delta'%row,'completed_row%d_jet0_total_delta_hamiltonian'%row)
   oldrow=read_closed(source['phase_rows'][row],tuple(n+'_'+w for n in names for w in ('hi','lo')));oldphase,native,ordinary,total=[phase_join_pair(oldrow,n,(3784,),keep,'column%d_row%d_unchanged_'%(iq,row)+n) for n in names];assert all(np.array_equal(a,b[:,row,0]) for a,b in zip(total,old))
   replacement=P.a_sub(oldphase,normal['delta']['action']);new=phase_join_add(total,replacement,keep,'column%d_row%d_chi_total_join'%(iq,row));reconstruction=P.a_sub(P.a_add(tuple(-a for a in native),ordinary),normal['delta']['action'])
   fy_keep('column%d_row%d_new_joined_minus_source_terms'%(iq,row),P.a_sub(new,reconstruction),keep);fy_keep('column%d_row%d_NEW_chi_normal_replacement'%(iq,row),replacement,keep)
   for word in (0,1):out[word][:,row,0]=new[word];inc[word][:,row,0]=replacement[word]
   en=np.asarray(unsigned['normals'][row]['action'][2]);assert np.all(en>=0) and np.all(np.isfinite(en));bound[:,row,0]=abs(oldphase[0])+abs(oldphase[1])+en
   keep('column%d_row%d_unsigned_NEW_action_contact'%(iq,row),en);keep('column%d_row%d_uncancelled_old_plus_NEW_contact'%(iq,row),bound[:,row,0].copy());fy_keep('column%d_completed_new_chi_coefficients'%iq,out,keep);fy_keep('column%d_completed_new_chi_replacement'%iq,inc,keep)
   q=seal_completed('PHASE_CHI_NORMAL_ROW',dict(kind='NEW_cached_phase_original_chi_all_four_normal_value_test_contact',column=iq,row=row,jet=0,input=thin(header),eos_contact=thin(eosref),closed_new_phase_row=thin(source['joined_rows'][row]),old_chi_phase_row=thin(source['phase_rows'][row]),state=thin(source['state']),relative_phase_count=1,ordinary_mean_count=1,test_R_Z_t_phase_contact_zero_by_action=True,unchanged_native_EH_ordinary_copied_by_phi_only_action_invariance=True,four_point_Fraction_targets=[q for q in REFERENCE_METADATA if q['name'].startswith('four_point_row%d_'%row)] if iq==0 else [],physical_adoption=False));rowrefs.append(thin(q));clear_completed()
  assert all(np.array_equal(a[:,:,1:],b[:,:,1:]) for a,b in zip(out,old))
  for n,a in saved.items():keep('column%d_action_invariant_copied_'%iq+n,a.copy())
  value=read_closed(source['joined'],('NEW_phase_normal_join_column%d_NEW_normal_coefficients_hi'%iq,'NEW_phase_normal_join_column%d_NEW_normal_coefficients_lo'%iq))
  for n,a in value.items():keep('column%d_updated_phase_value_normal_copied_'%iq+n,a.copy())
  fy_keep('column%d_NEW_updated_phase_chi_normal_coefficients'%iq,out,keep);fy_keep('column%d_NEW_phase_chi_replacement'%iq,inc,keep);keep('column%d_uncancelled_phase_chi_replacement'%iq,bound.copy())
  for n in ('p','H'):fy_keep('column%d_NEW_cached_chi_'%iq+n,eos['delta'][n],keep);keep('column%d_NEW_cached_chi_positive_'%iq+n,envelope[n])
  for n,q in eos['chain_gaps'].items():fy_keep('column%d_NEW_stage_minus_analytic_'%iq+n,q,keep)
  rec=seal_completed('CHI_COLUMN',dict(kind='NEW_updated_phase_original_compact_chi_contact_and_invariant_components',column=iq,input=thin(header),eos_contact=thin(eosref),normal_contacts=rowrefs,state=thin(source['state']),old_column=thin(source['old']),closed_value_column=thin(source['joined']),normal_coordinate_order=['value','R','Z','t'],mechanical_CMC_and_test_gradient_contacts_bitwise_unchanged=True,new_phase_delta_is_chi_not_temporal_step=True,original_primitive_targets_unchanged=True,physical_adoption=False));columns.append(thin(rec));coefficients.append(out);increments.append(inc);bounds.append(bound);point_p.append(eos['delta']['p']);point_ep.append(envelope['p']);point_eH.append(eos['delta']['H']);clear_completed()
 point=P.a_reshape(P.a_stack(increments,0),(15136,4,3));epoint=np.concatenate(bounds);replacement_weak=N.paired_scatter_normal(point,basis,'NEW_chi_phase_replacement');fy_keep('NEW_chi_phase_replacement_weak',replacement_weak,keep)
 names=tuple(n for n in refs['loads']['metadata']['schema'] if n.startswith(('prior_signed_bridge_','prior_phase_current_')))+tuple(n+'_'+w for n in ('delta_native_current','delta_metric_current','delta_initial_weak_CMC','delta_total_weak_normal','candidate_global_delta_current_point_Hamiltonian_normal','candidate_global_delta_current_time_primary_action_coefficients') for w in ('hi','lo'));loads=read_closed(refs['loads'],names)
 for n,a in loads.items():keep('closed_action_invariant_load_'+n,a.copy())
 oldweak=phase_join_pair(loads,'delta_total_weak_normal',(4,87,45),keep,'old_chi_normal_weak');newweak=phase_join_add(oldweak,replacement_weak,keep,'NEW_updated_phase_chi_weak_normal');oldpoint=phase_join_pair(loads,'candidate_global_delta_current_point_Hamiltonian_normal',(15136,4,3),keep,'old_chi_normal_point');newpoint=P.a_reshape(P.a_stack([P.a_slice(a,(slice(None),slice(None),slice(0,3))) for a in coefficients],0),(15136,4,3));fy_keep('NEW_updated_phase_chi_normal_point',newpoint,keep);fy_keep('NEW_chi_point_assembly_gap',P.a_sub(newpoint,P.a_add(oldpoint,point)),keep)
 sheet=read_closed(refs['sheet'],('sheet_delta_weak_normal_hi','sheet_delta_weak_normal_lo'));sheetpair=phase_join_pair(sheet,'sheet_delta_weak_normal',(4,87,45),keep,'unchanged_off_sheet_chi_delta');assert all(np.all(a==0) for a in sheetpair)
 normaltest=np.zeros((4,87,45));normaltest[:,43,22]=(1.,2.,3.,4.);scalartest=np.zeros((87,45));scalartest[43,22]=1.;tv,sv=finite_candidate_test_polynomials(normaltest,scalartest,basis,keep,'NEW_chi_independent_fixed_basis_polynomials')
 functional=phase_join_functional(newpoint,newweak,sheetpair,basis,normaltest,tv,abs(oldpoint[0])+abs(oldpoint[1])+epoint,keep,P.check,'NEW_updated_phase_chi_normal_functional')
 p=P.a_reshape(P.a_stack(point_p,0),(15136,));H=P.a_reshape(P.a_stack(point_eH,0),(15136,));ep=np.concatenate(point_ep);weakp=P.dd_scalar_scatter(p,basis,keep,'NEW_updated_phase_chi_literal_current');fy_keep('NEW_updated_phase_chi_literal_point_current',p,keep);fy_keep('NEW_updated_phase_chi_literal_H_contact',H,keep);fy_keep('NEW_updated_phase_chi_literal_weak_current',weakp,keep)
 scalar=scalar_contact_functional(p,weakp,ep,basis,sv,keep,'NEW_updated_phase_chi_literal_current_functional');keep('NEW_chi_positive_point_current',ep)
 record=seal_completed('CHI_READOUT',dict(kind='NEW_updated_phase_original_compact_chi_normal_and_literal_current_contact',input=thin(header),columns=columns,closed_normal_loads=thin(refs['loads']),closed_joined_values=thin(refs['joined_readout']),fixed_literal_target=thin(refs['prior']),all_original_canonical_and_phase_targets_held=True,new_phase_mass_H_requires_updated13764_cache=True,geometry_response_or_physical_admission=False,point_direction_count=1,physical_adoption=False));clear_completed()
 expected=['CACHED_CHI_INPUT']+(['EOS_CHI_CONTACT']+['PHASE_CHI_NORMAL_ROW']*4+['CHI_COLUMN'])*4+['CHI_READOUT'];assert len(RECORDS)==26 and [q['metadata']['role'] for q in RECORDS]==expected
 assert len(CHECKS)==48 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
 return dict(status='CACHED_UPDATED_PHASE_ORIGINAL_COMPACT_CHI_CONTACT_MEASURED',input=thin(header),columns=columns,readout=thin(record),normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],point_control_cells=[list(q) for q in POINT_CELLS],controls=48,roles=26,new_EOS_values_or_logs=False,old_temporal_direction_reused=False,original_targets_or_epsilon_refitted=False,full_geometry_Jacobian_or_physical_admission=False,physical_adoption=False)


def main():
 assert AUTHOR_DRAFT is False and AUTHORING_IN_PROGRESS is False and PROTOCOL_SHA is not None,'Root reviewed guard/protocol release required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive unused namespace required'
 load_io();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(IO_PARENT,IO_PARENT_SHA);bind(DRIVER_PROTOCOL,PROTOCOL_SHA);bind(*COMPONENT_PROTOCOL)
  for name,h in PINS.items():bind(name,h)
  initialize_helpers();refs=cached_chi_admission()
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,normal_terminal=refs['normal_terminal'],finite_terminal=refs['finite_terminal'],join_terminal=refs['join_terminal'],original_input=thin(refs['input']),basis=thin(refs['basis']),controls=48,roles=26,point_control_cells=[list(q) for q in POINT_CELLS],chi_node=[43,22],EOS_values_or_logs_replayed=False,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):case=cached_chi_packet(refs)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status=case['status'],case=case,controls=CHECKS,checkpoints=RECORDS,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(case['status'],len(CHECKS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=None;close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**AVAILABLE,**RAW,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(kind='available_unfinished_NEW_cached_updated_phase_chi_contact',context=dict(CONTEXT)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
