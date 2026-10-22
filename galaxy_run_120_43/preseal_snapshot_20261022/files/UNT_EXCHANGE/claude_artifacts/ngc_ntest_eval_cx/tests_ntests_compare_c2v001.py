"""Synthetic outcome/invalid-input tests. No scientific outcome inference."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ntests_compare_c2v001 as C
import ngc_ring_tail_ctx_c2v001 as L

def fixture():
    r={n:dict(schema='NGC_NTEST_RECORD_C2V001',test=n,label='TESTED',operator_sha256=C.OP_SHA,theta=C.THETA) for n in C.REQUIRED if n.startswith('N')}
    r['N0'].update(bitwise_equal=True,mismatches=0,ring_count=156,azimuths=32,heights=7)
    r['NQ'].update(ring_count=156,azimuths=32,heights=7,base_quadrature=[.005,.007,8],fine_quadrature=[.0025,.0035,12],max_delta_lnN0=0.,max_delta_dL=0.)
    r['N1'].update(spread=[0.]*100,c1prime_spread=[0.]*100,reference_check_spread=[0.]*100,c1prime_reference='G160L',reference_checked_against='G120L')
    r['N2'].update(ring_count=156,azimuths=32,heights=7,max_delta_lnN0=0.,max_delta_dL=0.)
    pair=dict(same_kept_packet=True,arithmetic='1.+(n_kept+t)',ring_count=156,azimuths=32,max_delta_S=0.,max_delta_dL=0.)
    r['N3']['pairs']={n:copy.deepcopy(pair) for n in ('8_vs_16','32_vs_16')}
    r['N4'].update(ring_count=156,azimuths=32,e4_z95=999.) # no threshold allowed
    for n,f in [('LO_NGC','LO_NGC_CERT_V002.json'),('I1T_NGC','I1T_NGC_T120L_V001.json')]:r[n]=json.loads(L.verify(L.CERT/f).read_text())
    return r

def main():
    results=[]
    def test(name,mut,expected):
        r=fixture();mut(r);got=C.compare(r)['outcome'];results.append(dict(name=name,expected=expected,got=got,pass_=got==expected))
    test('all_pass_N4_report_only',lambda r:None,'PASS_N_TESTS')
    test('N0_bit_failure',lambda r:r['N0'].update(bitwise_equal=False,mismatches=1),'IMPLEMENTATION_DEFECT')
    test('I1T_failure',lambda r:r['I1T_NGC'].update(verdict='FAIL'),'IMPLEMENTATION_DEFECT')
    test('LO_readout_failure',lambda r:r['LO_NGC']['shells'][0].update(readout_coupled_over_theta=.006),'NON_LAPSE_TAIL_MATERIAL')
    test('NQ_failure',lambda r:r['NQ'].update(max_delta_dL=C.THETA/19),'NUMERICS_UNCERTIFIED')
    test('N1_strict_equality',lambda r:r['N1']['spread'].__setitem__(1,C.THETA),'N1_FAIL')
    test('C1prime_failure',lambda r:r['N1']['c1prime_spread'].__setitem__(99,C.THETA),'N1_FAIL')
    test('reference_check_failure',lambda r:r['N1']['reference_check_spread'].__setitem__(99,C.THETA),'N1_FAIL')
    test('N2_failure',lambda r:r['N2'].update(max_delta_lnN0=C.THETA/3),'SHAPE_DISAGREEMENT')
    test('N3_failure',lambda r:r['N3']['pairs']['8_vs_16'].update(max_delta_dL=C.THETA/3),'KBIG_NOT_CONVERGED')
    test('N3_literal_normalized_stricter',lambda r:r['N3']['pairs']['32_vs_16'].update(max_delta_S=C.THETA/8),'KBIG_NOT_CONVERGED')
    for n in C.REQUIRED:
        test('missing_'+n,lambda r,n=n:r.pop(n),'INCOMPLETE')
    test('unknown_record',lambda r:r.update(EXTRA={}),'INCOMPLETE')
    test('NaN',lambda r:r['NQ'].update(max_delta_dL=float('nan')),'INCOMPLETE')
    test('infinity',lambda r:r['N2'].update(max_delta_lnN0=float('inf')),'INCOMPLETE')
    test('boolean_numeric',lambda r:r['N2'].update(max_delta_lnN0=True),'INCOMPLETE')
    test('negative_metric',lambda r:r['N2'].update(max_delta_lnN0=-1.),'INCOMPLETE')
    test('unknown_gate_verdict',lambda r:r['LO_NGC'].update(verdict='MAYBE'),'INCOMPLETE')
    test('wrong_operator',lambda r:r['N1'].update(operator_sha256='0'*64),'INCOMPLETE')
    test('wrong_theta',lambda r:r['N1'].update(theta=1.),'INCOMPLETE')
    test('missing_shape_ring',lambda r:r['N1'].update(spread=[0.]*99),'INCOMPLETE')
    test('NQ_not_doubled',lambda r:r['NQ'].update(fine_quadrature=[.005,.007,8]),'INCOMPLETE')
    test('not_tested',lambda r:r['N4'].update(label='UNTESTED'),'INCOMPLETE')
    test('N0_incomplete_coverage',lambda r:r['N0'].update(ring_count=100),'INCOMPLETE')
    test('N3_reconstructed_kept',lambda r:r['N3']['pairs']['8_vs_16'].update(same_kept_packet=False),'INCOMPLETE')
    test('inclusive_NQ_boundary',lambda r:r['NQ'].update(max_delta_dL=C.THETA/20),'PASS_N_TESTS')
    test('inclusive_N2_boundary',lambda r:r['N2'].update(max_delta_dL=C.THETA/4),'PASS_N_TESTS')
    test('N1_fail_before_N2',lambda r:(r['N1']['spread'].__setitem__(1,C.THETA),r['N2'].update(max_delta_dL=1.)),'N1_FAIL')
    rep=dict(label='TESTED_SYNTHETIC',passed=sum(x['pass_'] for x in results),total=len(results),results=results)
    L.write('out/COMPARE_SYNTHETIC_V001.json',rep);print(rep['passed'],rep['total'])
    assert rep['passed']==rep['total']
if __name__=='__main__':main()
