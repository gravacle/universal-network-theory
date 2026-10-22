"""Write SEAL_READY.json and HASHES.txt for KMAX prereg V005 (Claude2 lane).  Existence checks only on run
directories (no result.json / finish.json is opened).  Every hash from bytes.  Exclusive create.
usage: python3 -I -B make_seal_ready_v005_c2.py
"""
import hashlib
import json
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
MON = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
       'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107')
CAPS = ['--wall-cap-s', '21600', '--rss-cap-bytes', '3221225472', '--output-cap-bytes', '17179869184', '--poll-s', '2.0']  # = S2/Y2 first attempts


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def state(name):
    d = RUNS / name
    return {'dir_exists': d.is_dir(), 'result_json_exists': (d / 'result.json').exists(), 'finish_json_exists': (d / 'finish.json').exists(),
            'receipt_exists': Path(str(d) + '.receipt.json').exists(), 'launch_file_exists': Path(str(d) + '.receipt.json.launch.json').exists()}


def q(x):
    return "'" + x + "'" if ' ' in x else x


def main():
    pre = json.loads((OUT / 'KMAX_MATRIX_PREREG_V005.json').read_text())
    d7 = pre['amendment_v005']['d7_recovery']
    drv = pre['binding_inputs']['drivers']
    if sha(MON[0]) != MON[1]:
        raise SystemExit('monitor sha mismatch')
    launches = {}
    for cid in ('S2R', 'Y2R', 'C2R'):
        c = d7['calls'][cid]
        if sha(c['path']) != c['sha256']:
            raise SystemExit('spec sha mismatch %s' % cid)
        argv = [PY, '-I', '-B', MON[0], '--driver', drv['v001']['path'], '--driver-sha256', drv['v001']['sha256'], '--spec', c['path'],
                '--outdir', c['outdir'], '--receipt', c['outdir'] + '.receipt.json'] + CAPS
        launches[cid] = {'case': c['case'], 'spec_sha256': c['sha256'], 'driver': 'v001', 'argv': argv, 'shell': ' '.join(q(x) for x in argv),
                         'outdir_state_now': state(Path(c['outdir']).name)}
    runs = {}
    names = sorted(p.name for p in RUNS.iterdir() if p.is_dir() and (p.name.startswith('KMAX_') or p.name.startswith('DDO154_ROUTE_B_C2V005')
                                                                     or p.name.startswith('A2_ANCHOR_F10')))
    planned = [Path(c['outdir']).name for c in d7['calls'].values()] + [Path(t['outdir']).name for t in d7['templates'].values()]
    for n in sorted(set(names) | set(planned)):
        runs[n] = state(n)
    files = sorted(p for p in OUT.rglob('*') if p.is_file() and 'test_runs' not in p.parts and p.name not in ('SEAL_READY.json', 'HASHES.txt'))
    must_absent = {n: runs[n] for n in planned}
    v005_runs = {n: runs[n] for n in runs if n.endswith('_V005_RUN_V001') or n.startswith('DDO154_ROUTE_B_C2V005')}
    ready = {'schema': 'KMAX_PREREG_V005_SEAL_READY', 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
             'prereg': {'path': str(OUT / 'KMAX_MATRIX_PREREG_V005.json'), 'sha256': sha(OUT / 'KMAX_MATRIX_PREREG_V005.json')},
             'compare': {'path': str(OUT / 'kmax_compare_c2v005.py'), 'sha256': sha(OUT / 'kmax_compare_c2v005.py'),
                         'pins_prereg_sha256': [l for l in (OUT / 'kmax_compare_c2v005.py').read_text().splitlines() if l.startswith('PREREG_SHA256')][0].split("'")[1]},
             'd7_recovery_R1': {'path': d7['R1']['recovery_file']['path'], 'sha256': sha(d7['R1']['recovery_file']['path'])},
             'tests': json.loads((OUT / 'test_runs/RUN_V001/TEST_RESULTS.json').read_text())['n_pass'],
             'tests_total': json.loads((OUT / 'test_runs/RUN_V001/TEST_RESULTS.json').read_text())['n'],
             'test_results': {'path': str(OUT / 'test_runs/RUN_V001/TEST_RESULTS.json'), 'sha256': sha(OUT / 'test_runs/RUN_V001/TEST_RESULTS.json')},
             'dryrun_compare': {'path': str(OUT / 'dryrun/DRYRUN_COMPARE_V001.json'), 'sha256': sha(OUT / 'dryrun/DRYRUN_COMPARE_V001.json'),
                                'verdicts': {k: v['verdict'] for k, v in json.loads((OUT / 'dryrun/DRYRUN_COMPARE_V001.json').read_text())['pairs'].items()}},
             'seal_preconditions': {
                 'no_v005_result_or_finish_exists': not any(v['result_json_exists'] or v['finish_json_exists'] for v in v005_runs.values()),
                 'no_recovery_outdir_exists': not any(v['dir_exists'] for v in must_absent.values())},
             'v005_runs_state': v005_runs, 'recovery_outdirs_state': must_absent, 'run_dirs_state': runs,
             'launch_commands_after_seal': launches,
             'launch_order_note': 'S2R, Y2R, C2R are independent (each admits the F10 prefix; v001). C3R/C4R/RR and S3/Y3/S4/Y4 are filled with '
                                  'make_kmax_v005_c2.py fill TEMPLATE <cube v005 outdir> OUT_SPEC after the cube v005 prefix exists, run under v005.',
             'statement': 'Prepared by Claude2 for sealing. Run directories were checked for existence only; no result.json or finish.json of a '
                          '*_V005_RUN_V001 or DDO154_ROUTE_B_C2V005_* run was opened.',
             'files': {str(p.relative_to(OUT)): sha(p) for p in files}}
    with open(OUT / 'SEAL_READY.json', 'x') as f:
        json.dump(ready, f, indent=1)
        f.write('\n')
    with open(OUT / 'HASHES.txt', 'x') as f:
        for p in files + [OUT / 'SEAL_READY.json']:
            f.write('%s  %s\n' % (sha(p), p.relative_to(OUT)))
    print(json.dumps({k: ready[k] for k in ('prereg', 'compare', 'd7_recovery_R1', 'tests', 'tests_total', 'seal_preconditions')}, indent=1))
    print(json.dumps({k: v['shell'] for k, v in launches.items()}, indent=1))


if __name__ == '__main__':
    main()
