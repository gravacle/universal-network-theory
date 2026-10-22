"""V006 R1 specs (CHECK_V001 M1): the C5 (G5, 108 nodes) and C6 (G6, 120 nodes) cube call specs with
numerics.route_a.max_iterations 32 (the driver c2v009 ceiling ROUTE_A_MAX_ITERATIONS_MAX).  Generated from the bytes of the
R3 cube spec C4R3 (3ea94efe...) exactly as tools/make_ext_specs_c2ext.py does (admit -> {}, composite_grid_spec -> the
registered G5/G6 block, numerics.route_a {column_workers N, max_iterations 32}, label); everything else byte-copied.
Also records the leaf diff of each R1 spec against its superseded _M16 predecessor (expected: /label and
/numerics/route_a/max_iterations only).  Writes v006_r1/specs/ (files must not exist).
usage: python3 -I -B make_specs_r1.py"""
import hashlib
import json
import re
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
LANE = EX / 'kmax_prereg_v005_c2/extension_c5c6'
OUT = LANE / 'v006_r1'
C4R3 = (EX / 'kmax_prereg_v005_c2/d7_recovery_r3/specs_d7r3/CALL_KMAX_C4R3_A2F10_D7R3_C2V005.json',
        '3ea94efe3ac2fb270993c7354ced82408c90aeb62e8eb3bf6bcf406d8a41ab17')
R3 = (EX / 'kmax_prereg_v005_c2/d7_recovery_r3/KMAX_D7_RECOVERY_R3.json',
      '7946b8575a2f95fb093c55e35bfffba48f4a8b5daf5e75d89132446b2b9c7453')
V006 = (LANE / 'prereg_v006/KMAX_MATRIX_PREREG_V006.json', 'f90ab96cc1640cb2bc4204489f3e44e9165eb1aaead9875e7a8e754c9e02eb79')
M16 = {'C5_N8': 'c8321156cafb0867260883ecae5de03680e2f71b194b7ff23533710d3f6a2f3a',
       'C5_N1': 'c7d6b7223e43d362d4306c4fa967e02600e19babfaadca3236a238488e311c1e',
       'C6_N8': 'b7bf831fbf0b7d1aac6ea5c31e2ff45e20e18f8730618f35a878a16d024a71ef',
       'C6_N1': '19b651bf6507de3933f596b3f0e9a8779173cee8ed5234b39c98ab975fa47ab2'}
MAX_IT = 32
KEY_RE = re.compile(r'0|[1-9][0-9]*')


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
    v006 = json.loads(pinned(*V006))
    if json.dumps(base['numerics']['brackets'], sort_keys=True) != json.dumps(r3['brackets'], sort_keys=True):
        raise SystemExit('REFUSED: C4R3 brackets are not the R3 block')
    (OUT / 'specs').mkdir(parents=True, exist_ok=True)
    rec = {'schema': 'UNT_KMAX_EXT_SPECS_C2EXT_V006_R1', 'reason': 'CHECK_V001 (849d1b8d) M1: route_a.max_iterations 32 (v009 ceiling) for C5/C6',
           'derived_from': {'path': str(C4R3[0]), 'sha256': C4R3[1]}, 'bracket_block': {'path': str(R3[0]), 'sha256': R3[1]},
           'grids_from': {'path': str(V006[0]), 'sha256': V006[1], 'keys': ['grids.G5.composite_grid_spec', 'grids.G6.composite_grid_spec']},
           'specs': {}}
    for case, gid in (('C5', 'G5'), ('C6', 'G6')):
        g = v006['grids'][gid]['composite_grid_spec']
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
            p = OUT / 'specs' / ('CALL_KMAX_%sR3_A2F10_EXT_%s_M32_C2V009.json' % (case, var))
            with open(p, 'xb') as f:
                f.write(b)
            la, lb = leaves(base), leaves(s)
            diff = sorted(k for k in set(la) | set(lb) if la.get(k, '<absent>') != lb.get(k, '<absent>'))
            key = '%s_%s' % (case, var)
            p16 = LANE / 'specs' / ('CALL_KMAX_%sR3_A2F10_EXT_%s_M16_C2V009.json' % (case, var))
            s16 = json.loads(pinned(p16, M16[key]))
            l16 = leaves(s16)
            d16 = sorted(k for k in set(l16) | set(lb) if l16.get(k, '<absent>') != lb.get(k, '<absent>'))
            rec['specs'][key] = {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'grid': gid,
                                 'route_a_column_workers': n, 'route_a_max_iterations': MAX_IT,
                                 'override_key_lint': 'PASS', 'leaf_diff_vs_C4R3': diff,
                                 'brackets_equal_R3': json.dumps(s['numerics']['brackets'], sort_keys=True) == json.dumps(r3['brackets'], sort_keys=True),
                                 'supersedes': {'path': str(p16), 'sha256': M16[key]}, 'leaf_diff_vs_superseded_M16': d16,
                                 'only_label_and_max_iterations_differ_from_M16': d16 == ['/label', '/numerics/route_a/max_iterations']}
    with open(OUT / 'specs/SPECS_EXT_M32.json', 'x') as f:
        json.dump(rec, f, indent=1)
        f.write('\n')
    for k, v in rec['specs'].items():
        print(k, v['sha256'], v['grid'], 'lint', v['override_key_lint'], 'R3', v['brackets_equal_R3'], 'nC4R3diff', len(v['leaf_diff_vs_C4R3']),
              'vsM16', v['leaf_diff_vs_superseded_M16'])


if __name__ == '__main__':
    main()
