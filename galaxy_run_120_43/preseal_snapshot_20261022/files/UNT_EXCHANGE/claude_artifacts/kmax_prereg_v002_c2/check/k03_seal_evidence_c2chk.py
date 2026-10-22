"""CHECK_V001 K03 (independent checker, Claude2 lane): SEAL_RECORD evidence from file METADATA only.
os.stat / os.walk / os.listdir only under CLAUDE2/runs/A2_ANCHOR_* and KMAX_*: no file there is opened.
Volume atime policy (measured by this checker on a scratch file, see CHECK_V001.md s5): a read updates atime only
when atime <= mtime (relatime-like), so atime > mtime means "read at least once after the last write, first such
read at atime"; atime <= mtime means "not read since the last write".  Also: one robustness probe of evaluate().
usage: python3 -I -B k03_seal_evidence_c2chk.py NEW_OUT_JSON
"""
import collections
import copy
import datetime as dt
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/kmax_prereg_v002_c2')
SEAL = json.loads((D / 'SEAL_RECORD.json').read_bytes())
SEAL_NS = int(dt.datetime.strptime(SEAL['utc'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc).timestamp() * 1e9)


def utc(ns):
    return dt.datetime.fromtimestamp(ns / 1e9, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


rows = []
for top in sorted(os.listdir(RUNS)):
    if not (top.startswith('A2_ANCHOR') or top.startswith('KMAX')):
        continue
    p0 = RUNS / top
    items = [p0] if p0.is_file() else [Path(dp) / n for dp, dn, fn in os.walk(p0) for n in fn]
    for p in items:
        st = os.stat(p, follow_symlinks=False)
        rows.append({'path': str(p.relative_to(RUNS)), 'birth': utc(int(st.st_birthtime * 1e9)), 'mtime_ns': st.st_mtime_ns,
                     'atime_ns': st.st_atime_ns, 'read_after_write': st.st_atime_ns > st.st_mtime_ns, 'size': st.st_size})


def cls(path):
    for pat, lab in (('/checkpoint/iteration_', 'route-A checkpoint iteration json'), ('/checkpoint/IDENTITY.json', 'route-A IDENTITY.json'),
                     ('/checkpoint/attempts/', 'route-A attempts json'), ('/attempt_000/start.json', 'route-A attempt start.json'),
                     ('/node_diagnostics/', 'route-A node_diagnostics'), ('/inputs/', 'inputs'), ('/blobs/', 'route-A blobs'),
                     ('result.json', 'result.json'), ('finish.json', 'finish.json'), ('progress.jsonl', 'progress.jsonl')):
        if pat in path:
            return lab
    return 'other'


def window(lo_ns, hi_ns):
    c = collections.Counter()
    for r in rows:
        if lo_ns <= r['atime_ns'] <= hi_ns:
            c[(r['path'].split('/')[0], cls(r['path']), r['path'].rsplit('.', 1)[-1] if '.' in r['path'] else '')] += 1
    return [{'run': k[0], 'class': k[1], 'ext': k[2], 'n': v} for k, v in sorted(c.items())]


anchor = [r for r in rows if r['path'].startswith('A2_ANCHOR')]
pre_seal_reads = [r for r in anchor if r['read_after_write'] and r['atime_ns'] < SEAL_NS]
by_sec = collections.Counter(utc(r['atime_ns'])[:19] for r in pre_seal_reads)
scan_1456 = window(int(dt.datetime(2026, 10, 17, 14, 56, 28, tzinfo=dt.timezone.utc).timestamp() * 1e9),
                   int(dt.datetime(2026, 10, 17, 14, 56, 30, tzinfo=dt.timezone.utc).timestamp() * 1e9))
scan_1508 = window(int(dt.datetime(2026, 10, 17, 15, 8, 30, tzinfo=dt.timezone.utc).timestamp() * 1e9),
                   int(dt.datetime(2026, 10, 17, 15, 8, 40, tzinfo=dt.timezone.utc).timestamp() * 1e9))
f3 = RUNS / 'A2_ANCHOR_F3_RUN_V001'
key_files = {}
for rel in ('A2_ANCHOR_F3_RUN_V001/inputs/call_spec.json', 'A2_ANCHOR_F3_RUN_V001/inputs/seed_c2v001.json',
            'A2_ANCHOR_F3_RUN_V001.receipt.json.launch.json', 'A2_ANCHOR_F10_RUN_V001.receipt.json.launch.json',
            'A2_ANCHOR_F3_RUN_V001/stages/01_route_a/attempt_000/result.json', 'A2_ANCHOR_F3_RUN_V001/stages/01_route_a/attempt_000/finish.json',
            'A2_ANCHOR_F3_RUN_V001/progress.jsonl', 'A2_ANCHOR_F3_RUN_V001/stages/01_route_a/checkpoint/IDENTITY.json',
            'KMAX_C2_A2_RUN_V001/result.json', 'KMAX_C2_A2_RUN_V001/finish.json'):
    st = os.stat(RUNS / rel)
    key_files[rel] = {'birth': utc(int(st.st_birthtime * 1e9)), 'mtime': utc(st.st_mtime_ns), 'atime': utc(st.st_atime_ns),
                      'read_after_write': st.st_atime_ns > st.st_mtime_ns}
own = {}
for rel in ('KMAX_MATRIX_PREREG_V002.json', 'kmax_compare_c2v002.py', 'tests_kmax_compare_c2v002.py', 'test_runs/RUN_V002/TEST_RESULTS.json',
            'SEAL_RECORD.json', 'specs_anchor/generator_raw/wave1/SPECS_MANIFEST.json', 'specs_anchor/v002/PATCH_MANIFEST.json', 'HASHES.txt'):
    st = os.stat(D / rel)
    own[rel] = {'birth': utc(int(st.st_birthtime * 1e9)), 'mtime': utc(st.st_mtime_ns), 'before_seal': st.st_mtime_ns <= SEAL_NS + 999999999}
later_dirs = sorted(x for x in os.listdir(RUNS) if os.stat(RUNS / x).st_birthtime * 1e9 > SEAL_NS)

# robustness probe: a non-numeric final change (the driver writes non-finite floats as strings, e.g. 'nan')
cmp_p = D / 'kmax_compare_c2v002.py'
spec = importlib.util.spec_from_file_location('cmp_k03', str(cmp_p))
cmp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmp)
pre = json.loads((D / 'KMAX_MATRIX_PREREG_V002.json').read_bytes())
ns = {'galaxy': 'DDO154', 'physical': pre['anchor']['physical'], 'coefficients': pre['anchor']['coefficients'],
      'numerics': {'composite_grid_spec': None, 'truncation': {'shape': 'cube', 'kmax_inverse_kpc': None},
                   'picard': {'passes': 6, 'speed_change_bound_km_s': 0.01, 'observe_every_pass': True}, 'brackets': pre['anchor']['brackets']}}
ad = {'C2': {'schema': cmp.RESULT_SCHEMA, 'status': 'COMPLETED', 'valid': True, 'rows': {i: 20.0 for i in pre['row_ids']},
             'normalized_spec': ns, 'grid_spec': None, 'truncation': ns['numerics']['truncation'], 'last_change_km_s': 'nan',
             'driver_sha256': pre['binding_inputs']['drivers']['v001']['sha256'], 'call_spec_sha256': 'x' * 64,
             'route_a_identity_sha256': 'a' * 64, 'm4_row_window': None}}
try:
    cmp.evaluate(pre, ad, {'C2': {'V4': True, 'V5': True}}, pre['anchor']['brackets'])
    probe = 'no exception'
except Exception as exc:
    probe = '%s: %s' % (type(exc).__name__, exc)

out = {'schema': 'UNT_KMAX_PREREG_V002_CHECK_K03_C2_V001', 'seal_utc': SEAL['utc'],
       'F3_top_level_result_json_exists_now': (f3 / 'result.json').exists(), 'F3_finish_json_exists_now': (f3 / 'finish.json').exists(),
       'F3_stage_dirs_now': sorted(os.listdir(f3 / 'stages')), 'run_dirs_created_after_seal': later_dirs,
       'key_files': key_files, 'prereg_dir_timeline': own,
       'anchor_pre_seal_reads_after_write_by_second': dict(sorted(by_sec.items())),
       'scan_2026-10-17T14:56:28Z': scan_1456, 'scan_2026-10-17T15:08:30-40Z_this_checker_grep': scan_1508,
       'robustness_probe_last_change_string_nan': probe,
       'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with open(sys.argv[1], 'x') as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: out[k] for k in ('F3_top_level_result_json_exists_now', 'F3_finish_json_exists_now', 'F3_stage_dirs_now', 'run_dirs_created_after_seal',
                                      'anchor_pre_seal_reads_after_write_by_second', 'robustness_probe_last_change_string_nan')}, indent=1))
print(json.dumps(scan_1456, indent=0)[:1500])
print(json.dumps(key_files, indent=1))
