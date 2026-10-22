import sys,tempfile,hashlib,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from invocation_interpreter_cx1v001 import check
from snapshot_cx1v001 import Snapshot
from request_guard_cx1v002 import Refusal
b=Path(__file__).parent;f=Path(tempfile.mkdtemp(prefix='python_association_',dir=b/'inert_fixtures'))
binary=f/'inert_binary';binary.write_bytes(b'NOT EXECUTABLE: INERT BYTES')
alias=f/'python';alias.symlink_to(binary)
identity=dict(realpath=str(binary),sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
cases=[('canonical',str(binary),identity,True),('alias spelling preserved',str(alias),identity,True),('foreign hash',str(alias),dict(identity,sha256='0'*64),False),('foreign realpath',str(alias),dict(identity,realpath=str(f/'other')),False),('relative', 'python',identity,False),('missing',str(f/'missing'),identity,False),('extra identity field',str(alias),dict(identity,extra=True),False)]
results=[]
for name,python,i,expected in cases:
 try:
  result=check(Snapshot(),python=python,identity=i);ok=True;assert result['python']==python
 except Refusal:ok=False
 assert ok==expected,name
 results.append(dict(name=name,status='PASS'))
with (f/'TEST_REPORT.json').open('x') as h:json.dump(results,h,indent=2)
print(f/'TEST_REPORT.json')
