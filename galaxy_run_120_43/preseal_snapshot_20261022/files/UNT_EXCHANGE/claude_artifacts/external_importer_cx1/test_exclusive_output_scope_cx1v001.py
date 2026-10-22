import tempfile,types,json
from pathlib import Path
from snapshot_cx1v001 import Snapshot,Refusal
from exclusive_output_scope_cx1v002 import ExclusiveOutputScope
b=Path(tempfile.mkdtemp(prefix='outputscope_',dir=Path(__file__).parent/'inert_fixtures')).resolve()
m=types.ModuleType('private_inert');m.__file__=str(b/'inert.py');m.Path=Path;m.json=json
inp=b/'input.json';inp.write_text('{"value":1}')
root=b/'outputs';snap=Snapshot();checks=[]
with ExclusiveOutputScope(snap,[m],[root]):
 m.Path(root).mkdir()
 assert m.Path(inp).read_text()==m.Path(inp).read_text();assert snap.read_counts[str(inp)]==1
 checks.append('input read once')
 target=root/'new.json'
 with m.open(target,'x') as f:
  f.write('{"new":true}')
  try:m.Path(target).read_bytes();raise AssertionError('read open output')
  except Refusal:pass
 checks.append('read before close refuses')
 assert m.json.loads(m.Path(target).read_bytes())=={'new':True};checks.append('closed output can be verified')
 for mode in ['w','a','r+']:
  try:m.open(target,mode);raise AssertionError(mode)
  except Refusal:pass
 checks.append('nonexclusive writes refuse')
 try:m.open(target,'x');raise AssertionError('overwrite')
 except FileExistsError:pass
 checks.append('existing output preserved')
 try:m.open(b/'outside','x');raise AssertionError('escape')
 except Refusal:pass
 checks.append('outside output refuses')
 try:m.Path(b/'outside_dir').mkdir();raise AssertionError('mkdir escape')
 except Refusal:pass
 checks.append('outside directory refuses')
assert m.Path is Path and 'open' not in m.__dict__;checks.append('module globals restored')
r={'status':'PASS','blocking_count':0,'scope':'Exclusive-output IO adapter utility only; not a security sandbox','tested':checks,'untested':['Real producer dependency IO audit','os/io/numpy direct access','Concurrent filesystem mutation','Full acceptance execution']}
p=b/'TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)
