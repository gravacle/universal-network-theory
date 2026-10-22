"""Tests for calibration_orchestrator_c2v004.  SYNTHETIC ONLY.

Mock worker: tests/mock_forward_driver_c2v004.py (the v003 mock + the S1 outcomes nonpositive_rotation_all and
nonpositive_rotation_history_unreadable) run through the pinned root monitor and the campaign launcher campaign_c2v003
(be462862, unchanged, read from v003/).  The coordinate spec, the template (the real anchor spec bytes, read only), the
engine/freeze modules, FAILURE_TAXONOMY_V003.json and COORDINATE_SPEC_ADDENDUM_V004.json are the real files; the
observation region is a SYNTHETIC 12-row region (ids SYN_ROW_xx); deciding results (with genuine monitor receipts of
mock runs), comparator reports and files, numerics verdicts and capability evidence are SYNTHETIC fixtures.

Two coordinate modes are exercised:
  * the v003 suite T0-T33 (carried, adapted only where v004 changes the contract on purpose, each marked 'v004:') runs in
    the 4-coordinate DDO154_DISTANCE_NUISANCE mode through a SYNTHETIC addendum fixture (byte-for-byte the V004 addendum
    with only coordinate_mode replaced), so every distance path of v003 stays covered;
  * the new blocks run the REAL V004 addendum (A13: distance fixed at 4.04, 3 free coordinates) where they concern A13.
New (one block per fix): T34 S1, T35 S2, T36 S3, T37 S4, T38 F1, T39 F2, T40 F3, T41 A13 (3 coordinates).
No project forward, no network, single thread.  Writes only under ../test_runs/RUN_<UTC>_<pid>/ (an audit hook refuses
any other write and any open of a result.json under a KMAX_/D7R1/V005/V006/V007/DECIDING path).

usage: nice -n 10 <codex python3> -I -B tests/test_orchestrator_c2v004.py [--only T34,T35,...]
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import copy
import datetime
import hashlib
import importlib.util
import json
import math
import shutil
import signal
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(os.path.dirname(os.path.realpath(__file__)))
LANE = HERE.parent
ORCH_PATH = LANE / 'calibration_orchestrator_c2v004.py'
CAMP_PATH = LANE.parent / 'v003' / 'campaign_c2v003.py'          # unchanged launcher (be462862), read only
MOCK_PATH = HERE / 'mock_forward_driver_c2v004.py'
CRASH_RUNNER = HERE / 'crash_runner_c2v004.py'
VERIFY_PATH = LANE / 'verify_v008_specs_c2v004.py'
TAX_PATH = LANE / 'FAILURE_TAXONOMY_V003.json'
ADD_PATH = LANE / 'COORDINATE_SPEC_ADDENDUM_V004.json'             # REAL: A13 distance fixed (3 coordinates)
ADD4D = {}                                                         # SYNTHETIC 4-coordinate fixture (filled in main)
SPEC_PATH = LANE.parent / 'DDO154_CALIBRATION_COORDINATE_SPEC_V001.json'
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
V008 = ART / 'driver_v008_c2' / 'galaxy_m0_forward_c2v008.py'
MONITOR = {'path': str(ART / 'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'),
           'sha256': 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'}
C2R_SPEC = ART / 'kmax_prereg_v005_c2/specs_d7r1/CALL_KMAX_C2R_A2F10_D7R1_C2V005.json'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
RUN_DIR = LANE / 'test_runs' / ('RUN_%s_%d' % (STAMP, os.getpid()))
FIX = RUN_DIR / 'fixtures'
RESULTS = []
Z = 2.865260238532134
FORBIDDEN_RESULT_TOKENS = ('KMAX_', 'D7R1', 'V005', 'V006', 'V007', 'DECIDING')
AUDIT = {'denied': []}


def _audit(event, args):
    if event != 'open':
        return
    p = args[0]
    if not isinstance(p, (str, bytes, os.PathLike)):
        return
    p = os.path.abspath(os.fsdecode(p))
    mode, flags = args[1], args[2]
    w = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
        (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)))
    if w and not p.startswith(str(LANE) + '/') and not p.startswith('/dev/'):
        AUDIT['denied'].append(['write', p])
        raise PermissionError('test audit: write outside the lane refused: %s' % p)
    if os.path.basename(p) == 'result.json' and any(t in comp for comp in p.split('/') for t in FORBIDDEN_RESULT_TOKENS):
        if not p.startswith(str(RUN_DIR)):
            AUDIT['denied'].append(['forbidden_result', p])
            raise PermissionError('test audit: forbidden result.json refused: %s' % p)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p):
    return {'path': str(p), 'sha256': sha(p)}


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def check(tid, ok, detail=None):
    RESULTS.append({'id': tid, 'pass': bool(ok), 'detail': detail})
    print('%s %-58s %s' % ('PASS' if ok else 'FAIL', tid, json.dumps(detail, default=str)[:300]), flush=True)


ONLY = []


def guard(tid, fn):
    if ONLY and not any(tid == o or tid.startswith(o + '.') for o in ONLY):
        return
    try:
        fn()
    except BaseException as exc:   # noqa: BLE001 -- a test crash is a FAIL row, never a silent pass
        if isinstance(exc, KeyboardInterrupt):
            raise
        check(tid, False, {'raised': '%s: %s' % (type(exc).__name__, exc), 'tb': traceback.format_exc()[-2500:]})


O = load(ORCH_PATH, 'orch4_under_test')
MK = load(MOCK_PATH, 'mock4_under_test')
CAMP = load(CAMP_PATH, 'camp4_under_test')
SPEC = json.loads(SPEC_PATH.read_text())
TEMPLATE = json.loads(Path(SPEC['call_spec_mapping']['template']['path']).read_text())
C2R_NUMERICS = json.loads(C2R_SPEC.read_text())['numerics']
PH = TEMPLATE['physical']
ROWS = ['SYN_ROW_%02d' % i for i in range(1, 13)]
RADII = [0.5 * i for i in range(1, 13)]
TRUTH = {'x': 0.30, 'y': -0.10, 'z': 0.15, 'w': 0.004}
BASE_CONTROL = {'row_ids': ROWS, 'radii_kpc': RADII,
                'anchor': {'s0': PH['common_scale_s'], 'g0': PH['gamma'] / PH['Eref_J'], 'ell0': PH['ell_F_m']},
                'sleep_s': 0.3,
                'outcome_rules': [{'if': 'x_lt', 'value': -1.0, 'outcome': 'route_a_budget_noncontracting'},
                                  {'if': 'z_gt', 'value': 0.45, 'outcome': 'nonpositive_rotation_all'}],   # v004: S1
                'route_a_iteration_rules': [{'if': 'y_gt', 'value': 0.0, 'converged_iteration': 5},
                                            {'if': 'y_lt', 'value': -0.05, 'converged_iteration': 3}]}
TEST_DECL = {'rule': 'LAST_RATIOS_AT_LEAST', 'n_last': 2, 'threshold': 1.0, 'judgment_call': False,
             'declared_by': 'SYNTHETIC test root', 'basis': 'SYNTHETIC: non-contracting over the last two ratios'}
SYN_SOLVER, SYN_ID, SYN_ATT, SYN_PROF = 'a1' * 32, 'b2' * 32, 'syn-attempt-0001', 'c3' * 32
SYN_COMP_BYTES = b'# SYNTHETIC comparator fixture (not compare_deciding_ii_c2v008.py)\n'
SYN_COMP = hashlib.sha256(SYN_COMP_BYTES).hexdigest()           # v004 S4: the comparator FILE is hashed from bytes
REQ_CHECKS = O.DECIDING_EXPECT['ii_full_anchor']['required_checks']


def write_region(path, truth, control):
    v = MK.toy_speeds_from_xyzw(truth, control)
    ds = json.loads(Path(SPEC['observation_region']['path']).read_text())['distance_summary']
    rows = []
    for r, rad in zip(control['row_ids'], control['radii_kpc']):
        sg = max(0.02 * v[r], 0.25)
        rows.append({'id': r, 'reference_radius_kpc': rad, 'observed_speed_km_s': v[r], 'quoted_random_sigma_km_s': sg,
                     'conditional_random_acceptance_low_km_s': v[r] - Z * sg,
                     'conditional_random_acceptance_high_km_s': v[r] + Z * sg})
    doc = {'rows': rows, 'statistical_choice': 'SYNTHETIC toy (not DDO154 data)', 'forward_coordinates': 'SYNTHETIC toy',
           'distance_summary': dict(ds, scope='SYNTHETIC copy of the DDO154 distance_summary NUMBERS only, so the '
                                              'real distance box binds')}
    with open(path, 'x') as fh:
        json.dump(doc, fh, indent=1)
    return pin(path)


def write_control(path, control):
    with open(path, 'x') as fh:
        json.dump(control, fh, indent=1)
    return str(path)


_fix_counter = [0]


def fixture_dir(tag):
    _fix_counter[0] += 1
    d = FIX / ('%s_%03d' % (tag, _fix_counter[0]))
    d.mkdir(parents=True)
    return d


def mock_variant(tag, distance='ANY', stage='ANY', marker=True):
    p = FIX / ('mock_forward_driver_c2v004_%s.py' % tag)
    if p.exists():
        return p
    src = MOCK_PATH.read_bytes().replace(b"DISTANCE_POLICY = 'ANY'", b"DISTANCE_POLICY = '%s'" % distance.encode())
    src = src.replace(b"STAGE_BINDING_POLICY = 'ANY'", b"STAGE_BINDING_POLICY = '%s'" % stage.encode())
    if not marker:
        src = src.replace(O.SYNTHETIC_DRIVER_MARKER, b'NO_MARKER_HERE')
    src += ('\n# VARIANT %s\n' % tag).encode()
    p.write_bytes(src)
    return p


_MON = [None]


def monitor_mod():
    if _MON[0] is None:
        _MON[0] = load(MONITOR['path'], 'monitor_tests')
    return _MON[0]


def monitored_mock_run(d, driver, spec_obj, control, wall=60.0):
    """A genuine monitor run of the mock (receipt + result + finish under d)."""
    sp = d / 'spec.json'
    sp.write_bytes((json.dumps(spec_obj, indent=1, sort_keys=True) + '\n').encode())
    cpath = write_control(d / 'control.json', control)
    os.environ['CAL_ORCH_MOCK_CONTROL'] = cpath
    rec = monitor_mod().run_monitored(driver=str(driver), driver_sha256=sha(driver), spec=str(sp), outdir=str(d / 'out'),
                                      receipt=str(d / 'RECEIPT.json'), wall_cap_s=wall, rss_cap_bytes=1 << 30,
                                      output_cap_bytes=64 << 20, poll_s=0.1, python=PY)
    return sp, rec


_DECIDING = {}


def make_deciding(driver, N=8, mut_i=None, mut_ii=None, drop=None, comp_bytes=None, ref_result_bytes=None):
    """SYNTHETIC deciding pair (i) + (ii) for `driver`, with genuine monitor receipts of mock runs.  v004 (S4): the
    comparator is a real file (SYN_COMP_BYTES unless comp_bytes) and the reference run directory carries a result.json
    whose sha256 is the synthetic expectation (ref_result_bytes replaces those bytes after the expectation is set)."""
    key = (str(driver), N, json.dumps(mut_i, sort_keys=True), json.dumps(mut_ii, sort_keys=True), drop,
           comp_bytes, ref_result_bytes)
    if key in _DECIDING:
        return copy.deepcopy(_DECIDING[key])
    ctl = dict(BASE_CONTROL, sleep_s=0.0, route_a_s=0.0, rest_s=0.0, force_outcome='ok', force_converged_iteration=4,
               route_a_iteration_rules=[])
    out = {}
    # (i)
    d1 = fixture_dir('deciding_i')
    spec1 = dict(copy.deepcopy(TEMPLATE), label='SYNTHETIC deciding (i) fixture spec')
    ext = {'deciding_test': {'verdict': 'PASS_BITWISE_EQUAL'},
           'route_a_outcome': {'classification': 'CONVERGED', 'converged_iteration': 4},
           'identity': {'route_a': {'custody': {'iteration': 4, 'solver_code': {'path': '<syn>', 'sha256': SYN_SOLVER},
                                                'attempt_link': {'identity_sha256': SYN_ID, 'attempt': SYN_ATT},
                                                'source_profile_sha256': SYN_PROF}}}}
    if mut_i:
        MK._merge(ext, mut_i)
    sp1, rec1 = monitored_mock_run(d1, driver, spec1, dict(ctl, extra_result=ext, drop_result_keys=[drop] if drop else []))
    out['i_admit_prefix'] = {'result': {'path': rec1['result']['path'], 'sha256': rec1['result']['sha256']},
                             'finish_path': str(d1 / 'out' / 'finish.json'), 'receipt': pin(d1 / 'RECEIPT.json'),
                             'call_spec_sha256': sha(sp1)}
    # (ii)
    d2 = fixture_dir('deciding_ii')
    spec2 = copy.deepcopy(TEMPLATE)
    spec2['label'] = 'SYNTHETIC deciding (ii) fixture spec'
    spec2['numerics']['route_a'] = {'column_workers': N}
    ext2 = {'identity': {'route_a': {'implementation': {'column_workers': N}}}}
    sp2, rec2 = monitored_mock_run(d2, driver, spec2, dict(ctl, extra_result=ext2))
    ref = d2 / 'A2_ANCHOR_F10_RUN_V001'
    ref.mkdir()
    ref_bytes = b'{"synthetic_reference_result": true}\n'
    (ref / 'result.json').write_bytes(ref_result_bytes if ref_result_bytes is not None else ref_bytes)
    cfile = d2 / 'SYNTHETIC_COMPARATOR.py'
    cfile.write_bytes(comp_bytes if comp_bytes is not None else SYN_COMP_BYTES)
    rep = {'schema': 'UNT_DRIVER_V008_DECIDING_II_COMPARE_V001', 'comparator': {'path': str(cfile), 'sha256': SYN_COMP},
           'reference': str(ref), 'new': str(d2 / 'out'), 'column_workers': N, 'expect_new': 'parallel',
           'checks': {c: {'pass': True} for c in REQ_CHECKS}, 'verdict': 'PASS_BITWISE_EQUAL', 'failing': []}
    if mut_ii:
        MK._merge(rep, mut_ii)
    rp = d2 / 'COMPARE_DECIDING_II_SYNTHETIC.json'
    rp.write_text(json.dumps(rep, indent=1))
    out['ii_full_anchor'] = {'result': {'path': rec2['result']['path'], 'sha256': rec2['result']['sha256']},
                             'finish_path': str(d2 / 'out' / 'finish.json'), 'receipt': pin(d2 / 'RECEIPT.json'),
                             'call_spec_sha256': sha(sp2), 'compare_report': pin(rp)}
    out['synthetic_expect'] = {'i_admit_prefix': {'spec_sha256': sha(sp1), 'solver_sha256': SYN_SOLVER,
                                                  'attempt_link': {'identity_sha256': SYN_ID, 'attempt': SYN_ATT},
                                                  'source_profile_sha256': SYN_PROF},
                               'ii_full_anchor': {'spec_sha256': sha(sp2), 'comparator_sha256': SYN_COMP,
                                                  'reference_path': str(ref),
                                                  'reference_result_sha256': hashlib.sha256(ref_bytes).hexdigest()}}
    _DECIDING[key] = out
    return copy.deepcopy(out)


def make_numerics(block, *, attest=False, tamper=None, artifact_block=None):
    d = fixture_dir('verdict')
    vp = d / 'SYNTHETIC_KMAX_VERDICT.json'
    doc_block = copy.deepcopy(artifact_block if artifact_block is not None else block)
    if tamper == 'pointer_mismatch':
        doc_block['column_workers'] = 7
    vp.write_bytes(json.dumps({'decision': {'numerics_block': doc_block}, 'synthetic_fixture': True}, indent=1).encode())
    art = pin(vp)
    if tamper == 'sha':
        art['sha256'] = '2' * 64
    out = {'block': copy.deepcopy(block), 'verdict_artifact': art,
           'block_pointer': None if attest else '/decision/numerics_block',
           'root_attestation': 'SYNTHETIC attestation' if attest else None}
    if tamper == 'no_artifact':
        out['verdict_artifact'] = None
    if tamper == 'bad_pointer':
        out['block_pointer'] = '/decision/missing'
    return out


def c2r_like():
    return copy.deepcopy(C2R_NUMERICS)


def make_config(work_dir, region, anchor, *, numerics_block=None, numerics=None, wall_cap_s=60.0,
                executor='campaign', override=None, orphan=None, driver=None, deciding=None, max_concurrent=3,
                process_budget=12, n_cores=18, stage_aware=True, recovery_rules=None, disk_guard=None,
                contraction='DEFAULT', capability_evidence=None, deciding_N=8, volume=None, mode='4D',
                work_dir_identity=None):
    drv = driver or MOCK_PATH
    if numerics is None:
        numerics = make_numerics(numerics_block if numerics_block is not None else copy.deepcopy(TEMPLATE['numerics']))
    cfg = {'schema': O.SCHEMA_CONFIG, 'synthetic_test': True, 'work_dir': str(work_dir), 'work_dir_volume': volume,
           'coordinate_spec': pin(SPEC_PATH),
           'coordinate_spec_addendum': pin(ADD_PATH) if mode == '3D' else dict(ADD4D),
           'work_dir_identity': work_dir_identity,
           'observation_region': region, 'numerics': numerics, 'ngc3198_slots': None, 'anchor': anchor,
           'driver': pin(drv), 'deciding_test': deciding if deciding is not None else make_deciding(drv, N=deciding_N),
           'capability_evidence': capability_evidence,
           'taxonomy': pin(TAX_PATH), 'route_a_contraction_test': TEST_DECL if contraction == 'DEFAULT' else contraction,
           'recovery_rules': recovery_rules or [], 'monitor': MONITOR, 'campaign': pin(CAMP_PATH), 'python': PY,
           'max_concurrent': max_concurrent, 'process_budget': process_budget, 'stage_aware_budget': stage_aware,
           'n_cores': n_cores,
           'per_call': {'wall_cap_s': wall_cap_s, 'rss_cap_bytes': 1 << 30, 'output_cap_bytes': 64 << 20, 'poll_s': 0.25},
           'campaign_wall_cap_s': 3600.0,
           'disk_guard': disk_guard or {'per_call_bytes': 64 << 20, 'reserve_bytes': 1 << 30, 'measured_per_call_bytes': 1 << 20},
           'orphan_wait': orphan or {'poll_s': 0.5, 'cap_s': 300.0, 'receipt_grace_s': 5.0},
           'engine_parameters_override': override, 'executor': executor,
           'notes': 'SYNTHETIC TEST CONFIG (mock driver, synthetic region)'}
    return cfg


def save_config(cfg, name):
    p = FIX / name
    with open(p, 'x') as fh:
        json.dump(cfg, fh, indent=1)
    return p


def cli(cmd, cfg_path, control_path, extra=(), wait=True):
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['CAL_ORCH_MOCK_CONTROL'] = str(control_path)
    args = [PY, '-I', '-B', str(ORCH_PATH), cmd, '--config', str(cfg_path)] + list(extra)
    if not wait:
        return subprocess.Popen(args, env=env, stdout=open(str(cfg_path) + '.%s.stdout.txt' % cmd, 'a'),
                                stderr=open(str(cfg_path) + '.%s.stderr.txt' % cmd, 'a'))
    p = subprocess.run(args, env=env, capture_output=True, text=True)
    with open(str(cfg_path) + '.%s.log' % cmd, 'a') as fh:
        fh.write(p.stdout + '\n' + p.stderr + '\n')
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = {'unparsed': p.stdout[-2000:], 'stderr': p.stderr[-2000:]}
    return p.returncode, out


def halt_sha(work, wave_name):
    return sha(Path(work) / 'waves' / wave_name / 'HALT.json')


def resolve_all(cp, cpath, work, wave_name, decision, reason, extra=()):
    return cli('resolve', cp, cpath, ['--wave', str(int(wave_name.split('_')[1])), '--all', '--halt-sha256',
                                      halt_sha(work, wave_name), '--decision', decision, '--reason', reason] + list(extra))


def spec_forward_factory(control, judgment=False):
    def spec_forward(cs):
        oc, k, c = MK.choose(cs['physical'], control)
        if oc in ('ok', 'picard_bound_not_met'):
            return {'valid': True, 'speeds_km_s': MK.toy_speeds_from_xyzw(c, control), 'reasons': []}
        f = {'valid': False, 'speeds_km_s': {}, 'reasons': ['MOCK %s' % oc]}
        if judgment:
            f['_judgment'] = True
        return f
    return spec_forward


def max_overlap(timeline_path):
    ev = []
    for ln in Path(timeline_path).read_text().splitlines():
        d = json.loads(ln)
        if d['event'] in ('start', 'finish'):
            ev.append((d['t'], 1 if d['event'] == 'start' else -1))
    cur = best = 0
    for _, s in sorted(ev, key=lambda x: (x[0], x[1])):
        cur += s
        best = max(best, cur)
    return best


def max_weight(timeline_path):
    cur, best = {}, 0
    for ln in sorted(Path(timeline_path).read_text().splitlines(), key=lambda l: json.loads(l)['t']):
        d = json.loads(ln)
        cur[d['pid']] = d['weight']
        best = max(best, sum(cur.values()))
    return best


# ----------------------------------------------------------------------------------------------------------- tests
def t0_pins():
    E = load(SPEC['engine']['path'], 'eng_t0')
    tax = json.loads(TAX_PATH.read_text())
    la = json.loads((ART / 'driver_v008_c2/deciding/LAUNCH_DECIDING_I_C2V008.json').read_text())
    lb = json.loads((ART / 'driver_v008_c2/deciding/LAUNCH_DECIDING_II_C2V008.json').read_text())
    ei, eii = O.DECIDING_EXPECT['i_admit_prefix'], O.DECIDING_EXPECT['ii_full_anchor']
    pc = ' '.join(la['pass_condition'])
    deciding_ok = (la['pins']['spec']['sha256'] == ei['spec_sha256'] and ei['attempt_link']['identity_sha256'] in pc
                   and ei['attempt_link']['attempt'] in pc and ei['source_profile_sha256'] in pc and ei['solver_sha256'][:8] in pc
                   and lb['pins']['spec']['sha256'] == eii['spec_sha256'] and lb['pins']['comparator']['sha256'] == eii['comparator_sha256']
                   and la['pins']['driver']['sha256'] == sha(V008) and lb['pins']['driver']['sha256'] == sha(V008)
                   and lb['pins']['reference_run']['path'].endswith(eii['reference_run_name'])
                   and lb['pins']['reference_run']['path'] == eii['reference_path']                       # v004 S4
                   and lb['pins']['reference_run']['result_sha256'] == eii['reference_result_sha256'])
    a4 = json.loads(ADD_PATH.read_text())
    a4d = json.loads(Path(ADD4D['path']).read_text())
    mode_ok = (a4['coordinate_mode']['mode'] == O.MODE_D_FIXED and a4d['coordinate_mode']['mode'] == O.MODE_D_NUISANCE and
               {k: v for k, v in a4.items() if k != 'coordinate_mode'} == {k: v for k, v in a4d.items() if k != 'coordinate_mode'})
    real_ok = all(s in O.KNOWN_REAL_DRIVER_SHA256 for s in (sha(V008), tax['driver']['sha256']))
    ok = (sha(SPEC['engine']['path']) == '193841fa1f1d078f7fc981fdba78cf3d736b50ee17e019f0cf94aae94e3a63a6' and
          sha(SPEC['freeze']['path']) == '5ee3e5dce72c77870903ce378e146fb86f7288ab2a403deb39796e348ee0f9b8' and
          sha(MONITOR['path']) == MONITOR['sha256'] and
          sha(SPEC_PATH) == 'fdeb5eb9b69b302c3b7eca21ed772184da56e26224fa4f8b08c8a2b0534106f8' and
          SPEC['call_spec_mapping']['template']['sha256'] == sha(SPEC['call_spec_mapping']['template']['path']) and
          sha(tax['driver']['path']) == tax['driver']['sha256'] == 'f8e4770106abb83df5e658e91edc5593198fe87f0600ee5d1946f22415902f28'
          and json.loads(ADD_PATH.read_text())['applies_to_coordinate_spec_sha256'] == sha(SPEC_PATH)
          and sha(CAMP_PATH) == 'be462862b4f35970c9d13cbab5d65e8c02e951a8a02d4848d12058708c48d7a8')
    check('T0.pins_from_bytes', ok and deciding_ok and real_ok and mode_ok,
          {'orchestrator_sha256': sha(ORCH_PATH)[:16], 'campaign_sha256': sha(CAMP_PATH)[:16], 'mock_sha256': sha(MOCK_PATH)[:16],
           'taxonomy_sha256': sha(TAX_PATH)[:16], 'v008': sha(V008)[:16], 'deciding_constants_match_launch_json': deciding_ok,
           'addendum_4d_fixture_differs_only_in_mode': mode_ok,
           'engine_module': E.MODULE_NAME})


def t1_stop_contract(ctx):
    E = ctx.E
    calls = {'n': 0}

    def fwd_stop(theta):
        calls['n'] += 1
        if calls['n'] == 3:
            raise O._ProbeStop('TEST_STOP')
        return {'valid': True, 'speeds_km_s': {r: 10.0 for r in ctx.row_ids}, 'reasons': []}
    raised = None
    try:
        E.run_calibration_region(forward=fwd_stop, **ctx.run_kwargs())
    except O._ProbeStop as exc:
        raised = exc.reason
    check('T1.stop_propagates_out_of_engine', raised == 'TEST_STOP' and calls['n'] == 3,
          {'raised': raised, 'calls': calls['n']})


T2_CASES = [
    ('main', TRUTH, None, None),
    ('budget40_exhaust_in_core', TRUTH, None, {'budget': 40}),
    ('budget6_exhaust_in_jacobian', TRUTH, None, {'budget': 6}),
    ('seed_admitted', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 0.0}, None, None),
    ('no_admitted_point', {'x': 0.0, 'y': 0.0, 'z': 3.0, 'w': 0.0}, None, None),
    ('invalid_band_validity_limited', TRUTH, [{'if': 'z_gt', 'value': 0.2, 'outcome': 'route_a_budget'}], None),
    ('rounds3_tight_tol', TRUTH, None, {'max_march_rounds': 3, 'hull_growth_tol': 0.007, 'budget': 150}),
    ('budget_guard_tight', TRUTH, None, {'budget': 30, 'design_count': 12, 'global_design_count': 24}),
]


def t2_inprocess_matrix():
    out = []
    for name, truth, rules, override in T2_CASES:
        d = RUN_DIR / 'T2' / name
        d.mkdir(parents=True)
        control = copy.deepcopy(BASE_CONTROL)
        control['sleep_s'] = 0.0
        if rules is not None:
            control['outcome_rules'] = rules
        region = write_region(d / 'SYNTHETIC_REGION_NOT_DDO154.json', truth, control)
        cfg = make_config(d / 'work', region, {'use': False}, executor='in_process_test', override=override,
                          numerics_block=c2r_like())
        ctx = O.Context(cfg)
        fwd = spec_forward_factory(control)
        orc = O.Orchestrator(ctx, O.InProcessExecutor(ctx, fwd), log=lambda m: None)
        res = orc.run()
        direct = ctx.E.run_calibration_region(forward=lambda th: fwd(ctx.mapper.build(th)['spec']), **ctx.run_kwargs())
        rep = orc.probe.run(orc.cache, 'replay')['run']
        same = ctx.E._canonical_bytes(direct) == ctx.E._canonical_bytes(rep)
        row = {'case': name, 'orchestration': res.get('status'), 'engine_status': res.get('engine_status'),
               'evaluations': len(direct['evaluation_log']), 'distinct_launched': res.get('n_launched_distinct'),
               'waves': res.get('n_waves'), 'unused_launched': res.get('n_unused_launched_theta'),
               'replay_uncached': (res.get('replay') or {}).get('uncached_calls'),
               'deterministic': (res.get('replay') or {}).get('deterministic'),
               'record_verify': (res.get('record') or {}).get('verify_ok'), 'identical_to_direct_engine_run': same,
               'wave_sizes': [w.get('n_calls') for w in res.get('waves') or []],
               'D5_assessment': (res.get('D5_assessment') or {}).get('this_run_meets_tested_negative_condition')}
        out.append(row)
        ok = (res.get('status') == 'COMPLETE' and same and row['unused_launched'] == 0 and row['replay_uncached'] == 0
              and row['deterministic'] is True and row['record_verify'] is True)
        check('T2.%s' % name, ok, row)
    with open(RUN_DIR / 'T2' / 'T2_MATRIX.json', 'x') as fh:
        json.dump(out, fh, indent=1)
    return out


def make_anchor_fixture(control_path, driver=None, tag='ANCHOR'):
    """Mock anchor run at the template spec (bytes = the real anchor spec) by `driver` (default: the mock itself)."""
    drv = driver or MOCK_PATH
    d = fixture_dir('anchor_' + tag)
    spec_copy = d / 'ANCHOR_SPEC_COPY.json'
    with open(spec_copy, 'xb') as fh:
        fh.write(Path(SPEC['call_spec_mapping']['template']['path']).read_bytes())
    os.environ['CAL_ORCH_MOCK_CONTROL'] = str(control_path)
    rec = monitor_mod().run_monitored(driver=str(drv), driver_sha256=sha(drv), spec=str(spec_copy),
                                      outdir=str(d / 'out'), receipt=str(d / 'RECEIPT.json'),
                                      wall_cap_s=60.0, rss_cap_bytes=1 << 30, output_cap_bytes=64 << 20, poll_s=0.25, python=PY)
    anchor = {'use': True, 'receipt': pin(d / 'RECEIPT.json'),
              'result': {'path': rec['result']['path'], 'sha256': rec['result']['sha256']},
              'spec_sha256': sha(spec_copy), 'driver_sha256': sha(drv)}
    check('T3.anchor_fixture_run_%s' % tag, rec['status'] == 'FINISHED' and rec['driver_status'] == 'COMPLETED' and
          anchor['spec_sha256'] == SPEC['call_spec_mapping']['template']['sha256'],
          {'receipt_status': rec['status'], 'anchor_driver_sha256': anchor['driver_sha256'][:16]})
    return anchor


def ngc_stub_factory(qids, entropy_override=None):
    def forward_ngc(theta):
        assert 'distance_Mpc' not in theta, 'DDO154 nuisance leaked into the NGC forward'
        th = dict(theta)
        if entropy_override is not None:
            th['entropy_K_factor'] = entropy_override
        s = math.log(th['common_scale_s'] / PH['common_scale_s'])
        g = math.log(th['gamma_over_Eref'] / (PH['gamma'] / PH['Eref_J']))
        l = math.log(th['ell_F_m'] / PH['ell_F_m'])
        return {'speeds_km_s': {q: 150.0 * math.exp(-0.5 * (s + g)) * (1 - math.exp(-(j + 1) / (6.0 * math.exp(0.4 * l))))
                                + 2.0 * (th['entropy_K_factor'] - 64.0 / 121.0)
                                + 5.0 * (th['ngc3198_distance_Mpc'] / 13.8 - 1.0)
                                + 0.1 * (th['ngc3198_inclination_deg'] - 70.0)
                                for j, q in enumerate(qids)}, 'valid': True, 'reasons': []}
    return forward_ngc


def freeze_path(orc, ctx, rec_summary, tdir):
    F, E = ctx.F, ctx.E
    run = orc.probe.run(orc.cache, 'replay')['run']
    qids = ['SYN-Q%02d' % k for k in range(1, 44)]
    qm = tdir / 'SYNTHETIC_QUERY_MANIFEST_NOT_NGC3198.json'
    with open(qm, 'x') as fh:
        json.dump({'rows': [{'query_id': q, 'data_row_index': j + 1, 'Rad_text': '%.2f' % (1.0 * (j + 1)),
                             'Rad_unit': 'kpc'} for j, q in enumerate(qids)]}, fh)
    fs = ctx.freeze_spec
    stub = ngc_stub_factory(qids)
    sel = F.select_representative_points(exploration=run, interior_count=6, spec=fs['spec'])
    ev = F.evaluate_envelopes(forward_ngc=stub, points=sel['points'], spec=fs['spec'], query_ids=qids, budget=200)
    ev_k = F.evaluate_envelopes(forward_ngc=ngc_stub_factory(qids, 1.0), points=sel['points'], spec=fs['spec'],
                                query_ids=qids, budget=200)
    ref = F.select_reference_member(selection=sel, evaluation=ev)
    sens = F.evaluate_sensitivity(forward_ngc=stub, reference=ref, selection=sel, spec=fs['spec'], query_ids=qids,
                                  null_direction_rule={'mode': 'box_ends'}, budget=400)
    rp = rec_summary['record_path']
    w = F.write_freeze_manifest(
        out_path=str(tdir / 'FREEZE_MANIFEST.json'), registration_path=str(tdir / 'FREEZE_REGISTRATION.json'),
        parameter_region={'description': 'DDO154 computational trial box (synthetic test)',
                          'bounds_semantics': 'COMPUTATIONAL_TRIAL_BOX_NOT_EMPIRICAL_BOUNDS'},
        observation_rule={'rule': 'closed Bonferroni rectangle (synthetic region)'}, spec=fs['spec'], selection=sel,
        alternatives=SPEC['discrete_alternatives']['freeze_alternatives_declaration'],
        alternative_evaluations={'BR_A_F10_PRIMARY': ev, 'ORIGINAL_K': ev_k}, reference=ref, sensitivity=sens,
        query_ids=qids, query_manifest={'path': str(qm), 'sha256': sha(qm), 'role': 'SYNTHETIC_FIXTURE'},
        code_files=[SPEC['freeze']['path'], SPEC['engine']['path']], input_files=[ctx.region_pin['path'], str(qm), rp],
        notes={'synthetic_test': True}, allow_incomplete=False)
    if not w.get('ok'):
        check('T3.freeze_write', False, {'reasons': w.get('reasons')})
        return
    vf = F.verify_freeze_manifest(freeze_manifest_path=w['path'])
    vr = F.verify_registration(registration_path=w['registration_path'])
    vc = E.verify_calibration_record(record_path=rp, registry_path=rec_summary['registry_path'])
    targets = [{'id': q, 'velocity': 140.0 + 0.2 * j, 'sigma': 3.0} for j, q in enumerate(qids)]   # invented
    sc = F.score_after_freeze(freeze_manifest_path=w['path'], registration_path=w['registration_path'],
                              expected_manifest_file_sha256=w['manifest_file_sha256'], target_rows=targets)
    check('T3.freeze_path_to_ngc_stub', w.get('freeze_status') == 'FREEZE_COMPLETE' and vf.get('ok') and vr.get('ok')
          and vc.get('ok') and sc.get('ok') and w.get('calibration_record_bound') is True,
          {'n_members': len(sel['points']), 'freeze_status': w.get('freeze_status')})


def t3_end_to_end(region, control_path, anchor):
    tdir = RUN_DIR / 'T3'
    tdir.mkdir()
    cfg = make_config(tdir / 'work', region, anchor, numerics_block=c2r_like())
    os.environ['CAL_ORCH_MOCK_CONTROL'] = str(control_path)
    ctx = O.Context(cfg)
    orc = O.Orchestrator(ctx, log=lambda m: print('   [T3] ' + m, flush=True))
    t0 = time.time()
    res = orc.run()
    wall = time.time() - t0
    with open(tdir / 'T3_RESULT.json', 'x') as fh:
        json.dump(res, fh, indent=1, default=str)
    check('T3.orchestration_complete', res.get('status') == 'COMPLETE' and res.get('engine_status') == 'COMPLETE',
          {'status': res.get('status'), 'engine_status': res.get('engine_status'), 'wall_s': round(wall, 1),
           'n_waves': res.get('n_waves'), 'n_launched': res.get('n_launched'), 'halt': str(res.get('halt'))[:300]})
    if res.get('status') != 'COMPLETE':
        return None, None, None
    led = orc.launches()
    first = res['waves'][0]
    check('T3.alias_not_used_c2r_numerics_seed_computed_first', res['anchor_alias'].get('used') is False and
          first['families'] == [['seed']] and first['n_calls'] == 1, {'alias': res['anchor_alias'], 'first_wave': first})
    check('T3.every_theta_launched_once', all(v == 1 for v in led.values()), {'n_keys': len(led), 'max': max(led.values())})
    entries = orc.cache.entries
    inv = [e for e in entries.values() if e['classification'] == 'MODEL_INVALID']
    rules = sorted(set((e['provenance'].get('taxonomy') or {}).get('rule') for e in inv))
    r10 = [e for e in inv if (e['provenance'].get('taxonomy') or {}).get('rule') == 'R10']
    r30 = [e for e in inv if (e['provenance'].get('taxonomy') or {}).get('rule') == 'R30']
    check('T3.model_invalid_cached_by_taxonomy_never_relaunched', len(inv) > 0 and all(led.get(e['key'], 0) == 1 for e in inv)
          and set(rules) <= {'R10', 'R30'},
          {'n_model_invalid': len(inv), 'rules': rules, 'by_code': res.get('model_invalid_evaluations_in_run_by_code')})
    check('T3.C2_R10_model_invalid_only_under_declared_test_with_history',
          all(e['failure_class'] == 'ROUTE_A_NON_CONTRACTING_WITHIN_MAX_ITERATIONS' and
              len(e['provenance']['taxonomy']['detail']['residual_history']) == 8 and
              e['provenance']['taxonomy']['detail']['contraction']['verdict'] == 'NON_CONTRACTING' for e in r10)
          and all(e['provenance']['taxonomy']['judgment_call'] is True and e['provenance']['taxonomy']['detail']['passes']
                  for e in r30),
          {'n_R10': len(r10), 'n_R30': len(r30)})
    iters = {}
    for e in entries.values():
        if e['classification'] == 'VALID' and e['source'] == 'WAVE':
            cv = tuple((e['provenance'].get('route_a') or {}).get('converged') or [])
            iters[str(cv)] = iters.get(str(cv), 0) + 1
    check('T3.route_a_converged_at_3_4_5_all_VALID', all(iters.get(str((k,)), 0) > 0 for k in (3, 4, 5)),
          {'valid_entries_by_converged_iteration': iters})
    rp = res['replay']
    check('T3.replay_zero_uncached_and_deterministic', rp['uncached_calls'] == 0 and rp['calls'] == rp['hits'] and
          rp['deterministic'] is True, rp)
    check('T3.no_unused_launches', res['n_unused_launched_theta'] == 0, {'unused': res['n_unused_launched_theta']})
    rec = res['record']
    check('T3.calibration_record_and_registry', rec['verify_ok'] is True and rec['registry_chain_ok'] is True,
          {'record_file_sha256': rec['record_file_sha256'][:16]})
    run = orc.probe.run(orc.cache, 'replay')['run']
    leaked = [e['index'] for e in run['evaluation_log'] if O.PLACEHOLDER_REASON in json.dumps(e.get('prediction'))]
    check('T3.no_probe_placeholder_in_real_run', not leaked, {'leaked': leaked})
    fwd = spec_forward_factory(json.loads(Path(control_path).read_text()))
    direct = ctx.E.run_calibration_region(forward=lambda th: fwd(ctx.mapper.build(th)['spec']), **ctx.run_kwargs())

    def sig(r):
        return O.canonical([[e.get('theta_natural'), e['valid'],
                             (e.get('prediction') or {}).get('speeds_km_s') if e['valid'] else None]
                            for e in r['evaluation_log']] + [(r.get('exploration') or {}).get('admitted_points'), r['status']])
    check('T3.same_thetas_validity_speeds_admitted_as_direct_engine_run', sig(direct) == sig(run),
          {'direct_evaluations': len(direct['evaluation_log']), 'run_evaluations': len(run['evaluation_log'])})
    camp, acc = [], []
    for wd in sorted((tdir / 'work' / 'waves').glob('wave_*')):
        c = json.loads((wd / 'WAVE_RESULT.json').read_text())['campaign']
        camp.append(c.get('max_concurrent_observed'))
        acc.append(c.get('max_accounted_processes'))
    check('T3.waves_concurrency_and_process_budget', max(camp) <= 3 and max(acc) <= 12,   # v004: 3 calls (machine load rule)
          {'max_concurrent_observed': max(camp), 'max_accounted_processes': max(acc),
           'mock_timeline_max_overlap': max_overlap(json.loads(Path(control_path).read_text())['timeline']),
           'mock_timeline_max_weight': max_weight(json.loads(Path(control_path).read_text())['timeline'])})
    check('T3.summary_carries_addendum_work_dir_weights', res.get('open_items_from_addendum') and
          'D5' in res['open_items_from_addendum'] and str(res.get('column_workers_invariance', '')).startswith('UNTESTED')
          and res['work_dir']['resolved'] == os.path.realpath(str(tdir / 'work')) and res['call_weights']['peak'] == 2,
          {'addendum_items': sorted(res.get('open_items_from_addendum') or []), 'weights': res.get('call_weights')})
    freeze_path(orc, ctx, rec, tdir)
    return res, rp['run_canonical_sha256'], orc


def t4_resume(region, control_path, anchor, ref_sha):
    tdir = RUN_DIR / 'T4'
    tdir.mkdir()
    cfg = make_config(tdir / 'work', region, anchor, numerics_block=c2r_like())
    cp = save_config(cfg, 'T4_CONFIG.json')
    p = cli('run', cp, control_path, wait=False)
    killed_at, orphans = None, []
    t0 = time.time()
    while time.time() - t0 < 900:
        waves = sorted((tdir / 'work' / 'waves').glob('wave_*')) if (tdir / 'work' / 'waves').exists() else []
        if len(waves) >= 4 and not (waves[-1] / 'WAVE_RESULT.json').exists():
            calls = list((waves[-1] / 'campaign').glob('call_*')) if (waves[-1] / 'campaign').exists() else []
            running = [c for c in calls if (c / 'RECEIPT.json.launch.json').exists() and not (c / 'RECEIPT.json').exists()]
            if len(running) >= 2:
                os.kill(p.pid, signal.SIGKILL)
                p.wait()
                killed_at = waves[-1].name
                orphans = [json.loads((c / 'RECEIPT.json.launch.json').read_text())['child_pid'] for c in running]
                break
        if p.poll() is not None:
            break
        time.sleep(0.05)
    alive = [pid for pid in orphans if O.pid_alive(pid)]
    check('T4.killed_mid_wave_with_live_orphans', killed_at is not None and len(alive) >= 1,
          {'killed_at': killed_at, 'orphans': orphans, 'alive_after_kill': alive})
    code, out = cli('run', cp, control_path)
    ctx = O.Context(cfg)
    orc = O.Orchestrator(ctx, log=lambda m: None)
    led = orc.launches()
    events = O.read_jsonl(tdir / 'work' / 'EVENTS.jsonl')
    resumed = [e for e in events if 'resuming interrupted wave' in e['msg']]
    wr = json.loads((tdir / 'work' / 'waves' / killed_at / 'WAVE_RESULT.json').read_text()) if killed_at else {}
    camp = wr.get('campaign') or {}
    check('T4.resume_completes_identically', code == 0 and out.get('status') == 'COMPLETE' and
          (out.get('replay') or {}).get('run_canonical_sha256') == ref_sha,
          {'exit': code, 'status': out.get('status'), 'run_sha_equal_T3': (out.get('replay') or {}).get('run_canonical_sha256') == ref_sha})
    check('T4.no_relaunch_after_interruption', all(v == 1 for v in led.values()) and len(resumed) == 1 and
          (camp.get('n_resumed') or 0) >= 1,
          {'max_launches': max(led.values()) if led else None, 'resumed_events': len(resumed),
           'n_resumed_calls': camp.get('n_resumed')})


def t5_infra(region, anchor, ref_sha, persist):
    name = 'T5b_invalid' if persist else 'T5a_retry'
    tdir = RUN_DIR / name
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    if persist:
        control['outcome_rules'] = [{'if': 'z_lt', 'value': -0.5, 'outcome': 'unknown_stage'}] + control['outcome_rules']
    else:
        control['hang_rules'] = [{'if': 'z_lt', 'value': -0.5}]
    cpath = write_control(FIX / ('control_%s.json' % name), control)
    cfg = make_config(tdir / 'work', region, anchor, wall_cap_s=6.0, numerics_block=c2r_like())
    cp = save_config(cfg, '%s_CONFIG.json' % name)
    code1, out1 = cli('run', cp, cpath)
    halt = out1.get('halt') or []
    want = 'FAILED_AT_STAGE' if persist else 'MONITOR_STOPPED_WALL_CAP'
    check('%s.halted_infra' % name, code1 == 4 and out1.get('status') == 'HALTED_INFRA' and halt and
          all(i['reason'].startswith(want) and i['class'] == 'INFRA' and len(i['token']) == 64 for i in halt),
          {'exit': code1, 'status': out1.get('status'), 'n_halt': len(halt), 'wave': out1.get('wave'),
           'reason': halt[0]['reason'][:80] if halt else None})
    if code1 != 4:
        return
    code2, out2 = cli('run', cp, cpath)
    check('%s.unresolved_halt_blocks_relaunch' % name, code2 == 7 and out2.get('status') == 'HALTED_UNRESOLVED',
          {'exit': code2, 'n_keys': len(out2.get('keys') or [])})
    if persist:
        code3, out3 = resolve_all(cp, cpath, tdir / 'work', out1['wave'], 'invalid', 'TEST: declared invalid after an INFRA stage failure')
    else:
        c_inv, o_inv = resolve_all(cp, cpath, tdir / 'work', out1['wave'], 'invalid', 'TEST: must be refused (C11)')
        check('T27.C11_invalid_refused_after_wall_cap', c_inv == 3 and 'INVALID_REFUSED_FOR_MONITOR_STOPPED_WALL_CAP' in
              json.dumps(o_inv), {'exit': c_inv, 'reason': str(o_inv.get('reasons'))[:200]})
        control.pop('hang_rules')
        Path(cpath).write_text(json.dumps(control, indent=1))   # transient failure gone (test-owned control file)
        code3, out3 = resolve_all(cp, cpath, tdir / 'work', out1['wave'], 'retry', 'TEST: transient infrastructure failure')
    code4, out4 = cli('run', cp, cpath)
    orc = O.Orchestrator(O.Context(cfg), log=lambda m: None)
    orc.cache.open(create=False)
    led = orc.launches()
    keys = [i['key'] for i in halt]
    entries = {k: orc.cache.entries.get(k) for k in keys}
    if persist:
        ok = (code3 == 0 and code4 == 0 and all(led[k] == 1 for k in keys) and
              all(e and e['classification'] == 'MODEL_INVALID' and e['source'] == 'ROOT_RESOLUTION' for e in entries.values()))
        check('%s.declared_invalid_then_complete' % name, ok,
              {'exit_resolve': code3, 'exit_run': code4, 'launches': [led[k] for k in keys],
               'failure_classes': sorted(set(e['failure_class'] for e in entries.values() if e))})
    else:
        ok = (code3 == 0 and code4 == 0 and all(led[k] == 2 for k in keys) and
              all(e and e['classification'] == 'VALID' for e in entries.values()) and
              (out4.get('replay') or {}).get('run_canonical_sha256') == ref_sha)
        check('%s.token_retry_then_complete_identical' % name, ok,
              {'exit_resolve': code3, 'exit_run': code4, 'launches': [led[k] for k in keys],
               'run_sha_equal_T3': (out4.get('replay') or {}).get('run_canonical_sha256') == ref_sha})


def t6_numerics(region, anchor_same, anchor_variant):
    tdir = RUN_DIR / 'T6'
    tdir.mkdir()
    ctx_a = O.Context(make_config(tdir / 'work_a', region, anchor_same))                       # template numerics
    ctx_b = O.Context(make_config(tdir / 'work_b', region, anchor_same, numerics_block=c2r_like()))
    blk_c = c2r_like()
    blk_c['column_workers'] = 1
    ctx_c = O.Context(make_config(tdir / 'work_c', region, anchor_same, numerics_block=blk_c))
    plan_b = O.Orchestrator(ctx_b).plan_only()
    calls = plan_b['next_wave']['calls']
    check('T6.c2r_numerics_disable_alias_seed_computed', ctx_a.cache_id != ctx_b.cache_id and
          plan_b['alias']['used'] is False and len(calls) == 1 and calls[0]['family'] == ['seed'],
          {'alias': plan_b['alias'], 'first_call_family': calls[0]['family']})
    plan_a = O.Orchestrator(ctx_a).plan_only()
    fam = sorted(set(tuple(c['family']) for c in plan_a['next_wave']['calls']))
    check('T6.template_numerics_same_driver_alias_first_wave_is_jacobian', plan_a['alias']['used'] is True and
          fam == [('jacobian',)] and plan_a['next_wave']['n_calls'] == 4, {'n_calls': plan_a['next_wave']['n_calls'], 'families': fam})
    ctx_v = O.Context(make_config(tdir / 'work_v', region, anchor_variant))
    plan_v = O.Orchestrator(ctx_v).plan_only()
    check('T6.C5_anchor_of_another_driver_never_aliased', plan_v['alias']['used'] is False and
          'ANCHOR_DRIVER_DIFFERS' in plan_v['alias']['reason'] and plan_v['next_wave']['calls'][0]['family'] == ['seed'],
          {'alias': plan_v['alias']})
    bad = dict(anchor_same, accept_driver_equivalence=True)
    try:
        O.Orchestrator(O.Context(make_config(tdir / 'work_e', region, bad))).plan_only()
        r = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        r = str(exc)[:120]
    check('T6.C5_accept_driver_equivalence_key_refused', 'accept_driver_equivalence' in r, {'reason': r})
    check('T6.column_workers_enters_cache_id_and_spec', ctx_b.cache_id != ctx_c.cache_id and
          ctx_c.base['numerics']['column_workers'] == 1 and ctx_b.base['numerics']['column_workers'] == 2,
          {'cw_b': ctx_b.column_workers, 'cw_c': ctx_c.column_workers})
    ctx_d = O.Context(make_config(tdir / 'work_d', region, anchor_same, numerics_block=c2r_like(), contraction=None))
    check('T6.contraction_test_declaration_enters_cache_id', ctx_d.cache_id != ctx_b.cache_id, {})
    d = O.diff_paths(TEMPLATE, ctx_b.base)
    check('T6.base_spec_differs_from_template_only_in_numerics', d and all(p.startswith('numerics.') for p in d),
          {'paths': d[:12], 'n': len(d)})


def t7_mapper(region):
    ctx = O.Context(make_config(RUN_DIR / 'T7' / 'work', region, {'use': False}, numerics_block=c2r_like()))
    import random
    rnd = random.Random(7)
    bad, nchk = [], 0
    for _ in range(40):
        u = [rnd.random() for _ in range(ctx.n_varying)]
        th = ctx.E.to_natural(spec=ctx.es, u=u)['theta_natural']
        b = ctx.mapper.build(th)
        if not set(b['changed_paths']) <= set(O.DECLARED_CHANGED_PATHS):
            bad.append(b['changed_paths'])
        n = ctx.prelaunch_check(b['spec'])
        nd = O.diff_paths(ctx.norm_base, n)
        if not set(nd) <= set(O.DECLARED_CHANGED_PATHS):
            bad.append(('normalized', nd))
        nchk += 1
        ph = b['spec']['physical']
        if ph['gamma'] != th['gamma_over_Eref'] * th['Eref_base_J'] or ph['common_scale_s'] != th['common_scale_s'] or \
                ph['distance_Mpc'] != th['distance_Mpc'] or ph['inclination_deg'] != 66.0:
            bad.append('physical')
        if CAMP._spec_bytes({'spec': b['spec']}) != b['raw']:
            bad.append('campaign_bytes')
        if b['spec']['numerics'] != ctx.base['numerics']:
            bad.append('numerics')
    cap = ctx.gates['driver_capability']
    check('T7.only_declared_fields_change_vs_base_and_normalized', not bad and cap['ok'] and cap['n_points'] == 17,
          {'bad': bad[:3], 'checked': nchk, 'capability': {k: cap[k] for k in ('ok', 'n_points', 'n_accepted')}})
    th = ctx.E.to_natural(spec=ctx.es, u=[0.5] * ctx.n_varying)['theta_natural']
    refusals = {}
    for label, mut in (('fixed_changed', ('ML_3p6', 0.45)), ('outside_box', ('ell_F_m', th['ell_F_m'] * 10)),
                       ('missing_coordinate', ('native_g', None))):
        t2 = dict(th)
        if mut[1] is None:
            t2.pop(mut[0])
        else:
            t2[mut[0]] = mut[1]
        try:
            ctx.mapper.build(t2)
            refusals[label] = 'NOT REFUSED'
        except O.OrchestratorError as exc:
            refusals[label] = 'refused: %s' % str(exc)[:80]
    check('T7.mapper_refuses_tampered_theta', all(v.startswith('refused') for v in refusals.values()), refusals)


def _tamper_copy(t3_work, tag):
    dst = RUN_DIR / ('T24_%s' % tag) / 'work'
    shutil.copytree(Path(t3_work) / 'cache', dst / 'cache')
    return dst


def _rehash(d):
    body = {k: v for k, v in d.items() if k != 'entry_sha256'}
    d['entry_sha256'] = O.sha256_bytes(O.canonical(body))
    return d


def t8_t24_cache_tamper(region, anchor, t3_work):
    """T8 (v002) + T24 (M3/C9/L1: CHECK_SOFTWARE C6b/C6c/C6d/C6e) on test-owned copies of the T3 cache."""
    def open_copy(dst):
        ctx = O.Context(make_config(dst, region, anchor, numerics_block=c2r_like()))
        try:
            O.Cache(ctx).open(create=False)
            return 'ACCEPTED'
        except O.OrchestratorError as exc:
            return 'REFUSED: %s' % str(exc)

    def entries(dst):
        return [(p, json.loads(p.read_text())) for p in sorted((dst / 'cache').glob('*/entries/*.json'))]
    dst = _tamper_copy(t3_work, 'control')
    r = open_copy(dst)
    check('T24.untampered_copy_opens', r == 'ACCEPTED', {'result': r})
    for variant in ('stale_selfhash', 'F2_speed_with_fresh_selfhash'):
        dst = _tamper_copy(t3_work, variant)
        p, d = next((p, d) for p, d in entries(dst) if d['classification'] == 'VALID' and d['source'] == 'WAVE')
        k0 = sorted(d['forward']['speeds_km_s'])[0]
        d['forward']['speeds_km_s'][k0] += 5.0
        if variant != 'stale_selfhash':
            _rehash(d)
        p.write_text(json.dumps(d))
        r = open_copy(dst)
        want = 'self-hash' if variant == 'stale_selfhash' else 'F2 custody'
        check('T8.cache_tamper_refused.%s' % variant, r.startswith('REFUSED') and want in r, {'result': r[:160]})
    # C6b: a VALID entry copied to a new theta (ell_F x 1.0001) under a new key and file name
    dst = _tamper_copy(t3_work, 'C6b_copy_to_new_theta')
    p, d = next((p, d) for p, d in entries(dst) if d['classification'] == 'VALID' and d['source'] == 'WAVE')
    d2 = copy.deepcopy(d)
    d2['theta']['ell_F_m'] = d2['theta']['ell_F_m'] * 1.0001
    d2['key'] = O.theta_key(d2['theta'])
    _rehash(d2)
    (p.parent / (d2['key'] + '.json')).write_text(json.dumps(d2))
    r = open_copy(dst)
    check('T24.M3_C6b_copy_to_new_theta_refused', r.startswith('REFUSED') and 'M3' in r, {'result': r[:160]})
    # C6c: VALID relabelled MODEL_INVALID with a consistent forward and rule
    dst = _tamper_copy(t3_work, 'C6c_valid_to_invalid')
    p, d = next((p, d) for p, d in entries(dst) if d['classification'] == 'VALID' and d['source'] == 'WAVE')
    res = json.loads(Path(d['provenance']['result_path']).read_text())
    fc = 'FINAL_PASS_NONPOSITIVE_ROTATION_SQUARE'
    d.update(classification='MODEL_INVALID', failure_class=fc,
             forward=O.forward_from_result(res, 'MODEL_INVALID', fc, 'R30', ROWS))
    d['provenance']['taxonomy'].update(rule='R30', code=fc, **{'class': 'MODEL_INVALID'})
    _rehash(d)
    p.write_text(json.dumps(d))
    r = open_copy(dst)
    check('T24.C9_C6c_valid_relabelled_invalid_refused', r.startswith('REFUSED') and 'C9' in r, {'result': r[:160]})
    # C6e: a MODEL_INVALID entry's failure_class and rule edited consistently
    dst = _tamper_copy(t3_work, 'C6e_reason_forged')
    p, d = next((p, d) for p, d in entries(dst) if d['classification'] == 'MODEL_INVALID' and d['source'] == 'WAVE')
    res = json.loads(Path(d['provenance']['result_path']).read_text())
    fc = 'FINAL_PASS_NONPOSITIVE_ROTATION_SQUARE' if d['failure_class'] != 'FINAL_PASS_NONPOSITIVE_ROTATION_SQUARE' else \
        'ROUTE_A_NON_CONTRACTING_WITHIN_MAX_ITERATIONS'
    rule = 'R30' if fc.startswith('FINAL') else 'R10'
    d.update(failure_class=fc, forward=O.forward_from_result(res, 'MODEL_INVALID', fc, rule, ROWS))
    d['provenance']['taxonomy'].update(rule=rule, code=fc)
    _rehash(d)
    p.write_text(json.dumps(d))
    r = open_copy(dst)
    check('T24.C9_C6e_failure_class_forged_refused', r.startswith('REFUSED') and 'C9' in r, {'result': r[:160]})
    # C6d: a VALID theta turned into a forged ROOT_RESOLUTION entry
    dst = _tamper_copy(t3_work, 'C6d_forged_root_resolution')
    p, d = next((p, d) for p, d in entries(dst) if d['classification'] == 'VALID' and d['source'] == 'WAVE')
    d.update(classification='MODEL_INVALID', failure_class='ROOT_DECLARED_INVALID_AFTER_INFRA:FORGED',
             source='ROOT_RESOLUTION', forward={'valid': False, 'speeds_km_s': {}, 'reasons': ['forged']})
    d['provenance'] = {'wave': 1, 'halt_token': 'e' * 64, 'resolution_line_sha256': 'f' * 64}
    _rehash(d)
    p.write_text(json.dumps(d))
    r = open_copy(dst)
    check('T24.L1_C6d_forged_root_resolution_refused', r.startswith('REFUSED') and 'L1' in r, {'result': r[:160]})


T9_CASES = [
    ('ok_iter3', 'ok', 3, 'VALID', 'R01', False, None),
    ('ok_iter4', 'ok', 4, 'VALID', 'R01', False, None),
    ('ok_iter5', 'ok', 5, 'VALID', 'R01', False, None),
    ('C1_picard_bound_not_met', 'picard_bound_not_met', 4, 'NUMERICS_LIMITED', 'R03', False, 'PICARD_BOUND_NOT_MET_WITHIN_PASSES'),
    ('C2_budget_contracting_declared_test', 'route_a_budget', 4, 'NUMERICS_LIMITED', 'R10', True,
     'ROUTE_A_ITERATION_BUDGET_EXHAUSTED_CONTRACTING'),
    ('C2_budget_noncontracting_declared_test', 'route_a_budget_noncontracting', 4, 'MODEL_INVALID', 'R10', False,
     'ROUTE_A_NON_CONTRACTING_WITHIN_MAX_ITERATIONS'),
    ('route_a_fsp_numeric', 'route_a_fsp:FREE_BOUNDARY_NOT_BRACKETED', 2, 'NUMERICS_LIMITED', 'R11', True, None),
    ('route_a_fsp_unknown', 'route_a_fsp:SOMETHING_NEW', 2, 'INFRA', 'R14', False, None),
    ('route_a_cap_no_end', 'route_a_cap_no_end', 4, 'NUMERICS_LIMITED', 'R12', False, None),
    ('route_a_nonfinite', 'route_a_nonfinite', 2, 'NUMERICS_LIMITED', 'R13', True, None),
    ('C10_relaxed_gas_nonfinite', 'route_a_relaxed_nonfinite', 2, 'NUMERICS_LIMITED', 'R13', True,
     'ROUTE_A_WORKER_NONFINITE:relaxed gas: nonfinite'),
    ('route_a_pool_failure', 'route_a_pool_failure', 2, 'INFRA', 'R15', False, None),
    ('fs_mass_enthalpy', 'fs_column:MASS_ENTHALPY_NOT_BRACKETED', 4, 'NUMERICS_LIMITED', 'R20', False, None),
    ('fs_interior_hole', 'fs_column:SAMPLED_INTERIOR_HOLE', 4, 'NUMERICS_LIMITED', 'R20', True, None),
    ('fs_unknown_token', 'fs_column:NOT_A_KNOWN_TOKEN', 4, 'INFRA', 'R41', False, None),
    ('rfs_no_two_surfaces', 'rfs_column:NO_TWO_SAMPLED_FREE_SURFACES', 4, 'NUMERICS_LIMITED', 'R21', False, None),
    ('C3_nonpositive_rotation_bound_declared', 'nonpositive_rotation_all', 4, 'MODEL_INVALID', 'R30', True,   # v004: S1
     'FINAL_PASS_NONPOSITIVE_ROTATION_SQUARE'),
    ('S1_positive_passes_then_nonpositive_bound_declared', 'nonpositive_rotation', 4, 'NUMERICS_LIMITED', 'R30', True,
     'FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED'),
    ('S1_pass_history_unreadable', 'nonpositive_rotation_history_unreadable', 4, 'INFRA', 'R30', False,
     'FINAL_PASS_NONPOSITIVE_PASS_HISTORY_UNREADABLE'),
    ('C6_colmean_invalid_rotation', 'colmean_invalid_rotation', 4, 'INFRA', 'R31', False, None),
    ('enospc', 'enospc', 4, 'INFRA', 'R44', False, None),
    ('custody', 'custody', 4, 'INFRA', 'R40', False, None),
    ('two_converged_ends', 'two_converged_ends', 4, 'INFRA', 'R40', False, None),
    ('unknown_stage_reason', 'unknown_stage', 4, 'INFRA', 'R41', False, None),
    ('weird_status', 'weird_status', 4, 'INFRA', 'DEFAULT', False, None),
]


def _classify_case(tdir, ctx, b, name, outcome, k, driver=MOCK_PATH):
    ex = O.CampaignExecutor(ctx)
    control = copy.deepcopy(BASE_CONTROL)
    control.update(sleep_s=0.0, route_a_s=0.0, rest_s=0.0, force_outcome=outcome, force_converged_iteration=k,
                   route_a_iteration_rules=[])
    d = tdir / 'campaign' / ('call_%s' % name)
    d.mkdir(parents=True)
    (d / 'spec.json').write_bytes(b['raw'])
    os.environ['CAL_ORCH_MOCK_CONTROL'] = write_control(FIX / ('control_%s_%s.json' % (tdir.name, name)), control)
    rec = monitor_mod().run_monitored(driver=str(driver), driver_sha256=sha(driver), spec=str(d / 'spec.json'),
                                      outdir=str(d / 'out'), receipt=str(d / 'RECEIPT.json'), wall_cap_s=60.0,
                                      rss_cap_bytes=1 << 30, output_cap_bytes=64 << 20, poll_s=0.1, python=PY)
    crec = {'status': 'OK' if rec.get('driver_status') == 'COMPLETED' else 'FAILED', 'call_dir': str(d)}
    cls, code, fwd, prov = ex.classify({'spec_sha256': b['sha256']}, crec)
    return cls, code, fwd, prov, json.loads((d / 'out' / 'result.json').read_text())['status']


def t9_taxonomy(region):
    tdir = RUN_DIR / 'T9'
    tdir.mkdir()
    blk = c2r_like()
    blk['brackets']['rule']['fs_absolute_overrides']['5'] = [302500000.0, 317625000.0]   # pre-R1: the mock cure is off
    ctx = O.Context(make_config(tdir / 'work', region, {'use': False}, numerics_block=blk))
    th = ctx.E.to_natural(spec=ctx.es, u=[0.5] * ctx.n_varying)['theta_natural']
    b = ctx.mapper.build(th)
    rows, by_status = [], {}
    for name, outcome, k, want_cls, want_rule, want_j, want_code in T9_CASES:
        cls, code, fwd, prov, st = _classify_case(tdir, ctx, b, name, outcome, k)
        tx = prov.get('taxonomy') or {}
        ok = cls == want_cls and tx.get('rule') == want_rule and bool(tx.get('judgment_call')) == want_j
        if want_code:
            ok = ok and code == want_code
        if cls in O.CACHED_CLASSES:
            ok = ok and isinstance(fwd, dict) and fwd['valid'] == (cls == 'VALID')
        else:
            ok = ok and fwd is None
        by_status.setdefault(st, set()).add(cls)
        rows.append({'case': name, 'driver_status': st, 'class': cls, 'rule': tx.get('rule'), 'code': code,
                     'judgment_call': tx.get('judgment_call'), 'converged': (prov.get('route_a') or {}).get('converged'),
                     'detail_keys': sorted((tx.get('detail') or {}).keys())})
        check('T9.%s' % name, ok, rows[-1])
    check('T9.not_status_alone_ROUTE_A_NO_FIXED_POINT_maps_to_three_classes', by_status.get('ROUTE_A_NO_FIXED_POINT') ==
          {'MODEL_INVALID', 'NUMERICS_LIMITED', 'INFRA'}, {k: sorted(v) for k, v in by_status.items()})
    # C2: without a declaration the non-contracting history is NUMERICS_LIMITED; judgment_call as declared when true
    ctx0 = O.Context(make_config(tdir / 'work0', region, {'use': False}, numerics_block=blk, contraction=None))
    b0 = ctx0.mapper.build(th)
    c0 = _classify_case(tdir, ctx0, b0, 'C2_noncontracting_no_declaration', 'route_a_budget_noncontracting', 4)
    ctxj = O.Context(make_config(tdir / 'workj', region, {'use': False}, numerics_block=blk,
                                 contraction=dict(TEST_DECL, judgment_call=True)))
    bj = ctxj.mapper.build(th)
    cj = _classify_case(tdir, ctxj, bj, 'C2_noncontracting_declared_judgment', 'route_a_budget_noncontracting', 4)
    det = (c0[3].get('taxonomy') or {}).get('detail') or {}
    check('T9.C2_no_declaration_is_numerics_limited_with_history',
          c0[0] == 'NUMERICS_LIMITED' and c0[1] == 'ROUTE_A_ITERATION_BUDGET_EXHAUSTED_NO_DISCRIMINATOR_DECLARED' and
          len(det.get('residual_history') or []) == 8 and len((det.get('contraction') or {}).get('ratios') or []) == 7,
          {'class': c0[0], 'code': c0[1], 'ratios': [round(x, 3) for x in (det.get('contraction') or {}).get('ratios') or []]})
    check('T9.C2_declared_test_states_its_judgment_flag', cj[0] == 'MODEL_INVALID' and
          (cj[3].get('taxonomy') or {}).get('judgment_call') is True, {'class': cj[0], 'jc': (cj[3].get('taxonomy') or {}).get('judgment_call')})
    # C3: no bound declared -> R30 not a judgment call; the per-pass history is recorded either way
    blk_nb = copy.deepcopy(blk)
    blk_nb['picard']['speed_change_bound_km_s'] = None
    ctxn = O.Context(make_config(tdir / 'workn', region, {'use': False}, numerics_block=blk_nb))
    bn = ctxn.mapper.build(th)
    cn = _classify_case(tdir, ctxn, bn, 'C3_nonpositive_no_bound', 'nonpositive_rotation', 4)
    txn = cn[3].get('taxonomy') or {}
    check('T9.C3_no_bound_nonpositive_is_not_a_judgment_call', cn[0] == 'MODEL_INVALID' and txn.get('rule') == 'R30' and
          txn.get('judgment_call') is False and len((txn.get('detail') or {}).get('passes') or []) >= 1,
          {'class': cn[0], 'jc': txn.get('judgment_call'), 'passes': len((txn.get('detail') or {}).get('passes') or [])})
    cb = _classify_case(tdir, ctxn, bn, 'C1_no_bound_ok_is_valid', 'ok', 4)
    check('T9.C1_no_bound_declared_completed_is_valid', cb[0] == 'VALID', {'class': cb[0], 'code': cb[1]})
    # R39: the stage binding refuses the per-call geometry (mock of c2v008 + gal_c2v004)
    vg = mock_variant('STAGE_REGISTERED_ONLY', stage='REGISTERED_ONLY')
    ctxg = O.Context(make_config(tdir / 'workg', region, {'use': False}, numerics_block=blk, driver=vg))
    corner = {nm: ctxg.es['trial_values'][nm] for nm in ctxg.es['names']}
    corner['distance_Mpc'] = ctxg.es['upper']['distance_Mpc']
    bg = ctxg.mapper.build(corner)
    cg = _classify_case(tdir, ctxg, bg, 'R39_geometry_blocked', 'ok', 4, driver=vg)
    check('T9.R39_stage_binding_geometry_gap_is_infra_never_invalid', cg[0] == 'INFRA' and
          (cg[3].get('taxonomy') or {}).get('rule') == 'R39' and ctxg.taxonomy.never_invalid_code(cg[1]),
          {'class': cg[0], 'code': cg[1], 'status': cg[4]})
    with open(tdir / 'T9_MATRIX.json', 'x') as fh:
        json.dump(rows, fh, indent=1)


def t10_deciding(region):
    tdir = RUN_DIR / 'T10'
    tdir.mkdir()
    M = monitor_mod()
    good = make_deciding(MOCK_PATH)
    g = O.check_deciding(good, sha(MOCK_PATH), M, synthetic=True)
    check('T10.deciding_gate.good_both_parts', g['ok'] is True and g['route_a_column_workers_verified'] == 8,
          {'reasons': g['reasons'][:1], 'N': g.get('route_a_column_workers_verified')})
    cases = []
    cases.append(('absent', None))
    cases.append(('only_i', dict(good, ii_full_anchor=None)))
    cases.append(('only_ii', dict(good, i_admit_prefix=None)))
    cases.append(('i_verdict_FAIL', make_deciding(MOCK_PATH, mut_i={'deciding_test': {'verdict': 'FAIL'}})))
    cases.append(('i_iteration_5', make_deciding(MOCK_PATH, mut_i={'route_a_outcome': {'converged_iteration': 5}})))
    cases.append(('i_attempt_link_other', make_deciding(MOCK_PATH, mut_i={'identity': {'route_a': {'custody': {
        'attempt_link': {'identity_sha256': '0' * 64}}}}})))
    cases.append(('i_profile_other', make_deciding(MOCK_PATH, mut_i={'identity': {'route_a': {'custody': {
        'source_profile_sha256': '1' * 64}}}})))
    cases.append(('i_geometry_key', make_deciding(MOCK_PATH, mut_i={'geometry': {'distance_Mpc': 4.1}})))
    cases.append(('i_solver_other', make_deciding(MOCK_PATH, mut_i={'identity': {'route_a': {'custody': {
        'solver_code': {'sha256': '2' * 64}}}}})))
    x = copy.deepcopy(good)
    x['i_admit_prefix']['result']['sha256'] = '3' * 64
    cases.append(('i_result_pin_mismatch', x))
    x = copy.deepcopy(good)
    d = fixture_dir('finish_tamper')
    (d / 'finish.json').write_text(json.dumps({'result_sha256': '4' * 64}))
    x['i_admit_prefix']['finish_path'] = str(d / 'finish.json')
    cases.append(('i_finish_mismatch', x))
    x = copy.deepcopy(good)
    x['i_admit_prefix']['receipt']['sha256'] = '5' * 64
    cases.append(('i_receipt_pin_mismatch', x))
    cases.append(('ii_verdict_FAIL', make_deciding(MOCK_PATH, mut_ii={'verdict': 'FAIL', 'failing': ['SPEEDS']})))
    cases.append(('ii_check_missing', make_deciding(MOCK_PATH, mut_ii={'checks': {'NEW_CUSTODY': {'pass': False}}})))
    cases.append(('ii_comparator_other', make_deciding(MOCK_PATH, mut_ii={'comparator': {'sha256': '6' * 64}})))
    cases.append(('ii_new_not_result_dir', make_deciding(MOCK_PATH, mut_ii={'new': '/nonexistent/other_run'})))
    cases.append(('ii_column_workers_mismatch', make_deciding(MOCK_PATH, mut_ii={'column_workers': 4})))
    cases.append(('ii_expect_new_serial', make_deciding(MOCK_PATH, mut_ii={'expect_new': 'serial'})))
    cases.append(('ii_reference_other', make_deciding(MOCK_PATH, mut_ii={'reference': '/x/OTHER_RUN'})))
    x = copy.deepcopy(good)
    x['ii_full_anchor']['compare_report']['sha256'] = '7' * 64
    cases.append(('ii_report_pin_mismatch', x))
    cases.append(('other_driver', good))
    for name, dt in cases:
        drv_sha = sha(TAX_PATH) if name == 'other_driver' else sha(MOCK_PATH)
        g = O.check_deciding(dt, drv_sha, M, synthetic=True)
        check('T10.deciding_gate_refuses.%s' % name, g['ok'] is False, {'reasons': [r[:120] for r in g['reasons'][:2]]})
    g = O.check_deciding(good, sha(MOCK_PATH), M, synthetic=False)
    check('T10.synthetic_expect_refused_outside_synthetic', g['ok'] is False and 'synthetic' in json.dumps(g['reasons']),
          {'reasons': g['reasons'][:1]})
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test',
                      deciding=dict(good, ii_full_anchor=None))
    ctx = O.Context(cfg)
    res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(BASE_CONTROL)), log=lambda m: None).run()
    check('T10.C5_run_refuses_with_only_one_deciding_test', res['status'] == 'REFUSED' and not (tdir / 'work').exists()
          and res['gates']['deciding_test']['ok'] is False, {'status': res['status']})


def t11_numerics_gate(region):
    tdir = RUN_DIR / 'T11'
    tdir.mkdir()
    blk = c2r_like()
    blk8 = dict(copy.deepcopy(blk), route_a={'column_workers': 8})
    blk4 = dict(copy.deepcopy(blk), route_a={'column_workers': 4})
    for name, ncfg, N, want in (('null', None, 8, False), ('no_artifact', make_numerics(blk, tamper='no_artifact'), 8, False),
                                ('artifact_sha_mismatch', make_numerics(blk, tamper='sha'), 8, False),
                                ('pointer_unresolved', make_numerics(blk, tamper='bad_pointer'), 8, False),
                                ('pointer_block_mismatch', make_numerics(blk, tamper='pointer_mismatch'), 8, False),
                                ('C8_attestation_only_not_verified', make_numerics(blk, attest=True), 8, False),
                                ('pointer_equal', make_numerics(blk), 8, True),
                                ('C8_route_a_override_N8_covered', make_numerics(blk8, artifact_block=blk), 8, True),
                                ('C8_route_a_override_N4_not_covered', make_numerics(blk4, artifact_block=blk), 8, False),
                                ('C8_route_a_override_without_deciding_ii', make_numerics(blk8, artifact_block=blk), None, False),
                                ('C8_route_a_serial_explicit', make_numerics(dict(copy.deepcopy(blk), route_a={'column_workers': 1}),
                                                                             artifact_block=blk), None, True),
                                ('C8_column_workers_differs_from_artifact',
                                 make_numerics(dict(copy.deepcopy(blk), column_workers=4), artifact_block=blk), 8, False)):
        _, g = O.check_numerics(ncfg, TEMPLATE['numerics'], N)
        check('T11.numerics_gate.%s' % name, g['ok'] is want, {'reasons': g['reasons'][:1], 'binding': g.get('binding')})
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics=make_numerics(blk, tamper='sha'),
                      executor='in_process_test')
    ctx = O.Context(cfg)
    res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(BASE_CONTROL)), log=lambda m: None).run()
    check('T11.run_refuses_unpinned_numerics', res['status'] == 'REFUSED' and res['gates']['numerics_verdict']['ok'] is False,
          {'status': res['status']})
    cfg = make_config(tdir / 'w2', region, {'use': False}, numerics_block=blk)
    cfg['column_workers'] = 1
    try:
        O.Context(cfg)
        r = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        r = str(exc)
    check('T11.C8_top_level_column_workers_key_refused', "(extra: ['column_workers'])" in r, {'reason': r[-80:]})
    cfg = make_config(tdir / 'w3', region, {'use': False}, numerics=make_numerics(blk8, artifact_block=blk))
    ctx = O.Context(cfg)
    check('T11.C8_run_numerics_equal_verified_block_plus_recorded_override',
          ctx.numerics == blk8 and ctx.gates['numerics_verdict']['execution_overrides'].get('route_a', {}).get('run') ==
          {'column_workers': 8} and ctx.weights['peak'] == 8, {'weights': ctx.weights,
                                                               'binding': ctx.gates['numerics_verdict']['binding'][:120]})


def t12_a7(region):
    tdir = RUN_DIR / 'T12'
    tdir.mkdir()
    ctx = O.Context(make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like()))
    th = ctx.E.to_natural(spec=ctx.es, u=[0.5] * ctx.n_varying)['theta_natural']
    good = ctx.mapper.build(th)['spec']
    bad_keys = ['05', '٥', '+1', ' 1', '1.0', '', '00', '¹']
    out = {}
    for bk in bad_keys:
        for where in ('fs_absolute_overrides', 'rfs_factor_overrides'):
            s = copy.deepcopy(good)
            s['numerics']['brackets']['rule'][where][bk] = [0.8, 1.2]
            try:
                ctx.prelaunch_check(s)
                out['%s[%r]' % (where, bk)] = 'NOT REFUSED'
            except O.OrchestratorError as exc:
                out['%s[%r]' % (where, bk)] = 'A7' if 'A7_GUARD' in str(exc) else 'other: %s' % exc
    for name, tab in (('pass_key', {'01': {'5': [0.8, 1.1]}}), ('nested_index', {'1': {'07': [0.8, 1.1]}})):
        s = copy.deepcopy(good)
        s['numerics']['brackets']['rule']['le_factor_overrides'] = tab
        try:
            ctx.prelaunch_check(s)
            out['le_factor_overrides.%s' % name] = 'NOT REFUSED'
        except O.OrchestratorError as exc:
            out['le_factor_overrides.%s' % name] = 'A7' if 'A7_GUARD' in str(exc) else 'other: %s' % exc
    check('T12.override_key_lint_refuses_noncanonical', all(v == 'A7' for v in out.values()), out)
    deep = O.lint_override_keys({'le_factor_overrides': {'1': {'3': {'05': [0.8, 1.1]}}}})
    clean = O.lint_override_keys({'le_factor_overrides': {'1': {'3': [0.8, 1.1]}}, 'x': {'05': 1}})
    check('T12.L6_lint_at_every_depth', len(deep) == 1 and "'05'" in deep[0] and clean == [], {'deep': deep, 'clean': clean})
    s = copy.deepcopy(good)
    s['coefficients']['path'] = 'relative/coefficients.npz'
    try:
        ctx.prelaunch_check(s)
        rel = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        rel = str(exc)[:100]
    cfg = make_config(tdir / 'w2', region, {'use': False}, numerics_block=c2r_like())
    cfg['work_dir'] = 'relative/work'
    try:
        O.Context(cfg)
        wd = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        wd = str(exc)[:100]
    blk = c2r_like()
    blk['brackets']['rule']['fs_absolute_overrides']['07'] = [1.0, 2.0]
    try:
        O.Context(make_config(tdir / 'w3', region, {'use': False}, numerics_block=blk))
        base = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        base = str(exc)[:100]
    check('T12.absolute_paths_and_base_lint', 'A7_GUARD' in rel and 'A7_ABSOLUTE_PATH' in wd and 'A7_GUARD' in base,
          {'relative_coefficients': rel, 'relative_work_dir': wd, 'base_block_bad_key': base})
    d = fixture_dir('recovery_bad')
    rp = d / 'BAD_RULE.json'
    rp.write_text(json.dumps({'brackets': {'mode': 'rule', 'rule': {'fs_absolute_overrides': {'05': [1, 2]}}}}))
    ctx2 = O.Context(make_config(tdir / 'w4', region, {'use': False}, numerics_block=c2r_like(),
                                 recovery_rules=[dict(pin(rp), rule_id='BAD')]))
    try:
        ctx2.recovery_rule(str(rp))
        rr = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        rr = str(exc)[:100]
    try:
        ctx2.recovery_rule('/not/allowlisted.json')
        al = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        al = str(exc)[:100]
    check('T12.recovery_rule_lint_and_allowlist', 'A7_GUARD' in rr and 'allowlist' in al, {'bad_key': rr, 'not_listed': al})


def t13_capability(region):
    tdir = RUN_DIR / 'T13'
    tdir.mkdir()
    variant = mock_variant('DISTANCE_REGISTERED_ONLY', distance='REGISTERED_ONLY')
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like(), driver=variant,
                      executor='in_process_test')
    ctx = O.Context(cfg)
    cap = ctx.gates['driver_capability']
    check('T13.layer1_refuses_distance_registered_only_normalizer', cap['ok'] is False and cap['n_points'] == 17 and
          cap['n_accepted'] == 1 and len(cap['refused']) == 16 and all('UNSUPPORTED geometry' in r['reason'] for r in cap['refused']),
          {'n_accepted': cap['n_accepted'], 'n_refused': len(cap['refused'])})
    res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(BASE_CONTROL)), log=lambda m: None).run()
    check('T13.run_refuses_on_capability_gap', res['status'] == 'REFUSED' and not (tdir / 'work').exists(),
          {'status': res['status']})
    ctx2 = O.Context(make_config(tdir / 'w2', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test'))
    ctx2.synthetic = False                      # unit check of the non-synthetic branch (no evidence pinned)
    cap2 = ctx2.capability_probe()
    check('T13.non_synthetic_without_run_mode_evidence_fails', cap2['ok'] is False and cap2['layer2_run_mode'] == 'UNVERIFIED'
          and 'RUN_MODE_ADMISSION_UNVERIFIED' in cap2['reasons'][0], {'reasons': cap2['reasons'][:1]})


def t14_crash_windows(region):
    class _CrashCommit(O.Orchestrator):
        def _commit_plan(self, wd, plan):
            for c in plan['calls']:
                O.append_jsonl(self.ledger_path, {'wave': plan['wave'], 'call_index': c['call_index'], 'key': c['key'],
                                                  'spec_sha256': c['spec_sha256'], 'utc': O.utc()})
            raise SystemExit('SIMULATED_CRASH_AFTER_LEDGER_BEFORE_PLAN_COMMIT')

    class _CrashFinal(O.Orchestrator):
        def _write_final(self, summary):
            raise SystemExit('SIMULATED_CRASH_AFTER_RECORD_BEFORE_FINAL_SUMMARY')
    tdir = RUN_DIR / 'T14'
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    fwd = spec_forward_factory(control)
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test')
    ctx = O.Context(cfg)
    crashed = None
    try:
        _CrashCommit(ctx, O.InProcessExecutor(ctx, fwd), log=lambda m: None).run(max_waves=None)
    except SystemExit as exc:
        crashed = str(exc)
    o2 = O.Orchestrator(O.Context(cfg), O.InProcessExecutor(ctx, fwd), log=lambda m: None)
    res = o2.run()
    led_lines = O.read_jsonl(tdir / 'work' / 'LAUNCH_LEDGER.jsonl')
    committed = o2.launches()
    check('T14.F3_crash_between_ledger_and_plan', crashed is not None and res.get('status') == 'COMPLETE' and
          res.get('n_planless_wave_dirs') == 1 and all(v == 1 for v in committed.values()) and
          len(led_lines) == sum(committed.values()) + 1,
          {'crashed': crashed, 'status': res.get('status'), 'planless': res.get('n_planless_wave_dirs')})
    cfg2 = make_config(tdir / 'work2', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test')
    ctx2 = O.Context(cfg2)
    crashed2 = None
    try:
        _CrashFinal(ctx2, O.InProcessExecutor(ctx2, fwd), log=lambda m: None).run()
    except SystemExit as exc:
        crashed2 = str(exc)
    res2 = O.Orchestrator(O.Context(cfg2), O.InProcessExecutor(ctx2, fwd), log=lambda m: None).run()
    recs = sorted((tdir / 'work2' / 'records').glob('CALIBRATION_RECORD_*.json'))
    reg = O.read_jsonl(tdir / 'work2' / 'records' / 'CALIBRATION_REGISTRY.jsonl')
    check('T14.F3_no_duplicate_record_after_crash_before_summary', crashed2 is not None and res2.get('status') == 'COMPLETE'
          and len(recs) == 1 and len(reg) == 1 and (res2.get('record') or {}).get('reused_existing_record') is True
          and (res2.get('record') or {}).get('verify_ok') is True,
          {'crashed': crashed2, 'n_records': len(recs), 'n_registry_lines': len(reg)})


def t15_orphans(region):
    tdir = RUN_DIR / 'T15'
    tdir.mkdir()
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like())
    ctx = O.Context(cfg)
    orc = O.Orchestrator(ctx, log=lambda m: None)
    orc.prepare(create=True)              # v004 F3: a populated work dir needs its WORK_DIR.json (written by prepare)
    ex = orc.executor
    th = ctx.E.to_natural(spec=ctx.es, u=[0.5] * ctx.n_varying)['theta_natural']
    b = ctx.mapper.build(th)
    wd = tdir / 'work' / 'waves' / 'wave_0001'
    d = wd / 'campaign' / 'call_0000'
    d.mkdir(parents=True)
    (d / 'spec.json').write_bytes(b['raw'])
    dummy = subprocess.Popen([PY, '-I', '-B', '-c', 'import time; time.sleep(120)', str(d / 'spec.json')])
    time.sleep(1.0)
    o1 = ex.orphans(wd / 'campaign')
    plan = {'wave': 1, 'calls': [{'key': b['key'], 'theta': th, 'call_index': 0}]}
    O.write_json_x(wd / 'WAVE_PLAN.json', plan)
    O.append_jsonl(tdir / 'work' / 'LAUNCH_LEDGER.jsonl', {'wave': 1, 'call_index': 0, 'key': b['key'], 'utc': O.utc()})
    tok = O.halt_token(ctx.cache_id, 1, b['key'], 0, 'INFRA', 'CAMPAIGN_DIR_EXISTS_UNVERIFIED', 1)
    O.write_json_x(wd / 'HALT.json', {'wave': 1, 'items': [{'key': b['key'], 'call_index': 0, 'class': 'INFRA',
                                                            'reason': 'CAMPAIGN_DIR_EXISTS_UNVERIFIED', 'token': tok,
                                                            'provenance': {'call_dir': str(d)}}]})
    try:
        orc.resolve(1, 'retry', 'TEST', tokens=[tok])
        r1 = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        r1 = str(exc)[:120]
    dummy.kill()
    dummy.wait()
    time.sleep(0.5)
    o2 = ex.orphans(wd / 'campaign')
    r2 = orc.resolve(1, 'retry', 'TEST after the stray process ended', tokens=[tok])
    check('T15.F4_orphan_without_launch_record_detected_by_process_scan',
          len(o1) == 1 and o1[0]['alive'] is True and o1[0]['launch_record'] is False and o1[0]['live_processes'] and
          len(o2) == 1 and o2[0]['alive'] is None,
          {'before': {k: o1[0][k] for k in ('alive', 'launch_record')}, 'after_alive': o2[0]['alive']})
    check('T15.F4_resolve_retry_refused_while_process_alive', r1.startswith('F4') and r2['status'] == 'OK' and
          len(r2['resolved']) == 1, {'while_alive': r1, 'after': r2['status']})


def t16_disk(region):
    tdir = RUN_DIR / 'T16'
    tdir.mkdir()
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test',
                      disk_guard={'reserve_bytes': 1 << 62, 'per_call_bytes': 8 << 30, 'measured_per_call_bytes': 6081118006})
    ctx = O.Context(cfg)
    orc = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(BASE_CONTROL)), log=lambda m: None)
    res = orc.run()
    st = orc.status()
    pl = orc.plan_only()
    f = st['disk']
    check('T16.halted_disk_and_forecast_fields', res['status'] == 'HALTED_DISK' and f['calls_affordable_now_guard'] == 0
          and 'next_wave_fits' in pl['disk'] and pl['disk']['next_wave_fits'] is False,
          {'status': res['status'], 'disk': {k: f[k] for k in ('free_bytes', 'calls_affordable_now_guard')}})
    cfg2 = make_config(tdir / 'work2', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test',
                       disk_guard={'reserve_bytes': 0, 'per_call_bytes': 8 << 30, 'measured_per_call_bytes': 6081118006})
    f2 = O.Context(cfg2).disk_forecast(4)
    check('T16.calls_affordable_now', f2['calls_affordable_now_guard'] == f2['free_bytes'] // (8 << 30) and
          f2['calls_affordable_now_measured'] == f2['free_bytes'] // 6081118006, {k: f2[k] for k in ('free_bytes', 'next_wave_fits')})
    out = {}
    for name, dg in (('zero', {'per_call_bytes': 0, 'reserve_bytes': 0}), ('negative', {'per_call_bytes': -5, 'reserve_bytes': 0}),
                     ('below_output_cap', {'per_call_bytes': 1 << 20, 'reserve_bytes': 0}),
                     ('missing', None), ('negative_reserve', {'per_call_bytes': 64 << 20, 'reserve_bytes': -1})):
        c = make_config(tdir / ('w_%s' % name), region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test')
        c['disk_guard'] = dg
        try:
            O.Context(c)
            out[name] = 'NOT REFUSED'
        except O.OrchestratorError as exc:
            out[name] = 'refused'
    c = make_config(tdir / 'w_cap0', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test')
    c['per_call']['output_cap_bytes'] = 0
    try:
        O.Context(c)
        out['output_cap_zero'] = 'NOT REFUSED'
    except O.OrchestratorError:
        out['output_cap_zero'] = 'refused'
    check('T16.L2_disk_guard_cannot_be_disabled', all(v == 'refused' for v in out.values()), out)


def t17_numerics_limited(region, anchor):
    tdir = RUN_DIR / 'T17'
    tdir.mkdir()
    blk = c2r_like()
    rule_dir = fixture_dir('recovery_rule')
    rp = rule_dir / 'SYNTHETIC_RECOVERY_RULE.json'
    rb = copy.deepcopy(blk['brackets'])
    blk['brackets']['rule']['fs_absolute_overrides']['5'] = [302500000.0, 317625000.0]
    rb['rule']['fs_absolute_overrides']['5'] = [MK.RECOVERY_LO, 317625000.0]
    rp.write_text(json.dumps({'brackets': rb, 'invocation': 'SYNTHETIC_R1', 'reason': 'test'}, indent=1))
    control = copy.deepcopy(BASE_CONTROL)
    control['outcome_rules'] = [{'if': 'z_lt', 'value': -0.3, 'outcome': 'fs_column:MASS_ENTHALPY_NOT_BRACKETED'}]
    cpath = write_control(FIX / 'control_T17.json', control)
    cfg = make_config(tdir / 'work', region, anchor, numerics_block=blk, recovery_rules=[dict(pin(rp), rule_id='SYNTHETIC_R1')])
    cp = save_config(cfg, 'T17_CONFIG.json')
    code1, out1 = cli('run', cp, cpath)
    halt = out1.get('halt') or []
    check('T17.numerics_limited_halts_not_cached', code1 == 11 and out1.get('status') == 'HALTED_NUMERICS' and halt and
          all(h['class'] == 'NUMERICS_LIMITED' and h['reason'].startswith('COLUMN_FAILED:fs:MASS_ENTHALPY') for h in halt),
          {'exit': code1, 'status': out1.get('status'), 'n_halt': len(halt)})
    if code1 != 11:
        return
    code2, out2 = cli('run', cp, cpath)
    rounds, codes, status, wave = 0, [], None, out1['wave']
    while rounds < 20:
        code_r, out_r = resolve_all(cp, cpath, tdir / 'work', wave, 'retry_with_recovery', 'TEST: D7-style recovery',
                                    ['--recovery', str(rp)])
        codes.append(code_r)
        code_n, out_n = cli('run', cp, cpath)
        rounds += 1
        status = out_n.get('status')
        if status != 'HALTED_NUMERICS':
            break
        wave = out_n['wave']
    orc = O.Orchestrator(O.Context(cfg), log=lambda m: None)
    orc.cache.open(create=False)
    led = orc.launches()
    rec_entries = [e for e in orc.cache.entries.values() if (e.get('provenance') or {}).get('recovery')]
    plans = [json.loads(p.read_text()) for p in sorted((tdir / 'work' / 'waves').glob('wave_*/WAVE_PLAN.json'))]
    rec_calls = [c for p in plans for c in p['calls'] if c.get('recovery')]
    ok = (code2 == 7 and status == 'COMPLETE' and all(cc == 0 for cc in codes) and rec_entries and
          all(e['classification'] == 'VALID' and led[e['key']] == 2 for e in rec_entries) and
          all(c['spec']['numerics']['brackets']['rule']['fs_absolute_overrides']['5'][0] == MK.RECOVERY_LO for c in rec_calls)
          and all(c['authorized_by'] for c in rec_calls) and all(v in (1, 2) for v in led.values()))
    check('T17.retry_with_recovery_relaunches_with_rule_brackets_and_token', ok,
          {'unresolved_exit': code2, 'final_status': status, 'resolve_rounds': rounds, 'n_recovered_entries': len(rec_entries),
           'n_recovery_calls': len(rec_calls), 'max_launches': max(led.values())})
    tdir2 = RUN_DIR / 'T17b'
    tdir2.mkdir()
    cfg2 = make_config(tdir2 / 'work', region, anchor, numerics_block=blk)
    cp2 = save_config(cfg2, 'T17b_CONFIG.json')
    c1, o1 = cli('run', cp2, cpath)
    ok2 = c1 == 11
    if ok2:
        cr, orr = resolve_all(cp2, cpath, tdir2 / 'work', o1['wave'], 'invalid', 'TEST: root declares invalid')
        orc2 = O.Orchestrator(O.Context(cfg2), log=lambda m: None)
        orc2.cache.open(create=False)
        es = [orc2.cache.entries.get(h['key']) for h in o1['halt']]
        ok2 = cr == 0 and all(e and e['classification'] == 'MODEL_INVALID' and e['source'] == 'ROOT_RESOLUTION' and
                              e['failure_class'].startswith('ROOT_DECLARED_INVALID_AFTER_NUMERICS_LIMITED') for e in es)
    check('T17.resolve_invalid_on_numerics_limited', ok2, {'run_exit': c1})


def t18_unknown_e2e(region, anchor):
    tdir = RUN_DIR / 'T18'
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    control['outcome_rules'] = [{'if': 'x_gt', 'value': -10.0, 'outcome': 'weird_status'}]
    cpath = write_control(FIX / 'control_T18.json', control)
    cfg = make_config(tdir / 'work', region, anchor, numerics_block=c2r_like())
    cp = save_config(cfg, 'T18_CONFIG.json')
    code, out = cli('run', cp, cpath)
    h = out.get('halt') or []
    check('T18.unknown_status_end_to_end_halts_infra', code == 4 and h and h[0]['class'] == 'INFRA' and
          h[0]['provenance']['taxonomy']['rule'] == 'DEFAULT' and not list((tdir / 'work' / 'cache').glob('*/entries/*.json')),
          {'exit': code, 'reason': h[0]['reason'] if h else None})


def t19_concurrency(region):
    tdir = RUN_DIR / 'T19'
    tdir.mkdir()
    blk8 = dict(c2r_like(), route_a={'column_workers': 8})
    for name, mc, pb, nc, blk, want in (('8calls_budget17_on_18', 8, 17, 18, None, True),
                                        ('budget18_refused', 6, 18, 18, None, False),
                                        ('budget_above_n_cores', 6, 12, 8, None, False),
                                        ('max_concurrent_above_budget', 13, 12, 18, None, False),
                                        ('route_a8_peak_above_budget', 2, 6, 18, blk8, False),
                                        ('route_a8_budget17_ok', 4, 17, 18, blk8, True),
                                        ('12calls_budget12', 12, 12, 18, None, True)):
        try:
            if blk is not None:
                O.Context(make_config(tdir / name, region, {'use': False},
                                      numerics=make_numerics(blk, artifact_block=c2r_like()), max_concurrent=mc,
                                      process_budget=pb, n_cores=nc))
            else:
                O.Context(make_config(tdir / name, region, {'use': False}, numerics_block=c2r_like(), max_concurrent=mc,
                                      process_budget=pb, n_cores=nc))
            got = True
            why = None
        except O.OrchestratorError as exc:
            got = False
            why = str(exc)[:100]
        check('T19.concurrency.%s' % name, got is want, {'accepted': got, 'why': why})


def t20_plan_output(region, anchor):
    ctx = O.Context(make_config(RUN_DIR / 'T20' / 'work', region, anchor, numerics_block=c2r_like()))
    pl = O.Orchestrator(ctx).plan_only()
    check('T20.plan_reports_gates_disk_addendum_work_dir', pl['gates_ok'] is True and set(pl['gates']) ==
          {'numerics_verdict', 'deciding_test', 'driver_capability'} and 'calls_affordable_now_guard' in pl['disk'] and
          'D5' in pl['open_items_from_addendum'] and not (RUN_DIR / 'T20' / 'work').exists() and pl['process_budget'] == 12
          and pl['work_dir']['configured'] == str(RUN_DIR / 'T20' / 'work'),
          {'gates_ok': pl['gates_ok'], 'next_wave_calls': pl['next_wave']['n_calls']})


def t21_c7(region):
    tdir = RUN_DIR / 'T21'
    tdir.mkdir()
    out = {}
    for name, drv in (('real_v008', V008), ('no_marker_copy', mock_variant('NO_MARKER', marker=False))):
        try:
            O.Context(make_config(tdir / name, region, {'use': False}, numerics_block=c2r_like(), driver=drv,
                                  deciding={'i_admit_prefix': None, 'ii_full_anchor': None}))
            out[name] = 'NOT REFUSED'
        except O.OrchestratorError as exc:
            out[name] = str(exc)[:90]
    tax = json.loads(TAX_PATH.read_text())
    fake = fixture_dir('tax_points_to_mock') / 'FAILURE_TAXONOMY_FOR_MOCK.json'
    fake.write_text(json.dumps(dict(tax, driver=pin(MOCK_PATH))))
    c = make_config(tdir / 'tax', region, {'use': False}, numerics_block=c2r_like())
    c['taxonomy'] = pin(fake)
    try:
        O.Context(c)
        out['taxonomy_driver'] = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        out['taxonomy_driver'] = str(exc)[:90]
    check('T21.C7_synthetic_refused_with_real_or_unmarked_driver', all(v.startswith('C7_') for v in out.values()), out)


def t22_m1_crash_windows(region, control_path, anchor, ref_sha):
    tdir = RUN_DIR / 'T22'
    tdir.mkdir()
    rows = []
    for window in ('put:1', 'put:3', 'put:9', 'link_unlink:2', 'link_unlink:6', 'before_wave_result:3'):
        tag = window.replace(':', '_')
        cfg = make_config(tdir / tag / 'work', region, anchor, numerics_block=c2r_like())
        cp = save_config(cfg, 'T22_%s_CONFIG.json' % tag)
        env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
        env['CAL_ORCH_MOCK_CONTROL'] = str(control_path)
        p = subprocess.run([PY, '-I', '-B', str(CRASH_RUNNER), str(ORCH_PATH), str(cp), window], env=env,
                           capture_output=True, text=True)
        code, out = cli('run', cp, control_path)
        ctx = O.Context(cfg)
        led = O.Orchestrator(ctx, log=lambda m: None).launches()
        rows.append({'window': window, 'crash_exit': p.returncode, 'rerun_exit': code, 'status': out.get('status'),
                     'sha_equal': (out.get('replay') or {}).get('run_canonical_sha256') == ref_sha,
                     'max_launches': max(led.values()) if led else None,
                     'tmp_left': len(list((tdir / tag / 'work').glob('cache/*/entries/.*.tmp')))})
        check('T22.M1_crash_%s_rerun_completes_identically' % tag, p.returncode == 77 and code == 0 and
              out.get('status') == 'COMPLETE' and rows[-1]['sha_equal'] and rows[-1]['max_launches'] == 1, rows[-1])
    # a halting wave: crash right after HALT.json is linked, then rerun -> the same halt, then a token resolve -> complete
    control = copy.deepcopy(BASE_CONTROL)
    control['outcome_rules'] = [{'if': 'z_lt', 'value': -0.3, 'outcome': 'fs_column:MASS_ENTHALPY_NOT_BRACKETED'}]
    cpath = write_control(FIX / 'control_T22_halt.json', control)
    blk = c2r_like()
    blk['brackets']['rule']['fs_absolute_overrides']['5'] = [302500000.0, 317625000.0]
    cfg = make_config(tdir / 'halt_linked' / 'work', region, anchor, numerics_block=blk)
    cp = save_config(cfg, 'T22_halt_linked_CONFIG.json')
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    env['CAL_ORCH_MOCK_CONTROL'] = cpath
    p = subprocess.run([PY, '-I', '-B', str(CRASH_RUNNER), str(ORCH_PATH), str(cp), 'halt_linked'], env=env,
                       capture_output=True, text=True)
    halts = sorted((tdir / 'halt_linked' / 'work' / 'waves').glob('wave_*/HALT.json'))
    sha_before = sha(halts[-1]) if halts else None
    code, out = cli('run', cp, cpath)
    wr = halts[-1].parent / 'WAVE_RESULT.json' if halts else None
    check('T22.M1_crash_after_halt_linked_rerun_reports_the_same_halt', p.returncode == 77 and code == 11 and
          halts and sha(halts[-1]) == sha_before and wr.is_file() and out.get('wave') == halts[-1].parent.name,
          {'crash_exit': p.returncode, 'rerun_exit': code, 'halt_unchanged': bool(halts) and sha(halts[-1]) == sha_before})


def t23_m2_tokens(region, anchor):
    tdir = RUN_DIR / 'T23'
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    control['outcome_rules'] = [{'if': 'z_lt', 'value': -0.3, 'outcome': 'fs_column:MASS_ENTHALPY_NOT_BRACKETED'}]
    cpath = write_control(FIX / 'control_T23.json', control)
    blk = c2r_like()
    blk['brackets']['rule']['fs_absolute_overrides']['5'] = [302500000.0, 317625000.0]
    work = tdir / 'work'
    cfg = make_config(work, region, anchor, numerics_block=blk)
    cp = save_config(cfg, 'T23_CONFIG.json')
    c1, o1 = cli('run', cp, cpath)
    w1 = o1.get('wave')
    toks = [h['token'] for h in o1.get('halt') or []]
    keys = [h['key'] for h in o1.get('halt') or []]
    w1n = str(int(w1.split('_')[1])) if w1 else '0'
    cb, ob = cli('resolve', cp, cpath, ['--wave', w1n, '--token', '9' * 64, '--decision', 'retry', '--reason', 'bogus'])
    cw, ow = cli('resolve', cp, cpath, ['--wave', w1n, '--all', '--halt-sha256', '0' * 64, '--decision', 'retry', '--reason', 'x'])
    cn, on = cli('resolve', cp, cpath, ['--wave', w1n, '--all', '--decision', 'retry', '--reason', 'x'])
    check('T23.M2_bogus_token_and_wrong_halt_sha_refused', c1 == 11 and cb == 3 and cw == 3 and cn == 3,
          {'run': c1, 'bogus': cb, 'wrong_sha': cw, 'no_sha': cn})
    c2, o2 = resolve_all(cp, cpath, work, w1, 'retry', 'TEST: retry without recovery (fails again)')
    c3, o3 = resolve_all(cp, cpath, work, w1, 'retry', 'TEST: duplicate resolve')
    c3b, o3b = cli('resolve', cp, cpath, ['--wave', w1n, '--token', toks[0], '--decision', 'retry', '--reason', 'dup token'])
    check('T23.M2_duplicate_resolve_refused_nothing_written', c2 == 0 and c3 == 3 and c3b == 3 and
          'TOKEN_ALREADY_USED' in json.dumps(o3) and len(O.read_jsonl(work / 'RESOLUTIONS.jsonl')) == len(toks),
          {'first': c2, 'dup_all': c3, 'dup_token': c3b, 'lines': len(O.read_jsonl(work / 'RESOLUTIONS.jsonl'))})
    c4, o4 = cli('run', cp, cpath)
    w2 = o4.get('wave')
    c5, o5 = cli('run', cp, cpath)
    orc = O.Orchestrator(O.Context(cfg), log=lambda m: None)
    led = orc.launches()
    check('T23.M2_no_relaunch_without_a_fresh_token', c4 == 11 and w2 != w1 and c5 == 7 and all(led[k] == 2 for k in keys),
          {'relaunch_run': c4, 'second_run': c5, 'launches': [led.get(k) for k in keys]})
    c6, o6 = cli('resolve', cp, cpath, ['--wave', w1n, '--token', toks[0], '--decision', 'retry', '--reason', 'stale'])
    check('T23.M2_stale_token_of_an_older_wave_refused', c6 == 3 and 'STALE_TOKEN' in json.dumps(o6),
          {'exit': c6, 'reason': str(o6.get('reasons'))[:200]})
    # L3: a torn RESOLUTIONS tail is skipped; the next resolve still works
    with open(work / 'RESOLUTIONS.jsonl', 'ab') as fh:
        fh.write(b'{"schema":"DDO154_CALIBRATION_RESOL')
    cs, os_ = cli('status', cp, cpath)
    # L5: resolve takes the lock
    dummy = subprocess.Popen([PY, '-I', '-B', '-c', 'import time; time.sleep(60)', 'calibration_orchestrator_c2v004-lock-holder'])
    time.sleep(0.5)
    (work / 'ORCHESTRATOR.lock').write_text(json.dumps({'pid': dummy.pid, 'host': 'otherhost', 'module': O.MODULE_NAME}))
    cl, ol = resolve_all(cp, cpath, work, w2, 'invalid', 'TEST: locked')
    dummy.kill()
    dummy.wait()
    time.sleep(0.3)
    ci, oi = resolve_all(cp, cpath, work, w2, 'invalid', 'TEST: invalid after the second failure')
    check('T23.L3_torn_resolution_line_skipped_and_L5_resolve_locked', cs == 0 and
          sum((os_.get('torn_jsonl_lines_skipped') or {}).values()) >= 1 and cl == 8 and ci == 0,
          {'status_exit': cs, 'torn': os_.get('torn_jsonl_lines_skipped'), 'locked_exit': cl, 'after_unlock': ci})
    status, rounds = None, 0
    while rounds < 20:
        cr, orr = cli('run', cp, cpath)
        status = orr.get('status')
        rounds += 1
        if status != 'HALTED_NUMERICS':
            break
        resolve_all(cp, cpath, work, orr['wave'], 'invalid', 'TEST: invalid')
    led = O.Orchestrator(O.Context(cfg), log=lambda m: None).launches()
    check('T23.M2_campaign_completes_every_key_at_most_twice', status == 'COMPLETE' and max(led.values()) <= 2,
          {'status': status, 'rounds': rounds, 'max_launches': max(led.values())})


def t25_l3_torn(region, anchor, t3_work, control_path):
    tdir = RUN_DIR / 'T25'
    tdir.mkdir()
    dst = tdir / 'work'
    cfg = make_config(dst, region, anchor, numerics_block=c2r_like())
    O.Orchestrator(O.Context(cfg), log=lambda m: None).prepare(create=True)   # v004 F3: the work dir's own WORK_DIR.json
    shutil.copytree(Path(t3_work) / 'cache', dst / 'cache', dirs_exist_ok=True)
    p = sorted((dst / 'cache').glob('*/entries/*.json'))[0]
    raw = p.read_bytes()
    p.write_bytes(raw[:len(raw) // 2])
    cp = save_config(cfg, 'T25_CONFIG.json')
    code, out = cli('status', cp, control_path)
    check('T25.L3_truncated_cache_entry_is_a_refusal_not_a_traceback', code == 3 and out.get('status') == 'REFUSED' and
          'torn or corrupt' in json.dumps(out), {'exit': code, 'reason': str(out.get('reasons'))[:160]})
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    fwd = spec_forward_factory(control)
    cfg2 = make_config(tdir / 'work2', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test')
    ctx = O.Context(cfg2)
    r1 = O.Orchestrator(ctx, O.InProcessExecutor(ctx, fwd), log=lambda m: None).run(max_waves=2)
    with open(tdir / 'work2' / 'LAUNCH_LEDGER.jsonl', 'ab') as fh:
        fh.write(b'{"wave":99,"call_index":0,"key":"tor')
    ctx2 = O.Context(cfg2)
    orc2 = O.Orchestrator(ctx2, O.InProcessExecutor(ctx2, fwd), log=lambda m: None)
    r2 = orc2.run()
    st = orc2.status()
    check('T25.L3_torn_ledger_tail_skipped_run_completes', r1['status'] == 'MAX_WAVES' and r2['status'] == 'COMPLETE' and
          any(v >= 1 for v in st['torn_jsonl_lines_skipped'].values()),
          {'first': r1['status'], 'second': r2['status'], 'torn': st['torn_jsonl_lines_skipped']})


def t26_l4_lock(region, anchor, control_path):
    tdir = RUN_DIR / 'T26'
    tdir.mkdir()
    rows = {}
    for name in ('live_other_host', 'dead_pid', 'live_pid_not_orchestrator'):
        work = tdir / name
        work.mkdir()
        cfg = make_config(work, region, anchor, numerics_block=c2r_like())
        cp = save_config(cfg, 'T26_%s_CONFIG.json' % name)
        dummy = None
        if name == 'live_other_host':
            dummy = subprocess.Popen([PY, '-I', '-B', '-c', 'import time; time.sleep(60)', 'calibration_orchestrator_c2v004-holder'])
            pid = dummy.pid
        elif name == 'dead_pid':
            q = subprocess.Popen([PY, '-I', '-B', '-c', 'pass'])
            q.wait()
            pid = q.pid
        else:
            dummy = subprocess.Popen(['sleep', '60'])
            pid = dummy.pid
        time.sleep(0.3)
        (work / 'ORCHESTRATOR.lock').write_text(json.dumps({'pid': pid, 'host': 'some-other-host', 'module': O.MODULE_NAME}))
        code, out = cli('run', cp, control_path, ['--max-waves', '1'])
        if dummy is not None:
            dummy.kill()
            dummy.wait()
        rows[name] = {'exit': code, 'status': out.get('status'), 'stale_kept': len(list(work.glob('ORCHESTRATOR.lock.stale_*')))}
    check('T26.L4_live_holder_other_host_is_LOCKED', rows['live_other_host']['exit'] == 8, rows['live_other_host'])
    check('T26.L4_dead_holder_is_stale_and_kept_renamed', rows['dead_pid']['status'] == 'MAX_WAVES' and
          rows['dead_pid']['stale_kept'] == 1, rows['dead_pid'])
    check('T26.L4_live_pid_that_is_not_an_orchestrator_is_stale', rows['live_pid_not_orchestrator']['status'] == 'MAX_WAVES',
          rows['live_pid_not_orchestrator'])


def t27_geometry_halt(region):
    tdir = RUN_DIR / 'T27'
    tdir.mkdir()
    vg = mock_variant('STAGE_REGISTERED_ONLY', stage='REGISTERED_ONLY')
    control = copy.deepcopy(BASE_CONTROL)
    cpath = write_control(FIX / 'control_T27.json', control)
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like(), driver=vg)
    cp = save_config(cfg, 'T27_CONFIG.json')
    code, out = cli('run', cp, cpath)
    h = out.get('halt') or []
    check('T27.geometry_gap_halts_infra_R39', code == 4 and h and all(i['provenance']['taxonomy']['rule'] == 'R39' and
                                                                     i['never_resolve_invalid'] for i in h),
          {'exit': code, 'n': len(h), 'reason': h[0]['reason'][:80] if h else None})
    if code != 4:
        return
    ci, oi = resolve_all(cp, cpath, tdir / 'work', out['wave'], 'invalid', 'TEST: must be refused')
    cr, orr = resolve_all(cp, cpath, tdir / 'work', out['wave'], 'retry', 'TEST: retry is allowed')
    check('T27.C11_invalid_refused_for_capability_gap_retry_allowed', ci == 3 and 'INVALID_REFUSED_FOR_DRIVER_CAPABILITY_GAP'
          in json.dumps(oi) and cr == 0, {'invalid_exit': ci, 'retry_exit': cr})


def t28_campaign_budget(region):
    tdir = RUN_DIR / 'T28'
    tdir.mkdir()
    blk4 = dict(c2r_like(), route_a={'column_workers': 4})
    rows = {}
    for aware in (True, False):
        tag = 'aware' if aware else 'conservative'
        control = copy.deepcopy(BASE_CONTROL)
        control.update(route_a_s=1.5, rest_s=1.5, timeline=str(FIX / ('timeline_T28_%s.jsonl' % tag)))
        cpath = write_control(FIX / ('control_T28_%s.json' % tag), control)
        cfg = make_config(tdir / tag / 'work', region, {'use': False}, numerics=make_numerics(blk4, artifact_block=c2r_like()),
                          max_concurrent=4, process_budget=9, stage_aware=aware, deciding_N=4)
        cp = save_config(cfg, 'T28_%s_CONFIG.json' % tag)
        code, out = cli('run', cp, cpath, ['--max-waves', '2'])
        w2 = tdir / tag / 'work' / 'waves' / 'wave_0002'
        wr = json.loads((w2 / 'WAVE_RESULT.json').read_text()) if (w2 / 'WAVE_RESULT.json').is_file() else {}
        camp = wr.get('campaign') or {}
        rows[tag] = {'exit': code, 'status': out.get('status'), 'n_calls_w2': len(wr.get('calls') or []),
                     'max_concurrent_observed': camp.get('max_concurrent_observed'),
                     'max_accounted_processes': camp.get('max_accounted_processes'),
                     'mock_max_actual_weight': max_weight(control['timeline']),
                     'stage_aware': camp.get('stage_aware'), 'process_budget': camp.get('process_budget')}
    a, c = rows['aware'], rows['conservative']
    check('T28.budget_never_exceeded_actual_le_accounted_le_budget',
          all(r['status'] == 'MAX_WAVES' and r['n_calls_w2'] == 4 and r['mock_max_actual_weight'] <= r['max_accounted_processes'] <= 9
              for r in rows.values()), rows)
    check('T28.stage_aware_admits_a_third_call_after_route_a', a['max_concurrent_observed'] >= 3 and
          c['max_concurrent_observed'] == 2, {'aware': a['max_concurrent_observed'], 'conservative': c['max_concurrent_observed']})
    M = monitor_mod()
    base = {'calls': [{'spec': dict(copy.deepcopy(TEMPLATE), numerics=blk4)}], 'per_call': {'wall_cap_s': 5.0,
            'rss_cap_bytes': 1 << 30, 'output_cap_bytes': 1 << 20, 'poll_s': 0.5}, 'campaign_wall_cap_s': 10.0,
            'driver': pin(MOCK_PATH), 'monitor': MONITOR}
    refs = {}
    for name, extra in (('budget_18', {'process_budget': 18, 'max_concurrent': 1}),
                        ('max_concurrent_above_budget', {'process_budget': 3, 'max_concurrent': 4}),
                        ('peak_above_budget', {'process_budget': 3, 'max_concurrent': 1}),
                        ('stage_aware_not_bool', {'process_budget': 9, 'max_concurrent': 1, 'stage_aware': 'yes'})):
        r = CAMP.run_campaign(campaign=dict(base, **extra), campaign_dir=str(tdir / ('refused_%s' % name)), python=PY)
        refs[name] = r['status']
    del M
    check('T28.campaign_c2v003_refusals', all(v == 'REFUSED' for v in refs.values()) and
          not any((tdir / ('refused_%s' % n)).exists() for n in refs), refs)
    w = [CAMP.spec_weights((json.dumps(s) + '\n').encode()) for s in (
        dict(copy.deepcopy(TEMPLATE), numerics=blk4), TEMPLATE,
        dict(copy.deepcopy(TEMPLATE), numerics=blk4, admit={'route_a': {'x': 1}}))]
    check('T28.call_weights_from_spec', w == [(4, 2), (2, 2), (2, 2)], {'weights': w})


def t29_d5(region):
    tdir = RUN_DIR / 'T29'
    tdir.mkdir()
    rows = {}
    for tag, judg in (('plain', False), ('judgment', True)):
        d = tdir / tag
        d.mkdir()
        control = copy.deepcopy(BASE_CONTROL)
        control['sleep_s'] = 0.0
        region2 = write_region(d / 'SYNTHETIC_REGION_NOT_DDO154.json', {'x': 0.0, 'y': 0.0, 'z': 3.0, 'w': 0.0}, control)
        cfg = make_config(d / 'work', region2, {'use': False}, executor='in_process_test', numerics_block=c2r_like())
        ctx = O.Context(cfg)
        res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(control, judgment=judg)), log=lambda m: None).run()
        rows[tag] = {'status': res.get('status'), 'engine_status': res.get('engine_status'), 'D5': res.get('D5_assessment')}
    p, j = rows['plain'], rows['judgment']
    check('T29.C4_D5_condition_met_without_judgment_calls', p['engine_status'] == 'NO_ADMITTED_POINT_FOUND' and
          p['D5']['this_run_meets_tested_negative_condition'] is True and p['D5']['status'].startswith('UNTESTED'),
          {'D5': p['D5']})
    check('T29.C4_judgment_call_model_invalid_keeps_D5_untested', j['engine_status'] == 'NO_ADMITTED_POINT_FOUND' and
          j['D5']['this_run_meets_tested_negative_condition'] is False and j['D5']['n_judgment_call_model_invalid'] > 0,
          {'n_jc': (j['D5'] or {}).get('n_judgment_call_model_invalid')})
    a = O.Orchestrator.d5_assessment('NO_ADMITTED_POINT_FOUND', [{'key': 'k' * 64, 'classification': 'MODEL_INVALID',
                                                                  'source': 'ROOT_RESOLUTION', 'provenance': {}}])
    check('T29.C4_root_declared_invalid_keeps_D5_untested', a['this_run_meets_tested_negative_condition'] is False and
          a['n_root_declared_invalid'] == 1 and O.Orchestrator.d5_assessment('COMPLETE', []) is None, {'a': a['status'][:80]})


def t30_c8_labels(region):
    tdir = RUN_DIR / 'T30'
    tdir.mkdir()
    blk = c2r_like()
    n = make_numerics(blk)
    n['root_attestation'] = 'SYNTHETIC attestation recorded next to a pointer binding'
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics=n, executor='in_process_test')
    ctx = O.Context(cfg)
    res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(control)), log=lambda m: None).run(max_waves=1)
    _, g = O.check_numerics(make_numerics(blk, attest=True), TEMPLATE['numerics'], 8)
    check('T30.C8_binding_labels', ctx.gates['numerics_verdict']['binding'].startswith('BLOCK_EQUALS_ARTIFACT_AT_POINTER') and
          ctx.gates['numerics_verdict']['root_attestation'].startswith('ATTESTED_NOT_VERIFIED') and
          g['binding'] == 'ATTESTED_NOT_VERIFIED' and g['ok'] is False and res['status'] == 'MAX_WAVES',
          {'binding': ctx.gates['numerics_verdict']['binding'][:60], 'attested_only': g['binding']})


def t31_capability_evidence(region, anchor):
    tdir = RUN_DIR / 'T31'
    tdir.mkdir()
    V = load(VERIFY_PATH, 'verify4_under_test')
    rows = {}
    for tag, stage in (('ANY', 'ANY'), ('STAGE_REGISTERED_ONLY', 'REGISTERED_ONLY')):
        drv = mock_variant('EVIDENCE_%s' % tag, stage=stage)
        cfg = make_config(tdir / tag / 'work', region, anchor, numerics_block=c2r_like(), driver=drv)
        cp = save_config(cfg, 'T31_%s_CONFIG.json' % tag)
        ev = V.main(str(cp), str(tdir / tag / 'evidence'), use_guard=True)
        doc = json.loads(Path(ev).read_text())
        cfg2 = copy.deepcopy(cfg)
        cfg2['capability_evidence'] = pin(ev)
        ctx = O.Context(cfg2)
        cap = ctx.gates['driver_capability']
        rows[tag] = {'counts': doc['counts'], 'only_declared_raw': doc['only_declared_fields_change_raw'],
                     'only_declared_norm': doc['only_declared_fields_change_normalized'],
                     'guard_denials': doc['guard_denials_total'], 'gate_ok': cap['ok'], 'layer2': cap['layer2_run_mode'],
                     'run_mode_refused': len(cap.get('run_mode_refused') or [])}
    a, r = rows['ANY'], rows['STAGE_REGISTERED_ONLY']
    check('T31.evidence_builder_guarded_dry_runs', all(x['guard_denials'] == 0 and x['only_declared_raw'] and x['only_declared_norm']
                                                      and x['counts']['corners'] == 16 for x in rows.values()), rows)
    check('T31.layer2_admits_when_the_stage_binding_admits', a['gate_ok'] is True and a['layer2'] == 'ADMITTED', a)
    check('T31.layer2_refuses_the_16_corners_like_c2v008', r['gate_ok'] is False and r['layer2'] == 'REFUSED' and
          r['run_mode_refused'] == 16, r)
    drv = mock_variant('EVIDENCE_ANY', stage='ANY')
    cfg3 = make_config(tdir / 'other_base' / 'work', region, anchor, numerics_block=dict(c2r_like(), column_workers=1),
                       driver=drv)
    cfg3['capability_evidence'] = pin(tdir / 'ANY' / 'evidence' / 'DRIVER_CAPABILITY_EVIDENCE_V001.json')
    cap3 = O.Context(cfg3).gates['driver_capability']
    check('T31.evidence_of_another_base_spec_refused', cap3['ok'] is False and 'not for this driver / base spec' in
          json.dumps(cap3['reasons']), {'reasons': [x[:100] for x in cap3['reasons']]})


def t32_work_dir(region):
    tdir = RUN_DIR / 'T32'
    tdir.mkdir()
    target = tdir / 'EXTERNAL_TARGET'
    target.mkdir()
    link = tdir / 'runs_ext_link'
    os.symlink(str(target), str(link))
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    cfg = make_config(link / 'WORK_V003', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test')
    ctx = O.Context(cfg)
    res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(control)), log=lambda m: None).run(max_waves=1)
    wrec = json.loads((target / 'WORK_V003' / 'WORK_DIR.json').read_text()) if (target / 'WORK_V003' / 'WORK_DIR.json').is_file() else {}
    check('T32.work_dir_through_symlink_resolved_and_recorded', res['status'] == 'MAX_WAVES' and
          (target / 'WORK_V003' / 'LAUNCH_LEDGER.jsonl').is_file() and wrec.get('resolved') == os.path.realpath(str(target / 'WORK_V003'))
          and wrec.get('symlinks') and ctx.disk_forecast(1)['free_bytes_read_at'].startswith(os.path.realpath(str(target))),
          {'status': res['status'], 'resolved': wrec.get('resolved'), 'links': len(wrec.get('symlinks') or [])})
    dang = tdir / 'dangling_link'
    os.symlink(str(tdir / 'NOT_MOUNTED_VOLUME' / 'x'), str(dang))
    out = {}
    for name, wd, vol in (('dangling', dang / 'WORK', None), ('not_on_volume', link / 'W2', '/Volumes/External1'),
                          ('volume_not_mount', link / 'W3', str(target))):
        c = make_config(wd, region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test', volume=vol)
        try:
            O.Context(c)
            out[name] = 'NOT REFUSED'
        except O.OrchestratorError as exc:
            out[name] = str(exc)[:60]
    check('T32.dangling_link_off_volume_and_non_mount_refused', out['dangling'].startswith('WORK_DIR_DANGLING_SYMLINK') and
          out['not_on_volume'].startswith('WORK_DIR_NOT_ON_VOLUME') and out['volume_not_mount'].startswith('WORK_DIR_VOLUME_NOT_MOUNTED'), out)
    real = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext/DDO154_CALIBRATION_ORCH_V004'
    r = O.resolve_work_dir(real, '/Volumes/External1')
    check('T32.real_runs_ext_path_resolves_onto_External1_read_only', r['resolved'].startswith('/Volumes/External1/') and
          r['volume'] == '/Volumes/External1' and not os.path.exists(r['resolved']),
          {'resolved': r['resolved'], 'existing_ancestor': r['existing_ancestor']})


def t33_real_anchor_bytes():
    """C1/C2/C3/C6 on the REAL A2 anchor call directory (read-only; driver c2v001 record = the c2v008 stage layout)."""
    run = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs/A2_ANCHOR_F10_RUN_V001')
    raw = TAX_PATH.read_bytes()
    tax = O.Taxonomy(json.loads(raw), O.sha256_bytes(raw), TEST_DECL)
    res = json.loads((run / 'result.json').read_bytes())
    rows = sorted(res['speeds_km_s'])
    ev = O.collect_evidence(run, res, rows, tax)
    hist = (ev.get('route_a') or {}).get('residual_history') or []
    as_is = tax.classify(res, ev)
    r2 = copy.deepcopy(res)
    r2['picard_bound_met'] = True                      # the field c2v008 records (DRV L2834); the final change is 0.00908
    v = tax.classify(r2, ev)
    r3 = copy.deepcopy(r2)
    r3['passes'][-1]['max_abs_change_km_s'] = 0.02     # inconsistent with the flag -> not VALID
    ev3 = O.collect_evidence(run, r3, rows, tax)
    inc = tax.classify(r3, ev3)
    c = tax.contraction(hist)
    check('T33.real_anchor_residual_history_decoded', not ev['errors'] and [round(h['residual_J'] / h['bound_J'], 2) for h in hist]
          == [16.81, 8.09, 3.89, 1.87, 0.89] and c['verdict'] == 'CONTRACTING',
          {'ratios': [round(x, 3) for x in c['ratios']], 'n_files': len(ev['files'])})
    check('T33.C1_real_record_without_flag_is_R03_with_flag_is_R01_inconsistent_is_R03',
          as_is['rule'] == 'R03' and v['rule'] == 'R01' and v['class'] == 'VALID' and inc['rule'] == 'R03',
          {'as_is': as_is['rule'], 'with_flag': v['rule'], 'inconsistent': inc['rule']})


# ======================================================================================================= v004 blocks
TRUTH3 = {'x': 0.30, 'y': -0.10, 'z': 0.15, 'w': 0.0}


def t34_s1(region, anchor):
    """S1: positive passes then a nonpositive final pass under a declared bound -> NUMERICS_LIMITED halt with the pass
    history; nothing cached; root confirms an invalid through resolve (ROOT_RESOLUTION)."""
    tdir = RUN_DIR / 'T34'
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    control['outcome_rules'] = [{'if': 'x_gt', 'value': -10.0, 'outcome': 'nonpositive_rotation'}]
    cpath = write_control(FIX / 'control_T34.json', control)
    cfg = make_config(tdir / 'work', region, anchor, numerics_block=c2r_like())
    cp = save_config(cfg, 'T34_CONFIG.json')
    code, out = cli('run', cp, cpath)
    h = out.get('halt') or []
    det = ((h[0]['provenance'].get('taxonomy') or {}).get('detail') or {}) if h else {}
    ph = (h[0]['provenance'].get('passes_history') or []) if h else []
    cached = list((tdir / 'work' / 'cache').glob('*/entries/*.json'))
    check('T34.S1_unconverged_nonpositive_iterate_halts_numerics_with_pass_history',
          code == 11 and out.get('status') == 'HALTED_NUMERICS' and h and
          all(i['class'] == 'NUMERICS_LIMITED' and i['reason'] == 'FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED' and
              i['provenance']['taxonomy']['rule'] == 'R30' and i['provenance']['taxonomy']['judgment_call'] is True and
              not i['never_resolve_invalid'] for i in h) and not cached and
          [x['rotation_positive'] for x in ph][:-1] and all(x['rotation_positive'] is True for x in ph[:-1]) and
          ph[-1]['rotation_positive'] is False and det.get('positive_passes') == [x['pass'] for x in ph[:-1]],
          {'exit': code, 'status': out.get('status'), 'reason': h[0]['reason'] if h else None,
           'pass_flags': [x['rotation_positive'] for x in ph], 'positive_passes': det.get('positive_passes'),
           'n_cached': len(cached)})
    if code != 11:
        return
    cr, orr = resolve_all(cp, cpath, tdir / 'work', out['wave'], 'invalid', 'TEST: root confirms the iterate is final')
    orc = O.Orchestrator(O.Context(cfg), log=lambda m: None)
    orc.cache.open(create=False)
    es = [orc.cache.entries.get(i['key']) for i in h]
    check('T34.S1_root_confirmation_is_a_root_resolution',
          cr == 0 and all(e and e['source'] == 'ROOT_RESOLUTION' and e['classification'] == 'MODEL_INVALID' and
                          e['failure_class'] == 'ROOT_DECLARED_INVALID_AFTER_NUMERICS_LIMITED:FINAL_PICARD_ITERATE_'
                                                'NONPOSITIVE_UNCONVERGED' for e in es) and
          O.Orchestrator.d5_assessment('NO_ADMITTED_POINT_FOUND', es)['this_run_meets_tested_negative_condition'] is False,
          {'resolve_exit': cr, 'failure_classes': sorted(set(e['failure_class'] for e in es if e))})
    # all passes nonpositive -> MODEL_INVALID (cached, judgment call); unreadable history -> INFRA
    tax = O.Taxonomy(json.loads(TAX_PATH.read_bytes()), sha(TAX_PATH), TEST_DECL)
    base_ev = {'picard': {'bound_declared': True, 'bound_km_s': 0.01}, 'files': {}, 'errors': [], 'row_ids': ROWS}
    rows = {}
    for name, flags in (('all_false', [False, False, False]), ('one_true', [True, False, False]),
                        ('last_only', [True, True, False]), ('non_bool', ['true', False]), ('none', [None, False]),
                        ('empty', [])):
        hist = [{'pass': i + 1, 'rotation_positive': f} for i, f in enumerate(flags)]
        ev = dict(base_ev, passes_history=hist, final_pass={'rotation_positive': False})
        r = tax.classify({'status': 'COMPLETED_INVALID', 'reasons': ['final column mean did not return 12 rows']}, ev)
        rows[name] = (r['class'], r['rule'], r['code'])
    nb = dict(base_ev, picard={'bound_declared': False}, passes_history=[{'pass': 1, 'rotation_positive': True}],
              final_pass={'rotation_positive': False})
    rows['no_bound_one_true'] = tuple(tax.classify({'status': 'COMPLETED_INVALID', 'reasons': []}, nb)[k]
                                      for k in ('class', 'rule', 'code'))
    want = {'all_false': ('MODEL_INVALID', 'R30', 'FINAL_PASS_NONPOSITIVE_ROTATION_SQUARE'),
            'one_true': ('NUMERICS_LIMITED', 'R30', 'FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED'),
            'last_only': ('NUMERICS_LIMITED', 'R30', 'FINAL_PICARD_ITERATE_NONPOSITIVE_UNCONVERGED'),
            'non_bool': ('INFRA', 'R30', 'FINAL_PASS_NONPOSITIVE_PASS_HISTORY_UNREADABLE'),
            'none': ('INFRA', 'R30', 'FINAL_PASS_NONPOSITIVE_PASS_HISTORY_UNREADABLE'),
            'empty': ('INFRA', 'R30', 'FINAL_PASS_NONPOSITIVE_PASS_HISTORY_UNREADABLE'),
            'no_bound_one_true': ('MODEL_INVALID', 'R30', 'FINAL_PASS_NONPOSITIVE_ROTATION_SQUARE')}
    check('T34.S1_rule_matrix_model_invalid_only_without_any_positive_pass', rows == want,
          {k: list(v) for k, v in rows.items()})


def t35_s2(region):
    tdir = RUN_DIR / 'T35'
    tdir.mkdir()
    tax = json.loads(TAX_PATH.read_text())
    out = {}
    for t in (0.4, 1e-9, 0.999999, 1.0, 1.02, 3, float('inf'), True):
        try:
            O.validate_contraction_test(dict(TEST_DECL, threshold=t), tax)
            out[repr(t)] = 'accepted'
        except O.OrchestratorError as exc:
            out[repr(t)] = 'refused' if '>= 1' in str(exc) else 'refused: %s' % exc
    check('T35.S2_threshold_below_1_refused', out == {'0.4': 'refused', '1e-09': 'refused', '0.999999': 'refused',
                                                     '1.0': 'accepted', '1.02': 'accepted', '3': 'accepted',
                                                     'inf': 'refused', 'True': 'refused'}, out)
    try:
        O.Context(make_config(tdir / 'w', region, {'use': False}, numerics_block=c2r_like(),
                              contraction=dict(TEST_DECL, threshold=0.4, n_last=2)))
        r = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        r = str(exc)[:120]
    check('T35.S2_config_with_threshold_0p4_refused', 'S2' in r, {'reason': r})
    tx = O.Taxonomy(tax, sha(TAX_PATH), dict(TEST_DECL, threshold=1.0, n_last=2))
    hist = [{'residual_J': 400.0 * 0.48 ** i, 'bound_J': 1.0} for i in range(8)]
    c = tx.contraction(hist)
    check('T35.S2_contracting_history_is_contracting_at_threshold_1', c['verdict'] == 'CONTRACTING',
          {'ratios': [round(x, 3) for x in c['ratios']][-3:], 'verdict': c['verdict']})


def t36_s3(region, anchor):
    tdir = RUN_DIR / 'T36'
    tdir.mkdir()
    ctl = copy.deepcopy(BASE_CONTROL)
    ctl.update(force_outcome='picard_bound_not_met', sleep_s=0.0)
    cbad = write_control(FIX / 'control_T36_anchor_bound_not_met.json', ctl)
    bad_anchor = make_anchor_fixture(cbad, tag='BOUND_NOT_MET')
    ctx_b = O.Context(make_config(tdir / 'work_bad', region, bad_anchor))           # template numerics: alias eligible
    try:
        O.Orchestrator(ctx_b).plan_only()
        r = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        r = str(exc)
    check('T36.S3_alias_of_a_non_R01_anchor_result_refused', r.startswith('S3') and 'R03' in r, {'reason': r[:160]})
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    cfg = make_config(tdir / 'work', region, anchor, executor='in_process_test')
    ctx = O.Context(cfg)
    orc = O.Orchestrator(ctx, O.InProcessExecutor(ctx, spec_forward_factory(control)), log=lambda m: None)
    res = orc.run(max_waves=0)
    ents = [(p, json.loads(p.read_text())) for p in sorted((tdir / 'work' / 'cache').glob('*/entries/*.json'))]
    al = [(p, e) for p, e in ents if e['source'] == 'ANCHOR_ALIAS']
    ok0 = (res['status'] == 'MAX_WAVES' and len(al) == 1 and al[0][1]['provenance']['taxonomy']['rule'] == 'R01'
           and al[0][1]['provenance']['evidence_files'])
    check('T36.S3_alias_entry_carries_its_R01_classification', ok0,
          {'status': res['status'], 'n_alias': len(al), 'rule': al[0][1]['provenance']['taxonomy']['rule'] if al else None})
    if not al:
        return
    p, e = al[0]
    raw = p.read_bytes()
    e2 = copy.deepcopy(e)
    e2['provenance']['evidence_files'] = {k: '0' * 64 for k in e2['provenance']['evidence_files']}
    _rehash(e2)
    p.write_text(json.dumps(e2))
    try:
        O.Cache(O.Context(cfg)).open(create=False)
        r2 = 'ACCEPTED'
    except O.OrchestratorError as exc:
        r2 = 'REFUSED: %s' % exc
    e3 = copy.deepcopy(e)
    e3['provenance']['taxonomy']['rule'] = 'R03'
    _rehash(e3)
    p.write_text(json.dumps(e3))
    try:
        O.Cache(O.Context(cfg)).open(create=False)
        r3 = 'ACCEPTED'
    except O.OrchestratorError as exc:
        r3 = 'REFUSED: %s' % exc
    p.write_bytes(raw)                                    # test-owned entry restored
    try:
        O.Cache(O.Context(cfg)).open(create=False)
        r4 = 'ACCEPTED'
    except O.OrchestratorError as exc:
        r4 = 'REFUSED: %s' % exc
    check('T36.S3_alias_verify_reclassifies_on_open', r2.startswith('REFUSED') and 'S3' in r2 and
          r3.startswith('REFUSED') and 'S3' in r3 and r4 == 'ACCEPTED',
          {'evidence_tamper': r2[:120], 'taxonomy_tamper': r3[:120], 'restored': r4})


def t37_s4(region):
    M = monitor_mod()
    good = make_deciding(MOCK_PATH)
    g = O.check_deciding(good, sha(MOCK_PATH), M, synthetic=True)
    ii = g['parts'].get('ii_full_anchor') or {}
    check('T37.S4_good_pair_passes_with_bytes_recorded', g['ok'] is True and ii.get('comparator_sha256_from_bytes') == SYN_COMP
          and ii.get('reference_result_sha256_from_bytes'), {'reasons': g['reasons'][:1]})
    cases = []
    cases.append(('comparator_file_other_bytes_same_claimed_sha', make_deciding(MOCK_PATH, comp_bytes=b'# other bytes\n')))
    other = fixture_dir('other_reference') / 'A2_ANCHOR_F10_RUN_V001'
    other.mkdir()
    (other / 'result.json').write_bytes(b'{"synthetic_reference_result": true}\n')     # same bytes, other place
    cases.append(('reference_same_name_and_bytes_elsewhere', make_deciding(MOCK_PATH, mut_ii={'reference': str(other)})))
    cases.append(('reference_result_bytes_differ', make_deciding(MOCK_PATH, ref_result_bytes=b'{"stale": true}\n')))
    cases.append(('comparator_path_missing', make_deciding(MOCK_PATH, mut_ii={'comparator': {'path': '/nonexistent/c.py'}})))
    cases.append(('comparator_path_relative', make_deciding(MOCK_PATH, mut_ii={'comparator': {'path': 'c.py'}})))
    x = copy.deepcopy(good)
    x['ii_full_anchor']['comparator'] = {'path': str(Path(json.loads(Path(good['ii_full_anchor']['compare_report']['path'])
                                                                     .read_text())['comparator']['path'])), 'sha256': '8' * 64}
    cases.append(('config_comparator_pin_wrong_sha', x))
    rows = {}
    for name, dt in cases:
        r = O.check_deciding(dt, sha(MOCK_PATH), M, synthetic=True)
        rows[name] = {'ok': r['ok'], 'S4': 'S4' in json.dumps(r['reasons'])}
    check('T37.S4_deciding_ii_bytes_checks_refuse', all(v['ok'] is False and v['S4'] for v in rows.values()), rows)
    y = copy.deepcopy(good)
    rp = json.loads(Path(good['ii_full_anchor']['compare_report']['path']).read_text())
    y['ii_full_anchor']['comparator'] = {'path': rp['comparator']['path'], 'sha256': SYN_COMP}
    gy = O.check_deciding(y, sha(MOCK_PATH), M, synthetic=True)
    check('T37.S4_config_comparator_pin_of_the_right_bytes_accepted', gy['ok'] is True, {'reasons': gy['reasons'][:1]})
    ex = O.DECIDING_EXPECT['ii_full_anchor']
    real_ref_sha = sha(Path(ex['reference_path']) / 'result.json')
    check('T37.S4_real_reference_pin_matches_the_anchor_bytes', real_ref_sha == ex['reference_result_sha256'] and
          sha(ART / 'driver_v008_c2/deciding/compare_deciding_ii_c2v008.py') == ex['comparator_sha256'],
          {'reference_result_sha256': real_ref_sha[:16]})


def t38_f1(region):
    tdir = RUN_DIR / 'T38'
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    cpath = write_control(FIX / 'control_T38.json', control)
    cfg = make_config(tdir / 'work', region, {'use': False}, numerics_block=c2r_like())
    cp = save_config(cfg, 'T38_CONFIG.json')
    code, out = cli('run', cp, cpath, ['--max-waves', '1'])

    def opened():
        try:
            O.Cache(O.Context(cfg)).open(create=False)
            return 'ACCEPTED'
        except O.OrchestratorError as exc:
            return 'REFUSED: %s' % exc
    ents = [(p, json.loads(p.read_text())) for p in sorted((tdir / 'work' / 'cache').glob('*/entries/*.json'))]
    v = [(p, e) for p, e in ents if e['classification'] == 'VALID' and e['source'] == 'WAVE']
    base = opened()
    check('T38.F1_wave_entry_records_receipt_and_finish_pins', code == 6 and v and base == 'ACCEPTED' and
          v[0][1]['provenance'].get('finish', {}).get('sha256') and v[0][1]['provenance'].get('receipt_file_sha256'),
          {'exit': code, 'n_valid': len(v), 'open': base})
    if not v:
        return
    p, e = v[0]
    pv = e['provenance']
    res_p, rec_p = Path(pv['result_path']), Path(pv['receipt_path'])
    fin_p = res_p.parent / 'finish.json'
    raw_e, raw_r, raw_rec, raw_f = p.read_bytes(), res_p.read_bytes(), rec_p.read_bytes(), fin_p.read_bytes()
    rows = {}
    # C6x4: result speeds edited, entry result pin + forward + self-hash made consistent
    res = json.loads(raw_r)
    k0 = sorted(res['speeds_km_s'])[0]
    res['speeds_km_s'][k0] += 7.0
    new_raw = (json.dumps(res, indent=1, sort_keys=True) + '\n').encode()
    res_p.write_bytes(new_raw)
    e2 = copy.deepcopy(e)
    e2['provenance']['result_sha256'] = O.sha256_bytes(new_raw)
    e2['forward']['speeds_km_s'][k0] += 7.0
    _rehash(e2)
    p.write_text(json.dumps(e2))
    rows['C6x4_result_and_entry_consistently_forged'] = opened()
    res_p.write_bytes(raw_r)
    p.write_bytes(raw_e)
    # finish.json no longer names the result
    fin = json.loads(raw_f)
    fin['result_sha256'] = '9' * 64
    fin_p.write_text(json.dumps(fin))
    rows['finish_unbound'] = opened()
    fin_p.write_bytes(raw_f)
    # receipt file bytes changed (self-hash recomputed would still change the file sha)
    rec_p.write_bytes(raw_rec + b'\n')
    rows['receipt_file_changed'] = opened()
    rec_p.write_bytes(raw_rec)
    # entry receipt self-hash field forged
    e3 = copy.deepcopy(e)
    e3['provenance']['receipt_sha256_self'] = '1' * 64
    _rehash(e3)
    p.write_text(json.dumps(e3))
    rows['entry_receipt_self_hash_forged'] = opened()
    p.write_bytes(raw_e)
    rows['restored'] = opened()
    check('T38.F1_receipt_and_finish_reverified_on_open',
          all(v_.startswith('REFUSED') and 'F1' in v_ for k, v_ in rows.items() if k != 'restored') and
          rows['restored'] == 'ACCEPTED', {k: v_[:110] for k, v_ in rows.items()})
    d = fixture_dir('finish_unit')
    (d / 'result.json').write_bytes(b'{}')
    a = O.finish_binding(d / 'result.json', O.sha256_bytes(b'{}'))
    (d / 'finish.json').write_text(json.dumps({'result_sha256': O.sha256_bytes(b'{}'), 'result_path': str(d / 'result.json')}))
    b = O.finish_binding(d / 'result.json', O.sha256_bytes(b'{}'))
    check('T38.F1_classify_time_finish_binding', a == (None, 'FINISH_JSON_MISSING') and b[1] is None and b[0]['sha256'],
          {'missing': a[1], 'bound': b[1]})


LOCK_STRESS = r"""
import importlib.util, os, sys, time
sp = importlib.util.spec_from_file_location('orch4_lock_stress', sys.argv[1])
O = importlib.util.module_from_spec(sp); sp.loader.exec_module(O)
work, log, n = sys.argv[2], sys.argv[3], int(sys.argv[4])
got = 0
for i in range(n):
    L = O.Lock(work)
    if L.acquire():
        fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644); os.write(fd, ('A %d\n' % os.getpid()).encode()); os.close(fd)
        time.sleep(0.002)
        fd = os.open(log, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644); os.write(fd, ('R %d\n' % os.getpid()).encode()); os.close(fd)
        L.release(); got += 1
print(got)
"""


def t39_f2(region, control_path):
    tdir = RUN_DIR / 'T39'
    tdir.mkdir()
    rows = {}
    w = tdir / 'empty_fresh'
    w.mkdir()
    (w / 'ORCHESTRATOR.lock').write_bytes(b'')
    rows['empty_fresh_LOCKED'] = O.Lock(w).acquire() is False
    cfg = make_config(w, region, {'use': False}, numerics_block=c2r_like())
    code, out = cli('run', save_config(cfg, 'T39_empty_fresh.json'), control_path, ['--max-waves', '1'])
    rows['empty_fresh_cli_exit_8'] = code == 8
    w2 = tdir / 'garbage_fresh'
    w2.mkdir()
    (w2 / 'ORCHESTRATOR.lock').write_bytes(b'{"pid": 12')
    rows['unparseable_fresh_LOCKED'] = O.Lock(w2).acquire() is False
    w3 = tdir / 'empty_old'
    w3.mkdir()
    (w3 / 'ORCHESTRATOR.lock').write_bytes(b'')
    t_old = time.time() - 2 * O.LOCK_EMPTY_LIVE_S
    os.utime(w3 / 'ORCHESTRATOR.lock', (t_old, t_old))
    L3 = O.Lock(w3)
    a3 = L3.acquire()
    body = json.loads((w3 / 'ORCHESTRATOR.lock').read_text())
    rows['empty_old_taken_over_stale_kept'] = (a3 is True and body['pid'] == os.getpid() and
                                               len(list(w3.glob('ORCHESTRATOR.lock.stale_*'))) == 1)
    L3.release()

    class RacingLock(O.Lock):                    # a contender judges a dead lock stale; a winner replaces it meanwhile
        def _judge(self):
            st, raw = O.Lock._judge(self)
            live = O.canonical({'pid': os.getppid(), 'module': O.MODULE_NAME, 'cmd_marker': 'python'})
            self.path.write_bytes(live)
            return st, raw
    w4 = tdir / 'toctou'
    w4.mkdir()
    q = subprocess.Popen([PY, '-I', '-B', '-c', 'pass'])
    q.wait()
    (w4 / 'ORCHESTRATOR.lock').write_bytes(O.canonical({'pid': q.pid, 'module': O.MODULE_NAME}))
    a4 = RacingLock(w4).acquire()
    now = (w4 / 'ORCHESTRATOR.lock').read_bytes() if (w4 / 'ORCHESTRATOR.lock').exists() else None
    rows['toctou_moved_live_lock_restored_LOCKED'] = a4 is False and now is not None and json.loads(now)['pid'] == os.getppid()
    w5 = tdir / 'stress'
    w5.mkdir()
    script = FIX / 'lock_stress_c2v004.py'
    script.write_text(LOCK_STRESS)
    log = tdir / 'stress_log.txt'
    procs = [subprocess.Popen([PY, '-I', '-B', str(script), str(ORCH_PATH), str(w5), str(log), '60'],
                              stdout=subprocess.PIPE, text=True) for _ in range(3)]
    gots = [int(pp.communicate(timeout=900)[0].strip() or 0) for pp in procs]
    seq = [ln.split() for ln in log.read_text().splitlines()] if log.is_file() else []
    holder, viol = None, 0
    for ev, pid in seq:
        if ev == 'A':
            if holder is not None:
                viol += 1
            holder = pid
        else:
            if holder != pid:
                viol += 1
            holder = None
    rows['stress_3_contenders_never_two_holders'] = viol == 0 and sum(gots) == len(seq) // 2 and sum(gots) > 0
    check('T39.F2_atomic_lock', all(rows.values()), dict(rows, stress_acquisitions=gots, stress_violations=viol))


def t40_f3(region, control_path):
    tdir = RUN_DIR / 'T40'
    tdir.mkdir()
    ta, tb = tdir / 'TARGET_A', tdir / 'TARGET_B_EMPTY'
    ta.mkdir()
    tb.mkdir()
    la, lb = tdir / 'runs_ext_a', tdir / 'runs_ext_b'
    os.symlink(str(ta), str(la))
    os.symlink(str(tb), str(lb))
    pin_a = O.work_dir_identity_core(O.resolve_work_dir(str(la / 'WORK'), None))
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    fwd = spec_forward_factory(control)
    cfg = make_config(la / 'WORK', region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test',
                      work_dir_identity=pin_a)
    ctx = O.Context(cfg)
    res = O.Orchestrator(ctx, O.InProcessExecutor(ctx, fwd), log=lambda m: None).run(max_waves=1)
    wj = json.loads((ta / 'WORK' / 'WORK_DIR.json').read_text())
    check('T40.F3_pinned_work_dir_runs_and_records_identity', res['status'] == 'MAX_WAVES' and
          wj.get('work_dir_st_ino') == os.stat(ta / 'WORK').st_ino and 'volume_uuid' in wj and
          wj['symlinks'][0]['target'] == str(ta), {'status': res['status'], 'ino': wj.get('work_dir_st_ino')})
    # (b) the link now leads to another (empty) directory: refused by every command, nothing created there
    cfg_b = make_config(lb / 'WORK', region, {'use': False}, numerics_block=c2r_like(), work_dir_identity=pin_a)
    cpb = save_config(cfg_b, 'T40_repointed.json')
    codes = {}
    for cmd, extra in (('plan', []), ('status', []), ('run', []),
                       ('resolve', ['--wave', '1', '--token', '0' * 64, '--decision', 'retry', '--reason', 'x'])):
        c, o = cli(cmd, cpb, control_path, extra)
        codes[cmd] = (c, 'WORK_DIR_REPOINTED' in json.dumps(o))
    check('T40.F3_repointed_link_refused_by_plan_status_run_resolve', all(v == (3, True) for v in codes.values()) and
          not (tb / 'WORK').exists(), {k: list(v) for k, v in codes.items()})
    # (c) a copy of the tree under another path with its own correct pin: WORK_DIR.json identity differs
    tc = tdir / 'TARGET_C'
    shutil.copytree(str(ta / 'WORK'), str(tc / 'WORK'), symlinks=True)
    pin_c = O.work_dir_identity_core(O.resolve_work_dir(str(tc / 'WORK'), None))
    cfg_c = make_config(tc / 'WORK', region, {'use': False}, numerics_block=c2r_like(), work_dir_identity=pin_c)
    cpc = save_config(cfg_c, 'T40_copied.json')
    codes = {}
    for cmd, extra in (('plan', []), ('status', []), ('run', []),
                       ('resolve', ['--wave', '1', '--token', '0' * 64, '--decision', 'retry', '--reason', 'x'])):
        c, o = cli(cmd, cpc, control_path, extra)
        codes[cmd] = (c, 'WORK_DIR.json identity differs' in json.dumps(o))
    n_waves_c = len(list((tc / 'WORK' / 'waves').glob('wave_*')))
    check('T40.F3_copied_tree_refused_by_WORK_DIR_json_in_plan_status_run_resolve',
          all(v == (3, True) for v in codes.values()) and n_waves_c == 1, {k: list(v) for k, v in codes.items()})
    # (d) a populated work dir without WORK_DIR.json; (e) a forged inode
    td = tdir / 'TARGET_D' / 'WORK'
    (td / 'waves').mkdir(parents=True)
    pin_d = O.work_dir_identity_core(O.resolve_work_dir(str(td), None))
    try:
        O.Orchestrator(O.Context(make_config(td, region, {'use': False}, numerics_block=c2r_like(),
                                             work_dir_identity=pin_d))).plan_only()
        rd = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        rd = str(exc)
    te = tdir / 'TARGET_E' / 'WORK'
    pin_e = O.work_dir_identity_core(O.resolve_work_dir(str(te), None))
    cfg_e = make_config(te, region, {'use': False}, numerics_block=c2r_like(), executor='in_process_test',
                        work_dir_identity=pin_e)
    ctx_e = O.Context(cfg_e)
    O.Orchestrator(ctx_e, O.InProcessExecutor(ctx_e, fwd), log=lambda m: None).run(max_waves=0)
    wje = json.loads((te / 'WORK_DIR.json').read_text())
    wje['work_dir_st_ino'] = int(wje['work_dir_st_ino']) + 1
    (te / 'WORK_DIR.json').write_text(json.dumps(wje))
    try:
        O.Orchestrator(O.Context(cfg_e), O.InProcessExecutor(ctx_e, fwd), log=lambda m: None).status()
        re_ = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        re_ = str(exc)
    check('T40.F3_populated_without_record_and_forged_inode_refused', 'no WORK_DIR.json' in rd and
          'WORK_DIR.json identity differs' in re_, {'populated': rd[:100], 'inode': re_[:100]})
    # (f) volume identity; (g) a non-synthetic config needs the pin
    uuid_root = O.volume_uuid('/')
    tv = tdir / 'TARGET_V' / 'WORK'
    rec_v = O.resolve_work_dir(str(tv), '/')
    pv = O.work_dir_identity_core(rec_v)
    out = {}
    for name, pinv in (('right_uuid', pv), ('wrong_uuid', dict(pv, volume_uuid='00000000-0000-0000-0000-000000000000')),
                       ('uuid_not_pinned', dict(pv, volume_uuid=None))):
        try:
            O.Context(make_config(tv, region, {'use': False}, numerics_block=c2r_like(), volume='/',
                                  work_dir_identity=pinv))
            out[name] = 'accepted'
        except O.OrchestratorError as exc:
            out[name] = str(exc)[:90]
    c_ns = make_config(tdir / 'NS' / 'WORK', region, {'use': False}, numerics_block=c2r_like())
    c_ns['synthetic_test'] = False
    try:
        O.Context(c_ns)
        ns = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        ns = str(exc)[:90]
    check('T40.F3_volume_uuid_pinned_and_compared_and_required_outside_tests',
          isinstance(uuid_root, str) and out['right_uuid'] == 'accepted' and
          'WORK_DIR_VOLUME_IDENTITY_MISMATCH' in out['wrong_uuid'] and 'NOT_PINNED' in out['uuid_not_pinned'] and
          ns.startswith('F3: work_dir_identity'), dict(out, non_synthetic_without_pin=ns, uuid_root=uuid_root))


def t41_a13(region4, anchor):
    tdir = RUN_DIR / 'T41'
    tdir.mkdir()
    control = copy.deepcopy(BASE_CONTROL)
    control['sleep_s'] = 0.0
    region3 = write_region(tdir / 'SYNTHETIC_REGION_3D_NOT_DDO154.json', TRUTH3, control)
    cfg3 = make_config(tdir / 'w3', region3, {'use': False}, numerics_block=c2r_like(), executor='in_process_test',
                       mode='3D')
    ctx3 = O.Context(cfg3)
    ctx4 = O.Context(make_config(tdir / 'w4', region3, {'use': False}, numerics_block=c2r_like(), executor='in_process_test'))
    cap = ctx3.gates['driver_capability']
    pts = ctx3.probe_points()
    diff = [(a['name'], k) for a, b in zip(ctx4.engine_coordinates, ctx3.engine_coordinates) for k in a if a[k] != b[k]]
    check('T41.A13_three_free_coordinates_distance_fixed_at_4p04',
          list(ctx3.es['varying_names']) == ['common_scale_s', 'gamma_over_Eref', 'ell_F_m'] and
          'distance_Mpc' in ctx3.es['fixed_names'] and ctx3.es['trial_values']['distance_Mpc'] == 4.04 and
          cap['ok'] and cap['n_points'] == 9 and all(th['distance_Mpc'] == 4.04 for _, th in pts) and
          diff == [('distance_Mpc', 'role')] and ctx3.cache_id != ctx4.cache_id and
          ctx3.es['lower']['distance_Mpc'] == ctx4.es['lower']['distance_Mpc'],
          {'varying': ctx3.es['varying_names'], 'n_points': cap['n_points'], 'diff_vs_4d': diff})
    th = ctx3.E.to_natural(spec=ctx3.es, u=[0.5] * ctx3.n_varying)['theta_natural']
    t2 = dict(th, distance_Mpc=4.05)
    try:
        ctx3.mapper.build(t2)
        rm = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        rm = str(exc)[:90]
    check('T41.A13_mapper_refuses_a_distance_off_4p04', 'fixed coordinate distance_Mpc' in rm, {'reason': rm})
    rows = []
    for name, truth, override in (('main', TRUTH3, None), ('no_admitted_point', {'x': 0.0, 'y': 0.0, 'z': 3.0, 'w': 0.0}, None),
                                  ('budget40', TRUTH3, {'budget': 40}),
                                  ('budget120_rounds3', TRUTH3, {'max_march_rounds': 3, 'hull_growth_tol': 0.007,
                                                                 'budget': 120})):
        d = tdir / ('inproc_%s' % name)
        d.mkdir()
        rg = write_region(d / 'SYNTHETIC_REGION_NOT_DDO154.json', truth, control)
        c = make_config(d / 'work', rg, {'use': False}, numerics_block=c2r_like(), executor='in_process_test', mode='3D',
                        override=override)
        cx = O.Context(c)
        f = spec_forward_factory(control)
        orc = O.Orchestrator(cx, O.InProcessExecutor(cx, f), log=lambda m: None)
        res = orc.run()
        direct = cx.E.run_calibration_region(forward=lambda t: f(cx.mapper.build(t)['spec']), **cx.run_kwargs())
        rep = orc.probe.run(orc.cache, 'replay')['run']
        dists = sorted(set(e['theta_natural']['distance_Mpc'] for e in direct['evaluation_log'] if e.get('theta_natural')))
        rows.append({'case': name, 'status': res.get('status'), 'engine_status': res.get('engine_status'),
                     'same_as_direct': cx.E._canonical_bytes(direct) == cx.E._canonical_bytes(rep),
                     'wave_sizes': [w_.get('n_calls') for w_ in res.get('waves') or []], 'distances': dists,
                     'evaluations': len(direct['evaluation_log']), 'n_launched_distinct': res.get('n_launched_distinct'),
                     'freeze_gate': str(res.get('freeze_gate'))[:60]})
    with open(tdir / 'T41_WAVE_SIZES_3D.json', 'x') as fh:          # input of make_timing_model_c2v004.py (MEASURED on the toy)
        json.dump({'schema': 'DDO154_CALIBRATION_SYNTHETIC_WAVE_SIZES_C2V004', 'coordinate_mode': O.MODE_D_FIXED,
                   'source': 'tests/test_orchestrator_c2v004.py T41: in-process orchestrator c2v004, real V004 addendum (3 '
                             'free coordinates), SYNTHETIC toy forward and region (not DDO154 data)',
                   'cases': rows}, fh, indent=1)
    check('T41.A13_in_process_runs_complete_identically_at_4p04',
          all(r['status'] == 'COMPLETE' and r['same_as_direct'] and r['distances'] == [4.04] for r in rows) and
          rows[0]['engine_status'] == 'COMPLETE' and rows[0]['wave_sizes'][:2] == [1, 3], rows)
    # campaign end to end with the mock of c2v008 + gal_c2v004 (refuses run mode at D != 4.04): A13 unblocks it
    vg = mock_variant('STAGE_REGISTERED_ONLY', stage='REGISTERED_ONLY')
    cpath = write_control(FIX / 'control_T41.json', control)
    cfg_c = make_config(tdir / 'camp' / 'work', region3, anchor, numerics_block=c2r_like(), driver=vg, mode='3D')
    cp = save_config(cfg_c, 'T41_campaign.json')
    code, out = cli('run', cp, cpath)
    plans = [json.loads(p_.read_text()) for p_ in sorted((tdir / 'camp' / 'work' / 'waves').glob('wave_*/WAVE_PLAN.json'))]
    specs_d = sorted(set(c_['spec']['physical']['distance_Mpc'] for p_ in plans for c_ in p_['calls']))
    check('T41.A13_campaign_with_registered_only_stage_binding_completes', code == 0 and out.get('status') == 'COMPLETE'
          and specs_d == [4.04] and out.get('coordinate_mode', {}).get('mode') == O.MODE_D_FIXED,
          {'exit': code, 'status': out.get('status'), 'engine_status': out.get('engine_status'), 'n_waves': out.get('n_waves'),
           'spec_distances': specs_d})
    # capability evidence builder (guarded dry-runs of the mock) in the 3-coordinate mode
    V = load(VERIFY_PATH, 'verify4_t41')
    ev = V.main(str(cp), str(tdir / 'evidence'), use_guard=True)
    doc = json.loads(Path(ev).read_text())
    cfg_e = copy.deepcopy(cfg_c)
    cfg_e['capability_evidence'] = pin(ev)
    cap_e = O.Context(cfg_e).gates['driver_capability']
    check('T41.A13_capability_evidence_trial_W1_W2x3_corners8_all_run_mode_admitted',
          doc['counts'] == {'checked': 13, 'normalize_accepted': 13, 'run_mode_admitted': 13, 'trial': 1, 'W1': 1, 'W2': 3,
                            'corners': 8} and doc['all_points_at_registered_distance'] and doc['guard_denials_total'] == 0
          and cap_e['ok'] and cap_e['layer2_run_mode'] == 'ADMITTED', {'counts': doc['counts'], 'layer2': cap_e['layer2_run_mode']})
    # a non-synthetic config refuses the nuisance mode; malformed fixed declarations refused
    c_ns = make_config(tdir / 'ns' / 'WORK', region4, {'use': False}, numerics_block=c2r_like())
    c_ns['synthetic_test'] = False
    c_ns['work_dir_identity'] = O.work_dir_identity_core(O.resolve_work_dir(str(tdir / 'ns' / 'WORK'), None))
    try:
        O.Context(c_ns)
        rn = 'NOT REFUSED'
    except O.OrchestratorError as exc:
        rn = str(exc)[:80]
    bad = {}
    for name, cm in (('distance_4p05', {'fixed_engine_coordinates': {'distance_Mpc': 4.05}}),
                     ('extra_fixed', {'fixed_engine_coordinates': {'distance_Mpc': 4.04, 'common_scale_s': 0.1}}),
                     ('free_list_4', {'free_coordinates': list(O.VARYING_EXPECTED_BY_MODE[O.MODE_D_NUISANCE])}),
                     ('unknown_mode', {'mode': 'SOMETHING'})):
        a = json.loads(ADD_PATH.read_text())
        a['coordinate_mode'].update(cm)
        ap = fixture_dir('addendum_bad') / 'ADDENDUM.json'
        ap.write_text(json.dumps(a))
        c = make_config(tdir / ('bad_%s' % name), region3, {'use': False}, numerics_block=c2r_like(), mode='3D')
        c['coordinate_spec_addendum'] = pin(ap)
        try:
            O.Context(c)
            bad[name] = 'NOT REFUSED'
        except O.OrchestratorError as exc:
            bad[name] = 'refused'
    check('T41.A13_nuisance_mode_refused_outside_tests_and_bad_mode_declarations_refused',
          rn.startswith('A13') and all(v == 'refused' for v in bad.values()), dict(bad, non_synthetic_nuisance=rn))
    # freeze compatibility (TESTED-NEGATIVE): prediction_freeze_c2v003a cannot consume the fixed-D calibration
    orc3 = O.Orchestrator(ctx3, O.InProcessExecutor(ctx3, spec_forward_factory(control)), log=lambda m: None)
    r3 = orc3.run()
    run3 = orc3.probe.run(orc3.cache, 'replay')['run']
    F = ctx3.F
    sel4 = F.select_representative_points(exploration=run3, interior_count=6, spec=ctx3.freeze_spec['spec'])
    coords3 = [c_ for c_ in SPEC['coordinates'] if c_['name'] != 'distance_Mpc'] + \
        SPEC['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation']
    fs3 = F.make_freeze_coordinate_spec(coordinates=coords3)
    sel3 = F.select_representative_points(exploration=run3, interior_count=6, spec=fs3['spec']) if fs3['ok'] else {'ok': None}
    cfix = copy.deepcopy(SPEC['coordinates'])
    for c_ in cfix:
        if c_['name'] == 'distance_Mpc':
            c_['role'] = 'fixed'
    fsf = F.make_freeze_coordinate_spec(coordinates=cfix + SPEC['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation'])
    check('T41.A13_freeze_c2v003a_cannot_consume_fixed_distance_TESTED_NEGATIVE',
          r3['status'] == 'COMPLETE' and sel4['ok'] is False and sel3.get('ok') is False and fsf['ok'] is False,
          {'with_v001_freeze_list': sel4['reasons'][:1], 'distance_slot_omitted': (sel3.get('reasons') or [None])[:1],
           'distance_role_fixed_in_freeze_list': fsf['reasons'][:1]})


def write_addendum_4d():
    """SYNTHETIC 4-coordinate addendum: the V004 addendum bytes with ONLY coordinate_mode replaced by the nuisance mode
    (the v003 suite runs on it; a non-synthetic config refuses this mode, A13)."""
    a = json.loads(ADD_PATH.read_text())
    a['coordinate_mode'] = {'mode': O.MODE_D_NUISANCE,
                            'free_coordinates': list(O.VARYING_EXPECTED_BY_MODE[O.MODE_D_NUISANCE]),
                            'fixed_engine_coordinates': {},
                            'note': 'SYNTHETIC TEST FIXTURE: the recorded alternative (distance as a nuisance)'}
    p = FIX / 'SYNTHETIC_ADDENDUM_4D_NUISANCE_MODE.json'
    with open(p, 'x') as fh:
        json.dump(a, fh, indent=1)
    ADD4D.update(pin(p))


def main():
    if '--only' in sys.argv:
        ONLY.extend(x for x in sys.argv[sys.argv.index('--only') + 1].split(',') if x)
    RUN_DIR.mkdir(parents=True)
    FIX.mkdir()
    sys.addaudithook(_audit)
    t_start = time.time()
    write_addendum_4d()
    guard('T0', t0_pins)
    control = copy.deepcopy(BASE_CONTROL)
    control['timeline'] = str(FIX / 'mock_timeline_main.jsonl')
    control_path = write_control(FIX / 'control_main.json', control)
    region = write_region(FIX / 'SYNTHETIC_REGION_NOT_DDO154.json', TRUTH, control)
    ctx0 = O.Context(make_config(RUN_DIR / 'T1' / 'work', region, {'use': False}, numerics_block=c2r_like()))
    guard('T1', lambda: t1_stop_contract(ctx0))
    guard('T2', t2_inprocess_matrix)
    guard('T7', lambda: t7_mapper(region))
    guard('T9', lambda: t9_taxonomy(region))
    guard('T10', lambda: t10_deciding(region))
    guard('T11', lambda: t11_numerics_gate(region))
    guard('T12', lambda: t12_a7(region))
    guard('T13', lambda: t13_capability(region))
    guard('T14', lambda: t14_crash_windows(region))
    guard('T15', lambda: t15_orphans(region))
    guard('T16', lambda: t16_disk(region))
    guard('T19', lambda: t19_concurrency(region))
    guard('T21', lambda: t21_c7(region))
    guard('T29', lambda: t29_d5(region))
    guard('T30', lambda: t30_c8_labels(region))
    guard('T32', lambda: t32_work_dir(region))
    guard('T33', t33_real_anchor_bytes)
    anchor = {}
    guard('T3.anchor', lambda: anchor.update(make_anchor_fixture(control_path)))
    anchor_v = {}
    guard('T3.anchor_variant', lambda: anchor_v.update(make_anchor_fixture(
        control_path, driver=mock_variant('ANCHOR_VARIANT'), tag='VARIANT')))
    guard('T20', lambda: t20_plan_output(region, anchor))
    guard('T6', lambda: t6_numerics(region, anchor, anchor_v))
    guard('T28', lambda: t28_campaign_budget(region))
    guard('T31', lambda: t31_capability_evidence(region, anchor))
    state = {}

    def run_t3():
        res, ref_sha, orc = t3_end_to_end(region, control_path, anchor)
        state.update(res=res, ref_sha=ref_sha)
    guard('T3', run_t3)
    if state.get('ref_sha'):
        control_t4 = copy.deepcopy(BASE_CONTROL)
        cpath_t4 = write_control(FIX / 'control_T4.json', control_t4)
        guard('T4', lambda: t4_resume(region, cpath_t4, anchor, state['ref_sha']))
        guard('T5a', lambda: t5_infra(region, anchor, state['ref_sha'], persist=False))
        guard('T5b', lambda: t5_infra(region, anchor, state['ref_sha'], persist=True))
        guard('T8_T24', lambda: t8_t24_cache_tamper(region, anchor, RUN_DIR / 'T3' / 'work'))
        guard('T22', lambda: t22_m1_crash_windows(region, cpath_t4, anchor, state['ref_sha']))
        guard('T25', lambda: t25_l3_torn(region, anchor, RUN_DIR / 'T3' / 'work', cpath_t4))
        guard('T26', lambda: t26_l4_lock(region, anchor, cpath_t4))
    elif not ONLY or 'T3' in ONLY:
        check('T3.reference_run_missing_dependent_tests_not_run', False, {})
    guard('T17', lambda: t17_numerics_limited(region, anchor))
    guard('T18', lambda: t18_unknown_e2e(region, anchor))
    guard('T23', lambda: t23_m2_tokens(region, anchor))
    guard('T27', lambda: t27_geometry_halt(region))
    guard('T34', lambda: t34_s1(region, anchor))
    guard('T35', lambda: t35_s2(region))
    guard('T36', lambda: t36_s3(region, anchor))
    guard('T37', lambda: t37_s4(region))
    guard('T38', lambda: t38_f1(region))
    guard('T39', lambda: t39_f2(region, control_path))
    guard('T40', lambda: t40_f3(region, control_path))
    guard('T41', lambda: t41_a13(region, anchor))
    check('TZ.audit_hook_no_denied_access', not AUDIT['denied'], {'denied': AUDIT['denied'][:5]})
    n_pass = sum(1 for r in RESULTS if r['pass'])
    summary = {'run_dir': str(RUN_DIR), 'n': len(RESULTS), 'n_pass': n_pass, 'n_fail': len(RESULTS) - n_pass,
               'wall_s': round(time.time() - t_start, 1), 'orchestrator_sha256': sha(ORCH_PATH),
               'campaign_sha256': sha(CAMP_PATH), 'taxonomy_sha256': sha(TAX_PATH), 'addendum_sha256': sha(ADD_PATH),
               'mock_sha256': sha(MOCK_PATH), 'crash_runner_sha256': sha(CRASH_RUNNER), 'verify_sha256': sha(VERIFY_PATH),
               'test_sha256': sha(__file__), 'audit_denied': AUDIT['denied'], 'results': RESULTS}
    with open(RUN_DIR / 'TEST_RESULTS.json', 'x') as fh:
        json.dump(summary, fh, indent=1, default=str)
    print('TOTAL %d/%d PASS  (%s)' % (n_pass, len(RESULTS), RUN_DIR))
    return 0 if n_pass == len(RESULTS) else 1


if __name__ == '__main__':
    sys.exit(main())
