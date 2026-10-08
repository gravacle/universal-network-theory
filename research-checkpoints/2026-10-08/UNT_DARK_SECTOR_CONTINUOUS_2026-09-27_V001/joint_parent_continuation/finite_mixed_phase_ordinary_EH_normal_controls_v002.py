"""HELD one new mixed integration point; root alone releases and executes.
Definitions-only provider loads, fresh inputs only, no old fixture/payload replay.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import ast,hashlib,json,math,os,types,traceback
BASE=Path(__file__).resolve().parent
AUTHOR_DRAFT=False
AUTHORING_IN_PROGRESS=False
STEM='FINITE_MIXED_PHASE_ORDINARY_EH_NORMAL_CONTROLS_V002'
PINS={
 'cross_u_canonical_nodal_metric_rate_dd_coordinates_v001.py':'5d4bdfeaa5da8f09c95f805a5c41b17909d77e1f3feb01271a496a9b989d0d18',
 'cross_u_paired_current_primitive_momentum_readout_v002.py':'b147761642485d1bdce9b0fb831ed5f5f2a1aa458182908766ffcb17b1e80c19',
 'author_fragment_finite_york_geometry_target_v001.py':'12fe8b5ac355fd2f94e2fdaa37244aedabe6fa1212b796ddd2f6411002555e70',
 'author_fragment_finite_york_spacetime_first_jets_v001.py':'aea9eda31c264c4c706f6fe72f086921b842681f9581334d5c4db03b506dd14d',
 'author_fragment_finite_candidate_raw_action_adapter_v001.py':'9f5367d7c3d70b93adde90502ff3d6bd6694ea50406bce69826644be58a18474',
 'author_fragment_compact_metric_contact_momenta_v002.py':'f884ba20c78a5e64c598a3907070fa45e76327d7344fdaeb2cfa9aa71e21d0bd',
 'author_fragment_finite_candidate_configuration_contact_v001.py':'7703f3c31e7a120d332d11ccaef97e60b4471066cccb22f6e0186b16cab59e41',
 'author_fragment_finite_candidate_native_EH_normal_v001.py':'51947ffe86b0b2aa592ac331aaaca2323872249785268d0dbfc4dec662a79152',
 'author_fragment_candidate_invariant_phase_eos_current_v001.py':'fa5303146a0bf5ddd47b5108abaa5b220169509f9241c96d1c181a79fd8d88ae',
 'author_fragment_candidate_phase_normal_stress_v001.py':'c957bda90eaea28107bb38b1785f3a392ade6357e2ec20aeb8fe874a194393dd',
 'author_fragment_finite_fixed_canonical_ordinary_v001.py':'2570c014c1623ba1dc119e428a9ec480c9ec79e1a949ad8d1c9f8230fb87287a',
 'author_fragment_fresh_finite_mixed_normal_integration_control_v001.py':'76968f1c453ad135bc53056338f2958989982f64f952bac19f45a793e45c6656'}
DRIVER_PROTOCOL='FINITE_MIXED_PHASE_ORDINARY_EH_NORMAL_CONTROLS_V001.md'
DRIVER_PROTOCOL_SHA='1f0ac342a18aa781994c60da0e950eea869a0ffaf46054a52e8bcb5f32787496'
np=P=None;PROVIDER_SCOPE={};RAW={};CONTROLS=[];EXACT_TARGETS={};COMPLETED={}

def sha(name):return hashlib.sha256((BASE/name).read_bytes()).hexdigest()
def keep(name,value):
 a=np.asarray(value).copy();assert a.dtype.kind in 'fiub' and np.all(np.isfinite(a));RAW[name]=a;return a
def check(name,actual,expected,envelope):
 assert all(w.shape==actual[0].shape and w.dtype==np.float64 for pair in (actual,expected) for w in pair)
 envelope=np.asarray(envelope).copy();assert envelope.shape==actual[0].shape and np.all(np.isfinite(envelope)) and np.all(envelope>0)
 for n,x in (('actual_hi',actual[0]),('actual_lo',actual[1]),('expected_hi',expected[0]),('expected_lo',expected[1]),('envelope',envelope)):keep(name+'_'+n,x)
 gap=P.a_sub(actual,expected);keep(name+'_gap_hi',gap[0]);keep(name+'_gap_lo',gap[1]);error=float(np.max((abs(gap[0])+abs(gap[1]))/envelope,initial=0))
 CONTROLS.append(dict(name=name,error=error,tolerance=2e-11,passed=error<=2e-11));assert error<=2e-11,(name,error)

def initialize():
 global np,P,PROVIDER_SCOPE
 import numpy as numpy
 np=numpy;names=list(PINS);trees=[ast.parse((BASE/f).read_text()) for f in names[:2]];maps=[{n.name:n for n in t.body if isinstance(n,ast.FunctionDef)} for t in trees]
 base={'a_keep','a_sum','a_split','a_prod','a_dd','a_add','a_sub','a_mul','a_mul64','a_stack','a_slice','a_div64'}
 scalar={'a_reshape','scalar_mask','scalar_lift','scalar_scatter','dd_scalar_scatter'}
 primitive={'a_matvec','a_transpose','normal_keep_pair','normal_pair_left','normal_pair_right','normal_pair_sandwich','normal_pair_sum','paired_current_affine_features','paired_current_affine_momenta'}
 for n in base:assert ast.dump(maps[0][n],include_attributes=False)==ast.dump(maps[1][n],include_attributes=False),n
 selected=[n for n in trees[0].body if isinstance(n,ast.FunctionDef) and n.name in base|scalar]+[n for n in trees[1].body if isinstance(n,ast.FunctionDef) and n.name in primitive];assert len(selected)==26
 PROVIDER_SCOPE=dict(np=np,DD_ARRAY_CURRENT={},capture=keep,B=1.,GC=1.,ALPHA=.02/1.98,ELL=.1,C=1.98)
 exec(compile(ast.Module(body=selected,type_ignores=[]),names[1],'exec'),PROVIDER_SCOPE)
 P=types.SimpleNamespace(**{n:PROVIDER_SCOPE[n] for n in base|scalar|primitive|{'B','GC','ALPHA','ELL','C'}});globals().update(vars(P))
 # Only function definitions are imported; no provider main or top-level math.
 for file,count in zip(names[2:],(11,20,8,7,5,8,3,1,1,6)):
  tree=ast.parse((BASE/file).read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)];assert len(defs)==count,file
  exec(compile(ast.Module(body=defs,type_ignores=[]),file,'exec'),globals())

def save_json(name,data):
 with (BASE/name).open('x') as f:json.dump(data,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
 (BASE/name).chmod(0o444);return dict(file=name,sha256=sha(name))

def main():
 assert AUTHOR_DRAFT is False and not AUTHORING_IN_PROGRESS and DRIVER_PROTOCOL_SHA is not None and not list(BASE.glob(STEM+'_*')),'Root exclusive reviewed release required'
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 owner=save_json(STEM+'_OWNER_START.json',dict(pid=os.getpid(),source_file=Path(__file__).name,source_sha256=sha(Path(__file__).name),pins=PINS,protocol_sha256=DRIVER_PROTOCOL_SHA))
 initialize();out=fresh_finite_mixed_normal_integration_control(keep,check);COMPLETED.update(out)
 assert len(CONTROLS)==7 and all(x['passed'] for x in CONTROLS) and out['native_terms_exactly_zero'] and out['relative_phase_count']==out['ordinary_label_count']==1
 name=STEM+'_POINT.npz'
 for n,x in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+n]=np.asarray(x).copy()
 with (BASE/name).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
 (BASE/name).chmod(0o444);point=dict(file=name,sha256=sha(name),fields=len(RAW))
 references=save_json(STEM+'_INDEPENDENT_REFERENCES.json',dict(precision=100,targets=EXACT_TARGETS,rounded_two_word_comparisons=True))
 for n,h in tuple(PINS.items())+((DRIVER_PROTOCOL,DRIVER_PROTOCOL_SHA),):assert sha(n)==h,n
 report=dict(status='NEW_SHARED_CANDIDATE_MIXED_FOUR_NORMAL_CONTROL_PASS',pid=os.getpid(),owner=owner,source_sha256=sha(Path(__file__).name),protocol_sha256=DRIVER_PROTOCOL_SHA,pins=PINS,point=point,independent_references=references,controls=CONTROLS,scope=out,all_four_normal_rows_and_direction_retained=True,original_action_or_source_changed=False,finite_constraints_or_physical_state_admitted=False)
 saved=save_json(STEM+'_RESULT.json',report);print(json.dumps(dict(status=report['status'],controls=len(CONTROLS),sha256=saved['sha256'])))
if __name__=='__main__':
 try:main()
 except BaseException:
  if np is not None:
   for n,x in PROVIDER_SCOPE.get('DD_ARRAY_CURRENT',{}).get('arrays',{}).items():RAW['last_arithmetic_'+n]=np.asarray(x).copy()
   if RAW:
    with (BASE/(STEM+'_ERROR_RAW.npz')).open('xb') as f:np.savez_compressed(f,**{n:np.asarray(x).copy() for n,x in RAW.items()})
    (BASE/(STEM+'_ERROR_RAW.npz')).chmod(0o444)
  save_json(STEM+'_ERROR.json',dict(status='FAILED',pid=os.getpid(),controls=CONTROLS,completed=COMPLETED,exact_targets=EXACT_TARGETS,traceback=traceback.format_exc()));raise
