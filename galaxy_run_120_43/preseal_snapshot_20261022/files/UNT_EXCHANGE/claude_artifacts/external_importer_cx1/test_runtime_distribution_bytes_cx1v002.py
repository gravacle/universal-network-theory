from pathlib import Path
import tempfile,json,hashlib
from runtime_distribution_bytes_cx1v002 import capture_bytes
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='distribution_bytes_',dir=b/'inert_fixtures'))
def fixture(label,native=b'NATIVE',cache=b'CACHE',dylib=b'DYLIB'):
 site=c/label;site.mkdir()
 data={'numpy/__init__.py':b'INERT','numpy/core.so':native,'numpy/.dylibs/lib.dylib':dylib,'numpy/__pycache__/x.pyc':cache,'numpy/extra.txt':b'EXTRA'}
 for name,raw in data.items():
  p=site/name;p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('xb') as f:f.write(raw)
 return capture_bytes(site_root=site,owned_roots=[site/'numpy'],record_relative_files=['numpy/__init__.py','numpy/core.so','numpy/.dylibs/lib.dylib'])
a=fixture('a');same=fixture('same');assert a['sha256']==same['sha256'];passed=['identical bytes equal across roots']
assert fixture('native',native=b'CHANGED')['sha256']!=a['sha256'];passed.append('extension bytes change equality')
assert fixture('dylib',dylib=b'CHANGED')['sha256']!=a['sha256'];passed.append('bundled dylib bytes change equality')
cache=fixture('cache',cache=b'CHANGED');assert cache['sha256']==a['sha256'] and cache['files']!=a['files'];passed.append('pycache recorded but excluded')
assert next(e for e in a['files'] if e['path']=='numpy/extra.txt')['outside_RECORD'];passed.append('unlisted file explicitly recorded')
r=dict(status='PASS',blocking_count=0,scope='Inert installed-file bytes only',tested=passed,untested=['Complete distribution root ownership discovery','Full runtime capture integration','Concurrent mutation stress tests'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'runtime_distribution_bytes_cx1v002.py',Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
