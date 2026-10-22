"""Claude4 S0 build_c4v001: the per-point NGC EPS successor.  S0 POINT EPS CERTIFICATE NUMERICS (root A133 S0 certificates; A135
item 2 "EPS: each S0 point's own record, from Claude4's S0 successor, with rule (b) per 0693"; 0689, 0694, 0695 item 3).
Successor of eps_ngc_point_c4v001.py (79a5ac1d).  Implements Claude3 0184 items 1-8 and 10-12 (REVIEW_RI45_06_RESULT_C3V001
e6bcca96) and root 0693 rule (b); runs only inside fence_c4v004 (item 9), through tools/run_fenced_c4st4.py.

What runs.  The EPS procedure of certificates_ngc_k32/tools/eps_ngc91_c2v001.py main() (2e59a461, the producer of the anchor record
EPS_NGC91_SAMPLES_V001 ce26ced9), TRANSCRIBED in run_eps() below (each line cites the author line it reproduces) with only the
point-scoped changes, calling only the author's functions, loaded from verified bytes (the c4v001 chain, the same 7 pins):
eps_cert_c2v002.certify (the registered rule), eps_cert_c2v004.dense_eps (10000-direction audit), eps_cert_c2v005.env_search /
actual_search, certs2_common.Envelope and its grids, certs_common.direction_sets / q_of / require_env.  The author's main() is not
called: it binds the anchor (qinf_binder: point 'anchor_F10' from lwr_common ANCHOR_UNSCALED) and exits at any other point (L50-52).
Changes from the author's main(), against Claude3 0184:
  item 1   the theta is bound explicitly from a pinned record: point_binder() = certs_common qinf_binder's A2-grid loading and A2
           grid check (L205-214) + qinf_eval_v001 L146-148: B = L.Binder(g, Cb, mu, Eref=s*EB, ell=ell_F, gam=s*ge*EB), EB = the
           seed-scan base Eref_J (951580e2).  lwr_common's EREF/ELL/GAM and ANCHOR_UNSCALED never enter B; no point literal.  An S0
           record's Eref_base_J must equal EB bitwise; B must carry exactly the bound values.
  item 2   no anchor comparison is run: repro_qinf_anchor, the V006 reproduction fields, the TAIL_REANCHOR identity and the
           ce26ced9 / 1d5eef1b comparisons are reported NOT_APPLICABLE; EPS_CERT_V006, QINF_EVAL_V001.json and TAIL_REANCHOR are
           not read.
  items 3-4  the anchor-only inputs (EPS_CERT_K128_V004 node maxima; EPS_SUP_SUPP check own sup) are not read: actual_vals =
           [eps_base, eps_refined, dense audit, local max] on every shell, so on the C1 shells {2,3,4,5,6,8,12,16,32}
           eps_actual_set, eps, envelope_over_actual and envelope_dominates_actual come from point values only;
           eps_node_maxima_from_V004 and eps_check_own_sup are null and disclosed; no substitute is computed.
  item 5 + 0693  shells (2,5]: eps = max(envelope, actual-set max) (rule (b)); the 'converged: CHECK F1' label is gone.
  item 6   eps_source = the argmax of max(envelope, actual) on every shell ('envelope' on a tie, as max() returns the first); the
           domination flag and the minimum envelope/actual ratio (all shells; lo >= 5) are reported.
  item 7   unchanged: the 89 unit shells (2,91] and the 15 AUDIT_SHELLS, read from the verified eps_ngc91_c2v001 module; the
           registered CERTIFIED rule (certify's flags); default_rng(20261018) consumed in V005 order, the 2000-node envelope
           self-test first; the A2 grid check; single-thread env (certs_common.require_env, NUMEXPR_NUM_THREADS included).
  item 8   custody sandwich: root pin file c0390172; the 3 run inputs (read with O_NOFOLLOW_ANY) and the 25 modules sha-checked
           from bytes before AND after the run; the binder's seed-scan sha-at-read must be 951580e2 and lwr_common's 758740eb;
           lwr_common IDENT/SEED must equal the verified IDENTITY/start bytes; fence_c4v004's pin table must equal the pin file.
  item 10  the STEP2 watch read is optional (pinload_c4v002.step2_watch_rows never raises).
  item 11  GQ is written by tools/gq_binding_c4v002.py (be148bab re-binding, open item carried).
  item 12  no LO, rho or per-state number: no LO module is loaded and none is written.
Every record carries the label, the rule-(b) statement, the theta binding, the theta record pin and the 0182 scope correction.
Field use: shells[i].lo_inverse_kpc / hi_inverse_kpc / eps are the per-shell certificate values (what the tail module's
field_bound reads); shells[i].rule_registered is eps_cert_c2v002.certify's own dict (its 'eps' is the rule's max(base, refined)).

Modes (exactly one):
  point  --s0-record PATH --s0-sha256 HEX --point-key HEX [--bind-check 1]   S0 POINT EPS CERTIFICATE NUMERICS
         --bind-check 1 stops after the custody preflight and the theta binding (no EPS numerics; not a certificate).
  smoke  --smoke-anchor 1 [--smoke-n-hi N] [--smoke-audit a,b | none]         SMOKE (never a certificate)
         theta from the evaluator block of the anchor record EPS_NGC91_SAMPLES_V001 (ce26ced9); shells (2,3] .. (N-1,N],
         contiguous from 2 (the rng stream is then the full run's for those shells); audits a subset of AUDIT_SHELLS below N.
Usage (from the build folder):
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 taskpolicy -b \\
  <python3> -I -B tools/run_fenced_c4st4.py tools/eps_ngc_point_c4v002.py <sha256 of this file> --run-id <alnum> <mode args>"""
import ast
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import sys
import time
import traceback

T_WALL0 = time.time()
T0 = time.perf_counter()
C0 = time.process_time()
TOOLS = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(TOOLS)
PINLOAD = (os.path.join(TOOLS, 'pinload_c4v002.py'), 'b8ae4b06802b563848f6de6b2d349d5e806574b9661026614937cda4fb685067')
S0THETA = (os.path.join(TOOLS, 's0theta_c4v001.py'), '950d774a794d50315857cb1fcc901d829f9136cc60e78d45ecbc9117dfa7fd3a')
FENCE = (os.path.join(TOOLS, 'fence_c4v004.py'), 'b5a6aa0951f46c78acfd46c2626f3aa97e0bd063835c7770e2ed5ea56c562d29')
RUNNER = (os.path.join(TOOLS, 'run_fenced_c4st4.py'), '9327b0b5d37b24fbf89ff97ecd8af94d6f61b696de5cd90b6c0c6e403de72a10')
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
UPC = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
TSI = ART + '/tail_scheme_impl_c2'
NGCK = TSI + '/certificates_ngc_k32'
V1T = TSI + '/certificates_v001/tools'
V2T = TSI + '/certificates_v002/tools'
CHAIN = (  # (import name, path, sha256), in load order (each one's project imports are already in sys.modules); = c4v001
    ('certs_common_c2v001', V1T + '/certs_common_c2v001.py', '1946a394c0c36754c0fb9fbc39fb9e2243e042dfcab977c0d4c360313aa5ec99'),
    ('certs2_common_c2v002', V2T + '/certs2_common_c2v002.py', '8a42fbf34339392d60164bfd108a38b02d093b5bc5066522655b9e3705ff863b'),
    ('certsngc_common_c2v001', NGCK + '/tools/certsngc_common_c2v001.py', 'ee68e83cd2c77277ce19eb1a4de4a5b6ea84fdda5ddb631c02ef17f1ae0b35d5'),
    ('eps_cert_c2v002', V1T + '/eps_cert_c2v002.py', 'e41548099df88f3622892e0342597482d8e3df5b4230a0b87e600286071ef62a'),
    ('eps_cert_c2v004', V1T + '/eps_cert_c2v004.py', 'c62f2e6eb25ff06c8da4bfd91f99833ff57c92b6d9c01bff89c32b47857f1162'),
    ('eps_cert_c2v005', V2T + '/eps_cert_c2v005.py', '3c20fd514dded6d4fcb44ecd5d0d230c8728a12b2025b307bcbcf112dcf2b709'),
    ('eps_ngc91_c2v001', NGCK + '/tools/eps_ngc91_c2v001.py', '2e59a46195a7a94593f53eefc57828f0ce598d4b40458eec343693f2f967d033'),
)
LWR_COMMON = (ART + '/long_wavelength_response_c2/tools/lwr_common_v001.py', '758740ebf6caeb80876497674c3ee844f0ec8a9d0fae5d1fb8d491376e3aff48')
SEED_SCAN_SHA = '951580e26aea5a0b4d0d2d73da7b1730effaac9444f385908e1ee4bb9778677d'
DATA = (  # every other file the EPS route reads, verified before the run (the author's own pin checks re-read them)
    ('qinf_eval_v001 (the evaluator whose binding L146-148 is transcribed)', ART + '/qinf_dependence_c2/tools/qinf_eval_v001.py',
     'f58de0dcc67cc4097b4604dc96b640fbf8aaee0520d0478e214673b931eb3346'),
    ('GRID_INVENTORY_V001', ART + '/long_wavelength_response_c2/out/GRID_INVENTORY_V001.npz',
     '1833cca4b27edafde5e1d27f511b5bc7843f5447eb4d0faebbdeeb98b790d20d'),
    ('CANDIDATE_4CHAIN_POOLED_GRID_V001', UPC + '/CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
     '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'),
)
ANCHOR_SAMPLES = (NGCK + '/out/EPS_NGC91_SAMPLES_V001.json', 'ce26ced9d3e864fa158e8f38bd20d83eea1d5e7de1533c3633354fa99571c1a5')
CERTS_R5 = (ART + '/calib_tail_readiness_cx2/certificates_per_point/certs_common_r5_cx2v001.py',
            'c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7')
NOT_READ = (  # anchor-only or anchor-comparison files the c4v001 producer read and this successor does not (0184 items 2-4)
    ('EPS_CERT_V006 (V006 reproduction fields)', TSI + '/certificates_v002/gates/EPS_CERT_V006.json', '598c8fa3'),
    ('EPS_CERT_V004 (V004 record)', TSI + '/certificates_v001/gates/EPS_CERT_V004.json', 'de0dcefd'),
    ('EPS_CERT_K128_V004 (V004 node maxima)', TSI + '/certificates_v001/gates/EPS_CERT_K128_V004.json', '260d5503'),
    ('EPS_SUP_SUPP (certificates_v001 check own sup)', TSI + '/certificates_v001/check/out/EPS_SUP_SUPP.json', '0ddec5a7'),
    ('QINF_EVAL_V001.json (repro_qinf_anchor)', ART + '/qinf_dependence_c2/out/QINF_EVAL_V001.json', '50aab701'),
    ('TAIL_REANCHOR (anchor identity)', ART + '/step4_launch_readiness_c4/dryplans/specs_v001/specs/TAIL_REANCHOR.json', '5fc6f0bd'),
    ('EPS_CERT_NGC91_V001 (anchor gate comparison)', NGCK + '/gates/EPS_CERT_NGC91_V001.json', '1d5eef1b'),
    ('EPS_NGC91_SAMPLES_V001 (anchor samples comparison; read in SMOKE mode only, as the theta source)', ANCHOR_SAMPLES[0], 'ce26ced9'),
)
AUDIT_EXPECTED = (2, 3, 4, 5, 6, 8, 12, 16, 19, 32, 45, 63, 64, 80, 90)
C1_SHELLS = (2, 3, 4, 5, 6, 8, 12, 16, 32)
SCHEMA = 'UNT_CLAUDE4_S0_POINT_EPS_C4V002'
RULE_B = ("Root 0693 rule (b) (Claude2, 2026-10-19 12:11Z; A135 item 2): on the shells (2,5] -- (2,3], (3,4], (4,5] -- eps = "
          "max(envelope, actual-set max).  The anchor's converged-actual rule for lo < 5 (eps_cert_c2v005 docstring L19-21: CHECK F1 own "
          "sup / record 1.0005, 0.9995, 1.0011, anchor values) is anchor evidence and is not carried to a point.  It is the reading less "
          "favourable to a pass (at the anchor 8.2025e-4 on (2,3] against an actual 6.4230e-4).  On lo >= 5 the rule is unchanged: eps = "
          "max(envelope, actual-set max) (the envelope dominates the actual set by construction; the max guards the search).  "
          "eps_source names the argmax ('envelope' on a tie).")
RULE_LT5 = '(2,5]: rule (b), root 0693: eps = max(envelope, actual-set max); the anchor CHECK F1 convergence basis is not carried over'
RULE_GE5 = 'lo >= 5: eps = max(envelope, actual-set max) (V005 rule; the envelope dominates by construction, the max guards the search)'
SCOPE_0182 = ("Erratum of record (Claude4 0182; root 0693): the anchor-only EPS inputs are not confined to lo < 5 (the c4v001 POINT_NOTE (ii) "
              "'lo < 5' scope was wrong and stays only in those exclusive-create copies).  The V004 node maxima (DDO_C4R3_cache_7b9816ae, "
              "NGC_T120L_stored_operator) sit on shells (2,3]..(6,7]; the certificates_v001 check's own sup (EPS_SUP_SUPP 0ddec5a7) on "
              "(3,4], (4,5], (5,6], (6,7], (8,9], (12,13], (16,17], (32,33]: the C1 shells {2,3,4,5,6,8,12,16,32}.  Here both are removed "
              "from the actual set on every shell, and eps_actual_set, eps, envelope_over_actual and envelope_dominates_actual are "
              "recomputed from point values only.  The node maxima are |1-q| of stored anchor-state operator and cache responses "
              "(eps_cert_c2v004 node_shell_eps L43-53) and cannot be recomputed at a theta: dropped (null), no substitute.  The check's "
              "own sup could be recomputed only by running that independent check's sup method at the point binding; not done: dropped (null).")
THETA_ROUTE = ("qinf_eval_v001 (f58de0dc) L146-148: Eeff = s*EB; geff = s*ge*EB; B = L.Binder(g, Cb, mu, Eref=Eeff, ell=ell, gam=geff); "
               "(g, Cb, mu) = the A2 pooled grid of GRID_INVENTORY_V001 (1833cca4), checked bitwise against CANDIDATE_4CHAIN_POOLED_GRID_V001 "
               "(2e3a36d8) as certs_common qinf_binder L208-214; EB = the A2_SEED_SCAN_G2 base Eref_J (951580e2); s = common_scale_s, "
               "ge = gamma_over_Eref, ell = ell_F_m, bit for bit from the pinned record (theta_hex).  lwr_common's EREF/ELL/GAM (from "
               "start.json) and ANCHOR_UNSCALED never enter B: all three Binder arguments are explicit.  An S0 record's Eref_base_J must "
               "equal EB bitwise.")
NO_LO = ('No LO, rho or per-state acceptance number is computed, read or written (0679, A134 hold); EPS certificate numerics only '
         '(0681, 0689, 0693, A135 item 2).')
REGISTRATION = ('Not a registered slot record: A132 D3 (registration) is deferred until registration; root pins the per-point record '
                '(A135 item 2: certificate_pins_by_point {theta key: {eps_certificate}}).')


def hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def bootstrap(path_sha, name):
    with open(path_sha[0], 'rb') as f:
        b = f.read()
    if hashlib.sha256(b).hexdigest() != path_sha[1]:
        raise SystemExit('%s pin mismatch' % name)
    m = importlib.util.module_from_spec(importlib.machinery.ModuleSpec(name, None, origin=path_sha[0]))
    m.__file__ = path_sha[0]
    sys.modules[name] = m
    exec(compile(b, path_sha[0], 'exec', dont_inherit=True), m.__dict__)
    return m


def args():
    a = sys.argv[1:]
    allowed = ('--run-id', '--s0-record', '--s0-sha256', '--point-key', '--bind-check', '--smoke-anchor', '--smoke-n-hi',
               '--smoke-audit')
    if len(a) % 2:
        raise SystemExit('arguments come in pairs')
    out = {}
    for i in range(0, len(a), 2):
        if a[i] not in allowed:
            raise SystemExit('unknown argument ' + a[i])
        if a[i] in out:
            raise SystemExit('repeated argument ' + a[i])
        out[a[i]] = a[i + 1]
    run_id = out.get('--run-id')
    if not run_id or not run_id.isascii() or not run_id.isalnum():
        raise SystemExit('--run-id <alnum> required')
    point = any(k in out for k in ('--s0-record', '--s0-sha256', '--point-key', '--bind-check'))
    smoke = any(k in out for k in ('--smoke-anchor', '--smoke-n-hi', '--smoke-audit'))
    if point == smoke:
        raise SystemExit('exactly one mode: point (--s0-record P --s0-sha256 H --point-key K [--bind-check 1]) or smoke '
                         '(--smoke-anchor 1 [--smoke-n-hi N] [--smoke-audit a,b|none])')
    if point:
        for k in ('--s0-record', '--s0-sha256', '--point-key'):
            if k not in out:
                raise SystemExit('point mode needs %s (no anchor default exists)' % k)
        for k in ('--s0-sha256', '--point-key'):
            if not hex64(out[k]):
                raise SystemExit('%s must be 64 lowercase hex' % k)
        if not out['--s0-record'].startswith('/'):
            raise SystemExit('--s0-record must be an absolute path')
        if out.get('--bind-check', '0') not in ('0', '1'):
            raise SystemExit('--bind-check 0|1')
        return dict(mode='point', run_id=run_id, s0_record=out['--s0-record'], s0_sha=out['--s0-sha256'],
                    point_key=out['--point-key'], bind_check=out.get('--bind-check') == '1')
    if out.get('--smoke-anchor') != '1':
        raise SystemExit('smoke mode needs --smoke-anchor 1')
    nh = out.get('--smoke-n-hi', '9')
    if not nh.isdigit():
        raise SystemExit('--smoke-n-hi N (an integer)')
    au = out.get('--smoke-audit', '2')
    if au == 'none':
        aud = ()
    else:
        if not all(x.isdigit() for x in au.split(',')):
            raise SystemExit('--smoke-audit a,b,... | none')
        aud = tuple(int(x) for x in au.split(','))
    return dict(mode='smoke', run_id=run_id, n_hi=int(nh), audits=aud, bind_check=False)


def jnorm(x):
    return json.loads(json.dumps(x, allow_nan=False))


def same(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def py_strings(x, acc):
    if isinstance(x, dict):
        for v in x.values():
            py_strings(v, acc)
    elif isinstance(x, list):
        for v in x:
            py_strings(v, acc)
    elif isinstance(x, str) and x.endswith('.py'):
        acc.add(x)
    return acc


def seg(src, fname):
    for node in ast.parse(src).body:
        if isinstance(node, ast.FunctionDef) and node.name == fname:
            return ast.get_source_segment(src, node)
    return None


def pin_entries(src):
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'PINS':
            d = node.value
            return {ast.literal_eval(k): ast.get_source_segment(src, v) for k, v in zip(d.keys, d.values)
                    if ast.literal_eval(k) in ('seed_scan_result', 'lwr_common')}
    return None


def tcall(fn, *a, **k):
    t1 = time.perf_counter()
    c1 = time.process_time()
    r = fn(*a, **k)
    return r, [round(time.perf_counter() - t1, 3), round(time.process_time() - c1, 3)]


def point_binder(P, S, CC, np, TH, mode):
    """certs_common qinf_binder (L203-224) with the anchor point replaced by the pinned theta (qinf_eval_v001 L146-148)."""
    pins = {k: CC.pin(k) for k in ('qinf_evaluator', 'inventory_npz', 'A2_npz', 'seed_scan_result', 'lwr_common')}  # qinf_binder L205
    if pins['seed_scan_result']['sha256'] != SEED_SCAN_SHA or pins['lwr_common']['sha256'] != LWR_COMMON[1]:
        raise SystemExit('binder sha-at-read: seed scan %s (want 951580e2), lwr_common %s (want 758740eb)' % (
            pins['seed_scan_result']['sha256'][:8], pins['lwr_common']['sha256'][:8]))
    sys.path.insert(0, str(CC.LWR / 'tools'))                                                         # L206
    L = CC.load_module(CC.PINS['lwr_common'][0], 'lwr_common')                                       # L207 (S3: verified bytes)
    inv = np.load(CC.PINS['inventory_npz'][0])                                                        # L208
    g = inv['A2_pooled__grid']; Cb = inv['A2_pooled__Cbar']; mu = inv['A2_pooled__mubar']            # L209
    with np.load(CC.PINS['A2_npz'][0]) as z:                                                          # L210-211
        sg, sC, smu = z['source_hessian_grid'].copy(), z['background_C'].copy(), z['background_mu'].copy()
    grid_check = dict(grid_equal_pinned_source=bool(np.array_equal(g, sg)),                          # L212 (A2 grid check)
                      background_equal_pinned_source=bool(np.array_equal(Cb, sC) and np.array_equal(mu, smu)))
    if not all(grid_check.values()):                                                                  # L213-214
        raise SystemExit('A2 grid/background not equal to pinned source')
    scan = json.loads(P.read_verified(str(CC.PINS['seed_scan_result'][0]), SEED_SCAN_SHA, 'seed scan result (binder EB)',
                                      nofollow_any=True))
    EB = scan['base']['Eref_J']                                                                       # L216 / qinf_eval L85
    bound = S.bind(TH['eps_theta'], EB)                                                               # qinf_eval L147
    checks = {}
    if mode == 'point':
        checks['record_Eref_base_J_equals_seed_scan_EB'] = bool(float(TH['eps_theta']['Eref_base_J']).hex() == float(EB).hex())
        if not checks['record_Eref_base_J_equals_seed_scan_EB']:
            raise SystemExit('S0 record Eref_base_J %r is not the seed-scan base Eref_J %r: binding refused' % (
                TH['eps_theta']['Eref_base_J'], EB))
    else:
        exp = TH['expected_bound']
        checks['smoke_Eref_eff_equals_anchor_record'] = bool(bound['Eref_eff_J'].hex() == float(exp['Eref_eff_J']).hex())
        checks['smoke_gamma_eff_equals_anchor_record'] = bool(bound['gamma_eff'].hex() == float(exp['gamma_eff']).hex())
        if not all(checks.values()):
            raise SystemExit('SMOKE: the anchor record evaluator is not reproduced by the binding: %r' % checks)
    B = L.Binder(g, Cb, mu, Eref=bound['Eref_eff_J'], ell=bound['ell_F_m'], gam=bound['gamma_eff'])   # qinf_eval L148
    checks['binder_carries_bound_values'] = bool(B.Eref == bound['Eref_eff_J'] and B.ell == bound['ell_F_m'] and
                                                 B.gam == bound['gamma_eff'])
    if not checks['binder_carries_bound_values']:
        raise SystemExit('Binder does not carry the bound values')
    s0 = L.ANCHOR_UNSCALED['common_scale_s']; ge0 = L.ANCHOR_UNSCALED['gamma'] / EB; ell0 = L.ANCHOR_UNSCALED['ell_F_m']
    vs_anchor = dict(
        note=('information only: the anchor of lwr_common ANCHOR_UNSCALED is NOT used to bind; this records whether the bound theta '
              'happens to equal it bit for bit'),
        s_equal=bool(bound['s'] == s0), gamma_over_Eref_equal=bool(bound['gamma_over_Eref'] == ge0), ell_F_equal=bool(bound['ell_F_m'] == ell0),
        rel_diff=dict(s=abs(bound['s'] - s0) / s0, gamma_over_Eref=abs(bound['gamma_over_Eref'] - ge0) / ge0,
                      ell_F_m=abs(bound['ell_F_m'] - ell0) / ell0),
        seed_scan_base_equals_lwr_anchor_constants=bool(EB == L.ANCHOR_UNSCALED['Eref_J'] and scan['base']['ell_F_m'] == ell0),
        lwr_module_defaults_not_passed=dict(EREF=L.EREF, ELL=L.ELL, GAM=L.GAM,
                                            note='Binder received Eref, ell, gam explicitly (qinf_eval L148); values may coincide at the anchor'))
    info = dict(pins=pins, grid_check=grid_check, theta_source=TH['source'], point=TH['point'].get('role'),
                point_key=TH['point'].get('key'), s=bound['s'], gamma_over_Eref=bound['gamma_over_Eref'], ell_F_m=bound['ell_F_m'],
                Eref_base_J=EB, Eref_eff_J=bound['Eref_eff_J'], gamma_eff=bound['gamma_eff'], hex=bound['hex'], checks=checks,
                theta_vs_lwr_anchor=vs_anchor, route=THETA_ROUTE,
                grid_array_sha256=hashlib.sha256(np.ascontiguousarray(g).tobytes()).hexdigest(), Cbar=Cb.tolist(), mubar=mu.tolist())
    return L, B, info


def run_eps(np, CC, C2, E2, E4, E5, L, B, n_lo, n_hi, audits, PHASE):
    """eps_ngc91_c2v001 main() L43-111, transcribed; the changes are marked CHANGE."""
    CC.require_env()                                                                                  # L43
    for p, want in ((C2.V001_TOOLS / 'eps_cert_c2v002.py', E5.PIN_E2), (C2.V001_TOOLS / 'eps_cert_c2v004.py', E5.PIN_E4)):  # L44
        if CC.sha(p) != want:                                                                         # L45
            raise SystemExit('pin ' + str(p))                                                         # L46
    # CHANGE L47-52: no V006 record, no qinf_binder anchor, no repro_qinf_anchor (B is the point binder's)
    ts0 = time.perf_counter()
    E = C2.Envelope(L, B)                                                                             # L53
    rng = np.random.default_rng(20261018)                                                            # L54
    kv = rng.standard_normal((2000, 3)); kv /= np.linalg.norm(kv, axis=1)[:, None]; kv *= rng.uniform(2, 363, (2000, 1)) / L.KPC  # L55
    selftest = dict(n=2000, bitwise_equal=bool(np.array_equal(E.q(kv, E.t_of(kv)), CC.q_of(B, kv))))     # L56
    if not selftest['bitwise_equal']:                                                                 # L57
        raise SystemExit('envelope self-test failed')                                                 # L58
    print('self-test', selftest, flush=True)                                                          # L59
    D = CC.direction_sets(L)                                                                          # L60
    dense2 = E4.fib_sphere(2000); dense = np.concatenate([dense2, E4.fib_sphere(8000)])               # L61
    # CHANGE L62-66: the V004 records and EPS_SUP_SUPP are anchor-only inputs and are not read (0184 items 3-4)
    T12 = C2.torus_grid_v(12); Nt12 = E.native(T12)                                                   # L67
    dirs200 = C2.fib_hemi(200); kref = 10.0 / L.KPC; Ed200 = E.eh_dir(dirs200, kref)                   # L68
    setup = dict(wall_s=round(time.perf_counter() - ts0, 3))
    shells = []; prev = None                                                                          # L69
    for n in range(n_lo, n_hi):                                                                       # L70
        PHASE[0] = 'shell %d' % n
        lo, hi = float(n), float(n + 1); ts = time.time(); tcp = time.process_time()                  # L71
        s, t_cert = tcall(E2.certify, B, L, D, lo, hi)                                                # L72
        da, t_dense = tcall(E4.dense_eps, B, L, lo, hi, dense)                                        # L73 (L74 not applied: s stays certify's dict)
        env, t_env = tcall(E5.env_search, E, L, Nt12, T12, dirs200, Ed200, kref, lo, hi, rng, extra=prev)  # L75
        prev = dict(t=env['t_at'], dir=env['dir_at'], k=env['k_at_inverse_kpc'] + 1.0)               # L76
        seeds = [dict(dir=da['dir_at_max'], k=da['k_at_max_inverse_kpc'])] + [dict(dir=v['dir_at_max'], k=v['k_at_max_inverse_kpc']) for v in s['levels'].values()]  # L77
        act, t_act = tcall(E5.actual_search, B, L, lo, hi, dense2, rng, seeds)                        # L78
        # CHANGE L79-83: point values only (no V004 node maxima, no check own sup)
        members = dict(eps_base=s['eps_base'], eps_refined=s['eps_refined'], eps_dense_audit=da['eps'],
                       eps_actual_local_max=act['eps_actual_local_max'])
        actual_vals = [members[k] for k in ('eps_base', 'eps_refined', 'eps_dense_audit', 'eps_actual_local_max')]
        eps_actual = float(max(actual_vals))                                                          # L84
        amax = [k for k in ('eps_base', 'eps_refined', 'eps_dense_audit', 'eps_actual_local_max') if members[k] == eps_actual][0]
        # CHANGE L85-88: every shell eps = max(envelope, actual) (rule (b) on (2,5], 0693); eps_source = the argmax
        eps = float(max(env['eps_envelope'], eps_actual))                                             # L86
        src = 'envelope' if env['eps_envelope'] >= eps_actual else 'actual_set_max'
        flat = dict(eps_base=s['eps_base'], eps_refined=s['eps_refined'], refinements=s['refinements'], eps=eps, eps_source=src,  # L89-91
                    eps_envelope=env['eps_envelope'], eps_actual_set=eps_actual, eps_actual_local_max=act['eps_actual_local_max'],
                    eps_dense_audit=da['eps'], eps_check_own_sup=None, envelope_over_actual=env['eps_envelope'] / eps_actual)
        shells.append(dict(
            range_inverse_kpc=s['range_inverse_kpc'], lo_inverse_kpc=s['lo_inverse_kpc'], hi_inverse_kpc=s['hi_inverse_kpc'],
            eps=eps, eps_source=src, eps_rule=RULE_LT5 if lo < 5.0 else RULE_GE5, eps_actual_argmax=amax, flat=flat,
            rule_registered=s, dense_audit=da, envelope=env, actual_local=act, actual_set_members=members,
            eps_node_maxima_from_V004=None, eps_check_own_sup=None, c1_shell=bool(n in C1_SHELLS),                # L96 CHANGE
            envelope_dominates_actual=bool(env['eps_envelope'] >= eps_actual * (1 - 1e-12)),                     # L97
            envelope_over_actual=env['eps_envelope'] / eps_actual,
            seconds=round(time.time() - ts, 2), cpu_seconds=round(time.process_time() - tcp, 3),                 # L98
            timing=dict(certify=t_cert, dense_eps=t_dense, env_search=t_env, actual_search=t_act)))
        print('(%d,%d] rule %.4e/%.4e r%d dense %.4e act %.4e env %.4e eps %.4e [%s] %.1fs' % (                 # L100-102
            n, n + 1, s['eps_base'], s['eps_refined'], s['refinements'], da['eps'], act['eps_actual_local_max'], env['eps_envelope'],
            eps, src[:8], shells[-1]['seconds']), flush=True)
    PHASE[0] = 'audit setup'
    ta0 = time.perf_counter()
    audit = []
    if audits:
        T20 = C2.torus_grid_v(20); Nt20 = E.native(T20); dirs400 = C2.fib_hemi(400); Ed400 = E.eh_dir(dirs400, kref)  # L103
    setup['audit_setup_wall_s'] = round(time.perf_counter() - ta0, 3)
    for n in audits:                                                                                  # L105
        PHASE[0] = 'audit %d' % n
        lo, hi = float(n), float(n + 1)                                                               # L106
        a, t_a = tcall(E5.env_search, E, L, Nt20, T20, dirs400, Ed400, kref, lo, hi, rng, n_starts=16,
                       ks_frac=(0.0, 0.25, 0.5, 0.75, 1.0))                                           # L107
        prod = shells[n - n_lo]['envelope']['eps_envelope']                                           # L108
        audit.append(dict(shell=[lo, hi], production=prod, dense=a['eps_envelope'], dense_over_production=a['eps_envelope'] / prod,
                          dense_t_at=a['t_at'], dense_dir_at=a['dir_at'], dense_k_at=a['k_at_inverse_kpc'], dense_grid_max=a['grid_max'],
                          timing=t_a))                                                                # L109-110
        print('audit (%d,%d] prod %.6e dense %.6e ratio %.8f' % (n, n + 1, prod, a['eps_envelope'], a['eps_envelope'] / prod), flush=True)
    return selftest, shells, audit, setup


def summarize(shells, audit, n_lo, n_hi):
    best = max(shells, key=lambda x: x['eps'])
    ge5 = [x for x in shells if x['lo_inverse_kpc'] >= 5.0]
    lt5 = [x for x in shells if x['lo_inverse_kpc'] < 5.0]
    r_all = min(shells, key=lambda x: x['envelope_over_actual'])
    r_ge5 = min(ge5, key=lambda x: x['envelope_over_actual']) if ge5 else None
    certified = all(x['rule_registered']['certified'] for x in shells)
    ok_rule = all(x['rule_registered']['refinements'] <= 1 and x['rule_registered']['eps_refined'] <= 1.1 * x['rule_registered']['eps_base']
                  for x in shells)
    src = {}
    for x in shells:
        src[x['eps_source']] = src.get(x['eps_source'], 0) + 1
    return dict(
        coverage_inverse_kpc=[float(n_lo), float(n_hi)], n_shells=len(shells),
        rule_verdict='CERTIFIED' if certified else 'EPS_UNCERTIFIED',
        rule_note='the registered rule alone decides: CERTIFIED iff every shell has refinements <= 1 (eps_cert_c2v002 certify flags L55)',
        rule_flags_agree_with_v005_form=bool(certified == ok_rule),
        eps_max=best['eps'], eps_max_shell=best['range_inverse_kpc'], eps_max_source=best['eps_source'],
        eps_max_envelope=max(x['flat']['eps_envelope'] for x in shells),
        eps_max_actual_set=max(x['flat']['eps_actual_set'] for x in shells),
        eps_source_counts=src,
        rule_b_shells=[dict(shell=x['range_inverse_kpc'], eps=x['eps'], eps_envelope=x['flat']['eps_envelope'],
                            eps_actual_set=x['flat']['eps_actual_set'], eps_source=x['eps_source']) for x in lt5],
        envelope_dominates_actual_every_shell=bool(all(x['envelope_dominates_actual'] for x in shells)),
        shells_actual_above_envelope=[x['range_inverse_kpc'] for x in shells if not x['envelope_dominates_actual']],
        min_envelope_over_actual=dict(value=r_all['envelope_over_actual'], shell=r_all['range_inverse_kpc']),
        min_envelope_over_actual_lo_ge_5=(dict(value=r_ge5['envelope_over_actual'], shell=r_ge5['range_inverse_kpc']) if r_ge5 else None),
        refinements_used=[x['range_inverse_kpc'] for x in shells if x['rule_registered']['refinements']],
        envelope_audit=(dict(shells=[a['shell'] for a in audit], max_dense_over_production=max(a['dense_over_production'] for a in audit),
                             min_dense_over_production=min(a['dense_over_production'] for a in audit)) if audit else None))


def main():
    A = args()
    F = sys.modules.get('fence_c4v004')
    if F is None or getattr(F, 'FENCE_VERSION', None) != 'fence_c4v004':
        raise SystemExit('run only under tools/run_fenced_c4st4.py (fence_c4v004 is not installed)')
    if not sys.pycache_prefix or os.path.exists(sys.pycache_prefix):
        raise SystemExit('sys.pycache_prefix must be set by the runner to an absent path')
    P = bootstrap(PINLOAD, 'pinload_c4v002')
    P.T0 = T0   # one time origin for the guard log, the sampler and the timing
    P.install_guard()
    S = P.load_verified_module(S0THETA[0], S0THETA[1], 's0theta_c4v001', 's0theta_c4v001')
    P.read_verified(FENCE[0], FENCE[1], 'fence_c4v004 (as pinned by this producer)')
    P.read_verified(RUNNER[0], RUNNER[1], 'run_fenced_c4st4 (as pinned by this producer)')
    PHASE = ['verify_pins']
    sampler = P.Sampler(PHASE, period=10.0)
    r_start = P.rusage()
    sampler.take()
    sampler.start()
    timebase = P.mach_timebase()
    rid = A['run_id']
    if A['mode'] == 'smoke':
        base = 'SMOKE_ANCHOR_POINT_EPS_C4V002_%s' % rid
        label = ('SMOKE TEST at the ANCHOR theta (code path of the S0 POINT EPS successor; shells (2,%d] only): NOT a certificate, '
                 'NOT an S0 point, never to be pinned' % A['n_hi'])
    elif A['bind_check']:
        base = 'BIND_CHECK_S0_%s_C4V002_%s' % (A['point_key'][:16], rid)
        label = 'BIND CHECK (S0 point theta binding and custody only): no EPS numerics, NOT a certificate'
    else:
        base = 'S0_POINT_EPS_%s_C4V002_%s' % (A['point_key'][:16], rid)
        label = 'S0 POINT EPS CERTIFICATE NUMERICS'
    STOP = 'out/%s_RUN_STOP.json' % base
    HDR = dict(label=label, registration=REGISTRATION, rule_b=RULE_B, theta_binding=dict(route=THETA_ROUTE),
               theta_record_pin=None, scope_corrections_0182=SCOPE_0182, no_lo_rho_per_state=NO_LO)
    TIM = {}
    try:
        step2_start = P.step2_watch_rows(3)                       # optional (0184 item 10)
        # ---- theta source: the pinned record, bytes checked before any parse
        if A['mode'] == 'point':
            raw = P.read_verified(A['s0_record'], A['s0_sha'], 'S0 record (theta source)')
            TH = S.s0_point(raw, A['s0_record'], A['s0_sha'], A['point_key'])
        else:
            raw = P.read_verified(ANCHOR_SAMPLES[0], ANCHOR_SAMPLES[1], 'anchor EPS samples (SMOKE theta source)')
            TH = S.anchor_smoke_theta(raw, ANCHOR_SAMPLES[0], ANCHOR_SAMPLES[1])
        HDR['theta_record_pin'] = dict(TH['record'], point_key=TH['point'].get('key'), point_role=TH['point'].get('role'))
        HDR['theta_binding']['theta_from_record'] = dict(TH['eps_theta'], hex={k: (None if v is None else float(v).hex())
                                                                               for k, v in TH['eps_theta'].items()})
        # ---- custody (pre): root pin file, fence/loader tables, 3 run inputs, 25 modules, lwr_common, data
        rawpin = P.read_verified(P.ROOT_PIN_FILE[0], P.ROOT_PIN_FILE[1], 'root_pin_file')
        pins = json.loads(rawpin)
        rin = {r['path']: r['sha256'] for r in pins['completed_run_inputs']}
        tables = dict(root_pin_file_equals_fence=bool(rin == F.PINNED_RUN_INPUTS), root_pin_file_equals_loader=bool(rin == P.RUN_INPUTS),
                      fence_root_pin_file=list(F.ROOT_PIN_FILE) == list(P.ROOT_PIN_FILE))
        if not all(tables.values()):
            raise SystemExit('run-input tables differ: %r' % tables)
        runb = {p: P.read_verified(p, sh, 'root_pinned_run_input', nofollow_any=True) for p, sh in rin.items()}
        root25 = [(m['path'], m['sha256']) for m in pins['modules_named_in_identity']]
        if len(root25) != 25 or len(set(root25)) != 25:
            raise SystemExit('the root pin file does not list 25 modules')
        for p, sh in root25:
            P.read_verified(p, sh, 'root_pinned_module')
        P.read_verified(LWR_COMMON[0], LWR_COMMON[1], 'lwr_common_v001 (root-cited 758740eb)')
        for name, path, sha in DATA:
            P.read_verified(path, sha, name)
        ident_all = json.loads(runb[P.RUN_INPUT_PATHS[0]])
        idpy = py_strings(ident_all, set())
        identity_names = dict(n_py_paths_named_anywhere_in_identity=len(idpy),
                              root25_all_named_in_identity=bool(all(p in idpy for p, _ in root25)),
                              named_in_identity_not_in_root25=sorted(p for p in idpy if p not in {q for q, _ in root25}))
        # ---- A132 D1(a) names certs_common_r5 (c75aaa5a) as the import path; this route reads through certs_common_c2v001
        # (1946a394, the record's chain).  Their run-input readers are compared from source (ast; nothing executed).
        c1src = P.read_verified(CHAIN[0][1], CHAIN[0][2], 'certs_common_c2v001 (reader comparison)').decode()
        r5src = P.read_verified(CERTS_R5[0], CERTS_R5[1], 'certs_common_r5_cx2v001 (reader comparison)').decode()
        reader_identity = {('%s_source_identical' % f): bool(seg(c1src, f) is not None and seg(c1src, f) == seg(r5src, f))
                           for f in ('pin', 'sha', 'load_module', 'qinf_binder')}
        reader_identity['PINS_seed_scan_and_lwr_common_identical'] = bool(pin_entries(c1src) == pin_entries(r5src) and
                                                                          pin_entries(c1src) is not None)
        n_pre = len(P.VERIFIED)
        start_doc = dict(schema=SCHEMA + '_RUN_START', **HDR, mode=A['mode'], bind_check=A['bind_check'], run_id=rid, utc=P.utc(),
                         pid=os.getpid(), nice=os.getpriority(os.PRIO_PROCESS, 0), argv=sys.argv, python=sys.version,
                         flags=dict(isolated=sys.flags.isolated, dont_write_bytecode=sys.flags.dont_write_bytecode),
                         pycache_prefix=sys.pycache_prefix,
                         thread_env={k: os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                                                                    'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')},
                         tables=tables, verified_pre=list(P.VERIFIED), identity_names=identity_names, reader_identity=reader_identity,
                         step2_watch_at_start=step2_start, rusage_at_start=r_start, mach_timebase=timebase)
        P.write_new_json('out/%s_RUN_START.json' % base, start_doc)
        # ---- imports: numpy, then the author chain from verified bytes
        PHASE[0] = 'import'
        ti = time.perf_counter()
        import numpy as np
        TIM['numpy_import_s'] = round(time.perf_counter() - ti, 3)
        mods = {}
        for name, path, sha in CHAIN:
            mods[name] = P.load_verified_module(path, sha, name, 'chain:' + name)
        TIM['chain_import_s'] = round(time.perf_counter() - ti - TIM['numpy_import_s'], 3)
        CC = mods['certs_common_c2v001']; C2 = mods['certs2_common_c2v002']; N = mods['certsngc_common_c2v001']
        E2 = mods['eps_cert_c2v002']; E4 = mods['eps_cert_c2v004']; E5 = mods['eps_cert_c2v005']; TOOL = mods['eps_ngc91_c2v001']
        if not (TOOL.N is N and TOOL.CC is CC and TOOL.C2 is C2 and TOOL.E5 is E5 and TOOL.E2 is E2 and TOOL.E4 is E4
                and N.C2 is C2 and C2.CC is CC and E5.C2 is C2 and E5.E2 is E2 and E5.E4 is E4 and E4.E2 is E2 and E2.CC is CC):
            raise SystemExit('the chain did not bind to the verified modules')
        n_lo, n_hi_full, audit_full = TOOL.N_LO, TOOL.N_HI, tuple(TOOL.AUDIT_SHELLS)
        if (n_lo, n_hi_full, audit_full) != (2, 91, AUDIT_EXPECTED):
            raise SystemExit('the verified eps_ngc91_c2v001 shells/audits are not (2, 91, the 15 audit shells)')
        if A['mode'] == 'smoke':
            n_hi = A['n_hi']
            audits = A['audits']
            if not (n_lo < n_hi <= n_hi_full) or any(a not in audit_full or not (n_lo <= a < n_hi) for a in audits):
                raise SystemExit('smoke shells must be (2,N] with 3 <= N <= 91 and audits a subset of AUDIT_SHELLS below N')
        else:
            n_hi, audits = n_hi_full, audit_full
        # ---- S3 (as c4v001, but an exact-string check, no realpath): lwr_common only, from its verified bytes
        LOADED = {}

        def s3_load_module(path, name, want=None):
            if str(path) != LWR_COMMON[0] or (want is not None and want != LWR_COMMON[1]):
                raise SystemExit('S3: load_module of a path outside this run\'s pin table: %s' % path)
            m = P.load_verified_module(str(path), LWR_COMMON[1], 'certs_' + name, 'S3:' + name)
            LOADED[name] = m
            return m
        CC.load_module = s3_load_module
        # ---- the point binding (item 1)
        PHASE[0] = 'bind'
        tb = time.perf_counter()
        L, B, info = point_binder(P, S, CC, np, TH, A['mode'])
        TIM['bind_s'] = round(time.perf_counter() - tb, 3)
        HDR['theta_binding'].update(bound=dict(s=info['s'], gamma_over_Eref=info['gamma_over_Eref'], ell_F_m=info['ell_F_m'],
                                               Eref_base_J=info['Eref_base_J'], Eref_eff_J=info['Eref_eff_J'],
                                               gamma_eff=info['gamma_eff'], hex=info['hex']), checks=info['checks'])
        selftest = shells = audit = setup = None
        if not A['bind_check']:
            PHASE[0] = 'eps'
            tm = time.perf_counter(); cm = time.process_time()
            selftest, shells, audit, setup = run_eps(np, CC, C2, E2, E4, E5, L, B, n_lo, n_hi, audits, PHASE)
            TIM['eps_wall_s'] = round(time.perf_counter() - tm, 3); TIM['eps_cpu_s'] = round(time.process_time() - cm, 3)
            TIM['eps_setup'] = setup
        PHASE[0] = 'custody_post'
        r_end_eps = P.rusage()
        # ---- custody (post): lwr_common parsed exactly the verified bytes; run inputs and 25 modules re-read and re-checked
        Lm = LOADED['lwr_common']
        ident_b = json.loads(runb[P.RUN_INPUT_PATHS[0]])
        start_b = json.loads(runb[P.RUN_INPUT_PATHS[1]])
        root25s = set(root25)
        lwr_parse = dict(IDENT_equals_verified_identity=bool(same(Lm.IDENT, ident_b['identity'])),
                         SEED_equals_verified_start_seed=bool(same(Lm.SEED, start_b['seed']['numerical_inputs'])),
                         ANCHOR_CHECK=Lm.ANCHOR_CHECK,
                         modules_loaded={n: dict(path=Lm.MODS[n]['path'], sha256=Lm.MODS[n]['sha256'],
                                                 in_root_pin_file=bool((Lm.MODS[n]['path'], Lm.MODS[n]['sha256']) in root25s))
                                         for n in ('fourier_arguments.cardinal_module', 'fourier_arguments.complex_binding_module',
                                                   'fourier_arguments.static_binding_module')},
                         checkpoint_module=dict(path=str(Lm.CKMOD), sha256=Lm.CKMOD_SHA,
                                                in_root_pin_file=bool((str(Lm.CKMOD), Lm.CKMOD_SHA) in root25s)))
        for p, sh in rin.items():
            P.read_verified(p, sh, 'post_run_recheck_run_input', nofollow_any=True)
        for p, sh in root25:
            P.read_verified(p, sh, 'post_run_recheck_module')
        P.read_verified(LWR_COMMON[0], LWR_COMMON[1], 'post_run_recheck_lwr_common')
        lwr_ok = (lwr_parse['IDENT_equals_verified_identity'] and lwr_parse['SEED_equals_verified_start_seed'] and
                  all(v['in_root_pin_file'] for v in lwr_parse['modules_loaded'].values()) and lwr_parse['checkpoint_module']['in_root_pin_file'])
        G = P.guard_report()
        runtree_opens = [o for o in G['opened_outside_build'] if o['cls'] == 'root_pinned_run_input']
        custody = dict(
            root_pin_file=dict(path=P.ROOT_PIN_FILE[0], sha256=P.ROOT_PIN_FILE[1]), tables=tables,
            pre_run_verified_ok=bool(all(v['ok'] for v in P.VERIFIED[:n_pre])), n_pre_run_verified=n_pre,
            post_run_verified_ok=bool(all(v['ok'] for v in P.VERIFIED[n_pre:])), n_post_run_and_run_verified=len(P.VERIFIED) - n_pre,
            run_inputs_read_nofollow_any=bool(all(v['nofollow_any'] for v in P.VERIFIED if v['path'] in rin)),
            binder_seed_scan_sha_at_read=info['pins']['seed_scan_result']['sha256'],
            binder_seed_scan_is_951580e2=bool(info['pins']['seed_scan_result']['sha256'] == SEED_SCAN_SHA),
            binder_lwr_common_sha_at_read=info['pins']['lwr_common']['sha256'],
            lwr_common_parse=lwr_parse, lwr_common_parse_ok=bool(lwr_ok),
            run_tree_opens=[dict(given=o['given'], count=o['count'], write=o['write']) for o in runtree_opens],
            run_tree_opens_only_the_pins_read_only=bool(all(o['given'] in rin and not o['write'] for o in runtree_opens)),
            guard_refused=len(G['refused']), fence_blocked_during_script=len(G['fence_blocked_during_script']),
            identity_names=identity_names, reader_identity=reader_identity)
        if not (custody['pre_run_verified_ok'] and custody['post_run_verified_ok'] and lwr_ok and custody['binder_seed_scan_is_951580e2']
                and custody['run_tree_opens_only_the_pins_read_only']):
            raise SystemExit('custody sandwich failed: %r' % {k: custody[k] for k in ('pre_run_verified_ok', 'post_run_verified_ok',
                                                                                         'lwr_common_parse_ok', 'binder_seed_scan_is_951580e2')})
        prod = dict(path=os.path.abspath(__file__), sha256=hashlib.sha256(_SELF_BYTES[0]).hexdigest() if _SELF_BYTES else None)
        build_pins = dict(pinload_c4v002=dict(path=PINLOAD[0], sha256=PINLOAD[1]), s0theta_c4v001=dict(path=S0THETA[0], sha256=S0THETA[1]),
                          fence_c4v004=dict(path=FENCE[0], sha256=FENCE[1]), run_fenced_c4st4=dict(path=RUNNER[0], sha256=RUNNER[1]))
        chain = {name: dict(path=path, sha256=sha) for name, path, sha in CHAIN}
        not_applicable = dict(
            status='NOT_APPLICABLE at a point (Claude3 0184 item 2)',
            dropped=['repro_qinf_anchor (author main L50-52 would exit at any other point)',
                     'V006 reproduction fields (v006_reproduction, v006_all_bitwise, all_shells_bitwise_equal_to_v006, compared_with)',
                     'TAIL_REANCHOR / lwr_common ANCHOR_UNSCALED identity',
                     'comparisons with EPS_NGC91_SAMPLES_V001 (ce26ced9) and EPS_CERT_NGC91_V001 (1d5eef1b)'],
            files_not_read=[dict(role=r, path=p, sha8=s) for r, p, s in NOT_READ])
        anchor_only = dict(
            c1_shells=list(C1_SHELLS), eps_node_maxima_from_V004=None, eps_check_own_sup=None,
            disclosure=SCOPE_0182, substitute_computed=False)
        if A['bind_check']:
            rec = dict(schema=SCHEMA + '_BIND_CHECK', **HDR, certificate=False, mode=A['mode'], run_id=rid, utc=P.utc(),
                       point=TH['point'], key_check=TH.get('key_check'), other_theta_coordinates=TH.get('other_theta_coordinates'),
                       evaluator=info, custody=custody, producer=prod, build_pins=build_pins, chain=chain,
                       eps_numerics='none (bind check)', timing=TIM)
            w = P.write_new_json('out/%s.json' % base, rec)
            sampler.stop_evt.set()
            print(json.dumps(dict(BIND_CHECK=w['sha256'], path=w['path'], Eref_eff_J=info['Eref_eff_J'], gamma_eff=info['gamma_eff'],
                                  checks=info['checks'])), flush=True)
            return
        summ = summarize(shells, audit, n_lo, n_hi)
        rec = dict(
            schema=SCHEMA + ('_SMOKE_ANCHOR' if A['mode'] == 'smoke' else ''), **HDR,
            certificate=bool(A['mode'] == 'point'), mode=A['mode'], run_id=rid, utc=P.utc(),
            gate='EPS', verdict=summ['rule_verdict'], eps_max=summ['eps_max'], eps_max_shell=summ['eps_max_shell'],
            eps_max_source=summ['eps_max_source'], coverage_inverse_kpc={'NGC': summ['coverage_inverse_kpc']}, summary=summ,
            point=TH['point'], key_check=TH.get('key_check'), other_theta_coordinates=TH.get('other_theta_coordinates'),
            evaluator=info, anchor_comparisons=not_applicable, anchor_only_inputs=anchor_only,
            envelope_self_test=selftest, envelope_audit=audit, shells=shells, custody=custody,
            producer=prod, build_pins=build_pins, chain=chain,
            eps_v005_functions=dict(path=CHAIN[5][1], sha256=CHAIN[5][2]),
            seconds=round(time.perf_counter() - T0, 1))
        w = P.write_new_json('out/%s.json' % base, rec)
        PHASE[0] = 'done'
        sampler.stop_evt.set()
        sampler.join(timeout=30)
        sampler.take()
        r_end = P.rusage()
        step2_end = P.step2_watch_rows(3)
        fp = [s.get('ri_phys_footprint') for s in sampler.samples if s.get('ri_phys_footprint') is not None]
        raw_t = dict(
            schema=SCHEMA + '_TIMING_RAW', **HDR, record=dict(path=w['path'], sha256=w['sha256']), mode=A['mode'], run_id=rid,
            utc_start=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(T_WALL0)), utc_end=P.utc(), pid=os.getpid(),
            nice=os.getpriority(os.PRIO_PROCESS, 0), numpy=np.__version__, python=sys.version,
            timing=dict(total_wall_s=round(time.perf_counter() - T0, 3), total_cpu_s=round(time.process_time() - C0, 3), phases=TIM,
                        per_shell=[dict(n=int(x['lo_inverse_kpc']), wall_s=x['seconds'], cpu_s=x['cpu_seconds'], calls=x['timing'])
                                   for x in shells],
                        audit=[dict(shell=int(a['shell'][0]), wall_cpu=a['timing']) for a in audit]),
            memory=dict(ru_maxrss_bytes_end=r_end['ru_maxrss_bytes'], lifetime_max_phys_footprint_bytes=r_end.get('ri_lifetime_max_phys_footprint'),
                        phys_footprint_end_bytes=r_end.get('ri_phys_footprint'), sampled_phys_footprint_max_bytes=max(fp) if fp else None,
                        n_samples=len(sampler.samples), sample_period_s=sampler.period, samples=sampler.samples),
            rusage=dict(start=r_start, end_of_eps=r_end_eps, end=r_end, mach_timebase=timebase,
                        qos_cpu_s={k: r_end.get(k) for k in ('ri_cpu_time_qos_background', 'ri_cpu_time_qos_default',
                                                            'ri_cpu_time_qos_legacy', 'ri_cpu_time_qos_utility')}),
            step2_watch=dict(start=step2_start, end=step2_end), verified=P.VERIFIED, guard=G)
        wt = P.write_new_json('out/%s_TIMING_RAW.json' % base, raw_t)
        print(json.dumps(dict(RECORD=w['sha256'], record_path=w['path'], TIMING_RAW=wt['sha256'], verdict=summ['rule_verdict'],
                              eps_max=summ['eps_max'], eps_max_shell=summ['eps_max_shell'], eps_max_source=summ['eps_max_source'],
                              total_wall_s=raw_t['timing']['total_wall_s'],
                              lifetime_max_phys_footprint_bytes=raw_t['memory']['lifetime_max_phys_footprint_bytes'],
                              guard_refused=len(G['refused']))), flush=True)
    except BaseException as e:
        sampler.stop_evt.set()
        try:
            P.write_new_json(STOP, dict(schema=SCHEMA + '_RUN_STOP', **HDR, run_id=rid, utc=P.utc(), phase=PHASE[0],
                                        error=repr(e)[:2000], traceback=traceback.format_exc()[-8000:],
                                        elapsed_s=round(time.perf_counter() - T0, 3), verified=P.VERIFIED,
                                        guard=P.guard_report(), samples=sampler.samples, rusage=P.rusage()))
        finally:
            raise


_SELF_BYTES = []


if __name__ == '__main__':
    with open(__file__, 'rb') as _f:   # the bytes of this file as run (the runner checked the same sha before compiling)
        _SELF_BYTES.append(_f.read())
    main()
