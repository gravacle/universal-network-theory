"""HELD selective recovery of CLOSED30246; no completed calculation replay.
The first NEW weak column resumes at V from saved lifts/jets/nu/nz/q. Original
18 factor/fixture controls and12success roles retain their original owner.
Root alone binds the failure proof/releases/executes. No law/gate change.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_RECOVERY_V001'
DRIVER_PROTOCOL='CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_RECOVERY_V001.md'
PROTOCOL_SHA='e362ca8ab2636532ad5b490fe38624de11fceda40f34db6995b13127e320f4a1'
FAILED_SOURCE=('candidate_directed_nodal_factor_apply_controls_v003.py','e66d3b74bc5b24e3cba59eb56df10813360124dc38edc2d0dfe27641bcdf9044')
FAILED_ERROR=('CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_CONTROLS_V003_ERROR.json','d026f3cbb408c83d602c34a0e2c688e9d10e3a837e2a0ea2238c1558d862cd46')
FAILED_RECEIPT=('CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_CONTROLS_V003_RECEIPT.json','15ef9e35920fce3ccefa2721e4791b6dd5720204e38a2e873c946ac8e033d9bc')
FAILED_PROOF=(None,None,'ROOT_NATURAL_CLOSED_FACTOR_APPLY_PARTIAL_SUCCESS_AND_ERROR_SEALS_VERIFIED')
np=P=None;SCOPE={};RAW={};AVAILABLE={};DD_ARRAY_CURRENT={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DESCRIPTIONS={}
FLAGS=dict(represented_factor_or_adjoint_admitted=False,old_componentwise_inverse_failure_repaired=False,full_weak_inverse_qualified=False,global_rank_earned=False,canonical_currents_restored=False,physical_adoption=False)
FACTOR_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
FACTOR_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
FACTOR_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
FACTOR_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py', '489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json', '49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e', 'COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json', 'c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64', 'CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json', '2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9', 'ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py': '5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18', 'cross_u_paired_current_primitive_momentum_readout_v002.py': 'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19', 'author_fragment_exact_exponent_two_product_v003.py': 'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235', 'author_fragment_finite_york_geometry_target_v001.py': '12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70', 'author_fragment_compact_metric_contact_momenta_v002.py': 'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd', 'author_fragment_candidate_specialized_temporal_action_v001.py': 'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc', 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py': 'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db', 'author_fragment_candidate_directed_nodal_factor_apply_v001.py': '4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b', 'author_fragment_candidate_chunk_point_block_provider_v001.py': '4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625', 'author_fragment_single_decode_recheck_v001.py': 'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d'}
DECLARED_NODES=((43, 22), (43, 0), (86, 22), (43, 44))

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h;INPUTS[str(P.path(n).resolve())]=h

def keep(n,x):
 a=np.asarray(x).copy();AVAILABLE[n]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),n;return a

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def clear():RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear();DESCRIPTIONS.clear()

def seal(role,metadata):
 q=P.checkpoint(role,{n:np.asarray(a).copy() for n,a in {**RAW,**AVAILABLE}.items()},dict(metadata,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)));clear();return q

def initialize():
 global np,P,SCOPE
 for file,h in PINS.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 n=list(PINS)[1];assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==PINS[n]
 io={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'};tree=ast.parse((BASE/n).read_text());defs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in io];assert len(defs)==13
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 exec(compile(ast.Module(body=defs,type_ignores=[]),n,'exec'),SCOPE);P=types.SimpleNamespace(**{k:SCOPE[k] for k in io})
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep,B=1.0059833281731022e-10*3.085677581491367e19/299792458.**2,GC=3*math.pi/8,C=1.98,ALPHA=.02/1.98,ELL=.1)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_native_node_value','dd_metric_node_value','metric_R_matrix'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','native_mask','metric_mask','lift_velocity','lift_metric','dd_metric_F','dd_native_scatter','dd_metric_scatter','scalar_mask','pack_fields','unpack_fields'}
 for file,wanted in ((list(PINS)[0],base),(list(PINS)[1],primitive)):
  tree=ast.parse((BASE/file).read_text());defs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in wanted];assert len(defs)==len(wanted);exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),SCOPE)
 for n in base|primitive|{'B','GC','C','ALPHA','ELL'}:setattr(P,n,SCOPE[n])
 P.TOL=2e-11;compact={'compact_contact_swap','compact_momentum_matvec','compact_contact_left','compact_contact_right','compact_contact_outer','compact_contact_reduce'};provider={'candidate_point_provider_admission','candidate_point_cache_names','candidate_point_canonical_envelopes'}
 for file,count,chosen in ((list(PINS)[2],2,None),(list(PINS)[3],11,None),(list(PINS)[4],6,compact),(list(PINS)[5],6,None),(list(PINS)[6],3,None),(list(PINS)[7],9,None),(list(PINS)[8],3,provider)):
  tree=ast.parse((BASE/file).read_text());defs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and (chosen is None or x.name in chosen)];assert len(defs)==count;exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 for node in ast.parse((BASE/list(PINS)[8]).read_text()).body:
  if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id.startswith('POINT_'):globals()[node.targets[0].id]=ast.literal_eval(node.value)
 globals()['POINT_PROVIDER_AUTHOR_DRAFT']=False;globals()['POINT_PROVIDER_AUTHORING_IN_PROGRESS']=False
 tree=ast.parse((BASE/list(PINS)[9]).read_text());defs=[x for x in tree.body if isinstance(x,ast.FunctionDef)];assert len(defs)==1;exec(compile(ast.Module(body=defs,type_ignores=[]),list(PINS)[9],'exec'),SCOPE);P.recheck=SCOPE['recheck']
 install_exact_exponent_product(SCOPE,P,keep,'NEW_apply_exact_product')

def exact(a):return Fraction.from_float(float(a))

def rat(a):return dict(numerator_hex=hex(a.numerator),denominator_hex=hex(a.denominator))

def value(pair,index):return exact(pair[0][index])+exact(pair[1][index])

def scalar_contact(actual,expected,envelope,label):
 bound=abs(expected)+envelope;gap=actual-expected;ratio=abs(gap)/bound if bound else Fraction(0);words=[]
 for name,t in (('actual',actual),('expected',expected)):
  DESCRIPTIONS[label+'_'+name]=dict(value=rat(t));h=float(t);l=float(t-exact(h));words.append([h,l]);DESCRIPTIONS[label+'_'+name]['conversion_remainder']=rat(t-exact(h)-exact(l))
 DESCRIPTIONS[label+'_exact_difference']=dict(gap=rat(gap),uncancelled_envelope=rat(envelope),ratio=rat(ratio));keep(label+'_scalar_words_with_remainders_declared',np.array(words));r=float(ratio);r=np.nextafter(r,np.inf) if exact(r)<ratio else r;keep(label+'_upward_exact_ratio',np.array([r]))
 assert bound or actual==expected==0,'Zero envelope requires exact zero scalar identity'
 P.check(label,np.array([r]),np.zeros(1),np.ones(1));assert ratio<=Fraction.from_float(2e-11)

def independent_weak_contact(result,basis,test_native,test_metric,label):
 pn=result['point']['native'];pm=result['point']['metric'];wn=result['weak']['native'];wm=result['weak']['metric'];nodal=[Fraction(0),Fraction(0)];direct=[Fraction(0),Fraction(0)];envelope=[Fraction(0),Fraction(0)];terms=[]
 for n,weak,test in ((0,wn,test_native),(1,wm,test_metric)):
  mask=(test[0]!=0)|(test[1]!=0)
  for index in zip(*np.nonzero(mask)):
   product=value(weak,index)*value(test,index);nodal[n]+=product;envelope[n]+=abs(product)
 F=P.dd_metric_F(basis['R'])
 for iq in range(4):
  for p in range(3784):
   i,j=int(basis['cell_i'][p]),int(basis['cell_j'][p]);r=basis['R'][iq,p];weight=exact(float(basis['dv'][iq,p]/r));tn=[[Fraction(0)]*3 for _ in range(33)];tm=[Fraction(0)]*6
   for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
    ni,nj=i+di,j+dj;hat=basis['hats'][iq,corner,0].reshape(3784)[p]
    for component in range(3):
     independent_i=1 if ni==0 and component in (1,2) else ni;factor=exact(float(hat*(np.asarray(r)**2))) if component==2 else exact(hat)
     if ni==0 and component==0 or nj==0 and component==1:continue
     for mode in range(33):tn[mode][component]+=factor*value(test_native,(mode,component,independent_i,nj))
    for slot in range(6):
     independent_i=1 if ni==0 else ni
     if nj==0 and slot in (3,4):continue
     coefficient=value(test_metric,(slot,independent_i,nj))
     for physical in range(6):tm[physical]+=exact(F[iq,p,physical,slot])*exact(hat)*coefficient
   if not any(any(row) for row in tn) and not any(tm):continue
   idx=iq*3784+p;local=[Fraction(0),Fraction(0)];absolute=[Fraction(0),Fraction(0)]
   for mode in range(33):
    for component in range(3):
     product=weight*tn[mode][component]*value(pn,(idx,3*mode+component));local[0]+=product;absolute[0]+=abs(product)
   for physical in range(6):
    product=weight*tm[physical]*value(pm,(idx,physical));local[1]+=product;absolute[1]+=abs(product)
   for n in (0,1):direct[n]+=local[n];envelope[n]+=absolute[n]
   terms.append(dict(column=iq,point=p,native=rat(local[0]),metric=rat(local[1]),absolute_native=rat(absolute[0]),absolute_metric=rat(absolute[1])));DESCRIPTIONS[label+'_separate_E_F_weight_hat_polynomial_terms']=terms.copy()
 for n,name in enumerate(('native','metric')):scalar_contact(nodal[n],direct[n],envelope[n],label+'_'+name+'_polynomial_transpose')

def initialize_recovery():
 initialize()
 # Compact six functions were compiled in caller globals; alias the SAME repaired scope.
 globals().update({n:SCOPE[n] for n in ('a_dd','a_slice','a_add','a_mul','a_stack','normal_pair_sum')})
 file='author_fragment_candidate_specialized_temporal_action_v001.py';tree=ast.parse((BASE/file).read_text());old=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='candidate_temporal_canonical')
 start=next(i for i,n in enumerate(old.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='nu' for t in n.targets))
 tail=next(i for i,n in enumerate(old.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='V' for t in n.targets))
 head=ast.parse("nu,nz,q=(saved[n] for n in ('nu','nz','q'))\nput('nu',nu);put('nz',nz);put('q',q)").body
 args=ast.parse('def recovered_canonical_after_q(cache,jets,saved,keep,label): pass').body[0].args
 resumed=ast.FunctionDef(name='recovered_canonical_after_q',args=args,body=old.body[:start]+head+old.body[tail:],decorator_list=[])
 assert [ast.dump(n,include_attributes=False) for n in resumed.body[-len(old.body[tail:]):]]==[ast.dump(n,include_attributes=False) for n in old.body[tail:]]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[resumed],type_ignores=[])),file+'_unearned_tail','exec'),globals())
 file='author_fragment_candidate_specialized_weak_mechanical_action_v002.py';tree=ast.parse((BASE/file).read_text());old=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='specialized_weak_mechanical_action')
 tail=next(i for i,n in enumerate(old.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='point_native' for t in n.targets))
 args=ast.parse('def recovered_weak_collect(basis,native_parts,metric_parts,completed,keep,label): pass').body[0].args
 head=ast.parse("masks=dict(native=np.broadcast_to(P.native_mask(),(33,3,87,45)),metric=P.metric_mask())").body
 resumed=ast.FunctionDef(name='recovered_weak_collect',args=args,body=head+old.body[tail:],decorator_list=[])
 assert [ast.dump(n,include_attributes=False) for n in resumed.body[1:]]==[ast.dump(n,include_attributes=False) for n in old.body[tail:]]
 exec(compile(ast.fix_missing_locations(ast.Module(body=[resumed],type_ignores=[])),file+'_unearned_collector','exec'),globals())


def failed_admission():
 for ref in (FAILED_SOURCE,FAILED_ERROR,FAILED_RECEIPT,FAILED_PROOF):bind(ref[0],ref[1])
 e=json.loads(P.path(FAILED_ERROR[0]).read_text());rc=json.loads(P.path(FAILED_RECEIPT[0]).read_text());proof=json.loads(P.path(FAILED_PROOF[0]).read_text())
 assert e['status']=='FAILED' and rc['status']=='CLOSED_ERROR' and rc['error_sha256']==FAILED_ERROR[1] and rc['prior_receipt_sha256'] is None
 assert e['owner']==rc['owner']==proof['owner'] and e['owner']['pid']==30246 and e['owner']['source_sha256']==FAILED_SOURCE[1]
 assert e['qualification']==rc['qualification']==proof['qualification']==FLAGS and e['raw_preservation_traceback'] is e['closing_traceback'] is None
 assert proof['status']==FAILED_PROOF[2] and proof['source_sha256']==FAILED_SOURCE[1] and proof['error_sha256']==FAILED_ERROR[1] and proof['receipt_sha256']==FAILED_RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==1 and proof['all_input_seals_verified'] is proof['all_output_seals_verified'] is proof['all_success_role_seals_verified'] is proof['failed_role_seal_verified'] is True
 assert proof['input_seals_verified']==len(rc['input_sha256'])==34 and proof['output_seals_verified']==len(rc['output_sha256'])==29
 assert proof['completed_original_controls']==18 and proof['unstarted_original_controls']==4 and proof['recover_earned_lifts_jets_nu_nz_q_before_new_V'] is True
 tb=e['traceback'];assert "NameError: name 'a_dd' is not defined" in tb and 'compact_momentum_matvec' in tb and "V=put('V',compact_momentum_matvec(proj,q))" in tb
 assert not P.path(FAILED_ERROR[0].removesuffix('_ERROR.json')+'_RESULT.json').exists()
 controls=e['controls'];assert len(controls)==18 and all(q['passed'] is True and q['tolerance']==2e-11 for q in controls)
 expected=[f'NEW_{kind}_{way}_node{node}' for kind in ('actual','fixture') for way in ('forward','adjoint') for node in (1912,1890,3847,1934)]
 expected.insert(8,'NEW_actual_adjoint_directed_transpose_pairing');expected.append('NEW_fixture_adjoint_directed_transpose_pairing')
 assert [q['name'] for q in controls]==expected;CHECKS.extend(controls)
 records=e['checkpoints'];assert len(records)==13 and [thin(q) for q in records[:12]]==proof['successful_roles'] and thin(records[-1])==proof['failed_role']
 kinds=['copied_actual_closed_full_node_factors_and_same_candidate_basis','independent_fraction_directed_arrowhead_polynomials_before_NEW_apply','NEW_represented_factor_application_and_independent_polynomial_contacts','NEW_represented_factor_application_and_independent_polynomial_contacts','NEW_complete_dyadic_directed_factor_fixture','independent_fraction_directed_arrowhead_polynomials_before_NEW_apply','NEW_represented_factor_application_and_independent_polynomial_contacts','NEW_represented_factor_application_and_independent_polynomial_contacts']+['direct_hydration_of_earned_full147_cache_without_prepare_or_action']*4
 for i,q in enumerate(records):
  for key,h in (('file','sha256'),('commit_file','commit_sha256')):bind(q[key],q[h]);assert rc['output_sha256'][q[key]]==q[h]
  assert json.loads(P.path(q['commit_file']).read_text())=={k:v for k,v in q.items() if k not in ('commit_file','commit_sha256')}
  assert q['metadata']['owner']==e['owner'] and q['metadata']['qualification']==FLAGS and q['metadata']['failed'] is (i==12)
  if i<12:assert q['metadata']['kind']==kinds[i]
 for n,h in rc['input_sha256'].items():bind(n,h)
 return dict(error=e,receipt=rc,proof=proof,success=records[:12],raw=records[-1],original_failure_preserved=True)


def hydrate_recovery(refs):
 inp=refs['success'][0];data=P.read_pair(inp,tuple('authentic_basis_'+n for n in ('R','dv','hats','cell_i','cell_j','r','z')));RAW.clear()
 basis={n:keep('inherited_basis_'+n,data['authentic_basis_'+n]) for n in ('R','dv','hats','cell_i','cell_j','r','z')}
 admitted=candidate_point_provider_admission(bind);assert inp['metadata']['mechanical']==json.loads(P.encode(admitted['closed_provenance']).decode())
 prefix=POINT_CACHE_PREFIX;caches=[]
 for iq,ref in enumerate(refs['success'][8:12]):
  md=ref['metadata'];assert md['column']==iq and md['source']==thin(admitted['caches'][iq]) and md['mechanical']==inp['metadata']['mechanical']
  original=admitted['caches'][iq];names=candidate_point_cache_names(original['metadata']);selected=tuple('closed_cache%d_'%iq+n for n in names)
  data=P.read_pair(ref,selected);RAW.clear();local={n:keep('inherited_cache%d_'%iq+n,data['closed_cache%d_'%iq+n]) for n in names};pair=lambda n:tuple(local[prefix+n+'_'+w] for w in ('hi','lo'));ep=prefix+'copied_positive_coefficient_'
  cache=dict(s={n:local[prefix+'raw_configuration_'+n] for n in POINT_S},c={n:local[prefix+'raw_chart_'+n] for n in POINT_C},p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a for n,a in local.items() if n.startswith(ep)},constants=original['metadata']['constants'],candidate_provenance=original['metadata']['candidate_provenance'],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
  assert all(cache['constants'][n]==getattr(P,n) for n in ('ALPHA','ELL','C'));caches.append(cache)
 raw=refs['raw'];data=P.read_pair(raw,tuple(raw['metadata']['schema']));RAW.clear()
 for n,a in data.items():keep('inherited_failed_raw_'+n,a)
 def pair(n):return tuple(data[n+'_'+w].copy() for w in ('hi','lo'))
 root='NEW_fullweak0';jet=root+'_column0_NEW_NEW_linear_jets_';can=root+'_column0_NEW_NEW_linear_canonical_'
 jets={n:pair(jet+field) for n,field in dict(du='du',dz='dz',dg='dg',Ga='Ga',Ut='formal_U_time_direction',Zt='formal_z_time_direction',Q='physical_symmetric_hdot',formal_inverse_time='formal_inverse_time_direction',formal_up_time='formal_up_time_direction',gamma_time='gamma_time_direction').items()}
 saved={n:pair(can+n) for n in ('nu','nz','q')};physical={n:pair(jet+'input_'+n) for n in ('native','metric')}
 native=pair(root+'_original_lift_native_values');metric=pair(root+'_original_lift_physical_metric_values');nodes={n:pair(root+'_supplied_'+n+'_nodes') for n in ('native','metric')}
 rhs=[tuple(data['declared_rhs%d_packed_both_words'%d][w].copy() for w in (0,1)) for d in (0,1)];nodepairs=[]
 for d,x in enumerate(rhs):
  u=[P.unpack_fields(a,False) for a in x];nodepairs.append((tuple(v[0] for v in u),tuple(v[1] for v in u)))
  assert all(np.array_equal(nodepairs[0][k][w],nodes[('native','metric')[k]][w]) for k in (0,1) for w in (0,1))
 assert native[0].shape==native[1].shape==(33,15136,3) and metric[0].shape==metric[1].shape==(15136,6)
 assert all(np.array_equal(physical['native'][w],native[w][:,:3784].transpose(1,0,2).reshape(3784,99)) and np.array_equal(physical['metric'][w],metric[w][:3784]) for w in (0,1))
 assert not any(can+n+'_'+w in data for n in ('V','D','F','Pi','native_density') for w in ('hi','lo')),'Unexpected completed canonical substep needs different recovery'
 partial=seal('INHERITED_PARTIAL',dict(kind='copied_earned_basis_cache_lifts_col0_jets_nu_nz_q_before_NEW_V_only',failed_source=FAILED_SOURCE,failed_error=FAILED_ERROR,failed_receipt=FAILED_RECEIPT,failed_proof=FAILED_PROOF,old_success_roles=[thin(q) for q in refs['success']],failed_raw=thin(raw),original18controls_inherited_verbatim=True,old_failure_preserved=True,old_action_or_fixture_replayed=False,physical_adoption=False))
 return dict(columns=caches,basis={n:basis[n] for n in ('R','dv','hats')},all_four_actual_columns_required=True,global_inverse_earned=False,physical_adoption=False),basis,admitted,dict(jets=jets,saved=saved,physical=physical,native_lift=native,metric_lift=metric,nodepairs=nodepairs,partial=thin(partial))


def resume_first_weak(blocks,basis,partial,keep,label,column_complete):
 native_parts=[];metric_parts=[];completed=[]
 for iq,cache in enumerate(blocks['columns']):
  CONTEXT.update(stage='NEW_unearned_weak_column',direction=0,column=iq,resume_at='V' if iq==0 else 'temporal_jets')
  sl=slice(iq*3784,(iq+1)*3784);physical=dict(native=tuple(a[:,sl].transpose(1,0,2).reshape(3784,99).copy() for a in partial['native_lift']),metric=tuple(a[sl].copy() for a in partial['metric_lift']))
  if iq==0:
   point=recovered_canonical_after_q(cache,partial['jets'],partial['saved'],keep,label+'_column0_NEW_NEW_linear_canonical')
   result=dict(point=point,jets=partial['jets'],fixed_configuration_temporal_derivative=True,old_frozen_or_general160_action_replayed=False,physical_adoption=False)
  else:result=candidate_specialized_temporal_action(cache,physical,keep,label+'_column%d_NEW'%iq)
  point=result['point'];native_parts.append(sw_keep(label+'_column%d_native_point'%iq,point['native'],keep));metric_parts.append(sw_keep(label+'_column%d_metric_point'%iq,point['metric_total'],keep))
  completed.append(column_complete(iq,dict(supplied_physical_rates=physical,specialized_temporal_result=result,general160_configuration_contact_evaluated=False,normal_stress_response_earned=False)))
 return recovered_weak_collect(basis,native_parts,metric_parts,completed,keep,label)


def recovered_weak_contacts(blocks,basis,admitted,input_ref,partial):
 for direction in (0,1):
  native,metric=partial['nodepairs'][direction];test_native,test_metric=partial['nodepairs'][1-direction]
  def column_complete(iq,data):
   CONTEXT.update(stage='NEW_unearned_weak_column',direction=direction,column=iq)
   point=data['specialized_temporal_result']['point'];raw=candidate_point_canonical_envelopes(blocks['columns'][iq],data['supplied_physical_rates'],keep,'NEW_weak%d_column%d_bounds'%(direction,iq));gamma=2048*np.finfo(np.float64).eps/(1-2048*np.finfo(np.float64).eps)
   for name,key in (('native','native'),('metric_total','metric_total')):
    e=raw[key];pair=point[name];zero=e==0;upper=np.nextafter(abs(pair[0])+abs(pair[1]),np.inf);padded=np.nextafter(e*(1+gamma),np.inf);upper[zero]=padded[zero]=0.;keep('NEW_weak%d_column%d_%s_enclosure_operands'%(direction,iq,name),np.stack((e,upper,padded)))
    assert all(np.all(w[zero]==0) for w in pair) and np.all(upper<=padded),'NEW source positive chain must enclose represented point action'
   return thin(seal('WEAK_COLUMN',dict(kind='NEW_fullweak67_column_and_positive147_operands',direction=direction,column=iq,mechanical=admitted['closed_provenance'],source_cache=thin(admitted['caches'][iq]),partial=partial['partial'] if direction==iq==0 else None,old_action_replayed=False,normal_phase_or_current_reevaluated=False)))
  label='NEW_fullweak%d'%direction;CONTEXT.update(stage='NEW_unearned_weak_direction',direction=direction,column=0,resume_at='V' if direction==0 else 'original_nodal_lifts')
  result=resume_first_weak(blocks,basis,partial,keep,label,column_complete) if direction==0 else specialized_weak_mechanical_action(blocks,basis,native,metric,keep,label,column_complete=column_complete)
  for family in ('point','weak'):
   for name,pair in result[family].items():keep(label+'_%s_%s_both_words'%(family,name),np.stack(pair))
  independent_weak_contact(result,basis,test_native,test_metric,label)
  seal('WEAK_CONTACT',dict(kind='NEW_all_four_candidate_weak_action_and_independent_nodal_polynomial_transpose_contact',direction=direction,input=thin(input_ref),same_four_authentic_cached147_columns=True,source_positive_enclosure_retained=True,old_point_action_or_fixture_replayed=False,original_six_solve_gates_not_tested=True,full_weak_inverse_qualified=False,physical_adoption=False))


def main():
 assert not AUTHOR_DRAFT and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root reviewed release required'
 assert all(x is not None for ref in (FAILED_SOURCE,FAILED_ERROR,FAILED_RECEIPT,FAILED_PROOF) for x in ref),'Authentic natural failed closure and root proof required'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive recovery namespace required';initialize_recovery();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);bind(Path(__file__).name,SCOPE['OWNER']['source_sha256']);bind(DRIVER_PROTOCOL,PROTOCOL_SHA)
  for n,h in PINS.items():bind(n,h)
  refs=failed_admission();P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,failed_source=FAILED_SOURCE,failed_proof=FAILED_PROOF,original18controls_inherited_verbatim=True,original12success_roles=[thin(q) for q in refs['success']],failed_raw=thin(refs['raw']),qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):
   blocks,basis,admitted,partial=hydrate_recovery(refs);recovered_weak_contacts(blocks,basis,admitted,refs['success'][0],partial)
  assert CHECKS[:18]==refs['error']['controls'] and len(CHECKS)==22 and all(q['passed'] is True and q['tolerance']==2e-11 for q in CHECKS)
  assert [q['name'] for q in CHECKS[18:]]==['NEW_fullweak%d_%s_polynomial_transpose'%(d,n) for d in (0,1) for n in ('native','metric')]
  assert len(RECORDS)==11 and RECORDS[0]['metadata']['kind']=='copied_earned_basis_cache_lifts_col0_jets_nu_nz_q_before_NEW_V_only'
  logical=refs['success']+RECORDS[1:];assert len(logical)==22
  case=dict(factor_record=refs['success'][0]['metadata']['factor_record'],factor_terminal=dict(source=FACTOR_SOURCE,result=FACTOR_RESULT,receipt=FACTOR_RECEIPT,proof=FACTOR_CLOSURE_PROOF),original_failed_source=FAILED_SOURCE,original_failed_error=FAILED_ERROR,original_failed_receipt=FAILED_RECEIPT,original_failed_proof=FAILED_PROOF,original_failure_preserved=True,inherited_controls=18,new_controls=4,original_logical_roles=22,inherited_success_roles=12,new_original_roles=10,current_recovery_roles=11,auxiliary_partial_copy=partial['partial'],inherited_success_records=[thin(q) for q in refs['success']],old_factor_fixture_lifts_col0_jets_nu_nz_q_replayed=False,physical_adoption=False)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status='DIRECTED_NODAL_REPRESENTED_FACTOR_ADJOINT_AND_NEW_WEAK_CONTACTS_PASS',case=case,controls=CHECKS,checkpoints=logical,roles=22,current_checkpoints=RECORDS,current_roles=11,old_componentwise_inverse_failure_repaired=False,original_six_residual_gates_tested=False,uniform_DD_or_global_inverse_qualified=False,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',{n:np.asarray(a).copy() for n,a in {**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}.items()},dict(context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
