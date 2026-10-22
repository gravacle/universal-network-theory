"""Claude4 lead static inspection for the 0439 weak Euler module (0440 review).

AST only: the target is parsed, never imported or executed.
Usage: python3 -I -B static_check_c4lead_v001.py TARGET.py [FUNC_NAME] > out.json
"""
import ast
import hashlib
import json
import sys

FORBIDDEN_ATTRS = {
    'inv', 'pinv', 'solve', 'lstsq', 'svd', 'eig', 'eigh', 'eigvals', 'eigvalsh',
    'cond', 'matrix_rank', 'qr', 'cholesky', 'tensorsolve', 'tensorinv',
    'clip', 'diag', 'diagflat', 'eye', 'identity', 'nan_to_num', 'real_if_close',
}
SIDE_EFFECT_NAMES = {'open', 'eval', 'exec', 'compile', '__import__', 'input', 'print', 'breakpoint'}
SIDE_EFFECT_MODULES = {'os', 'sys', 'subprocess', 'socket', 'urllib', 'http', 'pathlib', 'shutil',
                       'pickle', 'scipy', 'importlib', 'ctypes', 'multiprocessing', 'threading'}


def dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return '.'.join(reversed(parts))
    return None


def main(path, func_name='assemble_weak_euler'):
    src_bytes = open(path, 'rb').read()
    src = src_bytes.decode('utf-8')
    tree = ast.parse(src, filename=path)
    report = {'path': path, 'sha256': hashlib.sha256(src_bytes).hexdigest(),
              'lines': src.count('\n') + (0 if src.endswith('\n') else 1)}

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [{'line': node.lineno, 'module': a.name, 'as': a.asname} for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imports += [{'line': node.lineno, 'module': (node.module or '') + ':' + a.name, 'as': a.asname}
                        for a in node.names]
    report['imports'] = imports
    roots = {i['module'].split(':')[0].split('.')[0] for i in imports}
    report['non_numpy_imports'] = sorted(r for r in roots if r not in ('numpy', '__future__'))
    report['side_effect_module_imports'] = sorted(r for r in roots if r in SIDE_EFFECT_MODULES)

    forbidden, side_calls, conj_like, transposes = [], [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = dotted(node.func)
            if name:
                leaf = name.split('.')[-1]
                if leaf in FORBIDDEN_ATTRS:
                    forbidden.append({'line': node.lineno, 'call': name})
                if name in SIDE_EFFECT_NAMES:
                    side_calls.append({'line': node.lineno, 'call': name})
                if leaf in ('conj', 'conjugate', 'vdot'):
                    conj_like.append({'line': node.lineno, 'call': name})
        if isinstance(node, ast.Attribute) and node.attr in ('T', 'H', 'mT'):
            transposes.append({'line': node.lineno, 'expr': ast.get_source_segment(src, node)})
    report['forbidden_calls'] = forbidden
    report['side_effect_calls'] = side_calls
    report['conjugation_sites'] = conj_like
    report['transpose_sites'] = transposes

    # Module-level statements other than docstring/imports/defs/constant assignments.
    toplevel = []
    for i, node in enumerate(tree.body):
        if i == 0 and isinstance(node, ast.Expr) and isinstance(getattr(node, 'value', None), ast.Constant):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value
            calls = [n for n in ast.walk(value)] if value is not None else []
            if not any(isinstance(n, ast.Call) for n in calls):
                continue
        toplevel.append({'line': node.lineno, 'stmt': ast.get_source_segment(src, node)[:200]})
    report['module_level_executable_statements'] = toplevel

    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    report['functions'] = sorted(funcs)
    f = funcs.get(func_name)
    if f is None:
        report['target_function'] = None
    else:
        a = f.args
        kwonly = [k.arg for k in a.kwonlyargs]
        defaults = {k.arg: (ast.get_source_segment(src, d) if d is not None else None)
                    for k, d in zip(a.kwonlyargs, a.kw_defaults)}
        params = set(kwonly) | {x.arg for x in a.args} | {x.arg for x in a.posonlyargs}
        inplace = []
        for node in ast.walk(f):
            if isinstance(node, ast.AugAssign):
                tgt = node.target
                base = tgt
                while isinstance(base, (ast.Subscript, ast.Attribute)):
                    base = base.value
                inplace.append({'line': node.lineno, 'target': ast.get_source_segment(src, tgt),
                                'base_is_parameter': isinstance(base, ast.Name) and base.id in params})
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Subscript):
                        base = tgt
                        while isinstance(base, (ast.Subscript, ast.Attribute)):
                            base = base.value
                        if isinstance(base, ast.Name) and base.id in params:
                            inplace.append({'line': node.lineno, 'target': ast.get_source_segment(src, tgt),
                                            'base_is_parameter': True})
            if isinstance(node, ast.Call):
                for kw in node.keywords:
                    if kw.arg == 'out':
                        inplace.append({'line': node.lineno, 'target': 'out=' + ast.get_source_segment(src, kw.value),
                                        'base_is_parameter': None})
        report['target_function'] = {
            'name': func_name, 'line': f.lineno,
            'positional_params': [x.arg for x in a.posonlyargs] + [x.arg for x in a.args],
            'vararg': a.vararg.arg if a.vararg else None,
            'kwarg': a.kwarg.arg if a.kwarg else None,
            'keyword_only_params': kwonly,
            'keyword_only_defaults': {k: v for k, v in defaults.items() if v is not None},
            'all_keyword_only_required': (not a.args and not a.posonlyargs and a.vararg is None
                                          and a.kwarg is None and all(d is None for d in a.kw_defaults)),
            'inplace_writes': inplace,
        }
    return report


if __name__ == '__main__':
    target = sys.argv[1]
    fname = sys.argv[2] if len(sys.argv) > 2 else 'assemble_weak_euler'
    print(json.dumps(main(target, fname), indent=1))
