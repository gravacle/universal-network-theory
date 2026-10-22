"""Synthetic tests of fill_c1_pin_c2v002.py. Fixtures and outputs by exclusive create under ./synthetic_gate_test_v002/
(a NEW folder; its root/ is the tool's --synthetic-root, outside claude_artifacts). Not a review, not a C1. Reads the draft
C1_H1_DRAFT_C2V002.json; reads code pins under claude_artifacts (the guard, the producers, the c3v004/c3v005 assemblers
and commons) and hashes registry 2dea408f from bytes (c1_policy_gate L68); opens no NGC3198 file and no run output.
Usage: python3 -I -B fill_test_c1_h1_c2v002.py <stamp from date -u>
"""
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
TOP = os.path.join(HERE, 'synthetic_gate_test_v002')
ROOT = os.path.join(TOP, 'root')
OUTSIDE = os.path.join(TOP, 'outside')
TOOL = os.path.join(HERE, 'fill_c1_pin_c2v002.py')
ART = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'
ASM5 = (ART + '/s4rc1_c3/build_c3v005_c2/registry_assembler_c3v005.py', '7df1c4813865b9e1245f5a91d827591a6d87963b6413ab53c50d2a542d211310')
ASM4 = (ART + '/s4rc1_c3/build_c3v004/registry_assembler_c3v004.py', 'cb5c61ee3d515588394c694b115aca733426db670385eddf92ed389894d065b0')
DRAFT = (os.path.join(HERE, 'C1_H1_DRAFT_C2V002.json'), '3a9299a343bb0a54d90b9e92d2814e78ce44def846adf5a37a890d80a4cf0320')
DRAFT_V001 = (os.path.join(HERE, 'C1_H1_DRAFT_C2V001.json'), '7a6c09c56a0e2b3836521d77928c27bb093c75bc64340f17e0c12ce629ec3ce7')
MARK = 'SYNTHETIC_TEST_FIXTURE_NOT_A_REVIEW (c1_h1 fill test v002; never pin, never publish)'
PY = sys.executable
STAMP = sys.argv[1]
os.mkdir(TOP)
os.mkdir(ROOT)
os.mkdir(OUTSIDE)
CASES = []


def sha(b):
    return hashlib.sha256(b).hexdigest()


def xwrite(path, data):
    with open(path, 'xb') as f:
        f.write(data)
    return {'path': path, 'sha256': sha(data)}


def jwrite(path, obj):
    return xwrite(path, (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode())


def exact(path, want):
    with open(path, 'rb') as f:
        raw = f.read()
    if sha(raw) != want:
        raise SystemExit('REFUSED: %s is not %s' % (path, want[:8]))
    return raw


draft_raw = exact(*DRAFT)
draft = json.loads(draft_raw)
tr = draft['tail_readiness']
DCOPY = xwrite(os.path.join(ROOT, 'C1_H1_DRAFT_C2V002.json'), draft_raw)       # the draft, byte-identical, inside the root
CS = xwrite(os.path.join(ROOT, 'check_script_synthetic_fixture.py'), b'# synthetic check-script fixture; never run\n')
dig = draft['placeholder']['c1_tail_readiness_digest_excluding_review']
BASE = {'schema': 'DDO154_CERTIFICATE_POLICY_REVIEW_CX2V001', 'status': 'TESTED', 'ok': True,
        'driver_sha256': 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6',
        'custody_deriver': tr['custody_deriver'], 'state_enumerator': tr['state_enumerator'],
        'approved_certificate_producers': tr['approved_certificate_producers'],
        'guard_sha256': '9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677',
        'driver_slot_rule': 'POINT_EPS_AND_REGISTERED_RHO_SLOT_PER_STATE_LO_ACCEPTANCE',
        'post_state_handoff': 'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001',
        'c1_tail_readiness_digest_excluding_review': dig, 'reviewed_c1_draft': {'path': DCOPY['path'], 'sha256': DCOPY['sha256']},
        'blocking_findings': [], 'distinct_from_producer_lane': True, 'certificate_registry': tr['certificate_registry'],
        'trusted_source_producers': tr['trusted_source_producers'],
        'trusted_row_policy_review_sha256': tr['trusted_row_policy_review_sha256'], 'signed_utc': STAMP,
        'checks': [{'id': 'C%02d' % i, 'result': 'PASS', 'evidence': 'synthetic'} for i in range(1, 13)],
        'files_opened': [], 'check_script': CS, 'q3_rule': 'synthetic', 'q8_rule': 'synthetic',
        'reviewer_lane': 'SYNTHETIC', 'synthetic': MARK}


def review(name, **chg):
    rv = copy.deepcopy(BASE)
    for k, v in chg.items():
        if v is KeyError:
            rv.pop(k, None)
        else:
            rv[k] = v
    return jwrite(os.path.join(ROOT, name), rv)


def run(tag, rv_pin, *, draft_pin=DCOPY, synthetic=True, root=ROOT, out=None, extra=()):
    out = out or os.path.join(ROOT, 'SYN_FILLED_%s.json' % tag)
    cmd = [PY, '-I', '-B', TOOL, '--draft', draft_pin['path'], '--draft-sha256', draft_pin['sha256'], '--review', rv_pin['path'],
           '--review-sha256', rv_pin['sha256'], '--out', out, '--utc', STAMP]
    if synthetic:
        cmd += ['--synthetic-test'] + ([] if root is None else ['--synthetic-root', root])
    cmd += list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, cwd='/')
    try:
        o = json.loads(p.stdout)
    except ValueError:
        o = {'status': 'NO_JSON', 'stdout': p.stdout[-300:], 'stderr': p.stderr[-300:]}
    return p.returncode, o, out


def refused(cid, tag, rv_pin, code, **kw):
    rc, o, out = run(tag, rv_pin, **kw)
    ok = rc == 2 and o.get('status') == 'REFUSED' and code in o.get('reason', '') and not os.path.exists(out)
    CASES.append({'case': cid, 'kind': 'MUST_REFUSE', 'as_expected': ok, 'expected': code, 'observed': o})


# ---- the positive case
good = review('REV_GOOD.json')
rc, o, out1 = run('OK', good)
filled = None
if rc == 0:
    with open(out1, 'rb') as f:
        filled = json.loads(f.read())
ok1 = (rc == 0 and o.get('status') == 'WRITTEN' and filled is not None
       and filled['schema'] == 'UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002'
       and filled['status'].startswith('SYNTHETIC_TEST_NOT_C1') and 'synthetic_fixture' in filled
       and 'placeholder' not in filled and filled['frozen']['synthetic_test'] is True
       and filled['tail_readiness']['certificate_policy_review'] == {'path': good['path'], 'sha256': good['sha256']}
       and {k: v for k, v in filled['tail_readiness'].items() if k != 'certificate_policy_review'} ==
           {k: v for k, v in tr.items() if k != 'certificate_policy_review'}
       and filled['frozen']['from_draft'] == {'path': DCOPY['path'], 'sha256': DCOPY['sha256']}
       and filled['frozen']['c1_tail_readiness_digest_excluding_review'] == dig and filled['frozen']['check_script'] == CS)
CASES.append({'case': 'F01_bound_synthetic_review_fills_with_the_synthetic_schema_only', 'kind': 'MUST_WRITE', 'as_expected': ok1,
              'expected': 'WRITTEN; schema UNT_DDO154_C1_SYNTHETIC_FILL_TEST_NOT_C1_C2V002; only the review key changes',
              'observed': o})
filled_raw_before = open(out1, 'rb').read() if os.path.exists(out1) else None

# ---- binding and custody refusals (canonical bytes)
refused('F02_wrong_draft_sha_refused', 'BADSHA', good, 'SHA_MISMATCH: draft', draft_pin={'path': DCOPY['path'], 'sha256': '0' * 64})
refused('F03_reordered_producer_list_refused', 'REORDER',
        review('REV_REORDERED.json', approved_certificate_producers=list(reversed(tr['approved_certificate_producers']))),
        'REVIEW_BINDING_MISMATCH: approved_certificate_producers')
refused('F04_ok_1_refused', 'OK1', review('REV_OK1.json', ok=1), 'REVIEW_BINDING_MISMATCH: ok')
refused('F05_ok_string_true_refused', 'OKSTR', review('REV_OKSTR.json', ok='true'), 'REVIEW_BINDING_MISMATCH: ok')
refused('F06_other_driver_refused', 'DRV', review('REV_DRV.json', driver_sha256='9' * 64), 'REVIEW_BINDING_MISMATCH: driver_sha256')
refused('F07_reviewed_draft_other_path_same_sha_refused', 'DPATH',
        review('REV_DPATH.json', reviewed_c1_draft={'path': DRAFT[0], 'sha256': DCOPY['sha256']}),
        'REVIEW_CUSTODY_MISMATCH: reviewed_c1_draft')
refused('F08_blocking_findings_refused', 'BLOCK', review('REV_BLOCK.json', blocking_findings=[{'id': 'X', 'text': 'synthetic'}]),
        'REVIEW_CUSTODY_MISMATCH: blocking_findings')
bad_checks = copy.deepcopy(BASE['checks'])
bad_checks[6]['result'] = 'FAIL'
refused('F09_failed_check_refused', 'CHKFAIL', review('REV_CHKFAIL.json', checks=bad_checks), 'REVIEW_HAS_A_FAILED_CHECK')
refused('F10_missing_check_C07_refused', 'CHKMISS', review('REV_CHKMISS.json', checks=[c for c in BASE['checks'] if c['id'] != 'C07']),
        'REVIEW_CHECKS_MISSING: C07')
refused('F11_check_script_sha_mismatch_refused', 'CSSHA', review('REV_CSSHA.json', check_script={'path': CS['path'], 'sha256': '1' * 64}),
        'SHA_MISMATCH: check script')
dup_raw = (json.dumps(BASE, sort_keys=True, indent=2)[:-2] + ',\n  "ok": true\n}\n').encode()
refused('F12_duplicate_json_key_refused', 'DUP', xwrite(os.path.join(ROOT, 'REV_DUP.json'), dup_raw), 'DUPLICATE_JSON_KEY: ok')
nan_raw = (json.dumps(dict(BASE, nan_probe=0.5), sort_keys=True, indent=2).replace('0.5', 'NaN')).encode()
refused('F13_nan_refused', 'NAN', xwrite(os.path.join(ROOT, 'REV_NAN.json'), nan_raw), 'NONFINITE_JSON')
refused('F14_template_marker_refused', 'TPL', review('REV_TPL.json', q3_rule='<FILL: rule>'), 'REVIEW_IS_AN_UNFILLED_TEMPLATE')
refused('F28_synthetic_mode_needs_a_synthetic_review', 'NOSYN', review('REV_NOSYN.json', synthetic=KeyError),
        'SYNTHETIC_TEST_NEEDS_A_SYNTHETIC_REVIEW')
refused('F29_signed_utc_missing_refused', 'NOUTC', review('REV_NOUTC.json', signed_utc=KeyError), 'REVIEW_SIGNED_UTC_MISSING')

# ---- path, file-type and size refusals (A209 item 6)
link = os.path.join(ROOT, 'REV_SYMLINK.json')
os.symlink(good['path'], link)
refused('F15_symlinked_review_refused', 'SYMLINK', {'path': link, 'sha256': good['sha256']}, 'SYMLINK_COMPONENT: review')
hl_src = review('REV_FOR_HARDLINK.json')
hl = os.path.join(ROOT, 'REV_HARDLINK.json')
os.link(hl_src['path'], hl)
refused('F16_two_link_review_refused', 'HARDLINK', {'path': hl, 'sha256': hl_src['sha256']}, 'NOT_A_SINGLE_LINK_FILE: review')
big = os.path.join(ROOT, 'REV_OVER_8MIB.json')
with open(big, 'xb') as f:
    f.write(b'{')
    f.truncate(8 * 1024 * 1024 + 1)
refused('F17_review_over_8MiB_refused', 'BIG', {'path': big, 'sha256': '2' * 64}, 'FILE_EXCEEDS_8_MIB: review')
ngc = os.path.join(ROOT, 'NGC3198_probe_never_created', 'REV.json')
refused('F18_ngc3198_component_refused_lexically', 'NGC', {'path': ngc, 'sha256': good['sha256']}, 'NGC3198_COMPONENT_REFUSED: review')
uvt = os.path.join(ROOT, 'uvt_probe_never_created', 'REV.json')
refused('F19_uvt_component_refused_lexically', 'UVT', {'path': uvt, 'sha256': good['sha256']}, 'UVT_COMPONENT_REFUSED: review')
out_rv = jwrite(os.path.join(OUTSIDE, 'REV_OUTSIDE.json'), BASE)
refused('F20_review_outside_the_root_refused', 'OUTSIDE', out_rv, 'OUTSIDE_ALLOWED_ROOT')
refused('F21_dot_alias_path_refused', 'ALIAS', {'path': ROOT + '/./REV_GOOD.json', 'sha256': good['sha256']},
        'PATH_NOT_NORMALIZED: review')
refused('F22_real_mode_refuses_paths_outside_claude_artifacts', 'REAL', good, 'OUTSIDE_ALLOWED_ROOT ' + ART, synthetic=False)
refused('F23_synthetic_root_inside_claude_artifacts_refused', 'SYNART', good, 'SYNTHETIC_ROOT_INSIDE_CLAUDE_ARTIFACTS',
        root=ART + '/s4rc1_c3')
refused('F24_synthetic_test_without_root_refused', 'NOROOT', good, 'SYNTHETIC_ROOT_REQUIRED', root=None)
v1copy = xwrite(os.path.join(ROOT, 'C1_H1_DRAFT_C2V001.json'), exact(*DRAFT_V001))
refused('F25_draft_v001_refused', 'V001', review('REV_V001.json', reviewed_c1_draft=v1copy), 'DRAFT_SCHEMA', draft_pin=v1copy)
rc26, o26, _ = run('EXISTS', good, out=out1)
CASES.append({'case': 'F26_existing_output_never_overwritten', 'kind': 'MUST_REFUSE',
              'as_expected': rc26 == 2 and 'File exists' in o26.get('reason', '') and filled_raw_before is not None
              and open(out1, 'rb').read() == filled_raw_before, 'expected': 'FileExistsError; F01 bytes unchanged', 'observed': o26})
refused('F27_output_outside_the_root_refused', 'OUTOUT', good, 'OUTSIDE_ALLOWED_ROOT', out=os.path.join(OUTSIDE, 'SYN_FILLED.json'))
refused('F30_real_mode_rejects_synthetic_root_flag', 'REALROOT', good, 'SYNTHETIC_ROOT_ONLY_WITH_SYNTHETIC_TEST', synthetic=False,
        extra=('--synthetic-root', ROOT))

# ---- in-process unit tests of the real-mode content checks (check_review) and of the canonical comparison
sp = importlib.util.spec_from_file_location('fill_c2v002_unit', TOOL)
FT = importlib.util.module_from_spec(sp)
sp.loader.exec_module(FT)
REAL = {k: v for k, v in copy.deepcopy(BASE).items() if k != 'synthetic'}
REAL['reviewer_lane'] = 'Codex3'
dp = {'path': DCOPY['path'], 'sha256': DCOPY['sha256']}


def unit(cid, rv, code):
    try:
        FT.check_review(rv, tr, draft_pin=dp, tr_digest=dig, synthetic=False)
        got = 'ACCEPTED'
    except FT.Refused as exc:
        got = 'REFUSED: ' + str(exc)
    ok = (got == 'ACCEPTED') if code is None else (got.startswith('REFUSED') and code in got)
    CASES.append({'case': cid, 'kind': 'UNIT', 'as_expected': ok, 'expected': code or 'ACCEPTED', 'observed': got})


unit('U01_real_mode_codex3_review_accepted', copy.deepcopy(REAL), None)
unit('U02_real_mode_top_level_synthetic_key_refused', dict(copy.deepcopy(REAL), synthetic='x'), 'SYNTHETIC_KEY_IN_REVIEW')
nested = copy.deepcopy(REAL)
nested['checks'][0]['synthetic_fixture'] = 'x'
unit('U03_real_mode_nested_synthetic_fixture_key_refused', nested, 'SYNTHETIC_KEY_IN_REVIEW')
unit('U04_real_mode_reviewer_not_codex3_refused', dict(copy.deepcopy(REAL), reviewer_lane='SYNTHETIC'), 'REVIEWER_NOT_CODEX3')
unit('U05_distinct_lane_1_not_true_refused', dict(copy.deepcopy(REAL), distinct_from_producer_lane=1),
     'REVIEW_CUSTODY_MISMATCH: distinct_from_producer_lane')
unit('U06_real_mode_ok_1_refused', dict(copy.deepcopy(REAL), ok=1), 'REVIEW_BINDING_MISMATCH: ok')
unit('U07_missing_check_script_pin_refused', {k: v for k, v in copy.deepcopy(REAL).items() if k != 'check_script'},
     'REVIEW_CHECK_SCRIPT_PIN_MISSING')
same_ok = (FT.same(1, True) is False and FT.same(1.0, 1) is False and FT.same(['a', 'b'], ['b', 'a']) is False
           and FT.same({'a': 1, 'b': 2}, {'b': 2, 'a': 1}) is True and FT.same(True, True) is True)
CASES.append({'case': 'U08_canonical_bytes_equality', 'kind': 'UNIT', 'as_expected': same_ok,
              'expected': '1!=true, 1.0!=1, list order counts, dict key order does not', 'observed': same_ok})


# ---- the filled synthetic C1 against the real verifier gates, in process (reads code pins and hashes the registry)
def load_asm(path, want, name):
    raw = exact(path, want)
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    exec(compile(raw, path, 'exec'), m.__dict__)
    return m


if rc == 0:
    c1_pin = {'path': out1, 'sha256': o['c1']['sha256']}
    A5 = load_asm(*ASM5, 'fill_test_asm_c3v005')
    _, bl5 = A5.c1_policy_gate(c1_pin, tr['certificate_registry'], roots=(A5.C.ART, ROOT))
    CASES.append({'case': 'G01_filled_six_pin_C1_passes_the_c3v005_policy_gate', 'kind': 'GATE', 'as_expected': bl5 == [],
                  'expected': 'no blockers (common c3v005 canonical six, no override)', 'observed': bl5})
    A4 = load_asm(*ASM4, 'fill_test_asm_c3v004')
    _, bl4 = A4.c1_policy_gate(c1_pin, tr['certificate_registry'], roots=(A4.C.ART, ROOT))
    six = tr['approved_certificate_producers']
    CASES.append({'case': 'G02_same_C1_refused_by_c3v004_with_exactly_three_blockers', 'kind': 'GATE',
                  'as_expected': len(bl4) == 3 and all(b.startswith('C1_APPROVED_PRODUCER_NOT_CANONICAL') for b in bl4)
                  and all(any(p['sha256'] in b for b in bl4) for p in six[3:]),
                  'expected': '3 x C1_APPROVED_PRODUCER_NOT_CANONICAL (211a3220, 08e9ac0a, 7044e131)', 'observed': bl4})
    ok1rv = review('REV_OK1_FOR_GATE.json', ok=1)
    ok1c1 = jwrite(os.path.join(ROOT, 'SYN_C1_OK1_DIRECT.json'),
                   {'synthetic_fixture': MARK, 'tail_readiness': dict(copy.deepcopy(filled['tail_readiness']),
                                                                     certificate_policy_review=ok1rv)})
    _, bl6 = A5.c1_policy_gate(ok1c1, tr['certificate_registry'], roots=(A5.C.ART, ROOT))
    CASES.append({'case': 'G03_c3v005_gate_refuses_a_review_with_ok_1', 'kind': 'GATE',
                  'as_expected': bl6 == ['evidence is not TESTED ok'], 'expected': "['evidence is not TESTED ok']", 'observed': bl6})

res = {'schema': 'C1_H1_FILL_TEST_C2V002', 'utc': STAMP, 'tool': {'path': TOOL, 'sha256': sha(open(TOOL, 'rb').read())},
       'draft': {'path': DRAFT[0], 'sha256': DRAFT[1]}, 'cases': CASES, 'n': len(CASES),
       'n_as_expected': sum(1 for c in CASES if c['as_expected']), 'all_as_expected': all(c['as_expected'] for c in CASES),
       'synthetic_fixture': 'fill tool v002 test results; synthetic; not a review, not a C1'}
p = jwrite(os.path.join(TOP, 'FILL_TEST_RESULTS_C2V002.json'), res)
print(json.dumps({'results': p, 'n': res['n'], 'n_as_expected': res['n_as_expected'], 'all_as_expected': res['all_as_expected'],
                  'failed': [c['case'] for c in CASES if not c['as_expected']]}, indent=1))
sys.exit(0 if res['all_as_expected'] else 1)
