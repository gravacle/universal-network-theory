"""Provisional immutable-snapshot review, exact inert D05/B8 controls; never real seal/science."""
from pathlib import Path
import ast,copy,hashlib,json,os,re,shlex,subprocess,sys,types
ROOT=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/review_seal_tools_v003_cx1')
SNAP=ROOT/'provisional_snapshot_v001';OUT=ROOT/'integration_controls_v001'
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
# Audited snapshots are compiled from their checked buffers and pre-registered in sys.modules.
C=load('seal_common_c4v003');T1=load('check_frozen_addendum_c4v003');T2=load('check_sealed_compare_c4v003');T3=load('check_slot_fill_c4v003');T4=load('build_seal_record_c4v003')
def xw(name,obj,raw=False):
 data=(obj.encode() if isinstance(obj,str) else obj) if raw else (json.dumps(obj,indent=1,sort_keys=True)+'\n').encode()
 return put(OUT/name,data)
def record(name,res,want='PASS',code=None):
 codes=[x['code'] for x in res.get('failures',[])];ck(name,res['verdict']==want and (code is None or any(code in c for c in codes)),{'actual':res['verdict'],'expected':want,'codes':codes});return res
frozen=xw('SYNTH_V005_ADDENDUM_FROZEN.md',''.join('## A%d: synthetic rule\nsynthetic rule %d\n'%(n,n) for n in range(82,103)),True)
dep=xw('SYNTH_DEPENDENCY.txt','SYNTHETIC INERT DEPENDENCY\n',True)
# Explicit synthetic API double. Production compare semantics are not exercised.
worker=xw('fixture/driver.py','# SYNTHETIC inert driver\n',True)
check=xw('fixture/CHECK.txt','SYNTHETIC inert check record\n',True)
cm=xw('fixture/CASCADE_MAP.json',{'synthetic':True})
compare_text='\n'.join(n+' = None' for n in C.PIN_NAMES)+'\nADDENDUM_V005_CITED = '+repr(str(frozen))+'\n'+'''
import json,hashlib
from pathlib import Path
SCHEMA_REPORT='SYNTHETIC_REPORT'
PRODUCTION_GAS_M_S_A57=128
NGC_GAS_M_S_A57=96
CASE_BLOCK_SCHEMA='SYNTHETIC_CASE_BLOCK'
GATE_SCHEMA='SYNTHETIC_GATE_RECORD'
ROUTE_A_MODES=('parallel8',)
ROUTE_A_MODE_DEFAULT='parallel8'
ACTIVE=None
EVENTS=[]
def load_driver_build_record(path,sha):
 b=Path(path).read_bytes()
 if hashlib.sha256(b).hexdigest()!=sha:raise SystemExit('synthetic hash')
 return json.loads(b),sha
def activate_driver_build(obj):
 global ACTIVE
 if obj.get('synthetic') is not True:raise SystemExit('synthetic invalid build')
 ACTIVE=obj;EVENTS.append('activate');return obj
def load_strict_file(path,label):return json.loads(Path(path).read_bytes())
def validate_case_block(cb,route_a_mode):
 EVENTS.append('validate')
 return [] if ACTIVE is not None and cb.get('schema')==CASE_BLOCK_SCHEMA and cb.get('synthetic_valid') is True and route_a_mode=='parallel8' else ['SYNTHETIC_CASE_BLOCK_INVALID']
def registered_gas_M_s(ctx):return ctx['case_block'].get('ddo_gas_M_s',128)
'''
compare=xw('fixture/SYNTH_COMPARE_API_DOUBLE.py',compare_text,True)
cb=xw('fixture/SYNTH_CASE_BLOCK.json',{'schema':'SYNTHETIC_CASE_BLOCK','synthetic_valid':True,'route_a_mode':'parallel8','ddo_gas_M_s':128,'key_equivalence_map':[]})
bld=xw('fixture/SYNTH_DRIVER_BUILD.json',{'synthetic':True,'build':'r5','driver':pin(worker),'cascade_map':pin(cm),'check_record':pin(check)})
cma=xw('fixture/CASCADE_MAP_R5_ADDENDUM_SYNTH.json',{'synthetic':True,'map':pin(cm)})
src=[xw('fixture/source_%02d.py'%i,'# synthetic inert source %d\n'%i,True) for i in range(15)]
allow={str(p):C.sha(p) for p in src}
tpl=xw('fixture/SYNTH_TEMPLATE.json',{'synthetic':True})
build=xw('fixture/BUILD_V007.md','# SYNTHETIC BUILD\n\n'+C.BUILD_HEADER+'\n\n'+''.join(h+'  '+p+'\n' for p,h in allow.items())+'\n## Synthetic template\n'+C.sha(tpl)+'  '+str(tpl)+'\n',True)
plan={'driver':pin(worker),'frozen_addendum':pin(frozen),'launcher':pin(src[0]),'guard':pin(src[1]),'template_pin':pin(tpl),'seal_binding_status':'BOUND_SYNTHETIC_INERT','calls':[{'spec':pin(dep)} for _ in range(10)]}
planf=xw('fixture/SYNTH_PLAN.json',plan)
cmd=xw('fixture/SYNTH_COMMAND.txt','# SYNTHETIC STRING NEVER EXECUTED\n'+shlex.join([C.PYTHON,'-I','-B',str(src[0]),str(planf),'--execute-root-only'])+'\n',True)
ids={k:pin(xw('fixture/IDENTITY_'+k+'.json',{'schema':'SYNTHETIC_GATE_RECORD','gate':g,'result_json_driver_sha256':C.sha(worker),'NEW_DRIVER_PIN':True})) for k,g in T3.IDENTITY_GATE_OF.items()}
certs={}
for k,g in T3.CERT_GATE_OF.items():
 o={'schema':'SYNTHETIC_GATE_RECORD','gate':g}
 if k=='LO':o['source_gas_M_s']=128
 if k=='GQ':o['rosters']=[{'roster':'DDO','M_s':128,'M_s_doubled':256}]
 if k=='DOUBLING':o['ddo_gas_M_s']=128
 certs[k]=pin(xw('fixture/CERT_'+k+'.json',o))
reg=xw('fixture/SYNTH_REGISTRY.json',{'gate_records':{}})
sl={'schema':T3.SCHEMA,'driver_branch':'r5','ngc_gas_M_s':96,'frozen_addendum':pin(frozen),'driver':pin(worker),'driver_build_record':pin(bld),'driver_check_record':pin(check),'compare_reviewed_source':pin(compare),'identity_comparator':pin(src[2]),'identity_gate_records':ids,'launch_packet':{'build':pin(build),'bound_plan':pin(planf),'bound_command':pin(cmd)},'certificates':certs,'producer_registry':pin(reg),'cache_directory_r6_only':T3.NOT_APPLICABLE_R5,'cascade_map_r5_addendum':pin(cma),'admission_entry':{'launcher':pin(src[0]),'guard':pin(src[1])}}
tr={'status':'SYNTHETIC ONLY: NOT AUTHORIZATION','binding_inputs':{'case_block':pin(cb)},'route_a_mode':'parallel8','seal_slots':{k:{'value':'PENDING_SYNTHETIC'} for k in T3.PREREG_SLOT_OF},'sources':['A82-A101'],'seal_record_requirements':[{'text':'Disclosure E5-08 synthetic-only fixture.'}]}
tr['seal_slots']['frozen_addendum']['path_to_be']=str(frozen)
tr['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']={'build':pin(build),'template_plan':pin(tpl)}
tr['entries_after_A81']={'rows':[{'entry':'A'+str(n),'decision':'NO_CHANGE','reason':'Synthetic no-change control for this fixture.','section_sha256':C.sha_bytes(v[0][1])} for n,v in T1.sections(frozen.read_bytes()).items() if n<=101]}

# Actual T3 and T4 use actual T1/T2; only the scientific comparator API is the clearly synthetic inert double above.
ss=xw('fixture/SYNTH_SLOTS.json',sl);tor=xw('fixture/SYNTH_TEXT_OF_RECORD.json',tr);sealed_prereg=copy.deepcopy(tr)
for pk,sk in T3.PREREG_SLOT_OF.items():sealed_prereg['seal_slots'][pk]['value']=copy.deepcopy(sl[sk])
sp=xw('fixture/SYNTH_PREREG.json',sealed_prereg)
exp=T2.expected_pins(sl,str(sp));sealed_text=compare_text
for n in C.PIN_NAMES:sealed_text=sealed_text.replace(n+' = None',n+' = '+repr(exp[n]),1)
sc=xw('fixture/SYNTH_SEALED_COMPARE.py',sealed_text,True)
disp_obj={'schema':C.DISPOSITIONS_SCHEMA,'frozen_addendum_sha256':C.sha(frozen),'entries':[{'entry':'A102','disposition':'no_change','reason':'A102 is a synthetic metadata-only addition; it does not revise the inert fixture rule.','section_sha256':C.sha_bytes(T1.sections(frozen.read_bytes())[102][0][1])}]}
disp_raw=(json.dumps(disp_obj,ensure_ascii=False,indent=3)+'\n').encode();dp=xw('fixture/SYNTH_DISPOSITIONS.json',disp_raw,True);disp=(str(dp),C.sha(dp))
def t3(d=disp):return T3.run(str(ss),str(sp),str(tor),str(frozen),(),str(compare),str(sc),C.sha(tor),d)
pos=record('integration/T3_complete_positive',t3())
expected={'pin':pin(dp),'content':disp_obj,'raw_text':disp_raw.decode()}
ck('integration/T3_exact_disposition_passthrough',pos.get('passthrough',{}).get('later_entry_dispositions')==expected)
base={'schema':'SYNTHETIC_REPORT_GATES_ONLY','blinded':True,'test_mode':False,'script_sha256':C.sha(sc),'route_a_mode':'parallel8','gates':{'B0':{'verdict':'PASS'}}}
gates=xw('build/GATES_ONLY.json',base);valid=copy.deepcopy(base);valid['schema']='SYNTHETIC_REPORT_VALIDITY_ONLY';valid.pop('gates');valid['cases']={'C5H':{'verdict':'PASS'}};validp=xw('build/VALIDITY_ONLY.json',valid)
km=xw('build/SYNTH_KEY_MAP.json',{'schema':T4.KEY_MAP_SCHEMA,'key_equivalence_map':[]})
impl=xw('build/SYNTH_IMPL.md','SYNTHETIC API '+C.sha(compare)+'\n',True)
ni=xw('build/SYNTH_NEW_ITEMS.json',{'schema':T4.NEW_ITEMS_SCHEMA,'compare_impl':pin(impl),'items':[]})
cu=xw('build/SYNTH_CUSTODY.json',{'schema':T4.CUSTODY_SCHEMA,'identity_run':'Z2','driver_sha256':C.sha(worker),'stages_total':1,'stages_successor':1,'verdict':'PASS','method':'SYNTHETIC ASSERTION ONLY; no stage executed'})
a=types.SimpleNamespace(slots=str(ss),prereg=str(sp),text_of_record=str(tor),text_of_record_sha=C.sha(tor),frozen=str(frozen),covered_later=[],dispositions=disp,reviewed=str(compare),sealed_compare=str(sc),gates_only_output=str(gates),validity_only_output=str(validp),key_equivalence_map=str(km),new_item_list=str(ni),successor_custody=str(cu),b2_record=None)
res,text=T4.safe_build(a);record('integration/T3_T4_returned_record_positive',res)
ck('integration/returned_text_exists',isinstance(text,str))
if text is not None:
 rec=json.loads(text);led=rec.get('later_entry_dispositions')
 ck('integration/record_exact_disposition',led==expected)
 ck('integration/record_exact_disposition_raw_bytes',led['raw_text'].encode()==disp_raw)
 ck('integration/record_disposition_hash_from_bytes',h(led['raw_text'].encode())==led['pin']['sha256']==disp[1])
 ck('integration/returned_record_hash',h(text.encode())==res['seal_record_sha256'])
 # Retain returned inert bytes as a clearly labelled fixture, never a real SEAL_RECORD or authority.
 returned=xw('RETURNED_SYNTHETIC_NOT_AUTHORITY.json',text,True)
else:returned=None
for name,mut,code in [('empty_reason',lambda o:o['entries'][0].update(reason=''),'DISPOSITION_REASON_EMPTY'),('wrong_section',lambda o:o['entries'][0].update(section_sha256='0'*64),'DISPOSITION_SECTION_SHA_MISMATCH')]:
 obj=copy.deepcopy(disp_obj);mut(obj);p=xw('mutations/'+name+'.json',obj);aa=copy.copy(a);aa.dispositions=(str(p),C.sha(p));rr,tt=T4.safe_build(aa);record('integration/'+name,rr,'REFUSE',code);ck('integration/'+name+'_no_record',tt is None)
aa=copy.copy(a);aa.dispositions=(str(dp),'0'*64);rr,tt=T4.safe_build(aa);record('integration/wrong_root_pin',rr,'REFUSE','DISPOSITIONS_PIN_MISMATCH');ck('integration/wrong_root_pin_no_record',tt is None)
# Mutate the bytes returned only at the builder's re-read, after T3/T1 passed the original exact buffer.
orig=Path.read_bytes
for name,changed in [('changed_object',b'{}\n'),('same_object_different_bytes',(json.dumps(disp_obj,sort_keys=True)+'\n').encode())]:
 reads=[0]
 try:
  def injection(self):
   if str(self)==str(dp):
    reads[0]+=1
    if reads[0]>=2:return changed
   return orig(self)
  Path.read_bytes=injection;rr,tt=T4.safe_build(a)
 finally:Path.read_bytes=orig
 record('integration/late_'+name,rr,'REFUSE','DISPOSITIONS_CHANGED_AFTER_CHECK');ck('integration/late_'+name+'_two_reads_no_record',reads[0]==2 and tt is None,reads[0])
ck('execution/nice10_isolated_no_bytecode',NICE==10 and sys.flags.isolated==1 and sys.dont_write_bytecode)
ck('execution/zero_audit_denials',not DENIED,DENIED)
result={'date_u':DATE,'status':'TESTED_PROVISIONAL_SYNTHETIC_FULL_T3_BUILDER_INTEGRATION','count':len(CHECKS),'passed':sum(x['passed'] for x in CHECKS),'checks':CHECKS,'source_pins':manifest['sources'],'snapshot_manifest':pin(SNAP/'SNAPSHOT_CX1V001.json'),'harness':pin(Path(__file__)),'returned_inert_record':pin(returned) if returned else None,'audit_denials':DENIED,'scope':'Actual immutable snapshot T1/T2/T3/T4 execution. Comparator is explicitly own synthetic API double; its scientific semantics and all production certificates/driver/launch behavior are UNTESTED. Full returned record is inert metadata under review only, never installed as authority. Exact disposition text/content/hash retained; T3 failures and post-check byte mutation suppress all record output. No actual C5H data, target, science or launch.'}
p=jp(OUT/'RESULTS_CX1V001.json',result);print(json.dumps({'result':pin(p),'passed':result['passed'],'count':result['count'],'failed':[x for x in CHECKS if not x['passed']]},indent=1))
