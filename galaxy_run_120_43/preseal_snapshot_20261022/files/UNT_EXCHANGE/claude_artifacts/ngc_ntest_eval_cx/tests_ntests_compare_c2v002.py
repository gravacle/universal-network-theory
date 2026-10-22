"""0512 comparator branch and hostile-record tests. Synthetic only."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ntests_compare_c2v002 as C
from tests_ntests_compare_c2v001 import fixture
import ngc_ring_tail_ctx_c2v001 as L

def main():
    results=[]
    def test(name,mut,expected,failures=None):
        r=fixture();mut(r);got=C.compare(r)
        ok=got['outcome']==expected and (failures is None or got['failures']==failures)
        results.append(dict(name=name,expected=expected,got=got['outcome'],pass_=ok))
    test('all_pass_N4_report_only',lambda r:None,'N_PASS')
    test('N0_decided_failure',lambda r:r['N0'].update(bitwise_equal=False,mismatches=1),'N_FAIL_N0')
    test('NQ_decided_failure',lambda r:r['NQ'].update(max_delta_dL=C.THETA/19),'N_FAIL_NQ')
    test('N1_strict_boundary',lambda r:r['N1']['spread'].__setitem__(1,C.THETA),'N_FAIL_N1')
    test('N2_decided_failure',lambda r:r['N2'].update(max_delta_lnN0=C.THETA/3),'N_FAIL_N2')
    test('N3_decided_failure',lambda r:r['N3']['pairs']['8_vs_16'].update(max_delta_dL=C.THETA/3),'N_FAIL_N3')
    test('N3_dimensional_ruling',lambda r:r['N3']['pairs']['32_vs_16'].update(max_delta_S=C.THETA/8),'N_PASS')
    test('C1prime_pending',lambda r:r['N1'].pop('c1prime_spread'),'N_INCOMPLETE')
    test('C1prime_failure',lambda r:r['N1']['c1prime_spread'].__setitem__(99,C.THETA),'N_FAIL_N1')
    test('reference_failure',lambda r:r['N1']['reference_check_spread'].__setitem__(99,C.THETA),'N_FAIL_N1')
    for n in C.REQUIRED:test('missing_'+n,lambda r,n=n:r.pop(n),'N_INCOMPLETE')
    test('unknown_record',lambda r:r.update(EXTRA={}),'N_INCOMPLETE')
    test('unknown_schema',lambda r:r['N0'].update(schema='unknown'),'N_INCOMPLETE')
    test('unknown_gate',lambda r:r['LO_NGC'].update(verdict='MAYBE'),'N_INCOMPLETE')
    test('untested',lambda r:r['N0'].update(label='UNTESTED'),'N_INCOMPLETE')
    test('NaN',lambda r:r['NQ'].update(max_delta_dL=float('nan')),'N_NO_RUN')
    test('infinity',lambda r:r['N2'].update(max_delta_lnN0=float('inf')),'N_NO_RUN')
    test('boolean_statistic',lambda r:r['N2'].update(max_delta_lnN0=True),'N_NO_RUN')
    test('negative_statistic',lambda r:r['N2'].update(max_delta_lnN0=-1.),'N_NO_RUN')
    test('wrong_operator',lambda r:r['N1'].update(operator_sha256='0'*64),'N_NO_RUN')
    test('wrong_theta',lambda r:r['N1'].update(theta=1.),'N_NO_RUN')
    test('missing_shape_ring',lambda r:r['N1'].update(spread=[0.]*99),'N_NO_RUN')
    test('not_doubled',lambda r:r['NQ'].update(fine_quadrature=[.005,.007,8]),'N_NO_RUN')
    test('N0_coverage',lambda r:r['N0'].update(ring_count=100),'N_NO_RUN')
    test('N0_contradiction',lambda r:r['N0'].update(bitwise_equal=False),'N_NO_RUN')
    test('N3_reconstructed_packet',lambda r:r['N3']['pairs']['8_vs_16'].update(same_kept_packet=False),'N_NO_RUN')
    test('inclusive_NQ',lambda r:r['NQ'].update(max_delta_dL=C.THETA/20),'N_PASS')
    test('inclusive_N2',lambda r:r['N2'].update(max_delta_dL=C.THETA/4),'N_PASS')
    test('inclusive_N3',lambda r:r['N3']['pairs']['8_vs_16'].update(max_delta_S=C.THETA/4),'N_PASS')
    def multi(r):
        r['N0'].update(bitwise_equal=False,mismatches=1);r['NQ']['max_delta_dL']=1.
        r['N1']['spread'][1]=1.;r['N2']['max_delta_dL']=1.;r['N3']['pairs']['8_vs_16']['max_delta_dL']=1.
    test('every_failure_ordered',multi,'N_FAIL_NQ',['N_FAIL_NQ','N_FAIL_N0','N_FAIL_N1','N_FAIL_N2','N_FAIL_N3'])
    test('defect_precedes_missing',lambda r:(r.pop('N4'),r['N0'].update(mismatches=1)),'N_NO_RUN')
    def i1fail(r):
        r['I1T_NGC']['verdict']='FAIL';r['I1T_NGC']['builds'][0].update(verdict='FAIL',max_rel=1e-9)
    test('I1T_not_passed',i1fail,'N_INCOMPLETE')
    test('I1T_contradiction',lambda r:r['I1T_NGC'].update(verdict='FAIL'),'N_NO_RUN')
    def lofail(r):
        r['LO_NGC']['verdict']='FAIL';r['LO_NGC']['shells'][0]['readout_coupled_over_theta']=.006
        r['LO_NGC']['summed_max_over_theta']=.006
    test('LO_not_passed',lofail,'N_INCOMPLETE')
    test('LO_contradiction',lambda r:r['LO_NGC']['shells'][0].update(readout_coupled_over_theta=.006),'N_NO_RUN')
    test('bad_memory_override',lambda r:r['NQ'].update(memory_cap_override={'bytes':99}),'N_NO_RUN')
    rep=dict(label='TESTED_SYNTHETIC',passed=sum(x['pass_'] for x in results),total=len(results),results=results)
    L.write('out/COMPARE_SYNTHETIC_V002.json',rep);print(rep['passed'],rep['total'],flush=True)
    assert rep['passed']==rep['total']
if __name__=='__main__':main()
