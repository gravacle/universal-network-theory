"""NGC LO slot proof c3v003 (Claude3 lane; root A136 G3-G5, FROM_CODEX/0698; 0717 R4/R5; A153 0723; A155 0728 + 0729;
A167 0741; NGC_RHO_INTERFACE_C3V001 sections 3-5; CHANGES_C3V003).  The successor of ngc_lo_slot_proof_c3v002 (fbdcaacd)
by E1 + E2 (A167 gamma route; W1), E3 (W6), E5 (schemas), E6 (0741 in the root gate; W12 texts) and E8 (W2) only.

A separate module with its own constants; it widens nothing of the DDO slot proof (lo_slot_proof_c3v003, cd10cd59).

What it binds.  The NGC launch carries LO_NGC_K32_CERT_V001 (07745bbf) in numerics.uv_tail.lo_certificate as a custody
pin: cx3r008 L1076-1086 / L5270-5280 only verify_pin it and L1105 / L5299 pass it to route A; the tail library
(2026f2b6) L664-674 re-hashes it and L687 records it (A136: no numeric use).  So this proof serves POST-RUN acceptance:
  1. root gate: the A136, A134 (text of record and 0688), A146, 0717, A153 (0723), A155 (0728, 0729), 0730 and A167
     (0741) pins,
     whole-dict, bytes re-read, before anything else;
  2. this module's own sha is in the caller's approved list;
  3. the rho record is an exact pin in root's registered list (whole dict);
  4. D1 (0717 R4): the spec's numerics.route_a.column_workers must be exactly int 1: the cw8 twin gets no rho record
     (NGC_RHO_TWIN_GETS_NO_RECORD); the spec's lo_certificate slot is the launch pin (whole dict; bytes re-read);
  5. custody is derived independently from bytes by the approved producer's pure derive_point() (G3: driver cx3r008,
     the S0 theta key, the spec sha, route_a.column_workers inside), and the record's identity, point_sha256 and custody
     must equal it whole;
  6. the rho record is the approved producer's full registered record (schema, gate, settings, coverage [2, 91], the
     9-shell partition, finite rho_used); the producer's bytes are re-read; a test-symbol record is refused; D3 with E1
     and E2 (A167 0741; W1): the record must carry theta_binding.theta_route_gamma_eff_bits_equal (the theta route
     (s*ge)*EB against the bound spec route s*(ge*EB)) EQUAL to this proof's own derive_point value, and its bound
     gamma_eff (float and hex) equal to derive_point's bitwise; both are surfaced as theta_route_diagnostic (a false
     flag is shown, never refused; root's adapter C4b compares the state's gamma_eff with the bound one bitwise);
  7. G4: two registered records of that producer at the S0 seed key, distinct by sha and path, each with custody
     route_a_column_workers exactly int 1 (E8, W2: the cw8 twin is never a member), equal in identity and
     custody, must be equal under wrapper v002's 10-key canonical comparison (7a6af535 L177-179, L189-191; A138 V03);
     at the seed's own slot the slot rho must equal the pair the same way.  The projection (partition + bits of
     rho_used) is a recorded diagnostic only;
  8. G5: route NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE; the certificate's registered thresholds read from its
     producer's bytes (lo_ngc_k32_cert_c2v001 4dfbb1aa L102), with the compared quantity a NAMED INPUT (D2: A153 0723,
     A155 0728 + E_A155_1 0729: NGC_PER_STATE_LO_INDICATOR_G_S, evaluated by root's NGC per-state adapter, never here; its
     definition is re-checked against the pinned dispatch bytes); the A134 Q5 readings (56774ba7 L126-133) and the 0690
     OPEN-4/6 and OPEN-5 confirmations, NGC having no anchor class (D4, A153); the A153 scope disclosure, verbatim from
     0723 and re-checked from its bytes (D5).
The proof certifies NO LO (lo_certified false) and NEVER carries covers_all_consumed_states; a rho record carrying it
is refused.  No rho, LO or per-state number is computed here.
Usage (root): taskpolicy -b python3 -I -B ngc_lo_slot_proof_c3v003.py --args <json> --args-sha256 <sha> --out-root <dir>
"""
import datetime
import hashlib
import importlib.util
import json
import math
import os
import struct
import sys
import types

HERE = os.path.dirname(os.path.realpath(__file__))
PRODUCER = (os.path.join(HERE, 'ngc_rho_producer_c3v003.py'), 'd3d0f3ddda8be2e3d4b0e0732e5237a602cb3b1fb99d7921e8c10a886420a3c4')
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
NGCK = ART + '/tail_scheme_impl_c2/certificates_ngc_k32'
CERT_PRODUCER = {'path': NGCK + '/tools/lo_ngc_k32_cert_c2v001.py',
                 'sha256': '4dfbb1aa9a36dce67dd87bc55eafd897095bca3c014f89d2bb9dc171ce6e6be4'}
THRESHOLD_LINE = (102, 'ok = max(vals) <= 0.005 and sum(vals) <= 0.05')
FROM_CODEX = '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX'
DISPATCH = {   # A153 (0723) and A155 (0728; E_A155_1 0729): the dispatches defining the compared quantity (sha from bytes)
    '0723': {'path': FROM_CODEX + '/0723_2026-10-19_A153_ngc_lo_quantity.md',
             'sha256': 'b8f95c9cf4d4337cd3c7c526fbfdb71a85e7a3f0f174bea163adbdcc2c6a3df0'},
    '0728': {'path': FROM_CODEX + '/0728_2026-10-19_A155_ngc_lo_ti_declared_codex1_check.md',
             'sha256': '87e7ca3cd205bcb515206668bd0ce02c45d368c8e09a5d633f5ea3bda8686952'},
    '0729': {'path': FROM_CODEX + '/0729_2026-10-19_A155_amended_E_A155_1.md',
             'sha256': '8d220ecc62baa9f9c480f7481c4205475d2aad21e6fe5a6d1d1c6eebcc9ce502'}}
COMPARED_QUANTITY = {   # D2 (0717 R5 N2; A153 0723; A155 0728 + E_A155_1 0729): a NAMED INPUT; nothing is evaluated here
    'name': 'NGC_PER_STATE_LO_INDICATOR_G_S',
    'defined_by': [dict(DISPATCH[k]) for k in ('0723', '0728', '0729')],
    'definition': [   # transcribed from the pinned bytes, verbatim up to markdown ** emphasis; re-checked from bytes per proof
        {'dispatch': '0723', 'text': ('Per-state quantity: the A134 readout indicator d_i,s = |v_i| R_i \u03c1_s B1_s / 4, with '
                                      'g_s = max_i d_i,s / t_i \u2264 0.005 per shell and \u03a3 \u2264 0.05.')},
        {'dispatch': '0723', 'text': 'Scope: all consumed states.'},
        {'dispatch': '0728', 'text': ('g_s = max_i (|v_i|\xb71e3)\xb2 \xb7 R_i \xb7 \u03c1_s \xb7 B1_s / (2c\xb2\u03b8) '
                                      '\u2264 0.005 per shell, with \u03a3 \u2264 0.05.')},
        {'dispatch': '0728', 'text': 'This is the lo_core L165 numerator divided by t_i = c\xb2\u03b8/(2|v_i|).'},
        {'dispatch': '0728', 'text': ('\u03b8 = log1p(h0/c\xb2), the HI free-boundary threshold, with \u03c30 = 11 km/s and '
                                      '\u0393 = 5/3.')},
        {'dispatch': '0728', 'text': 'P-1 reads TARGET_FREE, recorded from bytes.'},
        {'dispatch': '0728', 'text': 'The row contract carries no t_i, no velocity and no \u03c3.'},
        {'dispatch': '0729', 'text': ('R G\u2032 = 1 is a declared approximation, and the O(h) wording is withdrawn. A PASS '
                                      'certifies the indicator normalized under that approximation. The real-row remainder '
                                      'stays UNTESTED.')},
        {'dispatch': '0729', 'text': ("t_i is the linearized velocity-response scale under R G\u2032 = 1, not the exact finite "
                                      "change. At |v| = 0 the ratio's 0 is the continuous extension.")},
        {'dispatch': '0729', 'text': 'Unchanged: the formula, inputs, thresholds and contract.'}],
    'evaluated_by': ('the root NGC per-state adapter (claude_artifacts/ngc_acceptance_c2/; A153 s6: S1, S3-S11 and S13 are '
                     'root\'s, S2 (this rho producer, slot proof and stage) is Claude3\'s; 0723 Builds; A155 0728: the '
                     'adapter evaluates the ratio form)'),
    'evaluated_here': False}
THRESHOLDS = {'per_shell_max': 0.005, 'summed': 0.05,
              'units': ('dimensionless: g_s is a fraction of t_i (A153 text 9916cb6f s2 Units; A155 0728 ratio form). '
                        'LO_NGC_K32_CERT_V001 (07745bbf) stays the N-test record and the custody pin; its statistic is not '
                        'the compared quantity (A153, 0723)'),
              'source': 'lo_ngc_k32_cert_c2v001 (4dfbb1aa) L102, re-read from bytes',
              'compared_quantity': COMPARED_QUANTITY}
SCOPE_DISCLOSURE = {   # D5: A153's scope disclosure, on every NGC LO record (0723), verbatim; re-checked from the 0723 bytes
    'text': ("the indicator does not bound the omitted tail's effect on the 43 route-B rows through the source. That effect "
             "is UNTESTED, and its deciding test is the 10-component tail successor."),
    'source': dict(DISPATCH['0723']), 'rule': 'A153 (0723): scope disclosure, on every NGC LO record'}
THETA_ROUTE = {   # D3, E1, E2 (A167, FROM_CODEX/0741; W1): the gamma-route diagnostic and the bound gamma_eff of the record
    'bound_route': ('s*(ge*EB) = s*spec.physical.gamma: the SPEC route (filler ec417e76 L294 order), the gamma_eff the call '
                    'runs at, as DDO (A167, 0741; 0717 R5 N1 is reversed)'),
    'diagnostic_route': '(s*ge)*EB: the theta route (qinf_eval_v001 L146-148; the c3v002 binding), a diagnostic only',
    'rule': ('informational only: a false reading is shown, never refused (0216 N1 is ruled by A167). Root\'s NGC per-state '
             'adapter C4b compares the state\'s gamma_eff with this record\'s bound gamma_eff bitwise, with no tolerance '
             '(A167, 0741; A153 s6 S3 C4b)'),
    'refused_on_false': False,
    'checked_here': ('the record\'s flag and its bound gamma_eff (float and hex) must equal this proof\'s own derive_point '
                     'values, fail-closed (E2, W1)'),
    'source': ('the rho record theta_binding.theta_route_gamma_eff_bits_equal and theta_binding.gamma_eff (outside the 10 '
               'compared keys)')}
TWIN_CODE = 'NGC_RHO_TWIN_GETS_NO_RECORD'
NGC_NO_ANCHOR = 'NGC: no anchor class (A153 0723; A153 text 9916cb6f s3: is_anchor is False at every NGC point)'
READINGS = {   # A134 Q5 readings (S4RC1 text of record 56774ba7 L126-133), recorded verbatim in substance; D4: + 0690 e45c9a6d
    'actual_failure_accepted_inherited_or_route_b_state': 'NON_LAPSE_TAIL_MATERIAL at that point; rows not scored or imputed, '
                                                          'not calibration misses',
    'failure_confined_to_route_a_iterates_before_acceptance': 'LO_UNCERTIFIED_TRANSIENT: fails closed, preserved, no physics content',
    'anchor_failure': 'preserved; step 4 stops for a root ruling | ' + NGC_NO_ANCHOR,
    'high_Q_inf': "NGC's own LO is flagged at any high-Q-inf admitted point",
    'gate_scope': 'ALL_CONSUMED_STATES (registered); acceptance recomputes rho per consumed state and requires bitwise equality '
                  'with the slot rho (10-key canonical)',
    'open_4_route_a_pre_acceptance_iterate': ("The final iteration's monitor-consumed next state, which is never accepted, is "
                                              "ROUTE_A_PRE_ACCEPTANCE_ITERATE. A failure confined there reads "
                                              "LO_UNCERTIFIED_TRANSIENT. [0690 item 3, OPEN-4, confirmed]"),
    'open_6_decisive_fail_and_transient_completeness': (
        'A FAIL at an accepted, inherited or route-B state is decisive (NON_LAPSE_TAIL_MATERIAL) even when other states are '
        'UNAVAILABLE. TRANSIENT needs every non-iterate state at PASS; otherwise the call reads INCOMPLETE, with the iterate '
        'failures recorded. [0690 item 4, OPEN-6, confirmed]'),
    'open_5_anchor_lo_fail': ('Any LO FAIL at the anchor reads the step-4 stop, with the class reading recorded beside it. '
                              '[0690 item 5, OPEN-5, confirmed] | ' + NGC_NO_ANCHOR)}
ROOT_RULINGS = (
    {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0698_2026-10-19_A136_NGC_LO_launch_pin_and_G1-G5.md',
     'sha256': 'daab5f598072adfe146ed97bff8c86859f12e269ca6199072eb30a98918a1f65'},
    {'path': '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/'
             'CLAUDE2/S4RC1_ROOT_RULINGS_DRAFT_WF_C88BB583.md',
     'sha256': '56774ba7a1ad54be89cb1cbb6bd256333de4134ed9ef8a8e949898f7ed8c2c82'},
    {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0688_2026-10-19_A134_S4RC1_LO_route_ruled_owners.md',
     'sha256': 'bcb6df8e9cbd7d01c7c10e4673fb6ca60ecf6c4a439be4db6140ed521689b30d'},
    {'path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CODEX/0712_2026-10-19_A146_errata_selected_rho_gate_open_CP1_early.md',
     'sha256': 'bed3a961edcd06c09d1b538654c00d700eabb8849f52290fd06844493ddf7b64'},
    {'path': FROM_CODEX + '/0717_2026-10-19_claude3_ngc_rho_root_items.md',
     'sha256': '19cddf7b75ffcdff1e23cbfd81f47c0a1ab35d44c7045a6660e95db11946a4ec'},
    dict(DISPATCH['0723']), dict(DISPATCH['0728']), dict(DISPATCH['0729']),
    {'path': FROM_CODEX + '/0730_2026-10-19_claude3_ngc_rho_v2_yes.md',
     'sha256': 'b0c4b62853304d30626cf08ef6748f371fcb78ea3b09e54a65ae01fee29940e7'},
    {'path': FROM_CODEX + '/0741_2026-10-19_claude3_ngc_rho_c3v003_spec_route.md',                       # E6 (A167)
     'sha256': 'b8a9c3fe6da0a955d28cd1b959f47d09b0765129277afe57a24555f0e0da60c6'},
)
RESULT_SCHEMA = 'NGC_LO_SLOT_PROOF_RESULT_C3V003'
PROOF_SCHEMA = 'UNT_NGC_POINT_LO_SLOT_PROOF_C3V003'
GATE = 'NGC_LO_RHO_SLOT'
SLOT_RULE = 'A136_G5_NGC_LO_SLOT_IS_THE_LAUNCH_CUSTODY_PIN_RHO_BOUND_POST_RUN'
LO_ROUTE = 'NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'
READY = 'READY_FOR_POST_RUN_ACCEPTANCE'
FORBIDDEN_KEYS = ('covers_all_consumed_states', 'cover_all_consumed_states')   # A134 Q5
LABEL_PREFIX = 'step5 A_K32_A2_HEADLINE theta_key='


class Refusal(Exception):
    """Fail-closed refusal with a stable code."""


CAUGHT = (Refusal, ValueError, KeyError, TypeError, OSError, OverflowError, AttributeError, IndexError)


def need(ok, code):
    if not ok:
        raise Refusal(code)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def _is_sha(x):
    return isinstance(x, str) and len(x) == 64 and all(c in '0123456789abcdef' for c in x)


def _is_pin(x):
    return isinstance(x, dict) and set(x) == {'path', 'sha256'} and isinstance(x['path'], str) and _is_sha(x['sha256'])


def _in_list(pin, pins):
    return isinstance(pins, (list, tuple)) and any(_is_pin(p) and p == pin for p in pins)


def _ngc3198_named(p):
    """E3 (W6): True when any component string of the path contains 'ngc3198' (case-insensitive); no filesystem call."""
    return any('ngc3198' in part.lower() for part in p.split('/'))


def read_raw(ref):
    """Exact bytes of a {path, sha256} pin: absolute canonical path, no symlink, no NGC3198-named file (0708).  E3 (W6):
    the NGC3198 test runs first, on every path component, before realpath (which lstats every component)."""
    need(_is_pin(ref), 'NOT_AN_EXACT_PIN')
    p = ref['path']
    need(not _ngc3198_named(p), 'NGC3198_NAMED_FILE_REFUSED (0708; any path component, before realpath): ' + p)
    need(os.path.isabs(p) and os.path.realpath(p) == p, 'NONCANONICAL_PATH: ' + p)
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], 'BYTE_PIN_MISMATCH: ' + p)
    return raw


def read_json(ref, label):
    def pairs(items):
        out = {}
        for k, v in items:
            need(k not in out, label + ': DUPLICATE_JSON_KEY')
            out[k] = v
        return out

    def bad(s):
        raise Refusal(label + ': NONFINITE_JSON')
    return json.loads(read_raw(ref), object_pairs_hook=pairs, parse_constant=bad)


def _load_exact(path, sha, name):
    need(isinstance(path, str) and os.path.isabs(path) and os.path.realpath(path) == path, 'NONCANONICAL_MODULE_PATH: ' + str(path))
    with open(path, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == sha, 'MODULE_PIN_MISMATCH: ' + path)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, path, 'exec'), mod.__dict__)
    return mod


def _self_pin():
    p = __file__
    need(isinstance(p, str) and os.path.isabs(p) and os.path.realpath(p) == p, 'NONCANONICAL_PROOF_FILE')
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def bits(x):
    need(type(x) is float and math.isfinite(x), 'RHO_USED_NOT_A_FINITE_FLOAT')
    return struct.pack('<d', x).hex()


def rho_projection(rec):
    """Diagnostic only: [(range, bits(rho_used))] in record order."""
    return [[list(s['range_inverse_kpc']), bits(s['rho_used'])] for s in rec['shells']]


def rho_bitwise_canonical(rec, keys):
    """Wrapper v002's comparison, exactly (7a6af535 L177-179, L189-191): canonical JSON of the 10 keys, absent = None."""
    need(isinstance(rec, dict), 'RHO_RECORD_NOT_AN_OBJECT')
    return canonical({k: rec.get(k) for k in keys})


def _verbatim(reader, ref, text):
    """D2/D5: text must occur in the pinned dispatch's bytes (UTF-8), verbatim up to markdown ** emphasis."""
    src = reader(dict(ref)).decode('utf-8').replace('**', '')
    need(isinstance(text, str) and len(text) > 0 and text in src,
         'TEXT_NOT_VERBATIM_IN_THE_PINNED_DISPATCH: %s: %r' % (ref['path'], str(text)[:60]))


def _route_a_column_workers(spec):
    num = spec.get('numerics') if isinstance(spec, dict) else None
    ra = num.get('route_a') if isinstance(num, dict) else None
    return ra.get('column_workers') if isinstance(ra, dict) else None


def _forbidden_anywhere(obj):
    if isinstance(obj, dict):
        return any(k in FORBIDDEN_KEYS for k in obj) or any(_forbidden_anywhere(v) for v in obj.values())
    if isinstance(obj, list):
        return any(_forbidden_anywhere(v) for v in obj)
    return False


def check_rho_record(rec, env, *, identity=None, custody=None, point_sha256=None):
    """Read-only checks of one NGC rho record of the approved producer (no number is computed)."""
    P = env.P
    need(isinstance(rec, dict), 'RHO_RECORD_NOT_AN_OBJECT')
    need(not _forbidden_anywhere(rec), 'RHO_RECORD_CARRIES_COVERS_ALL_CONSUMED_STATES (A134 Q5)')
    need(rec.get('schema') == P.SCHEMA and rec.get('gate') == P.GATE, 'RHO_SCHEMA_OR_GATE_MISMATCH')
    need(rec.get('status') == 'TESTED' and rec.get('verdict') == P.VERDICT, 'RHO_STATUS_OR_VERDICT_MISMATCH')
    need(rec.get('settings') == P.SETTINGS and rec.get('full_registered_search_executed') is True,
         'RHO_SETTINGS_NOT_REGISTERED_FULL_SEARCH')
    need(rec.get('coverage_complete') is True and rec.get('required_coverage_inverse_kpc') == P.COVERAGE,
         'RHO_COVERAGE_NOT_2_TO_91')
    shells = rec.get('shells')
    need(isinstance(shells, list) and [s.get('range_inverse_kpc') if isinstance(s, dict) else None for s in shells] == P.PARTITION,
         'RHO_PARTITION_NOT_REGISTERED')
    for s in shells:
        need(type(s.get('rho_used')) is float and math.isfinite(s['rho_used']) and s['rho_used'] >= 0, 'RHO_USED_INVALID')
    need(rec.get('producer') == env.producer_pin, 'RHO_PRODUCER_NOT_THE_APPROVED_NGC_PRODUCER')
    try:
        env.read_raw(dict(env.producer_pin))
    except CAUGHT as exc:
        raise Refusal('RHO_PRODUCER_BYTES_NOT_APPROVED (%s: %s)' % (type(exc).__name__, exc))
    idn, cus = rec.get('identity'), rec.get('custody')
    need(isinstance(idn, dict) and isinstance(cus, dict) and rec.get('point_sha256') == digest(idn)
         and cus.get('point_sha256') == rec.get('point_sha256'), 'RHO_IDENTITY_POINT_SHA_INCONSISTENT')
    if not env.allow_synthetic:
        need(cus.get('registry_kind') == P.REGISTRY_REGISTERED and cus.get('symbol_route') == P.SYMBOL_REGISTERED,
             'RHO_RECORD_IS_A_TEST_SYMBOL_RECORD')
    if identity is not None:
        need(idn == identity and cus == custody and rec.get('point_sha256') == point_sha256, 'RHO_POINT_CUSTODY_MISMATCH')
    return rho_projection(rec)


def root_gate(refs, reader):
    refs = list(refs) if isinstance(refs, (list, tuple)) else None
    need(refs is not None and len(refs) == len(ROOT_RULINGS) and all(a == b for a, b in zip(refs, ROOT_RULINGS)),
         'ROOT_RULINGS_NOT_PINNED (A136 0698, A134 56774ba7 + 0688, A146 0712, 0717, A153 0723, A155 0728 + 0729, 0730, '
         'A167 0741, in that order)')
    for ref in refs:
        try:
            reader(dict(ref))
        except CAUGHT as exc:
            raise Refusal('ROOT_RULING_UNREADABLE_OR_CHANGED: %s: %s' % (ref['path'], exc))
    return [dict(r) for r in refs]


def thresholds(reader):
    lines = reader(dict(CERT_PRODUCER)).decode('utf-8').splitlines()
    n, text = THRESHOLD_LINE
    need(len(lines) >= n and lines[n - 1].strip() == text, 'CERTIFICATE_THRESHOLD_LINE_CHANGED L%d' % n)
    cq = json.loads(json.dumps(THRESHOLDS['compared_quantity']))      # D2: a named input, evaluated by root's adapter
    for d in cq['definition']:
        _verbatim(reader, DISPATCH[d['dispatch']], d['text'])
    return dict(THRESHOLDS, compared_quantity=cq, line=n, text=text, producer=dict(CERT_PRODUCER))


def _refuse_forbidden(proof):
    need(not _forbidden_anywhere(proof), 'NGC_LO_SLOT_PROOF_MUST_NOT_CARRY_COVERS_ALL_CONSUMED_STATES (A134 Q5)')


def _prove(spec_ref, rho_ref, *, registered_rho_records, seed_rho_pair, root_ruling_refs, approved_producer_sha256, env):
    out = {'schema': RESULT_SCHEMA, 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'BLOCKED', 'blockers': [],
           'proof': None}
    try:
        out['root_rulings'] = root_gate(root_ruling_refs, env.read_raw)                       # 1
        me = env.self_pin()
        need(isinstance(approved_producer_sha256, (list, tuple, set, frozenset)) and me['sha256'] in set(approved_producer_sha256),
             'NGC_SLOT_PROOF_PRODUCER_NOT_APPROVED (root approved list; review first)')          # 2
        need(_is_pin(rho_ref), 'RHO_REF_NOT_AN_EXACT_PIN')
        need(_in_list(rho_ref, registered_rho_records), 'RHO_NOT_REGISTERED (root registered NGC rho records; whole dict)')  # 3
        need(_is_pin(spec_ref), 'SPEC_REF_NOT_AN_EXACT_PIN')
        spec = read_json(spec_ref, 'spec')
        cw = _route_a_column_workers(spec)                                                       # D1 (0717 R4)
        need(type(cw) is int and cw == 1, TWIN_CODE + ' (0717 R4): numerics.route_a.column_workers is %r, not int 1; the cw8 '
             'twin is never a member and gets no rho record' % (cw,))
        label = spec.get('label') if isinstance(spec, dict) else None
        need(isinstance(label, str) and label.startswith(LABEL_PREFIX) and _is_sha(label[len(LABEL_PREFIX):]),
             'SPEC_LABEL_HAS_NO_THETA_KEY')
        key = label[len(LABEL_PREFIX):]
        reg = env.registry
        slot = ((spec.get('numerics') or {}).get('uv_tail') or {}).get('lo_certificate')
        need(slot == reg['launch'], 'LO_SLOT_IS_NOT_THE_LAUNCH_PIN (A136: LO_NGC_K32_CERT_V001 07745bbf)')    # 4
        env.read_raw(dict(slot))
        pt = env.P.derive_point(spec_ref, key, reg)                                              # 5
        rho = read_json(rho_ref, 'rho record')
        proj = check_rho_record(rho, env, identity=pt['identity'], custody=pt['custody'], point_sha256=pt['point_sha256'])  # 6
        tb = rho.get('theta_binding')                                                            # D3; E1 (A167 0741)
        gbits = tb.get('theta_route_gamma_eff_bits_equal') if isinstance(tb, dict) else None
        need(type(gbits) is bool, 'RHO_RECORD_LACKS_THE_THETA_ROUTE_DIAGNOSTIC (A167 0741: '
             'theta_binding.theta_route_gamma_eff_bits_equal)')
        need(gbits == pt['bind']['theta_route_gamma_eff_bits_equal'],                           # E2 (W1)
             'RHO_RECORD_THETA_ROUTE_FLAG_IS_NOT_DERIVE_POINT_S (W1: the record reads %r, this proof\'s derive_point %r)'
             % (gbits, pt['bind']['theta_route_gamma_eff_bits_equal']))
        geff = tb.get('gamma_eff')                                                               # E1 + E2: what C4b reads
        need(type(geff) is float and geff.hex() == pt['bind']['hex']['gamma_eff']
             and isinstance(tb.get('hex'), dict) and tb['hex'].get('gamma_eff') == pt['bind']['hex']['gamma_eff'],
             'RHO_RECORD_BOUND_GAMMA_EFF_IS_NOT_DERIVE_POINT_S (E1, E2: the bound s*(ge*EB) that root\'s C4b compares)')
        diag = dict(THETA_ROUTE, theta_route_gamma_eff_bits_equal=gbits, bound_gamma_eff=pt['bind']['gamma_eff'],
                    bound_gamma_eff_hex=pt['bind']['hex']['gamma_eff'],
                    theta_route_gamma_eff_hex=pt['bind']['hex']['theta_route_gamma_eff'])
        keys = env.P.RHO_COMPARE_KEYS
        pair = list(seed_rho_pair) if isinstance(seed_rho_pair, (list, tuple)) else []           # 7
        need(len(pair) == 2 and all(_is_pin(p) for p in pair), 'SEED_RHO_REPRODUCIBILITY_UNPROVEN (G4: two registered seed records)')
        need(all(_in_list(p, registered_rho_records) for p in pair), 'SEED_RHO_RECORD_NOT_REGISTERED')
        need(pair[0]['sha256'] != pair[1]['sha256'] and pair[0]['path'] != pair[1]['path'],
             'SEED_RHO_PAIR_NOT_TWO_RECORDS (distinct sha and path)')
        seeds = [read_json(p, 'seed rho record') for p in pair]
        sproj = [check_rho_record(s, env) for s in seeds]
        need(all(type(s['custody'].get('route_a_column_workers')) is int and s['custody']['route_a_column_workers'] == 1
                 for s in seeds), TWIN_CODE + ' (0717 R4; E8, W2): a G4 seed pair record\'s custody route_a_column_workers '
             'is not int 1; the cw8 twin is never a member and gets no rho record')
        need(all(s['identity'].get('theta_key') == reg['seed_key'] and s['custody'].get('theta_key') == reg['seed_key']
                 for s in seeds), 'SEED_RHO_RECORD_NOT_AT_THE_SEED_KEY')
        need(seeds[0]['identity'] == seeds[1]['identity'] and seeds[0]['custody'] == seeds[1]['custody'],
             'SEED_RHO_RECORDS_DIFFER_IN_POINT_OR_CUSTODY')
        c0, c1 = rho_bitwise_canonical(seeds[0], keys), rho_bitwise_canonical(seeds[1], keys)
        need(c0 == c1, 'SEED_RHO_NOT_BITWISE_EQUAL (G4: wrapper v002 10-key canonical; no NGC rho may bind)')
        if key == reg['seed_key']:
            need(rho_bitwise_canonical(rho, keys) == c0, 'SEED_SLOT_RHO_NOT_BITWISE_EQUAL_TO_THE_REPRODUCED_PAIR')
        thr = thresholds(env.read_raw)                                                           # 8
        disclosure = json.loads(json.dumps(SCOPE_DISCLOSURE))                                    # D5 (A153, 0723)
        _verbatim(env.read_raw, disclosure['source'], disclosure['text'])
        proof = {'schema': PROOF_SCHEMA, 'gate': GATE, 'utc': env.utc(), 'status': 'TESTED', 'verdict': 'PASS',
                 'theta_key': key, 'theta_role': pt['theta_role'], 'point_sha256': pt['point_sha256'],
                 'custody_sha256': pt['custody_sha256'], 'producer': me, 'driver_certificate': dict(slot),
                 'lo_certificate_launch_pin': dict(reg['launch']), 'rho_record': dict(rho_ref),
                 'rho_producer': dict(env.producer_pin),
                 'rho_bitwise_canonical_sha256': hashlib.sha256(rho_bitwise_canonical(rho, keys)).hexdigest(),
                 'rho_projection_diagnostic': proj, 'rho_projection_sha256': digest(proj),
                 'route_a_column_workers': pt['custody']['route_a_column_workers'],
                 'theta_route_diagnostic': diag,
                 'seed_rho_reproducibility': {
                     'records': [dict(p) for p in pair], 'seed_theta_key': reg['seed_key'], 'bitwise_equal_10_key': True,
                     'compare_keys': list(keys), 'canonical_sha256': hashlib.sha256(c0).hexdigest(),
                     'projection_equal_diagnostic_only': sproj[0] == sproj[1],
                     'rule': 'wrapper v002 7a6af535 L177-179, L189-191 (A138 V03): identical canonical bytes of the 10 keys'},
                 'slot_rule': SLOT_RULE, 'lo_route': LO_ROUTE, 'lo_certified': False, 'thresholds': thr,
                 'readings': READINGS, 'root_rulings': out['root_rulings'], 'scope_disclosure_a153': disclosure,
                 'scope': ('Binds the NGC call\'s lo_certificate slot (the launch custody pin LO_NGC_K32_CERT_V001, hash-recorded '
                           'only by the driver and the tail library) to the point\'s ROOT-REGISTERED rho record for post-run '
                           'per-state acceptance. It certifies no LO and compares nothing to the thresholds; rho is a '
                           'numerical maximum estimate, not a rigorous supremum.')}
        _refuse_forbidden(proof)
        out.update(verdict=READY, proof=proof)
    except CAUGHT as exc:
        out['blockers'].append(type(exc).__name__ + ': ' + str(exc))
    return out


def _real_env():
    state = {}

    def producer():
        if 'P' not in state:
            state['P'] = _load_exact(PRODUCER[0], PRODUCER[1], 'ngc_rho_producer_c3v003_for_slot_proof')
        return state['P']
    env = types.SimpleNamespace(read_raw=read_raw, self_pin=_self_pin, utc=_utc, allow_synthetic=False,
                                producer_pin={'path': PRODUCER[0], 'sha256': PRODUCER[1]})
    env.P = producer()
    env.registry = env.P.real_registry()
    return env


def prove_ngc_lo_slot(spec_ref, rho_ref, *, registered_rho_records=(), seed_rho_pair=(), root_ruling_refs=None,
                      approved_producer_sha256=()):
    """Public entry: the registered inputs only (no test symbol, no synthetic registry)."""
    try:
        root_gate(root_ruling_refs, read_raw)          # the gate runs before the producer module is loaded
        env = _real_env()
    except CAUGHT as exc:
        return {'schema': RESULT_SCHEMA, 'utc': _utc(), 'status': 'TESTED', 'verdict': 'BLOCKED',
                'blockers': [type(exc).__name__ + ': ' + str(exc)], 'proof': None}
    return _prove(spec_ref, rho_ref, registered_rho_records=registered_rho_records, seed_rho_pair=seed_rho_pair,
                  root_ruling_refs=root_ruling_refs, approved_producer_sha256=approved_producer_sha256, env=env)


def write_new(out_root, name, obj):
    need(isinstance(out_root, str) and os.path.isabs(out_root) and os.path.realpath(out_root) == out_root
         and os.path.isdir(out_root), 'OUT_ROOT_INVALID')
    need(isinstance(name, str) and name == os.path.basename(name) and name.endswith('.json'), 'OUT_NAME_INVALID')
    raw = (json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    path = os.path.join(out_root, name)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}


def write_proof(result, out_root, name=None):
    proof = (result or {}).get('proof')
    need((result or {}).get('verdict') == READY and isinstance(proof, dict), 'NO_PROOF_TO_WRITE')
    _refuse_forbidden(proof)
    need(proof.get('schema') == PROOF_SCHEMA and proof.get('gate') == GATE and proof.get('status') == 'TESTED'
         and proof.get('verdict') == 'PASS' and proof.get('lo_certified') is False, 'PROOF_SHAPE_INVALID')
    return write_new(out_root, name or 'NGC_LO_RHO_SLOT_PROOF_%s.json' % proof['theta_key'][:16], proof)


def _background_qos():
    try:
        return os.getpriority(4, 0) == 1
    except Exception:
        return False


def main(argv=None):
    if not _background_qos():
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        return 2
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B, no -O)', flush=True)
        return 2
    import argparse
    ap = argparse.ArgumentParser(description='NGC LO slot proof c3v003 (A136 G5)')
    ap.add_argument('--args', required=True, help='JSON: spec_ref, rho_ref, registered_rho_records, seed_rho_pair, '
                    'root_ruling_refs, approved_producer_sha256')
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--out-root', required=True)
    a = ap.parse_args(argv)
    try:
        root_gate(ROOT_RULINGS, read_raw)                  # before any pin is read
        args = read_json({'path': a.args, 'sha256': a.args_sha256}, 'args')
        res = prove_ngc_lo_slot(args.get('spec_ref'), args.get('rho_ref'),
                                registered_rho_records=args.get('registered_rho_records', ()),
                                seed_rho_pair=args.get('seed_rho_pair', ()), root_ruling_refs=args.get('root_ruling_refs'),
                                approved_producer_sha256=args.get('approved_producer_sha256', ()))
        pin = write_proof(res, a.out_root) if res['verdict'] == READY else None
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        rpin = write_new(a.out_root, 'NGC_LO_RHO_SLOT_RESULT_%s.json' % stamp, res)
    except CAUGHT as exc:
        print(json.dumps({'verdict': 'BLOCKED', 'blockers': [type(exc).__name__ + ': ' + str(exc)]}), flush=True)
        return 3
    print(json.dumps({'verdict': res['verdict'], 'blockers': res['blockers'], 'proof': pin, 'result': rpin}), flush=True)
    return 0 if pin else 3


if __name__ == '__main__':
    sys.exit(main())
