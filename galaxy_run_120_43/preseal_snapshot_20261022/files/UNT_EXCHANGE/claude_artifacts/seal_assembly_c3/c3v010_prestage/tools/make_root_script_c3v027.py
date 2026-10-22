# Claude3 (c3v011, root 0667 A123; Claude4 0154): derive ROOT_SEAL_STEPS_c3v027.sh from ROOT_SEAL_STEPS_c3v026.sh (b43cc38b, SELECTED c3v010) by an explicit
# replacement set (each old string exactly once). ONLY the MANIFEST_GATES / MANIFEST_GATES_SHA pin changes (plus the header and history comments): the
# gates-only manifest is MANIFEST_GATES_ONLY_C3SA_c3v002.json, the draft e5967bb9 with only gates.B0_RO1 and gates.B0_N3 set to the pre-seal records V012
# registers. The pre-publication checker (check_manifest_gates_vs_registry_c3v001.py) must PASS on it. No other check is added (A123).
# usage: python3 -I -B make_root_script_c3v027.py OUT_SCRIPT
import hashlib, json, re, subprocess, sys, types
OUT = sys.argv[1]
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'; W2 = C3 + '/c3v010_prestage'
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
SRC, SRC_SHA = C3 + '/ROOT_SEAL_STEPS_c3v026.sh', 'b43cc38be5f19c473167d8d57211c54d336d09d58fcfd66f5ca8187ad033c464'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
src = open(SRC, 'rb').read(); assert hashlib.sha256(src).hexdigest() == SRC_SHA; s = src.decode('utf-8')
OLDM, OLDMS = C3 + '/MANIFEST_GATES_ONLY_DRAFT_C3SA.json', 'e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da'
NEWM, NEWMS = C3 + '/MANIFEST_GATES_ONLY_C3SA_c3v002.json', '46dc53104d518edc9b00e77c0b4995df3e4871999c7264926dad186726ed62ca'
REGP, REGS = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json', '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa'
CK, CKS = W2 + '/tools/check_manifest_gates_vs_registry_c3v001.py', 'f92a4e031ffb3405030513c8cb05bb8bbf108b1e631addb68d62113c3d78ca5b'
H.pin(NEWM, NEWMS, 'manifest_c3v002'); assert hashlib.sha256(open(CK, 'rb').read()).hexdigest() == CKS
ck = subprocess.run([PY, '-I', '-B', CK, '%s=%s' % (NEWM, NEWMS), '%s=%s' % (REGP, REGS)], capture_output=True, text=True, cwd='/', env={'PATH': '/usr/bin:/bin', 'LANG': 'en_US.UTF-8'})
assert ck.returncode == 0 and json.loads(ck.stdout)['verdict'] == 'PASS', ck.stdout[-400:]
assert 'REGISTRY_SHA="%s"' % REGS in s
R = [
 ('header', '# ROOT_SEAL_STEPS_c3v026.sh:', '# ROOT_SEAL_STEPS_c3v027.sh:'),
 ('history', '# c3v026 supersedes ROOT_SEAL_STEPS_c3v025.sh (22746e21, never published) for the c3v010 selection:',
  '''# c3v027 supersedes ROOT_SEAL_STEPS_c3v026.sh (b43cc38b, SELECTED c3v010) for the c3v011 selection: root 0667 (A123, 92a1aa78), after Claude4 0154
#   (3b7cc56f): the gates-only manifest e5967bb9 (registry-V009 era) had gates.B0_RO1 and gates.B0_N3 null, so step 8's E-SEAL1 recorded both as
#   MISSING although V012 registers their pre-seal records (prereg r6 srr[0]: the RO1 replay's gate output goes into E-SEAL1). From bytes
#   (make_root_script_c3v027.py): MANIFEST_GATES = MANIFEST_GATES_ONLY_C3SA_c3v002.json (%s) = e5967bb9 with only gates.B0_RO1 =
#   ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json (332452b7) and gates.B0_N3 = ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json (dd1dd912), in the absolute form
#   of every other gate; its note is unchanged (A123). The pre-publication checker check_manifest_gates_vs_registry_c3v001.py (%s) PASSES on it
#   against V012: every pre-seal gate named, with registered bytes; every PRODUCED_AFTER_THE_SEAL gate null. e5967bb9 is not pinned. Nothing
#   else changes: no new check (A123).
# c3v026 superseded ROOT_SEAL_STEPS_c3v025.sh (22746e21, never published) for the c3v010 selection:''' % (NEWMS[:8], CKS[:8])),
 ('manifest pin', 'MANIFEST_GATES="$C3/MANIFEST_GATES_ONLY_DRAFT_C3SA.json"; MANIFEST_GATES_SHA="%s"' % OLDMS,
  'MANIFEST_GATES="$C3/MANIFEST_GATES_ONLY_C3SA_c3v002.json"; MANIFEST_GATES_SHA="%s"' % NEWMS),
]
out = s
for rid, o, n in R:
    assert out.count(o) == 1, (rid, out.count(o))
    out = out.replace(o, n)
assert OLDMS not in out.split('# ============================================================================================================ PINS', 1)[1]
pins = out[out.index('# ============================================================================================================ PINS'):out.index('# ---------------------------------------------------------------------------------------------------- OUTPUTS')]
assert not re.search(r'^[A-Z0-9_]+="PENDING', pins, re.M) and '_SHA="PENDING"' not in pins
progs = re.findall(r'"\$\{PYX\[@\]\}" -c \'(.*?)\'', out, re.S)
for pr in progs:
    compile(pr, 'embedded', 'exec', dont_inherit=True)
def code(x):
    return [ln for ln in x.splitlines() if not ln.lstrip().startswith('#')]
cs, co = code(s), code(out)
changed = [(a, b) for a, b in zip(cs, co) if a != b]
assert len(cs) == len(co) and len(changed) == 1 and changed[0][1].startswith('MANIFEST_GATES="$C3/MANIFEST_GATES_ONLY_C3SA_c3v002.json"'), changed
with open(OUT, 'x') as f:
    f.write(out)
bn = subprocess.run(['/bin/bash', '-n', OUT], capture_output=True, text=True)
print(json.dumps({'script': {'path': OUT, 'sha256': hashlib.sha256(out.encode()).hexdigest(), 'bytes': len(out.encode())}, 'from': SRC_SHA, 'manifest': [NEWM, NEWMS],
                  'replacements': len(R), 'non_comment_lines_changed': [b for a, b in changed], 'embedded_python_programs_compiled': len(progs), 'checker': 'PASS', 'bash_n_ok': bn.returncode == 0}, indent=1))
sys.exit(0 if bn.returncode == 0 else 2)
