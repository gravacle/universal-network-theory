# c3v003 (0644 follow-up: r6 wired): the text of record is the REAL r6 (d28c95f5) named by the REAL SELECTED_R6_C4V001 (7200acd9); the
# C02/SEL cases use the real role schema (files.text_of_record) through check-tor --selected-schema/--tor-role, and selected-roles is
# checked on the real file; Codex1's schema-less fixtures now all refuse.
# c3v002 (FROM_CODEX/0644, A107; Codex1 0101): + C02-SEL-ASSOCIATION / C02-SEL-STRICT (Codex1's own five counterexample files,
# read only, and replicas; every strict-parse class), the v003 selected-names path, A106-C03-S1 (null / empty / malformed / upper-case
# embedded hashes), and C-04 with the A107 exclusion list (a third slot, another sha or path, one entry, a changed excluded pin) and
# the gate pass verdict (a REGISTERED record with a FAIL, absent or unknown verdict, through a synthetic registry copy).
# Claude3 (FROM_CODEX/0643, A106): MUST_FAIL controls for A (the FINAL V005 freeze), C-02, C-03, C-04, C-05 and C-06. Every case runs
# the helper's own CLI in a separate isolated process (python3 -I -B -X pycache_prefix=<empty>), exactly as ROOT_SEAL_STEPS calls
# it. The positive inputs are dry run 10's real pass-B outputs (read only); every edited input is a synthetic copy written under OUTDIR
# (open 'x'). Nothing outside OUTDIR is written.
# usage: python3 -I -B mustfail_c0x_c3sa_c3v001.py OUTDIR HELPER=SHA DRYRUN_DIR
import hashlib, json, os, subprocess, sys
OUT, HS, DRY = sys.argv[1], sys.argv[2], sys.argv[3]
HP, HSHA = HS.rsplit('=', 1)
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; PKT = A + '/v007_launch_packet_cx1'
assert hashlib.sha256(open(HP, 'rb').read()).hexdigest() == HSHA
os.mkdir(OUT); PFX = OUT + '/NO_PYCACHE_PREFIX_EMPTY'; os.mkdir(PFX)
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def wx(name, data):
    p = OUT + '/' + name
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return p, sha(p)
RES = []
def case(cid, desc, argv, want, post=None):
    r = subprocess.run([PY, '-I', '-B', '-X', 'pycache_prefix=' + PFX, HP] + argv, capture_output=True, text=True, cwd='/',
                       env={'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
                            'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'})
    lines = [ln for ln in r.stderr.splitlines() if ln.strip()]
    try:
        v = json.loads(lines[-1])
    except Exception:
        v = {'verdict': 'NO_VERDICT', 'code': r.stderr[-300:]}
    row = {'case': cid, 'what': desc, 'want': want, 'verdict': v.get('verdict'), 'exit': r.returncode, 'code': (v.get('code') or '')[:400]}
    if post:
        row['post'] = post()
    row['MUST_FAIL_ok'] = row['verdict'] == want and row['exit'] == (0 if want == 'PASS' else 2) and all((row.get('post') or {}).values())
    RES.append(row)
    return v
B = DRY + '/passB'; S = B + '/scratch_ctrl/V007_SEAL_ASSEMBLY'
BP = B + '/scratch_pkt/P128/LAUNCH_PLAN_V011_CX3V001_BOUND_R5_V007_SEAL.json'; BC = B + '/scratch_pkt/P128/LAUNCH_COMMAND_V011_CX3V001_BOUND_R5_V007_SEAL.txt'
BIN = B + '/scratch_pkt/bind_sealed_launch_plan_cx1v001.py'; SL = S + '/SLOT_VALUES_FINAL_V007.json'; SP = S + '/KMAX_TAIL_PREREG_V007_SEALED.json'
GJ = S + '/E_SEAL1_GATES_ONLY_OUT/GATES_ONLY.json'; R6F = A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json'; assert sha(R6F) == '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
TOR = A + '/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json'; TORS = 'd28c95f56321f566b444c3e0bfbbe0ecdac564cbc03a8583ecd5f8d0ae40c0a9'
SELS = 'UNT_V007_SELECTED_PREREG_C4V001'
R4 = A + '/v007_final_prereg_c4/r4/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R4.json'
OPEN = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
FIN, FINB = 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1', 143081
BUILD, BUILDS = PKT + '/BUILD_V007.md', '94bc05a5db1e6350b246c22e850ae62d95cd05ce21cdf5b329e3edded588a0de'
LA, LAS = PKT + '/route_a_token_launcher_cx1v007.py', '861bba68dd7d207beb30ed828c1557955f31979cf2e15369acccc52ea595953d'
GU, GUS = PKT + '/producer_guard_cx1v008.py', '294cb7760679b883a62fb3117dc75e91231b2f173bcec65983e6762371ea0731'
EA, EAS = PKT + '/ea_replay_cx1v012.py', '380e2d81027eba4c86843b904ccb79f5f27e6c917b5f3f5a71f286c01be32156'
SF, SFS = PKT + '/shell_filter_cx1v004.py', '4fcbd495fe41e881637aa64eef342c8adf1193b54e9b7e80b7261f9217b5dabb'
BINS = 'f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca'
R13, R13S = A + '/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
REG, REGS = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json', '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8'
FEN, FENS = A + '/seal_assembly_c3/tools/fence_c3sa_c3v003.py', '9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863'
GQ5, GQ5S = A + '/tail_scheme_impl_c2/certificates_v003/gates/GQ_CERT_V005_MS128.json', 'fbceefe68fec' 
GQ5S = sha(GQ5); assert GQ5S.startswith('fbceefe6')
OLDC = A + '/tail_scheme_impl_c2/gates_v007/run_identity_compare_c2v007.py'; OLDCS = sha(OLDC); assert OLDCS.startswith('06ff52d6')
# ---------------------------------------------------------------------------------------------- A: the FINAL V005 freeze
ob = open(OPEN, 'rb').read(); assert hashlib.sha256(ob).hexdigest() == FIN and len(ob) == FINB
op, _ = wx('SYNTHETIC_OPEN_COPY_V005_ADDENDUM.md', ob)
case('A-0', 'freeze a byte copy of the final V005 (sha and length right)', ['freeze', '--open', op, '--open-sha', FIN, '--open-bytes', str(FINB), '--out', OUT + '/A0_V005_ADDENDUM_FROZEN.md'], 'PASS',
     post=lambda: {'copy_is_the_final_bytes': sha(OUT + '/A0_V005_ADDENDUM_FROZEN.md') == FIN})
case('A-1', 'the right sha but a wrong length (143080)', ['freeze', '--open', op, '--open-sha', FIN, '--open-bytes', str(FINB - 1), '--out', OUT + '/A1_V005_ADDENDUM_FROZEN.md'], 'REFUSE',
     post=lambda: {'nothing_copied': not os.path.lexists(OUT + '/A1_V005_ADDENDUM_FROZEN.md')})
op2, _ = wx('SYNTHETIC_OPEN_PLUS_ONE_BYTE_V005_ADDENDUM.md', ob + b'\n')
case('A-2', 'an open file one byte longer, checked against the final sha', ['freeze', '--open', op2, '--open-sha', FIN, '--open-bytes', str(FINB), '--out', OUT + '/A2_V005_ADDENDUM_FROZEN.md'], 'REFUSE',
     post=lambda: {'nothing_copied': not os.path.lexists(OUT + '/A2_V005_ADDENDUM_FROZEN.md')})
case('A-3', 'the FROZEN copy exists already (exclusive create)', ['freeze', '--open', op, '--open-sha', FIN, '--open-bytes', str(FINB), '--out', OUT + '/A0_V005_ADDENDUM_FROZEN.md'], 'REFUSE')
# ---------------------------------------------------------------------------------------------- C-02
SPS, SLS = sha(SP), sha(SL)
tor_args = lambda t, ts, sel, sels: ['check-tor', '--text-of-record', t, '--tor-sha', ts, '--selected', sel, '--selected-sha', sels, '--selected-schema', SELS, '--tor-role', 'text_of_record']
full = lambda t, ts, sel, sels, sp, sps: tor_args(t, ts, sel, sels) + ['--sealed-prereg', sp, '--sealed-prereg-sha', sps, '--slots', SL, '--slots-sha', SLS]
case('C02-0', 'control: the real r6, named by the real SELECTED_R6_C4V001, + the real sealed prereg and slots', full(TOR, TORS, R6F, sha(R6F), SP, SPS), 'PASS')
sp_text = open(SP, 'rb').read().decode('utf-8'); d = json.loads(sp_text)
d['seal_slots']['driver']['rule'] = str(d['seal_slots']['driver']['rule']) + ' SYNTHETIC EDIT (MUST_FAIL control C-02)'
ep, eps = wx('C02_EDITED_SEALED_PREREG.json', json.dumps(d, indent=1, ensure_ascii=False) + '\n')
case('C02-1', 'an EDITED sealed prereg named as its own text of record (and as the sealed prereg)', full(ep, eps, R6F, sha(R6F), ep, eps), 'REFUSE')
fs, fss = wx('C02_FORGED_SELECTED_NAMING_THE_EDITED_FILE.json', json.dumps({'schema': SELS, 'files': {'text_of_record': {'path': ep, 'sha256': eps}}}, indent=1) + '\n')
case('C02-2', 'the same edited sealed prereg, with a forged SELECTED that names it', tor_args(ep, eps, fs, fss), 'REFUSE')
fs2, fss2 = wx('C02_FORGED_SELECTED_NAMING_THE_SEALED_PREREG.json', json.dumps({'schema': SELS, 'files': {'text_of_record': {'path': SP, 'sha256': SPS}}}, indent=1) + '\n')
case('C02-3', 'the genuine sealed prereg named as the text of record (forged SELECTED names it)', tor_args(SP, SPS, fs2, fss2), 'REFUSE')
case('C02-4', 'r5 as text of record, but a sealed prereg edited outside the slot values', full(TOR, TORS, R6F, sha(R6F), ep, eps), 'REFUSE')
fs3, fss3 = wx('C02_SELECTED_NAMING_R5_WITH_ANOTHER_SHA.json', json.dumps({'schema': SELS, 'files': {'text_of_record': {'path': TOR, 'sha256': TORS}, 'b': {'path': TOR, 'sha256': '0' * 64}}}, indent=1) + '\n')
case('C02-5', 'a SELECTED file that also gives the text-of-record path another sha', tor_args(TOR, TORS, fs3, fss3), 'REFUSE')
case('C02-6', 'prereg r4 as the text of record while the SELECTED file stores r6', tor_args(R4, sha(R4), R6F, sha(R6F)), 'REFUSE')
case('C02-7', 'the sealed prereg given as both files (same path and sha)', full(SP, SPS, fs2, fss2, SP, SPS), 'REFUSE')
# ---------------------------------------------------------------------------------------------- C-03
g = json.loads(open(GJ, 'rb').read()); GJS = sha(GJ)
prov = lambda p, ps: ['gates-provenance', '--gates-json', p, '--gates-json-sha', ps, '--slots', SL, '--slots-sha', SLS]
case('C03-0', 'control: the real sealed-mode GATES_ONLY body of dry run 10', prov(GJ, GJS), 'PASS')
def gvar(name, fn):
    x = json.loads(json.dumps(g)); fn(x); return wx(name, json.dumps(x, indent=1) + '\n')
case('C03-1', 'the body evaluated another GQ record than the slot', prov(*gvar('C03_GQ_OTHER_RECORD.json', lambda x: x['gates']['GQ'].__setitem__('record_sha256', GQ5S))), 'REFUSE')
case('C03-2', 'the B1 (Z2) gate status is FAIL', prov(*gvar('C03_B1_FAIL.json', lambda x: x['gates']['B1'].__setitem__('status', 'FAIL'))), 'REFUSE')
case('C03-3', 'the LO_NGC gate is missing from the body', prov(*gvar('C03_LO_NGC_MISSING.json', lambda x: x['gates'].pop('LO_NGC'))), 'REFUSE')
case('C03-4', 'a test-mode body (not sealed)', prov(*gvar('C03_TEST_MODE.json', lambda x: x.__setitem__('test_mode', True))), 'REFUSE')
# ---------------------------------------------------------------------------------------------- C-04 (A107 exclusions + pass verdict)
EPSN = ('certificates.EPS_NGC', A + '/tail_scheme_impl_c2/certificates_ngc_k32/gates/EPS_CERT_NGC91_V001.json', '1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d')
I1TN = ('certificates.I1T_NGC', A + '/tail_scheme_impl_c2/certificates_v002/gates/I1T_NGC_T120L_V001.json', '3ae7981a0c022d50a153a0857b10660661fedfd5adedcba3b805802b4a1809b6')
ex = lambda *e: [y for x in e for y in ('--exclude', '%s=%s=%s' % x)]
EXCL = ex(EPSN, I1TN)
reg_args = lambda sl, sls, excl=EXCL, reg=REG, regs=REGS: ['slot-registry', '--compare', R13, '--compare-sha', R13S, '--registry', reg, '--registry-sha', regs,
                                                   '--slots', sl, '--slots-sha', sls, '--fence', FEN, '--fence-sha', FENS] + excl
sl0 = json.loads(open(SL, 'rb').read())
case('C04-0', 'control: the real final slots with exactly the A107 two-entry exclusion list (every other slot passes, with its pass verdict)', reg_args(SL, SLS), 'PASS')
case('C04-1', 'the real final slots with NO exclusion list', reg_args(SL, SLS, excl=[]), 'REFUSE')
def svar(name, fn):
    x = json.loads(json.dumps(sl0)); fn(x)
    return wx(name, json.dumps(x, indent=1, ensure_ascii=False) + '\n')
case('C04-2', 'the GQ slot holds the superseded GQ V005 record (fbceefe6)', reg_args(*svar('C04_SLOTS_GQ_V005.json', lambda x: x['certificates'].__setitem__('GQ', {'path': GQ5, 'sha256': GQ5S}))), 'REFUSE')
case('C04-3', 'the identity comparator slot holds a superseded comparator (gates_v007 c2v007, 06ff52d6)', reg_args(*svar('C04_SLOTS_OLD_COMPARATOR.json', lambda x: x.__setitem__('identity_comparator', {'path': OLDC, 'sha256': OLDCS}))), 'REFUSE')
case('C04-4', 'the Z2 slot holds the B1_OFF record (gate not the slot)', reg_args(*svar('C04_SLOTS_Z2_IS_B1_OFF.json', lambda x: x['identity_gate_records'].__setitem__('Z2', dict(x['identity_gate_records']['Z2_OFF_RO1'])))), 'REFUSE')
case('C04-5', 'the slots name another registry sha than the one checked', reg_args(*svar('C04_SLOTS_OTHER_REGISTRY_SHA.json', lambda x: x['producer_registry'].__setitem__('sha256', '0' * 64))), 'REFUSE')
GQS = sl0['certificates']['GQ']
case('C04-6', 'A107 MUST_FAIL: a THIRD slot (certificates.GQ) added to the exclusion list', reg_args(SL, SLS, excl=EXCL + ex(('certificates.GQ', GQS['path'], GQS['sha256']))), 'REFUSE')
case('C04-7', 'A107 MUST_FAIL: the EPS_NGC exclusion with another sha', reg_args(SL, SLS, excl=ex((EPSN[0], EPSN[1], '0' * 64), I1TN)), 'REFUSE')
case('C04-8', 'the I1T_NGC exclusion with another path', reg_args(SL, SLS, excl=ex(EPSN, (I1TN[0], I1TN[1] + '.other', I1TN[2]))), 'REFUSE')
case('C04-9', 'only one of the two exclusions', reg_args(SL, SLS, excl=ex(EPSN)), 'REFUSE')
case('C04-10', 'the slot EPS_NGC holds another record than the A107 pin (the exclusion names the A107 pin)', reg_args(*svar('C04_SLOTS_EPS_NGC_OTHER.json', lambda x: x['certificates'].__setitem__('EPS_NGC', dict(x['certificates']['EPS'])))), 'REFUSE')
case('C04-11', 'the same exclusion entry given twice', reg_args(SL, SLS, excl=EXCL + ex(EPSN)), 'REFUSE')
# the pass verdict (Codex1 0101 C04 boundary note): REGISTERED synthetic EPS records whose verdict is FAIL / absent / unknown, via a synthetic
# registry copy whose gate_records.EPS also lists them (so registry admission passes and only the verdict can refuse)
eps_ref = sl0['certificates']['EPS']; eps = json.loads(open(eps_ref['path'], 'rb').read()); assert eps.get('verdict') == 'CERTIFIED'
syn = {}
for tag, fn in (('PASS', lambda r: r.__setitem__('verdict', 'CERTIFIED')), ('FAIL', lambda r: r.__setitem__('verdict', 'FAIL')),
                ('ABSENT', lambda r: r.pop('verdict')), ('UNKNOWN', lambda r: r.__setitem__('verdict', 'NOT_COMPUTED'))):
    r = json.loads(json.dumps(eps)); fn(r); r['synthetic_note'] = 'SYNTHETIC MUST_FAIL record (Claude3 0644): EPS_CERT_V006 copy, verdict %s' % tag
    syn[tag] = wx('C04_SYNTHETIC_EPS_%s.json' % tag, json.dumps(r, indent=1) + '\n')
regobj = json.loads(open(REG, 'rb').read()); regobj['gate_records']['EPS'] = list(regobj['gate_records']['EPS']) + [syn[t][1] for t in ('PASS', 'FAIL', 'ABSENT', 'UNKNOWN')]
regobj['note'] = 'SYNTHETIC registry copy of V009 (Claude3 0644 MUST_FAIL): gate_records.EPS also lists four synthetic EPS records'
SREG, SREGS = wx('C04_SYNTHETIC_REGISTRY_V009_COPY.json', json.dumps(regobj, indent=1) + '\n')
for cid, tag, want in (('C04-12', 'PASS', 'PASS'), ('C04-13', 'FAIL', 'REFUSE'), ('C04-14', 'ABSENT', 'REFUSE'), ('C04-15', 'UNKNOWN', 'REFUSE')):
    p, h = syn[tag]
    slp, slh = svar('C04_SLOTS_SYNTHETIC_EPS_%s.json' % tag, lambda x, p=p, h=h: (x['certificates'].__setitem__('EPS', {'path': p, 'sha256': h}),
                                                                                  x.__setitem__('producer_registry', {'path': SREG, 'sha256': SREGS})))
    case(cid, 'registered synthetic EPS record, verdict %s (registry admission passes; only the verdict decides)' % tag, reg_args(slp, slh, reg=SREG, regs=SREGS), want)
# ---------------------------------------------------------------------------------------------- C02-SEL, role-qualified (c3v014; real r6 schema)
CX = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_prestage_cx1/provisional_a106_cx1v001/c02_freeze_cx1v001/fixtures'
CTOR = CX + '/tor_inert.json'
for cid, f in (('CX1-SEL-0', 'selected_good.json'), ('CX1-SEL-1', 'selected_unassociated_strings.json'), ('CX1-SEL-2', 'selected_different_selected_path_prefix.json'),
               ('CX1-SEL-3', 'selected_duplicate_json_keys.json'), ('CX1-SEL-4', 'selected_invalid_json_trailing.json'), ('CX1-SEL-5', 'selected_nonfinite_json.json')):
    case(cid, "Codex1 0101's own fixture %s (read only): the real SELECTED schema is now required, so every schema-less form refuses" % f,
         tor_args(CTOR, sha(CTOR), CX + '/' + f, sha(CX + '/' + f)), 'REFUSE')
def selx(cid, desc, obj, want, raw=None):
    p, h = wx('SEL_%s.json' % cid.replace('-', '_'), raw if raw is not None else json.dumps(obj, indent=1) + '\n')
    case(cid, desc, tor_args(TOR, TORS, p, h), want)
pair = {'path': TOR, 'sha256': TORS}
base = lambda **files: {'schema': SELS, 'files': dict({'text_of_record': dict(pair)}, **files)}
selx('SEL-A0', 'control: the real schema, text_of_record exactly the pair, other roles present', base(entry_table={'path': R4, 'sha256': sha(R4)}), 'PASS')
selx('SEL-A1', 'unassociated strings: no files.text_of_record; the path and the sha in two other fields',
     {'schema': SELS, 'files': {'x': {'path': R4, 'sha256': sha(R4)}}, 'requested_path': TOR, 'unrelated_sha': TORS}, 'REFUSE')
selx('SEL-A2', 'files.text_of_record path is the requested path plus ".other"', {'schema': SELS, 'files': {'text_of_record': {'path': TOR + '.other', 'sha256': TORS}}}, 'REFUSE')
selx('SEL-A3', 'the path and the sha split across two roles', {'schema': SELS, 'files': {'text_of_record': {'path': TOR, 'sha256': '1' * 64}, 'other': {'path': R4, 'sha256': TORS}}}, 'REFUSE')
selx('SEL-A4', 'files.text_of_record with an extra key', {'schema': SELS, 'files': {'text_of_record': dict(pair, note='x')}}, 'REFUSE')
selx('SEL-A5', 'the exact pair only under another role name', {'schema': SELS, 'files': {'text_of_record_r6': dict(pair)}}, 'REFUSE')
selx('SEL-A6', 'another schema string', dict(base(), schema='UNT_V007_SELECTED_PREREG_C4V999'), 'REFUSE')
selx('SEL-A7', 'another files entry with a relative path', base(other={'path': 'relative/x.json', 'sha256': sha(R4)}), 'REFUSE')
selx('SEL-A8', 'another files entry with an upper-case sha', base(other={'path': R4, 'sha256': sha(R4).upper()}), 'REFUSE')
selx('SEL-A9', 'another role gives the text-of-record path another sha', base(dup={'path': TOR, 'sha256': '2' * 64}), 'REFUSE')
selx('SEL-A10', "'files' is a list of pairs, not an object", {'schema': SELS, 'files': [dict(pair, role='text_of_record')]}, 'REFUSE')
good = json.dumps(base())[:-1]   # the valid object text without its closing brace, for the raw strictness cases
selx('SEL-S1', 'duplicate key (files twice)', None, 'REFUSE', raw=good + ', "files": {}}')
selx('SEL-S2', 'trailing invalid text', None, 'REFUSE', raw=good + '}\nNOT JSON\n')
selx('SEL-S3', 'NaN', None, 'REFUSE', raw=good + ', "x": NaN}')
selx('SEL-S4', '-Infinity', None, 'REFUSE', raw=good + ', "x": -Infinity}')
selx('SEL-S5', 'a float overflowing to inf (1e999)', None, 'REFUSE', raw=good + ', "x": 1e999}')
selx('SEL-S6', 'an integer of 4301 digits', None, 'REFUSE', raw=good + ', "x": %s}' % ('9' * 4301))
selx('SEL-S7', 'invalid UTF-8 bytes', None, 'REFUSE', raw=(good + ', "x": "Z"}').encode().replace(b'"Z"', b'"\xff\xfe"'))
selx('SEL-S8', 'nesting 100 levels deep', None, 'REFUSE', raw=good + ', "x": %s}' % ('[' * 100 + ']' * 100))
selx('SEL-S9', 'a top-level list', None, 'REFUSE', raw=json.dumps([base()]))
selx('SEL-S10', 'a UTF-8 BOM', None, 'REFUSE', raw=b'\xef\xbb\xbf' + json.dumps(base()).encode())
# selected-roles on the REAL r6 SELECTED file (the step-0 roles)
SR = lambda sel, sels, *rp: ['selected-roles', '--selected', sel, '--selected-sha', sels, '--schema', SELS] + [y for x in rp for y in ('--role-pin', '%s=%s=%s' % x)]
ADD6 = A + '/v007_final_prereg_c4/r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'
CB, CBS = A + '/v007_final_prereg_c4/r5/case_block/CASE_BLOCK_V007_C4V001.json', '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71'
IMPL, IMPLS = A + '/v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3'
ROLES = (('addendum_at_text_of_record', ADD6, FIN), ('case_block', CB, CBS), ('impl_of_record_r13', IMPL, IMPLS), ('closed_v005_live', OPEN, FIN))
case('R6-0', 'control: the real r6 SELECTED file stores exactly the four step-0 roles', SR(R6F, sha(R6F), *ROLES), 'PASS')
case('R6-1', 'the case_block role with another sha', SR(R6F, sha(R6F), ('case_block', CB, '0' * 64)), 'REFUSE')
case('R6-2', "r5's addendum copy given as addendum_at_text_of_record",
     SR(R6F, sha(R6F), ('addendum_at_text_of_record', A + '/v007_final_prereg_c4/r5/addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md', '70a48f51e20311de82a37b13bee8cf18f7eaf9adbb976d957e50c5334e7c8c7e')), 'REFUSE')
case('R6-3', 'a role the SELECTED file does not have', SR(R6F, sha(R6F), ('impl_of_record_r12', IMPL, IMPLS)), 'REFUSE')
case('R6-4', 'the right role and pin but the wrong schema string', ['selected-roles', '--selected', R6F, '--selected-sha', sha(R6F), '--schema', 'UNT_V007_SELECTED_PREREG_C4V002', '--role-pin', '%s=%s=%s' % ROLES[1]], 'REFUSE')
V3F = DRY + '/fixtures/V003_SELECTED_DRYRUN_FIXTURE.json'; v3 = json.loads(open(V3F, 'rb').read()); TPINS = [(t['path'], t['sha256']) for t in v3['tools']]
v3args = lambda p, h: ['selected-names', '--selected', p, '--selected-sha', h] + [y for t in TPINS for y in ('--pin', '%s=%s' % t)]
case('V3-0', 'v003 selected-names: control, the labelled v003 fixture (exact pairs)', v3args(V3F, sha(V3F)), 'PASS')
case('V3-1', 'v003 selected-names: the tool paths and shas only as unassociated strings',
     v3args(*wx('V3_UNASSOCIATED.json', json.dumps({'paths': [p for p, _ in TPINS], 'shas': [h for _, h in TPINS]}))), 'REFUSE')
case('V3-2', 'v003 selected-names: a duplicate key', v3args(*wx('V3_DUPKEY.json', '{"tools": %s, "tools": []}' % json.dumps([{'path': p, 'sha256': h} for p, h in TPINS]))), 'REFUSE')
case('V3-3', 'v003 selected-names: one tool named with a suffixed path',
     v3args(*wx('V3_SUFFIX.json', json.dumps({'tools': [{'path': p + ('.bak' if i == 2 else ''), 'sha256': h} for i, (p, h) in enumerate(TPINS)]}))), 'REFUSE')
# ---------------------------------------------------------------------------------------------- A106-C03-S1
for cid, val, bodyval in (('C03-5', None, None), ('C03-6', '', ''), ('C03-7', 'not-a-sha', 'not-a-sha'),
                          ('C03-8', 'GOOD', 'not-a-sha'), ('C03-9', 'UPPER', 'UPPER')):
    good_sha = sl0['certificates']['EPS']['sha256']
    v = {'GOOD': good_sha, 'UPPER': good_sha.upper()}.get(val, val); bv = {'GOOD': good_sha, 'UPPER': good_sha.upper()}.get(bodyval, bodyval)
    slp, slh = svar('C03_SLOTS_EPS_%s.json' % cid.replace('-', '_'), lambda x, v=v: x['certificates']['EPS'].__setitem__('sha256', v))
    gp, gh = gvar('C03_BODY_EPS_%s.json' % cid.replace('-', '_'), lambda x, bv=bv: x['gates']['EPS'].__setitem__('record_sha256', bv))
    case(cid, 'A106-C03-S1: slot EPS sha %r, body record_sha256 %r (status PASS)' % (val, bodyval),
         ['gates-provenance', '--gates-json', gp, '--gates-json-sha', gh, '--slots', slp, '--slots-sha', slh], 'REFUSE')
# ---------------------------------------------------------------------------------------------- C-05 / C-06
BPS, BCS = sha(BP), sha(BC)
bnd = lambda bp, bps, bc, bcs, la=LA, las=LAS, gu=GU, gus=GUS: ['bound-check', '--build', BUILD, '--build-sha', BUILDS, '--plan', bp, '--plan-sha', bps,
        '--command', bc, '--command-sha', bcs, '--binder', BIN, '--binder-sha', BINS, '--launcher', la, '--launcher-sha', las, '--guard', gu, '--guard-sha', gus]
case('C05-0', 'control: the real bound plan and command of dry run 10', bnd(BP, BPS, BC, BCS), 'PASS')
pl = json.loads(open(BP, 'rb').read())
def pvar(name, key, ref):
    x = json.loads(json.dumps(pl)); x[key] = ref; return wx(name, json.dumps(x, indent=1) + '\n')
case('C05-1', 'the bound plan names another allowlisted source (ea_replay_cx1v012) as the launcher', bnd(*pvar('C05_PLAN_LAUNCHER_EA_REPLAY.json', 'launcher', {'path': EA, 'sha256': EAS}), BC, BCS), 'REFUSE')
case('C05-2', 'the bound plan names another allowlisted source (shell_filter_cx1v004) as the guard', bnd(*pvar('C05_PLAN_GUARD_SHELL_FILTER.json', 'guard', {'path': SF, 'sha256': SFS}), BC, BCS), 'REFUSE')
case('C05-3', 'another allowlisted source given AS the launcher (ea_replay, its BUILD row)', bnd(BP, BPS, BC, BCS, la=EA, las=EAS), 'REFUSE')
case('C05-4', 'the launcher by its exact name but another sha', bnd(BP, BPS, BC, BCS, las=EAS), 'REFUSE')
cb = open(BC, 'rb').read(); l1, rest = cb.split(b'\n', 1)
case('C06-0', 'control: the real bound command (2 lines) is byte-equal to the binder output form', bnd(BP, BPS, BC, BCS), 'PASS')
case('C06-1', 'an edit in the NON-final line (the comment line); the last line intact', bnd(BP, BPS, *wx('C06_EDIT_FIRST_LINE.txt', l1.replace(b'launches nothing', b'launches nothing (edited)') + b'\n' + rest)), 'REFUSE')
case('C06-2', 'an extra trailing line', bnd(BP, BPS, *wx('C06_EXTRA_LINE.txt', cb + b'echo extra\n')), 'REFUSE')
case('C06-3', 'the last line edited (another plan path)', bnd(BP, BPS, *wx('C06_EDIT_LAST_LINE.txt', cb.replace(b'_BOUND_R5_V007_SEAL.json', b'_BOUND_R5_V007_SEAL_X.json'))), 'REFUSE')
case('C06-4', 'CRLF line endings', bnd(BP, BPS, *wx('C06_CRLF.txt', cb.replace(b'\n', b'\r\n'))), 'REFUSE')
ok = all(r['MUST_FAIL_ok'] for r in RES)
res = {'schema': 'C3SA_MUSTFAIL_C0X_V003', 'helper': {'path': HP, 'sha256': HSHA}, 'dry_run': DRY, 'n_cases': len(RES), 'ALL_OK': ok,
       'pycache_prefix_entries': len(os.listdir(PFX)), 'results': RES}
t = json.dumps(res, indent=1) + '\n'
with open(OUT + '/MUSTFAIL_C0X_RESULTS_C3SA.json', 'x') as f:
    f.write(t)
print(json.dumps({'ALL_OK': ok, 'n': len(RES), 'sha256': hashlib.sha256(t.encode()).hexdigest(), 'pycache_prefix_entries': len(os.listdir(PFX))}))
for r in RES:
    print('%-7s %-7s exit=%s ok=%s  %s' % (r['case'], r['verdict'], r['exit'], r['MUST_FAIL_ok'], r['code'][:120]))
