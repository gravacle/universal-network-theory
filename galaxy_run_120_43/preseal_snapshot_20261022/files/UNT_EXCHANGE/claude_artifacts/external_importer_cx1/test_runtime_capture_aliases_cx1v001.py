"""Real assembly/fingerprints, synthetic modules/interpreter and platform/import doubles."""
import runpy,types,tempfile,json,hashlib,sys
from pathlib import Path
b=Path(__file__).resolve().parent;entry=b/'runtime_capture_entry_cx1v003.py'
original=runpy.run_path(str(entry));assembly=original['load_helpers']()
policy=sys.modules['runtime_policy_cx1v002']
case=Path(tempfile.mkdtemp(prefix='capture_fingerprints_',dir=b/'inert_fixtures'))
exe=case/'inert_interpreter'
with exe.open('xb') as f:f.write(b'INERT NOT EXECUTABLE')
passed=[]
for mode in ['valid','missing_version','alias','unbound_alias','impostor_alias','missing_file']:
 modules={}
 for name in ['numpy','scipy']:
  path=case/(mode+'_'+name+'.py')
  with path.open('xb') as f:f.write(('INERT MODULE BYTES '+name).encode())
  module=types.ModuleType(name);module.__file__=str(path);module.__version__='INERT-1'
  modules[name]=module
 if mode=='missing_version':del modules['scipy'].__version__
 if mode=='alias':modules['alias_numpy']=modules['numpy']
 if mode=='unbound_alias':modules['alias_numpy']=modules.pop('numpy')
 if mode=='impostor_alias':
  m=types.ModuleType('numpy');m.__file__=modules['numpy'].__file__;m.__version__='INERT-1';modules['alias_numpy']=m
 if mode=='missing_file':modules['scipy'].__file__=str(case/'does_not_exist')
 modules['runtime_policy_cx1v002']=policy
 func=runpy.run_path(str(entry))['capture'];ns=func.__globals__
 ns['sys']=types.SimpleNamespace(platform='darwin',executable=str(exe),version='INERT VERSION',stdlib_module_names=set(),flags=types.SimpleNamespace(isolated=1,dont_write_bytecode=1),modules=modules)
 ns['os']=types.SimpleNamespace(environ={'PATH':'/fixture','PYTHON_TEST':'removed','SECRET':'not recorded'})
 ns['importlib']=types.SimpleNamespace(import_module=lambda name:modules.get(name))
 ns['subprocess']=types.SimpleNamespace(run=lambda *a,**kw:types.SimpleNamespace(stdout='INERT PLATFORM'))
 ns['load_helpers']=lambda:assembly
 out=case/(mode+'.json');args=types.SimpleNamespace(output=str(out),inventory='/INERT/inventory',inventory_sha256='0'*64)
 inv=dict(schema='CX1_RUNTIME_INVENTORY_V001',module_names=['numpy','scipy'],audit_complete=True,unresolved_dynamic=[])
 try:func(args,inv)
 except (ValueError,OSError):
  assert mode not in ('valid','alias'),mode
  assert not out.exists()
 else:
  assert mode in ('valid','alias'),mode
  r=json.loads(out.read_text())
  assert r['interpreter']['sha256']==hashlib.sha256(exe.read_bytes()).hexdigest()
  assert 'SECRET' not in r['effective_environment'] and 'PYTHON_TEST' not in r['effective_environment']
  assert r['launch_association']=='REQUIRES_ROOT_BINDING'
  for record in r['modules']:
   assert record['sha256']==hashlib.sha256(Path(modules[record['name']].__file__).read_bytes()).hexdigest()
  if mode=='alias':
   alias=next(m for m in r['modules'] if m['name']=='alias_numpy');assert alias['canonical_name']=='numpy'
   policy.compare_records(r,r)
   bad=json.loads(json.dumps(r));next(m for m in bad['modules'] if m['name']=='alias_numpy')['canonical_name']='scipy'
   try:policy.compare_records(r,bad)
   except ValueError:pass
   else:raise AssertionError('tampered alias accepted')
 passed.append(mode)
report=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Actual isolated package imports','Complete dynamic driver inventory','Launch capture/authentication','Actual standard-library and third-party alias resolution'],pins=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [entry,Path(__file__)]+[b/(n+'.py') for n in original['HELPERS']]])
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
