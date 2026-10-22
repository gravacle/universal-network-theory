#!/usr/bin/env python3
"""test_stage0_successor_c2v002 -- synthetic tests of the STAGE0-only successor c2v002 (root V006 A142, r3a M-14).

Run:  python3 -I -B test_stage0_successor_c2v002.py --run-dir NEW_DIR [--module PATH]

c2v002 keeps every c2v001 test and adds the review D05 / D07 regressions (G*, H*), their MUST_FAIL forgeries
(F14-F18), absolute-path pins (N11, N12) and two controls run on the unadopted c2v001 module (C04, C05), which show
the two defects reproduce there.

Everything is synthetic. The slots file is a SYNTHETIC copy with a synthetic pin (the real slots V003 file is never
opened); so are the GL-node roster, route-B config, query manifest, rosters, DDO154 region, calibration record,
forward results, STAGE0 status records, terminal receipts and target rows. The three modules (v003g, c2v001, the
successor under test) are imported read-only (-B: no bytecode is written) and their ROOT_SLOTS_* /
REGISTERED_GL_NODES_* pins are patched in memory to the synthetic copies. The only program file opened is the v003g
module (bytes hashed and imported). Every file is written by exclusive create inside --run-dir, which must not
exist (the D07 tests create a root file, or a symlink to one, only AFTER the freeze, at a path that was empty);
the run ends by writing FILES_WRITTEN_test_stage0_successor_c2v002.json, the list of every file and symlink the run
created, with sha256 from bytes.

Expectations: MUST_PASS (the behaviour must hold), MUST_FAIL (an attack that must fail: the test passes when the
attack is refused or reads non-EVALUATED), CONTROL (a v003g or c2v001 fact the successor is built against).
"""
import argparse
import ast
import copy
import datetime
import hashlib
import importlib.util
import json
import math
import os
import platform
import sys
import traceback

V003G_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/'
              'prediction_freeze_c2v003g_cx3v001.py')
V003G_SHA256 = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
V001_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/stage0_successor_c2/'
             'prediction_freeze_c2v003g_stage0_c2v001.py')
V001_SHA256 = 'e015e617c7437afc1863ef8e30e82f040555bdf32ed0f6518f27ac7ccfb330fe'
SUCCESSOR_NAME = 'prediction_freeze_c2v003g_stage0_c2v002.py'
CAL_SCHEMA = 'CALIBRATION_RUN_RECORD_C2V003'

PRIMARY = 'BR_A_F10_PRIMARY'
ALT_EV = 'SYN_ALT_EVALUATED'
STAGE0 = 'STAGE0_GRID_OUTER'
EVAL = 'EVALUATED_BEFORE_FREEZE'
NOT_EVAL = 'NOT_EVALUATED_BEFORE_FREEZE'
REFUSED = 'EVALUATED_REFUSED'
RECORD_SCHEMA = 'STAGE0_STATUS_RECORD_C2V001'
RECEIPT_SCHEMA = 'STAGE0_TERMINAL_RECEIPT_C2V001'
STEP4 = '2026-11-02T10:00:00Z'
SEAL_SOURCE = 'SYNTHETIC seal entry (test fixture; not a V006 heading)'

IDS = ['Q%02d' % k for k in range(1, 44)]
RADII = [0.5, 0.9] + [1.5 + (29.0 - 1.5) * k / 32.0 for k in range(33)] + [30.0 + 2.0 * k for k in range(8)]
RAD_TEXT = ['%.3f' % r for r in RADII]
RAD = dict(zip(IDS, [float(t) for t in RAD_TEXT]))
OUTER = [q for q in IDS if RAD[q] >= 30.0]
GL4_INVALID = ['Q01', 'Q02']

COORDS = [
    {'name': 'a0', 'transform': 'log', 'lower': 0.5, 'upper': 2.0, 'role': 'free', 'trial_value': 1.0,
     'units': 'dimensionless', 'scope': 'shared', 'kind': 'other', 'reference_value': None, 'sensitivity': None},
    {'name': 'b1', 'transform': 'linear', 'lower': -1.0, 'upper': 1.0, 'role': 'free', 'trial_value': 0.0,
     'units': 'dimensionless', 'scope': 'shared', 'kind': 'other', 'reference_value': None, 'sensitivity': None},
    {'name': 'ddo_D', 'transform': 'linear', 'lower': 3.5, 'upper': 4.5, 'role': 'nuisance', 'trial_value': 4.04,
     'units': 'Mpc', 'scope': 'ddo154_nuisance', 'kind': 'distance', 'reference_value': 4.04, 'sensitivity': None},
    {'name': 'ngc_D', 'transform': 'linear', 'lower': 12.0, 'upper': 15.0, 'role': 'nuisance', 'trial_value': 13.8,
     'units': 'Mpc', 'scope': 'ngc3198_nuisance', 'kind': 'distance', 'reference_value': 13.8,
     'sensitivity': {'mode': 'box_ends'}},
    {'name': 'ngc_i', 'transform': 'linear', 'lower': 65.0, 'upper': 80.0, 'role': 'nuisance', 'trial_value': 72.0,
     'units': 'deg', 'scope': 'ngc3198_nuisance', 'kind': 'inclination', 'reference_value': None,
     'sensitivity': {'mode': 'box_ends'}},
]

EXPECTED_CHANGED_FUNCTIONS = ['_load_row_roster', '_root_rosters_for_alternatives', '_bind_alternatives',
                              '_validate_manifest_structure', 'write_freeze_manifest', '_alternative_score_scope',
                              'score_after_freeze']
EXPECTED_CHANGED_CONSTANTS = ['SCHEMA', 'MODULE_NAME', 'MANIFEST_KEYS']
MANIFEST_IDENTITY_KEYS = {'schema', 'module', 'created_utc', 'pins', 'manifest_sha256'}
SCORE_IDENTITY_KEYS = {'manifest_file_sha256_expected', 'manifest_file_sha256_actual', 'manifest_file_sha256_registered',
                       'manifest_sha256_self', 'registration_file_sha256'}
STAGE0_STATUS_DEPENDENT_SCORE_KEYS = {'status', 'scored', 'note', 'members', 'member_within_error_counts',
                                      'member_evaluation_status'}

RESULTS = []
WRITTEN = []   # every file / symlink this run created (absolute paths), for FILES_WRITTEN


# ----------------------------------------------------------------------------- helpers

def canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    with open(path, 'rb') as fh:
        return sha_bytes(fh.read())


def track(path):
    WRITTEN.append(os.path.abspath(path))


def wx(path, data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    with open(path, 'xb') as fh:
        fh.write(data)
    track(path)
    return os.path.realpath(path)


def json_bytes(obj):
    return (json.dumps(obj, sort_keys=True, indent=1) + '\n').encode('utf-8')


def wjson(path, obj):
    return wx(path, json_bytes(obj))


def late_json(path, obj):
    """The bytes a root file WILL hold and its pin, WITHOUT writing it (the D07 tests write it after the freeze)."""
    data = json_bytes(obj)
    return data, {'path': os.path.realpath(path), 'sha256': sha_bytes(data)}


def symlink(target, link):
    os.symlink(target, link)   # fails if link exists: exclusive create
    track(link)
    return os.path.abspath(link)


def pin(path):
    return {'path': os.path.realpath(path), 'sha256': sha_file(path)}


def rjson(path):
    with open(path, 'rb') as fh:
        return json.loads(fh.read().decode('utf-8'))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def diff_paths(a, b, path=()):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b), key=str):
            if k not in a or k not in b:
                out.append(path + (k,))
            else:
                out.extend(diff_paths(a[k], b[k], path + (k,)))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(diff_paths(x, y, path + (i,)))
        return out
    return [] if canon(a) == canon(b) else [path]


def run_test(tid, expectation, title, fn):
    try:
        passed, detail = fn()
    except Exception as exc:   # noqa: BLE001
        passed, detail = False, {'exception': '%s: %s' % (type(exc).__name__, exc), 'trace': traceback.format_exc()}
    RESULTS.append({'id': tid, 'expectation': expectation, 'title': title, 'pass': bool(passed), 'detail': detail})
    print('%-5s %-9s %-4s %s' % (tid, expectation, 'PASS' if passed else 'FAIL', title))


# ----------------------------------------------------------------------------- AST identity

def top_level(tree):
    funcs, assigns, other, order = {}, {}, [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            funcs[node.name] = ast.dump(node)
            order.append(('def', node.name))
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) for t in node.targets):
            name = ','.join(t.id for t in node.targets)
            assigns[name] = ast.dump(node)
            order.append(('assign', name))
        else:
            kind = type(node).__name__
            other.append((kind, ast.dump(node)))
            order.append(('other', kind))
    return funcs, assigns, other, order


def ast_identity(v_path, s_path):
    with open(v_path, 'rb') as fh:
        vt = ast.parse(fh.read().decode('utf-8'))
    with open(s_path, 'rb') as fh:
        st = ast.parse(fh.read().decode('utf-8'))
    vf, va, vo, vord = top_level(vt)
    sf, sa, so, sord = top_level(st)
    rows = []
    for name in vf:
        status = ('MISSING' if name not in sf else 'IDENTICAL' if vf[name] == sf[name] else 'CHANGED')
        rows.append({'kind': 'function', 'name': name, 'status': status,
                     'v003g_ast_sha256': sha_bytes(vf[name].encode()),
                     'successor_ast_sha256': sha_bytes(sf[name].encode()) if name in sf else None})
    for name in sf:
        if name not in vf:
            rows.append({'kind': 'function', 'name': name, 'status': 'NEW', 'v003g_ast_sha256': None,
                         'successor_ast_sha256': sha_bytes(sf[name].encode())})
    for name in va:
        status = ('MISSING' if name not in sa else 'IDENTICAL' if va[name] == sa[name] else 'CHANGED')
        rows.append({'kind': 'constant', 'name': name, 'status': status,
                     'v003g_ast_sha256': sha_bytes(va[name].encode()),
                     'successor_ast_sha256': sha_bytes(sa[name].encode()) if name in sa else None})
    for name in sa:
        if name not in va:
            rows.append({'kind': 'constant', 'name': name, 'status': 'NEW', 'v003g_ast_sha256': None,
                         'successor_ast_sha256': sha_bytes(sa[name].encode())})
    v_other = [k for k, _d in vo]
    s_other = [k for k, _d in so]
    other_rows = []
    for (vk, vd), (sk, sd) in zip(vo, so):
        other_rows.append({'kind': vk, 'status': 'IDENTICAL' if vd == sd else 'CHANGED'})
    # v003g top-level order must survive as a subsequence of the successor's
    it = iter(sord)
    order_kept = all(any(x == y for y in it) for x in vord)
    return {'rows': rows, 'other_statements': other_rows, 'v003g_other_kinds': v_other,
            'successor_other_kinds': s_other, 'v003g_order_kept_as_subsequence': order_kept}


# ----------------------------------------------------------------------------- fixture

def forward_factory(kind, invalid_thetas=()):
    invalid = set(canon(t) for t in invalid_thetas)

    def fwd(theta):
        if canon(theta) in invalid:
            return {'valid': False, 'reasons': ['SYNTHETIC_MEMBER_FAILURE (fixture)']}
        rows, speeds = [], {}
        for q in IDS:
            if q in GL4_INVALID:
                rows.append({'id': q, 'valid': False, 'speed_km_s': None, 'reason': 'QUERY_INSIDE_INNERMOST_NODE'})
                speeds[q] = None
                continue
            r = RAD[q]
            v = (150.0 * (1.0 - math.exp(-r / 6.0)) * theta['a0'] ** 0.2 + 4.0 * theta['b1']
                 + 0.3 * (theta['ngc_i'] - 72.0) - 1.5 * (theta['ngc_D'] - 13.8))
            if kind == 'stage0':
                v += 2.5 if r >= 30.0 else 0.4
            elif kind == 'alt':
                v *= 1.01
            rows.append({'id': q, 'valid': True, 'speed_km_s': v, 'reason': None})
            speeds[q] = v
        return {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'galaxy': 'NGC3198', 'status': 'COMPLETED',
                'scored': False, 'driver_sha256': 'a' * 64, 'call_spec_sha256': 'b' * 64,
                'route_a_outcome': {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                                    'ro1': {'rule': 'RO1', 'armed': True, 'fired': False, 'worker_sha256': 'c' * 64,
                                            'binding_sha256': 'd' * 64, 'events': []}},
                'uv_tail': {'schema': 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010', 'enabled': True,
                            'admissibility': 'production', 'pending_certificates': [], 'source_rule': 'continuum_v001',
                            'nodes_ext_context': None, 'config': {'normalized_sha256': 'e' * 64},
                            'stage_records': [{'finish_sha256': 'f' * 64, 'state_digest': '1' * 64,
                                               'production_admissible': True, 'test_only_admitted': False}]},
                'valid': True, 'rows': rows, 'speeds_km_s': speeds, 'invalid_rows': list(GL4_INVALID), 'reasons': []}
    return fwd


class Fixture(object):
    pass


def build_fixture(fdir, mods, succ):
    os.makedirs(fdir)
    fx = Fixture()
    qm = {'schema': 'SYNTHETIC_QUERY_MANIFEST_FIXTURE_C2V001', 'synthetic_fixture': True,
          'rows': [{'query_id': q, 'data_row_index': i + 1, 'Rad_text': RAD_TEXT[i], 'Rad_unit': 'kpc'}
                   for i, q in enumerate(IDS)]}
    fx.qm_path = wjson(os.path.join(fdir, 'synthetic_query_manifest.json'), qm)
    fx.qm_pin = pin(fx.qm_path)
    profile = wjson(os.path.join(fdir, 'synthetic_source_profile.json'),
                    {'schema': 'SYNTHETIC_SOURCE_PROFILE_FIXTURE', 'values': [1.0, 2.0, 3.0]})
    profile_pin = pin(profile)
    config = wjson(os.path.join(fdir, 'synthetic_route_b_config.json'),
                   {'schema': 'SYNTHETIC_ROUTE_B_CONFIG_FIXTURE',
                    'fields': {'radial.source_gauss_order': {'value': 4}, 'radial.n_columns': {'value': 100},
                               'source.profile': {'value': profile_pin}}})
    grid = wx(os.path.join(fdir, 'synthetic_stage0_grid.bin'),
              b'SYNTHETIC STAGE0 COEFFICIENT GRID FIXTURE (not the stage-0 pooled grid)\n')
    fx.grid_pin = pin(grid)
    declared = [
        {'name': PRIMARY, 'kind': 'state', 'description': 'synthetic primary (fixture)', 'status': EVAL},
        {'name': ALT_EV, 'kind': 'source', 'description': 'synthetic evaluated full-row alternative', 'status': EVAL},
        {'name': 'GL10_SOURCE_GAUSS_ORDER', 'kind': 'source', 'description': 'synthetic GL10 record',
         'status': NOT_EVAL},
        {'name': 'SYN_ALT_NOT_EVALUATED_A', 'kind': 'state', 'description': 'synthetic', 'status': NOT_EVAL},
        {'name': 'SYN_ALT_NOT_EVALUATED_B', 'kind': 'approximation', 'description': 'synthetic', 'status': NOT_EVAL},
        {'name': STAGE0, 'kind': 'approximation', 'description': 'synthetic STAGE0 record (fixture)',
         'status': NOT_EVAL, 'headline': False,
         'scoring_scope': {'zone': 'OUTER', 'radius_min_kpc': 30.0, 'radius_min_inclusive': True,
                           'query_ids': list(OUTER)},
         'coefficient_grid_pin': fx.grid_pin},
    ]
    slots = {'schema': 'SYNTHETIC_SLOTS_FIXTURE_C2V001', 'synthetic_fixture': True,
             'query_block': {'rows': [{'query_id': q, 'data_row_index': i + 1, 'Rad_text': RAD_TEXT[i],
                                       'radius_kpc': RAD[q],
                                       'primary_GL4': ({'valid': False, 'reason': 'QUERY_INSIDE_INNERMOST_NODE'}
                                                       if q in GL4_INVALID else {'valid': True, 'reason': None})}
                                      for i, q in enumerate(IDS)],
                             'invalid_primary_GL4': list(GL4_INVALID)},
             'alternatives': {'primary': PRIMARY, 'declared': declared},
             'projection_pins': {'route_b_config': pin(config)}}
    fx.slots_path = wjson(os.path.join(fdir, 'synthetic_slots.json'), slots)
    fx.slots_pin = pin(fx.slots_path)
    gl = {'schema': 'NGC_REGISTERED_ROUTE_B_GL_NODES_CX3V001', 'synthetic_fixture': True,
          'kpc_m': 3.085677581491367e19, 'sources': {'profile': profile_pin},
          'orders': {'4': {'source_gauss_order': 4, 'registered_n_columns': 100,
                           'radii_m': [1.0e19 * (k + 1) for k in range(100)]},
                     '10': {'source_gauss_order': 10, 'registered_n_columns': 250,
                            'radii_m': [4.0e18 * (k + 1) for k in range(250)]}}}
    fx.gl_path = wjson(os.path.join(fdir, 'synthetic_gl_nodes.json'), gl)
    for m in mods:   # synthetic slots copy with a synthetic pin (and synthetic GL nodes), patched in memory
        m.ROOT_SLOTS_PATH = fx.slots_path
        m.ROOT_SLOTS_SHA256 = sha_file(fx.slots_path)
        m.REGISTERED_GL_NODES_PATH = fx.gl_path
        m.REGISTERED_GL_NODES_SHA256 = sha_file(fx.gl_path)
    fx.alternatives = rjson(fx.slots_path)['alternatives']
    fx.roster_pins = {}
    for alt in fx.alternatives['declared']:
        roster = {'schema': 'ROOT_ROW_REGISTRATION_ROSTER_CX3V001', 'scope': 'SYNTHETIC_FIXTURE', 'alternative': alt,
                  'slots': fx.slots_pin, 'query_manifest': fx.qm_pin,
                  'query_mapping': [{'query_id': q, 'slots_query_id': q} for q in IDS], 'root_gates': [],
                  'outer_cut': {'mode': 'NONE'}}
        fx.roster_pins[alt['name']] = pin(wjson(os.path.join(fdir, 'synthetic_roster_%s.json' % alt['name']), roster))
    region_rows = [{'id': 'D%02d' % (k + 1), 'reference_radius_kpc': 0.5 * (k + 1),
                    'observed_speed_km_s': 30.0 + 2.0 * k, 'quoted_random_sigma_km_s': 2.0,
                    'conditional_random_acceptance_low_km_s': 25.0 + 2.0 * k,
                    'conditional_random_acceptance_high_km_s': 35.0 + 2.0 * k} for k in range(12)]
    fx.region_path = wjson(os.path.join(fdir, 'synthetic_ddo154_region.json'),
                           {'schema': 'SYNTHETIC_DDO154_REGION_FIXTURE', 'rows': region_rows,
                            'statistical_choice': 'synthetic', 'distance_summary': {'central_Mpc': 4.04},
                            'forward_coordinates': ['a0', 'b1', 'ddo_D']})
    region_sha = sha_file(fx.region_path)
    fx.spec = succ.make_freeze_coordinate_spec(coordinates=COORDS)
    assert fx.spec['ok'], fx.spec['reasons']
    S = succ._build_spec(COORDS, [])
    pts = []
    for i in range(10):
        u = [0.2 + 0.06 * i, 0.75 - 0.05 * i + 0.02 * (i % 3), 0.35 + 0.03 * i]
        pts.append({'log_index': 5 + 3 * i, 'u': u, 'theta_natural': succ._theta_engine_from_u(S, u),
                    'prediction': {'valid': True,
                                   'speeds_km_s': {r['id']: r['observed_speed_km_s'] for r in region_rows}}})
    hull = {'0': {'min': min(p['u'][0] for p in pts), 'max': max(p['u'][0] for p in pts)},
            '1': {'min': min(p['u'][1] for p in pts), 'max': max(p['u'][1] for p in pts)}}
    ex = {'status': 'COMPLETE', 'stage_reached': 'march', 'admitted_points': pts, 'hull_box': hull,
          'primary_anchor': {'log_index': 17}, 'flags': [], 'region_possibly_truncated': False,
          'truncation_causes': [], 'coverage': {'n_evaluated': 64, 'synthetic': True},
          'unidentified_directions': [{'index': 2, 'sensitivity': 0.3}]}
    ident = {'varying_names': ['a0', 'b1', 'ddo_D'],
             'right_vectors': [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
             'identified': [0, 1], 'near_null': [2], 'singular_values': [10.0, 5.0, 0.5],
             'scaled_jacobian': [[10.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 0.5]],
             'null_tolerance': 0.1, 'effective_null_tolerance': 0.1,
             'numerical_rank_floor': 3 * 2.220446049250313e-16}
    fx.run = {'ok': True, 'status': 'COMPLETE', 'stage_reached': 'exploration:march', 'flags': [],
              'region_possibly_truncated': False, 'truncation_causes': [],
              'spec': {'names': ['a0', 'b1', 'ddo_D'], 'roles': {'a0': 'free', 'b1': 'free', 'ddo_D': 'nuisance'},
                       'scopes': {'a0': 'shared', 'b1': 'shared', 'ddo_D': 'DDO154'}},
              'region': {'ok': True, 'path': fx.region_path, 'sha256': region_sha},
              'identifiability': ident, 'exploration': ex}
    body = {'schema': 'CALIBRATION_RUN_RECORD_C2V003', 'synthetic_fixture': True, 'status': 'COMPLETE',
            'stage_reached': 'exploration:march', 'ok': True, 'region_sha256': region_sha,
            'exploration_fingerprint': succ._fingerprint([(p['log_index'], p['u']) for p in pts], region_sha),
            'run': fx.run}
    body['record_sha256'] = sha_bytes(succ._canonical_bytes(body))
    fx.record_path = wx(os.path.join(fdir, 'synthetic_calibration_record.json'), succ._canonical_bytes(body))
    fx.target_rows = [{'id': q, 'velocity': 100.0 + 0.5 * k + (3.0 if RAD[q] >= 30.0 else 0.0), 'sigma': 6.0}
                      for k, q in enumerate(IDS)]
    return fx


def pipeline(m, fx, with_stage0):
    """select / evaluate / reference / sensitivity with module m (each module runs its own pipeline)."""
    p = {}
    p['sel'] = m.select_representative_points(exploration=fx.run, interior_count=2, spec=fx.spec)
    assert p['sel']['ok'], p['sel']['reasons']
    pts = p['sel']['points']

    def ev(kind, name, budget=100, invalid=(), roster=None):
        return m.evaluate_envelopes(forward_ngc=forward_factory(kind, invalid), points=pts, spec=fx.spec,
                                    query_ids=IDS, budget=budget, row_registration_roster=fx.roster_pins[roster or name])
    p['ev'] = ev
    p['prim'] = ev('primary', PRIMARY)
    assert p['prim']['ok'], p['prim']['reasons']
    p['alt'] = ev('alt', ALT_EV)
    assert p['alt']['ok'], p['alt']['reasons']
    p['ref'] = m.select_reference_member(selection=p['sel'], evaluation=p['prim'])
    assert p['ref']['ok'], p['ref']['reasons']
    p['sens'] = m.evaluate_sensitivity(forward_ngc=forward_factory('primary'), reference=p['ref'],
                                       selection=p['sel'], spec=fx.spec, query_ids=IDS,
                                       null_direction_rule={'mode': 'box_ends'}, budget=100,
                                       row_registration_roster=fx.roster_pins[PRIMARY])
    assert p['sens']['ok'], p['sens']['reasons']
    if with_stage0:
        p['s0'] = ev('stage0', STAGE0)
        assert p['s0']['ok'], p['s0']['reasons']
    p['members'] = [{'member_id': x['member_id'], 'log_index': x['log_index'], 'theta_ngc': x['theta_ngc']}
                    for x in p['prim']['members']]
    return p


class Ctx(object):
    pass


def freeze(ctx, m, p, sdir, name, alt_evals, stage0_record='OMIT', alternatives=None, allow_incomplete=False,
           extra_code_files=(), extra_input_files=()):
    kw = dict(out_path=os.path.join(sdir, name + '_manifest.json'),
              registration_path=os.path.join(sdir, name + '_registration.json'),
              parameter_region={'bounds_semantics': m.BOUNDS_SEMANTICS, 'fixture': 'synthetic'},
              observation_rule={'rule': 'SYNTHETIC_FIXTURE'}, spec=ctx.fx.spec, selection=p['sel'],
              alternatives=copy.deepcopy(alternatives if alternatives is not None else ctx.fx.alternatives),
              alternative_evaluations=alt_evals, reference=p['ref'], sensitivity=p['sens'], query_ids=IDS,
              query_manifest={'path': ctx.fx.qm_path, 'sha256': ctx.fx.qm_pin['sha256'], 'role': 'SYNTHETIC_FIXTURE'},
              code_files=[os.path.realpath(m.__file__)] + list(extra_code_files),
              input_files=[ctx.fx.qm_path, ctx.fx.region_path, ctx.fx.record_path] + list(extra_input_files), notes={},
              allow_incomplete=allow_incomplete, row_registration_rosters=dict(ctx.fx.roster_pins))
    if stage0_record != 'OMIT':
        kw['stage0_status_record'] = stage0_record
    try:
        return m.write_freeze_manifest(**kw)
    finally:
        for key in ('out_path', 'registration_path'):
            if os.path.lexists(kw[key]):
                track(kw[key])


def score(ctx, m, res, manifest_path=None, registration_path=None, expected=None):
    return m.score_after_freeze(freeze_manifest_path=manifest_path or res['path'],
                                registration_path=registration_path or res['registration_path'],
                                expected_manifest_file_sha256=expected or res['manifest_file_sha256'],
                                target_rows=copy.deepcopy(ctx.fx.target_rows),
                                row_registration_rosters=dict(ctx.fx.roster_pins))


def receipt_doc(ctx, member, status='FINISHED', written='2026-11-01T12:00:00Z', theta=None, li=None, grid_sha=None,
                alternative=STAGE0, schema=RECEIPT_SCHEMA):
    return {'schema': schema, 'alternative': alternative,
            'member_log_index': member['log_index'] if li is None else li,
            'theta_ngc': member['theta_ngc'] if theta is None else theta,
            'coefficient_grid_sha256': grid_sha or ctx.fx.grid_pin['sha256'],
            'terminal_status': status, 'written_utc': written}


def receipt(ctx, sdir, tag, member, status='FINISHED', written='2026-11-01T12:00:00Z', theta=None, li=None,
            grid_sha=None, alternative=STAGE0, entry_li=None, schema=RECEIPT_SCHEMA):
    doc = receipt_doc(ctx, member, status=status, written=written, theta=theta, li=li, grid_sha=grid_sha,
                      alternative=alternative, schema=schema)
    path = wjson(os.path.join(sdir, 'receipt_%s.json' % tag), doc)
    return {'member_log_index': doc['member_log_index'] if entry_li is None else entry_li, 'receipt': pin(path)}


def all_receipts(ctx, sdir, statuses=None, written=None):
    out = []
    for j, mem in enumerate(ctx.sp['members']):
        st = (statuses or {}).get(j, 'FINISHED')
        wt = (written or {}).get(j, '2026-11-01T12:00:%02dZ' % j)
        out.append(receipt(ctx, sdir, 'm%d' % j, mem, status=st, written=wt))
    return out


def record_doc(ctx, entries, phase='PHASE_2', sealed='SELF', step4=STEP4, drop=None, source=SEAL_SOURCE):
    sealed_sha = ctx.succ_sha if sealed == 'SELF' else sealed
    doc = {'schema': RECORD_SCHEMA, 'phase': phase, 'alternative': STAGE0,
           'sealed_successor': ({'module_sha256': sealed_sha, 'source': source} if sealed_sha else None),
           'step4_start_utc': step4, 'receipts': entries}
    if drop:
        del doc[drop]
    return doc


def status_record(ctx, sdir, entries, phase='PHASE_2', sealed='SELF', step4=STEP4, drop=None,
                  name='stage0_status_record.json', source=SEAL_SOURCE):
    doc = record_doc(ctx, entries, phase=phase, sealed=sealed, step4=step4, drop=drop, source=source)
    return pin(wjson(os.path.join(sdir, name), doc))


def sdir_of(ctx, name):
    d = os.path.join(ctx.run_dir, 'scenarios', name)
    os.makedirs(d)
    return d


def s_evals(ctx, stage0=True, s0=None):
    d = {PRIMARY: ctx.sp['prim'], ALT_EV: ctx.sp['alt']}
    if stage0:
        d[STAGE0] = s0 if s0 is not None else ctx.sp['s0']
    return d


def stage0_alt(doc):
    return [a for a in doc['alternatives']['declared'] if a['name'] == STAGE0][0]


def summary(res, doc=None):
    out = {'ok': res.get('ok'), 'reasons': res.get('reasons')[:4] if isinstance(res.get('reasons'), list) else None,
           'freeze_status': res.get('freeze_status')}
    if doc is not None:
        b = doc['stage0_status']
        out.update({'stage0_status': stage0_alt(doc)['status'], 'reading': b['reading'], 'reasons_m14': b['reasons'],
                    'member_defects': [x['defects'] for x in b['members']], 'receipt_refusals': b['receipt_refusals'],
                    'evaluation_refusals': b['evaluation_refusals'], 'diagnostics': b['diagnostics'],
                    'alternative_results': sorted(doc['alternative_results'])})
    return out


def frozen(res):
    return rjson(res['path']) if res.get('ok') else None


def expect_stage0(ctx, res, reading, reasons, verify=True, extra=None):
    """Common assertions: the freeze completed, STAGE0's reading/codes, status consistency, verifier ok."""
    doc = frozen(res)
    if doc is None:
        return False, summary(res)
    b = doc['stage0_status']
    ok = (b['reading'] == reading and b['reasons'] == reasons
          and stage0_alt(doc)['status'] == (EVAL if reading == EVAL else NOT_EVAL)
          and ((STAGE0 in doc['alternative_results']) == (reading == EVAL)))
    det = summary(res, doc)
    if verify:
        v = ctx.succ.verify_freeze_manifest(freeze_manifest_path=res['path'])
        det['verify_ok'] = v['ok']
        det['verify_reasons'] = v['reasons'][:3]
        ok = ok and v['ok']
    if extra is not None:
        e_ok, e_det = extra(doc)
        det['extra'] = e_det
        ok = ok and e_ok
    return ok, det


def forge_manifest(ctx, m, src_path, mutate, out_path):
    doc = rjson(src_path)
    mutate(doc)
    body = {k: v for k, v in doc.items() if k != 'manifest_sha256'}
    doc['manifest_sha256'] = sha_bytes(m._canonical_bytes(body))
    raw = m._canonical_bytes(doc)
    wx(out_path, raw)
    return out_path, sha_bytes(raw), doc['manifest_sha256'], len(raw)


def forge_registration(m, manifest_path, file_sha, self_sha, nbytes, out_path):
    reg = {'schema': m.REGISTRATION_SCHEMA, 'created_utc': '2026-11-02T11:00:00Z',
           'manifest_path': os.path.realpath(manifest_path), 'expected_manifest_file_sha256': file_sha,
           'manifest_sha256_self': self_sha, 'manifest_bytes': nbytes, 'note': 'FORGED registration (test fixture)'}
    reg['registration_sha256'] = sha_bytes(m._canonical_bytes(reg))
    wx(out_path, m._canonical_bytes(reg))
    return out_path


# ----------------------------------------------------------------------------- tests

def tests(ctx):
    v, s, fx = ctx.v, ctx.succ, ctx.fx

    # ---- AST identity
    def t_ast():
        rep = ast_identity(V003G_PATH, ctx.succ_path)
        ctx.ast = rep
        fn_changed = sorted(r['name'] for r in rep['rows'] if r['kind'] == 'function' and r['status'] == 'CHANGED')
        fn_missing = [r['name'] for r in rep['rows'] if r['status'] == 'MISSING']
        fn_new = sorted(r['name'] for r in rep['rows'] if r['kind'] == 'function' and r['status'] == 'NEW')
        c_changed = sorted(r['name'] for r in rep['rows'] if r['kind'] == 'constant' and r['status'] == 'CHANGED')
        c_new = sorted(r['name'] for r in rep['rows'] if r['kind'] == 'constant' and r['status'] == 'NEW')
        n_ident = sum(1 for r in rep['rows'] if r['kind'] == 'function' and r['status'] == 'IDENTICAL')
        other = rep['other_statements']
        ok = (fn_changed == sorted(EXPECTED_CHANGED_FUNCTIONS) and not fn_missing
              and all(n.startswith('_stage0_') for n in fn_new)
              and c_changed == sorted(EXPECTED_CHANGED_CONSTANTS) and all(n.startswith('STAGE0_') for n in c_new)
              and rep['v003g_other_kinds'] == rep['successor_other_kinds']
              and [o['status'] for o in other][0] == 'CHANGED'   # the module docstring
              and all(o['status'] == 'IDENTICAL' for o in other[1:])   # imports
              and rep['v003g_order_kept_as_subsequence'])
        return ok, {'functions_identical': n_ident, 'functions_changed': fn_changed, 'functions_new': fn_new,
                    'constants_changed': c_changed, 'constants_new': c_new, 'missing': fn_missing,
                    'other_statements': other, 'order_kept': rep['v003g_order_kept_as_subsequence']}
    run_test('T01', 'MUST_PASS', 'AST identity: every non-STAGE0 function and constant of v003g is AST-identical', t_ast)

    # ---- v003g controls
    def t_v_baseline():
        d = sdir_of(ctx, 'C01_v003g_baseline')
        res = freeze(ctx, v, ctx.vp, d, 'v003g', {PRIMARY: ctx.vp['prim'], ALT_EV: ctx.vp['alt']})
        ctx.v_base = res
        sc = score(ctx, v, res) if res['ok'] else None
        ctx.v_base_score = sc
        return bool(res['ok'] and sc and sc['ok']), {'freeze': summary(res), 'score_ok': sc and sc['ok']}
    run_test('C01', 'CONTROL', 'v003g freeze + score on the synthetic fixture without a STAGE0 evaluation (baseline)',
             t_v_baseline)

    def t_v_stage0_roster():
        r = ctx.vp['ev']('stage0', STAGE0)
        return (r['ok'] is False and any('ROOT_ROSTER_ALTERNATIVE_NOT_EVALUATED' in x for x in r['reasons']),
                {'ok': r['ok'], 'reasons': r['reasons'][:2]})
    run_test('C02', 'CONTROL', 'v003g evaluate_envelopes refuses a STAGE0 replay evaluation (slots status)',
             t_v_stage0_roster)

    def t_v_d9():
        d = sdir_of(ctx, 'C03_v003g_D9')
        res = freeze(ctx, v, ctx.vp, d, 'v003g', {PRIMARY: ctx.vp['prim'], ALT_EV: ctx.vp['alt'],
                                                  STAGE0: ctx.sp['s0']})
        return (res['ok'] is False and any('REFUSED (D9)' in x for x in res['reasons'])
                and not os.path.lexists(os.path.join(d, 'v003g_manifest.json')),
                {'ok': res['ok'], 'reasons': res['reasons'][:2]})
    run_test('C03', 'CONTROL', 'v003g D9 refuses the WHOLE freeze when a STAGE0 evaluation is supplied', t_v_d9)

    # ---- TEST (a)
    def t_a1():
        d = sdir_of(ctx, 'A1_not_finished_with_eval')
        rec = status_record(ctx, d, all_receipts(ctx, d, statuses={0: 'INVALID_RULE_C'}))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        ctx.a1 = res

        def extra(doc):
            sc = score(ctx, s, res)
            ctx.a1_score = sc
            rec5 = [a for a in sc['alternatives'] if a['name'] == STAGE0][0] if sc['ok'] else None
            e = (doc['freeze_status'] == 'FREEZE_COMPLETE'
                 and doc['stage0_status']['members'][0]['defects'] == ['STAGE0_RECEIPT_TERMINAL_STATUS_NOT_FINISHED']
                 and sc['ok'] and rec5['scored'] is False and rec5['status'] == NOT_EVAL
                 and sc['stage0_status']['reading'] == NOT_EVAL)
            return e, {'score_ok': sc['ok'], 'stage0_score_record': rec5 and {k: rec5[k] for k in ('status', 'scored')},
                       'score_stage0_reading': sc['stage0_status'] and sc['stage0_status']['reading']}
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=extra)
    run_test('A1', 'MUST_PASS', 'TEST (a): Phase-2 freeze with a non-FINISHED STAGE0 receipt (STAGE0 evaluation '
             'supplied) completes; STAGE0 NOT_EVALUATED (STAGE0_RECEIPT_NOT_FINISHED); verifies; scores', t_a1)

    def t_a2():
        d = sdir_of(ctx, 'A2_not_finished_no_eval')
        rec = status_record(ctx, d, all_receipts(ctx, d, statuses={2: 'INVALID_RULE_C'}))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx, stage0=False), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'])
    run_test('A2', 'MUST_PASS', 'TEST (a) variant: no STAGE0 evaluation supplied; freeze completes NOT_EVALUATED', t_a2)

    def t_a3():
        d = sdir_of(ctx, 'A3_not_finished_partial_eval')
        n = len(ctx.sp['members'])
        part = ctx.sp['ev']('stage0', STAGE0, budget=n - 1)
        rec = status_record(ctx, d, all_receipts(ctx, d, statuses={n - 1: 'RUNNING'}))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx, s0=part), stage0_record=rec, allow_incomplete=False)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'],
                             extra=lambda doc: (doc['freeze_status'] == 'FREEZE_COMPLETE' and part['status']
                                                == 'BUDGET_EXHAUSTED' and doc['incomplete_reasons'] == [],
                                                {'stage0_eval_status': part['status'],
                                                 'freeze_status': doc['freeze_status']}))
    run_test('A3', 'MUST_PASS', 'TEST (a) variant: partial (BUDGET_EXHAUSTED) STAGE0 evaluation, allow_incomplete=False:'
             ' freeze completes FREEZE_COMPLETE, STAGE0 adds no incomplete reason', t_a3)

    # ---- EVALUATED
    def t_e1():
        d = sdir_of(ctx, 'E1_all_finished')
        rec = status_record(ctx, d, all_receipts(ctx, d))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        ctx.e1 = res

        def extra(doc):
            sc = score(ctx, s, res)
            ctx.e1_score = sc
            r = [a for a in sc['alternatives'] if a['name'] == STAGE0][0]
            ok = (sc['ok'] and r['status'] == EVAL and r['scored'] is True and r['headline'] is False
                  and r['scoring_scope']['query_ids'] == OUTER and r['scoring_scope']['n_rows'] == 8
                  and all(mm['n_rows'] == 8 and [x['id'] for x in mm['rows']] == OUTER for mm in r['members'])
                  and len(r['members']) == len(ctx.sp['members'])
                  and doc['stage0_status']['rule_a_receipts_finished'] and doc['stage0_status']['rule_b_successor_sealed'])
            return ok, {'score_ok': sc['ok'], 'n_rows_per_member': sorted(set(mm['n_rows'] for mm in r['members'])),
                        'scored': r['scored'], 'headline': r['headline']}
        return expect_stage0(ctx, res, EVAL, [], extra=extra)
    run_test('E1', 'MUST_PASS', 'all STAGE0 receipts FINISHED + successor sealed: EVALUATED_BEFORE_FREEZE, scored on its '
             '8 OUTER rows only, headline false', t_e1)

    def t_e2():
        d = sdir_of(ctx, 'E2_tie_at_step4')
        rec = status_record(ctx, d, all_receipts(ctx, d, written={1: STEP4}))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, EVAL, [])
    run_test('E2', 'MUST_PASS', 'a receipt written at the step-4 start instant counts as before step 4', t_e2)

    def t_e3():
        d = sdir_of(ctx, 'E3_invalid_member_finished')
        s0_bad = ctx.sp['ev']('stage0', STAGE0, invalid=[ctx.sp['members'][1]['theta_ngc']])
        rec = status_record(ctx, d, all_receipts(ctx, d))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx, s0=s0_bad), stage0_record=rec)

        def extra(doc):
            ms = doc['alternative_results'][STAGE0]['members']
            sc = score(ctx, s, res)
            r = [a for a in sc['alternatives'] if a['name'] == STAGE0][0]
            return (ms[1]['member_valid'] is False and r['members'][1]['within_error_count'] == 0 and sc['ok'],
                    {'member_valid': [x['member_valid'] for x in ms],
                     'within_error_counts': [x['within_error_count'] for x in r['members']]})
        return expect_stage0(ctx, res, EVAL, [], extra=extra)
    run_test('E3', 'MUST_PASS', 'validity never changes the status: a FINISHED STAGE0 member that is valid:false leaves '
             'STAGE0 EVALUATED (that member scores 0)', t_e3)

    # ---- TEST (b)
    def t_b1():
        V = rjson(ctx.v_base['path'])
        S = rjson(ctx.a1['path'])
        alt_same = canon(V['alternatives']) == canon(S['alternatives'])
        qb_same = canon(V['query_ids']) == canon(S['query_ids']) and \
            canon(V['input_bindings']) == canon(S['input_bindings'])
        keys_diff = sorted(k for k in set(V) | set(S) if k not in MANIFEST_IDENTITY_KEYS and
                           (k not in V or k not in S or canon(V[k]) != canon(S[k])))
        vin = set((p['path'], p['sha256']) for p in V['pins']['input_files'])
        sin = set((p['path'], p['sha256']) for p in S['pins']['input_files'])
        vsc, ssc = ctx.v_base_score, ctx.a1_score
        score_diff = sorted(k for k in set(vsc) | set(ssc) if k not in SCORE_IDENTITY_KEYS and
                            (k not in vsc or k not in ssc or canon(vsc[k]) != canon(ssc[k])))
        ok = (alt_same and qb_same and keys_diff == ['stage0_status'] and vin <= sin
              and score_diff == ['stage0_status'] and canon(vsc['alternatives']) == canon(ssc['alternatives']))
        return ok, {'manifest_alternatives_byte_identical': alt_same, 'query_block_byte_identical': qb_same,
                    'manifest_keys_differing_beyond_identity': keys_diff,
                    'successor_extra_input_pins': len(sin - vin),
                    'score_keys_differing_beyond_identity': score_diff,
                    'score_alternatives_byte_identical': canon(vsc['alternatives']) == canon(ssc['alternatives'])}
    run_test('B1', 'MUST_PASS', 'TEST (b), NOT_EVALUATED: manifest query block and alternatives byte-identical to v003g; '
             'every other manifest/score field identical except identity hashes and the added stage0_status', t_b1)

    def t_b2():
        V = rjson(ctx.v_base['path'])
        S = rjson(ctx.e1['path'])
        alt_paths = diff_paths(V['alternatives'], S['alternatives'])
        idx = [i for i, a in enumerate(V['alternatives']['declared']) if a['name'] == STAGE0][0]
        qb_same = canon(V['query_ids']) == canon(S['query_ids']) and \
            canon(V['input_bindings']) == canon(S['input_bindings'])
        keys_diff = sorted(k for k in set(V) | set(S) if k not in MANIFEST_IDENTITY_KEYS and
                           (k not in V or k not in S or canon(V[k]) != canon(S[k])))
        altres_ok = (sorted(S['alternative_results']) == sorted(list(V['alternative_results']) + [STAGE0]) and
                     all(canon(V['alternative_results'][k]) == canon(S['alternative_results'][k])
                         for k in V['alternative_results']))
        vsc, ssc = ctx.v_base_score, ctx.e1_score
        score_diff = sorted(k for k in set(vsc) | set(ssc) if k not in SCORE_IDENTITY_KEYS and
                            (k not in vsc or k not in ssc or canon(vsc[k]) != canon(ssc[k])))
        sp = diff_paths(vsc['alternatives'], ssc['alternatives'])
        sidx = [i for i, a in enumerate(vsc['alternatives']) if a['name'] == STAGE0][0]
        score_alt_ok = all(p[0] == sidx and p[1] in STAGE0_STATUS_DEPENDENT_SCORE_KEYS for p in sp)
        ok = (alt_paths == [('declared', idx, 'status')] and qb_same
              and keys_diff == ['alternative_results', 'alternatives', 'stage0_status'] and altres_ok
              and score_diff == ['alternatives', 'stage0_status'] and score_alt_ok
              and canon(vsc['headline']) == canon(ssc['headline']))
        return ok, {'manifest_alternatives_diff_paths': [list(p) for p in alt_paths],
                    'query_block_byte_identical': qb_same, 'manifest_keys_differing_beyond_identity': keys_diff,
                    'alternative_results_only_gains_stage0': altres_ok, 'score_keys_differing': score_diff,
                    'score_stage0_record_keys_differing': sorted(set(str(p[1]) for p in sp)),
                    'headline_identical': canon(vsc['headline']) == canon(ssc['headline'])}
    run_test('B2', 'MUST_PASS', 'TEST (b), EVALUATED: alternatives differ from v003g only at STAGE0.status; query block '
             'identical; headline identical; score differs only in STAGE0 status-dependent fields', t_b2)

    # ---- NOT_EVALUATED codes
    def t_n(tag, title, build, reading, reasons, diag=None, extra_check=None):
        def f():
            d = sdir_of(ctx, tag)
            rec = build(d)
            res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)

            def extra(doc):
                b = doc['stage0_status']
                ok = diag is None or diag in b['diagnostics']
                if extra_check is not None:
                    ok = ok and extra_check(b)
                return ok, {'diagnostics': b['diagnostics'], 'post_score_exploratory': b['post_score_exploratory']}
            return expect_stage0(ctx, res, reading, reasons, extra=extra)
        run_test(tag.split('_')[0], 'MUST_PASS', title, f)

    t_n('N1_no_sealed_successor', 'sealed successor not named: NOT_EVALUATED (NO_SEALED_SUCCESSOR)',
        lambda d: status_record(ctx, d, all_receipts(ctx, d), sealed=None), NOT_EVAL, ['NO_SEALED_SUCCESSOR'],
        'STAGE0_SEALED_SUCCESSOR_NOT_NAMED')
    t_n('N2_sealed_is_other_module', 'sealed successor sha is another module (v003g): NOT_EVALUATED (NO_SEALED_SUCCESSOR)',
        lambda d: status_record(ctx, d, all_receipts(ctx, d), sealed=V003G_SHA256), NOT_EVAL,
        ['NO_SEALED_SUCCESSOR'], 'STAGE0_SEALED_SUCCESSOR_IS_NOT_THIS_MODULE')
    t_n('N3_both_fail', 'receipt not FINISHED and no sealed successor: both codes',
        lambda d: status_record(ctx, d, all_receipts(ctx, d, statuses={1: 'FAILED'}), sealed=None), NOT_EVAL,
        ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'])
    t_n('N4_after_step4', 'a FINISHED receipt written after the step-4 start: RECEIPTS_AFTER_STEP4, exploratory',
        lambda d: status_record(ctx, d, all_receipts(ctx, d, written={2: '2026-11-02T10:00:01Z'})), NOT_EVAL,
        ['RECEIPTS_AFTER_STEP4'], None, lambda b: b['post_score_exploratory'] is True)
    t_n('N5_phase1', 'Phase-1 record: NOT_EVALUATED (NOT_IN_PHASE_1), unchanged reading',
        lambda d: status_record(ctx, d, all_receipts(ctx, d), phase='PHASE_1'), NOT_EVAL, ['NOT_IN_PHASE_1'],
        None, lambda b: b['phase'] == 'PHASE_1' and all(m['receipt'] is None for m in b['members']))
    t_n('N6_no_record', 'no status record supplied: NOT_EVALUATED with both codes',
        lambda d: None, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'],
        'STAGE0_STATUS_RECORD_NOT_SUPPLIED')
    t_n('N7_record_malformed', 'malformed status record (no step-4 start): NOT_EVALUATED with both codes',
        lambda d: status_record(ctx, d, all_receipts(ctx, d), drop='step4_start_utc'), NOT_EVAL,
        ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'], 'STAGE0_STATUS_RECORD_MALFORMED')
    t_n('N8_record_custody', 'status record pin sha does not match its bytes: NOT_EVALUATED with both codes',
        lambda d: dict(status_record(ctx, d, all_receipts(ctx, d)), sha256='0' * 64), NOT_EVAL,
        ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'], 'STAGE0_STATUS_RECORD_CUSTODY_MISMATCH')

    def t_n9():
        d = sdir_of(ctx, 'N9_v003g_style_call')
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx, stage0=False))
        V = rjson(ctx.v_base['path'])
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'],
                             extra=lambda doc: (canon(doc['alternatives']) == canon(V['alternatives']),
                                                {'alternatives_identical_to_v003g':
                                                 canon(doc['alternatives']) == canon(V['alternatives'])}))
    run_test('N9', 'MUST_PASS', 'a v003g-style call (no stage0_status_record) still freezes; STAGE0 NOT_EVALUATED', t_n9)

    # ---- EVALUATED_REFUSED
    def t_r(tag, title, s0, code_prefix):
        def f():
            d = sdir_of(ctx, tag)
            rec = status_record(ctx, d, all_receipts(ctx, d))
            res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx, stage0=s0 is not None, s0=s0), stage0_record=rec)
            return expect_stage0(ctx, res, REFUSED, [], extra=lambda doc: (
                len(doc['stage0_status']['evaluation_refusals']) == 1 and
                doc['stage0_status']['evaluation_refusals'][0].startswith(code_prefix) and
                doc['freeze_status'] == 'FREEZE_COMPLETE',
                {'evaluation_refusals': doc['stage0_status']['evaluation_refusals']}))
        run_test(tag.split('_')[0], 'MUST_PASS', title, f)

    n = len(ctx.sp['members'])
    t_r('R1_no_eval', 'receipt rule holds, no STAGE0 evaluation supplied: EVALUATED_REFUSED, freeze completes', None,
        'STAGE0_EVALUATION_NOT_SUPPLIED')
    t_r('R2_partial_eval', 'receipt rule holds, STAGE0 evaluation BUDGET_EXHAUSTED: EVALUATED_REFUSED, FREEZE_COMPLETE',
        ctx.sp['ev']('stage0', STAGE0, budget=n - 1), 'STAGE0_EVALUATION_NOT_COMPLETE')
    t_r('R3_wrong_roster', 'receipt rule holds, STAGE0 evaluation run under the PRIMARY roster: EVALUATED_REFUSED',
        ctx.sp['ev']('stage0', STAGE0, roster=PRIMARY), 'STAGE0_EVALUATION_ROSTER_PIN_MISMATCH')
    bad = copy.deepcopy(ctx.sp['s0'])
    bad['members'][0]['speeds_km_s'][5] = None
    t_r('R4_malformed_eval', 'receipt rule holds, a STAGE0 evaluation member is malformed: EVALUATED_REFUSED, the '
        'freeze completes', bad, 'STAGE0_EVALUATION_STRUCTURE')

    def t_n10():
        d = sdir_of(ctx, 'N10_not_finished_bad_eval')
        rec = status_record(ctx, d, all_receipts(ctx, d, statuses={4: 'INVALID_RULE_C'}))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx, s0=bad), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['evaluation_refusals'] == [],
            {'evaluation_refusals': doc['stage0_status']['evaluation_refusals']}))
    run_test('N10', 'MUST_PASS', 'evaluation refusals are judged only when the receipt rule holds: a malformed STAGE0 '
             'evaluation with a non-FINISHED receipt reads NOT_EVALUATED and records no refusal', t_n10)

    def t_p1():
        d = sdir_of(ctx, 'P1_caller_flip')
        flipped = copy.deepcopy(fx.alternatives)
        for a in flipped['declared']:
            if a['name'] == STAGE0:
                a['status'] = EVAL
        rec = status_record(ctx, d, all_receipts(ctx, d, statuses={3: 'INVALID_RULE_C'}))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec, alternatives=flipped)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'])
    run_test('P1', 'MUST_PASS', 'a caller (producer) flip of STAGE0 to EVALUATED is ignored: the receipt rule decides',
             t_p1)

    # ---- MUST_FAIL attacks
    def t_f1():
        d = sdir_of(ctx, 'F1_forged_finished_custody')
        entries = all_receipts(ctx, d)
        mem = ctx.sp['members'][0]
        honest = receipt(ctx, d, 'm0_honest_invalid', mem, status='INVALID_RULE_C')
        forged = receipt(ctx, d, 'm0_forged_finished', mem, status='FINISHED')
        # the record pins the honest (non-FINISHED) receipt's sha256 but the path holds a FINISHED forgery
        entries[0] = {'member_log_index': mem['log_index'],
                      'receipt': {'path': forged['receipt']['path'], 'sha256': honest['receipt']['sha256']}}
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][0]['defects'] == ['STAGE0_RECEIPT_CUSTODY_MISMATCH']
            and doc['stage0_status']['members'][0]['custody_ok'] is False,
            {'member0': doc['stage0_status']['members'][0]}))
    run_test('F1', 'MUST_FAIL', 'forged FINISHED receipt, sha/custody mismatch: not accepted (STAGE0 NOT_EVALUATED)', t_f1)

    def t_f2():
        d = sdir_of(ctx, 'F2_forged_finished_identity')
        entries = all_receipts(ctx, d)
        m0, m1 = ctx.sp['members'][0], ctx.sp['members'][1]
        # custody-correct bytes, but the receipt is for another member's call (theta of member 1)
        entries[0] = receipt(ctx, d, 'm0_other_theta', m0, theta=m1['theta_ngc'])
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][0]['defects'] == ['STAGE0_RECEIPT_IDENTITY_MISMATCH'],
            {'member0_defects': doc['stage0_status']['members'][0]['defects']}))
    run_test('F2', 'MUST_FAIL', 'forged FINISHED receipt naming another member\'s theta: not accepted', t_f2)

    def t_f3():
        d = sdir_of(ctx, 'F3_forged_finished_grid')
        entries = all_receipts(ctx, d)
        entries[2] = receipt(ctx, d, 'm2_wrong_grid', ctx.sp['members'][2], grid_sha='f' * 64)
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][2]['defects'] == ['STAGE0_RECEIPT_IDENTITY_MISMATCH'],
            {'member2_defects': doc['stage0_status']['members'][2]['defects']}))
    run_test('F3', 'MUST_FAIL', 'FINISHED receipt for another coefficient grid: not accepted', t_f3)

    def flip_to_evaluated(src_doc_evaluated):
        def mutate(doc):
            for a in doc['alternatives']['declared']:
                if a['name'] == STAGE0:
                    a['status'] = EVAL
            doc['alternative_results'][STAGE0] = src_doc_evaluated['alternative_results'][STAGE0]
            b = doc['stage0_status']
            b['reading'] = EVAL
            b['reasons'] = []
            b['rule_a_receipts_finished'] = True
            for mm in b['members']:
                mm['finished'] = True
                mm['defects'] = []
        return mutate

    def t_f4():
        d = sdir_of(ctx, 'F4_forged_manifest_flip')
        E = rjson(ctx.e1['path'])
        path, fsha, ssha, nb = forge_manifest(ctx, s, ctx.a1['path'], flip_to_evaluated(E),
                                              os.path.join(d, 'forged_manifest.json'))
        vr = s.verify_freeze_manifest(freeze_manifest_path=path)
        reg = forge_registration(s, path, fsha, ssha, nb, os.path.join(d, 'forged_registration.json'))
        sc = s.score_after_freeze(freeze_manifest_path=path, registration_path=reg, expected_manifest_file_sha256=fsha,
                                  target_rows=copy.deepcopy(fx.target_rows),
                                  row_registration_rosters=dict(fx.roster_pins))
        ok = (vr['ok'] is False and any('STAGE0_STATUS_BLOCK_MISMATCH' in x for x in vr['reasons'])
              and sc['ok'] is False and sc['refused'] is True)
        return ok, {'verify_ok': vr['ok'], 'verify_reasons': vr['reasons'][:2], 'score_ok': sc['ok'],
                    'score_reasons': sc['reasons'][:3]}
    run_test('F4', 'MUST_FAIL', 'forged manifest: a NOT_EVALUATED freeze re-hashed to claim STAGE0 EVALUATED is refused '
             'by the verifier and by the scorer (with a matching forged registration)', t_f4)

    def t_f5():
        d = sdir_of(ctx, 'F5_non_member_substitution')
        entries = all_receipts(ctx, d)
        mem = ctx.sp['members'][3]
        # the receipt for member 3 is replaced by a FINISHED receipt for a non-member (an admitted, unselected point)
        selected = set(x['log_index'] for x in ctx.sp['members'])
        non_member = [p['log_index'] for p in fx.run['exploration']['admitted_points']
                      if p['log_index'] not in selected][0]
        entries[3] = receipt(ctx, d, 'non_member', mem, li=non_member)
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][3]['defects'] == ['STAGE0_RECEIPT_MISSING']
            and any('STAGE0_RECEIPT_NON_MEMBER' in x for x in doc['stage0_status']['receipt_refusals']),
            {'member3_defects': doc['stage0_status']['members'][3]['defects'],
             'receipt_refusals': doc['stage0_status']['receipt_refusals'], 'non_member_log_index': non_member}))
    run_test('F5', 'MUST_FAIL', 'STAGE0 receipt for a non-member substituted for a member\'s: not accepted '
             '(NOT_EVALUATED, STAGE0_RECEIPT_NOT_FINISHED)', t_f5)

    def t_f6():
        d = sdir_of(ctx, 'F6_non_member_addition')
        entries = all_receipts(ctx, d)
        selected = set(x['log_index'] for x in ctx.sp['members'])
        non_member = [p['log_index'] for p in fx.run['exploration']['admitted_points']
                      if p['log_index'] not in selected][0]
        entries.append(receipt(ctx, d, 'non_member_extra', ctx.sp['members'][0], li=non_member))
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, REFUSED, [], extra=lambda doc: (
            any('STAGE0_RECEIPT_NON_MEMBER' in x for x in doc['stage0_status']['receipt_refusals']),
            {'receipt_refusals': doc['stage0_status']['receipt_refusals']}))
    run_test('F6', 'MUST_FAIL', 'an extra STAGE0 receipt for a non-member next to all FINISHED member receipts: the '
             'successor refuses it (EVALUATED_REFUSED, never EVALUATED)', t_f6)

    def t_f7():
        d = sdir_of(ctx, 'F7_partial_receipt_set')
        entries = all_receipts(ctx, d)[:-1]   # every listed receipt FINISHED, one member has none
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        ctx.f7 = res
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][-1]['defects'] == ['STAGE0_RECEIPT_MISSING']
            and all(mm['finished'] for mm in doc['stage0_status']['members'][:-1]),
            {'defects': [mm['defects'] for mm in doc['stage0_status']['members']]}))
    run_test('F7', 'MUST_FAIL', 'partial receipt set (all listed FINISHED, one member missing) is not read as EVALUATED',
             t_f7)

    def t_f8():
        d = sdir_of(ctx, 'F8_partial_set_forged_manifest')
        E = rjson(ctx.e1['path'])
        path, _fsha, _ssha, _nb = forge_manifest(ctx, s, ctx.f7['path'], flip_to_evaluated(E),
                                                 os.path.join(d, 'forged_manifest.json'))
        vr = s.verify_freeze_manifest(freeze_manifest_path=path)
        return (vr['ok'] is False and any('STAGE0_STATUS_BLOCK_MISMATCH' in x for x in vr['reasons']),
                {'verify_ok': vr['ok'], 'verify_reasons': vr['reasons'][:2]})
    run_test('F8', 'MUST_FAIL', 'partial receipt set re-hashed into a manifest claiming EVALUATED: verifier refuses', t_f8)

    def t_f9():
        d = sdir_of(ctx, 'F9_duplicate_receipts')
        entries = all_receipts(ctx, d)
        entries.append(receipt(ctx, d, 'm1_second', ctx.sp['members'][1]))
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][1]['defects'] == ['STAGE0_RECEIPT_DUPLICATE'],
            {'member1_defects': doc['stage0_status']['members'][1]['defects']}))
    run_test('F9', 'MUST_FAIL', 'two FINISHED receipts for one member (more than one call): not accepted', t_f9)

    def t_f10():
        d = sdir_of(ctx, 'F10_forged_block_custody')
        # a manifest whose block keeps the EVALUATED reading but drops a receipt pin from input_files
        def mutate(doc):
            r0 = os.path.realpath(doc['stage0_status']['members'][0]['receipt']['path'])
            doc['pins']['input_files'] = [p for p in doc['pins']['input_files'] if p['path'] != r0]
        path, _f, _s, _n = forge_manifest(ctx, s, ctx.e1['path'], mutate, os.path.join(d, 'forged_manifest.json'))
        vr = s.verify_freeze_manifest(freeze_manifest_path=path)
        return (vr['ok'] is False and any('STAGE0_CUSTODY_FILE_NOT_PINNED' in x for x in vr['reasons']),
                {'verify_ok': vr['ok'], 'verify_reasons': vr['reasons'][:2]})
    run_test('F10', 'MUST_FAIL', 'an EVALUATED manifest whose STAGE0 receipt is not pinned in input_files is refused',
             t_f10)

    def t_f11():
        d = sdir_of(ctx, 'F11_refusals_without_receipt_rule')

        def mutate(doc):
            doc['stage0_status']['evaluation_refusals'] = ['STAGE0_EVALUATION_NOT_SUPPLIED']
        path, _f, _s, _n = forge_manifest(ctx, s, ctx.a1['path'], mutate, os.path.join(d, 'forged_manifest.json'))
        vr = s.verify_freeze_manifest(freeze_manifest_path=path)
        return (vr['ok'] is False and any('receipt rule does not hold' in x for x in vr['reasons']),
                {'verify_ok': vr['ok'], 'verify_reasons': vr['reasons'][:2]})
    run_test('F11', 'MUST_FAIL', 'a manifest recording STAGE0 evaluation refusals where the receipt rule does not hold '
             'is refused', t_f11)

    def t_f12():
        d = sdir_of(ctx, 'F12_receipt_of_other_member')
        entries = all_receipts(ctx, d)
        m0, m1 = ctx.sp['members'][0], ctx.sp['members'][1]
        # member 1's genuine FINISHED receipt listed a second time, as member 0's
        entries[0] = receipt(ctx, d, 'm1_listed_as_m0', m1, entry_li=m0['log_index'])
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][0]['defects'] == ['STAGE0_RECEIPT_IDENTITY_MISMATCH'],
            {'member0_defects': doc['stage0_status']['members'][0]['defects']}))
    run_test('F12', 'MUST_FAIL', 'another member\'s FINISHED receipt listed under a member: not accepted', t_f12)

    def t_f13():
        d = sdir_of(ctx, 'F13_headline_call_receipt')
        entries = all_receipts(ctx, d)
        entries[2] = receipt(ctx, d, 'm2_headline_call', ctx.sp['members'][2], alternative=PRIMARY)
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][2]['defects'] == ['STAGE0_RECEIPT_IDENTITY_MISMATCH'],
            {'member2_defects': doc['stage0_status']['members'][2]['defects']}))
    run_test('F13', 'MUST_FAIL', 'a FINISHED receipt of the PRIMARY (headline) call is never read as a STAGE0 receipt', t_f13)

    # ---- cross-module and score-time checks
    def t_x1():
        a = v.verify_freeze_manifest(freeze_manifest_path=ctx.e1['path'])
        b = s.verify_freeze_manifest(freeze_manifest_path=ctx.v_base['path'])
        return (a['ok'] is False and b['ok'] is False,
                {'v003g_on_successor': a['reasons'][:2], 'successor_on_v003g': b['reasons'][:2]})
    run_test('X1', 'MUST_PASS', 'no cross-use: v003g refuses a successor manifest and the successor refuses a v003g one',
             t_x1)

    def t_s1():
        a1, e1 = ctx.a1_score, ctx.e1_score
        ok = (a1['ok'] and e1['ok'] and canon(a1['headline']) == canon(e1['headline'])
              and canon(a1['members']) == canon(e1['members'])
              and e1['stage0_status'] == rjson(ctx.e1['path'])['stage0_status'])
        return ok, {'headline_identical': canon(a1['headline']) == canon(e1['headline']),
                    'primary_members_identical': canon(a1['members']) == canon(e1['members'])}
    run_test('S1', 'MUST_PASS', 'STAGE0 never enters the headline: headline and PRIMARY member scores are identical '
             'whether STAGE0 is EVALUATED or not; the score output carries the frozen stage0_status', t_s1)

    # ================================================================ c2v002: review D05 / D07 regressions
    def pinned_paths(doc):
        return [p['path'] for label in ('code_files', 'input_files') for p in doc['pins'][label]]

    def cal_copy(d, name):
        with open(fx.record_path, 'rb') as fh:
            return wx(os.path.join(d, name), fh.read())

    def vs(m, res):
        vr = m.verify_freeze_manifest(freeze_manifest_path=res['path'])
        sc = score(ctx, m, res)
        return vr, sc

    def brief(vr, sc):
        return {'verify_ok': vr['ok'], 'verify_reasons': vr['reasons'][:2], 'score_ok': sc['ok'],
                'score_reasons': sc['reasons'][:3]}

    # ---- D05: a custody-correct STAGE0 pin to a file that is not a STAGE0 record never refuses the freeze
    def t_g1():
        d = sdir_of(ctx, 'G1_record_pin_to_calibration_copy')
        cp = cal_copy(d, 'calibration_record_copy.json')
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=pin(cp))

        def extra(doc):
            b = doc['stage0_status']
            sc = score(ctx, s, res)
            ok = (b['diagnostics'] == ['STAGE0_STATUS_RECORD_MALFORMED'] and b['status_record_custody_ok'] is False
                  and cp not in pinned_paths(doc) and sc['ok']
                  and doc['input_bindings']['calibration_record']['path'] == fx.record_path)
            return ok, {'diagnostics': b['diagnostics'], 'status_record_custody_ok': b['status_record_custody_ok'],
                        'copy_pinned': cp in pinned_paths(doc), 'score_ok': sc['ok']}
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'], extra=extra)
    run_test('G1', 'MUST_PASS', 'D05: the status-record pin is custody-correct but names a copy of the calibration '
             'record: the freeze completes (STAGE0 NOT_EVALUATED, STAGE0_STATUS_RECORD_MALFORMED), the copy is not '
             'pinned, the manifest verifies and scores', t_g1)

    def t_receipt_not_stage0(tag, title, idx, make):
        def f():
            d = sdir_of(ctx, tag)
            entries = all_receipts(ctx, d)
            entries[idx] = make(d, ctx.sp['members'][idx])
            rec = status_record(ctx, d, entries)
            res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)

            def extra(doc):
                row = doc['stage0_status']['members'][idx]
                sc = score(ctx, s, res)
                ok = (row['defects'] == ['STAGE0_RECEIPT_MALFORMED'] and row['custody_ok'] is False
                      and os.path.realpath(row['receipt']['path']) not in pinned_paths(doc)
                      and doc['stage0_status']['status_record_custody_ok'] is True
                      and rec['path'] in pinned_paths(doc) and sc['ok'])
                return ok, {'row': row, 'receipt_pinned': os.path.realpath(row['receipt']['path']) in pinned_paths(doc),
                            'score_ok': sc['ok']}
            return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=extra)
        run_test(tag.split('_')[0], 'MUST_PASS', title, f)

    t_receipt_not_stage0(
        'G2_receipt_with_calibration_schema', 'D05: a member receipt is custody-correct but its schema is %s: the '
        'freeze completes (that member STAGE0_RECEIPT_MALFORMED, custody_ok false), the receipt is not pinned, the '
        'manifest verifies and scores' % CAL_SCHEMA, 1,
        lambda d, mem: receipt(ctx, d, 'm1_calibration_schema', mem, schema=CAL_SCHEMA))
    t_receipt_not_stage0(
        'G3_receipt_pin_to_calibration_copy', 'D05: a member receipt pin is custody-correct but names a copy of the '
        'calibration record: the freeze completes, the copy is not pinned, the manifest verifies and scores', 3,
        lambda d, mem: {'member_log_index': mem['log_index'],
                        'receipt': pin(cal_copy(d, 'calibration_record_copy_as_receipt.json'))})

    def t_g4():
        d = sdir_of(ctx, 'G4_record_pin_to_bound_calibration_record')
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=pin(fx.record_path))

        def extra(doc):
            b = doc['stage0_status']
            sc = score(ctx, s, res)
            n = pinned_paths(doc).count(fx.record_path)
            return (b['diagnostics'] == ['STAGE0_STATUS_RECORD_MALFORMED'] and b['status_record_custody_ok'] is False
                    and n == 1 and sc['ok'], {'diagnostics': b['diagnostics'], 'times_pinned': n, 'score_ok': sc['ok']})
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'], extra=extra)
    run_test('G4', 'MUST_PASS', 'D05: the status-record pin names the bound calibration record itself: the freeze '
             'completes, the record is pinned exactly once, the manifest verifies and scores', t_g4)

    def t_g5():
        d = sdir_of(ctx, 'G5_calibration_string_as_value')
        entries = all_receipts(ctx, d)
        entries[0] = receipt(ctx, d, 'm0_status_is_cal_string', ctx.sp['members'][0], status=CAL_SCHEMA)
        rec = status_record(ctx, d, entries, source='%s (a value here, not a schema)' % CAL_SCHEMA)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)

        def extra(doc):
            b = doc['stage0_status']
            row = b['members'][0]
            sc = score(ctx, s, res)
            ok = (b['status_record_custody_ok'] is True and rec['path'] in pinned_paths(doc)
                  and row['custody_ok'] is True and row['terminal_status'] == CAL_SCHEMA
                  and row['defects'] == ['STAGE0_RECEIPT_TERMINAL_STATUS_NOT_FINISHED']
                  and os.path.realpath(row['receipt']['path']) in pinned_paths(doc)
                  and doc['input_bindings']['calibration_record']['path'] == fx.record_path and sc['ok'])
            return ok, {'row0': row, 'score_ok': sc['ok']}
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=extra)
    run_test('G5', 'MUST_PASS', 'D05: schema-valid STAGE0 files that carry the calibration schema string as a value '
             'are pinned and do not enter the calibration-record census: the freeze completes, verifies and scores',
             t_g5)

    def t_g6():
        d = sdir_of(ctx, 'G6_aliases_and_code_files')
        entries = all_receipts(ctx, d)
        m0 = ctx.sp['members'][0]
        alias0 = symlink(entries[0]['receipt']['path'], os.path.join(d, 'receipt_m0_alias.json'))
        entries[0] = {'member_log_index': m0['log_index'],
                      'receipt': {'path': alias0, 'sha256': entries[0]['receipt']['sha256']}}
        rec = status_record(ctx, d, entries)
        rec_alias = symlink(rec['path'], os.path.join(d, 'stage0_status_record_alias.json'))
        m1_receipt = entries[1]['receipt']['path']
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx),
                     stage0_record={'path': rec_alias, 'sha256': rec['sha256']},
                     extra_code_files=[rec['path']], extra_input_files=[m1_receipt])
        ctx.g6 = {'res': res, 'rec_alias': rec_alias, 'alias0': alias0, 'rec_real': rec['path']}

        def extra(doc):
            paths = pinned_paths(doc)
            b = doc['stage0_status']
            sc = score(ctx, s, res)
            ok = (len(paths) == len(set(paths)) and paths.count(rec['path']) == 1
                  and rec['path'] in [p['path'] for p in doc['pins']['code_files']]
                  and paths.count(os.path.realpath(m1_receipt)) == 1 and os.path.realpath(alias0) in paths
                  and b['status_record']['path'] == os.path.normpath(rec_alias)
                  and b['members'][0]['receipt']['path'] == os.path.normpath(alias0) and sc['ok'])
            return ok, {'duplicate_pin_paths': len(paths) - len(set(paths)),
                        'record_pinned_in_code_files_once': paths.count(rec['path']),
                        'status_record_pin': b['status_record'], 'score_ok': sc['ok']}
        return expect_stage0(ctx, res, EVAL, [], extra=extra)
    run_test('G6', 'MUST_PASS', 'STAGE0 files reached through symlink aliases, the status record also listed in '
             'code_files and a receipt also listed in input_files: no duplicate pin path; EVALUATED; verifies; scores',
             t_g6)

    def t_n11():
        d = sdir_of(ctx, 'N11_record_pin_relative')
        rec = status_record(ctx, d, all_receipts(ctx, d))
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx),
                     stage0_record={'path': os.path.relpath(rec['path']), 'sha256': rec['sha256']})
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR'],
                             extra=lambda doc: (doc['stage0_status']['diagnostics'] ==
                                                ['STAGE0_STATUS_RECORD_PIN_MALFORMED']
                                                and doc['stage0_status']['status_record'] is None,
                                                {'diagnostics': doc['stage0_status']['diagnostics']}))
    run_test('N11', 'MUST_PASS', 'a status-record pin with a relative path: NOT_EVALUATED with both codes '
             '(STAGE0_STATUS_RECORD_PIN_MALFORMED); the freeze completes and verifies', t_n11)

    def t_n12():
        d = sdir_of(ctx, 'N12_receipt_entry_relative')
        entries = all_receipts(ctx, d)
        e = entries[1]
        entries[1] = {'member_log_index': e['member_log_index'],
                      'receipt': {'path': os.path.relpath(e['receipt']['path']), 'sha256': e['receipt']['sha256']}}
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'succ', s_evals(ctx), stage0_record=rec)
        return expect_stage0(ctx, res, NOT_EVAL, ['STAGE0_RECEIPT_NOT_FINISHED'], extra=lambda doc: (
            doc['stage0_status']['members'][1]['defects'] == ['STAGE0_RECEIPT_MISSING']
            and doc['stage0_status']['receipt_refusals'] == ['STAGE0_RECEIPT_ENTRY_MALFORMED: receipts[1]'],
            {'member1_defects': doc['stage0_status']['members'][1]['defects'],
             'receipt_refusals': doc['stage0_status']['receipt_refusals']}))
    run_test('N12', 'MUST_PASS', 'a receipt entry with a relative path is refused as malformed; that member has no '
             'receipt: NOT_EVALUATED (STAGE0_RECEIPT_NOT_FINISHED)', t_n12)

    # ---- D07: a STAGE0 file that was not custody-verified at freeze time can never void a registered freeze
    def late_receipt_scenario(m, tag, sealed):
        d = sdir_of(ctx, tag)
        entries = all_receipts(ctx, d)
        mem = ctx.sp['members'][2]
        late_path = os.path.join(d, 'receipt_m2_late.json')
        data, lpin = late_json(late_path, receipt_doc(ctx, mem))
        entries[2] = {'member_log_index': mem['log_index'], 'receipt': lpin}
        rec = status_record(ctx, d, entries, sealed=sealed)
        res = freeze(ctx, m, ctx.sp, d, 'freeze', s_evals(ctx), stage0_record=rec)
        return res, rec, late_path, data, lpin

    def t_h1():
        res, rec, late_path, data, lpin = late_receipt_scenario(s, 'H1_receipt_absent_at_freeze', 'SELF')
        ctx.h1, ctx.h1_late_path = res, late_path
        doc0 = frozen(res)
        if doc0 is None:
            return False, summary(res)
        b = doc0['stage0_status']
        row = b['members'][2]
        v0, sc0 = vs(s, res)
        wx(late_path, data)   # the root-pinned bytes appear at that path AFTER the freeze
        v1, sc1 = vs(s, res)
        now = s._stage0_block(s._stage0_receipt_verdict(rec, s._stage0_members_of(ctx.sp['members'])), [])['reading']
        ok = (b['reading'] == NOT_EVAL and b['reasons'] == ['STAGE0_RECEIPT_NOT_FINISHED']
              and row['defects'] == ['STAGE0_RECEIPT_CUSTODY_MISMATCH'] and row['custody_ok'] is False
              and os.path.realpath(late_path) not in pinned_paths(doc0)
              and v0['ok'] and sc0['ok'] and v1['ok'] and sc1['ok']
              and canon(sc1['stage0_status']) == canon(b) and sha_file(late_path) == lpin['sha256'] and now == EVAL)
        return ok, {'frozen_reading': b['reading'], 'row2': row, 'before': brief(v0, sc0), 'after': brief(v1, sc1),
                    'late_bytes_match_root_pin': sha_file(late_path) == lpin['sha256'],
                    'rule_read_from_current_bytes_now': now}
    run_test('H1', 'MUST_PASS', 'D07: a member receipt is absent at freeze (the record pins the sha256 of the bytes '
             'root writes later): the freeze completes NOT_EVALUATED; after the root-pinned bytes appear at that path, '
             'verify and score still succeed and the frozen stage0_status stands (re-read now, the rule would hold)',
             t_h1)

    def t_h2():
        d = sdir_of(ctx, 'H2_record_absent_at_freeze')
        entries = all_receipts(ctx, d)
        late_path = os.path.join(d, 'stage0_status_record_late.json')
        data, rpin = late_json(late_path, record_doc(ctx, entries))
        res = freeze(ctx, s, ctx.sp, d, 'freeze', s_evals(ctx), stage0_record=rpin)
        ctx.h2 = res
        doc0 = frozen(res)
        if doc0 is None:
            return False, summary(res)
        b = doc0['stage0_status']
        v0, sc0 = vs(s, res)
        wx(late_path, data)
        v1, sc1 = vs(s, res)
        fresh = freeze(ctx, s, ctx.sp, d, 'fresh_after_record_appears', s_evals(ctx), stage0_record=rpin)
        fdoc = frozen(fresh)
        ok = (b['reading'] == NOT_EVAL and b['reasons'] == ['STAGE0_RECEIPT_NOT_FINISHED', 'NO_SEALED_SUCCESSOR']
              and b['diagnostics'] == ['STAGE0_STATUS_RECORD_CUSTODY_MISMATCH'] and b['status_record_custody_ok'] is False
              and all(r['receipt'] is None for r in b['members'])
              and os.path.realpath(late_path) not in pinned_paths(doc0)
              and v0['ok'] and sc0['ok'] and v1['ok'] and sc1['ok'] and canon(sc1['stage0_status']) == canon(b)
              and fdoc is not None and fdoc['stage0_status']['reading'] == EVAL)
        return ok, {'frozen_diagnostics': b['diagnostics'], 'before': brief(v0, sc0), 'after': brief(v1, sc1),
                    'fresh_freeze_reading_after_record_appears': fdoc and fdoc['stage0_status']['reading']}
    run_test('H2', 'MUST_PASS', 'D07: the status record is absent at freeze: the freeze completes NOT_EVALUATED; after '
             'the root-pinned record appears (one that satisfies the rule: a fresh freeze now reads EVALUATED), the '
             'registered freeze still verifies and scores NOT_EVALUATED', t_h2)

    def t_h3():
        d = sdir_of(ctx, 'H3_receipt_symlink_appears')
        entries = all_receipts(ctx, d)
        mem = ctx.sp['members'][3]
        link_path = os.path.join(d, 'receipt_m3_link.json')
        data, lpin = late_json(link_path, receipt_doc(ctx, mem))
        entries[3] = {'member_log_index': mem['log_index'], 'receipt': lpin}
        rec = status_record(ctx, d, entries)
        res = freeze(ctx, s, ctx.sp, d, 'freeze', s_evals(ctx), stage0_record=rec)
        doc0 = frozen(res)
        if doc0 is None:
            return False, summary(res)
        b = doc0['stage0_status']
        v0, sc0 = vs(s, res)
        target = wx(os.path.join(d, 'receipt_m3_target.json'), data)
        symlink(target, link_path)   # the path now resolves to another file holding the root-pinned bytes
        v1, sc1 = vs(s, res)
        ok = (b['reading'] == NOT_EVAL and b['members'][3]['defects'] == ['STAGE0_RECEIPT_CUSTODY_MISMATCH']
              and os.path.realpath(link_path) == target and v0['ok'] and sc0['ok'] and v1['ok'] and sc1['ok']
              and canon(sc1['stage0_status']) == canon(b))
        return ok, {'row3': b['members'][3], 'link_resolves_to': os.path.realpath(link_path),
                    'before': brief(v0, sc0), 'after': brief(v1, sc1)}
    run_test('H3', 'MUST_PASS', 'D07: a receipt path that is empty at freeze later becomes a symlink to the '
             'root-pinned bytes: verify and score still succeed (pins are normalised lexically, never by realpath '
             'of an unread path)', t_h3)

    def t_h4():
        g6, h1 = getattr(ctx, 'g6', None), getattr(ctx, 'h1', None)
        if not (isinstance(g6, dict) and g6['res'].get('ok') and isinstance(h1, dict) and h1.get('ok')):
            return False, {'source_freezes': 'missing'}
        # root-named STAGE0 paths that are not themselves pinned copies: two symlink aliases and the late receipt
        named = set(os.path.normpath(p) for p in (g6['rec_alias'], g6['alias0'], ctx.h1_late_path))
        touched = []
        orig_read, orig_real = s._read_regular, os.path.realpath

        def rr(path, require_nonempty):
            touched.append(('read', path))
            return orig_read(path, require_nonempty)

        def rp(path, *a, **k):
            touched.append(('realpath', path))
            return orig_real(path, *a, **k)
        s._read_regular, os.path.realpath = rr, rp
        try:
            out = [vs(s, g6['res']), vs(s, h1)]
        finally:
            s._read_regular, os.path.realpath = orig_read, orig_real
        hit = sorted(set('%s %s' % (k, p) for k, p in touched if isinstance(p, str) and os.path.normpath(p) in named))
        read_real = ('read', g6['rec_real']) in touched
        ok = all(v['ok'] and sc['ok'] for v, sc in out) and not hit and read_real
        return ok, {'root_named_paths_touched': hit, 'pinned_record_copy_read': read_real,
                    'n_filesystem_calls_recorded': len(touched),
                    'results': [brief(v, sc) for v, sc in out]}
    run_test('H4', 'MUST_PASS', 'D07: verify and score (G6 and H1 manifests, instrumented) make no read and no '
             'realpath call on any path a root STAGE0 record names; custody_ok files are read from their pinned '
             'copies', t_h4)

    # ---- MUST_FAIL: the carried (unread) STAGE0 defects cannot be forged
    def forged_verify(tag, src, mutate):
        d = sdir_of(ctx, tag)
        path, _f, _s, _n = forge_manifest(ctx, s, src['path'], mutate, os.path.join(d, 'forged_manifest.json'))
        return s.verify_freeze_manifest(freeze_manifest_path=path)

    def t_forged(tag, title, src_attr, mutate, expect='STAGE0_STATUS_BLOCK_MISMATCH'):
        def f():
            src = getattr(ctx, src_attr, None)
            if not (isinstance(src, dict) and src.get('ok')):
                return False, {'source_freeze': 'missing'}
            vr = forged_verify(tag, src, mutate)
            return (vr['ok'] is False and any(expect in x for x in vr['reasons']),
                    {'verify_ok': vr['ok'], 'verify_reasons': vr['reasons'][:2]})
        run_test(tag.split('_')[0], 'MUST_FAIL', title, f)

    def set_row2(pin_late=False, **kw):
        def mutate(doc):
            doc['stage0_status']['members'][2].update(kw)
            if pin_late:
                late_real = os.path.realpath(ctx.h1_late_path)
                doc['pins']['input_files'].append({'path': late_real, 'sha256': sha_file(late_real),
                                                   'bytes': os.path.getsize(late_real)})
        return mutate

    t_forged('F14_carried_row_custody_flip', 'a re-hashed manifest that marks the carried (unread) receipt row '
             'custody_ok and pins the late bytes is refused by the verifier (the recomputed row reads FINISHED, not '
             'the frozen defect)', 'h1', set_row2(pin_late=True, custody_ok=True))
    t_forged('F19_carried_row_custody_flip_unpinned', 'a re-hashed manifest that marks the carried receipt row '
             'custody_ok without pinning it is refused (STAGE0_CUSTODY_FILE_NOT_PINNED)', 'h1',
             set_row2(custody_ok=True), expect='STAGE0_CUSTODY_FILE_NOT_PINNED')
    t_forged('F15_carried_row_other_code', 'a re-hashed manifest that gives the carried receipt row a code a read '
             'cannot produce (STAGE0_RECEIPT_MISSING) is refused', 'h1', set_row2(defects=['STAGE0_RECEIPT_MISSING']))

    def other_sha(doc):
        r = doc['stage0_status']['members'][2]['receipt']
        doc['stage0_status']['members'][2]['receipt'] = {'path': r['path'], 'sha256': 'f' * 64}
    t_forged('F16_carried_row_other_pin', 'a re-hashed manifest that changes the carried receipt row\'s pin is '
             'refused', 'h1', other_sha)

    def record_code(doc):
        doc['stage0_status']['diagnostics'] = ['STAGE0_STATUS_RECORD_NOT_SUPPLIED']
    t_forged('F17_carried_record_other_code', 'a re-hashed manifest that gives the carried (unread) status record a '
             'code its pin cannot produce (NOT_SUPPLIED with a pin) is refused', 'h2', record_code)

    def t_f18():
        src = getattr(ctx, 'h1', None)
        if not (isinstance(src, dict) and src.get('ok')):
            return False, {'source_freeze': 'missing'}
        d = sdir_of(ctx, 'F18_full_flip_after_bytes_appear')
        E = rjson(ctx.e1['path'])
        late_real = os.path.realpath(ctx.h1_late_path)
        rdoc = rjson(late_real)

        def mutate(doc):
            flip_to_evaluated(E)(doc)
            doc['stage0_status']['members'][2].update({'custody_ok': True, 'terminal_status': rdoc['terminal_status'],
                                                       'written_utc': rdoc['written_utc'], 'before_step4': True})
            doc['pins']['input_files'].append({'path': late_real, 'sha256': sha_file(late_real),
                                               'bytes': os.path.getsize(late_real)})
        path, _fsha, _ssha, _nb = forge_manifest(ctx, s, src['path'], mutate, os.path.join(d, 'forged_manifest.json'))
        vr = s.verify_freeze_manifest(freeze_manifest_path=path)
        sc = s.score_after_freeze(freeze_manifest_path=path, registration_path=src['registration_path'],
                                  expected_manifest_file_sha256=src['manifest_file_sha256'],
                                  target_rows=copy.deepcopy(fx.target_rows),
                                  row_registration_rosters=dict(fx.roster_pins))
        ok = sc['ok'] is False and sc['refused'] is True and any('REFUSED (D8)' in x for x in sc['reasons'])
        return ok, {'score_ok': sc['ok'], 'score_reasons': sc['reasons'][:2],
                    'verify_ok_D8_boundary': vr['ok'], 'verify_reasons': vr['reasons'][:2]}
    run_test('F18', 'MUST_FAIL', 'a manifest re-hashed after the late receipt appeared, to claim STAGE0 EVALUATED, is '
             'refused by the scorer under the genuine registration (D8); the verifier alone is not expected to tell a '
             'fully re-hashed edit from a genuine freeze (v003g D8 note)', t_f18)

    # ---- controls: the two review defects reproduce in the unadopted c2v001
    def t_c04():
        d = sdir_of(ctx, 'C04_c2v001_D05')
        cp = cal_copy(d, 'calibration_record_copy.json')
        res = freeze(ctx, ctx.v1, ctx.sp, d, 'c2v001', s_evals(ctx), stage0_record=pin(cp))
        return (res['ok'] is False and any('more than one calibration record pinned' in x for x in res['reasons']),
                {'ok': res['ok'], 'reasons': res['reasons'][:2]})
    run_test('C04', 'CONTROL', 'c2v001 refuses the WHOLE freeze when the status-record pin names a custody-correct '
             'copy of the calibration record (review D05 reproduced)', t_c04)

    def t_c05():
        res, _rec, late_path, data, _lpin = late_receipt_scenario(ctx.v1, 'C05_c2v001_D07', V001_SHA256)
        if not res.get('ok'):
            return False, summary(res)
        v0, sc0 = vs(ctx.v1, res)
        wx(late_path, data)
        v1, sc1 = vs(ctx.v1, res)
        ok = (v0['ok'] and sc0['ok'] and v1['ok'] is False and sc1['ok'] is False
              and any('STAGE0_STATUS_BLOCK_MISMATCH' in x for x in v1['reasons']))
        return ok, {'before': brief(v0, sc0), 'after': brief(v1, sc1)}
    run_test('C05', 'CONTROL', 'c2v001: a registered freeze whose receipt was absent at freeze time fails verify and '
             'score once the root-pinned bytes appear (review D07 reproduced)', t_c05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run-dir', required=True)
    ap.add_argument('--module', default=None)
    args = ap.parse_args()
    started = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if not (sys.flags.isolated and sys.flags.dont_write_bytecode):
        raise SystemExit('run with python3 -I -B')
    run_dir = os.path.realpath(args.run_dir)
    os.makedirs(run_dir)   # must not exist
    here = os.path.dirname(os.path.realpath(__file__))
    succ_path = os.path.realpath(args.module or os.path.join(here, SUCCESSOR_NAME))
    if sha_file(V003G_PATH) != V003G_SHA256:
        raise SystemExit('v003g bytes changed')
    if sha_file(V001_PATH) != V001_SHA256:
        raise SystemExit('c2v001 bytes changed')
    ctx = Ctx()
    ctx.run_dir = run_dir
    ctx.succ_path = succ_path
    ctx.succ_sha = sha_file(succ_path)
    ctx.v = load_module(V003G_PATH, 'v003g_under_test')
    ctx.v1 = load_module(V001_PATH, 'c2v001_control')
    ctx.succ = load_module(succ_path, 'stage0_successor_under_test')
    ctx.fx = build_fixture(os.path.join(run_dir, 'fixture'), [ctx.v, ctx.v1, ctx.succ], ctx.succ)
    ctx.vp = pipeline(ctx.v, ctx.fx, with_stage0=False)
    ctx.sp = pipeline(ctx.succ, ctx.fx, with_stage0=True)
    tests(ctx)
    finished = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    counts = {}
    for r in RESULTS:
        c = counts.setdefault(r['expectation'], {'pass': 0, 'fail': 0})
        c['pass' if r['pass'] else 'fail'] += 1
    out = {'schema': 'STAGE0_SUCCESSOR_TEST_RUN_C2V002', 'started_utc': started, 'finished_utc': finished,
           'python': platform.python_version(), 'flags': {'isolated': sys.flags.isolated,
                                                          'dont_write_bytecode': sys.flags.dont_write_bytecode},
           'test_script': {'path': os.path.realpath(__file__), 'sha256': sha_file(os.path.realpath(__file__))},
           'v003g': {'path': V003G_PATH, 'sha256': V003G_SHA256},
           'c2v001_control': {'path': V001_PATH, 'sha256': V001_SHA256},
           'successor': {'path': succ_path, 'sha256': ctx.succ_sha},
           'synthetic_slots': {'path': ctx.fx.slots_path, 'sha256': sha_file(ctx.fx.slots_path)},
           'n_tests': len(RESULTS), 'n_pass': sum(r['pass'] for r in RESULTS),
           'n_fail': sum(not r['pass'] for r in RESULTS), 'counts_by_expectation': counts,
           'ast_identity': getattr(ctx, 'ast', None), 'results': RESULTS}
    wx(os.path.join(run_dir, 'RESULTS_test_stage0_successor_c2v002.json'),
       json.dumps(out, sort_keys=True, indent=1) + '\n')
    # every file and symlink this run created, sha256 from bytes (no directory walk)
    files = []
    for p in sorted(set(WRITTEN)):
        rel = os.path.relpath(p, run_dir)
        if os.path.islink(p):
            files.append({'path': rel, 'kind': 'symlink', 'target': os.readlink(p)})
        else:
            with open(p, 'rb') as fh:
                raw = fh.read()
            files.append({'path': rel, 'kind': 'file', 'sha256': sha_bytes(raw), 'bytes': len(raw)})
    wx(os.path.join(run_dir, 'FILES_WRITTEN_test_stage0_successor_c2v002.json'),
       json.dumps({'schema': 'STAGE0_SUCCESSOR_TEST_FILES_WRITTEN_C2V002', 'run_dir': run_dir, 'files': files},
                  sort_keys=True, indent=1) + '\n')
    print('TOTAL %d tests: %d pass, %d fail; by expectation %s' % (out['n_tests'], out['n_pass'], out['n_fail'],
                                                                    json.dumps(counts, sort_keys=True)))
    return 0 if out['n_fail'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
