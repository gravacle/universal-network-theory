# Claude4 (dispatch 0584) seal tool 4: build the exact SEAL_RECORD bytes for root to create exclusively. It writes nothing.
# It first runs the slot-fill check (tool 3) with the frozen-addendum check (tool 1) and the sealed-compare check (tool 2); any refusal
# means no record is produced. Then it prints the record to stdout (canonical JSON: sorted keys, indent 1, trailing newline) and its
# sha256 and verdict to stderr. The pins guard v008 reads (sealed_by, prereg, compare, driver, frozen_addendum) are exact {path, sha256}
# dicts; prereg and compare are the SEALED prereg and the SEALED compare (A82); driver and frozen_addendum equal the bound plan's pins
# byte for byte (launcher v007 compares them exactly). The E-SEAL1 outputs are pinned and embedded only if they contain no decimal
# number that could be a row value (blinding, A47 I3). Root creates the file with exclusive create, e.g.
#   python3 -I -B build_seal_record_c4v001.py ... | python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" SEAL_RECORD.json
# usage: python3 -I -B build_seal_record_c4v001.py --slots S.json --prereg SEALED.json --text-of-record R4.json --frozen F.md
#        --covered-later A82 --reviewed R.py --sealed-compare S.py --gates-only-output G.txt --validity-only-output V.txt
#        --key-equivalence-map K.json --new-item-list N.json --successor-custody Z.json
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v001 as C
import check_slot_fill_c4v001 as T3

SCHEMA = 'UNT_V007_SEAL_RECORD_C4V001'
ROW_VALUE_RX = re.compile(r'(?<![\w.])\d+\.\d{3,}(?![\w.])|(?<![\w.])\d(?:\.\d+)?[eE][-+]?\d+(?![\w.])')


def build(a):
    res = T3.run(a.slots, a.prereg, a.text_of_record, a.frozen, a.covered_later, a.reviewed, a.sealed_compare)
    chk = C.Checker('build_seal_record_c4v001')
    for f in res['failures']:
        chk.fail('T3:' + f['code'], f['detail'])
    if chk.failures:
        return chk.result(), None
    slots = C.strict_json(a.slots)
    sp = C.strict_json(a.prereg)
    plan = C.strict_json(slots['launch_packet']['bound_plan']['path'])
    outputs = {}
    for label, path in (('gates_only', a.gates_only_output), ('validity_only_C5H', a.validity_only_output)):
        p = Path(path)
        if not p.is_file():
            chk.fail('E_SEAL1_OUTPUT_MISSING', label)
            continue
        text = p.read_bytes().decode('utf-8')
        if ROW_VALUE_RX.search(text):
            chk.fail('E_SEAL1_OUTPUT_MAY_SHOW_A_ROW_VALUE', '%s contains a decimal number; blinded output prints codes only (A47 I3)' % label)
            continue
        outputs[label] = {'path': str(p.resolve()), 'sha256': C.sha(p), 'text': text}
    extras = {}
    for label, path in (('key_equivalence_map', a.key_equivalence_map), ('new_item_dispositions', a.new_item_list), ('raw_successor_custody', a.successor_custody)):
        ref = {'path': str(Path(path).resolve()), 'sha256': C.sha(path)} if Path(path).is_file() else None
        if ref is None:
            chk.fail('SEAL_RECORD_INPUT_MISSING', label)
            continue
        try:
            C.strict_json(path)
        except Exception as e:
            chk.fail('SEAL_RECORD_INPUT_JSON', '%s: %s' % (label, e))
            continue
        extras[label] = ref
    if chk.failures:
        return chk.result(), None
    disclosure = next((r['text'] for r in sp['seal_record_requirements'] if r['text'].startswith('Disclosure E5-08')), None)
    if not disclosure:
        chk.fail('E5_08_TEXT_NOT_FOUND', 'the prereg carries the E5-08 disclosure text')
        return chk.result(), None
    sealed_compare = {'path': str(Path(a.sealed_compare).resolve()), 'sha256': C.sha(a.sealed_compare)}
    rec = {
        'schema': SCHEMA,
        'sealed_by': dict(C.AUTHORITY),
        'prereg': {'path': str(Path(a.prereg).resolve()), 'sha256': C.sha(a.prereg)},
        'compare': sealed_compare,
        'driver': dict(plan['driver']),
        'frozen_addendum': dict(plan['frozen_addendum']),
        'driver_branch': slots['driver_branch'],
        'bound_plan': dict(slots['launch_packet']['bound_plan']),
        'bound_command': dict(slots['launch_packet']['bound_command']),
        'build': dict(slots['launch_packet']['build']),
        'compare_reviewed_source': dict(slots['compare_reviewed_source']),
        'identity_comparator': dict(slots['identity_comparator']),
        'identity_gate_records': {k: dict(v) for k, v in slots['identity_gate_records'].items()},
        'certificates': {k: dict(v) for k, v in slots['certificates'].items()},
        'producer_registry': dict(slots['producer_registry']),
        'driver_build_record': dict(slots['driver_build_record']),
        'driver_check_record': dict(slots['driver_check_record']),
        'ngc_gas_M_s': slots['ngc_gas_M_s'],
        'e_seal1': {k: {'path': v['path'], 'sha256': v['sha256']} for k, v in outputs.items()},
        'e_seal1_text': {k: v['text'] for k, v in outputs.items()},
        'no_row_value_shown': True,
        'disclosures': [disclosure],
        'no_change_notes': ['%s: covers this entry for the prereg text of record (A81 RI-26)' % e for e in a.covered_later],
        **extras,
    }
    if slots['driver_branch'] == 'r6':
        rec['cache_directory'] = dict(slots['cache_directory_r6_only'])
    if rec['driver'] != slots['driver'] or rec['frozen_addendum'] != slots['frozen_addendum']:
        chk.fail('PLAN_PINS_NOT_SLOTS', 'internal: the bound plan and the slots disagree')
        return chk.result(), None
    text = json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    out = chk.result()
    out['seal_record_sha256'] = __import__('hashlib').sha256(text.encode('utf-8')).hexdigest()
    return out, text


def main(argv=None):
    p = C.parser('build the exact SEAL_RECORD bytes (prints them; writes nothing)')
    for flag in ('--slots', '--prereg', '--text-of-record', '--frozen', '--reviewed', '--sealed-compare', '--gates-only-output', '--validity-only-output',
                 '--key-equivalence-map', '--new-item-list', '--successor-custody'):
        p.add_argument(flag, required=True)
    p.add_argument('--covered-later', default='')
    a = C.parse_args(p, argv)
    a.covered_later = [x.strip() for x in a.covered_later.split(',') if x.strip()]
    res, text = build(a)
    print(json.dumps(res, indent=1, sort_keys=True), file=sys.stderr)
    if text is None:
        return 2
    sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
