# Claude4 helper: INDEPENDENT refute-by-default check of seal tools v002 r2 (A99 item 4, dispatch 0621).
# Imports the r2 tools of record READ-ONLY from seal_tools_v002/r2 (shas checked first) and uses their SHIPPED state (tool 3's
# text-of-record pin PENDING; root states the sha with text_of_record_sha). Base: a scratch sealed prereg built from the REAL prereg
# r5 3245899f (only path_to_be moved into this run folder), the real case block 76309ae3, the real BUILD_V007 94bc05a5, a plan bound by
# the real binder from the real V011 template, the real certificates / identity records / CHECK.md / registry C3V009 / B2 C3V003, the
# REAL compare r12 4bd7b262 as the reviewed source, a scratch sealed compare (r12 + the five pins), a CASCADE_MAP_R5_ADDENDUM
# stand-in, B6 bodies built with r12's own blinded_gate / blinded_case / assert_no_numbers, and B7 inputs in the v002 schemas.
# Every mutation starts from that base, which must PASS first (non-vacuous). Also: the 40 v001 cases ported to v002 (tag V001PORT).
# Run under tools/run_fenced_c4chk.py (fence_c4v002 of this folder). A local hook also refuses writes outside the run folder.
import os, sys
RUNROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_HOLDER = [RUNROOT]


def _local_hook(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn', 'os.spawn', 'os.fork', 'os.forkpty', 'pty.spawn', 'os.kill',
                 'socket.connect', 'socket.bind', 'os.remove', 'os.rmdir', 'shutil.rmtree', 'os.rename'):
        raise PermissionError('LOCAL_HOOK ' + event)
    if event == 'open' and len(args) >= 2:
        p, mode, flags = args[0], args[1], (args[2] if len(args) > 2 else 0)
        w = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC))
        if w and isinstance(p, (str, bytes, os.PathLike)):
            real = os.path.realpath(os.path.abspath(os.fsdecode(p)))
            if not real.startswith(ROOT_HOLDER[0] + os.sep):
                raise PermissionError('LOCAL_HOOK write outside run folder: ' + real)
    if event in ('os.mkdir', 'os.symlink') and args:
        p = args[1] if event == 'os.symlink' else args[0]
        real = os.path.join(os.path.realpath(os.path.dirname(os.path.abspath(os.fsdecode(p)))), os.path.basename(os.fsdecode(p)))
        if not real.startswith(ROOT_HOLDER[0] + os.sep):
            raise PermissionError('LOCAL_HOOK %s outside run folder: %s' % (event, real))


sys.addaudithook(_local_hook)
import copy, contextlib, hashlib, importlib.util, io, json, re, shlex, time
from pathlib import Path

CA = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
R2 = CA / 'v007_final_prereg_c4/seal_tools_v002/r2'
R2_SHAS = {'seal_common_c4v002.py': 'f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10',
           'check_frozen_addendum_c4v002.py': '06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891',
           'check_sealed_compare_c4v002.py': 'aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf',
           'check_slot_fill_c4v002.py': '806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb',
           'build_seal_record_c4v002.py': '4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52',
           'print_driver_build_record_c4v002.py': 'fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673'}
for n, h in R2_SHAS.items():
    assert hashlib.sha256((R2 / n).read_bytes()).hexdigest() == h, n
sys.path.insert(0, str(R2))
import seal_common_c4v002 as C
import check_frozen_addendum_c4v002 as T1
import check_sealed_compare_c4v002 as T2
import check_slot_fill_c4v002 as T3
import build_seal_record_c4v002 as T4
import print_driver_build_record_c4v002 as T5
assert T3.TEXT_OF_RECORD_SHA == T3.TEXT_OF_RECORD_PENDING, 'shipped state expected'

C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
OPEN_ADD = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
FROZEN_NAME = 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md'
R4 = CA / 'v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json'
R5 = CA / 'v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'
R12 = CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'
R12_IMPL = CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md'
PKT = CA / 'v007_launch_packet_cx1'
T_ = CA / 'tail_scheme_impl_c2'
BUILD_V007 = PKT / 'BUILD_V007.md'
TEMPLATE_V011 = PKT / 'P128/LAUNCH_PLAN_V011_CX3V001.json'
BINDER = PKT / 'bind_sealed_launch_plan_cx1v001.py'
GUARD = PKT / 'producer_guard_cx1v008.py'
LAUNCHER = PKT / 'route_a_token_launcher_cx1v007.py'
DRIVER = T_ / 'driver_r5/galaxy_m0_forward_c2v010.py'
CHECK_MD = T_ / 'driver_r5/check/CHECK.md'
COMPARATOR = T_ / 'gates_v007/r2/run_identity_compare_c2v007.py'
IDENT = {'Z2': T_ / 'gates_v007/r2/records/R5_V001/B1_R5_C2V007.json', 'Z2_OFF_RO1': T_ / 'gates_v007/r2/records/R5_V001/B1_OFF_R5_C2V007.json',
         'B0prime_RERUN': T_ / 'gates_v007/r2/records/R5_V001/B0prime_RERUN_R5_C2V007.json'}
CERTS = {'EPS': T_ / 'certificates_v002/gates/EPS_CERT_V006.json', 'LO': T_ / 'certificates_v004/gates/LO_CERT_V004_MS128.json',
         'GQ': CA / 'producer_registry_c3/out/GQ_CERT_V006.json', 'DOUBLING': CA / 'producer_registry_c3/out/DOUBLING_MERGED_C3V001.json',
         'EPS_NGC': T_ / 'certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json', 'LO_NGC': T_ / 'certificates_v002/gates/LO_NGC_CERT_V002.json',
         'I1T_NGC': T_ / 'certificates_v002/gates/I1T_NGC_T120L_V001.json'}
GQ_V005 = T_ / 'certificates_v003/gates/GQ_CERT_V005_MS128.json'
REGISTRY = CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json'
B2_REC = CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V003.json'
CASE_BLOCK = CA / 'v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json'
DRAFT_CB = T_ / 'driver/out/CASE_BLOCK_V007_DRAFT_C2V001.json'
REAL = {R4: 'e3b6b5b2ba265f54d15381f358913dd3ea931761aaa649c98a7583f58f1b7cf8', R5: '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393',
        R12: '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28', R12_IMPL: 'ef0db32dc5d8c099d9346bb33cfabdc52cd73bdcd5ffdc91dc7cc922c3b9484c',
        BUILD_V007: '94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de', TEMPLATE_V011: '1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c',
        BINDER: 'f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca', GUARD: '294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731',
        LAUNCHER: '861bba68dd7d207beb30ed828c1557955f31979cf2e15369acccc52ea595953d', DRIVER: 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6',
        CHECK_MD: '89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632', COMPARATOR: '052da0fe378b7927f35be28f9eda6f03313aef32bae7d5c9a301d276de21b12e',
        IDENT['Z2']: '83e7b0673159156832995a1d7caae401a430918cbd110975bac8e18335aedc72', IDENT['Z2_OFF_RO1']: '3b9ad4029a8673eabfa87b2fe77ea66241589412291c44af5d0b220a6fad3df2',
        IDENT['B0prime_RERUN']: 'e33af53d1df36d858ed887bc4ed24fae77fe606d88ab26e2a77d9e5481d09258',
        CERTS['EPS']: '598c8fa34dc85113aa99dd3722f6b37f6625149995d7365c8cbd1b796f830192', CERTS['LO']: '1c384f763e663d85414f25ef8c02b4291efd88b63353a77961f2e88aca2e204a',
        CERTS['GQ']: '5a1b39f8eccaaea107b5e4f5888456bf286714f17659d7dae256de3611b6484f', CERTS['DOUBLING']: 'ea48ac2bc429a1b6f7ae9b2cf96964a42bbedfd64afab21f724259114d8b0f7b',
        CERTS['EPS_NGC']: '1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d', CERTS['LO_NGC']: '33bc21905045431ca877ea26d5c9edf07fd3d7c9e33409cf9e24752da039c724',
        CERTS['I1T_NGC']: '3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6', GQ_V005: 'fbceefe68fecda35745575fba6c85e550e016e8aeefea59233147e520c803e21',
        REGISTRY: '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8', B2_REC: '915fbcda4f4a2cb5f61b257ff83494738144e177401c11c94e254c322df2411c',
        CASE_BLOCK: '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71', DRAFT_CB: '6bf4ce5a4219d281fa480d4249e818e8d9fc39779b3ad605e1a069f42e0da4c1'}
R12_SHA = REAL[R12]


def pin(p):
    p = Path(p)
    return {'path': str(p), 'sha256': C.sha(p)}


def rpin(p):
    p = Path(os.path.realpath(p))
    return {'path': str(p), 'sha256': C.sha(p)}


def xw(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'x', encoding='utf-8') as f:
        f.write(data if isinstance(data, str) else json.dumps(data, indent=1, ensure_ascii=False) + '\n')
    return p


def codes_of(res):
    return [f['code'] for f in res.get('failures', [])]


def main():
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    run = Path(RUNROOT) / ('run_v1_' + stamp)
    run.mkdir()
    ROOT_HOLDER[0] = os.path.realpath(str(run))
    run = Path(ROOT_HOLDER[0])
    results = []

    def rec_(group, tag, name, ok, verdict, codes, expect, note=''):
        results.append({'group': group, 'tag': tag, 'case': name, 'ok': bool(ok), 'verdict': verdict, 'codes': codes, 'expect': expect, 'note': note})

    def expect_refuse(group, tag, name, res, code, absent=None):
        cs = codes_of(res)
        ok = res.get('verdict') == 'REFUSE' and any(code in c for c in cs) and not (absent and any(absent in c for c in cs))
        rec_(group, tag, name, ok, res.get('verdict'), cs, 'REFUSE ' + code + ((' without ' + absent) if absent else ''))
        return res

    def expect_pass(group, tag, name, res, note=None):
        cs = codes_of(res)
        ok = res.get('verdict') == 'PASS' and (note is None or note in [n['code'] for n in res.get('notes', [])])
        rec_(group, tag, name, ok, res.get('verdict'), cs, 'PASS' + ((' with note ' + note) if note else ''))
        return res

    def finding(group, name, observed_pass, res, detail):
        """a probe of a suspected gap: ok=True records that the gap is REAL (the tool PASSES what it should refuse)."""
        rec_(group, 'GAP_PROBE', name, observed_pass, res.get('verdict') if isinstance(res, dict) else str(res), codes_of(res) if isinstance(res, dict) else [],
             'PASS observed = gap confirmed', detail)

    def check(group, tag, name, ok, detail=''):
        rec_(group, tag, name, ok, 'TRUE' if ok else 'FALSE', [] if ok else [detail], 'TRUE', detail if ok else '')
    for p, h in REAL.items():
        assert C.sha(p) == h, str(p)
    open_bytes_start = OPEN_ADD.read_bytes()
    M = C.load_reviewed_compare(str(R12), R12_SHA)
    # ---------------- frozen copy at a scratch path_to_be (the open file's bytes now)
    frozen = xw(run / 'frozen' / FROZEN_NAME, open_bytes_start.decode('utf-8'))
    fsha = C.sha(frozen)
    ftext = frozen.read_bytes().decode('utf-8')
    heads = sorted({int(n) for n in re.findall(r'^## A(\d{1,3}):', ftext, re.M)})
    NMAX = max(heads)
    COV = ['A%d' % n for n in heads if n > 101]
    r5 = json.loads(R5.read_bytes())

    def tor_from(mut=None, name=None):
        d = copy.deepcopy(r5)
        d['seal_slots']['frozen_addendum']['path_to_be'] = str(frozen)
        if mut:
            mut(d)
        return xw(run / (name or 'KMAX_TAIL_PREREG_V007_R5S_C4CHK.json'), json.dumps(d, indent=1, ensure_ascii=False) + '\n')
    R5S = tor_from()
    # ---------------- tool 5: the driver BUILD record
    t5res, t5text = T5.record_bytes(str(R12), R12_SHA, str(CHECK_MD))
    expect_pass('T5', 'REAL', 'tool 5 prints an r5 driver BUILD record with CHECK.md 89a6de88', t5res)
    dbr = xw(run / 'DRIVER_BUILD_R5_C4CHK.json', t5text)
    check('T5', 'REAL', 'tool 5 bytes reproduce the builder\'s out/CLI_R2_T5_DRIVER_BUILD_RECORD_BYTES.json sha 25b4ff69',
          C.sha(dbr) == '25b4ff697748ae23c0d1322228c8bdd689b4b378a70035ab89f5de03b2ba79fb', C.sha(dbr))
    M.activate_driver_build(json.loads(t5text))
    # ---------------- binder (real), guard and launcher modules (REGISTERED / CONFIG patched before any guard call)
    sys.path.insert(0, str(PKT))
    gspec = importlib.util.spec_from_file_location('producer_guard_cx1v008', GUARD)
    G = importlib.util.module_from_spec(gspec)
    sys.modules['producer_guard_cx1v008'] = G
    gspec.loader.exec_module(G)
    G.REGISTERED = (run / 'synthetic_registered_A' / G.C5H_NAME, run / 'synthetic_registered_B' / G.C5H_NAME)
    G.CONFIG = run / 'NO_CONFIG_YET.json'
    lspec = importlib.util.spec_from_file_location('route_a_token_launcher_cx1v007', LAUNCHER)
    L = importlib.util.module_from_spec(lspec)
    lspec.loader.exec_module(L)
    bspec = importlib.util.spec_from_file_location('bind_sealed_launch_plan_cx1v001', BINDER)
    B = importlib.util.module_from_spec(bspec)
    bspec.loader.exec_module(B)
    B.HERE = run
    dsha = C.sha(DRIVER)
    plan_p, cmd_p = run / 'BOUND_PLAN_V011_C4CHK.json', run / 'BOUND_COMMAND_V011_C4CHK.txt'
    B.bind(str(TEMPLATE_V011), str(DRIVER), dsha, str(frozen), fsha, str(plan_p), str(cmd_p))
    plan = json.loads(plan_p.read_bytes())
    cma = xw(run / 'CASCADE_MAP_R5_ADDENDUM_STANDIN_C4CHK.md',
             '# CASCADE_MAP_R5_ADDENDUM stand-in (Claude4 helper, synthetic test input; NOT the immutable inventory addendum of record, A69)\n\n'
             'Extends the r5 cascade map %s (%s).\n' % (M.PIN_R5_CASCADE_MAP[0], M.PIN_R5_CASCADE_MAP[1]))
    slots = {'schema': T3.SCHEMA, 'driver_branch': 'r5', 'ngc_gas_M_s': 96, 'frozen_addendum': dict(plan['frozen_addendum']), 'driver': dict(plan['driver']),
             'driver_build_record': rpin(dbr), 'driver_check_record': pin(CHECK_MD), 'compare_reviewed_source': pin(R12),
             'identity_comparator': pin(COMPARATOR), 'identity_gate_records': {k: pin(v) for k, v in IDENT.items()},
             'launch_packet': {'build': pin(BUILD_V007), 'bound_plan': rpin(plan_p), 'bound_command': rpin(cmd_p)},
             'certificates': {k: pin(v) for k, v in CERTS.items()}, 'producer_registry': pin(REGISTRY),
             'cache_directory_r6_only': T3.NOT_APPLICABLE_R5, 'cascade_map_r5_addendum': rpin(cma),
             'admission_entry': {'launcher': dict(plan['launcher']), 'guard': dict(plan['guard'])}}
    nm = r5['seal_slots']
    check('setup', 'REAL', 'slot values equal prereg r5\'s named candidates (driver, compare r12, comparator, identity records, certificates, BUILD_V007, registry C3V009, plan launcher/guard)',
          slots['driver'] == nm['driver']['named_candidates_verified_from_bytes']['r5']
          and slots['compare_reviewed_source'] == nm['compare']['named_candidates_verified_from_bytes']['r12_cx3v002_final_round']
          and slots['identity_comparator'] == nm['identity_comparator']['named_candidates_verified_from_bytes']['c2v007r2']
          and all(slots['identity_gate_records'][k] == nm['identity_gate_records']['named_candidates_verified_from_bytes'][k] for k in IDENT)
          and slots['certificates']['DOUBLING'] == nm['certificates']['named_candidates_verified_from_bytes']['DOUBLING_merged']
          and slots['launch_packet']['build'] == nm['launch_packet']['named_candidates_verified_from_bytes']['build']
          and slots['producer_registry'] == {k: nm['producer_registry']['named_candidates_verified_from_bytes']['C3V009_candidate'][k] for k in ('path', 'sha256')}
          and slots['admission_entry']['launcher'] == nm['launch_packet']['named_candidates_verified_from_bytes']['build_v007_check_at_r5_generation']['launcher']
          and slots['admission_entry']['guard'] == nm['launch_packet']['named_candidates_verified_from_bytes']['build_v007_check_at_r5_generation']['guard'], 'mismatch')

    def sealed_prereg(sl, tor, name, mutate=None):
        d = json.loads(Path(tor).read_bytes())
        for pk, sk in T3.PREREG_SLOT_OF.items():
            d['seal_slots'][pk]['value'] = copy.deepcopy(sl[sk])
        if mutate:
            mutate(d)
        return xw(run / name, json.dumps(d, indent=1, ensure_ascii=False) + '\n')

    def sealed_compare(sl, prereg_path, name, edit=None, src=R12):
        lines = Path(src).read_bytes().decode('utf-8').splitlines(keepends=True)
        exp = T2.expected_pins(sl, prereg_path)
        out = []
        for ln in lines:
            n_ = next((n for n in C.PIN_NAMES if ln.startswith(n + ' = None')), None)
            if n_:
                ln = '%s = %r%s' % (n_, exp[n_], ln[len(n_ + ' = None'):])
            out.append(ln)
        if edit:
            out = edit(out)
        return xw(run / name, ''.join(out))
    slots_p = xw(run / 'SLOTS_C4CHK.json', slots)
    sp = sealed_prereg(slots, R5S, 'KMAX_TAIL_PREREG_V007_SEALED_C4CHK.json')
    sc = sealed_compare(slots, sp, 'kmax_tail_compare_c2v007_r12_SEALED_C4CHK.py')
    trs = C.sha(R5S)

    def t3(sl_p=None, sp_p=None, tor=None, tor_sha='auto', full=True, cov=None, frozen_p=None, reviewed=None, sealed_c=None):
        tor = tor or R5S
        sha_arg = C.sha(tor) if tor_sha == 'auto' else tor_sha
        if full:
            return T3.run(str(sl_p or slots_p), str(sp_p or sp), str(tor), str(frozen_p or frozen), COV if cov is None else cov,
                          str(reviewed or R12), str(sealed_c or sc), sha_arg)
        return T3.run(str(sl_p or slots_p), str(sp_p or sp), str(tor), None, (), None, None, sha_arg)

    def variant(name, mutate, prereg_mutate=None, tor=None):
        s2 = copy.deepcopy(slots)
        mutate(s2)
        p2 = xw(run / ('slots_%s.json' % name), s2)
        sp2 = sealed_prereg(s2, tor or R5S, 'prereg_%s.json' % name, prereg_mutate)
        sc2 = sealed_compare(s2, sp2, 'sc_%s.py' % name)
        return s2, p2, sp2, sc2
    # ================= BASE (must pass)
    base1 = expect_pass('base', 'BASE', 'tool 1 on the scratch r5 sealed prereg; entries after A101 listed %s' % COV, T1.run(str(sp), str(frozen), None, COV))
    base2 = expect_pass('base', 'BASE', 'tool 2: the scratch sealed compare differs from REAL r12 only in the five pins', T2.run(str(R12), str(sc), str(slots_p), str(sp)))
    base3 = expect_pass('base', 'BASE', 'tool 3 full (tools 1 and 2 inside), text of record = scratch r5 stated by root', t3(), note='TEXT_OF_RECORD_FROM_ROOT_ARGUMENT')
    # ---------------- B6 bodies with r12's own blinding functions; B7 inputs
    sc_sha = C.sha(sc)

    def gate_entry(g, sha_, status='PASS'):
        return M.blinded_gate({'gate': g, 'status': status, 'codes': [] if status == 'PASS' else ['DEFECT:SYNTHETIC_%s' % g], 'fields_read': ['verdict'],
                               'record': {'sha256': sha_} if sha_ else None, 'crossref': {}})
    GATE_SHAS = {g: None for g in M.ALL_GATES}
    GATE_SHAS.update({'EPS': slots['certificates']['EPS']['sha256'], 'LO': slots['certificates']['LO']['sha256'], 'GQ': slots['certificates']['GQ']['sha256'],
                      'DOUBLING': slots['certificates']['DOUBLING']['sha256'], 'LO_NGC': slots['certificates']['LO_NGC']['sha256'],
                      'B1': slots['identity_gate_records']['Z2']['sha256'], 'B1_OFF': slots['identity_gate_records']['Z2_OFF_RO1']['sha256'],
                      'B0prime_RERUN': slots['identity_gate_records']['B0prime_RERUN']['sha256'], 'B2': C.sha(B2_REC)})

    def gates_body(sha_=None, status=None, shas=None, **over):
        hit = []
        gs = dict(GATE_SHAS if shas is None else shas)
        body = {'schema': M.SCHEMA_REPORT + '_GATES_ONLY', 'blinded': True,
                'statement': 'gate statuses and reason codes only; case results read by sha256 of their bytes only; no row value or record number is written or printed',
                'test_mode': False, 'route_a_mode': 'parallel8', 'script_sha256': sha_ or sc_sha,
                'gates': {g: gate_entry(g, gs.get(g), (status or {}).get(g, 'PASS')) for g in M.ALL_GATES},
                'mt_crosscheck': 'NOT_APPLICABLE',
                'identity_runs': M.blind_strings({n: {'valid': True, 'codes': []} for n in M.IDENTITY_RUNS}, hit)}
        body['blinding_redaction_applied'] = bool(hit)
        body.update(over)
        M.assert_no_numbers(body)
        return body

    def validity_body(sha_=None, valid=True, **over):
        v = {'label': 'C5H', 'present': True, 'valid_all': valid, 'failed': [] if valid else ['V1'], 'reading': None, 'V1_codes': [], 'V2_codes': [],
             'V3_mismatch': [], 'V6_codes': [], 'misses': [], 'V1': valid, 'V2': True, 'V3': True, 'ro1': {}, 'uvt': {}}
        body = {'schema': M.SCHEMA_REPORT + '_VALIDITY_ONLY', 'blinded': True,
                'statement': 'validity/admissibility booleans and reason codes only; no row value, speed or other number is written or printed (A47 I3)',
                'test_mode': False, 'route_a_mode': 'parallel8', 'script_sha256': sha_ or sc_sha, 'cases': {'C5H': M.blinded_case(v)},
                'I1T_gate': gate_entry('I1T', None, 'NO_RUN'), 'B0_gate': gate_entry('B0', None)}
        body.update(over)
        M.assert_no_numbers(body)
        return body
    nb = [0]

    def body_file(body, name='GATES_ONLY.json'):
        nb[0] += 1
        return xw(run / ('b6_%02d' % nb[0]) / name, json.dumps(body, indent=1) + '\n')
    kmap = xw(run / 'KEY_EQUIVALENCE_MAP_C4CHK.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': [], 'note': 'synthetic test input (equals the case block map [])'})
    newl = xw(run / 'NEW_ITEM_DISPOSITIONS_C4CHK.json', {'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': pin(R12_IMPL),
                                                          'items': [{'id': 'NEW-71', 'disposition': 'ADOPTED', 'reason': 'synthetic test row', 'must_fail_tests': ['T_X']}]})
    cust = xw(run / 'RAW_SUCCESSOR_CUSTODY_C4CHK.json', {'schema': T4.CUSTODY_SCHEMA, 'identity_run': 'Z2', 'driver_sha256': dsha, 'stages_total': 21,
                                                          'stages_successor': 21, 'verdict': 'PASS', 'method': 'synthetic test input (root\'s check, A59)'})

    class A:
        pass

    def args_for(sl_p=None, sp_p=None, sc_p=None, tor=None, cov=None, **over):
        a = A()
        a.slots, a.prereg, a.text_of_record = str(sl_p or slots_p), str(sp_p or sp), str(tor or R5S)
        a.text_of_record_sha = C.sha(a.text_of_record)
        a.frozen, a.covered_later = str(frozen), list(COV if cov is None else cov)
        a.reviewed, a.sealed_compare = str(R12), str(sc_p or sc)
        sh = C.sha(a.sealed_compare)
        a.gates_only_output = str(body_file(gates_body(sh)))
        a.validity_only_output = str(body_file(validity_body(sh), 'VALIDITY_ONLY.json'))
        a.key_equivalence_map, a.new_item_list, a.successor_custody, a.b2_record = str(kmap), str(newl), str(cust), str(B2_REC)
        a.__dict__.update(over)
        return a
    a0 = args_for()
    res4, text4 = T4.safe_build(a0)
    expect_pass('base', 'BASE', 'builder: SEAL_RECORD built from the r5-based base (B6 bodies made with r12\'s own blinding functions)', res4)
    rec4 = json.loads(text4) if text4 else {}
    seal_p = xw(run / 'SEAL_RECORD_C4CHK.json', text4 or '{}\n')
    check('base', 'BASE', 'builder: printed seal_record_sha256 equals the sha of the bytes written (utf-8)', res4.get('seal_record_sha256') == C.sha(seal_p), str(res4.get('seal_record_sha256')))
    check('base', 'REAL', 'SEAL_RECORD carries case block 76309ae3, BUILD_V007 94bc05a5 with its 15 sources, the launch entry, the CMA stand-in, ROOT_ARGUMENT, B2 disclosure, E5-08, entry table',
          rec4.get('case_block') == pin(CASE_BLOCK) and rec4.get('build') == pin(BUILD_V007) and len(rec4.get('admission_allowlist') or {}) == 15
          and rec4.get('launch_entry') == slots['admission_entry'] and rec4.get('cascade_map_r5_addendum') == slots['cascade_map_r5_addendum']
          and rec4.get('text_of_record_pinned_by') == 'ROOT_ARGUMENT' and (rec4.get('b2_disclosure') or {}).get('record') == pin(B2_REC)
          and any(t.startswith('Disclosure E5-08') for t in rec4.get('disclosures', [])) and (rec4.get('entry_table') or {}).get('key') == 'entries_after_A81'
          and len(((rec4.get('entry_table') or {}).get('table') or {}).get('rows', [])) == 20, 'record content')
    allow = rec4.get('admission_allowlist') or {}
    cfg = {'schema': C.ADMISSION_SCHEMA, 'authority': dict(C.AUTHORITY), 'seal': pin(seal_p), 'prereg': rec4.get('prereg'), 'compare': rec4.get('compare'),
           'build': rec4.get('build'), 'producer_allowlist': allow}
    cfg_p = xw(run / 'ROOT_SEAL_ADMISSION_C4CHK.json', cfg)
    expect_pass('base', 'BASE', 'admission-config check on the base SEAL_RECORD', T4.check_admission_config(str(cfg_p), str(seal_p)))
    G.CONFIG = cfg_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_p)
    try:
        G.admission(str(LAUNCHER))
        oa = 'ok'
    except BaseException as e:
        oa = '%s: %s' % (type(e).__name__, e)
    check('integration', 'REAL', 'real guard v008 admission() accepts the config built on the r5-based SEAL_RECORD', oa == 'ok', oa)
    G.CONFIG = run / 'NO_CONFIG_YET.json'
    os.environ.pop('UNT_ROOT_ADMISSION_SHA256', None)
    # the SEALED compare's own functions (scratch sealed compare loaded from its own bytes): activate the driver BUILD record,
    # validate the case block, and load the slot's registry (the sealed-mode order)
    MS = C.load_reviewed_compare(str(sc), sc_sha)
    try:
        bS = MS.activate_driver_build(MS.load_driver_build_record(MS.PIN_DRIVER_BUILD_RECORD[0], MS.PIN_DRIVER_BUILD_RECORD[1])[0])
        cbS = MS.load_strict_file(str(CASE_BLOCK), 'case block')
        whyS = MS.validate_case_block(cbS, route_a_mode='parallel8')
        regS = MS.load_producer_registry(MS.PIN_PRODUCER_REGISTRY[0], MS.PIN_PRODUCER_REGISTRY[1])
        oS = 'ok' if (bS.get('build') == 'r5' and whyS == [] and isinstance(regS, dict)) else 'why %r' % (whyS,)
    except BaseException as e:
        oS = '%s: %s %s' % (type(e).__name__, getattr(e, 'refusal_code', ''), str(e)[:200])
    check('integration', 'REAL', 'the scratch SEALED compare\'s own activate_driver_build, validate_case_block (76309ae3) and load_producer_registry (C3V009) accept the base', oS == 'ok', oS)
    # =========================================================== D-01
    G1 = 'D-01'

    def cert_mut(name, kind, mutate, src=None):
        d = json.loads(Path(src or CERTS[kind]).read_bytes())
        mutate(d)
        f = xw(run / ('CERT_%s_C4CHK.json' % name), d)
        return variant('cert_' + name, lambda s: s['certificates'].update({kind: pin(f)}))
    for name, kind, mut, code in (
            ('dbl_float', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=128.0), 'CERTIFICATE_M_S'),
            ('dbl_string', 'DOUBLING', lambda d: d.update(ddo_gas_M_s='128'), 'CERTIFICATE_M_S'),
            ('dbl_bool', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=True), 'CERTIFICATE_M_S'),
            ('dbl_null', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=None), 'CERTIFICATE_M_S'),
            ('dbl_ngchalf_Ms128', 'DOUBLING', lambda d: d['ngc_half'].update(M_s=128), 'CERTIFICATE_M_S'),
            ('dbl_ddohalf_Ms64', 'DOUBLING', lambda d: d['ddo_half'].update(M_s=64), 'CERTIFICATE_M_S'),
            ('dbl_gas_M_s_NGC128', 'DOUBLING', lambda d: d.update(gas_M_s_NGC=128), 'CERTIFICATE_M_S'),
            ('dbl_perK_Ms64', 'DOUBLING', lambda d: d['ddo_half']['per_K_big']['128'].update(gas_M_s=64), 'CERTIFICATE_M_S'),
            ('lo_echo_gas64', 'LO', lambda d: d.update(gas_M_s=64), 'CERTIFICATE_M_S'),
            ('lo_build_roster64', 'LO', lambda d: d['build']['roster_gas'].update(M_s=64), 'CERTIFICATE_M_S'),
            ('lo_no_source', 'LO', lambda d: d.pop('source_gas_M_s'), 'CERTIFICATE_STATES_NO_M_S'),
            ('lo_evidence64', 'LO', lambda d: d['source_gas_M_s_evidence']['read_from_V003'].update(gas_M_s=64), 'CERTIFICATE_M_S'),
            ('gq_ngc_renamed', 'GQ', lambda d: [r.update(roster='T120L_NGC') for r in d['rosters'] if r['roster'] == 'NGC_T120L'], 'CERTIFICATE_M_S'),
            ('gq_no_doubled', 'GQ', lambda d: d['rosters'][1].pop('M_s_doubled'), 'CERTIFICATE_M_S_DOUBLED'),
            ('gq_empty', 'GQ', lambda d: d.update(rosters=[]), 'CERTIFICATE_STATES_NO_M_S'),
            ('gq_top_DDO64', 'GQ', lambda d: d.update(gas_M_s_DDO=64), 'CERTIFICATE_M_S'),
            ('gq_top_NGC128', 'GQ', lambda d: d.update(gas_M_s_NGC=128), 'CERTIFICATE_M_S'),
            ('epsngc_Ms128', 'EPS_NGC', lambda d: d.update(M_s=128), 'CERTIFICATE_M_S'),
            ('longc_gas128', 'LO_NGC', lambda d: d.update(gas_M_s=128), 'CERTIFICATE_M_S'),
            ('eps_galaxy_ngc128', 'EPS', lambda d: d.update(extra=[{'galaxy': 'NGC3198', 'M_s': 128}]), 'CERTIFICATE_M_S')):
        s2, p2, sp2, sc2 = cert_mut(name, kind, mut)
        expect_refuse(G1, 'MUT', 'D-01 %s: %s' % (kind, name), t3(p2, sp2, full=False), code)
    s2, p2, sp2, sc2 = cert_mut('i1tngc_Ms96', 'I1T_NGC', lambda d: d.update(M_s=96))
    expect_pass(G1, 'MUT', 'D-01 I1T_NGC stating M_s 96 (consistent with the NGC slot) passes', t3(p2, sp2, full=False))
    for name, kind, mut in (('dbl_lowercase_ddo64', 'DOUBLING', lambda d: d.update(gas_M_s_ddo=64)),
                            ('dbl_dotted_key64', 'DOUBLING', lambda d: d.update(**{'gas.M_s': 64})),
                            ('dbl_Ms_value64', 'DOUBLING', lambda d: d.update(M_s_value=64)),
                            ('dbl_Ms_suffix_source64', 'DOUBLING', lambda d: d.update(gas_M_s_source=64))):
        s2, p2, sp2, sc2 = cert_mut(name, kind, mut)
        r_ = t3(p2, sp2, full=False)
        finding(G1, 'D-01 scan coverage: a contradicting M_s stated under key %s passes' % name, r_.get('verdict') == 'PASS', r_,
                'MS_KEY_RX only matches keys ending M_s / M_s_DDO / M_s_NGC after start, _ or /')
    # GQ V005 (A86 superseded; real record, registered? no) in the GQ slot
    s2, p2, sp2, sc2 = variant('gq_v005', lambda s: s['certificates'].update(GQ=pin(GQ_V005)))
    r_ = t3(p2, sp2, full=False)
    finding(G1, 'slot GQ = the superseded GQ_CERT_V005 fbceefe6 (A86; not in registry C3V009 gate_records.GQ)', r_.get('verdict') == 'PASS', r_,
            'tool 3 checks gate, schema and M_s of the slot record, never that it is the registry\'s record of record')
    reg = json.loads(REGISTRY.read_bytes())
    check(G1, 'INFO', 'registry C3V009 gate_records.GQ does not list fbceefe6 (so the sealed compare would read the slot\'s record as unregistered)',
          GQ_V005 and REAL[GQ_V005] not in (reg['gate_records'].get('GQ') or []), repr(reg['gate_records'].get('GQ')))
    # =========================================================== D-04 case block
    G4 = 'D-04'
    cb_real = json.loads(CASE_BLOCK.read_bytes())

    def cb_variant(name, raw_text):
        cbp = xw(run / ('CASE_BLOCK_%s_C4CHK.json' % name), raw_text)
        tor_x = tor_from(lambda d: d['binding_inputs'].update(case_block=pin(cbp)), 'tor_cb_%s.json' % name)
        sp_x = sealed_prereg(slots, tor_x, 'sp_cb_%s.json' % name)
        return tor_x, sp_x
    cbt = json.dumps(cb_real, indent=1)
    tor_x, sp_x = cb_variant('dupkey', cbt.replace('{\n "schema"', '{\n "schema": "x",\n "schema"', 1))
    expect_refuse(G4, 'MUT', 'D-04 a case block with a duplicate key (sha pinned)', t3(None, sp_x, tor_x, full=False), 'CASE_BLOCK_JSON')
    tor_x, sp_x = cb_variant('ab1', cbt.replace('{\n "schema"', '{\n "big": %s,\n "schema": "x",\n "schema"' % ('9' * 5000), 1))
    expect_refuse(G4, 'MUT', 'D-04 A-B1 class: a duplicate key behind a 5,000-digit integer in the case block', t3(None, sp_x, tor_x, full=False), 'CASE_BLOCK_JSON')
    cbk = copy.deepcopy(cb_real)
    cbk['cases']['C4T-KHI']['normalized_spec_equal']['/numerics']['uv_tail']['outer']['K_big_inverse_kpc'] = 128.0
    tor_x, sp_x = cb_variant('khi_alias', json.dumps(cbk, indent=1))
    expect_refuse(G4, 'MUT', 'D-04 a case block with C4T-KHI at K_big 128 (r12 validate_case_block refuses)', t3(None, sp_x, tor_x, full=False), 'CASE_BLOCK_INVALID')
    cbm = copy.deepcopy(cb_real)
    cbm['route_a_mode'] = 'serial_with_exemption'
    tor_x, sp_x = cb_variant('mode_serial', json.dumps(cbm, indent=1))
    r_ = t3(None, sp_x, tor_x, full=False)
    rec_(G4, 'INFO', 'D-04 a case block naming serial_with_exemption (prereg names none): tool 3 validates in that mode (r12 L5722 order)', True, r_.get('verdict'), codes_of(r_), 'INFO')
    tor_x = tor_from(lambda d: d['binding_inputs'].update(case_block={'path': 'relative/CASE_BLOCK.json', 'sha256': REAL[CASE_BLOCK]}), 'tor_cb_relpath.json')
    expect_refuse(G4, 'MUT', 'D-04 a relative case-block path', t3(None, sealed_prereg(slots, tor_x, 'sp_cb_relpath.json'), tor_x, full=False), 'CASE_BLOCK_PIN_SHAPE')
    s2, p2, sp2, sc2 = variant('dbr_wrongsha', lambda s: s['driver_build_record'].update(sha256='1' * 64))
    r_ = expect_refuse(G4, 'MUT', 'D-04 driver BUILD record pin wrong: the case block is then not validated (CASE_BLOCK_NOT_VALIDATED, layered)', t3(p2, sp2, full=False),
                       'CASE_BLOCK_NOT_VALIDATED')
    # registry the sealed compare refuses at load, but tool 3 only pins it
    regx = copy.deepcopy(reg)
    k0 = next(k for k, v in regx['producers'].items() if isinstance(v, list) and v)
    regx['producers'][k0] = regx['producers'][k0] + [regx['producers'][k0][0]]
    regx_p = xw(run / 'PRODUCER_REGISTRY_DUP_ENTRY_C4CHK.json', regx)
    s2, p2, sp2, sc2 = variant('reg_dup', lambda s: s.update(producer_registry=pin(regx_p)))
    try:
        M.load_producer_registry(str(regx_p), C.sha(regx_p))
        regload = 'loaded'
    except SystemExit as e:
        regload = 'REFUSED %s' % getattr(e, 'refusal_code', None)
    r_ = t3(p2, sp2, full=False)
    finding(G4, 'a producer registry r12 refuses at load (duplicate producer entry, A71: %s) passes tool 3' % regload, r_.get('verdict') == 'PASS' and regload != 'loaded', r_,
            'tool 3 pins the registry from bytes but never calls the compare\'s load_producer_registry')
    # =========================================================== D-07 pin shapes
    G7 = 'D-07'
    for name, mut in (('none', lambda s: s.update(frozen_addendum=None)), ('partial', lambda s: s.update(driver_build_record={'path': str(dbr)})),
                      ('extra_key', lambda s: s.update(producer_registry=dict(pin(REGISTRY), note='x'))), ('int', lambda s: s.update(compare_reviewed_source=42)),
                      ('list', lambda s: s.update(driver_check_record=[str(CHECK_MD), REAL[CHECK_MD]])),
                      ('bare_pending', lambda s: s.update(driver_build_record='PENDING_ROOT_AT_SEAL_ASSEMBLY'))):
        s2 = copy.deepcopy(slots)
        mut(s2)
        p2 = xw(run / ('slots_shape_%s.json' % name), s2)
        r_ = T2.run(str(R12), str(sc), str(p2), str(sp))
        expect_refuse(G7, 'MUT', 'D-07 tool 2: pin slot %s refuses PIN_SHAPE (never INTERNAL_EXCEPTION)' % name, r_, 'PIN_SHAPE', absent='INTERNAL_EXCEPTION')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = T2.main(['--reviewed', str(R12), '--sealed', str(sc), '--slots', str(p2), '--prereg', str(sp)])
        try:
            cli = json.loads(buf.getvalue())
        except ValueError:
            cli = {}
        check(G7, 'MUT', 'D-07 tool 2 CLI: pin slot %s exits 2 with a REFUSE verdict JSON' % name, rc == 2 and cli.get('verdict') == 'REFUSE', 'rc %r' % rc)
        r3_ = T3.run(str(p2), str(sp), str(R5S), None, (), None, None, trs)
        check(G7, 'MUT', 'D-07 tool 3: pin slot %s refuses with codes, never INTERNAL_EXCEPTION' % name,
              r3_['verdict'] == 'REFUSE' and not any(c.startswith('INTERNAL_EXCEPTION') for c in codes_of(r3_)), repr(codes_of(r3_)[:4]))
    for name, mut in (('certs_string', lambda s: s.update(certificates='PENDING_ROOT_AT_SEAL_ASSEMBLY')),
                      ('cert_entry_list', lambda s: s['certificates'].update(EPS=[str(CERTS['EPS']), REAL[CERTS['EPS']]])),
                      ('admission_entry_string', lambda s: s.update(admission_entry='PENDING')),
                      ('identity_entry_none', lambda s: s['identity_gate_records'].update(Z2=None))):
        s2 = copy.deepcopy(slots)
        mut(s2)
        p2 = xw(run / ('slots_shape_%s.json' % name), s2)
        r3_ = T3.run(str(p2), str(sp), str(R5S), None, (), None, None, trs)
        check(G7, 'MUT', 'D-07 tool 3: %s refuses with codes, never INTERNAL_EXCEPTION' % name,
              r3_['verdict'] == 'REFUSE' and not any(c.startswith('INTERNAL_EXCEPTION') for c in codes_of(r3_)), repr(codes_of(r3_)[:4]))
    bad_cmd = xw(run / 'BOUND_COMMAND_NOT_UTF8_C4CHK.txt', 'x')
    with open(bad_cmd, 'wb') as f:
        pass
    s2, p2, sp2, sc2 = variant('cmd_latin1', lambda s: s['launch_packet'].update(bound_command=rpin(bad_cmd)))
    r_ = t3(p2, sp2, full=False)
    rec_(G7, 'INFO', 'D-07 class: an empty bound command file', r_['verdict'] == 'REFUSE', r_['verdict'], codes_of(r_), 'REFUSE')
    # =========================================================== D-10 path_to_be
    G10 = 'D-10'
    real_r5_sp = sealed_prereg(slots, R5, 'KMAX_TAIL_PREREG_V007_SEALED_ON_REAL_R5_C4CHK.json')
    r_ = T3.run(str(slots_p), str(real_r5_sp), str(R5), str(frozen), COV, str(R12), str(sealed_compare(slots, real_r5_sp, 'sc_real_r5.py')), REAL[R5])
    cs = sorted(set(codes_of(r_)))
    check(G10, 'REAL', 'REAL r5 3245899f as the text of record (root states its sha): tool 3 refuses ONLY the path_to_be pair (reproduces builder F-06)',
          cs == ['FROZEN_SLOT_NOT_PATH_TO_BE', 'T1:FROZEN_PATH_NOT_PATH_TO_BE'], repr(cs))
    os.symlink(str(frozen), str(run / 'frozen_link'))
    link_dir = run / 'frozen_link_dir'
    link_dir.mkdir()
    os.symlink(str(frozen), str(link_dir / FROZEN_NAME))
    tor_l = tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(link_dir / FROZEN_NAME)), 'tor_ptb_symlink.json')
    sp_l = sealed_prereg(dict(slots), tor_l, 'sp_ptb_symlink.json')
    expect_refuse(G10, 'MUT', 'D-10 tool 1: path_to_be names a symlink to the frozen copy (the file at path_to_be is not the frozen file itself)',
                  T1.run(str(sp_l), str(link_dir / FROZEN_NAME), None, COV), 'FROZEN_PATH_NOT_PATH_TO_BE')
    tor_d = tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(frozen).replace('/frozen/', '/frozen//')), 'tor_ptb_double_slash.json')
    expect_refuse(G10, 'MUT', 'D-10 tool 1: path_to_be spelled with // (fail closed)', T1.run(str(sealed_prereg(slots, tor_d, 'sp_ptb_dslash.json')), str(frozen), None, COV),
                  'FROZEN_PATH_NOT_PATH_TO_BE')
    other_copy = xw(run / 'frozen_other' / FROZEN_NAME, ftext)
    expect_refuse(G10, 'MUT', 'D-10 tool 3: --frozen is a byte-identical copy elsewhere (FROZEN_ARG_NOT_THE_SLOT)', t3(frozen_p=other_copy), 'FROZEN_ARG_NOT_THE_SLOT')
    cwd = os.getcwd()
    os.chdir(str(run / 'frozen'))
    try:
        expect_pass(G10, 'MUT', 'D-10 tool 1: --frozen given relative to the cwd resolves to path_to_be', T1.run(str(sp), FROZEN_NAME, None, COV))
    finally:
        os.chdir(cwd)
    # =========================================================== R-04 B6 / B7
    G6 = 'R-04'

    def t4(name, code, tag='MUT', base=None, **over):
        b = A()
        b.__dict__.update((base or a0).__dict__)
        b.__dict__.update(over)
        r, t = T4.safe_build(b)
        ok = t is None and r['verdict'] == 'REFUSE' and any(code in f['code'] for f in r['failures'])
        rec_(G6, tag, name, ok, r['verdict'], codes_of(r), 'REFUSE ' + code)
        return r, t

    def t4_probe(name, detail, **over):
        b = A()
        b.__dict__.update(a0.__dict__)
        b.__dict__.update(over)
        r, t = T4.safe_build(b)
        finding(G6, name, r['verdict'] == 'PASS' and t is not None, r, detail)
        return r, t
    t4('R-04 GATES body: a JSON number nested in a gate entry', 'E_SEAL1_OUTPUT_VALUE_BEARING',
       gates_only_output=str(body_file(dict(gates_body(), gates=dict(gates_body()['gates'], EPS=dict(gates_body()['gates']['EPS'], n=3))))))
    t4('R-04 GATES body: a 64-hex sha in UPPER case is not masked (number run)', 'E_SEAL1_OUTPUT_VALUE_BEARING',
       gates_only_output=str(body_file(gates_body(mt_crosscheck='DEADBEEF' + '1234567890' * 5 + 'AB'))))
    t4('R-04 GATES body: A-B1 class (5,000-digit integer and a duplicate key)', 'E_SEAL1_OUTPUT_JSON',
       gates_only_output=str(xw(run / 'b6_ab1' / 'GATES_ONLY.json', '{"x": %s, "schema": "a", "schema": "b"}\n' % ('9' * 5000))))
    t4('R-04 GATES body: script_sha256 of the REVIEWED r12 (not the sealed compare)', 'E_SEAL1_SCRIPT_NOT_THE_SEALED_COMPARE', gates_only_output=str(body_file(gates_body(R12_SHA))))
    t4('R-04 VALIDITY body: test_mode true', 'E_SEAL1_TEST_MODE', validity_only_output=str(body_file(validity_body(test_mode=True), 'VALIDITY_ONLY.json')))
    t4('R-04 VALIDITY body: cases C5H plus C4T', 'E_SEAL1_VALIDITY_CASES_NOT_C5H',
       validity_only_output=str(body_file(validity_body(cases={'C5H': validity_body()['cases']['C5H'], 'C4T': validity_body()['cases']['C5H']}), 'VALIDITY_ONLY.json')))
    t4('R-04 the two B6 files swapped', 'E_SEAL1', gates_only_output=a0.validity_only_output, validity_only_output=a0.gates_only_output)
    t4_probe('R-04 GATES body showing DOUBLING and B2 FAIL (pre-seal gates) still yields a SEAL_RECORD', 'the builder never reads gate statuses',
             gates_only_output=str(body_file(gates_body(status={'DOUBLING': 'FAIL', 'B2': 'FAIL'}))))
    wrong = dict(GATE_SHAS, DOUBLING='5' * 64, GQ=REAL[GQ_V005])
    t4_probe('R-04 GATES body whose DOUBLING / GQ record_sha256 are not the slot records (GQ = superseded V005) still yields a SEAL_RECORD',
             'the builder never compares the B6 record_sha256 values with the slot certificates / identity records',
             gates_only_output=str(body_file(gates_body(shas=wrong))))
    t4_probe('R-04 VALIDITY body with C5H valid_all false still yields a SEAL_RECORD', 'the builder never reads the C5H admissibility it embeds',
             validity_only_output=str(body_file(validity_body(valid=False), 'VALIDITY_ONLY.json')))
    t4_probe('R-04 GATES body with a single gate entry (the r12 body carries every ALL_GATES entry)', 'gate completeness is not checked',
             gates_only_output=str(body_file(gates_body(gates={'B0': gates_body()['gates']['B0']}))))
    impl_text = R12_IMPL.read_bytes().decode('utf-8')
    impl_ids = sorted(set(re.findall(r'\bNEW-\d{1,3}\b', impl_text)), key=lambda x: int(x[4:]))
    t4_probe('R-04/B7 a NEW-item list with 1 of the %d NEW ids the r12 IMPL names still yields a SEAL_RECORD' % len(impl_ids),
             'the list is not checked for completeness against the IMPL (A81 RI-20: the IMPL lists each NEW item; the seal record quotes that list)')
    t4_probe('R-04/B7 a NEW-item list naming an id the IMPL never declares (NEW-999)', 'ids are not checked against the IMPL',
             new_item_list=str(xw(run / 'NEW_ITEMS_UNKNOWN_ID_C4CHK.json', dict(json.loads(newl.read_bytes()), items=[{'id': 'NEW-999', 'disposition': 'ADOPTED',
                                                                                                                      'reason': 'x', 'must_fail_tests': ['T']}]))))
    t4_probe('R-04/B7 NEW-71 and NEW-071 both listed (one item, two spellings)', 'the id is a string, not a number: NEW-071 is not a duplicate of NEW-71',
             new_item_list=str(xw(run / 'NEW_ITEMS_ZERO_PAD_C4CHK.json', dict(json.loads(newl.read_bytes()), items=json.loads(newl.read_bytes())['items'] + [
                 {'id': 'NEW-071', 'disposition': 'REJECTED', 'reason': 'x', 'must_fail_tests': []}]))))
    t4_probe('R-04/B7 raw successor custody with no evidence pins', 'evidence is optional (A59 check is root\'s); FORMAL by design',
             successor_custody=str(cust))
    t4('R-04/B7 custody stages_total as a bool', 'CUSTODY_STAGES',
       successor_custody=str(xw(run / 'CUSTODY_BOOL_C4CHK.json', dict(json.loads(cust.read_bytes()), stages_total=True, stages_successor=True))))
    t4('R-04/B7 key map with an extra top-level key', 'KEY_MAP_SCHEMA',
       key_equivalence_map=str(xw(run / 'KEYMAP_EXTRA_C4CHK.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': [], 'extra': 1})))
    # =========================================================== R-10
    G10b = 'R-10'
    t4('R-10 SEAL key map [one entry] while the case block 76309ae3 map is []', 'KEY_MAP_NOT_THE_CASE_BLOCK_MAP', tag='MUT',
       key_equivalence_map=str(xw(run / 'KEYMAP_ONE_C4CHK.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': [
           {'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0, 'b0_identity_evidence': 'x'}]})))
    # =========================================================== BUILD_V007 (A99.1) and the launch packet
    GB = 'BUILD'
    allow7 = C.build_allowlist(BUILD_V007.read_bytes().decode('utf-8'))
    tpl_line = '%s  %s' % (REAL[TEMPLATE_V011], TEMPLATE_V011)

    def build_standin(sub, entries, extra=''):
        body = ('# BUILD_V007 stand-in (Claude4 helper test fixture; NOT the BUILD of record)\n\n## Supported runtime entry allowlist\n\n```text\n'
                + ''.join('%s  %s\n' % (h, p) for h, p in entries) + extra + '```\n\n## Byte-pinned evidence\n\n```text\n' + tpl_line + '\n```\n')
        return xw(run / sub / 'BUILD_V007.md', body)

    def build_case(sub, entries, extra=''):
        bx = build_standin(sub, entries, extra)
        tor_x = tor_from(lambda d: d['seal_slots']['launch_packet']['named_candidates_verified_from_bytes'].update(build=pin(bx)), 'tor_%s.json' % sub)
        return variant(sub, lambda s: s['launch_packet'].update(build=pin(bx)), tor=tor_x) + (tor_x,)
    s2, p2, sp2, sc2, tor_x = build_case('build_upper16', allow7, extra='%s  %s\n' % (allow7[0][0].upper(), '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/x_extra16.py'))
    r_ = t3(p2, sp2, tor_x, full=False)
    finding(GB, 'a BUILD_V007 whose allowlist section carries a 16th source line in upper-case hex passes as 15 sources', r_['verdict'] == 'PASS', r_,
            'build_allowlist ignores lines that do not match its exact regex inside the section')
    s2, p2, sp2, sc2, tor_x = build_case('build_twosec', allow7)
    rec_(GB, 'INFO', 'control: the stand-in BUILD_V007 with the real 15 entries passes', t3(p2, sp2, tor_x, full=False)['verdict'] == 'PASS', '', [], 'PASS')
    s2, p2, sp2, sc2, tor_x = build_case('build_space_path', allow7[:14] + [(allow7[14][0], allow7[14][1].replace('/claude_artifacts/', '/claude artifacts/'))])
    expect_refuse(GB, 'MUT', 'a BUILD_V007 with one path containing a space (the parser skips it: 14 sources)', t3(p2, sp2, tor_x, full=False), 'BUILD_ALLOWLIST_COUNT_NOT_15')
    # the plan's launcher swapped to another allowlisted source (command and admission entry consistent)
    other = next({'path': p, 'sha256': h} for h, p in allow7 if 'aggregate_records' in p)
    plan2 = copy.deepcopy(plan)
    plan2['launcher'] = other
    plan2_p = xw(run / 'BOUND_PLAN_LAUNCHER_SWAPPED_C4CHK.json', json.dumps(plan2, indent=1) + '\n')
    cmd2_p = xw(run / 'BOUND_COMMAND_LAUNCHER_SWAPPED_C4CHK.txt', cmd_p.read_bytes().decode('utf-8').splitlines()[0] + '\n'
                + shlex.join([C.PYTHON, '-I', '-B', other['path'], str(plan2_p.resolve()), '--execute-root-only']) + '\n')
    s2, p2, sp2, sc2 = variant('launcher_swapped', lambda s: (s['launch_packet'].update(bound_plan=rpin(plan2_p), bound_command=rpin(cmd2_p)),
                                                              s['admission_entry'].update(launcher=dict(other))))
    r_ = t3(p2, sp2, full=False)
    finding(GB, 'a bound plan whose launcher is aggregate_records_cx1v008.py (an allowlisted producer, not the launcher) passes tool 3',
            r_['verdict'] == 'PASS', r_, 'launcher / guard are checked only for BUILD_V007 allowlist membership, not against the r5-named launcher 861bba68 / guard 294cb776')
    # the plan's calls swapped (template_pin still V011)
    plan3 = copy.deepcopy(plan)
    plan3['calls'][1]['spec'], plan3['calls'][2]['spec'] = plan3['calls'][2]['spec'], plan3['calls'][1]['spec']
    plan3_p = xw(run / 'BOUND_PLAN_SPECS_SWAPPED_C4CHK.json', json.dumps(plan3, indent=1) + '\n')
    cmd3_p = xw(run / 'BOUND_COMMAND_SPECS_SWAPPED_C4CHK.txt', cmd_p.read_bytes().decode('utf-8').splitlines()[0] + '\n'
                + shlex.join([C.PYTHON, '-I', '-B', plan3['launcher']['path'], str(plan3_p.resolve()), '--execute-root-only']) + '\n')
    s2, p2, sp2, sc2 = variant('specs_swapped', lambda s: s['launch_packet'].update(bound_plan=rpin(plan3_p), bound_command=rpin(cmd3_p)))
    r_ = t3(p2, sp2, full=False)
    finding(GB, 'a bound plan with two calls\' specs swapped (template_pin still V011) passes tool 3', r_['verdict'] == 'PASS', r_,
            'the plan is not compared with the template (A81 RI-25 makes a template-equality check optional)')
    # the bound command's first line replaced by a shell command
    cmd4_p = xw(run / 'BOUND_COMMAND_LINE1_SHELL_C4CHK.txt', 'touch /tmp/claude4_probe_never_run\n' + cmd_p.read_bytes().decode('utf-8').splitlines()[1] + '\n')
    s2, p2, sp2, sc2 = variant('cmd_line1', lambda s: s['launch_packet'].update(bound_command=rpin(cmd4_p)))
    r_ = t3(p2, sp2, full=False)
    finding(GB, 'a bound command whose first line is a shell command (not the binder\'s comment) passes tool 3', r_['verdict'] == 'PASS', r_,
            'only the last line is compared with the binder line; line 1 is unchecked (the file never ran here)')
    # =========================================================== text of record (r2 root argument)
    GT = 'TOR'
    r_ = T3.run(str(slots_p), str(sp), str(sp), str(frozen), COV, str(R12), str(sc), C.sha(sp))
    finding(GT, 'root names the SEALED prereg itself as the text of record (its own sha): tool 3 passes', r_['verdict'] == 'PASS', r_,
            'the outside-slot text check becomes self-comparison; the v001 constant pin made this impossible')
    sp_edit = sealed_prereg(slots, R5S, 'prereg_tests_T3_edited.json', mutate=lambda d: d['tests']['T3'].update(text=d['tests']['T3']['text'] + ' EDITED THRESHOLD'))
    expect_refuse(GT, 'MUT', 'control: an edited T3 text in the sealed prereg against the scratch r5 text of record', t3(None, sp_edit, full=False), 'SEALED_PREREG_TEXT_CHANGED')
    r_ = T3.run(str(slots_p), str(sp_edit), str(sp_edit), None, (), None, None, C.sha(sp_edit))
    finding(GT, 'the same edited sealed prereg named as its own text of record passes tool 3 (the edit is invisible)', r_['verdict'] == 'PASS', r_,
            'needs a guard: the text of record must hold PENDING slot values / differ from the sealed prereg / be r5 3245899f')
    s_sc = sealed_compare(slots, sp_edit, 'sc_edit.py')
    b_ = A()
    b_.__dict__.update(args_for(sp_p=sp_edit, sc_p=s_sc).__dict__)
    b_.text_of_record, b_.text_of_record_sha = str(sp_edit), C.sha(sp_edit)
    r_b, t_b = T4.safe_build(b_)
    finding(GT, 'the builder then prints a SEAL_RECORD for the edited sealed prereg (text_of_record = the sealed prereg, pinned_by ROOT_ARGUMENT)',
            r_b['verdict'] == 'PASS' and t_b is not None, r_b, 'same root cause as the tool 3 probe')
    expect_refuse(GT, 'MUT', 'root states an upper-case sha', T3.run(str(slots_p), str(sp), str(R5S), None, (), None, None, trs.upper()), 'TEXT_OF_RECORD_SHA_ARG_MISMATCH')
    expect_refuse(GT, 'MUT', 'no root argument while the pin is PENDING', T3.run(str(slots_p), str(sp), str(R5S), None, (), None, None, None), 'TEXT_OF_RECORD_PIN_PENDING')
    # =========================================================== tool 1 entry table
    GE = 'A99.3'
    expect_refuse(GE, 'MUT', 'tool 1: --covered-later empty with A102 present (UNCOVERED_LATER_ENTRY)', T1.run(str(sp), str(frozen), None, []), 'UNCOVERED_LATER_ENTRY')
    expect_refuse(GE, 'MUT', 'tool 1: --covered-later A101 (cited by r5)', T1.run(str(sp), str(frozen), None, ['A101'] + COV), 'COVERED_LATER_IS_CITED')
    f99 = xw(run / 'variant_A99' / FROZEN_NAME, ftext.replace('**Rulings:**\n1. **D-02.', '**Rulings:**\n1. **D-02 (edited).', 1))
    tor_99 = tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(f99)), 'tor_A99.json')
    sl99 = copy.deepcopy(slots)
    sl99['frozen_addendum'] = pin(f99)
    sp99 = sealed_prereg(sl99, tor_99, 'sp_A99.json')
    expect_refuse(GE, 'MUT', 'tool 1: an edit inside A99 (a table row) is detected', T1.run(str(sp99), str(f99), None, COV), 'ENTRY_TABLE_SECTION_CHANGED')
    expect_pass(GE, 'MUT', 'tool 1: the A99 edit with root\'s note (--covered-later A99,...)', T1.run(str(sp99), str(f99), None, ['A99'] + COV), note='ENTRY_TABLE_SECTION_CHANGED_NOTED')
    old_marker = '## A62: launch packet reviewed'
    i62 = ftext.index(old_marker)
    j62 = ftext.index('\n', ftext.index('**Review.**', i62))
    f62 = xw(run / 'variant_A62' / FROZEN_NAME, ftext[:j62] + ' EDITED AFTER r5 WAS WRITTEN.' + ftext[j62:])
    tor_62 = tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(f62)), 'tor_A62.json')
    sl62 = copy.deepcopy(slots)
    sl62['frozen_addendum'] = pin(f62)
    sp62 = sealed_prereg(sl62, tor_62, 'sp_A62.json')
    r_ = T1.run(str(sp62), str(f62), None, COV)
    finding(GE, 'tool 1: an edit inside cited entry A62 (before A82, no table row) after r5 was written passes', r_['verdict'] == 'PASS', r_,
            'only A82+ sections are re-hashed; A47-A81 are checked for heading presence only (A81 RI-26 asks presence)')
    # =========================================================== tool 2 cited addendum (A82 hazard)
    GS = 'T2'
    f_short = xw(run / 'variant_short' / FROZEN_NAME, ftext[:-1] if ftext.endswith('\n') else ftext + '\n')
    sls = copy.deepcopy(slots)
    sls['frozen_addendum'] = pin(f_short)
    tor_s = tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(f_short)), 'tor_short.json')
    sps = sealed_prereg(sls, tor_s, 'sp_short.json')
    sls_p = xw(run / 'slots_short.json', sls)
    expect_refuse(GS, 'MUT', 'tool 2: a frozen copy whose bytes differ from the open V005 file the compare hashes (A82 hazard)',
                  T2.run(str(R12), str(sealed_compare(sls, sps, 'sc_short.py')), str(sls_p), str(sps)), 'CITED_ADDENDUM_BYTES_NOT_PINNED')

    def edit_pin(nm_, new_rhs):
        def ed(out):
            i = next(i for i, l in enumerate(out) if l.startswith(nm_ + ' = '))
            body, _, comment = out[i].partition('#')
            out[i] = '%s = %s   #%s' % (nm_, new_rhs, comment)
            return out
        return ed
    expect_refuse(GS, 'MUT', 'tool 2: a pin line with a trailing statement', T2.run(str(R12), str(sealed_compare(slots, sp, 'sc_semicolon.py',
                  lambda o: [l.replace("'%s'" % C.sha(sp), "'%s'; V007_PREREG_SHA256 = None" % C.sha(sp), 1) if l.startswith('V007_PREREG_SHA256 = ') else l for l in o])),
                  str(slots_p), str(sp)), 'PIN_')
    # =========================================================== v001 40 cases, ported to v002 on the r5-based base (tag V001PORT)
    GP = 'V001PORT'
    expect_pass(GP, 'V001PORT', 'T1 genuine', T1.run(str(sp), str(frozen), None, COV))
    fa = xw(run / 'p_a' / FROZEN_NAME, ftext.replace('## A60:', '## A60 (heading removed):', 1))
    expect_refuse(GP, 'V001PORT', 'T1 cited entry A60 absent', T1.run(str(sealed_prereg(dict(slots, frozen_addendum=pin(fa)), tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(fa)), 'tor_p_a.json'), 'sp_p_a.json')), str(fa), None, COV), 'CITED_ENTRY_ABSENT_FROM_FROZEN')

    def t1_on(fx, name):
        torx = tor_from(lambda d: d['seal_slots']['frozen_addendum'].update(path_to_be=str(fx)), 'tor_%s.json' % name)
        return T1.run(str(sealed_prereg(dict(slots, frozen_addendum=pin(fx)), torx, 'sp_%s.json' % name)), str(fx), None, COV)
    fb = xw(run / 'p_b' / FROZEN_NAME, ftext + '\n## A70: duplicate entry\n')
    expect_refuse(GP, 'V001PORT', 'T1 duplicate heading', t1_on(fb, 'p_b'), 'DUPLICATE_ENTRY_HEADING')
    fc = xw(run / 'p_c' / FROZEN_NAME, ftext + '\nsealed prereg %s\n' % C.sha(sp))
    expect_refuse(GP, 'V001PORT', 'T1 frozen cites the sealed prereg sha', T1.run(str(sp), str(fc), None, COV), 'FROZEN_CITES_SEALED_PREREG_SHA')
    expect_refuse(GP, 'V001PORT', 'T1 later entry uncovered', T1.run(str(sp), str(frozen), None, []), 'UNCOVERED_LATER_ENTRY')
    fe = xw(run / 'p_e' / 'V005_ADDENDUM_COPY.md', ftext)
    expect_refuse(GP, 'V001PORT', 'T1 not the _FROZEN copy', T1.run(str(sp), str(fe), None, COV), 'NOT_THE_FROZEN_COPY')
    expect_refuse(GP, 'V001PORT', 'T1 expected sha differs', T1.run(str(sp), str(frozen), '0' * 64, COV), 'FROZEN_SHA_MISMATCH')
    expect_refuse(GP, 'V001PORT', 'T1 covered-later names an absent entry', T1.run(str(sp), str(frozen), None, COV + ['A%d' % (NMAX + 7)]), 'COVERED_LATER_NOT_IN_FROZEN')
    dj = xw(run / 'p_dup_prereg.json', sp.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "dup",\n "schema"', 1))
    expect_refuse(GP, 'V001PORT', 'T1 prereg JSON with a duplicate key', T1.run(str(dj), str(frozen), None, COV), 'PREREG_JSON')
    expect_pass(GP, 'V001PORT', 'T2 genuine', T2.run(str(R12), str(sc), str(slots_p), str(sp)))

    def t2_edit(name, ed, sl=None, spx=None, other_prereg=None):
        slx = sl or slots
        spx = spx or sp
        scx = sealed_compare(slx, other_prereg or spx, 'p2_%s.py' % name, ed)
        return T2.run(str(R12), str(scx), str(slots_p), str(spx))

    def nonpin(out):
        i = next(i for i, l in enumerate(out) if l.startswith('ART = '))
        out[i] = out[i].rstrip('\n') + '  # tampered\n'
        return out
    expect_refuse(GP, 'V001PORT', 'T2 a non-pin line changed', t2_edit('nonpin', nonpin), 'NON_PIN_LINE_DIFFERS')
    expect_refuse(GP, 'V001PORT', 'T2 pin value for another prereg', t2_edit('otherprereg', None, other_prereg=R5), 'PIN_VALUE_MISMATCH')
    expect_refuse(GP, 'V001PORT', 'T2 inserted line', t2_edit('inserted', lambda o: o[:10] + ['# inserted\n'] + o[10:]), 'LINE_COUNT_DIFFERS')

    def second_assign(out):
        i = next(i for i, l in enumerate(out) if l.startswith('#'))
        out[i] = "V007_PREREG_SHA256 = '%s'\n" % ('0' * 64)
        return out
    expect_refuse(GP, 'V001PORT', 'T2 second assignment of a pin', t2_edit('second', second_assign), 'NON_PIN_LINE_DIFFERS')

    def chg_comment(out):
        i = next(i for i, l in enumerate(out) if l.startswith('V007_PREREG_SHA256 = '))
        out[i] = out[i].replace('# PENDING_FROM_BYTES', '# EDITED')
        return out
    expect_refuse(GP, 'V001PORT', 'T2 pin comment changed', t2_edit('comment', chg_comment), 'PIN_COMMENT_CHANGED')

    def as_list(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_PRODUCER_REGISTRY = '))
        out[i] = 'PIN_PRODUCER_REGISTRY = %r\n' % [slots['producer_registry']['path'], slots['producer_registry']['sha256']]
        return out
    expect_refuse(GP, 'V001PORT', 'T2 pair pin as a list', t2_edit('aslist', as_list), 'PIN_PAIR_SHAPE')

    def unset(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_V010_R5_CHECK = '))
        out[i] = 'PIN_V010_R5_CHECK = None\n'
        return out
    expect_refuse(GP, 'V001PORT', 'T2 one pin left unset', t2_edit('unset', unset), 'PIN_NOT_SET')
    rvc = xw(run / 'p_reviewed_copy.py', R12.read_bytes().decode('utf-8'))
    expect_refuse(GP, 'V001PORT', 'T2 reviewed path not the slot', T2.run(str(rvc), str(sc), str(slots_p), str(sp)), 'REVIEWED_PATH_NOT_THE_SLOT')
    expect_refuse(GP, 'V001PORT', 'T2 sealed is the reviewed file', T2.run(str(R12), str(R12), str(slots_p), str(sp)), 'SEALED_IS_REVIEWED')
    spj = sealed_prereg(slots, R5S, 'p_sp_j.json', mutate=lambda d: d['seal_slots']['compare'].update(value=pin(sc)))
    expect_refuse(GP, 'V001PORT', 'T2 prereg compare slot holds the sealed compare', T2.run(str(R12), str(sealed_compare(slots, spj, 'p_sc_j.py')), str(slots_p), str(spj)),
                  'PREREG_COMPARE_SLOT_DIFFERS')
    expect_pass(GP, 'V001PORT', 'T3 genuine', t3())
    s2, p2, sp2, _ = variant('p_pending', lambda s: s.update(producer_registry={'path': str(REGISTRY), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    expect_refuse(GP, 'V001PORT', 'T3 a PENDING value', t3(p2, sp2, full=False), 'PENDING')
    s2, p2, sp2, _ = variant('p_badpin', lambda s: s['identity_gate_records']['Z2'].update(sha256='0' * 64))
    expect_refuse(GP, 'V001PORT', 'T3 identity record pin bytes differ', t3(p2, sp2, full=False), 'PIN_BYTES_MISMATCH')
    s2, p2, sp2, _ = variant('p_text', lambda s: None, prereg_mutate=lambda d: d['tests']['T3'].update(text=d['tests']['T3']['text'] + ' (edited)'))
    expect_refuse(GP, 'V001PORT', 'T3 sealed prereg text changed outside the slots', t3(p2, sp2, full=False), 'SEALED_PREREG_TEXT_CHANGED')
    p_sd = xw(run / 'slots_p_slotdiff.json', dict(copy.deepcopy(slots), producer_registry=pin(CHECK_MD)))
    expect_refuse(GP, 'V001PORT', 'T3 prereg slot value differs from the slots', t3(p_sd, sp, full=False), 'PREREG_SLOT_VALUE_DIFFERS')
    s2, p2, sp2, _ = variant('p_alias', lambda s: s.update(driver={'path': str(DRIVER).replace('/driver_r5/', '/driver_r5/./'), 'sha256': dsha}))
    expect_refuse(GP, 'V001PORT', 'T3 driver slot spelled differently from the plan', t3(p2, sp2, full=False), 'PLAN_DRIVER_NOT_THE_SLOT')
    bad_id = xw(run / 'IDENTITY_Z2_OTHER_DRIVER_C4CHK.json', {'schema': M.GATE_SCHEMA, 'gate': 'B1', 'NEW_DRIVER_PIN': {'pass': True, 'detail': {'result_json_driver_sha256': '2' * 64}}})
    s2, p2, sp2, _ = variant('p_iddriver', lambda s: s['identity_gate_records'].update(Z2=pin(bad_id)))
    expect_refuse(GP, 'V001PORT', 'T3 identity record carries another driver', t3(p2, sp2, full=False), 'IDENTITY_RECORD')
    lo64 = json.loads(CERTS['LO'].read_bytes())
    lo64['source_gas_M_s'] = 64
    lo64_p = xw(run / 'LO_M_S64_C4CHK.json', lo64)
    s2, p2, sp2, _ = variant('p_lo64', lambda s: s['certificates'].update(LO=pin(lo64_p)))
    expect_refuse(GP, 'V001PORT', 'T3 LO certificate at M_s 64', t3(p2, sp2, full=False), 'CERTIFICATE_M_S')
    cdir = run / 'cache_nonempty'
    cdir.mkdir()
    xw(cdir / 'prewarmed.bin', 'x')
    s2, p2, sp2, _ = variant('p_r6full', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir)}, cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    expect_refuse(GP, 'V001PORT', 'T3 r6 cache directory not empty (pre-warmed)', t3(p2, sp2, full=False), 'CACHE_DIRECTORY_NOT_EMPTY')
    cdir2 = run / 'cache_empty'
    cdir2.mkdir()
    s2, p2, sp2, _ = variant('p_r6empty', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir2)}, cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    expect_refuse(GP, 'V001PORT', 'T3 r6 with an empty cache dir: v001 PASS; v002 refuses only for the r5 driver BUILD record (A96)', t3(p2, sp2, full=False),
                  'DRIVER_BUILD_NOT_THE_BRANCH', absent='CACHE_DIRECTORY')
    s2, p2, sp2, _ = variant('p_r5cache', lambda s: s.update(cache_directory_r6_only={'path': str(cdir2)}))
    expect_refuse(GP, 'V001PORT', 'T3 r5 slot set naming a cache directory', t3(p2, sp2, full=False), 'CACHE_DIRECTORY_UNDER_R5')
    cmde = xw(run / 'BOUND_COMMAND_EDITED_C4CHK.txt', cmd_p.read_bytes().decode('utf-8').replace('--execute-root-only', '--execute-root-only --worker'))
    s2, p2, sp2, _ = variant('p_cmd', lambda s: s['launch_packet'].update(bound_command=rpin(cmde)))
    expect_refuse(GP, 'V001PORT', 'T3 bound command edited', t3(p2, sp2, full=False), 'BOUND_COMMAND_NOT_THE_BINDER_LINE')
    dups = xw(run / 'slots_p_dupkey.json', slots_p.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "x",\n "schema"', 1))
    expect_refuse(GP, 'V001PORT', 'T3 slot JSON with a duplicate key', t3(dups, sp, full=False), 'INPUT_JSON')
    expect_refuse(GP, 'V001PORT', 'T3 text of record not the one the sealed prereg was made from (r4 given, its own sha stated)',
                  T3.run(str(slots_p), str(sp), str(R4), None, (), None, None, REAL[R4]), 'SEALED_PREREG_TEXT_CHANGED')
    expect_refuse(GP, 'V001PORT', 'T3 text of record sha stated for another file (r4 sha for the r5 text)',
                  T3.run(str(slots_p), str(sp), str(R5S), None, (), None, None, REAL[R4]), 'TEXT_OF_RECORD_SHA_ARG_MISMATCH')
    p_b6 = xw(run / 'slots_p_build6.json', dict(copy.deepcopy(slots), launch_packet=dict(slots['launch_packet'], build=pin(PKT / 'BUILD_V006.md'))))
    expect_refuse(GP, 'V001PORT', 'T3 launch build not the prereg-named build (slots name BUILD_V006)', t3(p_b6, sp, full=False), 'BUILD_NOT_THE_PREREG_NAMED_BUILD')
    expect_pass(GP, 'V001PORT', 'T4 genuine (record built; nothing written by the tool)', res4)
    t4('T4 E-SEAL1 output with a decimal row-like value', 'E_SEAL1_OUTPUT', tag='V001PORT', gates_only_output=str(body_file(gates_body(statement='GATES: row 03 speed 45.1234 km/s'))))
    s2, p2, sp2, sc2 = variant('p_t4pending', lambda s: s.update(producer_registry={'path': str(REGISTRY), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    t4('T4 any slot-fill refusal produces no record', 'T3:', tag='V001PORT', slots=str(p2), prereg=str(sp2), sealed_compare=str(sc2))
    # integration (2): launcher validate on a plan bound from a test copy of V011 whose outputs lie in this run folder
    tplt = json.loads(TEMPLATE_V011.read_bytes())
    outs = run / 'launch_outputs'
    tplt['launcher_log'] = str(outs / 'LAUNCHER_TEST.log')
    for x in tplt['calls']:
        base = os.path.basename(x['outdir'])
        x['outdir'] = str(outs / base)
        x['receipt'] = str(outs / (base + '.receipt.json'))
        x['monitor_log'] = str(outs / (base + '.monitor.log'))
        x['monitor_argv'] = L.monitor_argv.__wrapped__(tplt, x)
    tplt_p = xw(run / 'TEST_TEMPLATE_V011_OUTPUTS_HERE_C4CHK.json', json.dumps(tplt, indent=1) + '\n')
    plant_p, cmdt_p = run / 'BOUND_PLAN_TEST_TEMPLATE_C4CHK.json', run / 'BOUND_COMMAND_TEST_TEMPLATE_C4CHK.txt'
    B.bind(str(tplt_p), str(DRIVER), dsha, str(frozen), fsha, str(plant_p), str(cmdt_p))
    G.CONFIG = cfg_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_p)
    try:
        ov = 'ok' if L.validate(json.loads(plant_p.read_bytes())) is True else 'not True'
    except BaseException as e:
        ov = '%s: %s' % (type(e).__name__, e)
    check(GP, 'V001PORT', 'integration: real guard v008 + launcher v007 validate() accept a plan with the SEAL_RECORD\'s driver / frozen pins', ov == 'ok', ov)
    rec_o = dict(rec4, driver=pin(R12))
    seal_o = xw(run / 'SEAL_RECORD_OTHER_DRIVER_C4CHK.json', json.dumps(rec_o, indent=1, sort_keys=True) + '\n')
    cfg_o = xw(run / 'ROOT_SEAL_ADMISSION_OTHER_DRIVER_C4CHK.json', dict(cfg, seal=pin(seal_o)))
    G.CONFIG = cfg_o
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_o)
    try:
        L.validate(json.loads(plant_p.read_bytes()))
        o3 = 'accepted'
    except BaseException as e:
        o3 = '%s: %s' % (type(e).__name__, e)
    check(GP, 'V001PORT', 'integration: a SEAL_RECORD naming another driver is refused by launcher v007', 'PLAN_SEALED_DRIVER_MISMATCH' in o3, o3)
    G.CONFIG = run / 'NO_CONFIG_AFTER_TESTS.json'
    os.environ.pop('UNT_ROOT_ADMISSION_SHA256', None)
    open_bytes_end = OPEN_ADD.read_bytes()
    summary = {'harness': 'test_c4chk_v1.py', 'harness_sha256': C.sha(__file__), 'utc': stamp, 'run_dir': str(run),
               'tools_r2': R2_SHAS, 'inputs': {str(p): h for p, h in REAL.items()},
               'open_V005_sha_start': C.sha_bytes(open_bytes_start), 'open_V005_sha_end': C.sha_bytes(open_bytes_end), 'frozen_copy': pin(frozen), 'entries': 'A47-A%d' % NMAX,
               'covered_later': COV, 'impl_new_ids': impl_ids,
               'results': results, 'passed': sum(r['ok'] for r in results), 'total': len(results),
               'by_tag': {t: '%d/%d' % (sum(r['ok'] for r in results if r['tag'] == t), sum(1 for r in results if r['tag'] == t)) for t in sorted({r['tag'] for r in results})}}
    with open(run / 'TEST_RESULTS_C4CHK_V1.json', 'x') as f:
        json.dump(summary, f, indent=1)
    for r in results:
        print('%-12s %-10s %-118s %-5s %s' % (r['group'], r['tag'], r['case'][:118], 'ok' if r['ok'] else 'NOT', '' if r['ok'] else (r['codes'][:4], r['expect'])))
    print('passed', summary['passed'], '/', summary['total'], summary['by_tag'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
