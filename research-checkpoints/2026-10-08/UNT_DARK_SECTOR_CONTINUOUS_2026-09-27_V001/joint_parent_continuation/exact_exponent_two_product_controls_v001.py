"""HELD exact arithmetic controls; numerical invocation belongs to root alone.
Five fresh controls plus one authenticated CLOSED failed product. No candidate,
normal, EOS, inverse, ordinary, earlier fixture or scientific action is replayed.
"""
from pathlib import Path
from fractions import Fraction
import ast,hashlib,json,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='EXACT_EXPONENT_TWO_PRODUCT_CONTROLS_V001'
DRIVER_PROTOCOL='EXACT_EXPONENT_TWO_PRODUCT_CONTROLS_V001.md'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_exact_exponent_two_product_v002.py':'23750efc4326f0b9154da9a052001dbc44119dab7c7bd286ed86f1522a9707a9',
 'EXACT_EXPONENT_TWO_PRODUCT_V001.md':'dd184c87a19a57df59552fd9c78d0f6961246381feeaf2087f2768a19c1a0f32',
 'CLOSED_FINITE0_FAILED_PRODUCT_INPUTS_V001.json':'6d5e6259d23c566c336e5ab26192b9b4cdefe7fadfb3601e05d2b6c005d072da',
 'CLOSED_FINITE0_FAILED_PRODUCT_INPUTS_V001.npz':'053e2c33246c94e3fa59f7d04b421addc4f3cb61118ea99a56bb235b29a36b8c'}
PROTOCOL_SHA='9eba4c5a7cc3522b94eaf4fedb93ad4ec8571f0b91526ee47b57bdf1d5944a5c'
np=P=None;ARITH_SCOPE={};RAW={};CASES=[];CONTROLS=[]

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def keep(name,value):
 a=np.asarray(value).copy();RAW[name]=a;assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));return a
def words(name,value):
 keep(name+'_hi',value[0]);keep(name+'_lo',value[1]);return value
def fraction_product_reference(x,y,actual):
 # Independent exact rational multiplication of the original binary64 inputs.
 x,y=np.broadcast_arrays(x,y);eh=np.zeros(x.shape);el=np.zeros(x.shape);identity=np.zeros(x.shape,dtype=bool)
 for index in np.ndindex(x.shape):
  expected=Fraction.from_float(float(x[index]))*Fraction.from_float(float(y[index]))
  eh[index]=float(expected);el[index]=float(expected-Fraction.from_float(float(eh[index])))
  identity[index]=Fraction.from_float(float(actual[0][index]))+Fraction.from_float(float(actual[1][index]))==expected
 words('independent_Fraction_product',(eh,el));keep('independent_Fraction_exact_identity',identity)
 return (eh,el),bool(np.all(identity))
def record_control(name,predicates):
 actual=np.asarray(predicates,dtype=np.float64);expected=np.ones_like(actual);envelope=np.ones_like(actual)
 for n,a in (('actual',actual),('expected',expected),('envelope',envelope)):keep(name+'_'+n,a)
 error=float(np.max(abs(actual-expected),initial=0.));passed=bool(np.all(actual==expected))
 CONTROLS.append(dict(name=name,error=error,tolerance=2e-11,passed=passed,exact_rational_or_word_predicate=True));assert passed,name
def save_case(case,metadata):
 name=STEM+'_CASE'+str(case)+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(a).copy() for n,a in RAW.items()})
 (BASE/name).chmod(0o444);CASES.append(dict(case=case,file=name,sha256=sha(name),fields=len(RAW),metadata=metadata));RAW.clear();ARITH_SCOPE['DD_ARRAY_CURRENT'].clear()
def fresh_case(case):
 e=2.**-52
 if case==1:return np.array([0.,-0.,1.+e,-3./8,2.**450,2.**-450]),np.array([3.,-4.,1.+e,5./16,2.**-450,2.**450]),None
 if case==2:return np.array([2.**-600*(1.+e)]),np.array([1.+e]),(np.array([2.**-600*(1.+2.**-51)]),np.array([2.**-704]))
 if case==3:return np.array([2.**600*(1.+e)]),np.array([2.**-700*(1.+e)]),(np.array([2.**-100*(1.+2.**-51)]),np.array([2.**-204]))
 if case==4:return np.array([[2.**-600],[2.**600]]),np.array([[0.,-0.]]),(np.array([[0.,-0.],[0.,-0.]]),np.zeros((2,2)))
 assert case==5;return np.array([2.**-1074]),np.array([2.**-1074]),None
def authenticated_failed_case():
 name='CLOSED_FINITE0_FAILED_PRODUCT_INPUTS_V001.json';d=json.loads((BASE/name).read_text())
 assert d['status']=='SAVED_FAILED_PRODUCT_OPERANDS_EXACT_IDENTITY' and d['no_action_or_fixture_replay'] is True
 assert d['file']=='CLOSED_FINITE0_FAILED_PRODUCT_INPUTS_V001.npz' and d['sha256']==PINS[d['file']]
 assert d['original_product_order']==['denominator','failed_quotient'] and d['shape']==[32,3784]
 assert d['matched_failed_quotient']=='row0_jet0_native_EH_quotient_test_first_0_value_correction_0_second_quotient'
 assert d['exact_quotient_matches']==[d['matched_failed_quotient']] and d['parent_error_raw']['metadata']['owner']['pid']==94049 and d['parent_error_raw']['metadata']['failed'] is True
 with np.load(BASE/d['file'],allow_pickle=False) as z:
  assert set(z.files)=={'x','y'};x=z['x'].copy();y=z['y'].copy()
 assert x.shape==y.shape==(32,3784) and x.dtype==y.dtype==np.float64
 return x,y,dict(binding_file=name,binding_sha256=PINS[name],failed_product_file=d['file'],failed_product_sha256=d['sha256'],parent_error_raw={n:d['parent_error_raw'][n] for n in ('file','sha256','commit_file','commit_sha256')},original_failed_status_preserved=True)
def main():
 global np,P,ARITH_SCOPE
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and not list(BASE.glob(STEM+'_*')),'Root reviewed exclusive release required'
 assert PROTOCOL_SHA is not None and sha(DRIVER_PROTOCOL)==PROTOCOL_SHA
 for name,h in PINS.items():assert sha(name)==h,name
 import numpy as numpy
 np=numpy;file=next(iter(PINS));names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==12
 ARITH_SCOPE=dict(np=np,DD_ARRAY_CURRENT={});exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),ARITH_SCOPE);P=types.SimpleNamespace(**{n:ARITH_SCOPE[n] for n in names})
 file=list(PINS)[1];tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==2
 exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals());old=install_exact_exponent_product(ARITH_SCOPE,P,keep,'balanced_product')
 for case in range(1,7):
  metadata=dict(fresh=case<6,physical_or_action_admission=False)
  if case<6:x,y,declared=fresh_case(case)
  else:x,y,metadata=authenticated_failed_case();declared=None
  keep('original_product_x',x);keep('original_product_y',y)
  if declared is not None:words('predeclared_exact_dyadic_product',declared)
  if case==5:
   rejected=False
   try:P.a_prod(x,y)
   except AssertionError as exc:rejected=str(exc)=='Exponent-balanced product restoration lost a word';metadata['expected_refusal']=str(exc)
   expected=Fraction(1,2**2148);metadata['exact_nonzero_product']=dict(numerator=str(expected.numerator),denominator=str(expected.denominator))
   record_control('case5_genuine_underflow_refusal_and_completed_word_custody',[rejected,'balanced_product_restoration_attempt_all_words' in RAW,expected>0]);save_case(case,metadata);continue
  actual=words('completed_product',P.a_prod(x,y));expected,exact=fraction_product_reference(x,y,actual)
  predicates=[exact,all(np.array_equal(actual[w],expected[w]) for w in (0,1))]
  if case==1:
   inherited=words('inherited_same_fresh_input_product',old(x,y));predicates.append(all(np.array_equal(actual[w],inherited[w]) for w in (0,1)))
  if declared is not None:predicates.append(all(np.array_equal(actual[w],declared[w]) for w in (0,1)))
  if case==4:predicates.append(np.array_equal(np.signbit(actual[0]),np.signbit(declared[0])))
  metadata.update(exact_Fraction_product_identity=True,expected_pair_definition='high=float(Fraction(x)*Fraction(y));low=float(exact_product-Fraction(high))',entries=int(actual[0].size))
  record_control('case%d_exact_product_words_and_Fraction_identity'%case,predicates);save_case(case,metadata)
 assert len(CONTROLS)==6 and all(c['passed'] for c in CONTROLS)
 for name,h in PINS.items():assert sha(name)==h,name
 assert sha(DRIVER_PROTOCOL)==PROTOCOL_SHA
 report=dict(status='EXACT_EXPONENT_TWO_PRODUCT_FRESH_AND_CLOSED_OPERAND_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),protocol_sha256=PROTOCOL_SHA,pins=PINS,controls=CONTROLS,cases=CASES,original_finite0_failure_preserved=True,old_candidate_state_action_fixture_EOS_or_ordinary_replayed=False,physical_or_constraint_qualification=False)
 name=STEM+'_RESULT.json'
 with (BASE/name).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=6,sha256=sha(name))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for name,x in ARITH_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+name]=np.asarray(x).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
