"""Synthetic tests for galaxy_m0_forward_c2v003 (no project stage is executed; no launch).
usage: python3 -I -B tests_c2v003.py WORK_DIR   (WORK_DIR must be absent)
Writes WORK_DIR/TEST_RESULTS.json."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import traceback
import types
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DRV = HERE / 'galaxy_m0_forward_c2v003.py'
V001 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/galaxy_m0_forward_c2v001.py')
V001_SHA = '75b0c08a44eac92caedd46564eaaefe08b88a6c536e95cb46f54a9d8da962f22'
V001_SPECS = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/specs')
KC = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calibration_prep_c2_0470/kmax_convergence')
WAVE1 = KC / 'specs/wave1'
TEMPLATES = KC / 'specs/templates'
PREREG = (KC / 'KMAX_MATRIX_PREREG_V001.json', 'd5acfc2fea1c99adf7709ab509eb95bf966c0b3d6db7398b091ec2bd305538be')
GEN = (KC / 'make_kmax_specs_c2v001.py', '6c74318e602e7589a5eb5e540c463e2e9101d5b80d508167818a933a9f3096c0')
MONITOR = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
           'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(path, name, expected=None):
    raw = Path(path).read_bytes()
    if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
        raise AssertionError('pin mismatch ' + str(path))
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


D = load(DRV, 'drv3')
D1 = load(V001, 'drv1', V001_SHA)
RESULTS = []


def test(fn):
    def run(work):
        try:
            detail = fn(work)
            RESULTS.append({'test': fn.__name__, 'pass': True, 'detail': detail})
        except Exception as exc:
            RESULTS.append({'test': fn.__name__, 'pass': False, 'error': '%s: %s' % (type(exc).__name__, exc),
                            'traceback': traceback.format_exc()})
    run.__name__ = fn.__name__
    return run


def jl(p):
    return json.loads(Path(p).read_text())


def refused(fn, *a):
    try:
        fn(*a)
    except D.Refusal as exc:
        return str(exc)
    raise AssertionError('not refused')


# ----------------------------------------------------------------------------------------- specs
@test
def t01_wave1_specs_accepted_unchanged(work):
    out = {}
    for c in ('C2', 'C3', 'C4', 'R'):
        p = WAVE1 / ('CALL_KMAX_%s_C2V001.json' % c)
        ns = D.normalize_spec(jl(p))
        ns1 = D1.normalize_spec(jl(p))
        assert ns == ns1, 'normalized spec differs from v001 for ' + c
        out[c] = {'sha256': sha(p), 'nodes': (ns['numerics']['composite_grid_spec'] or {}).get('total_axis_nodes', 72)}
    man = jl(WAVE1 / 'SPECS_MANIFEST.json')
    for c, v in man['specs'].items():
        assert sha(v['path']) == v['sha256'], 'wave1 spec bytes changed ' + c
    return out


@test
def t02_templates_sphere_cylinder_accepted(work):
    """Wave-2 S/Y templates (PENDING admits replaced by absolute toy paths/hex) normalize; kmax == grid edge."""
    out = {}
    for c in ('S2', 'Y2', 'S3', 'Y3', 'S4', 'Y4'):
        s = jl(TEMPLATES / ('CALL_KMAX_%s_C2V001.TEMPLATE.json' % c))
        s['admit'] = {'route_a': {'attempt_directory': '/x/a', 'checkpoint_directory': '/x/c', 'identity_sha256': '0' * 64, 'result_sha256': '1' * 64},
                      'reference': {'directory': '/x/r', 'start_sha256': '2' * 64, 'finish_sha256': '3' * 64},
                      'body': {'directory': '/x/b', 'finish_sha256': '4' * 64}}
        ns = D.normalize_spec(s)
        g = ns['numerics']['composite_grid_spec']
        edge = float(g['breaks_inverse_kpc'][-1]) if g else 2.0
        assert ns['numerics']['truncation']['kmax_inverse_kpc'] == edge
        out[c] = ns['numerics']['truncation']
    return out


@test
def t03_grid_acceptance_boundaries(work):
    base = jl(WAVE1 / 'CALL_KMAX_C3_C2V001.json')
    out = {}
    # undeclared 84-node grid (G3 with one inner order changed) -> refused
    s = json.loads(json.dumps(base))
    s['numerics']['composite_grid_spec']['panel_orders'] = [6] * 6 + [5, 7] + [6] * 6
    out['undeclared_84'] = refused(D.normalize_spec, s)
    # 98-node grid -> refused
    s = json.loads(json.dumps(base))
    s['numerics']['composite_grid_spec']['panel_orders'] = [7] + [6] * 12 + [7]
    s['numerics']['composite_grid_spec']['total_axis_nodes'] = 86
    out['undeclared_86'] = refused(D.normalize_spec, s)
    # <=80 nodes: arbitrary grid still accepted exactly as v001 (prep V007 then decides)
    s = json.loads(json.dumps(base))
    s['numerics']['composite_grid_spec'].update(breaks_inverse_kpc=[-3, -2, -1, -0.3, -0.1, -0.03, -0.01, 0, 0.01, 0.03, 0.1, 0.3, 1, 2, 3],
                                                 panel_orders=[4] + [6] * 12 + [4], total_axis_nodes=80)
    assert D.normalize_spec(s) == D1.normalize_spec(s)
    out['80_node_grid_accepted_as_v001'] = True
    # declared grids equal the prereg definitions
    pre = jl(PREREG[0])
    assert sha(PREREG[0]) == PREREG[1]
    for gid, (b, o, t) in D.DECLARED_LARGE_GRIDS.items():
        cg = pre['grids'][gid]['composite_grid_spec']
        assert cg['breaks_inverse_kpc'] == b and cg['panel_orders'] == o and cg['total_axis_nodes'] == t, gid
    out['declared_equal_prereg'] = sorted(D.DECLARED_LARGE_GRIDS)
    # cube with kmax still refused (no declared grid needs it)
    s = json.loads(json.dumps(base))
    s['numerics']['truncation'] = {'shape': 'cube', 'kmax_inverse_kpc': 3.0}
    out['cube_with_kmax'] = refused(D.normalize_spec, s)
    return out


@test
def t04_relative_paths_refused(work):
    base = jl(V001_SPECS / 'CALL_REPRO_PINNED_ADMIT_PREFIX_C2V001.json')
    out = {}
    s = json.loads(json.dumps(base))
    s['coefficients'] = {'path': 'rel/coefficients.npz', 'sha256': '0' * 64}
    out['coefficients'] = refused(D.normalize_spec, s)
    s = json.loads(json.dumps(base))
    s['admit']['body']['directory'] = 'rel/body'
    out['admit_body'] = refused(D.normalize_spec, s)
    s = json.loads(json.dumps(base))
    s['numerics']['brackets']['pinned_controls']['fs'][0]['path'] = 'rel/controls.json'
    out['pinned_controls'] = refused(D.normalize_spec, s)
    v001_specs = {'CALL_EXAMPLE_CANDIDATE_SPHERE_C2V001.json': 'b24333ab5da52d11c484ea3ae640443830094dc4a1110e0a1453001dad68dd39',
                  'CALL_REPRO_PINNED_ADMIT_PREFIX_C2V001.json': '30b9b927c7825aee4f71d2cc70018864188dd6fc54944b6b9e3a29d3d1f62f9b',
                  'CALL_REPRO_PINNED_FULL_C2V001.json': '9542a413f91db28a017f54e6a30d6c9174e610cfb6dc6d1003f89631622279fb',
                  'CALL_REPRO_RULE_FULL_C2V001.json': 'c92344bff03cf10a5eed18c612e36be5f6c2a742eb03d9a111e90ae3c8c732b6'}
    for name, h in v001_specs.items():
        p = V001_SPECS / name
        assert sha(p) == h, name
        assert D.normalize_spec(jl(p)) == D1.normalize_spec(jl(p)), p.name
    out['all_v001_specs_normalize_identically'] = True
    return out


# ----------------------------------------------------------------------------------------- seed + prep
def _prep_guard_block(prep_path):
    """The reviewed prep's own grid construction lines (from 'nk = fourier_points_per_axis' to the
    'grid_description=' line of the composite branch), executed from the file bytes."""
    lines = Path(prep_path).read_text().splitlines()
    i = next(k for k, l in enumerate(lines) if l.strip() == 'nk = fourier_points_per_axis')
    j = next(k for k, l in enumerate(lines) if "grid_description='Composite tensor Gauss cube" in l)
    import textwrap
    return textwrap.dedent('\n'.join(lines[i:j + 1]))


@test
def t05_seed_and_reviewed_prep_guard(work):
    """per_call_seed values; the reviewed V007/V008 grid guards executed from bytes on each call seed."""
    v7, v8 = D.AUX['prep'], D.AUX['prep_v008']
    assert sha(v7[0]) == v7[1] and sha(v8[0]) == v8[1]
    b7, b8 = _prep_guard_block(v7[0]), _prep_guard_block(v8[0])
    assert b7.replace('nk>80', 'nk>96') == b8, 'guard blocks differ beyond the budget'
    out = {}
    for c in ('C2', 'C3', 'C4', 'R'):
        ns = D.normalize_spec(jl(WAVE1 / ('CALL_KMAX_%s_C2V001.json' % c)))
        seed, changed, reusable = D.per_call_seed(ns)
        seed1, changed1, reusable1 = D1.per_call_seed(ns)
        assert changed == changed1 and reusable == reusable1
        assert {k: v for k, v in seed.items() if k != 'c2_changed_fields'} == seed1
        assert ('c2_changed_fields' in seed) == (not reusable)
        ni = seed['numerical_inputs']
        res = {}
        for tag, block in (('v007', b7), ('v008', b8)):
            env = {'np': np, 'json': json, 'fourier_points_per_axis': ni['fourier_points_per_axis'],
                   'kmax_inverse_kpc': ni['kmax_inverse_kpc'], 'kpc_m': ni['kpc_m'],
                   'composite_grid_spec': ni['composite_grid_spec']}
            try:
                exec(block, env)
                res[tag] = {'accepted': True, 'axis_len': len(env['axis']), 'axis_sha': hashlib.sha256(env['axis'].tobytes()).hexdigest()[:16]}
            except ValueError as exc:
                res[tag] = {'accepted': False, 'error': str(exc)}
        nk = ni['fourier_points_per_axis']
        assert res['v008']['accepted'] and res['v008']['axis_len'] == nk
        assert res['v007']['accepted'] == (nk <= 80)
        if nk <= 80:
            assert res['v007']['axis_sha'] == res['v008']['axis_sha']
        out[c] = dict(res, nodes=nk, base_seed_reused=reusable, changed=[x['field'] for x in changed])
    return out


@test
def t06_prep_selection_in_plan(work):
    """Simulated chain: >80 nodes -> LOCAL['prep'] := V008 and COEFFICIENT patch on V008; <=80 -> V001 request exactly."""
    out = {}
    for c in ('C2', 'C3', 'C4', 'R'):
        ns = D.normalize_spec(jl(WAVE1 / ('CALL_KMAX_%s_C2V001.json' % c)))
        recs = {}
        for tag, mod in (('v3', D), ('v1', D1)):
            ctx = mod.Ctx('simulate', ns, Path(work) / ('t06_%s_%s' % (c, tag)))
            info, final = mod.execute_chain(ctx)
            recs[tag] = (ctx.records, info)
        r3 = recs['v3'][0][0]
        r1 = recs['v1'][0][0]
        nk = recs['v3'][1]['route_a']['prep']['axis_nodes']
        patch = r3['module_patches'][0]
        if nk > 80:
            assert r3['stage_dict_items'] == {'LOCAL': {'prep': {'path': str(D.AUX['prep_v008'][0]), 'sha256': D.AUX['prep_v008'][1]}}}
            assert patch['path'] == str(D.AUX['prep_v008'][0]) and patch['sha256'] == D.AUX['prep_v008'][1]
            assert set(patch['set']) == {'COEFFICIENT', 'COEFFICIENT_SHA'}
        else:
            assert 'stage_dict_items' not in r3
            assert patch['path'] == str(D.AUX['prep'][0])
        # every stage request other than route A identical to v001 (after outdir normalization)
        # the only intended non-path difference: a non-reused seed now carries the c2_changed_fields
        # annotation, so its sha differs; the v003 seed minus that key must equal the v001 seed bytes' content.
        s3, s1 = recs['v3'][1]['seed'], recs['v1'][1]['seed']
        if not s3['base_seed_reused']:
            a3, a1 = jl(s3['path']), jl(s1['path'])
            assert a3.pop('c2_changed_fields') and a3 == a1, 'seed content differs beyond the annotation'
        else:
            assert s3['sha256'] == s1['sha256']
        n3 = json.loads(json.dumps(recs['v3'][0]).replace('t06_%s_v3' % c, 'X').replace(s3['sha256'], 'SEED_SHA'))
        n1 = json.loads(json.dumps(recs['v1'][0]).replace('t06_%s_v1' % c, 'X').replace(s1['sha256'], 'SEED_SHA'))
        def mask_manifest_sha(recs):
            for r in recs:
                av = r.get('argv') or []
                for i, x in enumerate(av[:-1]):
                    if x == '--column-manifest-sha256':
                        av[i + 1] = 'SHA_OF_OWN_MANIFEST'  # manifest bytes embed the (different) work-dir path
            return recs
        n3, n1 = mask_manifest_sha(n3), mask_manifest_sha(n1)
        for a, b in zip(n3, n1):
            a = {k: v for k, v in a.items() if k != 'stage_dict_items'}
            if a['name'] == 'route_a':
                a = dict(a, module_patches=[]); b = dict(b, module_patches=[])
            assert a == b, a['name']
        assert len(n3) == len(n1)
        out[c] = {'nodes': nk, 'prep': Path(recs['v3'][1]['route_a']['prep']['path']).name, 'stages_planned': len(n3),
                  'seed_sha_v003': s3['sha256'], 'seed_sha_v001': s1['sha256']}
    return out


# ----------------------------------------------------------------------------------------- shim
TOY_STAGE = '''
import importlib.util, json, sys
from pathlib import Path
LOCAL = {'a': (Path('/nonexistent/a.py'), '%s'), 'prep': (Path('/nonexistent/prep.py'), '%s'), 'z': (Path('/nonexistent/z.py'), '%s')}
def main():
    out = {'LOCAL': [[k, str(p), s] for k, (p, s) in LOCAL.items()]}
    spec = importlib.util.spec_from_file_location('toy_prep', LOCAL['prep'][0])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    out['COEFFICIENT'] = str(m.COEFFICIENT); out['COEFFICIENT_SHA'] = m.COEFFICIENT_SHA
    Path(sys.argv[1]).write_text(json.dumps(out))
''' % ('a' * 64, 'b' * 64, 'c' * 64)


@test
def t07_stage_dict_item_and_v008_patch(work):
    """Run the real _stage shim in a fresh -I -B process on a toy stage whose LOCAL['prep'] is replaced by the
    REAL prep V008 file and whose loader receives the COEFFICIENT patch (V008 top-level is inert)."""
    w = Path(work) / 't07'
    w.mkdir()
    toy = w / 'toy_stage.py'
    toy.write_text(TOY_STAGE)
    v8p, v8s = str(D.AUX['prep_v008'][0]), D.AUX['prep_v008'][1]

    def req(items, out_name, patch_sha=v8s):
        return {'script': str(toy), 'script_sha256': sha(toy), 'argv': [str(w / out_name)], 'stage_globals': {},
                'module_patches': [{'path': v8p, 'sha256': patch_sha, 'set': {'COEFFICIENT': {'__path__': '/toy/coefficients.npz'}, 'COEFFICIENT_SHA': 'd' * 64}}],
                'mask': None, 'stage_dict_items': items}

    def run(r, name):
        rp = w / (name + '.request.json')
        rp.write_text(json.dumps(r))
        return subprocess.run([PY, '-I', '-B', str(DRV), '_stage', str(rp)], capture_output=True, text=True, cwd=str(w),
                              env=D.single_thread_env())
    p = run(req({'LOCAL': {'prep': {'path': v8p, 'sha256': v8s}}}, 'ok.json'), 'ok')
    assert p.returncode == 0, p.stderr[-2000:]
    o = jl(w / 'ok.json')
    assert [x[0] for x in o['LOCAL']] == ['a', 'prep', 'z'], 'order changed'
    assert o['LOCAL'][1] == ['prep', v8p, v8s] and o['LOCAL'][0][2] == 'a' * 64 and o['LOCAL'][2][2] == 'c' * 64
    assert o['COEFFICIENT'] == '/toy/coefficients.npz' and o['COEFFICIENT_SHA'] == 'd' * 64
    bad_sha = run(req({'LOCAL': {'prep': {'path': v8p, 'sha256': 'e' * 64}}}, 'bad.json'), 'bad_sha')
    absent = run(req({'LOCAL': {'nope': {'path': v8p, 'sha256': v8s}}}, 'absent.json'), 'absent')
    noglob = run(req({'NOPE': {'prep': {'path': v8p, 'sha256': v8s}}}, 'noglob.json'), 'noglob')
    for name, pr in (('bad_sha', bad_sha), ('absent', absent), ('noglob', noglob)):
        assert pr.returncode != 0 and 'Stage dict override' in pr.stderr, name
    # real route-A worker LOCAL: hard-coded prep is V007 (the only entry the item replaces)
    rw = load(D.SCRIPTS['route_a'][0], 'rw', D.SCRIPTS['route_a'][1])
    assert rw.LOCAL['prep'] == (D.AUX['prep'][0], D.AUX['prep'][1])
    return {'replaced': o['LOCAL'][1], 'coefficient_patch_on_v008': True,
            'refusals': {k: v.stderr.strip().splitlines()[-1] for k, v in (('bad_sha', bad_sha), ('absent', absent), ('noglob', noglob))}}


# ----------------------------------------------------------------------------------------- mask
def toy_offset(dirpath, shape, kmax, masked=True, mismatch=False, seed=0):
    rng = np.random.default_rng(seed)
    br = np.array([-3, -2, -1, -0.3, 0, 0.3, 1, 2, 3], float)
    axis = np.concatenate([((lo + hi) / 2 + (hi - lo) * np.polynomial.legendre.leggauss(3)[0] / 2) for lo, hi in zip(br[:-1], br[1:])]) / D.KPC_M
    waves = np.array([(x, y, z) for x in axis for y in axis for z in axis])
    r = rng.normal(size=(len(waves), 10, 1)) + 1j * rng.normal(size=(len(waves), 10, 1))
    m = D.truncation_mask(waves, shape, kmax)
    unit = D.apply_mask(r, m) if masked else r
    off = D.apply_mask(2.5 * r, m) if masked else 2.5 * r
    Path(dirpath).mkdir(parents=True)
    np.savez(Path(dirpath) / 'unit_response.npz', wavevectors=waves, dk_weights=np.ones(len(waves)), weighted_responses=unit)
    w2 = waves.copy()
    if mismatch:
        w2[0, 0] *= -1
    np.savez(Path(dirpath) / 'offset_prepared.npz', wavevectors=w2, weighted_responses=off)
    return int(m.sum()), len(m)


@test
def t08_mask_fired_check(work):
    out = {}
    for shape in ('sphere', 'cylinder'):
        kmax = 2.0 / D.KPC_M
        d = Path(work) / ('t08_ok_' + shape)
        kept, total = toy_offset(d, shape, kmax)
        rec = D.mask_fired_check(d, shape, kmax)
        assert rec['kept_nodes'] == kept and rec['total_nodes'] == total and kept < total and not rec['vacuous']
        assert rec['files']['offset_prepared.npz']['outside_rows_nonzero'] == 0
        out[shape] = {'kept': kept, 'total': total}
        d = Path(work) / ('t08_unmasked_' + shape)
        toy_offset(d, shape, kmax, masked=False)
        try:
            D.mask_fired_check(d, shape, kmax)
            raise AssertionError('unmasked not refused')
        except D.StageFailed as exc:
            assert 'MASK_NOT_FIRED' in str(exc)
            out[shape]['unmasked'] = str(exc)
    d = Path(work) / 't08_mismatch'
    toy_offset(d, 'sphere', 2.0 / D.KPC_M, mismatch=True)
    try:
        D.mask_fired_check(d, 'sphere', 2.0 / D.KPC_M)
        raise AssertionError('wave mismatch not refused')
    except D.StageFailed as exc:
        out['mismatch'] = str(exc)
    d = Path(work) / 't08_missing'
    d.mkdir()
    try:
        D.mask_fired_check(d, 'sphere', 2.0 / D.KPC_M)
        raise AssertionError('missing not refused')
    except D.StageFailed as exc:
        out['missing'] = str(exc)
    # vacuous mask (kmax beyond every node) passes and is labelled
    d = Path(work) / 't08_vacuous'
    toy_offset(d, 'sphere', 10.0 / D.KPC_M)
    out['vacuous'] = D.mask_fired_check(d, 'sphere', 10.0 / D.KPC_M)['vacuous']
    assert out['vacuous'] is True
    return out


@test
def t09_mask_check_placement_in_chain(work):
    """Simulated chain with a sphere spec whose 'saved' offset dir holds toy packets: a fired mask is
    recorded in identity.truncation; an unfired mask stops the chain right after the offset stage."""
    s = jl(TEMPLATES / 'CALL_KMAX_S3_C2V001.TEMPLATE.json')
    s['admit'] = {}
    ns = D.normalize_spec(s)
    kmax = 3.0 / D.KPC_M
    good, bad = Path(work) / 't09_good_offset', Path(work) / 't09_bad_offset'
    toy_offset(good, 'sphere', kmax)
    toy_offset(bad, 'sphere', kmax, masked=False)
    ctx = D.Ctx('simulate', ns, Path(work) / 't09_good', saved_runs={'offset': good})
    info, final = D.execute_chain(ctx)
    mc = info['truncation']['mask_check']
    assert mc['status'] == 'MASK_FIRED_OUTSIDE_ROWS_EXACTLY_ZERO'
    names = [r['name'] for r in ctx.records]
    ctx2 = D.Ctx('simulate', ns, Path(work) / 't09_bad', saved_runs={'offset': bad})
    try:
        D.execute_chain(ctx2)
        raise AssertionError('unfired mask not refused')
    except D.StageFailed as exc:
        names2 = [r['name'] for r in ctx2.records]
        assert names2[-1] == 'offset', names2
        msg = str(exc)
    assert info['route_a']['prep']['axis_nodes'] == 84 and info['route_a']['prep']['path'].endswith('_v008.py')
    return {'kept': mc['kept_nodes'], 'total': mc['total_nodes'], 'planned_after_good': names[3:6],
            'stages_before_refusal': names2, 'refusal': msg, 'scope_note': info['truncation']['scope']}


# ----------------------------------------------------------------------------------------- annotations / trivial fixes
@test
def t10_bracket_source_and_bound(work):
    out = {}
    try:
        D.require_bracket_source({0: 1.0}, 2, 'rfs')
        raise AssertionError('missing column not refused')
    except D.StageFailed as exc:
        out['missing'] = str(exc)
    D.require_bracket_source({0: 1.0, 1: 2.0}, 2, 'rfs')
    # picard_bound_met through the real cmd_run with execute_chain replaced by a fake (no stage runs)
    m = load(DRV, 'drv3_fake')
    spec = jl(WAVE1 / 'CALL_KMAX_C2_C2V001.json')
    rows = [{'id': 'r%02d' % i, 'speed_km_s': 10.0 + i} for i in range(12)]
    for tag, chg in (('met', 0.004), ('not_met', 0.05), ('none', None)):
        def fake(ctx, chg=chg):
            rec = {'pass': 4, 'rows': rows, 'column_failures': [], 'rotation_positive': True}
            if chg is not None:
                rec['max_abs_change_km_s'] = chg
            ctx.passes.append(rec)
            return {'seed': {}}, rec
        m.execute_chain = fake
        sp = Path(work) / ('t10_%s_spec.json' % tag)
        sp.write_text(json.dumps(spec))
        od = Path(work) / ('t10_%s_out' % tag)
        code = m.cmd_run(str(sp), str(od))
        r = jl(od / 'result.json')
        out[tag] = {'exit': code, 'status': r['status'], 'picard_bound_met': r['picard_bound_met']}
    assert out['met']['picard_bound_met'] is True and out['not_met']['picard_bound_met'] is False and out['none']['picard_bound_met'] is None
    return out


@test
def t11_generator_preflight_and_specs_bytes(work):
    """The kit's own spec generator against v003: preflight P1 now true; regenerated wave1 CALL specs are
    byte-identical to the shipped ones (only the campaign driver pin changes)."""
    g = load(GEN[0], 'gen', GEN[1])
    pf = g.driver_preflight(str(DRV))
    assert pf['driver_mentions_prep_v008'] is True
    od = Path(work) / 't11_wave1'
    p = subprocess.run([PY, '-I', '-B', str(GEN[0]), 'wave1', '--prereg', str(PREREG[0]), '--outdir', str(od),
                        '--driver', str(DRV), '--driver-sha256', sha(DRV), '--monitor', MONITOR[0], '--monitor-sha256', MONITOR[1]],
                       capture_output=True, text=True, env=D.single_thread_env())
    assert p.returncode == 0, p.stderr[-2000:]
    for c in ('C2', 'C3', 'C4', 'R'):
        assert sha(od / ('CALL_KMAX_%s_C2V001.json' % c)) == sha(WAVE1 / ('CALL_KMAX_%s_C2V001.json' % c)), c
    a = jl(od / 'CAMPAIGN_KMAX_WAVE1_C2V001.json')
    b = jl(WAVE1 / 'CAMPAIGN_KMAX_WAVE1_C2V001.json')
    diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    assert diff == ['calls', 'driver'], diff
    assert [x['spec_sha256'] for x in a['calls']] == [x['spec_sha256'] for x in b['calls']]
    return {'preflight': pf['driver_mentions_prep_v008'], 'campaign_keys_differing': diff,
            'manifest_preflight': jl(od / 'SPECS_MANIFEST.json')['preflight']['driver_mentions_prep_v008']}


@test
def t12_repro_plan_identical_to_v001(work):
    out = {}
    for s in ('REPRO_PINNED_ADMIT_PREFIX', 'REPRO_PINNED_FULL', 'KMAX_C2'):
        c = jl(HERE / 'dryrun' / ('PLAN_COMPARE_%s_V001.json' % s))
        assert c['stage_plan_identical'] and c['dryrun_plan_txt_identical_after_prefix_normalization'] and c['final_rows_identical']
        assert sha(c['v003_report']) == c['v003_report_sha256'] and sha(c['v001_report']) == c['v001_report_sha256']
        r = jl(c['v003_report'])
        assert r['executed_stages'] == 0 and r['driver_sha256'] == sha(DRV), 'dry run not from current v003 bytes'
        out[s] = {'stages': c['n_stages_v003'], 'overrides': r['summary']['overrides_wording'], 'other_report_differences': c['other_report_differences']}
    return out


@test
def t13_kmax_dryruns_from_current_bytes(work):
    out = {}
    for c in ('C3', 'C4', 'R', 'C2'):
        r = jl(HERE / 'dryrun' / ('V003_KMAX_%s_V001' % c) / 'DRYRUN_REPORT.json')
        assert r['driver_sha256'] == sha(DRV) and r['executed_stages'] == 0
        assert r['call_spec_sha256'] == sha(WAVE1 / ('CALL_KMAX_%s_C2V001.json' % c))
        assert not r['summary']['pin_problems'] and not r['summary']['scipy_imports']
        ra = r['stages'][0]
        prep = r['identity']['route_a']['prep']
        out[c] = {'prep': Path(prep['path']).name, 'nodes': prep['axis_nodes'], 'stage_dict_items': bool(ra.get('stage_dict_items')),
                  'stages_planned': r['summary']['stages_planned'], 'verified_files': r['transitive_pins']['verified_files']}
        assert (prep['axis_nodes'] > 80) == out[c]['stage_dict_items']
    return out


@test
def t14_campaign_repin(work):
    """specs/CAMPAIGN_KMAX_WAVE1_C2V003.json = the shipped wave-1 campaign with ONLY the driver block re-pinned."""
    a = jl(HERE / 'specs' / 'CAMPAIGN_KMAX_WAVE1_C2V003.json')
    b = jl(WAVE1 / 'CAMPAIGN_KMAX_WAVE1_C2V001.json')
    assert sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k)) == ['driver']
    assert a['driver'] == {'path': str(DRV), 'sha256': sha(DRV)}
    assert a['monitor'] == {'path': MONITOR[0], 'sha256': MONITOR[1]} and sha(MONITOR[0]) == MONITOR[1]
    camp = load('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/galaxy_m0_forward_c2_0466/campaign_c2v001.py', 'camp',
                '71274ceb15e57786ee8f575fd74b48e848193467156f0adcebbe7ee415e44597')
    for call in a['calls']:
        camp._spec_bytes(call)
        assert sha(call['spec_path']) == call['spec_sha256']
    return {'calls': [Path(c['spec_path']).name for c in a['calls']], 'driver_sha256': a['driver']['sha256']}


def main(work):
    work = Path(work)
    work.mkdir(parents=True)
    for t in (t01_wave1_specs_accepted_unchanged, t02_templates_sphere_cylinder_accepted, t03_grid_acceptance_boundaries,
              t04_relative_paths_refused, t05_seed_and_reviewed_prep_guard, t06_prep_selection_in_plan,
              t07_stage_dict_item_and_v008_patch, t08_mask_fired_check, t09_mask_check_placement_in_chain,
              t10_bracket_source_and_bound, t11_generator_preflight_and_specs_bytes, t12_repro_plan_identical_to_v001,
              t13_kmax_dryruns_from_current_bytes, t14_campaign_repin):
        t(work)
    res = {'schema': 'UNT_GALAXY_M0_FORWARD_TESTS_C2V003', 'driver_sha256': sha(DRV), 'tests_sha256': sha(__file__),
           'passed': sum(r['pass'] for r in RESULTS), 'total': len(RESULTS), 'results': RESULTS,
           'scope': 'synthetic and simulate-mode only; no project stage executed'}
    with open(work / 'TEST_RESULTS.json', 'x') as f:
        json.dump(res, f, indent=1, default=str)
    for r in RESULTS:
        print('PASS' if r['pass'] else 'FAIL', r['test'], '' if r['pass'] else r['error'])
    print('%d/%d' % (res['passed'], res['total']))
    return 0 if res['passed'] == res['total'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
