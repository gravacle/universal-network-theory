"""HELD new three-label Q1/reference/conformal controls; root owns execution.
Only new exact data are evaluated after release. No source labels, old control,
volume geometry, Gauss metric, fixture or scientific payload is replayed.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import ast,hashlib,json,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='FIXED_LABEL_FINITE_SHEET_GEOMETRY_CONTROLS_V002'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_fixed_label_finite_sheet_geometry_v002.py':'556bac0713c74947b0abece865bf7e74c3d3b212029af1248aa7dd0af525a661'}
DRIVER_PROTOCOL='FIXED_LABEL_FINITE_SHEET_GEOMETRY_CONTROLS_V001.md'
DRIVER_PROTOCOL_SHA='a954f63c1d59671e6e85ca4f9718f851cea261863a1b99217684d1b8f90a4040'
np=P=None;PROVIDER_SCOPE={};RAW={};CONTROLS=[];REFERENCES={};COMPLETED=[]

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def pair(value):
 h=np.asarray(value,dtype=np.float64);return h.copy(),np.zeros_like(h)
def capture(prefix,value):
 if isinstance(value,dict):
  for n,x in value.items():capture(prefix+'_'+n,x)
 elif isinstance(value,(tuple,list)):
  if len(value)==2 and all(isinstance(w,np.ndarray) for w in value):keep(prefix+'_hi',value[0]);keep(prefix+'_lo',value[1])
  else:
   for i,x in enumerate(value):capture(prefix+'_'+str(i),x)
 elif isinstance(value,(np.ndarray,int,float,bool)):keep(prefix,value)
def decimal_pair(name,values,shape):
 hi=[];lo=[];rem=[]
 for x in values:
  a=float(x);b=float(x-Decimal.from_float(a));hi.append(a);lo.append(b);rem.append(str(x-Decimal.from_float(a)-Decimal.from_float(b)))
 REFERENCES[name]=dict(shape=shape,decimal100_values=[str(x) for x in values],two_word_conversion_remainders=rem)
 out=(np.array(hi).reshape(shape),np.array(lo).reshape(shape));capture('independent_'+name,out);return out
def check(name,actual,expected,envelope,exact=False):
 assert all(w.shape==actual[0].shape and w.dtype==np.float64 for p in (actual,expected) for w in p)
 e=np.broadcast_to(np.asarray(envelope),actual[0].shape).copy();assert np.all(np.isfinite(e)) and np.all(e>0)
 for n,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',e)):keep(name+'_'+n,x)
 gap=P.a_sub(actual,expected);capture(name+'_gap',gap);err=float(np.max((abs(gap[0])+abs(gap[1]))/e,initial=0));words=not exact or all(np.array_equal(actual[i],expected[i]) for i in (0,1))
 keep(name+'_exact_words_predicate',np.asarray(words));CONTROLS.append(dict(name=name,error=err,tolerance=2e-11,exact_words_required=exact,exact_words=words,passed=err<=2e-11 and words));assert err<=2e-11 and words,(name,err,words)

def new_inputs(case):
 # Full metric entries are exact dyadics, from independently declared h/N/beta.
 g=np.array([[[1/4,2.,-9/4,2.],[2.,4.,0.,0.],[-9/4,0.,9.,0.],[2.,0.,0.,16.]],
             [[-5/8,-1/4,2.,9/4],[-1/4,1.,0.,0.],[2.,0.,4.,0.],[9/4,0.,0.,9.]],
             [[-9/16,7/8,-1/4,9/2],[7/8,4.,1.,0.],[-1/4,1.,4.,0.],[9/2,0.,0.,9.]]])
 r=np.arange(87,dtype=np.float64);indices=np.array([10,20,30],dtype=np.int64);right=np.array([1/4,1/2,3/4]);R=np.array([41/4,41/2,123/4]);Z=np.zeros(3)
 rho=(np.full((87,45),0. if case==0 else 1/32),np.full((87,45),0. if case==0 else 2.**-62));drho=pair(np.zeros((87,45)))
 for i,a,b in ((10,1/8,2.**-60),(11,3/8,-2.**-59),(20,-1/4,2.**-61),(21,1/4,2.**-61),(30,1/2,-2.**-60),(31,-1/4,2.**-61)):drho[0][i,0]=a;drho[1][i,0]=b
 return g,R,Z,r,indices,right,rho,drho

def independent_targets(case):
 with localcontext() as ctx:
  ctx.prec=100;D=Decimal;F=Fraction;dd=lambda x:D(x.numerator)/D(x.denominator)
  rho=F(0) if case==0 else F(1,32)+F(1,2**62);d=[F(3,16)+F(1,2**62),F(1,2**61),-F(1,16)+F(1,2**63)];lam=(4*dd(rho)).exp();ilam=1/lam
  h=[[F(4),0,0,0,F(9),0,0,0,F(16)],[F(1),0,0,0,F(4),0,0,0,F(9)],[F(4),F(1),0,F(1),F(4),0,0,0,F(9)]]
  inverse=[[F(1,4),0,0,0,F(1,9),0,0,0,F(1,16)],[F(1),0,0,0,F(1,4),0,0,0,F(1,9)],[F(4,15),-F(1,15),0,-F(1,15),F(4,15),0,0,0,F(1,9)]]
  base_mu=[D(24),D(6),D(135).sqrt()];mu=[m*(6*dd(rho)).exp() for m in base_mu]
  beta=[[F(1,2),-F(1,4),F(1,8)],[-F(1,4),F(1,2),F(1,4)],[F(1,4),-F(1,8),F(1,2)]];lapse=[F(5,4),F(3,2),F(7,4)]
  vals=dict(rho=([dd(rho)]*3,(3,)),delta_rho=([dd(x) for x in d],(3,)),h=([lam*dd(F(x)) for row in h for x in row],(3,3,3)),ih=([ilam*dd(F(x)) for row in inverse for x in row],(3,3,3)),mu=(mu,(3,)),N=([dd(x) for x in lapse],(3,)),beta=([dd(x) for row in beta for x in row],(3,3)),delta_h=([4*dd(d[i])*lam*dd(F(x)) for i,row in enumerate(h) for x in row],(3,3,3)),delta_ih=([-4*dd(d[i])*ilam*dd(F(x)) for i,row in enumerate(inverse) for x in row],(3,3,3)),delta_mu=([6*dd(d[i])*mu[i] for i in range(3)],(3,)))
  REFERENCES['case%d_conformal'%case]=dict(rho_fraction=str(rho),direction_fractions=[str(x) for x in d],lambda_exp_4rho=str(lam),volume_exp_6rho=str((6*dd(rho)).exp()),precision=100,reference_matrices_independent=True)
  target={n:decimal_pair('case%d_%s'%(case,n),x,s) for n,(x,s) in vals.items()}
  eh=np.array([float(lam*sum(abs(dd(F(x))) for x in row)) for row in h]);ei=np.array([float(ilam*sum(abs(dd(F(x))) for x in row)) for row in inverse]);ed=np.array([float(abs(dd(x))) for x in d])
  bounds=dict(h=eh[:,None,None],ih=ei[:,None,None],mu=np.array([float(x) for x in mu]),N=np.array([float(x) for x in lapse]),beta=np.array([float(sum(abs(dd(x)) for x in row)) for row in beta])[:,None],delta_h=4*ed[:,None,None]*eh[:,None,None],delta_ih=4*ed[:,None,None]*ei[:,None,None],delta_mu=6*ed*np.array([float(x) for x in mu]))
  return target,bounds

def run_new_case(case):
 inputs=new_inputs(case);capture('case%d_fresh_inputs'%case,dict(zip(('reference_g','R','Z','r','indices','right','rho_nodes','delta_rho_nodes'),inputs)));targets,bounds=independent_targets(case)
 result=fixed_label_finite_sheet_geometry(*inputs,keep,'case%d_NEW_fixed_label_geometry'%case);capture('case%d_completed_output'%case,result)
 check('case%d_Q1_rho'%case,result['rho'],targets['rho'],np.ones(3),True);check('case%d_Q1_direction'%case,result['delta_rho'],targets['delta_rho'],np.array([1/2,1/2,3/4]),True)
 for n in ('h','ih','mu','delta_h','delta_ih','delta_mu'):check('case%d_%s'%(case,n),result['geometry'][n],targets[n],bounds[n])
 for n in ('N','beta'):check('case%d_fixed_%s'%(case,n),result['gauge'][n],targets[n],bounds[n])
 assert all(np.all(w==0) for n in ('N','beta') for w in result['gauge_direction'][n])
 assert result['original_label_positions_unchanged'] and not result['mass_or_volume_factor_added'] and not result['reference_metric_lineage_admitted_by_this_helper'] and not result['conformal_exp_accuracy_admitted'] and not result['physical_inverse_precision_admitted'] and not result['finite_candidate_physically_admitted']
 if case==0:assert np.array_equal(result['geometry']['h'][0],inputs[0][:,1:,1:]) and np.all(result['geometry']['h'][1]==0)
 COMPLETED.append(dict(case=case,three_fixed_labels=True,rho_zero_reference_exact=case==0,physical_adoption=False))

def initialize():
 global np,P,PROVIDER_SCOPE
 import numpy as numpy
 np=numpy;names=list(PINS);tree=ast.parse((BASE/names[0]).read_text());wanted={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'};defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted];assert len(defs)==12
 PROVIDER_SCOPE=dict(np=np,DD_ARRAY_CURRENT={},capture=keep);exec(compile(ast.Module(body=defs,type_ignores=[]),names[0],'exec'),PROVIDER_SCOPE);P=types.SimpleNamespace(**{n:PROVIDER_SCOPE[n] for n in wanted})
 for file,count in ((names[1],11),(names[2],2)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count;exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())

def save_json(name,data):
 with (BASE/name).open('x') as f:json.dump(data,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);return dict(file=name,sha256=sha(name))
def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and DRIVER_PROTOCOL_SHA is not None and not list(BASE.glob(STEM+'_*')),'Root exclusive reviewed release required'
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert h is not None and sha(n)==h,n
 owner=save_json(STEM+'_OWNER_START.json',dict(pid=os.getpid(),source_sha256=sha(Path(__file__).name),pins=PINS,protocol_sha256=DRIVER_PROTOCOL_SHA));initialize()
 for case in (0,1):run_new_case(case)
 assert len(CONTROLS)==20 and all(x['passed'] for x in CONTROLS)
 for n,x in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+n]=np.asarray(x).copy()
 point=STEM+'_POINTS.npz'
 with (BASE/point).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
 (BASE/point).chmod(0o444);refs=save_json(STEM+'_INDEPENDENT_REFERENCES.json',REFERENCES)
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 report=dict(status='NEW_FIXED_LABEL_Q1_REFERENCE_CONFORMAL_CONTROLS_PASS',pid=os.getpid(),owner=owner,source_sha256=sha(Path(__file__).name),pins=PINS,protocol_sha256=DRIVER_PROTOCOL_SHA,controls=CONTROLS,cases=COMPLETED,point=dict(file=point,sha256=sha(point),fields=len(RAW)),independent_references=refs,old_fixture_or_source_labels_or_payload_replayed=False,reference_lineage_or_physical_finite_state_admitted=False)
 saved=save_json(STEM+'_RESULT.json',report);print(json.dumps(dict(status=report['status'],controls=len(CONTROLS),sha256=saved['sha256'])))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for n,x in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+n]=np.asarray(x).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  save_json(STEM+'_ERROR.json',dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,completed=COMPLETED,independent_references=REFERENCES,traceback=traceback.format_exc()));raise
