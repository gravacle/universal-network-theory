# Claude3 (c3v009, from mustfail_v003_c3sa_c3v001.py 707747ef): the same controls on the REAL seal tools v004 of record (SELECTED_SEAL_TOOLS_V004_C4V001
# 593c59fa: all five tools from seal_tools_v004; tool 4 build_seal_record_c4v004.py 9787cf58), the v004 SELECTED roles, the c3v020 dry run's
# outputs, plus A4 (tool 4 v004 admission refuses a v003-schema SEAL_RECORD). Base description:
# Claude3 (WIRE v003): MUST_FAIL controls on the REAL seal tools v003 (run from verified bytes through the pinned-source runner, each in its
# own isolated process) and on helper c3v016's v003 paths. Inputs: the real r6, its addendum copy, the closed V005, and dry run 17's
# pass-A outputs (read only). Every edited input is a synthetic copy under OUTDIR (open 'x').
# usage: python3 -I -B mustfail_v004_c3sa_c3v001.py OUTDIR HELPER=SHA RUNNER=SHA DRYRUN_DIR
import hashlib, json, os, subprocess, sys
OUT, HS, RS, DRY = sys.argv[1:5]
HP, HSHA = HS.rsplit('=', 1); RP, RSHA = RS.rsplit('=', 1)
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; V = A + '/v007_final_prereg_c4/seal_tools_v004'
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
assert sha(HP) == HSHA and sha(RP) == RSHA
T = {n: V + '/' + f for n, f in (('C', 'seal_common_c4v003.py'), ('T1', 'check_frozen_addendum_c4v003.py'), ('T2', 'check_sealed_compare_c4v003.py'),
                                  ('T3', 'check_slot_fill_c4v003.py'), ('T4', 'build_seal_record_c4v004.py'), ('T5', 'print_driver_build_record_c4v003.py'))}
WANT = {'C': '101a3aeb9846a21c35993e8e7e4b50a8f1206ed4202b131afd12d7e496c5ab21', 'T1': 'a56f8d793750151920b1b47e77b46aebbfadea71fe77730f360beb02af788fb4',
        'T2': 'c2c5dfc5ddba1e44ff82811a38d4c05b0a669f2294b229efe3437623d596f9f1', 'T3': '316973a1abf5aa2151dc1a517733d970ce1004313395d05fe590f82ed439b0af',
        'T4': '9787cf587ca3e9a92c24587a9c5ea56568b808f53c48acf739eea71b997ceb41', 'T5': 'e5bedffe3c91650d5dba7fbd1ed5476e228158679d8959dfea0e2eff436ebdea'}
for k in T:
    assert sha(T[k]) == WANT[k], k
os.mkdir(OUT); PFX = OUT + '/NO_PYCACHE_PREFIX_EMPTY'; os.mkdir(PFX)
ENV = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}
def mod(n, k):
    return ['--module', '%s=%s=%s' % (n, T[k], WANT[k])]
def tool(k, argv):
    m = mod('seal_common_c4v003', 'C')
    if k == 'T4':
        m += mod('check_frozen_addendum_c4v003', 'T1') + mod('check_sealed_compare_c4v003', 'T2') + mod('check_slot_fill_c4v003', 'T3')
    return [PY, '-I', '-B', '-X', 'pycache_prefix=' + PFX, RP] + m + ['--main', '%s=%s' % (T[k], WANT[k]), '--call', 'main', '--'] + argv
def helper(argv):
    return [PY, '-I', '-B', '-X', 'pycache_prefix=' + PFX, HP] + argv
RES = []
def case(cid, desc, cmd, want, verdict_from='stdout', kind='MUST_FAIL'):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd='/', env=ENV)
    txt = r.stdout if verdict_from == 'stdout' else r.stderr
    try:
        v = json.loads(txt.strip().splitlines()[-1]) if verdict_from == 'stderr' else json.loads(txt)
    except Exception:
        v = {'verdict': 'NO_VERDICT'}
    codes = [f.get('code') for f in v.get('failures', [])] if isinstance(v.get('failures'), list) else ([v.get('code')] if v.get('code') else [])
    row = {'case': cid, 'what': desc, 'kind': kind, 'want': want, 'verdict': v.get('verdict'), 'exit': r.returncode, 'codes': [str(c)[:200] for c in codes][:6]}
    row['ok'] = (row['verdict'] == want and row['exit'] == (0 if want == 'PASS' else 2)) if kind == 'MUST_FAIL' else True
    RES.append(row)
def wx(name, data):
    p = OUT + '/' + name
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return p
R6 = A + '/v007_final_prereg_c4/r6/KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json'; ADD6 = A + '/v007_final_prereg_c4/r6/addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'
OPEN = '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
FIN = 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'
ob = open(OPEN, 'rb').read(); assert hashlib.sha256(ob).hexdigest() == FIN
os.mkdir(OUT + '/f0'); os.mkdir(OUT + '/f1'); os.mkdir(OUT + '/f3')
F0 = wx('f0/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ob)
i = ob.index(b'\n## A') + 1
F1 = wx('f1/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ob[:i] + b'SYNTHETIC PREAMBLE LINE OUTSIDE EVERY ENTRY SECTION (MUST_FAIL control)\n' + ob[i:])
j = ob.index(b'## A100:'); k2 = ob.index(b'\n', j + 200)
F3 = wx('f3/ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM_FROZEN.md', ob[:k2] + b' SYNTHETIC EDIT INSIDE A100' + ob[k2:])
t1 = lambda fz, extra: tool('T1', ['--prereg', R6, '--frozen', fz, '--addendum-at-text-of-record', ADD6] + extra)
case('F0', 'control: tool 1 on r6, an exact FROZEN-named copy of the final V005, --expect-frozen-sha c01b3c51 (dry-run path allowance)', t1(F0, ['--expect-frozen-sha', FIN, '--allow-open-copy-for-dry-run']), 'PASS')
case('F1', 'MUST_FAIL (0643 R-01): a FROZEN copy whose bytes OUTSIDE every entry section differ (a preamble line), with --expect-frozen-sha c01b3c51', t1(F1, ['--expect-frozen-sha', FIN, '--allow-open-copy-for-dry-run']), 'REFUSE')
case('F1r', 'R-01 reproduction: the same copy WITHOUT --expect-frozen-sha (tool 1 compares entry sections only)', t1(F1, ['--allow-open-copy-for-dry-run']), 'PASS', kind='OBSERVATION')
case('F2', 'D-10: the exact copy, not at path_to_be, without the dry-run allowance', t1(F0, ['--expect-frozen-sha', FIN]), 'REFUSE')
case('F3', 'a FROZEN copy with an edit INSIDE the A100 entry section, with --expect-frozen-sha', t1(F3, ['--expect-frozen-sha', FIN, '--allow-open-copy-for-dry-run']), 'REFUSE')
VS = A + '/v007_final_prereg_c4/seal_tools_v004/SELECTED_SEAL_TOOLS_V004_C4V001.json'; VSS = '593c59faf39074b14579f927ae17c5aeda1f7450ee4a9f264f96a1f2c7b195e0'
R6S = A + '/v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json'; R6SS = '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
README = A + '/v007_final_prereg_c4/seal_tools_v003/README_SEAL_TOOLS_V003.md'; README4 = V + '/README_SEAL_TOOLS_V004_DELTA.md'
V3SEL, V3SELS = A + '/v007_final_prereg_c4/seal_tools_v003/SELECTED_SEAL_TOOLS_V003_C4V001.json', 'cf7e5b2f1b3daf55c485ada1c869bc7249040a8db8202eb1b1a90bebe1431305'
ROLES = [('seal_common', T['C'], WANT['C']), ('tool_1_check_frozen_addendum', T['T1'], WANT['T1']), ('tool_2_check_sealed_compare', T['T2'], WANT['T2']),
         ('tool_3_check_slot_fill', T['T3'], WANT['T3']), ('tool_4_build_seal_record', T['T4'], WANT['T4']), ('tool_5_print_driver_build_record', T['T5'], WANT['T5']),
         ('readme_v003_run_order', README, sha(README)), ('readme_v004_delta', README4, sha(README4)), ('selected_r6', R6S, R6SS),
         ('selected_v003_superseded_for_the_seal', V3SEL, V3SELS)]
sr = lambda roles, schema='UNT_V007_SELECTED_SEAL_TOOLS_C4V001': helper(['selected-roles', '--selected', VS, '--selected-sha', VSS, '--schema', schema] + [y for r in roles for y in ('--role-pin', '%s=%s=%s' % r)])
case('S1', 'control: the real v004 SELECTED file stores exactly the ten step-0 roles of c3v020', sr(ROLES), 'PASS', verdict_from='stderr')
case('S2', 'tool_3 role with another sha (the v001 tool 3)', sr([('tool_3_check_slot_fill', T['T3'], '7f3cf07da0d92fef0a1cc592cb644eafca2737e90b917e83ea9ffa5fc367187b')]), 'REFUSE', verdict_from='stderr')
case('S3', 'seal_common role given the v001 seal_common path and sha', sr([('seal_common', A + '/v007_final_prereg_c4/seal_tools/seal_common_c4v001.py', '43d8f8eb610106c61be197defba59cff7f357bb31c70ca9c9136a44b5d267c25')]), 'REFUSE', verdict_from='stderr')
case('S4', "the v004 SELECTED file checked against r6's schema string", sr(ROLES[:1], 'UNT_V007_SELECTED_PREREG_C4V001'), 'REFUSE', verdict_from='stderr')
S = DRY + '/passA/scratch_ctrl/V007_SEAL_ASSEMBLY'
DBR = S + '/DRIVER_BUILD_RECORD_R5_V007_SEAL.json'
R13, R13S = A + '/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
CK, CKS = A + '/tail_scheme_impl_c2/driver_r5/check/CHECK.md', '89a6de88739e1c4b76c39dc11d7417d7e243b7235511d8ea0951e1493865b632'
FEN, FENS = A + '/seal_assembly_c3/tools/fence_c3sa_c3v003.py', '9c62ad4902c895f0aeeba3a78976b5944146ee0de153989dbc79470528dd2863'
cd = lambda rec, ck=CK, cks=CKS: helper(['check-driver-build-record', '--compare', R13, '--compare-sha', R13S, '--record', rec, '--record-sha', sha(rec), '--check-record', ck,
                                       '--check-sha', cks, '--fence', FEN, '--fence-sha', FENS])
case('D1', "control: dry run 17's driver BUILD record (v003 tool 5 bytes, 25b4ff69)", cd(DBR), 'PASS', verdict_from='stderr')
rec = json.loads(open(DBR, 'rb').read())
case('D2', 'the same record re-serialized with indent 2 (not the tool 5 byte form)', cd(wx('DBR_INDENT2.json', json.dumps(rec, indent=2, sort_keys=True) + '\n')), 'REFUSE', verdict_from='stderr')
case('D3', 'the record with one extra key', cd(wx('DBR_EXTRA_KEY.json', json.dumps(dict(rec, synthetic='x'), indent=1, sort_keys=True) + '\n')), 'REFUSE', verdict_from='stderr')
case('D4', 'the record checked against the other RI-36 candidate as check record', cd(DBR, A + '/review_r5_certs_cx3/R5_REVIEW_FINAL_V001.md', '6758bd24784ec514d73054a30a8fdd673c3d0c571521a62514ba4260f3ad7ba9'), 'REFUSE', verdict_from='stderr')
CFG = DRY + '/passA/scratch_pkt/ROOT_SEAL_ADMISSION_V001.json'; SR = S + '/SEAL_RECORD_V007.json'
adm = lambda cfg: tool('T4', ['--check-admission-config', cfg, '--seal-record', SR])
case('A1', "control: tool 4 v004 --check-admission-config on the c3v020 dry run's config and SEAL_RECORD (schema C4V004)", adm(CFG), 'PASS')
D11 = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/dry_run_20261019T013957Z/passA'
case('A4', 'tool 4 v004 admission on the c3v008 dry run v003-schema SEAL_RECORD and its own config (DELTA: v004 refuses a v003 record)',
     tool('T4', ['--check-admission-config', D11 + '/scratch_pkt/ROOT_SEAL_ADMISSION_V001.json', '--seal-record', D11 + '/scratch_ctrl/V007_SEAL_ASSEMBLY/SEAL_RECORD_V007.json']), 'REFUSE')
cfg = json.loads(open(CFG, 'rb').read())
pa = dict(cfg['producer_allowlist']); pa[A + '/v007_launch_packet_cx1/postseal_records_cx1v006.py'] = '9fbdb0ca24153436b7c807778f140b7998fc0c0b5d18f4372d65a20a0e11cc59'
pa[A + '/v007_launch_packet_cx1/srb_rot_record_cx1v008.py'] = '500f8b6a27cff6157246cdaca1373ad7340003263578331d30cbdf7cebc0e4f4'
case('A2', 'tool 4 v004 admission: a 17-row config (+ the V006 writers)', adm(wx('CFG_17_ROWS.json', json.dumps(dict(cfg, producer_allowlist=pa), indent=1) + '\n')), 'REFUSE')
case('A3', 'tool 4 v004 admission: the config pins another SEAL_RECORD sha', adm(wx('CFG_OTHER_SEAL.json', json.dumps(dict(cfg, seal={'path': SR, 'sha256': '0' * 64}), indent=1) + '\n')), 'REFUSE')
ok = all(r['ok'] for r in RES)
res = {'schema': 'C3SA_MUSTFAIL_V004_V001', 'helper': {'path': HP, 'sha256': HSHA}, 'runner': {'path': RP, 'sha256': RSHA}, 'v004_tools': {k: {'path': T[k], 'sha256': WANT[k]} for k in T},
       'dry_run': DRY, 'n_cases': len(RES), 'ALL_OK': ok, 'pycache_prefix_entries': len(os.listdir(PFX)), 'results': RES}
t = json.dumps(res, indent=1) + '\n'
with open(OUT + '/MUSTFAIL_V004_RESULTS_C3SA.json', 'x') as f:
    f.write(t)
print(json.dumps({'ALL_OK': ok, 'n': len(RES), 'sha256': hashlib.sha256(t.encode()).hexdigest(), 'pycache_prefix_entries': len(os.listdir(PFX))}))
for r in RES:
    print('%-4s %-12s %-7s exit=%s ok=%s  %s' % (r['case'], r['kind'], r['verdict'], r['exit'], r['ok'], '; '.join(r['codes'])[:150]))
