# Claude4 lens_integration probe (dispatch 0651, A114; compare r14 delta review of record). Run ONLY through
# tools/run_fenced_c4st2.py (fence_c4v002 c993d34c): no process, no network, no delete, writes only inside this review folder.
# Synthetic inputs only: fixture producer files, a synthetic I4 gate record, synthetic seal slots / prereg / sealed-copy files,
# all written under out/<run>/ in this folder. Nothing here runs a driver, the production comparator or a seal tool's CLI; tool 2 and
# tool 4 functions are called in-process on the synthetic inputs, and the compare modules only on synthetic registry objects/records.
# usage: python3 -I -B tools/run_fenced_c4st2.py probe_integration_c4.py OUTDIR_NAME
import copy, difflib, hashlib, importlib.util, json, os, re, sys, time, traceback
from pathlib import Path

REVIEW = Path(__file__).resolve().parent
OUT = REVIEW / 'out' / sys.argv[1]
OUT.mkdir(parents=True, exist_ok=False)
FIX = OUT / 'fixtures'
FIX.mkdir()
SB = OUT / 'sandbox_synthetic'
SB.mkdir()

R14D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14'
R13D = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13'
ST4 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v004'
RIN = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/root_inputs'
CTRL = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2'
PINS = {   # every value pasted from shasum output of the bytes (this session), re-verified below before use
    'r14_source': (R14D + '/kmax_tail_compare_c2v007_r14_cx1v001.py', 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'),
    'r13_source': (R13D + '/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'),
    'r14_impl_v001': (R14D + '/COMPARE_V007_IMPL_R14.md', '854cad0d269161bff1fc314cdb2801df000eeb0d94ea004ef659d62edfb44680'),
    'r14_impl_v002': (R14D + '/COMPARE_V007_IMPL_R14_CX1V002.md', '2ba6d12ecc36ab444365348573b7f49a02a12a818dd15d67de35d77300fa17c9'),
    'r13_impl': (R13D + '/COMPARE_V007_IMPL_R13.md', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3'),
    'r14_selected_v001': (R14D + '/SELECTED_R14_CX1V001.json', 'dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533'),
    'r14_selected_v002': (R14D + '/SELECTED_R14_CX1V002.json', '6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a'),
    'r14_harness': (R14D + '/tests_kmax_tail_compare_c2v007_r14_cx1v001.py', '998e0c2eb7309fd2a2135bc27974b95899f2f3583116312ccb7476120a1555c6'),
    'r14_validation': (R14D + '/VALIDATION_R14_CX1V001.json', '930ca7bc78e74134aeac46851a6bbf9481e78f9ce3862b77d370b716dd8380ec'),
    'r14_source_delta': (R14D + '/SOURCE_DELTA_CX1V001.json', '56a95b7ef983608b89b5f4c30799fa9ea578eb69c7e01ccb31de96b8bf92ec51'),
    'r14_hashes_v001': (R14D + '/HASHES_R14_CX1V001.json', '8b92153a0200953df2e4df8e1993cfcade58ddc4b6b5536439359a9119be5a8f'),
    'r14_hashes_v002': (R14D + '/HASHES_R14_CX1V002.json', '46b811c188834d8a72293d60d6ed792c8130dc31a565d40ac8884713e8b4d317'),
    'r14_fields_v001': (R14D + '/FIELDS_R14_CX1V001.md', 'a33b153b40e3a709cbbf095908007c737e90c3383e6a113d30c786732e800c83'),
    'r14_fields_v002': (R14D + '/FIELDS_R14_CX1V002.md', '2ce9f1c710bb16ad1224ab49ec0713dd4f3fd48a04d730c78cfc3ed0ffdb7fe4'),
    'tool4': (ST4 + '/build_seal_record_c4v004.py', '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41'),
    'tool2': (ST4 + '/check_sealed_compare_c4v003.py', 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1'),
    'tool3': (ST4 + '/check_slot_fill_c4v003.py', '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af'),
    'tool1': (ST4 + '/check_frozen_addendum_c4v003.py', 'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4'),
    'seal_common': (ST4 + '/seal_common_c4v003.py', '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21'),
    'md_v001': (RIN + '/SEAL_MANUAL_DISCLOSURES_V001.json', 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6'),
    'md_v002': (RIN + '/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3'),
    'md_v003_draft': (RIN + '/SEAL_MANUAL_DISCLOSURES_V003_DRAFT.json', '21968a07f50d6bf5dda9e64cfa61c7e3ec80bca9943c0f84956611ac99b8be3e'),
    'r6_selected': ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json',
                    '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'),
    'v005_addendum_live': (CTRL + '/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md',
                           'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'),
}
R = {'utc_start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'python': sys.version, 'sections': {}}
FAILS = []


def sha_b(b):
    return hashlib.sha256(b).hexdigest()


def sha_f(p):
    return sha_b(Path(p).read_bytes())


def rec(sec, name, ok, **info):
    R['sections'].setdefault(sec, []).append(dict({'check': name, 'ok': bool(ok)}, **info))
    if not ok:
        FAILS.append('%s/%s' % (sec, name))
    print('%-4s %s/%s %s' % ('OK' if ok else 'FAIL', sec, name, json.dumps(info, default=str)[:400]))


def write_json(p, obj):
    Path(p).write_text(json.dumps(obj, indent=1, sort_keys=True) + '\n')
    return {'path': str(Path(p)), 'sha256': sha_f(p)}


def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ------------------------------------------------------------------ 0. every pinned input from bytes
for k, (p, h) in PINS.items():
    got = sha_f(p)
    rec('S0_pins', k, got == h, path=p, want=h, got=got)
if FAILS:
    Path(OUT / 'PROBE_RESULTS_C4.json').write_text(json.dumps(R, indent=1, default=str))
    sys.stderr.write('STOP: a pinned input differs from its sha\n')
    raise SystemExit(4)

# ------------------------------------------------------------------ 1. byte delta r13 -> r14 (independent of the author's SOURCE_DELTA)
b13 = Path(PINS['r13_source'][0]).read_bytes()
b14 = Path(PINS['r14_source'][0]).read_bytes()
L13 = b13.decode('utf-8').splitlines(keepends=True)
L14 = b14.decode('utf-8').splitlines(keepends=True)
diffs = [i for i, (a, b) in enumerate(zip(L13, L14)) if a != b]
rec('S1_delta', 'same_line_count', len(L13) == len(L14), r13=len(L13), r14=len(L14))
rec('S1_delta', 'exactly_one_line_differs_L341', diffs == [340], differing_lines_1based=[i + 1 for i in diffs])
if diffs == [340]:
    a, b = L13[340], L14[340]
    rec('S1_delta', 'the_line_is_the_allowed_set_plus_I4', a.rstrip('\n').replace("'SR_K')", "'SR_K', 'I4')") == b.rstrip('\n'),
        r13_line=a.rstrip('\n'), r14_line=b.rstrip('\n'))
    inv = ''.join(L14[:340] + [a] + L14[341:]).encode('utf-8')
    rec('S1_delta', 'exact_inverse_restores_r13_sha', sha_b(inv) == PINS['r13_source'][1], got=sha_b(inv))
    rec('S1_delta', 'byte_length_delta_is_6', len(b14) - len(b13) == 6, r13=len(b13), r14=len(b14))

# ------------------------------------------------------------------ 2. load both compare modules (as the author harness does)
try:
    M14 = load(PINS['r14_source'][0], 'c4probe_cmp_r14')
    M13 = load(PINS['r13_source'][0], 'c4probe_cmp_r13')
    rec('S2_load', 'both_modules_import_under_the_fence', True)
except Exception as e:
    rec('S2_load', 'both_modules_import_under_the_fence', False, exc='%s: %s' % (type(e).__name__, e), tb=traceback.format_exc()[-1500:])
    Path(OUT / 'PROBE_RESULTS_C4.json').write_text(json.dumps(R, indent=1, default=str))
    raise SystemExit(5)

# module-level constants: every public non-callable name equal between r13 and r14 except GATE_RECORD_AFTER_SEAL_ALLOWED
def consts(M):
    return {k: v for k, v in vars(M).items() if not (k.startswith('__') or callable(v) or type(v).__name__ == 'module')}


def same(a, b):
    """structural equality across the two module instances: functions/lambdas by qualname and code object (CPython code equality:
    bytecode, consts (nested code objects recursively), names, first line number), containers element-wise, else =="""
    if hasattr(a, '__code__') and hasattr(b, '__code__'):
        return a.__qualname__ == b.__qualname__ and a.__code__ == b.__code__
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(same(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if type(a).__name__ == 'ndarray':
        return a.shape == b.shape and bool((a == b).all())
    try:
        return bool(a == b)
    except Exception:
        return repr(a) == repr(b)
c13, c14 = consts(M13), consts(M14)
dk = sorted(k for k in set(c13) | set(c14) if k not in c13 or k not in c14 or not same(c13[k], c14[k]))
rec('S2_load', 'only_GATE_RECORD_AFTER_SEAL_ALLOWED_differs_among_module_constants', dk == ['GATE_RECORD_AFTER_SEAL_ALLOWED'], differing=dk,
    n_constants=len(c14))
rec('S2_load', 'r14_allowed_set', tuple(M14.GATE_RECORD_AFTER_SEAL_ALLOWED) == tuple(M13.GATE_RECORD_AFTER_SEAL_ALLOWED) + ('I4',),
    r13=M13.GATE_RECORD_AFTER_SEAL_ALLOWED, r14=M14.GATE_RECORD_AFTER_SEAL_ALLOWED)
rec('S2_load', 'GATE_RECORD_SHA_REQUIRED_empty_both', M13.GATE_RECORD_SHA_REQUIRED == () and M14.GATE_RECORD_SHA_REQUIRED == ())
rec('S2_load', 'I4_still_required_in_parallel8_only_both',
    all('I4' in M.required_gates('parallel8') and 'I4' not in M.required_gates('serial_with_exemption') for M in (M13, M14)))
rec('S2_load', 'route_a_mode_default_parallel8_both', M13.ROUTE_A_MODE_DEFAULT == M14.ROUTE_A_MODE_DEFAULT == 'parallel8')
_fn = lambda M, n: (getattr(M, n).__code__.co_code, getattr(M, n).__code__.co_consts, getattr(M, n).__code__.co_names)
_fnames = sorted(k for k, v in vars(M14).items() if callable(v) and getattr(v, '__module__', None) == M14.__name__ and hasattr(v, '__code__'))
_fdiff = [n for n in _fnames if not hasattr(M13, n) or _fn(M13, n) != _fn(M14, n)]
rec('S2_load', 'every_module_function_code_object_identical_r13_r14', _fdiff == [], n_functions=len(_fnames), differing=_fdiff)
rec('S2_load', 'I4_verdict_and_gate_func_unchanged', M13.I4_PASS_VERDICT == M14.I4_PASS_VERDICT and _fn(M13, 'g_I4') == _fn(M14, 'g_I4'),
    verdict=M14.I4_PASS_VERDICT)

# ------------------------------------------------------------------ 3. the 12 A114 MUST assertions (harness L4313-4321), own fixtures
def fixture(content):
    p = FIX / ('fx_' + sha_b(content.encode())[:16] + '.fixture')
    if not p.exists():
        p.write_text(content)
    return {'path': str(p), 'sha256': sha_b(content.encode())}

GQ_GEOMETRY = {'DDO_C2T': ('C2T_KB128', 1059379200), 'DDO_C3T': ('C3T_KB128', 1060288000), 'DDO_C4T': ('C4T_KB256', 4219494400)}


def reg_obj(M, token_gates):
    """the harness REG_OBJ shape in the C2V003 form (reg10): file pins for producers / comparators / tokens (fixtures written here)"""
    return {'schema': M.PRODUCER_REGISTRY_SCHEMA, 'producers': {g: [fixture(g)] for g in M.ALL_GATES},
            'identity_comparators': [fixture('comparator')], 'identity_tokens': {g: [fixture('tokens' + g)] for g in M.IDENTITY_GATES},
            'gate_records': {g: (M.GATE_RECORD_AFTER_SEAL if g in token_gates else []) for g in M.ALL_GATES},
            'gq_all_nodes_counts': {geo: n for geo, n in GQ_GEOMETRY.values()},
            'note': 'Claude4 lens_integration synthetic TEST registry; not a root registration'}


def raises(f, exc):
    try:
        f()
    except exc as e:
        return True, e
    return False, None


def tk_sweep(M, base_tokens):
    out = {}
    for g0 in M.ALL_GATES:
        o6 = reg_obj(M, base_tokens)
        o6['gate_records'][g0] = M.GATE_RECORD_AFTER_SEAL
        r_, e_ = raises(lambda: M.producer_registry_from_obj(o6), M.Refused)
        out[g0] = {'accepted': not r_, 'code': getattr(e_, 'refusal_code', None) if r_ else None}
    return out

MUST_REFUSED = sorted(set(('B0', 'B1', 'B2', 'B3', 'EPS', 'GQ', 'LO', 'LO_NGC', 'DOUBLING') + M14.IDENTITY_GATES))
rec('S3_must', 'must_list_is_1_plus_11', len(MUST_REFUSED) == 11, refused_gates=MUST_REFUSED)
sweeps = {}
for lab, M in (('r14', M14), ('r13', M13)):
    # faithful: the harness base (token on the module's own allowed set) then the token on g0
    tk = tk_sweep(M, M.GATE_RECORD_AFTER_SEAL_ALLOWED)
    # isolated: no token anywhere in the base, the token only on g0
    tki = tk_sweep(M, ())
    sweeps[lab] = {'faithful': tk, 'isolated': tki}
    must = [('A114_MUST_I4_TOKEN_ACCEPTED', tk['I4']['accepted'] is True)] + \
           [('A114_MUST_TOKEN_REFUSED_' + g, tk[g]['accepted'] is False) for g in MUST_REFUSED]
    R.setdefault('must_results', {})[lab] = must
    npass = sum(1 for _, ok in must if ok)
    if lab == 'r14':
        rec('S3_must', 'r14_all_12_MUST_pass', npass == 12, passed=npass, of=len(must), failing=[n for n, ok in must if not ok])
    else:
        rec('S3_must', 'r13_fails_exactly_the_I4_accepted_MUST', [n for n, ok in must if not ok] == ['A114_MUST_I4_TOKEN_ACCEPTED'],
            passed=npass, of=len(must), failing=[n for n, ok in must if not ok], i4_code=tk['I4']['code'])
    acc = sorted(g for g, v in tk.items() if v['accepted'])
    acci = sorted(g for g, v in tki.items() if v['accepted'])
    want = sorted(M.GATE_RECORD_AFTER_SEAL_ALLOWED)
    rec('S3_must', lab + '_faithful_accepts_exactly_its_allowed_set', acc == want, accepted=acc)
    rec('S3_must', lab + '_isolated_accepts_exactly_its_allowed_set', acci == want, accepted=acci)
    codes = sorted({v['code'] for v in tki.values() if not v['accepted']})
    rec('S3_must', lab + '_every_refusal_is_PRODUCER_REGISTRY_GATE_RECORDS', codes == ['PRODUCER_REGISTRY_GATE_RECORDS'], codes=codes)
rec('S3_must', 'r14_minus_r13_accepted_is_exactly_I4',
    sorted(set(g for g, v in sweeps['r14']['isolated'].items() if v['accepted']) - set(g for g, v in sweeps['r13']['isolated'].items() if v['accepted'])) == ['I4']
    and not (set(g for g, v in sweeps['r13']['isolated'].items() if v['accepted']) - set(g for g, v in sweeps['r14']['isolated'].items() if v['accepted'])))
# the author's own R12_ADAPTED test is self-referential (it compares with M's constant): it passes on BOTH modules
for lab, M in (('r14', M14), ('r13', M13)):
    tk = sweeps[lab]['faithful']
    selfref = all(tk[g]['accepted'] == (g in M.GATE_RECORD_AFTER_SEAL_ALLOWED) for g in M.ALL_GATES) and 'SR_K' in M.GATE_RECORD_AFTER_SEAL_ALLOWED \
        and 'EPS' not in M.GATE_RECORD_AFTER_SEAL_ALLOWED
    rec('S3_must', lab + '_author_R12_ADAPTED_selfreferential_test_passes', selfref)
# the token is refused on every B0-family gate too (B0prime_DRY, B0_FA, B0_RO1, B0_N3: not named by A114, refused all the same)
for g in ('B0prime_DRY', 'B0_FA', 'B0_RO1', 'B0_N3', 'B0prime_RERUN'):
    rec('S3_must', 'r14_token_refused_' + g, sweeps['r14']['isolated'][g]['accepted'] is False)
# the base registry the harness builds on r14 (token on all ten) loads; the same base on r13 is refused (it carries the I4 token)
o_base14 = reg_obj(M14, M14.GATE_RECORD_AFTER_SEAL_ALLOWED)
rec('S3_must', 'r14_harness_base_registry_loads', not raises(lambda: M14.producer_registry_from_obj(o_base14), M14.Refused)[0])
o_base14_on13 = reg_obj(M13, M14.GATE_RECORD_AFTER_SEAL_ALLOWED)
r_, e_ = raises(lambda: M13.producer_registry_from_obj(o_base14_on13), M13.Refused)
rec('S3_must', 'r13_refuses_the_r14_base_registry', r_, code=getattr(e_, 'refusal_code', None))

# ------------------------------------------------------------------ 4. the token end to end on I4 (evaluate_gate, synthetic record)
DRV = sha_b(b'c4probe synthetic driver (not b5cc62af)')
prod_i4 = fixture('I4')
prod_other = fixture('not the I4 producer')


def i4_record(path, verdict=None, bitwise=True, prod=prod_i4):
    obj = {'schema': M14.GATE_SCHEMA, 'gate': 'I4', 'producer': dict(prod), 'verdict': verdict or M14.I4_PASS_VERDICT, 'tail': 'ON',
           'driver_sha256': DRV, 'serial_result_sha256': sha_b(b'c4probe serial'), 'parallel_result_sha256': sha_b(b'c4probe parallel'),
           'v8c_f1_fix_confirmed': True, 'bitwise_equal': bitwise, 'differences_outside_custody': [],
           'note': 'Claude4 lens_integration SYNTHETIC I4 record; no run exists behind it'}
    return write_json(path, obj)

rp_pass = i4_record(SB / 'I4_SYNTH_PASS.json')
rp_fail = i4_record(SB / 'I4_SYNTH_FAIL.json', verdict='FAIL', bitwise=False)
rp_contra = i4_record(SB / 'I4_SYNTH_PASS_VERDICT_BITWISE_FALSE.json', bitwise=False)
rp_badprod = i4_record(SB / 'I4_SYNTH_UNREGISTERED_PRODUCER.json', prod=prod_other)


def ctx_for(M, reg):
    return {'producer_registry': reg, 'case_block': {'cases': {c: {'drivers_allowed': [DRV]} for c in M.T_CASES}}}


def ev(M, token_on_i4, recpin, i4_list=None, hand_token=False, gate='I4'):
    o = reg_obj(M, M.GATE_RECORD_AFTER_SEAL_ALLOWED if token_on_i4 else tuple(g for g in M.GATE_RECORD_AFTER_SEAL_ALLOWED if g != 'I4'))
    if i4_list is not None:
        o['gate_records']['I4'] = i4_list
    reg = M.producer_registry_from_obj(o)
    if hand_token:
        reg['gate_records'][gate] = M.GATE_RECORD_AFTER_SEAL
    e = M.evaluate_gate(gate, recpin['path'], ctx_for(M, reg))
    return e['status'], e['codes']

st, cd = ev(M14, True, rp_pass)
rec('S4_eval', 'r14_I4_token_synthetic_pass_record_PASS', st == 'PASS' and cd == [], status=st, codes=cd)
st, cd = ev(M14, False, rp_pass, i4_list=[])
rec('S4_eval', 'r14_I4_no_token_no_sha_RECORD_DEFECT_A67_N2', st == 'RECORD_DEFECT' and 'GATE_RECORD_SHA_NOT_ROOT_REGISTERED_A67_N2:I4' in cd,
    status=st, codes=cd)
st, cd = ev(M14, False, rp_pass, i4_list=[rp_pass['sha256']])
rec('S4_eval', 'r14_I4_registered_by_sha_still_PASS', st == 'PASS', status=st, codes=cd)
st, cd = ev(M14, True, rp_badprod)
rec('S4_eval', 'r14_I4_token_does_not_bypass_producer_pin', st == 'RECORD_DEFECT' and any(c.startswith('PRODUCER_NOT_ROOT_REGISTERED_A62_2:I4') for c in cd),
    status=st, codes=cd)
st, cd = ev(M14, True, rp_fail)
rec('S4_eval', 'r14_I4_token_failing_record_FAIL', st == 'FAIL' and 'I4_SERIAL_PARALLEL_NOT_BITWISE_EQUAL' in cd, status=st, codes=cd)
st, cd = ev(M14, True, rp_contra)
rec('S4_eval', 'r14_I4_token_pass_verdict_contradicting_data_RECORD_DEFECT', st == 'RECORD_DEFECT' and 'VERDICT_PASS_CONTRADICTS_DATA:I4' in cd,
    status=st, codes=cd)
st, cd = ev(M13, False, rp_pass, i4_list=[], hand_token=True)
rec('S4_eval', 'r13_hand_built_I4_token_fails_closed_NEW52', st == 'RECORD_DEFECT' and 'GATE_RECORD_TOKEN_NOT_ALLOWED_FOR_THIS_GATE_NEW52:I4' in cd,
    status=st, codes=cd)
# hand-built token on a refused gate stays fail-closed on r14 (gate_record_sha_codes; every gate, direct call)
gsc = {}
for lab, M in (('r14', M14), ('r13', M13)):
    for g in M.ALL_GATES:
        gsc.setdefault(lab, {})[g] = M.gate_record_sha_codes(g, sha_b(b'x'), {'gate_records': {g: M.GATE_RECORD_AFTER_SEAL}})
ok14 = all((gsc['r14'][g] == []) == (g in M14.GATE_RECORD_AFTER_SEAL_ALLOWED) for g in M14.ALL_GATES)
ok13 = all((gsc['r13'][g] == []) == (g in M13.GATE_RECORD_AFTER_SEAL_ALLOWED) for g in M13.ALL_GATES)
rec('S4_eval', 'gate_record_sha_codes_hand_built_token_matches_allowed_set_both', ok14 and ok13,
    r14_I4=gsc['r14']['I4'], r13_I4=gsc['r13']['I4'], r14_EPS=gsc['r14']['EPS'])

# ------------------------------------------------------------------ 5. seal tool 4 new_items_codes (its own function, its own folder)
sys.path.insert(0, ST4)
T4 = load(PINS['tool4'][0], 'c4probe_tool4')
rec('S5_tool4', 'tool4_loaded_with_siblings', all(sha_f(getattr(m, '__file__')) == PINS[k][1] for m, k in ((T4.C, 'seal_common'), (T4.T2, 'tool2'), (T4.T3, 'tool3'))),
    C=T4.C.__file__, T2=T4.T2.__file__, T3=T4.T3.__file__)
R14SHA = PINS['r14_source'][1]
R13SHA = PINS['r13_source'][1]
ITEM = {'id': 'NEW-52', 'disposition': 'ADOPTED', 'reason': 'synthetic probe item', 'must_fail_tests': ['R10_NEW52_HAND_BUILT_REGISTRY_WITH_THE_TOKEN_ON_EPS_FAILS_CLOSED']}


def ni(impl_key, reviewed, items=(), pin_sha=None):
    p, h = PINS[impl_key]
    chk = T4.C.Checker('c4probe_new_items')
    obj = {'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': {'path': p, 'sha256': pin_sha or h}, 'items': [dict(x) for x in items],
           'note': 'Claude4 lens_integration synthetic NEW-item list'}
    q = T4.new_items_codes(chk, obj, reviewed)
    return [f['code'] for f in chk.failures], q

for impl, reviewed, items, want, lab in (
        ('r14_impl_v001', R14SHA, (), ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'], 'IMPL_R14_V001_854cad0d_reviewed_r14_REFUSED'),
        ('r14_impl_v001', R14SHA, (ITEM,), ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'], 'IMPL_R14_V001_with_one_valid_item_REFUSED'),
        ('r14_impl_v002', R14SHA, (), [], 'IMPL_R14_V002_2ba6d12e_reviewed_r14_PASS'),
        ('r14_impl_v002', R14SHA, (ITEM,), [], 'IMPL_R14_V002_with_one_valid_item_PASS'),
        ('r13_impl', R14SHA, (), ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'], 'IMPL_R13_274f7049_reviewed_r14_REFUSED'),
        ('r13_impl', R13SHA, (), [], 'control_IMPL_R13_reviewed_r13_PASS'),
        ('r14_impl_v002', R13SHA, (), ['NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE'], 'IMPL_R14_V002_reviewed_r13_REFUSED'),
        ('r14_selected_v001', R14SHA, (), [], 'SELECTED_R14_V001_as_impl_PASSES_substring_check_NOTE')):
    codes, q = ni(impl, reviewed, items)
    rec('S5_tool4', lab, codes == want, codes=codes, impl=PINS[impl][0], reviewed=reviewed[:8])
codes, q = ni('r14_impl_v002', R14SHA, (), pin_sha=PINS['r14_impl_v001'][1])
rec('S5_tool4', 'control_wrong_impl_pin_PIN_BYTES_MISMATCH_and_no_text_check', codes == ['PIN_BYTES_MISMATCH'], codes=codes)
# which r14 top-level files carry the reviewed source sha in full (and the 8-hex prefix)
cont = {}
for p in sorted(Path(R14D).iterdir()):
    if p.is_file():
        t = p.read_bytes().decode('utf-8', 'replace')
        cont[p.name] = {'full_sha': R14SHA in t, 'prefix8': R14SHA[:8] in t, 'sha256': sha_f(p)}
R['r14_sha_containment'] = cont
rec('S5_tool4', 'IMPL_R14_V001_contains_neither_full_sha_nor_prefix', cont['COMPARE_V007_IMPL_R14.md'] == dict(cont['COMPARE_V007_IMPL_R14.md'], full_sha=False, prefix8=False),
    v001=cont['COMPARE_V007_IMPL_R14.md'])
rec('S5_tool4', 'IMPL_R14_V002_contains_full_sha', cont['COMPARE_V007_IMPL_R14_CX1V002.md']['full_sha'] is True)
rec('S5_tool4', 'r14_files_with_full_sha_listed', True, files=sorted(k for k, v in cont.items() if v['full_sha']))
# SELECTED V002 (the publication successor) pins the V002 IMPL; SELECTED V001 pins V001
s1 = json.loads(Path(PINS['r14_selected_v001'][0]).read_bytes())
s2 = json.loads(Path(PINS['r14_selected_v002'][0]).read_bytes())
rec('S5_tool4', 'SELECTED_V001_pins_IMPL_V001', s1['implementation'] == {'path': PINS['r14_impl_v001'][0], 'sha256': PINS['r14_impl_v001'][1], 'bytes': 2080})
rec('S5_tool4', 'SELECTED_V002_pins_IMPL_V002_and_supersedes_V001',
    s2['implementation']['sha256'] == PINS['r14_impl_v002'][1] and s2['supersedes_selection']['sha256'] == PINS['r14_selected_v001'][1])
same = sorted(k for k in s1 if k not in ('utc', 'implementation', 'note') and s1[k] == s2.get(k))
diffk = sorted(k for k in set(s1) | set(s2) if s1.get(k) != s2.get(k))
rec('S5_tool4', 'SELECTED_V002_differs_from_V001_only_in_utc_implementation_note_and_supersedes_selection',
    diffk == ['implementation', 'note', 'supersedes_selection', 'utc'], differing=diffk)
# V002 IMPL = V001 IMPL bytes + an appended section (prefix check)
i1 = Path(PINS['r14_impl_v001'][0]).read_bytes()
i2 = Path(PINS['r14_impl_v002'][0]).read_bytes()
rec('S5_tool4', 'IMPL_V002_is_IMPL_V001_plus_appended_section', i2.startswith(i1), appended=i2[len(i1):].decode('utf-8', 'replace'))

# ------------------------------------------------------------------ 6. tool 2 on r14: a synthetic sealed copy (five pin lines only)
T2 = T4.T2
C = T4.C
rec('S6_tool2', 'pin_names', tuple(C.PIN_NAMES) == ('V007_PREREG_SHA256', 'PIN_ADDENDUM_V005', 'PIN_DRIVER_BUILD_RECORD', 'PIN_V010_R5_CHECK',
                                                       'PIN_PRODUCER_REGISTRY'), names=C.PIN_NAMES)
import ast as _ast
for lab, txt in (('r14', b14.decode()), ('r13', b13.decode())):
    cnt = T2.assign_counts(_ast.parse(txt))
    rec('S6_tool2', lab + '_each_pin_assigned_exactly_once', all(v == 1 for v in cnt.values()), counts=cnt)
    env = T2.module_strings(_ast.parse(txt))
    rec('S6_tool2', lab + '_cited_addendum_and_schema_report', env.get('ADDENDUM_V005_CITED') == PINS['v005_addendum_live'][0], cited=env.get('ADDENDUM_V005_CITED'),
        schema_report=env.get('SCHEMA_REPORT'))
dbr = write_json(SB / 'SYNTH_DRIVER_BUILD_RECORD.json', {'synthetic': 'driver build record stand-in (Claude4 probe)'})
dcr = write_json(SB / 'SYNTH_DRIVER_CHECK_RECORD.json', {'synthetic': 'driver check record stand-in (Claude4 probe)'})
prg = write_json(SB / 'SYNTH_PRODUCER_REGISTRY.json', {'synthetic': 'producer registry stand-in (Claude4 probe)'})
rev14 = {'path': PINS['r14_source'][0], 'sha256': R14SHA}
fa = {'path': PINS['v005_addendum_live'][0], 'sha256': PINS['v005_addendum_live'][1]}
slots = write_json(SB / 'SYNTH_SLOTS.json', {'compare_reviewed_source': rev14, 'frozen_addendum': fa, 'driver_build_record': dbr,
                                             'driver_check_record': dcr, 'producer_registry': prg})
prereg = write_json(SB / 'SYNTH_PREREG.json', {'seal_slots': {'compare': {'value': rev14}}, 'note': 'synthetic prereg stand-in (Claude4 probe)'})
lit = {'V007_PREREG_SHA256': repr(prereg['sha256']), 'PIN_ADDENDUM_V005': repr(fa['sha256']),
       'PIN_DRIVER_BUILD_RECORD': repr((dbr['path'], dbr['sha256'])), 'PIN_V010_R5_CHECK': repr((dcr['path'], dcr['sha256'])),
       'PIN_PRODUCER_REGISTRY': repr((prg['path'], prg['sha256']))}


def sealed_copy(lines, name):
    out, n = [], 0
    for ln in lines:
        nm = next((k for k in C.PIN_NAMES if ln.startswith(k + ' = None')), None)
        if nm:
            rhs, com = T2.split_assignment(ln, nm)
            assert rhs == 'None'
            body = ln.rstrip('\n')
            new = nm + ' = ' + lit[nm] + body[len(nm + ' = None'):]
            out.append(new + ('\n' if ln.endswith('\n') else ''))
            n += 1
        else:
            out.append(ln)
    p = SB / name
    p.write_text(''.join(out))
    return str(p), n

sp14, n14 = sealed_copy(L14, 'SYNTHETIC_NOT_A_SEAL_sealed_copy_of_r14.py.txt')
rec('S6_tool2', 'synthetic_sealed_copy_changes_five_lines', n14 == 5, n=n14)
r = T2.run(PINS['r14_source'][0], sp14, slots['path'], prereg['path'])
rec('S6_tool2', 'tool2_PASS_on_r14_with_five_pins_set', r['verdict'] == 'PASS', verdict=r['verdict'], failures=r['failures'],
    notes=[n['code'] for n in r['notes']])
sp13, n13 = sealed_copy(L13, 'SYNTHETIC_NOT_A_SEAL_sealed_copy_of_r13.py.txt')
r = T2.run(PINS['r14_source'][0], sp13, slots['path'], prereg['path'])
rec('S6_tool2', 'tool2_refuses_r13_sealed_against_r14_reviewed_NON_PIN_LINE_341', r['verdict'] == 'REFUSE' and
    [f['code'] for f in r['failures']] == ['NON_PIN_LINE_DIFFERS'] and r['failures'][0]['detail'] == 'line 341', failures=r['failures'])
slots13 = write_json(SB / 'SYNTH_SLOTS_R13_REVIEWED.json', {'compare_reviewed_source': {'path': PINS['r13_source'][0], 'sha256': R13SHA},
                                                           'frozen_addendum': fa, 'driver_build_record': dbr, 'driver_check_record': dcr,
                                                           'producer_registry': prg})
r = T2.run(PINS['r14_source'][0], sp14, slots13['path'], prereg['path'])
rec('S6_tool2', 'tool2_refuses_when_the_slot_still_names_r13', r['verdict'] == 'REFUSE', failures=[f['code'] for f in r['failures']])
# tool 3's compare API is all present on r14 (load_reviewed_compare: compiled from the verified bytes)
M14b = C.load_reviewed_compare(PINS['r14_source'][0], R14SHA)
missing = [a for a in T4.T3.COMPARE_API if not hasattr(M14b, a)]
rec('S6_tool2', 'tool3_COMPARE_API_present_on_r14', missing == [], missing=missing)
rec('S6_tool2', 'tool3_r14_constants_it_reads_equal_r13',
    all(getattr(M14b, a) == getattr(M13, a) for a in ('PRODUCTION_GAS_M_S_A57', 'NGC_GAS_M_S_A57', 'CASE_BLOCK_SCHEMA', 'GATE_SCHEMA', 'ROUTE_A_MODE_DEFAULT'))
    and M14b.ROUTE_A_MODES == M13.ROUTE_A_MODES)
rec('S6_tool2', 'tool4_sealed_schema_report_on_r14', T4.sealed_schema_report(PINS['r14_source'][0]) == M13.SCHEMA_REPORT, got=T4.sealed_schema_report(PINS['r14_source'][0]))

# ------------------------------------------------------------------ 7. C-08 rows: the cited line carries the id, in r13 and r14
ID_RX = re.compile(r'NEW-(\d+)(?!\d)')


def first_lines(lines):
    fl = {}
    for i, ln in enumerate(lines):
        for m in ID_RX.finditer(ln):
            fl.setdefault('NEW-' + m.group(1), i + 1)
    return fl
fl13, fl14 = first_lines(L13), first_lines(L14)
rec('S7_c08', 'r13_r14_first_line_maps_identical', fl13 == fl14, n_ids=len(fl14))
for key in ('md_v002', 'md_v003_draft'):
    d = json.loads(Path(PINS[key][0]).read_bytes())
    rows = d['c08_table']
    bad = []
    for r_ in rows:
        nid, ln = r_['new_item_id'], r_['line']
        f = r_['file']
        for lab, LL in (('r13', L13), ('r14', L14)):
            text = LL[ln - 1] if 0 < ln <= len(LL) else ''
            has = any(('NEW-' + m.group(1)) == nid for m in ID_RX.finditer(text))
            if not has:
                bad.append((nid, lab, ln, 'id_not_on_line'))
        if fl14.get(nid) != ln:
            bad.append((nid, 'r14', ln, 'not_first_line_first_is_%s' % fl14.get(nid)))
    ids = sorted(r_['new_item_id'] for r_ in rows)
    rec('S7_c08', key + '_every_row_line_carries_its_id_in_r13_and_r14_and_is_the_first', bad == [], rows=len(rows), bad=bad,
        files=sorted({r_['file'] for r_ in rows}))
    rec('S7_c08', key + '_row_ids_are_exactly_the_ids_in_r14', sorted(fl14) == ids, missing=sorted(set(fl14) - set(ids)),
        extra=sorted(set(ids) - set(fl14)))
    chk = T4.C.Checker('c4probe_md_form')
    T4.manual_disclosures_form_codes(chk, d)
    rec('S7_c08', key + '_tool4_form_check', chk.failures == [], failures=chk.failures)
# the IMPLs: no NEW id is declared by r14 (the V001 and V002 IMPL texts carry no NEW-<n>)
for k in ('r14_impl_v001', 'r14_impl_v002', 'r13_impl'):
    t = Path(PINS[k][0]).read_bytes().decode('utf-8')
    rec('S7_c08', k + '_carries_no_NEW_id', not ID_RX.search(t), found=sorted(set('NEW-' + m.group(1) for m in ID_RX.finditer(t))))

# ------------------------------------------------------------------ 8. E_R6_1 (tool 4 constant) and the r13 IMPL it names
r6 = json.loads(Path(PINS['r6_selected'][0]).read_bytes())
e = T4.E_R6_1
rec('S8_e_r6_1', 'tool4_E_R6_1_equals_r6_SELECTED_basis_erratum', e == r6['basis']['erratum_E_R6_1'], chars=len(e))
rec('S8_e_r6_1', 'E_R6_1_utf8_sha', sha_b(e.encode('utf-8')) == 'c28202b0909371f43180ca832e4652f3d835a977852cde5c261842315deb33f4',
    got=sha_b(e.encode('utf-8')))
rec('S8_e_r6_1', 'E_R6_1_names_the_r13_IMPL_274f7049', 'v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md' in e and '274f7049' in e and 'r14' not in e)
for key in ('md_v001', 'md_v002', 'md_v003_draft'):
    d = json.loads(Path(PINS[key][0]).read_bytes())
    rec('S8_e_r6_1', key + '_e_r6_1_text_equals_tool4_constant', d['e_r6_1_text'] == e)
d3 = json.loads(Path(PINS['md_v003_draft'][0]).read_bytes())
a114 = [x for x in d3['root_disclosures'] if x['id'] == 'A114_I4_AFTER_SEAL_R14']
rec('S8_e_r6_1', 'v003_draft_has_A114_row_naming_r14_sha_IMPL_V002_and_E_R6_1_succession',
    len(a114) == 1 and R14SHA in a114[0]['text'] and PINS['r14_impl_v002'][1] in a114[0]['text'] and 'E_R6_1' in a114[0]['text'],
    text=a114[0]['text'] if a114 else None)
rec('S8_e_r6_1', 'v003_draft_c08_confirmation_names_r14_sha_and_IMPL_V002',
    R14SHA in d3['c08_confirmation'] and PINS['r14_impl_v002'][1] in d3['c08_confirmation'])
rec('S8_e_r6_1', 'r6_selected_unchanged_bindings_names_r13_candidate', 'r13 f5adfd11' in r6['basis']['unchanged_bindings'],
    text=r6['basis']['unchanged_bindings'])

R['utc_end'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
R['fails'] = FAILS
R['n_checks'] = sum(len(v) for v in R['sections'].values())
R['n_ok'] = R['n_checks'] - len(FAILS)
R['sweeps'] = sweeps
Path(OUT / 'PROBE_RESULTS_C4.json').write_text(json.dumps(R, indent=1, sort_keys=True, default=str) + '\n')
print('\nPROBE %d/%d ok; fails: %s' % (R['n_ok'], R['n_checks'], FAILS))
raise SystemExit(0 if not FAILS else 1)
