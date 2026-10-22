"""Claude3 independent N=1 identity check: fold pool=None into the parallel _solve and compare ASTs with the reviewed solve.
Also compares the worker column body (_run_column) with the serial loop body statements. Read-only."""
import ast, sys, json, copy, hashlib
BASE='base_copies/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_c2v001.py'
PAR='coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_c2v001.py'
b=ast.parse(open(BASE).read()); p=ast.parse(open(PAR).read())
def fn(tree,name): return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
class Fold(ast.NodeTransformer):
    def visit_If(self,node):
        self.generic_visit(node)
        t=node.test
        if isinstance(t,ast.Compare) and isinstance(t.left,ast.Name) and t.left.id=='pool' and len(t.ops)==1 and isinstance(t.ops[0],ast.IsNot) and isinstance(t.comparators[0],ast.Constant) and t.comparators[0].value is None:
            return node.orelse or None   # drop `if pool is not None:` block
        return node
    def visit_IfExp(self,node):
        self.generic_visit(node)
        t=node.test
        # `A if fresh and pool is None else (pool.take(i) if fresh else restored[i])` -> `A if fresh else restored[i]`
        if isinstance(t,ast.BoolOp) and isinstance(t.op,ast.And) and len(t.values)==2 and isinstance(t.values[1],ast.Compare) and isinstance(t.values[1].left,ast.Name) and t.values[1].left.id=='pool' and isinstance(t.values[1].ops[0],ast.Is):
            inner=node.orelse
            if isinstance(inner,ast.IfExp) and isinstance(inner.test,ast.Name) and inner.test.id=='fresh':
                return ast.IfExp(test=t.values[0],body=node.body,orelse=inner.orelse)
        # `A if pool is None or not pool.source_split else B` -> A
        if isinstance(t,ast.BoolOp) and isinstance(t.op,ast.Or) and isinstance(t.values[0],ast.Compare) and isinstance(t.values[0].left,ast.Name) and t.values[0].left.id=='pool' and isinstance(t.values[0].ops[0],ast.Is):
            return node.body
        return node
par_solve=copy.deepcopy(fn(p,'_solve')); par_solve=Fold().visit(par_solve); ast.fix_missing_locations(par_solve)
par_solve.args.kwonlyargs=[a for a in par_solve.args.kwonlyargs if a.arg!='pool']; par_solve.args.kw_defaults=par_solve.args.kw_defaults[:-1]
par_solve.name='solve'
base_solve=fn(b,'solve')
def dump(n): return ast.dump(n,include_attributes=False)
R={'solve_body_identical_after_fold': dump(par_solve)==dump(base_solve)}
if not R['solve_body_identical_after_fold']:
    import difflib
    R['first_differences']=[l for l in difflib.unified_diff(dump(base_solve).split('('),dump(par_solve).split('('),lineterm='',n=0)][:40]
for name in ('_finite','_supplied_fixed_source','cylindrical_metric_covector_to_registered'):
    R['identical_'+name]= dump(fn(b,name))==dump(fn(p,name))
# wrapper: solve passes every reviewed kwonly parameter by name with the same defaults
w=fn(p,'solve'); bs=base_solve
R['wrapper_kwonly_names_superset']= set(a.arg for a in bs.args.kwonlyargs) <= set(a.arg for a in w.args.kwonlyargs)
R['wrapper_defaults_match']= {a.arg:(ast.dump(d) if d else None) for a,d in zip(bs.args.kwonlyargs,bs.args.kw_defaults)} == {a.arg:(ast.dump(d) if d else None) for a,d in zip(w.args.kwonlyargs,w.args.kw_defaults) if a.arg!='column_workers'}
# worker column body vs serial loop statements: metric_point and at_z function defs and the HI call
def inner_defs(fnode):
    out={}
    for n in ast.walk(fnode):
        if isinstance(n,ast.FunctionDef) and n.name in ('metric_point','at_z'): out[n.name]=dump(n)
    return out
sd=inner_defs(base_solve); wd=inner_defs(fn(p,'_run_column'))
R['metric_point_identical_serial_vs_worker']= sd.get('metric_point')==wd.get('metric_point')
R['at_z_identical_serial_vs_worker']= sd.get('at_z')==wd.get('at_z')
def hi_call(fnode):
    for n in ast.walk(fnode):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='solve_hi_column': return dump(n)
R['hi_call_identical_serial_vs_worker']= hi_call(base_solve)==hi_call(fn(p,'_run_column'))
# checkpoint open_run call identical
def call_named(fnode,attr):
    for n in ast.walk(fnode):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr==attr: return dump(n)
for attr in ('open_run','begin_iteration','write_column','complete_iteration','finish'):
    R['checkpoint_call_identical_'+attr]= call_named(base_solve,attr)==call_named(fn(p,'_solve'),attr)
R['base_sha256']=hashlib.sha256(open(BASE,'rb').read()).hexdigest(); R['parallel_sha256']=hashlib.sha256(open(PAR,'rb').read()).hexdigest()
json.dump(R,open(sys.argv[1],'w'),indent=1); print(json.dumps(R,indent=1)[:2500])
