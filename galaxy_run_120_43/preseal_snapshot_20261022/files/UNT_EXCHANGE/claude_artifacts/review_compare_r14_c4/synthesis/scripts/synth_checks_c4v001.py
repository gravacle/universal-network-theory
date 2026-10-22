# Claude4 synthesis-stage checks for the compare r14 delta review of record (dispatch 0651, root entry A114 in V006).
# Run ONLY through tools/run_fenced_c4st2.py (fence_c4v002 c993d34c): no process, network or delete; writes only inside
# review_compare_r14_c4/. Synthetic inputs only (fixture producer files, synthetic I4 records and registries), written under
# synthesis/out/<RUN>/. Nothing here runs a driver, the production comparator CLI or a seal tool CLI. The r13 and r14 modules
# are compiled from their sha-verified bytes and their functions are called in-process on synthetic inputs; tool 4 is imported
# from its own folder (siblings verified from bytes) and only new_items_codes / manual_disclosures_form_codes are called.
# usage: python3 -I -B tools/run_fenced_c4st2.py synthesis/scripts/synth_checks_c4v001.py RUN_NAME
import difflib, hashlib, importlib.util, json, os, re, sys, time, traceback, types
from pathlib import Path

REVIEW = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_compare_r14_c4')
OUT = REVIEW / 'synthesis' / 'out' / sys.argv[1]
OUT.mkdir(parents=True, exist_ok=False)
FX = OUT / 'fixtures'
FX.mkdir()
GEN = OUT / 'gen'
GEN.mkdir()

R14D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14'
R13D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13'
R12D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r12'
ST4 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004'
RIN = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs'
C3SA = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3'
PRE = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
REG9 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json'
PINS = {   # every value pasted from shasum output of the bytes in this session (2026-10-19 03:41Z-03:50Z), re-verified below
    'r14_source': (R14D + '/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
    'r13_source': (R13D + '/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'),
    'sel_v001': (R14D + '/SELECTED_R14_CX1V001.json', 'dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533'),
    'sel_v002': (R14D + '/SELECTED_R14_CX1V002.json', '6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a'),
    'fields_v002': (R14D + '/FIELDS_R14_CX1V002.md', '2ce9f1c710bb16ad1224ab49ec0713dd4f3fd48a04d730c78cfc3ed0ffdb7fe4'),
    'fields_v001': (R14D + '/FIELDS_R14_CX1V001.md', 'a33b153b40e3a709cbbf095908007c737e90c3383e6a113d30c786732e800c83'),
    'impl_v001': (R14D + '/COMPARE_V007_IMPL_R14.md', '854cad0d269161bff1fc314cdb2801df000eeb0d94ea004ef659d62edfb44680'),
    'impl_v002': (R14D + '/COMPARE_V007_IMPL_R14_CX1V002.md', '2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9'),
    'validation': (R14D + '/VALIDATION_R14_CX1V001.json', '930ca7bc78e74134aeac46851a6bbf9481e78f9ce3862b77d370b716dd8380ec'),
    'harness_r14': (R14D + '/tests_kmax_tail_compare_c2v007_r14_cx1v001.py', '998e0c2eb7309fd2a2135bc27974b95899f2f3583116312ccb7476120a1555c6'),
    'harness_copy': (R14D + '/tests_kmax_tail_compare_c2v007_r13_cx3v001.py', 'b00e533adf3f62846f5fe4da3fb74bd73655a37c4065c438dcb37736c7c4d059'),
    'harness_r13': (R13D + '/tests_kmax_tail_compare_c2v007_r13_cx3v001.py', '71c7b516bca41a8b0779e5da39704a84d1188bdeeb8f3df4920f843faae7e5aa'),
    'source_delta': (R14D + '/SOURCE_DELTA_CX1V001.json', '56a95b7ef983608b89b5f4c30799fa9ea578eb69c7e01ccb31de96b8bf92ec51'),
    'hashes_v001': (R14D + '/HASHES_R14_CX1V001.json', '8b92153a0200953df2e4df8e1993cfcade58ddc4b6b5536439359a9119be5a8f'),
    'hashes_v002': (R14D + '/HASHES_R14_CX1V002.json', '46b811c188834d8a72293d60d6ed792c8130dc31a565d40ac8884713e8b4d317'),
    'build_progress': (R14D + '/BUILD_PROGRESS_CX1V001.json', 'd246fa90dd5032ae6f6801056d1763b498fa6aba5534346b0d379a7e0ace0d01'),
    'r13_impl': (R13D + '/COMPARE_V007_IMPL_R13.md', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3'),
    'r13_fields': (R13D + '/FIELDS_R13_CX3V001.md', '7b116b0103fdeb83d2cd358976e2c901be15313ad7f9ab8d159af6d9ee3bb365'),
    'r12_fields': (R12D + '/FIELDS_R12_CX3V002.md', '5cc95a06dbe91275cd891e9832a0b7709301ac076a1ce49a3a675d76ee1a967f'),
    'tool4': (ST4 + '/build_seal_record_c4v004.py', '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41'),
    'seal_common': (ST4 + '/seal_common_c4v003.py', '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21'),
    'tool2': (ST4 + '/check_sealed_compare_c4v003.py', 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1'),
    'tool3': (ST4 + '/check_slot_fill_c4v003.py', '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af'),
    'md_v002': (RIN + '/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3'),
    'md_v003_draft': (RIN + '/SEAL_MANUAL_DISCLOSURES_V003_DRAFT.json', '21968a07f50d6bf5dda9e64cfa61c7e3ec80bca9943c0f84956611ac99b8be3e'),
    'r6_selected': (PRE + '/r6/SELECTED_R6_C4V001.json', '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'),
    'r6_prereg_json': (PRE + '/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json', 'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9'),
    'case_block': (PRE + '/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
    'prestage_c3v020': (C3SA + '/ROOT_SEAL_STEPS_c3v020.sh', '36058df84bb2088970be442bc64445a4c6939b45df3e9cb3294cedef62c65ac0'),
    'prestage_sel_c3v009': (C3SA + '/SELECTED_SEAL_PRESTAGE_C3SA_c3v009.json', '9e10eae111ba322806195273e149831da60a99956e7e0e0f01f46711f0f62167'),
    # V006 moved during this synthesis: 63e7802f (03:41Z) -> 3d4cbe56 (03:58:53Z, A116 appended; the A114 section is unchanged)
    'v006': (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md', '3d4cbe565faa2711dd9e910e781090e2a2063ed9a31b77015d03e684bb8aadce'),
    'registry_v009': (REG9, '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8'),
}
PROTECTED_WORDS = ('runs_ext', 'uvt_', 'kmax_a2f10_c5h_run_v001', 'rotmod', 'vobs', 'massmodels', 'sparc', 'ngc3198', 'ngc_3198')
R = {'utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'python': sys.version, 'checks': [], 'info': {}}
FAILS = []


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    return sha_b(Path(p).read_bytes())


def rec(sec, name, ok, label='TESTED', **info):
    R['checks'].append(dict({'sec': sec, 'check': name, 'ok': bool(ok), 'label': label}, **info))
    if not ok:
        FAILS.append('%s/%s' % (sec, name))
    print('%-4s %s/%s %s' % ('OK' if ok else 'FAIL', sec, name, json.dumps(info, default=str)[:300]))


def section(fn):
    try:
        fn()
    except (Exception, SystemExit) as exc:      # Refused is a SystemExit subclass
        rec(fn.__name__, 'SECTION_RAISED', False, error='%s: %s' % (type(exc).__name__, exc), tb=traceback.format_exc()[-1500:])


def load_verified(key, name):
    """compile the module from its verified bytes (no bytecode cache is consulted) and exec it as module `name`."""
    p, h = PINS[key]
    b = Path(p).read_bytes()
    if sha_b(b) != h:
        raise SystemExit('STOP: %s differs from its pin' % key)
    m = types.ModuleType(name)
    m.__file__ = p
    sys.modules[name] = m
    exec(compile(b, p, 'exec'), m.__dict__)
    return m


# ------------------------------------------------------------------ S0 every pinned input from bytes (stop if any differs)
for k, (p, h) in PINS.items():
    got = sha_f(p)
    rec('S0_pins', k, got == h, path=p, got=got)
if FAILS:
    (OUT / 'SYNTH_CHECKS_C4.json').write_text(json.dumps(R, indent=1, default=str) + '\n')
    sys.stderr.write('STOP: a pinned input differs from its sha\n')
    raise SystemExit(4)

B13 = Path(PINS['r13_source'][0]).read_bytes()
B14 = Path(PINS['r14_source'][0]).read_bytes()
L13 = B13.decode('utf-8').split('\n')
L14 = B14.decode('utf-8').split('\n')
TOKEN = 'PRODUCED_AFTER_THE_SEAL'
NINE = ('SRB_ROT', 'RB_FP', 'T2I', 'EA', 'MT', 'I1T', 'FLAG_RULINGS', 'HARMONICS', 'SR_K')


# ------------------------------------------------------------------ S1 byte / line delta and the consumers of the tuple
def S1_delta():
    old = b"GATE_RECORD_AFTER_SEAL_ALLOWED = ('SRB_ROT', 'RB_FP', 'T2I', 'EA', 'MT', 'I1T', 'FLAG_RULINGS', 'HARMONICS', 'SR_K')\n"
    new = old.replace(b"'SR_K')", b"'SR_K', 'I4')")
    rec('S1_delta', 'old_line_unique_in_r13_new_line_unique_in_r14', B13.count(old) == 1 and B14.count(new) == 1 and B14.count(old) == 0)
    rec('S1_delta', 'forward_step_on_r13_gives_r14_bytes', B13.replace(old, new) == B14, sha=sha_b(B13.replace(old, new)))
    inv = B14.replace(new, old)
    rec('S1_delta', 'exact_inverse_gives_r13_f5adfd11', sha_b(inv) == PINS['r13_source'][1], sha=sha_b(inv))
    rec('S1_delta', 'size_delta_plus_6_bytes', len(B14) - len(B13) == 6, r13=len(B13), r14=len(B14))
    ln13 = B13[:B13.index(old)].count(b'\n') + 1
    ln14 = B14[:B14.index(new)].count(b'\n') + 1
    rec('S1_delta', 'changed_line_is_L341_in_both', ln13 == 341 and ln14 == 341, ln13=ln13, ln14=ln14)
    rec('S1_delta', 'same_line_count_and_only_L341_differs', len(L13) == len(L14) and [i + 1 for i, (a, b) in enumerate(zip(L13, L14)) if a != b] == [341],
        lines=len(L13), cr=(b'\r' in B13, b'\r' in B14))
    sd = json.loads(Path(PINS['source_delta'][0]).read_bytes())
    ud = ''.join(difflib.unified_diff(B13.decode().splitlines(keepends=True), B14.decode().splitlines(keepends=True)))
    rec('S1_delta', 'SOURCE_DELTA_diff_equals_recomputed_unified_diff', sd['diff'] == ud and sd['exact_inverse_restores_parent'] is True,
        chars=len(ud))
    uses = [i + 1 for i, s in enumerate(L14) if 'GATE_RECORD_AFTER_SEAL_ALLOWED' in s]
    rec('S1_delta', 'tuple_name_occurs_on_exactly_L332_L341_L1106_L1122_L1126_L1184_L5172', uses == [332, 341, 1106, 1122, 1126, 1184, 5172],
        uses=uses, texts={u: L14[u - 1].strip()[:150] for u in uses})
    rec('S1_delta', 'no_indirect_reference_to_the_tuple_name', B14.count(b'AFTER_SEAL_ALLOWED') == 7, n=B14.count(b'AFTER_SEAL_ALLOWED'))
    rec('S1_delta', 'stale_comment_L332_334_still_lists_I4_as_by_record_sha', 'the B-gates, I4) is registered by record sha' in L14[333],
        l334=L14[333].strip())
    rec('S1_delta', 'L1125_and_L1178_cite_A88_not_A114', 'A88' in L14[1124] and 'A114' not in B14.decode(), l1125=L14[1124].strip()[-90:],
        l1178=L14[1177].strip()[-90:])


section(S1_delta)

M14 = load_verified('r14_source', 'c4synth_r14')
M13 = load_verified('r13_source', 'c4synth_r13')


def reg_obj(M, gate_records, producers=None, **extra):
    o = {'schema': M.PRODUCER_REGISTRY_SCHEMA, 'producers': producers or {}, 'identity_comparators': [], 'identity_tokens': {},
         'gate_records': gate_records, 'gq_all_nodes_counts': {}}
    o.update(extra)
    return o


def try_load(M, obj):
    try:
        return 'ACCEPT', M.producer_registry_from_obj(obj)
    except M.Refused as e:
        return e.refusal_code, None
    except Exception as e:
        return 'EXC:%s' % type(e).__name__, None


def mkfile(name, text):
    p = FX / name
    p.write_text(text)
    return {'path': str(p), 'sha256': sha_f(p)}


P_I4 = mkfile('i4_producer_fixture_c4synth.py', '# synthetic I4 producer fixture (Claude4 synthesis; never executed)\n')
P_OTHER = mkfile('other_producer_fixture_c4synth.py', '# synthetic unregistered producer fixture (Claude4 synthesis)\n')
P_N1SPEC = mkfile('n1_spec_fixture_c4synth.json', '{"synthetic": "C2T N1 spec stand-in", "route_a": {"column_workers": 1}}\n')
DRV = 'd' * 64


# ------------------------------------------------------------------ S2 loader / sha-codes sweeps over ALL_GATES, and the 12 MUSTs
def S2_token_sweep():
    rec('S2_token', 'tuples', M13.GATE_RECORD_AFTER_SEAL_ALLOWED == NINE and M14.GATE_RECORD_AFTER_SEAL_ALLOWED == NINE + ('I4',),
        r13=M13.GATE_RECORD_AFTER_SEAL_ALLOWED, r14=M14.GATE_RECORD_AFTER_SEAL_ALLOWED)
    rec('S2_token', 'ALL_GATES_25_and_equal', M13.ALL_GATES == M14.ALL_GATES and len(M14.ALL_GATES) == 25, n=len(M14.ALL_GATES))
    res = {}
    for lab, M in (('r13', M13), ('r14', M14)):
        res[lab] = {g: try_load(M, reg_obj(M, {g: TOKEN}))[0] for g in M.ALL_GATES}
    acc13 = {g for g, v in res['r13'].items() if v == 'ACCEPT'}
    acc14 = {g for g, v in res['r14'].items() if v == 'ACCEPT'}
    R['info']['loader_sweep'] = res
    rec('S2_token', 'loader_r13_accepts_exactly_the_nine', acc13 == set(NINE), acc=sorted(acc13))
    rec('S2_token', 'loader_r14_accepts_exactly_the_nine_plus_I4', acc14 == set(NINE) | {'I4'}, acc=sorted(acc14))
    rec('S2_token', 'loader_every_refusal_is_PRODUCER_REGISTRY_GATE_RECORDS',
        all(v in ('ACCEPT', 'PRODUCER_REGISTRY_GATE_RECORDS') for d in res.values() for v in d.values()))
    named = ('B0', 'B1', 'B2', 'B3', 'EPS', 'GQ', 'LO', 'LO_NGC', 'DOUBLING') + tuple(M14.IDENTITY_GATES)
    rec('S2_token', 'r14_refuses_every_gate_A114_names', all(res['r14'][g] == 'PRODUCER_REGISTRY_GATE_RECORDS' for g in named), named=named)
    bfam = ('B0prime_DRY', 'B0_FA', 'B0_RO1', 'B0_N3')
    rec('S2_token', 'r14_refuses_the_B0_family_A114_list_does_not_name', all(res['r14'][g] == 'PRODUCER_REGISTRY_GATE_RECORDS' for g in bfam))
    # gate_record_sha_codes on a hand-built registry that bypasses the loader
    sc = {}
    for lab, M in (('r13', M13), ('r14', M14)):
        sc[lab] = {g: M.gate_record_sha_codes(g, 'a' * 64, {'gate_records': {g: TOKEN}}) for g in M.ALL_GATES}
    R['info']['sha_codes_sweep'] = sc
    diff = sorted(g for g in M14.ALL_GATES if sc['r13'][g] != sc['r14'][g])
    rec('S2_token', 'gate_record_sha_codes_differs_only_on_I4', diff == ['I4'] and sc['r14']['I4'] == []
        and sc['r13']['I4'] == ['GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4'], diff=diff)
    rec('S2_token', 'gate_record_sha_codes_r14_refuses_all_15_outside_the_ten',
        all(sc['r14'][g] == ['GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:%s' % g] for g in M14.ALL_GATES if g not in acc14))
    # the 12 A114 MUST assertions, replicated (isolated base) on both rounds
    must = {}
    for lab, M in (('r13', M13), ('r14', M14)):
        tk = {g: res[lab][g] == 'ACCEPT' for g in M.ALL_GATES}
        rows = [('A114_MUST_I4_TOKEN_ACCEPTED', tk['I4'] is True)]
        for g in sorted(set(('B0', 'B1', 'B2', 'B3', 'EPS', 'GQ', 'LO', 'LO_NGC', 'DOUBLING') + M.IDENTITY_GATES)):
            rows.append(('A114_MUST_TOKEN_REFUSED_' + g, tk[g] is False))
        must[lab] = rows
    R['info']['must_replica'] = must
    rec('S2_token', 'MUST_replica_r14_12_of_12', len(must['r14']) == 12 and all(ok for _, ok in must['r14']))
    rec('S2_token', 'MUST_replica_r13_11_of_12_failing_only_I4_accepted',
        [n for n, ok in must['r13'] if not ok] == ['A114_MUST_I4_TOKEN_ACCEPTED'] and len(must['r13']) == 12)
    # the file route
    for lab, M in (('r13', M13), ('r14', M14)):
        for g in ('I4', 'EPS'):
            p = FX / ('reg_token_%s_%s.json' % (g, lab))
            p.write_text(json.dumps(reg_obj(M, {g: TOKEN})))
            try:
                M.load_producer_registry(str(p))
                code = 'ACCEPT'
            except M.Refused as e:
                code = e.refusal_code
            res.setdefault('file_' + lab, {})[g] = code
    rec('S2_token', 'file_route_r14_I4_accept_EPS_refuse_r13_both_refuse',
        res['file_r14'] == {'I4': 'ACCEPT', 'EPS': 'PRODUCER_REGISTRY_GATE_RECORDS'}
        and res['file_r13'] == {'I4': 'PRODUCER_REGISTRY_GATE_RECORDS', 'EPS': 'PRODUCER_REGISTRY_GATE_RECORDS'},
        r14=res['file_r14'], r13=res['file_r13'])


section(S2_token_sweep)


def i4_record(M, **over):
    r = {'schema': M.GATE_SCHEMA, 'gate': 'I4', 'producer': dict(P_I4), 'verdict': M.I4_PASS_VERDICT, 'tail': 'ON',
         'driver_sha256': DRV, 'serial_result_sha256': 'a' * 64, 'parallel_result_sha256': 'b' * 64,
         'v8c_f1_fix_confirmed': True, 'bitwise_equal': True, 'differences_outside_custody': []}
    for k, v in over.items():
        if v is None:
            r.pop(k, None)
        else:
            r[k] = v
    return r


def wrec(name, obj=None, raw=None):
    p = FX / name
    p.write_bytes(raw if raw is not None else (json.dumps(obj, indent=1) + '\n').encode())
    return str(p)


def ctx_for(M, reg):
    return {'producer_registry': reg, 'case_block': {'cases': {c: {'drivers_allowed': [DRV]} for c in M.T_CASES}}}


def ev(M, path, ctx, runs_sha=None):
    o = M.evaluate_gate('I4', path, ctx, runs_sha)
    return {'status': o['status'], 'codes': o['codes'], 'crossref': o['crossref']}


# ------------------------------------------------------------------ S3 evaluate_gate on synthetic I4 records (r14 token; r13 contrast)
def S3_i4_semantics():
    code, reg_tok = try_load(M14, reg_obj(M14, {'I4': TOKEN}, producers={'I4': [dict(P_I4)]}))
    rec('S3_i4', 'r14_loads_token_registry_with_a_registered_I4_producer', code == 'ACCEPT', code=code)
    ctx = ctx_for(M14, reg_tok)
    e = {}
    e['E01_no_path'] = ev(M14, None, ctx)
    e['E02_path_not_yet_written'] = ev(M14, str(FX / 'I4_not_written_yet.json'), ctx)
    good = wrec('I4_good.json', i4_record(M14))
    e['E03_valid_record'] = ev(M14, good, ctx)
    e['E04_parallel_sha_not_C2T'] = ev(M14, wrec('I4_par_not_c2t.json', i4_record(M14, parallel_result_sha256='9' * 64)), ctx, {'C2T': 'e' * 64})
    e['E05_serial_equals_parallel'] = ev(M14, wrec('I4_ser_eq_par.json', i4_record(M14, serial_result_sha256='c' * 64, parallel_result_sha256='c' * 64)), ctx)
    e['E06_empty_file'] = ev(M14, wrec('I4_empty.json', raw=b''), ctx)
    e['E07_placeholder_pending'] = ev(M14, wrec('I4_placeholder.json', i4_record(M14, verdict='PENDING', bitwise_equal=None)), ctx)
    e['E08_unregistered_producer'] = ev(M14, wrec('I4_unreg_prod.json', i4_record(M14, producer=dict(P_OTHER))), ctx)
    e['E09_failing_record_FAIL_verdict'] = ev(M14, wrec('I4_fail.json', i4_record(M14, bitwise_equal=False, verdict='FAIL')), ctx)
    e['E10_PASS_verdict_over_failing_data'] = ev(M14, wrec('I4_pass_bad.json', i4_record(M14, bitwise_equal=False)), ctx)
    e['E11_tail_off'] = ev(M14, wrec('I4_tail_off.json', i4_record(M14, tail='OFF')), ctx)
    e['E12_driver_not_registered'] = ev(M14, wrec('I4_drv.json', i4_record(M14, driver_sha256='e' * 64)), ctx)
    code_l, reg_list_other = try_load(M14, reg_obj(M14, {'I4': ['f' * 64]}, producers={'I4': [dict(P_I4)]}))
    e['E13_sha_list_naming_another_sha'] = ev(M14, good, ctx_for(M14, reg_list_other))
    code_s, reg_list_own = try_load(M14, reg_obj(M14, {'I4': [sha_f(good)]}, producers={'I4': [dict(P_I4)]}))
    e['E14_sha_list_naming_its_own_sha'] = ev(M14, good, ctx_for(M14, reg_list_own))
    e['E15_r13_hand_built_token_registry'] = ev(M13, good, ctx_for(M13, reg_tok))
    code13, _ = try_load(M13, reg_obj(M13, {'I4': TOKEN}, producers={'I4': [dict(P_I4)]}))
    R['info']['i4_cases'] = e
    rec('S3_i4', 'E01_E02_absent_record_reads_MISSING', all(e[k]['status'] == 'MISSING' and e[k]['codes'] == ['GATE_RECORD_MISSING:I4']
                                                            for k in ('E01_no_path', 'E02_path_not_yet_written')))
    rec('S3_i4', 'E03_valid_record_under_token_reads_PASS', e['E03_valid_record']['status'] == 'PASS' and e['E03_valid_record']['codes'] == [])
    rec('S3_i4', 'E04_parallel_sha_not_the_C2T_result_still_PASS_no_crossref (S1)',
        e['E04_parallel_sha_not_C2T']['status'] == 'PASS' and e['E04_parallel_sha_not_C2T']['crossref'] == {})
    rec('S3_i4', 'E05_serial_equals_parallel_still_PASS (S1)', e['E05_serial_equals_parallel']['status'] == 'PASS')
    rec('S3_i4', 'E06_empty_file_RECORD_DEFECT_unreadable (N3)', e['E06_empty_file']['status'] == 'RECORD_DEFECT'
        and e['E06_empty_file']['codes'][:1] == ['GATE_RECORD_UNREADABLE:I4:JSONDecodeError'], codes=e['E06_empty_file']['codes'])
    rec('S3_i4', 'E07_placeholder_RECORD_DEFECT_field_missing (N3)', e['E07_placeholder_pending']['status'] == 'RECORD_DEFECT'
        and any('bitwise_equal' in c for c in e['E07_placeholder_pending']['codes']), codes=e['E07_placeholder_pending']['codes'])
    rec('S3_i4', 'E08_token_does_not_bypass_producer_pin', e['E08_unregistered_producer']['status'] == 'RECORD_DEFECT'
        and 'PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4' in e['E08_unregistered_producer']['codes'])
    rec('S3_i4', 'E09_failing_data_reads_FAIL', e['E09_failing_record_FAIL_verdict']['status'] == 'FAIL'
        and 'I4_SERIAL_PARALLEL_NOT_BITWISE_EQUAL' in e['E09_failing_record_FAIL_verdict']['codes'])
    rec('S3_i4', 'E10_PASS_over_failing_data_RECORD_DEFECT', e['E10_PASS_verdict_over_failing_data']['status'] == 'RECORD_DEFECT'
        and 'VERDICT_PASS_CONTRADICTS_DATA:I4' in e['E10_PASS_verdict_over_failing_data']['codes'])
    rec('S3_i4', 'E11_E12_tail_and_driver_clauses_enforced', 'I4_TAIL_NOT_ON' in e['E11_tail_off']['codes']
        and 'I4_DRIVER_NOT_REGISTERED_FOR_EVERY_T_CASE' in e['E12_driver_not_registered']['codes'])
    rec('S3_i4', 'E13_E14_token_waives_record_sha_list_binds_it', code_l == 'ACCEPT' and code_s == 'ACCEPT'
        and e['E13_sha_list_naming_another_sha']['status'] == 'RECORD_DEFECT'
        and 'GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4' in e['E13_sha_list_naming_another_sha']['codes']
        and e['E14_sha_list_naming_its_own_sha']['status'] == 'PASS')
    rec('S3_i4', 'E15_r13_fails_closed_on_hand_built_token_and_its_loader_refuses', code13 == 'PRODUCER_REGISTRY_GATE_RECORDS'
        and e['E15_r13_hand_built_token_registry']['status'] == 'RECORD_DEFECT'
        and 'GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4' in e['E15_r13_hand_built_token_registry']['codes'])
    # A114.3 / 0651: 'the N1 spec sha in V010's I4 entry' against the C2V003 registry schema (S2)
    s = {}
    s['extra_key_in_producer_pin'] = try_load(M14, reg_obj(M14, {'I4': TOKEN}, producers={'I4': [dict(P_I4, n1_spec_sha256=P_N1SPEC['sha256'])]}))[0]
    s['top_level_n1_key'] = try_load(M14, reg_obj(M14, {'I4': TOKEN}, producers={'I4': [dict(P_I4)]}, n1_spec_sha256=P_N1SPEC['sha256']))[0]
    s['note_carries_it'] = try_load(M14, reg_obj(M14, {'I4': TOKEN}, producers={'I4': [dict(P_I4)]}, note='I4 N1 spec sha256 ' + P_N1SPEC['sha256']))[0]
    s['gate_records_I4_as_dict'] = try_load(M14, reg_obj(M14, {'I4': {'token': TOKEN, 'n1_spec_sha256': P_N1SPEC['sha256']}}, producers={'I4': [dict(P_I4)]}))[0]
    code2, reg_two = try_load(M14, reg_obj(M14, {'I4': TOKEN}, producers={'I4': [dict(P_I4), dict(P_N1SPEC)]}))
    s['n1_spec_file_as_second_I4_producer_pin'] = code2
    s['two_pin_registry_genuine_record'] = ev(M14, good, ctx_for(M14, reg_two))['status'] if reg_two else None
    s['two_pin_registry_record_naming_the_spec_file'] = ev(M14, wrec('I4_prod_is_spec.json', i4_record(M14, producer=dict(P_N1SPEC))), ctx_for(M14, reg_two))['status'] if reg_two else None
    R['info']['n1_spec_schema'] = s
    rec('S3_i4', 'S2_extra_key_in_pin_refused_PRODUCER_REGISTRY_PRODUCERS', s['extra_key_in_producer_pin'] == 'PRODUCER_REGISTRY_PRODUCERS', got=s)
    rec('S3_i4', 'S2_top_level_key_refused_UNKNOWN_KEYS_and_dict_token_refused', s['top_level_n1_key'] == 'PRODUCER_REGISTRY_UNKNOWN_KEYS'
        and s['gate_records_I4_as_dict'] == 'PRODUCER_REGISTRY_GATE_RECORDS')
    rec('S3_i4', 'S2_note_accepts_it_and_second_file_pin_accepted', s['note_carries_it'] == 'ACCEPT' and code2 == 'ACCEPT'
        and s['two_pin_registry_genuine_record'] == 'PASS', two_pin_spec_as_producer=s['two_pin_registry_record_naming_the_spec_file'])
    g = [i + 1 for i, t in enumerate(L14) if t.startswith('def g_I4(')]
    body = '\n'.join(L14[g[0] - 1:g[0] + 18]) if g else ''
    rec('S3_i4', 'g_I4_at_L3741_makes_no_xr_call_and_reads_no_N1_field', g == [3741] and 'xr(' not in body and 'n1' not in body.lower()
        and L13[3740:3759] == L14[3740:3759], g=g)
    rec('S3_i4', 'required_gates_parallel8_has_I4_serial_mode_not', all('I4' in M.required_gates('parallel8')
        and 'I4' not in M.required_gates('serial_with_exemption') for M in (M13, M14)))
    cb = json.loads(Path(PINS['case_block'][0]).read_bytes())
    vals = []

    def find(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'route_a_mode':
                    vals.append(v)
                find(v)
        elif isinstance(o, list):
            for v in o:
                find(v)
    find(cb)
    rec('S3_i4', 'case_block_76309ae3_route_a_mode_is_parallel8', vals == ['parallel8'], route_a_mode=vals)


section(S3_i4_semantics)


# ------------------------------------------------------------------ S4 FIELDS: regenerate both contracts; decompose FIELDS V002
def S4_fields():
    p13, p14 = GEN / 'FIELDS_REGEN_r13_c4synth.md', GEN / 'FIELDS_REGEN_r14_c4synth.md'
    M13.write_field_contract(str(p13))
    M14.write_field_contract(str(p14))
    g13, g14 = p13.read_bytes(), p14.read_bytes()
    rec('S4_fields', 'r13_regen_equals_r12_FIELDS_R12_CX3V002_5cc95a06', sha_b(g13) == PINS['r12_fields'][1], sha=sha_b(g13))
    rec('S4_fields', 'r14_regen_equals_FIELDS_R14_CX1V001_a33b153b', sha_b(g14) == PINS['fields_v001'][1], sha=sha_b(g14))
    a, b = g13.decode().split('\n'), g14.decode().split('\n')
    dl = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y]
    rec('S4_fields', 'regens_differ_only_on_L66_by_comma_I4', len(a) == len(b) and dl == [66] and b[65] == a[65].replace('SR_K;', 'SR_K, I4;'),
        dl=dl, r14_l66=b[65][:220] if len(b) > 65 else None)
    v2, v1 = Path(PINS['fields_v002'][0]).read_bytes(), Path(PINS['fields_v001'][0]).read_bytes()
    f13, f12 = Path(PINS['r13_fields'][0]).read_bytes(), Path(PINS['r12_fields'][0]).read_bytes()
    rec('S4_fields', 'V002_ends_with_V001_exactly_and_r13_FIELDS_ends_with_r12_FIELDS', v2.endswith(v1) and f13.endswith(f12))
    pre2 = v2[:len(v2) - len(v1)].decode().split('\n')
    pre13 = f13[:len(f13) - len(f12)].decode().split('\n')
    ops = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, pre13, pre2, autojunk=False).get_opcodes():
        if tag != 'equal':
            ops.append({'tag': tag, 'r13_lines': [i1 + 1, i2], 'v002_lines': [j1 + 1, j2],
                        'r13_text': [x[:160] for x in pre13[i1:i2]], 'v002_text': [x[:160] for x in pre2[j1:j2]]})
    R['info']['fields_v002_prefix_ops'] = ops
    removed = [x for o in ops for x in o['r13_text']]
    rec('S4_fields', 'V002_drops_r13_sha_block_and_replaces_follows_verbatim_line (N5)',
        any('follows verbatim' in x for x in removed) and any('f5adfd11' in x or 'SHA256' in x for x in removed)
        and any('## Current generated contract' in x for o in ops for x in o['v002_text']), n_ops=len(ops),
        removed_lines=len(removed))
    rec('S4_fields', 'V002_preamble_discloses_I4_by_sha_statements_superseded',
        'superseded only on token timing' in v2[:len(v2) - len(v1)].decode())


section(S4_fields)


# ------------------------------------------------------------------ S5 selections, IMPL binding, tool 4, pre-stage selection check
def S5_selection_tool4():
    s1 = json.loads(Path(PINS['sel_v001'][0]).read_bytes())
    s2 = json.loads(Path(PINS['sel_v002'][0]).read_bytes())
    dk = sorted(k for k in set(s1) | set(s2) if s1.get(k) != s2.get(k))
    rec('S5_sel', 'SELECTED_V002_differs_from_V001_only_in_implementation_note_supersedes_utc',
        dk == ['implementation', 'note', 'supersedes_selection', 'utc'], differing=dk)
    rec('S5_sel', 'SELECTED_V002_supersedes_V001_by_sha_and_pins_IMPL_V002',
        s2['supersedes_selection']['sha256'] == PINS['sel_v001'][1] and s2['implementation']['sha256'] == PINS['impl_v002'][1]
        and s1['implementation']['sha256'] == PINS['impl_v001'][1])
    i1, i2 = Path(PINS['impl_v001'][0]).read_bytes(), Path(PINS['impl_v002'][0]).read_bytes()
    full, pre8 = PINS['r14_source'][1], PINS['r14_source'][1][:8]
    rec('S5_sel', 'IMPL_V002_is_IMPL_V001_plus_appended_binding_section', i2.startswith(i1) and full in i2[len(i1):].decode(),
        appended_head=i2[len(i1):].decode()[:120])
    rec('S5_sel', 'IMPL_V001_has_neither_full_sha_nor_prefix8', full not in i1.decode() and pre8 not in i1.decode())
    sys.path.insert(0, ST4)
    s = importlib.util.spec_from_file_location('c4synth_tool4', PINS['tool4'][0])
    T4 = importlib.util.module_from_spec(s)
    if sha_f(PINS['tool4'][0]) != PINS['tool4'][1]:
        raise SystemExit('STOP: tool 4 bytes changed')
    s.loader.exec_module(T4)
    rec('S5_tool4', 'tool4_siblings_are_the_pinned_bytes', sha_f(T4.C.__file__) == PINS['seal_common'][1]
        and sha_f(T4.T2.__file__) == PINS['tool2'][1] and sha_f(T4.T3.__file__) == PINS['tool3'][1])
    out = {}
    for key in ('impl_v001', 'impl_v002', 'r13_impl', 'sel_v001'):
        chk = T4.C.Checker('c4synth_new_items')
        obj = {'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': {'path': PINS[key][0], 'sha256': PINS[key][1]}, 'items': [],
               'note': 'Claude4 synthesis synthetic NEW-item list'}
        T4.new_items_codes(chk, obj, full)
        out[key] = [f['code'] for f in chk.failures]
    R['info']['tool4_new_items'] = out
    rec('S5_tool4', 'F1_IMPL_V001_refused_NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE', out['impl_v001'] == ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'], got=out)
    rec('S5_tool4', 'F1_IMPL_V002_passes', out['impl_v002'] == [])
    rec('S5_tool4', 'r13_IMPL_refused_for_reviewed_r14', out['r13_impl'] == ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'])
    rec('S5_tool4', 'F6_substring_check_passes_a_non_IMPL_file_SELECTED_V001', out['sel_v001'] == [])
    # disclosures: tool 4's form check, E_R6_1 and the A114 row
    forms = {}
    for key in ('md_v002', 'md_v003_draft'):
        d = json.loads(Path(PINS[key][0]).read_bytes())
        chk = T4.C.Checker('c4synth_md_form')
        T4.manual_disclosures_form_codes(chk, d)
        forms[key] = [f['code'] for f in chk.failures]
    rec('S5_tool4', 'manual_disclosures_form_check_passes_V002_and_V003_DRAFT', forms == {'md_v002': [], 'md_v003_draft': []}, got=forms)
    r6 = json.loads(Path(PINS['r6_selected'][0]).read_bytes())
    d3 = json.loads(Path(PINS['md_v003_draft'][0]).read_bytes())
    rec('S5_tool4', 'F7_E_R6_1_equals_r6_basis_and_V003_DRAFT_text_and_names_r13_IMPL', T4.E_R6_1 == r6['basis']['erratum_E_R6_1']
        and d3['e_r6_1_text'] == T4.E_R6_1 and '274f7049' in T4.E_R6_1 and 'r14' not in T4.E_R6_1, sha=sha_b(T4.E_R6_1.encode()))
    a114 = [x for x in d3['root_disclosures'] if x.get('id') == 'A114_I4_AFTER_SEAL_R14']
    txt = a114[0]['text'] if a114 else ''
    rec('S5_tool4', 'F7_V003_DRAFT_A114_row_names_r14_SELECTED_V002_IMPL_V002_and_succession', len(a114) == 1 and full in txt
        and 'SELECTED_R14_CX1V002' in txt and PINS['impl_v002'][1] in txt and 'supersedes r13' in txt)
    rec('S5_tool4', 'V003_DRAFT_A114_row_silent_on_prereg_r6_compare_slot_rule_text (NOTE)', 'seal_slots' not in txt and 'slot' not in txt,
        label='TESTED')
    # the pre-stage's own SELECTED-record check (c3v020 L405-413), emulated byte for byte in logic: generic over the compare
    def sel_check(sel_path, cpath, csha):
        b = Path(sel_path).read_bytes()
        t = b.decode('utf-8')
        if not (cpath in t and csha in t):
            return 'SELECTION_DOES_NOT_NAME_THE_COMPARE'
        d = json.loads(b)
        if isinstance(d, dict) and isinstance(d.get('selected_source'), dict):
            s_ = d['selected_source']
            if not (s_.get('path') == cpath and s_.get('sha256') == csha):
                return 'SELECTED_SOURCE_DIFFERS'
        return 'PASS'
    pc = {k: sel_check(PINS[k][0], PINS['r14_source'][0], full) for k in ('sel_v001', 'sel_v002')}
    pc['sel_v002_vs_r13'] = sel_check(PINS['sel_v002'][0], PINS['r13_source'][0], PINS['r13_source'][1])
    rec('S5_prestage', 'prestage_selection_check_logic_passes_both_r14_selections_and_refuses_r13', pc == {
        'sel_v001': 'PASS', 'sel_v002': 'PASS', 'sel_v002_vs_r13': 'SELECTION_DOES_NOT_NAME_THE_COMPARE'}, got=pc)
    ps = Path(PINS['prestage_c3v020'][0]).read_bytes().decode().split('\n')
    hits = {n: ps[n - 1].strip()[:170] for n in (218, 222, 241, 271, 272, 365, 377)}
    rec('S5_prestage', 'F2_c3v020_r13_bindings_at_the_cited_lines', 'COMPARE_R13_SHA="f5adfd11' in ps[271]
        and 'must be r13 f5adfd11' in ps[364] and 'f5adfd11' not in ps[270] and 'SEAL_MANUAL_DISCLOSURES_V002.json' in ps[221]
        and 'PRODUCER_REGISTRY_C3V009.json' in ps[240] and 'impl_of_record_r13' in ps[376] and '274f7049' in ps[217],
        label='FORMAL', lines=hits)
    sel9 = json.loads(Path(PINS['prestage_sel_c3v009'][0]).read_bytes())
    rec('S5_prestage', 'c3v009_selects_c3v020_36058df8', PINS['prestage_c3v020'][1] in json.dumps(sel9))


section(S5_selection_tool4)


# ------------------------------------------------------------------ S6 C-08 rows against r13 / r14 bytes; c08 wording
def S6_c08():
    rx = re.compile(r'NEW-(\d+)(?!\d)')
    fl = {}
    for lab, LL in (('r13', L13), ('r14', L14)):
        m = {}
        for i, s in enumerate(LL):
            for g in rx.finditer(s):
                m.setdefault('NEW-' + g.group(1), i + 1)
        fl[lab] = m
    rec('S6_c08', 'first_line_maps_identical_19_ids', fl['r13'] == fl['r14'] and len(fl['r14']) == 19, n=len(fl['r14']))
    for key in ('md_v002', 'md_v003_draft'):
        d = json.loads(Path(PINS[key][0]).read_bytes())
        bad = []
        for r_ in d['c08_table']:
            nid, ln = r_['new_item_id'], r_['line']
            for lab, LL in (('r13', L13), ('r14', L14)):
                if not any(('NEW-' + g.group(1)) == nid for g in rx.finditer(LL[ln - 1])):
                    bad.append((nid, lab, ln))
            if fl['r14'].get(nid) != ln or L13[ln - 1] != L14[ln - 1]:
                bad.append((nid, 'first_or_identical', ln))
        ids = sorted(r_['new_item_id'] for r_ in d['c08_table'])
        keys = sorted({tuple(sorted(r_)) for r_ in d['c08_table']})
        rec('S6_c08', key + '_19_rows_each_on_its_id_first_line_in_r13_and_r14', bad == [] and ids == sorted(fl['r14']) and len(ids) == 19,
            bad=bad, files=sorted({r_['file'] for r_ in d['c08_table']}), keys=keys)
    d3 = json.loads(Path(PINS['md_v003_draft'][0]).read_bytes())
    br = sorted({g.group(0) for s in L14 for g in re.finditer(r'\[NEW-\d+\]', s)})
    rec('S6_c08', 'N10_only_NEW_52_ever_appears_bracketed_in_r14', br == ['[NEW-52]'] and 'carried as a [NEW-n] tag' in d3['c08_confirmation'],
        bracketed=br, first_bracketed=[i + 1 for i, s in enumerate(L14) if '[NEW-52]' in s][:1])
    rec('S6_c08', 'N9_V003_DRAFT_says_checked_at_about_0345Z', '~03:45Z' in d3['c08_confirmation'])


section(S6_c08)


# ------------------------------------------------------------------ S7 the real registry V009 under both loaders; a V010-like copy
def S7_registry():
    n13 = M13.load_producer_registry(PINS['registry_v009'][0], PINS['registry_v009'][1])
    n14 = M14.load_producer_registry(PINS['registry_v009'][0], PINS['registry_v009'][1])
    rec('S7_reg', 'V009_loads_identically_under_r13_and_r14', n13 == n14, n_producer_gates=len(n14['producers']),
        I4_gate_records=sorted(n14['gate_records'].get('I4', [])) if not isinstance(n14['gate_records'].get('I4'), str) else n14['gate_records']['I4'])
    o = json.loads(Path(PINS['registry_v009'][0]).read_bytes())
    o['gate_records']['I4'] = TOKEN
    p = FX / 'REGISTRY_V010_LIKE_I4_TOKEN_c4synth.json'
    p.write_text(json.dumps(o, indent=1) + '\n')
    got = {}
    for lab, M in (('r13', M13), ('r14', M14)):
        try:
            M.load_producer_registry(str(p))
            got[lab] = 'ACCEPT'
        except M.Refused as e:
            got[lab] = e.refusal_code
    rec('S7_reg', 'V010_like_copy_with_I4_token_accepted_by_r14_refused_by_r13', got == {'r14': 'ACCEPT', 'r13': 'PRODUCER_REGISTRY_GATE_RECORDS'}, got=got)


section(S7_registry)


# ------------------------------------------------------------------ S8 harness deltas (r13 -> r14; the misnamed v001 copy -> r14)
def S8_harness():
    a = Path(PINS['harness_r13'][0]).read_bytes().decode().split('\n')
    b = Path(PINS['harness_r14'][0]).read_bytes().decode().split('\n')
    c = Path(PINS['harness_copy'][0]).read_bytes().decode().split('\n')

    def ops(x, y):
        o = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes():
            if tag != 'equal':
                o.append({'tag': tag, 'old': [i1 + 1, i2], 'new': [j1 + 1, j2], 'new_text': [s[:140] for s in y[j1:j2]]})
        return o
    o1, o2 = ops(a, b), ops(c, b)
    R['info']['harness_r13_to_r14'] = o1
    R['info']['harness_copy_to_r14'] = o2
    newl = sorted(n for o in o1 for n in range(o['new'][0], o['new'][1] + 1))
    rec('S8_harness', 'r13_to_r14_hunks_are_L1_L52_L68_L4319_4321_L5210_5211', newl == [1, 52, 68, 4319, 4320, 4321, 5210, 5211],
        hunks=len(o1), new_lines=newl)
    rec('S8_harness', 'misnamed_copy_b00e533a_differs_from_r14_only_at_L5210_5211',
        sorted(n for o in o2 for n in range(o['new'][0], o['new'][1] + 1)) == [5210, 5211], ops=o2)
    def where(marker):
        return [i + 1 for i, s in enumerate(b) if marker in s]
    nine = where('R12_ADAPTED_A88_TOKEN_ACCEPTED_ONLY_ON_THE_NINE_POST_SEAL_GATES')
    rec('S8_harness', 'NINE_test_assertion_is_relative_to_the_module_set (N3)', len(nine) == 1
        and "all(tk[g0] == (g0 in M.GATE_RECORD_AFTER_SEAL_ALLOWED) for g0 in M.ALL_GATES)" in b[nine[0] - 1], line=nine)
    rwr = where("r2['gate_records'][g] = (cur if isinstance(cur, frozenset) else frozenset()) | {")
    rec('S8_harness', 'registry_with_records_replaces_a_token_by_a_sha_set (F4)', len(rwr) == 1, label='FORMAL', line=rwr,
        defline=where('def registry_with_records('))
    fx = where("(HERE / 'FIELDS_R14_CX1V001.md').read_bytes() == fp11.read_bytes()")
    rec('S8_harness', 'FIELDS_test_compares_regen_with_r14s_own_V001 (N6)', fx == [5211], line=fx)
    mu = where("t('A114_MUST_")
    rec('S8_harness', 'MUST_lines_L4319_L4321', mu == [4319, 4321], lines=mu)


section(S8_harness)


# ------------------------------------------------------------------ S9 every publication pin from bytes; pin graph; unpinned evidence
def S9_pins():
    pubs = ['sel_v001', 'sel_v002', 'hashes_v001', 'hashes_v002', 'validation', 'source_delta', 'build_progress']
    allp, bad, skipped, edges = 0, [], [], {}
    pubpath = {os.path.realpath(PINS[k][0]): k for k in pubs}

    def walk(o, acc):
        if isinstance(o, dict):
            if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
                acc.append(o)
            for v in o.values():
                walk(v, acc)
        elif isinstance(o, list):
            for v in o:
                walk(v, acc)
    for k in pubs:
        acc = []
        walk(json.loads(Path(PINS[k][0]).read_bytes()), acc)
        edges[k] = []
        for x in acc:
            allp += 1
            if any(w in x['path'].lower() for w in PROTECTED_WORDS):
                skipped.append(x['path'])
                continue
            try:
                b = Path(x['path']).read_bytes()
                ok = sha_b(b) == x['sha256'] and ('bytes' not in x or x['bytes'] == len(b))
            except OSError as exc:
                ok = False
            if not ok:
                bad.append((k, x['path']))
            rp = os.path.realpath(x['path'])
            if rp in pubpath:
                edges[k].append(pubpath[rp])
    rec('S9_pins', 'all_publication_pins_match_bytes', allp == 114 and bad == [] and skipped == [], n=allp, bad=bad, skipped=skipped)
    state, cyc = {}, []

    def dfs(n, stack):
        state[n] = 1
        for m in edges.get(n, []):
            if m == n or state.get(m) == 1:
                cyc.append(stack + [m])
            elif not state.get(m):
                dfs(m, stack + [m])
        state[n] = 2
    for k in pubs:
        if not state.get(k):
            dfs(k, [k])
    R['info']['pin_edges'] = edges
    rec('S9_pins', 'pin_graph_among_publication_files_acyclic', cyc == [], cycles=cyc)
    names = [x for k in ('hashes_v001', 'hashes_v002', 'validation', 'sel_v001', 'sel_v002') for x in [json.dumps(json.loads(Path(PINS[k][0]).read_bytes()))]]
    rec('S9_pins', 'N8_TEST_SUMMARY_json_not_pinned', not any('TEST_SUMMARY.json' in s for s in names))
    v = json.loads(Path(PINS['validation'][0]).read_bytes())
    rec('S9_pins', 'VALIDATION_claims_718_70_96_and_0_blocking', v['counts']['author'] == {'passed': 718, 'total': 718, 'inherited': 706, 'A114_MUST': 12}
        and v['counts']['real_record']['passed'] == 70 and v['counts']['mutation']['passed'] == 96 and v['blocking_findings'] == 0, label='TESTED')


section(S9_pins)


# ------------------------------------------------------------------ S10 root texts: A114 section bytes, chronology, prereg r6 slot rule
def S10_root():
    v6 = Path(PINS['v006'][0]).read_bytes().decode().split('\n')
    sec = ('\n'.join(v6[119:140]) + '\n').encode()
    rec('S10_root', 'A114_section_L120_140_hashes_21720e08_as_at_0335Z', sha_b(sec) == '21720e08ab96db7ce401d3cc67290c34f206a92b6ebdef9972cb20733c4becdb',
        sha=sha_b(sec), head=v6[119][:100])
    rec('S10_root', 'A114_header_stamp_0335Z_A115_A116_present', '03:35Z' in v6[119] and any(s.startswith('## A115') for s in v6)
        and any(s.startswith('## A116: r14 enters the compare slot') for s in v6))
    a116 = '\n'.join(v6[[i for i, s in enumerate(v6) if s.startswith('## A116')][0]:])
    rec('S10_root', 'A116_names_r14_f3f9ba7e_SELECTED_V002_6b650ece_IMPL_V002_2ba6d12e_and_E_R6_2', all(x in a116 for x in (
        'f3f9ba7e', '6b650ece', '2ba6d12e', 'E_R6_2', 'No prereg r7', 'c3v010', 'tool 3 does not check the compare slot value against the rule text')))
    bp = json.loads(Path(PINS['build_progress'][0]).read_bytes())
    rec('S10_root', 'N9_BUILD_PROGRESS_0315Z_cites_A114_stamped_0335Z', bp['authority'] == '0651/A114' and bp['utc'].startswith('2026-10-19T03:15:27'),
        utc=bp['utc'])
    pr = json.loads(Path(PINS['r6_prereg_json'][0]).read_bytes())
    cs = pr['seal_slots']['compare']
    rec('S10_root', 'prereg_r6_compare_slot_value_pending_rule_names_r13_and_general_clause',
        cs['value'] == 'PENDING_ROOT_AT_SEAL_ASSEMBLY' and cs['rule'].startswith('The final compare round is r13 cx3v001')
        and 'V007 seals on the final compare round whose delta reviews of record each report 0 blocking' in cs['rule']
        and 'on top of r13' in cs['rule'])
    prr = pr['seal_slots']['producer_registry']['rule']
    rec('S10_root', 'prereg_r6_producer_registry_rule_says_I4_records_once_built', 'B0_N3, B0_RO1 and I4 records once built' in prr)


section(S10_root)


# ------------------------------------------------------------------ S11 A116.4: does tool 3 compare the compare slot value with the rule text?
def S11_tool3_rule_text():
    if ST4 not in sys.path:
        sys.path.insert(0, ST4)
    s = importlib.util.spec_from_file_location('c4synth_tool3', PINS['tool3'][0])
    T3 = importlib.util.module_from_spec(s)
    if sha_f(PINS['tool3'][0]) != PINS['tool3'][1]:
        raise SystemExit('STOP: tool 3 bytes changed')
    s.loader.exec_module(T3)
    src = Path(PINS['tool3'][0]).read_bytes().decode()
    rec('S11_tool3', 'tool3_source_never_reads_a_rule_key', "'rule'" not in src and '"rule"' not in src, label='FORMAL')
    rec('S11_tool3', 'tool3_maps_prereg_compare_slot_to_compare_reviewed_source', T3.PREREG_SLOT_OF.get('compare') == 'compare_reviewed_source')
    import copy
    tor = json.loads(Path(PINS['r6_prereg_json'][0]).read_bytes())
    sp = copy.deepcopy(tor)
    sp['seal_slots']['compare']['value'] = {'path': PINS['r14_source'][0], 'sha256': PINS['r14_source'][1]}
    rec('S11_tool3', 'sealed_prereg_with_r14_value_and_r6_rule_text_equals_text_of_record_outside_values',
        T3.blank_slot_values(sp) == T3.blank_slot_values(tor))
    sp2 = copy.deepcopy(sp)
    sp2['seal_slots']['compare']['rule'] = sp2['seal_slots']['compare']['rule'].replace('r13 cx3v001', 'r14 cx1v001', 1)
    rec('S11_tool3', 'editing_the_rule_text_would_differ_from_the_text_of_record (SEALED_PREREG_TEXT_CHANGED)',
        T3.blank_slot_values(sp2) != T3.blank_slot_values(tor))


section(S11_tool3_rule_text)

R['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
R['n_checks'] = len(R['checks'])
R['n_ok'] = sum(1 for c in R['checks'] if c['ok'])
R['fails'] = FAILS
(OUT / 'SYNTH_CHECKS_C4.json').write_text(json.dumps(R, indent=1, default=str) + '\n')
print('SUMMARY %d/%d ok; fails=%s' % (R['n_ok'], R['n_checks'], FAILS))
raise SystemExit(0 if not FAILS else 1)
