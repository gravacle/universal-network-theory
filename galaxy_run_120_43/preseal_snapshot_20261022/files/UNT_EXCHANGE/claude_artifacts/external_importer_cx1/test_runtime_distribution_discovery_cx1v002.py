import tempfile,types,json,hashlib
from pathlib import Path
from runtime_distribution_discovery_cx1v002 import discover
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='distribution_discovery_',dir=b/'inert_fixtures'));site=c/'site';site.mkdir()
for name in ['numpy','scipy']:
 (site/name).mkdir();(site/(name+'-1.dist-info')).mkdir()
 for relative in [name+'/__init__.py',name+'-1.dist-info/RECORD']:
  with (site/relative).open('x') as f:f.write('INERT NOT EXECUTED')
(site/'numpy.libs').mkdir()
with (site/'numpy.libs'/'native.so').open('xb') as f:f.write(b'INERT NATIVE BYTES')
def distribution(name):return types.SimpleNamespace(metadata={'Name':name},version='1',files=[name+'/__init__.py',name+'-1.dist-info/RECORD'],locate_file=lambda x:site/x)
def meta(mapping):return types.SimpleNamespace(packages_distributions=lambda:mapping,distribution=distribution)
args=dict(import_roots=['numpy','math'],stdlib_names={'math'},search_path=[str(site)],metadata=meta({'numpy':['numpy'],'scipy':['scipy']}),find_spec=lambda n,p:types.SimpleNamespace(origin=str(site/n/'__init__.py')))
r=discover(**args)
np=next(x for x in r['distributions'] if x['name']=='numpy')
assert any(f['path']=='numpy.libs/native.so' and f['outside_RECORD'] for f in np['files'])
assert [x['name'] for x in r['distributions']]==['numpy','scipy'];passed=['numpy and required scipy resolved without importing either']
for name,override in [('missing_mapping',{'metadata':meta({'numpy':['numpy']})}),('ambiguous_mapping',{'metadata':meta({'numpy':['numpy','other'],'scipy':['scipy']})}),('wrong_owner',{'metadata':meta({'numpy':['scipy'],'scipy':['scipy']})}),('namespace_origin',{'find_spec':lambda n,p:types.SimpleNamespace(origin=None)})]:
 try:discover(**{**args,**override})
 except ValueError:passed.append(name)
 else:raise AssertionError(name)
report=dict(status='PASS',blocking_count=0,tested=passed,scope='Inert distribution metadata and fabricated resolver results; package code never executed',untested=['Actual isolated importlib.metadata and PathFinder discovery','Full runtime capture integration','Outside-site installed scripts currently refuse'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'runtime_distribution_discovery_cx1v002.py',b/'runtime_distribution_cx1v001.py',b/'runtime_distribution_owned_bytes_cx1v001.py',b/'runtime_distribution_bytes_cx1v002.py',Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
