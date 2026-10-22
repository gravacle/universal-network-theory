"""Inert dependency preflight; no imported dependency code executes."""
from pathlib import Path
import tempfile,hashlib,json,copy
from accept_deps_preflight_cx1v001 import preflight,NAMES
from snapshot_cx1v001 import Snapshot,Refusal
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='accept_preflight_',dir=b/'inert_fixtures'));pins={}
for n in NAMES:
 p=c/(n+'.py')
 with p.open('x') as f:f.write("raise RuntimeError('INERT module MUST NOT execute')\n")
 pins[n]=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 if n.endswith('_adapter'):pins[n]['entry']='adapt'
s=Snapshot();got=preflight(s,pins,pins['lo_adapter']);assert len(got)==8 and all(v==1 for v in s.read_counts.values())
passed=['all eight raw dependencies verified and parsed without execution; one read each']
for name,mutate in [('missing lo_core',lambda p:p.update(lo_core=None)),('missing srb_adapter',lambda p:p.update(srb_adapter=None)),('foreign LO',lambda p:p['lo_adapter'].update(sha256='0'*64)),('extra dependency',lambda p:p.update(other={})),('bad adapter entry',lambda p:p['srb_adapter'].update(entry='bad.entry'))]:
 bad=copy.deepcopy(pins);mutate(bad);s=Snapshot()
 try:preflight(s,bad,pins['lo_adapter'])
 except Refusal:assert not s.read_counts
 else:raise AssertionError(name)
 passed.append(name+' refuses before any dependency read')
bad=copy.deepcopy(pins);bad['writer']['sha256']='0'*64
try:preflight(Snapshot(),bad,pins['lo_adapter'])
except Refusal:passed.append('wrong bytes refuse without executing any dependency')
else:raise AssertionError('bytes')
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Root-selected complete real dependency record','Transitive loader/import IO','Producer execution and scientific validity'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),b/'accept_deps_preflight_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2)
print(c/'TEST_REPORT.json')
