# Claude3 (c3v011, root 0667 A123): MUST_FAIL controls for check_manifest_gates_vs_registry_c3v001.py, on synthetic copies written under OUTDIR (open 'x').
# Each case runs the checker in its own isolated process. Nothing outside OUTDIR is written.
# usage: python3 -I -B THIS OUTDIR CHECKER=SHA MANIFEST=SHA REGISTRY=SHA OLD_MANIFEST=SHA
import hashlib, json, os, subprocess, sys
OUT = sys.argv[1]
(CK, CKS), (MP, MS), (RP, RS), (OP, OS_) = [a.rsplit('=', 1) for a in sys.argv[2:6]]
PY = '/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for p, h in ((CK, CKS), (MP, MS), (RP, RS), (OP, OS_)):
    assert sha(p) == h, p
os.mkdir(OUT); PFX = OUT + '/NO_PYCACHE_PREFIX_EMPTY'; os.mkdir(PFX)
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'en_US.UTF-8', 'HOME': '/Users/bgm', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}
M = json.loads(open(MP, 'rb').read()); R = json.loads(open(RP, 'rb').read())
def wx(name, obj):
    p = OUT + '/' + name
    with open(p, 'x') as f:
        f.write(json.dumps(obj, indent=1) + '\n')
    return p, sha(p)
RES = []
def case(cid, desc, man, reg, want, code=''):
    r = subprocess.run([PY, '-I', '-B', '-X', 'pycache_prefix=' + PFX, CK, '%s=%s' % man, '%s=%s' % reg], capture_output=True, text=True, cwd='/', env=ENV)
    try:
        v = json.loads(r.stdout)
    except Exception:
        v = {'verdict': 'NO_VERDICT', 'codes': [r.stderr[-300:]]}
    codes = v.get('codes') or []
    row = {'case': cid, 'what': desc, 'want': want, 'want_code': code, 'verdict': v.get('verdict'), 'exit': r.returncode, 'codes': [c[:200] for c in codes]}
    row['ok'] = row['verdict'] == want and r.returncode == (0 if want == 'PASS' else 2) and (want == 'PASS' or any(code in c for c in codes))
    RES.append(row)
def mvar(cid, fn):
    o = json.loads(json.dumps(M)); fn(o); return wx('%s_SYNTHETIC_MANIFEST.json' % cid.replace('-', '_'), o)
case('MG-0', 'control: MANIFEST_GATES_ONLY_C3SA_c3v002 against V012', (MP, MS), (RP, RS), 'PASS')
case('MG-1', 'the superseded draft e5967bb9 (B0_RO1 and B0_N3 null)', (OP, OS_), (RP, RS), 'REFUSE', 'PRESEAL_GATE_NULL_IN_MANIFEST:B0_RO1')
case('MG-1b', 'the superseded draft e5967bb9: B0_N3 is reported too', (OP, OS_), (RP, RS), 'REFUSE', 'PRESEAL_GATE_NULL_IN_MANIFEST:B0_N3')
case('MG-2', 'a copy with only B0_RO1 null', mvar('MG-2', lambda o: o['gates'].__setitem__('B0_RO1', None)), (RP, RS), 'REFUSE', 'PRESEAL_GATE_NULL_IN_MANIFEST:B0_RO1')
case('MG-3', 'a copy with only B0_N3 null', mvar('MG-3', lambda o: o['gates'].__setitem__('B0_N3', None)), (RP, RS), 'REFUSE', 'PRESEAL_GATE_NULL_IN_MANIFEST:B0_N3')
case('MG-4', 'a copy with another pre-seal gate (B0) null', mvar('MG-4', lambda o: o['gates'].__setitem__('B0', None)), (RP, RS), 'REFUSE', 'PRESEAL_GATE_NULL_IN_MANIFEST:B0')
case('MG-5', 'a PRODUCED_AFTER_THE_SEAL gate (I4) named by a path', mvar('MG-5', lambda o: o['gates'].__setitem__('I4', M['gates']['B0_RO1'])), (RP, RS), 'REFUSE', 'POSTSEAL_GATE_NAMED_IN_MANIFEST:I4')
case('MG-6', 'B0_RO1 pointed at the B0_N3 record (bytes not registered for B0_RO1)', mvar('MG-6', lambda o: o['gates'].__setitem__('B0_RO1', M['gates']['B0_N3'])), (RP, RS), 'REFUSE', 'MANIFEST_GATE_RECORD_NOT_REGISTERED:B0_RO1')
cp = OUT + '/B0_RO1_RECORD_BYTE_COPY.json'
with open(cp, 'xb') as f:
    f.write(open(M['gates']['B0_RO1'], 'rb').read())
case('MG-7', 'control: B0_RO1 named by a byte-identical copy at another path (the registry pins bytes)', mvar('MG-7', lambda o: o['gates'].__setitem__('B0_RO1', cp)), (RP, RS), 'PASS')
case('MG-8', 'a gate key missing (B0_N3 deleted)', mvar('MG-8', lambda o: o['gates'].pop('B0_N3')), (RP, RS), 'REFUSE', 'MANIFEST_GATE_KEYS_NOT_THE_REGISTRY_GATES')
case('MG-9', 'an extra gate key (B0_EXTRA null)', mvar('MG-9', lambda o: o['gates'].__setitem__('B0_EXTRA', None)), (RP, RS), 'REFUSE', 'MANIFEST_GATE_KEYS_NOT_THE_REGISTRY_GATES')
r10 = json.loads(json.dumps(R)); r10['gate_records']['B0_RO1'] = []
case('MG-10', 'a synthetic registry whose B0_RO1 slot is empty (not built)', (MP, MS), wx('MG_10_SYNTHETIC_REGISTRY.json', r10), 'REFUSE', 'REGISTRY_GATE_SLOT_EMPTY:B0_RO1')
case('MG-11', 'a gate value that is not a path (an integer)', mvar('MG-11', lambda o: o['gates'].__setitem__('B0_N3', 1)), (RP, RS), 'REFUSE', 'MANIFEST_GATE_NOT_A_PATH:B0_N3')
case('MG-12', 'the real manifest with a wrong sha', (MP, MS[:-1] + ('0' if MS[-1] != '0' else '1')), (RP, RS), 'REFUSE', 'PIN_BYTES_MISMATCH')
lk = OUT + '/LINK_TO_B0_RO1_RECORD.json'; os.symlink(M['gates']['B0_RO1'], lk)
case('MG-13', 'B0_RO1 named through a synthetic symlink (never followed)', mvar('MG-13', lambda o: o['gates'].__setitem__('B0_RO1', lk)), (RP, RS), 'REFUSE', 'PATH_HAS_SYMLINK_COMPONENT')
r14 = json.loads(json.dumps(R)); r14['gate_records']['I4'] = 'PRODUCED_LATER'
case('MG-14', 'a synthetic registry with an unknown gate form (I4)', (MP, MS), wx('MG_14_SYNTHETIC_REGISTRY.json', r14), 'REFUSE', 'REGISTRY_GATE_FORM:I4')
res = {'schema': 'C3SA_MUSTFAIL_MANIFEST_GATES_CHECK_C3V001', 'checker': {'path': CK, 'sha256': CKS}, 'manifest': {'path': MP, 'sha256': MS}, 'registry': {'path': RP, 'sha256': RS},
       'old_manifest': {'path': OP, 'sha256': OS_}, 'cases': RES, 'n': len(RES), 'n_ok': sum(r['ok'] for r in RES), 'pycache_prefix_entries': len(os.listdir(PFX))}
res['all_ok'] = res['n_ok'] == res['n'] and res['pycache_prefix_entries'] == 0
with open(OUT + '/MUSTFAIL_MANIFEST_GATES_CHECK_RESULTS_C3SA.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
for r in RES:
    print('%-6s ok=%s want=%s got=%s %s' % (r['case'], r['ok'], r['want'], r['verdict'], (r['codes'] or [''])[0][:110]))
print('ALL_OK' if res['all_ok'] else 'SOME_FAIL', '%d/%d' % (res['n_ok'], res['n']))
