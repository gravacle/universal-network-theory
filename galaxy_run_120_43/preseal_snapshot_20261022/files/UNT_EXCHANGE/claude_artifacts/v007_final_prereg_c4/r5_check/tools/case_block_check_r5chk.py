# case_block_check_r5chk.py -- independent check of the V007 case block CASE_BLOCK_V007_C4V001 (76309ae3) against compare r12
# cx3v002 (4bd7b262), loaded UNMODIFIED in-process (r5_check helper, Claude4). Run ONLY under tools/run_fenced_r5chk.py.
# usage: run_fenced_r5chk.py FENCE SHA case_block_check_r5chk.py OUT.json SCRATCH_DIR
# Reads only named files; writes OUT.json and mutated case-block copies under SCRATCH_DIR, each by exclusive create.
import sys, os, json, hashlib, copy, re, importlib.util

T = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5_check/tools'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
def imp(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
L = imp('load_compare_r5chk', T + '/load_compare_r5chk.py')
R12 = (A + '/v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py', '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28')
C, csha = L.load(R12[0], R12[1], 'r12_r5chk')
out_path, scratch = sys.argv[1], sys.argv[2]

PINS = {
    'case_block': (A + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'),
    'spec_registry': (A + '/v007_launch_packet_cx1/SPEC_REGISTRY_R5_MS128_CX1V004.json', 'c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90'),
    'dry_v004': (A + '/v007_launch_packet_cx1/DRY_R5_MS128_V004.json', 'ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed'),
    'plan_v010': (A + '/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V010.json', '26f1ebf90d95d2674d4bcba7ac3416049cdba171c5754c32440b4c66480c8021'),
    'plan_v011': (A + '/v007_launch_packet_cx1/P128/LAUNCH_PLAN_V011_CX3V001.json', '1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c'),
    'build_v005': (A + '/v007_launch_packet_cx1/BUILD_V005.md', '46bc5b5d23bb39e74478e1b8ce49f31ebe07fc5afe59276eb4792375352e6e30'),
    'build_v007': (A + '/v007_launch_packet_cx1/BUILD_V007.md', '94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de'),
    'eps_cert': (A + '/tail_scheme_impl_c2/certificates_v002/gates/EPS_CERT_V006.json', '598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192'),
    'lo_cert': (A + '/tail_scheme_impl_c2/certificates_v004/gates/LO_CERT_V004_MS128.json', '1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a'),
}
R5DRV = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
R4DRV = 'b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
res = {'schema': 'R5CHK_CASE_BLOCK_CHECK_V001', 'compare': {'path': R12[0], 'sha256': csha, 'loaded': 'unmodified, in-process'},
       'checks': [], 'mutations': [], 'byte_mutations': [], 'observations': {}}
def chk(name, ok, detail=None):
    res['checks'].append({'name': name, 'ok': bool(ok), **({'detail': detail} if detail is not None else {})})
def sha_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for k, (p, s) in PINS.items():
    chk('pin from bytes: ' + k, sha_file(p) == s)
C.activate_driver_build(None)
chk('active build is the built-in r5 set (test mode default)', C.sealed_driver_sha() == R5DRV)
chk('pinned tail library sha (normalize_config only)', sha_file(C.PIN_UVT_LIB[0]) == C.PIN_UVT_LIB[1] == 'c28d4209dc617708e1ae4d1d568ecf88d79fa926847f0ac050748642e6990b22')

# ---- 1. validation by r12's own functions
cb = C.load_strict_file(PINS['case_block'][0], 'case block')
v_default = C.validate_case_block(cb)
v_par = C.validate_case_block(cb, route_a_mode='parallel8')
chk('r12 validate_case_block(case block of record) == [] (default mode)', v_default == [], v_default or None)
chk('r12 validate_case_block(case block of record, parallel8) == []', v_par == [], v_par or None)
chk('case block route_a_mode is parallel8 and key_equivalence_map is []', cb.get('route_a_mode') == 'parallel8' and cb.get('key_equivalence_map') == [])

# ---- 2. independent re-derivation of the spec list and shas from the sources
reg = json.load(open(PINS['spec_registry'][0]))
cases = [s['case'] for s in reg['specs']]
chk('registry c7023846 lists exactly the ten T-cases once each', sorted(cases) == sorted(C.T_CASES) and len(cases) == 10, cases)
chk('registry driver is v010 r5', reg['driver']['sha256'] == R5DRV)
chk('registry certificate slots are the A70 slots', reg['EPS'] == {'path': PINS['eps_cert'][0], 'sha256': PINS['eps_cert'][1]}
    and reg['LO'] == {'path': PINS['lo_cert'][0], 'sha256': PINS['lo_cert'][1]})
filled = {s['case']: s['filled'] for s in reg['specs']}
for lab in C.T_CASES:
    chk('FILLED spec bytes: ' + lab, sha_file(filled[lab]['path']) == filled[lab]['sha256'])
dry = json.load(open(PINS['dry_v004'][0]))
chk('DRY_R5_MS128_V004 names registry c7023846 and driver r5', dry['registry'] == {'path': PINS['spec_registry'][0], 'sha256': PINS['spec_registry'][1]} and dry['driver']['sha256'] == R5DRV)
dck = {c['case']: c for c in dry['checks']}
chk('DRY_R5_MS128_V004 has the ten cases, passed 10', sorted(dck) == sorted(C.T_CASES) and dry.get('passed') == 10)
reports = {}
for lab in C.T_CASES:
    c = dck[lab]
    rp = c['report']
    chk('dry report bytes: ' + lab, sha_file(rp['path']) == rp['sha256'])
    r = json.load(open(rp['path']))
    reports[lab] = r
    chk('dry passed, exit 0, 0 executed stages: ' + lab, c['passed'] is True and c['exit'] == 0 and c['executed_stages'] == 0 and r['executed_stages'] == 0)
    chk('dry report call_spec is the FILLED spec (path and sha): ' + lab, r['call_spec'] == filled[lab]['path'] and r['call_spec_sha256'] == filled[lab]['sha256'])
    chk('dry report driver r5: ' + lab, r['driver_sha256'] == R5DRV)
    rr = r['remaining_refusals']
    chk('dry: no binding blockers, no unexplained / beyond-pending / static refusals: ' + lab,
        r['binding_blockers'] == [] and rr.get('unexplained') == [] and rr.get('beyond_pending_inputs') == [] and rr.get('static') == [])
plans = {}
for name in ('plan_v010', 'plan_v011'):
    pl = json.load(open(PINS[name][0])); plans[name] = pl
    calls = {c['case']: c['spec'] for c in pl['calls']}
    chk(name + ' launches exactly the ten FILLED specs (path and sha)',
        calls == {lab: {'path': filled[lab]['path'], 'sha256': filled[lab]['sha256']} for lab in C.T_CASES})
    chk(name + ' driver r5, registry c7023846, order = the ten cases', pl['driver']['sha256'] == R5DRV
        and pl['registry']['sha256'] == PINS['spec_registry'][1] and sorted(pl['order']) == sorted(C.T_CASES))
def flat(x, p=''):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, p + '/' + str(k))
        if not x:
            yield p, {}
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from flat(v, p + '[%d]' % i)
        if not x:
            yield p, []
    else:
        yield p, x
f10, f11 = dict(flat(plans['plan_v010'])), dict(flat(plans['plan_v011']))
dl = sorted(set(k for k in set(f10) | set(f11) if f10.get(k, '<A>') != f11.get(k, '<A>')))
nonstr = [k for k in dl if not (isinstance(f10.get(k), str) and isinstance(f11.get(k), str))]
spec_or_core = [k for k in dl if re.search(r'/spec/|^/driver|^/registry|^/order|cap|/case$|start_order|axis_nodes|K_out', k)]
res['observations']['plan_v010_vs_v011'] = {'differing_leaves': len(dl), 'non_string_or_added_or_removed': nonstr,
                                            'spec_driver_registry_order_caps_differing': spec_or_core,
                                            'examples': [[k, f10.get(k), f11.get(k)] for k in dl[:4]]}
chk('plan V011 differs from V010 only in string leaves, none in spec/driver/registry/order/caps', not nonstr and not spec_or_core, len(dl))
b5 = open(PINS['build_v005'][0]).read(); b7 = open(PINS['build_v007'][0]).read()
chk('BUILD_V005 text carries the full registry and dry-run shas', PINS['spec_registry'][1] in b5 and PINS['dry_v004'][1] in b5)
res['observations']['build_v007_names_full_sha'] = {k: (PINS[k][1] in b7) for k in ('spec_registry', 'dry_v004', 'plan_v011', 'plan_v010', 'case_block')}

lib = C.load_uvt_lib()
res['observations']['spec_vs_dry_normalized_numerics'] = {}
for lab in C.T_CASES:
    r = reports[lab]
    num = r['normalized_spec']['numerics']
    sh_drv = r['uv_tail']['config']['normalized_sha256']
    sh_lib = lib.normalize_config(num['uv_tail'])['sha256']
    chk('uv_tail sha: driver-side normalized == pinned-library normalize_config: ' + lab, sh_drv == sh_lib)
    exp = {'grid': C.EXPECTED_GRID[lab], 'truncation': C.EXPECTED_TRUNCATION[lab], 'normalized_spec_equal': {'/numerics': num},
           'tail': True, 'ro1_required': True, 'uv_tail_config_sha256': sh_lib, 'drivers_allowed': [R5DRV]}
    got = {k: v for k, v in cb['cases'][lab].items() if k != 'note'}
    same = C.canon(got) == C.canon(exp)
    chk('case entry == my derivation from FILLED spec + its r5 dry run (note excluded): ' + lab, same,
        None if same else sorted(k for k in set(got) | set(exp) if C.canon(got.get(k)) != C.canon(exp.get(k))))
    note = cb['cases'][lab].get('note', '')
    chk('note names its FILLED spec sha and dry report sha: ' + lab, filled[lab]['sha256'] in note and dck[lab]['report']['sha256'] in note)
    sp = json.load(open(filled[lab]['path']))
    fs, fn = dict(flat(sp['numerics'])), dict(flat(num))
    res['observations']['spec_vs_dry_normalized_numerics'][lab] = {
        'added': sorted(k for k in fn if k not in fs), 'removed': sorted(k for k in fs if k not in fn),
        'changed': sorted(k for k in fs if k in fn and fs[k] != fn[k])}
    uv = num['uv_tail']
    chk('A70 certificate slots in the registered uv_tail: ' + lab,
        uv.get('eps_certificate') == {'path': PINS['eps_cert'][0], 'sha256': PINS['eps_cert'][1]}
        and uv.get('lo_certificate') == {'path': PINS['lo_cert'][0], 'sha256': PINS['lo_cert'][1]})
e5 = {k: v for k, v in cb['cases']['C5H'].items() if k != 'note'}
exp5 = {'grid': 'G5', 'truncation': C.EXPECTED_TRUNCATION['C5H'], 'normalized_spec_equal': {}, 'tail': False, 'ro1_required': False,
        'call_spec_sha256': C.PIN_C5H_SPEC[1], 'drivers_allowed': [C.DRIVER_V009_EXT]}
chk('C5H entry == derivation (registered call 60b46130, v009-EXT 999331af, nothing else)', C.canon(e5) == C.canon(exp5))
ref = C.c5h_numerics_reference()
eq, diff = C.numerics_equal_except(cb['cases']['C4T-D5']['normalized_spec_equal']['/numerics'], ref, ('composite_grid_spec', 'uv_tail'))
chk('C4T-D5 /numerics equal the C5H reference outside composite_grid_spec and uv_tail (RA1, A50 S1)', eq, None if eq else diff[:6])
uvs = {lab: cb['cases'][lab]['uv_tail_config_sha256'] for lab in C.T_CASES}
res['observations']['uv_tail_config_sha256_groups'] = {s: sorted(l for l in uvs if uvs[l] == s) for s in sorted(set(uvs.values()))}

# ---- 3. in-memory mutations: each must be refused by r12 validate_case_block (except where stated)
old_c2 = json.load(open(A + '/v007_launch_packet_cx1/P128/specs/C2T_P128_CX1V002.FILLED.json'))['numerics']
def mut(name, f, expect=True, note=None):
    m = copy.deepcopy(cb)
    f(m)
    w = C.validate_case_block(m)
    res['mutations'].append({'name': name, 'refused': bool(w), 'expected_refused': expect, 'ok': bool(w) == expect,
                             'reasons_first': [x[:160] for x in w[:2]], 'n_reasons': len(w), **({'note': note} if note else {})})
for lab in list(C.REGISTERED):
    mut('drop case ' + lab, lambda m, lab=lab: m['cases'].pop(lab))
mut('add an unknown case C5T', lambda m: m['cases'].__setitem__('C5T', copy.deepcopy(m['cases']['C4T'])))
def swap_uvsha(m):
    a, b = m['cases']['C4T']['uv_tail_config_sha256'], m['cases']['C4T-KHI']['uv_tail_config_sha256']
    m['cases']['C4T']['uv_tail_config_sha256'], m['cases']['C4T-KHI']['uv_tail_config_sha256'] = b, a
mut('swap uv_tail_config_sha256 between C4T and C4T-KHI', swap_uvsha)
mut('C4T uv_tail_config_sha256 := its FILLED spec sha', lambda m: m['cases']['C4T'].__setitem__('uv_tail_config_sha256', filled['C4T']['sha256']))
mut('C5H call_spec_sha256 := the reviewed C5 spec 09ff5a96', lambda m: m['cases']['C5H'].__setitem__('call_spec_sha256', C.PIN_C5R3_SPEC_REVIEWED[1]))
def swap_num(m):
    a, b = m['cases']['C4T']['normalized_spec_equal'], m['cases']['C4T-KLO']['normalized_spec_equal']
    m['cases']['C4T']['normalized_spec_equal'], m['cases']['C4T-KLO']['normalized_spec_equal'] = b, a
mut('swap the whole /numerics of C4T and C4T-KLO', swap_num)
def swap_num_and_sha(m):
    swap_num(m); swap_sha = (m['cases']['C4T']['uv_tail_config_sha256'], m['cases']['C4T-KLO']['uv_tail_config_sha256'])
    m['cases']['C4T']['uv_tail_config_sha256'], m['cases']['C4T-KLO']['uv_tail_config_sha256'] = swap_sha[1], swap_sha[0]
mut('swap /numerics AND uv_tail sha of C4T and C4T-KLO (consistent swap)', swap_num_and_sha)
mut('C2T /numerics := the superseded CX1V002 FILLED C2T spec numerics', lambda m: m['cases']['C2T']['normalized_spec_equal'].__setitem__('/numerics', copy.deepcopy(old_c2)))
mut('C4T drivers_allowed := [v010 r4 b9ae92d5]', lambda m: m['cases']['C4T'].__setitem__('drivers_allowed', [R4DRV]))
mut('C4T drivers_allowed := [r5, r4]', lambda m: m['cases']['C4T'].__setitem__('drivers_allowed', [R5DRV, R4DRV]))
mut('C4T note: FILLED sha replaced by C2T FILLED sha (notes are free text)',
    lambda m: m['cases']['C4T'].__setitem__('note', m['cases']['C4T']['note'].replace(filled['C4T']['sha256'], filled['C2T']['sha256'])),
    expect=False, note='validate_case_block does not read notes; FILLED spec identity is bound by the launch template and V3 at run time, not by this block')
KM_OK = {'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0, 'b0_identity_evidence': 'B0 record c2cec35b'}
mut('key map: one well-formed entry on /numerics/route_a/seed_source_rtol_factor', lambda m: m.__setitem__('key_equivalence_map', [dict(KM_OK)]),
    expect=False, note='well-formed key-map entries on allowed pointers are admitted by validate_case_block; in sealed mode any byte change is refused by the binding_inputs.case_block sha (CASE_BLOCK_SHA_MISMATCH), see the CLI mutations')
mut('key map: well-formed entry on /numerics/column_workers', lambda m: m.__setitem__('key_equivalence_map', [{'pointer': '/numerics/column_workers', 'absent_equivalent_value': 2, 'b0_identity_evidence': 'x'}]),
    expect=False, note='as above')
mut('key map: entry missing b0_identity_evidence', lambda m: m.__setitem__('key_equivalence_map', [{'pointer': KM_OK['pointer'], 'absent_equivalent_value': 1.0}]))
mut('key map: one pointer mapped twice', lambda m: m.__setitem__('key_equivalence_map', [dict(KM_OK), dict(KM_OK)]))
mut('key map: pointer inside uv_tail', lambda m: m.__setitem__('key_equivalence_map', [{'pointer': '/numerics/uv_tail/gas', 'absent_equivalent_value': {}, 'b0_identity_evidence': 'x'}]))
mut('key map: pointer outside /numerics', lambda m: m.__setitem__('key_equivalence_map', [{'pointer': '/label', 'absent_equivalent_value': '', 'b0_identity_evidence': 'x'}]))
mut('key map: not a list', lambda m: m.__setitem__('key_equivalence_map', {'pointer': KM_OK['pointer']}))
mut('route_a_mode := serial_with_exemption', lambda m: m.__setitem__('route_a_mode', 'serial_with_exemption'),
    expect=False, note='recorded as observed; the mode is fixed by the pinned block, and a CLI mode differing from it is refused (ROUTE_A_MODE_SOURCES_DIFFER)')
mut('route_a_mode := bogus', lambda m: m.__setitem__('route_a_mode', 'bogus'))
mut('schema := C2V002', lambda m: m.__setitem__('schema', 'UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V002'))
mut('unknown top-level key', lambda m: m.__setitem__('extra', 1))
mut('C4T tail := false', lambda m: m['cases']['C4T'].__setitem__('tail', False))
mut('C4T ro1_required := false', lambda m: m['cases']['C4T'].__setitem__('ro1_required', False))
mut('C4T grid := G2', lambda m: m['cases']['C4T'].__setitem__('grid', 'G2'))
mut('S4T truncation := cube', lambda m: m['cases']['S4T'].__setitem__('truncation', {'shape': 'cube', 'kmax_inverse_kpc': None}))
mut('C4T-KLO outer K_big := 32', lambda m: m['cases']['C4T-KLO']['normalized_spec_equal']['/numerics']['uv_tail']['outer'].__setitem__('K_big_inverse_kpc', 32.0))
mut('C4T uv_tail gas M_s := 64', lambda m: m['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['gas'].__setitem__('M_s', 64))
mut('C4T-A lambda_scale := 1.0', lambda m: m['cases']['C4T-A']['normalized_spec_equal']['/numerics']['uv_tail'].__setitem__('lambda_scale', 1.0))
mut('C4T-D5 route_a column_workers := 1', lambda m: m['cases']['C4T-D5']['normalized_spec_equal']['/numerics']['route_a'].__setitem__('column_workers', 1))
mut('C2T route_a seed_source_rtol_factor := 0.1', lambda m: m['cases']['C2T']['normalized_spec_equal']['/numerics']['route_a'].__setitem__('seed_source_rtol_factor', 0.1))
mut('C4T-D5 source_rule := continuum_v001', lambda m: m['cases']['C4T-D5']['normalized_spec_equal']['/numerics']['uv_tail'].__setitem__('source_rule', 'continuum_v001'))
mut('C4T uv_tail eps_certificate sha := LO sha', lambda m: m['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['eps_certificate'].__setitem__('sha256', PINS['lo_cert'][1]))
mut('C5H tail := true', lambda m: m['cases']['C5H'].__setitem__('tail', True))
mut('C5H drivers_allowed := [r5]', lambda m: m['cases']['C5H'].__setitem__('drivers_allowed', [R5DRV]))
mut('C4T unknown entry key', lambda m: m['cases']['C4T'].__setitem__('spec_sha256', filled['C4T']['sha256']))
mut('C4T /numerics brackets := {}', lambda m: m['cases']['C4T']['normalized_spec_equal']['/numerics'].__setitem__('brackets', {}))

# ---- 4. byte-level duplicate-key mutations, read back with r12 load_strict_file (must refuse)
raw = open(PINS['case_block'][0], 'rb').read().decode('utf-8')
def write_scratch(name, text):
    p = os.path.join(scratch, name)
    with open(p, 'x') as f:
        f.write(text)
    return p
def bmut(name, text, want_code):
    p = write_scratch(name, text)
    try:
        C.load_strict_file(p, 'case block')
        code, refused = None, False
    except C.Refused as exc:
        code, refused = exc.refusal_code, True
    res['byte_mutations'].append({'name': name, 'path': p, 'sha256': sha_file(p), 'refused': refused, 'code': code,
                                  'expected_code': want_code, 'ok': refused and code == want_code})
def ins_after(text, pattern, insert):
    mm = re.search(pattern, text)
    assert mm, pattern
    return text[:mm.end()] + insert + text[mm.end():]
bmut('CB_DUP_SCHEMA_R5CHK.json', ins_after(raw, r'^\{', ' "schema": "UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V003",'), 'CASE_BLOCK_DUPLICATE_JSON_KEY_A71')
bmut('CB_DUP_CASE_C4T_R5CHK.json', ins_after(raw, r'"cases"\s*:\s*\{', ' "C4T": {},'), 'CASE_BLOCK_DUPLICATE_JSON_KEY_A71')
bmut('CB_DUP_ENTRY_KEY_R5CHK.json', ins_after(raw, r'"C4T"\s*:\s*\{', ' "uv_tail_config_sha256": "' + '0' * 64 + '",'), 'CASE_BLOCK_DUPLICATE_JSON_KEY_A71')
bmut('CB_DUP_NUMERICS_KEY_R5CHK.json', ins_after(raw, r'"/numerics"\s*:\s*\{', ' "picard": {},'), 'CASE_BLOCK_DUPLICATE_JSON_KEY_A71')
bmut('CB_DUP_EQUAL_VALUES_R5CHK.json', ins_after(raw, r'^\{', ' "route_a_mode": "parallel8",'), 'CASE_BLOCK_DUPLICATE_JSON_KEY_A71')
bmut('CB_DUP_PLUS_LONG_INT_R5CHK.json', ins_after(raw, r'^\{', ' "schema": "X", "n": ' + '7' * 4301 + ','), 'CASE_BLOCK_UNREADABLE')
km_text = json.dumps(dict(cb, key_equivalence_map=[KM_OK]), indent=1)
km_path = write_scratch('CB_KEYMAP_WELLFORMED_R5CHK.json', km_text)
res['observations']['keymap_mutated_copy'] = {'path': km_path, 'sha256': sha_file(km_path),
                                              'validate_case_block': C.validate_case_block(C.load_strict_file(km_path, 'case block'))}
cp = write_scratch('CASE_BLOCK_V007_C4V001_BYTE_COPY_R5CHK.json', raw)
res['observations']['byte_copy'] = {'path': cp, 'sha256': sha_file(cp), 'equals_record': sha_file(cp) == PINS['case_block'][1]}

res['summary'] = {'checks': '%d/%d' % (sum(c['ok'] for c in res['checks']), len(res['checks'])),
                  'mutations_as_expected': '%d/%d' % (sum(m['ok'] for m in res['mutations']), len(res['mutations'])),
                  'mutations_refused': '%d/%d' % (sum(m['refused'] for m in res['mutations']), len(res['mutations'])),
                  'byte_mutations_ok': '%d/%d' % (sum(m['ok'] for m in res['byte_mutations']), len(res['byte_mutations'])),
                  'validate_case_block_record': v_default}
with open(out_path, 'x') as f:
    json.dump(res, f, indent=1)
print(json.dumps(res['summary']))
for c in res['checks']:
    if not c['ok']:
        print('CHECK_FAIL', c)
for m in res['mutations']:
    if not m['ok']:
        print('MUTATION_UNEXPECTED', m)
for m in res['byte_mutations']:
    if not m['ok']:
        print('BYTE_MUTATION_UNEXPECTED', m)
