import runpy,types,tempfile,json,hashlib
from pathlib import Path
b=Path(__file__).resolve().parent
entry=b/'runtime_capture_entry_cx1v003.py'
g=runpy.run_path(str(entry));strict=g['strict'];passed=[]
for value in [b'{"x":1e999}',b'{"x":NaN}',b'{"x":1,"x":2}']:
 try:strict(value)
 except ValueError:passed.append('strict rejects '+value.decode())
 else:raise AssertionError(value)
case=Path(tempfile.mkdtemp(prefix='capture_branch_',dir=b/'inert_fixtures'))
policy=runpy.run_path(str(b/'runtime_policy_cx1v002.py'))
p=types.SimpleNamespace(**policy)
inv=dict(schema='CX1_RUNTIME_INVENTORY_V001',module_names=['numpy','scipy'],unresolved_dynamic=[],audit_complete=True)
for mode in ['valid_double','missing_api','environment_change','module_change','existing_output']:
 f=runpy.run_path(str(entry))['capture'];ns=f.__globals__
 env={'PATH':'/inert','PRIVATE_SECRET':'never record'}
 modules={'runtime_policy_cx1v002':p,'numpy':types.ModuleType('numpy'),'scipy':types.ModuleType('scipy')}
 fake_sys=types.SimpleNamespace(platform='darwin',executable='/INERT/python',version='INERT',flags=types.SimpleNamespace(isolated=1,dont_write_bytecode=1),modules=modules)
 if mode!='missing_api':fake_sys.stdlib_module_names=set()
 ns['sys']=fake_sys;ns['os']=types.SimpleNamespace(environ=env)
 ns['importlib']=types.SimpleNamespace(import_module=lambda name:modules[name])
 ns['subprocess']=types.SimpleNamespace(run=lambda *a,**k:types.SimpleNamespace(stdout='INERT_PLATFORM'))
 seen=[]
 def assemble(**kw):
  seen.append(kw)
  assert 'PRIVATE_SECRET' not in kw['inherited_environment']
  if mode=='module_change':modules['unexpected']=types.ModuleType('unexpected')
  return {'fixture_only':True}
 ns['load_helpers']=lambda:types.SimpleNamespace(assemble=assemble)
 if mode=='environment_change':
  def imp(name):env['OMP_NUM_THREADS']='9';return modules[name]
  ns['importlib']=types.SimpleNamespace(import_module=imp)
 out=case/(mode+'.json')
 if mode=='existing_output':
  with out.open('x') as h:h.write('PRESERVE')
 a=types.SimpleNamespace(output=str(out),inventory='/INERT/inventory',inventory_sha256='0'*64)
 try:f(a,inv)
 except ValueError:
  assert mode!='valid_double',mode
  if mode=='existing_output':assert out.read_text()=='PRESERVE'
  else:assert not out.exists()
 else:assert mode=='valid_double' and json.loads(out.read_text())['fixture_only']
 passed.append(mode)
report=dict(status='PASS',blocking_count=0,scope='Strict JSON and capture control flow with fabricated interpreter, modules, environment, platform and assembly; no real launch capture',tested=passed,untested=['Real module resolution/fingerprinting through CLI','Reviewed complete dynamic inventory','Launch authentication','Production integration'],pins=[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in [entry,Path(__file__)]])
with (case/'TEST_REPORT.json').open('x') as h:json.dump(report,h,indent=2);h.write('\n')
print(case/'TEST_REPORT.json')
