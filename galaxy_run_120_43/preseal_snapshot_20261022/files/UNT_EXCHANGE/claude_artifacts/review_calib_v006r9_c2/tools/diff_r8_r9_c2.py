"""Item (2): everything that changed from v006r8 to v006r9, from bytes. Read-only; writes one JSON."""
import difflib
import importlib.util
import json
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location('_c2r9_common', HERE / 'common_c2r9.py')
C = importlib.util.module_from_spec(_s)
_s.loader.exec_module(C)

PAIRS = [('wrapper', C.R8 / 'calibration_orchestrator_cx2v006r8_v004.py', C.R9 / 'calibration_orchestrator_cx2v006r9.py'),
         ('core', C.R8 / 'calibration_core_cx2v006r8_v003.py', C.R9 / 'calibration_core_cx2v006r9.py'),
         ('static_dry_check', C.R8 / 'check_static_dry_cx2v006r8.py', C.R9 / 'check_static_dry_cx2v006r9.py')]
out = {'schema': 'C2_DIFF_R8_R9_V001', 'sources': {}, 'config': [], 'manifests': {}, 'unlisted_r9_files': []}
for label, a, b in PAIRS:
    ta, tb = a.read_text().splitlines(), b.read_text().splitlines()
    d = list(difflib.unified_diff(ta, tb, str(a), str(b), n=0, lineterm=''))
    changed = [l for l in d if (l.startswith('+') or l.startswith('-')) and not l.startswith(('+++', '---'))]
    out['sources'][label] = {'r8': C.pin(a), 'r9': C.pin(b), 'changed_lines': len(changed), 'diff': d}


def walk(x, y, p=''):
    if type(x) is not type(y):
        out['config'].append({'path': p, 'r8': x, 'r9': y}); return
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x:
                out['config'].append({'path': p + '.' + k, 'r8': '<absent>', 'r9': y[k]})
            elif k not in y:
                out['config'].append({'path': p + '.' + k, 'r8': x[k], 'r9': '<absent>'})
            else:
                walk(x[k], y[k], p + '.' + k)
    elif isinstance(x, list):
        if len(x) != len(y):
            out['config'].append({'path': p, 'r8': x, 'r9': y})
        else:
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, '%s[%d]' % (p, i))
    elif x != y or repr(x) != repr(y):
        out['config'].append({'path': p, 'r8': x, 'r9': y})


c8 = json.loads((C.R8 / 'RUN_CONFIG_DDO154_CX2V006R8_P128_MS128.json').read_bytes())
c9 = json.loads((C.R9 / 'RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json').read_bytes())
walk(c8, c9)
out['numerics_block_canonical_equal'] = (json.dumps(c8['numerics'], sort_keys=True) == json.dumps(c9['numerics'], sort_keys=True))
out['anchor_equal'] = c8['anchor'] == c9['anchor']


def verify(man):
    ok = bad = 0; bads = []; listed = set()
    for line in Path(man).read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        h, p = line.split(None, 1)
        p = p.strip(); listed.add(str(Path(p)))
        try:
            same = C.sha_file(p) == h
        except OSError:
            same = False
        if same: ok += 1
        else: bad += 1; bads.append(p)
    return {'ok': ok, 'bad': bad, 'bad_paths': bads}, listed


for man in (C.R8 / 'HASHES.txt', C.R8 / 'HASHES_FINAL_CX2V006R8.txt', C.R9 / 'HASHES_FINAL_CX2V006R9.txt',
            C.R9 / 'independent_review/HASHES_CX2V001.txt'):
    rep, listed = verify(man)
    out['manifests'][str(man)] = rep
    if man.name == 'HASHES_FINAL_CX2V006R9.txt':
        for root, dirs, files in os.walk(C.R9):
            for f in files:
                fp = str(Path(root) / f)
                if fp not in listed and f != 'HASHES_FINAL_CX2V006R9.txt':
                    out['unlisted_r9_files'].append(fp)
# r8 directory: every file listed by its final manifest still has its bytes; any r8 file newer than r9 build?
r8_files = sorted(str(p) for p in C.R8.rglob('*') if p.is_file())
out['r8_file_count'] = len(r8_files)
out['r8_files_mtime_after_r9_start'] = [p for p in r8_files if os.stat(p).st_mtime > os.stat(C.R9 / 'BUILD_RECORD_CX2V006R9.json').st_mtime - 1]
res = C.write_x(C.OUT / ('DIFF_R8_R9_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '.json'), out)
print(json.dumps({'out': res, 'changed_lines': {k: v['changed_lines'] for k, v in out['sources'].items()},
                  'config_paths': [c['path'] for c in out['config']], 'numerics_equal': out['numerics_block_canonical_equal'],
                  'anchor_equal': out['anchor_equal'], 'manifests': out['manifests'],
                  'unlisted_r9_files': out['unlisted_r9_files'][:20], 'n_unlisted': len(out['unlisted_r9_files']),
                  'r8_late': out['r8_files_mtime_after_r9_start']}, indent=1))
