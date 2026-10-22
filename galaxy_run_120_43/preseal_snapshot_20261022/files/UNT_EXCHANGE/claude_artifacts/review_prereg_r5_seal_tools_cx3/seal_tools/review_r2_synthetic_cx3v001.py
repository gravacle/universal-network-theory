from pathlib import Path
import hashlib,json,os,sys,copy,subprocess,resource,contextlib,io,shlex,types
E=Path(__file__).parent
S=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_final_prereg_c4/seal_tools_v002/r2')
O=E/'r2_synthetic_v001';O.mkdir(exist_ok=False)
date=subprocess.check_output(['date','-u'],text=True).strip()
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
expected={'seal_common_c4v002.py':'f41b0fca51a95387577839e52308a2dc6ccb79b1e6b9283f389b54c7f348dc10','check_frozen_addendum_c4v002.py':'06a98bc6b56e71bff450b749b12a7e8978824baeda41458e4319506a0cfd1891','check_sealed_compare_c4v002.py':'aebb7b731a800e558b13a5f290c7fac062183cb9ba092af45df4e6bda1f390cf','check_slot_fill_c4v002.py':'806733fb18e167275a1de62ebc9433fecf632cc16393933801fd4c9e53cddffb','build_seal_record_c4v002.py':'4192983d262e2a27a3d9c90681b6ee66a90c901bfe2f99a7dce2349bc8c5de52','print_driver_build_record_c4v002.py':'fde0b26e7ea26d4ad15213cc9c3115a807179616e0e155037c97d2179db7a673'}
pins=[pin(S/n) for n in expected]
for p in pins:assert p['sha256']==expected[Path(p['path']).name]
readme=pin(S.parent/'README_SEAL_TOOLS.md')
audit=[]
def hook(ev,args):
 if ev.startswith(('subprocess.','socket.','os.exec','os.spawn','os.posix_spawn','os.fork')) or ev in ('os.system','os.remove','os.rmdir','os.rename','os.link','os.symlink','shutil.rmtree'):
  audit.append(ev);raise PermissionError('INDEPENDENT_FENCE '+ev)
 if ev=='open' and not isinstance(args[0],int):
  p=Path(os.fsdecode(args[0])).resolve();m=args[1];f=args[2]
  wr=(isinstance(m,str) and any(x in m for x in 'wax+')) or (isinstance(f,int) and f&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if wr:
   if not p.is_relative_to(O) or not f&os.O_EXCL:audit.append('write '+str(p));raise PermissionError('EXCLUSIVE_SYNTHETIC_WRITES_ONLY')
  elif not(p.is_relative_to(O) or p.is_relative_to(S) or p.is_relative_to(Path(sys.base_prefix)) or p==Path(__file__)):
   audit.append('read '+str(p));raise PermissionError('OUTSIDE_SYNTHETIC_SOURCE_SCOPE')
 if ev=='os.mkdir' and not Path(args[0]).resolve().is_relative_to(O):audit.append(ev);raise PermissionError('MKDIR_OUTSIDE_SCOPE')
sys.addaudithook(hook)
sys.path.insert(0,str(S))
import seal_common_c4v002 as C
import check_frozen_addendum_c4v002 as T1
import check_sealed_compare_c4v002 as T2
import check_slot_fill_c4v002 as T3
import build_seal_record_c4v002 as T4
rows=[]
def xw(name,obj,raw=False):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True)
 b=(obj.encode() if isinstance(obj,str) else obj) if raw else (json.dumps(obj,indent=1,sort_keys=True)+'\n').encode()
 with p.open('xb') as f:f.write(b)
 return p
def record(name,r,want='PASS',code=None,scope='actual tool with synthetic records'):
 codes=[x['code'] for x in r.get('failures',[])]
 rows.append({'name':name,'expected':want,'observed':r['verdict'],'codes':codes,'passed':r['verdict']==want and (code is None or any(code in x for x in codes)),'scope':scope})
 return r
def test(name,ok,detail=None):rows.append({'name':name,'passed':bool(ok),'detail':detail})
frozen=xw('SYNTH_V005_ADDENDUM_FROZEN.md','## A82: synthetic entry\nSynthetic rule.\n\n## A83: synthetic next entry\nSynthetic second rule.\n',True)
dep=xw('SYNTH_DEPENDENCY.txt','SYNTHETIC INERT DEPENDENCY\n',True)
ref=xw('t2/SYNTH_REVIEWED.py','\n'.join(n+' = None' for n in C.PIN_NAMES)+'\nADDENDUM_V005_CITED = '+repr(str(frozen))+'\n',True)
s2={k:pin(dep) for k in ('frozen_addendum','driver_build_record','driver_check_record','producer_registry')}
s2.update(frozen_addendum=pin(frozen),compare_reviewed_source=pin(ref))
p2=xw('t2/SYNTH_PREREG.json',{'seal_slots':{'compare':{'value':pin(ref)}}})
exp=T2.expected_pins(s2,str(p2))
sc2=xw('t2/SYNTH_COMPARE.py','\n'.join(n+' = '+repr(exp[n]) for n in C.PIN_NAMES)+'\nADDENDUM_V005_CITED = '+repr(str(frozen))+'\n',True)
def t2probe(name,s,p=p2,want='REFUSE'):
 f=xw('t2/SLOTS_%03d.json'%len(rows),s)
 record('D07/'+name,T2.run(str(ref),str(sc2),str(f),str(p)),want)
 if want=='REFUSE':
  out=io.StringIO()
  with contextlib.redirect_stdout(out):rc=T2.main(['--reviewed',str(ref),'--sealed',str(sc2),'--slots',str(f),'--prereg',str(p)])
  test('D07CLI/'+name,rc==2 and json.loads(out.getvalue())['verdict']=='REFUSE')
t2probe('valid',s2,want='PASS')
for k in s2:
 for name,bad in [('PENDING','PENDING'),('null',None),('list',[]),('wrongdict',{'wrong':1}),('wrongtypes',{'path':5,'sha256':[]})]:
  s=copy.deepcopy(s2);s[k]=bad;t2probe(k+'/'+name,s)
for name,bad in [('null',None),('list',[]),('string','PENDING')]:
 t2probe('top_slots/'+name,bad)
 t2probe('top_prereg/'+name,s2,xw('t2/BAD_PREREG_'+name+'.json',bad))
msc=[('alias128','DOUBLING',{'ddo_gas_M_s':128},True),('alias64','DOUBLING',{'ddo_gas_M_s':64},False),('bool','DOUBLING',{'ddo_gas_M_s':True},False),('conflict','DOUBLING',{'ddo_gas_M_s':128,'gas_M_s':64},False),('absent','DOUBLING',{},False),('optional_NGC','DOUBLING',{'ddo_gas_M_s':128,'NGC':{}},True),('NGC96','DOUBLING',{'ddo_gas_M_s':128,'ngc_gas_M_s':96},True),('NGC64','DOUBLING',{'ddo_gas_M_s':128,'ngc_gas_M_s':64},False),('LOecho','LO',{'source_gas_M_s':128,'gas_M_s':128,'tail_config_gas':{'M_s':128}},True),('LOconflict','LO',{'source_gas_M_s':128,'gas_M_s':64},False),('GQ','GQ',{'rosters':[{'roster':'DDO','M_s':128,'M_s_doubled':256},{'roster':'NGC_T120L','M_s':96,'M_s_doubled':192}]},True),('GQwrongdouble','GQ',{'rosters':[{'roster':'DDO','M_s':128,'M_s_doubled':128}]},False),('ambiguous','DOUBLING',{'ddo_gas_M_s':128,'DDO_NGC_M_s':128},False)]
for name,k,obj,good in msc:
 c=C.Checker('synthetic');T3.certificate_ms_codes(c,k,obj,128,96);record('D01/'+name,c.result(),'PASS' if good else 'REFUSE')
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
tr={'status':'SYNTHETIC ONLY: NOT AUTHORIZATION','binding_inputs':{'case_block':pin(cb)},'route_a_mode':'parallel8','seal_slots':{k:{'value':'PENDING_SYNTHETIC'} for k in T3.PREREG_SLOT_OF},'sources':['A82','A83'],'seal_record_requirements':[{'text':'Disclosure E5-08 synthetic-only fixture.'}]}
tr['seal_slots']['frozen_addendum']['path_to_be']=str(frozen)
tr['seal_slots']['launch_packet']['named_candidates_verified_from_bytes']={'build':pin(build),'template_plan':pin(tpl)}
tr['entries_after_A81']={'rows':[{'entry':'A'+str(n),'decision':'NO_CHANGE','reason':'Synthetic no-change control for this fixture.','section_sha256':C.sha_bytes(v[0][1])} for n,v in T1.sections(frozen.read_bytes()).items()]}
def chain(name,s=None,t=None,edit=None,arg='bytes',want='PASS',code=None):
 s=copy.deepcopy(sl if s is None else s);t=copy.deepcopy(tr if t is None else t)
 tor=xw('chains/'+name+'/SYNTH_TEXT.json',t);p=copy.deepcopy(t)
 for pk,sk in T3.PREREG_SLOT_OF.items():p['seal_slots'][pk]['value']=copy.deepcopy(s[sk])
 if edit:edit(p)
 sp=xw('chains/'+name+'/SYNTH_PREREG.json',p);ss=xw('chains/'+name+'/SYNTH_SLOTS.json',s)
 r=T3.run(str(ss),str(sp),str(tor),text_of_record_sha=C.sha(tor) if arg=='bytes' else arg)
 record('T3/'+name,r,want,code,'actual T3; explicit synthetic compare API double')
 return ss,sp,tor,r
ss,sp,tor,pos=chain('positive')
for k,v in [('case_block',pin(cb)),('cascade_map_r5_addendum',pin(cma)),('admission_entry',sl['admission_entry'])]:test('T3/passthrough/'+k,pos.get('passthrough',{}).get(k)==v)
M=C.load_reviewed_compare(str(compare),C.sha(compare));test('T3/activate before validate',M.EVENTS==['activate','validate'],M.EVENTS[:])
for name,mut,code in [('missing_case_block',lambda x:x.pop('binding_inputs'),'CASE_BLOCK_PIN_ABSENT'),('bad_case_block_shape',lambda x:x['binding_inputs'].update(case_block='PENDING'),'CASE_BLOCK_PIN_SHAPE'),('stale_case_block',lambda x:x['binding_inputs']['case_block'].update(sha256='0'*64),'PIN_BYTES_MISMATCH'),('wrong_frozen_path',lambda x:x['seal_slots']['frozen_addendum'].update(path_to_be=str(dep)),'FROZEN_SLOT_NOT_PATH_TO_BE'),('route_conflict',lambda x:x.update(route_a_mode='wrong'),'ROUTE_A_MODE_SOURCES_DIFFER'),('wrong_named_build',lambda x:x['seal_slots']['launch_packet']['named_candidates_verified_from_bytes'].update(build=pin(dep)),'BUILD_NOT_BUILD_V007'),('wrong_named_template',lambda x:x['seal_slots']['launch_packet']['named_candidates_verified_from_bytes'].update(template_plan=pin(dep)),'PLAN_TEMPLATE_NOT_THE_PREREG_NAMED_TEMPLATE')]:
 t=copy.deepcopy(tr);mut(t);chain(name,t=t,want='REFUSE',code=code)
for name,mut,code in [('missing_cascade',lambda x:x.update(cascade_map_r5_addendum='NOT_APPLICABLE_R6'),'CASCADE_MAP_R5_ADDENDUM_REQUIRED_UNDER_R5'),('stale_cascade',lambda x:x['cascade_map_r5_addendum'].update(sha256='0'*64),'PIN_BYTES_MISMATCH'),('wrong_launcher',lambda x:x['admission_entry'].update(launcher=pin(src[2])),'ADMISSION_ENTRY_NOT_THE_PLAN'),('wrong_guard',lambda x:x['admission_entry'].update(guard=pin(src[2])),'ADMISSION_ENTRY_NOT_THE_PLAN'),('stale_build',lambda x:x['driver_build_record'].update(sha256='0'*64),'PIN_BYTES_MISMATCH'),('stale_check',lambda x:x['driver_check_record'].update(sha256='0'*64),'PIN_BYTES_MISMATCH')]:
 s=copy.deepcopy(sl);mut(s);chain(name,s=s,want='REFUSE',code=code)
chain('text_change',edit=lambda x:x.update(status='DIFFERENT'),want='REFUSE',code='SEALED_PREREG_TEXT_CHANGED')
chain('arg_missing',arg=None,want='REFUSE',code='TEXT_OF_RECORD_PIN_PENDING')
chain('arg_wrong',arg='0'*64,want='REFUSE',code='TEXT_OF_RECORD_SHA_ARG_MISMATCH')
for name,data in [('duplicate_huge',b'{"n":'+b'9'*5000+b',"dup":1,"dup":2}'),('nonfinite',b'{"x":NaN}'),('invalid_utf8',b'\xff')]:
 p=xw('mutations/check_'+name+'.json',data,True);s=copy.deepcopy(sl);s['driver_check_record']=pin(p)
 b=json.loads(bld.read_bytes());b['check_record']=pin(p);s['driver_build_record']=pin(xw('mutations/check_'+name+'_BUILD.json',b))
 chain('check_'+name,s=s,want='REFUSE',code='DRIVER_CHECK_RECORD_JSON_DEFECT')
for name,data in [('duplicate_huge',b'{"n":'+b'9'*5000+b',"map":"'+C.sha(cm).encode()+b'","dup":1,"dup":2}'),('duplicate',b'{"map":"'+C.sha(cm).encode()+b'","dup":1,"dup":2}'),('nonfinite',b'{"map":"'+C.sha(cm).encode()+b'","x":NaN}')]:
 p=xw('mutations/CASCADE_MAP_R5_ADDENDUM_'+name+'.json',data,True);s=copy.deepcopy(sl);s['cascade_map_r5_addendum']=pin(p)
 chain('cascade_'+name,s=s,want='REFUSE',code='CASCADE_MAP_R5_ADDENDUM_JSON')
base={'schema':'SYNTHETIC_REPORT_GATES_ONLY','blinded':True,'test_mode':False,'script_sha256':C.sha(compare),'route_a_mode':'parallel8','gates':{'B0':{'verdict':'PASS'}}}
for name,mut,code in [('positive',lambda x:None,None),('wrong_schema',lambda x:x.update(schema='wrong'),'E_SEAL1_SCHEMA'),('not_blinded',lambda x:x.update(blinded=False),'E_SEAL1_NOT_BLINDED'),('test_mode',lambda x:x.update(test_mode=True),'E_SEAL1_TEST_MODE'),('wrong_script',lambda x:x.update(script_sha256='0'*64),'E_SEAL1_SCRIPT_NOT_THE_SEALED_COMPARE'),('wrong_mode',lambda x:x.update(route_a_mode='wrong'),'E_SEAL1_ROUTE_A_MODE'),('numeric',lambda x:x.update(value=3),'E_SEAL1_OUTPUT_VALUE_BEARING'),('numeric_string',lambda x:x.update(value='3.14159'),'E_SEAL1_OUTPUT_VALUE_BEARING'),('empty_gates',lambda x:x.update(gates={}),'E_SEAL1_GATES_SHAPE')]:
 b=copy.deepcopy(base);mut(b);p=xw('b6/'+name+'/GATES_ONLY.json',b);c=C.Checker('b6');T4.b6_codes(c,'gates',str(p),'GATES_ONLY.json','_GATES_ONLY','SYNTHETIC_REPORT',C.sha(compare),'parallel8');record('B6/'+name,c.result(),'PASS' if code is None else 'REFUSE',code)
exp=T2.expected_pins(sl,str(sp));txt=compare_text
for n in C.PIN_NAMES:txt=txt.replace(n+' = None',n+' = '+repr(exp[n]),1)
sc=xw('fixture/SYNTH_SEALED_COMPARE.py',txt,True)
g=dict(base,script_sha256=C.sha(sc));gates=xw('build/GATES_ONLY.json',g)
v=dict(g,schema='SYNTHETIC_REPORT_VALIDITY_ONLY',cases={'C5H':{'verdict':'PASS'}});v.pop('gates');valid=xw('build/VALIDITY_ONLY.json',v)
km=xw('build/SYNTH_KEY_MAP.json',{'schema':T4.KEY_MAP_SCHEMA,'key_equivalence_map':[]})
impl=xw('build/SYNTH_IMPL.md','SYNTHETIC API '+C.sha(compare)+'\n',True)
ni=xw('build/SYNTH_NEW_ITEMS.json',{'schema':T4.NEW_ITEMS_SCHEMA,'compare_impl':pin(impl),'items':[]})
cu=xw('build/SYNTH_CUSTODY.json',{'schema':T4.CUSTODY_SCHEMA,'identity_run':'Z2','driver_sha256':C.sha(worker),'stages_total':1,'stages_successor':1,'verdict':'PASS','method':'SYNTHETIC ASSERTION ONLY; no stage executed'})
a=types.SimpleNamespace(slots=str(ss),prereg=str(sp),text_of_record=str(tor),text_of_record_sha=C.sha(tor),frozen=str(frozen),covered_later=[],reviewed=str(compare),sealed_compare=str(sc),gates_only_output=str(gates),validity_only_output=str(valid),key_equivalence_map=str(km),new_item_list=str(ni),successor_custody=str(cu),b2_record=None)
r,bt=T4.safe_build(a);record('T4/returned record positive',r,scope='actual T1/2/3/4; synthetic compare API double; record never installed')
findings=[]
if bt:
 rec=json.loads(bt)
 for k,v in [('case_block',pin(cb)),('cascade_map_r5_addendum',pin(cma)),('launch_entry',sl['admission_entry']),('build',pin(build)),('admission_allowlist',allow)]:test('T4/passthrough/'+k,rec.get(k)==v)
 test('T4/root argument',rec.get('text_of_record_pinned_by')=='ROOT_ARGUMENT')
 def adm(name,seal,mut=None,want='PASS',code=None):
  rp=xw('admission/'+name+'/SYNTH_INERT_RECORD.json',seal)
  cfg={'schema':C.ADMISSION_SCHEMA,'authority':dict(C.AUTHORITY),'seal':pin(rp),'prereg':pin(sp),'compare':pin(sc),'build':pin(build),'producer_allowlist':dict(allow),'note':'SYNTHETIC INERT: NOT AUTHORIZATION'}
  if mut:mut(cfg)
  cp=xw('admission/'+name+'/SYNTH_INERT_CONFIG.json',cfg);return record('B8/'+name,T4.check_admission_config(str(cp),str(rp)),want,code)
 adm('positive',rec)
 adm('wrong_authority',rec,lambda x:x.update(authority={'identity':'wrong'}),'REFUSE','ADMISSION_CONFIG_AUTHORITY')
 adm('missing_allowlist',rec,lambda x:x['producer_allowlist'].pop(str(src[0])),'REFUSE','ADMISSION_ALLOWLIST_COUNT_NOT_15')
 adm('wrong_compare',rec,lambda x:x.update(compare=pin(dep)),'REFUSE','ADMISSION_CONFIG_PREREG_COMPARE')
 for name,mut in [('wrong_sealed_by',lambda x:x.update(sealed_by={'identity':'wrong'})),('missing_sealed_by',lambda x:x.pop('sealed_by')),('malformed_driver',lambda x:x.update(driver='PENDING')),('stale_driver',lambda x:x['driver'].update(sha256='0'*64)),('malformed_frozen',lambda x:x.update(frozen_addendum=[])),('stale_frozen',lambda x:x['frozen_addendum'].update(sha256='0'*64))]:
  q=copy.deepcopy(rec);mut(q);rr=adm(name,q)
  findings.append({'case':name,'observed':rr['verdict'],'guard_expected':'REFUSE by source inference; guard not invoked','classification':'readiness checker mismatch, no launch bypass','codes':[x['code'] for x in rr['failures']]})
for p in pins:assert pin(p['path'])==p
assert not audit
result={'date_u':date,'status':'TESTED_BOUNDED_SYNTHETIC','source_pins':pins,'readme_selection_pin':readme,'harness':pin(__file__),'count':len(rows),'passed':sum(x['passed'] for x in rows),'checks':rows,'findings':findings,'audit_denials':audit,'max_rss_bytes_darwin':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'No actual seal, admission, binder, receipt or launch. Actual T2/T3/T4 tools with own inert synthetic metadata. Full T3/T4 uses explicitly synthetic compare API double: production compare scientific semantics UNTESTED. No author harness executed. Six B8 PASS counterexamples are successful reproductions, not contract passes.'}
p=xw('RESULTS_CX3V001.json',result)
print(json.dumps({'result':pin(p),'passed':result['passed'],'count':result['count'],'failed':[x for x in rows if not x['passed']],'findings':findings,'rss':result['max_rss_bytes_darwin'],'audit_denials':audit},indent=1))
