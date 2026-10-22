"""Provisional immutable-snapshot review, exact inert D05/B8 controls; never real seal/science."""
from pathlib import Path
import ast,copy,hashlib,json,os,re,subprocess,sys,types
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1')
SNAP=ROOT/'provisional_snapshot_v001';OUT=ROOT/'provisional_controls_v001'
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip();NICE=os.getpriority(os.PRIO_PROCESS,0)
manifest=json.loads((SNAP/'SNAPSHOT_CX1V001.json').read_bytes());PINS={Path(x['snapshot_path']).name:x['sha256'] for x in manifest['sources']}
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
# Audited module-level effects only: imports, constants, definitions and snapshot directory sys.path insertion.
C=load('seal_common_c4v003');T1=load('check_frozen_addendum_c4v003')
p,raw=source('build_seal_record_c4v003');tree=ast.parse(raw)
names={'later_entry_dispositions','_check_admission_config','check_admission_config'};consts={'SCHEMA','DISPOSITIONS_NONE_REQUIRED'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in consts for t in n.targets)]
N={'C':C,'json':json,'Path':Path};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),N)
ck('execution/nice10',NICE==10,NICE)
ck('execution/isolated_no_bytecode',sys.flags.isolated==1 and sys.dont_write_bytecode)
ck('execution/single_blas',all(os.environ.get(k)=='1' for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS')))
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
entry_case('baseline20')
entry_case('later_missing',body(later=True),want='REFUSE')
entry_case('later_bare',body(later=True),('A102',),want='REFUSE')
entry_case('changed_missing',body(changed=True),want='REFUSE')
entry_case('changed_bare',body(changed=True),('A90',),want='REFUSE')
positive=entry_case('later_explicit',body(later=True),mode='later')
entry_case('later_revised',body(later=True),mode='later',edit=lambda o:o['entries'][0].update(disposition='revised'))
entry_case('changed_explicit',body(changed=True),mode='changed')
for label,edit in [('empty',lambda o:o['entries'][0].update(reason='')),('whitespace',lambda o:o['entries'][0].update(reason=' \t ')),('missing',lambda o:o['entries'][0].pop('reason')),('bare_row',lambda o:o.update(entries=['A102'])),('duplicate',lambda o:o['entries'].append(copy.deepcopy(o['entries'][0]))),('wrong_section',lambda o:o['entries'][0].update(section_sha256='0'*64)),('wrong_frozen',lambda o:o.update(frozen_addendum_sha256='0'*64))]:
 entry_case('later_'+label,body(later=True),mode='later',edit=edit,want='REFUSE')
entry_case('wrong_file_pin',body(later=True),mode='later',pin_bad=True,want='REFUSE')
entry_case('changed_nominal_no_change_field',body(changed=True),mode='changed',edit=lambda o:(o['entries'][0].update(reason='no change, because this synthetic rule has no operative delta'),o['entries'][0].pop('change')),want='REFUSE')
entry_case('changed_empty_change',body(changed=True),mode='changed',edit=lambda o:o['entries'][0]['change'].update(what_changed=' '),want='REFUSE')
nominal=entry_case('changed_nominal_reason_nominal_change',body(changed=True),mode='changed',edit=lambda o:(o['entries'][0].update(reason='no change, because this synthetic rule has no operative delta'),o['entries'][0]['change'].update(what_changed='no change')),want='REFUSE')
if nominal[0]['verdict']=='PASS':
 FINDINGS.append({'id':'PV-D05-1','severity':'BLOCKING_PROVISIONAL','status':'TESTED','summary':'Changed cited A90 marked no_change with generic reason and what_changed="no change" is accepted. Correct section hashes alone do not satisfy 0633 requirement that the reason names the change.','fixture':pin(nominal[2]),'actual':'PASS','expected':'REFUSE','source':{'path':str(SNAP/'check_frozen_addendum_c4v003.py'),'sha256':PINS['check_frozen_addendum_c4v003.py']},'scope':'Provisional development snapshot; root may clarify whether separate non-empty what_changed is intended contract. No final published tuple reviewed.'})
# Byte carry-forward: actual exact helper; final record AST also binds this returned object directly.
r,disp,dp,obj=positive;ch=C.Checker('carry_exact');out=N['later_entry_dispositions'](ch,disp,r['later_entry_dispositions'],r['dispositions_required'])
ck('D05/exact_content_text_pin',not ch.failures and out['content']==obj and out['raw_text'].encode()==dp.read_bytes() and out['pin']==pin(dp))
orig=Path.read_bytes
try:
 def changed_read(self):return b'{}\n' if str(self)==str(dp) else orig(self)
 Path.read_bytes=changed_read;ch=C.Checker('carry_mutated');out=N['later_entry_dispositions'](ch,disp,r['later_entry_dispositions'],r['dispositions_required'])
 ck('D05/late_byte_mutation_refused',out is None and any(x['code']=='DISPOSITIONS_CHANGED_AFTER_CHECK' for x in ch.failures))
finally:Path.read_bytes=orig
for name,edit in [('content',lambda v:v['content'].update(schema='changed')),('text',lambda v:v.update(raw_text=v['raw_text']+' '))]:
 v=copy.deepcopy(r['later_entry_dispositions']);edit(v);ch=C.Checker(name);out=N['later_entry_dispositions'](ch,disp,v,r['dispositions_required']);ck('D05/passthrough_'+name+'_refused',out is None and bool(ch.failures))
buildnode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build')
recdicts=[n.value for n in ast.walk(buildnode) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rec' for t in n.targets)]
ck('D05/record_AST_exact_helper_value',len(recdicts)==1 and any(isinstance(k,ast.Constant) and k.value=='later_entry_dispositions' and isinstance(v,ast.Name) and v.id=='led' for k,v in zip(recdicts[0].keys,recdicts[0].values)))
# Six exact B8 Codex3 mutations; all dependencies are existing owned inert fixtures.
b=ROOT/'baseline_v001/B8';seal=json.loads((b/'positive/SYNTH_INERT_RECORD.json').read_bytes());seal['schema']=N['SCHEMA'];cfg0=json.loads((b/'positive/SYNTH_INERT_CONFIG.json').read_bytes())
def admission_case(name,edit=None,want='PASS'):
 obj=copy.deepcopy(seal)
 if edit:edit(obj)
 rp=jp(OUT/'B8'/name/'SYNTH_INERT_RECORD.json',obj);cfg=copy.deepcopy(cfg0);cfg['seal']=pin(rp);cp=jp(OUT/'B8'/name/'SYNTH_INERT_CONFIG.json',cfg)
 res=N['check_admission_config'](str(cp),str(rp));ck('B8/'+name,res['verdict']==want,{'actual':res['verdict'],'codes':[x['code'] for x in res['failures']]})
admission_case('positive')
for name,edit in [('wrong_sealed_by',lambda x:x.update(sealed_by={'identity':'wrong'})),('missing_sealed_by',lambda x:x.pop('sealed_by')),('malformed_driver',lambda x:x.update(driver='PENDING')),('stale_driver',lambda x:x['driver'].update(sha256='0'*64)),('malformed_frozen',lambda x:x.update(frozen_addendum=[])),('stale_frozen',lambda x:x['frozen_addendum'].update(sha256='0'*64))]:admission_case(name,edit,'REFUSE')
ck('execution/zero_audit_denials',not DENIED,DENIED)
result={'date_u':DATE,'status':'PROVISIONAL_SNAPSHOT_REVIEW_NOT_FINAL_PUBLICATION','count':len(CHECKS),'passed':sum(x['passed'] for x in CHECKS),'checks':CHECKS,'findings':FINDINGS,'snapshot_manifest':pin(SNAP/'SNAPSHOT_CX1V001.json'),'source_pins':manifest['sources'],'harness':pin(Path(__file__)),'audit_denials':DENIED,'scope':'Actual snapshot common/T1 modules; exact AST builder admission and disposition helper. Actual file-hash/reparse/late-byte mutation checks; final record attachment audited by AST. Full builder, T3 complete integration and scientific comparator not executed. No real seal, launch, C5H/protected run or target read. README not present in snapshot.'}
p=jp(OUT/'RESULTS_CX1V001.json',result)
print(json.dumps({'result':pin(p),'passed':result['passed'],'count':result['count'],'failed':[x for x in CHECKS if not x['passed']],'findings':FINDINGS},indent=1))
