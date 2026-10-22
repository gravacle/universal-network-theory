"""Tests for the campaign certification build c2v004 (Claude2; V006 A192 item 3, verifier B1: ADV rows C03, C04).  SYNTHETIC
launches only.

c2v004 against test_campaign_cert_c2v003 (6fd12500): every c2v003 row is ported to the c2v004 chain (generator, regenerate,
wrapper source, entry template, acceptance step, placeholder chain c2v004); rows that named c2v003 now name c2v004, and:
  G03  compares the c2v004 generator with c2v003's (policy and core equal; wrapper and entry differ);
  G05  seven q5b1 lines replaced (c2v003's six plus the reingest signature); G06 the wrapper and entry deltas against c2v003;
  K04  the acceptance step c2v004 refuses a c2v003-line entry;
  EB14 (C04) a second pass after a NON_LAPSE first pass refuses (it ran in c2v003);
  EB26-EB28 the rerun after INCOMPLETE: refused without / with another call's / with a changed first-pass record; runs with
       the call's own INCOMPLETE record; a third pass refuses;
  U01  the wrapper's pass rule (A001..A<n> oldest first; a gap or a foreign ACCEPTANCE_TAILSTATES_* entry refuses);
  EB29-EB34 wave 4 (certified through the CP-1 list successor and the ledger): C03 (no second pass after an ACCEPTED first
       pass; reingest_invalid refuses while the call dir holds TAIL_CERTIFICATE_ACCEPTANCE.json), the stale-record VALID
       reingest and the stale-record reingest_invalid (MUST_FAIL), and one INFO row measuring the declared residual (a pass
       made by calling the handoff directly, outside the step).
Added declared substitutions (TOY_SEPARATION): EB31 writes TAIL_CERTIFICATE_ACCEPTANCE.json with the wrapper's own
write_acceptance in process (standing for a VALID reingest that stopped before its cache put); EB31 and EB33-EB34 make a
second pass by calling the adopted handoff v004 directly in process (the bypass the step cannot see).
Text below is c2v003's.

Tests for the campaign certification build c2v003 (Claude2; V006 A192 items 2-5).  SYNTHETIC launches only.

Rows are MUST_PASS (the rule accepts / holds) or MUST_FAIL (the rule refuses); a row passes when the outcome matches.
  G/R  generator make_campaign_cascade_c2v003 and regenerate_h3_c2v003 (the wrapper source with the ledger and F6).
  K    the REAL chain bytes, dry (v004a, placeholder c2v003 chain; a local never-created work dir): the ledger code is inert
       without tail_readiness.certificate_ledger.
  P    the CP-1 list-of-points successor: table mode IS c3v004; list rules; anchor gating; the worker command.
  H    the HEADLINE11 evidence assembler (deciding + capability documents; the A192 item 4 reuse test).
  A    apply_h3_fields_c2v003 (the ledger policy field).
  EA   world A, genesis = W1's points: W1; wave 2 is UNREGISTERED (refused), certified by the CP-1 list successor (mock),
       appended to the ledger, planned, run, accepted, reused; ledger-append refusals; forged ledgers refuse.
  EB   world B, genesis = W1 + wave 2 (pre-registered, like CP-1 rows 28-31): W1, wave 2; wave 3 (engine-chosen, march0-style)
       refused until the CP-1 list successor certifies it and the ledger takes it; wave 3 accepted with the F6 readings:
       NON_LAPSE_TAIL_MATERIAL and BOUND_INSUFFICIENT -> certified MODEL_INVALID; MUST_FAIL MODEL_INVALID on an ACCEPTED
       call, on another call's record, on an INCOMPLETE record; the rerun limit; reuse; tampering.
  S    storage_check_h3_c2v003 (b = call dir bytes after acceptance; the 17.08 GiB threshold regression).
  Z    every named input unchanged; no publish; the audit.
Declared synthetic substitutions (TOY_SEPARATION), on top of c2v002's (mock driver identity in core/wrapper DRIVER_SHA and
core BASE; the handoff's LO_ADAPTER; v004a with work dir, driver, taxonomy and anchor.driver_sha256 replaced):
  * the synthetic module is syn_h3_c2v003 (syn_h3_c2v001 + two reading switches driven by root_ruling_refs);
  * the c3v004 commons loaded by the CP-1 successor get DRIVER_SHA := the mock's, canonical pins custody / response_producer /
    gq_producer / eps_adapter / lo_slot_proof := synthetic stubs in the run, and background_qos := True (the runner's QoS
    precondition); run_point / adapt_point get mock_cp1_c2v003's producers through their own injection points; the
    Scheduler gets in-process spawn, memory, swap and vm_stat stand-ins; the LO_RHO_SLOT proof is written by mock_cp1 in
    place of root's proof-side step; the c3v004 out-root's anchor records (STAGE_CONTEXT, AGREE cross-check) are synthetic
    stand-ins, because a list run continues on CP-1's own out-root;
  * EB13's accept step runs with the entry's reingest replaced by a stub (as c2v002 EB19), to obtain an ACCEPTED record of a
    call that is not cached yet.
Nothing real is launched: the only subprocesses are the pinned python running the root monitor (mock calls), this file in
--child mode, and ps.
usage: <codex python3> -I -B tests/test_campaign_cert_c2v004.py [--runs-root DIR]   (c2v004)
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS',
           'BLIS_NUM_THREADS'):
    os.environ[_v] = '1'
import argparse
import contextlib
import copy
import datetime
import difflib
import hashlib
import importlib.util
import io
import json
import platform
import shutil
import subprocess
import sys
import time
import traceback
import types
from pathlib import Path

HERE = Path(os.path.dirname(os.path.realpath(__file__)))
H3 = HERE.parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
CX2 = ART / 'calib_tail_readiness_cx2'
GiB = 1 << 30
RAM = 137438953472
NAMED = {
    'parent': (ART / 'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py', 'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d'),
    'monitor': (ART / 'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py', 'ba031c2340057d88ee399138cc645012a93aa7dc3eb7c9bba56d112c94a47107'),
    'driver_r5': (ART / 'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py', 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'),
    'core_r9': (CX2 / 'v006r9/calibration_core_cx2v006r9.py', 'a595c5c0929fc0a8313bcdff3b79241f1e3ba8f77dc3749adc06b2a982b43605'),
    'policy_r7': (CX2 / 'v006r7/adoption_policy_cx2v006r7.py', '7c726fa2ad3f3e0fbcfcf36353901f970cde1eff3f76321327e5a8a5fbc29b1d'),
    'policy_r10_c4': (CX2 / 'v006r10_c4/adoption_policy_cx2v006r10_c4.py', '93d9c0acdb3e9fd40ec63ed0db7c1356b6d2b025eeb5bcde57a2ffebdbd04ba3'),
    'core_r10_c4': (CX2 / 'v006r10_c4/calibration_core_cx2v006r10_c4.py', 'dc895f8a993295b76a42b563893e990d2419432db78485dd387ddc232ff449d6'),
    'wrapper_q5b1': (CX2 / 'v006r10_c4/calibration_orchestrator_cx2v006r10_c4_q5b1.py', '7a6af535805399d49ec3f1c1cbe9e4911d98f6fae0ad50b69a0641214fcd5d4d'),
    'sensitivity': (CX2 / 'v006r8/sensitivity_policy_cx2v006r8_v002.py', '8fb0660077d56ddc787ac67386f8def72e6f5a04fd14e44eb20ed9facf19de4f'),
    'guard_b1': (ART / 's4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py', '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'),
    'handoff_v004': (ART / 's4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py', '5ff464cc866d3e69ef83ab7542701b211afaae29d7be14e69b10fb09f16692d8'),
    'config_v004a': (ART / 'sched_s45_c2/v004a/RUN_CONFIG_DDO154_CX2V006R9_S45_C2V004A.json', '63dac53de88303404c64e899856485bd912a4c493e44a93af0a6cb393240e4ec'),
    'taxonomy': (CX2 / 'v006r6/FAILURE_TAXONOMY_CX2V006R6_CANDIDATE.json', '0ad99c668377fcc60e754a377499fa1da15b2c1462486ef8631b05e8b023460c'),
    'cp1_runner': (ART / 's4rc1_c3/build_c3v004/cp1_runner_c3v004.py', '3f5e5c188d4a6967afdb3bfab805d1cc8650e9c26793895096be55ca8f4f1a48'),
    'cp1_common': (ART / 's4rc1_c3/build_c3v004/s4rc1_common_c3v004.py', '53f10e6eeef62518d7ac9cb21089331b797c5c25efeaa6df3664ff9fbbe51083'),
    'cp1_assembler': (ART / 's4rc1_c3/build_c3v004/registry_assembler_c3v004.py', 'cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0'),
    'entry_c2v002': (H3 / 'h3_campaign_entry_c2v002.py', '75b4cafa8563e31879ab1d70a74fe64dba9f4d61f496c3bc28479668c1e61c10'),
    'accept_c2v002': (H3 / 'h3_accept_call_c2v002.py', 'c9058dd5b2868b40660d9b39103939a9b5fad9967fa70bcacd6f19af16d9b89f'),
    'generator_c2v002': (H3 / 'make_campaign_cascade_c2v002.py', 'bbb9d6568894f615ab798003ddd285defed10c5ef9dc95d4dd5444f55ac1ab28'),
    'regenerate_c2v002': (H3 / 'regenerate_h3_c2v002.py', '0fc614f5a1fe7a7c8fc5bba9aa3cf783888dc1b00c3cddd14f2a1bc7625ca1f1'),
    'apply_c2v001': (H3 / 'apply_h3_fields_c2v001.py', '2e4a5393b5a1624b61c91424eaa90a61ce16cf2ef17dec60118158486e97877f'),
    'builder_c2v001': (H3 / 'build_adoption_derivation_c2v001.py', '01a4cbae729a0c44df2ea1f4cc500ae95669cb9ff6a7541bc94621c23c2294bd'),
    'storage_c2v001': (H3 / 'storage_check_h3_c2v001.py', 'e0b3a89a4a2930311c393cd62d2f51b0b343fe705736d8083a45628c8a75706d'),
    'seal_placeholder': (H3 / 'SEAL_TUPLE_RECORD_H3_C2V001_PLACEHOLDER.json', 'd43419be3cfe61684b68643e2edd1b199740c478a606f946d7bd5bf8d114cadf'),
    'syn_mock': (H3 / 'tests/synthetic/mock_driver_h3_c2v001.py', '374c508e83a6c6a8714be0e4cf25c08fe6d8325671603decdd36c75f5165f57c'),
    'wrapper_c2v003': (H3 / 'calibration_orchestrator_q5b1_ledger_c2v003.py', '5ea1780a1008b5158ca4e431bafc9f6597d7adcefd682423abb3bbbca81d6c2c'),
    'entry_c2v003': (H3 / 'h3_campaign_entry_c2v003.py', '5710e1fa457956087ac6a3e7e4484d51c30f3729b49788ea95c6f3d0a963f983'),
    'accept_c2v003': (H3 / 'h3_accept_call_c2v003.py', 'ae5ab4a6ab8e2e9931a090cc96d76a65ec31beb552badafa3b80e03383b00556'),
    'generator_c2v003': (H3 / 'make_campaign_cascade_c2v003.py', 'd7e6d77a8894687cd249a97daaef3c1286782586693af9d01774385e8a32e37a'),
    'regenerate_c2v003': (H3 / 'regenerate_h3_c2v003.py', '1a17239d29b011053eb20201df6dc7b87255ff408eda0129df5b8e492873a266'),
}
GEN = H3 / 'make_campaign_cascade_c2v004.py'
WRAP_SRC = H3 / 'calibration_orchestrator_q5b1_ledger_c2v004.py'
ENTRY_T = H3 / 'h3_campaign_entry_c2v004.py'
REGEN = H3 / 'regenerate_h3_c2v004.py'
ACCEPT = H3 / 'h3_accept_call_c2v004.py'
APPLY = H3 / 'apply_h3_fields_c2v003.py'
STORAGE = H3 / 'storage_check_h3_c2v003.py'
CP1R = H3 / 'cp1_points_runner_c2v001.py'
CP1A = H3 / 'cp1_points_assembler_c2v001.py'
CP1C = H3 / 'cp1_points_common_c2v001.py'
H11 = H3 / 'h11_evidence_assembler_c2v001.py'
SYN_SRC = H3 / 'tests' / 'synthetic'
SUB = 'v006r12_c4'
SEED_KEY16 = '968c915bece706ea'
SEED_SPEC_V004A = '3958aed31353908f'
SCHEMA_REPORT = 'UNT_KMAX_TAIL_COMPARISON_C2V007_R11'
LEDGER_SCHEMA = 'DDO154_CERTIFICATE_LEDGER_C2V003'
STUB_STATUS = 'TEST_STUB_REINGEST_NOT_CALLED'
SOURCE_PINS = {'synthetic_source_pins': 'H3_C2V003'}
RESULTS = []
AUDIT = {'denied': [], 'subprocess': {}, 'n_opened': 0}
STATE = {'run_dir': None}
WORLD_CTX = {}


# ------------------------------------------------------------------------------------------------ audit, helpers
def _audit(event, args):
    rd = STATE['run_dir']
    if event == 'open':
        p = args[0]
        if not isinstance(p, (str, bytes, os.PathLike)):
            return
        p = os.path.abspath(os.fsdecode(p))
        mode, flags = args[1], args[2]
        w = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or \
            (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC)))
        AUDIT['n_opened'] += 1
        if w and not (rd and p.startswith(rd + '/')) and not p.startswith('/dev/'):
            AUDIT['denied'].append(['write', p])
            raise PermissionError('audit: write outside the run dir refused: %s' % p)
        bad = (p.startswith('/Volumes/') or '/runs_ext/' in p or '/runs/' in p or 'UNT_INTERNAL_RUNS' in p or '/arrays/' in p
               or '/node_diagnostics/' in p or '/UVT_' in p or 'C5H' in p or 'c5h_hull_c2' in p or '/.codex/' in p
               or 'V007_SEAL_ASSEMBLY' in p or '/cp1_run_' in p or ('ngc3198' in p.lower() and not p.endswith('.py')))
        if bad:
            AUDIT['denied'].append(['read', p])
            raise PermissionError('audit: forbidden read refused: %s' % p)
    elif event in ('subprocess.Popen', 'os.posix_spawn', 'os.system', 'os.fork'):
        if event != 'subprocess.Popen':
            AUDIT['denied'].append(['exec', event])
            raise PermissionError('audit: %s refused' % event)
        exe = os.fsdecode(args[0]) if args[0] is not None else os.fsdecode(args[1][0])
        AUDIT['subprocess'][exe] = AUDIT['subprocess'].get(exe, 0) + 1
        if exe not in (PY, 'ps'):
            AUDIT['denied'].append(['exec', exe])
            raise PermissionError('audit: subprocess refused: %s' % exe)


def no_subprocess_platform():
    platform.platform = lambda *a, **kw: 'h3 test: no subprocess ' + repr(os.uname())
    platform._Processor.get = staticmethod(lambda: os.uname().machine)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), allow_nan=False)


def jbytes(o):
    return (json.dumps(o, indent=1, sort_keys=True, allow_nan=False) + '\n').encode()


def put_x(path, obj, raw=None):
    path = Path(path)
    b = raw if raw is not None else jbytes(obj)
    with open(path, 'xb') as f:
        f.write(b)
    return {'path': str(path), 'sha256': sha_b(b)}


def load(path, name):
    raw = Path(path).read_bytes()
    sp = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    exec(compile(raw, str(path), 'exec'), m.__dict__)
    return m


def flat(o, pre=''):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            out.update(flat(v, pre + k + '.') if isinstance(v, dict) and v else {pre + k: v})
        return out
    return {pre[:-1]: o}


def leaf_diff(a, b):
    fa, fb = flat(a), flat(b)
    return sorted(k for k in set(fa) | set(fb) if fa.get(k, '<absent>') != fb.get(k, '<absent>'))


def check(tid, expect, ok, detail=None):
    RESULTS.append({'id': tid, 'expect': expect, 'pass': bool(ok), 'detail': detail})
    print('%s %-9s %-96s %s' % ('PASS' if ok else 'FAIL', expect, tid, json.dumps(detail, default=str)[:240]), flush=True)


def guard(tid, fn):
    try:
        fn()
    except BaseException as exc:                                # noqa: BLE001 -- a crash is a FAIL row
        if isinstance(exc, KeyboardInterrupt):
            raise
        check(tid, 'CRASH', False, {'raised': '%s: %s' % (type(exc).__name__, exc), 'tb': traceback.format_exc()[-3000:]})


def quiet(fn, *a, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        try:
            r = fn(*a, **kw)
        except SystemExit as exc:
            r = ('SYSTEM_EXIT', exc.code)
    return r, buf.getvalue()


def last_json(text):
    s = text.strip()
    i = s.find('{')
    return json.loads(s[i:]) if i >= 0 else None


def gen():
    return load(GEN, '_c3_gen_%d' % time.monotonic_ns())


def build_layout(root, publish_root=None, seal_tuple=None, G=None):
    G = G or gen()
    files, outputs, _ = G.build(SUB, seal_tuple=seal_tuple, publish_root=str(publish_root or root))
    root = Path(root)
    root.mkdir()
    (root / SUB).mkdir()
    (root / 'v006r8').mkdir()
    shutil.copyfile(NAMED['sensitivity'][0], root / 'v006r8' / NAMED['sensitivity'][0].name)
    for n, b in files:
        put_x(root / SUB / n, None, raw=b)
    return {n: str(root / SUB / n) for n, _ in files}, outputs


def load_entry(path):
    return load(path, '_c3_entry_%d' % time.monotonic_ns())


def patch_chain(W, world):
    W.M.DRIVER_SHA = world['mock_sha']
    W.M.BASE = Path(world['syn_base'])
    W.DRIVER_SHA = world['mock_sha']
    return W


def patch_handoff(H, world):
    H.LO_ADAPTER = dict(world['syn_module'], entry='adapt_call_lo')
    return H


# ------------------------------------------------------------------------------------------------ child mode
def child(spec_path):
    spec = json.loads(Path(spec_path).read_text())
    STATE['run_dir'] = spec['run_dir']
    no_subprocess_platform()
    sys.addaudithook(_audit)
    buf = io.StringIO()
    rc = None
    try:
        with contextlib.redirect_stdout(buf):
            E = load_entry(spec['entry'])
            W = E.load_wrapper()
            if spec.get('world'):
                patch_chain(W, spec['world'])
            if spec['kind'] == 'entry':
                rc = E.dispatch(W, spec['argv'])
            else:
                A = load(spec['accept'], '_c3_accept')
                H = A.load_handoff()
                if spec.get('world'):
                    patch_handoff(H, spec['world'])
                if spec['kind'] == 'accept_handoff_only':
                    E = types.SimpleNamespace(reingest=lambda *a, **kw: {'status': STUB_STATUS})
                rc = A.execute(A.parse(spec['argv']), E, W, H)
    except BaseException as exc:                                # noqa: BLE001
        rc = 'CRASH %s: %s %s' % (type(exc).__name__, exc, traceback.format_exc()[-2000:])
    with open(spec['out'], 'x') as f:
        json.dump({'rc': rc, 'stdout': buf.getvalue(), 'audit_denied': AUDIT['denied'],
                   'session_leader': os.getsid(0) == os.getpid() == os.getpgrp()}, f, indent=1, default=str)
    return 0


def run_child(world, kind, entry, argv, tag, accept=None):
    rd = Path(STATE['run_dir'])
    spec = {'kind': kind, 'entry': entry, 'argv': argv, 'world': world, 'run_dir': str(rd), 'accept': str(accept or ACCEPT),
            'out': str(rd / 'children' / ('%s.out.json' % tag))}
    sp = put_x(rd / 'children' / ('%s.spec.json' % tag), spec)
    e = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
    with open(rd / 'children' / ('%s.stderr.txt' % tag), 'x') as se:
        p = subprocess.Popen([PY, '-I', '-B', str(Path(__file__).resolve()), '--child', sp['path']], stdout=subprocess.DEVNULL,
                             stderr=se, env=e, start_new_session=True)
        p.wait(timeout=1800)
    out = json.loads(Path(spec['out']).read_text())
    out['json'] = last_json(out['stdout'])
    return out


def run_monitor(spec_path, outdir, receipt):
    return [PY, '-I', '-B', str(NAMED['monitor'][0]), '--driver', WORLD_CTX['driver_path'], '--driver-sha256',
            WORLD_CTX['mock_sha'], '--spec', str(spec_path), '--outdir', str(outdir), '--receipt', str(receipt),
            '--wall-cap-s', '600', '--rss-cap-bytes', str(RAM), '--output-cap-bytes', str(80 * GiB), '--poll-s', '0.2',
            '--python', PY]


def mock_runs(rd, items):
    procs, out = [], {}
    for tag, raw in items:
        d = rd / tag
        d.mkdir()
        sp = put_x(d / 'spec.json', None, raw=raw)
        so = open(d / 'monitor.stdout.txt', 'x')
        procs.append((tag, d, sp, so, subprocess.Popen(run_monitor(d / 'spec.json', d / 'out', d / 'RECEIPT.json'), stdout=so,
                                                        stderr=subprocess.STDOUT, start_new_session=True)))
    for tag, d, sp, so, p in procs:
        p.wait(timeout=900)
        so.close()
        out[tag] = {'dir': str(d), 'spec': sp,
                    'result': {'path': str(d / 'out' / 'result.json'), 'sha256': sha(d / 'out' / 'result.json')},
                    'receipt': {'path': str(d / 'RECEIPT.json'), 'sha256': sha(d / 'RECEIPT.json')}}
    return out


def base_config(world, work_dir):
    cfg = json.loads(NAMED['config_v004a'][0].read_bytes())
    cfg['work_dir'] = str(work_dir)
    cfg['work_dir_volume'] = None
    cfg['work_dir_identity'] = {'resolved': str(work_dir), 'volume': None, 'volume_uuid': None, 'symlinks': []}
    cfg['driver'] = {'path': world['driver_path'], 'sha256': world['mock_sha']}
    cfg['taxonomy'] = world['taxonomy']
    cfg['anchor']['driver_sha256'] = world['mock_sha']
    return cfg


def proof(gate, point, custody_sha, producer, **kw):
    return dict({'schema': 'UNT_CALIBRATION_POINT_PROOF_CX2V001', 'gate': gate, 'status': 'TESTED', 'verdict': 'PASS',
                 'point_sha256': point, 'custody_sha256': custody_sha, 'producer': producer, 'synthetic': True}, **kw)


def register_point(cd, tag, spec, W, S, prods):
    """A genesis registry record (c2v002's, with the three canonical synthetic producers: EPS adapter, GQ, slot proof)."""
    ident = W.point_identity(spec)
    point = W.M.digest(ident)
    cus = S.derive_custody(spec=spec, driver_sha256=WORLD_CTX['mock_sha'])
    csha = W.M.digest(cus)
    d = cd / tag
    d.mkdir()
    eps_slot = put_x(d / 'EPS_CERTIFICATE.json', {'schema': 'H3_SYNTHETIC_EPS_CERTIFICATE', 'point_sha256': point})
    shells = [{'range_inverse_kpc': [4.0, 64.0], 'refinement_failures': 0, 'eps': 1e-9, 'eps_envelope': 1e-9},
              {'range_inverse_kpc': [64.0, S.EDGE], 'refinement_failures': 0, 'eps': 1e-9, 'eps_envelope': 1e-9}]
    rho = put_x(d / 'RHO_RECORD.json', {'schema': 'UNT_POINT_RHO_NUMERICAL_CX2V001', 'gate': 'RHO_G', 'identity': ident,
                                        'point_sha256': point, 'custody': cus, 'settings': 'registered',
                                        'coverage_complete': True, 'required_coverage_inverse_kpc': S.EDGE,
                                        'full_registered_search_executed': True,
                                        'shells': [{'range_inverse_kpc': [4.0, S.EDGE], 'rho': 1e-6}], 'synthetic': True})
    eps = put_x(d / 'EPS_PROOF.json', proof('EPS', point, csha, prods['eps_adapter'],
                                            envelope_rule='A52_5_SUP_OVER_DIRECTION_TIMES_CARDINAL_TORUS',
                                            shells=shells, driver_certificate=eps_slot))
    gq = put_x(d / 'GQ_PROOF.json', proof('GQ', point, csha, prods['gq_producer'], method='GEOMETRY_UNIFORM_COLUMN_BOUND',
                                          all_columns_included=True, all_production_kperp_nodes=True,
                                          nonnegative_masses_required=True, M_s=128, M_s_doubled=256, K_big_inverse_kpc=128.0,
                                          max_column_difference_over_analytic_Pi0=1e-15, max_zero_mode_relative_error=0.0))
    los = put_x(d / 'LO_RHO_SLOT_PROOF.json', proof('LO_RHO_SLOT', point, csha, prods['lo_slot_proof'], driver_certificate=rho))
    bundle = put_x(d / 'PRELAUNCH_BUNDLE.json', {
        'schema': 'UNT_CALIBRATION_POINT_CERTIFICATES_CX2V001', 'identity': ident, 'custody': cus,
        'domain': {'K_inverse_kpc': 4.0, 'K_big_inverse_kpc': 128.0}, 'prelaunch': {'EPS': eps, 'GQ': gq, 'LO_RHO_SLOT': los},
        'acceptance_rule': 'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED',
        'driver_certificate_bindings': {'eps_certificate': eps_slot, 'lo_certificate': rho}, 'synthetic': True})
    return point, {'identity': ident, 'bundle': bundle, 'eps_certificate': eps_slot, 'lo_certificate': rho}


def deps_doc(w, root_refs=None, approved=None):
    sm = w['syn_module']
    return {'schema': 'H3_CAMPAIGN_ACCEPTANCE_DEPS_C2V001', 'status': 'ROOT_FILLED', 'synthetic': True,
            'deps': {'enumerator': sm, 'evidence': sm, 'lo_core': sm, 'guard': {'path': str(NAMED['guard_b1'][0]),
                                                                               'sha256': NAMED['guard_b1'][1]},
                     'writer': sm, 'row_producer': sm, 'lo_adapter': dict(sm, entry='adapt_call_lo'),
                     'srb_adapter': dict(sm, entry='adapt_call_srb_rot')},
            'policy': {'approved_certificate_producers': approved if approved is not None else w['approved'],
                       'trusted_source_producers': ['67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e',
                                                    '7044e1310bb0b8cde08f7839b88b949409d15219fb24756f418224a0e7c0ddce'],
                       'row_policy_reviews': {}, 'packet_binding_reviews': {}, 'evidence_producer': sm,
                       'approved_review_sha256': [], 'approved_evidence_producer_sha256': [sm['sha256']],
                       'approved_uniform_producer_sha256': [w['prods']['gq_producer']['sha256']],
                       'root_ruling_refs': dict({'SYN_LO_PRODUCER': w['prods']['lo_slot_proof']}, **(root_refs or {}))}}


def deps_record(w, tag, root_refs=None, approved=None):
    return put_x(Path(w['dir']) / ('DEPS_%s.json' % tag), deps_doc(w, root_refs, approved))


# ------------------------------------------------------------------------------------------------ the CP-1 list successor (mock)
CP1 = {}


def cp1_modules():
    """The CP-1 list successor loaded once for the worlds, with the declared synthetic substitutions on its c3v004 commons."""
    if CP1:
        return CP1
    PR = load(CP1R, '_c3_cp1r')
    PA = load(CP1A, '_c3_cp1a')
    for C in (PR.C, PA.C):
        C.DRIVER_SHA = WORLD_CTX['mock_sha']
        C.PINS = dict(C.PINS)
        for k, v in WORLD_CTX['prods'].items():
            C.PINS[k] = (v['path'], v['sha256'])
        C.PINS['response_producer'] = (WORLD_CTX['response_producer']['path'], WORLD_CTX['response_producer']['sha256'])
        C.PINS['custody'] = (WORLD_CTX['syn_module']['path'], WORLD_CTX['syn_module']['sha256'])
    PR.C.background_qos = lambda: True
    S = load(WORLD_CTX['syn_module']['path'], '_c3_syn_cp1')
    MK = load(SYN_SRC / 'mock_cp1_c2v003.py', '_c3_mock_cp1')
    CP1.update(PR=PR, PA=PA, R=PR.R, A=PA.A, C=PR.C, mock=MK.make(PR.C, S, SOURCE_PINS), mockA=MK.make(PA.C, S, SOURCE_PINS))
    return CP1


class FakeProc:
    def __init__(self, rc):
        self.rc = rc

    def poll(self):
        return self.rc


def seed_anchor(out_root):
    """Declared stand-in for the anchor's records in CP-1's out-root (the c3v004 run did them for rows 1-31)."""
    R, C = CP1['R'], CP1['C']
    row = C.point_rows()[0]
    d = Path(out_root) / R.point_dir_name(row, 1)
    d.mkdir(parents=True)
    k16 = row['key'][:16]
    put_x(d / ('STAGE_CONTEXT_%s.json' % k16), {'source_pins': SOURCE_PINS, 'peak_rss_bytes_process_high_water': 1,
                                               'synthetic_anchor_stand_in': True})
    put_x(d / ('ANCHOR_EPS_CROSSCHECK_%s_tol0p001.json' % k16), {'verdict': 'AGREE', 'synthetic_anchor_stand_in': True})


def list_scheduler(rows, out_root, ref, spawn, run_id):
    PR = CP1['PR']
    return PR.ListScheduler(rows, str(out_root), list_ref=ref, operator_lane='SYN_OPERATOR', max_concurrent=4, margin_pct=5.0,
                            poll_seconds=0.0, spawn=spawn, memory=lambda: 90, swap=lambda: 0.0, sleep=lambda s: None,
                            vmstat=lambda: {'page_size_bytes': 16384, 'free_pages': 1, 'speculative_pages': 0,
                                            'available_bytes': 1 << 40, 'purgeable_counted': False},
                            run_id=run_id, rho_gate_args=WORLD_CTX['rho_gate'])


def cp1_certify(w, list_pin, tag):
    """CP-1 list successor on the list (mock producers), EPS review + adapt-eps, slot proof, bundles, records, offline verify."""
    m = cp1_modules()
    PR, PA, R, A, C = m['PR'], m['PA'], m['R'], m['A'], m['C']
    wd = Path(w['dir'])
    out_root = wd / 'CP1_OUT'                                   # one out-root per world: list runs continue on it
    if not out_root.exists():
        seed_anchor(out_root)
    doc, rows = PR.P.load_points_list(C, list_pin)
    ref = dict(list_pin)
    rcs = {}

    def spawn(row):
        rc, _ = PR.run_list_point(row, str(out_root), list_ref=ref, operator_lane='SYN_OPERATOR', attempt=1, run_id=tag,
                                  loader=m['mock'].loader, hold_sleep=lambda s: None, rho_gate_args=WORLD_CTX['rho_gate'])
        rcs[row['key']] = rc
        return FakeProc(rc)
    s = list_scheduler(rows, out_root, ref, spawn, tag)
    src = s.run()
    rv, sp = wd / ('EPS_REVIEWS_%s' % tag), wd / ('SLOT_PROOFS_%s' % tag)
    rv.mkdir()
    sp.mkdir()
    reg_out = wd / ('REGISTRY_OUT_%s' % tag)
    reg_out.mkdir()
    bundles, adapt = [], []
    for row in rows:
        k16 = row['key'][:16]
        pdir = Path(out_root) / R.point_dir_name(row, 1)
        st_eps = json.loads((pdir / ('STAGE_EPS_%s.json' % k16)).read_bytes())
        st_ctx = json.loads((pdir / ('STAGE_CONTEXT_%s.json' % k16)).read_bytes())
        done = json.loads((pdir / ('POINT_DONE_%s.json' % k16)).read_bytes())
        review = put_x(rv / ('EPS_REVIEW_%s.json' % k16), {
            'schema': R.REVIEW_SCHEMA_EPS, 'verdict': 'APPROVED', 'numeric_ref': st_eps['record'], 'point_sha256': row['key'],
            'custody_sha256': st_ctx['custody_sha256'], 'adapter_sha256': C.PINS['eps_adapter'][1],
            'accepts_registered_numerical_estimate_not_rigorous_sup': True, 'reviewer_lane': 'SYN_REVIEWER',
            'distinct_from_producer_lane': True, 'synthetic': True})
        rc, res = R.adapt_point(row, str(out_root), review_path=review['path'], approved_review_sha256=review['sha256'],
                                approved_signer_lanes=['SYN_REVIEWER'], attempt=1,
                                adapter_loader=lambda: m['mock'].adapter, require_env=False)
        adapt.append(rc)
        spec = json.loads(Path(row['spec_path']).read_bytes())
        lo = put_x(sp / ('LO_RHO_SLOT_PROOF_%s.json' % k16), m['mockA'].slot_proof(spec, done['rho']['rho_numeric']))
        bundles.append(A.assemble_bundle(row, eps_proof=res['eps_proof'], gq_proof=done['gq_proof'], lo_proof=lo,
                                         approved=w['approved'], out_root=str(reg_out))['path'])
    rec = PA.assemble_records(ref, doc, rows, bundles, approved=w['approved'], out_root=str(reg_out), genesis_ref=w['registry'])
    ver = PA.verify_list(rec, rows, c1_ref=w['c1'], genesis_ref=w['registry'], custody_loader=A.real_custody_fn,
                         guard=A.real_guard())
    return {'records': rec, 'verify': ver, 'scheduler_rc': src, 'point_rc': rcs, 'adapt_rc': adapt, 'rows': rows,
            'out_root': str(out_root), 'bundles': bundles, 'ref': ref}


# ------------------------------------------------------------------------------------------------ the synthetic world
def h11_specs(ctx, rean_spec, registry_points, W):
    """HEADLINE11 #0-#10 spec bytes under the candidate config (#0 the registered anchor with its registered slots)."""
    rec = registry_points[W.M.digest(W.point_identity(rean_spec))]
    s0 = copy.deepcopy(rean_spec)
    for f in ('eps_certificate', 'lo_certificate'):
        s0['numerics']['uv_tail'][f] = copy.deepcopy(rec[f])
    s0['label'] = 'H3 SYNTHETIC HEADLINE11 #0 TAIL_REANCHOR'
    s1 = copy.deepcopy(ctx.mapper.build(ctx.seed_theta)['spec'])
    s1['label'] = 'H3 SYNTHETIC HEADLINE11 #1 WORKERS_8_CANDIDATE_ANCHOR'
    H = load(H11, '_c3_h11_names')
    labels = H.probe_labels(ctx)
    by_label = {lab: ctx.mapper.build(th)['raw'] for lab, th in ctx.probe_points()}
    out = [('TAIL_REANCHOR', jbytes(s0)), ('WORKERS_8_CANDIDATE_ANCHOR', jbytes(s1))]
    out += [(n, by_label[labels[n]]) for n in H.NAMES[2:]]
    return out


def accept_direct(w, H, run, records_dir, root_refs=None):
    """The adopted handoff (v004) on one direct call, in process (as for every direct call)."""
    W = w['W']
    spec = json.loads(Path(run['spec']['path']).read_bytes())
    reg = json.loads(Path(w['registry']['path']).read_bytes())
    rec = reg['points'][W.M.digest(W.point_identity(spec))]
    d = deps_doc(w, root_refs)
    policy = dict({k: d['policy'][k] for k in ('approved_certificate_producers', 'trusted_source_producers', 'row_policy_reviews',
                                               'packet_binding_reviews', 'evidence_producer', 'approved_review_sha256',
                                               'approved_evidence_producer_sha256', 'approved_uniform_producer_sha256',
                                               'root_ruling_refs')}, receipt=run['receipt'], prelaunch_bundle=rec['bundle'])
    hrec, ref = H.accept_call(call_dir=run['dir'], spec=spec, deps=H.load_deps(d['deps']), policy=policy,
                              records_dir=str(records_dir), mode='guard')
    return hrec, ref


def build_world(name, extra_thetas=()):
    rd = Path(STATE['run_dir'])
    wd = rd / name
    wd.mkdir()
    w = dict(WORLD_CTX, name=name, dir=str(wd))
    S = load(w['syn_module']['path'], '_c3_syn_%s' % name)
    files_p, _ = build_layout(wd / 'CX2P')
    w['entry_placeholder'] = files_p['h3_campaign_entry_cx2%s.py' % SUB]
    W0 = patch_chain(load_entry(w['entry_placeholder']).load_wrapper(), w)
    (wd / 'CONFIGS').mkdir()
    t0 = base_config(w, wd / 'WORK')
    w['T0'] = put_x(wd / 'CONFIGS' / 'T0_BASE.json', t0)
    ctx0 = W0.Context(copy.deepcopy(t0))
    w['row_ids'] = list(ctx0.row_ids)
    side = Path(w['syn_base']) / 'tail_scheme_impl_c2' / 'driver_r5' / 'H3_MOCK_SIDECAR.json'
    if not side.exists():
        put_x(side, {'row_ids': w['row_ids'], 'synthetic': True})
    runs = wd / 'MOCKCALLS'
    runs.mkdir()
    c4t = copy.deepcopy(ctx0.base)
    c4t['admit'] = {}
    c4t['label'] = 'H3 SYNTHETIC C4T (mock driver)'
    m = mock_runs(runs, [('C4T', jbytes(c4t))])['C4T']
    w['C4T'] = m
    res = json.loads(Path(m['result']['path']).read_bytes())
    sd = wd / 'SEALED'
    sd.mkdir()
    cb = put_x(sd / 'CASE_BLOCK.json', {'cases': {'C4T': {'tail': True, 'drivers_allowed': [w['mock_sha']], 'grid': 'SYN_GRID',
                                                          'normalized_spec_equal': {'/numerics': res['normalized_spec']['numerics']}}}})
    pre = put_x(sd / 'PREREG_SYNTHETIC.json', {'schema': 'H3_SYNTHETIC_PREREG', 'binding_inputs': {'case_block': cb}})
    add = put_x(sd / 'V005_ADDENDUM_SYNTHETIC.md', None, raw=b'synthetic addendum\n')
    src = ("V007_PREREG_SHA256 = '%s'\nPIN_ADDENDUM_V005 = '%s'\nCTRL = '%s'\nADDENDUM_V005_CITED = CTRL + '/V005_ADDENDUM_SYNTHETIC.md'\n"
           "PRODUCTION_K_BIG_A55 = 128.0\nSCHEMA_REPORT = '%s'\n" % (pre['sha256'], add['sha256'], str(sd), SCHEMA_REPORT))
    cmp_ = put_x(sd / 'kmax_tail_compare_SYNTHETIC_SEALED.py', None, raw=src.encode())
    rep_doc = {'schema': SCHEMA_REPORT, 'script_sha256': cmp_['sha256'], 'prereg': pre,
               'pins_verified': {'V005_addendum': add['sha256']}, 'test_mode': False, 'case_block': cb,
               'decision': {'outcome': 'ADOPT_TAIL', 'tests_read': True, 'carried_numerical_uncertainty_km_s': {'r0': 0.1}},
               'validity': {'C4T': {'valid_all': True}}, 'inputs': {'C4T': {'result_sha256': m['result']['sha256']}}}
    rep = put_x(sd / 'V007_REPORT_SYNTHETIC.json', rep_doc)
    w['tuple'] = (cmp_['sha256'], pre['sha256'], add['sha256'], SCHEMA_REPORT, rep['sha256'])
    seal = {'schema': 'H3_V007_SEAL_TUPLE_RECORD_C2V001', 'status': 'ROOT_FILLED', 'sub': SUB, 'publish_root': str(wd / 'CX2'),
            'tuple': dict(zip(('compare_sha256', 'prereg_sha256', 'addendum_sha256', 'report_schema', 'verdict_sha256'), w['tuple'])),
            'report': rep, 'compare': cmp_, 'filled_by': 'c2v003 test (synthetic)', 'ruling': 'SYNTHETIC'}
    w['seal_record'] = put_x(sd / 'SEAL_TUPLE_RECORD_SYNTHETIC.json', seal)
    Rg = load(REGEN, '_c3_regen_%s' % name)
    G = Rg.load_generator()
    G.SEALED_COMPARE, G.SEALED_PREREG = cmp_['path'], pre['path']
    (wd / 'CX2').mkdir()
    (wd / 'CX2' / 'v006r8').mkdir()
    shutil.copyfile(NAMED['sensitivity'][0], wd / 'CX2' / 'v006r8' / NAMED['sensitivity'][0].name)
    w['regen'] = Rg.run(w['seal_record']['path'], w['seal_record']['sha256'], str(wd / 'CX2'), G=G)
    w['entry'] = str(wd / 'CX2' / SUB / ('h3_campaign_entry_cx2%s.py' % SUB))
    E = load_entry(w['entry'])
    W = patch_chain(E.load_wrapper(), w)
    w['E'], w['W'] = E, W
    # genesis registry: the 9 probe points, the seed, the registered anchor (HEADLINE11 #0) and any extra theta
    cd = wd / 'CERTS'
    cd.mkdir()
    reg_anchor = W.M.registered_anchor(t0['anchor'])
    rean = copy.deepcopy(ctx0.base)
    rean['physical'] = copy.deepcopy(reg_anchor['physical'])
    rean['coefficients'] = copy.deepcopy(reg_anchor['coefficients'])
    rean['admit'] = {}
    todo = [(lab, ctx0.mapper.build(th)['spec']) for lab, th in ctx0.probe_points()] + \
           [('seed', ctx0.mapper.build(ctx0.seed_theta)['spec']), ('reanchor', rean)] + \
           [('extra_%02d' % i, ctx0.mapper.build(th)['spec']) for i, th in enumerate(extra_thetas)]
    points, labels = {}, []
    for i, (lab, sp_) in enumerate(todo):
        dg = W0.M.digest(W0.point_identity(sp_))
        if dg in points:
            labels.append([lab, dg])
            continue
        dg, rec = register_point(cd, 'P%02d' % i, sp_, W0, S, w['prods'])
        points[dg] = rec
        labels.append([lab, dg])
    w['registry'] = put_x(cd / 'REGISTRY.json', {'schema': 'H3_SYNTHETIC_CERTIFICATE_REGISTRY', 'points': points, 'labels': labels})
    w['n_points'] = len(points)
    w['ledger'] = {'schema': LEDGER_SCHEMA, 'path': str(wd / 'WORK' / 'CERTIFICATE_LEDGER.jsonl')}
    review = put_x(cd / 'POLICY_REVIEW.json', {
        'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True, 'driver_sha256': w['mock_sha'],
        'custody_deriver': w['syn_module'], 'state_enumerator': w['syn_module'], 'approved_certificate_producers': w['approved'],
        'guard_sha256': NAMED['guard_b1'][1], 'driver_slot_rule': 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE',
        'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001', 'certificate_ledger': w['ledger'], 'synthetic': True})
    w['review'] = review
    h3 = {'numerics.block_source': m['spec'], 'numerics.adopted_result': m['result'], 'numerics.source_results': [],
          'tail_readiness.certificate_registry': w['registry'], 'tail_readiness.certificate_policy_review': review,
          'tail_readiness.approved_certificate_producers': w['approved'], 'tail_readiness.state_enumerator': w['syn_module'],
          'tail_readiness.custody_deriver': w['syn_module'], 'tail_readiness.certificate_ledger': w['ledger'],
          'u_i_carrier.declared_by': 'c2v003 test (synthetic)', 'u_i_carrier.basis': 'synthetic world'}
    Ap = load(APPLY, '_c3_apply_%s' % name)

    def stage(label, sets, pred):
        delta = put_x(wd / 'CONFIGS' / ('DELTA_%s.json' % label), {'set': sets, 'append': {'notes': ' | C2V003 TEST %s.' % label}})
        out, rp = Ap.apply(Path(pred['path']).read_bytes(), json.loads(Path(delta['path']).read_bytes()),
                           Path(w['seal_record']['path']).read_bytes(), w['seal_record']['sha256'])
        if out is None:
            raise RuntimeError('apply %s refused: %s' % (label, rp))
        return put_x(wd / 'CONFIGS' / ('%s.json' % label), None, raw=out), rp
    w['T1'], w['T1_report'] = stage('T1_CANDIDATE_NO_EVIDENCE', h3, w['T0'])
    w['c1'] = put_x(cd / 'C1_SYNTHETIC.json', {'tail_readiness': json.loads(Path(w['T1']['path']).read_bytes())['tail_readiness'],
                                               'synthetic': True})
    ctx1 = W.Context(w['T1']['path'])
    # HEADLINE11 #0-#10: 11 mock calls under the real monitor, each accepted by the adopted handoff (direct calls)
    specs = h11_specs(ctx1, rean, points, W)
    mr = mock_runs(runs, [('H11_%02d' % i, raw) for i, (_, raw) in enumerate(specs)])
    H = patch_handoff(load(NAMED['handoff_v004'][0], '_c3_handoff_%s' % name), w)
    w['H'] = H
    acc_root = wd / 'H11_ACCEPTANCE'
    acc_root.mkdir()
    rows = []
    for i, (nm, _) in enumerate(specs):
        run = mr['H11_%02d' % i]
        hrec, ref = accept_direct(w, H, run, acc_root / ('H11_%02d' % i))
        rows.append({'index': i, 'name': nm, 'call_dir': run['dir'], 'spec': run['spec'], 'receipt': run['receipt'],
                     'result': run['result'], 'acceptance_record': ref, '_reading': hrec.get('reading')})
    w['h11_readings'] = [r.pop('_reading') for r in rows]
    w['h11_rows'] = rows
    w['h11_runs'] = put_x(cd / 'HEADLINE11_RUNS.json', {'schema': 'H3_HEADLINE11_RUNS_C2V001', 'runs': rows})
    HA = load(H11, '_c3_h11_%s' % name)
    w['HA'] = HA
    w['h11_reuse'] = HA.reuse_test(E, W, w['T1']['path'], w['h11_runs'])
    w['h11_asm'] = HA.assemble(E, W, w['T1']['path'], w['T1']['sha256'], w['h11_runs'], str(wd / 'H11_EVIDENCE'),
                               me={'path': str(H11), 'sha256': sha(H11)})
    dl = json.loads(Path(w['h11_asm']['delta']['path']).read_bytes())
    w['T2'], _ = stage('T2_CANDIDATE', dl['set'], w['T1'])
    wall = put_x(cd / 'WALL_RULE_SYNTHETIC.json', {'schema': 'UNT_W1_WALL_RULE_SYNTHETIC', 'status': 'FINAL_FOR_THESE_RECEIPTS'})
    B = load(NAMED['builder_c2v001'][0], '_c3_builder_%s' % name)
    bo = B.build(W, config_path=w['T2']['path'], config_sha256=w['T2']['sha256'], wall_rule=wall,
                 receipts=[('C4T', m['receipt']['path'], m['receipt']['sha256'])], out_dir=str(wd / 'ADOPTION'))
    dlt = json.loads(Path(bo['delta']['path']).read_bytes())
    w['T3'], w['T3_report'] = stage('T3_H3', dlt['set'], w['T2'])
    w['child_world'] = {k: w[k] for k in ('mock_sha', 'syn_base', 'syn_module')}
    return w


# ------------------------------------------------------------------------------------------------ CLI wrappers
def entry_cmd(w, argv, tag, entry=None):
    return run_child(w['child_world'], 'entry', entry or w['entry'], argv, '%s_%s' % (w['name'], tag))


def accept_cmd(w, deps, tag, wave, call_index, kind='accept', first_pass=None):
    recs = str(Path(w['dir']) / ('RECORDS_%s' % tag))
    argv = ['--entry', w['entry'], '--entry-sha256', sha(w['entry']), '--config', w['T3']['path'], '--wave', str(wave),
            '--call-index', str(call_index), '--deps', deps['path'], '--deps-sha256', deps['sha256'], '--records-dir', recs]
    if first_pass is not None:                                  # c2v004 B1: the first pass's acceptance record
        argv += ['--first-pass-record', first_pass['path'], '--first-pass-record-sha256', first_pass['sha256']]
    out = run_child(w['child_world'], kind, w['entry'], argv, '%s_%s' % (w['name'], tag))
    out['records_dir'] = recs
    return out


def reingest_invalid_cmd(w, wave, call_index, record, tag):
    r = dict(zip(('path', 'sha256'), record)) if isinstance(record, tuple) else record
    return entry_cmd(w, ['reingest-invalid', '--config', w['T3']['path'], '--wave', str(wave), '--call-index', str(call_index),
                         '--acceptance-record', r['path'], '--acceptance-record-sha256', r['sha256']], tag)


def status(w, tag):
    return (entry_cmd(w, ['status', '--config', w['T3']['path']], tag)['json'] or {})


def work_dir(w):
    return Path(json.loads(Path(w['T3']['path']).read_bytes())['work_dir'])


def cached(w):
    """{key: (classification, source, failure_class)} from the cache entries (read-only)."""
    W = w['W']
    ctx = W.Context(w['T3']['path'])
    o = W.Orchestrator(ctx)
    o.cache.open(create=False)
    return {k: (e['classification'], e['source'], e.get('failure_class')) for k, e in o.cache.entries.items()}


def run_wave(w, label, wave, n_expected=None):
    r = entry_cmd(w, ['run', '--config', w['T3']['path']] + (['--new-campaign'] if wave == 1 else []) + ['--max-waves', '1'],
                  'run_w%d' % wave)
    js = r['json'] or {}
    pp = work_dir(w) / 'waves' / ('wave_%04d' % wave) / 'WAVE_PLAN.json'
    n = json.loads(pp.read_text())['n_calls'] if pp.is_file() else None
    ok = (r['rc'] == 4 and r['session_leader'] and js.get('status') == 'HALTED_INFRA' and n is not None and
          len(js.get('halt') or []) == n and (n_expected is None or n == n_expected) and
          all(str(h.get('reason')).startswith('CERTIFICATE_ACCEPTANCE_REFUSED') for h in js.get('halt') or []))
    check('%s.run_wave_%d_in_its_own_session_finishes_%s_mock_calls_and_halts_INFRA_awaiting_acceptance' % (label, wave, n),
          'MUST_PASS', ok, {'rc': r['rc'], 'status': js.get('status'), 'n_calls': n, 'n_halt': len(js.get('halt') or [])})
    return n


def accept_all(w, label, wave, n, good_deps, skip=()):
    rcs = {}
    for i in range(n):
        if i in skip:
            continue
        a = accept_cmd(w, good_deps, 'acc_w%d_c%d' % (wave, i), wave, i)
        aj = a['json'] or {}
        rcs[i] = (a['rc'], aj.get('reading'), (aj.get('reingest') or {}).get('classification'), aj.get('f6_action'))
    ok = all(v[0] == 0 and v[1] == 'ACCEPTED' and v[2] == 'VALID' and v[3] == 'CACHED_VALID' for v in rcs.values())
    check('%s.acceptance_step_c2v004_reads_ACCEPTED_and_caches_VALID_every_call_of_wave_%d_%s' % (label, wave, sorted(rcs)),
          'MUST_PASS', ok, rcs)
    return rcs


# ------------------------------------------------------------------------------------------------ G / R / K / A
def t_generator():
    G = gen()
    files, outputs, lit = G.build('v006r10_c4')
    en = 'h3_campaign_entry_cx2v006r10_c4.py'
    ent = dict(files)[en].decode().splitlines()
    tpl = ENTRY_T.read_text().splitlines()
    ediff = [i + 1 for i, (a, b) in enumerate(zip(tpl, ent)) if a != b]
    check('G01.regression_SUB_v006r10_c4_no_tuple:_published_policy_and_core,_the_wrapper_source_itself,_the_entry_template_but_its_'
          'WRAPPER_path_line', 'MUST_PASS',
          outputs['adoption_policy_cx2v006r10_c4.py'] == NAMED['policy_r10_c4'][1] and
          outputs['calibration_core_cx2v006r10_c4.py'] == NAMED['core_r10_c4'][1] and
          outputs['calibration_orchestrator_cx2v006r10_c4_q5b1.py'] == sha(WRAP_SRC) and len(ent) == len(tpl) and
          len(ediff) == 1 and ent[ediff[0] - 1] == "WRAPPER = Path('%s')" % (CX2 / 'v006r10_c4' / 'calibration_orchestrator_cx2v006r10_c4_q5b1.py'),
          {'entry_diff_lines': ediff, 'wrapper': outputs['calibration_orchestrator_cx2v006r10_c4_q5b1.py'][:8]})
    f12, o12, _ = G.build(SUB)
    ship = H3 / 'placeholder_chain_c2v004' / SUB
    same = {n: (ship / n).is_file() and sha(ship / n) == s for n, s in o12.items()}
    check('G02.the_shipped_placeholder_chain_c2v004_is_the_generator_output_for_%s' % SUB, 'MUST_PASS', all(same.values()),
          {k[:44]: v[:8] for k, v in o12.items()})
    G2 = load(NAMED['generator_c2v003'][0], '_c3_gen_c2v003')
    rows = {}
    for sb in ('v006r10_c4', SUB):
        _, o2, l2 = G2.build(sb)
        _, o3, l3 = G.build(sb)
        pn, cn, wn, enn = G.names(sb)
        rows[sb] = {'policy_core_equal': o2[pn] == o3[pn] and o2[cn] == o3[cn], 'wrapper_differs': o2[wn] != o3[wn],
                    'entry_differs': o2[enn] != o3[enn], 'resolve_literal_equal': l2 == l3}
    check('G03.generator_c2v004_equals_c2v003_for_policy_and_core_(and_the__resolve_source_literal);_wrapper_and_entry_differ',
          'MUST_PASS', all(all(v.values()) for v in rows.values()), rows)
    wq = dict(f12)['calibration_orchestrator_cx2%s_q5b1.py' % SUB].decode().splitlines()
    srcl = WRAP_SRC.read_text().splitlines()
    wdiff = [i + 1 for i, (a, b) in enumerate(zip(srcl, wq)) if a != b]
    ent = dict(f12)['h3_campaign_entry_cx2%s.py' % SUB].decode().splitlines()
    ediff = [i + 1 for i, (a, b) in enumerate(zip(tpl, ent)) if a != b]
    check('G04.r12_c4_wrapper_differs_from_its_source_at_the_core_pin_line_only;_entry_from_its_template_in_the_two_WRAPPER_lines',
          'MUST_PASS', len(wdiff) == 1 and wq[wdiff[0] - 1].startswith("M=load(HERE/'calibration_core_cx2%s.py'" % SUB) and
          len(srcl) == len(wq) and len(ediff) == 2 and all(ent[i - 1].startswith('WRAPPER') for i in ediff),
          {'wrapper_lines': wdiff, 'entry_lines': ediff})
    q = NAMED['wrapper_q5b1'][0].read_text().splitlines()
    removed = [ln[1:] for ln in difflib.unified_diff(q, srcl, lineterm='', n=0) if ln.startswith('-') and not ln.startswith('---')]
    want_removed = ["        registry=M.pin_doc(r['certificate_registry'],'certificate registry')",
                    "        rec=registry.get('points',{}).get(M.digest(ident))",
                    "                 'post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'},'certificate policy review')",
                    "        registry=M.pin_doc(self.cfg['tail_readiness']['certificate_registry'],'registry')",
                    "        rec=registry['points'][M.digest(point_identity(spec))]",
                    "        self.ctx.check_cached_certificate(dict(theta=theta,classification=classification,provenance=provenance))",
                    "    def reingest(self,wave,call_index,bundle_ref):"]
    block = '\n'.join(q[144:191])
    check('G05.wrapper_source_vs_q5b1:_exactly_seven_q5b1_lines_replaced_(the_two_lookups,_the_review_binding,_the_put_check,_the_'
          'reingest_signature);_the_slot_block_L145_191_verbatim', 'MUST_PASS',
          sorted(removed) == sorted(want_removed) and block in '\n'.join(srcl), {'removed': len(removed)})
    w3 = NAMED['wrapper_c2v003'][0].read_text().splitlines()
    rw = [ln[1:] for ln in difflib.unified_diff(w3, srcl, lineterm='', n=0) if ln.startswith('-') and not ln.startswith('---')]
    e3 = NAMED['entry_c2v003'][0].read_text().splitlines()
    re_ = [ln[1:] for ln in difflib.unified_diff(e3, tpl, lineterm='', n=0) if ln.startswith('-') and not ln.startswith('---')]
    want_e = [e3[0]] + [ln for ln in e3 if ln.startswith(('WRAPPER = ', 'WRAPPER_SHA = ', 'ENTRY_NAME = '))] + \
             ['    return M.Orchestrator(ctx).reingest(int(wave), int(call_index), bundle_ref)']
    check('G06.c2v004_deltas:_the_wrapper_source_removes_exactly_one_c2v003_line_(the_reingest_signature);_the_entry_template_'
          'exactly_its_first_docstring_line,_WRAPPER,_WRAPPER_SHA,_ENTRY_NAME_and_the_reingest_call', 'MUST_PASS',
          rw == ["    def reingest(self,wave,call_index,bundle_ref):"] and sorted(re_) == sorted(want_e),
          {'wrapper_removed': len(rw), 'entry_removed': len(re_)})
    Rc = load(REGEN, '_c3_regen_cli')
    ph = NAMED['seal_placeholder'][0]
    rd = Path(STATE['run_dir'])
    rc, txt = quiet(Rc.main, ['build', '--seal-record', str(ph), '--seal-record-sha256', sha(ph), '--out-dir', str(rd / 'REAL_REGEN')])
    check('R01.regenerate_c2v004_build_on_the_shipped_placeholder_record_refuses_EMPTY_TUPLE', 'MUST_FAIL',
          rc == 2 and 'EMPTY_TUPLE' in txt and not (rd / 'REAL_REGEN').exists(), (last_json(txt) or {}).get('reason'))


def t_regen_world(w):
    doc = w['regen']
    nd = {k: sum(1 for x in v if x.startswith('+')) for k, v in doc['line_diff_vs_no_tuple_build'].items()}
    check('R02.with_a_synthetic_sealed_tuple_regenerate_c2v004_writes_the_re_pinned_chain_(diffs_policy_2_core_1_wrapper_1_entry_1)',
          'MUST_PASS', all(doc['chain_checks'].values()) and sorted(nd.values()) == [1, 1, 1, 2] and
          doc['schema'] == 'H3_REGENERATE_RECORD_C2V004', nd)


def t_real_dry():
    rd = Path(STATE['run_dir'])
    files, _ = build_layout(rd / 'REAL_LAYOUT')
    ent = files['h3_campaign_entry_cx2%s.py' % SUB]
    E = load_entry(ent)
    W = E.load_wrapper()
    E.check_patch(W)
    cfg = json.loads(NAMED['config_v004a'][0].read_bytes())
    wd = rd / 'REAL_UNCREATED_WORK_DIR'
    cfg['work_dir'], cfg['work_dir_volume'] = str(wd), None
    cfg['work_dir_identity'] = {'resolved': str(wd), 'volume': None, 'volume_uuid': None, 'symlinks': []}
    cp = put_x(rd / 'REAL_V004A_LOCAL.json', cfg)
    ctx = W.Context(cp['path'])
    po = W.Orchestrator(ctx).plan_only()
    nw = po.get('next_wave') or {}
    pend = sorted(k for k, g in ctx.gates.items() if not g.get('ok'))
    six = ['adoption_regeneration', 'certificate_policy', 'deciding_test', 'driver_capability', 'numerics_verdict', 'u_i_carrier']
    check('K01.real_v004a_through_the_placeholder_c2v004_chain_plans_W1_(seed_key_and_spec_unchanged)_with_the_six_gates_pending',
          'MUST_PASS', po['status'] == 'OK' and pend == six and nw.get('n_calls') == 1 and nw['calls'][0]['key'] == SEED_KEY16 and
          nw['calls'][0]['spec_sha256'].startswith(SEED_SPEC_V004A) and not wd.exists() and ctx.ledger_head()['configured'] is False,
          {'cache_id': ctx.cache_id[:16], 'pending': pend})
    outs = {}
    for tag, argv in (('reingest_invalid', ['reingest-invalid', '--config', cp['path'], '--wave', '1', '--call-index', '0',
                                            '--acceptance-record', '/nonexistent_record.json', '--acceptance-record-sha256', '0' * 64]),
                      ('ledger_append', ['ledger-append', '--config', cp['path'], '--records', '/nonexistent_records.json',
                                         '--records-sha256', '0' * 64]),
                      ('points_manifest', ['points-manifest', '--config', cp['path'], '--out-dir', str(rd / 'REAL_POINTS')])):
        rc, txt = quiet(E.dispatch, W, argv)
        outs[tag] = (rc, str((last_json(txt) or {}).get('reasons'))[:90])
    check('K02.entry_c2v004_new_commands_on_the_real_chain_refuse_while_nothing_is_set_(nothing_created)', 'MUST_FAIL',
          all(v[0] == 3 for v in outs.values()) and 'GATES_NOT_PASSED' in outs['reingest_invalid'][1] and not wd.exists()
          and not (rd / 'REAL_POINTS').exists(), outs)
    rc, txt = quiet(E.dispatch, W, ['ledger-status', '--config', cp['path']])
    js = last_json(txt) or {}
    check('K03.entry_ledger_status_on_v004a_reads_no_ledger_configured_(the_lookup_is_the_genesis_registry_alone)', 'MUST_PASS',
          rc == 0 and (js.get('head') or {}).get('configured') is False and js.get('entries') == [], js.get('head'))
    Ac = load(ACCEPT, '_c3_accept_cli')
    e2 = NAMED['entry_c2v003'][0]
    rc, txt = quiet(Ac.main, ['--entry', str(e2), '--entry-sha256', sha(e2), '--config', cp['path'], '--wave', '1', '--call-index',
                              '0', '--deps', cp['path'], '--deps-sha256', cp['sha256'], '--records-dir', str(rd / 'REAL_RECORDS')])
    check('K04.acceptance_step_c2v004_refuses_a_c2v003_line_entry_(ENTRY_NOT_C2V004_LINE,_nothing_written)', 'MUST_FAIL',
          rc == 3 and 'ENTRY_NOT_C2V004_LINE' in txt and not (rd / 'REAL_RECORDS').exists(), str((last_json(txt) or {}).get('reasons'))[:90])
    Hc = load(H11, '_c3_h11_cli')
    hd = rd / 'REAL_H11'
    hd.mkdir()
    runs = [{'index': i, 'name': n, 'spec': put_x(hd / ('SPEC_%02d.json' % i), {'synthetic_placeholder_spec_not_a_run': n})}
            for i, n in enumerate(Hc.NAMES)]
    man = put_x(hd / 'RUNS_SPECS_ONLY.json', {'schema': 'H3_HEADLINE11_RUNS_C2V001', 'runs': runs})
    base = ['--entry', ent, '--entry-sha256', sha(ent), '--config', cp['path'], '--config-sha256', cp['sha256'], '--runs',
            man['path'], '--runs-sha256', man['sha256']]
    rc, txt = quiet(Hc.main, ['reuse-test'] + base)
    js = last_json(txt) or {}
    rc2, txt2 = quiet(Hc.main, ['assemble'] + base + ['--out-dir', str(rd / 'REAL_H11_OUT')])
    check('K05.HEADLINE11_assembler_CLI_on_the_real_chain_(v004a):_reuse_test_lists_the_9_probe_spec_shas_and_reads_RUN_9_CALLS_for_'
          'other_bytes_(exit_5);_assemble_refuses_a_manifest_without_receipts_(nothing_written)', 'MUST_FAIL',
          rc == 5 and js.get('verdict') == 'RUN_9_CALLS_AT_THESE_SPEC_SHAS' and len(js.get('probe_spec_sha256') or []) == 9 and
          rc2 == 3 and 'PINS_REQUIRED' in txt2 and not (rd / 'REAL_H11_OUT').exists(),
          {'reuse_rc': rc, 'verdict': js.get('verdict'), 'assemble_rc': rc2})


def t_apply(w):
    A3 = load(APPLY, '_c3_apply_rows')
    t0 = json.loads(Path(w['T0']['path']).read_bytes())
    t1 = json.loads(Path(w['T1']['path']).read_bytes())
    d = leaf_diff(t0, t1)
    check('A01.T1_leaf_diff_is_H3_gate_fields,_tail_readiness.certificate_ledger_and_notes_only;_the_ledger_field_is_in_the_cache_key',
          'MUST_PASS', d and all(any(k == a or k.startswith(a + '.') for a in A3.ALLOWED) for k in d) and
          t1['tail_readiness']['certificate_ledger'] == w['ledger'] and 'certificate_ledger' not in t0['tail_readiness'] and
          'tail_readiness.certificate_ledger.path' in w['T1_report']['changed_paths_in_wrapper_cache_key'] and
          t1['numerics']['block'] == t0['numerics']['block'], {'n_leaves': len(d)})
    t0b = Path(w['T0']['path']).read_bytes()
    bad = {}
    for tag, v in (('other_path', dict(w['ledger'], path=w['ledger']['path'] + '.x')), ('schema', dict(w['ledger'], schema='X')),
                   ('relative', dict(w['ledger'], path='CERTIFICATE_LEDGER.jsonl')), ('head_sha', dict(w['ledger'], sha256='0' * 64))):
        out, rp = A3.apply(t0b, {'set': {'tail_readiness.certificate_ledger': v}})
        bad[tag] = out is None
    check('A02.a_ledger_policy_other_than_{schema,_<work_dir>/CERTIFICATE_LEDGER.jsonl}_refuses_(other_path,_schema,_relative,_a_head_sha)',
          'MUST_FAIL', all(bad.values()), bad)
    A1 = load(NAMED['apply_c2v001'][0], '_c3_apply_c2v001')
    out, rp = A1.apply(t0b, {'set': {'tail_readiness.certificate_ledger': w['ledger']}})
    check('A03.contrast_apply_c2v001_cannot_set_tail_readiness.certificate_ledger', 'MUST_FAIL', out is None, rp.get('reasons', [])[:1])


# ------------------------------------------------------------------------------------------------ P: CP-1 list successor
def t_cp1_table_mode():
    PR = load(CP1R, '_c3_cp1r_table')
    R4 = load(NAMED['cp1_runner'][0], '_c3_cp1_c3v004_direct')
    a, ta = quiet(PR.main, ['plan'])
    b, tb = quiet(R4.main, ['plan'])
    ja, jb = last_json(ta) or {}, last_json(tb) or {}
    for j in (ja, jb):
        j.pop('utc', None)
    check('P01.table_mode_the_list_successor_CLI_is_the_c3v004_runner_(plan_of_rows_1_31_identical_incl._runner_pin)', 'MUST_PASS',
          a == b == 0 and ja == jb and len(ja.get('points') or []) == 31 and
          all(p['status'] == 'SPEC_AND_KEY_VERIFIED' for p in ja['points']) and ja['runner']['sha256'] == NAMED['cp1_runner'][1],
          {'rows': len(ja.get('points') or []), 'runner': (ja.get('runner') or {}).get('sha256', '')[:8]})
    PA = load(CP1A, '_c3_cp1a_table')
    check('P02.the_list_successor_loads_the_c3v004_runner,_common_and_assembler_from_their_pinned_bytes_(unchanged)', 'MUST_PASS',
          sha(PR.R.__file__) == NAMED['cp1_runner'][1] and sha(PR.C.__file__) == NAMED['cp1_common'][1] and
          sha(PA.A.__file__) == NAMED['cp1_assembler'][1] and PR.C.point_rows() == R4.C.point_rows(),
          [Path(x.__file__).name for x in (PR.R, PR.C, PA.A)])


def t_cp1_list_rules(w, list_pin):
    m = cp1_modules()
    PR, C = m['PR'], m['C']
    doc = json.loads(Path(list_pin['path']).read_bytes())
    rc, txt = quiet(PR.main, ['plan', '--points-list', list_pin['path'], '--points-list-sha256', list_pin['sha256']])
    js = last_json(txt) or {}
    check('P03.list_mode_plan_verifies_every_list_spec_pin_and_its_point_key_(core_recipe)', 'MUST_PASS',
          rc == 0 and len(js.get('points') or []) == doc['n_points'] and
          all(p['status'] == 'SPEC_AND_KEY_VERIFIED' for p in js['points']), [p['status'][:24] for p in js.get('points') or []])
    d = Path(w['dir']) / 'LIST_VARIANTS'
    d.mkdir()
    table = C.point_rows()
    bad = {}

    def variant(tag, mutate):
        v = copy.deepcopy(doc)
        mutate(v)
        p = put_x(d / ('LIST_%s.json' % tag), v)
        try:
            PR.P.load_points_list(C, p)
            return None
        except C.Refusal as exc:
            return str(exc)[:70]
    try:
        PR.P.load_points_list(C, dict(list_pin, sha256='0' * 64))
        bad['sha'] = None
    except C.Refusal as exc:
        bad['sha'] = str(exc)[:70]
    bad['key_not_spec'] = variant('KEY', lambda v: v['points'][0].update(key=v['points'][-1]['key'] if len(v['points']) > 1
                                                                          else '1' * 64))
    bad['table_key'] = variant('TABLE', lambda v: v['points'][0].update(key=table[27]['key']))
    bad['row_le_31'] = variant('ROW', lambda v: v['points'][0].update(row=31))
    bad['table_label'] = variant('LABEL', lambda v: v['points'][0].update(label='CAMPAIGN_W1_SEED'))
    check('P04.list_rules_refuse_a_sha_mismatch,_a_key_that_is_not_the_spec\'s,_a_31_table_key,_a_row_<=_31,_a_table_label',
          'MUST_FAIL', all(bad.values()), bad)
    _, rows = PR.P.load_points_list(C, list_pin)
    ref = dict(list_pin)
    empty = Path(w['dir']) / 'CP1_OUT_NO_ANCHOR'
    empty.mkdir()
    spawned = []
    s = list_scheduler(rows, empty, ref, lambda row: spawned.append(row) or FakeProc(0), 'noanchor')
    rc = s.run()
    check('P05.list_points_never_start_without_the_anchor_AGREE_in_the_out_root_(c3v004_gate_unchanged)', 'MUST_FAIL',
          rc == 3 and not spawned and 'ANCHOR_CROSSCHECK_AGREE_REQUIRED' in str(s.stopped), str(s.stopped)[:90])
    cmd = PR.worker_cmd(s, rows[0])
    check('P06.the_list_scheduler_spawns_THIS_successor\'s_worker_with_the_same_list_pin_(taskpolicy_-b,_python_-I_-B)', 'MUST_PASS',
          cmd[:6] == [C.TASKPOLICY, '-b', sys.executable, '-I', '-B', os.path.realpath(str(CP1R))] and cmd[6] == 'worker' and
          cmd[cmd.index('--points-list') + 1] == ref['path'] and cmd[cmd.index('--points-list-sha256') + 1] == ref['sha256'],
          cmd[5:9])


# ------------------------------------------------------------------------------------------------ H: HEADLINE11 assembler
def t_h11(w):
    HA, E, W = w['HA'], w['E'], w['W']
    ru = w['h11_reuse']
    check('H01.reuse_test_(A192_item_4):_status_under_the_candidate_lists_the_9_probe_spec_shas_and_they_equal_HEADLINE11_#2_#10',
          'MUST_PASS', ru['verdict'] == 'REUSE_HEADLINE11' and len(ru['rows']) == 9 and all(r['equal'] for r in ru['rows']) and
          not ru['name_label_mismatches'] and len(ru['probe_spec_sha256']) == 9,
          {'verdict': ru['verdict'], 'readings': w['h11_readings']})
    a = w['h11_asm']
    t2 = W.Context(w['T2']['path'])
    check('H02.assemble_writes_the_deciding_and_capability_documents;_the_chain\'s_gates_read_ok_in_memory_and_on_T2', 'MUST_PASS',
          a['status'] == 'OK' and all(g['ok'] for g in a['gate_check'].values()) and t2.gates['deciding_test']['ok'] and
          t2.gates['driver_capability']['ok'] and t2.gates['driver_capability']['layer1_normalize_ok'],
          {k: g['ok'] for k, g in a['gate_check'].items()})
    d = Path(w['dir']) / 'H11_VARIANTS'
    d.mkdir()
    base = json.loads(Path(w['h11_runs']['path']).read_bytes())

    def variant(tag, mutate):
        v = copy.deepcopy(base)
        mutate(v)
        return put_x(d / ('RUNS_%s.json' % tag), v)

    def asm(tag, ref):
        try:
            return HA.assemble(E, W, w['T1']['path'], w['T1']['sha256'], ref, str(d / ('OUT_%s' % tag)))
        except HA.Refused as exc:
            return {'status': 'REFUSED', 'reasons': [str(exc)]}
    sp5 = json.loads(Path(base['runs'][5]['spec']['path']).read_bytes())
    sp5['label'] += ' (other bytes)'
    other = put_x(d / 'SPEC_05_OTHER_BYTES.json', sp5)
    v1 = variant('OTHER_SPEC', lambda v: v['runs'][5].update(spec=other))
    r1 = HA.reuse_test(E, W, w['T1']['path'], v1)
    a1 = asm('OTHER_SPEC', v1)
    check('H03.a_corner_run_at_other_spec_bytes:_reuse_test_reads_RUN_9_CALLS_and_assemble_refuses_(nothing_written)', 'MUST_FAIL',
          r1['verdict'] == 'RUN_9_CALLS_AT_THESE_SPEC_SHAS' and r1['differ'] == [base['runs'][5]['name']] and
          a1['status'] == 'REFUSED' and not (d / 'OUT_OTHER_SPEC').exists(), {'reuse': r1['verdict'], 'differ': r1['differ']})
    acc4 = json.loads(Path(base['runs'][4]['acceptance_record']['path']).read_bytes())
    inc = put_x(d / 'ACC_04_INCOMPLETE.json', dict(acc4, reading='INCOMPLETE', outputs_are_evidence=False))
    a2 = asm('INCOMPLETE', variant('INCOMPLETE', lambda v: v['runs'][4].update(acceptance_record=inc)))
    acc0 = json.loads(Path(base['runs'][0]['acceptance_record']['path']).read_bytes())
    stop = put_x(d / 'ACC_00_STEP4_STOP.json', dict(acc0, step4_stop_for_root_ruling=True))
    a3 = asm('STEP4', variant('STEP4', lambda v: v['runs'][0].update(acceptance_record=stop)))
    a4 = asm('SWAP', variant('SWAP', lambda v: (v['runs'][3].update(receipt=base['runs'][4]['receipt']),
                                                 v['runs'][4].update(receipt=base['runs'][3]['receipt']))))
    a5 = asm('OTHER_CALL', variant('OTHER_CALL', lambda v: v['runs'][6].update(acceptance_record=base['runs'][7]['acceptance_record'])))
    rs = {k: str(x.get('reasons'))[:110] for k, x in (('incomplete', a2), ('step4', a3), ('swap', a4), ('other_call', a5))}
    check('H04.assemble_refuses_a_run_not_ACCEPTED,_#0_with_the_step_4_stop,_swapped_receipts,_another_call\'s_record', 'MUST_FAIL',
          all(x['status'] == 'REFUSED' for x in (a2, a3, a4, a5)) and 'NOT_ACCEPTED' in rs['incomplete'] and
          'STEP4_STOP' in rs['step4'] and 'receipt' in rs['swap'] and 'another call' in str(a5.get('reasons')), rs)


# ------------------------------------------------------------------------------------------------ ledger forgery (in process)
def ledger_variant(w, tag, lines):
    """A config whose work dir is a separate folder holding `lines` as its ledger (the genesis digest binds the path), with a
    policy review that binds that ledger policy (a copy of the world's review, only certificate_ledger changed)."""
    wd = Path(w['dir']) / ('FORGED_%s' % tag)
    wd.mkdir()
    cfg = json.loads(Path(w['T3']['path']).read_bytes())
    cfg['work_dir'] = str(wd / 'WORK')
    cfg['work_dir_identity'] = {'resolved': str(wd / 'WORK'), 'volume': None, 'volume_uuid': None, 'symlinks': []}
    cfg['tail_readiness']['certificate_ledger'] = {'schema': LEDGER_SCHEMA, 'path': str(wd / 'WORK' / 'CERTIFICATE_LEDGER.jsonl')}
    rv = json.loads(Path(w['review']['path']).read_bytes())
    rv['certificate_ledger'] = cfg['tail_readiness']['certificate_ledger']
    cfg['tail_readiness']['certificate_policy_review'] = put_x(wd / 'POLICY_REVIEW_VARIANT.json', rv)
    (wd / 'WORK').mkdir()
    with open(wd / 'WORK' / 'CERTIFICATE_LEDGER.jsonl', 'xb') as f:
        f.write(b''.join(lines))
    return cfg


def rechain(W, cfg, entries):
    """Re-chain entries for the variant's genesis (as an honest appender would write them)."""
    r = cfg['tail_readiness']
    prev = W.M.digest({'schema': LEDGER_SCHEMA + '_GENESIS', 'certificate_registry': r['certificate_registry'],
                       'certificate_ledger': r['certificate_ledger']})
    out = []
    for i, e in enumerate(entries):
        e = {k: v for k, v in e.items() if k != 'entry_sha256'}
        e.update(seq=i + 1, prev_sha256=prev)
        e['entry_sha256'] = W.M.digest(e)
        prev = e['entry_sha256']
        out.append(W.M.canonical(e) + b'\n')
    return out


def t_forged_ledgers(w):
    W = w['W']
    raw = Path(w['ledger']['path']).read_bytes()
    entries = [json.loads(x) for x in raw.split(b'\n') if x]

    def gate(tag, lines):
        cfg = ledger_variant(w, tag, lines)
        try:
            c = W.Context(cfg)
            g = c.certificate_policy_gate()
            return g['ok'], str(g.get('reasons'))[:120]
        except W.Error as exc:
            return False, str(exc)[:120]
    ok, why = gate('FAITHFUL', rechain(W, ledger_cfg_for(w, 'FAITHFUL'), entries))
    check('F01.contrast_a_faithful_re_chained_copy_of_the_ledger_verifies_(the_certificate_policy_gate_stays_ok)', 'MUST_PASS', ok, why)
    # a forged entry: chain recomputed, but its bundle's EPS proof names an unapproved producer
    e0 = copy.deepcopy(entries[0])
    b = json.loads(Path(e0['record']['bundle']['path']).read_bytes())
    epsd = json.loads(Path(b['prelaunch']['EPS']['path']).read_bytes())
    fd = Path(w['dir']) / 'FORGERY_FILES'
    fd.mkdir()
    eps_bad = put_x(fd / 'EPS_PROOF_UNAPPROVED.json', dict(epsd, producer=w['unapproved']))
    b['prelaunch']['EPS'] = eps_bad
    b_bad = put_x(fd / 'BUNDLE_UNAPPROVED.json', b)
    e0['record'] = dict(e0['record'], bundle=b_bad)
    cfg_tag = 'FORGED_ENTRY'
    res = {}
    res['forged_entry'] = gate(cfg_tag, rechain(W, ledger_cfg_for(w, cfg_tag), [e0] + entries[1:]))
    lines = rechain(W, ledger_cfg_for(w, 'HASH'), entries)
    e1 = json.loads(lines[1])
    e1['wave'] = 99
    res['entry_hash'] = gate('HASH', [lines[0], W.M.canonical(e1) + b'\n'] + lines[2:])
    lines = rechain(W, ledger_cfg_for(w, 'CHAIN'), entries)
    e1 = json.loads(lines[1])
    e1['prev_sha256'] = '0' * 64
    e1 = {k: v for k, v in e1.items() if k != 'entry_sha256'}
    e1['entry_sha256'] = W.M.digest(e1)
    res['chain_break'] = gate('CHAIN', [lines[0], W.M.canonical(e1) + b'\n'] + lines[2:])
    gen_key = next(iter(json.loads(Path(w['registry']['path']).read_bytes())['points']))
    g = json.loads(Path(w['registry']['path']).read_bytes())['points'][gen_key]
    e_gen = dict(copy.deepcopy(entries[0]), key=gen_key, record=g)
    res['genesis_key'] = gate('GENESIS', rechain(W, ledger_cfg_for(w, 'GENESIS'), [e_gen]))
    e_key = dict(copy.deepcopy(entries[0]), key='1' * 64)
    res['key_not_identity'] = gate('KEY', rechain(W, ledger_cfg_for(w, 'KEY'), [e_key]))
    lines = rechain(W, ledger_cfg_for(w, 'TORN'), entries)
    res['torn'] = gate('TORN', lines[:-1] + [lines[-1][:-1]])
    res['copied_from_another_work_dir'] = gate('COPIED', [raw])
    words = {'forged_entry': 'ENTRY_INVALID', 'entry_hash': 'ENTRY_HASH', 'chain_break': 'CHAIN_BREAK',
             'genesis_key': 'ALREADY_REGISTERED', 'key_not_identity': 'KEY_IS_NOT_THE_IDENTITY', 'torn': 'TORN',
             'copied_from_another_work_dir': 'CHAIN_BREAK'}
    check('F02.forged_ledgers_close_the_certificate_policy_gate:_forged_entry_(unapproved_producer),_entry_hash,_chain_break,_genesis_'
          'key,_key_not_the_identity_digest,_torn_line,_a_ledger_copied_from_another_work_dir', 'MUST_FAIL',
          all(not ok and words[k] in why for k, (ok, why) in res.items()), {k: v[1][:60] for k, v in res.items()})


def ledger_cfg_for(w, tag):
    """The config ledger_variant(w, tag, ...) will write (for re-chaining before the folder exists)."""
    wd = Path(w['dir']) / ('FORGED_%s' % tag)
    cfg = json.loads(Path(w['T3']['path']).read_bytes())
    cfg['tail_readiness']['certificate_ledger'] = {'schema': LEDGER_SCHEMA, 'path': str(wd / 'WORK' / 'CERTIFICATE_LEDGER.jsonl')}
    return cfg


# ------------------------------------------------------------------------------------------------ E: end to end
def e2e_w1(w, label):
    W = w['W']
    ctx = W.Context(w['T3']['path'])
    gates = {k: bool(g.get('ok')) for k, g in ctx.gates.items()}
    check('%s01.all_six_gates_pass_(deciding_and_capability_from_the_HEADLINE11_assembler;_ledger_policy_bound_by_the_review)' % label,
          'MUST_PASS', all(gates.values()) and len(gates) == 6 and ctx.ledger_head()['n_entries'] == 0, gates)
    w['cache_id0'], w['gate_digest0'] = ctx.cache_id, ctx.gate_digest
    p = entry_cmd(w, ['plan', '--config', w['T3']['path']], 'plan_w1')
    nw = (p['json'] or {}).get('next_wave') or {}
    check('%s02.entry_plan_W1_is_one_call_(the_seed)_with_gates_ok' % label, 'MUST_PASS',
          p['rc'] == 0 and (p['json'] or {}).get('gates_ok') is True and nw.get('n_calls') == 1 and nw['calls'][0]['key'] == SEED_KEY16,
          {'rc': p['rc'], 'n_calls': nw.get('n_calls')})
    run_wave(w, label + '03', 1, 1)
    a = accept_cmd(w, w['deps_good'], 'acc_w1', 1, 0)
    aj = a['json'] or {}
    reg = json.loads(Path(w['registry']['path']).read_bytes())
    check('%s04.acceptance_step_c2v004_W1:_ACCEPTED,_VALID,_f6_action_CACHED_VALID,_prelaunch_bundle_is_the_genesis_record\'s' % label,
          'MUST_PASS', a['rc'] == 0 and aj.get('reading') == 'ACCEPTED' and (aj.get('reingest') or {}).get('classification') == 'VALID'
          and aj.get('f6_action') == 'CACHED_VALID' and aj.get('schema') == 'H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V004' and
          aj.get('prelaunch_bundle') in [r['bundle'] for r in reg['points'].values()],
          {'rc': a['rc'], 'reading': aj.get('reading'), 'f6': aj.get('f6_action')})


def points_manifest(w, label, tag, n_expected=None):
    out = Path(w['dir']) / ('POINTS_%s' % tag)
    r = entry_cmd(w, ['points-manifest', '--config', w['T3']['path'], '--out-dir', str(out)], 'pm_%s' % tag)
    js = r['json'] or {}
    lp = js.get('points_list') or {}
    doc = json.loads(Path(lp['path']).read_bytes()) if lp else {}
    ok = (r['rc'] == 0 and js.get('status') == 'OK' and doc.get('schema') == 'H3_CAMPAIGN_POINTS_LIST_C2V003' and
          doc.get('n_points', 0) >= 1 and (n_expected is None or doc['n_points'] == n_expected) and
          all(sha(p['spec']['path']) == p['spec']['sha256'] == p['pending_spec_sha256'] for p in doc.get('points') or []))
    check('%s.points_manifest_lists_the_next_wave\'s_unregistered_points_as_mapper_built_specs_(pending_slots)' % label, 'MUST_PASS', ok,
          {'rc': r['rc'], 'wave': doc.get('wave'), 'n_points': doc.get('n_points'), 'skipped_registered': doc.get('n_registered_skipped')})
    return lp, doc


def certify_and_append(w, label, list_pin, tag):
    c = cp1_certify(w, list_pin, tag)
    v = c['verify']
    check('%sa.CP_1_list_successor_(c3v004_run_point,_mock_producers)_certifies_every_listed_point:_GQ,_EPS,_RHO,_adapt_eps,_bundle,_'
          'records;_the_offline_c3v004_replica_verifies' % label, 'MUST_PASS',
          c['scheduler_rc'] == 0 and all(x == 0 for x in c['point_rc'].values()) and all(x == 0 for x in c['adapt_rc']) and
          v['ok'] and v['n_ok'] == v['n'] == len(c['rows']),
          {'scheduler': c['scheduler_rc'], 'points': len(c['point_rc']), 'verify': [v['ok'], v['n_ok'], v['n']]})
    rec = c['records']
    r = entry_cmd(w, ['ledger-append', '--config', w['T3']['path'], '--records', rec['path'], '--records-sha256', rec['sha256']],
                  'append_%s' % tag)
    js = r['json'] or {}
    st = entry_cmd(w, ['ledger-status', '--config', w['T3']['path']], 'lstatus_%s' % tag)
    sj = st['json'] or {}
    ok = (r['rc'] == 0 and js.get('status') == 'OK' and len(js.get('appended') or []) == len(c['rows']) and st['rc'] == 0 and
          (sj.get('head') or {}).get('head_sha256') == js.get('head_sha256') and
          sj.get('file_sha256') == (js.get('ledger') or {}).get('sha256'))
    check('%sb.entry_ledger_append_appends_the_wave\'s_records_under_the_lock;_ledger_status_reads_the_same_head' % label, 'MUST_PASS',
          ok, {'rc': r['rc'], 'appended': len(js.get('appended') or []), 'n_entries': js.get('n_entries'),
               'head': str(js.get('head_sha256'))[:16], 'reasons': str(js.get('reasons'))[:160]})
    return c, js


def e2e_a(w):
    label = 'EA'
    e2e_w1(w, label)
    p2 = entry_cmd(w, ['plan', '--config', w['T3']['path']], 'plan_w2_unregistered')
    check('EA05.unregistered_point:_with_genesis_=_W1_and_an_empty_ledger_the_wave_2_plan_refuses_at_certificate_preflight', 'MUST_FAIL',
          p2['rc'] == 3 and 'CERTIFICATE_PREFLIGHT' in json.dumps(p2['json']) and 'CERTIFICATE_POINT_MISSING' in json.dumps(p2['json']),
          {'rc': p2['rc']})
    lp, doc = points_manifest(w, 'EA06', 'W0002', 3)
    STATE['wave2_thetas'] = [p['theta'] for p in doc.get('points') or []]
    w['list_w2'] = lp
    guard('P03', lambda: t_cp1_list_rules(w, lp))
    # ledger-append refusals before the good append (nothing may be appended)
    m = cp1_modules()
    c = cp1_certify(w, lp, 'W0002')
    w['cp1_w2'] = c
    v = c['verify']
    check('EA07.CP_1_list_successor_(c3v004_run_point,_mock_producers)_certifies_wave_2:_GQ,_EPS,_RHO,_adapt_eps,_bundle,_records;_the_'
          'offline_c3v004_replica_verifies', 'MUST_PASS',
          c['scheduler_rc'] == 0 and all(x == 0 for x in c['point_rc'].values()) and all(x == 0 for x in c['adapt_rc']) and
          v['ok'] and v['n_ok'] == v['n'] == 3, {'scheduler': c['scheduler_rc'], 'verify': [v['ok'], v['n_ok'], v['n']]})
    rec = c['records']
    recdoc = json.loads(Path(rec['path']).read_bytes())
    fd = Path(w['dir']) / 'RECORD_VARIANTS'
    fd.mkdir()
    b0 = json.loads(Path(recdoc['records'][0]['record']['bundle']['path']).read_bytes())
    epsd = json.loads(Path(b0['prelaunch']['EPS']['path']).read_bytes())
    eps_bad = put_x(fd / 'EPS_PROOF_UNAPPROVED.json', dict(epsd, producer=w['unapproved']))
    b0['prelaunch']['EPS'] = eps_bad
    b_bad = put_x(fd / 'BUNDLE_UNAPPROVED.json', b0)
    v1 = copy.deepcopy(recdoc)
    v1['records'][0]['record']['bundle'] = b_bad
    p_v1 = put_x(fd / 'RECORDS_UNAPPROVED_BUNDLE.json', v1)
    v2 = copy.deepcopy(recdoc)
    v2['records'][0]['theta'] = recdoc['records'][1]['theta']
    p_v2 = put_x(fd / 'RECORDS_OTHER_THETA.json', v2)
    v3 = copy.deepcopy(recdoc)
    v3['records'][0]['record'] = recdoc['records'][1]['record']
    p_v3 = put_x(fd / 'RECORDS_OTHER_POINT_RECORD.json', v3)
    outs = {}
    for tag, pin in (('unapproved_bundle', p_v1), ('other_theta', p_v2), ('other_point_record', p_v3),
                     ('sha_mismatch', dict(rec, sha256='0' * 64))):
        r = entry_cmd(w, ['ledger-append', '--config', w['T3']['path'], '--records', pin['path'], '--records-sha256', pin['sha256']],
                      'append_bad_%s' % tag)
        outs[tag] = (r['rc'], str((r['json'] or {}).get('reasons'))[:100])
    lg = Path(w['ledger']['path'])
    check('EA08.ledger_append_refuses_a_bundle_naming_an_unapproved_producer,_another_point\'s_theta,_another_point\'s_record,_a_records_'
          'sha_mismatch;_nothing_is_appended', 'MUST_FAIL',
          all(x[0] == 3 for x in outs.values()) and 'GUARD_REFUSED' in outs['unapproved_bundle'][1] and
          'THETA_OR_PENDING_SPEC' in outs['other_theta'][1] and 'RECORD_NOT_THIS_POINT' in outs['other_point_record'][1] and
          'sha256 mismatch' in outs['sha_mismatch'][1] and not lg.exists(), outs)
    r = entry_cmd(w, ['ledger-append', '--config', w['T3']['path'], '--records', rec['path'], '--records-sha256', rec['sha256']],
                  'append_w2')
    js = r['json'] or {}
    st = entry_cmd(w, ['ledger-status', '--config', w['T3']['path']], 'lstatus_w2')
    sj = st['json'] or {}
    check('EA09.entry_ledger_append_appends_wave_2\'s_3_records_under_the_lock;_ledger_status_reads_the_same_head_and_file_sha', 'MUST_PASS',
          r['rc'] == 0 and len(js.get('appended') or []) == 3 and js.get('n_entries') == 3 and
          (sj.get('head') or {}).get('head_sha256') == js.get('head_sha256') and sj.get('file_sha256') == (js.get('ledger') or {}).get('sha256'),
          {'rc': r['rc'], 'head': str(js.get('head_sha256'))[:16], 'reasons': str(js.get('reasons'))[:160]})
    w['append_w2'] = js
    r2 = entry_cmd(w, ['ledger-append', '--config', w['T3']['path'], '--records', rec['path'], '--records-sha256', rec['sha256']],
                   'append_w2_again')
    check('EA10.the_same_records_appended_again_refuse_LEDGER_KEY_ALREADY_REGISTERED;_the_ledger_bytes_are_unchanged', 'MUST_FAIL',
          r2['rc'] == 3 and 'ALREADY_REGISTERED' in str((r2['json'] or {}).get('reasons')) and sha(lg) == js['ledger']['sha256'],
          str((r2['json'] or {}).get('reasons'))[:100])
    c2 = W_ctx(w)
    check('EA11.the_cache_id_and_the_gate_digest_do_not_move_as_the_ledger_grows_(no_head_sha_in_config_or_key)', 'MUST_PASS',
          c2.cache_id == w['cache_id0'] and c2.gate_digest == w['gate_digest0'] and c2.ledger_head()['n_entries'] == 3,
          {'cache_id': c2.cache_id[:16]})
    p3 = entry_cmd(w, ['plan', '--config', w['T3']['path']], 'plan_w2_ledger')
    nw = (p3['json'] or {}).get('next_wave') or {}
    planned = sorted(c['spec_sha256'] for c in nw.get('calls') or [])
    ledger_planned = sorted(a['planned_spec_sha256'] for a in js.get('appended') or [])
    check('EA12.plan_via_the_ledger:_wave_2_plans_3_calls_whose_spec_shas_are_the_ledger_entries\'_planned_spec_shas', 'MUST_PASS',
          p3['rc'] == 0 and nw.get('n_calls') == 3 and planned == ledger_planned and (p3['json'] or {}).get('gates_ok') is True,
          {'rc': p3['rc'], 'n_calls': nw.get('n_calls')})
    n = run_wave(w, 'EA13', 2, 3)
    accept_all(w, 'EA14', 2, n or 0, w['deps_good'])
    s = status(w, 'status_w2')
    cc = cached(w)
    check('EA15.reuse_via_the_ledger:_status_re_opens_the_cache_(4_VALID;_the_3_ledger_points\'_certificates_re_verified)', 'MUST_PASS',
          s.get('n_cached') == 4 and sorted(v[0] for v in cc.values()) == ['VALID'] * 4, {'n_cached': s.get('n_cached')})
    guard('F', lambda: t_forged_ledgers(w))
    # last on world A: a truncated ledger (its last entry removed) closes every cache open of the removed point
    lg = Path(w['ledger']['path'])
    lines = lg.read_bytes().split(b'\n')[:-1]
    with open(lg, 'wb') as f:
        f.write(b'\n'.join(lines[:-1]) + b'\n')
    t = entry_cmd(w, ['status', '--config', w['T3']['path']], 'status_truncated')
    check('F03.a_truncated_ledger_(last_entry_removed)_refuses_every_cache_open:_the_removed_point\'s_entry_no_longer_maps_its_spec',
          'MUST_FAIL', t['rc'] == 3 and len(lines) == 3 and 'M3' in json.dumps(t['json']), str((t['json'] or {}).get('reasons'))[:140])


def W_ctx(w):
    return w['W'].Context(w['T3']['path'])


def e2e_b(w):
    label = 'EB'
    e2e_w1(w, label)
    p2 = entry_cmd(w, ['plan', '--config', w['T3']['path']], 'plan_w2_genesis')
    nw = (p2['json'] or {}).get('next_wave') or {}
    check('EB05.wave_2_pre_registered_in_the_genesis_(as_CP_1_rows_29_31)_plans_3_calls_with_an_empty_ledger', 'MUST_PASS',
          p2['rc'] == 0 and nw.get('n_calls') == 3 and W_ctx(w).ledger_head()['n_entries'] == 0, {'n_calls': nw.get('n_calls')})
    n2 = run_wave(w, 'EB06', 2, 3)
    accept_all(w, 'EB07', 2, n2 or 0, w['deps_good'])
    p3 = entry_cmd(w, ['plan', '--config', w['T3']['path']], 'plan_w3_unregistered')
    check('EB08.unregistered_point:_the_engine_chosen_wave_3_(march0_style)_plan_refuses_at_certificate_preflight', 'MUST_FAIL',
          p3['rc'] == 3 and 'CERTIFICATE_POINT_MISSING' in json.dumps(p3['json']), {'rc': p3['rc']})
    lp, doc = points_manifest(w, 'EB09', 'W0003')
    w3_keys = {p['call_key'] for p in doc.get('points') or []}
    c, js = certify_and_append(w, 'EB10', lp, 'W0003')
    p3b = entry_cmd(w, ['plan', '--config', w['T3']['path']], 'plan_w3_ledger')
    nw3 = (p3b['json'] or {}).get('next_wave') or {}
    check('EB11.after_the_ledger_append_wave_3_plans_(every_call_a_ledger_point)', 'MUST_PASS',
          p3b['rc'] == 0 and nw3.get('n_calls') == doc.get('n_next_wave_calls') and nw3.get('n_calls', 0) >= 1,
          {'n_calls': nw3.get('n_calls')})
    n3 = run_wave(w, 'EB12', 3, nw3.get('n_calls'))
    w['n3'] = n3
    e2e_b_f6(w, n3)


def pass_dirs(call_dir):
    """The ACCEPTANCE_TAILSTATES_* names in a call dir (read-only)."""
    return sorted(p.name for p in Path(call_dir).iterdir() if p.name.startswith('ACCEPTANCE_TAILSTATES_'))


def reasons(r):
    return json.dumps((r.get('json') or {}).get('reasons'))


def handoff_direct(w, wave, ci, root_refs, tag):
    """Declared bypass (c2v004): the adopted handoff v004 called directly on a campaign call, in process, OUTSIDE the
    acceptance step (as accept_direct does for HEADLINE11).  The pass it makes is a real ACCEPTANCE_TAILSTATES pass."""
    W, H = w['W'], w['H']
    ctx = W.Context(w['T3']['path'])
    cd = work_dir(w) / 'waves' / ('wave_%04d' % wave) / 'campaign' / ('call_%04d' % ci)
    spec = json.loads((cd / 'spec.json').read_bytes())
    rec = ctx.certificate_record(W.point_identity(spec))
    d = deps_doc(w, root_refs)
    policy = dict({k: d['policy'][k] for k in ('approved_certificate_producers', 'trusted_source_producers', 'row_policy_reviews',
                                               'packet_binding_reviews', 'evidence_producer', 'approved_review_sha256',
                                               'approved_evidence_producer_sha256', 'approved_uniform_producer_sha256',
                                               'root_ruling_refs')},
                  receipt={'path': str(cd / 'RECEIPT.json'), 'sha256': sha(cd / 'RECEIPT.json')}, prelaunch_bundle=rec['bundle'])
    return H.accept_call(call_dir=str(cd), spec=spec, deps=H.load_deps(d['deps']), policy=policy,
                         records_dir=str(Path(w['dir']) / ('RECORDS_%s' % tag)), mode='guard')


def b2_cmd(w, wave, ci, bundle, record, tag):
    return entry_cmd(w, ['reingest', '--config', w['T3']['path'], '--wave', str(wave), '--call-index', str(ci), '--bundle',
                         bundle['path'], '--bundle-sha256', bundle['sha256'], '--acceptance-record', record['path'],
                         '--acceptance-record-sha256', record['sha256']], tag)


def plan_keys(w, wave):
    p = json.loads((work_dir(w) / 'waves' / ('wave_%04d' % wave) / 'WAVE_PLAN.json').read_text())
    return {c['call_index']: c['key'] for c in p['calls']}


def e2e_b_f6(w, n3):
    """V006 A192 item 3 on wave 3: certified MODEL_INVALID for NON_LAPSE_TAIL_MATERIAL / BOUND_INSUFFICIENT only; c2v004 B1:
    a second pass only after an INCOMPLETE first pass (C04), never a third; then wave 4 (C03, stale records)."""
    wd = Path(w['dir'])
    calls = work_dir(w) / 'waves' / 'wave_0003' / 'campaign'
    nl = deps_record(w, 'NON_LAPSE', {'SYN_LO_VERDICT': 'FAIL'})
    bi = deps_record(w, 'BOUND_INSUFFICIENT', {'SYN_SRB_READING': 'BOUND_INSUFFICIENT'})
    wrong = deps_record(w, 'WRONG_LO_PRODUCER', {'SYN_LO_PRODUCER': w['unapproved']})
    w['deps_nl'] = nl
    keys3 = plan_keys(w, 3)
    k0 = keys3[0]
    # call 0: NON_LAPSE_TAIL_MATERIAL; that reading stands (C04: no second pass after it)
    a0 = accept_cmd(w, nl, 'w3c0_nl_1', 3, 0)
    j0 = a0['json'] or {}
    check('EB13.call_0_reads_NON_LAPSE_TAIL_MATERIAL:_exit_13,_nothing_cached,_rows_are_not_model_output,_f6_action_CERTIFIED_MODEL_'
          'INVALID_ELIGIBLE,_one_acceptance_pass', 'MUST_PASS',
          a0['rc'] == 13 and j0.get('reading') == 'NON_LAPSE_TAIL_MATERIAL' and j0.get('rows_are_model_output') is False and
          str(j0.get('f6_action')).startswith('CERTIFIED_MODEL_INVALID_ELIGIBLE') and j0.get('reingest') is None and
          j0.get('acceptance_passes_after') == 1 and j0.get('schema') == 'H3_CAMPAIGN_ACCEPT_STEP_RECORD_C2V004',
          {'rc': a0['rc'], 'reading': j0.get('reading'), 'f6': str(j0.get('f6_action'))[:40], 'passes': j0.get('acceptance_passes_after')})
    rec0 = j0.get('acceptance_record')
    c0 = calls / 'call_0000'
    a0b = accept_cmd(w, w['deps_good'], 'w3c0_rerun_no_record', 3, 0)
    a0c = accept_cmd(w, w['deps_good'], 'w3c0_rerun_nl_record', 3, 0, first_pass=rec0)
    check('EB14.C04:_a_second_acceptance_pass_after_a_NON_LAPSE_first_pass_refuses_(no_first_pass_record:_FIRST_PASS_RECORD_REQUIRED;_'
          'the_NON_LAPSE_record_pinned:_READING_STANDS);_nothing_written,_one_pass,_nothing_cached', 'MUST_FAIL',
          a0b['rc'] == 3 and 'ACCEPTANCE_RERUN_FIRST_PASS_RECORD_REQUIRED' in reasons(a0b) and a0c['rc'] == 3 and
          'ACCEPTANCE_RERUN_NOT_AFTER_INCOMPLETE' in reasons(a0c) and 'FIRST_PASS_READING_STANDS' in reasons(a0c) and
          not Path(a0b['records_dir']).exists() and not Path(a0c['records_dir']).exists() and len(pass_dirs(c0)) == 1 and
          k0 not in cached(w), {'no_record': reasons(a0b)[:70], 'nl_record': reasons(a0c)[:150], 'passes': pass_dirs(c0)})
    if n3 >= 2:
        o = reingest_invalid_cmd(w, 3, 1, rec0, 'ri_other_call')
        check('EB15.MODEL_INVALID_on_another_call:_call_0\'s_record_offered_for_call_1_refuses_OTHER_CALL_/_OTHER_RECEIPT', 'MUST_FAIL',
              o['rc'] == 3 and 'TAIL_INVALID_RECORD_OTHER_CALL' in str((o['json'] or {}).get('reasons')),
              str((o['json'] or {}).get('reasons'))[:140])
    ri = reingest_invalid_cmd(w, 3, 0, rec0, 'ri_c0')
    rj = ri['json'] or {}
    s = status(w, 'status_after_ri_c0')
    cc = cached(w)
    check('EB16.entry_reingest_invalid_caches_call_0_MODEL_INVALID_(TAIL_ACCEPTANCE_NON_LAPSE_TAIL_MATERIAL,_source_TAIL_ACCEPTANCE_'
          'CERTIFIED,_no_forward_call;_its_record_is_of_the_latest_pass);_status_re_opens_and_re_verifies_it', 'MUST_PASS',
          ri['rc'] == 0 and rj.get('classification') == 'MODEL_INVALID' and rj.get('new_cache_entry') is True and
          cc.get(k0) == ('MODEL_INVALID', 'TAIL_ACCEPTANCE_CERTIFIED', 'TAIL_ACCEPTANCE_NON_LAPSE_TAIL_MATERIAL') and
          s.get('status') == 'OK' and s.get('n_cached') == 5 and rj.get('launches_performed') == 0,
          {'rc': ri['rc'], 'n_cached': s.get('n_cached'), 'entry': cc.get(k0)})
    ri2 = reingest_invalid_cmd(w, 3, 0, rec0, 'ri_c0_again')
    check('EB17.reingest_invalid_of_an_already_cached_call_refuses_ALREADY_CACHED', 'MUST_FAIL',
          ri2['rc'] == 3 and 'ALREADY_CACHED' in str((ri2['json'] or {}).get('reasons')), str((ri2['json'] or {}).get('reasons'))[:100])
    nxt = 1
    if n3 >= 2:
        a1 = accept_cmd(w, bi, 'w3c1_bi', 3, 1)
        j1 = a1['json'] or {}
        ri1 = reingest_invalid_cmd(w, 3, 1, j1.get('acceptance_record') or {'path': '/x', 'sha256': '0' * 64}, 'ri_c1')
        r1j = ri1['json'] or {}
        check('EB18.call_1_reads_BOUND_INSUFFICIENT_(exit_13)_and_reingest_invalid_caches_it_MODEL_INVALID_TAIL_ACCEPTANCE_BOUND_INSUFFICIENT',
              'MUST_PASS', a1['rc'] == 13 and j1.get('reading') == 'BOUND_INSUFFICIENT' and j1.get('rows_are_model_output') is False
              and ri1['rc'] == 0 and r1j.get('failure_class') == 'TAIL_ACCEPTANCE_BOUND_INSUFFICIENT',
              {'reading': j1.get('reading'), 'ri_rc': ri1['rc'], 'fc': r1j.get('failure_class')})
        nxt = 2
    # the next call: INCOMPLETE first (MUST_FAIL as MODEL_INVALID), the one rerun (refused without its record, runs with it),
    # ACCEPTED (MUST_FAIL as MODEL_INVALID), the third pass (MUST_FAIL), then VALID through the B2 reingest
    if n3 > nxt:
        i = nxt
        ci = calls / ('call_%04d' % i)
        inc = accept_cmd(w, wrong, 'w3c%d_incomplete' % i, 3, i)
        ij = inc['json'] or {}
        r_inc = reingest_invalid_cmd(w, 3, i, ij.get('acceptance_record') or {'path': '/x', 'sha256': '0' * 64}, 'ri_incomplete')
        check('EB19.MODEL_INVALID_on_an_INCOMPLETE_record_refuses_TAIL_INVALID_READING_NOT_CERTIFIABLE_(f6_action_RERUN_ONCE)', 'MUST_FAIL',
              inc['rc'] == 13 and ij.get('reading') == 'INCOMPLETE' and str(ij.get('f6_action')).startswith('RERUN_ACCEPTANCE_ONCE') and
              'first-pass-record' in str(ij.get('f6_action')) and ij.get('acceptance_passes_after') == 1 and
              r_inc['rc'] == 3 and 'READING_NOT_CERTIFIABLE' in str((r_inc['json'] or {}).get('reasons')),
              {'reading': ij.get('reading'), 'ri': str((r_inc['json'] or {}).get('reasons'))[:80]})
        inc_rec = ij.get('acceptance_record') or {'path': '/x', 'sha256': '0' * 64}
        n_none = accept_cmd(w, w['deps_good'], 'w3c%d_rerun_no_record' % i, 3, i, kind='accept_handoff_only')
        n_other = accept_cmd(w, w['deps_good'], 'w3c%d_rerun_other_call' % i, 3, i, kind='accept_handoff_only', first_pass=rec0)
        n_sha = accept_cmd(w, w['deps_good'], 'w3c%d_rerun_sha' % i, 3, i, kind='accept_handoff_only',
                           first_pass=dict(inc_rec, sha256='0' * 64))
        check('EB26.the_rerun_after_INCOMPLETE_refuses_without_the_first_pass_record,_with_another_call\'s_record,_with_a_sha_'
              'mismatch_(nothing_written,_one_pass)', 'MUST_FAIL',
              all(x['rc'] == 3 and not Path(x['records_dir']).exists() for x in (n_none, n_other, n_sha)) and
              'FIRST_PASS_RECORD_REQUIRED' in reasons(n_none) and 'FIRST_PASS_RECORD_OTHER_CALL' in reasons(n_other) and
              'FIRST_PASS_RECORD_NOT_THE_FIRST_PASS' in reasons(n_other) and 'sha256 mismatch' in reasons(n_sha) and
              len(pass_dirs(ci)) == 1, {'none': reasons(n_none)[:60], 'other': reasons(n_other)[:120], 'sha': reasons(n_sha)[:120]})
        h = accept_cmd(w, w['deps_good'], 'w3c%d_handoff_only' % i, 3, i, kind='accept_handoff_only', first_pass=inc_rec)
        hj = h['json'] or {}
        pd = pass_dirs(ci)
        check('EB27.A192_INCOMPLETE_reruns_once:_with_the_call\'s_own_INCOMPLETE_first_pass_record_pinned_the_second_pass_runs_'
              '(reads_ACCEPTED;_two_passes)', 'MUST_PASS',
              hj.get('reading') == 'ACCEPTED' and hj.get('acceptance_passes_after') == 2 and hj.get('first_pass_record') == inc_rec
              and len(pd) == 2 and hj.get('acceptance_pass') == str(ci.resolve() / pd[-1]),
              {'reading': hj.get('reading'), 'passes': pd, 'reingest': (hj.get('reingest') or {}).get('status')})
        r_acc = reingest_invalid_cmd(w, 3, i, hj.get('acceptance_record') or {'path': '/x', 'sha256': '0' * 64}, 'ri_accepted')
        check('EB20.MODEL_INVALID_on_an_ACCEPTED_call:_reingest_invalid_with_the_call\'s_own_ACCEPTED_record_refuses_READING_NOT_'
              'CERTIFIABLE_(nothing_cached)', 'MUST_FAIL',
              hj.get('reading') == 'ACCEPTED' and (hj.get('reingest') or {}).get('status') == STUB_STATUS and r_acc['rc'] == 3 and
              'READING_NOT_CERTIFIABLE' in str((r_acc['json'] or {}).get('reasons')) and
              not (calls / ('call_%04d' % i) / 'TAIL_CERTIFICATE_ACCEPTANCE.json').exists(),
              str((r_acc['json'] or {}).get('reasons'))[:120])
        t3 = accept_cmd(w, w['deps_good'], 'w3c%d_third_pass' % i, 3, i, first_pass=inc_rec)
        check('EB28.third_pass:_with_two_passes_in_the_call_dir_the_step_refuses_ACCEPTANCE_RERUN_LIMIT_even_with_the_INCOMPLETE_'
              'record_pinned_(nothing_written)', 'MUST_FAIL',
              t3['rc'] == 3 and 'ACCEPTANCE_RERUN_LIMIT' in reasons(t3) and not Path(t3['records_dir']).exists() and
              len(pass_dirs(ci)) == 2, reasons(t3)[:100])
        b2 = b2_cmd(w, 3, i, hj['bundle'], hj['acceptance_record'], 'b2_reingest_w3c%d' % i)
        check('EB21.the_same_ACCEPTED_call_caches_VALID_through_the_B2_reingest_(the_record_of_the_latest_pass;_a_ledger_point:_'
              'write_acceptance_uses_the_one_lookup)', 'MUST_PASS', b2['rc'] == 0 and (b2['json'] or {}).get('classification') == 'VALID',
              {'rc': b2['rc'], 'reasons': reasons(b2)[:100]})
        nxt += 1
    if n3 > nxt:
        accept_all(w, 'EB22', 3, n3, w['deps_good'], skip=tuple(range(nxt)))
    s = status(w, 'status_w3_done')
    cc = cached(w)
    inv = sorted(v[2] for v in cc.values() if v[0] == 'MODEL_INVALID')
    want_inv = sorted(['TAIL_ACCEPTANCE_NON_LAPSE_TAIL_MATERIAL'] + (['TAIL_ACCEPTANCE_BOUND_INSUFFICIENT'] if n3 >= 2 else []))
    check('EB23.wave_3_fully_cached:_status_re_opens_every_entry_(VALID_and_the_certified_MODEL_INVALID)', 'MUST_PASS',
          s.get('status') == 'OK' and s.get('n_cached') == 4 + n3 and inv == want_inv, {'n_cached': s.get('n_cached'), 'invalid': inv})
    out = wd / 'POINTS_W0004'
    r = entry_cmd(w, ['points-manifest', '--config', w['T3']['path'], '--out-dir', str(out)], 'pm_W0004')
    js = r['json'] or {}
    pl = json.loads(Path(js['points_list']['path']).read_bytes()) if js.get('points_list') else {}
    keys4 = {p['call_key'] for p in pl.get('points') or []}
    check('EB24.reuse:_with_wave_3_cached_(incl._the_certified_invalid_points)_the_probe_moves_on;_the_next_wave\'s_points_are_new',
          'MUST_PASS', (r['rc'] == 0 and pl.get('wave') == 4 and not (keys4 & set(cc))) or
          (r['rc'] == 3 and ('PROBE_COMPLETE' in str(js.get('reasons')) or 'NOTHING_TO_CERTIFY' in str(js.get('reasons')))),
          {'rc': r['rc'], 'wave': pl.get('wave'), 'n_points': pl.get('n_points'), 'reasons': str(js.get('reasons'))[:80]})
    guard('EB29', lambda: e2e_b_w4(w, js.get('points_list')))
    # last: tampering with the acceptance record of the certified invalid entry closes every cache open
    ref = (json.loads((Path(a0['records_dir']) / 'ACCEPT_STEP_RECORD_W0003_C0000.json').read_text()))['acceptance_record']
    os.chmod(ref['path'], 0o644)
    with open(ref['path'], 'ab') as f:
        f.write(b' ')
    t = entry_cmd(w, ['status', '--config', w['T3']['path']], 'status_tampered')
    check('EB25.a_changed_byte_in_the_certified_invalid\'s_acceptance_record_refuses_every_cache_open_(status_exit_3)', 'MUST_FAIL',
          t['rc'] == 3 and 'tail acceptance record' in json.dumps(t['json']), str((t['json'] or {}).get('reasons'))[:140])


def e2e_b_w4(w, lp):
    """c2v004 B1 on wave 4: C03 and the stale-record reingests, on calls certified through the CP-1 list successor + ledger."""
    if not lp:
        check('EB29.wave_4_points_list_from_EB24', 'MUST_PASS', False, 'no POINTS_W0004 list')
        return
    certify_and_append(w, 'EB29', lp, 'W0004')
    n4 = run_wave(w, 'EB29c', 4)
    if not n4 or n4 < 2:
        check('EB29d.wave_4_has_at_least_2_calls_for_the_B1_rows', 'MUST_PASS', False, {'n4': n4})
        return
    w['n4'] = n4
    calls = work_dir(w) / 'waves' / 'wave_0004' / 'campaign'
    keys = plan_keys(w, 4)
    # call 4.0, C03: the first pass reads ACCEPTED and is not cached (the entry's reingest stubbed, as the verifier's C03)
    c0 = calls / 'call_0000'
    p1 = accept_cmd(w, w['deps_good'], 'w4c0_accepted_pass1', 4, 0, kind='accept_handoff_only')
    p1j = p1['json'] or {}
    rec1 = p1j.get('acceptance_record') or {'path': '/x', 'sha256': '0' * 64}
    r_none = accept_cmd(w, w['deps_nl'], 'w4c0_pass2_no_record', 4, 0)
    r_acc = accept_cmd(w, w['deps_nl'], 'w4c0_pass2_accepted_record', 4, 0, first_pass=rec1)
    check('EB30.C03:_after_a_first_pass_reading_ACCEPTED_(not_cached)_a_second_pass_refuses_(no_record:_FIRST_PASS_RECORD_REQUIRED;_'
          'the_ACCEPTED_record_pinned:_READING_STANDS);_nothing_written,_one_pass,_nothing_cached', 'MUST_FAIL',
          p1j.get('reading') == 'ACCEPTED' and (p1j.get('reingest') or {}).get('status') == STUB_STATUS and
          r_none['rc'] == 3 and 'ACCEPTANCE_RERUN_FIRST_PASS_RECORD_REQUIRED' in reasons(r_none) and r_acc['rc'] == 3 and
          'FIRST_PASS_READING_STANDS' in reasons(r_acc) and not Path(r_none['records_dir']).exists() and
          not Path(r_acc['records_dir']).exists() and len(pass_dirs(c0)) == 1 and keys[0] not in cached(w),
          {'pass1': p1j.get('reading'), 'no_record': reasons(r_none)[:60], 'accepted_record': reasons(r_acc)[:140]})
    # declared simulation: the VALID reingest of the ACCEPTED pass wrote TAIL_CERTIFICATE_ACCEPTANCE.json and stopped before its
    # cache put (the wrapper's own write_acceptance, in process); then a second pass made by calling the handoff directly
    ctx = w['W'].Context(w['T3']['path'])
    ctx.write_acceptance(c0, p1j['bundle'])
    h2, h2ref = handoff_direct(w, 4, 0, {'SYN_LO_VERDICT': 'FAIL'}, 'w4c0_direct_pass2_nl')
    ri = reingest_invalid_cmd(w, 4, 0, h2ref, 'ri_w4c0_handoff_file')
    pd0 = pass_dirs(c0)
    check('EB31.C03:_reingest_invalid_refuses_a_NON_LAPSE_record_of_the_latest_pass_while_the_call_dir_holds_TAIL_CERTIFICATE_'
          'ACCEPTANCE.json_(an_ACCEPTED_pass_was_reingested);_nothing_cached', 'MUST_FAIL',
          (c0 / 'TAIL_CERTIFICATE_ACCEPTANCE.json').is_file() and h2.get('reading') == 'NON_LAPSE_TAIL_MATERIAL' and len(pd0) == 2 and
          h2.get('tailstate_dir') == str(c0.resolve() / pd0[-1]) and ri['rc'] == 3 and
          'TAIL_INVALID_CALL_HOLDS_TAIL_CERTIFICATE_ACCEPTANCE' in reasons(ri) and 'NOT_THE_LATEST_PASS' not in reasons(ri) and
          keys[0] not in cached(w), {'pass2': h2.get('reading'), 'passes': pd0, 'reasons': reasons(ri)[:160]})
    st = b2_cmd(w, 4, 0, p1j['bundle'], rec1, 'b2_stale_w4c0')
    check('EB32.stale_record_VALID_reingest:_the_first_pass\'s_ACCEPTED_record_after_a_later_pass_refuses_REINGEST_RECORD_NOT_THE_'
          'LATEST_PASS_(under_the_work_dir_lock;_nothing_cached)', 'MUST_FAIL',
          st['rc'] == 3 and 'REINGEST_RECORD_NOT_THE_LATEST_PASS' in reasons(st) and keys[0] not in cached(w), reasons(st)[:160])
    # call 4.1: the first pass reads NON_LAPSE; a later pass (direct handoff) reads ACCEPTED
    c1 = calls / 'call_0001'
    q1 = accept_cmd(w, w['deps_nl'], 'w4c1_nl_pass1', 4, 1)
    q1j = q1['json'] or {}
    nl_rec = q1j.get('acceptance_record') or {'path': '/x', 'sha256': '0' * 64}
    g2, g2ref = handoff_direct(w, 4, 1, None, 'w4c1_direct_pass2_good')
    ri_stale = reingest_invalid_cmd(w, 4, 1, nl_rec, 'ri_w4c1_stale')
    check('EB33.stale_record_reingest_invalid:_the_first_pass\'s_NON_LAPSE_record_after_a_later_pass_refuses_TAIL_INVALID_RECORD_NOT_'
          'THE_LATEST_PASS_(nothing_cached)', 'MUST_FAIL',
          q1['rc'] == 13 and q1j.get('reading') == 'NON_LAPSE_TAIL_MATERIAL' and g2.get('reading') == 'ACCEPTED' and
          len(pass_dirs(c1)) == 2 and ri_stale['rc'] == 3 and 'TAIL_INVALID_RECORD_NOT_THE_LATEST_PASS' in reasons(ri_stale) and
          keys[1] not in cached(w), {'pass1': q1j.get('reading'), 'pass2': g2.get('reading'), 'reasons': reasons(ri_stale)[:160]})
    b2 = b2_cmd(w, 4, 1, g2['bundle'], g2ref, 'b2_bypass_w4c1')
    cc = cached(w)
    check('EB34.residual_(declared,_measured):_a_second_pass_made_by_calling_the_handoff_directly,_outside_the_acceptance_step,_after_'
          'a_NON_LAPSE_first_pass:_the_B2_reingest_of_its_ACCEPTED_record_(the_latest_pass)', 'INFO', True,
          {'rc': b2['rc'], 'classification': (b2['json'] or {}).get('classification'), 'cached': cc.get(keys[1]),
           'reasons': reasons(b2)[:120],
           'reading': 'the rerun rule is enforced by the acceptance step; the wrapper sees only the latest pass'})


# ------------------------------------------------------------------------------------------------ S: storage
def t_storage(w):
    St = load(STORAGE, '_c3_storage')
    work = str(work_dir(w))
    rc, txt = quiet(St.main, ['wave', '--work-dir', work, '--next-calls', '1'])
    js = last_json(txt) or {}
    acc = [c for c in js.get('call_dirs') or [] if c['accepted']]
    check('S01.storage_c2v003_measures_b_as_the_call_dir_bytes_after_acceptance_(incl._ACCEPTANCE_TAILSTATES)_above_the_receipt_bytes',
          'MUST_PASS', rc == 0 and len(acc) >= 1 and all(c['acceptance_tailstate_dirs'] for c in acc) and
          js['measured_per_call_bytes_after_acceptance'] > (js['receipt_output_bytes_max_for_comparison'] or 0) > 0,
          {'n_accepted': len(acc), 'b': js.get('measured_per_call_bytes_after_acceptance'),
           'receipt_max': js.get('receipt_output_bytes_max_for_comparison')})
    b = 17442511906
    rc, txt = quiet(St.main, ['wave', '--work-dir', work, '--per-call-output-bytes', str(b), '--threshold-total-free-bytes',
                              str(int((2877.5 + 953.0) * GiB)), '--threshold-other-program-bytes', str(int(370.5 * GiB))])
    th = (last_json(txt) or {}).get('threshold') or {}
    check('S02.threshold_regression:_the_erratum\'s_inputs_give_R_=_3385.8_GiB_binding_at_wave_15_and_b*_=_17.08_GiB', 'MUST_PASS',
          th.get('R_GiB') == 3385.8 and th.get('binding_wave') == 15 and th.get('b_star_GiB') == 17.08 and
          th.get('b_star_binding_wave') == 15 and th.get('fits') is True, {k: th.get(k) for k in ('R_GiB', 'binding_wave', 'b_star_GiB', 'fits')})
    rc, txt = quiet(St.main, ['wave', '--work-dir', work, '--next-calls', '1000000'])
    check('S03.storage_c2v003_wave_check_exit_5_for_a_wave_that_cannot_fit', 'MUST_FAIL', rc == 5, rc)
    rc, txt = quiet(St.main, ['move', '--candidate', str(Path(w['dir']) / 'CERTS'), '--work-dir', work, '--pins-from', w['T3']['path']])
    check('S04.storage_c2v003_move_(c2v001\'s)_refuses_a_directory_holding_pinned_files', 'MUST_FAIL', rc == 3,
          str((last_json(txt) or {}).get('reasons'))[:100])


def t_pass_rule(w):
    """c2v004 B1: the wrapper's acceptance_passes (used by the step and by both reingest paths), on folders in the run dir."""
    W = w['W']
    d = Path(w['dir']) / 'PASS_RULE'
    d.mkdir()
    out = {}
    for tag, names, files in (('contiguous', ['A001', 'A002'], []), ('gap', ['A001', 'A003'], []), ('first_missing', ['A002'], []),
                              ('foreign_name', ['A001'], ['ACCEPTANCE_TAILSTATES_OTHER']),
                              ('a_file', ['A001'], ['ACCEPTANCE_TAILSTATES_C2V002_A002'])):
        c = d / tag
        c.mkdir()
        for n in names:
            (c / ('ACCEPTANCE_TAILSTATES_C2V002_' + n)).mkdir()
        for f in files:
            put_x(c / f, {'synthetic': True})
        try:
            out[tag] = W.acceptance_passes(c)
        except W.Error as exc:
            out[tag] = 'REFUSED: ' + str(exc)[:70]
    check('U01.the_wrapper_pass_rule:_the_handoff\'s_A001..A<n>_directories_oldest_first;_a_gap,_a_missing_first_pass,_another_'
          'ACCEPTANCE_TAILSTATES_name_or_a_file_of_that_name_refuses', 'MUST_FAIL',
          out['contiguous'] == ['ACCEPTANCE_TAILSTATES_C2V002_A001', 'ACCEPTANCE_TAILSTATES_C2V002_A002'] and
          all(str(out[k]).startswith('REFUSED') for k in ('gap', 'first_missing', 'foreign_name', 'a_file')), out)


def t_pins():
    bad = {k: sha(p) for k, (p, s) in NAMED.items() if s is not None and sha(p) != s}
    check('Z01.every_named_input_hashes_to_its_pin_from_bytes_(unchanged)', 'MUST_PASS', not bad, bad or len(NAMED))
    check('Z02.no_publish:_the_campaign_SUB_is_absent_from_calib_tail_readiness_cx2', 'MUST_PASS',
          not (CX2 / SUB).exists() and not (CX2 / 'v006r11_c4').exists(), str(CX2 / SUB))


# ------------------------------------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs-root', default=str(H3 / 'test_runs_c2v004'))
    ap.add_argument('--child')
    a = ap.parse_args(argv)
    if a.child:
        return child(a.child)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    rd = Path(a.runs_root).resolve() / ('RUN_%s_%d' % (stamp, os.getpid()))
    STATE['run_dir'] = str(rd)
    no_subprocess_platform()
    sys.addaudithook(_audit)
    rd.mkdir(parents=True)
    (rd / 'children').mkdir()
    t0 = time.monotonic()
    sm = rd / 'SYN_MODULES'
    sm.mkdir()
    for n in ('mock_driver_h3_c2v001.py', 'syn_h3_c2v003.py'):
        shutil.copyfile(SYN_SRC / n, sm / n)
    prods = {k: put_x(sm / ('syn_producer_%s_c2v003.py' % k), None, raw=('"""SYNTHETIC %s stub (c2v003 tests)."""\n' % k).encode())
             for k in ('eps_adapter', 'gq_producer', 'lo_slot_proof')}
    resp = put_x(sm / 'syn_producer_response_c2v003.py', None, raw=b'"""SYNTHETIC point response producer stub (c2v003 tests)."""\n')
    unap = put_x(sm / 'syn_producer_unapproved_c2v003.py', None, raw=b'"""SYNTHETIC unapproved producer stub (c2v003 tests)."""\n')
    rho_review = put_x(sm / 'SYN_PROOF_SIDE_REVIEW.json', {'schema': 'SYNTHETIC_PROOF_SIDE_REVIEW', 'synthetic': True})
    base = rd / 'SYNTHETIC_BASE' / 'tail_scheme_impl_c2' / 'driver_r5'
    base.mkdir(parents=True)
    shutil.copyfile(SYN_SRC / 'mock_driver_h3_c2v001.py', base / 'galaxy_m0_forward_c2v010.py')
    mock_sha = sha(base / 'galaxy_m0_forward_c2v010.py')
    tax = json.loads(NAMED['taxonomy'][0].read_bytes())
    tax['driver'] = {'path': str(base / 'galaxy_m0_forward_c2v010.py'), 'sha256': mock_sha}
    taxp = put_x(sm / 'FAILURE_TAXONOMY_SYNTHETIC_MOCK_DRIVER.json', tax)
    WORLD_CTX.update({'mock_sha': mock_sha, 'syn_base': str(rd / 'SYNTHETIC_BASE'), 'driver_path': str(base / 'galaxy_m0_forward_c2v010.py'),
                      'syn_module': {'path': str(sm / 'syn_h3_c2v003.py'), 'sha256': sha(sm / 'syn_h3_c2v003.py')},
                      'prods': prods, 'approved': [prods['eps_adapter'], prods['gq_producer'], prods['lo_slot_proof']],
                      'response_producer': resp, 'unapproved': unap, 'taxonomy': taxp,
                      'rho_gate': {'allow_rho': True, 'review_pin': rho_review, 'review_sha256': rho_review['sha256']}})
    guard('G', t_generator)
    guard('K', t_real_dry)
    guard('P', t_cp1_table_mode)
    worlds = {}

    def world_a():
        worlds['A'] = w = build_world('WORLD_A')
        w['deps_good'] = deps_record(w, 'GOOD')
        guard('R02', lambda: t_regen_world(w))
        guard('A', lambda: t_apply(w))
        guard('H', lambda: t_h11(w))
        e2e_a(w)
    guard('EA', world_a)

    def world_b():
        worlds['B'] = w = build_world('WORLD_B', extra_thetas=STATE.get('wave2_thetas') or [])
        w['deps_good'] = deps_record(w, 'GOOD')
        check('EB00.world_B_genesis_=_world_A\'s_points_+_the_3_wave_2_points_world_A_certified_through_its_ledger', 'MUST_PASS',
              w['n_points'] == worlds['A']['n_points'] + 3 and len(STATE.get('wave2_thetas') or []) == 3,
              {'A': worlds['A']['n_points'], 'B': w['n_points']})
        e2e_b(w)
    guard('EB', world_b)
    if 'B' in worlds:
        guard('S', lambda: t_storage(worlds['B']))
        guard('U', lambda: t_pass_rule(worlds['B']))
    guard('Z', t_pins)
    check('A90.audit_no_denials_and_no_foreign_subprocess', 'MUST_PASS',
          not AUDIT['denied'] and set(AUDIT['subprocess']) <= {PY, 'ps'}, {'denied': AUDIT['denied'][:3], 'subprocess': AUDIT['subprocess']})
    kids = sorted((rd / 'children').glob('*.out.json'))
    kd = [x for k in kids for x in json.loads(k.read_text()).get('audit_denied') or []]
    crashed = [k.name for k in kids if str(json.loads(k.read_text()).get('rc')).startswith('CRASH')]
    check('A91.audit_in_every_child_no_denials_and_no_crash', 'MUST_PASS', not kd and not crashed and len(kids) > 0,
          {'children': len(kids), 'denied': kd[:3], 'crashed': crashed[:3]})
    n_pass = sum(1 for r in RESULTS if r['pass'])
    doc = {'schema': 'CAMPAIGN_CERT_TEST_RESULTS_C2V004', 'utc': stamp, 'run_dir': str(rd), 'n': len(RESULTS), 'n_pass': n_pass,
           'n_must_pass': sum(1 for r in RESULTS if r['expect'] == 'MUST_PASS'),
           'n_must_fail': sum(1 for r in RESULTS if r['expect'] == 'MUST_FAIL'),
           'n_info': sum(1 for r in RESULTS if r['expect'] == 'INFO'), 'all_pass': n_pass == len(RESULTS),
           'wall_s': round(time.monotonic() - t0, 1), 'audit': {'denied': AUDIT['denied'], 'subprocess': AUDIT['subprocess'],
                                                               'n_opened': AUDIT['n_opened'], 'children': len(kids)},
           'inputs': {p.name: sha(p) for p in (GEN, WRAP_SRC, ENTRY_T, REGEN, ACCEPT, APPLY, STORAGE, CP1R, CP1A, CP1C, H11,
                                               Path(__file__), SYN_SRC / 'syn_h3_c2v003.py', SYN_SRC / 'mock_cp1_c2v003.py')},
           'wave3_n_calls': (worlds.get('B') or {}).get('n3'), 'wave4_n_calls': (worlds.get('B') or {}).get('n4'),
           'results': RESULTS}
    with open(rd / 'TEST_RESULTS.json', 'x') as f:
        json.dump(doc, f, indent=1, default=str)
        f.write('\n')
    print('%d / %d pass (MUST_PASS %d, MUST_FAIL %d, INFO %d); audit denied %d; wall %.0f s; %s' % (
        n_pass, len(RESULTS), doc['n_must_pass'], doc['n_must_fail'], doc['n_info'], len(AUDIT['denied']), doc['wall_s'], rd))
    return 0 if doc['all_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
