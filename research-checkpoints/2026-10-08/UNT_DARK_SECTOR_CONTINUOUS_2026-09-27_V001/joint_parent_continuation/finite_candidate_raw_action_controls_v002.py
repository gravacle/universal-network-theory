"""HELD fresh candidate coefficient/action controls; root alone executes.
Three predeclared new inputs, independent rational answers, no prior fixture,
payload, source inventory, normal/scatter/operator/solver or offset replay.
"""
from pathlib import Path
from fractions import Fraction
import ast,hashlib,json,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='FINITE_CANDIDATE_RAW_ACTION_CONTROLS_V002'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'CROSS_U_FINITE_CANDIDATE_RAW_ACTION_ADAPTER_V001.md':'9ea02f39541eeebe49a3e88cb527a7292a47fc4307bec10e7d8acf24a5a6220c'}
DRIVER_PROTOCOL='FINITE_CANDIDATE_RAW_ACTION_CONTROLS_V001.md'
DRIVER_PROTOCOL_SHA='3cc759b52a0bb6347661d1d1c3e98ddb750ce3b551487daa21b062942c72ec6a'
np=P=None;PROVIDER_SCOPE={};RAW={};CASES=[];CONTROLS=[]

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def pair(high,low=None):
 h=np.asarray(high,dtype=np.float64);l=np.zeros_like(h) if low is None else np.asarray(low,dtype=np.float64)
 assert h.shape==l.shape;return h.copy(),l.copy()
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def capture_inputs(prefix,values):
 for name,value in values.items():
  if name in ('canonical_targets','prior_bridge_references'):continue
  if isinstance(value,dict):capture_inputs(prefix+name+'_',value)
  elif isinstance(value,tuple):keep(prefix+name+'_hi',value[0]);keep(prefix+name+'_lo',value[1])
  else:keep(prefix+name,value)
def rational_pair(values,shape):
 h=np.array([float(x) for x in values],dtype=np.float64);l=np.array([float(x-Fraction.from_float(float(a))) for x,a in zip(values,h)],dtype=np.float64)
 return h.reshape(shape),l.reshape(shape)
def rational_tensor(shape,entries,factor=Fraction(1)):
 values=[Fraction(0) for _ in range(int(np.prod(shape)))];index=np.arange(len(values)).reshape(shape)
 for key,value in entries.items():values[int(index[key])]=Fraction(value)*factor
 return rational_pair(values,shape)

def independent_model(case,modal):
 g=np.diag([-3.,16.,16.,16.])[None];g[0,0,1]=g[0,1,0]=4.
 hi=np.diag([-.25,3/64,1/16,1/16])[None];hi[0,0,1]=hi[0,1,0]=1/16
 z=np.zeros((32,1,4));z[0,0]=[-.1,2.,0.,0.] if modal else np.zeros(4)
 projector=np.eye(4)[None];projector[0,:2,:2]=[[-3/32,-7/128],[15/8,35/32]]
 du=np.zeros((1,4,4));dz=np.zeros((32,1,4,4));dg=np.zeros((1,4,4,4));Ga=np.zeros((1,4,4,4));e=2.**-60
 if case==3:
  du[0,0,3]=-3/128;dg[0,0,0,3]=dg[0,0,3,0]=.5;dg[0,0,1,3]=dg[0,0,3,1]=2.
  for l,a,b,v in ((3,0,0,1/32),(3,0,1,1/16),(3,1,0,1/16),(0,0,3,1/16),(0,3,0,1/16),(1,0,3,3/64),(1,3,0,3/64),(0,1,3,.25),(0,3,1,.25),(1,1,3,-1/16),(1,3,1,-1/16)):Ga[0,l,a,b]=v
 value=dict(g=pair(g),hi=pair(hi),U=pair([[5/8,1/32,0.,0.]]),z=pair(z),uc=pair([[-7/4,3.,0.,0.]]),P=pair(projector),up=pair([[3/16,0.,0.]]),gamma=pair([5/4]),dens=pair([128.]),du=pair(du,du*e if case==3 else None),dz=pair(dz),dg=pair(dg,dg*e if case==3 else None),Ga=pair(Ga,Ga*e if case==3 else None))
 if case==2:value['g'][1][0,2,2]=e;value['hi'][1][0,2,2]=-e/256;value['dens'][1][0]=4*e
 return dict(value=value,delta={n:pair(np.zeros_like(x[0])) for n,x in value.items()})

def case_inputs(case):
 e=2.**-60;modal=case!=1;h=np.eye(3)[None]*16.;low=np.zeros_like(h);I=np.eye(3)[None]/16;Ilow=np.zeros_like(I)
 if case==2:low[0,1,1]=e;Ilow[0,1,1]=-e/256
 geometry=dict(h=pair(h,low),ih=pair(I,Ilow),mu=pair([64.],[2*e] if case==2 else None),h_spatial_jets=pair(np.zeros((1,2,3,3))))
 gauge=dict(N=pair([2.]),beta=pair([[.25,0.,0.]]),N_jets=pair(np.zeros((1,4))),beta_jets=pair(np.zeros((1,4,3))))
 z=np.zeros((32,1,3));z[0,0,0]=2. if modal else 0.;ht=np.zeros((1,3,3))
 if case==3:ht[0,0,2]=ht[0,2,0]=2.
 covectors=dict(u=pair([[3.,0.,0.]]),z=pair(z),u_jets=pair(np.zeros((1,4,3))),z_jets=pair(np.zeros((32,1,4,3))))
 mechanical=dict(h_dot=pair(ht,ht*e if case==3 else None));phase=dict(phi=pair(np.zeros((1,4))))
 w=np.zeros(32);w[0]=1.;material=dict(omega=np.ones(32),xi=np.ones(32),w=w,B=1.,GC=1.,ALPHA=.02/1.98,ELL=.1,C=1.98,R=np.array([1.]),Z_coordinate=np.array([1.]))
 model=independent_model(case,modal);base=independent_model(1,modal)
 reference={n:base['value'][n] for n in ('g','hi','U','z','du','dz','dg','Ga')};reference.update(E0=pair(np.zeros((1,4,4,4))),canonical_targets=dict(kind='manufactured_prior_only',physical_target_adopted=False),prior_bridge_references=dict(kind='manufactured_reference_only',physical_primitive_admission=False))
 return geometry,model,gauge,covectors,mechanical,phase,material,reference

def check(name,actual,expected,bound,exact=False):
 envelope=np.full(actual[0].shape,float(bound))+abs(expected[0])+abs(expected[1]);assert np.all(envelope>0)
 for key,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(name+'_'+key,x)
 assert actual[0].shape==actual[1].shape==expected[0].shape==expected[1].shape
 gap=P.a_sub(actual,expected);keep(name+'_gap_hi',gap[0]);keep(name+'_gap_lo',gap[1]);error=float(np.max(abs(gap[0]+gap[1])/envelope,initial=0))
 word=not exact or all(np.array_equal(actual[i],expected[i]) for i in (0,1));keep(name+'_word_predicate',np.asarray(word))
 CONTROLS.append(dict(name=name,error=error,tolerance=2e-11,exact_words=exact,word_predicate=word,passed=error<=2e-11 and word));assert error<=2e-11 and word,(name,error,word)

def expected_tables(case):
 F=Fraction;e=F(1,2**60);factor=1+e if case==3 else F(1)
 expected_JU=rational_tensor((1,4,3),{(0,0,0):F(3,40),(0,1,0):F(7,160),(0,2,1):F(1,16),(0,3,2):F(1,16)})
 expected_Uh=rational_tensor((1,6,4),{(0,0,0):-F(9,1280),(0,0,1):-F(51,5120),(0,3,2):-F(3,256),(0,4,3):-F(3,256)})
 embed=rational_tensor((1,4,4),{(0,0,0):F(1,16),(0,0,1):F(1,4),(0,1,0):F(1,4),(0,1,1):F(1)})
 known=dict(h=pair(np.eye(3)[None]*16),ih=pair(np.eye(3)[None]/16),sqrt_h=pair([64.]),JU=expected_JU,Jzz=rational_tensor((1,3),{(0,0):-F(1,20)}),Uh=expected_Uh,embed_RR=embed)
 modal=case!=1;z2=rational_tensor((32,1),{(0,0):F(4,25)} if modal else {});f=rational_pair([F(29,25) if modal and i==0 else F(1) for i in range(32)],(32,1))
 known.update(JzU=rational_tensor((32,1,3),{(0,0,0):-F(16,125)} if modal else {}),zh=rational_tensor((32,1,6),{(0,0,0):F(123,4000)} if modal else {}),z2=z2,f=f,K_Gamma_minus_ADM=pair(np.zeros((1,3,3))),target_and_scope_preserved=pair(np.asarray(1.)))
 if case in (1,2):
  known.update(native_canonical_density=rational_tensor((1,99),{(0,0):F(32,5)} if modal else {}),metric_canonical_density=pair(np.zeros((1,6))))
  if case==1:known['new_static_Gamma']=pair(np.zeros((1,4,4,4)))
  else:
   expected=np.zeros((1,3,3));expected[0,1,1]=2.**-60;known.update(h_low_quantization_word=pair(expected),h_sum_rounding_word=pair(expected))
 else:
  independent=independent_model(3,True)
  for n in ('du','dg','Ga'):known['cross_time_'+n]=independent['value'][n]
  K=rational_tensor((1,3,3),{(0,0,2):F(1,2),(0,2,0):F(1,2)},factor)
  known.update(K_Gamma=K,K_ADM=K,Ktrace=pair([0.]),EH_cross_time_density=rational_tensor((1,6),{(0,4):1/(8*F.from_float(cast_physical_C()))},factor))
 return known

def known_controls(case,out,reference,known):
 c=out['c'];s=out['s'];m=out['momenta'];prefix='case%d_'%case
 for n,bound in (('h',32),('ih',2),('sqrt_h',128),('JU',8),('Jzz',8),('Uh',8),('embed_RR',8),('JzU',16),('zh',16),('z2',16),('f',16)):
  raw=c['embed'][:,0] if n=='embed_RR' else c[n] if n in c else s[n];check(prefix+n,pair(raw),known[n],bound)
 if case in (1,2):
  for n,key in (('native_canonical_density','native_density'),('metric_canonical_density','metric_total_density')):check(prefix+n,m[key],known[n],512)
  if case==1:check(prefix+'new_static_Gamma',out['jets']['Ga'],known['new_static_Gamma'],32,True)
  else:
   check(prefix+'h_low_quantization_word',tuple(RAW['new_case2_h_paired_minus_binary64_'+w] for w in ('hi','lo')),known['h_low_quantization_word'],32,True)
   check(prefix+'h_sum_rounding_word',pair(RAW['new_case2_h_sum_rounding_word']),known['h_sum_rounding_word'],32,True)
 else:
  for n in ('du','dg','Ga'):check(prefix+'cross_time_'+n,out['jets'][n],known['cross_time_'+n],32,True)
  for n,key in (('K_Gamma','K'),('Ktrace','Ktrace')):check(prefix+n,m[key],known[n],32,True)
  check(prefix+'K_ADM',out['KADM'],known['K_ADM'],32,True);check(prefix+'EH_cross_time_density',m['metric_EH_density'],known['EH_cross_time_density'],32)
 check(prefix+'K_Gamma_minus_ADM',tuple(RAW['new_case%d_KGamma_minus_KADM_%s'%(case,w)] for w in ('hi','lo')),known['K_Gamma_minus_ADM'],32)
 preserved=out['canonical_target_references'] is reference['canonical_targets'] and out['prior_bridge_references'] is reference['prior_bridge_references'] and not out['physical_adoption'] and not out['original_offsets_refitted'] and not out['candidate_action_JVP_evaluated']
 check(prefix+'target_and_scope_preserved',pair(np.asarray(float(preserved))),known['target_and_scope_preserved'],1,True)

def cast_physical_C():return 1.98
def save_case(case):
 name=STEM+'_CASE'+str(case)+'.npz'
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**RAW)
 (BASE/name).chmod(0o444);CASES.append(dict(case=case,file=name,sha256=sha(name),fields=len(RAW),physical_adoption=False));RAW.clear()

def main():
 global np,P,PROVIDER_SCOPE
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and DRIVER_PROTOCOL_SHA is not None and not list(BASE.glob(STEM+'_*')),'Root exclusive reviewed release required'
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 import numpy as numpy
 np=numpy;base_names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 extra_names={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','paired_current_affine_features','paired_current_affine_momenta'}
 arith_file=list(PINS)[0];provider_file=list(PINS)[1];trees=[ast.parse((BASE/f).read_text()) for f in (arith_file,provider_file)];maps=[{n.name:n for n in t.body if isinstance(n,ast.FunctionDef)} for t in trees]
 for n in base_names:assert ast.dump(maps[0][n],include_attributes=False)==ast.dump(maps[1][n],include_attributes=False),n
 selected=[maps[0][n.name] for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base_names]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in extra_names];assert len(selected)==20
 PROVIDER_SCOPE=dict(np=np,DD_ARRAY_CURRENT={},B=1.,GC=1.,ALPHA=.02/1.98,ELL=.1,C=1.98);exec(compile(ast.Module(body=selected,type_ignores=[]),provider_file,'exec'),PROVIDER_SCOPE)
 P=types.SimpleNamespace(**{n:PROVIDER_SCOPE[n] for n in base_names|extra_names|{'B','GC','ALPHA','ELL','C'}})
 for file in (list(PINS)[2],list(PINS)[4]):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())
 for case in (1,2,3):
  inputs=case_inputs(case);known=expected_tables(case);names=('geometry','spacetime','gauge','covectors','mechanical','phase','material','reference');capture_inputs('fresh_input_',dict(zip(names,inputs)));capture_inputs('independent_expected_',known)
  out=finite_candidate_raw_action_adapter(*inputs,P.paired_current_affine_features,P.paired_current_affine_momenta,keep,'new_case'+str(case))
  capture_inputs('completed_',dict(s=out['s'],c=out['c'],jets=out['jets'],features=out['features']['paired'],momenta=out['momenta'],bounds=out['coefficient_envelopes'],first_bounds=out['positive_first_jet_envelopes'],KADM=out['KADM']))
  known_controls(case,out,inputs[-1],known);save_case(case)
 assert len(CONTROLS)==53 and all(x['passed'] for x in CONTROLS)
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 report=dict(status='NEW_FINITE_CANDIDATE_RAW_COEFFICIENT_ACTION_CONTROLS_PASS',pid=os.getpid(),source_sha256=sha(Path(__file__).name),pins=PINS,driver_protocol_sha256=DRIVER_PROTOCOL_SHA,controls=CONTROLS,cases=CASES,only_three_new_inputs_and_new_candidate_coefficients_and_action_evaluated=True,old_15_or_82_fixture_or_source_payload_operator_solver_replayed=False,finite_candidate_weak_canonical_normal_CMC_or_physical_adoption=False)
 name=STEM+'_RESULT.json'
 with (BASE/name).open('x') as f:json.dump(report,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);print(json.dumps(dict(status=report['status'],controls=53,sha256=sha(name))))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for name,value in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+name]=np.asarray(value).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**RAW)
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  with (BASE/(STEM+'_ERROR.json')).open('x') as f:json.dump(dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,cases=CASES,traceback=traceback.format_exc()),f,sort_keys=True,indent=2);f.write('\n')
  (BASE/(STEM+'_ERROR.json')).chmod(0o444);raise
