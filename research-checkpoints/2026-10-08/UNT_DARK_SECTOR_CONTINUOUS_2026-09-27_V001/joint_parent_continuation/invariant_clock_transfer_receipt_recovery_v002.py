"""Recover complete scientific fields preceding V001 JSON-print failure.

All trajectories/identities/reference data were serialized before a NumPy
bool in controls stopped the writer. Preserve the partial original. Parse
only that complete prefix; independently recompute EVERY original control
from the stored numbers. Check row and snapshot counts, stages, source and
dependency hashes. No trajectory is rerun and no missing result is invented.
The original total runtime was not serialized and remains unavailable.
"""
from pathlib import Path
import hashlib
import json
import numpy as np

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'INVARIANT_CLOCK_TRANSFER_V001_RESULT.json'
OUT=BASE/'INVARIANT_CLOCK_TRANSFER_V002_RESULT.json'

def main():
    raw=SOURCE.read_text();prefix,tail=raw.rsplit('\n  "controls":',1)
    if tail.strip()!='{\n    "time_refinement": true,\n    "reference_refinement": true,\n    "material_polynomial": true,\n    "cross_identity":':
        raise ValueError('unexpected failure boundary; no recovery attempted')
    r=json.loads(prefix.rstrip().removesuffix(',')+'\n}')
    if r['self_sha256']!=hashlib.sha256((BASE/'invariant_clock_transfer_v001.py').read_bytes()).hexdigest():
        raise ValueError('original source changed')
    for name,sha in r['dependencies_sha256'].items():
        if sha!=hashlib.sha256((BASE/name).read_bytes()).hexdigest():raise ValueError(name)
    assert [x['Q0_over_H0'] for x in r['rows']]==[1.,10.,100.]
    for row in r['rows']:
        assert [h['steps'] for h in row['histories']]==[2048,4096,8192]
        for h in row['histories']:
            assert len(h['snapshots'])==65 and abs(h['snapshots'][-1]['a']-1)<1e-14
    assert len(r['identities'])==9 and len(r['pressureless_reference'])==2
    hh=np.array([x['H'] for x in r['identities']]).reshape(3,3)
    checks=dict(time_refinement=all(x['fine_error']<=1e-4 for x in r['rows']),
        reference_refinement=r['reference_error']<=1e-4,
        material_polynomial=max(x['material_polynomial_absolute_error'] for x in r['identities'])<=1e-8,
        cross_identity=max(x['cross_identity_relative_error'] for x in r['identities'])<=1e-12,
        same_background=float(np.max(abs(hh/hh[0]-1)))<=1e-12)
    r.update(controls=checks,all_controls_passed=all(checks.values()),
        recovery_protocol=__doc__,recovery_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        partial_receipt_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        original_elapsed_seconds=None)
    with OUT.open('x') as f:json.dump(r,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(controls=checks,comparisons=[{k:v for k,v in x.items() if k!='histories'} for x in r['rows']],
                          identities=r['identities']),indent=2))
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':main()
