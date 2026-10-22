"""Bounded synthetic review: candidate seal tools r2; never execute real compare or create a real seal."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,os,resource,subprocess,sys,types
D=Path(__file__).resolve().parent
B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
DATE=subprocess.check_output(['date','-u'],text=True).strip()
FILES={
 'seal_common_c4v002.py':'f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10',
 'check_frozen_addendum_c4v002.py':'06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891',
 'print_driver_build_record_c4v002.py':'fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673',
 'build_seal_record_c4v002.py':'4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52'}
denials=[];pins=[];checks=[];findings=[]
def audit(event,args):
 if event in ('subprocess.Popen','os.system','socket.connect','socket.getaddrinfo','os.remove','os.rename','os.rmdir'):
  denials.append([event,None]);raise PermissionError('review operation denied')
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0])).absolute();s=str(p)
  if '/runs_ext/' in s or '/.codex/' in s or not (p.is_relative_to(D) or p in [B/n for n in FILES] or s.startswith(sys.base_prefix+'/')):
   denials.append([event,s]);raise PermissionError('non-review read denied')
  flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
  if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_APPEND|os.O_TRUNC):
   if not p.is_relative_to(D) or not flags&os.O_EXCL:
    denials.append([event,s]);raise PermissionError('non-exclusive review write denied')
sys.addaudithook(audit)
def h(raw):return hashlib.sha256(raw).hexdigest()
def put(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw)
 return p
def jp(p,obj):return put(p,(json.dumps(obj,sort_keys=True,indent=1,allow_nan=False)+'\n').encode())
def ck(name,ok,detail=None):checks.append({'name':name,'passed':bool(ok),'detail':detail})
def load(name):
 p=B/(name+'.py');raw=p.read_bytes();assert h(raw)==FILES[p.name];pins.append({'path':str(p),'sha256':h(raw),'bytes':len(raw)})
 m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(raw,str(p),'exec'),m.__dict__);return m
C=load('seal_common_c4v002');T1=load('check_frozen_addendum_c4v002');T5=load('print_driver_build_record_c4v002')
# The builder's pure validation/formatting helpers are compiled from its exact AST;
# the full builder and its real slot/admission machinery are never imported/called.
raw=(B/'build_seal_record_c4v002.py').read_bytes();assert h(raw)==FILES['build_seal_record_c4v002.py'];pins.append({'path':str(B/'build_seal_record_c4v002.py'),'sha256':h(raw),'bytes':len(raw)})
names={'no_change_note','key_map_codes','new_items_codes','custody_codes'}
consts={'KEY_MAP_SCHEMA','NEW_ITEMS_SCHEMA','CUSTODY_SCHEMA','KEY_MAP_ENTRY_KEYS','KEY_MAP_UNMAPPABLE','NEW_DISPOSITIONS'}
tree=ast.parse(raw);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in consts for t in n.targets)]
ns={'C':C,'json':json,'Path':Path,'re':__import__('re')};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(B/'build_seal_record_c4v002.py'),'exec'),ns)
def body(changed=False,later=False):
 return b''.join(('## A%d: synthetic rule\n%s\n'%(n,'changed scientific rule' if changed and n==90 else 'synthetic rule '+str(n))).encode() for n in range(82,103 if later else 102))
base=body();rows=[]
for n,parts in T1.sections(base).items():
 heading,sec=parts[0];rows.append({'entry':'A'+str(n),'decision':'NO_CHANGE','reason':'no change, because this synthetic rule has no operative delta','section_sha256':h(sec),'section_bytes':len(sec),'heading':heading})
def run_case(name,raw=base,edit=None,covered=(),expected='PASS',expect_sha=None):
 root=D/'fixtures'/name;fz=put(root/'SYNTH_V005_ADDENDUM_FROZEN.md',raw)
 doc={'sources':['A82-A101'],'entries_after_A81':{'rows':copy.deepcopy(rows)},'seal_slots':{'frozen_addendum':{'path_to_be':str(fz),'value':{'path':str(fz),'sha256':h(raw)}}}}
 if edit:edit(doc)
 pr=jp(root/'SYNTH_PREREG.json',doc);res=T1.run(str(pr),str(fz),expect_sha or h(raw),covered)
 ck(name,res['verdict']==expected,{'actual':res['verdict'],'failures':res['failures']})
 return res
run_case('baseline20')
run_case('missing_row',edit=lambda d:d['entries_after_A81']['rows'].pop(8),expected='REFUSE')
run_case('duplicate_row',edit=lambda d:d['entries_after_A81']['rows'].append(copy.deepcopy(d['entries_after_A81']['rows'][0])),expected='REFUSE')
run_case('nochange_missing_reason',edit=lambda d:d['entries_after_A81']['rows'][0].update(reason=''),expected='REFUSE')
run_case('revised_missing_clauses',edit=lambda d:d['entries_after_A81']['rows'][0].update(decision='REVISED_HERE'),expected='REFUSE')
run_case('wrong_frozen_hash',expect_sha='0'*64,expected='REFUSE')
run_case('later_missing',raw=body(later=True),expected='REFUSE')
later=run_case('later_bare_note',raw=body(later=True),covered=('A102',))
note=ns['no_change_note']('A102',later['changed_sections'])
ck('D05_bare_later_reproduced',later['verdict']=='PASS' and note=='A102: covers this entry for the prereg text of record (A81 RI-26)',note)
run_case('changed_row_missing',raw=body(changed=True),expected='REFUSE')
changed=run_case('changed_row_bare_note',raw=body(changed=True),covered=('A90',))
changed_note=ns['no_change_note']('A90',changed['changed_sections'])
ck('D05_bare_changed_reproduced',changed['verdict']=='PASS' and 'explicit seal-record note' in changed_note,changed_note)
for name,cov in [('range',('A102-A103',)),('repeat',('A102','A102')),('absent',('A103',)),('already_cited',('A82',))]:run_case('covered_'+name,raw=body(later=True),covered=cov,expected='REFUSE')
findings.append({'id':'ED-D05-1','severity':'BLOCKING','status':'TESTED','summary':'Bare --covered-later is sufficient for PASS and generates boilerplate rather than an honest per-entry revision/no-change reason.','later_result':later,'later_note':note,'changed_result':changed,'changed_note':changed_note,'scope':'Candidate r2 source. A final authoritative README/ruling may affect procedural interpretation; no final handoff claimed.'})
# D06: exercise actual printer orchestration with an inert reviewed-module stub.
# This tests assembly/round-trip/refusal plumbing, not actual driver admission.
stub_file=put(D/'fixtures/SYNTH_COMPARE_STUB.py',b'# inert stub; never imported\n')
stub_sha=h(stub_file.read_bytes());calls=[]
def builtin():return {'schema':'SYNTH_DRIVER_BUILD','build':'r5','driver':{'path':'/synthetic/driver','sha256':'d'*64},'check_record':None}
def activate(obj):calls.append(copy.deepcopy(obj));return obj
fake=types.SimpleNamespace(builtin_r5_build=builtin,activate_driver_build=activate)
original_loader=C.load_reviewed_compare
def fake_loader(path,sha):
 if h(Path(path).read_bytes())!=sha:raise ValueError('REVIEWED_COMPARE_BYTES_NOT_THE_SLOT')
 return fake
C.load_reviewed_compare=fake_loader
def print_case(name,data,expect):
 before=len(calls);p=put(D/'fixtures'/('check_'+name+'.txt'),data);res,text=T5.record_bytes(str(stub_file),stub_sha,str(p))
 ck('D06_'+name,res['verdict']==expect and ((text is not None)==(expect=='PASS')),res)
 if expect=='PASS':
  obj=json.loads(text);expected=builtin();expected['check_record']={'path':str(p),'sha256':h(data)}
  ck('D06_'+name+'_canonical_roundtrip',text==json.dumps(expected,indent=1,sort_keys=True)+'\n' and len(calls)-before==2 and calls[-1]==calls[-2]==expected)
 else:ck('D06_'+name+'_no_activation',len(calls)==before)
print_case('legit_text',b'PASS synthetic driver review\n','PASS')
print_case('legit_json',b'{"verdict":"PASS","n":1}\n','PASS')
print_case('duplicate',b'{"verdict":"FAIL","verdict":"PASS"}','REFUSE')
print_case('duplicate_hugeint',b'{"verdict":"FAIL","verdict":"PASS","n":'+b'1'*4301+b'}','REFUSE')
print_case('nonfinite_constant',b'{"verdict":"PASS","n":NaN}','REFUSE')
print_case('undecodable',b'\xffPASS synthetic','REFUSE')
res,text=T5.record_bytes(str(stub_file),'0'*64,str(D/'fixtures/check_legit_text.txt'));ck('D06_wrong_reviewed_sha',res['verdict']=='REFUSE' and text is None,res)
C.load_reviewed_compare=original_loader
# B7 and R10: exact pure helper calls, no builder invocation or seal output.
def helper(name,fn,obj,*args,expected='PASS'):
 ch=C.Checker(name);ret=fn(ch,obj,*args);res=ch.result();ck(name,res['verdict']==expected,res);return ret
km={'schema':ns['KEY_MAP_SCHEMA'],'key_equivalence_map':[]}
helper('R10_empty_exact_map',ns['key_map_codes'],km,[])
entry={'pointer':'/numerics/example','absent_equivalent_value':0,'b0_identity_evidence':'synthetic evidence'}
helper('R10_map_mismatch',ns['key_map_codes'],dict(km,key_equivalence_map=[entry]),[],expected='REFUSE')
helper('R10_duplicate_pointer',ns['key_map_codes'],dict(km,key_equivalence_map=[entry,entry]),[entry,entry],expected='REFUSE')
helper('R10_forbidden_pointer',ns['key_map_codes'],dict(km,key_equivalence_map=[dict(entry,pointer='/numerics/uv_tail')]),[],expected='REFUSE')
helper('R10_wrong_schema',ns['key_map_codes'],{'key_equivalence_map':[]},[],expected='REFUSE')
impl=put(D/'fixtures/SYNTH_IMPL.md',('selected source '+stub_sha+'\n').encode())
ni={'schema':ns['NEW_ITEMS_SCHEMA'],'compare_impl':{'path':str(impl),'sha256':h(impl.read_bytes())},'items':[{'id':'NEW-1','disposition':'ADOPTED','reason':'synthetic closure','must_fail_tests':['synthetic must_fail']}]}
helper('B7_newitems_good',ns['new_items_codes'],ni,stub_sha)
bad=copy.deepcopy(ni);bad['items'][0]['must_fail_tests']=[];helper('B7_adopted_without_test',ns['new_items_codes'],bad,stub_sha,expected='REFUSE')
bad=copy.deepcopy(ni);bad['items']*=2;helper('B7_duplicate_newitem',ns['new_items_codes'],bad,stub_sha,expected='REFUSE')
helper('B7_wrong_compare_identity',ns['new_items_codes'],ni,'0'*64,expected='REFUSE')
cust={'schema':ns['CUSTODY_SCHEMA'],'identity_run':'Z2','driver_sha256':'d'*64,'stages_total':3,'stages_successor':3,'verdict':'PASS','method':'synthetic'}
helper('B7_custody_good',ns['custody_codes'],cust,'d'*64)
for key,val in [('stages_successor',2),('stages_total',True),('identity_run','OTHER'),('driver_sha256','e'*64),('verdict','FAIL')]:
 helper('B7_custody_bad_'+key,ns['custody_codes'],dict(cust,**{key:val}),'d'*64,expected='REFUSE')
ck('zero_audit_denials',not denials,denials)
result={'date_u':DATE,'candidate_only':True,'checks_passed':sum(x['passed'] for x in checks),'checks_total':len(checks),'checks':checks,'findings':findings,'pins':pins,'scope':'Synthetic T1 entry/covered-later metadata, actual T5 printer with synthetic reviewed-module stub, exact-AST B7/R10 pure helpers. No real compare or seal/driver/build/admission/scientific execution.','rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'audit_denials':denials}
jp(D/'RESULTS_CX3V001.json',result)
print(json.dumps({k:result[k] for k in ('checks_passed','checks_total','rss_bytes_macos')}));print(json.dumps([x for x in checks if not x['passed']]))
assert all(x['passed'] for x in checks)
