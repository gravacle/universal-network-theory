"""D004 actual metadata discovery on inert installed/absent scipy trees; no package execution."""
import runpy,sys,shutil,json,copy,hashlib
from pathlib import Path
b=Path(__file__).resolve().parent
g=runpy.run_path(str(b/'test_runtime_capture_pipeline_cx1v005.py'))
c=g['c'];site=g['site'];absent=c/'site_absent';absent.mkdir()
for name in ['numpy','numpy-1.dist-info']:shutil.copytree(site/name,absent/name)
ns=g['ns'];ns['sys'].path=[str(absent)];old=list(sys.path)
try:
 sys.path[:]=[str(absent)]+[p for p in old if 'site-packages' not in p and 'dist-packages' not in p]
 g['func'](str(c/'absent.json'),['numpy','math'])
 try:g['func'](str(c/'required_scipy_refused.json'),['numpy','scipy'])
 except ValueError as e:assert 'REQUIRED_IMPORT_ABSENT' in str(e)
 else:raise AssertionError('required scipy absent accepted')
finally:sys.path[:]=old
present=g['record'];record=json.loads((c/'absent.json').read_text());m=sys.modules['runtime_distribution_record_cx1v004']
assert record['scipy_presence']=={'state':'NOT_INSTALLED','find_spec_none':True,'search_path':[str(absent)]}
assert present['scipy_presence']['state']=='INSTALLED';m.compare(record,copy.deepcopy(record))
passed=['actual absent fixture records None search result and path','installed fixture records presence with byte capture','absent/absent equality passes','AST-required missing scipy refuses']
for label,a in [('presence mismatch',present),('contradictory absence',dict(record,scipy_presence=dict(record['scipy_presence'],find_spec_none=False))),('omitted evidence',{k:v for k,v in record.items() if k!='scipy_presence'})]:
 try:m.compare(record,a)
 except ValueError:passed.append(label+' refuses')
 else:raise AssertionError(label)
assert 'scipy' not in sys.modules and 'numpy' not in sys.modules
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Real launch capture','Root adoption','Registered runtime integration with revised record schema'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'runtime_distribution_discovery_cx1v005.py',b/'runtime_distribution_record_cx1v004.py',b/'runtime_distribution_capture_cx1v004.py',b/'registered_runtime_cx1v003.py',c/'absent.json',c/'TEST_REPORT.json']])
with (c/'SCIPY_PRESENCE_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'SCIPY_PRESENCE_REPORT.json')
