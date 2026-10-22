"""Provisional immutable-snapshot review, exact inert D05/B8 controls; never real seal/science."""
from pathlib import Path
import ast,copy,hashlib,json,os,re,subprocess,sys,types
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1')
SNAP=ROOT/'provisional_snapshot_v002';OUT=ROOT/'ascii_delta_controls_v001'
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip();NICE=os.getpriority(os.PRIO_PROCESS,0)
manifest=json.loads((SNAP/'SNAPSHOT_CX1V002.json').read_bytes());PINS={Path(x['snapshot_path']).name:x['sha256'] for x in manifest['sources']}
DENIED=[];CHECKS=[];FINDINGS=[];METADATA=[]
def lexical(path):
 if isinstance(path,(str,bytes,os.PathLike)):
  p=os.fsdecode(path)
  if '/runs_ext/' in p or '/KMAX_A2F10_C5H_RUN_V001' in p or ('ngc3198' in p.lower() and any(x in p.lower() for x in ('observ','target','velocity','velocities'))) or '/.codex/' in p:
   DENIED.append(['lexical',p]);raise PermissionError('protected path prohibited before metadata')
for name in ('stat','lstat','readlink'):
 orig=getattr(os,name)
 def wrapped(path,*a,_orig=orig,**kw):lexical(path);return _orig(path,*a,**kw)
 setattr(os,name,wrapped)
def audit(event,args):
 if event in ('subprocess.Popen','os.system','socket.connect','socket.getaddrinfo','os.remove','os.rename','os.rmdir','os.chmod','os.chown','os.utime'):
  DENIED.append(event);raise PermissionError('inert review prohibits '+event)
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  lexical(args[0]);p=Path(os.fsdecode(args[0])).absolute();s=str(p)
  if not (p.is_relative_to(ROOT) or s.startswith(sys.base_prefix+'/')):
   DENIED.append([event,s]);raise PermissionError('outside review read '+s)
  flags=args[2] if len(args)>2 and isinstance(args[2],int) else 0
  if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_APPEND|os.O_TRUNC):
   if not p.is_relative_to(OUT) or not flags&os.O_EXCL:
    DENIED.append([event,s]);raise PermissionError('exclusive control output only')
sys.addaudithook(audit)
def h(raw):return hashlib.sha256(raw).hexdigest()
def put(p,raw):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(raw)
 return p
def jp(p,obj):return put(p,(json.dumps(obj,sort_keys=True,indent=1,allow_nan=False)+'\n').encode())
def pin(p):return {'path':str(p),'sha256':h(p.read_bytes())}
def ck(name,ok,detail=None):CHECKS.append({'name':name,'passed':bool(ok),'detail':detail})
def source(name):
 p=SNAP/(name+'.py');raw=p.read_bytes();assert h(raw)==PINS[p.name];return p,raw
def load(name):
 p,raw=source(name);m=types.ModuleType(name);m.__file__=str(p);sys.modules[name]=m;exec(compile(raw,str(p),'exec'),m.__dict__);return m

C=load('seal_common_c4v003');T1=load('check_frozen_addendum_c4v003')
def body(changed=False,later=False):
 return b''.join(('## A%d: synthetic rule\n%s\n'%(n,'changed scientific rule' if changed and n==90 else 'synthetic rule '+str(n))).encode() for n in range(82,103 if later else 102))
base=body();rows=[]
for n,parts in T1.sections(base).items():
 heading,sec=parts[0];rows.append({'entry':'A'+str(n),'decision':'NO_CHANGE','reason':'no change, because this synthetic rule has no operative delta','section_sha256':h(sec),'section_bytes':len(sec),'heading':heading})
def entry_case(name,raw=base,covered=(),mode=None,edit=None,want='PASS',pin_bad=False,raw_override=None):
 d=OUT/'D05'/name;f=put(d/'SYNTH_V005_ADDENDUM_FROZEN.md',raw)
 pr=jp(d/'SYNTH_PREREG.json',{'sources':['A82-A101'],'entries_after_A81':{'rows':copy.deepcopy(rows)},'seal_slots':{'frozen_addendum':{'path_to_be':str(f),'value':pin(f)}}})
 disp=None;dp=None;obj=None
 if mode:
  n=90 if mode=='changed' else 102;sec=T1.sections(raw)[n][0][1]
  row={'entry':'A'+str(n),'disposition':'no_change','reason':('A90 changed from synthetic rule 90 to changed scientific rule; this explicit fixture change does not alter the synthetic decision.' if n==90 else 'A102 adds synthetic review metadata with no operative effect.'),'section_sha256':h(sec)}
  if n==90:row['change']={'from_section_sha256':h(T1.sections(base)[90][0][1]),'to_section_sha256':h(sec),'what_changed':'A90 body changed from synthetic rule 90 to changed scientific rule.'}
  obj={'schema':C.DISPOSITIONS_SCHEMA,'frozen_addendum_sha256':h(raw),'entries':[row]}
  if edit:edit(obj)
  dr=raw_override if raw_override is not None else (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
  dp=put(d/'SYNTH_DISPOSITIONS.json',dr);disp=(str(dp),'0'*64 if pin_bad else h(dr))
 res=T1.run(str(pr),str(f),h(raw),covered,False,disp)
 ck('D05/'+name,res['verdict']==want,{'actual':res['verdict'],'expected':want,'codes':[x['code'] for x in res['failures']]})
 return res,disp,dp,obj

entry_case('later_ascii_valid',body(later=True),mode='later')
entry_case('later_unicode_digit_refused',body(later=True),mode='later',edit=lambda o:o['entries'][0].update(entry='A10\u0662'),want='REFUSE')
pv=entry_case('PV_D05_1_unchanged_failure',body(changed=True),mode='changed',edit=lambda o:(o['entries'][0].update(reason='no change, because this synthetic rule has no operative delta'),o['entries'][0]['change'].update(what_changed='no change')),want='REFUSE')
# Audit executable delta against the prior pinned snapshot: only the entry-ID regex assignment changed.
oldraw=(ROOT/'provisional_snapshot_v001/check_frozen_addendum_c4v003.py').read_bytes();newraw=(SNAP/'check_frozen_addendum_c4v003.py').read_bytes()
assert h(oldraw)=='72d9191d064e61e0a3f6d40d04848971d1babd852236ddae4da36b8ca910a612'
def except_regex(raw):
 tree=ast.parse(raw);tree.body=[n for n in tree.body if not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='DISPOSITION_ENTRY_RX' for t in n.targets))];return ast.dump(tree,include_attributes=False)
delta_only=except_regex(oldraw)==except_regex(newraw);assert delta_only
missing=[name for name in ('no_change_after_change','changed_text','why_no_prereg_effect') if name not in newraw.decode()]
assert NICE==10 and sys.flags.isolated==1 and sys.dont_write_bytecode and not DENIED
result={'date_u':DATE,'status':'TESTED_PROVISIONAL_ASCII_DELTA_PV_D05_1_STILL_FAILS','count':len(CHECKS),'passed':sum(x['passed'] for x in CHECKS),'checks':CHECKS,'blocking_count':1,'finding':'PV-D05-1 remains: exact generic changed-A90 no_change input is still accepted. 0640 mechanical interface absent; no new blocking finding counted separately.','only_executable_delta_is_entry_regex':delta_only,'missing_0640_tokens':missing,'successor_0640_runtime':'UNTESTED_INTERFACE_NOT_IMPLEMENTED','source_pins':manifest['sources'],'snapshot_manifest':pin(SNAP/'SNAPSHOT_CX1V002.json'),'harness':pin(Path(__file__)),'pv_fixture':pin(pv[2]),'audit_denials':DENIED,'scope':'Actual checked-buffer common/T1 imports with only three focused runtime cases. No repeated broad suite; no full builder or comparator execution. Final selected publication absent. No author changes, production or target/protected reads.'}
p=jp(OUT/'RESULTS_CX1V001.json',result);print(json.dumps({'result':pin(p),'passed':result['passed'],'count':result['count'],'failed':[x for x in CHECKS if not x['passed']],'missing_0640_tokens':missing,'only_executable_delta_is_entry_regex':delta_only},indent=1))
