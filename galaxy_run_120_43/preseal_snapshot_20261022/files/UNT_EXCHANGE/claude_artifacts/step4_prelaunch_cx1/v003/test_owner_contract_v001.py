import ast,hashlib,json,types
from pathlib import Path
HERE=Path(__file__).parent;B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');P=HERE/'step4_guard_cx1v009.py'
g=types.ModuleType('guard009');g.__file__=str(P);exec(compile(P.read_bytes(),str(P),'exec'),g.__dict__)
rels=['calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4.py','calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py','calib_tail_readiness_cx2/v006r10_c4/adoption_policy_cx2v006r10_c4.py','calib_tail_readiness_cx2/v006r8/sensitivity_policy_cx2v006r8_v002.py','calib_tail_readiness_cx2/certificates_per_point/certificate_guard_cx2v003.py','calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py','calib_tail_readiness_cx2/v006r9/calibration_orchestrator_cx2v006r9.py','calib_tail_readiness_cx2/v006r9/calibration_core_cx2v006r9.py']
sources={str(B/r):hashlib.sha256((B/r).read_bytes()).hexdigest() for r in rels};cfg={'sources':sources};checks=[]
def check(name,fn,reason=None):
 try:fn();ok=reason is None;detail='passed'
 except Exception as e:detail=str(e);ok=reason is not None and reason in detail
 checks.append({'name':name,'passed':ok,'detail':detail})
def load(rel):
 with g.fence(sources):return g.load(g.pin(B/rel),cfg,'_owner_probe')
check('actual_r10_wrapper_import',lambda:load(rels[0]))
check('old_r9_owner_refused',lambda:load(rels[6]),'PREFLIGHT_COMPILE_HASH_MISMATCH')
raw=(B/rels[0]).read_text();t=ast.parse(raw);lit=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_resolve_source' for x in n.targets))
def altered():
 with g.fence(sources):compile(lit+'\n',str(B/rels[0]),'exec')
check('changed_generated_literal_refused',altered,'PREFLIGHT_COMPILE_HASH_MISMATCH')
def missing():
 with g.fence({k:v for k,v in sources.items() if k!=str(B/rels[0])}):compile(lit,str(B/rels[0]),'exec')
check('unregistered_owner_refused',missing,'PREFLIGHT_COMPILE_HASH_MISMATCH')
def eqfunc(name):
 def segment(p):
  s=p.read_text();return ast.get_source_segment(s,next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name==name))
 assert segment(P)==segment(B/'step4_launch_packet_cx1/impl/step4_guard_cx1v007.py')
check('native_preflight_function_unchanged',lambda:eqfunc('native_preflight'))
check('fence_function_unchanged',lambda:eqfunc('fence'))
assert hashlib.sha256(lit.encode()).hexdigest()=='79e8936d96103b1540987a980b289b6d25e5e25941b02db647f7a833818da0e1'
r={'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'scope':'Actual native module import only; no Context construction/data/science. Explicit refusal controls; production admission UNTESTED.','sources':sources,'guard':g.pin(P),'test':g.pin(__file__)}
with (HERE/'OWNER_RESULTS_V001.json').open('x') as f:json.dump(r,f,indent=2)
print(json.dumps({'passed':r['passed'],'total':r['total'],'checks':checks}));assert all(c['passed'] for c in checks)
