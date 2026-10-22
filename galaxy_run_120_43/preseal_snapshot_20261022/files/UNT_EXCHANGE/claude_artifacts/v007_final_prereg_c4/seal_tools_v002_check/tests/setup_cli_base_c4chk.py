# Claude4 helper: build a CLI test base for seal tools v002 r2 (compare r13 f5adfd11 = compare of record under A104; prereg r5
# with path_to_be moved into the run folder; the open V005 bytes now as the frozen copy) and write CLI_BASE_MANIFEST.json.
# Writes only into a new run folder here. Run under tools/run_fenced_c4chk.py.
import copy, hashlib, importlib.util, json, os, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R2 = CA / 'v007_final_prereg_c4/seal_tools_v002/r2'
sys.path.insert(0, str(R2))
import seal_common_c4v002 as C
import check_sealed_compare_c4v002 as T2
import check_slot_fill_c4v002 as T3
import build_seal_record_c4v002 as T4
import print_driver_build_record_c4v002 as T5
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
OPEN_ADD = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
FROZEN_NAME = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md'
R5 = CA / 'v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'
R13 = CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'
R13_SHA = 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
R13_IMPL = CA / 'v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md'
PKT = CA / 'v007_launch_packet_cx1'
T_ = CA / 'tail_scheme_impl_c2'
DRIVER = T_ / 'driver_r5/galaxy_m0_forward_c2v010.py'
CHECK_MD = T_ / 'driver_r5/check/CHECK.md'
assert C.sha(R13) == R13_SHA and C.sha(R5) == '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393'


def pin(p):
    return {'path': str(Path(p)), 'sha256': C.sha(p)}


def rpin(p):
    p = Path(os.path.realpath(p))
    return {'path': str(p), 'sha256': C.sha(p)}


run = HERE / ('cli_base_' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()))
run.mkdir()
run = Path(os.path.realpath(run))


def xw(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'x', encoding='utf-8') as f:
        f.write(data if isinstance(data, str) else json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    return p


M = C.load_reviewed_compare(str(R13), R13_SHA)
ob = OPEN_ADD.read_bytes()
frozen = xw(run / 'frozen' / FROZEN_NAME, ob.decode('utf-8'))
r5 = json.loads(R5.read_bytes())
r5['seal_slots']['frozen_addendum']['path_to_be'] = str(frozen)
tor = xw(run / 'KMAX_TAIL_PREREG_V007_R5S_C4CHK.json', json.dumps(r5, indent=1, ensure_ascii=False) + '\n')
res, text = T5.record_bytes(str(R13), R13_SHA, str(CHECK_MD))
assert res['verdict'] == 'PASS', res
dbr = xw(run / 'DRIVER_BUILD_R5_C4CHK.json', text)
sys.path.insert(0, str(PKT))
bspec = importlib.util.spec_from_file_location('bind_sealed_launch_plan_cx1v001', PKT / 'bind_sealed_launch_plan_cx1v001.py')
B = importlib.util.module_from_spec(bspec)
bspec.loader.exec_module(B)
B.HERE = run
plan_p, cmd_p = run / 'BOUND_PLAN_V011_C4CHK.json', run / 'BOUND_COMMAND_V011_C4CHK.txt'
B.bind(str(PKT / 'P128/LAUNCH_PLAN_V011_CX3V001.json'), str(DRIVER), C.sha(DRIVER), str(frozen), C.sha(frozen), str(plan_p), str(cmd_p))
plan = json.loads(plan_p.read_bytes())
cma = xw(run / 'CASCADE_MAP_R5_ADDENDUM_STANDIN_C4CHK.md', '# CASCADE_MAP_R5_ADDENDUM stand-in (Claude4 helper synthetic test input)\n\nExtends %s (%s).\n'
         % (M.PIN_R5_CASCADE_MAP[0], M.PIN_R5_CASCADE_MAP[1]))
nm = r5['seal_slots']
cn = nm['certificates']['named_candidates_verified_from_bytes']
slots = {'schema': T3.SCHEMA, 'driver_branch': 'r5', 'ngc_gas_M_s': 96, 'frozen_addendum': dict(plan['frozen_addendum']), 'driver': dict(plan['driver']),
         'driver_build_record': rpin(dbr), 'driver_check_record': pin(CHECK_MD), 'compare_reviewed_source': pin(R13),
         'identity_comparator': nm['identity_comparator']['named_candidates_verified_from_bytes']['c2v007r2'],
         'identity_gate_records': {k: nm['identity_gate_records']['named_candidates_verified_from_bytes'][k] for k in ('Z2', 'Z2_OFF_RO1', 'B0prime_RERUN')},
         'launch_packet': {'build': nm['launch_packet']['named_candidates_verified_from_bytes']['build'], 'bound_plan': rpin(plan_p), 'bound_command': rpin(cmd_p)},
         'certificates': {'EPS': cn['EPS'], 'LO': cn['LO'], 'GQ': cn['GQ'], 'DOUBLING': cn['DOUBLING_merged'], 'EPS_NGC': cn['EPS_NGC_91'], 'LO_NGC': cn['LO_NGC'],
                          'I1T_NGC': cn['I1T_NGC']},
         'producer_registry': {k: nm['producer_registry']['named_candidates_verified_from_bytes']['C3V009_candidate'][k] for k in ('path', 'sha256')},
         'cache_directory_r6_only': T3.NOT_APPLICABLE_R5, 'cascade_map_r5_addendum': rpin(cma),
         'admission_entry': {'launcher': dict(plan['launcher']), 'guard': dict(plan['guard'])}}
slots_p = xw(run / 'SLOTS_C4CHK.json', slots)
d = json.loads(tor.read_bytes())
for pk, sk in T3.PREREG_SLOT_OF.items():
    d['seal_slots'][pk]['value'] = copy.deepcopy(slots[sk])
sp = xw(run / 'KMAX_TAIL_PREREG_V007_SEALED_C4CHK.json', json.dumps(d, indent=1, ensure_ascii=False) + '\n')
exp = T2.expected_pins(slots, sp)
lines = []
for ln in R13.read_bytes().decode('utf-8').splitlines(keepends=True):
    n_ = next((n for n in C.PIN_NAMES if ln.startswith(n + ' = None')), None)
    if n_:
        ln = '%s = %r%s' % (n_, exp[n_], ln[len(n_ + ' = None'):])
    lines.append(ln)
sc = xw(run / 'kmax_tail_compare_c2v007_r13_SEALED_C4CHK.py', ''.join(lines))
scs = C.sha(sc)
hit = []
gates = {}
shas = {'EPS': slots['certificates']['EPS']['sha256'], 'LO': slots['certificates']['LO']['sha256'], 'GQ': slots['certificates']['GQ']['sha256'],
        'DOUBLING': slots['certificates']['DOUBLING']['sha256'], 'LO_NGC': slots['certificates']['LO_NGC']['sha256'], 'B1': slots['identity_gate_records']['Z2']['sha256'],
        'B1_OFF': slots['identity_gate_records']['Z2_OFF_RO1']['sha256'], 'B0prime_RERUN': slots['identity_gate_records']['B0prime_RERUN']['sha256']}
for g in M.ALL_GATES:
    gates[g] = M.blinded_gate({'gate': g, 'status': 'PASS', 'codes': [], 'fields_read': ['verdict'], 'record': {'sha256': shas[g]} if g in shas else None, 'crossref': {}})
gb = {'schema': M.SCHEMA_REPORT + '_GATES_ONLY', 'blinded': True, 'statement': 'gate statuses and reason codes only; case results read by sha256 of their bytes only; no row value '
      'or record number is written or printed', 'test_mode': False, 'route_a_mode': 'parallel8', 'script_sha256': scs, 'gates': gates, 'mt_crosscheck': 'NOT_APPLICABLE',
      'identity_runs': M.blind_strings({n: {'valid': True, 'codes': []} for n in M.IDENTITY_RUNS}, hit)}
gb['blinding_redaction_applied'] = bool(hit)
M.assert_no_numbers(gb)
v = {'label': 'C5H', 'present': True, 'valid_all': True, 'failed': [], 'reading': None, 'V1_codes': [], 'V2_codes': [], 'V3_mismatch': [], 'V6_codes': [], 'misses': [],
     'V1': True, 'ro1': {}, 'uvt': {}}
vb = {'schema': M.SCHEMA_REPORT + '_VALIDITY_ONLY', 'blinded': True, 'statement': 'validity/admissibility booleans and reason codes only; no row value, speed or other '
      'number is written or printed (A47 I3)', 'test_mode': False, 'route_a_mode': 'parallel8', 'script_sha256': scs, 'cases': {'C5H': M.blinded_case(v)},
      'I1T_gate': gates['I1T'], 'B0_gate': gates['B0']}
M.assert_no_numbers(vb)
g_p = xw(run / 'b6_gates' / 'GATES_ONLY.json', json.dumps(gb, indent=1) + '\n')
v_p = xw(run / 'b6_validity' / 'VALIDITY_ONLY.json', json.dumps(vb, indent=1) + '\n')
k_p = xw(run / 'KEY_EQUIVALENCE_MAP_C4CHK.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': [], 'note': 'synthetic test input'})
n_p = xw(run / 'NEW_ITEM_DISPOSITIONS_C4CHK.json', {'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': pin(R13_IMPL),
                                                     'items': [{'id': 'NEW-73', 'disposition': 'ADOPTED', 'reason': 'synthetic test row', 'must_fail_tests': ['T_X']}]})
c_p = xw(run / 'RAW_SUCCESSOR_CUSTODY_C4CHK.json', {'schema': T4.CUSTODY_SCHEMA, 'identity_run': 'Z2', 'driver_sha256': C.sha(DRIVER), 'stages_total': 21,
                                                     'stages_successor': 21, 'verdict': 'PASS', 'method': 'synthetic test input'})
heads = sorted({int(x) for x in __import__('re').findall(r'^## A(\d{1,3}):', ob.decode('utf-8'), __import__('re').M)})
man = {'run': str(run), 'open_v005_sha256': C.sha_bytes(ob), 'frozen': str(frozen), 'frozen_sha256': C.sha(frozen), 'tor': str(tor), 'tor_sha256': C.sha(tor),
       'slots': str(slots_p), 'sealed_prereg': str(sp), 'reviewed': str(R13), 'reviewed_sha256': R13_SHA, 'sealed_compare': str(sc), 'sealed_compare_sha256': scs,
       'check_md': str(CHECK_MD), 'gates_only': str(g_p), 'validity_only': str(v_p), 'key_map': str(k_p), 'new_items': str(n_p), 'custody': str(c_p),
       'b2': str(CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V003.json'), 'covered_later': ','.join('A%d' % n for n in heads if n > 101)}
xw(run / 'CLI_BASE_MANIFEST.json', man)
print(json.dumps(man, indent=1))
