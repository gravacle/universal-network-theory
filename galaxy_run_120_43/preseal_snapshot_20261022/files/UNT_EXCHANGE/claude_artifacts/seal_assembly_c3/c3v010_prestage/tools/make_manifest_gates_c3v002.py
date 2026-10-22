# Claude3 (c3v011, root 0667 A123; Claude4 0154): write MANIFEST_GATES_ONLY_C3SA_c3v002.json = MANIFEST_GATES_ONLY_DRAFT_C3SA.json (e5967bb9) with ONLY
# gates.B0_RO1 and gates.B0_N3 set to the pre-seal records registry V012 (4b8a3c35) registers, in the absolute /Users form the draft uses for every
# other gate; nothing else changes (the note too stays byte-identical, A123). Also SLOT_XREF_C3SA_c3v002.json = SLOT_XREF_C3SA.json (4bd214a8) with the
# two records added to cross_reference_not_slots and manifest_gates_only_draft moved to the new manifest (the old one kept under a new key).
# Every value from bytes through the pinned helper c3v019. usage: python3 -I -B THIS OUT_MANIFEST OUT_XREF
import hashlib, json, sys, types
OUTM, OUTX = sys.argv[1:3]
A = '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts'; C3 = A + '/seal_assembly_c3'
HP, HS = C3 + '/tools/seal_steps_c3sa_c3v019.py', '91b15dc688a2c28e1b5362d9568a80f92431938eb5e2807367b2327a37290cbf'
hb = open(HP, 'rb').read(); assert hashlib.sha256(hb).hexdigest() == HS
H = types.ModuleType('h'); H.__file__ = HP; exec(compile(hb, HP, 'exec', dont_inherit=True), H.__dict__)
OLDP, OLDS = C3 + '/MANIFEST_GATES_ONLY_DRAFT_C3SA.json', 'e5967bb9901fda39703553c5c02b4d11a580ef8456f6c0b7d315ee4c750f09da'
REGP, REGS = A + '/producer_registry_c3/out/PRODUCER_REGISTRY_C3V012.json', '4b8a3c35ca9a140bdb9e132f564d2163704e915aa67840c71c36fea551cafafa'
XP, XS = C3 + '/SLOT_XREF_C3SA.json', '4bd214a83f6f6b1acddd6d1ea6e6f106e20a18a6458e802a75be2b520f4972ce'
ob = H.pin(OLDP, OLDS, 'manifest_draft'); old = H._selected_strict(ob); t = ob.decode('utf-8')
reg = H._selected_strict(H.pin(REGP, REGS, 'registry_v012'))
NEW = {'B0_RO1': A + '/ri33_c3/b0_ro1/B0_RO1_RECORD_C3V001.json', 'B0_N3': A + '/ri33_c3/b0_n3/B0_N3_RECORD_C3V001.json'}
for g, p in NEW.items():
    lst = reg['gate_records'][g]
    assert isinstance(lst, list) and len(lst) == 1 and isinstance(lst[0], str), (g, lst)
    H.pin(p, lst[0], 'gate record ' + g)                      # the file's bytes hash to V012's registered sha
    assert old['gates'][g] is None
for g, p in old['gates'].items():                               # the path form of every other gate: absolute /Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/...
    if p is not None:
        assert p.startswith(A + '/'), (g, p)
out = t
for g, p in NEW.items():
    o = '  "%s": null,\n' % g
    assert out.count(o) == 1, (g, out.count(o))
    out = out.replace(o, '  "%s": %s,\n' % (g, json.dumps(p)))
new = H._selected_strict(out.encode('utf-8'))
assert {k: v for k, v in new.items() if k != 'gates'} == {k: v for k, v in old.items() if k != 'gates'}
assert list(new['gates']) == list(old['gates']) and all(new['gates'][k] == old['gates'][k] for k in old['gates'] if k not in NEW)
assert {k: new['gates'][k] for k in NEW} == NEW
with open(OUTM, 'x') as f:
    f.write(out)
MS = hashlib.sha256(out.encode()).hexdigest()
# SLOT_XREF successor
xb = H.pin(XP, XS, 'slot_xref'); x = json.loads(xb)
assert json.dumps(x, indent=1) + '\n' == xb.decode('utf-8') or json.dumps(x, indent=1) == xb.decode('utf-8'), 'xref formatting not reproducible'
trail = '\n' if xb.decode('utf-8').endswith('\n') else ''
assert x['manifest_gates_only_draft'] == {'path': OLDP, 'sha256': OLDS}
x2 = json.loads(xb)
for g, p in NEW.items():
    x2['cross_reference_not_slots'][g] = {'path': p, 'sha256': reg['gate_records'][g][0], 'registered_in': 'PRODUCER_REGISTRY_C3V012 %s gate_records.%s' % (REGS[:8], g)}
x2['manifest_gates_only_draft'] = {'path': OUTM, 'sha256': MS}
x2['manifest_gates_only_superseded'] = {'path': OLDP, 'sha256': OLDS, 'why': 'gates.B0_RO1 and gates.B0_N3 were null there although V012 registers both pre-seal records (Claude4 0154; root 0667 A123)'}
x2['successor_of'] = {'path': XP, 'sha256': XS, 'changed_only': ['cross_reference_not_slots.B0_RO1', 'cross_reference_not_slots.B0_N3', 'manifest_gates_only_draft', 'manifest_gates_only_superseded', 'successor_of']}
xt = json.dumps(x2, indent=1) + trail
with open(OUTX, 'x') as f:
    f.write(xt)
print(json.dumps({'manifest': {'path': OUTM, 'sha256': MS, 'bytes': len(out.encode())}, 'slot_xref': {'path': OUTX, 'sha256': hashlib.sha256(xt.encode()).hexdigest(), 'bytes': len(xt.encode())},
                  'B0_RO1': [NEW['B0_RO1'], reg['gate_records']['B0_RO1'][0]], 'B0_N3': [NEW['B0_N3'], reg['gate_records']['B0_N3'][0]], 'from': OLDS}, indent=1))
