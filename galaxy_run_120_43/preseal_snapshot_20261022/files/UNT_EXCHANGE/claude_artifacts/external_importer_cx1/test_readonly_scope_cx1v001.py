import hashlib,json,types,sys,builtins
from pathlib import Path
from datetime import datetime,timezone
from readonly_scope_cx1v001 import ReadOnlyScope
from snapshot_cx1v001 import Snapshot,Refusal
root=Path(__file__).resolve().parent
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('scope_%Y%m%dT%H%M%S%f')
case.mkdir(parents=True,exist_ok=False)
p=case/'input.json'
with p.open('xb') as f:f.write(b'{"value":1}')
m=types.ModuleType('_private_fixture');m.__file__=str(case/'private.py')
exec("import json\nfrom pathlib import Path\ndef read(p):\n return json.loads(Path(p).read_bytes()),json.load(open(p)),Path(p).read_text()\ndef write(p):\n return open(p,'w')",m.__dict__)
child=types.ModuleType('_private_child');child.__file__=str(case/'child.py')
exec("from pathlib import Path\ndef read(p):return Path(p).read_bytes()",child.__dict__)
m.load_pinned_module=lambda *a,**kw:child
oldloader=m.load_pinned_module;oldpath=m.Path;oldjson=m.json;oldopen=builtins.open
opens=[]
def audit(event,args):
 if event=='open' and args[0]==str(p):opens.append(args)
sys.addaudithook(audit)
snapshot=Snapshot();passed=[]
with ReadOnlyScope(snapshot,[m]):
 assert m.read(p)==({'value':1},{'value':1},'{"value":1}')
 assert m.load_pinned_module().read(p)==b'{"value":1}'
 assert len(opens)==1
 passed.append('module and dynamic dependency share one OS read')
 try:m.write(case/'forbidden')
 except Refusal:passed.append('write refused')
 else:raise AssertionError('write allowed')
 assert not (case/'forbidden').exists()
 assert builtins.open is oldopen
 passed.append('global builtins untouched')
assert m.Path is oldpath and m.json is oldjson and m.load_pinned_module is oldloader and 'open' not in m.__dict__
assert child.Path is Path
passed.append('all namespaces restored')
try:
 with ReadOnlyScope(Snapshot(),[m]):raise RuntimeError('test unwind')
except RuntimeError:pass
assert m.Path is oldpath and 'open' not in m.__dict__
passed.append('exception restoration')
report={'status':'PASS','blocking_count':0,'scope':'IO adapter utility only','tested':passed,
'untested':['real certificate-chain transitive read coverage','private-module ownership enforcement','production integration'],
'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [root/'readonly_scope_cx1v001.py',Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
