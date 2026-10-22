"""phase1_c2v003a -- the A133 Phase-1 tool (UNT Galaxy Run 120/43; Claude2 root-workflow build), successor of
phase1_c2v003 (149ed4cb) under ruling A149 items 1-4 (V006 addendum), which close the gaps both root verifiers found in
v003.  Changes against v003, and only these:
  A149.1  member_eps catches OverflowError (an int entry beyond the float range, e.g. 10**400): that pair is flagged
          MEMBER_EPS_NON_FINITE (MEMBER_POINT_NOISE_NOT_BOUNDED, bounded terms kept) instead of refusing the whole at1.
  A149.2  at0b records members_sha256 (the sha of the --members bytes it read); at1 refuses MEMBERS (no out-dir) unless
          its --members sha equals that recorded value.  This closes a gap present since v001.
  A149.3  at1 also prints band_region_box_only_extent: per identified c_j, [min, max] over the band region's BOX rows
          alone (E._lp_max, with both statuses), print only.  band_region_single_point stays exact (no new tolerance)
          and band_region_extent, its reason and every row are unchanged.
  CUSTODY at1 accepts only an L1 whose module is this MODULE ('phase1_c2v003a').
  (A149.4, the tests that kill v003's 5 surviving mutants, is in test_phase1_c2v003a.py.)

v003 header (unchanged behaviour; 'v003' below reads as this module):
phase1_c2v003 -- successor of phase1_c2v002 (d64351ec) under ruling A144 (V006 addendum; Claude3 0204 N1, N2 and N6;
erratum E_A133_2) and A135 item 10.  Changes against v002, and only these:
  R1   (E_A133_2(a), label only) AT-1 category: one helper, band_region, builds the band region's rows (A, b_band and
       the family slices TRUST_RADIUS, BOX, LINEAR_DDO) exactly as band_rows does.  Row i is violated iff
       (A c)_i - max(b_band_i, 0) > E._LP_EPS (the clip and the tolerance are the pinned engine's own, L1787 / L181),
       c = V_I Delta_m.  A failing (member, row) prints region_rows_violated (in the order TRUST_RADIUS, BOX,
       LINEAR_DDO; [] if none), region_max_violation per family, the category (the first violated family mapped to
       OUTSIDE_TRUST_RADIUS, OUTSIDE_BOX_SLICE or OUTSIDE_LINEAR_DDO_REGION; NGC_NONLINEAR only for []), and
       geometric_part and residual_part with excess = geometric_part + residual_part.  The AT-1 inequality, the failing
       set, the excess, norm_n and the outcome are not touched by R1.
  R2   at1 prints band_region_extent ([min, max] of each identified c_j over the band region's own rows, by
       E._lp_max, with both statuses), band_region_single_point (true iff every extent is OPTIMAL and exactly
       [0.0, 0.0]; NOT_AVAILABLE if any program is not OPTIMAL; never refuses, never changes a row) and
       band_region_single_point_reason (BOX_CORNER iff the box rows alone give [0.0, 0.0] on every j, else OTHER_ROWS;
       null unless the band region is a single point).  band, band_rows, cmd_band, linear_model and the L1 schema are
       unchanged (AST-identical to v002).
  R3   (E_A133_2(b), supersedes E_A133_1's formula; a physics-reading change, A115 (b)) e_q(m, q) = eps_m +
       eps_q (|1 - sum_k Delta_m,k / du_k| + sum_k |Delta_m,k| / h_k).  cmd_at1 refuses MEMBERS (no out-dir) when a
       member point lacks eps_km_s or its length is not 43; a bad entry (None, bool, non-finite, negative, not a number)
       keeps every bounded term and flags only that pair MEMBER_POINT_NOISE_NOT_BOUNDED; a row with no eps_q reads
       FD_NOISE_NOT_BOUNDED (e_q = 0), as in v002.  Flags are per pair, with flag_reason; at0b is not affected.
  CUSTODY  at1 refuses an L1 whose module is not this MODULE.
  A135 item 10  handoff accepts one certificate map per member (root fields 'certificate_pins_by_member', keyed by
       member log_index); each member's handoff carries its own map; a map pin that binds another admitted point is
       refused (CERTIFICATE_MAP).  The shared-map form (v002 root fields) and S0 are unchanged.

v002 header (unchanged behaviour):
  L5   B_P1 = the forward calls before the first call whose orchestrator Probe family is NOT in PREFIX_FAMILIES
       (seed, jacobian, repair, gd_pre).  Every v001 'march0' dependency now reads "the first non-prefix-family wave"
       (prefix detection, the replay stop, the NOT_READY rule, the snapshot's recorded wave, PREFIX_MISMATCH and
       AT-0a).  When that family IS march0 the behaviour and the output bytes are v001's (snapshot form 'march0_wave');
       otherwise the snapshot records 'first_non_prefix_wave' and 'boundary_call' (e.g. a corner anchor whose round-0
       march sides all close at a box face, so the first non-prefix family is 'design').
  N-B  AT-1's e_q is the member-displacement bound sum_k 2 eps_k |Delta_m,k| / h_k (A137; erratum E_A133_1),
       reported per (member, row); the v001 band-optimum reading is removed.  [Superseded in v003 by R3.]

Text of record: CLAUDE2/A133_TWO_PHASE_PROTOCOL_V001.md (cd92ef91), sections 1, 4 and 5; ruling A133 in
ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md.  Pinned sources are imported from their exact bytes
and never modified: orchestrator c2v005 (c75a889f), engine c2v003b (6ec8b2d0), freeze v003g (48a1e48a), KMAX prereg
V005 (dbddc02c, tau).

Commands (every check runs before the exclusive new output directory is created; nothing is ever overwritten; the
campaign work dir is only read):
  snapshot  B_P1 = the engine evaluations before the first call whose orchestrator Probe family is outside
            PREFIX_FAMILIES ('march0' in every campaign that marches), from a cache-only replay of the committed
            prefix (waves below the first non-prefix-family wave, each with WAVE_RESULT.json; that wave's WAVE_PLAN
            must exist and plan the boundary call's family).  The replay at budget B_P1 runs twice and must be
            byte-equal, under check_runtime.  The BUDGET_EXHAUSTED run goes through write_calibration_record into a NEW
            Phase-1 registry.  u_A = the engine's primary_anchor, checked equal to v003g's anchor.  Engine terminal
            statuses and m_id = 0 are reported (exit 20) with no record and no NGC call.
  handoff   RI45-01 except COMPLETE: native verifier, v003g reclassification, the double replay re-derived, plan and
            admission provenance, post-state acceptance, point-scoped certificates; then the target-free export of every
            admitted point and one RI45-10 10-field handoff per v003g member.
  fdplan    --s0: the seed and its three Jacobian first-attempt points (target-free, from the config alone).
            otherwise: F (three FD points from u_A), the v003g members M and the distinct call list.
  band      refuses without the seal sha; 86 band LPs and 86 allowance LPs with the engine's _lp_max (L1).
  agree     at0a | at0b | at1 (section 4).
Exit: 0 ok, 3 refused, 4 not ready, 10 AGREEMENT_DEFECT, 20 Phase-1 terminal (no NGC call).
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

MODULE = 'phase1_c2v003a'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
ORCH_PIN = (ART + 'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
            'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d')
ENGINE_PIN = (ART + 'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py',
              '6ec8b2d0085a9460bbf481852ea5e0f64dac09af3c8a6c6fea2bf126057c3bc3')
FREEZE_PIN = (ART + 'freeze_score_readiness_cx3/v003g/prediction_freeze_c2v003g_cx3v001.py',
              '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405')
KMAX_PIN = (ART + 'kmax_prereg_v005_c2/KMAX_MATRIX_PREREG_V005.json',
            'dbddc02c4d793b44a12136fc4fc88b20c001865ddd4c89b1b70c57bc406bb174')
TAU_DEFINITION = 'tau_i = 0.25 * sigma_i per row (sigma_i = quoted random sigma of row i); root decision (a)'
TAU_OVER_SIGMA = 0.25
PREFIX_FAMILIES = ('seed', 'jacobian', 'repair', 'gd_pre')
TERMINAL = ('SEED_INVALID', 'JACOBIAN_INCOMPLETE', 'JACOBIAN_FAILED', 'NUMERIC_RANGE_REFUSED', 'EXPLORATION_FAILED',
            'NO_VALID_EVALUATION', 'NO_ADMITTED_POINT_FOUND')
BAND_LABEL = 'PHASE1_LINEARISED_ADMITTED_SET_PROJECTION_TRUNCATED_LOWER_BOUND_ON_SPREAD_NOT_A_TIER'
BAND_CONDITION = 'conditional on A13 (D = 4.04 Mpc, i = 66 deg)'
S_SNAP, S_S0, S_FD = 'PHASE1_SNAPSHOT_C2V001', 'PHASE1_S0_C2V001', 'PHASE1_FDPLAN_C2V001'
S_L1, S_VALUES, S_PROV, S_ROOT = ('PHASE1_L1_C2V001', 'PHASE1_NGC_VALUES_C2V001', 'PHASE1_PUBLISHED_PROVENANCE_C2V001',
                                  'PHASE1_HANDOFF_ROOT_FIELDS_C2V001')
S_EXPORT, S_HANDOFF = 'UNT_STEP4_TARGET_FREE_ADMITTED_EXPORT_CX3V001', 'UNT_STEP5_ADMITTED_POINT_HANDOFF_CX3V001'
EXIT = {'OK': 0, 'REFUSED': 3, 'NOT_READY': 4, 'AGREEMENT_DEFECT': 10, 'PHASE1_TERMINAL': 20}
B_P1_RULE = ('A137 L5: B_P1 = forward calls before the first call whose orchestrator Probe family is not in '
             '(seed, jacobian, repair, gd_pre)')
E_Q_READING = ('A144 R3 (erratum E_A133_2(b), superseding the E_A133_1 formula): e_q(m, q) = eps_m + eps_q * '
               '(|1 - sum_k Delta_m,k / du_k| + sum_k |Delta_m,k| / h_k), the exact worst case of the noise in '
               'g(u_m) - g(u_A) - K_q Delta_m when |delta_m| <= eps_m and |delta_A|, |delta_Fk| <= eps_q; Delta_m = u_m - '
               'u_A (engine u); du_k = the signed fdplan step of F_k and h_k = |du_k|; eps_q = the row eps_q of L1 (the '
               'largest certificate eps over u_A and the three F points, A137); eps_m = the member point own '
               'eps_km_s[q] from the Phase-2 members file (43 entries per member point, else MEMBERS is refused).  An '
               'entry that is None, bool, non-finite, negative or not a number keeps every bounded term (e_q = eps_q * '
               '(...)) and flags that pair MEMBER_POINT_NOISE_NOT_BOUNDED; a row without eps_q reads '
               'FD_NOISE_NOT_BOUNDED (e_q = 0, flagged, flag_reason NO_ROW_EPS_Q) whatever eps_m is, as in v002')
REGION_FAMILIES = ('TRUST_RADIUS', 'BOX', 'LINEAR_DDO')   # A144 R1: the fixed print order of region_rows_violated
REGION_CATEGORY = {'TRUST_RADIUS': 'OUTSIDE_TRUST_RADIUS', 'BOX': 'OUTSIDE_BOX_SLICE',
                   'LINEAR_DDO': 'OUTSIDE_LINEAR_DDO_REGION'}
CERT_MAPS = 'certificate_pins_by_member'   # A135 item 10: one certificate map per member (root handoff fields)


class Refused(Exception):
    def __init__(self, code, detail=''):
        Exception.__init__(self, '%s: %s' % (code, detail))
        self.code = code


class _Stop(BaseException):
    """Leaves the engine like the orchestrator's _ProbeStop: the engine's guards catch Exception only.  A boundary stop
    (the first call outside PREFIX_FAMILIES) also carries that call's Probe family and the engine stage it ran in."""

    def __init__(self, code, index, family=None, stage=None):
        BaseException.__init__(self, code)
        self.code, self.index, self.family, self.stage = code, index, family, stage


class StopAt(tuple):
    """(code, log index) exactly as v001 reported a replay stop, plus .family and .stage for a boundary stop."""

    def __new__(cls, code, index, family=None, stage=None):
        t = tuple.__new__(cls, (code, index))
        t.family, t.stage = family, stage
        return t


def non_prefix_families(families):
    """The plan families (lists whose first element is the Probe family name) outside PREFIX_FAMILIES (A137 L5)."""
    return [list(f) for f in families or [] if list(f)[0] not in PREFIX_FAMILIES]


def explore_stage(probe, f):
    """The engine's own exploration stage (out['stage_reached'] of _explore_impl) at the call in frame f."""
    x = f
    while x is not None and x.f_code is not probe.code_explore:
        x = x.f_back
    return (x.f_locals.get('out') or {}).get('stage_reached') if x is not None else None


# ------------------------------------------------------------------------------------------------ bytes and pins
def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def read_pinned(path, sha, label):
    if not isinstance(path, str) or not os.path.isabs(path) or not isinstance(sha, str) or len(sha) != 64:
        raise Refused('PIN_REQUIRED', '%s needs an absolute path and a 64-hex sha256' % label)
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise Refused('PIN_UNREADABLE', '%s %s: %s' % (label, path, exc))
    if sha_bytes(raw) != sha.lower():
        raise Refused('PIN_MISMATCH', '%s %s does not hash to %s' % (label, path, sha[:16]))
    return raw


def read_json_pinned(path, sha, label):
    try:
        return json.loads(read_pinned(path, sha, label).decode('utf-8'))
    except ValueError as exc:
        raise Refused('PIN_NOT_JSON', '%s: %s' % (label, exc))


def load_module(pin, name):
    read_pinned(pin[0], pin[1], name)
    sp = importlib.util.spec_from_file_location(name, pin[0])
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    read_pinned(pin[0], pin[1], name + ' (after load)')
    return m


_MODS = {}


def mod(key):
    if key not in _MODS:
        _MODS[key] = load_module({'O': ORCH_PIN, 'E': ENGINE_PIN, 'G': FREEZE_PIN}[key], 'phase1_' + key)
    return _MODS[key]


def jbytes(obj):
    return (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def canon_sha(E, obj):
    return sha_bytes(E._canonical_bytes(obj))


def fhex(xs):
    return [float(x).hex() for x in xs]


def pin_of(path):
    raw = Path(path).read_bytes()
    return {'path': os.path.realpath(str(path)), 'sha256': sha_bytes(raw)}


def tau_check():
    doc = read_json_pinned(KMAX_PIN[0], KMAX_PIN[1], 'KMAX prereg')
    if (doc.get('criterion') or {}).get('tau_definition') != TAU_DEFINITION:
        raise Refused('TAU_SOURCE', 'criterion.tau_definition is not the registered text')
    return {'path': KMAX_PIN[0], 'sha256': KMAX_PIN[1], 'tau_definition': TAU_DEFINITION, 'tau_over_sigma': TAU_OVER_SIGMA}


class Out:
    """All checks first; then one exclusive new directory and exclusive files (validate before create)."""

    def __init__(self, path, forbid=()):
        if not isinstance(path, str) or not os.path.isabs(path):
            raise Refused('OUT_DIR', '--out-dir must be absolute')
        par = os.path.realpath(os.path.dirname(path.rstrip('/')))
        if not os.path.isdir(par) or os.path.lexists(path):
            raise Refused('OUT_DIR', 'parent must exist and %s must not exist' % path)
        real = os.path.join(par, os.path.basename(path.rstrip('/')))
        for f in forbid:
            if f and (real == f or real.startswith(f.rstrip('/') + '/')):
                raise Refused('OUT_DIR', '%s lies inside the campaign work dir %s' % (real, f))
        self.dir, self.files = real, {}

    def create(self):
        os.mkdir(self.dir)

    def write(self, name, obj=None, raw=None):
        raw = jbytes(obj) if raw is None else raw
        p = os.path.join(self.dir, name)
        with open(p, 'xb') as fh:
            fh.write(raw)
            fh.flush()
            os.fsync(fh.fileno())
        self.files[name] = sha_bytes(raw)
        return p, self.files[name]


# ------------------------------------------------------------------------------------------------ campaign access
class Campaign:
    """The registered campaign, read only: Context(config) and prepare(create=False), as orchestrator plan does."""

    def __init__(self, config, config_sha256, prepare=True):
        read_pinned(config, config_sha256, 'campaign config')
        O = self.O = mod('O')
        try:
            ctx = self.ctx = O.Context(config)
            if ctx.config_sha256 != config_sha256:
                raise Refused('CONFIG_CHANGED', 'config bytes changed while loading')
            if ctx.spec['engine']['sha256'] != ENGINE_PIN[1] or sha_bytes(Path(ctx.E.__file__).read_bytes()) != ENGINE_PIN[1]:
                raise Refused('ENGINE_PIN', 'the coordinate spec does not pin engine c2v003b %s' % ENGINE_PIN[1][:16])
            self.orch = O.Orchestrator(ctx, executor=object(), log=lambda m: None)
            if prepare:
                self.orch.prepare(create=False)
        except O.OrchestratorError as exc:
            raise Refused('ORCHESTRATOR_REFUSED', str(exc)[:600])
        if prepare and self.orch.work_dir_json != 'MATCHES':
            raise Refused('WORK_DIR', 'WORK_DIR.json %s' % self.orch.work_dir_json)
        self.E, self.probe = ctx.E, O.Probe(ctx)
        self.work_dir = ctx.work_dir_record['resolved']

    def waves(self):
        out = {}
        for d in self.orch.wave_dirs():
            pp = d / 'WAVE_PLAN.json'
            if not pp.is_file():
                continue
            raw = pp.read_bytes()
            plan = json.loads(raw.decode('utf-8'))
            rp = d / 'WAVE_RESULT.json'
            out[int(plan['wave'])] = {'dir': d, 'plan': plan, 'plan_sha256': sha_bytes(raw),
                                      'result_sha256': sha_bytes(rp.read_bytes()) if rp.is_file() else None}
        return out

    def prefix(self, require_boundary=True):
        """(first non-prefix-family wave or None, waves, key -> entry): cache entries of committed waves
        (WAVE_RESULT.json present) below the first wave whose plan holds a family outside PREFIX_FAMILIES (A137 L5;
        the march0 wave in every campaign that marches); all committed waves when there is none and require_boundary
        is False."""
        ctx, waves = self.ctx, self.waves()
        m0 = sorted(w for w, x in waves.items() if non_prefix_families(x['plan'].get('families')))
        if not m0 and require_boundary:
            raise Refused('NOT_READY', 'no committed WAVE_PLAN with a family outside %s' % (PREFIX_FAMILIES,))
        w0 = m0[0] if m0 else None
        top = w0 if w0 is not None else max(waves, default=0) + 1
        for w in sorted(waves):
            p = waves[w]['plan']
            if w <= top and (p.get('cache_id'), p.get('config_sha256'), p.get('gate_digest')) != \
                    (ctx.cache_id, ctx.config_sha256, ctx.gate_digest):
                raise Refused('PLAN_BINDING', 'wave %d was planned under another cache id, config or gate digest' % w)
            if w0 is not None and w < w0 and waves[w]['result_sha256'] is None:
                raise Refused('NOT_READY', 'prefix wave %d has no WAVE_RESULT.json' % w)
        if sorted(w for w in waves if w < top) != list(range(1, top)):
            raise Refused('NOT_READY', 'committed waves are not 1..%d' % (top - 1))
        entries = {}
        for k, e in self.orch.cache.entries.items():
            src, wv = e.get('source'), (e.get('provenance') or {}).get('wave')
            if src == 'ANCHOR_ALIAS' or (src in ('WAVE', 'IN_PROCESS_TEST', 'ROOT_RESOLUTION') and
                                         isinstance(wv, int) and wv < top and waves.get(wv, {}).get('result_sha256')):
                entries[k] = e
        return w0, waves, entries

    def replay(self, entries, budget):
        """The unmodified engine, forward = cache-only lookup in `entries`.  The first call whose family is outside
        PREFIX_FAMILIES stops it as the boundary (A137 L5; 'MARCH0' when that family is march0, as in v001); a miss
        stops it too."""
        O, probe, calls = self.O, self.probe, []

        def fwd(theta):
            f = sys._getframe(1)
            c = probe.context(f)
            idx = f.f_locals['entry']['index'] if f.f_code is probe.code_eval else None
            fam = c['family'][0]
            if idx != len(calls):
                raise _Stop('LOG_INDEX_NOT_CALL_COUNT', idx)
            if fam == 'march0':
                raise _Stop('MARCH0', idx, list(c['family']), 'march')
            if fam not in ('seed', 'jacobian') and c['m_id'] == 0:
                raise _Stop('NO_IDENTIFIED_DIRECTION', idx)
            if fam not in PREFIX_FAMILIES:
                raise _Stop('FIRST_NON_PREFIX_%s' % fam, idx, list(c['family']), explore_stage(probe, f))
            key = O.theta_key(theta)
            e = entries.get(key)
            if e is None:
                raise _Stop('PREFIX_MISS', idx)
            calls.append({'index': idx, 'key': key, 'family': list(c['family']), 'branch': list(c['branch'])})
            return copy.deepcopy(e['forward'])
        kw = self.ctx.run_kwargs()
        kw['budget'] = int(budget)
        try:
            return self.E.run_calibration_region(forward=fwd, **kw), calls, None
        except _Stop as s:
            return None, calls, StopAt(s.code, s.index, s.family, s.stage)

    def b_p1(self, entries):
        """Pass 1 at the registered budget: ('B_P1', n, calls, boundary) | ('TERMINAL', status, calls, None), with
        boundary = {family, stage_reached} of the first call outside PREFIX_FAMILIES (A137 L5)."""
        run, calls, stop = self.replay(entries, self.ctx.params['budget'])
        if stop is None:
            if run['status'] in TERMINAL:
                return 'TERMINAL', run['status'], calls, None
            if run['status'] == 'COMPLETE' and not (run.get('identifiability') or {}).get('identified'):
                return 'TERMINAL', 'NO_IDENTIFIED_DIRECTION', calls, None
            raise Refused('REPLAY_UNEXPECTED', 'replay ended %s with no call outside %s' % (run['status'],
                                                                                           PREFIX_FAMILIES))
        if stop.family is not None:
            return 'B_P1', stop[1], calls, {'family': list(stop.family), 'stage_reached': stop.stage}
        if stop[0] == 'NO_IDENTIFIED_DIRECTION':
            return 'TERMINAL', 'NO_IDENTIFIED_DIRECTION', calls, None
        raise Refused('NOT_READY' if stop[0] == 'PREFIX_MISS' else 'REPLAY_STOPPED', '%s at log index %s' % stop)

    def snapshot_run(self, entries, b, stage='march'):
        """The run at budget B_P1, twice, byte-equal and valid (refuses B_P1 +/- 1); `stage` is the engine stage of
        the first non-prefix-family call ('march' for march0, as in v001)."""
        r1, c1, s1 = self.replay(entries, b)
        r2, _c2, s2 = self.replay(entries, b)
        if s1 or s2:
            raise Refused('B_P1_WRONG', 'replay at budget %d stopped %s' % (b, s1 or s2))
        b1, b2 = self.E._canonical_bytes(r1), self.E._canonical_bytes(r2)
        if b1 != b2:
            raise Refused('REPLAY_NONDETERMINISTIC', 'the two replays at budget %d differ' % b)
        check_snapshot_run(r1, b, stage)
        return r1, c1, sha_bytes(b1)

    def runtime(self):
        bad = self.orch.check_runtime()
        if bad:
            raise Refused('RUNTIME', bad)

    def next_requested(self, entries):
        """The orchestrator's own probe on the prefix cache: the calls it would plan next (dedup, in order)."""
        class View:
            def forward(self, key):
                e = entries.get(key)
                return copy.deepcopy(e['forward']) if e is not None else None
        pr = self.probe.run(View(), 'probe')
        return [(m['key'], m['theta']) for m in self.orch._dedup(pr['misses'])]


def check_snapshot_run(run, b, stage='march'):
    ex = run.get('exploration') or {}
    pa = ex.get('primary_anchor')
    bad = []
    if run.get('status') != 'BUDGET_EXHAUSTED' or ex.get('status') != 'BUDGET_EXHAUSTED':
        bad.append('status %r/%r is not BUDGET_EXHAUSTED' % (run.get('status'), ex.get('status')))
    if len(run.get('evaluation_log') or []) != b:
        bad.append('log length %d != B_P1 %d' % (len(run.get('evaluation_log') or []), b))
    if ex.get('stage_reached') != stage:
        bad.append('budget exhausted at stage %r, not at the first march call' % ex.get('stage_reached')
                   if stage == 'march' else 'budget exhausted at stage %r, not at the stage %r of the first '
                   'non-prefix-family call' % (ex.get('stage_reached'), stage))
    if not isinstance(pa, dict) or not isinstance(pa.get('log_index'), int) or not 0 <= pa['log_index'] < b:
        bad.append('no primary_anchor inside the prefix')
    if not (run.get('identifiability') or {}).get('identified'):
        bad.append('no identified direction')
    if bad:
        raise Refused('B_P1_WRONG', '; '.join(bad))


# ------------------------------------------------------------------------------------------------ v003g
def freeze_spec(ctx):
    G = mod('G')
    coords = list(ctx.spec['coordinates']) + \
        list(ctx.spec['ngc3198_nuisance_slots']['placeholder_for_engine_coordinate_derivation'])
    am = G.apply_coordinate_mode(coordinates=coords, coordinate_mode=ctx.coordinate_mode)
    fs = G.make_freeze_coordinate_spec(coordinates=am.get('coordinates') or []) if am.get('ok') else {'ok': False}
    if not fs.get('ok') or _o_canon(fs['engine_coordinates']) != _o_canon(ctx.engine_coordinates):
        raise Refused('FREEZE_SPEC', 'v003g freeze coordinates do not reproduce the campaign engine coordinates')
    return fs['spec']


def v003g_members(ctx, run, interior_count):
    """v003g select_representative_points on the B_P1 run (layout A, rectangles from the region bytes)."""
    if type(interior_count) is not int or interior_count < 0:
        raise Refused('INTERIOR_COUNT', 'RI45-14 interior_count must be an int >= 0')
    sel = mod('G').select_representative_points(exploration=run, interior_count=interior_count, spec=freeze_spec(ctx))
    if not sel.get('ok'):
        raise Refused('V003G_REFUSED', sel.get('reasons'))
    pa = run['exploration']['primary_anchor']
    ar = sel['admitted_region']
    am = [p for p in sel['points'] if p['log_index'] == pa['log_index']]
    if ar['selection_anchor_log_index'] != pa['log_index'] or len(am) != 1 or am[0]['u'] != pa['u'] or \
            not sel['admission_reverified']:
        raise Refused('ANCHOR_MISMATCH', 'v003g anchor %r is not u_A (log index %r)'
                      % (ar['selection_anchor_log_index'], pa['log_index']))
    return sel


# ------------------------------------------------------------------------------------------------ snapshot
def cmd_snapshot(a):
    cp = Campaign(a.config, a.config_sha256)
    out = Out(a.out_dir, [cp.work_dir])
    w0, waves, entries = cp.prefix(require_boundary=False)
    kind, val, calls1, bnd = cp.b_p1(entries)
    fams0 = [list(f) for f in waves[w0]['plan'].get('families') or []] if w0 is not None else []
    if kind == 'B_P1' and w0 is None:
        raise Refused('NOT_READY', 'B_P1 = %d is reached but the march0 WAVE_PLAN is not written yet' % val
                      if bnd['family'] == ['march0'] else 'B_P1 = %d is reached but the first non-prefix-family '
                      'WAVE_PLAN (%s) is not written yet' % (val, bnd['family']))
    if kind == 'B_P1' and bnd['family'] not in fams0:
        raise Refused('PREFIX_MISMATCH', 'the first non-prefix-family wave %d plans %s, not the replay boundary '
                      'family %s' % (w0, fams0, bnd['family']))
    cp.runtime()
    used = sorted(w for w in waves if w0 is None or w < w0)
    m0form = w0 is not None and ((bnd['family'] == ['march0']) if kind == 'B_P1' else (['march0'] in fams0))
    base = {'schema': S_SNAP, 'module': MODULE, 'tool_sha256': pin_of(__file__)['sha256'],
            'pins': {'orchestrator': ORCH_PIN[1], 'engine': ENGINE_PIN[1], 'freeze_v003g': FREEZE_PIN[1],
                     'config': {'path': a.config, 'sha256': a.config_sha256}},
            'cache_id': cp.ctx.cache_id, 'gate_digest': cp.ctx.gate_digest, 'runtime_check': 'PASS',
            'march0_wave': {'wave': w0, 'plan_sha256': waves[w0]['plan_sha256']} if m0form else None,
            'prefix_waves': [{'wave': w, 'plan_sha256': waves[w]['plan_sha256'],
                              'result_sha256': waves[w]['result_sha256']} for w in used],
            'final_summary_present': (cp.ctx.work_dir / 'FINAL_SUMMARY.json').is_file()}
    if w0 is not None and not m0form:   # A137 L5: the recorded wave when the first non-prefix family is not march0
        base.update(first_non_prefix_wave={'wave': w0, 'plan_sha256': waves[w0]['plan_sha256'], 'families': fams0},
                    b_p1_rule=B_P1_RULE)
    if kind == 'TERMINAL':
        out.create()
        out.write('SNAPSHOT_C2V001.json', dict(base, phase1_status=val, ngc_calls=0, b_p1=None,
                                                 prefix_calls=calls1, note='A133 1.3: Phase 1 reports the code and makes '
                                                 'no NGC call; v003g refuses m_id = 0 (freeze L1326)'))
        return 'PHASE1_TERMINAL', {'phase1_status': val, 'out_dir': out.dir}
    b = val
    run, calls, run_sha = cp.snapshot_run(entries, b, bnd['stage_reached'])
    if not m0form:
        base['boundary_call'] = {'log_index': b, 'family': bnd['family'], 'stage_reached': bnd['stage_reached']}
    if [c['key'] for c in calls] != [c['key'] for c in calls1]:
        raise Refused('REPLAY_PREFIX_MISMATCH', 'the budget-B_P1 replay requested other thetas than pass 1')
    sel = v003g_members(cp.ctx, run, 0)
    out.create()
    rp = os.path.join(out.dir, 'PHASE1_CALIBRATION_RECORD_BUDGET_EXHAUSTED_%s.json' % run_sha[:16])
    gp = os.path.join(out.dir, 'PHASE1_CALIBRATION_REGISTRY.jsonl')
    w = cp.E.write_calibration_record(run=run, record_path=rp, registry_path=gp)
    v = cp.E.verify_calibration_record(record_path=rp, registry_path=gp)
    if not (w.get('ok') and v.get('ok')):
        raise Refused('RECORD', (w.get('reasons'), v.get('reasons')))
    pa = run['exploration']['primary_anchor']
    doc = dict(base, phase1_status='BUDGET_EXHAUSTED', b_p1=b, prefix_calls=calls,
               replay={'passes': 2, 'byte_equal': True, 'run_canonical_sha256': run_sha},
               record={'file': os.path.basename(rp), 'registry_file': os.path.basename(gp),
                       'record_file_sha256': w['record_file_sha256'], 'record_sha256': w['record_sha256'],
                       'registry_line_sha256': w['registry_line_sha256'],
                       'exploration_fingerprint': w['exploration_fingerprint']},
               u_A={'log_index': pa['log_index'], 'source': pa['source'], 'purpose': pa['purpose'], 'u': pa['u'],
                    'u_hex': fhex(pa['u']), 'theta_natural': pa['theta_natural']},
               v003g_anchor_check={'selection_anchor_log_index': sel['admitted_region']['selection_anchor_log_index'],
                                   'role': [p['role'] for p in sel['points'] if p['log_index'] == pa['log_index']][0],
                                   'n_admitted': sel['n_admitted']})
    out.write('SNAPSHOT_C2V001.json', doc)
    return 'OK', {'b_p1': b, 'u_A_log_index': pa['log_index'], 'out_dir': out.dir, 'files': out.files}


def recorded_boundary(doc):
    """The snapshot's recorded first non-prefix-family wave and boundary call (A137 L5): the v001 form 'march0_wave'
    when that family is march0, otherwise 'first_non_prefix_wave' with 'boundary_call'."""
    if doc.get('march0_wave') is not None:
        if 'first_non_prefix_wave' in doc or 'boundary_call' in doc:
            raise Refused('SNAPSHOT', 'both the march0 form and the first-non-prefix-family form are present')
        return {'wave': doc['march0_wave']['wave'], 'plan_sha256': doc['march0_wave']['plan_sha256'],
                'family': ['march0'], 'stage_reached': 'march'}
    w, c = doc.get('first_non_prefix_wave'), doc.get('boundary_call')
    if not isinstance(w, dict) or not isinstance(c, dict) or c.get('log_index') != doc.get('b_p1') or \
            c.get('family') == ['march0'] or c.get('family') not in (w.get('families') or []):
        raise Refused('SNAPSHOT', 'no consistent recorded first non-prefix-family wave and boundary call')
    return {'wave': w['wave'], 'plan_sha256': w['plan_sha256'], 'family': c['family'],
            'stage_reached': c['stage_reached']}


def load_snapshot(snap_dir, snap_sha):
    E = mod('E')
    doc = read_json_pinned(os.path.join(snap_dir, 'SNAPSHOT_C2V001.json'), snap_sha, 'snapshot')
    if doc.get('schema') != S_SNAP or doc.get('phase1_status') != 'BUDGET_EXHAUSTED':
        raise Refused('SNAPSHOT', 'not a BUDGET_EXHAUSTED %s' % S_SNAP)
    r = doc['record']
    rp, gp = os.path.join(snap_dir, r['file']), os.path.join(snap_dir, r['registry_file'])
    rec = read_json_pinned(rp, r['record_file_sha256'], 'Phase-1 record')
    v = E.verify_calibration_record(record_path=rp, registry_path=gp)
    run = rec.get('run') or {}
    if not v.get('ok') or rec.get('module_file_sha256') != ENGINE_PIN[1]:
        raise Refused('RECORD_UNVERIFIED', v.get('reasons'))
    if canon_sha(E, run) != doc['replay']['run_canonical_sha256']:
        raise Refused('RECORD_NOT_SNAPSHOT', 'record run is not the snapshot replay')
    check_snapshot_run(run, doc['b_p1'], recorded_boundary(doc)['stage_reached'])
    pa = run['exploration']['primary_anchor']
    if pa['log_index'] != doc['u_A']['log_index'] or fhex(pa['u']) != doc['u_A']['u_hex']:
        raise Refused('ANCHOR_MISMATCH', 'record primary_anchor is not the snapshot u_A')
    return doc, rec, run


# ------------------------------------------------------------------------------------------------ handoff (RI45-01)
def provenance_checks(cp, run, prov, waves):
    """Plan and admission provenance, post-state acceptance, point-scoped certificates, per admitted point."""
    O, bad, rows = cp.O, [], []
    if prov.get('schema') != S_PROV or prov.get('cache_id') != cp.ctx.cache_id:
        raise Refused('PROVENANCE', 'schema or cache id')
    adm = run['exploration']['admitted_points']
    keys = {p['log_index']: O.theta_key(p['theta_natural']) for p in adm}
    specs = {}
    for p in adm:
        e = cp.orch.cache.entries.get(keys[p['log_index']])
        specs[p['log_index']] = ((e or {}).get('provenance') or {}).get('spec_sha256')
    for p in adm:
        li, key = p['log_index'], keys[p['log_index']]
        e = cp.orch.cache.entries.get(key) or {}
        pv, row = e.get('provenance') or {}, {'log_index': li, 'key': key, 'spec_sha256': specs[li]}
        wv = pv.get('wave')
        wp = waves.get(wv)
        if e.get('source') not in ('WAVE', 'IN_PROCESS_TEST') or wp is None:
            bad.append('%d: no wave provenance (source %r)' % (li, e.get('source')))
            continue
        pcalls, ci = wp['plan'].get('calls') or [], pv.get('call_index')
        call = pcalls[ci] if isinstance(ci, int) and 0 <= ci < len(pcalls) else None
        if not call or call.get('key') != key or call.get('spec_sha256') != specs[li]:
            bad.append('%d: wave %s plan does not hold this call' % (li, wv))
        if (prov.get('wave_plans') or {}).get(str(wv)) != wp['plan_sha256']:
            bad.append('%d: wave %s plan sha differs from the published one' % (li, wv))
        adp = (prov.get('admissions') or {}).get(str(wv))
        try:
            araw = read_pinned((adp or {}).get('path'), (adp or {}).get('sha256'), 'admission %s' % wv)
            if wp['plan_sha256'].encode() not in araw:
                bad.append('%d: admission record of wave %s does not name its plan sha' % (li, wv))
        except Refused as exc:
            bad.append('%d: admission: %s' % (li, exc))
        pt = (prov.get('points') or {}).get(key) or {}
        acc, certs = pt.get('post_state_acceptance'), pt.get('certificates')
        if not isinstance(acc, dict) or acc.get('status') != 'ACCEPTED':
            bad.append('%d: post-state acceptance missing or not ACCEPTED' % li)
        else:
            try:
                raw = read_pinned(acc.get('path'), acc.get('sha256'), 'acceptance %d' % li)
                bad.extend(_scope(li, raw, key, specs[li], keys, specs, 'acceptance'))
            except Refused as exc:
                bad.append('%d: acceptance: %s' % (li, exc))
        if not isinstance(certs, list) or not certs:
            bad.append('%d: no point-scoped certificate' % li)
        for c in certs or []:
            try:
                raw = read_pinned((c or {}).get('path'), (c or {}).get('sha256'), 'certificate %d' % li)
                bad.extend(_scope(li, raw, key, specs[li], keys, specs, 'certificate'))
            except Refused as exc:
                bad.append('%d: certificate: %s' % (li, exc))
        row.update(wave=wv, call_index=pv.get('call_index'), plan_sha256=wp['plan_sha256'])
        rows.append(row)
    if bad:
        raise Refused('PROVENANCE', bad[:12])
    return rows


def _scope(li, raw, key, spec, keys, specs, what):
    """Binding by exact token: the record names this point (theta key or spec sha) and no other admitted point."""
    if key.encode() not in raw and not (spec and spec.encode() in raw):
        return ['%d: %s does not bind this point' % (li, what)]
    other = [o for o in keys if o != li and (keys[o].encode() in raw or (specs[o] and specs[o].encode() in raw))]
    return ['%d: %s also binds admitted point(s) %s' % (li, what, other)] if other else []


def cmd_handoff(a):
    E = mod('E')
    doc, rec, run = load_snapshot(a.snapshot, a.snapshot_sha256)
    cp = Campaign(a.config, a.config_sha256)
    out = Out(a.out_dir, [cp.work_dir])
    rb = recorded_boundary(doc)
    w0, waves, entries = cp.prefix()
    if w0 != rb['wave'] or waves[w0]['plan_sha256'] != rb['plan_sha256']:
        raise Refused('PREFIX_MISMATCH', 'march0 wave plan changed since the snapshot' if rb['family'] == ['march0']
                      else 'the first non-prefix-family wave or its plan changed since the snapshot (now wave %s, '
                      'recorded %s)' % (w0, rb['wave']))
    run2, _c, rsha = cp.snapshot_run(entries, doc['b_p1'], rb['stage_reached'])
    if rsha != canon_sha(E, run):
        raise Refused('REPLAY_MISMATCH', 'the double replay does not reproduce the recorded run')
    cp.runtime()
    sel = v003g_members(cp.ctx, run, a.interior_count)
    if sel['calibration_fingerprint'] != rec['exploration_fingerprint']:
        raise Refused('FINGERPRINT', 'v003g fingerprint differs from the record')
    adm = sorted(run['exploration']['admitted_points'], key=lambda p: p['log_index'])
    export_pts = [{'log_index': p['log_index'], 'u': list(p['u']), 'theta_natural': dict(p['theta_natural'])}
                  for p in adm]
    roster = sorted(x['log_index'] for x in sel['admitted_region']['admitted_projections_identified'])
    if [p['log_index'] for p in export_pts] != roster or len(roster) != sel['n_admitted']:
        raise Refused('ROSTER', 'the export is not the complete admitted roster')
    prov = read_json_pinned(a.provenance, a.provenance_sha256, 'published provenance')
    prow = provenance_checks(cp, run, prov, waves)
    rf = read_json_pinned(a.root_fields, a.root_fields_sha256, 'root handoff fields')
    want = {'schema', 'mode', 'root_admission', 'policy_pin', 'v007_adoption_pin', 'certificate_pins', 'driver_branch',
            'driver_acceptance_pin', 'coordinate_pin'}
    want_pm = (want - {'certificate_pins'}) | {CERT_MAPS}   # A135 item 10: one certificate map per member
    if set(rf) not in (want, want_pm) or rf['schema'] != S_ROOT:
        raise Refused('ROOT_FIELDS', 'keys must be %s' % sorted(want) + ', or the same with certificate_pins replaced by '
                      '%s (A135 item 10)' % CERT_MAPS)
    per_member = CERT_MAPS in rf
    if rf['mode'] != ('SYNTHETIC_DRY_ONLY' if cp.ctx.synthetic else 'ADMITTED'):
        raise Refused('ROOT_FIELDS', 'mode %r: a synthetic_test campaign hands off SYNTHETIC_DRY_ONLY only, a real one '
                      'ADMITTED only' % (rf['mode'],))
    if not all(rf[k] is None or (isinstance(rf[k], dict) and set(rf[k]) == {'path', 'sha256'})
               for k in ('policy_pin', 'v007_adoption_pin', 'driver_acceptance_pin', 'coordinate_pin')) or \
            not isinstance(rf[CERT_MAPS if per_member else 'certificate_pins'], dict):
        raise Refused('ROOT_FIELDS', 'pins must be {path, sha256} or null; certificate_pins an object' if not per_member
                      else 'pins must be {path, sha256} or null; %s an object' % CERT_MAPS)
    for lab in ('policy_pin', 'v007_adoption_pin', 'driver_acceptance_pin', 'coordinate_pin'):
        if rf[lab] is not None:
            read_pinned(rf[lab].get('path'), rf[lab].get('sha256'), lab)
    if per_member:
        cmaps = certificate_maps(rf[CERT_MAPS], sel['points'], prow)
    else:
        for lab, p in (rf['certificate_pins'] or {}).items():
            if isinstance(p, dict):
                read_pinned(p.get('path'), p.get('sha256'), 'certificate_pins.' + lab)
        cmaps = {m['log_index']: rf['certificate_pins'] for m in sel['points']}
    out.create()
    export = {'schema': S_EXPORT, 'mode': rf['mode'], 'target_free': True, 'coordinate_pin': rf['coordinate_pin'],
              'admitted_points': export_pts}
    ep, es = out.write('TARGET_FREE_EXPORT_C2V001.json', export)
    hand = []
    for m in sel['points']:
        h = {'schema': S_HANDOFF, 'mode': rf['mode'], 'root_admission': rf['root_admission'], 'log_index': m['log_index'],
             'policy_pin': rf['policy_pin'], 'source_export_pin': {'path': ep, 'sha256': es},
             'v007_adoption_pin': rf['v007_adoption_pin'], 'certificate_pins': cmaps[m['log_index']],
             'driver_branch': rf['driver_branch'], 'driver_acceptance_pin': rf['driver_acceptance_pin']}
        p, s = out.write('HANDOFF_%04d_C2V001.json' % m['log_index'], h)
        hand.append({'log_index': m['log_index'], 'role': m['role'], 'path': p, 'sha256': s})
    receipt = {'schema': 'PHASE1_HANDOFF_RECEIPT_C2V001', 'module': MODULE, 'launch_authorized': False,
               'snapshot_sha256': a.snapshot_sha256, 'record_file_sha256': doc['record']['record_file_sha256'],
               'interior_count_RI45_14': a.interior_count, 'export': {'path': ep, 'sha256': es}, 'handoffs': hand,
               'provenance': {'path': a.provenance, 'sha256': a.provenance_sha256, 'points': prow},
               'root_fields': {'path': a.root_fields, 'sha256': a.root_fields_sha256},
               'checks': ['native verify_calibration_record', 'v003g reclassification (admission_reverified) and '
                          'fingerprint', 'double replay reproduces the record', 'check_runtime',
                          'complete roster', 'plan/admission provenance', 'post-state acceptance',
                          'point-scoped certificates'],
               'departure': 'A133 1.6: RI45-01 COMPLETE requirement replaced (record status BUDGET_EXHAUSTED at B_P1)'}
    if per_member:   # A135 item 10; the shared-map receipt stays v002's (only module differs)
        receipt['certificate_map'] = 'ONE_PER_MEMBER (A135 item 10)'
        receipt['checks'] = receipt['checks'] + ['one certificate map per v003g member; every map pin hash-verified; '
                                                 'no map pin binds another admitted point']
    out.write('HANDOFF_RECEIPT_C2V001.json', receipt)
    return 'OK', {'members': [h['log_index'] for h in hand], 'out_dir': out.dir, 'files': out.files}


def certificate_maps(maps, members, prow):
    """A135 item 10: {log_index: certificate map} from root's certificate_pins_by_member (keys = the v003g member
    log_indices as strings, exactly).  A map is an object of label -> {path, sha256} or a non-pin placeholder, as the
    shared certificate_pins of v002.  Every pin is hash-verified, and a pin that binds another admitted point (its theta
    key or its spec sha, by exact token, as provenance _scope) is refused: a member is never handed another member's
    certificate.  A pin that binds no admitted point (a shared custody pin) is allowed."""
    want = sorted(str(m['log_index']) for m in members)
    if sorted(maps) != want:
        raise Refused('CERTIFICATE_MAP', '%s keys must be exactly the v003g member log indices %s, got %s'
                      % (CERT_MAPS, want, sorted(maps)))
    keys = {r['log_index']: r['key'] for r in prow}
    specs = {r['log_index']: r['spec_sha256'] for r in prow}
    out, bad = {}, []
    for m in members:
        li = m['log_index']
        cm = maps[str(li)]
        if not isinstance(cm, dict):
            raise Refused('CERTIFICATE_MAP', 'member %d: the certificate map must be an object' % li)
        for lab, p in sorted(cm.items()):
            if not isinstance(p, dict):
                continue
            raw = read_pinned(p.get('path'), p.get('sha256'), '%s.%d.%s' % (CERT_MAPS, li, lab))
            other = [o for o in sorted(keys) if o != li and (keys[o].encode() in raw or
                                                            (specs[o] and specs[o].encode() in raw))]
            if other:
                bad.append('member %d: %s binds admitted point(s) %s' % (li, lab, other))
        out[li] = cm
    if bad:
        raise Refused('CERTIFICATE_MAP', bad[:12])
    return out


# ------------------------------------------------------------------------------------------------ fdplan
def side_point(u, k, rel_step, min_step):
    """A133 1.4 / the engine's side rule: plus step min(rel_step, 1-u_k); below min_step the minus step min(rel_step, u_k)."""
    h = min(rel_step, 1.0 - float(u[k]))
    side = 'plus'
    if h < min_step:
        side, h = 'minus', min(rel_step, float(u[k]))
    p = [float(x) for x in u]
    p[k] = float(u[k]) + h if side == 'plus' else float(u[k]) - h
    p = [min(max(x, 0.0), 1.0) for x in p]   # the engine clips onto the unit box (_evaluate_point)
    return p, side, h


def theta_of(cp, u):
    nat = cp.E.to_natural(spec=cp.ctx.es, u=u)
    if not nat.get('ok'):
        raise Refused('TO_NATURAL', nat.get('reasons'))
    th = nat['theta_natural']
    sh = cp.E.shared_theta(spec=cp.ctx.es, theta_natural=th)
    return {'u': list(u), 'u_hex': fhex(u), 'theta_natural': th, 'theta_hex': {k: float(v).hex() for k, v in th.items()},
            'theta_shared': sh['theta_shared'] if sh.get('ok') else None, 'key': cp.O.theta_key(th)}


def s0_points(cp):
    P = cp.ctx.params
    u0 = [cp.ctx.trial_u[j] if (P['u_seed'] is None or P['u_seed'][j] is None) else P['u_seed'][j]
          for j in range(cp.ctx.n_varying)]
    pts = [dict(theta_of(cp, u0), role='seed')]
    for k in range(cp.ctx.n_varying):
        p, side, h = side_point(u0, k, float(P['rel_step']), float(P['min_step']))
        pts.append(dict(theta_of(cp, p), role='jacobian_first_attempt_%d' % k, axis=k, side=side, step=h))
    return pts


def cmd_fdplan(a):
    cp = Campaign(a.config, a.config_sha256, prepare=False)
    out = Out(a.out_dir, [cp.work_dir])
    if a.s0_only:
        doc = {'schema': S_S0, 'module': MODULE, 'config': {'path': a.config, 'sha256': a.config_sha256},
               'cache_id': cp.ctx.cache_id, 'points': s0_points(cp),
               'note': 'A133 1.4: S0 = the seed and its three Jacobian first-attempt points; target-free'}
        out.create()
        out.write('S0_C2V001.json', doc)
        return 'OK', {'out_dir': out.dir, 'files': out.files}
    doc, rec, run = load_snapshot(a.snapshot, a.snapshot_sha256)
    pa, P = run['exploration']['primary_anchor'], run['parameters']
    if cp.E._canonical_bytes(run['spec']) != cp.E._canonical_bytes(cp.ctx.es):
        raise Refused('SPEC_BINDING', 'the record engine spec is not the campaign engine spec')
    log = run['evaluation_log']
    F = []
    for k in range(cp.ctx.n_varying):
        p, side, h = side_point(pa['u'], k, float(P['rel_step']), float(P['min_step']))
        pt = dict(theta_of(cp, p), role='F%d' % k, axis=k, side=side, step=h, du=p[k] - float(pa['u'][k]))
        if pa['source'] == 'seed':   # A133 1.4: F is the seed Jacobian's first-attempt points, taken from the record
            hit = [e for e in log if e['purpose'] == 'jacobian' and fhex(e['u']) == pt['u_hex']]
            if len(hit) != 1 or cp.O.theta_key(hit[0]['theta_natural']) != pt['key']:
                raise Refused('F_NOT_IN_RECORD', 'seed first-attempt point %d is not in the record bit for bit' % k)
            pt['record_log_index'] = hit[0]['index']
        F.append(pt)
    sel = v003g_members(cp.ctx, run, a.interior_count)
    M = [dict(theta_of(cp, m['u']), role=m['role'], log_index=m['log_index']) for m in sel['points']]
    for m, s in zip(M, sel['points']):
        if m['theta_natural'] != s['theta_natural']:
            raise Refused('MEMBER_THETA', 'member %d theta does not re-derive bit for bit' % s['log_index'])
    calls, seen = [], {}
    for x in M + F:
        if x['key'] in seen:
            seen[x['key']]['serves'].append(x['role'])
            continue
        seen[x['key']] = {'key': x['key'], 'theta_shared': x['theta_shared'], 'u_hex': x['u_hex'], 'serves': [x['role']]}
        calls.append(seen[x['key']])
    plan = {'schema': S_FD, 'module': MODULE, 'snapshot_sha256': a.snapshot_sha256,
            'record_file_sha256': doc['record']['record_file_sha256'], 'interior_count_RI45_14': a.interior_count,
            'u_A': doc['u_A'], 'members': M, 'F': F, 'distinct_calls': calls, 'n_distinct_calls': len(calls),
            'rule': 'A133 1.4: h_k = min(rel_step, 1-u_A,k); below min_step the minus side with min(rel_step, u_A,k); an '
                    'F point equal to a member theta is the same call, not a skip',
            'not_run_in_phase1': {'ORIGINAL_K': 'budget 0 (NOT_AVAILABLE)', 'sensitivity': 'budget 0 (rows invalid)'}}
    out.create()
    out.write('FDPLAN_C2V001.json', plan)
    return 'OK', {'n_distinct_calls': len(calls), 'out_dir': out.dir, 'files': out.files}


# ------------------------------------------------------------------------------------------------ band (L1)
def linear_model(E, run):
    """u_A, q_A, S, V_I, V_N, zrow, sigma from the recorded run; rectangles re-derived from the region bytes."""
    import numpy as np
    reg = E.load_observation_region(path=run['region']['path'], expected_sha256=run['region']['sha256'])
    if not reg.get('ok'):
        raise Refused('REGION', reg.get('reasons'))
    rows, idn = reg['row_ids'], run['identifiability']
    pa = run['exploration']['primary_anchor']
    ent = run['evaluation_log'][pa['log_index']]
    cls = E.classify_prediction(prediction=ent['prediction'], rectangles=reg['rectangles'], row_ids=rows)
    if cls.get('admitted') is not True or fhex(ent['u']) != fhex(pa['u']):
        raise Refused('U_A_NOT_ADMITTED', 'the u_A log entry does not re-classify admitted')
    lo = np.array([reg['rectangles'][r][0] for r in rows])
    hi = np.array([reg['rectangles'][r][1] for r in rows])
    sig = np.array([reg['sigmas'][r] for r in rows])
    f = np.array([ent['prediction']['speeds_km_s'][r] for r in rows])
    S, V = np.array(idn['scaled_jacobian']), np.array(idn['right_vectors'])
    I, N = list(idn['identified']), list(idn['near_null'])
    return {'uA': np.array(pa['u']), 'qA': (f - 0.5 * (lo + hi)) / sig, 'zrow': 0.5 * (hi - lo) / sig, 'S': S,
            'V': V, 'I': I, 'N': N, 'VI': V[I], 'fA': f, 'sig': sig, 'J': np.array(run['jacobian']['jacobian_u']),
            'P': run['parameters'], 'rows': rows}


def lp_pair(E, A, b, w, lp=None):
    """(min, max, c_min, c_max, statuses) of w.c over A c <= b, with the engine's own simplex."""
    lp = lp or E._lp_max
    cmax, smax = lp(A, b, w)
    cmin, smin = lp(A, b, -w)
    return float(w @ cmin), float(w @ cmax), cmin, cmax, (smin, smax)


def band_rows(E, L, vals, fd, lp=None):
    import numpy as np
    VI, m = L['VI'], len(L['I'])
    SVI = L['S'] @ VI.T
    eye = np.eye(m)
    r = float(L['P']['max_repair_step']) / math.sqrt(m)
    A = np.vstack([SVI, -SVI, VI.T, -VI.T, eye, -eye])
    b_band = np.concatenate([L['zrow'] - L['qA'], L['zrow'] + L['qA'], 1.0 - L['uA'], L['uA'], np.full(m, r), np.full(m, r)])
    tol = float(L['P']['hull_growth_tol'])
    b_all = np.concatenate([np.full(len(L['rows']), TAU_OVER_SIGMA), np.full(len(L['rows']), TAU_OVER_SIGMA),
                            1.0 - L['uA'], L['uA'], np.full(m, tol), np.full(m, tol)])
    du = np.array([f['du'] for f in fd])
    h = np.abs(du)
    pts = {p['role']: p for p in vals['points']}
    roles = ['u_A'] + [f['role'] for f in fd]
    out = []
    for q, qid in enumerate(vals['query_ids']):
        row = {'id': qid}
        invalid = [ro for ro in roles if pts[ro]['valid'][q] is not True or
                   not isinstance(pts[ro]['speeds_km_s'][q], (int, float)) or isinstance(pts[ro]['speeds_km_s'][q], bool)
                   or not math.isfinite(pts[ro]['speeds_km_s'][q])]
        if invalid:
            out.append(dict(row, status='NOT_AVAILABLE', reason='INVALID_AT_' + '_'.join(invalid)))
            continue
        gA = float(pts['u_A']['speeds_km_s'][q])
        K = np.array([(float(pts[f['role']]['speeds_km_s'][q]) - gA) / du[k] for k, f in enumerate(fd)])
        w = VI @ K
        row.update(g_A=gA, K_q=K.tolist(), K_q_VI=w.tolist(),
                   K_q_near_null={str(j): float(K @ L['V'][j]) for j in L['N']})
        lo, hi, cmin, cmax, st = lp_pair(E, A, b_band, w, lp)
        alo, ahi, _x, _y, st2 = lp_pair(E, A, b_all, w, lp)
        row['lp_status'] = {'band_min': st[0], 'band_max': st[1], 'allowance_min': st2[0], 'allowance_max': st2[1]}
        if st != ('OPTIMAL', 'OPTIMAL'):
            row.update(status='NOT_AVAILABLE', reason='LP_%s_%s' % st)
            out.append(row)
            continue
        row.update(status='AVAILABLE', lo=gA + lo, hi=gA + hi, width=hi - lo,
                   du_at_lo=(VI.T @ cmin).tolist(), du_at_hi=(VI.T @ cmax).tolist())
        row['a_q'] = max(ahi, -alo) if st2 == ('OPTIMAL', 'OPTIMAL') else 'NOT_AVAILABLE'
        eps = [(pts[ro].get('eps_km_s') or [None] * len(vals['query_ids']))[q] for ro in roles]
        if all(isinstance(e, (int, float)) and not isinstance(e, bool) and math.isfinite(e) and e >= 0 for e in eps):
            e = max(eps)
            row['eps_q'] = e
            row['fd_noise'] = {'lo': float(np.sum(2 * e * np.abs(VI.T @ cmin) / h)),
                               'hi': float(np.sum(2 * e * np.abs(VI.T @ cmax) / h))}
        else:
            row['fd_noise'] = 'FD_NOISE_NOT_BOUNDED'
        row['non_discriminating'] = (row['a_q'] >= 0.5 * (hi - lo)) if row['a_q'] != 'NOT_AVAILABLE' else None
        out.append(row)
    return out, {'trust_radius': r, 'b_band_min': float(b_band.min()), 'hull_growth_tol': tol, 'm_id': m}


def check_values(vals, fd, n_rows=43):
    if vals.get('schema') != S_VALUES or len(vals.get('query_ids') or []) != n_rows:
        raise Refused('VALUES', 'schema %s with %d query ids required' % (S_VALUES, n_rows))
    pts = {p.get('role'): p for p in vals.get('points') or []}
    want = {'u_A': fd['u_A']}
    want.update({f['role']: f for f in fd['F']})
    if set(pts) != set(want) or len(vals['points']) != len(want):
        raise Refused('VALUES', 'points must be exactly %s' % sorted(want))
    akey = [m['key'] for m in fd['members'] if m['log_index'] == fd['u_A']['log_index']][0]
    for ro, p in pts.items():
        k = akey if ro == 'u_A' else want[ro]['key']
        if p.get('theta_key') != k or len(p.get('valid') or []) != n_rows or len(p.get('speeds_km_s') or []) != n_rows:
            raise Refused('VALUES', '%s is not bound to the fdplan theta or has the wrong row count' % ro)


def cmd_band(a):
    if not a.seal_sha256 or not a.seal_path:
        raise Refused('NO_SEAL', 'band values are step-5 output values (r3 L22): the r3a seal path and sha are required')
    read_pinned(a.seal_path, a.seal_sha256, 'r3a seal')
    E = mod('E')
    doc, rec, run = load_snapshot(a.snapshot, a.snapshot_sha256)
    fd = read_json_pinned(a.fdplan, a.fdplan_sha256, 'fdplan')
    if fd.get('schema') != S_FD or fd.get('record_file_sha256') != doc['record']['record_file_sha256']:
        raise Refused('FDPLAN', 'fdplan is not of this snapshot')
    vals = read_json_pinned(a.values, a.values_sha256, 'Phase-1 NGC values')
    check_values(vals, fd)
    L = linear_model(E, run)
    for f in fd['F']:
        same = [j for j in range(len(f['u'])) if j != f['axis'] and f['u_hex'][j] != fhex(L['uA'])[j]]
        if same or float.fromhex(f['u_hex'][f['axis']]) - float(L['uA'][f['axis']]) != f['du']:
            raise Refused('FDPLAN', 'F%d is not u_A + du e_k' % f['axis'])
    rows, meta = band_rows(E, L, vals, fd['F'])
    out = Out(a.out_dir)
    out.create()
    l1 = {'schema': S_L1, 'module': MODULE, 'label': BAND_LABEL, 'condition': BAND_CONDITION,
          'use': 'never a tier, a pattern or an uncertainty claim; no Gaussian propagation (the rule is the rectangle)',
          'seal': {'path': a.seal_path, 'sha256': a.seal_sha256}, 'snapshot_sha256': a.snapshot_sha256,
          'fdplan_sha256': a.fdplan_sha256, 'values_sha256': a.values_sha256, 'tau': tau_check(),
          'identified': L['I'], 'near_null': L['N'], 'meta': meta, 'rows': rows,
          'n_available': sum(1 for r_ in rows if r_['status'] == 'AVAILABLE')}
    out.write('L1_C2V001.json', l1)
    return 'OK', {'n_available': l1['n_available'], 'out_dir': out.dir, 'files': out.files}


# ------------------------------------------------------------------------------------------------ agree
def cmd_at0a(a):
    doc, rec, run = load_snapshot(a.snapshot, a.snapshot_sha256)
    cp = Campaign(a.config, a.config_sha256)
    out = Out(a.out_dir, [cp.work_dir])
    s0 = read_json_pinned(a.s0, a.s0_sha256, 'S0')
    rb = recorded_boundary(doc)
    m0 = rb['family'] == ['march0']
    fails = []
    try:
        w0, waves, entries = cp.prefix()
        kind, b, _c, bnd = cp.b_p1(entries)
        if (kind, b) != ('B_P1', doc['b_p1']):
            fails.append('B_P1 %s %s != snapshot %s' % (kind, b, doc['b_p1']))
        elif bnd['family'] != rb['family']:
            fails.append('first non-prefix family %s != snapshot %s' % (bnd['family'], rb['family']))
        else:
            _r, _c2, rsha = cp.snapshot_run(entries, b, rb['stage_reached'])
            if rsha != doc['replay']['run_canonical_sha256']:
                fails.append('replay run differs from the snapshot record')
        for e in run['evaluation_log']:
            ce = entries.get(cp.O.theta_key(e['theta_natural']))
            if ce is None or ce['theta'] != {k: float(v) for k, v in e['theta_natural'].items()}:
                fails.append('log %d theta is not a prefix cache entry' % e['index'])
        if w0 != rb['wave'] or waves[w0]['plan_sha256'] != rb['plan_sha256']:
            fails.append('march0 wave plan differs from the snapshot' if m0 else
                         'first non-prefix-family wave plan differs from the snapshot (now wave %s, recorded %s)'
                         % (w0, rb['wave']))
        nxt = cp.next_requested(entries)
        plan = [(c['key'], c['theta']) for c in waves[w0]['plan']['calls']]
        if nxt != plan:
            fails.append('next requested thetas (%d) differ from the committed %s plan (%d)'
                         % (len(nxt), 'march0' if m0 else 'first non-prefix-family', len(plan)))
    except Refused as exc:
        fails.append('prefix: %s' % exc)
    log = run['evaluation_log']
    if s0.get('schema') != S_S0 or len(s0.get('points') or []) != 1 + cp.ctx.n_varying or \
            s0.get('cache_id') != cp.ctx.cache_id:
        fails.append('S0 file malformed')
    else:
        for p in s0['points']:
            hit = [e for e in log if fhex(e['u']) == p['u_hex'] and e['purpose'] in ('seed', 'jacobian')]
            if len(hit) != 1 or {k: v.hex() for k, v in hit[0]['theta_natural'].items()} != p['theta_hex']:
                fails.append('S0 %s theta bits differ from the record' % p['role'])
    try:
        cp.runtime()
    except Refused as exc:
        fails.append(str(exc))
    res = {'schema': 'PHASE1_AT0A_C2V001', 'module': MODULE, 'snapshot_sha256': a.snapshot_sha256,
           's0_sha256': a.s0_sha256, 'outcome': 'PASS' if not fails else 'AGREEMENT_DEFECT', 'scope': 'prefix',
           'failures': fails}
    out.create()
    out.write('AT0A_C2V001.json', res)
    return ('OK' if not fails else 'AGREEMENT_DEFECT'), {'failures': fails, 'out_dir': out.dir, 'files': out.files}


def phase2_record(E, path, sha, registry):
    rec = read_json_pinned(path, sha, 'Phase-2 record')
    v = E.verify_calibration_record(record_path=path, registry_path=registry)
    if not v.get('ok') or rec.get('module_file_sha256') != ENGINE_PIN[1]:
        raise Refused('PHASE2_RECORD', v.get('reasons'))
    return rec['run']


def members_values(vals, run2, n_rows=43):
    O = mod('O')
    if vals.get('schema') != S_VALUES or len(vals.get('query_ids') or []) != n_rows:
        raise Refused('MEMBERS', 'schema %s with %d query ids required' % (S_VALUES, n_rows))
    adm = {p['log_index']: p for p in run2['exploration']['admitted_points']}
    out = {}
    for p in vals.get('points') or []:
        li = p.get('log_index')
        if p.get('role') != 'member' or li not in adm or O.theta_key(adm[li]['theta_natural']) != p.get('theta_key') \
                or li in out:
            raise Refused('MEMBERS', 'member %r is not a Phase-2 admitted point bound by theta key' % li)
        out[li] = p
    return out


def cmd_at0b(a):
    E = mod('E')
    doc, rec, run = load_snapshot(a.snapshot, a.snapshot_sha256)
    run2 = phase2_record(E, a.phase2_record, a.phase2_record_sha256, a.phase2_registry)
    v1 = read_json_pinned(a.values, a.values_sha256, 'Phase-1 values')
    mv = members_values(read_json_pinned(a.members, a.members_sha256, 'Phase-2 members'), run2)
    out = Out(a.out_dir)
    fails = []
    pa, pb = run['exploration']['primary_anchor'], (run2.get('exploration') or {}).get('primary_anchor') or {}
    if (run2.get('region') or {}).get('sha256') != run['region']['sha256'] or \
            E._canonical_bytes(run2.get('parameters')) != E._canonical_bytes(dict(run['parameters'], budget=run2.get('budget'))):
        fails.append('Phase-2 record region or engine parameters (other than the budget) differ from Phase 1')
    if pb.get('log_index') != pa['log_index'] or fhex(pb.get('u') or []) != fhex(pa['u']):
        fails.append('Phase-2 primary anchor is not u_A bitwise')
    b, log2 = doc['b_p1'], run2.get('evaluation_log') or []
    if len(log2) < b or any(E._canonical_bytes(x) != E._canonical_bytes(y) for x, y in zip(log2[:b], run['evaluation_log'])):
        fails.append('Phase-2 first B_P1 log entries differ from Phase 1')
    p1 = [p for p in v1.get('points') or [] if p.get('role') == 'u_A']
    p2 = mv.get(pa['log_index'])
    if len(p1) != 1 or p2 is None or not isinstance(p1[0].get('result_pin'), dict) or \
            (p1[0]['result_pin'] or {}).get('sha256') != (p2.get('result_pin') or {}).get('sha256'):
        fails.append('the u_A member does not re-bind to the same result file by sha')
    res = {'schema': 'PHASE1_AT0B_C2V001', 'module': MODULE, 'outcome': 'PASS' if not fails else 'AGREEMENT_DEFECT',
           'failures': fails, 'phase2_record_sha256': a.phase2_record_sha256, 'snapshot_sha256': a.snapshot_sha256,
           'members_sha256': a.members_sha256.lower()}   # A149 item 2: the sha of the members bytes read above
    out.create()
    out.write('AT0B_C2V001.json', res)
    return ('OK' if not fails else 'AGREEMENT_DEFECT'), {'failures': fails, 'out_dir': out.dir, 'files': out.files}


def band_region(L):
    """A144 R1: the band region's rows, built exactly as band_rows builds them (A, b_band; a test proves bitwise
    equality with the arrays band_rows passes to the LP), plus the row slice of each family:
    LINEAR_DDO = [0, 2N), BOX = [2N, 2N + 2d), TRUST_RADIUS = [2N + 2d, 2N + 2d + 2 m_id)."""
    import numpy as np
    VI, m = L['VI'], len(L['I'])
    SVI = L['S'] @ VI.T
    eye = np.eye(m)
    r = float(L['P']['max_repair_step']) / math.sqrt(m)
    A = np.vstack([SVI, -SVI, VI.T, -VI.T, eye, -eye])
    b_band = np.concatenate([L['zrow'] - L['qA'], L['zrow'] + L['qA'], 1.0 - L['uA'], L['uA'], np.full(m, r), np.full(m, r)])
    nr, nd = SVI.shape[0], VI.shape[1]
    fam = {'LINEAR_DDO': slice(0, 2 * nr), 'BOX': slice(2 * nr, 2 * nr + 2 * nd),
           'TRUST_RADIUS': slice(2 * nr + 2 * nd, 2 * nr + 2 * nd + 2 * m)}
    return A, b_band, fam


def region_violation(E, region, c):
    """A144 R1 row test with the band LP's own feasibility semantics: row i is violated iff
    (A c)_i - max(b_band_i, 0) > E._LP_EPS (the clip is _lp_max's, engine L1787; the tolerance is engine L181).
    Returns (violated families in the order TRUST_RADIUS, BOX, LINEAR_DDO, {family: max_i of that difference})."""
    import numpy as np
    A, b, fam = region
    v = A @ c - np.maximum(b, 0.0)
    viol = [f for f in REGION_FAMILIES if bool(np.any(v[fam[f]] > E._LP_EPS))]
    return viol, {f: float(np.max(v[fam[f]])) for f in REGION_FAMILIES}


def band_region_extent(E, L, lp=None):
    """A144 R2 (print only): per identified c_j, [min, max] over the band region's own rows (E._lp_max) with both
    statuses; band_region_single_point (True iff every extent is OPTIMAL and exactly [0.0, 0.0]; 'NOT_AVAILABLE' if
    any program is not OPTIMAL); the reason (BOX_CORNER iff the box rows alone give [0.0, 0.0] on every j, else
    OTHER_ROWS; None unless the band region is a single point)."""
    import numpy as np
    A, b, fam = band_region(L)
    m = len(L['I'])

    def extents(A_, b_):
        res = []
        for j in range(m):
            w = np.zeros(m)
            w[j] = 1.0
            lo, hi, _cmin, _cmax, st = lp_pair(E, A_, b_, w, lp)
            res.append({'direction': L['I'][j], 'extent': [lo if st[0] == 'OPTIMAL' else 'NOT_AVAILABLE',
                                                           hi if st[1] == 'OPTIMAL' else 'NOT_AVAILABLE'],
                        'lp_status': [st[0], st[1]]})
        return res

    def single(res):
        if any(s != 'OPTIMAL' for x in res for s in x['lp_status']):
            return 'NOT_AVAILABLE'
        return all(x['extent'][0] == 0.0 and x['extent'][1] == 0.0 for x in res)
    ext = extents(A, b)
    sp = single(ext)
    reason = None
    if sp is True:
        reason = 'BOX_CORNER' if single(extents(A[fam['BOX']], b[fam['BOX']])) is True else 'OTHER_ROWS'
    return ext, sp, reason


def band_region_box_only_extent(E, L, lp=None):
    """A149 item 3 (print only): per identified c_j, [min, max] over the band region's BOX rows alone (the same rows,
    objectives and E._lp_max programs band_region_extent's reason reads), with both statuses, in band_region_extent's
    form.  It never refuses and changes no row, no extent, no single-point value and no reason: the single-point rule
    stays exact.  It shows BOX_CORNER geometry when an LP tie leaves the full-region extent a few ulps off 0.0."""
    import numpy as np
    A, b, fam = band_region(L)
    A_, b_ = A[fam['BOX']], b[fam['BOX']]
    m = len(L['I'])
    res = []
    for j in range(m):
        w = np.zeros(m)
        w[j] = 1.0
        lo, hi, _cmin, _cmax, st = lp_pair(E, A_, b_, w, lp)
        res.append({'direction': L['I'][j], 'extent': [lo if st[0] == 'OPTIMAL' else 'NOT_AVAILABLE',
                                                       hi if st[1] == 'OPTIMAL' else 'NOT_AVAILABLE'],
                    'lp_status': [st[0], st[1]]})
    return res


def member_eps(eps_list, q):
    """(eps_m as float, None) for a bounded entry; (None, flag_reason) otherwise (A144 R3)."""
    if not isinstance(eps_list, list) or q >= len(eps_list):
        return None, 'MEMBER_EPS_LIST_MISSING'
    e = eps_list[q]
    if e is None:
        return None, 'MEMBER_EPS_NONE'
    if isinstance(e, bool):
        return None, 'MEMBER_EPS_BOOL'
    if not isinstance(e, (int, float)):
        return None, 'MEMBER_EPS_NOT_A_NUMBER'
    try:
        finite = math.isfinite(e)
    except OverflowError:   # A149 item 1: an int beyond the float range (e.g. 10**400) is non-finite, flagged per pair
        finite = False
    if not finite:
        return None, 'MEMBER_EPS_NON_FINITE'
    if e < 0:
        return None, 'MEMBER_EPS_NEGATIVE'
    return float(e), None


def check_member_eps(mv, n_rows=43):
    """A144 R3 input contract, at cmd_at1 only (members_values is shared with at0b and unchanged): every member point
    of the Phase-2 members file carries eps_km_s, a list of exactly n_rows entries; else MEMBERS is refused."""
    bad = [li for li, p in sorted(mv.items()) if not isinstance(p.get('eps_km_s'), list) or len(p['eps_km_s']) != n_rows]
    if bad:
        raise Refused('MEMBERS', 'member point(s) %s lack eps_km_s as a list of %d entries (A144 R3: the member point '
                      'own EPS certificate)' % (bad[:12], n_rows))


def at1_rows(E, L, l1, run2, mv, qids, lp=None):
    """AT-1 per (member, row), the A144 R1 categories, the R3 e_q, and the always-reported target-free lines."""
    import numpy as np
    m = len(L['I'])
    VN = L['V'][L['N']] if L['N'] else np.zeros((0, len(L['uA'])))
    rows1 = {x['id']: x for x in l1['rows']}
    region = band_region(L)
    du = np.array([float(f) for f in l1['fd_du']])
    h = np.abs(du)
    fails, resid, widths, eqs, pmp = [], [], {}, [], []
    untested = sorted(q for q, x in rows1.items() if x.get('status') != 'AVAILABLE' or x.get('a_q') == 'NOT_AVAILABLE')
    for li, p in sorted(mv.items()):
        u = np.array([pt for pt in run2['exploration']['admitted_points'] if pt['log_index'] == li][0]['u'])
        d = u - L['uA']
        c, n = L['VI'] @ d, VN @ d
        viol, maxv = region_violation(E, region, c)   # A144 R1
        cat = REGION_CATEGORY[viol[0]] if viol else 'NGC_NONLINEAR'
        coef = abs(1.0 - float(np.sum(d / du))) + float(np.sum(np.abs(d) / h))   # A144 R3: the eps_q coefficient
        for q, qid in enumerate(qids):
            b1 = rows1.get(qid) or {}
            g = p['speeds_km_s'][q]
            if p['valid'][q] is not True or not isinstance(g, (int, float)) or isinstance(g, bool) or not math.isfinite(g):
                continue
            widths.setdefault(qid, []).append(g)
            if qid in untested:
                continue
            K = np.array(b1['K_q'])
            shift = float(K @ (VN.T @ n)) if len(n) else 0.0
            e, eq, eps_m, flag, why = 0.0, 'FD_NOISE_NOT_BOUNDED', None, 'FD_NOISE_NOT_BOUNDED', 'NO_ROW_EPS_Q'
            if isinstance(b1.get('fd_noise'), dict):   # A144 R3 (E_A133_2(b))
                eps_m, why = member_eps(p.get('eps_km_s'), q)
                bounded = float(b1['eps_q']) * coef
                if eps_m is None:
                    e = eq = bounded
                    flag = 'MEMBER_POINT_NOISE_NOT_BOUNDED'
                    pmp.append({'log_index': li, 'id': qid, 'flag_reason': why})
                else:
                    e = eq = eps_m + bounded
                    flag = None
            eqs.append({'log_index': li, 'id': qid, 'e_q': eq, 'eps_m': eps_m, 'flag': flag, 'flag_reason': why})
            aq = b1['a_q']
            lo, hi = b1['lo'] - aq - e + shift, b1['hi'] + aq + e + shift
            resid.append({'log_index': li, 'id': qid, 'ngc_linearity_residual': g - b1['g_A'] - float(K @ d)})
            if not lo <= g <= hi:
                excess = (lo - g) if g < lo else (g - hi)
                kc = float(K @ (L['VI'].T @ c))
                geo = ((b1['lo'] - b1['g_A']) - kc) if g < lo else (kc - (b1['hi'] - b1['g_A']))
                fails.append({'log_index': li, 'id': qid, 'excess': excess,
                              'norm_n': float(np.linalg.norm(n)), 'category': cat, 'flag': flag, 'flag_reason': why,
                              'region_rows_violated': list(viol), 'region_max_violation': dict(maxv),
                              'geometric_part': geo, 'residual_part': excess - geo})
    env = {q: {'phase2_envelope_width': max(v) - min(v),
               'phase1_band_width': rows1.get(q, {}).get('width', 'NOT_AVAILABLE')} for q, v in widths.items()}
    tau = TAU_OVER_SIGMA * L['sig']
    lin_dev = max([float(np.max(np.abs(np.array([pt['prediction']['speeds_km_s'][rr] for rr in L['rows']]) -
                                       (L['fA'] + L['J'] @ (np.array(pt['u']) - L['uA']))) / tau))
                   for pt in run2['exploration']['admitted_points']] or [0.0])
    A = np.vstack([L['S'] @ L['VI'].T, -(L['S'] @ L['VI'].T), L['VI'].T, -L['VI'].T])
    bb = np.concatenate([L['zrow'] - L['qA'], L['zrow'] + L['qA'], 1.0 - L['uA'], L['uA']])
    proj = []
    for j, k in enumerate(L['I']):
        w = np.zeros(m)
        w[j] = 1.0
        lo, hi, _a, _b, st = lp_pair(E, A, bb, w)
        pr = [float((np.array(pt['u']) - L['uA']) @ L['V'][k]) for pt in run2['exploration']['admitted_points']]
        res_ = float(L['P']['march_step']) * 2.0 ** -3
        proj.append({'direction': k, 'phase2_range': [min(pr), max(pr)], 'linear_region': [lo, hi], 'lp_status': st,
                     'resolution_u': res_, 'beyond_linear_region': bool(min(pr) < lo - res_ or max(pr) > hi + res_)})
    ext, single, reason = band_region_extent(E, L, lp)   # A144 R2 (print only)
    box_ext = band_region_box_only_extent(E, L, lp)   # A149 item 3 (print only)
    return fails, {'rows_not_tested_phase1_not_available': untested, 'e_q_per_member_row': eqs,
                   'rows_fd_noise_not_bounded': sorted(q for q, x in rows1.items() if x.get('fd_noise') == 'FD_NOISE_NOT_BOUNDED'),
                   'pairs_member_point_noise_not_bounded': pmp,
                   'ngc_linearity_residuals': resid, 'envelope_vs_band_width': env,
                   'max_ddo_linearity_deviation_over_tau': lin_dev, 'identified_projection_vs_linear_region': proj,
                   'band_region_extent': ext, 'band_region_single_point': single,
                   'band_region_single_point_reason': reason, 'band_region_box_only_extent': box_ext}


def cmd_at1(a):
    E = mod('E')
    doc, rec, run = load_snapshot(a.snapshot, a.snapshot_sha256)
    l1 = read_json_pinned(a.l1, a.l1_sha256, 'L1')
    fd = read_json_pinned(a.fdplan, a.fdplan_sha256, 'fdplan')
    if l1.get('schema') != S_L1 or l1.get('snapshot_sha256') != a.snapshot_sha256 or l1.get('fdplan_sha256') != a.fdplan_sha256:
        raise Refused('L1', 'L1 is not of this snapshot and fdplan')
    if l1.get('module') != MODULE:   # A144 custody: at1 reads only an L1 written by this module's band
        raise Refused('L1', 'L1 module %r is not %s (A144)' % (l1.get('module'), MODULE))
    l1 = dict(l1, fd_du=[f['du'] for f in fd['F']])
    at0 = [read_json_pinned(p, s, lab) for p, s, lab in ((a.at0a, a.at0a_sha256, 'AT-0a'), (a.at0b, a.at0b_sha256, 'AT-0b'))]
    run2 = phase2_record(E, a.phase2_record, a.phase2_record_sha256, a.phase2_registry)
    mvals = read_json_pinned(a.members, a.members_sha256, 'Phase-2 members')
    if at0[1].get('members_sha256') != a.members_sha256.lower():   # A149 item 2: the members file AT-0b read
        raise Refused('MEMBERS', '--members sha256 %s is not the members_sha256 %r recorded by AT-0b (A149 item 2)'
                      % (a.members_sha256.lower(), at0[1].get('members_sha256')))
    mv = members_values(mvals, run2)
    check_member_eps(mv, len(mvals['query_ids']))   # A144 R3 input contract (at1 only; at0b is not affected)
    if [r['id'] for r in l1['rows']] != list(mvals['query_ids']):
        raise Refused('MEMBERS', 'query ids differ from L1')
    sel2 = v003g_members(Campaign(a.config, a.config_sha256, prepare=False).ctx, run2, a.interior_count)
    if sorted(p['log_index'] for p in sel2['points']) != sorted(mv):
        raise Refused('MEMBERS', 'the values do not cover exactly the Phase-2 v003g PRIMARY members')
    L = linear_model(E, run)
    out = Out(a.out_dir)
    fails, rep = at1_rows(E, L, l1, run2, {li: p for li, p in mv.items() if p.get('member_valid') is True},
                          mvals['query_ids'])
    at0_ok = all(x.get('outcome') == 'PASS' and x.get('snapshot_sha256') == a.snapshot_sha256 for x in at0) and \
        at0[0].get('schema') == 'PHASE1_AT0A_C2V001' and at0[1].get('schema') == 'PHASE1_AT0B_C2V001' and \
        at0[1].get('phase2_record_sha256') == a.phase2_record_sha256
    outcome = 'AGREEMENT_DEFECT' if not at0_ok else ('COVERED' if not fails else 'SUPERSEDED')
    res = {'schema': 'PHASE1_AT1_C2V001', 'module': MODULE, 'outcome': outcome, 'at0': [x.get('outcome') for x in at0],
           'e_q_reading': E_Q_READING,
           'failing': fails, 'non_discriminating_rows': [r['id'] for r in l1['rows'] if r.get('non_discriminating')],
           'reported': rep, 'record_of_result': 'Phase 2 in every outcome',
           'not_computed_here': 'headlines, E3 lines, pattern classifications and tier changes come from the sealed r3a '
                                'scoring of both manifests (target data); this tool is target-free'}
    out.create()
    out.write('AT1_C2V001.json', res)
    return ('OK' if outcome != 'AGREEMENT_DEFECT' else 'AGREEMENT_DEFECT'), {'outcome': outcome, 'n_failing': len(fails),
                                                                            'out_dir': out.dir, 'files': out.files}


# ------------------------------------------------------------------------------------------------ CLI
def _o_canon(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', choices=('snapshot', 'handoff', 'fdplan', 'band', 'agree'))
    ap.add_argument('test', nargs='?', choices=('at0a', 'at0b', 'at1'))
    for k in ('config', 'snapshot', 'provenance', 'root_fields', 'seal_path', 'fdplan', 'values', 's0', 'phase2_record',
              'phase2_registry', 'members', 'l1', 'at0a', 'at0b', 'out_dir'):
        ap.add_argument('--' + k.replace('_', '-'))
        if k not in ('phase2_registry', 'out_dir', 'seal_path'):
            ap.add_argument('--' + k.replace('_', '-') + '-sha256', dest=k + '_sha256')
    ap.add_argument('--seal-sha256', dest='seal_sha256')
    ap.add_argument('--interior-count', type=int)
    ap.add_argument('--s0-only', action='store_true')
    a = ap.parse_args(argv)
    try:
        fn = {'snapshot': cmd_snapshot, 'handoff': cmd_handoff, 'fdplan': cmd_fdplan, 'band': cmd_band}.get(a.command)
        if a.command == 'agree':
            fn = {'at0a': cmd_at0a, 'at0b': cmd_at0b, 'at1': cmd_at1}.get(a.test)
            if fn is None:
                raise Refused('USAGE', 'agree needs at0a | at0b | at1')
        status, out = fn(a)
    except Refused as exc:
        status, out = ('NOT_READY' if exc.code == 'NOT_READY' else 'REFUSED'), {'reason': str(exc)}
    except Exception as exc:   # noqa: BLE001 -- fail closed: an unanticipated input shape is a refusal, never a pass
        status, out = 'REFUSED', {'reason': 'INTERNAL_ERROR: %s: %s' % (type(exc).__name__, str(exc)[:400])}
    print(json.dumps(dict(out, status=status), indent=1, sort_keys=True, default=str))
    return EXIT[status]


if __name__ == '__main__':
    sys.exit(main())
