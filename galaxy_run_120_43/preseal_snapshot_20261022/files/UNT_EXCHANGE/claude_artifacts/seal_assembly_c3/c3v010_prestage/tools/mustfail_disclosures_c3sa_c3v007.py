# c3v007: the c3v016 contrast copies get the dispositions file of their own dry run (dry run 10's fixture); c3v006 gave them the target's
# (root's real 6a3fa535 since c3v024), which their env does not pin, so the four E1-xold contrasts refused for that reason, not the site.
# c3v006: S-8's draft is built inline (c3v005 crashed: draftvar was used before its definition).
# c3v005 (c3v010 near-final): S-8 isolates the A111 driver_check_record check on a copy of the TARGET draft (registry V010 makes the
# old c3v002 draft refuse earlier, at its producer_registry).
# c3v004 (c3v010 pre-stage): the draft and, while V003 is PENDING, the S27 stand-in V002 are taken from the target / generator c3v011.
# c3v003 (c3v009): re-pointed at the TARGET's own pins (DISCLOSURES V002, HELPER_SHA, the wired P13 line); generator c3v010 for c3v020.
# c3v002: H-4f is a real semantics control (the first character of the SAME text written as a \\u escape must PASS); c3v001's
# construction replaced that character, so it was never run.
# Claude3 (FROM_CODEX/0646 + 0647, A110/A111; c3v008 round): MUST_FAIL controls for
#  (H) helper c3v017 check-disclosures, the step-0 pre-check of root's SEAL_MANUAL_DISCLOSURES_V001.json: the four cases the coordinator
#      named (a wrong sha, a duplicate key, an empty e_r6_1_text, an e_r6_1_text one byte off from r6's basis.erratum_E_R6_1) plus every
#      strict-parse class and every form rule; each runs the helper CLI in its own isolated process, as the script calls it;
#  (S) the script itself, STEP 0 ONLY: the dry-run form of ROOT_SEAL_STEPS (generator make_dry_run c3v009, pass A substitutions, a fresh
#      scratch pass folder per case) with the step calls cut after step0_preflight, so nothing after step 0 runs and step 0 writes
#      nothing. It shows that the script refuses the same four disclosures cases, P13 (the real PENDING tool 4 v004 form), a stale A111
#      input, the superseded slot draft, a draft that is not the A111 record, and SA-C3-E1 (a non-final && operand); the SA-C3-E1 cases
#      also run on the c3v016 dry-run form (generator c3v008), where the same input PASSES step 0 (the defect reproduced).
# Every synthetic input is written under OUTDIR (open 'x'). Nothing outside OUTDIR is written. No launch; no protected path.
# usage: python3 -I -B mustfail_disclosures_c3sa_c3v001.py OUTDIR HELPER=SHA SCRIPT=SHA DRYRUN_DIR GEN=SHA OLD_SCRIPT=SHA OLD_GEN=SHA OLD_DRYRUN_DIR SHIM=SHA
import hashlib, json, os, re, subprocess, sys
OUT = sys.argv[1]
def pa(x):
    p, h = x.rsplit('=', 1); return p, h
(HP, HS), (SC, SCS) = pa(sys.argv[2]), pa(sys.argv[3]); DRY = sys.argv[4]; (GEN, GENS) = pa(sys.argv[5])
(OSC, OSCS), (OGEN, OGENS) = pa(sys.argv[6]), pa(sys.argv[7]); ODRY = sys.argv[8]; (SHIM, SHIMS) = pa(sys.argv[9])
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for p, h in ((HP, HS), (SC, SCS), (GEN, GENS), (OSC, OSCS), (OGEN, OGENS), (SHIM, SHIMS)):
    assert sha(p) == h, p
os.mkdir(OUT); PFX = OUT + '/NO_PYCACHE_PREFIX_EMPTY'; os.mkdir(PFX)
ENV = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1',
       'LANG': 'en_US.UTF-8', 'HOME': '/Users/bgm'}
def wx(name, data):
    p = OUT + '/' + name
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return p, sha(p)
# c3v003: the disclosures file, the helper sha and the P13 form are read from the TARGET script (c3v020 pins V002, A112)
_TT = open(SC, 'rb').read().decode('utf-8')
_DM = re.search(r'^DISCLOSURES="([^"]*)"; DISCLOSURES_SHA="([0-9a-f]{64})"$', _TT, re.M)
if _DM:
    DISC, DISCS = _DM.group(1).replace('$C3', C3, 1), _DM.group(2); _DLINE = _DM.group(0)
else:   # c3v004: the target's DISCLOSURES is the V003 PENDING placeholder: the copies carry the S27 stand-in V002 (generator c3v011)
    DISC, DISCS = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3'
    _DLINE = 'DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json"; DISCLOSURES_SHA="a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3"   # DRY RUN S27: STAND-IN (V003 PENDING)'
_DRM = re.search(r'^DRAFT="([^"]*)";\s+DRAFT_SHA="([0-9a-f]{64})"', _TT, re.M); _DRP = _DRM.group(1).replace('$C3', C3, 1)
R6F, R6FS, R6SCH = A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json', '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0', 'UNT_V007_SELECTED_PREREG_C4V001'
RB = open(DISC, 'rb').read(); assert hashlib.sha256(RB).hexdigest() == DISCS
D0 = json.loads(RB); E = D0['e_r6_1_text']
assert E == json.loads(open(R6F, 'rb').read())['basis']['erratum_E_R6_1'] and E.isascii() is not None
RES = []
def last_json(txt):
    for ln in reversed([x for x in txt.splitlines() if x.strip()]):
        try:
            return json.loads(ln)
        except Exception:
            continue
    return {}
# ------------------------------------------------------------------------------------------------ (H) helper check-disclosures
def hcase(cid, desc, path, psha, want, code_sub='', r6=(R6F, R6FS), schema=R6SCH):
    r = subprocess.run([PY, '-I', '-B', '-X', 'pycache_prefix=' + PFX, HP, 'check-disclosures', '--disclosures', path, '--disclosures-sha', psha,
                        '--r6-selected', r6[0], '--r6-selected-sha', r6[1], '--r6-schema', schema], capture_output=True, text=True, cwd='/', env=ENV)
    v = last_json(r.stderr)
    row = {'case': cid, 'level': 'helper', 'what': desc, 'want': want, 'want_code': code_sub, 'verdict': v.get('verdict', 'NO_VERDICT'), 'exit': r.returncode,
           'code': (v.get('code') or '')[:300]}
    row['ok'] = row['verdict'] == want and row['exit'] == (0 if want == 'PASS' else 2) and (want == 'PASS' or code_sub in row['code'])
    RES.append(row)
def dump(o):
    return json.dumps(o, indent=1, sort_keys=True) + '\n'
def var(name, **ch):
    o = json.loads(RB)
    for k, v in ch.items():
        o[k] = v
    return o
hcase('H-0', 'control: the real disclosures file b9db6fd1 against the real r6 SELECTED 7200acd9', DISC, DISCS, 'PASS')
# the four named cases
hcase('H-1', 'NAMED: the real file with a wrong sha (last hex digit changed)', DISC, DISCS[:-1] + ('7' if DISCS[-1] != '7' else '8'), 'REFUSE', 'PIN_BYTES_MISMATCH manual_disclosures')
p, h = wx('H2_duplicate_top_level_key.json', b'{"schema": "SEAL_MANUAL_DISCLOSURES_V001", ' + RB.lstrip()[1:]); hcase('H-2', 'NAMED: a duplicate key (schema twice at top level)', p, h, 'REFUSE', 'DISCLOSURES_DUPLICATE_KEY')
t = dump(json.loads(RB)); i = t.index('"new_item_id": "NEW-4"')
p, h = wx('H2b_duplicate_key_in_c08_row.json', t[:i] + '"new_item_id": "NEW-4",\n   ' + t[i:]); hcase('H-2b', 'NAMED: a duplicate key inside a c08_table row (new_item_id twice)', p, h, 'REFUSE', 'DISCLOSURES_DUPLICATE_KEY')
p, h = wx('H3_empty_e_r6_1_text.json', dump(var('', e_r6_1_text=''))); hcase('H-3', 'NAMED: an empty e_r6_1_text', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_EMPTY')
p, h = wx('H3b_whitespace_e_r6_1_text.json', dump(var('', e_r6_1_text=' \n\t'))); hcase('H-3b', 'an e_r6_1_text of whitespace only', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_EMPTY')
p, h = wx('H3c_null_e_r6_1_text.json', dump(var('', e_r6_1_text=None))); hcase('H-3c', 'an e_r6_1_text that is null', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_EMPTY')
last = E[-1]; sub = 'X' if last != 'X' else 'Y'
assert len((E[:-1] + sub).encode()) == len(E.encode()) and sum(a != b for a, b in zip((E[:-1] + sub).encode(), E.encode())) == 1
p, h = wx('H4a_one_byte_substituted.json', dump(var('', e_r6_1_text=E[:-1] + sub))); hcase('H-4a', 'NAMED: e_r6_1_text one byte off (its last byte substituted)', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL_TO_R6_SELECTED')
p, h = wx('H4b_one_byte_appended.json', dump(var('', e_r6_1_text=E + ' '))); hcase('H-4b', 'NAMED: e_r6_1_text one byte off (one space appended)', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL_TO_R6_SELECTED')
p, h = wx('H4c_one_byte_removed.json', dump(var('', e_r6_1_text=E[:-1]))); hcase('H-4c', 'NAMED: e_r6_1_text one byte off (its last byte removed)', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL_TO_R6_SELECTED')
p, h = wx('H4d_trailing_newline.json', dump(var('', e_r6_1_text=E + '\n'))); hcase('H-4d', 'e_r6_1_text with one trailing newline', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL_TO_R6_SELECTED')
j = E.find('-')
if j >= 0:
    p, h = wx('H4e_lookalike_hyphen.json', dump(var('', e_r6_1_text=E[:j] + '‐' + E[j + 1:]))); hcase('H-4e', 'e_r6_1_text with one ASCII hyphen replaced by the look-alike U+2010', p, h, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL_TO_R6_SELECTED')
t4f = dump(json.loads(RB)); old4f = '"e_r6_1_text": ' + json.dumps(E, sort_keys=True); assert t4f.count(old4f) == 1 and E[0].isascii() and E[0].isalnum()
p, h = wx('H4f_first_char_json_escaped.json', t4f.replace(old4f, '"e_r6_1_text": "\\u%04x' % ord(E[0]) + json.dumps(E)[2:], 1))
assert json.loads(open(p, 'rb').read())['e_r6_1_text'] == E and open(p, 'rb').read() != t4f.encode()
hcase('H-4f', 'control (semantics): the same e_r6_1_text value with its first character written as a JSON \\u escape; the comparison is on the decoded text, so this PASSES',
      p, h, 'PASS')
# strict-parse classes (the c3v013 SELECTED-strictness rules, typed DISCLOSURES_* codes)
p, h = wx('H5_bom.json', b'\xef\xbb\xbf' + RB); hcase('H-5', 'a UTF-8 BOM', p, h, 'REFUSE', 'DISCLOSURES_BOM')
k = RB.index(b'"c08_confirmation": "') + len(b'"c08_confirmation": "')
p, h = wx('H6_invalid_utf8.json', RB[:k] + b'\xff' + RB[k:]); hcase('H-6', 'one invalid UTF-8 byte inside c08_confirmation', p, h, 'REFUSE', 'DISCLOSURES_INVALID_UTF8')
m = re.search(rb'"line": (\d+)', RB)
p, h = wx('H7_nan.json', RB[:m.start(1)] + b'NaN' + RB[m.end(1):]); hcase('H-7', 'NaN as a c08 line', p, h, 'REFUSE', 'DISCLOSURES_NON_FINITE')
p, h = wx('H7b_overflow.json', RB[:m.start(1)] + b'1e400' + RB[m.end(1):]); hcase('H-7b', 'an overflowing float (1e400) as a c08 line', p, h, 'REFUSE', 'DISCLOSURES_NON_FINITE')
p, h = wx('H7c_long_int.json', RB[:m.start(1)] + b'1' * 4301 + RB[m.end(1):]); hcase('H-7c', 'a 4301-digit integer as a c08 line', p, h, 'REFUSE', 'DISCLOSURES_INTEGER_TOO_LONG')
p, h = wx('H8_trailing_text.json', RB + b'\n{}\n'); hcase('H-8', 'trailing text after the object', p, h, 'REFUSE', 'DISCLOSURES_NOT_STRICT_JSON')
p, h = wx('H9_top_level_array.json', b'[' + RB + b']'); hcase('H-9', 'a top-level array holding the object', p, h, 'REFUSE', 'DISCLOSURES_TOP_LEVEL_NOT_AN_OBJECT')
deep = json.loads(RB); deep['root_disclosures'][0]['text'] = 'x'
dt = dump(deep).replace('"text": "x"', '"text": ' + '[' * 70 + '"x"' + ']' * 70, 1)
p, h = wx('H9b_too_deep.json', dt); hcase('H-9b', 'JSON nested 70 deep inside a root disclosure', p, h, 'REFUSE', 'DISCLOSURES_JSON_TOO_DEEP')
# form rules
p, h = wx('H10_schema.json', dump(var('', schema='SEAL_MANUAL_DISCLOSURES_V002'))); hcase('H-10', 'another schema string', p, h, 'REFUSE', 'DISCLOSURES_SCHEMA')
o = json.loads(RB); del o['c08_confirmation']; p, h = wx('H11_missing_key.json', dump(o)); hcase('H-11', 'c08_confirmation missing', p, h, 'REFUSE', 'DISCLOSURES_KEYS')
p, h = wx('H12_extra_key.json', dump(var('', notes='x'))); hcase('H-12', 'an extra top-level key', p, h, 'REFUSE', 'DISCLOSURES_KEYS')
def rowvar(cid, desc, fn, code):
    o = json.loads(RB); fn(o); p, h = wx('%s.json' % cid.replace('-', '_'), dump(o)); hcase(cid, desc, p, h, 'REFUSE', code)
rowvar('H-13a', 'a c08 row with line 0', lambda o: o['c08_table'][0].__setitem__('line', 0), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-13b', 'a c08 row with line as a string', lambda o: o['c08_table'][0].__setitem__('line', str(o['c08_table'][0]['line'])), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-13c', 'a c08 row with line true', lambda o: o['c08_table'][0].__setitem__('line', True), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-13d', 'a c08 row without declared_in_r13', lambda o: o['c08_table'][0].pop('declared_in_r13'), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-13e', 'a c08 row with an extra key', lambda o: o['c08_table'][0].__setitem__('note', 'x'), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-13f', 'a c08 row id not NEW-<n>', lambda o: o['c08_table'][0].__setitem__('new_item_id', 'NEW-x'), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-13g', 'a c08 row with an empty file', lambda o: o['c08_table'][0].__setitem__('file', ''), 'DISCLOSURES_C08_ROW_FORM')
rowvar('H-14', 'two c08 rows with the same id', lambda o: o['c08_table'][1].__setitem__('new_item_id', o['c08_table'][0]['new_item_id']), 'DISCLOSURES_C08_DUPLICATE_ID')
rowvar('H-15', 'an empty c08_table', lambda o: o.__setitem__('c08_table', []), 'DISCLOSURES_C08_TABLE_EMPTY_OR_NOT_A_LIST')
rowvar('H-16', 'an empty c08_confirmation', lambda o: o.__setitem__('c08_confirmation', ''), 'DISCLOSURES_C08_CONFIRMATION_EMPTY')
rowvar('H-17a', 'a root disclosure without source', lambda o: o['root_disclosures'][0].pop('source'), 'DISCLOSURES_ROOT_DISCLOSURE_FORM')
rowvar('H-17b', 'a root disclosure with an empty text', lambda o: o['root_disclosures'][0].__setitem__('text', ' '), 'DISCLOSURES_ROOT_DISCLOSURE_FORM')
rowvar('H-17c', 'two root disclosures with the same id', lambda o: o['root_disclosures'][1].__setitem__('id', o['root_disclosures'][0]['id']), 'DISCLOSURES_ROOT_DISCLOSURE_DUPLICATE_ID')
rowvar('H-17d', 'an empty root_disclosures list', lambda o: o.__setitem__('root_disclosures', []), 'DISCLOSURES_ROOT_DISCLOSURES_EMPTY_OR_NOT_A_LIST')
os.symlink(DISC, OUT + '/H18_symlink_to_the_real_file.json')
hcase('H-18', 'the real file reached through a symlink (refused at the link)', OUT + '/H18_symlink_to_the_real_file.json', DISCS, 'REFUSE', 'SYMLINK')
hcase('H-19', 'the r6 SELECTED file with a wrong sha', DISC, DISCS, 'REFUSE', 'PIN_BYTES_MISMATCH r6_selected', r6=(R6F, R6FS[:-1] + ('0' if R6FS[-1] != '0' else '1')))
hcase('H-20', 'the r6 SELECTED file under another schema string', DISC, DISCS, 'REFUSE', 'R6_SELECTED_SCHEMA_MISMATCH', schema='UNT_V007_SELECTED_PREREG_C4V002')
r6o = json.loads(open(R6F, 'rb').read()); r6o['basis']['erratum_E_R6_1'] = E + ' '
p6, h6 = wx('H21_r6_selected_with_other_erratum.json', json.dumps(r6o, indent=1) + '\n')
hcase('H-21', 'a synthetic r6 SELECTED whose erratum differs by one byte (the disclosures file unchanged)', DISC, DISCS, 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL', r6=(p6, h6))
# ------------------------------------------------------------------------------------------- (S) the script, step 0 only
FIXT = DRY + '/fixtures'; MAN = FIXT + '/MANIFEST_GATES_ONLY_STANDIN.json'; MANS = sha(MAN)
BIN = DRY + '/passA/scratch_pkt/bind_sealed_launch_plan_cx1v001.py'; assert sha(BIN) == 'f3e4e2beeb8f1cb151892fd903b889c471cea58fea1b67c72552137d037575ca'
DSP = DRY + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json'
def run_env(run_file, v_dir):
    env = dict(ENV)
    for ln in open(run_file).read().splitlines():
        m = re.match(r'export (\w+)=("([^"]*)"|(\S+))', ln)
        if m:
            env[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(4)
    env['UNT_SEAL_DISPOSITIONS_PATH'] = v_dir + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json'
    return env
def mkpass(name, gen, root, root_sha, fixt=FIXT, man=MAN, mans=MANS, dsp=DSP):
    V = OUT + '/s_' + name
    for d in ('', '/scratch_ctrl', '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS', '/scratch_pkt', '/scratch_pkt/P128', '/scratch_internal'):
        os.mkdir(V + d)
    with open(V + '/scratch_pkt/bind_sealed_launch_plan_cx1v001.py', 'xb') as f:
        f.write(open(BIN, 'rb').read())
    with open(V + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json', 'xb') as f:
        f.write(open(dsp, 'rb').read())   # c3v007: the dispositions copy of the dry run that matches the copy's own env
    r = subprocess.run([PY, '-I', '-B', gen, root, root_sha, V, 'A', fixt, man, mans, SHIM], capture_output=True, text=True, cwd='/', env=ENV)
    assert r.returncode == 0, r.stderr[-500:]
    return V
def scase(cid, desc, want, code_sub, edits=(), env_set=None, env_drop=(), old=False):
    V = mkpass(cid.replace('-', '_'), OGEN if old else GEN, OSC if old else SC, OSCS if old else SCS, *( (ODRY + '/fixtures', ODRY + '/fixtures/MANIFEST_GATES_ONLY_STANDIN.json', sha(ODRY + '/fixtures/MANIFEST_GATES_ONLY_STANDIN.json'), ODRY + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json') if old else ()))
    s = open(V + '/ROOT_SEAL_STEPS_DRYRUN_A.sh').read()
    for o, n in edits:
        assert s.count(o) == 1, (cid, o[:80], s.count(o))
        s = s.replace(o, n)
    i = s.index('step0_preflight\nstep1_freeze\n')
    s = s[:i] + 'step0_preflight\necho "STEP0_ONLY: preflight passed (MUST_FAIL harness; no later step runs)"\n'
    sp = V + '/STEP0_ONLY_%s.sh' % cid.replace('-', '_')
    with open(sp, 'x') as f:
        f.write(s)
    env = run_env((ODRY if old else DRY) + '/passA/RUN_A.sh', V)
    for k in env_drop:
        env.pop(k, None)
    env.update(env_set or {})
    r = subprocess.run(['/bin/bash', sp], capture_output=True, text=True, cwd='/', env=env)
    passed = r.returncode == 0 and 'STEP0_ONLY: preflight passed' in r.stdout
    stopped = r.returncode != 0 and 'STOPPED at step 0' in r.stderr
    code = ''
    for ln in r.stderr.splitlines():
        if ln.startswith('REFUSE:'):
            code = ln; break
        if '"verdict": "REFUSE"' in ln:
            code = (last_json(ln).get('code') or ln)[:300]; break
    row = {'case': cid, 'level': 'script step 0' + (' (c3v016 contrast)' if old else ''), 'what': desc, 'want': want, 'want_code': code_sub,
           'verdict': 'PASS' if passed else ('REFUSE' if stopped else 'OTHER'), 'exit': r.returncode, 'code': code[:300],
           'wrote_nothing_beyond_the_harness': sorted(os.listdir(V)) == sorted(['scratch_ctrl', 'scratch_pkt', 'scratch_internal', 'ROOT_SEAL_STEPS_DRYRUN_A.sh', 'SUBSTITUTIONS_A.json', os.path.basename(sp)])
                                                and os.listdir(V + '/scratch_internal') == [] and os.listdir(V + '/scratch_pkt/P128') == []}
    row['ok'] = row['verdict'] == want and (want == 'PASS' or code_sub in row['code']) and row['wrote_nothing_beyond_the_harness']
    if row['verdict'] == 'OTHER':
        row['stderr_tail'] = r.stderr[-400:]
    RES.append(row)
DL = _DLINE
def dl(p, h):
    return [(DL, 'DISCLOSURES="%s"; DISCLOSURES_SHA="%s"' % (p, h))]
scase('S-0', 'control: c3v019 dry-run form (S24/S25 stand-in), step 0 with the real disclosures file', 'PASS', '')
scase('S-1', 'NAMED: the real disclosures file with a wrong DISCLOSURES_SHA', 'REFUSE', 'PIN_BYTES_MISMATCH manual_disclosures', dl(DISC, DISCS[:-1] + ('7' if DISCS[-1] != '7' else '8')))
scase('S-2', 'NAMED: a disclosures file with a duplicate key', 'REFUSE', 'DISCLOSURES_DUPLICATE_KEY', dl(*[(OUT + '/H2_duplicate_top_level_key.json', sha(OUT + '/H2_duplicate_top_level_key.json'))][0]))
scase('S-3', 'NAMED: a disclosures file with an empty e_r6_1_text', 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_EMPTY', dl(OUT + '/H3_empty_e_r6_1_text.json', sha(OUT + '/H3_empty_e_r6_1_text.json')))
scase('S-4', 'NAMED: a disclosures file whose e_r6_1_text is one byte off', 'REFUSE', 'DISCLOSURES_E_R6_1_TEXT_NOT_BYTE_EQUAL', dl(OUT + '/H4a_one_byte_substituted.json', sha(OUT + '/H4a_one_byte_substituted.json')))
_V4L = re.search(r'^V004_SELECTED="[^"]*"; V004_SELECTED_SHA="[^"]*"; V004_SELECTED_SCHEMA="[^"]*"$', _TT, re.M).group(0)
scase('S-5', 'P13: the wired v004 SELECTED pin put back to PENDING: step 0 refuses', 'REFUSE', 'a PINS value is still PENDING',
      [(_V4L, 'V004_SELECTED="PENDING_SEAL_TOOLS_V004_SELECTED_FILE (Claude4, A110)"; V004_SELECTED_SHA="PENDING"; V004_SELECTED_SCHEMA="PENDING"')])
scase('S-6', 'a stale A111 input: UNT_SEAL_RULING_EPS_NGC still set', 'REFUSE', 'UNT_SEAL_RULING_EPS_NGC is no longer an input', env_set={'UNT_SEAL_RULING_EPS_NGC': '1d5eef1b602d2489ba8c0e652156555bbd2bfddf083931c7c4c82fa0a1e0c13d'})
scase('S-7', 'a stale A111 input: UNT_SEAL_DRIVER_CHECK_RECORD_PATH still set', 'REFUSE', 'UNT_SEAL_DRIVER_CHECK_RECORD_PATH is no longer an input', env_set={'UNT_SEAL_DRIVER_CHECK_RECORD_PATH': A + '/tail_scheme_impl_c2/driver_r5/check/CHECK.md'})
DRL = _DRM.group(0)
def dr(p, h):
    return [(DRL, 'DRAFT="%s";              DRAFT_SHA="%s"' % (p, h))]
_OLDMARK = json.loads(open(C3 + '/SLOT_VALUES_DRAFT_c3v002.json', 'rb').read())['driver_check_record']['sha256']
def _s8_draft():   # c3v006: built inline (c3v005 called draftvar before its definition)
    o = json.loads(open(_DRP, 'rb').read()); o['driver_check_record']['sha256'] = _OLDMARK
    return wx('DRAFT_DRIVER_CHECK_RECORD_OLD_MARKER.json', json.dumps(o, indent=1) + '\n')
scase('S-8', 'the target draft with its driver_check_record back at the c3v002 PENDING_ROOT_RULING marker (A111 check isolated)', 'REFUSE', "the slot draft's driver_check_record is not the A111 record",
      dr(*_s8_draft()))
D3 = json.loads(open(_DRP, 'rb').read())
def draftvar(name, fn, base=_DRP):
    o = json.loads(open(base, 'rb').read()); fn(o); return wx(name, json.dumps(o, indent=1) + '\n')
p, h = draftvar('DRAFT_EPS_NGC_OTHER_SHA.json', lambda o: o['certificates']['EPS_NGC'].__setitem__('sha256', o['certificates']['LO_NGC']['sha256']))
scase('S-9', 'a slot draft whose EPS_NGC sha is not the A111 record', 'REFUSE', "the slot draft's certificates.EPS_NGC is not the A111 record", dr(p, h))
# SA-C3-E1: a non-final && operand; c3v019 refuses, the c3v016 form (generator c3v008, dry run 10 env) passes step 0
HL = re.search(r'HELPER_SHA="[0-9a-f]{64}"', _TT).group(0)
OHL = 'HELPER_SHA="21f0eb09e927722237459d65cf60eae79d92acf4c6a25bb4340f1519e66d28c0"'
scase('E1-1', 'SA-C3-E1: HELPER_SHA wrong (the first && operand of the helper/runner check)', 'REFUSE', 'the helper or runner bytes differ', [(HL, 'HELPER_SHA="%s"' % ('0' * 64))])
scase('E1-1old', 'SA-C3-E1 reproduced on the c3v016 form: the same wrong HELPER_SHA PASSES step 0', 'PASS', '', [(OHL, 'HELPER_SHA="%s"' % ('0' * 64))], old=True)
p, h = draftvar('DRAFT_DRIVER_PATH_OTHER.json', lambda o: o['driver'].__setitem__('path', o['driver']['path'] + '_NOT_THE_DRIVER'))
scase('E1-2', "SA-C3-E1: a draft whose driver.path is not DRIVER (sha unchanged)", 'REFUSE', "the slot draft's driver is not DRIVER", dr(p, h))
OD2 = C3 + '/SLOT_VALUES_DRAFT_c3v002.json'
ODRL = 'DRAFT="$C3/SLOT_VALUES_DRAFT_c3v002.json";              DRAFT_SHA="02d97c376ddf231ec9e9643e21b88e57669719e9bb3687c2e8b6f30eec711e7f"'
p, h = draftvar('OLD_DRAFT_DRIVER_PATH_OTHER.json', lambda o: o['driver'].__setitem__('path', o['driver']['path'] + '_NOT_THE_DRIVER'), base=OD2)
scase('E1-2old', 'SA-C3-E1 reproduced on c3v016: the same driver.path change PASSES step 0', 'PASS', '', [(ODRL, 'DRAFT="%s";              DRAFT_SHA="%s"' % (p, h))], old=True)
p, h = draftvar('DRAFT_LAUNCHER_PATH_OTHER.json', lambda o: o['admission_entry']['launcher'].__setitem__('path', o['admission_entry']['launcher']['path'] + '_NOT_IT'))
scase('E1-3', 'SA-C3-E1: a draft whose admission_entry.launcher.path is not LAUNCHER', 'REFUSE', "the slot draft's admission_entry is not LAUNCHER and GUARD", dr(p, h))
p, h = draftvar('OLD_DRAFT_LAUNCHER_PATH_OTHER.json', lambda o: o['admission_entry']['launcher'].__setitem__('path', o['admission_entry']['launcher']['path'] + '_NOT_IT'), base=OD2)
scase('E1-3old', 'SA-C3-E1 reproduced on c3v016: the same launcher.path change PASSES step 0', 'PASS', '', [(ODRL, 'DRAFT="%s";              DRAFT_SHA="%s"' % (p, h))], old=True)
p, h = draftvar('DRAFT_Z2_OTHER_SHA.json', lambda o: o['identity_gate_records']['Z2'].__setitem__('sha256', 'f' * 64))
scase('E1-4', 'SA-C3-E1: a draft whose identity_gate_records.Z2 sha is not IDREC_Z2', 'REFUSE', "the slot draft's identity_gate_records are not", dr(p, h))
p, h = draftvar('OLD_DRAFT_Z2_OTHER_SHA.json', lambda o: o['identity_gate_records']['Z2'].__setitem__('sha256', 'f' * 64), base=OD2)
scase('E1-4old', 'SA-C3-E1 reproduced on c3v016: the same Z2 sha change PASSES step 0', 'PASS', '', [(ODRL, 'DRAFT="%s";              DRAFT_SHA="%s"' % (p, h))], old=True)
res = {'schema': 'C3SA_MUSTFAIL_DISCLOSURES_V001', 'helper': {'path': HP, 'sha256': HS}, 'script': {'path': SC, 'sha256': SCS}, 'generator': {'path': GEN, 'sha256': GENS},
       'contrast_script': {'path': OSC, 'sha256': OSCS}, 'contrast_generator': {'path': OGEN, 'sha256': OGENS}, 'shim': {'path': SHIM, 'sha256': SHIMS},
       'dry_run_dir': DRY, 'contrast_dry_run_dir': ODRY, 'disclosures': {'path': DISC, 'sha256': DISCS}, 'r6_selected': {'path': R6F, 'sha256': R6FS},
       'scope': 'form and the E_R6_1 byte equality only; the content is not cross-checked against the A-entries (coordinator)',
       'pycache_prefix_entries': len(os.listdir(PFX)), 'cases': RES, 'n': len(RES), 'n_ok': sum(r['ok'] for r in RES)}
res['all_ok'] = res['n_ok'] == res['n'] and res['pycache_prefix_entries'] == 0
with open(OUT + '/MUSTFAIL_DISCLOSURES_RESULTS_C3SA.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
for r in RES:
    print('%-8s ok=%s want=%s got=%s exit=%s %s' % (r['case'], r['ok'], r['want'], r['verdict'], r['exit'], r['code'][:110]))
print('ALL_OK' if res['all_ok'] else 'SOME_FAIL', '%d/%d' % (res['n_ok'], res['n']))
