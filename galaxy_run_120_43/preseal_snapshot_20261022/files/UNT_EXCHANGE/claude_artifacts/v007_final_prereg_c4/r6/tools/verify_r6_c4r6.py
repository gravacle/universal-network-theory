# Claude4 r6 helper, continuation run 2: an INDEPENDENT verifier of a prereg r6 output set (it imports nothing from the generator; its
# section extractor, leaf differ, Markdown parsers and pin walker are written separately here). Read-only on everything outside OUT_DIR.
# usage: python3 -I -B verify_r6_c4r6.py OUT_DIR RECORD.json
#   OUT_DIR: the r6 folder, or a dry-run folder inside r6/scratch. RECORD.json: a new file inside r6 (exclusive create).
# Checks (each is a named entry in the record; the record's verdict is PASS only if every check passes):
#  V01 the r6 JSON is strict (no duplicate key, no NaN/Infinity) and every output file is UTF-8 and ends in one newline
#  V02 every {path, sha256} pin in r6 (64-hex sha) verifies from bytes; no pin names a protected path (runs_ext, UVT_*, the C5H run, target words)
#  V03 the closed V005: the byte copy and the live file hash to c01b3c51... (143081 bytes); A47-A106 each once; A47-A101 equal to r5's copy
#  V04 the entry table: 25 rows A82-A106 in order; each heading, section sha256 and section size re-derived from the byte copy by a
#      line-based extractor; the 20 r5 rows unchanged; the 5 new rows REVISED_HERE with clauses; addendum_read pins the copy
#  V05 the r5 -> r6 leaf diff equals the DELTA rows: every changed leaf lies in a DELTA clause (a sources item counts for its clause), every
#      DELTA JSON clause changes at least one leaf, and every DELTA row has an A-entry or F-finding in its trace
#  V06 the checklist diff equals the DELTA checklist rows exactly; only the title and the assembly time change in the header
#  V07 both ways between rows A102-A106 and DELTA traces (a clause a row names is changed by an edit traced to it, and the reverse)
#  V08 JSON and Markdown agree: the main MD carries the status, every slot, every seal-record requirement, the entry table, the DELTA list and
#      the open items verbatim; ENTRY_TABLE_R6, ROOT_ITEMS_R6 and CLAUSE_SOURCE_MAP_R6 carry the JSON values
#  V09 binding_inputs.case_block is byte-identical to r5's (76309ae3, r5 path); every seal-slot value is unchanged from r5
#  V10 the named pins the brief fixes (r13, SELECTED_R13, reviews, BUILD_V007, C3V009) and the text conditions of the brief items 1-9
import hashlib, json, math, os, re, sys
from pathlib import Path

R5D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r5')
R6D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/r6')
R5J = R5D / 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R5.json'
R5J_SHA = '3245899f68081a48928a7242a1d9f1ee3694bb13b3f04913dcb2825104a93393'
V005 = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/'
            'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md')
CLOSED = 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'
CLOSED_BYTES = 143081
COPY = R6D / 'addendum_read/V005_ADDENDUM_READ_AT_R6_GENERATION.md'
R5COPY = R5D / 'addendum_read/V005_ADDENDUM_READ_AT_R5_GENERATION.md'
NAMES = ('KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json', 'KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.md', 'ENTRY_TABLE_R6.md', 'SEAL_CHECKLIST_R6.md',
         'ROOT_ITEMS_R6.md', 'CLAUSE_SOURCE_MAP_R6.md', 'DELTA_R5_R6.md')
BRIEF = {'r13': 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157',
         'selected_r13': '10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e',
         'case_block': '76309ae39f23060cc662c4e218a41e1f95c56a26992402218a6198625f85ee71',
         'registry_c3v009': '32ddadcb7567213f42288004f19def122da1d8c4db1a426f0f888bc3242484e8',
         'build_v007_prefix': '94bc05a5', 'claude3_0092_prefix': 'c8277275', 'codex1_0076_prefix': 'd1da986c'}
PROTECTED = re.compile(r'(/runs_ext(/|$)|/uvt_[^/]*/|kmax_a2f10_c5h_run_v001|rotmod|vobs|massmodels|sparc)', re.I)

results = []


def check(name, ok, detail):
    results.append({'check': name, 'pass': bool(ok), 'detail': detail})
    return ok


def H(b):
    return hashlib.sha256(b).hexdigest()


def strict_load(raw):
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('duplicate key %r' % k)
            d[k] = v
        return d

    def bad_const(x):
        raise ValueError('non-finite constant %s' % x)
    return json.loads(raw, object_pairs_hook=hook, parse_constant=bad_const)


def line_sections(b):
    """independent extractor: a section starts at a line beginning '## A<digits>:' and runs to the next line beginning '## ' (or EOF)."""
    lines = b.splitlines(keepends=True)
    out, cur, buf = {}, None, []
    for ln in lines:
        if ln.startswith(b'## '):
            if cur is not None:
                out.setdefault(cur[0], []).append((cur[1], b''.join(buf)))
            m = re.match(rb'## (A[0-9]+):', ln)
            cur = (m.group(1).decode(), ln.rstrip(b'\n').decode()) if m else None
            buf = [ln]
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        out.setdefault(cur[0], []).append((cur[1], b''.join(buf)))
    return out


def flat(o, p=''):
    """independent leaf walker: root_items keyed by id, entries_after_A81.rows keyed by entry."""
    if isinstance(o, dict):
        if not o:
            yield p, '{}'
        for k, v in o.items():
            yield from flat(v, '%s.%s' % (p, k) if p else k)
    elif isinstance(o, list):
        if not o:
            yield p, '[]'
        for i, v in enumerate(o):
            if p == 'root_items' and isinstance(v, dict) and 'id' in v:
                yield from flat(v, '%s.%s' % (p, v['id']))
            elif p == 'entries_after_A81.rows' and isinstance(v, dict) and 'entry' in v:
                yield from flat(v, '%s.%s' % (p, v['entry']))
            else:
                yield from flat(v, '%s[%d]' % (p, i))
    else:
        yield p, json.dumps(o, ensure_ascii=False, sort_keys=True)


def inside(clause, leaf):
    return leaf == clause or leaf.startswith(clause + '.') or leaf.startswith(clause + '[')


def md_table(text, ncols):
    rows = []
    for ln in text.split('\n'):
        if ln.startswith('| ') and ln.endswith(' |') and not ln.startswith('|---'):
            cells = ln[2:-2].split(' | ')
            if len(cells) == ncols:
                rows.append(cells)
    return rows


def pins(o, p=''):
    if isinstance(o, dict):
        if 'path' in o and 'sha256' in o and isinstance(o['path'], str):
            yield p, o['path'], o['sha256']
        elif 'copy' in o and 'sha256' in o and isinstance(o['copy'], str):      # the V005 read records {read, sha256, copy}
            yield p, o['copy'], o['sha256']
        for k, v in o.items():
            yield from pins(v, '%s.%s' % (p, k) if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from pins(v, '%s[%d]' % (p, i))


def main():
    out = Path(sys.argv[1]).resolve()
    rec_path = Path(sys.argv[2]).resolve()
    if not (out == R6D or str(out).startswith(str(R6D / 'scratch') + '/')):
        raise SystemExit('OUT_DIR must be r6 or inside r6/scratch')
    if not str(rec_path).startswith(str(R6D) + '/') or os.path.lexists(rec_path):
        raise SystemExit('RECORD must be a new file inside r6')
    raw5 = R5J.read_bytes()
    if H(raw5) != R5J_SHA:
        raise SystemExit('r5 pin')
    d5 = strict_load(raw5)
    files = {n: (out / n).read_bytes() for n in NAMES}
    # V01
    bad = []
    for n, b in files.items():
        try:
            b.decode('utf-8')
        except UnicodeDecodeError:
            bad.append(n + ': not UTF-8')
        if not b.endswith(b'\n') or b.endswith(b'\n\n\n'):
            bad.append(n + ': trailing newline')
    try:
        d6 = strict_load(files['KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.json'])
    except ValueError as e:
        check('V01_strict_json_and_text', False, str(e))
        raise SystemExit('r6 JSON unreadable')
    check('V01_strict_json_and_text', not bad, bad or 'r6 JSON strict; 7 files UTF-8 with a final newline')
    texts = {n: b.decode('utf-8') for n, b in files.items()}
    # V02 pins
    pl = list(pins(d6))
    bad, prot, n_hex, n_other = [], [], 0, 0
    for where, path, s in pl:
        if not (isinstance(s, str) and re.fullmatch(r'[0-9a-f]{64}', s)):
            n_other += 1
            continue
        n_hex += 1
        if PROTECTED.search(path) or any(c.casefold().startswith('uvt_') for c in Path(path).parts[:-1]):
            prot.append(where)
            continue
        p = Path(path)
        if not p.is_file() or H(p.read_bytes()) != s:
            bad.append(where)
    check('V02_pins_from_bytes', not bad and not prot and n_hex > 180,
          {'pins_checked': n_hex, 'non_hex_sha_values': n_other, 'mismatch': bad, 'protected': prot})
    # V03 closed V005
    cb = COPY.read_bytes()
    live = H(V005.read_bytes())
    sec6 = line_sections(cb)
    dup = [k for k, v in sec6.items() if len(v) != 1]
    nums = sorted(int(k[1:]) for k in sec6)
    b5 = R5COPY.read_bytes()
    sec5 = line_sections(b5)
    same = all(sec5[k] == sec6.get(k) for k in sec5)
    pre_ok = b5[:b5.index(b'\n## A') + 1] == cb[:cb.index(b'\n## A') + 1]
    check('V03_closed_v005', H(cb) == CLOSED and len(cb) == CLOSED_BYTES and live == CLOSED and not dup and nums == list(range(47, 107)) and same and pre_ok,
          {'copy_sha256': H(cb), 'copy_bytes': len(cb), 'live_sha256': live, 'entries': '%d (A%d-A%d)' % (len(nums), nums[0], nums[-1]),
           'duplicates': dup, 'A47_A101_equal_to_r5_copy': same, 'preamble_equal': pre_ok})
    # V04 entry table
    ea6, ea5 = d6['entries_after_A81'], d5['entries_after_A81']
    rows6 = ea6['rows']
    order_ok = [r['entry'] for r in rows6] == ['A%d' % n for n in range(82, 107)]
    rehash_bad = []
    for r in rows6:
        head, body = sec6[r['entry']][0]
        if r['heading'] != head or r['section_sha256'] != H(body) or r['section_bytes'] != len(body):
            rehash_bad.append(r['entry'])
    r5_same = rows6[:20] == ea5['rows']
    new_ok = all(r['decision'] == 'REVISED_HERE' and r['revised_clauses'] and r.get('scope') and r['sources'] == [r['entry']] for r in rows6[20:])
    ar = ea6['addendum_read']
    ar_ok = (set(ar) == {'open_path', 'sha256_at_generation', 'bytes', 'byte_copy'} and ar['sha256_at_generation'] == CLOSED and ar['bytes'] == CLOSED_BYTES
             and ar['byte_copy'].startswith(str(COPY) + ' ') and ar['open_path'] == str(V005))
    check('V04_entry_table', order_ok and not rehash_bad and r5_same and new_ok and ar_ok,
          {'rows': len(rows6), 'order_A82_A106': order_ok, 'rehash_mismatch': rehash_bad, 'r5_rows_unchanged': r5_same, 'new_rows_revised_here': new_ok,
           'addendum_read_pins_the_copy': ar_ok, 'rows_rehashed_from_the_copy': len(rows6) - len(rehash_bad)})
    # DELTA parse
    drows = md_table(texts['DELTA_R5_R6.md'], 7)
    if drows and drows[0][0] == '#':
        drows = drows[1:]
    delta = [{'n': int(r[0]), 'item': r[1], 'clause': r[2].strip('`'), 'kind': r[3], 'added': r[4], 'trace': [t for t in r[5].split('; ') if t], 'why': r[6]}
             for r in drows]
    seq_ok = [x['n'] for x in delta] == list(range(1, len(delta) + 1))
    tr_ok = all(any(re.match(r'(A\d+|F-\d+)', t) for t in x['trace']) for x in delta)
    # V05 leaf diff
    L5, L6 = dict(flat(d5)), dict(flat(d6))
    changed = sorted(k for k in set(L5) | set(L6) if L5.get(k) != L6.get(k))
    jcl = [x['clause'] for x in delta if not x['clause'].startswith('SEAL_CHECKLIST_R6') and x['clause'] != 'root_items (order)']
    outside = []
    for k in changed:
        if any(inside(c, k) for c in jcl):
            continue
        m = re.match(r'(.+)\.sources\[\d+\]$', k)
        if m and any(c == m.group(1) or c.startswith(m.group(1) + '.') for c in jcl):
            continue
        outside.append(k)
    idle = [c for c in jcl if not any(inside(c, k) for k in changed)]
    order5 = [x['id'] for x in d5['root_items']]
    order6 = [x['id'] for x in d6['root_items']]
    order_row = any(x['clause'] == 'root_items (order)' for x in delta)
    check('V05_leaf_diff_equals_delta', seq_ok and tr_ok and not outside and not idle and (order_row == (order5 != order6)),
          {'leaves_changed': len(changed), 'delta_rows': len(delta), 'json_delta_clauses': len(jcl), 'outside_delta': outside[:10],
           'delta_clauses_without_change': idle, 'every_trace_has_a_ruling_or_finding': tr_ok, 'root_items_reordered': order5 != order6,
           'order_row_present': order_row})
    # V06 checklist
    def ck_parse(t):
        L = t.split('\n')
        return L[0], L[2], md_table('\n'.join(L[6:]), 3)
    t5, s5, c5 = ck_parse((R5D / 'SEAL_CHECKLIST_R5.md').read_text())
    t6, s6, c6 = ck_parse(texts['SEAL_CHECKLIST_R6.md'])

    def step(cell):
        m = re.match(r'(?:\*\*)?([ABC][0-9]+[a-z]?)\. ', cell)
        if m:
            return m.group(1)
        if cell.startswith('Compare r8, r10, r11'):
            return 'SUPERSEDED'
        return cell[:24]
    ch_steps = sorted(step(a[0]) for a, b in zip(c5, c6) if a != b) if len(c5) == len(c6) else None
    d_steps = sorted(x['clause'][len('SEAL_CHECKLIST_R6 '):] for x in delta if x['clause'].startswith('SEAL_CHECKLIST_R6 ') and x['clause'] != 'SEAL_CHECKLIST_R6 header')
    head_ok = (t5.replace('r5', 'r6', 1) == t6 and re.sub(r'\(.*?Z\)', '()', s5, count=1) == re.sub(r'\(.*?Z\)', '()', s6, count=1)
               and any(x['clause'] == 'SEAL_CHECKLIST_R6 header' for x in delta))
    check('V06_checklist_diff_equals_delta', ch_steps == d_steps and head_ok,
          {'rows_r5': len(c5), 'rows_r6': len(c6), 'changed_steps': ch_steps, 'delta_steps': d_steps, 'header_only_title_and_time': head_ok})
    # V07 both ways
    rowsby = {r['entry']: r for r in rows6[20:]}

    def ents(trace):
        return {m.group(1) for t in trace for m in [re.match(r'(A1\d\d)(\.\d+)?$', t)] if m and m.group(1) in rowsby}
    probs = []
    for e, r in rowsby.items():
        steps = []
        for cl in r['revised_clauses']:
            if cl.startswith('SEAL_CHECKLIST_R6 '):
                steps += [s.strip() for s in cl[len('SEAL_CHECKLIST_R6 '):].split(',')]
            elif not any(e in ents(x['trace']) and (inside(cl, x['clause']) or inside(x['clause'], cl)) for x in delta):
                probs.append('%s names %s without a traced edit' % (e, cl))
        for s in steps:
            if not any(x['clause'] == 'SEAL_CHECKLIST_R6 ' + s and e in ents(x['trace']) for x in delta):
                probs.append('%s names checklist %s without a traced edit' % (e, s))
    for x in delta:
        if x['clause'] in ('root_items (order)', 'SEAL_CHECKLIST_R6 header'):
            continue
        for e in ents(x['trace']):
            r = rowsby[e]
            if x['clause'].startswith('SEAL_CHECKLIST_R6 '):
                st = x['clause'][len('SEAL_CHECKLIST_R6 '):]
                if not any(cl.startswith('SEAL_CHECKLIST_R6 ') and st in [s.strip() for s in cl[len('SEAL_CHECKLIST_R6 '):].split(',')] for cl in r['revised_clauses']):
                    probs.append('edit %s traced to %s, not named there' % (x['clause'], e))
            elif not any(inside(cl, x['clause']) for cl in r['revised_clauses'] if not cl.startswith('SEAL_CHECKLIST_R6 ')):
                probs.append('edit %s traced to %s, not named there' % (x['clause'], e))
    check('V07_rows_and_traces_both_ways', not probs, probs or 'every row clause has an edit traced to its entry, and the reverse')
    # V08 JSON <-> Markdown
    md = texts['KMAX_TAIL_PREREG_V007_FINAL_DRAFT_R6.md']
    miss = []
    if d6['status'] not in md:
        miss.append('status')
    for k, s in d6['seal_slots'].items():
        if ('- **%s**: value `%s`. %s  \n  *Sources: %s*' % (k, s['value'], s['rule'], '; '.join(s['sources']))) not in md:
            miss.append('slot ' + k)
    for i, x in enumerate(d6['seal_record_requirements']):
        if ('- %s *(%s)*' % (x['text'], '; '.join(x['sources']))) not in md:
            miss.append('srr %d' % i)
    for r in rows6:
        if ('| %s | %s | `%s...` |' % (r['entry'], 'revised here' if r['decision'] == 'REVISED_HERE' else 'no change', r['section_sha256'][:16])) not in md:
            miss.append('md row ' + r['entry'])
    for x in delta:
        if ('- `%s` (%s; item %s; trace %s): %s' % (x['clause'], x['kind'], x['item'], ', '.join(x['trace']), x['why'])) not in md:
            miss.append('md change %d' % x['n'])
    opened = [x['id'] for x in d6['root_items'] if x['status'] == 'OPEN']
    if ('OPEN: %s (see `ROOT_ITEMS_R6.md`).' % ', '.join(opened)) not in md:
        miss.append('md open list')
    et = md_table(texts['ENTRY_TABLE_R6.md'], 4)
    et = [r for r in et if r[0] != 'entry']
    for r, x in zip(rows6, et):
        lab = 'revised here' if r['decision'] == 'REVISED_HERE' else 'no change'
        body = ('%s. Clauses: %s' % (r['scope'].rstrip('.'), ', '.join('`%s`' % c for c in r['revised_clauses']))) if r['decision'] == 'REVISED_HERE' else r['reason']
        if x != [r['entry'], lab, '`%s`' % r['section_sha256'], body]:
            miss.append('entry table ' + r['entry'])
    if len(et) != len(rows6):
        miss.append('entry table row count %d' % len(et))
    rim = texts['ROOT_ITEMS_R6.md']
    pos = -1
    for x in d6['root_items']:
        h = '## %s: %s (%s)\n\n- **Status:** %s\n- **Clause:** `%s`\n- **Issue:** %s\n- **Draft:** %s\n' % (
            x['id'], x['kind'], 'OPEN' if x['status'] == 'OPEN' else 'RESOLVED', x['status'], x['clause'], x['issue'], x['draft'])
        q = rim.find(h)
        if q <= pos:
            miss.append('root item ' + x['id'])
        pos = max(pos, q)
        if ('- **Sources:** %s\n' % '; '.join(x['sources'])) not in rim[q:]:
            miss.append('root item sources ' + x['id'])
    cmap = {r[0].strip('`'): r[1] for r in md_table(texts['CLAUSE_SOURCE_MAP_R6.md'], 3) if r[0] != 'clause'}
    srcs = {'seal_slots.' + k: s['sources'] for k, s in d6['seal_slots'].items()}
    srcs.update({'seal_record_requirements[%d]' % i: x['sources'] for i, x in enumerate(d6['seal_record_requirements'])})
    srcs['not_v007_text_scope'] = d6['not_v007_text_scope']['sources']
    srcs.update({'entries_after_A81.%s (%s)' % (r['entry'], r['decision']): r['sources'] for r in rows6})
    srcs['fixed_across_all_cases.production_tail.ngc_gas_M_s'] = d6['fixed_across_all_cases']['production_tail']['ngc_gas_M_s']['sources']
    srcs['binding_inputs.case_block_rule'] = d6['binding_inputs']['case_block_rule']['sources']
    for k, s in srcs.items():
        if cmap.get(k) != '; '.join(s):
            miss.append('clause map ' + k)
    check('V08_json_and_markdown_agree', not miss, miss or 'status, %d slots, %d requirements, %d table rows, %d changes, %d root items, %d map rows' % (
        len(d6['seal_slots']), len(d6['seal_record_requirements']), len(rows6), len(delta), len(d6['root_items']), len(srcs)))
    # V09 case block and slot values
    cb5, cb6 = d5['binding_inputs']['case_block'], d6['binding_inputs']['case_block']
    cb_ok = cb5 == cb6 and cb6['sha256'] == BRIEF['case_block'] and cb6['path'].startswith(str(R5D) + '/') and H(Path(cb6['path']).read_bytes()) == BRIEF['case_block']
    vals_ok = {k: s['value'] for k, s in d5['seal_slots'].items()} == {k: s['value'] for k, s in d6['seal_slots'].items()}
    check('V09_case_block_and_slot_values_unchanged', cb_ok and vals_ok, {'case_block': cb6, 'slot_values_unchanged': vals_ok})
    # V10 named pins and brief text conditions
    cp = d6['seal_slots']['compare']
    nc = cp['named_candidates_verified_from_bytes']
    lp = d6['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']
    pr = d6['seal_slots']['producer_registry']['named_candidates_verified_from_bytes']
    srr = d6['seal_record_requirements']
    ckt = texts['SEAL_CHECKLIST_R6.md']
    conds = {
        'compare_r13_pin': nc['r13_cx3v001_final_round']['sha256'] == BRIEF['r13'],
        'compare_selected_r13_pin': nc['r13_selection']['sha256'] == BRIEF['selected_r13'],
        'compare_reviews_of_record': nc['delta_review_of_record_Claude3_0092']['sha256'].startswith(BRIEF['claude3_0092_prefix'])
        and nc['delta_review_of_record_Codex1_0076']['sha256'].startswith(BRIEF['codex1_0076_prefix']),
        'compare_r12_superseded': 'superseded (A102)' in nc['r12_superseded_A102']['note'] and 'r12_cx3v002_final_round' not in nc,
        'F02_no_ruling_route': 'or a ruling' not in cp['rule'] and 'never a seal on that round' in cp['rule']
        and 'A81 RI-20, as applied by A83, A86, A91, A96, A102, A103, A104' in cp['rule'],
        'compare_value_pending': cp['value'] == 'PENDING_ROOT_AT_SEAL_ASSEMBLY' and 'only the five A82 pins on top of r13' in cp['rule'],
        'launch_packet_build_v007': lp['build']['sha256'].startswith(BRIEF['build_v007_prefix']) and 'W7-S1' in d6['seal_slots']['launch_packet']['rule']
        and 'RP-S1' in d6['seal_slots']['launch_packet']['rule'] and 'RP-S2' in d6['seal_slots']['launch_packet']['rule'] and '80 GB' in d6['seal_slots']['launch_packet']['rule'],
        'registry_c3v009_candidate': pr['C3V009_candidate']['sha256'] == BRIEF['registry_c3v009'] and 'C3V008_superseded' in pr,
        'srr0_e_ops5': 'E-OPS5' in srr[0]['text'] and 'E-SEAL1' in srr[0]['text'],
        'srr4_driver_build_record': 'the r5 driver BUILD record (PIN_DRIVER_BUILD_RECORD' in srr[4]['text'],
        'srr13_c02_c08': srr[13]['text'].startswith('A106.2:') and all(c in srr[13]['text'] for c in ('C-02', 'C-03', 'C-04', 'C-05', 'C-06', 'C-07', 'C-08')),
        'srr11_closed_and_v003': CLOSED in srr[11]['text'] and 'seal_tools_v003/' in srr[11]['text'] and '--addendum-at-text-of-record' in srr[11]['text'],
        'entries_rule_closed_v006': 'A82-A106' in ea6['rule'] and 'A106.3' in ea6['rule'] and 'V006 addendum' in ea6['rule'] and 'not V005 entries' in ea6['rule'],
        'no_r12_line_citations_left': all(s not in json.dumps({k: v for k, v in d6.items() if k not in ('entries_after_A81', 'assembly')}, ensure_ascii=False)
                                          for s in ('r12 L5706', '(r12 cx3v002 L5706)', 'r12 GATE_RECORD', 'every other gate (r12)')),
        'r13_line_citations': '(r13 cx3v001 L5708)' in d6['binding_inputs']['case_block_rule']['text'] and '(r13 L5708)' in d6['fixed_across_all_cases']['validity_gates']['text'],
        'b2_separator': '(<= 0.05 km/s). A94:' in d6['gates_before_any_T_result']['B2']['text'],
        'ri20_ri21_pointers': all(a in [x for x in d6['root_items'] if x['id'] == 'RI-20'][0]['status'] for a in ('A83', 'A102', 'A104'))
        and 'A83' in [x for x in d6['root_items'] if x['id'] == 'RI-21'][0]['status'],
        'f13_ngc_ms': 'checklist A7' in d6['fixed_across_all_cases']['production_tail']['ngc_gas_M_s']['text']
        and 'be148bab' in d6['fixed_across_all_cases']['production_tail']['ngc_gas_M_s']['text'],
        'checklist_A1_r13': '| A1. Final compare round r13 cx3v001 (f5adfd11' in ckt,
        'checklist_B1_closed_bytes_and_rows': CLOSED in ckt.split('| B1. ')[1].split('\n')[0] and 'A47-A106' in ckt.split('| B1. ')[1].split('\n')[0]
        and 'none at r5 generation' not in ckt,
        'checklist_B2a_r13': "compare r13's builtin_r5_build()" in ckt,
        'revision_r6': d6['revision'] == 'r6' and d6['supersedes_draft'] == {'path': str(R5J), 'sha256': R5J_SHA},
        'cites_A47_A106': d6['cites_by_name'][0].startswith('ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM: A47-A106 '),
        'no_c5h_run_name_in_new_text': 'KMAX_A2F10_C5H_RUN_V001' not in json.dumps(d6, ensure_ascii=False)
        or 'KMAX_A2F10_C5H_RUN_V001' in json.dumps(d5, ensure_ascii=False),
    }
    check('V10_brief_pins_and_text', all(conds.values()), {k: v for k, v in conds.items()})
    verdict = 'PASS' if all(r['pass'] for r in results) else 'FAIL'
    rec = {'schema': 'UNT_V007_PREREG_R6_VERIFY_C4R6V001', 'verdict': verdict, 'out_dir': str(out),
           'files': {n: H(b) for n, b in files.items()}, 'r5': {'path': str(R5J), 'sha256': R5J_SHA},
           'v005_copy': {'path': str(COPY), 'sha256': H(cb)}, 'checks': results}
    data = (json.dumps(rec, indent=1, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
    with open(rec_path, 'xb') as f:
        f.write(data)
    print(json.dumps({'verdict': verdict, 'record': str(rec_path), 'record_sha256': H(data),
                      'checks': {r['check']: r['pass'] for r in results}}, indent=1))
    sys.exit(0 if verdict == 'PASS' else 1)


if __name__ == '__main__':
    main()
