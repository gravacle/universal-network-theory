# Claude4 seal tools v002, tool 4 (successor of build_seal_record_c4v001.py 3091fc2a): build the exact SEAL_RECORD bytes for root to
# create exclusively, and check root's admission config against them. It writes nothing.
# BUILD MODE. It first runs tool 3 v002 with tool 1 (frozen addendum) and tool 2 (sealed compare); any refusal means no record. Then
# it prints the record to stdout (canonical JSON: sorted keys, indent 1, trailing newline) and its sha256 and verdict to stderr. The
# pins guard v008 reads (sealed_by, prereg, compare, driver, frozen_addendum) are exact {path, sha256} dicts; prereg and compare are
# the SEALED prereg and the SEALED compare (A82); driver and frozen_addendum equal the bound plan's pins byte for byte.
# New in v002:
#  R-04  the B6 outputs are the sealed compare's own blinded bodies: GATES_ONLY.json (--gates-only) and VALIDITY_ONLY.json
#        (--validity-only --case C5H), strict JSON, schema <SCHEMA_REPORT of the sealed compare>_GATES_ONLY / _VALIDITY_ONLY,
#        blinded true, test_mode false, script_sha256 = the sealed compare's sha, route_a_mode = the case block's, the validity body
#        on exactly C5H, and nothing value-bearing (no JSON number anywhere, no number token in any string or key: the compare's own
#        r12 _RE_NUMBER rule with its allowed constants, plus v001's row-value rule). The three B7 inputs parse with their schemas
#        (README): UNT_V007_SEAL_KEY_EQUIVALENCE_MAP_C4V002, UNT_V007_SEAL_NEW_ITEM_DISPOSITIONS_C4V002 (its compare_impl must name
#        the reviewed source sha) and UNT_V007_SEAL_RAW_SUCCESSOR_CUSTODY_C4V002 (on the driver slot).
#  R-10  the SEAL_RECORD key map equals the validated case block's key_equivalence_map.
#  D-04  the case block, the CASCADE_MAP_R5_ADDENDUM (r5), the admission launcher and guard, the BUILD_V007 pin and its 15-source
#        allowlist pass through from tool 3 into the record; A99.3: the prereg's entry table is quoted, and a --covered-later entry
#        whose table row's section changed after the text was written is noted with both section shas; D-09: the record states
#        that it is the authority on sealed status and lists the PENDING strings the text of record keeps outside slot values;
#        every seal_record_requirements text starting "Disclosure" is copied (E5-08 required).
#  A100  when the prereg asks the seal record to repeat the B2 disclosure block (prereg r5 seal_record_requirements; A100, A101),
#        --b2-record names the B2 record of record: a PASS B2 gate record registered as gate_records.B2 in the slot's producer
#        registry; its disclosure object and that requirement's text (which carries A101's erratum) are quoted.
# ADMISSION MODE (B8): --check-admission-config CFG --seal-record SEAL refuses unless root's ROOT_SEAL_ADMISSION config pins this
# SEAL_RECORD, its prereg, compare and BUILD_V007, and its producer_allowlist is exactly the record's 15-source BUILD_V007 allowlist
# (V6-S3), naming the record's launcher and guard exactly (SRR[10], A78 N2), every source verified from bytes and listed literally in
# the BUILD.
# Root creates the record with exclusive create, e.g.
#   python3 -I -B build_seal_record_c4v002.py ... | python3 -I -B -c "import sys; open(sys.argv[1], 'x').write(sys.stdin.read())" SEAL_RECORD.json
# usage: python3 -I -B build_seal_record_c4v002.py --slots S.json --prereg SEALED.json --text-of-record R5.json --frozen F.md
#        --covered-later A100 --reviewed R.py --sealed-compare S.py --gates-only-output GATES_ONLY.json
#        --validity-only-output VALIDITY_ONLY.json --key-equivalence-map K.json --new-item-list N.json --successor-custody Z.json
#        [--b2-record B2_GATE_RECORD.json]   (required when the prereg asks the seal record to repeat the B2 disclosure block, A100)
#        python3 -I -B build_seal_record_c4v002.py --check-admission-config ROOT_SEAL_ADMISSION_V001.json --seal-record SEAL_RECORD.json
import ast, hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import seal_common_c4v002 as C
import check_slot_fill_c4v002 as T3
import check_sealed_compare_c4v002 as T2

SCHEMA = 'UNT_V007_SEAL_RECORD_C4V002'
KEY_MAP_SCHEMA = 'UNT_V007_SEAL_KEY_EQUIVALENCE_MAP_C4V002'
NEW_ITEMS_SCHEMA = 'UNT_V007_SEAL_NEW_ITEM_DISPOSITIONS_C4V002'
CUSTODY_SCHEMA = 'UNT_V007_SEAL_RAW_SUCCESSOR_CUSTODY_C4V002'
ROW_VALUE_RX = re.compile(r'(?<![\w.])\d+\.\d{3,}(?![\w.])|(?<![\w.])\d(?:\.\d+)?[eE][-+]?\d+(?![\w.])')            # v001 rule, kept
# the sealed compare's own blinding rule (r12 L4818-4824, copied verbatim): 64-hex shas masked first, then any decimal, exponent,
# leading-dot, trailing-dot number or 5+ digit run is a number unless it is one of the compare's allowed constants
HEX64_ANY = re.compile(r'[0-9a-f]{64}')
NUMBER_RX = re.compile(r'[-+]?(?:\d+\.\d+(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+|\d+\.(?!\d)|\d{5,})')
ALLOWED_NUMBER_TOKENS = ('1e-4', '1e-12', '0.05', '0.005', '0.1', '1.0', '2.0', '64.0', '32.0')
B6 = (('gates_only', 'GATES_ONLY.json', '_GATES_ONLY'), ('validity_only_C5H', 'VALIDITY_ONLY.json', '_VALIDITY_ONLY'))
KEY_MAP_ENTRY_KEYS = {'pointer', 'absent_equivalent_value', 'b0_identity_evidence'}
KEY_MAP_UNMAPPABLE = ('composite_grid_spec', 'uv_tail', 'brackets', 'picard', 'truncation')     # r12 validate_case_block
NEW_DISPOSITIONS = ('ADOPTED', 'REJECTED')                                                      # A58 RI-10 / A81 RI-20
B2_SRR_MARK = 'B2 disclosure block'                                     # prereg r5 seal_record_requirements (A100, A101)
STATUS_AUTHORITY = ('This SEAL_RECORD is the authority on sealed status (rehearsal D-09): outside seal_slots.<k>.value the sealed prereg is the '
                    'text of record byte for byte, so it keeps that text\'s draft status line and the PENDING strings listed here.')


def number_tokens(obj, where='$', out=None):
    """every JSON number, and every number token in a string or key, of a blinded body (r12 assert_no_numbers / _blind_str rule)"""
    out = [] if out is None else out
    if isinstance(obj, bool) or obj is None:
        return out
    if isinstance(obj, (int, float)):
        out.append('number at %s' % where)
    elif isinstance(obj, str):
        masked = HEX64_ANY.sub(lambda m: 'h' * 64, obj)
        if any(m.group(0) not in ALLOWED_NUMBER_TOKENS for m in NUMBER_RX.finditer(masked)):
            out.append('number token in the string at %s' % where)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            number_tokens(k, where + '.<key>', out)
            number_tokens(v, '%s.%s' % (where, k), out)
    elif isinstance(obj, list):
        for j, v in enumerate(obj):
            number_tokens(v, '%s[%d]' % (where, j), out)
    else:
        out.append('unexpected type at %s' % where)
    return out


def sealed_schema_report(sealed_path):
    env = T2.module_strings(ast.parse(Path(sealed_path).read_bytes().decode('utf-8')))
    return env.get('SCHEMA_REPORT')


def b6_codes(chk, label, path, name, suffix, schema_report, sealed_sha, mode):
    p = Path(path)
    if not p.is_file():
        chk.fail('E_SEAL1_OUTPUT_MISSING', label)
        return None
    if p.name != name:
        chk.fail('E_SEAL1_OUTPUT_NAME', '%s must be the compare\'s own %s, got %s' % (label, name, p.name))
    raw = p.read_bytes()
    text = raw.decode('utf-8')
    try:
        body = C.strict_json_bytes(raw)
    except Exception as e:
        chk.fail('E_SEAL1_OUTPUT_JSON', '%s: %s' % (label, type(e).__name__))
        return None
    if not isinstance(body, dict):
        chk.fail('E_SEAL1_OUTPUT_JSON', '%s is not a JSON object' % label)
        return None
    if body.get('schema') != schema_report + suffix:
        chk.fail('E_SEAL1_SCHEMA', '%s: schema %r, the sealed compare writes %s' % (label, body.get('schema'), schema_report + suffix))
    if body.get('blinded') is not True:
        chk.fail('E_SEAL1_NOT_BLINDED', label)
    if body.get('test_mode') is not False:
        chk.fail('E_SEAL1_TEST_MODE', '%s: test_mode must be false (the sealed compare on the sealed prereg)' % label)
    if body.get('script_sha256') != sealed_sha:
        chk.fail('E_SEAL1_SCRIPT_NOT_THE_SEALED_COMPARE', '%s: script_sha256 %r, sealed compare %s' % (label, body.get('script_sha256'), sealed_sha))
    if body.get('route_a_mode') != mode:
        chk.fail('E_SEAL1_ROUTE_A_MODE', '%s: route_a_mode %r, the case block mode %r' % (label, body.get('route_a_mode'), mode))
    if suffix == '_VALIDITY_ONLY':
        cases = body.get('cases')
        if not (isinstance(cases, dict) and set(cases) == {'C5H'}):
            chk.fail('E_SEAL1_VALIDITY_CASES_NOT_C5H', '%s: the B6 validity run is --validity-only --case C5H' % label)
    else:
        if not (isinstance(body.get('gates'), dict) and body['gates']):
            chk.fail('E_SEAL1_GATES_SHAPE', '%s carries no gates' % label)
    nums = number_tokens(body)
    if nums:
        chk.fail('E_SEAL1_OUTPUT_VALUE_BEARING', '%s: %d number(s); blinded output prints codes only (A47 I3): %s' % (label, len(nums), '; '.join(nums[:3])))
    masked = HEX64_ANY.sub(lambda m: 'h' * 64, text)                 # the v001 row-value rule, after masking shas and the compare's
    masked = NUMBER_RX.sub(lambda m: 'n' * len(m.group(0)) if m.group(0) in ALLOWED_NUMBER_TOKENS else m.group(0), masked)   # allowed constants
    if ROW_VALUE_RX.search(masked):
        chk.fail('E_SEAL1_OUTPUT_MAY_SHOW_A_ROW_VALUE', '%s contains a decimal number; blinded output prints codes only (A47 I3)' % label)
    return {'path': str(p.resolve()), 'sha256': C.sha_bytes(raw), 'text': text}


def key_map_codes(chk, obj, case_block_map):
    if not (isinstance(obj, dict) and obj.get('schema') == KEY_MAP_SCHEMA and set(obj) - {'note'} == {'schema', 'key_equivalence_map'}):
        chk.fail('KEY_MAP_SCHEMA', 'keys exactly schema = %s, key_equivalence_map (note optional)' % KEY_MAP_SCHEMA)
        return None
    km = obj['key_equivalence_map']
    if not isinstance(km, list):
        chk.fail('KEY_MAP_SCHEMA', 'key_equivalence_map must be a list')
        return None
    seen = {}
    for j, x in enumerate(km):
        if not (isinstance(x, dict) and set(x) == KEY_MAP_ENTRY_KEYS and isinstance(x['pointer'], str) and x['pointer'].startswith('/numerics/')
                and isinstance(x['b0_identity_evidence'], str) and x['b0_identity_evidence']):
            chk.fail('KEY_MAP_ENTRY', 'key_equivalence_map[%d]: exactly {pointer (/numerics/..), absent_equivalent_value, b0_identity_evidence} (A48 AMB-13)' % j)
            continue
        if x['pointer'].split('/')[2] in KEY_MAP_UNMAPPABLE:
            chk.fail('KEY_MAP_ENTRY', 'key_equivalence_map[%d]: %s may not be mapped' % (j, x['pointer']))
        if x['pointer'] in seen:
            chk.fail('KEY_MAP_DUPLICATE_POINTER', 'key_equivalence_map[%d] and [%d] map one pointer (A71)' % (seen[x['pointer']], j))
        seen.setdefault(x['pointer'], j)
    if json.dumps(km, sort_keys=True) != json.dumps(case_block_map, sort_keys=True):
        chk.fail('KEY_MAP_NOT_THE_CASE_BLOCK_MAP', 'the SEAL_RECORD key map must equal the validated case block\'s key_equivalence_map (R-10)')
    return km


def new_items_codes(chk, obj, reviewed_sha):
    if not (isinstance(obj, dict) and obj.get('schema') == NEW_ITEMS_SCHEMA and set(obj) - {'note'} == {'schema', 'compare_impl', 'items'}):
        chk.fail('NEW_ITEMS_SCHEMA', 'keys exactly schema = %s, compare_impl, items (note optional)' % NEW_ITEMS_SCHEMA)
        return None
    if chk.pin('new_item_dispositions.compare_impl', obj['compare_impl']):
        if reviewed_sha not in Path(obj['compare_impl']['path']).read_bytes().decode('utf-8', 'replace'):
            chk.fail('NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE', 'the compare IMPL the list is taken from must name the reviewed source sha in full (A81 RI-20)')
    items = obj['items']
    if not isinstance(items, list):
        chk.fail('NEW_ITEMS_SCHEMA', 'items must be a list')
        return None
    seen = {}
    for j, x in enumerate(items):
        if not (isinstance(x, dict) and set(x) == {'id', 'disposition', 'reason', 'must_fail_tests'} and isinstance(x['id'], str)
                and re.fullmatch(r'NEW-\d{1,3}', x['id']) and x['disposition'] in NEW_DISPOSITIONS and isinstance(x['reason'], str)
                and x['reason'].strip() and isinstance(x['must_fail_tests'], list)
                and all(isinstance(t, str) and t.strip() for t in x['must_fail_tests'])):
            chk.fail('NEW_ITEMS_ENTRY', 'items[%d]: exactly {id NEW-<n>, disposition ADOPTED|REJECTED, reason, must_fail_tests [str]}' % j)
            continue
        if x['disposition'] == 'ADOPTED' and not x['must_fail_tests']:
            chk.fail('NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL', 'items[%d] %s: an adopted item names its MUST_FAIL tests (A75, A81 RI-20)' % (j, x['id']))
        if x['id'] in seen:
            chk.fail('NEW_ITEMS_DUPLICATE_ID', 'items[%d] and items[%d] carry one id (A71)' % (seen[x['id']], j))
        seen.setdefault(x['id'], j)
    return items


def custody_codes(chk, obj, driver_sha):
    req = {'schema', 'identity_run', 'driver_sha256', 'stages_total', 'stages_successor', 'verdict', 'method'}
    if not (isinstance(obj, dict) and obj.get('schema') == CUSTODY_SCHEMA and req <= set(obj) and set(obj) - req <= {'evidence', 'note'}):
        chk.fail('CUSTODY_SCHEMA', 'keys %s (evidence, note optional), schema %s' % (sorted(req), CUSTODY_SCHEMA))
        return None
    if obj['identity_run'] != 'Z2':
        chk.fail('CUSTODY_RUN', 'the raw successor-custody check is of the Z2 run (A59)')
    if obj['driver_sha256'] != driver_sha:
        chk.fail('CUSTODY_DRIVER_NOT_THE_SLOT', 'the checked run must be on the driver slot (A67 N1)')
    st, ss = obj['stages_total'], obj['stages_successor']
    if not (type(st) is int and st > 0 and type(ss) is int and ss == st):
        chk.fail('CUSTODY_STAGES', 'every stage must run its successor script: stages_successor = stages_total > 0 (A59)')
    if obj['verdict'] != 'PASS':
        chk.fail('CUSTODY_VERDICT', repr(obj['verdict']))
    if not (isinstance(obj['method'], str) and obj['method'].strip()):
        chk.fail('CUSTODY_SCHEMA', 'method must be a non-empty string')
    ev = obj.get('evidence', [])
    if not isinstance(ev, list):
        chk.fail('CUSTODY_SCHEMA', 'evidence must be a list of {path, sha256}')
    else:
        for j, x in enumerate(ev):
            chk.pin('raw_successor_custody.evidence[%d]' % j, x)
    return obj


def b2_codes(chk, path, registry_path, gate_schema):
    """A100 / r5 SRR: the B2 record of record, whose disclosure block the seal record repeats: a PASS B2 gate record registered as the
    B2 record of record in the slot's producer registry (gate_records.B2), carrying a disclosure object."""
    if not Path(path).is_file():
        chk.fail('B2_RECORD_MISSING', str(path))
        return None
    try:
        rec = C.strict_json(path)
        reg = C.strict_json(registry_path)
    except Exception as e:
        chk.fail('B2_RECORD_JSON', '%s: %s' % (type(e).__name__, e))
        return None
    if not (isinstance(rec, dict) and rec.get('schema') == gate_schema and rec.get('gate') == 'B2'):
        chk.fail('B2_RECORD_NOT_A_B2_RECORD', 'schema %s, gate B2' % gate_schema)
        return None
    if rec.get('verdict') != 'PASS':
        chk.fail('B2_RECORD_NOT_PASS', repr(rec.get('verdict')))
    rsha = C.sha(path)
    gr = ((reg.get('gate_records') or {}) if isinstance(reg, dict) else {}).get('B2')
    if not (isinstance(gr, list) and rsha in gr):
        chk.fail('B2_RECORD_NOT_REGISTERED', 'the B2 record is not the registry\'s B2 record of record (gate_records.B2)')
    if not (isinstance(rec.get('disclosure'), dict) and rec['disclosure']):
        chk.fail('B2_RECORD_NO_DISCLOSURE', 'the B2 record of record carries no disclosure block (A100)')
        return None
    return {'record': {'path': str(Path(path).resolve()), 'sha256': rsha}, 'disclosure': rec['disclosure']}


def no_change_note(e, changed):
    c = next((x for x in changed if x['entry'] == e), None)
    if c is None:
        return '%s: covers this entry for the prereg text of record (A81 RI-26)' % e
    return ('%s: its section changed after the text of record was written (table row %s, frozen %s); root\'s explicit seal-record note '
            '(A81 RI-26)' % (e, c['row_section_sha256'], c['frozen_section_sha256']))


def build(a):
    res = T3.run(a.slots, a.prereg, a.text_of_record, a.frozen, a.covered_later, a.reviewed, a.sealed_compare)
    chk = C.Checker('build_seal_record_c4v002')
    for f in res['failures']:
        chk.fail('T3:' + f['code'], f['detail'])
    if chk.failures:
        return chk.result(), None
    pt = res.get('passthrough') or {}
    slots = C.strict_json(a.slots)
    sp = C.strict_json(a.prereg)
    need = ['text_of_record', 'case_block', 'route_a_mode', 'key_equivalence_map', 'ddo_gas_M_s_registered', 'admission_entry', 'build',
            'admission_allowlist', 'driver_build', 'entry_table'] + (['cascade_map_r5_addendum'] if slots['driver_branch'] == 'r5' else [])
    for k in need:
        if pt.get(k) is None:
            chk.fail('PASSTHROUGH_MISSING', k)
    if chk.failures:
        return chk.result(), None
    plan = C.strict_json(slots['launch_packet']['bound_plan']['path'])
    sealed_sha = C.sha(a.sealed_compare)
    schema_report = sealed_schema_report(a.sealed_compare)
    if not isinstance(schema_report, str):
        chk.fail('SEALED_COMPARE_SCHEMA_REPORT_UNREADABLE', 'no module-level SCHEMA_REPORT string in the sealed compare')
        return chk.result(), None
    outputs = {}
    for (label, name, suffix), path in zip(B6, (a.gates_only_output, a.validity_only_output)):
        o = b6_codes(chk, label, path, name, suffix, schema_report, sealed_sha, pt['route_a_mode'])
        if o is not None:
            outputs[label] = o
    extras, quoted = {}, {}
    for label, path in (('key_equivalence_map', a.key_equivalence_map), ('new_item_dispositions', a.new_item_list), ('raw_successor_custody', a.successor_custody)):
        if not Path(path).is_file():
            chk.fail('SEAL_RECORD_INPUT_MISSING', label)
            continue
        try:
            obj = C.strict_json(path)
        except Exception as e:
            chk.fail('SEAL_RECORD_INPUT_JSON', '%s: %s' % (label, e))
            continue
        if label == 'key_equivalence_map':
            q = key_map_codes(chk, obj, pt['key_equivalence_map'])
        elif label == 'new_item_dispositions':
            q = new_items_codes(chk, obj, slots['compare_reviewed_source']['sha256'])
        else:
            q = custody_codes(chk, obj, slots['driver']['sha256'])
        extras[label] = {'path': str(Path(path).resolve()), 'sha256': C.sha(path)}
        quoted[label] = q
    if chk.failures:
        return chk.result(), None
    srr = sp.get('seal_record_requirements') or []
    b2_req = [r['text'] for r in srr if isinstance(r, dict) and isinstance(r.get('text'), str) and B2_SRR_MARK in r['text']]
    b2 = None
    if b2_req:
        if not getattr(a, 'b2_record', None):
            chk.fail('B2_DISCLOSURE_REQUIRED', 'the prereg asks the seal record to repeat the B2 disclosure block (A100): give --b2-record')
        else:
            b2 = b2_codes(chk, a.b2_record, slots['producer_registry']['path'], pt.get('gate_schema'))
            if b2 is not None:
                b2['requirement'] = b2_req[0]
    if chk.failures:
        return chk.result(), None
    disclosures = [r['text'] for r in srr if isinstance(r, dict) and isinstance(r.get('text'), str) and r['text'].startswith('Disclosure')]
    if not any(t.startswith('Disclosure E5-08') for t in disclosures):
        chk.fail('E5_08_TEXT_NOT_FOUND', 'the prereg carries the E5-08 disclosure text')
        return chk.result(), None
    et = pt['entry_table']
    sealed_compare = {'path': str(Path(a.sealed_compare).resolve()), 'sha256': sealed_sha}
    rec = {
        'schema': SCHEMA,
        'sealed_by': dict(C.AUTHORITY),
        'prereg': {'path': str(Path(a.prereg).resolve()), 'sha256': C.sha(a.prereg)},
        'compare': sealed_compare,
        'driver': dict(plan['driver']),
        'frozen_addendum': dict(plan['frozen_addendum']),
        'driver_branch': slots['driver_branch'],
        'text_of_record': dict(pt['text_of_record']),
        'bound_plan': dict(slots['launch_packet']['bound_plan']),
        'bound_command': dict(slots['launch_packet']['bound_command']),
        'build': dict(pt['build']),
        'admission_allowlist': dict(pt['admission_allowlist']),
        'launch_entry': {k: dict(v) for k, v in pt['admission_entry'].items()},
        'case_block': dict(pt['case_block']),
        'route_a_mode': pt['route_a_mode'],
        'compare_reviewed_source': dict(slots['compare_reviewed_source']),
        'identity_comparator': dict(slots['identity_comparator']),
        'identity_gate_records': {k: dict(v) for k, v in slots['identity_gate_records'].items()},
        'certificates': {k: dict(v) for k, v in slots['certificates'].items()},
        'producer_registry': dict(slots['producer_registry']),
        'driver_build_record': dict(slots['driver_build_record']),
        'driver_check_record': dict(slots['driver_check_record']),
        'ngc_gas_M_s': slots['ngc_gas_M_s'],
        'ddo_gas_M_s_registered': pt['ddo_gas_M_s_registered'],
        'e_seal1': {k: {'path': v['path'], 'sha256': v['sha256']} for k, v in outputs.items()},
        'e_seal1_text': {k: v['text'] for k, v in outputs.items()},
        'no_row_value_shown': True,
        'disclosures': disclosures,
        'entry_table': {'key': et['key'], 'table': sp[et['key']]},
        'no_change_notes': [no_change_note(e, pt.get('changed_sections') or []) for e in a.covered_later],
        'key_equivalence_map_quoted': quoted['key_equivalence_map'],
        'new_item_dispositions_quoted': quoted['new_item_dispositions'],
        'raw_successor_custody_quoted': quoted['raw_successor_custody'],
        'sealed_status_authority': STATUS_AUTHORITY,
        'pending_strings_outside_slot_values': list(pt.get('pending_strings_outside_slot_values') or []),
        **extras,
    }
    if b2 is not None:
        rec['b2_disclosure'] = b2
    if slots['driver_branch'] == 'r6':
        rec['cache_directory'] = dict(slots['cache_directory_r6_only'])
    else:
        rec['cascade_map_r5_addendum'] = dict(pt['cascade_map_r5_addendum'])
    if rec['driver'] != slots['driver'] or rec['frozen_addendum'] != slots['frozen_addendum']:
        chk.fail('PLAN_PINS_NOT_SLOTS', 'internal: the bound plan and the slots disagree')
        return chk.result(), None
    text = json.dumps(rec, indent=1, sort_keys=True, ensure_ascii=False) + '\n'
    out = chk.result()
    out['seal_record_sha256'] = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return out, text


def _check_admission_config(config_path, seal_record_path):
    chk = C.Checker('check_admission_config_c4v002')
    try:
        cfg = C.strict_json(config_path)
        seal = C.strict_json(seal_record_path)
    except Exception as e:
        chk.fail('ADMISSION_INPUT_JSON', type(e).__name__ + ': ' + str(e))
        return chk.result()
    if not (isinstance(cfg, dict) and isinstance(seal, dict)):
        chk.fail('ADMISSION_INPUT_SHAPE', 'the config and the SEAL_RECORD must be JSON objects')
        return chk.result()
    if seal.get('schema') != SCHEMA:
        chk.fail('ADMISSION_SEAL_RECORD_SCHEMA', repr(seal.get('schema')))
        return chk.result()
    req = {'schema', 'authority', 'seal', 'prereg', 'compare', 'build', 'producer_allowlist'}
    if set(cfg) - {'note'} != req:
        chk.fail('ADMISSION_CONFIG_KEYS', 'exactly %s (note optional), FORMAT_V004' % sorted(req))
        return chk.result()
    if cfg['schema'] != C.ADMISSION_SCHEMA:
        chk.fail('ADMISSION_CONFIG_SCHEMA', repr(cfg['schema']))
    if cfg['authority'] != C.AUTHORITY:
        chk.fail('ADMISSION_CONFIG_AUTHORITY', 'the authority equals sealed_by (FORMAT_V004)')
    for k in ('seal', 'prereg', 'compare', 'build'):
        chk.pin('config.' + k, cfg[k])
    if cfg['seal'] != {'path': str(Path(seal_record_path).resolve()), 'sha256': C.sha(seal_record_path)}:
        chk.fail('ADMISSION_CONFIG_SEAL_NOT_THE_RECORD', 'the config must pin this SEAL_RECORD (path and full sha, A81 RI-19)')
    if cfg['prereg'] != seal.get('prereg') or cfg['compare'] != seal.get('compare'):
        chk.fail('ADMISSION_CONFIG_PREREG_COMPARE', 'prereg and compare pins exactly match the seal (FORMAT_V004)')
    if cfg['build'] != seal.get('build') or Path(str((cfg['build'] or {}).get('path', ''))).name != C.BUILD_V007_NAME:
        chk.fail('ADMISSION_CONFIG_BUILD_NOT_BUILD_V007', 'the config pins the record\'s BUILD_V007 (A99.1)')
    allow = cfg['producer_allowlist']
    if not (isinstance(allow, dict) and all(isinstance(p, str) and isinstance(h, str) for p, h in allow.items())):
        chk.fail('ADMISSION_ALLOWLIST_SHAPE', 'producer_allowlist maps absolute source paths to full sha256')
        return chk.result()
    if len(allow) != C.BUILD_ALLOWLIST_COUNT:
        chk.fail('ADMISSION_ALLOWLIST_COUNT_NOT_15', '%d sources; BUILD_V007 supports %d (V6-S3)' % (len(allow), C.BUILD_ALLOWLIST_COUNT))
    if allow != seal.get('admission_allowlist'):
        chk.fail('ADMISSION_ALLOWLIST_NOT_THE_SEAL_RECORD_ALLOWLIST', 'the producer_allowlist must be the record\'s 15-source BUILD_V007 allowlist')
    if 'config.build' in chk.pins:
        btext = Path(cfg['build']['path']).read_bytes().decode('utf-8')
        sub = C.Checker('build')
        ballow = C.build_allowlist_codes(sub, btext)
        for f in sub.failures:
            chk.fail('ADMISSION_' + f['code'], f['detail'])
        if ballow is not None and allow != ballow:
            chk.fail('ADMISSION_ALLOWLIST_NOT_THE_BUILD_ALLOWLIST', 'the producer_allowlist must equal BUILD_V007\'s supported-entry allowlist exactly')
        for p, h in allow.items():
            if ('%s  %s' % (h, p)) not in btext:
                chk.fail('ADMISSION_ALLOWLIST_NOT_IN_BUILD', '%s is not listed literally in the BUILD (guard v008 L37)' % p)
    for p, h in allow.items():
        if Path(p).suffix != '.py' or not Path(p).is_file() or C.sha(p) != h:
            chk.fail('ADMISSION_ALLOWLIST_SOURCE_BYTES', '%s (guard v008 L36)' % p)
    le = seal.get('launch_entry') or {}
    for k in ('launcher', 'guard'):
        ref = le.get(k)
        if not (C.is_pin(ref) and allow.get(ref['path']) == ref['sha256']):
            chk.fail('ADMISSION_CONFIG_%s_NOT_NAMED_EXACTLY' % k.upper(), 'the config must name the record\'s %s source exactly (SRR[10], A78 N2)' % k)
    return chk.result()


def check_admission_config(config_path, seal_record_path):
    return C.guarded_run('check_admission_config_c4v002', _check_admission_config, config_path, seal_record_path)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if any(x.split('=', 1)[0] == '--check-admission-config' for x in argv):
        p = C.parser('check root\'s ROOT_SEAL_ADMISSION config against the SEAL_RECORD and its BUILD_V007 allowlist (writes nothing)')
        p.add_argument('--check-admission-config', required=True)
        p.add_argument('--seal-record', required=True)
        a = C.parse_args(p, argv)
        return C.emit(check_admission_config(a.check_admission_config, a.seal_record))
    p = C.parser('build the exact SEAL_RECORD bytes (prints them; writes nothing)')
    for flag in ('--slots', '--prereg', '--text-of-record', '--frozen', '--reviewed', '--sealed-compare', '--gates-only-output', '--validity-only-output',
                 '--key-equivalence-map', '--new-item-list', '--successor-custody'):
        p.add_argument(flag, required=True)
    p.add_argument('--covered-later', default='')
    p.add_argument('--b2-record')
    a = C.parse_args(p, argv)
    a.covered_later = [x.strip() for x in a.covered_later.split(',') if x.strip()]
    res, text = safe_build(a)
    print(json.dumps(res, indent=1, sort_keys=True), file=sys.stderr)
    if text is None:
        return 2
    sys.stdout.write(text)
    return 0


def safe_build(a):
    try:
        return build(a)
    except (Exception, SystemExit) as e:                          # D-07 class: a code, never a traceback
        return ({'check': 'build_seal_record_c4v002', 'verdict': 'REFUSE', 'failures': [{'code': 'INTERNAL_EXCEPTION:%s' % type(e).__name__,
                                                                                      'detail': str(e)[:300]}], 'notes': [], 'pins_verified': {}}, None)


if __name__ == '__main__':
    raise SystemExit(main())
