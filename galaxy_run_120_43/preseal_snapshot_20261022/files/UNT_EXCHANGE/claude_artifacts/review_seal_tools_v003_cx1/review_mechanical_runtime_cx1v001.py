"""Provisional immutable-snapshot review, exact inert D05/B8 controls; never real seal/science."""
from pathlib import Path
import ast,copy,hashlib,json,os,re,subprocess,sys,types
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1')
SNAP=ROOT/'provisional_snapshot_v003';OUT=ROOT/'mechanical_runtime_controls_v001'
DATE=subprocess.check_output(['/bin/date','-u'],text=True).strip();NICE=os.getpriority(os.PRIO_PROCESS,0)
manifest=json.loads((SNAP/'SNAPSHOT_CX1V003.json').read_bytes());PINS={Path(x['snapshot_path']).name:x['sha256'] for x in manifest['sources']}
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
mp=ROOT/'rule0640_controls_v001/D05_RULE_MATRIX_CX1V001.json';mr=mp.read_bytes();assert h(mr)=='bf7aad239db8932e7e10ad9cea9ed63f246391b6278085abc7f9e0d64462e3a3';matrix=json.loads(mr)
def section(n,text=None):return ('## A%d: synthetic rule\n%s\n'%(n,text if text is not None else 'synthetic rule '+str(n))).encode()
SECTIONS={n:section(n) for n in [62]+list(range(82,102))}
MAPPINGS=[];RUNS=[]
def run(name,oldparts=None,newparts=None,row=None,want='PASS',code=None,docedit=None,oldarg=True,oldarg_other=None,row_factory=None,oldsha_override=None):
 oldparts=copy.deepcopy(SECTIONS if oldparts is None else oldparts);newparts=copy.deepcopy(oldparts if newparts is None else newparts)
 oldraw=b''.join(oldparts[n] for n in sorted(oldparts));newraw=b''.join(newparts[n] for n in sorted(newparts));d=OUT/name
 op=put(d/'OLD_ADDENDUM_AT_TEXT_OF_RECORD.md',oldraw);np=put(d/'SYNTH_V005_ADDENDUM_FROZEN.md',newraw)
 table=[]
 for n,v in T1.sections(oldraw).items():
  if n>=82:table.append({'entry':'A'+str(n),'decision':'NO_CHANGE','reason':'Inert fixture no operative change at prereg generation.','section_sha256':h(v[0][1]),'section_bytes':len(v[0][1]),'heading':v[0][0]})
 doc={'sources':['A62','A82-A101'],'entries_after_A81':{'addendum_read':{'sha256_at_generation':oldsha_override or h(oldraw),'bytes':len(oldraw)},'rows':table},'seal_slots':{'frozen_addendum':{'path_to_be':str(np),'value':pin(np)}}}
 if docedit:docedit(doc)
 pp=jp(d/'SYNTH_PREREG.json',doc)
 if row_factory:row=row_factory(pp,d)
 dp=None;disp=None
 if row is not None:
  obj={'schema':C.DISPOSITIONS_SCHEMA,'frozen_addendum_sha256':h(newraw),'entries':[row] if isinstance(row,dict) else row}
  dp=jp(d/'SYNTH_DISPOSITIONS.json',obj);disp=(str(dp),h(dp.read_bytes()))
 oldpath=str(op) if oldarg else None
 if oldarg_other is not None:oldpath=str(oldarg_other)
 res=T1.run(str(pp),str(np),h(newraw),(),False,disp,oldpath);codes=[f['code'] for f in res['failures']]
 ck(name,res['verdict']==want and (code is None or code in codes),{'actual':res['verdict'],'expected':want,'codes':codes})
 RUNS.append({'name':name,'prereg':pin(pp),'old_addendum':pin(op),'frozen':pin(np),'dispositions':pin(dp) if dp else None,'actual':res['verdict']})
 return res,pp,dp
for case in matrix['cases']:
 x=case['input'];op=copy.deepcopy(SECTIONS);np=copy.deepcopy(SECTIONS);op[90]=Path(x['old_section']['path']).read_bytes();np[90]=Path(x['new_section']['path']).read_bytes()
 dis=x['disposition'];row={'entry':'A90','disposition':dis,'section_sha256':x['new_section']['sha256']}
 if dis=='no_change_after_change':
  for k in ('changed_text','why_no_prereg_effect'):
   if k in x:row[k]=x[k]
 elif dis=='revised':
  row['reason']='Synthetic reviewer prereg revision pointer.'
  if 'prereg_revision_pointer' in x:
   ptr=x['prereg_revision_pointer'];row['prereg_revision']={k:v for k,v in ptr['document'].items() if k in ('path','sha256')} if isinstance(ptr,dict) else ptr
 elif dis=='no_change':
  row['reason']=x.get('reason','Unchanged section bytes.')
  if 'change' in x:row['change']=x['change']
 # The matrix's stale old-section pin maps to the actual table-row source anchor.
 def docedit(doc,oldsha=x['old_section']['sha256']):
  next(z for z in doc['entries_after_A81']['rows'] if z['entry']=='A90')['section_sha256']=oldsha
 mapping='old_section => whole pinned old addendum plus A90 table row; revision_pointer.document => exact prereg_revision pin; section hash => frozen A90 row pin'
 if case['scope']=='NECESSARY_RULE_PERMISSION_ONLY_NOT_COMPLETE_T1_ADMISSION':
  row=None;mapping+='; unchanged cited/table entry needs no duplicate disposition row, so valid unchanged T1 baseline is used'
 want='PASS' if case['expected_rule_result']=='ALLOW' else 'REFUSE'
 code='DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY' if case['id']=='PV_D05_1_plain_no_change' else None
 run('matrix/'+case['id'],op,np,row,want,code,docedit)
 MAPPINGS.append({'matrix_case':case['id'],'mapping':mapping,'actual_interface':'run(...,dispositions=(path,sha),text_of_record_addendum=PATH); prereg entries_after_A81.addendum_read.sha256_at_generation/bytes'})
# C01: cited A62 sits before the table, so only authenticated whole-addendum comparison can detect its change.
oldparts=copy.deepcopy(SECTIONS);newparts=copy.deepcopy(SECTIONS);newparts[62]=section(62,'changed scientific rule sixty two')
def after62():return {'entry':'A62','disposition':'no_change_after_change','section_sha256':h(newparts[62]),'changed_text':'changed scientific rule sixty two','why_no_prereg_effect':'Synthetic fixture only; no operative prereg effect.'}
run('C01/A62_changed_without_disposition',oldparts,newparts,want='REFUSE',code='ENTRY_SECTION_CHANGED')
run('C01/A62_plain_no_change',oldparts,newparts,{'entry':'A62','disposition':'no_change','section_sha256':h(newparts[62]),'reason':'no change'},'REFUSE','DISPOSITION_PLAIN_NO_CHANGE_ON_CHANGED_ENTRY')
run('C01/A62_exact_new_only',oldparts,newparts,after62())
r=after62();r['changed_text']='rule';run('C01/A62_old_common_excerpt',oldparts,newparts,r,'REFUSE','DISPOSITION_CHANGED_TEXT_IN_OLD_SECTION')
run('anchor/missing_old_argument',oldparts,newparts,after62(),'REFUSE','ADDENDUM_AT_TEXT_OF_RECORD_REQUIRED',oldarg=False)
run('anchor/wrong_old_digest',oldparts,newparts,after62(),'REFUSE','ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH',oldsha_override='0'*64)
run('anchor/missing_prereg_old_pin',oldparts,newparts,after62(),'REFUSE','ADDENDUM_READ_PIN_ABSENT',docedit=lambda d:d['entries_after_A81'].pop('addendum_read'))
run('anchor/wrong_old_bytes_count',oldparts,newparts,after62(),'REFUSE','ADDENDUM_AT_TEXT_OF_RECORD_MISMATCH',docedit=lambda d:d['entries_after_A81']['addendum_read'].update(bytes=1))
missing=copy.deepcopy(oldparts);missing.pop(62);run('anchor/cited_A62_absent_old',missing,newparts,after62(),'REFUSE','CITED_ENTRY_ABSENT_FROM_READ_COPY')
run('anchor/row_old_hash_inconsistent',oldparts,newparts,after62(),'REFUSE','ENTRY_TABLE_ROW_NOT_THE_TEXT_OF_RECORD',docedit=lambda d:d['entries_after_A81']['rows'][0].update(section_sha256='0'*64))
# Revision pointer authenticates exact bytes and must differ from current prereg by path and bytes.
revision=jp(OUT/'SYNTH_PREREG_REVISION.json',{'schema':'SYNTHETIC_PREREG_REVISION_NOT_AUTHORITY','entry':'A62','revised_text':'changed scientific rule sixty two'})
def revised(ref):return {'entry':'A62','disposition':'revised','prereg_revision':ref,'reason':'Synthetic pinned revision of A62.','section_sha256':h(newparts[62])}
run('revision/A62_valid_distinct',oldparts,newparts,revised(pin(revision)))
run('revision/stale_pin',oldparts,newparts,revised({'path':str(revision),'sha256':'0'*64}),'REFUSE','DISPOSITION_PREREG_REVISION_PIN')
run('revision/missing_file',oldparts,newparts,revised({'path':str(OUT/'ABSENT_REVISION.json'),'sha256':'0'*64}),'REFUSE','DISPOSITION_PREREG_REVISION_PIN')
run('revision/self_path',oldparts,newparts,want='REFUSE',code='DISPOSITION_PREREG_REVISION_IS_THE_PREREG',row_factory=lambda pp,d:revised(pin(pp)))
def clone(pp,d):return revised(pin(put(d/'SAME_BYTES_OTHER_PATH.json',pp.read_bytes())))
run('revision/self_bytes_other_path',oldparts,newparts,want='REFUSE',code='DISPOSITION_PREREG_REVISION_IS_THE_PREREG',row_factory=clone)
# Current contract authenticates a pointer by file bytes only; no claimed semantic proof that the file really revises the prereg.
opaque=put(OUT/'SYNTH_OPAQUE_REVISION.txt',b'inert non-JSON file\n')
rr,_,_=run('revision/opaque_bytes_observation',oldparts,newparts,revised(pin(opaque)))
LIMITATIONS=['Revision pointer code authenticates an existing exact file pin distinct from the current prereg; it does not parse revision semantics. The accepted opaque inert-file observation is recorded as this documented interface limit, not a new blocker without a stronger root schema ruling.','All results are provisional checked snapshot runtime with inert own fixtures; no final selected publication or actual scientific checks.']
assert NICE==10 and sys.flags.isolated==1 and sys.dont_write_bytecode and not DENIED
result={'date_u':DATE,'status':'TESTED_PROVISIONAL_0640_C01_RUNTIME','count':len(CHECKS),'passed':sum(x['passed'] for x in CHECKS),'checks':CHECKS,'matrix_bindings':MAPPINGS,'matrix':pin(mp),'snapshot_manifest':pin(SNAP/'SNAPSHOT_CX1V003.json'),'source_pins':manifest['sources'],'harness':pin(Path(__file__)),'fixtures':RUNS,'limitations':LIMITATIONS,'audit_denials':DENIED,'scope':'Actual snapshot common/T1 only. Twenty prepared cases mapped explicitly to actual whole-old-addendum and revision-file-pin interface, plus C01/anchor/revision negatives. No author source edits, mutable imports, production comparator, scientific processes, targets or protected run reads.'}
p=jp(OUT/'RESULTS_CX1V001.json',result);print(json.dumps({'result':pin(p),'passed':result['passed'],'count':result['count'],'failed':[x for x in CHECKS if not x['passed']],'limitations':LIMITATIONS},indent=1))
