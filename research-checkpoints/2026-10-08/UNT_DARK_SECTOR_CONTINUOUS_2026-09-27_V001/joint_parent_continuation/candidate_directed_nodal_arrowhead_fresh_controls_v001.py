"""HELD fresh synthetic nodal map/moment/factor/carry controls; root only.
No actual candidate/action/producer, old fixture or payload is consumed.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_DIRECTED_NODAL_ARROWHEAD_FRESH_CONTROLS_V001'
PROTOCOL='CANDIDATE_DIRECTED_NODAL_ARROWHEAD_FRESH_CONTROLS_V002.md'
PROTOCOL_SHA='2fd4cdf10c614930ee90b83e2c8bb57bab7ca2627ae625a554cef39dc1e81851'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_exact_exponent_two_product_v003.py':'f9bd89a0672f3eeaf4c0dbcc4ee0c5b09236fe5f9cfc14645e24d9532f909235',
 'author_fragment_candidate_directed_nodal_arrowhead_v001.py':'0a05eacd67d3093e2328c7197cdfb257488771ec7e0078b77a972340ef662bb6'}
np=P=None;SCOPE={};RAW={};AVAILABLE={};DD_ARRAY_CURRENT={};INPUTS={};OUTPUTS={};RECORDS=[];CHECKS=[];CONTEXT={};DESCRIPTIONS={}
FLAGS=dict(actual_candidate_operator_qualified=False,nodal_factor_or_apply_admitted=False,full_weak_inverse_qualified=False,global_rank_earned=False,physical_adoption=False)

class FixtureInterrupted(Exception):pass

def bind(n,h):
 assert h is not None and P.sha(P.path(n))==h;INPUTS[str(P.path(n).resolve())]=h

def keep(n,x):
 a=np.asarray(x).copy();AVAILABLE[n]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),n;return a

def arrays(d):return {n:np.asarray(a).copy() for n,a in d.items()}

def thin(q):return {n:q[n] for n in ('file','sha256','commit_file','commit_sha256')}

def clear():RAW.clear();AVAILABLE.clear();DD_ARRAY_CURRENT.clear();DESCRIPTIONS.clear()

def seal(role,metadata):
 q=P.checkpoint(role,arrays({**RAW,**AVAILABLE}),dict(context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS),**metadata));clear();return q

def initialize():
 global P,SCOPE,np
 n=list(PINS)[1];assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==PINS[n]
 io={'now','path','sha','canonical','encode','publish','json_file','check','checkpoint','recheck','seal_actual','read_pair','resolve_record'};t=ast.parse((BASE/n).read_text());defs=[x for x in t.body if isinstance(x,ast.FunctionDef) and x.name in io];assert len(defs)==13
 SCOPE=dict(Path=Path,datetime=datetime,timezone=timezone,hashlib=hashlib,json=json,math=math,os=os,np=None,__file__=str(Path(__file__).resolve()),BASE=BASE,STEM=STEM,BAND='CROSS_U_NGC3198_ODD_BANDED_CORRECTION_V001',OWNER=None,TOL=2e-11,FLAGS=FLAGS,INPUTS=INPUTS,OUTPUTS=OUTPUTS,RECORDS=RECORDS,CHECKS=CHECKS,RAW=RAW,AVAILABLE=AVAILABLE,CONTEXT=CONTEXT,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT)
 exec(compile(ast.Module(body=defs,type_ignores=[]),n,'exec'),SCOPE);P=types.SimpleNamespace(**{k:SCOPE[k] for k in io})

def arithmetic():
 global np
 import numpy as numpy
 np=numpy;SCOPE.update(np=np,capture=keep)
 for n,h in PINS.items():bind(n,h)
 bind(PROTOCOL,PROTOCOL_SHA)
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64','a_reshape','dd_metric_F'};n=list(PINS)[0];t=ast.parse((BASE/n).read_text());defs=[x for x in t.body if isinstance(x,ast.FunctionDef) and x.name in base];assert len(defs)==14
 exec(compile(ast.Module(body=defs,type_ignores=[]),n,'exec'),SCOPE)
 for k in base:setattr(P,k,SCOPE[k])
 P.TOL=2e-11
 for n,count in ((list(PINS)[2],2),(list(PINS)[3],9)):
  t=ast.parse((BASE/n).read_text());defs=[x for x in t.body if isinstance(x,ast.FunctionDef)];assert len(defs)==count;exec(compile(ast.Module(body=defs,type_ignores=[]),n,'exec'),globals())
 install_exact_exponent_product(SCOPE,P,keep,'NEW_exact_product')

def rational(x):return dict(numerator_hex=hex(x.numerator),denominator_hex=hex(x.denominator))

def exact(x):return Fraction.from_float(float(x))

def reference_contact(pair,targets,label,word_exact=False):
 assert pair[0].shape==pair[1].shape==targets.shape;keep(label+'_actual_both_words',np.stack(pair));expected=(np.zeros(targets.shape),np.zeros(targets.shape));ratios=np.zeros(targets.shape);entries=[]
 for index in np.ndindex(targets.shape):
  t=targets[index];assert isinstance(t,Fraction);h=float(t);l=float(t-exact(h));expected[0][index]=h;expected[1][index]=l;a=exact(pair[0][index])+exact(pair[1][index]);e=abs(t);gap=a-t
  entries.append(dict(index=list(index),target=rational(t),conversion_remainder=rational(t-exact(h)-exact(l)),difference=rational(gap)));DESCRIPTIONS[label]=entries.copy()
  if not e:assert pair[0][index]==pair[1][index]==0
  else:
   ratio=abs(gap)/e;x=float(ratio);ratios[index]=float(np.nextafter(x,np.inf)) if exact(x)<ratio else x
 keep(label+'_expected_both_words',np.stack(expected));keep(label+'_exact_ratio_readout',ratios)
 if word_exact:assert all(np.array_equal(a,b) for a,b in zip(pair,expected))
 P.check(label,ratios,np.zeros_like(ratios),np.ones_like(ratios));assert all(not targets[k] or abs(exact(pair[0][k])+exact(pair[1][k])-targets[k])/abs(targets[k])<=Fraction.from_float(2e-11) for k in np.ndindex(targets.shape))

def mm(A,B):return [[sum((a*b for a,b in zip(row,col)),Fraction(0)) for col in zip(*B)] for row in A]

def transpose(A):return [list(x) for x in zip(*A)]

def fraction_matrix(A):return [[exact(x) for x in row] for row in A]

def map_controls():
 CONTEXT.update(case='first_axis_independent_alias_maps');R=keep('R',np.array([1.5,3.]));i=keep('cell_i',np.zeros(2,dtype=np.int64));j=keep('cell_j',np.array([0,1],dtype=np.int64));hat=keep('hats',np.array([[1/3]*2,[2/3]*2,[1/4]*2,[3/4]*2]));F=np.zeros((2,6,6))
 for p,r in enumerate((Fraction(3,2),Fraction(3))):
  for a,b,v in ((0,0,1),(0,1,r*r),(1,5,1),(2,0,r*r),(3,3,r),(4,2,r*r*r),(5,4,r*r)):F[p,a,b]=float(v)
 keep('independent_declared_F',F);native=np.empty((2,3),dtype=object);left=np.empty((2,6,6),dtype=object);right=np.empty_like(left)
 for p in range(2):
  native[p]=[exact(hat[1,p]),Fraction(0) if p==0 else exact(hat[0,p])+exact(hat[1,p]),exact(float(R[p]**2*hat[0,p]))+exact(float(R[p]**2*hat[1,p]))]
  for a in range(6):
   for b in range(6):
    left[p,a,b]=sum((exact(hat[k,p])*exact(F[p,a,b]) for k in (0,1)),Fraction(0));right[p,a,b]=sum((exact(float(hat[k,p]*F[p,a,b])) for k in (0,1)),Fraction(0))
    if p==0 and b in (3,4):left[p,a,b]=right[p,a,b]=Fraction(0)
 DESCRIPTIONS['independent_axis_targets']={n:[dict(index=list(k),target=rational(t[k])) for k in np.ndindex(t.shape)] for n,t in (('native',native),('left',left),('right',right))};maps=nj_identified_maps(R,hat,i,j,0,keep,'NEW_axis')
 reference_contact((AVAILABLE['NEW_axis_native_alias_paired_hi'],AVAILABLE['NEW_axis_native_alias_paired_lo']),native,'axis_native_words',True)
 reference_contact((AVAILABLE['NEW_axis_left_alias_paired_hi'],AVAILABLE['NEW_axis_left_alias_paired_lo']),left,'axis_left_exact_words',True)
 reference_contact((AVAILABLE['NEW_axis_right_alias_paired_hi'],AVAILABLE['NEW_axis_right_alias_paired_lo']),right,'axis_right_rounded_words',True)
 assert np.array_equal(maps['node'],np.array([0,1])) and np.all(maps['valid'])
 assert np.any(AVAILABLE['NEW_axis_left_minus_right_polynomial_hi']!=0) or np.any(AVAILABLE['NEW_axis_left_minus_right_polynomial_lo']!=0)
 seal('AXIS',dict(kind='fresh_exact_fraction_axis_alias_and_sheet_masks'))

def point_fixture():
 H=np.diag([-3.,4.,5.,-6.,7.,8.,9.,10.,11.]);H[0,1]=.25;H[1,0]=-.125;B=np.zeros((32,9,3));E=np.zeros((32,3,9));D=np.zeros((32,3,3))
 for m in range(32):
  B[m,0,0]=(m+1)/128;B[m,4,2]=-(m+2)/256;E[m,0,1]=-(m+3)/256;E[m,2,5]=(m+4)/512;D[m]=np.diag([(-1.)**m*(m+1)/16,2+(m+1)/32,3+(m+1)/64])
 return dict(H=H,B=B,E=E,D=D)

def moment_controls():
 CONTEXT.update(case='two_chunk_signed_unequal_mode_moments_and_carry');basis=dict(R=np.full((4,3784),2.),dv=np.full((4,3784),3.),hats=np.zeros((4,4,3,86,44)),cell_i=np.repeat(np.arange(86),44),cell_j=np.tile(np.arange(44),86),closed_provenance=dict(kind='NEW_declared_synthetic_basis'))
 active=(3590,3760);hv=((.125,.25,.375,.25),(.25,.125,.25,.375));flat=basis['hats'][3,:,0].reshape(4,3784)
 for pt,h in zip(active,hv):flat[:,pt]=h
 table=point_fixture();cols=[dict(closed_candidate_provenance=dict(kind='NEW_synthetic_point_blocks',column=k)) for k in range(4)]
 for n,a in table.items():keep('declared_point_'+n,a)
 for n,a in basis.items():
  if isinstance(a,np.ndarray):keep('declared_basis_'+n,a)
 inputs=seal('MOMENT_INPUT',dict(kind='synthetic_basis_and_signed_unequal_mode_point_blocks',active_points=list(active),zero_prefix_before3584=True))
 def provider(iq,sl,keep0,label):
  p=sl.stop-sl.start;out={}
  for n,a in table.items():
   shape=(p,)+a.shape if n=='H' else (32,p)+a.shape[1:];v=np.zeros(shape)
   for pt in active:
    if iq==3 and sl.start<=pt<sl.stop:
     if n=='H':v[pt-sl.start]=a
     else:v[:,pt-sl.start]=a
   out[n]=v;out['e'+n]=abs(v);keep0(label+'_'+n,v);keep0(label+'_e'+n,abs(v))
  out.update(paired_raw={n:P.a_dd(out[n]) for n in table},readout_gaps={n:P.a_dd(np.zeros_like(out[n])) for n in table},closed_candidate_provenance=cols[iq]['closed_candidate_provenance'],construction_contacts=[dict(scope='declared_NEW_synthetic_input',passed=True)],committed_chunk=thin(inputs));return out
 shapes=dict(H=(3870,9,9),B=(32,3870,9,3),E=(32,3870,3,9),D=(32,3870,3,3));zero={n:np.zeros(s) for n,s in shapes.items()};prefix=[dict(kind='manufactured_analytic_zero_prefix',ordinal=k,input=thin(inputs)) for k in range(118)]
 carry=dict(basis_provenance=basis['closed_provenance'],chunk_size=128,closed_restore_provenance=thin(inputs),next_chunk=118,completed_chunk_refs=prefix,moments=zero,bounds={n:a.copy() for n,a in zero.items()})
 saved={};serialrefs=[]
 def callback(d):
  keep('patch_node_ids',d['node_ids'])
  for n,a in d['updated_node_blocks'].items():keep('patch_'+n,a)
  q=seal('MOMENT_CHUNK',dict(kind='fresh_stub_point_aggregate_patch',chunk=d['chunk'],next_chunk=d['next_chunk'],lo=d['lo'],hi=d['hi'],input=thin(inputs)));serialrefs.append(q);saved.update(d=d,q=q)
  return thin(q)
 expected={n:{} for n in table};F=[[Fraction(0) for _ in range(6)] for _ in range(6)]
 for a,b,v in ((0,0,1),(0,1,4),(1,5,1),(2,0,4),(3,3,2),(4,2,8),(5,4,4)):F[a][b]=Fraction(v)
 for pt,hats in zip(active,hv):
  ci,cj=divmod(pt,44)
  for h,(di,dj) in zip(hats,((0,0),(1,0),(0,1),(1,1))):
   node=(ci+di-1)*45+cj+dj;N=[[Fraction(0) for _ in range(3)] for _ in range(3)]
   for k in range(3):N[k][k]=exact(h)*(4 if k==2 else 1)
   L=[[Fraction(0) for _ in range(9)] for _ in range(9)]
   for a in range(3):L[a][a]=N[a][a]
   for a in range(6):
    for b in range(6):L[a+3][b+3]=exact(h)*F[a][b]
   for n,left,right in (('H',L,L),('B',L,N),('E',N,L),('D',N,N)):
    matrices=[table[n]] if n=='H' else table[n]
    for mode,A in enumerate(matrices):
     value=mm(mm(transpose(left),fraction_matrix(A)),right);key=(node,) if n=='H' else (mode,node);old=expected[n].setdefault(key,[[Fraction(0) for _ in row] for row in value])
     for a in range(len(value)):
      for b in range(len(value[0])):old[a][b]+=Fraction(3,2)*value[a][b]
 DESCRIPTIONS['independent_corner_targets']={n:[dict(key=list(key),matrix=[[rational(v) for v in row] for row in target]) for key,target in entries.items()] for n,entries in expected.items()};target_ref=seal('MOMENT_TARGETS',dict(kind='independent_fraction_expected_corner_sums_before_NEW_builder',input=thin(inputs)))
 full=candidate_nodal_arrowhead_moments(cols,basis,provider,keep,callback,'NEW_continuous',carry=carry)
 for n,entries in expected.items():
  for key,target in entries.items():reference_contact(P.a_dd(full['moments'][n][key]),np.array(target,dtype=object),'moment_'+n+'_'+'_'.join(map(str,key)))
 one=seal('MOMENT_REFERENCE',dict(kind='independent_fraction_nonsymmetric_unequal_mode_corner_sums',expected=thin(target_ref),full_candidate_action=False))
 def interrupt(d):callback(d);raise FixtureInterrupted('Declared stop after first tail chunk')
 try:candidate_nodal_arrowhead_moments(cols,basis,provider,keep,interrupt,'NEW_interrupted',carry=carry)
 except FixtureInterrupted:pass
 else:raise AssertionError('Interruption not observed')
 resumed={n:a.copy() for n,a in zero.items()};resb={n:a.copy() for n,a in zero.items()};d=saved['d'];nodes=d['node_ids']
 for n in table:
  key=nodes if n=='H' else (slice(None),nodes);resumed[n][key]=d['updated_node_blocks'][n];resb[n][key]=d['updated_node_blocks']['e'+n]
 nextcarry=dict(carry,moments=resumed,bounds=resb,next_chunk=119,completed_chunk_refs=prefix+[thin(saved['q'])]);after=candidate_nodal_arrowhead_moments(cols,basis,provider,keep,callback,'NEW_resumed',carry=nextcarry)
 for n in table:assert np.array_equal(after['moments'][n],full['moments'][n]) and np.array_equal(after['bounds'][n],full['bounds'][n])
 keep('exact_moment_carry_equal',np.array([True]*8));seal('MOMENT_CARRY',dict(kind='exact_interrupted_resumed_tail_equality',continuous=thin(one),actual_candidate_or_wholegrid_test=False))

def factor_controls():
 CONTEXT.update(case='signed_active_factors_and_node_carry');H=np.zeros((3870,9,9));B=np.zeros((32,3870,9,3));E=np.zeros((32,3870,3,9));D=np.zeros((32,3870,3,3));diag=np.array([-2.,4.,-8.,16.,-32.,64.,-128.,256.,-512.])
 for node in (3825,3868,3869):
  H[node]=np.diag(diag);H[node,0,2 if node%45==0 else 1]=.5
  for m in range(32):
   D[m,node]=np.diag([(-1.)**m*2.**(m%4)*(1+(m+1)/128),2.+m/32,4.+m/64]);B[m,node,0,0]=(m+1)/256;E[m,node,0,2 if node%45==0 else 1]=-(m+3)/512
 targets={}
 for node in (3825,3868,3869):
  ai=[0,2] if node%45==0 else [0,1,2];hi=[0,2,3,4,5,8] if node%45==0 else list(range(9));di=np.empty((32,len(ai),len(ai)),dtype=object);head=np.empty((len(hi),len(hi)),dtype=object);di[:]=Fraction(0);head[:]=Fraction(0)
  for m in range(32):
   for k,slot in enumerate(ai):di[m,k,k]=1/exact(D[m,node,slot,slot])
  for k,slot in enumerate(hi):head[k,k]=1/exact(diag[slot])
  off=Fraction(1,2)-sum((exact(B[m,node,0,0])*exact(E[m,node,0,hi[1]])/exact(D[m,node,0,0]) for m in range(32)),Fraction(0));head[0,1]=-off/(exact(diag[hi[0]])*exact(diag[hi[1]]));targets[node]=(ai,hi,di,head)
  DESCRIPTIONS['independent_factor_node%d'%node]={n:[dict(index=list(k),target=rational(a[k])) for k in np.ndindex(a.shape)] for n,a in (('D_inverse',di),('S_inverse',head))}
 prepared=dict(moments=dict(H=H,B=B,E=E,D=D),bounds=dict(H=abs(H),B=abs(B),E=abs(E),D=abs(D)),full_all_four_sections=True,completed_chunk_refs=[dict(kind='NEW_manufactured_factor_coefficients')]);saved={}
 for n,a in prepared['moments'].items():keep('fresh_factor_active_tail_'+n,a[:,[3825,3868,3869]] if n!='H' else a[[3825,3868,3869]])
 inp=seal('FACTOR_INPUT',dict(kind='declared_NEW_signed_triangular_coefficient_fixture',active_nodes=[3825,3868,3869],not_actual_allgrid_moments=True))
 def carry(start):return dict(completed_moment_refs=prepared['completed_chunk_refs'],equilibrated=False,closed_restore_provenance=thin(inp),D_inverse_raw=np.zeros((32,3870,3,3)),S_inverse_raw=np.zeros((3870,9,9)),next_node=start,completed_node_refs=[dict(kind='explicit_unexamined_manufactured_prefix',ordinal=k,input=thin(inp)) for k in range(start)])
 def callback(d):
  node=d['node'];ai,hi,di,head=targets[node];assert list(d['active_arm'])==ai and list(d['active_head'])==hi
  reference_contact(P.a_dd(d['D_inverse']),di,'independent_Dinv_node%d'%node);reference_contact(P.a_dd(d['S_inverse']),head,'independent_Sinv_node%d'%node)
  for n in ('active_arm','active_head','D_inverse','S_inverse','S'):keep('completed_node_'+n,d[n])
  q=seal('FACTOR_NODE',dict(kind='NEW_independent_triangular_active_factor',node=node,sheet=d['sheet'],input=thin(inp),D_certificate={k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in d['D_certificate'].items()},S_certificate={k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in d['S_certificate'].items()}));saved.update(d=d,q=q);return thin(q)
 full=candidate_nodal_arrowhead_factors(prepared,keep,callback,'NEW_factor_continuous',carry=carry(3868))
 def interrupt(d):callback(d);raise FixtureInterrupted('Declared stop after one new factor node')
 try:candidate_nodal_arrowhead_factors(prepared,keep,interrupt,'NEW_factor_interrupted',carry=carry(3868))
 except FixtureInterrupted:pass
 else:raise AssertionError('Factor interruption not observed')
 c=carry(3869);d=saved['d'];c['completed_node_refs'][-1]=thin(saved['q'])
 for m in range(32):c['D_inverse_raw'][m,3868][np.ix_(d['active_arm'],d['active_arm'])]=d['D_inverse'][m]
 c['S_inverse_raw'][3868][np.ix_(d['active_head'],d['active_head'])]=d['S_inverse'];after=candidate_nodal_arrowhead_factors(prepared,keep,callback,'NEW_factor_resumed',carry=c)
 assert np.array_equal(full['D_inverse_raw'],after['D_inverse_raw']) and np.array_equal(full['S_inverse_raw'],after['S_inverse_raw']);keep('exact_factor_carry_equal',np.array([True,True]));seal('FACTOR_CARRY',dict(kind='exact_interrupted_resumed_two_node_tail',full3870_factor_admission=False))
 try:candidate_nodal_arrowhead_factors(prepared,keep,interrupt,'NEW_sheet_factor',carry=carry(3825))
 except FixtureInterrupted as stopped:
  trace=stopped.__traceback__
  while trace is not None and trace.tb_frame.f_code.co_name!='candidate_nodal_arrowhead_factors':trace=trace.tb_next
  assert trace is not None;fullD=keep('completed_sheet_full_D_inverse',trace.tb_frame.f_locals['DI'][:,3825]);fullJ=keep('completed_sheet_full_S_inverse',trace.tb_frame.f_locals['J'][3825])
  assert np.all(fullD[:,1,:]==0) and np.all(fullD[:,:,1]==0) and all(np.all(fullJ[k]==0) and np.all(fullJ[:,k]==0) for k in (1,6,7))
  del trace
 else:raise AssertionError('Sheet stop not observed')
 d=saved['d'];assert list(d['active_arm'])==[0,2] and list(d['active_head'])==[0,2,3,4,5,8] and d['D_inverse'].shape==(32,2,2) and d['S_inverse'].shape==(6,6)
 keep('sheet_exact_active_dimensions',np.array([2,6]));seal('SHEET_ACTIVE',dict(kind='actual_factory_sheet_active_selection_no_inactive_identity',node=3825))

def scale_controls():
 CONTEXT.update(case='exact_unit_skew_balancing_and_nonexact_refusal');A=np.diag([2.**300,2.**-300,8.]);A[0,1]=2.**299;eA=abs(A);keep('unit_skew_A',A);keep('unit_skew_eA',eA)
 expected=np.array([[Fraction(1,2**300),-Fraction(2**299),Fraction(0)],[Fraction(0),Fraction(2**300),Fraction(0)],[Fraction(0),Fraction(0),Fraction(1,8)]],dtype=object);DESCRIPTIONS['independent_unit_skew_inverse']=[dict(index=list(k),target=rational(expected[k])) for k in np.ndindex(expected.shape)];J,info=nj_active_inverse(A,eA,True,keep,'NEW_skew');reference_contact(P.a_dd(J),expected,'skew_physical_inverse',True);seal('SCALE',dict(kind='independent_exact_scaled_inverse_and_maps',certificate={k:v.tolist() if isinstance(v,np.ndarray) else v for k,v in info.items()}))
 x=np.array([float.fromhex('0x1.0000000000001p-1022')]);keep('nonexact_scale_input',x);keep('nonexact_scale_exponent',np.array([-1],dtype=np.int64))
 try:nj_exact_ldexp(x,np.array([-1],dtype=np.int64),keep,'NEW_refused_scale')
 except AssertionError as error:assert 'Nonexact power-of-two scaling refused' in str(error)
 else:raise AssertionError('Required lost-word scaling refusal absent')
 attempt=AVAILABLE['NEW_refused_scale_scaled_and_restored_attempt'];assert attempt.shape==(2,1) and np.all(np.isfinite(attempt)) and not np.array_equal(attempt[1].view(np.uint64),x.view(np.uint64));keep('nonexact_refusal_observed',np.array([True]));seal('REFUSAL',dict(kind='deliberate_NEW_nonexact_scaling_refusal_all_attempts_preserved'))

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS;assert not list(BASE.glob(STEM+'_*')),'Exclusive namespace required';initialize();SCOPE['OWNER']=dict(owner='root',pid=os.getpid(),started=P.now(),source_sha256=P.sha(Path(__file__).resolve()))
 try:
  P.json_file(STEM+'_OWNER_START.json',SCOPE['OWNER']);arithmetic();INPUTS[str(Path(__file__).resolve())]=SCOPE['OWNER']['source_sha256'];P.json_file(STEM+'_MANIFEST.json',dict(owner=SCOPE['OWNER'],input_sha256=INPUTS,scope='NEW_synthetic_nodal_controls_only',old_fixture_or_actual_candidate_action=False,apply_adjoint_controls_deferred=True,qualification=FLAGS))
  with np.errstate(over='raise',divide='raise',invalid='raise'):map_controls();moment_controls();factor_controls();scale_controls()
  assert CHECKS and all(q['passed'] for q in CHECKS);P.recheck();rh=P.json_file(STEM+'_RESULT.json',dict(owner=SCOPE['OWNER'],status='FRESH_SYNTHETIC_DIRECTED_NODAL_MAP_MOMENT_FACTOR_CARRY_CONTROLS_PASS',controls=CHECKS,checkpoints=RECORDS,apply_adjoint_controls_deferred=True,actual_candidate_or_global_factor_admitted=False,qualification=FLAGS));P.recheck();P.json_file(STEM+'_RECEIPT.json',dict(owner=SCOPE['OWNER'],status='CLOSED',closed=P.now(),input_sha256=INPUTS,output_sha256=dict(OUTPUTS),result_sha256=rh,error_sha256=None,qualification=FLAGS));P.recheck();print(len(CHECKS),len(RECORDS),rh);return 0
 except BaseException:
  failure=traceback.format_exc();raw_error=close_error=None
  if np is not None:
   try:P.checkpoint('ERROR_RAW',arrays({**RAW,**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}),dict(context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS)),failed=True)
   except BaseException:raw_error=traceback.format_exc()
  try:P.seal_actual();P.recheck(False)
  except BaseException:close_error=traceback.format_exc()
  eh=P.json_file(STEM+'_ERROR.json',dict(owner=SCOPE['OWNER'],status='FAILED',traceback=failure,raw_preservation_traceback=raw_error,closing_traceback=close_error,context=dict(CONTEXT),exact_targets=dict(DESCRIPTIONS),controls=CHECKS,checkpoints=RECORDS,input_sha256=INPUTS,qualification=FLAGS));prior=P.path(STEM+'_RECEIPT.json');P.json_file(STEM+('_ERROR_RECEIPT.json' if prior.exists() else '_RECEIPT.json'),dict(owner=SCOPE['OWNER'],status='CLOSED_ERROR',closed=P.now(),error_sha256=eh,prior_receipt_sha256=P.sha(prior) if prior.exists() else None,input_sha256=INPUTS,output_sha256=dict(OUTPUTS),qualification=FLAGS));P.seal_actual();P.recheck(False);raise
if __name__=='__main__':raise SystemExit(main())
