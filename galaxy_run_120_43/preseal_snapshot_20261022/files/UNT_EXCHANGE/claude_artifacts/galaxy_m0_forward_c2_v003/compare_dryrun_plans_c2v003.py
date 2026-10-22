"""Compare a c2v003 dry-run report with a c2v001 dry-run report of the same spec (simulate mode only).
Stage plan = every stage row (name, kind, script, sha, argv, stage_globals, module_patches, mask, note,
argv_comparison, override_comparison, ...) with the report-dir prefix normalized.  Also compares
DRYRUN_PLAN.txt bytes after the same normalization, and lists every other report key that differs.
usage: python3 -I -B compare_dryrun_plans_c2v003.py V003_DIR V001_DIR OUT.json"""
import hashlib
import json
import sys
from pathlib import Path


MANIFEST_MAP = {}


def manifest_map(d):
    """Generated column manifests embed the report-dir path, so their bytes (and the sha passed to the
    rotation stage) differ between two report dirs.  Map each manifest sha to a token derived from its
    content with the report-dir prefix normalized; equal tokens mean equal manifest content."""
    for m in sorted((Path(d) / 'simulated_call' / 'inputs').glob('*_manifest.json')):
        raw = m.read_bytes()
        normed = raw.decode().replace(str(d), '$DRY').encode()
        MANIFEST_MAP[hashlib.sha256(raw).hexdigest()] = 'MANIFEST_CONTENT_' + hashlib.sha256(normed).hexdigest()[:16]


def norm_text(s, a, b):
    s = s.replace(str(a), '$DRY').replace(str(b), '$DRY')
    for k, v in MANIFEST_MAP.items():
        s = s.replace(k, v)
    return s


def norm(obj, a, b):
    return json.loads(norm_text(json.dumps(obj, sort_keys=True), a, b))


def diff_keys(x, y, path=''):
    out = []
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x:
                out.append(path + '/' + k + ' (only in v003 report)')
            elif k not in y:
                out.append(path + '/' + k + ' (only in v001 report)')
            else:
                out += diff_keys(x[k], y[k], path + '/' + k)
    elif x != y:
        out.append(path)
    return out


def main(v3, v1, outp):
    v3, v1 = Path(v3).resolve(), Path(v1).resolve()
    manifest_map(v3)
    manifest_map(v1)
    r3 = json.loads((v3 / 'DRYRUN_REPORT.json').read_text())
    r1 = json.loads((v1 / 'DRYRUN_REPORT.json').read_text())
    s3, s1 = norm(r3['stages'], v3, v1), norm(r1['stages'], v3, v1)
    p3 = norm_text((v3 / 'DRYRUN_PLAN.txt').read_text(), v3, v1)
    p1 = norm_text((v1 / 'DRYRUN_PLAN.txt').read_text(), v3, v1)
    # plan txt header carries the spec sha only; identical spec -> identical header
    res = {'v003_report': str(v3 / 'DRYRUN_REPORT.json'), 'v003_report_sha256': hashlib.sha256((v3 / 'DRYRUN_REPORT.json').read_bytes()).hexdigest(),
           'v001_report': str(v1 / 'DRYRUN_REPORT.json'), 'v001_report_sha256': hashlib.sha256((v1 / 'DRYRUN_REPORT.json').read_bytes()).hexdigest(),
           'manifest_sha_tokens': MANIFEST_MAP,
           'n_stages_v003': len(s3), 'n_stages_v001': len(s1),
           'stage_plan_identical': s3 == s1,
           'stage_rows_differing': [i for i, (a, b) in enumerate(zip(s3, s1)) if a != b],
           'stage_request_fields_identical': [{k: a.get(k) for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask')}
                                              for a in s3] == [{k: b.get(k) for k in ('name', 'kind', 'script', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask')} for b in s1],
           'dryrun_plan_txt_identical_after_prefix_normalization': p3 == p1,
           'executed_stages': [r3.get('executed_stages'), r1.get('executed_stages')],
           'final_rows_identical': r3.get('final_rows_from_saved_chain') == r1.get('final_rows_from_saved_chain'),
           'other_report_differences': diff_keys(norm({k: v for k, v in r1.items() if k != 'stages'}, v3, v1),
                                                 norm({k: v for k, v in r3.items() if k != 'stages'}, v3, v1))}
    Path(outp).write_text(json.dumps(res, indent=1) + '\n')
    print(json.dumps({k: v for k, v in res.items() if k != 'other_report_differences'}, indent=1))
    print('other differences:', len(res['other_report_differences']))
    for x in res['other_report_differences'][:60]:
        print('  ', x)
    return 0 if res['stage_plan_identical'] and res['dryrun_plan_txt_identical_after_prefix_normalization'] else 1


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
