"""Independent 0808 source census and inert metadata checks; no science imports."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

D = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/cause_record_cx1/cxv002')
O = Path(__file__).parent
pins = {
    'cause_record_cxv002.py': '4271da4422c40faf1afbd115af836091e765f64e902809432b55af69036606f3',
    'metadata_selector_cx1v002.py': '86a71335a13457ce92c1bb0caa6632d17c5a8c5c27252f08777dabe9a975d90f',
    'CAUSE_VOCABULARY_CXV002.json': '839c75774c28c6c8213180df7e204ba5b9d0fbc63531591d22d9912149f8df37',
}
inputs = []
buffers = {}
for name, want in pins.items():
    p = D / name
    b = p.read_bytes()
    got = hashlib.sha256(b).hexdigest()
    assert got == want
    inputs.append({'path': str(p), 'sha256': got})
    buffers[name] = b
v = json.loads(buffers['CAUSE_VOCABULARY_CXV002.json'])
tokens = {'ROUTE_A_NO_FIXED_POINT', 'ITERATION_BUDGET_EXHAUSTED'}
modules = {}
roots = {}
for driver, reg in v.items():
    paths = {m['path'] for m in reg['modules']}
    assert reg['complete'] is True and reg['root'] in paths
    root_counts = {}
    for item in reg['modules']:
        p = Path(item['path'])
        assert p.is_absolute() and p.suffix == '.py'
        assert not any(s in str(p) for s in ['/runs_ext/', '/.codex/', 'KMAX_A2F10_C5H_RUN_V001'])
        if str(p) not in modules:
            b = p.read_bytes()
            h = hashlib.sha256(b).hexdigest()
            assert h == item['sha256']
            tree = ast.parse(b, filename=str(p))
            parent = {id(c): n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
            emissions = []
            uses = []
            for node in ast.walk(tree):
                if not isinstance(node, ast.Constant) or node.value not in tokens:
                    continue
                par = parent[id(node)]
                row = {'token': node.value, 'line': node.lineno, 'parent_ast': type(par).__name__}
                if isinstance(par, ast.Compare):
                    uses.append(row)
                    continue
                # Independent census includes every other exact token literal.
                # Unexpected syntax is reported, not silently omitted.
                ancestors = []
                q = node
                while id(q) in parent:
                    q = parent[id(q)]
                    ancestors.append(q)
                catches = [ast.unparse(a.type) if a.type else 'BARE'
                           for a in ancestors if isinstance(a, ast.ExceptHandler)]
                row['exception_context'] = catches[0] if catches else None
                row['expression'] = ast.unparse(par)
                if node.value == 'ITERATION_BUDGET_EXHAUSTED':
                    assert isinstance(par, ast.Call)
                    assert isinstance(par.func, ast.Name) and par.func.id == '_finish'
                    assert any(isinstance(a, ast.Return) for a in ancestors)
                    # Exhaustion is a return after the top-level bounded source loop,
                    # not an exception handler or a branch inside that loop.
                    assert not any(isinstance(a, (ast.For, ast.While, ast.ExceptHandler)) for a in ancestors)
                    assert par.args and isinstance(par.args[0], ast.Dict)
                    fields = {k.value: val for k, val in zip(par.args[0].keys, par.args[0].values)
                              if isinstance(k, ast.Constant)}
                    assert isinstance(fields.get('converged_finite_fixed_point'), ast.Constant)
                    assert fields['converged_finite_fixed_point'].value is False
                else:
                    assert isinstance(par, ast.Assign)
                    assert row['exception_context'] in (None, 'RouteANoFixedPoint')
                    row['classification_site_guarded_by_source_preparation_exclusion'] = not catches
                emissions.append(row)
            modules[str(p)] = {'sha256': h, 'bytes': len(b), 'emissions': emissions, 'comparisons': uses}
        assert modules[str(p)]['sha256'] == item['sha256']
        found = {(s['token'], s['line']) for s in modules[str(p)]['emissions']}
        claimed = {(s['token'], s['line']) for s in item['sites']}
        assert found == claimed, (str(p), found, claimed)
        assert not item.get('unresolved')
        for edge in item['refs']:
            assert edge['path'] in paths
            target = next(m for m in reg['modules'] if m['path'] == edge['path'])
            assert target['sha256'] == edge['sha256']
        for site in item['sites']:
            root_counts[site['token']] = root_counts.get(site['token'], 0) + 1
    roots[driver] = {'modules': len(paths), 'emission_counts': root_counts}

# Only the reviewed metadata producer/selector is executed, never a science source.
ns = {'__name__': 'independent_cause_review', '__file__': str(D/'cause_record_cxv002.py')}
exec(compile(buffers['cause_record_cxv002.py'], str(D/'cause_record_cxv002.py'), 'exec'), ns)
fixture = O/'inert_independent_cx3v001'
fixture.mkdir(exist_ok=False)
serial = 0
reads = []
def audit(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes)):
        path = os.fsdecode(args[0])
        if path.startswith(str(fixture)):
            reads.append(path)
sys.addaudithook(audit)
def put(obj):
    global serial
    serial += 1
    p = fixture / ('%03d.json' % serial)
    raw = obj if isinstance(obj, bytes) else json.dumps(obj, separators=(',', ':')).encode()
    with p.open('xb') as f:
        f.write(raw)
    return str(p), hashlib.sha256(raw).hexdigest()
checks = []
def check(name, condition, evidence=None):
    checks.append({'name': name, 'pass': bool(condition), 'evidence': evidence})
    assert condition, name
ddo = next(h for h in v if ns['DRIVERS'][h] == 'DDO')
ngc = next(h for h in v if ns['DRIVERS'][h] == 'NGC')
def case(driver=ddo, outcome='ITERATION_BUDGET_EXHAUSTED', result_change=None, finish_change=None):
    result = {'status':'ROUTE_A_NO_FIXED_POINT', 'route_a_outcome': {'outcome':outcome},
              'stage_records':[{'name':'route_a','exit_code':0}],
              'rows':[{'v':123.456, 'marker':'DO_NOT_MATERIALIZE'}],
              'reasons':['DO_NOT_MATERIALIZE']}
    if result_change:
        result_change(result)
    rp = put(result)
    mon = {'status':'CHILD_FAILED','driver_status':result['status'],'exit_code':3,'stop_reason':None,
           'result':{'path':rp[0],'sha256':rp[1]},
           'pins':{'spec':{'sha256':'a'*64},'driver':{'path':v[driver]['root'],'sha256':driver}}}
    receipt = put(mon)
    fin = {'status':mon['driver_status'],'result_path':rp[0],'result_sha256':rp[1]}
    if finish_change:
        finish_change(fin)
    fp = put(fin)
    return receipt, fp[0], rp
for h in (ddo, ngc):
    c = case(driver=h)
    att = put({'status':'POST_SEAL_ATTESTED','authority':'Claude2',
               'receipt_sha256':c[0][1],'spec_sha256':'a'*64,'driver_sha256':h})
    reads.clear()
    got = ns['classify'](c[0], c[1], post_seal=att if h==ngc else None)
    check('independent_real_pin_positive_'+ns['DRIVERS'][h], got['model_outcome'])
    check('fixture_inputs_single_read_'+ns['DRIVERS'][h], all(reads.count(p)==1 for p in reads),
          {'read_count':len(reads)})
c = case(driver=ngc)
reads.clear()
got = ns['classify'](c[0], c[1])
check('ngc_without_attestation_refuses', not got['model_outcome'])
check('ngc_without_attestation_no_result_or_finish', c[1] not in reads and c[2][0] not in reads)
check('ngc_before_attestation_receipt_is_read', reads==[c[0][0]],
      {'opened':list(reads),'reason':got['model_outcome_reason'],
       'scope':'This demonstrates the exception question; it is not a scientific-output read.'})
for key,value in [('status','FAILED'),('result_path','/synthetic/wrong'),('result_sha256','0'*64)]:
    c=case(finish_change=lambda f,k=key,val=value:f.update({k:val}))
    reads.clear()
    got=ns['classify'](c[0],c[1])
    check('finish_binding_'+key, not got['model_outcome'] and c[2][0] not in reads)
for outcome in ['FAILED_SOURCE_PREPARATION']:
    c=case(outcome=outcome)
    check('excluded_non_model_'+outcome, not ns['classify'](c[0],c[1])['model_outcome'])
for change,label in [
    (lambda r:r.update(status='FAILED'),'generic_failed'),
    (lambda r:r['stage_records'][0].update(exit_code=-9),'stage_signal'),
    (lambda r:r['stage_records'][0].update(exit_code=1),'stage_failure'),
    (lambda r:r['stage_records'].append({}),'missing_stage_metadata'),
    (lambda r:r.update(stage_records=[]),'empty_stage_list'),
]:
    c=case(result_change=change)
    check(label, not ns['classify'](c[0],c[1])['model_outcome'])
# Check unselected scientific string values are never passed to json.loads.
original = ns['Selector'].string
def inspect_string(self, decode=False):
    if decode and self.raw[self.i:].startswith(b'"DO_NOT_MATERIALIZE"'):
        raise AssertionError('UNSELECTED_VALUE_DECODED')
    return original(self, decode)
ns['Selector'].string = inspect_string
c=case()
check('unselected_value_not_decoded', ns['classify'](c[0],c[1])['model_outcome'])
ns['Selector'].string = original
for text in [b'{"status":"ROUTE_A_NO_FIXED_POINT","status":"FAILED"}',
             b'{"status":[]}', b'{"stage_records":[{}]}']:
    try:
        ns['Selector'](text,'result').select(ns['ALLOWED']['result'])
        refused=False
    except ns['Refused']:
        refused=True
    check('malformed_scalar_or_stage_'+str(len(checks)), refused)
result = {'schema':'CAUSE_INDEPENDENT_REVIEW_CX3V001',
          'date_u':subprocess.check_output(['date','-u'],text=True).strip(),
          'status':'TESTED_SOURCE_CENSUS_AND_INERT_METADATA_ONLY',
          'inputs':inputs, 'roots':roots, 'modules':modules, 'checks':checks,
          'scientific_modules_executed':False, 'real_run_outputs_opened':False,
          'vocabulary_scope':'Independent exact-token emission census within declared source union; not a proof for arbitrary dynamic imports.',
          'pending_scope_question':'Monitor receipt metadata is read before post-seal attestation; no result/finish is opened.',
          'self_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out = O/'INDEPENDENT_CX3V001.json'
with out.open('x') as f:
    json.dump(result,f,sort_keys=True,indent=2,allow_nan=False)
    f.write('\n')
print(json.dumps({'ok':True,'modules':len(modules),'checks':len(checks),
                  'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
