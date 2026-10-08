"""HELD three NEW manufactured phase mass components, not a candidate admission.
Four dyadic points/cell are an arithmetic rule, not the physical Gauss rule.
No prepare/EOS/provenance fabrication or old numerical fixture/producer call.
"""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as F
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=True
AUTHORING_IN_PROGRESS=True
STEM='CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V001'
PROTOCOL='CANDIDATE_LITERAL_PHASE_MASS_COMPONENT_CONTROLS_V001.md'
PROTOCOL_SHA=None
PINS={'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
      'author_fragment_phase_literal_charge_hessian_v002.py':'293b071b6021a236ef43e9be1bde9e304b6c716ec7f0519acfbb0377af4e7143',
      'author_fragment_candidate_literal_phase_mass_v001.py':'0227bc106f3f59be32a17d83f6ce6efc76032e5935cbf17c42b036a97c386b38'}
np=P=K=None;AVAILABLE={};DD_ARRAY_CURRENT={};CHECKS=[];CASES=[]

def keep(name,value):
 a=np.asarray(value).copy();AVAILABLE[name]=a
 assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a)),'nonfinite completed operand '+name
 return a

def check(name,actual,expected,envelope):
 a=np.asarray(actual,dtype=np.float64);e=np.asarray(expected,dtype=np.float64);b=np.asarray(envelope,dtype=np.float64)
 keep('control_%d_actual'%len(CHECKS),a);keep('control_%d_expected'%len(CHECKS),e);keep('control_%d_envelope'%len(CHECKS),b)
 score=float(np.max(abs(a-e)/np.maximum(abs(b),1e-30))) if a.size else 0.
 result=dict(name=name,normalized_error=score,passed=bool(math.isfinite(score) and score<=2e-11));CHECKS.append(result);assert result['passed'],name

def initialize():
 global np,P,K
 import numpy as numpy
 np=numpy;files=list(PINS);t=ast.parse((BASE/files[0]).read_text());names={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_reshape','scalar_mask','scalar_lift','dd_scalar_scatter'}
 scope=dict(np=np,DD_ARRAY_CURRENT=DD_ARRAY_CURRENT,capture=keep);defs=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==15;exec(compile(ast.Module(body=defs,type_ignores=[]),files[0],'exec'),scope);P=types.SimpleNamespace(**{n:scope[n] for n in names})
 t=ast.parse((BASE/files[1]).read_text());names={'phase_pair_keep','phase_scalar_value','phase_mass_diagonal'};scope=dict(np=np,P=P);defs=[n for n in t.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(defs)==3;exec(compile(ast.Module(body=defs,type_ignores=[]),files[1],'exec'),scope);K=types.SimpleNamespace(**{n:scope[n] for n in names})
 t=ast.parse((BASE/files[2]).read_text());defs=[n for n in t.body if isinstance(n,ast.FunctionDef)];assert len(defs)==5;exec(compile(ast.Module(body=defs,type_ignores=[]),files[2],'exec'),globals())

def publish_case(name,metadata):
 data={**AVAILABLE,**{'last_DD_'+n:a for n,a in DD_ARRAY_CURRENT.get('arrays',{}).items()}}
 file=STEM+'_%02d_CASE.npz'%len(CASES);assert not (BASE/file).exists();np.savez_compressed(BASE/file,**{n:np.asarray(a).copy() for n,a in data.items()})
 schema={n:dict(shape=list(np.asarray(a).shape),dtype=str(np.asarray(a).dtype),finite=bool(np.all(np.isfinite(a)))) for n,a in data.items()}
 record=dict(file=file,sha256=hashlib.sha256((BASE/file).read_bytes()).hexdigest(),metadata=dict(name=name,schema=schema,**metadata));CASES.append(record)
 (BASE/(file.removesuffix('.npz')+'_COMMIT.json')).write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
 return record

def manufactured_rule():
 I=np.arange(86)[:,None];J=np.arange(44)[None,:];R=np.zeros((4,86,44));Z=np.zeros_like(R);hats=np.zeros((4,4,3,86,44));points=((F(1,4),F(1,4)),(F(3,4),F(1,4)),(F(1,4),F(3,4)),(F(3,4),F(3,4)))
 for iq,(x,y) in enumerate(points):
  R[iq]=I+float(x);Z[iq]=J+float(y)
  for corner,(di,dj) in enumerate(((0,0),(1,0),(0,1),(1,1))):
   hx=x if di else 1-x;hy=y if dj else 1-y
   hats[iq,corner,0]=float(hx*hy);hats[iq,corner,1]=float((1 if di else -1)*hy);hats[iq,corner,2]=float(hx*(1 if dj else -1))
 i=np.arange(87)[:,None];j=np.arange(45)[None,:];nodes=(np.asarray(3+2*i-j+i*j/8.,dtype=np.float64),np.asarray(2.**-60*(1+i-2*j+i*j/16.),dtype=np.float64));nodes[0][0]=0.;nodes[1][0]=0.
 geometry=dict(R=R,dv=R/4.,hats=hats);H=P.a_dd((2+R/8+Z/16).reshape(15136))
 for n,a in geometry.items():keep('manufactured_'+n,a)
 for word,a in zip(('hi','lo'),nodes):keep('manufactured_phase_nodes_'+word,a)
 K.phase_pair_keep('manufactured_positive_analytic_H',H,keep)
 return geometry,H,nodes,points

def fraction_targets(points):
 shape=(4,86,44);targets={n:np.empty(shape,dtype=object) for n in ('value','R','Z','point')};weak=[[F(0) for j in range(45)] for i in range(87)];low=F(1,2**60)
 for iq,(xi,eta) in enumerate(points):
  for i in range(86):
   for j in range(44):
    r=F(i)+xi;z=F(j)+eta;x=F(1) if i==0 else r
    value=3+2*x-z+x*z/8+low*(1+x-2*z+x*z/16);dr=F(0) if i==0 else 2+z/8+low*(1+z/16);dz=-1+x/8+low*(-2+x/16)
    point=(2+r/8+z/16)*value
    for n,a in (('value',value),('R',dr),('Z',dz),('point',point)):targets[n][iq,i,j]=a
    # Independently defined four-corner weak functional; alias only AFTER summation.
    for di,dj in ((0,0),(1,0),(0,1),(1,1)):
     hx=xi if di else 1-xi;hy=eta if dj else 1-eta;weak[i+di][j+dj]+=point*hx*hy/4
 for j in range(45):weak[1][j]+=weak[0][j];weak[0][j]=F(0)
 targets['weak']=np.asarray(weak,dtype=object)
 return {n:a.reshape(15136) if n!='weak' else a for n,a in targets.items()}

def exact_expected_pair(name,expected):
 high=np.empty(expected.shape);low=np.empty(expected.shape);strings=[];largest=0
 for index in np.ndindex(expected.shape):
  a=expected[index];assert a.denominator&(a.denominator-1)==0 and a.denominator<=2**80 and abs(a.numerator).bit_length()<=95
  h=float(a);l=float(a-F.from_float(h));assert F.from_float(h)+F.from_float(l)==a
  high[index]=h;low[index]=l;strings.append(str(a));largest=max(largest,abs(a.numerator).bit_length())
 K.phase_pair_keep('independent_Fraction_'+name,(high,low),keep)
 return (high,low),dict(rational_reference_sha256=hashlib.sha256('\n'.join(strings).encode()).hexdigest(),maximum_dyadic_numerator_bits=largest,maximum_denominator_bound=2**80)

def run_components():
 geometry,H,nodes,points=manufactured_rule();cache=dict(H=H,basis=geometry) # analytic action inputs only; no prepare/candidate flags
 result=candidate_phase_mass_action(cache,geometry,nodes,keep,'manufactured_action');targets=fraction_targets(points);actual=dict(**result['scalar_jets'],point=result['point'],weak=result['weak']);counts=[];references={};expected_pairs={}
 for n in ('value','R','Z','point','weak'):
  expected_pairs[n],references[n]=exact_expected_pair(n,targets[n]);pair=actual[n]
  mismatch=sum(F.from_float(float(pair[0][index]))+F.from_float(float(pair[1][index]))!=targets[n][index] for index in np.ndindex(targets[n].shape));counts.append(mismatch)
 assert np.any(result['weak'][0][-1]!=0) and np.any(result['weak'][0][:,-1]!=0),'Outer/top phase nodes remain free'
 assert result['extra_N_or_mu_factor_inserted'] is False
 certificate=candidate_phase_mass_certificate(expected_pairs['weak'],result['weak'],np.ones(3870),keep,'manufactured_nonzero_original_RHS')
 check('NEW dyadic both-word mass/value/RZ/direct-functional and nonzero original certificate',np.array(counts+certificate['ratios'].tolist()),np.zeros(7),np.ones(7))
 publish_case('new_dyadic_mass_and_mixed_jets',dict(integration_rule='four dyadic quarter/three-quarter points; not physical Gauss',independent_axis_fold=True,expected_references=references,meaningful_low_word=2.**-60,extra_N_mu=False,physical_candidate_admission=False));AVAILABLE.clear();DD_ARRAY_CURRENT.clear()
 zero=P.a_dd(np.zeros((87,45)));certificate=candidate_phase_mass_certificate(zero,zero,np.ones(3870),keep,'exact_zero_target')
 assert certificate['zero_target_relative_ratio_undefined'] is True and certificate['exact_zero_residual'] is True
 check('NEW exact-zero charge target and residual fallback',certificate['ratios'],np.zeros(2),np.ones(2));publish_case('exact_zero_charge_fallback',dict(relative_score_undefined=True,certificate_returned=True,exact_words_required=True,physical_candidate_admission=False));AVAILABLE.clear();DD_ARRAY_CURRENT.clear()
 returned=False;refusal=None
 try:
  candidate_phase_mass_certificate(zero,result['weak'],np.ones(3870),keep,'zero_target_nonzero_residual');returned=True
 except AssertionError as error:refusal=str(error)
 name='zero_target_nonzero_residual_original_raw_scaled_ratio_or_exact_zero_fallback';attempt=AVAILABLE[name]
 assert refusal=='nonfinite completed operand '+name and not returned and np.all(np.isposinf(attempt))
 assert 'zero_target_nonzero_residual_original_residual_hi' in AVAILABLE and 'zero_target_nonzero_residual_original_RHS_raw_scaled_and_residual_raw_scaled_norms' in AVAILABLE
 check('NEW zero charge target with nonzero residual must retain infinity then refuse',np.array((int(returned),int(refusal is None))),np.zeros(2),np.ones(2));publish_case('intentional_zero_charge_nonzero_residual_refusal',dict(certificate_returned=False,expected_assertion=refusal,failed_ratio_hex=[float(a).hex() for a in attempt],retained_nonfinite_is_expected_refusal=True,physical_candidate_admission=False))
 assert len(CHECKS)==3 and len(CASES)==3 and all(q['passed'] for q in CHECKS)

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and PROTOCOL_SHA is not None,'Root release required'
 assert not list(BASE.glob(STEM+'_*')),'Unused namespace required'
 inputs=dict(PINS,**{PROTOCOL:PROTOCOL_SHA})
 for file,h in inputs.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
 owner=dict(owner='root',pid=os.getpid(),started=datetime.now(timezone.utc).isoformat(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest());(BASE/(STEM+'_OWNER_START.json')).write_text(json.dumps(owner,indent=2)+'\n')
 try:
  initialize();run_components()
  for file,h in inputs.items():assert hashlib.sha256((BASE/file).read_bytes()).hexdigest()==h,file
  status='CANDIDATE_LITERAL_PHASE_MASS_MANUFACTURED_COMPONENT_CONTROLS_PASS';result=dict(status=status,owner=owner,closed=datetime.now(timezone.utc).isoformat(),controls=CHECKS,cases=CASES,input_sha256=inputs,candidate_prepare_or_actual_H_admitted=False,actual_candidate_or_quadrature_or_fixed_charge_modified=False,physical_adoption=False)
  (BASE/(STEM+'_RESULT.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(status,len(CHECKS),len(CASES));return 0
 except BaseException:
  error=traceback.format_exc()
  if np is not None and AVAILABLE:publish_case('unexpected_unfinished_component_operands',dict(unexpected_error=True,physical_candidate_admission=False))
  (BASE/(STEM+'_ERROR.json')).write_text(json.dumps(dict(owner=owner,status='CLOSED_ERROR',traceback=error,controls=CHECKS,cases=CASES,input_sha256=inputs,physical_adoption=False),indent=2,allow_nan=False)+'\n');raise
if __name__=='__main__':raise SystemExit(main())
