# Claude4 refute helper (dispatch 0650, refute_p6): re-derive the builder's B7 claims with seal tool 4's OWN functions, in this
# process, from bytes. Tool 4 and its siblings are loaded from v007_final_prereg_c4/seal_tools_v004/ after their bytes are hashed;
# the builder's generator is loaded from its file to test the A118 completion path (build() only; nothing is written by it).
#  1. key map: the case block of record, parsed by tool 4's C.strict_json; key_equivalence_map at top level (where r13/r14
#     validate_case_block L1557 and tool 3 L482 read it) and nowhere else; key_map_codes on file 1, plus must-fails.
#  2. NEW items: C-08 ids vs the files; new_items_codes on the r13 file (f5adfd11), the R14 variant (f3f9ba7e), must-fails;
#     tool 4 accepts an id outside C-08 and a 17-of-19 list (P6-S1); the A118 completion (r14, NEW-30/NEW-44 ADOPTED) in memory.
#  3. custody: the converter's dry-run record on this folder's synthetic 18-stage control (refute fixture), custody_codes on the
#     driver slot sha, plus must-fails.
# Results are written once by exclusive create. Run under tools/run_fenced_c4st2.py. usage: validate_b7_refute_r6v001.py OUT.json
import contextlib, copy, hashlib, importlib.util, io, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
B = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_b7_inputs_c4')
ST = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004')
T4_SHA = '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41'           # dispatch pin (claim under test)
CASE_BLOCK = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json',
              '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71')
PREREG_R6 = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json',
             'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9')
DISCLOSURES = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json',
               'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3')
V006 = ('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
        'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md')
CMP = {'r13': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py',
       'r14': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py'}
R5 = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
R4 = 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
FIX = ROOT / 'fixtures' / 'real_stage_set_v001' / 'CONTROL_BUILDER_18_STAGES'


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha(p):
    return sha_b(Path(p).read_bytes())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def keys_anywhere(o, key, where='$', out=None):
    out = [] if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                out.append(where + '.' + k)
            keys_anywhere(v, key, where + '.' + k, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            keys_anywhere(v, key, '%s[%d]' % (where, i), out)
    return out


def main(argv):
    outp = Path(argv[0])
    res = {'pins': {}, 'calls': []}
    for n in ('build_seal_record_c4v004.py', 'seal_common_c4v003.py', 'check_slot_fill_c4v003.py', 'check_sealed_compare_c4v003.py'):
        res['pins'][n] = sha(ST / n)
    assert res['pins']['build_seal_record_c4v004.py'] == T4_SHA, 'tool 4 bytes are not 9787cf58'
    T4 = load('build_seal_record_c4v004', ST / 'build_seal_record_c4v004.py')
    C = T4.C
    src = (ST / 'build_seal_record_c4v004.py').read_text(encoding='utf-8')
    res['tool4_call_sites'] = {s: src.count(s) for s in ("q = key_map_codes(chk, obj, pt['key_equivalence_map'])",
                                                         "q = new_items_codes(chk, obj, slots['compare_reviewed_source']['sha256'])",
                                                         "q = custody_codes(chk, obj, slots['driver']['sha256'])", 'obj = C.strict_json(path)')}
    t3 = (ST / 'check_slot_fill_c4v003.py').read_text(encoding='utf-8').split('\n')
    res['tool3_L482'] = t3[481].strip()
    res['tool3_L485'] = t3[484].strip()
    for v, p in CMP.items():
        lines = Path(p).read_text(encoding='utf-8').split('\n')
        res['compare_%s_sha256' % v] = sha(p)
        res['compare_%s_L1557' % v] = lines[1556].strip()
        res['compare_%s_def_validate_case_block_line' % v] = next(i + 1 for i, l in enumerate(lines) if l.startswith('def validate_case_block('))

    def call(label, fn, obj, arg, expect):
        chk = C.Checker('refute_p6')
        exc = None
        try:
            fn(chk, obj, arg)
        except Exception as e:                      # tool 4 would turn this into a coded refusal; record it
            exc = '%s: %s' % (type(e).__name__, str(e)[:200])
        codes = sorted({f['code'] for f in chk.failures})
        row = {'call': label, 'function': fn.__name__, 'codes': codes, 'expected': sorted(expect), 'exception': exc,
               'ok': exc is None and codes == sorted(expect), 'pins_verified': sorted(chk.pins)}
        res['calls'].append(row)
        return row

    # ---- 1. key map
    cb_raw = Path(CASE_BLOCK[0]).read_bytes()
    res['case_block_sha256'] = sha_b(cb_raw)
    cb = C.strict_json_bytes(cb_raw)
    res['case_block_top_keys'] = sorted(cb)
    res['case_block_key_map_top_level_present'] = 'key_equivalence_map' in cb
    res['case_block_key_map_value'] = cb.get('key_equivalence_map', '<ABSENT>')
    res['case_block_key_map_paths_anywhere'] = keys_anywhere(cb, 'key_equivalence_map')
    pr = C.strict_json(PREREG_R6[0])
    res['prereg_r6_sha256'] = sha(PREREG_R6[0])
    res['prereg_r6_binding_case_block'] = pr['binding_inputs']['case_block']
    res['prereg_r6_binding_case_block_is_the_case_block'] = pr['binding_inputs']['case_block'] == {'path': CASE_BLOCK[0], 'sha256': res['case_block_sha256']}
    cbm = cb.get('key_equivalence_map', [])         # exactly tool 3 L482
    f1 = C.strict_json(B / 'KEY_EQUIVALENCE_MAP_V007.json')
    res['file1_sha256'] = sha(B / 'KEY_EQUIVALENCE_MAP_V007.json')
    call('KEY_MAP_FILE1_VS_CASE_BLOCK_MAP', T4.key_map_codes, f1, cbm, [])
    m = copy.deepcopy(f1); m['key_equivalence_map'] = [{'pointer': '/numerics/route_a/x', 'absent_equivalent_value': 1, 'b0_identity_evidence': 'e'}]
    call('MUST_FAIL_KEY_MAP_EXTRA_ENTRY', T4.key_map_codes, m, cbm, ['KEY_MAP_NOT_THE_CASE_BLOCK_MAP'])
    m = copy.deepcopy(f1); m['key_equivalence_map'] = [{'pointer': '/numerics/uv_tail/x', 'absent_equivalent_value': 1, 'b0_identity_evidence': 'e'}]
    call('MUST_FAIL_KEY_MAP_UNMAPPABLE_POINTER', T4.key_map_codes, m, cbm, ['KEY_MAP_ENTRY', 'KEY_MAP_NOT_THE_CASE_BLOCK_MAP'])
    m = copy.deepcopy(f1); m['key_equivalence_map'] = {}
    call('MUST_FAIL_KEY_MAP_NOT_A_LIST', T4.key_map_codes, m, cbm, ['KEY_MAP_SCHEMA'])
    m = copy.deepcopy(f1); m['extra'] = 1
    call('MUST_FAIL_KEY_MAP_EXTRA_KEY', T4.key_map_codes, m, cbm, ['KEY_MAP_SCHEMA'])

    # ---- 2. NEW items
    d_raw = Path(DISCLOSURES[0]).read_bytes()
    res['disclosures_sha256'] = sha_b(d_raw)
    c08 = [r['new_item_id'] for r in C.strict_json_bytes(d_raw)['c08_table']]
    res['c08_ids'] = c08
    files = {'r13': B / 'NEW_ITEM_DISPOSITIONS_V007.json', 'r14': B / 'NEW_ITEM_DISPOSITIONS_V007_R14_VARIANT.json'}
    objs = {}
    for v, p in files.items():
        o = C.strict_json(p)
        objs[v] = o
        ids = [x['id'] for x in o['items']]
        res['file2_%s' % v] = {'sha256': sha(p), 'n_items': len(ids), 'ids': ids, 'missing_from_c08': [x for x in c08 if x not in ids],
                               'not_in_c08': [x for x in ids if x not in c08], 'in_c08_order': ids == [x for x in c08 if x in ids],
                               'dispositions': sorted({x['disposition'] for x in o['items']}), 'compare_impl': o['compare_impl'],
                               'impl_names_r13_sha': sha(CMP['r13']) in Path(o['compare_impl']['path']).read_text(encoding='utf-8'),
                               'impl_names_r14_sha': sha(CMP['r14']) in Path(o['compare_impl']['path']).read_text(encoding='utf-8'),
                               'impl_declares_a_NEW_id': bool(re.search(r'NEW-[0-9]+', Path(o['compare_impl']['path']).read_text(encoding='utf-8')))}
    same = [(a['id'], a['disposition'], a['must_fail_tests']) for a in objs['r13']['items']] == \
           [(a['id'], a['disposition'], a['must_fail_tests']) for a in objs['r14']['items']]
    res['r13_and_r14_items_same_ids_dispositions_tests'] = same
    res['r13_and_r14_reasons_identical'] = [a['reason'] for a in objs['r13']['items']] == [a['reason'] for a in objs['r14']['items']]
    call('NEW_ITEMS_R13_FILE_VS_R13_SHA', T4.new_items_codes, objs['r13'], sha(CMP['r13']), [])
    call('NEW_ITEMS_R14_VARIANT_VS_R14_SHA', T4.new_items_codes, objs['r14'], sha(CMP['r14']), [])
    call('MUST_FAIL_NEW_ITEMS_R13_FILE_VS_R14_SLOT', T4.new_items_codes, objs['r13'], sha(CMP['r14']), ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'])
    m = copy.deepcopy(objs['r14']); m['items'][3]['must_fail_tests'] = []
    call('MUST_FAIL_NEW_ITEMS_ADOPTED_WITHOUT_TEST', T4.new_items_codes, m, sha(CMP['r14']), ['NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL'])
    m = copy.deepcopy(objs['r14']); m['items'].append(copy.deepcopy(m['items'][0]))
    call('MUST_FAIL_NEW_ITEMS_DUPLICATE_ID', T4.new_items_codes, m, sha(CMP['r14']), ['NEW_ITEMS_DUPLICATE_ID'])
    m = copy.deepcopy(objs['r14']); m['items'][0]['disposition'] = 'ACCEPTED'
    call('MUST_FAIL_NEW_ITEMS_BAD_DISPOSITION_WORD', T4.new_items_codes, m, sha(CMP['r14']), ['NEW_ITEMS_ENTRY'])
    m = copy.deepcopy(objs['r14']); m['items'].append({'id': 'NEW-999', 'disposition': 'REJECTED', 'reason': 'invented', 'must_fail_tests': []})
    call('ACCEPTED_BY_TOOL4_AN_ID_OUTSIDE_C08', T4.new_items_codes, m, sha(CMP['r14']), [])
    m = copy.deepcopy(objs['r14']); m['items'] = []
    call('ACCEPTED_BY_TOOL4_AN_EMPTY_ITEM_LIST', T4.new_items_codes, m, sha(CMP['r14']), [])
    # A118 completion path in memory (generator build(); no file written)
    v6_raw = Path(V006).read_bytes()
    v6 = v6_raw.decode('utf-8').split('\n')
    a118 = [l for l in v6 if l.startswith('- **NEW-30: ADOPTED.**') or l.startswith('- **NEW-44: ADOPTED as implemented.')]
    res['v006_sha256'] = sha_b(v6_raw)
    res['v006_a118_lines'] = a118
    gen_path = B / 'tools' / 'make_new_items_c4v001.py'
    res['generator_sha256'] = sha(gen_path)
    G = load('make_new_items_c4v001', gen_path)
    ref = 'V006 A118 (ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md, sha256 %s): %s' % (res['v006_sha256'], ' '.join(a118))
    comp = {}
    for v in ('r14', 'r13'):
        try:
            obj, text, summary, pending, c08g = G.build(v, '2026-10-19T00:00:00Z', {'NEW-30': 'ADOPTED', 'NEW-44': 'ADOPTED'}, ref, True)
            ids = [x['id'] for x in obj['items']]
            comp[v] = {'ok': True, 'n_items': len(ids), 'ids_equal_c08_in_order': ids == c08, 'pending': pending,
                       'text_sha256_in_memory': sha_b(text.encode('utf-8')),
                       'NEW-30': next(x for x in obj['items'] if x['id'] == 'NEW-30'),
                       'NEW-44': next(x for x in obj['items'] if x['id'] == 'NEW-44')}
            call('COMPLETION_A118_%s_VS_%s_SHA' % (v.upper(), v.upper()), T4.new_items_codes, obj, sha(CMP[v]), [])
        except Exception as e:
            comp[v] = {'ok': False, 'error': '%s: %s' % (type(e).__name__, str(e)[:300])}
    res['completion_a118'] = comp
    try:
        G.build('r14', '2026-10-19T00:00:00Z', {}, None, True)
        res['require_complete_without_rulings'] = 'NO_REFUSAL'
    except G.Refuse as e:
        res['require_complete_without_rulings'] = 'REFUSED: %s' % str(e)[:200]

    # ---- 3. custody (synthetic control from this folder's refute fixture)
    conv_path = B / 'tools' / 'make_custody_record_c4v001.py'
    res['converter_sha256'] = sha(conv_path)
    CV = load('make_custody_record_c4v001', conv_path)
    rp, recp = FIX / 'Z2_REPORT_SYNTHETIC.json', FIX / 'B1_RECORD_SYNTHETIC.json'
    argv2 = ['--report', str(rp), '--report-sha256', sha(rp), '--identity-record', str(recp), '--identity-record-sha256', sha(recp),
             '--driver-sha256', R5, '--out', str(FIX / 'CUSTODY_WOULD_BE_VALIDATION.json'), '--dry-run']
    so, se = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se):
        rc = CV.main(argv2)
    res['converter_control_dry_run'] = {'rc': rc, 'stderr_last': se.getvalue().strip().splitlines()[-1]}
    cust = json.loads(so.getvalue())
    res['converter_control_record_counts'] = [cust['stages_total'], cust['stages_successor']]
    res['converter_control_evidence'] = cust['evidence']
    call('CUSTODY_SYNTHETIC_CONTROL_VS_DRIVER_SLOT', T4.custody_codes, cust, R5, [])
    m = copy.deepcopy(cust)
    call('MUST_FAIL_CUSTODY_R4_SLOT', T4.custody_codes, m, R4, ['CUSTODY_DRIVER_NOT_THE_SLOT'])
    m = copy.deepcopy(cust); m['stages_successor'] = m['stages_total'] - 1
    call('MUST_FAIL_CUSTODY_STAGE_WITHOUT_SUCCESSOR', T4.custody_codes, m, R5, ['CUSTODY_STAGES'])
    m = copy.deepcopy(cust); m['stages_total'] = True; m['stages_successor'] = True
    call('MUST_FAIL_CUSTODY_BOOL_COUNTS', T4.custody_codes, m, R5, ['CUSTODY_STAGES'])
    m = copy.deepcopy(cust); m['identity_run'] = 'Z2_OFF_RO1'
    call('MUST_FAIL_CUSTODY_NOT_Z2', T4.custody_codes, m, R5, ['CUSTODY_RUN'])
    m = copy.deepcopy(cust); m['evidence'][0] = dict(m['evidence'][0], sha256='0' * 64)
    call('MUST_FAIL_CUSTODY_EVIDENCE_PIN', T4.custody_codes, m, R5, ['PIN_BYTES_MISMATCH'])
    res['n_calls'] = len(res['calls'])
    res['n_ok'] = sum(1 for c in res['calls'] if c['ok'])
    with open(outp, 'x', encoding='utf-8') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True, ensure_ascii=False) + '\n')
    print(json.dumps({'n_calls': res['n_calls'], 'n_ok': res['n_ok'], 'out': str(outp), 'sha256': sha(outp)}, sort_keys=True))
    return 0 if res['n_ok'] == res['n_calls'] else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
