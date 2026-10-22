"""Claude3 (0646/0647, A110/A111): cross-check of root's SEAL_MANUAL_DISCLOSURES_V001.json from bytes.
(1) e_r6_1_text == SELECTED_R6_C4V001 basis.erratum_E_R6_1 byte for byte; (2) c08_table rows: file sha == r13 f5adfd11, line == first
line carrying the id (token NEW-n not followed by a digit), and completeness: every NEW-n id in r13 appears exactly once in the table;
(3) each root_disclosures text against its addendum entry: every hex token (>=8) and every decimal number in the text must occur in the
entry section (or be explained). Read-only. usage: PY -I -B this OUT_JSON"""
import json, hashlib, re, sys
from pathlib import Path
A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
CTRL = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
DISC = A / 'seal_assembly_c3/root_inputs/SEAL_MANUAL_DISCLOSURES_V001.json'
SEL_R6 = A / 'v007_final_prereg_c4/r6/SELECTED_R6_C4V001.json'
R13 = A / 'v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py'
V005 = CTRL / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V005_ADDENDUM.md'
V006 = CTRL / 'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md'
sha = lambda b: hashlib.sha256(b).hexdigest()
def strict(b):
    def hook(p):
        ks = [k for k, _ in p]
        if len(ks) != len(set(ks)): raise ValueError('DUPLICATE_KEY')
        return dict(p)
    return json.loads(b, object_pairs_hook=hook)
out = {'inputs': {}}
for k, p in (('disclosures', DISC), ('selected_r6', SEL_R6), ('r13', R13), ('v005', V005), ('v006', V006)):
    out['inputs'][k] = {'path': str(p), 'sha256': sha(p.read_bytes())}
assert out['inputs']['disclosures']['sha256'] == 'b9db6fd1716be1e2fb47b6daf9b1e6e81743d6544f9ec72b589cf50fe0fa4ab6'
assert out['inputs']['selected_r6']['sha256'] == '7200acd996755730573ad72d876ff632b8ef59bf86f2b0cf176ae3fceb4403b0'
assert out['inputs']['r13']['sha256'] == 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
assert out['inputs']['v005']['sha256'] == 'c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1'
d = strict(DISC.read_bytes()); r6 = strict(SEL_R6.read_bytes())
e = r6['basis']['erratum_E_R6_1']
out['e_r6_1'] = {'equal_str': d['e_r6_1_text'] == e, 'equal_utf8_bytes': d['e_r6_1_text'].encode() == e.encode(), 'len': len(e)}
src = R13.read_text().splitlines()
first = {}
for i, line in enumerate(src, 1):
    for m in re.finditer(r'NEW-(\d+)(?!\d)', line):
        first.setdefault('NEW-' + m.group(1), i)
rows = d['c08_table']; ids = [r['new_item_id'] for r in rows]
row_checks = []
for r in rows:
    f = A / r['file']
    row_checks.append({'id': r['new_item_id'], 'line': r['line'], 'file_is_r13': f.resolve() == R13.resolve(),
                       'first_line_in_r13': first.get(r['new_item_id']), 'line_ok': first.get(r['new_item_id']) == r['line'],
                       'line_text_has_id': bool(re.search(re.escape(r['new_item_id']) + r'(?!\d)', src[r['line'] - 1])) if 0 < r['line'] <= len(src) else False,
                       'declared_in_r13': r.get('declared_in_r13')})
out['c08'] = {'rows': len(rows), 'ids_in_r13': sorted(first, key=lambda x: int(x.split('-')[1])), 'n_ids_in_r13': len(first),
              'missing_from_table': sorted(set(first) - set(ids)), 'extra_in_table': sorted(set(ids) - set(first)),
              'duplicate_rows': sorted({x for x in ids if ids.count(x) > 1}), 'all_lines_ok': all(c['line_ok'] for c in row_checks),
              'all_files_r13': all(c['file_is_r13'] for c in row_checks), 'row_checks': row_checks}
def section(text, entry):
    m = re.search(r'^(#{1,4})\s*\**%s\b' % re.escape(entry), text, re.M)
    if not m: return None
    lvl = len(m.group(1)); rest = text[m.end():]
    n = re.search(r'^#{1,%d}\s' % lvl, rest, re.M)
    return text[m.start(): m.end() + (n.start() if n else len(rest))]
docs = {'V005': V005.read_text(), 'V006': V006.read_text()}
rd = []
for r in d['root_disclosures']:
    src_doc, entry = r['source'].split()
    sec = section(docs[src_doc], entry)
    toks_hex = sorted(set(re.findall(r'\b[0-9a-f]{8,64}\b', r['text'])))
    toks_num = sorted(set(re.findall(r'(?<![\w.])\d+\.\d+(?:e-?\d+)?(?![\w.])', r['text'])))
    miss_hex = [t for t in toks_hex if sec is None or t not in sec]
    miss_num = [t for t in toks_num if sec is None or t not in sec]
    rd.append({'id': r['id'], 'source': r['source'], 'section_found': sec is not None, 'section_len': len(sec) if sec else 0,
               'hex_tokens': toks_hex, 'hex_not_in_entry': miss_hex, 'num_tokens': toks_num, 'num_not_in_entry': miss_num})
out['root_disclosures'] = rd
with open(sys.argv[1], 'x') as fh: json.dump(out, fh, indent=1)
print(json.dumps({'e_r6_1': out['e_r6_1'], 'c08': {k: v for k, v in out['c08'].items() if k != 'row_checks'}}, indent=1))
for x in rd: print(x['id'], x['source'], 'found', x['section_found'], 'len', x['section_len'], '| hex miss', x['hex_not_in_entry'], '| num miss', x['num_not_in_entry'])
print('bad rows', [c for c in row_checks if not (c['line_ok'] and c['file_is_r13'] and c['line_text_has_id'])])
