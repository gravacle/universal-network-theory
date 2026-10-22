"""Claude2-review static tail-site census (no execution of any stage).
For every NGC route-B successor and its reviewed DDO base, and for the route-B binding and its base, count every AST call
that applies or builds the UV tail (calls on the stage's `uvt` binding object; TailBoundary/build/kept-region/jet/lapse calls
in the binding), and every use of the tail argv in the driver chain (v010 r4 execute_chain vs v011 _execute_ngc_v011_chain).
A tail application site added, removed or duplicated by v011 shows up as a count difference.
usage: tail_sites_c2r.py OUT_JSON
"""
import ast
import collections
import hashlib
import json
import sys
from pathlib import Path

A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
BUILD = A / 'ngc_route_tail_readiness_cx3/v011/route_b/BUILD_ROUTE_B_CX3V006.json'
DRV_OLD = A / 'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
DRV_NEW = A / 'ngc_route_tail_readiness_cx3/v011/galaxy_m0_forward_c2v011_cx3v003.py'
TAILWORDS = ('tail', 'jet', 'lapse', 'TailBoundary', 'build', 'kept', 'offset_fields', 'record', 'bind')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def calls(tree, pred):
    c = collections.Counter()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            name = ast.unparse(f)
            if pred(f, name):
                c[name] += 1
    return c


def stage_pred(f, name):
    return isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == 'uvt'


def binding_pred(f, name):
    leaf = name.split('.')[-1]
    return any(w.lower() in leaf.lower() for w in TAILWORDS) and not leaf.startswith('ngc_')


def fn(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)


def main():
    out = Path(sys.argv[1]); assert not out.exists()
    b = json.loads(BUILD.read_text()); res = {'stages': {}, 'binding': None, 'driver_chain': None}
    for k, v in b['stages'].items():
        t0 = ast.parse(Path(v['base']['path']).read_text()); t1 = ast.parse(Path(v['successor']['path']).read_text())
        c0, c1 = calls(t0, stage_pred), calls(t1, stage_pred)
        assert sha(v['successor']['path']) == v['successor']['sha256'] and sha(v['base']['path']) == v['base']['sha256']
        res['stages'][k] = {'base': dict(c0), 'successor': dict(c1), 'equal': c0 == c1}
    t0 = ast.parse(Path(b['base_binding']['path']).read_text()); t1 = ast.parse(Path(b['binding']['path']).read_text())
    c0, c1 = calls(t0, binding_pred), calls(t1, binding_pred)
    res['binding'] = {'base': dict(c0), 'successor': dict(c1), 'only_in_successor': dict(c1 - c0), 'only_in_base': dict(c0 - c1)}
    o = fn(ast.parse(DRV_OLD.read_text()), 'execute_chain'); n = fn(ast.parse(DRV_NEW.read_text()), '_execute_ngc_v011_chain')
    u0 = calls(o, lambda f, nm: nm in ('uvt_argv', 'uvt_plan', '_uvt_ngc_v011_plan', 'uvt_admitted_record_check', 'uvt_route_a_identity_check'))
    u1 = calls(n, lambda f, nm: nm in ('uvt_argv', 'uvt_plan', '_uvt_ngc_v011_plan', 'uvt_admitted_record_check', 'uvt_route_a_identity_check'))
    a0 = [ast.unparse(x) for x in ast.walk(o) if isinstance(x, ast.Call) and ast.unparse(x.func) == 'uvt_argv']
    a1 = [ast.unparse(x) for x in ast.walk(n) if isinstance(x, ast.Call) and ast.unparse(x.func) == 'uvt_argv']
    res['driver_chain'] = {'v010r4': dict(u0), 'v011': dict(u1), 'uvt_argv_call_list_equal': sorted(a0) == sorted(a1), 'uvt_argv_calls': sorted(a1)}
    res['verdict'] = ('NO_TAIL_SITE_ADDED_REMOVED_OR_DUPLICATED' if all(s['equal'] for s in res['stages'].values())
                      and res['driver_chain']['uvt_argv_call_list_equal'] else 'TAIL_SITE_CENSUS_DIFFERS')
    res['tool'] = {'path': str(Path(__file__).resolve()), 'sha256': sha(__file__)}
    with out.open('x') as f:
        json.dump(res, f, indent=1)
    for k, s in res['stages'].items():
        print('%-18s equal=%s %s' % (k, s['equal'], s['successor']))
    print('binding only_in_successor', res['binding']['only_in_successor'], 'only_in_base', res['binding']['only_in_base'])
    print('driver', res['driver_chain']['v010r4'], res['driver_chain']['v011'], res['driver_chain']['uvt_argv_call_list_equal'])
    print(res['verdict'])


if __name__ == '__main__':
    main()
