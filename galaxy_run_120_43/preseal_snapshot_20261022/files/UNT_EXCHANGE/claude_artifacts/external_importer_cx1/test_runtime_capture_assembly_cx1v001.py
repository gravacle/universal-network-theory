import tempfile,types,json,hashlib,copy
from pathlib import Path
from runtime_capture_assembly_cx1v001 import assemble
from runtime_policy_cx1v001 import RuntimeRefusal
root=Path(__file__).resolve().parent;case=Path(tempfile.mkdtemp(prefix='capture_assembly_',dir=root/'inert_fixtures'))
exe=case/'python';exe.write_bytes(b'INERT EXECUTABLE')
modules={}
for name in ('numpy','scipy'):
 p=case/(name+'.py');p.write_bytes(('INERT '+name).encode());m=types.ModuleType(name);m.__file__=str(p);m.__version__='fixture';modules[name]=m
inventory={'schema':'CX1_RUNTIME_INVENTORY_V001','module_names':['numpy','scipy'],'unresolved_dynamic':[]}
args=dict(inventory=inventory,resolved_modules=modules,package_roots=modules,inherited_environment={'SECRET':'MUST_NOT_RECORD','PATH':'/fixture'},interpreter_path=str(exe),sys_version='fixture',sys_flags={'isolated':1,'dont_write_bytecode':1},stdlib_names=set(),macos_build='FIXTURE',hardware_model='FIXTURE',captured_utc='2026-01-01T00:00:00Z',producer_pin={'path':str(root/'runtime_capture_assembly_cx1v001.py'),'sha256':hashlib.sha256((root/'runtime_capture_assembly_cx1v001.py').read_bytes()).hexdigest()})
r=assemble(**args);assert r['coverage_complete'] and 'SECRET' not in r['effective_environment'];passed=['complete inert inventory assembles byte fingerprints without recording unrelated environment']
for name,over in [('unresolved dynamic',dict(inventory={**inventory,'unresolved_dynamic':['loader']})),('missing module',dict(resolved_modules={'numpy':modules['numpy']})),('nonisolated',dict(sys_flags={'isolated':0,'dont_write_bytecode':1})),('bytecode enabled',dict(sys_flags={'isolated':1,'dont_write_bytecode':0})),('DYLD inherited',dict(inherited_environment={'DYLD_LIBRARY_PATH':'/fixture'}))]:
 try:assemble(**{**args,**over})
 except RuntimeRefusal:passed.append(name+' refuses')
 else:raise AssertionError(name)
report=dict(status='PASS',blocking_count=0,scope='Capture assembly with fabricated runtime facts and modules',tested=passed,untested=['Actual capture CLI and isolated import resolution','Audited complete dynamic inventory','Launch-time platform/environment collection and authentication'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),root/'runtime_capture_assembly_cx1v001.py']])
p=case/'TEST_REPORT.json'
with p.open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(p)
