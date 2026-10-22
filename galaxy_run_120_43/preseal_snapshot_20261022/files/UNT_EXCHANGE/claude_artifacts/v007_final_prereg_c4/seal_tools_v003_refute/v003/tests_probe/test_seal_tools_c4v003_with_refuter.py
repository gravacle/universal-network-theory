# Claude4 seal tools v003: tamper tests for the five seal tools. Successor of r2 test_seal_tools_c4v002.py (8c677fdb, 148/148). Every r2 case
# is ported, with its r2 index: tag PORT (the call and expectation are r2's, apart from the v002->v003 renames) or PORT_CHANGED (the call or
# the expectation changed; 'why' gives the reason). v003 implements the full D-05 rule of dispatches 0633 and 0640 (with Claude4's v002-check
# C-01): tool 1 reads the V005 bytes the text of record was written against (the prereg pins them in entries_after_A81.addendum_read; root
# gives the copy), CH = every entry whose section changed between that copy and the frozen copy (plus every table row whose sha is not the
# frozen section), L = later entries with no table row and entries absent from the copy, and root's byte-pinned dispositions file gives each
# entry of L u CH exactly one row with the exact keys of its disposition (no_change for L only; revised with a pinned prereg_revision;
# no_change_after_change for CH only, with a changed_text excerpt present in the new section bytes and absent from the old).
# Tags: NEW (MUST_FAIL cases of v003), NEW_CONTROL (positive controls), REPRO (r2's own tool 1, or the real guard, reproduces a known
# acceptance), REAL_NEW (prereg r5 3245899f with its pinned read copy 70a48f51 and a FROZEN-named copy of the current open V005),
# ENVIRONMENT (the open V005 did not change during the run, so no tool 2 cited-addendum result is an artifact of a concurrent write).
# MUST_FAIL coverage asked for by the task: Codex1's PV-D05-1 fixture (b1b6000f; verbatim and with a read copy built from Codex1's own
# OLD_A90_SECTION 92129acd), C-01 (an edit inside a cited A62 with no row), plain no_change on CH, changed_text present in the old bytes,
# absent from the new bytes, generic, empty why_no_prereg_effect, revised without or with a forged prereg_revision, prereg_revision = the
# prereg itself, read-copy sha mismatch, missing read copy, bare names in tools 1/3/4 (API and CLI), and the W7-S1 B8 cases (a 17-row
# admission config with the superseded writers 9fbdb0ca and 500f8b6a; a config with BUILD_V006's 15 rows). r13 f5adfd11 (A104, the compare
# of record) is a reviewed-compare fixture for tools 2, 3 and 5 (and one full tool 4 build) alongside r12 4bd7b262.
# Fixtures are built under tests/run_<UTC>/; every disposition and revision file there carries SYNTHETIC reasons and is not root's:
#  - the open V005 addendum, read now (fence exception (b)), copied as the FROZEN copy; the stand-in's read copy is that copy minus its
#    newest entry A<NMAX> (the stand-in text was "written" before A<NMAX>); FROZEN-named variants with one section edited (A62, A90);
#  - a SYNTHETIC prereg r5 STAND-IN (from the real r4 text: binding_inputs.case_block, a named BUILD, path_to_be in the run folder,
#    an entries_after_A81 table in the r5 form with section shas and an addendum_read pin read from the read copy, a B2-disclosure
#    requirement); it is not the prereg r5 of record;
#  - a case block built in-process by Claude3's recipe (validate_registry_r12_c3v002.py) from the ten DRY_R5_MS128_V004 dry reports,
#    validated by the reviewed compare's own validate_case_block;
#  - the r5 driver BUILD record printed by tool 5 (builtin_r5_build + CHECK.md), admitted by the compare's activate_driver_build;
#  - a SYNTHETIC BUILD_V007 STAND-IN with the 15 BUILD_V006 sources (verified from bytes) and a test template whose output paths
#    lie in the run folder (no runs_ext path is ever stat'ed); plans bound by the REAL binder (HERE patched to the run folder);
#  - a SYNTHETIC CASCADE_MAP_R5_ADDENDUM stand-in, synthetic B6 bodies in the r12 format and B7 inputs in the v002 schemas.
# Integration: as r2, the built SEAL_RECORD passes the admission-config check and is fed to the REAL guard v008 / launcher v007 (CONFIG and
# REGISTERED patched in-process to synthetic files before any guard call; validate() and admission() only; nothing is started). The real
# guard's admission() also runs on each B8 record (its refusal is TESTED) and on the two W7-S1 configs (its acceptance is TESTED: the B8
# check, not the guard, closes W7-S1).
# Run inside tools/run_fenced_c4st2.py (fence_c4v002). A local audit hook also refuses process creation, network, deletes and any
# write outside the run folder.
# usage: python3 -I -B ../tools/run_fenced_c4st2.py test_seal_tools_c4v003.py
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
import seal_common_c4v003 as C
import check_frozen_addendum_c4v003 as T1
import check_sealed_compare_c4v003 as T2
import check_slot_fill_c4v003 as T3
import build_seal_record_c4v003 as T4
import print_driver_build_record_c4v003 as T5

EX = Path('/Users/bgm/Research/UNT_EXCHANGE'); CA = EX / 'claude_artifacts'
C2 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
R4 = CA / 'v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json'
R5 = CA / 'v007_final_prereg_c4/r5/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'     # prereg r5 as landed (FROM_CLAUDE4/0103), not yet ruled of record
R5_READ = CA / 'v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md'   # the bytes r5's table was read from (its pin)
OPEN_ADD = C2 / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
PKT = CA / 'v007_launch_packet_cx1'
T = CA / 'tail_scheme_impl_c2'
R12 = CA / 'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'
R12_SHA = '4bd7b262caae26f2de146cee803dd689a1f4e565cb67552f04e6d6b97188dd28'
R12_IMPL = CA / 'v007_compare_c2/r12/COMPARE_V007_IMPL_R12.md'
R13 = CA / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'          # A104: the compare of record
R13_SHA = 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
R13_IMPL = CA / 'v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md'
DRIVER = T / 'driver_r5/galaxy_m0_forward_c2v010.py'
CHECK_MD = T / 'driver_r5/check/CHECK.md'
IDENT = T / 'gates_v007/r2/records/R5_V001'
COMPARATOR = T / 'gates_v007/r2/run_identity_compare_c2v007.py'
REGISTRY = CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V008.json'
REGISTRY_V007 = CA / 'producer_registry_c3/out/PRODUCER_REGISTRY_C3V007.json'
B2_REC = CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V003.json'
B2_REC_V002 = CA / 'gate_b2_c3/out/B2_GATE_RECORD_C3V002.json'
BUILD_V007 = PKT / 'BUILD_V007.md'
BUILD_V006 = PKT / 'BUILD_V006.md'
TEMPLATE_V011 = PKT / 'P128/LAUNCH_PLAN_V011_CX3V001.json'
DRAFT_CASE_BLOCK = T / 'driver/out/CASE_BLOCK_V007_DRAFT_C2V001.json'
CERTS = {'EPS': T / 'certificates_v002/gates/EPS_CERT_V006.json', 'LO': T / 'certificates_v004/gates/LO_CERT_V004_MS128.json',
         'GQ': CA / 'producer_registry_c3/out/GQ_CERT_V006.json', 'DOUBLING': CA / 'producer_registry_c3/out/DOUBLING_MERGED_C3V001.json',
         'EPS_NGC': T / 'certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json', 'LO_NGC': T / 'certificates_v002/gates/LO_NGC_CERT_V002.json',
         'I1T_NGC': T / 'certificates_v002/gates/I1T_NGC_T120L_V001.json'}
IDENTITY_FILES = {'Z2': IDENT / 'B1_R5_C2V007.json', 'Z2_OFF_RO1': IDENT / 'B1_OFF_R5_C2V007.json', 'B0prime_RERUN': IDENT / 'B0prime_RERUN_R5_C2V007.json'}
# r2 (the base, for the reproductions and the port map), Codex3's D-05 fixtures (pinned by its RESULTS_CX3V001.json 086bc3d3) and
# Codex1's PV-D05-1 fixture (PROVISIONAL_REVIEW_CX1V002 c483cc99) with Codex1's own old A90 section (rule0640 controls)
R2 = CA / 'v007_final_prereg_c4/seal_tools_v002/r2'
R2_RESULTS = R2 / 'tests/run_20261018T212903Z/TEST_RESULTS_C4V002.json'
CX3 = CA / 'review_prereg_r5_seal_tools_cx3/entry_driver_review/fixtures'
CX3_LATER = (CX3 / 'later_bare_note/SYNTH_PREREG.json', CX3 / 'later_bare_note/SYNTH_V005_ADDENDUM_FROZEN.md')
CX3_CHANGED = (CX3 / 'changed_row_bare_note/SYNTH_PREREG.json', CX3 / 'changed_row_bare_note/SYNTH_V005_ADDENDUM_FROZEN.md')
CX1 = CA / 'review_seal_tools_v003_cx1/provisional_controls_v002/D05/changed_nominal_reason_nominal_change'
CX1_PV = (CX1 / 'SYNTH_PREREG.json', CX1 / 'SYNTH_V005_ADDENDUM_FROZEN.md', CX1 / 'SYNTH_DISPOSITIONS.json')
CX1_OLD_A90 = CA / 'review_seal_tools_v003_cx1/rule0640_controls_v001/OLD_A90_SECTION.txt'
REAL_SHAS = {CERTS['DOUBLING']: 'ea48ac2bc429a1b6f7ae9b2cf96964a42bbedfd64afab21f724259114d8b0f7b',
             CHECK_MD: '89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632',
             IDENTITY_FILES['Z2']: '83e7b0673159156832995a1d7caae401a430918cbd110975bac8e18335aedc72',
             IDENTITY_FILES['Z2_OFF_RO1']: '3b9ad4029a8673eabfa87b2fe77ea66241589412291c44af5d0b220a6fad3df2',
             IDENTITY_FILES['B0prime_RERUN']: 'e33af53d1df36d858ed887bc4ed24fae77fe606d88ab26e2a77d9e5481d09258',
             R12: R12_SHA, R13: R13_SHA, DRAFT_CASE_BLOCK: '6bf4ce5a4219d281fa480d4249e818e8d9fc39779b3ad605e1a069f42e0da4c1',
             R13_IMPL: '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3',
             B2_REC: '915fbcda4f4a2cb5f61b257ff83494738144e177401c11c94e254c322df2411c',
             BUILD_V007: '94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de',
             BUILD_V006: 'fb9e6a4a19395f35b9929fb163df6305c1b472f504266e2b4b98453f5bbb004f',
             TEMPLATE_V011: '1b406591784ab4647e4aaf2686d9b3d18a259fadb435391439d2ff75df22ad3c',
             REGISTRY: 'f189cd3fcd45426c23ba8600104a0a2ebf8ca7bcb453327aae19e6ebc1ee1120',
             R5: '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393',
             R5_READ: '70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e',
             R2 / 'seal_common_c4v002.py': 'f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10',
             R2 / 'check_frozen_addendum_c4v002.py': '06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891',
             R2_RESULTS: '6de5ab43119b2371e6941ba3ab56ae7ea70f8cdd57a2c59e1678be2948e6b639',
             CX3_LATER[0]: '8f3c5b703e290cb299bb093689777df792897421000fc8efc8193be59c688def',
             CX3_LATER[1]: 'd4a4af0583dee302ed6f5db742b49fa9c00d87dadea9e54c292d9a05711269c0',
             CX3_CHANGED[0]: '7ff80919250bee2472a5cda22bd73724de6ef33a038962c12c15082c7269a261',
             CX3_CHANGED[1]: '1cbad5e1841205f47356f4789eeb4059dd9d8f97ca16a5d8987e037e0f9ab0b2',
             CX1_PV[0]: '0daa5e813df0c673074020b55a35823ab49716b9b585e98021b186345ce60399',
             CX1_PV[1]: '1cbad5e1841205f47356f4789eeb4059dd9d8f97ca16a5d8987e037e0f9ab0b2',
             CX1_PV[2]: 'b1b6000f6e886d130396777c483eca583e182e6b1b84304c6f47cdf5499004ba',
             CX1_OLD_A90: '92129acd1ad111dfc395eb495a57c2568a87610e4656f473feeb2a77f4b74180'}
OLD_WRITER_PREFIXES = ('9fbdb0ca', '500f8b6a')          # W7-S1: the superseded writers BUILD_V007 cites outside its allowlist section
GATES_SCHEMA = 'UNT_KMAX_TAIL_COMPARISON_C2V007_R11'
B2_TEXT = ('The seal record repeats the B2 disclosure block of the B2 record of record (A100) and A101\'s erratum. SYNTHETIC test text in the '
           'r5 stand-in; the requirement of record is prereg r5\'s.')
WHY_DISP = 'D-05: the bare covered-later list is removed; the same coverage is now a byte-pinned dispositions fixture (dispositions=D0)'
WHY_RC = ('0640: tool 1 also takes the V005 bytes the text of record was written against (text_of_record_addendum; the prereg pins them in '
          'entries_after_A81.addendum_read)')
WHY_DISP_RC = WHY_DISP + '; ' + WHY_RC
WHY_BASE = 'D-05: the builder\'s base arguments carry the dispositions fixture D0 and the read copy RC0 instead of covered_later'
WHY_BARE = 'D-05: the bare list form is removed; any non-empty covered_later refuses COVERED_LATER_BARE_NAMES_REFUSED (r2: %s)'
SYN_REASON = 'SYNTHETIC TEST ROW (Claude4 seal tools v003 tests): not root\'s disposition of %s'
SYN_WHY = 'SYNTHETIC TEST ROW (Claude4 seal tools v003 tests): the edit has no prereg effect only in this fixture; not root\'s reading of %s'
EDIT62 = 'SYNTHETIC EDIT INSIDE A62 (Claude4 seal tools v003 tests, C-01): not root text.\n'
EDIT62U = 'SYNTHETIC café EDIT INSIDE A62 (Claude4 seal tools v003 tests, NFC): not root text.\n'
EDIT90 = 'SYNTHETIC EDIT INSIDE A90 (Claude4 seal tools v003 tests): not root text.\n'


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


def xwb(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'xb') as f:
        f.write(data)
    return p


def cli(main_fn, argv):
    """run a tool's main() with captured stdout and stderr: (rc, stdout, stderr)"""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            rc = main_fn(argv)
        except SystemExit as e:
            rc = e.code
    return rc, out.getvalue(), err.getvalue()


def jcodes(s):
    try:
        return [f['code'] for f in json.loads(s).get('failures', [])]
    except (ValueError, AttributeError):
        return ['<not a JSON verdict>']


def jget(s, key):
    """key of a JSON verdict printed by a tool, or None when the text is not a JSON object (the harness never raises on a bad verdict)"""
    try:
        return json.loads(s).get(key)
    except (ValueError, AttributeError):
        return None


def without_section(raw, n):
    """the bytes with entry n's whole section removed (every other section keeps its bytes under the r5 section_rule)"""
    sec = T1.sections(raw)[n][0][1]
    i = raw.index(sec)
    return raw[:i] + raw[i + len(sec):]


def with_section(raw, n, new_sec):
    """the bytes with entry n's section replaced by new_sec"""
    sec = T1.sections(raw)[n][0][1]
    i = raw.index(sec)
    return raw[:i] + new_sec + raw[i + len(sec):]


def edited(raw, n, insert):
    """the bytes with `insert` placed right after entry n's heading line: only entry n's section changes"""
    sec = T1.sections(raw)[n][0][1]
    le = sec.index(b'\n') + 1
    return with_section(raw, n, sec[:le] + insert.encode('utf-8') + sec[le:])


def changed_entries(a, b):
    sa, sb = T1.sections(a), T1.sections(b)
    return sorted(n for n in set(sa) | set(sb) if sa.get(n) != sb.get(n))


def main():
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    run = Path(RUNROOT) / ('run_' + stamp)
    run.mkdir()
    ROOT_HOLDER[0] = os.path.realpath(str(run))
    run = Path(ROOT_HOLDER[0])
    results = []

    def record(tool, name, res, expect_pass, code=None, absent=None, tag='NEW', note=None, r2=None, why=None, exact=None):
        codes = [f['code'] for f in res.get('failures', [])]
        notes = [n['code'] for n in res.get('notes', [])]
        ok = (res['verdict'] == 'PASS') if expect_pass else (res['verdict'] == 'REFUSE' and (code is None or any(code in c for c in codes)))
        if absent:
            ok = ok and not any(absent in c for c in codes)
        if note:
            ok = ok and note in notes
        if exact is not None:
            ok = ok and sorted(set(codes)) == sorted(exact)
        results.append({'tool': tool, 'tag': tag, 'r2': r2, 'why': why, 'case': name, 'expect': 'PASS' if expect_pass else 'REFUSE ' + (code or ''),
                        'verdict': res['verdict'], 'codes': codes, 'notes': sorted(set(notes)), 'ok': ok})
        return res

    def check(tool, name, ok, detail, tag='NEW', r2=None, why=None):
        results.append({'tool': tool, 'tag': tag, 'r2': r2, 'why': why, 'case': name, 'expect': 'TRUE', 'verdict': 'PASS' if ok else 'FAIL',
                        'codes': [] if ok else [detail], 'notes': [], 'ok': bool(ok)})
    # ---------------- real inputs, from bytes
    for p, h in REAL_SHAS.items():
        assert C.sha(p) == h, p
    M = C.load_reviewed_compare(str(R12), R12_SHA)
    # ---------------- fixtures: frozen copy (fence exception (b): the open V005 addendum is read here), read copies, reviewed source copies
    frozen = xw(run / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', OPEN_ADD.read_bytes().decode('utf-8'))
    ftext = frozen.read_bytes().decode('utf-8')
    FB = frozen.read_bytes()
    heads = sorted({int(n) for n in re.findall(r'^## A(\d{1,3}):', ftext, re.M)})
    NMAX = max(heads)
    assert all(n in heads for n in range(47, NMAX + 1)), 'the frozen copy has a gap in A47..A%d' % NMAX
    COV = ['A%d' % NMAX]
    SECS = T1.sections(FB)
    # the stand-in's read copy: the frozen bytes without the newest entry (the stand-in cites A47..A<NMAX-1>, tables A82..A<NMAX-1>)
    RC0 = xwb(run / ('read_copies/V005_READ_COPY_STANDIN_WITHOUT_A%d_C4V003.md' % NMAX), without_section(FB, NMAX))
    assert changed_entries(FB, RC0.read_bytes()) == [NMAX]
    RC0s = str(RC0)
    # a read copy with every entry (for the stand-in variants whose table also has A<NMAX>)
    RCF = xwb(run / 'read_copies/V005_READ_COPY_STANDIN_FULL_C4V003.md', FB)
    RCFs = str(RCF)

    def ar_pin(rc):
        return {'open_path': str(OPEN_ADD), 'sha256_at_generation': C.sha(rc), 'bytes': len(Path(rc).read_bytes()),
                'byte_copy': 'SYNTHETIC read-copy fixture in the test run folder (Claude4 seal tools v003 tests): %s' % Path(rc).name}
    reviewed = xw(run / 'reviewed_compare_r12_copy.py', R12.read_bytes().decode('utf-8'))
    assert C.sha(reviewed) == R12_SHA
    reviewed13 = xw(run / 'reviewed_compare_r13_copy.py', R13.read_bytes().decode('utf-8'))
    assert C.sha(reviewed13) == R13_SHA
    # FROZEN-named variants whose single changed section is the CH entry under test (the stand-in "was written" before the edit)
    f_62 = xwb(run / 'variant_A62_edited/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', edited(FB, 62, EDIT62))
    f_62u = xwb(run / 'variant_A62_edited_utf8/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', edited(FB, 62, EDIT62U))
    f_90 = xwb(run / 'variant_A90_edited/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', edited(FB, 90, EDIT90))
    assert changed_entries(FB, f_62.read_bytes()) == [62] and changed_entries(FB, f_62u.read_bytes()) == [62] and changed_entries(FB, f_90.read_bytes()) == [90]
    rev_file = xw(run / 'PREREG_REVISION_SYNTH_C4V003.json', {'schema': 'SYNTHETIC_PREREG_REVISION_FIXTURE', 'note': 'SYNTHETIC test fixture standing for a '
                  'prereg revision (Claude4 seal tools v003 tests); not a revision of record'})
    REV = pin(rev_file)
    # ---------------- v003: dispositions fixtures (root's form; SYNTHETIC reasons)
    nd = [0]

    def disp_row(secs, e, disposition='no_change', ct=None, rev=None):
        s = C.sha_bytes(secs[int(e[1:])][0][1])
        if disposition == 'no_change':
            return {'entry': e, 'disposition': 'no_change', 'reason': SYN_REASON % e, 'section_sha256': s}
        if disposition == 'revised':
            return {'entry': e, 'disposition': 'revised', 'prereg_revision': dict(rev or REV), 'reason': SYN_REASON % e, 'section_sha256': s}
        return {'entry': e, 'disposition': 'no_change_after_change', 'changed_text': ct, 'why_no_prereg_effect': SYN_WHY % e, 'section_sha256': s}

    def disp(fz, later=(), nca=None, revised=(), rows=None, mutate=None, raw=None, name='LATER_ENTRY_DISPOSITIONS_SYNTH_C4V003.json'):
        """a dispositions file in the run folder; returns root's pin (path, sha256). later: L entries (no_change rows); nca: {entry:
        changed_text} (no_change_after_change rows); revised: entries with revised rows (pinned REV); rows: explicit rows; mutate(obj);
        raw: the exact text or bytes."""
        nd[0] += 1
        if raw is None:
            fb = Path(fz).read_bytes()
            secs = T1.sections(fb)
            if rows is None:
                rows = ([disp_row(secs, e) for e in later] + [disp_row(secs, e, 'no_change_after_change', ct) for e, ct in (nca or {}).items()]
                        + [disp_row(secs, e, 'revised') for e in revised])
            obj = {'schema': C.DISPOSITIONS_SCHEMA, 'frozen_addendum_sha256': C.sha_bytes(fb), 'entries': rows}
            if mutate:
                mutate(obj)
            raw = json.dumps(obj, indent=1, ensure_ascii=False) + '\n'
            try:
                raw.encode('utf-8')
            except UnicodeEncodeError:                  # a lone surrogate under test: written as a JSON escape, so the file stays UTF-8 text
                raw = json.dumps(obj, indent=1, ensure_ascii=True) + '\n'
        p = xwb(run / ('dispositions_%03d' % nd[0]) / name, raw if isinstance(raw, bytes) else raw.encode('utf-8'))
        return (str(p), C.sha(p))
    D0 = disp(frozen, later=COV)                       # the stand-in's L = {A<NMAX>}: it cites A47-A<NMAX-1> and tables A82-A<NMAX-1>
    D0_TEXT = Path(D0[0]).read_bytes().decode('utf-8')
    # ---------------- the case block (Claude3 recipe), validated by r12's own validate_case_block
    dry = json.loads((PKT / 'DRY_R5_MS128_V004.json').read_bytes())
    nums = {}
    for c in dry['checks']:
        b = Path(c['report']['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == c['report']['sha256'] and c['passed'] and c['executed_stages'] == 0
        nums[c['case']] = json.loads(b)['normalized_spec']['numerics']
    # ---------------- tool 5: the driver BUILD record (builtin_r5_build + CHECK.md), printed bytes
    r5res, r5text = T5.record_bytes(str(R12), R12_SHA, str(CHECK_MD))
    record('T5', 'tool 5 prints an admissible r5 driver BUILD record with the real CHECK.md 89a6de88 (D-06)', r5res, True, tag='PORT', r2=0)
    dbr = xw(run / 'DRIVER_BUILD_R5_TEST_FIXTURE_C4ST2.json', r5text)
    LIB = M.load_uvt_lib()
    M.activate_driver_build(json.loads(r5text))
    KEYMAP = [{'pointer': '/numerics/route_a/seed_source_rtol_factor', 'absent_equivalent_value': 1.0,
               'b0_identity_evidence': 'SYNTHETIC test row: absent means 1.0 (A48 AMB-14); not the key map of record'}]

    def case_block(mutate=None, keymap=KEYMAP):
        cb = {'schema': M.CASE_BLOCK_SCHEMA, 'route_a_mode': 'parallel8', 'cases': {}, 'note': 'SYNTHETIC TEST FIXTURE (Claude4 seal tools v003); not the V007 case block of record'}
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
    v6 = BUILD_V006.read_bytes().decode('utf-8')
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
    tpl['label'] = 'SYNTHETIC TEST TEMPLATE (Claude4 seal tools v003): the r5 template with every output path moved into the test run folder'
    template = xw(run / 'LAUNCH_PLAN_V010_TEST_TEMPLATE_C4ST2.json', json.dumps(tpl, indent=1) + '\n')

    def build_v007(name='BUILD_V007.md', sub='build_v007_standin', entries=None):
        ents = allow6 if entries is None else entries
        body = ('# BUILD_V007 -- SYNTHETIC STAND-IN (Claude4 seal tools v003 tests; NOT the BUILD_V007 of record)\n\n'
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
    plan_90p, cmd_90p = run / 'BOUND_PLAN_A90_EDITED_SYNTH.json', run / 'BOUND_COMMAND_A90_EDITED_SYNTH.txt'
    B.bind(str(template), str(DRIVER), dsha, str(f_90), C.sha(f_90), str(plan_90p), str(cmd_90p))
    plan90 = json.loads(plan_90p.read_bytes())
    cma = xw(run / 'CASCADE_MAP_R5_ADDENDUM_TEST_STANDIN_C4ST2.json',
             {'schema': 'SYNTHETIC_CASCADE_MAP_R5_ADDENDUM_STANDIN', 'amends': {'path': M.PIN_R5_CASCADE_MAP[0], 'sha256': M.PIN_R5_CASCADE_MAP[1]},
              'note': 'SYNTHETIC test stand-in; the immutable inventory addendum of record is root\'s (A69)'})
    # ---------------- the prereg r5 STAND-IN (text of record for the tests)
    r4 = json.loads(R4.read_bytes())

    def table(entries, revised=('A82',), bad_sha=(), mutate_row=None, rc=None, ar='pin'):
        rcp = RC0 if rc is None else rc
        rsecs = T1.sections(Path(rcp).read_bytes())
        rows = []
        for e in entries:
            heading, sec = rsecs[int(e[1:])][0]
            r = {'entry': e, 'heading': heading, 'section_sha256': ('9' * 64 if e in bad_sha else C.sha_bytes(sec)), 'section_bytes': len(sec)}
            if e in revised:
                r.update(decision='REVISED_HERE', revised_clauses=['seal_slots.compare'], scope='SYNTHETIC test row')
            else:
                r.update(decision='NO_CHANGE', revised_clauses=[], reason='no change, because SYNTHETIC test row (not the r5 table of record)')
            if mutate_row:
                mutate_row(r)
            rows.append(r)
        t = {'rule': 'SYNTHETIC stand-in of the A99.3 table', 'section_rule': 'as prereg r5', 'rows': rows, 'sources': ['A81 RI-26', 'A99.3']}
        if ar == 'pin':
            t['addendum_read'] = ar_pin(rcp)
        elif ar is not None:
            t['addendum_read'] = ar
        return t

    def text_of_record(name, build_sha='file', case_blk='fixture', ptb=None, tab=None, cites=NMAX - 1, mutate=None, build_path=None, b2=True):
        d = copy.deepcopy(r4)
        d['revision'] = 'r5-SYNTHETIC-STAND-IN'
        d['status'] = 'SYNTHETIC prereg r5 STAND-IN for the Claude4 seal tools v003 tests; not the prereg r5 of record'
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
    record('T1', 'genuine (the later entry has a row in root\'s dispositions file; r5-form entry table re-hashed from the frozen bytes; read copy verified)',
           T1.run(sp, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), True, tag='PORT_CHANGED', r2=1, why=WHY_DISP_RC)
    f_a = xw(run / 'variant_a/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext.replace('## A60:', '## A60 (removed heading):'))
    record('T1', 'cited entry A60 absent', T1.run(sp, f_a, None, dispositions=disp(f_a, later=COV), text_of_record_addendum=RC0s), False,
           'CITED_ENTRY_ABSENT_FROM_FROZEN', tag='PORT_CHANGED', r2=2, why=WHY_DISP_RC + ', written for this frozen variant')
    f_b = xw(run / 'variant_b/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext + '\n## A70: duplicate entry\n')
    record('T1', 'duplicate heading', T1.run(sp, f_b, None, dispositions=disp(f_b, later=COV), text_of_record_addendum=RC0s), False, 'DUPLICATE_ENTRY_HEADING',
           tag='PORT_CHANGED', r2=3, why=WHY_DISP_RC + ', written for this frozen variant')
    f_c = xw(run / 'variant_c/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext + '\nsealed prereg %s\n' % C.sha(sp))
    record('T1', 'frozen cites the sealed prereg sha', T1.run(sp, f_c, None, dispositions=disp(f_c, later=COV), text_of_record_addendum=RC0s), False,
           'FROZEN_CITES_SEALED_PREREG_SHA', tag='PORT_CHANGED', r2=4, why=WHY_DISP_RC + ', written for this frozen variant')
    record('T1', 'later entry uncovered', T1.run(sp, frozen, None, [], text_of_record_addendum=RC0s), False, 'UNCOVERED_LATER_ENTRY', tag='PORT_CHANGED', r2=5,
           why=WHY_RC)
    f_e = xw(run / 'variant_e/V005_ADDENDUM_COPY.md', ftext)
    record('T1', 'not the _FROZEN copy', T1.run(sp, f_e, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'NOT_THE_FROZEN_COPY', tag='PORT_CHANGED', r2=6,
           why=WHY_DISP_RC + ' (the copy has the frozen bytes)')
    record('T1', 'expected sha differs', T1.run(sp, frozen, '0' * 64, dispositions=D0, text_of_record_addendum=RC0s), False, 'FROZEN_SHA_MISMATCH', tag='PORT_CHANGED',
           r2=7, why=WHY_DISP_RC)
    D_absent = disp(frozen, later=COV, mutate=lambda o: o['entries'].append(dict(o['entries'][0], entry='A%d' % (NMAX + 5))))
    record('T1', 'a dispositions row names an entry absent from the frozen bytes (r2: covered-later names an absent entry)',
           T1.run(sp, frozen, None, dispositions=D_absent, text_of_record_addendum=RC0s), False, 'DISPOSITION_ENTRY_NOT_IN_FROZEN', tag='PORT_CHANGED', r2=8,
           why='D-05: the bare list is removed; the same defect is a dispositions row for A%d (r2: COVERED_LATER_NOT_IN_FROZEN); %s' % (NMAX + 5, WHY_RC))
    dup_json = xw(run / 'variant_h_prereg.json', sp.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "dup",\n "schema"', 1))
    record('T1', 'prereg JSON with a duplicate key', T1.run(dup_json, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'PREREG_JSON',
           tag='PORT_CHANGED', r2=9, why=WHY_DISP_RC)
    # D-10
    f_d = xw(run / 'variant_d10/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ftext)
    record('T1', 'D-10: a FROZEN-named copy at a path other than path_to_be', T1.run(sp, f_d, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'FROZEN_PATH_NOT_PATH_TO_BE', tag='PORT_CHANGED', r2=10, why=WHY_DISP_RC)
    sp_noptb = sealed_prereg_for(slots, TOR, 'variant_noptb_prereg.json', mutate=lambda d: d['seal_slots']['frozen_addendum'].pop('path_to_be'))
    record('T1', 'D-10: a prereg without path_to_be', T1.run(sp_noptb, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'FROZEN_PATH_TO_BE_ABSENT',
           tag='PORT_CHANGED', r2=11, why=WHY_DISP_RC)
    record('T1', 'D-10: the dry-run flag records the path deviation as a note and never fails it', T1.run(TOR, f_d, None, (), True, D0, RC0s), True,
           note='DRY_RUN_FROZEN_PATH_NOT_PATH_TO_BE', tag='PORT_CHANGED', r2=12, why=WHY_DISP_RC)
    # D-05 (r2 cases: the bare list in each r2 form now refuses as a whole)
    record('T1', 'D-05: covered-later as a range', T1.run(sp, frozen, None, ['A82-A%d' % NMAX], dispositions=D0, text_of_record_addendum=RC0s), False,
           'COVERED_LATER_BARE_NAMES_REFUSED', tag='PORT_CHANGED', r2=13, why=WHY_BARE % 'COVERED_LATER_FORMAT')
    record('T1', 'D-05: the stale README form covered-later A82', T1.run(sp, frozen, None, ['A82'], dispositions=D0, text_of_record_addendum=RC0s), False,
           'COVERED_LATER_BARE_NAMES_REFUSED', tag='PORT_CHANGED', r2=14, why=WHY_BARE % 'COVERED_LATER_IS_CITED')
    record('T1', 'D-05: an entry listed twice', T1.run(sp, frozen, None, COV + COV, dispositions=D0, text_of_record_addendum=RC0s), False,
           'COVERED_LATER_BARE_NAMES_REFUSED', tag='PORT_CHANGED', r2=15, why=WHY_BARE % 'COVERED_LATER_DUPLICATE')
    # A99.3 entry table (r5 form)
    ents = lambda hi, skip=(): ['A%d' % n for n in range(82, hi + 1) if n not in skip]

    def t1_variant(name, **kw):
        tor = text_of_record('variant_%s.json' % name, **kw)
        return tor, sealed_prereg_for(slots, tor, 'variant_%s_sealed.json' % name)
    _, sp_t = t1_variant('table_missing_A90', tab=table(ents(NMAX - 1, (90,))))
    record('T1', 'A99.3: the entry table lacks A90', T1.run(sp_t, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'ENTRY_TABLE_MISSING_ENTRY',
           tag='PORT_CHANGED', r2=16, why=WHY_DISP_RC)
    _, sp_t = t1_variant('table_absent', tab='absent')
    record('T1', 'A99.3: no entry table', T1.run(sp_t, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'ENTRY_TABLE_ABSENT', tag='PORT_CHANGED',
           r2=17, why=WHY_DISP_RC)
    tor_thl, sp_thl = t1_variant('table_has_later', tab=table(ents(NMAX), rc=RCF))
    record('T1', 'A99.3: a later entry with a table row and a dispositions row', T1.run(sp_thl, frozen, None, dispositions=D0, text_of_record_addendum=RCFs), False,
           'DISPOSITION_FOR_TABLED_ENTRY', absent='DISPOSITION_FOR_CITED_ENTRY', tag='PORT_CHANGED', r2=18,
           why='D-05: the no-change note is now a dispositions row; a row for an entry with an unchanged table row refuses DISPOSITION_FOR_TABLED_ENTRY '
               '(r2: COVERED_LATER_IN_ENTRY_TABLE); %s (this table also rows A%d, so its read copy holds A%d)' % (WHY_RC, NMAX, NMAX))
    record('T1', 'A99.3: a later entry covered by its table row alone', T1.run(sp_thl, frozen, None, [], text_of_record_addendum=RCFs), True, tag='PORT_CHANGED', r2=19,
           why=WHY_RC + ' (the read copy holds A%d)' % NMAX)
    _, sp_t = t1_variant('table_dup', tab=table(ents(NMAX - 1) + ['A85']))
    record('T1', 'A99.3: a table row repeated', T1.run(sp_t, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'ENTRY_TABLE_DUPLICATE_ENTRY',
           tag='PORT_CHANGED', r2=20, why=WHY_DISP_RC)
    tor_90 = text_of_record('variant_tor_A90_edited.json', ptb=str(f_90))
    record('T1', 'A99.3: a row whose section no longer re-hashes from the frozen bytes (A90 edited after the text was written; no row for it)',
           T1.run(tor_90, f_90, None, dispositions=disp(f_90, later=COV), text_of_record_addendum=RC0s), False, 'ENTRY_TABLE_SECTION_CHANGED', tag='PORT_CHANGED',
           r2=21, why='0640: the change is now made in the frozen bytes (A90 edited after the read copy); a row sha that differs from the read copy '
                      'is ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD instead; ' + WHY_DISP_RC)
    D_90 = disp(f_90, later=COV, nca={'A90': EDIT90[:40]})
    record('T1', 'A99.3: the changed row with root\'s no_change_after_change row naming the change (r2: --covered-later A90)',
           T1.run(tor_90, f_90, None, dispositions=D_90, text_of_record_addendum=RC0s), True, note='ENTRY_TABLE_SECTION_CHANGED_NOTED', tag='PORT_CHANGED', r2=22,
           why='D-05 (0640): root\'s explicit note is now a no_change_after_change row for A90 whose changed_text occurs in the new section and not the '
               'old; the change is made in the frozen bytes; ' + WHY_RC)
    _, sp_t = t1_variant('table_bad_decision', tab=table(ents(NMAX - 1), mutate_row=lambda r: r.update(decision='MAYBE') if r['entry'] == 'A84' else None))
    record('T1', 'A99.3: a row whose decision is neither REVISED_HERE nor NO_CHANGE', T1.run(sp_t, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'ENTRY_TABLE_MALFORMED', tag='PORT_CHANGED', r2=23, why=WHY_DISP_RC)
    _, sp_t = t1_variant('table_revised_no_clauses', tab=table(ents(NMAX - 1), mutate_row=lambda r: r.update(revised_clauses=[]) if r['entry'] == 'A82' else None))
    record('T1', 'A99.3: a REVISED_HERE row naming no revised clause', T1.run(sp_t, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'ENTRY_TABLE_MALFORMED', tag='PORT_CHANGED', r2=24, why=WHY_DISP_RC)
    rows5 = json.loads(R5.read_bytes())['entries_after_A81']['rows']
    mism = [r['entry'] for r in rows5 if C.sha_bytes(SECS[int(r['entry'][1:])][0][1]) != r['section_sha256'] or len(SECS[int(r['entry'][1:])][0][1]) != r['section_bytes']]
    check('T1', 'REAL cross-check: tool 1\'s section rule reproduces every section_sha256 of prereg r5 3245899f (%d rows; an independent implementation)' % len(rows5),
          not mism, 'mismatched rows %r' % mism, tag='PORT', r2=25)
    # ================= tool 1, v003 D-05 (NEW): the bare list, the pin, the strict parse, the schema and the rows
    record('T1', 'D-05: a bare name via the API refuses, even beside a valid dispositions file', T1.run(sp, frozen, None, COV, dispositions=D0,
           text_of_record_addendum=RC0s), False, 'COVERED_LATER_BARE_NAMES_REFUSED')
    record('T1', 'D-05: a bare name via the API with no dispositions file: refused, and it covers nothing', T1.run(sp, frozen, None, COV, text_of_record_addendum=RC0s),
           False, 'COVERED_LATER_BARE_NAMES_REFUSED')
    rc, so, se = cli(T1.main, ['--prereg', str(sp), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s, '--covered-later', COV[0]])
    check('T1', 'D-05: a bare name via the CLI (--covered-later A<n>) exits 2 with COVERED_LATER_BARE_NAMES_REFUSED', rc == 2 and
          jcodes(so) == ['COVERED_LATER_BARE_NAMES_REFUSED'], 'rc %r codes %r' % (rc, jcodes(so)))
    rc, so, se = cli(T1.main, ['--prereg', str(sp), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s, '--dispositions', D0[0], '--dispositions-sha', D0[1],
                               '--covered-later=%s' % COV[0]])
    check('T1', 'D-05: the CLI --covered-later=A<n> form beside valid dispositions flags is refused too', rc == 2 and
          jcodes(so) == ['COVERED_LATER_BARE_NAMES_REFUSED'], 'rc %r codes %r' % (rc, jcodes(so)))
    rc, so, se = cli(T1.main, ['--prereg', str(sp), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s, '--dispositions', D0[0], '--dispositions-sha', D0[1]])
    check('T1', 'D-05 control: the CLI with --addendum-at-text-of-record, --dispositions and --dispositions-sha passes (exit 0)', rc == 0
          and jget(so, 'verdict') == 'PASS', 'rc %r codes %r' % (rc, jcodes(so)), tag='NEW_CONTROL')
    rc, so, se = cli(T1.main, ['--prereg', str(sp), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s, '--dispositions', D0[0]])
    check('T1', 'D-05: --dispositions without --dispositions-sha refuses DISPOSITIONS_PIN_MISMATCH (exit 2)', rc == 2 and 'DISPOSITIONS_PIN_MISMATCH' in jcodes(so),
          'rc %r codes %r' % (rc, jcodes(so)))
    record('T1', 'D-05: the dispositions bytes do not hash to root\'s pin', T1.run(sp, frozen, None, dispositions=(D0[0], '0' * 64), text_of_record_addendum=RC0s),
           False, 'DISPOSITIONS_PIN_MISMATCH')
    record('T1', 'D-05: the pin\'s sha in capitals (not the hexdigest of the bytes)', T1.run(sp, frozen, None, dispositions=(D0[0], D0[1].upper()),
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_PIN_MISMATCH')
    record('T1', 'D-05: a relative dispositions path', T1.run(sp, frozen, None, dispositions=(os.path.relpath(D0[0]), D0[1]), text_of_record_addendum=RC0s), False,
           'DISPOSITIONS_PIN_MISMATCH')
    record('T1', 'D-05: the dispositions path is a directory', T1.run(sp, frozen, None, dispositions=(str(Path(D0[0]).parent), D0[1]), text_of_record_addendum=RC0s),
           False, 'DISPOSITIONS_PIN_MISMATCH')
    record('T1', 'D-05: the dispositions path does not exist', T1.run(sp, frozen, None, dispositions=(D0[0] + '.missing', D0[1]), text_of_record_addendum=RC0s), False,
           'DISPOSITIONS_PIN_MISMATCH')
    record('T1', 'D-05: the API pin is a bare path, not (path, sha256)', T1.run(sp, frozen, None, dispositions=D0[0], text_of_record_addendum=RC0s), False,
           'DISPOSITIONS_PIN_MISMATCH')
    record('T1', 'D-05: the API pin is a {path, sha256} dict, not (path, sha256)', T1.run(sp, frozen, None, dispositions={'path': D0[0], 'sha256': D0[1]},
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_PIN_MISMATCH')
    D_dupkey = disp(None, raw=D0_TEXT.replace('"disposition": "no_change"', '"disposition": "no_change",\n   "disposition": "revised"', 1))
    record('T1', 'D-05: a duplicate key in a row (strict JSON, A71)', T1.run(sp, frozen, None, dispositions=D_dupkey, text_of_record_addendum=RC0s), False,
           'DISPOSITIONS_JSON_DUPLICATE_KEY')
    D_dupkey2 = disp(None, raw=D0_TEXT.replace('{\n "schema"', '{\n "schema": "x",\n "schema"', 1))
    record('T1', 'D-05: a duplicate top-level key', T1.run(sp, frozen, None, dispositions=D_dupkey2, text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_DUPLICATE_KEY')
    sec0 = json.loads(D0_TEXT)['entries'][0]['section_sha256']
    D_nan = disp(None, raw=D0_TEXT.replace('"%s"' % sec0, 'NaN', 1))
    record('T1', 'D-05: a NaN constant', T1.run(sp, frozen, None, dispositions=D_nan, text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_NON_FINITE_CONSTANT')
    D_inf = disp(None, raw=D0_TEXT.replace('"%s"' % sec0, '-Infinity', 1))
    record('T1', 'D-05: a -Infinity constant', T1.run(sp, frozen, None, dispositions=D_inf, text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_NON_FINITE_CONSTANT')
    big = '9' * 5000
    reason0 = json.dumps(json.loads(D0_TEXT)['entries'][0]['reason'], ensure_ascii=False)
    D_big = disp(None, raw=D0_TEXT.replace(reason0, big, 1))
    record('T1', 'D-05: a 5,000-digit integer (Python\'s 4,300-digit limit)', T1.run(sp, frozen, None, dispositions=D_big, text_of_record_addendum=RC0s), False,
           'DISPOSITIONS_JSON_INTEGER_TOO_LONG')
    D_bigdup = disp(None, raw='{"n": %s, "schema": "%s", "schema": "x", "frozen_addendum_sha256": "%s", "entries": []}\n' % (big, C.DISPOSITIONS_SCHEMA, C.sha(frozen)))
    record('T1', 'D-05 (A-B1 class): a duplicate key behind a 5,000-digit integer refuses (no text fallback)', T1.run(sp, frozen, None, dispositions=D_bigdup,
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_')
    D_syntax = disp(None, raw=D0_TEXT[:-3])
    record('T1', 'D-05: a JSON syntax error (no text fallback)', T1.run(sp, frozen, None, dispositions=D_syntax, text_of_record_addendum=RC0s), False,
           'DISPOSITIONS_JSON_SYNTAX')
    D_utf16 = disp(None, raw=D0_TEXT.encode('utf-16'))
    record('T1', 'D-05: UTF-16 bytes (json.loads would decode them; the file must be UTF-8 text)', T1.run(sp, frozen, None, dispositions=D_utf16,
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_ENCODING')
    D_bom = disp(None, raw=b'\xef\xbb\xbf' + D0_TEXT.encode('utf-8'))
    record('T1', 'D-05: a UTF-8 byte-order mark', T1.run(sp, frozen, None, dispositions=D_bom, text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_SYNTAX')
    D_deep = disp(None, raw='[' * 100000)
    record('T1', 'D-05: nesting deep enough to exhaust the parser (a typed code, not a traceback)', T1.run(sp, frozen, None, dispositions=D_deep,
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_JSON_DEFECT')
    D_list = disp(None, raw=json.dumps([json.loads(D0_TEXT)]) + '\n')
    record('T1', 'D-05: the file is a JSON list, not an object', T1.run(sp, frozen, None, dispositions=D_list, text_of_record_addendum=RC0s), False, 'DISPOSITIONS_SHAPE')
    record('T1', 'D-05: an extra top-level key', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o.update(note='x')),
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_KEYS')
    record('T1', 'D-05: a missing top-level key (frozen_addendum_sha256)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV,
           mutate=lambda o: o.pop('frozen_addendum_sha256')), text_of_record_addendum=RC0s), False, 'DISPOSITIONS_KEYS')
    record('T1', 'D-05: a wrong schema', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o.update(
           schema='UNT_V007_LATER_ENTRY_DISPOSITIONS_C4V000')), text_of_record_addendum=RC0s), False, 'DISPOSITIONS_SCHEMA')
    record('T1', 'D-05: the file names another frozen sha', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV,
           mutate=lambda o: o.update(frozen_addendum_sha256=C.sha(f_a))), text_of_record_addendum=RC0s), False, 'DISPOSITIONS_FROZEN_SHA_MISMATCH')
    record('T1', 'D-05: entries is not a list', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o.update(entries={COV[0]: 'no_change'})),
           text_of_record_addendum=RC0s), False, 'DISPOSITIONS_ENTRIES_SHAPE')
    record('T1', 'D-05: a row that is not an object', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'].append(COV[0])),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_SHAPE')
    record('T1', 'D-05: an extra key in a row', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(note='x')),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS')
    record('T1', 'D-05: a row without its reason key', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].pop('reason')),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS')
    record('T1', 'D-05: a row without its section_sha256 key', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV,
           mutate=lambda o: o['entries'][0].pop('section_sha256')), text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS')
    record('T1', 'D-05: an entry with a leading zero (A0<n>)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV,
           mutate=lambda o: o['entries'][0].update(entry='A0%d' % NMAX)), text_of_record_addendum=RC0s), False, 'DISPOSITION_ENTRY_FORMAT')
    record('T1', 'D-05: an entry whose later digits are non-ASCII (fullwidth): A, an ASCII first digit, then U+FF10.. digits', T1.run(sp, frozen, None,
           dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(entry='A' + str(NMAX)[0] + ''.join(chr(0xFF10 + int(ch))
                                                                                                           for ch in str(NMAX)[1:]))),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_ENTRY_FORMAT')
    record('T1', 'D-05: an empty reason', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(reason='')),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_REASON_EMPTY')
    record('T1', 'D-05: a whitespace-only reason', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(reason=' \n\t ')),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_REASON_EMPTY')
    record('T1', 'D-05: a reason that is not a string', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(reason=5)),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_REASON_EMPTY')
    record('T1', 'D-05: a bad disposition (maybe)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(
           disposition='maybe')), text_of_record_addendum=RC0s), False, 'DISPOSITION_VALUE')
    record('T1', 'D-05: a disposition in the table\'s spelling (NO_CHANGE)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV,
           mutate=lambda o: o['entries'][0].update(disposition='NO_CHANGE')), text_of_record_addendum=RC0s), False, 'DISPOSITION_VALUE')
    record('T1', 'D-05: a disposition that is a list (unhashable; a typed code, not an exception)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV,
           mutate=lambda o: o['entries'][0].update(disposition=['no_change'])), text_of_record_addendum=RC0s), False, 'DISPOSITION_VALUE', absent='INTERNAL_EXCEPTION')
    r_ = record('T1', 'D-05: a missing row (entries [] while A<NMAX> is a later entry)', T1.run(sp, frozen, None, dispositions=disp(frozen, rows=[]),
                text_of_record_addendum=RC0s), False, 'UNCOVERED_LATER_ENTRY', absent='DISPOSITIONS_REQUIRED')
    check('T1', 'D-05: a file missing a needed row is not returned as verified', r_.get('later_entry_dispositions') is None
          and 'DISPOSITIONS_VERIFIED' not in [n['code'] for n in r_['notes']], repr(r_.get('later_entry_dispositions'))[:120])
    record('T1', 'D-05: a duplicate row', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV + COV), text_of_record_addendum=RC0s), False,
           'DISPOSITION_DUPLICATE_ENTRY')
    record('T1', 'D-05: a wrong section sha', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(
        section_sha256=C.sha_bytes(SECS[NMAX - 1][0][1]))), text_of_record_addendum=RC0s), False, 'DISPOSITION_SECTION_SHA_MISMATCH')
    record('T1', 'D-05: the section sha in capitals', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(
        section_sha256=o['entries'][0]['section_sha256'].upper())), text_of_record_addendum=RC0s), False, 'DISPOSITION_SECTION_SHA_MISMATCH')
    record('T1', 'D-05: an extra row for an unchanged tabled and cited entry (A85)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV + ['A85']),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_FOR_TABLED_ENTRY')
    r_ = T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV + ['A85']), text_of_record_addendum=RC0s)
    check('T1', 'D-05: that A85 row is refused both as tabled and as cited', {'DISPOSITION_FOR_TABLED_ENTRY', 'DISPOSITION_FOR_CITED_ENTRY'} <= {f['code'] for f in r_['failures']},
          repr([f['code'] for f in r_['failures']]))
    record('T1', 'D-05: an extra row for a cited entry with no table row (A60, before the table)', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV + ['A60']),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_FOR_CITED_ENTRY', absent='DISPOSITION_FOR_TABLED_ENTRY')
    r_ = T1.run(sp, frozen, None, text_of_record_addendum=RC0s)
    check('T1', 'D-05: no dispositions file while A<NMAX> is a later entry: DISPOSITIONS_REQUIRED names it (and UNCOVERED_LATER_ENTRY)',
          r_['verdict'] == 'REFUSE' and any(f['code'] == 'DISPOSITIONS_REQUIRED' and COV[0] in f['detail'] for f in r_['failures'])
          and 'UNCOVERED_LATER_ENTRY' in [f['code'] for f in r_['failures']], repr(r_['failures'])[:300])
    tor_thl90 = text_of_record('variant_tor_table_has_later_A90_edited.json', ptb=str(f_90), tab=table(ents(NMAX), rc=RCF))
    r_ = T1.run(tor_thl90, f_90, None, text_of_record_addendum=RCFs)
    check('T1', 'D-05: no dispositions file while only a changed table row (A90) needs one: DISPOSITIONS_REQUIRED names A90',
          r_['verdict'] == 'REFUSE' and any(f['code'] == 'DISPOSITIONS_REQUIRED' and 'A90' in f['detail'] for f in r_['failures'])
          and 'ENTRY_TABLE_SECTION_CHANGED' in [f['code'] for f in r_['failures']] and 'UNCOVERED_LATER_ENTRY' not in [f['code'] for f in r_['failures']]
          and r_.get('dispositions_required') == ['A90'], repr(r_['failures'])[:300],
          why='0640: the change is made in the frozen bytes (A90 edited after the full read copy), not by a bad table-row sha')
    record('T1', 'D-05 control: that changed A90 with a proper no_change_after_change row (no later entry) passes', T1.run(tor_thl90, f_90, None,
           dispositions=disp(f_90, nca={'A90': EDIT90[:40]}), text_of_record_addendum=RCFs), True, note='ENTRY_TABLE_SECTION_CHANGED_NOTED', tag='NEW_CONTROL')
    record('T1', 'D-05 control: nothing needs a row and the file has entries []: it passes and is verified', T1.run(sp_thl, frozen, None,
           dispositions=disp(frozen, rows=[]), text_of_record_addendum=RCFs), True, note='DISPOSITIONS_VERIFIED', tag='NEW_CONTROL')
    r_ = T1.run(sp, frozen, None, dispositions=D0, text_of_record_addendum=RC0s)
    led = r_.get('later_entry_dispositions') or {}
    check('T1', 'D-05 control: tool 1 returns the verified file (its pin, the parsed content and the exact text) and the read copy\'s pin', r_['verdict'] == 'PASS'
          and led.get('pin') == {'path': D0[0], 'sha256': D0[1]} and led.get('content') == json.loads(D0_TEXT) and led.get('raw_text') == D0_TEXT
          and r_.get('dispositions_required') == COV and r_['pins_verified'].get('dispositions') == {'path': D0[0], 'sha256': D0[1]}
          and r_.get('addendum_at_text_of_record') == {'path': RC0s, 'sha256': C.sha(RC0)} == r_['pins_verified'].get('addendum_at_text_of_record'),
          repr([f['code'] for f in r_['failures']]), tag='NEW_CONTROL')
    # ================= tool 1, 0640: the read copy (old bytes)
    record('T1', '0640: no read copy given (API text_of_record_addendum=None): ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED, and the disposition layer is skipped',
           T1.run(sp, frozen, None, dispositions=D0), False, 'ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', note='LAYER_SKIPPED')
    rc, so, se = cli(T1.main, ['--prereg', str(sp), '--frozen', str(frozen), '--dispositions', D0[0], '--dispositions-sha', D0[1]])
    check('T1', '0640: the CLI without --addendum-at-text-of-record exits 2 with ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED (a typed code, not a usage error)',
          rc == 2 and jcodes(so) == ['ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED'], 'rc %r codes %r' % (rc, jcodes(so)))
    record('T1', '0640: the read copy path does not exist', T1.run(sp, frozen, None, dispositions=D0, text_of_record_addendum=RC0s + '.missing'), False,
           'ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED')
    record('T1', '0640: the read copy path is a directory', T1.run(sp, frozen, None, dispositions=D0, text_of_record_addendum=str(RC0.parent)), False,
           'ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED')
    record('T1', '0640: the frozen copy given as the read copy (its sha is not the prereg\'s addendum_read pin)', T1.run(sp, frozen, None, dispositions=D0,
           text_of_record_addendum=str(frozen)), False, 'ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH')
    rc_x = xwb(run / 'read_copies/V005_READ_COPY_ONE_BYTE_CHANGED_C4V003.md', RC0.read_bytes()[:-1] + b'#')
    record('T1', '0640: a read copy with one byte changed (sha mismatch)', T1.run(sp, frozen, None, dispositions=D0, text_of_record_addendum=str(rc_x)), False,
           'ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH')
    record('T1', '0640: a read copy passed as a Path object is read the same (control)', T1.run(sp, frozen, None, dispositions=D0, text_of_record_addendum=RC0), True,
           tag='NEW_CONTROL')
    _, sp_noar = t1_variant('table_no_addendum_read', tab=table(ents(NMAX - 1), ar=None))
    record('T1', '0640: a prereg whose table has no addendum_read pin', T1.run(sp_noar, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'ADDENDUM_READ_PIN_ABSENT', note='LAYER_SKIPPED')
    _, sp_shortar = t1_variant('table_short_addendum_read', tab=table(ents(NMAX - 1), ar=dict(ar_pin(RC0), sha256_at_generation=C.sha(RC0)[:8])))
    record('T1', '0640: a prereg whose addendum_read sha is an 8-hex prefix', T1.run(sp_shortar, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'ADDENDUM_READ_PIN_ABSENT')
    _, sp_bytes = t1_variant('table_addendum_read_bytes_off', tab=table(ents(NMAX - 1), ar=dict(ar_pin(RC0), bytes=len(RC0.read_bytes()) + 1)))
    record('T1', '0640: a prereg whose addendum_read byte count is not the read copy\'s', T1.run(sp_bytes, frozen, None, dispositions=D0, text_of_record_addendum=RC0s),
           False, 'ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH')
    rc_dup = xwb(run / 'read_copies/V005_READ_COPY_DUPLICATE_HEADING_C4V003.md', RC0.read_bytes() + b'\n## A70: duplicate entry\n')
    tor_rdup = text_of_record('variant_tor_read_copy_duplicate_heading.json', tab=table(ents(NMAX - 1), rc=rc_dup))
    record('T1', '0640: a read copy (pinned by the prereg) that repeats a heading', T1.run(tor_rdup, frozen, None, dispositions=D0, text_of_record_addendum=str(rc_dup)),
           False, 'READ_COPY_DUPLICATE_ENTRY_HEADING')
    rc_no60 = xwb(run / 'read_copies/V005_READ_COPY_WITHOUT_A60_C4V003.md', without_section(RC0.read_bytes(), 60))
    tor_no60 = text_of_record('variant_tor_read_copy_without_A60.json', tab=table(ents(NMAX - 1), rc=rc_no60))
    record('T1', '0640: a read copy (pinned by the prereg) that lacks a cited entry (A60)', T1.run(tor_no60, frozen, None, dispositions=disp(frozen, later=COV + ['A60']),
           text_of_record_addendum=str(rc_no60)), False, 'CITED_ENTRY_ABSENT_FROM_READ_COPY')
    f_nomax = xwb(run / 'variant_without_newest/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', without_section(FB, NMAX))
    tor_gone = text_of_record('variant_tor_read_copy_entry_gone_from_frozen.json', ptb=str(f_nomax), tab=table(ents(NMAX - 1), rc=RCF))
    record('T1', '0640: an entry of the read copy (A<NMAX>, uncited) that the frozen copy lacks', T1.run(tor_gone, f_nomax, None, dispositions=disp(f_nomax, rows=[]),
           text_of_record_addendum=RCFs), False, 'READ_COPY_ENTRY_ABSENT_FROM_FROZEN', exact=['READ_COPY_ENTRY_ABSENT_FROM_FROZEN'])
    _, sp_rowbad = t1_variant('table_row_not_read_copy', tab=table(ents(NMAX - 1), bad_sha=('A90',)))
    record('T1', '0640: a table row whose sha is neither the read copy\'s nor the frozen section (the r2 changed-row fixture) refuses',
           T1.run(sp_rowbad, frozen, None, dispositions=disp(frozen, later=COV, nca={'A90': 'x'}), text_of_record_addendum=RC0s), False,
           'ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD')
    _, sp_rowhead = t1_variant('table_row_heading_not_read_copy', tab=table(ents(NMAX - 1), mutate_row=lambda r: r.update(heading=r['heading'] + ' (edited)')
                                                                           if r['entry'] == 'A84' else None))
    record('T1', '0640: a table row whose heading is not the read copy\'s', T1.run(sp_rowhead, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD')
    _, sp_rowlen = t1_variant('table_row_bytes_not_read_copy', tab=table(ents(NMAX - 1), mutate_row=lambda r: r.update(section_bytes=r['section_bytes'] + 1)
                                                                         if r['entry'] == 'A84' else None))
    record('T1', '0640: a table row whose section_bytes is not the read copy\'s', T1.run(sp_rowlen, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False,
           'ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD')
    _, sp_rowmax = t1_variant('table_row_entry_not_in_read_copy', tab=table(ents(NMAX - 1), rc=RCF, mutate_row=None))
    record('T1', '0640 control: a stand-in whose addendum_read pins the full copy (A<NMAX> unchanged in it, no table row) passes with that copy and an L row',
           T1.run(sp_rowmax, frozen, None, dispositions=D0, text_of_record_addendum=RCFs), True, tag='NEW_CONTROL')
    tor_rowmax2 = text_of_record('variant_tor_table_rows_newest_read_copy_lacks.json', tab=table(ents(NMAX), rc=RCF, ar=ar_pin(RC0)))
    record('T1', '0640: a table row for an entry the pinned read copy lacks (A<NMAX>; it is in L, absent from the read copy, so D0\'s row for it is due)',
           T1.run(tor_rowmax2, frozen, None, dispositions=D0, text_of_record_addendum=RC0s), False, 'ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD',
           exact=['ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD'])
    # ================= tool 1, 0640: CH dispositions (C-01, PV-D05-1 and the mechanical changed_text rule)
    tor_62 = text_of_record('variant_tor_A62_edited.json', ptb=str(f_62))
    D62 = disp(f_62, later=COV, nca={'A62': EDIT62[:30]})
    r2l = importlib.machinery.SourceFileLoader('check_frozen_addendum_c4v002_r2ref', str(R2 / 'check_frozen_addendum_c4v002.py'))
    r2T1 = importlib.util.module_from_spec(importlib.util.spec_from_loader(r2l.name, r2l))
    r2l.exec_module(r2T1)
    rr = r2T1.run(str(tor_62), str(f_62), None, tuple(COV))
    check('T1', 'REPRO C-01 on r2\'s own tool 1 (06a98bc6): an edit inside the cited A62 (no table row) passes unseen', rr['verdict'] == 'PASS', repr(rr['failures']),
          tag='REPRO')
    r_ = record('T1', 'C-01: an edit inside the cited A62 with no dispositions row refuses ENTRY_SECTION_CHANGED', T1.run(tor_62, f_62, None,
                dispositions=disp(f_62, later=COV), text_of_record_addendum=RC0s), False, 'ENTRY_SECTION_CHANGED', exact=['ENTRY_SECTION_CHANGED'])
    r_ = T1.run(tor_62, f_62, None, text_of_record_addendum=RC0s)
    check('T1', 'C-01: with no dispositions file at all, A62 is required too (DISPOSITIONS_REQUIRED names A62 and A<NMAX>)', r_['verdict'] == 'REFUSE'
          and r_.get('dispositions_required') == sorted(['A62'] + COV, key=lambda e: int(e[1:])) and 'ENTRY_SECTION_CHANGED' in [f['code'] for f in r_['failures']],
          repr([f['code'] for f in r_['failures']]) + repr(r_.get('dispositions_required')))
    r_ = record('T1', 'C-01 control: the A62 edit with a correct no_change_after_change row passes', T1.run(tor_62, f_62, None, dispositions=D62,
                text_of_record_addendum=RC0s), True, note='ENTRY_SECTION_CHANGED_NOTED', tag='NEW_CONTROL')
    check('T1', 'C-01 control: tool 1 reports A62 as a changed section with both shas (read copy and frozen)', any(
        c['entry'] == 'A62' and c['text_of_record_section_sha256'] == C.sha_bytes(SECS[62][0][1]) and c['frozen_section_sha256'] == C.sha_bytes(
            T1.sections(f_62.read_bytes())[62][0][1]) and c['table_row_section_sha256'] is None for c in r_.get('changed_sections', [])),
          repr(r_.get('changed_sections'))[:300], tag='NEW_CONTROL')
    record('T1', 'PV-D05-1 (0640): plain no_change on the changed A62 refuses', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV + ['A62']),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', exact=['DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY'])
    record('T1', 'PV-D05-1 (0640): plain no_change on the changed table row A90 refuses (the pre-0640 control "a changed row may be no_change" is inverted)',
           T1.run(tor_90, f_90, None, dispositions=disp(f_90, later=COV + ['A90']), text_of_record_addendum=RC0s), False,
           'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', exact=['DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY'],
           why='0640 inverts the pre-0640 dev control (plain no_change that names the change in a change object)')
    a62_head = T1.sections(f_62.read_bytes())[62][0][0]
    for nm_, ct_, code_ in (('changed_text present in the old bytes too (the A62 heading line)', a62_head, 'DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION'),
                            ('changed_text absent from the new bytes', 'SYNTHETIC EDIT INSIDE A62 (not this text)', 'DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_SECTION'),
                            ('a generic changed_text ("no change")', 'no change', 'DISPOSITION_CHANGED_TEXT_'),
                            ('a generic changed_text ("the section changed")', 'the section changed', 'DISPOSITION_CHANGED_TEXT_'),
                            ('a generic changed_text present in both sections ("## A62:")', '## A62:', 'DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION'),
                            ('an empty changed_text', '', 'DISPOSITION_CHANGED_TEXT_EMPTY'),
                            ('a changed_text that is not a string', 62, 'DISPOSITION_CHANGED_TEXT_EMPTY'),
                            ('a changed_text with a lone surrogate (no UTF-8 form)', 'SYNTHETIC \ud800 EDIT', 'DISPOSITION_CHANGED_TEXT_ENCODING')):
        record('T1', '0640: %s refuses' % nm_, T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': ct_}), text_of_record_addendum=RC0s),
               False, code_, absent='INTERNAL_EXCEPTION')
    tor_62u = text_of_record('variant_tor_A62_edited_utf8.json', ptb=str(f_62u))
    record('T1', '0640 control: a non-ASCII changed_text (NFC, as in the bytes) passes', T1.run(tor_62u, f_62u, None, dispositions=disp(f_62u, later=COV,
           nca={'A62': 'café EDIT INSIDE A62'}), text_of_record_addendum=RC0s), True, tag='NEW_CONTROL')
    record('T1', '0640: the same changed_text in NFD (not the bytes) refuses', T1.run(tor_62u, f_62u, None, dispositions=disp(f_62u, later=COV,
           nca={'A62': 'café EDIT INSIDE A62'}), text_of_record_addendum=RC0s), False, 'DISPOSITION_CHANGED_TEXT_NOT_IN_NEW_SECTION')
    for nm_, why_ in (('an empty why_no_prereg_effect', ''), ('a whitespace-only why_no_prereg_effect', '  \n '), ('a why_no_prereg_effect that is not a string', None)):
        record('T1', '0640: %s refuses' % nm_, T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': EDIT62[:30]},
               mutate=lambda o, w=why_: o['entries'][1].update(why_no_prereg_effect=w)), text_of_record_addendum=RC0s), False, 'DISPOSITION_WHY_NO_PREREG_EFFECT_EMPTY')
    record('T1', '0640: a no_change_after_change row without why_no_prereg_effect', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV,
           nca={'A62': EDIT62[:30]}, mutate=lambda o: o['entries'][1].pop('why_no_prereg_effect')), text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS')
    record('T1', '0640: a no_change_after_change row that also carries a reason key', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV,
           nca={'A62': EDIT62[:30]}, mutate=lambda o: o['entries'][1].update(reason='x')), text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS')
    record('T1', '0640: the removed pre-0640 change object on a CH row refuses', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, nca={'A62': EDIT62[:30]},
           mutate=lambda o: o['entries'][1].update(change={'from_section_sha256': C.sha_bytes(SECS[62][0][1]), 'to_section_sha256': o['entries'][1]['section_sha256'],
                                                           'what_changed': 'x'})), text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS',
           why='0640 removes the change {from, to, what_changed} object of the pre-0640 dev design')
    record('T1', '0640: a CH row whose section_sha256 is the old (read-copy) section', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV,
           nca={'A62': EDIT62[:30]}, mutate=lambda o: o['entries'][1].update(section_sha256=C.sha_bytes(SECS[62][0][1]))), text_of_record_addendum=RC0s), False,
           'DISPOSITION_SECTION_SHA_MISMATCH')
    record('T1', '0640: no_change_after_change on an unchanged later entry (L) refuses', T1.run(sp, frozen, None, dispositions=disp(frozen, rows=[dict(
           disp_row(SECS, COV[0], 'no_change_after_change', SECS[NMAX][0][0]))]), text_of_record_addendum=RC0s), False,
           'DISPOSITION_NO_CHANGE_AFTER_CHANGE_ON_UNCHANGED_ENTRY')
    record('T1', '0640: an L row carrying changed_text refuses', T1.run(sp, frozen, None, dispositions=disp(frozen, later=COV, mutate=lambda o: o['entries'][0].update(
           changed_text=SECS[NMAX][0][0])), text_of_record_addendum=RC0s), False, 'DISPOSITION_ROW_KEYS')
    # revised rows and their prereg_revision pins
    record('T1', '0640 control: the changed A62 disposed revised with a real pinned revision file passes', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV,
           revised=['A62']), text_of_record_addendum=RC0s), True, note='ENTRY_SECTION_CHANGED_NOTED', tag='NEW_CONTROL')
    r_ = T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62']), text_of_record_addendum=RC0s)
    check('T1', '0640 control: the verified revision pin is reported', any(k.endswith('A62.prereg_revision') and v == REV for k, v in r_['pins_verified'].items()),
          repr(sorted(r_['pins_verified'])), tag='NEW_CONTROL')
    record('T1', '0640 control: a later entry (L) disposed revised with a real pinned revision file passes', T1.run(sp, frozen, None,
           dispositions=disp(frozen, revised=COV), text_of_record_addendum=RC0s), True, tag='NEW_CONTROL',
           why='0640: a revised row now carries its prereg_revision pin (the pre-0640 dev control had none)')
    record('T1', '0640: revised without prereg_revision refuses', T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62'],
           mutate=lambda o: o['entries'][1].pop('prereg_revision')), text_of_record_addendum=RC0s), False, 'DISPOSITION_PREREG_REVISION_REQUIRED')
    for nm_, ref_, code_ in (('a forged sha (not the file\'s bytes)', dict(REV, sha256='0' * 64), 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('a missing file', dict(REV, path=REV['path'] + '.missing'), 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('a relative path', dict(REV, path=os.path.relpath(REV['path'])), 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('an 8-hex sha prefix', dict(REV, sha256=REV['sha256'][:8]), 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('a pin with an extra key', dict(REV, note='x'), 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('a bare path string', REV['path'], 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('a pin naming a directory', {'path': str(rev_file.parent), 'sha256': REV['sha256']}, 'DISPOSITION_PREREG_REVISION_PIN'),
                             ('the prereg under check itself', pin(tor_62), 'DISPOSITION_PREREG_REVISION_IS_THE_PREREG')):
        record('T1', '0640: revised with %s as prereg_revision refuses' % nm_, T1.run(tor_62, f_62, None, dispositions=disp(f_62, later=COV, revised=['A62'],
               mutate=lambda o, r=ref_: o['entries'][1].update(prereg_revision=r)), text_of_record_addendum=RC0s), False, code_, absent='INTERNAL_EXCEPTION')
    tor_62copy = xw(run / 'variant_tor_A62_edited_COPY_AS_REVISION.json', tor_62.read_bytes().decode('utf-8'))
    record('T1', '0640: revised with a byte-identical copy of the prereg as prereg_revision refuses (by sha)', T1.run(tor_62, f_62, None,
           dispositions=disp(f_62, later=COV, revised=['A62'], mutate=lambda o: o['entries'][1].update(prereg_revision=pin(tor_62copy))),
           text_of_record_addendum=RC0s), False, 'DISPOSITION_PREREG_REVISION_IS_THE_PREREG')
    # ================= Codex1's PV-D05-1 fixture (0081/0083; PROVISIONAL_REVIEW_CX1V002 c483cc99): verbatim, then with a read copy
    cxp, cxf, cxd = CX1_PV
    r_ = record('T1', 'PV-D05-1 (Codex1 fixture b1b6000f, verbatim; its prereg has no addendum_read): refuses', T1.run(str(cxp), str(cxf), C.sha(cxf),
                dispositions=(str(cxd), C.sha(cxd))), False, 'ADDENDUM_READ_PIN_ABSENT')
    check('T1', 'PV-D05-1 (verbatim): no verified dispositions are returned', r_.get('later_entry_dispositions') is None and 'DISPOSITIONS_VERIFIED' not in
          [n['code'] for n in r_['notes']], repr(r_.get('later_entry_dispositions'))[:120])
    old90 = CX1_OLD_A90.read_bytes()
    rc_cx = xwb(run / 'read_copies/CX1_PV_D05_1_READ_COPY_WITH_OLD_A90_C4V003.md', with_section(cxf.read_bytes(), 90, old90))
    assert C.sha_bytes(T1.sections(rc_cx.read_bytes())[90][0][1]) == C.sha(CX1_OLD_A90) and changed_entries(cxf.read_bytes(), rc_cx.read_bytes()) == [90]

    def augmented(src, rcp, name):
        d = json.loads(Path(src).read_bytes())
        d['entries_after_A81']['addendum_read'] = {'open_path': 'SYNTHETIC', 'sha256_at_generation': C.sha(rcp), 'bytes': len(Path(rcp).read_bytes()),
                                                   'byte_copy': 'SYNTHETIC read copy (Claude4 seal tools v003 tests): %s' % Path(rcp).name}
        return xw(run / name, json.dumps(d, indent=1) + '\n')
    cxp_aug = augmented(cxp, rc_cx, 'CX1_PV_D05_1_PREREG_WITH_ADDENDUM_READ_C4V003.json')
    r_ = record('T1', 'PV-D05-1 (Codex1 fixture b1b6000f with the read copy built from Codex1\'s own OLD_A90_SECTION 92129acd): refuses '
                'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', T1.run(str(cxp_aug), str(cxf), C.sha(cxf), dispositions=(str(cxd), C.sha(cxd)),
                                                                      text_of_record_addendum=str(rc_cx)), False, 'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY')
    check('T1', 'PV-D05-1 (with the read copy): a refusing run returns no verified dispositions file', r_.get('later_entry_dispositions') is None
          and 'dispositions' not in r_['pins_verified'], repr(r_.get('later_entry_dispositions'))[:120])
    cx_row = json.loads(cxd.read_bytes())['entries'][0]
    D_cx_nc = disp(cxf, rows=[{k: cx_row[k] for k in ('entry', 'disposition', 'reason', 'section_sha256')}])
    record('T1', 'PV-D05-1 in the v003 row shape (Codex1\'s A90 row without its pre-0640 change object): refuses on that rule alone',
           T1.run(str(cxp_aug), str(cxf), C.sha(cxf), dispositions=D_cx_nc, text_of_record_addendum=str(rc_cx)), False,
           'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', exact=['DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY'])
    record('T1', 'PV-D05-1 control: Codex1\'s A90 with no_change_after_change, changed_text "changed scientific rule" (new bytes only), passes',
           T1.run(str(cxp_aug), str(cxf), C.sha(cxf), dispositions=disp(cxf, nca={'A90': 'changed scientific rule'}), text_of_record_addendum=str(rc_cx)), True,
           note='ENTRY_TABLE_SECTION_CHANGED_NOTED', tag='NEW_CONTROL')
    record('T1', 'PV-D05-1: Codex1\'s A90 with changed_text "synthetic rule" (in the old and the new bytes) refuses', T1.run(str(cxp_aug), str(cxf), C.sha(cxf),
           dispositions=disp(cxf, nca={'A90': 'synthetic rule'}), text_of_record_addendum=str(rc_cx)), False, 'DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION')
    # ================= Codex3's D-05 counterexamples (ED-D05-1, 0637/0639) on Codex3's own fixtures
    lp, lf = CX3_LATER
    cp_, cf = CX3_CHANGED
    rr = r2T1.run(str(lp), str(lf), C.sha(lf), ('A102',))
    check('T1', 'REPRO ED-D05-1 on r2\'s own tool 1 (06a98bc6): the bare A102 passes on Codex3\'s later_bare_note fixture', rr['verdict'] == 'PASS', repr(rr['failures']),
          tag='REPRO')
    rr = r2T1.run(str(cp_), str(cf), C.sha(cf), ('A90',))
    check('T1', 'REPRO ED-D05-1 on r2\'s own tool 1: the changed A90 under a bare name passes on Codex3\'s changed_row_bare_note fixture', rr['verdict'] == 'PASS',
          repr(rr['failures']), tag='REPRO')
    record('T1', 'Codex3 ED-D05-1 (a), verbatim: the bare A102 now refuses (COVERED_LATER_BARE_NAMES_REFUSED)', T1.run(str(lp), str(lf), C.sha(lf), ('A102',)),
           False, 'COVERED_LATER_BARE_NAMES_REFUSED')
    rc_l = xwb(run / 'read_copies/CX3_LATER_READ_COPY_WITHOUT_A102_C4V003.md', without_section(lf.read_bytes(), 102))
    lp_aug = augmented(lp, rc_l, 'CX3_LATER_PREREG_WITH_ADDENDUM_READ_C4V003.json')
    rc_c = xwb(run / 'read_copies/CX3_CHANGED_READ_COPY_WITH_OLD_A90_C4V003.md', with_section(cf.read_bytes(), 90, old90))
    cp_aug = augmented(cp_, rc_c, 'CX3_CHANGED_PREREG_WITH_ADDENDUM_READ_C4V003.json')
    r_ = record('T1', 'Codex3 ED-D05-1 (a) with a read copy: the bare A102 refuses, and A102 stays uncovered', T1.run(str(lp_aug), str(lf), C.sha(lf), ('A102',),
                text_of_record_addendum=str(rc_l)), False, 'COVERED_LATER_BARE_NAMES_REFUSED',
                why='0640: Codex3\'s synthetic prereg has no addendum_read; the copy pins a read copy (its frozen bytes without A102)')
    check('T1', 'Codex3 ED-D05-1 (a): ... and A102 is reported uncovered and required', {'UNCOVERED_LATER_ENTRY', 'DISPOSITIONS_REQUIRED'} <= {f['code'] for f in r_['failures']},
          repr([f['code'] for f in r_['failures']]), why='0640: run with the read-copy augmented prereg')
    record('T1', 'Codex3 ED-D05-1 (b), verbatim: the changed A90 under a bare name now refuses', T1.run(str(cp_), str(cf), C.sha(cf), ('A90',)), False,
           'COVERED_LATER_BARE_NAMES_REFUSED')
    r_ = T1.run(str(cp_aug), str(cf), C.sha(cf), ('A90',), text_of_record_addendum=str(rc_c))
    check('T1', 'Codex3 ED-D05-1 (b) with a read copy: ... and A90\'s changed section is reported (ENTRY_TABLE_SECTION_CHANGED, DISPOSITIONS_REQUIRED)',
          {'COVERED_LATER_BARE_NAMES_REFUSED', 'ENTRY_TABLE_SECTION_CHANGED', 'DISPOSITIONS_REQUIRED'} <= {f['code'] for f in r_['failures']},
          repr([f['code'] for f in r_['failures']]), why='0640: run with the read-copy augmented prereg (A90 old section = Codex1\'s OLD_A90_SECTION)')
    record('T1', 'Codex3 ED-D05-1 control (a): A102 with a proper no_change row passes on Codex3\'s fixture (read copy given)', T1.run(str(lp_aug), str(lf), C.sha(lf),
           dispositions=disp(lf, later=['A102']), text_of_record_addendum=str(rc_l)), True, note='DISPOSITIONS_VERIFIED', tag='NEW_CONTROL')
    record('T1', 'Codex3 ED-D05-1 control (b): the changed A90 with a proper no_change_after_change row passes on Codex3\'s fixture', T1.run(str(cp_aug), str(cf),
           C.sha(cf), dispositions=disp(cf, nca={'A90': 'changed scientific rule'}), text_of_record_addendum=str(rc_c)), True, note='ENTRY_TABLE_SECTION_CHANGED_NOTED',
           tag='NEW_CONTROL', why='0640: the row is no_change_after_change (the pre-0640 control used a change object)')
    record('T1', 'Codex3 ED-D05-1 (b\'): the changed A90 disposed plain no_change on Codex3\'s fixture refuses', T1.run(str(cp_aug), str(cf), C.sha(cf),
           dispositions=disp(cf, later=['A90']), text_of_record_addendum=str(rc_c)), False, 'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY',
           why='0640: replaces the pre-0640 case (a change object with a wrong from sha)')
    # ================= tool 2
    record('T2', 'genuine', T2.run(reviewed, sc, slots_p, sp), True, tag='PORT', r2=26)

    def chg_nonpin(out):
        i = next(i for i, l in enumerate(out) if l.startswith('TOL') or l.startswith('ART = '))
        out[i] = out[i].rstrip('\n') + '  # tampered\n'
        return out
    record('T2', 'a non-pin line changed', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_a.py', chg_nonpin), slots_p, sp), False, 'NON_PIN_LINE_DIFFERS', tag='PORT', r2=27)
    other_prereg = xw(run / 'other_prereg.json', '{}\n')
    record('T2', 'pin value for another prereg', T2.run(reviewed, sealed_compare_for(slots, other_prereg, 'sc_b.py'), slots_p, sp), False, 'PIN_VALUE_MISMATCH', tag='PORT', r2=28)
    record('T2', 'inserted line', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_c.py', lambda o: o[:10] + ['# inserted\n'] + o[10:]), slots_p, sp), False, 'LINE_COUNT_DIFFERS',
           tag='PORT', r2=29)

    def dup_assign(out):
        i = next(i for i, l in enumerate(out) if l.startswith('# ====') or l.startswith('#'))
        out[i] = "V007_PREREG_SHA256 = '%s'\n" % ('0' * 64)
        return out
    record('T2', 'second assignment of a pin', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_d.py', dup_assign), slots_p, sp), False, 'NON_PIN_LINE_DIFFERS', tag='PORT', r2=30)

    def chg_comment(out):
        i = next(i for i, l in enumerate(out) if l.startswith('V007_PREREG_SHA256 = '))
        out[i] = out[i].replace('# PENDING_FROM_BYTES', '# EDITED')
        return out
    record('T2', 'pin comment changed', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_e.py', chg_comment), slots_p, sp), False, 'PIN_COMMENT_CHANGED', tag='PORT', r2=31)

    def as_list(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_PRODUCER_REGISTRY = '))
        out[i] = 'PIN_PRODUCER_REGISTRY = %r\n' % [slots['producer_registry']['path'], slots['producer_registry']['sha256']]
        return out
    record('T2', 'pair pin as a list', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_f.py', as_list), slots_p, sp), False, 'PIN_PAIR_SHAPE', tag='PORT', r2=32)

    def unset_one(out):
        i = next(i for i, l in enumerate(out) if l.startswith('PIN_V010_R5_CHECK = '))
        out[i] = 'PIN_V010_R5_CHECK = None\n'
        return out
    record('T2', 'one pin left unset', T2.run(reviewed, sealed_compare_for(slots, sp, 'sc_g.py', unset_one), slots_p, sp), False, 'PIN_NOT_SET', tag='PORT', r2=33)
    rv_copy = xw(run / 'variant_reviewed_copy.py', reviewed.read_bytes().decode('utf-8'))
    record('T2', 'reviewed path not the slot', T2.run(rv_copy, sc, slots_p, sp), False, 'REVIEWED_PATH_NOT_THE_SLOT', tag='PORT', r2=34)
    record('T2', 'sealed is the reviewed file', T2.run(reviewed, reviewed, slots_p, sp), False, 'SEALED_IS_REVIEWED', tag='PORT', r2=35)
    sp_j = sealed_prereg_for(slots, TOR, 'variant_j_prereg.json', mutate=lambda d: d['seal_slots']['compare'].update(value=pin(sc)))
    record('T2', 'prereg compare slot holds the sealed compare', T2.run(reviewed, sealed_compare_for(slots, sp_j, 'sc_j.py'), slots_p, sp_j), False,
           'PREREG_COMPARE_SLOT_DIFFERS', tag='PORT', r2=36)
    # D-07
    s_str_p = xw(run / 'slots_bare_pending_string.json', dict(slots, frozen_addendum='PENDING_ROOT_AT_SEAL_ASSEMBLY'))
    record('T2', 'D-07: a bare PENDING string slot refuses PIN_SHAPE (no TypeError)', T2.run(reviewed, sc, s_str_p, sp), False, 'PIN_SHAPE', tag='PORT', r2=37)
    s_lst_p = xw(run / 'slots_list_slot.json', dict(slots, driver_check_record=[str(CHECK_MD), C.sha(CHECK_MD)]))
    record('T2', 'D-07: a list slot refuses PIN_SHAPE', T2.run(reviewed, sc, s_lst_p, sp), False, 'PIN_SHAPE', tag='PORT', r2=38)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = T2.main(['--reviewed', str(reviewed), '--sealed', str(sc), '--slots', str(s_str_p), '--prereg', str(sp)])
    try:
        cli_ = json.loads(buf.getvalue())
    except ValueError:
        cli_ = {}
    check('T2', 'D-07: the CLI exits 2 with a REFUSE verdict JSON (the v001 crash was exit 1)', rc == 2 and cli_.get('verdict') == 'REFUSE'
          and any(f['code'] == 'PIN_SHAPE' for f in cli_.get('failures', [])), 'rc %r verdict %r' % (rc, cli_.get('verdict')), tag='PORT', r2=39)
    # ---- tool 2 with r13 f5adfd11 (A104: the compare of record) as the reviewed source
    slots13 = copy.deepcopy(slots)
    slots13['compare_reviewed_source'] = rpin(reviewed13)
    slots13_p = xw(run / 'SLOTS_R13_SYNTH.json', slots13)
    sp13 = sealed_prereg_for(slots13, TOR, 'KMAX_TAIL_PREREG_V007_SEALED_R13_SYNTH.json')
    sc13 = sealed_compare_for(slots13, sp13, 'sealed_compare_R13_SYNTH.py', src=reviewed13)
    record('T2', 'r13 (A104): genuine, with r13 f5adfd11 as the reviewed source', T2.run(reviewed13, sc13, slots13_p, sp13), True, tag='NEW_CONTROL')
    record('T2', 'r13 (A104): a non-pin line changed in the r13-sealed compare', T2.run(reviewed13, sealed_compare_for(slots13, sp13, 'sc13_a.py', chg_nonpin, src=reviewed13),
           slots13_p, sp13), False, 'NON_PIN_LINE_DIFFERS')
    record('T2', 'r13 (A104): an r12-sealed compare checked against the r13 reviewed source', T2.run(reviewed13, sc, slots13_p, sp13), False)
    # ================= tool 3
    record('T3', 'genuine r5 (real certificates, A92 identity records, CHECK.md, case block validated in-process)',
           T3run(slots_p, sp, TOR, frozen=frozen, dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=sc), True, tag='PORT_CHANGED',
           r2=40, why=WHY_DISP_RC)

    def variant(name, mutate, prereg_mutate=None, same_prereg=False, tor=None):
        s2 = copy.deepcopy(slots)
        mutate(s2)
        p2 = xw(run / ('slots_%s.json' % name), s2)
        sp2 = sp if same_prereg else sealed_prereg_for(s2, tor or TOR, 'prereg_%s.json' % name, prereg_mutate)
        return p2, sp2
    preg = Path(slots['producer_registry']['path'])
    p2, sp2 = variant('pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    record('T3', 'a PENDING value', T3run(p2, sp2, TOR), False, 'PENDING', tag='PORT', r2=41)
    p2, sp2 = variant('badpin', lambda s: s['identity_gate_records']['Z2'].update(sha256='0' * 64))
    record('T3', 'identity record pin bytes differ', T3run(p2, sp2, TOR), False, 'PIN_BYTES_MISMATCH', tag='PORT', r2=42)
    p2, sp2 = variant('text', lambda s: None, prereg_mutate=lambda d: d['tests']['T3'].update(text=d['tests']['T3']['text'] + ' (edited)'))
    record('T3', 'sealed prereg text changed outside the slots', T3run(p2, sp2, TOR), False, 'SEALED_PREREG_TEXT_CHANGED', tag='PORT', r2=43)
    p2, _ = variant('slotdiff', lambda s: s.update(producer_registry=pin(CHECK_MD)), same_prereg=True)
    record('T3', 'prereg slot value differs from the slots', T3run(p2, sp, TOR), False, 'PREREG_SLOT_VALUE_DIFFERS', tag='PORT', r2=44)
    alias = slots['driver']['path'].replace('/driver_r5/', '/driver_r5/./')
    p2, sp2 = variant('driveralias', lambda s: s.update(driver={'path': alias, 'sha256': dsha}))
    record('T3', 'driver slot spelled differently from the plan', T3run(p2, sp2, TOR), False, 'PLAN_DRIVER_NOT_THE_SLOT', tag='PORT', r2=45)
    bad_id = xw(run / 'IDENTITY_Z2_WRONG_DRIVER.json', {'schema': M.GATE_SCHEMA, 'gate': 'B1', 'NEW_DRIVER_PIN': {'pass': True, 'detail': {'result_json_driver_sha256': '2' * 64}}})
    p2, sp2 = variant('iddriver', lambda s: s['identity_gate_records'].update(Z2=pin(bad_id)))
    record('T3', 'identity record carries another driver', T3run(p2, sp2, TOR), False, 'IDENTITY_RECORD', tag='PORT', r2=46)
    lo64 = json.loads(CERTS['LO'].read_bytes())
    lo64['source_gas_M_s'] = 64
    lo64_p = xw(run / 'LO_CERT_M_S64_SYNTH.json', lo64)
    p2, sp2 = variant('lo64', lambda s: s['certificates'].update(LO=pin(lo64_p)))
    record('T3', 'LO certificate at M_s 64', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S', tag='PORT', r2=47)
    cdir = run / 'cache_dir_nonempty'
    cdir.mkdir()
    xw(cdir / 'prewarmed.bin', 'x')
    p2, sp2 = variant('r6full', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir)}, cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    record('T3', 'r6 cache directory not empty (pre-warmed)', T3run(p2, sp2, TOR), False, 'CACHE_DIRECTORY_NOT_EMPTY', tag='PORT', r2=48)
    cdir2 = run / 'cache_dir_empty'
    cdir2.mkdir()
    p2, sp2 = variant('r6empty', lambda s: s.update(driver_branch='r6', cache_directory_r6_only={'path': str(cdir2)}, cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    record('T3', 'r6 with a fresh empty cache directory: the cache rule passes; it refuses only because the slot\'s driver BUILD record is r5 '
           '(v001 passed this; A96: V007 seals on r5)', T3run(p2, sp2, TOR), False, 'DRIVER_BUILD_NOT_THE_BRANCH', absent='CACHE_DIRECTORY', tag='PORT', r2=49)
    p2, sp2 = variant('r5cache', lambda s: s.update(cache_directory_r6_only={'path': str(cdir2)}))
    record('T3', 'r5 slot set naming a cache directory', T3run(p2, sp2, TOR), False, 'CACHE_DIRECTORY_UNDER_R5', tag='PORT', r2=50)
    cmd2 = xw(run / 'BOUND_COMMAND_EDITED.txt', cmd_p.read_bytes().decode('utf-8').replace('--execute-root-only', '--execute-root-only --worker'))
    p2, sp2 = variant('cmd', lambda s: s['launch_packet'].update(bound_command=rpin(cmd2)))
    record('T3', 'bound command edited', T3run(p2, sp2, TOR), False, 'BOUND_COMMAND_NOT_THE_BINDER_LINE', tag='PORT', r2=51)
    dupslots = xw(run / 'slots_dupkey.json', slots_p.read_bytes().decode('utf-8').replace('{\n "schema"', '{\n "schema": "x",\n "schema"', 1))
    record('T3', 'slot JSON with a duplicate key', T3run(dupslots, sp, TOR), False, 'INPUT_JSON', tag='PORT', r2=52)
    use(TOR)
    record('T3', 'text of record is not the pinned r5 (r4 given)', T3.run(slots_p, sp, R4), False, 'TEXT_OF_RECORD_NOT_R5', tag='PORT', r2=53)
    p2, sp2 = variant('build6slot', lambda s: s['launch_packet'].update(build=pin(BUILD_V006)), same_prereg=True)
    record('T3', 'launch build not the prereg-named BUILD_V007 (slots name BUILD_V006)', T3run(p2, sp, TOR), False, 'BUILD_NOT_THE_PREREG_NAMED_BUILD', tag='PORT', r2=54)
    # ---- D-01
    dbl = json.loads(CERTS['DOUBLING'].read_bytes())
    chk = C.Checker('x')
    n = T3.certificate_ms_codes(chk, 'DOUBLING', dbl, 128, 96)
    check('T3', 'D-01 REAL: DOUBLING ea48ac2b states its M_s only as ddo_gas_M_s; tool 3 reads it (1 field, no refusal)', n == 1 and not chk.failures,
          'n %d failures %r' % (n, chk.failures), tag='PORT', r2=55)
    v1 = importlib.machinery.SourceFileLoader('check_slot_fill_c4v001_ref', str(CA / 'v007_final_prereg_c4/seal_tools/check_slot_fill_c4v001.py'))
    v1m = importlib.util.module_from_spec(importlib.util.spec_from_loader(v1.name, v1))
    sys.path.insert(0, str(CA / 'v007_final_prereg_c4/seal_tools'))
    v1.exec_module(v1m)
    check('T3', 'D-01 reproduction: the v001 scanner finds no M_s in the real DOUBLING record (the defect)', v1m.ms_values(dbl) == [], repr(v1m.ms_values(dbl)), tag='PORT', r2=56)

    def cert_variant(name, kind, mutate):
        d = json.loads(CERTS[kind].read_bytes())
        mutate(d)
        f = xw(run / ('CERT_%s_SYNTH.json' % name), d)
        return variant('cert_' + name, lambda s: s['certificates'].update({kind: pin(f)}))
    p2, sp2 = cert_variant('dbl64', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=64))
    record('T3', 'D-01: DOUBLING ddo_gas_M_s 64 contradicts the registered M_s 128', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S', tag='PORT', r2=57)
    p2, sp2 = cert_variant('dblnoms', 'DOUBLING', lambda d: d.pop('ddo_gas_M_s'))
    record('T3', 'D-01: DOUBLING without ddo_gas_M_s', T3run(p2, sp2, TOR), False, 'CERTIFICATE_STATES_NO_M_S', tag='PORT', r2=58)
    p2, sp2 = cert_variant('dblngc128', 'DOUBLING', lambda d: d['ngc_half'].update(gas_M_s=128))
    record('T3', 'D-01: DOUBLING NGC half states M_s 128 against the ngc_gas_M_s slot 96', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S', tag='PORT', r2=59)
    p2, sp2 = cert_variant('dblngc96', 'DOUBLING', lambda d: d['ngc_half'].update(gas_M_s=96))
    record('T3', 'D-01: DOUBLING NGC half states M_s 96, consistent with the slot', T3run(p2, sp2, TOR, frozen=frozen, dispositions=D0, text_of_record_addendum=RC0s),
           True, tag='PORT_CHANGED', r2=60, why=WHY_DISP_RC)
    p2, sp2 = cert_variant('gqdbl', 'GQ', lambda d: d['rosters'][0].update(M_s_doubled=255))
    record('T3', 'D-01: GQ roster M_s_doubled is not 2 M_s', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S_DOUBLED', tag='PORT', r2=61)
    p2, sp2 = cert_variant('gqngc', 'GQ', lambda d: [r.update(M_s=128, M_s_doubled=256) for r in d['rosters'] if r['roster'] == 'NGC_T120L'])
    record('T3', 'D-01: GQ NGC_T120L roster at M_s 128 against the slot 96', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S', tag='PORT', r2=62)
    p2, sp2 = cert_variant('loecho', 'LO', lambda d: d['tail_config_gas'].update(M_s=64))
    record('T3', 'D-01: LO tail_config_gas.M_s 64 contradicts source_gas_M_s (A73 F2)', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S', tag='PORT', r2=63)
    p2, sp2 = cert_variant('ambig', 'EPS', lambda d: d.update(ddo_ngc_gas_M_s=128))
    record('T3', 'D-01: an M_s key naming both DDO and NGC', T3run(p2, sp2, TOR), False, 'CERTIFICATE_M_S_CONTEXT_AMBIGUOUS', tag='PORT', r2=64)
    p2, sp2 = variant('certgate', lambda s: s['certificates'].update(LO=pin(CERTS['GQ'])))
    record('T3', 'a certificate slot holding another gate\'s record (LO slot = the GQ record)', T3run(p2, sp2, TOR), False, 'CERTIFICATE_NOT_THE_SLOT_GATE', tag='PORT', r2=65)
    p2, sp2 = variant('idgate', lambda s: s['identity_gate_records'].update(Z2=pin(IDENTITY_FILES['Z2_OFF_RO1'])))
    record('T3', 'an identity slot holding another gate\'s record (Z2 slot = the B1_OFF record)', T3run(p2, sp2, TOR), False, 'IDENTITY_RECORD_NOT_THE_SLOT_GATE',
           tag='PORT', r2=66)
    p2, sp2 = variant('ngc128', lambda s: s.update(ngc_gas_M_s=128))
    record('T3', 'ngc_gas_M_s 128 against the compare\'s NGC 96 (RI-23 needs a compare successor)', T3run(p2, sp2, TOR), False, 'NGC_GAS_M_S_NOT_THE_COMPARE_NGC_M_S',
           tag='PORT', r2=67)
    record('T3', 'ngc_gas_M_s 128: DOUBLING and LO_NGC must state the recomputed NGC M_s (RI-23)', T3run(p2, sp2, TOR), False, 'NGC_M_S_128_NOT_EVIDENCED', tag='PORT', r2=68)
    # ---- D-04 case block
    tor_x = text_of_record('variant_tor_no_case_block.json', case_blk=None)
    record('T3', 'D-04: no binding_inputs.case_block in the sealed prereg', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_no_case_block.json'), tor_x),
           False, 'CASE_BLOCK_PIN_ABSENT', tag='PORT', r2=69)
    tor_x = text_of_record('variant_tor_cb_wrong_sha.json', case_blk={'path': str(cbf), 'sha256': '0' * 64})
    record('T3', 'D-04: case block pin bytes differ', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_cb_wrong_sha.json'), tor_x), False, 'PIN_BYTES_MISMATCH',
           tag='PORT', r2=70)
    tor_x = text_of_record('variant_tor_cb_extra_key.json', case_blk=dict(pin(cbf), note='x'))
    record('T3', 'D-04: case block pin with an extra key', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_cb_extra_key.json'), tor_x), False,
           'CASE_BLOCK_PIN_SHAPE', tag='PORT', r2=71)
    tor_x = text_of_record('variant_tor_draft_case_block.json', case_blk=pin(DRAFT_CASE_BLOCK))
    record('T3', 'D-04 REAL: the on-disk draft case block 6bf4ce5a refuses CASE_BLOCK_INVALID',
           T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_draft_case_block.json'), tor_x), False, 'CASE_BLOCK_INVALID', tag='PORT', r2=72)
    cb64 = xw(run / 'CASE_BLOCK_MS64_SYNTH.json', json.dumps(case_block(lambda c: c['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['gas'].update(M_s=64)),
                                                         indent=1) + '\n')
    tor_x = text_of_record('variant_tor_cb_ms64.json', case_blk=pin(cb64))
    record('T3', 'D-04: a case block registering gas M_s 64 (r12 validate_case_block refuses it)',
           T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_cb_ms64.json'), tor_x), False, 'CASE_BLOCK_INVALID', tag='PORT', r2=73)
    tor_x = text_of_record('variant_tor_mode_serial.json', mutate=lambda d: d.update(route_a_mode='serial_with_exemption'))
    record('T3', 'D-04: the prereg and the case block name different route-A modes',
           T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_mode_serial.json'), tor_x), False, 'ROUTE_A_MODE_SOURCES_DIFFER', tag='PORT', r2=74)
    p2, sp2 = variant('nocma', lambda s: s.update(cascade_map_r5_addendum=T3.NOT_APPLICABLE_R6))
    record('T3', 'D-04: r5 without the CASCADE_MAP_R5_ADDENDUM pin (SRR[9])', T3run(p2, sp2, TOR), False, 'CASCADE_MAP_R5_ADDENDUM_REQUIRED_UNDER_R5', tag='PORT', r2=75)
    cma_bad = xw(run / 'CASCADE_MAP_R5_ADDENDUM_NOT_NAMING_THE_MAP_SYNTH.json', {'schema': 'SYNTHETIC', 'amends': 'nothing named'})
    p2, sp2 = variant('cmamap', lambda s: s.update(cascade_map_r5_addendum=rpin(cma_bad)))
    record('T3', 'D-04: a CASCADE_MAP_R5_ADDENDUM that does not name the r5 cascade map', T3run(p2, sp2, TOR), False, 'CASCADE_MAP_R5_ADDENDUM_DOES_NOT_NAME_THE_R5_MAP',
           tag='PORT', r2=76)
    cma_name = xw(run / 'INVENTORY_ADDENDUM_SYNTH.json', json.loads(cma.read_bytes()))
    p2, sp2 = variant('cmaname', lambda s: s.update(cascade_map_r5_addendum=rpin(cma_name)))
    record('T3', 'D-04: an addendum not named CASCADE_MAP_R5_ADDENDUM', T3run(p2, sp2, TOR), False, 'CASCADE_MAP_R5_ADDENDUM_NAME', tag='PORT', r2=77)
    other = next(({'path': p, 'sha256': h} for h, p in allow6 if p != plan['guard']['path'] and p != plan['launcher']['path']))
    p2, sp2 = variant('aeplan', lambda s: s['admission_entry'].update(guard=other))
    record('T3', 'D-04: the admission guard is not the bound plan\'s (SRR[10])', T3run(p2, sp2, TOR), False, 'ADMISSION_ENTRY_NOT_THE_PLAN', tag='PORT', r2=78)
    p2, sp2 = variant('aebuild', lambda s: s['admission_entry'].update(launcher=pin(PKT / 'route_a_token_launcher_cx1v006.py')))
    record('T3', 'D-04: the admission launcher is not a supported BUILD_V007 entry', T3run(p2, sp2, TOR), False, 'ADMISSION_ENTRY_NOT_BUILD_SUPPORTED', tag='PORT', r2=79)
    # ---- D-10
    tor_x = text_of_record('variant_tor_ptb_elsewhere.json', ptb=str(run / 'elsewhere' / frozen.name))
    record('T3', 'D-10: the frozen slot path is not path_to_be', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_ptb_elsewhere.json'), tor_x), False,
           'FROZEN_SLOT_NOT_PATH_TO_BE', tag='PORT', r2=80)
    # ---- A99.1 BUILD_V007
    tor_pend = text_of_record('variant_tor_build_pending.json', build_sha=C.PENDING_BUILD_V007)
    sp_pend = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_pending.json')
    record('T3', 'A99.1: BUILD_V007 still PENDING_BUILD_V007 (gap)', T3run(slots_p, sp_pend, tor_pend), False, 'BUILD_V007_PENDING', tag='PORT', r2=81)
    sp_fill = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_filled.json', fill=C.sha(b7))
    record('T3', 'A99.1: text holds PENDING_BUILD_V007; the sealed prereg fills that one leaf with the real sha', T3run(slots_p, sp_fill, tor_pend,
           frozen=frozen, dispositions=D0, text_of_record_addendum=RC0s), True, note='BUILD_V007_SHA_FILLED_AT_SEAL', tag='PORT_CHANGED', r2=82, why=WHY_DISP_RC)
    sp_x = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_fill_wrong.json', fill='1' * 64)
    record('T3', 'A99.1: a seal-time fill with a sha that is not the file\'s bytes', T3run(slots_p, sp_x, tor_pend), False, 'PIN_BYTES_MISMATCH', tag='PORT', r2=83)
    sp_x = sealed_prereg_for(slots, tor_pend, 'variant_sealed_build_fill_path.json', fill=C.sha(b7), mutate=lambda d: d['seal_slots']['launch_packet'][
        'named_candidates_verified_from_bytes']['build'].update(path=str(b7) + '.alt'))
    record('T3', 'A99.1: the seal-time fill may not change the path', T3run(slots_p, sp_x, tor_pend), False, 'SEALED_PREREG_TEXT_CHANGED', tag='PORT', r2=84)
    for nm, idx in (('BUILD_V006.md', 85), ('BUILD_V005.md', 86)):
        tor_old = text_of_record('variant_tor_%s.json' % nm[:-3], build_path=PKT / nm)
        p2, sp_old = variant('old_' + nm[:-3], lambda s, nm=nm: s['launch_packet'].update(build=pin(PKT / nm)), tor=tor_old)
        record('T3', 'A99.1: the prereg names %s (not BUILD_V007)' % nm[:-3], T3run(p2, sp_old, tor_old), False, 'BUILD_NOT_BUILD_V007', tag='PORT', r2=idx)
    for sub, ents_, code, idx in (('build_v007_13', allow6[:13], 'BUILD_ALLOWLIST_COUNT_NOT_15', 87), ('build_v007_dup', allow6[:14] + [allow6[0]], 'BUILD_ALLOWLIST_DUPLICATE_PATH', 88),
                                  ('build_v007_bytes', [('0' * 64, allow6[0][1])] + allow6[1:], 'BUILD_ALLOWLIST_SOURCE_BYTES', 89)):
        bx = build_v007(sub=sub, entries=ents_)
        tor_x = text_of_record('variant_tor_%s.json' % sub, build_path=bx)
        p2, sp_x = variant(sub, lambda s, bx=bx: s['launch_packet'].update(build=pin(bx)), tor=tor_x)
        record('T3', 'A99.1: a BUILD_V007 %s' % {'build_v007_13': 'with 13 sources (V6-S3 needs 15)', 'build_v007_dup': 'listing one source twice',
                                                 'build_v007_bytes': 'entry whose sha is not its bytes'}[sub], T3run(p2, sp_x, tor_x), False, code, tag='PORT', r2=idx)
    # ---- driver BUILD record (sealed-mode activation)
    p2, sp2 = variant('dcr', lambda s: s.update(driver_check_record=pin(CERTS['LO'])))
    record('T3', 'the driver BUILD record\'s check_record is not the driver_check_record slot', T3run(p2, sp2, TOR), False, 'DRIVER_BUILD_CHECK_RECORD_NOT_THE_SLOT',
           tag='PORT', r2=90)
    badb = json.loads(r5text)
    badb['ro1_custody']['worker']['sha256'] = '3' * 64
    badb_p = xw(run / 'DRIVER_BUILD_BAD_WORKER_SYNTH.json', json.dumps(badb, indent=1, sort_keys=True) + '\n')
    p2, sp2 = variant('dbrbad', lambda s: s.update(driver_build_record=rpin(badb_p)))
    record('T3', 'a driver BUILD record the compare\'s activate_driver_build refuses', T3run(p2, sp2, TOR), False, 'DRIVER_BUILD_RECORD_REFUSED', tag='PORT', r2=91)
    # ---- text of record pending; D-08 layered reporting; unknown slots; real r12 path
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    res = T3.run(slots_p, sp_pend, tor_pend)
    codes = [f['code'] for f in res['failures']]
    check('T3', 'the r5 text-of-record pin still PENDING is a gap, and the other layers are still reported (BUILD_V007_PENDING too)',
          res['verdict'] == 'REFUSE' and 'TEXT_OF_RECORD_PIN_PENDING' in codes and 'BUILD_V007_PENDING' in codes, repr(codes), tag='PORT', r2=92)
    p2, sp2 = cert_variant('d08', 'DOUBLING', lambda d: d.update(ddo_gas_M_s=64))
    s3 = json.loads(p2.read_bytes())
    s3['producer_registry'] = {'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}
    p3 = xw(run / 'slots_d08.json', s3)
    res = T3run(p3, sealed_prereg_for(s3, TOR, 'prereg_d08.json'), TOR)
    codes = [f['code'] for f in res['failures']]
    check('T3', 'D-08: a pin gap no longer hides the certificate layer (PIN_PENDING and CERTIFICATE_M_S together)',
          'PIN_PENDING' in codes and 'CERTIFICATE_M_S' in codes, repr(codes), tag='PORT', r2=93)
    tor_x = text_of_record('variant_tor_unknown_slot.json', mutate=lambda d: d['seal_slots'].update(extra_slot={'value': 'x', 'rule': 'synthetic'}))
    record('T3', 'an unknown prereg seal slot', T3run(slots_p, sealed_prereg_for(slots, tor_x, 'variant_sealed_unknown_slot.json'), tor_x), False, 'PREREG_SLOT_UNKNOWN',
           tag='PORT', r2=94)
    p2, sp2 = variant('realr12', lambda s: s.update(compare_reviewed_source=pin(R12)))
    record('T3', 'REAL: the selected r12 4bd7b262 itself as the reviewed source', T3run(p2, sp2, TOR), True, tag='PORT', r2=95)
    p2, sp2 = variant('realr13', lambda s: s.update(compare_reviewed_source=pin(R13)))
    record('T3', 'REAL r13 (A104): the compare of record f5adfd11 itself as the reviewed source (its validate_case_block, activate_driver_build in-process)',
           T3run(p2, sp2, TOR), True, tag='NEW_CONTROL')
    s_lp = copy.deepcopy(slots)
    s_lp['launch_packet'] = 'PENDING_ROOT_AT_SEAL_ASSEMBLY'
    res = T3run(xw(run / 'slots_launch_packet_string.json', s_lp), sp, TOR)
    check('T3', 'D-07 class: a bare PENDING launch_packet slot refuses with codes, never an exception', res['verdict'] == 'REFUSE' and not any(
        f['code'].startswith('INTERNAL_EXCEPTION') for f in res['failures']) and any(f['code'] == 'SLOT_GROUP_KEYS' for f in res['failures']),
          repr([f['code'] for f in res['failures']]), tag='PORT', r2=96)
    record('T3', 'r13 (A104): genuine with tools 1 and 2, r13 f5adfd11 as the reviewed source and an r13-sealed compare', T3run(slots13_p, sp13, TOR, frozen=frozen,
           dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed13, sealed_compare=sc13), True, tag='NEW_CONTROL')
    # ---- tool 3, v003 D-05 (NEW)
    r_ = T3run(slots_p, sp, TOR, frozen=frozen, covered_later=COV, dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=sc)
    check('T3', 'D-05: a bare name via the API refuses in tool 3 itself and in tool 1 (COVERED_LATER_BARE_NAMES_REFUSED, T1:COVERED_LATER_BARE_NAMES_REFUSED)',
          r_['verdict'] == 'REFUSE' and {'COVERED_LATER_BARE_NAMES_REFUSED', 'T1:COVERED_LATER_BARE_NAMES_REFUSED'} <= {f['code'] for f in r_['failures']},
          repr([f['code'] for f in r_['failures']]))
    record('T3', 'D-05: a bare name via the API without --frozen still refuses in tool 3', T3run(slots_p, sp, TOR, covered_later=COV), False, 'COVERED_LATER_BARE_NAMES_REFUSED')
    rc, so, se = cli(T3.main, ['--slots', str(slots_p), '--prereg', str(sp), '--text-of-record', str(TOR), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s,
                               '--covered-later', COV[0]])
    check('T3', 'D-05: a bare name via the CLI exits 2 with COVERED_LATER_BARE_NAMES_REFUSED', rc == 2 and jcodes(so) == ['COVERED_LATER_BARE_NAMES_REFUSED'],
          'rc %r codes %r' % (rc, jcodes(so)))
    record('T3', 'D-05: a dispositions pin without --frozen (tool 1 cannot verify it)', T3run(slots_p, sp, TOR, dispositions=D0), False, 'DISPOSITIONS_WITHOUT_FROZEN')
    record('T3', '0640: a read copy without --frozen', T3run(slots_p, sp, TOR, text_of_record_addendum=RC0s), False, 'ADDENDUM_AT_TEXT_OF_RECORD_WITHOUT_FROZEN')
    record('T3', 'D-05: --frozen without a dispositions file while A<NMAX> is a later entry', T3run(slots_p, sp, TOR, frozen=frozen, text_of_record_addendum=RC0s), False,
           'T1:DISPOSITIONS_REQUIRED')
    record('T3', '0640: --frozen without the read copy', T3run(slots_p, sp, TOR, frozen=frozen, dispositions=D0), False, 'T1:ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED')
    record('T3', '0640: a read copy that is not the prereg\'s pin, through tool 3', T3run(slots_p, sp, TOR, frozen=frozen, dispositions=D0,
           text_of_record_addendum=str(frozen)), False, 'T1:ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH')
    record('T3', 'D-05: a dispositions pin whose sha is not the bytes, through tool 3', T3run(slots_p, sp, TOR, frozen=frozen, dispositions=(D0[0], '0' * 64),
           text_of_record_addendum=RC0s), False, 'T1:DISPOSITIONS_PIN_MISMATCH')
    r_ = T3run(slots_p, sp, TOR, frozen=frozen, dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=sc)
    pt_ = r_.get('passthrough') or {}
    check('T3', 'D-05 control: tool 3 passes tool 1\'s verified result through (dispositions pin, content, exact text; required entries; read copy pin)',
          r_['verdict'] == 'PASS' and pt_.get('later_entry_dispositions') == {'pin': {'path': D0[0], 'sha256': D0[1]}, 'content': json.loads(D0_TEXT), 'raw_text': D0_TEXT}
          and pt_.get('dispositions_required') == COV and 'covered_later' not in pt_ and pt_.get('addendum_at_text_of_record') == {'path': RC0s, 'sha256': C.sha(RC0)},
          repr([f['code'] for f in r_['failures']]), tag='NEW_CONTROL')
    use(TOR)
    rc, so, se = cli(T3.main, ['--slots', str(slots_p), '--prereg', str(sp), '--text-of-record', str(TOR), '--frozen', str(frozen), '--addendum-at-text-of-record', RC0s,
                               '--dispositions', D0[0], '--dispositions-sha', D0[1], '--reviewed', str(reviewed), '--sealed-compare', str(sc)])
    check('T3', 'D-05 control: the tool 3 CLI with --addendum-at-text-of-record, --dispositions and --dispositions-sha passes (exit 0)', rc == 0
          and jget(so, 'verdict') == 'PASS', 'rc %r codes %r' % (rc, jcodes(so)), tag='NEW_CONTROL')
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

    def args_for(sl_p, sp_p, tor, sc_p, **over):
        sh = C.sha(sc_p)
        a = A()
        a.slots, a.prereg, a.text_of_record, a.frozen, a.dispositions = str(sl_p), str(sp_p), str(tor), str(frozen), D0
        a.addendum_at_text_of_record = RC0s
        a.reviewed, a.sealed_compare = str(reviewed), str(sc_p)
        a.gates_only_output = str(body_file(gates_body(sh)))
        a.validity_only_output = str(body_file(validity_body(sh), 'VALIDITY_ONLY.json'))
        a.key_equivalence_map, a.new_item_list, a.successor_custody, a.b2_record = str(kmap), str(newl), str(cust), str(B2_REC)
        a.__dict__.update(over)
        return a

    def full_set(name, s2, tor, src=None):
        sl_p = xw(run / ('slots_%s.json' % name), s2)
        sp2 = sealed_prereg_for(s2, tor, 'prereg_%s.json' % name)
        return sl_p, sp2, sealed_compare_for(s2, sp2, 'sealed_compare_%s.py' % name, src=src)
    a = args_for(slots_p, sp, TOR, sc)
    before = sorted(str(p) for p in run.rglob('*'))
    res, text = T4.safe_build(a)
    after = sorted(str(p) for p in run.rglob('*'))
    rec = json.loads(text) if text else {}
    shape_ok = all(isinstance(rec.get(k), dict) and set(rec[k]) == {'path', 'sha256'} for k in ('prereg', 'compare', 'driver', 'frozen_addendum', 'case_block', 'build',
                                                                                              'cascade_map_r5_addendum', 'text_of_record', 'addendum_at_text_of_record'))
    b2dis = json.loads(B2_REC.read_bytes())['disclosure']
    LED0 = {'pin': {'path': D0[0], 'sha256': D0[1]}, 'content': json.loads(D0_TEXT), 'raw_text': D0_TEXT}
    content_ok = (rec.get('sealed_by') == C.AUTHORITY and rec.get('prereg') == {'path': str(sp.resolve()), 'sha256': C.sha(sp)}
                  and rec.get('compare') == {'path': str(sc.resolve()), 'sha256': C.sha(sc)} and rec.get('driver') == plan['driver']
                  and rec.get('frozen_addendum') == plan['frozen_addendum'] and rec.get('case_block') == pin(cbf) and rec.get('build') == pin(b7)
                  and rec.get('admission_allowlist') == {p: h for h, p in allow6} and rec.get('launch_entry') == {'launcher': plan['launcher'], 'guard': plan['guard']}
                  and rec.get('key_equivalence_map_quoted') == KEYMAP and rec.get('entry_table', {}).get('key') == 'entries_after_A81'
                  and len((rec.get('entry_table', {}).get('table') or {}).get('rows', [])) == NMAX - 82
                  and rec.get('later_entry_dispositions') == LED0 and 'no_change_notes' not in rec and rec.get('schema') == 'UNT_V007_SEAL_RECORD_C4V003'
                  and rec.get('addendum_at_text_of_record') == {'path': RC0s, 'sha256': C.sha(RC0)}
                  and rec.get('ddo_gas_M_s_registered') == 128 and rec.get('route_a_mode') == 'parallel8' and 'sealed_status_authority' in rec
                  and isinstance(rec.get('pending_strings_outside_slot_values'), list) and rec.get('text_of_record') == {'path': str(TOR), 'sha256': C.sha(TOR)}
                  and rec.get('b2_disclosure', {}).get('record') == pin(B2_REC) and rec.get('b2_disclosure', {}).get('disclosure') == b2dis
                  and rec.get('b2_disclosure', {}).get('requirement') == B2_TEXT and any(t.startswith('Disclosure E5-08') for t in rec.get('disclosures', [])))
    results.append({'tool': 'T4', 'tag': 'PORT_CHANGED', 'r2': 97, 'case': 'genuine: record built, nothing written, guard-shaped pins, pass-through fields, B2 disclosure '
                    '(real C3V003), later_entry_dispositions = {pin, content, raw_text} in place of the generic no_change_notes, and the read copy\'s pin '
                    '(schema C4V003)',
                    'why': WHY_BASE + '; the record carries later_entry_dispositions (exact pin, content and text) instead of no_change_notes and '
                           'addendum_at_text_of_record, schema UNT_V007_SEAL_RECORD_C4V003',
                    'expect': 'PASS', 'verdict': res['verdict'], 'codes': [f['code'] for f in res['failures']], 'notes': [],
                    'ok': res['verdict'] == 'PASS' and text is not None and before == after and shape_ok and content_ok})

    def t4(name, expect_code, tag='PORT_CHANGED', base=None, r2=None, why=WHY_BASE, **over):
        b = A()
        b.__dict__.update((base or a).__dict__)
        b.__dict__.update(over)
        r, t = T4.safe_build(b)
        results.append({'tool': 'T4', 'tag': tag, 'r2': r2, 'why': why if tag == 'PORT_CHANGED' else None, 'case': name, 'expect': 'REFUSE ' + expect_code,
                        'verdict': r['verdict'], 'codes': [f['code'] for f in r['failures']], 'notes': [],
                        'ok': t is None and r['verdict'] == 'REFUSE' and any(expect_code in f['code'] for f in r['failures'])})
        return r
    sh0 = C.sha(sc)
    t4('E-SEAL1 output with a decimal row-like value', 'E_SEAL1_OUTPUT_MAY_SHOW_A_ROW_VALUE', r2=98,
       gates_only_output=str(body_file(gates_body(sh0, statement='GATES: row 03 speed 45.1234 km/s'))))
    p2, sp2 = variant('t4pending', lambda s: s.update(producer_registry={'path': str(preg), 'sha256': 'PENDING_ROOT_AT_SEAL_ASSEMBLY'}))
    t4('any slot-fill refusal produces no record', 'T3:', r2=99, slots=str(p2), prereg=str(sp2))
    a_ok = args_for(slots_p, sp, TOR, sc, gates_only_output=str(body_file(gates_body(sh0, mt_crosscheck='LO shells at most 0.005; GQ max over P0 at most 1e-12'))))
    r_ok, t_ok = T4.safe_build(a_ok)
    check('T4', 'R-04: the compare\'s own allowed constants (0.005, 1e-12) in a blinded body are not taken for row values', r_ok['verdict'] == 'PASS' and t_ok is not None,
          repr([f['code'] for f in r_ok['failures']]), tag='PORT_CHANGED', r2=100, why=WHY_BASE)
    t4('R-04: a B6 body with test_mode true', 'E_SEAL1_TEST_MODE', r2=101, gates_only_output=str(body_file(gates_body(sh0, test_mode=True))))
    t4('R-04: a B6 body from another script (the reviewed source)', 'E_SEAL1_SCRIPT_NOT_THE_SEALED_COMPARE', r2=102, gates_only_output=str(body_file(gates_body(R12_SHA))))
    t4('R-04: the validity body given as the gates output', 'E_SEAL1_SCHEMA', r2=103, gates_only_output=str(body_file(validity_body(sh0), 'GATES_ONLY.json')))
    t4('R-04: a B6 body that is not blinded', 'E_SEAL1_NOT_BLINDED', r2=104, gates_only_output=str(body_file(gates_body(sh0, blinded=False))))
    t4('R-04: a B6 body carrying a JSON number', 'E_SEAL1_OUTPUT_VALUE_BEARING', r2=105, gates_only_output=str(body_file(gates_body(sh0, rows_read=12))))
    t4('R-04: a B6 body with a number glued to letters (x61.2222222)', 'E_SEAL1_OUTPUT_VALUE_BEARING', r2=106,
       gates_only_output=str(body_file(gates_body(sh0, statement='codes x61.2222222'))))
    t4('R-04: the validity body on cases other than C5H', 'E_SEAL1_VALIDITY_CASES_NOT_C5H', r2=107,
       validity_only_output=str(body_file(validity_body(sh0, cases={'C4T': {'label': 'C4T'}}), 'VALIDITY_ONLY.json')))
    t4('R-04: a B6 file that is not the compare\'s GATES_ONLY.json', 'E_SEAL1_OUTPUT_NAME', r2=108, gates_only_output=str(body_file(gates_body(sh0), 'gates.txt')))
    t4('R-04: a B6 body with another route-A mode', 'E_SEAL1_ROUTE_A_MODE', r2=109, gates_only_output=str(body_file(gates_body(sh0, route_a_mode='serial_with_exemption'))))
    t4('R-04 / v001 regression: a schemaless B7 key map ({"map": []} passed v001)', 'KEY_MAP_SCHEMA', r2=110,
       key_equivalence_map=str(xw(run / 'KEYMAP_V001_FORM.json', {'map': []})))
    t4('R-10: the SEAL_RECORD key map differs from the case block\'s', 'KEY_MAP_NOT_THE_CASE_BLOCK_MAP', r2=111,
       key_equivalence_map=str(xw(run / 'KEYMAP_EMPTY.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': []})))
    t4('B7: a key map mapping one pointer twice', 'KEY_MAP_DUPLICATE_POINTER', r2=112,
       key_equivalence_map=str(xw(run / 'KEYMAP_DUP.json', {'schema': T4.KEY_MAP_SCHEMA, 'key_equivalence_map': KEYMAP + KEYMAP})))
    impl_other = xw(run / 'IMPL_NOT_NAMING_THE_SOURCE.md', '# a compare IMPL that names no reviewed source sha\n')
    t4('B7: a NEW-item list taken from an IMPL that does not name the reviewed source', 'NEW_ITEMS_IMPL_NOT_THE_REVIEWED_SOURCE', r2=113,
       new_item_list=str(xw(run / 'NEW_ITEMS_OTHER_IMPL.json', dict(json.loads(newl.read_bytes()), compare_impl=pin(impl_other)))))
    t4('B7: an ADOPTED NEW item without MUST_FAIL tests', 'NEW_ITEMS_ADOPTED_WITHOUT_MUST_FAIL', r2=114,
       new_item_list=str(xw(run / 'NEW_ITEMS_NO_MUSTFAIL.json', dict(json.loads(newl.read_bytes()), items=[{'id': 'NEW-71', 'disposition': 'ADOPTED', 'reason': 'x', 'must_fail_tests': []}]))))
    t4('B7: one NEW id twice', 'NEW_ITEMS_DUPLICATE_ID', r2=115,
       new_item_list=str(xw(run / 'NEW_ITEMS_DUP.json', dict(json.loads(newl.read_bytes()), items=json.loads(newl.read_bytes())['items'] * 2))))
    t4('B7: raw successor custody of a run on another driver', 'CUSTODY_DRIVER_NOT_THE_SLOT', r2=116,
       successor_custody=str(xw(run / 'CUSTODY_OTHER_DRIVER.json', dict(json.loads(cust.read_bytes()), driver_sha256='4' * 64))))
    t4('B7: raw successor custody with a stage on its base script', 'CUSTODY_STAGES', r2=117,
       successor_custody=str(xw(run / 'CUSTODY_STAGES.json', dict(json.loads(cust.read_bytes()), stages_successor=20))))
    # ---- A100 B2 disclosure
    t4('A100: the prereg asks for the B2 disclosure block and no --b2-record is given', 'B2_DISCLOSURE_REQUIRED', r2=118, b2_record=None)
    s_v7 = copy.deepcopy(slots)
    s_v7['producer_registry'] = pin(REGISTRY_V007)
    sl7, sp7, sc7 = full_set('registry_v007', s_v7, TOR)
    t4('A100: a B2 record that is not the registry\'s B2 record of record (registry C3V007 names d4b41ffc)', 'B2_RECORD_NOT_REGISTERED', r2=119, base=args_for(sl7, sp7, TOR, sc7))
    t4('A100: the superseded B2 C3V002 record (FAIL, no disclosure block)', 'B2_RECORD_NOT_PASS', r2=120, base=args_for(sl7, sp7, TOR, sc7), b2_record=str(B2_REC_V002))
    # ---- A99.3 / 0640 changed-section disposition in the SEAL_RECORD (frozen copy with A90 edited; plan bound to it)
    # the reviewed r12 hashes the open V005 path (ADDENDUM_V005_CITED), which root stops writing at the freeze, so tool 2 needs the frozen
    # copy to equal the open file; this one test uses a SYNTHETIC copy of r12 whose ADDENDUM_V005_CITED names the A90-edited frozen variant
    # (that one line changed; its IMPL stand-in names the copy's sha)
    rv90 = R12.read_bytes().decode('utf-8').splitlines(keepends=True)
    i_cited = [i for i, l in enumerate(rv90) if l.startswith('ADDENDUM_V005_CITED = ')]
    assert len(i_cited) == 1
    rv90[i_cited[0]] = 'ADDENDUM_V005_CITED = %r   # SYNTHETIC test copy: the A90-edited frozen variant (r12 cites the open V005 path)\n' % str(f_90)
    reviewed90 = xw(run / 'reviewed_compare_r12_copy_citing_the_A90_variant.py', ''.join(rv90))
    impl90 = xw(run / 'IMPL_STANDIN_FOR_THE_A90_VARIANT_COPY_SYNTH.md', '# SYNTHETIC IMPL stand-in (Claude4 seal tools v003 tests) for the test copy %s\n'
                % C.sha(reviewed90))
    newl90 = xw(run / 'NEW_ITEM_DISPOSITIONS_A90_VARIANT_SYNTH.json', dict(json.loads(newl.read_bytes()), compare_impl=pin(impl90)))
    s90 = copy.deepcopy(slots)
    s90['frozen_addendum'] = dict(plan90['frozen_addendum'])
    s90['launch_packet'] = {'build': pin(b7), 'bound_plan': rpin(plan_90p), 'bound_command': rpin(cmd_90p)}
    s90['compare_reviewed_source'] = rpin(reviewed90)
    slc, spc, scc = full_set('changed_A90', s90, tor_90, src=reviewed90)
    use(tor_90)
    a90_base = args_for(slc, spc, tor_90, scc, frozen=str(f_90), dispositions=D_90, reviewed=str(reviewed90), new_item_list=str(newl90))
    r_c, t_c = T4.safe_build(a90_base)
    led_c = (json.loads(t_c).get('later_entry_dispositions') if t_c else None) or {}
    rows_c = (led_c.get('content') or {}).get('entries') or []
    a90 = next((r for r in rows_c if r.get('entry') == 'A90'), {})
    check('T4', 'A99.3: a changed table row disposed by root is recorded in the SEAL_RECORD (its no_change_after_change row, exact text and pin)', r_c['verdict'] == 'PASS'
          and len(rows_c) == 2 and a90.get('disposition') == 'no_change_after_change' and a90.get('changed_text') == EDIT90[:40]
          and a90.get('section_sha256') == C.sha_bytes(T1.sections(f_90.read_bytes())[90][0][1])
          and led_c.get('raw_text') == Path(D_90[0]).read_bytes().decode('utf-8') and led_c.get('pin') == {'path': D_90[0], 'sha256': D_90[1]},
          repr([f['code'] for f in r_c['failures']]) + repr(led_c)[:200], tag='PORT_CHANGED', r2=121,
          why='D-05 (0640): the A90 note (two shas in prose) is now root\'s no_change_after_change row, carried with its exact text and pin; the change '
              'is made in a frozen copy the plan is bound to')
    r_ = t4('0640: plain no_change on a changed entry, through the builder', 'T3:T1:DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', tag='NEW', base=a90_base,
            dispositions=disp(f_90, later=COV + ['A90']))
    check('T4', '0640: ... and that is its only refusal (the A90 variant set is otherwise clean)', [f['code'] for f in r_['failures']]
          == ['T3:T1:DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY'], repr([f['code'] for f in r_['failures']]))
    use(TOR)
    # ---- tool 4, v003 D-05 (NEW)
    bb = A()
    bb.__dict__.update(a.__dict__)
    bb.covered_later = COV
    r_, t_ = T4.safe_build(bb)
    check('T4', 'D-05: a bare name via the API refuses in the builder itself, in tool 3 and in tool 1, and builds no record', t_ is None
          and {'COVERED_LATER_BARE_NAMES_REFUSED', 'T3:COVERED_LATER_BARE_NAMES_REFUSED', 'T3:T1:COVERED_LATER_BARE_NAMES_REFUSED'} <= {f['code'] for f in r_['failures']},
          repr([f['code'] for f in r_['failures']]))
    t4('D-05: no dispositions file while A<NMAX> is a later entry', 'T3:T1:DISPOSITIONS_REQUIRED', tag='NEW', dispositions=None)
    t4('D-05: a dispositions pin whose sha is not the bytes', 'T3:T1:DISPOSITIONS_PIN_MISMATCH', tag='NEW', dispositions=(D0[0], '0' * 64))
    t4('D-05: an empty reason in root\'s file', 'T3:T1:DISPOSITION_REASON_EMPTY', tag='NEW', dispositions=disp(frozen, later=COV,
                                                                                                         mutate=lambda o: o['entries'][0].update(reason='')))
    t4('0640: no read copy given to the builder', 'T3:T1:ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', tag='NEW', addendum_at_text_of_record=None)
    t4('0640: a read copy that is not the prereg\'s pin, through the builder', 'T3:T1:ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH', tag='NEW',
       addendum_at_text_of_record=str(frozen))
    t4_argv = ['--slots', str(slots_p), '--prereg', str(sp), '--text-of-record', str(TOR), '--frozen', str(frozen), '--reviewed', str(reviewed), '--sealed-compare', str(sc),
               '--gates-only-output', a.gates_only_output, '--validity-only-output', a.validity_only_output, '--key-equivalence-map', str(kmap),
               '--new-item-list', str(newl), '--successor-custody', str(cust), '--b2-record', str(B2_REC)]
    rc, so, se = cli(T4.main, t4_argv + ['--addendum-at-text-of-record', RC0s, '--dispositions', D0[0], '--dispositions-sha', D0[1], '--covered-later', COV[0]])
    check('T4', 'D-05: a bare name via the CLI exits 2, prints nothing on stdout (no record bytes) and the code on stderr', rc == 2 and so == ''
          and jcodes(se) == ['COVERED_LATER_BARE_NAMES_REFUSED'], 'rc %r stdout %r codes %r' % (rc, so[:80], jcodes(se)))
    rc, so, se = cli(T4.main, t4_argv + ['--addendum-at-text-of-record', RC0s, '--dispositions', D0[0], '--dispositions-sha', D0[1]])
    check('T4', 'D-05 control: the builder CLI with --addendum-at-text-of-record and --dispositions/--dispositions-sha prints the record whose sha stderr names',
          rc == 0 and so == text and jget(se, 'seal_record_sha256') == C.sha_bytes(so.encode('utf-8')), 'rc %r codes %r' % (rc, jcodes(se)), tag='NEW_CONTROL')
    rc, so, se = cli(T4.main, t4_argv + ['--dispositions', D0[0], '--dispositions-sha', D0[1]])
    check('T4', '0640: the builder CLI without --addendum-at-text-of-record exits 2 with no record bytes', rc == 2 and so == ''
          and 'T3:T1:ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED' in jcodes(se), 'rc %r codes %r' % (rc, jcodes(se)))
    D_mut = disp(frozen, later=COV, name='LATER_ENTRY_DISPOSITIONS_MUTATED_AFTER_CHECK.json')
    orig_t1_run = T1.run

    def t1_then_append(*args_, **kw_):
        r = orig_t1_run(*args_, **kw_)
        with open(D_mut[0], 'a') as f:                      # the file changes after tool 1 verified it (a work copy in the run folder)
            f.write(' ')
        return r

    def t1_wrong_verified_sha(*args_, **kw_):
        r = orig_t1_run(*args_, **kw_)
        if r.get('later_entry_dispositions'):
            r['later_entry_dispositions']['pin']['sha256'] = '1' * 64
        return r

    def t1_wrong_verified_text(*args_, **kw_):
        r = orig_t1_run(*args_, **kw_)
        if r.get('later_entry_dispositions'):
            r['later_entry_dispositions']['raw_text'] += ' '
        return r

    def a_with(**over):
        b = A()
        b.__dict__.update(a.__dict__)
        b.__dict__.update(over)
        return b
    for nm_, fn_, dd in (('its bytes change after tool 1 verified them', t1_then_append, D_mut),
                         ('tool 1\'s verified sha is not root\'s pin', t1_wrong_verified_sha, D0),
                         ('the text tool 1 verified is not the bytes re-read', t1_wrong_verified_text, D0)):
        T1.run = fn_
        try:
            r_, t_ = T4.safe_build(a_with(dispositions=dd))
        finally:
            T1.run = orig_t1_run
        results.append({'tool': 'T4', 'tag': 'NEW', 'r2': None, 'why': None, 'case': 'D-05: tool 4 re-reads the dispositions file: %s' % nm_,
                        'expect': 'REFUSE DISPOSITIONS_CHANGED_AFTER_CHECK', 'verdict': r_['verdict'], 'codes': [f['code'] for f in r_['failures']], 'notes': [],
                        'ok': t_ is None and r_['verdict'] == 'REFUSE' and [f['code'] for f in r_['failures']] == ['DISPOSITIONS_CHANGED_AFTER_CHECK']})
    rc_, tc_ = T4.safe_build(a_with())
    check('T4', 'D-05 control: with the unchanged file the same build passes after the re-read checks (patch removed)', rc_['verdict'] == 'PASS' and tc_ == text,
          repr([f['code'] for f in rc_['failures']]), tag='NEW_CONTROL')
    led_rec = rec.get('later_entry_dispositions') or {}
    check('T4', 'D-05 control: the SEAL_RECORD carries the dispositions file\'s exact content, raw text and pin (raw_text hashes to the pin)',
          led_rec == LED0 and C.sha_bytes(led_rec.get('raw_text', '').encode('utf-8')) == D0[1] and json.loads(led_rec.get('raw_text', 'null')) == led_rec.get('content'),
          repr(led_rec)[:200], tag='NEW_CONTROL')
    sl_thl, sp_thl2, sc_thl = full_set('table_has_later', slots, tor_thl)
    use(tor_thl)
    r_n, t_n = T4.safe_build(args_for(sl_thl, sp_thl2, tor_thl, sc_thl, dispositions=None, addendum_at_text_of_record=RCFs))
    check('T4', 'D-05 control: no later or changed entry and no file: the record carries later_entry_dispositions = NOT_SUPPLIED_NONE_REQUIRED',
          r_n['verdict'] == 'PASS' and t_n is not None and json.loads(t_n).get('later_entry_dispositions') == T4.DISPOSITIONS_NONE_REQUIRED,
          repr([f['code'] for f in r_n['failures']]), tag='NEW_CONTROL')
    use(TOR)
    # ---- tool 4 with r13 f5adfd11 (A104) as the reviewed source: a full build (its NEW-item list from the r13 IMPL 274f7049)
    newl13 = xw(run / 'NEW_ITEM_DISPOSITIONS_R13_SYNTH.json', {'schema': T4.NEW_ITEMS_SCHEMA, 'compare_impl': pin(R13_IMPL), 'items': [],
                                                              'note': 'SYNTHETIC test input: the r13 IMPL declares no NEW id'})
    r13b, t13b = T4.safe_build(args_for(slots13_p, sp13, TOR, sc13, reviewed=str(reviewed13), new_item_list=str(newl13)))
    rec13 = json.loads(t13b) if t13b else {}
    check('T4', 'r13 (A104): the builder makes a SEAL_RECORD with r13 f5adfd11 as the reviewed source and an r13-sealed compare', r13b['verdict'] == 'PASS'
          and rec13.get('compare_reviewed_source') == rpin(reviewed13) and rec13.get('compare') == {'path': str(sc13.resolve()), 'sha256': C.sha(sc13)},
          repr([f['code'] for f in r13b['failures']]), tag='NEW_CONTROL')
    # ---- admission-config check (B8). If the genuine build refused (a mutant), this case fails and the cases below run on an empty record,
    # so the suite still completes and writes its results.
    check('T4', 'the genuine SEAL_RECORD was built, so the admission-config, B8 and integration cases below use a real record', text is not None and bool(rec),
          repr([f['code'] for f in res['failures']])[:300], tag='NEW_CONTROL')
    if text is None:
        rec, text = {'driver': {}, 'frozen_addendum': {}, 'sealed_by': {}, 'admission_allowlist': {}}, '{}\n'
    seal_p = xw(run / 'SEAL_RECORD_SYNTH.json', text)
    cfg = {'schema': C.ADMISSION_SCHEMA, 'authority': dict(C.AUTHORITY), 'seal': pin(seal_p), 'prereg': rec.get('prereg'), 'compare': rec.get('compare'),
           'build': rec.get('build'), 'producer_allowlist': rec.get('admission_allowlist')}
    cfg_p = xw(run / 'ROOT_SEAL_ADMISSION_SYNTH.json', cfg)
    record('T4', 'admission config: genuine (pins this SEAL_RECORD, BUILD_V007, the 15-source allowlist)', T4.check_admission_config(cfg_p, seal_p), True, tag='PORT', r2=122)
    allow5 = {p: h for h, p in C.build_allowlist((PKT / 'BUILD_V005.md').read_bytes().decode('utf-8'))}
    for name, over, code, idx in (('a V006 build pin', {'build': pin(BUILD_V006)}, 'ADMISSION_CONFIG_BUILD_NOT_BUILD_V007', 123),
                                  ('the 13-source BUILD_V005 allowlist', {'producer_allowlist': allow5}, 'ADMISSION_ALLOWLIST_COUNT_NOT_15', 124),
                                  ('the guard missing from the allowlist', {'producer_allowlist': {p: h for p, h in rec['admission_allowlist'].items() if p != plan['guard']['path']}},
                                   'ADMISSION_CONFIG_GUARD_NOT_NAMED_EXACTLY', 125),
                                  ('another SEAL_RECORD pinned', {'seal': pin(kmap)}, 'ADMISSION_CONFIG_SEAL_NOT_THE_RECORD', 126),
                                  ('an extra key', {'extra': 1}, 'ADMISSION_CONFIG_KEYS', 127)):
        cp = xw(run / ('ROOT_SEAL_ADMISSION_%s.json' % re.sub(r'\W+', '_', name)), dict(cfg, **over))
        record('T4', 'admission config: %s' % name, T4.check_admission_config(cp, seal_p), False, code, tag='PORT', r2=idx)
    # ---- B8 (0634; Codex3 0639): Codex3's six seal-record mutations, each re-pinned by its config, plus four more of the same class
    B8_CASES = (('wrong_sealed_by', lambda x: x.update(sealed_by={'identity': 'wrong'}), 'ADMISSION_SEAL_SEALED_BY_NOT_AUTHORITY', 'STRUCTURED_ROOT_SEAL_AUTHORITY_REQUIRED', True),
                ('missing_sealed_by', lambda x: x.pop('sealed_by'), 'ADMISSION_SEAL_SEALED_BY_NOT_AUTHORITY', 'STRUCTURED_ROOT_SEAL_AUTHORITY_REQUIRED', True),
                ('malformed_driver', lambda x: x.update(driver='PENDING'), 'ADMISSION_SEAL_DRIVER_PIN', 'ROOT_ADMISSION_PIN_MISMATCH', True),
                ('stale_driver', lambda x: x['driver'].update(sha256='0' * 64), 'ADMISSION_SEAL_DRIVER_PIN', 'ROOT_ADMISSION_PIN_MISMATCH', True),
                ('malformed_frozen', lambda x: x.update(frozen_addendum=[]), 'ADMISSION_SEAL_FROZEN_ADDENDUM_PIN', 'ROOT_ADMISSION_PIN_MISMATCH', True),
                ('stale_frozen', lambda x: x['frozen_addendum'].update(sha256='0' * 64), 'ADMISSION_SEAL_FROZEN_ADDENDUM_PIN', 'ROOT_ADMISSION_PIN_MISMATCH', True),
                ('missing_driver', lambda x: x.pop('driver'), 'ADMISSION_SEAL_DRIVER_REQUIRED', 'SEALED_DRIVER_REQUIRED', False),
                ('missing_frozen_addendum', lambda x: x.pop('frozen_addendum'), 'ADMISSION_SEAL_FROZEN_ADDENDUM_REQUIRED', 'SEALED_FROZEN_ADDENDUM_REQUIRED', False),
                ('sealed_by_extra_key', lambda x: x['sealed_by'].update(note='x'), 'ADMISSION_SEAL_SEALED_BY_NOT_AUTHORITY', 'STRUCTURED_ROOT_SEAL_AUTHORITY_REQUIRED', False),
                ('driver_pin_extra_key', lambda x: x['driver'].update(note='x'), 'ADMISSION_SEAL_DRIVER_PIN', 'ROOT_ADMISSION_PIN_MISMATCH', False))
    b8_files = {}
    for name, mut, code, gcode, cx3 in B8_CASES:
        q = copy.deepcopy(rec)
        mut(q)
        sp_b8 = xw(run / 'b8' / name / 'SEAL_RECORD_B8_SYNTH.json', json.dumps(q, indent=1, sort_keys=True) + '\n')
        cp_b8 = xw(run / 'b8' / name / 'ROOT_SEAL_ADMISSION_B8_SYNTH.json', dict(cfg, seal=pin(sp_b8)))
        b8_files[name] = (sp_b8, cp_b8, gcode)
        r_ = T4.check_admission_config(cp_b8, sp_b8)
        record('T4', 'B8%s: %s (the config re-pins the altered record) refuses %s' % (' (Codex3 0639)' if cx3 else '', name, code), r_, False, code)
    # ---- tool 5 MUST_FAIL
    r5bad, t5bad = T5.record_bytes(str(R12), R12_SHA, str(CERTS['LO']))
    record('T5', 'tool 5: a check record that is not a check of the r5 build (the LO certificate)', r5bad, False, 'DRIVER_BUILD_NOT_ADMISSIBLE', tag='PORT', r2=128)
    check('T5', 'tool 5: the printed bytes are the driver BUILD record fixture the slots pin', r5text == dbr.read_bytes().decode('utf-8') and t5bad is None, 'mismatch',
          tag='PORT', r2=129)
    # ---- tool 5 with r13 f5adfd11 (A104)
    r513, t513 = T5.record_bytes(str(R13), R13_SHA, str(CHECK_MD))
    record('T5', 'r13 (A104): tool 5 prints an admissible r5 driver BUILD record from r13 f5adfd11 with the real CHECK.md', r513, True, tag='NEW_CONTROL')
    check('T5', 'r13 (A104): the r13-printed record bytes equal the r12-printed ones (one driver BUILD record of record for either reviewed source)',
          t513 is not None and t513 == r5text, 'r13 %s, r12 %s' % (C.sha_bytes((t513 or '').encode('utf-8'))[:8], C.sha_bytes(r5text.encode('utf-8'))[:8]), tag='NEW_CONTROL')
    r513b, t513b = T5.record_bytes(str(R13), R13_SHA, str(CERTS['LO']))
    record('T5', 'r13 (A104): tool 5 refuses a check record that is not a check of the r5 build', r513b, False, 'DRIVER_BUILD_NOT_ADMISSIBLE')
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
    results.append({'tool': 'integration', 'tag': 'PORT', 'r2': 130, 'why': None, 'case': 'real guard v008 admits the v003 SEAL_RECORD (via the checked config); real launcher '
                    'v007 validate() accepts the bound plan', 'expect': 'PASS', 'verdict': 'PASS' if (o_adm == 'ok' and o_val == 'ok') else 'REFUSE', 'codes': [o_adm, o_val],
                    'notes': [], 'ok': o_adm == 'ok' and o_val == 'ok'})
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
    results.append({'tool': 'integration', 'tag': 'PORT', 'r2': 131, 'why': None, 'case': 'a SEAL_RECORD naming another driver is refused by launcher v007',
                    'expect': 'REFUSE PLAN_SEALED_DRIVER_MISMATCH', 'verdict': 'REFUSE' if o3 != 'accepted' else 'PASS', 'codes': [o3], 'notes': [],
                    'ok': 'PLAN_SEALED_DRIVER_MISMATCH' in o3})
    # ---- B8 under the REAL guard v008 admission() (validate not called; nothing is started): the guard refuses each B8 record too
    for name, (sp_b8, cp_b8, gcode) in b8_files.items():
        G.CONFIG = cp_b8
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cp_b8)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            og = 'admitted'
        except BaseException as e:
            og = '%s: %s' % (type(e).__name__, e)
        results.append({'tool': 'integration', 'tag': 'NEW', 'r2': None, 'why': None, 'case': 'B8: the real guard v008 admission() refuses the %s record (%s)' % (name, gcode),
                        'expect': 'REFUSE ' + gcode, 'verdict': 'REFUSE' if og != 'admitted' else 'PASS', 'codes': [og], 'notes': [], 'ok': gcode in og})
    G.CONFIG = cfg_p
    os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfg_p)
    try:
        G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
        og = 'ok'
    except BaseException as e:
        og = '%s: %s' % (type(e).__name__, e)
    r_ = T4.check_admission_config(cfg_p, seal_p)
    check('integration', 'B8 control: the genuine v003 record and its config still pass the v003 admission check and the real guard v008 admission()',
          r_['verdict'] == 'PASS' and og == 'ok' and {'seal.driver', 'seal.frozen_addendum'} <= set(r_['pins_verified']), repr([f['code'] for f in r_['failures']]) + og,
          tag='NEW_CONTROL')
    # ================= REAL BUILD_V007 94bc05a5: tool 3, the builder, the admission check and the guard's admission (no launcher validate)
    name_v011 = lambda d: d['seal_slots']['launch_packet']['named_candidates_verified_from_bytes'].update(template_plan=pin(TEMPLATE_V011))
    torR = text_of_record('KMAX_TAIL_PREREG_V007_R5_STANDIN_REAL_BUILD_V007_C4ST2.json', build_path=BUILD_V007, mutate=name_v011)
    sR = copy.deepcopy(slots)
    sR['launch_packet'] = {'build': pin(BUILD_V007), 'bound_plan': rpin(plan_r), 'bound_command': rpin(cmd_r)}
    sR['admission_entry'] = {'launcher': dict(planR['launcher']), 'guard': dict(planR['guard'])}
    slR, spR, scR = full_set('real_build_v007', sR, torR)
    record('T3', 'REAL BUILD_V007 94bc05a5 (15 sources from bytes) with a plan bound by the real binder from its own template V011 1b406591',
           T3run(slR, spR, torR, frozen=frozen, dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=scR), True, tag='PORT_CHANGED', r2=132,
           why=WHY_DISP_RC)
    rR, tR = T4.safe_build(args_for(slR, spR, torR, scR))
    recR = json.loads(tR) if tR else {}
    allow7 = {p: h for h, p in C.build_allowlist(BUILD_V007.read_bytes().decode('utf-8'))}
    check('T4', 'REAL BUILD_V007: the SEAL_RECORD pins it and carries its exact 15-source allowlist', rR['verdict'] == 'PASS' and recR.get('build') == pin(BUILD_V007)
          and recR.get('admission_allowlist') == allow7 and len(allow7) == 15, repr([f['code'] for f in rR['failures']]), tag='PORT_CHANGED', r2=133, why=WHY_BASE)
    if tR:
        sealR = xw(run / 'SEAL_RECORD_REAL_BUILD_V007_SYNTH.json', tR)
        cfgR_obj = {'schema': C.ADMISSION_SCHEMA, 'authority': dict(C.AUTHORITY), 'seal': pin(sealR), 'prereg': recR['prereg'], 'compare': recR['compare'],
                    'build': recR['build'], 'producer_allowlist': recR['admission_allowlist']}
        cfgR = xw(run / 'ROOT_SEAL_ADMISSION_REAL_BUILD_V007_SYNTH.json', cfgR_obj)
        record('T4', 'REAL BUILD_V007: the admission-config check passes on its 15 sources (V6-S3)', T4.check_admission_config(cfgR, sealR), True, tag='PORT', r2=134)
        G.CONFIG = cfgR
        os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cfgR)
        try:
            G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
            oR = 'ok'
        except BaseException as e:
            oR = '%s: %s' % (type(e).__name__, e)
        results.append({'tool': 'integration', 'tag': 'PORT', 'r2': 135, 'why': None, 'case': 'REAL BUILD_V007: the real guard v008 admission() accepts the config built from the '
                        'v003 SEAL_RECORD', 'expect': 'PASS', 'verdict': 'PASS' if oR == 'ok' else 'REFUSE', 'codes': [oR], 'notes': [], 'ok': oR == 'ok'})
        # ---- W7-S1 (Claude4 0108; A105): the guard matches its allowlist by substring, so these two configs pass the guard; the B8 check refuses both
        b7text = BUILD_V007.read_bytes().decode('utf-8')
        olds = [(h, p) for h, p in re.findall(r'^([0-9a-f]{64})  (/\S+\.py)$', b7text, re.M) if h[:8] in OLD_WRITER_PREFIXES]
        assert len(olds) == 2 and all(C.sha(p) == h and p not in allow7 for h, p in olds), olds
        w7 = {'17_rows_with_superseded_writers': dict(allow7, **{p: h for h, p in olds}), 'BUILD_V006_15_rows': {p: h for h, p in allow6}}
        assert len(w7['17_rows_with_superseded_writers']) == 17 and len(w7['BUILD_V006_15_rows']) == 15
        for wn, wa in w7.items():
            cw = xw(run / 'w7s1' / wn / 'ROOT_SEAL_ADMISSION_W7S1_SYNTH.json', dict(cfgR_obj, producer_allowlist=wa))
            record('T4', 'W7-S1 (B8): an admission config with %s refuses (%s)' % (wn.replace('_', ' '), 'ADMISSION_ALLOWLIST_NOT_THE_SEAL_RECORD_ALLOWLIST'),
                   T4.check_admission_config(cw, sealR), False, 'ADMISSION_ALLOWLIST_NOT_THE_SEAL_RECORD_ALLOWLIST')
            G.CONFIG = cw
            os.environ['UNT_ROOT_ADMISSION_SHA256'] = C.sha(cw)
            try:
                G.admission(str(PKT / 'route_a_token_launcher_cx1v007.py'))
                ow = 'admitted'
            except BaseException as e:
                ow = '%s: %s' % (type(e).__name__, e)
            results.append({'tool': 'integration', 'tag': 'REPRO', 'r2': None, 'why': None, 'case': 'W7-S1 reproduction: the real guard v008 admission() admits the %s '
                            'config (substring allowlist match, 0108); only the B8 check refuses it' % wn.replace('_', ' '), 'expect': 'ADMITTED',
                            'verdict': 'PASS' if ow == 'admitted' else 'REFUSE', 'codes': [ow], 'notes': [], 'ok': ow == 'admitted'})
        r_ = T4.check_admission_config(xw(run / 'w7s1' / 'ROOT_SEAL_ADMISSION_17_ROWS_CODES.json', dict(cfgR_obj, producer_allowlist=w7['17_rows_with_superseded_writers'])), sealR)
        check('T4', 'W7-S1 (B8): the 17-row config also refuses ADMISSION_ALLOWLIST_COUNT_NOT_15 and ADMISSION_ALLOWLIST_NOT_THE_BUILD_ALLOWLIST',
              {'ADMISSION_ALLOWLIST_COUNT_NOT_15', 'ADMISSION_ALLOWLIST_NOT_THE_BUILD_ALLOWLIST'} <= {f['code'] for f in r_['failures']}, repr([f['code'] for f in r_['failures']]))
    tor_t = text_of_record('variant_tor_names_v011_template.json', mutate=name_v011)
    record('T3', 'the bound plan is not bound from the template the prereg names (the r5 text names V011; the plan used the test template)',
           T3run(slots_p, sealed_prereg_for(slots, tor_t, 'variant_sealed_names_v011_template.json'), tor_t), False, 'PLAN_TEMPLATE_NOT_THE_PREREG_NAMED_TEMPLATE',
           tag='PORT', r2=136)
    # ================= REAL prereg r5 3245899f (landed, FROM_CLAUDE4/0103; not yet ruled the text of record) with its pinned read copy 70a48f51
    d5 = json.loads(R5.read_bytes())
    last5 = max(int(n) for a_, b_ in re.findall(r'A(\d{1,3})-A(\d{1,3})', d5['cites_by_name'][0]) for n in (a_, b_))
    cov5 = ['A%d' % n for n in heads if n > last5]
    R5_READs = str(R5_READ)
    D5 = disp(frozen, later=cov5, name='LATER_ENTRY_DISPOSITIONS_R5_SYNTH_C4V003.json')
    record('T1', 'REAL prereg r5 3245899f: tool 1 reads its 20 entries_after_A81 rows, each re-hashes from the frozen bytes, entries after A%d (%s) have rows in a '
           'dispositions file (dry-run flag only for path_to_be, the CLAUDE2 path root writes at the freeze)' % (last5, ', '.join(cov5)),
           T1.run(R5, frozen, None, (), True, D5, R5_READs), True, note='DRY_RUN_FROZEN_PATH_NOT_PATH_TO_BE', tag='PORT_CHANGED', r2=137,
           why='D-05: the later entries are covered by a dispositions fixture written for them instead of covered_later; ' + WHY_RC)
    sl5, sp5, sc5 = full_set('prereg_r5_landed', sR, R5)
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    res5 = T3.run(sl5, sp5, R5, frozen=frozen, dispositions=D5, reviewed=reviewed, sealed_compare=sc5, text_of_record_sha=C.sha(R5), text_of_record_addendum=R5_READs)
    codes5 = sorted(set(f['code'] for f in res5['failures']))
    check('T3', 'REAL prereg r5 3245899f as the text of record, its sha stated by root (case block %s validated in-process, real BUILD_V007, V011 plan): '
          'tool 3 refuses only because the frozen copy is not yet at path_to_be' % d5['binding_inputs']['case_block']['sha256'][:8],
          codes5 == ['FROZEN_SLOT_NOT_PATH_TO_BE', 'T1:FROZEN_PATH_NOT_PATH_TO_BE'] and any(n['code'] == 'TEXT_OF_RECORD_FROM_ROOT_ARGUMENT' for n in res5['notes']),
          repr(codes5), tag='PORT_CHANGED', r2=138, why='D-05: the later entries are covered by the dispositions fixture D5 instead of covered_later; ' + WHY_RC)
    r_ = T1.run(R5, frozen, None, (), True, None, R5_READs)
    cds = sorted({f['code'] for f in r_['failures']})
    check('T1', 'REAL v003: prereg r5 vs the FROZEN-named copy of the current V005 without a dispositions file refuses exactly DISPOSITIONS_REQUIRED and '
          'UNCOVERED_LATER_ENTRY, naming A102 (L = %s; no section of A47-A101 changed since 70a48f51: CH = [])' % ', '.join(cov5),
          r_['verdict'] == 'REFUSE' and cds == ['DISPOSITIONS_REQUIRED', 'UNCOVERED_LATER_ENTRY'] and all('A102' in f['detail'] for f in r_['failures'])
          and r_.get('dispositions_required') == cov5 and r_.get('changed_sections') == [], repr(r_['failures'])[:400] + repr(r_.get('changed_sections'))[:300],
          tag='REAL_NEW')
    r_ = T1.run(R5, frozen, None, ('A102',), True, None, R5_READs)
    check('T1', 'REAL v003: Codex3\'s bare A102 on prereg r5 and the current V005 refuses (COVERED_LATER_BARE_NAMES_REFUSED; A102 still uncovered)',
          r_['verdict'] == 'REFUSE' and {'COVERED_LATER_BARE_NAMES_REFUSED', 'DISPOSITIONS_REQUIRED', 'UNCOVERED_LATER_ENTRY'} <= {f['code'] for f in r_['failures']},
          repr([f['code'] for f in r_['failures']]), tag='REAL_NEW')
    r_ = T1.run(R5, frozen, None, (), True, D5, R5_READs)
    led5 = r_.get('later_entry_dispositions') or {}
    check('T1', 'REAL v003: L rows %s no_change: with a dispositions file giving each a no_change row prereg r5 passes (dry-run path notes only), and the verified '
          'file and the read copy pin 70a48f51 are returned exactly' % ', '.join(cov5),
          r_['verdict'] == 'PASS' and 'A102' in cov5 and led5.get('pin') == {'path': D5[0], 'sha256': D5[1]}
          and led5.get('raw_text') == Path(D5[0]).read_bytes().decode('utf-8') and [x['entry'] for x in led5.get('content', {}).get('entries', [])] == cov5
          and all(x['disposition'] == 'no_change' for x in led5.get('content', {}).get('entries', []))
          and r_.get('addendum_at_text_of_record') == {'path': R5_READs, 'sha256': REAL_SHAS[R5_READ]}, repr([f['code'] for f in r_['failures']]), tag='REAL_NEW')
    r_ = T1.run(R5, frozen, None, (), True, disp(frozen, later=[e for e in cov5 if e != 'A102']), R5_READs)
    check('T1', 'REAL v003: a dispositions file that omits A102 refuses UNCOVERED_LATER_ENTRY A102', r_['verdict'] == 'REFUSE'
          and any(f['code'] == 'UNCOVERED_LATER_ENTRY' and 'A102' in f['detail'] for f in r_['failures']), repr(r_['failures'])[:300], tag='REAL_NEW')
    record('T1', 'REAL v003: prereg r5 without its read copy refuses ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', T1.run(R5, frozen, None, (), True, D5, None), False,
           'ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED', tag='REAL_NEW')
    record('T1', 'REAL v003: prereg r5 with the current V005 given as its read copy refuses ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH', T1.run(R5, frozen, None, (), True, D5,
           str(frozen)), False, 'ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH', tag='REAL_NEW')
    f5_62 = xwb(run / 'variant_real_A62_edited/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', edited(FB, 62, EDIT62))
    record('T1', 'REAL v003 C-01: prereg r5 against a FROZEN-named copy of the current V005 with an edit inside A62 (no row) refuses ENTRY_SECTION_CHANGED',
           T1.run(R5, f5_62, None, (), True, disp(f5_62, later=cov5), R5_READs), False, 'ENTRY_SECTION_CHANGED', exact=['ENTRY_SECTION_CHANGED'], tag='REAL_NEW')
    record('T1', 'REAL v003 C-01 control: the same with a correct no_change_after_change row for A62 passes', T1.run(R5, f5_62, None, (), True,
           disp(f5_62, later=cov5, nca={'A62': EDIT62[:30]}), R5_READs), True, note='ENTRY_SECTION_CHANGED_NOTED', tag='REAL_NEW')
    record('T1', 'REAL v003 PV-D05-1: the same with plain no_change for A62 refuses', T1.run(R5, f5_62, None, (), True, disp(f5_62, later=cov5 + ['A62']), R5_READs), False,
           'DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY', exact=['DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY'], tag='REAL_NEW')
    # ================= r2: the text-of-record argument while the tool pin is PENDING
    record('T3', 'r2: pin PENDING, root states the stand-in sha: every layer passes and the note names the argument',
           T3.run(slots_p, sp, TOR, frozen=frozen, dispositions=D0, text_of_record_addendum=RC0s, reviewed=reviewed, sealed_compare=sc, text_of_record_sha=C.sha(TOR)),
           True, note='TEXT_OF_RECORD_FROM_ROOT_ARGUMENT', tag='PORT_CHANGED', r2=139, why=WHY_DISP_RC)
    record('T3', 'r2: pin PENDING, root states a sha that is not the file\'s bytes', T3.run(slots_p, sp, TOR, text_of_record_sha='5' * 64), False,
           'TEXT_OF_RECORD_SHA_ARG_MISMATCH', tag='PORT', r2=140)
    record('T3', 'r2: pin PENDING, root states the r4 sha for the r5 stand-in file', T3.run(slots_p, sp, TOR, text_of_record_sha=C.sha(R4)), False,
           'TEXT_OF_RECORD_SHA_ARG_MISMATCH', tag='PORT', r2=141)
    use(TOR)
    record('T3', 'r2: pin set, a stated sha that differs from the pin', T3.run(slots_p, sp, TOR, text_of_record_sha=C.sha(R4)), False, 'TEXT_OF_RECORD_SHA_ARG_DIFFERS',
           tag='PORT', r2=142)
    T3.TEXT_OF_RECORD_SHA = T3.TEXT_OF_RECORD_PENDING
    rA, tA = T4.safe_build(args_for(slots_p, sp, TOR, sc, text_of_record_sha=C.sha(TOR)))
    check('T4', 'r2: the SEAL_RECORD records that root\'s argument pinned the text of record', rA['verdict'] == 'PASS' and tA is not None
          and json.loads(tA).get('text_of_record_pinned_by') == 'ROOT_ARGUMENT', repr([f['code'] for f in rA['failures']]), tag='PORT_CHANGED', r2=143, why=WHY_BASE)
    use(TOR)
    # ================= r2: A102 A-B1 class (a duplicate key behind a 4,300+ digit integer)
    cma_ab1 = xw(run / 'CASCADE_MAP_R5_ADDENDUM_A_B1_SYNTH.json', '{"n": %s, "amends": "%s", "amends": "x"}\n' % (big, M.PIN_R5_CASCADE_MAP[1]))
    p2, sp2 = variant('cma_ab1', lambda s_: s_.update(cascade_map_r5_addendum=rpin(cma_ab1)))
    res = T3run(p2, sp2, TOR)
    record('T3', 'A102 A-B1: a JSON CASCADE_MAP_R5_ADDENDUM with a duplicate key behind a 5,000-digit integer (main-loop patch)', res, False, 'CASCADE_MAP_R5_ADDENDUM_JSON',
           tag='PORT', r2=144)
    chk_ab1 = xw(run / 'CHECK_RECORD_A_B1_SYNTH.json', '{"driver": "%s", "verdict": "PASS", "n": %s, "verdict": "FAIL"}\n' % (dsha, big))
    check('T3', 'A102 A-B1 reproduction: r12\'s own check_record_codes admits that duplicate-key check record (r13 fixes it)',
          M.check_record_codes(str(chk_ab1), dsha) == [], repr(M.check_record_codes(str(chk_ab1), dsha)), tag='PORT', r2=145)
    M13 = C.load_reviewed_compare(str(R13), R13_SHA)
    check('T3', 'r13 (A104): r13\'s own check_record_codes refuses that duplicate-key check record (A102 A-B1 fixed in the compare of record)',
          M13.check_record_codes(str(chk_ab1), dsha) != [], repr(M13.check_record_codes(str(chk_ab1), dsha)), tag='NEW_CONTROL')
    bab1 = json.loads(r5text)
    bab1['check_record'] = rpin(chk_ab1)
    bab1_p = xw(run / 'DRIVER_BUILD_A_B1_CHECK_SYNTH.json', json.dumps(bab1, indent=1, sort_keys=True) + '\n')
    p2, sp2 = variant('dcr_ab1', lambda s_: s_.update(driver_build_record=rpin(bab1_p), driver_check_record=rpin(chk_ab1)))
    res = T3run(p2, sp2, TOR)
    codes = sorted(set(f['code'] for f in res['failures']))
    check('T3', 'A102 A-B1: tool 3 refuses that check record itself (DRIVER_CHECK_RECORD_JSON_DEFECT), though the compare activated the build',
          'DRIVER_CHECK_RECORD_JSON_DEFECT' in codes and 'DRIVER_BUILD_RECORD_REFUSED' not in codes, repr(codes), tag='PORT', r2=146)
    r5ab, t5ab = T5.record_bytes(str(R12), R12_SHA, str(chk_ab1))
    record('T5', 'A102 A-B1: tool 5 refuses to print a driver BUILD record around that check record', r5ab, False, 'CHECK_RECORD_JSON_DEFECT', tag='PORT', r2=147)
    r5ab13, t5ab13 = T5.record_bytes(str(R13), R13_SHA, str(chk_ab1))
    record('T5', 'r13 (A104): tool 5 on r13 refuses to print a driver BUILD record around that check record', r5ab13, False, absent='INTERNAL_EXCEPTION')
    G.CONFIG = run / 'NO_CONFIG_AFTER_TESTS.json'
    os.environ.pop('UNT_ROOT_ADMISSION_SHA256', None)
    open_end = C.sha(OPEN_ADD)
    check('environment', 'the open V005 addendum did not change during this run (else the tool 2 cited-addendum checks would fail for that reason alone)',
          open_end == C.sha_bytes(FB), 'open V005 now %s, copied at start %s' % (open_end[:8], C.sha_bytes(FB)[:8]), tag='ENVIRONMENT')
    # ================= REFUTER PROBES (Claude4 v003 refuter work copy; NOT part of the v003 suite of record): this main()'s fixtures
    _rp_spec = importlib.util.spec_from_file_location('refute_probes_c4v003r', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v003_refute/probes/refute_probes_c4v003r.py')
    _rp = importlib.util.module_from_spec(_rp_spec)
    _rp_spec.loader.exec_module(_rp)
    _rp.run(dict(locals()), globals())
    # ================= the port map: every r2 case once, by index (r2 TEST_RESULTS_C4V002.json 6de5ab43)
    r2res = json.loads(R2_RESULTS.read_bytes())['results']
    ported = sorted(r['r2'] for r in results if r.get('r2') is not None)
    port_ok = ported == list(range(len(r2res))) and len(r2res) == 148
    for r in results:
        if r.get('r2') is not None:
            r['r2_tag'], r['r2_case'] = r2res[r['r2']]['tag'], r2res[r['r2']]['case']
    bad_tags = [r['case'] for r in results if r['tag'] == 'PORT_CHANGED' and not r.get('why')]
    summary = {'tool': 'test_seal_tools_c4v003.py', 'tool_sha256': C.sha(__file__), 'run_dir': str(run), 'utc': stamp,
               'tools': {n: C.sha(TOOLS / n) for n in ('seal_common_c4v003.py', 'check_frozen_addendum_c4v003.py', 'check_sealed_compare_c4v003.py',
                                                        'check_slot_fill_c4v003.py', 'build_seal_record_c4v003.py', 'print_driver_build_record_c4v003.py')},
               'inputs_read': {str(p): C.sha(p) for p in [R4, R12, R12_IMPL, R13, R13_IMPL, DRIVER, CHECK_MD, COMPARATOR, REGISTRY, REGISTRY_V007, DRAFT_CASE_BLOCK, B2_REC,
                                                          B2_REC_V002, BUILD_V007, TEMPLATE_V011, PKT / 'BUILD_V005.md', BUILD_V006, PKT / 'P128/LAUNCH_PLAN_V010.json',
                                                          PKT / 'DRY_R5_MS128_V004.json', PKT / 'bind_sealed_launch_plan_cx1v001.py', PKT / 'producer_guard_cx1v008.py',
                                                          PKT / 'route_a_token_launcher_cx1v007.py', PKT / 'route_a_token_launcher_cx1v006.py', R2 / 'seal_common_c4v002.py',
                                                          R2 / 'check_frozen_addendum_c4v002.py', R2_RESULTS, CX3_LATER[0], CX3_LATER[1], CX3_CHANGED[0], CX3_CHANGED[1],
                                                          CX1_PV[0], CX1_PV[1], CX1_PV[2], CX1_OLD_A90, R5_READ]
                               + [R5] + list(CERTS.values()) + list(IDENTITY_FILES.values())},
               'frozen_copy_of_the_open_V005': {'path': str(frozen), 'sha256': C.sha(frozen), 'entries': 'A47-A%d' % NMAX, 'later_entries_for_prereg_r5': cov5},
               'fixtures': {'text_of_record_standin': pin(TOR), 'read_copy_RC0': pin(RC0), 'read_copy_full': pin(RCF), 'case_block': pin(cbf),
                            'driver_build_record': rpin(dbr), 'build_v007_standin': pin(b7), 'template': pin(template), 'bound_plan': rpin(plan_p),
                            'bound_plan_real_build_v007': rpin(plan_r), 'bound_plan_A90_edited': rpin(plan_90p), 'cascade_addendum_standin': rpin(cma),
                            'seal_record': pin(seal_p), 'prereg_revision_standin': REV, 'dispositions_D0': {'path': D0[0], 'sha256': D0[1]},
                            'dispositions_D5_prereg_r5': {'path': D5[0], 'sha256': D5[1]}, 'dispositions_D_90': {'path': D_90[0], 'sha256': D_90[1]},
                            'frozen_A62_edited': pin(f_62), 'frozen_A90_edited': pin(f_90), 'cx1_pv_d05_1_read_copy': pin(rc_cx)},
               'port': {'r2_cases': len(r2res), 'ported': len(ported), 'each_once': port_ok, 'port_changed_without_reason': bad_tags},
               'results': results, 'passed': sum(r['ok'] for r in results), 'total': len(results),
               'by_tag': {t: '%d/%d' % (sum(r['ok'] for r in results if r['tag'] == t), sum(1 for r in results if r['tag'] == t)) for t in sorted({r['tag'] for r in results})}}
    with open(run / 'TEST_RESULTS_C4V003.json', 'x') as f:
        json.dump(summary, f, indent=1)
    for r in results:
        print('%-11s %-12s %-4s %-96s %-7s %s' % (r['tool'], r['tag'], '' if r.get('r2') is None else r['r2'], r['case'][:96], 'ok' if r['ok'] else 'NOT_OK',
                                               '' if r['ok'] else r['codes']))
    print('passed', summary['passed'], '/', summary['total'], summary['by_tag'], 'port', summary['port'])
    return 0 if summary['passed'] == summary['total'] and port_ok and not bad_tags else 1


if __name__ == '__main__':
    raise SystemExit(main())
