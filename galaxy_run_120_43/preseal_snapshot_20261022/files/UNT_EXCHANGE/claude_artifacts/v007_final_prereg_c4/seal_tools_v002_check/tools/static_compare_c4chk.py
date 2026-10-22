# Claude4 helper (seal tools v002 check): FORMAL static checks of a compare source, by AST only (nothing imported or executed).
# (1) module-level statements: every statement kind, and every module-level expression that CALLS something at import time;
# (2) call graph from the functions the seal tools call in-process (validate_case_block, activate_driver_build,
#     load_driver_build_record, load_strict_file, registered_gas_M_s, builtin_r5_build, load_producer_registry, blinded_gate,
#     blinded_case, blind_strings, assert_no_numbers) to the C5H-run stat / interlock helpers; prints any path found.
import ast, hashlib, json, sys
from pathlib import Path
ENTRY = ('validate_case_block', 'activate_driver_build', 'load_driver_build_record', 'load_strict_file', 'registered_gas_M_s', 'builtin_r5_build',
         'load_producer_registry', 'blinded_gate', 'blinded_case', 'blind_strings', 'assert_no_numbers', 'check_record_codes', 'driver_build_codes')
FORBIDDEN = ('_registered_run_identities', 'registered_identity_code', 'c5h_path_hit', 'c5h_interlock', '_resolved_walk_hit', 'interlock_guard',
             'read_run', 'read_all', 'read_gates', 'run_file_paths', 'manifest_run_paths', 'main', '_main')
out = {}
for path in sys.argv[1:]:
    raw = Path(path).read_bytes()
    tree = ast.parse(raw.decode('utf-8'))
    kinds, calls_at_import = {}, []
    for node in tree.body:
        kinds[type(node).__name__] = kinds.get(type(node).__name__, 0) + 1
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for d in node.decorator_list:
                for sub in ast.walk(d):
                    if isinstance(sub, ast.Call):
                        calls_at_import.append('decorator L%d' % node.lineno)
            continue
        if isinstance(node, ast.If):
            t = node.test
            if isinstance(t, ast.Compare) and isinstance(t.left, ast.Name) and t.left.id == '__name__':
                continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                f = sub.func
                nm = f.id if isinstance(f, ast.Name) else (ast.unparse(f) if hasattr(ast, 'unparse') else type(f).__name__)
                calls_at_import.append('L%d %s' % (node.lineno, nm))
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            called = set()
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    f = sub.func
                    if isinstance(f, ast.Name):
                        called.add(f.id)
                    elif isinstance(f, ast.Attribute):
                        called.add(f.attr)
                elif isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                    called.add(sub.id)             # a function passed as a value (callbacks) counts too
            funcs.setdefault(node.name, set()).update(called)
    reach = {}
    for e in ENTRY:
        seen, stack, parent = {e}, [e], {e: None}
        while stack:
            f = stack.pop()
            for g in funcs.get(f, ()):
                if g in funcs and g not in seen:
                    seen.add(g)
                    parent[g] = f
                    stack.append(g)
        hits = []
        for bad in FORBIDDEN:
            if bad in seen:
                chain, x = [], bad
                while x is not None:
                    chain.append(x)
                    x = parent[x]
                hits.append(' <- '.join(chain))
        reach[e] = {'reachable_functions': len(seen), 'forbidden_reached': hits}
    out[path] = {'sha256': hashlib.sha256(raw).hexdigest(), 'module_statement_kinds': kinds, 'calls_evaluated_at_import': calls_at_import, 'reach': reach}
print(json.dumps(out, indent=1))
