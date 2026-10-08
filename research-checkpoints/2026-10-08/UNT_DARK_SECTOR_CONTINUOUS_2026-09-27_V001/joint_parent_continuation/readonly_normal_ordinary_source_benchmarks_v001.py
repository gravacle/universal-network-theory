"""Saved component/source scales only; no equation, operator or residual replay.
All ratios are descriptive. No physical-zero or observational acceptance gate.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os
BASE = Path(__file__).resolve().parent
AUTHOR_DRAFT = False
BOUND = {'normal_result': 'ca1056f8798864eb7ae86c61812379ad8be46c4586560bf832f308fb79242158', 'normal_receipt': '00a630bd20e5ac06ce3dcc63dd4187c6d82b8ea73989274b0d105157cfee25b2', 'checker_result': '1e3b72fee21d3ec31335a02ae814d74c982d2970c39c9fb0575f28589ba2442b'}
OUT = 'READONLY_NORMAL_ORDINARY_SOURCE_BENCHMARKS_V001_RESULT.json'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert not AUTHOR_DRAFT and all(v is not None for v in BOUND.values())
    assert not (BASE / OUT).exists()
    source_sha = sha(Path(__file__))
    inputs = {}
    def get(key, name):
        p = BASE / name
        assert sha(p) == BOUND[key]
        inputs[name] = BOUND[key]
        return json.loads(p.read_text())
    result = get('normal_result', 'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RESULT.json')
    receipt = get('normal_receipt', 'CROSS_U_PAIRED_CURRENT_NORMAL_CONSTRAINTS_V002_RECEIPT.json')
    check = get('checker_result', 'READONLY_PAIRED_NORMAL_CLOSURE_V002_RESULT.json')
    assert receipt['status'] == 'CLOSED' and receipt['result_sha256'] == BOUND['normal_result']
    assert check['status'] == 'SAVED_PAIRED_NORMAL_CLOSURE_PASS'
    assert check['parent_terminal']['result_sha256'] == BOUND['normal_result']
    assert check['parent_terminal']['receipt_sha256'] == BOUND['normal_receipt']
    assert result['case']['physical_adoption'] is False and result['case']['normal_constraint_solution'] is False
    assert check['qualification'] == result['qualification'] and all(v is False for v in result['qualification'].values())
    ref = result['case']['loads']; p = BASE / ref['file']; cp = BASE / ref['commit_file']
    assert sha(p) == ref['sha256'] and sha(cp) == ref['commit_sha256']
    assert receipt['output_sha256'][ref['file']] == ref['sha256']
    assert json.loads(cp.read_text()) == {k: v for k, v in ref.items() if k not in ('commit_file', 'commit_sha256')}
    inputs[ref['file']] = ref['sha256']; inputs[ref['commit_file']] = ref['commit_sha256']
    import numpy as np
    with np.load(p, allow_pickle=False) as f:
        assert json.loads(str(f['metadata_json'])) == ref['metadata']
        words = [f['normal_Hamiltonian_components_' + w].copy() for w in ('hi', 'lo')]
    assert all(a.shape == (4, 87, 45, 5) and a.dtype == np.float64 and np.all(np.isfinite(a)) for a in words)
    components = words[0] + words[1]; names = ('native_metric', 'mode_z0_compensation', 'absolute_phase', 'EH_ADM', 'ordinary_matter')
    rows = []
    assert [r['row'] for r in check['per_row_diagnostic_scales']] == ['lapse', 'shift_R', 'shift_Z', 'shift_phi']
    for i, saved in enumerate(check['per_row_diagnostic_scales']):
        terms = [dict(component=n, L2=float(np.linalg.norm(components[i, ..., j])), Linf=float(np.max(abs(components[i, ..., j])))) for j, n in enumerate(names)]
        source = terms[4]
        rows.append(dict(row=saved['row'], components=terms, residual_L2_to_ordinary_source=saved['absolute_L2']/source['L2'] if source['L2'] else None, residual_Linf_to_ordinary_source=saved['absolute_Linf']/source['Linf'] if source['Linf'] else None))
    for name, digest in inputs.items():
        assert sha(BASE / name) == digest
    assert sha(Path(__file__)) == source_sha
    out = dict(status='SAVED_NORMAL_SOURCE_BENCHMARKS_MEASURED', pid=os.getpid(), closed=datetime.now(timezone.utc).isoformat(), source_sha256=source_sha, input_sha256=inputs, rows=rows, physical_zero_gate=False, background_subtraction=False, velocity_error_bound=False, qualification=result['qualification'], interpretation='Same saved weak nodal test space; ordinary source confined to sheet. Zero meridional source has no relative denominator. Source ratios do not bound orbital errors.')
    with (BASE / OUT).open('x') as f:
        json.dump(out, f, indent=2, sort_keys=True, allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    (BASE / OUT).chmod(0o444)
    print(out['status'], out['pid'], sha(BASE / OUT))
if __name__ == '__main__':
    main()
