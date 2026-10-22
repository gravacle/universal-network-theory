"""Inert exact-counterexample baseline for dispatch0638; no real compare/seal/admission."""
from pathlib import Path
import ast, copy, hashlib, json, os, subprocess, sys, types
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1')
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip()
PINS={'seal_common_c4v002.py':'f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10','check_frozen_addendum_c4v002.py':'06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891','build_seal_record_c4v002.py':'4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52'}
DENIED=[];CHECKS=[];SOURCES=[]
def audit(event,args):
 if event in ('subprocess.Popen','os.system','socket.connect','socket.getaddrinfo','os.remove','os.rename','os.rmdir','os.chmod','os.chown','os.utime'):
  DENIED.append(event);raise PermissionError('inert review prohibits '+event)
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=Path(os.fsdecode(args[0])).absolute();s=str(p)
  if '/runs_ext/' in s or '/.codex/' in s or not (p.is_relative_to(ROOT) or p in [BASE/n for n in PINS] or s.startswith(sys.base_prefix+'/')):
   DENIED.append([event,s]);raise PermissionError('outside inert review: '+s)
  flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
  if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_APPEND|os.O_TRUNC):
   if not p.is_relative_to(ROOT) or not flags&os.O_EXCL:
    DENIED.append([event,s]);raise PermissionError('only exclusive review output allowed')
sys.addaudithook(audit)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def put(path,raw):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('xb') as f:f.write(raw)
 return path
def jp(path,obj):return put(path,(json.dumps(obj,sort_keys=True,indent=1,allow_nan=False)+'\n').encode())
def pin(path):return {'path':str(path),'sha256':sha(path.read_bytes())}
def ck(name,ok,detail=None):CHECKS.append({'name':name,'passed':bool(ok),'detail':detail})
def load(name):
 p=BASE/(name+'.py');raw=p.read_bytes();assert sha(raw)==PINS[p.name]
 SOURCES.append({'path':str(p),'sha256':sha(raw),'bytes':len(raw)})
 mod=types.ModuleType(name);mod.__file__=str(p);sys.modules[name]=mod;exec(compile(raw,str(p),'exec'),mod.__dict__);return mod
C=load('seal_common_c4v002');T1=load('check_frozen_addendum_c4v002')
p=BASE/'build_seal_record_c4v002.py';raw=p.read_bytes();assert sha(raw)==PINS[p.name];SOURCES.append({'path':str(p),'sha256':sha(raw),'bytes':len(raw)})
names={'no_change_note','_check_admission_config','check_admission_config'}
tree=ast.parse(raw);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SCHEMA' for t in n.targets)]
N={'C':C,'Path':Path,'json':json};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),N)
def body(changed=False,later=False):
 return b''.join(('## A%d: synthetic rule\n%s\n'%(n,'changed scientific rule' if changed and n==90 else 'synthetic rule '+str(n))).encode() for n in range(82,103 if later else 102))
base=body();rows=[]
for n,parts in T1.sections(base).items():
 heading,section=parts[0];rows.append({'entry':'A'+str(n),'decision':'NO_CHANGE','reason':'no change, because this synthetic rule has no operative delta','section_sha256':sha(section),'section_bytes':len(section),'heading':heading})
def entry_case(name,raw=base,covered=(),expected='PASS'):
 d=ROOT/'baseline_v001'/'D05'/name;f=put(d/'SYNTH_V005_ADDENDUM_FROZEN.md',raw)
 prereg={'sources':['A82-A101'],'entries_after_A81':{'rows':copy.deepcopy(rows)},'seal_slots':{'frozen_addendum':{'path_to_be':str(f),'value':pin(f)}}}
 pp=jp(d/'SYNTH_PREREG.json',prereg);res=T1.run(str(pp),str(f),sha(raw),covered)
 ck('D05/'+name,res['verdict']==expected,{'actual':res['verdict'],'failures':res['failures']});return res
entry_case('baseline20')
entry_case('later_missing',body(later=True),expected='REFUSE')
r=entry_case('later_bare',body(later=True),('A102',))
note=N['no_change_note']('A102',r['changed_sections'])
ck('D05/bare_later_boilerplate_exact',note=='A102: covers this entry for the prereg text of record (A81 RI-26)',note)
entry_case('changed_missing',body(changed=True),expected='REFUSE')
r=entry_case('changed_bare',body(changed=True),('A90',));note=N['no_change_note']('A90',r['changed_sections'])
ck('D05/bare_changed_boilerplate',r['verdict']=='PASS' and 'explicit seal-record note' in note,note)
# Actual r2 admission checker AST, only owned inert metadata dependencies.
d=ROOT/'baseline_v001'/'B8';sources=[put(d/('source%02d.py'%i),('# inert source %d; never imported\n'%i).encode()) for i in range(15)]
allow={str(p):sha(p.read_bytes()) for p in sources}
build=put(d/'BUILD_V007.md',('## Supported runtime entry allowlist\n'+'\n'.join(h+'  '+p for p,h in allow.items())+'\n## end\n').encode())
prereg=jp(d/'SYNTH_PREREG.json',{'schema':'INERT_NOT_AUTHORITY'});compare=put(d/'SYNTH_COMPARE.py',b'# inert never imported\n');driver=put(d/'SYNTH_DRIVER.py',b'# inert never executed\n');frozen=put(d/'SYNTH_FROZEN.md',b'# inert frozen metadata\n')
seal={'schema':N['SCHEMA'],'sealed_by':dict(C.AUTHORITY),'prereg':pin(prereg),'compare':pin(compare),'build':pin(build),'driver':pin(driver),'frozen_addendum':pin(frozen),'admission_allowlist':allow,'launch_entry':{'launcher':pin(sources[0]),'guard':pin(sources[1])}}
def admission_case(name,edit=None,expected='PASS'):
 obj=copy.deepcopy(seal)
 if edit:edit(obj)
 rp=jp(d/name/'SYNTH_INERT_RECORD.json',obj)
 cfg={'schema':C.ADMISSION_SCHEMA,'authority':dict(C.AUTHORITY),'seal':pin(rp),'prereg':pin(prereg),'compare':pin(compare),'build':pin(build),'producer_allowlist':dict(allow),'note':'SYNTHETIC INERT: NOT AUTHORIZATION'}
 cp=jp(d/name/'SYNTH_INERT_CONFIG.json',cfg);res=N['check_admission_config'](str(cp),str(rp))
 ck('B8/'+name,res['verdict']==expected,{'actual':res['verdict'],'failures':res['failures']})
admission_case('positive')
for name,edit in [('wrong_sealed_by',lambda x:x.update(sealed_by={'identity':'wrong'})),('missing_sealed_by',lambda x:x.pop('sealed_by')),('malformed_driver',lambda x:x.update(driver='PENDING')),('stale_driver',lambda x:x['driver'].update(sha256='0'*64)),('malformed_frozen',lambda x:x.update(frozen_addendum=[])),('stale_frozen',lambda x:x['frozen_addendum'].update(sha256='0'*64))]:admission_case(name,edit)
ck('zero_audit_denials',not DENIED,DENIED)
result={'date_u':DATE,'status':'TESTED_BASELINE_DEFECT_REPRODUCTIONS','count':len(CHECKS),'passed':sum(c['passed'] for c in CHECKS),'checks':CHECKS,'source_pins':SOURCES,'harness':pin(Path(__file__)),'audit_denials':DENIED,'scope':'Exact Codex3 D05 fixtures and six B8 mutations on byte-pinned r2. Actual T1; exact AST admission/no_change helpers. No real compare or full builder imported. Synthetic records only, not valid authority; no seal installed or scientific process. Expected r2 malformed PASS results reproduce defects and are not correctness passes. v003 remains UNTESTED until frozen publication.'}
p=jp(ROOT/'BASELINE_RESULTS_CX1V001.json',result)
print(json.dumps({'result':pin(p),'count':result['count'],'passed':result['passed'],'failures':[c for c in CHECKS if not c['passed']],'scope':result['status']},indent=1))
