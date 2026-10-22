# Claude3 (c3v011, root 0667 A123): the gate-by-gate table of the dry-run E-SEAL1 gates-only output, from bytes. For each pass of DRY it reads
# scratch_ctrl/V007_SEAL_ASSEMBLY/E_SEAL1_GATES_ONLY_OUT/GATES_ONLY.json (no-follow, helper c3v019) and checks it against the registry and the manifest:
# every gate the registry registers with record shas must read PASS with one of those record shas; every PRODUCED_AFTER_THE_SEAL gate must read
# MISSING with exactly GATE_RECORD_MISSING:<gate>; the gate sets must be equal; the dry run's stand-in manifest must carry the manifest's gates. With
# BASE (an older dry run), it also lists every gate whose entry changed. Writes OUT.json and OUT.md (exclusive create). Exit 0 iff every check holds.
# usage: python3 -I -B THIS OUT_PREFIX DRY REGISTRY=SHA MANIFEST=SHA [BASE_DRY]
import hashlib, json, sys, types
HP, HS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
OUTP, DRY = sys.argv[1], sys.argv[2]; (RP, RS), (MP, MS) = sys.argv[3].rsplit('=', 1), sys.argv[4].rsplit('=', 1); BASE = sys.argv[5] if len(sys.argv) > 5 else None
reg = H._selected_strict(H.pin(RP, RS, 'registry')); man = H._selected_strict(H.pin(MP, MS, 'manifest')); rg = reg['gate_records']
def gj(d, p):
    path = '%s/pass%s/scratch_ctrl/V007_SEAL_ASSEMBLY/E_SEAL1_GATES_ONLY_OUT/GATES_ONLY.json' % (d, p)
    b = H.read_nofollow(path, 'gates_only_' + p); return path, hashlib.sha256(b).hexdigest(), H._selected_strict(b)
G = {p: gj(DRY, p) for p in 'AB'}
B = {p: gj(BASE, p) for p in 'AB'} if BASE else None
st = H._selected_strict(H.read_nofollow(DRY + '/fixtures/MANIFEST_GATES_ONLY_STANDIN.json', 'standin'))
checks, rows = [], []
def chk(name, ok):
    checks.append({'check': name, 'ok': bool(ok)})
chk('stand-in gates == manifest gates (key for key, in order)', list(st['gates'].items()) == list(man['gates'].items()))
chk('stand-in identity_runs empty', st.get('identity_runs') == {})
for p in 'AB':
    chk('pass %s: GATES_ONLY test_mode is False' % p, G[p][2].get('test_mode') is False)
    chk('pass %s: gate set == registry gate set' % p, set(G[p][2]['gates']) == set(rg))
for g in rg:
    v = rg[g]; pre = isinstance(v, list) and len(v) > 0
    row = {'gate': g, 'registry': ('pre-seal record ' + ', '.join(s[:8] for s in v)) if pre else v, 'manifest': (man['gates'].get(g) or None)}
    for p in 'AB':
        e = G[p][2]['gates'].get(g) or {}
        row['status_' + p] = e.get('status'); row['record_' + p] = e.get('record_sha256'); row['codes_' + p] = e.get('codes')
        if pre:
            chk('pass %s: %s PASS with a registered record sha' % (p, g), e.get('status') == 'PASS' and e.get('record_sha256') in v and not e.get('codes'))
        elif v == 'PRODUCED_AFTER_THE_SEAL':
            chk('pass %s: %s MISSING (PRODUCED_AFTER_THE_SEAL)' % (p, g), e.get('status') == 'MISSING' and e.get('codes') == ['GATE_RECORD_MISSING:' + g] and e.get('record_sha256') is None)
        else:
            chk('pass %s: %s has a known registry form' % (p, g), False)
        if B:
            be = B[p][2]['gates'].get(g) or {}
            row['changed_vs_base_' + p] = {k: [be.get(k), e.get(k)] for k in sorted(set(be) | set(e)) if be.get(k) != e.get(k)}
    row['ok'] = all(c['ok'] for c in checks if (' %s ' % g) in (c['check'] + ' '))
    rows.append(row)
changed = sorted({r['gate'] for r in rows for p in 'AB' if r.get('changed_vs_base_' + p)}) if B else None
if B:
    chk('vs base: the gates whose entries changed are exactly B0_N3 and B0_RO1', changed == ['B0_N3', 'B0_RO1'])
res = {'schema': 'C3SA_GATES_ONLY_TABLE_C3V001', 'dry_run': DRY, 'gates_only': {p: {'path': G[p][0], 'sha256': G[p][1]} for p in 'AB'},
       'base_dry_run': BASE, 'base_gates_only': {p: {'path': B[p][0], 'sha256': B[p][1]} for p in 'AB'} if B else None,
       'registry': {'path': RP, 'sha256': RS}, 'manifest': {'path': MP, 'sha256': MS}, 'rows': rows, 'gates_changed_vs_base': changed, 'checks': checks,
       'n_pass_A': sum(1 for r in rows if r['status_A'] == 'PASS'), 'n_missing_A': sum(1 for r in rows if r['status_A'] == 'MISSING'),
       'n_pass_B': sum(1 for r in rows if r['status_B'] == 'PASS'), 'n_missing_B': sum(1 for r in rows if r['status_B'] == 'MISSING')}
res['all_ok'] = all(c['ok'] for c in checks)
md = ['| gate | V012 gate_records | manifest c3v002 entry | pass A | pass B | record sha (A = B) |', '| --- | --- | --- | --- | --- | --- |']
for r in rows:
    rec = (r['record_A'] or '')[:8] if r['record_A'] == r['record_B'] else '%s / %s' % ((r['record_A'] or '')[:8], (r['record_B'] or '')[:8])
    md.append('| %s | %s | %s | %s | %s | %s |' % (r['gate'], r['registry'], ('`' + r['manifest'].split('/claude_artifacts/', 1)[1] + '`') if r['manifest'] else 'null',
                                              r['status_A'] + ('' if not r['codes_A'] else ' (`%s`)' % ', '.join(r['codes_A'])), r['status_B'], rec or '(none)'))
with open(OUTP + '.json', 'x') as f:
    f.write(json.dumps(res, indent=1) + '\n')
with open(OUTP + '.md', 'x') as f:
    f.write('\n'.join(md) + '\n')
print('\n'.join(md)); print('PASS A %d / MISSING A %d; PASS B %d / MISSING B %d; changed vs base: %s' % (res['n_pass_A'], res['n_missing_A'], res['n_pass_B'], res['n_missing_B'], changed))
print('ALL_OK' if res['all_ok'] else 'SOME_FAIL %s' % [c['check'] for c in checks if not c['ok']])
sys.exit(0 if res['all_ok'] else 2)
