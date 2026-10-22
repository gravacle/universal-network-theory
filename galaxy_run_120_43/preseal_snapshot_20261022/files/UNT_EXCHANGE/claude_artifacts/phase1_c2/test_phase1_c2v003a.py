"""Tests for phase1_c2v003a (A149 items 1-4 successor of phase1_c2v003: the member_eps OverflowError catch, the AT-0b
members_sha256 custody, the print-only band_region_box_only_extent, and tests that kill v003's 5 surviving mutants).
SYNTHETIC ONLY.

Every check of test_phase1_c2v003.py (331d0212; 142 checks) is ported, in v003's order, with v003's ids except the 9
part-2 ids, which now name v003 as the reference.  Port changes (each also noted at its site):
  - the module under test is phase1_c2v003a (T00, T33's custody text, T35's declared AST nodes);
  - T23: at1 with the AT-0b defect file now passes that AT-0b's own members file (MEMBERS_NOREBIND); the v003 form
    (another members file) is now REFUSED by A149 item 2 and is tested as such in T37;
  - T30 (c): v002's corner at1 is run directly (AT1_CORNER_V002) instead of being read from v002's shadow directory;
  - T36 keeps v002 as its reference (S0, the shared-map handoff and L1 byte-identical to v002 except module).
Part 1 (T00-T29): the ported v002-era tests.  Every CLI call is shadow-run with v003 (149ed4cb, untouched) on the same
inputs into the same out-dir path (v003's directory is moved aside to <out>.V003_SHADOW before v003a runs).  One input
is substituted for v003, and only for at1: v003's custody (A144) reads only a v003-written L1, so v003's at1 reads the L1
that v003's own band shadow wrote (<L1 dir>.V003_SHADOW/L1_C2V001.json), whose bytes the band comparison shows equal to
v003a's except module.
Part 2 (R01): regression against v003.  Exit codes, stdout and every output file must be byte-identical after
substituting v003's value for exactly these fields: module, tool_sha256 (tool identity); the engine record's
created_utc and the shas that hash it; at0b's new members_sha256 (A149 item 2; it must equal the --members sha); at1's
new reported.band_region_box_only_extent (A149 item 3).  Every at1 failing list is identical, field by field.
Part 3 (T30-T36): v003's A144 R1 (T30), R2 (T31), R3 (T32), custody (T33), A135 item 10 (T34), scope (T35), S0 /
shared-map identity (T36).
Part 4 (T37-T43, A149): T37 members_sha256 custody (item 2); T38 the region tolerance is exactly E._LP_EPS with a
strict '>' (kills tol 1e-9, tol 1e-13 and '>='); T39 the eps contract covers member_valid false points (kills the
member_valid-true-only contract); T40 the certificate-map scope check matches theta keys too (kills spec-sha-only);
T41 band_region_box_only_extent (item 3, with the exact-corner LP-tie case); T42 the 10**400 entry (item 1, shadowed
against v003: the declared overflow difference); T43 v003 untouched, the v003a custody and the AST scope against v003.

Synthetic campaigns are built by the REAL orchestrator c2v005 (Context, Probe, make_plan, _commit_plan, run_wave,
ingest, finalise) with its in-process test executor, a toy forward and a synthetic 12-row region, on the real coordinate
spec V002 (engine c2v003b), the real addendum V005A (A13: 3 free coordinates) and the real taxonomy V003.  The tool runs
through its CLI as root would run it (a subprocess of the campaign interpreter), except where a test injects a fault in
process or places members by hand (then the tool's own at1_rows runs in process on the real engine).  No project
forward, no NGC3198 data or targets: NGC values are a toy function of u.  Writes only under
<this dir>/test_runs_v003a/RUN_<UTC>_<pid>/ (an audit hook refuses any other write, and any open of a path with an
'ngc3198' or 'uvt_' component).

usage: <codex python3> -I -B test_phase1_c2v003a.py
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
TOOL = HERE / 'phase1_c2v003a.py'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
PH1 = Path(ART + 'phase1_c2')
V001 = (PH1 / 'phase1_c2v001.py', '34eaef36586aec77b3436d6bcd96d0a2948aef699d612077e2d6f9f32e4cd99c')
V001_TESTS = (PH1 / 'test_phase1_c2v001.py', '156f0bef3a9962774257f3737eaa61c7d7df26a2d3fdb7ebb5de81847ee83fac')
V002 = (PH1 / 'phase1_c2v002.py', 'd64351ecc06c61e99e2d7253c5d4311617fc1f64d34d37523102ed32720a6754')
V002_TESTS = (PH1 / 'test_phase1_c2v002.py', 'b1aedebc4573cdd64b882400305c57203a4f3ad1e82aad242b04eafac0a32372')
V003 = (PH1 / 'phase1_c2v003.py', '149ed4cbe1ad96e941ce01ad4cff46369dd559a9eee4356e155ad069f4a7b406')
V003_FILES = ((PH1 / 'test_phase1_c2v003.py', '331d02128c64cbc69f49bc2d995a0a1babb4a565c45584679cea7dc55d5f4770'),
              (PH1 / 'mutation_phase1_c2v003.py', '54d51eb363e8f4bdee720720856785254064daa55b59010fce2e0007792723ad'),
              (PH1 / 'README_PHASE1_C2V003.md', '52432afec3df76b6680f600ebc41c6147e2a473871d5d5296adb1d908e76a9a3'),
              (PH1 / 'HASHES_V003.txt', '518b6601db383091d9ef5c4a18111bd27c9510cba93216a4554a8aac991712ea'))
EPS_MEMBER = 0.01   # A144 R3: every Phase-2 members file carries eps_km_s (port change; the Phase-1 values use 0.01)
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
RUN = HERE / 'test_runs_v003a' / ('RUN_%s_%d' % (STAMP, os.getpid()))
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


def m2_speeds(a, const=False):
    """SYNTHETIC toy for the m_id = 2 corner (Claude3 0204 verifier C_M2): depends on s1 = a0 + a1 + sqrt2 a2 (every row)
    and s2 = a0 + a1 - sqrt2 a2 (alternating sign), so V_I = (1, 1, +-sqrt2)/2 and the near-null direction ~(1, -1, 0)."""
    s1, s2 = a[0] + a[1] + math.sqrt(2.0) * a[2], a[0] + a[1] - math.sqrt(2.0) * a[2]
    return {r: 40.0 + 8.0 * math.sqrt(rad) + 3.0 * s1 + (2.0 if i % 2 == 0 else -2.0) * s2
            for i, (r, rad) in enumerate(zip(ROWS, RADII))}


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
SHADOW = {'on': True, 'log': [], 'ref': V003[0], 'suffix': '.V003_SHADOW'}
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


def v003_l1_of(args):
    """For v003's at1 shadow: the L1 v003's own band shadow wrote next to the v003a L1 (<L1 dir>.V003_SHADOW), or None."""
    if args[:2] != ['agree', 'at1'] or '--l1' not in args:
        return None
    p = Path(args[args.index('--l1') + 1])
    alt = Path(str(p.parent) + '.V003_SHADOW') / p.name
    return alt if alt.is_file() else None


def tool(*args):
    """v003a through its CLI.  While SHADOW is on (part 1), the reference (v003; v002 for T36) runs first on the same
    arguments; its out dir is moved aside to <out><suffix>, v003a then writes the same path, and the two results are
    compared (R01).  For agree at1 under v003 only, --l1 and --l1-sha256 name the L1 that v003's own band shadow wrote
    (v003's A144 custody reads no other L1); the substitution is recorded in the comparison."""
    args = [str(x) for x in args]
    if not SHADOW['on']:
        return cli(TOOL, args)
    od = args[args.index('--out-dir') + 1] if '--out-dir' in args else None
    pre = od is not None and os.path.lexists(od)
    rargs, l1sub = list(args), None
    if SHADOW['ref'] == V003[0]:
        alt = v003_l1_of(args)
        if alt is not None:
            rargs[rargs.index('--l1') + 1] = str(alt)
            rargs[rargs.index('--l1-sha256') + 1] = sha(alt)
            l1sub = str(alt)
    rc1, o1 = cli(SHADOW['ref'], rargs)
    d1 = None
    if od is not None and not pre and os.path.lexists(od):
        d1 = od + SHADOW['suffix']
        os.rename(od, d1)
    rc2, o2 = cli(TOOL, args)
    d2 = od if (od is not None and not pre and os.path.lexists(od)) else None
    rec = shadow_compare(args, rc1, o1, d1, rc2, o2, d2, SHADOW['ref'])
    rec.update(ref=os.path.basename(str(SHADOW['ref'])), l1_substituted=l1sub)
    SHADOW['log'].append(rec)
    return rc2, o2


def shadowed(fn, ref=None, suffix=None):
    """Shadowed CLI calls outside part 1 (T36 against v002, T42 against v003): returns (fn's result, the comparison
    records of its calls); the records are not added to the part-1 log."""
    keep, n0 = dict(SHADOW), len(SHADOW['log'])
    SHADOW['on'] = True
    if ref is not None:
        SHADOW['ref'], SHADOW['suffix'] = ref, suffix
    try:
        res = fn()
    finally:
        SHADOW.update(on=keep['on'], ref=keep['ref'], suffix=keep['suffix'])
    new = SHADOW['log'][n0:]
    del SHADOW['log'][n0:]
    return res, new


AT0B_DECLARED = 'A149 item 2: at0b members_sha256 (v003a only)'
AT1_DECLARED = 'A149 item 3: reported.band_region_box_only_extent (v003a only)'


def same_bytes(name, raw1, raw2, ref=None):
    """(identical after the declared substitutions?, substituted fields, the at0b / at1 detail or None).  raw1 is the
    reference's file (v003, or v002 for T36), raw2 v003a's.  The A149 fields are declared against v003 only."""
    if raw1 == raw2:
        return True, [], None
    if name.endswith('.jsonl'):
        a_, b_ = raw1.split(b'\n'), raw2.split(b'\n')
        if len(a_) != len(b_):
            return False, [], None
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
        return b'\n'.join(rebuilt) == raw1, list(REGISTRY_VOLATILE), None
    j1, j2 = json.loads(raw1), json.loads(raw2)
    if name.startswith('PHASE1_CALIBRATION_RECORD_'):
        for k in ('created_utc', 'record_sha256'):
            j2[k] = j1.get(k)
        return E._canonical_bytes(j2) == raw1, ['created_utc', 'record_sha256'], None
    subst = [k for k in ('module', 'tool_sha256') if k in j1 and k in j2]
    for k in subst:
        j2[k] = j1[k]
    if name == 'SNAPSHOT_C2V001.json' and isinstance(j1.get('record'), dict) and isinstance(j2.get('record'), dict):
        for k in SNAP_RECORD_VOLATILE:
            j2['record'][k] = j1['record'].get(k)
        subst += ['record.' + k for k in SNAP_RECORD_VOLATILE]
    det = None
    if ref == V003[0] and name == 'AT0B_C2V001.json' and 'members_sha256' in j2 and 'members_sha256' not in j1:
        det = {'members_sha256': j2.pop('members_sha256')}
        subst.append(AT0B_DECLARED)
    if ref == V003[0] and name == 'AT1_C2V001.json':
        rep1, rep2 = j1.get('reported') or {}, j2.get('reported') or {}
        det = {'outcome': [j1.get('outcome'), j2.get('outcome')],
               'n_failing': [len(j1.get('failing') or []), len(j2.get('failing') or [])],
               'failing_identical': json.dumps(j1.get('failing'), sort_keys=True) == json.dumps(j2.get('failing'),
                                                                                                 sort_keys=True),
               'box_only_extent_v003a': rep2.get('band_region_box_only_extent'),
               'box_only_extent_in_v003': 'band_region_box_only_extent' in rep1}
        if 'band_region_box_only_extent' in rep2 and 'band_region_box_only_extent' not in rep1:
            rep2.pop('band_region_box_only_extent')
            subst.append(AT1_DECLARED)
    return P.jbytes(j2) == raw1, subst, det


def shadow_compare(args, rc1, o1, d1, rc2, o2, d2, ref=None):
    cmd = args[0] + (' ' + args[1] if args[0] == 'agree' and len(args) > 1 else '')
    r = {'cmd': cmd, 'out': d2 or d1, 'rc': [rc1, rc2], 'diffs': [], 'subst': [], 'at1': None, 'at0b': None}
    if rc1 != rc2:
        r['diffs'].append('exit code %s != %s' % (rc1, rc2))
    s1, s2 = dict(o1), dict(o2)
    for s in (s1, s2):
        if isinstance(s.get('files'), dict):
            s['files'] = sorted(s['files'])
    if s1 != s2:
        r['diffs'].append('stdout %s != %s' % (json.dumps(s1)[:300], json.dumps(s2)[:300]))
    n1 = sorted(os.listdir(d1)) if d1 else []
    n2 = sorted(os.listdir(d2)) if d2 else []
    if n1 != n2:
        r['diffs'].append('files %s != %s' % (n1, n2))
    for name in sorted(set(n1) & set(n2)):
        ok, subst, det = same_bytes(name, (Path(d1) / name).read_bytes(), (Path(d2) / name).read_bytes(), ref)
        r['subst'] = sorted(set(r['subst']) | set(subst))
        if det is not None and name == 'AT1_C2V001.json':
            r['at1'] = det
            if not det['failing_identical']:
                r['diffs'].append('%s: the failing lists differ' % name)
        if det is not None and name == 'AT0B_C2V001.json':
            want = sha(args[args.index('--members') + 1]) if '--members' in args else None
            r['at0b'] = dict(det, members_arg_sha256=want, equal=det['members_sha256'] == want)
            if det['members_sha256'] != want:
                r['diffs'].append('%s: members_sha256 is not the sha of the --members file' % name)
        if not ok:
            r['diffs'].append('%s differs beyond the declared fields' % name)
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
          P.MODULE == 'phase1_c2v003a' and P.PREFIX_FAMILIES == ('seed', 'jacobian', 'repair', 'gd_pre'),   # port: v003a
          {'v001': sha(V001[0])[:16], 'v001_tests': sha(V001_TESTS[0])[:16]})
    check('T00.v002_tool_and_tests_untouched_and_engine_LP_EPS_is_1e-12',
          sha(V002[0]) == V002[1] and sha(V002_TESTS[0]) == V002_TESTS[1] and E._LP_EPS == 1e-12,
          {'v002': sha(V002[0])[:16], 'v002_tests': sha(V002_TESTS[0])[:16], 'engine_LP_EPS': E._LP_EPS})


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
                        'speeds_km_s': ngc_toy(m['u'], kind), 'eps_km_s': [EPS_MEMBER] * 43})
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
    S['seed_phase2'] = {'rec2': rec2, 'run2': run2, 'sel2': sel2}

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
                        'member_valid': True, 'result_pin': rp_, 'valid': [True] * 43, 'speeds_km_s': ngc_toy(m['u'], kind),
                        'eps_km_s': [EPS_MEMBER] * 43})
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
    cats_ok = True
    for f in doc.get('failing') or []:   # port: the category oracle is A144 R1 (independent re-implementation)
        u = [p for p in run2['exploration']['admitted_points'] if p['log_index'] == f['log_index']][0]['u']
        cvec = L['VI'] @ (np.array(u) - L['uA'])
        viol, _mx = indep_region(L, cvec)
        want = CAT[viol[0]] if viol else 'NGC_NONLINEAR'
        cats_ok &= f['category'] == want and f['excess'] > 0 and f['region_rows_violated'] == viol
    rep = doc.get('reported') or {}
    check('T22.agree_at1_SUPERSEDED_with_categories_and_reported_lines (nonlinear NGC toy)',
          rcb == 0 and rc1 == 0 and doc.get('outcome') == 'SUPERSEDED' and cats_ok and
          'max_ddo_linearity_deviation_over_tau' in rep and rep.get('ngc_linearity_residuals'),
          {'outcome': doc.get('outcome'), 'n_failing': len(doc.get('failing') or []),
           'categories': sorted(set(f['category'] for f in doc.get('failing') or []))})
    a0b_bad = S['at0b_defect']
    m_bad = FIX / 'MEMBERS_NOREBIND.json'   # port (A149 item 2): the defect AT-0b's own members file, not MEMBERS_C1
    rc1, o1 = tool('agree', 'at1', '--snapshot', out, '--snapshot-sha256', snap_sha(out), '--l1', _l1, '--l1-sha256',
                   sha(_l1), '--fdplan', S['seed_fd'], '--fdplan-sha256', sha(S['seed_fd']), '--at0a', S['seed_at0a'],
                   '--at0a-sha256', sha(S['seed_at0a']), '--at0b', a0b_bad, '--at0b-sha256', sha(a0b_bad),
                   '--phase2-record', rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'],
                   '--phase2-registry', rec2['registry_path'], '--members', m_bad, '--members-sha256',
                   sha(m_bad), '--config', c.cfg, '--config-sha256', c.cfg_sha, '--interior-count', 6,
                   '--out-dir', RUN / 'AT1_DEFECT')
    check('T23.MUST_FAIL_at1_with_AT0_defect_reads_AGREEMENT_DEFECT', rc1 == 10 and o1.get('outcome') == 'AGREEMENT_DEFECT',
          {'rc': rc1, 'outcome': o1.get('outcome'), 'reason': o1.get('reason'),
           'port_note': 'members = the defect AT-0b own file (A149 item 2); the v003 form is REFUSED, see T37'})


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
        mv[li] = {'valid': [True] * 43, 'speeds_km_s': [x + bump * (j + 1) for j, x in enumerate(g)],
                  'eps_km_s': [EPS_MEMBER] * 43}   # port: A144 R3 member eps
    fails, rep = P.at1_rows(E, L, l1, {'exploration': {'admitted_points': pts}}, mv, QIDS)
    got, lists_ok = {}, True
    for f in fails:
        got.setdefault(f['log_index'], set()).add(f['category'])
        u = [p['u'] for p in pts if p['log_index'] == f['log_index']][0]
        lists_ok &= f['region_rows_violated'] == indep_region(L, L['VI'] @ (np.array(u) - L['uA']))[0]
    want_lin = abs(L['qA'] + L['S'] @ (L['VI'].T @ (L['VI'] @ (0.5 * r * v0)))).max() > L['zrow'].min()
    ok = (got.get(102) == {'OUTSIDE_TRUST_RADIUS'} and got.get(103) == {'NGC_NONLINEAR'} and 104 not in got and
          got.get(101) == {'OUTSIDE_LINEAR_DDO_REGION'} and want_lin and lists_ok)
    check('T25.AT1_categories_trust_radius_linear_DDO_region_NGC_nonlinear', ok,
          {'categories': {k: sorted(v) for k, v in got.items()}, 'region_lists_match_independent_rule': lists_ok})
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
TOOL_IDENTITY = {'module', 'tool_sha256', 'created_utc', 'record_sha256', 'record_file_sha256', 'line_sha256',
                 'record.record_file_sha256', 'record.record_sha256', 'record.registry_line_sha256'}
CMDS = ('snapshot', 'fdplan', 'handoff', 'band', 'agree at0a', 'agree at0b', 'agree at1')
DECLARED = {'agree at0b': AT0B_DECLARED, 'agree at1': AT1_DECLARED}   # A149 items 2 and 3; nothing else may differ


def r01_regression(S):
    """Every part-1 CLI call ran under v003 and v003a on identical inputs (at1: v003 reads its own band shadow's L1)
    into the same out-dir path.  Port of v003's R01 (which targeted v002): the reference is now v003."""
    groups = {}
    for r in SHADOW['log']:
        groups.setdefault(r['cmd'], []).append(r)
    for cmd in CMDS:
        rs = groups.get(cmd, [])
        bad = [r for r in rs if r['diffs']]
        allowed = TOOL_IDENTITY | ({DECLARED[cmd]} if cmd in DECLARED else set())
        ident = [r for r in rs if not r['diffs'] and set(r['subst']) <= TOOL_IDENTITY]
        det = {'calls': len(rs), 'identical_up_to_tool_identity': len(ident),
               'exit_codes': sorted(set(r['rc'][1] for r in rs)), 'reference': sorted(set(r['ref'] for r in rs)),
               'substituted_fields': sorted(set(f for r in rs for f in r['subst'])),
               'bad': [(r['out'], r['diffs'][:2]) for r in bad][:4]}
        ok = bool(rs) and not bad and all(set(r['subst']) <= allowed and r['ref'] == V003[0].name for r in rs)
        if cmd == 'agree at0b':   # A149 item 2: members_sha256 on every at0b file, equal to the --members sha
            wrote = [r for r in rs if r['out'] and os.path.isfile(os.path.join(r['out'], 'AT0B_C2V001.json'))]
            ok = ok and bool(wrote) and all(r['at0b'] and r['at0b']['equal'] and DECLARED[cmd] in r['subst']
                                            for r in wrote)
            det['at0b_members_sha256'] = [(os.path.basename(r['out'] or ''), (r['at0b'] or {}).get('equal'))
                                          for r in rs]
        elif cmd == 'agree at1':   # A149 item 3: the new print key only; v003 read its own band shadow's L1
            wrote = [r for r in rs if r['out'] and os.path.isfile(os.path.join(r['out'], 'AT1_C2V001.json'))]
            ok = ok and bool(wrote) and all(r['l1_substituted'] for r in rs) and \
                all(r['at1'] and r['at1']['failing_identical'] and DECLARED[cmd] in r['subst'] for r in wrote)
            det['at1'] = [(os.path.basename(r['out'] or ''), r['rc'], (r['at1'] or {}).get('outcome'),
                           (r['at1'] or {}).get('n_failing'), os.path.basename(os.path.dirname(r['l1_substituted'] or '')))
                          for r in rs]
        else:
            ok = ok and len(ident) == len(rs)
        check('R01.regression_v003_shadow_%s_byte_identical_except_declared_fields' % cmd.replace(' ', '_'), ok, det)
    other = sorted(set(groups) - set(CMDS))
    l5_fx = [r for r in SHADOW['log'] if r['cmd'] == 'snapshot' and
             any(t in (r['out'] or '') for t in ('/SNAP_NOID', '/SNAP_CORNER'))]
    check('R01.no_other_command_and_the_L5_fixtures_(NOID_and_corner)_are_identical_up_to_tool_identity',
          not other and len(l5_fx) >= 3 and all(not r['diffs'] and set(r['subst']) <= TOOL_IDENTITY for r in l5_fx),
          {'other_commands': other, 'l5_snapshot_calls': [(os.path.basename(r['out'] or ''), r['rc'], r['subst'])
                                                          for r in l5_fx]})
    at1 = [r for r in groups.get('agree at1', []) if r['at1']]
    check('R01.at1_failing_lists_identical_to_v003_field_by_field_(norm_n_category_excess_e_q_all_equal)',
          bool(at1) and all(r['at1']['failing_identical'] and r['at1']['outcome'][0] == r['at1']['outcome'][1] and
                            r['at1']['box_only_extent_in_v003'] is False and
                            isinstance(r['at1']['box_only_extent_v003a'], list) for r in at1),
          [(os.path.basename(r['out']), r['at1']['outcome'], r['at1']['n_failing'], r['at1']['failing_identical'])
           for r in at1])


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
                    'member_valid': True, 'result_pin': rp_, 'valid': [True] * 43, 'speeds_km_s': ngc_toy(m['u'], 'linear'),
                    'eps_km_s': [EPS_MEMBER] * 43})
    mp = FIX / 'MEMBERS_CORNER.json'
    mp.write_text(json.dumps({'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, indent=1))
    S['corner_phase2'] = {'rec2': rec2, 'run2': run2, 'sel2': sel2, 'vals': vals, 'l1': l1d / 'L1_C2V001.json',
                          'members': mp, 'at1': RUN / 'AT1_CORNER'}
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


# ----------------------------------------------------------------------------------------------- N-B (A137), ported to R3
def r3_eq(eps_m, eps_q, D, du):
    """Independent A144 R3 formula (E_A133_2(b)), plain Python floats."""
    s = sum(float(D[k]) / float(du[k]) for k in range(len(du)))
    return eps_m + eps_q * (abs(1.0 - s) + sum(abs(float(D[k])) / abs(float(du[k])) for k in range(len(du))))


def t29_nb(S):
    """v002's T29 (the A137 N-B checks; 0191 verifier P8), ported: the same fixtures re-run with eps_m present and read
    with A144 R3 (E_A133_2(b) supersedes the E_A133_1 formula)."""
    import numpy as np
    P2 = load(V002[0], 'phase1_v002_reference')   # v002's at1_rows (the superseded A137 reading), for comparison only
    _d, rec = rec_of(S['seed_snap'])
    L = P.linear_model(E, rec['run'])
    fd = json.loads(Path(S['seed_fd']).read_text())
    du = np.array([f['du'] for f in fd['F']])
    h = np.abs(du)
    VN = L['V'][L['N']] if L['N'] else np.zeros((0, 3))
    v0 = L['V'][L['I'][0]]
    r = 0.25 / math.sqrt(len(L['I']))
    # Claude3 0191 verifier P8: eps exaggerated to 1 km/s so the noise term is visible; row q = 0; eps_m = 1 km/s
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
        e_v002 = float(np.sum(2 * b['eps_q'] * np.abs(D) / h))
        e_v003 = r3_eq(1.0, b['eps_q'], D, du)
        hi_v002, hi_v003 = b['hi'] + b['a_q'] + e_v002 + shift, b['hi'] + b['a_q'] + e_v003 + shift
        g = 0.5 * (hi_v002 + hi_v003)   # between the two upper limits
        pts = [{'log_index': 7, 'u': u, 'prediction': {'speeds_km_s': {rr: float(x) for rr, x in zip(L['rows'], L['fA'])}}}]
        mv = {7: {'valid': [True] * 43, 'speeds_km_s': [g if j == q else rows[j].get('g_A', 150.0) for j in range(43)],
                  'eps_km_s': [1.0] * 43}}
        run2 = {'exploration': {'admitted_points': pts}}
        f2, _r2 = P2.at1_rows(E, L, l1, run2, mv, vd['query_ids'])
        f3, r3 = P.at1_rows(E, L, l1, run2, mv, vd['query_ids'])
        eq = [x['e_q'] for x in r3['e_q_per_member_row'] if x['log_index'] == 7 and x['id'] == qid]
        res[name] = {'e_v002_A137': e_v002, 'e_v003_E_A133_2b': e_v003, 'g': g, 'hi_v002': hi_v002, 'hi_v003': hi_v003,
                     'v002_fails_row': any(x['id'] == qid for x in f2), 'v003_fails_row': any(x['id'] == qid for x in f3),
                     'v003_reported_e_q': eq}
    ok = all(x['v002_fails_row'] == (x['g'] > x['hi_v002']) and x['v003_fails_row'] == (x['g'] > x['hi_v003']) and
             x['v002_fails_row'] != x['v003_fails_row'] and len(x['v003_reported_e_q']) == 1 and
             abs(x['v003_reported_e_q'][0] - x['e_v003_E_A133_2b']) <= 1e-12 * max(1.0, x['e_v003_E_A133_2b'])
             for x in res.values())
    res['port_note'] = 'v002 id kept; ported to A144 R3: v003 pass/fail follows the E_A133_2(b) bound, v002 the A137 one'
    check('T29.N-B_exaggerated_eps_both_flip_directions_follow_the_member_displacement_reading (0191 verifier P8)',
          ok, res)
    # FD_NOISE_NOT_BOUNDED where eps is unavailable (T16's values: eps None on row 7); the member eps is valid
    vd2 = json.loads(Path(S['vals1']).read_text())
    rows2, _m2 = P.band_rows(E, L, vd2, fd['F'])
    q7 = vd2['query_ids'][7]
    u = list(L['uA'] + 1e-4 * v0)
    mv = {8: {'valid': [True] * 43, 'speeds_km_s': [(rows2[7]['hi'] + 1000.0) if j == 7 else rows2[j].get('g_A', 150.0)
                                                    for j in range(43)], 'eps_km_s': [EPS_MEMBER] * 43}}
    pts = [{'log_index': 8, 'u': u, 'prediction': {'speeds_km_s': {rr: float(x) for rr, x in zip(L['rows'], L['fA'])}}}]
    f2, r2 = P.at1_rows(E, L, {'rows': rows2, 'fd_du': [f['du'] for f in fd['F']]},
                        {'exploration': {'admitted_points': pts}}, mv, vd2['query_ids'])
    e7 = [x['e_q'] for x in r2['e_q_per_member_row'] if x['id'] == q7]
    fl = [x for x in f2 if x['id'] == q7]
    others = [x['e_q'] for x in r2['e_q_per_member_row'] if x['id'] != q7]
    check('T29.N-B_FD_NOISE_NOT_BOUNDED_where_eps_is_unavailable (per member and row; the failing entry is flagged)',
          rows2[7].get('fd_noise') == 'FD_NOISE_NOT_BOUNDED' and e7 == ['FD_NOISE_NOT_BOUNDED'] and len(fl) == 1 and
          fl[0]['flag'] == 'FD_NOISE_NOT_BOUNDED' and fl[0]['flag_reason'] == 'NO_ROW_EPS_Q' and
          q7 in r2['rows_fd_noise_not_bounded'] and len(others) > 0 and all(isinstance(x, float) for x in others) and
          r2['pairs_member_point_noise_not_bounded'] == [], {'e_q_row7': e7, 'failing_row7': fl})
    # the CLI at1 of record (T22, nonlinear toy): e_q per (member, row) equals the independent E_A133_2(b) formula
    doc, l1p, mp, run2 = S['at1_q1']
    l1d = json.loads(Path(l1p).read_text())
    rows1 = {x['id']: x for x in l1d['rows']}
    epsm = {p['log_index']: p['eps_km_s'] for p in json.loads(Path(mp).read_text())['points']}
    uA = np.array(fd['u_A']['u'])
    upos = {p['log_index']: np.array(p['u']) for p in run2['exploration']['admitted_points']}
    eqs = (doc.get('reported') or {}).get('e_q_per_member_row') or []
    bad = []
    for x in eqs:
        rr = rows1[x['id']]
        if isinstance(rr.get('fd_noise'), dict):
            want = r3_eq(epsm[x['log_index']][QIDS.index(x['id'])], rr['eps_q'], upos[x['log_index']] - uA, du)
            if not isinstance(x['e_q'], float) or abs(x['e_q'] - want) > 1e-12 * max(1.0, want) or x['flag'] is not None:
                bad.append((x['log_index'], x['id'], x['e_q'], want))
        elif x['e_q'] != 'FD_NOISE_NOT_BOUNDED':
            bad.append((x['log_index'], x['id'], x['e_q'], 'FD_NOISE_NOT_BOUNDED'))
    pairs = sorted((x['log_index'], x['id']) for x in eqs)
    resid = sorted((x['log_index'], x['id']) for x in (doc.get('reported') or {}).get('ngc_linearity_residuals') or [])
    check('T29.at1_CLI_reports_e_q_per_member_and_row_equal_to_an_independent_member_displacement_sum (T22 Q1)',
          doc.get('e_q_reading') == P.E_Q_READING and pairs == resid and len(eqs) > 0 and not bad,
          {'n_pairs': len(eqs), 'bad': bad[:4], 'outcome': doc.get('outcome'),
           'port_note': 'v002 id kept; the independent sum is now the E_A133_2(b) formula with the members file eps_m'})


# ----------------------------------------------------------------------------------------------- A144 helpers (part 3)
CAT = {'TRUST_RADIUS': 'OUTSIDE_TRUST_RADIUS', 'BOX': 'OUTSIDE_BOX_SLICE', 'LINEAR_DDO': 'OUTSIDE_LINEAR_DDO_REGION'}
LP_EPS = 1e-12   # T00 asserts that the pinned engine's _LP_EPS is exactly this


def indep_region(L, c, tol=LP_EPS, clip=True):
    """Independent re-implementation of the A144 R1 rule from A133 1.5 (not the tool's band_region): the families
    violated by c, in the order TRUST_RADIUS, BOX, LINEAR_DDO, and the max violation per family.  clip=False and
    tol=0.0 give the rejected exact, unclipped comparison (for contrast only)."""
    import numpy as np
    VI = np.asarray(L['VI'], dtype=float)
    c = np.asarray(c, dtype=float)
    r = 0.25 / math.sqrt(VI.shape[0])
    x = VI.T @ c
    s = np.asarray(L['S']) @ x
    cl = (lambda v: np.maximum(v, 0.0)) if clip else (lambda v: v)
    fam = {'LINEAR_DDO': np.concatenate([s - cl(L['zrow'] - L['qA']), -s - cl(L['zrow'] + L['qA'])]),
           'BOX': np.concatenate([x - cl(1.0 - L['uA']), -x - cl(L['uA'])]),
           'TRUST_RADIUS': np.concatenate([c - r, -c - r])}
    viol = [f for f in ('TRUST_RADIUS', 'BOX', 'LINEAR_DDO') if bool(np.any(fam[f] > tol))]
    return viol, {f: float(np.max(v)) for f, v in fam.items()}


def synth_L(uA, Vtrue, s_vals, n_ddo=6, ddo_half=5.0, seed=0, qA=None):
    """SYNTHETIC linear model in linear_model's layout (sigma 1, rectangles f_A +- ddo_half, S = U diag(s) Vtrue,
    V = the SVD right vectors of S)."""
    import numpy as np
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.standard_normal((n_ddo, 3)))
    Vt = np.array(Vtrue, dtype=float)
    S = U @ np.diag(s_vals) @ Vt
    _u, _s, vt = np.linalg.svd(S)
    V = vt.copy()
    for k in range(3):
        if V[k] @ Vt[k] < 0:
            V[k] = -V[k]
    I = [k for k in range(3) if s_vals[k] > 0]
    N = [k for k in range(3) if s_vals[k] == 0]
    return {'uA': np.array(uA, dtype=float), 'qA': np.zeros(n_ddo) if qA is None else np.array(qA, dtype=float),
            'zrow': np.full(n_ddo, float(ddo_half)), 'S': S, 'V': V, 'I': I, 'N': N, 'VI': V[I],
            'fA': 100.0 + np.arange(n_ddo, dtype=float), 'sig': np.ones(n_ddo), 'J': S.copy(),
            'P': {'max_repair_step': 0.25, 'hull_growth_tol': 0.02, 'march_step': 0.05},
            'rows': ['SYN_D%02d' % i for i in range(n_ddo)]}


def synth_F(L, du):
    import numpy as np
    return [{'role': 'F%d' % k, 'axis': k, 'du': float(du[k]),
             'u': [float(x) for x in L['uA'] + float(du[k]) * np.eye(3)[k]]} for k in range(3)]


def rand_orth(seed):
    import numpy as np
    q, _r = np.linalg.qr(np.random.default_rng(seed).standard_normal((3, 3)))
    return q.T


def lin_g(u):
    return ngc_toy(u, 'linear')


def facecurv_g(u):
    """SYNTHETIC NGC toy, curved along the corner face directions (1, -1, 0) and (0, 0, 1) at u_A = (1, 0, 0.5)."""
    return [150.0 + (j + 1) * (3.0 * u[0] - 2.0 * u[1] + 0.5 * u[2]) +
            40.0 * (j + 1) * (((u[0] - u[1] - 1.0) / 2.0) ** 2 + (u[2] - 0.5) ** 2) for j in range(43)]


def bumped(gfn, bump=50.0):
    return lambda u: [x + bump * (j + 1) for j, x in enumerate(gfn(u))]


def ddo_pred(L, u):
    import numpy as np
    f = L['fA'] + L['J'] @ (np.asarray(u, dtype=float) - L['uA'])
    return {'speeds_km_s': {rr: float(x) for rr, x in zip(L['rows'], f)}}


def run2_of(L, members):
    return {'exploration': {'admitted_points': [{'log_index': li, 'u': [float(x) for x in u], 'prediction': ddo_pred(L, u)}
                                                for li, u in members]}}


def mv_of(members, gfn, eps=EPS_MEMBER, noise=None):
    out = {}
    for li, u in members:
        g = [float(x) + (noise or {}).get((li, j), 0.0) for j, x in enumerate(gfn(u))]
        out[li] = {'valid': [True] * 43, 'speeds_km_s': g, 'eps_km_s': [eps] * 43}
    return out


def l1_of(L, Fs, gfn, eps=0.01, noise=None, lp=None):
    """In-process L1 rows from the tool's band_rows (AST-identical to v002) on a SYNTHETIC values doc."""
    pts = []
    for role, u in [('u_A', L['uA'])] + [(f['role'], f['u']) for f in Fs]:
        g = [float(x) + (noise or {}).get((role, j), 0.0) for j, x in enumerate(gfn(u))]
        pts.append({'role': role, 'valid': [True] * 43, 'speeds_km_s': g, 'eps_km_s': [eps] * 43})
    rows, meta = P.band_rows(E, L, {'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, Fs, lp)
    return {'rows': rows, 'fd_du': [f['du'] for f in Fs]}, meta


def proj(fails):
    """The R1 regression projection: failing set (order), excess and norm_n, as JSON bytes."""
    return json.dumps([[x['log_index'], x['id'], x['excess'], x['norm_n']] for x in fails])


def fixture_L(snap_dir):
    _d, rec = rec_of(snap_dir)
    return P.linear_model(E, rec['run'])


def F_of(fd_path):
    return json.loads(Path(fd_path).read_text())['F']


def null_members(L, start, steps=(-0.3, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3), ts=(-0.3, -0.1, 0.0, 0.1, 0.3)):
    """Members displaced only along the near-null directions V_N (c = 0 in exact arithmetic), inside the box."""
    import numpy as np
    VN = L['V'][L['N']]
    out, li = [], start
    for s in steps:
        for t in (ts if len(VN) > 1 else (0.0,)):
            u = L['uA'] + s * VN[0] + (t * VN[1] if len(VN) > 1 else 0.0)
            if np.all(u >= 0.0) and np.all(u <= 1.0):
                out.append((li, [float(x) for x in u]))
                li += 1
    return out


def members_doc(sel2, uA_li, uA_pin, gfn, tag, eps_fn=None, drop_eps=False, eps_len=43, eps_raw=None):
    pts = []
    for m in sel2['points']:
        if m['log_index'] == uA_li:
            rp_ = uA_pin
        else:
            rf = FIX / ('%s_M%04d.json' % (tag, m['log_index']))
            rf.write_text(json.dumps({'synthetic_toy_result': True, 'log_index': m['log_index']}))
            rp_ = pin(rf)
        p = {'role': 'member', 'log_index': m['log_index'], 'theta_key': O.theta_key(m['theta_natural']),
             'member_valid': True, 'result_pin': rp_, 'valid': [True] * 43, 'speeds_km_s': gfn(m['u'])}
        if eps_raw is not None:
            p['eps_km_s'] = eps_raw
        elif not drop_eps:
            p['eps_km_s'] = [eps_fn(m['log_index'], q) if eps_fn else EPS_MEMBER for q in range(eps_len)]
        pts.append(p)
    mp = FIX / ('MEMBERS_%s.json' % tag)
    mp.write_text(json.dumps({'schema': P.S_VALUES, 'query_ids': QIDS, 'points': pts}, indent=1))   # NaN allowed here
    return mp


def at0b_cli(fx, vals, mp, tag):
    rec2 = fx['rec2']
    rc, o = tool('agree', 'at0b', '--snapshot', fx['snap'], '--snapshot-sha256', snap_sha(fx['snap']), '--phase2-record',
                 rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
                 rec2['registry_path'], '--values', vals, '--values-sha256', sha(vals), '--members', mp,
                 '--members-sha256', sha(mp), '--out-dir', RUN / ('AT0B_' + tag))
    return rc, o, RUN / ('AT0B_' + tag) / 'AT0B_C2V001.json'


def at1_cli(fx, l1p, a0b, mp, tag, path=None):
    rec2, c = fx['rec2'], fx['c']
    args = ['agree', 'at1', '--snapshot', fx['snap'], '--snapshot-sha256', snap_sha(fx['snap']), '--l1', l1p,
            '--l1-sha256', sha(l1p), '--fdplan', fx['fd'], '--fdplan-sha256', sha(fx['fd']), '--at0a', fx['at0a'],
            '--at0a-sha256', sha(fx['at0a']), '--at0b', a0b, '--at0b-sha256', sha(a0b), '--phase2-record',
            rec2['record_path'], '--phase2-record-sha256', rec2['record_file_sha256'], '--phase2-registry',
            rec2['registry_path'], '--members', mp, '--members-sha256', sha(mp), '--config', c.cfg, '--config-sha256',
            c.cfg_sha, '--interior-count', 6, '--out-dir', RUN / ('AT1_' + tag)]
    rc, o = cli(path, [str(x) for x in args]) if path else tool(*args)
    p = RUN / ('AT1_' + tag) / 'AT1_C2V001.json'
    return rc, o, (json.loads(p.read_text()) if p.exists() else {})


def chain(fx, tag, kind='linear', vals_eps=0.01, eps_none_rows=(), eps_fn=None, drop_eps=False, eps_len=43,
          eps_raw=None):
    """values -> members -> band (v003 CLI) -> at0b (v003 CLI); returns the paths for at1."""
    fd = json.loads(Path(fx['fd']).read_text())
    vals = values_file(FIX / ('VALUES_%s.json' % tag), fd, kind, eps=vals_eps, eps_none_rows=eps_none_rows)
    u1 = {p['role']: p for p in json.loads(vals.read_text())['points']}
    mp = members_doc(fx['sel2'], fd['u_A']['log_index'], u1['u_A']['result_pin'], lambda u: ngc_toy(u, kind), tag,
                     eps_fn, drop_eps, eps_len, eps_raw)
    rcb, ob, l1d = band_cli_on(fx['snap'], fx['fd'], vals, tag)
    rc0, o0, a0b = at0b_cli(fx, vals, mp, tag)
    return {'vals': vals, 'mp': mp, 'l1': l1d / 'L1_C2V001.json', 'a0b': a0b, 'rc': [rcb, rc0],
            'reasons': [ob.get('reason'), o0.get('reason')], 'fd': fd}


def fx_of(S, key):
    if key == 'seed':
        ph = S['seed_phase2']
        return {'c': S['seed'], 'snap': S['seed_snap'], 'fd': S['seed_fd'], 'at0a': S['seed_at0a'], 'rec2': ph['rec2'],
                'run2': ph['run2'], 'sel2': ph['sel2']}
    if key == 'corner':
        ph = S['corner_phase2']
        return {'c': S['corner'], 'snap': S['corner_snap'], 'fd': S['corner_fd'], 'at0a': S['corner_at0a'],
                'rec2': ph['rec2'], 'run2': ph['run2'], 'sel2': ph['sel2']}
    return S[key]


def upos_of(run2):
    return {p['log_index']: p['u'] for p in run2['exploration']['admitted_points']}


# ----------------------------------------------------------------------------------------------- part-3 fixtures
def t30_fixtures(S):
    """NEARCORNER (0204-style march0 case, u_A = (0.97, 0.03, 0.5), m_id = 1) and CM2 (the 0204 verifier's m_id = 2
    corner, u_A = (1, 0, 0.5), V_I = (1, 1, +-sqrt2)/2), both on the real orchestrator."""
    S['P2'] = load(V002[0], 'phase1_v002_reference_part3')
    nc = Camp('NEARCORNER', (0.94, -0.94, 0.0), 1.0, override={'u_seed': [0.97, 0.03, 0.5]}, speeds=corner_speeds)
    assert nc.until_march0_planned()
    rc, o, out = snap(nc, 'NEARCORNER')
    rcf, of = tool('fdplan', '--config', nc.cfg, '--config-sha256', nc.cfg_sha, '--snapshot', out, '--snapshot-sha256',
                   snap_sha(out), '--interior-count', 6, '--out-dir', RUN / 'FD_NEARCORNER')
    L = fixture_L(out) if rc == 0 else None
    d = rec_of(out)[0] if rc == 0 else {}
    check('T30.fixture_NEARCORNER_march0_snapshot_and_fdplan (u_A = seed (0.97, 0.03, 0.5), m_id = 1)',
          rc == 0 and rcf == 0 and len(L['I']) == 1 and d['march0_wave'] is not None and
          [round(x, 12) for x in L['uA']] == [0.97, 0.03, 0.5],
          {'rc': [rc, rcf], 'reason': [o.get('reason'), of.get('reason')], 'u_A': list(L['uA']) if L else None,
           'V_I': L['VI'].tolist() if L else None, 'b_p1': d.get('b_p1')})
    S['nc'] = {'c': nc, 'snap': out, 'fd': RUN / 'FD_NEARCORNER' / 'FDPLAN_C2V001.json', 'L': L}
    c = Camp('CM2', (1.0, -1.0, 0.0), 1.0, override={'u_seed': [1.0, 0.0, 0.5]}, speeds=m2_speeds)
    fams = []
    while True:
        nxt = c.peek()
        if nxt is None or P.non_prefix_families(nxt):
            break
        fams.append(c.step())
    fams.append(c.step(execute=False))
    rc, o, out = snap(c, 'CM2')
    rc0, o0 = tool('fdplan', '--s0-only', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir', RUN / 'S0_CM2')
    rcf, of = tool('fdplan', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--snapshot', out, '--snapshot-sha256',
                   snap_sha(out), '--interior-count', 6, '--out-dir', RUN / 'FD_CM2')
    s0 = RUN / 'S0_CM2' / 'S0_C2V001.json'
    rca, oa = at0a_cli(c, out, s0, 'CM2')
    fdp = RUN / 'FD_CM2' / 'FDPLAN_C2V001.json'
    final = c.complete()
    rec2 = final['record']
    run2 = json.loads(Path(rec2['record_path']).read_text())['run']
    sel2 = P.v003g_members(c.ctx, run2, 6)
    fx = {'c': c, 'snap': out, 'fd': fdp, 'at0a': RUN / 'AT0A_CM2' / 'AT0A_C2V001.json', 'rec2': rec2, 'run2': run2,
          'sel2': sel2}
    ch = chain(fx, 'CM2', 'linear')
    rc1, o1, doc3 = at1_cli(fx, ch['l1'], ch['a0b'], ch['mp'], 'CM2')
    rc2, o2, doc2 = at1_cli(fx, ch['l1'], ch['a0b'], ch['mp'], 'CM2_V002', path=V002[0])
    L = fixture_L(out) if rc == 0 else None
    d = rec_of(out)[0] if rc == 0 else {}
    check('T30.fixture_CM2_m_id_2_corner_snapshot_fdplan_at0a_band_at0b_at1_v003_and_v002',
          rc == 0 and rc0 == 0 and rcf == 0 and rca == 0 and ch['rc'] == [0, 0] and rc1 == 0 and rc2 == 0 and
          len(L['I']) == 2 and [round(x, 12) for x in L['uA']] == [1.0, 0.0, 0.5],
          {'rc': [rc, rc0, rcf, rca, ch['rc'], rc1, rc2], 'waves': fams, 'boundary': d.get('boundary_call'),
           'march0_wave': d.get('march0_wave'), 'V_I': L['VI'].tolist() if L else None,
           'outcome': [doc2.get('outcome'), doc3.get('outcome')], 'reasons': [o.get('reason'), oa.get('reason'),
                                                                               ch['reasons'], o1.get('reason')]})
    fx.update(L=L, doc3=doc3, doc2=doc2, l1=ch['l1'], vals=ch['vals'], mp=ch['mp'])
    S['cm2'] = fx


# ----------------------------------------------------------------------------------------------- T30: A144 R1
def t30_r1(S):
    import numpy as np
    P2 = S['P2']
    Ls = {'seed': fixture_L(S['seed_snap']), 'corner': fixture_L(S['corner_snap']), 'JAC': fixture_L(S['JAC'][1]),
          'nearcorner': S['nc']['L'], 'cm2': S['cm2']['L']}
    Fs = {'seed': F_of(S['seed_fd']), 'corner': F_of(S['corner_fd']), 'JAC': F_of(RUN / 'FD_JAC_T25' / 'FDPLAN_C2V001.json'),
          'nearcorner': F_of(S['nc']['fd']), 'cm2': F_of(S['cm2']['fd'])}
    L3 = synth_L((0.9, 0.1, 0.5), rand_orth(7), (3.0, 2.0, 1.0), seed=3)
    Ls['synthetic_m_id_3'], Fs['synthetic_m_id_3'] = L3, synth_F(L3, (0.05, 0.05, 0.05))
    S['Ls'], S['Fs'] = Ls, Fs
    # (a) the shared helper's rows are bitwise band_rows' rows (captured from the LP calls band_rows makes)
    res = {}
    for name in Ls:
        seen = []

        def lp(A_, b_, w_, seen=seen):
            seen.append((A_.copy(), b_.copy()))
            return E._lp_max(A_, b_, w_)
        l1_of(Ls[name], Fs[name], lin_g, lp=lp)
        A, b, fam = P.band_region(Ls[name])
        nr, m = len(Ls[name]['rows']), len(Ls[name]['I'])
        slices = [(fam[f].start, fam[f].stop) for f in ('LINEAR_DDO', 'BOX', 'TRUST_RADIUS')]
        bs = sorted(set(bx.tobytes() for _a, bx in seen))
        res[name] = {'lp_calls': len(seen), 'A_bitwise_every_call': all(ax.shape == A.shape and ax.dtype == A.dtype and
                                                                          ax.tobytes() == A.tobytes() for ax, _b in seen),
                     'b_band_bitwise_first_call': bool(seen) and seen[0][1].tobytes() == b.tobytes(),
                     'distinct_b': len(bs), 'slices': slices,
                     'slices_ok': slices == [(0, 2 * nr), (2 * nr, 2 * nr + 6), (2 * nr + 6, 2 * nr + 6 + 2 * m)] and
                     A.shape[0] == 2 * nr + 6 + 2 * m}
    check('T30.R1_band_region_A_and_b_band_bitwise_equal_to_band_rows_and_family_slices (6 fixtures)',
          all(x['A_bitwise_every_call'] and x['b_band_bitwise_first_call'] and x['distinct_b'] == 2 and x['slices_ok']
              for x in res.values()), res)
    # (b) eps = 0 everywhere: failing set, excess, norm_n and outcome byte-identical to v002 (in process)
    sp = S['seed_phase2']
    cp2 = S['corner_phase2']
    seed_m = [(m['log_index'], m['u']) for m in sp['sel2']['points']]
    corner_m = [(m['log_index'], m['u']) for m in cp2['sel2']['points']]
    cm2_m = [(m['log_index'], m['u']) for m in S['cm2']['sel2']['points']]
    VIn, VNn = Ls['nearcorner']['VI'], Ls['nearcorner']['V'][Ls['nearcorner']['N']]
    rn = 0.25
    nc_m, li = [], 300
    for cc in np.linspace(-rn * 0.95, rn * 0.95, 41):   # 0204 NEARCORNER construction: c grid x n grid, in box, DDO-linear
        for nn in np.linspace(-0.3, 0.3, 25):
            u = Ls['nearcorner']['uA'] + VIn.T @ np.array([cc]) + VNn.T @ np.array([nn, 0.0])
            Ln = Ls['nearcorner']
            if np.any(u < 0) or np.any(u > 1) or np.any(np.abs(Ln['qA'] + Ln['S'] @ (VIn.T @ np.array([cc]))) > Ln['zrow']):
                continue
            li += 1
            nc_m.append((li, [float(x) for x in u]))
    S['nc_members'] = nc_m
    cases = {'seed_quad_phase2_members': ('seed', seed_m, lambda u: ngc_toy(u, 'quad')),
             'corner_T27_linear_phase2_members': ('corner', corner_m, lin_g),
             'nearcorner_linear_grid_members': ('nearcorner', nc_m, lin_g),
             'cm2_linear_phase2_members': ('cm2', cm2_m, lin_g)}
    res, eps0 = {}, {}
    for name, (fx, mem, g) in cases.items():
        l1, _m = l1_of(Ls[fx], Fs[fx], g, eps=0.0)
        r2 = sp['run2'] if fx == 'seed' else cp2['run2'] if fx == 'corner' else S['cm2']['run2'] if fx == 'cm2' \
            else run2_of(Ls[fx], mem)
        mv = mv_of(mem, g, eps=0.0)
        f2, _r2 = P2.at1_rows(E, Ls[fx], l1, r2, mv, QIDS)
        f3, _r3 = P.at1_rows(E, Ls[fx], l1, r2, mv, QIDS)
        eps0[name] = (f2, f3, Ls[fx], r2)
        res[name] = {'n_failing': [len(f2), len(f3)], 'byte_identical': proj(f2) == proj(f3),
                     'outcome': ['COVERED' if not f2 else 'SUPERSEDED', 'COVERED' if not f3 else 'SUPERSEDED'],
                     'categories_v002': sorted(set(x['category'] for x in f2)),
                     'categories_v003': sorted(set(x['category'] for x in f3))}
    check('T30.R1_MUST_PASS_eps_0_failing_set_excess_norm_n_and_outcome_byte_identical_to_v002 (in process, 4 fixtures)',
          all(x['byte_identical'] and x['outcome'][0] == x['outcome'][1] for x in res.values()) and
          sum(x['n_failing'][0] for x in res.values()) > 0, res)
    S['eps0'] = eps0
    clires = {}
    for fxk, kind in (('seed', 'quad'), ('corner', 'linear')):
        fx = fx_of(S, fxk)
        ch = chain(fx, 'EPS0_' + fxk.upper(), kind, vals_eps=0.0, eps_fn=lambda li_, q: 0.0)
        rc3, o3, d3 = at1_cli(fx, ch['l1'], ch['a0b'], ch['mp'], 'EPS0_' + fxk.upper())
        rc2, o2, d2 = at1_cli(fx, ch['l1'], ch['a0b'], ch['mp'], 'EPS0_%s_V002' % fxk.upper(), path=V002[0])
        clires[fxk] = {'rc': [ch['rc'], rc2, rc3], 'n_failing': [len(d2.get('failing') or []), len(d3.get('failing') or [])],
                       'outcome': [d2.get('outcome'), d3.get('outcome')],
                       'byte_identical': bool(d2) and proj(d2['failing']) == proj(d3['failing']),
                       'categories': [sorted(set(x['category'] for x in d2.get('failing') or [])),
                                      sorted(set(x['category'] for x in d3.get('failing') or []))]}
    check('T30.R1_MUST_PASS_eps_0_CLI_at1_v003_vs_v002_failing_set_excess_norm_n_outcome_byte_identical (seed quad, corner)',
          all(x['rc'] == [[0, 0], 0, 0] and x['byte_identical'] and x['outcome'][0] == x['outcome'][1] and
              x['n_failing'][0] > 0 for x in clires.values()), clires)
    # (c) T27 corner: v002's 316 NGC_NONLINEAR pairs (linear toy) read OUTSIDE_BOX_SLICE ['BOX'] under v003
    # port: v002's corner at1 (formerly read from v002's part-1 shadow directory) is run directly on the same inputs
    rcv2, _ov2, d2 = at1_cli(fx_of(S, 'corner'), cp2['l1'], RUN / 'AT0B_CORNER' / 'AT0B_C2V001.json', cp2['members'],
                             'CORNER_V002', path=V002[0])
    d2 = d2 if rcv2 == 0 else {'failing': [], 'outcome': None}
    d3 = json.loads((RUN / 'AT1_CORNER' / 'AT1_C2V001.json').read_text())
    Lc = Ls['corner']
    upos = upos_of(cp2['run2'])
    reg = P.band_region(Lc)
    relab = [P.region_violation(E, reg, Lc['VI'] @ (np.array(upos[x['log_index']]) - Lc['uA']))[0] for x in d2['failing']]
    f2e, f3e, _L, _r = eps0['corner_T27_linear_phase2_members']
    check('T30.R1_MUST_PASS_T27_corner_316_v002_NGC_NONLINEAR_pairs_read_OUTSIDE_BOX_SLICE_[BOX]',
          len(d2['failing']) == 316 and all(x['category'] == 'NGC_NONLINEAR' for x in d2['failing']) and
          all(v == ['BOX'] for v in relab) and
          all(indep_region(Lc, Lc['VI'] @ (np.array(upos[x['log_index']]) - Lc['uA']))[0] == ['BOX'] for x in d2['failing'])
          and len(d3['failing']) > 0 and all(x['category'] == 'OUTSIDE_BOX_SLICE' and x['region_rows_violated'] == ['BOX']
                                             for x in d3['failing']) and
          len(f3e) > 0 and all(x['category'] == 'OUTSIDE_BOX_SLICE' and x['region_rows_violated'] == ['BOX'] for x in f3e),
          {'v002_cli_failing': len(d2['failing']), 'v002_categories': sorted(set(x['category'] for x in d2['failing'])),
           'v003_relabel_of_v002_pairs': sorted(set(tuple(v) for v in relab)), 'v003_cli_failing': len(d3['failing']),
           'v003_cli_categories': sorted(set(x['category'] for x in d3['failing'])), 'eps0_in_process_failing': len(f3e),
           'outcomes': [d2['outcome'], d3['outcome']]})
    # (d) NEARCORNER grid (0204-style): box-binding failures read OUTSIDE_BOX_SLICE, never NGC_NONLINEAR
    Ln, Fn = Ls['nearcorner'], Fs['nearcorner']
    l1n, _m = l1_of(Ln, Fn, lin_g, eps=0.01)
    r2n = run2_of(Ln, nc_m)
    f3n, _r = P.at1_rows(E, Ln, l1n, r2n, mv_of(nc_m, lin_g), QIDS)
    f2e, f3e, _L, _r = eps0['nearcorner_linear_grid_members']
    box_lo = max((-Ln['uA'][j] / Ln['VI'][0][j]) if Ln['VI'][0][j] > 0 else ((1 - Ln['uA'][j]) / Ln['VI'][0][j])
                 for j in range(3) if abs(Ln['VI'][0][j]) > 1e-12)
    box_hi = min(((1 - Ln['uA'][j]) / Ln['VI'][0][j]) if Ln['VI'][0][j] > 0 else (-Ln['uA'][j] / Ln['VI'][0][j])
                 for j in range(3) if abs(Ln['VI'][0][j]) > 1e-12)
    um = dict(nc_m)
    outside = lambda x: not (box_lo - 1e-12 <= float((Ln['VI'] @ (np.array(um[x['log_index']]) - Ln['uA']))[0]) <= box_hi + 1e-12)
    check('T30.R1_MUST_PASS_NEARCORNER_pairs_read_OUTSIDE_BOX_SLICE (0204-style grid, exactly linear NGC toy)',
          len(f3n) > 0 and all(x['category'] == 'OUTSIDE_BOX_SLICE' and x['region_rows_violated'] == ['BOX'] and outside(x)
                               for x in f3n) and
          len(f2e) > 0 and all(x['category'] == 'NGC_NONLINEAR' for x in f2e) and
          all(x['category'] == 'OUTSIDE_BOX_SLICE' for x in f3e),
          {'n_members': len(nc_m), 'box_c_interval': [box_lo, box_hi], 'trust_radius': rn,
           'v003_eps_0.01_failing_pairs': len(f3n), 'v003_failing_members': len(set(x['log_index'] for x in f3n)),
           'v003_categories': sorted(set(x['category'] for x in f3n)), 'eps0_v002_failing': len(f2e),
           'eps0_v002_categories': sorted(set(x['category'] for x in f2e)),
           'eps0_v003_categories': sorted(set(x['category'] for x in f3e))})
    # (e) members moving along the corner face with a curvature toy read NGC_NONLINEAR (BOX max violation <= 1e-12)
    fm = null_members(Lc, 500)
    l1c, _m = l1_of(Lc, Fs['corner'], facecurv_g, eps=0.01)
    f3c, _r = P.at1_rows(E, Lc, l1c, run2_of(Lc, fm), mv_of(fm, facecurv_g), QIDS)
    raw_box = sum(1 for _li, u in fm if 'BOX' in indep_region(Lc, Lc['VI'] @ (np.array(u) - Lc['uA']), 0.0, False)[0])
    cnz = sum(1 for _li, u in fm if float(np.max(np.abs(Lc['VI'] @ (np.array(u) - Lc['uA'])))) != 0.0)
    check('T30.R1_MUST_PASS_along_face_members_with_a_curvature_toy_read_NGC_NONLINEAR (BOX max violation <= 1e-12)',
          len(f3c) > 0 and all(x['category'] == 'NGC_NONLINEAR' and x['region_rows_violated'] == [] and
                               x['region_max_violation']['BOX'] <= 1e-12 for x in f3c),
          {'n_members': len(fm), 'members_with_c_not_exactly_0': cnz, 'failing_pairs': len(f3c),
           'failing_members': len(set(x['log_index'] for x in f3c)),
           'max_BOX_violation': max([x['region_max_violation']['BOX'] for x in f3c] or [None]),
           'members_the_rejected_exact_unclipped_test_would_label_BOX': raw_box})
    # (f) members exactly on a face (u_k = 0.0 or 1.0) at m_id = 3 are not BOX
    face_m = [(601, [1.0, 0.1, 0.5]), (602, [0.9, 0.0, 0.5]), (603, [1.0, 0.0, 0.5]), (604, [1.0, 0.05, 0.45]),
              (605, [0.95, 0.0, 0.55]), (606, [1.0, 0.15, 0.5]), (607, [0.85, 0.0, 0.5]), (608, [1.0, 0.0, 0.48])]
    l13, _m = l1_of(L3, Fs['synthetic_m_id_3'], lin_g, eps=0.01)
    f33, _r = P.at1_rows(E, L3, l13, run2_of(L3, face_m), mv_of(face_m, bumped(lin_g)), QIDS)
    raw3 = sum(1 for _li, u in face_m if 'BOX' in indep_region(L3, L3['VI'] @ (np.array(u) - L3['uA']), 0.0, False)[0])
    check('T30.R1_MUST_PASS_members_exactly_on_a_face_at_m_id_3_are_not_BOX',
          len(L3['I']) == 3 and len(set(x['log_index'] for x in f33)) == len(face_m) and
          all('BOX' not in x['region_rows_violated'] and x['category'] == 'NGC_NONLINEAR' for x in f33),
          {'members': len(face_m), 'failing_members': len(set(x['log_index'] for x in f33)),
           'categories': sorted(set(x['category'] for x in f33)),
           'max_BOX_violation': max([x['region_max_violation']['BOX'] for x in f33] or [None]),
           'members_the_rejected_exact_unclipped_test_would_label_BOX': raw3})
    # (g) c from the band's own optima (du_at_lo, du_at_hi) gives [] on every AVAILABLE row
    res = {}
    for name in Ls:
        if name == 'seed':
            rows = json.loads(Path(S['l1']).read_text())['rows']
        elif name == 'corner':
            rows = json.loads(Path(cp2['l1']).read_text())['rows']
        elif name == 'cm2':
            rows = json.loads(Path(S['cm2']['l1']).read_text())['rows']
        else:
            rows = l1_of(Ls[name], Fs[name], lin_g)[0]['rows']
        reg = P.band_region(Ls[name])
        n, bad, raw = 0, [], 0
        for x in rows:
            if x['status'] != 'AVAILABLE':
                continue
            for key in ('du_at_lo', 'du_at_hi'):
                cvec = Ls[name]['VI'] @ np.array(x[key])
                n += 1
                if P.region_violation(E, reg, cvec)[0] or indep_region(Ls[name], cvec)[0]:
                    bad.append((x['id'], key))
                raw += bool(indep_region(Ls[name], cvec, 0.0, False)[0])
        res[name] = {'optima': n, 'bad': bad[:4], 'rejected_exact_unclipped_test_flags': raw}
    check('T30.R1_MUST_PASS_c_at_the_band_optima_gives_[]_on_every_AVAILABLE_row (6 fixtures)',
          all(x['optima'] > 0 and not x['bad'] for x in res.values()), res)
    # (h) the m_id = 2 corner keeps OUTSIDE_TRUST_RADIUS
    d2, d3 = S['cm2']['doc2'], S['cm2']['doc3']
    Lm, upm = S['cm2']['L'], upos_of(S['cm2']['run2'])
    lab3 = {x['log_index']: P.region_violation(E, P.band_region(Lm), Lm['VI'] @ (np.array(upm[x['log_index']]) - Lm['uA']))[0]
            for x in d2.get('failing') or []}
    check('T30.R1_MUST_PASS_m_id_2_corner_v002_OUTSIDE_TRUST_RADIUS_failures_keep_OUTSIDE_TRUST_RADIUS',
          len(d2.get('failing') or []) > 0 and all(x['category'] == 'OUTSIDE_TRUST_RADIUS' for x in d2['failing']) and
          all(v and v[0] == 'TRUST_RADIUS' for v in lab3.values()) and
          all(x['category'] == 'OUTSIDE_TRUST_RADIUS' for x in d3.get('failing') or [] if x['log_index'] in lab3),
          {'v002_failing': len(d2.get('failing') or []),
           'v002_categories': sorted(set(x['category'] for x in d2.get('failing') or [])),
           'v003_failing': len(d3.get('failing') or []),
           'v003_categories': sorted(set(x['category'] for x in d3.get('failing') or [])),
           'v003_region_lists_of_v002_members': sorted(set(tuple(v) for v in lab3.values()))})
    # (i)-(k) MUST_FAIL label cases on hand-placed members (bumped NGC so every member fails)
    tb = [(701, [1.0, 0.4, 0.5]), (702, [0.9, 0.5, 0.5]), (703, [1.0, 0.5, 0.2])]
    l1c0, _m = l1_of(Lc, Fs['corner'], lin_g)
    ftb, _r = P.at1_rows(E, Lc, l1c0, run2_of(Lc, tb), mv_of(tb, bumped(lin_g)), QIDS)
    lists = {x['log_index']: x['region_rows_violated'] for x in ftb}
    check('T30.R1_MUST_FAIL_member_outside_trust_and_box_lists_both_TRUST_RADIUS_then_BOX_not_BOX_alone',
          len(lists) == len(tb) and all(v[:2] == ['TRUST_RADIUS', 'BOX'] for v in lists.values()) and
          all(x['category'] == 'OUTSIDE_TRUST_RADIUS' for x in ftb), lists)
    near = [(711, [1.0, 2e-6, 0.5]), (712, [1.0 - 1e-6, 3e-6, 0.5]), (713, [1.0, 2e-6, 0.6]), (714, [1.0, 1.5e-6, 0.3])]
    fnb, _r = P.at1_rows(E, Lc, l1c0, run2_of(Lc, near), mv_of(near, bumped(lin_g)), QIDS)
    fnb2, _r = P2.at1_rows(E, Lc, l1c0, run2_of(Lc, near), mv_of(near, bumped(lin_g)), QIDS)
    vb = {x['log_index']: x['region_max_violation']['BOX'] for x in fnb}
    check('T30.R1_MUST_FAIL_member_outside_the_box_slice_by_1e-6_is_never_NGC_NONLINEAR',
          len(vb) == len(near) and all(x['category'] == 'OUTSIDE_BOX_SLICE' for x in fnb) and
          all(3e-7 <= v <= 3e-6 for v in vb.values()),
          {'box_violation': vb, 'v003': sorted(set(x['category'] for x in fnb)),
           'v002_label_for_contrast': sorted(set(x['category'] for x in fnb2))})
    Vt = rand_orth(11)
    Lu = synth_L((0.5, 0.4, 0.6), Vt, (3.0, 0.0, 0.0), seed=5)
    Lu['qA'][0] = np.nextafter(Lu['zrow'][0], np.inf)   # f == hi up to one ulp: b_band row 0 = zrow - qA < 0
    A_, b_, _f = P.band_region(Lu)
    um_ = [(721, [float(x) for x in Lu['uA']])] + null_members(Lu, 722, steps=(-0.2, 0.1, 0.3), ts=(-0.2, 0.0, 0.2))
    l1u, _m = l1_of(Lu, synth_F(Lu, (0.05, 0.05, 0.05)), lin_g)
    fu, _r = P.at1_rows(E, Lu, l1u, run2_of(Lu, um_), mv_of(um_, bumped(lin_g)), QIDS)
    fu2, _r = P2.at1_rows(E, Lu, l1u, run2_of(Lu, um_), mv_of(um_, bumped(lin_g)), QIDS)
    raw_u = indep_region(Lu, Lu['VI'] @ np.zeros(3), 0.0, False)[0]
    check('T30.R1_MUST_FAIL_f_equals_hi_by_an_ulp_a_member_at_c_about_0_is_never_LINEAR_DDO',
          float(b_[0]) < 0.0 and len(set(x['log_index'] for x in fu)) == len(um_) and
          all('LINEAR_DDO' not in x['region_rows_violated'] and x['category'] == 'NGC_NONLINEAR' for x in fu),
          {'b_band_row0': float(b_[0]), 'members': len(um_), 'v003_categories': sorted(set(x['category'] for x in fu)),
           'max_LINEAR_DDO_violation': max(x['region_max_violation']['LINEAR_DDO'] for x in fu),
           'rejected_exact_unclipped_test_on_the_u_A_member': raw_u,
           'v002_label_for_contrast': sorted(set(x['category'] for x in fu2))})
    # the clip itself (beyond the tolerance): a SYNTHETIC row with b_band = -1e-9, which _lp_max solves as b = 0
    Lk = synth_L((0.5, 0.4, 0.6), Vt, (3.0, 0.0, 0.0), seed=5)
    Lk['qA'][0] = Lk['zrow'][0] + 1e-9
    Ak, bk, _f = P.band_region(Lk)
    l1k, _m = l1_of(Lk, synth_F(Lk, (0.05, 0.05, 0.05)), lin_g)
    fk, _r = P.at1_rows(E, Lk, l1k, run2_of(Lk, um_), mv_of(um_, bumped(lin_g)), QIDS)
    check('T30.R1_MUST_FAIL_a_row_with_b_band_below_zero_is_read_with__lp_max_clip_max(b,0) (b = -1e-9; c about 0 is '
          'never LINEAR_DDO)',
          -2e-9 < float(bk[0]) < -5e-10 and all(x['lp_status']['band_max'] == 'OPTIMAL' for x in l1k['rows']) and
          len(set(x['log_index'] for x in fk)) == len(um_) and
          all('LINEAR_DDO' not in x['region_rows_violated'] and x['category'] == 'NGC_NONLINEAR' for x in fk),
          {'b_band_row0': float(bk[0]), 'v003_categories': sorted(set(x['category'] for x in fk)),
           'max_LINEAR_DDO_violation': max(x['region_max_violation']['LINEAR_DDO'] for x in fk),
           'unclipped_test_with_the_tolerance_on_the_u_A_member': indep_region(Lk, np.zeros(1), LP_EPS, False)[0]})
    # (l) excess = geometric_part + residual_part; residual_part = +-rho - a_q - e_q
    res = {}
    dcorner = json.loads((RUN / 'AT1_CORNER' / 'AT1_C2V001.json').read_text())
    for name, doc, l1p, run2, snp in (('seed_Q1', S['at1_q1'][0], S['at1_q1'][1], sp['run2'], S['seed_snap']),
                                      ('corner_T27', dcorner, cp2['l1'], cp2['run2'], S['corner_snap'])):
        L_ = fixture_L(snp)
        rows1 = {x['id']: x for x in json.loads(Path(l1p).read_text())['rows']}
        rho = {(x['log_index'], x['id']): x['ngc_linearity_residual'] for x in doc['reported']['ngc_linearity_residuals']}
        eqm = {(x['log_index'], x['id']): x['e_q'] for x in doc['reported']['e_q_per_member_row']}
        up = upos_of(run2)
        bad = []
        for x in doc['failing']:
            b1 = rows1[x['id']]
            cvec = L_['VI'] @ (np.array(up[x['log_index']]) - L_['uA'])
            kc = float(np.array(b1['K_q']) @ (L_['VI'].T @ cvec))
            e = eqm[(x['log_index'], x['id'])]
            e = 0.0 if isinstance(e, str) else e
            gup, glo = kc - (b1['hi'] - b1['g_A']), (b1['lo'] - b1['g_A']) - kc
            r_ = rho[(x['log_index'], x['id'])]
            sc = 1e-9 * (1.0 + abs(x['excess']) + abs(kc) + abs(r_))
            up_ok = abs(x['geometric_part'] - gup) <= sc and abs(x['residual_part'] - (r_ - b1['a_q'] - e)) <= sc
            lo_ok = abs(x['geometric_part'] - glo) <= sc and abs(x['residual_part'] - (-r_ - b1['a_q'] - e)) <= sc
            if abs(x['geometric_part'] + x['residual_part'] - x['excess']) > 1e-12 * (1.0 + abs(x['excess'])) or \
                    not (up_ok or lo_ok):
                bad.append((x['log_index'], x['id']))
        res[name] = {'failing': len(doc['failing']), 'bad': bad[:4]}
    check('T30.R1_excess_equals_geometric_part_plus_residual_part_and_residual_part_is_+-rho_minus_a_q_minus_e_q',
          all(x['failing'] > 0 and not x['bad'] for x in res.values()), res)


# ----------------------------------------------------------------------------------------------- T31: A144 R2
def indep_extent(A, b):
    """Independent extents of c_j over A c <= max(b, 0) (1-D: bounds; m >= 2: vertex enumeration over m-row subsets)."""
    import itertools
    import numpy as np
    b = np.maximum(b, 0.0)
    M, m = A.shape
    if m == 1:
        a = A[:, 0]
        return [[max([b[i] / a[i] for i in range(M) if a[i] < 0] or [-math.inf]),
                 min([b[i] / a[i] for i in range(M) if a[i] > 0] or [math.inf])]]
    verts = []
    for idx in itertools.combinations(range(M), m):
        Mx = A[list(idx)]
        if abs(float(np.linalg.det(Mx))) < 1e-14:
            continue
        x = np.linalg.solve(Mx, b[list(idx)])
        if np.all(A @ x <= b + 1e-9):
            verts.append(x)
    return [[min(float(v[k]) for v in verts), max(float(v[k]) for v in verts)] for k in range(m)]


def t31_r2(S):
    import numpy as np
    d3c = json.loads((RUN / 'AT1_CORNER' / 'AT1_C2V001.json').read_text())['reported']
    check('T31.R2_MUST_PASS_m_id_1_corner_band_region_extent_[0.0,0.0]_single_point_true_BOX_CORNER (T27 CLI)',
          all(x['extent'] == [0.0, 0.0] and x['lp_status'] == ['OPTIMAL', 'OPTIMAL'] for x in d3c['band_region_extent'])
          and d3c['band_region_single_point'] is True and d3c['band_region_single_point_reason'] == 'BOX_CORNER' and
          [x['linear_region'] for x in d3c['identified_projection_vs_linear_region']] == [[0.0, 0.0]],
          {k: d3c[k] for k in ('band_region_extent', 'band_region_single_point', 'band_region_single_point_reason')})
    dm = S['cm2']['doc3']['reported']
    check('T31.R2_MUST_PASS_m_id_2_corner_single_point_false_reason_null (CM2 CLI; a segment c1 = -c2)',
          dm['band_region_single_point'] is False and dm['band_region_single_point_reason'] is None and
          any(x['extent'] != [0.0, 0.0] for x in dm['band_region_extent']),
          {k: dm[k] for k in ('band_region_extent', 'band_region_single_point', 'band_region_single_point_reason')})
    di = S['at1_q1'][0]['reported']
    check('T31.R2_MUST_PASS_interior_single_point_false (seed Q1 CLI)',
          di['band_region_single_point'] is False and di['band_region_single_point_reason'] is None,
          {k: di[k] for k in ('band_region_extent', 'band_region_single_point', 'band_region_single_point_reason')})
    # independent extents
    res = {}
    for name in ('seed', 'corner', 'nearcorner', 'cm2'):
        L = S['Ls'][name]
        A, b, fam = P.band_region(L)
        ext, sp, why = P.band_region_extent(E, L)
        ind = indep_extent(A, b)
        dif = max(abs(x['extent'][k] - ind[j][k]) for j, x in enumerate(ext) for k in (0, 1))
        res[name] = {'tool': [x['extent'] for x in ext], 'independent': ind, 'max_abs_diff': dif, 'single': sp,
                     'reason': why, 'box_only_independent': indep_extent(A[fam['BOX']], b[fam['BOX']])}
    check('T31.R2_band_region_extent_equals_an_independent_computation_within_1e-12 (seed, corner, nearcorner, cm2)',
          all(x['max_abs_diff'] <= 1e-12 for x in res.values()) and res['corner']['single'] is True and
          res['seed']['single'] is False and res['cm2']['single'] is False, res)
    # OTHER_ROWS: a single point from two DDO rows at zero slack, the box not binding
    Lo = synth_L((0.5, 0.5, 0.5), rand_orth(21), (3.0, 0.0, 0.0), seed=9)
    svi = (Lo['S'] @ Lo['VI'].T)[:, 0]
    sgn = 1.0 if np.sum(svi > 0) >= 2 else -1.0
    i, j = [k for k in range(len(svi)) if sgn * svi[k] > 0][:2]
    Lo['qA'][i], Lo['qA'][j] = Lo['zrow'][i], -Lo['zrow'][j]   # row i upper and row j lower at zero slack
    ext, sp, why = P.band_region_extent(E, Lo)
    A, b, fam = P.band_region(Lo)
    check('T31.R2_MUST_PASS_single_point_from_DDO_rows_with_the_box_not_binding_reads_OTHER_ROWS',
          sp is True and why == 'OTHER_ROWS' and indep_extent(A[fam['BOX']], b[fam['BOX']])[0][1] > 0.1,
          {'extent': ext, 'single': sp, 'reason': why, 'box_only': indep_extent(A[fam['BOX']], b[fam['BOX']])})
    # MUST_FAIL: a non-OPTIMAL extent program prints NOT_AVAILABLE, never true/false, never refuses, changes no row

    def lp_fault(A_, b_, w_):
        c_, _st = E._lp_max(A_, b_, w_)
        return c_, 'ITERATION_LIMIT'
    res = {}
    for name, fxk in (('corner', 'corner'), ('seed', 'seed')):
        L = S['Ls'][name]
        ph = S['corner_phase2'] if name == 'corner' else S['seed_phase2']
        l1p = ph['l1'] if name == 'corner' else S['at1_q1'][1]
        mpp = ph['members'] if name == 'corner' else S['at1_q1'][2]
        l1 = dict(json.loads(Path(l1p).read_text()), fd_du=[f['du'] for f in S['Fs'][name]])
        mvals = json.loads(Path(mpp).read_text())
        mv = {p['log_index']: p for p in mvals['points']}
        f_ok, r_ok = P.at1_rows(E, L, l1, ph['run2'], mv, QIDS)
        f_bad, r_bad = P.at1_rows(E, L, l1, ph['run2'], mv, QIDS, lp=lp_fault)
        same = json.dumps(f_ok) == json.dumps(f_bad) and all(json.dumps(r_ok[k]) == json.dumps(r_bad[k]) for k in r_ok
                                                             if not k.startswith('band_region'))
        res[name] = {'single_ok': r_ok['band_region_single_point'], 'single_fault': r_bad['band_region_single_point'],
                     'reason_fault': r_bad['band_region_single_point_reason'], 'extent_fault': r_bad['band_region_extent'],
                     'rows_and_failing_unchanged': same}
    check('T31.R2_MUST_FAIL_non_OPTIMAL_extent_program_reads_NOT_AVAILABLE_never_filled_and_changes_no_row',
          all(x['single_fault'] == 'NOT_AVAILABLE' and x['reason_fault'] is None and x['rows_and_failing_unchanged'] and
              all(e['extent'] == ['NOT_AVAILABLE', 'NOT_AVAILABLE'] for e in x['extent_fault']) for x in res.values())
          and res['corner']['single_ok'] is True, res)


# ----------------------------------------------------------------------------------------------- T32: A144 R3
def adversarial_noise(L, Fs, members, eps_q, eps_m, kappa=1.0 - 1e-9):
    """Honest noise at the certificate bound (|delta| = kappa eps) with adversarial signs: on row q the signs maximise
    |nu| = |delta_m - delta_A (1 - sum t) - sum delta_Fk t_k| for member members[q % n] (upper miss on even rows,
    lower on odd rows); the other members get +-eps_m."""
    import numpy as np
    du = np.array([f['du'] for f in Fs])
    nP, nM = {}, {}
    for q in range(43):
        li_d, u_d = members[q % len(members)]
        t = (np.array(u_d) - L['uA']) / du
        sg = 1.0 if q % 2 == 0 else -1.0
        nP[('u_A', q)] = -sg * eps_q * (1.0 if (1.0 - float(t.sum())) >= 0 else -1.0) * kappa
        for k, f in enumerate(Fs):
            nP[(f['role'], q)] = -sg * eps_q * (1.0 if t[k] >= 0 else -1.0) * kappa
        for li, _u in members:
            nM[(li, q)] = sg * eps_m * kappa if li == li_d else (1.0 if (li + q) % 2 else -1.0) * eps_m * kappa
    return nP, nM


def random_noise(Fs, members, eps_q, eps_m, rng):
    nP, nM = {}, {}
    for q in range(43):
        for role in ['u_A'] + [f['role'] for f in Fs]:
            nP[(role, q)] = float(rng.uniform(-eps_q, eps_q))
        for li, _u in members:
            nM[(li, q)] = float(rng.uniform(-eps_m, eps_m))
    return nP, nM


def inregion_members(L, start, n, rng, shrink=0.9):
    """Members whose c lies inside the band region (independent rule) with random near-null components, in the box."""
    import numpy as np
    A, b, _f = P.band_region(L)
    m = len(L['I'])
    VN = L['V'][L['N']] if L['N'] else np.zeros((0, 3))
    out, li, tries = [], start, 0
    while len(out) < n and tries < 20000:
        tries += 1
        c = rng.uniform(-0.25, 0.25, size=m) * shrink
        u = L['uA'] + L['VI'].T @ c + (VN.T @ rng.uniform(-0.3, 0.3, size=len(VN)) if len(VN) else 0.0)
        if np.any(u < 0) or np.any(u > 1):
            continue
        cc = L['VI'] @ (u - L['uA'])
        if indep_region(L, cc, -1e-9)[0] or P.region_violation(E, (A, b, _f), cc)[0]:
            continue
        out.append((li, [float(x) for x in u]))
        li += 1
    return out


def t32_r3(S):
    import numpy as np
    P2 = S['P2']
    # (a) e_q equals the independent exact formula (corner CLI, interior CLI with eps varying per member and row, face)
    fxs = fx_of(S, 'seed')
    ch = chain(fxs, 'R3_SEED', 'quad', eps_fn=lambda li, q: 0.004 + 0.001 * ((li + q) % 7))
    rc, o, doc = at1_cli(fxs, ch['l1'], ch['a0b'], ch['mp'], 'R3_SEED')
    S['r3_seed'] = (doc, ch)
    res = {}
    for name, d_, l1p, mpp, run2, fdp in (
            ('interior_seed_cli', doc, ch['l1'], ch['mp'], fxs['run2'], fxs['fd']),
            ('corner_T27_cli', json.loads((RUN / 'AT1_CORNER' / 'AT1_C2V001.json').read_text()), S['corner_phase2']['l1'],
             S['corner_phase2']['members'], S['corner_phase2']['run2'], S['corner_fd'])):
        fd = json.loads(Path(fdp).read_text())
        du = [f['du'] for f in fd['F']]
        uA = np.array(fd['u_A']['u'])
        rows1 = {x['id']: x for x in json.loads(Path(l1p).read_text())['rows']}
        em = {p['log_index']: p['eps_km_s'] for p in json.loads(Path(mpp).read_text())['points']}
        up = upos_of(run2)
        bad, n, nA = [], 0, 0
        for x in d_['reported']['e_q_per_member_row']:
            want = r3_eq(em[x['log_index']][QIDS.index(x['id'])], rows1[x['id']]['eps_q'],
                         np.array(up[x['log_index']]) - uA, du)
            n += 1
            if not isinstance(x['e_q'], float) or abs(x['e_q'] - want) > 1e-12 * max(1.0, abs(want)):
                bad.append((x['log_index'], x['id'], x['e_q'], want))
            if x['log_index'] == fd['u_A']['log_index']:
                nA += 1
                if x['e_q'] != x['eps_m'] + rows1[x['id']]['eps_q']:
                    bad.append(('u_A', x['id'], x['e_q']))
        res[name] = {'pairs': n, 'u_A_pairs': nA, 'bad': bad[:4], 'signed_du': du, 'outcome': d_.get('outcome')}
    Lf = synth_L((1.0, 0.4, 0.5), rand_orth(31), (3.0, 2.0, 0.0), seed=13)
    Ff = synth_F(Lf, (-0.05, 0.05, 0.05))
    rng = np.random.default_rng(4242)
    fmem = inregion_members(Lf, 800, 6, rng) + [(899, [1.0, 0.7, 0.1])]
    l1f, _m = l1_of(Lf, Ff, lin_g, eps=0.02)
    mvf = mv_of(fmem, lin_g)
    for li, p in mvf.items():
        p['eps_km_s'] = [float(x) for x in rng.uniform(0.001, 0.03, size=43)]
    _ff, rf = P.at1_rows(E, Lf, l1f, run2_of(Lf, fmem), mvf, QIDS)
    um = dict(fmem)
    badf = [(x['log_index'], x['id']) for x in rf['e_q_per_member_row']
            if abs(x['e_q'] - r3_eq(mvf[x['log_index']]['eps_km_s'][QIDS.index(x['id'])], 0.02,
                                    np.array(um[x['log_index']]) - Lf['uA'], [f['du'] for f in Ff])) >
            1e-12 * max(1.0, x['e_q'])]
    res['face_synthetic_in_process'] = {'pairs': len(rf['e_q_per_member_row']), 'bad': badf[:4],
                                        'signed_du': [f['du'] for f in Ff]}
    check('T32.R3_MUST_PASS_e_q_equals_the_independent_E_A133_2b_formula_within_1e-12_rel (corner, interior, face)',
          rc == 0 and ch['rc'] == [0, 0] and all(x['pairs'] > 0 and not x['bad'] for x in res.values()), res)
    check('T32.R3_MUST_PASS_u_A_member_e_q_is_exactly_eps_m_plus_eps_q (seed and corner CLI)',
          res['interior_seed_cli']['u_A_pairs'] > 0 and res['corner_T27_cli']['u_A_pairs'] > 0 and
          not res['interior_seed_cli']['bad'] and not res['corner_T27_cli']['bad'],
          {k: res[k]['u_A_pairs'] for k in ('interior_seed_cli', 'corner_T27_cli')})
    # (b) honest noise at the bound, adversarial signs, exactly linear NGC: v003 COVERED; v002 SUPERSEDED at the corner
    res = {}
    Lc, Fc = S['Ls']['corner'], S['Fs']['corner']
    Ls_, Fs_ = S['Ls']['seed'], S['Fs']['seed']
    cm = null_members(Lc, 900)
    sm = inregion_members(Ls_, 950, 12, np.random.default_rng(77))
    fm = inregion_members(Lf, 980, 10, np.random.default_rng(78))
    for name, L, Fs, mem, e_q, e_m in (('corner_T27_null_members', Lc, Fc, cm, 0.01, 0.02),
                                       ('interior_seed_inregion', Ls_, Fs_, sm, 0.01, 0.02),
                                       ('face_synthetic_inregion', Lf, Ff, fm, 0.02, 0.01)):
        nP, nM = adversarial_noise(L, Fs, mem, e_q, e_m)
        l1, _m = l1_of(L, Fs, lin_g, eps=e_q, noise=nP)
        r2 = run2_of(L, mem)
        mv = mv_of(mem, lin_g, eps=e_m, noise=nM)
        f3, r3 = P.at1_rows(E, L, l1, r2, mv, QIDS)
        f2, _r2 = P2.at1_rows(E, L, l1, r2, mv, QIDS)
        regs = [indep_region(L, L['VI'] @ (np.array(u) - L['uA']))[0] for _li, u in mem]
        # slack of the designated pairs relative to their own e_q (at the bound: about 1e-9)
        rows1 = {x['id']: x for x in l1['rows']}
        VN = L['V'][L['N']] if L['N'] else np.zeros((0, 3))
        sl = []
        for q, qid in enumerate(QIDS):
            li_d, u_d = mem[q % len(mem)]
            b1 = rows1[qid]
            D = np.array(u_d) - L['uA']
            sh = float(np.array(b1['K_q']) @ (VN.T @ (VN @ D))) if len(VN) else 0.0
            e = r3_eq(e_m, b1['eps_q'], D, [f['du'] for f in Fs])
            g = mv[li_d]['speeds_km_s'][q]
            hi, lo = b1['hi'] + b1['a_q'] + e + sh, b1['lo'] - b1['a_q'] - e + sh
            sl.append(((hi - g) if q % 2 == 0 else (g - lo)) / e)
        res[name] = {'members': len(mem), 'all_in_region': all(not v for v in regs), 'v003_failing': len(f3),
                     'v002_failing': len(f2), 'outcome': ['SUPERSEDED' if f2 else 'COVERED', 'SUPERSEDED' if f3 else 'COVERED'],
                     'designated_pair_min_slack_over_e_q': min(sl), 'designated_pair_max_slack_over_e_q': max(sl),
                     'a_q_max': max(x['a_q'] for x in l1['rows'])}
    check('T32.R3_MUST_PASS_honest_noise_at_the_bound_adversarial_signs_exactly_linear_NGC_reads_COVERED (v002 '
          'SUPERSEDED at the corner)',
          all(x['all_in_region'] and x['v003_failing'] == 0 and x['members'] >= 6 and
              x['designated_pair_min_slack_over_e_q'] >= 0 for x in res.values()) and
          res['corner_T27_null_members']['v002_failing'] > 0 and res['corner_T27_null_members']['a_q_max'] == 0.0 and
          res['corner_T27_null_members']['designated_pair_max_slack_over_e_q'] < 1e-6, res)
    # (c) the guarantee under random noise within the certificates: no in-region pair fails (linear NGC)
    rng = np.random.default_rng(99)
    res = {}
    for name, L, Fs, mem in (('corner', Lc, Fc, cm), ('interior', Ls_, Fs_, sm), ('face', Lf, Ff, fm)):
        nf, nt = 0, 0
        for _t in range(15):
            nP, nM = random_noise(Fs, mem, 0.01, 0.02, rng)
            l1, _m = l1_of(L, Fs, lin_g, eps=0.01, noise=nP)
            f3, _r3 = P.at1_rows(E, L, l1, run2_of(L, mem), mv_of(mem, lin_g, eps=0.02, noise=nM), QIDS)
            nf += len(f3)
            nt += 1
        res[name] = {'trials': nt, 'pairs_per_trial': 43 * len(mem), 'failing_pairs_total': nf}
    check('T32.R3_MUST_PASS_guarantee_random_noise_within_certificates_no_in_region_pair_fails (linear NGC; 45 trials)',
          all(x['failing_pairs_total'] == 0 for x in res.values()), res)
    # (d)-(h) the members-file contract and the per-pair flags, through the CLI
    chn = chain(fxs, 'R3_NOEPS', 'linear', drop_eps=True)
    rcn, on, _dn = at1_cli(fxs, chn['l1'], chn['a0b'], chn['mp'], 'R3_NOEPS')
    check('T32.R3_MUST_FAIL_members_file_without_eps_km_s_REFUSED_MEMBERS_and_no_out_dir',
          rcn == 3 and 'MEMBERS' in on.get('reason', '') and 'eps_km_s' in on.get('reason', '') and
          not (RUN / 'AT1_R3_NOEPS').exists(), on.get('reason'))
    check('T32.R3_MUST_PASS_at0b_still_PASS_on_a_members_file_without_eps_km_s', chn['rc'] == [0, 0] and
          json.loads(Path(chn['a0b']).read_text())['outcome'] == 'PASS', {'rc': chn['rc'], 'reasons': chn['reasons']})
    bads = {}
    for tag, kw in (('R3_LEN42', {'eps_len': 42}), ('R3_LEN44', {'eps_len': 44}), ('R3_SCALAR', {'eps_raw': 0.01}),
                    ('R3_OBJECT', {'eps_raw': {'SYN-Q01': 0.01}})):
        chb = chain(fxs, tag, 'linear', **kw)
        rcb, ob, _db = at1_cli(fxs, chb['l1'], chb['a0b'], chb['mp'], tag)
        bads[tag] = {'rc': rcb, 'refused_members': rcb == 3 and 'MEMBERS' in ob.get('reason', ''),
                     'no_out_dir': not (RUN / ('AT1_' + tag)).exists(), 'at0b': chb['rc'][1]}
    check('T32.R3_MUST_FAIL_eps_km_s_of_length_42_(and_44,_a_scalar,_an_object)_REFUSED_MEMBERS_and_no_out_dir',
          all(x['refused_members'] and x['no_out_dir'] and x['at0b'] == 0 for x in bads.values()), bads)
    sel_ids = [m['log_index'] for m in fxs['sel2']['points'] if m['log_index'] != ch['fd']['u_A']['log_index']]
    uAli = ch['fd']['u_A']['log_index']
    spec = {(sel_ids[0], 3): None, (sel_ids[1 % len(sel_ids)], 5): float('nan'), (sel_ids[2 % len(sel_ids)], 9): -1.0,
            (sel_ids[3 % len(sel_ids)], 11): True, (sel_ids[4 % len(sel_ids)], 13): 'x', (uAli, 15): float('inf'),
            (sel_ids[0], 7): None}   # row 7 has no eps_q: FD_NOISE_NOT_BOUNDED whatever eps_m is
    reason_want = {(sel_ids[0], 3): 'MEMBER_EPS_NONE', (sel_ids[1 % len(sel_ids)], 5): 'MEMBER_EPS_NON_FINITE',
                   (sel_ids[2 % len(sel_ids)], 9): 'MEMBER_EPS_NEGATIVE', (sel_ids[3 % len(sel_ids)], 11): 'MEMBER_EPS_BOOL',
                   (sel_ids[4 % len(sel_ids)], 13): 'MEMBER_EPS_NOT_A_NUMBER', (uAli, 15): 'MEMBER_EPS_NON_FINITE'}
    chf = chain(fxs, 'R3_FLAGS', 'quad', eps_none_rows=(7,), eps_fn=lambda li, q: spec.get((li, q), 0.004 + 0.001 * (q % 5)))
    rcf, of, df = at1_cli(fxs, chf['l1'], chf['a0b'], chf['mp'], 'R3_FLAGS')
    rep = df.get('reported') or {}
    fd = chf['fd']
    du = [f['du'] for f in fd['F']]
    uA = np.array(fd['u_A']['u'])
    rows1 = {x['id']: x for x in json.loads(Path(chf['l1']).read_text())['rows']}
    up = upos_of(fxs['run2'])
    flagged = {(x['log_index'], x['id']): x['flag_reason'] for x in rep.get('pairs_member_point_noise_not_bounded') or []}
    want_flag = {(li, QIDS[q]): r for (li, q), r in reason_want.items()}
    bad = []
    for x in rep.get('e_q_per_member_row') or []:
        key = (x['log_index'], x['id'])
        D = np.array(up[x['log_index']]) - uA
        b1 = rows1[x['id']]
        if x['id'] == QIDS[7]:
            if not (x['e_q'] == 'FD_NOISE_NOT_BOUNDED' and x['flag'] == 'FD_NOISE_NOT_BOUNDED' and
                    x['flag_reason'] == 'NO_ROW_EPS_Q' and x['eps_m'] is None):
                bad.append(('row7', key, x))
        elif key in want_flag:
            if not (x['flag'] == 'MEMBER_POINT_NOISE_NOT_BOUNDED' and x['flag_reason'] == want_flag[key] and
                    x['eps_m'] is None and abs(x['e_q'] - r3_eq(0.0, b1['eps_q'], D, du)) <= 1e-12 * max(1.0, x['e_q'])):
                bad.append(('flagged', key, x))
        elif not (x['flag'] is None and x['flag_reason'] is None and isinstance(x['e_q'], float) and
                  abs(x['e_q'] - r3_eq(x['eps_m'], b1['eps_q'], D, du)) <= 1e-12 * max(1.0, x['e_q'])):
            bad.append(('bounded', key, x))
    # the AT-1 inequality recomputed independently from the reported e_q (0 on FD_NOISE_NOT_BOUNDED rows)
    mvals = {p['log_index']: p for p in json.loads(Path(chf['mp']).read_text())['points']}
    L = S['Ls']['seed']
    VN = L['V'][L['N']] if L['N'] else np.zeros((0, 3))
    want_fail = set()
    for x in rep.get('e_q_per_member_row') or []:
        b1 = rows1[x['id']]
        D = np.array(up[x['log_index']]) - uA
        g = mvals[x['log_index']]['speeds_km_s'][QIDS.index(x['id'])]
        sh = float(np.array(b1['K_q']) @ (VN.T @ (VN @ D))) if len(VN) else 0.0
        e = 0.0 if isinstance(x['e_q'], str) else x['e_q']
        if not (b1['lo'] - b1['a_q'] - e + sh <= g <= b1['hi'] + b1['a_q'] + e + sh):
            want_fail.add((x['log_index'], x['id']))
    got_fail = {(x['log_index'], x['id']): (x['flag'], x['flag_reason']) for x in df.get('failing') or []}
    def want_ff(k):
        if k[1] == QIDS[7]:
            return ('FD_NOISE_NOT_BOUNDED', 'NO_ROW_EPS_Q')
        return ('MEMBER_POINT_NOISE_NOT_BOUNDED', want_flag[k]) if k in want_flag else (None, None)
    flag_fail_ok = all(got_fail[k] == want_ff(k) for k in got_fail)
    check('T32.R3_MUST_FAIL_bad_member_eps_entries_None_NaN_-1_True_str_inf_flag_only_that_pair_with_bounded_terms_kept',
          rcf == 0 and chf['rc'] == [0, 0] and flagged == want_flag and not bad and flag_fail_ok,
          {'rc': rcf, 'reason': of.get('reason'), 'flagged': sorted(flagged.items()), 'bad': bad[:3],
           'outcome': df.get('outcome'), 'failing_flags': sorted(set(got_fail.values()), key=str)})
    check('T32.R3_MUST_PASS_row_without_eps_q_reads_FD_NOISE_NOT_BOUNDED_e_q_0_NO_ROW_EPS_Q_whatever_eps_m '
          '(and the AT-1 inequality recomputed independently gives the failing set)',
          rcf == 0 and rep.get('rows_fd_noise_not_bounded') == [QIDS[7]] and
          not [b_ for b_ in bad if b_[0] == 'row7'] and want_fail == set(got_fail) and
          (sel_ids[0], QIDS[7]) not in flagged,
          {'rows_fd_noise_not_bounded': rep.get('rows_fd_noise_not_bounded'), 'n_failing': len(got_fail),
           'independent_failing': len(want_fail), 'symmetric_difference': sorted(want_fail ^ set(got_fail))[:4]})


# ----------------------------------------------------------------------------------------------- T33: custody
def t33_custody(S):
    fx = fx_of(S, 'seed')
    vals = S['vals1']
    seal_p = FIX / 'SYNTHETIC_R3A_SEAL.json'
    args = ['band', '--snapshot', fx['snap'], '--snapshot-sha256', snap_sha(fx['snap']), '--fdplan', fx['fd'],
            '--fdplan-sha256', sha(fx['fd']), '--values', vals, '--values-sha256', sha(vals), '--seal-path', seal_p,
            '--seal-sha256', sha(seal_p), '--out-dir', RUN / 'L1_V002_CUSTODY']
    rcb, ob = cli(V002[0], [str(x) for x in args])
    l1p = RUN / 'L1_V002_CUSTODY' / 'L1_C2V001.json'
    ch = S['r3_seed'][1]
    rc, o, _d = at1_cli(fx, l1p, ch['a0b'], ch['mp'], 'V002_L1_CUSTODY')
    check('T33.MUST_FAIL_at1_on_an_L1_written_by_v002_refused_L1_module_and_no_out_dir',
          rcb == 0 and json.loads(l1p.read_text())['module'] == 'phase1_c2v002' and rc == 3 and
          "L1 module 'phase1_c2v002' is not phase1_c2v003a" in o.get('reason', '') and   # port: v003a
          not (RUN / 'AT1_V002_L1_CUSTODY').exists(), {'band_v002_rc': rcb, 'rc': rc, 'reason': o.get('reason')})


# ----------------------------------------------------------------------------------------------- T34: A135 item 10
def t34_handoff(S):
    c, out = S['seed'], S['seed_snap']
    pp, rp = provenance_fixture(c, out, 'PM')
    _d, rec = rec_of(out)
    members = [m['log_index'] for m in P.v003g_members(c.ctx, rec['run'], 6)['points']]
    fx = RUN / 'PROV_PM'
    lo = fx / 'SHARED_LO_CUSTODY_PIN.json'
    lo.write_text('{"synthetic": true, "shared_custody_pin": "LO (binds no point)"}')

    def rf_with(maps, extra=None, drop_shared=True):
        rf = json.loads(Path(rp).read_text())
        if drop_shared:
            rf.pop('certificate_pins')
        rf[P.CERT_MAPS] = maps
        rf.update(extra or {})
        p = fx / ('ROOT_FIELDS_PM_%d.json' % len(list(fx.glob('ROOT_FIELDS_PM_*.json'))))
        p.write_text(json.dumps(rf, indent=1))
        return p
    good = {str(li): {'eps_certificate': pin(fx / ('CERT_%d.json' % li)), 'lo_certificate': pin(lo),
                      'gq_certificate': 'PENDING_UV_TAIL_CERTIFICATE'} for li in members}
    rc, o, o_ = handoff(c, out, pp, rf_with(good), 'PER_MEMBER')
    ok = rc == 0
    det = {'rc': rc, 'members': o.get('members'), 'reason': o.get('reason')}
    if ok:
        rcpt = json.loads((o_ / 'HANDOFF_RECEIPT_C2V001.json').read_text())
        hs = {h['log_index']: json.loads(Path(h['path']).read_text()) for h in rcpt['handoffs']}
        ok = (sorted(hs) == sorted(members) and all(len(h) == 10 and h['certificate_pins'] == good[str(li)]
                                                   for li, h in hs.items()) and
              rcpt['certificate_map'] == 'ONE_PER_MEMBER (A135 item 10)' and rcpt['launch_authorized'] is False and
              len({json.dumps(h['certificate_pins'], sort_keys=True) for h in hs.values()}) == len(members))
        det.update(n_handoffs=len(hs), receipt_checks=rcpt['checks'][-1])
    check('T34.A135_item_10_MUST_PASS_one_certificate_map_per_member_accepted_each_handoff_carries_its_own_map', ok
          and len(members) >= 2, det)
    a_, b_ = members[0], members[1]
    swap = json.loads(json.dumps(good))
    swap[str(a_)]['eps_certificate'] = pin(fx / ('CERT_%d.json' % b_))
    rc, o, o_ = handoff(c, out, pp, rf_with(swap), 'PM_SWAPPED')
    check('T34.A135_item_10_MUST_FAIL_member_mapped_to_another_members_certificate_refused_CERTIFICATE_MAP',
          rc == 3 and not o_.exists() and 'CERTIFICATE_MAP' in o.get('reason', '') and
          ('member %d' % a_) in o.get('reason', ''), o.get('reason', '')[:240])
    cases = {'missing_member': {k: v for k, v in good.items() if k != str(a_)},
             'extra_key': dict(good, **{'99999': good[str(a_)]}),
             'map_not_an_object': dict(good, **{str(a_): 'PENDING'}),
             'pin_sha_wrong': dict(good, **{str(a_): dict(good[str(a_)], lo_certificate={'path': str(lo),
                                                                                         'sha256': '0' * 64})})}
    res = {}
    for name, maps in cases.items():
        rc, o, o_ = handoff(c, out, pp, rf_with(maps), 'PM_' + name.upper())
        res[name] = {'rc': rc, 'no_out_dir': not o_.exists(), 'reason': o.get('reason', '')[:160]}
    rc, o, o_ = handoff(c, out, pp, rf_with(good, drop_shared=False), 'PM_BOTH_FORMS')
    res['both_shared_and_per_member_keys'] = {'rc': rc, 'no_out_dir': not o_.exists(), 'reason': o.get('reason', '')[:160]}
    check('T34.A135_item_10_MUST_FAIL_map_keys_not_the_member_set_non_object_map_bad_pin_or_both_forms_refused',
          all(x['rc'] == 3 and x['no_out_dir'] for x in res.values()) and
          'CERTIFICATE_MAP' in res['missing_member']['reason'] and 'CERTIFICATE_MAP' in res['extra_key']['reason'] and
          'CERTIFICATE_MAP' in res['map_not_an_object']['reason'] and 'PIN_MISMATCH' in res['pin_sha_wrong']['reason'] and
          'ROOT_FIELDS' in res['both_shared_and_per_member_keys']['reason'], res)


# ----------------------------------------------------------------------------------------------- T35: scope (AST)
def t35_scope(S):
    import ast

    def tops(p):
        out = {}
        for n in ast.parse(Path(p).read_text()).body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                out[n.name] = ast.dump(n)
            elif isinstance(n, ast.Assign):
                for tg in n.targets:
                    for nm in ([tg] if isinstance(tg, ast.Name) else getattr(tg, 'elts', [])):
                        if isinstance(nm, ast.Name):
                            out['=' + nm.id] = ast.dump(n)
            elif isinstance(n, ast.Expr) and isinstance(getattr(n, 'value', None), ast.Constant):
                out['<docstring>'] = ast.dump(n)
        return out
    a, b = tops(V002[0]), tops(TOOL)
    changed = sorted(k for k in a if k in b and a[k] != b[k])
    added = sorted(k for k in b if k not in a)
    removed = sorted(k for k in a if k not in b)
    # port: v003a also changes cmd_at0b against v002 and adds band_region_box_only_extent (A149); T43 checks v003a
    # against v003 node by node
    want_changed = ['<docstring>', '=E_Q_READING', '=MODULE', 'at1_rows', 'cmd_at0b', 'cmd_at1', 'cmd_handoff']
    want_added = ['=CERT_MAPS', '=REGION_CATEGORY', '=REGION_FAMILIES', 'band_region', 'band_region_box_only_extent',
                  'band_region_extent', 'certificate_maps', 'check_member_eps', 'member_eps', 'region_violation']
    check('T35.scope_band_rows_cmd_band_linear_model_AST_identical_to_v002_and_only_the_declared_nodes_changed',
          all(a[k] == b[k] for k in ('band_rows', 'cmd_band', 'linear_model')) and changed == want_changed and
          added == want_added and removed == [],
          {'changed': changed, 'added': added, 'removed': removed})


# ----------------------------------------------------------------------------------------------- T36: S0 and shared map
def t36_identity(S):
    """Port: the reference stays v002 (the shared form is kept for S0 / u_A alone and stays byte-identical to v002)."""
    c = S['corner']
    v2 = {'ref': V002[0], 'suffix': '.V002_SHADOW'}
    (r0, recs0) = shadowed(lambda: tool('fdplan', '--s0-only', '--config', c.cfg, '--config-sha256', c.cfg_sha, '--out-dir',
                                        RUN / 'S0_CORNER_T36'), **v2)
    cs, outs = S['seed'], S['seed_snap']
    pp, rp = provenance_fixture(cs, outs, 'T36')
    (r1, recs1) = shadowed(lambda: handoff(cs, outs, pp, rp, 'T36_SHARED'), **v2)
    (r2, recs2) = shadowed(lambda: band_cli_on(S['seed_snap'], S['seed_fd'], S['vals1'], 'T36'), **v2)
    recs = {'fdplan_s0': recs0, 'handoff_shared_map': recs1, 'band': recs2}
    check('T36.MUST_PASS_S0_path_shared_map_handoff_and_L1_byte_identical_to_v002_except_the_module_field',
          r0[0] == 0 and r1[0] == 0 and r2[0] == 0 and
          all(len(v) == 1 and not v[0]['diffs'] and v[0]['subst'] == ['module'] and v[0]['rc'] == [0, 0]
              for v in recs.values()),
          {k: [(x['rc'], x['subst'], x['diffs']) for x in v] for k, v in recs.items()})


# ----------------------------------------------------------------------------------------------- part 4: A149
def t37_members_custody(S):
    """A149 item 2: at0b records members_sha256; at1 refuses MEMBERS (no out-dir) unless its --members sha equals it."""
    fx = fx_of(S, 'seed')
    rec = {'AT0B_OK': FIX / 'MEMBERS_LINEAR.json', 'AT0B_NOREBIND': FIX / 'MEMBERS_NOREBIND.json',
           'AT0B_C1': FIX / 'MEMBERS_C1.json', 'AT0B_Q1': FIX / 'MEMBERS_Q1.json',
           'AT0B_CORNER': S['corner_phase2']['members']}
    got = {k: json.loads((RUN / k / 'AT0B_C2V001.json').read_text()) for k in rec}
    check('T37.A149_2_MUST_PASS_at0b_records_members_sha256_equal_to_the_sha_of_the_members_bytes_it_read',
          all(got[k].get('members_sha256') == sha(m) and got[k]['module'] == 'phase1_c2v003a' for k, m in rec.items()),
          {k: [got[k].get('outcome'), (got[k].get('members_sha256') or '')[:16], sha(m)[:16]] for k, m in rec.items()})
    # (b) v003's T23 combination: the AT-0b defect file (NOREBIND) with another members file (C1)
    l1c1 = RUN / 'L1_C1' / 'L1_C2V001.json'
    a0b_bad = RUN / 'AT0B_NOREBIND' / 'AT0B_C2V001.json'
    rc, o, _d = at1_cli(fx, l1c1, a0b_bad, FIX / 'MEMBERS_C1.json', 'A149_DEFECT_AT0B_OTHER_MEMBERS')
    rcv, ov, _dv = at1_cli(fx, RUN / 'L1_C1.V003_SHADOW' / 'L1_C2V001.json', a0b_bad, FIX / 'MEMBERS_C1.json',
                           'A149_DEFECT_AT0B_OTHER_MEMBERS_V003', path=V003[0])
    check('T37.A149_2_MUST_FAIL_at1_members_file_other_than_the_one_AT0b_read_REFUSED_MEMBERS_no_out_dir (v003 T23 form)',
          rc == 3 and 'MEMBERS' in o.get('reason', '') and 'members_sha256' in o.get('reason', '') and
          'A149 item 2' in o.get('reason', '') and not (RUN / 'AT1_A149_DEFECT_AT0B_OTHER_MEMBERS').exists(),
          {'rc': rc, 'reason': o.get('reason'), 'v003_on_the_same_inputs': [rcv, ov.get('outcome'), ov.get('reason')]})
    # (c) the adversarial verifier's case: the Q1 members file with only the u_A member's result_pin changed
    mq = json.loads((FIX / 'MEMBERS_Q1.json').read_text())
    rf = FIX / 'A149_OTHER_UA_RESULT.json'
    rf.write_text('{"synthetic_toy_result": true, "note": "not the Phase-1 u_A result"}')
    uAli = json.loads(Path(S['seed_fd']).read_text())['u_A']['log_index']
    for p in mq['points']:
        if p['log_index'] == uAli:
            p['result_pin'] = pin(rf)
    mp2 = FIX / 'MEMBERS_Q1_UA_RESULT_PIN_CHANGED.json'
    mp2.write_text(json.dumps(mq, indent=1))
    a0bq = RUN / 'AT0B_Q1' / 'AT0B_C2V001.json'
    rc, o, _d = at1_cli(fx, RUN / 'L1_Q1' / 'L1_C2V001.json', a0bq, mp2, 'A149_UA_RESULT_PIN_CHANGED')
    rcv, ov, _dv = at1_cli(fx, RUN / 'L1_Q1.V003_SHADOW' / 'L1_C2V001.json', a0bq, mp2,
                           'A149_UA_RESULT_PIN_CHANGED_V003', path=V003[0])
    check('T37.A149_2_MUST_FAIL_at1_members_file_with_the_u_A_result_pin_changed_after_AT0b_REFUSED_no_out_dir',
          rc == 3 and 'members_sha256' in o.get('reason', '') and not (RUN / 'AT1_A149_UA_RESULT_PIN_CHANGED').exists(),
          {'rc': rc, 'reason': o.get('reason'), 'v003_on_the_same_inputs': [rcv, ov.get('outcome')]})
    # (d) an AT-0b file without members_sha256 (written by v003)
    a0b3 = RUN / 'AT0B_C1.V003_SHADOW' / 'AT0B_C2V001.json'
    rc, o, _d = at1_cli(fx, l1c1, a0b3, FIX / 'MEMBERS_C1.json', 'A149_V003_AT0B')
    check('T37.A149_2_MUST_FAIL_at1_with_an_AT0b_that_records_no_members_sha256_(v003-written)_REFUSED_no_out_dir',
          'members_sha256' not in json.loads(a0b3.read_text()) and rc == 3 and 'members_sha256' in o.get('reason', '')
          and "recorded by AT-0b" in o.get('reason', '') and not (RUN / 'AT1_A149_V003_AT0B').exists(),
          {'rc': rc, 'reason': o.get('reason')})


def exact_L(uA=(0.0, 0.4, 0.6)):
    """SYNTHETIC exact-geometry linear model in linear_model's layout: V = I (V_I = e_0, m_id = 1), S has only column 0
    (entries +-1, +-2, +-0.5) and DDO row 0 has zero slack (q_A,0 = zrow_0: b_band row 0 = 0.0).  For a member
    u = u_A + t e_0 with u_A,0 = 0.0: Delta = (t, 0, 0), c = t and DDO row 0's violation (A c)_0 - max(b_0, 0) = t, all
    exact in floating point; every other row has slack >= 0.25 - t."""
    import numpy as np
    S_ = np.zeros((6, 3))
    S_[:, 0] = [1.0, -1.0, 2.0, -2.0, 0.5, -0.5]
    V = np.eye(3)
    qA = np.zeros(6)
    qA[0] = 5.0
    return {'uA': np.array(uA, dtype=float), 'qA': qA, 'zrow': np.full(6, 5.0), 'S': S_, 'V': V, 'I': [0], 'N': [1, 2],
            'VI': V[[0]], 'fA': 100.0 + np.arange(6, dtype=float), 'sig': np.ones(6), 'J': S_.copy(),
            'P': {'max_repair_step': 0.25, 'hull_growth_tol': 0.02, 'march_step': 0.05},
            'rows': ['SYN_X%02d' % i for i in range(6)]}


def t38_region_tolerance(S):
    """A149 item 4: the region test is (A c)_i - max(b_i, 0) > E._LP_EPS, exactly: violations 5e-13 and 1e-12 read [],
    1e-12 + one ulp and 1e-10 read LINEAR_DDO (kills tolerance 1e-9, tolerance 1e-13 and '>=')."""
    import numpy as np
    Lx = exact_L()
    ts = {1001: 5e-13, 1002: 1e-12, 1003: float(np.nextafter(1e-12, np.inf)), 1004: 1e-10, 1005: 2e-12}
    want = {1001: [], 1002: [], 1003: ['LINEAR_DDO'], 1004: ['LINEAR_DDO'], 1005: ['LINEAR_DDO']}
    mem = [(li, [t, 0.4, 0.6]) for li, t in ts.items()]
    l1x, _m = l1_of(Lx, synth_F(Lx, (0.05, 0.05, 0.05)), lin_g)
    fx_, _r = P.at1_rows(E, Lx, l1x, run2_of(Lx, mem), mv_of(mem, bumped(lin_g)), QIDS)
    reg = P.band_region(Lx)
    res, ok = {}, len(fx_) == 43 * len(mem)
    for li, t in ts.items():
        c = Lx['VI'] @ (np.array(dict(mem)[li]) - Lx['uA'])
        viol, mx = P.region_violation(E, reg, c)
        ind = indep_region(Lx, c)
        cats = sorted(set(x['category'] for x in fx_ if x['log_index'] == li))
        lists = sorted(set(tuple(x['region_rows_violated']) for x in fx_ if x['log_index'] == li))
        res[li] = {'t': t.hex(), 'c_equals_t': float(c[0]) == t, 'LINEAR_DDO_violation': mx['LINEAR_DDO'],
                   'violation_equals_t_exactly': mx['LINEAR_DDO'] == t, 'region': viol, 'independent': ind[0],
                   'categories': cats, 'lists': [list(x) for x in lists]}
        ok = ok and float(c[0]) == t and mx['LINEAR_DDO'] == t and viol == want[li] and ind[0] == want[li] and \
            lists == [tuple(want[li])] and cats == ([CAT[want[li][0]]] if want[li] else ['NGC_NONLINEAR'])
    check('T38.A149_4_MUST_FAIL_region_tolerance_is_exactly_E._LP_EPS_with_a_strict_> (violations 5e-13 and 1e-12 '
          'read [], 1e-12+ulp, 2e-12 and 1e-10 read LINEAR_DDO)', ok and E._LP_EPS == 1e-12, res)


def t39_contract_member_valid_false(S):
    """A149 item 4: the A144 R3 contract covers every member point of the file, member_valid false included (kills the
    member_valid-true-only contract); a member_valid false point with a full list is accepted (control)."""
    fxs = fx_of(S, 'seed')
    fd = json.loads(Path(fxs['fd']).read_text())
    ch = chain(fxs, 'MVF', 'linear')
    base = json.loads(Path(ch['mp']).read_text())
    li_x = [p['log_index'] for p in base['points'] if p['log_index'] != fd['u_A']['log_index']][0]
    res = {}
    for tag, mut in (('MVF_NOEPS', lambda p: p.pop('eps_km_s')), ('MVF_LEN42', lambda p: p.update(eps_km_s=[0.01] * 42)),
                     ('MVF_CONTROL', lambda p: None)):
        doc = json.loads(json.dumps(base))
        for p in doc['points']:
            if p['log_index'] == li_x:
                p['member_valid'] = False
                mut(p)
        mp = FIX / ('MEMBERS_%s.json' % tag)
        mp.write_text(json.dumps(doc, indent=1))
        rc0, o0, a0b = at0b_cli(fxs, ch['vals'], mp, tag)
        rc, o, d = at1_cli(fxs, ch['l1'], a0b, mp, tag)
        res[tag] = {'at0b': [rc0, json.loads(a0b.read_text()).get('outcome') if a0b.exists() else None], 'rc': rc,
                    'reason': o.get('reason'), 'out_dir': (RUN / ('AT1_' + tag)).exists(), 'outcome': d.get('outcome')}
    ok = all(res[t]['at0b'] == [0, 'PASS'] and res[t]['rc'] == 3 and 'eps_km_s' in (res[t]['reason'] or '') and
             ('[%d]' % li_x) in (res[t]['reason'] or '') and not res[t]['out_dir'] for t in ('MVF_NOEPS', 'MVF_LEN42'))
    check('T39.A149_4_MUST_FAIL_member_valid_false_point_without_a_43_entry_eps_km_s_REFUSED_MEMBERS_no_out_dir '
          '(control: with the list it is accepted)',
          ok and res['MVF_CONTROL']['rc'] == 0 and res['MVF_CONTROL']['out_dir'], dict(res, member=li_x))


def t40_scope_by_theta_key(S):
    """A149 item 4: a per-member map pin that names another admitted point by its theta key alone is refused (kills the
    spec-sha-only scope check); by its spec sha alone, refused; naming only its own member's key, accepted (control)."""
    c, out = S['seed'], S['seed_snap']
    pp, rp = provenance_fixture(c, out, 'PM_KEY')
    _d, rec = rec_of(out)
    members = [m['log_index'] for m in P.v003g_members(c.ctx, rec['run'], 6)['points']]
    keys = {p['log_index']: O.theta_key(p['theta_natural']) for p in rec['run']['exploration']['admitted_points']}
    cp = campaign_of(c)
    specs = {li: cp.orch.cache.entries[k]['provenance']['spec_sha256'] for li, k in keys.items()}
    fx = RUN / 'PROV_PM_KEY'
    a_, b_ = members[0], members[1]
    files = {'key_only_other': {'synthetic': True, 'point_theta_key': keys[b_]},
             'spec_only_other': {'synthetic': True, 'point_spec_sha256': specs[b_]},
             'key_only_own': {'synthetic': True, 'point_theta_key': keys[a_]}}
    res = {}
    for name, body in files.items():
        cf = fx / ('CERT_%s.json' % name.upper())
        cf.write_text(json.dumps(body))
        raw = cf.read_bytes()
        maps = {str(li): {'eps_certificate': pin(fx / ('CERT_%d.json' % li)), 'gq_certificate': 'PENDING'}
                for li in members}
        maps[str(a_)]['eps_certificate'] = pin(cf)
        rf = json.loads(Path(rp).read_text())
        rf.pop('certificate_pins')
        rf[P.CERT_MAPS] = maps
        rfp = fx / ('ROOT_FIELDS_%s.json' % name.upper())
        rfp.write_text(json.dumps(rf, indent=1))
        rc, o, o_ = handoff(c, out, pp, rfp, 'PM_' + name.upper())
        res[name] = {'rc': rc, 'out_dir': o_.exists(), 'reason': o.get('reason', '')[:240],
                     'names_other_key': keys[b_].encode() in raw, 'names_any_spec_sha': any(s.encode() in raw
                                                                                        for s in specs.values() if s)}
    ko, so, own = res['key_only_other'], res['spec_only_other'], res['key_only_own']
    check('T40.A149_4_MUST_FAIL_map_pin_naming_another_member_by_theta_key_alone_refused_CERTIFICATE_MAP (and by spec '
          'sha alone; own key alone accepted)',
          ko['names_other_key'] and not ko['names_any_spec_sha'] and ko['rc'] == 3 and not ko['out_dir'] and
          'CERTIFICATE_MAP' in ko['reason'] and ('member %d' % a_) in ko['reason'] and str(b_) in ko['reason'] and
          so['rc'] == 3 and not so['out_dir'] and 'CERTIFICATE_MAP' in so['reason'] and
          own['rc'] == 0 and own['out_dir'], dict(res, member=a_, other=b_))


def tie_L(tiny):
    """The adversarial verifier's A5 construction (p1v003_verify_adv probes, inproc A5): u_A = (1, 0, 0.5), V_I ~ (1, 1,
    0)/sqrt2, so the box rows alone pin c = 0 exactly; the DDO row with the largest |S V_I^T| gets b_band = tiny."""
    import numpy as np
    V = np.array([[1.0, 1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 0.0, 1.0]]) / np.array([[math.sqrt(2)], [math.sqrt(2)], [1.0]])
    L = synth_L((1.0, 0.0, 0.5), V, (3.0, 0.0, 0.0), n_ddo=8, ddo_half=6.0, seed=7)
    s0 = (L['S'] @ L['VI'].T)[:, 0]
    i0 = int(np.argmax(np.abs(s0)))
    L['qA'][i0] = (L['zrow'][i0] - tiny) if s0[i0] > 0 else -(L['zrow'][i0] - tiny)
    return L


def t41_box_only_extent(S):
    """A149 item 3: band_region_box_only_extent, print only."""
    import numpy as np

    def ok_box(ext, want):
        return len(ext) == len(want) and all(e['lp_status'] == ['OPTIMAL', 'OPTIMAL'] and
                                             abs(e['extent'][0] - w[0]) <= 1e-12 and abs(e['extent'][1] - w[1]) <= 1e-12
                                             for e, w in zip(ext, want))
    docs = {'corner_T27': (RUN / 'AT1_CORNER', 'corner'), 'seed_Q1': (RUN / 'AT1_Q1', 'seed'),
            'cm2': (RUN / 'AT1_CM2', 'cm2'), 'seed_R3': (RUN / 'AT1_R3_SEED', 'seed')}
    res, ok = {}, True
    for name, (d, lk) in docs.items():
        rep = json.loads((d / 'AT1_C2V001.json').read_text())['reported']
        L = S['Ls'][lk]
        A, b, fam = P.band_region(L)
        ind = indep_extent(A[fam['BOX']], b[fam['BOX']])
        box, full = rep.get('band_region_box_only_extent') or [], rep['band_region_extent']
        contains = all(bx['extent'][0] <= fl['extent'][0] + 1e-12 and fl['extent'][1] <= bx['extent'][1] + 1e-12
                       for bx, fl in zip(box, full))
        res[name] = {'box_only': [x['extent'] for x in box], 'independent_box_only': ind, 'full': [x['extent'] for x in full],
                     'single_point': rep['band_region_single_point'], 'reason': rep['band_region_single_point_reason'],
                     'directions': [x['direction'] for x in box] == L['I'], 'box_contains_full': contains}
        ok = ok and ok_box(box, ind) and res[name]['directions'] and contains
    ok = ok and res['corner_T27']['box_only'] == [[0.0, 0.0]] and res['corner_T27']['single_point'] is True and \
        res['corner_T27']['reason'] == 'BOX_CORNER' and res['seed_Q1']['box_only'] != res['seed_Q1']['full']
    check('T41.A149_3_MUST_PASS_at1_prints_band_region_box_only_extent_equal_to_an_independent_box_only_computation '
          '(corner [0.0,0.0], interior, CM2; it contains the full-region extent)', ok, res)
    # (b) the exact-corner LP-tie case: the full-region extent is a few ulps off 0.0, the box-only extent is [0.0, 0.0]
    res, tie = {}, []
    for tiny in (0.0, 1e-14, 1e-13, 5e-13, 1e-12):
        L = tie_L(tiny)
        ext, sp, why = P.band_region_extent(E, L)
        box = P.band_region_box_only_extent(E, L)
        res[repr(tiny)] = {'full': ext[0]['extent'], 'full_status': ext[0]['lp_status'], 'single_point': sp,
                           'reason': why, 'box_only': box[0]['extent'], 'box_status': box[0]['lp_status']}
        if ext[0]['extent'] != [0.0, 0.0]:
            tie.append(repr(tiny))
    ok = all(x['box_only'] == [0.0, 0.0] and x['box_status'] == ['OPTIMAL', 'OPTIMAL'] for x in res.values()) and \
        res['0.0']['single_point'] is True and res['0.0']['reason'] == 'BOX_CORNER' and len(tie) >= 1 and \
        all(res[t]['single_point'] is False and res[t]['reason'] is None and
            0.0 <= min(res[t]['full']) and max(res[t]['full']) < 1e-12 for t in tie)
    L = tie_L(float(tie[0])) if tie else tie_L(1e-14)
    mem = [(1101, [float(x) for x in L['uA']])]
    _f, rr = P.at1_rows(E, L, l1_of(L, synth_F(L, (-0.05, 0.05, 0.05)), lin_g)[0], run2_of(L, mem),
                        mv_of(mem, lin_g), QIDS)
    ok = ok and rr['band_region_box_only_extent'][0]['extent'] == [0.0, 0.0] and rr['band_region_single_point'] is False
    check('T41.A149_3_MUST_PASS_exact_corner_LP_tie_full_region_extent_off_0.0_by_ulps_single_point_stays_exact_false_'
          'and_box_only_extent_is_[0.0,0.0]', ok, dict(res, tie_cases=tie,
                                                       at1_rows_box_only=rr['band_region_box_only_extent'],
                                                       at1_rows_single_point=rr['band_region_single_point']))
    # (c) non-OPTIMAL programs: box-only prints NOT_AVAILABLE with the statuses, and changes no row
    def lp_fault(A_, b_, w_):
        c_, _st = E._lp_max(A_, b_, w_)
        return c_, 'ITERATION_LIMIT'
    L = S['Ls']['corner']
    ph = S['corner_phase2']
    l1 = dict(json.loads(Path(ph['l1']).read_text()), fd_du=[f['du'] for f in S['Fs']['corner']])
    mv = {p['log_index']: p for p in json.loads(Path(ph['members']).read_text())['points']}
    f_ok, r_ok = P.at1_rows(E, L, l1, ph['run2'], mv, QIDS)
    f_bad, r_bad = P.at1_rows(E, L, l1, ph['run2'], mv, QIDS, lp=lp_fault)
    same = json.dumps(f_ok) == json.dumps(f_bad) and all(json.dumps(r_ok[k]) == json.dumps(r_bad[k]) for k in r_ok
                                                         if not k.startswith('band_region'))
    check('T41.A149_3_MUST_FAIL_non_OPTIMAL_box_only_program_prints_NOT_AVAILABLE_with_its_status_and_changes_no_row',
          same and all(e['extent'] == ['NOT_AVAILABLE', 'NOT_AVAILABLE'] and
                       e['lp_status'] == ['ITERATION_LIMIT', 'ITERATION_LIMIT'] for e in r_bad['band_region_box_only_extent'])
          and r_ok['band_region_box_only_extent'][0]['extent'] == [0.0, 0.0],
          {'fault': r_bad['band_region_box_only_extent'], 'ok': r_ok['band_region_box_only_extent'],
           'rows_and_failing_unchanged': same})
    # (d) the reason and the printed box-only extent agree wherever the band region is a single point
    Lo = synth_L((0.5, 0.5, 0.5), rand_orth(21), (3.0, 0.0, 0.0), seed=9)
    svi = (Lo['S'] @ Lo['VI'].T)[:, 0]
    sgn = 1.0 if np.sum(svi > 0) >= 2 else -1.0
    i, j = [k for k in range(len(svi)) if sgn * svi[k] > 0][:2]
    Lo['qA'][i], Lo['qA'][j] = Lo['zrow'][i], -Lo['zrow'][j]   # T31's OTHER_ROWS fixture
    cases = dict(S['Ls'], other_rows=Lo, tie_0=tie_L(0.0), **{'tie_%s' % t: tie_L(float(t)) for t in tie})
    res, ok = {}, True
    for name, L in cases.items():
        _e, sp, why = P.band_region_extent(E, L)
        box = P.band_region_box_only_extent(E, L)
        zero = all(x['lp_status'] == ['OPTIMAL', 'OPTIMAL'] and x['extent'] == [0.0, 0.0] for x in box)
        res[name] = {'single_point': sp, 'reason': why, 'box_only_zero': zero}
        if sp is True:
            ok = ok and (why == 'BOX_CORNER') == zero
        else:
            ok = ok and why is None
    check('T41.A149_3_MUST_PASS_single_point_reason_BOX_CORNER_iff_the_printed_box_only_extents_are_OPTIMAL_[0.0,0.0]',
          ok and res['corner']['single_point'] is True and res['other_rows']['reason'] == 'OTHER_ROWS', res)


def t42_overflow(S):
    """A149 item 1: an int entry beyond the float range is flagged MEMBER_EPS_NON_FINITE for that pair only; v003 refused
    the whole at1 (INTERNAL_ERROR OverflowError) -- the declared overflow difference, shadowed against v003."""
    def me(v):
        try:
            return P.member_eps([v], 0)
        except Exception as exc:   # noqa: BLE001 -- recorded, so the CLI checks below still run
            return ('RAISED', type(exc).__name__)
    unit = {'10**400': me(10 ** 400), '-10**400': me(-(10 ** 400)), '2**1024': me(2 ** 1024), '2**1023': me(2 ** 1023),
            '10**300': me(10 ** 300)}
    check('T42.A149_1_MUST_FAIL_member_eps_int_beyond_the_float_range_is_NON_FINITE_never_an_exception (in process)',
          unit['10**400'] == (None, 'MEMBER_EPS_NON_FINITE') and unit['-10**400'] == (None, 'MEMBER_EPS_NON_FINITE') and
          unit['2**1024'] == (None, 'MEMBER_EPS_NON_FINITE') and unit['2**1023'] == (float(2 ** 1023), None) and
          unit['10**300'] == (1e300, None), {k: list(v) for k, v in unit.items()})
    fxs = fx_of(S, 'seed')
    fd = json.loads(Path(fxs['fd']).read_text())
    li_x = [m['log_index'] for m in fxs['sel2']['points'] if m['log_index'] != fd['u_A']['log_index']][0]
    out = {}
    for tag, val in (('A149_OVERFLOW', 10 ** 400), ('A149_INF', float('inf'))):
        def run(tag=tag, val=val):
            ch = chain(fxs, tag, 'quad', eps_fn=lambda li, q: val if (li, q) == (li_x, 9) else 0.004 + 0.001 * (q % 5))
            rc, o, d = at1_cli(fxs, ch['l1'], ch['a0b'], ch['mp'], tag)
            return ch, rc, o, d
        (ch, rc, o, d), recs = shadowed(run, ref=V003[0], suffix='.V003_SHADOW')
        out[tag] = {'ch': ch, 'rc': rc, 'o': o, 'd': d, 'recs': recs}
    ov = out['A149_OVERFLOW']
    rep = ov['d'].get('reported') or {}
    raw_ok = ('%d' % 10 ** 400).encode() in Path(ov['ch']['mp']).read_bytes()
    recs = {r['cmd']: r for r in ov['recs']}
    a1 = recs.get('agree at1') or {}
    v3_reason = ''
    for d_ in a1.get('diffs') or []:
        v3_reason += d_
    check('T42.A149_1_MUST_FAIL_10**400_entry_flags_one_pair_MEMBER_EPS_NON_FINITE_and_at1_completes (CLI)',
          raw_ok and ov['ch']['rc'] == [0, 0] and ov['rc'] == 0 and
          rep.get('pairs_member_point_noise_not_bounded') == [{'log_index': li_x, 'id': QIDS[9],
                                                               'flag_reason': 'MEMBER_EPS_NON_FINITE'}] and
          [x for x in rep.get('e_q_per_member_row') or [] if x['flag'] == 'MEMBER_POINT_NOISE_NOT_BOUNDED'] ==
          [x for x in rep.get('e_q_per_member_row') or [] if (x['log_index'], x['id']) == (li_x, QIDS[9])],
          {'rc': ov['rc'], 'reason': ov['o'].get('reason'), 'outcome': ov['d'].get('outcome'),
           'flagged': rep.get('pairs_member_point_noise_not_bounded'), 'members_file_holds_the_401_digit_int': raw_ok})
    # the shadow: band and at0b differ from v003 only in the declared fields; at1 differs only by the overflow case
    v3 = a1.get('rc') == [3, 0] and a1.get('out', '').endswith('AT1_A149_OVERFLOW') and \
        not os.path.exists(str(RUN / 'AT1_A149_OVERFLOW') + '.V003_SHADOW') and \
        all(d_.startswith(('exit code 3 != 0', 'stdout ', 'files [] != ')) for d_ in a1.get('diffs') or []) and \
        'OverflowError' in v3_reason and a1.get('l1_substituted')
    band_ok = not recs['band']['diffs'] and recs['band']['subst'] == ['module']
    at0b_ok = not recs['agree at0b']['diffs'] and recs['agree at0b']['subst'] == sorted(['module', AT0B_DECLARED])
    inf_ = out['A149_INF']
    same = (RUN / 'AT1_A149_OVERFLOW' / 'AT1_C2V001.json').read_bytes() == \
        (RUN / 'AT1_A149_INF' / 'AT1_C2V001.json').read_bytes() if ov['rc'] == 0 and inf_['rc'] == 0 else False
    i1 = {r['cmd']: r for r in inf_['recs']}.get('agree at1') or {}
    check('T42.A149_1_shadow_v003_declared_overflow_difference_only (v003 refuses INTERNAL_ERROR OverflowError, no '
          'out-dir; band and at0b declared fields only; v003a reads 10**400 byte-identically to an inf entry)',
          v3 and band_ok and at0b_ok and same and not i1.get('diffs') and AT1_DECLARED in (i1.get('subst') or []),
          {'at1_shadow': [a1.get('rc'), [d_[:200] for d_ in a1.get('diffs') or []]], 'band': recs['band']['subst'],
           'at0b': recs['agree at0b']['subst'], 'overflow_equals_inf_bytes': same,
           'inf_shadow': [i1.get('rc'), i1.get('diffs'), i1.get('subst')]})


def t43_v003_and_scope(S):
    """v003 untouched; at1 custody accepts only a v003a-written L1; the AST scope against v003."""
    import ast
    check('T43.v003_tool_tests_mutation_README_and_HASHES_untouched (sha256 from bytes)',
          sha(V003[0]) == V003[1] and all(sha(p) == h for p, h in V003_FILES),
          {os.path.basename(str(p)): sha(p)[:16] for p, _h in ((V003[0], None),) + V003_FILES})
    fx = fx_of(S, 'seed')
    l13 = RUN / 'L1_C1.V003_SHADOW' / 'L1_C2V001.json'
    rc, o, _d = at1_cli(fx, l13, RUN / 'AT0B_C1' / 'AT0B_C2V001.json', FIX / 'MEMBERS_C1.json', 'A149_V003_L1')
    check('T43.MUST_FAIL_at1_on_an_L1_written_by_v003_refused_L1_module_and_no_out_dir',
          json.loads(l13.read_text())['module'] == 'phase1_c2v003' and rc == 3 and
          "L1 module 'phase1_c2v003' is not phase1_c2v003a" in o.get('reason', '') and
          not (RUN / 'AT1_A149_V003_L1').exists(), {'rc': rc, 'reason': o.get('reason')})

    def tops(p):
        out = {}
        for n in ast.parse(Path(p).read_text()).body:
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                out[n.name] = ast.dump(n)
            elif isinstance(n, ast.Assign):
                for tg in n.targets:
                    for nm in ([tg] if isinstance(tg, ast.Name) else getattr(tg, 'elts', [])):
                        if isinstance(nm, ast.Name):
                            out['=' + nm.id] = ast.dump(n)
            elif isinstance(n, ast.Expr) and isinstance(getattr(n, 'value', None), ast.Constant):
                out['<docstring>'] = ast.dump(n)
        return out
    a, b = tops(V003[0]), tops(TOOL)
    changed = sorted(k for k in a if k in b and a[k] != b[k])
    added = sorted(k for k in b if k not in a)
    removed = sorted(k for k in a if k not in b)
    keep = ('band_rows', 'cmd_band', 'linear_model', 'band_region', 'band_region_extent', 'region_violation',
            'check_member_eps', 'certificate_maps', 'cmd_handoff', 'members_values', '=E_Q_READING')
    check('T43.scope_against_v003_only_MODULE_member_eps_cmd_at0b_at1_rows_cmd_at1_changed_and_box_only_helper_added '
          '(band_rows, cmd_band, linear_model and the A144 helpers AST-identical)',
          changed == ['<docstring>', '=MODULE', 'at1_rows', 'cmd_at0b', 'cmd_at1', 'member_eps'] and
          added == ['band_region_box_only_extent'] and removed == [] and all(a[k] == b[k] for k in keep),
          {'changed': changed, 'added': added, 'removed': removed})


def main():
    RUN.mkdir(parents=True)
    FIX.mkdir()
    sys.addaudithook(_audit)
    S = {}
    # part 1: the v002-era tests, ported; every CLI call is shadow-run with v003 (R01)
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
    guard('T27', lambda: t27_corner(S))   # v002's A137 L5 and N-B checks, under the v003 shadow
    guard('T28', lambda: t28_corner_must_fail(S))
    guard('T29', lambda: t29_nb(S))
    n_ported = len(RESULTS)
    # part 2: regression against v003
    SHADOW['on'] = False
    with open(RUN / 'SHADOW_REGRESSION_V003_V003A.json', 'x') as fh:
        json.dump(SHADOW['log'], fh, indent=1, default=str)
    guard('R01', lambda: r01_regression(S))
    n_r01 = len(RESULTS) - n_ported
    # part 3: A144 R1, R2, R3, the L1 custody, A135 item 10, scope, S0 / shared-map identity
    guard('T30F', lambda: t30_fixtures(S))
    guard('T30', lambda: t30_r1(S))
    guard('T31', lambda: t31_r2(S))
    guard('T32', lambda: t32_r3(S))
    guard('T33', lambda: t33_custody(S))
    guard('T34', lambda: t34_handoff(S))
    guard('T35', lambda: t35_scope(S))
    guard('T36', lambda: t36_identity(S))
    n_p3 = len(RESULTS) - n_ported - n_r01
    # part 4: A149 items 1-4 (new)
    guard('T37', lambda: t37_members_custody(S))
    guard('T38', lambda: t38_region_tolerance(S))
    guard('T39', lambda: t39_contract_member_valid_false(S))
    guard('T40', lambda: t40_scope_by_theta_key(S))
    guard('T41', lambda: t41_box_only_extent(S))
    guard('T42', lambda: t42_overflow(S))
    guard('T43', lambda: t43_v003_and_scope(S))
    n_pass = sum(1 for r in RESULTS if r['pass'])
    summary = {'run_dir': str(RUN), 'n': len(RESULTS), 'pass': n_pass, 'fail': len(RESULTS) - n_pass,
               'n_ported_part1': n_ported, 'n_regression_part2': n_r01, 'n_ported_part3': n_p3,
               'n_ported_total': n_ported + n_r01 + n_p3, 'n_new_part4_A149': len(RESULTS) - n_ported - n_r01 - n_p3,
               'shadow_cli_calls': len(SHADOW['log']),
               'must_fail': sum(1 for r in RESULTS if 'MUST_FAIL' in r['id']),
               'must_fail_pass': sum(1 for r in RESULTS if 'MUST_FAIL' in r['id'] and r['pass']),
               'must_pass': sum(1 for r in RESULTS if 'MUST_FAIL' not in r['id']),
               'must_pass_pass': sum(1 for r in RESULTS if 'MUST_FAIL' not in r['id'] and r['pass']),
               'audit_denied': AUDIT['denied'], 'tool_sha256': sha(TOOL), 'test_sha256': sha(__file__),
               'v001_sha256': sha(V001[0]), 'v002_sha256': sha(V002[0]), 'v003_sha256': sha(V003[0])}
    with open(RUN / 'RESULTS.json', 'x') as fh:
        json.dump({'summary': summary, 'results': RESULTS}, fh, indent=1, default=str)
    print(json.dumps(summary, indent=1))
    return 0 if summary['fail'] == 0 and not AUDIT['denied'] else 1


if __name__ == '__main__':
    sys.exit(main())
