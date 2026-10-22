"""NGC acceptance handoff c2v003a (V006 A162 + A167; A153 S11 + A155). Root build (Claude2 workflow); nothing here is
adopted until root rules and Claude3 reviews the c2v003 round. Values writer v004 (A159) then pins this handoff's schema
and sha.

c2v003a = the handoff c2v003 with only the A167 change: it pins the adapter successor ngc_lo_state_adapter_c2v003a (C4b on
the spec route s*(ge*EB), the theta route a diagnostic; Claude3 NGC rho c3v003 schema strings *_C3V003 in S2) in place of
c2v002, and its record schemas move to C2V003A. The reader, the S5 tool, the contract, the S2 pins (PENDING), the
execution facts and the SRB-ROT report are c2v003's, unchanged. The c2v003 text follows.

NGC acceptance handoff c2v003 (V006 A162; A153 S11 + A155).

A162: "NGC acceptance = the A153/A155 LO gate + custody + execution facts."

c2v003 = the c2v002 handoff (ef3da6f5) plus the A162 rulings 1-6, built here:
  1. Route-A iterate list (A162 item 1): the list must be the pinned reader's (ngc_route_a_iterates_c2v003, ITERATE_READER)
     and its occurrences must be exactly the call's own sidecar enumeration, re-derived here from bytes
     (verify_iterate_list). The enumerator c2v001 receives only that reader's sha as the approved iterate producer.
  2. S5 rebuild exports (A162 item 2): every non-accepted state's input must be the pinned S5 tool's
     (ngc_s5_rebuild_export_c2v003, S5_TOOL) and carry an ADMITTED admission whose exported files are the input's
     tail-state pins (verify_export); the adapter's approved rebuild producer is that sha only. An export that does not
     verify is dropped (blocker REBUILD_EXPORT_REFUSED) and its state reads UNAVAILABLE in the adapter.
  3. The NGC row contract (A162 item 3): ROW_CONTRACT, built by root from manifest a2936517 (ngc_row_contract_c2v003),
     pinned by sha. One contract: a policy row_contract other than it is refused.
  4. Execution facts (A162 item 4; A138 V01(b) for DDO): {fresh_call, resumed, retried, route_a_completed_normally,
     run_root}, each read from the call's own records by the DDO handoff c2v004 EXECUTION_RULE (the v005 fresh_scope rule
     it cites), mapped onto the NGC records (NGC_EXECUTION_RULE). Anything not established (None) refuses, and so does an
     established fact other than fresh / not resumed / not retried / completed normally (A48). A refusal stops before the
     inventory: the call reads INCOMPLETE and no LO number is computed.
  5. SRB-ROT for NGC (A162 item 5): REPORT-ONLY, labelled 'report-only: no registered NGC tau'. The bound is exactly A152's
     eps_km_s (W-1: the pinned library srb_rot(S, C, rows)['bound_km_s'], S = the le{final_pass}_rotation TailState from
     its verified S5 export, C = the point's own EPS certificate field eps, rows = row producer 67fddd24 rotation_rows on
     the call's own rotation arrays with the own column-mean query-support radii; tau inert). It is written to
     SRB_ROT_REPORT.json and NEVER gates: no reading, blocker or member flag reads it.
  6. S2 rho (A162 item 6): S2_PINS hold Claude3's NGC rho producer and slot-proof producer shas. They read PENDING until
     root pins Claude3's NGC rho c3v002 after its review; PENDING reads UNAVAILABLE (blocker S2_RHO_PINS_PENDING; the
     adapter receives empty approved lists, so every state reads NGC_RHO_RECORD_MISMATCH). Policy cannot supply S2
     approvals.
Everything else is c2v002's behaviour: FINISHED receipt gate; accepted state input from the call's own
ROUTE_A_TAIL_MANIFEST; the pinned adapter c2v002 (ce33b526) and enumerator c2v001 (607b7f66), unchanged; adoption
re-reads and guards every per-state record; readings recomputed (A134 Q5 / 0690 OPEN-6, no anchor); S12 blinding (the
summary and the CLI carry verdicts, codes, coverage flags and execution facts only).
"""
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LO_ADAPTER = {'path': os.path.join(HERE, 'ngc_lo_state_adapter_c2v003a.py'),
              'sha256': '9c4b6dfc591cfd5c372416beb936d5d903540e5fc41e4a327b428d7ba5001eb2', 'entry': 'adapt_call_ngc_lo'}
ENUMERATOR = {'path': os.path.join(HERE, 'ngc_consumed_states_c2v001.py'),
              'sha256': '607b7f667dfa1612da3fd874ab2656dc5ca487285a28afb2e4b1bfe979bd3125', 'entry': 'enumerate_call'}
ITERATE_READER = {'path': os.path.join(HERE, 'ngc_route_a_iterates_c2v003.py'),
                  'sha256': '9335ee4212719944b6dd45369161de16891ec0ed5dbdd97fed36d68d0b993bdc'}
S5_TOOL = {'path': os.path.join(HERE, 'ngc_s5_rebuild_export_c2v003.py'),
           'sha256': '3611e9933b57363ffab8dbdbaae67960751e59d3d34b219f1777e8e2f2a54100'}
ROW_CONTRACT = {'path': os.path.join(HERE, 'NGC_ROW_CONTRACT_C2V001.json'),
                'sha256': '80cbf2f5be2e9f22a0b751376dcde3e7e779bd89f531a8ffe9d654616490fe32'}
ROW_PRODUCER = {'path': ART + '/s4_acceptance_c2/acceptance_q2/row_reference_producer_c2v003.py',
                'sha256': '67fddd24945de31d70f940cb1ff85ef9d467b20d62a764cd159f58afc909e01e'}   # rotation_rows L171-193
LIBRARY = {'path': ART + '/tail_scheme_impl_c2/driver_r5/module/owned_uv_tail_lapse_v002.py',
           'sha256': '2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'}   # srb_rot L860-871
PENDING = 'PENDING'
# A162 item 6 as updated by A167: Claude3's NGC rho c3v003 producer and slot-proof producer, pinned by root after its
# review (A167 R2-R4).
S2_PINS = {'rho_producer_sha256': PENDING, 'slot_proof_producer_sha256': PENDING}
RECORD_SCHEMA = 'UNT_NGC_LO_ACCEPTANCE_RECORD_C2V003A'
SUMMARY_SCHEMA = 'UNT_NGC_LO_ACCEPTANCE_ROOT_SUMMARY_C2V003A'
SRB_SCHEMA = 'UNT_NGC_SRB_ROT_REPORT_C2V003'
STATE_INPUT_SCHEMA = 'UNT_NGC_LO_STATE_INPUT_C2V001'
ROUTE = 'NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'
READINGS = ('NON_LAPSE_TAIL_MATERIAL', 'LO_UNCERTIFIED_TRANSIENT', 'INCOMPLETE', 'ACCEPTED')   # precedence
MEMBER_LO_OK = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT')                                      # A152 W-3 / A134
DECISIVE = ('ACCEPTED_ROUTE_A', 'INHERITED_ROUTE_A', 'ROUTE_B_STAGE')
ITERATE = 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'
ADAPTER_DIR = 'LO_ADAPTER_C2'
C_ADMISSION = 'NGC_LO_ADAPTER_NOT_ADMITTED'
POLICY_KEYS = ('receipt', 'route_a_iterates', 'rebuild_exports', 'row_contract', 'row_policy_review',
               'trusted_row_policy_review_sha256', 'slot_proof', 'rho_producer', 'approved_producer_sha256',
               'eps_certificate', 'high_qinf_admitted')
# ---- A162 item 4: execution facts
EXECUTION_KEYS = ('fresh_call', 'resumed', 'retried', 'route_a_completed_normally', 'run_root')
EXECUTION_REQUIRED = {'fresh_call': True, 'resumed': False, 'retried': False, 'route_a_completed_normally': True}
ROUTE_A_CONVERGED = {'classification': 'CONVERGED', 'converged_finite_fixed_point': True,
                     'outcome': 'CONVERGED_FINITE_FIXED_POINT'}       # handoff c2v004 L75-76; driver route_a_outcome_record
DDO_EXECUTION_RULE_OF_RECORD = (
    'A138 V01(b); keys of lo_producer_cx2v004 L56-59; values read from this call by the 0528 rule of '
    'consumed_states_cx2v005 fresh_scope L223-257: fresh_call = discovery coverage FRESH_COMPLETED, no '
    'spec.admit, result and out/finish.json COMPLETED and valid, finish bound to this result; retried = '
    'finish.retries != 0 or more than one route_a stage record; resumed = the single route_a stage argv '
    'lacks --start-iteration 0, or carries a resume/retry flag, or a --checkpoint-mode other than new; '
    'route_a_completed_normally = that stage executed with exit 0, route_a_outcome CONVERGED / '
    'converged_finite_fixed_point is True / CONVERGED_FINITE_FIXED_POINT, identity.route_a.mode computed; '
    'run_root = <call>/out')                                          # acceptance_handoff_c2v004 L66-73, verbatim
NGC_EXECUTION_RULE = (
    'A162 item 4, the DDO rule of record mapped onto the NGC records (driver cx3r008): FRESH scope = result and '
    'out/finish.json status COMPLETED and valid true, finish.result_sha256 = sha256(result.json bytes), finish.result_path '
    'is this out/result.json, out/start.json binds the same driver and call spec, the spec and normalized_spec carry no '
    'admit, identity.route_a.mode computed (no admitted or pending NGC route-A lane), and the route-A sidecar finish is '
    'finish_000 (no earlier controller finish); retried = finish.retries != 0 or more than one route_a stage record '
    '(the driver never retries: L9101 retries 0); resumed = the single route_a stage argv lacks --start-iteration 0, '
    'carries a resume/retry flag or a --checkpoint-mode other than new, or the route-A record has a reloaded iteration '
    '(controller L355) or a sidecar finish index other than 000; route_a_completed_normally = that stage executed with '
    'exit 0, result.route_a_outcome classification CONVERGED, converged_finite_fixed_point is True, outcome '
    'CONVERGED_FINITE_FIXED_POINT, identity.route_a.mode computed; run_root = <call>/out. A fact the records do not '
    'establish stays None and refuses; acceptance needs fresh, not resumed, not retried, completed normally.')
# ---- A162 item 5: SRB-ROT report-only
SRB_LABEL = 'report-only: no registered NGC tau'
SRB_RULE = ('A162 item 5 / A152 W-1: bound_km_s = owned_uv_tail_lapse_v002 srb_rot(S, C, rows)[bound_km_s] (L860-871); '
            'S = the TailState of the call own le{final_pass}_rotation stage from its verified S5 export (digest = the '
            'stage finish.json uv_tail.state_digest; record.eps_certificate = the point EPS pin); C = the point own '
            'certificate, field eps per unit shell; rows = row_reference_producer_c2v003 rotation_rows (L171-193) on the '
            'own rotation arrays with the own column-mean query-support radii; tau inert (bound_km_s does not depend on '
            'it; ratio_to_tau and pass_tau_over_10 are discarded). It is exactly A152 eps_km_s, AT-1 noise term. It never '
            'gates: A134 Q10 tau_i/10 is DDO\'s, and there is no registered NGC tau.')
CERT_SCHEMAS = ('UNT_CLAUDE4_S0_POINT_EPS_C4V002',)                                        # A148 / W-4
CERT_PRODUCERS = ('8972822b5439e184297b4a5dbb552983ddb806804565ee1cc26691b680147235',)   # eps_ngc_point_c4v002 (A148)
CERT_COVERAGE = (2.0, 91.0)
INERT_TAU_KM_S = 1.0
FINAL_ROTATION_KIND = 'le_rotation'
COLUMN_MEAN_OK = 'CONDITIONAL_PREPARATION_ROWS_NOT_CALIBRATION'
LABEL_PREFIX = 'step5 A_K32_A2_HEADLINE theta_key='


class Refusal(ValueError):
    """Fail-closed refusal."""


def need(ok, code):
    if not ok:
        raise Refusal(code)


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


def self_pin():
    p = os.path.realpath(__file__)
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def read_raw(ref):
    need(is_pin(ref) and os.path.isabs(ref['path']), 'NOT_AN_EXACT_PIN')
    real = os.path.realpath(ref['path'])
    need('ngc3198' not in os.path.basename(real).lower(), 'NGC3198_NAMED_FILE_REFUSED')
    with open(real, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], 'BYTE_PIN_MISMATCH: ' + ref['path'])
    return raw


def read_pin(ref):
    return json.loads(read_raw(ref))


def load_pinned(ref, name):
    p = ref['path']
    need(os.path.isabs(p) and os.path.realpath(p) == p, 'NONCANONICAL_MODULE_PATH')
    with open(p, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], 'MODULE_PIN_MISMATCH: ' + p)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    exec(compile(raw, p, 'exec'), mod.__dict__)
    return mod


def _own(path, out, label):
    need(isinstance(path, str) and os.path.isabs(path), label + ': PATH_NOT_ABSOLUTE')
    real = os.path.realpath(path)
    need(real.startswith(out + os.sep), label + ': OUTSIDE_OWN_CALL_OUT')
    need('ngc3198' not in os.path.basename(real).lower(), label + ': NGC3198_NAMED_FILE_REFUSED')
    return real


def _own_bytes(ref, out, label):
    need(is_pin(ref), label + ': NOT_AN_EXACT_PIN')
    real = _own(ref['path'], out, label)
    with open(real, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], label + ': SHA_MISMATCH')
    return raw


class Store:
    """Exclusive-create JSON writer for one call's NGC acceptance records."""

    def __init__(self, records_dir):
        d = os.path.realpath(str(records_dir))
        need(d.startswith(ART + os.sep), 'RECORDS_DIR_OUTSIDE_CLAUDE_ARTIFACTS')
        parts = [x.casefold() for x in d.split(os.sep)]
        need(not any(x.startswith('uvt_') or 'ngc3198' in x or x == 'c5h_hull_c2' for x in parts),
             'RECORDS_DIR_FORBIDDEN_COMPONENT')
        os.mkdir(d)
        self.dir = d
        self.files = []

    def put(self, name, obj):
        need(name == os.path.basename(name) and name.endswith('.json'), 'OUT_NAME_INVALID')
        p = os.path.join(self.dir, name)
        raw = canonical(obj) + b'\n'
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o644)
        with os.fdopen(fd, 'wb') as f:
            f.write(raw)
        ref = {'path': p, 'sha256': hashlib.sha256(raw).hexdigest()}
        self.files.append(ref)
        return ref


def receipt_ok(receipt_ref, result_sha):
    rc = read_pin(receipt_ref)
    return (rc.get('status') == 'FINISHED' and rc.get('driver_status') == 'COMPLETED'
            and (rc.get('result') or {}).get('sha256') == result_sha)


# ------------------------------------------------------------------------------------------------ A162 item 4
def execution_block(*, out, result, result_raw, spec, enum):
    """The execution facts, each read from this call's own records (NGC_EXECUTION_RULE). Nothing is assumed: a fact the
    records do not establish stays None."""
    ex = {'fresh_call': None, 'resumed': None, 'retried': None, 'route_a_completed_normally': None, 'run_root': out}
    basis = {'rule': NGC_EXECUTION_RULE, 'rule_of_record': DDO_EXECUTION_RULE_OF_RECORD}
    try:
        with open(os.path.join(out, 'finish.json'), 'rb') as f:
            fraw = f.read()
        fin = json.loads(fraw)
        basis['finish'] = {'path': os.path.join(out, 'finish.json'), 'sha256': hashlib.sha256(fraw).hexdigest()}
        start = None
        sp = os.path.join(out, 'start.json')
        if os.path.isfile(sp) and not os.path.islink(sp):
            with open(sp, 'rb') as f:
                sraw = f.read()
            start = json.loads(sraw)
            basis['start'] = {'path': sp, 'sha256': hashlib.sha256(sraw).hexdigest()}
        stages = [r for r in result.get('stage_records') or [] if isinstance(r, dict) and r.get('kind') == 'route_a']
        argv = stages[0].get('argv') if len(stages) == 1 else None
        argv = argv if isinstance(argv, list) and all(isinstance(x, str) for x in argv) else None

        def value(flag):
            if argv is None or argv.count(flag) != 1 or argv.index(flag) + 1 >= len(argv):
                return None
            return argv[argv.index(flag) + 1]
        retries = fin.get('retries')
        if len(stages) > 1 or (type(retries) is int and retries != 0):
            ex['retried'] = True
        elif len(stages) == 1 and type(retries) is int and retries == 0:
            ex['retried'] = False
        sidecar = (enum or {}).get('sidecar') or {}
        reloaded = (enum or {}).get('reloaded_iterations')
        if argv is not None and type(sidecar.get('finish_index')) is int and isinstance(reloaded, list):
            flags = [x.casefold() for x in argv if x.startswith('--')]
            ex['resumed'] = not (value('--start-iteration') == '0' and not any('resume' in f or 'retry' in f for f in flags)
                                 and ('--checkpoint-mode' not in argv or value('--checkpoint-mode') == 'new')
                                 and not reloaded and sidecar['finish_index'] == 0)
        mode = ((result.get('identity') or {}).get('route_a') or {}).get('mode')
        if len(stages) == 1:
            st = stages[0]
            outcome = result.get('route_a_outcome') or {}
            ex['route_a_completed_normally'] = (
                st.get('executed') is True and type(st.get('exit_code')) is int and st['exit_code'] == 0
                and all(outcome.get(k) == v for k, v in ROUTE_A_CONVERGED.items())
                and outcome.get('converged_finite_fixed_point') is True and mode == 'computed')
        rsha = hashlib.sha256(result_raw).hexdigest()
        ns = result.get('normalized_spec')
        try:
            path_ok = os.path.realpath(str(fin.get('result_path'))) == os.path.join(out, 'result.json')
        except (TypeError, ValueError):
            path_ok = False
        if start is not None and type(sidecar.get('finish_index')) is int and isinstance(spec, dict):
            ex['fresh_call'] = (result.get('status') == 'COMPLETED' and result.get('valid') is True
                                and fin.get('status') == 'COMPLETED' and fin.get('valid') is True
                                and fin.get('result_sha256') == rsha and path_ok
                                and isinstance(start, dict) and start.get('driver_sha256') == result.get('driver_sha256')
                                and start.get('call_spec_sha256') == result.get('call_spec_sha256')
                                and 'admit' not in spec and not (isinstance(ns, dict) and 'admit' in ns)
                                and mode == 'computed' and sidecar['finish_index'] == 0)
        basis.update(route_a_stage_records=len(stages), route_a_mode=mode, sidecar_finish_index=sidecar.get('finish_index'),
                     reloaded_iterations=reloaded, start_present=start is not None)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        basis['not_established'] = '%s: %s' % (type(exc).__name__, exc)
    ex['basis'] = basis
    return ex


def execution_problems(ex, out):
    bad = ['%s NOT_ESTABLISHED' % k for k in EXECUTION_REQUIRED if ex.get(k) is None]
    bad += ['%s=%r (required %r)' % (k, ex.get(k), v) for k, v in EXECUTION_REQUIRED.items()
            if ex.get(k) is not None and ex.get(k) is not v]
    if ex.get('run_root') != out:
        bad.append('run_root %r is not this call out %r' % (ex.get('run_root'), out))
    return bad


# ------------------------------------------------------------------------------------------------ A162 item 5
def check_certificate(cert_ref, theta_key):
    """values_writer_c2v003a check_certificate (W-4 / C-8) for this point: -> ({'shells': [...]}, checks)."""
    rec = read_pin(cert_ref)
    need(isinstance(rec, dict) and rec.get('schema') in CERT_SCHEMAS, 'CERT_SCHEMA')
    pt = rec.get('point') if isinstance(rec.get('point'), dict) else {}
    role = str(pt.get('role'))
    need(rec.get('mode') == 'point' and 'anchor' not in role.lower() and 'smoke' not in role.lower(), 'CERT_NOT_A_POINT_RECORD')
    need(is_sha(theta_key) and pt.get('key') == theta_key, 'CERT_OTHER_POINT')
    kc = rec.get('key_check') or {}
    need(kc.get('equals_point_key') is True and kc.get('from_theta_hex') == theta_key
         and kc.get('from_theta_natural') == theta_key, 'CERT_KEY_CHECK')
    prod = rec.get('producer')
    need(isinstance(prod, dict) and prod.get('sha256') in CERT_PRODUCERS, 'CERT_PRODUCER_NOT_REVIEWED')
    need(rec.get('gate') == 'EPS' and rec.get('verdict') == 'CERTIFIED' and rec.get('certificate') is True
         and (rec.get('summary') or {}).get('rule_verdict') == 'CERTIFIED', 'CERT_NOT_CERTIFIED')
    need(rec.get('coverage_inverse_kpc') == {'NGC': list(CERT_COVERAGE)}, 'CERT_COVERAGE')
    shells = rec.get('shells')
    need(isinstance(shells, list) and shells, 'CERT_SHELLS_MISSING')
    cursor, out = CERT_COVERAGE[0], []
    for s in shells:
        lo, hi, eps = (s.get(k) if isinstance(s, dict) else None for k in ('lo_inverse_kpc', 'hi_inverse_kpc', 'eps'))
        need(_num(lo) and _num(hi) and _num(eps) and lo == cursor and hi == lo + 1.0, 'CERT_SHELLS_NOT_CONTIGUOUS_UNIT_SHELLS')
        envs = [(s.get(k) or {}).get('eps_envelope') for k in ('flat', 'envelope')]
        need(eps >= 0 and all(_num(e) and 0 <= e <= eps for e in envs), 'CERT_EPS_NOT_THE_LARGER_VALUE')
        out.append({'lo_inverse_kpc': float(lo), 'hi_inverse_kpc': float(hi), 'eps': float(eps)})
        cursor = hi
    need(cursor == CERT_COVERAGE[1], 'CERT_COVERAGE')
    return {'shells': out}, {'schema': rec['schema'], 'point_key': theta_key, 'point_role': role,
                             'producer_sha256': prod['sha256'], 'n_unit_shells': len(out), 'eps_field': 'eps',
                             'eps_max_read': False}


def srb_rot_report(*, store, out, result, inv, spec, cert_ref, state_inputs, lib, rowmod):
    """A162 item 5. Returns the status block; the values go to SRB_ROT_REPORT.json only. Never raises, never gates."""
    import numpy as np
    status = {'label': SRB_LABEL, 'gates': False, 'status': 'UNAVAILABLE', 'code': None, 'report': None}
    try:
        need(is_pin(cert_ref), 'NO_POINT_CERTIFICATE (policy eps_certificate)')
        label = (spec or {}).get('label')
        need(isinstance(label, str) and label.startswith(LABEL_PREFIX) and is_sha(label[len(LABEL_PREFIX):]),
             'SPEC_LABEL_HAS_NO_THETA_KEY')
        key = label[len(LABEL_PREFIX):]
        cert, checks = check_certificate(cert_ref, key)
        n, passes = result.get('final_pass'), result.get('passes')
        need(type(n) is int and n >= 1 and isinstance(passes, list) and len(passes) == n and isinstance(passes[-1], dict)
             and passes[-1].get('pass') == n, 'FINAL_PASS_UNAVAILABLE')
        fp = passes[-1]
        stage = 'le%d_rotation' % n
        hits = [o for o in inv.get('occurrences') or [] if o.get('role') == 'own_source_state' and o.get('stage') == stage]
        need(len(hits) == 1 and hits[0]['state'].get('stage_kind') == FINAL_ROTATION_KIND,
             'FINAL_ROTATION_STATE_NOT_UNIQUE_IN_INVENTORY ' + stage)
        target = hits[0]['state']
        rot = str(fp.get('rotation'))
        need(re.fullmatch(r'[0-9]+_' + stage, os.path.basename(os.path.dirname(rot))) is not None
             and os.path.basename(rot) == 'rotation', 'FINAL_ROTATION_STAGE_DIR')
        frp = _own(os.path.join(rot, 'finish.json'), out, 'rotation finish')
        with open(frp, 'rb') as f:
            fraw = f.read()
        srec = [e for e in (result.get('uv_tail') or {}).get('stage_records') or [] if isinstance(e, dict)
                and e.get('stage') == stage]
        need(len(srec) == 1 and srec[0].get('finish_sha256') == hashlib.sha256(fraw).hexdigest(),
             'FINAL_ROTATION_FINISH_NOT_THE_RECORDED_FINISH (driver uvt_stage_records L1155-1172)')
        fin = json.loads(fraw)
        fuv = fin.get('uv_tail') or {}
        need(fuv.get('state_digest') == target['state_sha256'] and fuv.get('stage_kind') == FINAL_ROTATION_KIND,
             'FINAL_ROTATION_FINISH_STATE')
        need((fuv.get('config') or {}).get('eps_certificate') == cert_ref, 'STAGE_EPS_PIN_NOT_THE_POINT_CERTIFICATE')
        arrays_pin = fp.get('rotation_arrays')
        need(is_pin(arrays_pin) and {'path': fin.get('arrays_path'), 'sha256': fin.get('arrays_sha256')} == arrays_pin,
             'FINAL_PASS_ROTATION_ARRAYS_MISMATCH (driver L8927)')
        need(fp.get('rotation_positive') is True and fin.get('positive_rotation_square') is True,
             'NONPOSITIVE_ROTATION (W-3 v <= 0: no bound)')
        with np.load(io.BytesIO(_own_bytes(arrays_pin, out, 'rotation arrays')), allow_pickle=False) as z:
            R, omega, fields = (np.array(z[k]) for k in ('radial_nodes_m', 'rotation_Omega_squared', 'full_fields_complex'))
        cm = fp.get('column_mean')
        need(isinstance(cm, dict) and cm.get('status') == COLUMN_MEAN_OK, 'COLUMN_MEAN_UNAVAILABLE')
        cmr = json.loads(_own_bytes({'path': cm.get('path'), 'sha256': cm.get('sha256')}, out, 'column mean'))
        pred = cmr.get('prediction') or {}
        need(cmr.get('status') == COLUMN_MEAN_OK and cmr.get('rotation_array_pin') == arrays_pin,
             'COLUMN_MEAN_NOT_OF_THIS_ROTATION')
        rows = fp.get('rows')
        need(isinstance(rows, list) and pred.get('rows') == rows and result.get('rows') == rows, 'FINAL_ROWS_NOT_THE_COLUMN_MEAN_ROWS')
        valid = [r['id'] for r in rows if r.get('valid', True) is True and _num(r.get('speed_km_s'))]
        sup = pred.get('query_support')
        need(isinstance(sup, list) and [s.get('id') for s in sup] == valid, 'QUERY_SUPPORT_NOT_THE_VALID_ROWS')
        radii = [s.get('radius_m') for s in sup]
        need(all(_num(x) and x > 0 for x in radii), 'ROW_RADII')
        sin = state_inputs.get(target['state_sha256'])
        need(is_pin(sin), 'FINAL_ROTATION_STATE_HAS_NO_VERIFIED_S5_EXPORT')
        si = read_pin(sin)
        rec = json.loads(read_raw(si['tail_state']['record']))
        with np.load(io.BytesIO(read_raw(si['tail_state']['arrays'])), allow_pickle=False) as z:
            arrays = {k: z[k].copy() for k in z.files}
        try:
            st = lib.TailState.from_arrays(arrays, rec, expected_digest=target['state_sha256'])
        except lib.Refusal as exc:
            raise Refusal('TAIL_STATE_NOT_THE_CALL_STATE %s' % exc)
        need(rec.get('stage_kind') == FINAL_ROTATION_KIND and rec.get('roster_digest') == fuv.get('roster_digest')
             and rec.get('config_sha256') == fuv.get('config_sha256'), 'TAIL_STATE_STAGE_SOURCE_OR_CONFIG_MISMATCH')
        need(rec.get('eps_certificate') == cert_ref, 'TAIL_STATE_DID_NOT_RUN_WITH_THE_POINT_CERTIFICATE')
        edges = np.asarray(arrays['shell_edges_inverse_kpc'], float)
        nz = np.flatnonzero(np.any(np.asarray(arrays['shell_integrals']) != 0, axis=1))
        if len(nz):
            need(float(edges[nz[0]]) >= CERT_COVERAGE[0] - 1e-12 and float(edges[nz[-1] + 1]) <= CERT_COVERAGE[1] + 1e-12,
                 'CERT_COVERAGE_DOES_NOT_COVER_STATE')
        try:
            rr = rowmod.rotation_rows(R, omega, fields, radii)
        except rowmod.Unavailable as exc:
            raise Refusal('ROTATION_ROWS_UNAVAILABLE %s' % exc)
        need(rr['row_columns'] == [s.get('column_indices') for s in sup], 'ROW_COLUMNS_DIFFER_FROM_COLUMN_MEAN_SUPPORT')
        sr = lib.srb_rot(st, cert, dict(rr, tau_km_s=[INERT_TAU_KM_S] * len(radii)))
        bound = sr['bound_km_s']
        need(len(bound) == len(valid) and all(_num(b) and b >= 0 for b in bound), 'BOUND_NOT_FINITE_NONNEGATIVE')
        by_id = dict(zip(valid, bound))
        speed = {r['id']: r.get('speed_km_s') for r in rows}
        reason = []
        for r in rows:
            if r['id'] not in by_id:
                reason.append('ROW_INVALID_IN_CALL: %s' % r.get('reason'))
            elif not speed[r['id']] > 0:
                reason.append('ROW_SPEED_NONPOSITIVE_IN_CALL (W-3, v <= 0)')
            else:
                reason.append(None)
        frp_sha = hashlib.sha256(fraw).hexdigest()
        rep ={'schema': SRB_SCHEMA, 'label': SRB_LABEL, 'gates': False, 'rule': SRB_RULE,
               'state': target, 'stage': stage, 'final_pass': n, 'certificate': dict(cert_ref), 'certificate_checks': checks,
               'row_ids': [r['id'] for r in rows],
               'bound_km_s': [by_id[r['id']] if why is None else None for r, why in zip(rows, reason)],
               'row_reason': reason,
               'rows_input': {'column_R_m': rr['column_R_m'], 'v_c_m_s': rr['v_c_m_s'], 'row_columns': rr['row_columns'],
                              'N_min': rr['N_min'], 'row_radii_m': radii},
               'library': dict(LIBRARY), 'row_producer': dict(ROW_PRODUCER), 'tau': 'inert (%r km/s)' % INERT_TAU_KM_S,
               'discarded': ['ratio_to_tau', 'pass_tau_over_10'], 'state_input': dict(sin),
               'rotation_finish': {'path': frp, 'sha256': frp_sha},
               'rotation_arrays': dict(arrays_pin)}
        status.update(status='COMPUTED', report=store.put('SRB_ROT_REPORT.json', rep))
    except Refusal as exc:
        status['code'] = str(exc)
    except Exception as exc:          # report-only: a failure is recorded and never changes the acceptance reading
        status['code'] = '%s: %s' % (type(exc).__name__, exc)
    return status


# ------------------------------------------------------------------------------------------------ adoption, readings
def adopt(rec, inv, call_rec, A, expected_kind):
    """Per state: exactly one adapter entry, its record re-read from the exact pin and guarded."""
    by_state = {}
    for s in call_rec.get('states') or []:
        if isinstance(s, dict) and isinstance(s.get('state'), dict):
            by_state.setdefault(digest(s['state']), []).append(s)
    classes = {digest(c['state']): c['class'] for c in inv['classes']}
    for state in inv['states']:
        e = {'state': state, 'class': classes.get(digest(state)), 'verdict': 'UNAVAILABLE', 'reading': 'UNAVAILABLE',
             'codes': [], 'coverage_flags': None, 'record': None}
        rec['states'].append(e)
        got = by_state.get(digest(state)) or []
        try:
            need(len(got) == 1, 'ADAPTER_STATE_ENTRY_NOT_UNIQUE')
            a = got[0]
            need(is_pin(a.get('record')), 'ADAPTER_STATE_RECORD_NOT_PINNED: %s' % a.get('record_error'))
            r = read_pin(a['record'])
            A.guard_state_record(r)                                     # scope text, PASS meaning, FAIL text, no anchor
            need(r.get('registry_kind') == expected_kind, 'STATE_RECORD_REGISTRY_KIND_%s' % r.get('registry_kind'))
            need(r.get('state') == state and r.get('state_class') == e['class'] == a.get('state_class'),
                 'STATE_RECORD_STATE_OR_CLASS')
            need(r.get('verdict') == a.get('verdict') and r.get('reading') == a.get('reading')
                 and r.get('codes') == a.get('codes'), 'STATE_RECORD_DIFFERS_FROM_CALL_ENTRY')
            need(r.get('call_result') == rec.get('result'), 'STATE_RECORD_NOT_THIS_CALL')
            e.update(verdict=r['verdict'], reading=r['reading'], codes=list(r['codes']), record=a['record'],
                     coverage_flags=r.get('coverage_flags'))
        except (Refusal, ValueError, KeyError, TypeError, OSError) as exc:
            e['codes'] = [C_ADMISSION]
            e['adoption_problem'] = str(exc)


def readings(rec):
    """A134 Q5 / 0690 OPEN-6, mechanically; no anchor class."""
    st = rec['states']
    failed = [e for e in st if e['verdict'] == 'FAIL']
    unavailable = [e for e in st if e['verdict'] != 'FAIL' and e['verdict'] != 'PASS']
    non_iterate = [e for e in st if e['class'] != ITERATE]
    found = set()
    if any(e['class'] in DECISIVE for e in failed):
        found.add('NON_LAPSE_TAIL_MATERIAL')
    elif failed and all(e['class'] == ITERATE for e in failed) and all(e['verdict'] == 'PASS' for e in non_iterate):
        found.add('LO_UNCERTIFIED_TRANSIENT')
    elif failed:
        rec['transient_candidate_unconfirmed'] = [e['state'] for e in failed]
    if unavailable or not st or rec['blockers']:
        found.add('INCOMPLETE')
    found.add('ACCEPTED')
    return next(r for r in READINGS if r in found), sorted(found - {'ACCEPTED'})


def blinded_summary(rec):
    """S12: verdicts, reason codes, shell coverage flags and execution facts only (no NGC value)."""
    ex = rec.get('execution') or {}
    srb = rec.get('srb_rot_report') or {}
    return {'schema': SUMMARY_SCHEMA, 'route': ROUTE, 'reading': rec['reading'], 'member_lo_ok': rec['member_lo_ok'],
            'high_qinf_ngc_lo_flagged': rec.get('high_qinf_ngc_lo_flagged'), 'registry_kind': rec.get('registry_kind'),
            't_rule_id': rec.get('t_rule_id'), 'blockers': list(rec['blockers']),
            'execution': {k: ex.get(k) for k in EXECUTION_KEYS},
            'srb_rot_report': {'label': srb.get('label'), 'gates': srb.get('gates'), 'status': srb.get('status'),
                               'code': srb.get('code')},
            's2': rec.get('s2'),
            'states': [{'state_sha256': e['state']['state_sha256'], 'stage_kind': e['state']['stage_kind'],
                        'class': e['class'], 'verdict': e['verdict'], 'reading': e['reading'], 'codes': e['codes'],
                        'coverage_flags': e.get('coverage_flags')} for e in rec['states']],
            'scope_disclosure': rec.get('scope_disclosure'), 'pass_meaning': rec.get('pass_meaning'), 'is_anchor': False}


def _s2_lists(s2_pins):
    need(isinstance(s2_pins, dict) and set(s2_pins) == set(S2_PINS), 'S2_PINS_KEYS')
    pending = [k for k, v in s2_pins.items() if v == PENDING]
    need(all(v == PENDING or is_sha(v) for v in s2_pins.values()), 'S2_PINS_NOT_SHA_OR_PENDING')
    if pending:
        return [], [], 'S2_RHO_PINS_PENDING (%s): UNAVAILABLE until root pins Claude3 NGC rho c3v003 after its review (A167 R2-R4)' % sorted(pending)
    return [s2_pins['slot_proof_producer_sha256']], [s2_pins['rho_producer_sha256']], None


def _accept(*, call_dir, spec_ref, policy, records_dir, enumerate_fn, adapter_fn, A, registry, R, S, s2_pins, contract_pin,
            lib, rowmod, approvals):
    store = Store(records_dir)
    rec = {'schema': RECORD_SCHEMA, 'route': ROUTE, 'call_dir': os.path.realpath(str(call_dir)), 'reading': 'INCOMPLETE',
           'blockers': [], 'states': [], 'registry_kind': registry['kind'], 'is_anchor': False,
           'scope_disclosure': A.SCOPE_DISCLOSURE, 'pass_meaning': A.PASS_MEANING, 'handoff': self_pin(),
           'execution': None, 'srb_rot_report': {'label': SRB_LABEL, 'gates': False, 'status': 'NOT_RUN', 'code': None,
                                                 'report': None}}
    rec['pins'] = {'lo_adapter': dict(LO_ADAPTER), 'enumerator': dict(ENUMERATOR), 'iterate_reader': dict(approvals['reader']),
                   's5_tool': dict(approvals['s5']), 'row_contract': dict(contract_pin) if is_pin(contract_pin) else contract_pin,
                   'row_producer': dict(ROW_PRODUCER), 'library': dict(LIBRARY), 's2': dict(s2_pins) if isinstance(s2_pins, dict) else s2_pins}
    rec['high_qinf_ngc_lo_flagged'] = True if (policy or {}).get('high_qinf_admitted') is True else None
    try:
        need(isinstance(policy, dict) and set(policy) <= set(POLICY_KEYS), 'POLICY_KEYS (S2 and producer approvals are pins, not policy)')
        if registry['kind'] == 'REGISTERED':
            need(s2_pins == S2_PINS, 'S2_PINS_NOT_THE_MODULE_CONSTANTS')
            need(contract_pin == ROW_CONTRACT, 'ROW_CONTRACT_NOT_THE_PINNED_CONTRACT')
            need(approvals == {'reader': ITERATE_READER, 's5': S5_TOOL}, 'READER_OR_S5_NOT_THE_PINNED_MODULES')
        need(is_pin(contract_pin), 'ROW_CONTRACT_NOT_PINNED')
        need(policy.get('row_contract') is None or policy['row_contract'] == contract_pin,
             'ROW_CONTRACT_NOT_THE_PINNED_CONTRACT (one contract, A162 item 3)')
        approved_slot, approved_rho, s2_block = _s2_lists(s2_pins)
        rec['s2'] = 'PENDING' if s2_block else 'PINNED'
        out = os.path.realpath(os.path.join(rec['call_dir'], 'out'))
        rp = os.path.join(out, 'result.json')
        with open(rp, 'rb') as f:
            rraw = f.read()
        rec['result'] = {'path': rp, 'sha256': hashlib.sha256(rraw).hexdigest()}
        result = json.loads(rraw)
        if not (is_pin(policy.get('receipt')) and receipt_ok(policy['receipt'], rec['result']['sha256'])):
            rec['blockers'].append('FINISHED_RECEIPT_REQUIRED')
            raise Refusal('FINISHED_RECEIPT_REQUIRED')
        spec = json.loads(read_raw(spec_ref)) if is_pin(spec_ref) else None
        # ---- A162 item 1: the call's own sidecar (custody); A162 item 4: execution facts
        try:
            enum = R.enumerate_sidecar(rec['call_dir'], driver_sha256=registry['driver']['sha256'])
        except R.Refusal as exc:
            enum = None
            rec['blockers'].append('ROUTE_A_SIDECAR: %s' % exc)
        rec['execution'] = ex = execution_block(out=out, result=result, result_raw=rraw, spec=spec, enum=enum)
        bad = execution_problems(ex, out)
        if bad:
            raise Refusal('EXECUTION_FACTS_REFUSE (A162 item 4): ' + '; '.join(bad))
        iter_ref = policy.get('route_a_iterates')
        try:
            rec['route_a_iterates'] = R.verify_iterate_list(iter_ref, rec['call_dir'], driver_sha256=registry['driver']['sha256'])['list']
        except (R.Refusal, Refusal) as exc:
            rec['blockers'].append('ROUTE_A_ITERATE_LIST: %s' % exc)
            iter_ref = None
        inv = enumerate_fn(rec['call_dir'], route_a_iterates_ref=iter_ref,
                           approved_iterate_producer_sha256=[approvals['reader']['sha256']],
                           driver_sha256=registry['driver']['sha256'])
        rec['inventory'] = store.put('INVENTORY.json', inv)
        rec['inventory_complete'] = inv.get('complete') is True
        if not rec['inventory_complete']:
            rec['blockers'] += ['INVENTORY: %s' % b for b in inv.get('blockers') or []] or ['INVENTORY_INCOMPLETE']
        # ---- A162 item 2: S5 exports, verified; the accepted state from the call's own manifest
        state_inputs = {}
        exports = policy.get('rebuild_exports') or {}
        need(isinstance(exports, dict), 'REBUILD_EXPORTS_NOT_A_MAP')
        rec['rebuild_exports'] = {}
        if inv.get('complete') is True:
            for s in inv['states']:
                if s['state_sha256'] == inv['accepted_state_sha256']:
                    continue
                ref = exports.get(s['state_sha256'])
                try:
                    v = S.verify_export(ref, call_result=rec['result'], state=s)
                    state_inputs[s['state_sha256']] = dict(ref)
                    rec['rebuild_exports'][s['state_sha256']] = {'input': dict(ref), 'admission': v['admission']}
                except (S.Refusal, Refusal, OSError, ValueError, KeyError, TypeError) as exc:
                    rec['blockers'].append('REBUILD_EXPORT_REFUSED %s: %s' % (s['state_sha256'][:16], exc))
            man = read_pin(inv['manifest'])
            acc = [s for s in inv['states'] if s['state_sha256'] == inv['accepted_state_sha256']]
            need(len(acc) == 1, 'ACCEPTED_STATE_NOT_UNIQUE')
            rref = store.put('ACCEPTED_TAILSTATE_RECORD.json', man['state']['record'])
            state_inputs[acc[0]['state_sha256']] = store.put('ACCEPTED_STATE_INPUT.json', {
                'schema': STATE_INPUT_SCHEMA, 'state': acc[0], 'call_result': rec['result'], 'source': 'ROUTE_A_TAIL_MANIFEST',
                'tail_state': {'record': rref, 'arrays': dict(man['state']['arrays'])}})
        if s2_block:
            rec['blockers'].append(s2_block)
        lo_root = os.path.join(store.dir, ADAPTER_DIR)
        os.mkdir(lo_root)
        call_rec = adapter_fn(
            call_dir=rec['call_dir'], spec_ref=spec_ref, inventory=inv, state_inputs=state_inputs,
            row_contract_ref=dict(contract_pin), row_policy_review_ref=policy.get('row_policy_review'),
            slot_proof_ref=policy.get('slot_proof'), rho_producer_ref=policy.get('rho_producer'),
            approved_producer_sha256=policy.get('approved_producer_sha256') or (),
            approved_slot_proof_producer_sha256=approved_slot, approved_rho_producer_sha256=approved_rho,
            approved_rebuild_producer_sha256=[approvals['s5']['sha256']],
            trusted_row_policy_review_sha256=policy.get('trusted_row_policy_review_sha256') or (), out_root=lo_root)
        rec['lo_adapter_call_record'] = store.put('LO_ADAPTER_CALL_RECORD.json', call_rec)
        rec['t_rule_id'] = call_rec.get('t_rule_id')
        rec['blockers'] += ['ADAPTER: %s' % b for b in call_rec.get('blockers') or []]
        need(call_rec.get('registry_kind') == registry['kind'], 'ADAPTER_REGISTRY_KIND')
        need(call_rec.get('is_anchor') is False and 'ANCHOR' not in str(call_rec.get('call_lo_reading')).upper(),
             'ANCHOR_CLASS_EMITTED (NGC has no anchor class)')
        need(call_rec.get('scope_disclosure') == A.SCOPE_DISCLOSURE, 'CALL_RECORD_WITHOUT_THE_A153_SCOPE_TEXT')
        need(call_rec.get('pass_meaning') == A.PASS_MEANING, 'CALL_RECORD_WITHOUT_THE_E_A155_1_PASS_MEANING')
        if inv.get('complete') is True:
            adopt(rec, inv, call_rec, A, registry['kind'])
        rec['reading'], rec['all_readings'] = readings(rec)
        mapped = {'PASS': 'ACCEPTED'}.get(call_rec.get('call_lo_reading'), call_rec.get('call_lo_reading'))
        if mapped != rec['reading'] and not (mapped == 'INCOMPLETE' and rec['blockers']):
            rec['blockers'].append('HANDOFF_AND_ADAPTER_READINGS_DIFFER: %s / %s' % (rec['reading'], mapped))
            rec['reading'] = rec['reading'] if rec['reading'] == 'NON_LAPSE_TAIL_MATERIAL' else 'INCOMPLETE'   # A48
        # ---- A162 item 5: SRB-ROT, report-only (after the reading; it never changes it)
        if inv.get('complete') is True:
            rec['srb_rot_report'] = srb_rot_report(store=store, out=out, result=result, inv=inv, spec=spec,
                                                   cert_ref=policy.get('eps_certificate'), state_inputs=state_inputs,
                                                   lib=lib, rowmod=rowmod)
    except (Refusal, ValueError, KeyError, TypeError, OSError, AttributeError) as exc:
        if str(exc) not in rec['blockers']:
            rec['blockers'].append('%s: %s' % (type(exc).__name__, exc))
        rec['reading'] = 'INCOMPLETE'
    rec['member_lo_ok'] = rec['reading'] in MEMBER_LO_OK
    rec['rows_are_model_output'] = False if rec['reading'] == 'NON_LAPSE_TAIL_MATERIAL' else None
    rec['root_summary'] = store.put('ROOT_SUMMARY.json', blinded_summary(rec))
    rec['files'] = list(store.files)
    return rec, store.put('ACCEPTANCE_RECORD.json', rec)


def load_modules():
    E = load_pinned(ENUMERATOR, 'ngc_handoff_c2v003a_enumerator')
    A = load_pinned(LO_ADAPTER, 'ngc_handoff_c2v003a_adapter')
    R = load_pinned(ITERATE_READER, 'ngc_handoff_c2v003a_iterate_reader')
    S = load_pinned(S5_TOOL, 'ngc_handoff_c2v003a_s5_tool')
    lib = load_pinned(LIBRARY, 'ngc_handoff_c2v003a_owned_uv_tail_lapse_v002')
    rowmod = load_pinned(ROW_PRODUCER, 'ngc_handoff_c2v003a_row_reference_producer_c2v003')
    need(R.S5_TOOL == (S5_TOOL['path'], S5_TOOL['sha256']), 'READER_DOES_NOT_PIN_THIS_S5_TOOL')
    return E, A, R, S, lib, rowmod


def accept_call_ngc(*, call_dir, spec_ref, policy, records_dir):
    """Public entry: the pinned enumerator, adapter, reader, S5 tool, contract and S2 pins (REGISTERED registry)."""
    E, A, R, S, lib, rowmod = load_modules()
    fn = getattr(A, LO_ADAPTER['entry'])
    need(fn.__code__.co_filename == LO_ADAPTER['path'], 'LO_ADAPTER_CALLABLE_NOT_THE_PINNED_ENTRY')
    return _accept(call_dir=call_dir, spec_ref=spec_ref, policy=policy, records_dir=records_dir,
                   enumerate_fn=getattr(E, ENUMERATOR['entry']), adapter_fn=fn, A=A, registry=A.real_registry(), R=R, S=S,
                   s2_pins=dict(S2_PINS), contract_pin=dict(ROW_CONTRACT), lib=lib, rowmod=rowmod,
                   approvals={'reader': dict(ITERATE_READER), 's5': dict(S5_TOOL)})


def prepare_acceptance_inputs(*, call_dir, recipe_ref, approved_recipe_sha256, out_dir, driver_sha256=None, modules=None):
    """Root's pre-step (A162 items 1-2), before accept_call_ngc: enumerate the sidecar (reader), rebuild and admit every
    non-accepted iterate (S5), write the iterate list (reader), enumerate the call (enumerator c2v001), rebuild and admit
    every route-B state (S5), and export a state input for every non-accepted inventory state (S5). Returns the policy
    fragment {route_a_iterates, rebuild_exports} plus every admission pin; nothing here reads or computes an LO value."""
    E, A, R, S = (modules or load_modules())[:4]
    drv = driver_sha256 or A.DRIVER['sha256']
    out_dir = os.path.realpath(out_dir)
    os.mkdir(out_dir)
    enum = R.enumerate_sidecar(call_dir, driver_sha256=drv)
    admissions = {}
    for tg in R.s5_targets(enum):
        admissions[tg['state']['state_sha256']] = S.rebuild_admit(call_dir=call_dir, target=tg, recipe_ref=recipe_ref,
                                                                  approved_recipe_sha256=approved_recipe_sha256,
                                                                  out_dir=out_dir, driver_sha256=drv)
    lst = R.write_iterate_list(call_dir, admissions, out_dir, driver_sha256=drv)
    inv = E.enumerate_call(call_dir, route_a_iterates_ref=lst, approved_iterate_producer_sha256=[R.self_pin()['sha256']],
                           driver_sha256=drv)
    need(inv.get('complete') is True, 'INVENTORY_INCOMPLETE: %s' % inv.get('blockers'))
    exports = {}
    for tg in S.targets_from_inventory(inv):
        d = tg['state']['state_sha256']
        if d not in admissions:
            admissions[d] = S.rebuild_admit(call_dir=call_dir, target=tg, recipe_ref=recipe_ref,
                                            approved_recipe_sha256=approved_recipe_sha256, out_dir=out_dir,
                                            driver_sha256=drv)
        exports[d] = S.export_state_input(admission_ref=admissions[d], state=tg['state'], out_dir=out_dir)
    return {'route_a_iterates': lst, 'rebuild_exports': exports, 'admissions': admissions}


def _background_qos():
    try:
        return os.getpriority(4, 0) == 1
    except Exception:
        return False


def main(argv=None):
    """CLI (root): taskpolicy -b python3 -I -B ngc_acceptance_handoff_c2v003a.py --args A --args-sha256 S --records-dir D.
    Prints the blinded summary only (S12)."""
    if not _background_qos():
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        return 2
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B, no -O)', flush=True)
        return 2
    import argparse
    ap = argparse.ArgumentParser(description='NGC LO acceptance handoff c2v003a (A153 S11; A155; A162; A167)')
    ap.add_argument('--args', required=True, help='JSON: call_dir, spec_ref, policy')
    ap.add_argument('--args-sha256', required=True)
    ap.add_argument('--records-dir', required=True)
    a = ap.parse_args(argv)
    try:
        args = read_pin({'path': os.path.realpath(a.args), 'sha256': a.args_sha256})
        rec, pin = accept_call_ngc(call_dir=args['call_dir'], spec_ref=args['spec_ref'], policy=args['policy'],
                                   records_dir=a.records_dir)
    except (Refusal, ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'reading': 'INCOMPLETE', 'blockers': ['%s: %s' % (type(exc).__name__, exc)]}), flush=True)
        return 3
    print(json.dumps(dict(blinded_summary(rec), record=pin)), flush=True)
    return 0 if rec['reading'] == 'ACCEPTED' else 3


if __name__ == '__main__':
    for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
               'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        os.environ[_k] = '1'          # before numpy loads (every numpy import here is lazy): the G4 rho condition
    sys.exit(main())
