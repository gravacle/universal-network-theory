"""Claude4 r5 helper (A99.2, rehearsal D-03): build CASE_BLOCK_V007_C4V001.json, the V007 case block, from the ten FILLED P128 /
M_s 128 T-case specs of SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846; the same ten FILLED shas the plan template LAUNCH_PLAN_V010
26f1ebf9 launches), using their driver-r5 dry-run normalized numerics (DRY_R5_MS128_V004 ff60cd6b; all of these are byte-pinned in
BUILD_V005), by Claude3's in-process recipe (producer_registry_c3/scripts/validate_registry_r11_c3v001.py and its r12 successors
validate_registry_r12_c3v001/_c3v002.py). Validate the block with compare r12 cx3v002's OWN validate_case_block, in-process (exec'd
unmodified by load_r12_c4r5), on the in-memory object and again on the written bytes; diagnose why the on-disk draft 6bf4ce5a reads
CASE_BLOCK_INVALID; run must-refuse mutations. Target-free spec metadata only. Run ONLY under run_fenced_c4r5.py. Exclusive create.
usage: run_fenced_c4r5.py FENCE SHA build_case_block_c4v001.py UTC"""
import copy, hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import load_r12_c4r5 as L                                                     # noqa: E402

UTC = sys.argv[1]
R5 = Path(__file__).resolve().parent.parent
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/'
PKT = A + 'v007_launch_packet_cx1/'
CB_OUT = R5 / 'case_block' / 'CASE_BLOCK_V007_C4V001.json'
RES_OUT = R5 / 'out' / 'CASE_BLOCK_BUILD_C4V001.json'
PINS = {
    'registry': (PKT + 'SPEC_REGISTRY_R5_MS128_CX1V004.json', 'c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90'),
    'plan_template_V010': (PKT + 'P128/LAUNCH_PLAN_V010.json', '26f1ebf90d95d2674d4bcba7ac3416049cdba171c5754c32440b4c66480c8021'),
    'dry_run_record': (PKT + 'DRY_R5_MS128_V004.json', 'ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed'),
    'build_v005_custody': (PKT + 'BUILD_V005.md', '46bc5b5d23bb39e74478e1b8ce49f31ebe07fc5afe59276eb4792375352e6e30'),
    'draft_case_block': (A + 'tail_scheme_impl_c2/driver/out/CASE_BLOCK_V007_DRAFT_C2V001.json',
                         '6bf4ce5a4219d281fa480d4249e818e8d9fc39779b3ad605e1a069f42e0da4c1'),
    'recipe_r11': (A + 'producer_registry_c3/scripts/validate_registry_r11_c3v001.py', '6580741c2bb4a822a7ef7451784c0d1b7abd2bf2d2c9d36346234cbb2af6cb36'),
    'recipe_r12_v001': (A + 'producer_registry_c3/scripts/validate_registry_r12_c3v001.py', '2935ab81fb92e370bada4766762066aa180802a959d16e1e837b8d1c7e47c040'),
    'recipe_r12_v002': (A + 'producer_registry_c3/scripts/validate_registry_r12_c3v002.py', 'fed3b7b8973916f2779fd01d187fb5b51c3006efc64888c1b1412404291526a6'),
    'fields_r12': (A + 'v007_compare_c2/r12/FIELDS_R12_CX3V002.md', '5cc95a06dbe91275cd891e9832a0b7709301ac076a1ce49a3a675d76ee1a967f'),
    'selected_r12': (A + 'v007_compare_c2/r12/SELECTED_R12_CX3V001.json', '91aa9747eccc0c4d1b7630547707f626fc6423db69947e21d503626c3beda883'),
}
CERT_EPS = '598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192'      # A70 EPS slot (EPS_CERT_V006)
CERT_LO = '1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a'       # A70/A72 LO slot (LO_CERT_V004_MS128)
sha = lambda b: hashlib.sha256(b).hexdigest()
OUT = {'schema': 'UNT_V007_CASE_BLOCK_BUILD_C4V001', 'utc': UTC, 'labels': 'TESTED = run or read from bytes here; FORMAL = from code read here',
       'checks': {}, 'pins_verified': {}}
FAIL = []


def check(name, ok, detail=None):
    OUT['checks'][name] = {'ok': bool(ok), 'detail': detail}
    if not ok:
        FAIL.append(name)


M = L.load()
OUT['compare'] = {'path': L.CMP, 'sha256': L.CMP_SHA, 'loaded_unmodified': True, 'module_name': M.__name__,
                  'c5h_registered_run_dirs_redirected_to': list(M.C5H_REGISTERED_RUN_DIRS)}
raw = {}
for k, (p, s) in PINS.items():
    b = Path(p).read_bytes()
    raw[k] = b
    OUT['pins_verified'][k] = {'path': p, 'sha256': sha(b), 'matches_pin': sha(b) == s}
    check('pin:' + k, sha(b) == s, sha(b))
reg = M.loads_strict(raw['registry'])
plan = M.loads_strict(raw['plan_template_V010'])
dry = M.loads_strict(raw['dry_run_record'])
r5 = M.PIN_DRIVER_V010_R5[1]
check('registry_driver_is_r5', reg['driver']['sha256'] == r5, reg['driver']['sha256'])
check('plan_driver_is_r5', plan['driver']['sha256'] == r5, plan['driver']['sha256'])
check('plan_registry_is_c7023846', plan['registry']['sha256'] == PINS['registry'][1], plan['registry']['sha256'])
check('dry_driver_is_r5', dry['driver']['sha256'] == r5, dry['driver']['sha256'])
check('dry_registry_is_c7023846', dry['registry']['sha256'] == PINS['registry'][1], dry['registry']['sha256'])
check('dry_passed_10', dry.get('passed') == 10, dry.get('passed'))
check('registry_EPS_is_A70_slot', reg['EPS']['sha256'] == CERT_EPS, reg['EPS']['sha256'])
check('registry_LO_is_A70_slot', reg['LO']['sha256'] == CERT_LO, reg['LO']['sha256'])
check('build_v005_pins_registry_plan_dry', all(PINS[k][1] in raw['build_v005_custody'].decode() for k in ('registry', 'plan_template_V010', 'dry_run_record')))


def one(rows, key, lab, where):
    hit = [r for r in rows if r.get(key) == lab]
    check('%s_has_exactly_one_%s' % (where, lab), len(hit) == 1, len(hit))
    return hit[0] if hit else None


T = list(M.T_CASES)
check('registry_cases_exactly_the_ten', sorted(x['case'] for x in reg['specs']) == sorted(T), [x['case'] for x in reg['specs']])
check('plan_cases_exactly_the_ten', sorted(x['case'] for x in plan['calls']) == sorted(T), [x['case'] for x in plan['calls']])
check('dry_cases_exactly_the_ten', sorted(x['case'] for x in dry['checks']) == sorted(T), [x['case'] for x in dry['checks']])
LIB = M.load_uvt_lib()
sealed = M.sealed_driver_sha()
check('sealed_driver_of_the_builtin_r5_build_is_b5cc62af', sealed == r5, sealed)
cases, prov = {}, {}
for lab in T:
    rs, pc, dc = one(reg['specs'], 'case', lab, 'registry'), one(plan['calls'], 'case', lab, 'plan'), one(dry['checks'], 'case', lab, 'dry')
    fp, fs = rs['filled']['path'], rs['filled']['sha256']
    fb = Path(fp).read_bytes()
    check(lab + ':filled_spec_bytes_are_the_registry_sha', sha(fb) == fs, sha(fb))
    check(lab + ':plan_spec_is_the_filled_spec', pc['spec'] == {'path': fp, 'sha256': fs}, pc['spec'])
    check(lab + ':dry_check_passed_exit0_no_stage', dc['passed'] is True and dc['exit'] == 0 and dc['executed_stages'] == 0)
    rb = Path(dc['report']['path']).read_bytes()
    check(lab + ':dry_report_bytes_are_the_recorded_sha', sha(rb) == dc['report']['sha256'], sha(rb))
    rep = M.loads_strict(rb)
    check(lab + ':dry_report_call_spec_is_the_filled_spec', rep.get('call_spec_sha256') == fs, rep.get('call_spec_sha256'))
    check(lab + ':dry_report_driver_is_r5', rep.get('driver_sha256') == r5, rep.get('driver_sha256'))
    check(lab + ':dry_report_no_binding_blockers', rep.get('binding_blockers') == [], rep.get('binding_blockers'))
    rr = rep.get('remaining_refusals') or {}
    check(lab + ':dry_report_no_unexplained_refusals', rr.get('unexplained') == [] and rr.get('beyond_pending_inputs') == [])
    num = (rep.get('normalized_spec') or {}).get('numerics')
    check(lab + ':dry_report_normalized_numerics_present', isinstance(num, dict))
    spec = M.loads_strict(fb)
    ls, ld = M._spec_leaves(spec['numerics']), M._spec_leaves(num)
    changed = sorted(k for k in ls if k in ld and ld[k] != ls[k])
    removed = sorted(k for k in ls if k not in ld)
    added = sorted(k for k in ld if k not in ls)
    check(lab + ':dry_normalization_changes_or_removes_no_spec_leaf', not changed and not removed, {'changed': changed, 'removed': removed})
    uvsha = LIB.normalize_config(num['uv_tail'])['sha256']
    drv_norm = ((rep.get('uv_tail') or {}).get('config') or {}).get('normalized_sha256')
    check(lab + ':uv_tail_config_sha_compare_side_equals_driver_dry_run_side', uvsha == drv_norm, {'compare_lib_c28d4209': uvsha, 'driver_r5_dry_run': drv_norm})
    ec, lc = num['uv_tail'].get('eps_certificate') or {}, num['uv_tail'].get('lo_certificate') or {}
    check(lab + ':uv_tail_certificates_are_the_A70_slots', ec.get('sha256') == CERT_EPS and lc.get('sha256') == CERT_LO)
    check(lab + ':uv_tail_certificate_files_hash_to_their_pins', sha(Path(ec['path']).read_bytes()) == ec['sha256'] and sha(Path(lc['path']).read_bytes()) == lc['sha256'])
    cases[lab] = {'grid': M.EXPECTED_GRID[lab], 'truncation': copy.deepcopy(M.EXPECTED_TRUNCATION[lab]),
                  'normalized_spec_equal': {'/numerics': num}, 'tail': True, 'ro1_required': True, 'uv_tail_config_sha256': uvsha,
                  'drivers_allowed': [sealed],
                  'note': 'FILLED spec %s sha256 %s; registered /numerics = its driver v010 r5 dry-run normalized_spec.numerics, report %s '
                          'sha256 %s (DRY_R5_MS128_V004 ff60cd6b)' % (fp, fs, dc['report']['path'], dc['report']['sha256'])}
    prov[lab] = {'filled_spec': {'path': fp, 'sha256': fs}, 'dry_report': dc['report'], 'uv_tail_config_sha256': uvsha,
                 'dry_normalization_added_leaves': added,
                 'outer': num['uv_tail']['outer'], 'gas': num['uv_tail']['gas'], 'lambda_scale': num['uv_tail']['lambda_scale'],
                 'source_rule': num['uv_tail']['source_rule'] if isinstance(num['uv_tail']['source_rule'], str) else
                 {'rule': num['uv_tail']['source_rule'].get('rule'), 'ext_grid': 'G5 composite grid (registered)'},
                 'route_a': num.get('route_a'), 'picard': num.get('picard')}
cases[M.C5H] = {'grid': M.EXPECTED_GRID[M.C5H], 'truncation': copy.deepcopy(M.EXPECTED_TRUNCATION[M.C5H]), 'normalized_spec_equal': {},
                'tail': False, 'ro1_required': False, 'call_spec_sha256': M.PIN_C5H_SPEC[1], 'drivers_allowed': [M.DRIVER_V009_EXT],
                'note': 'C5H (A44, A48 AMB-20, A50): the registered C5H call 60b46130 on v009-EXT 999331af; its numerics are checked by the '
                        'compare against the spec as normalized by its pinned dry run cbd2885d (A50 S1); nothing else registered here'}
cb = {'schema': M.CASE_BLOCK_SCHEMA, 'route_a_mode': 'parallel8',
      'cases': {lab: cases[lab] for lab in M.REGISTERED}, 'key_equivalence_map': [],
      'note': ('V007 case block of record candidate, built by Claude4 under A99.2 (dispatch 0621) from the ten FILLED P128/M_s 128 '
               'specs of SPEC_REGISTRY_R5_MS128_CX1V004 (c7023846299bae03c5793c4187ca334d35ca3108401208761edbca37574dee90) and their '
               'driver v010 r5 (b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6) dry-run normalized numerics '
               '(DRY_R5_MS128_V004 ff60cd6b7d33b9a89326b90329e55a4b589f516b7e63cb2d28b41c4e83b7ceed), by the in-process recipe of '
               'Claude3 validate_registry_r11_c3v001.py / validate_registry_r12_c3v002.py. Route-A mode parallel8 (A47 I4 condition met, '
               'A51). key_equivalence_map is empty: no /numerics key of C4T-D5 outside composite_grid_spec and uv_tail differs from '
               'the C5H reference (A48 AMB-13; validate_case_block). Target-free spec metadata only. Codex2 checks it (A99.2).')}
why_mem = M.validate_case_block(cb, route_a_mode='parallel8')
check('validate_case_block_in_memory_valid', why_mem == [], why_mem)
check('registered_P_is_128', M.registered_P(cb) == 128.0, M.registered_P(cb))
check('registered_gas_M_s_is_128', M.registered_gas_M_s({'case_block': cb}) == 128, M.registered_gas_M_s({'case_block': cb}))
check('gas_M_s_context_codes_empty', M.gas_M_s_context_codes({'case_block': cb}, 'GQ') == [], M.gas_M_s_context_codes({'case_block': cb}, 'GQ'))
check('route_a_mode_is_the_default_parallel8', cb['route_a_mode'] == M.ROUTE_A_MODE_DEFAULT)
data = (json.dumps(cb, indent=1, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
if not FAIL:
    with open(CB_OUT, 'xb') as f:
        f.write(data)
    back = CB_OUT.read_bytes()
    cb_sha = sha(back)
    cb2 = M.load_strict_file(str(CB_OUT), 'case block')                      # the compare's own strict loader
    why_file = M.validate_case_block(cb2, route_a_mode='parallel8')
    check('written_bytes_equal_serialized', back == data)
    check('validate_case_block_on_written_bytes_valid', why_file == [], why_file)
    check('round_trip_canonical_equal', M.canon(cb2) == M.canon(cb))
    OUT['case_block'] = {'path': str(CB_OUT), 'sha256': cb_sha, 'bytes': len(back)}
else:
    OUT['case_block'] = {'path': None, 'sha256': None, 'not_written_because': list(FAIL)}
OUT['provenance_per_case'] = prov

# ---- must-refuse mutations of the new block (validate_case_block has power on it)
def mutate(name, fn):
    m = copy.deepcopy(cb)
    fn(m)
    w = M.validate_case_block(m, route_a_mode='parallel8')
    return {'mutation': name, 'refused': bool(w), 'first_reason': (w[0][:200] if w else None)}


def resha(m, lab):
    m['cases'][lab]['uv_tail_config_sha256'] = LIB.normalize_config(m['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail'])['sha256']


def uvt(m, lab):
    return m['cases'][lab]['normalized_spec_equal']['/numerics']['uv_tail']


def ms64(m):
    for lab in T:
        uvt(m, lab)['gas']['M_s'] = 64
        resha(m, lab)


def swap_klo_khi(m):
    a, b = uvt(m, 'C4T-KLO')['outer'], uvt(m, 'C4T-KHI')['outer']
    uvt(m, 'C4T-KLO')['outer'], uvt(m, 'C4T-KHI')['outer'] = b, a
    resha(m, 'C4T-KLO'); resha(m, 'C4T-KHI')


def c4ta_alias(m):
    uvt(m, 'C4T-A')['lambda_scale'] = 1.0
    resha(m, 'C4T-A')


def c5c_kout6(m):
    uvt(m, 'C4T-C5c')['outer']['K_out_inverse_kpc'] = 6.0
    resha(m, 'C4T-C5c')


def s4t_cube(m):
    m['cases']['S4T']['truncation'] = {'shape': 'cube', 'kmax_inverse_kpc': None}


def d5_continuum(m):
    uvt(m, 'C4T-D5')['source_rule'] = 'continuum_v001'
    resha(m, 'C4T-D5')


MUT = [
    ('schema_is_the_draft_C2V002', lambda m: m.__setitem__('schema', 'UNT_KMAX_TAIL_V007_CASE_BLOCK_C2V002')),
    ('case_C4T-A_missing', lambda m: m['cases'].pop('C4T-A')),
    ('retired_label_C4T-K64_for_C4T-KHI', lambda m: m['cases'].__setitem__('C4T-K64', m['cases'].pop('C4T-KHI'))),
    ('drivers_allowed_r4_b9ae92d5', lambda m: m['cases']['C2T'].__setitem__('drivers_allowed', [M.R4_CUSTODY_SHAS['driver']])),
    ('gas_M_s_64_everywhere_shas_recomputed', ms64),
    ('KLO_KHI_outer_swapped_shas_recomputed', swap_klo_khi),
    ('C4T-A_lambda_scale_1_alias_of_C4T', c4ta_alias),
    ('C4T-C5c_K_out_6', c5c_kout6),
    ('C4T-D5_source_rule_continuum', d5_continuum),
    ('uv_tail_config_sha_tampered_C6T', lambda m: m['cases']['C6T'].__setitem__('uv_tail_config_sha256', '0' * 64)),
    ('C5H_call_spec_tampered', lambda m: m['cases']['C5H'].__setitem__('call_spec_sha256', '1' * 64)),
    ('unknown_case_entry_key', lambda m: m['cases']['C3T'].__setitem__('status', 'x')),
    ('unknown_top_level_key', lambda m: m.__setitem__('extra', 1)),
    ('seed_source_rtol_factor_0.1_C4T', lambda m: m['cases']['C4T']['normalized_spec_equal']['/numerics']['route_a'].__setitem__('seed_source_rtol_factor', 0.1)),
    ('route_a_mode_unknown', lambda m: m.__setitem__('route_a_mode', 'parallel6')),
    ('C4T-D5_picard_passes_7_differs_from_C5H', lambda m: m['cases']['C4T-D5']['normalized_spec_equal']['/numerics']['picard'].__setitem__('passes', 7)),
    ('C2T_brackets_rfs_factor_changed', lambda m: m['cases']['C2T']['normalized_spec_equal']['/numerics']['brackets']['rule'].__setitem__('rfs_factors', [0.8, 1.21])),
    ('key_map_pointer_into_uv_tail', lambda m: m.__setitem__('key_equivalence_map', [{'pointer': '/numerics/uv_tail/lambda_scale', 'absent_equivalent_value': 1.0, 'b0_identity_evidence': 'x'}])),
    ('key_map_pointer_twice', lambda m: m.__setitem__('key_equivalence_map', [{'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0, 'b0_identity_evidence': 'x'}] * 2)),
    ('S4T_truncation_cube', s4t_cube),
    ('C2T_tail_false', lambda m: m['cases']['C2T'].__setitem__('tail', False)),
    ('C4T_numerics_not_whole', lambda m: m['cases']['C4T'].__setitem__('normalized_spec_equal', {'/numerics/uv_tail': uvt(m, 'C4T')})),
]
OUT['mutations_must_refuse'] = [mutate(n, f) for n, f in MUT]
check('every_mutation_refused', all(x['refused'] for x in OUT['mutations_must_refuse']),
      [x['mutation'] for x in OUT['mutations_must_refuse'] if not x['refused']])

# ---- why the on-disk draft 6bf4ce5a reads CASE_BLOCK_INVALID (layered, in memory only)
draft = M.loads_strict(raw['draft_case_block'])
layers = {'L0_as_on_disk': M.validate_case_block(draft, route_a_mode='parallel8')}
d1 = copy.deepcopy(draft); d1['schema'] = M.CASE_BLOCK_SCHEMA
layers['L1_schema_set_to_C2V003'] = M.validate_case_block(d1, route_a_mode='parallel8')
d2 = copy.deepcopy(d1)
d2['cases']['C4T-KLO'] = d2['cases'].pop('C4T-K16'); d2['cases']['C4T-KHI'] = d2['cases'].pop('C4T-K64')
layers['L2_plus_retired_K16_K64_relabelled_KLO_KHI'] = M.validate_case_block(d2, route_a_mode='parallel8')
OUT['draft_diagnosis'] = {
    'draft': {'path': PINS['draft_case_block'][0], 'sha256': sha(raw['draft_case_block'])},
    'layers': {k: {'refused': bool(v), 'n_reasons': len(v), 'reasons': [x[:220] for x in v[:40]]} for k, v in layers.items()},
    'field_facts': {
        'schema': draft.get('schema'), 'case_labels': list(draft.get('cases', {})),
        'drivers_allowed_prefixes': sorted({x[:8] for e in draft['cases'].values() for x in e.get('drivers_allowed', [])}),
        'T_case_outer_K_big': {lab: (((e.get('normalized_spec_equal') or {}).get('/numerics') or {}).get('uv_tail') or {}).get('outer')
                               for lab, e in draft['cases'].items() if lab != 'C5H'},
        'T_case_gas': {lab: (((e.get('normalized_spec_equal') or {}).get('/numerics') or {}).get('uv_tail') or {}).get('gas')
                       for lab, e in draft['cases'].items() if lab != 'C5H'},
        'uv_tail_config_sha256_values': sorted({str(e.get('uv_tail_config_sha256'))[:24] for lab, e in draft['cases'].items() if lab != 'C5H'}),
        'C4T-D5_keys': sorted(draft['cases'].get('C4T-D5', {})), 'note': draft.get('note')}}
check('draft_reads_invalid_under_r12', bool(layers['L0_as_on_disk']))
OUT['fail'] = FAIL
OUT['loader_stat_guard'] = {'refused': L.GUARD['refused'], 'events': L.GUARD['events']}
OUT['verdict'] = 'CASE_BLOCK_VALID_UNDER_R12' if not FAIL and OUT['case_block'].get('sha256') else 'NOT_BUILT'
with open(RES_OUT, 'x') as f:
    f.write(json.dumps(OUT, indent=1, ensure_ascii=False, allow_nan=False) + '\n')
print('verdict', OUT['verdict'], '| case block', OUT['case_block'], '| fails', FAIL)
print('mutations refused %d/%d' % (sum(1 for x in OUT['mutations_must_refuse'] if x['refused']), len(OUT['mutations_must_refuse'])))
print('draft layers', {k: len(v) for k, v in layers.items()}, '| stat guard refused', L.GUARD['refused'])
print('results', RES_OUT, hashlib.sha256(RES_OUT.read_bytes()).hexdigest())
