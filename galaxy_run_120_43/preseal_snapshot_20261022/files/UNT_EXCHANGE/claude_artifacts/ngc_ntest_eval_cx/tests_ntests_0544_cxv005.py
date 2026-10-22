"""0544 branch checks; carries old43 cases with explicit synthetic provenance and GQ admission."""
import copy,json,sys,types
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ngc_ring_tail_ctx_c2v001 as L
import ntests_compare_c2v009 as C
import ntests_compare_c2v002 as Core
import tests_ntests_compare_c2v002 as Old
oldfixture=Old.fixture
producer={'path':str(Path(__file__).resolve()),'sha256':L.sha(__file__),'version':Path(__file__).stem}
gq=json.loads((L.CERT/'GQ_CERT_V003_KB128.json').read_bytes())
def fixture():
 r=oldfixture()
 for k,v in r.items():
  v['producer']=producer
  if k.startswith('N'):v['replay_producers']={'synthetic':producer}
 r['GQ_NGC']=copy.deepcopy(gq);return r
Old.fixture=fixture;Old.C=types.SimpleNamespace(compare=C.compare,THETA=Core.THETA,REQUIRED=Core.REQUIRED)
oldwrite=L.write
L.write=lambda name,obj:oldwrite(name.replace('COMPARE_SYNTHETIC_V002','COMPARE_SYNTHETIC_0544_V005'),obj)
Old.main()
checks=[]
def check(name,mut,want):
 r=fixture();mut(r);out=C.compare(r);checks.append({'name':name,'expected':want,'actual':out['outcome'],'passed':out['outcome']==want})
check('GQ_missing',lambda r:r.pop('GQ_NGC'),'N_INCOMPLETE')
check('GQ_unknown_verdict',lambda r:r['GQ_NGC'].update(verdict='UNKNOWN'),'N_INCOMPLETE')
check('GQ_FAIL',lambda r:r['GQ_NGC'].update(verdict='FAIL'),'N_INCOMPLETE')
check('GQ_no_NGC_roster',lambda r:r['GQ_NGC'].update(rosters=[]),'N_INCOMPLETE')
def mutate_rows(r,**kw):
 for x in r['GQ_NGC']['rosters']:
  if x['roster']=='NGC_T120L':x.update(**kw)
check('GQ_short_range',lambda r:mutate_rows(r,k_range_inverse_kpc=[2.,31.]),'N_INCOMPLETE')
check('GQ_gap',lambda r:mutate_rows(r,k_range_inverse_kpc=[3.,46.]),'N_INCOMPLETE')
check('GQ_wrong_Ms',lambda r:mutate_rows(r,M_s=64),'N_NO_RUN')
check('GQ_wrong_doubling',lambda r:mutate_rows(r,M_s_doubled=96),'N_NO_RUN')
check('GQ_node_coverage',lambda r:mutate_rows(r,nodes=4095),'N_NO_RUN')
check('GQ_false_PASS',lambda r:mutate_rows(r,max_abs_diff_over_P0=1e-9),'N_NO_RUN')
check('GQ_nan',lambda r:mutate_rows(r,max_abs_diff_over_P0=float('nan')),'N_NO_RUN')
check("GQ_float_nodes_refused",lambda r:mutate_rows(r,nodes=4096.0),"N_NO_RUN")
check("GQ_malformed_roster_refused",lambda r:r["GQ_NGC"].update(rosters=[None]),"N_NO_RUN")
checks.append({"name":"nonobject_manifest","passed":C.compare(None)["outcome"]=="N_NO_RUN"})
check('producer_missing',lambda r:r['NQ'].pop('producer'),'N_INCOMPLETE')
check('producer_bad_pin',lambda r:r['N0'].update(producer={'path':'x','sha256':'bad'}),'N_NO_RUN')
check('replay_versions_missing',lambda r:r['NQ'].pop('replay_producers'),'N_INCOMPLETE')
check('GQ_defect_precedes_N_missing',lambda r:(r.pop('N4'),mutate_rows(r,M_s=64)),'N_NO_RUN')
checks.append({'name':'resolution_wording','passed':C.compare(fixture())['NQ_resolution_note']=='below one N step (3.3e-8 theta)'})
oldwrite('out/COMPARE_0544_TESTS_V005.json',{'label':'TESTED synthetic branch tests; no scientific N reading','producer':producer,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)})
print('0544',sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
