"""Report existing D_m4 diagnostics; missing data remains unavailable, never zero.
RUN LABEL OUTPUT. No source solve, targets or run launches.
"""
import sys as _guard_sys
from pathlib import Path as _GuardPath
_guard_sys.path.insert(0, str(_GuardPath(__file__).parent))
import producer_guard_cx1v008 as _root_guard
_root_guard.admission(__file__)
import hashlib, json, sys
from pathlib import Path

@_root_guard.guarded
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))
    import producer_guard_cx1v008 as guard
    guard.authorize(sys.argv, 'run')
    run, label, out = sys.argv[1:]
    p = Path(run) / 'result.json'
    r = json.loads(p.read_bytes())
    h = (r.get('residual_diagnostics') or {}).get('azimuthal_harmonics') or {}
    rs = h.get('radial_nodes_m')
    per = h.get('per_radius_max')
    ok = isinstance(rs, list) and isinstance(per, list) and (len(rs) == len(per)) and (len(rs) > 0) and all(('m4' in x for x in per))
    rec = {'schema': 'UNT_V007_DM4_REPORT_CX1V001', 'case': label, 'producer': pin(Path(__file__)), 'result': pin(p), 'label': 'TESTED extraction', 'status': 'REPORTED' if ok else 'UNAVAILABLE', 'quantity': h.get('quantity'), 'radial_nodes_m': rs if ok else None, 'D_m4': [x['m4'] for x in per] if ok else None}
    _root_guard.check_run_path(out, allow_registered=False)
    with open(out, 'x') as f:
        json.dump(_root_guard.stamp(rec, __file__), f, indent=1)
    print(label, rec['status'])
