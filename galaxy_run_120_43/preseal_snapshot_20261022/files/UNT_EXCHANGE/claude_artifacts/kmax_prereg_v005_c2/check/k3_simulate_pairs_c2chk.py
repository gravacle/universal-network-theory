"""Checker K3: independent comparison of my own guarded v001 dry runs (check/dryrun_chk/<name>) for
S2 vs S2R, Y2 vs Y2R, F10 vs C2R.  Per-column view (each fs/rfs/le column -> its full solver block), every
simulated input file by bytes, every stage row with paths normalized and fs-run numbering removed.
Also compares my reports with the author's dryrun/<name>/DRYRUN_REPORT.json (path-normalized)."""
import glob
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MY = HERE / 'dryrun_chk'
AU = HERE.parent / 'dryrun'
DECLARED = {'5', '6', '7', '8', '9', '45', '50'}
R1E = [151250000.0, 317625000.0]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def leaves(o, p=''):
    if isinstance(o, dict):
        r = {}
        for k, v in o.items():
            r.update(leaves(v, p + '/' + str(k)))
        return r or {p: {}}
    if isinstance(o, list):
        r = {}
        for i, v in enumerate(o):
            r.update(leaves(v, p + '[%d]' % i))
        return r or {p: []}
    return {p: o}


def ldiff(a, b):
    la, lb = leaves(a), leaves(b)
    return sorted(k for k in set(la) | set(lb) if la.get(k, '<absent>') != lb.get(k, '<absent>'))


def norm(s, root):
    s = s.replace(str(root), '$DRY')
    s = re.sub(r'(fs|rfs|le)_columns_\d\d', r'\1_columns_NN', s)
    s = re.sub(r'/stages/\d\d_', '/stages/NN_', s)
    s = re.sub(r'(fs|rfs|le)_controls_\d\d', r'\1_controls_NN', s)
    return s


def column_table(root):
    """index -> full solver block, per column pass tag (fs, rfs*, le*) from every *_controls_*.json."""
    tab = {}
    for f in sorted(glob.glob(str(root / 'simulated_call/inputs/*controls_*.json'))):
        tag = re.sub(r'_\d\d\.json$', '', Path(f).name)
        c = json.loads(Path(f).read_text())
        for i in c['radial_indices']:
            key = (tag, str(i))
            if key in tab:
                raise SystemExit('dup column %s' % (key,))
            blk = {k: v for k, v in c.items() if k != 'radial_indices'}
            if 'column_enthalpy_brackets' in blk:
                blk['column_enthalpy_brackets'] = blk['column_enthalpy_brackets'].get(str(i))
            tab[key] = json.dumps(blk, sort_keys=True)
    return tab


def other_inputs(root):
    out = {}
    for f in sorted(glob.glob(str(root / 'simulated_call/inputs/*'))):
        n = Path(f).name
        if 'controls_' in n or n.endswith('_manifest.json'):
            continue
        out[n] = sha(f)
    return out


def stage_rows(rep, root):
    rows = []
    for s in rep['stages']:
        r = {k: s.get(k) for k in ('kind', 'script_sha256', 'argv', 'stage_globals', 'module_patches', 'mask')}
        r = json.loads(norm(json.dumps(r, sort_keys=True), root))
        # controls/manifest shas are covered by the column tables
        if r['argv']:
            r['argv'] = ['<sha>' if i > 0 and r['argv'][i - 1] in ('--controls-sha256', '--column-manifest-sha256', '--manifest-sha256') else x
                         for i, x in enumerate(r['argv'])]
        rows.append((re.sub(r'_\d\d$', '_NN', s['name']), json.dumps(r, sort_keys=True)))
    return rows


def compress(rows):
    """collapse consecutive identical fs column rows (grouping into runs follows the bracket table)."""
    out = []
    for n, r in rows:
        if out and out[-1] == (n, r) and n.endswith('_NN'):
            continue
        out.append((n, r))
    return out


def load(name):
    root = MY / name
    rep = json.loads((root / 'DRYRUN_REPORT.json').read_text())
    return root, rep, json.loads(Path(rep['call_spec']).read_text())


def pair(a, b, expect_spec):
    ra, repa, sa = load(a)
    rb, repb, sb = load(b)
    ta, tb = column_table(ra), column_table(rb)
    col_diff = sorted({k for k in set(ta) | set(tb) if ta.get(k) != tb.get(k)})
    fs_cols_diff = sorted({k[1] for k in col_diff if k[0] == 'fs_controls'}, key=int)
    non_fs_col_diff = [k for k in col_diff if k[0] != 'fs_controls']
    new_vals_ok = all(json.loads(tb[('fs_controls', i)])['solver']['enthalpy_bracket'] == R1E for i in fs_cols_diff)
    only_bracket_changed = all(
        {k: v for k, v in json.loads(ta[('fs_controls', i)])['solver'].items() if k != 'enthalpy_bracket'}
        == {k: v for k, v in json.loads(tb[('fs_controls', i)])['solver'].items() if k != 'enthalpy_bracket'}
        and {k: v for k, v in json.loads(ta[('fs_controls', i)]).items() if k != 'solver'} == {k: v for k, v in json.loads(tb[('fs_controls', i)]).items() if k != 'solver'}
        for i in fs_cols_diff)
    oa, ob = other_inputs(ra), other_inputs(rb)
    rows_a, rows_b = stage_rows(repa, ra), stage_rows(repb, rb)
    res = {
        'pair': [a, b],
        'call_spec_sha256': [repa['call_spec_sha256'], repb['call_spec_sha256']],
        'driver_sha256': [repa['driver_sha256'], repb['driver_sha256']],
        'spec_leaf_diff': ldiff(sa, sb),
        'normalized_spec_leaf_diff': ldiff(repa['normalized_spec'], repb['normalized_spec']),
        'seed': [repa['seed'], repb['seed']],
        'route_a_identity': [((repa['identity'].get('route_a') or {}).get('custody') or {}).get('identity_sha256'),
                             ((repb['identity'].get('route_a') or {}).get('custody') or {}).get('identity_sha256')],
        'columns_per_pass': {tag: [sum(1 for k in ta if k[0] == tag), sum(1 for k in tb if k[0] == tag)] for tag in sorted({k[0] for k in ta} | {k[0] for k in tb})},
        'column_blocks_differing_fs': fs_cols_diff,
        'column_blocks_differing_other_passes': non_fs_col_diff,
        'fs_new_values_are_R1': new_vals_ok,
        'fs_only_enthalpy_bracket_changed': only_bracket_changed,
        'other_input_files_differing': sorted(k for k in set(oa) | set(ob) if oa.get(k) != ob.get(k)),
        'n_stages': [len(rows_a), len(rows_b)],
        'stage_rows_equal_after_run_collapse': compress(rows_a) == compress(rows_b),
        'non_fs_stage_rows_equal': [r for r in rows_a if not r[0].startswith('fs_columns')] == [r for r in rows_b if not r[0].startswith('fs_columns')],
        'pin_problems': [repa['summary'].get('pin_problems'), repb['summary'].get('pin_problems')],
        'scipy_imports': [repa['summary'].get('scipy_imports'), repb['summary'].get('scipy_imports')],
        'passes_simulated': [repa.get('passes_simulated'), repb.get('passes_simulated')],
    }
    if expect_spec is not None:
        res['verdict'] = bool(res['spec_leaf_diff'] == expect_spec and res['normalized_spec_leaf_diff'] == expect_spec
                              and res['seed'][0] == res['seed'][1] and res['route_a_identity'][0] == res['route_a_identity'][1] is not None
                              and set(fs_cols_diff) == DECLARED and not non_fs_col_diff and new_vals_ok and only_bracket_changed
                              and not res['other_input_files_differing'] and res['non_fs_stage_rows_equal'])
    return res


def author_match(name):
    mine = json.loads((MY / name / 'DRYRUN_REPORT.json').read_text())
    theirs = json.loads((AU / name / 'DRYRUN_REPORT.json').read_text())
    a = json.loads(norm(json.dumps(mine, sort_keys=True), MY / name))
    b = json.loads(norm(json.dumps(theirs, sort_keys=True), AU / name))
    d = ldiff(a, b)
    return {'n_leaf_diffs': len(d), 'diffs': d[:20],
            'plan_txt_equal_after_norm': norm((MY / name / 'DRYRUN_PLAN.txt').read_text(), MY / name) == norm((AU / name / 'DRYRUN_PLAN.txt').read_text(), AU / name)}


exp = sorted(['/label'] + ['/numerics/brackets/rule/fs_absolute_overrides/%s[0]' % i for i in DECLARED])  # only lo moves (W1 root_below_lo)
out = {'S2_vs_S2R': pair('S2', 'S2R', exp), 'Y2_vs_Y2R': pair('Y2', 'Y2R', exp), 'F10_vs_C2R': pair('F10', 'C2R', None),
       'author_reports_match': {n: author_match(n) for n in ('S2', 'S2R', 'Y2', 'Y2R', 'F10', 'C2R')}}
json.dump(out, sys.stdout, indent=1, default=str)
