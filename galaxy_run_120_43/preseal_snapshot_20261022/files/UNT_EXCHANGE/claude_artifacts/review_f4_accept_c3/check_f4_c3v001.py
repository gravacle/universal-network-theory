"""Claude3 delta check of Codex2's D017/F4 successor h3_accept_call_a296_cx2v001.py (edcd3ffa) vs h3_accept_call_c2v004
(eb895263). (1) text and AST delta scope; (2) load_module/load_chain/Refused/ENTRY_LINE extracted by AST from the
successor's pinned bytes, run on synthetic entry modules written to a NEW scratch dir (ENTRY_NAME values read from the
pinned A296 entry, the r12 placeholder entry and the old c2v004 entry; stub load_wrapper/check_patch); (3) mutant: the
successor with the old ENTRY_LINE must refuse the A296 entry. Read-only on all pinned files.
usage: python3 -I -B check_f4_c3v001.py SCRATCH_NEW_DIR OUT_JSON"""
import ast, difflib, hashlib, json, os, re, sys
from pathlib import Path
A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
NEW = {'path': str(A/'eps_rule_successor_cx2/integration/campaign/h3_accept_call_a296_cx2v001.py'), 'sha256': 'edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007'}
OLD = {'path': str(A/'h3_campaign_path_c2/h3_accept_call_c2v004.py'), 'sha256': 'eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19'}
ENTRIES = {'a296_entry': (str(A/'eps_rule_successor_cx2/integration/campaign/h3_campaign_entry_a296_cx2v001.py'), '05738509efb85f1a64d0031bf0e1c6b0d96f3427ab1a5670704affcd47f4ff28'),
           'r12_placeholder_entry': (str(A/'eps_rule_successor_cx2/integration/campaign/placeholder_chain_a296_cx2v001/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py'), 'af4e4f36ab74c8be01d3384bcaf83bdfdc3d867207b41bad447087eea4e21743'),
           'old_c2v004_entry': (str(A/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py'), None)}
scratch, outp = Path(sys.argv[1]), Path(sys.argv[2]); os.mkdir(scratch)
def sha(b): return hashlib.sha256(b).hexdigest()
def pinned(ref):
    raw = Path(ref['path']).read_bytes(); assert sha(raw) == ref['sha256'], ref['path']; return raw
nraw, oraw = pinned(NEW), pinned(OLD)
res = {'schema': 'F4_DELTA_CHECK_C3V001', 'new': NEW, 'old': OLD, 'checks': {}}
C = res['checks']
# 1. text delta: changed lines only at the docstring, ENTRY_LINE and the refusal prefix
nl, ol = nraw.decode().splitlines(), oraw.decode().splitlines()
sm = difflib.SequenceMatcher(a=ol, b=nl, autojunk=False)
hunks = [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
changed_new = [nl[j] for t, i1, i2, j1, j2 in hunks for j in range(j1, j2)]
C['text_hunks'] = len(hunks); C['line_count_equal'] = len(nl) == len(ol)
def allowed(line):
    return (line.startswith('"""Per-call acceptance step') or 'A296-line entry' in line or 'ENTRY_NOT_A296_LINE' in line
            or line.startswith('usage: python3 -I -B h3_accept_call_a296_cx2v001.py') or line.startswith("ENTRY_LINE = 'h3_campaign_entry_a296_cx2v001'"))
C['all_changed_lines_allowed'] = all(allowed(l) for l in changed_new)
# 2. AST delta
def items(t):
    out = {}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): out['def ' + n.name] = ast.dump(n)
        elif isinstance(n, ast.Assign): out['assign ' + ','.join(ast.unparse(x) for x in n.targets)] = ast.dump(n.value)
        elif isinstance(n, ast.Expr) and isinstance(getattr(n, 'value', None), ast.Constant) and isinstance(n.value.value, str): out['docstring'] = 'doc'
        else: out.setdefault('other', []).append(ast.dump(n))
    return out
ta, tb = ast.parse(oraw), ast.parse(nraw)
ia, ib = items(ta), items(tb)
C['ast_differing'] = sorted(k for k in set(ia) | set(ib) if ia.get(k) != ib.get(k))
# load_chain must differ only in one string constant
def strip_strings(fn):
    class T(ast.NodeTransformer):
        def visit_Constant(self, node):
            return ast.Constant('S') if isinstance(node.value, str) else node
    return ast.dump(T().visit(ast.parse(ast.unparse(fn))))
fa = [n for n in ta.body if isinstance(n, ast.FunctionDef) and n.name == 'load_chain'][0]
fb = [n for n in tb.body if isinstance(n, ast.FunctionDef) and n.name == 'load_chain'][0]
C['load_chain_equal_modulo_strings'] = strip_strings(fa) == strip_strings(fb)
C['ast_delta_ok'] = set(C['ast_differing']) <= {"assign ENTRY_LINE", 'def load_chain'} and C['load_chain_equal_modulo_strings']
# 3. functional: extract and run load_module/load_chain on synthetic entries
def extract(tree, entry_line):
    keep = [n for n in tree.body if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in ('load_module', 'load_chain', 'Refused'))]
    ns = {'__name__': 'f4check', 'hashlib': hashlib, 'importlib': __import__('importlib.util').util and __import__('importlib'), 'sys': sys, 'Path': Path,
          'ENTRY_LINE': entry_line}
    import importlib.util as ilu; ns['importlib'] = __import__('importlib'); ns['importlib'].util = ilu
    exec(compile(ast.Module(body=keep, type_ignores=[]), NEW['path'] + ':extract', 'exec'), ns)
    return ns
line_new = ast.literal_eval([n for n in tb.body if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == 'ENTRY_LINE'][0].value)
def entry_name_of(path, want_sha):
    raw = Path(path).read_bytes()
    if want_sha: assert sha(raw) == want_sha, path
    m = re.search(r"^ENTRY_NAME = '([^']+)'$", raw.decode(), re.M); return m.group(1) if m else None
names = {k: entry_name_of(p, s) for k, (p, s) in ENTRIES.items()}
names['unnamed'] = None
res['entry_names_from_bytes'] = names
def synth(label, name):
    body = ('ENTRY_NAME = %r\n' % name if name is not None else '') + 'class _M: G = None\ndef load_wrapper():\n    return _M()\ndef check_patch(M):\n    return None\n'
    p = scratch/('entry_%s.py' % label); p.write_text(body); return str(p), sha(p.read_bytes())
def run(ns, label, name):
    p, h = synth(label, name)
    try: ns['load_chain'](p, h); return 'LOADED'
    except ns['Refused'] as e: return 'REFUSED:' + str(e).split(':')[0]
nsn = extract(tb, line_new)
fun = {k: run(nsn, k, v) for k, v in names.items()}
p, h = synth('pin_mismatch', names['a296_entry'])
try: nsn['load_chain'](p, '0' * 64); fun['wrong_entry_pin'] = 'LOADED'
except nsn['Refused'] as e: fun['wrong_entry_pin'] = 'REFUSED:' + str(e).split(':')[0]
res['functional'] = fun
C['functional_ok'] = (fun['a296_entry'] == 'LOADED' and fun['r12_placeholder_entry'] == 'LOADED' and fun['old_c2v004_entry'] == 'REFUSED:ENTRY_NOT_A296_LINE'
                      and fun['unnamed'] == 'REFUSED:ENTRY_NOT_A296_LINE' and fun['wrong_entry_pin'] == 'REFUSED:PIN_MISMATCH')
# 4. mutant: the old line restored refuses the A296 entry (and the original c2v004 behaves the same)
nso = extract(tb, 'h3_campaign_entry_c2v004')
res['mutant_old_line_on_a296_entry'] = run(nso, 'mutant_a296', names['a296_entry'])
C['mutant_killed'] = res['mutant_old_line_on_a296_entry'].startswith('REFUSED')
res['ok'] = all(v is True for k, v in C.items() if isinstance(v, bool)) and C['all_changed_lines_allowed']
res['self_sha256'] = sha(Path(__file__).read_bytes())
with open(outp, 'x') as f: f.write(json.dumps(res, indent=1, sort_keys=True) + '\n')
print(json.dumps({'ok': res['ok'], 'checks': C, 'functional': fun, 'mutant': res['mutant_old_line_on_a296_entry'], 'names': names}))
