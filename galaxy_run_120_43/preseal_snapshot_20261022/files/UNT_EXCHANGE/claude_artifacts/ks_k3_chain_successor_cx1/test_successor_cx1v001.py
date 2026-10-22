from pathlib import Path
import ast,json,hashlib,types,sys,tempfile,copy,collections
D=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/ks_k3_chain_successor_cx1'); K=D.parent/'ks_k3_chain_c2'
cn=D/'s4rc1_common_ks3_cx1v001.py';an=D/'registry_assembler_ks4_cx1v001.py'
craw=cn.read_bytes();araw=an.read_bytes()
def load(p,raw):
 m=types.ModuleType(p.stem);m.__file__=str(p);exec(compile(raw,str(p),'exec'),m.__dict__);return m
A=load(an,araw);C=A.C
# Exact AST delta, with a separate PINS comparison to forbid altered existing pins.
def filtered(raw,skip):
 return [ast.dump(n,include_attributes=False) for n in ast.parse(raw).body if not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in skip for t in n.targets))]
oc=(K/'s4rc1_common_c3v004_ks3_c2v002.py').read_bytes();oa=(K/'registry_assembler_c3v004_ks4_c2v002.py').read_bytes();OC=load(K/'s4rc1_common_c3v004_ks3_c2v002.py',oc)
added={'lo_state_adapter_s1','srb_rot_adapter_s1','evidence_s1'}
ast_checks={'common_other_nodes_identical':filtered(craw,{'PINS','CANONICAL_APPROVED_PRODUCERS_S1'})==filtered(oc,{'PINS','CANONICAL_APPROVED_PRODUCERS_S1'}),'assembler_other_nodes_identical':filtered(araw,{'COMMON_PATH','COMMON_SHA'})==filtered(oa,{'COMMON_PATH','COMMON_SHA'}),'existing_pins_identical':{k:v for k,v in C.PINS.items() if k not in added}==OC.PINS,'exactly_three_new_keys':set(C.PINS)-set(OC.PINS)==added,'non_s1_tuple_identical':C.CANONICAL_APPROVED_PRODUCERS==OC.CANONICAL_APPROVED_PRODUCERS,'common_pin_correct':A.COMMON_SHA==hashlib.sha256(craw).hexdigest()}
assert all(ast_checks.values()),ast_checks
original_pins=dict(C.PINS)
fixture=Path(tempfile.mkdtemp(prefix='cx1_0794_',dir='/private/tmp'))
def put(path,obj):
 raw=(json.dumps(obj,sort_keys=True)+'\n').encode() if not isinstance(obj,bytes) else obj
 with path.open('xb') as f:f.write(raw)
 return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()}
# Replace only test-environment pin tables with inert files; production sources unchanged.
for i,k in enumerate(C.PINS):
 p=put(fixture/f'producer_{i}.txt',k.encode());C.PINS[k]=(p['path'],p['sha256'])
row=put(fixture/'row_source.txt',b'row source');reg=put(fixture/'registry.json',{})
count=collections.Counter();active=False
allowed={str(an),str(cn)}
def audit(event,args):
 if event=='open' and isinstance(args[0],str):
  p=args[0]
  if active and p.startswith(str(fixture)):count[p]+=1
  if '/Users/bgm/Research/' in p and p not in allowed:raise RuntimeError('test research read refused: '+p)
sys.addaudithook(audit)
serial=0
six=[C.canonical_pin(k) for k in C.CANONICAL_APPROVED_PRODUCERS_S1]
non=[C.canonical_pin(k) for k in C.CANONICAL_APPROVED_PRODUCERS]
A.wrapper_l30_guard_pin=lambda: C.canonical_pin('guard_v003')
def run(producers,s1=True,ok=True,review_reverse=False):
 global serial,active
 serial+=1
 review={'schema':A.POLICY_SCHEMA,'status':'TESTED','ok':ok,'driver_sha256':C.DRIVER_SHA,'custody_deriver':C.canonical_pin('custody_ks1' if s1 else 'custody'),'state_enumerator':C.canonical_pin('state_enumerator_g6' if s1 else 'state_enumerator'),'approved_certificate_producers':list(reversed(producers)) if review_reverse else producers,'guard_sha256':C.PINS['guard_ks5' if s1 else 'guard_v003'][1],'driver_slot_rule':A.SLOT_RULE,'post_state_handoff':'TAIL_CERTIFICATE_ACCEPTANCE_CX2V001'}
 rp=put(fixture/f'review_{serial}.json',review)
 cfg={'tail_readiness':dict(certificate_registry=reg,custody_deriver=review['custody_deriver'],state_enumerator=review['state_enumerator'],certificate_policy_review=rp,approved_certificate_producers=producers)}
 cp=put(fixture/f'c1_{serial}.json',cfg)
 count.clear();active=True
 try: _,bad=A.c1_policy_gate(cp,reg,roots=(str(fixture),),s1=s1)
 finally:active=False
 return bad,dict(count),rp
cases=[]
def check(name,bad,want):
 passed=(len(bad)==want);cases.append({'id':name,'PASS':passed,'blockers':bad});return passed
check('six_pass',run(six)[0],0);check('three_compatibility_pass',run(six[:3])[0],0)
check('seventh_row_refused',run(six+[row])[0],1)
alias=copy.deepcopy(six);alias[-1]['path']=str(fixture)+'/./'+Path(alias[-1]['path']).name
check('aliased_producer_path_refused',run(alias)[0],1)
check('ok_integer_one_refused',run(six,ok=1)[0],1)
check('review_other_order_refused',run(six,review_reverse=True)[0],1)
check('non_s1_original_three_pass',run(non,s1=False)[0],0)
check('non_s1_rejects_s1_additions',run(non+six[3:],s1=False)[0],3)
bad,counts,rp=run(six)
single={'id':'audit_single_read_MUST_PASS','PASS':not bad and all(n==1 for n in counts.values()),'counts':counts,'review_pin':rp,'observed_review_opens':counts[rp['path']],'scope':'Full successor c1_policy_gate, real common read_bytes/read_json on inert files. No I/O stubs; canonical PINS test-only inert paths. Each open performs one f.read in common.','reason':'Inherited c1_policy_gate reads certificate_policy_review in C1_REQUIRED_PINS loop then rereads it for JSON parsing.'}
# Mutate only in memory; exact baseline functions otherwise unchanged.
base_tuple=C.CANONICAL_APPROVED_PRODUCERS_S1; basefn=A.c1_policy_gate
mut=[]
def mutant(name,setup,probe,restore):
 setup()
 try:killed=probe()
 finally:restore()
 mut.append({'id':name,'killed':killed});assert killed,name
mutant('restore_three',lambda:setattr(C,'CANONICAL_APPROVED_PRODUCERS_S1',base_tuple[:3]),lambda:len(run(six)[0])==3,lambda:setattr(C,'CANONICAL_APPROVED_PRODUCERS_S1',base_tuple))
C.PINS['row_mutant']=(row['path'],row['sha256'])
mutant('approve_seventh',lambda:setattr(C,'CANONICAL_APPROVED_PRODUCERS_S1',base_tuple+('row_mutant',)),lambda:not run(six+[row])[0],lambda:setattr(C,'CANONICAL_APPROVED_PRODUCERS_S1',base_tuple))
node=next(n for n in ast.parse(araw).body if isinstance(n,ast.FunctionDef) and n.name=='c1_policy_gate');src=ast.unparse(node)
def install(src):exec(compile(src,'<inert-mutant>','exec'),A.__dict__)
mutant('weaken_ok_to_equal',lambda:install(src.replace("rv.get('ok') is not True","rv.get('ok') != True")),lambda:not run(six,ok=1)[0],lambda:setattr(A,'c1_policy_gate',basefn))
mutant('omit_canonical_membership',lambda:install(src.replace('if p not in canon','if False')),lambda:not run(six+[row])[0],lambda:setattr(A,'c1_policy_gate',basefn))
mutant('omit_review_binding',lambda:install(src.replace('if rv.get(k) != v','if False')),lambda:not run(six,review_reverse=True)[0],lambda:setattr(A,'c1_policy_gate',basefn))
assert all(c['PASS'] for c in cases)
# Preserve evidence even though the required single-read test fails.
out={'verdict':'PASS' if single['PASS'] else 'FAIL','blocking_count':0 if single['PASS'] else 1,'AST':ast_checks,'policy_cases':cases,'mutations':mut,'single_read':single,'fixture_root':str(fixture),'UNTESTED':['full registry verify, published large suites, real S1 acceptance/admission and scientific runs'],'blocker':'CX1-KS-SR-01: minimal AST-only successor inherits duplicate certificate-policy-review read. A226 single-read MUST_PASS unmet. Need root ruling permitting behavior change or explicit inherited-code treatment; do not adopt as single-read.'}
# Audit allows writes only to new result paths after disabling the research-read guard.
allowed.add(str(D/'TEST_RESULT_CX1V001.json'));allowed.add(str(D/'test_successor_cx1v001.py'))
with (D/'TEST_RESULT_CX1V001.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
with (D/'test_successor_cx1v001.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print(json.dumps({'cases':len(cases),'mutations':len(mut),'single_read':single['PASS'],'review_opens':single['observed_review_opens'],'verdict':out['verdict']}))
