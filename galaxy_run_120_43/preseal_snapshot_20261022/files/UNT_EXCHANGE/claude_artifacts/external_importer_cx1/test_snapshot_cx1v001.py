import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import snapshot_cx1v001 as S

root=Path(__file__).resolve().parent
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('snapshot_%Y%m%dT%H%M%S%f')
case.mkdir(parents=True,exist_ok=False)
p=case/'evidence.json'
with p.open('xb') as f:f.write(b'{"nested":{"value":7}}')
pin={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
reads=[]
def audit(event,args):
    if event=='open' and args[0]==str(p):reads.append(args)
sys.addaudithook(audit)
snap=S.Snapshot()
assert snap.document(pin)=={'nested':{'value':7}}
assert snap.hash(p)==pin['sha256']
assert snap.document(pin)=={'nested':{'value':7}}
assert len(reads)==1
passed=['single OS open for repeated pin/hash/parse']
for name,fn in [
 ('duplicate nested key',lambda:S.strict_json(b'{"a":{"b":1,"b":2}}')),
 ('NaN',lambda:S.strict_json(b'{"a":NaN}')),
 ('Infinity',lambda:S.strict_json(b'[Infinity]')),
 ('overflow number',lambda:S.strict_json(b'[1e999]')),
 ('invalid UTF8',lambda:S.strict_json(b'\xff')),
 ('trailing value',lambda:S.strict_json(b'{}{}')),
 ('extra pin field',lambda:snap.pin(dict(pin,extra=True))),
 ('wrong hash',lambda:snap.pin(dict(pin,sha256='0'*64))),
 ('relative path',lambda:snap.read('evidence.json')),
 ('missing file',lambda:snap.read(case/'absent.json')),
 ('directory',lambda:snap.read(case))]:
    try:fn()
    except S.Refusal:passed.append(name)
    else:raise AssertionError(name)
assert len(reads)==1
assert not issubclass(S.Refusal,Exception)
report={'status':'PASS','blocking_count':0,'scope':'snapshot utility only','tested':passed,
        'untested':['production integration','complete importer admission'],
        'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [Path(S.__file__),Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
