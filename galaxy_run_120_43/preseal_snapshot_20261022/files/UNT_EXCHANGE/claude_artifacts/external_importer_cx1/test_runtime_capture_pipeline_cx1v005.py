"""End-to-end capture plumbing with real metadata/bytes and inert runtime/platform/code pins."""
import sys,runpy,types,tempfile,json,hashlib
from pathlib import Path
b=Path(__file__).resolve().parent;entry=b/'runtime_distribution_capture_cx1v004.py'
g=runpy.run_path(str(entry));g['prepare']()
c=Path(tempfile.mkdtemp(prefix='capture_pipeline_',dir=b/'inert_fixtures'));site=c/'site';site.mkdir();(c/'bin').mkdir()
for name in ('numpy','scipy'):
 (site/name).mkdir();(site/(name+'-1.dist-info')).mkdir()
 contents={name+'/__init__.py':'raise AssertionError("MUST NEVER EXECUTE")\n',name+'-1.dist-info/METADATA':'Metadata-Version: 2.1\nName: '+name+'\nVersion: 1\n',name+'-1.dist-info/top_level.txt':name+'\n',name+'/inert.so':'NATIVE FIXTURE'}
 if name=='numpy':contents['../bin/f2py']='INERT SCRIPT NEVER EXECUTED'
 contents[name+'-1.dist-info/RECORD']=''.join(p+',,\n' for p in sorted(list(contents)+[name+'-1.dist-info/RECORD']))
 for p,t in contents.items():
  with (site/p).open('x') as f:f.write(t)
pins={}
for name in ['interpreter','driver','monitor']:
 p=c/name
 with p.open('xb') as f:f.write(('INERT '+name).encode())
 pins[name]=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
func=g['capture'];ns=func.__globals__
ns['sys']=types.SimpleNamespace(platform='darwin',prefix=str(c),flags=sys.flags,version='INERT',executable=pins['interpreter']['path'],modules=sys.modules,path=[str(site)],stdlib_module_names=sys.stdlib_module_names)
ns['os']=types.SimpleNamespace(environ={'PATH':'/INERT','SECRET':'DO_NOT_RECORD','PYTHON_TEST':'remove'})
ns['subprocess']=types.SimpleNamespace(run=lambda *a,**k:types.SimpleNamespace(stdout='INERT_PLATFORM'))
ns['SOURCE_PINS']=[pins['driver']];ns['MONITOR_PIN']=pins['monitor']
old=list(sys.path);output=c/'capture.json'
try:
 sys.path[:]=[str(site)]+[p for p in old if 'site-packages' not in p and 'dist-packages' not in p]
 func(str(output),['numpy','math'])
finally:sys.path[:]=old
record=json.loads(output.read_text());assert record['interpreter']['sha256']==pins['interpreter']['sha256']
assert record['driver']['sha256']==pins['driver']['sha256'] and record['monitor']['sha256']==pins['monitor']['sha256']
assert 'SECRET' not in record['effective_environment'] and 'PYTHON_TEST' not in record['effective_environment']
assert 'numpy' not in sys.modules and 'scipy' not in sys.modules
assert any(f['path']=='prefix:bin/f2py' and not f['excluded_from_equality'] for d in record['distributions'] for f in d['files'])
assert record['launch_association']=='REQUIRES_ROOT_BINDING'
validate=sys.modules['runtime_distribution_record_cx1v004'].validate;validate(record)
before=output.read_bytes()
try:func(str(output),['numpy'])
except ValueError:pass
else:raise AssertionError('existing output accepted')
assert output.read_bytes()==before
from importlib import metadata
real=next(d for d in metadata.distributions(path=[str(site)]) if d.metadata['Name']=='numpy')
owned=sys.modules['runtime_distribution_owned_bytes_cx1v003'].capture_distribution
for mode in ['stale_version','stale_file_list']:
 fake=types.SimpleNamespace(metadata={'Name':'numpy'},version='WRONG' if mode=='stale_version' else real.version,files=list(real.files)+(['invented.py'] if mode=='stale_file_list' else []),locate_file=real.locate_file)
 try:owned(fake,site_root=site,prefix_root=c)
 except ValueError:pass
 else:raise AssertionError(mode)
report=dict(status='PASS',blocking_count=0,scope=__doc__,tested=['Real metadata discovery through capture function','Real installed-file bytes and runtime pin assembly','Environment normalization and secret exclusion','No numpy/scipy package execution','Exclusive existing-output refusal','Stale package version refuses','Stale distribution file list refuses','D001 explicit console script included in prefix namespace'],untested=['Actual installed package layout','Actual platform commands or launch-time capture','Root authentication and importer integration'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [entry,Path(__file__),output]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
