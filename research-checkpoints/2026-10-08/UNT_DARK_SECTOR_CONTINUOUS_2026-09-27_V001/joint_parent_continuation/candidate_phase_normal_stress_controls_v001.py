"""HELD three fresh phase normal/stress cases; root alone releases and runs.
No old fixture/source/geometry/normal/scatter/operator or physical state replay.
"""
from pathlib import Path
from decimal import Decimal,localcontext
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_PHASE_NORMAL_STRESS_CONTROLS_V001'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'CANDIDATE_INVARIANT_PHASE_EOS_CURRENT_SPEC_V001.txt':'946244eb7f92460026de2979c32edc317b4bd02f37b59a7e959b70ff707c0787',
 'author_fragment_candidate_phase_normal_stress_v001.py':'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd',
 'CANDIDATE_PHASE_NORMAL_STRESS_SPEC_V001.md':'d864cfd8914586b14f22e264996e35d9596a141ca6ad31b96bb174b5f34e93a9'}
np=P=None;PROVIDER_SCOPE={};RAW={};CASES=[];CONTROLS=[]

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def pair(value):
 h=np.asarray(value,dtype=np.float64);return h.copy(),np.zeros_like(h)
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def capture(prefix,values):
 for n,x in values.items():
  if isinstance(x,dict):capture(prefix+n+'_',x)
  elif isinstance(x,tuple):keep(prefix+n+'_hi',x[0]);keep(prefix+n+'_lo',x[1])
  else:keep(prefix+n,x)

def fresh_inputs(case):
 g=pair(np.diag([-1.,1.,1.,1.])[None]);I=pair(np.diag([-1.,1.,1.,1.])[None]);U=pair([[1.,0.,0.,0.]]);uc=pair([[-1.,0.,0.,0.]])
 projector=pair(np.diag([0.,1.,1.,1.])[None]);phi=pair([[5/4,0.,0.,0.]])
 if case==2:phi=pair([[25/16,15/16,0.,0.]])
 if case==3:
  U=pair([[5/4,3/4,0.,0.]]);uc=pair([[-5/4,3/4,0.,0.]])
  projector=pair(np.array([[[-9/16,-15/16,0.,0.],[15/16,25/16,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]]]))
 s=dict(g=g,hi=I,U=U,uc=uc,P=projector,phi=phi)
 c=dict(N=pair([1.]),mu=pair([1.]),h=pair(np.eye(3)[None]),beta=pair([[0.,0.,0.]]),ih=pair(np.eye(3)[None]),u=pair([[3/4 if case==3 else 0.,0.,0.]]))
 d={n:pair(np.zeros_like(x[0])) for n,x in dict(s,**c).items()}
 if case in (1,2):d['phi'][0][0,0]=1.
 else:
  d['N'][0][0]=.5;d['g'][0][0,0,0]=-1.;d['hi'][0][0,0,0]=1.
  d['U'][0][0,0]=d['uc'][0][0,0]=-5/8;d['P'][0][0,0,1]=d['P'][0][0,1,0]=-15/32
 constants=dict(eps=1.,norm=1.-math.log1p(1.),X0=1.,A0=1.,C=1.98,synthetic_control=True,relative_phase_coefficient=1.,physical_constants_selected_or_fitted=False)
 return s,c,d,constants

def independent_targets(case):
 with localcontext() as context:
  context.prec=100;D=Decimal;n=1-D(2).ln();pressure=((D(16)/7).ln()-D(9)/16)/n-1;PX=D(45)/(14*n);PXX=D(1726)/(49*n)
  values=[[D(0) for _ in range(4)] for _ in range(4)];directions=[[D(0) for _ in range(4)] for _ in range(4)]
  if case==1:values[0][:2]=[pressure-D(5)*PX/4,D(0)];directions[0][:2]=[-D(5)*PXX/4,D(0)]
  elif case==2:
   values[0][:2]=[pressure-D(125)*PX/64,-D(225)/512];directions[0][:2]=[D(45)*PX/64-D(625)*PXX/256,D(0)]
   values[1][:2]=[-D(75)*PX/64,D(0)];directions[1][:2]=[D(27)*PX/64-D(375)*PXX/256,D(0)]
  else:values[0][:2]=[pressure-D(5)*PX/4,D(225)/512];directions[0][:2]=[D(25)*PXX/32,-D(225)/512]
  for table in (values,directions):
   for row in table:row[2]=row[0]+row[1];row[3]=-row[2]
  flat=[x for table in (values,directions) for row in table for x in row]
  high=[float(x) for x in flat];low=[float(x-D.from_float(h)) for x,h in zip(flat,high)]
  return np.asarray(high,dtype=np.float64).reshape(2,4,4),np.asarray(low,dtype=np.float64).reshape(2,4,4)

def check(name,actual,expected):
 envelope=np.full((2,4,4),768.)+abs(expected[0])+abs(expected[1])
 for n,v in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(name+'_'+n,v)
 assert all(x.shape==(2,4,4) for x in (*actual,*expected))
 gap=P.a_sub(actual,expected);keep(name+'_gap_hi',gap[0]);keep(name+'_gap_lo',gap[1])
 error=float(np.max((abs(gap[0])+abs(gap[1]))/envelope,initial=0));row=dict(name=name,error=error,tolerance=2e-11,passed=error<=2e-11);CONTROLS.append(row);assert row['passed'],row

def save_case(case):
 name=STEM+'_CASE'+str(case)+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/name).chmod(0o444);CASES.append(dict(case=case,file=name,sha256=sha(name),fields=len(RAW)));RAW.clear()

def main():
 global np,P,PROVIDER_SCOPE
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and not list(BASE.glob(STEM+'_*')),'Root exclusive reviewed release required'
 for n,h in PINS.items():assert sha(n)==h,n
 import numpy as numpy
 np=numpy;names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 file=next(iter(PINS));tree=ast.parse((BASE/file).read_text());selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(selected)==12
 PROVIDER_SCOPE=dict(np=np,DD_ARRAY_CURRENT={});exec(compile(ast.Module(body=selected,type_ignores=[]),file,'exec'),PROVIDER_SCOPE);P=types.SimpleNamespace(**{n:PROVIDER_SCOPE[n] for n in names})
 for file in ('author_fragment_finite_york_geometry_target_v001.py','author_fragment_finite_york_spacetime_first_jets_v001.py','author_fragment_candidate_invariant_phase_eos_current_v001.py','author_fragment_candidate_phase_normal_stress_v001.py'):
  tree=ast.parse((BASE/file).read_text());definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=definitions,type_ignores=[]),file,'exec'),globals())
 for case in (1,2,3):
  s,c,d,constants=fresh_inputs(case);expected=independent_targets(case);capture('new_input_',dict(s=s,c=c,direction=d));capture('new_constants_',constants);capture('independent_',dict(expected=expected))
  eos=candidate_invariant_phase_eos_current(s,c,d,constants,keep,'new_case%d_eos'%case);capture('completed_EOS_',dict(value=eos['value'],delta=eos['delta'],PXXX=eos['PXXX']))
  rows=[]
  for test in range(4):
   f=np.array([1. if test==0 else 0.]);b=np.zeros((1,3))
   if test:b[0,test-1]=1.
   capture('new_test%d_'%test,dict(f=f,b=b));out=candidate_phase_normal_stress(s,c,d,eos,f,b,keep,'new_case%d_test%d'%(case,test))
   capture('completed_test%d_'%test,dict(value=out['value'],delta=out['delta']))
   scope=out['relative_phase_included_once'] and out['test_first_derivative_coefficients_zero'] and not out['global_weak_rows_assembled'] and not out['finite_candidate_physically_admitted'] and not eos['elementary_log_accuracy_admitted']
   keep('completed_test%d_scope_predicate'%test,np.asarray(scope));assert scope
   rows.append(out)
  keys=('absolute','relative','action','hamiltonian');tables=[]
  for family in ('value','delta'):
   tables.append(P.a_stack([P.a_stack([P.a_slice(out[family][n],0) for n in keys],0) for out in rows],0))
  actual=P.a_stack(tables,0);capture('completed_packed_',dict(coefficients=actual));check('case%d_lapse_and_three_shift_values_and_directions'%case,actual,expected);save_case(case)
 assert len(CONTROLS)==3 and len(CASES)==3 and all(x['passed'] for x in CONTROLS)
 for n,h in PINS.items():assert sha(n)==h,n
 report=dict(status='NEW_CANDIDATE_PHASE_NORMAL_STRESS_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),pins=PINS,controls=CONTROLS,cases=CASES,synthetic_EOS_only=True,three_new_cases_four_tests_each=True,old_fixture_or_source_geometry_normal_scatter_operator_replayed=False,transcendental_accuracy_admitted=False,finite_candidate_physically_admitted=False,galaxy_readout_admitted=False)
 name=STEM+'_RESULT.json'
 with (BASE/name).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=3,sha256=sha(name))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for n,x in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+n]=np.asarray(x).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**RAW)
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
