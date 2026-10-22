# Claude3 (c3v011, root 0667 A123; pre-publication verification, NOT a seal-script step): check, from bytes, a gates-only manifest against the
# producer registry. Every gate the registry registers with record shas (pre-seal) must be named in the manifest by a path whose bytes hash to one
# of those shas; every gate the registry marks PRODUCED_AFTER_THE_SEAL must be null; the two gate key sets must be equal. Anything else refuses.
# Reads through the pinned helper c3v019 (no-follow, /Users spellings, read once). Exit 0 PASS, 2 REFUSE; a JSON verdict on stdout.
# usage: python3 -I -B THIS MANIFEST=SHA REGISTRY=SHA [OUT_JSON]
import hashlib, json, re, sys, types
HP, HS = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/seal_assembly_c3/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
HEX = re.compile(r'[0-9a-f]{64}')
(MP, MS), (RP, RS) = sys.argv[1].rsplit('=', 1), sys.argv[2].rsplit('=', 1)
OUT = sys.argv[3] if len(sys.argv) > 3 else None
res = {'schema': 'C3SA_MANIFEST_GATES_VS_REGISTRY_C3V001', 'manifest': {'path': MP, 'sha256': MS}, 'registry': {'path': RP, 'sha256': RS}, 'gates': {}, 'codes': []}
def done():
    res['verdict'] = 'PASS' if not res['codes'] else 'REFUSE'
    t = json.dumps(res, indent=1) + '\n'
    if OUT:
        with open(OUT, 'x') as f:
            f.write(t)
    sys.stdout.write(t)
    sys.exit(0 if res['verdict'] == 'PASS' else 2)
try:
    m = H._selected_strict(H.pin(MP, MS, 'manifest'))
    r = H._selected_strict(H.pin(RP, RS, 'registry'))
except H.Refuse as e:
    res['codes'].append(str(e)); done()
mg, rg = m.get('gates'), r.get('gate_records')
if not isinstance(mg, dict) or not isinstance(rg, dict):
    res['codes'].append('GATES_NOT_OBJECTS'); done()
if set(mg) != set(rg):
    res['codes'].append('MANIFEST_GATE_KEYS_NOT_THE_REGISTRY_GATES missing=%s extra=%s' % (sorted(set(rg) - set(mg)), sorted(set(mg) - set(rg))))
for g in rg:
    v, p = rg[g], mg.get(g)
    row = {'registry': None, 'manifest': p, 'file_sha256': None, 'ok': False}
    if v == 'PRODUCED_AFTER_THE_SEAL':
        row['registry'] = 'PRODUCED_AFTER_THE_SEAL'
        if g in mg and p is None:
            row['ok'] = True
        elif g in mg:
            res['codes'].append('POSTSEAL_GATE_NAMED_IN_MANIFEST:%s' % g)
    elif isinstance(v, list) and v and all(isinstance(s, str) and HEX.fullmatch(s) for s in v):
        row['registry'] = {'pre_seal_record_sha256': v}
        if g not in mg:
            pass
        elif p is None:
            res['codes'].append('PRESEAL_GATE_NULL_IN_MANIFEST:%s' % g)
        elif not isinstance(p, str):
            res['codes'].append('MANIFEST_GATE_NOT_A_PATH:%s' % g)
        else:
            try:
                b = H.read_nofollow(p, 'gate ' + g)
                row['file_sha256'] = hashlib.sha256(b).hexdigest()
                if row['file_sha256'] in v:
                    row['ok'] = True
                else:
                    res['codes'].append('MANIFEST_GATE_RECORD_NOT_REGISTERED:%s' % g)
            except H.Refuse as e:
                res['codes'].append('MANIFEST_GATE_PATH_REFUSED:%s: %s' % (g, e))
    elif v == []:
        res['codes'].append('REGISTRY_GATE_SLOT_EMPTY:%s (a named slot that fails closed: not built)' % g)
    else:
        res['codes'].append('REGISTRY_GATE_FORM:%s' % g)
    res['gates'][g] = row
res['n_pre_seal'] = sum(1 for x in res['gates'].values() if isinstance(x['registry'], dict))
res['n_produced_after_the_seal'] = sum(1 for x in res['gates'].values() if x['registry'] == 'PRODUCED_AFTER_THE_SEAL')
res['nulls_in_manifest'] = sorted(g for g, p in mg.items() if p is None)
done()
