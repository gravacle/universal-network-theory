"""Private loader bootstrap tests using inert source files only."""
from pathlib import Path
import json,hashlib,tempfile,sys,copy
from pinned_helper_loader_cx1v002 import prepare
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
import numpy as np
npcomp={'inert_numpy.py':create('inert_numpy','import numpy as np\nVALUE=np.arange(3).tolist()\n')}
try:prepare(npcomp)
except ValueError:passed.append('NumPy requires explicit runtime module binding')
else:raise AssertionError('implicit numpy')
assert prepare(npcomp,runtime_modules={'numpy':np})('inert_numpy').VALUE==[0,1,2]
passed.append('captured runtime NumPy identity supplied explicitly')
try:prepare(npcomp,runtime_modules={'untrusted':np})
except ValueError:passed.append('arbitrary runtime dependency refused')
else:raise AssertionError('runtime allowlist')
# Exact static helper closure for the new acceptance/factory/phase graph.
import ast
names=set();pending=['importer_installation_cx1v001','valid_executor_factory_cx1v004','stateless_phase_cx1v002','cache_phase_forward_cx1v001','cache_certificate_adapter_cx1v003','classifier_spec_adapter_cx1v001','scheduler_adapter_cx1v001']
while pending:
 name=pending.pop()
 if name in names:continue
 names.add(name);source=b/(name+'.py')
 for node in ast.walk(ast.parse(source.read_bytes())):
  roots=[]
  if isinstance(node,ast.Import):roots=[a.name.split('.')[0] for a in node.names]
  elif isinstance(node,ast.ImportFrom) and node.module:roots=[node.module.split('.')[0]]
  pending.extend(n for n in roots if (b/(n+'.py')).exists() and n not in names)
graph={n+'.py':dict(path=str(b/(n+'.py')),sha256=hashlib.sha256((b/(n+'.py')).read_bytes()).hexdigest()) for n in names}
private=prepare(graph,runtime_modules={'numpy':np})
for name in names:private(name)
passed.append('complete selected integration helper graph loads privately: '+str(len(names))+' modules')
r=dict(status='PASS' ,blocking_count=0,tested=passed,untested=['Full actual helper graph loading','Separate root-authenticated entry','Dynamic private parent loaders and producer IO'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'pinned_helper_loader_cx1v002.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')
