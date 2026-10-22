"""Tests for phase1_c2v002 (A137 successor of phase1_c2v001: L5 and N-B only).  SYNTHETIC ONLY.

Part 1 (T00-T26): every test of test_phase1_c2v001.py (156f0bef) ported against v002 (A133 section 5 MUST_FAIL list +
MUST_PASS).  Part 2 (R01): regression -- every CLI call of part 1 is also run with v001 (34eaef36, untouched) on the same
inputs and into the same out-dir path (v001's directory is moved aside to <out>.V001_SHADOW before v002 runs).  Exit
codes, stdout and every output file must be byte-identical after substituting v001's value for exactly these fields:
module, tool_sha256 (tool identity); the engine record's created_utc and the shas that hash it (record_sha256,
record_file_sha256, registry line_sha256; they differ between any two v001 runs too); for at1 only, the N-B fields
(outcome, failing, e_q_reading, reported.e_q_per_member_row).  The one v001 fixture whose first non-prefix family is
not march0 (T10.NOID, m_id = 0 at the 'design' wave) may differ only in prefix_waves and the recorded wave.  Part 3
(T27-T29): A137 L5 (corner anchor, MUST_PASS and MUST_FAIL) and N-B (e_q member-displacement reading).

Synthetic campaigns are built by the REAL orchestrator c2v005 (Context, Probe, make_plan, _commit_plan, run_wave,
ingest, finalise) with its in-process test executor, a toy forward and a synthetic 12-row region, on the real coordinate
spec V002 (engine c2v003b), the real addendum V005A (A13: 3 free coordinates) and the real taxonomy V003.  The tool runs
through its CLI as root would run it (a subprocess of the campaign interpreter), except where a test injects a fault in
process.  Oracle: a direct engine run with the same forward (its primary_anchor and the index of its first 'march' call;
for L5 the first call whose Probe family is outside PREFIX_FAMILIES).  No project forward, no NGC3198 data or targets:
NGC values are a toy function of u.  Writes only under phase1_c2/test_runs_v002/RUN_<UTC>_<pid>/ (an audit hook refuses
any other write, and any open of a path with an 'ngc3198' or 'uvt_' component).

usage: <codex python3> -I -B test_phase1_c2v002.py
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
TOOL = HERE / 'phase1_c2v002.py'
V001 = (HERE / 'phase1_c2v001.py', '34eaef36586aec77b3436d6bcd96d0a2948aef699d612077e2d6f9f32e4cd99c')
V001_TESTS = (HERE / 'test_phase1_c2v001.py', '156f0bef3a9962774257f3737eaa61c7d7df26a2d3fdb7ebb5de81847ee83fac')
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
RUN = HERE / 'test_runs_v002' / ('RUN_%s_%d' % (STAMP, os.getpid()))
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


def corner_speeds(a, const=False):
    """SYNTHETIC toy for A137 L5 (Claude3 0191 verifier P7): depends on a0 + a1 only, so m_id = 1 along ~(1, 1, 0)."""
    return {r: 40.0 + 8.0 * math.sqrt(rad) + (3.0 + 0.5 * rad) * (a[0] + a[1]) for r, rad in zip(ROWS, RADII)}


def forward_factory(invalid=None, const=False, speeds=None):
    sp = speeds or toy_speeds

    def fwd(spec):
        a = a_of_spec(spec)
        if invalid is not None and invalid(a):
            return {'valid': False, 'speeds_km_s': {}, 'reasons': ['TOY_INVALID']}
        return {'valid': True, 'speeds_km_s': sp(a, const), 'reasons': []}
    return fwd


def write_region(path, truth, sigma, const=False, speeds=None):
    v = (speeds or toy_speeds)(truth, const)
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

    def __init__(self, tag, truth, sigma, invalid=None, const=False, override=None, speeds=None):
        self.dir = RUN / tag
        self.dir.mkdir(parents=True)
        region = write_region(self.dir / 'SYNTHETIC_REGION.json', truth, sigma, const, speeds)
        cfg = make_config(self.dir / 'work', region, override)
        self.cfg = self.dir / 'CONFIG.json'
        with open(self.cfg, 'x') as fh:
            json.dump(cfg, fh, indent=1)
        self.cfg_sha = sha(self.cfg)
        self.fwd = forward_factory(invalid, const, speeds)
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

    def peek(self):
        """The families the probe would plan next (nothing committed); None when the probe is complete."""
        pr = self.orc.probe.run(self.orc.cache, 'probe')
        if pr['complete']:
            return None
        return sorted(set(tuple(m['family']) for m in self.orc._dedup(pr['misses'])))

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
SHADOW = {'on': True, 'log': []}
SNAP_RECORD_VOLATILE = ('record_file_sha256', 'record_sha256', 'registry_line_sha256')
REGISTRY_VOLATILE = ('created_utc', 'record_file_sha256', 'line_sha256')


def cli(path, args):
    env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    p = subprocess.run([PY, '-I', '-B', str(path)] + [str(x) for x in args], capture_output=True, text=True, env=env)
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = {'unparsed': p.stdout[-1500:], 'stderr': p.stderr[-1500:]}
    return p.returncode, out


def tool(*args):
    """v002 through its CLI.  While SHADOW is on (part 1), v001 runs first on the same arguments; its out dir is moved
    aside to <out>.V001_SHADOW, v002 then writes the same path, and the two results are compared (R01)."""
    args = [str(x) for x in args]
    if not SHADOW['on']:
        return cli(TOOL, args)
    od = args[args.index('--out-dir') + 1] if '--out-dir' in args else None
    pre = od is not None and os.path.lexists(od)
    rc1, o1 = cli(V001[0], args)
    d1 = None
    if od is not None and not pre and os.path.lexists(od):
        d1 = od + '.V001_SHADOW'
        os.rename(od, d1)
    rc2, o2 = cli(TOOL, args)
    d2 = od if (od is not None and not pre and os.path.lexists(od)) else None
    SHADOW['log'].append(shadow_compare(args, rc1, o1, d1, rc2, o2, d2))
    return rc2, o2


def same_bytes(name, raw1, raw2):
    """(identical after the named substitutions?, substituted fields, L5 non-march0 keys, N-B changed?)"""
    if raw1 == raw2:
        return True, [], None, False
    if name.endswith('.jsonl'):
        a_, b_ = raw1.split(b'\n'), raw2.split(b'\n')
        if len(a_) != len(b_):
            return False, [], None, False
        rebuilt = []
        for x, y in zip(a_, b_):
            if not x or not y:
                rebuilt.append(y)
                continue
            jx, jy = json.loads(x), json.loads(y)
            for k in REGISTRY_VOLATILE:
                if k in jx and k in jy:
                    jy[k] = jx[k]
            rebuilt.append(E._canonical_bytes(jy))
        return b'\n'.join(rebuilt) == raw1, list(REGISTRY_VOLATILE), None, False
    j1, j2 = json.loads(raw1), json.loads(raw2)
    if name.startswith('PHASE1_CALIBRATION_RECORD_'):
        for k in ('created_utc', 'record_sha256'):
            j2[k] = j1.get(k)
        return E._canonical_bytes(j2) == raw1, ['created_utc', 'record_sha256'], None, False
    subst = [k for k in ('module', 'tool_sha256') if k in j1 and k in j2]
    for k in subst:
        j2[k] = j1[k]
    if name == 'SNAPSHOT_C2V001.json' and isinstance(j1.get('record'), dict) and isinstance(j2.get('record'), dict):
        for k in SNAP_RECORD_VOLATILE:
            j2['record'][k] = j1['record'].get(k)
        subst += ['record.' + k for k in SNAP_RECORD_VOLATILE]
    if 'first_non_prefix_wave' in j2:   # L5: the first non-prefix family is not march0 (outside the identity scope)
        return False, subst, sorted(k for k in set(j1) | set(j2) if j1.get(k) != j2.get(k)), False
    nb = False
    if name == 'AT1_C2V001.json':
        nb = (j1.get('outcome'), j1.get('failing')) != (j2.get('outcome'), j2.get('failing'))
        if nb:
            p1 = set((x['log_index'], x['id']) for x in j1.get('failing') or [])
            p2 = set((x['log_index'], x['id']) for x in j2.get('failing') or [])
            nb = {'outcome': [j1.get('outcome'), j2.get('outcome')], 'n_failing': [len(p1), len(p2)],
                  'only_v001': len(p1 - p2), 'only_v002': len(p2 - p1)}
        j2['outcome'], j2['failing'] = j1.get('outcome'), j1.get('failing')
        j2.pop('e_q_reading', None)
        (j2.get('reported') or {}).pop('e_q_per_member_row', None)
        subst += ['N-B: outcome, failing, e_q_reading, reported.e_q_per_member_row']
    return P.jbytes(j2) == raw1, subst, None, nb


def shadow_compare(args, rc1, o1, d1, rc2, o2, d2):
    cmd = args[0] + (' ' + args[1] if args[0] == 'agree' and len(args) > 1 else '')
    r = {'cmd': cmd, 'out': d2 or d1, 'rc': [rc1, rc2], 'diffs': [], 'subst': [], 'l5_non_march0': None,
         'nb_changed': False}
    if rc1 != rc2:
        r['diffs'].append('exit code %s != %s' % (rc1, rc2))
    s1, s2 = dict(o1), dict(o2)
    for s in (s1, s2):
        if isinstance(s.get('files'), dict):
            s['files'] = sorted(s['files'])
    if cmd == 'agree at1':
        for k in ('outcome', 'n_failing'):
            if k in s1 and s1.get(k) != s2.get(k):
                r['nb_changed'] = True
                s2[k] = s1[k]
    if s1 != s2:
        r['diffs'].append('stdout %s != %s' % (json.dumps(s1)[:300], json.dumps(s2)[:300]))
    n1 = sorted(os.listdir(d1)) if d1 else []
    n2 = sorted(os.listdir(d2)) if d2 else []
    if n1 != n2:
        r['diffs'].append('files %s != %s' % (n1, n2))
    for name in sorted(set(n1) & set(n2)):
        ok, subst, l5, nb = same_bytes(name, (Path(d1) / name).read_bytes(), (Path(d2) / name).read_bytes())
        r['subst'] = sorted(set(r['subst']) | set(subst))
        if nb:
            r['nb_changed'] = nb
        if l5 is not None:
            r['l5_non_march0'] = {'file': name, 'differing_keys': l5}
        elif not ok:
            r['diffs'].append('%s differs beyond the named fields' % name)
    return r


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
    check('T00.v001_tool_and_tests_untouched', sha(V001[0]) == V001[1] and sha(V001_TESTS[0]) == V001_TESTS[1] and
          P.MODULE == 'phase1_c2v002' and P.PREFIX_FAMILIES == ('seed', 'jacobian', 'repair', 'gd_pre'),
          {'v001': sha(V001[0])[:16], 'v001_tests': sha(V001_TESTS[0])[:16]})


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
    S['at1_q1'] = (doc, l1, FIX / 'MEMBERS_Q1.json', run2)
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


# ----------------------------------------------------------------------------------------------- R01 (regression)
def r01_regression(S):
    """Every part-1 CLI call ran under v001 and v002 on identical inputs into the same out-dir path."""
    groups = {}
    for r in SHADOW['log']:
        groups.setdefault(r['cmd'], []).append(r)
    for cmd in ('snapshot', 'fdplan', 'handoff', 'band', 'agree at0a', 'agree at0b', 'agree at1'):
        rs = groups.get(cmd, [])
        bad = [r for r in rs if r['diffs'] or (r['l5_non_march0'] and cmd != 'snapshot')]
        ident = [r for r in rs if not r['diffs'] and r['l5_non_march0'] is None]
        check('R01.regression_v001_shadow_%s_byte_identical_except_named_fields' % cmd.replace(' ', '_'),
              bool(rs) and not bad,
              {'calls': len(rs), 'identical': len(ident), 'exit_codes': sorted(set(r['rc'][1] for r in rs)),
               'substituted_fields': sorted(set(f for r in rs for f in r['subst'])),
               'at1_nb_changed_outcome_or_failing': [(os.path.basename(r['out'] or ''), r['nb_changed'])
                                                      for r in rs if r['nb_changed']],
               'bad': [(r['out'], r['diffs'][:2]) for r in bad][:4]})
    other = sorted(set(groups) - {'snapshot', 'fdplan', 'handoff', 'band', 'agree at0a', 'agree at0b', 'agree at1'})
    l5 = [r for r in SHADOW['log'] if r['l5_non_march0']]
    ok = not other and len(l5) == 1 and l5[0]['out'].endswith('/SNAP_NOID') and \
        set(l5[0]['l5_non_march0']['differing_keys']) == {'b_p1_rule', 'first_non_prefix_wave', 'prefix_waves'}
    det = {'other_commands': other, 'l5_calls': [(r['out'], r['l5_non_march0']) for r in l5]}
    if ok:
        j1 = json.loads((Path(l5[0]['out'] + '.V001_SHADOW') / 'SNAPSHOT_C2V001.json').read_text())
        j2 = json.loads((Path(l5[0]['out']) / 'SNAPSHOT_C2V001.json').read_text())
        w0 = j2['first_non_prefix_wave']['wave']
        ok = ([p for p in j1['prefix_waves'] if p['wave'] < w0] == j2['prefix_waves'] and j1['march0_wave'] is None
              and j2['march0_wave'] is None and j2['first_non_prefix_wave']['families'] == [['design']] and
              j2['phase1_status'] == j1['phase1_status'] == 'NO_IDENTIFIED_DIRECTION')
        det.update(v001_prefix_waves=[p['wave'] for p in j1['prefix_waves']],
                   v002_prefix_waves=[p['wave'] for p in j2['prefix_waves']], recorded_wave=w0)
    check('R01.only_the_NOID_fixture_has_a_non_march0_first_non_prefix_family_and_differs_only_in_prefix_waves_and_the_'
          'recorded_wave', ok, det)


# ----------------------------------------------------------------------------------------------- L5 (A137; 0191 L5)
def family_oracle(c):
    """Direct engine run with the campaign forward, every call classified by the orchestrator's own Probe.context."""
    probe = O.Probe(c.ctx)
    fams = []

    def fwd(theta):
        f = sys._getframe(1)
        fams.append((f.f_locals['entry']['index'], probe.context(f)['family'][0]))
        return c.fwd(c.ctx.mapper.build(theta)['spec'])
    run = c.ctx.E.run_calibration_region(forward=fwd, **c.ctx.run_kwargs())   # the engine instance the Probe reads
    first = next((i for i, fm in fams if fm not in P.PREFIX_FAMILIES), None)
    return {'first_non_prefix_index': first, 'first_non_prefix_family': dict(fams).get(first), 'families': fams,
            'n_calls_before': sum(1 for i, _f in fams if first is not None and i < first), 'run': run,
            'primary': (run.get('exploration') or {}).get('primary_anchor')}


def band_cli_on(snap_dir, fd_path, vals, tag):
    seal_p = FIX / 'SYNTHETIC_R3A_SEAL.json'
    if not seal_p.exists():
        seal_p.write_text('{"synthetic_seal": true}')
    rc, o = tool('band', '--snapshot', snap_dir, '--snapshot-sha256', snap_sha(snap_dir), '--fdplan', fd_path,
                 '--fdplan-sha256', sha(fd_path), '--values', vals, '--values-sha256', sha(vals), '--seal-path', seal_p,
                 '--seal-sha256', sha(seal_p), '--out-dir', RUN / ('L1_' + tag))
    return rc, o, RUN / ('L1_' + tag)


def at0a_cli(c, snap_dir, s0, tag):
    return tool('agree', 'at0a', '--snapshot', snap_dir, '--snapshot-sha256', snap_sha(snap_dir), '--config', c.cfg,
                '--config-sha256', c.cfg_sha, '--s0', s0, '--s0-sha256', sha(s0), '--out-dir', RUN / ('AT0A_' + tag))


def t27_corner(S):
    """MUST_PASS (A137 L5; Claude3 0191 L5): corner seed u = (1, 0, 0.5), both round-0 march sides closed at a box
    face, the campaign plans design then lp and never march0.  B_P1 = the calls before the 'design' family."""
    c = Camp('CORNER', (1.0, -1.0, 0.0), 1.0, override={'u_seed': [1.0, 0.0, 0.5]}, speeds=corner_speeds)
    S['corner'] = c
    fams = []
    while True:
        nxt = c.peek()
        if nxt is None or P.non_prefix_families(nxt):
            break
        fams.append(c.step())
    rc, o, out = snap(c, 'CORNER_BEFORE_PLAN')
    check('T27.MUST_FAIL_corner_B_P1_reached_but_the_first_non_prefix_wave_plan_not_written_NOT_READY',
          rc == 4 and not out.exists() and 'first non-prefix-family WAVE_PLAN' in o.get('reason', ''), o.get('reason'))
    fams.append(c.step(execute=False))
    orc_ = family_oracle(c)
    run = orc_['run']
    causes = (run.get('exploration') or {}).get('boundary_cause') or {}
    names = [f for _i, f in orc_['families']]
    first = orc_['first_non_prefix_index']
    log = run['evaluation_log']
    check('T27.corner_fixture_round0_sides_closed_at_a_face_no_march0_waves_seed_jac_jac_design (oracle)',
          fams == [[['seed']], [['jacobian']], [['jacobian']], [['design']]] and 'march0' not in names and
          bool(causes) and all(v == 'COMPUTATIONAL_BOX_FACE_NO_EVALUATION' for x in causes.values() for v in x.values())
          and orc_['first_non_prefix_family'] == 'design' and 'lp' in names and log[first]['purpose'] == 'global_design'
          and run['exploration']['global_design']['run_before_march'] is False,
          {'waves': fams, 'causes': causes, 'first_non_prefix': [first, orc_['first_non_prefix_family']],
           'm_id': len(run['identifiability']['identified']), 'families_after': sorted(set(names[first:]))})
    rcv, ov = cli(V001[0], ['snapshot', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir',
                            RUN / 'SNAP_CORNER_V001'])
    check('T27.v001_refuses_the_corner_REPLAY_STOPPED_FAMILY_design_BEFORE_MARCH0 (0191 L5 reproduced)',
          rcv == 3 and 'FAMILY_design_BEFORE_MARCH0' in ov.get('reason', '') and not (RUN / 'SNAP_CORNER_V001').exists(),
          ov.get('reason'))
    t0 = c.tree()
    rc, o, out = snap(c, 'CORNER')
    ok = rc == 0
    det = {'rc': rc, 'reason': o.get('reason'), 'oracle_first_non_prefix': first, 'oracle_calls_before': orc_['n_calls_before']}
    if ok:
        d, rec = rec_of(out)
        r1 = rec['run']
        pa = r1['exploration']['primary_anchor']
        v = E.verify_calibration_record(record_path=str(out / d['record']['file']),
                                        registry_path=str(out / d['record']['registry_file']))
        ok = (d['b_p1'] == first == orc_['n_calls_before'] == 5 and d['march0_wave'] is None and
              d['first_non_prefix_wave']['wave'] == 4 and d['first_non_prefix_wave']['families'] == [['design']] and
              d['boundary_call'] == {'log_index': 5, 'family': ['design'], 'stage_reached': 'global_design'} and
              d['b_p1_rule'] == P.B_P1_RULE and [p['wave'] for p in d['prefix_waves']] == [1, 2, 3] and
              r1['evaluation_log'] == log[:5] and rec['status'] == 'BUDGET_EXHAUSTED' and v['ok'] and
              r1['exploration']['stage_reached'] == 'global_design' and
              pa['log_index'] == orc_['primary']['log_index'] and pa['u'] == orc_['primary']['u'] and
              [x['family'][0] for x in d['prefix_calls']] == names[:5] and c.tree() == t0)
        det.update(b_p1=d['b_p1'], boundary_call=d['boundary_call'], u_A=[pa['log_index'], pa['source'], pa['u']],
                   v003g_role=d['v003g_anchor_check']['role'])
        S['corner_snap'] = out
    check('T27.MUST_PASS_corner_snapshot_B_P1_is_the_calls_before_design_equal_to_the_Probe_family_oracle', ok, det)
    rc0, o0 = tool('fdplan', '--s0-only', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', RUN / 'S0_CORNER')
    S['corner_s0'] = RUN / 'S0_CORNER' / 'S0_C2V001.json'
    rcf, of = tool('fdplan', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--snapshot', out, '--snapshot-sha256',
                   snap_sha(out), '--interior-count', 6, '--out-dir', RUN / 'FD_CORNER')
    fdp = RUN / 'FD_CORNER' / 'FDPLAN_C2V001.json'
    fd = json.loads(fdp.read_text()) if rcf == 0 else {}
    check('T27.MUST_PASS_corner_fdplan_S0_and_F (face sides minus/plus/plus, F from the record when u_A is the seed)',
          rc0 == 0 and rcf == 0 and [f['side'] for f in fd['F']] == ['minus', 'plus', 'plus'] and
          (fd['u_A']['source'] != 'seed' or all('record_log_index' in f for f in fd['F'])),
          {'rc': [rc0, rcf], 'sides': [f['side'] for f in fd.get('F') or []], 'source': (fd.get('u_A') or {}).get('source'),
           'n_distinct': fd.get('n_distinct_calls'), 'reason': of.get('reason')})
    S['corner_fd'] = fdp
    rc, o = at0a_cli(c, out, S['corner_s0'], 'CORNER')
    check('T27.MUST_PASS_corner_at0a_PASS (next requested thetas = the committed design plan)',
          rc == 0 and o.get('failures') == [], {'rc': rc, 'failures': o.get('failures'), 'reason': o.get('reason')})
    S['corner_at0a'] = RUN / 'AT0A_CORNER' / 'AT0A_C2V001.json'
    pp, rp = provenance_fixture(c, out, 'CORNER')
    rc, o, o_ = handoff(c, out, pp, rp, 'CORNER')
    d, _rec = rec_of(out)
    check('T27.MUST_PASS_corner_handoff (export, 10-field handoffs, u_A a member)',
          rc == 0 and d['u_A']['log_index'] in (o.get('members') or []), {'rc': rc, 'members': o.get('members'),
                                                                           'reason': o.get('reason')})
    vals = values_file(FIX / 'VALUES_CORNER.json', fd, 'linear')
    rc, o, l1d = band_cli_on(out, fdp, vals, 'CORNER')
    l1 = json.loads((l1d / 'L1_C2V001.json').read_text()) if rc == 0 else {}
    check('T27.MUST_PASS_corner_band_L1_written', rc == 0 and l1.get('n_available', 0) > 0,
          {'rc': rc, 'n_available': l1.get('n_available'), 'reason': o.get('reason')})
    # the whole campaign runs on (design, lp, ...); the snapshot and AT-0a do not move
    final = c.complete()
    rc, o, out2 = snap(c, 'CORNER_AFTER_COMPLETION')
    d2 = rec_of(out2)[0] if rc == 0 else {}
    check('T27.MUST_PASS_corner_snapshot_after_campaign_completion_equals_early_snapshot',
          rc == 0 and all(d2.get(k) == d.get(k) for k in ('b_p1', 'u_A', 'boundary_call', 'first_non_prefix_wave',
                                                           'prefix_calls', 'prefix_waves')) and
          d2['replay']['run_canonical_sha256'] == d['replay']['run_canonical_sha256'],
          {'rc': rc, 'reason': o.get('reason'), 'final_status': (final or {}).get('status')})
    rc, o = at0a_cli(c, out, S['corner_s0'], 'CORNER_AFTER_COMPLETION')
    check('T27.MUST_PASS_corner_at0a_still_PASS_after_campaign_completion', rc == 0 and o.get('failures') == [],
          o.get('failures'))
    rec2 = final['record']
    run2 = json.loads(Path(rec2['record_path']).read_text())['run']
    sel2 = P.v003g_members(c.ctx, run2, 6)
    u1 = {p['role']: p for p in json.loads(vals.read_text())['points']}
    pts = []
    for m in sel2['points']:
        if m['log_index'] == fd['u_A']['log_index']:
            rp_ = u1['u_A']['result_pin']
        else:
            rf = FIX / ('CORNER_M%04d.json' % m['log_index'])
            rf.write_text(json.dumps({'synthetic_toy_result': True, 'log_index': m['log_index']}))
            rp_ = pin(rf)
        pts.append({'role': 'member', 'log_index': m['log_index'], 'theta_key': O.theta_key(m['theta_natural']),
                    'member_valid': True, 'result_pin': rp_, 'valid': [True] * 43, 'speeds_km_s': ngc_toy(m['u'], 'linear')})
    mp = FIX / 'MEMBERS_CORNER.json'
    mp.write_text(json.dumps({'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, indent=1))
    rcb, ob = tool('agree', 'at0b', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--phase2-record',
                   rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
                   rec2['registry_path'], '--values', vals, '--values-sha256', sha(vals), '--members', mp,
                   '--members-sha256', sha(mp), '--out-dir', RUN / 'AT0B_CORNER')
    a0b = RUN / 'AT0B_CORNER' / 'AT0B_C2V001.json'
    l1p = l1d / 'L1_C2V001.json'
    rc1, o1 = tool('agree', 'at1', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--l1', l1p, '--l1-sha256',
                   sha(l1p), '--fdplan', fdp, '--fdplan-sha256', sha(fdp), '--at0a', S['corner_at0a'], '--at0a-sha256',
                   sha(S['corner_at0a']), '--at0b', a0b, '--at0b-sha256', sha(a0b), '--phase2-record',
                   rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
                   rec2['registry_path'], '--members', mp, '--members-sha256', sha(mp), '--config', c.cfg,
                   '--config-sha256', c.cfg_sha, '--interior-count', 6, '--out-dir', RUN / 'AT1_CORNER')
    check('T27.MUST_PASS_corner_at0b_PASS_and_at1_outcome_is_not_AGREEMENT_DEFECT (linear NGC toy)',
          rcb == 0 and ob.get('failures') == [] and rc1 == 0 and o1.get('outcome') in ('COVERED', 'SUPERSEDED'),
          {'at0b': [rcb, ob.get('failures'), ob.get('reason')], 'at1': [rc1, o1.get('outcome'), o1.get('n_failing'),
                                                                         o1.get('reason')]})


def t28_corner_must_fail(S):
    """MUST_FAIL (A137 L5): a non-prefix family appearing before the recorded boundary."""
    c, out = S['corner'], S['corner_snap']
    d, rec = rec_of(out)
    b, st = d['b_p1'], d['boundary_call']['stage_reached']
    cp = campaign_of(c)
    _w0, _waves, entries = cp.prefix()
    try:
        cp.snapshot_run(entries, b + 1, st)
        res = 'NO_REFUSAL'
    except P.Refused as exc:
        res = str(exc)
    check('T28.MUST_FAIL_replay_to_a_claimed_B_P1_plus_1_meets_design_before_it_refused',
          res.startswith('B_P1_WRONG') and "('FIRST_NON_PREFIX_design', %d)" % b in res, res)
    ok, code = refused(lambda: cp.snapshot_run(entries, b - 1, st), 'B_P1_WRONG')
    check('T28.MUST_FAIL_corner_B_P1_minus_1_refused', ok, code)
    # a self-consistent forged snapshot claiming B_P1 + 1: its record (a direct engine run at budget B_P1 + 1) holds the
    # design call at log index B_P1, i.e. a non-prefix family before the recorded boundary
    fx = RUN / 'SNAP_FORGED_CORNER_BP1_PLUS_1'
    fx.mkdir()
    run6 = E.run_calibration_region(forward=lambda th: c.fwd(c.ctx.mapper.build(th)['spec']),
                                    **dict(c.ctx.run_kwargs(), budget=b + 1))
    w6 = E.write_calibration_record(run=run6, record_path=str(fx / 'REC.json'), registry_path=str(fx / 'REG.jsonl'))
    d6 = copy.deepcopy(d)
    d6['b_p1'] = b + 1
    d6['boundary_call']['log_index'] = b + 1
    d6['record'].update(file='REC.json', registry_file='REG.jsonl', record_file_sha256=w6['record_file_sha256'])
    d6['replay']['run_canonical_sha256'] = hashlib.sha256(E._canonical_bytes(run6)).hexdigest()
    (fx / 'SNAPSHOT_C2V001.json').write_text(json.dumps(d6, indent=1))
    try:
        P.load_snapshot(str(fx), sha(fx / 'SNAPSHOT_C2V001.json'))
        loads = 'LOADS'
    except P.Refused as exc:
        loads = exc.code
    pp, rp_ = provenance_fixture(c, out, 'FORGED_CORNER')
    rc, o, o_ = handoff(c, fx, pp, rp_, 'FORGED_CORNER')
    reason = o.get('reason', '')
    check('T28.MUST_FAIL_non_prefix_family_before_the_recorded_boundary_handoff_refused (self-consistent B_P1+1 record)',
          w6.get('ok') and run6['evaluation_log'][b]['purpose'] == 'global_design' and rc == 3 and not o_.exists() and
          'B_P1_WRONG' in reason and 'FIRST_NON_PREFIX_design' in reason,
          {'load_snapshot': loads, 'rc': rc, 'reason': reason[:200]})
    rc, o = at0a_cli(c, fx, S['corner_s0'], 'FORGED_CORNER')
    check('T28.MUST_FAIL_non_prefix_family_before_the_recorded_boundary_at0a_AGREEMENT_DEFECT',
          rc == 10 and any(f.startswith('B_P1 B_P1 %d != snapshot %d' % (b, b + 1)) for f in o.get('failures') or []),
          o.get('failures'))
    # the corner record presented in the v001 (march0) form, and a doc carrying both forms
    m0w = {'wave': 4, 'plan_sha256': d['first_non_prefix_wave']['plan_sha256']}

    def as_march0_form(x):
        for k in ('first_non_prefix_wave', 'boundary_call', 'b_p1_rule'):
            x.pop(k)
        x['march0_wave'] = dict(m0w)

    def both_forms(x):
        x['march0_wave'] = dict(m0w)
    for tag, mutate, code in (('AS_MARCH0_FORM', as_march0_form, 'B_P1_WRONG'), ('BOTH_FORMS', both_forms, 'SNAPSHOT')):
        fxm = RUN / ('SNAP_CORNER_' + tag)
        fxm.mkdir()
        for f in (d['record']['file'], d['record']['registry_file']):
            (fxm / f).write_bytes((Path(out) / f).read_bytes())
        dm = copy.deepcopy(d)
        mutate(dm)
        (fxm / 'SNAPSHOT_C2V001.json').write_text(json.dumps(dm, indent=1))
        ok, got = refused(lambda: P.load_snapshot(str(fxm), sha(fxm / 'SNAPSHOT_C2V001.json')), code)
        check('T28.MUST_FAIL_corner_snapshot_%s_refused' % tag, ok, got)
    # a prefix wave plan edited to carry a non-prefix family (the jacobian wave 3 now plans ['lp', 1])
    wp = c.orc.waves_dir / 'wave_0003' / 'WAVE_PLAN.json'
    plan = json.loads(wp.read_text())
    plan['families'] = [['lp', 1]]
    for cl in plan['calls']:
        cl['family'] = ['lp', 1]
    os.chmod(wp, 0o644)
    wp.write_text(json.dumps(plan, indent=1, sort_keys=True))
    rc, o = at0a_cli(c, out, S['corner_s0'], 'CORNER_TAMPERED')
    check('T28.MUST_FAIL_non_prefix_family_wave_below_the_recorded_boundary_wave_at0a_AGREEMENT_DEFECT',
          rc == 10 and bool(o.get('failures')), o.get('failures'))
    pp2, rp2 = provenance_fixture(c, out, 'CORNER_TAMPERED')
    rc, o, o_ = handoff(c, out, pp2, rp2, 'CORNER_TAMPERED')
    check('T28.MUST_FAIL_non_prefix_family_wave_below_the_recorded_boundary_wave_handoff_PREFIX_MISMATCH',
          rc == 3 and not o_.exists() and 'PREFIX_MISMATCH' in o.get('reason', '') and
          'now wave 3, recorded 4' in o.get('reason', ''), o.get('reason'))
    rc, o, out3 = snap(c, 'CORNER_TAMPERED')
    check('T28.MUST_FAIL_snapshot_on_the_edited_prefix_writes_nothing', rc in (3, 4) and not out3.exists(),
          {'rc': rc, 'reason': o.get('reason')})


# ----------------------------------------------------------------------------------------------- N-B (A137; 0191 N-B)
def t29_nb(S):
    import numpy as np
    P1 = load(V001[0], 'phase1_v001_reference')   # v001's at1_rows, for the flip comparison only
    _d, rec = rec_of(S['seed_snap'])
    L = P.linear_model(E, rec['run'])
    fd = json.loads(Path(S['seed_fd']).read_text())
    h = np.array([abs(f['du']) for f in fd['F']])
    VN = L['V'][L['N']] if L['N'] else np.zeros((0, 3))
    v0 = L['V'][L['I'][0]]
    r = 0.25 / math.sqrt(len(L['I']))
    # Claude3 0191 verifier P8: eps exaggerated to 1 km/s so the noise term is visible; row q = 0
    vd = json.loads(Path(S['vals1']).read_text())
    for p in vd['points']:
        p['eps_km_s'] = [1.0] * 43
    rows, _m = P.band_rows(E, L, vd, fd['F'])
    l1 = {'rows': rows, 'fd_du': [f['du'] for f in fd['F']]}
    q, b = 0, rows[0]
    qid = vd['query_ids'][q]
    res = {}
    for name, t in (('far_member_t_3r', 3.0 * r), ('near_member_t_1e-4', 1e-4)):
        u = list(L['uA'] + t * v0)
        D = np.array(u) - L['uA']
        n = VN @ D
        shift = float(np.array(b['K_q']) @ (VN.T @ n)) if len(n) else 0.0
        e_v001 = max(b['fd_noise']['lo'], b['fd_noise']['hi']) + float(np.sum(2 * b['eps_q'] * np.abs(VN.T @ n) / h))
        e_mem = float(np.sum(2 * b['eps_q'] * np.abs(D) / h))
        hi_v001, hi_mem = b['hi'] + b['a_q'] + e_v001 + shift, b['hi'] + b['a_q'] + e_mem + shift
        g = 0.5 * (hi_v001 + hi_mem)   # between the two upper limits
        pts = [{'log_index': 7, 'u': u, 'prediction': {'speeds_km_s': {rr: float(x) for rr, x in zip(L['rows'], L['fA'])}}}]
        mv = {7: {'valid': [True] * 43, 'speeds_km_s': [g if j == q else rows[j].get('g_A', 150.0) for j in range(43)]}}
        run2 = {'exploration': {'admitted_points': pts}}
        f1, _r1 = P1.at1_rows(E, L, l1, run2, mv, vd['query_ids'])
        f2, r2 = P.at1_rows(E, L, l1, run2, mv, vd['query_ids'])
        eq = [x['e_q'] for x in r2['e_q_per_member_row'] if x['log_index'] == 7 and x['id'] == qid]
        res[name] = {'e_v001_band_optimum': e_v001, 'e_member_displacement': e_mem, 'g': g,
                     'v001_fails_row': any(x['id'] == qid for x in f1), 'v002_fails_row': any(x['id'] == qid for x in f2),
                     'v002_reported_e_q': eq}
    far, near = res['far_member_t_3r'], res['near_member_t_1e-4']
    ok = (far['v001_fails_row'] and not far['v002_fails_row'] and not near['v001_fails_row'] and near['v002_fails_row']
          and all(len(x['v002_reported_e_q']) == 1 and abs(x['v002_reported_e_q'][0] - x['e_member_displacement']) <=
                  1e-12 * max(1.0, x['e_member_displacement']) for x in res.values()))
    check('T29.N-B_exaggerated_eps_both_flip_directions_follow_the_member_displacement_reading (0191 verifier P8)',
          ok, res)
    # FD_NOISE_NOT_BOUNDED where eps is unavailable (T16's values: eps None on row 7)
    vd2 = json.loads(Path(S['vals1']).read_text())
    rows2, _m2 = P.band_rows(E, L, vd2, fd['F'])
    q7 = vd2['query_ids'][7]
    u = list(L['uA'] + 1e-4 * v0)
    mv = {8: {'valid': [True] * 43, 'speeds_km_s': [(rows2[7]['hi'] + 1000.0) if j == 7 else rows2[j].get('g_A', 150.0)
                                                    for j in range(43)]}}
    pts = [{'log_index': 8, 'u': u, 'prediction': {'speeds_km_s': {rr: float(x) for rr, x in zip(L['rows'], L['fA'])}}}]
    f2, r2 = P.at1_rows(E, L, {'rows': rows2, 'fd_du': [f['du'] for f in fd['F']]},
                        {'exploration': {'admitted_points': pts}}, mv, vd2['query_ids'])
    e7 = [x['e_q'] for x in r2['e_q_per_member_row'] if x['id'] == q7]
    fl = [x for x in f2 if x['id'] == q7]
    others = [x['e_q'] for x in r2['e_q_per_member_row'] if x['id'] != q7]
    check('T29.N-B_FD_NOISE_NOT_BOUNDED_where_eps_is_unavailable (per member and row; the failing entry is flagged)',
          rows2[7].get('fd_noise') == 'FD_NOISE_NOT_BOUNDED' and e7 == ['FD_NOISE_NOT_BOUNDED'] and len(fl) == 1 and
          fl[0]['flag'] == 'FD_NOISE_NOT_BOUNDED' and q7 in r2['rows_fd_noise_not_bounded'] and len(others) > 0 and
          all(isinstance(x, float) for x in others), {'e_q_row7': e7, 'failing_row7': fl})
    # the CLI at1 of record (T22, nonlinear toy): e_q per (member, row) equals an independent sum
    doc, l1p, _mp, run2 = S['at1_q1']
    l1d = json.loads(Path(l1p).read_text())
    rows1 = {x['id']: x for x in l1d['rows']}
    uA = np.array(fd['u_A']['u'])
    upos = {p['log_index']: np.array(p['u']) for p in run2['exploration']['admitted_points']}
    eqs = (doc.get('reported') or {}).get('e_q_per_member_row') or []
    bad = []
    for x in eqs:
        rr = rows1[x['id']]
        if isinstance(rr.get('fd_noise'), dict):
            want = sum(2.0 * rr['eps_q'] * abs(float(upos[x['log_index']][k] - uA[k])) / float(h[k]) for k in range(3))
            if not isinstance(x['e_q'], float) or abs(x['e_q'] - want) > 1e-12 * max(1.0, want):
                bad.append((x['log_index'], x['id'], x['e_q'], want))
        elif x['e_q'] != 'FD_NOISE_NOT_BOUNDED':
            bad.append((x['log_index'], x['id'], x['e_q'], 'FD_NOISE_NOT_BOUNDED'))
    pairs = sorted((x['log_index'], x['id']) for x in eqs)
    resid = sorted((x['log_index'], x['id']) for x in (doc.get('reported') or {}).get('ngc_linearity_residuals') or [])
    check('T29.at1_CLI_reports_e_q_per_member_and_row_equal_to_an_independent_member_displacement_sum (T22 Q1)',
          doc.get('e_q_reading') == P.E_Q_READING and pairs == resid and len(eqs) > 0 and not bad,
          {'n_pairs': len(eqs), 'bad': bad[:4], 'outcome': doc.get('outcome')})


def main():
    RUN.mkdir(parents=True)
    FIX.mkdir()
    sys.addaudithook(_audit)
    S = {}
    # part 1: the v001 tests, ported; every CLI call is shadow-run with v001 (R01)
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
    n_ported = len(RESULTS)
    # part 2: regression against v001
    SHADOW['on'] = False
    with open(RUN / 'SHADOW_REGRESSION_V001_V002.json', 'x') as fh:
        json.dump(SHADOW['log'], fh, indent=1, default=str)
    guard('R01', lambda: r01_regression(S))
    # part 3: A137 L5 and N-B
    guard('T27', lambda: t27_corner(S))
    guard('T28', lambda: t28_corner_must_fail(S))
    guard('T29', lambda: t29_nb(S))
    n_pass = sum(1 for r in RESULTS if r['pass'])
    summary = {'run_dir': str(RUN), 'n': len(RESULTS), 'pass': n_pass, 'fail': len(RESULTS) - n_pass,
               'n_ported_part1': n_ported, 'n_new': len(RESULTS) - n_ported,
               'shadow_cli_calls': len(SHADOW['log']),
               'must_fail': sum(1 for r in RESULTS if 'MUST_FAIL' in r['id']),
               'must_fail_pass': sum(1 for r in RESULTS if 'MUST_FAIL' in r['id'] and r['pass']),
               'audit_denied': AUDIT['denied'], 'tool_sha256': sha(TOOL), 'test_sha256': sha(__file__),
               'v001_sha256': sha(V001[0])}
    with open(RUN / 'RESULTS.json', 'x') as fh:
        json.dump({'summary': summary, 'results': RESULTS}, fh, indent=1, default=str)
    print(json.dumps(summary, indent=1))
    return 0 if summary['fail'] == 0 and not AUDIT['denied'] else 1


if __name__ == '__main__':
    sys.exit(main())
