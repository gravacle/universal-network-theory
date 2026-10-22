"""Synthetic production32/certificate91 boundaries; no scientific result."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ntests_compare_k32_cxv001 as C
import ngc_ring_tail_ctx_c2v001 as L
from tests_ntests_compare_c2v001 import fixture as oldfixture
producer={'path':str(Path(__file__).resolve()),'sha256':L.sha(__file__),'version':Path(__file__).stem}
def fixture():
 r=oldfixture()
 for name,obj in r.items():
  obj['producer']=producer
  if name.startswith('N'):obj.update(production_K_big=32,replay_producers={'synthetic':producer})
 pp=r['N3']['pairs'];r['N3']['pairs']={'16_vs_32':pp['8_vs_16'],'64_vs_32':pp['32_vs_16']}
 r['LO_NGC']['shells'].append({'range_inverse_kpc':[16.,91.],'readout_coupled_over_theta':0.})
 r['GQ_NGC']={'gate':'GQ_NGC','verdict':'PASS','producer':producer,'rosters':[{'roster':'NGC_T120L','M_s':96,'M_s_doubled':192,'nodes':4096,'k_range_inverse_kpc':[2.,91.],'max_abs_diff_over_P0':0.}]}
 r['EPS_NGC']={'verdict':'CERTIFIED','coverage_inverse_kpc':{'NGC':[2,91]},'shells':[{'range_inverse_kpc':[2,91]}],'producer':producer}
 return r
checks=[]
def test(name,mut,want):
 r=fixture();mut(r);out=C.compare(r);checks.append({'name':name,'want':want,'got':out['outcome'],'passed':out['outcome']==want,'pending':out.get('pending',[]),'defects':out.get('defects',[])})
test('K32_complete_synthetic',lambda r:None,'N_PASS')
test('K16_production_refused',lambda r:r['N1'].update(production_K_big=16),'N_NO_RUN')
test('old_N3_keys_refused',lambda r:r['N3'].update(pairs={'8_vs_16':r['N3']['pairs']['16_vs_32'],'32_vs_16':r['N3']['pairs']['64_vs_32']}),'N_NO_RUN')
test('N3prime_64_strict_limit',lambda r:r['N3']['pairs']['64_vs_32'].update(max_delta_dL=C.Core.THETA/3),'N_FAIL_N3')
test('N3prime_inclusive',lambda r:r['N3']['pairs']['16_vs_32'].update(max_delta_dL=C.Core.THETA/4),'N_PASS')
test('EPS_missing',lambda r:r.pop('EPS_NGC'),'N_INCOMPLETE')
test('EPS_old_46',lambda r:r['EPS_NGC'].update(coverage_inverse_kpc={'NGC':[2,46]}),'N_INCOMPLETE')
test('EPS_shell_gap',lambda r:r['EPS_NGC'].update(shells=[{'range_inverse_kpc':[2,46]},{'range_inverse_kpc':[47,91]}]),'N_INCOMPLETE')
test('EPS_not_certified',lambda r:r['EPS_NGC'].update(verdict='FAIL'),'N_INCOMPLETE')
test('LO_old_16',lambda r:r['LO_NGC']['shells'].pop(),'N_INCOMPLETE')
test('GQ_old_46',lambda r:r['GQ_NGC']['rosters'][0].update(k_range_inverse_kpc=[2,46]),'N_INCOMPLETE')
test('GQ_wrong_Ms',lambda r:r['GQ_NGC']['rosters'][0].update(M_s=128),'N_NO_RUN')
test('pending_coverage_precedes_N1_failure',lambda r:(r['EPS_NGC'].update(coverage_inverse_kpc={'NGC':[2,46]}),r['N1']['spread'].__setitem__(15,1.)),'N_INCOMPLETE')
test('malformed_shell_precedes_missing',lambda r:(r.pop('N2'),r['EPS_NGC'].update(shells=[{'range_inverse_kpc':[91,2]}])),'N_NO_RUN')
L.write('out/K32_COMPARE_TESTS_V001.json',{'label':'TESTED synthetic only','producer':producer,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)})
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks),checks
