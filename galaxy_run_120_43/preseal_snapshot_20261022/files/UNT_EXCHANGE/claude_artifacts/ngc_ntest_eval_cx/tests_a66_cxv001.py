"""0550 route consequence tests; all records synthetic."""
import ast,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import ntests_compare_k32_cxv003 as C
import ngc_ring_tail_ctx_c2v001 as L
from tests_ntests_compare_c2v001 import fixture as oldfixture
producer={'path':str(Path(__file__).resolve()),'sha256':L.sha(__file__),'version':Path(__file__).stem}
tree=ast.parse((L.HERE/'tests_k32_compare_cxv001.py').read_text());exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='fixture'],type_ignores=[]),'synthetic_fixture','exec'))
checks=[]
def test(name,mut,outcome,gate):
 r=fixture();r['N1']['ring_radii_kpc']=list(range(100));mut(r);v=C.compare(r);checks.append({'name':name,'outcome':v['outcome'],'gate':v['n_route_ab_gate'],'reasons':v['n_route_ab_reason_codes'],'passed':v['outcome']==outcome and v['n_route_ab_gate']==gate})
 if name=='shape_failure_keeps_name':assert v['failing_TRUNCATION_SHAPE_rings'][0]['radial_support']=={'kind':'sampled_ring','R_kpc':15}
test('all_pass',lambda r:None,'N_PASS','OPEN')
test('shape_failure_keeps_name',lambda r:r['N1']['spread'].__setitem__(15,C.Core.THETA),'N_FAIL_N1','OPEN')
test('notgrid_failure_blocks',lambda r:r['N1']['c1prime_spread'].__setitem__(12,C.Core.THETA),'N_FAIL_N1','BLOCKED')
test('gf_failure_blocks',lambda r:r['N1']['spread'].__setitem__(0,C.Core.THETA),'N_FAIL_N1','BLOCKED')
test('reference_failure_blocks',lambda r:r['N1']['reference_check_spread'].__setitem__(15,C.Core.THETA),'N_FAIL_N1','BLOCKED')
test('shape_and_N2_blocks',lambda r:(r['N1']['spread'].__setitem__(15,C.Core.THETA),r['N2'].update(max_delta_dL=1.)),'N_FAIL_N1','BLOCKED')
test('N3prime_blocks',lambda r:r['N3']['pairs']['64_vs_32'].update(max_delta_dL=1.),'N_FAIL_N3','BLOCKED')
test('NQ_blocks',lambda r:r['NQ'].update(max_delta_dL=1.),'N_FAIL_NQ','BLOCKED')
test('N0_blocks',lambda r:r['N0'].update(bitwise_equal=False,mismatches=1),'N_FAIL_N0','BLOCKED')
test('incomplete_blocks',lambda r:r.pop('EPS_NGC'),'N_INCOMPLETE','BLOCKED')
test('missing_support_blocks',lambda r:r['N1'].pop('ring_radii_kpc'),'N_NO_RUN','BLOCKED')
test('N4_report_only',lambda r:r['N4'].update(e4_z95=100.),'N_PASS','OPEN')
L.write('out/A66_GATE_TESTS_V001.json',{'label':'TESTED synthetic only','producer':producer,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks)})
print(sum(x['passed'] for x in checks),len(checks));assert all(x['passed'] for x in checks)
