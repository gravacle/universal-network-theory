"""PORT (ks_k3_chain_c2 G-wave c2v001): the proof-side c3v003 suite against G1 (slot proof), G2 (SRB-ROT) and KS6'.

S4-R-C1 proof side c3v003: synthetic MUST_PASS / MUST_FAIL suite (Claude3 builder; A134, FROM_CODEX/0688, 0696; A138 0703;
Codex1 reviews).

c3v003 = every c3v002 case (unchanged in intent; the inventory fixtures now carry the b1 enumerator pin 4ca7f364, V02),
plus the A138 erratum cases: V02 (a v010 inventory is refused and a b1 inventory accepted, by both adapters; the b1
enumerator bytes differ from v010 only in PINS), V03 (wrapper v002's 10-key canonical rho comparison, AST-extracted from
the 7a6af535 bytes, decides the slot proof's (a)4 pair and the per-state adapter; a 1-ulp change in a diagnostic field
refuses, as the wrapper does) and B3 (the call reading equals 0690 OPEN-6 and root's acceptance_handoff_c2v002 L373-391,
AST-extracted and executed, on every verdict combination). Outputs go under <suite dir>/synthetic/ (F11).
The c3v002 description follows.

c3v002 = every c3v001 case (unchanged in intent; fixtures now carry the row-reference state_files that F6 requires),
plus one or more cases per erratum fix (F3, F4, F5, F6, F8, F9, F11), plus the wrapper v002 (7a6af535) cases: the
real L145-191 bytes, AST-extracted from that file, accept the c3v002 slot proof (prelaunch) and the per-state LO
proofs through their core_record pin (acceptance, L185). F11: every output of this suite goes under
<suite dir>/synthetic/, and a SYNTHETIC_OUTPUTS_MANIFEST lists every file written there.

SYNTHETIC inputs only. No producer runs on a real state, a real call output, a real rho record or a real EPS record.
No run tree is read or listed, and nothing is launched.

Real files that ARE read, and how they are used:
- Pinned source modules, imported only. Their top level reads only source bytes:
  - common fa48b1a1, custody 6810b7c3, guard v003 5f1e49e6;
  - lo_config 6654d93c, which loads lo_core 12d36305, response a1dcdea8 and certs commons;
  - library v002 2026f2b6.
- Real functions run on synthetic inputs:
  - guard verify_bundle;
  - lo_core aggregate_shares (L142-175, the registered threshold arithmetic);
  - library TailState, field_bound and srb_rot;
  - r14 apply_flag, AST-extracted;
  - wrapper r10_c4 L145-161 bytes, executed unchanged and with the A134 Q5 patch.
- Wrapper primitives are AST-extracted from their real files: core dc895f8a canonical/digest/pin_doc and parent v005
  c75a889f sha256_bytes/read_pinned.
- Two dry-plan specs are read: TAIL_REANCHOR and HEADLINE_CORNER_000, for the real point identities only.
- The ruling files are read: A134 56774ba7, FROM_CODEX/0688 bcb6df8e and 0528 d11654e5.

The suite never calls lo_core produce_current_lo, point_context, produce_rho, or custody derive_details on a real
spec. Those are replaced by synthetic test doubles. The core double mirrors lo_core L190-267 with its I/O replaced
and runs the REAL aggregate_shares.

Every fixture is created by exclusive create under a NEW fixture root and carries 'synthetic_fixture'.

Usage:
  taskpolicy -b PY -I -B test_proof_side_c3v003.py --build-dir DIR --fixture-root NEW_DIR --results-dir DIR [--reader custody|local]
  (F11: --fixture-root and --results-dir must be under <suite dir>/synthetic/)
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
           'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import sys


def _refuse_env():
    try:
        bg = os.getpriority(4, 0) == 1
    except Exception:
        bg = False
    if not bg:
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        sys.exit(2)
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B)', flush=True)
        sys.exit(2)


if __name__ == '__main__':
    _refuse_env()

import argparse
import ast
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import io
import json
import math
import struct
import subprocess
import textwrap
import traceback
import types

import numpy as np

SYN = 'S4RC1 proof side c3v003 synthetic test fixture; not a measurement, not a review, not a ruling'
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CERT = ART + '/calib_tail_readiness_cx2/certificates_per_point'
TASKPOLICY = '/usr/sbin/taskpolicy'
REAL = {
    'common': (ART + '/s4rc1_c3/build_c3v002/s4rc1_common_c3v002.py', 'fa48b1a16d26ff14445f6823bd7c15554e50bd0f75b882e0564c4e40980055ce'),
    'custody': (CERT + '/custody_cx2v002.py', '6810b7c3614e219f6e059208fbe59e905d01aa3a115e3c723079b579a027a377'),
    'guard': (CERT + '/certificate_guard_cx2v003.py', '5f1e49e689a859c003b137c45c07f887423443ef2c726182616b41bf290c9c2f'),
    'lo_config': (CERT + '/lo_config_r5_cx2v001.py', '6654d93c0241afd230d90bfcf327f16c22dd24c4da1d3eea72602212c2b6ae5a'),
    'lo_core': (CERT + '/lo_core_r5_cx2v001.py', '12d36305e09651fcb0dca0b76f85c755ff063c9d9e3ce0dd1e1baacf7b3d430e'),
    'response': (CERT + '/point_response_producer_cx2v002.py', 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'),
    'enumerator': (ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py', '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'),   # c3v003 V02
    'enumerator_v010': (CERT + '/consumed_states_cx2v010.py', 'e48cca3c35a3d6d3724f74b9407b91f006bd31f2f30f416f9c328ba9e4144ca2'),          # c3v003 V02: refused
    'eps_adapter': (CERT + '/point_response_admission_adapter_cx2v003.py', '4de70486120de215838f5ca2b0c9464d52a0edc3d5280dd042d5521d60f1c372'),
    'gq_producer': (CERT + '/gq_producer_cx2v005.py', '2832ceb95e1f4c4065963a50475b42cdb176744b824ae6a06f15c30db76441bd'),
    'library': (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py', '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
    'r14': (ART + '/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
    'wrapper': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4.py', 'ef3d3d69e01999dcfa255a75c98bcdee31a9512f0e284053139ea190ef9445c3'),
    'wrapper_core': (ART + '/calib_tail_readiness_cx2/v006r10_c4/calibration_core_cx2v006r10_c4.py', 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'),
    'parent_v005': (ART + '/calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py', 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'),
    'eps_cert_v006': (ART + '/tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json', '598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192'),
    'spec_anchor': (ART + '/step4_launch_readiness_c4/dryplans/specs_v001/specs/TAIL_REANCHOR.json', '5fc6f0bdcbe5c58c371f77e886facfc6610ae10c5018a544aa0b67c6facd58e3'),
    'spec_corner000': (ART + '/step4_launch_readiness_c4/dryplans/specs_v001/specs/HEADLINE_CORNER_000.json', 'f3c72d953ad21659cb2d4382a9d19994770fd720f183e34dabdcc3bc0dbc0dd4'),
    'ruling_a134': ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md', '56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82'),
    'ruling_0688': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0688_2026-10-19_A134_S4RC1_LO_route_ruled_owners.md', 'bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d'),
    'ruling_0528': ('/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0528_2026-10-18_codex2_rulings_P0_normalization_and_certificate_admission.md', 'd11654e5a2ab24944a861372769e75e0a2bbac035feecdf4a54286e3841aae83'),
    # c3v002 additions (read as source bytes only)
    'wrapper_v002': (ART + '/s4_acceptance_c2/wrapper_q5/build_v002/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py', '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'),
    'guard_b1': (ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'),
    'lo_producer_v004': (CERT + '/lo_producer_cx2v004.py', '5db60d0f6db6d481e2f748b19bef08ce425f19a0e463d58727c184d633e03d51'),
    'route_a_controller': (ART + '/tail_scheme_impl_c2/route_a/route_a_uv_tail_controller_c2v001.py', '51d32e7b2b8c83c7544c24d64ea3161007fbec35769a64a869972efac055cb68'),
    'row_producer_q2_v002': (ART + '/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v002.py', 'e9190f5e3e852eb540a3300ed98c79bc0a4d55d0525eca41095f3881d2e121b6'),
    'handoff_q2_v002': (ART + '/s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v002.py', 'ccdbec2b831a1ee5b7feadc68156f7329b9490ee21dc0820589b6760757e5c08'),
    # c3v003 (read only): the c3v002 state adapter, whose call reading the B3 table compares
    'state_c3v002': (ART + '/s4rc1_c3/proof_side_c3v002/lo_state_proof_adapter_c3v002.py', '8cae0b1a9a05e655bc00a4f476b0d448510daf7f566d355e96fe7d6ca9484598'),
}
WRAPPER_V002_BLOCK_LINES = (145, 191)     # the L145-191 slot block of wrapper v002 (ef3d3d69 L145-161 successor)
SUITE_DIR = os.path.dirname(os.path.realpath(__file__))
SYNTHETIC_DIR = SUITE_DIR + '/synthetic'
ANCHOR_KEY = '8ad6ca4e867854dad71f56a97fda66f7d7b295473092a0bec84a4aca968635f8'
CORNER000_KEY = '64dc775b80425f8a890e4b23aa985922b19bfe9512456ebf51b0207b4e2eba80'
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
WRAPPER_BLOCK_SHA = 'd626db7a1f002102c85b87b001c512301fb4e6f6cec0e671981b112c6194504b'   # r10_c4 L145-161 bytes
OLD_L148 = "            for slot,gate_name in (('eps_certificate','EPS'),('lo_certificate','LO_ENVELOPE')):"
NEW_L148 = "            for slot,gate_name in (('eps_certificate','EPS'),('lo_certificate','LO_RHO_SLOT')):"
OLD_L160 = ("                if gate_name=='LO_ENVELOPE' and proof.get('covers_all_consumed_states') is not True:\n"
            "                    raise Error('a reviewed prelaunch LO envelope is required; no anchor substitution')")
NEW_L160 = ("                if gate_name=='LO_RHO_SLOT':\n"
            "                    if 'covers_all_consumed_states' in proof or 'cover_all_consumed_states' in proof:\n"
            "                        raise Error('LO slot proof must not carry covers_all_consumed_states (A134 Q5)')\n"
            "                    rho=M.pin_doc(slots[slot],'lo slot rho record')\n"
            "                    if rho.get('schema')!='UNT_POINT_RHO_NUMERICAL_CX2V001' or rho.get('gate')!='RHO_G' or rho.get('point_sha256')!=M.digest(ident) or rho.get('custody')!=custody:\n"
            "                        raise Error(\"lo slot is not this point's rho record\")")
KPC = 3.085677581491367e19
RESULTS = []


# ------------------------------------------------------------------------------------------------ harness
def record(cid, kind, req, passed, expected, observed):
    RESULTS.append({'id': cid, 'kind': kind, 'requirement': req, 'passed': bool(passed),
                    'expected': expected, 'observed': str(observed)[:900]})


def run_case(cid, kind, req, fn, check, expected):
    """fn() -> value; check(value) -> bool. Exceptions count as failure of the case unless check accepts them."""
    try:
        v = fn()
    except Exception as exc:
        v = {'__exception__': type(exc).__name__ + ': ' + str(exc), 'trace': traceback.format_exc()[-600:]}
    try:
        ok = bool(check(v))
    except Exception as exc:
        ok = False
        v = {'__check_exception__': type(exc).__name__ + ': ' + str(exc), 'value': str(v)[:400]}
    record(cid, kind, req, ok, expected, json.dumps(v, default=str)[:900] if not isinstance(v, str) else v)
    return v


def MP(cid, req, fn, check, expected='ok'):
    return run_case(cid, 'MUST_PASS', req, fn, check, expected)


def MF(cid, req, fn, check, expected):
    return run_case(cid, 'MUST_FAIL', req, fn, check, expected)


def raises(fn, code):
    """For MUST_FAIL: returns the exception text if fn raises one containing code, else a failure marker."""
    try:
        v = fn()
    except Exception as exc:
        t = type(exc).__name__ + ': ' + str(exc)
        return {'raised': t, 'match': code in t}
    return {'raised': None, 'match': False, 'value': str(v)[:300]}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, 'rb') as f:
        return sha_bytes(f.read())


def load_exact(path, sha, name):
    if os.path.realpath(path) != path:
        raise ValueError('noncanonical ' + path)
    with open(path, 'rb') as f:
        raw = f.read()
    if sha is not None and sha_bytes(raw) != sha:
        raise ValueError('pin mismatch ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def load_via(path, name):
    """Load a module whose __file__ is exactly `path` (used for the R4 non-canonical alias case)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with open(path, 'rb') as f:
        exec(compile(f.read(), path, 'exec'), mod.__dict__)
    return mod


def extract_functions(path, sha, names, ns):
    with open(path, 'rb') as f:
        raw = f.read()
    if sha_bytes(raw) != sha:
        raise ValueError('pin mismatch ' + path)
    tree = ast.parse(raw.decode('utf-8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if sorted(n.name for n in nodes) != sorted(names):
        raise ValueError('functions not found ' + repr(names))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), path, 'exec'), ns)
    return ns


def nextup(x):
    return float(np.nextafter(x, np.inf))


def nextdown(x):
    return float(np.nextafter(x, -np.inf))


class FX:
    """Synthetic fixture writer: exclusive create only, under one NEW fixture root."""

    def __init__(self, root, C):
        if os.path.exists(root):
            raise SystemExit('fixture root must be NEW: ' + root)
        os.makedirs(root)
        self.root = os.path.realpath(root)
        self.C = C

    def path(self, rel):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        return p

    def dir(self, rel):
        p = os.path.join(self.root, rel)
        os.makedirs(p)
        return p

    def raw(self, rel, data):
        p = self.path(rel)
        with open(p, 'xb') as f:
            f.write(data)
        return {'path': p, 'sha256': sha_bytes(data)}

    def json(self, rel, obj):
        if isinstance(obj, dict) and 'synthetic_fixture' not in obj:
            obj = dict(obj, synthetic_fixture=SYN)
        return self.raw(rel, self.C.encode_record(obj))

    def npz(self, rel, arrays):
        buf = io.BytesIO()
        np.savez(buf, **arrays)
        return self.raw(rel, buf.getvalue())


# ------------------------------------------------------------------------------------------------ world
class World:
    def __init__(self, a):
        self.a = a
        for k, (p, s) in REAL.items():
            if sha_file(p) != s:
                raise SystemExit('REAL PIN MISMATCH: ' + k)
        self.C = load_exact(REAL['common'][0], REAL['common'][1], 'ps_test_common')
        self.CU = load_exact(REAL['custody'][0], REAL['custody'][1], 'ps_test_custody')
        self.G = load_exact(REAL['guard'][0], REAL['guard'][1], 'ps_test_guard')
        self.LIB = load_exact(REAL['library'][0], REAL['library'][1], 'ps_test_uvt_lapse_v002')
        self.CFG = load_exact(REAL['lo_config'][0], REAL['lo_config'][1], 'ps_test_lo_config')
        self.V1 = self.CFG.V1
        b = os.path.realpath(a.build_dir)
        self.paths = {'slot': b + '/lo_slot_proof_c3v003_g1_c2v001.py', 'state': b + '/lo_state_proof_adapter_c3v003_ks6_c2v002.py',
                      'srb': b + '/srb_rot_adapter_c3v003_g2_c2v001.py'}   # PORT (G-wave): G1, KS6', G2
        self.shas = {k: sha_file(p) for k, p in self.paths.items()}
        self.SLOT = load_exact(self.paths['slot'], self.shas['slot'], 'ps_mod_slot')
        self.STATE = load_exact(self.paths['state'], self.shas['state'], 'ps_mod_state')
        self.SRB = load_exact(self.paths['srb'], self.shas['srb'], 'ps_mod_srb')
        self.fx = FX(a.fixture_root, self.C)
        roots = [ART]
        for extra in (self.fx.root, b):
            if not extra.startswith(ART + '/'):
                roots.append(extra)
        self.allowed_roots = tuple(roots)
        self.rulings = [{'path': REAL['ruling_a134'][0], 'sha256': REAL['ruling_a134'][1]},
                        {'path': REAL['ruling_0688'][0], 'sha256': REAL['ruling_0688'][1]}]
        self.pin = {k: {'path': p, 'sha256': s} for k, (p, s) in REAL.items()}
        self.approved = sorted({self.shas['slot'], self.shas['state'], self.shas['srb'],
                                REAL['eps_adapter'][1], REAL['gq_producer'][1]})
        self.approved_pins = [{'path': self.paths['slot'], 'sha256': self.shas['slot']},
                              {'path': self.paths['state'], 'sha256': self.shas['state']},
                              {'path': self.paths['srb'], 'sha256': self.shas['srb']},
                              self.pin['eps_adapter'], self.pin['gq_producer']]
        self.DETAILS = {}
        self.derive_calls = []
        self.core_calls = []
        if a.reader == 'custody':
            self.read_pin = lambda ref: self.CU.read_pin(ref)
            self.read_raw = lambda ref: self.CU.read_pin(ref, document=False)
            self.read_bytes = lambda p: self.CU.allowed_path(p).read_bytes()
            self.resolve = lambda p: self.CU.allowed_path(p)
        else:
            self.read_pin = lambda ref: json.loads(self._local(ref))
            self.read_raw = self._local
            self.read_bytes = lambda p: open(p, 'rb').read()
            self.resolve = lambda p: os.path.realpath(p)
        self.review_shas = []
        self.src_producer = None

    def _local(self, ref):
        if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'}:
            raise ValueError('exact byte reference required')
        raw = open(ref['path'], 'rb').read()
        if sha_bytes(raw) != ref['sha256']:
            raise ValueError('byte pin mismatch')
        return raw

    # -- synthetic custody / point
    def details(self, spec, tag, *, radii_m=None, tau=None):
        ident = self.C.point_identity(spec)
        n = 12
        radii_m = radii_m or [(0.5 + 0.7 * i) * KPC for i in range(n)]
        tau = tau or [3.0 + 0.25 * i for i in range(n)]
        rows = [{'id': 'ROW_%02d' % (i + 1), 'radius_m': r} for i, r in enumerate(radii_m)]
        row = {'schema': 'DDO154_POINT_ROWS_CX2V001', 'rows': rows, 'tau_km_s': tau,
               'distance_Mpc': spec['physical']['distance_Mpc'], 'synthetic_fixture': SYN + ' :: ' + tag}
        custody = {k: sha_bytes((tag + ':' + k).encode()) for k in
                   ('grid_sha256', 'background_sha256', 'geometry_sha256', 'modules_sha256')}
        custody['row_contract_sha256'] = self.C.digest(row)
        d = {'schema': 'DDO154_POINT_CUSTODY_CX2V001', 'identity': ident, 'point_sha256': self.C.digest(ident),
             'custody': custody, 'custody_sha256': self.C.digest(custody), 'row_contract': row}
        return d

    def derive_details(self, spec):
        self.derive_calls.append(spec.get('label'))
        return copy.deepcopy(self.DETAILS[spec['label']])

    def rho_record(self, d, rhos, *, settings='registered', partition=None, producer=None, utc='2026-10-19T00:00:00Z',
                   seconds=1.0, **over):
        partition = partition or [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                                  [32.0, 64.0], [64.0, 128.0], [128.0, 182.0]]
        shells = [{'range_inverse_kpc': list(p), 'rho_used': r,
                   'rho_envelope': {'estimate': r, 'seed': 20261018 + i, 'estimator_scope': 'synthetic'},
                   'sampled_levels': [{'level': 1, 'estimate': r * 0.5, 'n_samples': 10}]}
                  for i, (p, r) in enumerate(zip(partition, rhos))]
        rec = {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'utc': utc, 'status': 'TESTED',
               'identity': d['identity'], 'point_sha256': d['point_sha256'], 'custody': d['custody'],
               'producer': producer or self.pin['response'], 'dependencies': {}, 'settings': settings,
               'point_symbol_checks': {}, 'rigorous_supremum': False, 'production_admissible': False,
               'covers_all_consumed_states': False, 'limitation': 'synthetic', 'gate': 'RHO_G',
               'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED', 'shells': shells, 'coverage_complete': True,
               'required_coverage_inverse_kpc': [4.0, 182.0],
               'full_registered_search_executed': settings == 'registered', 'seconds': seconds, 'peak_rss_bytes': 1}
        rec.update(over)
        return rec

    def eps_record(self, d, *, eps_fn=None, env_fn=None, lo=4, hi=182, skip=()):
        eps_fn = eps_fn or (lambda k: 1e-4 + 1e-6 * k)
        env_fn = env_fn or (lambda k: 0.9 * eps_fn(k))
        shells = []
        for k in range(lo, hi):
            if k in skip:
                continue
            shells.append({'range_inverse_kpc': [float(k), float(k + 1)], 'lo_inverse_kpc': float(k),
                           'hi_inverse_kpc': float(k + 1), 'eps': eps_fn(k), 'eps_envelope': env_fn(k),
                           'eps_base': eps_fn(k), 'eps_refined': eps_fn(k), 'refinements': 0, 'certified': True})
        return {'schema': 'UNT_POINT_EPS_NUMERICAL_CX2V001', 'utc': '2026-10-19T00:00:00Z', 'status': 'TESTED',
                'identity': d['identity'], 'point_sha256': d['point_sha256'], 'custody': d['custody'],
                'producer': self.pin['response'], 'settings': 'registered', 'gate': 'EPS',
                'verdict': 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED', 'registered_discrete_verdict': 'CERTIFIED',
                'full_registered_search_executed': True, 'coverage_complete': True,
                'required_coverage_inverse_kpc': [4.0, 182.0], 'shells': shells,
                'eps_max': max(s['eps'] for s in shells) if shells else None,
                'envelope_rule': 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS'}

    def eps_proof(self, d, eps_pin, eps_rec):
        return {'schema': 'UNT_CALIBRATION_POINT_PROOF_CX2V001', 'gate': 'EPS', 'utc': '2026-10-19T00:00:00Z',
                'status': 'TESTED', 'verdict': 'PASS', 'point_sha256': d['point_sha256'],
                'custody_sha256': d['custody_sha256'], 'producer': self.pin['eps_adapter'],
                'driver_certificate': eps_pin, 'numeric_evidence': eps_pin,
                'envelope_rule': 'A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS',
                'shells': [{'range_inverse_kpc': s['range_inverse_kpc'], 'eps': s['eps'],
                            'eps_envelope': s['eps_envelope'], 'refinement_failures': 0} for s in eps_rec['shells']],
                'rigorous_supremum': False}

    def gq_proof(self, d):
        return {'schema': 'UNT_CALIBRATION_POINT_PROOF_CX2V001', 'gate': 'GQ', 'status': 'TESTED', 'verdict': 'PASS',
                'point_sha256': d['point_sha256'], 'custody_sha256': d['custody_sha256'],
                'producer': self.pin['gq_producer'], 'method': 'GEOMETRY_UNIFORM_COLUMN_BOUND',
                'all_columns_included': True, 'all_production_kperp_nodes': True, 'nonnegative_masses_required': True,
                'M_s': 128, 'M_s_doubled': 256, 'K_big_inverse_kpc': 128.0,
                'max_column_difference_over_analytic_Pi0': 1e-15, 'max_zero_mode_relative_error': 1e-6}

    # -- envs
    def slot_env(self, **over):
        e = types.SimpleNamespace(derive_details=self.derive_details, read_pin=self.read_pin, read_raw=self.read_raw,
                                  self_pin=self.SLOT._self_pin, utc=self.SLOT._utc)
        for k, v in over.items():
            setattr(e, k, v)
        return e

    def writer(self, obj, out_root, name):
        return self.C.write_new(os.path.join(out_root, name), obj, out_root)

    def state_env(self, **over):
        e = types.SimpleNamespace(derive_details=self.derive_details, read_pin=self.read_pin, read_raw=self.read_raw,
                                  read_bytes=self.read_bytes, resolve=self.resolve,
                                  point_context=lambda spec: {'synthetic_context': spec['label']},
                                  produce_current_lo=self.stub_core, validate_config=self.stub_validate,
                                  write=self.writer, self_pin=self.STATE._self_pin, utc=self.STATE._utc)
        for k, v in over.items():
            setattr(e, k, v)
        return e

    def srb_env(self, **over):
        r14raw = open(REAL['r14'][0], 'rb').read()

        def load_arrays(pin):
            raw = self.read_raw(pin)
            with np.load(io.BytesIO(raw), allow_pickle=False) as z:
                return {k: z[k] for k in z.files}
        e = types.SimpleNamespace(derive_details=self.derive_details, read_pin=self.read_pin, read_raw=self.read_raw,
                                  read_bytes=self.read_bytes, resolve=self.resolve, lib=lambda: self.LIB,
                                  load_arrays=load_arrays,
                                  apply_flag=lambda: self.SRB.extract_apply_flag(r14raw), write=self.writer,
                                  self_pin=self.SRB._self_pin, utc=self.SRB._utc)
        for k, v in over.items():
            setattr(e, k, v)
        return e

    # -- lo_core test doubles (I/O replaced; REAL aggregate_shares)
    def stub_validate(self, spec, obj):
        if obj.get('synthetic_validate_fail'):
            raise ValueError('actual state certificate slot mismatch (synthetic)')
        return {'normalized_config_sha256': 'synthetic', 'exact_production_nodes_verified': True,
                'certificate_slots_bound': not obj.get('synthetic_validate_unbound'), 'synthetic': True}   # F3 seam

    def stub_core(self, spec, ref, *, expected_state=None, trusted_source_producers=(), trusted_review_hashes=(),
                  settings='registered', shell_ranges=None, context=None, progress=None):
        self.core_calls.append({'label': spec.get('label'), 'expected_state': expected_state, 'settings': settings,
                                'shell_ranges': shell_ranges, 'trusted_review_hashes': list(trusted_review_hashes),
                                'trusted_source_producers': list(trusted_source_producers), 'context': context})
        d = self.DETAILS[spec['label']]
        obj = self.read_pin(ref)
        if obj.get('schema') != 'UNT_POINT_LO_STATE_INPUT_CX2V001':
            raise ValueError('reference schema mismatch')
        if obj.get('identity') != d['identity'] or obj.get('custody') != d['custody']:
            raise ValueError('point/custody mismatch')
        state, blockers = obj['state'], []
        if expected_state is None:
            blockers.append('NO_INDEPENDENT_CONSUMED_STATE_EXPECTATION')
        elif state != expected_state:
            raise ValueError('consumed state differs from independently enumerated state')
        row = self.read_pin(obj['row_reference'])
        ids = [r['id'] for r in d['row_contract']['rows']]
        R = np.asarray([r['radius_m'] for r in d['row_contract']['rows']], float)
        tau = np.asarray(d['row_contract']['tau_km_s'], float)
        if row.get('row_ids') != ids or row.get('row_contract_sha256') != d['custody']['row_contract_sha256']:
            raise ValueError('row order/custody mismatch')
        v = np.asarray(row['v_reference_km_s'], float)
        if (row.get('producer') or {}).get('sha256') not in trusted_source_producers:
            blockers.append('ROW_RECONSTRUCTION_PRODUCER_NOT_APPROVED')
        rv = row.get('policy_review')
        if not rv or rv.get('sha256') not in trusted_review_hashes:
            blockers.append('ROW_REFERENCE_POLICY_NOT_REVIEWED')
        blockers += list(obj.get('synthetic_extra_core_blockers', []))
        slot = self.read_pin(spec['numerics']['uv_tail']['lo_certificate'])
        rho = copy.deepcopy(obj.get('synthetic_rho_override') or slot)
        rho['utc'], rho['seconds'] = '2026-10-19T12:00:00Z', 0.25
        B1 = np.asarray(obj['synthetic_B1_unit_shells'], float)
        shares = self.V1.aggregate_shares(rho, np.arange(4.0, 183.0), B1, R, tau, np.abs(v))   # REAL lo_core L142-175
        if not rho['full_registered_search_executed']:
            blockers.append('FULL_POINT_RHO_NUMERICAL_SEARCH_UNTESTED')
        if not shares['all_nonzero_B1_consumed']:
            blockers.append('LO_SHELL_COVERAGE_INCOMPLETE')
        if not shares['numerical_thresholds_pass']:
            blockers.append('LO_NUMERICAL_INDICATOR_ABOVE_THRESHOLD')
        rec = dict(schema='UNT_POINT_LO_NUMERICAL_CX2V001', gate='LO', kind='CURRENT_SAVED_STATE',
                   utc='2026-10-19T12:00:00Z', status='TESTED',
                   producer=obj.get('synthetic_core_producer') or self.pin['lo_core'],
                   response_producer=self.pin['response'], identity=d['identity'], point_sha256=d['point_sha256'],
                   custody=d['custody'], production_admissible=False, cover_all_consumed_states=False,
                   covers_all_consumed_states=False, rigorous_supremum=False, driver_certificate=None,
                   limitations=['synthetic test double of lo_core produce_current_lo L190-267; aggregate_shares real'])
        rec.update(state=obj.get('synthetic_core_state') or state, state_input=ref,
                   state_digest_verified=state['state_sha256'], B1_recomputed={'synthetic': True}, rho=rho,
                   row_ids=ids, v_reference_km_s=np.abs(v).tolist(), **shares, blockers=blockers,
                   verdict='BLOCKED' if blockers else 'CURRENT_LO_NUMERICAL_EVIDENCE_REVIEW_REQUIRED',
                   custody_verified_without_scientific_approval=True, seconds=0.0, peak_rss_bytes=0,
                   synthetic_fixture=SYN)
        return rec


# ------------------------------------------------------------------------------------------------ scenario builders
DEFAULT_RHOS = [0.02, 0.019, 0.018, 0.017, 0.016, 0.015, 0.014, 0.013, 0.012]


def unit_b1(scale=1e-23, fail_shell=None, fail_factor=100.0):
    b = [scale / (1.0 + k / 10.0) for k in range(178)]
    if fail_shell is not None:
        for k in range(178):
            if 124 <= k:            # unit shells [128,182] -> rho shell [128,182]
                b[k] *= fail_factor
    return b


class Point:
    pass


def make_point(W, tag, base_spec, *, rhos=None, radii_m=None, tau=None):
    P = Point()
    P.tag = tag
    spec = copy.deepcopy(base_spec)
    spec['label'] = tag
    d = W.details(spec, tag, radii_m=radii_m, tau=tau)
    W.DETAILS[tag] = d
    P.details = d
    P.rho_rec = W.rho_record(d, rhos or DEFAULT_RHOS)
    P.rho_pin = W.fx.json(tag + '/rho_registered.json', P.rho_rec)
    P.eps_rec = W.eps_record(d)
    P.eps_pin = W.fx.json(tag + '/eps_numeric.json', P.eps_rec)
    spec['numerics']['uv_tail']['lo_certificate'] = P.rho_pin
    spec['numerics']['uv_tail']['eps_certificate'] = P.eps_pin
    P.spec = spec
    P.eps_proof_pin = W.fx.json(tag + '/eps_proof.json', W.eps_proof(d, P.eps_pin, P.eps_rec))
    P.gq_proof_pin = W.fx.json(tag + '/gq_proof.json', W.gq_proof(d))
    P.out = W.fx.dir(tag + '/out')
    return P


def anchor_pair(W, A):
    """Two synthetic registered rho runs at the anchor key (bitwise-equal rho, different run metadata)."""
    a = W.rho_record(A.details, DEFAULT_RHOS, utc='2026-10-19T01:00:00Z', seconds=31.0)
    b = W.rho_record(A.details, DEFAULT_RHOS, utc='2026-10-19T02:00:00Z', seconds=33.5)
    return [W.fx.json(A.tag + '/rho_anchor_run_1.json', a), W.fx.json(A.tag + '/rho_anchor_run_2.json', b)]


def slot_prove(W, P, pair, registered, **kw):
    args = dict(registered_rho_records=registered, anchor_rho_pair=pair, root_ruling_refs=W.rulings,
                approved_producer_sha256=W.approved)
    args.update({k: v for k, v in kw.items() if k != 'env'})
    return W.SLOT._prove(P.spec, kw.get('rho_ref', P.rho_pin), env=kw.get('env') or W.slot_env(),
                         **{k: v for k, v in args.items() if k != 'rho_ref'})


def bundle(W, P, slot_proof_pin, *, extra_prelaunch=None, bindings=None):
    pre = {'EPS': P.eps_proof_pin, 'GQ': P.gq_proof_pin, 'LO_RHO_SLOT': slot_proof_pin}
    pre.update(extra_prelaunch or {})
    b = {'schema': 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001', 'identity': P.details['identity'],
         'custody': P.details['custody'], 'domain': {'K_inverse_kpc': 4.0, 'K_big_inverse_kpc': 128.0},
         'prelaunch': pre, 'driver_certificate_bindings': bindings or {'eps_certificate': P.eps_pin, 'lo_certificate': P.rho_pin},
         'acceptance_rule': 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED', 'point_sha256': P.details['point_sha256'],
         'custody_sha256': P.details['custody_sha256']}
    return b


class Call:
    pass


def make_inventory(W, P, *, final_pass=2, rot_state=None, occurrences=True):
    def h(x):
        return sha_bytes((P.tag + ':' + x).encode())

    def S(name, kind, nonneg=True):
        return {'state_sha256': h(name + ':state'), 'source_sha256': h(name + ':source'), 'stage_kind': kind,
                'nonnegative_masses': nonneg}
    st = {'A0': S('A0', 'route_a'), 'A1': S('A1', 'route_a'), 'A2': S('A2', 'route_a'),
          'OFF': S('OFF', 'offset', False), 'F0': S('F0', 'fs_columns'), 'R0': S('R0', 'fs_rotation'),
          'RC0': S('RC0', 'rfs_columns')}
    for i in range(1, final_pass + 1):
        st['L%dC' % i] = S('L%dC' % i, 'le_columns')
        st['L%dR' % i] = S('L%dR' % i, 'le_rotation')
    if rot_state is not None:
        st['L%dR' % final_pass] = rot_state
    occ = []

    def O(stage, kind, role, state, it=None, **extra):
        o = {'ordinal': len(occ), 'stage': stage, 'stage_kind': kind, 'role': role, 'iteration': it,
             'state_sha256_claimed': None if state is None else state['state_sha256'],
             'source_sha256_claimed': None if state is None else state['source_sha256'],
             'evidence': {'path': '/synthetic/evidence', 'sha256': h('ev%d' % len(occ))}, 'guard_ready': False}
        o.update(extra)
        occ.append(o)
        return o
    O('route_a', 'route_a', 'current_begin_inferred_from_completion', st['A0'], 0)
    O('route_a', 'route_a', 'next_built_and_monitor_consumed', st['A1'], 1)
    O('route_a', 'route_a', 'current_begin_inferred_from_completion', st['A1'], 1)
    O('route_a', 'route_a', 'next_built_and_monitor_consumed', st['A2'], 2)
    O('route_a', 'route_a', 'boundary_at_return', st['A1'])
    O('reference', 'reference', 'inherited_route_a', st['A1'])
    O('body', 'body', 'inherited_route_a', st['A1'])
    O('offset', 'offset', 'signed_body_minus_route_a', st['OFF'])
    O('offset', 'offset_positive_component', 'body_gas_component', None)
    O('offset', 'offset_negative_component', 'route_a_gas_component', None)
    O('fs_columns_00', 'fs_columns', 'own_source_state', st['F0'])
    O('fs_rotation', 'fs_rotation', 'own_source_state', st['R0'])
    O('rfs_columns_00', 'rfs_columns', 'own_source_state', st['RC0'])
    for i in range(1, final_pass + 1):
        O('le%d_columns_00' % i, 'le_columns', 'own_source_state', st['L%dC' % i])
        O('le%d_rotation' % i, 'le_rotation', 'own_source_state', st['L%dR' % i])
    joined = [{'ordinal': o['ordinal'], 'state': next(s for s in st.values() if s['state_sha256'] == o['state_sha256_claimed'])}
              for o in occ if o['state_sha256_claimed'] is not None]
    order = ['A0', 'A1', 'A2', 'OFF', 'F0', 'R0', 'RC0'] + [k for i in range(1, final_pass + 1) for k in ('L%dC' % i, 'L%dR' % i)]
    inv = {'schema': 'DDO154_CONSUMED_STATE_JOIN_CX2V010', 'status': 'TESTED', 'complete': True,
           'states': [st[k] for k in order], 'blockers': [], 'certificate_status': 'UNAVAILABLE',
           'point_status': 'PENDING_CERTIFICATES', 'driver_sha256': DRIVER_SHA, 'producer': W.pin['enumerator'],
           'point_sha256': P.details['point_sha256'], 'custody_sha256': P.details['custody_sha256'],
           'verified_files': [], 'synthetic_fixture': SYN}
    if occurrences:
        inv['occurrences'] = occ
        inv['joined_occurrences'] = joined
    return inv, st


def passes_rows(ids, final_pass=2):
    out = []
    for p in range(final_pass):
        rows = []
        for i, rid in enumerate(ids):
            v = 30.0 + 2.0 * i + ((1.0 if i % 2 == 0 else -1.0) if p == final_pass - 1 else 0.0)
            rows.append({'id': rid, 'speed_km_s': v, 'valid': True})
        out.append({'pass': p + 1, 'rows': rows, 'max_abs_change_km_s': 1.0 if p else None})
    return out


def make_call(W, P, ctag, *, final_pass=2, passes=None, flagged=False, route_a_record=None, rot_state=None,
              occurrences=True):
    K = Call()
    K.tag = P.tag + '/' + ctag
    K.call_dir = W.fx.dir(K.tag + '/call')
    out = K.call_dir + '/out'
    os.makedirs(out)
    ids = [r['id'] for r in P.details['row_contract']['rows']]
    passes = passes_rows(ids, final_pass) if passes is None else passes
    ra = route_a_record or {'flags': ['TAIL_SOURCE_UNDERCONVERGED'] if flagged else [],
                            'monitor_status': 'FLAGGED' if flagged else 'M_T_WITHIN_THRESHOLD',
                            'M_T_accepted': 0.3 if flagged else 0.1, 'M_T_threshold': 0.25}
    K.result = {'status': 'COMPLETED', 'valid': True, 'passes': passes, 'final_pass': final_pass if passes else None,
                'uv_tail': {'route_a_record': ra}, 'synthetic_fixture': SYN}
    if passes:
        K.result['rows'] = passes[-1]['rows']
    K.result_pin = W.fx.json(K.tag + '/call/out/result.json', K.result)
    K.source_pins = [W.fx.raw(K.tag + '/call/out/source_%02d.bin' % i, (K.tag + ':src%d' % i).encode()) for i in range(2)]
    K.inventory, K.st = make_inventory(W, P, final_pass=final_pass, rot_state=rot_state, occurrences=occurrences)
    K.out = W.fx.dir(K.tag + '/lo_out')
    return K


def own_vmax(passes):
    vm = None
    for p in passes:
        v = [abs(r['speed_km_s']) if isinstance(r.get('speed_km_s'), (int, float)) else 0.0 for r in p['rows']]
        vm = v if vm is None else [max(a, b) for a, b in zip(vm, v)]
    return vm


def ensure_shared(W):
    if W.src_producer is None:
        W.src_producer = W.fx.raw('shared/synthetic_row_and_source_producer.py', b'# synthetic producer stand-in\n')
        W.review_pins = [W.fx.json('shared/row_policy_review_D%d.json' % i,
                                   {'schema': 'SYNTHETIC_ROW_POLICY_REVIEW', 'verdict': 'APPROVED', 'D_index': i})
                         for i in range(3)]
        W.review_shas = [p['sha256'] for p in W.review_pins]


def state_inputs(W, P, K, *, b1=None, overrides=None, row_over=None, missing=()):
    """Per-state synthetic input records (state input + row reference + source reconstruction)."""
    b1 = b1 or {}
    overrides = overrides or {}
    row_over = row_over or {}
    ensure_shared(W)
    ids = [r['id'] for r in P.details['row_contract']['rows']]
    vm = own_vmax(K.result['passes']) if K.result['passes'] else [0.0] * len(ids)
    out = {}
    for name, s in K.st.items():
        if name in missing:
            continue
        tag = K.tag + '/inputs/' + name
        src = W.fx.json(tag + '_source.json', {'schema': 'UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001',
                                               'source_files': K.source_pins, 'status': 'TESTED', 'verdict': 'PASS'})
        row = {'schema': 'UNT_POINT_LO_ROWS_CX2V001', 'state_sha256': s['state_sha256'], 'row_ids': ids,
               'row_contract_sha256': P.details['custody']['row_contract_sha256'],
               'R_m': [r['radius_m'] for r in P.details['row_contract']['rows']],
               'tau_km_s': P.details['row_contract']['tau_km_s'], 'v_reference_km_s': vm,
               'producer': W.src_producer, 'policy_review': W.review_pins[0], 'call_result': K.result_pin,
               'speed_reference_policy': W.STATE.SPEED_POLICY,
               'state_files': [K.result_pin]}           # F6: the call's own readout archive, inside <call_dir>/out
        ro = dict(row_over.get(name, {}))
        for k in ro.pop('__drop__', []):
            row.pop(k, None)
        row.update(ro)
        rowpin = W.fx.json(tag + '_rows.json', row)
        obj = {'schema': 'UNT_POINT_LO_STATE_INPUT_CX2V001', 'identity': P.details['identity'],
               'custody': P.details['custody'], 'state': s,
               'tail_state': {'record': {'path': '/synthetic/not_read_by_stub', 'sha256': '0' * 64},
                              'arrays': {'path': '/synthetic/not_read_by_stub', 'sha256': '0' * 64}},
               'row_reference': rowpin, 'source_reconstruction': src, 'call_result': K.result_pin,
               'execution': {'fresh_call': True, 'resumed': False, 'retried': False,
                             'route_a_completed_normally': True, 'run_root': K.call_dir + '/out'},
               'synthetic_B1_unit_shells': b1.get(name, unit_b1())}
        obj.update(overrides.get(name, {}))
        out[s['state_sha256']] = W.fx.json(tag + '_state_input.json', obj)
    return out


def run_state(W, P, K, inputs, *, bundle_pin, env=None, reviews=None, approved=None, rulings='default',
              inventory=None, result=None):
    return W.STATE._adapt_call(P.spec, call_dir=K.call_dir, result=K.result if result is None else result,
                               inventory=K.inventory if inventory is None else inventory, bundle_ref=bundle_pin,
                               state_inputs=inputs, root_ruling_refs=W.rulings if rulings == 'default' else rulings,
                               approved_producer_sha256=W.approved if approved is None else approved,
                               trusted_source_producers=[W.src_producer['sha256']],
                               trusted_row_policy_review_sha256=W.review_shas if reviews is None else reviews,
                               out_root=K.out, env=env or W.state_env())


def by_name(K, rec):
    rev = {s['state_sha256']: n for n, s in K.st.items()}
    return {rev.get(s['state']['state_sha256']): s for s in rec['states']}


# ------------------------------------------------------------------------------------------------ tests
def tests_common(W, A, Pc, pair, registered, slot_pass_pin):
    mods = (('slot', W.SLOT), ('state', W.STATE), ('srb', W.SRB))
    # C00: every pinned constant matches bytes.
    def consts():
        bad = []
        for name, m in mods:
            for k in ('COMMON', 'CUSTODY', 'LO_CONFIG', 'LO_CORE', 'LIBRARY', 'R14'):
                if hasattr(m, k):
                    p, s = getattr(m, k)
                    if sha_file(p) != s:
                        bad.append((name, k))
            for r in m.ROOT_RULINGS:
                if sha_file(r['path']) != r['sha256']:
                    bad.append((name, 'ROOT_RULINGS'))
            if hasattr(m, 'RESPONSE_SHA') and m.RESPONSE_SHA != REAL['response'][1]:
                bad.append((name, 'RESPONSE_SHA'))
            if hasattr(m, 'ENUMERATOR_SHA') and m.ENUMERATOR_SHA != REAL['enumerator'][1]:
                bad.append((name, 'ENUMERATOR_SHA'))
            if getattr(m, 'ANCHOR_KEY', ANCHOR_KEY) != ANCHOR_KEY or W.C.ANCHOR_KEY != ANCHOR_KEY:
                bad.append((name, 'ANCHOR_KEY'))
        return bad
    MP('C00_pinned_constants_match_bytes', 'hashes from bytes', consts, lambda v: v == [], '[]')
    # C01: root gate binding, for each module, before any custody derivation.
    for name, m in mods:
        for cid, refs in (('missing', None), ('reversed', list(reversed(W.rulings))),
                          ('wrong_sha', [dict(W.rulings[0], sha256='0' * 64), W.rulings[1]]),
                          ('only_a134', W.rulings[:1])):
            n0 = len(W.derive_calls)

            def go(refs=refs, m=m, name=name):
                if name == 'slot':
                    r = slot_prove(W, A, pair, registered, root_ruling_refs=refs)
                    return {'blockers': r['blockers'], 'verdict': r['verdict'], 'derive': len(W.derive_calls) - n0}
                if name == 'state':
                    K = W._cc_call
                    r = run_state(W, Pc, K, {}, bundle_pin=W._cc_bundle, rulings=refs)
                    return {'blockers': r['blockers'], 'verdict': r['call_lo_reading'], 'derive': len(W.derive_calls) - n0}
                r = W.SRB._adapt(Pc.spec, call_dir=W._cc_call.call_dir, result=W._cc_call.result,
                                 inventory=W._cc_call.inventory, bundle_ref=W._cc_bundle, state_input_ref=None,
                                 rows_input_ref=None, root_ruling_refs=refs, approved_producer_sha256=W.approved,
                                 trusted_source_producers=[], env=W.srb_env())
                return {'blockers': r['blockers'], 'verdict': r['verdict'], 'derive': len(W.derive_calls) - n0}
            MF('C01_%s_root_gate_%s' % (name, cid), 'root-gate binding (A134 56774ba7 + 0688 bcb6df8e)', go,
               lambda v: 'ROOT_RULING_A134_NOT_PINNED' in json.dumps(v) and v['derive'] == 0,
               'ROOT_RULING_A134_NOT_PINNED before any custody derivation')
    # C01b: right pins, but the ruling bytes are not the pinned bytes -> refused (read from bytes).
    v = raises(lambda: W.SLOT.root_gate(W.rulings, lambda ref: (_ for _ in ()).throw(ValueError('byte pin mismatch'))),
               'ROOT_RULING_UNREADABLE_OR_CHANGED')
    record('C01b_root_gate_bytes_reread', 'MUST_FAIL', 'root-gate binding (sha from bytes)', v['match'],
           'ROOT_RULING_UNREADABLE_OR_CHANGED', v)
    MP('C01c_root_gate_accepts_exact_pins', 'root-gate binding', lambda: W.SLOT.root_gate(W.rulings, W.read_raw),
       lambda v: v == W.rulings, 'returns the two pins')
    # C02: R4 canonical __file__.
    for name, m in mods:
        MP('C02_%s_self_pin_canonical' % name, 'canonical __file__ (R4)', lambda m=m: m._self_pin(),
           lambda v, name=name: v == {'path': W.paths[name], 'sha256': W.shas[name]}, 'pin == canonical path + sha')
        alias = os.path.join(W.fx.root, 'alias', os.path.basename(W.paths[name]))
        os.makedirs(os.path.dirname(alias), exist_ok=True)
        os.symlink(W.paths[name], alias)
        am = load_via(alias, 'ps_alias_' + name)
        v = raises(lambda am=am: am._self_pin(), 'NONCANONICAL_PRODUCER_FILE')
        record('C02_%s_alias_refused' % name, 'MUST_FAIL', 'canonical __file__ (R4)', v['match'],
               'NONCANONICAL_PRODUCER_FILE', v)
        W.__dict__.setdefault('aliases', {})[name] = alias
    # C03: exclusive create.
    def twice():
        res = slot_prove(W, Pc, pair, registered)
        d = W.fx.dir('c03_out')
        first = W.SLOT.write_proof(res, d, 'X.json')
        try:
            W.SLOT.write_proof(res, d, 'X.json')
        except FileExistsError as exc:
            return {'first': first, 'second': 'FileExistsError'}
        return {'first': first, 'second': 'WROTE_TWICE'}
    MF('C03_exclusive_create_second_write_refused', 'exclusive create', twice,
       lambda v: v.get('second') == 'FileExistsError', 'FileExistsError on the second write')
    v = raises(lambda: W.C.write_new(os.path.join(W.fx.root, 'outside.json'), {'x': 1}, os.path.join(W.fx.root, 'c03_out')),
               'OUTSIDE_ALLOWED_ROOTS')
    record('C03b_writer_refuses_outside_out_root', 'MUST_FAIL', 'exclusive create inside the named out root only',
           v['match'], 'OUTSIDE_ALLOWED_ROOTS', v)
    # C04: CLI refusals (taskpolicy -b; -I -B), each module and the suite itself.
    py = sys.executable
    unbg = ['-I', '-B', '-c', 'import os,sys; os.setpriority(4,0,0); os.execv(sys.argv[1], sys.argv[1:])', py]
    targets = [(n, W.paths[n]) for n in ('slot', 'state', 'srb')] + [('suite', os.path.realpath(__file__))]
    for name, path in targets:
        tail = ['--args', '/nonexistent.json', '--args-sha256', '0' * 64, '--out-root', '/nonexistent'] if name != 'suite' \
            else ['--build-dir', '/nonexistent', '--fixture-root', '/nonexistent', '--results-dir', '/nonexistent']
        r1 = subprocess.run([py] + unbg + ['-I', '-B', path] + tail, capture_output=True, text=True, timeout=120)
        record('C04_%s_without_taskpolicy_b_refused' % name, 'MUST_FAIL', 'taskpolicy -b required',
               'BACKGROUND_QOS_REQUIRED' in r1.stdout and r1.returncode == 2, 'BACKGROUND_QOS_REQUIRED, exit 2',
               (r1.returncode, r1.stdout[-300:], r1.stderr[-300:]))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        r2 = subprocess.run([TASKPOLICY, '-b', py, path] + tail, capture_output=True, text=True, timeout=120, env=env)
        record('C04_%s_without_I_B_refused' % name, 'MUST_FAIL', 'python3 -I -B required',
               'ISOLATED_INTERPRETER_REQUIRED' in r2.stdout and r2.returncode == 2, 'ISOLATED_INTERPRETER_REQUIRED, exit 2',
               (r2.returncode, r2.stdout[-300:], r2.stderr[-300:]))
        r3 = subprocess.run([TASKPOLICY, '-b', py, '-I', path] + tail, capture_output=True, text=True, timeout=120)
        record('C04_%s_I_without_B_refused' % name, 'MUST_FAIL', 'python3 -I -B required (-B missing)',
               'ISOLATED_INTERPRETER_REQUIRED' in r3.stdout and r3.returncode == 2, 'ISOLATED_INTERPRETER_REQUIRED, exit 2',
               (r3.returncode, r3.stdout[-300:], r3.stderr[-300:]))
        if name != 'suite':
            r4 = subprocess.run([TASKPOLICY, '-b', py, '-I', '-B', path] + tail, capture_output=True, text=True, timeout=120)
            record('C04_%s_with_b_I_B_passes_the_refusals' % name, 'MUST_PASS', 'taskpolicy -b -I -B accepted',
                   'REFUSED' not in r4.stdout and r4.returncode != 0 and r4.returncode != 2,
                   'past the refusals (then fails on the nonexistent args file)', (r4.returncode, r4.stdout[-200:], r4.stderr[-200:]))
    # C05: real environment wiring: lazy, and the real LO stack is the unchanged one at canonical paths.
    def lazy():
        before = set(sys.modules)
        envs = [W.SLOT._real_env(), W.STATE._real_env(), W.SRB._real_env()]
        new = sorted(set(sys.modules) - before)
        return {'new_modules': new, 'n': len(envs)}
    MP('C05_real_env_is_lazy', 'nothing loaded before the root gate', lazy, lambda v: v['new_modules'] == [], 'no module loaded')
    def stack():
        cfg = W.STATE._load_exact(W.STATE.LO_CONFIG[0], W.STATE.LO_CONFIG[1], 'ps_c05_lo_config')
        f = cfg.V1.produce_current_lo
        return {'core_file': cfg.V1.__file__, 'core_sha': sha_file(cfg.V1.__file__), 'co_filename': f.__code__.co_filename,
                'firstline': f.__code__.co_firstlineno, 'validate': cfg.validate_current_config.__code__.co_filename}
    MP('C05b_real_stack_is_unchanged_lo_core_L190', 'UNCHANGED lo_core produce_current_lo L190-267', stack,
       lambda v: v['core_file'] == REAL['lo_core'][0] and v['core_sha'] == REAL['lo_core'][1]
       and v['co_filename'] == REAL['lo_core'][0] and v['firstline'] == 190 and v['validate'] == REAL['lo_config'][0],
       'lo_core 12d36305 at its canonical path; produce_current_lo starts at L190')
    v = raises(lambda: W.STATE._load_exact(W.aliases['state'], W.shas['state'], 'ps_c05_alias'), 'NONCANONICAL_MODULE_PATH')
    record('C05c_loader_refuses_noncanonical_path', 'MUST_FAIL', 'canonical module paths (R4)', v['match'],
           'NONCANONICAL_MODULE_PATH', v)
    v = raises(lambda: W.STATE._load_exact(W.STATE.LO_CORE[0], '0' * 64, 'ps_c05_bad'), 'MODULE_PIN_MISMATCH')
    record('C05d_loader_refuses_sha_mismatch', 'MUST_FAIL', 'hashes from bytes', v['match'], 'MODULE_PIN_MISMATCH', v)
    # C06: no threshold re-declared in the three modules (numeric literals).
    def literals():
        found = []
        for name, m in mods:
            tree = ast.parse(open(W.paths[name]).read())
            for n in ast.walk(tree):
                if isinstance(n, ast.Constant) and type(n.value) is float and n.value in (0.005, 0.05, 0.1, 0.25, 0.0125, 1e-12):
                    found.append((name, n.lineno, n.value))
        return found
    MP('C06_no_threshold_literal_in_modules', 'no threshold re-declared', literals, lambda v: v == [], 'no 0.005/0.05/0.1/0.25/1e-12 literal')
    # C07: rho projection parity between the slot proof and the per-state adapter.
    def parity():
        recs = [A.rho_rec, Pc.rho_rec, W.rho_record(Pc.details, [0.0, -0.0, 1e-300, 5e-324, 1.0, 2.0, 3.0, 4.0, 5.0])]
        return [W.SLOT.rho_projection(r) == W.STATE.rho_projection(r) for r in recs]
    MP('C07_rho_projection_parity', 'one rho bitwise definition', parity, lambda v: v == [True, True, True], 'identical')


def tests_slot(W, A, Pc, pair, registered):
    ok = lambda v: v.get('verdict') == 'READY_FOR_MANIFEST' and isinstance(v.get('proof'), dict)
    res = MP('S01_slot_proof_ready', 'slot = registered rho; TESTED/PASS from approved producer',
             lambda: slot_prove(W, Pc, pair, registered), ok, 'READY_FOR_MANIFEST')
    MP('S01b_proof_never_carries_covers_all', 'covers_all_consumed_states refused (never emitted)',
       lambda: sorted(res['proof']), lambda v: 'covers_all_consumed_states' not in v and 'cover_all_consumed_states' not in v,
       'no covers_all_consumed_states / cover_all_consumed_states key')
    MP('S01c_proof_fields', 'slot proof schema',
       lambda: res['proof'], lambda p: p['schema'] == 'UNT_CALIBRATION_POINT_PROOF_CX2V001' and p['gate'] == 'LO_RHO_SLOT'
       and p['status'] == 'TESTED' and p['verdict'] == 'PASS' and p['driver_certificate'] == Pc.rho_pin
       and p['point_sha256'] == Pc.details['point_sha256'] and p['custody_sha256'] == Pc.details['custody_sha256']
       and p['producer'] == {'path': W.paths['slot'], 'sha256': W.shas['slot']} and p['lo_certified'] is False
       and p['anchor_rho_reproducibility']['bitwise_equal'] is True and p['root_rulings'] == W.rulings,
       'gate LO_RHO_SLOT, driver_certificate = rho pin, canonical producer, lo_certified false')
    MP('S01d_anchor_point_slot_proof_ready', '(a)4 at the anchor itself', lambda: slot_prove(W, A, pair, registered), ok,
       'READY_FOR_MANIFEST')
    fail = lambda code: (lambda v: v.get('verdict') == 'BLOCKED' and v.get('proof') is None and code in json.dumps(v['blockers']))
    MF('S02_unregistered_rho_refused', 'slot binds only a registered rho',
       lambda: slot_prove(W, Pc, pair, [p for p in registered if p != Pc.rho_pin]), fail('RHO_NOT_REGISTERED'), 'RHO_NOT_REGISTERED')
    other = W.fx.json(Pc.tag + '/rho_same_values_unregistered.json', W.rho_record(Pc.details, DEFAULT_RHOS, utc='2026-10-19T05:00:00Z'))
    sp = copy.deepcopy(Pc.spec); sp['numerics']['uv_tail']['lo_certificate'] = other
    P2 = copy.copy(Pc); P2.spec = sp
    MF('S03_same_rho_values_other_bytes_unregistered_refused', 'slot binds only a registered rho BY SHA',
       lambda: slot_prove(W, P2, pair, registered, rho_ref=other), fail('RHO_NOT_REGISTERED'), 'RHO_NOT_REGISTERED')
    alias = dict(Pc.rho_pin, path=Pc.rho_pin['path'].replace('/rho_registered.json', '/./rho_registered.json'))
    MF('S03b_registered_sha_other_path_refused', 'whole-dict registration match',
       lambda: slot_prove(W, Pc, pair, registered, rho_ref=alias), fail('RHO_NOT_REGISTERED'), 'RHO_NOT_REGISTERED')
    badsha = dict(Pc.rho_pin, sha256='f' * 64)
    sp = copy.deepcopy(Pc.spec); sp['numerics']['uv_tail']['lo_certificate'] = badsha
    Pbad = copy.copy(Pc); Pbad.spec = sp
    MF('S03c_wrong_sha_refused', 'hashes from bytes', lambda: slot_prove(W, Pbad, pair, registered + [badsha], rho_ref=badsha),
       fail('byte pin mismatch'), 'byte pin mismatch')
    sp = copy.deepcopy(Pc.spec); sp['numerics']['uv_tail']['lo_certificate'] = 'PENDING_UV_TAIL_CERTIFICATE'
    P3 = copy.copy(Pc); P3.spec = sp
    MF('S04_spec_slot_not_the_rho_refused', 'slot = the rho pin', lambda: slot_prove(W, P3, pair, registered),
       fail('LO_SLOT_NOT_BOUND_TO_REGISTERED_RHO'), 'LO_SLOT_NOT_BOUND_TO_REGISTERED_RHO')

    def variant(tag, **over):
        rec = W.rho_record(Pc.details, DEFAULT_RHOS, **over)
        pin = W.fx.json(Pc.tag + '/rho_variant_%s.json' % tag, rec)
        s = copy.deepcopy(Pc.spec); s['numerics']['uv_tail']['lo_certificate'] = pin
        P = copy.copy(Pc); P.spec = s
        return lambda: slot_prove(W, P, pair, registered + [pin], rho_ref=pin)
    MF('S05_smoke_rho_refused', 'no smoke rho', variant('smoke', settings='smoke'), fail('RHO_SETTINGS_NOT_REGISTERED'),
       'RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH')
    MF('S06_partial_partition_refused', 'registered partition only',
       variant('partial', partition=[[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0],
                                     [32.0, 64.0], [64.0, 128.0], [128.0, 181.0]]), fail('RHO_PARTITION_NOT_REGISTERED'),
       'RHO_PARTITION_NOT_REGISTERED')
    MF('S07_other_point_rho_refused', 'point/custody binding',
       variant('custody', custody=dict(Pc.details['custody'], grid_sha256='1' * 64)), fail('RHO_POINT_CUSTODY_MISMATCH'),
       'RHO_POINT_CUSTODY_MISMATCH')
    MF('S08_rho_producer_not_a1dcdea8_refused', 'rho producer pinned', variant('producer', producer=W.pin['lo_core']),
       fail('RHO_PRODUCER_NOT_RESPONSE_A1DCDEA8'), 'RHO_PRODUCER_NOT_RESPONSE_A1DCDEA8')
    MF('S09_anchor_pair_missing_refused', '(a)4 two registered anchor runs', lambda: slot_prove(W, Pc, [], registered),
       fail('ANCHOR_RHO_REPRODUCIBILITY_UNPROVEN'), 'ANCHOR_RHO_REPRODUCIBILITY_UNPROVEN')
    MF('S10_anchor_pair_one_record_twice_refused', '(a)4 two RUNS', lambda: slot_prove(W, Pc, [pair[0], pair[0]], registered),
       fail('ANCHOR_RHO_PAIR_NOT_TWO_RUNS'), 'ANCHOR_RHO_PAIR_NOT_TWO_RUNS')
    rr = list(DEFAULT_RHOS); rr[8] = nextup(rr[8])
    b_ulp = W.fx.json(A.tag + '/rho_anchor_run_ulp.json', W.rho_record(A.details, rr, utc='2026-10-19T03:00:00Z'))
    MF('S11_anchor_pair_one_ulp_apart_refused', '(a)4 BITWISE', lambda: slot_prove(W, Pc, [pair[0], b_ulp], registered + [b_ulp]),
       fail('ANCHOR_RHO_NOT_BITWISE_EQUAL'), 'ANCHOR_RHO_NOT_BITWISE_EQUAL')
    z = list(DEFAULT_RHOS); z[0] = 0.0
    zz = list(DEFAULT_RHOS); zz[0] = -0.0
    a0 = W.fx.json(A.tag + '/rho_anchor_zero_pos.json', W.rho_record(A.details, z, utc='2026-10-19T03:10:00Z'))
    a1 = W.fx.json(A.tag + '/rho_anchor_zero_neg.json', W.rho_record(A.details, zz, utc='2026-10-19T03:20:00Z'))
    MF('S11b_anchor_pair_plus_minus_zero_refused', '(a)4 BITWISE, not numeric equality',
       lambda: slot_prove(W, Pc, [a0, a1], registered + [a0, a1]), fail('ANCHOR_RHO_NOT_BITWISE_EQUAL'), 'ANCHOR_RHO_NOT_BITWISE_EQUAL')
    MF('S12_anchor_run_unregistered_refused', '(a)4 REGISTERED runs', lambda: slot_prove(W, Pc, pair, [Pc.rho_pin, pair[0]]),
       fail('ANCHOR_RHO_RUN_NOT_REGISTERED'), 'ANCHOR_RHO_RUN_NOT_REGISTERED')
    c2 = W.fx.json(Pc.tag + '/rho_corner_run_2.json', W.rho_record(Pc.details, DEFAULT_RHOS, utc='2026-10-19T04:00:00Z'))
    MF('S13_pair_not_at_anchor_key_refused', '(a)4 AT THE ANCHOR KEY', lambda: slot_prove(W, Pc, [Pc.rho_pin, c2], registered + [c2]),
       fail('ANCHOR_RHO_RUN_NOT_AT_ANCHOR_KEY'), 'ANCHOR_RHO_RUN_NOT_AT_ANCHOR_KEY')
    ra = list(DEFAULT_RHOS); ra[3] = nextdown(ra[3])
    a_other = W.fx.json(A.tag + '/rho_anchor_slot_differs.json', W.rho_record(A.details, ra, utc='2026-10-19T04:10:00Z'))
    sp = copy.deepcopy(A.spec); sp['numerics']['uv_tail']['lo_certificate'] = a_other
    A2 = copy.copy(A); A2.spec = sp
    MF('S14_anchor_slot_rho_not_equal_to_pair_refused', '(a)4 at the anchor slot', lambda: slot_prove(W, A2, pair, registered + [a_other], rho_ref=a_other),
       fail('ANCHOR_SLOT_RHO_NOT_BITWISE_EQUAL_TO_REPRODUCED_PAIR'), 'ANCHOR_SLOT_RHO_NOT_BITWISE_EQUAL_TO_REPRODUCED_PAIR')
    MF('S16_self_not_approved_refused', 'approved producer only', lambda: slot_prove(W, Pc, pair, registered, approved_producer_sha256=[REAL['eps_adapter'][1]]),
       fail('LO_SLOT_PROOF_PRODUCER_NOT_APPROVED'), 'LO_SLOT_PROOF_PRODUCER_NOT_APPROVED')
    forged = dict(res, proof=dict(res['proof'], covers_all_consumed_states=True))
    v = raises(lambda: W.SLOT.write_proof(forged, Pc.out, 'FORGED.json'), 'LO_SLOT_PROOF_MUST_NOT_CARRY')
    record('S17_writer_refuses_covers_all', 'MUST_FAIL', 'covers_all_consumed_states refused', v['match'], 'LO_SLOT_PROOF_MUST_NOT_CARRY', v)
    forged2 = dict(res, proof=dict(res['proof'], cover_all_consumed_states=False))
    v = raises(lambda: W.SLOT.write_proof(forged2, Pc.out, 'FORGED2.json'), 'LO_SLOT_PROOF_MUST_NOT_CARRY')
    record('S17b_writer_refuses_key_even_false', 'MUST_FAIL', 'the key never appears, with any value', v['match'], 'LO_SLOT_PROOF_MUST_NOT_CARRY', v)
    return res


def tests_wrapper_and_guard(W, Pc, slot_res, slot_pin):
    raw = open(REAL['wrapper'][0], 'rb').read()
    lines = raw.decode('utf-8').split('\n')
    blk = '\n'.join(lines[144:161]) + '\n'
    MP('W00_wrapper_block_is_r10_c4_L145_161', 'existing wrapper structure (ef3d3d69 bytes)',
       lambda: sha_bytes(blk.encode()), lambda v: v == WRAPPER_BLOCK_SHA and blk.count(OLD_L148) == 1 and blk.count(OLD_L160) == 1,
       WRAPPER_BLOCK_SHA)

    class Error(Exception):
        pass
    ns_o = extract_functions(REAL['parent_v005'][0], REAL['parent_v005'][1], ['sha256_bytes', 'read_pinned'],
                             {'hashlib': hashlib, 'Path': __import__('pathlib').Path, 'OrchestratorError': Error})
    O = types.SimpleNamespace(read_pinned=ns_o['read_pinned'])
    ns_m = extract_functions(REAL['wrapper_core'][0], REAL['wrapper_core'][1], ['canonical', 'digest', 'pin_doc'],
                             {'json': json, 'hashlib': hashlib, 'O': O})
    M = types.SimpleNamespace(pin_doc=ns_m['pin_doc'], digest=ns_m['digest'])

    def block(patched):
        b = blk.replace(OLD_L148, NEW_L148).replace(OLD_L160, NEW_L160) if patched else blk
        src = 'def _slot_block(spec, bundle, custody, ident, r, M, O, G, Error):\n' + textwrap.indent(textwrap.dedent(b), '    ') + '    return "ACCEPTED"\n'
        ns = {}
        exec(compile(src, '<r10_c4 L145-161%s>' % (' + A134 Q5 patch' if patched else ''), 'exec'), ns)
        return ns['_slot_block']

    r = {'approved_certificate_producers': W.approved_pins}
    ident, custody = Pc.details['identity'], Pc.details['custody']

    def run(patched, bun, rr=None):
        return block(patched)(Pc.spec, bun, custody, ident, rr or r, M, O, W.G, Error)
    b0 = bundle(W, Pc, slot_pin)
    MP('W01_successor_patch_accepts_slot_proof', 'wrapper r10_c4 structure + stated Q5 change accepts the proof',
       lambda: run(True, b0), lambda v: v == 'ACCEPTED', 'ACCEPTED')
    b1 = bundle(W, Pc, slot_pin, extra_prelaunch={'LO_ENVELOPE': slot_pin})
    v = raises(lambda: run(False, b1), 'LO_ENVELOPE proof schema/gate/custody mismatch')
    record('W02_unchanged_r10_c4_refuses_slot_proof', 'MUST_FAIL', 'retired envelope route cannot be satisfied by the slot proof',
           v['match'], 'LO_ENVELOPE proof schema/gate/custody mismatch', v)
    forged = dict(slot_res['proof'], covers_all_consumed_states=True)
    fp = W.fx.json(Pc.tag + '/forged_slot_proof_covers_all.json', forged)
    v = raises(lambda: run(True, bundle(W, Pc, fp)), 'must not carry covers_all_consumed_states')
    record('W03_successor_refuses_covers_all', 'MUST_FAIL', 'covers_all_consumed_states refused', v['match'],
           'LO slot proof must not carry covers_all_consumed_states', v)
    notrho = W.fx.json(Pc.tag + '/old_lo_numeric_record.json', {'schema': 'UNT_POINT_LO_NUMERICAL_CX2V001', 'gate': 'LO',
                                                               'point_sha256': Pc.details['point_sha256'], 'custody': custody})
    sp = copy.deepcopy(Pc.spec); sp['numerics']['uv_tail']['lo_certificate'] = notrho
    pr = dict(slot_res['proof'], driver_certificate=notrho)
    pp = W.fx.json(Pc.tag + '/slot_proof_on_non_rho.json', pr)
    bb = bundle(W, Pc, pp, bindings={'eps_certificate': Pc.eps_pin, 'lo_certificate': notrho})
    v = raises(lambda: block(True)(sp, bb, custody, ident, r, M, O, W.G, Error), "lo slot is not this point's rho record")
    record('W04_successor_refuses_non_rho_slot', 'MUST_FAIL', 'slot = the point\'s rho record', v['match'],
           "lo slot is not this point's rho record", v)
    al = dict(slot_res['proof'], producer={'path': W.aliases['slot'], 'sha256': W.shas['slot']})
    ap = W.fx.json(Pc.tag + '/slot_proof_alias_producer.json', al)
    v = raises(lambda: run(True, bundle(W, Pc, ap)), 'LO_RHO_SLOT producer is not approved')
    record('W05_successor_refuses_alias_producer_pin', 'MUST_FAIL', 'whole-dict producer pin (R4)', v['match'],
           'LO_RHO_SLOT producer is not approved', v)
    other_rho = W.fx.json(Pc.tag + '/rho_other_for_w06.json', W.rho_record(Pc.details, DEFAULT_RHOS, utc='2026-10-19T06:00:00Z'))
    od = dict(slot_res['proof'], driver_certificate=other_rho)
    op = W.fx.json(Pc.tag + '/slot_proof_other_rho.json', od)
    v = raises(lambda: run(True, bundle(W, Pc, op)), 'LO_RHO_SLOT proof differs from attached driver certificate')
    record('W06_successor_refuses_proof_for_other_rho', 'MUST_FAIL', 'proof binds the attached slot', v['match'],
           'proof differs from attached driver certificate', v)
    # Guard v003 prelaunch on the bundle with the real slot proof.
    bp = W.fx.json(Pc.tag + '/bundle_prelaunch.json', b0)
    g = MP('G01_guard_v003_prelaunch_accepts_bundle', 'guard verify_bundle(prelaunch) accepts the bundle',
           lambda: W.G.verify_bundle(bp, ident, expected_custody=custody, approved_producer_sha256=W.approved,
                                     phase='prelaunch', allowed_roots=W.allowed_roots),
           lambda v: v.get('ok') is True and v.get('blockers') == [], 'ok True')
    return bp, b0


def tests_state(W, A, Pc, pair, registered, slot_pin_c, bundle_pin_c, slot_pin_a, bundle_pin_a):
    # L01: all PASS.
    K = make_call(W, Pc, 'L01')
    W._l01_call = K
    inp = state_inputs(W, Pc, K)
    rec = MP('L01_all_states_pass', 'per-state LO, unchanged core, all consumed states',
             lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_c),
             lambda v: v['call_lo_reading'] == 'PASS' and len(v['states']) == len(K.inventory['states'])
             and all(s['verdict'] == 'PASS' for s in v['states']) and len(v['lo_rows_for_acceptance_bundle']) == len(v['states']),
             'call PASS; every state PASS; one LO row per state')
    MP('L01b_core_called_unchanged_contract', 'core args: expected_state, registered, full shells, the 3 reviews',
       lambda: W.core_calls[-len(K.inventory['states']):],
       lambda v: len(v) == len(K.inventory['states']) and all(c['settings'] == 'registered' and c['shell_ranges'] is None
           and c['trusted_review_hashes'] == W.review_shas and c['expected_state'] in K.inventory['states'] for c in v)
       and [c['expected_state'] for c in v] == K.inventory['states'], 'settings registered; shell_ranges None; reviews; expected_state each')
    MP('L01c_point_context_once_per_call', 'context computed once per call', lambda: [c['context'] for c in W.core_calls[-len(K.inventory['states']):]],
       lambda v: all(x == {'synthetic_context': Pc.tag} for x in v), 'same context object for every state')
    MP('L01d_state_class_mapping', 'Q5 classes from the inventory',
       lambda: {n: s['state_class'] for n, s in by_name(K, rec).items()},
       lambda v: v['A1'] == 'ACCEPTED_ROUTE_A' and v['A0'] == 'ROUTE_A_PRE_ACCEPTANCE_ITERATE' and v['A2'] == 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'
       and v['OFF'] == 'ROUTE_B_STAGE' and v['L2R'] == 'ROUTE_B_STAGE' and v['F0'] == 'ROUTE_B_STAGE', 'A1 accepted; A0/A2 iterates; route-B stages')
    MP('L01e_summed_lo_recorded_for_RC2', 'Q4c: summed LO in the acceptance record',
       lambda: rec['summed_lo_for_RC2'], lambda v: v['complete'] is True and v['max_over_states'] is not None
       and len(v['per_state']) == len(K.inventory['states']), 'per-state sums and the max')
    # G02: guard v003 acceptance on these LO proofs (synthetic GQ_SIGNED for the offset state).
    def acceptance(rec_, K_, drop=None, tamper=None, vtag='main'):
        pre = W.read_pin(bundle_pin_c)
        rows = []
        for row in rec_['lo_rows_for_acceptance_bundle']:
            if drop is not None and row['state'] == drop:
                continue
            lo = row['LO']
            if tamper is not None and row['state'] == tamper:
                p = W.read_pin(lo)
                p['shells'][0]['max_over_tau'] = nextup(0.005)
                lo = W.fx.json(K_.tag + '/acc_%s/tampered_lo_proof.json' % vtag, p)
            entry = {'state': row['state'], 'LO': lo}
            if row['state']['nonnegative_masses'] is False:
                mb, ma, z, b = 3.0, 1.0, 1e-6, 1e-15
                tv, low = mb + ma, abs(mb - ma) - z * (mb + ma)
                sg = {'schema': 'UNT_CALIBRATION_POINT_PROOF_CX2V001', 'gate': 'GQ_SIGNED', 'status': 'TESTED', 'verdict': 'PASS',
                      'point_sha256': Pc.details['point_sha256'], 'custody_sha256': Pc.details['custody_sha256'],
                      'producer': W.pin['gq_producer'], 'state': row['state'], 'method': 'TV_BOUND_WITH_SIGNED_P0',
                      'normalization': 'ABS_SIGNED_ZERO_MODE', 'positive_components_verified': True,
                      'GQ_uniform_proof_sha256': pre['prelaunch']['GQ']['sha256'],
                      'signed_offset_policy': {'branch': 'CONSERVATIVE_FINITE_DENOMINATOR', 'ruling': W.pin['ruling_0528'],
                                               'max_component_alternative_adopted': False},
                      'body_mass_kg': mb, 'route_a_mass_kg': ma, 'component_mass_sum_kg': tv,
                      'P0_abs_signed_mass_lower_bound_kg': low, 'max_difference_over_signed_P0_bound': b * tv / low}
                entry['GQ_SIGNED'] = W.fx.json(K_.tag + '/acc_%s/gq_signed_%s.json' % (vtag, row['state']['state_sha256'][:12]), sg)
            rows.append(entry)
        acc = dict(pre, states=rows, parent_prelaunch_bundle=bundle_pin_c)
        ap = W.fx.json(K_.tag + '/acc_%s/bundle_acceptance.json' % vtag, acc)
        return W.G.verify_bundle(ap, Pc.details['identity'], expected_custody=Pc.details['custody'],
                                 approved_producer_sha256=W.approved, phase='acceptance',
                                 required_states=K_.inventory['states'], allowed_roots=W.allowed_roots)
    MP('G02_guard_v003_acceptance_accepts_lo_proofs', 'feeds the guard acceptance phase (L155-219)', lambda: acceptance(rec, K),
       lambda v: v.get('ok') is True, 'ok True')
    MF('G03_guard_acceptance_missing_state_refused', 'every consumed state', lambda: acceptance(rec, K, drop=K.st['L2R'], vtag='drop'),
       lambda v: v.get('ok') is False and 'state inventory mismatch' in json.dumps(v['blockers']), 'state inventory mismatch')
    MF('G04_guard_threshold_mechanical', 'thresholds stay mechanical in the guard', lambda: acceptance(rec, K, tamper=K.st['A1'], vtag='tamper'),
       lambda v: v.get('ok') is False and 'LO per-shell threshold failed' in json.dumps(v['blockers']), 'LO per-shell threshold failed')

    def scenario(tag, *, P=None, bundle_pin=None, call_kw=None, inp_kw=None, run_kw=None):
        P = P or Pc
        K_ = make_call(W, P, tag, **(call_kw or {}))
        kw = dict(inp_kw or {})
        if callable(kw.get('b1')):
            kw['b1'] = kw['b1'](K_)
        if callable(kw.get('overrides')):
            kw['overrides'] = kw['overrides'](K_)
        if callable(kw.get('row_over')):
            kw['row_over'] = kw['row_over'](K_)
        inp_ = state_inputs(W, P, K_, **kw)
        r_ = run_state(W, P, K_, inp_, bundle_pin=bundle_pin or bundle_pin_c, **(run_kw or {}))
        return K_, r_
    unav = lambda code: (lambda v: v[1]['call_lo_reading'] == 'INCOMPLETE' and any(code in json.dumps(s['blockers']) for s in v[1]['states']))
    # L02: rho recompute must be bitwise equal to the slot.
    rr = list(DEFAULT_RHOS); rr[5] = nextup(rr[5])
    bad_rho = W.rho_record(Pc.details, rr)
    MF('L02_rho_recompute_one_ulp_off_refused', 'rho recompute bitwise equal to the slot',
       lambda: scenario('L02', inp_kw={'overrides': lambda K_: {'A1': {'synthetic_rho_override': bad_rho}}}),
       lambda v: by_name(v[0], v[1])['A1']['verdict'] == 'UNAVAILABLE' and v[1]['call_lo_reading'] == 'INCOMPLETE'
       and 'RHO_RECOMPUTE_NOT_BITWISE_EQUAL_TO_SLOT' in json.dumps(by_name(v[0], v[1])['A1']['blockers']),
       'A1 UNAVAILABLE RHO_RECOMPUTE_NOT_BITWISE_EQUAL_TO_SLOT; call INCOMPLETE')
    # L03-L08: |v_i| own call only.
    MF('L03_observed_ddo_speeds_refused', '|v_i| never observed DDO154 speeds',
       lambda: scenario('L03', inp_kw={'row_over': lambda K_: {'A1': {'v_reference_km_s': [47.0 + i for i in range(12)]}}}),
       lambda v: 'ROW_SPEED_NOT_OWN_CALL_MAX' in json.dumps(by_name(v[0], v[1])['A1']['blockers']), 'ROW_SPEED_NOT_OWN_CALL_MAX')
    Kx = make_call(W, Pc, 'L04_other_call')
    MF('L04_another_calls_readouts_refused', '|v_i| never another call\'s speeds',
       lambda: scenario('L04', inp_kw={'row_over': lambda K_: {'OFF': {'call_result': Kx.result_pin}}}),
       lambda v: 'ROW_REFERENCE_NOT_OWN_CALL' in json.dumps(by_name(v[0], v[1])['OFF']['blockers']), 'ROW_REFERENCE_NOT_OWN_CALL')
    other_vmax = [x * 1.5 for x in own_vmax(passes_rows(['ROW_%02d' % (i + 1) for i in range(12)]))]
    MF('L04b_another_points_speeds_refused', '|v_i| never another point\'s speeds',
       lambda: scenario('L04b', inp_kw={'row_over': lambda K_: {'F0': {'v_reference_km_s': other_vmax}}}),
       lambda v: 'ROW_SPEED_NOT_OWN_CALL_MAX' in json.dumps(by_name(v[0], v[1])['F0']['blockers']), 'ROW_SPEED_NOT_OWN_CALL_MAX')
    n0 = [len(W.core_calls)]
    MF('L05_no_readout_unavailable_no_substitution', 'no readout -> UNAVAILABLE, nothing substituted',
       lambda: (lambda r: (r, len(W.core_calls) - n0[0]))(scenario('L05', call_kw={'passes': []})),
       lambda v: all(s['verdict'] == 'UNAVAILABLE' and 'OWN_CALL_READOUT_UNAVAILABLE' in json.dumps(s['blockers'])
                     for s in v[0][1]['states']) and v[0][1]['call_lo_reading'] == 'INCOMPLETE' and v[1] == 0,
       'every state UNAVAILABLE; the core never ran')
    def nan_passes():
        p = passes_rows(['ROW_%02d' % (i + 1) for i in range(12)])
        p[0]['rows'][3]['speed_km_s'] = None
        return p
    MF('L06_missing_readout_unavailable', 'every readout must exist', lambda: scenario('L06', call_kw={'passes': nan_passes()}),
       lambda v: all('OWN_CALL_READOUT_UNAVAILABLE' in json.dumps(s['blockers']) for s in v[1]['states']), 'OWN_CALL_READOUT_UNAVAILABLE')
    final_only = [r['speed_km_s'] for r in passes_rows(['ROW_%02d' % (i + 1) for i in range(12)])[-1]['rows']]
    MF('L07_final_pass_speeds_only_refused', '|v_i| = max over EVERY readout (not the final pass alone)',
       lambda: scenario('L07', inp_kw={'row_over': lambda K_: {'L2R': {'v_reference_km_s': final_only}}}),
       lambda v: 'ROW_SPEED_NOT_OWN_CALL_MAX' in json.dumps(by_name(v[0], v[1])['L2R']['blockers']), 'ROW_SPEED_NOT_OWN_CALL_MAX')
    MP('L07b_vmax_is_elementwise_max_over_passes', '|v_i| = max over every readout of row i',
       lambda: W.STATE.own_call_vmax({'passes': passes_rows(['R1', 'R2', 'R3'])}, ['R1', 'R2', 'R3']),
       lambda v: v == [31.0, 32.0, 35.0], '[31, 32, 35]: even rows from pass 2, odd rows from pass 1')
    MF('L08_speed_policy_string_missing_refused', 'Q4a policy bound in the row reference',
       lambda: scenario('L08', inp_kw={'row_over': lambda K_: {'A0': {'speed_reference_policy': 'PENDING'}}}),
       lambda v: 'ROW_REFERENCE_SPEED_POLICY_NOT_Q4A' in json.dumps(by_name(v[0], v[1])['A0']['blockers']), 'ROW_REFERENCE_SPEED_POLICY_NOT_Q4A')
    # L09: frozen readings.
    fb = lambda names: (lambda K_: {n: unit_b1(fail_shell=True) for n in names})
    reading = lambda want: (lambda v: v[1]['call_lo_reading'] == want)
    MF('L09a_fail_at_accepted_state_NLTM', 'Q5: accepted route-A failure', lambda: scenario('L09a', inp_kw={'b1': fb(['A1'])}),
       lambda v: v[1]['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL' and by_name(v[0], v[1])['A1']['verdict'] == 'FAIL'
       and by_name(v[0], v[1])['A1']['reading'] == 'NON_LAPSE_TAIL_MATERIAL' and v[1]['lo_gate_passed_all_states'] is False,
       'NON_LAPSE_TAIL_MATERIAL')
    MF('L09b_fail_at_route_b_stage_NLTM', 'Q5: route-B stage failure', lambda: scenario('L09b', inp_kw={'b1': fb(['L1C'])}),
       reading('NON_LAPSE_TAIL_MATERIAL'), 'NON_LAPSE_TAIL_MATERIAL')
    MF('L09c_fail_at_offset_stage_NLTM', 'Q5: route-B (offset) stage failure', lambda: scenario('L09c', inp_kw={'b1': fb(['OFF'])}),
       reading('NON_LAPSE_TAIL_MATERIAL'), 'NON_LAPSE_TAIL_MATERIAL')
    MF('L09d_fail_confined_to_iterates_TRANSIENT', 'Q5: route-A iterates before acceptance',
       lambda: scenario('L09d', inp_kw={'b1': fb(['A0', 'A2'])}),
       lambda v: v[1]['call_lo_reading'] == 'LO_UNCERTIFIED_TRANSIENT' and v[1]['lo_gate_passed_all_states'] is False,
       'LO_UNCERTIFIED_TRANSIENT (fails closed)')
    MF('L09e_iterate_fail_plus_unavailable_INCOMPLETE', 'Q5: transient needs every non-iterate state PASS (OPEN-6; F0 is one)',
       lambda: scenario('L09e', inp_kw={'b1': fb(['A0']), 'missing': ('F0',)}), reading('INCOMPLETE'), 'INCOMPLETE')
    MF('L09f_accepted_fail_plus_unavailable_NLTM', 'Q5: decisive failure (OPEN-6)',
       lambda: scenario('L09f', inp_kw={'b1': fb(['A1']), 'missing': ('F0',)}), reading('NON_LAPSE_TAIL_MATERIAL'), 'NON_LAPSE_TAIL_MATERIAL')
    MF('L09g_anchor_failure_step4_stops', 'Q5: anchor failure preserved; step 4 stops for root',
       lambda: scenario('L09g', P=A, bundle_pin=bundle_pin_a, inp_kw={'b1': fb(['L2C'])}),
       lambda v: v[1]['call_lo_reading'] == 'ANCHOR_LO_FAILURE_PRESERVED_STEP4_STOPS_FOR_ROOT' and v[1]['step4_stop'] is True
       and v[1]['class_reading'] == 'NON_LAPSE_TAIL_MATERIAL', 'anchor stop; class reading recorded beside it')
    MP('L09g2_anchor_all_pass', 'anchor call passes when every state passes',
       lambda: scenario('L09g2', P=A, bundle_pin=bundle_pin_a), lambda v: v[1]['call_lo_reading'] == 'PASS', 'PASS')
    MF('L09h_class_unavailable_gap_recorded', 'Q5 readings only when the class is available',
       lambda: scenario('L09h', call_kw={'occurrences': False}, inp_kw={'b1': fb(['A1'])}),
       lambda v: v[1]['call_lo_reading'] == 'LO_FAIL_STATE_CLASS_UNAVAILABLE'
       and any('STATE_CLASS_UNAVAILABLE' in b for b in v[1]['blockers'])
       and all(s['state_class'] == 'UNAVAILABLE' for s in v[1]['states']), 'LO_FAIL_STATE_CLASS_UNAVAILABLE; gap recorded')
    def classifier():
        inv, st = make_inventory(W, Pc)
        inv['occurrences'].append({'ordinal': len(inv['occurrences']), 'stage': 'reference_x', 'stage_kind': 'reference',
                                   'role': 'inherited_route_a', 'state_sha256_claimed': st['F0']['state_sha256']})
        inv['joined_occurrences'].append({'ordinal': inv['occurrences'][-1]['ordinal'], 'state': st['F0']})
        c, gap, acc = W.STATE.state_classes(inv)
        return {'F0': c[W.STATE.digest(st['F0'])][0], 'A1': c[W.STATE.digest(st['A1'])][0], 'gap': gap}
    MP('L09i_inherited_class_precedence', 'Q5 class precedence (accepted > inherited > route-B > iterate)', classifier,
       lambda v: v['F0'] == 'INHERITED_ROUTE_A' and v['A1'] == 'ACCEPTED_ROUTE_A' and v['gap'] is None, 'INHERITED for a non-accepted inherited digest')
    # L10: threshold boundary decided by the REAL registered arithmetic, not by this module.
    unit_tau = [1.0] * 12
    Pb = make_point(W, 'BOUNDARY', W._corner_spec, rhos=[1.0] * 9, radii_m=[1.0] * 12, tau=unit_tau)
    pb_res = slot_prove(W, Pb, pair, registered + [Pb.rho_pin])
    pb_slot = W.SLOT.write_proof(pb_res, Pb.out)
    pb_bundle = W.fx.json(Pb.tag + '/bundle_prelaunch.json', bundle(W, Pb, pb_slot))
    ones = [{'pass': 1, 'rows': [{'id': 'ROW_%02d' % (i + 1), 'speed_km_s': 1.0} for i in range(12)]}]
    edge = [0.0] * 178
    edge[0] = 0.02
    over = [0.0] * 178
    over[0] = nextup(0.02)
    MP('L10_at_threshold_passes', 'no threshold re-declared: max_over_tau == 0.005 passes (core <=)',
       lambda: scenario('L10', P=Pb, bundle_pin=pb_bundle, call_kw={'passes': ones, 'final_pass': 1},
                        inp_kw={'b1': lambda K_: {n: edge for n in K_.st}}),
       lambda v: v[1]['call_lo_reading'] == 'PASS' and all(s['summed_max_over_tau'] == 0.005 for s in v[1]['states']), 'PASS at exactly 0.005')
    MF('L10b_one_ulp_above_fails', 'no threshold re-declared: one ulp above fails (core)',
       lambda: scenario('L10b', P=Pb, bundle_pin=pb_bundle, call_kw={'passes': ones, 'final_pass': 1},
                        inp_kw={'b1': lambda K_: {n: (over if n == 'L1C' else edge) for n in K_.st}}),
       lambda v: by_name(v[0], v[1])['L1C']['verdict'] == 'FAIL' and v[1]['call_lo_reading'] == 'NON_LAPSE_TAIL_MATERIAL', 'FAIL')
    # L11-L19: other fail-closed paths.
    MF('L11_threshold_fail_with_other_blocker_is_unavailable', 'actual failure needs otherwise-clean inputs',
       lambda: scenario('L11', inp_kw={'b1': fb(['A1']), 'overrides': lambda K_: {'A1': {'synthetic_extra_core_blockers': ['SOURCE_RECONSTRUCTION_INCOMPLETE']}}}),
       lambda v: by_name(v[0], v[1])['A1']['verdict'] == 'UNAVAILABLE' and v[1]['call_lo_reading'] == 'INCOMPLETE', 'UNAVAILABLE, not FAIL')
    MF('L11b_unreviewed_row_policy_unavailable', 'row-reference policy review required (core L225-231)',
       lambda: scenario('L11b', run_kw={'reviews': ['e' * 64]}),
       lambda v: all('ROW_REFERENCE_POLICY_NOT_REVIEWED' in json.dumps(s['blockers']) for s in v[1]['states']), 'ROW_REFERENCE_POLICY_NOT_REVIEWED')
    inc = copy.deepcopy(K.inventory); inc['complete'] = False
    MF('L12_incomplete_inventory_refused', 'complete v010 inventory', lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_c, inventory=inc),
       lambda v: v['call_lo_reading'] == 'INCOMPLETE' and 'COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED' in json.dumps(v['blockers']), 'COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED')
    badp = copy.deepcopy(K.inventory); badp['producer'] = dict(badp['producer'], sha256='d' * 64)
    MF('L13_inventory_producer_not_b1_refused', 'enumerator 4ca7f364 (c3v003 V02)', lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_c, inventory=badp),
       lambda v: 'INVENTORY_PRODUCER_NOT_B1_4CA7F364' in json.dumps(v['blockers']), 'INVENTORY_PRODUCER_NOT_B1_4CA7F364')
    MF('L14_missing_state_input_unavailable', 'every consumed state needs its input', lambda: scenario('L14', inp_kw={'missing': ('L1R',)}),
       lambda v: 'STATE_INPUT_MISSING' in json.dumps(by_name(v[0], v[1])['L1R']['blockers']) and v[1]['call_lo_reading'] == 'INCOMPLETE', 'STATE_INPUT_MISSING')
    MF('L15_resumed_call_unavailable', 'fresh, completed, no resume (v004 L56-59)',
       lambda: scenario('L15', inp_kw={'overrides': lambda K_: {'A0': {'execution': {'fresh_call': True, 'resumed': True, 'retried': False,
                                                                                    'route_a_completed_normally': True, 'run_root': K_.call_dir + '/out'}}}}),
       lambda v: 'FRESH_COMPLETED_NO_RESUME_NO_RETRY' in json.dumps(by_name(v[0], v[1])['A0']['blockers']), 'FRESH_COMPLETED_NO_RESUME_NO_RETRY_CALL_NOT_ESTABLISHED')
    foreign = W.fx.raw('shared/foreign_source.bin', b'foreign')
    def foreign_src(K_):
        src = W.fx.json(K_.tag + '/inputs/foreign_source.json', {'schema': 'UNT_POINT_SOURCE_RECONSTRUCTION_CX2V001',
                                                                 'source_files': [foreign], 'status': 'TESTED', 'verdict': 'PASS'})
        return {'R0': {'source_reconstruction': src}}
    MF('L16_cross_run_source_refused', 'own-run sources only (v004 L67-69)', lambda: scenario('L16', inp_kw={'overrides': foreign_src}),
       lambda v: 'CROSS_RUN_SOURCE_SUBSTITUTION_FORBIDDEN' in json.dumps(by_name(v[0], v[1])['R0']['blockers']), 'CROSS_RUN_SOURCE_SUBSTITUTION_FORBIDDEN')
    forged = dict(W.read_pin(slot_pin_c), covers_all_consumed_states=True)
    fpin = W.fx.json(Pc.tag + '/forged_slot_for_state_adapter.json', forged)
    fb_pin = W.fx.json(Pc.tag + '/bundle_forged_slot.json', bundle(W, Pc, fpin))
    MF('L17_slot_proof_with_covers_all_refused', 'covers_all_consumed_states refused at acceptance too',
       lambda: run_state(W, Pc, K, inp, bundle_pin=fb_pin),
       lambda v: 'LO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES' in json.dumps(v['blockers']) and v['call_lo_reading'] == 'INCOMPLETE',
       'LO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES')
    MF('L17b_slot_proof_producer_not_approved', 'approved slot producer', lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_c,
                                                                                          approved=[W.shas['state']]),
       lambda v: 'LO_SLOT_PROOF_PRODUCER_NOT_APPROVED' in json.dumps(v['blockers']), 'LO_SLOT_PROOF_PRODUCER_NOT_APPROVED')
    MF('L17c_adapter_not_approved', 'approved adapter only', lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_c, approved=[W.shas['slot']]),
       lambda v: 'LO_STATE_ADAPTER_NOT_APPROVED' in json.dumps(v['blockers']), 'LO_STATE_ADAPTER_NOT_APPROVED')
    MF('L18_config_validation_failure_unavailable', 'lo_config validate_current_config (6654d93c)',
       lambda: scenario('L18', inp_kw={'overrides': lambda K_: {'A1': {'synthetic_validate_fail': True}}}),
       lambda v: 'actual state certificate slot mismatch' in json.dumps(by_name(v[0], v[1])['A1']['blockers']), 'UNAVAILABLE')
    MF('L19_core_producer_not_unchanged_refused', 'UNCHANGED core only',
       lambda: scenario('L19', inp_kw={'overrides': lambda K_: {'A1': {'synthetic_core_producer': W.pin['lo_config']}}}),
       lambda v: 'CORE_PRODUCER_NOT_UNCHANGED_12D36305' in json.dumps(by_name(v[0], v[1])['A1']['blockers']), 'CORE_PRODUCER_NOT_UNCHANGED_12D36305_A1DCDEA8')
    MF('L19b_core_state_mismatch_refused', 'core record for this state', lambda: scenario('L19b', inp_kw={'overrides': lambda K_: {
        'A2': {'synthetic_core_state': K_.st['A0']}}}),
       lambda v: 'CORE_RECORD_SHAPE_OR_STATE_MISMATCH' in json.dumps(by_name(v[0], v[1])['A2']['blockers']), 'CORE_RECORD_SHAPE_OR_STATE_MISMATCH')
    MF('L21_bundle_of_another_point_refused', 'registered bundle of THIS point', lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_a),
       lambda v: 'BUNDLE_POINT_OR_CUSTODY_MISMATCH' in json.dumps(v['blockers']), 'BUNDLE_POINT_OR_CUSTODY_MISMATCH')
    MP('L22_call_record_carries_thread_env_and_policy', 'diagnostics recorded (rho bitwise depends on single-thread BLAS)',
       lambda: {k: rec.get(k) for k in ('blas_thread_env', 'speed_reference_policy', 'readout_set', 'lo_slot', 'call_result')},
       lambda v: isinstance(v['blas_thread_env'], dict) and v['speed_reference_policy'] == W.STATE.SPEED_POLICY
       and v['lo_slot'] == Pc.rho_pin and v['call_result'] == K.result_pin, 'recorded')
    def respelled(K_):
        rp = dict(K_.result_pin, path=K_.result_pin['path'].replace('/call/out/', '/call/./out/'))
        return {'A1': {'call_result': rp}}
    MP('L23_same_result_file_other_spelling_accepted', 'own-call binding by sha + resolved path (v010 same_ref)',
       lambda: scenario('L23', inp_kw={'overrides': respelled}), lambda v: v[1]['call_lo_reading'] == 'PASS', 'PASS')
    stale = copy.deepcopy(K.result); stale['passes'][0]['rows'][0]['speed_km_s'] = 99.0
    MF('L20_supplied_result_differs_from_bytes', 'call result from bytes', lambda: run_state(W, Pc, K, inp, bundle_pin=bundle_pin_c, result=stale),
       lambda v: 'CALL_RESULT_BYTES_DIFFER_FROM_SUPPLIED_RESULT' in json.dumps(v['blockers']), 'CALL_RESULT_BYTES_DIFFER_FROM_SUPPLIED_RESULT')
    return rec


def tests_srb(W, A, Pc, pair, registered, bundle_pin_c):
    U = W.LIB
    N = 2
    edges = np.arange(4.0, 183.0)

    def tail_state(tag, *, B=None, eps_pin=None, lo_pin=None, kind='le_rotation', source='synthetic-source'):
        if B is None:
            B = np.zeros((178, 3))
            B[:, 1] = [1e-30 / (1.0 + k) for k in range(178)]
        rec = {'schema': 'UNT_UV_TAIL_STATE_C2V001', 'stage_kind': kind, 'roster_digest': sha_bytes((tag + source).encode()),
               'eps_certificate': eps_pin or Pc.eps_pin, 'lo_certificate': lo_pin or Pc.rho_pin, 'c_m_s': 299792458.0,
               'empty': False, 'synthetic_fixture': SYN}
        arrays = {'shell_edges_inverse_kpc': edges.copy(), 'shell_integrals': B}
        st = U.TailState(empty=False, record=rec, arrays=arrays)
        rp = W.fx.json('srb/' + tag + '/tail_record.json', rec)
        rec_loaded = W.read_pin(rp)
        if U.TailState(empty=False, record=rec_loaded, arrays=arrays).digest != st.digest:
            raise ValueError('synthetic record does not round-trip')
        ap = W.fx.npz('srb/' + tag + '/tail_arrays.npz', arrays)
        state = {'state_sha256': st.digest, 'source_sha256': rec['roster_digest'], 'stage_kind': kind, 'nonnegative_masses': True}
        return state, rp, ap, st

    def setup(tag, *, flagged=False, B=None, rows_over=None, tau=None, eps_pin=None, ra=None, state_over=None):
        P = Pc
        state, rp, ap, st = tail_state(tag, B=B, eps_pin=eps_pin)
        K = make_call(W, P, 'srb_' + tag, final_pass=N, flagged=flagged, route_a_record=ra, rot_state=state)
        sin = {'schema': 'UNT_POINT_LO_STATE_INPUT_CX2V001', 'identity': P.details['identity'], 'custody': P.details['custody'],
               'state': state_over(K) if state_over else state, 'tail_state': {'record': rp, 'arrays': ap},
               'call_result': K.result_pin}
        sin_pin = W.fx.json('srb/' + tag + '/state_input.json', sin)
        if W.src_producer is None:
            state_inputs(W, P, make_call(W, P, 'srb_bootstrap'))
        n_cols = 4
        rows = {'schema': 'S4RC1_SRB_ROT_ROWS_INPUT_C3V001', 'state': state, 'call_result': K.result_pin,
                'producer': W.src_producer, 'row_ids': [r['id'] for r in P.details['row_contract']['rows']],
                'row_contract_sha256': P.details['custody']['row_contract_sha256'],
                'tau_km_s': tau or P.details['row_contract']['tau_km_s'],
                'column_R_m': [(1.0 + c) * KPC for c in range(n_cols)], 'v_c_m_s': [4.0e4 + 1e3 * c for c in range(n_cols)],
                'row_columns': [[i % n_cols] for i in range(12)], 'N_min': 0.999, 'provenance': 'synthetic'}
        rows.update(rows_over or {})
        rows_pin = W.fx.json('srb/' + tag + '/rows_input.json', rows)
        return K, sin_pin, rows_pin, state, st

    def run(K, sin_pin, rows_pin, *, env=None, approved=None):
        return W.SRB._adapt(Pc.spec, call_dir=K.call_dir, result=K.result, inventory=K.inventory, bundle_ref=bundle_pin_c,
                            state_input_ref=sin_pin, rows_input_ref=rows_pin, root_ruling_refs=W.rulings,
                            approved_producer_sha256=W.approved if approved is None else approved,
                            trusted_source_producers=[W.src_producer['sha256']], env=env or W.srb_env())
    K, s, r, state, st = setup('R01')
    # ---- c3v003 V02 (A138 item 2): the SRB adapter's inventory enumerator is the b1 enumerator 4ca7f364. These two
    # cases run first, on the R01 call, so a mutant that breaks the later SRB cases cannot hide them.
    inv010 = copy.deepcopy(K.inventory)
    inv010['producer'] = W.pin['enumerator_v010']

    def run_inv(inv):
        return W.SRB._adapt(Pc.spec, call_dir=K.call_dir, result=K.result, inventory=inv, bundle_ref=bundle_pin_c,
                            state_input_ref=s, rows_input_ref=r, root_ruling_refs=W.rulings,
                            approved_producer_sha256=W.approved, trusted_source_producers=[W.src_producer['sha256']],
                            env=W.srb_env())
    MF('R17_V02_srb_v010_inventory_refused', 'V02 a v010 inventory is refused (SRB adapter, A138)', lambda: run_inv(inv010),
       lambda v: v['verdict'] == 'UNAVAILABLE' and v['proof'] is None
       and 'INVENTORY_PRODUCER_NOT_B1_4CA7F364' in json.dumps(v['blockers']), 'UNAVAILABLE INVENTORY_PRODUCER_NOT_B1_4CA7F364')
    MP('R17b_V02_srb_b1_inventory_accepted', 'V02 a b1 inventory is accepted (SRB adapter, A138)',
       lambda: (run_inv(K.inventory), K.inventory['producer']),
       lambda v: v[0]['verdict'] == 'PASS' and v[0]['proof'] is not None and v[1] == W.pin['enumerator']
       and v[1]['sha256'] == B1_ENUM_SHA, 'PASS on the R01 call with the b1 inventory (producer 4ca7f364)')
    res = MP('R01_srb_rot_pass', 'library srb_rot on the accepted final-rotation state', lambda: run(K, s, r),
             lambda v: v['verdict'] == 'PASS' and v['amb04_status'] == 'PASS' and v['reading'] == 'PASS'
             and v['proof'] is not None and v['proof']['gate'] == 'SRB_ROT' and v['stage'] == 'le2_rotation', 'PASS; SRB_ROT proof')
    def manual():
        eps_cert = W.SRB.format_eps(W.read_pin(Pc.eps_pin), Pc.details)
        fb_ = U.field_bound(st, eps_cert)
        rows = W.SRB.format_rows(W.read_pin(r), Pc.details, state, K.result_pin, [W.src_producer['sha256']])
        sr = U.srb_rot(st, eps_cert, rows)
        return {'lib': sr['bound_km_s'], 'adapter': res['bound_km_s'], 'eps_keys': sorted(eps_cert['shells'][0]),
                'n': len(eps_cert['shells']), 'first': eps_cert['shells'][0], 'last': eps_cert['shells'][-1]}
    MP('R01b_adapter_equals_direct_library_call', 'thin format adapter (no other arithmetic)', manual,
       lambda v: v['lib'] == v['adapter'] and v['eps_keys'] == ['eps', 'hi_inverse_kpc', 'lo_inverse_kpc'] and v['n'] == 178
       and v['first']['lo_inverse_kpc'] == 4.0 and v['last']['hi_inverse_kpc'] == 182.0, 'identical bound; 178 unit shells 4->182')
    # R02: final-rotation state only.
    K2, s2, r2, st2, _ = setup('R02', state_over=lambda K_: K_.st['L1R'])
    MF('R02_non_final_rotation_state_refused', 'final-rotation state only', lambda: run(K2, s2, r2),
       lambda v: v['verdict'] == 'UNAVAILABLE' and 'SRB_ROT_FINAL_ROTATION_STATE_ONLY' in json.dumps(v['blockers']), 'SRB_ROT_FINAL_ROTATION_STATE_ONLY')
    K2b, s2b, r2b, _, _ = setup('R02b', state_over=lambda K_: K_.st['A1'])
    MF('R02b_route_a_state_refused', 'final-rotation state only', lambda: run(K2b, s2b, r2b),
       lambda v: 'SRB_ROT_FINAL_ROTATION_STATE_ONLY' in json.dumps(v['blockers']), 'SRB_ROT_FINAL_ROTATION_STATE_ONLY')
    MP('R02c_final_rotation_selection', 'le{final_pass}_rotation own_source_state', lambda: W.SRB.final_rotation_state(K.inventory, K.result),
       lambda v: v[0] == state and v[1] == 'le2_rotation', 'le2_rotation state')
    # R03: eps is the larger value; eps_envelope never fed.
    def eps_variant(tag, **kw):
        rec = W.eps_record(Pc.details, **kw)
        return W.fx.json('srb/eps_' + tag + '.json', rec), rec
    p_env_hi, _ = eps_variant('env_above', env_fn=lambda k: 2e-4 + 1e-6 * k)
    MF('R03_eps_below_envelope_refused', 'eps field is the larger value (guard L139)',
       lambda: W.SRB.format_eps(W.read_pin(p_env_hi), Pc.details), lambda v: 'EPS_FIELD_NOT_THE_LARGER_VALUE' in json.dumps(v), 'EPS_FIELD_NOT_THE_LARGER_VALUE')
    p_env_lo, _ = eps_variant('env_low', env_fn=lambda k: 1e-9)
    MP('R03b_eps_envelope_never_used', 'only eps enters', lambda: [W.SRB.format_eps(W.read_pin(p), Pc.details) for p in (Pc.eps_pin, p_env_lo)],
       lambda v: v[0] == v[1], 'identical library input when only eps_envelope differs')
    p_short, _ = eps_variant('short', hi=181)
    MF('R04_eps_coverage_short_refused', 'eps over [4,182]', lambda: W.SRB.format_eps(W.read_pin(p_short), Pc.details),
       lambda v: 'EPS_COVERAGE_NOT_4_TO_182' in json.dumps(v) or 'EPS_SHELLS_NOT' in json.dumps(v), 'EPS_COVERAGE_NOT_4_TO_182')
    p_gap, _ = eps_variant('gap', skip=(100,))
    MF('R04b_eps_gap_refused', 'eps over [4,182], no gap', lambda: W.SRB.format_eps(W.read_pin(p_gap), Pc.details),
       lambda v: 'EPS_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS_FROM_4' in json.dumps(v), 'EPS_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS_FROM_4')
    p_other_pt = W.fx.json('srb/eps_other_point.json', W.eps_record(A.details))
    MF('R04c_eps_record_other_point_refused', 'the point\'s own EPS record', lambda: W.SRB.format_eps(W.read_pin(p_other_pt), Pc.details),
       lambda v: 'EPS_RECORD_POINT_CUSTODY_MISMATCH' in json.dumps(v), 'EPS_RECORD_POINT_CUSTODY_MISMATCH')
    Ke, se, re_, _, _ = setup('R04d', eps_pin=p_env_lo)
    MF('R04d_state_ran_with_other_eps_refused', 'EPS record the call ran with', lambda: run(Ke, se, re_),
       lambda v: 'TAIL_STATE_DID_NOT_RUN_WITH_THESE_CERTIFICATE_SLOTS' in json.dumps(v['blockers']), 'TAIL_STATE_DID_NOT_RUN_WITH_THESE_CERTIFICATE_SLOTS')
    # R05: the tau/10 rule at the exact boundary (library comparison).
    base = res['bound_km_s']
    def tau_for(bound):
        t0 = bound * 10.0
        cands, up, dn = [t0], t0, t0
        for _ in range(8):
            up, dn = nextup(up), nextdown(dn)
            cands += [up, dn]
        for t in cands:
            if t / 10 == bound:
                return t
        return None
    exact = [tau_for(b) for b in base]
    tau_ok = exact[0] is not None
    taus = [t if t is not None else b * 1000.0 for t, b in zip(exact, base)]
    det = W.DETAILS[Pc.tag]
    def with_tau(tag, tvec):
        d2 = copy.deepcopy(det)
        d2['row_contract']['tau_km_s'] = tvec
        d2['custody']['row_contract_sha256'] = W.C.digest(d2['row_contract'])
        d2['custody_sha256'] = W.C.digest(d2['custody'])
        return d2
    # The row contract change alters custody, so the R05 cases run with a patched derive_details for the SRB env only;
    # every custody-bound record (inventory, EPS record and proof, state input, rows input) is re-derived from it.
    def boundary_case(tag, tvec):
        d2 = with_tau(tag, tvec)
        spec = copy.deepcopy(Pc.spec); spec['label'] = tag
        W.DETAILS[tag] = d2
        eps_rec = W.eps_record(d2); eps_pin = W.fx.json('srb/' + tag + '/eps.json', eps_rec)
        rho_rec = W.rho_record(d2, DEFAULT_RHOS); rho_pin = W.fx.json('srb/' + tag + '/rho.json', rho_rec)
        spec['numerics']['uv_tail']['eps_certificate'] = eps_pin; spec['numerics']['uv_tail']['lo_certificate'] = rho_pin
        epr = W.fx.json('srb/' + tag + '/eps_proof.json', W.eps_proof(d2, eps_pin, eps_rec))
        bpin = W.fx.json('srb/' + tag + '/bundle.json', {'identity': d2['identity'], 'custody': d2['custody'],
                                                          'driver_certificate_bindings': {'eps_certificate': eps_pin, 'lo_certificate': rho_pin},
                                                          'prelaunch': {'EPS': epr}})
        state2, rp2, ap2, st2_ = tail_state(tag, eps_pin=eps_pin, lo_pin=rho_pin)
        P2 = copy.copy(Pc); P2.details = d2; P2.tag = Pc.tag + '_' + tag
        K_ = make_call(W, P2, 'srb_' + tag, final_pass=N, rot_state=state2)
        sin_ = W.fx.json('srb/' + tag + '/state_input.json', {'schema': 'UNT_POINT_LO_STATE_INPUT_CX2V001', 'identity': d2['identity'],
                                                             'custody': d2['custody'], 'state': state2,
                                                             'tail_state': {'record': rp2, 'arrays': ap2}, 'call_result': K_.result_pin})
        rows_ = W.fx.json('srb/' + tag + '/rows.json', {'schema': 'S4RC1_SRB_ROT_ROWS_INPUT_C3V001', 'state': state2,
                                                       'call_result': K_.result_pin, 'producer': W.src_producer,
                                                       'row_ids': [x['id'] for x in d2['row_contract']['rows']],
                                                       'row_contract_sha256': d2['custody']['row_contract_sha256'], 'tau_km_s': tvec,
                                                       'column_R_m': [(1.0 + c) * KPC for c in range(4)],
                                                       'v_c_m_s': [4.0e4 + 1e3 * c for c in range(4)],
                                                       'row_columns': [[i % 4] for i in range(12)], 'N_min': 0.999})
        return W.SRB._adapt(spec, call_dir=K_.call_dir, result=K_.result, inventory=K_.inventory, bundle_ref=bpin,
                            state_input_ref=sin_, rows_input_ref=rows_, root_ruling_refs=W.rulings,
                            approved_producer_sha256=W.approved, trusted_source_producers=[W.src_producer['sha256']], env=W.srb_env())
    if tau_ok:
        MP('R05_bound_equal_tau_over_10_passes', 'V007 frozen <= tau_i/10 (library)', lambda: boundary_case('R05eq', taus),
           lambda v: v['verdict'] == 'PASS' and v['pass_tau_over_10'] is True, 'PASS at bound == tau/10')
        down = [nextdown(t) if i == 0 else t for i, t in enumerate(taus)]
        MF('R05b_bound_one_ulp_above_tau_over_10_fails', 'V007 frozen <= tau_i/10 (library)', lambda: boundary_case('R05up', down),
           lambda v: v['verdict'] == 'FAIL' and v['reading'] == 'BOUND_INSUFFICIENT', 'FAIL -> BOUND_INSUFFICIENT')
    else:
        record('R05_bound_equal_tau_over_10_passes', 'MUST_PASS', 'V007 frozen <= tau_i/10', False, 'boundary tau found', taus)
    # R06: AMB-04 outcomes (r14 apply_flag).
    bigB = np.zeros((178, 3)); bigB[:, 1] = 1e-14
    cases = (('R06a_unflagged_pass', False, None, 'PASS', 'PASS', 'PASS'),
             ('R06b_flagged_pass', True, None, 'PASS', 'PASS_FLAGGED', 'PASS_FLAGGED'),
             ('R06c_flagged_fail', True, bigB, 'UNDECIDABLE_FLAGGED', 'UNDECIDABLE_FLAGGED', 'UNDECIDABLE_FLAGGED'),
             ('R06d_unflagged_fail', False, bigB, 'FAIL', 'FAIL', 'BOUND_INSUFFICIENT'))
    for cid, flag, B, verdict, amb, reading in cases:
        Kc, sc, rc, _, _ = setup(cid, flagged=flag, B=B)
        fn = MP if verdict == 'PASS' else MF
        fn(cid, 'AMB-04 exactly as r14 L4617 apply_flag', lambda Kc=Kc, sc=sc, rc=rc: run(Kc, sc, rc),
           lambda v, verdict=verdict, amb=amb, reading=reading: v['verdict'] == verdict and v['amb04_status'] == amb
           and v['reading'] == reading and ((v['proof'] is not None) == (verdict == 'PASS')),
           '%s / %s / %s' % (verdict, amb, reading))
    Ki, si, ri, _, _ = setup('R07', ra={'flags': ['TAIL_SOURCE_UNDERCONVERGED'], 'monitor_status': 'M_T_WITHIN_THRESHOLD'})
    MF('R07_inconsistent_flag_record_unavailable', 'the call\'s own flag record', lambda: run(Ki, si, ri),
       lambda v: v['verdict'] == 'UNAVAILABLE' and 'ROUTE_A_FLAG_RECORD_INCONSISTENT' in json.dumps(v['blockers']), 'ROUTE_A_FLAG_RECORD_INCONSISTENT')
    def apply_flag_identity():
        raw = open(REAL['r14'][0], 'rb').read()
        f = W.SRB.extract_apply_flag(raw)
        outs = [f({'status': s}, fl) for s, fl in (('PASS', []), ('PASS', ['C']), ('FAIL', ['C']), ('FAIL', []), ('NOT_READ', ['C']))]
        return [o['status'] for o in outs] + [f.__code__.co_filename, f.__code__.co_firstlineno]
    MP('R08_apply_flag_is_r14_L4099', 'apply_flag extracted from r14 f3f9ba7e', apply_flag_identity,
       lambda v: v == ['PASS', 'PASS_FLAGGED', 'UNDECIDABLE_FLAGGED', 'FAIL', 'NOT_READ', REAL['r14'][0], 4099], 'r14 mapping')
    tampered = open(REAL['r14'][0], 'rb').read().replace(b"out['status'] = 'PASS_FLAGGED'", b"out['status'] = 'PASS'", 1)
    v = raises(lambda: W.SRB.extract_apply_flag(tampered), 'R14_BYTES_NOT_F3F9BA7E')
    record('R08b_tampered_r14_refused', 'MUST_FAIL', 'apply_flag only from the pinned r14 bytes', v['match'], 'R14_BYTES_NOT_F3F9BA7E', v)
    # R09: no bare EPS magnitude gate: corner-sized eps passes when the bound is small.
    big_eps, _ = eps_variant('corner_sized', eps_fn=lambda k: 0.0125, env_fn=lambda k: 0.0125)
    MP('R09_no_bare_eps_magnitude_gate', 'no EPS magnitude gate', lambda: W.SRB.format_eps(W.read_pin(big_eps), Pc.details)['shells'][0]['eps'],
       lambda v: v == 0.0125, 'eps 0.0125 accepted by the format adapter (only the bound is gated)')
    # R10-R12: rows and state custody.
    Kr, sr_, rr_, _, _ = setup('R10', rows_over={'tau_km_s': [5.0] * 12})
    MF('R10_rows_tau_not_row_contract_refused', 'tau_i = 0.25 sigma_i via the row contract', lambda: run(Kr, sr_, rr_),
       lambda v: 'SRB_ROWS_INPUT_TAU_NOT_ROW_CONTRACT_TAU' in json.dumps(v['blockers']), 'SRB_ROWS_INPUT_TAU_NOT_ROW_CONTRACT_TAU')
    Kr2, sr2, rr2, _, _ = setup('R10b', rows_over={'row_columns': [[9]] * 12})
    MF('R10b_rows_column_index_out_of_range_refused', 'rows shape', lambda: run(Kr2, sr2, rr2),
       lambda v: 'SRB_ROWS_INPUT_ROW_COLUMNS_INVALID' in json.dumps(v['blockers']), 'SRB_ROWS_INPUT_ROW_COLUMNS_INVALID')
    Kr3, sr3, rr3, _, _ = setup('R10c', rows_over={'N_min': 0.0})
    MF('R10c_rows_N_min_not_positive_refused', 'rows values', lambda: run(Kr3, sr3, rr3),
       lambda v: 'SRB_ROWS_INPUT_N_MIN_NOT_POSITIVE' in json.dumps(v['blockers']), 'SRB_ROWS_INPUT_N_MIN_NOT_POSITIVE')
    Kr4, sr4, rr4, _, _ = setup('R10d', rows_over={'call_result': Kr3.result_pin})
    MF('R10d_rows_from_another_call_refused', 'the call\'s own rows', lambda: run(Kr4, sr4, rr4),
       lambda v: 'SRB_ROWS_INPUT_NOT_THIS_CALL' in json.dumps(v['blockers']), 'SRB_ROWS_INPUT_NOT_THIS_CALL')
    def tampered_arrays():
        state_, rp_, ap_, st_ = tail_state('R11')
        Kt = make_call(W, Pc, 'srb_R11', final_pass=N, rot_state=state_)
        B2 = np.zeros((178, 3)); B2[:, 1] = 2e-30
        ap2 = W.fx.npz('srb/R11/tail_arrays_tampered.npz', {'shell_edges_inverse_kpc': edges.copy(), 'shell_integrals': B2})
        sin_ = W.fx.json('srb/R11/state_input.json', {'schema': 'UNT_POINT_LO_STATE_INPUT_CX2V001', 'identity': Pc.details['identity'],
                                                     'custody': Pc.details['custody'], 'state': state_,
                                                     'tail_state': {'record': rp_, 'arrays': ap2}, 'call_result': Kt.result_pin})
        rows_ = W.fx.json('srb/R11/rows.json', dict(W.read_pin(r), state=state_, call_result=Kt.result_pin))
        return run(Kt, sin_, rows_)
    MF('R11_state_digest_mismatch_refused', 'state digest from the library', tampered_arrays,
       lambda v: 'UV_TAIL_STATE_DIGEST_MISMATCH' in json.dumps(v['blockers']), 'UV_TAIL_STATE_DIGEST_MISMATCH')
    def other_bundle():
        return W.SRB._adapt(Pc.spec, call_dir=K.call_dir, result=K.result, inventory=K.inventory, bundle_ref=W._anchor_bundle,
                            state_input_ref=s, rows_input_ref=r, root_ruling_refs=W.rulings, approved_producer_sha256=W.approved,
                            trusted_source_producers=[W.src_producer['sha256']], env=W.srb_env())
    MF('R12b_bundle_of_another_point_refused', 'the point\'s own registered bundle', other_bundle,
       lambda v: 'BUNDLE_POINT_OR_CUSTODY_MISMATCH' in json.dumps(v['blockers']), 'BUNDLE_POINT_OR_CUSTODY_MISMATCH')
    MF('R12_srb_adapter_not_approved', 'approved adapter only', lambda: run(K, s, r, approved=[W.shas['slot']]),
       lambda v: 'SRB_ROT_ADAPTER_NOT_APPROVED' in json.dumps(v['blockers']), 'SRB_ROT_ADAPTER_NOT_APPROVED')
    MP('R13_rb_fp_screen_not_a_gate', 'RB-FP(p) optional, never a gate', lambda: res['rb_fp_screen'],
       lambda v: v.startswith('NOT_COMPUTED_IN_C3V001') and 'never a gate' in v, 'NOT_COMPUTED; never a gate')
    d = W.fx.dir('srb/R01_out')
    MP('R14_writer_outputs', 'exclusive-create proof and result', lambda: W.SRB.write_outputs(res, d),
       lambda v: v['proof'] is not None and v['result'] is not None, 'two pins')
    v = raises(lambda: W.SRB.write_outputs(res, d), 'File exists')
    record('R14b_writer_second_write_refused', 'MUST_FAIL', 'exclusive create', v['match'] or 'FileExistsError' in str(v['raised']),
           'FileExistsError', v)

    # ---- c3v002 F8: M_T_NOT_NORMALIZED with flags [] reads unflagged (r14 raw_flag L4587-4590); other statuses UNAVAILABLE.
    ctrl = open(REAL['route_a_controller'][0], 'rb').read().decode('utf-8').split('\n')
    MP('R15_F8_controller_emits_mt_not_normalized_with_flags_empty', 'F8 r14 raw_flag reading (source fact)',
       lambda: [ctrl[530].strip(), ctrl[533].strip(), ctrl[534].strip()],
       lambda v: v == ['flags = []', "if accepted['M_T'] is None:", "status = 'M_T_NOT_NORMALIZED'"],
       'controller c2v001 L531, L534-535')
    Kn, sn, rn, _, _ = setup('R15b', ra={'flags': [], 'monitor_status': 'M_T_NOT_NORMALIZED'})
    MP('R15b_F8_mt_not_normalized_flags_empty_unflagged_pass', 'F8 M_T_NOT_NORMALIZED with flags [] reads UNFLAGGED',
       lambda: run(Kn, sn, rn), lambda v: v['verdict'] == 'PASS' and v['amb04_status'] == 'PASS' and v['flagged'] is False
       and v['proof'] is not None, 'PASS, unflagged, SRB_ROT proof')
    Kf, sf, rf, _, _ = setup('R15c', B=bigB, ra={'flags': [], 'monitor_status': 'M_T_NOT_NORMALIZED'})
    MF('R15c_F8_mt_not_normalized_unflagged_fail_bound_insufficient', 'F8 M_T_NOT_NORMALIZED with flags [] reads UNFLAGGED',
       lambda: run(Kf, sf, rf), lambda v: v['verdict'] == 'FAIL' and v['reading'] == 'BOUND_INSUFFICIENT' and v['flagged'] is False,
       'FAIL -> BOUND_INSUFFICIENT (an unflagged fail, as r14 reads it)')
    for cid, ra, code in (('R15d_F8_mt_not_normalized_with_tsu_flag_unavailable',
                           {'flags': ['TAIL_SOURCE_UNDERCONVERGED'], 'monitor_status': 'M_T_NOT_NORMALIZED'}, 'ROUTE_A_FLAG_RECORD_INCONSISTENT'),
                          ('R15e_F8_mt_not_normalized_with_other_flag_unavailable',
                           {'flags': ['SOMETHING_ELSE'], 'monitor_status': 'M_T_NOT_NORMALIZED'}, 'ROUTE_A_FLAG_RECORD_INCONSISTENT'),
                          ('R15f_F8_other_status_still_unavailable', {'flags': [], 'monitor_status': 'NO_ACCEPTED_ITERATION'},
                           'ROUTE_A_FLAG_RECORD_INCONSISTENT'),
                          ('R15g_F8_flagged_status_without_tsu_still_unavailable', {'flags': [], 'monitor_status': 'FLAGGED'},
                           'ROUTE_A_FLAG_RECORD_INCONSISTENT')):
        Kx_, sx_, rx_, _, _ = setup(cid[:4], ra=ra)
        MF(cid, 'F8 any other status stays UNAVAILABLE; FLAGGED <-> TAIL_SOURCE_UNDERCONVERGED kept',
           lambda Kx_=Kx_, sx_=sx_, rx_=rx_: run(Kx_, sx_, rx_),
           lambda v, code=code: v['verdict'] == 'UNAVAILABLE' and code in json.dumps(v['blockers']), code)


# ------------------------------------------------------------------------------------------------ c3v002 additions
def require_synthetic(path):
    """F11: every suite output goes under <suite dir>/synthetic/ (lexical and realpath check of the nearest parent)."""
    p = os.path.abspath(path)
    q = p
    while not os.path.exists(q):
        q = os.path.dirname(q)
    real = os.path.join(os.path.realpath(q), os.path.relpath(p, q))
    for x in (p, real):
        if not (x + '/').startswith(SYNTHETIC_DIR + '/') or x == SYNTHETIC_DIR:
            raise ValueError('REFUSED: F11 suite outputs must be under ' + SYNTHETIC_DIR + '/: ' + path)
    return p


def snapshot_tree(top, skip=()):
    out = []
    for d, dirs, files in os.walk(top):
        dirs[:] = sorted(x for x in dirs if os.path.join(d, x) not in skip)
        for n in sorted(files):
            p = os.path.join(d, n)
            if p in skip:
                continue
            st = os.lstat(p)
            out.append((os.path.relpath(p, top), st.st_size, st.st_mtime_ns))
    return out


def hashed_snapshot(top, hashes_name):
    """c3v003 hygiene: (name, size, mtime) of every file the folder's own HASHES file lists, plus that HASHES file."""
    out = []
    with open(os.path.join(top, hashes_name), encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or '  ' not in line:
                continue
            rel = line.rstrip('\n').split('  ', 1)[1]
            st = os.lstat(os.path.join(top, rel))
            out.append((rel, st.st_size, st.st_mtime_ns))
    st = os.lstat(os.path.join(top, hashes_name))
    return out + [(hashes_name, st.st_size, st.st_mtime_ns)]


def scen(W, tag, *, P, bundle_pin, call_kw=None, inp_kw=None, run_kw=None):
    K_ = make_call(W, P, tag, **(call_kw or {}))
    kw = dict(inp_kw or {})
    for k in ('b1', 'overrides', 'row_over'):
        if callable(kw.get(k)):
            kw[k] = kw[k](K_)
    inp_ = state_inputs(W, P, K_, **kw)
    r_ = run_state(W, P, K_, inp_, bundle_pin=bundle_pin, **(run_kw or {}))
    return K_, r_


def tests_c3v002(W, A, Pc, pair, registered, slot_pin_c, bundle_pin_c, rec_l01, K_l01):
    fb = lambda names: (lambda K_: {n: unit_b1(fail_shell=True) for n in names})
    # ---- F3: lo_config certificate_slots_bound honoured, exactly as lo_config L85-90 (after the core).
    MF('L24_F3_unbound_certificate_slots_state_unavailable', 'F3 certificate_slots_bound honoured (lo_config L85-90)',
       lambda: scen(W, 'L24', P=Pc, bundle_pin=bundle_pin_c,
                    inp_kw={'overrides': lambda K_: {'A1': {'synthetic_validate_unbound': True}}}),
       lambda v: (lambda s: s['verdict'] == 'UNAVAILABLE' and 'ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND' in json.dumps(s['blockers'])
                  and s['core_record'] is not None and s['record'] is not None)(by_name(v[0], v[1])['A1'])
       and v[1]['call_lo_reading'] == 'INCOMPLETE'
       and all(s['verdict'] == 'PASS' for n, s in by_name(v[0], v[1]).items() if n != 'A1'),
       'A1 UNAVAILABLE ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND (core record kept); the others PASS; call INCOMPLETE')
    MF('L24b_F3_unbound_plus_threshold_miss_is_unavailable_not_fail', 'F3 certificate_slots_bound honoured (lo_config L85-90)',
       lambda: scen(W, 'L24b', P=Pc, bundle_pin=bundle_pin_c,
                    inp_kw={'b1': fb(['A1']), 'overrides': lambda K_: {'A1': {'synthetic_validate_unbound': True}}}),
       lambda v: (lambda s: s['verdict'] == 'UNAVAILABLE' and s.get('threshold_failed_observation') is True
                  and 'ACTUAL_POINT_CERTIFICATE_SLOTS_UNBOUND' in json.dumps(s['blockers']))(by_name(v[0], v[1])['A1'])
       and v[1]['call_lo_reading'] == 'INCOMPLETE',
       'UNAVAILABLE (never FAIL) with the threshold observation recorded; call INCOMPLETE, not NON_LAPSE_TAIL_MATERIAL')
    MP('L24c_F3_bound_slots_recorded_on_pass_states', 'F3 certificate_slots_bound honoured (control)',
       lambda: [s.get('state_configuration_validation', {}).get('certificate_slots_bound') for s in rec_l01['states']],
       lambda v: len(v) == len(K_l01.inventory['states']) and all(x is True for x in v), 'every PASS state recorded bound True')
    # ---- F4: common Refusal and writer refusals give a structured result.
    def writer_refusal():
        K_ = make_call(W, Pc, 'L25')
        inp_ = state_inputs(W, Pc, K_)
        bad_out = os.path.join(W.fx.root, Pc.tag, 'L25', 'uvt_lo_out')
        r_ = W.STATE._adapt_call(Pc.spec, call_dir=K_.call_dir, result=K_.result, inventory=K_.inventory,
                                 bundle_ref=bundle_pin_c, state_inputs=inp_, root_ruling_refs=W.rulings,
                                 approved_producer_sha256=W.approved, trusted_source_producers=[W.src_producer['sha256']],
                                 trusted_row_policy_review_sha256=W.review_shas, out_root=bad_out, env=W.state_env())
        return {'rec': r_, 'created': os.path.exists(bad_out)}
    MF('L25_F4_writer_policy_refusal_is_a_structured_incomplete', 'F4 common Refusal and writer refusals caught (never a crash)',
       writer_refusal, lambda v: isinstance(v.get('rec'), dict) and v['rec']['call_lo_reading'] == 'INCOMPLETE' and not v['created']
       and bool(v['rec']['states']) and all(s['verdict'] == 'UNAVAILABLE' and 'UVT_COMPONENT_REFUSED' in json.dumps(s['blockers'])
                                            for s in v['rec']['states']),
       'a call record (no exception): INCOMPLETE, every state UNAVAILABLE with UVT_COMPONENT_REFUSED, nothing created')

    def boom(ref):
        raise W.C.Refusal('SYNTHETIC_COMMON_REFUSAL_FROM_A_READER')
    MF('S18_F4_slot_common_refusal_structured_blocked', 'F4 common Refusal and writer refusals caught (never a crash)',
       lambda: slot_prove(W, Pc, pair, registered, env=W.slot_env(read_pin=boom)),
       lambda v: v.get('verdict') == 'BLOCKED' and v.get('proof') is None
       and 'SYNTHETIC_COMMON_REFUSAL_FROM_A_READER' in json.dumps(v['blockers']), 'BLOCKED with the common refusal recorded')
    K16 = W._cc_call
    sin_any = W.fx.json(Pc.tag + '/F4/state_input_any.json', {'schema': 'UNT_POINT_LO_STATE_INPUT_CX2V001'})
    MF('R16_F4_srb_common_refusal_structured_unavailable', 'F4 common Refusal and writer refusals caught (never a crash)',
       lambda: W.SRB._adapt(Pc.spec, call_dir=K16.call_dir, result=K16.result, inventory=K16.inventory, bundle_ref=W._cc_bundle,
                            state_input_ref=sin_any, rows_input_ref=None, root_ruling_refs=W.rulings,
                            approved_producer_sha256=W.approved, trusted_source_producers=[W.src_producer['sha256']],
                            env=W.srb_env(read_pin=boom)),
       lambda v: v.get('verdict') == 'UNAVAILABLE' and 'SYNTHETIC_COMMON_REFUSAL_FROM_A_READER' in json.dumps(v['blockers']),
       'UNAVAILABLE with the common refusal recorded')
    # F4 in main(): a writer refusal in each CLI is a JSON result with exit 3, never a traceback.
    py = sys.executable
    spec_pin = W.fx.json(Pc.tag + '/F4/spec_for_cli.json', Pc.spec)
    inv_pin = W.fx.json(Pc.tag + '/F4/inventory_for_cli.json', K16.inventory)
    cli_args = {
        'slot': {'spec_ref': spec_pin, 'rho_ref': Pc.rho_pin, 'registered_rho_records': registered, 'anchor_rho_pair': pair,
                 'root_ruling_refs': W.rulings, 'approved_producer_sha256': []},
        'state': {'spec_ref': spec_pin, 'call_dir': K16.call_dir, 'inventory_ref': inv_pin, 'bundle_ref': W._cc_bundle,
                  'state_inputs': {}, 'root_ruling_refs': W.rulings, 'approved_producer_sha256': [],
                  'trusted_source_producers': [], 'trusted_row_policy_review_sha256': []},
        'srb': {'spec_ref': spec_pin, 'call_dir': K16.call_dir, 'inventory_ref': inv_pin, 'bundle_ref': W._cc_bundle,
                'state_input_ref': None, 'rows_input_ref': None, 'root_ruling_refs': W.rulings, 'approved_producer_sha256': [],
                'trusted_source_producers': []}}
    for name in ('slot', 'state', 'srb'):
        ap_ = W.fx.json(Pc.tag + '/F4/cli_args_%s.json' % name, cli_args[name])
        bad_out = os.path.join(W.fx.root, Pc.tag, 'F4', 'uvt_cli_out_%s' % name)
        r = subprocess.run([TASKPOLICY, '-b', py, '-I', '-B', W.paths[name], '--args', ap_['path'], '--args-sha256', ap_['sha256'],
                            '--out-root', bad_out], capture_output=True, text=True, timeout=300)
        last = (r.stdout.strip().splitlines() or [''])[-1]
        record('C09_%s_cli_writer_refusal_structured_exit_3' % name, 'MUST_FAIL', 'F4 main(): structured result, never a crash',
               r.returncode == 3 and 'UVT_COMPONENT_REFUSED' in last and 'Traceback' not in r.stderr and not os.path.exists(bad_out),
               'exit 3, one JSON line naming UVT_COMPONENT_REFUSED, no traceback, nothing created',
               (r.returncode, last[-400:], r.stderr[-300:]))
    # ---- F5: the rho record's producer bytes are read and must be a1dcdea8.
    def rho_variant_pin(tag, producer, d=None):
        rec_ = W.rho_record(d or Pc.details, DEFAULT_RHOS, producer=producer, utc='2026-10-19T07:00:00Z')
        return W.fx.json(Pc.tag + '/F5/rho_%s.json' % tag, rec_), rec_
    missing_prod = {'path': '/nonexistent_c3v002/point_response_producer_cx2v002.py', 'sha256': REAL['response'][1]}
    other_prod = {'path': REAL['custody'][0], 'sha256': REAL['response'][1]}
    for cid, prod in (('S19_F5_rho_producer_path_missing_refused', missing_prod),
                      ('S19b_F5_rho_producer_other_bytes_refused', other_prod)):
        pin_, _ = rho_variant_pin(cid[:4], prod)
        sp_ = copy.deepcopy(Pc.spec)
        sp_['numerics']['uv_tail']['lo_certificate'] = pin_
        Pv = copy.copy(Pc)
        Pv.spec = sp_
        MF(cid, 'F5 rho producer bytes read and verified (a1dcdea8)',
           lambda Pv=Pv, pin_=pin_: slot_prove(W, Pv, pair, registered + [pin_], rho_ref=pin_),
           lambda v: v.get('verdict') == 'BLOCKED' and 'RHO_PRODUCER_BYTES_NOT_A1DCDEA8' in json.dumps(v['blockers']),
           'BLOCKED RHO_PRODUCER_BYTES_NOT_A1DCDEA8')
    reads = []

    def spy_raw(ref):
        reads.append(dict(ref))
        return W.read_raw(ref)
    MP('S19c_F5_honest_producer_bytes_are_read', 'F5 rho producer bytes read and verified (a1dcdea8)',
       lambda: (slot_prove(W, Pc, pair, registered, env=W.slot_env(read_raw=spy_raw))['verdict'], reads.count(W.pin['response'])),
       lambda v: v[0] == 'READY_FOR_MANIFEST' and v[1] >= 3, 'READY; the a1dcdea8 bytes were read for the slot rho and both anchor runs')
    bad_slot_pin, bad_slot_rec = rho_variant_pin('L26_slot', missing_prod)
    forged = dict(W.read_pin(slot_pin_c), driver_certificate=bad_slot_pin, rho_record=bad_slot_pin)
    forged_pin = W.fx.json(Pc.tag + '/F5/slot_proof_on_missing_producer_rho.json', forged)
    sp26 = copy.deepcopy(Pc.spec)
    sp26['numerics']['uv_tail']['lo_certificate'] = bad_slot_pin
    P26 = copy.copy(Pc)
    P26.spec = sp26
    b26 = W.fx.json(Pc.tag + '/F5/bundle_missing_producer_rho.json',
                    bundle(W, Pc, forged_pin, bindings={'eps_certificate': Pc.eps_pin, 'lo_certificate': bad_slot_pin}))
    MF('L26_F5_state_slot_rho_producer_bytes_missing', 'F5 rho producer bytes read and verified (a1dcdea8)',
       lambda: scen(W, 'L26', P=P26, bundle_pin=b26),
       lambda v: v[1]['call_lo_reading'] == 'INCOMPLETE' and 'RHO_PRODUCER_BYTES_NOT_A1DCDEA8' in json.dumps(v[1]['blockers']),
       'call INCOMPLETE RHO_PRODUCER_BYTES_NOT_A1DCDEA8 (slot rho)')
    core_bad = W.rho_record(Pc.details, DEFAULT_RHOS, producer=missing_prod)
    MF('L26b_F5_state_core_rho_producer_bytes_missing', 'F5 rho producer bytes read and verified (a1dcdea8)',
       lambda: scen(W, 'L26b', P=Pc, bundle_pin=bundle_pin_c,
                    inp_kw={'overrides': lambda K_: {'A2': {'synthetic_rho_override': core_bad}}}),
       lambda v: by_name(v[0], v[1])['A2']['verdict'] == 'UNAVAILABLE'
       and 'RHO_PRODUCER_BYTES_NOT_A1DCDEA8' in json.dumps(by_name(v[0], v[1])['A2']['blockers']),
       'A2 UNAVAILABLE RHO_PRODUCER_BYTES_NOT_A1DCDEA8 (recomputed rho)')
    # ---- F6: lo_producer v004 L71-78 re-applied (row state_files).
    foreign = W.fx.raw(Pc.tag + '/F6/foreign_readout_state.bin', b'foreign readout archive')
    for cid, over, code in (
            ('L27_F6_row_state_files_empty', lambda K_: {'A1': {'state_files': []}}, 'OWN_RUN_READOUT_STATE_ARCHIVES_UNAVAILABLE'),
            ('L27b_F6_row_state_files_absent', lambda K_: {'A1': {'__drop__': ['state_files']}}, 'OWN_RUN_READOUT_STATE_ARCHIVES_UNAVAILABLE'),
            ('L27c_F6_row_state_files_outside_run_root', lambda K_: {'A1': {'state_files': [foreign]}},
             'CROSS_RUN_READOUT_SUBSTITUTION_FORBIDDEN'),
            ('L27d_F6_row_state_file_bytes_differ', lambda K_: {'A1': {'state_files': [dict(K_.result_pin, sha256='e' * 64)]}},
             'byte pin mismatch')):
        MF(cid, 'F6 lo_producer v004 L71-78 row state_files rule',
           lambda over=over, cid=cid: scen(W, cid[:4] + cid[-6:], P=Pc, bundle_pin=bundle_pin_c, inp_kw={'row_over': over}),
           lambda v, code=code: by_name(v[0], v[1])['A1']['verdict'] == 'UNAVAILABLE'
           and code in json.dumps(by_name(v[0], v[1])['A1']['blockers']) and v[1]['call_lo_reading'] == 'INCOMPLETE', code)
    MP('L27e_F6_honest_state_files_inside_run_root_pass', 'F6 lo_producer v004 L71-78 row state_files rule (control)',
       lambda: (rec_l01['call_lo_reading'], [s['verdict'] for s in rec_l01['states']]),
       lambda v: v[0] == 'PASS' and v[1] and all(x == 'PASS' for x in v[1]),
       'L01 (row state_files = the call\'s own result.json inside <call_dir>/out) reads PASS on every state')
    # ---- F9: each CLI main() runs the root gate before any pin read.
    def gate_first(mod):
        saved, saved_common = mod.ROOT_RULINGS, mod.common
        calls = []

        def no_common():
            calls.append('common')
            raise AssertionError('COMMON_LOADED_BEFORE_THE_ROOT_GATE')
        mod.ROOT_RULINGS = (dict(saved[0], sha256='0' * 64), saved[1])
        mod.common = no_common
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = mod.main(['--args', '/nonexistent_c3v002/args.json', '--args-sha256', '0' * 64,
                               '--out-root', '/nonexistent_c3v002/out'])
        finally:
            mod.ROOT_RULINGS, mod.common = saved, saved_common
        return {'rc': rc, 'stdout': out.getvalue()[-500:], 'common_calls': calls}
    for name, mod in (('slot', W.SLOT), ('state', W.STATE), ('srb', W.SRB)):
        MF('C08_F9_%s_main_root_gate_before_any_pin_read' % name, 'F9 the root gate runs before any pin read in main()',
           lambda mod=mod: gate_first(mod),
           lambda v: v['rc'] == 3 and 'ROOT_RULING_UNREADABLE_OR_CHANGED' in v['stdout'] and v['common_calls'] == [],
           'exit 3 ROOT_RULING_UNREADABLE_OR_CHANGED; nothing loaded or read before the gate')

        def real_gate_then_args(mod=mod):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = mod.main(['--args', '/nonexistent_c3v002/args.json', '--args-sha256', '0' * 64,
                               '--out-root', '/nonexistent_c3v002/out'])
            return {'rc': rc, 'stdout': out.getvalue()[-500:]}
        MP('C08b_F9_%s_main_real_gate_passes_then_structured_args_refusal' % name, 'F9 + F4 (control)', real_gate_then_args,
           lambda v: v['rc'] == 3 and 'OUTSIDE_ALLOWED_ROOTS' in v['stdout'], 'gate passes; the args read refusal is a JSON result')
    # ---- F11 and hygiene.
    v = raises(lambda: require_synthetic(SUITE_DIR + '/not_synthetic/x'), 'F11 suite outputs must be under')
    record('H01_F11_outputs_outside_synthetic_refused', 'MUST_FAIL', 'F11 suite outputs only under synthetic/', v['match'],
           'REFUSED F11', v)
    v = raises(lambda: require_synthetic(SYNTHETIC_DIR), 'F11 suite outputs must be under')
    record('H01b_F11_synthetic_dir_itself_refused', 'MUST_FAIL', 'F11 suite outputs only under synthetic/ (a run folder)',
           v['match'], 'REFUSED F11', v)
    # ---- NOTE evidence (A115 NOTE for root; TESTED from bytes): the v002 input side emits neither field F6 / c3v001 need.
    def interface_gap():
        rp = open(REAL['row_producer_q2_v002'][0], 'rb').read()
        hp = open(REAL['handoff_q2_v002'][0], 'rb').read()
        return {'row_producer_sha_ok': sha_bytes(rp) == REAL['row_producer_q2_v002'][1],
                'handoff_sha_ok': sha_bytes(hp) == REAL['handoff_q2_v002'][1],
                'row_producer_emits_state_files': b'state_files' in rp, 'handoff_emits_execution': b"'execution'" in hp}
    MP('N01_NOTE_input_side_v002_emits_no_state_files_and_no_execution', 'NOTE evidence for root (interface gap)', interface_gap,
       lambda v: v['row_producer_sha_ok'] and v['handoff_sha_ok'] and not v['row_producer_emits_state_files']
       and not v['handoff_emits_execution'],
       'TESTED: row_reference_producer_c2v002 has no state_files and acceptance_handoff_c2v002 no execution, so on those '
       'inputs every state reads UNAVAILABLE (fail closed) until the input side adds them')


def tests_wrapper_v002(W, Pc, slot_res, slot_pin_c, bundle_pin_c, rec_l01, K_l01):
    """The real wrapper v002 (7a6af535) L145-191 bytes, AST-extracted, against the c3v002 proof-side outputs."""
    raw = open(REAL['wrapper_v002'][0], 'rb').read()
    src = raw.decode('utf-8')
    tree = ast.parse(src)
    ctx = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Context'][0]
    cc = [n for n in ctx.body if isinstance(n, ast.FunctionDef) and n.name == 'certificate_check'][0]
    tries = [n for n in cc.body if isinstance(n, ast.Try)]
    lo_l, hi_l = WRAPPER_V002_BLOCK_LINES
    sel = [n for n in tries[0].body if n.lineno >= lo_l and n.end_lineno <= hi_l] if len(tries) == 1 else []
    inside = [n for n in tries[0].body if lo_l <= n.lineno <= hi_l] if len(tries) == 1 else []
    lines = src.split('\n')
    blk = '\n'.join(lines[lo_l - 1:hi_l]) + '\n'
    l30 = [n for n in tree.body if isinstance(n, ast.Assign) and n.lineno == 30]
    guard_path = guard_sha = None
    if len(l30) == 1 and isinstance(l30[0].value, ast.Call):
        call = l30[0].value
        a0 = call.args[0] if call.args else None
        if isinstance(a0, ast.Call) and a0.args and isinstance(a0.args[0], ast.Constant):
            guard_path = a0.args[0].value
        guard_sha = next((k.value.value for k in call.keywords if k.arg == 'expected'), None)
    MP('W07_wrapper_v002_block_is_L145_191_by_AST', 'wrapper v002 L145-191 extracted by AST from the 7a6af535 bytes',
       lambda: {'sha_ok': sha_bytes(raw) == REAL['wrapper_v002'][1], 'n': len(sel), 'first': sel[0].lineno if sel else None,
                'last': sel[-1].end_lineno if sel else None, 'contiguous': [n.lineno for n in sel] == [n.lineno for n in inside],
                'core_record_reads': blk.count("lo['core_record']"), 'rule_in_file': src.count(
                    "'driver_slot_rule':'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'"),
                'block_sha256': sha_bytes(blk.encode()), 'guard_l30': [guard_path, guard_sha]},
       lambda v: v['sha_ok'] and v['n'] == 3 and v['first'] == lo_l and v['last'] == hi_l and v['contiguous']
       and v['core_record_reads'] == 1 and v['rule_in_file'] == 1
       and v['guard_l30'] == [REAL['guard_b1'][0], REAL['guard_b1'][1]],
       'three statements L145-191; one core_record read; root slot-rule string at L74; L30 loads guard b1 9e3fc109')

    class Error(Exception):
        pass
    ns_o = extract_functions(REAL['parent_v005'][0], REAL['parent_v005'][1], ['sha256_bytes', 'read_pinned'],
                             {'hashlib': hashlib, 'Path': __import__('pathlib').Path, 'OrchestratorError': Error})
    O = types.SimpleNamespace(read_pinned=ns_o['read_pinned'])
    ns_m = extract_functions(REAL['wrapper_core'][0], REAL['wrapper_core'][1], ['canonical', 'digest', 'pin_doc'],
                             {'json': json, 'hashlib': hashlib, 'O': O})
    M = types.SimpleNamespace(pin_doc=ns_m['pin_doc'], digest=ns_m['digest'], canonical=ns_m['canonical'])
    G = load_exact(guard_path or REAL['guard_b1'][0], REAL['guard_b1'][1], 'ps_test_guard_b1')
    fsrc = ('def _wrapper_v002_slot_block(spec, bundle, custody, ident, r, rec, phase, M, O, G, Error):\n'
            + textwrap.indent(textwrap.dedent(blk), '    ') + '    return "ACCEPTED"\n')
    nsb = {}
    exec(compile(fsrc, REAL['wrapper_v002'][0] + ' L145-191', 'exec'), nsb)
    block = nsb['_wrapper_v002_slot_block']
    ident, custody = Pc.details['identity'], Pc.details['custody']
    r = {'approved_certificate_producers': W.approved_pins}
    b0 = W.read_pin(bundle_pin_c)
    rec0 = {'identity': ident, 'bundle': bundle_pin_c, 'eps_certificate': Pc.eps_pin, 'lo_certificate': Pc.rho_pin}

    def run(bun, phase='prelaunch', rec=rec0, spec=None):
        return block(spec or Pc.spec, bun, custody, ident, r, rec, phase, M, O, G, Error)
    MP('W08_wrapper_v002_prelaunch_accepts_c3v002_slot_proof', 'wrapper v002 L145-172 (prelaunch) accepts the slot proof',
       lambda: run(b0), lambda v: v == 'ACCEPTED', 'ACCEPTED')
    rows = rec_l01['lo_rows_for_acceptance_bundle']
    acc = dict(b0, states=rows, parent_prelaunch_bundle=bundle_pin_c)
    MP('W09_wrapper_v002_acceptance_reads_core_record_of_every_state', 'per-state LO proof core_record as wrapper v002 L185 reads it',
       lambda: (run(acc, 'acceptance'), len(rows), all(C_is_pin(W.read_pin(x['LO']).get('core_record')) for x in rows)),
       lambda v: v[0] == 'ACCEPTED' and v[1] == len(K_l01.inventory['states']) and v[2] is True,
       'ACCEPTED: every per-state proof core_record pin resolves to the CURRENT_SAVED_STATE record of that state')
    first = rows[0]
    lo = W.read_pin(first['LO'])
    no_core = {k: v for k, v in lo.items() if k != 'core_record'}
    p_nc = W.fx.json(Pc.tag + '/W10/lo_proof_without_core_record.json', no_core)
    v = raises(lambda: run(dict(acc, states=[dict(first, LO=p_nc)] + rows[1:]), 'acceptance'), 'core_record')
    record('W10_wrapper_v002_refuses_proof_without_core_record', 'MUST_FAIL', 'per-state LO proof core_record as wrapper v002 L185 reads it',
           v['match'] and 'KeyError' in str(v['raised']), "KeyError: 'core_record'", v)
    core = W.read_pin(lo['core_record'])
    core2 = copy.deepcopy(core)
    core2['rho']['shells'][0]['rho_used'] = nextup(core2['rho']['shells'][0]['rho_used'])
    c2pin = W.fx.json(Pc.tag + '/W11/core_record_rho_one_ulp.json', core2)
    p2 = W.fx.json(Pc.tag + '/W11/lo_proof_core_rho_one_ulp.json', dict(lo, core_record=c2pin))
    v = raises(lambda: run(dict(acc, states=[dict(first, LO=p2)] + rows[1:]), 'acceptance'), 'recomputed rho differs from the lo slot rho')
    record('W11_wrapper_v002_refuses_core_rho_one_ulp_off', 'MUST_FAIL', 'wrapper v002 10-key bitwise rho compare', v['match'],
           'recomputed rho differs from the lo slot rho (bitwise)', v)
    core3 = copy.deepcopy(core)                     # c3v003 V03: a 1-ulp change in a diagnostic field only
    core3['rho']['shells'][2]['rho_envelope']['estimate'] = nextup(core3['rho']['shells'][2]['rho_envelope']['estimate'])
    c3pin = W.fx.json(Pc.tag + '/W16/core_record_rho_diagnostic_one_ulp.json', core3)
    p3d = W.fx.json(Pc.tag + '/W16/lo_proof_core_rho_diagnostic_one_ulp.json', dict(lo, core_record=c3pin))
    v = raises(lambda: run(dict(acc, states=[dict(first, LO=p3d)] + rows[1:]), 'acceptance'), 'recomputed rho differs from the lo slot rho')
    record('W16_V03_wrapper_v002_refuses_core_rho_one_ulp_diagnostic', 'MUST_FAIL',
           'V03 a 1-ulp diagnostic change refuses in the wrapper (L189-191), as in the adapter (L02b)',
           v['match'] and W.STATE.rho_projection(core3['rho']) == W.STATE.rho_projection(core['rho']),
           'recomputed rho differs from the lo slot rho (bitwise), with the projection unchanged', v)
    other = rows[1]['state']
    p3 = W.fx.json(Pc.tag + '/W12/lo_proof_other_state.json', dict(lo, state=other))
    v = raises(lambda: run(dict(acc, states=[dict(first, LO=p3)] + rows[1:]), 'acceptance'),
               'per-state LO record is not the acceptance record of this state')
    record('W12_wrapper_v002_refuses_proof_for_another_state', 'MUST_FAIL', 'per-state LO proof bound to its state', v['match'],
           'per-state LO record is not the acceptance record of this state', v)
    fc = W.fx.json(Pc.tag + '/W13/slot_proof_covers_all.json', dict(slot_res['proof'], covers_all_consumed_states=False))
    v = raises(lambda: run(bundle(W, Pc, fc)), 'carries covers_all_consumed_states')
    record('W13_wrapper_v002_refuses_slot_proof_with_covers_all_key', 'MUST_FAIL', 'covers_all_consumed_states refused (L163)',
           v['match'], 'LO_RHO_SLOT proof carries covers_all_consumed_states', v)
    v = raises(lambda: run(b0, rec=dict(rec0, lo_certificate=W.fx.json(Pc.tag + '/W14/other_rho.json',
                                                                        W.rho_record(Pc.details, DEFAULT_RHOS, utc='2026-10-19T08:00:00Z')))),
               'lo slot is not the registered rho record of this point')
    record('W14_wrapper_v002_refuses_slot_not_the_registry_rho', 'MUST_FAIL', 'slot = the registry lo_certificate (L165)', v['match'],
           'lo slot is not the registered rho record of this point', v)
    v = raises(lambda: run(bundle(W, Pc, slot_pin_c, extra_prelaunch={'LO_RHO_SLOT': None})), '{path, sha256} required')
    record('W15_wrapper_v002_refuses_missing_slot_proof', 'MUST_FAIL', 'the LO_RHO_SLOT proof is required (L149)',
           v['match'], 'LO_RHO_SLOT slot proof: {path, sha256} required', v)


# ------------------------------------------------------------------------------------------------ c3v003 additions (A138)
B1_ENUM_SHA = '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0'     # V02: consumed_states_b1_c2v001
V010_ENUM_SHA = 'e48cca3c35a3d6d3724f74b9407b91f006bd31f2f30f416f9c328ba9e4144ca2'   # consumed_states_cx2v010
HANDOFF_READING_LINES = (373, 391)         # B3: root's acceptance_handoff_c2v002 call reading (0690 OPEN-6)


def wrapper_v002_rho_compare():
    """V03: wrapper v002's own bitwise rho comparison, taken from the 7a6af535 bytes by AST: the L177-178 keys tuple, the
    L179 want, and the L190 test (whose L191 body raises). Returns (keys, equal(slot_rho, got) -> bool, provenance)."""
    raw = open(REAL['wrapper_v002'][0], 'rb').read()
    if sha_bytes(raw) != REAL['wrapper_v002'][1]:
        raise ValueError('wrapper v002 bytes are not 7a6af535')
    src = raw.decode('utf-8')
    tree = ast.parse(src)
    found = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            if (n.targets[0].id, n.lineno) in (('keys', 177), ('want', 179), ('got', 189)):
                found[n.targets[0].id] = n
        if isinstance(n, ast.If) and n.lineno == 190:
            found['test'] = n
    if sorted(found) != ['got', 'keys', 'test', 'want'] or found['keys'].end_lineno != 178:
        raise ValueError('wrapper v002 L177-191 rho comparison not found by AST: %r' % sorted(found))
    body = found['test'].body
    msg = None
    if len(body) == 1 and isinstance(body[0], ast.Raise) and isinstance(body[0].exc, ast.Call) and body[0].exc.args \
            and isinstance(body[0].exc.args[0], ast.Constant):
        msg = body[0].exc.args[0].value
    keys = ast.literal_eval(found['keys'].value)
    seg = lambda n: ast.get_source_segment(src, n)
    fsrc = ('def _wrapper_v002_rho_equal(rho, got, M):\n    %s\n    %s\n    return not (%s)\n'
            % (seg(found['keys']), seg(found['want']), seg(found['test'].test)))
    ns = {}
    exec(compile(fsrc, REAL['wrapper_v002'][0] + ' L177-179,L190', 'exec'), ns)

    class Error(Exception):
        pass
    ns_o = extract_functions(REAL['parent_v005'][0], REAL['parent_v005'][1], ['sha256_bytes', 'read_pinned'],
                             {'hashlib': hashlib, 'Path': __import__('pathlib').Path, 'OrchestratorError': Error})
    ns_m = extract_functions(REAL['wrapper_core'][0], REAL['wrapper_core'][1], ['canonical', 'digest', 'pin_doc'],
                             {'json': json, 'hashlib': hashlib, 'O': types.SimpleNamespace(read_pinned=ns_o['read_pinned'])})
    M = types.SimpleNamespace(canonical=ns_m['canonical'])
    fn = ns['_wrapper_v002_rho_equal']
    prov = {'keys': list(keys), 'want_src': seg(found['want']), 'test_src': seg(found['test'].test), 'raise': msg,
            'got_src': seg(found['got'])}
    return tuple(keys), (lambda slot_rho, got: fn(slot_rho, got, M)), prov


def root_handoff_reading():
    """B3: root's acceptance_handoff_c2v002 (ccdbec2b) call reading L373-391 and READINGS, from its bytes by AST, compiled
    unchanged into a function of rec. Returns (function(rec) -> rec, READINGS)."""
    raw = open(REAL['handoff_q2_v002'][0], 'rb').read()
    if sha_bytes(raw) != REAL['handoff_q2_v002'][1]:
        raise ValueError('acceptance_handoff_c2v002 bytes are not ccdbec2b')
    src = raw.decode('utf-8')
    tree = ast.parse(src)
    rd = [n for n in tree.body if isinstance(n, ast.Assign) and [getattr(t, 'id', None) for t in n.targets] == ['READINGS']]
    readings = ast.literal_eval(rd[0].value) if len(rd) == 1 else None
    lo_l, hi_l = HANDOFF_READING_LINES
    fns = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.lineno <= lo_l <= hi_l <= n.end_lineno]
    tries = [t for f in fns for t in ast.walk(f) if isinstance(t, ast.Try) and any(s.lineno == lo_l for s in t.body)]
    sel = [s for s in tries[0].body if lo_l <= s.lineno <= hi_l] if len(tries) == 1 else []
    if not readings or not sel or sel[0].lineno != lo_l or sel[-1].end_lineno != hi_l:
        raise ValueError('root handoff reading block L373-391 not found by AST')
    blk = '\n'.join(src.split('\n')[lo_l - 1:hi_l]) + '\n'
    fsrc = 'def _root_reading(rec, READINGS):\n' + textwrap.indent(textwrap.dedent(blk), '    ') + '    return rec\n'
    ns = {}
    exec(compile(fsrc, REAL['handoff_q2_v002'][0] + ' L373-391', 'exec'), ns)
    return (lambda rec: ns['_root_reading'](rec, readings)), readings


def group(name, fn, default=None):
    """c3v003 harness: a test group that raises is recorded as one failed case and the suite goes on, so a mutant that
    breaks an early group still yields a results file that names the cases it fails. No case, check or expectation
    changes; an honest run records no extra case."""
    try:
        return fn()
    except Exception as exc:
        record('ZZ_GROUP_ABORTED_' + name, 'MUST_PASS', 'harness: every test group runs to its end', False, 'no exception',
               type(exc).__name__ + ': ' + str(exc) + ' | ' + traceback.format_exc()[-600:])
        return default


def tests_c3v003_v02(W, A, Pc, pair, registered, bundle_pin_c):
    # ================================================================ V02: the b1 enumerator (A138 item 2)
    def enum_scope():
        b1 = open(REAL['enumerator'][0], 'rb').read()
        v10 = open(REAL['enumerator_v010'][0], 'rb').read()
        tb, tv = ast.parse(b1.decode('utf-8')), ast.parse(v10.decode('utf-8'))
        is_pins = lambda n: isinstance(n, ast.Assign) and [getattr(t, 'id', None) for t in n.targets] == ['PINS']
        same = (len(tb.body) == len(tv.body) and all(ast.dump(a) == ast.dump(b) for a, b in zip(tb.body, tv.body)
                                                       if not (is_pins(a) and is_pins(b))))
        pins_b1 = [ast.literal_eval(n.value) for n in tb.body if is_pins(n)]
        return {'b1_sha': sha_bytes(b1), 'v010_sha': sha_bytes(v10), 'b1_path': REAL['enumerator'][0],
                'non_PINS_statements_identical': same, 'pins_differ': [ast.dump(n) for n in tb.body if is_pins(n)] !=
                [ast.dump(n) for n in tv.body if is_pins(n)], 'b1_pins_A': (pins_b1[0] if len(pins_b1) == 1 else {}).get('A'),
                'schema_in_both': b1.count(b"'schema':'DDO154_CONSUMED_STATE_JOIN_CX2V010'") == 1 ==
                v10.count(b"'schema':'DDO154_CONSUMED_STATE_JOIN_CX2V010'"),
                'adapter_consts': [W.STATE.ENUMERATOR_SHA, W.SRB.ENUMERATOR_SHA]}
    MP('V02a_b1_enumerator_bytes_and_PINS_only_diff', 'V02 the C1 enumerator is consumed_states_b1_c2v001 4ca7f364 (A138)',
       enum_scope, lambda v: v['b1_sha'] == B1_ENUM_SHA and v['v010_sha'] == V010_ENUM_SHA
       and v['b1_path'] == ART + '/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py'
       and v['non_PINS_statements_identical'] and v['pins_differ'] and v['schema_in_both']
       and v['b1_pins_A'] == (ART + '/s4_acceptance_c2/offset_b1/current_source_evidence_b1_c2v001.py',
                              '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce')
       and v['adapter_consts'] == [B1_ENUM_SHA, B1_ENUM_SHA],
       'b1 4ca7f364 from bytes (offset_b1 README item 4); every statement but PINS identical to v010 e48cca3c; the v010 '
       'join schema; PINS A = evidence b1 7044e131; both adapters pin 4ca7f364')
    K2 = make_call(W, Pc, 'V02_state')
    inp2 = state_inputs(W, Pc, K2)
    inv010 = copy.deepcopy(K2.inventory)
    inv010['producer'] = W.pin['enumerator_v010']
    n0 = [0]

    def v010_state():
        n0[0] = len(W.core_calls)
        r_ = run_state(W, Pc, K2, inp2, bundle_pin=bundle_pin_c, inventory=inv010)
        return r_, len(W.core_calls) - n0[0]
    MF('L13b_V02_state_v010_inventory_refused', 'V02 a v010 inventory is refused (state adapter, A138)', v010_state,
       lambda v: v[0]['call_lo_reading'] == 'INCOMPLETE' and v[0]['states'] == [] and v[1] == 0
       and 'INVENTORY_PRODUCER_NOT_B1_4CA7F364' in json.dumps(v[0]['blockers']) and v[0]['lo_gate_passed_all_states'] is False,
       'INCOMPLETE INVENTORY_PRODUCER_NOT_B1_4CA7F364; no state read; the core never ran')
    MP('L13c_V02_state_b1_inventory_accepted', 'V02 a b1 inventory is accepted (state adapter, A138)',
       lambda: (run_state(W, Pc, K2, inp2, bundle_pin=bundle_pin_c), K2.inventory['producer']),
       lambda v: v[0]['call_lo_reading'] == 'PASS' and len(v[0]['states']) == len(K2.inventory['states'])
       and all(s['verdict'] == 'PASS' for s in v[0]['states']) and v[1] == W.pin['enumerator'] and v[1]['sha256'] == B1_ENUM_SHA,
       'PASS on the same call and inputs with the b1 inventory (producer 4ca7f364)')


def tests_c3v003_v03(W, A, Pc, pair, registered, bundle_pin_c):
    by = lambda v: by_name(v[0], v[1])
    # ================================================================ V03: wrapper v002's 10-key canonical rho comparison
    keys, wrapper_equal, prov = wrapper_v002_rho_compare()

    def ast_parity():
        def fn_dump(path, name):
            t = ast.parse(open(path).read())
            f = [n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == name]
            return ast.dump(ast.Module(body=f[0].body, type_ignores=[])) if len(f) == 1 else None
        return {'keys': list(keys), 'slot': list(W.SLOT.RHO_COMPARE_KEYS), 'state': list(W.STATE.RHO_COMPARE_KEYS),
                'canonical_core': fn_dump(REAL['wrapper_core'][0], 'canonical'),
                'canonical_slot': fn_dump(W.paths['slot'], 'canonical'), 'canonical_state': fn_dump(W.paths['state'], 'canonical'),
                'want': prov['want_src'], 'test': prov['test_src'], 'raise': prov['raise'], 'got': prov['got_src']}
    MP('C07b_V03_compare_keys_and_canonical_are_wrapper_v002_by_AST', 'V03 the 10-key canonical comparison of wrapper v002 L177-191',
       ast_parity, lambda v: v['keys'] == v['slot'] == v['state'] and len(v['keys']) == 10
       and v['canonical_core'] is not None and v['canonical_core'] == v['canonical_slot'] == v['canonical_state']
       and v['want'] == 'want=M.canonical({k:rho.get(k) for k in keys})' and v['got'] == "got=evidence.get('rho')"
       and v['test'] == 'not isinstance(got,dict) or M.canonical({k:got.get(k) for k in keys})!=want'
       and v['raise'] == 'recomputed rho differs from the lo slot rho (bitwise)',
       'keys = wrapper L177-178 in both modules; canonical() = core dc895f8a L34-35 by AST; L179/L190/L191 as read')

    def ulp_at(rec, i, path):
        r = copy.deepcopy(rec)
        o = r['shells'][i]
        for k in path[:-1]:
            o = o[k]
        o[path[-1]] = nextup(o[path[-1]])
        return r
    base = copy.deepcopy(Pc.rho_rec)
    zero_p, zero_n = copy.deepcopy(base), copy.deepcopy(base)
    zero_p['shells'][0]['rho_used'], zero_n['shells'][0]['rho_used'] = 0.0, -0.0
    ints = copy.deepcopy(base)
    ints['shells'][0]['range_inverse_kpc'] = [4, 5]
    extra = copy.deepcopy(base)
    extra['shells'][5]['note'] = 'x'
    nosettings = copy.deepcopy(base)
    nosettings.pop('settings')
    meta = dict(copy.deepcopy(base), utc='2026-10-19T13:00:00Z', seconds=77.0, peak_rss_bytes=999, dependencies={'d': 1},
                point_symbol_checks={'x': 1}, limitation='other', status='OTHER', verdict='OTHER',
                producer={'path': '/synthetic/other_producer.py', 'sha256': '0' * 64}, synthetic_fixture='other')
    cases = [('identical', base, copy.deepcopy(base), True), ('run_metadata_and_provenance_only', base, meta, True),
             ('rho_used_one_ulp', base, ulp_at(base, 0, ['rho_used']), False),
             ('rho_envelope_estimate_one_ulp', base, ulp_at(base, 3, ['rho_envelope', 'estimate']), False),
             ('sampled_level_estimate_one_ulp', base, ulp_at(base, 8, ['sampled_levels', 0, 'estimate']), False),
             ('plus_zero_vs_minus_zero', zero_p, zero_n, False), ('range_int_vs_float', base, ints, False),
             ('extra_shell_key', base, extra, False), ('settings_key_absent', base, nosettings, False),
             ('custody_differs', base, dict(copy.deepcopy(base), custody=dict(base['custody'], grid_sha256='9' * 64)), False)]

    def decisions():
        out = []
        for name, a, b, want in cases:
            out.append({'case': name, 'want': want, 'wrapper': wrapper_equal(a, b),
                        'slot': W.SLOT.rho_bitwise_canonical(a) == W.SLOT.rho_bitwise_canonical(b),
                        'state': W.STATE.rho_bitwise_canonical(a) == W.STATE.rho_bitwise_canonical(b),
                        'projection_diagnostic': _safe_projection(W, a) == _safe_projection(W, b)})
        return out
    MP('C07c_V03_decisions_equal_wrapper_v002_on_every_case', 'V03 the 10-key canonical comparison of wrapper v002 L177-191',
       decisions, lambda v: all(x['wrapper'] == x['slot'] == x['state'] == x['want'] for x in v)
       and [x['case'] for x in v if x['projection_diagnostic'] and not x['want']] ==
       ['rho_envelope_estimate_one_ulp', 'sampled_level_estimate_one_ulp', 'range_int_vs_float', 'extra_shell_key',
        'settings_key_absent', 'custody_differs'],
       'slot and state decisions equal the wrapper\'s own L177-190 expressions on 10 cases; the old projection alone would '
       'have read 6 of the 8 unequal cases equal (it is a diagnostic only now)')
    fail = lambda code: (lambda v: v.get('verdict') == 'BLOCKED' and v.get('proof') is None and code in json.dumps(v['blockers']))
    a0 = W.read_pin(pair[0])
    d1 = ulp_at(W.rho_record(A.details, DEFAULT_RHOS, utc='2026-10-19T03:30:00Z'), 4, ['rho_envelope', 'estimate'])
    d1_pin = W.fx.json(A.tag + '/rho_anchor_run_diag_ulp.json', d1)
    MF('S11c_V03_anchor_pair_one_ulp_diagnostic_refused', 'V03 (a)4: a 1-ulp diagnostic change refuses, as the wrapper does',
       lambda: (slot_prove(W, Pc, [pair[0], d1_pin], registered + [d1_pin]), W.SLOT.rho_projection(a0) == W.SLOT.rho_projection(d1),
                wrapper_equal(a0, d1)),
       lambda v: fail('ANCHOR_RHO_NOT_BITWISE_EQUAL')(v[0]) and v[1] is True and v[2] is False,
       'BLOCKED ANCHOR_RHO_NOT_BITWISE_EQUAL with the projection equal; the wrapper comparison also reads unequal')
    d2 = ulp_at(W.rho_record(A.details, DEFAULT_RHOS, utc='2026-10-19T03:35:00Z'), 0, ['sampled_levels', 0, 'estimate'])
    d2_pin = W.fx.json(A.tag + '/rho_anchor_run_sampled_ulp.json', d2)
    MF('S11d_V03_anchor_pair_sampled_level_one_ulp_refused', 'V03 (a)4: a 1-ulp diagnostic change refuses, as the wrapper does',
       lambda: slot_prove(W, Pc, [pair[0], d2_pin], registered + [d2_pin]), fail('ANCHOR_RHO_NOT_BITWISE_EQUAL'),
       'BLOCKED ANCHOR_RHO_NOT_BITWISE_EQUAL')
    m1 = W.rho_record(A.details, DEFAULT_RHOS, utc='2026-10-19T03:40:00Z', seconds=99.0, peak_rss_bytes=12345,
                      dependencies={'synthetic': 'other run'}, point_symbol_checks={'synthetic': 1}, limitation='synthetic other')
    m1_pin = W.fx.json(A.tag + '/rho_anchor_run_metadata_only.json', m1)
    MP('S11e_V03_anchor_pair_run_metadata_not_compared', 'V03 (a)4: run metadata and provenance are not compared (wrapper L176)',
       lambda: slot_prove(W, Pc, [pair[0], m1_pin], registered + [m1_pin]),
       lambda v: v.get('verdict') == 'READY_FOR_MANIFEST' and v['proof']['anchor_rho_reproducibility']['bitwise_equal'] is True,
       'READY_FOR_MANIFEST')
    sd = ulp_at(W.rho_record(A.details, DEFAULT_RHOS, utc='2026-10-19T04:20:00Z'), 6, ['rho_envelope', 'estimate'])
    sd_pin = W.fx.json(A.tag + '/rho_anchor_slot_diag_ulp.json', sd)
    spd = copy.deepcopy(A.spec)
    spd['numerics']['uv_tail']['lo_certificate'] = sd_pin
    Ad = copy.copy(A)
    Ad.spec = spd
    MF('S14b_V03_anchor_slot_one_ulp_diagnostic_refused', 'V03 (a)4 at the anchor slot: 10-key canonical against the pair',
       lambda: slot_prove(W, Ad, pair, registered + [sd_pin], rho_ref=sd_pin),
       fail('ANCHOR_SLOT_RHO_NOT_BITWISE_EQUAL_TO_REPRODUCED_PAIR'), 'ANCHOR_SLOT_RHO_NOT_BITWISE_EQUAL_TO_REPRODUCED_PAIR')
    slot_rec = W.read_pin(Pc.rho_pin)
    over_diag = ulp_at(Pc.rho_rec, 2, ['rho_envelope', 'estimate'])
    MF('L02b_V03_state_rho_one_ulp_diagnostic_refused', 'V03 per state: a 1-ulp diagnostic change refuses, as the wrapper does',
       lambda: (scen(W, 'L02b', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'overrides': lambda K_: {'A1': {'synthetic_rho_override': over_diag}}}),
                wrapper_equal(slot_rec, over_diag)),
       lambda v: (lambda s: s['verdict'] == 'UNAVAILABLE' and s.get('rho_bitwise_equal_to_slot') is False
                  and s.get('rho_projection_equal_to_slot_diagnostic_only') is True
                  and 'RHO_RECOMPUTE_NOT_BITWISE_EQUAL_TO_SLOT' in json.dumps(s['blockers']))(by(v[0])['A1'])
       and v[0][1]['call_lo_reading'] == 'INCOMPLETE' and v[1] is False,
       'A1 UNAVAILABLE RHO_RECOMPUTE_NOT_BITWISE_EQUAL_TO_SLOT (projection diagnostic True); call INCOMPLETE; wrapper unequal too')
    over_meta = dict(copy.deepcopy(Pc.rho_rec), dependencies={'synthetic': 'recompute'}, peak_rss_bytes=4321)
    MP('L02c_V03_state_rho_metadata_only_accepted', 'V03 per state: run metadata and provenance are not compared (wrapper L176)',
       lambda: scen(W, 'L02c', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'overrides': lambda K_: {'A1': {'synthetic_rho_override': over_meta}}}),
       lambda v: v[1]['call_lo_reading'] == 'PASS' and by(v)['A1']['rho_bitwise_equal_to_slot'] is True
       and by(v)['A1']['rho_projection_equal_to_slot_diagnostic_only'] is True, 'PASS; both forms recorded equal')
    MP('L02d_V03_projection_recorded_as_diagnostic_on_pass_states', 'V03 the old projection stays as a recorded diagnostic only',
       lambda: scen(W, 'L02d', P=Pc, bundle_pin=bundle_pin_c),
       lambda v: v[1]['call_lo_reading'] == 'PASS' and all(s.get('rho_projection_equal_to_slot_diagnostic_only') is True
                                                           and s.get('rho_bitwise_equal_to_slot') is True for s in v[1]['states']),
       'every PASS state records rho_bitwise_equal_to_slot (decision) and rho_projection_equal_to_slot_diagnostic_only')


def tests_c3v003_b3(W, A, Pc, bundle_pin_c, bundle_pin_a):
    fb = lambda names: (lambda K_: {n: unit_b1(fail_shell=True) for n in names})
    by = lambda v: by_name(v[0], v[1])
    # ================================================================ B3: the call reading is exactly 0690 OPEN-6
    reading = lambda want, cls=None: (lambda v: v[1]['call_lo_reading'] == want and (cls is None or v[1]['class_reading'] == cls))
    MF('L09j_B3_iterate_fail_and_iterate_unavailable_all_non_iterate_pass_TRANSIENT',
       'B3 0690 OPEN-6: TRANSIENT needs every non-iterate state at PASS (an UNAVAILABLE iterate does not block it)',
       lambda: scen(W, 'L09j', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'b1': fb(['A0']), 'missing': ('A2',)}),
       lambda v: v[1]['call_lo_reading'] == 'LO_UNCERTIFIED_TRANSIENT' and v[1]['class_reading'] == 'LO_UNCERTIFIED_TRANSIENT'
       and by(v)['A0']['verdict'] == 'FAIL' and by(v)['A0']['reading'] == 'LO_UNCERTIFIED_TRANSIENT'
       and by(v)['A2']['verdict'] == 'UNAVAILABLE' and 'STATE_INPUT_MISSING' in json.dumps(by(v)['A2']['blockers'])
       and all(s['verdict'] == 'PASS' for n, s in by(v).items() if n not in ('A0', 'A2'))
       and v[1]['lo_gate_passed_all_states'] is False,
       'LO_UNCERTIFIED_TRANSIENT (c3v002 read INCOMPLETE here); fails closed')

    def preserved(v, name):
        s = by(v)[name]
        doc = W.read_pin(s['record']) if C_is_pin(s.get('record')) else {}
        return (s['verdict'] == 'FAIL' and s['reading'] == 'LO_UNCERTIFIED_TRANSIENT' and doc.get('status') == 'TESTED'
                and doc.get('verdict') == 'FAIL' and doc.get('reading') == 'LO_UNCERTIFIED_TRANSIENT')
    MF('L09k_B3_iterate_fail_plus_non_iterate_unavailable_INCOMPLETE',
       'B3 0690 OPEN-6: otherwise INCOMPLETE, with the iterate failures recorded',
       lambda: scen(W, 'L09k', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'b1': fb(['A0']), 'missing': ('A2', 'L1C')}),
       lambda v: reading('INCOMPLETE', 'INCOMPLETE')(v) and preserved(v, 'A0'),
       'INCOMPLETE; the A0 failure is kept in its own TESTED state record (verdict FAIL, reading LO_UNCERTIFIED_TRANSIENT)')
    MF('L09k2_B3_iterate_fail_plus_accepted_unavailable_INCOMPLETE', 'B3 0690 OPEN-6: the accepted state is a non-iterate state',
       lambda: scen(W, 'L09k2', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'b1': fb(['A0']), 'missing': ('A1',)}),
       lambda v: reading('INCOMPLETE', 'INCOMPLETE')(v) and preserved(v, 'A0'), 'INCOMPLETE; A0 failure recorded')
    MF('L09l_B3_decisive_route_b_fail_with_others_unavailable_NLTM',
       'B3 0690 OPEN-6: a FAIL at a route-B state is decisive even when other states are UNAVAILABLE',
       lambda: scen(W, 'L09l', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'b1': fb(['OFF']), 'missing': ('A2', 'F0')}),
       lambda v: reading('NON_LAPSE_TAIL_MATERIAL', 'NON_LAPSE_TAIL_MATERIAL')(v) and by(v)['OFF']['verdict'] == 'FAIL',
       'NON_LAPSE_TAIL_MATERIAL')
    MF('L09l2_B3_decisive_accepted_fail_with_iterate_fail_and_unavailable_NLTM',
       'B3 0690 OPEN-6: a FAIL at the accepted state is decisive even when other states are UNAVAILABLE',
       lambda: scen(W, 'L09l2', P=Pc, bundle_pin=bundle_pin_c, inp_kw={'b1': fb(['A1', 'A0']), 'missing': ('A2', 'R0')}),
       reading('NON_LAPSE_TAIL_MATERIAL', 'NON_LAPSE_TAIL_MATERIAL'), 'NON_LAPSE_TAIL_MATERIAL')
    MF('L09m_B3_anchor_corner_step4_stop_class_TRANSIENT', 'B3 with OPEN-5: any LO FAIL at the anchor reads the step-4 stop',
       lambda: scen(W, 'L09m', P=A, bundle_pin=bundle_pin_a, inp_kw={'b1': fb(['A0']), 'missing': ('A2',)}),
       lambda v: v[1]['call_lo_reading'] == 'ANCHOR_LO_FAILURE_PRESERVED_STEP4_STOPS_FOR_ROOT' and v[1]['step4_stop'] is True
       and v[1]['class_reading'] == 'LO_UNCERTIFIED_TRANSIENT', 'anchor stop; class reading LO_UNCERTIFIED_TRANSIENT beside it')
    # B3 table: every verdict combination over 5 states, against root's own L373-391 bytes and the c3v002 reading.
    root_fn, readings = root_handoff_reading()
    old = load_exact(REAL['state_c3v002'][0], REAL['state_c3v002'][1], 'ps_c3v002_state_read_only')
    S = W.STATE
    classes = [S.ACCEPTED, S.ROUTE_B, S.ROUTE_B, S.ITERATE, S.ITERATE]
    root_cls = {S.ACCEPTED: 'ACCEPTED_ROUTE_A', S.ROUTE_B: 'ROUTE_B_STAGE', S.ITERATE: 'ROUTE_A_ITERATE'}
    root_rd = {'PASS': 'PASS', 'FAIL': 'LO_ABOVE_THRESHOLD', 'UNAVAILABLE': 'UNAVAILABLE'}

    def table():
        import itertools
        rows_, diff_old, mism = [], [], []
        for combo in itertools.product(('PASS', 'FAIL', 'UNAVAILABLE'), repeat=len(classes)):
            st = [{'verdict': v, 'state_class': c, 'state': {'state_sha256': '%064x' % i}} for i, (v, c) in enumerate(zip(combo, classes))]
            ours = S.call_reading(st, is_anchor=False, class_gap=None)['reading']
            rec = {'states': [{'reading': root_rd[s['verdict']], 'class': root_cls[s['state_class']], 'state': s['state']} for s in st],
                   'srb_rot': {'reading': 'PASS'}, 'guard': {'ok': True}, 'blockers': []}
            theirs = root_fn(rec)['reading']
            mapped = {'ACCEPTED': 'PASS'}.get(theirs, theirs)
            prev = old.call_reading(copy.deepcopy(st), is_anchor=False, class_gap=None)['reading']
            corner = (not any(v == 'FAIL' and c != S.ITERATE for v, c in zip(combo, classes))
                      and any(v == 'FAIL' and c == S.ITERATE for v, c in zip(combo, classes))
                      and all(v == 'PASS' for v, c in zip(combo, classes) if c != S.ITERATE)
                      and any(v == 'UNAVAILABLE' and c == S.ITERATE for v, c in zip(combo, classes)))
            rows_.append(combo)
            if ours != mapped:
                mism.append({'combo': combo, 'ours': ours, 'root': theirs})
            if (prev != ours) != corner or (corner and (prev, ours) != ('INCOMPLETE', 'LO_UNCERTIFIED_TRANSIENT')):
                diff_old.append({'combo': combo, 'c3v002': prev, 'c3v003': ours, 'corner': corner})
        return {'n': len(rows_), 'mismatch_vs_root': mism, 'unexpected_vs_c3v002': diff_old, 'readings': list(readings)}
    MP('B3T_call_reading_equals_root_handoff_L373_391_on_all_243_combinations', 'B3 0690 OPEN-6 (root handoff reference)',
       table, lambda v: v['n'] == 243 and v['mismatch_vs_root'] == [] and v['unexpected_vs_c3v002'] == []
       and v['readings'][:5] == ['NON_LAPSE_TAIL_MATERIAL', 'BOUND_INSUFFICIENT', 'UNDECIDABLE_FLAGGED', 'LO_UNCERTIFIED_TRANSIENT',
                                 'INCOMPLETE'],
       'equal to root\'s L373-391 (SRB PASS, guard ok; ACCEPTED = PASS) on every combination; c3v002 differs exactly on the '
       'B3 corner (iterate FAIL, iterate UNAVAILABLE, every non-iterate PASS), where it read INCOMPLETE')

    def inherited_and_gap():
        mk = lambda pairs: [{'verdict': v, 'state_class': c, 'state': {'state_sha256': '%064x' % i}} for i, (v, c) in enumerate(pairs)]
        r = lambda pairs, anchor=False: S.call_reading(mk(pairs), is_anchor=anchor, class_gap=None)
        return {
            'inherited_fail_others_unavailable': r([('FAIL', S.INHERITED), ('UNAVAILABLE', S.ITERATE), ('UNAVAILABLE', S.ROUTE_B)])['reading'],
            'inherited_unavailable_iterate_fail': r([('UNAVAILABLE', S.INHERITED), ('FAIL', S.ITERATE), ('PASS', S.ACCEPTED)])['reading'],
            'inherited_pass_iterate_fail_iterate_unav': r([('PASS', S.INHERITED), ('FAIL', S.ITERATE), ('UNAVAILABLE', S.ITERATE),
                                                          ('PASS', S.ACCEPTED)])['reading'],
            'class_unavailable_state_unavailable_iterate_fail': r([('UNAVAILABLE', S.CLASS_UNAVAILABLE), ('FAIL', S.ITERATE),
                                                                   ('PASS', S.ACCEPTED)])['reading'],
            'anchor_corner': r([('FAIL', S.ITERATE), ('UNAVAILABLE', S.ITERATE), ('PASS', S.ACCEPTED)], anchor=True)}
    MP('B3T2_inherited_and_unclassified_states_per_0690', 'B3 0690 OPEN-6 (inherited is decisive; any non-iterate must PASS)',
       inherited_and_gap, lambda v: v['inherited_fail_others_unavailable'] == 'NON_LAPSE_TAIL_MATERIAL'
       and v['inherited_unavailable_iterate_fail'] == 'INCOMPLETE'
       and v['inherited_pass_iterate_fail_iterate_unav'] == 'LO_UNCERTIFIED_TRANSIENT'
       and v['class_unavailable_state_unavailable_iterate_fail'] == 'INCOMPLETE'
       and v['anchor_corner']['reading'] == 'ANCHOR_LO_FAILURE_PRESERVED_STEP4_STOPS_FOR_ROOT'
       and v['anchor_corner']['class_reading'] == 'LO_UNCERTIFIED_TRANSIENT' and v['anchor_corner']['step4_stop'] is True,
       'NLTM / INCOMPLETE / TRANSIENT / INCOMPLETE / anchor stop with class TRANSIENT')


def _safe_projection(W, rec):
    try:
        return W.SLOT.rho_projection(rec)
    except Exception as exc:
        return 'REFUSED: ' + str(exc)


def C_is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and len(x['sha256']) == 64


def write_manifest(run_dir, fixture_root, results_pin):
    """F11: one manifest of every file under the run folder, written last by exclusive create."""
    files = []
    for d, dirs, names in os.walk(run_dir):
        dirs.sort()
        for n in sorted(names):
            p = os.path.join(d, n)
            if os.path.islink(p):
                files.append({'path': os.path.relpath(p, run_dir), 'symlink_to': os.readlink(p)})
                continue
            with open(p, 'rb') as f:
                data = f.read()
            try:
                doc = json.loads(data) if n.endswith('.json') else None
            except ValueError:
                doc = None
            files.append({'path': os.path.relpath(p, run_dir), 'sha256': sha_bytes(data), 'bytes': len(data),
                          'synthetic_fixture_key': isinstance(doc, dict) and 'synthetic_fixture' in doc})
    man = {'schema': 'S4RC1_PROOF_SIDE_SYNTHETIC_OUTPUTS_MANIFEST_C3V003', 'run_dir': run_dir, 'fixture_root': fixture_root,
           'results': results_pin, 'n_files': len(files), 'files': files,
           'statement': ('Every file listed here was written by the c3v003 synthetic suite or by a module under test during it. '
                         'All of them are SYNTHETIC: none is a measurement, a review, a ruling or a record of any real '
                         'computation. Module-written proofs and readings carry no synthetic_fixture key (the modules write '
                         'production-shaped records) and some carry real point keys, but their custody is synthetic, so the '
                         'wrapper, the guard and the adapters refuse them for any real point. Never register, pin or cite '
                         'any of them as evidence.'),
           'synthetic_fixture': SYN}
    out = os.path.join(run_dir, 'SYNTHETIC_OUTPUTS_MANIFEST_C3V003.json')
    raw = (json.dumps(man, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with open(out, 'xb') as f:
        f.write(raw)
    return {'path': out, 'sha256': sha_bytes(raw), 'n_files': len(files)}



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build-dir', required=True)
    ap.add_argument('--fixture-root', required=True)
    ap.add_argument('--results-dir', required=True)
    ap.add_argument('--reader', choices=('custody', 'local'), default='custody')
    a = ap.parse_args()
    try:
        a.fixture_root = require_synthetic(a.fixture_root)      # F11
        a.results_dir = require_synthetic(a.results_dir)
    except ValueError as exc:
        raise SystemExit(str(exc))
    os.makedirs(a.results_dir, exist_ok=True)
    suite_before = snapshot_tree(SUITE_DIR, skip=(SYNTHETIC_DIR, SUITE_DIR + '/PARTIAL.md'))
    GUARDED = [ART + '/s4rc1_c3/proof_side_c3v001', ART + '/s4rc1_c3/build_c3v001', ART + '/s4rc1_c3/build_c3v002']
    guarded_before = [snapshot_tree(p) for p in GUARDED]
    # c3v003: proof_side_c3v002 and build_c3v003 by every file their HASHES list (name, size, mtime). Their synthetic/
    # folders also hold the reviewer's own later runs (codex1_review_*), which this suite neither writes nor guards.
    HASHED = [(ART + '/s4rc1_c3/proof_side_c3v002', 'HASHES_C3V002.txt'), (ART + '/s4rc1_c3/build_c3v003', 'HASHES_C3V003.txt')]
    hashed_before = [hashed_snapshot(p, h) for p, h in HASHED]
    t0 = datetime.datetime.now(datetime.timezone.utc)
    W = World(a)
    spec_a = json.loads(open(REAL['spec_anchor'][0], 'rb').read())
    spec_c = json.loads(open(REAL['spec_corner000'][0], 'rb').read())
    if W.C.point_key(spec_a) != ANCHOR_KEY or W.C.point_key(spec_c) != CORNER000_KEY:
        raise SystemExit('point keys of the dry-plan specs differ from the 31-point table')
    W._corner_spec = spec_c
    A = make_point(W, 'ANCHOR', spec_a)
    Pc = make_point(W, 'CORNER000', spec_c)
    pair = anchor_pair(W, A)
    registered = [A.rho_pin, Pc.rho_pin] + pair
    # Slot proofs and prelaunch bundles used by the per-state and SRB tests.
    res_c = slot_prove(W, Pc, pair, registered)
    slot_pin_c = W.SLOT.write_proof(res_c, Pc.out)
    res_a = slot_prove(W, A, pair, registered)
    slot_pin_a = W.SLOT.write_proof(res_a, A.out)
    bundle_pin_c = W.fx.json(Pc.tag + '/bundle_prelaunch_main.json', bundle(W, Pc, slot_pin_c))
    bundle_pin_a = W.fx.json(A.tag + '/bundle_prelaunch_main.json', bundle(W, A, slot_pin_a))
    ensure_shared(W)
    W._cc_call = make_call(W, Pc, 'common')
    W._cc_bundle = bundle_pin_c
    W._anchor_bundle = bundle_pin_a
    # c3v003 harness: each group through group(), so an aborted group is one recorded failure (mutation check).
    group('tests_common', lambda: tests_common(W, A, Pc, pair, registered, slot_pin_c))
    slot_res = group('tests_slot', lambda: tests_slot(W, A, Pc, pair, registered))
    group('tests_wrapper_and_guard', lambda: tests_wrapper_and_guard(W, Pc, res_c, slot_pin_c))
    rec_l01 = group('tests_state', lambda: tests_state(W, A, Pc, pair, registered, slot_pin_c, bundle_pin_c, slot_pin_a,
                                                       bundle_pin_a))
    K_l01 = getattr(W, '_l01_call', None)
    group('tests_srb', lambda: tests_srb(W, A, Pc, pair, registered, bundle_pin_c))
    group('tests_c3v002', lambda: tests_c3v002(W, A, Pc, pair, registered, slot_pin_c, bundle_pin_c, rec_l01, K_l01))
    group('tests_wrapper_v002', lambda: tests_wrapper_v002(W, Pc, res_c, slot_pin_c, bundle_pin_c, rec_l01, K_l01))
    group('tests_c3v003_v02', lambda: tests_c3v003_v02(W, A, Pc, pair, registered, bundle_pin_c))       # c3v003 V02
    group('tests_c3v003_v03', lambda: tests_c3v003_v03(W, A, Pc, pair, registered, bundle_pin_c))       # c3v003 V03
    group('tests_c3v003_b3', lambda: tests_c3v003_b3(W, A, Pc, bundle_pin_c, bundle_pin_a))             # c3v003 B3
    record('H02_F11_nothing_written_outside_synthetic', 'MUST_PASS', 'F11 suite outputs only under synthetic/',
           snapshot_tree(SUITE_DIR, skip=(SYNTHETIC_DIR, SUITE_DIR + '/PARTIAL.md')) == suite_before,
           'the suite folder outside synthetic/ (and the append-only PARTIAL.md) is unchanged', len(suite_before))
    record('H03_c3v001_and_c3v002_tooling_untouched', 'MUST_PASS', 'hygiene: proof_side_c3v001, build_c3v001, build_c3v002 unchanged',
           [snapshot_tree(p) for p in GUARDED] == guarded_before, 'names, sizes and mtimes unchanged', [len(x) for x in guarded_before])
    record('H03b_proof_side_c3v002_and_build_c3v003_untouched', 'MUST_PASS',
           'hygiene: proof_side_c3v002 and build_c3v003 unchanged (every HASHES-listed file)',
           [hashed_snapshot(p, h) for p, h in HASHED] == hashed_before and all(len(x) > 1000 for x in hashed_before),
           'names, sizes and mtimes of every listed file unchanged', [len(x) for x in hashed_before])
    t1 = datetime.datetime.now(datetime.timezone.utc)
    mp = [r for r in RESULTS if r['kind'] == 'MUST_PASS']
    mf = [r for r in RESULTS if r['kind'] == 'MUST_FAIL']
    summary = {'schema': 'S4RC1_PROOF_SIDE_TEST_RESULTS_C3V003', 'utc_start': t0.strftime('%Y-%m-%dT%H:%M:%SZ'),
               'utc_end': t1.strftime('%Y-%m-%dT%H:%M:%SZ'), 'reader': a.reader, 'fixture_root': W.fx.root,
               'modules': {k: {'path': W.paths[k], 'sha256': W.shas[k]} for k in W.paths},
               'suite': {'path': os.path.realpath(__file__), 'sha256': sha_file(os.path.realpath(__file__))},
               'real_inputs': {k: {'path': p, 'sha256': s} for k, (p, s) in REAL.items()},
               'counts': {'total': len(RESULTS), 'passed': sum(r['passed'] for r in RESULTS),
                          'MUST_PASS': len(mp), 'MUST_PASS_passed': sum(r['passed'] for r in mp),
                          'MUST_FAIL': len(mf), 'MUST_FAIL_passed': sum(r['passed'] for r in mf)},
               'failed_ids': [r['id'] for r in RESULTS if not r['passed']], 'results': RESULTS,
               'python': sys.version, 'flags': {'isolated': sys.flags.isolated, 'dont_write_bytecode': sys.flags.dont_write_bytecode},
               'background_qos': os.getpriority(4, 0) == 1, 'synthetic_fixture': SYN}
    out = os.path.join(os.path.realpath(a.results_dir), 'TEST_RESULTS_%s.json' % t1.strftime('%Y%m%dT%H%M%SZ'))
    with open(out, 'xb') as f:
        f.write(W.C.encode_record(summary))
    man = write_manifest(os.path.realpath(a.results_dir), W.fx.root, {'path': out, 'sha256': sha_file(out)})   # F11
    print(json.dumps({'results': out, 'sha256': sha_file(out), 'counts': summary['counts'], 'failed': summary['failed_ids'],
                      'synthetic_outputs_manifest': man}), flush=True)
    return 0 if not summary['failed_ids'] else 1


if __name__ == '__main__':
    sys.exit(main())
