"""Guarded fresh independent spacetime/firstjet controls; root owns execution."""
from pathlib import Path
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='FINITE_YORK_SPACETIME_FIRST_JET_CONTROLS_V001'
ARITHMETIC='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
ARITHMETIC_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
GEOMETRY='author_fragment_finite_york_geometry_target_v001.py'
GEOMETRY_SHA='12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70'
KERNEL='author_fragment_finite_york_spacetime_first_jets_v001.py'
KERNEL_SHA='aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d'
PROTOCOL='CROSS_U_FINITE_YORK_SPACETIME_FIRST_JETS_CORE_V001.md'
PROTOCOL_SHA='587f4bc5b8fc954b5c2b8376734c747e3d3f1b8b09a484f9c5f71cb3c7663fde'
DRIVER_PROTOCOL='FINITE_YORK_SPACETIME_FIRST_JET_CONTROLS_V001.md'
DRIVER_PROTOCOL_SHA='3d11ccbd38b8cf1233acab47ead0527dd9de3551c8bbb558153d37b56984258c'
np=P=None;ARITH_SCOPE={};RAW={};CONTROLS=[];CASES=[]

def sha(n):return hashlib.sha256((BASE/n).read_bytes()).hexdigest()
def pair(x,time_words=False):
 a=np.asarray(x,dtype=float);return a.copy(),a*2.**-60 if time_words else np.zeros_like(a)
def keep(n,x):
 a=np.asarray(x).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[n]=a;return a
def capture_inputs(prefix,d):
 for n,x in d.items():
  if isinstance(x,dict):capture_inputs(prefix+n+'_',x)
  elif isinstance(x,tuple):keep(prefix+n+'_hi',x[0]);keep(prefix+n+'_lo',x[1])
  else:keep(prefix+n,x)

def check(label,actual,expected,operation_bound,exact=False):
 envelope=np.full(actual[0].shape,float(operation_bound))+abs(expected[0])+abs(expected[1])
 for n,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(label+'_'+n,x)
 assert actual[0].shape==actual[1].shape==expected[0].shape==expected[1].shape and np.all(envelope>0)
 gap=P.a_sub(actual,expected);keep(label+'_gap_hi',gap[0]);keep(label+'_gap_lo',gap[1]);error=float(np.max(abs(gap[0]+gap[1])/envelope,initial=0))
 word_pass=not exact or all(np.array_equal(actual[w],expected[w]) for w in (0,1));keep(label+'_word_predicate',np.asarray(word_pass))
 CONTROLS.append(dict(name=label,error=error,tolerance=2e-11,exact_words=exact,word_predicate=word_pass,passed=error<=2e-11 and word_pass));assert error<=2e-11 and word_pass,(label,error,word_pass)

def answers(time,E=False):
 g=np.diag([-3.,16.,16.,16.])[None];g[0,0,1]=g[0,1,0]=4.
 hi=np.diag([-.25,3/64,1/16,1/16])[None];hi[0,0,1]=hi[0,1,0]=1/16
 z=np.zeros((32,1,4));z[0,0]=[-.1,2.,0.,0.]
 dg=np.zeros((1,4,4,4));du=np.zeros((1,4,4));dz=np.zeros((32,1,4,4));Ga=np.zeros((1,4,4,4));dGa=Ga.copy()
 if time:
  dg[0,0,0,0]=.5;dg[0,0,0,1]=dg[0,0,1,0]=2.;dg[0,0,1,1]=8.
  du[0,0,:2]=[-3/160,-37/640];dz[0,0,0,:2]=[339/2000,.25]
  for m,a,b,v in ((0,0,0,1/16),(1,0,0,7/64),(0,0,1,.25),(0,1,0,.25),(1,0,1,3/16),(1,1,0,3/16),(0,1,1,1.),(1,1,1,-.25)):Ga[0,m,a,b]=v
  dGa[0,1,0,0]=-1/16;dGa[0,1,0,1]=dGa[0,1,1,0]=-.125
 result=dict(g=pair(g),hi=pair(hi),U=pair(np.array([[5/8,1/32,0.,0.]])),z=pair(z),up=pair(np.array([[3/16,0.,0.]])),gamma=pair(np.array([5/4])),dens=pair(np.array([128.])),dg=pair(dg,time),du=pair(du,time),dz=pair(dz,time),Ga=pair(Ga,time),delta_Ga=pair(dGa,time))
 if E:
  for m,a,b,v,dv in ((2,1,2,-1/16,1/32),(2,2,1,-1/16,1/32),(0,2,2,1/16,0.),(1,2,2,3/64,-1/32)):
   result['Ga'][0][0,m,a,b]=v;result['delta_Ga'][0][0,m,a,b]=dv
 return result

def case_inputs(case):
 time=case!=1;E=case==3;h=np.eye(3)[None]*16.;I=np.eye(3)[None]/16
 geometry=dict(h=pair(h),ih=pair(I),mu=pair(np.array([64.])),delta_h=pair(h/2),delta_ih=pair(-I/2),delta_mu=pair(np.array([48.])),h_spatial_jets=pair(np.zeros((1,2,3,3))),delta_h_spatial_jets=pair(np.zeros((1,2,3,3))))
 conformal={'lambda':pair(np.array([16.])),'rho_gradient':pair(np.zeros((1,2)))}
 gauge=dict(N=pair(np.array([2.])),beta=pair(np.array([[.25,0.,0.]])),N_jets=pair(np.zeros((1,4))),beta_jets=pair(np.zeros((1,4,3))))
 u=np.array([[3.,0.,0.]]);z=np.zeros((32,1,3));z[0,0,0]=2.;uj=np.zeros((1,4,3));zj=np.zeros((32,1,4,3));ht=np.zeros((1,3,3))
 if time:uj[0,0,0]=.5;zj[0,0,0,0]=.25;ht[0,0,0]=8.
 covectors=dict(u=pair(u),z=pair(z),u_jets=pair(uj,time),z_jets=pair(zj,time));mechanical=dict(h_dot=pair(ht,time))
 direction=dict(rho=pair(np.array([.125])),rho_gradient=pair(np.zeros((1,2))),u_jets=pair(np.zeros_like(uj)),z_jets=pair(np.zeros_like(zj)),h_dot=pair(np.zeros_like(ht)))
 expected=answers(time,E);reference={n:tuple(w.copy() for w in expected[n]) for n in ('g','hi','U','z','du','dz','dg','Ga')}
 reference.update(physical_spatial_inverse=pair(np.eye(3)[None]),h_spatial_jets=pair(np.zeros((1,2,3,3))),E0=pair(np.zeros((1,4,4,4))))
 if E:
  reference['E0'][0][0,1,2,2]=2.;reference['hi'][0][0,1,1]+=.125;reference['du'][0][0,0,1]+=.0625;reference['Ga'][0][0,2,1,2]+=.03125
 return geometry,conformal,gauge,covectors,mechanical,direction,reference,expected

def save_case(name):
 file=STEM+'_'+name+'.npz'
 with (BASE/file).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/file).chmod(0o444);CASES.append(dict(name=name,file=file,sha256=sha(file),fields=len(RAW),physical_adoption=False));RAW.clear()

def main():
 global np,P,ARITH_SCOPE
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and not list(BASE.glob(STEM+'_*')),'Root reviewed exclusive release required'
 for n,h in ((ARITHMETIC,ARITHMETIC_SHA),(GEOMETRY,GEOMETRY_SHA),(KERNEL,KERNEL_SHA),(PROTOCOL,PROTOCOL_SHA),(DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA)):assert sha(n)==h
 import numpy as numpy
 np=numpy;names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'};tree=ast.parse((BASE/ARITHMETIC).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==12
 ARITH_SCOPE=dict(np=np,DD_ARRAY_CURRENT={});exec(compile(ast.Module(body=defs,type_ignores=[]),ARITHMETIC,'exec'),ARITH_SCOPE);P=types.SimpleNamespace(**{n:ARITH_SCOPE[n] for n in names})
 for file in (GEOMETRY,KERNEL):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 for case in (1,2,3):
  geometry,conformal,gauge,covectors,mechanical,direction,reference,expected=case_inputs(case)
  capture_inputs('fresh_input_',dict(geometry=geometry,conformal=conformal,gauge=gauge,covectors=covectors,mechanical=mechanical,direction=direction,reference=reference,expected=expected))
  out=finite_york_spacetime_first_jets(geometry,conformal,gauge,covectors,mechanical,direction,reference,keep,'fresh_case_'+str(case));capture_inputs('completed_',dict(value=out['value'],delta=out['delta']))
  for n,b in (('g',32),('hi',2),('U',4),('z',8),('up',2),('gamma',4),('dens',256),('dg',32),('du',8),('dz',8),('Ga',16)):check('case%d_primal_%s'%(case,n),out['value'][n],expected[n],b,exact=n in ('dg','Ga'))
  dz=np.zeros((32,1,4));dz[0,0,0]=123/500
  contacts=dict(up=np.array([[-3/32,0.,0.]]),gamma=np.array([-9/80]),U=np.array([[-9/160,-51/640,0.,0.]]),z=dz)
  for n,x in contacts.items():check('case%d_direction_%s'%(case,n),out['delta'][n],pair(x),8)
  check('case%d_direction_Gamma'%case,out['delta']['Ga'],expected['delta_Ga'],16,True)
  if case!=1:
   du=np.zeros((1,4,4));du[0,0,:2]=[573/16000,4427/64000];dzj=np.zeros((32,1,4,4));dzj[0,0,0,0]=-16111/100000
   check('case%d_direction_time_U'%case,out['delta']['du'],pair(du,True),8);check('case%d_direction_time_z'%case,out['delta']['dz'],pair(dzj,True),8)
  for n in ('unit_constraint','transverse_constraint','unit_first_constraint','transverse_first_constraint','compatibility_minus_fixed_E0'):
   for delta in ('','_delta'):
    actual=tuple(RAW['fresh_case_%d_%s%s_%s'%(case,n,delta,w)] for w in ('hi','lo'));check('case%d_identity_%s%s'%(case,n,delta),actual,pair(np.zeros_like(actual[0])),128)
  save_case('CASE%d'%case)
 report=dict(status='NEW_FINITE_SPACETIME_FIRST_JET_ANALYTIC_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),kernel_sha256=KERNEL_SHA,geometry_definitions_sha256=GEOMETRY_SHA,arithmetic_sha256=ARITHMETIC_SHA,protocol_sha256=PROTOCOL_SHA,driver_protocol_sha256=DRIVER_PROTOCOL_SHA,controls=CONTROLS,cases=CASES,only_fresh_exact_geometry_and_inputs_evaluated=True,old_geometry_fixtures_payload_action_operator_or_solver_replayed=False,candidate_action_or_physical_adoption=False)
 file=STEM+'_RESULT.json'
 with (BASE/file).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/file).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=report['pid'],controls=len(CONTROLS),sha256=sha(file))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for n,x in ARITH_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():keep('last_arithmetic_'+n,x)
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**RAW)
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
