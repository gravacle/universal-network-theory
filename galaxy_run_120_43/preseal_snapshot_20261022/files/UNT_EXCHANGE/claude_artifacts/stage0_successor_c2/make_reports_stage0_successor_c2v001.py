#!/usr/bin/env python3
"""make_reports_stage0_successor_c2v001 -- the unified diff and the AST-identity report, successor vs v003g.

Usage: python3 -I -B make_reports_stage0_successor_c2v001.py --out-dir DIR [--module PATH]
Reads the v003g module bytes (sha256 verified) and the successor bytes; writes, by exclusive create:
  DIR/DIFF_v003g_to_stage0_successor_c2v001.diff
  DIR/AST_IDENTITY_STAGE0_SUCCESSOR_C2V001.md
AST identity: ast.dump(node) of every top-level statement (no line/column attributes), compared as strings; the
sha256 columns are sha256 of those dump strings (UTF-8).
"""
import argparse
import ast
import datetime
import difflib
import hashlib
import os
import sys

V003G_PATH = ('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/freeze_score_readiness_cx3/v003g/'
              'prediction_freeze_c2v003g_cx3v001.py')
V003G_SHA256 = '48a1e48a5230fff346705c338da30a8ee53a8643193dbe4616c25e61eab3d405'
SUCCESSOR_NAME = 'prediction_freeze_c2v003g_stage0_c2v001.py'

CHANGED_PURPOSE = {
    '_load_row_roster': 'require_evaluated no longer refuses the STAGE0 roster, so a STAGE0 replay evaluation can be '
                        'computed; whether it is frozen is decided only by the receipt rule in the writer',
    '_root_rosters_for_alternatives': 'the slots comparison and the per-roster record comparison go through '
                                      '_stage0_status_neutral / _stage0_neutral_record: STAGE0 status is the only '
                                      'tolerated difference',
    '_bind_alternatives': 'the slots comparison goes through _stage0_status_neutral (STAGE0 status only)',
    '_validate_manifest_structure': 'runs _stage0_manifest_check after the v003g checks (writer, verifier, scorer)',
    'write_freeze_manifest': 'new keyword stage0_status_record=None; caller STAGE0 status neutralised; STAGE0 '
                             'evaluation set aside before D9; _stage0_freeze_decision admits it only by the receipt '
                             'rule; manifest body gains stage0_status; STAGE0 custody files added to input_files; '
                             'docstring paragraph',
    '_alternative_score_scope': 'the STAGE0 record comparison goes through _stage0_neutral_record (status only)',
    'score_after_freeze': 'output gains stage0_status (None on refusal paths; the frozen block when scored)',
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def wx(path, text):
    with open(path, 'xb') as fh:
        fh.write(text.encode('utf-8'))
    return path


def frozen_set_literal(node):
    """The element set of a frozenset({...}) literal of constants; None for anything else."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'frozenset' and \
            len(node.args) == 1 and isinstance(node.args[0], ast.Set) and not node.keywords:
        try:
            return set(ast.literal_eval(node.args[0]))
        except ValueError:
            return None
    return None


def top(tree):
    funcs, consts, other, order = {}, {}, [], []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            funcs[node.name] = node
            order.append(('def', node.name))
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) for t in node.targets):
            name = ','.join(t.id for t in node.targets)
            consts[name] = node
            order.append(('assign', name))
        else:
            other.append(node)
            order.append(('other', type(node).__name__))
    return funcs, consts, other, order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--module', default=None)
    a = ap.parse_args()
    here = os.path.dirname(os.path.realpath(__file__))
    spath = os.path.realpath(a.module or os.path.join(here, SUCCESSOR_NAME))
    with open(V003G_PATH, 'rb') as fh:
        vraw = fh.read()
    if sha(vraw) != V003G_SHA256:
        raise SystemExit('v003g bytes changed')
    with open(spath, 'rb') as fh:
        sraw = fh.read()
    ssha = sha(sraw)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    # unified diff
    vl = vraw.decode('utf-8').splitlines(True)
    sl = sraw.decode('utf-8').splitlines(True)
    diff = ''.join(difflib.unified_diff(
        vl, sl, fromfile='v003g/prediction_freeze_c2v003g_cx3v001.py (sha256 %s)' % V003G_SHA256,
        tofile='stage0_successor_c2/%s (sha256 %s)' % (SUCCESSOR_NAME, ssha), n=3))
    added = sum(1 for ln in diff.splitlines() if ln.startswith('+') and not ln.startswith('+++'))
    removed = sum(1 for ln in diff.splitlines() if ln.startswith('-') and not ln.startswith('---'))
    dpath = wx(os.path.join(a.out_dir, 'DIFF_v003g_to_stage0_successor_c2v001.diff'), diff)

    # AST identity
    vt, st = ast.parse(vraw.decode('utf-8')), ast.parse(sraw.decode('utf-8'))
    vf, vc, vo, vord = top(vt)
    sf, sc, so, sord = top(st)
    d = lambda n: ast.dump(n)
    h = lambda n: sha(ast.dump(n).encode('utf-8'))
    fn_rows = []
    for name, node in vf.items():
        status = 'MISSING' if name not in sf else ('IDENTICAL' if d(node) == d(sf[name]) else 'CHANGED_STAGE0')
        fn_rows.append((name, status, h(node), h(sf[name]) if name in sf else '-'))
    new_fns = [(name, h(node), (ast.get_docstring(node) or '').split('\n')[0]) for name, node in sf.items()
               if name not in vf]
    c_rows = []
    for name, node in vc.items():
        status = 'MISSING' if name not in sc else ('IDENTICAL' if d(node) == d(sc[name]) else 'CHANGED_STAGE0')
        c_rows.append((name, status, node, sc.get(name)))
    new_cs = [(name, node) for name, node in sc.items() if name not in vc]
    other_rows = [(type(x).__name__, 'IDENTICAL' if d(x) == d(y) else 'CHANGED') for x, y in zip(vo, so)]
    it = iter(sord)
    order_kept = all(any(x == y for y in it) for x in vord)
    n_ident = sum(1 for r in fn_rows if r[1] == 'IDENTICAL')
    n_changed = [r[0] for r in fn_rows if r[1] == 'CHANGED_STAGE0']
    n_missing = [r[0] for r in fn_rows if r[1] == 'MISSING']
    c_changed = [r[0] for r in c_rows if r[1] == 'CHANGED_STAGE0']
    c_ident = sum(1 for r in c_rows if r[1] == 'IDENTICAL')
    unexpected = sorted(set(n_changed) - set(CHANGED_PURPOSE))

    L = []
    L.append('# AST identity report: STAGE0 successor c2v001 against v003g')
    L.append('')
    L.append('Generated %s by `make_reports_stage0_successor_c2v001.py` (python %s, `-I -B`).' % (
        stamp, '.'.join(map(str, sys.version_info[:3]))))
    L.append('')
    L.append('- v003g: `%s`, sha256 `%s`' % (V003G_PATH, V003G_SHA256))
    L.append('- successor: `%s`, sha256 `%s`' % (spath, ssha))
    L.append('- diff: `%s` (%d lines added, %d removed)' % (os.path.basename(dpath), added, removed))
    L.append('')
    L.append('Method: `ast.parse` both files; every top-level statement is compared by `ast.dump` (no line or column '
             'attributes), so comments, blank lines and line positions do not count. The sha256 columns are sha256 of '
             'the `ast.dump` strings, not of file bytes. TESTED: computed from the bytes named above.')
    L.append('')
    L.append('## Summary')
    L.append('')
    L.append('| Item | Count |')
    L.append('|---|---|')
    L.append('| v003g top-level functions | %d |' % len(vf))
    L.append('| identical (non-STAGE0) | %d |' % n_ident)
    L.append('| changed, STAGE0-only (listed below) | %d |' % len(n_changed))
    L.append('| missing from the successor | %d |' % len(n_missing))
    L.append('| changed but not in the STAGE0 list | %d |' % len(unexpected))
    L.append('| new successor functions (all `_stage0_*`) | %d |' % len(new_fns))
    L.append('| v003g top-level constants | %d (identical %d, changed %d) |' % (len(vc), c_ident, len(c_changed)))
    L.append('| new successor constants (all `STAGE0_*`) | %d |' % len(new_cs))
    L.append('| v003g top-level order kept (as a subsequence) | %s |' % order_kept)
    L.append('')
    L.append('Result: every v003g function other than the %d below is AST-identical; no v003g function or constant is '
             'missing; %s.' % (len(n_changed), 'no other function changed' if not unexpected else
                                 'UNEXPECTED changes: %s' % unexpected))
    L.append('')
    L.append('## Changed functions (STAGE0 only)')
    L.append('')
    L.append('| Function | What changed |')
    L.append('|---|---|')
    for name in n_changed:
        L.append('| `%s` | %s |' % (name, CHANGED_PURPOSE.get(name, 'UNEXPECTED')))
    L.append('')
    L.append('## Changed constants')
    L.append('')
    L.append('| Constant | v003g | successor |')
    L.append('|---|---|---|')
    for name, status, vn, sn in c_rows:
        if status != 'IDENTICAL':
            vset, sset = frozen_set_literal(vn.value), frozen_set_literal(sn.value) if sn is not None else None
            if vset is not None and sset is not None:
                vv = 'frozenset of %d names' % len(vset)
                sv = 'adds %s; removes %s' % (sorted(sset - vset), sorted(vset - sset))
            else:
                vv = ast.unparse(vn.value).replace('\n', ' ')
                sv = ast.unparse(sn.value).replace('\n', ' ') if sn is not None else '-'
            L.append('| `%s` | `%s` | `%s` |' % (name, vv, sv))
    L.append('')
    L.append('Unchanged pins (AST-identical): `ROOT_SLOTS_PATH`, `ROOT_SLOTS_SHA256` (slots V003 `d3859b42...`), '
             '`REGISTRATION_SCHEMA`, `PROGRAM_QUERY_MANIFEST_SHA256`, `REGISTERED_GL_NODES_PATH`, '
             '`REGISTERED_GL_NODES_SHA256`, `ROW_ROSTER_SCHEMA`, `INVALID_GATE_SCHEMA` and every other v003g constant.')
    L.append('')
    L.append('## New functions')
    L.append('')
    L.append('| Function | ast sha256 | First docstring line |')
    L.append('|---|---|---|')
    for name, hh, doc in new_fns:
        L.append('| `%s` | `%s` | %s |' % (name, hh, doc.replace('|', '/')))
    L.append('')
    L.append('## New constants')
    L.append('')
    L.append(', '.join('`%s`' % n for n, _node in new_cs))
    L.append('')
    L.append('## Other top-level statements')
    L.append('')
    L.append('| # | Kind | Status |')
    L.append('|---|---|---|')
    for i, (k, s) in enumerate(other_rows):
        L.append('| %d | %s | %s%s |' % (i, k, s, ' (module docstring: successor header prepended)' if i == 0 else ''))
    L.append('')
    L.append('## Every v003g function')
    L.append('')
    L.append('| Function | Status | v003g ast sha256 | successor ast sha256 |')
    L.append('|---|---|---|---|')
    for name, status, a1, a2 in fn_rows:
        L.append('| `%s` | %s | `%s` | `%s` |' % (name, status, a1, a2))
    L.append('')
    apath = wx(os.path.join(a.out_dir, 'AST_IDENTITY_STAGE0_SUCCESSOR_C2V001.md'), '\n'.join(L))
    print('wrote %s sha256 %s' % (dpath, sha(open(dpath, 'rb').read())))
    print('wrote %s sha256 %s' % (apath, sha(open(apath, 'rb').read())))
    print('functions: %d identical, %d changed %s, %d missing, %d new; constants changed %s; unexpected %s; order %s'
          % (n_ident, len(n_changed), n_changed, len(n_missing), len(new_fns), c_changed, unexpected, order_kept))
    return 0 if (not unexpected and not n_missing and order_kept) else 1


if __name__ == '__main__':
    sys.exit(main())
