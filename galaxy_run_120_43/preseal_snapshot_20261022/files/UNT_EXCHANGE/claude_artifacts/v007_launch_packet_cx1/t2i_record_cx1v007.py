"""Wrap the existing pinned T2I replica replay; require all three components.
RUN LABEL KEPT_GRID_JSON RAW_OUTPUT GATE_OUTPUT. Exclusive outputs, no launches.
Fixture labels remain real labels; no fixture is represented as a C5H scientific test.
"""
import sys as _guard_sys
from pathlib import Path as _GuardPath
_guard_sys.path.insert(0, str(_GuardPath(__file__).parent))
import producer_guard_cx1v006 as _root_guard
_root_guard.admission(__file__)
import hashlib, json, runpy, sys
from pathlib import Path
ROOT = Path(__file__).parent
PRODUCER = ROOT / 't2i_replica_admitted_cx1v003.py'

@_root_guard.guarded
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}

@_root_guard.guarded
def convert(raw, run, label):
    r = json.loads(Path(raw).read_bytes())
    items = r['items_max_rel']
    groups = {'route_a_updated': [v for k, v in items.items() if k.startswith('route_a.updated_')], 'offset_new_body_fourier_J': [v for k, v in items.items() if k == 'offset.new_body'], 'feedback_gas_source_feedback': [v for k, v in items.items() if k.startswith('feedback.')]}
    missing = [k for k, v in groups.items() if not v]
    meta = r['meta'].get('route_a')
    if not isinstance(meta, dict) or not meta.get('roster_digest_equals_identity') or (not meta.get('waves_equal_ext_tensor')):
        missing.append('route_a_identity')
    rec = {'schema': 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002', 'gate': 'T2I', 'producer': pin(Path(__file__)), 'case': label, 'region': 'G5\\G4' if label == 'C5H' else 'fixture ext grid minus supplied kept grid', 'c5h_result_sha256': pin(Path(run) / 'result.json')['sha256'] if label == 'C5H' else None, 'actual_result': pin(Path(run) / 'result.json'), 'raw_replay': pin(raw), 'components': {k: max(v) for k, v in groups.items() if v}, 'max_rel': max(items.values()) if items else None, 'missing_components': missing, 'label': 'TESTED saved transform replay; fixture only' if label != 'C5H' else 'TESTED saved transform replay'}
    rec['verdict'] = 'PASS' if not missing and r['verdict'] == 'PASS' else 'FAIL'
    return rec
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))
    import producer_guard_cx1v006 as guard
    guard.authorize(sys.argv, 'run')
    run, label, kept, raw, out = sys.argv[1:]
    sys.argv = [str(PRODUCER), run, kept, raw]
    runpy.run_path(str(PRODUCER), run_name='__main__')
    rec = convert(raw, run, label)
    with open(out, 'x') as f:
        json.dump(rec, f, indent=1)
    print(json.dumps({'label': label, 'verdict': rec['verdict'], 'missing': rec['missing_components']}))
