"""Write LAUNCH_EXT_V001.json and LAUNCH_EXT_V001.commands.txt for C5/C6 (NOT launched; root launches).  Pins from bytes.
Resource numbers: analysis/ESTIMATES_V001.json (models stated there) updated with the measured prep v009 operator
evaluation at G5/G6 (analysis/prep_smoke, iteration-0 prepare = prep + base unit solve) and the registered route-A budget 16.
usage: python3 -I -B make_launch_ext_c2ext.py"""
import hashlib
import json
import shlex
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
MON = EX / 'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
DRV = HERE / 'driver_v009/galaxy_m0_forward_c2v009.py'
EXT1 = '/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
LINK = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext'
GIB = 1024 ** 3
CAPS = {  # rss, wall, output
    'C5_N8': (24 * GIB, 50400, 64 * GIB), 'C6_N8': (32 * GIB, 64800, 96 * GIB),
    'C5_N1': (8 * GIB, 57600, 64 * GIB), 'C6_N1': (12 * GIB, 79200, 96 * GIB)}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    est = json.loads((HERE / 'analysis/ESTIMATES_V001.json').read_text())
    specs = json.loads((HERE / 'specs/SPECS_EXT_M16.json').read_text())['specs']
    pre = HERE / 'prereg_v006/KMAX_MATRIX_PREREG_V006.json'
    cmp_ = HERE / 'prereg_v006/kmax_compare_ext_c2v006.py'
    c4 = est['measured_route_a']['G4']
    s_iter = est['route_a_parallel_measured']['iteration_speedup_N8']
    rec = {'schema': 'UNT_KMAX_EXT_LAUNCH_C2EXT_V001', 'status': 'NOT_LAUNCHED (root launches)',
           'preconditions': ['prereg V006 sealed (SEAL_RECORD_V006 pinning KMAX_MATRIX_PREREG_V006.json %s and kmax_compare_ext_c2v006.py %s)' % (sha(pre)[:16], sha(cmp_)[:16]),
                             'separate review of prep v009 + driver v009 recorded at extension_c5c6/check/REVIEW_V009_PREP_V009_V001.json (V006 v009_admissibility; '
                             'results are inadmissible at comparison time until it exists)',
                             'outdirs absent (the driver and the monitor refuse an existing outdir)'],
           'outdir_location': ('External1 (APFS, PCI-Express SSD, 3.6 TiB free) by its real path %s.  CLAUDE2/runs_ext is a symlink to the same '
                               'directory; the real path is used so that every lexical path the driver writes (os.path.abspath, no symlink '
                               'resolution) equals the resolved path the route-A worker records (Path.resolve()).  The internal volume '
                               '(CLAUDE2/runs) has about 217 GiB free; one C6 call may write up to about 60 GiB.' % EXT1),
           'pins': {'python': PY, 'monitor': {'path': str(MON), 'sha256': sha(MON)}, 'driver_v009': {'path': str(DRV), 'sha256': sha(DRV)},
                    'prereg_v006': {'path': str(pre), 'sha256': sha(pre)}, 'compare_v006': {'path': str(cmp_), 'sha256': sha(cmp_)}},
           'calls': {}, 'primary': ['C5_N8', 'C6_N8'], 'alternates': ['C5_N1', 'C6_N1'],
           'concurrency_note': ('C5_N8 and C6_N8 may run concurrently: route-A phases then hold 2 x (8 workers + parent) = 18 processes on '
                                '6 Super + 12 Performance cores (parallel_route_a_c2 INTERFACE advises <= 17 across stages) and up to about '
                                '36 GiB of RAM (128 GiB installed).  Starting C6 when C5 leaves route A avoids the overlap.'),
           'superseded_not_to_launch': ['specs/CALL_KMAX_C5R3_A2F10_EXT_{N8,N1}_C2V009.json and C6 (route_a.max_iterations 12; replaced by the _M16 specs)',
                                        'driver build 1 aeb6739c (replaced in place by build 2; dryrun/ and dryrun_m16/ were made with build 1)']}
    lines = ['# kmax extension C5/C6 (prereg V006 DRAFT; NOT launched).  Primary = N8; alternates = N1 (serial route A).']
    for key, (rss, wall, outc) in CAPS.items():
        case, var = key.split('_')
        sp = specs[key]
        gid = 'G5' if case == 'C5' else 'G6'
        e = est['estimates'][gid]
        f = e['wave_count_ratio_to_G4']
        smoke = json.loads((HERE / ('analysis/prep_smoke/%s/PREP_V009_SMOKE.json' % case)).read_text())
        it0 = smoke['t_prepare_inputs_s'] + smoke['t_iteration0_prepare_s']
        per = c4['mean_iteration_s'] * f
        post = c4['post_s'] * f
        n_lo, n_hi = (7, 16)
        ra = lambda n, par: it0 + n * (per / s_iter if par else per) + post
        par = var == 'N8'
        outdir = '%s/KMAX_A2F10_%sR3_RUN_V001' % (EXT1, case) if var == 'N8' else '%s/KMAX_A2F10_%sR3_N1_RUN_V001' % (EXT1, case)
        cmd = [PY, '-I', '-B', str(MON), '--driver', str(DRV), '--driver-sha256', sha(DRV), '--spec', sp['path'], '--outdir', outdir,
               '--receipt', outdir + '.receipt.json', '--wall-cap-s', str(wall), '--rss-cap-bytes', str(rss), '--output-cap-bytes', str(outc), '--poll-s', '2.0']
        rec['calls'][key] = {
            'case': case, 'grid': gid, 'route_a_column_workers': sp['route_a_column_workers'], 'route_a_max_iterations': sp['route_a_max_iterations'],
            'spec': {'path': sp['path'], 'sha256': sha(sp['path'])}, 'outdir': outdir, 'outdir_via_symlink': outdir.replace(EXT1, LINK),
            'receipt': outdir + '.receipt.json', 'caps': {'rss_cap_bytes': rss, 'rss_cap_GiB': rss / GIB, 'wall_cap_s': wall, 'output_cap_bytes': outc,
                                                          'output_cap_GiB': outc / GIB, 'poll_s': 2.0},
            'estimates': {'route_a_s_at_7_and_16_iterations': [round(ra(n_lo, par)), round(ra(n_hi, par))],
                          'route_b_s_linear_proportional': [e['route_b_s_linear'], e['route_b_s_proportional']],
                          'call_h_range': [round((ra(n_lo, par) + e['route_b_s_linear']) / 3600, 1), round((ra(n_hi, par) + e['route_b_s_proportional']) / 3600, 1)],
                          'peak_rss_GiB': (e['route_a_N8_peak_rss_GiB'] if par else e['route_a_serial_peak_rss_GiB']) + e['route_b_peak_rss_GiB'],
                          'output_GiB_at_7_iterations': e['output_bytes_GiB_estimate'],
                          'measured_iteration0_prepare_s_standalone': round(it0, 1),
                          'measured_iteration0_peak_rss_GiB_standalone': smoke['peak_rss_after_iteration0_prepare_GiB']},
            'command': cmd, 'command_shell': ' '.join(shlex.quote(x) for x in cmd)}
        lines += ['', '## %s (%s, %s, route_a column_workers %d, max_iterations %d)' % (key, case, gid, sp['route_a_column_workers'], sp['route_a_max_iterations']),
                  rec['calls'][key]['command_shell']]
    cases_tmpl = {'C4': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001/result.json',
                  'C5': rec['calls']['C5_N8']['outdir'] + '/result.json', 'C6': rec['calls']['C6_N8']['outdir'] + '/result.json',
                  'C3': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C3R3_D7R3_RUN_V001/result.json',
                  'C2': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_C2R3_D7R3_RUN_V001/result.json',
                  'R': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/KMAX_A2F10_RR3_D7R3_RUN_V001/result.json'}
    rec['comparison_after_runs'] = {
        'cases_file_content': cases_tmpl,
        'command': [PY, '-I', '-B', str(cmp_), '--prereg', str(pre), '--cases', '<CASES_EXT.json with cases_file_content>', '--outdir',
                    str(HERE / 'verdict_ext/COMPARE_EXT_V001'), '--bracket-recovery', str(EX / 'kmax_prereg_v005_c2/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json')]}
    lines += ['', '## comparison after both receipts exist (CASES_EXT.json = comparison_after_runs.cases_file_content in LAUNCH_EXT_V001.json)',
              ' '.join(shlex.quote(x) for x in rec['comparison_after_runs']['command'])]
    with open(HERE / 'LAUNCH_EXT_V001.json', 'w') as f:  # regenerated whenever the V006 draft changes (unsealed)
        json.dump(rec, f, indent=1)
    with open(HERE / 'LAUNCH_EXT_V001.commands.txt', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    for k, v in rec['calls'].items():
        print(k, v['spec']['sha256'][:16], v['caps']['rss_cap_GiB'], v['caps']['wall_cap_s'], v['caps']['output_cap_GiB'], v['estimates']['call_h_range'], v['estimates']['peak_rss_GiB'], v['estimates']['route_a_s_at_7_and_16_iterations'])


if __name__ == '__main__':
    main()
