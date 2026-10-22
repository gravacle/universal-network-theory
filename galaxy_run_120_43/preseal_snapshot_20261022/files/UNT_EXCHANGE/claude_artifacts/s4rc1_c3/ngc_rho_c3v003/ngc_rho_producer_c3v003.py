"""NGC point rho producer c3v003 (Claude3 lane; root A136 G1-G4, FROM_CODEX/0698; NGC_RHO_INTERFACE_C3V001 42946e20;
CHANGES_C3V003).  The successor of ngc_rho_producer_c3v002 (9502e86d) by E1 (A167, FROM_CODEX/0741: the Binder binds the
spec route), E3 (W6: the NGC3198 refusal before realpath) and E5 (the *_C3V003 schemas) ONLY.  D9 (0730 V2) is c3v002's.

G1. The theta-bound successor of the rho part of certificates_ngc_k32/tools/lo_ngc_field_k64_c2v001.py (73636240)
    L45-59 and L76.  rho_rows() below is that part verbatim (each line is the base line, stripped; the base bytes and
    lines are re-read and checked at every run).  There is one change: the Binder B is bound at the point's S0 theta, with
    Eref = s*EB and ell = ell_F as qinf_eval_v001 (f58de0dc) L146-148 and, by E1 (A167, 0741), gam = s*(ge*EB): the SPEC
    ROUTE, the filler ec417e76 L294 order (spec.physical.gamma = ge*EB; the call runs at s*gamma), so the gamma the call
    runs at, as DDO.  The theta route (s*ge)*EB (qinf_eval L146-148; certs_common_c2v001 qinf_binder L219-220; Claude4
    s0theta_c4v001 bind() L131-139; the c3v002 binding) is recorded as a diagnostic only (A167 reverses 0717 R5 N1).
    The anchor Binder from qinf_binder() is kept
    only for the base's symbol-route check (repro_qinf_anchor bitwise, base L46-48; a1dcdea8 L80-82).  The B0 part of the
    base (roster, saved states, gamma file, I1-T, module build, field indicator) is not carried: rho does not use it.
G2. The registered settings behind LO_NGC_K32_CERT_V001 (07745bbf): coverage [2, 91]; the 9 shells (2,3] .. (64,91];
    the kept-cube cut K = 2 on the sampled path; sampled levels (1, 2) (52 dirs x 128/decade, 104 x 256/decade); the
    envelope search torus 12^3 x 200 hemisphere directions x {lo, sqrt(lo hi), hi}, 8 starts, refine defaults; ONE
    default_rng(20261018) stream across the shells in partition order; rho_used = max(sampled, envelope).  The partition
    and coverage are read from the certificate bytes and must equal these constants.  Only settings='registered'
    exists: any other settings value, any shell selection and any override is refused.
G3. Custody = driver cx3r008 (577f8c94) + the S0 theta key (S0_C2V001 1be5ed70) + the spec sha.  The spec's
    numerics.route_a.column_workers is inside identity and custody (until the identity pair is TESTED), so a record
    binds exactly one spec.  The spec's lo_certificate must be the launch pin LO_NGC_K32_CERT_V001 (A136).
G4. Decided by ngc_lo_slot_proof_c3v003: two records of this producer at the S0 seed, compared by wrapper v002's 10-key
    canonical comparison.  Only deterministic content is written inside those 10 keys.
D9. (root 0730 V2; Claude4 eps_ngc_point_c4v002 8972822b L27-32 item 8 and L548-562.)  The three D1(a) run inputs are
    verified from their bytes BEFORE the symbol route reads them and again AFTER the run: the A2 seed-scan
    CLAUDE2/runs/A2_SEED_SCAN_G2_RUN_V001/result.json (951580e2) and, in lwr_common 758740eb's RUN directory
    CLAUDE2/runs/NGC3198_ROUTE_A_A2F10_RUN_V001 (lwr_common L19-20), checkpoint/IDENTITY.json (7795015e, read at L48)
    and start.json (bbff6f25, read at L61).  The expected shas are Claude4's pins, held here as strings (pinload_c4v002
    b8ae4b06 L46-53, = root pin file c0390172 completed_run_inputs).  Each check reads each file once with O_NOFOLLOW_ANY
    (a symbolic link in any component is refused; this process stats nothing).  After the symbol route, lwr_common's IDENT
    and SEED must equal the verified IDENTITY ['identity'] and start ['seed']['numerical_inputs'] (Claude4 L548-549), and
    the verified seed-scan base Eref_J must be the bound EB bitwise (Claude4 L261-270).  A mismatch before the run refuses
    before the symbol route; a mismatch after the run refuses before the record is returned, so no record is written.
    The table is the registry's 'run_inputs': a SYNTHETIC_TEST registry carries synthetic fixture files only and is
    refused if it names a registered run input or a run tree.  The rho loop, the settings and the record's top-level keys
    are c3v001's (E1 changes the bound gamma and the theta_binding keys; E5 the schema strings).
E3. (W6.)  check_path refuses a path any of whose component strings contains 'ngc3198' (case-insensitive) BEFORE realpath,
    which lstats every component, so this process never stats an NGC3198-named path.  The D9 reads keep their own
    basename rule (lwr_common's two run inputs live inside the NGC3198-named run directory; those reads stat nothing).

Never: an import of certsngc_common_c2v002 or lo_ngc_field_k64_c2v001; a call of decisions(); a read of any file whose
name contains 'ngc3198' (case-insensitive); saved_states_v001.ngc_inputs(); any LO or per-state number.  The two
addenda appear only as root's pin strings (from LO_NGC_K32_CERT_V001 'decisions').
The registered symbol route (certs_common qinf_binder L205-215 -> the lwr_common_v001 import, L48 and L61) reads the A2
seed-scan result and lwr_common's two run inputs inside the NGC3198-named run directory named in D9, as Claude4's S0 EPS
does (D1(a); 0717 R1: root's run only; 0730 V1).  The builder never ran it and never opened those files; tests use a
synthetic symbol and synthetic run-input fixtures, refused at the registered S0 record, at any of its four keys and at
any registered run-input path.

Usage (root): taskpolicy -b python3 -I -B ngc_rho_producer_c3v003.py --spec-pin '{"path":..,"sha256":..}'
              --theta-key <64-hex> --out-root <existing dir> --out-name <name.json>
"""
import os

THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')
PARENT_THREAD_ENV = {_k: os.environ.get(_k) for _k in THREAD_ENV}
for _k in THREAD_ENV:                       # single-thread BLAS by override at import, before numpy can load
    os.environ[_k] = '1'

import datetime  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import resource  # noqa: E402
import struct  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
TSI = ART + '/tail_scheme_impl_c2'
NGCK = TSI + '/certificates_ngc_k32'

MODULES = (   # load order; executed from the exact hashed bytes under these sys.modules names
    ('certs_common_c2v001', TSI + '/certificates_v001/tools/certs_common_c2v001.py',
     '1946a394c0c36754c0fb9fbc39fb9e2243e042dfcab977c0d4c360313aa5ec99'),
    ('certs2_common_c2v002', TSI + '/certificates_v002/tools/certs2_common_c2v002.py',
     '8a42fbf34339392d60164bfd108a38b02d093b5bc5066522655b9e3705ff863b'),
    ('lo_cert_c2v001', TSI + '/certificates_v001/tools/lo_cert_c2v001.py',
     'd8a70a5e0b3c933147ac0a7c951c7c4d4f4ba0d442676a7bcfc36a96be2111c5'),
    ('lo_cert_c2v002', TSI + '/certificates_v002/tools/lo_cert_c2v002.py',
     '1ad8504e5d13af4b62c2d59aa30d603ba6f64e1662710169c41e645a2e4e8975'),
)
G1_BASE = {'path': NGCK + '/tools/lo_ngc_field_k64_c2v001.py',
           'sha256': '7363624099009cdb4abbdc7e7e1492879670f60c2a856662ab5b11cc16ab1b10'}
G1_BASE_LINES = (   # (base line number, exact stripped text); rho_rows() carries each of these lines verbatim
    (35, 'SHELLS = ((2, 3), (3, 4), (4, 6), (6, 8), (8, 12), (12, 16), (16, 32), (32, 64), (64, 91))'),
    (49, 'D = CC.direction_sets(L); E = C2.Envelope(L, B)'),
    (50, 'ev, V = np.linalg.eigh(np.asarray(Cb, float)); isq = (V / np.sqrt(ev)) @ V.T'),
    (51, 'rng = np.random.default_rng(20261018)'),
    (52, 'T12 = C2.torus_grid_v(12); Nt12 = E.native(T12); dirs200 = C2.fib_hemi(200); kref = 10.0 / L.KPC; '
         'Ed200 = E.eh_dir(dirs200, kref)'),
    (54, 'for lo, hi in SHELLS:'),
    (56, 'r = LO1.rho_shell(B, L, D, Cb, lo, hi, 2.0)'),
    (57, 're = LO2.rho_env_search(E, L, Nt12, T12, dirs200, Ed200, kref, isq, float(lo), float(hi), rng)'),
    (76, "rho_used = max(r['rho_G'], re['rho_G_envelope'])"),
)
CERT = {'path': NGCK + '/gates/LO_NGC_K32_CERT_V001.json',
        'sha256': '07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382'}
S0 = {'path': ART + '/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json',
      'sha256': '1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143'}
DRIVER = {'path': ART + '/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
          'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'}
S0_KEYS = ('968c915bece706ea1d6c0fa15357984884a87443e7c19eebd104230c9c961981',    # seed
           '3d7785669b549d6f9b9e0df65a3ad71de00c0da26a974c77ccb258856000fa60',    # jacobian_first_attempt_0
           'ab7bf95317b37652282ac7da86931816955ce8a781279b79e1d5258689c3970c',    # jacobian_first_attempt_1
           '4b9b4ec88eb2d94ce2c8eeb52e2f7c5b5b7f96bdb5d4df52b9077ba06401f6a2')    # jacobian_first_attempt_2
SEED_KEY = S0_KEYS[0]
SEED_SCAN_SHA = '951580e26aea5a0b4d0d2d73da7b1730effaac9444f385908e1ee4bb9778677d'   # Claude4 eps_ngc_point_c4v002 L84
LWR_COMMON_SHA = '758740ebf6caeb80876497674c3ee844f0ec8a9d0fae5d1fb8d491376e3aff48'  # a1dcdea8 L28; c4v002 L83
UPC_C2 = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
LWR_RUN_DIR = UPC_C2 + '/runs/NGC3198_ROUTE_A_A2F10_RUN_V001'      # lwr_common 758740eb L19-20 RUN: a name, never opened here
RUN_INPUT_ROLES = ('identity', 'start', 'seed_scan_result')
RUN_INPUTS = {   # D9 (0730 V2): the three D1(a) run inputs; Claude4 pinload_c4v002 (b8ae4b06) L46-53 = root pin file c0390172
    'identity': {'path': LWR_RUN_DIR + '/checkpoint/IDENTITY.json',                       # lwr_common L20, L48
                 'sha256': '7795015ee67b4712ff08fc5f41a5ae5ffcda4f850ed89de9f0dd70382af4d095'},
    'start': {'path': LWR_RUN_DIR + '/start.json',                                         # lwr_common L61
              'sha256': 'bbff6f2529bf9d743015912e5826097fac2f04fb4ad22c3a4b969835da0d8d61'},
    'seed_scan_result': {'path': UPC_C2 + '/runs/A2_SEED_SCAN_G2_RUN_V001/result.json',   # certs_common L41, L205, L215
                         'sha256': SEED_SCAN_SHA}}
D9_BEFORE = 'D9_RUN_INPUT_PIN_MISMATCH_BEFORE_SYMBOL_ROUTE (0730 V2)'
D9_AFTER = 'D9_RUN_INPUT_CHANGED_AFTER_RUN_NO_RECORD (0730 V2)'
ADDENDA_RECORDED_NOT_OPENED = {      # root's pins as strings (LO_NGC_K32_CERT_V001 'decisions'); never opened here
    'v005_open_sha256_at_read': '17cb4fd496845823227562682341eb605304d0ec14842d3e26369215e49d538b',
    'v004_frozen_sha256': '487d44498205e563c752e692b48bbb7288055591c72cfdcf5a75d849fef3d82b',
    'note': 'decisions() is never called; the NGC3198-named addenda are not opened (0708; A136 build brief).'}
SHELLS = ((2, 3), (3, 4), (4, 6), (6, 8), (8, 12), (12, 16), (16, 32), (32, 64), (64, 91))
PARTITION = [[float(a), float(b)] for a, b in SHELLS]
COVERAGE = [2.0, 91.0]
K_KEPT = 2.0
RNG_SEED = 20261018
SETTINGS = 'registered'
REGISTERED_SETTINGS = {
    'coverage_inverse_kpc': COVERAGE, 'partition': PARTITION,
    'top_shell': '(64,91]: rho on the complete spherical shell |k| in [64,91] (a superset of the B0 domain D cap {|k|>64} '
                 'of cylinder 64)',
    'kept_cube_cut': {'K_inverse_kpc': K_KEPT, 'rule': '|k|_inf * KPC > K (1 + 1e-12), sampled path only (lo_cert_c2v001 L56)'},
    'sampled': {'levels': [1, 2], 'directions': {'1': 52, '2': 104}, 'per_decade': {'1': 128, '2': 256}},
    'envelope': {'torus_m': 12, 'hemisphere_directions': 200, 'k_ref_inverse_kpc': 10.0, 'radii': 'lo, sqrt(lo hi), hi',
                 'n_starts': 8, 'refine': 'certs2_common_c2v002 refine defaults: M 48, max_it 120, tol 1e-7, grow 1.3'},
    'rng': {'scheme': 'ONE default_rng stream, consumed across the shells in partition order', 'seed': RNG_SEED},
    'rho_used': 'max(rho_G sampled, rho_G envelope)',
    'K_big_dependence': 'none (rho does not read K_big; B0 does)',
    'sources': {'certificate': 'LO_NGC_K32_CERT_V001 coverage_inverse_kpc, shells[*].range_inverse_kpc',
                'code': 'lo_ngc_field_k64_c2v001 L35, L49-57, L76; lo_cert_c2v001 L50-68; lo_cert_c2v002 L49-90; '
                        'certs2_common_c2v002 L170; certs_common_c2v001 L285-317'}}
SCHEMA = 'UNT_NGC_POINT_RHO_NUMERICAL_C3V003'
GATE = 'RHO_G'
VERDICT = 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED'
IDENTITY_SCHEMA = 'UNT_NGC_POINT_RHO_IDENTITY_C3V003'
CUSTODY_SCHEMA = 'UNT_NGC_POINT_RHO_CUSTODY_C3V003'
THETA_KEY_SCHEMA = 'DDO154_CALIBRATION_THETA_KEY_C2V001'      # fill_step5_c2v001 L38; orchestrator c2v005 L132
S0_SCHEMA, S0_MODULE = 'PHASE1_S0_C2V001', 'phase1_c2v001'
S0_ROLES = ('seed', 'jacobian_first_attempt_0', 'jacobian_first_attempt_1', 'jacobian_first_attempt_2')
BIND_KEYS = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'Eref_base_J')
GAMMA_ROUTE = ('SPEC_ROUTE s*(ge*EB): the filler ec417e76 L294 order (spec.physical.gamma = ge*EB; the call runs at '
               's*gamma), the gamma_eff the call runs at, as DDO (E1; A167, FROM_CODEX/0741); the theta route (s*ge)*EB '
               '(qinf_eval_v001 L146-148) is a diagnostic only')
TEMPLATE_LABEL_ID = 'A_K32_A2_HEADLINE'                        # template 68a19360 label_template_id (call and twin)
SPEC_GALAXY = 'NGC3198'                                        # the spec's galaxy value (template 68a19360)
K_BIG_PRODUCTION = 32.0
REGISTRY_REGISTERED, REGISTRY_SYNTHETIC = 'REGISTERED', 'SYNTHETIC_TEST'
SYMBOL_REGISTERED = 'REGISTERED_QINF_BINDER_THETA_BOUND_QINF_EVAL_L146_148'
SYMBOL_SYNTHETIC = 'SYNTHETIC_TEST_SYMBOL'
RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # wrapper v002 L177-178


class Refusal(Exception):
    """Fail-closed refusal with a stable code."""


def need(ok, code):
    if not ok:
        raise Refusal(code)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and is_sha(x['sha256'])


def hexf(x):
    return float(x).hex()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def real_registry():
    """The registered inputs (G3; D9 run inputs); a record from any other registry is marked SYNTHETIC_TEST in its custody."""
    return {'kind': REGISTRY_REGISTERED, 's0': dict(S0), 'driver': dict(DRIVER), 'launch': dict(CERT), 'cert': dict(CERT),
            'base': dict(G1_BASE), 'seed_key': SEED_KEY, 'run_inputs': {r: dict(RUN_INPUTS[r]) for r in RUN_INPUT_ROLES}}


def ngc3198_named(path):
    """E3 (W6): True when any component string of the path contains 'ngc3198' (case-insensitive); no filesystem call."""
    return any('ngc3198' in part.lower() for part in path.split('/'))


def check_path(path, label):
    need(isinstance(path, str) and os.path.isabs(path), label + ': PATH_NOT_ABSOLUTE')
    need(not ngc3198_named(path), label + ': NGC3198_NAMED_FILE_REFUSED (0708; any path component, before realpath)')
    need(os.path.realpath(path) == path, label + ': NONCANONICAL_PATH (symlink or relative component)')
    return path


def read_exact(ref, label):
    """Bytes of an exact {path, sha256} pin, hashed from the bytes read (no symlinks, no NGC3198-named file)."""
    need(is_pin(ref), label + ': NOT_AN_EXACT_PIN')
    check_path(ref['path'], label)
    fd = os.open(ref['path'], os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], label + ': BYTE_PIN_MISMATCH')
    return raw


def strict_json(raw, label):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, label + ': DUPLICATE_JSON_KEY ' + str(k))
            out[k] = v
        return out

    def bad(s):
        raise Refusal(label + ': NONFINITE_JSON_' + s)
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except ValueError as exc:
        raise Refusal(label + ': JSON_INVALID: ' + str(exc))


def self_pin():
    p = __file__
    need(isinstance(p, str) and os.path.isabs(p) and os.path.realpath(p) == p, 'NONCANONICAL_PRODUCER_FILE')
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def require_registered_settings(settings, shell_ranges, overrides):
    """G2: no smoke, no partial and no modified search can produce an NGC rho record."""
    need(type(settings) is str and settings == SETTINGS, 'NON_REGISTERED_SETTINGS_REFUSED: %r' % (settings,))
    need(shell_ranges is None, 'PARTIAL_SHELL_SELECTION_REFUSED (the full registered partition only)')
    need(overrides is None, 'SETTING_OVERRIDE_REFUSED: %r' % (overrides,))


def theta_key(theta):
    """fill_step5_c2v001 L97-102 / s0theta_c4v001 L41-46 (orchestrator c2v005 L523-529), verbatim logic."""
    th = {str(k): float(v) for k, v in theta.items()}
    need(all(math.isfinite(v) for v in th.values()), 'THETA_KEY_NONFINITE')
    return hashlib.sha256(canonical({'schema': THETA_KEY_SCHEMA, 'theta': th})).hexdigest()


def _number(x):
    return type(x) in (int, float) and math.isfinite(x)


def s0_point(raw, key):
    """The S0 point checks of Claude4 s0theta_c4v001 s0_point (L57-...), for ONE point; returns (point, theta)."""
    need(is_sha(key), 'THETA_KEY_NOT_64_HEX')
    doc = strict_json(raw, 'S0 record')
    need(isinstance(doc, dict) and doc.get('schema') == S0_SCHEMA and doc.get('module') == S0_MODULE, 'S0_SCHEMA_OR_MODULE')
    pts = doc.get('points')
    need(isinstance(pts, list) and len(pts) == 4 and all(isinstance(p, dict) for p in pts), 'S0_HAS_4_POINTS')
    need(sorted(p.get('role') for p in pts) == sorted(S0_ROLES), 'S0_ROLES')
    keys = [p.get('key') for p in pts]
    need(all(is_sha(k) for k in keys) and len(set(keys)) == 4, 'S0_KEYS_MALFORMED')
    hit = [p for p in pts if p.get('key') == key]
    need(len(hit) == 1, 'THETA_KEY_NOT_IN_S0_RECORD')
    p = hit[0]
    th_hex, th_nat, th_sh = p.get('theta_hex'), p.get('theta_natural'), p.get('theta_shared')
    need(isinstance(th_hex, dict) and isinstance(th_nat, dict) and isinstance(th_sh, dict) and set(th_hex) == set(th_nat),
         'S0_THETA_FORMS_MALFORMED')
    theta = {}
    for k, h in th_hex.items():
        n = th_nat[k]
        need(isinstance(h, str) and _number(n), 'S0_THETA_VALUE_MALFORMED ' + k)
        v = float.fromhex(h)
        need(hexf(v) == hexf(n), 'S0_THETA_HEX_NOT_NATURAL_BITWISE ' + k)
        theta[k] = v
    for k, v in th_sh.items():
        need(k in theta and _number(v) and hexf(v) == hexf(theta[k]), 'S0_THETA_SHARED_DISAGREES ' + k)
    for k in BIND_KEYS:
        need(k in theta and math.isfinite(theta[k]) and theta[k] > 0, 'S0_BIND_COORDINATE_INVALID ' + k)
    need(theta_key(theta) == key and theta_key(th_nat) == key, 'THETA_KEY_NOT_RECOMPUTED_FROM_BOTH_FORMS')
    return p, theta


def theta_bind(theta):
    """E1 (A167, FROM_CODEX/0741): Eref = s*EB and ell = ell_F as qinf_eval_v001 L146-148; gam = s*(ge*EB), the SPEC ROUTE
    (filler ec417e76 L294 order: spec.physical.gamma = ge*EB, then the call runs at s*gamma), the gamma the call runs at,
    as DDO.  The theta route (s*ge)*EB (qinf_eval L146-148; certs_common qinf_binder L219-220; s0theta_c4v001 bind
    L131-139; the c3v002 binding) is recorded as a diagnostic only: its value, its hex and its bitwise equality."""
    s, ge, ell, EB = (theta[k] for k in BIND_KEYS)
    Eeff = s * EB
    geff = s * (ge * EB)                                 # E1: the spec route, bound (the gamma_eff the call runs at)
    geff_theta = (s * ge) * EB                           # E1: the theta route, a diagnostic only
    out = {'s': s, 'gamma_over_Eref': ge, 'ell_F_m': ell, 'Eref_base_J': EB, 'Eref_eff_J': Eeff, 'gamma_eff': geff,
           'theta_route_gamma_eff': geff_theta}
    out['hex'] = {k: hexf(v) for k, v in out.items()}
    out['gamma_eff_route'] = GAMMA_ROUTE
    out['theta_route_gamma_eff_bits_equal'] = bool(out['hex']['theta_route_gamma_eff'] == out['hex']['gamma_eff'])
    return out


def check_spec(spec, key, theta, registry):
    """G3: the filled NGC call spec is this theta's call (filler ec417e76 L291-315); returns its custody fields."""
    need(isinstance(spec, dict), 'SPEC_NOT_AN_OBJECT')
    need(spec.get('galaxy') == SPEC_GALAXY, 'SPEC_GALAXY_MISMATCH')
    label = 'step5 %s theta_key=%s' % (TEMPLATE_LABEL_ID, key)
    need(spec.get('label') == label, 'SPEC_LABEL_THETA_KEY_MISMATCH')
    phys = spec.get('physical')
    need(isinstance(phys, dict), 'SPEC_PHYSICAL_MISSING')
    want = {'Eref_J': theta['Eref_base_J'], 'ell_F_m': theta['ell_F_m'],
            'gamma': theta['gamma_over_Eref'] * theta['Eref_base_J'],          # filler L294, same operation order
            'common_scale_s': theta['common_scale_s']}
    for k, v in want.items():
        need(_number(phys.get(k)) and hexf(phys[k]) == hexf(v), 'SPEC_PHYSICAL_NOT_THE_THETA_MAPPING ' + k)
    num = spec.get('numerics')
    need(isinstance(num, dict) and isinstance(num.get('uv_tail'), dict) and isinstance(num.get('route_a'), dict),
         'SPEC_NUMERICS_MALFORMED')
    uv = num['uv_tail']
    need(uv.get('lo_certificate') == registry['launch'], 'SPEC_LO_SLOT_IS_NOT_THE_LAUNCH_PIN (A136: LO_NGC_K32_CERT_V001)')
    outer = uv.get('outer')
    need(isinstance(outer, dict) and set(outer) == {'shape', 'K_big_inverse_kpc'} and outer['shape'] == 'cylinder'
         and _number(outer['K_big_inverse_kpc']) and float(outer['K_big_inverse_kpc']) == K_BIG_PRODUCTION,
         'SPEC_OUTER_NOT_PRODUCTION_CYLINDER_32')
    cw = num['route_a'].get('column_workers')
    need(type(cw) is int and cw >= 1, 'SPEC_ROUTE_A_COLUMN_WORKERS_INVALID')
    return {'label': label, 'column_workers': cw, 'lo_certificate': dict(uv['lo_certificate']),
            'physical_from_theta_hex': {k: hexf(v) for k, v in want.items()},
            'spec_route_gamma_eff_hex': hexf(phys['common_scale_s'] * phys['gamma'])}


def derive_point(spec_ref, theta_key_, registry):
    """G3 identity and custody of one NGC point (pure: no numpy, no symbol)."""
    need(isinstance(registry, dict) and registry.get('kind') in (REGISTRY_REGISTERED, REGISTRY_SYNTHETIC), 'REGISTRY_KIND')
    s0_ref = registry['s0']
    point, theta = s0_point(read_exact(s0_ref, 'S0 record'), theta_key_)
    spec_raw = read_exact(spec_ref, 'spec')
    spec = strict_json(spec_raw, 'spec')
    sc = check_spec(spec, theta_key_, theta, registry)
    read_exact(registry['driver'], 'driver cx3r008')
    read_exact(registry['launch'], 'launch pin LO_NGC_K32_CERT_V001')
    bind = theta_bind(theta)                     # E1 (A167): gamma_eff is the spec route; the theta route is a diagnostic
    need(sc['spec_route_gamma_eff_hex'] == bind['hex']['gamma_eff'],
         'BOUND_GAMMA_EFF_IS_NOT_THE_SPEC_ROUTE (E1, A167: s*(ge*EB) = spec.physical.common_scale_s * spec.physical.gamma)')
    identity = {'schema': IDENTITY_SCHEMA, 'theta_key': theta_key_, 's0_record_sha256': s0_ref['sha256'],
                'driver_sha256': registry['driver']['sha256'], 'spec_sha256': spec_ref['sha256'],
                'route_a_column_workers': sc['column_workers'],
                'theta_binding_hex': {k: bind['hex'][k] for k in ('s', 'gamma_over_Eref', 'ell_F_m', 'Eref_base_J')}}
    psha = digest(identity)
    custody = {'schema': CUSTODY_SCHEMA, 'registry_kind': registry['kind'],
               'symbol_route': SYMBOL_REGISTERED if registry['kind'] == REGISTRY_REGISTERED else SYMBOL_SYNTHETIC,
               'driver': dict(registry['driver']), 's0_record': dict(s0_ref), 'theta_key': theta_key_,
               'theta_role': point.get('role'), 'spec': dict(spec_ref), 'spec_label': sc['label'],
               'route_a_column_workers': sc['column_workers'], 'spec_lo_certificate': sc['lo_certificate'],
               'lo_certificate_launch_pin': dict(registry['launch']), 'spec_physical_from_theta_hex': sc['physical_from_theta_hex'],
               'settings_certificate': dict(registry['cert']), 'point_sha256': psha}
    return {'identity': identity, 'point_sha256': psha, 'custody': custody, 'custody_sha256': digest(custody),
            'bind': bind, 'theta_role': point.get('role'), 'spec': spec}


def verify_g1_base(registry):
    """The G1 base bytes and every transcribed line, re-read (the base is read as text, never imported)."""
    lines = read_exact(registry['base'], 'G1 base lo_ngc_field_k64_c2v001').decode('utf-8').splitlines()
    for n, text in G1_BASE_LINES:
        need(len(lines) >= n and lines[n - 1].strip() == text, 'G1_BASE_LINE_CHANGED L%d' % n)
    return {'base': dict(registry['base']), 'lines_verified': [n for n, _ in G1_BASE_LINES]}


def verify_certificate(registry):
    """G2: the partition and coverage are the certificate's registered fields, bitwise."""
    cert = strict_json(read_exact(registry['cert'], 'LO_NGC_K32_CERT_V001'), 'LO_NGC_K32_CERT_V001')
    need(cert.get('gate') == 'LO_NGC' and cert.get('verdict') == 'PASS', 'CERTIFICATE_GATE_OR_VERDICT')
    need(cert.get('coverage_inverse_kpc') == COVERAGE, 'CERTIFICATE_COVERAGE_NOT_2_TO_91')
    need([s.get('range_inverse_kpc') for s in cert.get('shells') or []] == PARTITION, 'CERTIFICATE_PARTITION_CHANGED')
    need(cert.get('production_K_big_inverse_kpc') == K_BIG_PRODUCTION, 'CERTIFICATE_PRODUCTION_K_BIG')
    return {'certificate': dict(registry['cert']), 'coverage_inverse_kpc': COVERAGE, 'partition': PARTITION,
            'production_K_big_inverse_kpc': K_BIG_PRODUCTION, 'n3_prime_K_big_inverse_kpc': cert.get('n3_prime_K_big_inverse_kpc')}


_MODS = {}


def load_registered_modules():
    """The four registered modules, executed from their exact hashed bytes (no NGC3198-named open at import time)."""
    if 'M' in _MODS:
        return _MODS['M']
    import numpy as np                      # after the thread override above
    out = {'np': np}
    for name, path, sha in MODULES:
        check_path(path, name)
        with open(path, 'rb') as f:
            raw = f.read()
        need(hashlib.sha256(raw).hexdigest() == sha, 'REGISTERED_MODULE_PIN_MISMATCH ' + name)
        prior = sys.modules.get(name)
        need(prior is None or getattr(prior, '__file__', None) == path, 'MODULE_NAME_TAKEN ' + name)
        if prior is None:
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            exec(compile(raw, path, 'exec'), mod.__dict__)
        out[name] = sys.modules[name]
    CC, C2 = out['certs_common_c2v001'], out['certs2_common_c2v002']
    LO1, LO2 = out['lo_cert_c2v001'], out['lo_cert_c2v002']
    need(C2.CC is CC and LO1.CC is CC and LO2.C2 is C2 and LO2.LO1 is LO1 and LO2.PIN_LO1 == MODULES[2][2],
         'REGISTERED_MODULE_CHAIN')
    out.update(CC=CC, C2=C2, LO1=LO1, LO2=LO2,
               pins=[{'name': n, 'path': p, 'sha256': s} for n, p, s in MODULES])
    _MODS['M'] = out
    return out


def read_run_inputs(registry):
    """D9: the bytes of the three D1(a) run inputs of the registry's table, each read once with O_NOFOLLOW_ANY (the kernel
    refuses a symbolic link in any component; this process stats nothing), as Claude4 pinload_c4v002 L165-178."""
    table = registry.get('run_inputs')
    need(isinstance(table, dict) and set(table) == set(RUN_INPUT_ROLES) and all(is_pin(table[r]) for r in RUN_INPUT_ROLES),
         'D9_RUN_INPUT_TABLE_MALFORMED')
    flag = getattr(os, 'O_NOFOLLOW_ANY', None)
    need(flag is not None, 'D9_O_NOFOLLOW_ANY_UNAVAILABLE')
    out = {}
    for r in RUN_INPUT_ROLES:
        p = table[r]['path']
        need(os.path.isabs(p) and 'ngc3198' not in os.path.basename(p).lower(), 'D9_RUN_INPUT_PATH_REFUSED ' + r)
        try:
            fd = os.open(p, os.O_RDONLY | getattr(os, 'O_CLOEXEC', 0) | flag)
            try:
                chunks = []
                while True:
                    c = os.read(fd, 1 << 20)
                    if not c:
                        break
                    chunks.append(c)
            finally:
                os.close(fd)
        except OSError as exc:
            raise Refusal('D9_RUN_INPUT_UNREADABLE %s (%s: %s)' % (r, type(exc).__name__, exc))
        out[r] = b''.join(chunks)
    return out


def check_run_input_pins(registry, raw, code):
    """D9: sha256 of exactly the bytes read, against the table's pins (code: D9_BEFORE or D9_AFTER)."""
    for r in RUN_INPUT_ROLES:
        need(hashlib.sha256(raw[r]).hexdigest() == registry['run_inputs'][r]['sha256'],
             '%s: %s %s' % (code, r, registry['run_inputs'][r]['path']))


def same_json(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)           # Claude4 eps_ngc_point_c4v002 L206-207


def check_run_input_parse(L, bind, raw):
    """D9: the symbol route parsed exactly the verified bytes (Claude4 L548-549: lwr_common IDENT = IDENTITY['identity'] and
    SEED = start['seed']['numerical_inputs']; L261-270: the seed-scan base Eref_J is the bound EB, bitwise)."""
    try:
        ident, start, scan = (json.loads(raw[r]) for r in RUN_INPUT_ROLES)
    except ValueError as exc:
        raise Refusal('D9_RUN_INPUT_NOT_JSON: ' + str(exc))
    need(isinstance(ident, dict) and 'identity' in ident and hasattr(L, 'IDENT') and same_json(L.IDENT, ident['identity']),
         'D9_LWR_COMMON_IDENT_IS_NOT_THE_VERIFIED_IDENTITY')
    seed = start.get('seed') if isinstance(start, dict) else None
    need(isinstance(seed, dict) and 'numerical_inputs' in seed and hasattr(L, 'SEED')
         and same_json(L.SEED, seed['numerical_inputs']), 'D9_LWR_COMMON_SEED_IS_NOT_THE_VERIFIED_START')
    base = scan.get('base') if isinstance(scan, dict) else None
    eb = base.get('Eref_J') if isinstance(base, dict) else None
    need(_number(eb) and hexf(eb) == bind['hex']['Eref_base_J'], 'D9_SEED_SCAN_EB_IS_NOT_THE_BOUND_EB')


def synthetic_run_inputs_ok(table):
    """D9: a SYNTHETIC_TEST registry names synthetic fixture files only (never a registered run input or a run tree)."""
    prod = {v[k] for v in RUN_INPUTS.values() for k in ('path', 'sha256')}
    return (isinstance(table, dict) and set(table) == set(RUN_INPUT_ROLES) and all(is_pin(table[r]) for r in RUN_INPUT_ROLES)
            and all(table[r]['path'] not in prod and table[r]['sha256'] not in prod and '/runs/' not in table[r]['path'].lower()
                    and 'ngc3198' not in table[r]['path'].lower() for r in RUN_INPUT_ROLES))


def registered_symbol(bind, M):
    """certs_common qinf_binder (A2 grid, grid check, anchor) + repro_qinf_anchor (base L45-48); then the point Binder at
    theta (Eref and ell as qinf_eval L146-148; gam the spec route, E1).  Reads the D1(a) run-tree inputs inside
    qinf_binder: root's run only (NEED R1)."""
    CC = M['CC']
    L, A, info, (g, Cb, mu) = CC.qinf_binder()
    pins = info['pins']
    need(pins['seed_scan_result']['sha256'] == SEED_SCAN_SHA, 'SEED_SCAN_RESULT_SHA_AT_READ')
    need(pins['lwr_common']['sha256'] == LWR_COMMON_SHA, 'LWR_COMMON_SHA_AT_READ')
    rep = CC.repro_qinf_anchor(L, A)
    need(rep['bitwise_equal'] is True and rep['gamma_equal'] is True, 'QINF_ANCHOR_REPRODUCTION_FAILED')
    EB = L.ANCHOR_UNSCALED['Eref_J']          # = the seed-scan base Eref_J (qinf_binder L216-217)
    need(hexf(EB) == bind['hex']['Eref_base_J'], 'S0_EREF_BASE_IS_NOT_THE_SEED_SCAN_EB')
    B = L.Binder(g, Cb, mu, Eref=bind['Eref_eff_J'], ell=bind['ell_F_m'], gam=bind['gamma_eff'])
    np = M['np']
    return L, B, Cb, {'route': SYMBOL_REGISTERED, 'pins': pins, 'grid_check': info['grid_check'],
                      'grid_array_sha256': info['grid_array_sha256'],
                      'Cbar_sha256': hashlib.sha256(np.ascontiguousarray(np.asarray(Cb, float)).tobytes()).hexdigest(),
                      'anchor_reproduction': {'bitwise_equal': rep['bitwise_equal'], 'gamma_equal': rep['gamma_equal'],
                                              'max_rel_diff': rep['max_rel_diff']}}


def rho_rows(L, B, Cb, M, progress=None):
    """lo_ngc_field_k64_c2v001 L49-59 and L76, verbatim, on the theta Binder B (G1).  Returns the shell rows."""
    np, CC, C2, LO1, LO2 = M['np'], M['CC'], M['C2'], M['LO1'], M['LO2']
    SHELLS = ((2, 3), (3, 4), (4, 6), (6, 8), (8, 12), (12, 16), (16, 32), (32, 64), (64, 91))
    D = CC.direction_sets(L); E = C2.Envelope(L, B)
    ev, V = np.linalg.eigh(np.asarray(Cb, float)); isq = (V / np.sqrt(ev)) @ V.T
    rng = np.random.default_rng(20261018)
    T12 = C2.torus_grid_v(12); Nt12 = E.native(T12); dirs200 = C2.fib_hemi(200); kref = 10.0 / L.KPC; Ed200 = E.eh_dir(dirs200, kref)
    rows = []
    for lo, hi in SHELLS:
        ts = time.monotonic()
        r = LO1.rho_shell(B, L, D, Cb, lo, hi, 2.0)
        re = LO2.rho_env_search(E, L, Nt12, T12, dirs200, Ed200, kref, isq, float(lo), float(hi), rng)
        rho_used = max(r['rho_G'], re['rho_G_envelope'])
        need(_number(rho_used) and rho_used >= 0, 'RHO_NONFINITE_OR_NEGATIVE (%g,%g]' % (lo, hi))
        rows.append({'range_inverse_kpc': [float(lo), float(hi)], 'rho_used': float(rho_used),
                     'rho_G_sampled': float(r['rho_G']), 'rho_G_envelope': float(re['rho_G_envelope']),
                     'rho_V_sampled': float(r['rho_V']), 'rho_levels': r['levels'], 'rho_envelope_search': re,
                     'domain': ('complete spherical shell [%g,%g] /kpc; sampled points with |k|_inf > 2 (kept cube K = 2)'
                                % (lo, hi))})
        if progress:
            progress({'shell': [float(lo), float(hi)], 'shell_seconds': round(time.monotonic() - ts, 3)})
    return rows


def produce(spec_ref, theta_key_, *, settings='registered', shell_ranges=None, overrides=None, registry=None,
            symbol=None, progress=None):
    """One NGC point rho record.  Registered registry => registered symbol; a SYNTHETIC_TEST registry needs a test
    symbol and is refused at the registered S0 record and at any of its four keys (no real theta).  D9: the three run inputs
    are verified from bytes before the symbol route and after the run."""
    t0 = time.monotonic()
    require_registered_settings(settings, shell_ranges, overrides)
    need(sys.flags.optimize == 0, 'OPTIMIZE_FLAG_REFUSED (asserts of the registered modules must run)')
    reg = real_registry() if registry is None else registry
    need(isinstance(reg, dict) and reg.get('kind') in (REGISTRY_REGISTERED, REGISTRY_SYNTHETIC), 'REGISTRY_KIND')
    if reg['kind'] == REGISTRY_REGISTERED:
        need(reg == real_registry(), 'REGISTRY_IS_NOT_THE_REGISTERED_ONE')
        need(symbol is None, 'TEST_SYMBOL_REFUSED_AT_REGISTERED_INPUTS')
    else:
        need(symbol is not None, 'SYNTHETIC_REGISTRY_NEEDS_A_TEST_SYMBOL')
        need(reg['s0'] != S0 and reg['s0']['sha256'] != S0['sha256'] and theta_key_ not in S0_KEYS,
             'TEST_SYMBOL_AT_A_REAL_THETA_REFUSED (0688/A136: synthetic thetas only)')
        need(synthetic_run_inputs_ok(reg.get('run_inputs')),
             'SYNTHETIC_RUN_INPUT_TABLE_REFUSED (D9: three exact pins to synthetic fixture files; never a registered run input '
             'or a run tree)')
    base = verify_g1_base(reg)
    cert = verify_certificate(reg)
    pt = derive_point(spec_ref, theta_key_, reg)
    M = load_registered_modules()
    M['CC'].require_env()
    run_raw = read_run_inputs(reg)                       # D9 (0730 V2): BEFORE the symbol route reads them
    check_run_input_pins(reg, run_raw, D9_BEFORE)
    if reg['kind'] == REGISTRY_REGISTERED:
        L, B, Cb, sym = registered_symbol(pt['bind'], M)
    else:
        L, B, Cb, sym = symbol(pt['bind'], M)
        need(isinstance(sym, dict) and sym.get('route') == SYMBOL_SYNTHETIC, 'TEST_SYMBOL_ROUTE_LABEL')
    b = pt['bind']
    need(B.Eref == b['Eref_eff_J'] and B.ell == b['ell_F_m'] and B.gam == b['gamma_eff'], 'BINDER_DOES_NOT_CARRY_THE_BOUND_THETA')
    check_run_input_parse(L, b, run_raw)                 # D9: the symbol route parsed the verified bytes
    rows = rho_rows(L, B, Cb, M, progress)
    need([r['range_inverse_kpc'] for r in rows] == PARTITION, 'PARTITION_NOT_COMPLETE')
    check_run_input_pins(reg, read_run_inputs(reg), D9_AFTER)    # D9: AFTER the run; a mismatch returns no record
    rec = {'schema': SCHEMA, 'gate': GATE, 'status': 'TESTED', 'verdict': VERDICT,
           'identity': pt['identity'], 'point_sha256': pt['point_sha256'], 'custody': pt['custody'],
           'settings': SETTINGS, 'coverage_complete': True, 'required_coverage_inverse_kpc': list(COVERAGE),
           'full_registered_search_executed': True, 'shells': rows,
           # ---- outside wrapper v002's 10 compared keys
           'custody_sha256': pt['custody_sha256'], 'registered_settings': REGISTERED_SETTINGS,
           'theta_binding': b, 'symbol': sym, 'g1_base_transcription': base, 'certificate_settings': cert,
           'producer': self_pin(), 'modules': M['pins'], 'decisions_recorded_not_opened': ADDENDA_RECORDED_NOT_OPENED,
           'rigorous_supremum': False, 'production_admissible': False, 'lo_certified': False,
           'label': 'TESTED numerical estimate: rho is a sampled / locally maximized sup, not a proven sup; review required',
           'limitation': ('Binds no slot by itself: ngc_lo_slot_proof_c3v003 binds a ROOT-REGISTERED record, after the seed '
                          'pair (G4).  No LO or per-state number is computed here (post-run acceptance only, A136 G5).'),
           'utc': utc(), 'seconds': round(time.monotonic() - t0, 3), 'pid': os.getpid(),
           'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           'thread_env': {k: os.environ.get(k) for k in THREAD_ENV}, 'thread_env_parent': dict(PARENT_THREAD_ENV)}
    return rec


def encode_record(rec):
    return (json.dumps(rec, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')


def write_record(rec, out_root, name):
    """Exclusive create of one record directly inside out_root (an existing canonical directory)."""
    check_path(out_root, 'out-root')
    need(os.path.isdir(out_root), 'OUT_ROOT_NOT_A_DIRECTORY')
    need(isinstance(name, str) and name == os.path.basename(name) and name.endswith('.json') and not name.startswith('.'),
         'OUT_NAME_INVALID')
    path = os.path.join(out_root, name)
    raw = encode_record(rec)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}


def background_qos():
    try:
        return os.getpriority(4, 0) == 1           # PRIO_DARWIN_PROCESS: 1 under taskpolicy -b
    except Exception:
        return False


def main(argv=None):
    if not background_qos():
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        return 2
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B, no -O)', flush=True)
        return 2
    import argparse
    ap = argparse.ArgumentParser(description='NGC point rho producer c3v003 (registered settings only)')
    ap.add_argument('--spec-pin', required=True)
    ap.add_argument('--theta-key', required=True)
    ap.add_argument('--out-root', required=True)
    ap.add_argument('--out-name', required=True)
    a = ap.parse_args(argv)
    try:
        rec = produce(json.loads(a.spec_pin), a.theta_key,
                      progress=lambda x: print(json.dumps(dict(x, utc=utc())), flush=True))
        pin = write_record(rec, a.out_root, a.out_name)
    except (Refusal, ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'verdict': 'REFUSED', 'blocker': type(exc).__name__ + ': ' + str(exc)}), flush=True)
        return 3
    print(json.dumps({'verdict': rec['verdict'], 'record': pin}), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
