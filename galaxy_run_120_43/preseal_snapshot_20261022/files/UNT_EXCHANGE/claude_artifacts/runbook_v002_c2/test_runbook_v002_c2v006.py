#!/usr/bin/env python3
"""Synthetic MUST_PASS / MUST_FAIL suite for roster_builder_c2v006 and the RUNBOOK_V002 (c2v006) checks.

Usage: python3 -I -B test_runbook_v002_c2v006.py --record-dir DIR      (DIR must not exist)

Port from c2v005 (this file is test_runbook_v002_c2v005.py with the changes below): all 149 c2v005 cases are kept,
in c2v005's order. Root ruling A173 on OI-A1, ruling (a): every root-written record carries `schema` set to its
contract name, with classifier A's exact key sets. Ported cases that asserted the c2v005 record forms now assert the
c2v006 forms: X01 (the gate list is exactly {schema, gates}), X02 (the TSR flag record is V003, with `schema`; its id
now says V003), and the synthetic TSR flag records of SynTsr carry `schema` (T02-T04, T06, T07). One ported case
changes expectation: X06 (a FULL build's list plus `schema: GATE_STATUS_LIST_C4V001`) was MUST_FAIL
GATE_STATUS_LIST_DEFECT and is now MUST_PASS, since that list is exactly the c2v006 builder's own list; its id suffix
says so. The production flag record read by T01, T05, T08, T09, X02 and the S cases is ROOT_TSR_FLAG_RECORD_V003.json
(V002 plus `schema`). New in c2v006: Y01-Y11 (the builder constants equal A's contracts; the gate list with schema
passes check-gate-list as a command; V003 is V002 plus schema, passes tsr-check and is rewritten byte for byte by the
tsr-record command; MUST_FAIL: the gate list without schema (the c2v005 form), with a wrong schema string, with an
extra key; the TSR record without schema (synthetic, and the production V002 through the tsr-check command), with a
wrong schema string, with an extra key; seal-check refuses V002 as the sealed flag record). The program files read
are those of c2v005 plus ROOT_TSR_FLAG_RECORD_V003.json; ROOT_TSR_FLAG_RECORD_V002.json is read as the c2v005 form.

The c2v005 docstring follows.

Port from c2v004 (this file is test_runbook_v002_c2v004.py with the changes below): all 137 c2v004 cases are kept.
Two change expectation under root ruling G29 (byte-identical cut records of distinct calls are allowed; a cut record
is bound to its call by residence): H02 (a byte copy of M000's cut record inside M001's own run directory) and H06
(two calls' byte-identical cut records naming no call) were MUST_FAIL CUT_RECORD_BORROWED by sha256 and are now
MUST_PASS; their id suffixes say so. H08's docstring no longer cites a sha256 check for cut records (its body and
expectation are unchanged). The fixture form of c2v004 (a synthetic cut record names its call) is kept; it is no
longer needed by the builder. New in c2v005: J01-J12 (the re-verify probes Q4b, Q4, Q5 as MUST_FAIL; G29 residence:
a cut record outside its own run directory, inside another roster call's terminal or non-terminal run directory,
inside an OTHER call's run directory; G29 identity: a byte-identical cut-record pair as one hard-linked file; byte-
identical cut records building in Phase 2; C38 and the content rule in both call orders; a failure record outside
its own run directory). Hard links are made with os.link inside the work directory only.

The c2v004 docstring follows.

Port from c2v003 (this file is test_runbook_v002_c2v003.py with the changes below; the docstring that follows is
c2v003's): all 124 c2v003 cases are kept under their ids and expectations. Fixture change: a synthetic cut record now
carries its call (alternative:kind:key) in classification_evidence, so the cut records of distinct calls differ in
bytes (c2v004 refuses a cut record whose sha256 is another call's; whether production cut records are call-specific
is root ruling G29, and H06 tests the refusal when they are not). New in c2v004: H01-H13 (one run file serves one
call: file identity (st_dev, st_ino) for receipts, results and cut records; sha256 for cut records and FINISHED
results; byte-identical failure records of failed calls pass). Hard links are made with os.link inside the work
directory only.


Every fixture is synthetic and is written under DIR/work: synthetic slots, query manifest, GL-node record, route-B
config, STAGE0 grid, selection, spec, gates, cut records, receipts (with the rule-(c) evidence keys and, new in
c2v003, the call-binding keys spec_sha256 and theta_sha256), launch registries, forward results, V006 copies,
pre-launch records and the step-7 ledger root, with synthetic pins. The only program files read are: the pinned
freeze module v003g (executed from its verified bytes, with its slots and node constants patched to the synthetic
fixtures, so the real slots are never opened), the root TSR flag records ROOT_TSR_FLAG_RECORD_V001.json (c2v001,
unchanged; the derivation input) and ROOT_TSR_FLAG_RECORD_V002.json (c2v003, classifier A's schema), and the
target-free compare, N1 and node records they pin. A read guard refuses any other path in-process. No NGC3198
target, no slots file and no query manifest of the program is opened. Commands that load the freeze module (build,
pass) run in-process under the guard; only commands that never load it (build with a bad input pin,
check-gate-list, seal-check, tsr-check, step7, and the removed pass-record) run as subprocesses.

Port from c2v002: all 96 c2v002 cases are kept under their ids, with fixtures moved to the c2v003 input forms (the
launch registry, the binding keys on every receipt, the ledger root, the classifier-A record schemas); the cases
whose c2v002 object no longer exists in c2v003 (T01, T04, T05, T08, T09 on the V001 record form; M01-M09 on the
c2v002 list form) test the same property on its c2v003 successor and say so in their docstrings.
"""

import copy
import hashlib
import io
import json
import math
import os
import subprocess
import sys
import traceback
import types
import contextlib

HERE = os.path.dirname(os.path.realpath(__file__))
BUILDER_PATH = os.path.join(HERE, 'roster_builder_c2v006.py')
TSR_V001_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/'
                 'ROOT_TSR_FLAG_RECORD_V001.json')
TSR_V001_SHA = '61bd8a83492e96ffb22d576a93b65d14c047f92e3be4bbfc2c0120f439cf7edc'
TSR_RECORD_PATH = os.path.join(HERE, 'ROOT_TSR_FLAG_RECORD_V003.json')
TSR_RECORD_SHA = '7d3c1eb915cd9a85b1a9dab388e6a3fb6c218ef3d4e8e6f2dc726bea15c54070'
# c2v006: the c2v005 production record (no `schema` key), read only to show it is refused
TSR_V002_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/runbook_v002_c2/'
                 'ROOT_TSR_FLAG_RECORD_V002.json')
TSR_V002_SHA = 'c9d8ab4573278f2d325bc5fe50e396e35e9981f0561cfa20e61e8a215bb5cea0'
V003G_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/'
              'prediction_freeze_c2v003g_cx3v001.py')
V003G_SHA = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
_B = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
TSR_FILES = {_B + 'ngc_ntest_eval_cx/out/K32_COMPARE_COMPLETE_V001.json',
             _B + 'ngc_ntest_eval_cx/out/K32_RECORDS_COMPLETE_V001_N1.json',
             _B + 'ngc_route_tail_readiness_cx3/v011/cx3v005/REGISTERED_ROUTE_B_GL_NODES_CX3V001.json'}
KPC_M = 3.085677581491367e19
PRIMARY, OK_ALT, STAGE0 = 'BR_A_F10_PRIMARY', 'ORIGINAL_K', 'STAGE0_GRID_OUTER'
IDS = ['SYN-Q%02d' % i for i in range(1, 44)]
RAD_TEXT = ['%.2f' % float(i) for i in range(1, 44)]
GL4_KPC = [(k + 0.5) * 0.45 for k in range(100)]
GL10_KPC = [(k + 0.5) * 0.18 for k in range(250)]
RECEIPT_KEYS = {'status': 'receipt_status', 'time_utc': 'receipt_written_utc', 'spec_sha256': 'spec_sha256',
                'theta_sha256': 'theta_sha256', 'rss_cap_bytes': 'rss_cap_bytes', 'wall_cap_s': 'wall_cap_s', 'host_ram_bytes': 'host_ram_bytes',
                'other_ngc_processes_max': 'other_ngc_processes_max', 'output_cap_bytes': 'output_cap_bytes'}
CLASSES = {'FINISHED': 'FINISHED', 'FAILED_SOLVER': 'FAILED', 'WALL_CAP': 'CAP', 'RSS_CAP': 'CAP',
           'OUTPUT_CAP_STOP': 'OUTPUT_CAP', 'INFRA_SPAWN': 'INFRA', 'PLANNED_KILL': 'PLANNED_STOP'}
RAM = 128 * 2 ** 30
DROP = '__DROP_THIS_RECEIPT_KEY__'
ROLES = ['anchor', 'hull_vertex', 'centroid_nearest']
US = [[0.2, 0.3], [0.9, 0.6], [0.55, 0.45]]
LOGS = [0, 3, 5]
PROJ = [[0.2], [0.9], [0.55]]
SEL = {'ok': True, 'admitted_region': {'centroid_identified': [0.5], 'near_null_directions': [
    {'index': 1, 'vector_u': [0.0, 1.0], 'ddo_sensitivity_sigma_per_unit_t': None}]}}
NULL_RULE = {'mode': 'box_ends'}
COORDS = [
    {'name': 'syn_a', 'transform': 'linear', 'lower': 0.0, 'upper': 1.0, 'role': 'free', 'trial_value': 0.5,
     'units': 'dimensionless', 'scope': 'shared', 'kind': 'other', 'reference_value': None, 'sensitivity': None},
    {'name': 'syn_b', 'transform': 'log', 'lower': 0.1, 'upper': 10.0, 'role': 'free', 'trial_value': 1.0,
     'units': 'dimensionless', 'scope': 'shared', 'kind': 'other', 'reference_value': None, 'sensitivity': None},
    {'name': 'syn_ngc_d', 'transform': 'linear', 'lower': 12.0, 'upper': 15.0, 'role': 'nuisance',
     'trial_value': 13.8, 'units': 'Mpc', 'scope': 'ngc3198_nuisance', 'kind': 'distance', 'reference_value': 13.8,
     'sensitivity': {'mode': 'box_ends'}},
    {'name': 'syn_ngc_i', 'transform': 'linear', 'lower': 65.0, 'upper': 80.0, 'role': 'nuisance',
     'trial_value': 72.0, 'units': 'deg', 'scope': 'ngc3198_nuisance', 'kind': 'inclination',
     'reference_value': None, 'sensitivity': {'mode': 'step', 'step': 2.0}},
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def tsha(theta):
    """The exact-theta key, computed here independently of the builder: sha256 of the v003g canonical JSON bytes."""
    return sha(json.dumps(theta, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8'))


def spec_of(alt, theta_key):
    """The synthetic spec sha registered at launch for the call (alternative, exact theta)."""
    return sha(('SYN-SPEC|%s|%s' % (alt, theta_key)).encode())


def other_tsha(label):
    return sha(('SYN-OTHER-THETA|' + label).encode())


def other_spec(label):
    return sha(('SYN-OTHER-SPEC|' + label).encode())


def ev(solo=True, raised=False, spec=None, wall=43200, out_cap=96 * 2 ** 30, rss=None):
    """Rule-(c) receipt evidence. raised: the rerun form (RSS cap at RAM, wall cap twice the first attempt's). The
    receipt's spec_sha256 is the call's registered spec (filled in by Base.call) unless `spec` overrides it."""
    d = {'rss_cap_bytes': rss if rss is not None else (RAM if raised else 64 * 2 ** 30),
         'wall_cap_s': 2 * wall if raised else wall, 'host_ram_bytes': RAM,
         'other_ngc_processes_max': 0 if solo else 2, 'output_cap_bytes': out_cap}
    if spec is not None:
        d['spec_sha256'] = spec
    return d


def load_module(path, name, expect_sha=None):
    with open(path, 'rb') as f:
        raw = f.read()
    if expect_sha is not None and sha(raw) != expect_sha:
        raise SystemExit('pinned module bytes differ: ' + path)
    mod = types.ModuleType(name)
    mod.__file__ = os.path.realpath(path)
    exec(compile(raw, mod.__file__, 'exec'), mod.__dict__)
    return mod


class Env:
    """Holds the work directory, the builder module and a factory of patched freeze modules."""

    def __init__(self, work):
        self.work = work
        self.allowed = {os.path.realpath(p) for p in TSR_FILES | {TSR_RECORD_PATH, TSR_V001_PATH, TSR_V002_PATH}}
        self.rb = load_module(BUILDER_PATH, 'rb')
        self.rb._read_regular = self._guard(self.rb._read_regular)
        self.n = 0

    def _guard(self, fn):
        work = os.path.realpath(self.work)

        def guarded(path, *a):
            rp = os.path.realpath(path)
            if not (rp.startswith(work + os.sep) or rp in self.allowed):
                raise AssertionError('READ_GUARD: a test read outside the synthetic work dir: ' + rp)
            return fn(path, *a)
        return guarded

    def fm(self, slots_pin, nodes_pin):
        m = load_module(V003G_PATH, 'v003g_patched', V003G_SHA)
        m.ROOT_SLOTS_PATH, m.ROOT_SLOTS_SHA256 = slots_pin['path'], slots_pin['sha256']
        m.REGISTERED_GL_NODES_PATH, m.REGISTERED_GL_NODES_SHA256 = nodes_pin['path'], nodes_pin['sha256']
        m._read_regular = self._guard(m._read_regular)
        return m

    def dir(self, *parts):
        p = os.path.join(self.work, *parts)
        os.makedirs(p, exist_ok=True)
        return os.path.realpath(p)

    def fresh(self, prefix):
        self.n += 1
        return os.path.join(self.dir('out'), '%s_%03d' % (prefix, self.n))


def wjson(path, obj):
    raw = (json.dumps(obj, indent=1, sort_keys=True) + '\n').encode()
    with open(path, 'xb') as f:
        f.write(raw)
    return {'path': os.path.realpath(path), 'sha256': sha(raw)}


def wbytes(path, raw):
    with open(path, 'xb') as f:
        f.write(raw)
    return {'path': os.path.realpath(path), 'sha256': sha(raw)}


def pin(path):
    with open(path, 'rb') as f:
        return {'path': os.path.realpath(path), 'sha256': sha(f.read())}


def hlink(src_pin, dst_dir, name):
    """c2v004: a hard link (os.link) to src_pin's file in dst_dir: the same file (st_dev, st_ino), another path."""
    dst = os.path.join(dst_dir, name)
    os.link(src_pin['path'], dst)
    a, b = os.stat(src_pin['path']), os.stat(dst)
    assert (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino) and os.path.realpath(dst) != src_pin['path']
    return {'path': os.path.realpath(dst), 'sha256': src_pin['sha256']}


def bcopy(src_pin, dst_dir, name):
    """c2v004: a byte copy of src_pin's file in dst_dir: another file with the same bytes."""
    with open(src_pin['path'], 'rb') as f:
        p = wbytes(os.path.join(dst_dir, name), f.read())
    a, b = os.stat(src_pin['path']), os.stat(p['path'])
    assert (a.st_dev, a.st_ino) != (b.st_dev, b.st_ino) and p['sha256'] == src_pin['sha256']
    return p


def jload(path):
    with open(path) as f:
        return json.load(f)


FORBIDDEN_VALUE_KEYS = {'reference_speed_km_s', 'box_limited_band_low_km_s', 'box_limited_band_high_km_s',
                        'max_abs_delta_km_s', 'band_low_km_s', 'band_high_km_s', 'pointwise_envelope', 'envelopes',
                        'member'}


def assert_value_free(obj, where):
    """No NGC output value: no value-bearing key, value arrays all null, and no float in the synthetic speed range
    (synthetic speeds are 100 + 0.25 j + seed <= 132.5; no theta, displacement or u reaches 99)."""
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in FORBIDDEN_VALUE_KEYS:
                    raise AssertionError('%s: value key %s at %s' % (where, k, path))
                if k in ('speeds_km_s', 'delta_from_reference_km_s') and v is not None and \
                        any(x is not None for x in v):
                    raise AssertionError('%s: non-null %s at %s' % (where, k, path))
                walk(v, path + '.' + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, '%s[%d]' % (path, i))
        elif isinstance(o, float) and 99.0 <= o <= 140.0:
            raise AssertionError('%s: a float in the synthetic NGC value range at %s' % (where, path))
    walk(obj, '')


# --------------------------------------------------------------------------------------------------------------
# synthetic fixtures
# --------------------------------------------------------------------------------------------------------------

class Base:
    def __init__(self, env, name, stage0_evaluated):
        self.env = env
        d = env.dir('base_' + name)
        self.d = d
        self.sens_tsha = {}      # entry_id -> exact-theta key of the saved value-free sensitivity plan (set by P2)
        prof = wbytes(os.path.join(d, 'profile.dat'), b'synthetic profile source\n')
        cfg = wjson(os.path.join(d, 'route_b_config.json'), {'fields': {
            'radial.source_gauss_order': {'value': 4}, 'radial.n_columns': {'value': 100},
            'source.profile': {'value': prof}}})
        self.nodes = wjson(os.path.join(d, 'gl_nodes.json'), {
            'schema': 'NGC_REGISTERED_ROUTE_B_GL_NODES_CX3V001', 'kpc_m': KPC_M, 'method': 'synthetic',
            'date_u': 'synthetic', 'sources': {'profile': prof},
            'orders': {'4': {'source_gauss_order': 4, 'registered_n_columns': 100, 'radii_kpc': GL4_KPC,
                             'radii_m': [r * KPC_M for r in GL4_KPC]},
                       '10': {'source_gauss_order': 10, 'registered_n_columns': 250, 'radii_kpc': GL10_KPC,
                              'radii_m': [r * KPC_M for r in GL10_KPC]}}})
        grid = wbytes(os.path.join(d, 'stage0_grid.bin'), b'synthetic stage0 grid\n')
        evd, ne = 'EVALUATED_BEFORE_FREEZE', 'NOT_EVALUATED_BEFORE_FREEZE'
        declared = [
            {'name': PRIMARY, 'kind': 'state', 'description': 'synthetic primary', 'status': evd},
            {'name': OK_ALT, 'kind': 'state', 'description': 'synthetic twin', 'status': evd},
            {'name': 'ML_3p6_0.4', 'kind': 'source', 'description': 'synthetic', 'status': ne},
            {'name': 'ML_3p6_0.6', 'kind': 'source', 'description': 'synthetic', 'status': ne},
            {'name': 'GL10_SOURCE_GAUSS_ORDER', 'kind': 'approximation', 'description': 'synthetic', 'status': ne},
            {'name': STAGE0, 'kind': 'approximation', 'description': 'synthetic',
             'status': evd if stage0_evaluated else ne, 'headline': False, 'coefficient_grid_pin': grid,
             'scoring_scope': {'query_ids': IDS[35:]}},
        ]
        self.slots = wjson(os.path.join(d, 'slots.json'), {
            'query_block': {'rows': [{'query_id': q, 'Rad_text': t, 'radius_kpc': float(t), 'data_row_index': i + 1,
                                      'primary_GL4': {'reason': 'QUERY_INSIDE_INNERMOST_NODE' if i < 2 else None}}
                                     for i, (q, t) in enumerate(zip(IDS, RAD_TEXT))],
                            'invalid_primary_GL4': IDS[:2]},
            'alternatives': {'primary': PRIMARY, 'declared': declared},
            'projection_pins': {'route_b_config': cfg}})
        self.qm = wjson(os.path.join(d, 'query_manifest.json'), {'rows': [
            {'query_id': q, 'data_row_index': i + 1, 'Rad_text': t, 'Rad_unit': 'kpc'}
            for i, (q, t) in enumerate(zip(IDS, RAD_TEXT))]})
        self.fm = env.fm(self.slots, self.nodes)
        self.fm_pin = {'path': V003G_PATH, 'sha256': V003G_SHA}
        env.rb.load_freeze_module = lambda p: self.fm
        self.spec = self.fm.make_freeze_coordinate_spec(coordinates=COORDS)['spec']
        S = self.fm._spec_from(self.spec, [])
        self.points = [{'theta_natural': self.fm._theta_engine_from_u(S, u), 'u': list(u), 'log_index': li,
                        'role': ro, 'identified_projection': pr} for u, li, ro, pr in zip(US, LOGS, ROLES, PROJ)]
        self.sel = wjson(os.path.join(d, 'selection.json'), dict(SEL, points=self.points))
        self.spec_pin = wjson(os.path.join(d, 'spec.json'), self.spec)
        self.evaluated = [PRIMARY, OK_ALT] + ([STAGE0] if stage0_evaluated else [])
        # PLAN stage and the value-free plan outputs
        out = env.fresh('plan_' + name)
        self.build(self.input(d, 'PHASE_1' if not stage0_evaluated else 'PHASE_2', 'PLAN', {}), out)
        plan_pins = jload(os.path.join(out, 'ROSTER_PINS.json'))['row_registration_rosters']
        self.plan_outputs = {}
        for alt in self.evaluated:
            r = self.fm.evaluate_envelopes(forward_ngc=self.never, points=self.points, spec=self.spec,
                                           query_ids=IDS, budget=0, row_registration_roster=plan_pins[alt])
            assert r['ok'] and r['status'] == 'BUDGET_EXHAUSTED', r['reasons']
            self.plan_outputs[alt] = wjson(os.path.join(d, 'plan_%s.json' % alt), r)
        self.thetas = {m['member_id']: m['theta_ngc'] for m in
                       jload(self.plan_outputs[PRIMARY]['path'])['members']}

    @staticmethod
    def never(theta):
        raise AssertionError('a budget-0 call evaluated a point')

    def activate(self):
        self.env.rb.load_freeze_module = lambda p: self.fm

    def input(self, d, phase, stage, extra):
        """A builder input. MEMBERS/FULL inputs get the launch registry of exactly their calls unless the case gives
        one; FULL inputs get the suite's step-7 ledger root unless the case gives one."""
        doc = {'schema': 'ROSTER_BUILDER_INPUT_C2V003', 'phase': phase, 'stage': stage,
               'freeze_module': self.fm_pin, 'slots': self.slots, 'query_manifest': self.qm}
        doc.update(extra)
        if stage in ('MEMBERS', 'FULL') and 'launch_registry' not in extra:
            calls = extra.get('calls') if isinstance(extra.get('calls'), list) else []
            others = extra.get('other_phase_calls') if isinstance(extra.get('other_phase_calls'), list) else []
            doc['launch_registry'] = self.registry_pin(d, phase, calls, others)
        self.env.n += 1
        if stage == 'FULL' and 'step7_ledger_root' not in extra:
            # one ledger root per FULL input: equal plans built by different cases never share a root (K17 does)
            doc['step7_ledger_root'] = self.env.dir('ledgers', 'L%04d' % self.env.n)
        return wjson(os.path.join(d, 'input_%03d.json' % self.env.n), doc)

    def registry_doc(self, phase, calls, others, call_over=None, other_over=None, extra_entries=()):
        """The launch registry (G27 proposal) root keeps: per call, its exact-theta key and the spec sha registered
        at launch. Thetas come from the PLAN outputs and the saved sensitivity plan, never from a receipt."""
        entries = []
        for c in calls:
            alt, kind, key = c['alternative'], c['kind'], c['key']
            t = tsha(self.thetas[key]) if kind == 'MEMBER' else self.sens_tsha[key]
            e = {'alternative': alt, 'kind': kind, 'key': key, 'theta_sha256': t, 'spec_sha256': spec_of(alt, t)}
            e.update((call_over or {}).get((alt, kind, key), {}))
            entries.append(e)
        for o in others:
            lab = o['label']
            e = {'alternative': None, 'kind': 'OTHER', 'key': lab, 'theta_sha256': other_tsha(lab),
                 'spec_sha256': other_spec(lab)}
            e.update((other_over or {}).get(lab, {}))
            entries.append(e)
        return {'schema': 'STEP5_LAUNCH_REGISTRY_C2V003', 'phase': phase, 'calls': entries + list(extra_entries)}

    def registry_pin(self, d, phase, calls, others, **kw):
        """Content-addressed: equal registries share one file (so B04's two builds see byte-equal inputs)."""
        raw = (json.dumps(self.registry_doc(phase, calls, others, **kw), indent=1, sort_keys=True) + '\n').encode()
        path = os.path.join(self.env.dir('registries'), 'launch_registry_%s.json' % sha(raw)[:32])
        if os.path.exists(path):
            return pin(path)
        return wbytes(path, raw)

    def build(self, ipin, out):
        self.activate()
        return self.env.rb.build(ipin['path'], ipin['sha256'], out)

    # --- results and calls -------------------------------------------------------------------------------------
    def contract(self, theta, cut_kpc):
        fm = self.fm
        roster = {'required': {q: {'status': 'INVALID', 'reason': 'QUERY_INSIDE_INNERMOST_NODE',
                                   'registration': None} for q in IDS[:2]},
                  'cut_mode': 'PER_THETA', 'contexts': [(fm._canonical_bytes(theta), cut_kpc)], 'kpc_m': KPC_M,
                  'registered_radii_m': [r * KPC_M for r in GL4_KPC],
                  'radii': {q: float(t) for q, t in zip(IDS, RAD_TEXT)}}
        return {q: v['reason'] for q, v in fm._row_contract(roster, theta).items()}

    @staticmethod
    def valid_result(theta, required, gate_rows, seed):
        rows, speeds, invalid = [], {}, []
        for j, q in enumerate(IDS):
            reason = required.get(q) or gate_rows.get(q)
            if reason:
                rows.append({'id': q, 'valid': False, 'speed_km_s': None, 'reason': reason})
                speeds[q] = None
                invalid.append(q)
            else:
                v = 100.0 + 0.25 * j + seed
                rows.append({'id': q, 'valid': True, 'speed_km_s': v, 'reason': None})
                speeds[q] = v
        h = sha(json.dumps(theta, sort_keys=True).encode())
        return {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'galaxy': 'NGC3198', 'status': 'COMPLETED',
                'valid': True, 'scored': False, 'reasons': [], 'driver_sha256': h, 'call_spec_sha256': h,
                'rows': rows, 'speeds_km_s': speeds, 'invalid_rows': invalid,
                'route_a_outcome': {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                                    'ro1': {'rule': 'RO1', 'armed': True, 'fired': False, 'events': [],
                                            'worker_sha256': h, 'binding_sha256': h}},
                'uv_tail': {'schema': 'UNT_GALAXY_M0_FORWARD_UV_TAIL_C2V010', 'enabled': True,
                            'admissibility': 'production', 'pending_certificates': [],
                            'source_rule': 'continuum_v001', 'nodes_ext_context': None,
                            'config': {'normalized_sha256': h},
                            'stage_records': [{'finish_sha256': h, 'state_digest': h, 'production_admissible': True,
                                               'test_only_admitted': False}]}}

    @staticmethod
    def failure_record():
        return {'schema': 'UNT_GALAXY_M0_FORWARD_RESULT_C2V001', 'galaxy': 'NGC3198', 'status': 'FAILED',
                'valid': False, 'scored': False, 'reasons': ['SYNTHETIC_SOLVER_FAILURE'], 'rows': None,
                'speeds_km_s': None}

    def call(self, d, alt, kind, key, theta, attempts, result='valid', cut_kpc=None, gate_rows=None, seed=0.0,
             shared_run_dir=None, cut_path=None):
        """attempts: (raw_status, utc) or (raw_status, utc, evidence) or (raw_status, utc, evidence, run_dir).
        Every receipt carries the call-binding keys (the call's exact-theta key and registered spec sha) unless the
        evidence overrides one or sets it to DROP."""
        base = os.path.join(d, 'runs', alt, kind, key)
        att = []
        tk = tsha(theta)
        for i, a in enumerate(attempts):
            raw, t = a[0], a[1]
            evidence = a[2] if len(a) > 2 and a[2] is not None else {}
            rd = (a[3] if len(a) > 3 else None) or shared_run_dir or os.path.join(base, 'a%d' % i)
            os.makedirs(rd, exist_ok=True)
            doc = {'receipt_status': raw, 'receipt_written_utc': t, 'theta_sha256': tk, 'spec_sha256': spec_of(alt, tk)}
            doc.update(evidence)
            doc = {k: v for k, v in doc.items() if v != DROP}
            rp = wjson(os.path.join(rd, 'receipt_%s_%s_%d.json' % (alt, key, i)), doc)
            att.append({'run_dir': os.path.realpath(rd), 'receipt': rp})
        td = att[-1]['run_dir']
        cut = None
        if cut_path is not None:
            cut = cut_path
        elif cut_kpc is not None:
            # c2v004: the evidence names its call, so distinct calls' cut records differ in bytes (G29)
            cut = wjson(os.path.join(td, 'cut_%s_%s.json' % (alt, key)), {
                'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001', 'confinement_status': 'CERTIFIED_UNCONFINED',
                'classification_evidence': {'synthetic': True, 'synthetic_call': '%s:%s:%s' % (alt, kind, key)},
                'first_unconfined_R_kpc': cut_kpc})
        res = None
        if result == 'valid':
            res = wjson(os.path.join(td, 'result_%s_%s.json' % (alt, key)),
                        self.valid_result(theta, self.contract(theta, cut_kpc), gate_rows or {}, seed))
        elif result == 'failure':
            res = wjson(os.path.join(td, 'result_%s_%s.json' % (alt, key)), self.failure_record())
        return {'alternative': alt, 'kind': kind, 'key': key, 'attempts': att, 'result': res, 'cut_record': cut}


def gate_doc(reasons, qids):
    return {'schema': 'REGISTERED_INVALID_ROW_GATE_CX3V001', 'registration_status': 'REGISTERED',
            'registered_reasons': reasons, 'query_ids': qids}


def v006_text(entries):
    return ('# synthetic V006\n\n' + ''.join('## %s\n\n- pins `%s`\n\n' % (h, s) for h, s in entries)).encode()


def drive(env, base, out, label, plan_pin=None, fm=None, build_record=None, roster_pins=None, freeze_module=None):
    """The in-memory pass driver on a build output directory (RUNBOOK steps 2 and 7)."""
    doc = {'schema': 'PASS_INPUT_C2V003', 'pass_label': label, 'freeze_module': freeze_module or base.fm_pin,
           'build_record': build_record or pin(os.path.join(out, 'BUILD_RECORD.json')),
           'replay_plan': plan_pin or pin(os.path.join(out, 'REPLAY_PLAN.json')),
           'roster_pins': roster_pins or pin(os.path.join(out, 'ROSTER_PINS.json')),
           'selection': base.sel, 'spec': base.spec_pin, 'null_direction_rule': NULL_RULE}
    return env.rb.pass_driver(fm or base.fm, doc)


def save(env, d, name, obj):
    return wbytes(os.path.join(env.dir(*d) if isinstance(d, tuple) else d, name), env.rb.dump_bytes(obj))


def step7(env, out, plan_pin, p1_pin, pk_pin):
    return env.rb.step7_run(pin(os.path.join(out, 'BUILD_RECORD.json')), plan_pin, p1_pin, pk_pin)


def ledger_dir(out):
    """R3: the step-7 ledger of a FULL build: <step7_ledger_root>/STEP7_LEDGER_<sha256 of BUILD_RECORD.json bytes>."""
    with open(os.path.join(out, 'BUILD_RECORD.json'), 'rb') as f:
        raw = f.read()
    return os.path.join(json.loads(raw)['step7_ledger_root'], 'STEP7_LEDGER_' + sha(raw))


def copy_build(env, out, tag):
    """A byte copy of a build directory's files (the R3 copy attack): same BUILD_RECORD sha256, new location."""
    dst = env.fresh(tag)
    os.mkdir(dst)
    for nm in sorted(os.listdir(out)):
        src_p = os.path.join(out, nm)
        if os.path.isfile(src_p):
            with open(src_p, 'rb') as f:
                wbytes(os.path.join(dst, nm), f.read())
    return dst


def discrepant_fm(env, base):
    """A freeze-module instance whose pass sees M001 member-invalid: a validity outcome differing from pass one
    (stands in for a nondeterministic validity result; no fixture file is edited)."""
    m = env.fm(base.slots, base.nodes)
    orig = m._member_contract_valid
    m._member_contract_valid = lambda mem: False if mem['member_id'] == 'M001' else orig(mem)
    return m


# --------------------------------------------------------------------------------------------------------------
# scenario: Phase 1 (A133 1.6) and Phase 2 (unchanged order)
# --------------------------------------------------------------------------------------------------------------

class World:
    def __init__(self, env):
        self.env = env
        rb = env.rb
        self.b1 = Base(env, 'v003', stage0_evaluated=False)
        self.b2 = Base(env, 'succ', stage0_evaluated=True)
        d = env.dir('world')
        self.d = d
        self.g1 = wjson(os.path.join(d, 'gate_G1.json'), gate_doc(['SYN_GATE_REASON'], ['SYN-Q20']))
        self.g2 = wjson(os.path.join(d, 'gate_G2.json'), gate_doc(['SYN_GATE_REASON_B'], ['SYN-Q21']))
        self.cutoff = wbytes(os.path.join(d, 'v006_cutoff.md'), v006_text(
            [('A900: gate G1 pinned (synthetic)', self.g1['sha256']),
             ('A901: gate G2 pinned (synthetic)', self.g2['sha256'])]))
        logged = v006_text([('A900: gate G1 pinned (synthetic)', self.g1['sha256'])])
        self.logged = wbytes(os.path.join(d, 'v006_logged_prelaunch.md'), logged)
        self.prelaunch = wjson(os.path.join(d, 'prelaunch_record.json'), {
            'schema': rb.M15_RECORD_SCHEMA, 'date_u': 'Wed Oct 21 21:59:58 UTC 2026',
            'v006_sha256': self.logged['sha256'], 'gate_document_sha256s': [self.g1['sha256']]})
        self.launch_serial = wjson(os.path.join(d, 'launch_serial.json'), {
            'receipt_status': 'LAUNCHED', 'receipt_written_utc': '2026-10-21T22:00:00Z'})
        self.launch_twin = wjson(os.path.join(d, 'launch_twin.json'), {
            'receipt_status': 'LAUNCHED', 'receipt_written_utc': '2026-10-21T23:30:00Z'})
        self.m15 = {'pre_launch_record': self.prelaunch, 'logged_v006_copy': self.logged,
                    'launch_receipts': [self.launch_serial, self.launch_twin]}
        b = self.b1
        th = b.thetas
        self.p1_calls = [
            b.call(d, PRIMARY, 'MEMBER', 'M000', th['M000'], [('FINISHED', '2026-10-23T10:00:00Z')],
                   cut_kpc=38.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'}, seed=0.0),
            b.call(d, PRIMARY, 'MEMBER', 'M001', th['M001'], [('FINISHED', '2026-10-23T11:00:00Z')],
                   cut_kpc=None, seed=1.0),
            b.call(d, PRIMARY, 'MEMBER', 'M002', th['M002'], [('FINISHED', '2026-10-23T12:00:00Z')],
                   cut_kpc=30.5, seed=2.0),
        ]
        self.other = []
        for i, t in enumerate(('2026-10-23T13:00:00Z', '2026-10-23T14:00:00Z', '2026-10-23T15:00:00Z')):
            od = env.dir('world', 'runs_other', 'F%d' % (i + 1))
            lab = 'F%d' % (i + 1)
            self.other.append({'label': lab, 'attempts': [{'run_dir': od, 'receipt': wjson(
                os.path.join(od, 'receipt.json'), {'receipt_status': 'FINISHED', 'receipt_written_utc': t,
                                                   'theta_sha256': other_tsha(lab),
                                                   'spec_sha256': other_spec(lab)})}]})
        td = env.dir('world', 'runs_other', 'TWIN')
        lab = 'IDENTITY_TWIN_CW8'
        self.other.append({'label': lab, 'attempts': [{'run_dir': td, 'receipt': wjson(
            os.path.join(td, 'receipt.json'), {'receipt_status': 'PLANNED_KILL',
                                               'receipt_written_utc': '2026-10-22T01:00:00Z',
                                               'theta_sha256': other_tsha(lab), 'spec_sha256': other_spec(lab)})}]})

    def p1_extra(self, **over):
        b = self.b1
        x = {'plan_outputs': {a: b.plan_outputs[a] for a in b.evaluated}, 'calls': self.p1_calls,
             'gate_cutoff': {'kind': 'PHASE1_STEP4_START', 'v006_copy': self.cutoff},
             'gate_documents': [self.g1, self.g2], 'receipt_keys': RECEIPT_KEYS,
             'receipt_status_classes': CLASSES, 'sensitivity_plan_output': None, 'members_stage_rosters': None,
             'members_stage_build_record': None, 'm15': self.m15, 'other_phase_calls': self.other}
        x.update(over)
        return x

    def build_p1(self, tag, **over):
        b = self.b1
        d = self.env.dir('cases', tag)
        ipin = b.input(d, 'PHASE_1', 'FULL', self.p1_extra(**over))
        out = self.env.fresh(tag)
        b.build(ipin, out)
        return out

    def p1_with_m001(self, tag, attempts, result='failure', cut_kpc=None):
        b = self.b1
        c = b.call(self.env.dir('cases', tag), PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], attempts,
                   result=result, cut_kpc=cut_kpc)
        return self.build_p1(tag, calls=[self.p1_calls[0], c, self.p1_calls[2]])

    @staticmethod
    def outputs(out):
        """(roster pins, replay plan, gate-status REPORT). The c2v002 list form is c2v003's GATE_STATUS_REPORT.json;
        classifier A's list is GATE_STATUS_LIST.json (a_list)."""
        pins = jload(os.path.join(out, 'ROSTER_PINS.json'))['row_registration_rosters']
        plan = jload(os.path.join(out, 'REPLAY_PLAN.json'))
        gl_path = os.path.join(out, 'GATE_STATUS_REPORT.json')
        gl = jload(gl_path) if os.path.exists(gl_path) else None
        return pins, plan, gl

    @staticmethod
    def a_list(out):
        return jload(os.path.join(out, 'GATE_STATUS_LIST.json'))


def frozen_checks(base, mem, pins):
    """What write_freeze_manifest/_root_manifest_check apply to every evaluated member and sensitivity entry."""
    fm = base.fm
    envs, sens = mem['envelopes'], mem['sensitivity']
    for alt, ev_ in envs.items():
        r = fm._load_row_roster(pins[alt], IDS)
        for m in ev_['members']:
            fm._root_frozen_rows(m, IDS, r)
    rp = fm._load_row_roster(pins[PRIMARY], IDS)
    for e in sens['evaluations']:
        fm._root_frozen_rows(e, IDS, rp)
    alt_results = {a: {'member_evaluation': fm._member_eval_record(e)} for a, e in envs.items() if a != PRIMARY}
    return fm._incomplete_reasons({'exploration_status': 'COMPLETE'}, fm._member_eval_record(envs[PRIMARY]),
                                  {'status': sens['status']}, alt_results)


# --------------------------------------------------------------------------------------------------------------
# cases
# --------------------------------------------------------------------------------------------------------------

CASES = []


def case(cid, expect, code=None):
    def deco(fn):
        CASES.append((cid, expect, code, fn))
        return fn
    return deco


def expect_refusal(rb, fn, code):
    try:
        fn()
    except (rb.Refused, rb.Stop) as exc:
        if exc.code != code:
            raise AssertionError('expected %s, observed %s (%s)' % (code, exc.code, exc.detail))
        raise
    raise AssertionError('no refusal; expected ' + code)


def run_cli(args):
    r = subprocess.run([sys.executable, '-I', '-B', BUILDER_PATH] + args, capture_output=True, text=True)
    return r


def main_in_process(env, args):
    out = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = env.rb.main(args)
    return rc, out.getvalue(), err.getvalue()


@case('B01_plan_stage_six_NONE_rosters_accepted_by_v003g', 'MUST_PASS')
def _b01(env, w):
    out = env.fresh('plan_check')
    w.b1.build(w.b1.input(env.dir('cases', 'b01'), 'PHASE_1', 'PLAN', {}), out)
    pins = jload(os.path.join(out, 'ROSTER_PINS.json'))['row_registration_rosters']
    assert len(pins) == 6
    for alt, p in pins.items():
        r = w.b1.fm._load_row_roster(p, IDS)
        assert r['cut_mode'] == 'NONE' and r['gates'] == {}
    rec = jload(os.path.join(out, 'BUILD_RECORD.json'))
    assert rec['status'] == 'BUILT' and rec['double_run'] == 'BYTE_EQUAL'


@case('B02_phase1_full_rosters_modes_budgets_and_v003g_acceptance', 'MUST_PASS')
def _b02(env, w):
    out = w.build_p1('b02')
    pins, plan, gl = w.outputs(out)
    modes = {a['name']: a['mode'] for a in plan['alternatives']}
    assert modes == {PRIMARY: 'PER_THETA', OK_ALT: 'NONE', 'ML_3p6_0.4': 'NONE', 'ML_3p6_0.6': 'NONE',
                     'GL10_SOURCE_GAUSS_ORDER': 'NONE', STAGE0: 'NONE'}, modes
    budgets = {a['name']: a['member_budget'] for a in plan['alternatives']}
    assert budgets[PRIMARY] == 3 and budgets[OK_ALT] == 0 and plan['sensitivity']['budget'] == 0
    roster = jload(pins[PRIMARY]['path'])
    ctx = roster['outer_cut']['contexts']
    assert [c['cut'] is None for c in ctx] == [False, True, False]
    assert [c['theta_ngc'] for c in ctx] == [w.b1.thetas[k] for k in ('M000', 'M001', 'M002')]
    assert all(jload(p['path'])['root_gates'] == sorted([w.g1, w.g2], key=lambda g: g['sha256'])
               for p in pins.values())
    assert plan['stage0_status'] == {'status': 'NOT_EVALUATED_BEFORE_FREEZE', 'reasons': ['NOT_IN_PHASE_1'],
                                     'receipts': [], 'step4_start_utc': '2026-10-23T15:00:00Z'}
    assert plan['step4']['start_utc'] == '2026-10-23T15:00:00Z'
    ok = [m for m in plan['alternatives'] if m['name'] == OK_ALT][0]
    assert all(m['own_disposition'] == 'NOT_RUN_PHASE1_BUDGET0' for m in ok['members'])
    assert plan['pass_one']['replay_plan_sha256'] is None and plan['pass_one']['member_budget'] == {
        PRIMARY: 3, OK_ALT: 0}
    assert 'no other NGC process running' in plan['rules']['c'] and 'wall cap' in plan['rules']['c']


@case('B03_phase1_end_to_end_driver_v003g_freeze_checks_and_step7', 'MUST_PASS')
def _b03(env, w):
    out = w.build_p1('b03')
    pins, plan, _ = w.outputs(out)
    rec1, extract, mem = drive(env, w.b1, out, 'PASS_ONE')
    assert extract is None
    pe = mem['envelopes'][PRIMARY]
    assert pe['status'] == 'COMPLETE' and pe['n_member_valid'] == 3, pe['reasons']
    assert mem['envelopes'][OK_ALT]['status'] == 'BUDGET_EXHAUSTED' and mem['envelopes'][OK_ALT]['n_evaluated'] == 0
    assert mem['reference']['member_id'] == 'M002'
    regs = pe['members'][0]['row_registration']
    assert regs[19]['reason'] == 'SYN_GATE_REASON' and regs[19]['registration']['sha256'] == w.g1['sha256']
    assert sum(1 for r in regs if r and r['reason'] == 'QUERY_BEYOND_OUTER_GAS_CUT') == 5   # 39..43 >= 38.5
    inc = frozen_checks(w.b1, mem, pins)
    assert inc == ['SENSITIVITY_BUDGET_EXHAUSTED', 'ALTERNATIVE_ORIGINAL_K_MEMBER_EVALUATION_BUDGET_EXHAUSTED'], inc
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    d = env.dir('cases', 'b03')
    res, _raw, succ = step7(env, out, pin(os.path.join(out, 'REPLAY_PLAN.json')), save(env, d, 'p1.json', rec1),
                            save(env, d, 'pk.json', reck))
    assert res['status'] == 'NO_NEW_DISCREPANCY' and succ is None and res['seq'] == 1, res
    assert sorted(os.listdir(ledger_dir(out)))[-1] == 'STEP7_0001.json'
    assert not os.path.lexists(os.path.join(out, 'STEP7_LEDGER'))


@case('B04_double_run_byte_equal_outputs', 'MUST_PASS')
def _b04(env, w):
    o1, o2 = w.build_p1('b04a'), w.build_p1('b04b')
    for name in ('GATE_STATUS_LIST.json', 'REPLAY_PLAN.json') + tuple(
            'ROSTER_%s.json' % a['name'] for a in jload(os.path.join(o1, 'REPLAY_PLAN.json'))['alternatives']):
        with open(os.path.join(o1, name), 'rb') as f1, open(os.path.join(o2, name), 'rb') as f2:
            assert f1.read() == f2.read(), name
    with open(os.path.join(o1, 'ROSTER_PINS.json')) as f1, open(os.path.join(o2, 'ROSTER_PINS.json')) as f2:
        assert f1.read().replace(os.path.realpath(o1), 'OUT') == f2.read().replace(os.path.realpath(o2), 'OUT')


@case('B05_unpinned_gate_document_refused', 'MUST_FAIL', 'GATE_NOT_PINNED_IN_CUTOFF_V006')
def _b05(env, w):
    g3 = wjson(os.path.join(env.dir('cases', 'b05'), 'gate_G3.json'), gate_doc(['SYN_GATE_REASON_C'], ['SYN-Q22']))
    expect_refusal(env.rb, lambda: w.build_p1('b05', gate_documents=[w.g1, w.g2, g3]),
                   'GATE_NOT_PINNED_IN_CUTOFF_V006')


@case('B06_missing_cut_record_key_refused', 'MUST_FAIL', 'CUT_CONTEXT_MISSING')
def _b06(env, w):
    calls = copy.deepcopy(w.p1_calls)
    del calls[1]['cut_record']
    expect_refusal(env.rb, lambda: w.build_p1('b06', calls=calls), 'CUT_CONTEXT_MISSING')


@case('B07_cut_record_pin_to_absent_file_refused', 'MUST_FAIL', 'PIN_UNREADABLE')
def _b07(env, w):
    calls = copy.deepcopy(w.p1_calls)
    calls[0]['cut_record'] = {'path': calls[0]['cut_record']['path'] + '.absent', 'sha256': '0' * 64}
    expect_refusal(env.rb, lambda: w.build_p1('b07', calls=calls), 'PIN_UNREADABLE')


@case('B08_cut_record_of_another_call_refused', 'MUST_FAIL', 'CUT_RECORD_NOT_OF_ITS_CALL')
def _b08(env, w):
    calls = copy.deepcopy(w.p1_calls)
    calls[1]['cut_record'] = calls[0]['cut_record']
    expect_refusal(env.rb, lambda: w.build_p1('b08', calls=calls), 'CUT_RECORD_NOT_OF_ITS_CALL')


@case('B09_one_cut_file_serving_two_calls_refused', 'MUST_FAIL', 'CUT_RECORD_BORROWED')
def _b09(env, w):
    d = env.dir('cases', 'b09')
    b = w.b1
    shared = env.dir('cases', 'b09', 'shared_run')
    c0 = b.call(d, PRIMARY, 'MEMBER', 'M000', b.thetas['M000'], [('FINISHED', '2026-10-23T10:00:00Z')],
                cut_kpc=38.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'}, shared_run_dir=shared)
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], [('FINISHED', '2026-10-23T11:00:00Z')],
                shared_run_dir=shared, cut_path=c0['cut_record'])
    calls = [c0, c1, w.p1_calls[2]]
    expect_refusal(env.rb, lambda: w.build_p1('b09', calls=calls), 'CUT_RECORD_BORROWED')


@case('B10_gate_with_builtin_reason_refused', 'MUST_FAIL', 'GATE_BUILTIN_REASON_MUST_DERIVE_FROM_RULE')
def _b10(env, w):
    d = env.dir('cases', 'b10')
    g = wjson(os.path.join(d, 'g.json'), gate_doc(['QUERY_BEYOND_OUTER_GAS_CUT'], ['SYN-Q22']))
    cut = wbytes(os.path.join(d, 'cutoff.md'), v006_text([('A900', w.g1['sha256']), ('A901', w.g2['sha256']),
                                                          ('A902', g['sha256'])]))
    expect_refusal(env.rb, lambda: w.build_p1('b10', gate_documents=[w.g1, w.g2, g],
                                              gate_cutoff={'kind': 'PHASE1_STEP4_START', 'v006_copy': cut}),
                   'GATE_BUILTIN_REASON_MUST_DERIVE_FROM_RULE')


@case('B11_duplicate_query_reason_pair_across_gates_refused', 'MUST_FAIL', 'GATE_AMBIGUOUS')
def _b11(env, w):
    d = env.dir('cases', 'b11')
    g = wjson(os.path.join(d, 'g.json'), gate_doc(['SYN_GATE_REASON'], ['SYN-Q20', 'SYN-Q23']))
    cut = wbytes(os.path.join(d, 'cutoff.md'), v006_text([('A900', w.g1['sha256']), ('A902', g['sha256'])]))
    expect_refusal(env.rb, lambda: w.build_p1('b11', gate_documents=[w.g1, g],
                                              gate_cutoff={'kind': 'PHASE1_STEP4_START', 'v006_copy': cut}),
                   'GATE_AMBIGUOUS')


@case('B12_member_without_terminal_call_record_refused', 'MUST_FAIL', 'CALL_RECORD_MISSING')
def _b12(env, w):
    expect_refusal(env.rb, lambda: w.build_p1('b12', calls=w.p1_calls[:2]), 'CALL_RECORD_MISSING')


@case('B13_input_manifest_sha_mismatch_refused_cli_exit_2', 'MUST_FAIL', 'PIN_MISMATCH')
def _b13(env, w):
    d = env.dir('cases', 'b13')
    ipin = w.b1.input(d, 'PHASE_1', 'FULL', w.p1_extra())
    r = run_cli(['build', '--input', ipin['path'], '--input-sha256', '1' * 64, '--out-dir', env.fresh('b13')])
    assert r.returncode == 2, (r.returncode, r.stderr)
    raise env.rb.Refused(json.loads(r.stderr)['refused'])


@case('B14_infra_last_attempt_not_terminal_refused', 'MUST_FAIL', 'CALL_NOT_TERMINAL')
def _b14(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('b14', [('INFRA_SPAWN', '2026-10-23T11:00:00Z')], result=None),
                   'CALL_NOT_TERMINAL')


@case('B15_failed_after_one_attempt_rule_c_incomplete_refused', 'MUST_FAIL', 'RULE_C_INCOMPLETE')
def _b15(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('b15', [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev())]),
                   'RULE_C_INCOMPLETE')


@case('B16_phase1_original_k_call_refused', 'MUST_FAIL', 'CALL_NOT_REGISTERED_FOR_PHASE')
def _b16(env, w):
    d = env.dir('cases', 'b16')
    b = w.b1
    c = b.call(d, OK_ALT, 'MEMBER', 'M000', b.thetas['M000'], [('FINISHED', '2026-10-23T10:00:00Z')])
    expect_refusal(env.rb, lambda: w.build_p1('b16', calls=w.p1_calls + [c]), 'CALL_NOT_REGISTERED_FOR_PHASE')


@case('B17_plan_output_carrying_an_evaluation_refused', 'MUST_FAIL', 'PLAN_OUTPUT_NOT_VALUE_FREE')
def _b17(env, w):
    d = env.dir('cases', 'b17')
    doc = jload(w.b1.plan_outputs[PRIMARY]['path'])
    doc['members'][1]['evaluated'] = True
    doc['members'][1]['speeds_km_s'][5] = 123.0
    p = wjson(os.path.join(d, 'plan.json'), doc)
    po = dict(w.p1_extra()['plan_outputs'])
    po[PRIMARY] = p
    expect_refusal(env.rb, lambda: w.build_p1('b17', plan_outputs=po), 'PLAN_OUTPUT_NOT_VALUE_FREE')


@case('B18_cut_record_with_target_field_refused', 'MUST_FAIL', 'CUT_RECORD_TARGET_FIELDS_REFUSED')
def _b18(env, w):
    calls = copy.deepcopy(w.p1_calls)
    td = calls[0]['attempts'][-1]['run_dir']
    p = wjson(os.path.join(td, 'cut_with_target_key.json'), {
        'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001', 'confinement_status': 'CERTIFIED_UNCONFINED',
        'classification_evidence': {'synthetic': True}, 'first_unconfined_R_kpc': 38.5, 'target_note': 'x'})
    calls[0]['cut_record'] = p
    expect_refusal(env.rb, lambda: w.build_p1('b18', calls=calls), 'CUT_RECORD_TARGET_FIELDS_REFUSED')


@case('B19_empty_valid_set_caught_by_v003g_self_check_G23', 'MUST_FAIL', 'V003G_SELF_CHECK')
def _b19(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('b19', [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
                                                          ('FAILED_SOLVER', '2026-10-23T11:30:00Z', ev(raised=True))],
                                                  cut_kpc=0.5), 'V003G_SELF_CHECK')


@case('B24_finished_call_without_a_saved_result_refused', 'MUST_FAIL', 'FINISHED_WITHOUT_RESULT')
def _b24(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('b24', [('FINISHED', '2026-10-23T11:00:00Z')], result=None),
                   'FINISHED_WITHOUT_RESULT')


@case('B20_cap_terminal_with_rule_c_evidence_leaves_member_UNEVALUATED_rule_f', 'MUST_PASS')
def _b20(env, w):
    out = w.p1_with_m001('b20', [('WALL_CAP', '2026-10-23T11:00:00Z', ev()),
                                 ('WALL_CAP', '2026-10-24T11:00:00Z', ev(raised=True))], result=None)
    pins, plan, _ = w.outputs(out)
    pa = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]
    assert pa['member_budget'] == 1
    assert [m['effective_disposition'] for m in pa['members']] == [
        'EVALUATED', 'UNEVALUATED_CAP', 'UNEVALUATED_BY_ORDER_TRUNCATION']
    rc = pa['members'][1]['rule_c']
    assert rc['counted_attempts'] == [0, 1] and rc['rerun_wall_cap_s'] == 86400 and rc['rerun_rss_cap_bytes'] == RAM
    assert len(jload(pins[PRIMARY]['path'])['outer_cut']['contexts']) == 2
    _rec, _x, mem = drive(env, w.b1, out, 'PASS_ONE')
    pe = mem['envelopes'][PRIMARY]
    assert pe['status'] == 'BUDGET_EXHAUSTED' and pe['n_member_invalid'] == 0
    assert [m['evaluated'] for m in pe['members']] == [True, False, False]
    inc = frozen_checks(w.b1, mem, pins)
    assert 'PRIMARY_MEMBER_EVALUATION_BUDGET_EXHAUSTED' in inc, inc


@case('B21_failed_terminal_with_rule_c_evidence_is_a_failure_record_MEMBER_INVALID', 'MUST_PASS')
def _b21(env, w):
    d = env.dir('cases', 'b21')
    b = w.b1
    c = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'],
               [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
                ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(raised=True))], result='failure')
    k = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'],
               [('FAILED_SOLVER', '2026-10-23T12:00:00Z', ev()),
                ('FAILED_SOLVER', '2026-10-24T12:00:00Z', ev(raised=True))], result=None, cut_kpc=30.5)
    out = w.build_p1('b21', calls=[w.p1_calls[0], c, k])
    pins, plan, _ = w.outputs(out)
    pa = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]
    assert pa['member_budget'] == 3
    _rec, _x, mem = drive(env, b, out, 'PASS_ONE')
    pe = mem['envelopes'][PRIMARY]
    assert pe['status'] == 'COMPLETE' and pe['n_member_invalid'] == 2
    assert pe['members'][1]['forward_valid_flag'] is False and pe['members'][2]['exception'] is not None
    assert mem['reference']['member_id'] == 'M000'
    frozen_checks(b, mem, pins)


@case('B22_one_ulp_different_theta_has_no_context', 'MUST_FAIL', 'ROOT_ROSTER_MISSING_OR_AMBIGUOUS_CUT_THETA')
def _b22(env, w):
    out = w.build_p1('b22')
    pins, _plan, _ = w.outputs(out)
    r = w.b1.fm._load_row_roster(pins[PRIMARY], IDS)
    th = dict(w.b1.thetas['M001'])
    th['syn_a'] = math.nextafter(th['syn_a'], 2.0)
    try:
        w.b1.fm._row_contract(r, th)
    except ValueError as exc:
        raise env.rb.Refused(str(exc).split(':')[0])
    raise AssertionError('v003g accepted a one-ulp-different theta')


@case('B23_replay_adapter_never_invents_a_result_and_flags_custody_breach', 'MUST_PASS')
def _b23(env, w):
    out = w.build_p1('b23')
    _pins, plan, _ = w.outputs(out)
    log = []
    fwd = env.rb.make_replay_adapter(plan, PRIMARY, log, 'ENVELOPES')
    th = dict(w.b1.thetas['M001'])
    th['syn_b'] = th['syn_b'] * 1.5
    try:
        fwd(th)
        raise AssertionError('served an unregistered theta')
    except env.rb.ReplayUnknownKey:
        pass
    assert log[-1]['outcome'] == 'UNKNOWN_KEY'
    doc = fwd(dict(w.b1.thetas['M001']))
    assert doc['valid'] is True and log[-1]['outcome'] == 'SERVED'
    fk = env.rb.make_replay_adapter(plan, OK_ALT, log, 'ENVELOPES')
    try:
        fk(dict(w.b1.thetas['M001']))
        raise AssertionError('served ORIGINAL_K in Phase 1')
    except env.rb.ReplayUnknownKey:
        pass
    bad = copy.deepcopy(plan)
    key = env.rb.theta_sha256(w.b1.thetas['M001'])
    for e in bad['replay_index'][PRIMARY]:
        if e['theta_sha256'] == key:
            e['result'] = dict(e['result'], sha256='e' * 64)
    fb = env.rb.make_replay_adapter(bad, PRIMARY, log, 'ENVELOPES')
    try:
        fb(dict(w.b1.thetas['M001']))
        raise AssertionError('served bytes that do not verify')
    except env.rb.ReplayNoSavedResult:
        pass
    assert log[-1]['outcome'] == 'RESULT_CUSTODY_BREACH'


# ---------------- rule (c) mechanization and attempt distinctness ----------------

@case('C01_two_failures_1s_apart_without_solo_or_cap_evidence_refused', 'MUST_FAIL', 'RULE_C_EVIDENCE_MISSING')
def _c01(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('c01', [('FAILED_SOLVER', '2026-10-23T11:00:00Z'),
                                                          ('FAILED_SOLVER', '2026-10-23T11:00:01Z')]),
                   'RULE_C_EVIDENCE_MISSING')


@case('C02_identical_failures_with_another_NGC_process_running_refused', 'MUST_FAIL', 'RULE_C_NOT_SOLO')
def _c02(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('c02', [
        ('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
        ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(solo=False, raised=True))]), 'RULE_C_NOT_SOLO')


@case('C03_rerun_RSS_cap_not_at_RAM_refused', 'MUST_FAIL', 'RULE_C_RERUN_CAPS')
def _c03(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('c03', [
        ('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
        ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(raised=True, rss=96 * 2 ** 30))]), 'RULE_C_RERUN_CAPS')


@case('C04_rerun_wall_cap_not_doubled_refused', 'MUST_FAIL', 'RULE_C_RERUN_CAPS')
def _c04(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('c04', [
        ('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
        ('FAILED_SOLVER', '2026-10-24T11:00:00Z', dict(ev(raised=True), wall_cap_s=43200))]), 'RULE_C_RERUN_CAPS')


@case('C05_rerun_of_a_different_spec_refused', 'MUST_FAIL', 'RULE_C_SPEC_NOT_IDENTICAL')
def _c05(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('c05', [
        ('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
        ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(raised=True, spec='6' * 64))]), 'RULE_C_SPEC_NOT_IDENTICAL')


@case('C06_non_solo_pair_then_solo_raised_pair_is_terminal_at_the_third_attempt', 'MUST_PASS')
def _c06(env, w):
    out = w.p1_with_m001('c06', [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev(solo=False)),
                                 ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(raised=True)),
                                 ('FAILED_SOLVER', '2026-10-25T11:00:00Z', ev(raised=True))])
    _pins, plan, _ = w.outputs(out)
    m = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]['members'][1]
    assert m['own_disposition'] == 'EVALUATED_FAILED' and m['n_attempts'] == 3, m
    assert m['rule_c']['counted_attempts'] == [1, 2] and m['rule_c']['other_ngc_processes_max'] == [0, 0]


@case('C07_output_cap_rerun_without_a_raised_output_cap_refused_A141_L1', 'MUST_FAIL', 'RULE_C_RERUN_CAPS')
def _c07(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('c07', [
        ('OUTPUT_CAP_STOP', '2026-10-23T11:00:00Z', ev()),
        ('OUTPUT_CAP_STOP', '2026-10-24T11:00:00Z', ev(raised=True))], result=None), 'RULE_C_RERUN_CAPS')


@case('C08_output_cap_rerun_with_raised_caps_is_UNEVALUATED_CAP', 'MUST_PASS')
def _c08(env, w):
    out = w.p1_with_m001('c08', [('OUTPUT_CAP_STOP', '2026-10-23T11:00:00Z', ev()),
                                 ('OUTPUT_CAP_STOP', '2026-10-24T11:00:00Z',
                                  ev(raised=True, out_cap=136 * 2 ** 30))], result=None)
    _pins, plan, _ = w.outputs(out)
    pa = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]
    assert pa['member_budget'] == 1 and pa['members'][1]['own_disposition'] == 'UNEVALUATED_CAP'
    assert pa['members'][1]['rule_c']['rerun_output_cap_bytes'] == 136 * 2 ** 30


@case('O1a_one_attempt_listed_twice_refused', 'MUST_FAIL', 'ATTEMPT_RUN_DIR_REPEATED')
def _o1a(env, w):
    b = w.b1
    c = b.call(env.dir('cases', 'o1a'), PRIMARY, 'MEMBER', 'M001', b.thetas['M001'],
               [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev(raised=True))], result='failure')
    c['attempts'] = [c['attempts'][0], c['attempts'][0]]
    expect_refusal(env.rb, lambda: w.build_p1('o1a', calls=[w.p1_calls[0], c, w.p1_calls[2]]),
                   'ATTEMPT_RUN_DIR_REPEATED')


@case('O1b_second_run_dir_a_symlink_to_the_first_refused', 'MUST_FAIL', 'ATTEMPT_RUN_DIR_REPEATED')
def _o1b(env, w):
    b = w.b1
    d = env.dir('cases', 'o1b')
    c = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], [('WALL_CAP', '2026-10-23T11:00:00Z', ev())],
               result=None)
    a0 = c['attempts'][0]['run_dir']
    link = os.path.join(d, 'a1_link')
    os.symlink(a0, link)
    r1 = wjson(os.path.join(a0, 'receipt_second.json'), dict(
        ev(raised=True), receipt_status='WALL_CAP', receipt_written_utc='2026-10-24T11:00:00Z'))
    c['attempts'].append({'run_dir': link, 'receipt': r1})
    expect_refusal(env.rb, lambda: w.build_p1('o1b', calls=[w.p1_calls[0], c, w.p1_calls[2]]),
                   'ATTEMPT_RUN_DIR_REPEATED')


@case('O1c_byte_identical_receipt_in_a_second_run_dir_refused', 'MUST_FAIL', 'ATTEMPT_RECEIPT_REPEATED')
def _o1c(env, w):
    b = w.b1
    d = env.dir('cases', 'o1c')
    c = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev())],
               result='failure')
    a1 = env.dir('cases', 'o1c', 'second')
    with open(c['attempts'][0]['receipt']['path'], 'rb') as f:
        r1 = wbytes(os.path.join(a1, 'receipt_copy.json'), f.read())
    c['attempts'].append({'run_dir': a1, 'receipt': r1})
    expect_refusal(env.rb, lambda: w.build_p1('o1c', calls=[w.p1_calls[0], c, w.p1_calls[2]]),
                   'ATTEMPT_RECEIPT_REPEATED')


@case('O2_equal_receipt_times_refused', 'MUST_FAIL', 'ATTEMPT_ORDER')
def _o2(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('o2', [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
                                                         ('FAILED_SOLVER', '2026-10-23T11:00:00Z',
                                                          ev(raised=True))]), 'ATTEMPT_ORDER')


@case('O5_failures_after_a_FINISHED_attempt_refused', 'MUST_FAIL', 'ATTEMPT_AFTER_TERMINAL')
def _o5(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('o5', [('FINISHED', '2026-10-23T10:00:00Z'),
                                                         ('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
                                                         ('FAILED_SOLVER', '2026-10-24T11:00:00Z',
                                                          ev(raised=True))]), 'ATTEMPT_AFTER_TERMINAL')


@case('O6_a_second_FINISHED_attempt_re_rolling_a_finished_call_refused', 'MUST_FAIL', 'ATTEMPT_AFTER_TERMINAL')
def _o6(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('o6', [('FINISHED', '2026-10-23T10:00:00Z'),
                                                         ('FINISHED', '2026-10-23T11:00:00Z')], result='valid'),
                   'ATTEMPT_AFTER_TERMINAL')


@case('O7_attempt_after_a_rule_c_terminal_pair_refused', 'MUST_FAIL', 'ATTEMPT_AFTER_TERMINAL')
def _o7(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('o7', [('FAILED_SOLVER', '2026-10-23T10:00:00Z', ev()),
                                                         ('FAILED_SOLVER', '2026-10-24T10:00:00Z', ev(raised=True)),
                                                         ('FINISHED', '2026-10-25T10:00:00Z')], result='valid'),
                   'ATTEMPT_AFTER_TERMINAL')


@case('O8_nested_attempt_run_dirs_refused', 'MUST_FAIL', 'ATTEMPT_RUN_DIR_NESTED')
def _o8(env, w):
    outer = env.dir('cases', 'o8', 'run')
    inner = env.dir('cases', 'o8', 'run', 'retry')
    expect_refusal(env.rb, lambda: w.p1_with_m001('o8', [
        ('FAILED_SOLVER', '2026-10-23T10:00:00Z', ev(), outer),
        ('FAILED_SOLVER', '2026-10-24T10:00:00Z', ev(raised=True), inner)]), 'ATTEMPT_RUN_DIR_NESTED')


# ---------------- M-15 ----------------

@case('M01_m15_on_time_and_late_gates', 'MUST_PASS')
def _m01(env, w):
    out = w.build_p1('m01')
    _pins, _plan, gl = w.outputs(out)
    st = {g['gate']['sha256']: (g['status'], g['reason']) for g in gl['gates']}
    assert st[w.g1['sha256']] == ('ON_TIME', 'PINNED_IN_LOGGED_PRE_LAUNCH_V006'), st
    assert gl['record_precedes_launch'] is True and gl['earliest_launch_receipt_utc'] == '2026-10-21T22:00:00Z'
    assert all(g['pinned_by_entry'].startswith('A90') for g in gl['gates'])


@case('M02_gate_pinned_after_the_launch_receipt_reads_LATE', 'MUST_PASS')
def _m02(env, w):
    out = w.build_p1('m02')
    _pins, _plan, gl = w.outputs(out)
    st = {g['gate']['sha256']: (g['status'], g['reason']) for g in gl['gates']}
    assert st[w.g2['sha256']] == ('LATE', 'NOT_PINNED_IN_LOGGED_PRE_LAUNCH_V006'), st


@case('M03_pre_launch_record_written_after_the_launch_receipt_all_LATE', 'MUST_PASS')
def _m03(env, w):
    d = env.dir('cases', 'm03')
    rec = jload(w.prelaunch['path'])
    rec['date_u'] = 'Wed Oct 21 22:00:01 UTC 2026'
    p = wjson(os.path.join(d, 'prelaunch.json'), rec)
    out = w.build_p1('m03', m15=dict(w.m15, pre_launch_record=p))
    _pins, _plan, gl = w.outputs(out)
    assert [g['status'] for g in gl['gates']] == ['LATE', 'LATE']
    assert {g['reason'] for g in gl['gates']} == {'PRE_LAUNCH_RECORD_AFTER_LAUNCH_RECEIPT'}


@case('M04_no_pre_launch_record_all_LATE', 'MUST_PASS')
def _m04(env, w):
    out = w.build_p1('m04', m15=None)
    _pins, _plan, gl = w.outputs(out)
    assert [g['status'] for g in gl['gates']] == ['LATE', 'LATE']


@case('M05_record_and_receipt_same_second_counts_as_preceding', 'MUST_PASS')
def _m05(env, w):
    d = env.dir('cases', 'm05')
    rec = jload(w.prelaunch['path'])
    rec['date_u'] = 'Wed Oct 21 22:00:00 UTC 2026'
    p = wjson(os.path.join(d, 'prelaunch.json'), rec)
    out = w.build_p1('m05', m15=dict(w.m15, pre_launch_record=p))
    _pins, _plan, gl = w.outputs(out)
    assert gl['record_precedes_launch'] is True


@case('M09_gate_in_logged_v006_but_omitted_from_record_list_reads_ON_TIME_by_the_text', 'MUST_PASS')
def _m09(env, w):
    d = env.dir('cases', 'm09')
    rec = jload(w.prelaunch['path'])
    rec['gate_document_sha256s'] = []
    p = wjson(os.path.join(d, 'prelaunch.json'), rec)
    out = w.build_p1('m09', m15=dict(w.m15, pre_launch_record=p))
    _pins, _plan, gl = w.outputs(out)
    g1 = [g for g in gl['gates'] if g['gate']['sha256'] == w.g1['sha256']][0]
    assert g1['status'] == 'ON_TIME' and g1['in_pre_launch_record_list'] is False, g1


@case('M10_pre_launch_record_naming_a_sha_absent_from_its_logged_v006_refused', 'MUST_FAIL', 'M15_RECORD_INCONSISTENT')
def _m10(env, w):
    d = env.dir('cases', 'm10')
    rec = jload(w.prelaunch['path'])
    rec['gate_document_sha256s'] = [w.g1['sha256'], w.g2['sha256']]
    p = wjson(os.path.join(d, 'prelaunch.json'), rec)
    expect_refusal(env.rb, lambda: w.build_p1('m10', m15=dict(w.m15, pre_launch_record=p)), 'M15_RECORD_INCONSISTENT')


@case('M06_logged_v006_copy_not_the_logged_bytes_refused', 'MUST_FAIL', 'M15_LOGGED_V006_MISMATCH')
def _m06(env, w):
    expect_refusal(env.rb, lambda: w.build_p1('m06', m15=dict(w.m15, logged_v006_copy=w.cutoff)),
                   'M15_LOGGED_V006_MISMATCH')


@case('M07_gate_status_list_check_passes_on_builder_output', 'MUST_PASS')
def _m07(env, w):
    out = w.build_p1('m07')
    pins, _plan, _gl = w.outputs(out)
    r = env.rb.check_gate_list(pins, pin(os.path.join(out, 'GATE_STATUS_LIST.json')),
                               pin(os.path.join(out, 'BUILD_RECORD.json')))
    assert r['verdict'] == 'PASS' and r['list_schema'] == 'GATE_STATUS_LIST_C4V001', r


@case('M08_gate_missing_from_status_list_GATE_STATUS_LIST_DEFECT', 'MUST_FAIL', 'GATE_STATUS_LIST_DEFECT')
def _m08(env, w):
    out = w.build_p1('m08')
    pins, _plan, _gl = w.outputs(out)
    gl = w.a_list(out)                       # classifier A's list form (c2v003); g2 removed
    gl['gates'] = [g for g in gl['gates'] if g['gate_sha256'] != w.g2['sha256']]
    d = env.dir('cases', 'm08')
    gp = wjson(os.path.join(d, 'gate_list_defective.json'), gl)
    cin = wjson(os.path.join(d, 'check_in.json'), {'schema': 'CHECK_GATE_LIST_INPUT_C2V003', 'roster_pins': pins,
                                                   'gate_status_list': gp,
                                                   'build_record': pin(os.path.join(out, 'BUILD_RECORD.json'))})
    r = run_cli(['check-gate-list', '--input', cin['path'], '--input-sha256', cin['sha256'], '--out',
                 os.path.join(d, 'check_out.json')])
    assert r.returncode == 3, (r.returncode, r.stderr)
    raise env.rb.Stop(json.loads(r.stderr)['stop'])


# ---------------- validity-only: the in-memory pass driver ----------------

@case('V01_cli_pass_phase1_pass_one_writes_only_a_value_free_pass_record', 'MUST_PASS')
def _v01(env, w):
    out = w.build_p1('v01')
    d = env.dir('cases', 'v01')
    w.b1.activate()
    doc = {'schema': 'PASS_INPUT_C2V003', 'pass_label': 'PASS_ONE', 'freeze_module': w.b1.fm_pin,
           'build_record': pin(os.path.join(out, 'BUILD_RECORD.json')),
           'replay_plan': pin(os.path.join(out, 'REPLAY_PLAN.json')),
           'roster_pins': pin(os.path.join(out, 'ROSTER_PINS.json')), 'selection': w.b1.sel, 'spec': w.b1.spec_pin,
           'null_direction_rule': NULL_RULE}
    ip = wjson(os.path.join(d, 'pass_in.json'), doc)
    po = os.path.join(d, 'pass_out')
    rc, so, se = main_in_process(env, ['pass', '--input', ip['path'], '--input-sha256', ip['sha256'],
                                       '--out-dir', po])
    assert rc == 0, (rc, se)
    assert sorted(os.listdir(po)) == ['PASS_RECORD.json'], os.listdir(po)
    rec = jload(os.path.join(po, 'PASS_RECORD.json'))
    assert_value_free(rec, 'PASS_RECORD')
    assert_value_free(json.loads(so), 'stdout')
    assert rec['replay_plan_sha256'] == pin(os.path.join(out, 'REPLAY_PLAN.json'))['sha256']
    assert rec['alternatives'][PRIMARY]['budget'] == 3 and rec['sensitivity']['budget'] == 0


@case('V02_cli_pass_phase2_pass_one_writes_record_and_whitelisted_value_free_plan', 'MUST_PASS')
def _v02(env, w):
    p = P2(env, w, w.b1, 'v02')
    d = env.dir('cases', 'v02')
    w.b1.activate()
    doc = {'schema': 'PASS_INPUT_C2V003', 'pass_label': 'PASS_ONE', 'freeze_module': w.b1.fm_pin,
           'build_record': pin(os.path.join(p.m_out, 'BUILD_RECORD.json')),
           'replay_plan': pin(os.path.join(p.m_out, 'REPLAY_PLAN.json')),
           'roster_pins': pin(os.path.join(p.m_out, 'ROSTER_PINS.json')), 'selection': w.b1.sel,
           'spec': w.b1.spec_pin, 'null_direction_rule': NULL_RULE}
    ip = wjson(os.path.join(d, 'pass_in.json'), doc)
    po = os.path.join(d, 'pass_out')
    rc, _so, se = main_in_process(env, ['pass', '--input', ip['path'], '--input-sha256', ip['sha256'],
                                        '--out-dir', po])
    assert rc == 0, (rc, se)
    assert sorted(os.listdir(po)) == ['PASS_RECORD.json', 'SENSITIVITY_PLAN_VALUE_FREE.json'], os.listdir(po)
    for nm in os.listdir(po):
        assert_value_free(jload(os.path.join(po, nm)), nm)
    sp = jload(os.path.join(po, 'SENSITIVITY_PLAN_VALUE_FREE.json'))
    assert sp['per_query'] == [] and sp['per_target'] == [] and len(sp['evaluations']) == 6
    with open(os.path.join(po, 'SENSITIVITY_PLAN_VALUE_FREE.json'), 'rb') as f1, open(p.sens_plan['path'], 'rb') as f2:
        assert f1.read() == f2.read()      # the CLI writes the same bytes the in-process driver returned


@case('V03_c2v001_pass_record_command_is_removed', 'MUST_FAIL', 'USAGE')
def _v03(env, w):
    d = env.dir('cases', 'v03')
    ip = wjson(os.path.join(d, 'in.json'), {'schema': 'PASS_RECORD_INPUT_C2V001'})
    r = run_cli(['pass-record', '--input', ip['path'], '--input-sha256', ip['sha256'], '--out',
                 os.path.join(d, 'out.json')])
    assert r.returncode == 2 and not os.path.exists(os.path.join(d, 'out.json')), (r.returncode, r.stderr)
    raise env.rb.Refused(json.loads(r.stderr)['refused'])


@case('V04_pass_with_roster_pins_of_another_build_refused', 'MUST_FAIL', 'PASS_ROSTER_PINS_NOT_OF_BUILD')
def _v04(env, w):
    o1, o2 = w.build_p1('v04a'), w.build_p1('v04b')
    expect_refusal(env.rb, lambda: drive(env, w.b1, o1, 'PASS_ONE',
                                         roster_pins=pin(os.path.join(o2, 'ROSTER_PINS.json'))),
                   'PASS_ROSTER_PINS_NOT_OF_BUILD')


@case('V05_pass_k_under_a_members_stage_plan_refused', 'MUST_FAIL', 'PASS_K_STAGE')
def _v05(env, w):
    p = P2(env, w, w.b1, 'v05')
    expect_refusal(env.rb, lambda: drive(env, w.b1, p.m_out, 'PASS_K'), 'PASS_K_STAGE')


@case('V06_saved_sensitivity_plan_with_a_non_whitelisted_key_refused', 'MUST_FAIL', 'SENSITIVITY_PLAN_NOT_VALUE_FREE')
def _v06(env, w):
    p = P2(env, w, w.b1, 'v06')
    doc = jload(p.sens_plan['path'])
    doc['reference_speeds_note'] = 'any extra key'
    leaky = wjson(os.path.join(p.d, 'plan_extra_key.json'), doc)
    expect_refusal(env.rb, lambda: p.full('v06_full', sensitivity_plan_output=leaky),
                   'SENSITIVITY_PLAN_NOT_VALUE_FREE')


@case('V07_pass_under_another_freeze_module_pin_refused', 'MUST_FAIL', 'PASS_FREEZE_MODULE_NOT_OF_BUILD')
def _v07(env, w):
    out = w.build_p1('v07')
    expect_refusal(env.rb, lambda: drive(env, w.b1, out, 'PASS_ONE',
                                         freeze_module={'path': V003G_PATH, 'sha256': '7' * 64}),
                   'PASS_FREEZE_MODULE_NOT_OF_BUILD')


# ---------------- Phase 2 ----------------

class P2:
    """Phase-2 flow: MEMBERS stage, pass one (driver), value-free sensitivity plan, sensitivity calls, FULL stage."""

    def __init__(self, env, w, base, tag, stage0_calls=None):
        self.env, self.w, self.b = env, w, base
        d = env.dir('cases', tag)
        self.d = d
        b = base
        th = b.thetas
        self.calls = []
        for alt in base.evaluated:
            if alt == STAGE0 and stage0_calls is not None:
                self.calls += stage0_calls(d, th)
                continue
            for i, k in enumerate(('M000', 'M001', 'M002')):
                self.calls.append(b.call(d, alt, 'MEMBER', k, th[k], [('FINISHED', '2026-10-30T0%d:00:00Z' % i)],
                                         cut_kpc=(38.5, None, 30.5)[i],
                                         gate_rows=({'SYN-Q20': 'SYN_GATE_REASON'} if i == 0 else None),
                                         seed=float(i) + (0.5 if alt != PRIMARY else 0.0)))
        common = {'plan_outputs': {a: b.plan_outputs[a] for a in b.evaluated}, 'calls': self.calls,
                  'gate_cutoff': {'kind': 'PHASE1_SCORE', 'v006_copy': w.cutoff},
                  'gate_documents': [w.g1, w.g2], 'receipt_keys': RECEIPT_KEYS, 'receipt_status_classes': CLASSES}
        self.common = common
        self.m_out = env.fresh(tag + '_members')
        b.build(b.input(d, 'PHASE_2', 'MEMBERS', common), self.m_out)
        self.m_pins, self.m_plan, _ = World.outputs(self.m_out)
        self.rec1, extract, self.pass_one_mem = drive(env, b, self.m_out, 'PASS_ONE')
        self.p1_pin = save(env, d, 'pass_one_record.json', self.rec1)
        self.sens_plan = save(env, d, 'sensitivity_plan_value_free.json', extract)
        self.sens_calls = []
        for i, e in enumerate(extract['evaluations']):
            if e['skipped_zero_displacement']:
                continue
            geometry = e['kind'] == 'NGC3198_NUISANCE'
            b.sens_tsha[e['entry_id']] = tsha(e['theta_ngc'])
            att = ([('FAILED_SOLVER', '2026-10-31T0%d:00:00Z' % i, ev()),
                    ('FAILED_SOLVER', '2026-10-31T1%d:00:00Z' % i, ev(raised=True))]
                   if geometry else [('FINISHED', '2026-10-31T0%d:30:00Z' % i)])
            self.sens_calls.append(b.call(d, PRIMARY, 'SENSITIVITY', e['entry_id'], e['theta_ngc'], att,
                                          result='failure' if geometry else 'valid', seed=10.0 + i))

    def full(self, tag, **over):
        b = self.b
        x = dict(self.common, calls=self.calls + self.sens_calls, sensitivity_plan_output=self.sens_plan,
                 members_stage_rosters=self.m_pins,
                 members_stage_build_record=pin(os.path.join(self.m_out, 'BUILD_RECORD.json')),
                 m15=self.w.m15, other_phase_calls=[])
        x.update(over)
        out = self.env.fresh(tag)
        b.build(b.input(self.d, 'PHASE_2', 'FULL', x), out)
        return out


@case('P01_phase2_members_then_full_member_contexts_byte_identical_end_to_end', 'MUST_PASS')
def _p01(env, w):
    p = P2(env, w, w.b1, 'p01')
    out = p.full('p01_full')
    pins, plan, gl = World.outputs(out)
    mctx = jload(p.m_pins[PRIMARY]['path'])['outer_cut']['contexts']
    fctx = jload(pins[PRIMARY]['path'])['outer_cut']['contexts']
    assert len(mctx) == 3 and len(fctx) == 9 and fctx[:3] == mctx
    assert plan['sensitivity']['budget'] == 6
    assert env.rb.sensitivity_budget(plan, jload(p.sens_plan['path']))['budget'] == 6
    assert [a['member_budget'] for a in plan['alternatives'] if a['name'] in (PRIMARY, OK_ALT)] == [3, 3]
    assert plan['pass_one']['replay_plan_sha256'] == pin(os.path.join(p.m_out, 'REPLAY_PLAN.json'))['sha256']
    reck, _x, mem = drive(env, w.b1, out, 'PASS_K')
    assert mem['reference']['member_id'] == p.pass_one_mem['reference']['member_id'] == 'M002'
    assert mem['sensitivity']['status'] == 'COMPLETE' and mem['envelopes'][OK_ALT]['status'] == 'COMPLETE'
    inc = frozen_checks(w.b1, mem, pins)
    assert inc == [], inc
    res, _raw, succ = step7(env, out, pin(os.path.join(out, 'REPLAY_PLAN.json')), p.p1_pin,
                            save(env, p.d, 'pk.json', reck))
    assert res['status'] == 'NO_NEW_DISCREPANCY' and succ is None, res
    assert plan['stage0_status']['status'] == 'NOT_EVALUATED_BEFORE_FREEZE'
    assert plan['stage0_status']['reasons'] == ['NO_SEALED_SUCCESSOR']
    assert plan['step4']['start_utc'] == '2026-10-31T15:00:00Z'
    gl1 = World.outputs(w.build_p1('p01_gl'))[2]
    assert [(g['gate'], g['status']) for g in gl['gates']] == [(g['gate'], g['status']) for g in gl1['gates']]


class Discrepancy:
    """Phase 2 with a step-7 discrepancy on M001: FULL build, a discrepant pass k, step 7 through the CLI."""

    def __init__(self, env, w, tag):
        self.env, self.w = env, w
        p = P2(env, w, w.b1, tag)
        self.p = p
        self.out = p.full(tag + '_full')
        self.pins, self.plan, _ = World.outputs(self.out)
        self.plan_pin = pin(os.path.join(self.out, 'REPLAY_PLAN.json'))
        self.br = pin(os.path.join(self.out, 'BUILD_RECORD.json'))
        # an agreeing pass k made under the FULL plan before step 7 runs (the driver refuses it afterwards, K08)
        self.rec_agree, _x, _m = drive(env, w.b1, self.out, 'PASS_K')
        self.pk_agree = save(env, p.d, 'pass_k_agreeing.json', self.rec_agree)
        reck, _x, _m = drive(env, w.b1, self.out, 'PASS_K', fm=discrepant_fm(env, w.b1))
        self.pk = save(env, p.d, 'pass_k_discrepant.json', reck)
        d = env.dir('cases', tag, 'cli')
        sin = wjson(os.path.join(d, 'step7_in.json'), {'schema': 'STEP7_INPUT_C2V003', 'build_record': self.br,
                                                       'replay_plan': self.plan_pin, 'pass_one': p.p1_pin,
                                                       'pass_k': self.pk})
        self.so = os.path.join(d, 'step7_out')
        r = run_cli(['step7', '--input', sin['path'], '--input-sha256', sin['sha256'], '--out-dir', self.so])
        assert r.returncode == 0, r.stderr
        self.res = jload(os.path.join(self.so, 'STEP7_RESULT.json'))
        self.succ_pin = pin(os.path.join(self.so, 'REPLAY_PLAN.json'))
        self.succ = jload(self.succ_pin['path'])

    def pass_k(self, plan_pin=None):
        rec, _x, mem = drive(self.env, self.w.b1, self.out, 'PASS_K', plan_pin=plan_pin)
        return rec, mem


@case('P02_step7_discrepancy_makes_member_UNEVALUATED_never_resolved_successor_chain', 'MUST_PASS')
def _p02(env, w):
    x = Discrepancy(env, w, 'p02')
    assert sorted(os.listdir(x.so)) == ['REPLAY_PLAN.json', 'STEP7_RESULT.json']   # no roster is ever written
    res = x.res
    assert res['status'] == 'NEW_UNEVALUATED' and res['seq'] == 1, res
    assert {(e['alternative'], e['member_id']) for e in res['new_unevaluated']} == {
        (PRIMARY, 'M001'), (OK_ALT, 'M001')}, res
    assert sorted(os.listdir(ledger_dir(x.out))) == sorted(
        ['LEDGER_GENESIS.json', 'STEP7_0001.json', 'PLAN_%s.json' % x.succ_pin['sha256'],
         'PASS_%s.json' % x.p.p1_pin['sha256'], 'PASS_%s.json' % x.pk['sha256']])
    succ = x.succ
    assert succ['registered_roster_sha256'] == x.plan['registered_roster_sha256']
    assert succ['predecessor_sha256'] == x.plan_pin['sha256']
    pa = [a for a in succ['alternatives'] if a['name'] == PRIMARY][0]
    assert pa['member_budget'] == 1 and [m['effective_disposition'] for m in pa['members']] == [
        'EVALUATED', 'UNEVALUATED_STEP7_DISCREPANCY', 'UNEVALUATED_BY_ORDER_TRUNCATION']
    assert succ['sensitivity']['budget'] is None
    # pass three under the successor (driver): D1 moves to M000, the new plan has no saved calls, FREEZE_INCOMPLETE
    rec3, mem3 = x.pass_k(plan_pin=x.succ_pin)
    assert mem3['reference']['member_id'] == 'M000'
    assert rec3['sensitivity_budget_source'] == 'SENS_BUDGET_RULE' and rec3['sensitivity']['budget'] == 0
    assert rec3['alternatives'][PRIMARY]['budget'] == 1
    inc = frozen_checks(w.b1, mem3, x.pins)
    assert 'PRIMARY_MEMBER_EVALUATION_BUDGET_EXHAUSTED' in inc and 'SENSITIVITY_BUDGET_EXHAUSTED' in inc, inc
    res3, _raw, succ3 = step7(env, x.out, x.succ_pin, x.p.p1_pin, save(env, x.p.d, 'pass3.json', rec3))
    assert res3['status'] == 'NO_NEW_DISCREPANCY' and succ3 is None and res3['seq'] == 2, res3
    assert res3['checks']['pass_k_member_budget'][PRIMARY] == 1


@case('K01_pass_three_at_the_original_budget_under_the_successor_refused_A3a', 'MUST_FAIL',
      'STEP7_PASS_BUDGET_MISMATCH')
def _k01(env, w):
    x = Discrepancy(env, w, 'k01')
    rec = copy.deepcopy(x.rec_agree)                     # budget 3, the original plan's
    rec['replay_plan_sha256'] = x.succ_pin['sha256']      # forged claim: run under the successor (budget 1)
    rec['sensitivity_budget_source'] = 'SENS_BUDGET_RULE'  # and the successor's sensitivity rule (D1 unchanged: 6)
    forged = save(env, x.p.d, 'pass3_forged.json', rec)
    try:
        step7(env, x.out, x.succ_pin, x.p.p1_pin, forged)
    except env.rb.Refused as exc:
        assert exc.code == 'STEP7_PASS_BUDGET_MISMATCH' and 'ran at budget 3; the plan says 1' in exc.detail, exc
        raise
    raise AssertionError('no refusal')


@case('K02_pass_of_another_plan_given_with_the_successor_refused_A3e', 'MUST_FAIL', 'STEP7_PASS_NOT_OF_THIS_PLAN')
def _k02(env, w):
    x = Discrepancy(env, w, 'k02')
    expect_refusal(env.rb, lambda: step7(env, x.out, x.succ_pin, x.p.p1_pin, x.pk_agree),
                   'STEP7_PASS_NOT_OF_THIS_PLAN')


@case('K03_superseded_plan_reused_with_an_agreeing_rerun_refused_A3b', 'MUST_FAIL', 'STEP7_PLAN_SUPERSEDED')
def _k03(env, w):
    x = Discrepancy(env, w, 'k03')
    expect_refusal(env.rb, lambda: step7(env, x.out, x.plan_pin, x.p.p1_pin, x.pk_agree), 'STEP7_PLAN_SUPERSEDED')


@case('K04_hand_edited_successor_restoring_M001_refused_A3c', 'MUST_FAIL', 'PLAN_NOT_OF_BUILD_RECORD')
def _k04(env, w):
    x = Discrepancy(env, w, 'k04')
    s = copy.deepcopy(x.succ)
    for a in s['alternatives']:
        if a['name'] in (PRIMARY, OK_ALT):
            a['members'][1]['own_disposition'] = 'EVALUATED'
            a['member_budget'] = 3
            for m in a['members']:
                m['effective_disposition'] = m['own_disposition']
    edited = save(env, x.p.d, 'successor_edited.json', s)
    rec = copy.deepcopy(x.rec_agree)
    rec['replay_plan_sha256'] = edited['sha256']
    pk = save(env, x.p.d, 'pass_k_for_edited.json', rec)
    expect_refusal(env.rb, lambda: step7(env, x.out, edited, x.p.p1_pin, pk), 'PLAN_NOT_OF_BUILD_RECORD')


@case('K05_plan_with_edited_registered_roster_sha_refused_A3d', 'MUST_FAIL', 'PLAN_NOT_OF_BUILD_RECORD')
def _k05(env, w):
    p = P2(env, w, w.b1, 'k05')
    out = p.full('k05_full')
    plan = jload(os.path.join(out, 'REPLAY_PLAN.json'))
    plan['registered_roster_sha256'][PRIMARY] = p.m_pins[PRIMARY]['sha256']
    edited = save(env, p.d, 'plan_edited.json', plan)
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    pk = save(env, p.d, 'pk.json', reck)
    expect_refusal(env.rb, lambda: step7(env, out, edited, p.p1_pin, pk), 'PLAN_NOT_OF_BUILD_RECORD')


@case('K06_pass_k_sensitivity_budget_not_the_plans_refused', 'MUST_FAIL', 'STEP7_PASS_BUDGET_MISMATCH')
def _k06(env, w):
    p = P2(env, w, w.b1, 'k06')
    out = p.full('k06_full')
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    reck['sensitivity']['budget'] = 2
    pk = save(env, p.d, 'pk_sens_forged.json', reck)
    expect_refusal(env.rb, lambda: step7(env, out, pin(os.path.join(out, 'REPLAY_PLAN.json')), p.p1_pin, pk),
                   'STEP7_PASS_BUDGET_MISMATCH')


@case('K07_forged_ledger_entry_on_a_superseded_plan_breaks_the_ledger', 'MUST_FAIL', 'STEP7_LEDGER_BROKEN')
def _k07(env, w):
    x = Discrepancy(env, w, 'k07')
    led = ledger_dir(x.out)
    with open(os.path.join(led, 'STEP7_0001.json'), 'rb') as f:
        raw1 = f.read()
    r = json.loads(raw1)
    r.update({'seq': 2, 'previous_result_sha256': sha(raw1), 'status': 'NO_NEW_DISCREPANCY', 'new_unevaluated': [],
              'successor_replay_plan_sha256': None})
    wbytes(os.path.join(led, 'STEP7_0002.json'), env.rb.dump_bytes(r))
    expect_refusal(env.rb, lambda: step7(env, x.out, x.succ_pin, x.p.p1_pin, x.pk), 'STEP7_LEDGER_BROKEN')


@case('K09_ledger_result_that_does_not_re_derive_from_its_stored_passes_refused', 'MUST_FAIL', 'STEP7_LEDGER_BROKEN')
def _k09(env, w):
    out = w.build_p1('k09')
    d = env.dir('cases', 'k09')
    rec1, _x, _m = drive(env, w.b1, out, 'PASS_ONE')
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    root = pin(os.path.join(out, 'REPLAY_PLAN.json'))
    res, raw1, _succ = step7(env, out, root, save(env, d, 'p1.json', rec1), save(env, d, 'pk.json', reck))
    assert res['status'] == 'NO_NEW_DISCREPANCY'
    # forge a NEW_UNEVALUATED entry from the same passes, with a successor made exactly as step 7 would make it
    succ_raw = env.rb.dump_bytes(env.rb._apply_unevaluated(jload(root['path']), root['sha256'], [(PRIMARY, 'M000')]))
    led = ledger_dir(out)
    wbytes(os.path.join(led, 'PLAN_%s.json' % sha(succ_raw)), succ_raw)
    r2 = dict(res, seq=2, previous_result_sha256=sha(raw1), status='NEW_UNEVALUATED',
              new_unevaluated=[{'alternative': PRIMARY, 'member_id': 'M000'}],
              successor_replay_plan_sha256=sha(succ_raw))
    wbytes(os.path.join(led, 'STEP7_0002.json'), env.rb.dump_bytes(r2))
    expect_refusal(env.rb, lambda: step7(env, out, root, save(env, d, 'p1b.json', rec1),
                                         save(env, d, 'pkb.json', reck)), 'STEP7_LEDGER_BROKEN')


@case('K08_pass_driver_refuses_a_superseded_plan', 'MUST_FAIL', 'PASS_PLAN_SUPERSEDED')
def _k08(env, w):
    x = Discrepancy(env, w, 'k08')
    expect_refusal(env.rb, lambda: x.pass_k(), 'PASS_PLAN_SUPERSEDED')


@case('P03_step7_pass_under_a_successor_roster_refused', 'MUST_FAIL', 'STEP7_ROSTER_NOT_REGISTERED')
def _p03(env, w):
    p = P2(env, w, w.b1, 'p03')
    out = p.full('p03_full')
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    reck['alternatives'][PRIMARY]['roster'] = {'path': '/synthetic/successor_roster.json', 'sha256': 'a' * 64}
    pk = save(env, p.d, 'pk_roster.json', reck)
    expect_refusal(env.rb, lambda: step7(env, out, pin(os.path.join(out, 'REPLAY_PLAN.json')), p.p1_pin, pk),
                   'STEP7_ROSTER_NOT_REGISTERED')


@case('P04_full_stage_member_context_changed_since_members_stage_refused', 'MUST_FAIL', 'MEMBER_CONTEXTS_CHANGED')
def _p04(env, w):
    p = P2(env, w, w.b1, 'p04')
    b = w.b1
    d = env.dir('cases', 'p04', 'relaunch')
    new0 = b.call(d, PRIMARY, 'MEMBER', 'M000', b.thetas['M000'], [('FINISHED', '2026-10-30T05:00:00Z')],
                  cut_kpc=36.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'})
    calls = [new0 if (c['alternative'], c['key']) == (PRIMARY, 'M000') else c for c in p.calls]
    expect_refusal(env.rb, lambda: p.full('p04_full', calls=calls + p.sens_calls), 'MEMBER_CONTEXTS_CHANGED')


@case('P06_phase2_gate_cutoff_must_be_the_phase1_score_copy', 'MUST_FAIL', 'GATE_CUTOFF_KIND')
def _p06(env, w):
    p = P2(env, w, w.b1, 'p06')
    expect_refusal(env.rb, lambda: p.full('p06_full', gate_cutoff={'kind': 'PHASE1_STEP4_START',
                                                                   'v006_copy': w.cutoff}), 'GATE_CUTOFF_KIND')


@case('P07_phase2_full_without_a_sensitivity_call_record_refused', 'MUST_FAIL', 'CALL_RECORD_MISSING')
def _p07(env, w):
    p = P2(env, w, w.b1, 'p07')
    expect_refusal(env.rb, lambda: p.full('p07_full', calls=p.calls + p.sens_calls[:-1]), 'CALL_RECORD_MISSING')


@case('P08_sensitivity_plan_saved_with_reference_values_refused', 'MUST_FAIL', 'SENSITIVITY_PLAN_NOT_VALUE_FREE')
def _p08(env, w):
    p = P2(env, w, w.b1, 'p08')
    leaky = wjson(os.path.join(p.d, 'sensitivity_plan_with_values.json'),
                  json.loads(json.dumps(p.pass_one_mem['sensitivity'])))
    expect_refusal(env.rb, lambda: p.full('p08_full', sensitivity_plan_output=leaky),
                   'SENSITIVITY_PLAN_NOT_VALUE_FREE')


@case('P09_step7_selection_difference_is_a_stop_not_a_member_mark', 'MUST_PASS')
def _p09(env, w):
    p = P2(env, w, w.b1, 'p09')
    out = p.full('p09_full')
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    reck['alternatives'][PRIMARY]['members'][2]['theta_sha256'] = 'b' * 64
    pk = save(env, p.d, 'pk_sel.json', reck)
    res, _raw, succ = step7(env, out, pin(os.path.join(out, 'REPLAY_PLAN.json')), p.p1_pin, pk)
    assert res['status'] == 'STOP_NOT_MECHANIZED' and succ is None and res['new_unevaluated'] == [], res


@case('P05_stage0_receipt_rule_M14', 'MUST_PASS')
def _p05(env, w):
    b2 = w.b2

    def fin(d, th):
        return [b2.call(d, STAGE0, 'MEMBER', k, th[k], [('FINISHED', '2026-11-01T0%d:00:00Z' % i)], seed=20.0 + i)
                for i, k in enumerate(('M000', 'M001', 'M002'))]

    def one_failed(d, th):
        c = fin(d, th)
        c[2] = b2.call(env.dir('cases', 'p05b', 'f'), STAGE0, 'MEMBER', 'M002', th['M002'],
                       [('FAILED_SOLVER', '2026-11-01T02:00:00Z', ev()),
                        ('FAILED_SOLVER', '2026-11-02T02:00:00Z', ev(raised=True))], result='failure')
        return c
    p = P2(env, w, b2, 'p05a', stage0_calls=fin)
    out = p.full('p05a_full')
    pins, plan, _ = World.outputs(out)
    st = plan['stage0_status']
    assert st['status'] == 'EVALUATED_BEFORE_FREEZE' and st['reasons'] == [] and len(st['receipts']) == 3, st
    assert [a['mode'] for a in plan['alternatives'] if a['name'] == STAGE0] == ['PER_THETA']
    assert st['step4_start_utc'] == '2026-11-01T02:00:00Z'
    _rec, _x, mem = drive(env, b2, out, 'PASS_K')
    frozen_checks(b2, mem, pins)
    q = P2(env, w, b2, 'p05b', stage0_calls=one_failed)
    _pins, plan2, _ = World.outputs(q.full('p05b_full'))
    st2 = plan2['stage0_status']
    assert st2['status'] == 'NOT_EVALUATED_BEFORE_FREEZE' and st2['reasons'] == ['STAGE0_RECEIPT_NOT_FINISHED']


# ---------------- M-6 seal check (seal-entry format proposed under G17) ----------------

class Seal:
    def __init__(self, env, tag, tsr=None, manifest_files=None, extra_lines='', heading_token='SEAL_ENTRY'):
        d = env.dir('cases', tag)
        self.d = d
        self.text = wbytes(os.path.join(d, 'prereg_text.md'), b'synthetic sealed text\n')
        self.cls = wbytes(os.path.join(d, 'classifier.py'), b'# synthetic classifier\n')
        self.withdrawn = wbytes(os.path.join(d, 'classifier_withdrawn.py'), b'# synthetic withdrawn classifier\n')
        self.tsr = tsr or {'path': os.path.realpath(TSR_RECORD_PATH), 'sha256': TSR_RECORD_SHA}
        self.other = wbytes(os.path.join(d, 'older.json'), b'{"older": true}\n')
        body = ('# synthetic V006\n\n## A950: an older entry\n\n- `%s`\n\n'
                '## A955: a classifier is withdrawn\n\n- the withdrawn classifier `%s`\n\n'
                '## A960: %s PHASE_1 of the text %s\n\n'
                '- PREREG_TEXT: `%s`\n- CLASSIFIER: `%s` (replaces the withdrawn `%s`)\n'
                '- TSR_FLAG_RECORD: `%s`\n%s\n## A961: a later entry\n\n- nothing\n') % (
            self.other['sha256'], self.withdrawn['sha256'], heading_token, self.text['sha256'], self.text['sha256'],
            self.cls['sha256'], self.withdrawn['sha256'], self.tsr['sha256'], extra_lines)
        self.v006 = wbytes(os.path.join(d, 'v006_after_seal.md'), body.encode())
        files = manifest_files if manifest_files is not None else [self.tsr]
        self.manifest = wjson(os.path.join(d, 'freeze_manifest_standin.json'), {'pins': {'input_files': [
            {'path': p['path'], 'sha256': p['sha256'], 'bytes': 1} for p in files]}})

    def objects(self, **over):
        o = {'PREREG_TEXT': self.text, 'CLASSIFIER': self.cls, 'TSR_FLAG_RECORD': self.tsr}
        o.update(over)
        return [{'role': k, 'path': v['path'], 'sha256': v['sha256']} for k, v in o.items() if v is not None]

    def check(self, env, objects=None):
        return env.rb.seal_check(self.v006, objects or self.objects(), self.manifest)


def tsr_variant(env, tag):
    """An unsealed variant of the production flag record: the same content in other bytes (c2v003: V002 has no
    free-text field outside A's schema, so the variant differs in serialization only; any changed byte stops)."""
    rec = jload(TSR_RECORD_PATH)
    raw = (json.dumps(rec, indent=2, sort_keys=True) + '\n').encode()
    return wbytes(os.path.join(env.dir('cases', tag), 'tsr_flag_record_unsealed_variant.json'), raw)


@case('S01_seal_check_passes_when_every_sealed_sha_matches_its_bytes_and_role_line', 'MUST_PASS')
def _s01(env, w):
    s = Seal(env, 's01')
    r = s.check(env)
    assert r['verdict'] == 'PASS' and r['seal_entry_heading'].startswith('A960'), r


@case('S02_sealed_object_bytes_changed_SEAL_SHA_MISMATCH_cli_exit_3', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s02(env, w):
    s = Seal(env, 's02')
    swapped = wbytes(os.path.join(s.d, 'classifier_edited.py'), b'# synthetic classifier, edited\n')
    objs = s.objects()
    objs[1]['path'] = swapped['path']     # the sealed sha256 stays; the bytes at the path differ
    cin = wjson(os.path.join(s.d, 'seal_in.json'), {'schema': 'SEAL_CHECK_INPUT_C2V003', 'v006_copy': s.v006,
                                                    'objects': objs, 'freeze_manifest': s.manifest})
    outp = os.path.join(s.d, 'seal_out.json')
    r = run_cli(['seal-check', '--input', cin['path'], '--input-sha256', cin['sha256'], '--out', outp])
    assert r.returncode == 3, (r.returncode, r.stderr)
    assert jload(outp)['verdict'] == 'STOP'
    err = json.loads(r.stderr)
    assert "['CLASSIFIER']" in err['detail'] and '[]' in err['detail'], err
    raise env.rb.Stop(err['stop'])


@case('S03_sha_not_on_its_role_line_SEAL_SHA_MISMATCH', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s03(env, w):
    s = Seal(env, 's03')
    expect_refusal(env.rb, lambda: s.check(env, s.objects(CLASSIFIER=s.other)), 'SEAL_SHA_MISMATCH')


@case('S04_missing_sealed_role_SEAL_SHA_MISMATCH', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s04(env, w):
    s = Seal(env, 's04')
    expect_refusal(env.rb, lambda: s.check(env, s.objects(TSR_FLAG_RECORD=None)), 'SEAL_SHA_MISMATCH')


@case('S05_classifier_given_as_the_sealed_prereg_text_refused_A4c', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s05(env, w):
    s = Seal(env, 's05')
    try:
        s.check(env, s.objects(CLASSIFIER=s.text))
    except env.rb.Stop as exc:
        assert 'two roles name one sha256' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('S06_all_three_roles_given_as_one_sealed_file_refused_A4d', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s06(env, w):
    s = Seal(env, 's06')
    try:
        s.check(env, s.objects(CLASSIFIER=s.text, TSR_FLAG_RECORD=s.text))
    except env.rb.Stop as exc:
        assert 'two roles name one sha256' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('S07_withdrawn_classifier_named_only_as_replaced_refused_A4e', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s07(env, w):
    s = Seal(env, 's07')
    try:
        s.check(env, s.objects(CLASSIFIER=s.withdrawn))
    except env.rb.Stop as exc:
        assert exc.detail == "roles ['CLASSIFIER']; []", exc.detail
        raise
    raise AssertionError('no stop')


@case('S08_freeze_input_files_list_an_unsealed_flag_record_refused_A5g', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s08(env, w):
    var = tsr_variant(env, 's08')
    s = Seal(env, 's08', manifest_files=[var])
    try:
        s.check(env)
    except env.rb.Stop as exc:
        assert 'FREEZE_INPUT_FILES_LACK_SEALED_TSR_FLAG_RECORD' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('S09_sealed_flag_record_not_the_pinned_production_record_refused', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s09(env, w):
    var = tsr_variant(env, 's09')
    s = Seal(env, 's09', tsr=var, manifest_files=[var])
    try:
        s.check(env)
    except env.rb.Stop as exc:
        assert 'SEALED_TSR_FLAG_RECORD_NOT_THE_PINNED_RECORD' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('S10_seal_entry_naming_a_role_twice_refused', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s10(env, w):
    s = Seal(env, 's10', extra_lines='- CLASSIFIER: `%s`\n' % ('d' * 64))
    expect_refusal(env.rb, lambda: s.check(env), 'SEAL_SHA_MISMATCH')


@case('S11_seal_entry_role_not_supplied_refused', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s11(env, w):
    s = Seal(env, 's11', extra_lines='- BAND_AGREE: `%s`\n' % ('c' * 64))
    expect_refusal(env.rb, lambda: s.check(env), 'SEAL_SHA_MISMATCH')


@case('S12_heading_without_SEAL_ENTRY_token_is_not_a_seal_entry', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _s12(env, w):
    s = Seal(env, 's12', heading_token='registration')
    expect_refusal(env.rb, lambda: s.check(env), 'SEAL_SHA_MISMATCH')


# ---------------- M-7 TSR check ----------------

class SynTsr:
    """Synthetic stand-ins with synthetic pins: compare, N1, node and a flag record in classifier A's
    TSR_FLAG_RECORD_C4V001 schema (the production V003 form: c2v006 adds `schema`, A173)."""

    def __init__(self, env, tag):
        d = env.dir('cases', tag)
        self.d = d
        self.rr = [1.1 * (k + 1) for k in range(10)]
        ring = {'ordinal': 3, 'classification': 'TRUNCATION_SHAPE', 'S_over_theta': 1.01, 'criterion_over_theta':
                1.01, 'criterion': 'C1', 'R_kpc': self.rr[3], 'radial_support': {'kind': 'sampled_ring',
                                                                                   'R_kpc': self.rr[3]}}
        self.ring = ring
        self.compare = wjson(os.path.join(d, 'compare.json'), {
            'schema': 'NGC_NTEST_COMPARE_C2V002', 'failing_TRUNCATION_SHAPE_rings': [ring],
            'failing_non_TRUNCATION_SHAPE_rings': [], 'n_route_ab_gate': 'OPEN'})
        self.n1 = wjson(os.path.join(d, 'n1.json'), {'ring_radii_kpc': self.rr})
        self.node = wjson(os.path.join(d, 'node.json'), {'orders': {'4': {'radii_kpc': self.rr}}})
        self.ids = ['SYN-Q%02d' % i for i in range(1, 44)]
        self.rule = jload(TSR_RECORD_PATH)['rule']
        self.expected = {'compare_sha256': self.compare['sha256'], 'n1_sha256': self.n1['sha256'],
                         'node_sha256': self.node['sha256'], 'failing_ordinal': 3, 'lower_kpc': self.rr[2],
                         'upper_kpc': self.rr[4], 'flagged_ids': ['SYN-Q04'], 'all_ids': self.ids,
                         'rule': self.rule}

    def record(self, name, mutate=None, compare=None):
        rec = {'schema': 'TSR_FLAG_RECORD_C4V001', 'target_free': True, 'rule': self.rule, 'failing_ring_ordinal': 3,
               'ntest_compare_pin': compare or self.compare, 'n1_record_pin': self.n1, 'gl_node_record_pin': self.node,
               'flags': [{'query_id': q, 'TRUNCATION_SHAPE_RESIDUAL': q == 'SYN-Q04'} for q in self.ids]}
        if mutate:
            mutate(rec)
        return wjson(os.path.join(self.d, name), rec)

    def manifest(self, name, pins):
        return wjson(os.path.join(self.d, name), {'pins': {'input_files': [
            {'path': p['path'], 'sha256': p['sha256'], 'bytes': 1} for p in pins]}})


@case('T01_production_tsr_flag_record_passes_against_the_pinned_bytes', 'MUST_PASS')
def _t01(env, w):
    """c2v003: the production record is V002 (classifier A's schema); V001 stays the derivation input. c2v006: the
    production record is V003 (V002 plus `schema`, A173)."""
    fr = pin(TSR_RECORD_PATH)
    assert fr['sha256'] == env.rb.PRODUCTION_TSR['flag_record_sha256'] == TSR_RECORD_SHA
    assert pin(TSR_V001_PATH)['sha256'] == env.rb.PRODUCTION_TSR['v001_flag_record_sha256'] == TSR_V001_SHA
    r = env.rb.tsr_check(fr)
    assert r['verdict'] == 'PASS' and r['record_schema'] == 'TSR_FLAG_RECORD_C4V001', r
    rec = jload(TSR_RECORD_PATH)
    assert len(rec['flags']) == 43 and rec['failing_ring_ordinal'] == 15 and rec['target_free'] is True
    assert [f['query_id'] for f in rec['flags'] if f['TRUNCATION_SHAPE_RESIDUAL']] == ['NGC3198-Q25']
    assert env.rb.PRODUCTION_TSR['lower_kpc'] == 9.901810628740723
    assert env.rb.PRODUCTION_TSR['upper_kpc'] == 10.911721936765339
    v1 = jload(TSR_V001_PATH)
    assert v1['pins']['support_record']['status'] == 'PENDING' and 'sha256' not in v1['pins']['support_record']

    def keys(o):
        if isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from keys(v)
        elif isinstance(o, list):
            for v in o:
                yield from keys(v)
    assert not any('target' in k.lower() and k != 'target_free' or k.lower().startswith(('observed', 'vobs'))
                   for k in keys(rec))


@case('T02_synthetic_stand_ins_pass_with_freeze_input_files', 'MUST_PASS')
def _t02(env, w):
    t = SynTsr(env, 't02')
    fr = t.record('flag.json')
    m = t.manifest('manifest.json', [fr, t.compare, t.n1, t.node])
    assert env.rb.tsr_check(fr, m, dict(t.expected, flag_record_sha256=fr['sha256']))['verdict'] == 'PASS'


@case('T03_tampered_flag_record_flags_a_second_row', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _t03(env, w):
    t = SynTsr(env, 't03')

    def mut(rec):
        rec['flags'][4]['TRUNCATION_SHAPE_RESIDUAL'] = True
    expect_refusal(env.rb, lambda: env.rb.tsr_check(t.record('flag.json', mut), None, t.expected),
                   'TSR_FLAG_TABLE_MISMATCH')


@case('T04_tampered_flag_record_bound_made_inclusive', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _t04(env, w):
    """c2v003: classifier A's record carries the bounds only in its rule text (no support block); the bound is
    made inclusive there."""
    t = SynTsr(env, 't04')

    def mut(rec):
        rec['rule'] = rec['rule'].replace('r(k-1) < R_q < r(k+1)', 'r(k-1) <= R_q <= r(k+1)')
        assert rec['rule'] != t.rule
    try:
        env.rb.tsr_check(t.record('flag.json', mut), None, t.expected)
    except env.rb.Stop as exc:
        assert 'RULE_TEXT' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('T05_production_record_tampered_copy_cli_exit_3', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _t05(env, w):
    d = env.dir('cases', 't05')
    rec = jload(TSR_RECORD_PATH)
    rec['flags'][25]['TRUNCATION_SHAPE_RESIDUAL'] = True       # NGC3198-Q26
    fr = wjson(os.path.join(d, 'tampered_flag_record.json'), rec)
    cin = wjson(os.path.join(d, 'tsr_in.json'), {'schema': 'TSR_CHECK_INPUT_C2V003', 'flag_record': fr,
                                                 'freeze_manifest': None})
    r = run_cli(['tsr-check', '--input', cin['path'], '--input-sha256', cin['sha256'], '--out',
                 os.path.join(d, 'tsr_out.json')])
    assert r.returncode == 3, (r.returncode, r.stderr)
    raise env.rb.Stop(json.loads(r.stderr)['stop'])


@case('T06_compare_with_a_second_failing_ring', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _t06(env, w):
    t = SynTsr(env, 't06')
    doc = jload(t.compare['path'])
    extra = dict(t.ring, ordinal=6, R_kpc=t.rr[6])
    doc['failing_TRUNCATION_SHAPE_rings'].append(extra)
    c2 = wjson(os.path.join(t.d, 'compare2.json'), doc)
    exp = dict(t.expected, compare_sha256=c2['sha256'])
    expect_refusal(env.rb, lambda: env.rb.tsr_check(t.record('flag.json', compare=c2), None, exp),
                   'TSR_FLAG_TABLE_MISMATCH')


@case('T07_freeze_input_files_without_the_flag_record', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _t07(env, w):
    t = SynTsr(env, 't07')
    fr = t.record('flag.json')
    m = t.manifest('manifest.json', [t.compare, t.n1, t.node])
    expect_refusal(env.rb, lambda: env.rb.tsr_check(fr, m, t.expected), 'TSR_FLAG_TABLE_MISMATCH')


@case('T08_production_record_with_production_node_and_compare_in_input_files', 'MUST_PASS')
def _t08(env, w):
    d = env.dir('cases', 't08')
    rec = jload(TSR_RECORD_PATH)
    fr = pin(TSR_RECORD_PATH)
    pins = [fr] + [rec[k] for k in ('ntest_compare_pin', 'n1_record_pin', 'gl_node_record_pin')]
    m = wjson(os.path.join(d, 'manifest_standin.json'), {'pins': {'input_files': [
        {'path': p['path'], 'sha256': p['sha256'], 'bytes': 1} for p in pins]}})
    assert env.rb.tsr_check(fr, m)['verdict'] == 'PASS'


@case('T09_unsealed_flag_record_variant_in_input_files_refused_A5g', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _t09(env, w):
    d = env.dir('cases', 't09')
    var = tsr_variant(env, 't09')
    rec = jload(TSR_RECORD_PATH)
    pins = [var] + [rec[k] for k in ('ntest_compare_pin', 'n1_record_pin', 'gl_node_record_pin')]
    m = wjson(os.path.join(d, 'manifest_standin.json'), {'pins': {'input_files': [
        {'path': p['path'], 'sha256': p['sha256'], 'bytes': 1} for p in pins]}})
    try:
        env.rb.tsr_check(var, m)
    except env.rb.Stop as exc:
        assert exc.detail == "['FLAG_RECORD_NOT_THE_PINNED_RECORD']", exc.detail
        raise
    raise AssertionError('no stop')


# ---------------- c2v003: R1 (one terminal prefix, one spec per call) ----------------

@case('R1a_terminal_pair_then_FINISHED_of_another_spec_refused', 'MUST_FAIL', 'ATTEMPT_AFTER_TERMINAL')
def _r1a(env, w):
    """The re-verify probe: a terminal rule-(c) pair, then a FINISHED receipt carrying a different spec_sha256. In
    c2v002 the later spec un-terminated the pair (the pair was judged on every attempt) and the FINISHED re-rolled the
    call. The pair is now judged on its own prefix."""
    expect_refusal(env.rb, lambda: w.p1_with_m001('r1a', [
        ('FAILED_SOLVER', '2026-10-23T10:00:00Z', ev()),
        ('FAILED_SOLVER', '2026-10-24T10:00:00Z', ev(raised=True)),
        ('FINISHED', '2026-10-25T10:00:00Z', {'spec_sha256': '6' * 64})], result='valid'), 'ATTEMPT_AFTER_TERMINAL')


@case('R1b_failure_then_FINISHED_of_another_spec_refused', 'MUST_FAIL', 'RULE_C_SPEC_NOT_IDENTICAL')
def _r1b(env, w):
    """One failure, then a FINISHED attempt of another spec: not a rerun of the identical spec; the call's attempts
    may carry one spec_sha256 only."""
    expect_refusal(env.rb, lambda: w.p1_with_m001('r1b', [
        ('FAILED_SOLVER', '2026-10-23T10:00:00Z', ev()),
        ('FINISHED', '2026-10-24T10:00:00Z', {'spec_sha256': '6' * 64})], result='valid'), 'RULE_C_SPEC_NOT_IDENTICAL')


@case('R1c_failure_then_FINISHED_of_the_identical_spec_is_EVALUATED', 'MUST_PASS')
def _r1c(env, w):
    out = w.p1_with_m001('r1c', [('FAILED_SOLVER', '2026-10-23T10:00:00Z', ev()),
                                 ('FINISHED', '2026-10-24T10:00:00Z', ev(raised=True))], result='valid')
    _pins, plan, _ = w.outputs(out)
    m = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]['members'][1]
    assert m['own_disposition'] == 'EVALUATED' and m['n_attempts'] == 2 and m['rule_c'] is None, m


# ---------------- c2v003: R2 (every receipt bound to its call; launch registry) ----------------

@case('R2a_one_failure_pair_copied_to_a_second_call_refused', 'MUST_FAIL', 'RECEIPT_THETA_NOT_OF_CALL')
def _r2a(env, w):
    """The re-verify probe: M001's terminal failure pair, byte-copied into M002's own run directories, made M002
    EVALUATED_FAILED too in c2v002. The copies carry M001's exact-theta key."""
    d = env.dir('cases', 'r2a')
    b = w.b1
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'],
                [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
                 ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(raised=True))], result='failure')
    att = []
    for i, a in enumerate(c1['attempts']):
        rd = env.dir('cases', 'r2a', 'm002_copy', 'a%d' % i)
        with open(a['receipt']['path'], 'rb') as f:
            att.append({'run_dir': rd, 'receipt': wbytes(os.path.join(rd, 'receipt_copy.json'), f.read())})
    res = wjson(os.path.join(att[-1]['run_dir'], 'result_failure.json'), Base.failure_record())
    c2 = {'alternative': PRIMARY, 'kind': 'MEMBER', 'key': 'M002', 'attempts': att, 'result': res,
          'cut_record': None}
    expect_refusal(env.rb, lambda: w.build_p1('r2a', calls=[w.p1_calls[0], c1, c2]), 'RECEIPT_THETA_NOT_OF_CALL')


@case('R2b_receipt_spec_not_the_calls_registered_spec_refused', 'MUST_FAIL', 'RECEIPT_SPEC_NOT_REGISTERED')
def _r2b(env, w):
    other = spec_of(PRIMARY, tsha(w.b1.thetas['M002']))
    expect_refusal(env.rb, lambda: w.p1_with_m001('r2b', [('FINISHED', '2026-10-23T11:00:00Z',
                                                           {'spec_sha256': other})], result='valid'),
                   'RECEIPT_SPEC_NOT_REGISTERED')


def _twin_on_serial(env, w, tag, same_file, hard_link=False):
    """The identity twin registered at the serial member's theta and spec (A133 re-binding: the spec sha without
    column_workers), its attempt being M000's own receipt (same_file), a hard link to it in its own run dir
    (hard_link; c2v004) or a byte copy of it in its own run dir."""
    m000 = w.p1_calls[0]
    if same_file:
        att = dict(m000['attempts'][0])
    elif hard_link:
        rd = env.dir('cases', tag, 'twin_run')
        att = {'run_dir': rd, 'receipt': hlink(m000['attempts'][0]['receipt'], rd, 'receipt_link.json')}
    else:
        rd = env.dir('cases', tag, 'twin_run')
        with open(m000['attempts'][0]['receipt']['path'], 'rb') as f:
            att = {'run_dir': rd, 'receipt': wbytes(os.path.join(rd, 'receipt_copy.json'), f.read())}
    twin = {'label': 'IDENTITY_TWIN_CW8', 'attempts': [att]}
    others = w.other[:3] + [twin]
    t0 = tsha(w.b1.thetas['M000'])
    reg = w.b1.registry_pin(env.dir('cases', tag), 'PHASE_1', w.p1_calls, others,
                            other_over={'IDENTITY_TWIN_CW8': {'theta_sha256': t0, 'spec_sha256': spec_of(PRIMARY, t0)}})
    return w.build_p1(tag, other_phase_calls=others, launch_registry=reg)


@case('R2c_one_receipt_byte_copy_serving_a_member_and_the_twin_refused', 'MUST_FAIL', 'RECEIPT_REUSED_ACROSS_CALLS')
def _r2c(env, w):
    expect_refusal(env.rb, lambda: _twin_on_serial(env, w, 'r2c', same_file=False), 'RECEIPT_REUSED_ACROSS_CALLS')


@case('R2d_one_receipt_file_serving_a_member_and_the_twin_refused', 'MUST_FAIL', 'RECEIPT_REUSED_ACROSS_CALLS')
def _r2d(env, w):
    expect_refusal(env.rb, lambda: _twin_on_serial(env, w, 'r2d', same_file=True), 'RECEIPT_REUSED_ACROSS_CALLS')


@case('R2e_registry_theta_key_not_the_calls_exact_theta_refused', 'MUST_FAIL', 'LAUNCH_REGISTRY_THETA_MISMATCH')
def _r2e(env, w):
    d = env.dir('cases', 'r2e')
    reg = w.b1.registry_pin(d, 'PHASE_1', w.p1_calls, w.other,
                            call_over={(PRIMARY, 'MEMBER', 'M001'): {'theta_sha256': 'e' * 64}})
    expect_refusal(env.rb, lambda: w.build_p1('r2e', launch_registry=reg), 'LAUNCH_REGISTRY_THETA_MISMATCH')


@case('R2f_call_without_a_registry_entry_refused', 'MUST_FAIL', 'LAUNCH_REGISTRY_ENTRY_MISSING')
def _r2f(env, w):
    d = env.dir('cases', 'r2f')
    reg = w.b1.registry_pin(d, 'PHASE_1', w.p1_calls[:2], w.other)
    expect_refusal(env.rb, lambda: w.build_p1('r2f', launch_registry=reg), 'LAUNCH_REGISTRY_ENTRY_MISSING')


@case('R2g_FINISHED_receipt_without_the_theta_key_refused', 'MUST_FAIL', 'RECEIPT_CALL_BINDING_MISSING')
def _r2g(env, w):
    expect_refusal(env.rb, lambda: w.p1_with_m001('r2g', [('FINISHED', '2026-10-23T11:00:00Z',
                                                           {'theta_sha256': DROP})], result='valid'),
                   'RECEIPT_CALL_BINDING_MISSING')


@case('R2h_registry_entry_without_a_call_record_refused', 'MUST_FAIL', 'LAUNCH_REGISTRY_ENTRY_WITHOUT_CALL')
def _r2h(env, w):
    d = env.dir('cases', 'r2h')
    extra = [{'alternative': None, 'kind': 'OTHER', 'key': 'F9', 'theta_sha256': other_tsha('F9'),
              'spec_sha256': other_spec('F9')}]
    reg = w.b1.registry_pin(d, 'PHASE_1', w.p1_calls, w.other, extra_entries=extra)
    expect_refusal(env.rb, lambda: w.build_p1('r2h', launch_registry=reg), 'LAUNCH_REGISTRY_ENTRY_WITHOUT_CALL')


@case('R2i_one_call_registered_with_two_spec_shas_refused', 'MUST_FAIL', 'LAUNCH_REGISTRY_CONFLICT')
def _r2i(env, w):
    """A MEMBER and a SENSITIVITY entry at one exact theta are one call (A133); two specs for it refuse."""
    d = env.dir('cases', 'r2i')
    t1 = tsha(w.b1.thetas['M001'])
    extra = [{'alternative': PRIMARY, 'kind': 'SENSITIVITY', 'key': 'S_SAME_THETA', 'theta_sha256': t1,
              'spec_sha256': '7' * 64}]
    reg = w.b1.registry_pin(d, 'PHASE_1', w.p1_calls, w.other, extra_entries=extra)
    expect_refusal(env.rb, lambda: w.build_p1('r2i', launch_registry=reg), 'LAUNCH_REGISTRY_CONFLICT')


@case('R2j_registry_and_binding_recorded_in_the_replay_plan', 'MUST_PASS')
def _r2j(env, w):
    d = env.dir('cases', 'r2j')
    reg = w.b1.registry_pin(d, 'PHASE_1', w.p1_calls, w.other)
    out = w.build_p1('r2j', launch_registry=reg)
    _pins, plan, _ = w.outputs(out)
    assert plan['launch_registry'] == reg, plan['launch_registry']
    assert len(env.rb.RECEIPT_KEY_ROLES) == 9 and 'theta_sha256' in env.rb.RECEIPT_KEY_ROLES
    keys = dict(RECEIPT_KEYS)
    del keys['theta_sha256']
    try:
        env.rb._receipt_cfg(keys, CLASSES)
        raise AssertionError('receipt_keys without the theta_sha256 role accepted')
    except env.rb.Refused as exc:
        assert exc.code == 'INPUT_KEY_MISSING', exc.code


# ---------------- c2v003: R3 (the step-7 ledger outside the build directory) ----------------

@case('K10_copied_build_directory_does_not_reset_the_ledger_step7_refused', 'MUST_FAIL', 'STEP7_PLAN_SUPERSEDED')
def _k10(env, w):
    """The re-verify probe: copy the build directory (same BUILD_RECORD sha256) and compare the superseded plan
    again with an agreeing pass. In c2v002 the copy carried no ledger, so the reset succeeded."""
    x = Discrepancy(env, w, 'k10')
    cp = copy_build(env, x.out, 'k10_copy')
    assert pin(os.path.join(cp, 'BUILD_RECORD.json'))['sha256'] == x.br['sha256']
    expect_refusal(env.rb, lambda: env.rb.step7_run(pin(os.path.join(cp, 'BUILD_RECORD.json')),
                                                    pin(os.path.join(cp, 'REPLAY_PLAN.json')), x.p.p1_pin,
                                                    x.pk_agree), 'STEP7_PLAN_SUPERSEDED')


@case('K11_pass_driver_on_a_copied_build_directory_refuses_the_superseded_plan', 'MUST_FAIL', 'PASS_PLAN_SUPERSEDED')
def _k11(env, w):
    x = Discrepancy(env, w, 'k11')
    cp = copy_build(env, x.out, 'k11_copy')
    expect_refusal(env.rb, lambda: drive(env, w.b1, cp, 'PASS_K'), 'PASS_PLAN_SUPERSEDED')


@case('K12_ledger_moved_away_reads_STEP7_LEDGER_MISSING_not_an_empty_ledger', 'MUST_FAIL', 'STEP7_LEDGER_MISSING')
def _k12(env, w):
    x = Discrepancy(env, w, 'k12')
    led = ledger_dir(x.out)
    os.rename(led, led + '_moved_by_test_k12')
    expect_refusal(env.rb, lambda: step7(env, x.out, x.plan_pin, x.p.p1_pin, x.pk_agree), 'STEP7_LEDGER_MISSING')


@case('K13_second_ledger_beside_the_build_record_refused', 'MUST_FAIL', 'STEP7_LEDGER_SECOND_LEDGER')
def _k13(env, w):
    out = w.build_p1('k13')
    d = env.dir('cases', 'k13')
    rec1, _x, _m = drive(env, w.b1, out, 'PASS_ONE')
    reck, _x, _m = drive(env, w.b1, out, 'PASS_K')
    os.mkdir(os.path.join(out, 'STEP7_LEDGER'))
    expect_refusal(env.rb, lambda: step7(env, out, pin(os.path.join(out, 'REPLAY_PLAN.json')),
                                         save(env, d, 'p1.json', rec1), save(env, d, 'pk.json', reck)),
                   'STEP7_LEDGER_SECOND_LEDGER')


@case('K14_full_build_with_a_relative_ledger_root_refused', 'MUST_FAIL', 'STEP7_LEDGER_ROOT_INVALID')
def _k14(env, w):
    expect_refusal(env.rb, lambda: w.build_p1('k14', step7_ledger_root='ledgers_relative'),
                   'STEP7_LEDGER_ROOT_INVALID')


@case('K15_full_build_creates_its_ledger_genesis_outside_the_build_dir', 'MUST_PASS')
def _k15(env, w):
    out = w.build_p1('k15')
    rec = jload(os.path.join(out, 'BUILD_RECORD.json'))
    led = ledger_dir(out)
    assert os.path.dirname(rec['step7_ledger_root']) == env.dir('ledgers') and os.path.isdir(led), led
    assert not os.path.commonpath([os.path.realpath(out), led]) == os.path.realpath(out)
    assert os.listdir(led) == ['LEDGER_GENESIS.json']
    g = jload(os.path.join(led, 'LEDGER_GENESIS.json'))
    assert g['build_record_sha256'] == pin(os.path.join(out, 'BUILD_RECORD.json'))['sha256'], g
    assert g['replay_plan_sha256'] == pin(os.path.join(out, 'REPLAY_PLAN.json'))['sha256'], g
    assert not os.path.lexists(os.path.join(out, 'STEP7_LEDGER'))


@case('K16_genesis_of_another_build_record_breaks_the_ledger', 'MUST_FAIL', 'STEP7_LEDGER_BROKEN')
def _k16(env, w):
    a, b = w.build_p1('k16a'), w.build_p1('k16b')
    la, lb = ledger_dir(a), ledger_dir(b)
    os.rename(la, la + '_moved_by_test_k16')
    os.mkdir(la)
    with open(os.path.join(lb, 'LEDGER_GENESIS.json'), 'rb') as f:
        wbytes(os.path.join(la, 'LEDGER_GENESIS.json'), f.read())
    d = env.dir('cases', 'k16')
    rec1, _x, _m = drive(env, w.b1, a, 'PASS_ONE')
    reck, _x, _m = drive(env, w.b1, a, 'PASS_K')
    expect_refusal(env.rb, lambda: step7(env, a, pin(os.path.join(a, 'REPLAY_PLAN.json')),
                                         save(env, d, 'p1.json', rec1), save(env, d, 'pk.json', reck)),
                   'STEP7_LEDGER_BROKEN')


@case('K17_rebuild_of_the_same_plan_under_the_same_ledger_root_refused', 'MUST_FAIL',
      'STEP7_LEDGER_PLAN_ALREADY_LEDGERED')
def _k17(env, w):
    """A rebuild into a new directory is a new BUILD_RECORD sha256; under the root-fixed ledger root it never gets
    a second, empty ledger for the same replay plan."""
    root = env.dir('cases', 'k17', 'ledger_root')
    a = w.build_p1('k17a', step7_ledger_root=root)
    assert os.path.isdir(ledger_dir(a))
    expect_refusal(env.rb, lambda: w.build_p1('k17b', step7_ledger_root=root), 'STEP7_LEDGER_PLAN_ALREADY_LEDGERED')


# ---------------- c2v003: classifier A's input contracts ----------------

@case('X01_gate_status_list_is_classifier_A_GATE_STATUS_LIST_C4V001_exactly', 'MUST_PASS')
def _x01(env, w):
    out = w.build_p1('x01')
    gl, rep = w.a_list(out), w.outputs(out)[2]
    assert set(gl) == {'schema', 'gates'} and gl['schema'] == 'GATE_STATUS_LIST_C4V001', sorted(gl)   # A173 (a)
    assert all(set(g) == {'gate_sha256', 'status', 'pinned_by_entry'} for g in gl['gates'])
    st = {g['gate_sha256']: g['status'] for g in gl['gates']}
    assert st == {w.g1['sha256']: 'ON-TIME', w.g2['sha256']: 'LATE'}, st
    assert len(st) == len(gl['gates'])
    assert all(isinstance(g['pinned_by_entry'], str) and g['pinned_by_entry'] for g in gl['gates'])
    assert [(g['gate_sha256'], g['status'].replace('-', '_'), g['pinned_by_entry']) for g in gl['gates']] == \
        [(g['gate']['sha256'], g['status'], g['pinned_by_entry']) for g in rep['gates']]
    with open(os.path.join(out, 'GATE_STATUS_LIST.json'), 'rb') as f:
        assert f.read() == env.rb.dump_bytes(gl)


@case('X02_tsr_flag_record_V003_is_classifier_A_TSR_FLAG_RECORD_C4V001_and_projects_V001', 'MUST_PASS')
def _x02(env, w):
    """c2v006: the record is V003 (id was X02_tsr_flag_record_V002_...); its keys include `schema` (A173)."""
    rec, v1 = jload(TSR_RECORD_PATH), jload(TSR_V001_PATH)
    assert set(rec) == {'schema', 'target_free', 'rule', 'failing_ring_ordinal', 'ntest_compare_pin', 'n1_record_pin',
                        'gl_node_record_pin', 'flags'}, sorted(rec)
    assert rec['schema'] == 'TSR_FLAG_RECORD_C4V001'
    assert rec['target_free'] is True and rec['failing_ring_ordinal'] == 15 and rec['rule'] == v1['rule']
    for k, k1, s in (('ntest_compare_pin', 'ntest_compare', '6f095f64'), ('n1_record_pin', 'n1_record', '8867c376'),
                     ('gl_node_record_pin', 'gl_node_record', 'ec1dcca5')):
        assert set(rec[k]) == {'path', 'sha256'} and rec[k] == v1['pins'][k1] and rec[k]['sha256'].startswith(s)
    assert [f['query_id'] for f in rec['flags']] == ['NGC3198-Q%02d' % i for i in range(1, 44)]
    assert all(set(f) == {'query_id', 'TRUNCATION_SHAPE_RESIDUAL'} for f in rec['flags'])
    assert rec['flags'] == [{'query_id': f['query_id'], 'TRUNCATION_SHAPE_RESIDUAL': f['TRUNCATION_SHAPE_RESIDUAL']}
                            for f in v1['flags']]
    with open(TSR_RECORD_PATH, 'rb') as f:
        assert env.rb.tsr_record_v003(pin(TSR_V001_PATH)) == f.read()      # tsr-record reproduces V003 byte for byte
    assert pin(TSR_RECORD_PATH)['sha256'] == env.rb.PRODUCTION_TSR['flag_record_sha256']


@case('X03_check_gate_list_refuses_a_c2v002_form_list', 'MUST_FAIL', 'GATE_STATUS_LIST_DEFECT')
def _x03(env, w):
    out = w.build_p1('x03')
    pins, _plan, _ = w.outputs(out)
    expect_refusal(env.rb, lambda: env.rb.check_gate_list(pins, pin(os.path.join(out, 'GATE_STATUS_REPORT.json')),
                                                          pin(os.path.join(out, 'BUILD_RECORD.json'))),
                   'GATE_STATUS_LIST_DEFECT')


@case('X04_tsr_check_refuses_the_V001_schema_record', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _x04(env, w):
    try:
        env.rb.tsr_check(pin(TSR_V001_PATH))
    except env.rb.Stop as exc:
        assert 'TSR_FLAG_RECORD_C4V001' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('X05_well_formed_list_with_an_edited_status_refused', 'MUST_FAIL', 'GATE_STATUS_LIST_DEFECT')
def _x05(env, w):
    out = w.build_p1('x05')
    pins, _plan, _ = w.outputs(out)
    gl = w.a_list(out)
    for g in gl['gates']:
        g['status'] = 'ON-TIME'                                  # G2 was LATE
    gp = wjson(os.path.join(env.dir('cases', 'x05'), 'list_edited.json'), gl)
    try:
        env.rb.check_gate_list(pins, gp, pin(os.path.join(out, 'BUILD_RECORD.json')))
    except env.rb.Stop as exc:
        assert 'not the FULL build' in exc.detail, exc.detail
        raise
    raise AssertionError('no stop')


@case('X06_gate_list_carrying_the_schema_key_accepted_A173', 'MUST_PASS')
def _x06(env, w):
    """c2v005: MUST_FAIL GATE_STATUS_LIST_DEFECT (id X06_gate_list_carrying_a_key_outside_A_schema_refused): a list
    with `schema: GATE_STATUS_LIST_C4V001` was outside the c2v005 form. c2v006, A173 OI-A1 ruling (a): that list is
    exactly the builder's own GATE_STATUS_LIST.json (same bytes), and check-gate-list passes it. A key outside A's
    schema is Y06."""
    out = w.build_p1('x06')
    pins, _plan, _ = w.outputs(out)
    gl = dict(w.a_list(out), schema='GATE_STATUS_LIST_C4V001')
    gp = wjson(os.path.join(env.dir('cases', 'x06'), 'list_with_schema_key.json'), gl)
    assert gp['sha256'] == pin(os.path.join(out, 'GATE_STATUS_LIST.json'))['sha256']
    r = env.rb.check_gate_list(pins, gp, pin(os.path.join(out, 'BUILD_RECORD.json')))
    assert r['verdict'] == 'PASS' and r['list_schema'] == 'GATE_STATUS_LIST_C4V001', r


@case('X07_builder_outputs_and_the_classifier_A_records_it_does_not_write', 'MUST_PASS')
def _x07(env, w):
    out = w.build_p1('x07')
    names = sorted(os.listdir(out))
    alts = [a['name'] for a in jload(os.path.join(out, 'REPLAY_PLAN.json'))['alternatives']]
    assert names == sorted(['BUILD_RECORD.json', 'GATE_STATUS_LIST.json', 'GATE_STATUS_REPORT.json',
                            'REPLAY_PLAN.json', 'ROSTER_PINS.json'] + ['ROSTER_%s.json' % a for a in alts]), names
    produced = env.rb.A_INPUTS_PRODUCED
    not_produced = env.rb.A_INPUTS_NOT_PRODUCED
    roles = ['phase_inputs', 'freeze_manifest', 'score', 'slots', 'gate_status_list', 'tsr_flag_record',
             'tsr_support_record', 'ntest_compare', 'stage0_status', 'commitment_status', 'agree_record',
             'phase1_classification', 'l1_record', 'c3_record', 'root_disclosures', 'fallback', 'field_map']
    assert sorted(produced) == ['gate_status_list', 'tsr_flag_record'], produced
    assert sorted(set(produced) | set(not_produced)) == sorted(roles) and not set(produced) & set(not_produced)
    assert all(isinstance(v, str) and v for v in not_produced.values())


# ---------------- c2v004: one run file serves one call (file identity; cut-record content) ----------------

def plain_cut(run_dir, name, kpc):
    """A cut record whose bytes name no call (the c2v003 fixture form)."""
    return wjson(os.path.join(run_dir, name), {
        'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001', 'confinement_status': 'CERTIFIED_UNCONFINED',
        'classification_evidence': {'synthetic': True}, 'first_unconfined_R_kpc': kpc})


def expect_borrow(rb, fn, code, how):
    """expect_refusal, and the refusal names how the file was recognised (realpath, file identity or sha256)."""
    try:
        fn()
    except rb.Refused as exc:
        if exc.code == code and how not in exc.detail:
            raise AssertionError('%s refused, but not by %s: %s' % (code, how, exc.detail))
        raise
    raise AssertionError('no refusal; expected ' + code)


def failed_pair(hour):
    """A rule-(c) terminal FAILED pair (solo, rerun at RAM with the wall cap doubled) at the given hour."""
    return [('FAILED_SOLVER', '2026-10-23T%02d:00:00Z' % hour, ev()),
            ('FAILED_SOLVER', '2026-10-24T%02d:00:00Z' % hour, ev(raised=True))]


def _m001_own(env, w, tag, cut_kpc):
    """M001 (PRIMARY, Phase 1) in its own run directory under the case, FINISHED, with its own result (consistent
    with a cut at cut_kpc when one is given) and its own cut record."""
    b = w.b1
    return b.call(env.dir('cases', tag), PRIMARY, 'MEMBER', 'M001', b.thetas['M001'],
                  [('FINISHED', '2026-10-23T11:00:00Z')], cut_kpc=cut_kpc, seed=1.0)


@case('H01_A2e_cut_record_of_M000_hard_linked_into_M001_run_dir_refused', 'MUST_FAIL', 'CUT_RECORD_BORROWED')
def _h01(env, w):
    """The c2v001 attack probe A2e, open through c2v003 (the blocking finding): M000's cut record, hard-linked into
    M001's terminal run directory (same st_dev and st_ino, another realpath), paired with a result consistent with
    that cut. c2v003 built BUILT and pass one read M001 evaluated, forward_valid and member_valid true."""
    m000 = w.p1_calls[0]
    c1 = _m001_own(env, w, 'h01', 38.5)
    c1['cut_record'] = hlink(m000['cut_record'], c1['attempts'][-1]['run_dir'], 'cut_hardlink.json')
    expect_borrow(env.rb, lambda: w.build_p1('h01', calls=[m000, c1, w.p1_calls[2]]), 'CUT_RECORD_BORROWED',
                  'file identity')


@case('H02_byte_copy_of_M000_cut_record_in_M001_run_dir_builds_G29', 'MUST_PASS')
def _h02(env, w):
    """The finding's REUSE1 probe: a byte copy of M000's cut record in M001's own run directory (a new file).
    c2v004: MUST_FAIL CUT_RECORD_BORROWED by sha256. c2v005, root ruling G29: the byte-equality refusal for cut
    records is removed (two honest calls may emit byte-identical cut records); the copy resides in M001's own run
    directory, is a file of no other call and so builds. Its bytes are M000's, and each roster context carries it."""
    m000 = w.p1_calls[0]
    c1 = _m001_own(env, w, 'h02', 38.5)
    c1['cut_record'] = bcopy(m000['cut_record'], c1['attempts'][-1]['run_dir'], 'cut_bytecopy.json')
    out = w.build_p1('h02', calls=[m000, c1, w.p1_calls[2]])
    pins, _plan, _ = w.outputs(out)
    ctx = jload(pins[PRIMARY]['path'])['outer_cut']['contexts']
    assert [c['cut'] for c in ctx[:2]] == [m000['cut_record'], c1['cut_record']], ctx
    assert ctx[0]['cut']['sha256'] == ctx[1]['cut']['sha256'] and ctx[0]['cut']['path'] != ctx[1]['cut']['path']


@case('H03_result_of_M000_hard_linked_as_the_result_of_M001_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _h03(env, w):
    m000 = w.p1_calls[0]
    c1 = _m001_own(env, w, 'h03', None)
    c1['result'] = hlink(m000['result'], c1['attempts'][-1]['run_dir'], 'result_hardlink.json')
    expect_borrow(env.rb, lambda: w.build_p1('h03', calls=[m000, c1, w.p1_calls[2]]), 'FILE_BORROWED',
                  'file identity')


@case('H04_one_receipt_hard_link_serving_a_member_and_the_twin_refused', 'MUST_FAIL', 'RECEIPT_REUSED_ACROSS_CALLS')
def _h04(env, w):
    """R2c with a hard link in place of the byte copy: the receipt check now names the file identity first."""
    expect_borrow(env.rb, lambda: _twin_on_serial(env, w, 'h04', same_file=False, hard_link=True),
                  'RECEIPT_REUSED_ACROSS_CALLS', 'file identity')


@case('H05_phase2_original_k_cut_record_a_hard_link_of_primarys_at_one_theta_refused', 'MUST_FAIL',
      'CUT_RECORD_BORROWED')
def _h05(env, w):
    """Distinct calls at one exact theta (PRIMARY M000 and ORIGINAL_K M000, MEMBERS stage): ORIGINAL_K's cut record
    is a hard link of PRIMARY's, inside ORIGINAL_K's own terminal run directory."""
    p = P2(env, w, w.b1, 'h05')
    calls = copy.deepcopy(p.calls)
    src = [c for c in calls if (c['alternative'], c['key']) == (PRIMARY, 'M000')][0]
    tgt = [c for c in calls if (c['alternative'], c['key']) == (OK_ALT, 'M000')][0]
    tgt['cut_record'] = hlink(src['cut_record'], tgt['attempts'][-1]['run_dir'], 'cut_hardlink.json')
    out = env.fresh('h05_members')
    expect_borrow(env.rb, lambda: w.b1.build(w.b1.input(p.d, 'PHASE_2', 'MEMBERS', dict(p.common, calls=calls)),
                                             out), 'CUT_RECORD_BORROWED', 'file identity')


@case('H06_distinct_calls_with_byte_identical_cut_records_naming_no_call_build_G29', 'MUST_PASS')
def _h06(env, w):
    """Each call has its own cut-record file, but neither names its call and both radii are equal, so the bytes are
    equal (the c2v003 fixture form). c2v004: MUST_FAIL CUT_RECORD_BORROWED by sha256 (fail-closed). c2v005, root
    ruling G29: distinct calls may carry byte-identical cut records, each inside its own run directory; this builds.
    M000 and M002, Phase 1."""
    b = w.b1
    d = env.dir('cases', 'h06')
    c0 = b.call(d, PRIMARY, 'MEMBER', 'M000', b.thetas['M000'], [('FINISHED', '2026-10-23T10:00:00Z')],
                cut_kpc=38.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'}, seed=0.0)
    c2 = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'], [('FINISHED', '2026-10-23T12:00:00Z')],
                cut_kpc=38.5, seed=2.0)
    for c in (c0, c2):
        c['cut_record'] = plain_cut(c['attempts'][-1]['run_dir'], 'cut_plain.json', 38.5)
    assert c0['cut_record']['sha256'] == c2['cut_record']['sha256'] and \
        c0['cut_record']['path'] != c2['cut_record']['path']
    out = w.build_p1('h06', calls=[c0, w.p1_calls[1], c2])
    pins, plan, _ = w.outputs(out)
    ctx = jload(pins[PRIMARY]['path'])['outer_cut']['contexts']
    assert [c['cut'] for c in ctx] == [c0['cut_record'], None, c2['cut_record']], ctx
    pa = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]
    assert [m['own_disposition'] for m in pa['members']] == ['EVALUATED'] * 3


@case('H07_cut_record_of_M000_hard_linked_as_the_result_of_M001_refused', 'MUST_FAIL', 'CUT_RECORD_BORROWED')
def _h07(env, w):
    """Across roles: one call's cut record serving as another call's result (CUT_RECORD_BORROWED when either file
    is a cut record)."""
    m000 = w.p1_calls[0]
    c1 = _m001_own(env, w, 'h07', None)
    c1['result'] = hlink(m000['cut_record'], c1['attempts'][-1]['run_dir'], 'result_is_a_cut_record.json')
    expect_borrow(env.rb, lambda: w.build_p1('h07', calls=[m000, c1, w.p1_calls[2]]), 'CUT_RECORD_BORROWED',
                  'file identity')


@case('H08_own_cut_record_of_equal_radius_naming_its_call_builds_and_passes', 'MUST_PASS')
def _h08(env, w):
    """Control: M001 with its own cut record at M000's radius (38.5 kpc), naming its own call, and its own result.
    Equal radii are not borrowing. (c2v005: docstring only; c2v004 added "the sha256 check reads the record's
    bytes", and c2v005 has no sha256 check for cut records, G29.)"""
    m000 = w.p1_calls[0]
    c1 = _m001_own(env, w, 'h08', 38.5)
    assert jload(c1['cut_record']['path'])['first_unconfined_R_kpc'] == \
        jload(m000['cut_record']['path'])['first_unconfined_R_kpc'] and \
        c1['cut_record']['sha256'] != m000['cut_record']['sha256']
    out = w.build_p1('h08', calls=[m000, c1, w.p1_calls[2]])
    pins, plan, _ = w.outputs(out)
    ctx = jload(pins[PRIMARY]['path'])['outer_cut']['contexts']
    assert [c['cut']['sha256'] for c in ctx] == [m000['cut_record']['sha256'], c1['cut_record']['sha256'],
                                                 w.p1_calls[2]['cut_record']['sha256']], ctx
    _rec, _x, mem = drive(env, w.b1, out, 'PASS_ONE')
    pe = mem['envelopes'][PRIMARY]
    assert pe['status'] == 'COMPLETE' and pe['n_member_valid'] == 3, pe['reasons']


@case('H09_byte_copy_of_M000_result_as_the_result_of_M001_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _h09(env, w):
    """A byte copy of a FINISHED call's result as another call's result (a new file with another call's bytes). In
    c2v003 this built BUILT, and these synthetic fixtures caught it only in the pass (v003g, PASS_ENVELOPES_NOT_OK)."""
    m000 = w.p1_calls[0]
    c1 = _m001_own(env, w, 'h09', None)
    c1['result'] = bcopy(m000['result'], c1['attempts'][-1]['run_dir'], 'result_bytecopy.json')
    expect_borrow(env.rb, lambda: w.build_p1('h09', calls=[m000, c1, w.p1_calls[2]]), 'FILE_BORROWED', 'sha256')


@case('H10_phase2_original_k_result_a_byte_copy_of_primarys_at_one_theta_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _h10(env, w):
    """Distinct calls at one exact theta (PRIMARY and ORIGINAL_K M000, MEMBERS stage): ORIGINAL_K's result is a byte
    copy of PRIMARY's. Under c2v003 this built BUILT and the synthetic pass one read ORIGINAL_K M000 evaluated,
    forward valid and member valid (development probe; v003g does not catch it)."""
    p = P2(env, w, w.b1, 'h10')
    calls = copy.deepcopy(p.calls)
    src = [c for c in calls if (c['alternative'], c['key']) == (PRIMARY, 'M000')][0]
    tgt = [c for c in calls if (c['alternative'], c['key']) == (OK_ALT, 'M000')][0]
    tgt['result'] = bcopy(src['result'], tgt['attempts'][-1]['run_dir'], 'result_bytecopy.json')
    out = env.fresh('h10_members')
    expect_borrow(env.rb, lambda: w.b1.build(w.b1.input(p.d, 'PHASE_2', 'MEMBERS', dict(p.common, calls=calls)),
                                             out), 'FILE_BORROWED', 'sha256')


@case('H11_failed_call_saving_a_byte_copy_of_a_finished_calls_result_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _h11(env, w):
    """M001 terminal by a rule-(c) FAILED pair, its saved result a byte copy of M000's FINISHED result: the content
    rule applies when either call is FINISHED."""
    b = w.b1
    m000 = w.p1_calls[0]
    c1 = b.call(env.dir('cases', 'h11'), PRIMARY, 'MEMBER', 'M001', b.thetas['M001'],
                [('FAILED_SOLVER', '2026-10-23T11:00:00Z', ev()),
                 ('FAILED_SOLVER', '2026-10-24T11:00:00Z', ev(raised=True))], result=None)
    c1['result'] = bcopy(m000['result'], c1['attempts'][-1]['run_dir'], 'result_bytecopy.json')
    expect_borrow(env.rb, lambda: w.build_p1('h11', calls=[m000, c1, w.p1_calls[2]]), 'FILE_BORROWED', 'sha256')


@case('H12_two_failed_calls_with_byte_identical_failure_records_build', 'MUST_PASS')
def _h12(env, w):
    """The scope of the content rule: M001 and M002 each FAILED by a rule-(c) pair, each saving its own failure
    record file with identical bytes (no call-specific field). This builds and both read EVALUATED_FAILED."""
    b = w.b1
    d = env.dir('cases', 'h12')
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], failed_pair(11), result='failure')
    c2 = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'], failed_pair(12), result='failure', cut_kpc=30.5)
    assert c1['result']['sha256'] == c2['result']['sha256'] and c1['result']['path'] != c2['result']['path']
    out = w.build_p1('h12', calls=[w.p1_calls[0], c1, c2])
    _pins, plan, _ = w.outputs(out)
    pa = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]
    assert [m['own_disposition'] for m in pa['members']] == ['EVALUATED', 'EVALUATED_FAILED', 'EVALUATED_FAILED']


@case('H13_failure_record_of_M001_hard_linked_as_M002s_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _h13(env, w):
    """As H12, but M002's saved failure record is a hard link of M001's: equal bytes are allowed between failed
    calls, one file is not. Only the file identity check detects this case."""
    b = w.b1
    d = env.dir('cases', 'h13')
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], failed_pair(11), result='failure')
    c2 = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'], failed_pair(12), result=None, cut_kpc=30.5)
    c2['result'] = hlink(c1['result'], c2['attempts'][-1]['run_dir'], 'result_hardlink.json')
    expect_borrow(env.rb, lambda: w.build_p1('h13', calls=[w.p1_calls[0], c1, c2]), 'FILE_BORROWED',
                  'file identity')


# ---------------- c2v005: every call's run files (OTHER calls included); G29 residence; C38 ----------------

def own_other(run_dir, label, t, extra=None):
    """An OTHER call (other_phase_calls) with one FINISHED attempt whose run directory is run_dir (created here) and
    whose receipt carries the label's binding keys, plus `extra` keys."""
    os.makedirs(run_dir, exist_ok=True)
    doc = {'receipt_status': 'FINISHED', 'receipt_written_utc': t, 'theta_sha256': other_tsha(label),
           'spec_sha256': other_spec(label)}
    doc.update(extra or {})
    return {'label': label, 'attempts': [{'run_dir': os.path.realpath(run_dir),
                                          'receipt': wjson(os.path.join(run_dir, 'receipt.json'), doc)}]}


def named_cut(path, call, kpc):
    """A cut record whose bytes name `call` (the c2v004 fixture form)."""
    return wjson(path, {'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001', 'confinement_status': 'CERTIFIED_UNCONFINED',
                        'classification_evidence': {'synthetic': True, 'synthetic_call': call},
                        'first_unconfined_R_kpc': kpc})


@case('J01_Q4b_result_of_M001_is_an_OTHER_calls_receipt_same_path_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _j01(env, w):
    """The c2v004 re-verify probe Q4b: M001's terminal run directory is F1's run directory and M001's result pin is
    F1's receipt (one file, one realpath). c2v004 kept OTHER calls out of the run-file check and built BUILT (pass one
    then read M001 evaluated)."""
    b = w.b1
    od = env.dir('cases', 'j01', 'run_F1')
    f1 = own_other(od, 'F1', '2026-10-23T13:00:00Z')
    c1 = b.call(env.dir('cases', 'j01'), PRIMARY, 'MEMBER', 'M001', b.thetas['M001'],
                [('FINISHED', '2026-10-23T11:00:00Z')], result=None, shared_run_dir=od)
    c1['result'] = dict(f1['attempts'][0]['receipt'])
    assert c1['attempts'][-1]['run_dir'] == f1['attempts'][0]['run_dir'] and c1['cut_record'] is None
    expect_borrow(env.rb, lambda: w.build_p1('j01', calls=[w.p1_calls[0], c1, w.p1_calls[2]],
                                             other_phase_calls=[f1] + w.other[1:]), 'FILE_BORROWED', 'realpath')


@case('J02_Q4_result_of_M001_a_hard_link_of_an_OTHER_calls_receipt_refused', 'MUST_FAIL', 'FILE_BORROWED')
def _j02(env, w):
    """The c2v004 re-verify probe Q4: M001's result is a hard link, inside M001's own run directory, of F1's receipt
    (an OTHER call). c2v004 built BUILT."""
    c1 = _m001_own(env, w, 'j02', None)
    c1['result'] = hlink(w.other[0]['attempts'][0]['receipt'], c1['attempts'][-1]['run_dir'], 'result_hardlink.json')
    expect_borrow(env.rb, lambda: w.build_p1('j02', calls=[w.p1_calls[0], c1, w.p1_calls[2]]), 'FILE_BORROWED',
                  'file identity')


@case('J03_Q5_cut_record_of_M001_a_hard_link_of_an_OTHER_calls_receipt_refused', 'MUST_FAIL', 'CUT_RECORD_BORROWED')
def _j03(env, w):
    """The c2v004 re-verify probe Q5: an OTHER call F9 whose receipt also parses as a cut record; M001's cut record is
    a hard link of that receipt inside M001's own run directory. c2v004 built BUILT and pass one read M001 evaluated,
    forward_valid and member_valid true."""
    od = env.dir('cases', 'j03', 'run_F9')
    f9 = own_other(od, 'F9', '2026-10-23T16:00:00Z', extra={
        'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001', 'confinement_status': 'CERTIFIED_UNCONFINED',
        'classification_evidence': {'synthetic': True}, 'first_unconfined_R_kpc': 38.5})
    c1 = _m001_own(env, w, 'j03', 38.5)
    c1['cut_record'] = hlink(f9['attempts'][0]['receipt'], c1['attempts'][-1]['run_dir'], 'cut_is_F9_receipt.json')
    expect_borrow(env.rb, lambda: w.build_p1('j03', calls=[w.p1_calls[0], c1, w.p1_calls[2]],
                                             other_phase_calls=w.other + [f9]), 'CUT_RECORD_BORROWED', 'file identity')


@case('J04_phase2_primary_and_original_k_byte_identical_cut_records_at_one_theta_build_and_pass_G29', 'MUST_PASS')
def _j04(env, w):
    """G29 MUST_PASS in the Phase-2 form: PRIMARY and ORIGINAL_K run the same member thetas, and their cut records
    name no call (the c2v003 fixture form), so at M000 and at M002 the two calls' cut records are byte-identical, each
    a file inside its own call's terminal run directory. c2v004 refused this (CUT_RECORD_BORROWED by sha256). c2v005
    builds the MEMBERS stage, and pass one evaluates every member of both alternatives as valid."""
    p = P2(env, w, w.b1, 'j04')
    calls = copy.deepcopy(p.calls)
    kpc = {'M000': 38.5, 'M002': 30.5}
    for c in calls:
        if c['key'] in kpc:
            c['cut_record'] = plain_cut(c['attempts'][-1]['run_dir'], 'cut_plain.json', kpc[c['key']])
    by = {(c['alternative'], c['key']): c for c in calls}
    for k in kpc:
        a, o = by[(PRIMARY, k)]['cut_record'], by[(OK_ALT, k)]['cut_record']
        assert a['sha256'] == o['sha256'] and a['path'] != o['path'], k
    out = env.fresh('j04_members')
    w.b1.build(w.b1.input(p.d, 'PHASE_2', 'MEMBERS', dict(p.common, calls=calls)), out)
    pins, _plan, _ = w.outputs(out)
    for alt in (PRIMARY, OK_ALT):
        ctx = jload(pins[alt]['path'])['outer_cut']['contexts']
        assert [c['cut'] for c in ctx] == [by[(alt, k)]['cut_record'] for k in ('M000', 'M001', 'M002')], ctx
    _rec, _x, mem = drive(env, w.b1, out, 'PASS_ONE')
    for alt in (PRIMARY, OK_ALT):
        e = mem['envelopes'][alt]
        assert e['status'] == 'COMPLETE' and e['n_member_valid'] == 3, (alt, e['reasons'])


@case('J05_cut_record_outside_its_calls_run_dir_refused_G29', 'MUST_FAIL', 'CUT_RECORD_NOT_OF_ITS_CALL')
def _j05(env, w):
    """G29 residence: M001's own cut record (bytes naming M001, a file of no other call) lies outside M001's terminal
    run directory, in a directory that is no call's run directory."""
    c1 = _m001_own(env, w, 'j05', None)
    c1['cut_record'] = named_cut(os.path.join(env.dir('cases', 'j05', 'not_a_run_dir'), 'cut_M001.json'),
                                 '%s:MEMBER:M001' % PRIMARY, 38.5)
    expect_refusal(env.rb, lambda: w.build_p1('j05', calls=[w.p1_calls[0], c1, w.p1_calls[2]]),
                   'CUT_RECORD_NOT_OF_ITS_CALL')


@case('J06_cut_record_inside_another_calls_run_dir_refused_G29', 'MUST_FAIL', 'CUT_RECORD_IN_OTHER_CALL_RUN_DIR')
def _j06(env, w):
    """G29 residence: M001's terminal run directory is nested inside M000's terminal run directory, so M001's own cut
    record (bytes naming M001, a file of M001 only) lies inside M000's run directory as well as its own."""
    b = w.b1
    d = env.dir('cases', 'j06')
    c0 = b.call(d, PRIMARY, 'MEMBER', 'M000', b.thetas['M000'], [('FINISHED', '2026-10-23T10:00:00Z')],
                cut_kpc=38.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'}, seed=0.0)
    nested = os.path.join(c0['attempts'][-1]['run_dir'], 'nested_M001_run')
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], [('FINISHED', '2026-10-23T11:00:00Z', None, nested)],
                cut_kpc=38.5, seed=1.0)
    assert c1['attempts'][-1]['run_dir'] == os.path.realpath(nested)
    expect_refusal(env.rb, lambda: w.build_p1('j06', calls=[c0, c1, w.p1_calls[2]]), 'CUT_RECORD_IN_OTHER_CALL_RUN_DIR')


@case('J07_cut_record_inside_an_OTHER_calls_run_dir_refused_G29', 'MUST_FAIL', 'CUT_RECORD_IN_OTHER_CALL_RUN_DIR')
def _j07(env, w):
    """G29 residence against OTHER calls: F1's run directory is nested inside M001's terminal run directory, and
    M001's cut record (bytes naming M001, a file of M001 only) is written inside F1's run directory, so it lies inside
    M001's own run directory and inside F1's."""
    c1 = _m001_own(env, w, 'j07', None)
    od = os.path.join(c1['attempts'][-1]['run_dir'], 'F1_run')
    f1 = own_other(od, 'F1', '2026-10-23T13:00:00Z')
    c1['cut_record'] = named_cut(os.path.join(od, 'cut_M001.json'), '%s:MEMBER:M001' % PRIMARY, 38.5)
    expect_refusal(env.rb, lambda: w.build_p1('j07', calls=[w.p1_calls[0], c1, w.p1_calls[2]],
                                              other_phase_calls=[f1] + w.other[1:]),
                   'CUT_RECORD_IN_OTHER_CALL_RUN_DIR')


@case('J08_byte_identical_cut_record_pair_as_one_hard_linked_file_refused_G29', 'MUST_FAIL', 'CUT_RECORD_BORROWED')
def _j08(env, w):
    """G29 identity: H06's pair (two calls' cut records naming no call, equal radii), but M002's is a hard link of
    M000's, inside M002's own run directory. Equal bytes in two files build (H06); one file serving two calls is
    refused, and only the file identity sees it here."""
    b = w.b1
    d = env.dir('cases', 'j08')
    c0 = b.call(d, PRIMARY, 'MEMBER', 'M000', b.thetas['M000'], [('FINISHED', '2026-10-23T10:00:00Z')],
                cut_kpc=38.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'}, seed=0.0)
    c2 = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'], [('FINISHED', '2026-10-23T12:00:00Z')],
                cut_kpc=38.5, seed=2.0)
    c0['cut_record'] = plain_cut(c0['attempts'][-1]['run_dir'], 'cut_plain.json', 38.5)
    c2['cut_record'] = hlink(c0['cut_record'], c2['attempts'][-1]['run_dir'], 'cut_plain_hardlink.json')
    expect_borrow(env.rb, lambda: w.build_p1('j08', calls=[c0, w.p1_calls[1], c2]), 'CUT_RECORD_BORROWED',
                  'file identity')


@case('J09_Q6_failure_record_with_another_calls_cut_record_bytes_builds_in_both_call_orders_G29', 'MUST_PASS')
def _j09(env, w):
    """The c2v004 re-verify probe Q6: M001 FAILED, its saved failure record and its cut record having the same bytes
    X (a valid cut document), and M002 FAILED, saving a byte copy of X in its own run directory. c2v004 refused one
    call order (CUT_RECORD_BORROWED by sha256) and built the other. c2v005: no FINISHED result is involved and cut
    records may be byte-identical (G29), so both orders build, with M001 and M002 EVALUATED_FAILED."""
    b = w.b1
    for order in ('A', 'B'):
        d = env.dir('cases', 'j09' + order)
        c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], failed_pair(11), result=None)
        rd1 = c1['attempts'][-1]['run_dir']
        xdoc = {'schema': 'NGC_CANDIDATE_ROSTER_CUT_CX3V001', 'confinement_status': 'CERTIFIED_UNCONFINED',
                'classification_evidence': {'synthetic': True, 'x': 'j09'}, 'first_unconfined_R_kpc': 33.5}
        c1['result'] = wjson(os.path.join(rd1, 'failure_record.json'), xdoc)
        c1['cut_record'] = wjson(os.path.join(rd1, 'cut.json'), xdoc)
        c2 = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'], failed_pair(12), result=None)
        c2['result'] = bcopy(c1['result'], c2['attempts'][-1]['run_dir'], 'failure_record_copy.json')
        assert c1['result']['sha256'] == c1['cut_record']['sha256'] == c2['result']['sha256']
        calls = [w.p1_calls[0], c1, c2] if order == 'A' else [w.p1_calls[0], c2, c1]
        out = w.build_p1('j09' + order, calls=calls)
        _pins, plan, _ = w.outputs(out)
        pa = [a for a in plan['alternatives'] if a['name'] == PRIMARY][0]
        assert [m['own_disposition'] for m in pa['members']] == ['EVALUATED', 'EVALUATED_FAILED',
                                                                  'EVALUATED_FAILED'], order


@case('J10_finished_result_with_another_calls_cut_record_bytes_refused_in_both_call_orders_C38', 'MUST_FAIL',
      'CUT_RECORD_BORROWED')
def _j10(env, w):
    """C38, kept under G29: M001 FINISHED, its saved result (inside its own run directory) a byte copy of M000's cut
    record. Refused by sha256 whichever call comes first in the build input (CUT_RECORD_BORROWED, because one of the
    two files is a cut record, C40)."""
    m000 = w.p1_calls[0]
    for order in ('A', 'B'):
        c1 = _m001_own(env, w, 'j10' + order, None)
        c1['result'] = bcopy(m000['cut_record'], c1['attempts'][-1]['run_dir'], 'result_bytecopy_of_a_cut.json')
        calls = [m000, c1, w.p1_calls[2]] if order == 'A' else [w.p1_calls[2], c1, m000]
        if order == 'A':
            try:
                w.build_p1('j10A', calls=calls)
            except env.rb.Refused as exc:
                assert exc.code == 'CUT_RECORD_BORROWED' and 'sha256' in exc.detail, (exc.code, exc.detail)
            else:
                raise AssertionError('order A: no refusal')
        else:
            expect_borrow(env.rb, lambda: w.build_p1('j10B', calls=calls), 'CUT_RECORD_BORROWED', 'sha256')


@case('J11_failed_calls_failure_record_outside_its_own_run_dir_refused_G29', 'MUST_FAIL', 'RESULT_NOT_OF_ITS_CALL')
def _j11(env, w):
    """G29: failure records of FAILED calls may be byte-identical (H12) but must lie in their own call's terminal
    run directory. M002's failure record, byte-identical to M001's, is written in M001's run directory."""
    b = w.b1
    d = env.dir('cases', 'j11')
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], failed_pair(11), result='failure')
    c2 = b.call(d, PRIMARY, 'MEMBER', 'M002', b.thetas['M002'], failed_pair(12), result=None, cut_kpc=30.5)
    c2['result'] = bcopy(c1['result'], c1['attempts'][-1]['run_dir'], 'failure_record_of_M002.json')
    expect_refusal(env.rb, lambda: w.build_p1('j11', calls=[w.p1_calls[0], c1, c2]), 'RESULT_NOT_OF_ITS_CALL')


@case('J12_cut_record_inside_a_non_terminal_attempt_run_dir_of_another_call_refused_G29', 'MUST_FAIL',
      'CUT_RECORD_IN_OTHER_CALL_RUN_DIR')
def _j12(env, w):
    """G29 residence covers every attempt's run directory of every other call: M000 failed once and finished on the
    rerun of the identical spec (two run directories), and M001's terminal run directory is nested inside M000's
    first, non-terminal, run directory, so M001's own cut record lies inside a run directory of M000."""
    b = w.b1
    d = env.dir('cases', 'j12')
    c0 = b.call(d, PRIMARY, 'MEMBER', 'M000', b.thetas['M000'],
                [('FAILED_SOLVER', '2026-10-23T09:00:00Z', ev()), ('FINISHED', '2026-10-23T10:00:00Z', ev(raised=True))],
                cut_kpc=38.5, gate_rows={'SYN-Q20': 'SYN_GATE_REASON'}, seed=0.0)
    first = c0['attempts'][0]['run_dir']
    assert first != c0['attempts'][-1]['run_dir']
    nested = os.path.join(first, 'nested_M001_run')
    c1 = b.call(d, PRIMARY, 'MEMBER', 'M001', b.thetas['M001'], [('FINISHED', '2026-10-23T11:00:00Z', None, nested)],
                cut_kpc=38.5, seed=1.0)
    expect_refusal(env.rb, lambda: w.build_p1('j12', calls=[c0, c1, w.p1_calls[2]]), 'CUT_RECORD_IN_OTHER_CALL_RUN_DIR')


# ---------------- c2v006: A173 OI-A1 ruling (a): every root-written record carries `schema` ----------------

# classifier A's contracts as its bytes state them (classifier_a_c4v004.py e92aa30e: check_gate_list L734, L739;
# check_tsr L679-681, L699), typed here independently of the builder's constants
A_GATE_LIST_CONTRACT = ('GATE_STATUS_LIST_C4V001', {'schema', 'gates'})
A_TSR_CONTRACT = ('TSR_FLAG_RECORD_C4V001', {'schema', 'target_free', 'rule', 'failing_ring_ordinal',
                                             'ntest_compare_pin', 'n1_record_pin', 'gl_node_record_pin', 'flags'})


def gate_list_variant(env, w, tag, mutate):
    """A FULL build's GATE_STATUS_LIST.json, mutated and written as a new file: (roster pins, list pin, build record
    pin)."""
    out = w.build_p1(tag)
    pins, _plan, _ = w.outputs(out)
    gl = w.a_list(out)
    mutate(gl)
    gp = wjson(os.path.join(env.dir('cases', tag), 'gate_list_variant.json'), gl)
    return pins, gp, pin(os.path.join(out, 'BUILD_RECORD.json'))


def expect_schema_stop(rb, fn, code, contract_name):
    """fn must stop with code at the record-schema check (its detail names the contract), not at a later check."""
    try:
        fn()
    except rb.Stop as exc:
        assert exc.code == code and contract_name + ' schema' in exc.detail, (exc.code, exc.detail)
        raise
    raise AssertionError('no stop')


@case('Y01_builder_constants_are_classifier_A_contracts_with_schema', 'MUST_PASS')
def _y01(env, w):
    rb = env.rb
    assert (rb.A_GATE_LIST_NAME, set(rb.A_GATE_LIST_KEYS)) == A_GATE_LIST_CONTRACT
    assert (rb.A_TSR_NAME, set(rb.A_TSR_KEYS)) == A_TSR_CONTRACT
    assert set(rb.A_GATE_ENTRY_KEYS) == {'gate_sha256', 'status', 'pinned_by_entry'}
    assert set(rb.A_TSR_FLAG_KEYS) == {'query_id', 'TRUNCATION_SHAPE_RESIDUAL'}
    assert rb.PRODUCTION_TSR['flag_record_sha256'] == TSR_RECORD_SHA != TSR_V002_SHA


@case('Y02_gate_list_with_schema_accepted_by_the_check_gate_list_command', 'MUST_PASS')
def _y02(env, w):
    """The FULL build writes {schema: GATE_STATUS_LIST_C4V001, gates}; check-gate-list (a subprocess) passes it."""
    out = w.build_p1('y02')
    pins, _plan, _ = w.outputs(out)
    gl = w.a_list(out)
    assert gl['schema'] == A_GATE_LIST_CONTRACT[0] and set(gl) == A_GATE_LIST_CONTRACT[1], sorted(gl)
    d = env.dir('cases', 'y02')
    cin = wjson(os.path.join(d, 'check_in.json'), {'schema': 'CHECK_GATE_LIST_INPUT_C2V003', 'roster_pins': pins,
                                                   'gate_status_list': pin(os.path.join(out, 'GATE_STATUS_LIST.json')),
                                                   'build_record': pin(os.path.join(out, 'BUILD_RECORD.json'))})
    outp = os.path.join(d, 'check_out.json')
    r = run_cli(['check-gate-list', '--input', cin['path'], '--input-sha256', cin['sha256'], '--out', outp])
    assert r.returncode == 0, (r.returncode, r.stderr)
    res = jload(outp)
    assert res['verdict'] == 'PASS' and res['list_schema'] == 'GATE_STATUS_LIST_C4V001' and res['n_listed'] == 2, res


@case('Y03_tsr_record_V003_is_V002_plus_schema_passes_tsr_check_and_is_rederived_by_tsr_record', 'MUST_PASS')
def _y03(env, w):
    """V003 is V002's exact content plus "schema": "TSR_FLAG_RECORD_C4V001"; its keys are A's; tsr-check passes it
    from bytes; the tsr-record command (in process) writes V003's bytes from V001."""
    v3, v2 = jload(TSR_RECORD_PATH), jload(TSR_V002_PATH)
    assert pin(TSR_V002_PATH)['sha256'] == TSR_V002_SHA and pin(TSR_RECORD_PATH)['sha256'] == TSR_RECORD_SHA
    assert v3 == dict(v2, schema=A_TSR_CONTRACT[0]) and set(v3) == A_TSR_CONTRACT[1], sorted(v3)
    assert env.rb.tsr_check(pin(TSR_RECORD_PATH))['verdict'] == 'PASS'
    d = env.dir('cases', 'y03')
    cin = wjson(os.path.join(d, 'tsr_record_in.json'), {'schema': 'TSR_RECORD_INPUT_C2V003',
                                                        'flag_record_v001': pin(TSR_V001_PATH)})
    outp = os.path.join(d, 'ROOT_TSR_FLAG_RECORD_V003_rederived.json')
    rc, so, se = main_in_process(env, ['tsr-record', '--input', cin['path'], '--input-sha256', cin['sha256'],
                                       '--out', outp])
    assert rc == 0 and json.loads(so) == {'status': 'WRITTEN', 'sha256': TSR_RECORD_SHA,
                                          'schema': 'TSR_FLAG_RECORD_C4V001'}, (rc, so, se)
    with open(outp, 'rb') as f1, open(TSR_RECORD_PATH, 'rb') as f2:
        assert f1.read() == f2.read()


@case('Y04_gate_list_without_schema_the_c2v005_form_refused', 'MUST_FAIL', 'GATE_STATUS_LIST_DEFECT')
def _y04(env, w):
    """The c2v005 form {gates}: classifier A reads it GATE_STATUS_LIST_DEFECT (L734), and so does check-gate-list,
    at the schema check (before the binding to the build)."""
    pins, gp, br = gate_list_variant(env, w, 'y04', lambda gl: gl.pop('schema'))
    assert set(jload(gp['path'])) == {'gates'}
    expect_schema_stop(env.rb, lambda: env.rb.check_gate_list(pins, gp, br), 'GATE_STATUS_LIST_DEFECT',
                       'GATE_STATUS_LIST_C4V001')


@case('Y05_gate_list_with_a_wrong_schema_string_refused', 'MUST_FAIL', 'GATE_STATUS_LIST_DEFECT')
def _y05(env, w):
    """Any schema value other than the exact string GATE_STATUS_LIST_C4V001 refuses (the list check on six values,
    then check-gate-list on a file)."""
    out = w.build_p1('y05_base')
    good = w.a_list(out)
    assert env.rb._a_gate_list_problem(good) is None
    for bad in ('GATE_STATUS_LIST_C4V002', 'gate_status_list_c4v001', 'GATE_STATUS_REPORT_C2V003',
                'TSR_FLAG_RECORD_C4V001', '', None):
        why = env.rb._a_gate_list_problem(dict(good, schema=bad))
        assert why is not None and 'GATE_STATUS_LIST_C4V001 schema' in why, (bad, why)
    pins, gp, br = gate_list_variant(env, w, 'y05', lambda gl: gl.update(schema='GATE_STATUS_LIST_C4V002'))
    expect_schema_stop(env.rb, lambda: env.rb.check_gate_list(pins, gp, br), 'GATE_STATUS_LIST_DEFECT',
                       'GATE_STATUS_LIST_C4V001')


@case('Y06_gate_list_with_schema_and_an_extra_key_refused', 'MUST_FAIL', 'GATE_STATUS_LIST_DEFECT')
def _y06(env, w):
    """The key set is exact: {schema, gates} plus any other key refuses."""
    pins, gp, br = gate_list_variant(env, w, 'y06', lambda gl: gl.update(builder='roster_builder_c2v006'))
    assert set(jload(gp['path'])) == {'schema', 'gates', 'builder'}
    expect_schema_stop(env.rb, lambda: env.rb.check_gate_list(pins, gp, br), 'GATE_STATUS_LIST_DEFECT',
                       'GATE_STATUS_LIST_C4V001')


@case('Y07_tsr_record_without_schema_refused', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _y07(env, w):
    """A synthetic record in the c2v005 form (no `schema`), bound by its own sha256, so only the schema check can
    stop it."""
    t = SynTsr(env, 'y07')
    fr = t.record('flag_without_schema.json', lambda rec: rec.pop('schema'))
    expect_schema_stop(env.rb, lambda: env.rb.tsr_check(fr, None, dict(t.expected, flag_record_sha256=fr['sha256'])),
                       'TSR_FLAG_TABLE_MISMATCH', 'TSR_FLAG_RECORD_C4V001')


@case('Y08_production_V002_without_schema_refused_by_the_tsr_check_command_exit_3', 'MUST_FAIL',
      'TSR_FLAG_TABLE_MISMATCH')
def _y08(env, w):
    """The c2v005 production record V002 (c9d8ab45) through the tsr-check command (a subprocess): it stops at the
    schema check."""
    d = env.dir('cases', 'y08')
    cin = wjson(os.path.join(d, 'tsr_in.json'), {'schema': 'TSR_CHECK_INPUT_C2V003', 'flag_record': pin(TSR_V002_PATH),
                                                 'freeze_manifest': None})
    outp = os.path.join(d, 'tsr_out.json')
    r = run_cli(['tsr-check', '--input', cin['path'], '--input-sha256', cin['sha256'], '--out', outp])
    assert r.returncode == 3, (r.returncode, r.stderr)
    err = json.loads(r.stderr)
    assert 'TSR_FLAG_RECORD_C4V001 schema' in err['detail'] and jload(outp)['verdict'] == 'STOP', err
    raise env.rb.Stop(err['stop'], err['detail'])


@case('Y09_tsr_record_with_a_wrong_schema_string_refused', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _y09(env, w):
    """Synthetic records bound by their own sha256, each with exactly A's keys and a schema value other than the
    exact string TSR_FLAG_RECORD_C4V001: each stops at the schema check."""
    t = SynTsr(env, 'y09')
    last = None
    for i, bad in enumerate(('UNT_ROOT_TSR_FLAG_RECORD_C2V001', 'GATE_STATUS_LIST_C4V001', 'tsr_flag_record_c4v001',
                             None)):
        fr = t.record('flag_bad_schema_%d.json' % i, lambda rec, b=bad: rec.update(schema=b))
        try:
            env.rb.tsr_check(fr, None, dict(t.expected, flag_record_sha256=fr['sha256']))
        except env.rb.Stop as exc:
            assert exc.code == 'TSR_FLAG_TABLE_MISMATCH' and 'TSR_FLAG_RECORD_C4V001 schema' in exc.detail, \
                (bad, exc.detail)
            last = exc
        else:
            raise AssertionError('no stop for schema %r' % bad)
    raise last


@case('Y10_tsr_record_with_schema_and_an_extra_key_refused', 'MUST_FAIL', 'TSR_FLAG_TABLE_MISMATCH')
def _y10(env, w):
    t = SynTsr(env, 'y10')
    fr = t.record('flag_extra_key.json', lambda rec: rec.update(rule_id='M7_I_DEPENDENCE_OPEN_INTERVAL_C2V001'))
    expect_schema_stop(env.rb, lambda: env.rb.tsr_check(fr, None, dict(t.expected, flag_record_sha256=fr['sha256'])),
                       'TSR_FLAG_TABLE_MISMATCH', 'TSR_FLAG_RECORD_C4V001')


@case('Y11_seal_check_refuses_V002_as_the_sealed_flag_record', 'MUST_FAIL', 'SEAL_SHA_MISMATCH')
def _y11(env, w):
    """V003 supersedes V002 for the seal (A173): a seal entry and manifest naming V002 stop."""
    v2 = pin(TSR_V002_PATH)
    s = Seal(env, 'y11', tsr=v2, manifest_files=[v2])
    try:
        s.check(env)
    except env.rb.Stop as exc:
        assert exc.detail == "roles []; ['SEALED_TSR_FLAG_RECORD_NOT_THE_PINNED_RECORD']", exc.detail
        raise
    raise AssertionError('no stop')


# --------------------------------------------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------------------------------------------

def main(argv):
    if len(argv) != 2 or argv[0] != '--record-dir':
        print(__doc__)
        return 2
    rec_dir = os.path.abspath(argv[1])
    os.mkdir(rec_dir)
    work = os.path.join(rec_dir, 'work')
    os.mkdir(work)
    env = Env(work)
    world = World(env)
    results = []
    for cid, expect, code, fn in CASES:
        verdict, observed, detail = 'FAIL', None, ''
        try:
            fn(env, world)
            observed = 'NO_REFUSAL'
            verdict = 'PASS' if expect == 'MUST_PASS' else 'FAIL'
        except (env.rb.Refused, env.rb.Stop) as exc:
            observed = exc.code
            verdict = 'PASS' if expect == 'MUST_FAIL' and exc.code == code else 'FAIL'
            detail = '' if verdict == 'PASS' else str(exc)[:400]
        except AssertionError as exc:
            observed = 'ASSERTION'
            detail = str(exc)[:600]
        except Exception as exc:  # noqa: BLE001
            observed = 'ERROR'
            detail = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))[-1200:]
        results.append({'id': cid, 'expect': expect, 'expected_code': code, 'observed': observed,
                        'verdict': verdict, 'detail': detail})
        print('%-4s %-9s %s %s' % (verdict, expect, cid, detail))
    norm = [[r['id'], r['expect'], r['expected_code'], r['observed'], r['verdict']] for r in results]

    def pinf(p):
        with open(p, 'rb') as f:
            return {'path': os.path.realpath(p), 'sha256': sha(f.read())}
    record = {'schema': 'TEST_RECORD_RUNBOOK_V002_C2V006', 'builder': pinf(BUILDER_PATH),
              'test_file': pinf(os.path.realpath(__file__)), 'freeze_module': pinf(V003G_PATH),
              'tsr_flag_record': pinf(TSR_RECORD_PATH), 'tsr_flag_record_v001': pinf(TSR_V001_PATH),
              'tsr_flag_record_v002': pinf(TSR_V002_PATH),
              'python': sys.version.split()[0],
              'n_cases': len(results), 'n_pass': sum(r['verdict'] == 'PASS' for r in results),
              'n_must_pass': sum(r['expect'] == 'MUST_PASS' for r in results),
              'n_must_fail': sum(r['expect'] == 'MUST_FAIL' for r in results),
              'results_sha256': sha(json.dumps(norm, separators=(',', ':')).encode()), 'cases': results}
    with open(os.path.join(rec_dir, 'TEST_RECORD.json'), 'x') as f:
        f.write(json.dumps(record, indent=1, sort_keys=True) + '\n')
    print('%d/%d PASS; results_sha256 %s' % (record['n_pass'], record['n_cases'], record['results_sha256']))
    return 0 if record['n_pass'] == record['n_cases'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
