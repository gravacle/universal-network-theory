"""HELD NEW analytic paired invariant phase/EOS controls; root alone executes.
Independent Decimal100 closed targets; no old fixture, physical field or solve.
Inputs, elementary logs, complete outputs, chain contacts and references persist.
"""
from pathlib import Path
from decimal import Decimal,localcontext
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=False
STEM='CANDIDATE_INVARIANT_PHASE_EOS_CURRENT_CONTROLS_V001'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'CANDIDATE_INVARIANT_PHASE_EOS_CURRENT_SPEC_V001.txt':'946244eb7f92460026de2979c32edc317b4bd02f37b59a7e959b70ff707c0787'}
DRIVER_PROTOCOL='CANDIDATE_INVARIANT_PHASE_EOS_CURRENT_CONTROLS_V001.md'
DRIVER_PROTOCOL_SHA='bb06ec1ac23f09ba6a93cbf3c0dc709f0ef63b6d7c8ccee522288faf1efdd8ec'
np=P=None;PROVIDER_SCOPE={};RAW={};CASES=[];CONTROLS=[]

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def pair(value):
 h=np.asarray(value,dtype=np.float64);return h.copy(),np.zeros_like(h)
def capture_tree(prefix,value):
 if isinstance(value,dict):
  for n,x in value.items():capture_tree(prefix+n+'_',x)
 elif isinstance(value,tuple):keep(prefix+'hi',value[0]);keep(prefix+'lo',value[1])
 elif isinstance(value,(int,float,bool)) or hasattr(value,'dtype'):keep(prefix.rstrip('_'),value)

def independent_decimal_reference():
 # Analytic X=5/4 targets, not evaluation of the implementation's u/s algorithm.
 D=Decimal;n=D(1)-D(2).ln();ell=(D(16)/D(7)).ln()
 return dict(norm=n,log_one_plus_s=ell,pressure=(ell-D(9)/D(16))/n-D(1),
             PX=D(45)/(D(14)*n),PXX=D(1726)/(D(49)*n),PXXX=D(154880)/(D(343)*n),
             pressure_envelope=(abs(ell)+D(9)/D(16))/n+D(1))

def fresh_inputs(case):
 hi=np.diag([-1.,1.,1.,1.])[None];U=np.array([[1.,0.,0.,0.]]);uc=-U.copy();projector=np.diag([0.,1.,1.,1.])[None]
 phi=np.array([[5/4,0.,0.,0.]]);u=np.zeros((1,3));N=np.ones(1);mu=np.ones(1)
 s=dict(hi=pair(hi),P=pair(projector),phi=pair(phi),U=pair(U),uc=pair(uc));c=dict(N=pair(N),mu=pair(mu),ih=pair(np.eye(3)[None]),u=pair(u))
 direction={n:pair(np.zeros_like(v[0])) for n,v in dict(s,**c).items()}
 if case==1:direction['phi'][0][0,0]=1.
 elif case==2:
  s['U']=pair([[3/2,1/2,0.,0.]]);s['uc']=pair([[-3/2,1/2,0.,0.]])
  s['P']=pair([[[-5/4,-3/4,0.,0.],[3/4,5/4,0.,0.],[0.,0.,1.,0.],[0.,0.,0.,1.]]]);c['u']=pair([[1/2,0.,0.]])
 elif case==3:
  s['phi']=pair([[25/16,15/16,0.,0.]]);direction['hi'][0][0,0,0]=1.
  direction['phi']=pair([[5/8,5/16,0.,0.]]);direction['N'][0][0]=1/2
  direction['U'][0][0,0]=direction['uc'][0][0,0]=-1/2
 else:
  assert case in (4,5);s['phi']=pair([[1. if case==4 else 3/2,0.,0.,0.]])
 constants=dict(eps=1.,norm=1.-math.log1p(1.),X0=1.,A0=1.,synthetic_control=True,relative_phase_coefficient=1.)
 return s,c,direction,constants

def verify_group(name,entries):
 D=Decimal;actuals=[];expected=[];bounds=[];errors=[];descriptors=[]
 for path,value,target,envelope in entries:
  h,l=value;assert h.shape==l.shape and h.size==len(target)==len(envelope)
  actuals.append(h.reshape(-1));expected.extend(target);bounds.extend(envelope)
  row=[]
  for ah,al,ex,bound in zip(h.reshape(-1),l.reshape(-1),target,envelope):
   actual=D.from_float(float(ah))+D.from_float(float(al));gap=actual-ex
   assert bound>=0;error=abs(gap)/bound if bound else D(0) if not gap else D('Infinity')
   errors.append(error);row.append(dict(actual_two_word_decimal=str(actual),expected_decimal=str(ex),operation_envelope_decimal=str(bound),gap_decimal=str(gap),normalized_error_decimal=str(error)))
  descriptors.append(dict(path=path,entries=row))
 # Persist references and complete contacts before any admission assertion.
 eh=np.array([float(x) for x in expected]);el=np.array([float(x-D.from_float(float(a))) for x,a in zip(expected,eh)])
 keep(name+'_actual_hi',np.concatenate(actuals));keep(name+'_actual_lo',np.concatenate([v[1].reshape(-1) for _,v,_,_ in entries]))
 keep(name+'_expected_hi',eh);keep(name+'_expected_lo',el);keep(name+'_operation_envelope',np.array([float(x) for x in bounds]))
 passed=all(x<=D.from_float(2e-11) for x in errors);error=max(errors,default=D(0))
 CONTROLS.append(dict(name=name,maximum_error_decimal=str(error),tolerance=2e-11,exact_zero_required_if_envelope_zero=True,passed=passed,decimal_contacts=descriptors))
 assert passed,(name,str(error))

def fresh_controls(case,out,r):
 D=Decimal;F=lambda a,b=1:D(a)/D(b);z=D(0);px,xx,xxx,pr=(r[n] for n in ('PX','PXX','PXXX','pressure'))
 v,delta=out['value'],out['delta'];entry=lambda n,ex,b,source=v:(n,source[n],ex,b)
 verify_group('case%d_invariant_clock'%case,[entry(n,[ex],[abs(ex)]) for n,ex in (('X2',F(25,16)),('X',F(5,4)),('q',F(5,4)),('u',F(9,16)),('s',F(9,7)))])
 verify_group('case%d_EOS_Decimal100'%case,[entry('pressure',[pr],[r['pressure_envelope']]),entry('PX',[px],[px]),entry('PXX',[xx],[xx]),('PXXX',out['PXXX'],[xxx],[xxx])])
 if case==1:
  J=[px,z,z,z];eJ=[px,z,z,z];p=px;H=xx;eH=xx;cg=[z]*4;ecg=[2*px,z,z,z];hg=rg=z;ehg=erg=2*xx
  dX=F(1);dP=px;dPX=xx;dXX=xxx;dJ=[xx,z,z,z];edJ=dJ;dp=xx;edp=xx;dH=xxx;edH=xxx
 elif case==2:
  J=[px+F(5,4),z,z,z];eJ=[px+F(85,32),F(75,32),z,z];p=J[0];H=xx+1;eH=xx+F(17,8)
  cg=[F(45,16),F(15,16),z,z];ecg=[2*px+F(45,16),F(105,32),z,z];hg=F(9,4);rg=F(5,4);ehg=2*xx+F(9,4);erg=2*xx+F(5,4)
  dX=dP=dPX=dXX=dp=dH=edp=edH=z;dJ=edJ=[z]*4
 else:
  J=[F(5,4)*px,-F(3,4)*px-F(15,16),z,z];eJ=[J[0],-J[1],z,z];p=J[0];H=F(25,16)*xx-F(9,20)*px;eH=F(25,16)*xx+F(9,20)*px
  cg=[z]*4;ecg=[2*eJ[0],2*eJ[1],z,z];hg=z;rg=F(9,16)*xx-F(9,20)*px;ehg=2*eH;erg=F(9,16)*xx+F(9,20)*px
  dX=-F(55,128);dP=dX*px;dPX=dX*xx;dXX=dX*xxx
  dJ=[-(164*px+275*xx)/512,(165*xx-260*px-160)/512,z,z];edJ=[-dJ[0],(165*xx+260*px+160)/512,z,z]
  dp=(156*px-275*xx)/512;edp=(156*px+275*xx)/512;dH=(356*xx-1104*px-1375*xxx)/2048;edH=(356*xx+1104*px+1375*xxx)/2048
 verify_group('case%d_literal_current_density_H'%case,[entry('J',J,eJ),entry('p',[p],[eJ[0]]),entry('H',[H],[eH])])
 verify_group('case%d_literal_registered_reduced_gaps'%case,[entry('current_gap',cg,ecg),entry('density_gap',[cg[0]],[ecg[0]]),entry('hessian_gap',[hg],[ehg]),entry('reduced_gap',[rg],[erg])])
 verify_group('case%d_full_product_rule_direction'%case,[entry('X',[dX],[abs(dX)],delta),entry('pressure',[dP],[abs(dP)],delta),entry('PX',[dPX],[abs(dPX)],delta),entry('PXX',[dXX],[abs(dXX)],delta),entry('J',dJ,edJ,delta),entry('p',[dp],[edp],delta),entry('H',[dH],[edH],delta)])

def save_case(case):
 name=STEM+'_CASE'+str(case)+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/name).chmod(0o444);CASES[-1].update(file=name,sha256=sha(name),fields=len(RAW));RAW.clear()

def load_definitions():
 global P,PROVIDER_SCOPE
 arith=('a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64')
 path=BASE/list(PINS)[0];tree=ast.parse(path.read_text());defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 PROVIDER_SCOPE=dict(np=np,DD_ARRAY_CURRENT={});exec(compile(ast.Module(body=[defs[n] for n in arith],type_ignores=[]),str(path),'exec'),PROVIDER_SCOPE)
 P=types.SimpleNamespace(**{n:PROVIDER_SCOPE[n] for n in arith})
 fy=('fy_keep','fy_sum','fy_div','fy_sqrt')
 fs=('fs_dual','fs_add','fs_neg','fs_sub','fs_mul','fs_scale','fs_slice','fs_stack','fs_expand','fs_sum','fs_dot','fs_mv','fs_transpose','fs_keep','fs_div','fs_sqrt')
 for file,names in ((list(PINS)[1],fy),(list(PINS)[2],fs),(list(PINS)[3],('candidate_phase_registered_constants','candidate_phase_log1p_dual','candidate_invariant_phase_eos_current'))):
  tree=ast.parse((BASE/file).read_text());defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
  exec(compile(ast.Module(body=[defs[n] for n in names],type_ignores=[]),file,'exec'),globals())

def main():
 global np
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and DRIVER_PROTOCOL_SHA is not None
 assert not list(BASE.glob(STEM+'_*')),'Exclusive reviewed root-only namespace required'
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 import numpy as numpy
 np=numpy;load_definitions()
 with localcontext() as context:
  context.prec=100;reference=independent_decimal_reference()
  for case in (1,2,3,4,5):
   CASES.append(dict(case=case,synthetic_constants_only=True,physical_adoption=False,decimal_precision=100,independent_EOS_reference={n:str(x) for n,x in reference.items()}))
   s,c,direction,constants=fresh_inputs(case);capture_tree('input_',dict(s=s,c=c,direction=direction,constants=constants));CASES[-1]['supplied_constants']=constants
   if case<4:
    out=candidate_invariant_phase_eos_current(s,c,direction,constants,keep,'fresh_case'+str(case));capture_tree('completed_',out)
    CASES[-1]['completed_output_flags']={n:x for n,x in out.items() if type(x) is bool};fresh_controls(case,out,reference)
   else:
    refused=False
    try:
     out=candidate_invariant_phase_eos_current(s,c,direction,constants,keep,'fresh_case'+str(case));capture_tree('unexpected_completed_',out)
    except AssertionError as exc:
     refused=True;CASES[-1]['refusal_reason']=str(exc)
    no_log=not any('elementary_log' in n for n in RAW);CASES[-1]['refused_before_log']=refused and no_log
    assert 'Same strict invariant EOS domain' in CASES[-1].get('refusal_reason','')
    verify_group('case%d_strict_invariant_domain_refusal'%case,[('refused_before_log',pair([float(refused and no_log)]),[Decimal(1)],[Decimal(1)])])
   save_case(case)
 assert len(CONTROLS)==17 and all(x['passed'] for x in CONTROLS)
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 report=dict(status='NEW_CANDIDATE_INVARIANT_PHASE_EOS_CURRENT_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),pins=PINS,driver_protocol_sha256=DRIVER_PROTOCOL_SHA,controls=CONTROLS,cases=CASES,synthetic_log_and_chain_accuracy_test_only=True,old_fixture_payload_field_operator_solver_replayed=False,physical_constants_builder_used_for_a_physical_candidate=False,finite_candidate_physically_admitted=False)
 with (BASE/(STEM+'_RESULT.json')).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/(STEM+'_RESULT.json')).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=17,sha256=sha(STEM+'_RESULT.json'))))

if __name__=='__main__':
 if AUTHOR_DRAFT or AUTHORING_IN_PROGRESS:raise SystemExit('Held definitions; reviewed root release required')
 try:main()
 except BaseException:
  if np is not None:
   for name,value in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+name]=np.asarray(value).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**RAW)
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
