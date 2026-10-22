"""selfcheck_freeze_c2v004.py -- the F-row status self-check for FREEZE_EXPECTED_INPUTS (s0_launch_kit_c2, C2V004).

Successor of selfcheck_freeze_c2v003.py (1875c697) with exactly one change, VERBATIM:
  The string leaves under write_freeze_manifest_inputs[kwarg=notes].value are not read as claims.  That value is a
  verbatim copy of pinned documents (slots V003 notes_block_for_manifest and the V004 A18 section, Claude4 0223 B1), so
  its words belong to those documents, not to this list: the C2V003 rule reads the slots sentence "The status of these
  slots under A16.1 is NOT_EVALUATED_BEFORE_FREEZE" as a status claim about this list's slots pin and refuses.  The
  contract checker (selfcheck_contract_c2v004.py, row K3) checks that subtree byte for byte against its sources instead.
  The number of leaves skipped is reported.
Everything else is the C2V003 rule, unchanged:
Rule: no string anywhere in the file may give a named item a status different from that item's structured entry.
  Named items (read from the file's own structure):
    code_files[i], input_files[i], referenced_not_input_files[i]   status = sha_status (first word)
    freeze_module, coordinator_evidence, query_manifest, slots, route_b_projection_config   status = sha_status
    write_freeze_manifest_inputs[k] for the distinctive kwarg names (KWARG_ITEMS)           status = status (first word)
    exact_alternative_declarations.declared[i]                                               status = status
    interior_count                                                                           status = status
  Aliases of an item: its name, the basename and stem of its path, the ALIASES table below, and every bare version
  word (v001, v003a, ...) found in its path stem (a bare version word is usually shared by several items).
  Status words: every structured status value in the file, the label names, the fixed STATUS_WORDS, plus the verbal
  forms ABSENT_VERBAL (claim the file is not there) and PRESENT_VERBAL (claim it is there).
Binding: each string is cut into clauses at '; ', '. ' and newlines; inside a clause each status word binds to the
  nearest alias that ends before it (longest alias wins at a position).  An unbound status word is not a claim about
  a named item and is skipped.
Refusal: a bound exact status word that differs from the status of any item the alias names (an alias naming items
  of different statuses is ambiguous and refuses); an ABSENT_VERBAL word bound to an item whose status is not PENDING;
  a PRESENT_VERBAL word bound to an item whose status is PENDING.
  A PRESENT_VERBAL word directly after a modal ('must exist', 'whether it exists', 'not exist') is not a claim.
Limit (disclosed): a status word after a list ('A, B, C STATUS') binds to C only.
Usage: PY -I -B selfcheck_freeze_c2v004.py FILE.json   -> prints JSON; exit 0 PASS, 3 REFUSED, 2 usage
"""
import json
import os
import re
import sys

SCHEMA = 'UNT_FREEZE_STATUS_SELFCHECK_C2V004'
STATUS_WORDS = ('TESTED_FROM_BYTES', 'EXISTS_NOT_ADOPTED', 'EXISTS_SHA_IN_V006', 'RECORDED_PIN_NOT_REHASHED', 'PENDING',
                'PENDING_ROOT_ADOPTION', 'MISMATCH_FROM_BYTES', 'MISSING', 'NO_REGISTERED_VALUE', 'PENDING_ROOT_FIXES',
                'EVALUATED_BEFORE_FREEZE', 'NOT_EVALUATED_BEFORE_FREEZE', 'ADOPTED_IN_V006')
ABSENT_VERBAL = ('not built', 'absent', 'does not exist', 'not produced')
PRESENT_VERBAL = ('exists', 'exist')
KWARG_ITEMS = ('out_path', 'registration_path', 'parameter_region', 'observation_rule', 'alternative_evaluations',
               'row_registration_rosters', 'allow_incomplete', 'code_files', 'input_files')
TOP_PINS = ('freeze_module', 'coordinator_evidence', 'query_manifest', 'slots', 'route_b_projection_config')
ALIASES = {   # item name (as in the file) -> extra spellings used in prose
    'TSR flag record (M-7)': ['TSR flag record', 'ROOT_TSR_FLAG_RECORD'],
    'TSR support record (UNT_ROOT_TSR_SUPPORT_CX3V001)': ['TSR support record', 'UNT_ROOT_TSR_SUPPORT_CX3V001',
                                                          'support_record', 'support record'],
    'roster builder (roster_builder_c2v001.py)': ['roster builder'],
    'RUNBOOK_V002': ['RUNBOOK_V002.md'],
    'replay adapter': ['replay adapter'],
    'phase1_c2v003a (phase1_c2v003a.py)': ['phase1_c2v003a'],
    's0 launch kit': ['s0 launch kit', 's0_launch_kit_c2 version'],
    'calibration record (CALIBRATION_RUN_RECORD_C2V003), exactly one': ['calibration record',
                                                                         'CALIBRATION_RUN_RECORD_C2V003'],
    'V007 adoption pin': ['V007 adoption pin', 'V007 pin'],
    'sched v003 machine gate': ['sched v003 gate', 'machine gate'],
    'v003g freeze module': ['v003g module', 'v003g'],
}
MODAL = ('must', 'may', 'should', 'to', 'whether it', 'if it', 'not')   # 'X must exist' / 'whether it exists' claim nothing
VERBATIM_KWARGS = ('notes',)   # C2V004: write_freeze_manifest_inputs[kwarg].value is a verbatim copy; not read as claims


def first_word(s):
    return re.split(r'[\s:(]', s.strip(), maxsplit=1)[0] if isinstance(s, str) else None


def version_words(stem):
    return sorted(set(re.findall(r'v\d{3}[a-z]?(?![a-z0-9])', stem.lower())))


def items_of(doc):
    items = []

    def add(iid, name, path, status):
        al = set()
        if name:
            al.add(name)
            al.update(ALIASES.get(name, []))
        if isinstance(path, str) and path.startswith('/'):
            base = os.path.basename(path)
            al.update({base, os.path.splitext(base)[0]})
            for v in version_words(os.path.splitext(base)[0]):
                al.add(v)
        items.append({'id': iid, 'name': name, 'status': status, 'aliases': sorted(a for a in al if a)})

    for sec in ('code_files', 'input_files', 'referenced_not_input_files'):
        for i, e in enumerate(doc.get(sec) or []):
            add('%s[%d]' % (sec, i), e.get('name'), e.get('path'), first_word(e.get('sha_status')))
    for k in TOP_PINS:
        e = doc.get(k)
        if isinstance(e, dict) and 'sha_status' in e:
            add(k, k, e.get('path'), first_word(e['sha_status']))
    for e in doc.get('write_freeze_manifest_inputs') or []:
        if e.get('kwarg') in KWARG_ITEMS:
            add('write_freeze_manifest_inputs.' + e['kwarg'], e['kwarg'], None, first_word(e.get('status')))
    for i, e in enumerate(((doc.get('exact_alternative_declarations') or {}).get('declared')) or []):
        add('exact_alternative_declarations.declared[%d]' % i, e.get('name'), None, first_word(e.get('status')))
    ic = doc.get('interior_count')
    if isinstance(ic, dict):
        add('interior_count', 'interior_count', None, first_word(ic.get('status')))
    return items


def verbatim_prefixes(doc):
    return ['write_freeze_manifest_inputs[%d].value' % i
            for i, e in enumerate(doc.get('write_freeze_manifest_inputs') or [])
            if isinstance(e, dict) and e.get('kwarg') in VERBATIM_KWARGS]


def leaves(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, p + '.' + k if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, '%s[%d]' % (p, i))
    elif isinstance(o, str):
        yield p, o


def word_re(words):
    alts = sorted(set(words), key=len, reverse=True)
    return re.compile(r'(?<![A-Za-z0-9_])(' + '|'.join(re.escape(w) for w in alts) + r')(?![A-Za-z0-9_])')


def check(doc):
    items = items_of(doc)
    by_alias = {}
    for it in items:
        for a in it['aliases']:
            by_alias.setdefault(a, []).append(it)
    statuses = set(STATUS_WORDS) | {it['status'] for it in items if it['status']} | set((doc.get('labels') or {}).keys())
    statuses = {s for s in statuses if s and re.fullmatch(r'[A-Z][A-Z0-9_]*[A-Z0-9]', s)}
    alias_re = word_re(by_alias)
    status_re = word_re(statuses)
    verbal_re = word_re(ABSENT_VERBAL + PRESENT_VERBAL)
    skip = verbatim_prefixes(doc)
    violations, bound_n, skipped_n = [], 0, 0
    for path, s in leaves(doc):
        if any(path == x or path.startswith(x + '.') or path.startswith(x + '[') for x in skip):
            skipped_n += 1
            continue
        for clause in re.split(r';\s|\.\s|\n', s):
            al = [(m.start(), m.end(), m.group(1)) for m in alias_re.finditer(clause)]
            toks = [(m.start(), m.group(1), 'exact') for m in status_re.finditer(clause)] + \
                   [(m.start(), m.group(1), 'verbal') for m in verbal_re.finditer(clause)
                    if not (m.group(1) in PRESENT_VERBAL and
                            re.search(r'(?:^|\s)(?:%s)\s+$' % '|'.join(MODAL), clause[:m.start()]))]
            for start, tok, kind in toks:
                prior = [a for a in al if a[1] <= start]
                if not prior:
                    continue
                a = max(prior, key=lambda x: (x[1], x[1] - x[0]))
                its = by_alias[a[2]]
                bound_n += 1
                for it in its:
                    st = it['status']
                    if kind == 'exact':
                        bad = st != tok
                    elif tok in ABSENT_VERBAL:
                        bad = st != 'PENDING'
                    else:
                        bad = st == 'PENDING'
                    if bad:
                        violations.append({'string_key': path, 'alias': a[2], 'item': it['id'], 'item_status': st,
                                           'claimed': tok, 'claim_kind': kind,
                                           'ambiguous_alias': len({x['status'] for x in its}) > 1})
    return {'schema': SCHEMA, 'ok': not violations, 'n_items': len(items), 'n_bound_status_words': bound_n,
            'verbatim_subtrees_not_read': skip, 'n_verbatim_leaves_not_read': skipped_n, 'violations': violations}


def main(argv):
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    with open(argv[1], 'rb') as f:
        doc = json.loads(f.read())
    r = check(doc)
    print(json.dumps(r, indent=1))
    return 0 if r['ok'] else 3


if __name__ == '__main__':
    sys.exit(main(sys.argv))
