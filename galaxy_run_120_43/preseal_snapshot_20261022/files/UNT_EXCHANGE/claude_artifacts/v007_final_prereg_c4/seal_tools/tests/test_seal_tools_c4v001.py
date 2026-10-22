# Claude4 (dispatch 0584): tamper tests for the four seal tools, on my own fixtures. Fixtures are built under tests/run_<UTC>/ from:
# the real r4 text of record (read), a frozen copy of the current open V005 addendum (read, then copied into the run folder), the real
# compare r10 source as the "reviewed source" (copied), the real BUILD_V005, template V010, r5 driver and certificates (read), and a plan
# bound by the REAL binder with its HERE patched to the run folder. Integration: the built SEAL_RECORD is fed to the REAL guard v008 /
# launcher v007 (CONFIG and REGISTERED patched in-process to synthetic files; validate() only; nothing is started).
# A local audit hook refuses process creation, network, deletes and any write outside the run folder.
# usage: python3 -I -B test_seal_tools_c4v001.py
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

import contextlib, copy, hashlib, importlib.util, io, json, shlex, time
from pathlib import Path
TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
import seal_common_c4v001 as C
import check_frozen_addendum_c4v001 as T1
import check_sealed_compare_c4v001 as T2
import check_slot_fill_c4v001 as T3
import build_seal_record_c4v001 as T4

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
R4 = CA / 'v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json'
R3 = CA / 'v007_final_prereg_c4/r3/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R3.json'
OPEN_ADD = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
PKT = CA / 'v007_launch_packet_cx1'
T = CA / 'tail_scheme_impl_c2'
COMPARE_R10 = CA / 'v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py'
DRIVER = T / 'driver_r5/galaxy_m0_forward_c2v010.py'


def pin(p):
    p = Path(p)
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
    results = []

    def record(tool, name, res, expect_pass, code=None):
        codes = [f['code'] for f in res.get('failures', [])]
        ok = (res['verdict'] == 'PASS') if expect_pass else (res['verdict'] == 'REFUSE' and (code is None or any(code in c for c in codes)))
        results.append({'tool': tool, 'case': name, 'expect': 'PASS' if expect_pass else 'REFUSE ' + (code or ''), 'verdict': res['verdict'], 'codes': codes, 'ok': ok})
    # ---------------- fixtures
    frozen = xw(run / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', OPEN_ADD.read_bytes().decode('utf-8'))
    frozen_r = Path(os.path.realpath(frozen))
    reviewed = xw(run / 'reviewed_compare_r10_copy.py', COMPARE_R10.read_bytes().decode('utf-8'))
    dbr = xw(run / 'DRIVER_BUILD_RECORD_SYNTH.json', {'schema': 'SYNTH_DRIVER_BUILD', 'driver': pin(DRIVER)})
    dcr = xw(run / 'DRIVER_CHECK_RECORD_SYNTH.json', {'schema': 'SYNTH_DRIVER_CHECK', 'verdict': 'PASS_WITH_FINDINGS'})
    preg = xw(run / 'PRODUCER_REGISTRY_SYNTH.json', {'schema': 'SYNTH_PRODUCER_REGISTRY', 'entries': []})
    dsha = C.sha(DRIVER)
    ids = {k: xw(run / ('IDENTITY_%s_SYNTH.json' % k), {'gate': k, 'NEW_DRIVER_PIN': {'pass': True, 'detail': {'result_json_driver_sha256': dsha}},
                                                        'ref_driver_sha256': '1' * 64}) for k in T3.IDENTITY_KEYS}
    lo_ngc = xw(run / 'LO_NGC_SYNTH.json', {'gate': 'LO_NGC', 'gas_M_s': 96})
    dbl = xw(run / 'DOUBLING_MERGED_SYNTH.json', {'gate': 'DOUBLING', 'gas_M_s': 128, 'ngc_half': {'gas_M_s_NGC': 96}})
    spec = importlib.util.spec_from_file_location('bind_sealed_launch_plan_cx1v001', PKT / 'bind_sealed_launch_plan_cx1v001.py')
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    B.HERE = Path(ROOT_HOLDER[0])
    plan_p, cmd_p = run / 'BOUND_PLAN_SYNTH.json', run / 'BOUND_COMMAND_SYNTH.txt'
    B.bind(str(PKT / 'P128/LAUNCH_PLAN_V010.json'), str(DRIVER), dsha, str(frozen_r), C.sha(frozen_r), str(plan_p), str(cmd_p))
    plan = json.loads(plan_p.read_bytes())
    slots = {'schema': T3.SCHEMA, 'driver_branch': 'r5', 'ngc_gas_M_s': 96, 'frozen_addendum': dict(plan['frozen_addendum']), 'driver': dict(plan['driver']),
             'driver_build_record': pin(dbr), 'driver_check_record': pin(dcr), 'compare_reviewed_source': pin(reviewed),
             'identity_comparator': pin(T / 'gates_v007/run_identity_compare_c2v007.py'),
             'identity_gate_records': {k: pin(v) for k, v in ids.items()},
             'launch_packet': {'build': pin(PKT / 'BUILD_V005.md'), 'bound_plan': pin(os.path.realpath(plan_p)), 'bound_command': pin(os.path.realpath(cmd_p))},
             'certificates': {'EPS': pin(T / 'certificates_v002/gates/EPS_CERT_V006.json'), 'LO': pin(T / 'certificates_v004/gates/LO_CERT_V004_MS128.json'),
                              'GQ': pin(T / 'certificates_v003/gates/GQ_CERT_V005_MS128.json'), 'DOUBLING': pin(dbl),
                              'EPS_NGC': pin(T / 'certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json'), 'LO_NGC': pin(lo_ngc),
                              'I1T_NGC': pin(T / 'certificates_v002/gates/I1T_NGC_T120L_V001.json')},
             'producer_registry': pin(preg), 'cache_directory_r6_only': T3.NOT_APPLICABLE_R5}

    def sealed_prereg_for(sl, name='KMAX_TAIL_PREREG_V007_SEALED_SYNTH.json', mutate=None):
        d = json.loads(R4.read_bytes())
        for pk, sk in T3.PREREG_SLOT_OF.items():
            d['seal_slots'][pk]['value'] = copy.deepcopy(sl[sk])
        if mutate:
            mutate(d)
        return xw(run / name, json.dumps(d, indent=1, ensure_ascii=False) + '\n')
    sp = sealed_prereg_for(slots)
    slots_p = xw(run / 'SLOTS_SYNTH.json', slots)

    def sealed_compare_for(sl, prereg_path, name, edit=None):
        lines = reviewed.read_bytes().decode('utf-8').splitlines(keepends=True)
        exp = T2.expected_pins(sl, prereg_path)
        out = []
        for ln in lines:
            nm = next((n for n in C.PIN_NAMES if ln.startswith(n + ' = None')), None)
            if nm:
                rest = ln[len(nm + ' = None'):]
                ln = '%s = %r%s' % (nm, exp[nm], rest)
            out.append(ln)
        if edit:
            out = edit(out)
        return xw(run / name, ''.join(out))
    sc = sealed_compare_for(slots, sp, 'sealed_compare_SYNTH.py')
    # ---------------- tool 1
    record('T1', 'genuine', T1.run(sp, frozen, None, ['A82']), True)
    txt = frozen.read_bytes().decode('utf-8')
    f_a = xw(run / 'variant_a/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', txt.replace('## A60:', '## A60 (removed heading):'))
    record('T1', 'cited entry A60 absent', T1.run(sp, f_a, None, ['A82']), False, 'CITED_ENTRY_ABSENT_FROM_FROZEN')
    f_b = xw(run / 'variant_b/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', txt + '\n## A70: duplicate entry\n')
    record('T1', 'duplicate heading', T1.run(sp, f_b, None, ['A82']), False, 'DUPLICATE_ENTRY_HEADING')
    f_c = xw(run / 'variant_c/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', txt + '\nsealed prereg %s\n' % C.sha(sp))
    record('T1', 'frozen cites the sealed prereg sha', T1.run(sp, f_c, None, ['A82']), False, 'FROZEN_CITES_SEALED_PREREG_SHA')
    record('T1', 'later entry A82 uncovered', T1.run(sp, frozen, None, []), False, 'UNCOVERED_LATER_ENTRY')
    f_e = xw(run / 'variant_e/V005_ADDENDUM_COPY.md', txt)
    record('T1', 'not the _FROZEN copy', T1.run(sp, f_e, None, ['A82']), False, 'NOT_THE_FROZEN_COPY')
    record('T1', 'expected sha differs', T1.run(sp, frozen, '0' * 64, ['A82']), False, 'FROZEN_SHA_MISMATCH')
    record('T1', 'covered-later names an absent entry', T1.run(sp, frozen, None, ['A82', 'A99']), False, 'COVERED_LATER_NOT_IN_FROZEN')
    dup_json = xw(run / 'variant_h_prereg.json', sp.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "dup",\n "schema"', 1))
    record('T1', 'prereg JSON with a duplicate key', T1.run(dup_json, frozen, None, ['A82']), False, 'PREREG_JSON')
    # ---------------- tool 2
    record('T2', 'genuine', T2.run(reviewed, sc, slots_p, sp), True)
    def chg_nonpin(out):
        i = next(i for i, l in enumerate(out) if l.startswith('TOL') or l.startswith('ART = '))
        out[i] = out[i].rstrip('\n') + '  # tampered\n'
        return out
    record('T2', 'a non-pin line changed', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_a.py', chg_nonpin), slots_p, sp), False, 'NON_PIN_LINE_DIFFERS')
    other_prereg = xw(run / 'other_prereg.json', '{}\n')
    record('T2', 'pin value for another prereg', T2.run(reviewed, sealed_compare_for(slots, other_prereg, 'sc_b.py'), slots_p, sp), False, 'PIN_VALUE_MISMATCH')
    record('T2', 'inserted line', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_c.py', lambda o: o[:10] + ['# inserted\n'] + o[10:]), slots_p, sp), False, 'LINE_COUNT_DIFFERS')
    def dup_assign(out):
        i = next(i for i, l in enumerate(out) if l.startswith('# ====') or l.startswith('#'))
        out[i] = "V007_PREREG_SHA256 = '%s'\n" % ('0' * 64)
        return out
    record('T2', 'second assignment of a pin', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_d.py', dup_assign), slots_p, sp), False, 'NON_PIN_LINE_DIFFERS')
    def chg_comment(out):
        i = next(i for i, l in enumerate(out) if l.startswith('V007_PREREG_SHA256 = '))
        out[i] = out[i].replace('# PENDING_FROM_BYTES', '# EDITED')
        return out
    record('T2', 'pin comment changed', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_e.py', chg_comment), slots_p, sp), False, 'PIN_COMMENT_CHANGED')
    def as_list(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_PRODUCER_REGISTRY = '))
        out[i] = 'PIN_PRODUCER_REGISTRY = %r\n' % [slots['producer_registry']['path'], slots['producer_registry']['sha256']]
        return out
    record('T2', 'pair pin as a list', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_f.py', as_list), slots_p, sp), False, 'PIN_PAIR_SHAPE')
    def unset_one(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_V010_R5_CHECK = '))
        out[i] = 'PIN_V010_R5_CHECK = None\n'
        return out
    record('T2', 'one pin left unset', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_g.py', unset_one), slots_p, sp), False, 'PIN_NOT_SET')
    rv_copy = xw(run / 'variant_reviewed_copy.py', reviewed.read_bytes().decode('utf-8'))
    record('T2', 'reviewed path not the slot', T2.run(rv_copy, sc, slots_p, sp), False, 'REVIEWED_PATH_NOT_THE_SLOT')
    record('T2', 'sealed is the reviewed file', T2.run(reviewed, reviewed, slots_p, sp), False, 'SEALED_IS_REVIEWED')
    sp_j = sealed_prereg_for(slots, 'variant_j_prereg.json', lambda d: d['seal_slots']['compare'].update(value=pin(sc)))
    record('T2', 'prereg compare slot holds the sealed compare', T2.run(reviewed, sealed_compare_for(slots, sp_j, 'sc_j.py'), slots_p, sp_j), False, 'PREREG_COMPARE_SLOT_DIFFERS')
    # ---------------- tool 3
    record('T3', 'genuine r5', T3.run(slots_p, sp, R4, frozen, ['A82'], reviewed, sc), True)

    def variant(name, mutate, prereg_mutate=None, same_prereg=False):
        s2 = copy.deepcopy(slots)
        mutate(s2)
        p2 = xw(run / ('slots_%s.json' % name), s2)
        sp2 = sp if same_prereg else sealed_prereg_for(s2, 'prereg_%s.json' % name, prereg_mutate)
        return p2, sp2
    p2, sp2 = variant('pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    record('T3', 'a PENDING value', T3.run(p2, sp2, R4), False, 'PENDING')
    p2, sp2 = variant('badpin', lambda s: s['identity_gate_records']['Z2'].update(sha256='0' * 64))
    record('T3', 'identity record pin bytes differ', T3.run(p2, sp2, R4), False, 'PIN_BYTES_MISMATCH')
    p2, sp2 = variant('text', lambda s: None, prereg_mutate=lambda d: d['tests']['T3'].update(text=d['tests']['T3']['text'] + ' (edited)'))
    record('T3', 'sealed prereg text changed outside the slots', T3.run(p2, sp2, R4), False, 'SEALED_PREREG_TEXT_CHANGED')
    p2, _ = variant('slotdiff', lambda s: s.update(producer_registry=pin(dcr)), same_prereg=True)
    record('T3', 'prereg slot value differs from the slots', T3.run(p2, sp, R4), False, 'PREREG_SLOT_VALUE_DIFFERS')
    alias = slots['driver']['path'].replace('/driver_r5/', '/driver_r5/./')
    p2, sp2 = variant('driveralias', lambda s: s.update(driver={'path': alias, 'sha256': dsha}))
    record('T3', 'driver slot spelled differently from the plan', T3.run(p2, sp2, R4), False, 'PLAN_DRIVER_NOT_THE_SLOT')
    bad_id = xw(run / 'IDENTITY_Z2_WRONG_DRIVER.json', {'gate': 'Z2', 'NEW_DRIVER_PIN': {'pass': True, 'detail': {'result_json_driver_sha256': '2' * 64}}})
    p2, sp2 = variant('iddriver', lambda s: s['identity_gate_records'].update(Z2=pin(bad_id)))
    record('T3', 'identity record carries another driver', T3.run(p2, sp2, R4), False, 'IDENTITY_RECORD')
    lo64 = json.loads((T / 'certificates_v004/gates/LO_CERT_V004_MS128.json').read_bytes())
    lo64['source_gas_M_s'] = 64
    lo64_p = xw(run / 'LO_CERT_M_S64_SYNTH.json', lo64)
    p2, sp2 = variant('lo64', lambda s: s['certificates'].update(LO=pin(lo64_p)))
    record('T3', 'LO certificate at M_s 64', T3.run(p2, sp2, R4), False, 'CERTIFICATE_M_S')
    cdir = run / 'cache_dir_nonempty'
    cdir.mkdir()
    xw(cdir / 'prewarmed.bin', 'x')
    p2, sp2 = variant('r6full', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir)}))
    record('T3', 'r6 cache directory not empty (pre-warmed)', T3.run(p2, sp2, R4), False, 'CACHE_DIRECTORY_NOT_EMPTY')
    cdir2 = run / 'cache_dir_empty'
    cdir2.mkdir()
    p2, sp2 = variant('r6empty', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir2)}))
    record('T3', 'r6 with a fresh empty cache directory', T3.run(p2, sp2, R4), True)
    p2, sp2 = variant('r5cache', lambda s: s.update(cache_directory_r6_only={'path': str(cdir2)}))
    record('T3', 'r5 slot set naming a cache directory', T3.run(p2, sp2, R4), False, 'CACHE_DIRECTORY_UNDER_R5')
    cmd2 = xw(run / 'BOUND_COMMAND_EDITED.txt', cmd_p.read_bytes().decode('utf-8').replace('--execute-root-only', '--execute-root-only --worker'))
    p2, sp2 = variant('cmd', lambda s: s['launch_packet'].update(bound_command=pin(cmd2)))
    record('T3', 'bound command edited', T3.run(p2, sp2, R4), False, 'BOUND_COMMAND_NOT_THE_BINDER_LINE')
    dupslots = xw(run / 'slots_dupkey.json', slots_p.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "x",\n "schema"', 1))
    record('T3', 'slot JSON with a duplicate key', T3.run(dupslots, sp, R4), False, 'INPUT_JSON')
    record('T3', 'text of record is not r4', T3.run(slots_p, sp, R3), False, 'TEXT_OF_RECORD_NOT_R4')
    p2, sp2 = variant('build4', lambda s: s['launch_packet'].update(build=pin(PKT / 'BUILD_V004.md')))
    record('T3', 'launch build not the prereg-named BUILD_V005', T3.run(p2, sp2, R4), False, 'BUILD_NOT_THE_PREREG_NAMED_BUILD')
    # ---------------- tool 4
    g_out = xw(run / 'GATES_ONLY_OUTPUT_SYNTH.txt', 'GATES: B0 PASS; B1 PASS; Z2_OFF_RO1 PASS; EPS PASS; LO PASS; GQ PASS; DOUBLING PASS\n')
    v_out = xw(run / 'VALIDITY_ONLY_C5H_OUTPUT_SYNTH.txt', 'C5H: VALID; ADMISSIBLE; reasons: none recorded\n')
    kmap = xw(run / 'KEY_EQUIVALENCE_MAP_SYNTH.json', {'map': []})
    newl = xw(run / 'NEW_ITEM_LIST_SYNTH.json', {'items': []})
    cust = xw(run / 'SUCCESSOR_CUSTODY_SYNTH.json', {'stages': 21})

    class A:
        pass
    a = A()
    a.slots, a.prereg, a.text_of_record, a.frozen, a.covered_later = str(slots_p), str(sp), str(R4), str(frozen), ['A82']
    a.reviewed, a.sealed_compare = str(reviewed), str(sc)
    a.gates_only_output, a.validity_only_output, a.key_equivalence_map, a.new_item_list, a.successor_custody = str(g_out), str(v_out), str(kmap), str(newl), str(cust)
    before = sorted(str(p) for p in run.rglob('*'))
    res, text = T4.build(a)
    after = sorted(str(p) for p in run.rglob('*'))
    ok = res['verdict'] == 'PASS' and text is not None and before == after
    rec = json.loads(text) if text else {}
    shape_ok = all(isinstance(rec.get(k), dict) and set(rec[k]) == {'path', 'sha256'} for k in ('prereg', 'compare', 'driver', 'frozen_addendum'))
    results.append({'tool': 'T4', 'case': 'genuine: record built, nothing written, guard-shaped pins', 'expect': 'PASS', 'verdict': res['verdict'],
                    'codes': [f['code'] for f in res['failures']], 'ok': ok and shape_ok and rec.get('sealed_by') == C.AUTHORITY
                    and rec['prereg'] == {'path': str(sp.resolve()), 'sha256': C.sha(sp)} and rec['compare'] == {'path': str(sc.resolve()), 'sha256': C.sha(sc)}
                    and rec['driver'] == plan['driver'] and rec['frozen_addendum'] == plan['frozen_addendum']})
    bad_out = xw(run / 'GATES_ONLY_OUTPUT_LEAK.txt', 'GATES: row 03 speed 45.1234 km/s\n')
    a.gates_only_output = str(bad_out)
    res2, text2 = T4.build(a)
    results.append({'tool': 'T4', 'case': 'E-SEAL1 output with a decimal row-like value', 'expect': 'REFUSE E_SEAL1_OUTPUT_MAY_SHOW_A_ROW_VALUE', 'verdict': res2['verdict'],
                    'codes': [f['code'] for f in res2['failures']], 'ok': text2 is None and any('E_SEAL1_OUTPUT_MAY_SHOW_A_ROW_VALUE' in f['code'] for f in res2['failures'])})
    a.gates_only_output = str(g_out)
    p2, sp2 = variant('t4pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    a.slots, a.prereg = str(p2), str(sp2)
    res3, text3 = T4.build(a)
    results.append({'tool': 'T4', 'case': 'any slot-fill refusal produces no record', 'expect': 'REFUSE', 'verdict': res3['verdict'], 'codes': [f['code'] for f in res3['failures']],
                    'ok': text3 is None and res3['verdict'] == 'REFUSE'})
    # ---------------- integration: the built SEAL_RECORD under the REAL guard v008 and launcher v007 (validate only)
    seal_p = xw(run / 'SEAL_RECORD_SYNTH.json', text)
    gspec = importlib.util.spec_from_file_location('producer_guard_cx1v008', PKT / 'producer_guard_cx1v008.py')
    G = importlib.util.module_from_spec(gspec)
    sys.modules['producer_guard_cx1v008'] = G
    gspec.loader.exec_module(G)
    G.REGISTERED = (run / 'synthetic_registered_A' / G.C5H_NAME, run / 'synthetic_registered_B' / G.C5H_NAME)
    build_text = (PKT / 'BUILD_V005.md').read_bytes().decode('utf-8')
    sec = build_text.split('## Supported runtime entry allowlist\n', 1)[1].split('\n## ', 1)[0]
    import re as _re
    allow = {p: h for h, p in _re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', sec, _re.M)}
    cfg = {'schema': 'UNT_ROOT_SEAL_ADMISSION_CX1V001', 'authority': dict(G.AUTHORITY), 'seal': pin(seal_p), 'prereg': rec['prereg'], 'compare': rec['compare'],
           'build': pin(PKT / 'BUILD_V005.md'), 'producer_allowlist': allow}
    cfg_p = xw(run / 'ROOT_SEAL_ADMISSION_SYNTH.json', cfg)
    G.CONFIG = cfg_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_p)
    lspec = importlib.util.spec_from_file_location('route_a_token_launcher_cx1v007', PKT / 'route_a_token_launcher_cx1v007.py')
    L = importlib.util.module_from_spec(lspec)
    lspec.loader.exec_module(L)
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
    results.append({'tool': 'integration', 'case': 'real guard v008 admits the built SEAL_RECORD; real launcher v007 validate() accepts the bound plan',
                    'expect': 'PASS', 'verdict': 'PASS' if (o_adm == 'ok' and o_val == 'ok') else 'REFUSE', 'codes': [o_adm, o_val], 'ok': o_adm == 'ok' and o_val == 'ok'})
    # tamper the seal: another driver -> the launcher must refuse
    rec2 = dict(rec, driver=pin(reviewed))
    seal2 = xw(run / 'SEAL_RECORD_OTHER_DRIVER_SYNTH.json', json.dumps(rec2, indent=1, sort_keys=True) + '\n')
    cfg2 = dict(cfg, seal=pin(seal2))
    cfg2_p = xw(run / 'ROOT_SEAL_ADMISSION_OTHER_DRIVER_SYNTH.json', cfg2)
    G.CONFIG = cfg2_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg2_p)
    try:
        L.validate(json.loads(plan_p.read_bytes()))
        o3 = 'accepted'
    except BaseException as e:
        o3 = '%s: %s' % (type(e).__name__, e)
    results.append({'tool': 'integration', 'case': 'a SEAL_RECORD naming another driver is refused by launcher v007', 'expect': 'REFUSE PLAN_SEALED_DRIVER_MISMATCH',
                    'verdict': 'REFUSE' if o3 != 'accepted' else 'PASS', 'codes': [o3], 'ok': 'PLAN_SEALED_DRIVER_MISMATCH' in o3})
    summary = {'tool': 'test_seal_tools_c4v001.py', 'tool_sha256': C.sha(__file__), 'run_dir': str(run),
               'tools': {n: C.sha(TOOLS / n) for n in ('seal_common_c4v001.py', 'check_frozen_addendum_c4v001.py', 'check_sealed_compare_c4v001.py',
                                                        'check_slot_fill_c4v001.py', 'build_seal_record_c4v001.py')},
               'inputs_read': {str(p): C.sha(p) for p in (R4, R3, OPEN_ADD, COMPARE_R10, DRIVER, PKT / 'BUILD_V005.md', PKT / 'P128/LAUNCH_PLAN_V010.json',
                                                         PKT / 'bind_sealed_launch_plan_cx1v001.py', PKT / 'producer_guard_cx1v008.py', PKT / 'route_a_token_launcher_cx1v007.py')},
               'results': results, 'passed': sum(r['ok'] for r in results), 'total': len(results)}
    with open(run / 'TEST_RESULTS_C4V001.json', 'x') as f:
        json.dump(summary, f, indent=1)
    for r in results:
        print('%-11s %-74s %-7s %s' % (r['tool'], r['case'][:74], 'ok' if r['ok'] else 'NOT_OK', '' if r['ok'] else r['codes']))
    print('passed', summary['passed'], '/', summary['total'])
    return 0 if summary['passed'] == summary['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
