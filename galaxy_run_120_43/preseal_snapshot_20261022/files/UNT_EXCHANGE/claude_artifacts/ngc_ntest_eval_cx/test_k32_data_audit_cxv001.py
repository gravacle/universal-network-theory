"""Actual partial replay custody plus deliberate corrupt successors; all mutations isolated."""
import copy,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ntests_compare_k32_cxv003 as C
R=Path(__file__).parent;mp=R/'out/K32_RECORDS_PARTIAL_V001_MANIFEST.json';m=json.loads(mp.read_bytes());original=json.loads(Path(m['N1']['path']).read_bytes());checks=[]
def put(p,obj):
 with p.open('x') as f:json.dump(obj,f,indent=1)
 return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
checks.append({'name':'valid_partial','passed':C.evaluate_manifest(mp)['outcome']=='N_INCOMPLETE'})
for name,mut in [('radius',lambda d:d['ring_radii_kpc'].__setitem__(15,99.)),('spread',lambda d:d['spread'].__setitem__(15,0.)),('producer_hash',lambda d:d['producer'].update(sha256='0'*64)),('producer_path',lambda d:d['producer'].update(path='/private/tmp/nonallowlisted.py'))]:
 d=copy.deepcopy(original);mut(d);mm=copy.deepcopy(m);mm['N1']=put(R/f'out/K32_AUDIT_{name}_RECORD_V001.json',d);p=R/f'out/K32_AUDIT_{name}_MANIFEST_V001.json';put(p,mm);v=C.evaluate_manifest(p);checks.append({'name':name,'passed':v['outcome']=='N_NO_RUN' and v['n_route_ab_gate']=='BLOCKED','outcome':v['outcome'],'defects':v.get('defects')})
put(R/'out/K32_DATA_AUDIT_TESTS_V001.json',{'label':'TESTED actual partial custody plus isolated corrupt successors; no full scientific N outcome','checks':checks})
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
