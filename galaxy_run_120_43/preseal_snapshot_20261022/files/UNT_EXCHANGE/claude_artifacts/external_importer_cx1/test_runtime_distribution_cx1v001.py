import tempfile,types,json,hashlib,copy
from pathlib import Path
from runtime_distribution_cx1v001 import capture_distribution,compare_distributions
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='distribution_',dir=b/'inert_fixtures'))
site=c/'site';site.mkdir();info=site/'numpy-1.dist-info';info.mkdir();record=info/'RECORD'
with record.open('x') as f:f.write('INERT RECORD BYTES\n')
def dist(files=('numpy-1.dist-info/RECORD',),version='1'):
 return types.SimpleNamespace(metadata={'Name':'NumPy'},version=version,files=files,locate_file=lambda x:site/x)
r=capture_distribution(dist(),site_root=site);assert r['name']=='numpy' and r['record']['sha256']==hashlib.sha256(record.read_bytes()).hexdigest()
assert compare_distributions([r],[copy.deepcopy(r)]);passed=['RECORD byte hash and canonical name','same distribution identity']
for name,d in [('missing_RECORD',dist(files=[])),('duplicate_RECORD',dist(files=['numpy-1.dist-info/RECORD']*2)),('missing_version',dist(version=''))]:
 try:capture_distribution(d,site_root=site)
 except ValueError:passed.append(name)
 else:raise AssertionError(name)
for field in ['version','hash']:
 bad=copy.deepcopy(r)
 if field=='version':bad['version']='2'
 else:bad['record']['sha256']='0'*64
 try:compare_distributions([r],[bad])
 except ValueError:passed.append('changed_'+field)
 else:raise AssertionError(field)
report=dict(status='PASS',blocking_count=0,tested=passed,scope='Inert distribution metadata and RECORD bytes only',untested=['Isolated interpreter distribution discovery','Runtime producer integration','Installed packages and launch capture'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'runtime_distribution_cx1v001.py',Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
