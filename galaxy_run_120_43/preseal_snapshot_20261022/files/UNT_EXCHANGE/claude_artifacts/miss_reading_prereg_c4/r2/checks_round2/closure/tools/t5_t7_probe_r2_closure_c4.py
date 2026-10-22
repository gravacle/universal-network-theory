# R2-A closure lens (B-6 / A-11 / L-C11 closure): replicate the ROUND-2 check's T5 (V005 per-entry pins) and T7 (currency) logic
# with the tool's OWN functions, on in-memory variants of a V005 snapshot kept in this lens folder. Nothing is written except --out.
import hashlib, json, sys
R2T, prereg_path, v005_path, outp = sys.argv[1:5]
sys.path.insert(0, R2T)
import check_target_free_c4v002 as T
prereg = open(prereg_path, 'rb').read().decode('utf-8')
base = open(v005_path, 'rb').read().decode('utf-8')

def t5_t7(v):
    pins = T.v005_entry_pins(prereg)
    markers = {n: mk for n, mk, _ in pins if mk}
    secs = T.entry_sections(v, markers)
    bad = []
    for n, mk, eh in pins:
        found = secs.get(n, [])
        if len(found) != 1 or found[0] is None:
            bad.append('A%d sections/marker' % n); continue
        if hashlib.sha256(found[0].encode('utf-8')).hexdigest() != eh:
            bad.append('A%d changed' % n)
    cited = {n for n, _, _ in pins}
    nochange = T.no_change_list(prereg)
    heads = sorted(set(n for n in T.all_headings(v) if n >= 47))
    later = ['A%d' % n for n in heads if n not in cited and n not in nochange]
    return {'T5_pass': not bad, 'T5_problems': bad, 'T7_pass': not later, 'T7_later': later}

def insert_before(v, anchor, text):
    i = v.index(anchor)
    return v[:i] + text + v[i:]

def append_in_section(v, heading_prefix, text):
    # append text at the end of the named section (just before the next '## ' line)
    i = v.index('\n' + heading_prefix) + 1
    j = v.find('\n## ', i + 1)
    j = len(v) if j < 0 else j + 1
    return v[:j] + text + v[j:]

top = base.split('\n## ', 1)
first_head = '## ' + base.split('\n## ')[1].split('\n')[0]
# root inserts new entries just above the newest one; find the first heading after A77 (the insertion point used for A90-A98)
ins_anchor = '\n## A98:' if '\n## A98:' in base else '\n## A96:'
variants = {
    'baseline': base,
    'X1_new_heading_A99': insert_before(base, ins_anchor, '\n## A99: synthetic probe entry, amends A81 RI-23 (closure lens)\n\nsynthetic.\n'),
    'X2_inplace_edit_cited_A66': append_in_section(base, '## A66:', 'Synthetic probe: A66.2 is withdrawn.\n\n'),
    'X3_inplace_edit_nochange_A91': append_in_section(base, '## A91:', 'Synthetic probe: A66.2 is withdrawn; R-TSR is dropped.\n\n'),
    'X4_suffix_heading_A81a': insert_before(base, ins_anchor, '\n## A81a: synthetic probe, amends RI-23 (closure lens)\n\nsynthetic.\n'),
    'X5_heading_A66_amendment': insert_before(base, ins_anchor, '\n## A66 amendment: synthetic probe, withdraws A66.2 (closure lens)\n\nsynthetic.\n'),
    'X6_append_at_EOF_plain_text': base + '\n**Synthetic probe (closure lens).** A66.2 is withdrawn; N_FAIL_N1 now blocks route A/B.\n',
    'X7_edit_inside_A65_trailing_block': base.replace('N_PASS is only an input to NGC route A/B.', 'N_PASS is the only input to NGC route A/B.', 1),
    'X8_inplace_edit_nochange_A47_I3': append_in_section(base, '## A47:', 'Synthetic probe: RA13 blinding (I3) is withdrawn.\n\n'),
}
out = {'v005_snapshot_sha256': hashlib.sha256(base.encode('utf-8')).hexdigest(), 'cases': {}}
for k, v in variants.items():
    assert k == 'baseline' or v != base, k
    out['cases'][k] = t5_t7(v)
with open(outp, 'x') as f:
    f.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
print(json.dumps(out, indent=1, sort_keys=True))
