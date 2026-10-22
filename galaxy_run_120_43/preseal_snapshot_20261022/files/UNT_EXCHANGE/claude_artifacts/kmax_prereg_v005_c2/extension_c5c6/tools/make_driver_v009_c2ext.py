"""Build driver c2v009 from the bytes of driver_v008_c2/galaxy_m0_forward_c2v008.py (f8e47701) by exact-once text
replacements (each old string must occur exactly once; otherwise REFUSED).  Writes driver_v009/galaxy_m0_forward_c2v009.py
(must not exist) and driver_v009/DIFF_V008_V009.diff.  usage: python3 -I -B make_driver_v009_c2ext.py"""
import difflib
import hashlib
import sys
from pathlib import Path

EX = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
SRC = EX / 'driver_v008_c2/galaxy_m0_forward_c2v008.py'
SRC_SHA = 'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28'
OUT = EX / 'kmax_prereg_v005_c2/extension_c5c6/driver_v009'
SUPERSEDED_BUILD1 = 'aeb6739c707265ddeb55f6bc1f29eed840e1ee6eb3a6aaecebfd9c6ea027651b'
SUPERSEDED_BUILD1_DIFF = '44a767c0d68d727c32673be8f729d95af21b9adade2877badc082383c199ce0a'

R = []
# (1) docstring
R.append(('''"""INERT parameterized clean m=0 ("route B") forward driver, Claude2 lane, galaxy-config binding c2v006.
c2v008 (Claude2 lane driver_v008_c2)''', '''"""INERT parameterized clean m=0 ("route B") forward driver, Claude2 lane, galaxy-config binding c2v006.
c2v009 (Claude2 lane kmax_prereg_v005_c2/extension_c5c6): successor of driver_v008_c2/galaxy_m0_forward_c2v008.py (f8e47701).
Changes ONLY (see the C2V009 comments):
  (a) route-A prep node budget: DDO154 grids of 97..120 nodes/axis run prep v009 (extension_c5c6/prep_successor,
      b4b27a1d = prep v008 except line 130: nk>96 -> nk>120), and only the declared kmax-extension grids G5 (108 nodes,
      kmax 5/kpc) and G6 (120 nodes, kmax 6/kpc) are accepted above 96.  Grids <= 96 nodes/axis select prep v007/v008
      exactly as c2v008, so their requests, inputs and reports are byte-identical to c2v008.  Prep v009 has no review
      pin in this driver (its review is the separate review named by prereg V006); prep_info records that.
  (b) OPTIONAL numerics.route_a.max_iterations M (int 1..32): the per-call seed numerical_inputs.max_iterations, the
      route-A outer-iteration budget.  The serial and parallel solvers use it only as the loop bound
      (for iteration in range(start_iteration, max_iterations)) and record it in the checkpoint identity controls, so
      a route A that converges at iteration < min(8, M) computes the same arrays with M as with the base value 8.
      Absent: the per-call seed is exactly the c2v008 seed.  With an admitted route A it is allowed and must equal the
      value the admitted checkpoint was computed with: it enters the per-call seed, and route_a_custody blocks a seed sha
      that differs from the checkpoint's caller seed (an admitted rerun of a C5/C6 prefix carries the same value).
c2v008 text follows.
c2v008 (Claude2 lane driver_v008_c2)'''))
# (2) prep v009 pin
R.append(("""    'prep_v008': (HC / 'ddo_actual_initial_source_preparation_v008.py', 'bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62'),
}""", """    'prep_v008': (HC / 'ddo_actual_initial_source_preparation_v008.py', 'bb05f97452cec43e215fa0853b0674262eb54c75de524b5a640cd984cd137e62'),
    # C2V009 (a): prep v009 = v008 except line 130 (nk>96 -> nk>120).  Used ONLY for grids of 97..120 nodes/axis (G5, G6).
    'prep_v009': (EX / 'kmax_prereg_v005_c2/extension_c5c6/prep_successor/ddo_actual_initial_source_preparation_v009.py',
                  'b4b27a1deb68a2ec24e9bd3700de3a23537fd14b7029e124aab0f7b50bcac8bc'),
}"""))
# (3) budget constant
R.append(("""PREP_V008_MAX_AXIS_NODES = 96  # v008.py:130
""", """PREP_V008_MAX_AXIS_NODES = 96  # v008.py:130
PREP_V009_MAX_AXIS_NODES = 120  # C2V009 (a): v009.py:130
"""))
# (4) declared grids
R.append(("""    'GR': (list(_G2_BREAKS), [6] + [8] * 10 + [6], 92),
}""", """    'GR': (list(_G2_BREAKS), [6] + [8] * 10 + [6], 92),
    # C2V009 (a): kmax-extension grids (prereg V005 decision rule 3 next step; prereg V006 grids G5/G6): G4 plus unit
    # outer panels of order 6 per side.
    'G5': ([-5, -4, -3] + _G2_BREAKS + [3, 4, 5], [6] * 18, 108),
    'G6': ([-6, -5, -4, -3] + _G2_BREAKS + [3, 4, 5, 6], [6] * 20, 120),
}"""))
# (5) normalize guard
R.append(("""            if not hit or grid['total_axis_nodes'] > PREP_V008_MAX_AXIS_NODES:""",
          """            if not hit or grid['total_axis_nodes'] > PREP_V009_MAX_AXIS_NODES:  # C2V009 (a): budget 120"""))
# (6) prep selection
R.append(("""        elif nk <= PREP_V008_MAX_AXIS_NODES:
            prep_key = 'prep_v008'
            verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
        else:
            raise Refusal('%d nodes/axis exceeds every reviewed route-A prep budget (%d)' % (nk, PREP_V008_MAX_AXIS_NODES))
        prep_path, prep_sha = AUX[prep_key]
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk,
                     'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)'
                             % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}""",
          """        elif nk <= PREP_V008_MAX_AXIS_NODES:
            prep_key = 'prep_v008'
            verify_pin(PREP_V008_REVIEW[0], PREP_V008_REVIEW[1], 'prep V008 review')
        elif nk <= PREP_V009_MAX_AXIS_NODES:  # C2V009 (a)
            prep_key = 'prep_v009'
        else:
            raise Refusal('%d nodes/axis exceeds every route-A prep budget (%d)' % (nk, PREP_V009_MAX_AXIS_NODES))
        prep_path, prep_sha = AUX[prep_key]
        prep_info = {'path': str(prep_path), 'sha256': prep_sha, 'axis_nodes': nk,
                     'rule': 'V007 for <=%d nodes/axis (unchanged); V008 for %d..%d (review %s)'
                             % (PREP_V007_MAX_AXIS_NODES, PREP_V007_MAX_AXIS_NODES + 1, PREP_V008_MAX_AXIS_NODES, PREP_V008_REVIEW[1][:16])}
        if prep_key == 'prep_v009':  # C2V009 (a): only here does the record differ from c2v008
            prep_info['rule'] += '; V009 for %d..%d (declared G5/G6 only; review: separate, named by prereg V006)' % (
                PREP_V008_MAX_AXIS_NODES + 1, PREP_V009_MAX_AXIS_NODES)"""))
# (7) LOCAL prep dict item
R.append(("""        if prep_key == 'prep_v008':
            req['stage_dict_items']""", """        if prep_key in ('prep_v008', 'prep_v009'):  # C2V009 (a): v009 is injected the same way as v008
            req['stage_dict_items']"""))
# (8) route_a numerics: optional max_iterations
R.append(("""    _strict(ra, ('column_workers',), 'numerics.route_a')
    n = ra.get('column_workers', 1)
    if type(n) is not int or not 1 <= n <= ROUTE_A_COLUMN_WORKERS_MAX:
        raise Refusal('numerics.route_a.column_workers must be an int in 1..%d, not %r' % (ROUTE_A_COLUMN_WORKERS_MAX, n))
    return {'column_workers': n}""", """    _strict(ra, ('column_workers', 'max_iterations'), 'numerics.route_a')  # C2V009 (b): + max_iterations
    n = ra.get('column_workers', 1)
    if type(n) is not int or not 1 <= n <= ROUTE_A_COLUMN_WORKERS_MAX:
        raise Refusal('numerics.route_a.column_workers must be an int in 1..%d, not %r' % (ROUTE_A_COLUMN_WORKERS_MAX, n))
    out = {'column_workers': n}
    if 'max_iterations' in ra:  # C2V009 (b): present only when declared (absent -> exactly the c2v008 normalization)
        m = ra['max_iterations']
        if type(m) is not int or not 1 <= m <= ROUTE_A_MAX_ITERATIONS_MAX:
            raise Refusal('numerics.route_a.max_iterations must be an int in 1..%d, not %r' % (ROUTE_A_MAX_ITERATIONS_MAX, m))
        out['max_iterations'] = m
    return out"""))
R.append(("""ROUTE_A_COLUMN_WORKERS_MAX = 64  # the worker and solver refuse anything outside 1..64 (INTERFACE "API")
""", """ROUTE_A_COLUMN_WORKERS_MAX = 64  # the worker and solver refuse anything outside 1..64 (INTERFACE "API")
ROUTE_A_MAX_ITERATIONS_MAX = 32  # C2V009 (b): declared ceiling for numerics.route_a.max_iterations (base seed value 8)
"""))
# (9) [removed in build 2: an admitted rerun of a C5/C6 prefix (D7 step 3/4, V2 picard rerun) must carry the same
#     max_iterations so that its per-call seed equals the admitted checkpoint's seed; route_a_custody's seed-sha check
#     is the guard.  Build 1 (aeb6739c, superseded, never pinned outside this lane) refused it.]
# (10) per-call seed
R.append(("""        new['fourier_points_per_axis'] = int(grid['total_axis_nodes'])
    changed = []""", """        new['fourier_points_per_axis'] = int(grid['total_axis_nodes'])
    ra_num = nspec['numerics'].get('route_a') or {}
    if 'max_iterations' in ra_num:  # C2V009 (b): route-A outer-iteration budget (absent: base seed value, c2v008 seed)
        new['max_iterations'] = ra_num['max_iterations']
    changed = []"""))


def main():
    raw = SRC.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SRC_SHA:
        raise SystemExit('REFUSED: v008 sha changed')
    text = raw.decode()
    for i, (old, new) in enumerate(R, 1):
        n = text.count(old)
        if n != 1:
            raise SystemExit('REFUSED: replacement %d occurs %d times' % (i, n))
        text = text.replace(old, new)
    OUT.mkdir(exist_ok=True)
    dst = OUT / 'galaxy_m0_forward_c2v009.py'
    # build 2 replaces build 1 (aeb6739c...) in place; it refuses to overwrite anything else
    if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() not in (SUPERSEDED_BUILD1,):
        raise SystemExit('REFUSED: %s exists and is not build 1' % dst)
    with open(dst, 'w') as f:
        f.write(text)
    diff = ''.join(difflib.unified_diff(raw.decode().splitlines(True), text.splitlines(True),
                                        'driver_v008_c2/galaxy_m0_forward_c2v008.py', 'extension_c5c6/driver_v009/galaxy_m0_forward_c2v009.py'))
    dp = OUT / 'DIFF_V008_V009.diff'
    if dp.exists() and hashlib.sha256(dp.read_bytes()).hexdigest() != SUPERSEDED_BUILD1_DIFF:
        raise SystemExit('REFUSED: diff exists and is not build 1')
    with open(dp, 'w') as f:
        f.write(diff)
    print(dst, hashlib.sha256(text.encode()).hexdigest(), 'replacements', len(R))


if __name__ == '__main__':
    main()
