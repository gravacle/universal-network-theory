"""PORT (ks_k3_chain_c2 G-wave c2v001): the c3v004 suite (wave-1 port) against KS3' and KS4' (runner/assembler c2v002).

S4-R-C1 c3v004 synthetic test suite (Claude3 builder; A122, A134, A138; distinct-lane review under A115).

c3v004 = every c3v003 r2 case that still applies, plus the A138 erratum cases:
- V09: the canonical wrapper pin is the published path calib_tail_readiness_cx2/v006r10_c4/
  calibration_orchestrator_cx2v006r10_c4_q5b1.py with the same sha 7a6af535. The suite never needs that file: every
  assembler call reads a byte-identical copy in a synthetic layout under its fixture root, through a test-only override
  of the assembler's own common module (A.C.PINS), and an audit hook records that the published path is never opened;
- V02: the common pin and the registry manifest's draft C1 state_enumerator are the b1 enumerator 4ca7f364;
- V03: the anchor pair record names wrapper v002's 10-key canonical comparison as the (a)4 rule, and a runner pair that
  differs only by 1 ulp in a diagnostic is refused end to end by the real slot proof c3v003, the canonical slot producer.
Two case ids follow the object they test: T_E01 (..._c3v003) and T_B12 (..._c3v004_pins). The c3v003 r2 description
follows.

r2 changes the harness only (no case, check or expectation changes): a failed L30 guard load, a missing anchor rho file
or a missing E2E proof is now a recorded case failure instead of a suite abort, so that the c3v003 mutation check
names the failing cases for every mutant. r1 (test_s4rc1_c3v003.py, 97118534) passed 286/286 and stays as written.

c3v003 = every c3v002 case that still applies (the LO_ENVELOPE bundle cases now run on LO_RHO_SLOT bundles, and the
verifier is the wrapper v002 replica with the guard that wrapper L30 loads), plus: the RHO stage and its HELD gate, the
two anchor attempts in separate processes, the (a)4 pair fed END TO END into the REAL slot proof c3v002 and then the
assembler and the offline verifier (wrapper v002 L145-191 executed from its 7a6af535 bytes), and the assembler's
LO_RHO_SLOT acceptance and refusals. Outputs only under <build dir>/synthetic/, with a SYNTHETIC_OUTPUTS_MANIFEST.
The c3v002 description follows.

c3v002 = the c3v001 suite minus its LO-only cases, plus the F1-F8 cases (CHANGES_C3V002.md maps every
hunk to its finding). FROM_CODEX/0679 holds LO: the LO facade and adapter are not part of c3v002, so their
mapping and recompute cases are dropped; their root-gate cases (T72-T74, T90-T92) still run against the
build_c3v001 files, loaded read-only by exact path and sha from bytes.
SYNTHETIC inputs only. No producer runs on a real point input, no run tree is read or listed,
nothing is launched. Real files that ARE read: the pinned source modules (import only, for the
R4 producer-pin checks; their top level only reads source bytes), the 31 dry-plan spec files
(bytes and point keys), EPS_CERT_V006 (anchor cross-check logic), guard v003 (its
verify_bundle runs on synthetic bundles), the r9 run config 721c7230 (a policy-pending C1, F3), and one
read-only report each from /usr/bin/memory_pressure and /usr/bin/vm_stat. Every fixture is created by
exclusive create under a NEW fixture root and carries 'synthetic_fixture'. MUST_FAIL cases must fail for
the stated reason; scheduler MUST_FAIL cases also assert the exact set of points started (F8).

Usage (under background QoS):
  taskpolicy -b PY -I -B test_s4rc1_c3v004.py --build-dir DIR --fixture-root NEW_DIR_UNDER_<DIR>/synthetic [--extra-root DIR]
"""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_k] = '1'
import argparse
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import math
import subprocess
import sys
import traceback
import types

SYN = 'S4RC1 c3v004 synthetic test fixture; not a measurement, not a review, not a ruling'
RESULTS = []
# 0679: the HELD LO facade and adapter of build_c3v001, loaded read-only by exact path and sha for the root-gate cases.
LO_FACADE_C3V001 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v001/lo_producer_c3v001.py',
                    'da27543a7f3f237415068e9e396b3dcdb578d00137b458a602d9c3eb0cd556d1')
LO_ADAPTER_C3V001 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v001/lo_envelope_adapter_c3v001.py',
                     '6c31a3087250bc859b91b97e440caa1c96bd6764cf1946cde4bc1f3a6949424b')
DROPPED_C3V001_LO_CASES = ('T62', 'T63', 'T64', 'T65', 'T66', 'T67', 'T68', 'T69', 'T70', 'T70b', 'T71', 'T75', 'T76',
                           'T77', 'T78', 'T79', 'T80', 'T81', 'T81b', 'T82', 'T83', 'T84a', 'T84', 'T85', 'T86', 'T87',
                           'T88', 'T89')

# c3v004 (A138): the V09 published wrapper path (never opened by this suite), its build copy (the source of the
# synthetic layout copy), and the V02 enumerator pins.
PUBLISHED_WRAPPER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/calib_tail_readiness_cx2/v006r10_c4/'
                     'calibration_orchestrator_cx2v006r10_c4_q5b1.py')
BUILD_WRAPPER = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/wrapper_q5/build_v002/v006r10_c4/'
                 'calibration_orchestrator_cx2v006r10_c4_q5b1.py')
WRAPPER_SHA = '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'
B1_ENUM = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4_acceptance_c2/offset_b1/consumed_states_b1_c2v001.py',
           '4ca7f3640bff6adc13d181a8045bec750681362595a9a9e71e643fa521af60f0')
V010_ENUM_SHA = 'e48cca3c35a3d6d3724f74b9407b91f006bd31f2f30f416f9c328ba9e4144ca2'
PUBLISHED_OPENS = []


def _audit_published(event, args):
    """V09: records every open() of the published wrapper path in this process (the suite must never need that file)."""
    if event != 'open' or not args or not isinstance(args[0], (str, bytes)):
        return
    try:
        p = os.fsdecode(args[0])
        if p == PUBLISHED_WRAPPER or os.path.abspath(p) == PUBLISHED_WRAPPER:
            PUBLISHED_OPENS.append(p)
    except Exception:
        pass


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def record(cid, kind, req, passed, expected, observed):
    RESULTS.append({'id': cid, 'kind': kind, 'requirement': req, 'passed': bool(passed),
                    'expected': expected, 'observed': str(observed)[:600]})


def must_fail(cid, req, fn, code):
    """Passes only if fn raises (or returns a failing result) whose text contains `code`."""
    try:
        out = fn()
    except Exception as exc:
        txt = type(exc).__name__ + ': ' + str(exc)
        record(cid, 'MUST_FAIL', req, code in txt, 'refusal containing ' + code, txt)
        return
    txt = json.dumps(out, default=str) if not isinstance(out, str) else out
    failed = isinstance(out, dict) and (out.get('ok') is False or out.get('verdict') in ('BLOCKED', 'UNAVAILABLE', 'DISAGREE')
                                        or out.get('facade_verdict') in ('BLOCKED', 'UNAVAILABLE'))
    record(cid, 'MUST_FAIL', req, failed and code in txt, 'failing result containing ' + code, txt)


def must_pass(cid, req, fn, check=lambda out: True, expected='ok'):
    try:
        out = fn()
        ok = check(out)
        record(cid, 'MUST_PASS', req, ok, expected, json.dumps(out, default=str)[:600])
        return out
    except Exception as exc:
        record(cid, 'MUST_PASS', req, False, expected, type(exc).__name__ + ': ' + str(exc) + ' | ' +
               traceback.format_exc(limit=3)[-400:])
        return None


def _safe(fn):
    try:
        return fn()
    except Exception as exc:
        return 'UNAVAILABLE: %s: %s' % (type(exc).__name__, exc)


def write_manifest(run_dir, results_pin):
    """One manifest of every file under the run folder, written last by exclusive create (the F11 rule)."""
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
            files.append({'path': os.path.relpath(p, run_dir), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    man = {'schema': 'S4RC1_C3V004_SYNTHETIC_OUTPUTS_MANIFEST', 'run_dir': run_dir, 'results': results_pin,
           'n_files': len(files), 'files': files, 'synthetic_fixture': SYN,
           'statement': ('Every file listed was written by the c3v004 synthetic suite or by a tool under test during it. All are '
                         'SYNTHETIC: none is a measurement, a review, a ruling or a record of any real computation. Runner '
                         'and assembler records here carry real point keys but synthetic custody and synthetic numbers. '
                         'Never register, pin or cite any of them as evidence.')}
    out = os.path.join(run_dir, 'SYNTHETIC_OUTPUTS_MANIFEST_C3V004.json')
    raw = (json.dumps(man, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    with open(out, 'xb') as f:
        f.write(raw)
    return {'path': out, 'sha256': hashlib.sha256(raw).hexdigest(), 'n_files': len(files)}


def hashed_snapshot(top, hashes_name):
    """c3v004 hygiene: (name, size, mtime) of every file the folder's own HASHES file lists, plus that HASHES file."""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build-dir', required=True)
    ap.add_argument('--fixture-root', required=True)
    ap.add_argument('--extra-root', action='append', default=[])
    ns = ap.parse_args()
    build = os.path.realpath(ns.build_dir)
    sys.addaudithook(_audit_published)                # c3v004 V09: any open() of the published wrapper is recorded
    R = load(build + '/cp1_runner_c3v004_ks3_c2v002.py', 't_runner')
    A = load(build + '/registry_assembler_c3v004_ks4_c2v002.py', 't_assembler')
    CANON_WRAPPER_PIN = tuple(A.C.PINS['wrapper_q5b1'])   # c3v004 V09: the canonical pin, before the test-only override
    C = R.C
    # The HELD LO files: exact bytes, no copy, no .pyc (load_exact compiles the hashed bytes in memory).
    F = C.load_exact(LO_FACADE_C3V001[0], LO_FACADE_C3V001[1], 't_lo_facade_c3v001')
    L = C.load_exact(LO_ADAPTER_C3V001[0], LO_ADAPTER_C3V001[1], 't_lo_adapter_c3v001')

    def snapshot(top):
        out = []
        for d, dirs, files in os.walk(top):
            dirs.sort()
            for n in sorted(files):
                st = os.lstat(os.path.join(d, n))
                out.append((os.path.relpath(os.path.join(d, n), top), st.st_size, st.st_mtime_ns))
        return out
    lane_before = sorted(os.listdir(C.LANE_ROOT))
    c3v001_before = snapshot(C.LANE_ROOT + '/build_c3v001')
    c3v002_before = snapshot(C.LANE_ROOT + '/build_c3v002')                  # c3v003 hygiene
    ps1_before = snapshot(C.LANE_ROOT + '/proof_side_c3v001')
    PS2_CODE = ('lo_slot_proof_c3v002.py', 'lo_state_proof_adapter_c3v002.py', 'srb_rot_adapter_c3v002.py')
    ps2_before = [C.sha256_file(C.LANE_ROOT + '/proof_side_c3v002/' + n) for n in PS2_CODE]
    # c3v004 hygiene: build_c3v003 and proof_side_c3v002 by every file their HASHES list (their synthetic/ folders also
    # hold the reviewer's own later runs, codex1_review_*, which this suite neither writes nor guards), and the proof side
    # c3v003 code by sha.
    HASHED = [(C.LANE_ROOT + '/build_c3v003', 'HASHES_C3V003.txt'), (C.LANE_ROOT + '/proof_side_c3v002', 'HASHES_C3V002.txt')]
    hashed_before = [hashed_snapshot(p, h) for p, h in HASHED]
    PS3_CODE = ('lo_slot_proof_c3v003.py', 'lo_state_proof_adapter_c3v003.py', 'srb_rot_adapter_c3v003.py')
    ps3_before = [C.sha256_file(C.LANE_ROOT + '/proof_side_c3v003/' + n) for n in PS3_CODE]
    GUARD_B1 = '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'
    ROOT_RULE = 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE'
    ROOTS = (C.ART,) + tuple(ns.extra_root)
    GROOTS = None if not ns.extra_root else tuple(ns.extra_root) + (C.ART,)
    fx = ns.fixture_root
    if not (os.path.abspath(fx) + '/').startswith(build + '/synthetic/') or os.path.abspath(fx) == build + '/synthetic':
        raise SystemExit('REFUSED: c3v004 suite outputs go only under ' + build + '/synthetic/ (F11 rule): ' + fx)
    if os.path.exists(fx):
        raise SystemExit('fixture root must be new: ' + fx)
    os.makedirs(os.path.dirname(fx), exist_ok=True)
    os.mkdir(fx)
    fx = os.path.realpath(fx)
    C.require_policy(fx, ROOTS, 'fixture root')

    def W(rel, obj, raw=None):
        path = os.path.join(fx, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if isinstance(obj, dict):
            obj = dict(obj, synthetic_fixture=SYN) if 'synthetic_fixture' not in obj else obj
        return C.write_new(path, obj, fx, raw=raw)
    # c3v004 V09: the synthetic layout. A byte-identical copy of the wrapper v002 bytes (read from its build copy, sha
    # checked) stands at <fixture root>/layout_v09/calib_tail_readiness_cx2/v006r10_c4/, and ONLY the assembler's own
    # common module (A.C) is pointed at it. C (the runner's common, R.C) keeps the canonical published pin; no case opens it.
    with open(BUILD_WRAPPER, 'rb') as f:
        wraw = f.read()
    if hashlib.sha256(wraw).hexdigest() != WRAPPER_SHA:
        raise SystemExit('wrapper v002 build copy is not 7a6af535')
    LAYOUT_PIN = W('layout_v09/calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py', None,
                   raw=wraw)
    A.C.PINS['wrapper_q5b1'] = (LAYOUT_PIN['path'], WRAPPER_SHA)          # the test-only path override (V09)
    try:
        G = A.real_guard()                           # c3v003: the guard wrapper v002 L30 loads (b1 9e3fc109)
    except Exception as exc:                          # r2: recorded, then the b1 guard by its literal pin so cases still run
        record('T_B00_L30_guard_loads', 'MUST_PASS', 'guard binding follows wrapper v002 L30', False, 'the L30 guard loads',
               type(exc).__name__ + ': ' + str(exc))
        G = C.load_exact(C.ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', GUARD_B1, 't_guard_b1_fallback')

    def readpin(ref):
        return C.read_json_pinned(ref, ROOTS, 'fixture', max_bytes=None)

    def readraw(ref):
        return C.read_bytes_pinned(ref, ROOTS, 'fixture', max_bytes=None)

    # ------------------------------------------------------------------ shared synthetic world
    rows = C.point_rows()
    anchor, c000 = rows[0], rows[1]
    with open(anchor['spec_path'], 'rb') as f:
        spec = json.loads(f.read())
    ident = C.point_identity(spec)
    key = C.digest(ident)
    k16 = key[:16]
    custody = {k: hashlib.sha256(('synthetic ' + k).encode()).hexdigest() for k in
               ('grid_sha256', 'background_sha256', 'geometry_sha256', 'modules_sha256', 'row_contract_sha256')}
    csha = C.digest(custody)
    ids = ['R%02d' % i for i in range(1, 13)]
    radii = [float(i) * 3.0856775814913673e19 for i in range(1, 13)]
    tau = [0.4, 0.2, 0.175, 0.125, 0.1, 0.05, 0.05, 0.05, 0.075, 0.15, 0.175, 0.325]
    details = {'identity': ident, 'point_sha256': key, 'custody': custody, 'custody_sha256': csha,
               'row_contract': {'rows': [{'id': i, 'radius_m': r} for i, r in zip(ids, radii)], 'tau_km_s': tau}}
    ENV_RULE = C.EPS_ENVELOPE_RULE
    PR_PIN, AD_PIN, GQ_PIN = C.canonical_pin('response_producer'), C.canonical_pin('eps_adapter'), C.canonical_pin('gq_producer')
    LOCORE_PIN = C.canonical_pin('lo_core')

    def eps_numeric(settings='registered', full=True, ident_=None, custody_=None, end=182):
        shells = []
        for n in range(4, end):
            e = 1e-4 / (n - 3)
            shells.append({'range_inverse_kpc': [float(n), float(n + 1)], 'lo_inverse_kpc': float(n),
                           'hi_inverse_kpc': float(n + 1), 'eps': e, 'eps_envelope': e, 'eps_base': 0.5 * e,
                           'eps_refined': 0.5 * e, 'refinements': 0, 'certified': True, 'actual': {'estimate': 0.9 * e}})
        return {'schema': 'UNT_POINT_EPS_NUMERICAL_CX2V001', 'gate': 'EPS', 'status': 'TESTED',
                'identity': ident_ or ident, 'point_sha256': C.digest(ident_ or ident), 'custody': custody_ or custody,
                'producer': PR_PIN, 'settings': settings, 'full_registered_search_executed': full,
                'coverage_complete': full, 'registered_discrete_verdict': 'CERTIFIED',
                'verdict': 'NUMERICAL_RULE_PASSED_REVIEW_REQUIRED', 'shells': shells,
                'envelope_audit': [{'range_inverse_kpc': [float(n), float(n + 1)]} for n in (4, 5, 6, 8, 12, 16, 19, 32, 45, 63, 64, 100, 128, 181)],
                'eps_max': 1e-4, 'eps_max_shell': [4.0, 5.0], 'seconds': 1.0, 'peak_rss_bytes': 1}

    STUB_N = [0]
    RHO_PART = [[4.0, 5.0], [5.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0], [64.0, 128.0],
                [128.0, 182.0]]                       # c3v003: written out here, independent of the runner constant

    def rho_numeric(ident_, key_, *, settings='registered', rhos=None, partition=None, custody_=None, producer=None):
        part = partition or RHO_PART
        rhos = rhos or [0.02 - 0.001 * i for i in range(len(part))]
        shells = [{'range_inverse_kpc': list(p), 'rho_used': r, 'rho_envelope': {'estimate': r, 'seed': 20261018 + i,
                   'estimator_scope': 'synthetic'}, 'sampled_levels': [{'level': 1, 'estimate': 0.5 * r, 'n_samples': 10}]}
                  for i, (p, r) in enumerate(zip(part, rhos))]
        return {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'utc': '2026-10-19T00:00:00Z', 'status': 'TESTED',
                'identity': ident_, 'point_sha256': key_, 'custody': custody_ or custody, 'producer': producer or PR_PIN,
                'dependencies': {}, 'settings': settings, 'point_symbol_checks': {}, 'rigorous_supremum': False,
                'production_admissible': False, 'covers_all_consumed_states': False, 'limitation': 'synthetic',
                'gate': 'RHO_G', 'verdict': 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED', 'shells': shells, 'coverage_complete': True,
                'required_coverage_inverse_kpc': [4.0, 182.0], 'full_registered_search_executed': settings == 'registered',
                'seconds': 1.0, 'peak_rss_bytes': 1, 'synthetic_fixture': SYN}

    def eps_proof(slot, *, producer=AD_PIN, end=182, point=None, cs=None):
        rows_ = [{'range_inverse_kpc': [float(n), float(n + 1)], 'eps': 1e-4 / (n - 3), 'eps_envelope': 1e-4 / (n - 3),
                  'refinement_failures': 0} for n in range(4, end)]
        return {'schema': C.PROOF_SCHEMA, 'gate': 'EPS', 'status': 'TESTED', 'verdict': 'PASS',
                'point_sha256': point or key, 'custody_sha256': cs or csha, 'producer': producer,
                'driver_certificate': slot, 'numeric_evidence': slot, 'envelope_rule': ENV_RULE, 'shells': rows_}

    def gq_proof(*, producer=GQ_PIN, nodes=20736, full=True, point=None, cs=None):
        return {'schema': C.PROOF_SCHEMA, 'gate': 'GQ', 'status': 'TESTED', 'verdict': 'PASS',
                'point_sha256': point or key, 'custody_sha256': cs or csha, 'producer': producer,
                'method': 'GEOMETRY_UNIFORM_COLUMN_BOUND', 'all_columns_included': True,
                'all_production_kperp_nodes': full, 'nonnegative_masses_required': True, 'M_s': 128,
                'M_s_doubled': 256, 'K_big_inverse_kpc': 128.0, 'max_column_difference_over_analytic_Pi0': 3.0e-14,
                'max_zero_mode_relative_error': 3.5e-14, 'conservative_bound': 3.0e-14, 'nodes_tested': nodes,
                'production_nodes': 20736, 'seconds': 1.0}

    # ---------------------------------------------------------------- 1. tables, keys, policy, writer
    def all_keys():
        for r in rows:
            R.load_spec(r)
        return len(rows)
    must_pass('T01_points_31_keys_and_spec_pins', 'point key check', all_keys, lambda n: n == 31, '31 verified')
    bad_key = dict(anchor, key='0' * 64)
    must_fail('T02_point_mismatch_spec_key', 'custody or point mismatch', lambda: R.load_spec(bad_key), 'POINT_KEY_MISMATCH')
    bad_sha = dict(anchor, spec_sha256='f' * 64)
    must_fail('T03_spec_pin_mismatch', 'custody or point mismatch', lambda: R.load_spec(bad_sha), 'SPEC_PIN_MISMATCH')
    for i, (p, code) in enumerate((
            (C.LANE_ROOT + '/cp1_x/uvt_probe/a.json', 'UVT_COMPONENT_REFUSED'),
            (C.LANE_ROOT + '/cp1_x/UVT_A/a.json', 'UVT_COMPONENT_REFUSED'),
            (C.LANE_ROOT + '/cp1_ngc3198_x/a.json', 'NGC3198_COMPONENT_REFUSED'),
            (C.ART + '/kmax_a2f10_c5h_run_v001/a.json', 'C5H_COMPONENT_REFUSED'),
            ('/Users/bgm/Research/UNT_INTERNAL_RUNS/x.json', 'RUN_TREE_REFUSED'),
            (C.ART + '/runs_ext/x.json', 'RUN_TREE_REFUSED'),
            (C.ART + '/a/../b.json', 'PATH_NOT_NORMALIZED'))):
        must_fail('T04_policy_%d' % i, 'uvt_ path component' if 'UVT' in code else 'path policy',
                  lambda p=p: C.require_policy(p, (C.ART, '/Users/bgm/Research'), 'probe'), code)
    must_fail('T05_out_root_uvt', 'uvt_ path component', lambda: R.validate_out_root(C.LANE_ROOT + '/cp1_uvt_x/uvt_y'), 'UVT_COMPONENT_REFUSED')
    must_fail('T06_out_root_codex2_folder', 'own output folder', lambda: R.validate_out_root(C.CERT + '/cp1_x'), 'OUT_ROOT_MUST_BE')
    must_fail('T07_out_root_outside_lane', 'own output folder', lambda: R.validate_out_root(C.ART + '/cp1_x'), 'OUT_ROOT_MUST_BE')
    must_pass('T08_out_root_ok', 'own output folder', lambda: R.validate_out_root(C.LANE_ROOT + '/cp1_run_c3v001'))
    p1 = W('writer/once.json', {'a': 1})
    must_fail('T09_writer_exclusive', 'exclusive create', lambda: C.write_new(p1['path'], {'a': 2}, fx), 'File exists')
    must_fail('T10_writer_outside_root', 'exclusive create', lambda: C.write_new(C.ART + '/x.json', {'a': 1}, fx), 'OUTSIDE_ALLOWED_ROOTS')
    must_fail('T11_writer_uvt_name', 'uvt_ path component', lambda: C.write_new(fx + '/uvt_x.json', {'a': 1}, fx), 'UVT_COMPONENT_REFUSED')
    record('T12_writer_uvt_not_created', 'MUST_FAIL', 'uvt_ path component', not os.path.exists(fx + '/uvt_x.json'),
           'no uvt_ file created', os.path.exists(fx + '/uvt_x.json'))

    # ---------------------------------------------------------------- 2. memory gate, QoS, interpreter
    sample = 'The system has 137438953472 (8388608 pages with a page size of 16384).\nSystem-wide memory free percentage: 63%\n'
    must_pass('T13_memory_parse', 'memory gate', lambda: C.parse_memory_pressure(sample), lambda v: v == 63, '63')
    must_fail('T14_memory_parse_two_lines', 'memory gate', lambda: {'ok': C.parse_memory_pressure(sample + sample) is not None,
              'why': 'MALFORMED_REFUSED'}, 'MALFORMED_REFUSED')
    must_pass('T15_memory_gate_28_margin3', 'memory gate', lambda: C.memory_gate(28, 3), lambda v: v[0] is True)
    must_fail('T16_memory_gate_27_margin3', 'memory gate', lambda: {'ok': C.memory_gate(27, 3)[0], 'why': C.memory_gate(27, 3)[1]}, 'MEMORY_BELOW_GATE')
    must_fail('T17_memory_gate_25_no_margin', 'memory gate', lambda: {'ok': C.memory_gate(25, 0)[0], 'why': C.memory_gate(25, 0)[1]}, 'MEMORY_MARGIN_INVALID')
    must_fail('T18_memory_gate_none', 'memory gate', lambda: {'ok': C.memory_gate(None, 5)[0], 'why': C.memory_gate(None, 5)[1]}, 'MEMORY_METRIC_UNAVAILABLE')
    must_pass('T19_memory_pressure_live_read_only', 'memory gate', C.memory_free_percent, lambda v: type(v) is int and 0 <= v <= 100,
              'int percent from /usr/bin/memory_pressure (no arguments)')
    must_pass('T20_swapusage_parse', 'memory gate', lambda: C.parse_swapusage('total = 3072.00M  used = 1869.25M  free = 1202.75M  (encrypted)'),
              lambda v: v == 1869.25)
    py = sys.executable
    # H1: the probe sets sys.dont_write_bytecode (sys.flags are unchanged), so T23's deliberate no -I/-B run
    # still tests the refusal but writes no .pyc into the build folder (c3v001 hand-back housekeeping note).
    probe = ("import importlib.util,sys;sys.dont_write_bytecode=True;sp=importlib.util.spec_from_file_location('r',%r);"
             "m=importlib.util.module_from_spec(sp);"
             "sp.loader.exec_module(m)\ntry:\n m.require_compute_environment();print('ENV_OK')\nexcept m.Refusal as e:print('REFUSED',e)") % (build + '/cp1_runner_c3v004_ks3_c2v002.py')
    unbg = ['-I', '-B', '-c', 'import os,sys; os.setpriority(4,0,0); os.execv(sys.argv[1], sys.argv[1:])', py]
    nobg = subprocess.run([py] + unbg + ['-I', '-B', '-c', probe], capture_output=True, text=True, timeout=120)
    record('T21_no_background_qos_refused', 'MUST_FAIL', 'taskpolicy -b', 'BACKGROUND_QOS_REQUIRED' in nobg.stdout,
           'refusal BACKGROUND_QOS_REQUIRED', nobg.stdout + nobg.stderr[-300:])
    bg = subprocess.run([C.TASKPOLICY, '-b', py, '-I', '-B', '-c', probe], capture_output=True, text=True, timeout=120)
    record('T22_background_qos_accepted', 'MUST_PASS', 'taskpolicy -b', 'ENV_OK' in bg.stdout, 'ENV_OK', bg.stdout + bg.stderr[-300:])
    noiso = subprocess.run([C.TASKPOLICY, '-b', py, '-c', probe], capture_output=True, text=True, timeout=120)
    record('T23_not_isolated_refused', 'MUST_FAIL', 'python3 -I -B', 'ISOLATED_INTERPRETER_REQUIRED' in noiso.stdout,
           'refusal ISOLATED_INTERPRETER_REQUIRED', noiso.stdout + noiso.stderr[-300:])
    cli = subprocess.run([C.TASKPOLICY, '-b', py, '-I', '-B', build + '/cp1_runner_c3v004_ks3_c2v002.py', 'run', '--out-root',
                          C.LANE_ROOT + '/cp1_never_created', '--operator-lane', 'X', '--settings', 'smoke'],
                         capture_output=True, text=True, timeout=120)
    record('T24_cli_has_no_smoke_option', 'MUST_FAIL', 'smoke or partial', cli.returncode == 2 and 'unrecognized arguments' in cli.stderr,
           'argparse refusal', cli.stderr[-300:])
    cli2 = subprocess.run([py] + unbg + ['-I', '-B', build + '/cp1_runner_c3v004_ks3_c2v002.py', 'worker', '--out-root',
                           C.LANE_ROOT + '/cp1_never_created', '--point', anchor['key'], '--operator-lane', 'X'],
                          capture_output=True, text=True, timeout=120)
    record('T25_cli_worker_without_bg_refused_first', 'MUST_FAIL', 'taskpolicy -b',
           cli2.returncode == 2 and 'BACKGROUND_QOS_REQUIRED' in cli2.stdout and not os.path.exists(C.LANE_ROOT + '/cp1_never_created'),
           'exit 2, nothing created', cli2.stdout[-300:])
    cli3 = subprocess.run([C.TASKPOLICY, '-b', py, '-I', '-B', build + '/cp1_runner_c3v004_ks3_c2v002.py', 'run', '--out-root',
                           C.LANE_ROOT + '/cp1_x/uvt_y', '--operator-lane', 'X'], capture_output=True, text=True, timeout=120)
    record('T26_cli_uvt_out_root_refused', 'MUST_FAIL', 'uvt_ path component',
           cli3.returncode == 2 and 'UVT_COMPONENT_REFUSED' in cli3.stdout and not os.path.exists(C.LANE_ROOT + '/cp1_x'),
           'exit 2, nothing created', cli3.stdout[-300:])
    for cid, kw, code in (('T27_settings_smoke', dict(settings='smoke'), 'SMOKE_OR_UNREGISTERED_SETTINGS_REFUSED'),
                          ('T28_partial_shells', dict(shell_ranges=[[4.0, 5.0]]), 'PARTIAL_SHELL_SELECTION_REFUSED'),
                          ('T29_gq_node_limit', dict(node_limit=128), 'PARTIAL_GQ_NODE_LIMIT_REFUSED')):
        must_fail(cid, 'smoke or partial', lambda kw=kw: R.run_point(anchor, fx, operator_lane='X', **kw), code)

    # ---------------------------------------------------------------- 3. R4: canonical producer pins (import only)
    def r4():
        gq = C.load_pinned('gq_producer', 't_r4_gq')
        ad = C.load_pinned('eps_adapter', 't_r4_adapter')
        pr = C.load_pinned('response_producer', 't_r4_pr')
        return {'gq': gq.C.pin(gq.__file__) == GQ_PIN, 'eps_adapter': ad.CU.pin(ad.__file__) == AD_PIN,
                'response': pr.CU.pin(pr.__file__) == PR_PIN}
    must_pass('T30_R4_canonical_import_pins', 'R4 canonical producer pins', r4, lambda d: all(d.values()), 'all True')
    alias = C.CERT + '/../certificates_per_point/gq_producer_cx2v005.py'
    must_fail('T31_R4_alias_path_refused', 'R4 canonical producer pins', lambda: C.load_exact(alias, GQ_PIN['sha256'], 't_alias'), 'NONCANONICAL_PATH')

    def alias_hazard():
        spec_ = importlib.util.spec_from_file_location('t_alias_raw', alias)
        m = importlib.util.module_from_spec(spec_)
        spec_.loader.exec_module(m)
        pin = m.C.pin(m.__file__)
        return {'ok': pin in [GQ_PIN], 'alias_pin_path': pin['path'], 'why': 'WHOLE_DICT_PIN_MISMATCH_UNDER_ALIAS_IMPORT'}
    must_fail('T32_R4_alias_import_breaks_whole_dict_pin', 'R4 canonical producer pins', alias_hazard, 'WHOLE_DICT_PIN_MISMATCH')

    # ---------------------------------------------------------------- 4. runner worker with stub producers
    out_root = os.path.join(fx, 'runner_out')
    os.mkdir(out_root)

    def stub_loader(row=anchor, gq_override=None, eps_override=None, pins_override=None, trace=None, rho_override=None,
                    rho_trace=None):
        with open(row['spec_path'], 'rb') as f:
            rid = C.point_identity(json.loads(f.read()))

        def produce(spec_, node_limit=None, progress=None):
            if trace is not None:
                trace.append('GQ')                    # F6 cases: did the point proceed past CONTEXT?
            g = gq_proof(point=row['key'])
            g.update(gq_override or {})
            return g

        def point_context(spec_):
            return {'details': {'point_sha256': row['key'], 'custody': custody, 'custody_sha256': csha, 'identity': rid},
                    'source_pins': dict({'producer': PR_PIN}, **(pins_override or {})), 'checks': {'anchor_bitwise': True}}

        def produce_eps(spec_, settings='registered', shell_ranges=None, context=None, progress=None):
            for n in (4, 5, 6):
                progress({'shell': [float(n), float(n + 1)], 'eps': 1e-4, 'refinements': 0})
            e = eps_numeric(ident_=rid)
            e.update(eps_override or {})
            return e

        def produce_rho(spec_, settings='registered', shell_ranges=None, context=None, progress=None):
            if rho_trace is not None:                 # c3v003: the RHO stage call contract
                rho_trace.append({'settings': settings, 'shell_ranges': shell_ranges, 'context': context})
            for sh in RHO_PART[:3]:
                progress({'shell': sh, 'rho': 0.02})
            r = rho_numeric(rid, row['key'], settings=settings)
            STUB_N[0] += 1                            # run metadata differs per run, as in produce_rho (utc, seconds)
            r['utc'], r['seconds'] = C.utc(), float(STUB_N[0])
            if callable(rho_override):
                r = rho_override(r)
            elif rho_override:
                r.update(rho_override)
            return r
        return lambda: (types.SimpleNamespace(produce=produce),
                        types.SimpleNamespace(point_context=point_context, produce_eps=produce_eps, produce_rho=produce_rho))

    rc_sum = must_pass('T33_worker_stub_point_done', 'runner GQ+EPS stages',
                       lambda: R.run_point(anchor, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader()),
                       lambda v: v[0] == 0 and v[1].get('done') is True, 'exit 0, POINT_DONE')
    pdir = os.path.join(out_root, R.point_dir_name(anchor, 1))

    def stage_files():
        names = sorted(os.listdir(pdir))
        st = json.load(open(os.path.join(pdir, 'STAGE_EPS_%s.json' % k16)))
        sg = json.load(open(os.path.join(pdir, 'STAGE_GQ_%s.json' % k16)))
        return {'names': names, 'eps_seconds': st.get('seconds'), 'eps_rss': st.get('peak_rss_bytes_process_high_water'),
                'gq_seconds': sg.get('seconds'), 'gq_rss': sg.get('peak_rss_bytes_process_high_water'),
                'checks': st['checks'], 'gq_checks': sg['checks']}
    must_pass('T34_stage_metrics_recorded', 'seconds and peak RSS per stage', stage_files,
              lambda d: all(isinstance(d[k], (int, float)) for k in ('eps_seconds', 'eps_rss', 'gq_seconds', 'gq_rss'))
              and all(d['checks'].values()) and all(d['gq_checks'].values()) and
              {'POINT_START_%s.json' % k16, 'STAGE_CONTEXT_%s.json' % k16, 'GQ_PROOF_%s.json' % k16, 'STAGE_GQ_%s.json' % k16,
               'EPS_PROGRESS_%s.jsonl' % k16, 'EPS_NUMERIC_%s.json' % k16, 'STAGE_EPS_%s.json' % k16,
               'EPS_REVIEW_REQUEST_%s.json' % k16, 'POINT_DONE_%s.json' % k16, 'STAGE_RHO_HELD_%s.json' % k16} <= set(d['names']),
              'all stage files (c3v003: plus STAGE_RHO_HELD, the gate is closed)')
    must_fail('T35_rerun_same_attempt_refused', 'exclusive create',
              lambda: R.run_point(anchor, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader()), 'POINT_DIR_EXISTS_NOT_RERUN')
    gq_fail = must_pass('T36_gq_fail_recorded_and_point_stopped', 'runner GQ+EPS stages',
                        lambda: R.run_point(c000, out_root, operator_lane='SYNTHETIC_OPERATOR',
                                            loader=stub_loader(c000, {'verdict': 'FAIL'})),
                        lambda v: v[0] == 3 and v[1].get('stopped') == 'GQ', 'exit 3 at GQ; EPS skipped')
    c000dir = os.path.join(out_root, R.point_dir_name(c000, 1))
    record('T37_no_eps_after_gq_fail', 'MUST_FAIL', 'runner GQ+EPS stages',
           not any(n.startswith('EPS_') for n in os.listdir(c000dir)) and any(n.startswith('POINT_STOP') for n in os.listdir(c000dir)),
           'POINT_STOP and no EPS files', sorted(os.listdir(c000dir)))
    row3 = rows[2]
    must_pass('T38_R4_noncanonical_gq_producer_stops_point', 'R4 canonical producer pins',
              lambda: R.run_point(row3, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(
                  row3, {'producer': {'path': C.CERT + '/./gq_producer_cx2v005.py', 'sha256': GQ_PIN['sha256']}})),
              lambda v: v[0] == 3 and v[1].get('stopped') == 'GQ', 'exit 3 (producer_pin_canonical_R4 False)')

    row4 = rows[3]
    must_pass('T38b_source_pin_drift_stops_point', 'custody or point mismatch (upstream drift)',
              lambda: R.run_point(row4, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(
                  row4, pins_override={'reference_lwr_common': {'path': '/x', 'sha256': '5' * 64}})),
              lambda v: v[0] == 3 and v[1].get('stopped') == 'CONTEXT', 'exit 3 at CONTEXT (source pins differ from the anchor)')
    row5 = rows[4]
    must_pass('T38c_source_pins_match_anchor_control', 'custody or point mismatch (upstream drift) control',
              lambda: R.run_point(row5, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(row5)),
              lambda v: v[0] == 0, 'exit 0 with source_pins_match_anchor True')

    # ---------------------------------------------------------------- 4b. F4 thread env, F5 point folder, F6 anchor context
    recs = {n: json.load(open(os.path.join(pdir, n))) for n in sorted(os.listdir(pdir)) if n.endswith('.json')}
    stage_recs = [v for n, v in recs.items() if n.startswith('STAGE_')]
    record('T_F4_01_stage_records_carry_thread_env_and_parent', 'MUST_PASS', 'F4 single-thread BLAS enforced by override at import',
           len(stage_recs) == 4 and all(v.get('thread_env_parent') == R.PARENT_THREAD_ENV and set(v.get('thread_env', {}).values()) == {'1'}
                                        and str(v.get('thread_env_rule', '')).startswith('ENFORCED_BY_OVERRIDE_AT_IMPORT') for v in stage_recs)
           and recs['POINT_START_%s.json' % k16].get('thread_env_parent') == R.PARENT_THREAD_ENV,
           'POINT_START and the 3 STAGE records carry thread_env (all 1), thread_env_parent and the override rule',
           [(v.get('stage'), v.get('thread_env_parent')) for v in stage_recs])
    f4_root = os.path.join(fx, 'f4_out')
    os.mkdir(f4_root)
    f4_probe = ("import importlib.util,json,os,sys,types\nsys.dont_write_bytecode=True\n"
                "sp=importlib.util.spec_from_file_location('r',sys.argv[1]);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)\n"
                "row=m.C.point_rows()[0];k16=row['key'][:16];cust={'synthetic':'custody'}\n"
                "pc=lambda s:{'details':{'point_sha256':'0'*64,'custody':cust,'custody_sha256':m.C.digest(cust)},'source_pins':{},'checks':{}}\n"
                "ld=lambda:(types.SimpleNamespace(produce=None),types.SimpleNamespace(point_context=pc,produce_eps=None))\n"
                "rc,s=m.run_point(row,sys.argv[2],operator_lane='SYNTHETIC_OPERATOR',loader=ld)\n"
                "d=os.path.join(sys.argv[2],m.point_dir_name(row,1))\n"
                "st=json.load(open(os.path.join(d,'STAGE_CONTEXT_%s.json'%k16)));ps=json.load(open(os.path.join(d,'POINT_START_%s.json'%k16)))\n"
                "print(json.dumps({'rc':rc,'stopped':s.get('stopped'),'in_process':m.C.single_thread_env(),'module_parent':m.PARENT_THREAD_ENV,"
                "'stage_thread_env':st.get('thread_env'),'stage_parent':st.get('thread_env_parent'),'start_parent':ps.get('thread_env_parent')}))\n")
    f4 = subprocess.run([C.TASKPOLICY, '-b', py, '-I', '-B', '-c', f4_probe, build + '/cp1_runner_c3v004_ks3_c2v002.py', f4_root],
                        capture_output=True, text=True, timeout=300, env=dict(os.environ, **{k: '8' for k in C.THREAD_ENV}))

    def f4_check():
        if not f4.stdout.strip():
            raise RuntimeError('probe printed nothing: ' + f4.stderr[-500:])
        v = json.loads(f4.stdout.strip().splitlines()[-1])
        one, eight = {k: '1' for k in C.THREAD_ENV}, {k: '8' for k in C.THREAD_ENV}
        return dict(v, passed=(v['rc'] == 3 and v['stopped'] == 'CONTEXT' and v['in_process'] == one and
                               v['stage_thread_env'] == one and v['module_parent'] == eight and
                               v['stage_parent'] == eight and v['start_parent'] == eight))
    must_pass('T_F4_02_parent_env_8_gives_1_in_process_and_8_recorded', 'F4 single-thread BLAS enforced by override at import',
              f4_check, lambda v: v['passed'], 'subprocess under taskpolicy -b -I -B, all six = 8: in-process 1, parent 8 recorded')

    def post_import_change():
        prev = os.environ.get('OMP_NUM_THREADS')
        os.environ['OMP_NUM_THREADS'] = '8'
        try:
            R.require_compute_environment()
            return {'ok': True, 'why': 'NO_REFUSAL'}
        finally:
            if prev is None:
                del os.environ['OMP_NUM_THREADS']
            else:
                os.environ['OMP_NUM_THREADS'] = prev
    must_fail('T_F4_03_in_process_check_is_an_invariant_of_the_override', 'F4 single-thread BLAS enforced by override at import',
              post_import_change, 'SINGLE_THREAD_BLAS_ENV_REQUIRED')

    f5_target = os.path.join(fx, 'f5_symlink_target')
    os.mkdir(f5_target)
    f5_link = os.path.join(fx, 'f5_symlinked_out_root')
    os.symlink(f5_target, f5_link)
    must_fail('T_F5_01_symlinked_out_root_refused_before_mkdir', 'F5 output-folder confinement',
              lambda: R.run_point(anchor, f5_link, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader()),
              'OUTPUT_PARENT_NOT_CANONICAL (realpath differs; no point folder created)')
    record('T_F5_02_nothing_created_in_symlink_target', 'MUST_FAIL', 'F5 output-folder confinement', os.listdir(f5_target) == [],
           'no point folder created through the symlink', os.listdir(f5_target))

    a_dir = R.point_dir_name(anchor, 1)
    a_ctx = 'STAGE_CONTEXT_%s.json' % k16
    a_ctx_ok = {'schema': R.STAGE_SCHEMA, 'stage': 'CONTEXT', 'key': key, 'source_pins': {'producer': PR_PIN}}

    def f6(name, files=(), attempts=(1,), on_first_sleep=()):
        """HEADLINE_CORNER_000 in its own out-root beside a synthetic anchor folder; returns what the point did."""
        root = os.path.join(fx, 'f6_' + name)
        os.mkdir(root)
        for a in attempts:
            os.mkdir(os.path.join(root, R.point_dir_name(anchor, a)))
        for fname, obj, raw in files:
            W('f6_%s/%s/%s' % (name, a_dir, fname), obj, raw=raw)
        trace, sleeps = [], []

        def sleeper(_):
            sleeps.append(1)
            if len(sleeps) > 3:
                raise RuntimeError('HOLD_DID_NOT_END')
            if len(sleeps) == 1:
                for fname, obj, raw in on_first_sleep:
                    W('f6_%s/%s/%s' % (name, a_dir, fname), obj, raw=raw)
        rc, summ = R.run_point(c000, root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(c000, trace=trace),
                               hold_poll_seconds=0.0, hold_sleep=sleeper)
        cdir = os.path.join(root, R.point_dir_name(c000, 1))
        ctx = json.load(open(os.path.join(cdir, 'STAGE_CONTEXT_%s.json' % c000['key'][:16])))
        return {'rc': rc, 'stopped': summ.get('stopped'), 'reason': summ.get('reason'), 'gq_called': 'GQ' in trace,
                'sleeps': len(sleeps), 'later_files': [n for n in sorted(os.listdir(cdir)) if n.startswith(('GQ_', 'STAGE_GQ', 'EPS_'))],
                'anchor_context': ctx['checks_info'].get('anchor_context'), 'hold': ctx['checks_info'].get('anchor_context_hold'),
                'checks': ctx['checks']}

    def f6_refused(v, sleeps):
        """MUST_FAIL helper: stopped at CONTEXT, GQ never called, no later file, exactly `sleeps` hold polls."""
        good = (v['rc'] == 3 and v['stopped'] == 'CONTEXT' and not v['gq_called'] and not v['later_files']
                and v['sleeps'] == sleeps)
        return dict(v, ok=False if good else 'POINT_PROCEEDED_OR_UNEXPECTED_HOLD')
    start_only = [('POINT_START_%s.json' % k16, {'schema': 'S4RC1_CP1_POINT_START_C3V002'}, None)]
    stop_rec = ('POINT_STOP_%s.json' % k16, {'schema': 'S4RC1_CP1_POINT_STOP_C3V002', 'stage': 'REFUSAL'}, None)
    must_fail('T_F6_01_held_then_anchor_stops_point_stops', 'F6 anchor context before a non-anchor point proceeds',
              lambda: f6_refused(f6('hold_then_stop', start_only, on_first_sleep=[stop_rec]), 1),
              'ANCHOR_CONTEXT_RECORD_UNAVAILABLE: ANCHOR_ENDED_WITHOUT_A_READABLE_CONTEXT_RECORD (POINT_STOP)')
    must_pass('T_F6_02_held_until_anchor_context_exists_then_proceeds', 'F6 anchor context before a non-anchor point proceeds',
              lambda: f6('hold_then_ctx', start_only, on_first_sleep=[(a_ctx, a_ctx_ok, None)]),
              lambda v: v['rc'] == 0 and v['gq_called'] and v['sleeps'] == 1 and v['anchor_context'] == 'PRESENT'
              and v['hold']['polls'] == 1 and v['checks'].get('source_pins_match_anchor') is True,
              'holds one poll, then compares source pins and runs GQ and EPS')
    must_fail('T_F6_03_two_anchor_attempts_refused', 'F6 anchor context before a non-anchor point proceeds',
              lambda: f6_refused(f6('two_attempts', [(a_ctx, a_ctx_ok, None)], attempts=(1, 2)), 0), 'ANCHOR_ATTEMPTS_AMBIGUOUS')
    must_fail('T_F6_04_no_anchor_attempt_refused', 'F6 anchor context before a non-anchor point proceeds',
              lambda: f6_refused(f6('no_anchor', attempts=()), 0), 'ANCHOR_NOT_STARTED_IN_THIS_OUT_ROOT')
    must_fail('T_F6_05_anchor_stopped_before_context_refused', 'F6 anchor context before a non-anchor point proceeds',
              lambda: f6_refused(f6('anchor_stopped', [stop_rec]), 0), 'ANCHOR_ENDED_WITHOUT_A_READABLE_CONTEXT_RECORD (POINT_STOP)')
    must_fail('T_F6_06_torn_anchor_context_after_anchor_ended_refused', 'F6 anchor context before a non-anchor point proceeds',
              lambda: f6_refused(f6('anchor_ctx_torn', [(a_ctx, None, b'{"stage": "CONTEXT", "source_pi'), stop_rec]), 0),
              'ANCHOR_ENDED_WITHOUT_A_READABLE_CONTEXT_RECORD (POINT_STOP)')

    # ---------------------------------------------------------------- 5. adapt-eps gating (stub adapter)
    st_eps = json.load(open(os.path.join(pdir, 'STAGE_EPS_%s.json' % k16)))
    numeric_ref = st_eps['record']
    calls = []

    def stub_adapter():
        def adapt_eps(spec_, nref, *, review_ref=None, approved_producer_sha256=(), approved_review_sha256=()):
            calls.append(review_ref)
            proof = eps_proof(nref)
            return {'verdict': 'READY_FOR_MANIFEST', 'proof': proof, 'driver_certificate': nref, 'blockers': []}
        return types.SimpleNamespace(adapt_eps=adapt_eps)

    good_review = {'schema': 'UNT_POINT_EPS_REVIEW_CX2V001', 'verdict': 'APPROVED', 'numeric_ref': numeric_ref,
                   'point_sha256': key, 'custody_sha256': csha, 'adapter_sha256': AD_PIN['sha256'],
                   'accepts_registered_numerical_estimate_not_rigorous_sup': True,
                   'reviewer_lane': 'SYNTHETIC_REVIEWER_LANE', 'distinct_from_producer_lane': True}

    def review_file(name, **chg):
        r = dict(good_review, **chg)
        return W('reviews/' + name, r)

    def adapt(rpin, signers=('SYNTHETIC_REVIEWER_LANE',), approved=None):
        return R.adapt_point(anchor, out_root, review_path=None if rpin is None else rpin['path'],
                             approved_review_sha256=approved or (rpin or {}).get('sha256'),
                             approved_signer_lanes=list(signers), adapter_loader=stub_adapter,
                             review_roots=ROOTS + (C.EXCHANGE,))

    must_fail('T39_review_missing', 'missing or non-distinct review', lambda: adapt(None), 'EPS_REVIEW_MISSING')
    must_fail('T40_review_operator_lane', 'missing or non-distinct review',
              lambda: adapt(review_file('op.json', reviewer_lane='SYNTHETIC_OPERATOR'), signers=('SYNTHETIC_OPERATOR',)), 'REVIEW_NOT_DISTINCT')
    must_fail('T41_review_producer_lane_codex2', 'missing or non-distinct review',
              lambda: adapt(review_file('cx2.json', reviewer_lane='Codex2'), signers=('Codex2',)), 'REVIEW_NOT_DISTINCT')
    must_fail('T42_review_not_asserting_distinct', 'missing or non-distinct review',
              lambda: adapt(review_file('nd.json', distinct_from_producer_lane=False)), 'REVIEW_DOES_NOT_ASSERT_DISTINCT_LANE')
    must_fail('T43_review_template_unfilled', 'missing or non-distinct review',
              lambda: adapt(review_file('tpl.json', verdict='TEMPLATE_NOT_A_REVIEW', reviewer_lane='<FILL: lane>')), 'REVIEW_IS_AN_UNFILLED_TEMPLATE')
    must_fail('T44_review_sha_not_root_approved', 'missing or non-distinct review',
              lambda: adapt(review_file('sha.json'), approved='0' * 64), 'EPS_REVIEW_SHA_NOT_ROOT_APPROVED')
    must_fail('T45_review_signer_not_approved', 'missing or non-distinct review',
              lambda: adapt(review_file('sig.json'), signers=('SOMEONE_ELSE',)), 'REVIEWER_LANE_NOT_ROOT_APPROVED_SIGNER')
    must_fail('T46_review_no_signers', 'missing or non-distinct review', lambda: adapt(review_file('nos.json'), signers=()), 'NO_ROOT_APPROVED_SIGNER_LANES')
    must_fail('T47_review_binds_other_bytes', 'missing or non-distinct review',
              lambda: adapt(review_file('other.json', numeric_ref={'path': numeric_ref['path'], 'sha256': '1' * 64})), 'EPS_REVIEW_FIELD_MISMATCH: numeric_ref')
    inside = C.write_new(os.path.join(out_root, 'REVIEW_INSIDE_OUT_ROOT.json'), dict(good_review, synthetic_fixture=SYN), out_root)
    must_fail('T48_review_inside_runner_root', 'tool never approves its own output',
              lambda: adapt(inside), 'REVIEW_INSIDE_RUNNER_OUTPUT_ROOT')
    record('T49_adapter_not_called_on_refusals', 'MUST_FAIL', 'missing or non-distinct review', calls == [],
           'adapt_eps never called', len(calls))
    must_pass('T50_review_ok_adapt_eps_called', 'missing or non-distinct review (control)',
              lambda: adapt(review_file('good.json')), lambda v: v[0] == 0 and 'eps_proof' in v[1], 'exit 0, EPS_PROOF written')
    must_fail('T50b_second_adapt_same_attempt_refused', 'exclusive create', lambda: adapt(review_file('good2.json')), 'EPS_PROOF_EXISTS')

    # ---------------------------------------------------------------- 6. anchor cross-check (stop rule)
    v6 = readpin(C.canonical_pin('eps_cert_v006'))
    by = {tuple(s['range_inverse_kpc']): s for s in v6['shells']}

    def cx2_like(perturb=None):
        shells = []
        for n in range(4, 182):
            o = by[(float(n), float(n + 1))]
            env = o['eps_envelope'] * (1.0 + (perturb or {}).get(n, 0.0))
            shells.append({'range_inverse_kpc': [float(n), float(n + 1)], 'eps_envelope': env,
                           'eps': max(o['eps'], env), 'eps_base': o['eps_base'], 'eps_refined': o['eps_refined'],
                           'refinements': o['refinements'], 'actual': {'estimate': o['eps_actual_set']}})
        return {'shells': shells}
    must_pass('T51_anchor_crosscheck_agree_real_V006', 'anchor stop rule', lambda: R.compare_anchor_records(cx2_like(), v6),
              lambda v: v['verdict'] == 'AGREE' and v['overlap_shells'] == 178, 'AGREE on 178 shells; [4,5] uses dominating value')
    must_fail('T52_anchor_crosscheck_disagree', 'anchor stop rule', lambda: R.compare_anchor_records(cx2_like({100: 0.01}), v6), 'SHELL_[100.0, 101.0]_DISAGREES')
    short = cx2_like()
    short['shells'] = short['shells'][:100]
    must_fail('T53_anchor_crosscheck_partial', 'anchor stop rule', lambda: R.compare_anchor_records(short, v6), 'OVERLAP_COUNT_100_NOT_178')

    # ---------------------------------------------------------------- 7. scheduler (stubs; no processes)
    class Proc:
        def __init__(self, rc, polls):
            self.rc, self.left = rc, polls

        def poll(self):
            self.left -= 1
            return self.rc if self.left <= 0 else None

    class Stop(Exception):
        pass

    def vm_text(free_pages, spec_pages, page=16384):
        return ('Mach Virtual Memory Statistics: (page size of %d bytes)\nPages free:%34d.\nPages active:%32d.\n'
                'Pages speculative:%27d.\nPages purgeable:%29d.\nPages tag-storage free:%22d.\n'
                % (page, free_pages, 2147074, spec_pages, 99999999, 12979))

    def vm_gib(g):                                   # a vm_stat reading with exactly g GiB of free pages (speculative 0)
        return C.parse_vm_stat(vm_text(int(g * C.GIB) // 16384, 0))
    VM_PLENTY = vm_gib(100)

    def sched(sel_rows, *, codes=None, memory=lambda: 60, compare_verdict='AGREE', hold=None, swap=lambda: 100.0,
              max_c=2, limit=200, root_name='s', vmstat=lambda: VM_PLENTY, prep=None, floor=None):
        sroot = os.path.join(fx, 'sched_' + root_name)
        os.mkdir(sroot)
        if prep:
            prep(sroot)
        events, started, peak = [], [], [0]
        log = types.SimpleNamespace(write=lambda ev: events.append(ev))
        n = [0]

        def spawn(row):
            started.append(row['label'])
            sch = holder[0]
            peak[0] = max(peak[0], len(sch.running) + 1)
            return Proc((codes or {}).get(row['label'], 0), 3)

        def compare():
            adir = os.path.join(sroot, R.point_dir_name(anchor, 1))
            os.makedirs(adir, exist_ok=True)
            res = {'verdict': compare_verdict, 'max_rel_envelope': 0.0, 'max_rel_dominating': 0.0}
            pin = C.write_new(os.path.join(adir, 'ANCHOR_EPS_CROSSCHECK_%s_tol0p001.json' % k16), res, sroot)
            return compare_verdict, pin, res

        def sleep(_):
            n[0] += 1
            if n[0] > limit:
                raise Stop()
        holder = [None]
        s = R.Scheduler(sel_rows, sroot, operator_lane='SYNTHETIC_OPERATOR', max_concurrent=max_c, margin_pct=3,
                        hold_file=hold, spawn=spawn, memory=memory, swap=swap, sleep=sleep, compare=compare, log=log,
                        poll_seconds=0.0, vmstat=vmstat, **(floor or {}))
        holder[0] = s
        try:
            rc = s.run()
        except Stop:
            rc = 'TIMEOUT'
        return {'rc': rc, 'started': started, 'peak': peak[0], 'events': [e['event'] for e in events],
                'waits': [e.get('reason') for e in events if e['event'] == 'WAIT'], 'results': s.results, 'stopped': s.stopped,
                'start_events': [e for e in events if e['event'] == 'POINT_START'],
                'wait_events': [e for e in events if e['event'] == 'WAIT'], 'first_event': events[0] if events else None}

    def sched_refused(expected_started, **kw):
        """F8: a scheduler MUST_FAIL passes only if its reason appears AND exactly `expected_started` started."""
        v = sched(**kw)
        return dict(v, expected_started=expected_started,
                    ok=False if v['started'] == expected_started else 'STARTED_SET_MISMATCH: %r' % (v['started'],))

    four = rows[:4]

    def order_ok(v):
        ev = v['events']
        first_other = [i for i, e in enumerate(ev) if e == 'POINT_START'][2]
        return (v['rc'] == 0 and v['started'] == [r['label'] for r in four] and v['peak'] <= 3 and
                'WAITING_FOR_ANCHOR_EPS_CROSSCHECK' in v['waits'] and ev.index('ANCHOR_EPS_CROSSCHECK') < first_other)
    t54 = must_pass('T54_scheduler_order_concurrency_anchor_gate', 'scheduler', lambda: sched(four, max_c=3, root_name='ok'), order_ok,
              'anchor and C000 first; third point only after the anchor cross-check AGREE; <= 3 running')
    must_fail('T55_scheduler_anchor_disagree_stops', 'anchor stop rule',
              lambda: sched_refused(['TAIL_REANCHOR', 'HEADLINE_CORNER_000'], sel_rows=four, compare_verdict='DISAGREE',
                                    root_name='dis'), 'ANCHOR_EPS_DISAGREES')
    seq = iter([27, 27, 27] + [40] * 1000)
    must_pass('T56_scheduler_memory_gate_waits', 'memory gate', lambda: sched(rows[:1], memory=lambda: next(seq), root_name='mem'),
              lambda v: v['rc'] == 0 and any('MEMORY_BELOW_GATE' in (w or '') for w in v['waits']), 'waits at 27 %, starts at 40 %')
    must_fail('T57_scheduler_memory_unavailable_never_starts', 'memory gate',
              lambda: sched_refused([], sel_rows=rows[:1], memory=lambda: None, limit=20, root_name='memnone'), 'MEMORY_METRIC_UNAVAILABLE')
    holdf = W('hold/HOLD', {'hold': True})['path']
    must_fail('T58_scheduler_hold_file', 'memory gate (T-case pause)',
              lambda: sched_refused([], sel_rows=rows[:1], hold=holdf, limit=20, root_name='hold'), 'HOLD_FILE_PRESENT')
    sw = iter([100.0] + [2000.0] * 1000)
    must_fail('T59_scheduler_swap_growth_hold', 'memory gate (stricter-only swap hold)',
              lambda: sched_refused([], sel_rows=rows[:1], swap=lambda: next(sw), limit=20, root_name='swap'), 'SWAP_GROWTH_HOLD')
    record('T59b_swap_hold_nothing_started', 'MUST_FAIL', 'memory gate (stricter-only swap hold)',
           not os.listdir(os.path.join(fx, 'sched_swap')), 'no point started while swap grows', os.listdir(os.path.join(fx, 'sched_swap')))
    must_fail('T60_scheduler_anchor_not_selected', 'anchor stop rule',
              lambda: sched_refused([], sel_rows=rows[2:4], root_name='noanchor'), 'ANCHOR_CROSSCHECK_AGREE_REQUIRED_BEFORE_OTHER_POINTS')
    must_fail('T61_scheduler_anchor_worker_failed', 'anchor stop rule',
              lambda: sched_refused(['TAIL_REANCHOR', 'HEADLINE_CORNER_000'], sel_rows=four, codes={'TAIL_REANCHOR': 3},
                                    root_name='afail'), 'ANCHOR_WORKER_DID_NOT_FINISH_CLEANLY')
    must_pass('T_F8_01_started_set_assertion_is_not_vacuous', 'F8 scheduler MUST_FAIL asserts the started set',
              lambda: sched_refused(['TAIL_REANCHOR'], sel_rows=rows[:1], memory=lambda: None, limit=20, root_name='f8meta'),
              lambda v: v['ok'] is not False and v['started'] == [], 'a wrong expected set is reported as STARTED_SET_MISMATCH')

    # ---------------------------------------------------------------- 7b. F1 physical-headroom floor (vm_stat)
    real_like = ('Mach Virtual Memory Statistics: (page size of 16384 bytes)\nPages free:                                  2733145.\n'
                 'Pages active:                                2147074.\nPages speculative:                            170031.\n'
                 'Pages purgeable:                               48137.\nPages tag-storage free:                        12979.\n')
    must_pass('T_F1_01_vmstat_parse', 'F1 physical-headroom floor', lambda: C.parse_vm_stat(real_like),
              lambda v: v == {'page_size_bytes': 16384, 'free_pages': 2733145, 'speculative_pages': 170031,
                              'available_bytes': (2733145 + 170031) * 16384, 'purgeable_counted': False},
              '(free + speculative) x 16384; purgeable and tag-storage lines not counted')
    hdr = 'Mach Virtual Memory Statistics: (page size of 16384 bytes)\n'
    for cid, text in (('empty', ''), ('none', None), ('no_header', real_like.split('\n', 1)[1]),
                      ('page_size_zero', real_like.replace('page size of 16384', 'page size of 0')),
                      ('page_size_not_power_of_two', real_like.replace('page size of 16384', 'page size of 3000')),
                      ('two_headers', hdr + real_like), ('free_missing', real_like.replace('Pages free:', 'Pages fre:')),
                      ('free_twice', real_like + 'Pages free:                                  1.\n'),
                      ('speculative_missing', real_like.replace('Pages speculative:', 'Pages spec:')),
                      ('no_trailing_dot', real_like.replace('2733145.', '2733145')),
                      ('negative', real_like.replace('2733145.', '-2733145.')),
                      ('not_a_number', real_like.replace('170031.', '17OO31.'))):
        out = C.parse_vm_stat(text)
        record('T_F1_02_vmstat_parse_fails_closed_%s' % cid, 'MUST_FAIL', 'F1 physical-headroom floor', out is None,
               'None (unparseable vm_stat means no start)', out)
    must_pass('T_F1_03_vmstat_live_read_only', 'F1 physical-headroom floor', C.vm_stat_reading,
              lambda v: isinstance(v, dict) and v['page_size_bytes'] in (4096, 16384) and v['available_bytes'] > 0,
              'one read-only report from /usr/bin/vm_stat (no arguments)')
    G26, G2, G4 = 26 * C.GIB, 2 * C.GIB, 4 * C.GIB
    must_pass('T_F1_04_floor_exact_boundary_passes', 'F1 physical-headroom floor',
              lambda: C.physical_floor(vm_gib(32), running=0, r2_spike_allowance_bytes=G26, per_worker_peak_bytes=G2,
                                       floor_margin_bytes=G4), lambda v: v[0] is True, 'available 32 GiB == 26 + 1 x 2 + 4')
    one_page_short = C.parse_vm_stat(vm_text(32 * C.GIB // 16384 - 1, 0))
    must_fail('T_F1_05_floor_one_page_short_refused', 'F1 physical-headroom floor',
              lambda: dict(zip(('ok', 'why', 'detail'), C.physical_floor(one_page_short, running=0, r2_spike_allowance_bytes=G26,
                                                                         per_worker_peak_bytes=G2, floor_margin_bytes=G4))),
              'PHYSICAL_FLOOR_BELOW_REQUIRED')
    must_pass('T_F1_06_floor_scales_with_running_plus_one', 'F1 physical-headroom floor',
              lambda: [C.physical_floor(vm_gib(34), running=r, r2_spike_allowance_bytes=G26, per_worker_peak_bytes=G2,
                                        floor_margin_bytes=G4)[0] for r in (0, 1, 2)],
              lambda v: v == [True, True, False], '34 GiB admits running 0 and 1 (32, 34 GiB) but not 2 (36 GiB)')
    must_fail('T_F1_07_floor_metric_unavailable', 'F1 physical-headroom floor',
              lambda: dict(zip(('ok', 'why'), C.physical_floor(None, running=0, r2_spike_allowance_bytes=G26,
                                                               per_worker_peak_bytes=G2, floor_margin_bytes=G4)[:2])),
              'PHYSICAL_FLOOR_METRIC_UNAVAILABLE')
    must_fail('T_F1_08_floor_nonfinite_setting', 'F1 physical-headroom floor',
              lambda: dict(zip(('ok', 'why'), C.physical_floor(VM_PLENTY, running=0, r2_spike_allowance_bytes=math.nan,
                                                               per_worker_peak_bytes=G2, floor_margin_bytes=G4)[:2])),
              'PHYSICAL_FLOOR_SETTING_INVALID')
    must_fail('T_F1_10_scheduler_vmstat_unavailable_never_starts', 'F1 physical-headroom floor',
              lambda: sched_refused([], sel_rows=rows[:1], vmstat=lambda: None, limit=20, root_name='vmnone'),
              'PHYSICAL_FLOOR_METRIC_UNAVAILABLE')
    must_fail('T_F1_11_scheduler_vmstat_garbage_never_starts', 'F1 physical-headroom floor',
              lambda: sched_refused([], sel_rows=rows[:1], vmstat=lambda: C.parse_vm_stat('vm_stat: garbage'), limit=20,
                                    root_name='vmgarbage'), 'PHYSICAL_FLOOR_METRIC_UNAVAILABLE')
    must_fail('T_F1_12_scheduler_floor_low_although_0674_gate_passes', 'F1 physical-headroom floor (a start needs both)',
              lambda: sched_refused([], sel_rows=rows[:1], memory=lambda: 85, vmstat=lambda: vm_gib(31), limit=20,
                                    root_name='floorlow'), 'PHYSICAL_FLOOR_BELOW_REQUIRED')
    must_fail('T_F1_13_scheduler_0674_gate_low_although_floor_passes', 'F1 physical-headroom floor (a start needs both)',
              lambda: sched_refused([], sel_rows=rows[:1], memory=lambda: 27, vmstat=lambda: VM_PLENTY, limit=20,
                                    root_name='mem27'), 'MEMORY_BELOW_GATE')
    must_pass('T_F1_14_scheduler_floor_counts_running_plus_one', 'F1 physical-headroom floor',
              lambda: sched(rows[:2], vmstat=lambda: vm_gib(33), max_c=2, root_name='floorscale'),
              lambda v: v['rc'] == 0 and v['started'] == ['TAIL_REANCHOR', 'HEADLINE_CORNER_000'] and v['peak'] == 1
              and any('PHYSICAL_FLOOR_BELOW_REQUIRED' in (w or '') for w in v['waits']),
              '33 GiB: the anchor starts (32 GiB), C000 waits (34 GiB) until the anchor exits, then starts')

    def stage_peak(peak_bytes=None, raw=None):
        def prep(sroot):
            d = os.path.join(sroot, 'P05_b6de7aa886bb243c_HEADLINE_CORNER_011_a1')
            os.mkdir(d)
            obj = None if raw is not None else {'stage': 'EPS', 'peak_rss_bytes_process_high_water': peak_bytes, 'synthetic_fixture': SYN}
            C.write_new(os.path.join(d, 'STAGE_EPS_b6de7aa886bb243c.json'), obj, sroot, raw=raw)
        return prep
    v_meas = sched(rows[:1], vmstat=lambda: vm_gib(33), prep=stage_peak(10 * C.GIB), limit=20, root_name='measured')
    record('T_F1_15_scheduler_uses_larger_measured_stage_peak', 'MUST_FAIL', 'F1 physical-headroom floor',
           v_meas['started'] == [] and bool(v_meas['wait_events']) and
           v_meas['wait_events'][0]['physical_floor']['per_worker_peak_bytes'] == 10 * C.GIB and
           v_meas['wait_events'][0]['physical_floor']['per_worker_peak_measured_stage_bytes'] == 10 * C.GIB and
           'PHYSICAL_FLOOR_BELOW_REQUIRED' in v_meas['waits'][0],
           'a measured 10 GiB STAGE peak replaces the 2 GiB default: 26 + 10 + 4 = 40 > 33 GiB, nothing starts',
           json.dumps(v_meas['wait_events'][:1])[:500])
    must_fail('T_F1_16_scheduler_unreadable_stage_record_no_start', 'F1 physical-headroom floor',
              lambda: sched_refused([], sel_rows=rows[:1], prep=stage_peak(raw=b'{"stage": "EPS", "peak_rss_by'), limit=20,
                                    root_name='stagebad'), 'STAGE_PEAK_RSS_UNREADABLE')
    defaults = {'r2_spike_allowance_gib': 26.0, 'per_worker_peak_gib': 2.0, 'floor_margin_gib': 4.0}
    record('T_F1_17_floor_recorded_in_every_start_decision', 'MUST_PASS', 'F1 physical-headroom floor',
           t54 is not None and len(t54['start_events']) == 4 and
           all(e['physical_floor']['ok'] is True and e['physical_floor']['settings_gib'] == defaults and
               type(e['physical_floor']['available_bytes']) is int and e['physical_floor']['required_bytes'] > 0 for e in t54['start_events'])
           and t54['first_event']['physical_floor_settings_gib'] == defaults,
           'every POINT_START (and SCHEDULER_START) records the floor settings, available and required bytes',
           json.dumps((t54 or {}).get('start_events', [])[:1])[:500])
    must_pass('T_F1_18_floor_settings_are_root_choices', 'F1 physical-headroom floor',
              lambda: sched(rows[:1], vmstat=lambda: vm_gib(12), floor={'r2_spike_allowance_gib': 10.0, 'per_worker_peak_gib': 1.0,
                                                                         'floor_margin_gib': 0.0}, root_name='floorcustom'),
              lambda v: v['rc'] == 0 and v['started'] == ['TAIL_REANCHOR'] and v['start_events'][0]['physical_floor']['settings_gib'] ==
              {'r2_spike_allowance_gib': 10.0, 'per_worker_peak_gib': 1.0, 'floor_margin_gib': 0.0},
              'r2 10, peak 1, margin 0 GiB: 11 GiB required, 12 available, the anchor starts')
    must_pass('T_F1_19_floor_settings_zero_accepted', 'F1 physical-headroom floor', lambda: R.Scheduler(
              rows[:1], fx, operator_lane='X', max_concurrent=1, margin_pct=3, r2_spike_allowance_gib=0.0, per_worker_peak_gib=0,
              floor_margin_gib=0.0).floor_gib, lambda v: v == {'r2_spike_allowance_gib': 0.0, 'per_worker_peak_gib': 0,
                                                               'floor_margin_gib': 0.0}, 'finite and >= 0 is accepted')
    NEVER = C.LANE_ROOT + '/f_c3v003_never_created'

    def cli(argv):
        """In-process runner CLI. Settings refuse before any path is used, and NEVER is refused as an out-root anyway."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = R.main(argv)
            except SystemExit as exc:
                rc = exc.code
        return {'ok': rc == 0, 'rc': rc, 'stdout': out.getvalue()[-400:], 'stderr': err.getvalue()[-300:]}
    BAD_NONNEG = (('nan', math.nan), ('inf', math.inf), ('-inf', -math.inf), ('-1', -1.0))
    for opt in ('r2_spike_allowance_gib', 'per_worker_peak_gib', 'floor_margin_gib'):
        for s, val in BAD_NONNEG:
            must_fail('T_F1_20_scheduler_%s_%s' % (opt, s), 'F1 floor settings validated',
                      lambda o=opt, val=val: R.Scheduler(rows[:1], fx, operator_lane='X', max_concurrent=1, margin_pct=3, **{o: val}),
                      opt.upper() + '_MUST_BE_FINITE_AND_NONNEGATIVE')
            must_fail('T_F1_21_cli_%s_%s' % (opt, s), 'F1 floor settings validated',
                      lambda o=opt, s=s: cli(['run', '--out-root', NEVER, '--operator-lane', 'X', '--%s=%s' % (o.replace('_', '-'), s)]),
                      opt.upper() + '_MUST_BE_FINITE_AND_NONNEGATIVE')

    # ---------------------------------------------------------------- 7c. F2 anchor tolerance and swap hold validated
    big_err = cx2_like({n: 0.5 for n in range(4, 182)})      # the verifier's probe P1: a 50 % envelope error on every shell
    for s, val in (('nan', math.nan), ('inf', math.inf), ('-inf', -math.inf), ('0', 0.0), ('-1e-3', -1e-3), ('1e3', 1e3)):
        must_fail('T_F2_01_compare_anchor_records_tol_%s' % s, 'F2 anchor tolerance validated',
                  lambda val=val: R.compare_anchor_records(big_err, v6, val), 'ANCHOR_TOL_MUST_BE_FINITE')
        must_fail('T_F2_02_scheduler_tol_%s' % s, 'F2 anchor tolerance validated',
                  lambda val=val: R.Scheduler(rows[:1], fx, operator_lane='X', max_concurrent=1, margin_pct=3, tol=val),
                  'ANCHOR_TOL_MUST_BE_FINITE')
        must_fail('T_F2_03_cli_run_anchor_tol_%s' % s, 'F2 anchor tolerance validated',
                  lambda s=s: cli(['run', '--out-root', NEVER, '--operator-lane', 'X', '--anchor-tol=' + s]), 'ANCHOR_TOL_MUST_BE_FINITE')
        must_fail('T_F2_04_cli_compare_anchor_tol_%s' % s, 'F2 anchor tolerance validated',
                  lambda s=s: cli(['compare-anchor', '--out-root', NEVER, '--tol=' + s]), 'ANCHOR_TOL_MUST_BE_FINITE')
    must_pass('T_F2_05_tol_1e-2_accepted_and_still_catches_probe', 'F2 anchor tolerance validated',
              lambda: (R.compare_anchor_records(cx2_like(), v6, 1e-2)['verdict'], R.compare_anchor_records(big_err, v6, 1e-2)['verdict']),
              lambda v: v == ('AGREE', 'DISAGREE'), 'tol 1e-2 (the maximum): AGREE on V006 itself, DISAGREE on a 50 % error')
    for s, val in BAD_NONNEG:
        must_fail('T_F2_06_scheduler_swap_hold_%s' % s, 'F2 swap hold validated',
                  lambda val=val: R.Scheduler(rows[:1], fx, operator_lane='X', max_concurrent=1, margin_pct=3, swap_hold_mib=val),
                  'SWAP_HOLD_MIB_MUST_BE_FINITE_AND_NONNEGATIVE')
        must_fail('T_F2_07_cli_swap_hold_%s' % s, 'F2 swap hold validated',
                  lambda s=s: cli(['run', '--out-root', NEVER, '--operator-lane', 'X', '--swap-hold-mib=' + s]),
                  'SWAP_HOLD_MIB_MUST_BE_FINITE_AND_NONNEGATIVE')
    must_pass('T_F2_08_swap_hold_0_accepted', 'F2 swap hold validated', lambda: R.Scheduler(
              rows[:1], fx, operator_lane='X', max_concurrent=1, margin_pct=3, swap_hold_mib=0.0).swap_hold, lambda v: v == 0.0)
    must_pass('T_F2_09_cli_defaults_validate_then_out_root_refused', 'F2 swap hold validated (control)',
              lambda: cli(['run', '--out-root', NEVER, '--operator-lane', 'X']),
              lambda v: v['rc'] == 2 and 'OUT_ROOT_MUST_BE' in v['stdout'] and not os.path.exists(NEVER),
              'default settings pass validation; the out-root guard refuses next; nothing created')

    # ---------------------------------------------------------------- 8. LO facade (synthetic core only)
    ruling = W('lo/SYNTHETIC_ROOT_LO_RULING_FIXTURE.json', {'schema': 'S4RC1_SYNTHETIC_ROOT_RULING_FIXTURE', 'note': SYN})
    enf = W('lo/SYNTHETIC_ENFORCEMENT_MODULE_FIXTURE.json', {'schema': 'S4RC1_SYNTHETIC_ENFORCEMENT_FIXTURE'})
    ncol = 72
    cap = W('lo/CAP_%s.json' % k16, {'schema': 'UNT_POINT_LO_CAPS_CX2V001', 'identity': ident, 'custody': custody,
                                     'component_names': ['gas_body', 'route_a_offset'],
                                     'component_column_TV_mass_caps_kg': [[1.0e35] * ncol, [1.0e34] * ncol],
                                     'mass_convention': 'ACTUAL_PROPER_SOURCE_TOTAL_VARIATION_PER_COLUMN',
                                     'fixed_registered_stars_multiplier_abs': 0.0, 'gas_z_abs_max_m': 3.0e19,
                                     'readout_caps': {'row_ids': ids, 'row_contract_sha256': custody['row_contract_sha256'],
                                                      'R_m': radii, 'tau_km_s': tau, 'speed_abs_max_km_s': [60.0] * 12}})
    capr_body = {'schema': 'UNT_POINT_LO_CAP_REVIEW_CX2V001', 'identity': ident, 'custody': custody, 'cap_ref': cap,
                 'verdict': 'APPROVED', 'producer_sha256': LOCORE_PIN['sha256'], 'response_producer_sha256': PR_PIN['sha256'],
                 'enforcement': {'every_constructed_and_consumed_state': True, 'reject_before_consume': True,
                                 'complete_stage_inventory_reviewed': True, 'module': enf},
                 'accepts_registered_numerical_rho_and_node_quadrature': True,
                 'proper_source_caps_valid_for_all_stage_rosters': True, 'row_speed_and_uncertainty_policy_reviewed': True,
                 'distinct_from_producer_lane': True, 'reviewer_lane': 'SYNTHETIC_REVIEWER_LANE'}
    capr = W('lo/CAP_REVIEW_%s.json' % k16, capr_body)
    PART = L.RHO_PARTITION
    M = max(60.0 * r / (4 * t) for r, t in zip(radii, tau))

    def core_record(targets, *, rho_settings='registered', executed=True, blockers_override=None, partition=PART):
        shells, rho_shells = [], []
        for (lo, hi), t in zip(partition, targets):
            rho = 1.0e-3
            b1 = t / (rho * M)
            per = [60.0 * radii[i] * rho * b1 / (4 * tau[i]) for i in range(12)]
            shells.append({'range_inverse_kpc': [lo, hi], 'rho_used': rho, 'B1_per_m': b1, 'per_row_over_tau': per,
                           'max_over_tau': max(per), 'row_argmax_0based': per.index(max(per))})
            rho_shells.append({'range_inverse_kpc': [lo, hi], 'rho_used': rho})
        total = sum(s['max_over_tau'] for s in shells)
        thr = all(s['max_over_tau'] <= .005 for s in shells) and total <= .05
        bl = blockers_override if blockers_override is not None else ([] if thr else ['CONSERVATIVE_CAP_ENVELOPE_ABOVE_THRESHOLD'])
        rec = {'schema': 'UNT_POINT_LO_NUMERICAL_CX2V001', 'gate': 'LO', 'kind': 'PRELAUNCH_CONDITIONAL_SOURCE_ENVELOPE',
               'utc': C.utc(), 'status': 'TESTED', 'producer': LOCORE_PIN, 'response_producer': PR_PIN,
               'identity': ident, 'point_sha256': key, 'custody': custody, 'production_admissible': False,
               'cover_all_consumed_states': not bl, 'covers_all_consumed_states': not bl, 'rigorous_supremum': False,
               'driver_certificate': None, 'verdict': 'BLOCKED' if bl else 'CONDITIONAL_NUMERICAL_EVIDENCE_REVIEW_REQUIRED',
               'blockers': bl, 'numerical_envelope_executed': executed, 'coverage_is_conditional': True,
               'condition': 'reviewed enforcer rejects each constructed/consumed source or readout outside caps',
               'rho': {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'gate': 'RHO_G', 'settings': rho_settings,
                       'full_registered_search_executed': rho_settings == 'registered', 'coverage_complete': True,
                       'identity': ident, 'custody': custody, 'producer': PR_PIN, 'shells': rho_shells},
               'shells': shells, 'summed_max_over_tau': total, 'numerical_thresholds_pass': thr,
               'all_nonzero_B1_consumed': True, 'row_ids': ids, 'synthetic_fixture': SYN}
        if not executed:
            for k in ('rho', 'shells', 'summed_max_over_tau', 'numerical_thresholds_pass', 'all_nonzero_B1_consumed'):
                rec.pop(k)
        return rec

    core_calls = []

    def facade_env(rec):
        def produce_conditional_lo(spec_, cap_ref, *, review_ref=None, trusted_review_hashes=(), settings=None,
                                   shell_ranges=None, context=None):
            core_calls.append({'settings': settings, 'shell_ranges': shell_ranges})
            out = copy.deepcopy(rec)
            out.update(cap_ref=cap_ref, review_ref=review_ref)     # as lo_core L441/L458 record its inputs
            return out
        core = types.SimpleNamespace(produce_conditional_lo=produce_conditional_lo)
        return types.SimpleNamespace(core=lambda: core, read_pin=readpin, read_raw=readraw,
                                     self_pin=lambda: C.pin_of(F.__file__, ROOTS), root_rulings=(ruling['sha256'],),
                                     point_context=lambda s: {'synthetic_context': True})

    def facade(rec, *, cap_ref=cap, review_ref=capr, trusted=None, ruling_ref=ruling):
        return F._produce(spec, cap_ref, review_ref=review_ref, trusted_review_hashes=trusted or [capr['sha256']],
                          root_ruling_ref=ruling_ref, context=None, env=facade_env(rec))

    clean = core_record([0.001] * 9)
    # c3v002 (0679): the LO facade mapping cases T62-T71 and T70b are dropped; the facade is HELD in build_c3v001
    # and is not part of c3v002. Its root-gate cases T72-T74 follow unchanged.
    must_fail('T72_facade_root_gate_pending', 'no LO number before root rules', lambda: facade(clean, ruling_ref=None),
              'ROOT_LO_CAP_AND_ENFORCEMENT_RULING_PENDING')
    pub = must_fail('T73_facade_public_entry_unavailable', 'no LO number before root rules',
                    lambda: F.produce_conditional_lo(spec, cap, review_ref=capr, trusted_review_hashes=[capr['sha256']],
                                                     root_ruling_ref=ruling), 'ROOT_LO_CAP_AND_ENFORCEMENT_RULING_PENDING')
    record('T74_facade_public_entry_loaded_no_core', 'MUST_FAIL', 'no LO number before root rules',
           's4rc1_lo_core_r5_cx2v001' not in sys.modules and F.ROOT_LO_RULING_SHA256 == (),
           'lo_core never imported; ROOT_LO_RULING_SHA256 empty', F.ROOT_LO_RULING_SHA256)

    # ---------------------------------------------------------------- 9. LO_ENVELOPE adapter (synthetic env)
    lo_slot = W('lo/LO_NUMERIC_%s.json' % k16, clean)     # c3v002: a placeholder; the root gate refuses before reading it
    fac_pin = C.pin_of(F.__file__, ROOTS)
    ad_pin = C.pin_of(L.__file__, ROOTS)
    lo_rev_body = {'schema': 'UNT_POINT_LO_ENVELOPE_REVIEW_C3V001', 'verdict': 'APPROVED', 'numeric_ref': lo_slot,
                   'point_sha256': key, 'custody_sha256': csha, 'adapter_sha256': ad_pin['sha256'],
                   'facade_sha256': fac_pin['sha256'], 'accepts_conditional_prelaunch_envelope_not_rigorous_sup': True,
                   'condition_acknowledged': clean['condition'], 'distinct_from_producer_lane': True,
                   'reviewer_lane': 'SYNTHETIC_REVIEWER_LANE'}
    lo_rev = W('lo/LO_REVIEW_%s.json' % k16, lo_rev_body)
    APPROVED_LO = (LOCORE_PIN['sha256'], PR_PIN['sha256'], fac_pin['sha256'], ad_pin['sha256'])

    def adapter_env(det=None):
        return types.SimpleNamespace(derive_details=lambda s: det or details, read_pin=readpin, read_raw=readraw,
                                     self_pin=lambda: ad_pin, root_rulings=(ruling['sha256'],), utc=C.utc)

    def adapt_lo(slot=lo_slot, *, capr_=capr, lorev=lo_rev, det=None, approved=APPROVED_LO, reviews=None, ruling_ref=ruling):
        return L._adapt(spec, slot, cap_ref=cap, cap_review_ref=capr_, lo_review_ref=lorev, root_ruling_ref=ruling_ref,
                        approved_producer_sha256=approved,
                        approved_review_sha256=reviews or (capr_ and capr_['sha256'], lorev and lorev['sha256']), env=adapter_env(det))
    # c3v002 (0679): the LO_ENVELOPE adapter cases T75-T89, T81b and T84a are dropped; the adapter is HELD in
    # build_c3v001 and is not part of c3v002. Its root-gate cases T90-T92 follow unchanged.
    must_fail('T90_lo_adapter_root_gate', 'no LO number before root rules', lambda: adapt_lo(ruling_ref=None), 'ROOT_LO_CAP_AND_ENFORCEMENT_RULING_PENDING')
    must_fail('T91_lo_adapter_public_entry_blocked', 'no LO number before root rules',
              lambda: L.adapt_lo_envelope(spec, lo_slot, cap_ref=cap, cap_review_ref=capr, lo_review_ref=lo_rev,
                                          root_ruling_ref=ruling, approved_producer_sha256=APPROVED_LO,
                                          approved_review_sha256=(capr['sha256'], lo_rev['sha256'])), 'ROOT_LO_CAP_AND_ENFORCEMENT_RULING_PENDING')
    record('T92_lo_adapter_public_no_custody_load', 'MUST_FAIL', 'no LO number before root rules',
           's4rc1_lo_adapter_custody_cx2v002' not in sys.modules and L.ROOT_LO_RULING_SHA256 == (),
           'custody never loaded; ROOT_LO_RULING_SHA256 empty', L.ROOT_LO_RULING_SHA256)

    # ---------------------------------------------------------------- 10. bundle, registry, offline verifier
    b_root = os.path.join(fx, 'registry_out')
    os.mkdir(b_root)
    eps_slot = W('bundle_in/EPS_NUMERIC_%s.json' % k16, eps_numeric())
    eps_pf = W('bundle_in/EPS_PROOF_%s.json' % k16, eps_proof(eps_slot))
    gq_pf = W('bundle_in/GQ_PROOF_%s.json' % k16, gq_proof())
    # c3v003: the lo slot is the point's registered rho record (synthetic here) and its proof is gate LO_RHO_SLOT from the
    # canonical slot-proof producer lo_slot_proof_c3v002 (a synthetic proof here; section 14 uses the real module's proof).
    SLOT_PIN = C.canonical_pin('lo_slot_proof')
    LO_SYN = W('bundle_in/SYNTHETIC_LO_ENVELOPE_PRODUCER_FIXTURE.json', {'schema': 'S4RC1_SYNTHETIC_PRODUCER_FIXTURE',
               'note': 'stands for the retired LO_ENVELOPE producer (A134 Q1/Q5); never executed'})
    lo_slot_b = W('bundle_in/RHO_NUMERIC_SYNTHETIC_%s.json' % k16, rho_numeric(ident, key))
    lo_pf = W('bundle_in/LO_RHO_SLOT_PROOF_%s.json' % k16, {'schema': C.PROOF_SCHEMA, 'gate': 'LO_RHO_SLOT', 'status': 'TESTED',
              'verdict': 'PASS', 'point_sha256': key, 'custody_sha256': csha, 'producer': SLOT_PIN,
              'driver_certificate': lo_slot_b, 'rho_record': lo_slot_b})
    approved = [AD_PIN, GQ_PIN, SLOT_PIN]
    appr_file = W('bundle_in/C1_APPROVED_PRODUCERS_SYNTHETIC.json', {'approved_certificate_producers': approved})
    CANON_TEST = None                       # c3v003: the slot producer is canonical in common c3v003; no seam
    loaded = []

    def custody_loader_for(cust=None):
        def loader(pin):
            loaded.append(pin)
            return lambda s: copy.deepcopy(cust or custody)
        return loader
    c1_n = [0]

    def c1_fixture(registry, appr, *, deriver=None, enumerator=None, review_over=None, review=True, raw_doc=None):
        """A synthetic C1 document {tail_readiness: ...} with a matching certificate_policy_review (wrapper L61-75)."""
        c1_n[0] += 1
        tr = {'certificate_registry': registry, 'custody_deriver': deriver or C.canonical_pin('custody'),
              'state_enumerator': enumerator or C.canonical_pin('state_enumerator'), 'approved_certificate_producers': appr}
        rv = {'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True, 'driver_sha256': C.DRIVER_SHA,
              'custody_deriver': tr['custody_deriver'], 'state_enumerator': tr['state_enumerator'],
              'approved_certificate_producers': appr, 'guard_sha256': '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677',
              'driver_slot_rule': 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE',
              'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
        rv.update(review_over or {})
        tr['certificate_policy_review'] = W('c1/POLICY_REVIEW_%02d.json' % c1_n[0], rv) if review else None
        return W('c1/C1_%02d.json' % c1_n[0], {'tail_readiness': tr} if raw_doc is None else raw_doc)

    def build_reg(tag, *, eps=eps_pf, gq=gq_pf, lo=lo_pf, appr=approved):
        broot = os.path.join(b_root, tag)
        os.mkdir(broot)
        b = A.assemble_bundle(anchor, eps_proof=eps['path'], gq_proof=gq['path'], lo_proof=lo['path'], approved=appr,
                              out_root=broot, roots=ROOTS)
        reg, man = A.assemble_registry([b['path']], approved=appr, out_root=broot, roots=ROOTS)
        return b, reg, man, broot

    def verify(reg, *, cust=None, appr=None, canon=CANON_TEST, c1=None):
        """F3: the verifier reads the approved producers and the custody deriver from a C1 that names `reg`."""
        appr = approved if appr is None else appr
        return A.verify_registry(reg, [anchor], c1_ref=c1 or c1_fixture(reg, appr), custody_loader=custody_loader_for(cust),
                                 guard=G, roots=ROOTS, guard_roots=GROOTS, canonical_producers=canon)
    built = must_pass('T93_bundle_and_registry_assembled', 'registry assembler', lambda: build_reg('ok'),
                      lambda v: v is not None and v[0]['sha256'] and v[1]['sha256'], 'bundle + registry + manifest')
    if built is None:
        raise SystemExit('T93 failed; later registry cases depend on it')
    b_ok, reg_ok, man_ok, broot_ok = built
    rep = must_pass('T94_offline_verifier_PASS', 'offline verifier (wrapper v002 L86-90, L145-191 bytes + L30 guard)', lambda: verify(reg_ok),
                    lambda v: v['ok'] is True and v['points'][0]['wrapper_replica']['ok'] and v['points'][0]['guard_b1']['ok'],
                    'wrapper replica ok and guard verify_bundle(prelaunch) ok')
    reg_doc = readpin(reg_ok)
    record('T95_registry_record_exact_shape', 'MUST_PASS', 'registry assembler',
           set(reg_doc['points'][key]) == {'identity', 'bundle', 'eps_certificate', 'lo_certificate'} and
           all(C.is_pin(reg_doc['points'][key][k]) for k in ('bundle', 'eps_certificate', 'lo_certificate')) and
           reg_doc['schema'] == A.REGISTRY_SCHEMA and C.is_pin(reg_doc['generator']), '{identity, bundle, eps_certificate, lo_certificate}',
           sorted(reg_doc['points'][key]))
    # custody mismatch
    rv = verify(reg_ok, cust=dict(custody, modules_sha256='4' * 64))
    record('T96_custody_mismatch_fails_both', 'MUST_FAIL', 'custody or point mismatch',
           rv['ok'] is False and 'custody mismatch' in json.dumps(rv['points'][0]['wrapper_replica']),
           'wrapper replica custody mismatch', json.dumps(rv['points'][0]['wrapper_replica'])[:300])

    def guard_only(bundle_pin, cust=custody, appr=approved):
        kw = {} if GROOTS is None else {'allowed_roots': GROOTS}
        return G.verify_bundle(bundle_pin, ident, expected_custody=cust, approved_producer_sha256=[p['sha256'] for p in appr],
                               phase='prelaunch', required_states=[], **kw)
    gq_ = guard_only(b_ok, dict(custody, modules_sha256='4' * 64))
    record('T97_guard_custody_mismatch', 'MUST_FAIL', 'custody or point mismatch', gq_['ok'] is False and 'manifest custody mismatch' in gq_['blockers'][0],
           'guard: manifest custody mismatch', gq_['blockers'])
    # point mismatch: registry record identity altered
    tampered = copy.deepcopy(reg_doc)
    tampered['points'][key]['identity'] = C.point_identity(json.load(open(c000['spec_path'])))
    treg = W('tamper/REGISTRY_IDENTITY_TAMPERED.json', tampered)
    rv = verify(treg)
    record('T98_point_identity_mismatch', 'MUST_FAIL', 'custody or point mismatch',
           rv['ok'] is False and 'CERTIFICATE_POINT_MISSING_OR_MISMATCHED' in json.dumps(rv), 'CERTIFICATE_POINT_MISSING_OR_MISMATCHED',
           json.dumps(rv['points'][0]['wrapper_replica'])[:300])
    other_pt = W('tamper/GQ_PROOF_OTHER_POINT.json', gq_proof(point=c000['key']))
    must_fail('T99_bundle_refuses_other_point_proof', 'custody or point mismatch', lambda: build_reg('otherpt', gq=other_pt), 'GQ_POINT_MISMATCH')
    # slot binding differs from the proof driver_certificate
    eps_slot2 = W('tamper/EPS_NUMERIC_SECOND_COPY.json', eps_numeric())
    bdoc = readpin(b_ok)
    b_bad = copy.deepcopy(bdoc)
    b_bad['driver_certificate_bindings']['eps_certificate'] = eps_slot2
    b_bad_pin = W('tamper/BUNDLE_BINDING_DIFFERS.json', b_bad)
    reg_b = copy.deepcopy(reg_doc)
    reg_b['points'][key]['bundle'] = b_bad_pin
    reg_b['points'][key]['eps_certificate'] = eps_slot2
    reg_b_pin = W('tamper/REGISTRY_SLOT_DIFFERS_FROM_PROOF.json', reg_b)
    rv = verify(reg_b_pin)
    record('T100_slot_differs_from_proof_driver_certificate', 'MUST_FAIL', 'slot binding differs from driver_certificate',
           rv['ok'] is False and 'EPS proof differs from attached driver certificate' in json.dumps(rv),
           'EPS proof differs from attached driver certificate', json.dumps(rv['points'][0]['wrapper_replica'])[:300])
    reg_c = copy.deepcopy(reg_doc)
    reg_c['points'][key]['eps_certificate'] = eps_slot2
    reg_c_pin = W('tamper/REGISTRY_SLOT_DIFFERS_FROM_BUNDLE.json', reg_c)
    rv = verify(reg_c_pin)
    record('T101_registry_slot_differs_from_bundle_binding', 'MUST_FAIL', 'slot binding differs from driver_certificate',
           rv['ok'] is False and 'bundle does not bind the actual driver certificate slots' in json.dumps(rv),
           'bundle does not bind the actual driver certificate slots', json.dumps(rv['points'][0]['wrapper_replica'])[:300])
    # unapproved producer
    rv = verify(reg_ok, appr=[AD_PIN, GQ_PIN], canon=None)   # a C1 without the slot producer: refused at LO_RHO_SLOT (L158-159)
    record('T102_unapproved_lo_slot_producer', 'MUST_FAIL', 'unapproved producer',
           rv['ok'] is False and 'LO_RHO_SLOT producer is not approved' in json.dumps(rv), 'LO_RHO_SLOT producer is not approved',
           json.dumps(rv['points'][0]['wrapper_replica'])[:300])
    alias_ad = {'path': C.CERT + '/./point_response_admission_adapter_cx2v003.py', 'sha256': AD_PIN['sha256']}
    rv = verify(reg_ok, appr=[alias_ad, GQ_PIN, SLOT_PIN])
    gq2 = guard_only(b_ok, appr=[alias_ad, GQ_PIN, SLOT_PIN])
    record('T103_R4_alias_pin_refused_by_replica_but_not_guard', 'MUST_FAIL', 'unapproved producer (R4 whole-dict pin)',
           rv['ok'] is False and 'C1_APPROVED_PRODUCER_NOT_CANONICAL' in json.dumps(rv['c1_policy_gate']) and
           'point_response_admission_adapter' in json.dumps(rv['c1_policy_gate']) and gq2['ok'] is True,
           'replica refuses the alias (at the C1 canonical-pin check, F3) while the L30 guard (sha only) passes: the replica is needed',
           json.dumps(rv['c1_policy_gate'])[:300])
    must_fail('T104_bundle_refuses_unapproved', 'unapproved producer', lambda: build_reg('unappr', appr=[AD_PIN, GQ_PIN]), 'LO_RHO_SLOT_PRODUCER_NOT_APPROVED')
    # uvt_ path component (existing pinned uvt_ SOURCE module; never created by this suite)
    uvt_src = {'path': C.ART + '/tail_scheme_impl_c2/driver_r5/cascade/tail_scheme_impl_c2/route_b/uvt_route_b_binding_c2v001_r5.py',
               'sha256': '1e27430c12cc84195b7642fe925bc6f9916a55158ecc02c9fbff9b8564506329'}
    b_uvt = copy.deepcopy(bdoc)
    b_uvt['prelaunch']['GQ'] = uvt_src
    b_uvt_pin = W('tamper/BUNDLE_GQ_PIN_UVT.json', b_uvt)
    g3 = guard_only(b_uvt_pin)
    record('T105_guard_refuses_uvt_component', 'MUST_FAIL', 'uvt_ path component', g3['ok'] is False and 'forbidden input path' in g3['blockers'][0],
           'guard v003: forbidden input path', g3['blockers'])
    b_uvt2 = copy.deepcopy(bdoc)
    b_uvt2['prelaunch']['EPS'] = uvt_src
    b_uvt2_pin = W('tamper/BUNDLE_EPS_PIN_UVT.json', b_uvt2)
    reg_u = copy.deepcopy(reg_doc)
    reg_u['points'][key]['bundle'] = b_uvt2_pin
    reg_u_pin = W('tamper/REGISTRY_UVT.json', reg_u)
    rv = verify(reg_u_pin)
    record('T106_replica_refuses_uvt_lexically', 'MUST_FAIL', 'uvt_ path component', rv['ok'] is False and 'UVT_COMPONENT_REFUSED' in json.dumps(rv),
           'UVT_COMPONENT_REFUSED before opening', json.dumps(rv['points'][0]['wrapper_replica'])[:300])
    # file over 8 MiB (sparse fixture; the guard refuses on size before reading)
    big = os.path.join(fx, 'tamper', 'GQ_PROOF_OVER_8MIB.json')
    head = json.dumps(gq_proof()).encode()
    with open(big, 'xb') as f:
        f.write(head)
        f.truncate(C.EIGHT_MIB + 1)
    big_pin = {'path': big, 'sha256': C.sha256_file(big)}
    b_big = copy.deepcopy(bdoc)
    b_big['prelaunch']['GQ'] = big_pin
    b_big_pin = W('tamper/BUNDLE_GQ_OVER_8MIB.json', b_big)
    g4 = guard_only(b_big_pin)
    record('T107_guard_refuses_file_over_8MiB', 'MUST_FAIL', 'file over 8 MiB', g4['ok'] is False and 'exceeds 8 MiB' in g4['blockers'][0],
           'guard v003: proof/code file exceeds 8 MiB', g4['blockers'])
    must_fail('T108_assembler_refuses_file_over_8MiB', 'file over 8 MiB', lambda: build_reg('big', gq=big_pin), 'exceeds 8 MiB')
    # smoke or partial in bundle inputs
    drift = eps_numeric()
    drift['dependencies'] = {'reference_lwr_common': {'path': '/x', 'sha256': '6' * 64}}
    drift_slot = W('tamper/EPS_NUMERIC_DRIFT.json', drift)
    drift_pf = W('tamper/EPS_PROOF_DRIFT.json', eps_proof(drift_slot))
    broot_d = os.path.join(b_root, 'drift')
    os.mkdir(broot_d)
    b_drift = A.assemble_bundle(anchor, eps_proof=drift_pf['path'], gq_proof=gq_pf['path'], lo_proof=lo_pf['path'],
                                approved=approved, out_root=broot_d, roots=ROOTS)
    c000_ident = C.point_identity(json.load(open(c000['spec_path'])))
    c000_bundle = copy.deepcopy(readpin(b_ok))
    c000_bundle['identity'] = c000_ident
    c000_bpin = W('tamper/BUNDLE_C000_FOR_DRIFT_TEST.json', c000_bundle)
    must_fail('T108b_registry_refuses_source_pin_drift', 'custody or point mismatch (upstream drift)',
              lambda: A.assemble_registry([b_drift['path'], c000_bpin['path']], approved=approved, out_root=broot_d, roots=ROOTS),
              'EPS_SOURCE_PINS_DIFFER_ACROSS_POINTS')
    smoke_eps = W('tamper/EPS_NUMERIC_SMOKE.json', eps_numeric(settings='smoke', full=False))
    smoke_pf = W('tamper/EPS_PROOF_SMOKE.json', eps_proof(smoke_eps))
    must_fail('T109_assembler_refuses_smoke_eps_record', 'smoke or partial', lambda: build_reg('smoke', eps=smoke_pf), 'SMOKE_OR_PARTIAL_EPS_RECORD_REFUSED')
    part_gq = W('tamper/GQ_PROOF_PARTIAL.json', gq_proof(nodes=128, full=False))
    must_fail('T110_assembler_refuses_partial_gq', 'smoke or partial', lambda: build_reg('partgq', gq=part_gq), 'PARTIAL_GQ_PROOF_REFUSED')
    short_pf = W('tamper/EPS_PROOF_SHORT_SHELLS.json', eps_proof(eps_slot, end=100))
    b_short = copy.deepcopy(bdoc)
    b_short['prelaunch']['EPS'] = short_pf
    g5 = guard_only(W('tamper/BUNDLE_EPS_SHORT.json', b_short))
    record('T111_guard_refuses_partial_eps_shells', 'MUST_FAIL', 'smoke or partial', g5['ok'] is False and 'spherical coverage shortfall' in g5['blockers'][0],
           'guard v003: EPS spherical coverage shortfall', g5['blockers'])

    # ---------------------------------------------------------------- 10b. F3 C1-level gate, F5 assembler out-root, F7 C1 draft
    l0 = len(loaded)
    rep2 = verify(reg_ok)
    record('T_F3_01_custody_deriver_and_producers_read_from_the_C1', 'MUST_PASS', 'F3 offline verifier reads the C1',
           rep2['ok'] is True and loaded[l0:] == [C.canonical_pin('custody')] and rep2['c1_policy_gate']['ok'] is True and
           rep2['c1_policy_gate']['approved_certificate_producers'] == approved and
           rep2['c1_policy_gate']['custody_deriver'] == C.canonical_pin('custody'),
           'the custody loader receives exactly the C1 custody_deriver pin; the approved list is the C1 list',
           json.dumps(rep2['c1_policy_gate'])[:400])
    must_fail('T_F3_02_real_r9_config_as_C1_is_policy_pending', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=C.canonical_pin('config_r9')),
              'CERTIFICATE_POLICY_PENDING: certificate_registry,certificate_policy_review,approved_certificate_producers')
    must_fail('T_F3_03_C1_without_tail_readiness', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(reg_ok, approved, raw_doc={'schema': 'NOT_A_C1'})), 'TAIL_READINESS_CONFIG_REQUIRED')
    must_fail('T_F3_04_policy_review_missing', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(reg_ok, approved, review=False)), 'CERTIFICATE_POLICY_PENDING: certificate_policy_review')
    must_fail('T_F3_05_approved_producers_empty', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(reg_ok, [])), 'CERTIFICATE_POLICY_PENDING: approved_certificate_producers')
    l1 = len(loaded)
    alias_cu = {'path': C.CERT + '/./custody_cx2v002.py', 'sha256': C.PINS['custody'][1]}
    must_fail('T_F3_06_custody_deriver_alias_not_canonical', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(reg_ok, approved, deriver=alias_cu)), 'C1_CUSTODY_DERIVER_NOT_CANONICAL')
    must_fail('T_F3_07_custody_deriver_other_bytes', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(reg_ok, approved, deriver={'path': C.PINS['custody'][0], 'sha256': '7' * 64})),
              'C1_CUSTODY_DERIVER_NOT_CANONICAL')
    record('T_F3_08_noncanonical_deriver_never_loaded', 'MUST_FAIL', 'F3 offline verifier C1-level gate', len(loaded) == l1,
           'custody is never derived with a non-canonical deriver', loaded[l1:])
    must_fail('T_F3_09_retired_LO_ENVELOPE_producer_not_canonical', 'F3 offline verifier C1-level gate (c3v003: LO_RHO_SLOT only)',
              lambda: verify(reg_ok, appr=approved + [LO_SYN], canon=None), 'C1_APPROVED_PRODUCER_NOT_CANONICAL')
    for cid, over, code in (('10_review_binds_other_producer_list', {'approved_certificate_producers': [AD_PIN, GQ_PIN]},
                             'binding mismatch: approved_certificate_producers'),
                            ('11_review_not_TESTED_ok', {'ok': False}, 'evidence is not TESTED ok'),
                            ('12_review_other_guard', {'guard_sha256': '8' * 64}, 'binding mismatch: guard_sha256'),
                            ('13_review_wrong_schema', {'schema': 'DDO154_OTHER'}, 'wrong evidence schema'),
                            ('14_review_other_slot_rule', {'driver_slot_rule': 'OTHER'}, 'binding mismatch: driver_slot_rule'),
                            ('15_review_other_driver', {'driver_sha256': '9' * 64}, 'binding mismatch: driver_sha256')):
        must_fail('T_F3_%s' % cid, 'F3 offline verifier C1-level gate (certificate_policy_review checked_gate)',
                  lambda over=over: verify(reg_ok, c1=c1_fixture(reg_ok, approved, review_over=over)), code)
    must_fail('T_F3_16_C1_names_another_registry', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(treg, approved)), 'C1_CERTIFICATE_REGISTRY_IS_NOT_THE_VERIFIED_REGISTRY')
    must_fail('T_F3_17_state_enumerator_bytes_differ', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, c1=c1_fixture(reg_ok, approved, enumerator={'path': C.PINS['state_enumerator'][0],
                                                                                 'sha256': '6' * 64})),
              'C1 state_enumerator: sha256 mismatch')
    fake_lo = {'path': SLOT_PIN['path'], 'sha256': '5' * 64}
    must_fail('T_F3_18_approved_producer_bytes_differ', 'F3 offline verifier C1-level gate',
              lambda: verify(reg_ok, appr=[AD_PIN, GQ_PIN, fake_lo], canon=[AD_PIN, GQ_PIN, fake_lo]),
              'C1 approved certificate producer: sha256 mismatch')

    def pins_r10_c4():
        # c3v004 V09: wrapper_q5b1 (the published path) is checked as a string by T_V09_01 and is never opened here.
        bad = [n for n, (p, s) in sorted(C.PINS.items())
               if n != 'wrapper_q5b1' and (os.path.realpath(p) != p or C.sha256_file(p) != s)]
        return {'bad': bad, 'wrapper': C.PINS.get('wrapper_r10_c4'), 'core': C.PINS.get('core_r10_c4'),
                'r9_labels': sorted(n for n in C.PINS if n in ('wrapper_r9', 'core_r9'))}
    must_pass('T_F3_19_PINS_relabelled_r10_c4_and_all_pins_from_bytes', 'F3 relabel to the wrapper of record', pins_r10_c4,
              lambda v: v['bad'] == [] and v['r9_labels'] == [] and v['wrapper'][1].startswith('ef3d3d69') and
              v['core'][1].startswith('dc895f8a') and v['wrapper'][0].endswith('/v006r10_c4/calibration_orchestrator_cx2v006r10_c4.py'),
              'wrapper_r10_c4 ef3d3d69 and core_r10_c4 dc895f8a; every PINS entry realpath-exact and sha from bytes')
    record('T_F3_20_verifier_output_states_its_scope', 'MUST_PASS', 'F3 scope limit stated', 'wrapper v002 7a6af535' in rep2['scope']
           and 'L67-75' in rep2['scope'] and 'NOT replicated' in rep2['scope'] and 'EXECUTED from the' in rep2['scope'],
           'scope names wrapper v002 7a6af535, L67-75, the executed L145-191 bytes and what is not replicated',
           rep2['scope'][:300])

    def asm_cli(argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                rc = A.main(argv)
            except SystemExit as exc:
                rc = exc.code
        return {'ok': rc == 0, 'rc': rc, 'stdout': out.getvalue()[-400:], 'stderr': err.getvalue()[-400:]}
    must_fail('T_F3_21_cli_verify_requires_the_C1_not_a_producer_list', 'F3 offline verifier reads the C1',
              lambda: asm_cli(['verify', '--registry', reg_ok['path'], '--registry-sha256', reg_ok['sha256'],
                               '--approved-producers', appr_file['path']]), 'the following arguments are required: --c1, --c1-sha256')
    must_fail('T_F3_22_cli_verify_refuses_a_noncanonical_C1_path', 'F3 offline verifier reads the C1',
              lambda: asm_cli(['verify', '--registry', reg_ok['path'], '--registry-sha256', reg_ok['sha256'],
                               '--c1', C.CERT + '/../v006r9/RUN_CONFIG_DDO154_CX2V006R9_P128_MS128.json', '--c1-sha256', '0' * 64]),
              'NONCANONICAL_PATH')

    lane = os.path.join(fx, 'lane_f5')
    os.mkdir(lane)
    os.mkdir(os.path.join(lane, 'registry_ok'))
    os.mkdir(os.path.join(lane, 'build_c3v009'))
    os.symlink(os.path.join(lane, 'registry_ok'), os.path.join(lane, 'registry_link'))
    must_pass('T_F5_03_assembler_out_root_registry_name_ok', 'F5 assembler out-root confinement',
              lambda: A._out_root(os.path.join(lane, 'registry_ok'), lane_root=lane), lambda p: p == os.path.join(lane, 'registry_ok'))
    for cid, path, code in (('04_build_folder', os.path.join(lane, 'build_c3v009'), 'ASSEMBLER_OUT_ROOT_MUST_BE'),
                            ('05_symlinked_registry_folder', os.path.join(lane, 'registry_link'), 'OUT_ROOT_MUST_EXIST_AND_BE_CANONICAL'),
                            ('06_nested_under_registry', os.path.join(lane, 'registry_ok', 'sub'), 'ASSEMBLER_OUT_ROOT_MUST_BE'),
                            ('07_empty_registry_name', os.path.join(lane, 'registry_'), 'ASSEMBLER_OUT_ROOT_MUST_BE')):
        must_fail('T_F5_%s' % cid, 'F5 assembler out-root confinement', lambda path=path: A._out_root(path, lane_root=lane), code)
    for cid, path, code in (('08_real_build_c3v001', C.LANE_ROOT + '/build_c3v001', 'ASSEMBLER_OUT_ROOT_MUST_BE'),
                            ('09_real_build_c3v002', C.LANE_ROOT + '/build_c3v002', 'ASSEMBLER_OUT_ROOT_MUST_BE'),
                            ('10_real_verify_folder', C.LANE_ROOT + '/verify_c3v001', 'ASSEMBLER_OUT_ROOT_MUST_BE'),
                            ('11_real_missing_registry_folder', C.LANE_ROOT + '/registry_c3v002_never_created',
                             'OUT_ROOT_MUST_EXIST_AND_BE_CANONICAL')):
        must_fail('T_F5_%s' % cid, 'F5 assembler out-root confinement (default lane root)', lambda path=path: A._out_root(path), code)

    with open(os.path.join('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s4rc1_c3/build_c3v004', 'C1_DRAFT_APPROVED_PRODUCERS_C3V004.json'), 'rb') as f:
        draft = json.loads(f.read())
    record('T_F7_01_C1_draft_lists_EPS_GQ_and_the_slot_producer', 'MUST_PASS', 'F7 C1 draft (c3v004: the LO_RHO_SLOT producer c3v003)',
           draft.get('schema') == 'S4RC1_C1_DRAFT_APPROVED_PRODUCERS_C3V004' and 'approved_certificate_producers' not in draft and
           draft.get('proposed_approved_certificate_producers') == [C.canonical_pin(n) for n in C.CANONICAL_APPROVED_PRODUCERS] and
           not any('lo_envelope' in p['path'] or p['sha256'] == LO_ADAPTER_C3V001[1] for p in draft['proposed_approved_certificate_producers']),
           'exactly [EPS adapter v003 4de70486, GQ producer v005 2832ceb9, LO slot proof c3v003]; no LO_ENVELOPE entry',
           draft.get('proposed_approved_certificate_producers'))
    record('T_H1_01_no_pyc_written_in_build_folder', 'MUST_PASS', 'hygiene: exclusive-create writes only',
           not os.path.exists(os.path.join(build, '__pycache__')), 'no __pycache__ in the build folder',
           os.path.exists(os.path.join(build, '__pycache__')))
    record('T_H1_02_lane_root_listing_unchanged', 'MUST_PASS', 'hygiene: writes only under the fixture root',
           sorted(os.listdir(C.LANE_ROOT)) == lane_before and not os.path.exists(NEVER), 'the s4rc1_c3 listing is unchanged',
           sorted(set(os.listdir(C.LANE_ROOT)) ^ set(lane_before)))
    record('T_H1_03_build_c3v001_untouched', 'MUST_PASS', 'hygiene: build_c3v001 stays as it is (0679)',
           snapshot(C.LANE_ROOT + '/build_c3v001') == c3v001_before and C.sha256_file(LO_FACADE_C3V001[0]) == LO_FACADE_C3V001[1]
           and C.sha256_file(LO_ADAPTER_C3V001[0]) == LO_ADAPTER_C3V001[1], 'names, sizes and mtimes unchanged; LO shas from bytes',
           len(c3v001_before))


    # ================================================================ c3v003 sections (11-17)
    # ---------------------------------------------------------------- 11. the RHO HELD gate (0696)
    rev = W('rho_gate/CODEX1_PROOF_SIDE_REVIEW_SYNTHETIC_STANDIN.json',
            {'schema': 'SYNTHETIC_REVIEW_STANDIN_C3V003', 'note': 'stands for Codex1\'s proof-side review record; not a review'})
    gate_ok = {'allow_rho': True, 'review_pin': rev, 'review_sha256': rev['sha256']}

    def gate(**kw):
        g = R.rho_gate(**kw)
        return dict(g, ok=g['open'])
    must_fail('T_G01_gate_default_is_held', 'RHO HELD gate', lambda: gate(), 'ALLOW_RHO_NOT_GIVEN')
    must_fail('T_G02_gate_allow_rho_without_root_pin_held', 'RHO HELD gate', lambda: gate(allow_rho=True, review_sha256=rev['sha256']),
              'ROOT_PROVIDED_REVIEW_PIN_MISSING_OR_NOT_AN_EXACT_PIN')
    must_fail('T_G03_gate_sha_not_the_root_pin_held', 'RHO HELD gate',
              lambda: gate(allow_rho=True, review_pin=rev, review_sha256='0' * 64), 'PROOF_SIDE_REVIEW_SHA_DOES_NOT_MATCH_THE_ROOT_PIN')
    must_fail('T_G04_gate_pin_bytes_differ_held', 'RHO HELD gate (bytes read)',
              lambda: gate(allow_rho=True, review_pin=dict(rev, sha256='1' * 64), review_sha256='1' * 64), 'sha256 mismatch')
    must_fail('T_G05_gate_review_inside_runner_out_root_held', 'RHO HELD gate',
              lambda: gate(out_root=os.path.dirname(rev['path']), **gate_ok), 'REVIEW_INSIDE_RUNNER_OUTPUT_ROOT')
    must_fail('T_G06_gate_review_path_uvt_component_held', 'RHO HELD gate (lexical policy)',
              lambda: gate(allow_rho=True, review_pin={'path': fx + '/uvt_x/review.json', 'sha256': '2' * 64}, review_sha256='2' * 64),
              'UVT_COMPONENT_REFUSED')
    must_pass('T_G07_gate_open_with_allow_rho_and_matching_root_pin', 'RHO HELD gate', lambda: gate(**gate_ok),
              lambda v: v['open'] is True and v['status'] == 'OPEN', 'OPEN')
    g_tr = []
    rowh = rows[5]
    must_pass('T_G08_worker_gate_closed_rho_held_and_never_called', 'RHO HELD gate (worker)',
              lambda: R.run_point(rowh, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(rowh, rho_trace=g_tr)),
              lambda v: v[0] == 0 and v[1]['stages'].get('RHO') == R.RHO_HELD and g_tr == [], 'exit 0; RHO HELD; produce_rho never called')
    hdir = os.path.join(out_root, R.point_dir_name(rowh, 1))
    record('T_G08b_held_point_wrote_no_rho_record', 'MUST_FAIL', 'RHO HELD gate (worker)',
           os.path.exists(os.path.join(hdir, 'STAGE_RHO_HELD_%s.json' % rowh['key'][:16])) and
           not any(n.startswith('RHO_NUMERIC_') for n in os.listdir(hdir)) and
           json.load(open(os.path.join(hdir, 'POINT_DONE_%s.json' % rowh['key'][:16])))['rho']['status'] == R.RHO_HELD,
           'STAGE_RHO_HELD written, no RHO_NUMERIC, POINT_DONE rho HELD', sorted(os.listdir(hdir)))
    must_fail('T_G09_cli_unparseable_pin_is_a_held_gate', 'RHO HELD gate (CLI input)',
              lambda: gate(**R.gate_args_from_cli(types.SimpleNamespace(allow_rho=True, proof_side_review_pin='{not json',
                                                                         proof_side_review_sha256=rev['sha256']))),
              'ROOT_PROVIDED_REVIEW_PIN_MISSING_OR_NOT_AN_EXACT_PIN')
    must_pass('T_G10_gate_argv_round_trip', 'RHO HELD gate (worker argv)', lambda: R.gate_argv(gate_ok),
              lambda v: v == ['--allow-rho', '--proof-side-review-pin', json.dumps(rev, sort_keys=True),
                              '--proof-side-review-sha256', rev['sha256']], 'the three gate inputs, unchanged')

    # ---------------------------------------------------------------- 12. the RHO stage (stubbed producers)
    r_tr = []
    rowr = rows[6]
    rr_ = must_pass('T_R01_rho_stage_non_anchor_computed', 'RHO stage (registered, [4,182], 9 shells)',
                    lambda: R.run_point(rowr, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(rowr, rho_trace=r_tr),
                                        rho_gate_args=gate_ok),
                    lambda v: v[0] == 0 and 'RHO_a' in v[1]['stages'] and 'RHO_b' not in v[1]['stages'], 'exit 0; attempt a only')
    rdir = os.path.join(out_root, R.point_dir_name(rowr, 1))
    rk16 = rowr['key'][:16]

    def rho_files():
        st = json.load(open(os.path.join(rdir, 'STAGE_RHO_a_%s.json' % rk16)))
        done = json.load(open(os.path.join(rdir, 'POINT_DONE_%s.json' % rk16)))
        return {'ok': st['ok'], 'checks': st['checks'], 'record': st['record'], 'done_rho': done['rho'],
                'names': sorted(n for n in os.listdir(rdir) if 'RHO' in n), 'pid': st['pid']}
    must_pass('T_R01b_rho_records_and_checks', 'RHO stage (registered, [4,182], 9 shells)', rho_files,
              lambda v: v['ok'] and all(v['checks'].values()) and len(v['checks']) == 9 and v['done_rho']['status'] == 'COMPUTED'
              and v['done_rho']['rho_numeric'] == v['record'] and v['names'] == sorted(
                  ['RHO_NUMERIC_%s_a.json' % rk16, 'RHO_PROGRESS_%s_a.jsonl' % rk16, 'STAGE_RHO_a_%s.json' % rk16]),
              'RHO_NUMERIC/RHO_PROGRESS/STAGE_RHO for attempt a; 9 checks true; POINT_DONE carries the pin')
    must_pass('T_R08_produce_rho_called_registered_full_with_the_eps_context', 'RHO stage call contract', lambda: r_tr,
              lambda v: len(v) == 1 and v[0]['settings'] == 'registered' and v[0]['shell_ranges'] is None
              and isinstance(v[0]['context'], dict) and v[0]['context'].get('details', {}).get('point_sha256') == rowr['key'],
              'one call: settings registered, shell_ranges None, the point context of this worker')
    for i, (cid, over, check_name) in enumerate((
            ('T_R02_smoke_rho_stops', {'settings': 'smoke', 'full_registered_search_executed': False}, 'registered_full_search'),
            ('T_R03_partial_partition_stops', lambda r: dict(r, shells=r['shells'][:8]), 'partition_9_shells_K_big_128'),
            ('T_R04_other_custody_stops', {'custody': dict(custody, grid_sha256='3' * 64)}, 'custody_matches_context'),
            ('T_R05_noncanonical_producer_pin_stops',
             {'producer': {'path': C.CERT + '/./point_response_producer_cx2v002.py', 'sha256': PR_PIN['sha256']}},
             'producer_pin_canonical_R4'),
            ('T_R06_short_coverage_stops', {'required_coverage_inverse_kpc': [4.0, 181.0]}, 'coverage_4_to_182'),
            ('T_R07_negative_rho_used_stops',
             lambda r: dict(r, shells=[dict(r['shells'][0], rho_used=-1e-9)] + r['shells'][1:]), 'rho_used_finite_nonnegative'),
            ('T_R07b_other_point_stops', {'point_sha256': '4' * 64}, 'point_sha256_is_key'))):
        rowx = rows[7 + i]

        def go(rowx=rowx, over=over):
            rc, s = R.run_point(rowx, out_root, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(rowx, rho_override=over),
                                rho_gate_args=gate_ok)
            st = json.load(open(os.path.join(out_root, R.point_dir_name(rowx, 1), 'STAGE_RHO_a_%s.json' % rowx['key'][:16])))
            return {'ok': rc == 0, 'rc': rc, 'stopped': s.get('stopped'), 'failed_checks': sorted(k for k, v in st['checks'].items() if not v)}
        must_fail(cid, 'RHO stage record admissibility', lambda go=go, cn=check_name: (
            lambda v: dict(v, ok=False if (v['rc'] == 3 and v['stopped'] == 'RHO' and cn in v['failed_checks']) else 'NOT_STOPPED'))(go()),
            check_name)

    # ---------------------------------------------------------------- 13. the anchor: two attempts, two processes
    def anchor_root(name):
        p = os.path.join(fx, 'anchor_' + name)
        os.mkdir(p)
        return p

    def inproc_spawn(loader_b):
        def spawn(row_, out_root_, *, attempt, run_id, gate_args):
            rc, rec = R.rho_repeat_point(row_, out_root_, attempt=attempt, run_id=run_id, gate_args=gate_args, loader=loader_b)
            return rc, {'in_process_test_spawn': True}
        return spawn

    def anchor_files(root):
        d = os.path.join(root, R.point_dir_name(anchor, 1))

        def rd(name):                                 # r2: a missing record is an empty dict (the case then fails), not an abort
            try:
                return json.load(open(os.path.join(d, name)))
            except (OSError, ValueError):
                return {}
        return {'pair': rd('ANCHOR_RHO_PAIR_%s.json' % k16), 'a': rd('STAGE_RHO_a_%s.json' % k16),
                'b': rd('STAGE_RHO_b_%s.json' % k16), 'done': rd('POINT_DONE_%s.json' % k16) or {'rho': {}}, 'dir': d}
    ar1 = anchor_root('inproc')
    must_pass('T_A01_anchor_attempts_a_and_b', 'two anchor rho attempts ((a)4)',
              lambda: R.run_point(anchor, ar1, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(), rho_gate_args=gate_ok,
                                  rho_spawn=inproc_spawn(stub_loader())),
              lambda v: v[0] == 0 and 'RHO_a' in v[1]['stages'] and 'RHO_b' in v[1]['stages'], 'exit 0; RHO_a and RHO_b')
    af1 = anchor_files(ar1)
    record('T_A01b_anchor_pair_record_diagnostic', 'MUST_PASS', 'two anchor rho attempts ((a)4)',
           af1['pair'].get('distinct_records') and af1['pair'].get('projection_bitwise_equal_diagnostic') and
           af1['pair'].get('wrapper_v002_10_key_canonical_equal_diagnostic') and af1['a'].get('ok') and af1['b'].get('ok') and
           af1['done']['rho'].get('rho_numeric') == af1['a'].get('record') and af1['done']['rho'].get('rho_numeric_b') == af1['b'].get('record')
           and af1['a'].get('record') is not None,
           'two distinct records, bitwise equal (P and the wrapper 10 keys); POINT_DONE carries a, b and the pair',
           json.dumps(af1['pair'])[:400])
    rule_ = str(af1['pair'].get('rule'))
    record('T_V03_01_runner_pair_rule_names_the_10_key_comparison', 'MUST_PASS',
           'V03 the anchor pair record names the decisive (a)4 comparison (a diagnostic record; A138)',
           'lo_slot_proof_c3v003' in rule_ and "wrapper v002's 10-key canonical comparison" in rule_
           and 'L177-179, L189-191' in rule_ and 'lo_slot_proof_c3v002' not in rule_,
           'decided by lo_slot_proof_c3v003, by wrapper v002\'s 10-key canonical comparison (L177-179, L189-191)', rule_)
    # the separate-process path: attempt b in its own interpreter (probe with stub producers), pid recorded
    probe_dir = os.path.join(fx, 'probe_b_inputs')
    os.mkdir(probe_dir)
    ctx_p = W('probe_b_inputs/stub_context.json', {'point_sha256': key, 'custody': custody, 'custody_sha256': csha, 'identity': ident})
    tpl_p = W('probe_b_inputs/rho_template.json', rho_numeric(ident, key))
    PROBE_B = ("import importlib.util,json,os,sys,types,copy\nsys.dont_write_bytecode=True\n"
               "sp=importlib.util.spec_from_file_location('r_probe_b',sys.argv[1]);m=importlib.util.module_from_spec(sp);"
               "sp.loader.exec_module(m)\n"
               "ctx=json.load(open(sys.argv[3]));tpl=json.load(open(sys.argv[4]))\n"
               "ctx.pop('synthetic_fixture',None);tpl.pop('synthetic_fixture',None)\n"
               "def pc(s): return {'details':ctx,'source_pins':{},'checks':{}}\n"
               "def prho(s,settings='registered',shell_ranges=None,context=None,progress=None):\n"
               " r=copy.deepcopy(tpl);r['settings']=settings;r['synthetic_fixture']='probe b stub';return r\n"
               "ld=lambda:(types.SimpleNamespace(produce=None),types.SimpleNamespace(point_context=pc,produce_rho=prho))\n"
               "row=[x for x in m.C.point_rows() if x['key']==m.C.ANCHOR_KEY][0]\n"
               "rc,rec=m.rho_repeat_point(row,sys.argv[2],attempt=1,run_id='probe',gate_args=json.loads(sys.argv[5]),loader=ld)\n"
               "print(json.dumps({'rc':rc,'pid':os.getpid(),'ok':rec.get('ok')}));sys.exit(rc)\n")

    def proc_spawn(row_, out_root_, *, attempt, run_id, gate_args):
        r_ = subprocess.run([C.TASKPOLICY, '-b', py, '-I', '-B', '-c', PROBE_B, build + '/cp1_runner_c3v004_ks3_c2v002.py', out_root_,
                             ctx_p['path'], tpl_p['path'], json.dumps(gate_args)], capture_output=True, text=True, timeout=300)
        return r_.returncode, {'stdout': r_.stdout[-300:], 'stderr': r_.stderr[-300:]}
    ar2 = anchor_root('subprocess')
    must_pass('T_A02_anchor_attempt_b_in_a_separate_process', 'two separate rho processes at the anchor ((a)4)',
              lambda: R.run_point(anchor, ar2, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(), rho_gate_args=gate_ok,
                                  rho_spawn=proc_spawn),
              lambda v: v[0] == 0 and 'RHO_b' in v[1]['stages'], 'exit 0')
    af2 = anchor_files(ar2)
    record('T_A02b_separate_processes_bitwise_equal', 'MUST_PASS', 'two separate rho processes at the anchor ((a)4)',
           af2['pair'].get('separate_processes') is True and af2['a'].get('pid') == os.getpid() and af2['b'].get('pid') not in (None, os.getpid())
           and af2['pair'].get('projection_bitwise_equal_diagnostic') is True and af2['pair'].get('distinct_records') is True,
           'attempt a in this process, attempt b in another (pids differ); projections equal', json.dumps(af2['pair'])[:400])
    ar3 = anchor_root('ulp')
    ulp = lambda r: dict(r, shells=[dict(r['shells'][0], rho_used=math.nextafter(r['shells'][0]['rho_used'], 1.0))] + r['shells'][1:])
    R.run_point(anchor, ar3, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(), rho_gate_args=gate_ok,
                rho_spawn=inproc_spawn(stub_loader(rho_override=ulp)))
    af3 = anchor_files(ar3)
    must_fail('T_A03_anchor_b_one_ulp_off_diagnostic_reads_unequal', 'two anchor rho attempts ((a)4) diagnostic',
              lambda: {'ok': af3['pair'].get('projection_bitwise_equal_diagnostic', 'PAIR_RECORD_MISSING'), 'why': 'PROJECTION_NOT_BITWISE_EQUAL'},
              'PROJECTION_NOT_BITWISE_EQUAL')
    ar4 = anchor_root('bfail')
    must_fail('T_A04_anchor_attempt_b_failure_stops_the_point', 'two anchor rho attempts ((a)4)',
              lambda: (lambda v: {'ok': v[0] == 0, 'stopped': v[1].get('stopped'), 'reason': v[1].get('reason')})(
                  R.run_point(anchor, ar4, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(), rho_gate_args=gate_ok,
                              rho_spawn=lambda *a_, **k_: (3, {'synthetic': 'attempt b failed'}))),
              'ANCHOR_RHO_ATTEMPT_B_NOT_A_CLEAN_RECORD')
    must_fail('T_A05_rho_repeat_refuses_a_non_anchor_point', 'rho-repeat confinement',
              lambda: R.rho_repeat_point(rowr, out_root, gate_args=gate_ok, loader=stub_loader(rowr)), 'RHO_REPEAT_IS_FOR_THE_ANCHOR_KEY_ONLY')
    must_fail('T_A06_rho_repeat_refuses_a_held_gate', 'rho-repeat confinement',
              lambda: R.rho_repeat_point(anchor, ar1, gate_args={}, loader=stub_loader()), R.RHO_HELD)
    must_fail('T_A07_rho_repeat_never_overwrites_attempt_b', 'rho-repeat confinement (exclusive create)',
              lambda: R.rho_repeat_point(anchor, ar1, gate_args=gate_ok, loader=stub_loader()), 'RHO_ATTEMPT_B_EXISTS')
    ar8 = anchor_root('noa')
    os.mkdir(os.path.join(ar8, R.point_dir_name(anchor, 1)))
    must_fail('T_A08_rho_repeat_needs_attempt_a', 'rho-repeat confinement',
              lambda: R.rho_repeat_point(anchor, ar8, gate_args=gate_ok, loader=stub_loader()), 'No such file')
    calls_b = []

    def fake_call(cmd, **kw):
        calls_b.append(cmd)
        return 0
    saved_call = R.subprocess.call
    try:
        R.subprocess.call = fake_call
        sp_root = anchor_root('spawncmd')
        rcb, infob = R.spawn_rho_repeat(anchor, sp_root, attempt=1, run_id='t', gate_args=gate_ok)
    finally:
        R.subprocess.call = saved_call
    must_pass('T_A09_default_spawn_is_a_separate_taskpolicy_b_I_B_process', 'two separate rho processes at the anchor ((a)4)',
              lambda: calls_b[0], lambda v: v[:5] == [C.TASKPOLICY, '-b', sys.executable, '-I', '-B'] and v[5] == R.RUNNER_PATH
              and v[6] == 'rho-repeat' and v[v.index('--point') + 1] == anchor['key'] and '--allow-rho' in v,
              'taskpolicy -b python3 -I -B cp1_runner_c3v004.py rho-repeat --point <anchor> ... --allow-rho ...')
    clib = subprocess.run([py] + unbg + ['-I', '-B', build + '/cp1_runner_c3v004_ks3_c2v002.py', 'rho-repeat', '--out-root',
                           C.LANE_ROOT + '/cp1_never_created_c3v003', '--point', anchor['key']], capture_output=True, text=True, timeout=120)
    record('T_A10_cli_rho_repeat_without_bg_refused_first', 'MUST_FAIL', 'rho-repeat QoS', clib.returncode == 2
           and 'BACKGROUND_QOS_REQUIRED' in clib.stdout and not os.path.exists(C.LANE_ROOT + '/cp1_never_created_c3v003'),
           'exit 2, nothing created', clib.stdout[-300:])

    # ---------------------------------------------------------------- 14. END TO END: (a)4 pair -> REAL slot proof -> assembler
    SLOT = C.load_exact(C.PINS['lo_slot_proof'][0], C.PINS['lo_slot_proof'][1], 't_real_slot_proof_c3v003')
    RULING_ROOTS = ROOTS + (C.EXCHANGE, '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL')
    a_pin, b_pin = af2['a'].get('record'), af2['b'].get('record')
    spec_e = copy.deepcopy(spec)
    spec_e['numerics']['uv_tail']['lo_certificate'] = a_pin
    spec_e['numerics']['uv_tail']['eps_certificate'] = eps_slot

    def slot_env():
        return types.SimpleNamespace(derive_details=lambda s: {'identity': ident, 'custody': custody, 'point_sha256': key,
                                                               'custody_sha256': csha},
                                     read_pin=lambda ref: C.read_json_pinned(ref, ROOTS, 'slot input', max_bytes=None),
                                     read_raw=lambda ref: C.read_bytes_pinned(ref, RULING_ROOTS, 'slot input', max_bytes=None),
                                     self_pin=SLOT._self_pin, utc=SLOT._utc)

    def prove(rho_ref, pair, reg):
        return SLOT._prove(spec_e, rho_ref, registered_rho_records=reg, anchor_rho_pair=pair,
                           root_ruling_refs=[dict(r) for r in SLOT.ROOT_RULINGS],
                           approved_producer_sha256=[C.PINS['lo_slot_proof'][1]], env=slot_env())
    e1 = must_pass('T_E01_runner_pair_into_the_real_slot_proof_c3v003', 'END TO END: (a)4 pair -> slot proof',
                   lambda: prove(a_pin, [a_pin, b_pin], [a_pin, b_pin]),
                   lambda v: v['verdict'] == 'READY_FOR_MANIFEST' and v['proof']['gate'] == 'LO_RHO_SLOT'
                   and v['proof']['anchor_rho_reproducibility']['records'] == [a_pin, b_pin]
                   and v['proof']['producer'] == SLOT_PIN, 'READY; gate LO_RHO_SLOT; the (a)4 pair is the runner\'s two records')
    must_fail('T_E04_slot_proof_refuses_the_one_ulp_pair', 'END TO END: (a)4 pair -> slot proof',
              lambda: (lambda pa, pb: prove(a_pin, [pa, pb], [a_pin, pa, pb]))(af3['a'].get('record'), af3['b'].get('record')),
              'ANCHOR_RHO_NOT_BITWISE_EQUAL')
    must_fail('T_E05_slot_proof_refuses_one_record_twice', 'END TO END: (a)4 pair -> slot proof',
              lambda: prove(a_pin, [a_pin, a_pin], [a_pin, b_pin]), 'ANCHOR_RHO_PAIR_NOT_TWO_RUNS')
    # c3v004 V03: attempt b differs from attempt a only by 1 ulp in a diagnostic (shell 0 rho_envelope.estimate).
    ar5 = anchor_root('diag_ulp')
    diag = lambda r: dict(r, shells=[dict(r['shells'][0], rho_envelope=dict(r['shells'][0]['rho_envelope'], estimate=math.nextafter(
        r['shells'][0]['rho_envelope']['estimate'], 1.0)))] + r['shells'][1:])
    R.run_point(anchor, ar5, operator_lane='SYNTHETIC_OPERATOR', loader=stub_loader(), rho_gate_args=gate_ok,
                rho_spawn=inproc_spawn(stub_loader(rho_override=diag)))
    af5 = anchor_files(ar5)

    def diag_pair():
        pa, pb = af5['a'].get('record'), af5['b'].get('record')
        res = prove(a_pin, [pa, pb], [a_pin, pa, pb])
        if not (af5['pair'].get('projection_bitwise_equal_diagnostic') is True
                and af5['pair'].get('wrapper_v002_10_key_canonical_equal_diagnostic') is False):
            return {'verdict': 'PAIR_DIAGNOSTICS_NOT_AS_EXPECTED', 'pair': af5['pair'], 'slot': res}
        return res
    must_fail('T_V03_02_one_ulp_diagnostic_pair_refused_by_the_real_slot_proof_c3v003',
              'V03 the (a)4 decision is wrapper v002\'s 10-key canonical comparison (A138), end to end', diag_pair,
              'ANCHOR_RHO_NOT_BITWISE_EQUAL')
    e_root = os.path.join(b_root, 'e2e')
    os.mkdir(e_root)
    slot_pf = (SLOT.write_proof(e1, e_root, 'LO_RHO_SLOT_PROOF_E2E.json')
               if (e1 or {}).get('verdict') == 'READY_FOR_MANIFEST' else None)

    def e2e_registry():
        b = A.assemble_bundle(anchor, eps_proof=eps_pf['path'], gq_proof=gq_pf['path'], lo_proof=slot_pf['path'],
                              approved=approved, out_root=e_root, roots=ROOTS)
        reg, man = A.assemble_registry([b['path']], approved=approved, out_root=e_root, roots=ROOTS)
        return b, reg, man
    e2 = must_pass('T_E02_bundle_registry_from_the_real_slot_proof', 'END TO END: slot proof -> assembler', e2e_registry,
                   lambda v: v is not None and readpin(v[1])['points'][key]['lo_certificate'] == a_pin
                   and readpin(v[0])['prelaunch']['LO_RHO_SLOT'] == slot_pf and 'LO_ENVELOPE' not in readpin(v[0])['prelaunch'],
                   'bundle prelaunch LO_RHO_SLOT = the real proof; registry lo_certificate = the anchor rho a')
    e3 = must_pass('T_E03_offline_verifier_ok_wrapper_v002_bytes_and_L30_guard', 'END TO END: assembler -> offline verifier',
                   lambda: verify(e2[1]), lambda v: v['ok'] is True and v['points'][0]['guard_b1']['ok'] is True
                   and v['points'][0]['wrapper_replica']['block']['block_sha256'] ==
                   '4ea218ea15df9a5e4897946fc1bccd2edaa4eba8edcb878b07407429c1207710'
                   and v['points'][0]['wrapper_replica']['block']['wrapper']['sha256'].startswith('7a6af535'),
                   'ok: the executed block is wrapper v002 L145-191 (block sha 4ea218ea, as the proof side W07 read it)')
    must_fail('T_E06_verifier_refuses_old_slot_rule_string', 'root slot-rule string (0697)',
              lambda: verify(e2[1], c1=c1_fixture(e2[1], approved, review_over={'driver_slot_rule': 'POINT_EPS_AND_REVIEWED_PRELAUNCH_LO_ENVELOPE'})),
              'binding mismatch: driver_slot_rule')
    must_fail('T_E07_verifier_refuses_claude3_proposed_slot_rule', 'root slot-rule string supersedes the proposal (0697)',
              lambda: verify(e2[1], c1=c1_fixture(e2[1], approved, review_over={'driver_slot_rule': 'POINT_EPS_AND_REGISTERED_RHO_LO_SLOT_PER_STATE_ACCEPTANCE'})),
              'binding mismatch: driver_slot_rule')
    must_fail('T_E08_verifier_refuses_guard_v003_binding', 'guard binding follows wrapper v002 L30',
              lambda: verify(e2[1], c1=c1_fixture(e2[1], approved, review_over={'guard_sha256': C.PINS['guard_v003'][1]})),
              'binding mismatch: guard_sha256')
    must_fail('T_E09_verifier_refuses_C1_without_the_slot_producer', 'unapproved producer',
              lambda: verify(e2[1], appr=[AD_PIN, GQ_PIN]), 'LO_RHO_SLOT producer is not approved')

    def wrapper_changed():
        saved = A.C.PINS['wrapper_q5b1']           # the assembler's own common module object
        A.C.PINS['wrapper_q5b1'] = (saved[0], '7' * 64)
        try:
            return verify(e2[1])
        finally:
            A.C.PINS['wrapper_q5b1'] = saved
    must_fail('T_E10_verifier_refuses_wrapper_bytes_not_7a6af535', 'wrapper v002 pin (bytes)', wrapper_changed, 'sha256 mismatch')

    # ---------------------------------------------------------------- 15. assembler LO_RHO_SLOT acceptance and refusals
    proof_doc = readpin(slot_pf) if slot_pf else dict(readpin(lo_pf))   # r2: the synthetic proof if E2E failed
    for cid, doc, code in (
            ('T_B01_assembler_refuses_LO_ENVELOPE_proof', dict(proof_doc, gate='LO_ENVELOPE', covers_all_consumed_states=True),
             'LO_RHO_SLOT_PROOF_SCHEMA_OR_GATE'),
            ('T_B02_assembler_refuses_covers_all_key', dict(proof_doc, covers_all_consumed_states=False),
             'LO_RHO_SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES'),
            ('T_B03_assembler_refuses_cover_all_key', dict(proof_doc, cover_all_consumed_states=True),
             'LO_RHO_SLOT_PROOF_CARRIES_COVER_ALL_CONSUMED_STATES'),
            ('T_B06_assembler_refuses_proof_rho_record_other_than_its_slot', dict(proof_doc, rho_record=b_pin),
             'LO_RHO_SLOT_PROOF_RHO_RECORD_DIFFERS_FROM_ITS_DRIVER_CERTIFICATE')):
        fp = W('asm_refusals/%s.json' % cid, doc)
        must_fail(cid, 'assembler LO_RHO_SLOT (A134 Q5)', lambda fp=fp: build_reg(cid[:6], lo=fp), code)
    lo_num = W('asm_refusals/LO_NUMERIC_AS_SLOT.json', {'schema': 'UNT_POINT_LO_NUMERICAL_CX2V001', 'gate': 'LO', 'identity': ident,
                                                        'custody': custody, 'point_sha256': key})
    must_fail('T_B04_assembler_refuses_a_non_rho_slot_record', 'assembler LO_RHO_SLOT (A134 Q5)',
              lambda: build_reg('B04', lo=W('asm_refusals/B04_proof.json', dict(proof_doc, driver_certificate=lo_num, rho_record=lo_num))),
              'LO_SLOT_RECORD_IS_NOT_THIS_POINTS_RHO_RECORD')
    smoke_rho = W('asm_refusals/RHO_SMOKE.json', rho_numeric(ident, key, settings='smoke'))
    must_fail('T_B05_assembler_refuses_a_smoke_rho_record', 'assembler LO_RHO_SLOT (A134 Q5)',
              lambda: build_reg('B05', lo=W('asm_refusals/B05_proof.json', dict(proof_doc, driver_certificate=smoke_rho, rho_record=smoke_rho))),
              'SMOKE_OR_PARTIAL_RHO_RECORD_REFUSED')
    must_pass('T_B11_guard_binding_follows_wrapper_v002_L30', 'guard binding follows wrapper v002 L30',
              lambda: (A.wrapper_l30_guard_pin(), C.sha256_file(G.__file__), G.__file__),
              lambda v: v[0] == {'path': C.ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', 'sha256': GUARD_B1}
              and v[1] == GUARD_B1 and v[2] == v[0]['path'], 'b1 9e3fc109, loaded from the path and sha that L30 names')

    def pins_c3v004():
        return {'wrapper': C.PINS.get('wrapper_q5b1'), 'slot': C.PINS.get('lo_slot_proof'), 'canon': list(C.CANONICAL_APPROVED_PRODUCERS),
                'slot_bytes': C.sha256_file(C.PINS['lo_slot_proof'][0]),
                'canonical_paths': all(os.path.realpath(p) == p for p, _ in C.PINS.values())}
    must_pass('T_B12_common_c3v004_pins', 'common c3v004: wrapper v002 at its published path (V09) and slot producer c3v003',
              pins_c3v004, lambda v: tuple(v['wrapper']) == (PUBLISHED_WRAPPER, WRAPPER_SHA)
              and v['slot'][0] == C.LANE_ROOT + '/proof_side_c3v003/lo_slot_proof_c3v003.py' and v['slot_bytes'] == v['slot'][1]
              and v['canon'] == ['eps_adapter', 'gq_producer', 'lo_slot_proof'] and v['canonical_paths'],
              'wrapper_q5b1 = the published path, 7a6af535 (not opened); lo_slot_proof c3v003 from bytes; canonical EPS, GQ, '
              'LO_RHO_SLOT')
    must_pass('T_B13_registry_manifest_names_wrapper_v002_L30_guard_and_rule', 'assembler manifest',
              lambda: readpin(e2[2]), lambda m: m['guard'] == {'path': C.ART + '/s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py',
                                                               'sha256': GUARD_B1}
              and m['wrapper'] == A.C.canonical_pin('wrapper_q5b1') == {'path': LAYOUT_PIN['path'], 'sha256': WRAPPER_SHA}
              and m['slot_rule'] == ROOT_RULE, 'guard b1; wrapper v002 = the assembler common pin (here the V09 test layout); root rule')
    must_pass('T_B14_assembler_constants', 'root slot-rule string; LO_RHO_SLOT; block lines',
              lambda: (A.SLOT_GATE, A.SLOT_RULE, A.WRAPPER_BLOCK_LINES, A.FORBIDDEN_PROOF_KEYS),
              lambda v: v == ('LO_RHO_SLOT', ROOT_RULE, (145, 191), ('covers_all_consumed_states', 'cover_all_consumed_states')),
              'constants as ruled')

    # ---------------------------------------------------------------- 18. c3v004 (A138): V09 and V02
    must_pass('T_V09_01_canonical_wrapper_pin_is_the_published_path', 'V09 the wrapper pin is the published path, same sha (A138/A139)',
              lambda: {'runner_common': tuple(C.PINS['wrapper_q5b1']), 'assembler_common_before_override': CANON_WRAPPER_PIN,
                       'core_dir': os.path.dirname(C.PINS['core_r10_c4'][0])},
              lambda v: v['runner_common'] == v['assembler_common_before_override'] == (PUBLISHED_WRAPPER, WRAPPER_SHA)
              and os.path.dirname(PUBLISHED_WRAPPER) == v['core_dir'] and v['runner_common'][0] != BUILD_WRAPPER
              and os.path.normpath(PUBLISHED_WRAPPER) == PUBLISHED_WRAPPER,
              'calib_tail_readiness_cx2/v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py beside core dc895f8a (wrapper '
              'L27), sha 7a6af535, not the build_v002 path; a string check (the file is not opened)')
    must_pass('T_V09_02_test_layout_copy_and_override_are_test_only', 'V09 the suite does not require the published file',
              lambda: {'layout_sha': C.sha256_file(LAYOUT_PIN['path']), 'override': tuple(A.C.PINS['wrapper_q5b1']),
                       'separate_modules': A.C is not C, 'runner_common': tuple(C.PINS['wrapper_q5b1']),
                       'block_wrapper': ((((e3 or {}).get('points') or [{}])[0].get('wrapper_replica') or {}).get('block')
                                         or {}).get('wrapper')},
              lambda v: v['layout_sha'] == WRAPPER_SHA and v['override'] == (LAYOUT_PIN['path'], WRAPPER_SHA) and v['separate_modules']
              and v['runner_common'] == (PUBLISHED_WRAPPER, WRAPPER_SHA)
              and v['block_wrapper'] == {'path': LAYOUT_PIN['path'], 'sha256': WRAPPER_SHA},
              'the layout copy is byte-identical (7a6af535); only the assembler common is overridden; the executed L145-191 block '
              'came from that copy')
    must_pass('T_V02_01_common_state_enumerator_pin_is_b1', 'V02 the C1 enumerator is the b1 enumerator 4ca7f364 (A138)',
              lambda: {'pin': tuple(C.PINS['state_enumerator']), 'bytes': C.sha256_file(C.PINS['state_enumerator'][0])},
              lambda v: v['pin'] == B1_ENUM and v['bytes'] == B1_ENUM[1] and v['bytes'] != V010_ENUM_SHA,
              'consumed_states_b1_c2v001.py, 4ca7f364 from bytes')
    must_pass('T_V02_02_registry_manifest_c1_state_enumerator_is_b1', 'V02 the registry manifests carry the b1 enumerator (A138)',
              lambda: [readpin(m_)['c1_tail_readiness_fields']['state_enumerator'] for m_ in (man_ok, e2[2])],
              lambda v: v == [{'path': B1_ENUM[0], 'sha256': B1_ENUM[1]}] * 2, 'both registry manifests: the b1 enumerator 4ca7f364')
    # ---------------------------------------------------------------- 16-17. hygiene (c3v003)
    record('T_H2_01_build_c3v002_and_proof_sides_untouched', 'MUST_PASS', 'hygiene: build_c3v002, proof_side_c3v001/c3v002 code',
           snapshot(C.LANE_ROOT + '/build_c3v002') == c3v002_before and snapshot(C.LANE_ROOT + '/proof_side_c3v001') == ps1_before
           and [C.sha256_file(C.LANE_ROOT + '/proof_side_c3v002/' + n) for n in PS2_CODE] == ps2_before,
           'names, sizes and mtimes unchanged; proof_side_c3v002 code shas unchanged', [len(c3v002_before), len(ps1_before)])
    record('T_H2_02_build_c3v003_proof_side_c3v002_and_c3v003_code_untouched', 'MUST_PASS',
           'hygiene: build_c3v003 and proof_side_c3v002 (every HASHES-listed file), proof_side_c3v003 code (c3v004)',
           [hashed_snapshot(p, h) for p, h in HASHED] == hashed_before and all(len(x) > 1000 for x in hashed_before)
           and [C.sha256_file(C.LANE_ROOT + '/proof_side_c3v003/' + n) for n in PS3_CODE] == ps3_before,
           'names, sizes and mtimes of every listed file unchanged; proof side c3v003 code shas unchanged',
           [len(x) for x in hashed_before])
    record('T_V09_03_published_wrapper_never_opened', 'MUST_PASS', 'V09 the suite does not require the published file',
           PUBLISHED_OPENS == [], 'no open() of the published path in this process (audit hook from the start)', PUBLISHED_OPENS)
    pub_present = os.path.exists(PUBLISHED_WRAPPER)
    record('T_V09_04_published_wrapper_absent_or_byte_equal', 'MUST_PASS', 'V09 the published copy, if present, is 7a6af535',
           (not pub_present) or C.sha256_file(PUBLISHED_WRAPPER) == WRAPPER_SHA,
           'absent, or byte-equal to the pin (read once, after T_V09_03)', 'present' if pub_present else 'absent')
    # ---------------------------------------------------------------- summary
    n_fail = [r for r in RESULTS if not r['passed']]
    by_kind = {k: sum(1 for r in RESULTS if r['kind'] == k) for k in ('MUST_PASS', 'MUST_FAIL')}
    reqs = sorted({r['requirement'] for r in RESULTS})
    summary = {'schema': 'S4RC1_C3V004_SYNTHETIC_TEST_RESULTS', 'utc': C.utc(), 'build_dir': build,
               'tools': {n: C.sha256_file(os.path.join(build, n)) for n in sorted(os.listdir(build)) if n.endswith('.py')},
               'held_lo_files_read_only_for_root_gate_cases': [{'path': p, 'sha256': s} for p, s in (LO_FACADE_C3V001, LO_ADAPTER_C3V001)],
               'dropped_c3v001_lo_cases': list(DROPPED_C3V001_LO_CASES),
               'guard_l30': _safe(A.wrapper_l30_guard_pin), 'fixture_root': fx, 'counts': dict(by_kind, total=len(RESULTS)),
               'passed': len(RESULTS) - len(n_fail), 'failed': len(n_fail), 'failed_ids': [r['id'] for r in n_fail],
               'requirements_covered': reqs, 'cases': RESULTS,
               'scope': 'SYNTHETIC only; no producer ran on a real point input; no run tree read; no launch'}
    pin = C.write_new(os.path.join(fx, 'TEST_RESULTS_%s.json' % C.utc_compact()), summary, fx)
    man = write_manifest(fx, pin)                     # F11 rule for this suite too
    print(json.dumps({'passed': summary['passed'], 'failed': summary['failed'], 'counts': summary['counts'],
                      'failed_ids': summary['failed_ids'], 'results': pin, 'synthetic_outputs_manifest': man}, indent=1))
    return 0 if not n_fail else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    finally:
        bad = [r for r in RESULTS if not r['passed']]
        if bad:
            sys.stderr.write('FAILED CASES (%d of %d):\n' % (len(bad), len(RESULTS)))
            for r in bad:
                sys.stderr.write('  %s | %s | expected %s | observed %s\n' % (r['id'], r['kind'], r['expected'], r['observed'][:400]))
