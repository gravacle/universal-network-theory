"""dryrun_freeze_c2v004.py -- synthetic fixed-distance write_freeze_manifest dry runs for FREEZE_EXPECTED_INPUTS_C2V004.

It shows, through the pinned v003g writer itself, that the C2V004 notes (Claude4 0223 B1) and spec of record (B2) pass
_check_slot_geometry and _headline_conditions in the forced mode DDO154_DISTANCE_FIXED_AT_REGISTERED, that the C2V003
notes and the placeholder-slot spec are refused, that member selection does not depend on the NGC3198 slots, and that
the V-N1 Phase-2 rule (A163) gives the freeze status it names.  SYNTHETIC ONLY.
  Real (pinned, sha256 from bytes): v003g (48a1e48a); engine c2v003b (6ec8b2d0); the list's spec_of_record, notes,
    parameter_region and exact_alternative_declarations, passed literally; through the spec, the CX2V006 engine
    coordinates and slots V003 ngc3198_slots; the CX2V006 placeholder slots (contrast rows only); the STAGE0 grid that
    v003g pins for the STAGE0_GRID_OUTER roster.
  Synthetic (written here): the region file (12 rows, NOT DDO154), the query manifest (43 DRY-Q ids, role
    SYNTHETIC_FIXTURE), the DDO and NGC forwards, a slots document, a GL-node record, its source and a route-B config.
    v003g's root constants ROOT_SLOTS_PATH/ROOT_SLOTS_SHA256 and REGISTERED_GL_NODES_PATH/REGISTERED_GL_NODES_SHA256 are
    patched in memory to those synthetic files, so v003g opens no program slots file, NGC3198 query manifest or route-B
    config.  Nothing else in v003g is changed.
  The synthetic NGC forward refuses any geometry other than 13.8 Mpc / 72 deg with GEOMETRY_NOT_EXPOSED (V004 A16.4),
  except in row D-08, which uses a forward that ignores geometry (the A16.4 hazard).
Rows: D-01 Phase-1 shape (ORIGINAL_K and sensitivity at budget 0, allow_incomplete True) MUST_PASS FREEZE_INCOMPLETE;
  D-02 Phase-2 shape, no rule-(b)/(f) member, V-N1 gives False, MUST_PASS FREEZE_COMPLETE with the four NGC box-end
  sensitivity calls refused GEOMETRY_NOT_EXPOSED; D-03 one rule-(f) member with False (C2V003's fixed value) MUST_FAIL
  (A3); D-04 the same with V-N1 (True) MUST_PASS FREEZE_INCOMPLETE; D-05 the C2V003 notes MUST_FAIL; D-06 the notes
  without the A18 entry MUST_FAIL; D-07 the placeholder spec with the honest forward MUST_FAIL (NO_VALID_MEMBER);
  D-08 the placeholder spec with a geometry-ignoring forward MUST_FAIL (A16.1); D-09 the members under the placeholder
  spec equal those under the spec of record; D-10 PLAN outputs (budget 0) carry theta_ngc 13.8/72 (record) vs 13.8/70.
Every write is an exclusive create under --scratch; the results JSON is written by exclusive create to --out.
Nothing is launched; no value here is a value of record; no forward value is printed.
Usage: PY -I -B dryrun_freeze_c2v004.py --list LIST.json --list-sha256 SHA --c2v003 C2V003.json --scratch DIR --out OUT
"""
import os
for _k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import subprocess
from pathlib import Path

A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
V003G = (A + 'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
         '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405')
ENGINE = (A + 'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py',
          '6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3')
CX2V006 = (A + 'calib_tail_readiness_cx2/DDO154_COORDINATES_CX2V006.json',
           '50e7288e4697c8c8bca0544a4b81b5b15462c10efaed2d437530b95d8a80951f')
ADDENDUM = (A + 'calib_tail_readiness_cx2/COORDINATE_ADDENDUM_CX2V006.json',
            '9962b2aa673572a712d07fd74d12e61fe2418acbeb03b0ef3437118a6ca1e2b9')
C2V003_SHA = '454dd3ccb6f9d1056981aa44b24237e12066c43ef8a37753606b783fa3383e9d'
PRIMARY = 'BR_A_F10_PRIMARY'
QIDS = ['DRY-Q%02d' % k for k in range(1, 44)]
INVALID_IDS = QIDS[:2]
REGION_ROWS = ['DRY-R%02d' % i for i in range(1, 13)]
OBS, SIG, ZW, SCALE = 50.0, 2.0, 2.865260238532134, 8.0
REG_GEOM = {'ngc3198_distance_Mpc': 13.8, 'ngc3198_inclination_deg': 72.0}
KPC_M = 3.085677581491367e19
A18_KEY = 'A18-ROOT-V004'
VN1 = ('UNEVALUATED_CAP', 'UNEVALUATED_STEP7_DISCREPANCY')
ENGINE_PARAMS = None   # read from CX2V006 engine_parameters (budget raised so the synthetic run is COMPLETE)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def pinned(pin):
    b = Path(pin[0]).read_bytes()
    if sha_bytes(b) != pin[1]:
        raise SystemExit('PIN MISMATCH %s' % pin[0])
    return b


def load(pin, name):
    pinned(pin)
    sp = importlib.util.spec_from_file_location(name, pin[0])
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    pinned(pin)
    return m


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def write_x(path, obj):
    data = obj if isinstance(obj, bytes) else canon(obj)
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'path': os.path.realpath(str(path)), 'sha256': sha_bytes(data)}


def date_u():
    return subprocess.run(['/bin/date', '-u'], capture_output=True, text=True, env={'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'},
                          check=True).stdout.rstrip('\n')


def stub(label):
    return sha_bytes(('DRYRUN_C2V004_SYNTHETIC:' + label).encode())


def a_row(r):
    return (math.cos(0.9 * r + 0.3), math.sin(1.1 * r + 0.2), math.cos(1.7 * r + 1.0))


# ------------------------------------------------------------------------------------------------ synthetic world
def build_world(W, eng_coords, alternatives):
    dist = [c for c in eng_coords if c['name'] == 'distance_Mpc'][0]
    region = write_x(W / 'DRYRUN_SYNTHETIC_REGION_NOT_DDO154.json', {
        'rows': [{'id': rid, 'reference_radius_kpc': 0.5 * (i + 1), 'observed_speed_km_s': OBS,
                  'quoted_random_sigma_km_s': SIG, 'conditional_random_acceptance_low_km_s': OBS - ZW * SIG,
                  'conditional_random_acceptance_high_km_s': OBS + ZW * SIG} for i, rid in enumerate(REGION_ROWS)],
        'statistical_choice': 'dry-run synthetic; not DDO154', 'forward_coordinates': 'dry-run synthetic',
        'distance_summary': {'modulus_mag': 25.0 + 5.0 * math.log10(4.04), 'distance_central_Mpc': 4.04,
                             'reported68_low_Mpc': dist['lower'], 'reported68_high_Mpc': dist['upper'],
                             'scope': 'dry-run synthetic; the box of the CX2V006 distance coordinate'}})
    qm = write_x(W / 'DRYRUN_SYNTHETIC_QUERY_MANIFEST_NOT_NGC3198.json', {
        'rows': [{'query_id': q, 'data_row_index': j + 1, 'Rad_text': '%.2f' % (0.75 * (j + 1)), 'Rad_unit': 'kpc'}
                 for j, q in enumerate(QIDS)]})
    src = write_x(W / 'DRYRUN_SYNTHETIC_GL_SOURCE.json', {'schema': 'DRYRUN_SYNTHETIC_GL_SOURCE', 'note': 'synthetic'})
    src_pin = {'path': src['path'], 'sha256': src['sha256']}
    cfg = write_x(W / 'DRYRUN_SYNTHETIC_ROUTE_B_CONFIG.json', {
        'fields': {'radial.source_gauss_order': {'value': 4}, 'radial.n_columns': {'value': 100},
                   'source.profile': {'value': src_pin}}, 'note': 'dry-run synthetic; not the route-B config of record'})
    nodes = write_x(W / 'DRYRUN_SYNTHETIC_GL_NODES.json', {
        'schema': 'NGC_REGISTERED_ROUTE_B_GL_NODES_CX3V001', 'kpc_m': KPC_M, 'sources': {'profile': src_pin},
        'note': 'dry-run synthetic; not the registered node record',
        'orders': {'4': {'source_gauss_order': 4, 'registered_n_columns': 100,
                         'radii_m': [KPC_M * (0.3 + 0.4 * i) for i in range(100)]},
                   '10': {'source_gauss_order': 10, 'registered_n_columns': 250,
                          'radii_m': [KPC_M * (0.2 + 0.16 * i) for i in range(250)]}}})
    slots = write_x(W / 'DRYRUN_SYNTHETIC_SLOTS_DOCUMENT.json', {
        'schema': 'DRYRUN_SYNTHETIC_SLOTS_DOCUMENT_NOT_NGC3198', 'alternatives': alternatives,
        'query_block': {'rows': [{'query_id': q, 'Rad_text': '%.2f' % (0.75 * (j + 1)),
                                  'primary_GL4': {'reason': 'QUERY_INSIDE_INNERMOST_NODE' if q in INVALID_IDS else None}}
                                 for j, q in enumerate(QIDS)], 'invalid_primary_GL4': list(INVALID_IDS)},
        'projection_pins': {'route_b_config': {'path': cfg['path'], 'sha256': cfg['sha256']}},
        'note': 'dry-run synthetic: carries the list\'s alternatives; no query row of NGC3198'})
    return {'region': region, 'qm': qm, 'gl_source': src, 'route_b_config': cfg, 'gl_nodes': nodes, 'slots': slots}


def rosters(W, world, alternatives):
    pins = {}
    for a in alternatives['declared']:
        p = write_x(W / ('DRYRUN_ROSTER_%s.json' % a['name'].replace('.', 'p')), {
            'schema': 'ROOT_ROW_REGISTRATION_ROSTER_CX3V001', 'scope': 'SYNTHETIC_FIXTURE', 'alternative': a,
            'slots': {'path': world['slots']['path'], 'sha256': world['slots']['sha256']},
            'query_manifest': {'path': world['qm']['path'], 'sha256': world['qm']['sha256']},
            'query_mapping': [{'query_id': q, 'slots_query_id': q} for q in QIDS],
            'root_gates': [], 'outer_cut': {'mode': 'NONE'}})
        pins[a['name']] = {'path': p['path'], 'sha256': p['sha256']}
    return pins


def make_fwd_ddo(eng_coords):
    free = [(c['name'], math.log(c['lower']), math.log(c['upper'])) for c in eng_coords if c['role'] == 'free']
    assert len(free) == 3, free

    def f(theta):
        u = [(math.log(theta[n]) - lo) / (hi - lo) for n, lo, hi in free]
        return {'speeds_km_s': {rid: OBS + SIG * SCALE * sum(a * (x - 0.5) for a, x in zip(a_row(r), u))
                                for r, rid in enumerate(REGION_ROWS)}, 'valid': True, 'reasons': []}
    return f


def v010_result(speeds):
    rows, smap, inv = [], {}, []
    for q, s in zip(QIDS, speeds):
        if q in INVALID_IDS:
            rows.append({'id': q, 'speed_km_s': None, 'valid': False, 'reason': 'QUERY_INSIDE_INNERMOST_NODE'})
            smap[q] = None
            inv.append(q)
        else:
            rows.append({'id': q, 'speed_km_s': s, 'valid': True, 'reason': None})
            smap[q] = s
    stages = [{'stage': 'dry_' + k, 'kind': k, 'finish_sha256': stub(k + 'f'), 'state_digest': stub(k + 's'),
               'empty': False, 'production_admissible': True, 'test_only_admitted': False}
              for k in ('reference', 'body', 'columns', 'rotation')]
    return {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'galaxy': 'NGC3198', 'driver_sha256': stub('driver'),
            'call_spec_sha256': stub('spec'), 'scored': False, 'valid': True, 'status': 'COMPLETED', 'reasons': [],
            'rows': rows, 'speeds_km_s': smap, 'invalid_rows': inv,
            'route_a_outcome': {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                                'ro1': {'rule': 'RO1', 'armed': True, 'fired': False, 'events': [],
                                        'worker_sha256': stub('w'), 'binding_sha256': stub('b')}},
            'uv_tail': {'schema': 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010', 'enabled': True, 'admissibility': 'production',
                        'pending_certificates': [], 'source_rule': 'continuum_v001', 'nodes_ext_context': None,
                        'config': {'normalized_sha256': stub('cfg')}, 'stage_records': stages}}


def make_fwd_ngc(delta=0.0, honest=True, calls=None):
    def f(theta):
        if calls is not None:
            calls.append({k: theta.get(k) for k in REG_GEOM})
        if honest and any(theta.get(k) != v for k, v in REG_GEOM.items()):
            return {'valid': False, 'speeds_km_s': {}, 'reasons': [
                'GEOMETRY_NOT_EXPOSED: dry-run synthetic wrapper refuses any geometry other than 13.8 Mpc / 72 deg (A16.4)']}
        base = 120.0 + 40.0 * math.log(theta['common_scale_s'] / 0.1) + 3.0 * math.log(theta['gamma_over_Eref'] / 2e-16) \
            - 5.0 * math.log(theta['ell_F_m'] / 1e20) + delta
        return v010_result([base + 0.7 * (j + 1) for j in range(len(QIDS))])
    return f


def vn1_allow_incomplete(plan):
    """A163 V-N1, as FREEZE_EXPECTED_INPUTS_C2V004 states it: True iff a member of an evaluated alternative has
    own_disposition UNEVALUATED_CAP or UNEVALUATED_STEP7_DISCREPANCY in the replay plan of the last pass."""
    return any(m['own_disposition'] in VN1 for a in plan['alternatives'] if a['slots_status'] == 'EVALUATED_BEFORE_FREEZE'
               for m in a['members'])


def plan_of(alternatives, n_members, last_primary):
    out = []
    for a in alternatives['declared']:
        ms = []
        if a['status'] == 'EVALUATED_BEFORE_FREEZE':
            ms = [{'own_disposition': 'EVALUATED'} for _ in range(n_members)]
            if a['name'] == PRIMARY:
                ms[-1]['own_disposition'] = last_primary
        out.append({'name': a['name'], 'slots_status': a['status'], 'members': ms})
    return {'schema': 'DRYRUN_REPLAY_PLAN_SHAPE', 'alternatives': out}


def build_spec(G, cx, ngc, cm):
    am = G.apply_coordinate_mode(coordinates=copy.deepcopy(list(cx['coordinates'])) + copy.deepcopy(list(ngc)),
                                 coordinate_mode=copy.deepcopy(cm))
    assert am.get('ok'), am.get('reasons')
    fs = G.make_freeze_coordinate_spec(coordinates=am['coordinates'])
    assert fs.get('ok'), fs.get('reasons')
    return fs


# ------------------------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', required=True)
    ap.add_argument('--list-sha256', required=True)
    ap.add_argument('--c2v003', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    lst_raw = pinned((a.list, a.list_sha256))
    lst = json.loads(lst_raw)
    prev = json.loads(pinned((a.c2v003, C2V003_SHA)))
    W = Path(a.scratch)
    assert W.is_absolute() and not W.exists() and os.path.isdir(W.parent)
    os.mkdir(W)
    W = Path(os.path.realpath(W))
    G = load(V003G, 'dryrun_v003g')
    E = load(ENGINE, 'dryrun_engine')
    cx = json.loads(pinned(CX2V006))
    add = json.loads(pinned(ADDENDUM))
    wfm = {e['kwarg']: e for e in lst['write_freeze_manifest_inputs']}
    spec_rec = wfm['spec']['value']['spec_of_record']
    assert sha_bytes(G._canonical_bytes(spec_rec)) == wfm['spec']['value']['spec_canonical_sha256']
    notes_rec = wfm['notes']['value']
    param_region = wfm['parameter_region']['value']
    alternatives = lst['exact_alternative_declarations']
    fs_rec = G.make_freeze_coordinate_spec(coordinates=spec_rec['coordinates'])
    assert fs_rec.get('ok') and G._canonical_bytes(fs_rec['spec']) == G._canonical_bytes(spec_rec)
    fs_ph = build_spec(G, cx, cx['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation'],
                       add['coordinate_mode'])
    spec_ph = fs_ph['spec']
    assert G._canonical_bytes(fs_ph['engine_coordinates']) == G._canonical_bytes(fs_rec['engine_coordinates'])
    eng = fs_rec['engine_coordinates']

    world = build_world(W, eng, alternatives)
    real_consts = {'ROOT_SLOTS_PATH': G.ROOT_SLOTS_PATH, 'ROOT_SLOTS_SHA256': G.ROOT_SLOTS_SHA256,
                   'REGISTERED_GL_NODES_PATH': G.REGISTERED_GL_NODES_PATH,
                   'REGISTERED_GL_NODES_SHA256': G.REGISTERED_GL_NODES_SHA256}
    G.ROOT_SLOTS_PATH, G.ROOT_SLOTS_SHA256 = world['slots']['path'], world['slots']['sha256']
    G.REGISTERED_GL_NODES_PATH, G.REGISTERED_GL_NODES_SHA256 = world['gl_nodes']['path'], world['gl_nodes']['sha256']
    pins = rosters(W, world, alternatives)

    # the synthetic DDO run over the real CX2V006 engine coordinates (the CX2V006 engine parameters, budget raised)
    P = dict(cx['engine_parameters'])
    P['budget'] = 2000
    run = E.run_calibration_region(
        forward=make_fwd_ddo(eng), coordinates=eng, observation_region_path=world['region']['path'],
        observation_region_sha256=world['region']['sha256'], u_seed=P['u_seed'], budget=P['budget'],
        rel_step=P['rel_step'], min_step=P['min_step'], max_halvings=P['max_halvings'], null_tolerance=P['null_tolerance'],
        repair_iterations=P['repair_iterations'], max_repair_step=P['max_repair_step'], march_step=P['march_step'],
        bisection_steps=P['bisection_steps'], design_count=P['design_count'],
        global_design_count=P['global_design_count'], max_march_rounds=P['max_march_rounds'],
        hull_growth_tol=P['hull_growth_tol'], ddo154_distance=P['ddo154_distance'], rng_seed=P['rng_seed'])
    rec = E.write_calibration_record(run=run, record_path=str(W / 'DRYRUN_CALIBRATION_RECORD.json'),
                                     registry_path=str(W / 'DRYRUN_CALIBRATION_REGISTRY.jsonl'))
    if not rec.get('ok'):
        raise SystemExit('calibration record refused: %s; run %s %s' % (rec.get('reasons'), run.get('status'),
                                                                        (run.get('reasons') or [])[:4]))
    sel = G.select_representative_points(exploration=run, interior_count=5, spec=spec_rec)
    sel_ph = G.select_representative_points(exploration=run, interior_count=5, spec=spec_ph)
    if not (sel.get('ok') and sel_ph.get('ok')):
        raise SystemExit('selection refused: %s / %s' % (sel.get('reasons'), sel_ph.get('reasons')))
    n = len(sel['points'])
    world_summary = {
        'run_status': run.get('status'), 'evaluations_used': run.get('evaluations_used'),
        'n_admitted': sel['n_admitted'], 'n_members': n, 'member_roles': [p['role'] for p in sel['points']],
        'interior_count': 5, 'selection_interior_count_frozen': sel['admitted_region']['selection_interior_count'],
        'identified_directions': len(sel['admitted_region']['identified']),
        'engine_parameters': 'CX2V006 engine_parameters with budget 2000 (registered 120) so the synthetic run completes',
        'calibration_record': {'path': rec['record_path'] if 'record_path' in rec else str(W / 'DRYRUN_CALIBRATION_RECORD.json'),
                               'record_file_sha256': rec.get('record_file_sha256')},
        'synthetic_files': {k: v for k, v in world.items()}, 'rosters': pins,
        'patched_v003g_constants': {'real': real_consts,
                                    'dry_run': {'ROOT_SLOTS_PATH': world['slots']['path'],
                                                'ROOT_SLOTS_SHA256': world['slots']['sha256'],
                                                'REGISTERED_GL_NODES_PATH': world['gl_nodes']['path'],
                                                'REGISTERED_GL_NODES_SHA256': world['gl_nodes']['sha256']}}}
    rows = []
    code_files = [G.__file__, E.__file__, os.path.realpath(__file__)]
    input_files = [world['region']['path'], world['qm']['path'], str(W / 'DRYRUN_CALIBRATION_RECORD.json')]
    obs_rule = {'kind': 'DRYRUN_SYNTHETIC_RECTANGLES_NOT_DDO154', 'rule': 'the closed rectangles of the synthetic region'}

    def freeze(case, spec, selection, notes, fwd_p, fwd_k, b_prim, b_k, b_sens, allow):
        F = W / case
        os.mkdir(F)
        evp = G.evaluate_envelopes(forward_ngc=fwd_p, points=selection['points'], spec=spec, query_ids=QIDS,
                                   budget=b_prim, row_registration_roster=pins[PRIMARY])
        evk = G.evaluate_envelopes(forward_ngc=fwd_k, points=selection['points'], spec=spec, query_ids=QIDS, budget=b_k,
                                   row_registration_roster=pins['ORIGINAL_K'])
        ref = G.select_reference_member(selection=selection, evaluation=evp) if evp.get('ok') else {'ok': False}
        sens = (G.evaluate_sensitivity(forward_ngc=fwd_p, reference=ref, selection=selection, spec=spec, query_ids=QIDS,
                                       null_direction_rule={'mode': 'box_ends'}, budget=b_sens,
                                       row_registration_roster=pins[PRIMARY]) if ref.get('ok') else {'ok': False})
        w = G.write_freeze_manifest(
            out_path=str(F / 'FREEZE_MANIFEST.json'), registration_path=str(F / 'FREEZE_REGISTRATION.json'),
            parameter_region=param_region, observation_rule=obs_rule, spec=spec, selection=selection,
            alternatives=alternatives, alternative_evaluations={PRIMARY: evp, 'ORIGINAL_K': evk}, reference=ref,
            sensitivity=sens, query_ids=QIDS,
            query_manifest={'path': world['qm']['path'], 'sha256': world['qm']['sha256'], 'role': 'SYNTHETIC_FIXTURE'},
            code_files=code_files, input_files=input_files, notes=notes, allow_incomplete=allow,
            row_registration_rosters=pins)
        out = {'allow_incomplete': allow, 'budgets': {'primary': b_prim, 'original_k': b_k, 'sensitivity': b_sens},
               'evaluate_envelopes_primary': {'ok': evp.get('ok'), 'status': evp.get('status'),
                                              'n_member_valid': evp.get('n_member_valid'),
                                              'n_member_invalid': evp.get('n_member_invalid')},
               'reference': {'ok': ref.get('ok'), 'reasons': [r[:160] for r in (ref.get('reasons') or [])][:2]},
               'sensitivity': {'ok': sens.get('ok'), 'status': sens.get('status')},
               'writer': {'ok': w.get('ok'), 'freeze_status': w.get('freeze_status'),
                          'incomplete_reasons': w.get('incomplete_reasons'),
                          'reasons': [r[:240] for r in (w.get('reasons') or [])][:6],
                          'manifest_file_sha256': w.get('manifest_file_sha256')}}
        if w.get('ok'):
            vf = G.verify_freeze_manifest(freeze_manifest_path=w['path'])
            doc = json.loads(Path(w['path']).read_bytes())
            hc = doc.get('headline_conditions') or {}
            sb = hc.get('ngc3198_slot_box_sensitivity') or {}
            out['verify_freeze_manifest_ok'] = vf.get('ok')
            out['manifest'] = {
                'freeze_status': doc['freeze_status'], 'coordinate_mode': hc.get('coordinate_mode'),
                'structural_assumptions_present': hc.get('structural_assumptions_present'),
                'slot_headline_geometry': sb.get('headline_geometry'), 'slot_declared_range': sb.get('declared_range'),
                'n_refused_geometry_not_exposed': sb.get('n_refused_geometry_not_exposed'),
                'n_not_evaluated': sb.get('n_not_evaluated'),
                'member_theta_ngc_geometry': sorted({canon({k: m['theta_ngc'][k] for k in REG_GEOM}).decode()
                                                     for m in doc['members']}),
                'notes_equal_list_value': canon(doc['notes']) == canon(notes),
                'selection_interior_count': doc['admitted_region']['selection_interior_count']}
        return out

    def add_row(rid, kind, what, res, ok):
        rows.append({'row': rid, 'kind': kind, 'what': what, 'result': res, 'outcome': 'AS_EXPECTED' if ok else 'UNEXPECTED'})

    honest_p, honest_k = make_fwd_ngc(0.0), make_fwd_ngc(6.5)
    # D-01 Phase-1 shape
    r = freeze('D01_PHASE1_SHAPE', spec_rec, sel, notes_rec, honest_p, honest_k, n, 0, 0, True)
    m = r.get('manifest') or {}
    add_row('D-01', 'MUST_PASS', 'Phase-1 shape: spec of record + C2V004 notes; ORIGINAL_K and sensitivity at budget 0; '
            'allow_incomplete True', r,
            r['writer']['ok'] and r.get('verify_freeze_manifest_ok') and m.get('freeze_status') == 'FREEZE_INCOMPLETE' and
            A18_KEY in (m.get('structural_assumptions_present') or []) and
            m.get('slot_headline_geometry') == REG_GEOM and m.get('notes_equal_list_value') and
            m.get('selection_interior_count') == 5)
    # D-02 Phase-2 shape, V-N1 false
    plan2 = plan_of(alternatives, n, 'EVALUATED')
    allow2 = vn1_allow_incomplete(plan2)
    r = freeze('D02_PHASE2_COMPLETE', spec_rec, sel, notes_rec, honest_p, honest_k, n, n, 100, allow2)
    r['vn1'] = {'replay_plan_shape': 'no member with a V-N1 disposition', 'allow_incomplete': allow2}
    m = r.get('manifest') or {}
    add_row('D-02', 'MUST_PASS', 'Phase-2 shape, every call evaluated; V-N1 gives False; NGC box-end sensitivity calls '
            'refused GEOMETRY_NOT_EXPOSED', r,
            allow2 is False and r['writer']['ok'] and r.get('verify_freeze_manifest_ok') and
            m.get('freeze_status') == 'FREEZE_COMPLETE' and m.get('n_refused_geometry_not_exposed') == 4)
    # D-03 / D-04 one rule-(f) member
    plan3 = plan_of(alternatives, n, 'UNEVALUATED_CAP')
    allow4 = vn1_allow_incomplete(plan3)
    r = freeze('D03_CAP_FIXED_FALSE', spec_rec, sel, notes_rec, honest_p, honest_k, n - 1, n, 100, False)
    add_row('D-03', 'MUST_FAIL', 'Phase-2 shape with the last PRIMARY member UNEVALUATED_CAP (rule (f); budget n-1) and '
            'allow_incomplete False (C2V003\'s fixed value)', r,
            not r['writer']['ok'] and any('REFUSED (A3)' in x for x in r['writer']['reasons']))
    r = freeze('D04_CAP_VN1', spec_rec, sel, notes_rec, honest_p, honest_k, n - 1, n, 100, allow4)
    r['vn1'] = {'replay_plan_shape': 'the last PRIMARY member UNEVALUATED_CAP', 'allow_incomplete': allow4}
    m = r.get('manifest') or {}
    add_row('D-04', 'MUST_PASS', 'the same with allow_incomplete from the V-N1 rule', r,
            allow4 is True and r['writer']['ok'] and m.get('freeze_status') == 'FREEZE_INCOMPLETE' and
            r['writer']['incomplete_reasons'] == ['PRIMARY_MEMBER_EVALUATION_BUDGET_EXHAUSTED'])
    # D-05 the C2V003 notes
    notes_c3 = [e for e in prev['write_freeze_manifest_inputs'] if e['kwarg'] == 'notes'][0]['value']
    r = freeze('D05_C2V003_NOTES', spec_rec, sel, notes_c3, honest_p, honest_k, n, 0, 0, True)
    rs = r['writer']['reasons']
    add_row('D-05', 'MUST_FAIL', 'Phase-1 shape with the C2V003 notes value {A13, A16.1}', r,
            not r['writer']['ok'] and any(x.startswith('REFUSED (A16.1)') for x in rs) and
            any(x.startswith('REFUSED (A10/A12/A18)') for x in rs))
    # D-06 no A18 entry
    notes_no18 = copy.deepcopy(notes_rec)
    del notes_no18['structural_assumptions'][A18_KEY]
    r = freeze('D06_NO_A18', spec_rec, sel, notes_no18, honest_p, honest_k, n, 0, 0, True)
    add_row('D-06', 'MUST_FAIL', 'Phase-1 shape with the A18 entry removed from the notes', r,
            not r['writer']['ok'] and any(x.startswith('REFUSED (A18)') for x in r['writer']['reasons']))
    # D-07 placeholder spec, honest forward
    calls7 = []
    r = freeze('D07_PLACEHOLDER_HONEST', spec_ph, sel_ph, notes_rec, make_fwd_ngc(0.0, True, calls7),
               make_fwd_ngc(6.5, True), n, 0, 0, True)
    r['forward_geometries_seen'] = sorted({canon(c).decode() for c in calls7})
    add_row('D-07', 'MUST_FAIL', 'Phase-1 shape with the phase1 freeze_spec as coded (CX2V006 placeholder slots) and the '
            'A16.4 wrapper: every member refused, NO_VALID_MEMBER', r,
            not r['writer']['ok'] and r['evaluate_envelopes_primary']['n_member_valid'] == 0 and
            not r['reference']['ok'] and any('NO_VALID_MEMBER' in x for x in r['reference']['reasons']))
    # D-08 placeholder spec, geometry-ignoring forward
    r = freeze('D08_PLACEHOLDER_IGNORING', spec_ph, sel_ph, notes_rec, make_fwd_ngc(0.0, False),
               make_fwd_ngc(6.5, False), n, 0, 0, True)
    rs = r['writer']['reasons']
    add_row('D-08', 'MUST_FAIL', 'Phase-1 shape with the placeholder spec and a forward that ignores geometry (the A16.4 '
            'hazard): the writer refuses at the A16.1 slot check', r,
            not r['writer']['ok'] and sum(1 for x in rs if 'declared_range' in x) == 2 and
            any('headline_geometry' in x for x in rs))
    # D-09 members independent of the NGC slots
    same_ar = G._canonical_bytes(sel['admitted_region']) == G._canonical_bytes(sel_ph['admitted_region'])
    same_pts = G._canonical_bytes(sel['points']) == G._canonical_bytes(sel_ph['points'])
    add_row('D-09', 'TESTED_EQUAL', 'select_representative_points on the same run with the spec of record and with the '
            'placeholder spec: admitted_region and points canonically equal',
            {'admitted_region_equal': same_ar, 'points_equal': same_pts, 'n_members': n}, same_ar and same_pts)
    # D-10 PLAN outputs at budget 0
    pl = G.evaluate_envelopes(forward_ngc=honest_p, points=sel['points'], spec=spec_rec, query_ids=QIDS, budget=0,
                              row_registration_roster=pins[PRIMARY])
    pl_ph = G.evaluate_envelopes(forward_ngc=honest_p, points=sel_ph['points'], spec=spec_ph, query_ids=QIDS, budget=0,
                                 row_registration_roster=pins[PRIMARY])
    g_rec = sorted({canon({k: mm['theta_ngc'][k] for k in REG_GEOM}).decode() for mm in pl['members']})
    g_ph = sorted({canon({k: mm['theta_ngc'][k] for k in REG_GEOM}).decode() for mm in pl_ph['members']})
    add_row('D-10', 'TESTED_EQUAL', 'PLAN outputs (evaluate_envelopes at budget 0): member theta_ngc geometry under the '
            'spec of record and under the placeholder spec',
            {'spec_of_record': g_rec, 'placeholder_spec': g_ph},
            g_rec == [canon(REG_GEOM).decode()] and
            g_ph == [canon({'ngc3198_distance_Mpc': 13.8, 'ngc3198_inclination_deg': 70.0}).decode()])
    res = {'schema': 'UNT_FREEZE_DRYRUN_C2V004', 'date_u': date_u(), 'synthetic_only': True, 'launch_authorized': False,
           'list': {'path': os.path.realpath(a.list), 'sha256': a.list_sha256},
           'c2v003': {'path': os.path.realpath(a.c2v003), 'sha256': C2V003_SHA},
           'script': {'path': os.path.realpath(__file__), 'sha256': sha_bytes(Path(__file__).read_bytes())},
           'real_pins': {'v003g': V003G[1], 'engine_c2v003b': ENGINE[1], 'CX2V006': CX2V006[1], 'addendum': ADDENDUM[1]},
           'values_from_the_list': {
               'spec_of_record_canonical_sha256': wfm['spec']['value']['spec_canonical_sha256'],
               'notes_value_canonical_sha256': sha_bytes(G._canonical_bytes(notes_rec)),
               'parameter_region_canonical_sha256': sha_bytes(G._canonical_bytes(param_region)),
               'alternatives_canonical_sha256': sha_bytes(G._canonical_bytes(alternatives))},
           'placeholder_spec_canonical_sha256': sha_bytes(G._canonical_bytes(spec_ph)),
           'scratch': str(W), 'world': world_summary, 'rows': rows,
           'all_as_expected': all(x['outcome'] == 'AS_EXPECTED' for x in rows),
           'not_shown': 'no forward value, speed or manifest row is printed; the manifests stay in the scratch folder'}
    o = write_x(Path(a.out), (json.dumps(res, indent=1, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8'))
    print(json.dumps({'out': o, 'all_as_expected': res['all_as_expected'],
                      'rows': [(x['row'], x['outcome']) for x in rows], 'world': {k: world_summary[k] for k in (
                          'run_status', 'evaluations_used', 'n_admitted', 'n_members', 'member_roles',
                          'identified_directions')}}, indent=1))


if __name__ == '__main__':
    main()
