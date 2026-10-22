# Claude4 lens_diff: static scan (no execution) of r14's module-level statements that contain a call, to see what an import runs.
import ast, sys
from pathlib import Path
SRC = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r14/kmax_tail_compare_c2v007_r14_cx1v001.py')
A = ast.parse(SRC.read_bytes())
for n in A.body:
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        continue
    if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and ast.unparse(n.test).startswith('__name__'):
        print('L%d main-guard: %s' % (n.lineno, ast.unparse(n.test)))
        continue
    calls = [c for c in ast.walk(n) if isinstance(c, ast.Call)]
    if calls:
        names = sorted({ast.unparse(c.func) for c in calls})
        print('L%d %s calls=%s' % (n.lineno, type(n).__name__, names[:12]))
