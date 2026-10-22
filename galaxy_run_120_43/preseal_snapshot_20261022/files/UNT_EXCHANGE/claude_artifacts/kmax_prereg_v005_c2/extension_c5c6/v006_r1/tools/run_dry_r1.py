"""Guarded dry runs (driver dry-run = simulate mode; no stage executed, no process created inside the guard) of the V006 R1
specs under driver c2v009 (999331af).  Jobs: the 4 R1 specs (C5/C6 x N8/N1, max_iterations 32; expect exit 0, 0 binding
blockers); NEG_MAXIT_33 (the C5 N8 R1 spec with max_iterations 33; expect refused: above the v009 ceiling); the C5 N8 R1 spec
under c2v008 (expect refused: 108 nodes).  Then summarizes every DRYRUN_REPORT.json and diffs each R1 per-call seed and
simulated input against the superseded _M16 dry run (dryrun_b2, same driver build 2).
nice 10, single-thread BLAS env, <= 4 concurrent.  usage: python3 -I -B run_dry_r1.py   (writes v006_r1/dryrun/, must not exist)"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
LANE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
OUT = LANE / 'v006_r1'
GUARD = OUT / 'tools/guard_r1.py'
DRV = {'v008': (EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py', 'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28'),
       'v009': (LANE / 'driver_v009/galaxy_m0_forward_c2v009.py', '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6')}
SPECS = json.loads((OUT / 'specs/SPECS_EXT_M32.json').read_text())['specs']
B2 = LANE / 'dryrun_b2/dry'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + k))
        return out or {p: '{}'}
    return {p: json.dumps(o)}


def main():
    d = OUT / 'dryrun'
    d.mkdir()
    (d / 'dry').mkdir()
    (d / 'logs').mkdir()
    (d / 'negative').mkdir()
    for k, (p, s) in DRV.items():
        if sha(p) != s:
            raise SystemExit('REFUSED driver pin %s' % k)
    for k, v in SPECS.items():
        if sha(v['path']) != v['sha256']:
            raise SystemExit('REFUSED spec pin %s' % k)
    neg = json.loads(Path(SPECS['C5_N8']['path']).read_text())
    neg['numerics']['route_a']['max_iterations'] = 33
    negp = d / 'negative/NEG_MAXIT_33_FROM_C5_N8_M32.json'
    with open(negp, 'x') as f:
        f.write(json.dumps(neg, indent=1, sort_keys=True) + '\n')
    jobs = [('v009_%s_M32' % k, 'v009', v['path'], 'expect_ok') for k, v in SPECS.items()]
    jobs += [('v009_NEG_MAXIT_33', 'v009', str(negp), 'expect_refused'), ('v008_C5_N8_M32', 'v008', SPECS['C5_N8']['path'], 'expect_refused')]
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[k] = '1'
    os.nice(10)
    pending, running, done = list(jobs), [], []
    while pending or running:
        while pending and len(running) < 4:
            name, v, s, exp = pending.pop(0)
            so = open(d / 'logs' / (name + '.stdout.txt'), 'x')
            se = open(d / 'logs' / (name + '.stderr.txt'), 'x')
            cmd = [PY, '-I', '-B', str(GUARD), str(d / 'logs' / (name + '.guard.json')), str(DRV[v][0]), 'dry-run', '--spec', str(s),
                   '--report-dir', str(d / 'dry' / name)]
            running.append((name, v, s, exp, subprocess.Popen(cmd, stdout=so, stderr=se, env=env, cwd=str(d)), time.time(), so, se))
        time.sleep(0.5)
        for r in list(running):
            name, v, s, exp, p, t, so, se = r
            if p.poll() is not None:
                so.close(); se.close(); running.remove(r)
                done.append({'name': name, 'driver': v, 'driver_sha256': DRV[v][1], 'spec': str(s), 'spec_sha256': sha(s), 'expect': exp,
                             'exit': p.returncode, 'seconds': round(time.time() - t, 2)})
    summ = {'schema': 'UNT_KMAX_EXT_DRYRUN_V006_R1', 'jobs': {}}
    for j in sorted(done, key=lambda x: x['name']):
        name = j['name']
        g = json.loads((d / 'logs' / (name + '.guard.json')).read_text())
        rp = d / 'dry' / name / 'DRYRUN_REPORT.json'
        e = dict(j, guard_denied=g['denied'], guard_velocity_like_opened=g['velocity_like_paths_opened'])
        if rp.is_file():
            r = json.loads(rp.read_text())
            e.update(report_sha256=sha(rp), stages_planned=r.get('stages_planned'), binding_blockers=r.get('binding_blockers'),
                     unexplained_refusals=r.get('unexplained_refusals'), refusals_beyond_pending_inputs=r.get('refusals_beyond_pending_inputs'),
                     remaining_refusals_by_class=r.get('remaining_refusals_by_class'), pin_problems=r.get('pin_problems'),
                     route_a_prep=r.get('route_a_prep'))
        err = (d / 'logs' / (name + '.stderr.txt')).read_text()
        out_ = (d / 'logs' / (name + '.stdout.txt')).read_text()
        if j['expect'] == 'expect_refused':
            txt = (out_ + err)
            e['refusal_text'] = [ln for ln in txt.splitlines() if 'REFUS' in ln.upper() or 'must be' in ln][:3]
            e['as_expected'] = j['exit'] != 0 and not rp.is_file()
        else:
            e['as_expected'] = j['exit'] == 0 and rp.is_file() and e.get('binding_blockers') == [] and e.get('unexplained_refusals') == [] \
                and not g['denied'] and e.get('pin_problems') == []
            key = name[len('v009_'):-len('_M32')]
            inp = d / 'dry' / name / 'simulated_call/inputs'
            b2 = B2 / ('v009_' + key) / 'simulated_call/inputs'
            seed_new, seed_old = json.loads((inp / 'seed_c2v001.json').read_text()), json.loads((b2 / 'seed_c2v001.json').read_text())
            ln, lo = leaves(seed_new), leaves(seed_old)
            e['seed'] = {'sha256': sha(inp / 'seed_c2v001.json'), 'max_iterations': seed_new['numerical_inputs']['max_iterations'],
                         'fourier_points_per_axis': seed_new['numerical_inputs']['fourier_points_per_axis'],
                         'M16_seed': {'path': str(b2 / 'seed_c2v001.json'), 'sha256': sha(b2 / 'seed_c2v001.json')},
                         'leaf_diff_vs_M16_seed': sorted(k for k in set(ln) | set(lo) if ln.get(k) != lo.get(k))}
            rd_new, rd_old = str(d / 'dry' / name), str(B2 / ('v009_' + key))
            files = {}
            for f in sorted(inp.iterdir()):
                if f.name == 'seed_c2v001.json':
                    continue
                a = f.read_text().replace(rd_new, '<REPORT_DIR>')
                b = (b2 / f.name).read_text().replace(rd_old, '<REPORT_DIR>') if (b2 / f.name).is_file() else None
                files[f.name] = a == b
            e['other_simulated_inputs_equal_M16_after_report_dir_substitution'] = files
        summ['jobs'][name] = e
    summ['all_as_expected'] = all(e['as_expected'] for e in summ['jobs'].values())
    summ['n_jobs'] = len(summ['jobs'])
    with open(d / 'DRYRUN_R1_SUMMARY.json', 'x') as f:
        json.dump(summ, f, indent=1)
        f.write('\n')
    for k, e in summ['jobs'].items():
        print(k, 'exit', e['exit'], 'as_expected', e['as_expected'], 'stages', e.get('stages_planned'), 'blockers', e.get('binding_blockers'),
              'seed_maxit', (e.get('seed') or {}).get('max_iterations'), 'seed_diff', (e.get('seed') or {}).get('leaf_diff_vs_M16_seed'),
              'inputs_eq', None if 'other_simulated_inputs_equal_M16_after_report_dir_substitution' not in e else all(e['other_simulated_inputs_equal_M16_after_report_dir_substitution'].values()),
              e.get('refusal_text', ''))
    print('all_as_expected', summ['all_as_expected'])


if __name__ == '__main__':
    main()
