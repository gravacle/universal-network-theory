"""HELD fresh fixed-canonical ordinary controls; root alone owns execution.
Independent Fraction targets use the three registered arithmetic cases only.
No source labels, old fixtures, quadrature, volume or producer are evaluated.
"""
from pathlib import Path
from fractions import Fraction
import ast,hashlib,json,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='FINITE_FIXED_CANONICAL_ORDINARY_CONTROLS_V002'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'FINITE_FIXED_CANONICAL_ORDINARY_POINT_CORE_V001.md':'14813daec5acdba28447d8c6118f0bc7c2d8e760e709ff099f21854205e1aed8'}
np=P=None;ARITH_SCOPE={};RAW={};CASES=[];CONTROLS=[]

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def pair(high,low=None):
 h=np.asarray(high,dtype=np.float64);l=np.zeros_like(h) if low is None else np.asarray(low,dtype=np.float64)
 assert h.shape==l.shape;return h.copy(),l.copy()
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def capture_inputs(prefix,values):
 for name,value in values.items():
  if name=='provenance':continue
  if isinstance(value,dict):capture_inputs(prefix+name+'_',value)
  elif isinstance(value,tuple):keep(prefix+name+'_hi',value[0]);keep(prefix+name+'_lo',value[1])
  else:keep(prefix+name,value)
def rational_pair(values,shape):
 # Independent exact rational answer -> nearest high plus its rational remainder.
 h=np.array([float(x) for x in values],dtype=np.float64)
 l=np.array([float(x-Fraction.from_float(float(a))) for x,a in zip(values,h)],dtype=np.float64)
 return h.reshape(shape),l.reshape(shape)
def case_inputs(case):
 e=2.**-60;h=np.eye(3)[None];dh=np.zeros((1,3,3));dh[0,0,0]=-.5
 geometry=dict(h=pair(h),ih=pair(h),delta_h=pair(dh),delta_ih=pair(-dh))
 gauge=dict(N=pair([2.]),beta=pair([[.25,0.,0.]]))
 mass=2. if case in (1,3) else 0.;dust=3. if case in (2,3) else 0.
 rays=np.array([[[3.,4.,0.]],[[-3.,-4.,0.]]]) if case in (2,3) else np.zeros((0,1,3))
 weight=np.full((len(rays),1),.125)
 labels=dict(galaxy_mass_weight=pair([mass],[mass*e]),galaxy_specific_covector=pair([[.75,0.,0.]]),
  reference_dust_energy_weight=pair([dust]),radiation_weights=pair(weight,weight*e),radiation_covectors=pair(rays),
  existing_once_counted_branch_registered=True,provenance=dict(kind='NEW_independent_analytic_inventory_control',actual_source_inventory_evaluated=False))
 return geometry,gauge,labels
def known_answers(case):
 e=Fraction(1,2**60);v=1+e;F=Fraction
 # Literal independent tables from the point-core protocol; no tested formula here.
 if case==1:E=F(5,2)*v;M=F(3,2)*v;rr=F(9,10)*v;rz=zz=F(0);dE=F(9,40)*v;drr=F(819,1000)*v;drz=dzz=F(0);H=F(37,8)*v;dH=F(9,20)*v
 elif case==2:E=F(17,4)+F(5,4)*e;M=F(0);rr=F(9,20)*v;rz=F(3,5)*v;zz=F(4,5)*v;dE=F(9,80)*v;drr=F(819,2000)*v;drz=F(123,500)*v;dzz=-F(9,125)*v;H=F(17,2)+F(5,2)*e;dH=F(9,40)*v
 else:assert case==3;E=F(27,4)+F(15,4)*e;M=F(3,2)*v;rr=F(27,20)*v;rz=F(3,5)*v;zz=F(4,5)*v;dE=F(27,80)*v;drr=F(2457,2000)*v;drz=F(123,500)*v;dzz=-F(9,125)*v;H=F(105,8)+F(57,8)*e;dH=F(27,40)*v
 Z=F(0);S=[rr,rz,Z,rz,zz,Z,Z,Z,Z];dS=[drr,drz,Z,drz,dzz,Z,Z,Z,Z]
 value=dict(energy=rational_pair([E],(1,)),momentum=rational_pair([M,Z,Z],(1,3)),stress=rational_pair(S,(1,3,3)),normal_density=rational_pair([E,-M,Z,Z],(1,4)),metric_force=rational_pair(S,(1,3,3)),Hamiltonian=rational_pair([H],(1,)))
 delta=dict(energy=rational_pair([dE],(1,)),momentum=rational_pair([Z,Z,Z],(1,3)),stress=rational_pair(dS,(1,3,3)),normal_density=rational_pair([dE,Z,Z,Z],(1,4)),metric_force=rational_pair(dS,(1,3,3)),Hamiltonian=rational_pair([dH],(1,)))
 return value,delta
def check(name,actual,expected,bound,exact=False):
 assert actual[0].shape==actual[1].shape==expected[0].shape==expected[1].shape
 envelope=np.full(actual[0].shape,float(bound))+abs(expected[0])+abs(expected[1]);assert np.all(envelope>0)
 for key,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(name+'_'+key,x)
 gap=P.a_sub(actual,expected);keep(name+'_gap_hi',gap[0]);keep(name+'_gap_lo',gap[1])
 error=float(np.max(abs(gap[0]+gap[1])/envelope,initial=0));word=not exact or all(np.array_equal(actual[i],expected[i]) for i in (0,1));keep(name+'_exact_word_predicate',np.asarray(word))
 CONTROLS.append(dict(name=name,error=error,tolerance=2e-11,exact_words=exact,word_predicate=word,passed=error<=2e-11 and word));assert error<=2e-11 and word,(name,error,word)
def save_case(case,provenance):
 name=STEM+'_CASE'+str(case)+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/name).chmod(0o444);CASES.append(dict(case=case,file=name,sha256=sha(name),fields=len(RAW),provenance=provenance,source_inventory_admission_performed=False));RAW.clear()
def main():
 global np,P,ARITH_SCOPE
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and not list(BASE.glob(STEM+'_*')),'Root reviewed exclusive release required'
 for name,h in PINS.items():assert sha(name)==h,name
 import numpy as numpy
 np=numpy;arithmetic=next(iter(PINS));names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 tree=ast.parse((BASE/arithmetic).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==12
 ARITH_SCOPE=dict(np=np,DD_ARRAY_CURRENT={});exec(compile(ast.Module(body=defs,type_ignores=[]),arithmetic,'exec'),ARITH_SCOPE);P=types.SimpleNamespace(**{n:ARITH_SCOPE[n] for n in names})
 for file in list(PINS)[1:4]:
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 bounds=dict(energy=16,momentum=8,stress=8,normal_density=16,metric_force=8,Hamiltonian=32)
 for case in (1,2,3):
  geometry,gauge,labels=case_inputs(case);expected,expected_delta=known_answers(case)
  capture_inputs('fresh_',dict(geometry=geometry,gauge=gauge,labels=labels,expected=expected,expected_delta=expected_delta))
  result=finite_fixed_canonical_ordinary_point(geometry,gauge,labels,keep,'case'+str(case));capture_inputs('completed_',dict(value=result['value'],delta=result['delta'],energy_metric_direction_contact=result['energy_metric_direction_contact']))
  for name,bound in bounds.items():
   check('case%d_value_%s'%(case,name),result['value'][name],expected[name],bound,name in ('energy','momentum','normal_density','Hamiltonian'))
   check('case%d_direction_%s'%(case,name),result['delta'][name],expected_delta[name],bound,name=='momentum')
  check('case%d_energy_metric_contact'%case,result['energy_metric_direction_contact'],pair([0.]),16)
  assert result['existing_labels_and_mean_weights_unchanged'] and not result['extra_volume_factor_or_budget_subtraction_introduced'] and not result['physical_adoption']
  save_case(case,labels['provenance'])
 assert len(CONTROLS)==39 and all(x['passed'] for x in CONTROLS)
 for name,h in PINS.items():assert sha(name)==h,name
 report=dict(status='NEW_FINITE_FIXED_CANONICAL_ORDINARY_ANALYTIC_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),pins=PINS,controls=CONTROLS,cases=CASES,
  only_fresh_three_known_inventories_evaluated=True,source_mean_quadrature_volume_old_fixture_or_producer_replayed=False,actual_source_inventory_admitted=False,physical_or_observational_adoption=False)
 name=STEM+'_RESULT.json'
 with (BASE/name).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=39,sha256=sha(name))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for name,x in ARITH_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():keep('last_arithmetic_'+name,x)
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**RAW)
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
