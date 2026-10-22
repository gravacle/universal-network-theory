#!/usr/bin/env python3
"""build_stage0_successor_c2v001 -- builds the STAGE0-only successor of the v003g freeze module.

Reads the v003g module bytes (sha256 verified), applies a fixed list of exact-once text replacements (each one is
named and must match exactly one place), and writes the successor by exclusive create. Nothing else is read or
written. Usage: python3 -I -B build_stage0_successor_c2v001.py OUT_PATH
"""
import hashlib
import sys

V003G_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/'
              'prediction_freeze_c2v003g_cx3v001.py')
V003G_SHA256 = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'

STAGE0_BLOCK = r'''

# --------------------------------------------------------------------------
# STAGE0 successor (root V006 A142; r3a ROOT_ITEMS M-14; prereg r3a section 6.3) -- the only new behaviour
# --------------------------------------------------------------------------
# STAGE0_GRID_OUTER may read EVALUATED_BEFORE_FREEZE in a Phase-2 freeze, and only by the receipt rule below. Its
# slots V003 record (scope OUTER Q36-Q43, coefficient grid pin, headline false) is unchanged, and so is the slots pin
# (ROOT_SLOTS_PATH / ROOT_SLOTS_SHA256). The successor only PERMITS EVALUATED: every other outcome freezes STAGE0
# NOT_EVALUATED_BEFORE_FREEZE with its codes, and STAGE0 never makes a freeze refuse. The rule reads root-written
# status and receipt bytes only (identities, terminal statuses, times); it never reads an output value.

STAGE0_ALTERNATIVE = 'STAGE0_GRID_OUTER'
STAGE0_STATUS_RECORD_SCHEMA = 'STAGE0_STATUS_RECORD_C2V001'
STAGE0_RECEIPT_SCHEMA = 'STAGE0_TERMINAL_RECEIPT_C2V001'
STAGE0_STATUS_RECORD_KEYS = frozenset({'schema', 'phase', 'alternative', 'sealed_successor', 'step4_start_utc',
                                       'receipts'})
STAGE0_SEALED_SUCCESSOR_KEYS = frozenset({'module_sha256', 'source'})
STAGE0_RECEIPT_ENTRY_KEYS = frozenset({'member_log_index', 'receipt'})
STAGE0_RECEIPT_KEYS = frozenset({'schema', 'alternative', 'member_log_index', 'theta_ngc', 'coefficient_grid_sha256',
                                 'terminal_status', 'written_utc'})
STAGE0_PHASE_1 = 'PHASE_1'
STAGE0_PHASE_2 = 'PHASE_2'
STAGE0_FINISHED = 'FINISHED'
STAGE0_EVALUATED_REFUSED = 'EVALUATED_REFUSED'
STAGE0_NOT_IN_PHASE_1 = 'NOT_IN_PHASE_1'
STAGE0_RECEIPT_NOT_FINISHED = 'STAGE0_RECEIPT_NOT_FINISHED'
STAGE0_NO_SEALED_SUCCESSOR = 'NO_SEALED_SUCCESSOR'
STAGE0_RECEIPTS_AFTER_STEP4 = 'RECEIPTS_AFTER_STEP4'
STAGE0_UTC_FORMATS = ('%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S.%fZ')
STAGE0_MEMBER_KEYS = frozenset({'member_id', 'log_index', 'receipt', 'custody_ok', 'terminal_status', 'written_utc',
                                'finished', 'before_step4', 'defects'})
STAGE0_BLOCK_KEYS = frozenset({'rule', 'alternative', 'module', 'successor_module_sha256', 'status_record',
                               'status_record_custody_ok', 'phase', 'sealed_successor', 'step4_start_utc', 'members',
                               'rule_a_receipts_finished', 'rule_b_successor_sealed', 'receipts_before_step4',
                               'receipt_refusals', 'evaluation_refusals', 'diagnostics', 'reading', 'reasons',
                               'post_score_exploratory'})
STAGE0_RULE = (
    'M-14 receipt rule (r3a ROOT_ITEMS M-14 = prereg r3a section 6.3; root V006 A142). Phase 1: STAGE0_GRID_OUTER reads '
    'NOT_EVALUATED_BEFORE_FREEZE with NOT_IN_PHASE_1. Phase 2: it is EVALUATED_BEFORE_FREEZE iff (a) every registered '
    'STAGE0 member (one STAGE0 call per PRIMARY member) has exactly one custody-verified terminal receipt reading '
    'FINISHED, (b) the root STAGE0 status record names the sha256 of this module as the sealed successor, every '
    'FINISHED receipt was written no later than the recorded Phase-2 step-4 start (a receipt written at that instant '
    'counts as before), and this successor refuses no STAGE0 record. Otherwise it reads NOT_EVALUATED_BEFORE_FREEZE '
    'with every code that applies (STAGE0_RECEIPT_NOT_FINISHED, NO_SEALED_SUCCESSOR, RECEIPTS_AFTER_STEP4: '
    'exploratory, post-score), or EVALUATED_REFUSED when the receipt rule holds and a STAGE0 record is refused. '
    'Validity booleans and output values never change the status. STAGE0 never makes the freeze refuse and never '
    'enters the headline; when evaluated it is scored on its registered OUTER rows only.')


def _stage0_neutral_record(a):
    """A STAGE0_GRID_OUTER record that reads EVALUATED_BEFORE_FREEZE, with its status put back to the slots V003
    value NOT_EVALUATED_BEFORE_FREEZE; every other value is returned unchanged. Wherever v003g compared a record to
    slots V003 exactly, the successor compares through this, so the only difference ever tolerated is STAGE0's
    status (and _stage0_manifest_check binds that status to the receipt rule)."""
    if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE and a.get('status') == ALT_EVALUATED:
        return dict(a, status=ALT_NOT_EVALUATED)
    return a


def _stage0_status_neutral(alternatives):
    """The alternatives declaration with _stage0_neutral_record applied to every declared record."""
    if not isinstance(alternatives, dict) or not isinstance(alternatives.get('declared'), list):
        return alternatives
    return dict(alternatives, declared=[_stage0_neutral_record(a) for a in alternatives['declared']])


def _stage0_effective_alternatives(alternatives):
    """The slots alternatives with STAGE0's status EVALUATED_BEFORE_FREEZE (used only once the receipt rule held)."""
    return dict(alternatives, declared=[dict(a, status=ALT_EVALUATED)
                                        if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE else a
                                        for a in alternatives['declared']])


def _stage0_split_evaluations(alternative_evaluations):
    """(the evaluations without STAGE0, the STAGE0 evaluation or None)."""
    if not isinstance(alternative_evaluations, dict) or STAGE0_ALTERNATIVE not in alternative_evaluations:
        return alternative_evaluations, None
    rest = {k: v for k, v in alternative_evaluations.items() if k != STAGE0_ALTERNATIVE}
    return rest, alternative_evaluations[STAGE0_ALTERNATIVE]


def _stage0_registered():
    """The slots V003 STAGE0_GRID_OUTER record (None if the pinned slots declare none)."""
    for a in _root_slots()[0]['alternatives']['declared']:
        if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE:
            return a
    return None


def _stage0_self_sha256():
    """sha256 of this module's own file bytes: the sha rule (b) needs the seal entry to pin."""
    raw, _real, _err = _read_regular(os.path.realpath(__file__), True)
    return _sha256_hex(raw) if raw is not None else None


def _stage0_utc(value):
    """A root-recorded UTC time written exactly in one of STAGE0_UTC_FORMATS; None otherwise."""
    if not isinstance(value, str):
        return None
    for fmt in STAGE0_UTC_FORMATS:
        try:
            t = datetime.datetime.strptime(value, fmt)
        except ValueError:
            continue
        if t.strftime(fmt) == value:
            return t
    return None


def _stage0_pin(pin):
    """A well-formed {'path', 'sha256'} pin, normalised to (realpath, lowercase sha256); None otherwise."""
    if isinstance(pin, dict) and set(pin) == {'path', 'sha256'} and isinstance(pin['path'], str) and pin['path'] \
            and _is_hex64(pin['sha256']):
        return {'path': os.path.realpath(pin['path']), 'sha256': pin['sha256'].lower()}
    return None


def _stage0_read(pin, where):
    """(doc, None) for a custody-verified (sha256 from the bytes), target-screened JSON object; (None, code)
    otherwise. A STAGE0 file defect is a code, never a refusal."""
    try:
        doc, _canonical_pin = _root_pinned_document(pin, where)
    except Exception as exc:   # noqa: BLE001
        text = _safe_str(exc)
        if text.startswith('ROOT_ROSTER_PIN_MISMATCH'):
            return None, 'CUSTODY_MISMATCH'
        if text.startswith('ROOT_ROSTER_TARGET_FIELDS_REFUSED'):
            return None, 'TARGET_FIELDS_REFUSED'
        return None, 'MALFORMED'
    return doc, None


def _stage0_same_theta(a, b):
    """Exact theta identity (same keys, equal finite values): the receipt is for this member's call."""
    return bool(isinstance(a, dict) and isinstance(b, dict) and set(a) == set(b)
                and all(_is_real(a[k]) and _is_real(b[k]) and float(a[k]) == float(b[k]) for k in a))


def _stage0_members_of(members):
    """The registered STAGE0 members: one per PRIMARY member, in member order ([] if the list is malformed)."""
    try:
        return [{'member_id': m['member_id'], 'log_index': int(m['log_index']), 'theta_ngc': dict(m['theta_ngc'])}
                for m in members]
    except Exception:   # noqa: BLE001 -- a malformed PRIMARY list refuses elsewhere (v003g checks)
        return []


def _stage0_apply_record(v, members):
    """Fill the verdict v from the status record and its receipts (helper of _stage0_receipt_verdict)."""
    pin = v['status_record']
    if pin is None:
        v['diagnostics'].append('STAGE0_STATUS_RECORD_NOT_SUPPLIED')
        return
    doc, err = _stage0_read(pin, 'STAGE0 status record')
    if doc is None:
        v['diagnostics'].append('STAGE0_STATUS_RECORD_' + err)
        return
    v['status_record_custody_ok'] = True
    if set(doc) != STAGE0_STATUS_RECORD_KEYS or doc['schema'] != STAGE0_STATUS_RECORD_SCHEMA or \
            doc['alternative'] != STAGE0_ALTERNATIVE or doc['phase'] not in (STAGE0_PHASE_1, STAGE0_PHASE_2):
        v['diagnostics'].append('STAGE0_STATUS_RECORD_MALFORMED')
        return
    v['phase'] = doc['phase']
    if doc['phase'] == STAGE0_PHASE_1:
        return   # NOT_IN_PHASE_1: no receipt is read
    ss, st, receipts = doc['sealed_successor'], doc['step4_start_utc'], doc['receipts']
    if not (ss is None or (isinstance(ss, dict) and set(ss) == STAGE0_SEALED_SUCCESSOR_KEYS
                           and _is_hex64(ss['module_sha256']) and isinstance(ss['source'], str)
                           and ss['source'].strip())) \
            or _stage0_utc(st) is None or not isinstance(receipts, list):
        v['diagnostics'].append('STAGE0_STATUS_RECORD_MALFORMED')
        return
    step4 = _stage0_utc(st)
    v['step4_start_utc'] = st
    if ss is None:
        v['diagnostics'].append('STAGE0_SEALED_SUCCESSOR_NOT_NAMED')
    else:
        v['sealed_successor'] = {'module_sha256': ss['module_sha256'].lower(), 'source': ss['source']}
        v['rule_b_successor_sealed'] = v['sealed_successor']['module_sha256'] == v['successor_module_sha256']
        if not v['rule_b_successor_sealed']:
            v['diagnostics'].append('STAGE0_SEALED_SUCCESSOR_IS_NOT_THIS_MODULE')
    registered = _stage0_registered()
    grid = registered.get('coefficient_grid_pin') if isinstance(registered, dict) else None
    grid_sha = grid.get('sha256') if isinstance(grid, dict) else None
    member_lis = set(m['log_index'] for m in members)
    found = {}
    for i, entry in enumerate(receipts):
        li = entry.get('member_log_index') if isinstance(entry, dict) else None
        if not isinstance(entry, dict) or set(entry) != STAGE0_RECEIPT_ENTRY_KEYS or not _is_int(li) or \
                _stage0_pin(entry['receipt']) is None:
            v['receipt_refusals'].append('STAGE0_RECEIPT_ENTRY_MALFORMED: receipts[%d]' % i)
            continue
        if int(li) not in member_lis:
            v['receipt_refusals'].append('STAGE0_RECEIPT_NON_MEMBER: receipts[%d] member_log_index %d' % (i, int(li)))
            continue
        found.setdefault(int(li), []).append(_stage0_pin(entry['receipt']))
    for row, m in zip(v['members'], members):
        got = found.get(m['log_index'], [])
        if not got:
            row['defects'].append('STAGE0_RECEIPT_MISSING')
            continue
        if len(got) > 1:
            row['defects'].append('STAGE0_RECEIPT_DUPLICATE')
            continue
        row['receipt'] = got[0]
        rdoc, rerr = _stage0_read(got[0], 'STAGE0 terminal receipt')
        if rdoc is None:
            row['defects'].append('STAGE0_RECEIPT_' + rerr)
            continue
        row['custody_ok'] = True
        if set(rdoc) != STAGE0_RECEIPT_KEYS or rdoc['schema'] != STAGE0_RECEIPT_SCHEMA or \
                not isinstance(rdoc['terminal_status'], str) or not rdoc['terminal_status'] or \
                _stage0_utc(rdoc['written_utc']) is None:
            row['defects'].append('STAGE0_RECEIPT_MALFORMED')
            continue
        row['terminal_status'] = rdoc['terminal_status']
        row['written_utc'] = rdoc['written_utc']
        if rdoc['alternative'] != STAGE0_ALTERNATIVE or not _is_int(rdoc['member_log_index']) or \
                int(rdoc['member_log_index']) != m['log_index'] or \
                not _stage0_same_theta(rdoc['theta_ngc'], m['theta_ngc']) or \
                not _is_hex64(grid_sha) or rdoc['coefficient_grid_sha256'] != grid_sha:
            row['defects'].append('STAGE0_RECEIPT_IDENTITY_MISMATCH')
            continue
        if rdoc['terminal_status'] != STAGE0_FINISHED:
            row['defects'].append('STAGE0_RECEIPT_TERMINAL_STATUS_NOT_FINISHED')
            continue
        row['finished'] = True
        row['before_step4'] = _stage0_utc(rdoc['written_utc']) <= step4
        if not row['before_step4']:
            row['defects'].append('STAGE0_RECEIPT_WRITTEN_AFTER_STEP4')
    v['rule_a_receipts_finished'] = bool(members) and all(r['finished'] for r in v['members'])
    v['receipts_before_step4'] = all(r['before_step4'] is not False for r in v['members'])


def _stage0_receipt_verdict(record_pin, members):
    """M-14 rule (a), rule (b) and the step-4 timing, from root-written bytes only (no output value is read).

    record_pin: the root STAGE0 status record pin {'path', 'sha256'} (schema STAGE0_STATUS_RECORD_C2V001) or None.
    members: _stage0_members_of(PRIMARY members) -- the registered STAGE0 members, one STAGE0 call per PRIMARY
    member. Every terminal receipt is read from its own bytes (sha256 verified, target-screened) and must name this
    alternative, the member's log_index and exact theta, and the slots V003 STAGE0 coefficient grid sha256. Returns
    the stage0_status fields other than the reading (_stage0_block adds it). Never raises."""
    v = {'successor_module_sha256': _stage0_self_sha256(), 'status_record': _stage0_pin(record_pin),
         'status_record_custody_ok': False, 'phase': None, 'sealed_successor': None, 'step4_start_utc': None,
         'members': [{'member_id': m['member_id'], 'log_index': m['log_index'], 'receipt': None, 'custody_ok': False,
                      'terminal_status': None, 'written_utc': None, 'finished': False, 'before_step4': None,
                      'defects': []} for m in members],
         'rule_a_receipts_finished': False, 'rule_b_successor_sealed': False, 'receipts_before_step4': True,
         'receipt_refusals': [], 'diagnostics': []}
    try:
        _stage0_apply_record(v, members)
    except Exception as exc:   # noqa: BLE001 -- never raises: a defect establishes neither (a) nor (b)
        v['rule_a_receipts_finished'] = v['rule_b_successor_sealed'] = False
        v['diagnostics'].append('STAGE0_RECEIPT_RULE_EXCEPTION: %s' % type(exc).__name__)
    return v


def _stage0_eligible(v):
    """Phase 2, rule (a), rule (b) and the step-4 timing all hold (refusals are judged after this)."""
    return bool(v['phase'] == STAGE0_PHASE_2 and v['rule_a_receipts_finished'] and v['rule_b_successor_sealed']
                and v['receipts_before_step4'])


def _stage0_block(v, evaluation_refusals):
    """The frozen stage0_status block: the receipt verdict plus the M-14 reading and its codes."""
    if v['phase'] == STAGE0_PHASE_1:
        reading, reasons = ALT_NOT_EVALUATED, [STAGE0_NOT_IN_PHASE_1]
    else:
        reasons = []
        if not v['rule_a_receipts_finished']:
            reasons.append(STAGE0_RECEIPT_NOT_FINISHED)
        if not v['rule_b_successor_sealed']:
            reasons.append(STAGE0_NO_SEALED_SUCCESSOR)
        if not v['receipts_before_step4']:
            reasons.append(STAGE0_RECEIPTS_AFTER_STEP4)
        if reasons:
            reading = ALT_NOT_EVALUATED
        elif v['receipt_refusals'] or evaluation_refusals:
            reading = STAGE0_EVALUATED_REFUSED
        else:
            reading = ALT_EVALUATED
    block = dict(v)
    block.update({'rule': STAGE0_RULE, 'alternative': STAGE0_ALTERNATIVE, 'module': MODULE_NAME,
                  'evaluation_refusals': list(evaluation_refusals), 'reading': reading, 'reasons': reasons,
                  'post_score_exploratory': STAGE0_RECEIPTS_AFTER_STEP4 in reasons})
    return block


def _stage0_custody_pins(block):
    """The custody-verified STAGE0 files (status record, member receipts): each must be pinned in input_files."""
    pins = [block['status_record']] if block['status_record_custody_ok'] else []
    return pins + [m['receipt'] for m in block['members'] if m['custody_ok']]


def _stage0_input_files(input_files, block):
    """input_files plus the custody-verified STAGE0 files (realpaths; a file already listed is not added again)."""
    have = set(os.path.realpath(p) for p in input_files if isinstance(p, str) and p)
    extra = [p['path'] for p in _stage0_custody_pins(block) if p['path'] not in have]
    return list(dict.fromkeys(list(input_files) + extra))


def _stage0_evaluation_refusals(ev, selection, spec, ids, roster, roster_pin):
    """Every check v003g applies to a frozen non-primary alternative (writer: ok, query ids, root roster pin, D2
    members; verifier: _validate_members / _validate_member_eval / _validate_envelope; _root_frozen_rows on its
    roster; canonical form; target screen), applied to the STAGE0 evaluation BEFORE it is admitted, plus COMPLETE
    status and member identity with the selection. Any failure is a STAGE0 record refusal (EVALUATED_REFUSED), so an
    admitted STAGE0 cannot make the freeze refuse. Returns the refusal codes ([] = admissible)."""
    try:
        if ev is None:
            return ['STAGE0_EVALUATION_NOT_SUPPLIED']
        if not isinstance(ev, dict) or ev.get('ok') is not True or ev.get('query_ids') != list(ids):
            return ['STAGE0_EVALUATION_NOT_OK']
        if roster is None or ev.get('row_registration_roster') != roster_pin:
            return ['STAGE0_EVALUATION_ROSTER_PIN_MISMATCH']
        if ev.get('status') != STATUS_COMPLETE:
            return ['STAGE0_EVALUATION_NOT_COMPLETE']
        if _canonical_bytes([_member_key(m, 'theta_engine') for m in ev['members']]) != \
                _canonical_bytes([_member_key(p, 'theta_natural') for p in selection['points']]):
            return ['STAGE0_EVALUATION_MEMBERS_NOT_THE_SELECTION']
        reasons = []
        S = _spec_from(spec, reasons)
        if S is None:
            return ['STAGE0_EVALUATION_SPEC_REFUSED']
        ar = selection['admitted_region']
        adm = {p['log_index']: p['projection'] for p in ar['admitted_projections_identified']}
        rec = _plain({'members': ev['members'], 'member_evaluation': _member_eval_record(ev),
                      'pointwise_envelope': ev['pointwise_envelope']}, 'stage0_evaluation')
        if _validate_members(rec['members'], S, ids, len(ar['identified']), 'stage0.members', reasons, adm):
            _validate_member_eval(rec['member_evaluation'], rec['members'], 'stage0.member_evaluation', reasons)
            _validate_envelope(rec['pointwise_envelope'], rec['members'], ids, 'stage0.pointwise_envelope', reasons,
                               _mode_labels(S)[0])
        if reasons:
            return ['STAGE0_EVALUATION_STRUCTURE: ' + _safe_str(reasons[0])[:_MAX_REASON_CHARS]]
        for m in rec['members']:
            _root_frozen_rows(m, list(ids), roster)
        hits = []
        _safe_scan(rec, 'stage0_evaluation', hits, reasons)
        if hits or reasons:
            return ['STAGE0_EVALUATION_TARGET_FIELDS_REFUSED']
        return []
    except Exception as exc:   # noqa: BLE001 -- a refusal of the STAGE0 record, never of the freeze
        return ['STAGE0_EVALUATION_REFUSED: %s: %s' % (type(exc).__name__, _safe_str(exc)[:200])]


def _stage0_freeze_decision(record_pin, evaluation, primary_evaluation, selection, spec, ids, roster, roster_pin):
    """Writer side of M-14. Returns (stage0_status block, admitted). Appends no refusal reason: when STAGE0 is not
    admitted it is frozen NOT_EVALUATED_BEFORE_FREEZE (its reading and codes in the block) and the freeze goes on."""
    members = _stage0_members_of(primary_evaluation.get('members') if isinstance(primary_evaluation, dict) else None)
    v = _stage0_receipt_verdict(record_pin, members)
    refusals = (_stage0_evaluation_refusals(evaluation, selection, spec, ids, roster, roster_pin)
                if _stage0_eligible(v) else [])
    block = _stage0_block(v, refusals)
    return block, block['reading'] == ALT_EVALUATED


def _stage0_manifest_check(doc, reasons):
    """Verifier side of M-14 (writer, verifier and scorer all run it): the frozen stage0_status block must equal the
    block the receipt rule recomputes from the pinned root bytes and the frozen PRIMARY members; STAGE0's declared
    status must follow its reading; an EVALUATED STAGE0 must be COMPLETE; and every custody-verified STAGE0 file must
    be pinned in input_files. The evaluation refusals (EVALUATED_REFUSED) are the writer's record: they are accepted
    only where the receipt rule holds. Appends reasons."""
    block = doc['stage0_status']
    if not isinstance(block, dict) or set(block) != STAGE0_BLOCK_KEYS:
        reasons.append('STAGE0_STATUS_BLOCK_MALFORMED: keys must be %s' % sorted(STAGE0_BLOCK_KEYS))
        return
    if not isinstance(block['members'], list) or \
            any(not isinstance(x, dict) or set(x) != STAGE0_MEMBER_KEYS for x in block['members']):
        reasons.append('STAGE0_STATUS_BLOCK_MALFORMED: member rows must have keys %s' % sorted(STAGE0_MEMBER_KEYS))
        return
    refusals = block['evaluation_refusals']
    if not isinstance(refusals, list) or not all(isinstance(r, str) and r for r in refusals):
        reasons.append('STAGE0_STATUS_BLOCK_MALFORMED: evaluation_refusals must be a list of non-empty strings')
        return
    v = _stage0_receipt_verdict(block['status_record'], _stage0_members_of(doc['members']))
    if refusals and not _stage0_eligible(v):
        reasons.append('STAGE0_STATUS_BLOCK_MISMATCH: evaluation refusals are recorded but the receipt rule does not '
                       'hold')
        return
    if _canonical_bytes(_stage0_block(v, refusals)) != _canonical_bytes(block):
        reasons.append('STAGE0_STATUS_BLOCK_MISMATCH: the frozen stage0_status block differs from the receipt rule '
                       'recomputed from the pinned root bytes')
        return
    evaluated = block['reading'] == ALT_EVALUATED
    status = [a.get('status') for a in doc['alternatives']['declared']
              if isinstance(a, dict) and a.get('name') == STAGE0_ALTERNATIVE]
    if status != [ALT_EVALUATED if evaluated else ALT_NOT_EVALUATED]:
        reasons.append('STAGE0_STATUS_READING_MISMATCH: %s status %s with reading %s'
                       % (STAGE0_ALTERNATIVE, status, block['reading']))
        return
    if evaluated and doc['alternative_results'][STAGE0_ALTERNATIVE]['member_evaluation']['status'] != STATUS_COMPLETE:
        reasons.append('STAGE0_EVALUATION_NOT_COMPLETE: an evaluated STAGE0 must have every member evaluated')
        return
    pinned = set((p['path'], p['sha256']) for p in doc['pins']['input_files'])
    missing = [p['path'] for p in _stage0_custody_pins(block) if (p['path'], p['sha256']) not in pinned]
    if missing:
        reasons.append('STAGE0_CUSTODY_FILE_NOT_PINNED: %s' % missing[:5])
'''

WRITER_DOC = '''    STAGE0 successor (root V006 A142; r3a ROOT_ITEMS M-14; prereg r3a section 6.3): stage0_status_record is the
    root-written STAGE0 status record pin {'path', 'sha256'} (schema STAGE0_STATUS_RECORD_C2V001) or None. The caller
    passes the slots alternatives unchanged (a STAGE0 status set by the caller is put back to the slots value; it is
    never the caller's to set) and may include a STAGE0_GRID_OUTER replay evaluation in alternative_evaluations. That
    evaluation is frozen, with STAGE0 EVALUATED_BEFORE_FREEZE, only when the receipt rule holds
    (_stage0_receipt_verdict) and it passes every check a frozen alternative must pass
    (_stage0_evaluation_refusals). Otherwise STAGE0 is frozen NOT_EVALUATED_BEFORE_FREEZE (reading
    NOT_EVALUATED_BEFORE_FREEZE or EVALUATED_REFUSED, with its codes, in the manifest's stage0_status block) and the
    freeze goes on: STAGE0 never makes the freeze refuse. The status record and every custody-verified receipt are
    added to input_files.
'''

HEADER = '''"""prediction_freeze_c2v003g_stage0_c2v001 -- STAGE0-only successor of prediction_freeze_c2v003g_cx3v001.

Predecessor: v003g, sha256 48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405 (slots V003 pin
unchanged). Built for root V006 A142 (r3a ROOT_ITEMS M-14, adopted; prereg r3a section 6.3). Its only behavioural
change: in a Phase-2 freeze STAGE0_GRID_OUTER may read EVALUATED_BEFORE_FREEZE, exactly by the M-14 receipt rule
(every registered STAGE0 member's terminal receipt FINISHED, and this module named as the sealed successor in the
root STAGE0 status record). The successor only PERMITS EVALUATED; it never requires it, and STAGE0 never makes a
freeze refuse (v003g D9 refused a freeze that carried a STAGE0 evaluation). A Phase-1 status record reads
NOT_IN_PHASE_1. The new code is the 'STAGE0 successor' section and the lines marked 'STAGE0 successor'; every other
function and constant is AST-identical to v003g. The v003g module docstring follows unchanged.

'''


def replacements():
    return [
        ('R01 module docstring: successor header',
         '"""prediction_freeze_c2v003g_cx3v001 — root-roster-bound freeze/score successor.\n',
         HEADER + 'prediction_freeze_c2v003g_cx3v001 — root-roster-bound freeze/score successor.\n'),
        ('R02 constants: SCHEMA, MODULE_NAME',
         "SCHEMA = 'FREEZE_MANIFEST_C2V003G'\nREGISTRATION_SCHEMA = 'FREEZE_REGISTRATION_C2V003G'\n"
         "MODULE_NAME = 'prediction_freeze_c2v003g_cx3v001'\n",
         "SCHEMA = 'FREEZE_MANIFEST_C2V003G_STAGE0_C2V001'   # STAGE0 successor (M-14): the manifest adds stage0_status\n"
         "REGISTRATION_SCHEMA = 'FREEZE_REGISTRATION_C2V003G'\n"
         "MODULE_NAME = 'prediction_freeze_c2v003g_stage0_c2v001'   # STAGE0 successor of prediction_freeze_c2v003g_cx3v001\n"),
        ('R03 constant: MANIFEST_KEYS gains stage0_status',
         "    'notes', 'target_velocities_included', 'manifest_sha256', 'input_bindings', 'module', "
         "'row_registration_rosters',\n})\n",
         "    'notes', 'target_velocities_included', 'manifest_sha256', 'input_bindings', 'module', "
         "'row_registration_rosters',\n"
         "    'stage0_status',   # STAGE0 successor (M-14): the frozen receipt-rule record of STAGE0_GRID_OUTER\n})\n"),
        ('R04 _load_row_roster: a STAGE0 replay evaluation is permitted',
         "    if require_evaluated and alt['status'] != ALT_EVALUATED:\n"
         "        raise ValueError('ROOT_ROSTER_ALTERNATIVE_NOT_EVALUATED: ' + alt['name'])\n",
         "    # STAGE0 successor (M-14): a STAGE0 replay evaluation is permitted here; whether it is frozen is decided only\n"
         "    # by the receipt rule in write_freeze_manifest (_stage0_freeze_decision), never by this roster read.\n"
         "    if require_evaluated and alt['status'] != ALT_EVALUATED and alt['name'] != STAGE0_ALTERNATIVE:\n"
         "        raise ValueError('ROOT_ROSTER_ALTERNATIVE_NOT_EVALUATED: ' + alt['name'])\n"),
        ('R05 _root_rosters_for_alternatives: slots comparison tolerates only STAGE0 status',
         "    if alternatives != _root_slots()[0]['alternatives']:\n"
         "        raise ValueError('ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED",
         "    if _stage0_status_neutral(alternatives) != _root_slots()[0]['alternatives']:   # STAGE0 successor (M-14)\n"
         "        raise ValueError('ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED"),
        ('R06 _root_rosters_for_alternatives: roster record comparison tolerates only STAGE0 status',
         "        if rosters[alternative['name']]['alternative'] != alternative:\n",
         "        if rosters[alternative['name']]['alternative'] != _stage0_neutral_record(alternative):\n"),
        ('R07 _bind_alternatives: slots comparison tolerates only STAGE0 status',
         "    if alternatives != registered:\n"
         "        reasons.append('ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED",
         "    # STAGE0 successor (M-14): the one tolerated difference is STAGE0's status; _stage0_manifest_check binds it\n"
         "    # to the receipt rule recomputed from the pinned root bytes.\n"
         "    if _stage0_status_neutral(alternatives) != registered:\n"
         "        reasons.append('ROOT_ROSTERS_EXACT_ORDERED_SLOTS_ALTERNATIVES_REQUIRED"),
        ('R08 _validate_manifest_structure: STAGE0 receipt-rule check',
         "        _validate_manifest_impl(doc, reasons)\n        if not reasons:\n            _root_manifest_check(doc)\n",
         "        _validate_manifest_impl(doc, reasons)\n        if not reasons:\n            _root_manifest_check(doc)\n"
         "        if not reasons:\n            _stage0_manifest_check(doc, reasons)   # STAGE0 successor (M-14)\n"),
        ('R09 write_freeze_manifest: signature gains stage0_status_record',
         "                          code_files, input_files, notes, allow_incomplete, row_registration_rosters=None):\n",
         "                          code_files, input_files, notes, allow_incomplete, row_registration_rosters=None,\n"
         "                          stage0_status_record=None):\n"),
        ('R10 write_freeze_manifest: docstring STAGE0 paragraph',
         "    After the manifest, writes registration_path (D8) recording the manifest FILE sha256; that\n",
         WRITER_DOC +
         "    After the manifest, writes registration_path (D8) recording the manifest FILE sha256; that\n"),
        ('R11 write_freeze_manifest: STAGE0 status is never the caller\'s',
         "    alts = _bind_alternatives(alternatives, reasons)\n    if alts is None:\n        return out\n    try:\n"
         "        root_rosters = _root_rosters_for_alternatives(row_registration_rosters, alternatives, ids)\n",
         "    alternatives = _stage0_status_neutral(alternatives)   # STAGE0 successor: the receipt rule sets STAGE0's status\n"
         "    alts = _bind_alternatives(alternatives, reasons)\n    if alts is None:\n        return out\n    try:\n"
         "        root_rosters = _root_rosters_for_alternatives(row_registration_rosters, alternatives, ids)\n"),
        ('R12 write_freeze_manifest: STAGE0 evaluation set aside before D9',
         "    if not isinstance(alternative_evaluations, dict) or set(alternative_evaluations) != set(alts['evaluated']):\n",
         "    # STAGE0 successor (M-14): a STAGE0 evaluation is set aside here and admitted below only by the receipt rule,\n"
         "    # so D9 binds every other alternative exactly as in v003g and STAGE0 never refuses the freeze.\n"
         "    alternative_evaluations, stage0_evaluation = _stage0_split_evaluations(alternative_evaluations)\n"
         "    if not isinstance(alternative_evaluations, dict) or set(alternative_evaluations) != set(alts['evaluated']):\n"),
        ('R13 write_freeze_manifest: the receipt rule decides STAGE0',
         "    elif sensitivity.get('row_registration_roster') != root_pins[alts['primary']]:\n"
         "        reasons.append('ROOT_ROSTER_SENSITIVITY_PIN_MISMATCH')\n    if reasons:\n        return out\n",
         "    elif sensitivity.get('row_registration_roster') != root_pins[alts['primary']]:\n"
         "        reasons.append('ROOT_ROSTER_SENSITIVITY_PIN_MISMATCH')\n    if reasons:\n        return out\n"
         "    # STAGE0 successor (M-14): the receipt rule decides STAGE0's status from root-written bytes. The successor only\n"
         "    # PERMITS EVALUATED_BEFORE_FREEZE; every other outcome freezes STAGE0 NOT_EVALUATED without a refusal.\n"
         "    stage0, stage0_admitted = _stage0_freeze_decision(\n"
         "        stage0_status_record, stage0_evaluation, alternative_evaluations[alts['primary']], selection, spec, ids,\n"
         "        root_rosters.get(STAGE0_ALTERNATIVE), root_pins.get(STAGE0_ALTERNATIVE))\n"
         "    if stage0_admitted:\n"
         "        alternatives = _stage0_effective_alternatives(alternatives)\n"
         "        alts = _bind_alternatives(alternatives, reasons)\n"
         "        if alts is None:\n"
         "            return out\n"
         "        alternative_evaluations = dict(alternative_evaluations)\n"
         "        alternative_evaluations[STAGE0_ALTERNATIVE] = stage0_evaluation\n"
         "    input_files = _stage0_input_files(input_files, stage0)\n"),
        ('R14 write_freeze_manifest: manifest body carries stage0_status',
         "            'row_registration_rosters': root_pins,\n",
         "            'row_registration_rosters': root_pins,\n"
         "            'stage0_status': stage0,   # STAGE0 successor (M-14)\n"),
        ('R15 STAGE0 successor section (constants and _stage0_* functions)',
         "def _member_order(members):\n    return [{'log_index': m['log_index'], 'role': m['role']} for m in members]\n",
         "def _member_order(members):\n    return [{'log_index': m['log_index'], 'role': m['role']} for m in members]\n"
         + STAGE0_BLOCK),
        ('R16 _alternative_score_scope: STAGE0 record comparison tolerates only its status',
         "    if alternative != registered or alternative['headline'] is not False:\n",
         "    if _stage0_neutral_record(alternative) != registered or alternative['headline'] is not False:   # STAGE0 successor\n"),
        ('R17 score_after_freeze: output gains stage0_status (refusal paths: None)',
         "           'pointwise_envelope': None, 'sensitivity': None, 'alternatives': [], 'reasons': reasons}\n",
         "           'pointwise_envelope': None, 'sensitivity': None, 'alternatives': [], 'stage0_status': None,\n"
         "           'reasons': reasons}\n"),
        ('R18 score_after_freeze: output stage0_status is the frozen block',
         "    out['alternatives'] = alts\n    out['refused'] = False\n",
         "    out['alternatives'] = alts\n"
         "    out['stage0_status'] = doc['stage0_status']   # STAGE0 successor (M-14): the frozen receipt-rule record\n"
         "    out['refused'] = False\n"),
    ]


def main(argv):
    if len(argv) != 2:
        raise SystemExit('usage: build_stage0_successor_c2v001.py OUT_PATH')
    with open(V003G_PATH, 'rb') as fh:
        raw = fh.read()
    if hashlib.sha256(raw).hexdigest() != V003G_SHA256:
        raise SystemExit('v003g bytes do not hash to %s' % V003G_SHA256)
    text = raw.decode('utf-8')
    for name, old, new in replacements():
        n = text.count(old)
        if n != 1:
            raise SystemExit('%s: expected exactly one match, found %d' % (name, n))
        text = text.replace(old, new)
    out = text.encode('utf-8')
    with open(argv[1], 'xb') as fh:
        fh.write(out)
    print('wrote %s sha256 %s bytes %d (%d replacements)' % (argv[1], hashlib.sha256(out).hexdigest(), len(out),
                                                             len(replacements())))


if __name__ == '__main__':
    main(sys.argv)
