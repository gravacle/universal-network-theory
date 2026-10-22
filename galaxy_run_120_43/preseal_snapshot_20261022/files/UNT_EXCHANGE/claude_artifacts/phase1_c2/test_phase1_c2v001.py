"""Tests for phase1_c2v001 (A133 section 5 MUST_FAIL list + MUST_PASS).  SYNTHETIC ONLY.

Synthetic campaigns are built by the REAL orchestrator c2v005 (Context, Probe, make_plan, _commit_plan, run_wave,
ingest, finalise) with its in-process test executor, a toy forward and a synthetic 12-row region, on the real coordinate
spec V002 (engine c2v003b), the real addendum V005A (A13: 3 free coordinates) and the real taxonomy V003.  The tool runs
through its CLI as root would run it (a subprocess of the campaign interpreter), except where a test injects a fault in
process.  Oracle: a direct engine run with the same forward (its primary_anchor and the index of its first 'march' call).
No project forward, no NGC3198 data or targets: NGC values are a toy function of u.  Writes only under
phase1_c2/test_runs/RUN_<UTC>_<pid>/ (an audit hook refuses any other write, and any open of a path with an 'ngc3198'
or 'uvt_' component).

usage: <codex python3> -I -B test_phase1_c2v001.py
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
import subprocess
import sys
import traceback
from pathlib import Path

HERE = Path(os.path.dirname(os.path.realpath(__file__)))
TOOL = HERE / 'phase1_c2v001.py'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
A133 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'A133_TWO_PHASE_PROTOCOL_V001.md', 'cd92ef914a0d562f0392080ebf709b5fdb1d85ef7f7b4493ee143fe782cfac17')
V005A = ART + 'calibration_engine_freeze_v003b_v003d/orchestrator_v005a/'
SPEC_PATH = V005A + 'DDO154_CALIBRATION_COORDINATE_SPEC_V002.json'
ADD_PATH = V005A + 'COORDINATE_SPEC_ADDENDUM_V005A.json'
TAX_PATH = ART + 'calibration_orchestrator_c2/v004/FAILURE_TAXONOMY_V003.json'
MONITOR = {'path': ART + 'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py',
           'sha256': 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'}
CAMP_PATH = ART + 'calibration_orchestrator_c2/v005/campaign_c2v005.py'
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
RUN = HERE / 'test_runs' / ('RUN_%s_%d' % (STAMP, os.getpid()))
FIX = RUN / 'fixtures'
RESULTS = []
Z = 2.865260238532134
AUDIT = {'denied': []}


def _audit(event, args):
    if event != 'open' or not isinstance(args[0], (str, bytes, os.PathLike)):
        return
    p = os.path.abspath(os.fsdecode(args[0]))
    comps = [c.lower() for c in p.split('/')]
    if any('ngc3198' in c or c.startswith('uvt_') for c in comps):
        AUDIT['denied'].append(['forbidden_path', p])
        raise PermissionError('test audit: ngc3198/uvt_ path refused: %s' % p)
    mode, flags = args[1], args[2]
    w = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
        (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)))
    if w and not p.startswith(str(RUN) + '/') and not p.startswith('/dev/'):
        AUDIT['denied'].append(['write', p])
        raise PermissionError('test audit: write outside the run dir refused: %s' % p)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p):
    return {'path': str(p), 'sha256': sha(p)}


def check(tid, ok, detail=None):
    RESULTS.append({'id': tid, 'pass': bool(ok), 'detail': detail})
    print('%s %-62s %s' % ('PASS' if ok else 'FAIL', tid, json.dumps(detail, default=str)[:260]), flush=True)


def guard(tid, fn):
    try:
        fn()
    except BaseException as exc:   # noqa: BLE001 -- a crash is a FAIL row
        if isinstance(exc, KeyboardInterrupt):
            raise
        check(tid, False, {'raised': '%s: %s' % (type(exc).__name__, exc), 'tb': traceback.format_exc()[-1800:]})


def load(path, name):
    sp = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


P = load(TOOL, 'phase1_under_test')
O, E, G = P.mod('O'), P.mod('E'), P.mod('G')
SPEC = json.loads(Path(SPEC_PATH).read_text())
TEMPLATE = json.loads(Path(SPEC['call_spec_mapping']['template']['path']).read_text())
PH = TEMPLATE['physical']
S0_, G0_, L0_ = PH['common_scale_s'], PH['gamma'] / PH['Eref_J'], PH['ell_F_m']
ROWS = ['SYN_ROW_%02d' % i for i in range(1, 13)]
RADII = [0.5 * i for i in range(1, 13)]
QIDS = ['SYN-Q%02d' % k for k in range(1, 44)]


# ----------------------------------------------------------------------------------------------- toy model
def a_of_spec(spec):
    ph = spec['physical']
    return (math.log2(ph['common_scale_s'] / S0_), math.log10((ph['gamma'] / ph['Eref_J']) / G0_),
            math.log2(ph['ell_F_m'] / L0_))


def toy_speeds(a, const=False):
    if const:
        return {r: 50.0 for r in ROWS}
    return {r: 40.0 + 8.0 * math.sqrt(rad) * (1.0 + 0.3 * a[0] + 0.1 * a[1] * rad / 6.0) + 0.001 * a[2] * math.sin(rad)
            + 0.5 * a[0] ** 2 for r, rad in zip(ROWS, RADII)}


def forward_factory(invalid=None, const=False):
    def fwd(spec):
        a = a_of_spec(spec)
        if invalid is not None and invalid(a):
            return {'valid': False, 'speeds_km_s': {}, 'reasons': ['TOY_INVALID']}
        return {'valid': True, 'speeds_km_s': toy_speeds(a, const), 'reasons': []}
    return fwd


def write_region(path, truth, sigma, const=False):
    v = toy_speeds(truth, const)
    ds = json.loads(Path(SPEC['observation_region']['path']).read_text())['distance_summary']
    rows = [{'id': r, 'reference_radius_kpc': rad, 'observed_speed_km_s': v[r], 'quoted_random_sigma_km_s': sigma,
             'conditional_random_acceptance_low_km_s': v[r] - Z * sigma,
             'conditional_random_acceptance_high_km_s': v[r] + Z * sigma} for r, rad in zip(ROWS, RADII)]
    doc = {'rows': rows, 'statistical_choice': 'SYNTHETIC toy (not DDO154 data)', 'forward_coordinates': 'SYNTHETIC',
           'distance_summary': dict(ds, scope='SYNTHETIC copy of the distance_summary numbers so the real box binds')}
    with open(path, 'x') as fh:
        json.dump(doc, fh, indent=1)
    return pin(path)


DRIVER = {}


def driver_pin():
    if not DRIVER:
        p = FIX / 'mock_driver_phase1_c2v001.py'
        p.write_text('# %s (phase1_c2 SYNTHETIC test fixture: normalize_spec only, never a forward)\nimport copy\n\n\n'
                     'def normalize_spec(spec):\n    return copy.deepcopy(spec)\n' % O.SYNTHETIC_DRIVER_MARKER.decode())
        DRIVER.update(pin(p))
    return dict(DRIVER)


def make_config(work, region, override=None):
    return {'schema': O.SCHEMA_CONFIG, 'synthetic_test': True, 'work_dir': str(work), 'work_dir_volume': None,
            'coordinate_spec': pin(SPEC_PATH), 'coordinate_spec_addendum': pin(ADD_PATH), 'work_dir_identity': None,
            'observation_region': region, 'numerics': None, 'ngc3198_slots': None, 'anchor': {'use': False},
            'driver': driver_pin(), 'deciding_test': None, 'capability_evidence': None, 'taxonomy': pin(TAX_PATH),
            'route_a_contraction_test': None, 'recovery_rules': [], 'monitor': MONITOR, 'campaign': pin(CAMP_PATH),
            'python': {'path': PY, 'sha256': sha(os.path.realpath(PY))}, 'max_concurrent': 1, 'process_budget': 17,
            'stage_aware_budget': False, 'n_cores': 18,
            'per_call': {'wall_cap_s': 60.0, 'rss_cap_bytes': 1 << 30, 'output_cap_bytes': 64 << 20, 'poll_s': 0.25},
            'campaign_wall_cap_s': 3600.0,
            'disk_guard': {'per_call_bytes': 64 << 20, 'reserve_bytes': 1 << 20, 'measured_per_call_bytes': 1 << 20},
            'orphan_wait': {'poll_s': 0.5, 'cap_s': 30.0, 'receipt_grace_s': 1.0},
            'engine_parameters_override': override, 'executor': 'in_process_test', 'u_i_carrier': None,
            'adoption_derivation': None, 'notes': 'SYNTHETIC phase1_c2 test config (toy forward, synthetic region)'}


class Camp:
    """A synthetic campaign driven by the real orchestrator's wave machinery (no gates: in-process test executor)."""

    def __init__(self, tag, truth, sigma, invalid=None, const=False, override=None):
        self.dir = RUN / tag
        self.dir.mkdir(parents=True)
        region = write_region(self.dir / 'SYNTHETIC_REGION.json', truth, sigma, const)
        cfg = make_config(self.dir / 'work', region, override)
        self.cfg = self.dir / 'CONFIG.json'
        with open(self.cfg, 'x') as fh:
            json.dump(cfg, fh, indent=1)
        self.cfg_sha = sha(self.cfg)
        self.fwd = forward_factory(invalid, const)
        self.ctx = O.Context(str(self.cfg))
        self.orc = O.Orchestrator(self.ctx, O.InProcessExecutor(self.ctx, self.fwd), log=lambda m: None)
        self.orc.prepare(create=True, init_work_dir=True)
        self.final = None

    def step(self, execute=True):
        """Plan (and run) one wave; returns its families, or None when the probe is complete (then finalise)."""
        pr = self.orc.probe.run(self.orc.cache, 'probe')
        if pr['complete']:
            self.final = self.orc.finalise()
            return None
        misses = self.orc._dedup(pr['misses'])
        n = len(self.orc.wave_dirs()) + 1
        wd = self.orc.waves_dir / ('wave_%04d' % n)
        plan = self.orc.make_plan(n, misses)
        plan['probe'] = {k: pr[k] for k in ('stop_reason', 'calls', 'hits', 'placeholders', 'families')}
        wd.mkdir(parents=True)
        self.orc._commit_plan(wd, plan)
        self.pending = (wd, plan) if not execute else None
        if execute:
            res, _m = self.orc.run_wave(wd, plan, resume=False)
            assert not res['halt'], res['halt']
        return [list(f) for f in plan['families']]

    def run_pending(self):
        wd, plan = self.pending
        self.orc.run_wave(wd, plan, resume=False)
        self.pending = None

    def until_march0_planned(self):
        while True:
            fam = self.step(execute=False)
            if fam is None:
                return False
            if ['march0'] in fam:
                return True
            self.run_pending()

    def complete(self):
        if getattr(self, 'pending', None):
            self.run_pending()
        while self.step() is not None:
            pass
        return self.final

    def oracle(self):
        direct = E.run_calibration_region(forward=lambda th: self.fwd(self.ctx.mapper.build(th)['spec']),
                                          **self.ctx.run_kwargs())
        idx = [e['index'] for e in direct['evaluation_log'] if e['purpose'] == 'march']
        ex = direct.get('exploration') or {}
        return {'b_p1': idx[0] if idx else None, 'status': direct['status'], 'primary': ex.get('primary_anchor'),
                'run': direct}

    def tree(self):
        h = hashlib.sha256()
        for p in sorted(Path(self.dir / 'work').rglob('*')):
            if p.is_file():
                h.update(str(p).encode() + b'\0' + p.read_bytes())
        return h.hexdigest()


# ----------------------------------------------------------------------------------------------- tool CLI
def tool(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    p = subprocess.run([PY, '-I', '-B', str(TOOL)] + [str(x) for x in args], capture_output=True, text=True, env=env)
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = {'unparsed': p.stdout[-1500:], 'stderr': p.stderr[-1500:]}
    return p.returncode, out


def snap(c, name):
    out = RUN / ('SNAP_' + name)
    rc, o = tool('snapshot', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', out)
    return rc, o, out


def snap_sha(out):
    return sha(Path(out) / 'SNAPSHOT_C2V001.json')


def rec_of(out):
    d = json.loads((Path(out) / 'SNAPSHOT_C2V001.json').read_text())
    return d, json.loads((Path(out) / d['record']['file']).read_text())


def campaign_of(c):
    return P.Campaign(str(c.cfg), c.cfg_sha)


def refused(fn, code=None):
    try:
        fn()
    except P.Refused as exc:
        return code is None or exc.code == code, exc.code
    return False, 'NO_REFUSAL'


# ----------------------------------------------------------------------------------------------- tests
def t00_pins():
    ok = (sha(A133[0]) == A133[1] and sha(P.ORCH_PIN[0]) == P.ORCH_PIN[1] and sha(P.ENGINE_PIN[0]) == P.ENGINE_PIN[1]
          and sha(P.FREEZE_PIN[0]) == P.FREEZE_PIN[1] and SPEC['engine']['sha256'] == P.ENGINE_PIN[1]
          and SPEC['engine']['path'] == P.ENGINE_PIN[0] and P.tau_check()['tau_over_sigma'] == 0.25
          and SPEC['engine_parameters']['rel_step'] == 0.05 and SPEC['engine_parameters']['min_step'] == 0.005
          and SPEC['engine_parameters']['hull_growth_tol'] == 0.02 and SPEC['engine_parameters']['max_repair_step'] == 0.25)
    check('T00.pins_from_bytes_and_registered_parameters', ok, {'a133': A133[1][:16], 'engine': P.ENGINE_PIN[1][:16]})


def scenario_checks(tag, c, o_rc, o, out, orc_):
    d, rec = rec_of(out)
    run = rec['run']
    pa = run['exploration']['primary_anchor']
    v = E.verify_calibration_record(record_path=str(Path(out) / d['record']['file']),
                                    registry_path=str(Path(out) / d['record']['registry_file']))
    reg_lines = (Path(out) / d['record']['registry_file']).read_text().splitlines()
    ok = (o_rc == 0 and d['b_p1'] == orc_['b_p1'] and pa['log_index'] == orc_['primary']['log_index'] and
          pa['u'] == orc_['primary']['u'] and rec['status'] == 'BUDGET_EXHAUSTED' and v['ok'] and len(reg_lines) == 1 and
          run['evaluation_log'] == orc_['run']['evaluation_log'][:d['b_p1']] and
          run['exploration']['stage_reached'] == 'march')
    check('T%s.snapshot_B_P1_and_u_A_equal_direct_engine_oracle' % tag, ok,
          {'rc': o_rc, 'b_p1': d.get('b_p1'), 'oracle_b_p1': orc_['b_p1'], 'u_A_log_index': pa['log_index'],
           'source': pa['source'], 'verify': v['ok'], 'reason': o.get('reason')})
    return d, rec


def t01_seed(S):
    c = Camp('SEED', (0.0, 0.0, 0.0), 1.0)
    assert c.until_march0_planned()
    S['seed'] = c
    orc_ = c.oracle()
    t0 = c.tree()
    rc, o, out = snap(c, 'SEED')
    check('T01.snapshot_reads_only (work dir tree unchanged)', c.tree() == t0, {'rc': rc})
    d, rec = scenario_checks('01', c, rc, o, out, orc_)
    check('T01.seed_case_B_P1_is_7_u_A_is_seed', d['b_p1'] == 7 and d['u_A']['source'] == 'seed', d['u_A']['source'])
    S['seed_snap'] = out
    rc2, o2 = tool('snapshot', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', out)
    check('T02.MUST_FAIL_snapshot_out_dir_exists_refused', rc2 == 3 and snap_sha(out) == sha(Path(out) / 'SNAPSHOT_C2V001.json'),
          o2.get('reason'))
    rc3, o3 = tool('snapshot', '--config', c.cfg, '--config-sha256', '0' * 64, '--out-dir', RUN / 'SNAP_BADPIN')
    check('T02.MUST_FAIL_config_pin_mismatch_refused', rc3 == 3 and not (RUN / 'SNAP_BADPIN').exists(), o3.get('reason'))


def t03_s0_fd(S):
    c = S['seed']
    rc, o = tool('fdplan', '--s0-only', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', RUN / 'S0_SEED')
    s0 = json.loads((RUN / 'S0_SEED' / 'S0_C2V001.json').read_text())
    _d, rec = rec_of(S['seed_snap'])
    log = rec['run']['evaluation_log']
    first = [0, 1, 3, 5]   # engine order: seed, then per column the plus side and the minus side
    same = [P.fhex(log[i]['u']) == s0['points'][j]['u_hex'] and
            {k: v.hex() for k, v in log[i]['theta_natural'].items()} == s0['points'][j]['theta_hex']
            for j, i in enumerate(first)]
    check('T03.fdplan_s0_target_free_equals_record_seed_and_first_attempts', rc == 0 and all(same),
          {'rc': rc, 'same': same, 'roles': [p['role'] for p in s0['points']]})
    S['s0'] = RUN / 'S0_SEED' / 'S0_C2V001.json'
    ss = snap_sha(S['seed_snap'])
    rc, o = tool('fdplan', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--snapshot', S['seed_snap'],
                 '--snapshot-sha256', ss, '--interior-count', 6, '--out-dir', RUN / 'FD_SEED')
    fd = json.loads((RUN / 'FD_SEED' / 'FDPLAN_C2V001.json').read_text())
    f_keys = [f['key'] for f in fd['F']]
    m_keys = [m['key'] for m in fd['members']]
    ok = (rc == 0 and f_keys == [p['key'] for p in s0['points'][1:]] and all('record_log_index' in f for f in fd['F'])
          and fd['n_distinct_calls'] == len(set(f_keys + m_keys)))
    check('T04.fdplan_F_is_seed_first_attempts_from_record_and_dedups_members', ok,
          {'rc': rc, 'n_members': len(m_keys), 'F_in_M': sum(k in m_keys for k in f_keys),
           'n_distinct': fd.get('n_distinct_calls')})
    S['seed_fd'] = RUN / 'FD_SEED' / 'FDPLAN_C2V001.json'


def side_rule_unit():
    p, side, h = P.side_point([0.999, 0.5, 0.0], 0, 0.05, 0.005)
    p2, side2, h2 = P.side_point([0.999, 0.5, 0.0], 2, 0.05, 0.005)
    p3, side3, h3 = P.side_point([0.9949, 0.5, 0.5], 0, 0.05, 0.005)
    p4, side4, h4 = P.side_point([0.9951, 0.5, 0.5], 0, 0.05, 0.005)
    ok = (side == 'minus' and h == 0.05 and p[0] == 0.999 - 0.05 and side2 == 'plus' and p2[2] == 0.05 and
          side3 == 'plus' and h3 == 1.0 - 0.9949 and p3[0] == min(0.9949 + (1.0 - 0.9949), 1.0) and
          side4 == 'minus' and p4[0] == 0.9951 - 0.05)
    check('T05.F_side_rule_minus_below_min_step_plus_otherwise', ok, {'sides': [side, side2, side3, side4]})


def provenance_fixture(c, out, tag, mutate=None):
    """SYNTHETIC published provenance: wave-plan shas from bytes, admission records naming them, ACCEPTED post-state
    acceptance and a certificate per admitted point, each binding the point's spec sha."""
    _d, rec = rec_of(out)
    run = rec['run']
    fx = RUN / ('PROV_' + tag)
    fx.mkdir()
    cp = campaign_of(c)
    waves = cp.waves()
    prov = {'schema': P.S_PROV, 'cache_id': c.ctx.cache_id, 'wave_plans': {}, 'admissions': {}, 'points': {}}
    for w, x in waves.items():
        prov['wave_plans'][str(w)] = x['plan_sha256']
        ap = fx / ('ADMISSION_W%d.json' % w)
        ap.write_text(json.dumps({'synthetic': True, 'wave': w, 'plan_sha256': x['plan_sha256']}))
        prov['admissions'][str(w)] = pin(ap)
    for p in run['exploration']['admitted_points']:
        key = O.theta_key(p['theta_natural'])
        spec_sha = cp.orch.cache.entries[key]['provenance']['spec_sha256']
        a_ = fx / ('ACCEPT_%d.json' % p['log_index'])
        a_.write_text(json.dumps({'synthetic': True, 'point_spec_sha256': spec_sha}))
        cf = fx / ('CERT_%d.json' % p['log_index'])
        cf.write_text(json.dumps({'synthetic': True, 'point_spec_sha256': spec_sha}))
        prov['points'][key] = {'post_state_acceptance': dict(pin(a_), status='ACCEPTED'), 'certificates': [pin(cf)]}
    if mutate:
        mutate(prov, fx, run, cp)
    pp = fx / 'PROVENANCE.json'
    pp.write_text(json.dumps(prov, indent=1))
    pol = fx / 'SYNTHETIC_POLICY.json'
    pol.write_text('{"synthetic": true}')
    rf = {'schema': P.S_ROOT, 'mode': 'SYNTHETIC_DRY_ONLY', 'root_admission': 'SYNTHETIC_DRY_ONLY', 'policy_pin': pin(pol),
          'v007_adoption_pin': None, 'certificate_pins': {'eps_certificate': 'PENDING_UV_TAIL_CERTIFICATE',
                                                          'lo_certificate': 'PENDING_UV_TAIL_CERTIFICATE'},
          'driver_branch': 'r006_fallback', 'driver_acceptance_pin': None, 'coordinate_pin': pin(SPEC_PATH)}
    rp = fx / 'ROOT_FIELDS.json'
    rp.write_text(json.dumps(rf, indent=1))
    return pp, rp


def handoff(c, out, pp, rp, tag):
    o_ = RUN / ('HANDOFF_' + tag)
    rc, o = tool('handoff', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--config', c.cfg,
                 '--config-sha256', c.cfg_sha, '--interior-count', 6, '--provenance', pp, '--provenance-sha256', sha(pp),
                 '--root-fields', rp, '--root-fields-sha256', sha(rp), '--out-dir', o_)
    return rc, o, o_


def t06_handoff(S):
    c, out = S['seed'], S['seed_snap']
    pp, rp = provenance_fixture(c, out, 'OK')
    t0 = c.tree()
    rc, o, o_ = handoff(c, out, pp, rp, 'OK')
    check('T06.handoff_reads_only (work dir tree unchanged)', c.tree() == t0, None)
    ok = rc == 0
    if ok:
        ex = json.loads((o_ / 'TARGET_FREE_EXPORT_C2V001.json').read_text())
        rcpt = json.loads((o_ / 'HANDOFF_RECEIPT_C2V001.json').read_text())
        hs = [json.loads(Path(h['path']).read_text()) for h in rcpt['handoffs']]
        _d, rec = rec_of(out)
        adm = sorted(p['log_index'] for p in rec['run']['exploration']['admitted_points'])
        ok = (set(ex) == {'schema', 'mode', 'target_free', 'coordinate_pin', 'admitted_points'} and
              [p['log_index'] for p in ex['admitted_points']] == adm and
              all(set(p) == {'log_index', 'u', 'theta_natural'} for p in ex['admitted_points']) and
              all(len(h) == 10 and h['source_export_pin']['sha256'] == sha(o_ / 'TARGET_FREE_EXPORT_C2V001.json')
                  for h in hs) and rcpt['launch_authorized'] is False and
              _d['u_A']['log_index'] in [h['log_index'] for h in hs])
    check('T06.handoff_complete_roster_export_and_10_field_handoffs_per_member', ok,
          {'rc': rc, 'members': o.get('members'), 'reason': o.get('reason')})

    def bad_plan(prov, fx, run, cp):
        prov['wave_plans']['2'] = '0' * 64

    def no_accept(prov, fx, run, cp):
        k = sorted(prov['points'])[0]
        prov['points'][k]['post_state_acceptance'] = None

    def refused_accept(prov, fx, run, cp):
        k = sorted(prov['points'])[0]
        prov['points'][k]['post_state_acceptance']['status'] = 'REFUSED'

    def cert_other(prov, fx, run, cp):
        ks = sorted(prov['points'])
        if len(ks) > 1:
            prov['points'][ks[0]]['certificates'] = list(prov['points'][ks[1]]['certificates'])

    def adm_unbound(prov, fx, run, cp):
        ap = fx / 'ADMISSION_UNBOUND.json'
        ap.write_text('{"synthetic": true, "plan_sha256": "none"}')
        prov['admissions']['1'] = pin(ap)
    for name, mut in (('plan_hash_mismatch', bad_plan), ('post_state_acceptance_missing', no_accept),
                      ('post_state_acceptance_refused', refused_accept),
                      ('certificate_bound_to_another_point', cert_other),
                      ('admission_does_not_name_plan', adm_unbound)):
        pp2, rp2 = provenance_fixture(c, out, name, mut)
        rc2, o2, o2_ = handoff(c, out, pp2, rp2, name)
        check('T07.MUST_FAIL_handoff_%s' % name, rc2 == 3 and not o2_.exists() and 'PROVENANCE' in o2.get('reason', ''),
              o2.get('reason', '')[:200])
    rf = json.loads(Path(rp).read_text())
    rf['mode'] = 'ADMITTED'
    rp3 = RUN / 'PROV_OK' / 'ROOT_FIELDS_ADMITTED_ON_SYNTHETIC.json'
    rp3.write_text(json.dumps(rf))
    rc3, o3, o3_ = handoff(c, out, pp, rp3, 'MODE_FENCE')
    check('T07.MUST_FAIL_handoff_ADMITTED_mode_on_a_synthetic_campaign_refused',
          rc3 == 3 and not o3_.exists() and 'ROOT_FIELDS' in o3.get('reason', ''), o3.get('reason', '')[:160])


def t08_at0a(S):
    c, out = S['seed'], S['seed_snap']
    t0 = c.tree()
    rc, o = tool('agree', 'at0a', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--config', c.cfg,
                 '--config-sha256', c.cfg_sha, '--s0', S['s0'], '--s0-sha256', sha(S['s0']), '--out-dir', RUN / 'AT0A_SEED')
    check('T08.agree_at0a_PASS_prefix_next_requested_s0_runtime', rc == 0 and o.get('failures') == [] and c.tree() == t0,
          {'rc': rc, 'failures': o.get('failures'), 'reason': o.get('reason'), 'work_dir_unchanged': c.tree() == t0})
    rc, o = tool('snapshot', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', c.dir / 'work' / 'P1_INSIDE')
    check('T08.MUST_FAIL_out_dir_inside_the_campaign_work_dir_refused', rc == 3 and 'OUT_DIR' in o.get('reason', '')
          and not (c.dir / 'work' / 'P1_INSIDE').exists(), o.get('reason'))
    S['seed_at0a'] = RUN / 'AT0A_SEED' / 'AT0A_C2V001.json'


def t09_scenarios(S):
    cases = [('JAC', (0.1, 0.0, 0.0), 0.1, None, None, 'log_scan'),
             ('REPAIR', (0.3, 0.0, 0.0), 0.1, None, None, 'repair'),
             ('GD', (-0.5, 1.0 / 3.0, -0.2), 0.1, (lambda a: 0.26 < (a[0] + 1) / 2 < 0.45), None, 'global_design'),
             ('HALVE', (0.0, 0.0, 0.0), 1.0, (lambda a: a[0] > 0.075), None, 'seed')]
    for tag, truth, sigma, inv, ov, source in cases:
        c = Camp(tag, truth, sigma, invalid=inv, override=ov)
        if not c.until_march0_planned():
            check('T09.%s.campaign_reaches_march0' % tag, False, 'campaign ended without march0')
            continue
        orc_ = c.oracle()
        rc, o, out = snap(c, tag)
        d, rec = scenario_checks('09.%s' % tag, c, rc, o, out, orc_)
        check('T09.%s.u_A_source_%s' % (tag, source), d['u_A']['source'] == source,
              {'source': d['u_A']['source'], 'b_p1': d['b_p1']})
        S[tag] = (c, out)
    if 'HALVE' in S:
        c, out = S['HALVE']
        d, rec = rec_of(out)
        fam = [x['family'][0] for x in d['prefix_calls']]
        check('T09.HALVE.B_P1_counts_the_halving_call', d['b_p1'] == 8 and fam.count('jacobian') == 7,
              {'b_p1': d['b_p1'], 'families': fam})
        rc, o = tool('fdplan', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--snapshot', out, '--snapshot-sha256',
                     snap_sha(out), '--interior-count', 6, '--out-dir', RUN / 'FD_HALVE')
        fd = json.loads((RUN / 'FD_HALVE' / 'FDPLAN_C2V001.json').read_text()) if rc == 0 else {}
        log = rec['run']['evaluation_log']
        f0 = (fd.get('F') or [{}])[0]
        check('T09.HALVE.F0_is_the_DDO_invalid_first_attempt_point_from_the_record',
              rc == 0 and log[f0['record_log_index']]['valid'] is False and f0['side'] == 'plus',
              {'rc': rc, 'F0_log_index': f0.get('record_log_index')})
    if 'GD' in S:
        d, _r = rec_of(S['GD'][1])
        fam = sorted(set(x['family'][0] for x in d['prefix_calls']))
        check('T09.GD.prefix_holds_repair_and_pre_march_global_design', fam == ['gd_pre', 'jacobian', 'repair', 'seed']
              and d['b_p1'] == 22, {'families': fam, 'b_p1': d['b_p1']})
    if 'JAC' in S:
        c, out = S['JAC']
        rc, o = tool('fdplan', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--snapshot', out, '--snapshot-sha256',
                     snap_sha(out), '--interior-count', 6, '--out-dir', RUN / 'FD_JAC')
        fd = json.loads((RUN / 'FD_JAC' / 'FDPLAN_C2V001.json').read_text()) if rc == 0 else {}
        d, rec = rec_of(out)
        n_adm = len(rec['run']['exploration']['admitted_points'])
        roles = [m['role'] for m in fd.get('members') or []]
        ok = rc == 0 and (n_adm != 1 or (roles == ['hull_vertex'] and fd['n_distinct_calls'] == 4))
        check('T09.JAC.single_admitted_u_A_role_hull_and_4_distinct_calls', ok,
              {'n_admitted': n_adm, 'roles': roles, 'n_distinct': fd.get('n_distinct_calls'), 'snapshot_v003g_role':
               d['v003g_anchor_check']['role']})


def t10_terminal(S):
    for tag, truth, sigma, inv, const, want in (
            ('NOADMIT', (0.9, 0.0, 0.0), 0.001, None, False, 'NO_ADMITTED_POINT_FOUND'),
            ('SEEDINVALID', (0.0, 0.0, 0.0), 1.0, (lambda a: abs(a[0]) < 0.01), False, 'SEED_INVALID'),
            ('NOID', (0.0, 0.0, 0.0), 1.0, None, True, 'NO_IDENTIFIED_DIRECTION')):
        c = Camp(tag, truth, sigma, invalid=inv, const=const)
        if tag == 'NOID':
            for _ in range(3):
                c.step()
            c.step(execute=False)
        else:
            c.complete()
        rc, o, out = snap(c, tag)
        doc = json.loads((out / 'SNAPSHOT_C2V001.json').read_text()) if out.exists() else {}
        files = sorted(p.name for p in out.iterdir()) if out.exists() else []
        orc_ = c.oracle()
        check('T10.%s.terminal_reported_no_record_no_NGC_call' % tag,
              rc == 20 and doc.get('phase1_status') == want and doc.get('ngc_calls') == 0 and files == ['SNAPSHOT_C2V001.json']
              and (want == 'NO_IDENTIFIED_DIRECTION' or orc_['status'] == want),
              {'rc': rc, 'status': doc.get('phase1_status'), 'oracle': orc_['status'], 'reason': o.get('reason')})


def t11_not_ready(S):
    c = Camp('EARLY', (0.0, 0.0, 0.0), 1.0)
    c.step()
    c.step()
    rc, o, out = snap(c, 'EARLY_W2')
    check('T11.MUST_FAIL_prefix_not_committed_NOT_READY', rc == 4 and not out.exists(), o.get('reason'))
    c.step()
    rc, o, out = snap(c, 'EARLY_W3')
    check('T11.MUST_FAIL_B_P1_reached_but_march0_plan_not_written_NOT_READY', rc == 4 and not out.exists(),
          o.get('reason'))
    c2 = Camp('TORN', (0.0, 0.0, 0.0), 1.0)
    assert c2.until_march0_planned()
    wr = c2.orc.waves_dir / 'wave_0003' / 'WAVE_RESULT.json'
    os.rename(wr, str(wr) + '.HIDDEN_BY_TEST')
    rc, o, out = snap(c2, 'TORN')
    check('T11.MUST_FAIL_prefix_wave_without_WAVE_RESULT_NOT_READY', rc == 4 and not out.exists(), o.get('reason'))


def t12_off_by_one_and_replay(S):
    c, out = S['seed'], S['seed_snap']
    cp = campaign_of(c)
    _w0, _waves, entries = cp.prefix()
    d, rec = rec_of(out)
    b = d['b_p1']
    for db in (-1, +1):
        ok, code = refused(lambda: cp.snapshot_run(entries, b + db), 'B_P1_WRONG')
        check('T12.MUST_FAIL_B_P1_off_by_%+d_refused' % db, ok, code)
    # a snapshot file claiming B_P1 + 1 for the same record
    fx = RUN / 'SNAP_FORGED_BP1'
    fx.mkdir()
    for f in (d['record']['file'], d['record']['registry_file']):
        (fx / f).write_bytes((Path(out) / f).read_bytes())
    (fx / 'SNAPSHOT_C2V001.json').write_text(json.dumps(dict(d, b_p1=b + 1), indent=1))
    ok, code = refused(lambda: P.load_snapshot(str(fx), sha(fx / 'SNAPSHOT_C2V001.json')), 'B_P1_WRONG')
    check('T12.MUST_FAIL_snapshot_file_B_P1_plus_1_refused', ok, code)
    rc, o = tool('agree', 'at0a', '--snapshot', fx, '--snapshot-sha256', sha(fx / 'SNAPSHOT_C2V001.json'), '--config',
                 c.cfg, '--config-sha256', c.cfg_sha, '--s0', S['s0'], '--s0-sha256', sha(S['s0']), '--out-dir',
                 RUN / 'AT0A_FORGED')
    check('T12.MUST_FAIL_at0a_on_off_by_one_snapshot_refused', rc == 3 and not (RUN / 'AT0A_FORGED').exists(),
          o.get('reason'))
    # replay mismatch: one prefix forward altered
    e2 = dict(entries)
    k = sorted(e2)[0]
    e2[k] = copy.deepcopy(e2[k])
    sp = e2[k]['forward']['speeds_km_s']
    sp[ROWS[0]] = sp[ROWS[0]] + 1e-9
    try:
        _r, _c, rsha = cp.snapshot_run(e2, b)
        ok = rsha != d['replay']['run_canonical_sha256']
    except P.Refused:
        ok = True
    check('T13.MUST_FAIL_replay_mismatch_detected (altered prefix forward)', ok, None)

    class Flip(dict):
        n = 0

        def get(self, key, default=None):
            e = dict.get(self, key, default)
            Flip.n += 1
            if e is not None and Flip.n == 2 + b:   # second pass, second call
                e = copy.deepcopy(e)
                e['forward']['speeds_km_s'][ROWS[0]] += 1e-9
            return e
    ok, code = refused(lambda: cp.snapshot_run(Flip(entries), b), 'REPLAY_NONDETERMINISTIC')
    check('T13.MUST_FAIL_replay_not_byte_equal_refused', ok, code)
    # prefix mismatch: a committed prefix entry missing from the view
    e3 = dict(entries)
    del e3[sorted(e3)[1]]
    ok, code = refused(lambda: cp.b_p1(e3), 'NOT_READY')
    check('T13.MUST_FAIL_prefix_miss_refused', ok, code)


def t14_anchor(S):
    c, out = S['seed'], S['seed_snap']
    d, rec = rec_of(out)
    run = rec['run']
    adm = [p for p in run['exploration']['admitted_points'] if p['log_index'] != d['u_A']['log_index']]
    if not adm:
        check('T14.MUST_FAIL_anchor_different_from_v003g', False, 'fixture has one admitted point')
        return
    forged = copy.deepcopy(run)
    forged['exploration']['primary_anchor']['log_index'] = adm[0]['log_index']   # u stays u_A's
    ok, code = refused(lambda: P.v003g_members(c.ctx, forged, 0), 'ANCHOR_MISMATCH')
    check('T14.MUST_FAIL_anchor_different_from_v003g_refused', ok, code)
    sel = P.v003g_members(c.ctx, run, 6)
    check('T14.v003g_anchor_equals_u_A_on_the_record', sel['admitted_region']['selection_anchor_log_index'] ==
          d['u_A']['log_index'], sel['admitted_region']['selection_anchor_log_index'])
    # a forged record (re-registered) whose primary anchor is another admitted point: load_snapshot refuses
    fx = RUN / 'SNAP_FORGED_ANCHOR'
    fx.mkdir()
    forged2 = copy.deepcopy(run)
    forged2['exploration']['primary_anchor'].update(log_index=adm[0]['log_index'], u=list(adm[0]['u']))
    rp, gp = str(fx / 'REC.json'), str(fx / 'REG.jsonl')
    w = E.write_calibration_record(run=forged2, record_path=rp, registry_path=gp)
    d2 = copy.deepcopy(d)
    d2['record'].update(file='REC.json', registry_file='REG.jsonl', record_file_sha256=w['record_file_sha256'])
    d2['replay']['run_canonical_sha256'] = hashlib.sha256(E._canonical_bytes(forged2)).hexdigest()
    (fx / 'SNAPSHOT_C2V001.json').write_text(json.dumps(d2, indent=1))
    ok, code = refused(lambda: P.load_snapshot(str(fx), sha(fx / 'SNAPSHOT_C2V001.json')), 'ANCHOR_MISMATCH')
    check('T14.MUST_FAIL_record_primary_anchor_not_snapshot_u_A_refused', ok, code)
    d3 = copy.deepcopy(d2)
    d3['u_A'].update(log_index=adm[0]['log_index'], u_hex=P.fhex(adm[0]['u']))
    fx3 = RUN / 'SNAP_FORGED_ANCHOR_CONSISTENT'
    fx3.mkdir()
    for f in ('REC.json', 'REG.jsonl'):
        (fx3 / f).write_bytes((fx / f).read_bytes())
    (fx3 / 'SNAPSHOT_C2V001.json').write_text(json.dumps(d3, indent=1))
    pp, rp_ = provenance_fixture(c, out, 'FORGED')
    rc, o, o_ = handoff(c, fx3, pp, rp_, 'FORGED')
    check('T14.MUST_FAIL_handoff_on_a_self_consistent_forged_record_refused (double replay)', rc == 3 and not o_.exists()
          and 'REPLAY_MISMATCH' in o.get('reason', ''), o.get('reason', '')[:160])
    # Claude3's 1-of-N case: a re-registered record whose admitted roster is truncated
    fx4 = RUN / 'SNAP_FORGED_TRUNCATED'
    fx4.mkdir()
    tr = copy.deepcopy(run)
    tr['exploration']['admitted_points'] = [p for p in tr['exploration']['admitted_points']
                                            if p['log_index'] == d['u_A']['log_index']]
    tr['exploration_fingerprint'] = None
    w4 = E.write_calibration_record(run=tr, record_path=str(fx4 / 'REC.json'), registry_path=str(fx4 / 'REG.jsonl'))
    d4 = copy.deepcopy(d)
    d4['record'].update(file='REC.json', registry_file='REG.jsonl', record_file_sha256=w4['record_file_sha256'])
    d4['replay']['run_canonical_sha256'] = hashlib.sha256(E._canonical_bytes(tr)).hexdigest()
    (fx4 / 'SNAPSHOT_C2V001.json').write_text(json.dumps(d4, indent=1))
    rc, o, o_ = handoff(c, fx4, pp, rp_, 'TRUNCATED')
    check('T14.MUST_FAIL_handoff_on_a_truncated_roster_record_refused', w4.get('ok') and rc == 3 and not o_.exists(),
          o.get('reason', '')[:160])


def t15_v003g_budget_exhausted(S):
    c, out = S['seed'], S['seed_snap']
    _d, rec = rec_of(out)
    sel = G.select_representative_points(exploration=rec['run'], interior_count=6, spec=P.freeze_spec(c.ctx))
    ar = sel.get('admitted_region') or {}
    check('T15.v003g_runs_on_a_synthetic_BUDGET_EXHAUSTED_record', sel.get('ok') and
          ar.get('exploration_status') == 'BUDGET_EXHAUSTED' and 'EXPLORATION_STATUS_BUDGET_EXHAUSTED' in
          ar.get('truncation_evidence', []) and sel['admission_reverified'] is True,
          {'n_members': len(sel.get('points') or []), 'evidence': ar.get('truncation_evidence')})
    # MUST_FAIL: BUDGET_EXHAUSTED records v003g refuses (no admitted point; no identified direction)
    cp = campaign_of(c)
    _w0, _w, entries = cp.prefix()
    r3, _c3, s3 = cp.replay(entries, 3)
    ok, code = refused(lambda: P.v003g_members(c.ctx, r3, 0), 'V003G_REFUSED')
    check('T15.MUST_FAIL_v003g_on_BUDGET_EXHAUSTED_record_without_admitted_point_refused',
          s3 is None and r3['status'] == 'BUDGET_EXHAUSTED' and ok, code)
    noid = Camp('NOID_REC', (0.0, 0.0, 0.0), 1.0, const=True)
    for _ in range(3):
        noid.step()
    run = E.run_calibration_region(forward=lambda th: noid.fwd(noid.ctx.mapper.build(th)['spec']),
                                   **dict(noid.ctx.run_kwargs(), budget=7))
    sel = G.select_representative_points(exploration=run, interior_count=0, spec=P.freeze_spec(noid.ctx))
    check('T15.MUST_FAIL_v003g_refuses_BUDGET_EXHAUSTED_record_with_m_id_0 (freeze L1326)',
          run['status'] == 'BUDGET_EXHAUSTED' and not sel.get('ok') and 'no identified directions' in sel.get('reasons', []),
          sel.get('reasons'))


def ngc_toy(u, kind):
    """SYNTHETIC NGC values: a function of u only (no NGC3198 data)."""
    if kind == 'const':
        return [150.0] * 43
    if kind == 'linear':
        return [150.0 + (j + 1) * (3.0 * u[0] - 2.0 * u[1] + 0.5 * u[2]) for j in range(43)]
    return [150.0 + (j + 1) * (3.0 * u[0] + 40.0 * (u[0] - 0.5) ** 2 - 2.0 * u[1] + 0.5 * u[2]) for j in range(43)]


def values_file(path, fd, kind, invalid=None, eps=0.01, eps_none_rows=()):
    rd = path.parent / (path.stem + '_RESULTS')
    rd.mkdir()
    pts = []
    for role, key, u in [('u_A', [m['key'] for m in fd['members'] if m['log_index'] == fd['u_A']['log_index']][0],
                          fd['u_A']['u'])] + [(f['role'], f['key'], f['u']) for f in fd['F']]:
        rf = rd / ('%s.json' % role)
        rf.write_text(json.dumps({'synthetic_toy_result': True, 'key': key}))
        v = ngc_toy(u, kind)
        valid = [True] * 43
        if invalid and role in invalid:
            for q in invalid[role]:
                valid[q] = False
        pts.append({'role': role, 'theta_key': key, 'result_pin': pin(rf), 'valid': valid,
                    'speeds_km_s': [x if ok else None for x, ok in zip(v, valid)],
                    'eps_km_s': [None if q in eps_none_rows else eps for q in range(43)]})
    path.write_text(json.dumps({'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, indent=1))
    return path


def band_cli(S, vals, tag, seal=True, seal_sha=None):
    out = S['seed_snap']
    seal_p = FIX / 'SYNTHETIC_R3A_SEAL.json'
    if not seal_p.exists():
        seal_p.write_text('{"synthetic_seal": true}')
    args = ['band', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--fdplan', S['seed_fd'], '--fdplan-sha256',
            sha(S['seed_fd']), '--values', vals, '--values-sha256', sha(vals), '--out-dir', RUN / ('L1_' + tag)]
    if seal:
        args += ['--seal-path', seal_p, '--seal-sha256', seal_sha or sha(seal_p)]
    rc, o = tool(*args)
    return rc, o, RUN / ('L1_' + tag)


def t16_band(S):
    fd = json.loads(Path(S['seed_fd']).read_text())
    vals = values_file(FIX / 'VALUES_LINEAR.json', fd, 'linear', invalid={'F1': [4]}, eps_none_rows=(7,))
    rc, o, l1d = band_cli(S, vals, 'NOSEAL', seal=False)
    check('T16.MUST_FAIL_band_without_the_seal_sha_refused', rc == 3 and 'NO_SEAL' in o.get('reason', '') and
          not l1d.exists(), o.get('reason'))
    rc, o, l1d = band_cli(S, vals, 'BADSEAL', seal_sha='1' * 64)
    check('T16.MUST_FAIL_band_with_a_wrong_seal_sha_refused', rc == 3 and not l1d.exists(), o.get('reason'))
    rc, o, l1d = band_cli(S, vals, 'LINEAR')
    l1 = json.loads((l1d / 'L1_C2V001.json').read_text()) if rc == 0 else {'rows': []}
    rows = {r['id']: r for r in l1['rows']}
    r4 = rows.get(QIDS[4], {})
    check('T17.MUST_FAIL_INVALID_FD_row_reads_NOT_AVAILABLE_never_zero_width',
          r4.get('status') == 'NOT_AVAILABLE' and 'lo' not in r4 and 'width' not in r4, r4)
    check('T17.FD_noise_unbounded_row_flagged', rows.get(QIDS[7], {}).get('fd_noise') == 'FD_NOISE_NOT_BOUNDED',
          rows.get(QIDS[7], {}).get('fd_noise'))
    # independent check of the band: K recovered for the linear toy, optima feasible, random feasible c inside
    import numpy as np
    _d, rec = rec_of(S['seed_snap'])
    L = P.linear_model(E, rec['run'])
    m = len(L['I'])
    A = np.vstack([L['S'] @ L['VI'].T, -(L['S'] @ L['VI'].T), L['VI'].T, -L['VI'].T, np.eye(m), -np.eye(m)])
    r = 0.25 / math.sqrt(m)
    b = np.concatenate([L['zrow'] - L['qA'], L['zrow'] + L['qA'], 1 - L['uA'], L['uA'], np.full(m, r), np.full(m, r)])
    rng = np.random.default_rng(12345)
    cs = [c_ for c_ in rng.uniform(-r, r, size=(20000, m)) if np.all(A @ c_ <= b + 1e-12)]
    bad = []
    for j, q in enumerate(QIDS):
        x = rows[q]
        if x['status'] != 'AVAILABLE':
            continue
        Kt = np.array([3.0, -2.0, 0.5]) * (j + 1)
        w = L['VI'] @ Kt
        if np.max(np.abs(np.array(x['K_q']) - Kt)) > 1e-6 * (j + 1):
            bad.append((q, 'K'))
        vals_ = [float(w @ c_) for c_ in cs]
        if vals_ and (min(vals_) < x['lo'] - x['g_A'] - 1e-9 or max(vals_) > x['hi'] - x['g_A'] + 1e-9):
            bad.append((q, 'sample outside'))
        for key in ('du_at_lo', 'du_at_hi'):
            du = np.array(x[key])
            cc = L['VI'] @ du
            if np.any(A @ cc > b + 1e-9):
                bad.append((q, key + ' infeasible'))
    check('T17.band_LP_bounds_independently_verified (feasible optima, %d sampled points inside)' % len(cs),
          rc == 0 and not bad and l1['n_available'] == 42 and l1['label'] == P.BAND_LABEL, {'bad': bad[:4]})
    S['l1'] = l1d / 'L1_C2V001.json'
    S['vals1'] = vals
    # a non-OPTIMAL program reads NOT_AVAILABLE (fault injected into the simplex for one objective)
    vd = json.loads(Path(vals).read_text())

    def lp_fault(A_, b_, w_):
        c_, st = E._lp_max(A_, b_, w_)
        return (c_, 'ITERATION_LIMIT') if abs(float(np.sum(w_))) > 0 and abs(float(w_[0]) - target) < 1e-12 else (c_, st)
    w10 = L['VI'] @ (np.array([3.0, -2.0, 0.5]) * 11)
    target = float(w10[0])
    rows2, _meta = P.band_rows(E, L, vd, fd['F'], lp=lp_fault)
    r10 = rows2[10]
    check('T18.MUST_FAIL_non_OPTIMAL_program_reads_NOT_AVAILABLE_not_filled', r10['status'] == 'NOT_AVAILABLE' and
          'lo' not in r10 and r10['reason'].startswith('LP_'), {'reason': r10.get('reason')})


def t19_phase2_agree(S):
    c, out = S['seed'], S['seed_snap']
    final = c.complete()
    rec2 = final['record']
    fd = json.loads(Path(S['seed_fd']).read_text())
    run2 = json.loads(Path(rec2['record_path']).read_text())['run']
    sel2 = P.v003g_members(c.ctx, run2, 6)
    u1 = {p['role']: p for p in json.loads(Path(S['vals1']).read_text())['points']}

    def members_file(name, kind, rebind=True):
        pts = []
        for m in sel2['points']:
            rf = FIX / ('%s_M%04d.json' % (name, m['log_index']))
            rf.write_text(json.dumps({'synthetic_toy_result': True, 'log_index': m['log_index']}))
            rp_ = u1['u_A']['result_pin'] if (rebind and m['log_index'] == fd['u_A']['log_index']) else pin(rf)
            pts.append({'role': 'member', 'log_index': m['log_index'], 'theta_key': O.theta_key(m['theta_natural']),
                        'member_valid': True, 'result_pin': rp_, 'valid': [True] * 43,
                        'speeds_km_s': ngc_toy(m['u'], kind)})
        p = FIX / ('%s.json' % name)
        p.write_text(json.dumps({'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, indent=1))
        return p

    def at0b(mp, tag):
        rc, o = tool('agree', 'at0b', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--phase2-record',
                     rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
                     rec2['registry_path'], '--values', S['vals1'], '--values-sha256', sha(S['vals1']), '--members', mp,
                     '--members-sha256', sha(mp), '--out-dir', RUN / ('AT0B_' + tag))
        return rc, o, RUN / ('AT0B_' + tag) / 'AT0B_C2V001.json'
    m_lin = members_file('MEMBERS_LINEAR', 'linear')
    rc, o, at0b_ok = at0b(m_lin, 'OK')
    check('T19.agree_at0b_PASS (anchor bitwise, first B_P1 entries, u_A re-binds by sha)', rc == 0 and not o['failures'],
          o)
    m_bad = members_file('MEMBERS_NOREBIND', 'linear', rebind=False)
    rc, o, at0b_bad = at0b(m_bad, 'NOREBIND')
    check('T19.MUST_FAIL_at0b_u_A_member_not_rebound_AGREEMENT_DEFECT', rc == 10 and o['failures'], o.get('failures'))
    S['at0b_defect'] = at0b_bad
    pa2 = run2['exploration']['primary_anchor']
    check('T19.phase2_primary_anchor_is_u_A_and_first_B_P1_entries_equal (oracle)',
          pa2['log_index'] == fd['u_A']['log_index'] and P.fhex(pa2['u']) == fd['u_A']['u_hex'], pa2['log_index'])


def t20_at1(S):
    c, out = S['seed'], S['seed_snap']
    fd = json.loads(Path(S['seed_fd']).read_text())
    final = c.final
    rec2 = final['record']
    run2 = json.loads(Path(rec2['record_path']).read_text())['run']
    sel2 = P.v003g_members(c.ctx, run2, 6)

    def pair(kind, tag):
        vals = values_file(FIX / ('VALUES_%s.json' % tag), fd, kind)
        u1 = {p['role']: p for p in json.loads(vals.read_text())['points']}
        pts = []
        for m in sel2['points']:
            rp_ = u1['u_A']['result_pin'] if m['log_index'] == fd['u_A']['log_index'] else None
            if rp_ is None:
                rf = FIX / ('%s_M%04d.json' % (tag, m['log_index']))
                rf.write_text(json.dumps({'synthetic_toy_result': True}))
                rp_ = pin(rf)
            pts.append({'role': 'member', 'log_index': m['log_index'], 'theta_key': O.theta_key(m['theta_natural']),
                        'member_valid': True, 'result_pin': rp_, 'valid': [True] * 43, 'speeds_km_s': ngc_toy(m['u'], kind)})
        mp = FIX / ('MEMBERS_%s.json' % tag)
        mp.write_text(json.dumps({'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, indent=1))
        rc, o, l1d = band_cli(S, vals, tag)
        rcb, ob = tool('agree', 'at0b', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--phase2-record',
                       rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
                       rec2['registry_path'], '--values', vals, '--values-sha256', sha(vals), '--members', mp,
                       '--members-sha256', sha(mp), '--out-dir', RUN / ('AT0B_' + tag))
        a0b = RUN / ('AT0B_' + tag) / 'AT0B_C2V001.json'
        l1 = l1d / 'L1_C2V001.json'
        rc1, o1 = tool('agree', 'at1', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--l1', l1, '--l1-sha256',
                       sha(l1), '--fdplan', S['seed_fd'], '--fdplan-sha256', sha(S['seed_fd']), '--at0a', S['seed_at0a'],
                       '--at0a-sha256', sha(S['seed_at0a']), '--at0b', a0b, '--at0b-sha256', sha(a0b), '--phase2-record',
                       rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
                       rec2['registry_path'], '--members', mp, '--members-sha256', sha(mp), '--config', c.cfg,
                       '--config-sha256', c.cfg_sha, '--interior-count', 6, '--out-dir', RUN / ('AT1_' + tag))
        doc = json.loads((RUN / ('AT1_' + tag) / 'AT1_C2V001.json').read_text()) if rc1 in (0, 10) else {}
        return rcb, rc1, o1, doc, l1
    rcb, rc1, o1, doc, _l1 = pair('const', 'C1')
    check('T21.agree_at1_COVERED (constant NGC toy, AT-0 PASS)', rcb == 0 and rc1 == 0 and doc.get('outcome') == 'COVERED',
          {'at0b_rc': rcb, 'rc': rc1, 'outcome': doc.get('outcome'), 'reason': o1.get('reason')})
    rcb, rc1, o1, doc, l1 = pair('quad', 'Q1')
    import numpy as np
    _d, rec = rec_of(out)
    L = P.linear_model(E, rec['run'])
    r = 0.25 / math.sqrt(len(L['I']))
    cats_ok = True
    for f in doc.get('failing') or []:
        u = [p for p in run2['exploration']['admitted_points'] if p['log_index'] == f['log_index']][0]['u']
        cvec = L['VI'] @ (np.array(u) - L['uA'])
        lin = L['qA'] + L['S'] @ (L['VI'].T @ cvec)
        want = ('OUTSIDE_TRUST_RADIUS' if np.any(np.abs(cvec) > r) else
                'OUTSIDE_LINEAR_DDO_REGION' if np.any(np.abs(lin) > L['zrow']) else 'NGC_NONLINEAR')
        cats_ok &= f['category'] == want and f['excess'] > 0
    rep = doc.get('reported') or {}
    check('T22.agree_at1_SUPERSEDED_with_categories_and_reported_lines (nonlinear NGC toy)',
          rcb == 0 and rc1 == 0 and doc.get('outcome') == 'SUPERSEDED' and cats_ok and
          'max_ddo_linearity_deviation_over_tau' in rep and rep.get('ngc_linearity_residuals'),
          {'outcome': doc.get('outcome'), 'n_failing': len(doc.get('failing') or []),
           'categories': sorted(set(f['category'] for f in doc.get('failing') or []))})
    a0b_bad = S['at0b_defect']
    rc1, o1 = tool('agree', 'at1', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--l1', _l1, '--l1-sha256',
                   sha(_l1), '--fdplan', S['seed_fd'], '--fdplan-sha256', sha(S['seed_fd']), '--at0a', S['seed_at0a'],
                   '--at0a-sha256', sha(S['seed_at0a']), '--at0b', a0b_bad, '--at0b-sha256', sha(a0b_bad),
                   '--phase2-record', rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'],
                   '--phase2-registry', rec2['registry_path'], '--members', FIX / 'MEMBERS_C1.json', '--members-sha256',
                   sha(FIX / 'MEMBERS_C1.json'), '--config', c.cfg, '--config-sha256', c.cfg_sha, '--interior-count', 6,
                   '--out-dir', RUN / 'AT1_DEFECT')
    check('T23.MUST_FAIL_at1_with_AT0_defect_reads_AGREEMENT_DEFECT', rc1 == 10 and o1.get('outcome') == 'AGREEMENT_DEFECT',
          {'rc': rc1, 'outcome': o1.get('outcome')})


def t25_categories(S):
    """AT-1 inequality and categories on hand-placed Phase-2 points (in process, JAC snapshot, sigma 0.1)."""
    c, out = S['JAC']
    d, rec = rec_of(out)
    rc, o = tool('fdplan', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--snapshot', out, '--snapshot-sha256',
                 snap_sha(out), '--interior-count', 6, '--out-dir', RUN / 'FD_JAC_T25')
    fd = json.loads((RUN / 'FD_JAC_T25' / 'FDPLAN_C2V001.json').read_text())
    vals = json.loads(values_file(FIX / 'VALUES_JAC_LINEAR.json', fd, 'linear').read_text())
    L = P.linear_model(E, rec['run'])
    rows, _m = P.band_rows(E, L, vals, fd['F'])
    l1 = {'rows': rows, 'fd_du': [f['du'] for f in fd['F']]}
    r = 0.25 / math.sqrt(len(L['I']))
    import numpy as np
    m = len(L['I'])
    A = np.vstack([L['S'] @ L['VI'].T, -(L['S'] @ L['VI'].T), L['VI'].T, -L['VI'].T, np.eye(m), -np.eye(m)])
    b = np.concatenate([L['zrow'] - L['qA'], L['zrow'] + L['qA'], 1 - L['uA'], L['uA'], np.full(m, r), np.full(m, r)])
    span = np.abs(np.linalg.pinv(L['S'] @ L['VI'].T)).sum(axis=1).max() * (L['zrow'] + np.abs(L['qA'])).max()
    rng = np.random.default_rng(54321)
    cs = [c_ for c_ in rng.uniform(-min(r, span), min(r, span), size=(40000, m)) if np.all(A @ c_ <= b + 1e-12)]
    bad, binding = [], 0
    for x in rows:
        if x['status'] != 'AVAILABLE':
            bad.append((x['id'], 'not available'))
            continue
        w = np.array(x['K_q_VI'])
        vv = [float(w @ c_) for c_ in cs]
        if min(vv) < x['lo'] - x['g_A'] - 1e-9 or max(vv) > x['hi'] - x['g_A'] + 1e-9:
            bad.append((x['id'], 'sample outside'))
        for key in ('du_at_lo', 'du_at_hi'):
            if np.any(A @ (L['VI'] @ np.array(x[key])) > b + 1e-9):
                bad.append((x['id'], key))
        binding += (x['hi'] - x['g_A']) < r * float(np.abs(w).sum()) - 1e-9
    check('T25.band_with_binding_DDO_rows_independently_verified (%d sampled points inside)' % len(cs),
          not bad and binding == len(rows) and len(cs) > 100, {'bad': bad[:4], 'rows_narrower_than_trust_box': binding})
    v0 = L['V'][L['I'][0]]
    places = {101: (0.5 * r, 'OUTSIDE_LINEAR_DDO_REGION', 50.0), 102: (1.5 * r, 'OUTSIDE_TRUST_RADIUS', 0.0),
              103: (1e-4, 'NGC_NONLINEAR', 50.0), 104: (1e-4, None, 0.0)}
    pts, mv = [], {}
    for li, (t, _cat, bump) in places.items():
        u = list(L['uA'] + t * v0)
        pts.append({'log_index': li, 'u': u, 'prediction': {'speeds_km_s': toy_speeds(tuple(2 * x - 1 for x in u))}})
        g = ngc_toy(u, 'linear')
        mv[li] = {'valid': [True] * 43, 'speeds_km_s': [x + bump * (j + 1) for j, x in enumerate(g)]}
    fails, rep = P.at1_rows(E, L, l1, {'exploration': {'admitted_points': pts}}, mv, QIDS)
    got = {}
    for f in fails:
        got.setdefault(f['log_index'], set()).add(f['category'])
    want_lin = abs(L['qA'] + L['S'] @ (L['VI'].T @ (L['VI'] @ (0.5 * r * v0)))).max() > L['zrow'].min()
    ok = (got.get(102) == {'OUTSIDE_TRUST_RADIUS'} and got.get(103) == {'NGC_NONLINEAR'} and 104 not in got and
          got.get(101) == {'OUTSIDE_LINEAR_DDO_REGION'} and want_lin)
    check('T25.AT1_categories_trust_radius_linear_DDO_region_NGC_nonlinear', ok,
          {k: sorted(v) for k, v in got.items()})
    check('T25.AT1_linear_member_inside_region_is_covered', 104 not in got, None)


def t26_snapshot_race_free(S):
    """After the whole campaign has run (Phase 2), a new snapshot of the same config equals the early one."""
    c, out = S['seed'], S['seed_snap']
    rc, o, out2 = snap(c, 'SEED_AFTER_COMPLETION')
    d1, _r1 = rec_of(out)
    d2, _r2 = rec_of(out2) if rc == 0 else ({}, {})
    check('T26.snapshot_after_campaign_completion_equals_early_snapshot', rc == 0 and d2['b_p1'] == d1['b_p1'] and
          d2['replay']['run_canonical_sha256'] == d1['replay']['run_canonical_sha256'] and d2['u_A'] == d1['u_A'],
          {'rc': rc, 'reason': o.get('reason')})
    rc, o = tool('agree', 'at0a', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--config', c.cfg,
                 '--config-sha256', c.cfg_sha, '--s0', S['s0'], '--s0-sha256', sha(S['s0']), '--out-dir',
                 RUN / 'AT0A_SEED_AFTER_COMPLETION')
    check('T26.at0a_still_PASS_after_campaign_completion', rc == 0 and o.get('failures') == [], o.get('failures'))


def t24_at0a_tamper(S):
    c = Camp('TAMPER', (0.0, 0.0, 0.0), 1.0)
    assert c.until_march0_planned()
    rc, o, out = snap(c, 'TAMPER')
    rc0, o0 = tool('fdplan', '--s0-only', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', RUN / 'S0_TAMPER')
    s0 = RUN / 'S0_TAMPER' / 'S0_C2V001.json'
    wp = c.orc.waves_dir / 'wave_0004' / 'WAVE_PLAN.json'
    plan = json.loads(wp.read_text())
    k = sorted(plan['calls'][0]['theta'])[0]
    plan['calls'][0]['theta'][k] = math.nextafter(plan['calls'][0]['theta'][k], math.inf)
    os.chmod(wp, 0o644)
    wp.write_text(json.dumps(plan, indent=1, sort_keys=True))
    rc, o = tool('agree', 'at0a', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--config', c.cfg,
                 '--config-sha256', c.cfg_sha, '--s0', s0, '--s0-sha256', sha(s0), '--out-dir', RUN / 'AT0A_TAMPER')
    check('T24.MUST_FAIL_at0a_march0_plan_differs_from_next_requested_AGREEMENT_DEFECT',
          rc == 10 and any('march0' in f for f in o.get('failures') or []), o.get('failures'))
    s0d = json.loads(s0.read_text())
    s0d['points'][1]['theta_hex'] = dict(s0d['points'][1]['theta_hex'], common_scale_s='0x1.0p-3')
    s0b = FIX / 'S0_BITS_ALTERED.json'
    s0b.write_text(json.dumps(s0d))
    rc, o = tool('agree', 'at0a', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--config', c.cfg,
                 '--config-sha256', c.cfg_sha, '--s0', s0b, '--s0-sha256', sha(s0b), '--out-dir', RUN / 'AT0A_S0BITS')
    check('T24.MUST_FAIL_at0a_S0_theta_bits_differ_AGREEMENT_DEFECT',
          rc == 10 and any('S0' in f for f in o.get('failures') or []), o.get('failures'))


def main():
    RUN.mkdir(parents=True)
    FIX.mkdir()
    sys.addaudithook(_audit)
    S = {}
    guard('T00', t00_pins)
    guard('T01', lambda: t01_seed(S))
    guard('T03', lambda: t03_s0_fd(S))
    guard('T05', side_rule_unit)
    guard('T06', lambda: t06_handoff(S))
    guard('T08', lambda: t08_at0a(S))
    guard('T09', lambda: t09_scenarios(S))
    guard('T10', lambda: t10_terminal(S))
    guard('T11', lambda: t11_not_ready(S))
    guard('T12', lambda: t12_off_by_one_and_replay(S))
    guard('T14', lambda: t14_anchor(S))
    guard('T15', lambda: t15_v003g_budget_exhausted(S))
    guard('T16', lambda: t16_band(S))
    guard('T19', lambda: t19_phase2_agree(S))
    guard('T21', lambda: t20_at1(S))
    guard('T25', lambda: t25_categories(S))
    guard('T26', lambda: t26_snapshot_race_free(S))
    guard('T24', lambda: t24_at0a_tamper(S))
    n_pass = sum(1 for r in RESULTS if r['pass'])
    summary = {'run_dir': str(RUN), 'n': len(RESULTS), 'pass': n_pass, 'fail': len(RESULTS) - n_pass,
               'must_fail': sum(1 for r in RESULTS if 'MUST_FAIL' in r['id']),
               'must_fail_pass': sum(1 for r in RESULTS if 'MUST_FAIL' in r['id'] and r['pass']),
               'audit_denied': AUDIT['denied'], 'tool_sha256': sha(TOOL), 'test_sha256': sha(__file__)}
    with open(RUN / 'RESULTS.json', 'x') as fh:
        json.dump({'summary': summary, 'results': RESULTS}, fh, indent=1, default=str)
    print(json.dumps(summary, indent=1))
    return 0 if summary['fail'] == 0 and not AUDIT['denied'] else 1


if __name__ == '__main__':
    sys.exit(main())
