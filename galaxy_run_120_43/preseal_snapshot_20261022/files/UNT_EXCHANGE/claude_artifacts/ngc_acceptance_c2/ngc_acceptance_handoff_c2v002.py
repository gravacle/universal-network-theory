"""NGC acceptance handoff c2v002 (V006 A153 S11 + A155; text of record NGC_LO_QUANTITY_RULING_DRAFT_WF_A88C2E94.md
9916cb6f). Root build (Claude2 workflow); nothing here is adopted until root rules and a distinct lane reviews.

c2v002 delta from c2v001 (2ed50410): it pins the A155 successor adapter ngc_lo_state_adapter_c2v002 (t_i never stored;
the TI_B_SCALE_R_V001 ratio form; an empty row set reads LO_ROW_SET_EMPTY, never a PASS), carries and checks the E_A155_1
PASS meaning, and writes C2V002 record schemas. The enumerator pin (c2v001, 607b7f66) is unchanged.

acceptance_handoff_c2v004 (5ff464cc) is DDO-only (L43, L199). This is the NGC handoff for route
NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE (A136 G5). Root runs accept_call_ngc() once per NGC call after the call's
FINISHED receipt and before any value from the call is scored, adopted or reported. It is glue around two pinned modules:
  - the enumerator ngc_consumed_states_c2v001 (S9), by exact path and sha;
  - the per-state adapter ngc_lo_state_adapter_c2v002 (S1, S3-S8, S10, S13; A155), by exact path and sha, entry
    adapt_call_ngc_lo (the REGISTERED registry only).
It never approves and never writes a proof. Its scope is the LO acceptance only (A152 W-3 reads it for member_valid);
GQ and SRB-ROT are not read here.

What it adds to the adapter:
  - the FINISHED receipt gate (v004 receipt_ok: FINISHED, driver COMPLETED, result sha);
  - the accepted route-A state input from the call's own ROUTE_A_TAIL_MANIFEST (S5): the manifest record written here,
    the manifest's arrays pin carried unchanged; every other state's input is root's rebuild export (OPEN INTERFACE);
  - adoption: every per-state record is re-read from its exact pin and must carry the A153 scope disclosure and the
    E_A155_1 PASS meaning, a FAIL the FAIL text, no anchor class, no stored t_i, a PASS or FAIL a non-empty arithmetic
    row set, and the expected registry kind; the call reading is recomputed here (A134 Q5 / 0690 OPEN-6, no anchor)
    and must agree with the adapter's;
  - S12 blinding: ROOT_SUMMARY.json and the CLI output carry only verdicts, reason codes and shell coverage flags; the
    values stay in the per-state record files.
Readings: ACCEPTED (every consumed state PASS), NON_LAPSE_TAIL_MATERIAL (a FAIL at the accepted, an inherited or a
route-B state; decisive even with other states UNAVAILABLE), LO_UNCERTIFIED_TRANSIENT (FAIL confined to route-A
pre-acceptance iterates with every non-iterate state PASS), INCOMPLETE (otherwise; the call is preserved and the member is
invalid at the freeze). The adapter pins root's t_i entry (V006 A155). A contract without the rule reads
NGC_LO_TOLERANCE_NOT_DECLARED; theta or c bits that differ read NGC_LO_TOLERANCE_RULE_MISMATCH; an empty row set reads
LO_ROW_SET_EMPTY; each makes the call INCOMPLETE: UNTESTED, not a null.
"""
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
LO_ADAPTER = {'path': os.path.join(HERE, 'ngc_lo_state_adapter_c2v002.py'), 'sha256': 'ce33b526c38490687744d6b9a4b383cb540c1af6a8da7d8d4f0298807ce43047',
              'entry': 'adapt_call_ngc_lo'}
ENUMERATOR = {'path': os.path.join(HERE, 'ngc_consumed_states_c2v001.py'), 'sha256': '607b7f667dfa1612da3fd874ab2656dc5ca487285a28afb2e4b1bfe979bd3125',
              'entry': 'enumerate_call'}
RECORD_SCHEMA = 'UNT_NGC_LO_ACCEPTANCE_RECORD_C2V002'
SUMMARY_SCHEMA = 'UNT_NGC_LO_ACCEPTANCE_ROOT_SUMMARY_C2V002'
STATE_INPUT_SCHEMA = 'UNT_NGC_LO_STATE_INPUT_C2V001'
ROUTE = 'NGC_POINT_RHO_POST_RUN_PER_STATE_LO_ACCEPTANCE'
READINGS = ('NON_LAPSE_TAIL_MATERIAL', 'LO_UNCERTIFIED_TRANSIENT', 'INCOMPLETE', 'ACCEPTED')   # precedence
MEMBER_LO_OK = ('ACCEPTED', 'LO_UNCERTIFIED_TRANSIENT')                                      # A152 W-3 / A134
DECISIVE = ('ACCEPTED_ROUTE_A', 'INHERITED_ROUTE_A', 'ROUTE_B_STAGE')
ITERATE = 'ROUTE_A_PRE_ACCEPTANCE_ITERATE'
ADAPTER_DIR = 'LO_ADAPTER_C2'
C_ADMISSION = 'NGC_LO_ADAPTER_NOT_ADMITTED'
POLICY_KEYS = ('receipt', 'route_a_iterates', 'approved_iterate_producer_sha256', 'rebuild_exports', 'row_contract',
               'row_policy_review', 'slot_proof', 'rho_producer', 'approved_producer_sha256',
               'approved_slot_proof_producer_sha256', 'approved_rho_producer_sha256', 'approved_rebuild_producer_sha256',
               'trusted_row_policy_review_sha256', 'high_qinf_admitted')


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


def self_pin():
    p = os.path.realpath(__file__)
    with open(p, 'rb') as f:
        return {'path': p, 'sha256': hashlib.sha256(f.read()).hexdigest()}


def read_pin(ref):
    need(is_pin(ref) and os.path.isabs(ref['path']), 'NOT_AN_EXACT_PIN')
    real = os.path.realpath(ref['path'])
    need('ngc3198' not in os.path.basename(real).lower(), 'NGC3198_NAMED_FILE_REFUSED')
    with open(real, 'rb') as f:
        raw = f.read()
    need(hashlib.sha256(raw).hexdigest() == ref['sha256'], 'BYTE_PIN_MISMATCH: ' + ref['path'])
    return json.loads(raw)


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
            A.guard_state_record(r)                                     # scope text, FAIL text, no anchor
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
    """S12: verdicts, reason codes and shell coverage flags only."""
    return {'schema': SUMMARY_SCHEMA, 'route': ROUTE, 'reading': rec['reading'], 'member_lo_ok': rec['member_lo_ok'],
            'high_qinf_ngc_lo_flagged': rec.get('high_qinf_ngc_lo_flagged'), 'registry_kind': rec.get('registry_kind'),
            't_rule_id': rec.get('t_rule_id'), 'blockers': list(rec['blockers']),
            'states': [{'state_sha256': e['state']['state_sha256'], 'stage_kind': e['state']['stage_kind'],
                        'class': e['class'], 'verdict': e['verdict'], 'reading': e['reading'], 'codes': e['codes'],
                        'coverage_flags': e.get('coverage_flags')} for e in rec['states']],
            'scope_disclosure': rec.get('scope_disclosure'), 'pass_meaning': rec.get('pass_meaning'), 'is_anchor': False}


def _accept(*, call_dir, spec_ref, policy, records_dir, enumerate_fn, adapter_fn, A, registry):
    store = Store(records_dir)
    rec = {'schema': RECORD_SCHEMA, 'route': ROUTE, 'call_dir': os.path.realpath(str(call_dir)), 'reading': 'INCOMPLETE',
           'blockers': [], 'states': [], 'registry_kind': registry['kind'], 'is_anchor': False,
           'scope_disclosure': A.SCOPE_DISCLOSURE, 'pass_meaning': A.PASS_MEANING, 'handoff': self_pin()}
    rec['pins'] = {'lo_adapter': dict(LO_ADAPTER), 'enumerator': dict(ENUMERATOR)}
    rec['high_qinf_ngc_lo_flagged'] = True if (policy or {}).get('high_qinf_admitted') is True else None
    try:
        need(isinstance(policy, dict) and set(policy) <= set(POLICY_KEYS), 'POLICY_KEYS')
        out = os.path.realpath(os.path.join(rec['call_dir'], 'out'))
        rp = os.path.join(out, 'result.json')
        with open(rp, 'rb') as f:
            rraw = f.read()
        rec['result'] = {'path': rp, 'sha256': hashlib.sha256(rraw).hexdigest()}
        if not (is_pin(policy.get('receipt')) and receipt_ok(policy['receipt'], rec['result']['sha256'])):
            rec['blockers'].append('FINISHED_RECEIPT_REQUIRED')
            raise Refusal('FINISHED_RECEIPT_REQUIRED')
        inv = enumerate_fn(rec['call_dir'], route_a_iterates_ref=policy.get('route_a_iterates'),
                           approved_iterate_producer_sha256=policy.get('approved_iterate_producer_sha256') or (),
                           driver_sha256=registry['driver']['sha256'])
        rec['inventory'] = store.put('INVENTORY.json', inv)
        rec['inventory_complete'] = inv.get('complete') is True
        if not rec['inventory_complete']:
            rec['blockers'] += ['INVENTORY: %s' % b for b in inv.get('blockers') or []] or ['INVENTORY_INCOMPLETE']
        state_inputs = dict(policy.get('rebuild_exports') or {})
        if inv.get('complete') is True:
            man = read_pin(inv['manifest'])
            acc = [s for s in inv['states'] if s['state_sha256'] == inv['accepted_state_sha256']]
            need(len(acc) == 1, 'ACCEPTED_STATE_NOT_UNIQUE')
            rref = store.put('ACCEPTED_TAILSTATE_RECORD.json', man['state']['record'])
            state_inputs[acc[0]['state_sha256']] = store.put('ACCEPTED_STATE_INPUT.json', {
                'schema': STATE_INPUT_SCHEMA, 'state': acc[0], 'call_result': rec['result'], 'source': 'ROUTE_A_TAIL_MANIFEST',
                'tail_state': {'record': rref, 'arrays': dict(man['state']['arrays'])}})
        lo_root = os.path.join(store.dir, ADAPTER_DIR)
        os.mkdir(lo_root)
        call_rec = adapter_fn(
            call_dir=rec['call_dir'], spec_ref=spec_ref, inventory=inv, state_inputs=state_inputs,
            row_contract_ref=policy.get('row_contract'), row_policy_review_ref=policy.get('row_policy_review'),
            slot_proof_ref=policy.get('slot_proof'), rho_producer_ref=policy.get('rho_producer'),
            approved_producer_sha256=policy.get('approved_producer_sha256') or (),
            approved_slot_proof_producer_sha256=policy.get('approved_slot_proof_producer_sha256') or (),
            approved_rho_producer_sha256=policy.get('approved_rho_producer_sha256') or (),
            approved_rebuild_producer_sha256=policy.get('approved_rebuild_producer_sha256') or (),
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
    except (Refusal, ValueError, KeyError, TypeError, OSError, AttributeError) as exc:
        if str(exc) not in rec['blockers']:
            rec['blockers'].append('%s: %s' % (type(exc).__name__, exc))
        rec['reading'] = 'INCOMPLETE'
    rec['member_lo_ok'] = rec['reading'] in MEMBER_LO_OK
    rec['rows_are_model_output'] = False if rec['reading'] == 'NON_LAPSE_TAIL_MATERIAL' else None
    rec['root_summary'] = store.put('ROOT_SUMMARY.json', blinded_summary(rec))
    rec['files'] = list(store.files)
    return rec, store.put('ACCEPTANCE_RECORD.json', rec)


def accept_call_ngc(*, call_dir, spec_ref, policy, records_dir):
    """Public entry: the pinned enumerator and adapter (REGISTERED registry)."""
    E = load_pinned(ENUMERATOR, 'ngc_handoff_c2v002_enumerator')
    A = load_pinned(LO_ADAPTER, 'ngc_handoff_c2v002_adapter')
    fn = getattr(A, LO_ADAPTER['entry'])
    need(fn.__code__.co_filename == LO_ADAPTER['path'], 'LO_ADAPTER_CALLABLE_NOT_THE_PINNED_ENTRY')
    return _accept(call_dir=call_dir, spec_ref=spec_ref, policy=policy, records_dir=records_dir,
                   enumerate_fn=getattr(E, ENUMERATOR['entry']), adapter_fn=fn, A=A, registry=A.real_registry())


def _background_qos():
    try:
        return os.getpriority(4, 0) == 1
    except Exception:
        return False


def main(argv=None):
    """CLI (root): taskpolicy -b python3 -I -B ngc_acceptance_handoff_c2v002.py --args A --args-sha256 S --records-dir D.
    Prints the blinded summary only (S12)."""
    if not _background_qos():
        print('REFUSED: BACKGROUND_QOS_REQUIRED (run under taskpolicy -b)', flush=True)
        return 2
    if not (sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0):
        print('REFUSED: ISOLATED_INTERPRETER_REQUIRED (python3 -I -B, no -O)', flush=True)
        return 2
    import argparse
    ap = argparse.ArgumentParser(description='NGC LO acceptance handoff c2v002 (A153 S11; A155)')
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
