"""Private loader bootstrap tests using inert source files only."""
from pathlib import Path
import json,hashlib,tempfile,sys,copy
from pinned_helper_loader_cx1v001 import prepare
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='helper_loader_',dir=b/'inert_fixtures'))
def create(name,text):
 p=c/(name+'.py')
 with p.open('x') as f:f.write(text)
 return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
components={'inert_leaf.py':create('inert_leaf','VALUE=19\n'),'inert_root.py':create('inert_root','from inert_leaf import VALUE\nRESULT=VALUE+1\n')}
load=prepare(components);assert load('inert_root').RESULT==20 and load('inert_leaf') is load('inert_leaf')
assert 'inert_leaf' not in sys.modules and 'inert_root' not in sys.modules
passed=['pinned local import resolves privately','modules cached privately without global sys.modules changes']
bad=copy.deepcopy(components);bad['inert_leaf.py']['sha256']='0'*64
try:prepare(bad)
except ValueError:passed.append('wrong hash refuses before helper execution')
else:raise AssertionError('hash')
unknown={'inert_unknown.py':create('inert_unknown','import unavailable_inert_dependency\n')}
try:prepare(unknown)
except ValueError:passed.append('unlisted nonstdlib import refuses during preflight')
else:raise AssertionError('import')
# Every source compiles before any execution, even when an earlier helper would raise.
invalid={'inert_raise.py':create('inert_raise',"raise AssertionError('must not execute')\n"),'inert_syntax.py':create('inert_syntax','def broken(\n')}
try:prepare(invalid)
except SyntaxError:passed.append('whole inventory compiles before execution')
else:raise AssertionError('syntax')
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Full actual helper graph loading','Separate root-authenticated entry','Dynamic private parent loaders and producer IO'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'pinned_helper_loader_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')
