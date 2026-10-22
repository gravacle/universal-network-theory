"""NGC per-state LO adapter c2v001 (V006 A153; text of record NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md 9916cb6f,
section 6: S1, S3-S11, S13; S2 as an interface). Root build (Claude2 workflow); nothing here is adopted until root rules
and a distinct lane reviews.

The NGC successor of lo_state_proof_adapter_c3v003 (211a3220) and of the lo_core_r5_cx2v001 (12d36305) arithmetic it runs.
Per consumed state of one NGC call it evaluates the A134 linear readout indicator (A153):
    d_i,s = |v_i| * R_i * rho_s * B1_s / 4   (km/s; lo_core L165 numerator, unchanged)
    g_s   = max_i d_i,s / t_i <= 0.005 in each of the 9 shells, and G = sum_s g_s <= 0.05   (lo_core L170-171)
Scope ALL_CONSUMED_STATES (route-B states included); the A134 Q5 / 0690 readings; no anchor class; the monotone-FAIL rule
(A48 last sentence).

ORDER (freeze before pin). Nothing numeric is read or computed before root's t_i entry is pinned (T_I_ENTRY below).
While T_I_ENTRY is None every consumed state reads UNAVAILABLE / NGC_LO_TOLERANCE_NOT_DECLARED and the call reads
INCOMPLETE: no speed is read, no B1 is rebuilt, no rho is recomputed, no d value exists. That is UNTESTED, not a null.

What each S item is here:
  S1  point custody: driver cx3r008 577f8c94 + the S0 theta key (S0_C2V001 1be5ed70) + the spec sha; the spec's physical
      block is the theta mapping (filler L291-298 order) bitwise; the call result binds the spec sha and the driver.
  S2  rho (INTERFACE): the slot proof (Claude3 ngc_lo_slot_proof, schema UNT_NGC_POINT_LO_SLOT_PROOF_C3V001) and its
      rho_record are pinned inputs; the proof's producer and its rho producer must be in root's approved lists; the spec
      slot = 07745bbf = the proof's driver_certificate; the certificate is never parsed as rho (a rho_record pin equal to
      the launch pin is refused before any read); a1dcdea8 is never a rho producer. Per state the approved NGC producer's
      registered recompute must equal the slot rho under the A138 V03 10-key canonical comparison, else
      NGC_RHO_RECORD_MISMATCH. G4 (two processes) is the slot proof's: seed_rho_reproducibility.bitwise_equal_10_key.
  S3  every state: kept {cube, 2.0}, outer {cylinder, 32}, edges[0] = 2 (and the library's unit edges 2..47), checked
      from the state's own arrays; C4b: the state's gamma_eff, s*spec.physical.gamma (spec route) and s*ge*EB (theta
      route, the rho Binder's) must be one bit pattern, else NGC_GAMMA_ROUTE_BITS_DIFFER (until root rules 0216 N1).
  S4  tiling: hi <= E_top exact tiling (lo_core L156-158); lo < E_top < hi: the unit shells (lo, E_top] starting at lo;
      lo >= E_top: B1_s = 0, r = 0, NOT_IN_STATE_DOMAIN (not a physics PASS). rho_s = the registered rho_used of the full
      shell. All 9 rows kept, G sums all 9. A nonzero unit shell outside exactly one rho shell, or above 91:
      LO_SHELL_COVERAGE_INCOMPLETE.
  S5  B1: the accepted route-A state from the call's ROUTE_A_TAIL_MANIFEST arrays; every other state from a post-run
      rebuild export (OPEN INTERFACE: root's approved rebuild producer) admitted only if its TailState digest equals the
      recorded state digest; then lo_core L109-139 max(stored, recomputed) with the 1e-10 summation-order check.
  S6  |v_i| = max |speed_km_s| over every finite readout of row i in every pass (A134 Q4(a)); the invalid-row rules and
      the monotone-FAIL rule; set(pass.invalid_rows) == X recorded as a diagnostic.
  S7  R_i = the call's own column-mean query-support radius (A152 C-1), bitwise equal to the row contract, which is
      cross-checked against the target-free manifest a2936517 (ids and order exact; radii to 1e-12 relative).
  S8  the row contract {query ids, R_i, t_i, rule id}: no velocity, no sigma, no tau; t_rule_id must be root's entry.
  S9  the inventory from the pinned enumerator ngc_consumed_states_c2v001; classes re-derived here.
  S10 one row-reference policy review per row-contract sha, else ROW_REFERENCE_POLICY_NOT_REVIEWED.
  S12 values (v, d, ratios, G) live only in the per-state record files; the call record carries verdicts, codes and
      shell coverage flags only.
  S13 the MUST_FAIL list is the test suite's.
Every NGC LO record carries the A153 scope disclosure verbatim; a FAIL record also carries the text of record's FAIL text.
"""
import datetime
import hashlib
import importlib.util
import io
import json
import math
import os
import struct
import sys
import types

HERE = os.path.dirname(os.path.realpath(__file__))
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13'
ENUMERATOR = (os.path.join(HERE, 'ngc_consumed_states_c2v001.py'), '607b7f667dfa1612da3fd874ab2656dc5ca487285a28afb2e4b1bfe979bd3125')
LIBRARY = (ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54')       # the library cx3r008 pins
V006 = CTRL + '/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
A153 = {'path': V006, 'heading': '## A153', 'section_sha256': 'aa079db7cc07c2973075514a5d359ff3941b69f414687f12827cc06dab94c51e'}
TEXT_OF_RECORD = {'path': CTRL + '/CLAUDE2/NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md',
                  'sha256': '9916cb6f54a050367fffca0225c97f60b72aaea16a427791ae7c3311838e47e5'}
# Root's t_i entry. None = not declared: every state reads NGC_LO_TOLERANCE_NOT_DECLARED. A successor pins
# {'path': V006, 'heading': '## A1xx', 'section_sha256': <sha of that section's bytes>} here.
T_I_ENTRY = None
DRIVER = {'path': ART + '/ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
          'sha256': '577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377'}
S0 = {'path': ART + '/phase1_c2/S0_RECORD_ROOT_V001/S0_C2V001.json',
      'sha256': '1be5ed709cdb49106652beb76baaafc1c257e760d8cda2c62c18ea6fb2e88143'}
LAUNCH_PIN = {'path': ART + '/tail_scheme_impl_c2/certificates_ngc_k32/gates/LO_NGC_K32_CERT_V001.json',
              'sha256': '07745bbf6d5c35d5a8568de7fc9e78b8c3bd8c3e371680dc8869c42a893c0382'}
MANIFEST = {'path': CTRL + '/CODEX1/NGC3198_TARGET_FREE_QUERY_MANIFEST_V001.json',
            'sha256': 'a293651733ba2e6cff5e313d060521d8481bac39bf6f0af540d0108538535494'}
DDO_RESPONSE_SHA = 'a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'   # never an NGC rho producer (S2)
DDO_RHO_SCHEMA = 'UNT_POINT_RHO_NUMERICAL_CX2V001'

ROUTE = 'NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'                         # A136 G5
STATE_RECORD_SCHEMA = 'UNT_NGC_LO_STATE_RECORD_C2V001'
CALL_SCHEMA = 'UNT_NGC_LO_CALL_ACCEPTANCE_C2V001'
STATE_INPUT_SCHEMA = 'UNT_NGC_LO_STATE_INPUT_C2V001'
ROW_CONTRACT_SCHEMA = 'UNT_NGC_LO_ROW_CONTRACT_C2V001'
REVIEW_SCHEMA = 'UNT_NGC_LO_ROW_POLICY_REVIEW_C2V001'
POINT_IDENTITY_SCHEMA = 'UNT_NGC_LO_POINT_IDENTITY_C2V001'
POINT_CUSTODY_SCHEMA = 'UNT_NGC_LO_POINT_CUSTODY_C2V001'
INVENTORY_SCHEMA = 'UNT_NGC_CONSUMED_STATE_INVENTORY_C2V001'
SLOT_PROOF_SCHEMA = 'UNT_NGC_POINT_LO_SLOT_PROOF_C3V001'                        # Claude3 ngc_lo_slot_proof_c3v001 L68
SLOT_GATE = 'NGC_LO_RHO_SLOT'
RHO_SCHEMA = 'UNT_NGC_POINT_RHO_NUMERICAL_C3V001'                               # Claude3 ngc_rho_producer_c3v001 L113
RHO_IDENTITY_SCHEMA = 'UNT_NGC_POINT_RHO_IDENTITY_C3V001'
RHO_GATE = 'RHO_G'
RHO_VERDICT = 'NUMERICAL_ESTIMATE_REVIEW_REQUIRED'
RHO_SETTINGS = 'registered'
RHO_REGISTERED_KIND = 'REGISTERED'
RHO_REGISTERED_SYMBOL = 'REGISTERED_QINF_BINDER_THETA_BOUND_QINF_EVAL_L146_148'
RHO_COVERAGE = [2.0, 91.0]
RHO_PARTITION = [[2.0, 3.0], [3.0, 4.0], [4.0, 6.0], [6.0, 8.0], [8.0, 12.0], [12.0, 16.0], [16.0, 32.0], [32.0, 64.0],
                 [64.0, 91.0]]
RHO_COMPARE_KEYS = ('schema', 'gate', 'identity', 'point_sha256', 'custody', 'settings', 'coverage_complete',
                    'required_coverage_inverse_kpc', 'full_registered_search_executed', 'shells')   # A138 V03
FORBIDDEN_PROOF_KEYS = ('covers_all_consumed_states', 'cover_all_consumed_states')
S0_SCHEMA = 'PHASE1_S0_C2V001'
THETA_KEY_SCHEMA = 'DDO154_CALIBRATION_THETA_KEY_C2V001'
BIND_KEYS = ('common_scale_s', 'gamma_over_Eref', 'ell_F_m', 'Eref_base_J')
LABEL_PREFIX = 'step5 A_K32_A2_HEADLINE theta_key='
GALAXY = 'NGC3198'
N_ROWS = 43
KEPT = {'shape': 'cube', 'K_inverse_kpc': 2.0}
OUTER = {'shape': 'cylinder', 'K_big_inverse_kpc': 32.0}
C_M_S = 299792458.0                                                             # certs_common_r5 L29 (lo_core CC.C)
TOP_INVERSE_KPC = 91.0
PER_SHELL_MAX = 0.005                                                           # lo_core L171; A136 G5
SUMMED_MAX = 0.05
B1_RELATIVE_CHECK = 1e-10                                                       # lo_core L136
RADIUS_CROSSCHECK_REL = 1e-12
COLUMN_MEAN_OK = 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'                 # driver L8946 (status of record)
AUTHORIZED_INVALID_REASONS = ('QUERY_INSIDE_INNERMOST_NODE', 'QUERY_BEYOND_OUTER_GAS_CUT',
                              'QUERY_OUTSIDE_RETAINED_SUPPORT')                 # driver L9040 headline_rule (N1/A4)
ROW_TOKENS_FORBIDDEN = ('sigma', 'tau', 'err', 'v_obs', 'vobs', 'observed', 'velocity', 'speed', 'target')
SPEED_POLICY = 'A134_Q4A_OWN_CALL_MAX_ABS_OVER_EVERY_RECORDED_READOUT (A153 S6)'

# custody codes (A153 / text of record section 3) and this build's additions (disclosed in the README)
C_TOL = 'NGC_LO_TOLERANCE_NOT_DECLARED'
C_COVERAGE = 'LO_SHELL_COVERAGE_INCOMPLETE'
C_GAMMA = 'NGC_GAMMA_ROUTE_BITS_DIFFER'
C_RHO = 'NGC_RHO_RECORD_MISMATCH'
C_READOUT = 'READOUT_NOT_RECORDED'
C_GEOMETRY = 'STATE_GEOMETRY_MISMATCH'
C_REVIEW = 'ROW_REFERENCE_POLICY_NOT_REVIEWED'
C_CUSTODY = 'NGC_POINT_CUSTODY_MISMATCH'            # build addition
C_CONTRACT = 'NGC_ROW_CONTRACT_MISMATCH'            # build addition (S7/S8 "reads UNAVAILABLE")
C_INPUT = 'NGC_STATE_INPUT_UNAVAILABLE'             # build addition (S5)
C_CLASS = 'NGC_STATE_CLASS_UNAVAILABLE'             # build addition (S9)
C_ADMISSION = 'NGC_LO_ADAPTER_NOT_ADMITTED'         # build addition (root gate, self approval, inventory)
CODES_OF_RECORD = (C_TOL, C_COVERAGE, C_GAMMA, C_RHO, C_READOUT, C_GEOMETRY, C_REVIEW)
CODES_ADDED = (C_CUSTODY, C_CONTRACT, C_INPUT, C_CLASS, C_ADMISSION)
MONOTONE_CODES = (C_READOUT, C_TOL)                 # a decided FAIL is read past these (A48 last sentence)

ACCEPTED = 'ACCEPTED_ROUTE_A'
INHERITED = 'INHERITED_ROUTE_A'
ROUTE_B = 'ROUTE_B_STAGE'
ITERATE = 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'
CLASS_UNAVAILABLE = 'UNAVAILABLE'
DECISIVE_CLASSES = (ACCEPTED, INHERITED, ROUTE_B)
R_PASS = 'PASS'
R_NLTM = 'NON_LAPSE_TAIL_MATERIAL'
R_TRANSIENT = 'LO_UNCERTIFIED_TRANSIENT'
R_INCOMPLETE = 'INCOMPLETE'
R_CLASS_GAP = 'LO_FAIL_STATE_CLASS_UNAVAILABLE'
DOMAIN_TILED = 'TILED'
DOMAIN_PARTIAL = 'PARTIAL_TO_E_TOP'
DOMAIN_OUT = 'NOT_IN_STATE_DOMAIN'
ROW_INCLUDED = 'INCLUDED'
ROW_EXCLUDED = 'EXCLUDED_REGISTERED_MISS'
ROW_MISSING = 'MISSING'

# A153, verbatim (the V006 line, list marker removed); checked against the A153 section bytes at every run.
SCOPE_DISCLOSURE = ("**Scope disclosure, required on every NGC LO record.** The indicator acts on route A's readout "
                    "channel. It **does not bound** the omitted tail's contribution to the 43 route-B rows through the "
                    "source: that contribution is UNTESTED, and its deciding test is the 10-component tail successor as "
                    "a companion call. A PASS certifies the indicator only.")
# Text of record section 3, "What a FAIL record must add", verbatim; checked against its bytes at every run.
FAIL_TEXT = ("Indicator above threshold on the route-A readout channel. At a route-B stage state no NGC row reads this "
             "channel. Whether the 43 rows move materially is UNTESTED. Deciding test: the 10-component tail successor "
             "(A134 Q5's named next step) run as a companion call at this point, its 43 rows compared with this call's "
             "against t_i.")
BLINDING = ('S12: v_reference_km_s, d_i,s and the per-row ratios are NGC values. Until r3a and M-12 are sealed (A133) '
            'root reads only verdicts, reason codes and shell coverage flags.')
THREAD_ENV = ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS')       # single-thread BLAS: the G4 rho reproducibility condition
CAUGHT = (ValueError, KeyError, TypeError, OSError, OverflowError, AttributeError, IndexError, ZeroDivisionError,
          FloatingPointError)


class Refusal(ValueError):
    """Fail-closed refusal carrying a custody code."""

    def __init__(self, code, detail=''):
        ValueError.__init__(self, '%s: %s' % (code, detail) if detail else code)
        self.code = code
        self.detail = detail


def need(ok, code, detail=''):
    if not ok:
        raise Refusal(code, detail)


# ------------------------------------------------------------------------------------------------ bytes and pins
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and is_sha(x['sha256'])


def _num(x):
    return type(x) in (int, float) and math.isfinite(x)


def hexf(x):
    return float(x).hex()


def bits(x):
    return struct.pack('<d', float(x)).hex()


def strict_json(raw, label, code=C_INPUT):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, code, label + ': DUPLICATE_JSON_KEY')
            out[k] = v
        return out

    def bad(_):
        raise Refusal(code, label + ': NONFINITE_JSON')
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except Refusal:
        raise
    except ValueError:
        raise Refusal(code, label + ': JSON_INVALID')


def make_reader(registry):
    """Exact-bytes reader of {path, sha256} pins: absolute canonical path, no NGC3198-named file except the two the
    registry names (the V006 addendum and the target-free manifest, read-only)."""
    allowed = {os.path.realpath(registry['a153']['path']), os.path.realpath(registry['manifest']['path'])}
    if registry.get('t_i_entry'):
        allowed.add(os.path.realpath(registry['t_i_entry']['path']))

    def read_raw(ref, code=C_INPUT, label='pin'):
        need(is_pin(ref), code, label + ': NOT_AN_EXACT_PIN')
        p = ref['path']
        need(os.path.isabs(p), code, label + ': PATH_NOT_ABSOLUTE')
        real = os.path.realpath(p)
        need('ngc3198' not in os.path.basename(real).lower() or real in allowed, code,
             label + ': NGC3198_NAMED_FILE_REFUSED ' + os.path.basename(real))
        try:
            with open(real, 'rb') as f:
                raw = f.read()
        except OSError as exc:
            raise Refusal(code, '%s: UNREADABLE %s' % (label, exc))
        need(hashlib.sha256(raw).hexdigest() == ref['sha256'], code, label + ': BYTE_PIN_MISMATCH ' + p)
        return raw
    return read_raw


def section_bytes(raw, heading):
    """The bytes of one addendum entry: from the line starting with `heading` up to (not including) the next '## '
    heading line, joined with b'\\n' (the A153 section sha was computed this way from the V006 bytes)."""
    lines = raw.split(b'\n')
    hits = [i for i, ln in enumerate(lines) if ln.startswith(heading.encode() + b':') or ln == heading.encode()]
    if len(hits) != 1:
        return None
    j = hits[0] + 1
    while j < len(lines) and not lines[j].startswith(b'## '):
        j += 1
    return b'\n'.join(lines[hits[0]:j])


def _entry_text(ref, registry, read_raw, label):
    need(isinstance(ref, dict) and set(ref) == {'path', 'heading', 'section_sha256'} and is_sha(ref['section_sha256'])
         and isinstance(ref['heading'], str) and ref['heading'].startswith('## '), C_ADMISSION, label + ': ENTRY_PIN_MALFORMED')
    real = os.path.realpath(ref['path'])
    try:
        with open(real, 'rb') as f:
            raw = f.read()
    except OSError as exc:
        raise Refusal(C_ADMISSION, '%s: UNREADABLE %s' % (label, exc))
    sec = section_bytes(raw, ref['heading'])
    need(sec is not None and hashlib.sha256(sec).hexdigest() == ref['section_sha256'], C_ADMISSION,
         label + ': SECTION_NOT_FOUND_OR_CHANGED')
    return sec.decode('utf-8')


def root_gate(registry, read_raw):
    """A153 entry (section-pinned, robust to later appends), the text of record (whole-file pin), the scope disclosure and
    the FAIL text verbatim in those bytes; root's t_i entry when pinned."""
    sec = _entry_text(registry['a153'], registry, read_raw, 'A153')
    need(SCOPE_DISCLOSURE in sec, C_ADMISSION, 'A153 scope disclosure text not found verbatim')
    tor = read_raw(registry['text_of_record'], C_ADMISSION, 'text of record').decode('utf-8')
    need(FAIL_TEXT in tor, C_ADMISSION, 'FAIL text not found verbatim in the text of record')
    out = [dict(registry['a153']), dict(registry['text_of_record'])]
    if registry.get('t_i_entry') is not None:
        _entry_text(registry['t_i_entry'], registry, read_raw, 't_i entry')
        out.append(dict(registry['t_i_entry']))
    return out


def t_rule_id(registry):
    e = registry.get('t_i_entry')
    return None if e is None else '%s@%s' % (e['heading'], e['section_sha256'])


def real_registry():
    return {'kind': 'REGISTERED', 'a153': dict(A153), 'text_of_record': dict(TEXT_OF_RECORD), 't_i_entry': T_I_ENTRY,
            'driver': dict(DRIVER), 's0': dict(S0), 'launch': dict(LAUNCH_PIN), 'manifest': dict(MANIFEST)}


def check_registry(registry):
    keys = {'kind', 'a153', 'text_of_record', 't_i_entry', 'driver', 's0', 'launch', 'manifest'}
    need(isinstance(registry, dict) and set(registry) == keys and registry['kind'] in ('REGISTERED', 'SYNTHETIC_TEST'),
         C_ADMISSION, 'REGISTRY_MALFORMED')
    if registry['kind'] == 'REGISTERED':
        need(registry == real_registry(), C_ADMISSION, 'REGISTRY_IS_NOT_THE_REGISTERED_ONE')
    else:   # a synthetic registry can never meet a real call, a real S0 point or the real spec slot
        need(registry['driver']['sha256'] != DRIVER['sha256'] and registry['s0']['sha256'] != S0['sha256']
             and registry['launch']['sha256'] != LAUNCH_PIN['sha256'] and registry['manifest']['sha256'] != MANIFEST['sha256']
             and os.path.realpath(registry['a153']['path']) != os.path.realpath(V006)
             and (registry['t_i_entry'] is None or os.path.realpath(registry['t_i_entry']['path']) != os.path.realpath(V006)),
             C_ADMISSION, 'SYNTHETIC_REGISTRY_TOUCHES_A_REGISTERED_INPUT')
    return registry


def load_exact(path, sha, name, code=C_ADMISSION):
    need(isinstance(path, str) and os.path.isabs(path) and os.path.realpath(path) == path, code,
         'NONCANONICAL_MODULE_PATH: ' + str(path))
    with open(path, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == sha, code, 'MODULE_PIN_MISMATCH: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def self_pin():
    p = __file__
    need(isinstance(p, str) and os.path.isabs(p) and os.path.realpath(p) == p, C_ADMISSION, 'NONCANONICAL_PRODUCER_FILE')
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def write_new(out_root, name, obj):
    need(isinstance(out_root, str) and os.path.isabs(out_root) and os.path.realpath(out_root) == out_root
         and os.path.isdir(out_root), C_ADMISSION, 'OUT_ROOT_INVALID')
    need(isinstance(name, str) and name == os.path.basename(name) and name.endswith('.json'), C_ADMISSION, 'OUT_NAME_INVALID')
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    path = os.path.join(out_root, name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}


def _forbidden_anywhere(obj, keys=FORBIDDEN_PROOF_KEYS):
    if isinstance(obj, dict):
        return any(k in keys for k in obj) or any(_forbidden_anywhere(v, keys) for v in obj.values())
    if isinstance(obj, list):
        return any(_forbidden_anywhere(v, keys) for v in obj)
    return False


def _keys_with_tokens(obj, tokens=ROW_TOKENS_FORBIDDEN):
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if any(t in str(k).lower() for t in tokens):
                found.append(str(k))
            found += _keys_with_tokens(v, tokens)
    elif isinstance(obj, list):
        for v in obj:
            found += _keys_with_tokens(v, tokens)
    return found


# ------------------------------------------------------------------------------------------------ S1 point custody
def theta_key(theta):
    th = {str(k): float(v) for k, v in theta.items()}
    return hashlib.sha256(canonical({'schema': THETA_KEY_SCHEMA, 'theta': th})).hexdigest()


def point_custody(spec_ref, result, registry, read_raw):
    """S1 / A136 G3: driver + S0 theta key + spec sha; the spec is that theta's call; the call ran that spec."""
    spec = strict_json(read_raw(spec_ref, C_CUSTODY, 'spec'), 'spec', C_CUSTODY)
    need(isinstance(spec, dict) and spec.get('galaxy') == GALAXY, C_CUSTODY, 'SPEC_GALAXY')
    label = spec.get('label')
    need(isinstance(label, str) and label.startswith(LABEL_PREFIX) and is_sha(label[len(LABEL_PREFIX):]), C_CUSTODY,
         'SPEC_LABEL_HAS_NO_THETA_KEY')
    key = label[len(LABEL_PREFIX):]
    s0 = strict_json(read_raw(registry['s0'], C_CUSTODY, 'S0 record'), 'S0 record', C_CUSTODY)
    pts = s0.get('points') if isinstance(s0, dict) else None
    need(isinstance(s0, dict) and s0.get('schema') == S0_SCHEMA and isinstance(pts, list) and len(pts) == 4, C_CUSTODY,
         'S0_RECORD_SHAPE')
    hit = [p for p in pts if isinstance(p, dict) and p.get('key') == key]
    need(len(hit) == 1, C_CUSTODY, 'THETA_KEY_NOT_IN_S0_RECORD')
    th_hex = hit[0].get('theta_hex')
    need(isinstance(th_hex, dict) and all(isinstance(v, str) for v in th_hex.values()), C_CUSTODY, 'S0_THETA_HEX_MISSING')
    theta = {k: float.fromhex(v) for k, v in th_hex.items()}
    need(all(k in theta and math.isfinite(theta[k]) and theta[k] > 0 for k in BIND_KEYS), C_CUSTODY, 'S0_BIND_KEYS')
    need(theta_key(theta) == key, C_CUSTODY, 'THETA_KEY_NOT_RECOMPUTED_FROM_THETA_HEX')
    s, ge, ell, EB = (theta[k] for k in BIND_KEYS)
    phys = spec.get('physical')
    need(isinstance(phys, dict), C_CUSTODY, 'SPEC_PHYSICAL_MISSING')
    want = {'Eref_J': EB, 'ell_F_m': ell, 'gamma': ge * EB, 'common_scale_s': s}      # filler L294 operation order
    for k, v in want.items():
        need(_num(phys.get(k)) and hexf(phys[k]) == hexf(v), C_CUSTODY, 'SPEC_PHYSICAL_NOT_THE_THETA_MAPPING ' + k)
    uv = ((spec.get('numerics') or {}).get('uv_tail') or {})
    need(uv.get('lo_certificate') == registry['launch'], C_CUSTODY, 'SPEC_LO_SLOT_IS_NOT_THE_LAUNCH_PIN (A136)')
    need(uv.get('outer') == OUTER, C_CUSTODY, 'SPEC_OUTER_NOT_CYLINDER_32')
    need(_num(uv.get('lambda_scale')) and uv['lambda_scale'] > 0, C_CUSTODY, 'SPEC_LAMBDA_SCALE')
    cw = ((spec.get('numerics') or {}).get('route_a') or {}).get('column_workers')
    need(type(cw) is int and cw >= 1, C_CUSTODY, 'SPEC_ROUTE_A_COLUMN_WORKERS')
    read_raw(registry['launch'], C_CUSTODY, 'launch pin (bytes only; never parsed)')
    need(result.get('driver_sha256') == registry['driver']['sha256'], C_CUSTODY, 'CALL_DRIVER_NOT_THE_REGISTERED_DRIVER')
    need(result.get('galaxy') == GALAXY, C_CUSTODY, 'CALL_GALAXY')
    need(result.get('call_spec_sha256') == spec_ref['sha256'], C_CUSTODY, 'CALL_DID_NOT_RUN_THIS_SPEC')
    identity = {'schema': POINT_IDENTITY_SCHEMA, 'driver_sha256': registry['driver']['sha256'],
                's0_record_sha256': registry['s0']['sha256'], 'theta_key': key, 'spec_sha256': spec_ref['sha256']}
    psha = digest(identity)
    custody = {'schema': POINT_CUSTODY_SCHEMA, 'driver': dict(registry['driver']), 's0_record': dict(registry['s0']),
               'theta_key': key, 'theta_role': hit[0].get('role'), 'spec': dict(spec_ref),
               'lo_certificate_launch_pin': dict(registry['launch']), 'text_of_record': dict(registry['text_of_record']),
               'a153': dict(registry['a153']), 'registry_kind': registry['kind'], 'point_sha256': psha}
    routes = {'spec_route_gamma_eff_hex': hexf(phys['common_scale_s'] * phys['gamma']),
              'theta_route_gamma_eff_hex': hexf(s * ge * EB)}                  # qinf_eval L146-148 order
    return {'spec': spec, 'key': key, 'identity': identity, 'point_sha256': psha, 'custody': custody,
            'custody_sha256': digest(custody), 'theta_hex': {k: hexf(theta[k]) for k in BIND_KEYS},
            'column_workers': cw, 'gamma_routes': routes, 'uv': uv}


# ------------------------------------------------------------------------------------------------ S2 rho (interface)
def rho_bitwise_canonical(rec):
    need(isinstance(rec, dict), C_RHO, 'RHO_RECORD_NOT_AN_OBJECT')
    return canonical({k: rec.get(k) for k in RHO_COMPARE_KEYS})


def check_rho_record(rec, point, rho_producer_pin, *, allow_synthetic):
    """One NGC rho record of the approved producer at this point (no number computed)."""
    need(isinstance(rec, dict), C_RHO, 'RHO_RECORD_NOT_AN_OBJECT')
    need(rec.get('schema') != DDO_RHO_SCHEMA and (rec.get('producer') or {}).get('sha256') != DDO_RESPONSE_SHA, C_RHO,
         'RHO_FROM_A1DCDEA8_REFUSED (S2: per-shell seeds never match the NGC producer)')
    need(not _forbidden_anywhere(rec), C_RHO, 'RHO_RECORD_CARRIES_COVERS_ALL_CONSUMED_STATES')
    need(rec.get('schema') == RHO_SCHEMA and rec.get('gate') == RHO_GATE, C_RHO, 'RHO_SCHEMA_OR_GATE')
    need(rec.get('status') == 'TESTED' and rec.get('verdict') == RHO_VERDICT, C_RHO, 'RHO_STATUS_OR_VERDICT')
    need(rec.get('settings') == RHO_SETTINGS and rec.get('full_registered_search_executed') is True, C_RHO,
         'RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH')
    need(rec.get('coverage_complete') is True and rec.get('required_coverage_inverse_kpc') == RHO_COVERAGE, C_RHO,
         'RHO_COVERAGE_NOT_2_TO_91')
    shells = rec.get('shells')
    need(isinstance(shells, list) and [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells]
         == RHO_PARTITION, C_RHO, 'RHO_PARTITION_NOT_THE_9_NGC_SHELLS')
    for s in shells:
        need(type(s.get('rho_used')) is float and math.isfinite(s['rho_used']) and s['rho_used'] >= 0, C_RHO, 'RHO_USED_INVALID')
    need(rec.get('producer') == rho_producer_pin, C_RHO, 'RHO_PRODUCER_NOT_THE_APPROVED_NGC_PRODUCER')
    idn, cus = rec.get('identity'), rec.get('custody')
    need(isinstance(idn, dict) and isinstance(cus, dict) and rec.get('point_sha256') == digest(idn)
         and cus.get('point_sha256') == rec.get('point_sha256'), C_RHO, 'RHO_IDENTITY_POINT_SHA_INCONSISTENT')
    need(idn.get('schema') == RHO_IDENTITY_SCHEMA and idn.get('theta_key') == point['key']
         and idn.get('s0_record_sha256') == point['identity']['s0_record_sha256']
         and idn.get('driver_sha256') == point['identity']['driver_sha256']
         and idn.get('spec_sha256') == point['identity']['spec_sha256']
         and idn.get('route_a_column_workers') == point['column_workers'], C_RHO, 'RHO_NOT_AT_THIS_POINT_AND_SPEC (S1)')
    tb = idn.get('theta_binding_hex')
    need(isinstance(tb, dict) and tb == {'s': point['theta_hex']['common_scale_s'],
                                         'gamma_over_Eref': point['theta_hex']['gamma_over_Eref'],
                                         'ell_F_m': point['theta_hex']['ell_F_m'],
                                         'Eref_base_J': point['theta_hex']['Eref_base_J']}, C_RHO,
         'RHO_THETA_BINDING_NOT_THE_S0_THETA')
    if not allow_synthetic:
        need(cus.get('registry_kind') == RHO_REGISTERED_KIND and cus.get('symbol_route') == RHO_REGISTERED_SYMBOL, C_RHO,
             'RHO_RECORD_IS_A_TEST_SYMBOL_RECORD')
    return shells


def check_slot_proof(proof_ref, point, registry, read_raw, *, approved_slot, approved_rho, allow_synthetic):
    """S2: the NGC slot proof (Claude3 schema), the slot rho it binds, and the approved rho producer."""
    need(is_pin(proof_ref), C_RHO, 'SLOT_PROOF_NOT_PINNED')
    proof = strict_json(read_raw(proof_ref, C_RHO, 'slot proof'), 'slot proof', C_RHO)
    need(isinstance(proof, dict) and not _forbidden_anywhere(proof), C_RHO, 'SLOT_PROOF_CARRIES_COVERS_ALL_CONSUMED_STATES')
    need(proof.get('schema') == SLOT_PROOF_SCHEMA and proof.get('gate') == SLOT_GATE and proof.get('status') == 'TESTED'
         and proof.get('verdict') == 'PASS', C_RHO, 'SLOT_PROOF_NOT_TESTED_PASS')
    prod = proof.get('producer')
    need(is_pin(prod) and prod['sha256'] in set(approved_slot), C_RHO, 'SLOT_PROOF_PRODUCER_NOT_APPROVED')
    read_raw(prod, C_RHO, 'slot proof producer')
    need(proof.get('theta_key') == point['key'], C_RHO, 'SLOT_PROOF_OTHER_POINT')
    slot = point['uv'].get('lo_certificate')
    need(proof.get('driver_certificate') == slot == registry['launch'] and proof.get('lo_certificate_launch_pin')
         == registry['launch'], C_RHO, 'SLOT_PROOF_SLOT_IS_NOT_07745BBF')
    rr = proof.get('rho_record')
    need(is_pin(rr), C_RHO, 'SLOT_PROOF_RHO_RECORD_NOT_PINNED')
    need(rr['sha256'] != registry['launch']['sha256'] and os.path.realpath(rr['path']) != os.path.realpath(registry['launch']['path']),
         C_RHO, 'CERTIFICATE_PARSED_AS_RHO_REFUSED (S2: the certificate is never a rho record)')
    rp = proof.get('rho_producer')
    need(is_pin(rp) and rp['sha256'] != DDO_RESPONSE_SHA, C_RHO, 'RHO_PRODUCER_A1DCDEA8_REFUSED')
    need(rp['sha256'] in set(approved_rho), C_RHO, 'RHO_PRODUCER_NOT_APPROVED')
    read_raw(rp, C_RHO, 'rho producer')
    rho = strict_json(read_raw(rr, C_RHO, 'slot rho record'), 'slot rho record', C_RHO)
    shells = check_rho_record(rho, point, rp, allow_synthetic=allow_synthetic)
    need(proof.get('point_sha256') == rho.get('point_sha256'), C_RHO, 'SLOT_PROOF_POINT_DIFFERS_FROM_RHO')
    need(proof.get('rho_bitwise_canonical_sha256') == hashlib.sha256(rho_bitwise_canonical(rho)).hexdigest(), C_RHO,
         'SLOT_PROOF_CANONICAL_SHA_DIFFERS')
    seed = proof.get('seed_rho_reproducibility')
    need(isinstance(seed, dict) and seed.get('bitwise_equal_10_key') is True, C_RHO, 'G4_TWO_PROCESS_EQUALITY_UNPROVEN')
    need(proof.get('lo_route') == ROUTE and proof.get('lo_certified') is False, C_RHO, 'SLOT_PROOF_ROUTE')
    return {'proof': dict(proof_ref), 'slot_rho_pin': dict(rr), 'rho_producer': dict(rp), 'shells': shells,
            'slot_canonical': rho_bitwise_canonical(rho),
            'slot_canonical_sha256': hashlib.sha256(rho_bitwise_canonical(rho)).hexdigest()}


# ------------------------------------------------------------------------------------------------ S8 row contract, S10
def check_row_contract(ref, registry, read_raw, point, result_pin, rule_id):
    """S8: {query ids in manifest order, R_i, t_i, rule id}; no velocity, no sigma, no tau. Returns (contract, sha, t_ok)."""
    need(is_pin(ref), C_CONTRACT, 'ROW_CONTRACT_NOT_PINNED')
    c = strict_json(read_raw(ref, C_CONTRACT, 'row contract'), 'row contract', C_CONTRACT)
    need(isinstance(c, dict), C_CONTRACT, 'ROW_CONTRACT_NOT_AN_OBJECT')
    bad = _keys_with_tokens(c)
    need(not bad, C_CONTRACT, 'ROW_CONTRACT_CARRIES_VELOCITY_SIGMA_OR_TAU_KEYS %s' % sorted(set(bad)))
    keys = {'schema', 'query_ids', 'manifest', 'manifest_radius_scale', 'R_m', 't_km_s', 't_rule_id', 'binding'}
    need(set(c) <= keys and set(c) >= keys - {'t_km_s', 't_rule_id'}, C_CONTRACT, 'ROW_CONTRACT_FIELDS %s' % sorted(set(c) ^ keys))
    need(c['schema'] == ROW_CONTRACT_SCHEMA, C_CONTRACT, 'ROW_CONTRACT_SCHEMA')
    ids = c['query_ids']
    need(isinstance(ids, list) and len(ids) == N_ROWS and len(set(ids)) == N_ROWS
         and all(isinstance(q, str) and q for q in ids), C_CONTRACT, 'ROW_CONTRACT_IDS')
    need(c['manifest'] == registry['manifest'], C_CONTRACT, 'ROW_CONTRACT_MANIFEST_NOT_A2936517')
    R = c['R_m']
    need(isinstance(R, list) and len(R) == N_ROWS and all(_num(x) and x > 0 for x in R), C_CONTRACT, 'ROW_CONTRACT_R')
    sc = c['manifest_radius_scale']
    need(_num(sc) and sc > 0, C_CONTRACT, 'ROW_CONTRACT_RADIUS_SCALE')
    b = c['binding']
    need(b is None or (isinstance(b, dict) and len(b) == 1 and (
        (set(b) == {'point_sha256'} and b['point_sha256'] == point['point_sha256'])
        or (set(b) == {'call_result_sha256'} and b['call_result_sha256'] == result_pin['sha256']))), C_CONTRACT,
         'ROW_CONTRACT_BINDING_NOT_THIS_POINT_OR_CALL')
    man = strict_json(read_raw(registry['manifest'], C_CONTRACT, 'target-free manifest'), 'manifest', C_CONTRACT)
    rows = man.get('rows') if isinstance(man, dict) else None
    need(isinstance(rows, list) and [r.get('query_id') if isinstance(r, dict) else None for r in rows] == ids, C_CONTRACT,
         'ROW_CONTRACT_ORDER_NOT_THE_MANIFEST_ORDER (S7)')
    for r, x in zip(rows, R):
        need(r.get('Rad_unit') == 'kpc' and isinstance(r.get('Rad_text'), str), C_CONTRACT, 'MANIFEST_ROW_UNIT')
        want = float(r['Rad_text']) * sc * 3.085677581491367e19                       # driver KPC_M L183
        need(want > 0 and abs(x - want) <= RADIUS_CROSSCHECK_REL * want, C_CONTRACT,
             'ROW_CONTRACT_RADIUS_DIFFERS_FROM_MANIFEST (S7) ' + str(r.get('query_id')))
    # t_i: absent, or not bound to root's entry -> NGC_LO_TOLERANCE_NOT_DECLARED (never a FAIL; nothing computed)
    t, rid = c.get('t_km_s'), c.get('t_rule_id')
    t_ok = (rule_id is not None and rid == rule_id and isinstance(t, list) and len(t) == N_ROWS
            and all(v is None or (_num(v) and v >= 0) for v in t))
    if isinstance(t, list):
        need(all(v is None or (_num(v) and v >= 0) for v in t), C_CONTRACT, 'ROW_CONTRACT_T_NEGATIVE_OR_NONNUMERIC')
    return c, ref['sha256'], t_ok


def check_review(review_ref, trusted, contract_sha, read_raw):
    """S10: one NGC review per row-contract sha (lo_core L225-231 analogue)."""
    if not is_pin(review_ref) or review_ref['sha256'] not in set(trusted or ()):
        raise Refusal(C_REVIEW, 'no trusted review for row contract %s' % contract_sha[:16])
    rv = strict_json(read_raw(review_ref, C_REVIEW, 'row policy review'), 'row policy review', C_REVIEW)
    need(isinstance(rv, dict) and rv.get('schema') == REVIEW_SCHEMA and rv.get('verdict') == 'APPROVED'
         and rv.get('row_contract_sha256') == contract_sha, C_REVIEW, 'REVIEW_SCOPE_OR_APPROVAL_MISMATCH')
    return dict(review_ref)


# ------------------------------------------------------------------------------------------------ S6, S7 own readouts
def own_call_readouts(result, row_ids):
    """S6. Per row: INCLUDED (exact max |speed| over every pass), EXCLUDED_REGISTERED_MISS (in X with an authorized reason
    and no finite readout in any pass, every pass recorded), or MISSING (lower bound = the max over what is recorded, or
    None). Returns {'rows': [...], 'X': [...], 'diagnostic': {...}, 'call_problem': str|None}."""
    n = len(row_ids)
    out = {'rows': [{'id': q, 'status': ROW_MISSING, 'v': None, 'reason': None} for q in row_ids], 'X': None,
           'diagnostic': {}, 'call_problem': None}
    passes = result.get('passes') if isinstance(result, dict) else None
    if not isinstance(passes, list) or not passes:
        out['call_problem'] = 'NO_PASS_RECORDED'
        return out
    final = result.get('rows')
    if not isinstance(final, list) or [r.get('id') if isinstance(r, dict) else None for r in final] != list(row_ids):
        out['call_problem'] = 'FINAL_ROWS_NOT_THE_CONTRACT_ROWS'
        return out
    if not isinstance(passes[-1], dict) or final != passes[-1].get('rows'):
        out['call_problem'] = 'FINAL_ROWS_DIFFER_FROM_FINAL_PASS'
        return out
    X = result.get('invalid_rows', [])
    marked = [r['id'] for r in final if r.get('valid') is False]
    if not isinstance(X, list) or sorted(X) != sorted(marked) or len(set(X)) != len(X):
        out['call_problem'] = 'INVALID_ROWS_X_INCONSISTENT_WITH_FINAL_ROWS'
        return out
    out['X'] = list(X)
    reason = {r['id']: r.get('reason') for r in final}
    vmax = [None] * n
    missing = [False] * n
    pass_sets, pass_status = [], []
    for p in passes:
        rows = p.get('rows') if isinstance(p, dict) else None
        if not isinstance(rows, list) or [r.get('id') if isinstance(r, dict) else None for r in rows] != list(row_ids):
            missing = [True] * n                                        # a missing / malformed pass row list
            pass_sets.append(None)
            cm = p.get('column_mean') if isinstance(p, dict) else None
            pass_status.append('NOT_OBSERVED' if rows is None and isinstance(cm, str) and cm.startswith('NOT_OBSERVED')
                               else 'MISSING_OR_MALFORMED')
            continue
        pass_status.append('RECORDED')
        pi = p.get('invalid_rows')
        pass_sets.append(sorted(pi) if isinstance(pi, list) else None)
        for i, r in enumerate(rows):
            v = r.get('speed_km_s')
            if type(v) in (int, float) and math.isfinite(v):
                a = abs(float(v))
                vmax[i] = a if vmax[i] is None or a > vmax[i] else vmax[i]
            elif v is None and r.get('valid') is False:
                continue                                                # no readout in this pass (row invalid here)
            else:
                missing[i] = True                                       # missing or non-finite readout
    for i, q in enumerate(row_ids):
        row = out['rows'][i]
        in_x = q in X
        row['reason'] = reason.get(q) if in_x else None
        if in_x and reason.get(q) in AUTHORIZED_INVALID_REASONS and vmax[i] is None and not missing[i]:
            row.update(status=ROW_EXCLUDED, v=None)
        elif missing[i] or (in_x and reason.get(q) not in AUTHORIZED_INVALID_REASONS and vmax[i] is None) or vmax[i] is None:
            row.update(status=ROW_MISSING, v=vmax[i])                   # v is a lower bound (or None)
        else:
            row.update(status=ROW_INCLUDED, v=vmax[i])                  # in X with a finite readout: INCLUDED (A48)
    out['diagnostic'] = {'pass_invalid_rows_equal_X': [None if s is None else s == sorted(X) for s in pass_sets],
                         'pass_row_list_status': pass_status,
                         'rule': 'recorded only, not a gate (S6; U3: a NOT_OBSERVED pass is read as a missing row list)'}
    return out


def own_call_radii(result, out_dir, read_raw):
    """S7: the call's own column-mean query support of the final pass (radius_m per valid row; an invalid row's radius_m
    from the column mean's own row). Returns {id: radius_m}."""
    passes = result.get('passes')
    fp = passes[-1] if isinstance(passes, list) and passes and isinstance(passes[-1], dict) else {}
    cm = fp.get('column_mean')
    need(isinstance(cm, dict) and cm.get('status') == COLUMN_MEAN_OK, C_CONTRACT, 'FINAL_COLUMN_MEAN_UNAVAILABLE')
    pin = {'path': cm.get('path'), 'sha256': cm.get('sha256')}
    need(is_pin(pin) and os.path.realpath(pin['path']).startswith(out_dir + os.sep), C_CONTRACT, 'COLUMN_MEAN_NOT_OWN_CALL')
    cmr = strict_json(read_raw(pin, C_CONTRACT, 'final column mean'), 'final column mean', C_CONTRACT)
    pred = cmr.get('prediction') if isinstance(cmr, dict) else None
    need(isinstance(pred, dict) and cmr.get('status') == COLUMN_MEAN_OK and pred.get('rows') == fp.get('rows'), C_CONTRACT,
         'COLUMN_MEAN_ROWS_NOT_THE_FINAL_ROWS')
    rows = pred['rows']
    valid = [r['id'] for r in rows if isinstance(r, dict) and r.get('valid', True) is True]
    sup = pred.get('query_support')
    need(isinstance(sup, list) and [s.get('id') if isinstance(s, dict) else None for s in sup] == valid, C_CONTRACT,
         'QUERY_SUPPORT_NOT_THE_VALID_ROWS')
    radii = {}
    for s in sup:
        need(_num(s.get('radius_m')) and s['radius_m'] > 0, C_CONTRACT, 'QUERY_SUPPORT_RADIUS')
        radii[s['id']] = float(s['radius_m'])
    for r in rows:
        if isinstance(r, dict) and r.get('valid') is False and _num(r.get('radius_m')) and r['radius_m'] > 0:
            radii[r['id']] = float(r['radius_m'])
    return radii, pin


# ------------------------------------------------------------------------------------------------ S3, S5 state arrays
def _finite(x, name, *, positive=False, nonnegative=False, code=C_INPUT):
    import numpy as np
    a = np.asarray(x)
    need(a.dtype != object and np.all(np.isfinite(a)), code, 'NONFINITE ' + name)
    if positive:
        need(np.all(a > 0), code, 'NONPOSITIVE ' + name)
    if nonnegative:
        need(np.all(a >= 0), code, 'NEGATIVE ' + name)
    return a


def expected_unit_edges():
    """Library v002 L730-731 at kept cube 2 / outer cylinder 32: Kmin + arange(0, ceil(sqrt(top^2+topz^2) - Kmin) + 2)
    with top = topz = K_big (_grid L246-247). E_top = 47 /kpc."""
    import numpy as np
    kmin, top = KEPT['K_inverse_kpc'], OUTER['K_big_inverse_kpc']
    return kmin + np.arange(0, int(math.ceil(math.sqrt(top ** 2 + top ** 2) - kmin)) + 2, dtype=float)


def check_state_geometry(record, arrays):
    """S3 (replaces lo_core L85-86, L104, L214): checked on every state from its own record and arrays."""
    import numpy as np
    need(record.get('empty') is False, C_GEOMETRY, 'STATE_EMPTY_OR_UNRECORDED')
    need(record.get('kept') == KEPT, C_GEOMETRY, 'KEPT_NOT_CUBE_2: %r' % (record.get('kept'),))
    need(record.get('outer') == OUTER, C_GEOMETRY, 'OUTER_NOT_CYLINDER_32: %r' % (record.get('outer'),))
    need(not any(str(k).startswith('sph_') for k in arrays), C_GEOMETRY, 'SPHERE_ARRAYS')
    edges = _finite(arrays['shell_edges_inverse_kpc'], 'shell edges', positive=True, code=C_GEOMETRY)
    need(edges.ndim == 1 and len(edges) >= 2 and np.all(np.diff(edges) > 0), C_GEOMETRY, 'EDGES_NOT_INCREASING')
    need(float(edges[0]) == 2.0, C_GEOMETRY, 'EDGES0_NOT_2')
    need(np.array_equal(edges, expected_unit_edges()), C_GEOMETRY,
         'UNIT_EDGES_NOT_THE_OUTER_32_EDGES (E_top must be 47; a cylinder-64 layout is refused without S4)')
    return edges


def validate_tail_arrays(arrays, record):
    """lo_core L81-106 with the NGC geometry (S3)."""
    edges = check_state_geometry(record, arrays)
    for key in ('kp', 'kz', 'wkp', 'wz'):
        a = _finite(arrays[key], key, positive=True)
        need(a.ndim == 1, C_INPUT, 'non-vector ' + key)
    need(arrays['wkp'].shape == arrays['kp'].shape and arrays['wz'].shape == arrays['kz'].shape, C_INPUT, 'quadrature shape')
    P, F = _finite(arrays['P'], 'P'), _finite(arrays['F'], 'F')
    need(P.ndim == 2 and F.ndim == 2 and P.shape[0] == len(arrays['kp']) and F.shape == (len(arrays['kz']), P.shape[1]),
         C_INPUT, 'source factor shape')
    import numpy as np
    need(not (np.iscomplexobj(P) and np.any(P.imag)), C_INPUT, 'non-real radial factor')
    stored = _finite(arrays['shell_integrals'], 'shell integrals', nonnegative=True)
    need(stored.shape == (len(edges) - 1, 3), C_INPUT, 'shell data shape/coverage')
    return edges


def recompute_b1(arrays, record, U, *, chunk=64):
    """lo_core L109-139, unchanged arithmetic; the NGC validation above."""
    import numpy as np
    edges = validate_tail_arrays(arrays, record)
    pref = float(record['lambda_scale']) / (4 * float(record['gamma_eff']) * (2 * math.pi) ** 3)
    need(record.get('pref') == pref, C_GEOMETRY, 'tail prefactor mismatch')
    _finite([pref, record['c_m_s']], 'pref/c', positive=True)
    kp, kz = arrays['kp'], arrays['kz']
    out = np.zeros(len(edges) - 1)
    for start in range(0, len(kp), chunk):
        sl = slice(start, min(start + chunk, len(kp)))
        k = kp[sl]
        source = arrays['P'][sl] @ arrays['F'].T
        c0 = U._c0_D(record['kept'], record['outer'], k * U.KPC_M, kz * U.KPC_M)
        need(not np.any(c0 < 0), C_INPUT, 'negative angular-domain measure')
        km = np.sqrt(k[:, None] ** 2 + kz[None, :] ** 2)
        fac = (pref * arrays['wkp'][sl] * k)[:, None] * arrays['wz'][None, :] / km ** 2
        weight = 2 * np.abs(source) * fac * c0 * km
        index = np.clip(np.searchsorted(edges, km * U.KPC_M, side='right') - 1, 0, len(out) - 1)
        out += np.bincount(index.ravel(), weights=weight.ravel(), minlength=len(out))
    _finite(out, 'recomputed B1', nonnegative=True)
    old = arrays['shell_integrals'][:, 1]
    need(not np.any((old == 0) != (out == 0)), C_INPUT, 'B1 zero support mismatch')
    relative = np.abs(out - old) / np.maximum(np.maximum(out, old), np.finfo(float).tiny)
    need(not np.max(relative) > B1_RELATIVE_CHECK, C_INPUT, 'stored B1 does not reproduce from saved source factors')
    return edges, np.maximum(old, out), dict(max_relative_difference=float(np.max(relative)),
                                             arithmetic='max(stored B1, recomputed B1); summation-order check 1e-10')


# ------------------------------------------------------------------------------------------------ S4 aggregation
def aggregate(rho_shells, edges, B1, rows):
    """S4 + lo_core L142-175 arithmetic. rows: [{'id','status','v','R','t'}] for every row; a row enters the arithmetic
    when its status is INCLUDED or MISSING with a recorded (lower-bound) speed and its t is finite and > 0."""
    import numpy as np
    edges = _finite(edges, 'edges', positive=True)
    B1 = _finite(B1, 'B1', nonnegative=True)
    need(edges.ndim == 1 and B1.shape == (len(edges) - 1,) and np.all(np.diff(edges) > 0), C_INPUT, 'B1 shell dimensions')
    calc = [r for r in rows if r['status'] in (ROW_INCLUDED, ROW_MISSING) and r['v'] is not None
            and _num(r['t']) and r['t'] > 0]
    idx = [r['id'] for r in calc]
    v = np.asarray([r['v'] for r in calc], float)
    R = np.asarray([r['R'] for r in calc], float)
    t = np.asarray([r['t'] for r in calc], float)
    _finite(v, 'speeds', nonnegative=True)
    _finite(R, 'R', positive=True)
    _finite(t, 't', positive=True)
    e_top = float(edges[-1])
    used = np.zeros(len(B1), dtype=bool)
    shells, problem = [], None
    for sh in rho_shells:
        lo, hi = (float(x) for x in sh['range_inverse_kpc'])
        rho = float(sh['rho_used'])
        if hi <= e_top:
            take = (edges[:-1] >= lo) & (edges[1:] <= hi)
            if not take.any() or edges[:-1][take][0] != lo or edges[1:][take][-1] != hi:
                problem = 'B1_DOES_NOT_TILE_RHO_SHELL (%g,%g]' % (lo, hi)
                break
            dom = DOMAIN_TILED
        elif lo < e_top:
            take = (edges[:-1] >= lo) & (edges[1:] <= e_top)
            if not take.any() or edges[:-1][take][0] != lo or edges[1:][take][-1] != e_top:
                problem = 'B1_DOES_NOT_TILE_(lo,E_top] (%g,%g]' % (lo, e_top)
                break
            dom = DOMAIN_PARTIAL
        else:
            take = np.zeros(len(B1), dtype=bool)
            dom = DOMAIN_OUT
        if used[take].any():
            problem = 'DUPLICATE_LO_SHELL_CONSUMPTION'
            break
        used |= take
        if dom == DOMAIN_OUT:
            b1 = 0.0
            d = np.zeros(len(calc))
            ratios = np.zeros(len(calc))
        else:
            b1 = float(B1[take].sum())
            d = v * R * rho * b1 / 4
            ratios = v * R * rho * b1 / (4 * t)                       # lo_core L165, tau -> t_i
        _finite(ratios, 'LO ratios', nonnegative=True)
        shells.append(dict(range_inverse_kpc=[lo, hi], rho_used=rho, B1_per_m=b1, domain=dom,
                           per_row_d_km_s=d.tolist(), per_row_over_t=ratios.tolist(),
                           max_over_t=float(ratios.max()) if len(calc) else 0.0,
                           row_argmax=idx[int(np.argmax(ratios))] if len(calc) and dom != DOMAIN_OUT else None))
    unconsumed = bool(np.any(~used & (B1 != 0)))
    above = bool(np.any((edges[1:] > TOP_INVERSE_KPC) & (B1 != 0)))
    if problem is None and (unconsumed or above):
        problem = 'NONZERO_B1_ABOVE_91' if above else 'NONZERO_B1_OUTSIDE_EXACTLY_ONE_RHO_SHELL'
    total = float(sum(s['max_over_t'] for s in shells))
    fail = any(s['max_over_t'] > PER_SHELL_MAX for s in shells) or total > SUMMED_MAX       # lo_core L171, negated
    flags = {'E_top_inverse_kpc': e_top, 'shell_domains': [[s['range_inverse_kpc'], s['domain']] for s in shells],
             'all_nonzero_B1_consumed': not unconsumed, 'nonzero_B1_above_91': above, 'tiling_problem': problem}
    return {'shells': shells, 'G': total, 'rows_in_arithmetic': idx, 'coverage_problem': problem,
            'fail_on_present': bool(fail), 'coverage_flags': flags}


def decide(agg, rows):
    """Verdict from the aggregate and the row statuses (monotone-FAIL rule, A48 last sentence)."""
    missing_v = [r['id'] for r in rows if r['status'] == ROW_MISSING]
    missing_t = [r['id'] for r in rows if r['status'] in (ROW_INCLUDED, ROW_MISSING) and not (_num(r['t']) and r['t'] > 0)]
    if agg['coverage_problem'] is not None:
        return 'UNAVAILABLE', [C_COVERAGE], False
    if agg['fail_on_present']:
        return 'FAIL', [], bool(missing_v or missing_t)
    codes = ([C_READOUT] if missing_v else []) + ([C_TOL] if missing_t else [])
    return ('UNAVAILABLE', codes, False) if codes else ('PASS', [], False)


# ------------------------------------------------------------------------------------------------ records
def guard_state_record(rec):
    """Refuses any NGC LO record without the scope text, a FAIL without the FAIL text, or an anchor emission."""
    need(isinstance(rec, dict) and rec.get('schema') == STATE_RECORD_SCHEMA, C_ADMISSION, 'STATE_RECORD_SCHEMA')
    need(rec.get('scope_disclosure') == SCOPE_DISCLOSURE, C_ADMISSION, 'NGC_LO_RECORD_WITHOUT_THE_A153_SCOPE_TEXT')
    need(rec.get('is_anchor') is False and 'ANCHOR' not in str(rec.get('reading')).upper()
         and 'ANCHOR' not in str(rec.get('state_class')).upper(), C_ADMISSION, 'ANCHOR_CLASS_EMITTED (NGC has no anchor class)')
    need(rec.get('verdict') in ('PASS', 'FAIL', 'UNAVAILABLE'), C_ADMISSION, 'STATE_VERDICT')
    if rec['verdict'] == 'FAIL':
        need(rec.get('fail_text') == FAIL_TEXT, C_ADMISSION, 'FAIL_RECORD_WITHOUT_THE_FAIL_TEXT')
        need(rec.get('reading') in (R_NLTM, R_TRANSIENT, R_CLASS_GAP), C_ADMISSION, 'FAIL_READING')
    if rec['verdict'] == 'PASS':
        need(rec.get('codes') == [] and rec.get('reading') == R_PASS, C_ADMISSION, 'PASS_WITH_CODES')
    if rec['verdict'] == 'UNAVAILABLE':
        need(rec.get('reading') == 'UNAVAILABLE' and rec.get('codes'), C_ADMISSION, 'UNAVAILABLE_WITHOUT_CODE')
    return rec


def write_state_record(rec, out_root):
    guard_state_record(rec)
    return write_new(out_root, 'NGC_LO_STATE_%s.json' % digest(rec['state'])[:24], rec)


def state_reading(verdict, cls):
    if verdict == 'PASS':
        return R_PASS
    if verdict == 'FAIL':
        return {ACCEPTED: R_NLTM, INHERITED: R_NLTM, ROUTE_B: R_NLTM, ITERATE: R_TRANSIENT}.get(cls, R_CLASS_GAP)
    return 'UNAVAILABLE'


def call_reading(states):
    """A134 Q5 / 0690 OPEN-6 (c3v003 B3), no anchor: a FAIL at an accepted, inherited or route-B state is decisive even
    with other states UNAVAILABLE; LO_UNCERTIFIED_TRANSIENT needs every non-iterate state at PASS; else INCOMPLETE."""
    fails = [s for s in states if s['verdict'] == 'FAIL']
    unav = [s for s in states if s['verdict'] == 'UNAVAILABLE']
    out = {'class_reading': None}
    if not states:
        out['reading'] = R_INCOMPLETE
        return out
    if not fails:
        out['reading'] = R_PASS if not unav else R_INCOMPLETE
        return out
    classes = {s['state_class'] for s in fails}
    if classes & set(DECISIVE_CLASSES):
        cr = R_NLTM
    elif CLASS_UNAVAILABLE in classes:
        cr = R_CLASS_GAP
    elif classes == {ITERATE} and all(s['verdict'] == 'PASS' for s in states if s['state_class'] != ITERATE):
        cr = R_TRANSIENT
    else:
        cr = R_INCOMPLETE
    out['class_reading'] = cr
    out['reading'] = cr if cr in (R_NLTM, R_TRANSIENT) else R_INCOMPLETE
    return out


def _base_record(cls_info, call):
    return {'schema': STATE_RECORD_SCHEMA, 'registry_kind': call['registry']['kind'], 'utc': call['env'].utc(),
            'route': ROUTE, 'producer': call['me'], 'root_rulings': call['rulings'], 't_rule_id': call['rule_id'],
            'state': cls_info['state'], 'state_class': cls_info['class'], 'roles': cls_info['roles'],
            'stages': cls_info['stages'], 'call_result': call['result_pin'], 'point_sha256': call.get('point_sha256'),
            'custody_sha256': call.get('custody_sha256'), 'row_contract': call.get('row_contract_pin'),
            'row_policy_review': call.get('review_pin'), 'slot_proof': call.get('slot_proof_pin'),
            'status': 'UNTESTED', 'verdict': 'UNAVAILABLE', 'reading': 'UNAVAILABLE', 'codes': [], 'detail': [],
            'is_anchor': False, 'scope_disclosure': SCOPE_DISCLOSURE, 'blinding': BLINDING,
            'thresholds': {'per_shell_max_over_t': PER_SHELL_MAX, 'summed_over_t': SUMMED_MAX,
                           'source': 'lo_core L170-171; A136 G5; LO_NGC_K32_CERT_V001 numbers (A153)'}}


def _one_state(cls_info, call, *, out_root):
    env = call['env']
    rec = _base_record(cls_info, call)
    state = cls_info['state']
    try:
        if call.get('call_code'):
            raise Refusal(call['call_code'], call.get('call_detail', ''))
        need(cls_info['class'] != CLASS_UNAVAILABLE, C_CLASS, 'Q5 class unavailable from the inventory')
        ref = (call['state_inputs'] or {}).get(state['state_sha256'])
        need(is_pin(ref), C_INPUT, 'STATE_INPUT_MISSING')
        obj = strict_json(env.read_raw(ref, C_INPUT, 'state input'), 'state input')
        need(isinstance(obj, dict) and obj.get('schema') == STATE_INPUT_SCHEMA and obj.get('state') == state, C_INPUT,
             'STATE_INPUT_SCHEMA_OR_STATE')
        need(obj.get('call_result') == call['result_pin'], C_INPUT, 'STATE_INPUT_NOT_THIS_CALL')
        tail = obj.get('tail_state')
        need(isinstance(tail, dict) and set(tail) == {'record', 'arrays'} and is_pin(tail['record'])
             and is_pin(tail['arrays']), C_INPUT, 'STATE_INPUT_TAIL_STATE_PINS')
        record = strict_json(env.read_raw(tail['record'], C_INPUT, 'tail state record'), 'tail state record')
        need(isinstance(record, dict), C_INPUT, 'TAIL_RECORD_NOT_AN_OBJECT')
        if state['state_sha256'] == call['accepted']:                   # S5: the accepted route-A state
            need(obj.get('source') == 'ROUTE_A_TAIL_MANIFEST', C_INPUT, 'ACCEPTED_STATE_NOT_FROM_THE_MANIFEST')
            need(tail['arrays'] == call['manifest_state']['arrays'] and record == call['manifest_state']['record'], C_INPUT,
                 'ACCEPTED_STATE_NOT_THE_MANIFEST_ARRAYS (S5, manifest L169)')
        else:                                                           # S5: post-run rebuild export (interface)
            prod = obj.get('producer')
            need(obj.get('source') == 'POST_RUN_REBUILD' and is_pin(prod)
                 and prod['sha256'] in set(call['approved_rebuild']), C_INPUT,
                 'REBUILD_EXPORT_PRODUCER_NOT_APPROVED (open interface: NGC rebuild-and-export successor)')
            env.read_raw(prod, C_INPUT, 'rebuild producer')
        import numpy as np
        raw = env.read_raw(tail['arrays'], C_INPUT, 'tail state arrays')
        with np.load(io.BytesIO(raw), allow_pickle=False) as z:
            arrays = {k: z[k].copy() for k in z.files}
        U = env.lib()
        try:
            U.TailState.from_arrays(arrays, record, expected_digest=state['state_sha256'])
        except U.Refusal as exc:
            raise Refusal(C_INPUT, 'TAILSTATE_DIGEST_NOT_THE_RECORDED_DIGEST (S5): %s' % exc)
        need(record.get('roster_digest') == state['source_sha256'] and record.get('stage_kind') == state['stage_kind'],
             C_INPUT, 'STATE_RECORD_SOURCE_OR_STAGE_MISMATCH')
        need(isinstance(record.get('i1t'), dict) and record['i1t'].get('verdict') == 'PASS', C_INPUT,
             'I1T_NOT_ESTABLISHED (lo_core L250)')
        need(record.get('lo_certificate') == call['registry']['launch'], C_CUSTODY, 'STATE_NOT_RUN_UNDER_THE_LAUNCH_PIN')
        for claim in cls_info.get('kept_claims') or []:
            need(claim is None or claim == KEPT, C_GEOMETRY, 'INVENTORY_KEPT_CLAIM_NOT_CUBE_2')
        check_state_geometry(record, arrays)                            # S3
        need(record.get('outer') == call['point']['uv']['outer'], C_GEOMETRY, 'STATE_OUTER_NOT_THE_SPEC_OUTER')
        need(record.get('c_m_s') == C_M_S and record.get('lambda_scale') == call['point']['uv']['lambda_scale'], C_GEOMETRY,
             'saved state physical prefactor mismatch (lo_core L216)')
        g = record.get('gamma_eff')
        need(_num(g) and g > 0, C_GAMMA, 'STATE_GAMMA_MISSING')
        routes = dict(call['point']['gamma_routes'], state_gamma_eff_hex=hexf(g))
        rec['gamma_c4b'] = dict(routes, bits_equal=len(set(routes.values())) == 1)
        need(rec['gamma_c4b']['bits_equal'], C_GAMMA, 'state / spec route / theta route gamma bits differ (0216 N1)')
        edges, B1, b1check = recompute_b1(arrays, record, U)            # S5 + lo_core L109-139
        rec['B1_recomputed'] = b1check
        rho = env.rho_recompute(call['spec_ref'], call['point']['key'])   # S2: the approved producer, registered
        check_rho_record(rho, call['point'], call['rho']['rho_producer'], allow_synthetic=call['registry']['kind'] != 'REGISTERED')
        rec['rho_bitwise_equal_to_slot'] = rho_bitwise_canonical(rho) == call['rho']['slot_canonical']
        need(rec['rho_bitwise_equal_to_slot'], C_RHO, 'RECOMPUTE_NOT_10_KEY_EQUAL_TO_THE_SLOT_RHO (A138 V03)')
        rec['rho'] = {'slot_rho': call['rho']['slot_rho_pin'], 'canonical_sha256': call['rho']['slot_canonical_sha256'],
                      'rho_producer': call['rho']['rho_producer']}
        agg = aggregate(call['rho']['shells'], edges, B1, call['rows'])  # S4
        verdict, codes, monotone = decide(agg, call['rows'])
        rec.update(shells=agg['shells'], G=agg['G'], rows_in_arithmetic=agg['rows_in_arithmetic'],
                   coverage_flags=agg['coverage_flags'], monotone_fail_decided=monotone,
                   threshold_failed_observation=agg['fail_on_present'],
                   rows={'policy': SPEED_POLICY, 'rows': call['rows_record']})
        if codes:
            rec['detail'].append('decision: ' + ','.join(codes) + (' (' + agg['coverage_problem'] + ')' if agg['coverage_problem'] else ''))
        rec['verdict'], rec['codes'] = verdict, codes
    except Refusal as exc:
        rec['verdict'], rec['codes'] = 'UNAVAILABLE', [exc.code]
        rec['detail'].append(str(exc))
    except CAUGHT as exc:
        rec['verdict'], rec['codes'] = 'UNAVAILABLE', [C_INPUT]
        rec['detail'].append('%s: %s' % (type(exc).__name__, exc))
    rec['reading'] = state_reading(rec['verdict'], cls_info['class'])
    rec['status'] = 'TESTED' if rec['verdict'] in ('PASS', 'FAIL') else 'UNTESTED'
    if rec['verdict'] == 'FAIL':
        rec['fail_text'] = FAIL_TEXT
    entry = {'state': state, 'state_class': cls_info['class'], 'verdict': rec['verdict'], 'reading': rec['reading'],
             'codes': list(rec['codes']), 'coverage_flags': rec.get('coverage_flags'), 'record': None}
    try:
        entry['record'] = write_state_record(rec, out_root)
    except (Refusal, OSError) as exc:
        entry.update(verdict='UNAVAILABLE', reading='UNAVAILABLE', codes=[C_ADMISSION],
                     record_error='STATE_RECORD_NOT_WRITTEN: %s' % exc)
    return entry


# ------------------------------------------------------------------------------------------------ call level
def _inventory(inventory, result_pin, env):
    need(isinstance(inventory, dict) and inventory.get('schema') == INVENTORY_SCHEMA, C_ADMISSION, 'INVENTORY_SCHEMA')
    prod = inventory.get('producer')
    need(is_pin(prod) and prod['sha256'] == ENUMERATOR[1], C_ADMISSION, 'INVENTORY_PRODUCER_NOT_THE_PINNED_ENUMERATOR')
    env.read_raw(prod, C_ADMISSION, 'enumerator')
    need(inventory.get('call_result') == result_pin, C_ADMISSION, 'INVENTORY_NOT_THIS_CALL')
    need(inventory.get('complete') is True and not inventory.get('blockers'), C_ADMISSION,
         'COMPLETE_CONSUMED_STATE_INVENTORY_REQUIRED: %s' % inventory.get('blockers'))
    states = inventory.get('states')
    need(isinstance(states, list) and states and all(isinstance(s, dict) and set(s) == {'state_sha256', 'source_sha256',
                                                                                          'stage_kind'} for s in states)
         and len({digest(s) for s in states}) == len(states), C_ADMISSION, 'INVENTORY_STATES')
    E = env.enumerator()
    occ = [{k: o[k] for k in ('role', 'stage', 'state')} for o in inventory.get('occurrences') or []]
    classes = E.classify(occ, inventory.get('accepted_state_sha256'), states)
    need(classes == inventory.get('classes'), C_ADMISSION, 'INVENTORY_CLASSES_DO_NOT_RE_DERIVE')
    for c in classes:
        c['kept_claims'] = [o.get('kept_claim') for o in inventory['occurrences'] if o['state'] == c['state']]
    return classes


def _adapt_call(*, call_dir, spec_ref, inventory, state_inputs, row_contract_ref, row_policy_review_ref, slot_proof_ref,
                approved_producer_sha256, approved_slot_proof_producer_sha256, approved_rho_producer_sha256,
                approved_rebuild_producer_sha256, trusted_row_policy_review_sha256, out_root, env):
    registry = env.registry
    rec = {'schema': CALL_SCHEMA, 'registry_kind': registry.get('kind') if isinstance(registry, dict) else None,
           'utc': env.utc(), 'route': ROUTE, 'call_lo_reading': R_INCOMPLETE, 'class_reading': None, 'blockers': [],
           'states': [], 'lo_rows_for_acceptance': [], 'is_anchor': False, 'scope_disclosure': SCOPE_DISCLOSURE,
           'blinding': BLINDING, 'speed_reference_policy': SPEED_POLICY}
    try:
        check_registry(registry)
        rec['root_rulings'] = rulings = root_gate(registry, env.read_raw)
        me = env.self_pin()
        need(isinstance(approved_producer_sha256, (list, tuple, set, frozenset)) and me['sha256'] in set(approved_producer_sha256),
             C_ADMISSION, 'NGC_LO_ADAPTER_NOT_APPROVED (root approved list; review first)')
        rec['producer'] = me
        call = os.path.realpath(str(call_dir))
        out = os.path.realpath(os.path.join(call, 'out'))
        rp = os.path.join(out, 'result.json')
        with open(rp, 'rb') as f:
            rraw = f.read()
        result_pin = {'path': rp, 'sha256': hashlib.sha256(rraw).hexdigest()}
        result = strict_json(rraw, 'result.json', C_ADMISSION)
        rec['call_result'] = result_pin
        classes = _inventory(inventory, result_pin, env)
        rec['inventory_digest'] = digest(inventory)
        rec['accepted_state_sha256'] = inventory['accepted_state_sha256']
        ctx = {'env': env, 'registry': registry, 'me': me, 'rulings': rulings, 'rule_id': t_rule_id(registry),
               'result_pin': result_pin, 'state_inputs': state_inputs, 'accepted': inventory['accepted_state_sha256'],
               'approved_rebuild': list(approved_rebuild_producer_sha256 or ()), 'spec_ref': spec_ref}
        rec['t_rule_id'] = ctx['rule_id']
        rec['t_i_declared'] = ctx['rule_id'] is not None
        rec['blas_thread_env'] = {k: os.environ.get(k) for k in THREAD_ENV}
        # ---- freeze before pin: nothing numeric before root's t_i entry
        if ctx['rule_id'] is None:
            ctx.update(call_code=C_TOL, call_detail='no root t_i entry is pinned (A153: t_i still to be declared)')
        if not ctx.get('call_code'):
            try:
                ctx['point'] = point = point_custody(spec_ref, result, registry, env.read_raw)
                ctx.update(point_sha256=point['point_sha256'], custody_sha256=point['custody_sha256'])
                rec.update(point_sha256=point['point_sha256'], custody_sha256=point['custody_sha256'])
                contract, csha, t_ok = check_row_contract(row_contract_ref, registry, env.read_raw, point, result_pin,
                                                          ctx['rule_id'])
                ctx['row_contract_pin'] = rec['row_contract'] = dict(row_contract_ref)
                if not t_ok:
                    raise Refusal(C_TOL, 't_i absent from the row contract or not bound to root\'s entry %s' % ctx['rule_id'])
                ctx['review_pin'] = rec['row_policy_review'] = check_review(row_policy_review_ref,
                                                                            trusted_row_policy_review_sha256, csha, env.read_raw)
                ctx['rho'] = check_slot_proof(slot_proof_ref, point, registry, env.read_raw,
                                              approved_slot=approved_slot_proof_producer_sha256 or (),
                                              approved_rho=approved_rho_producer_sha256 or (),
                                              allow_synthetic=registry['kind'] != 'REGISTERED')
                need(env.rho_producer_pin == ctx['rho']['rho_producer'], C_RHO, 'RECOMPUTE_PRODUCER_IS_NOT_THE_PROOF_PRODUCER')
                ctx['slot_proof_pin'] = rec['slot_proof'] = dict(slot_proof_ref)
                man = strict_json(env.read_raw(inventory['manifest'], C_INPUT, 'route-A tail manifest'), 'manifest')
                ctx['manifest_state'] = man['state']
                ids = contract['query_ids']
                ro = own_call_readouts(result, ids)                     # S6 (speeds read only now)
                if ro['call_problem']:
                    raise Refusal(C_READOUT, ro['call_problem'])
                radii, cm_pin = own_call_radii(result, out, env.read_raw)   # S7
                rows, rows_record = [], []
                for i, q in enumerate(ids):
                    r = ro['rows'][i]
                    own = radii.get(q)
                    if r['status'] != ROW_EXCLUDED or own is not None:
                        need(own is not None and bits(own) == bits(contract['R_m'][i]), C_CONTRACT,
                             'R_i_NOT_THE_CALL_OWN_QUERY_SUPPORT_RADIUS (S7) ' + q)
                    t = contract['t_km_s'][i]
                    rows.append({'id': q, 'status': r['status'], 'v': r['v'], 'R': float(contract['R_m'][i]),
                                 't': t if (_num(t) and t > 0) else None})
                    rows_record.append({'id': q, 'status': r['status'], 'v_reference_km_s': r['v'],
                                        'R_m': float(contract['R_m'][i]), 't_km_s': t, 'reason': r['reason']})
                ctx['rows'], ctx['rows_record'] = rows, rows_record
                rec['readout_diagnostic'] = ro['diagnostic']
                rec['column_mean'] = cm_pin
                rec['row_statuses'] = {s: sum(1 for r in rows if r['status'] == s) for s in (ROW_INCLUDED, ROW_EXCLUDED, ROW_MISSING)}
            except Refusal as exc:
                ctx.update(call_code=exc.code, call_detail=str(exc))
                rec['blockers'].append(str(exc))
        for info in classes:
            rec['states'].append(_one_state(info, ctx, out_root=out_root))
        cr = call_reading(rec['states'])
        rec['call_lo_reading'], rec['class_reading'] = cr['reading'], cr['class_reading']
        rec['lo_rows_for_acceptance'] = [{'state': s['state'], 'LO': s['record']} for s in rec['states'] if s['verdict'] == 'PASS']
        rec['transient_candidate_unconfirmed'] = [s['state'] for s in rec['states'] if s['reading'] == R_TRANSIENT] \
            if cr['reading'] != R_TRANSIENT else []
    except Refusal as exc:
        rec['blockers'].append(str(exc))
        rec['call_lo_reading'] = R_INCOMPLETE
    except CAUGHT as exc:
        rec['blockers'].append('%s: %s' % (type(exc).__name__, exc))
        rec['call_lo_reading'] = R_INCOMPLETE
    rec['lo_gate_passed_all_states'] = rec['call_lo_reading'] == R_PASS
    return rec


def make_env(registry, *, rho_producer_ref=None, approved_rho_producer_sha256=()):
    """The adapter's environment. The rho recompute loads root's approved NGC producer by exact bytes and calls its
    produce(spec_ref, theta_key) (Claude3 ngc_rho_producer_c3v001 signature) at registered settings."""
    check_registry(registry)
    read_raw = make_reader(registry)
    state = {}

    def lib():
        if 'U' not in state:
            state['U'] = load_exact(LIBRARY[0], LIBRARY[1], 'ngc_lo_c2v001_owned_uv_tail_lapse_v002', C_INPUT)
        return state['U']

    def enumerator():
        if 'E' not in state:
            state['E'] = load_exact(ENUMERATOR[0], ENUMERATOR[1], 'ngc_lo_c2v001_consumed_states', C_ADMISSION)
        return state['E']

    def rho_recompute(spec_ref, key):
        need(is_pin(rho_producer_ref) and rho_producer_ref['sha256'] in set(approved_rho_producer_sha256 or ())
             and rho_producer_ref['sha256'] != DDO_RESPONSE_SHA, C_RHO, 'RHO_PRODUCER_NOT_APPROVED')
        need(all(os.environ.get(k) == '1' for k in THREAD_ENV), C_RHO,
             'BLAS_NOT_SINGLE_THREAD (set the six thread variables to 1 before numpy loads; the handoff CLI does)')
        if 'P' not in state:
            state['P'] = load_exact(os.path.realpath(rho_producer_ref['path']), rho_producer_ref['sha256'],
                                    'ngc_lo_c2v001_rho_producer', C_RHO)
        try:
            return state['P'].produce(spec_ref, key)
        except Exception as exc:     # the producer's own refusal class is not ours: a structured mismatch, never a crash
            raise Refusal(C_RHO, 'RHO_RECOMPUTE_REFUSED: %s: %s' % (type(exc).__name__, exc))

    return types.SimpleNamespace(registry=registry, read_raw=read_raw, self_pin=self_pin, utc=utc, lib=lib,
                                 enumerator=enumerator, rho_recompute=rho_recompute,
                                 rho_producer_pin=dict(rho_producer_ref) if is_pin(rho_producer_ref) else None)


def adapt_call_ngc_lo(*, call_dir, spec_ref, inventory, state_inputs, row_contract_ref=None, row_policy_review_ref=None,
                      slot_proof_ref=None, rho_producer_ref=None, approved_producer_sha256=(),
                      approved_slot_proof_producer_sha256=(), approved_rho_producer_sha256=(),
                      approved_rebuild_producer_sha256=(), trusted_row_policy_review_sha256=(), out_root):
    """Public entry (root operates it through the NGC handoff): the REGISTERED registry only."""
    try:
        env = make_env(real_registry(), rho_producer_ref=rho_producer_ref,
                       approved_rho_producer_sha256=approved_rho_producer_sha256)
    except (Refusal,) + CAUGHT as exc:
        return {'schema': CALL_SCHEMA, 'registry_kind': 'REGISTERED', 'utc': utc(), 'route': ROUTE,
                'call_lo_reading': R_INCOMPLETE, 'blockers': [str(exc)], 'states': [], 'is_anchor': False,
                'scope_disclosure': SCOPE_DISCLOSURE, 'lo_gate_passed_all_states': False}
    return _adapt_call(call_dir=call_dir, spec_ref=spec_ref, inventory=inventory, state_inputs=state_inputs,
                       row_contract_ref=row_contract_ref, row_policy_review_ref=row_policy_review_ref,
                       slot_proof_ref=slot_proof_ref, approved_producer_sha256=approved_producer_sha256,
                       approved_slot_proof_producer_sha256=approved_slot_proof_producer_sha256,
                       approved_rho_producer_sha256=approved_rho_producer_sha256,
                       approved_rebuild_producer_sha256=approved_rebuild_producer_sha256,
                       trusted_row_policy_review_sha256=trusted_row_policy_review_sha256, out_root=out_root, env=env)
