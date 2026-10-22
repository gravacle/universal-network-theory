import tempfile,types,json
from pathlib import Path
import numpy as np
from snapshot_cx1v001 import Snapshot,Refusal
from exclusive_output_scope_cx1v003 import ExclusiveOutputScope
b=Path(tempfile.mkdtemp(prefix='arrayscope_',dir=Path(__file__).parent/'inert_fixtures')).resolve()
m=types.ModuleType('private_inert');m.__file__=str(b/'inert.py');m.Path=Path;m.np=np
src=b/'input.npz'
with src.open('xb') as f:np.savez(f,values=np.array([1.,2.,3.]))
root=b/'out';snap=Snapshot();checks=[]
with ExclusiveOutputScope(snap,[m],[root]):
 m.Path(root).mkdir()
 for i in range(3):
  with m.np.load(src,allow_pickle=False) as z:assert np.array_equal(z['values'],[1.,2.,3.])
 assert snap.read_counts[str(src)]==1;checks.append('three array loads share one byte read')
 with m.open(root/'new.npz','xb') as f:m.np.savez(f,values=np.array([4.,5.]))
 with m.np.load(root/'new.npz',allow_pickle=False) as z:assert np.array_equal(z['values'],[4.,5.])
 checks.append('exclusive array write and snapshot readback')
 for name,fn in [('path_write',lambda:m.np.savez(root/'forbidden.npz',x=np.array([1]))),('pickle',lambda:m.np.load(src,allow_pickle=True)),('mmap',lambda:m.np.load(src,mmap_mode='r'))]:
  try:fn();raise AssertionError(name)
  except Refusal:checks.append(name+' refused')
assert m.np is np and m.Path is Path;checks.append('shared numpy untouched and private globals restored')
r={'status':'PASS','blocking_count':0,'scope':'Private module NumPy IO shim only','tested':checks,'untested':['Function-local numpy imports','Dynamic producer dependency loading','Complete producer execution','Concurrent mutation races']}
p=b/'TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)
