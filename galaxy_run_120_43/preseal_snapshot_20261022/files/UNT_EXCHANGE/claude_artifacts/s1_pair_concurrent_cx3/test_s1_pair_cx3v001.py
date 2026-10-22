"""Synthetic pair guard/binder/worker controls. No scientific code or real child starts.
Native policy/direct-context and fill replay are source-pinned synthetic fixtures.
Full real successor validate runs; only disk readings, process creation and clock waits use stubs.
"""
import ast,copy,contextlib,hashlib,io,json,os,signal,sys,types,traceback,datetime
from pathlib import Path
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2')
ART=BASE.parent
D=Path(sys.argv[1]);RUN=Path(sys.argv[2]);RUN.mkdir()
RESULTS=[];WRITES=0;DENIED=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):p=Path(p);return {'path':str(p),'sha256':sha(p.read_bytes())}
def wx(p,b):
 p=Path(p)
 with p.open('xb') as f:f.write(b)
 return pin(p)
def wj(p,j):return wx(p,(json.dumps(j,sort_keys=True,indent=1,allow_nan=False)+'\n').encode())
def newj(tag,j):
 global WRITES
 WRITES+=1;return wj(RUN/f'{tag}_{WRITES:04d}.json',j)
def load(p):
 p=Path(p);m=types.ModuleType(p.stem);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def audited(event,args):
 if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn','os.exec','socket.connect','socket.bind'):
  DENIED.append(event);raise RuntimeError('REAL PROCESS OR NETWORK BLOCKED')
 if event=='open' and isinstance(args[0],(str,bytes)):
  p=os.fsdecode(args[0])
  if p.startswith('/Volumes/') or '/runs_ext/' in p or '/.codex/' in p:
   DENIED.append(p);raise RuntimeError('PROTECTED READ BLOCKED')
sys.addaudithook(audited)
G0=load(BASE/'step4_guard_c2v014.py')
B=load(D/'step4_bind_c2v011_s1pair_cx3v001.py');G=B.G
GP=pin(D/'step4_guard_c2v014_s1pair_cx3v001.py');LP=pin(D/'step4_launcher_c2v015_s1pair_cx3v001.py')
MON=pin(ART/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py');DRV=pin(ART/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py')
assert MON['sha256']==G.MONITOR_SHA and DRV['sha256']==G.R5_SHA
CASES=list(G.S1_OVERLAP_CASES)
SOURCES_SRC={
'context':"def validate_block(x):\n    assert x['route_a']['column_workers']==1\nO=object()\n",
'direct':"""import copy
DIRECT_CONTEXT_API='UNT_STEP4_DIRECT_PREFLIGHT_CX1V001'
class Ctx:
 def __init__(self,config):self.config=config
 def certificate_policy_gate(self):return {'ok':True,'reasons':[]}
 def certificate_check(self,spec,phase):
  ok=spec['label']==self.config['expected_case']
  return {'ok':ok,'blockers':[] if ok else ['CASE_C1_MISMATCH']}
 def sensitivity_gate(self,spec):return {'ok':True,'reasons':[]}
 def prelaunch_check(self,spec):return copy.deepcopy(spec)
def build(C,config,guard=None,admission=None):return Ctx(config)
""",
'replay':"""import json,hashlib
from pathlib import Path
S1_REPLAY_API='UNT_S1_FILL_REPLAY_C2V002'
def guard_replay(ref):
 raw=Path(ref['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==ref['sha256']
 j=json.loads(raw);out={}
 for c,v in j['cases'].items():
  r=v['spec'];b=Path(r['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha256']
  out[c]={'spec':r,'bytes':b}
 return {'cases':out}
""",
'producer':'# synthetic producer; no science\n', 'custody':'# synthetic custody; no science\n','enumerator':'# synthetic enumerator; no science\n'}
MODS={n:wx(RUN/(n+'.py'),s.encode()) for n,s in SOURCES_SRC.items()}
B.REPLAY_PIN=MODS['replay'] # disclosed fixture only; production binder stays pinned to original S1 lib.
B.PACKET=RUN/'packet';B.PACKET.mkdir()
G.disk_admission=lambda plan,call=None:{'synthetic_disk':True}
V={}
for n in ('compare','addendum','case_block'):V[n]=newj(n,{'synthetic':n})
V['prereg']=newj('prereg',{'binding_inputs':{'case_block':V['case_block']}})
V['seal']=newj('seal',{'sealed_by':G.AUTHORITY,'prereg':V['prereg'],'compare':V['compare'],'driver':{'sha256':DRV['sha256']},'frozen_addendum':V['addendum']})
V['verdict']=newj('verdict',{'schema':'SYNTHETIC','test_mode':False,'decision':{'tests_read':True,'outcome':'ADOPT_TAIL'},'script_sha256':V['compare']['sha256'],'prereg':V['prereg'],'case_block':V['case_block']})
TUP=(V['compare']['sha256'],V['prereg']['sha256'],V['addendum']['sha256'],'SYNTHETIC',V['verdict']['sha256'])
POL=wx(RUN/'policy.py',("APPROVED_V007_SEALS="+repr({TUP})+"\ndef check_numerics(ncfg,block,n,**kw):\n    return ncfg,{'ok':True,'reasons':[]}\n").encode())
REG=newj('registry',{'schema':'SYNTHETIC','points':{}});REV=newj('policyreview',{'schema':'SYNTHETIC'})
CONFIGS={c:newj('c1_'+c,{'expected_case':c,'numerics':{'verdict_artifact':V['verdict'],'sealed_prereg':V['prereg'],'compare':V['compare'],'block':{'route_a':{'column_workers':1}}},'tail_readiness':{'certificate_registry':REG,'certificate_policy_review':REV,'custody_deriver':MODS['custody'],'state_enumerator':MODS['enumerator'],'approved_certificate_producers':[MODS['producer']]}}) for c in CASES}
SPECS={c:newj('spec_'+c,{'galaxy':'DDO154','admit':{},'label':c,'physical':{'distance_Mpc':4.04},'numerics':{'route_a':{'column_workers':1},'uv_tail':{'enabled':True}}}) for c in CASES}
FILL=newj('fill',{'schema':'SYNTHETIC_FILL','cases':{c:{'spec':SPECS[c]} for c in CASES}})
ORIGINAL_PINS=[pin(BASE/'step4_guard_c2v014.py'),pin(BASE/'step4_launcher_c2v015.py'),pin(BASE/'step4_bind_c2v011.py')]
orig_sources={p['path']:p['sha256'] for p in [ORIGINAL_PINS[0],ORIGINAL_PINS[1],MON,DRV,POL,*MODS.values()]}
parent_sources=dict(orig_sources,**{p['path']:p['sha256'] for p in [GP,LP,pin(D/'step4_bind_c2v011_s1pair_cx3v001.py')]})
def source_review(src):return newj('source_review',{'schema':'UNT_STEP4_SOURCE_REVIEW_CX1V001','status':'TESTED','verdict':'PASS','approved_sources':src,'blocking_findings':[],'reviewer':'SYNTHETIC_CLAUDE_REVIEW'})
O_REVIEW=source_review(orig_sources);P_REVIEW=source_review(parent_sources)
RULE={'max_active':1,'poll_seconds':60,'ramp':'previous_first_completed_route_a_iteration'}
OV={'schema':G.S1_OVERLAP_SCHEMA,'replay_module':MODS['replay'],'fill_record':FILL}
CAPS={'wall_cap_s':100800,'rss_cap_bytes':137438953472,'output_cap_bytes':85899345920}
NPAIR=0
def pair_fixture(inactive=False):
 global NPAIR
 NPAIR+=1;fd=RUN/f'fixture_{NPAIR:03d}';fd.mkdir();od=fd/'outputs';od.mkdir();children={};calls=[]
 for i,c in enumerate(CASES):
  partial={'schema':'UNT_STEP4_ADMISSION_CX1V001','authority':G.AUTHORITY,'status':'ROOT_AUTHORIZED','sources':orig_sources,'source_review':O_REVIEW,'v007':V,'adoption_policy':POL,'config':CONFIGS[c],'context_module':MODS['context'],'direct_context':MODS['direct'],'tail_off_policy':None}
  outdir=str(od/c)
  call={'case':c,'spec':SPECS[c],'driver':DRV,'spec_status':'ROOT_FINAL','pending':[],'distance_Mpc':4.04,'tail_on':True,'family':'S4_POST_S1','outdir':outdir,'receipt':outdir+'.receipt.json','monitor_log':outdir+'.monitor.log',**CAPS}
  pre=G0.native_preflight(partial,call);call['prelaunch']=newj('pre_'+c,pre);calls.append(call)
  op={'schema':'UNT_STEP4_LAUNCH_PLAN_CX1V001','binding_status':'ROOT_BOUND','batch':'POST_S1','guard':ORIGINAL_PINS[0],'launcher':ORIGINAL_PINS[1],'monitor':MON,'route_a_admission':RULE,'launcher_log':str(od/(c+'.launcher.log')),'calls':[call],'s1':{'fill_record':FILL,'theta_key':'a'*64,'k':3 if i==0 else 4,'branch':'SYNTHETIC','attempt':1}}
  pref=newj('parentplan_'+c,op)
  cfg=dict(partial,plan=pref,route_a_admission=RULE,core_priority=G.CORE_PRIORITY_INACTIVE if inactive else G.CORE_PRIORITY_S1_OVERLAP,case_order=[c],caps={c:CAPS},calls={c:{'spec':SPECS[c],'driver':DRV,'prelaunch':call['prelaunch']}},s1_overlap=OV)
  cref=newj('parentadmission_'+c,cfg);G0.validate(pref,ORIGINAL_PINS[1]['path'],config_ref=cref,disk_batch=False)
  children[c]=cref
 asm=B.assemble_pair(children,P_REVIEW,str(od/'pair.launcher.log'),B.PACKET/f'p{NPAIR}.json',B.PACKET/f'c{NPAIR}.json')
 bound=B.bind(asm['plan']['path'],asm['admission_candidate']['path'],B.PACKET/f'p{NPAIR}.bound.json',B.PACKET/f'a{NPAIR}.bound.json',B.PACKET/f'command{NPAIR}.sh')
 plan=json.loads(Path(bound['plan']['path']).read_bytes());cfg=json.loads(Path(bound['admission']['path']).read_bytes())
 return {'dir':fd,'plan':plan,'cfg':cfg,'bound':bound,'calls':calls,'children':children,'assembly':asm}
def check(name,fn):
 try:v=fn();RESULTS.append({'id':name,'status':'PASS','detail':v})
 except Exception as ex:RESULTS.append({'id':name,'status':'FAIL','detail':type(ex).__name__+': '+str(ex),'trace':traceback.format_exc()[-1800:]})
def require(v):assert v
def validate_obj(f,pm=None,cm=None):
 p=copy.deepcopy(f['plan']);c=copy.deepcopy(f['cfg'])
 if pm:pm(p)
 if cm:cm(c)
 raw=G.canonical(p);pr={'path':f['bound']['plan']['path'],'sha256':sha(raw)};c['plan']=pr
 return G.validate(pr,LP['path'],_candidate_config=c,_plan_bytes=raw,disk_batch=False)
def refused(f,pm=None,cm=None,contains=None):
 try:validate_obj(f,pm,cm)
 except Exception as e:
  if contains:assert contains in str(e),(contains,str(e))
  return str(e)
 raise AssertionError('unexpected admission')
f=pair_fixture()
check('full_guard_bind_both_separate_C1',lambda:require(validate_obj(f)[0]['calls']==f['calls']))
check('spec_driver_caps_outputs_preserved',lambda:require(all(f['plan']['calls'][i]==json.loads(Path(json.loads(Path(f['children'][c]['path']).read_bytes())['plan']['path']).read_bytes())['calls'][0] for i,c in enumerate(CASES))))
check('native_preflight_config_is_per_case',lambda:require(all(G.native_preflight(f['cfg'],c)['config']==CONFIGS[c['case']] for c in f['calls'])))
check('inactive_also_one_exact_pair',lambda:require(validate_obj(pair_fixture(True))[0]['batch']=='POST_S1'))
for batch in ('HEADLINE','DIII','SENS_LO','SENS_HI'):
 check('refuse_batch_'+batch,lambda batch=batch:refused(f,lambda p:p.update(batch=batch),contains='S1_PAIR_POST_S1_REQUIRED'))
for tag,fn in [('one',lambda p:p.update(calls=p['calls'][:1])),('three',lambda p:p['calls'].append(copy.deepcopy(p['calls'][1]))),('reverse',lambda p:p['calls'].reverse()),('duplicate',lambda p:p['calls'][1].update(case=CASES[0])),('foreign',lambda p:p['calls'][1].update(case='HEADLINE_TRIAL'))]:
 check('refuse_calls_'+tag,lambda fn=fn:refused(f,fn))
for maxa in (1,3,True):
 check('refuse_max_active_'+str(maxa),lambda maxa=maxa:refused(f,lambda p:p['route_a_admission'].update(max_active=maxa),lambda c:c['route_a_admission'].update(max_active=maxa)))
for key,v in [('poll_seconds',30),('ramp','none'),('minimum_free_percent',25)]:
 check('refuse_route_rule_'+key,lambda key=key,v=v:refused(f,lambda p:p['route_a_admission'].update({key:v}),lambda c:c['route_a_admission'].update({key:v})))
for k in G.CORE_PRIORITY_INACTIVE:
 if k=='campaign_inactive':continue
 check('refuse_core_'+k,lambda k=k:refused(f,cm=lambda c:c['core_priority'].update({k:False})))
check('refuse_parent_plan_admission_map',lambda:refused(f,lambda p:p['s1_pair_admissions'].pop(CASES[1]),contains='S1_PAIR_PLAN_ADMISSION_BINDING'))
check('refuse_child_byte_pin',lambda:refused(f,lambda p:p['s1_pair_admissions'][CASES[1]].update(sha256='0'*64),lambda c:c['s1_pair_admissions'][CASES[1]].update(sha256='0'*64)))
def altered_child(cas,fn):
 cfg=json.loads(Path(f['children'][cas]['path']).read_bytes());fn(cfg);return newj('child_mut',cfg)
def child_mutation(cas,fn):
 ref=altered_child(cas,fn)
 return refused(f,lambda p:p['s1_pair_admissions'].update({cas:ref}),lambda c:c['s1_pair_admissions'].update({cas:ref}))
for cas in CASES:
 for tag,fn in [('root',lambda c:c.update(status='NOT_AUTHORIZED')),('caps',lambda c:c['caps'][c['case_order'][0]].update(wall_cap_s=1)),('C1_swap',lambda c,cas=cas:c.update(config=CONFIGS[CASES[1-CASES.index(cas)]])),('source_review',lambda c:c.update(source_review=REV)),('fill',lambda c:c['s1_overlap'].update(fill_record=REG))]:
  check('refuse_'+cas+'_'+tag,lambda cas=cas,fn=fn:child_mutation(cas,fn))
check('refuse_tail_off',lambda:refused(f,lambda p:p['calls'][1].update(tail_on=False)))
check('refuse_driver',lambda:refused(f,lambda p:p['calls'][1]['driver'].update(sha256=G.REF_SHA)))
check('refuse_spec_swap',lambda:refused(f,lambda p:p['calls'][1].update(spec=p['calls'][0]['spec'])))
check('refuse_output_alias',lambda:refused(f,lambda p:p['calls'][1].update(outdir=p['calls'][0]['outdir'])))
check('refuse_parent_unreviewed',lambda:refused(f,cm=lambda c:c.update(source_review=REV)))
check('refuse_memory_binding',lambda:refused(f,cm=lambda c:c['route_a_admission'].update(source='/usr/bin/memory_pressure')))
def bind_existing():
 try:B.bind(f['assembly']['plan']['path'],f['assembly']['admission_candidate']['path'],Path(f['bound']['plan']['path']),B.PACKET/'unused_a.json',B.PACKET/'unused_cmd.sh')
 except G.Refusal as e:assert str(e)=='EXCLUSIVE_PACKET_OUTPUT_REQUIRED';return str(e)
 raise AssertionError('overwrite accepted')
check('binder_refuses_existing_output',bind_existing)
check('binder_command_BLAS_and_root_only',lambda:require('OPENBLAS_NUM_THREADS=1' in Path(f['bound']['command']['path']).read_text() and '--execute-root-only' in Path(f['bound']['command']['path']).read_text() and 'nice ' not in Path(f['bound']['command']['path']).read_text()))
def functions(p):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(Path(p).read_bytes()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
check('launcher_all_runtime_functions_unchanged',lambda:require(functions(LP['path'])==functions(BASE/'step4_launcher_c2v015.py')))
def guard_scope():
 a=functions(GP['path']);b=functions(BASE/'step4_guard_c2v014.py');diff=[k for k in b if a[k]!=b[k]]
 assert diff==['native_preflight','core_priority_admission'],diff
 assert set(a)-set(b)=={'pair_case_admission'}
 return diff
check('guard_function_diff_confinement',guard_scope)
check('binder_bind_function_unchanged',lambda:require(functions(D/'step4_bind_c2v011_s1pair_cx3v001.py')['bind']==functions(BASE/'step4_bind_c2v011.py')['bind']))
class FakeProc:
 def __init__(self,poll):self._poll=poll
 def poll(self):return self._poll()
def worker_scenario(tag,stop_first=False,wrong_c1_at_start=False):
 fx=pair_fixture();m=load(LP['path']);m.G.disk_admission=lambda p,call=None:{'synthetic_disk':True}
 m.LOCK=fx['dir']/'SYNTHETIC_LOCK';m.G.Refusal=G.Refusal
 clock=[0];running={};starts=[];reqs=[];polls=[];finished=[];overlap=[False]
 # Keep the real guard/native validation; its byte-bound fixture sources are read on every start/poll.
 def fake_popen(argv,**kw):
  reqs.append(argv)
  if argv[:3]==['/usr/bin/caffeinate','-i','-w']:return FakeProc(lambda:None)
  assert argv[:2]==['/usr/bin/caffeinate','-i'] and '--outdir' in argv
  od=argv[argv.index('--outdir')+1];call=next(c for c in fx['calls'] if c['outdir']==od)
  assert kw['pass_fds'] and kw['env']['OPENBLAS_NUM_THREADS']=='1'
  if running and any(v is None for v in running.values()):overlap[0]=True
  Path(od).mkdir();starts.append(call['case']);running[call['case']]=None
  return FakeProc(lambda:running[call['case']])
 def finish(c,status='FINISHED',rc=0):
  if status=='FINISHED':wx(Path(c['outdir'])/'progress.jsonl',b'{"stage":"route_a","event":"finished"}\n')
  wj(c['receipt'],{'status':status,'exit_code':rc});running[c['case']]=rc;finished.append(c['case'])
 def sleep(s):
  assert s==60;clock[0]+=1;polls.append(s)
  if clock[0]==1:
   if stop_first:finish(fx['calls'][0],'STOPPED_RSS_CAP',1)
   else:
    p=Path(fx['calls'][0]['outdir'])/'stages/01_route_a/attempt_000';p.mkdir(parents=True)
    wx(p/'progress.jsonl',b'{"stage":"iteration_completed","iteration":0}\n')
  elif clock[0]==2:finish(fx['calls'][0])
  elif clock[0]==3:finish(fx['calls'][1])
  assert clock[0]<8,'synthetic loop bound'
 m.subprocess=types.SimpleNamespace(Popen=fake_popen,run=lambda *a,**kw:types.SimpleNamespace(returncode=0),DEVNULL=-3,PIPE=-1,STDOUT=-2)
 m.time=types.SimpleNamespace(sleep=sleep)
 for k in m.BLAS:os.environ[k]='1'
 wx(fx['plan']['launcher_log'],b'')
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):rc=m.worker(fx['bound']['plan'])
 rows=[json.loads(s) for s in buf.getvalue().splitlines() if s.startswith('{')]
 if stop_first:
  assert starts==[CASES[0]] and rc==1 and not overlap[0]
 else:assert starts==CASES and rc==0 and overlap[0]
 assert rows[-1]['retry']=='NONE'
 return {'starts':starts,'concurrent':overlap[0],'exit':rc,'sleep_polls':len(polls),'guard_validate':'REAL; native contexts synthetic','requests_recorded':len(reqs),'processes_started':0}
check('worker_pair_overlaps_under_one_lock',lambda:worker_scenario('overlap'))
check('worker_systemic_failure_drains_no_second',lambda:worker_scenario('drain',True))
def same_lock_refuses():
 m=load(LP['path']);m.LOCK=RUN/'LOCK_CONTROL';fd=m.acquire_lock()
 try:
  try:m.acquire_lock()
  except m.G.Refusal as e:assert str(e)=='ANOTHER_STEP4_BATCH_ACTIVE';return str(e)
  raise AssertionError('lock did not refuse')
 finally:os.close(fd)
check('second_batch_lock_preserved',same_lock_refuses)
check('original_HEADLINE11_pins_unchanged',lambda:require(all(pin(p['path'])==p for p in ORIGINAL_PINS)))
check('no_process_network_or_volume_access',lambda:require(DENIED==[]))
rec={'date_u':datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),'status':'TESTED' if all(r['status']=='PASS' for r in RESULTS) else 'FAIL','n_total':len(RESULTS),'n_pass':sum(r['status']=='PASS' for r in RESULTS),'checks':RESULTS,'source_pins':[pin(__file__),GP,LP,pin(D/'step4_bind_c2v011_s1pair_cx3v001.py'),*ORIGINAL_PINS], 'substitutions':['Synthetic byte-pinned native policy/context/registry/certificates and fill replay; no real science.','Disk function returns synthetic metadata; no /Volumes open or statvfs.','Worker subprocess and clock stubs record requests; full actual guard validate remains live.','Binder PACKET is synthetic run/packet; REPLAY_PIN points to synthetic replay source.'],'production':'UNTESTED; root S1 dry preflight and Claude3 review required','audit_denied':DENIED}
wx(RUN/'TEST_RECORD.json',(json.dumps(rec,sort_keys=True,indent=2)+'\n').encode())
print(json.dumps({k:rec[k] for k in ('status','n_total','n_pass')}))
for r in RESULTS:
 if r['status']=='FAIL':print(json.dumps(r))
sys.exit(0 if rec['status']=='TESTED' else 1)
