"""0541: current generated entry points reject import before seal; all functions have entry decorators."""
import ast,hashlib,json,runpy
from pathlib import Path
R=Path(__file__).parent;reg=json.loads((R/'GUARDED_SUCCESSORS_0541_V001.json').read_bytes());checks=[]
assert not (R/'ROOT_SEAL_ADMISSION_V001.json').exists(),'TEST_REQUIRES_NO_PRODUCTION_SEAL_ADMISSION'
for ref in reg['files']:
 p=Path(ref['path']);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==ref['sha256'];tree=ast.parse(raw)
 functions=[n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)]
 guarded=all(any(isinstance(d,ast.Attribute) and isinstance(d.value,ast.Name) and d.value.id=='_root_guard' and d.attr=='guarded' for d in n.decorator_list) for n in functions)
 try:runpy.run_path(str(p),run_name='test_guarded_import');refused=False
 except PermissionError as e:refused=str(e)=='ROOT_SEAL_ADMISSION_PENDING'
 checks.append({'file':ref,'function_count':len(functions),'every_function_guarded':guarded,'preseal_import_refused':refused,'passed':guarded and refused})
with (R/'GUARDED_ENTRYPOINT_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED source and preseal refusal; no production functions executed','checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)},f,indent=1)
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
