# Claude4 helper (dispatch 0650, A113 P6 step 4): validate the three B7 inputs with seal tool 4's OWN functions, loaded from
# v007_final_prereg_c4/seal_tools_v004/ (tool 4 and its siblings verified from bytes first), the way build() calls them:
#   key_map_codes(chk, obj, pt['key_equivalence_map'])           pt from tool 3 = the case block's top-level cb.get('key_equivalence_map', [])
#   new_items_codes(chk, obj, slots['compare_reviewed_source']['sha256'])
#   custody_codes(chk, obj, slots['driver']['sha256'])
# Each input is read with tool 4's own C.strict_json (as build() reads it). Then one or more must-fail per function. The custody input
# is the converter's SYNTHETIC output (root produces the real one). Results are written once, by exclusive create.
# Run under tools/run_fenced_c4st2.py. usage: validate_b7_with_tool4_c4v001.py OUT.json
import copy, hashlib, importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ST = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004')
PINS = {'build_seal_record_c4v004.py': '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41',
        'seal_common_c4v003.py': '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21',
        'check_slot_fill_c4v003.py': '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af',
        'check_sealed_compare_c4v003.py': 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1'}
CASE_BLOCK = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
              '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
PREREG_R6 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json',
             'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9')
DISCLOSURES = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json',
               'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3')
REVIEWED = {'r13': 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157', 'r14': 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'}
R5 = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
R4 = 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
FILE1 = ROOT / 'KEY_EQUIVALENCE_MAP_V007.json'
FILE2 = ROOT / 'NEW_ITEM_DISPOSITIONS_V007.json'
FILE2_R14 = ROOT / 'NEW_ITEM_DISPOSITIONS_V007_R14_VARIANT.json'
CUSTODY_SYNTH = ROOT / 'fixtures' / 'custody_cli_v002' / 'CUSTODY_CLI_PASS.json'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv):
    outp = Path(argv[0])
    res = {'tool4_dir': str(ST), 'pins_verified': {}, 'build_call_sites': {}, 'calls': [], 'synthetic_custody_only': True}
    for name, h in PINS.items():
        got = sha(ST / name)
        res['pins_verified'][name] = {'sha256': got, 'ok': got == h}
        if got != h:
            print('REFUSED: %s is %s, pinned %s' % (name, got, h), file=sys.stderr)
            return 2
    t4_src = (ST / 'build_seal_record_c4v004.py').read_text(encoding='utf-8')
    for k, s in (('key_map', "q = key_map_codes(chk, obj, pt['key_equivalence_map'])"),
                 ('new_items', "q = new_items_codes(chk, obj, slots['compare_reviewed_source']['sha256'])"),
                 ('custody', "q = custody_codes(chk, obj, slots['driver']['sha256'])"),
                 ('inputs_read_by_strict_json', 'obj = C.strict_json(path)')):
        res['build_call_sites'][k] = {'text': s, 'present_once': t4_src.count(s) == 1}
    spec = importlib.util.spec_from_file_location('build_seal_record_c4v004', str(ST / 'build_seal_record_c4v004.py'))
    T4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(T4)
    C = T4.C
    res['loaded'] = {'tool4': T4.__file__, 'seal_common': C.__file__, 'KEY_MAP_SCHEMA': T4.KEY_MAP_SCHEMA, 'NEW_ITEMS_SCHEMA': T4.NEW_ITEMS_SCHEMA,
                     'CUSTODY_SCHEMA': T4.CUSTODY_SCHEMA}

    def call(label, fn, obj, arg, expect_codes):
        chk = C.Checker('validate_b7_c4v001')
        try:
            ret = fn(chk, obj, arg)
            exc = None
        except Exception as e:
            ret, exc = None, '%s: %s' % (type(e).__name__, str(e)[:200])
        codes = [f['code'] for f in chk.failures]
        ok = (exc is None) and (sorted(set(codes)) == sorted(set(expect_codes))) and (bool(codes) == bool(expect_codes))
        row = {'call': label, 'function': fn.__name__, 'arg': arg if isinstance(arg, str) else '<case block map %s>' % json.dumps(arg),
               'expected_codes': expect_codes, 'codes': codes, 'details': [f['detail'][:240] for f in chk.failures], 'exception': exc,
               'returned_none': ret is None, 'pins_verified': sorted(chk.pins), 'ok': ok}
        res['calls'].append(row)
        return row

    # ---- inputs of record, read as build() reads them
    cb = C.strict_json(CASE_BLOCK[0])
    assert sha(CASE_BLOCK[0]) == CASE_BLOCK[1]
    cb_map = cb.get('key_equivalence_map', [])
    pr = C.strict_json(PREREG_R6[0])
    assert sha(PREREG_R6[0]) == PREREG_R6[1]
    slot_driver = pr['seal_slots']['driver']['named_candidates_verified_from_bytes']['r5']
    res['prereg_r6_driver_slot_candidate'] = slot_driver
    res['driver_slot_sha_is_r5_b5cc62af'] = slot_driver.get('sha256') == R5
    f1 = C.strict_json(str(FILE1))
    f2 = C.strict_json(str(FILE2))
    f2b = C.strict_json(str(FILE2_R14))
    cu = C.strict_json(str(CUSTODY_SYNTH))
    res['inputs'] = {str(p): sha(p) for p in (FILE1, FILE2, FILE2_R14, CUSTODY_SYNTH)}
    # ---- 1. key map
    call('KEY_MAP_OF_RECORD', T4.key_map_codes, f1, cb_map, [])
    bad = copy.deepcopy(f1)
    bad['key_equivalence_map'] = [{'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0,
                                   'b0_identity_evidence': 'synthetic must-fail entry'}]
    call('MUST_FAIL_KEY_MAP_NOT_THE_CASE_BLOCK_MAP', T4.key_map_codes, bad, cb_map, ['KEY_MAP_NOT_THE_CASE_BLOCK_MAP'])
    bad2 = dict(f1, schema='UNT_V007_SEAL_KEY_EQUIVALENCE_MAP_C4V001')
    call('MUST_FAIL_KEY_MAP_SCHEMA', T4.key_map_codes, bad2, cb_map, ['KEY_MAP_SCHEMA'])
    # ---- 2. NEW-item dispositions
    call('NEW_ITEMS_OF_RECORD_R13_ON_THE_R13_REVIEWED_SHA', T4.new_items_codes, f2, REVIEWED['r13'], [])
    call('NEW_ITEMS_R14_VARIANT_ON_THE_R14_REVIEWED_SHA', T4.new_items_codes, f2b, REVIEWED['r14'], [])
    call('MUST_FAIL_NEW_ITEMS_R13_FILE_WITH_THE_R14_SLOT', T4.new_items_codes, f2, REVIEWED['r14'], ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'])
    bad3 = copy.deepcopy(f2)
    bad3['items'][0]['must_fail_tests'] = []
    call('MUST_FAIL_NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL', T4.new_items_codes, bad3, REVIEWED['r13'], ['NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL'])
    bad4 = copy.deepcopy(f2)
    bad4['items'].append(copy.deepcopy(bad4['items'][0]))
    call('MUST_FAIL_NEW_ITEMS_DUPLICATE_ID', T4.new_items_codes, bad4, REVIEWED['r13'], ['NEW_ITEMS_DUPLICATE_ID'])
    # completeness against the C-08 id index (root's table; tool 4 itself does not compare the list with it)
    c08 = [r['new_item_id'] for r in C.strict_json(DISCLOSURES[0])['c08_table']]
    assert sha(DISCLOSURES[0]) == DISCLOSURES[1]
    for lab, f in (('r13', f2), ('r14_variant', f2b)):
        ids = [x['id'] for x in f['items']]
        res.setdefault('c08_completeness', {})[lab] = {
            'c08_ids': len(c08), 'items': len(ids), 'in_c08_order': ids == [x for x in c08 if x in ids],
            'missing_from_file': [x for x in c08 if x not in ids], 'not_in_c08': [x for x in ids if x not in c08],
            'dispositions': sorted({x['disposition'] for x in f['items']}),
            'every_adopted_names_a_test': all(x['must_fail_tests'] for x in f['items'] if x['disposition'] == 'ADOPTED')}
    res['tool4_checks_completeness_against_c08'] = 'c08' in t4_src[t4_src.find('def new_items_codes'):t4_src.find('def custody_codes')]
    # ---- 3. raw successor custody (the converter's SYNTHETIC output; root produces the real one)
    call('CUSTODY_SYNTHETIC_ON_THE_DRIVER_SLOT_SHA', T4.custody_codes, cu, R5, [])
    call('MUST_FAIL_CUSTODY_ON_THE_R4_DRIVER_SHA', T4.custody_codes, cu, R4, ['CUSTODY_DRIVER_NOT_THE_SLOT'])
    bad5 = dict(cu, stages_successor=cu['stages_total'] - 1)
    call('MUST_FAIL_CUSTODY_A_STAGE_WITHOUT_ITS_SUCCESSOR', T4.custody_codes, bad5, R5, ['CUSTODY_STAGES'])
    bad6 = dict(cu, identity_run='Z2_OFF_RO1')
    call('MUST_FAIL_CUSTODY_NOT_Z2', T4.custody_codes, bad6, R5, ['CUSTODY_RUN'])
    res['n_calls'] = len(res['calls'])
    res['n_ok'] = sum(1 for r in res['calls'] if r['ok'])
    res['all_ok'] = (res['n_ok'] == res['n_calls'] and all(v['present_once'] for v in res['build_call_sites'].values())
                     and res['driver_slot_sha_is_r5_b5cc62af'])
    with open(outp, 'x', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True) + '\n')
    print(json.dumps({'all_ok': res['all_ok'], 'n_ok': res['n_ok'], 'n_calls': res['n_calls'], 'out': str(outp), 'sha256': sha(outp),
                      'c08_completeness': res['c08_completeness'], 'tool4_checks_completeness_against_c08': res['tool4_checks_completeness_against_c08'],
                      'build_call_sites': {k: v['present_once'] for k, v in res['build_call_sites'].items()}}, sort_keys=True))
    for r in res['calls']:
        print('%-50s %-16s expect %-45s got %s ok=%s' % (r['call'], r['function'], r['expected_codes'], r['codes'], r['ok']))
    return 0 if res['all_ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
