# Claude3 (c3v009): MUST_FAIL controls for R-02 (SELECTED_SEAL_TOOLS_V004_C4V001 593c59fa basis.for_the_seal_script) and root A112 (0648).
#  (R) helper c3v019 check-seal-record-disclosures on the REAL SEAL_RECORDs written by the c3v020 dry runs (read only) and on synthetic
#      copies of them under OUTDIR, one edit each: R-02's four bypasses (manual_disclosures removed; set to null; a wrong e_r6_1_text; a
#      raw_text that no longer hashes to the pin) plus the pin, a record carrying V001, the content, the form, the schema and strictness;
#  (A) the script itself (a COPY of ROOT_SEAL_STEPS_c3v020.sh in its dry-run form, generator c3v010, a fresh scratch pass folder per
#      case, the step calls cut after step 11): V002 control (step 11 PASS); V001 as the disclosures pin (refused in step 0); V001 given
#      to tool 4 at step 10 while the pin stays V002 (tool 4 builds, step 11 refuses). Step 9 stays the published stub (S15).
# Nothing outside OUTDIR is written. No launch; no protected path.
# usage: python3 -I -B mustfail_r02_a112_c3sa_c3v001.py OUTDIR HELPER=SHA SCRIPT=SHA DRYRUN_DIR
import hashlib, json, os, re, subprocess, sys
OUT = sys.argv[1]
def pa(x):
    p, h = x.rsplit('=', 1); return p, h
(HP, HS), (SC, SCS) = pa(sys.argv[2]), pa(sys.argv[3]); DRY = sys.argv[4]
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'; W = C3 + '/c3v009_prestage'
GEN, GENS = W + '/tools/make_dry_run_c3sa_c3v010.py', 'ab01df672987408cb18954db79698da8051097d1fd6d8ddcc66522e028fedf4c'
SHIM, SHIMS = C3 + '/tools/dryrun_tool_shim_c3sa_c3v007.py', 'df19ac11401d76593f3b7a03474a31c955a77ec5585475e2a5bc9588027fd135'
D1, D1S = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json', 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6'
D2, D2S = C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3'
R6, R6S, R6C = A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json', '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0', 'UNT_V007_SELECTED_PREREG_C4V001'
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for p, h in ((HP, HS), (SC, SCS), (GEN, GENS), (SHIM, SHIMS), (D1, D1S), (D2, D2S), (R6, R6S)):
    assert sha(p) == h, p
os.mkdir(OUT); PFX = OUT + '/NO_PYCACHE_PREFIX_EMPTY'; os.mkdir(PFX)
ENV = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1',
       'LANG': 'en_US.UTF-8', 'HOME': '/Users/bgm'}
def wx(name, data):
    p = OUT + '/' + name
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return p, sha(p)
RES = []
def last_json(t):
    for ln in reversed([x for x in t.splitlines() if x.strip()]):
        try:
            return json.loads(ln)
        except Exception:
            continue
    return {}
RA = DRY + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json'; RB_ = DRY + '/passB/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json'
REC = json.loads(open(RA, 'rb').read()); assert REC['schema'] == 'UNT_V007_SEAL_RECORD_C4V004' and REC['manual_disclosures']['pin'] == {'path': D2, 'sha256': D2S}
DB2, DB1 = open(D2, 'rb').read(), open(D1, 'rb').read()
def hcase(cid, desc, rec_path, rec_sha, want, code='', r6=(R6, R6S, R6C), dpin=(D2, D2S), key='manual_disclosures', form='pin_content_raw_text', schema='UNT_V007_SEAL_RECORD_C4V004'):
    argv = [PY, '-I', '-B', '-X', 'pycache_prefix=' + PFX, HP, 'check-seal-record-disclosures', '--seal', rec_path, '--seal-sha', rec_sha, '--disclosures', dpin[0],
            '--disclosures-sha', dpin[1], '--key-path', key, '--form', form, '--record-schema', schema]
    if r6:
        argv += ['--r6-selected', r6[0], '--r6-selected-sha', r6[1], '--r6-schema', r6[2]]
    r = subprocess.run(argv, capture_output=True, text=True, cwd='/', env=ENV)
    v = last_json(r.stderr)
    row = {'case': cid, 'level': 'helper', 'what': desc, 'want': want, 'want_code': code, 'verdict': v.get('verdict', 'NO_VERDICT'), 'exit': r.returncode, 'code': (v.get('code') or '')[:300]}
    row['ok'] = row['verdict'] == want and row['exit'] == (0 if want == 'PASS' else 2) and (want == 'PASS' or code in row['code'])
    RES.append(row)
def synth(cid, fn, raw=None):
    rec = json.loads(json.dumps(REC)); fn(rec)
    return wx('%s_SYNTHETIC_SEAL_RECORD.json' % cid.replace('-', '_'), raw if raw is not None else json.dumps(rec, indent=1, sort_keys=True) + '\n')
hcase('R02-0', 'control: the REAL written SEAL_RECORD of dry-run pass A', RA, sha(RA), 'PASS')
hcase('R02-0b', 'control: the REAL written SEAL_RECORD of dry-run pass B', RB_, sha(RB_), 'PASS')
hcase('R02-1', 'R-02 bypass 1: manual_disclosures removed', *synth('R02-1', lambda r: r.pop('manual_disclosures')), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_KEY_PATH_MISSING')
hcase('R02-2', 'R-02 bypass 2: manual_disclosures set to null', *synth('R02-2', lambda r: r.__setitem__('manual_disclosures', None)), 'REFUSE', "SEAL_RECORD_DISCLOSURES_FORM_KEYS 'NoneType'")
def wrong_e(r):
    e = r['manual_disclosures']['content']['e_r6_1_text']; r['manual_disclosures']['content']['e_r6_1_text'] = e[:-1] + ('X' if e[-1] != 'X' else 'Y')
hcase('R02-3', 'R-02 bypass 3: a wrong content.e_r6_1_text (one byte off; raw_text and pin unchanged)', *synth('R02-3', wrong_e), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_E_R6_1_NOT_THE_R6_ERRATUM')
hcase('R02-4', 'R-02 bypass 4: a raw_text that no longer hashes to the pin (one byte off)', *synth('R02-4', lambda r: r['manual_disclosures'].__setitem__('raw_text', r['manual_disclosures']['raw_text'].replace('C-08', 'C-09', 1))), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_RAW_TEXT_NOT_THE_FILE_BYTES')
hcase('R02-4b', 'raw_text without its final newline', *synth('R02-4b', lambda r: r['manual_disclosures'].__setitem__('raw_text', r['manual_disclosures']['raw_text'][:-1])), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_RAW_TEXT_NOT_THE_FILE_BYTES')
hcase('R02-5', 'the pin sha changed to V001 (raw_text still V002)', *synth('R02-5', lambda r: r['manual_disclosures']['pin'].__setitem__('sha256', D1S)), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_PIN')
hcase('R02-5b', 'the pin path changed to V001 (raw_text still V002)', *synth('R02-5b', lambda r: r['manual_disclosures']['pin'].__setitem__('path', D1)), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_PIN')
def as_v001(r):
    r['manual_disclosures'] = {'pin': {'path': D1, 'sha256': D1S}, 'content': json.loads(DB1), 'raw_text': DB1.decode('utf-8')}
hcase('R02-6', 'A112: a record that consistently carries V001 (pin, content and raw_text all V001)', *synth('R02-6', as_v001), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_RAW_TEXT_NOT_THE_FILE_BYTES')
hcase('R02-7', 'content without the A106_2_SRR13_CHECK_SPLIT row (raw_text, pin and e_r6_1_text intact)', *synth('R02-7', lambda r: r['manual_disclosures']['content'].__setitem__('root_disclosures', [x for x in r['manual_disclosures']['content']['root_disclosures'] if x['id'] != 'A106_2_SRR13_CHECK_SPLIT'])), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_CONTENT_NOT_THE_FILE')
def booltype(r):
    row = r['manual_disclosures']['content']['c08_table'][0]; row['declared_in_r13'] = 1 if row['declared_in_r13'] is True else 0
hcase('R02-8', 'content with one bool turned into an int (type-exact)', *synth('R02-8', booltype), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_CONTENT_NOT_THE_FILE')
hcase('R02-9', 'manual_disclosures with an extra key', *synth('R02-9', lambda r: r['manual_disclosures'].__setitem__('note', 'x')), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_FORM_KEYS')
hcase('R02-10', 'the record schema of v003 (UNT_V007_SEAL_RECORD_C4V003)', *synth('R02-10', lambda r: r.__setitem__('schema', 'UNT_V007_SEAL_RECORD_C4V003')), 'REFUSE', 'SEAL_RECORD_SCHEMA')
t = json.dumps(REC, indent=1, sort_keys=True)
hcase('R02-11', 'a duplicate manual_disclosures key (a V001 copy first; strict parse)', *synth('R02-11', lambda r: None, raw='{"manual_disclosures": null, ' + t.lstrip()[1:] + '\n'), 'REFUSE', 'SEAL_RECORD_DUPLICATE_KEY')
hcase('R02-12', 'the R-02 form without the r6 SELECTED file', RA, sha(RA), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_NEEDS_THE_R6_SELECTED_FILE', r6=None)
hcase('R02-13', 'the r6 SELECTED file with a wrong sha', RA, sha(RA), 'REFUSE', 'PIN_BYTES_MISMATCH r6_selected', r6=(R6, R6S[:-1] + ('0' if R6S[-1] != '0' else '1'), R6C))
r6o = json.loads(open(R6, 'rb').read()); r6o['basis']['erratum_E_R6_1'] = r6o['basis']['erratum_E_R6_1'] + ' '
p6, h6 = wx('R02_14_SYNTHETIC_R6_SELECTED.json', json.dumps(r6o, indent=1) + '\n')
hcase('R02-14', 'a synthetic r6 SELECTED whose erratum differs by one byte (the record unchanged)', RA, sha(RA), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_E_R6_1_NOT_THE_R6_ERRATUM', r6=(p6, h6, R6C))
hcase('R02-15', 'the REAL record checked against V001 as the pinned file (A112)', RA, sha(RA), 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_RAW_TEXT_NOT_THE_FILE_BYTES', dpin=(D1, D1S))
# ------------------------------------------------------------------------------------------- (A) the script copy, steps 0..11
def run_env(run_file, v):
    env = dict(ENV)
    for ln in open(run_file).read().splitlines():
        m = re.match(r'export (\w+)=("([^"]*)"|(\S+))', ln)
        if m:
            env[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(4)
    env['UNT_SEAL_DISPOSITIONS_PATH'] = v + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json'
    return env
KEEP = ['step0_preflight', 'step1_freeze', 'step2_tool1', 'step2a_driver_build', 'step3_bind', 'step3a_fill', 'step3b_c04', 'step4_sealed_prereg', 'step4a_tool3',
        'step5_sealed_compare', 'step5a_tool2', 'step8_gates_only', 'step9_validity_c5h', 'step10_tool4', 'step11_seal_record']
def scase(cid, desc, edits, want, code_sub, want_step):
    v = OUT + '/s_' + cid.replace('-', '_')
    for d in ('', '/scratch_ctrl', '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS', '/scratch_pkt', '/scratch_pkt/P128', '/scratch_internal'):
        os.mkdir(v + d)
    for src, dst in ((DRY + '/passA/scratch_pkt/bind_sealed_launch_plan_cx1v001.py', v + '/scratch_pkt/bind_sealed_launch_plan_cx1v001.py'),
                     (DRY + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json', v + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json')):
        with open(dst, 'xb') as f:
            f.write(open(src, 'rb').read())
    man = DRY + '/fixtures/MANIFEST_GATES_ONLY_STANDIN.json'
    r = subprocess.run([PY, '-I', '-B', GEN, SC, SCS, v, 'A', DRY + '/fixtures', man, sha(man), SHIM], capture_output=True, text=True, cwd='/', env=ENV)
    assert r.returncode == 0, r.stderr[-400:]
    s = open(v + '/ROOT_SEAL_STEPS_DRYRUN_A.sh').read()
    for o, n in edits:
        assert s.count(o) == 1, (cid, o[:80], s.count(o)); s = s.replace(o, n)
    k = s.index('step0_preflight\nstep1_freeze\n')
    s = s[:k] + '\n'.join(KEEP) + '\necho "COPY_END: steps 0 to 11 ran"\n'
    cp = v + '/COPY_%s.sh' % cid.replace('-', '_')
    with open(cp, 'x') as f:
        f.write(s)
    r = subprocess.run(['/bin/bash', cp], capture_output=True, text=True, cwd='/', env=run_env(DRY + '/passA/RUN_A.sh', v))
    with open(v + '/RUN.stdout.txt', 'x') as f:
        f.write(r.stdout)
    with open(v + '/RUN.stderr.txt', 'x') as f:
        f.write(r.stderr)
    m = re.search(r'STOPPED at step (\S+) ', r.stderr)
    code = next((ln for ln in r.stderr.splitlines() if ln.startswith('REFUSE:')), '')
    if not code:
        for ln in r.stderr.splitlines():
            if '"verdict": "REFUSE"' in ln:
                code = (last_json(ln).get('code') or ln)[:300]; break
    lg = v + '/scratch_ctrl/V007_SEAL_ASSEMBLY/logs/STEP_11_DISCLOSURES_VERBATIM.json'
    if not code and os.path.exists(lg) and '"REFUSE"' in open(lg).read():
        code = json.loads(open(lg).read()).get('code', '')
    row = {'case': cid, 'level': 'script copy, steps 0-11', 'what': desc, 'want': want, 'want_code': code_sub, 'want_step': want_step, 'exit': r.returncode,
           'stopped_at_step': m.group(1) if m else None, 'copy_end_reached': 'COPY_END' in r.stdout, 'code': code[:300],
           'step10_tool4_ran': 'PASS  STEP_10_TOOL4_CHECK' in r.stdout or os.path.exists(v + '/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_CANDIDATE_TOOL4.stdout.json'),
           'step11_log': json.loads(open(lg).read()).get('verdict') if os.path.exists(lg) else None, 'copy': {'path': cp, 'sha256': sha(cp)}}
    if want == 'PASS':
        row['ok'] = r.returncode == 0 and row['copy_end_reached'] and row['step11_log'] == 'PASS'
    else:
        row['ok'] = r.returncode != 0 and row['stopped_at_step'] == want_step and code_sub in row['code'] and not row['copy_end_reached']
    RES.append(row)
DLINE = 'DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json"; DISCLOSURES_SHA="%s"' % D2S
FLAGS = '--manual-disclosures "$DISCLOSURES" --manual-disclosures-sha256 "$DISCLOSURES_SHA"'
scase('A112-0', 'control: the c3v020 copy with V002 runs steps 0 to 11; step 11 (R-02) PASSES', [], 'PASS', '', None)
scase('A112-1', 'A112: V001 (path and sha) as the disclosures pin: refused in step 0 (superseded)', [(DLINE, 'DISCLOSURES="%s"; DISCLOSURES_SHA="%s"' % (D1, D1S))], 'REFUSE', 'REFUSE: the disclosures file is a superseded version', '0')
scase('A112-2', 'A112: tool 4 run with V001 path and sha at step 10 while the pin stays V002: tool 4 builds; step 11 (R-02) refuses', [(FLAGS, '--manual-disclosures "%s" --manual-disclosures-sha256 "%s"' % (D1, D1S))], 'REFUSE', 'SEAL_RECORD_DISCLOSURES_R02_RAW_TEXT_NOT_THE_FILE_BYTES', '11')
res = {'schema': 'C3SA_MUSTFAIL_R02_A112_V001', 'helper': {'path': HP, 'sha256': HS}, 'script': {'path': SC, 'sha256': SCS}, 'dry_run_dir': DRY,
       'generator': {'path': GEN, 'sha256': GENS}, 'disclosures_v002': {'path': D2, 'sha256': D2S}, 'disclosures_v001_superseded': {'path': D1, 'sha256': D1S},
       'cases': RES, 'n': len(RES), 'n_ok': sum(r['ok'] for r in RES), 'pycache_prefix_entries': len(os.listdir(PFX))}
res['all_ok'] = res['n_ok'] == res['n'] and res['pycache_prefix_entries'] == 0
with open(OUT + '/MUSTFAIL_R02_A112_RESULTS_C3SA.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
for r in RES:
    print('%-7s ok=%s want=%s got=%s exit=%s step=%s %s' % (r['case'], r['ok'], r['want'], r.get('verdict', r.get('step11_log')), r['exit'], r.get('stopped_at_step'), r['code'][:110]))
print('ALL_OK' if res['all_ok'] else 'SOME_FAIL', '%d/%d' % (res['n_ok'], res['n']))
