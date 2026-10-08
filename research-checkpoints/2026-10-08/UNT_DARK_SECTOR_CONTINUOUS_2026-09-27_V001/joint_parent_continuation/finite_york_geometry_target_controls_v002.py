"""Guarded fresh analytic finite geometry/target controls; root owns release."""
from pathlib import Path
import ast,hashlib,json,math,os,types,traceback
from fractions import Fraction
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
STEM='FINITE_YORK_GEOMETRY_TARGET_CONTROLS_V002'
KERNEL='author_fragment_finite_york_geometry_target_v001.py'
KERNEL_SHA='12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70'
PROTOCOL='CROSS_U_FINITE_YORK_GEOMETRY_TARGET_CORE_V001.md'
PROTOCOL_SHA='78343a0dd54df5d9363eff47ca97f6beaf02ab3442eed61c6d968d21979ce6c4'
ARITHMETIC='cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py'
ARITHMETIC_SHA='5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18'
np=P=None
RAW={};CONTROLS=[];CASES=[]

def sha(n):return hashlib.sha256((BASE/n).read_bytes()).hexdigest()
def keep(n,x):
 a=np.asarray(x).copy();assert a.dtype.kind in 'fiu' and np.all(np.isfinite(a));RAW[n]=a;return a

def pair(x,epsilon=False):
 a=np.asarray(x,dtype=float);return a.copy(),a*math.ldexp(1.,-60) if epsilon else np.zeros_like(a)

def check(label,actual,expected,envelope,exact=False):
 for name,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(label+'_'+name,x)
 assert actual[0].shape==actual[1].shape==expected[0].shape==expected[1].shape==np.shape(envelope) and np.all(envelope>0)
 gap=P.a_sub(actual,expected);keep(label+'_gap_hi',gap[0]);keep(label+'_gap_lo',gap[1]);error=float(np.max(abs(gap[0]+gap[1])/envelope,initial=0))
 if exact:assert all(np.array_equal(actual[w],expected[w]) for w in (0,1)),label
 CONTROLS.append(dict(name=label,error=error,tolerance=2e-11,exact_word_equality=exact,passed=error<=2e-11));assert error<=2e-11,(label,error)

def reference(defect=False):
 h=np.eye(3)[None] if defect else np.diag([1.,4.,9.])[None]
 inverse=np.diag([2.,1.,1.])[None] if defect else np.diag([1.,.25,1/9])[None]
 maps=np.zeros((1,3,3,3,3));maps[0,0,0,0,0]=.25 if defect else 0.;maps[0,0,0,1,1]=-1. if defect else 0.
 return dict(h=h,h_spatial_jets=pair(np.zeros((1,2,3,3))),ih_owned=inverse,mu_owned=np.array([1. if defect else 6.]),target_raising_inverse=inverse.copy(),Pi_owned=pair(np.diag([4.,2.,3.])[None],True) if defect else pair(np.zeros((1,3,3))),T_owned=pair(np.diag([-2.,-1.,0.])[None],True) if defect else pair(np.zeros((1,3,3))),tau_owned=pair(np.array([9.]),True) if defect else pair(np.zeros(1)),L_maps=pair(maps))

def fraction_pair(x,index):return Fraction.from_float(float(x[0][index]))+Fraction.from_float(float(x[1][index]))
def independent_contract(a,b):return sum((fraction_pair(a,(0,i,j))*fraction_pair(b,(0,i,j)) for i in range(3) for j in range(3)),Fraction(0))
def fraction_check(label,actual,expected,bound):
 error=float(abs(actual-expected)/bound);CONTROLS.append(dict(name=label,error=error,tolerance=2e-11,exact_serialized_fraction_contact=True,passed=error<=2e-11));keep(label+'_fraction_gap',np.asarray(float(actual-expected)));keep(label+'_fraction_bound',np.asarray(float(bound)));assert error<=2e-11,(label,error)

def save_case(name,meta):
 file=STEM+'_'+name+'.npz'
 with (BASE/file).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/file).chmod(0o444);CASES.append(dict(name=name,file=file,sha256=sha(file),fields=len(RAW),metadata=meta));RAW.clear()

def main():
 global np,P
 assert AUTHOR_DRAFT is False and not list(BASE.glob(STEM+'_*')),'Root reviewed exclusive release required'
 assert sha(KERNEL)==KERNEL_SHA and sha(PROTOCOL)==PROTOCOL_SHA and sha(ARITHMETIC)==ARITHMETIC_SHA
 import numpy as numpy
 np=numpy;tree=ast.parse((BASE/ARITHMETIC).read_text());names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'};defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==len(names)
 scope=dict(np=np,DD_ARRAY_CURRENT={});exec(compile(ast.Module(body=defs,type_ignores=[]),ARITHMETIC,'exec'),scope);P=types.SimpleNamespace(**{n:scope[n] for n in names})
 exec(compile((BASE/KERNEL).read_text(),KERNEL,'exec'),globals())
 eps=Fraction(1,2**60)
 for case in (1,2,3):
  ref=reference(case!=1);rho=pair(np.array([math.log(2.) if case!=2 else 0.]));grad=pair(np.array([[.25,-.125]]) if case==1 else np.zeros((1,2)));W=pair(np.zeros((1,3,3)));t=pair(np.zeros(1))
  direction=dict(rho=pair(np.array([.125 if case!=2 else 0.])),rho_gradient=pair(np.array([[-.0625,.03125]]) if case==1 else np.zeros((1,2))),W_jet=pair(np.zeros((1,3,3))),t=pair(np.zeros(1)))
  if case==3:
   W[0][0,0,0]=1.;W[1][0,0,0]=2.**-60;t=pair(np.array([3.]),True);direction['W_jet'][0][0,0,0]=2.;direction['W_jet'][1][0,0,0]=2.**-59;direction['t']=pair(np.array([6.]),True)
  for n,x in ref.items():
   if isinstance(x,tuple):keep('input_ref_'+n+'_hi',x[0]);keep('input_ref_'+n+'_lo',x[1])
   else:keep('input_ref_'+n,x)
  out=finite_york_geometry_target(ref,rho,grad,W,t,direction,keep,'fresh_case_'+str(case))
  keep('completed_h_hi',out['h'][0]);keep('completed_h_lo',out['h'][1])
  if case==1:
   h=np.diag([16.,64.,144.])[None];inverse=np.diag([1/16,1/64,1/144])[None]
   answers={'h':h,'ih':inverse,'mu':np.array([384.]),'delta_h':h/2,'delta_ih':-inverse/2,'delta_mu':np.array([288.]),'h_spatial_jets':np.stack((h,h*-.5),axis=1),'delta_h_spatial_jets':np.stack((h/4,-h/8),axis=1)}
   for n,answer in answers.items():check('finite_analytic_'+n,out[n],pair(answer),np.full(answer.shape,2*max(float(np.max(abs(answer))),1.)))
  elif case==2:
   check('owned_anchor_exact_target',out['target'],ref['Pi_owned'],np.full((1,3,3),8.),True);expected=pair(np.diag([2.,-1.,-1.])[None],True);check('owned_anchor_exact_tracefree_offset',out['reference_anchor'],expected,np.full((1,3,3),4.),True)
   check('resolved_physical_inverse_despite_owned_defect',out['ih'],pair(np.eye(3)[None]),np.ones((1,3,3))*2)
  else:
   expected=pair(np.diag([3/8,1/8,1/4])[None],True);check('mixed_finite_target',out['target'],expected,np.ones((1,3,3)))
   expected=pair(np.diag([1/16,-1/16,0.])[None],True);check('mixed_full_target_JVP',out['delta_target'],expected,np.ones((1,3,3)))
   actual=independent_contract(out['h'],out['target']);fraction_check('mixed_actual_trace_retains_low_words',actual,12*(1+eps),24*eps)
   actual=independent_contract(out['delta_h'],out['target'])+independent_contract(out['h'],out['delta_target']);fraction_check('mixed_differentiated_trace_retains_low_words',actual,6*(1+eps),24*eps)
  save_case('CASE%d'%case,dict(control_case=case,source_only_hypothesis_unchanged=True,physical_adoption=False))
 report=dict(status='NEW_FINITE_YORK_GEOMETRY_TARGET_ANALYTIC_CONTROLS_PASS',owner_pid=os.getpid(),source_sha256=sha(Path(__file__).name),kernel_sha256=KERNEL_SHA,arithmetic_sha256=ARITHMETIC_SHA,protocol_sha256=PROTOCOL_SHA,controls=CONTROLS,cases=CASES,only12_authenticated_arithmetic_definitions_loaded=True,old_fixture_producer_feature_operator_solver_or_live_payload_replayed=False,physical_candidate_spacetime_EOS_normal_CMC_or43_admitted=False)
 file=STEM+'_RESULT.json'
 with (BASE/file).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/file).chmod(0o444);print(json.dumps(dict(status=report['status'],pid=os.getpid(),controls=len(CONTROLS),maximum_error=max(q['error'] for q in CONTROLS),sha256=sha(file))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None and RAW:
   with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**RAW)
   (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',owner_pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
