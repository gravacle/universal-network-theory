"""Read-only saved final compare verification. Caller authenticates root pins.
Never executes snapshot/compare CLI, observes current files, or writes END/events.
"""
import ast,copy
from envelope_observation_adapter_cx1v002 import build
from snapshot_cx1v001 import Refusal
from request_guard_cx1v002 import require

def comparator(raw,path):
 m,_=build(raw,path);tree=ast.parse(raw)
 fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='compare')
 start=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Expr) and any(isinstance(v,ast.Constant) and isinstance(v.value,str) and v.value.startswith('START_NOT_LABELLED') for v in ast.walk(n)))
 end=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(v,ast.Name) and v.id=='verdict' for v in n.targets))
 f=ast.parse("def compare_saved(s,e):\n pass\n").body[0];f.body=copy.deepcopy(fn.body[start:end+1])
 f.body+=ast.parse("return dict(problems=problems,notes=notes,verdict=verdict)").body
 exec(compile(ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[])),path+'#saved-final-readonly','exec'),m.__dict__)
 return m

def check(snapshot,*,tool_pin,start_pin,end_pin,report_pin,pinset_pin):
 m=comparator(snapshot.pin(tool_pin),tool_pin['path'])
 def signed(p,schema):
  obj=snapshot.document(p);require(type(obj) is dict and obj.get('schema')==schema,'FINAL_SCHEMA')
  body={k:v for k,v in obj.items() if k!='body_sha256'}
  require(obj.get('body_sha256')==m.sha_b(m.canon(body).encode('ascii')),'FINAL_BODY_SHA')
  require(obj.get('phase')=='L2_DIRECT','FINAL_PHASE');return obj
 ps=signed(pinset_pin,m.SCHEMA_PINSET);s=signed(start_pin,m.SCHEMA_MANIFEST);e=signed(end_pin,m.SCHEMA_MANIFEST);r=signed(report_pin,m.SCHEMA_COMPARE)
 require(ps.get('unresolved_pins')==s.get('unresolved_pins')==e.get('unresolved_pins')==[],'FINAL_UNRESOLVED')
 binding=dict(path=pinset_pin['path'],file_sha256=pinset_pin['sha256'],body_sha256=ps['body_sha256'])
 require(s.get('pin_set')==e.get('pin_set')==r.get('pin_set')==binding,'FINAL_PINSET_BINDING')
 for name,p,obj in [('start',start_pin,s),('end',end_pin,e)]:
  require(r.get(name)==dict(path=p['path'],file_sha256=p['sha256'],body_sha256=obj['body_sha256'],created_utc=obj.get('created_utc')),'FINAL_MANIFEST_BINDING:'+name)
 try:actual=m.compare_saved(s,e)
 except m.Refusal as exc:raise Refusal('FINAL_COMPARE_REFUSED:'+str(exc)) from exc
 require(all(r.get(k)==v for k,v in actual.items()),'FINAL_REPORT_RECOMPUTATION')
 require(r.get('unresolved_pins_not_checked')==0,'FINAL_REPORT_UNRESOLVED')
 return dict(storage_event_kind='FINAL_PASS' if actual['verdict']=='OK' else 'FINAL_INVALIDATE',prerequisites_only=True,report=dict(report_pin),production_END_executed=False)
