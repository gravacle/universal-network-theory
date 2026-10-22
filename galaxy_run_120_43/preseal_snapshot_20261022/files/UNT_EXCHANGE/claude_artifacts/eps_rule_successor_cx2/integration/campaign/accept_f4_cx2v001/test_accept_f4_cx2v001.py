"""D017 bounded source and synthetic-module tests; no actual accept/context/handoff."""
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import types

HERE=Path(__file__).absolute().parent
ART=HERE.parents[3]
CAMPAIGN=HERE.parent
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip()
PINS={};CHECKS=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    p=Path(p);b=p.read_bytes();PINS[str(p)]=sha(b);return b
def pin(p):return {'path':str(p),'sha256':sha(read(p))}
def check(name,ok,detail=None):CHECKS.append({'name':name,'passed':bool(ok),'detail':detail})
def tree(p):return ast.parse(read(p),filename=str(p))
def assignment(t,name):return next(n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(q,ast.Name) and q.id==name for q in n.targets))
def fn(t,name):return next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==name)
def dump(n):return ast.dump(n,include_attributes=False)
oldp=ART/'h3_campaign_path_c2/h3_accept_call_c2v004.py';newp=CAMPAIGN/'h3_accept_call_a296_cx2v001.py'
old=tree(oldp);new=tree(newp)
assert pin(oldp)['sha256']=='eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19'
assert pin(newp)['sha256']=='edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007'
entries={
    'a296':CAMPAIGN/'h3_campaign_entry_a296_cx2v001.py',
    'r12':CAMPAIGN/'placeholder_chain_a296_cx2v001/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py',
    'old':ART/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py',
}
names={k:ast.literal_eval(assignment(tree(p),'ENTRY_NAME').value) for k,p in entries.items()}
entryline=ast.literal_eval(assignment(new,'ENTRY_LINE').value)
check('source_derived_A296_and_r12_entry_names_match',names['a296']==names['r12']==entryline=='h3_campaign_entry_a296_cx2v001')
check('old_source_name_is_distinct',names['old']=='h3_campaign_entry_c2v004' and names['old']!=entryline)
def wrapper_guard(p):
    node=assignment(tree(p),'G').value
    ref={'path':ast.literal_eval(node.args[0].args[0]),'sha256':ast.literal_eval(next(k.value for k in node.keywords if k.arg=='expected'))}
    assert pin(ref['path'])==ref
    return ref
newguard=wrapper_guard(CAMPAIGN/'calibration_orchestrator_q5b1_ledger_a296_cx2v001.py')
oldguard=wrapper_guard(ART/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py')
frozen=json.loads(read(ART/'c1_h1_c2/C1_H1_C2V001.json'))
six=copy.deepcopy(frozen['tail_readiness']['approved_certificate_producers'])
bridge=pin(CAMPAIGN.parent/'point_response_admission_a296_bridge_cx2v002.py')
seven=six+[bridge]
check('source_derived_six_plus_bridge',len(six)==6 and len(seven)==7 and bridge['sha256']=='1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4')
check('guard_source_sha_contract',oldguard['sha256']=='9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677' and newguard['sha256']=='3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25')

# Owned physical modules contain only test names, an object and trace functions.
# Actual load_module/load_chain AST executes these modules, never real entries.
fixtures=HERE/'fixtures';fixtures.mkdir()
entryrefs={}
for label,name in list(names.items())+[('unnamed',None)]:
    body=(('ENTRY_NAME = '+repr(name)+'\n') if name is not None else '')+'SYNTHETIC_TEST_ONLY = True\nTRACE = []\nWRAPPER = object()\ndef load_wrapper():\n    TRACE.append("load_wrapper")\n    return WRAPPER\ndef check_patch(wrapper):\n    TRACE.append("check_patch")\n    assert wrapper is WRAPPER\n'
    p=fixtures/('entry_'+label+'.py')
    with p.open('x') as f:f.write(body)
    entryrefs[label]=pin(p)

ns={'Path':Path,'hashlib':hashlib,'importlib':__import__('importlib'),'sys':sys,'json':json}
constants=['ENTRY_LINE','HANDOFF','DEPS_SCHEMA','DEP_KEYS','POLICY_KEYS']
nodes=[assignment(new,n) for n in constants]+[next(n for n in new.body if isinstance(n,ast.ClassDef) and n.name=='Refused')]+[fn(new,n) for n in ('load_module','load_chain','read_deps')]
exec(compile(ast.Module(body=copy.deepcopy(nodes),type_ignores=[]),'D017_selected_functions','exec'),ns)
Refused=ns['Refused']
# Preserve the exact original predicate statements, not a hand-restated gate.
oldchecks=[n for n in fn(old,'accept').body if 267<=n.lineno and n.end_lineno<=277]
newchecks=[n for n in fn(new,'accept').body if 267<=n.lineno and n.end_lineno<=277]
check('actual_dependency_predicate_AST_unchanged',dump(ast.Module(body=oldchecks,type_ignores=[]))==dump(ast.Module(body=newchecks,type_ignores=[])) and len(newchecks)==7)
gate=ast.parse('def dependency_check(M,ctx,deps_path,deps_sha256):\n    pass\n').body[0]
gate.body=copy.deepcopy(newchecks)+[ast.Return(value=ast.Constant(value=True))]
gate=ast.fix_missing_locations(gate)
ns['O']=types.SimpleNamespace(sha256_file=lambda p:newguard['sha256'] if str(p)==newguard['path'] else (_ for _ in ()).throw(AssertionError('UNEXPECTED_GUARD_PATH')))
exec(compile(ast.Module(body=[gate],type_ignores=[]),'D017_exact_dependency_predicate','exec'),ns)
M=types.SimpleNamespace(G=types.SimpleNamespace(__file__=newguard['path']))
tr=copy.deepcopy(frozen['tail_readiness']);tr['approved_certificate_producers']=seven
ctx=types.SimpleNamespace(cfg={'tail_readiness':tr})
base={'schema':ns['DEPS_SCHEMA'],'status':'ROOT_FILLED','SYNTHETIC_TEST_ONLY':True,'production_admissible':False,'deps':{k:{'path':str(fixtures/('unused_'+k+'.json')),'sha256':'0'*64} for k in ns['DEP_KEYS']},'policy':{k:[] for k in ns['POLICY_KEYS']}}
base['deps']['enumerator']=tr['state_enumerator'];base['deps']['guard']=newguard;base['policy']['approved_certificate_producers']=seven
deprefs={}
cases={'guard3939_ordered7':copy.deepcopy(base),'guard9e3_ordered7':copy.deepcopy(base),'guard3939_six':copy.deepcopy(base),'guard3939_reordered7':copy.deepcopy(base),'guard3939_changed_producer':copy.deepcopy(base),'changed_enumerator':copy.deepcopy(base)}
cases['guard9e3_ordered7']['deps']['guard']=oldguard
cases['guard3939_six']['policy']['approved_certificate_producers']=six
cases['guard3939_reordered7']['policy']['approved_certificate_producers']=seven[1:2]+seven[:1]+seven[2:]
cases['guard3939_changed_producer']['policy']['approved_certificate_producers'][-1]['sha256']='0'*64
cases['changed_enumerator']['deps']['enumerator']=dict(tr['state_enumerator'],sha256='0'*64)
for label,doc in cases.items():
    p=fixtures/('deps_'+label+'.json')
    with p.open('x') as f:json.dump(doc,f,indent=2,sort_keys=True);f.write('\n')
    deprefs[label]=pin(p)

# No more writes or source reads while the selected functions run.
testing=True
allowed={x['path'] for x in entryrefs.values()}|{x['path'] for x in deprefs.values()}
def fence(event,args):
    if not testing:return
    if event.startswith(('subprocess.','socket.')) or event in ('os.system','os.fork','os.posix_spawn','os.remove','os.rename','os.rmdir','os.mkdir'):raise RuntimeError('D017_NO_PROCESSES_OR_MUTATIONS')
    if event=='open':
        p=os.fsdecode(args[0]) if isinstance(args[0],(str,bytes,os.PathLike)) else None
        if p not in allowed or args[2]&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC):raise RuntimeError('D017_ONLY_OWNED_FIXTURE_READS')
sys.addaudithook(fence)
for label in ('a296','r12'):
    ref=entryrefs[label];E,W=ns['load_chain'](ref['path'],ref['sha256'])
    check('load_chain_accepts_'+label,E.ENTRY_NAME==names[label] and W is E.WRAPPER and E.TRACE==['load_wrapper','check_patch'])
for label in ('old','unnamed'):
    ref=entryrefs[label]
    try:ns['load_chain'](ref['path'],ref['sha256'])
    except Refused as exc:check('load_chain_refuses_'+label,'ENTRY_NOT_A296_LINE' in str(exc),str(exc))
    else:check('load_chain_refuses_'+label,False)
    check(label+'_refused_before_wrapper',sys.modules['_h3_accept_entry'].TRACE==[])
try:ns['load_chain'](entryrefs['a296']['path'],'0'*64)
except Refused as exc:check('entry_wrong_pin_refused','PIN_MISMATCH' in str(exc))
else:check('entry_wrong_pin_refused',False)

# Old-line mutant must fail the positive A296/r12 acceptance contract.
mut=dict(ns);mut['ENTRY_LINE']=names['old']
exec(compile(ast.Module(body=[copy.deepcopy(fn(new,'load_chain'))],type_ignores=[]),'D017_old_line_mutant','exec'),mut)
for label in ('a296','r12'):
    ref=entryrefs[label]
    try:mut['load_chain'](ref['path'],ref['sha256'])
    except Refused:check('old_line_mutant_killed_'+label,sys.modules['_h3_accept_entry'].TRACE==[])
    else:check('old_line_mutant_killed_'+label,False)

for label in cases:
    ref=deprefs[label]
    try:passed=ns['dependency_check'](M,ctx,ref['path'],ref['sha256'])
    except Refused as exc:
        want='guard' if label=='guard9e3_ordered7' else ('enumerator' if label=='changed_enumerator' else 'approved_certificate_producers')
        check('dependency_'+label,label!='guard3939_ordered7' and 'DEPS_DIFFER_FROM_CONFIG' in str(exc) and want in str(exc),str(exc))
    else:check('dependency_'+label,label=='guard3939_ordered7' and passed is True)
# The unchanged gate is exact equality against selected config, not a new count7 rule.
sixctx=types.SimpleNamespace(cfg={'tail_readiness':dict(tr,approved_certificate_producers=six)})
ref=deprefs['guard3939_six']
check('matching_legacy_six_config_and_deps_still_pass',ns['dependency_check'](M,sixctx,ref['path'],ref['sha256']) is True)
testing=False

# Normalize only the explicitly allowed executable string changes and docstring.
rest=copy.deepcopy(new);rest.body=rest.body[1:];baseline=copy.deepcopy(old);baseline.body=baseline.body[1:]
assignment(rest,'ENTRY_LINE').value=copy.deepcopy(assignment(old,'ENTRY_LINE').value)
for n in ast.walk(fn(rest,'load_chain')):
    if isinstance(n,ast.Constant) and isinstance(n.value,str):n.value=n.value.replace('ENTRY_NOT_A296_LINE','ENTRY_NOT_C2V004_LINE')
check('whole_module_AST_only_D017_allowed_delta',dump(rest)==dump(baseline))
unchanged=[]
for n in old.body:
    if isinstance(n,ast.FunctionDef) and n.name!='load_chain':
        equal=dump(n)==dump(fn(new,n.name));unchanged.append(n.name);check('unchanged_function_'+n.name,equal)
line_changes=[i for i,(a,b) in enumerate(zip(read(oldp).decode().splitlines(),read(newp).decode().splitlines()),1) if a!=b]
check('byte_line_delta_only_declared_lines',line_changes==[1,5,6,20,73,94,144] and len(read(oldp).splitlines())==len(read(newp).splitlines()),line_changes)
for p in [ART/'h3_campaign_path_c2/README_CAMPAIGN_CERT_C2V004.md',ART/'h3_campaign_path_c2/ACCEPT_DEPS_RECORD_C2V001_TEMPLATE.json',ART/'s4_acceptance_c2/acceptance_q2/acceptance_handoff_c2v004.py',HERE/'BUILD_CX2V001.json',Path(__file__)]:read(p)
report={'schema':'D017_ACCEPT_CALL_TESTS_CX2V001','date_u':DATE,'status':'TESTED_PASS' if all(c['passed'] for c in CHECKS) else 'TESTED_FAIL','passed':sum(c['passed'] for c in CHECKS),'total':len(CHECKS),'checks':CHECKS,'sources_and_owned_fixtures':[{'path':p,'sha256':h} for p,h in sorted(PINS.items())],'source_derived_entry_names':names,'source_derived_guard_pins':{'old':oldguard,'a296':newguard},'unchanged_functions':unchanged,'scope':'Actual load_module/load_chain AST on physically owned synthetic entry modules; exact accept dependency-predicate AST plus read_deps on owned JSON fixtures. No real entry/wrapper module, accept(), production Context/handoff/volume/run data or launch executed. Equality is against selected root config; matching legacy six/six behavior is intentionally unchanged. Production acceptance UNTESTED.'}
out=HERE/'TEST_RESULTS_CX2V001.json'
with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
print(json.dumps({'status':report['status'],'passed':report['passed'],'total':report['total'],'result':pin(out),'failures':[c for c in CHECKS if not c['passed']]}))
