"""Write v006_r1/LAUNCH_EXT_V002.json and LAUNCH_EXT_V002.commands.txt for C5/C6 under prereg V006 R1 (NOT launched; root
launches).  Successor of extension_c5c6/LAUNCH_EXT_V001.json (route-A budget 16, caps for 16).  Pins from bytes.
Changes (CHECK_V001 M1): R1 specs (max_iterations 32); output caps C5 96 GiB, C6 128 GiB (both variants); wall caps re-derived
for 32 iterations by the rule WALL_RULE below from analysis/ESTIMATES_V001.json (a51d6281) and the measured prep v009 operator
evaluation (analysis/prep_smoke); RSS caps unchanged (24/32/8/12 GiB, >= 1.5x the modelled peaks; the route-A budget is a loop
bound and holds no extra arrays in memory).  Outdirs on the External1 real path.  Sequencing: C6 starts after C5 leaves route A.
usage: python3 -I -B make_launch_r1.py   (outputs must not exist)"""
import hashlib
import json
import math
import os
import shlex
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
LANE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
OUT = LANE / 'v006_r1'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
MON = EX / 'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
DRV = (LANE / 'driver_v009/galaxy_m0_forward_c2v009.py', '999331afd604dd9829aa8f389f43cdb87603d03412d52ba09712226787f18db6')
EST = (LANE / 'analysis/ESTIMATES_V001.json', 'a51d62810550aa0664e5b324962075c2593663e141ff49c8d868f937c9e0a33f')
L1 = (LANE / 'LAUNCH_EXT_V001.json', 'a869567e284923ba5f1fd7276216e5aec3e6ebde0f1460bae4c86fb5e68070b6')
EXT1 = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
LINK = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
RUNS = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs')
G4_ROUTE_A = RUNS / 'KMAX_A2F10_C4_V005_RUN_V001/stages/01_route_a'
GIB = 1024 ** 3
MAXIT = 32
RSS = {'C5_N8': 24 * GIB, 'C6_N8': 32 * GIB, 'C5_N1': 8 * GIB, 'C6_N1': 12 * GIB}
OUTCAP = {'C5': 96 * GIB, 'C6': 128 * GIB}
WALL_RULE = ('wall_cap_s = 3600 * ceil(1.5 * (route_A(32) + route_B_proportional) / 3600), route_A(n) = measured iteration-0 '
             'prepare (analysis/prep_smoke, standalone) + n * G4 mean iteration * (n^3 ratio to G4) [/ 3.03 for N8] + G4 post * '
             '(n^3 ratio); route_B_proportional = ESTIMATES_V001 estimates.G*.route_b_s_proportional (the larger route-B model)')
ROUTE_A_GATE = '"stage": "route_a", "event": "finished"'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def tree_bytes(d):
    return sum(os.lstat(os.path.join(r, f)).st_size for r, _, fs in os.walk(d) for f in fs)


def main():
    for p, s in (DRV, EST, L1):
        if sha(p) != s:
            raise SystemExit('REFUSED pin %s' % p)
    est = json.loads(EST[0].read_text())
    specs = json.loads((OUT / 'specs/SPECS_EXT_M32.json').read_text())['specs']
    pre = OUT / 'prereg/KMAX_MATRIX_PREREG_V006_R1.json'
    cmp_ = OUT / 'prereg/kmax_compare_ext_c2v006_r1.py'
    prej = json.loads(pre.read_text())
    if "PREREG_SHA256 = '%s'" % sha(pre) not in cmp_.read_text():
        raise SystemExit('REFUSED: compare successor does not pin the R1 prereg')
    c4 = est['measured_route_a']['G4']
    s_iter = est['route_a_parallel_measured']['iteration_speedup_N8']
    ra_g4_bytes = tree_bytes(G4_ROUTE_A)
    ra_g4_iters = c4['iterations']
    rec = {'schema': 'UNT_KMAX_EXT_LAUNCH_C2EXT_V002', 'status': 'NOT_LAUNCHED (root launches)',
           'supersedes': {'path': str(L1[0]), 'sha256': L1[1], 'why': 'CHECK_V001 M1: route-A budget 32, output caps C5 96 GiB / C6 128 GiB, wall caps for 32 iterations; prereg V006 R1'},
           'preconditions': ['SEAL_RECORD_V006_R1 exists pinning KMAX_MATRIX_PREREG_V006_R1.json %s and kmax_compare_ext_c2v006_r1.py %s (seal preconditions: v006_r1/SEAL_READY_V006_R1.json)' % (sha(pre), sha(cmp_)),
                             'REVIEW_V009_PREP_V009_V001.json present at extension_c5c6/check/ (a review distinct from this lane; V006 R1 binding_inputs.v009_admissibility: results are inadmissible at comparison time without it)',
                             'no C5/C6 outdir or receipt exists (the driver and the monitor also refuse an existing outdir / receipt)'],
           'outdir_location': ('External1 real path %s (CLAUDE2/runs_ext is a symlink to it; the real path is used so that every lexical path the driver '
                               'writes equals the resolved path the route-A worker records).  Free at R1 build: see disk_free_bytes.' % EXT1),
           'disk_free_bytes': {'External1': os.statvfs(EXT1).f_bavail * os.statvfs(EXT1).f_frsize},
           'pins': {'python': PY, 'monitor': {'path': str(MON), 'sha256': sha(MON)}, 'driver_v009': {'path': str(DRV[0]), 'sha256': sha(DRV[0])},
                    'prereg_v006_r1': {'path': str(pre), 'sha256': sha(pre)}, 'compare_v006_r1': {'path': str(cmp_), 'sha256': sha(cmp_)},
                    'estimates': {'path': str(EST[0]), 'sha256': EST[1]}},
           'cap_rules': {'wall': WALL_RULE, 'output': 'CHECK_V001 M1: C5 96 GiB, C6 128 GiB (N8 and N1 write the same arrays)',
                         'rss': 'unchanged from LAUNCH_EXT_V001 (24/32 GiB N8, 8/12 GiB N1)'},
           'output_model_at_32_iterations': {
               'measured_G4_route_A_bytes': ra_g4_bytes, 'measured_G4_route_A_iterations': ra_g4_iters, 'source': str(G4_ROUTE_A),
               'model': 'route-A bytes ~ iterations (checkpoint blobs, attempt arrays and node diagnostics are per iteration) x n^3 ratio; route-B bytes = ESTIMATES output_bytes_GiB_estimate - route-A(G4 measured) x n^3 ratio; worst case = converged at the last iteration (a route A that exhausts the budget stops the call before route B)'},
           'calls': {}, 'primary': ['C5_N8', 'C6_N8'], 'alternates': ['C5_N1', 'C6_N1'],
           'sequencing': {'order': ['C5_N8', 'C6_N8'],
                          'rule': ('start C5_N8; start C6_N8 when C5 leaves route A, i.e. when the C5 outdir progress.jsonl records %s '
                                   '(driver event of stage route_a) or the C5 receipt exists (the call ended), whichever is first.  C6 never '
                                   'overlaps C5 route A (at most 8 route-A workers + parent + the C5 route-B stages at once).' % ROUTE_A_GATE),
                          'alternates': 'an N1 alternate is used only in place of its N8 primary (same rule, same order)'},
           'superseded_not_to_launch': ['extension_c5c6/specs/CALL_KMAX_C{5,6}R3_A2F10_EXT_{N8,N1}_M16_C2V009.json (max_iterations 16; replaced by v006_r1/specs/*_M32_*)',
                                        'extension_c5c6/specs/CALL_KMAX_C{5,6}R3_A2F10_EXT_{N8,N1}_C2V009.json (max_iterations 12)',
                                        'extension_c5c6/LAUNCH_EXT_V001.json / .commands.txt']}
    lines = ['# kmax extension C5/C6 under prereg V006 R1 (DRAFT until SEAL_RECORD_V006_R1; NOT launched).  Primary = N8; alternates = N1 (serial route A).',
             '# Preconditions: see LAUNCH_EXT_V002.json preconditions and SEAL_READY_V006_R1.json.  Order: C5_N8, then C6_N8 after C5 leaves route A.']
    for key in ('C5_N8', 'C6_N8', 'C5_N1', 'C6_N1'):
        case, var = key.split('_')
        sp = specs[key]
        if sha(sp['path']) != sp['sha256']:
            raise SystemExit('REFUSED spec pin %s' % key)
        gid = 'G5' if case == 'C5' else 'G6'
        e = est['estimates'][gid]
        f = e['wave_count_ratio_to_G4']
        smoke_p = LANE / ('analysis/prep_smoke/%s/PREP_V009_SMOKE.json' % case)
        smoke = json.loads(smoke_p.read_text())
        it0 = smoke['t_prepare_inputs_s'] + smoke['t_iteration0_prepare_s']
        per = c4['mean_iteration_s'] * f
        post = c4['post_s'] * f
        par = var == 'N8'
        ra = lambda n: it0 + n * (per / s_iter if par else per) + post
        upper32 = ra(MAXIT) + e['route_b_s_proportional']
        wall = int(3600 * math.ceil(1.5 * upper32 / 3600))
        ra_gib_32 = ra_g4_bytes / ra_g4_iters * MAXIT * f / GIB
        rb_gib = e['output_bytes_GiB_estimate'] - ra_g4_bytes * f / GIB
        out_est = ra_gib_32 + rb_gib
        outc = OUTCAP[case]
        rss = RSS[key]
        peak = (e['route_a_N8_peak_rss_GiB'] if par else e['route_a_serial_peak_rss_GiB'])
        peak_max = max(peak + e['route_b_peak_rss_GiB'])  # route A and route B do not overlap within a call
        if not (wall >= 1.5 * upper32 and outc >= 1.15 * out_est * GIB and rss >= 1.4 * peak_max * GIB):
            raise SystemExit('REFUSED: cap below rule for %s' % key)
        od = prej['cases'][[c['id'] for c in prej['cases']].index(case)]['outdirs']['primary_N8' if par else 'alternate_N1']
        outdir, receipt = od['outdir'], od['receipt']
        if not outdir.startswith(EXT1 + '/'):
            raise SystemExit('REFUSED: outdir not on the External1 real path')
        cmd = [PY, '-I', '-B', str(MON), '--driver', str(DRV[0]), '--driver-sha256', sha(DRV[0]), '--spec', sp['path'], '--outdir', outdir,
               '--receipt', receipt, '--wall-cap-s', str(wall), '--rss-cap-bytes', str(rss), '--output-cap-bytes', str(outc), '--poll-s', '2.0']
        rec['calls'][key] = {
            'case': case, 'grid': gid, 'route_a_column_workers': sp['route_a_column_workers'], 'route_a_max_iterations': sp['route_a_max_iterations'],
            'spec': {'path': sp['path'], 'sha256': sp['sha256']}, 'outdir': outdir, 'outdir_via_symlink': outdir.replace(EXT1, LINK),
            'receipt': receipt,
            'caps': {'rss_cap_bytes': rss, 'rss_cap_GiB': rss / GIB, 'wall_cap_s': wall, 'wall_cap_h': wall / 3600, 'output_cap_bytes': outc,
                     'output_cap_GiB': outc / GIB, 'poll_s': 2.0},
            'estimates': {'route_a_s_at_7_16_32_iterations': [round(ra(7)), round(ra(16)), round(ra(MAXIT))],
                          'route_b_s_linear_proportional': [e['route_b_s_linear'], e['route_b_s_proportional']],
                          'call_s_upper_at_32': round(upper32), 'wall_cap_over_upper_at_32': round(wall / upper32, 3),
                          'peak_rss_GiB_route_a_route_b': [peak, e['route_b_peak_rss_GiB']], 'rss_cap_over_max_modelled_peak': round(rss / GIB / peak_max, 3),
                          'output_GiB_at_32_iterations_worst_case': round(out_est, 1), 'output_cap_over_estimate': round(outc / GIB / out_est, 3),
                          'measured_iteration0_prepare_s_standalone': round(it0, 1),
                          'scope': 'models of ESTIMATES_V001 (measured under machine load 10-14); UNTESTED at G5/G6 until the calls run'},
            'command': cmd, 'command_shell': ' '.join(shlex.quote(x) for x in cmd)}
    q = shlex.quote
    c5 = rec['calls']['C5_N8']
    gate = ('until grep -qF %s %s 2>/dev/null || [ -e %s ]; do sleep 60; done'
            % (q(ROUTE_A_GATE), q(c5['outdir'] + '/progress.jsonl'), q(c5['receipt'])))
    rec['sequencing']['C6_start_gate_shell'] = gate
    c5n1 = rec['calls']['C5_N1']
    rec['sequencing']['C6_start_gate_shell_if_C5_N1'] = ('until grep -qF %s %s 2>/dev/null || [ -e %s ]; do sleep 60; done'
                                                         % (q(ROUTE_A_GATE), q(c5n1['outdir'] + '/progress.jsonl'), q(c5n1['receipt'])))
    lines += ['', '## 1. C5_N8 (C5, G5, route_a column_workers 8, max_iterations 32): start first', c5['command_shell'],
              '', '## 2. C6_N8 (C6, G6, route_a column_workers 8, max_iterations 32): start after C5 leaves route A (gate, then command)',
              gate, rec['calls']['C6_N8']['command_shell'],
              '', '## alternate C5_N1 (only in place of C5_N8)', c5n1['command_shell'],
              '', '## alternate C6_N1 (only in place of C6_N8; gate on whichever C5 call ran)', rec['sequencing']['C6_start_gate_shell_if_C5_N1'],
              rec['calls']['C6_N1']['command_shell']]
    cases_tmpl = {c: prej['cases'][[x['id'] for x in prej['cases']].index(c)]['bound']['result']['path'] for c in ('C4', 'C3', 'C2', 'R')}
    cases_tmpl.update(C5=c5['outdir'] + '/result.json', C6=rec['calls']['C6_N8']['outdir'] + '/result.json')
    cases_tmpl = {k: cases_tmpl[k] for k in ('C4', 'C5', 'C6', 'C3', 'C2', 'R')}
    rec['comparison_after_runs'] = {
        'cases_file_content': cases_tmpl,
        'cases_note': 'if an N1 alternate ran, its result.json replaces the N8 path of that case',
        'command': [PY, '-I', '-B', str(cmp_), '--prereg', str(pre), '--cases', '<CASES_EXT.json with cases_file_content>', '--outdir',
                    str(LANE / 'verdict_ext/COMPARE_EXT_R1_V001'), '--bracket-recovery', str(EX / 'kmax_prereg_v005_c2/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json')]}
    lines += ['', '## comparison after both receipts exist (CASES_EXT.json = comparison_after_runs.cases_file_content in LAUNCH_EXT_V002.json)',
              ' '.join(shlex.quote(x) for x in rec['comparison_after_runs']['command'])]
    with open(OUT / 'LAUNCH_EXT_V002.json', 'x') as f:
        json.dump(rec, f, indent=1)
        f.write('\n')
    with open(OUT / 'LAUNCH_EXT_V002.commands.txt', 'x') as f:
        f.write('\n'.join(lines) + '\n')
    for k, v in rec['calls'].items():
        print(k, v['spec']['sha256'][:16], 'rss', v['caps']['rss_cap_GiB'], 'wall', v['caps']['wall_cap_s'], 'out', v['caps']['output_cap_GiB'],
              v['estimates']['route_a_s_at_7_16_32_iterations'], 'upper32', v['estimates']['call_s_upper_at_32'], 'outest', v['estimates']['output_GiB_at_32_iterations_worst_case'])


if __name__ == '__main__':
    main()
