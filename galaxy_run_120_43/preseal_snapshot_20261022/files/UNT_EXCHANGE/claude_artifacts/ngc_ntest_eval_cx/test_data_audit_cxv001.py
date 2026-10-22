"""Run after real N0/NQ record assembly. Test raw-data contradiction and reader refusal behavior."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ngc_ring_tail_ctx_c2v001 as L
import ntests_compare_c2v004 as A
import ntests_compare_c2v005 as C

def main():
    manifest=Path(sys.argv[1]);records=A.P.read_manifest(manifest);tests=[]
    def check(name,fn,exception=None):
        try:
            value=fn();ok=exception is None and value is not False
        except Exception as e:ok=exception is not None and isinstance(e,exception)
        tests.append(dict(name=name,passed=ok))
    check('real_N0_NQ_raw_evidence',lambda:A.audit(records))
    def corrupt_metric():
        r=copy.deepcopy(records);r['NQ']['max_delta_dL']+=1e-5;return A.audit(r)
    check('refuse_metric_contradiction',corrupt_metric,ValueError)
    def corrupt_count():
        r=copy.deepcopy(records);r['N0']['mismatches']+=1;return A.audit(r)
    check('refuse_bit_count_contradiction',corrupt_count,ValueError)
    def missing_evidence():
        r=copy.deepcopy(records);r['NQ'].pop('input_pins');return A.audit(r)
    check('missing_evidence_pending',missing_evidence,FileNotFoundError)
    def outside_path():
        r=copy.deepcopy(records);r['NQ']['input_pins']['CUBE16']['path']='/DO_NOT_OPEN_NGC_TARGET';return A.audit(r)
    check('raw_path_refused_before_open',outside_path,ValueError)
    result=C.evaluate_manifest(manifest)
    check('missing_N1_N2_N3_N4_incomplete',lambda:result['outcome']=='N_INCOMPLETE' and not result['tests_read'])
    check('module_bytes_unchanged',lambda:L.sha(L.MOD/'owned_uv_tail_lapse_v001.py')=='c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22')
    rec=dict(label='TESTED',passed=sum(t['passed'] for t in tests),total=len(tests),tests=tests)
    L.write('out/DATA_AUDIT_TESTS_V001.json',rec);print(rec['passed'],rec['total'],flush=True)
    assert rec['passed']==rec['total']
if __name__=='__main__':main()
