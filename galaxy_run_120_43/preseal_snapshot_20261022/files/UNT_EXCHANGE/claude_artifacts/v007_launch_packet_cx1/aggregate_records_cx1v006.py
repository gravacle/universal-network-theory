"""Aggregate byte-pinned EA or SR_K component records after their replays. MODE MANIFEST OUTPUT.
Manifest: {label: {path,sha256}}. Never substitutes absent states or rows.
"""
import sys as _guard_sys
from pathlib import Path as _GuardPath
_guard_sys.path.insert(0, str(_GuardPath(__file__).parent))
import producer_guard_cx1v006 as _root_guard
_root_guard.admission(__file__)
import hashlib, importlib.util, json, sys
from pathlib import Path
R = Path(__file__).parent
P = R.parent / 'v007_compare_c2/r5/kmax_tail_compare_c2v007_r5.py'

@_root_guard.guarded
def pin(p):
    return {'path': str(p), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}

@_root_guard.guarded
def main():
    mode, mp, out = sys.argv[1:]
    refs = json.loads(Path(mp).read_bytes())
    records = {}
    for label, ref in refs.items():
        if pin(ref['path'])['sha256'] != ref['sha256']:
            raise ValueError('INPUT_PIN_MISMATCH')
        records[label] = json.loads(Path(ref['path']).read_bytes())
    rec = {'schema': 'UNT_KMAX_TAIL_V007_GATE_RECORD_C2V002', 'gate': mode, 'verdict': 'REPLAYED', 'producer': pin(Path(__file__)), 'input_pins': refs}
    import producer_guard_cx1v006 as guard
    ref = guard.SEALED_COMPARE_REF
    if ref is None:
        raise ValueError('SEALED_COMPARE_REQUIRED')
    sealed_path = Path(ref['path'])
    if pin(sealed_path)['sha256'] != ref['sha256']:
        raise ValueError('SEALED_COMPARE_CHANGED')
    rec['compare'] = ref
    s = importlib.util.spec_from_file_location('record_compare', sealed_path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    if mode == 'SR_K':
        if set(records) != {'C2R3', 'C3R3', 'C4R3'}:
            raise ValueError('ALL_THREE_SR_STATES_REQUIRED')
        states = {}
        delta = {}
        for lab, obj in records.items():
            if obj['case'] != lab or obj['state_result']['sha256'] != m.PIN_R3[lab][1] or obj['zero_correction_bitwise'] is not True or (obj['i1t']['verdict'] != 'PASS'):
                raise ValueError('SR_STATE_CUSTODY')
            states[lab] = obj['state_result']['sha256']
            delta[str(int(obj['K']))] = obj['Delta_km_s']
        rec.update(states=states, Delta_km_s=delta)
    elif mode == 'EA':
        if 'C5H' not in records:
            raise ValueError('C5H_EA_REQUIRED')
        per = {}
        for lab, obj in records.items():
            if set(obj['per_case']) != {lab}:
                raise ValueError('EA_LABEL_MISMATCH')
            per[lab] = obj['per_case'][lab]
        rec['per_case'] = per
    else:
        raise ValueError('MODE_SR_K_OR_EA_ONLY')
    with open(out, 'x') as f:
        json.dump(rec, f, indent=1)
if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).parent))
    import producer_guard_cx1v006 as guard
    guard.authorize(sys.argv, 'records')
    main()
