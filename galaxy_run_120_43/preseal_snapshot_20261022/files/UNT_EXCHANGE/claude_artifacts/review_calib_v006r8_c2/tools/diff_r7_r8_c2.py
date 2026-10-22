"""Item (3): everything that changed from v006r7 to v006r8, from bytes. Read-only; writes one JSON."""
import difflib
import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('_c2r8_common', HERE / 'common_c2r8.py')
C = importlib.util.module_from_spec(_s)
_s.loader.exec_module(C)

PAIRS = [('wrapper', C.R7 / 'calibration_orchestrator_cx2v006r7.py', C.R8 / 'calibration_orchestrator_cx2v006r8_v004.py'),
         ('core', C.R7 / 'calibration_core_cx2v006r7_v002.py', C.R8 / 'calibration_core_cx2v006r8_v003.py'),
         ('sensitivity', C.R7 / 'sensitivity_policy_cx2v006r7_v002.py', C.R8 / 'sensitivity_policy_cx2v006r8_v002.py')]
out = {'schema': 'C2_DIFF_R7_R8_V001', 'sources': {}, 'config': [], 'r7_manifest': {}}
for label, a, b in PAIRS:
    ta, tb = a.read_text().splitlines(), b.read_text().splitlines()
    d = list(difflib.unified_diff(ta, tb, str(a), str(b), n=0, lineterm=''))
    changed = [l for l in d if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
    out['sources'][label] = {'r7': C.pin(a), 'r8': C.pin(b), 'changed_lines': len(changed), 'diff': d}


def walk(x, y, p=''):
    if type(x) is not type(y):
        out['config'].append({'path': p, 'r7': x, 'r8': y}); return
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x:
                out['config'].append({'path': p + '.' + k, 'r7': '<absent>', 'r8': y[k]})
            elif k not in y:
                out['config'].append({'path': p + '.' + k, 'r7': x[k], 'r8': '<absent>'})
            else:
                walk(x[k], y[k], p + '.' + k)
    elif x != y:
        out['config'].append({'path': p, 'r7': x, 'r8': y})


c7 = json.loads((C.R7 / 'RUN_CONFIG_DDO154_CX2V006R7_P128_MS128.json').read_bytes())
c8 = json.loads((C.R8 / 'RUN_CONFIG_DDO154_CX2V006R8_P128_MS128.json').read_bytes())
walk(c7, c8)
# r7 artifacts unchanged: verify the r7 operations manifest and final r7 manifest from bytes.
for man in ('HASHES_OPERATIONS_CX2V006R7.txt', 'HASHES_SENSITIVITY_CX2V006R7.txt'):
    ok = bad = 0; bads = []
    for line in (C.R7 / man).read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        h, p = line.split(None, 1)
        p = p.strip()
        try:
            same = C.sha_file(p) == h
        except OSError as exc:
            same = False
        if same: ok += 1
        else: bad += 1; bads.append(p)
    out['r7_manifest'][man] = {'ok': ok, 'bad': bad, 'bad_paths': bads}
res = C.write_x(C.OUT / ('DIFF_R7_R8_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '.json'), out)
print(json.dumps({'out': res, 'changed_lines': {k: v['changed_lines'] for k, v in out['sources'].items()},
                  'config_paths': [c['path'] for c in out['config']], 'r7_manifest': out['r7_manifest']}, indent=1))
