# c3v004 (c3v010 FINAL, c3v026): + N-3c (the superseded registry V011 as REGISTRY, with the draft c3v007 on V012), N-10c (V004 superseded),
# N-10d (V005 superseded; the refusal names V006 as the file of record) and N-11c (the draft c3v006, on V011, against REGISTRY V012).
# c3v003 (c3v010 FINAL, c3v024): N-9 uses the real custody pin; + N-10b (V003 superseded) and N-11b (draft c3v005, registry V010).
# c3v002 (c3v010 near-final, c3v022): N-3/N-4 put the real REGISTRY / DISCLOSURES back to PENDING; + N-8 to N-13 (the B7 pins, V002 superseded,
# the c3v004 draft against V010, stale B7 env inputs); N-5 now refuses at the old draft registry; N-6 uses the TARGET draft (c3v005).
# Claude3 (c3v010 PRE-STAGE; root A114 / A116; lead dispatch): MUST_FAIL controls for what c3v021 adds, each on a COPY of the production
# ROOT_SEAL_STEPS_c3v021.sh in its dry-run form (generator c3v011: the published scratch substitutions plus the labelled stand-ins S26
# registry V009 and S27 disclosures V002), a fresh scratch pass folder per case, the step calls cut after step 0 (step 0 writes nothing).
#   r13 as the reviewed compare refuses (superseded); the superseded selection CX1V001 refuses; each PENDING placeholder refuses (the
#   stand-in reverted: the registry V010, root disclosures V003); the draft compare slot must be the reviewed compare (the old runtime-
#   marker draft c3v003; a c3v004 copy pointing at r13); the selection must carry IMPL r14 as its implementation entry.
# Nothing outside OUTDIR is written. No launch; no protected path. A115: these are fail-closed checks of the seal wiring (labels below).
# usage: python3 -I -B mustfail_r14_c3v021_c3sa_c3v001.py OUTDIR SCRIPT=SHA GEN=SHA DRYRUN_DIR SHIM=SHA
import hashlib, json, os, re, subprocess, sys
OUT = sys.argv[1]
def pa(x):
    p, h = x.rsplit('=', 1); return p, h
(SC, SCS), (GEN, GENS) = pa(sys.argv[2]), pa(sys.argv[3]); DRY = sys.argv[4]; (SHIM, SHIMS) = pa(sys.argv[5])
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'
R13P, R13S = A + '/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py', 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
SEL13P, SEL13S = A + '/v007_compare_c2/r13/SELECTED_R13_CX3V001.json', '10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e'
SEL1P, SEL1S = A + '/v007_compare_c2/r14/SELECTED_R14_CX1V001.json', 'dc74949d1d4f19336661f8ce85e9a85de0176837adad61c7a9585a147f933533'
SEL2P, SEL2S = A + '/v007_compare_c2/r14/SELECTED_R14_CX1V002.json', '6b650ececefee673ec3e04849574f9a4b75b977288afd3c9949a4b8d2d3cd49a'
IMPL13P, IMPL13S = A + '/v007_compare_c2/r13/COMPARE_V007_IMPL_R13.md', '274f7049ece71339d39395b434e7e08bfab33067e3e600d17b4a3bde43fb74a3'
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for p, h in ((SC, SCS), (GEN, GENS), (SHIM, SHIMS), (R13P, R13S), (SEL13P, SEL13S), (SEL1P, SEL1S), (SEL2P, SEL2S), (IMPL13P, IMPL13S)):
    assert sha(p) == h, p
os.mkdir(OUT)
ENV = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1',
       'LANG': 'en_US.UTF-8', 'HOME': '/Users/bgm'}
TT = open(SC).read()
DRM = re.search(r'^DRAFT="([^"]*)";\s+DRAFT_SHA="([0-9a-f]{64})"', TT, re.M); DRP = DRM.group(1).replace('$C3', C3, 1)
def wx(name, data):
    p = OUT + '/' + name
    with open(p, 'xb') as f:
        f.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return p, sha(p)
def run_env(run_file, v):
    env = dict(ENV)
    for ln in open(run_file).read().splitlines():
        m = re.match(r'export (\w+)=("([^"]*)"|(\S+))', ln)
        if m:
            env[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(4)
    env['UNT_SEAL_DISPOSITIONS_PATH'] = v + '/scratch_ctrl/V007_SEAL_ASSEMBLY_INPUTS/COVERED_LATER_DISPOSITIONS_V007.json'
    return env
RES = []
def scase(cid, label, desc, want, code_sub, edits=(), env_set=None, revert_s29=False):
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
    if revert_s29:
        m29 = S29N.search(s); assert m29, 'S29 line'
        s = s.replace(m29.group(0), 'B7_SUCCESSOR_CUSTODY="PENDING_B7_SUCCESSOR_CUSTODY_RECORD (root, converter v002; A118)"; B7_SUCCESSOR_CUSTODY_SHA="PENDING"', 1)
    for o, n in edits:
        assert s.count(o) == 1, (cid, o[:80], s.count(o)); s = s.replace(o, n)
    k = s.index('step0_preflight\nstep1_freeze\n')
    s = s[:k] + 'step0_preflight\necho "STEP0_ONLY: preflight passed (MUST_FAIL harness; no later step runs)"\n'
    cp = v + '/STEP0_ONLY_%s.sh' % cid.replace('-', '_')
    with open(cp, 'x') as f:
        f.write(s)
    env = run_env(DRY + '/passA/RUN_A.sh', v); env.update(env_set or {})
    r = subprocess.run(['/bin/bash', cp], capture_output=True, text=True, cwd='/', env=env)
    passed = r.returncode == 0 and 'STEP0_ONLY: preflight passed' in r.stdout
    stopped = r.returncode != 0 and 'STOPPED at step 0' in r.stderr
    code = next((ln for ln in r.stderr.splitlines() if ln.startswith('REFUSE:') or 'AssertionError' in ln), '')
    row = {'case': cid, 'a115_label': label, 'what': desc, 'want': want, 'want_code': code_sub, 'verdict': 'PASS' if passed else ('REFUSE' if stopped else 'OTHER'),
           'exit': r.returncode, 'code': code[:300], 'copy': {'path': cp, 'sha256': sha(cp)},
           'wrote_nothing_beyond_the_harness': os.listdir(v + '/scratch_internal') == [] and os.listdir(v + '/scratch_pkt/P128') == [] and not os.path.exists(v + '/scratch_ctrl/V007_SEAL_ASSEMBLY')}
    row['ok'] = row['verdict'] == want and (want == 'PASS' or code_sub in row['code']) and row['wrote_nothing_beyond_the_harness']
    if row['verdict'] == 'OTHER':
        row['stderr_tail'] = r.stderr[-400:]
    RES.append(row)
_REGL = re.search(r'^REGISTRY="[^"]*"; REGISTRY_SHA="[0-9a-f]{64}"$', TT, re.M).group(0)
_DISL = re.search(r'^DISCLOSURES="[^"]*"; DISCLOSURES_SHA="[0-9a-f]{64}"$', TT, re.M).group(0)
_NIL = re.search(r'^B7_NEW_ITEM_LIST="[^"]*"; B7_NEW_ITEM_LIST_SHA="[0-9a-f]{64}"$', TT, re.M).group(0)
_UNUSED_S26N = 'REGISTRY="$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V009.json"; REGISTRY_SHA="32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8"   # DRY RUN S26: STAND-IN (V010 PENDING)'
S26O = 'REGISTRY="PENDING_PRODUCER_REGISTRY_V010 (Claude3, A114)"; REGISTRY_SHA="PENDING"'
S27N = 'DISCLOSURES="$C3/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json"; DISCLOSURES_SHA="a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3"   # DRY RUN S27: STAND-IN (V003 PENDING)'
S27O = 'DISCLOSURES="PENDING_ROOT_DISCLOSURES_V003 (A116; root finalizes it once B0_N3 and B0_RO1 exist)"; DISCLOSURES_SHA="PENDING"'
scase('N-0', 'control', 'control: the c3v021 copy with the two labelled stand-ins passes step 0 (r14, SELECTED_R14_CX1V002, IMPL r14, draft c3v004)', 'PASS', '')
scase('N-1', 'NOTE (fail-closed)', 'r13 as the reviewed compare (with its own SELECTED_R13): refused as superseded', 'REFUSE', 'REFUSE: the compare source is a superseded round',
      env_set={'UNT_SEAL_COMPARE_REVIEWED_PATH': R13P, 'UNT_SEAL_COMPARE_REVIEWED_SHA256': R13S, 'UNT_SEAL_COMPARE_SELECTION_PATH': SEL13P, 'UNT_SEAL_COMPARE_SELECTION_SHA256': SEL13S})
scase('N-1b', 'NOTE (fail-closed)', 'r13 as the reviewed compare with the r14 selection: refused as superseded', 'REFUSE', 'REFUSE: the compare source is a superseded round',
      env_set={'UNT_SEAL_COMPARE_REVIEWED_PATH': R13P, 'UNT_SEAL_COMPARE_REVIEWED_SHA256': R13S})
scase('N-2', 'NOTE (fail-closed)', 'the superseded selection SELECTED_R14_CX1V001 (dc74949d) with r14', 'REFUSE', 'REFUSE: the compare selection must be SELECTED_R14_CX1V002',
      env_set={'UNT_SEAL_COMPARE_SELECTION_PATH': SEL1P, 'UNT_SEAL_COMPARE_SELECTION_SHA256': SEL1S})
scase('N-3', 'NOTE (fail-closed)', 'the registry pin put back to a PENDING placeholder', 'REFUSE', 'REFUSE: a PINS value is still PENDING', [(_REGL, 'REGISTRY="PENDING_PRODUCER_REGISTRY_V010 (Claude3, A114)"; REGISTRY_SHA="PENDING"')])
scase('N-4', 'NOTE (fail-closed)', 'the disclosures pin put back to a PENDING placeholder', 'REFUSE', 'REFUSE: a PINS value is still PENDING', [(_DISL, 'DISCLOSURES="PENDING_ROOT_DISCLOSURES_V003 (A116)"; DISCLOSURES_SHA="PENDING"')])
S29N = re.compile(r'^B7_SUCCESSOR_CUSTODY="[^"]*"; B7_SUCCESSOR_CUSTODY_SHA="[0-9a-f]{64}"$', re.M)   # c3v003: the REAL custody pin of c3v024
scase('N-8', 'NOTE (fail-closed)', 'the B7 NEW-item list pin put back to a PENDING placeholder', 'REFUSE', 'REFUSE: PENDING: the B7 NEW-item list is not pinned yet',
      [(_NIL, 'B7_NEW_ITEM_LIST="PENDING_B7_NEW_ITEM_LIST"; B7_NEW_ITEM_LIST_SHA="PENDING"')])
scase('N-9', 'NOTE (fail-closed)', 'the B7 successor-custody pin put back to a PENDING placeholder', 'REFUSE', 'REFUSE: PENDING: the B7 successor-custody record is not written yet', [], revert_s29=True)
scase('N-10', 'NOTE (fail-closed)', 'the superseded V002 as the disclosures pin', 'REFUSE', 'REFUSE: the disclosures file is a superseded version',
      [(_DISL, 'DISCLOSURES="%s"; DISCLOSURES_SHA="%s"' % (C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V002.json', 'a0284ecedd1c9a322242ee69611269afa8fdfc46c15ccd71e556248b230e1ed3'))])
scase('N-11', 'NOTE (fail-closed)', 'the pre-stage slot draft c3v004 (its producer_registry is V009) with REGISTRY V010', 'REFUSE', "REFUSE: the slot draft's producer_registry is not REGISTRY",
      [(re.search(r'^DRAFT="[^"]*";\s+DRAFT_SHA="[0-9a-f]{64}"', TT, re.M).group(0), 'DRAFT="%s";              DRAFT_SHA="%s"' % (C3 + '/c3v010_prestage/SLOT_VALUES_DRAFT_c3v004.json', '723a36d15a69c511570841c14724fb703d9bfff896f773530abbef3cab72dbeb'))])
scase('N-10b', 'NOTE (fail-closed)', 'the superseded V003 as the disclosures pin', 'REFUSE', 'REFUSE: the disclosures file is a superseded version',
      [(_DISL, 'DISCLOSURES="%s"; DISCLOSURES_SHA="%s"' % (C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V003.json', '990be628e810bc38afd6657ac151cfb908c761ce266c232de71baf8bd6d300eb'))])
scase('N-11b', 'NOTE (fail-closed)', 'the slot draft c3v005 (its producer_registry is V010) with REGISTRY V011', 'REFUSE', "REFUSE: the slot draft's producer_registry is not REGISTRY",
      [(re.search(r'^DRAFT="[^"]*";\s+DRAFT_SHA="[0-9a-f]{64}"', TT, re.M).group(0), 'DRAFT="%s";              DRAFT_SHA="%s"' % (C3 + '/c3v010_prestage/SLOT_VALUES_DRAFT_c3v005.json', 'd6924860628df553f19af6094316390169cbe7828e8a77aa35daff49dab600ca'))])
scase('N-12', 'NOTE (fail-closed)', 'a stale B7 input: UNT_SEAL_NEW_ITEM_LIST_PATH still set', 'REFUSE', 'REFUSE: UNT_SEAL_NEW_ITEM_LIST_PATH is no longer an input', env_set={'UNT_SEAL_NEW_ITEM_LIST_PATH': '/Users/bgm/x.json'})
scase('N-13', 'NOTE (fail-closed)', 'a stale B7 input: UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 still set', 'REFUSE', 'REFUSE: UNT_SEAL_SUCCESSOR_CUSTODY_SHA256 is no longer an input', env_set={'UNT_SEAL_SUCCESSOR_CUSTODY_SHA256': '0' * 64})
DRL = DRM.group(0)
D3P, D3S = C3 + '/SLOT_VALUES_DRAFT_c3v003.json', 'e12292a27e58aacdebfde5dfc4d1a3f7ccb0c5b3ca4b756ef2a6d8468a5311c5'
scase('N-5', 'NOTE (fail-closed)', 'the old slot draft c3v003 (registry V009; compare slot a run-time marker naming r13): refused at its first mismatch', 'REFUSE', "REFUSE: the slot draft's producer_registry is not REGISTRY",
      [(DRL, 'DRAFT="%s";              DRAFT_SHA="%s"' % (D3P, D3S))])
d6 = json.loads(open(DRP, 'rb').read()); d6['compare_reviewed_source'] = {'path': R13P, 'sha256': R13S}
p6, h6 = wx('DRAFT_C3V004_COMPARE_SLOT_R13.json', json.dumps(d6, indent=1) + '\n')
scase('N-6', 'NOTE (fail-closed)', 'a c3v004 copy whose compare slot is r13 (path and sha)', 'REFUSE', "REFUSE: the slot draft's compare_reviewed_source is not the reviewed compare (r14)",
      [(DRL, 'DRAFT="%s";              DRAFT_SHA="%s"' % (p6, h6))])
s7 = json.loads(open(SEL2P, 'rb').read()); s7['implementation'] = {'path': IMPL13P, 'sha256': IMPL13S, 'bytes': os.path.getsize(IMPL13P)}
p7, h7 = wx('SYNTHETIC_SELECTION_R14_WITH_IMPL_R13.json', json.dumps(s7, indent=2) + '\n')
SELLINE = re.search(r'^COMPARE_R14_SELECTION_SHA="[0-9a-f]{64}"', TT, re.M).group(0)
scase('N-7', 'NOTE (fail-closed)', 'a synthetic r14 selection whose implementation entry is IMPL r13 (its sha set as the selection pin of the copy)', 'REFUSE', 'SELECTION_IMPLEMENTATION_IS_NOT_IMPL_R14',
      [(SELLINE, 'COMPARE_R14_SELECTION_SHA="%s"' % h7)], env_set={'UNT_SEAL_COMPARE_SELECTION_PATH': p7, 'UNT_SEAL_COMPARE_SELECTION_SHA256': h7})
scase('N-3c', 'NOTE (fail-closed)', 'the superseded registry V011 (path and sha) as the REGISTRY pin, the draft c3v007 (V012) unchanged', 'REFUSE', "REFUSE: the slot draft's producer_registry is not REGISTRY",
      [(_REGL, 'REGISTRY="$A/producer_registry_c3/out/PRODUCER_REGISTRY_C3V011.json"; REGISTRY_SHA="512a7171b952ca97668e8646b106608679ed963faaceba9604dbc3750a7e45f8"')])
scase('N-10c', 'NOTE (fail-closed)', 'the superseded V004 as the disclosures pin', 'REFUSE', 'REFUSE: the disclosures file is a superseded version',
      [(_DISL, 'DISCLOSURES="%s"; DISCLOSURES_SHA="%s"' % (C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V004.json', 'adac5030770ec78114145fe80ae1b21e454d43b788037a632c01af076b25abfe'))])
scase('N-10d', 'NOTE (fail-closed)', 'the superseded V005 as the disclosures pin (the refusal names V006)', 'REFUSE', 'REFUSE: the disclosures file is a superseded version (root 0665: V006 is the file of record)',
      [(_DISL, 'DISCLOSURES="%s"; DISCLOSURES_SHA="%s"' % (C3 + '/root_inputs/SEAL_MANUAL_DISCLOSURES_V005.json', 'b1a7b3d5791772ff50c56c9aab277e5112d0ad463ada055067042ac62fbcafd4'))])
scase('N-11c', 'NOTE (fail-closed)', 'the slot draft c3v006 (its producer_registry is V011) with REGISTRY V012', 'REFUSE', "REFUSE: the slot draft's producer_registry is not REGISTRY",
      [(re.search(r'^DRAFT="[^"]*";\s+DRAFT_SHA="[0-9a-f]{64}"', TT, re.M).group(0), 'DRAFT="%s";              DRAFT_SHA="%s"' % (C3 + '/c3v010_prestage/SLOT_VALUES_DRAFT_c3v006.json', 'f542e394467873cbb3901f0a08fe880489250db4c15fb5ea8b696557f59d8fec'))])
res = {'schema': 'C3SA_MUSTFAIL_R14_C3V026_V004', 'script': {'path': SC, 'sha256': SCS}, 'generator': {'path': GEN, 'sha256': GENS}, 'dry_run_dir': DRY,
       'shim': {'path': SHIM, 'sha256': SHIMS}, 'cases': RES, 'n': len(RES), 'n_ok': sum(r['ok'] for r in RES)}
res['all_ok'] = res['n_ok'] == res['n']
with open(OUT + '/MUSTFAIL_R14_C3V024_RESULTS_C3SA.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
for r in RES:
    print('%-5s ok=%s want=%s got=%s exit=%s %s' % (r['case'], r['ok'], r['want'], r['verdict'], r['exit'], r['code'][:140]))
print('ALL_OK' if res['all_ok'] else 'SOME_FAIL', '%d/%d' % (res['n_ok'], res['n']))
