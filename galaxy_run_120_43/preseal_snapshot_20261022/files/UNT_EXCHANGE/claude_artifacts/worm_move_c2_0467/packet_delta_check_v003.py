"""Static and fake-module checks of the generated worm-loop pilot V003 packet (nothing launched).

P1 every generated file parses; worker SOURCES and monitor pins equal the bytes on disk; recipe
   WORM_SHA equals the worm module; the other recipe pins equal recipe V001's.
P2 branch_of(u) equals recipe V001's inline expression (worm_loop <-> current_cycle) on 200001 grid
   points and at every threshold and its float neighbours.
P3 recipe V003 prepare/run_prepared with FAKE family recipe, sampler and moves whose __file__ is the
   pinned real file (so pins pass): owner roster, binding, dispatch of every branch, the worm
   move receives (run, path, rng, diag, sampler, roster, state_labels), result['worm_binding'],
   patch removal; nested-patch refusal.
P4 worker V003: seed 2026101701 bound three times, no 2026101612, schedule checks retained, durable
   observer receives state_labels and dstar; monitor V003: output OWNED_L4_WORM_LOOP_RUN_V001,
   absent on disk, launch command, caps unchanged from monitor V002.
Usage: python3 -I -B packet_delta_check_v003.py <output_json>
"""
import ast
import hashlib
import importlib.util
import json
import re
import sys
import types
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
AI = UPC / 'helpers/admission_integration'
RECIPE = HERE / 'owned_L4_worm_loop_recipe_v003.py'
WORKER = HERE / 'owned_L4_worm_loop_root_worker_v003.py'
MONITOR = HERE / 'owned_L4_worm_loop_monitor_v003.py'
WORM = HERE / 'owned_worm_loop_whole_path_c2v001.py'
DUR = HERE / 'owned_worm_committed_capture_durability_v002.py'
R1 = AI / 'owned_L4_current_graph_cycle_recipe_v001.py'
M2 = AI / 'owned_L4_current_graph_cycle_monitor_v002.py'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def literal(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return node.value
    raise KeyError(name)


def main():
    out_path = Path(sys.argv[1])
    res = {}
    # P1
    trees = {p.name: ast.parse(p.read_text()) for p in (RECIPE, WORKER, MONITOR)}
    wt = WORKER.read_text()
    src_entries = re.findall(r"'(\w+)': \((B|X)/'([^']+)', '([0-9a-f]{64})'\)", wt)
    base = {'B': UPC, 'X': Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')}
    worker_pins = {k: (str(base[r] / p), s, sha(base[r] / p) == s) for k, r, p, s in src_entries}
    assert len(worker_pins) == 11 and all(v[2] for v in worker_pins.values()), worker_pins
    assert worker_pins['worm_module'][1] == sha(WORM) and worker_pins['durability'][1] == sha(DUR)
    assert worker_pins['recipe'][1] == sha(RECIPE) and 'cycle_module' not in worker_pins
    mt = MONITOR.read_text()
    mpins = ast.literal_eval(re.search(r"pins=\{Path\(p\):s for p,s in (\{.*?\})\.items\(\)\}", mt).group(1))
    assert all(sha(p) == s for p, s in mpins.items()) and mpins[str(WORKER)] == sha(WORKER)
    r = load(RECIPE, 'recipe_v003_check')
    r1 = load(R1, 'recipe_v001_check')
    assert r.WORM_SHA == sha(WORM)
    for k in ('ADMISSION_SHA', 'FAMILY_RECIPE_SHA', 'BIRTH_SHA'):
        assert getattr(r, k) == getattr(r1, k)
    res['P1_pins'] = {'worker_sources': {k: {'path': v[0], 'sha256': v[1]} for k, v in worker_pins.items()},
                      'monitor_pins': mpins, 'recipe_WORM_SHA': r.WORM_SHA,
                      'recipe_other_pins_equal_v001': True, 'all_parse': True}
    # P2 thresholds
    def v001(u):
        return 'current_cycle' if u < 2./15. else ('birth_residence' if u < 6./15. else ('admission_residence' if u < 10./15. else 'prior_base'))
    grid = list(np.linspace(0., 1., 200001)[:-1])
    for t in (2./15., 6./15., 10./15.):
        grid += [t, float(np.nextafter(t, 0.)), float(np.nextafter(t, 1.))]
    bad = [u for u in grid if (r.branch_of(u) if r.branch_of(u) != 'worm_loop' else 'current_cycle') != v001(u)]
    assert not bad
    res['P2_branch_thresholds_identical_to_v001'] = {'points': len(grid), 'mismatches': 0}
    # P3 fake-module dispatch
    calls = []
    real = {'admission': X_ADM, 'birth': UPC / 'helpers/coefficient_method/owned_worldline_birth_residence_transport_v001.py',
            'family': UPC / 'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py'}
    worm_real = load(WORM, 'worm_for_check')

    def mk(path, **kw):
        ns = types.SimpleNamespace(__file__=str(path), **kw)
        return ns

    def fake_move(tag):
        def mv(*args):
            calls.append((tag, len(args)))
            return args[1], 'rejected'
        return mv
    A, Bv = (0, 1), (2, 3)
    roster_edges = ((0, 2), (0, 3), (1, 2), (1, 3))

    class FakeSampler:
        def _budget_check(self, *a):
            pass

        def _move(self, run, path, rng, diag):
            calls.append(('prior_base', 4))
            return path, 'rejected'

    sampler = FakeSampler()
    us = [0.0, 2./15. - 1e-12, 2./15., 0.3, 6./15., 0.5, 10./15., 0.99]

    class URNG:
        def __init__(self):
            self.i = 0

        def random(self):
            u = us[self.i]
            self.i += 1
            return u

    def fam_prepare(**kw):
        return {'binding': {'graph0': {'A': A, 'B': Bv}}, 'edge_roster': roster_edges,
                'arguments': {'palette_parameters': {'palettes': [(1., (v,)) for v in A + Bv]}},
                'sampler_module': sampler}

    def fam_run_prepared(*, prepared):
        rng = URNG()
        for _ in us:
            sampler._move({'stage': 'fake'}, {'p': 1}, rng, {'sweeps_completed': 0})
        return {'status': 'fake'}
    family = mk(real['family'], prepare=fam_prepare, run_prepared=fam_run_prepared)
    wormf = mk(WORM, move=fake_move('worm_loop'), MODULE_VERSION=worm_real.MODULE_VERSION,
               MAX_WALK_STEPS=worm_real.MAX_WALK_STEPS, LOOKAHEAD=worm_real.LOOKAHEAD)
    birth = mk(real['birth'], move=fake_move('birth_residence'))
    adm = mk(real['admission'], move=lambda *a: (calls.append(('admission_residence', len(a))) or (a[1], 'rejected')))
    opm = mk('unused', state_labels=lambda **kw: ())
    prepared = r.prepare(family_recipe=family, worm_module=wormf, birth_module=birth, admission_module=adm,
                         operator_module=opm, sampler_module=sampler, diamond_adapter=None, progress_stream=None,
                         occupancy_module=None, statistics_module=None, accepted_sampler_sha256=None)
    assert prepared['worm_binding']['owner_roster'] == A + Bv and 'current_cycle_binding' not in prepared
    original = sampler._move
    out = r.run_prepared(prepared=prepared)
    got = [c[0] for c in calls]
    want = [r.branch_of(u) for u in us]
    assert got == want, (got, want)
    assert all(n == 7 for t, n in calls if t == 'worm_loop')
    assert sampler._move == original and not hasattr(sampler, '_worm_loop_recipe_active')
    assert out['worm_binding']['total_worm_loop_probability'] == .10 and out['worm_binding']['module_sha256'] == sha(WORM)
    sampler._current_cycle_recipe_active = True
    try:
        r.run_prepared(prepared=prepared)
        raise AssertionError('nested patch not refused')
    except RuntimeError:
        pass
    del sampler._current_cycle_recipe_active
    bad_worm = mk(WORM, move=fake_move('x'), MODULE_VERSION='other', MAX_WALK_STEPS=1024, LOOKAHEAD=True)
    try:
        r.prepare(family_recipe=family, worm_module=bad_worm, birth_module=birth, admission_module=adm,
                  operator_module=opm, sampler_module=sampler, diamond_adapter=None, progress_stream=None,
                  occupancy_module=None, statistics_module=None, accepted_sampler_sha256=None)
        raise AssertionError('changed walk rule not refused')
    except ValueError:
        pass
    res['P3_recipe_fake_dispatch'] = {'u_values': us, 'branches': got, 'worm_move_arity': 7,
                                      'patch_restored': True, 'nested_patch_refused': True,
                                      'changed_walk_rule_refused': True,
                                      'result_worm_binding_keys': sorted(out['worm_binding'])}
    # P4 worker / monitor text checks
    assert wt.count('2026101701') == 4 and '2026101612' not in wt  # docstring + three bindings
    for s in ("args['burn_in_sweeps']!=512", "args['measurement_sweeps']!=1024", "['moves_per_sweep']!=5",
              "len(args['chain_generators'])!=2", "state_labels=modules['operator'].state_labels",
              "dstar=modules['family_recipe'].TRIAL['dstar']", "result['worm_counters']"):
        assert s in wt, s
    m2 = M2.read_text()
    run_dir = UPC / 'CODEX1' / 'OWNED_L4_WORM_LOOP_RUN_V001'
    assert "out=b/'OWNED_L4_WORM_LOOP_RUN_V001'" in mt and not run_dir.exists()
    caps = re.findall(r"'(wall_cap_seconds|combined_rss_cap_bytes|output_cap_bytes)':([0-9.]+)", m2)
    caps3 = re.findall(r"'(wall_cap_seconds|combined_rss_cap_bytes|output_cap_bytes)':([0-9.]+)", mt)
    assert caps == caps3 and len(caps) == 3
    assert 'out.mkdir(exist_ok=False)' in mt and "for name in ['OMP_NUM_THREADS'" in mt
    res['P4_worker_monitor'] = {'seed_literal_count_incl_docstring': 4, 'old_seed_absent': True,
                                'schedule_checks_retained': True, 'monitor_caps_equal_v002': dict(caps3),
                                'pilot_output_directory': str(run_dir), 'pilot_output_directory_absent': True,
                                'single_thread_env_retained': True,
                                'launch_command': ['/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3', '-I', '-B', str(MONITOR)]}
    res['files'] = {p.name: sha(p) for p in (RECIPE, WORKER, MONITOR, WORM, DUR)}
    with out_path.open('x') as f:
        json.dump(res, f, indent=1)
        f.write('\n')
    print(json.dumps({'ok': True}))


X_ADM = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/admission_residence_0456/admission_residence_transport_c3v001.py')

if __name__ == '__main__':
    main()
