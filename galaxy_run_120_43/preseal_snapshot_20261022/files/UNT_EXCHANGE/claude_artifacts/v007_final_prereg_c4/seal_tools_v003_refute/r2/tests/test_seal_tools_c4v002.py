# Claude4 seal tools v002: tamper tests for the five seal tools. Successor of test_seal_tools_c4v001.py (9011e825): the 40 v001 cases
# are ported (each tagged PORT; one changed expectation is tagged PORT_CHANGED and explained), every v002 fix gets MUST_FAIL cases
# (tagged NEW), and positive cases run on the real records (tagged REAL): DOUBLING ea48ac2b, CHECK.md 89a6de88, the A92 identity
# records, the real certificates, the real on-disk draft case block, the real B2 record of record, the selected r12 itself, and the
# real BUILD_V007 94bc05a5 (landed 20:44:19Z) with a plan bound from its own template. Fixtures are built under tests/run_<UTC>/:
#  - the open V005 addendum, read now (fence exception (b)), copied as the FROZEN copy;
#  - a SYNTHETIC prereg r5 STAND-IN (from the real r4 text: binding_inputs.case_block, a named BUILD, path_to_be in the run folder,
#    an entries_after_A81 table in the r5 form with section shas read from the frozen bytes, a B2-disclosure requirement); it is
#    not the prereg r5 of record;
#  - a case block built in-process by Claude3's recipe (validate_registry_r12_c3v002.py) from the ten DRY_R5_MS128_V004 dry reports,
#    validated by the reviewed compare's own validate_case_block;
#  - the r5 driver BUILD record printed by tool 5 (builtin_r5_build + CHECK.md), admitted by the compare's activate_driver_build;
#  - a SYNTHETIC BUILD_V007 STAND-IN with the 15 BUILD_V006 sources (verified from bytes) and a test template whose output paths
#    lie in the run folder (no runs_ext path is ever stat'ed); plans bound by the REAL binder (HERE patched to the run folder);
#  - a SYNTHETIC CASCADE_MAP_R5_ADDENDUM stand-in, synthetic B6 bodies in the r12 format and B7 inputs in the v002 schemas.
# Integration: the built SEAL_RECORD passes the v002 admission-config check and is fed to the REAL guard v008 / launcher v007 (CONFIG
# and REGISTERED patched in-process to synthetic files before any guard call; validate() only; nothing is started). The real
# BUILD_V007 case runs the guard's admission() only (its template's outputs are internal-volume paths, which are never stat'ed here).
# Run inside tools/run_fenced_c4st2.py (fence_c4v002). A local audit hook also refuses process creation, network, deletes and any
# write outside the run folder.
# usage: python3 -I -B ../tools/run_fenced_c4st2.py test_seal_tools_c4v002.py
import os, sys
RUNROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def _hook_factory(root_holder):
    def hook(event, args):
        if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty', 'pty.spawn', 'os.kill',
                     'socket.connect', 'socket.bind', 'os.remove', 'os.rmdir', 'shutil.rmtree'):
            raise PermissionError('TEST_FENCE ' + event)
        if event == 'open' and len(args) >= 2:
            p, mode, flags = args[0], args[1], (args[2] if len(args) > 2 else 0)
            writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
            if writing and isinstance(p, (str, bytes, os.PathLike)):
                real = os.path.realpath(os.path.abspath(os.fsdecode(p)))
                if not real.startswith(root_holder[0] + os.sep):
                    raise PermissionError('TEST_FENCE write outside run folder: ' + real)
        if event in ('os.mkdir', 'os.symlink', 'os.link', 'os.rename') and args:
            p = args[1] if event in ('os.symlink', 'os.link', 'os.rename') else args[0]
            real = os.path.realpath(os.path.abspath(os.fsdecode(p)))
            if not real.startswith(root_holder[0] + os.sep):
                raise PermissionError('TEST_FENCE %s outside run folder: %s' % (event, real))
    return hook


ROOT_HOLDER = [RUNROOT]
sys.addaudithook(_hook_factory(ROOT_HOLDER))

import contextlib, copy, hashlib, importlib.machinery, importlib.util, io, json, re, shlex, time
from pathlib import Path
TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import seal_common_c4v002 as C
import check_frozen_addendum_c4v002 as T1
import check_sealed_compare_c4v002 as T2
import check_slot_fill_c4v002 as T3
import build_seal_record_c4v002 as T4
import print_driver_build_record_c4v002 as T5

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
R4 = CA / 'v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json'
R5 = CA / 'v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'     # prereg r5 as landed (FROM_CLAUDE4/0103), not yet ruled of record
OPEN_ADD = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
PKT = CA / 'v007_launch_packet_cx1'
T = CA / 'tail_scheme_impl_c2'
R12 = CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'
R12_SHA = '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'
R12_IMPL = CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md'
DRIVER = T / 'driver_r5/galaxy_m0_forward_c2v010.py'
CHECK_MD = T / 'driver_r5/check/CHECK.md'
IDENT = T / 'gates_v007/r2/records/R5_V001'
COMPARATOR = T / 'gates_v007/r2/run_identity_compare_c2v007.py'
REGISTRY = CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V008.json'
REGISTRY_V007 = CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V007.json'
B2_REC = CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V003.json'
B2_REC_V002 = CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V002.json'
BUILD_V007 = PKT / 'BUILD_V007.md'
TEMPLATE_V011 = PKT / 'P128/LAUNCH_PLAN_V011_CX3V001.json'
DRAFT_CASE_BLOCK = T / 'driver/out/CASE_BLOCK_V007_DRAFT_C2V001.json'
CERTS = {'EPS': T / 'certificates_v002/gates/EPS_CERT_V006.json', 'LO': T / 'certificates_v004/gates/LO_CERT_V004_MS128.json',
         'GQ': CA / 'producer_registry_c3/out/GQ_CERT_V006.json', 'DOUBLING': CA / 'producer_registry_c3/out/DOUBLING_MERGED_C3V001.json',
         'EPS_NGC': T / 'certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json', 'LO_NGC': T / 'certificates_v002/gates/LO_NGC_CERT_V002.json',
         'I1T_NGC': T / 'certificates_v002/gates/I1T_NGC_T120L_V001.json'}
IDENTITY_FILES = {'Z2': IDENT / 'B1_R5_C2V007.json', 'Z2_OFF_RO1': IDENT / 'B1_OFF_R5_C2V007.json', 'B0prime_RERUN': IDENT / 'B0prime_RERUN_R5_C2V007.json'}
REAL_SHAS = {CERTS['DOUBLING']: 'ea48ac2bc429a1b6f7ae9b2cf96964a42bbedfd64afab21f724259114d8b0f7b',
             CHECK_MD: '89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632',
             IDENTITY_FILES['Z2']: '83e7b0673159156832995a1d7caae401a430918cbd110975bac8e18335aedc72',
             IDENTITY_FILES['Z2_OFF_RO1']: '3b9ad4029a8673eabfa87b2fe77ea66241589412291c44af5d0b220a6fad3df2',
             IDENTITY_FILES['B0prime_RERUN']: 'e33af53d1df36d858ed887bc4ed24fae77fe606d88ab26e2a77d9e5481d09258',
             R12: R12_SHA, DRAFT_CASE_BLOCK: '6bf4ce5a4219d281fa480d4249e818e8d9fc39779b3ad605e1a069f42e0da4c1',
             B2_REC: '915fbcda4f4a2cb5f61b257ff83494738144e177401c11c94e254c322df2411c',
             BUILD_V007: '94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de',
             TEMPLATE_V011: '1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c',
             REGISTRY: 'f189cd3fcd45426c23ba8600104a0a2ebf8ca7bcb453327aae19e6ebc1ee1120',
             R5: '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393'}
GATES_SCHEMA = 'UNT_KMAX_TAIL_COMPARISON_C2V007_R11'
B2_TEXT = ('The seal record repeats the B2 disclosure block of the B2 record of record (A100) and A101\'s erratum. SYNTHETIC test text in the '
           'r5 stand-in; the requirement of record is prereg r5\'s.')


def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': C.sha(p)}


def rpin(p):
    p = Path(os.path.realpath(p))
    return {'path': str(p), 'sha256': C.sha(p)}


def xw(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'x') as f:
        f.write(data if isinstance(data, str) else json.dumps(data, indent=1))
    return p


def main():
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    run = Path(RUNROOT) / ('run_' + stamp)
    run.mkdir()
    ROOT_HOLDER[0] = os.path.realpath(str(run))
    run = Path(ROOT_HOLDER[0])
    results = []

    def record(tool, name, res, expect_pass, code=None, absent=None, tag='NEW', note=None):
        codes = [f['code'] for f in res.get('failures', [])]
        notes = [n['code'] for n in res.get('notes', [])]
        ok = (res['verdict'] == 'PASS') if expect_pass else (res['verdict'] == 'REFUSE' and (code is None or any(code in c for c in codes)))
        if absent:
            ok = ok and not any(absent in c for c in codes)
        if note:
            ok = ok and note in notes
        results.append({'tool': tool, 'tag': tag, 'case': name, 'expect': 'PASS' if expect_pass else 'REFUSE ' + (code or ''), 'verdict': res['verdict'],
                        'codes': codes, 'notes': sorted(set(notes)), 'ok': ok})

    def check(tool, name, ok, detail, tag='NEW'):
        results.append({'tool': tool, 'tag': tag, 'case': name, 'expect': 'TRUE', 'verdict': 'PASS' if ok else 'FAIL', 'codes': [] if ok else [detail],
                        'notes': [], 'ok': bool(ok)})
    # ---------------- real inputs, from bytes
    for p, h in REAL_SHAS.items():
        assert C.sha(p) == h, p
    M = C.load_reviewed_compare(str(R12), R12_SHA)
    # ---------------- fixtures: frozen copy (fence exception (b): the open V005 addendum is read here), reviewed source copy
    frozen = xw(run / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', OPEN_ADD.read_bytes().decode('utf-8'))
    ftext = frozen.read_bytes().decode('utf-8')
    heads = sorted({int(n) for n in re.findall(r'^## A(\d{1,3}):', ftext, re.M)})
    NMAX = max(heads)
    assert all(n in heads for n in range(47, NMAX + 1)), 'the frozen copy has a gap in A47..A%d' % NMAX
    COV = ['A%d' % NMAX]
    SECS = T1.sections(frozen.read_bytes())
    reviewed = xw(run / 'reviewed_compare_r12_copy.py', R12.read_bytes().decode('utf-8'))
    assert C.sha(reviewed) == R12_SHA
    # ---------------- the case block (Claude3 recipe), validated by r12's own validate_case_block
    dry = json.loads((PKT / 'DRY_R5_MS128_V004.json').read_bytes())
    nums = {}
    for c in dry['checks']:
        b = Path(c['report']['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == c['report']['sha256'] and c['passed'] and c['executed_stages'] == 0
        nums[c['case']] = json.loads(b)['normalized_spec']['numerics']
    # ---------------- tool 5: the driver BUILD record (builtin_r5_build + CHECK.md), printed bytes
    r5res, r5text = T5.record_bytes(str(R12), R12_SHA, str(CHECK_MD))
    record('T5', 'tool 5 prints an admissible r5 driver BUILD record with the real CHECK.md 89a6de88 (D-06)', r5res, True, tag='REAL')
    dbr = xw(run / 'DRIVER_BUILD_R5_TEST_FIXTURE_C4ST2.json', r5text)
    LIB = M.load_uvt_lib()
    M.activate_driver_build(json.loads(r5text))
    KEYMAP = [{'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0,
               'b0_identity_evidence': 'SYNTHETIC test row: absent means 1.0 (A48 AMB-14); not the key map of record'}]

    def case_block(mutate=None, keymap=KEYMAP):
        cb = {'schema': M.CASE_BLOCK_SCHEMA, 'route_a_mode': 'parallel8', 'cases': {}, 'note': 'SYNTHETIC TEST FIXTURE (Claude4 seal tools v002); not the V007 case block of record'}
        if keymap is not None:
            cb['key_equivalence_map'] = keymap
        for lab in M.REGISTERED:
            e = {'grid': M.EXPECTED_GRID[lab], 'truncation': M.EXPECTED_TRUNCATION[lab], 'normalized_spec_equal': {}}
            if lab == M.C5H:
                e.update(tail=False, ro1_required=False, call_spec_sha256=M.PIN_C5H_SPEC[1], drivers_allowed=[M.DRIVER_V009_EXT])
            else:
                n = copy.deepcopy(nums[lab])
                e.update(tail=True, ro1_required=True, uv_tail_config_sha256=LIB.normalize_config(n['uv_tail'])['sha256'],
                         drivers_allowed=[M.sealed_driver_sha()], normalized_spec_equal={'/numerics': n})
            cb['cases'][lab] = e
        if mutate:
            mutate(cb)
        return cb
    cb0 = case_block()
    assert M.validate_case_block(cb0, route_a_mode='parallel8') == [], 'fixture case block refused'
    cbf = xw(run / 'CASE_BLOCK_TEST_FIXTURE_C4ST2.json', json.dumps(cb0, indent=1, sort_keys=True) + '\n')
    # ---------------- the BUILD_V007 stand-in, the test template and the bound plans
    v6 = (PKT / 'BUILD_V006.md').read_bytes().decode('utf-8')
    allow6 = C.build_allowlist(v6)
    assert len(allow6) == 15
    sys.path.insert(0, str(PKT))
    gspec = importlib.util.spec_from_file_location('producer_guard_cx1v008', PKT / 'producer_guard_cx1v008.py')
    G = importlib.util.module_from_spec(gspec)
    sys.modules['producer_guard_cx1v008'] = G
    gspec.loader.exec_module(G)
    G.REGISTERED = (run / 'synthetic_registered_A' / G.C5H_NAME, run / 'synthetic_registered_B' / G.C5H_NAME)   # before any guard call
    G.CONFIG = run / 'NO_CONFIG_YET.json'
    lspec = importlib.util.spec_from_file_location('route_a_token_launcher_cx1v007', PKT / 'route_a_token_launcher_cx1v007.py')
    L = importlib.util.module_from_spec(lspec)
    lspec.loader.exec_module(L)
    tpl = json.loads((PKT / 'P128/LAUNCH_PLAN_V010.json').read_bytes())
    outs = run / 'launch_outputs'
    tpl['launcher_log'] = str(outs / 'KMAX_V007_LAUNCHER_TEST.log')
    for x in tpl['calls']:
        base = os.path.basename(x['outdir'])
        x['outdir'] = str(outs / base)
        x['receipt'] = str(outs / (base + '.receipt.json'))
        x['monitor_log'] = str(outs / (base + '.monitor.log'))
        x['monitor_argv'] = L.monitor_argv.__wrapped__(tpl, x)
    tpl['label'] = 'SYNTHETIC TEST TEMPLATE (Claude4 seal tools v002): the r5 template with every output path moved into the test run folder'
    template = xw(run / 'LAUNCH_PLAN_V010_TEST_TEMPLATE_C4ST2.json', json.dumps(tpl, indent=1) + '\n')

    def build_v007(name='BUILD_V007.md', sub='build_v007_standin', entries=None):
        ents = allow6 if entries is None else entries
        body = ('# BUILD_V007 -- SYNTHETIC STAND-IN (Claude4 seal tools v002 tests; NOT the BUILD_V007 of record)\n\n'
                'Test fixture only: the 15 BUILD_V006 sources, verified from bytes, and the test template.\n\n'
                '## Supported runtime entry allowlist\n\n```text\n' + ''.join('%s  %s\n' % (h, p) for h, p in ents) + '```\n\n'
                '## Byte-pinned evidence and dependencies\n\n```text\n%s  %s\n```\n' % (C.sha(template), str(template.resolve())))
        return xw(run / sub / name, body)
    b7 = build_v007()
    B = importlib.util.module_from_spec(importlib.util.spec_from_file_location('bind_sealed_launch_plan_cx1v001', PKT / 'bind_sealed_launch_plan_cx1v001.py'))
    B.__spec__.loader.exec_module(B)
    B.HERE = run
    dsha = C.sha(DRIVER)
    plan_p, cmd_p = run / 'BOUND_PLAN_SYNTH.json', run / 'BOUND_COMMAND_SYNTH.txt'
    B.bind(str(template), str(DRIVER), dsha, str(frozen), C.sha(frozen), str(plan_p), str(cmd_p))
    plan = json.loads(plan_p.read_bytes())
    plan_r, cmd_r = run / 'BOUND_PLAN_REAL_V011.json', run / 'BOUND_COMMAND_REAL_V011.txt'
    B.bind(str(TEMPLATE_V011), str(DRIVER), dsha, str(frozen), C.sha(frozen), str(plan_r), str(cmd_r))
    planR = json.loads(plan_r.read_bytes())
    cma = xw(run / 'CASCADE_MAP_R5_ADDENDUM_TEST_STANDIN_C4ST2.json',
             {'schema': 'SYNTHETIC_CASCADE_MAP_R5_ADDENDUM_STANDIN', 'amends': {'path': M.PIN_R5_CASCADE_MAP[0], 'sha256': M.PIN_R5_CASCADE_MAP[1]},
              'note': 'SYNTHETIC test stand-in; the immutable inventory addendum of record is root\'s (A69)'})
    # ---------------- the prereg r5 STAND-IN (text of record for the tests)
    r4 = json.loads(R4.read_bytes())

    def table(entries, revised=('A82',), bad_sha=(), mutate_row=None):
        rows = []
        for e in entries:
            heading, sec = SECS[int(e[1:])][0]
            r = {'entry': e, 'heading': heading, 'section_sha256': ('9' * 64 if e in bad_sha else C.sha_bytes(sec)), 'section_bytes': len(sec)}
            if e in revised:
                r.update(decision='REVISED_HERE', revised_clauses=['seal_slots.compare'], scope='SYNTHETIC test row')
            else:
                r.update(decision='NO_CHANGE', revised_clauses=[], reason='no change, because SYNTHETIC test row (not the r5 table of record)')
            if mutate_row:
                mutate_row(r)
            rows.append(r)
        return {'rule': 'SYNTHETIC stand-in of the A99.3 table', 'section_rule': 'as prereg r5', 'rows': rows, 'sources': ['A81 RI-26', 'A99.3']}

    def text_of_record(name, build_sha='file', case_blk='fixture', ptb=None, tab=None, cites=NMAX - 1, mutate=None, build_path=None, b2=True):
        d = copy.deepcopy(r4)
        d['revision'] = 'r5-SYNTHETIC-STAND-IN'
        d['status'] = 'SYNTHETIC prereg r5 STAND-IN for the Claude4 seal tools v002 tests; not the prereg r5 of record'
        if case_blk == 'fixture':
            d['binding_inputs']['case_block'] = pin(cbf)
        elif case_blk is not None:
            d['binding_inputs']['case_block'] = case_blk
        bp = build_path or b7
        d['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']['build'] = {
            'path': str(bp), 'sha256': (C.sha(bp) if build_sha == 'file' else build_sha)}
        d['seal_slots']['launch_packet']['rule'] = d['seal_slots']['launch_packet']['rule'].replace('BUILD_V005 (46bc5b5d)', 'BUILD_V007')
        d['seal_slots']['frozen_addendum']['path_to_be'] = str(frozen.resolve()) if ptb is None else ptb
        d['cites_by_name'][0] = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A%d (open; pinned by its frozen copy, PENDING)' % cites
        t = table(['A%d' % n for n in range(82, cites + 1)]) if tab is None else tab
        if t != 'absent':
            d['entries_after_A81'] = t
        if b2:
            d['seal_record_requirements'].append({'text': B2_TEXT, 'sources': ['A100']})          # cites no entry after NMAX - 1
        if mutate:
            mutate(d)
        return xw(run / name, json.dumps(d, indent=1, ensure_ascii=False) + '\n')

    def use(tor):
        T3.TEXT_OF_RECORD_SHA = C.sha(tor)
        return tor
    TOR = text_of_record('KMAX_TAIL_PREREG_V007_R5_STANDIN_C4ST2.json')
    slots = {'schema': T3.SCHEMA, 'driver_branch': 'r5', 'ngc_gas_M_s': 96, 'frozen_addendum': dict(plan['frozen_addendum']), 'driver': dict(plan['driver']),
             'driver_build_record': rpin(dbr), 'driver_check_record': pin(CHECK_MD), 'compare_reviewed_source': rpin(reviewed),
             'identity_comparator': pin(COMPARATOR), 'identity_gate_records': {k: pin(v) for k, v in IDENTITY_FILES.items()},
             'launch_packet': {'build': pin(b7), 'bound_plan': rpin(plan_p), 'bound_command': rpin(cmd_p)},
             'certificates': {k: pin(v) for k, v in CERTS.items()}, 'producer_registry': pin(REGISTRY),
             'cache_directory_r6_only': T3.NOT_APPLICABLE_R5, 'cascade_map_r5_addendum': rpin(cma),
             'admission_entry': {'launcher': dict(plan['launcher']), 'guard': dict(plan['guard'])}}

    def sealed_prereg_for(sl, tor, name, mutate=None, fill=None):
        d = json.loads(Path(tor).read_bytes())
        for pk, sk in T3.PREREG_SLOT_OF.items():
            d['seal_slots'][pk]['value'] = copy.deepcopy(sl[sk])
        if fill is not None:
            d['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']['build']['sha256'] = fill
        if mutate:
            mutate(d)
        return xw(run / name, json.dumps(d, indent=1, ensure_ascii=False) + '\n')
    sp = sealed_prereg_for(slots, TOR, 'KMAX_TAIL_PREREG_V007_SEALED_SYNTH.json')
    slots_p = xw(run / 'SLOTS_SYNTH.json', slots)

    def sealed_compare_for(sl, prereg_path, name, edit=None, src=None):
        lines = Path(src or reviewed).read_bytes().decode('utf-8').splitlines(keepends=True)
        exp = T2.expected_pins(sl, prereg_path)
        out = []
        for ln in lines:
            nm = next((n for n in C.PIN_NAMES if ln.startswith(n + ' = None')), None)
            if nm:
                ln = '%s = %r%s' % (nm, exp[nm], ln[len(nm + ' = None'):])
            out.append(ln)
        if edit:
            out = edit(out)
        return xw(run / name, ''.join(out))
    sc = sealed_compare_for(slots, sp, 'sealed_compare_SYNTH.py')

    def T3run(sl_p, sp_p, tor_p, **kw):
        use(tor_p)
        return T3.run(sl_p, sp_p, tor_p, **kw)
    # ================= tool 1
    record('T1', 'genuine (later entry listed explicitly; r5-form entry table re-hashed from the frozen bytes)', T1.run(sp, frozen, None, COV), True, tag='PORT')
    f_a = xw(run / 'variant_a/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext.replace('## A60:', '## A60 (removed heading):'))
    record('T1', 'cited entry A60 absent', T1.run(sp, f_a, None, COV), False, 'CITED_ENTRY_ABSENT_FROM_FROZEN', tag='PORT')
    f_b = xw(run / 'variant_b/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext + '\n## A70: duplicate entry\n')
    record('T1', 'duplicate heading', T1.run(sp, f_b, None, COV), False, 'DUPLICATE_ENTRY_HEADING', tag='PORT')
    f_c = xw(run / 'variant_c/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext + '\nsealed prereg %s\n' % C.sha(sp))
    record('T1', 'frozen cites the sealed prereg sha', T1.run(sp, f_c, None, COV), False, 'FROZEN_CITES_SEALED_PREREG_SHA', tag='PORT')
    record('T1', 'later entry uncovered', T1.run(sp, frozen, None, []), False, 'UNCOVERED_LATER_ENTRY', tag='PORT')
    f_e = xw(run / 'variant_e/V005_ADDENDUM_COPY.md', ftext)
    record('T1', 'not the _FROZEN copy', T1.run(sp, f_e, None, COV), False, 'NOT_THE_FROZEN_COPY', tag='PORT')
    record('T1', 'expected sha differs', T1.run(sp, frozen, '0' * 64, COV), False, 'FROZEN_SHA_MISMATCH', tag='PORT')
    record('T1', 'covered-later names an absent entry', T1.run(sp, frozen, None, COV + ['A%d' % (NMAX + 5)]), False, 'COVERED_LATER_NOT_IN_FROZEN', tag='PORT')
    dup_json = xw(run / 'variant_h_prereg.json', sp.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "dup",\n "schema"', 1))
    record('T1', 'prereg JSON with a duplicate key', T1.run(dup_json, frozen, None, COV), False, 'PREREG_JSON', tag='PORT')
    # D-10
    f_d = xw(run / 'variant_d10/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext)
    record('T1', 'D-10: a FROZEN-named copy at a path other than path_to_be', T1.run(sp, f_d, None, COV), False, 'FROZEN_PATH_NOT_PATH_TO_BE')
    sp_noptb = sealed_prereg_for(slots, TOR, 'variant_noptb_prereg.json', mutate=lambda d: d['seal_slots']['frozen_addendum'].pop('path_to_be'))
    record('T1', 'D-10: a prereg without path_to_be', T1.run(sp_noptb, frozen, None, COV), False, 'FROZEN_PATH_TO_BE_ABSENT')
    record('T1', 'D-10: the dry-run flag records the path deviation as a note and never fails it', T1.run(TOR, f_d, None, COV, True), True,
           note='DRY_RUN_FROZEN_PATH_NOT_PATH_TO_BE')
    # D-05
    record('T1', 'D-05: --covered-later as a range', T1.run(sp, frozen, None, ['A82-A%d' % NMAX]), False, 'COVERED_LATER_FORMAT')
    record('T1', 'D-05: the stale README form --covered-later A82', T1.run(sp, frozen, None, ['A82']), False, 'COVERED_LATER_IS_CITED')
    record('T1', 'D-05: an entry listed twice', T1.run(sp, frozen, None, COV + COV), False, 'COVERED_LATER_DUPLICATE')
    # A99.3 entry table (r5 form)
    ents = lambda hi, skip=(): ['A%d' % n for n in range(82, hi + 1) if n not in skip]

    def t1_variant(name, **kw):
        tor = text_of_record('variant_%s.json' % name, **kw)
        return tor, sealed_prereg_for(slots, tor, 'variant_%s_sealed.json' % name)
    _, sp_t = t1_variant('table_missing_A90', tab=table(ents(NMAX - 1, (90,))))
    record('T1', 'A99.3: the entry table lacks A90', T1.run(sp_t, frozen, None, COV), False, 'ENTRY_TABLE_MISSING_ENTRY')
    _, sp_t = t1_variant('table_absent', tab='absent')
    record('T1', 'A99.3: no entry table', T1.run(sp_t, frozen, None, COV), False, 'ENTRY_TABLE_ABSENT')
    _, sp_t = t1_variant('table_has_later', tab=table(ents(NMAX)))
    record('T1', 'A99.3: a later entry with a table row and a no-change note', T1.run(sp_t, frozen, None, COV), False, 'COVERED_LATER_IN_ENTRY_TABLE')
    record('T1', 'A99.3: a later entry covered by its table row alone', T1.run(sp_t, frozen, None, []), True)
    _, sp_t = t1_variant('table_dup', tab=table(ents(NMAX - 1) + ['A85']))
    record('T1', 'A99.3: a table row repeated', T1.run(sp_t, frozen, None, COV), False, 'ENTRY_TABLE_DUPLICATE_ENTRY')
    tor_chg, sp_chg = t1_variant('table_A90_changed', tab=table(ents(NMAX - 1), bad_sha=('A90',)))
    record('T1', 'A99.3: a row whose section no longer re-hashes from the frozen bytes', T1.run(sp_chg, frozen, None, COV), False, 'ENTRY_TABLE_SECTION_CHANGED')
    record('T1', 'A99.3: the changed row with root\'s explicit seal-record note (--covered-later A90)', T1.run(sp_chg, frozen, None, ['A90'] + COV), True,
           note='ENTRY_TABLE_SECTION_CHANGED_NOTED')
    _, sp_t = t1_variant('table_bad_decision', tab=table(ents(NMAX - 1), mutate_row=lambda r: r.update(decision='MAYBE') if r['entry'] == 'A84' else None))
    record('T1', 'A99.3: a row whose decision is neither REVISED_HERE nor NO_CHANGE', T1.run(sp_t, frozen, None, COV), False, 'ENTRY_TABLE_MALFORMED')
    _, sp_t = t1_variant('table_revised_no_clauses', tab=table(ents(NMAX - 1), mutate_row=lambda r: r.update(revised_clauses=[]) if r['entry'] == 'A82' else None))
    record('T1', 'A99.3: a REVISED_HERE row naming no revised clause', T1.run(sp_t, frozen, None, COV), False, 'ENTRY_TABLE_MALFORMED')
    rows5 = json.loads(R5.read_bytes())['entries_after_A81']['rows']
    mism = [r['entry'] for r in rows5 if C.sha_bytes(SECS[int(r['entry'][1:])][0][1]) != r['section_sha256'] or len(SECS[int(r['entry'][1:])][0][1]) != r['section_bytes']]
    check('T1', 'REAL cross-check: tool 1\'s section rule reproduces every section_sha256 of prereg r5 3245899f (%d rows; an independent implementation)' % len(rows5),
          not mism, 'mismatched rows %r' % mism, tag='REAL')
    # ================= tool 2
    record('T2', 'genuine', T2.run(reviewed, sc, slots_p, sp), True, tag='PORT')

    def chg_nonpin(out):
        i = next(i for i, l in enumerate(out) if l.startswith('TOL') or l.startswith('ART = '))
        out[i] = out[i].rstrip('\n') + '  # tampered\n'
        return out
    record('T2', 'a non-pin line changed', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_a.py', chg_nonpin), slots_p, sp), False, 'NON_PIN_LINE_DIFFERS', tag='PORT')
    other_prereg = xw(run / 'other_prereg.json', '{}\n')
    record('T2', 'pin value for another prereg', T2.run(reviewed, sealed_compare_for(slots, other_prereg, 'sc_b.py'), slots_p, sp), False, 'PIN_VALUE_MISMATCH', tag='PORT')
    record('T2', 'inserted line', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_c.py', lambda o: o[:10] + ['# inserted\n'] + o[10:]), slots_p, sp), False, 'LINE_COUNT_DIFFERS', tag='PORT')

    def dup_assign(out):
        i = next(i for i, l in enumerate(out) if l.startswith('# ====') or l.startswith('#'))
        out[i] = "V007_PREREG_SHA256 = '%s'\n" % ('0' * 64)
        return out
    record('T2', 'second assignment of a pin', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_d.py', dup_assign), slots_p, sp), False, 'NON_PIN_LINE_DIFFERS', tag='PORT')

    def chg_comment(out):
        i = next(i for i, l in enumerate(out) if l.startswith('V007_PREREG_SHA256 = '))
        out[i] = out[i].replace('# PENDING_FROM_BYTES', '# EDITED')
        return out
    record('T2', 'pin comment changed', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_e.py', chg_comment), slots_p, sp), False, 'PIN_COMMENT_CHANGED', tag='PORT')

    def as_list(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_PRODUCER_REGISTRY = '))
        out[i] = 'PIN_PRODUCER_REGISTRY = %r\n' % [slots['producer_registry']['path'], slots['producer_registry']['sha256']]
        return out
    record('T2', 'pair pin as a list', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_f.py', as_list), slots_p, sp), False, 'PIN_PAIR_SHAPE', tag='PORT')

    def unset_one(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_V010_R5_CHECK = '))
        out[i] = 'PIN_V010_R5_CHECK = None\n'
        return out
    record('T2', 'one pin left unset', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_g.py', unset_one), slots_p, sp), False, 'PIN_NOT_SET', tag='PORT')
    rv_copy = xw(run / 'variant_reviewed_copy.py', reviewed.read_bytes().decode('utf-8'))
    record('T2', 'reviewed path not the slot', T2.run(rv_copy, sc, slots_p, sp), False, 'REVIEWED_PATH_NOT_THE_SLOT', tag='PORT')
    record('T2', 'sealed is the reviewed file', T2.run(reviewed, reviewed, slots_p, sp), False, 'SEALED_IS_REVIEWED', tag='PORT')
    sp_j = sealed_prereg_for(slots, TOR, 'variant_j_prereg.json', mutate=lambda d: d['seal_slots']['compare'].update(value=pin(sc)))
    record('T2', 'prereg compare slot holds the sealed compare', T2.run(reviewed, sealed_compare_for(slots, sp_j, 'sc_j.py'), slots_p, sp_j), False,
           'PREREG_COMPARE_SLOT_DIFFERS', tag='PORT')
    # D-07
    s_str_p = xw(run / 'slots_bare_pending_string.json', dict(slots, frozen_addendum='PENDING_ROOT_AT_SEAL_ASSEMBLY'))
    record('T2', 'D-07: a bare PENDING string slot refuses PIN_SHAPE (no TypeError)', T2.run(reviewed, sc, s_str_p, sp), False, 'PIN_SHAPE')
    s_lst_p = xw(run / 'slots_list_slot.json', dict(slots, driver_check_record=[str(CHECK_MD), C.sha(CHECK_MD)]))
    record('T2', 'D-07: a list slot refuses PIN_SHAPE', T2.run(reviewed, sc, s_lst_p, sp), False, 'PIN_SHAPE')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = T2.main(['--reviewed', str(reviewed), '--sealed', str(sc), '--slots', str(s_str_p), '--prereg', str(sp)])
    try:
        cli = json.loads(buf.getvalue())
    except ValueError:
        cli = {}
    check('T2', 'D-07: the CLI exits 2 with a REFUSE verdict JSON (the v001 crash was exit 1)', rc == 2 and cli.get('verdict') == 'REFUSE'
          and any(f['code'] == 'PIN_SHAPE' for f in cli.get('failures', [])), 'rc %r verdict %r' % (rc, cli.get('verdict')))
    # ================= tool 3
    record('T3', 'genuine r5 (real certificates, A92 identity records, CHECK.md, case block validated in-process)',
           T3run(slots_p, sp, TOR, frozen=frozen, covered_later=COV, reviewed=reviewed, sealed_compare=sc), True, tag='PORT')

    def variant(name, mutate, prereg_mutate=None, same_prereg=False, tor=None):
        s2 = copy.deepcopy(slots)
        mutate(s2)
        p2 = xw(run / ('slots_%s.json' % name), s2)
        sp2 = sp if same_prereg else sealed_prereg_for(s2, tor or TOR, 'prereg_%s.json' % name, prereg_mutate)
        return p2, sp2
    preg = Path(slots['producer_registry']['path'])
    p2, sp2 = variant('pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    record('T3', 'a PENDING value', T3run(p2, sp2, TOR), False, 'PENDING', tag='PORT')
    p2, sp2 = variant('badpin', lambda s: s['identity_gate_records']['Z2'].update(sha256='0' * 64))
    record('T3', 'identity record pin bytes differ', T3run(p2, sp2, TOR), False, 'PIN_BYTES_MISMATCH', tag='PORT')
    p2, sp2 = variant('text', lambda s: None, prereg_mutate=lambda d: d['tests']['T3'].update(text=d['tests']['T3']['text'] + ' (edited)'))
    record('T3', 'sealed prereg text changed outside the slots', T3run(p2, sp2, TOR), False, 'SEALED_PREREG_TEXT_CHANGED', tag='PORT')
    p2, _ = variant('slotdiff', lambda s: s.update(producer_registry=pin(CHECK_MD)), same_prereg=True)
    record('T3', 'prereg slot value differs from the slots', T3run(p2, sp, TOR), False, 'PREREG_SLOT_VALUE_DIFFERS', tag='PORT')
    alias = slots['driver']['path'].replace('/driver_r5/', '/driver_r5/./')
    p2, sp2 = variant('driveralias', lambda s: s.update(driver={'path': alias, 'sha256': dsha}))
    record('T3', 'driver slot spelled differently from the plan', T3run(p2, sp2, TOR), False, 'PLAN_DRIVER_NOT_THE_SLOT', tag='PORT')
    bad_id = xw(run / 'IDENTITY_Z2_WRONG_DRIVER.json', {'schema': M.GATE_SCHEMA, 'gate': 'B1', 'NEW_DRIVER_PIN': {'pass': True, 'detail': {'result_json_driver_sha256': '2' * 64}}})
    p2, sp2 = variant('iddriver', lambda s: s['identity_gate_records'].update(Z2=pin(bad_id)))
    record('T3', 'identity record carries another driver', T3run(p2, sp2, TOR), False, 'IDENTITY_RECORD', tag='PORT')
    lo64 = json.loads(CERTS['LO'].read_bytes())
    lo64['source_gas_M_s'] = 64
    lo64_p = xw(run / 'LO_CERT_M_S64_SYNTH.json', lo64)
    p2, sp2 = variant('lo64', lambda s: s['certificates'].update(LO=pin(lo64_p)))
    record('T3', 'LO certificate at M_s 64', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S', tag='PORT')
    cdir = run / 'cache_dir_nonempty'
    cdir.mkdir()
    xw(cdir / 'prewarmed.bin', 'x')
    p2, sp2 = variant('r6full', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir)}, cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    record('T3', 'r6 cache directory not empty (pre-warmed)', T3run(p2, sp2, TOR), False, 'CACHE_DIRECTORY_NOT_EMPTY', tag='PORT')
    cdir2 = run / 'cache_dir_empty'
    cdir2.mkdir()
    p2, sp2 = variant('r6empty', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir2)}, cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    record('T3', 'r6 with a fresh empty cache directory: the cache rule passes; v002 refuses only because the slot\'s driver BUILD record is r5 '
           '(v001 passed this; A96: V007 seals on r5)', T3run(p2, sp2, TOR), False, 'DRIVER_BUILD_NOT_THE_BRANCH', absent='CACHE_DIRECTORY', tag='PORT_CHANGED')
    p2, sp2 = variant('r5cache', lambda s: s.update(cache_directory_r6_only={'path': str(cdir2)}))
    record('T3', 'r5 slot set naming a cache directory', T3run(p2, sp2, TOR), False, 'CACHE_DIRECTORY_UNDER_R5', tag='PORT')
    cmd2 = xw(run / 'BOUND_COMMAND_EDITED.txt', cmd_p.read_bytes().decode('utf-8').replace('--execute-root-only', '--execute-root-only --worker'))
    p2, sp2 = variant('cmd', lambda s: s['launch_packet'].update(bound_command=rpin(cmd2)))
    record('T3', 'bound command edited', T3run(p2, sp2, TOR), False, 'BOUND_COMMAND_NOT_THE_BINDER_LINE', tag='PORT')
    dupslots = xw(run / 'slots_dupkey.json', slots_p.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "x",\n "schema"', 1))
    record('T3', 'slot JSON with a duplicate key', T3run(dupslots, sp, TOR), False, 'INPUT_JSON', tag='PORT')
    use(TOR)
    record('T3', 'text of record is not the pinned r5 (r4 given)', T3.run(slots_p, sp, R4), False, 'TEXT_OF_RECORD_NOT_R5', tag='PORT')
    p2, sp2 = variant('build6slot', lambda s: s['launch_packet'].update(build=pin(PKT / 'BUILD_V006.md')), same_prereg=True)
    record('T3', 'launch build not the prereg-named BUILD_V007 (slots name BUILD_V006)', T3run(p2, sp, TOR), False, 'BUILD_NOT_THE_PREREG_NAMED_BUILD', tag='PORT')
    # ---- D-01
    dbl = json.loads(CERTS['DOUBLING'].read_bytes())
    chk = C.Checker('x')
    n = T3.certificate_ms_codes(chk, 'DOUBLING', dbl, 128, 96)
    check('T3', 'D-01 REAL: DOUBLING ea48ac2b states its M_s only as ddo_gas_M_s; v002 reads it (1 field, no refusal)', n == 1 and not chk.failures,
          'n %d failures %r' % (n, chk.failures), tag='REAL')
    v1 = importlib.machinery.SourceFileLoader('check_slot_fill_c4v001_ref', str(CA / 'v007_final_prereg_c4/seal_tools/check_slot_fill_c4v001.py'))
    v1m = importlib.util.module_from_spec(importlib.util.spec_from_loader(v1.name, v1))
    sys.path.insert(0, str(CA / 'v007_final_prereg_c4/seal_tools'))
    v1.exec_module(v1m)
    check('T3', 'D-01 reproduction: the v001 scanner finds no M_s in the real DOUBLING record (the defect)', v1m.ms_values(dbl) == [], repr(v1m.ms_values(dbl)), tag='REAL')

    def cert_variant(name, kind, mutate):
        d = json.loads(CERTS[kind].read_bytes())
        mutate(d)
        f = xw(run / ('CERT_%s_SYNTH.json' % name), d)
        return variant('cert_' + name, lambda s: s['certificates'].update({kind: pin(f)}))
    p2, sp2 = cert_variant('dbl64', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=64))
    record('T3', 'D-01: DOUBLING ddo_gas_M_s 64 contradicts the registered M_s 128', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S')
    p2, sp2 = cert_variant('dblnoms', 'DOUBLING', lambda d: d.pop('ddo_gas_M_s'))
    record('T3', 'D-01: DOUBLING without ddo_gas_M_s', T3run(p2, sp2, TOR), False, 'CERTIFICATE_STATES_NO_M_S')
    p2, sp2 = cert_variant('dblngc128', 'DOUBLING', lambda d: d['ngc_half'].update(gas_M_s=128))
    record('T3', 'D-01: DOUBLING NGC half states M_s 128 against the ngc_gas_M_s slot 96', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S')
    p2, sp2 = cert_variant('dblngc96', 'DOUBLING', lambda d: d['ngc_half'].update(gas_M_s=96))
    record('T3', 'D-01: DOUBLING NGC half states M_s 96, consistent with the slot', T3run(p2, sp2, TOR, frozen=frozen, covered_later=COV), True)
    p2, sp2 = cert_variant('gqdbl', 'GQ', lambda d: d['rosters'][0].update(M_s_doubled=255))
    record('T3', 'D-01: GQ roster M_s_doubled is not 2 M_s', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S_DOUBLED')
    p2, sp2 = cert_variant('gqngc', 'GQ', lambda d: [r.update(M_s=128, M_s_doubled=256) for r in d['rosters'] if r['roster'] == 'NGC_T120L'])
    record('T3', 'D-01: GQ NGC_T120L roster at M_s 128 against the slot 96', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S')
    p2, sp2 = cert_variant('loecho', 'LO', lambda d: d['tail_config_gas'].update(M_s=64))
    record('T3', 'D-01: LO tail_config_gas.M_s 64 contradicts source_gas_M_s (A73 F2)', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S')
    p2, sp2 = cert_variant('ambig', 'EPS', lambda d: d.update(ddo_ngc_gas_M_s=128))
    record('T3', 'D-01: an M_s key naming both DDO and NGC', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S_CONTEXT_AMBIGUOUS')
    p2, sp2 = variant('certgate', lambda s: s['certificates'].update(LO=pin(CERTS['GQ'])))
    record('T3', 'a certificate slot holding another gate\'s record (LO slot = the GQ record)', T3run(p2, sp2, TOR), False, 'CERTIFICATE_NOT_THE_SLOT_GATE')
    p2, sp2 = variant('idgate', lambda s: s['identity_gate_records'].update(Z2=pin(IDENTITY_FILES['Z2_OFF_RO1'])))
    record('T3', 'an identity slot holding another gate\'s record (Z2 slot = the B1_OFF record)', T3run(p2, sp2, TOR), False, 'IDENTITY_RECORD_NOT_THE_SLOT_GATE')
    p2, sp2 = variant('ngc128', lambda s: s.update(ngc_gas_M_s=128))
    record('T3', 'ngc_gas_M_s 128 against the compare\'s NGC 96 (RI-23 needs a compare successor)', T3run(p2, sp2, TOR), False, 'NGC_GAS_M_S_NOT_THE_COMPARE_NGC_M_S')
    record('T3', 'ngc_gas_M_s 128: DOUBLING and LO_NGC must state the recomputed NGC M_s (RI-23)', T3run(p2, sp2, TOR), False, 'NGC_M_S_128_NOT_EVIDENCED')
    # ---- D-04 case block
    tor_x = text_of_record('variant_tor_no_case_block.json', case_blk=None)
    record('T3', 'D-04: no binding_inputs.case_block in the sealed prereg', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_no_case_block.json'), tor_x),
           False, 'CASE_BLOCK_PIN_ABSENT')
    tor_x = text_of_record('variant_tor_cb_wrong_sha.json', case_blk={'path': str(cbf), 'sha256': '0' * 64})
    record('T3', 'D-04: case block pin bytes differ', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_cb_wrong_sha.json'), tor_x), False, 'PIN_BYTES_MISMATCH')
    tor_x = text_of_record('variant_tor_cb_extra_key.json', case_blk=dict(pin(cbf), note='x'))
    record('T3', 'D-04: case block pin with an extra key', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_cb_extra_key.json'), tor_x), False, 'CASE_BLOCK_PIN_SHAPE')
    tor_x = text_of_record('variant_tor_draft_case_block.json', case_blk=pin(DRAFT_CASE_BLOCK))
    record('T3', 'D-04 REAL: the on-disk draft case block 6bf4ce5a refuses CASE_BLOCK_INVALID',
           T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_draft_case_block.json'), tor_x), False, 'CASE_BLOCK_INVALID', tag='REAL')
    cb64 = xw(run / 'CASE_BLOCK_MS64_SYNTH.json', json.dumps(case_block(lambda c: c['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['gas'].update(M_s=64)),
                                                         indent=1) + '\n')
    tor_x = text_of_record('variant_tor_cb_ms64.json', case_blk=pin(cb64))
    record('T3', 'D-04: a case block registering gas M_s 64 (r12 validate_case_block refuses it)',
           T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_cb_ms64.json'), tor_x), False, 'CASE_BLOCK_INVALID')
    tor_x = text_of_record('variant_tor_mode_serial.json', mutate=lambda d: d.update(route_a_mode='serial_with_exemption'))
    record('T3', 'D-04: the prereg and the case block name different route-A modes',
           T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_mode_serial.json'), tor_x), False, 'ROUTE_A_MODE_SOURCES_DIFFER')
    p2, sp2 = variant('nocma', lambda s: s.update(cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    record('T3', 'D-04: r5 without the CASCADE_MAP_R5_ADDENDUM pin (SRR[9])', T3run(p2, sp2, TOR), False, 'CASCADE_MAP_R5_ADDENDUM_REQUIRED_UNDER_R5')
    cma_bad = xw(run / 'CASCADE_MAP_R5_ADDENDUM_NOT_NAMING_THE_MAP_SYNTH.json', {'schema': 'SYNTHETIC', 'amends': 'nothing named'})
    p2, sp2 = variant('cmamap', lambda s: s.update(cascade_map_r5_addendum=rpin(cma_bad)))
    record('T3', 'D-04: a CASCADE_MAP_R5_ADDENDUM that does not name the r5 cascade map', T3run(p2, sp2, TOR), False, 'CASCADE_MAP_R5_ADDENDUM_DOES_NOT_NAME_THE_R5_MAP')
    cma_name = xw(run / 'INVENTORY_ADDENDUM_SYNTH.json', json.loads(cma.read_bytes()))
    p2, sp2 = variant('cmaname', lambda s: s.update(cascade_map_r5_addendum=rpin(cma_name)))
    record('T3', 'D-04: an addendum not named CASCADE_MAP_R5_ADDENDUM', T3run(p2, sp2, TOR), False, 'CASCADE_MAP_R5_ADDENDUM_NAME')
    other = next(({'path': p, 'sha256': h} for h, p in allow6 if p != plan['guard']['path'] and p != plan['launcher']['path']))
    p2, sp2 = variant('aeplan', lambda s: s['admission_entry'].update(guard=other))
    record('T3', 'D-04: the admission guard is not the bound plan\'s (SRR[10])', T3run(p2, sp2, TOR), False, 'ADMISSION_ENTRY_NOT_THE_PLAN')
    p2, sp2 = variant('aebuild', lambda s: s['admission_entry'].update(launcher=pin(PKT / 'route_a_token_launcher_cx1v006.py')))
    record('T3', 'D-04: the admission launcher is not a supported BUILD_V007 entry', T3run(p2, sp2, TOR), False, 'ADMISSION_ENTRY_NOT_BUILD_SUPPORTED')
    # ---- D-10
    tor_x = text_of_record('variant_tor_ptb_elsewhere.json', ptb=str(run / 'elsewhere' / frozen.name))
    record('T3', 'D-10: the frozen slot path is not path_to_be', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_ptb_elsewhere.json'), tor_x), False,
           'FROZEN_SLOT_NOT_PATH_TO_BE')
    # ---- A99.1 BUILD_V007
    tor_pend = text_of_record('variant_tor_build_pending.json', build_sha=C.PENDING_BUILD_V007)
    sp_pend = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_pending.json')
    record('T3', 'A99.1: BUILD_V007 still PENDING_BUILD_V007 (gap)', T3run(slots_p, sp_pend, tor_pend), False, 'BUILD_V007_PENDING')
    sp_fill = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_filled.json', fill=C.sha(b7))
    record('T3', 'A99.1: text holds PENDING_BUILD_V007; the sealed prereg fills that one leaf with the real sha', T3run(slots_p, sp_fill, tor_pend,
           frozen=frozen, covered_later=COV), True, note='BUILD_V007_SHA_FILLED_AT_SEAL')
    sp_x = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_fill_wrong.json', fill='1' * 64)
    record('T3', 'A99.1: a seal-time fill with a sha that is not the file\'s bytes', T3run(slots_p, sp_x, tor_pend), False, 'PIN_BYTES_MISMATCH')
    sp_x = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_fill_path.json', fill=C.sha(b7), mutate=lambda d: d['seal_slots']['launch_packet'][
        'named_candidates_verified_from_bytes']['build'].update(path=str(b7) + '.alt'))
    record('T3', 'A99.1: the seal-time fill may not change the path', T3run(slots_p, sp_x, tor_pend), False, 'SEALED_PREREG_TEXT_CHANGED')
    for nm in ('BUILD_V006.md', 'BUILD_V005.md'):
        tor_old = text_of_record('variant_tor_%s.json' % nm[:-3], build_path=PKT / nm)
        p2, sp_old = variant('old_' + nm[:-3], lambda s, nm=nm: s['launch_packet'].update(build=pin(PKT / nm)), tor=tor_old)
        record('T3', 'A99.1: the prereg names %s (not BUILD_V007)' % nm[:-3], T3run(p2, sp_old, tor_old), False, 'BUILD_NOT_BUILD_V007')
    for sub, ents_, code in (('build_v007_13', allow6[:13], 'BUILD_ALLOWLIST_COUNT_NOT_15'), ('build_v007_dup', allow6[:14] + [allow6[0]], 'BUILD_ALLOWLIST_DUPLICATE_PATH'),
                             ('build_v007_bytes', [('0' * 64, allow6[0][1])] + allow6[1:], 'BUILD_ALLOWLIST_SOURCE_BYTES')):
        bx = build_v007(sub=sub, entries=ents_)
        tor_x = text_of_record('variant_tor_%s.json' % sub, build_path=bx)
        p2, sp_x = variant(sub, lambda s, bx=bx: s['launch_packet'].update(build=pin(bx)), tor=tor_x)
        record('T3', 'A99.1: a BUILD_V007 %s' % {'build_v007_13': 'with 13 sources (V6-S3 needs 15)', 'build_v007_dup': 'listing one source twice',
                                                 'build_v007_bytes': 'entry whose sha is not its bytes'}[sub], T3run(p2, sp_x, tor_x), False, code)
    # ---- driver BUILD record (sealed-mode activation)
    p2, sp2 = variant('dcr', lambda s: s.update(driver_check_record=pin(CERTS['LO'])))
    record('T3', 'the driver BUILD record\'s check_record is not the driver_check_record slot', T3run(p2, sp2, TOR), False, 'DRIVER_BUILD_CHECK_RECORD_NOT_THE_SLOT')
    badb = json.loads(r5text)
    badb['ro1_custody']['worker']['sha256'] = '3' * 64
    badb_p = xw(run / 'DRIVER_BUILD_BAD_WORKER_SYNTH.json', json.dumps(badb, indent=1, sort_keys=True) + '\n')
    p2, sp2 = variant('dbrbad', lambda s: s.update(driver_build_record=rpin(badb_p)))
    record('T3', 'a driver BUILD record the compare\'s activate_driver_build refuses', T3run(p2, sp2, TOR), False, 'DRIVER_BUILD_RECORD_REFUSED')
    # ---- text of record pending; D-08 layered reporting; unknown slots; real r12 path
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    res = T3.run(slots_p, sp_pend, tor_pend)
    codes = [f['code'] for f in res['failures']]
    check('T3', 'the r5 text-of-record pin still PENDING is a gap, and the other layers are still reported (BUILD_V007_PENDING too)',
          res['verdict'] == 'REFUSE' and 'TEXT_OF_RECORD_PIN_PENDING' in codes and 'BUILD_V007_PENDING' in codes, repr(codes))
    p2, sp2 = cert_variant('d08', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=64))
    s3 = json.loads(p2.read_bytes())
    s3['producer_registry'] = {'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}
    p3 = xw(run / 'slots_d08.json', s3)
    res = T3run(p3, sealed_prereg_for(s3, TOR, 'prereg_d08.json'), TOR)
    codes = [f['code'] for f in res['failures']]
    check('T3', 'D-08: a pin gap no longer hides the certificate layer (PIN_PENDING and CERTIFICATE_M_S together)',
          'PIN_PENDING' in codes and 'CERTIFICATE_M_S' in codes, repr(codes))
    tor_x = text_of_record('variant_tor_unknown_slot.json', mutate=lambda d: d['seal_slots'].update(extra_slot={'value': 'x', 'rule': 'synthetic'}))
    record('T3', 'an unknown prereg seal slot', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_unknown_slot.json'), tor_x), False, 'PREREG_SLOT_UNKNOWN')
    p2, sp2 = variant('realr12', lambda s: s.update(compare_reviewed_source=pin(R12)))
    record('T3', 'REAL: the selected r12 4bd7b262 itself as the reviewed source', T3run(p2, sp2, TOR), True, tag='REAL')
    s_lp = copy.deepcopy(slots)
    s_lp['launch_packet'] = 'PENDING_ROOT_AT_SEAL_ASSEMBLY'
    res = T3run(xw(run / 'slots_launch_packet_string.json', s_lp), sp, TOR)
    check('T3', 'D-07 class: a bare PENDING launch_packet slot refuses with codes, never an exception', res['verdict'] == 'REFUSE' and not any(
        f['code'].startswith('INTERNAL_EXCEPTION') for f in res['failures']) and any(f['code'] == 'SLOT_GROUP_KEYS' for f in res['failures']), repr([f['code'] for f in res['failures']]))
    # ================= tool 4
    use(TOR)

    def gates_body(sha, **kw):
        b = {'schema': GATES_SCHEMA + '_GATES_ONLY', 'blinded': True, 'statement': 'gate statuses and reason codes only; SYNTHETIC TEST BODY',
             'test_mode': False, 'route_a_mode': 'parallel8', 'script_sha256': sha,
             'gates': {'B0': {'gate': 'B0', 'status': 'PASS', 'codes': [], 'fields_read': ['maps/EXT'], 'record_sha256': 'c' * 64, 'crossref': {},
                              'blinding_redaction_applied': False}},
             'mt_crosscheck': 'NOT_APPLICABLE', 'identity_runs': {'Z2': {'valid': True, 'codes': []}}, 'blinding_redaction_applied': False}
        b.update(kw)
        return b

    def validity_body(sha, **kw):
        b = {'schema': GATES_SCHEMA + '_VALIDITY_ONLY', 'blinded': True, 'statement': 'validity booleans and reason codes only; SYNTHETIC TEST BODY',
             'test_mode': False, 'route_a_mode': 'parallel8', 'script_sha256': sha,
             'cases': {'C5H': {'label': 'C5H', 'present': True, 'valid_all': True, 'failed': [], 'reading': None}},
             'I1T_gate': {'gate': 'I1T', 'status': 'NO_RUN', 'codes': []}, 'B0_gate': {'gate': 'B0', 'status': 'PASS', 'codes': []}}
        b.update(kw)
        return b
    nb = [0]

    def body_file(body, name='GATES_ONLY.json'):
        nb[0] += 1
        return xw(run / ('b6_%02d' % nb[0]) / name, json.dumps(body, indent=1) + '\n')
    kmap = xw(run / 'KEY_EQUIVALENCE_MAP_SYNTH.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': KEYMAP, 'note': 'SYNTHETIC test input'})
    newl = xw(run / 'NEW_ITEM_DISPOSITIONS_SYNTH.json', {'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': pin(R12_IMPL),
                                                          'items': [{'id': 'NEW-71', 'disposition': 'ADOPTED', 'reason': 'SYNTHETIC test row', 'must_fail_tests': ['T_SYNTH_1']},
                                                                    {'id': 'NEW-72', 'disposition': 'REJECTED', 'reason': 'SYNTHETIC test row', 'must_fail_tests': []}]})
    cust = xw(run / 'RAW_SUCCESSOR_CUSTODY_SYNTH.json', {'schema': T4.CUSTODY_SCHEMA, 'identity_run': 'Z2', 'driver_sha256': dsha, 'stages_total': 21,
                                                         'stages_successor': 21, 'verdict': 'PASS', 'method': 'SYNTHETIC test input (the real check is root\'s, A59)'})

    class A:
        pass

    def args_for(sl_p, sp_p, tor, sc_p, cov=None, **over):
        sh = C.sha(sc_p)
        a = A()
        a.slots, a.prereg, a.text_of_record, a.frozen, a.covered_later = str(sl_p), str(sp_p), str(tor), str(frozen), list(COV if cov is None else cov)
        a.reviewed, a.sealed_compare = str(reviewed), str(sc_p)
        a.gates_only_output = str(body_file(gates_body(sh)))
        a.validity_only_output = str(body_file(validity_body(sh), 'VALIDITY_ONLY.json'))
        a.key_equivalence_map, a.new_item_list, a.successor_custody, a.b2_record = str(kmap), str(newl), str(cust), str(B2_REC)
        a.__dict__.update(over)
        return a

    def full_set(name, s2, tor):
        sl_p = xw(run / ('slots_%s.json' % name), s2)
        sp2 = sealed_prereg_for(s2, tor, 'prereg_%s.json' % name)
        return sl_p, sp2, sealed_compare_for(s2, sp2, 'sealed_compare_%s.py' % name)
    a = args_for(slots_p, sp, TOR, sc)
    before = sorted(str(p) for p in run.rglob('*'))
    res, text = T4.safe_build(a)
    after = sorted(str(p) for p in run.rglob('*'))
    rec = json.loads(text) if text else {}
    shape_ok = all(isinstance(rec.get(k), dict) and set(rec[k]) == {'path', 'sha256'} for k in ('prereg', 'compare', 'driver', 'frozen_addendum', 'case_block', 'build',
                                                                                              'cascade_map_r5_addendum', 'text_of_record'))
    b2dis = json.loads(B2_REC.read_bytes())['disclosure']
    content_ok = (rec.get('sealed_by') == C.AUTHORITY and rec.get('prereg') == {'path': str(sp.resolve()), 'sha256': C.sha(sp)}
                  and rec.get('compare') == {'path': str(sc.resolve()), 'sha256': C.sha(sc)} and rec.get('driver') == plan['driver']
                  and rec.get('frozen_addendum') == plan['frozen_addendum'] and rec.get('case_block') == pin(cbf) and rec.get('build') == pin(b7)
                  and rec.get('admission_allowlist') == {p: h for h, p in allow6} and rec.get('launch_entry') == {'launcher': plan['launcher'], 'guard': plan['guard']}
                  and rec.get('key_equivalence_map_quoted') == KEYMAP and rec.get('entry_table', {}).get('key') == 'entries_after_A81'
                  and len((rec.get('entry_table', {}).get('table') or {}).get('rows', [])) == NMAX - 82
                  and rec.get('no_change_notes') == ['%s: covers this entry for the prereg text of record (A81 RI-26)' % COV[0]]
                  and rec.get('ddo_gas_M_s_registered') == 128 and rec.get('route_a_mode') == 'parallel8' and 'sealed_status_authority' in rec
                  and isinstance(rec.get('pending_strings_outside_slot_values'), list) and rec.get('text_of_record') == {'path': str(TOR), 'sha256': C.sha(TOR)}
                  and rec.get('b2_disclosure', {}).get('record') == pin(B2_REC) and rec.get('b2_disclosure', {}).get('disclosure') == b2dis
                  and rec.get('b2_disclosure', {}).get('requirement') == B2_TEXT and any(t.startswith('Disclosure E5-08') for t in rec.get('disclosures', [])))
    results.append({'tool': 'T4', 'tag': 'PORT', 'case': 'genuine: record built, nothing written, guard-shaped pins, v002 pass-through fields, B2 disclosure (real C3V003)',
                    'expect': 'PASS', 'verdict': res['verdict'], 'codes': [f['code'] for f in res['failures']], 'notes': [],
                    'ok': res['verdict'] == 'PASS' and text is not None and before == after and shape_ok and content_ok})

    def t4(name, expect_code, tag='NEW', base=None, **over):
        b = A()
        b.__dict__.update((base or a).__dict__)
        b.__dict__.update(over)
        r, t = T4.safe_build(b)
        results.append({'tool': 'T4', 'tag': tag, 'case': name, 'expect': 'REFUSE ' + expect_code, 'verdict': r['verdict'], 'codes': [f['code'] for f in r['failures']],
                        'notes': [], 'ok': t is None and r['verdict'] == 'REFUSE' and any(expect_code in f['code'] for f in r['failures'])})
        return r
    sh0 = C.sha(sc)
    t4('E-SEAL1 output with a decimal row-like value', 'E_SEAL1_OUTPUT_MAY_SHOW_A_ROW_VALUE', tag='PORT',
       gates_only_output=str(body_file(gates_body(sh0, statement='GATES: row 03 speed 45.1234 km/s'))))
    p2, sp2 = variant('t4pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    t4('any slot-fill refusal produces no record', 'T3:', tag='PORT', slots=str(p2), prereg=str(sp2))
    a_ok = args_for(slots_p, sp, TOR, sc, gates_only_output=str(body_file(gates_body(sh0, mt_crosscheck='LO shells at most 0.005; GQ max over P0 at most 1e-12'))))
    r_ok, t_ok = T4.safe_build(a_ok)
    check('T4', 'R-04: the compare\'s own allowed constants (0.005, 1e-12) in a blinded body are not taken for row values', r_ok['verdict'] == 'PASS' and t_ok is not None,
          repr([f['code'] for f in r_ok['failures']]))
    t4('R-04: a B6 body with test_mode true', 'E_SEAL1_TEST_MODE', gates_only_output=str(body_file(gates_body(sh0, test_mode=True))))
    t4('R-04: a B6 body from another script (the reviewed source)', 'E_SEAL1_SCRIPT_NOT_THE_SEALED_COMPARE', gates_only_output=str(body_file(gates_body(R12_SHA))))
    t4('R-04: the validity body given as the gates output', 'E_SEAL1_SCHEMA', gates_only_output=str(body_file(validity_body(sh0), 'GATES_ONLY.json')))
    t4('R-04: a B6 body that is not blinded', 'E_SEAL1_NOT_BLINDED', gates_only_output=str(body_file(gates_body(sh0, blinded=False))))
    t4('R-04: a B6 body carrying a JSON number', 'E_SEAL1_OUTPUT_VALUE_BEARING', gates_only_output=str(body_file(gates_body(sh0, rows_read=12))))
    t4('R-04: a B6 body with a number glued to letters (x61.2222222)', 'E_SEAL1_OUTPUT_VALUE_BEARING', gates_only_output=str(body_file(gates_body(sh0, statement='codes x61.2222222'))))
    t4('R-04: the validity body on cases other than C5H', 'E_SEAL1_VALIDITY_CASES_NOT_C5H',
       validity_only_output=str(body_file(validity_body(sh0, cases={'C4T': {'label': 'C4T'}}), 'VALIDITY_ONLY.json')))
    t4('R-04: a B6 file that is not the compare\'s GATES_ONLY.json', 'E_SEAL1_OUTPUT_NAME', gates_only_output=str(body_file(gates_body(sh0), 'gates.txt')))
    t4('R-04: a B6 body with another route-A mode', 'E_SEAL1_ROUTE_A_MODE', gates_only_output=str(body_file(gates_body(sh0, route_a_mode='serial_with_exemption'))))
    t4('R-04 / v001 regression: a schemaless B7 key map ({"map": []} passed v001)', 'KEY_MAP_SCHEMA', key_equivalence_map=str(xw(run / 'KEYMAP_V001_FORM.json', {'map': []})))
    t4('R-10: the SEAL_RECORD key map differs from the case block\'s', 'KEY_MAP_NOT_THE_CASE_BLOCK_MAP',
       key_equivalence_map=str(xw(run / 'KEYMAP_EMPTY.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': []})))
    t4('B7: a key map mapping one pointer twice', 'KEY_MAP_DUPLICATE_POINTER',
       key_equivalence_map=str(xw(run / 'KEYMAP_DUP.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': KEYMAP + KEYMAP})))
    impl_other = xw(run / 'IMPL_NOT_NAMING_THE_SOURCE.md', '# a compare IMPL that names no reviewed source sha\n')
    t4('B7: a NEW-item list taken from an IMPL that does not name the reviewed source', 'NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE',
       new_item_list=str(xw(run / 'NEW_ITEMS_OTHER_IMPL.json', dict(json.loads(newl.read_bytes()), compare_impl=pin(impl_other)))))
    t4('B7: an ADOPTED NEW item without MUST_FAIL tests', 'NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL',
       new_item_list=str(xw(run / 'NEW_ITEMS_NO_MUSTFAIL.json', dict(json.loads(newl.read_bytes()), items=[{'id': 'NEW-71', 'disposition': 'ADOPTED', 'reason': 'x', 'must_fail_tests': []}]))))
    t4('B7: one NEW id twice', 'NEW_ITEMS_DUPLICATE_ID',
       new_item_list=str(xw(run / 'NEW_ITEMS_DUP.json', dict(json.loads(newl.read_bytes()), items=json.loads(newl.read_bytes())['items'] * 2))))
    t4('B7: raw successor custody of a run on another driver', 'CUSTODY_DRIVER_NOT_THE_SLOT',
       successor_custody=str(xw(run / 'CUSTODY_OTHER_DRIVER.json', dict(json.loads(cust.read_bytes()), driver_sha256='4' * 64))))
    t4('B7: raw successor custody with a stage on its base script', 'CUSTODY_STAGES',
       successor_custody=str(xw(run / 'CUSTODY_STAGES.json', dict(json.loads(cust.read_bytes()), stages_successor=20))))
    # ---- A100 B2 disclosure
    t4('A100: the prereg asks for the B2 disclosure block and no --b2-record is given', 'B2_DISCLOSURE_REQUIRED', b2_record=None)
    s_v7 = copy.deepcopy(slots)
    s_v7['producer_registry'] = pin(REGISTRY_V007)
    sl7, sp7, sc7 = full_set('registry_v007', s_v7, TOR)
    t4('A100: a B2 record that is not the registry\'s B2 record of record (registry C3V007 names d4b41ffc)', 'B2_RECORD_NOT_REGISTERED', base=args_for(sl7, sp7, TOR, sc7))
    t4('A100: the superseded B2 C3V002 record (FAIL, no disclosure block)', 'B2_RECORD_NOT_PASS', base=args_for(sl7, sp7, TOR, sc7), b2_record=str(B2_REC_V002))
    # ---- A99.3 changed-section note in the SEAL_RECORD
    slc, spc, scc = full_set('changed_A90', slots, tor_chg)
    use(tor_chg)
    r_c, t_c = T4.safe_build(args_for(slc, spc, tor_chg, scc, cov=['A90'] + COV))
    notes_c = (json.loads(t_c).get('no_change_notes') if t_c else None) or []
    check('T4', 'A99.3: a changed table row accepted by root\'s note is recorded in the SEAL_RECORD with both section shas', r_c['verdict'] == 'PASS' and len(notes_c) == 2
          and notes_c[0].startswith('A90: its section changed after the text of record was written') and C.sha_bytes(SECS[90][0][1]) in notes_c[0],
          repr([f['code'] for f in r_c['failures']]) + repr(notes_c))
    use(TOR)
    # ---- admission-config check (B8)
    seal_p = xw(run / 'SEAL_RECORD_SYNTH.json', text)
    cfg = {'schema': C.ADMISSION_SCHEMA, 'authority': dict(C.AUTHORITY), 'seal': pin(seal_p), 'prereg': rec['prereg'], 'compare': rec['compare'],
           'build': rec['build'], 'producer_allowlist': rec['admission_allowlist']}
    cfg_p = xw(run / 'ROOT_SEAL_ADMISSION_SYNTH.json', cfg)
    record('T4', 'admission config: genuine (pins this SEAL_RECORD, BUILD_V007, the 15-source allowlist)', T4.check_admission_config(cfg_p, seal_p), True)
    allow5 = {p: h for h, p in C.build_allowlist((PKT / 'BUILD_V005.md').read_bytes().decode('utf-8'))}
    for name, over, code in (('a V006 build pin', {'build': pin(PKT / 'BUILD_V006.md')}, 'ADMISSION_CONFIG_BUILD_NOT_BUILD_V007'),
                             ('the 13-source BUILD_V005 allowlist', {'producer_allowlist': allow5}, 'ADMISSION_ALLOWLIST_COUNT_NOT_15'),
                             ('the guard missing from the allowlist', {'producer_allowlist': {p: h for p, h in rec['admission_allowlist'].items() if p != plan['guard']['path']}},
                              'ADMISSION_CONFIG_GUARD_NOT_NAMED_EXACTLY'),
                             ('another SEAL_RECORD pinned', {'seal': pin(kmap)}, 'ADMISSION_CONFIG_SEAL_NOT_THE_RECORD'),
                             ('an extra key', {'extra': 1}, 'ADMISSION_CONFIG_KEYS')):
        cp = xw(run / ('ROOT_SEAL_ADMISSION_%s.json' % re.sub(r'\W+', '_', name)), dict(cfg, **over))
        record('T4', 'admission config: %s' % name, T4.check_admission_config(cp, seal_p), False, code)
    # ---- tool 5 MUST_FAIL
    r5bad, t5bad = T5.record_bytes(str(R12), R12_SHA, str(CERTS['LO']))
    record('T5', 'tool 5: a check record that is not a check of the r5 build (the LO certificate)', r5bad, False, 'DRIVER_BUILD_NOT_ADMISSIBLE')
    check('T5', 'tool 5: the printed bytes are the driver BUILD record fixture the slots pin', r5text == dbr.read_bytes().decode('utf-8') and t5bad is None, 'mismatch')
    # ================= integration: the built SEAL_RECORD under the REAL guard v008 and launcher v007 (validate only)
    G.CONFIG = cfg_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_p)
    o_adm, o_val = None, None
    try:
        G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
        o_adm = 'ok'
    except BaseException as e:
        o_adm = '%s: %s' % (type(e).__name__, e)
    try:
        o_val = 'ok' if L.validate(json.loads(plan_p.read_bytes())) is True else 'not True'
    except BaseException as e:
        o_val = '%s: %s' % (type(e).__name__, e)
    results.append({'tool': 'integration', 'tag': 'PORT', 'case': 'real guard v008 admits the v002 SEAL_RECORD (via the checked config); real launcher v007 validate() accepts the bound plan',
                    'expect': 'PASS', 'verdict': 'PASS' if (o_adm == 'ok' and o_val == 'ok') else 'REFUSE', 'codes': [o_adm, o_val], 'notes': [], 'ok': o_adm == 'ok' and o_val == 'ok'})
    rec2 = dict(rec, driver=pin(reviewed))
    seal2 = xw(run / 'SEAL_RECORD_OTHER_DRIVER_SYNTH.json', json.dumps(rec2, indent=1, sort_keys=True) + '\n')
    cfg2_p = xw(run / 'ROOT_SEAL_ADMISSION_OTHER_DRIVER_SYNTH.json', dict(cfg, seal=pin(seal2)))
    G.CONFIG = cfg2_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg2_p)
    try:
        L.validate(json.loads(plan_p.read_bytes()))
        o3 = 'accepted'
    except BaseException as e:
        o3 = '%s: %s' % (type(e).__name__, e)
    results.append({'tool': 'integration', 'tag': 'PORT', 'case': 'a SEAL_RECORD naming another driver is refused by launcher v007', 'expect': 'REFUSE PLAN_SEALED_DRIVER_MISMATCH',
                    'verdict': 'REFUSE' if o3 != 'accepted' else 'PASS', 'codes': [o3], 'notes': [], 'ok': 'PLAN_SEALED_DRIVER_MISMATCH' in o3})
    # ================= REAL BUILD_V007 94bc05a5: tool 3, the builder, the admission check and the guard's admission (no launcher validate)
    name_v011 = lambda d: d['seal_slots']['launch_packet']['named_candidates_verified_from_bytes'].update(template_plan=pin(TEMPLATE_V011))
    torR = text_of_record('KMAX_TAIL_PREREG_V007_R5_STANDIN_REAL_BUILD_V007_C4ST2.json', build_path=BUILD_V007, mutate=name_v011)
    sR = copy.deepcopy(slots)
    sR['launch_packet'] = {'build': pin(BUILD_V007), 'bound_plan': rpin(plan_r), 'bound_command': rpin(cmd_r)}
    sR['admission_entry'] = {'launcher': dict(planR['launcher']), 'guard': dict(planR['guard'])}
    slR, spR, scR = full_set('real_build_v007', sR, torR)
    record('T3', 'REAL BUILD_V007 94bc05a5 (15 sources from bytes) with a plan bound by the real binder from its own template V011 1b406591',
           T3run(slR, spR, torR, frozen=frozen, covered_later=COV, reviewed=reviewed, sealed_compare=scR), True, tag='REAL')
    rR, tR = T4.safe_build(args_for(slR, spR, torR, scR))
    recR = json.loads(tR) if tR else {}
    allow7 = {p: h for h, p in C.build_allowlist(BUILD_V007.read_bytes().decode('utf-8'))}
    check('T4', 'REAL BUILD_V007: the SEAL_RECORD pins it and carries its exact 15-source allowlist', rR['verdict'] == 'PASS' and recR.get('build') == pin(BUILD_V007)
          and recR.get('admission_allowlist') == allow7 and len(allow7) == 15, repr([f['code'] for f in rR['failures']]), tag='REAL')
    if tR:
        sealR = xw(run / 'SEAL_RECORD_REAL_BUILD_V007_SYNTH.json', tR)
        cfgR = xw(run / 'ROOT_SEAL_ADMISSION_REAL_BUILD_V007_SYNTH.json', {'schema': C.ADMISSION_SCHEMA, 'authority': dict(C.AUTHORITY), 'seal': pin(sealR),
                                                                           'prereg': recR['prereg'], 'compare': recR['compare'], 'build': recR['build'],
                                                                           'producer_allowlist': recR['admission_allowlist']})
        record('T4', 'REAL BUILD_V007: the admission-config check passes on its 15 sources (V6-S3)', T4.check_admission_config(cfgR, sealR), True, tag='REAL')
        G.CONFIG = cfgR
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfgR)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            oR = 'ok'
        except BaseException as e:
            oR = '%s: %s' % (type(e).__name__, e)
        results.append({'tool': 'integration', 'tag': 'REAL', 'case': 'REAL BUILD_V007: the real guard v008 admission() accepts the config built from the v002 SEAL_RECORD',
                        'expect': 'PASS', 'verdict': 'PASS' if oR == 'ok' else 'REFUSE', 'codes': [oR], 'notes': [], 'ok': oR == 'ok'})
    tor_t = text_of_record('variant_tor_names_v011_template.json', mutate=name_v011)
    record('T3', 'the bound plan is not bound from the template the prereg names (the r5 text names V011; the plan used the test template)',
           T3run(slots_p, sealed_prereg_for(slots, tor_t, 'variant_sealed_names_v011_template.json'), tor_t), False, 'PLAN_TEMPLATE_NOT_THE_PREREG_NAMED_TEMPLATE')
    # ================= REAL prereg r5 3245899f (landed, FROM_CLAUDE4/0103; not yet ruled the text of record): structural compatibility
    d5 = json.loads(R5.read_bytes())
    last5 = max(int(n) for a_, b_ in re.findall(r'A(\d{1,3})-A(\d{1,3})', d5['cites_by_name'][0]) for n in (a_, b_))
    cov5 = ['A%d' % n for n in heads if n > last5]
    record('T1', 'REAL prereg r5 3245899f: tool 1 reads its 20 entries_after_A81 rows, each re-hashes from the frozen bytes, entries after A%d covered %s '
           '(dry-run flag only for path_to_be, the CLAUDE2 path root writes at the freeze)' % (last5, cov5), T1.run(R5, frozen, None, cov5, True), True,
           tag='REAL', note='DRY_RUN_FROZEN_PATH_NOT_PATH_TO_BE')
    sl5, sp5, sc5 = full_set('prereg_r5_landed', sR, R5)
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    res5 = T3.run(sl5, sp5, R5, frozen=frozen, covered_later=cov5, reviewed=reviewed, sealed_compare=sc5, text_of_record_sha=C.sha(R5))
    codes5 = sorted(set(f['code'] for f in res5['failures']))
    check('T3', 'REAL prereg r5 3245899f as the text of record, its sha stated by root (case block %s validated in-process, real BUILD_V007, V011 plan): '
          'tool 3 refuses only because the frozen copy is not yet at path_to_be' % d5['binding_inputs']['case_block']['sha256'][:8],
          codes5 == ['FROZEN_SLOT_NOT_PATH_TO_BE', 'T1:FROZEN_PATH_NOT_PATH_TO_BE'] and any(n['code'] == 'TEXT_OF_RECORD_FROM_ROOT_ARGUMENT' for n in res5['notes']),
          repr(codes5), tag='REAL')
    # ================= r2: the text-of-record argument while the tool pin is PENDING
    record('T3', 'r2: pin PENDING, root states the stand-in sha: every layer passes and the note names the argument',
           T3.run(slots_p, sp, TOR, frozen=frozen, covered_later=COV, reviewed=reviewed, sealed_compare=sc, text_of_record_sha=C.sha(TOR)), True,
           note='TEXT_OF_RECORD_FROM_ROOT_ARGUMENT')
    record('T3', 'r2: pin PENDING, root states a sha that is not the file\'s bytes', T3.run(slots_p, sp, TOR, text_of_record_sha='5' * 64), False,
           'TEXT_OF_RECORD_SHA_ARG_MISMATCH')
    record('T3', 'r2: pin PENDING, root states the r4 sha for the r5 stand-in file', T3.run(slots_p, sp, TOR, text_of_record_sha=C.sha(R4)), False,
           'TEXT_OF_RECORD_SHA_ARG_MISMATCH')
    use(TOR)
    record('T3', 'r2: pin set, a stated sha that differs from the pin', T3.run(slots_p, sp, TOR, text_of_record_sha=C.sha(R4)), False, 'TEXT_OF_RECORD_SHA_ARG_DIFFERS')
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    rA, tA = T4.safe_build(args_for(slots_p, sp, TOR, sc, text_of_record_sha=C.sha(TOR)))
    check('T4', 'r2: the SEAL_RECORD records that root\'s argument pinned the text of record', rA['verdict'] == 'PASS' and tA is not None
          and json.loads(tA).get('text_of_record_pinned_by') == 'ROOT_ARGUMENT', repr([f['code'] for f in rA['failures']]))
    use(TOR)
    # ================= r2: A102 A-B1 class (a duplicate key behind a 4,300+ digit integer)
    big = '9' * 5000
    cma_ab1 = xw(run / 'CASCADE_MAP_R5_ADDENDUM_A_B1_SYNTH.json', '{"n": %s, "amends": "%s", "amends": "x"}\n' % (big, M.PIN_R5_CASCADE_MAP[1]))
    p2, sp2 = variant('cma_ab1', lambda s_: s_.update(cascade_map_r5_addendum=rpin(cma_ab1)))
    res = T3run(p2, sp2, TOR)
    record('T3', 'A102 A-B1: a JSON CASCADE_MAP_R5_ADDENDUM with a duplicate key behind a 5,000-digit integer (main-loop patch)', res, False, 'CASCADE_MAP_R5_ADDENDUM_JSON')
    chk_ab1 = xw(run / 'CHECK_RECORD_A_B1_SYNTH.json', '{"driver": "%s", "verdict": "PASS", "n": %s, "verdict": "FAIL"}\n' % (dsha, big))
    check('T3', 'A102 A-B1 reproduction: r12\'s own check_record_codes admits that duplicate-key check record (r13 fixes it)',
          M.check_record_codes(str(chk_ab1), dsha) == [], repr(M.check_record_codes(str(chk_ab1), dsha)))
    bab1 = json.loads(r5text)
    bab1['check_record'] = rpin(chk_ab1)
    bab1_p = xw(run / 'DRIVER_BUILD_A_B1_CHECK_SYNTH.json', json.dumps(bab1, indent=1, sort_keys=True) + '\n')
    p2, sp2 = variant('dcr_ab1', lambda s_: s_.update(driver_build_record=rpin(bab1_p), driver_check_record=rpin(chk_ab1)))
    res = T3run(p2, sp2, TOR)
    codes = sorted(set(f['code'] for f in res['failures']))
    check('T3', 'A102 A-B1: tool 3 refuses that check record itself (DRIVER_CHECK_RECORD_JSON_DEFECT), though the compare activated the build',
          'DRIVER_CHECK_RECORD_JSON_DEFECT' in codes and 'DRIVER_BUILD_RECORD_REFUSED' not in codes, repr(codes))
    r5ab, t5ab = T5.record_bytes(str(R12), R12_SHA, str(chk_ab1))
    record('T5', 'A102 A-B1: tool 5 refuses to print a driver BUILD record around that check record', r5ab, False, 'CHECK_RECORD_JSON_DEFECT')
    G.CONFIG = run / 'NO_CONFIG_AFTER_TESTS.json'
    os.environ.pop('UNT_ROOT_ADMISSION_SHA256', None)
    summary = {'tool': 'test_seal_tools_c4v002.py', 'tool_sha256': C.sha(__file__), 'run_dir': str(run), 'utc': stamp,
               'tools': {n: C.sha(TOOLS / n) for n in ('seal_common_c4v002.py', 'check_frozen_addendum_c4v002.py', 'check_sealed_compare_c4v002.py',
                                                        'check_slot_fill_c4v002.py', 'build_seal_record_c4v002.py', 'print_driver_build_record_c4v002.py')},
               'inputs_read': {str(p): C.sha(p) for p in [R4, R12, R12_IMPL, DRIVER, CHECK_MD, COMPARATOR, REGISTRY, REGISTRY_V007, DRAFT_CASE_BLOCK, B2_REC, B2_REC_V002,
                                                          BUILD_V007, TEMPLATE_V011, PKT / 'BUILD_V005.md', PKT / 'BUILD_V006.md', PKT / 'P128/LAUNCH_PLAN_V010.json',
                                                          PKT / 'DRY_R5_MS128_V004.json', PKT / 'bind_sealed_launch_plan_cx1v001.py', PKT / 'producer_guard_cx1v008.py',
                                                          PKT / 'route_a_token_launcher_cx1v007.py', PKT / 'route_a_token_launcher_cx1v006.py']
                               + [R5] + list(CERTS.values()) + list(IDENTITY_FILES.values())},
               'frozen_copy_of_the_open_V005': {'path': str(frozen), 'sha256': C.sha(frozen), 'entries': 'A47-A%d' % NMAX},
               'fixtures': {'text_of_record_standin': pin(TOR), 'case_block': pin(cbf), 'driver_build_record': rpin(dbr), 'build_v007_standin': pin(b7),
                            'template': pin(template), 'bound_plan': rpin(plan_p), 'bound_plan_real_build_v007': rpin(plan_r), 'cascade_addendum_standin': rpin(cma),
                            'seal_record': pin(seal_p)},
               'results': results, 'passed': sum(r['ok'] for r in results), 'total': len(results),
               'by_tag': {t: '%d/%d' % (sum(r['ok'] for r in results if r['tag'] == t), sum(1 for r in results if r['tag'] == t)) for t in sorted({r['tag'] for r in results})}}
    with open(run / 'TEST_RESULTS_C4V002.json', 'x') as f:
        json.dump(summary, f, indent=1)
    for r in results:
        print('%-11s %-12s %-96s %-7s %s' % (r['tool'], r['tag'], r['case'][:96], 'ok' if r['ok'] else 'NOT_OK', '' if r['ok'] else r['codes']))
    print('passed', summary['passed'], '/', summary['total'], summary['by_tag'])
    return 0 if summary['passed'] == summary['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
