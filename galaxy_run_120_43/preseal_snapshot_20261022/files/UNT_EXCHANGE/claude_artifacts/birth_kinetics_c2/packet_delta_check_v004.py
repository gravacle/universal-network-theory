"""Static, fake-module and real-prepare checks of the generated worm + channel-bearing Birth V004 packet.

Nothing is launched and nothing is sampled.
P1 every generated file parses; worker SOURCES and monitor pins equal the bytes on disk; worker
   SOURCES equal worker V003's except recipe (-> V004) and birth_module (-> c2v002); recipe V004
   pins equal recipe V003's except BIRTH_SHA (-> c2v002 bytes).
P2 branch_of(u) of recipe V004 equals recipe V003's on 200001 grid points and at every threshold and
   its float neighbours.
P3 recipe V004 prepare/run_prepared with FAKE family recipe, sampler and moves whose __file__ is the
   pinned real file: dispatch of every branch, Birth move receives (run, path, rng, diag, sampler,
   roster) (6 args), result['worm_binding'] names the c2v002 version and selection, patch removal,
   nested-patch refusal, the reviewed V001 Birth module (no MODULE_VERSION) refused.
P4 REAL recipe V004 prepare (actual pinned family recipe, operator, adapter, sampler, statistics,
   worm, Birth, admission modules; preparation only, no sampling call) then the worker V004
   schedule/cap/budget block executed verbatim (extracted from the worker bytes) on that prepared
   object: the worker's frozen-value guards pass, burn-in 1024, measurements 1024, caps, the
   replaced budget hook (soft 8800 s / 3.5 GiB / 3.2M calls) reads the prepared clock and call
   counter, prepared soft thresholds documented.
P5 worker text: seed 2026101702 bound three times (+ docstring), old seed absent; monitor V004:
   output OWNED_L4_WORM_BIRTHK_RUN_V001 absent on disk, hard wall 9000 s, RSS and output caps equal
   monitor V003's, single-thread env and exclusive mkdir retained, launch command.
Usage: python3 -I -B packet_delta_check_v004.py <output_json>
"""
import ast
import hashlib
import importlib.util
import io
import json
import re
import resource
import sys
import time
import types
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
XA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
W3 = XA / 'worm_move_c2_0467'
RECIPE = HERE / 'owned_L4_worm_birthk_recipe_v004.py'
WORKER = HERE / 'owned_L4_worm_birthk_root_worker_v004.py'
MONITOR = HERE / 'owned_L4_worm_birthk_monitor_v004.py'
BIRTH = HERE / 'owned_worldline_birth_residence_transport_c2v002.py'
R3, K3, M3 = (W3 / 'owned_L4_worm_loop_recipe_v003.py', W3 / 'owned_L4_worm_loop_root_worker_v003.py',
              W3 / 'owned_L4_worm_loop_monitor_v003.py')
WORM = W3 / 'owned_worm_loop_whole_path_c2v001.py'
V001 = UPC / 'helpers/coefficient_method/owned_worldline_birth_residence_transport_v001.py'
RUN_DIR = UPC / 'CODEX1' / 'OWNED_L4_WORM_BIRTHK_RUN_V001'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


def sources(text):
    base = {'B': UPC, 'X': XA}
    return {k: (str(base[r] / p), s) for k, r, p, s in re.findall(r"'(\w+)': \((B|X)/'([^']+)', '([0-9a-f]{64})'\)", text)}


def main():
    out_path = Path(sys.argv[1])
    res = {}
    # P1
    for p in (RECIPE, WORKER, MONITOR, BIRTH):
        ast.parse(p.read_text())
    wt, mt = WORKER.read_text(), MONITOR.read_text()
    s4, s3 = sources(wt), sources(K3.read_text())
    assert len(s4) == 11 and all(sha(p) == s for p, s in s4.values()), s4
    assert set(s4) == set(s3)
    assert {k for k in s4 if s4[k] != s3[k]} == {'recipe', 'birth_module'}
    assert s4['recipe'] == (str(RECIPE), sha(RECIPE)) and s4['birth_module'] == (str(BIRTH), sha(BIRTH))
    mpins = ast.literal_eval(re.search(r"pins=\{Path\(p\):s for p,s in (\{.*?\})\.items\(\)\}", mt).group(1))
    assert all(sha(p) == s for p, s in mpins.items()) and mpins[str(WORKER)] == sha(WORKER)
    assert mpins[str(BIRTH)] == sha(BIRTH) and mpins[str(RECIPE)] == sha(RECIPE)
    r = load(RECIPE, 'recipe_v004_check')
    r3 = load(R3, 'recipe_v003_check')
    assert r.BIRTH_SHA == sha(BIRTH) and r.BIRTH_MODULE_VERSION == 'birth_residence_c2v002'
    for k in ('ADMISSION_SHA', 'FAMILY_RECIPE_SHA', 'WORM_SHA', 'WORM_MODULE_VERSION', 'WORM_MAX_WALK_STEPS', 'WORM_LOOKAHEAD'):
        assert getattr(r, k) == getattr(r3, k), k
    res['P1_pins'] = {'worker_sources': {k: {'path': p, 'sha256': s} for k, (p, s) in s4.items()},
                      'worker_sources_changed_vs_v003': ['birth_module', 'recipe'], 'monitor_pins': mpins,
                      'recipe_BIRTH_SHA': r.BIRTH_SHA, 'recipe_other_pins_equal_v003': True, 'all_parse': True}
    # P2
    grid = list(np.linspace(0., 1., 200001)[:-1])
    for t in (2. / 15., 6. / 15., 10. / 15.):
        grid += [t, float(np.nextafter(t, 0.)), float(np.nextafter(t, 1.))]
    assert all(r.branch_of(u) == r3.branch_of(u) for u in grid)
    res['P2_branch_thresholds_identical_to_v003'] = {'points': len(grid), 'mismatches': 0}
    # P3 fake dispatch
    calls = []
    birth_real = load(BIRTH, 'birth_c2v002_check')
    worm_real = load(WORM, 'worm_check')

    def mk(path, **kw):
        return types.SimpleNamespace(__file__=str(path), **kw)

    def fake_move(tag):
        def mv(*args):
            calls.append((tag, len(args)))
            return args[1], 'rejected'
        return mv
    A, Bv = (0, 1), (2, 3)

    class FakeSampler:
        def _budget_check(self, *a):
            pass

        def _move(self, run, path, rng, diag):
            calls.append(('prior_base', 4))
            return path, 'rejected'
    sampler = FakeSampler()
    us = [0.0, 2. / 15. - 1e-12, 2. / 15., 0.3, 6. / 15., 0.5, 10. / 15., 0.99]

    class URNG:
        def __init__(self):
            self.i = 0

        def random(self):
            u = us[self.i]
            self.i += 1
            return u

    def fam_prepare(**kw):
        return {'binding': {'graph0': {'A': A, 'B': Bv}}, 'edge_roster': ((0, 2), (0, 3), (1, 2), (1, 3)),
                'arguments': {'palette_parameters': {'palettes': [(1., (v,)) for v in A + Bv]}},
                'sampler_module': sampler}

    def fam_run_prepared(*, prepared):
        rng = URNG()
        for _ in us:
            sampler._move({'stage': 'fake'}, {'p': 1}, rng, {'sweeps_completed': 0})
        return {'status': 'fake'}
    family = mk(UPC / 'helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py',
                prepare=fam_prepare, run_prepared=fam_run_prepared)
    wormf = mk(WORM, move=fake_move('worm_loop'), MODULE_VERSION=worm_real.MODULE_VERSION,
               MAX_WALK_STEPS=worm_real.MAX_WALK_STEPS, LOOKAHEAD=worm_real.LOOKAHEAD)
    birth = mk(BIRTH, move=fake_move('birth_residence'), MODULE_VERSION=birth_real.MODULE_VERSION)
    adm = mk(XA / 'admission_residence_0456/admission_residence_transport_c3v001.py',
             move=lambda *a: (calls.append(('admission_residence', len(a))) or (a[1], 'rejected')))
    opm = mk('unused', state_labels=lambda **kw: ())
    kw = dict(family_recipe=family, worm_module=wormf, admission_module=adm, operator_module=opm,
              sampler_module=sampler, diamond_adapter=None, progress_stream=None, occupancy_module=None,
              statistics_module=None, accepted_sampler_sha256=None)
    prepared = r.prepare(birth_module=birth, **kw)
    original = sampler._move
    out = r.run_prepared(prepared=prepared)
    got = [c[0] for c in calls]
    assert got == [r.branch_of(u) for u in us], got
    assert all(n == 6 for t, n in calls if t == 'birth_residence') and all(n == 7 for t, n in calls if t == 'worm_loop')
    assert sampler._move == original and not hasattr(sampler, '_worm_loop_recipe_active')
    wb = out['worm_binding']
    assert wb['birth_module_sha256'] == sha(BIRTH) and wb['birth_module_version'] == 'birth_residence_c2v002'
    assert wb['total_birth_residence_probability'] == .20 and wb['module_sha256'] == sha(WORM)
    sampler._worm_loop_recipe_active = True
    try:
        r.run_prepared(prepared=prepared)
        raise AssertionError('nested patch not refused')
    except RuntimeError:
        pass
    del sampler._worm_loop_recipe_active
    try:
        r.prepare(birth_module=mk(V001, move=fake_move('x')), **kw)
        raise AssertionError('V001 Birth transport not refused')
    except ValueError:
        pass
    res['P3_recipe_fake_dispatch'] = {'u_values': us, 'branches': got, 'birth_move_arity': 6, 'worm_move_arity': 7,
                                      'patch_restored': True, 'nested_patch_refused': True,
                                      'v001_birth_module_refused': True,
                                      'birth_owner_selection': wb['birth_owner_selection']}
    # P4 real prepare + verbatim worker schedule/cap/budget block
    mods = {k: load(Path(p), 'real_' + k) for k, (p, s) in s4.items()
            if k not in ('recipe', 'durability')}
    t0 = time.time()
    prepared = r.prepare(family_recipe=mods['family_recipe'], worm_module=mods['worm_module'],
                         birth_module=mods['birth_module'], admission_module=mods['admission_module'],
                         operator_module=mods['operator'], sampler_module=mods['sampler'],
                         diamond_adapter=mods['adapter'], progress_stream=io.StringIO(),
                         occupancy_module=mods['occupancy'], statistics_module=mods['statistics'],
                         accepted_sampler_sha256=s4['sampler'][1])
    args = prepared['arguments']
    lines = wt.splitlines(keepends=True)
    i0 = next(i for i, ln in enumerate(lines) if "args=prepared['arguments']" in ln)
    i1 = next(i for i, ln in enumerate(lines) if "old_seed=prepared['reweighting_capture_record']['rng_entropy']" in ln)
    block = ''.join(ln[16:] if ln.startswith(' ' * 16) else ln.lstrip() for ln in lines[i0:i1])
    ns = {'prepared': prepared, 'resource': resource, 'sys': sys, 'time': time, 'result': {}}
    exec(compile(block, 'worker_v004_schedule_block', 'exec'), ns)
    a = prepared['arguments']
    assert a['burn_in_sweeps'] == 1024 and a['measurement_sweeps'] == 1024 and len(a['chain_generators']) == 2
    assert a['move_parameters']['moves_per_sweep'] == 5
    assert a['caps'] == {'max_events_per_path': 10000, 'max_total_events': 4800000, 'max_sweeps': 4096,
                         'max_channel_enumerations': 3200000}
    assert prepared['reweighting_capture_record']['burn_in_per_chain'] == 1024
    assert a['budget_hook']() is False
    st = prepared['budget_state']()
    clock = prepared['counters']
    clock['primitive_calls'] = 3199999
    assert a['budget_hook']() is False
    clock['primitive_calls'] = 3200000
    assert a['budget_hook']() is True
    clock['primitive_calls'] = 0
    start = clock['start']
    clock['start'] = time.monotonic() - 8799.
    assert a['budget_hook']() is False
    clock['start'] = time.monotonic() - 8800.5
    assert a['budget_hook']() is True
    clock['start'] = start
    assert 'elapsed>=8800.' in block and '3584*1024**2' in block
    res['P4_real_prepare_and_worker_block'] = {
        'prepare_seconds': round(time.time() - t0, 1), 'worker_block_lines': i1 - i0,
        'schedule_after_block': {'burn_in_sweeps': a['burn_in_sweeps'], 'measurement_sweeps': a['measurement_sweeps'],
                                 'chains': len(a['chain_generators']), 'moves_per_sweep': 5},
        'caps_after_block': a['caps'], 'budget_state_keys': sorted(st),
        'budget_hook_calls_threshold_3200000': True, 'budget_hook_wall_threshold_8800s': True,
        'schedule_binding_record': ns['result']['schedule_binding'],
        'birth_module_version_bound': prepared['worm_binding']['birth_module'].MODULE_VERSION,
        'no_sampling_call': True}
    # P5 worker/monitor text
    assert wt.count('2026101702') == 4 and '2026101701' not in wt
    for s in ("args['burn_in_sweeps']!=512", "args['measurement_sweeps']!=1024", "['moves_per_sweep']!=5",
              "len(args['chain_generators'])!=2", "state_labels=modules['operator'].state_labels",
              "dstar=modules['family_recipe'].TRIAL['dstar']", "result['worm_counters']",
              "args['budget_hook']=lambda: bool(budget_state()['stop_requested'])"):
        assert s in wt, s
    m3 = M3.read_text()
    cap = r"'(wall_cap_seconds|combined_rss_cap_bytes|output_cap_bytes)':([0-9.]+)"
    c3, c4 = dict(re.findall(cap, m3)), dict(re.findall(cap, mt))
    assert c4['wall_cap_seconds'] == '9000.0' and c3['wall_cap_seconds'] == '4500.0'
    assert c4['combined_rss_cap_bytes'] == c3['combined_rss_cap_bytes'] and c4['output_cap_bytes'] == c3['output_cap_bytes']
    assert "out=b/'OWNED_L4_WORM_BIRTHK_RUN_V001'" in mt and not RUN_DIR.exists()
    assert 'out.mkdir(exist_ok=False)' in mt and "for name in ['OMP_NUM_THREADS'" in mt
    assert "worker=Path(" + repr(str(WORKER)) + ")" in mt
    res['P5_worker_monitor'] = {'seed_literal_count_incl_docstring': 4, 'old_seed_absent': True,
                                'schedule_checks_retained': True, 'monitor_caps': c4, 'monitor_v003_caps': c3,
                                'pilot_output_directory': str(RUN_DIR), 'pilot_output_directory_absent': True,
                                'single_thread_env_retained': True,
                                'launch_command': [PY, '-I', '-B', str(MONITOR)]}
    res['files'] = {str(p): sha(p) for p in (RECIPE, WORKER, MONITOR, BIRTH, WORM)}
    with out_path.open('x') as f:
        json.dump(res, f, indent=1, default=repr)
        f.write('\n')
    print(json.dumps({'ok': True}))


if __name__ == '__main__':
    main()
