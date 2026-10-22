# Claude4 lens_diff (review of compare r14, dispatch 0651, A114): byte, line, token and AST diff of r14 vs r13.
# Reads two author files read-only; writes only into this review folder (exclusive 'x' writes).
import ast, difflib, hashlib, io, json, sys, tokenize
from pathlib import Path

R13 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r13/kmax_tail_compare_c2v007_r13_cx3v001.py')
R14 = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py')
SHA13 = 'f5adfd11ea7ecc982ba7650944f6a6d69eeff8be690bde6265a18d07d3bb2157'
SHA14 = 'f3f9ba7ec4439933ab88c7623a6ede5b04763b83f0610b1917393362f33c67d7'
OUT = Path(__file__).resolve().parent.parent / 'out' / 'DIFF_R13_R14_C4.json'

b13 = R13.read_bytes(); b14 = R14.read_bytes()
s13 = hashlib.sha256(b13).hexdigest(); s14 = hashlib.sha256(b14).hexdigest()
res = {'r13': {'path': str(R13), 'sha256': s13, 'bytes': len(b13), 'sha_ok': s13 == SHA13},
       'r14': {'path': str(R14), 'sha256': s14, 'bytes': len(b14), 'sha_ok': s14 == SHA14}}
if not (res['r13']['sha_ok'] and res['r14']['sha_ok']):
    print(json.dumps(res, indent=1)); raise SystemExit('SHA MISMATCH - stop')

# --- byte level
res['byte_len_delta'] = len(b14) - len(b13)
# common prefix / suffix
p = 0
while p < min(len(b13), len(b14)) and b13[p] == b14[p]:
    p += 1
s = 0
while s < min(len(b13), len(b14)) - p and b13[-1 - s] == b14[-1 - s]:
    s += 1
res['byte_common_prefix'] = p
res['byte_common_suffix'] = s
res['byte_r13_middle'] = b13[p:len(b13) - s].decode('utf-8', 'replace')
res['byte_r14_middle'] = b14[p:len(b14) - s].decode('utf-8', 'replace')

# --- line level
L13 = b13.split(b'\n'); L14 = b14.split(b'\n')
res['line_count_r13'] = len(L13); res['line_count_r14'] = len(L14)
res['newline_count_r13'] = b13.count(b'\n'); res['newline_count_r14'] = b14.count(b'\n')
res['crlf_r13'] = b13.count(b'\r'); res['crlf_r14'] = b14.count(b'\r')
sm = difflib.SequenceMatcher(a=L13, b=L14, autojunk=False)
ops = [op for op in sm.get_opcodes() if op[0] != 'equal']
res['line_opcodes'] = [{'tag': t, 'r13_lines': [i1 + 1, i2], 'r14_lines': [j1 + 1, j2],
                        'r13_text': [x.decode() for x in L13[i1:i2]], 'r14_text': [x.decode() for x in L14[j1:j2]]}
                       for (t, i1, i2, j1, j2) in ops]
same_line_numbers = all(t == 'replace' and (i2 - i1) == (j2 - j1) and i1 == j1 for (t, i1, i2, j1, j2) in ops)
res['every_line_keeps_its_number'] = same_line_numbers and len(L13) == len(L14)
res['unified_diff'] = ''.join(difflib.unified_diff([x.decode() + '\n' for x in L13], [x.decode() + '\n' for x in L14],
                                                    'r13', 'r14', n=0))

# --- exact inverse: replace the single changed r14 line by the r13 line and hash
inv_ok = None
if len(ops) == 1 and ops[0][0] == 'replace' and ops[0][2] - ops[0][1] == 1 and ops[0][4] - ops[0][3] == 1:
    t, i1, i2, j1, j2 = ops[0]
    new_line = L14[j1]; old_line = L13[i1]
    assert b14.count(new_line) == 1, 'changed line not unique in r14'
    inv = b14.replace(new_line, old_line, 1)
    inv_sha = hashlib.sha256(inv).hexdigest()
    inv_ok = inv_sha == SHA13
    res['inverse'] = {'method': 'bytes.replace(r14_changed_line, r13_line, 1) with the r14 changed line unique in r14',
                      'inverse_sha256': inv_sha, 'equals_f5adfd11': inv_ok, 'inverse_bytes': len(inv)}
    # forward too: apply to r13 and check equals r14
    fwd = b13.replace(old_line, new_line, 1)
    res['forward'] = {'r13_line_unique_in_r13': b13.count(old_line) == 1,
                      'forward_sha256': hashlib.sha256(fwd).hexdigest(), 'equals_f3f9ba7e': hashlib.sha256(fwd).hexdigest() == SHA14}
    # the r14 line equals r13 line with ", 'I4'" inserted before the closing paren
    res['line_is_r13_plus_I4_last'] = (new_line == old_line[:-1] + b", 'I4')" and old_line.endswith(b')'))
else:
    res['inverse'] = {'note': 'more than one changed line; inverse not single-line', 'ops': len(ops)}

# --- token level: compare every token incl. comments
def toks(b):
    return [(tokenize.tok_name[t.type], t.string, t.start, t.end) for t in tokenize.tokenize(io.BytesIO(b).readline)]
T13 = toks(b13); T14 = toks(b14)
res['token_count_r13'] = len(T13); res['token_count_r14'] = len(T14)
C13 = [(t[1], t[2][0]) for t in T13 if t[0] == 'COMMENT']; C14 = [(t[1], t[2][0]) for t in T14 if t[0] == 'COMMENT']
res['comment_count_r13'] = len(C13); res['comment_count_r14'] = len(C14)
res['comments_identical_text_and_line'] = C13 == C14
tsm = difflib.SequenceMatcher(a=[(t[0], t[1]) for t in T13], b=[(t[0], t[1]) for t in T14], autojunk=False)
res['token_opcodes'] = [{'tag': t, 'r13': [(T13[k][0], T13[k][1], T13[k][2]) for k in range(i1, i2)],
                         'r14': [(T14[k][0], T14[k][1], T14[k][2]) for k in range(j1, j2)]}
                        for (t, i1, i2, j1, j2) in tsm.get_opcodes() if t != 'equal']
# string-literal tokens (docstrings etc.)
S13 = [t[1] for t in T13 if t[0] == 'STRING']; S14 = [t[1] for t in T14 if t[0] == 'STRING']
res['string_tokens_r13'] = len(S13); res['string_tokens_r14'] = len(S14)
res['string_token_multiset_delta'] = {'only_r14': sorted(set(S14) - set(S13)), 'only_r13': sorted(set(S13) - set(S14))}

# --- AST level
A13 = ast.parse(b13); A14 = ast.parse(b14)
res['top_level_nodes_r13'] = len(A13.body); res['top_level_nodes_r14'] = len(A14.body)
def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign):
        return ','.join(ast.unparse(t) for t in n.targets)
    if isinstance(n, ast.AnnAssign):
        return ast.unparse(n.target)
    return type(n).__name__ + '@' + str(getattr(n, 'lineno', '?'))
changed = []
pos_changed = []
for a, b in zip(A13.body, A14.body):
    if ast.dump(a, include_attributes=False) != ast.dump(b, include_attributes=False):
        changed.append({'node': nm(a), 'r13_lineno': a.lineno, 'r14_lineno': b.lineno,
                        'r13': ast.unparse(a), 'r14': ast.unparse(b)})
    if (a.lineno, a.end_lineno, a.col_offset, a.end_col_offset) != (b.lineno, b.end_lineno, b.col_offset, b.end_col_offset):
        pos_changed.append({'node': nm(a), 'r13': [a.lineno, a.end_lineno, a.col_offset, a.end_col_offset],
                            'r14': [b.lineno, b.end_lineno, b.col_offset, b.end_col_offset]})
res['ast_changed_top_level_nodes'] = changed
res['ast_top_level_position_changes'] = pos_changed
res['ast_names_r13_eq_r14'] = [nm(n) for n in A13.body] == [nm(n) for n in A14.body]
# all-node position comparison (every node with lineno anywhere)
def allpos(t):
    out = []
    for n in ast.walk(t):
        if hasattr(n, 'lineno'):
            out.append((type(n).__name__, n.lineno, getattr(n, 'end_lineno', None), n.col_offset, getattr(n, 'end_col_offset', None)))
    return out
P13 = allpos(A13); P14 = allpos(A14)
res['all_ast_nodes_with_pos_r13'] = len(P13); res['all_ast_nodes_with_pos_r14'] = len(P14)
psm = difflib.SequenceMatcher(a=P13, b=P14, autojunk=False)
res['all_node_position_diffs'] = [{'tag': t, 'r13': P13[i1:i2], 'r14': P14[j1:j2]} for (t, i1, i2, j1, j2) in psm.get_opcodes() if t != 'equal']
# function / class inventory with line spans
def inv_defs(t):
    out = {}
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.setdefault(n.name, []).append([n.lineno, n.end_lineno, hashlib.sha256(ast.dump(n).encode()).hexdigest()[:16]])
    return out
D13 = inv_defs(A13); D14 = inv_defs(A14)
res['def_count_r13'] = sum(len(v) for v in D13.values()); res['def_count_r14'] = sum(len(v) for v in D14.values())
res['defs_identical_incl_lines_and_ast'] = D13 == D14
# module-level constant inventory
def consts(t):
    out = {}
    for n in t.body:
        if isinstance(n, ast.Assign):
            for tg in n.targets:
                out[ast.unparse(tg)] = hashlib.sha256(ast.dump(n.value).encode()).hexdigest()[:16]
        elif isinstance(n, ast.AnnAssign):
            out[ast.unparse(n.target)] = hashlib.sha256(ast.dump(n.value).encode()).hexdigest()[:16] if n.value else None
    return out
K13 = consts(A13); K14 = consts(A14)
res['module_constants_r13'] = len(K13); res['module_constants_r14'] = len(K14)
res['module_constants_differing'] = sorted(k for k in set(K13) | set(K14) if K13.get(k) != K14.get(k))

# --- every reference to GATE_RECORD_AFTER_SEAL_ALLOWED in r14 (where the tuple is consumed)
refs = []
for n in ast.walk(A14):
    if isinstance(n, ast.Name) and n.id == 'GATE_RECORD_AFTER_SEAL_ALLOWED':
        refs.append({'lineno': n.lineno, 'ctx': type(n.ctx).__name__, 'line': L14[n.lineno - 1].decode().strip()[:220]})
res['refs_GATE_RECORD_AFTER_SEAL_ALLOWED_r14'] = refs
# literal value of the tuple in both
for tag, t in (('r13', A13), ('r14', A14)):
    for n in t.body:
        if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'GATE_RECORD_AFTER_SEAL_ALLOWED' for x in n.targets):
            res['GATE_RECORD_AFTER_SEAL_ALLOWED_' + tag] = ast.literal_eval(n.value)
            res['GATE_RECORD_AFTER_SEAL_ALLOWED_' + tag + '_lineno'] = n.lineno
# other module text containing the literal token 'I4'
res['r14_lines_with_I4_token'] = [[i + 1, x.decode().strip()[:200]] for i, x in enumerate(L14) if b"'I4'" in x or b'"I4"' in x]
res['r13_lines_with_I4_token'] = [[i + 1, x.decode().strip()[:200]] for i, x in enumerate(L13) if b"'I4'" in x or b'"I4"' in x]

with open(OUT, 'x') as f:
    json.dump(res, f, indent=1, default=str)
summary = {k: res[k] for k in ('byte_len_delta', 'byte_common_prefix', 'byte_common_suffix', 'byte_r13_middle', 'byte_r14_middle',
                                'line_count_r13', 'line_count_r14', 'every_line_keeps_its_number', 'inverse', 'forward',
                                'line_is_r13_plus_I4_last', 'comment_count_r13', 'comment_count_r14',
                                'comments_identical_text_and_line', 'top_level_nodes_r13', 'top_level_nodes_r14',
                                'ast_names_r13_eq_r14', 'def_count_r13', 'def_count_r14', 'defs_identical_incl_lines_and_ast',
                                'module_constants_r13', 'module_constants_r14', 'module_constants_differing',
                                'string_token_multiset_delta', 'token_count_r13', 'token_count_r14',
                                'all_ast_nodes_with_pos_r13', 'all_ast_nodes_with_pos_r14') if k in res}
summary['n_line_opcodes'] = len(res['line_opcodes']); summary['line_opcodes'] = res['line_opcodes']
summary['token_opcodes'] = res['token_opcodes']
summary['ast_changed_top_level_nodes'] = [{k: v for k, v in c.items()} for c in res['ast_changed_top_level_nodes']]
summary['ast_top_level_position_changes'] = res['ast_top_level_position_changes']
summary['all_node_position_diffs'] = res['all_node_position_diffs']
summary['refs'] = res['refs_GATE_RECORD_AFTER_SEAL_ALLOWED_r14']
summary['tuple_r13'] = res.get('GATE_RECORD_AFTER_SEAL_ALLOWED_r13'); summary['tuple_r14'] = res.get('GATE_RECORD_AFTER_SEAL_ALLOWED_r14')
summary['r13_I4_lines'] = res['r13_lines_with_I4_token']; summary['r14_I4_lines'] = res['r14_lines_with_I4_token']
print(json.dumps(summary, indent=1, default=str))
print('unified diff:\n' + res['unified_diff'])
