"""D017 independent source/AST review. No campaign, context, handoff, or producer execution."""
from pathlib import Path
import ast,copy,datetime,hashlib,json,os,sys,types
D=Path(__file__).parent;A=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');C=D.parent;tests=[];pins={};raws={};blocked=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def guard(p):
    if isinstance(p,(str,bytes,os.PathLike)):
        s=os.fsdecode(p)
        if any(x.casefold() in ('runs','runs_ext','.codex','unt_internal_runs','v007_postseal_records') or x.casefold().startswith('uvt_') or 'ngc3198' in x.casefold() or 'kmax_a2f10_c5h_run_v001' in x.casefold() for x in Path(s).parts) or s.startswith('/Volumes/'):
            blocked.append(s);raise RuntimeError('INDEPENDENT_PROTECTED_PATH')
def audit(e,a):
    if e in ('open','os.listdir','os.scandir') and a:guard(a[0])
    if e.startswith(('subprocess.','socket.')) or e in ('os.system','os.exec','os.posix_spawn'):raise RuntimeError('INDEPENDENT_NO_PROCESS_NETWORK')
sys.addaudithook(audit)
for name in ('stat','lstat','readlink'):
    o=getattr(os,name)
    def f(p,*a,_o=o,**k):guard(p);return _o(p,*a,**k)
    setattr(os,name,f)
def read(p):
    b=Path(p).read_bytes();pins[str(p)]=sha(b);raws[str(p)]=b;return b
def check(n,ok,detail=None):tests.append({'name':n,'passed':bool(ok),'detail':detail})
def val(t,name):return ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==name for x in n.targets)))
def funcs(t):return {n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
def dump(n):return ast.dump(n,include_attributes=False)
oldp=A/'h3_campaign_path_c2/h3_accept_call_c2v004.py';newp=C/'h3_accept_call_a296_cx2v001.py'
oldraw,newraw=read(oldp),read(newp);old,new=ast.parse(oldraw),ast.parse(newraw)
check('exact_predecessor_pin',sha(oldraw)=='eb895263c8458696b265b30dc5dee771dcb89649e5b490c893bb613281c7bf19')
check('exact_candidate_pin',sha(newraw)=='edcd3ffa647c143eeb2a942e46d2420d2126d9f61f33252be8c9126db1bba007')
changed=[i+1 for i,(x,y) in enumerate(zip(oldraw.decode().splitlines(),newraw.decode().splitlines())) if x!=y]
check('only_seven_expected_text_lines_changed',len(oldraw.decode().splitlines())==len(newraw.decode().splitlines()) and changed==[1,5,6,20,73,94,144],changed)
class Normalize(ast.NodeTransformer):
    def visit_Constant(self,n):
        if isinstance(n.value,str):n.value=n.value.replace('ENTRY_NOT_A296_LINE:','ENTRY_NOT_C2V004_LINE:')
        return n
normalized=Normalize().visit(copy.deepcopy(new));normalized.body[0]=copy.deepcopy(old.body[0])
for n in normalized.body:
    if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='ENTRY_LINE' for x in n.targets):n.value=ast.Constant(value=val(old,'ENTRY_LINE'))
check('complete_AST_equal_after_only_D017_allowed_changes',dump(normalized)==dump(old))
for name,node in funcs(old).items():
    if name!='load_chain':check('unchanged_function_'+name,dump(node)==dump(funcs(new)[name]))
check('entry_line_exact_A296',val(new,'ENTRY_LINE')=='h3_campaign_entry_a296_cx2v001')
entries=[('A296_template',C/'h3_campaign_entry_a296_cx2v001.py'),('A296_r12_placeholder',C/'placeholder_chain_a296_cx2v001/v006r12_c4/h3_campaign_entry_cx2v006r12_c4.py'),('old_c2v004',A/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py')]
entrydata={}
for role,p in entries:
    b=read(p);entrydata[role]={'path':str(p),'sha256':sha(b),'name':val(ast.parse(b),'ENTRY_NAME')}
# Exact load_chain body. Only loader is synthetic: it authenticates cached source
# bytes and extracts the actual static ENTRY_NAME, never executes the entry cascade.
class Refused(Exception):pass
ns={'Refused':Refused,'ENTRY_LINE':val(new,'ENTRY_LINE')};exec(compile(ast.Module(body=[copy.deepcopy(funcs(new)['load_chain'])],type_ignores=[]),str(D/'OWNED_LOAD_CHAIN_AST.py'),'exec'),ns)
events=[];mode={};wrapper=object()
def loader(path,expected,name):
    events.append(('load_entry',path,expected,name))
    if path in raws:
        if sha(raws[path])!=expected:raise Refused('PIN_MISMATCH: '+path)
        entry_name=val(ast.parse(raws[path]),'ENTRY_NAME');attrs={'ENTRY_NAME':entry_name}
    else:attrs=dict(mode)
    def load_wrapper():events.append(('load_wrapper',));return wrapper
    def check_patch(m):events.append(('check_patch',m is wrapper))
    attrs.update(load_wrapper=load_wrapper,check_patch=check_patch);return types.SimpleNamespace(**attrs)
ns['load_module']=loader
for role in ('A296_template','A296_r12_placeholder'):
    p=entrydata[role];events.clear();E,M=ns['load_chain'](p['path'],p['sha256'])
    check('load_chain_accepts_source_derived_'+role,M is wrapper and [x[0] for x in events]==['load_entry','load_wrapper','check_patch'] and events[-1][1] is True)
def rejected(name,path,expected,needle='ENTRY_NOT_A296_LINE'):
    events.clear()
    try:ns['load_chain'](path,expected);check(name,False)
    except Refused as e:check(name,needle in str(e) and [x[0] for x in events]==['load_entry'],str(e))
p=entrydata['old_c2v004'];rejected('old_entry_refused_before_wrapper',p['path'],p['sha256'])
for label,attrs in [('unnamed',{}),('null',{'ENTRY_NAME':None}),('near_name',{'ENTRY_NAME':'h3_campaign_entry_a296_cx2v001_extra'}),('wrong_case',{'ENTRY_NAME':'H3_CAMPAIGN_ENTRY_A296_CX2V001'}),('bool',{'ENTRY_NAME':True})]:
    mode.clear();mode.update(attrs);rejected(label+'_refused_before_wrapper','IN_MEMORY_ONLY', '0'*64)
p=entrydata['A296_template'];rejected('wrong_source_sha_refused_before_wrapper',p['path'],'0'*64,'PIN_MISMATCH')
ns['ENTRY_LINE']=val(old,'ENTRY_LINE')
rejected('mutant_restoring_old_entry_line_is_killed',p['path'],p['sha256'])
ns['ENTRY_LINE']=val(new,'ENTRY_LINE')
# Exact statements from accept() surrounding deps predicates, with no call to accept().
acc=funcs(new)['accept'];start=next(i for i,n in enumerate(acc.body) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='tr' for x in n.targets));stop=next(i for i in range(start,len(acc.body)) if isinstance(acc.body[i],ast.If) and isinstance(acc.body[i].test,ast.Name) and acc.body[i].test.id=='bad')
body=copy.deepcopy(acc.body[start:stop+1])+[ast.Return(value=ast.Constant(value=True))]
fn=ast.FunctionDef(name='dependency_predicates',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=x) for x in ('ctx','d','M','O')],kwonlyargs=[],kw_defaults=[],defaults=[]),body=body,decorator_list=[])
depsns={'Refused':Refused};exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(D/'OWNED_DEPS_AST.py'),'exec'),depsns)
oldguard=A/'s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py';newguard=C.parent/'guard/certificate_guard_b1_a296_cx2v003.py';oldsha=sha(read(oldguard));newsha=sha(read(newguard))
check('guard_source_byte_pins',oldsha=='9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677' and newsha=='3939bc47c48f46f9e313969d77cc7895d7dd6936648b2060df31a5aff3cc4c25')
c1=json.loads(read(A/'c1_h1_c2/C1_H1_C2V001.json'));old6=copy.deepcopy(c1['tail_readiness']['approved_certificate_producers']);bridge=C.parent/'point_response_admission_a296_bridge_cx2v002.py';bsha=sha(read(bridge));seven=old6+[{'path':str(bridge),'sha256':bsha}]
check('proposed_seven_is_exact_original_six_plus_bridge',len(old6)==6 and bsha=='1eb94a51ef00de3cf353d76863ff7405aa11ff11d336e6426b10ceae590cadd4')
enumerator={'path':'IN_MEMORY_ONLY_ENUMERATOR','sha256':'e'*64};ctx=types.SimpleNamespace(cfg={'tail_readiness':{'state_enumerator':enumerator,'approved_certificate_producers':seven}})
M=types.SimpleNamespace(G=types.SimpleNamespace(__file__=str(newguard)));O=types.SimpleNamespace(sha256_file=lambda p:pins[p])
def record(producers=None,guardsha=newsha,enum=None):return {'deps':{'enumerator':enumerator if enum is None else enum,'guard':{'path':'IN_MEMORY_ONLY_GUARD','sha256':guardsha}},'policy':{'approved_certificate_producers':copy.deepcopy(seven if producers is None else producers)}}
def depcheck(label,d,ok):
    try:v=depsns['dependency_predicates'](ctx,d,M,O);check(label,ok and v is True)
    except Refused as e:check(label,not ok and 'DEPS_DIFFER_FROM_CONFIG' in str(e),str(e))
depcheck('new_guard_and_exact_ordered_seven_accept',record(),True)
depcheck('old_guard_with_seven_refuses',record(guardsha=oldsha),False)
depcheck('foreign_guard_with_seven_refuses',record(guardsha='0'*64),False)
depcheck('new_guard_with_six_refuses',record(old6),False)
depcheck('new_guard_with_reordered_seven_refuses',record([seven[1],seven[0]]+seven[2:]),False)
depcheck('new_guard_with_duplicate_producer_refuses',record(seven[:6]+[seven[5]]),False)
depcheck('new_guard_with_extra_eighth_refuses',record(seven+[seven[0]]),False)
mut=copy.deepcopy(seven);mut[-1]['sha256']='0'*64;depcheck('new_guard_with_wrong_bridge_sha_refuses',record(mut),False)
mut=copy.deepcopy(seven);mut[-1]['path']='IN_MEMORY_ONLY_WRONG_BRIDGE';depcheck('new_guard_with_wrong_bridge_path_refuses',record(mut),False)
depcheck('new_guard_with_wrong_enumerator_refuses',record(enum={'path':'IN_MEMORY_ONLY_OTHER','sha256':'f'*64}),False)
# Contract limitation control: equality predicate trusts the native config; it is not a new count-seven authority.
ctx6=types.SimpleNamespace(cfg={'tail_readiness':{'state_enumerator':enumerator,'approved_certificate_producers':old6}})
check('inherited_predicate_is_config_equality_not_global_count_rule',depsns['dependency_predicates'](ctx6,record(old6),M,O) is True)
# No stateful rerun flow is executed. Whole-function equality proves preservation.
check('rerun_latest_pass_and_locking_entire_accept_function_unchanged',dump(funcs(old)['accept'])==dump(funcs(new)['accept']))
check('handoff_pin_and_limits_unchanged',all(val(old,k)==val(new,k) for k in ('HANDOFF','MAX_PASSES','RERUNNABLE','ACCEPTANCE_RECORD_SCHEMA','ACCEPTED','DEP_KEYS','POLICY_KEYS')))
check('source_bytes_stable',all(sha(Path(p).read_bytes())==h for p,h in pins.items()))
check('no_protected_access_attempt',not blocked,blocked)
result={'date_u':datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),'python':sys.version,'runtime':'nice unavailable (sandbox); 0514 waiver','verdict':'PASS' if all(x['passed'] for x in tests) else 'FAIL','status':'TESTED_STATIC_AND_SYNTHETIC_AST_ONLY','passed':sum(x['passed'] for x in tests),'total':len(tests),'tests':tests,'input_pins':[{'path':p,'sha256':h} for p,h in pins.items()],'source_entry_metadata':entrydata,'proposed_ordered_seven_metadata_only':seven,'limitations':['Actual load_chain body with synthetic authenticated source-derived entry loader; no entry/wrapper/context imported.','Exact dependency statements executed in memory; accept(), handoff, adapt, producer and runtime state paths never executed.','Seven-producer premise is supplied by the bound native config; unchanged equality check alone admits equal lists of any size.','Root selection, final generated bytes, source reviews, dependencies record and runtime admission remain outside this review.']}
with (D/'RESULTS_CX2V001.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'verdict':result['verdict'],'passed':result['passed'],'total':result['total'],'failed':[x for x in tests if not x['passed']],'sha256':sha((D/'RESULTS_CX2V001.json').read_bytes())}))
