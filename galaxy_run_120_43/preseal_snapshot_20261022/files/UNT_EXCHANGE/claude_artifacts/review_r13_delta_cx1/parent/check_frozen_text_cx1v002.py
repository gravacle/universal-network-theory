import ast,hashlib,json,os,re,stat,subprocess,sys
from pathlib import Path
assert os.getpriority(os.PRIO_PROCESS,0)>=10
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUT=BASE/'review_r13_delta_cx1/parent'
R13=BASE/'v007_compare_c2/r13';R12=BASE/'v007_compare_c2/r12/kmax_tail_compare_c2v007_r12_cx3v002.py'
FIX=BASE/'review_v007_compare_c3/r12_review/A_dupjson/run_r12_003/fixtures/checks'
def sha(b):return hashlib.sha256(b).hexdigest()
def lexical(p):
 p=Path(p);parts=[v.lower() for v in p.parts];s=str(p).lower()
 assert p.is_absolute() and not any(v.startswith('uvt_') or v=='kmax_a2f10_c5h_run_v001' or v in ('.codex','.codex-alt') for v in parts)
 assert not ('ngc3198' in s and any(v in s for v in ('observed','velocit','rotmod')))
 return p
def safe(p):
 p=lexical(p);todo=list(p.parts[1:]);cur=Path('/');links=0
 while todo:
  v=todo.pop(0)
  if v in ('','.'):continue
  if v=='..':cur=cur.parent;continue
  q=lexical(cur/v);st=os.lstat(q)
  if stat.S_ISLNK(st.st_mode):
   links+=1;assert links<=40;t=os.readlink(q);lexical(Path(t) if os.path.isabs(t) else cur/t)
   if os.path.isabs(t):cur=Path('/');todo=list(Path(t).parts[1:])+todo
   else:todo=list(Path(t).parts)+todo
  else:cur=q
 return lexical(cur)
cache={};pins={}
def read(p):
 p=Path(p);key=str(p)
 if key not in cache:cache[key]=safe(p).read_bytes();pins[key]=sha(cache[key])
 return cache[key]
selp=R13/'SELECTED_R13_CX3V001.json';manp=R13/'HASHES_R13_CX3V001.json'
assert sha(read(selp))=='10acd09887bffa5130e2ebbff7d54ab2d70ea7aff0fb2cd696e0cda0fcf6bb5e'
assert sha(read(manp))=='d4509325af5feae7f3e5bcc15552c38004072f525cebb7a9da111940a4985557'
sel=json.loads(read(selp));manifest=json.loads(read(manp));verified=[]
for entry in manifest['files']:
 raw=read(entry['path']);assert sha(raw)==entry['sha256'] and len(raw)==entry['bytes'],entry['path'];verified.append(entry)
for key,e in sel.items():
 if isinstance(e,dict) and set(e)>={'path','sha256'}:assert sha(read(e['path']))==e['sha256'] and len(read(e['path']))==e['bytes']
P13=Path(sel['selected_source']['path']);assert sel['supersedes_selected_source']['path']==str(R12)
NOSHA="driver build: the check_record does not name the build's driver sha256";NOPASS='driver build: the check_record carries no PASS verdict token'
virtual={};cases=[]
for branch in ('r5','r6'):
 t1=next(p for p in FIX.glob('T01_*__'+branch+'.bin') if '__CANDIDATE__' not in p.name);driver=re.search(rb'[0-9a-f]{64}',read(t1)).group().decode()
 for i in range(1,20):
  matches=[p for p in FIX.glob('T%02d_*__%s.bin'%(i,branch)) if '__CANDIDATE__' not in p.name];assert len(matches)==1
  p=matches[0];virtual[str(p)]=read(p)
  exp=[NOPASS] if i in (5,8,11) else [NOSHA] if i in (6,7,17) else [NOSHA,NOPASS] if i==14 else []
  cases.append((p,driver,exp))
class InertPath:
 def __init__(self,p):assert str(p) in virtual;self.p=str(p)
 def read_bytes(self):return virtual[self.p]
names={'DuplicateKey','_hook_factory','loads_strict','_hex64','dup_naming_code','check_record_codes'}
def load(p):
 tree=ast.parse(read(p));nodes=[];found=set()
 for n in tree.body:
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names:nodes.append(n);found.add(n.name)
  elif isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GATE_SCHEMA' for t in n.targets):assert isinstance(n.value,ast.Constant);nodes.append(n)
 assert found==names
 g={'json':json,'re':re,'Path':InertPath};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'::exact_classifiers','exec'),g);return g
mods=[load(R12),load(P13)]
assert sys.get_int_max_str_digits()==4300
results=[]
for p,driver,exp in cases:
 got=[m['check_record_codes'](str(p),driver) for m in mods]
 results.append({'fixture_pin':{'path':str(p),'sha256':sha(virtual[str(p)])},'expected':exp,'r12':got[0],'r13':got[1],'pass':got[0]==got[1]==exp})
assert len(results)==38 and all(r['pass'] for r in results)
now=subprocess.check_output(['date','-u'],text=True).strip()
report={'schema':'UNT_R13_FROZEN_TEXT_REVIEW_CX1V001','date_u':now,'status':'TESTED','verdict':'PASS','blocking_count':0,'frozen_selection_sha256':pins[str(selp)],'frozen_manifest_sha256':pins[str(manp)],'selected_manifest_entries_verified':len(verified),'registered_text_controls':19,'driver_fixture_branches':['r5','r6'],'cases':38,'per_version_expected_matches':38,'total_inert_classifier_invocations':76,'unchanged_outcomes':38,'results':results,'pins':pins,'harness_note':'V001 stopped before controls because a broad glob also matched historical CANDIDATE fixtures; V002 selects only original registered fixtures. No candidate source changed.','limits':['Only exact AST classifier definitions invoked against named in-memory synthetic fixture bytes; no full comparator import/execution.','Real production records, scientific results, launch readiness and targets remain UNTESTED.','Frozen 202-entry artifact manifest verified from bytes; actual protected paths were not accessed.']}
report['harness_pin']={'path':str(Path(__file__)),'sha256':sha(Path(__file__).read_bytes())}
p=OUT/'FROZEN_TEXT_REVIEW_CX1V002.json'
with p.open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'verdict':'PASS','blocking_count':0,'manifest_entries':len(verified),'registered_controls':19,'driver_branches':2,'inert_invocations':76,'report':str(p),'sha256':sha(p.read_bytes())}))
