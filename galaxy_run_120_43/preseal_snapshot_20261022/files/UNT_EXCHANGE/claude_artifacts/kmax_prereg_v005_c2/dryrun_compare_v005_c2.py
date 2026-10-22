"""Compare driver-v001 dry runs (simulate mode, no stage executed) of the failed S2/Y2 specs and the bound C2
spec with the D7 recovery specs S2R/Y2R/C2R (Claude2 lane, c2v005).  Reads only dryrun/<name>/ produced by
galaxy_m0_forward_c2v001.py dry-run.  Writes dryrun/DRYRUN_COMPARE_V001.json (exclusive create).
usage: python3 -I -B dryrun_compare_v005_c2.py
"""
import glob
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DR = HERE / 'dryrun'
WIDENED = ['5', '6', '7', '8', '9', '45', '50']
R1_ENTRY = [151250000.0, 317625000.0]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + str(k)))
        return out
    if isinstance(o, list) and o and any(isinstance(x, (dict, list)) for x in o):
        out = {}
        for i, v in enumerate(o):
            out.update(leaves(v, p + '/' + str(i)))
        return out
    return {p: o}


def diff(a, b):
    la, lb = leaves(a), leaves(b)
    return sorted(k for k in set(la) | set(lb) if la.get(k, '<absent>') != lb.get(k, '<absent>'))


def fs_table(name):
    tab, solver = {}, None
    for f in sorted(glob.glob(str(DR / name / 'simulated_call/inputs/fs_controls_*.json'))):
        c = json.loads(Path(f).read_text())
        s = {k: v for k, v in c['solver'].items() if k != 'enthalpy_bracket'}
        if solver is not None and s != solver:
            raise SystemExit('solver block differs inside %s' % name)
        solver = s
        for i in c['radial_indices']:
            if str(i) in tab:
                raise SystemExit('column %s in two fs runs of %s' % (i, name))
            tab[str(i)] = c['solver']['enthalpy_bracket']
    return tab, solver


def norm_argv(argv, name):
    """$DRY for the report dir; stage-dir counters (NN_) masked, since they shift with the number of fs column runs."""
    import re
    pre = str(DR / name)
    return [re.sub(r'/stages/[0-9][0-9]_', '/stages/NN_', x.replace(pre, '$DRY')) for x in argv]


def stage_view(rep, name, drop_controls=False):
    out = []
    for s in rep['stages']:
        argv = norm_argv(s.get('argv') or [], name)
        if drop_controls:   # controls file bytes legitimately differ (bracket table); compared separately
            argv = ['<sha>' if (i > 0 and argv[i - 1] == '--controls-sha256') else a for i, a in enumerate(argv)]
            argv = ['<sha>' if (i > 0 and argv[i - 1] == '--column-manifest-sha256') else a for i, a in enumerate(argv)]
        nd = lambda o: json.loads(norm_argv([json.dumps(o, sort_keys=True)], name)[0])   # same $DRY / NN_ masking inside values
        out.append({'name': s['name'], 'kind': s.get('kind'), 'script_sha256': s.get('script_sha256'), 'argv': argv,
                    'stage_globals': nd(s.get('stage_globals')), 'module_patches': nd(s.get('module_patches')), 'mask': nd(s.get('mask'))})
    return out


def pair(old, new):
    ro = json.loads((DR / old / 'DRYRUN_REPORT.json').read_text())
    rn = json.loads((DR / new / 'DRYRUN_REPORT.json').read_text())
    so = json.loads(Path(ro['call_spec']).read_text())
    sn = json.loads(Path(rn['call_spec']).read_text())
    to, solo = fs_table(old)
    tn, soln = fs_table(new)
    col_diff = sorted((i for i in set(to) | set(tn) if to.get(i) != tn.get(i)), key=int)
    res = {'old': {'name': old, 'call_spec': ro['call_spec'], 'call_spec_sha256': ro['call_spec_sha256'], 'driver_sha256': ro['driver_sha256']},
           'new': {'name': new, 'call_spec': rn['call_spec'], 'call_spec_sha256': rn['call_spec_sha256'], 'driver_sha256': rn['driver_sha256']},
           'spec_leaf_diff': diff(so, sn),
           'normalized_spec_leaf_diff': diff(ro['normalized_spec'], rn['normalized_spec']),
           'seed_equal': ro['seed'] == rn['seed'] if old != 'F10' else None,
           'route_a_identity': [((ro['identity'].get('route_a') or {}).get('custody') or {}).get('identity_sha256'),
                                ((rn['identity'].get('route_a') or {}).get('custody') or {}).get('identity_sha256')],
           'fs_columns_covered': [sorted(map(int, to)) == list(range(72)), sorted(map(int, tn)) == list(range(72))],
           'fs_solver_block_equal_except_bracket': solo == soln,
           'fs_bracket_columns_differing': col_diff,
           'fs_bracket_new_values': {i: tn[i] for i in col_diff},
           'fs_bracket_old_values': {i: to[i] for i in col_diff},
           'n_stages': [len(ro['stages']), len(rn['stages'])],
           'stage_names': [[s['name'] for s in ro['stages']], [s['name'] for s in rn['stages']]],
           'pin_problems': [ro['summary'].get('pin_problems'), rn['summary'].get('pin_problems')],
           'scipy_imports': [ro['summary'].get('scipy_imports'), rn['summary'].get('scipy_imports')]}
    if old != 'F10':
        vo, vn = stage_view(ro, old, True), stage_view(rn, new, True)
        # stage rows other than fs column runs (whose grouping follows the bracket table) must be identical
        nonfs_o = [s for s in vo if not s['name'].startswith('fs_columns_')]
        nonfs_n = [s for s in vn if not s['name'].startswith('fs_columns_')]
        res['non_fs_column_stage_rows_identical'] = nonfs_o == nonfs_n
        fs_o = [s for s in vo if s['name'].startswith('fs_columns_')]
        fs_n = [s for s in vn if s['name'].startswith('fs_columns_')]
        strip = lambda rows: [{k: v for k, v in s.items() if k not in ('name', 'argv')} for s in rows]
        res['fs_column_stage_rows_identical_except_name_argv'] = (len(set(json.dumps(x, sort_keys=True) for x in strip(fs_o) + strip(fs_n))) == 1)
        res['fs_run_grouping'] = [[json.loads(Path(f).read_text())['radial_indices'] for f in sorted(glob.glob(str(DR / n / 'simulated_call/inputs/fs_controls_*.json')))]
                                  for n in (old, new)]
        expect_spec = sorted(['/label'] + ['/numerics/brackets/rule/fs_absolute_overrides/%s' % i for i in WIDENED])
        res['verdict'] = bool(res['spec_leaf_diff'] == expect_spec and res['normalized_spec_leaf_diff'] == expect_spec and res['seed_equal']
                              and res['route_a_identity'][0] == res['route_a_identity'][1] and all(res['fs_columns_covered'])
                              and res['fs_solver_block_equal_except_bracket'] and col_diff == WIDENED
                              and all(tn[i] == R1_ENTRY for i in WIDENED) and res['non_fs_column_stage_rows_identical']
                              and res['fs_column_stage_rows_identical_except_name_argv'])
        res['verdict_rule'] = ('PASS iff spec and normalized-spec leaf differences are exactly {label} + fs_absolute_overrides entries %s; '
                               'same seed and admitted route-A identity; fs bracket table differs exactly at those columns with R1 values; '
                               'every non-fs-column stage row identical (argv/globals/patches/mask, controls shas masked); fs column rows '
                               'identical apart from name/argv (grouping follows the bracket table)' % WIDENED)
    else:
        res['verdict_rule'] = 'diagnostic: F10 bound call (computes route A/reference/body, passes 4) vs C2R (admits them, passes 6, R1)'
        res['verdict'] = bool(col_diff == WIDENED and all(tn[i] == R1_ENTRY for i in WIDENED) and all(res['fs_columns_covered'])
                              and res['fs_solver_block_equal_except_bracket'])
    return res


def main():
    out = {'schema': 'UNT_KMAX_D7R1_DRYRUN_COMPARE_C2_V001', 'script_sha256': sha(__file__),
           'driver': {'path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py',
                      'sha256': sha('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py')},
           'pairs': {'S2_vs_S2R': pair('S2', 'S2R'), 'Y2_vs_Y2R': pair('Y2', 'Y2R'), 'F10_vs_C2R': pair('F10', 'C2R')},
           'reports': {n: sha(DR / n / 'DRYRUN_REPORT.json') for n in ('S2', 'S2R', 'Y2', 'Y2R', 'F10', 'C2R')}}
    with open(DR / 'DRYRUN_COMPARE_V001.json', 'x') as f:
        json.dump(out, f, indent=1)
        f.write('\n')
    for k, v in out['pairs'].items():
        print(k, 'verdict', v['verdict'], 'spec_diff', v['spec_leaf_diff'], 'fs_cols', v['fs_bracket_columns_differing'],
              'stages', v['n_stages'], 'nonfs_identical', v.get('non_fs_column_stage_rows_identical'))
    return 0 if all(v['verdict'] for v in out['pairs'].values()) else 1


if __name__ == '__main__':
    sys.exit(main())
