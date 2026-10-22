"""Non-fs-column stage rows of each R2 dry-run vs its R1 dry-run (argv/globals/patches/mask; report dir -> $DRY,
stage counters NN_, controls/manifest shas masked).  Writes DRYRUN_R2_STAGE_ROWS.json (exclusive create)."""
import json, re, sys
from pathlib import Path
V5 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v005_c2')
H = V5 / 'd7_recovery_r2'
PAIRS = {'C2R2': 'dryrun/C2R', 'S2R2': 'dryrun/S2R', 'Y2R2': 'dryrun/Y2R', 'C3R2': 'dryrun_filled/C3R', 'S3R2': 'dryrun_filled/S3', 'Y3R2': 'dryrun_filled/Y3'}
def norm(s, d):
    return re.sub(r'/stages/[0-9][0-9]_', '/stages/NN_', s.replace(str(d), '$DRY'))
def rows(d):
    rep = json.loads((d / 'DRYRUN_REPORT.json').read_text())
    out = []
    for s in rep['stages']:
        if s['name'].startswith('fs_columns_'):
            continue
        argv = [norm(x, d) for x in (s.get('argv') or [])]
        argv = ['<sha>' if i > 0 and argv[i - 1] in ('--controls-sha256', '--column-manifest-sha256') else a for i, a in enumerate(argv)]
        nd = lambda o: json.loads(norm(json.dumps(o, sort_keys=True), d))
        out.append({'name': s['name'], 'kind': s.get('kind'), 'script_sha256': s.get('script_sha256'), 'argv': argv,
                    'stage_globals': nd(s.get('stage_globals')), 'module_patches': nd(s.get('module_patches')), 'mask': nd(s.get('mask'))})
    return out
res = {}
for n, r1 in PAIRS.items():
    a, b = rows(V5 / r1), rows(H / 'dryrun_r2' / n)
    diff = [x['name'] for x, y in zip(a, b) if x != y]
    res[n] = {'r1_dryrun': str(V5 / r1), 'non_fs_stage_names': [x['name'] for x in b], 'identical': a == b, 'differing_rows': diff}
p = H / 'DRYRUN_R2_STAGE_ROWS.json'
with open(p, 'xb') as f:
    f.write((json.dumps(res, indent=1) + '\n').encode())
print(json.dumps(res, indent=1))
