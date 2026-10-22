# Claude4 helper (dispatch 0650, A113 P6): read the r13 compare test suite as AST (never imported or run) and print, as JSON,
# (1) every check('<name>', ..., ids=(...)) call whose ids name one of the given NEW ids, and (2) for each IMPL-named test string
# given with --names, the suite test names it matches (exact, or as a prefix/pattern after the IMPL's own ellipsis or '*').
# Read-only; prints only. Run under tools/run_fenced_c4st2.py.
# usage: extract_suite_tags_c4v001.py SUITE.py SUITE_SHA256 --ids NEW-4 NEW-7 ... --names NAME1 NAME2 ...
import ast, hashlib, json, re, sys
from pathlib import Path

argv = sys.argv[1:]
suite, want_sha = argv[0], argv[1]
i_ids, i_names = argv.index('--ids'), argv.index('--names')
ids = argv[i_ids + 1:i_names]
names = argv[i_names + 1:]
raw = Path(suite).read_bytes()
got = hashlib.sha256(raw).hexdigest()
if got != want_sha:
    print(json.dumps({'refused': 'SUITE_SHA_MISMATCH', 'got': got, 'want': want_sha}))
    raise SystemExit(2)
tree = ast.parse(raw.decode('utf-8'))


def name_form(node):
    """('exact', s) for a constant name, ('pattern', prefix) for a %-format / f-string / concatenation, else None"""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return ('exact', node.value)
    if isinstance(node, ast.BinOp) and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
        return ('pattern', node.left.value.split('%')[0])
    if isinstance(node, ast.JoinedStr) and node.values and isinstance(node.values[0], ast.Constant):
        return ('pattern', node.values[0].value)
    return None


calls = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'check' and node.args:
        nf = name_form(node.args[0])
        if nf is None:
            continue
        tags = []
        for kw in node.keywords:
            if kw.arg == 'ids' and isinstance(kw.value, (ast.Tuple, ast.List)):
                tags = [e.value for e in kw.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        calls.append({'form': nf[0], 'name': nf[1], 'ids': tags, 'line': node.lineno})

by_id = {}
for x in ids:
    hit = [c for c in calls if x in c['ids']]
    by_id[x] = [{'name': c['name'], 'form': c['form'], 'line': c['line']} for c in hit]

all_names = [c['name'] for c in calls]


def segments(s):
    """the literal segments of an IMPL test name: split on the IMPL's own wildcards (the ellipsis and '*')"""
    return [p for p in re.split(r'[…*]', s.strip('`').strip()) if p]


def matches_name(n, a):
    segs = segments(n)
    if not segs:
        return False
    if not re.search(r'[…*]', n):
        return a == n
    pos = 0
    if not re.match(r'[…*]', n):                     # no leading wildcard: the first segment is a prefix
        if not a.startswith(segs[0]):
            return False
        pos, segs = len(segs[0]), segs[1:]
    for sg in segs:                                   # the remaining segments occur in order
        j = a.find(sg, pos)
        if j < 0:
            return False
        pos = j + len(sg)
    return True


matches = {}
for n in names:
    exact = n in all_names
    hit = sorted({a for a in all_names if matches_name(n, a)})
    pre = sorted({a for a in all_names if not re.search(r'[…*]', n) and a.startswith(n) and a != n})
    matches[n] = {'segments': segments(n), 'exact_in_suite': exact, 'suite_names_matched': hit[:12], 'n_matched': len(hit),
                  'longer_names_with_this_prefix': pre[:12], 'n_longer': len(pre)}

print(json.dumps({'suite': suite, 'sha256': got, 'n_check_calls': len(calls), 'by_id': by_id, 'impl_named': matches}, indent=1, sort_keys=True))
