"""Synthetic real-replay integration: actual S1 filler/replayer, KS5 and b1 policy paths.
Inherits disclosed identity normalization and custody-result seam from the reviewed S1 suite.
No driver, observed data, science stage, real monitor, process, or volume read.
"""
import copy,datetime,hashlib,json,os,sys,types,traceback
from pathlib import Path
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/s1_successors_c2')
D=Path(sys.argv[1]);RUN=Path(sys.argv[2]);RUN.mkdir()
OPENED={};DENIED=[]
def audit(event,args):
 if event in ('subprocess.Popen','os.fork','os.forkpty','os.posix_spawn','os.system','os.exec','socket.connect','socket.bind'):
  DENIED.append(event);raise PermissionError('process or network blocked')
 if event=='open' and isinstance(args[0],(str,bytes)):
  p=os.fsdecode(args[0]);writing=isinstance(args[1],str) and any(c in args[1] for c in 'wax+')
  if p.startswith('/Volumes/') or '/runs_ext/' in p or '/.codex/' in p:
   DENIED.append(p);raise PermissionError('protected path blocked')
  if p.startswith('/Users/bgm/Research/') and not writing:OPENED[p]=True
sys.addaudithook(audit)
def pin(p):p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):
 p=Path(p);m=types.ModuleType(p.stem);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
T=load(BASE/'test_s1_path_c2v002c.py');T.RUN=RUN
T.L,_=T.load_lib();L=T.L;T.REAL_V6_PATH=L.V6_PATH
checks=[]
try:
 fx=T.build_fixtures();T.FX=fx
 base=L.strict_json(L.verify_pin(fx.base['off']))
 W4=T.dec_world('pair4',L.point_identity(base),4,T.B1_SHA,L.const_pin('KS1_PREDECESSOR'),L.const_pin('G6C'),[L.const_pin('G4'),L.const_pin('G3_PRODUCER'),L.const_pin('G1')])
 base['numerics']['uv_tail'].update(W4['slots'])
 br=T.wbytes(RUN/'pair_base4.spec.json',L.spec_bytes(base))
 pending,_,_=L.build_case(base,br['sha256'],L.theta_key(fx.off),L.S1_C3T,L.load_static(),None)
 W3=T.dec_world('pair3',L.point_identity(pending),3,L.PINS['KS5'][1],L.const_pin('KS1'),L.const_pin('G6C'),[L.const_pin('G4'),L.const_pin('G3_PRODUCER'),L.const_pin('G1')])
 filldir=RUN/'pair_fill';filldir.mkdir()
 fill=L.fill(fx.ua['off'],br,T.CFG_PIN,c3t_registry=W3['reg'],out_dir=str(filldir))
 replay=L.guard_replay(fill['record'])
 assert set(replay['cases'])==set(L.S1_CASES)
 checks.append({'id':'real_fill_and_replay_both_cases','status':'PASS'})
 childs={};singles={};worlds={L.S1_C3T:W3,L.S1_C4T:W4}
 for case in L.S1_CASES:
  nb=copy.deepcopy(base);nb['numerics']['uv_tail'].update(worlds[case]['slots']);ad=T.dec_adapter('pair_'+case,nb)
  cfg=T.dec_cfg(worlds[case],ad)
  res,pre,inner,opened,procs=T.preflight(cfg,case,fill['cases'][case]['spec'])
  assert res=='PASS',(case,res,inner)
  assert all(g['ok'] is True for g in inner['gates']) and not procs
  pr=T.wjson(RUN/(case+'_preflight.json'),pre)
  child=T.dec_admission('pair_'+case,fill['record'],case,pr,worlds[case],ad)
  fx.G.validate(child['plan'],L.PINS['LAUNCHER'][0],config_ref=child['admission'],disk_batch=False)
  childs[case]=child['admission'];singles[case]=child
  checks.append({'id':'real_native_'+case,'status':'PASS','gate_count':len(inner['gates']),'custody_derivers':[s['deriver_sha256'] for s in inner['seen']]})
 B=load(D/'step4_bind_c2v011_s1pair_cx3v001.py');G=B.G
 B.PACKET=RUN/'pair_packet';B.PACKET.mkdir();G.disk_admission=lambda p,call=None:{'synthetic_disk':True}
 sources={}
 for ref in childs.values():
  c=G.doc(ref)
  for p,h in c['sources'].items():assert p not in sources or sources[p]==h;sources[p]=h
 for p in (D/'step4_guard_c2v014_s1pair_cx3v001.py',D/'step4_launcher_c2v015_s1pair_cx3v001.py',D/'step4_bind_c2v011_s1pair_cx3v001.py',BASE/'s1_path_lib_c2v002c.py'):
  r=pin(p);sources[r['path']]=r['sha256']
 review=T.wjson(RUN/'pair_source_review.json',{'schema':'UNT_STEP4_SOURCE_REVIEW_CX1V001','status':'TESTED','verdict':'PASS','approved_sources':sources,'blocking_findings':[],'reviewer':'SYNTHETIC_DISTINCT_REVIEWER'})
 asm=B.assemble_pair(childs,review,str(RUN/'pair_launcher.log'),B.PACKET/'PLAN.json',B.PACKET/'CANDIDATE.json')
 bound=B.bind(asm['plan']['path'],asm['admission_candidate']['path'],B.PACKET/'BOUND_PLAN.json',B.PACKET/'BOUND_ADMISSION.json',B.PACKET/'COMMAND.sh')
 plan,cfg=G.validate(bound['plan'],str(D/'step4_launcher_c2v015_s1pair_cx3v001.py'),config_ref=bound['admission'],disk_batch=False)
 assert [c['case'] for c in plan['calls']]==list(L.S1_CASES)
 for c in plan['calls']:
  old=singles[c['case']]['plan_doc']['calls'][0];assert c==old
  assert G.native_preflight(cfg,c)==G.doc(c['prelaunch'])
 checks.append({'id':'pair_assemble_bind_real_KS5_and_b1_native','status':'PASS','unchanged_call_bytes':True,'replay_module':B.REPLAY_PIN,'config_by_case':{c:G.doc(r)['config'] for c,r in childs.items()}})
 # Distinct native C1 controls: retain C3's original preflight but swap to the b1 context and vice versa.
 for c in plan['calls']:
  wrong=copy.deepcopy(G.pair_case_admission(cfg,c));wrong['config']=worlds[L.S1_C4T if c['case']==L.S1_C3T else L.S1_C3T]['c1']
  try:fx.G.native_preflight(wrong,c)
  except Exception as e:checks.append({'id':'real_swapped_C1_refused_'+c['case'],'status':'PASS','refusal':str(e)})
  else:raise AssertionError('swapped C1 admitted')

 W=load(D/'s1_pair_root_cx3v002.py');W.modules=lambda:(G,L)
 L._process_table=lambda:'' # synthetic process-table metadata; no ps call
 rootcfg=T.wjson(RUN/'root_launch_cfg.json',{'schema':L.SCHEMA_LAUNCH_CFG,'campaign_state':'INACTIVE','step2_route_a_state':'INACTIVE'})
 def rootdry(lcfg=rootcfg,reg=None,record=None):
  return W.run(bound['plan'],bound['admission'],reg or fx.reg,fx.v6,lcfg,record_path=record)
 out=rootdry(record=str(RUN/'root_dry_record.json'));assert out['decision']=='ADMITTED',out
 checks.append({'id':'root_wrapper_real_pair_DRY','status':'PASS','checks':out['checks']})
 for tag,conf in [('step2',{'schema':L.SCHEMA_LAUNCH_CFG,'campaign_state':'INACTIVE','step2_route_a_state':'ACTIVE'}),('state_mismatch',{'schema':L.SCHEMA_LAUNCH_CFG,'campaign_state':'ACTIVE','step2_route_a_state':'INACTIVE'})]:
  rr=T.wjson(RUN/('root_bad_'+tag+'.json'),conf);o=rootdry(rr);assert o['decision']=='REFUSED',o
  checks.append({'id':'root_wrapper_refuse_'+tag,'status':'PASS','refusal':o['refusal']})
 badreg=dict(fx.reg,sha256='0'*64);o=rootdry(reg=badreg);assert o['decision']=='REFUSED'
 checks.append({'id':'root_wrapper_refuse_registration','status':'PASS','refusal':o['refusal']})
 o=W.run(bound['plan'],bound['admission'],fx.reg,fx.v6,rootcfg,mode='launch',record_path=str(RUN/'missing_confirm.json'))
 assert o['decision']=='REFUSED' and 'LAUNCH_CONFIRMATION_REQUIRED' in str(o['refusal'])
 checks.append({'id':'root_wrapper_refuse_unconfirmed_launch','status':'PASS'})
 original_trees=L.campaign_route_a_trees;L.campaign_route_a_trees=lambda text,own:[{'monitor_pid':123,'outdir':'SYNTHETIC_ACTIVE'}]
 o=rootdry();assert o['decision']=='REFUSED' and 'S1_CAMPAIGN_ROUTE_A_TREE' in str(o['refusal']);L.campaign_route_a_trees=original_trees
 checks.append({'id':'root_wrapper_refuse_active_tree_when_inactive','status':'PASS'})
 # Re-authorize the same synthetic child calls as campaign ACTIVE; no spec or caps change.
 active_children={}
 for c,ref in childs.items():
  child=G.doc(ref);child['core_priority']=G.CORE_PRIORITY_S1_OVERLAP;child['s1_overlap']=cfg['s1_overlap']
  active_children[c]=T.wjson(RUN/(c+'_active_admission.json'),child)
 active_asm=B.assemble_pair(active_children,review,str(RUN/'active_launcher.log'),B.PACKET/'ACTIVE_PLAN.json',B.PACKET/'ACTIVE_CANDIDATE.json')
 active=B.bind(active_asm['plan']['path'],active_asm['admission_candidate']['path'],B.PACKET/'ACTIVE_BOUND_PLAN.json',B.PACKET/'ACTIVE_BOUND_ADMISSION.json',B.PACKET/'ACTIVE_COMMAND.sh')
 acfg=T.wjson(RUN/'root_active_cfg.json',{'schema':L.SCHEMA_LAUNCH_CFG,'campaign_state':'ACTIVE','step2_route_a_state':'INACTIVE'})
 o=W.run(active['plan'],active['admission'],fx.reg,fx.v6,acfg)
 assert o['decision']=='ADMITTED',o
 checks.append({'id':'root_wrapper_active_no_C14_window','status':'PASS'})
 # Simulated launch branch only: stub never creates a process. Receipt-writing failure must not erase LAUNCHED.
 os.environ['UNT_STEP4_ADMISSION_PATH']=bound['admission']['path'];os.environ['UNT_STEP4_ADMISSION_SHA256']=bound['admission']['sha256']
 requests=[]
 def stub_spawn(argv,**kw):
  requests.append(argv);return types.SimpleNamespace(returncode=0,stdout='SYNTHETIC_STARTER_RETURN',stderr='')
 W.subprocess=types.SimpleNamespace(run=stub_spawn,DEVNULL=-3)
 original_write=L.write_exclusive
 def fail_outcome(path,data):
  if path.endswith('.outcome.json'):raise OSError('SYNTHETIC_DISK_FAILURE')
  return original_write(path,data)
 L.write_exclusive=fail_outcome
 o=W.run(bound['plan'],bound['admission'],fx.reg,fx.v6,rootcfg,mode='launch',confirm=bound['plan']['sha256'],record_path=str(RUN/'simulated_root_record.json'))
 L.write_exclusive=original_write
 assert o['decision']=='LAUNCHED' and 'SYNTHETIC_DISK_FAILURE' in o['outcome_record_error'] and len(requests)==1,o
 checks.append({'id':'root_wrapper_simulated_outcome_failure_preserves_launch_state','status':'PASS','real_processes':0})
 # Existing prelaunch record refuses before even the process stub is called.
 o=W.run(bound['plan'],bound['admission'],fx.reg,fx.v6,rootcfg,mode='launch',confirm=bound['plan']['sha256'],record_path=str(RUN/'simulated_root_record.json'))
 assert o['decision']=='REFUSED' and len(requests)==1,o
 checks.append({'id':'root_wrapper_record_exists_no_start','status':'PASS'})

 assert not DENIED
except Exception as e:
 checks.append({'id':'integration_exception','status':'FAIL','detail':repr(e),'trace':traceback.format_exc()[-5000:]})
# Hash named code and metadata read by this harness; no recursion or data-reference following.
opened_pins=[]
for p in sorted(list(OPENED)):
 if Path(p).is_file():opened_pins.append(pin(p))
rec={'date_u':datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),'n_total':len(checks),'n_pass':sum(c['status']=='PASS' for c in checks),'checks':checks,'source_pins':[pin(__file__),pin(BASE/'test_s1_path_c2v002c.py')],'opened_pins':opened_pins,'denied':DENIED,'substitutions':['Synthetic certificate worlds, verdict/adoption policy and source reviews.','Reviewed test direct adapter uses identity driver normalization and substitutes only custody return after actual deriver load.','Disk/process-table reads stubbed; output packet under run dir; no real subprocess allowed.','Root wrapper modules return actual guard/library with the inherited synthetic V006-path seam; simulated launch uses an in-memory subprocess stub.'],'production':'UNTESTED; real root dry preflights and review remain'}
T.wjson(RUN/'TEST_RECORD.json',rec)
print(json.dumps({k:rec[k] for k in ('n_total','n_pass','denied')}))
for c in checks:
 if c['status']=='FAIL':print(json.dumps(c))
sys.exit(0 if rec['n_total']==rec['n_pass'] and not DENIED else 1)
