"""Real isolated interpreter metadata and PathFinder; fabricated packages only."""
import sys,types,hashlib,json,tempfile
from pathlib import Path
from importlib import metadata
from importlib.machinery import PathFinder
PINS={'runtime_fingerprints_cx1v002': '5ec4f8c652917321c449d84b3272ed6f97504b002312ba8d89da583c1b00fc31', 'runtime_distribution_cx1v001': 'ce5f784dbe2d328a614df2ce2fa6dc24b89817678846c70c0fccef9e98a11228', 'runtime_distribution_bytes_cx1v002': '5fd62a00dbe4c0acc1e7aee2f2e62dfe1d34d5783a7d08a861364fdb4867ee1e', 'runtime_distribution_owned_bytes_cx1v001': 'e8642cfa161a3f20f5e3acfc5f3e13f20dd9b67b733d462e1fc83940faa56155', 'runtime_distribution_discovery_cx1v002': '1127eff447c2de74202ea1a36efb7d5f97c8039e74248ba51703276f46d3fbb2'}
b=Path(__file__).resolve().parent
assert sys.flags.isolated and sys.flags.dont_write_bytecode
for name,sha in PINS.items():
 path=b/(name+'.py');raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==sha
 module=types.ModuleType(name);module.__file__=str(path);sys.modules[name]=module;exec(compile(raw,str(path),'exec'),module.__dict__)
c=Path(tempfile.mkdtemp(prefix='real_metadata_',dir=b/'inert_fixtures'));site=c/'site';site.mkdir()
for name in ('numpy','scipy'):
 (site/name).mkdir();info=site/(name+'-1.0.dist-info');info.mkdir()
 contents={name+'/__init__.py':'raise AssertionError("INERT PACKAGE MUST NEVER EXECUTE")\n',name+'-1.0.dist-info/METADATA':'Metadata-Version: 2.1\nName: '+name+'\nVersion: 1.0\n',name+'-1.0.dist-info/top_level.txt':name+'\n'}
 contents[name+'-1.0.dist-info/RECORD']=''.join(p+',,\n' for p in sorted(list(contents)+[name+'-1.0.dist-info/RECORD']))
 for path,text in contents.items():
  with (site/path).open('x') as f:f.write(text)
(site/'numpy.libs').mkdir()
with (site/'numpy.libs'/'inert.so').open('xb') as f:f.write(b'INERT NATIVE')
old_path=list(sys.path)
try:
 sys.path[:]=[str(site)]+[p for p in old_path if 'site-packages' not in p and 'dist-packages' not in p]
 assert metadata.packages_distributions()['numpy']==['numpy']
 result=sys.modules['runtime_distribution_discovery_cx1v002'].discover(import_roots=['numpy','math'],stdlib_names=sys.stdlib_module_names,search_path=[str(site)],metadata=metadata,find_spec=PathFinder.find_spec)
finally:sys.path[:]=old_path
assert {r['name'] for r in result['distributions']}=={'numpy','scipy'}
assert 'numpy' not in sys.modules and 'scipy' not in sys.modules
assert any(f['path']=='numpy.libs/inert.so' and f['outside_RECORD'] for r in result['distributions'] for f in r['files'])
report=dict(status='PASS',blocking_count=0,scope=__doc__,tested=['Actual importlib.metadata maps fabricated distributions','Actual PathFinder resolves package origins without package execution','Byte route includes unlisted bundled native library','Required scipy included'],untested=['Real installed package layout including outside-site scripts','Production capture and importer integration'],pins=[dict(path=str(b/(n+'.py')),sha256=sha) for n,sha in PINS.items()]+[dict(path=str(Path(__file__)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
