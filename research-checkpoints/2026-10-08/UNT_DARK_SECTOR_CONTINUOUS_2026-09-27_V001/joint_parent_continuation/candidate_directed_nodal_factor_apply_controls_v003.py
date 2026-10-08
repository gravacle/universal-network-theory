"""HELD NEW full-node represented-factor/adjoint and separate weak contacts.
Root alone executes after CLOSED all-grid factors and independent review.
No factorization, old application/action/fixture or solver is replayed.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_CONTROLS_V003'
PROTOCOL='CANDIDATE_DIRECTED_NODAL_FACTOR_APPLY_CONTROLS_V002.md'
PROTOCOL_SHA='52ff8bd329cd4eb28e0c13a5a9b17661c47c93e1010c410d7e56020d2c568327'
FACTOR_SOURCE=('cross_u_candidate_directed_nodal_preconditioner_preparation_v005.py', '41d6b4b3d200c8e017759ee3f95e05addaf3d7ea59b53a61f0fcc12b3f514659')
FACTOR_RESULT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RESULT.json', '20ddbdfe237cf5062440971f59b838046962994ad9517d3851d400e3e3b8a811', 'CANDIDATE_DIRECTED_NODAL_NUMERICAL_FACTORS_PREPARED_UNQUALIFIED')
FACTOR_RECEIPT=('CROSS_U_CANDIDATE_DIRECTED_NODAL_PRECONDITIONER_PREPARATION_V005_RECEIPT.json', '46221584fefc9a1ee67cfe62cdf6b27d4710964f60b4ad7865ed6e48e0cdd57b', 'CLOSED')
FACTOR_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_V001.json', '915f5cb58d42291166940df770359ab4416ef153c47dba9b43c680dbc6a6b7af', 'ROOT_NATURAL_CLOSED_DIRECTED_NODAL_PREPARATION_SUCCESS_SEALS_VERIFIED')
MECHANICAL_SOURCE=('cross_u_completed_candidate_mechanical_cache_preparation_v004.py','489465b76f4a8afa7f50b4c1e859748de6d727b0587fc74d37775777a2b99522')
MECHANICAL_RESULT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RESULT.json','49f1c1fb43d3c5243264027e1c35a1020d87d419cb2649b2f5b3814f945ab31e','COMPLETED_CANDIDATE_MECHANICAL_TEMPORAL_CACHES_PREPARED_UNQUALIFIED')
MECHANICAL_RECEIPT=('CROSS_U_COMPLETED_CANDIDATE_MECHANICAL_CACHE_PREPARATION_V004_RECEIPT.json','c72d16d4c9ee1cec99435dd313db80f21d2cf86058fda67d18d7db1a9ec67b64','CLOSED')
MECHANICAL_CLOSURE_PROOF=('ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_V001.json','2ab686545fe9fec63048307ca73bb73bedfd82fb47540152123e545b42ab2ea9','ROOT_NATURAL_CLOSED_MECHANICAL_CACHE_SUCCESS_SEALS_VERIFIED')
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_candidate_specialized_temporal_action_v001.py':'e5f5d3e9ce78a80d85df1d7c5ca70d83204528f624072aafc26cb67862eabbdc',
 'author_fragment_candidate_specialized_weak_mechanical_action_v002.py':'cf26feac610bb9b4df88ce8eb918129a27f07ee5a8eb894184cfd3cea083b3db',
 'author_fragment_candidate_directed_nodal_factor_apply_v001.py':'4ca499ac2447a413742748e3f7bfc9267c0efe8915fa6af63f56c79c48d8169b',
 'author_fragment_candidate_chunk_point_block_provider_v001.py':'4239bfef28d5d961eca8596827eba8165653a723e9c8b379454e9089bdb3b625',
 'author_fragment_single_decode_recheck_v001.py':'ed626c4309030a576c438d8beb9365908593a2ec6b094dbf434e90df3432aa6d'}
DECLARED_NODES=((43,22),(43,0),(86,22),(43,44))
np=P=None;SCOPE={};RAW={};AVAILABLE={};DD_ARRAY_CURRENT={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DESCRIPTIONS={}
FLAGS=dict(represented_factor_or_adjoint_admitted=False,old_componentwise_inverse_failure_repaired=False,full_weak_inverse_qualified=False,global_rank_earned=False,canonical_currents_restored=False,physical_adoption=False)

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

def record(ref,owner,receipt):
 for key,hkey in (('file','sha256'),('commit_file','commit_sha256')):bind(ref[key],ref[hkey]);assert receipt['output_sha256'][ref[key]]==ref[hkey]
 q=P.resolve_record(ref);assert q['metadata']['owner']==owner and q['metadata']['failed'] is False;return q

def admit():
 for ref in (FACTOR_SOURCE,FACTOR_RESULT,FACTOR_RECEIPT,FACTOR_CLOSURE_PROOF):bind(ref[0],ref[1])
 result=json.loads(P.path(FACTOR_RESULT[0]).read_text());rc=json.loads(P.path(FACTOR_RECEIPT[0]).read_text());proof=json.loads(P.path(FACTOR_CLOSURE_PROOF[0]).read_text())
 assert result['status']==FACTOR_RESULT[2] and rc['status']==FACTOR_RECEIPT[2] and rc['result_sha256']==FACTOR_RESULT[1] and rc['error_sha256'] is None
 assert result['owner']==rc['owner']==proof['owner'] and result['owner']['source_sha256']==FACTOR_SOURCE[1]
 assert proof['status']==FACTOR_CLOSURE_PROOF[2] and proof['source_sha256']==FACTOR_SOURCE[1] and proof['result_sha256']==FACTOR_RESULT[1] and proof['receipt_sha256']==FACTOR_RECEIPT[1]
 assert proof['naturally_closed'] is True and proof['exit_code']==0 and proof['all_input_seals_verified'] is True and proof['all_success_role_seals_verified'] is True
 assert all(v is False for v in result['qualification'].values()) and result['qualification']==rc['qualification']
 stem=FACTOR_RESULT[0].removesuffix('_RESULT.json');assert not P.path(stem+'_ERROR.json').exists() and not P.path(stem+'_ERROR_RECEIPT.json').exists()
 case=result['case'];assert case['roles']==len(result['checkpoints'])==5661 and case['new_controls']==len(result['controls'])==15837 and all(x['passed'] and x['tolerance']==2e-11 for x in result['controls'])
 assert len(case['completed_node_refs'])==3870 and len(case['completed_chunk_refs'])==120 and case['right_preconditioner_factor_resolved'] is True and case['full_weak_or_global_inverse_qualified'] is False
 admitted=candidate_point_provider_admission(bind);assert case['closed_mechanical']==json.loads(P.encode(admitted['closed_provenance']).decode())
 q=record(case['factors'],result['owner'],rc);md=q['metadata'];assert md['qualification']==result['qualification'] and md['kind']=='completed_signed_directed_active_nodal_numerical_factors' and md['active_node_count']==3870 and md['coefficient_dimension']==403340
 assert md['sheet_head_dimension']==6 and md['sheet_arm_dimension']==2 and md['interior_head_dimension']==9 and md['interior_arm_dimension']==3 and md['inactive_coordinates_are_zero_not_identity_padding'] is True and md['right_preconditioner_factor_resolved'] is True
 assert md['nodal_apply_or_weak_functional_qualified'] is False and md['exact_weak_DD_or_global_inverse_qualified'] is False and md['physical_adoption'] is False
 names=tuple('assembled_'+n+'_'+w for n in ('D_inverse','S_inverse','B','E') for w in ('hi','lo'));data=P.read_pair(q,names);RAW.clear()
 factors={n:tuple(keep('authentic_factor_'+n+'_'+w,data['assembled_'+n+'_'+w]) for w in ('hi','lo')) for n in ('D_inverse','S_inverse','B','E')}
 factors.update(closed_provenance=dict(factor_record=thin(q),source=FACTOR_SOURCE,result=FACTOR_RESULT,receipt=FACTOR_RECEIPT,proof=FACTOR_CLOSURE_PROOF),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
 iq=admitted['input'];original=P.read_pair(iq,tuple('registered_basis_'+n for n in ('R','dv','hats','cell_i','cell_j','r','z')));RAW.clear();basis={n:keep('authentic_basis_'+n,original['registered_basis_'+n]) for n in ('R','dv','hats','cell_i','cell_j','r','z')}
 assert basis['R'].shape==basis['dv'].shape==(4,3784) and basis['hats'].shape==(4,4,3,86,44) and np.all(basis['R']>0) and np.all(basis['dv']>0)
 assert basis['cell_i'].dtype==basis['cell_j'].dtype==np.int64 and np.array_equal(basis['cell_i'],np.repeat(np.arange(86),44)) and np.array_equal(basis['cell_j'],np.tile(np.arange(44),86))
 inp=seal('INPUT',dict(kind='copied_actual_closed_full_node_factors_and_same_candidate_basis',factor_record=thin(q),factor_proof=FACTOR_CLOSURE_PROOF,mechanical=admitted['closed_provenance'],basis_input=thin(iq),old_componentwise_inverse_contact_remains_failed=True,physical_adoption=False))
 return factors,basis,admitted,inp

def exact(a):return Fraction.from_float(float(a))

def rat(a):return dict(numerator_hex=hex(a.numerator),denominator_hex=hex(a.denominator))

def value(pair,index):return exact(pair[0][index])+exact(pair[1][index])

def matrix(pair,index):return [[value(pair,index+(i,j)) for j in range(pair[0].shape[-1])] for i in range(pair[0].shape[-2])]

def mv(A,x):return [sum((a*b for a,b in zip(row,x)),Fraction(0)) for row in A]

def tr(A):return [list(row) for row in zip(*A)]

def reference(factors,head,arms,node,adjoint):
 D=[matrix(factors['D_inverse'],(m,node)) for m in range(32)];J=matrix(factors['S_inverse'],(node,));B=[matrix(factors['B'],(m,node)) for m in range(32)];E=[matrix(factors['E'],(m,node)) for m in range(32)]
 if adjoint:D=[tr(a) for a in D];J=tr(J);B,E=[tr(a) for a in E],[tr(a) for a in B]
 rh=[value(head,(node,k)) for k in range(9)];ra=[[value(arms,(m,node,k)) for k in range(3)] for m in range(32)];absM=lambda A:[[abs(a) for a in row] for row in A]
 free=[mv(D[m],ra[m]) for m in range(32)];efree=[mv(absM(D[m]),list(map(abs,ra[m]))) for m in range(32)];reduced=rh.copy();er=list(map(abs,rh))
 for m in range(32):
  v=mv(B[m],free[m]);e=mv(absM(B[m]),efree[m]);reduced=[a-b for a,b in zip(reduced,v)];er=[a+b for a,b in zip(er,e)]
 out=mv(J,reduced);eh=mv(absM(J),er);za=[];ez=[]
 for m in range(32):
  v=mv(E[m],out);e=mv(absM(E[m]),eh);za.append(mv(D[m],[a-b for a,b in zip(ra[m],v)]));ez.append(mv(absM(D[m]),[abs(a)+b for a,b in zip(ra[m],e)]))
 return out,za,eh,ez

def declared_rhs(kind):
 h=P.a_dd(np.zeros((3870,9)));a=P.a_dd(np.zeros((32,3870,3)))
 for i,j in DECLARED_NODES:
  node=(i-1)*45+j;hs=(0,2,3,4,5,8) if j==0 else tuple(range(9));arms=(0,2) if j==0 else (0,1,2)
  for k in hs:h[0][node,k]=(-1.)**(k+kind)*(k+1+kind)/(16 if kind==0 else 32);h[1][node,k]=(-1. if kind else 1.)*2.**-60*h[0][node,k]
  for m in range(32):
   for k in arms:a[0][m,node,k]=(-1.)**(m+k+kind)*(m+1+kind)*(k+1+kind)/(64 if kind==0 else 128);a[1][m,node,k]=(-1. if kind else 1.)*2.**-60*a[0][m,node,k]
 v=[];q=[]
 for word in (0,1):
  n=np.zeros((33,3,87,45));m=np.zeros((6,87,45));n[0,:,1:]=h[word][:,:3].T.reshape(3,86,45);n[1:,:,1:]=a[word].transpose(0,2,1).reshape(32,3,86,45);m[:,1:]=h[word][:,3:].T.reshape(6,86,45);v.append(n);q.append(m)
 packed=tuple(P.pack_fields(n,m) for n,m in zip(v,q));keep('declared_rhs%d_packed_both_words'%kind,np.stack(packed));return packed,h,a,tuple(v),tuple(q)

def contact(pair,targets,envelopes,label,word_exact=False):
 assert pair[0].shape==pair[1].shape==targets.shape==envelopes.shape;keep(label+'_actual_both_words',np.stack(pair));expected=np.zeros((2,)+targets.shape);ratios=np.zeros(targets.shape);entries=[];zero=[]
 for k in np.ndindex(targets.shape):
  t=targets[k];e=abs(t)+envelopes[k];h=float(t);l=float(t-exact(h));expected[(0,)+k]=h;expected[(1,)+k]=l;g=value(pair,k)-t;r=abs(g)/e if e else Fraction(0);z=float(r);ratios[k]=np.nextafter(z,np.inf) if exact(z)<r else z
  entries.append(dict(index=list(k),expected=rat(t),conversion_remainder=rat(t-exact(h)-exact(l)),uncancelled_envelope=rat(envelopes[k]),difference=rat(g)));DESCRIPTIONS[label]=entries.copy()
  if not e:zero.append(k)
 keep(label+'_independent_expected_words',expected);keep(label+'_upward_exact_ratios',ratios)
 assert all(pair[0][k]==pair[1][k]==0 for k in zero),'Zero polynomial envelope requires both words zero'
 if word_exact:assert np.array_equal(np.stack(pair),expected),'Fresh exact dyadic words required'
 P.check(label,ratios,np.zeros_like(ratios),np.ones_like(ratios));assert all(ratios[k]<=2e-11 for k in np.ndindex(ratios.shape))

def selected_output(pair,node):
 v=[];m=[]
 for word in (0,1):
  n,k,_=P.unpack_fields(pair[word],False);i,j=divmod(node,45);v.append(np.concatenate((n[0,:,i+1,j],k[:,i+1,j],n[1:,:,i+1,j].reshape(96))));m.append(n)
 return tuple(v)

def scalar_contact(actual,expected,envelope,label):
 bound=abs(expected)+envelope;gap=actual-expected;ratio=abs(gap)/bound if bound else Fraction(0);words=[]
 for name,t in (('actual',actual),('expected',expected)):
  DESCRIPTIONS[label+'_'+name]=dict(value=rat(t));h=float(t);l=float(t-exact(h));words.append([h,l]);DESCRIPTIONS[label+'_'+name]['conversion_remainder']=rat(t-exact(h)-exact(l))
 DESCRIPTIONS[label+'_exact_difference']=dict(gap=rat(gap),uncancelled_envelope=rat(envelope),ratio=rat(ratio));keep(label+'_scalar_words_with_remainders_declared',np.array(words));r=float(ratio);r=np.nextafter(r,np.inf) if exact(r)<ratio else r;keep(label+'_upward_exact_ratio',np.array([r]))
 assert bound or actual==expected==0,'Zero envelope requires exact zero scalar identity'
 P.check(label,np.array([r]),np.zeros(1),np.ones(1));assert ratio<=Fraction.from_float(2e-11)

def factor_contacts(factors,input_ref,fixture=False):
 CONTEXT.update(stage='NEW_complete_dyadic_fixture' if fixture else 'NEW_actual_represented_factor_contacts');x,h,a,native,metric=declared_rhs(0);y,hy,ay,_,_=declared_rhs(1);refs={}
 for adj,hh,aa in ((False,h,a),(True,hy,ay)):
  for i,j in DECLARED_NODES:
   node=(i-1)*45+j;t,z,e,ez=reference(factors,hh,aa,node,adj);refs[adj,node]=(np.array(t+sum(z,[]),dtype=object),np.array(e+sum(ez,[]),dtype=object));DESCRIPTIONS[('adjoint' if adj else 'forward')+'_node%d'%node]=[dict(target=rat(q),envelope=rat(b)) for q,b in zip(refs[adj,node][0],refs[adj,node][1])]
 target_ref=seal('FIXTURE_TARGETS' if fixture else 'FACTOR_TARGETS',dict(kind='independent_fraction_directed_arrowhead_polynomials_before_NEW_apply',input=thin(input_ref),nodes=DECLARED_NODES,fresh_fixture=fixture))
 prepared=prepare_candidate_directed_nodal_factor_apply(factors,keep,'NEW_fixture_prepare' if fixture else 'NEW_actual_prepare');outs=[]
 for adj,rhs in ((False,x),(True,y)):
  label=('NEW_fixture_' if fixture else 'NEW_actual_')+('adjoint' if adj else 'forward');out=(candidate_directed_nodal_factor_adjoint if adj else candidate_directed_nodal_factor_apply)(prepared,rhs,keep,label);outs.append(out)
  support=(x[0]!=0)|(x[1]!=0);assert all(np.all(w[~support]==0) for w in out),'Node-local factor cannot populate other coordinates';keep(label+'_exact_off_support_zero',np.array([True]))
  for i,j in DECLARED_NODES:
   node=(i-1)*45+j;t,e=refs[adj,node];contact(selected_output(out,node),t,e,label+'_node%d'%node,word_exact=fixture)
  if adj:
   indices=np.flatnonzero(support);left=right=bound=Fraction(0);products=[]
   for k in indices:
    l=value(y,(k,))*value(outs[0],(k,));r=value(x,(k,))*value(out,(k,));left+=l;right+=r;products.append(dict(packed_index=int(k),left=rat(l),right=rat(r)));DESCRIPTIONS[label+'_independent_bilinear_products']=products
   for i,j in DECLARED_NODES:
    node=(i-1)*45+j;xs=selected_output(x,node);ys=selected_output(y,node)
    for k in range(105):bound+=abs(value(ys,(k,)))*refs[False,node][1][k]+abs(value(xs,(k,)))*refs[True,node][1][k]
   scalar_contact(left,right,bound,label+'_directed_transpose_pairing')
  seal('FIXTURE_ADJOINT' if fixture and adj else 'FIXTURE_FORWARD' if fixture else 'FACTOR_ADJOINT' if adj else 'FACTOR_FORWARD',dict(kind='NEW_represented_factor_application_and_independent_polynomial_contacts',input=thin(input_ref),targets=thin(target_ref),fresh_literal_word_fixture=fixture,adjoint=adj,old_component_inverse_contact_replayed=False,global_inverse_qualified=False))
 return native,metric

def fixture_factors():
 shape=dict(D_inverse=(32,3870,3,3),S_inverse=(3870,9,9),B=(32,3870,9,3),E=(32,3870,3,9));f={n:P.a_dd(np.zeros(s)) for n,s in shape.items()}
 for node in range(3870):
  ai=(0,2) if node%45==0 else (0,1,2);hi=(0,2,3,4,5,8) if node%45==0 else tuple(range(9))
  for k in ai:f['D_inverse'][0][:,node,k,k]=1.
  for k in hi:f['S_inverse'][0][node,k,k]=2.
  f['B'][0][0,node,0,0]=.125;f['E'][0][1,node,2,2]=.25
 for n,x in f.items():keep('NEW_complete_fixture_'+n+'_both_words',np.stack(x))
 q=seal('FIXTURE_INPUT',dict(kind='NEW_complete_dyadic_directed_factor_fixture',independent_exact_factor_definition='DI=active_identity;J=2active_identity;B_mode0_head0_arm0=1/8;E_mode1_arm2_head2=1/4',actual_candidate_or_factory_resolution=False))
 f.update(closed_provenance=dict(manufactured_complete_factor_input=thin(q),not_actual_candidate=True),all_active_factor_seals_verified=True,active_node_count=3870,right_preconditioner_factor_resolved=True,sheet_head_dimension=6,sheet_arm_dimension=2,interior_head_dimension=9,interior_arm_dimension=3,nodal_apply_or_weak_functional_qualified=False,full_weak_or_global_inverse_qualified=False,physical_adoption=False)
 return f,q

def mechanical_blocks(admitted,basis):
 caches=[];prefix=POINT_CACHE_PREFIX
 for iq,ref in enumerate(admitted['caches']):
  data=P.read_pair(ref,candidate_point_cache_names(ref['metadata']));RAW.clear()
  for n,a in data.items():keep('closed_cache%d_'%iq+n,a)
  pair=lambda n:tuple(data[prefix+n+'_'+w].copy() for w in ('hi','lo'));s={n:data[prefix+'raw_configuration_'+n].copy() for n in POINT_S};c={n:data[prefix+'raw_chart_'+n].copy() for n in POINT_C};ep=prefix+'copied_positive_coefficient_'
  cache=dict(s=s,c=c,p=3784,A=pair('anchored_raw_up_dot_zi'),NA=pair('paired_N_times_anchored_A'),gamma_squared=pair('gamma_squared_denominator'),fixed_E0=pair('fixed_lowered_E0'),envelopes={n[len(ep):]:a.copy() for n,a in data.items() if n.startswith(ep)},constants=ref['metadata']['constants'],candidate_provenance=ref['metadata']['candidate_provenance'],configuration_held=True,old_coefficients_or_primal_features_replayed=False)
  assert all(cache['constants'][n]==getattr(P,n) for n in ('ALPHA','ELL','C')) and c['N'].shape==(3784,);caches.append(cache)
  seal('CACHE_COPY',dict(kind='direct_hydration_of_earned_full147_cache_without_prepare_or_action',column=iq,source=thin(ref),mechanical=admitted['closed_provenance'],physical_adoption=False))
 return dict(columns=caches,basis={n:basis[n] for n in ('R','dv','hats')},all_four_actual_columns_required=True,global_inverse_earned=False,physical_adoption=False)

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

def weak_contacts(admitted,basis,input_ref):
 blocks=mechanical_blocks(admitted,basis)
 for direction in (0,1):
  _,_,_,native,metric=declared_rhs(direction);_,_,_,test_native,test_metric=declared_rhs(1-direction)
  def column_complete(iq,data):
   point=data['specialized_temporal_result']['point'];raw=candidate_point_canonical_envelopes(blocks['columns'][iq],data['supplied_physical_rates'],keep,'NEW_weak%d_column%d_bounds'%(direction,iq));gamma=2048*np.finfo(np.float64).eps/(1-2048*np.finfo(np.float64).eps)
   for name,key in (('native','native'),('metric_total','metric_total')):
    e=raw[key];pair=point[name];zero=e==0;upper=np.nextafter(abs(pair[0])+abs(pair[1]),np.inf);padded=np.nextafter(e*(1+gamma),np.inf);upper[zero]=padded[zero]=0.;keep('NEW_weak%d_column%d_%s_enclosure_operands'%(direction,iq,name),np.stack((e,upper,padded)))
    assert all(np.all(w[zero]==0) for w in pair) and np.all(upper<=padded),'NEW source positive chain must enclose represented point action'
   return thin(seal('WEAK_COLUMN',dict(kind='NEW_fullweak67_column_and_positive147_operands',direction=direction,column=iq,mechanical=admitted['closed_provenance'],source_cache=thin(admitted['caches'][iq]),old_action_replayed=False,normal_phase_or_current_reevaluated=False)))
  result=specialized_weak_mechanical_action(blocks,basis,native,metric,keep,'NEW_fullweak%d'%direction,column_complete=column_complete)
  for family in ('point','weak'):
   for name,pair in result[family].items():keep('NEW_fullweak%d_%s_%s_both_words'%(direction,family,name),np.stack(pair))
  independent_weak_contact(result,basis,test_native,test_metric,'NEW_fullweak%d'%direction)
  seal('WEAK_CONTACT',dict(kind='NEW_all_four_candidate_weak_action_and_independent_nodal_polynomial_transpose_contact',direction=direction,input=thin(input_ref),same_four_authentic_cached147_columns=True,source_positive_enclosure_retained=True,old_point_action_or_fixture_replayed=False,original_six_solve_gates_not_tested=True,full_weak_inverse_qualified=False,physical_adoption=False))

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None
 assert all(x is not None for ref in (FACTOR_SOURCE,FACTOR_RESULT,FACTOR_RECEIPT,FACTOR_CLOSURE_PROOF) for x in ref),'Naturally CLOSED factors and proof required before IO'
 assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required';initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER'])
  for n,h in PINS.items():bind(n,h)
  bind(PROTOCOL,PROTOCOL_SHA);INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256']
  P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,nodes=DECLARED_NODES,scope='NEW_represented_factor_and_separate_fullweak_contacts',factor_closure=FACTOR_CLOSURE_PROOF,old10655_component_inverse_failure_remains=True,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):
   factors,basis,admitted,inp=admit();factor_contacts(factors,inp);fresh,fi=fixture_factors();factor_contacts(fresh,fi,True);weak_contacts(admitted,basis,inp)
  assert len(RECORDS)==22 and len(CHECKS)==22 and all(q['passed'] for q in CHECKS)
  P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status='DIRECTED_NODAL_REPRESENTED_FACTOR_ADJOINT_AND_NEW_WEAK_CONTACTS_PASS',case=dict(factor_record=factors['closed_provenance']['factor_record'],factor_terminal=dict(source=FACTOR_SOURCE,result=FACTOR_RESULT,receipt=FACTOR_RECEIPT,proof=FACTOR_CLOSURE_PROOF)),controls=CHECKS,checkpoints=RECORDS,roles=len(RECORDS),old_componentwise_inverse_failure_repaired=False,original_six_residual_gates_tested=False,uniform_DD_or_global_inverse_qualified=False,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',{n:np.asarray(a).copy() for n,a in {**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}.items()},dict(context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
