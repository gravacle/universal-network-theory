"""Generate the kmax-extension cube call specs C5 (G5, 108 nodes, kmax 5/kpc) and C6 (G6, 120 nodes, kmax 6/kpc) from the
bytes of the R3 cube spec C4R3 (3ea94efe...), for driver c2v009.  Only these leaves change: admit -> {} (route A, reference
and body computed by the call), numerics.composite_grid_spec -> the registered G5/G6 block, numerics.route_a added
({column_workers: N, max_iterations: 12}), label.  Brackets (R3 block 7946b857), physical, coefficients, picard, truncation
(cube), column_workers (fs/rfs 2), reference_compare and schema are copied byte-for-byte.  Variants: N8 (primary) and N1.
Writes specs/ (files must not exist) and specs/SPECS_EXT.json.  usage: python3 -I -B make_ext_specs_c2ext.py [MAX_IT]   (12 -> the first set, no tag; other values -> files tagged _M<MAX_IT>)"""
import hashlib
import json
import re
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
HERE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
C4R3 = (EX / 'kmax_prereg_v005_c2/d7_recovery_r3/specs_d7r3/CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json',
        '3ea94efe3ac2fb270993c7354ced82408c90aeb62e8eb3bf6bcf406d8a41ab17')
R3 = (EX / 'kmax_prereg_v005_c2/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json',
      '7946b8575a2f95fb093c55e35bfffba48f4a8b5daf5e75d89132446b2b9c7453')
KEY_RE = re.compile(r'0|[1-9][0-9]*')
G2B = [-2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2]
GRIDS = {
    'G5': {'breaks_inverse_kpc': [-5, -4, -3] + G2B + [3, 4, 5], 'panel_orders': [6] * 18,
           'scope': ('Seed V002 twelve panels to 2/kpc bitwise unchanged plus outer panels [-5,-4],[-4,-3],[-3,-2],[2,3],[3,4],'
                     '[4,5] order 6 (G4 plus [4,5] per side); full signed cube; k_max extension of P-88 (prereg V006) only; no '
                     'continuum or cutoff error certificate.'),
           'total_axis_nodes': 108, 'version': 'DIRECT_LAPSE_PANELS108_KMAX5_OUTER6_C2EXT_V001'},
    'G6': {'breaks_inverse_kpc': [-6, -5, -4, -3] + G2B + [3, 4, 5, 6], 'panel_orders': [6] * 20,
           'scope': ('Seed V002 twelve panels to 2/kpc bitwise unchanged plus outer panels [-6,-5],[-5,-4],[-4,-3],[-3,-2],'
                     '[2,3],[3,4],[4,5],[5,6] order 6 (G5 plus [5,6] per side); full signed cube; k_max extension of P-88 '
                     '(prereg V006) only; no continuum or cutoff error certificate.'),
           'total_axis_nodes': 120, 'version': 'DIRECT_LAPSE_PANELS120_KMAX6_OUTER6_C2EXT_V001'},
}
import sys
MAX_IT = int(sys.argv[1]) if len(sys.argv) > 1 else 12  # route-A outer-iteration budget (v1 run: 12; superseded by 16, see ROUTE_A_MODE/PROJECTION)
TAG = '' if MAX_IT == 12 else '_M%d' % MAX_IT


def spec_bytes(s):
    return (json.dumps(s, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()


def pinned(p, sha):
    b = Path(p).read_bytes()
    if hashlib.sha256(b).hexdigest() != sha:
        raise SystemExit('REFUSED pin %s' % p)
    return b


def leaves(o, p=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(leaves(v, p + '/' + k))
        return out or {p: '{}'}
    if isinstance(o, list):
        return {p: json.dumps(o)}
    return {p: json.dumps(o)}


def lint(o, path='', bad=None):
    bad = [] if bad is None else bad
    if isinstance(o, dict):
        for k, v in o.items():
            if k.endswith('_overrides') and isinstance(v, dict):
                for k2, v2 in v.items():
                    if not KEY_RE.fullmatch(k2):
                        bad.append('%s/%s/%s' % (path, k, k2))
                    if isinstance(v2, dict):
                        bad += ['%s/%s/%s/%s' % (path, k, k2, k3) for k3 in v2 if not KEY_RE.fullmatch(k3)]
            lint(v, path + '/' + k, bad)
    return bad


def main():
    base = json.loads(pinned(*C4R3))
    r3 = json.loads(pinned(*R3))
    if json.dumps(base['numerics']['brackets'], sort_keys=True) != json.dumps(r3['brackets'], sort_keys=True):
        raise SystemExit('REFUSED: C4R3 brackets are not the R3 block')
    (HERE / 'specs').mkdir(exist_ok=True)
    rec = {'schema': 'UNT_KMAX_EXT_SPECS_C2EXT_V001', 'derived_from': {'path': str(C4R3[0]), 'sha256': C4R3[1]},
           'bracket_block': {'path': str(R3[0]), 'sha256': R3[1]}, 'specs': {}}
    for case, gid in (('C5', 'G5'), ('C6', 'G6')):
        g = GRIDS[gid]
        assert sum(g['panel_orders']) == g['total_axis_nodes'] and len(g['breaks_inverse_kpc']) == len(g['panel_orders']) + 1
        for var, n in (('N8', 8), ('N1', 1)):
            s = json.loads(json.dumps(base))
            s['admit'] = {}
            s['numerics']['composite_grid_spec'] = dict(g)
            s['numerics']['route_a'] = {'column_workers': n, 'max_iterations': MAX_IT}
            s['label'] = ('P-88 kmax extension case %s (grid %s, %d nodes/axis, kmax %d/kpc, cube, prefix compute) under prereg V006 '
                          '(the V005 decision rule 3 next step) | brackets = D7 recovery R3 block 7946b8575a2f95fb (identical to '
                          'C3R3/C4R3) | route A computed by this call, numerics.route_a column_workers %d, max_iterations %d '
                          '(driver c2v009) | derived from C4R3 3ea94efe by admit/grid/route_a/label only'
                          % (case, gid, g['total_axis_nodes'], int(g['breaks_inverse_kpc'][-1]), n, MAX_IT))
            bad = lint(s)
            if bad:
                raise SystemExit('REFUSED lint %s' % bad)
            b = spec_bytes(s)
            p = HERE / 'specs' / ('CALL_KMAX_%sR3_A2F10_EXT_%s%s_C2V009.json' % (case, var, TAG))
            with open(p, 'xb') as f:
                f.write(b)
            la, lb = leaves(base), leaves(s)
            diff = sorted(k for k in set(la) | set(lb) if la.get(k, '<absent>') != lb.get(k, '<absent>'))
            rec['specs']['%s_%s' % (case, var)] = {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'grid': gid,
                                                   'route_a_column_workers': n, 'route_a_max_iterations': MAX_IT,
                                                   'override_key_lint': 'PASS', 'leaf_diff_vs_C4R3': diff,
                                                   'brackets_equal_R3': json.dumps(s['numerics']['brackets'], sort_keys=True) == json.dumps(r3['brackets'], sort_keys=True)}
    out = HERE / ('specs/SPECS_EXT%s.json' % TAG)
    with open(out, 'x') as f:
        json.dump(rec, f, indent=1)
    for k, v in rec['specs'].items():
        print(k, v['sha256'], v['grid'], 'lint', v['override_key_lint'], 'R3', v['brackets_equal_R3'], 'diff', [d.split('/')[1] + '/' + '/'.join(d.split('/')[2:3]) for d in v['leaf_diff_vs_C4R3']][:3], len(v['leaf_diff_vs_C4R3']))


if __name__ == '__main__':
    main()
