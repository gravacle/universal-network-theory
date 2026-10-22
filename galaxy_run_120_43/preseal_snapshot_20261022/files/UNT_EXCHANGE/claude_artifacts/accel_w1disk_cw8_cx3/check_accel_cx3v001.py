"""0817: source-only/AST and inert metadata checks; no scientific module execution."""
from pathlib import Path
import ast, copy, hashlib, json, subprocess, types, math
BASE=Path('/Users/bgm/Research/UNT_EXCHANGE')
A=BASE/'claude_artifacts'
OUT=A/'accel_w1disk_cw8_cx3'
C2=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2')
S={
'DISPATCH':BASE/'FROM_CODEX/0817_2026-10-21_codex3_W1_before_drive_and_cw8_phase1.md',
'V006':C2/'ROOT_DECISIONS_NGC3198_CONSTRUCTION_2026-10-17_V006_ADDENDUM.md',
'STORAGE':A/'h3_campaign_path_c2/storage_check_h3_c2v003.py',
'STORAGE_PARENT':A/'h3_campaign_path_c2/storage_check_h3_c2v001.py',
'ERRATUM':A/'h3_campaign_path_c2/STORAGE_PLAN_ERRATUM_C2V001.md',
'ORCH':A/'calibration_orchestrator_c2/v005/calibration_orchestrator_c2v005.py',
'WRAPPER':A/'h3_campaign_path_c2/calibration_orchestrator_q5b1_ledger_c2v004.py',
'ENTRY':A/'h3_campaign_path_c2/h3_campaign_entry_c2v004.py',
'A133':C2/'A133_TWO_PHASE_PROTOCOL_V001.md',
'PREREG':A/'miss_reading_prereg_c4/r3a_sc3/PREREG_MISS_READING_R3A.md',
'COMPARATOR':A/'step5_path_c2/tools/compare_identity_pair_c2v001.py',
'PAIR_SPEC':A/'step5_path_c2/IDENTITY_PAIR_COMPARISON_SPEC_C2V001.md',
'FILLER':A/'step5_path_c2/tools/fill_step5_c2v001.py',
'POLICY':A/'step5_path_c2/POLICY_C2V001.json',
'CAPS':A/'step5_path_c2/CAPS_FIRST_NGC_POINT_C2V001.json',
'ESTIMATE':A/'ngc_point_producer_c4/ri45_12/estimate/ESTIMATE_RI45_12_NGC_K32_C4V002.json',
'ESTIMATE_VERIFY':A/'ngc_point_producer_c4/ri45_12/verify/VERIFY_RI45_12_C4V001.md',
'P112':A/'phase1_ngc_launch_kit_cx2v004/phase1_ngc_launch_cx2v004.py',
'P112_README':A/'phase1_ngc_launch_kit_cx2v004/README_CONTRACT_CX2V004_V001.md',
'RUNBOOK':A/'runbook_v002_c2v007_cx2/RUNBOOK_V002_C2V007.md',
'BUILDER':A/'runbook_v002_c2v007_cx2/roster_builder_c2v007_a253_v001.py',
'KIT_README':A/'s0_launch_kit_c2/README_S0_LAUNCH_KIT_C2V003A.md',
'DRIVER':A/'ngc_cx3r008_closure_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r008_cx3v001.py',
'PARALLEL':A/'tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_parallel_uvtail_c2v001.py',
'SERIAL':A/'tail_scheme_impl_c2/route_a/coupled_hi_fourier_source_iteration_v005_resume_fixedsrc_uvtail_c2v001.py',
'ENGINE':A/'calibration_engine_freeze_v003b_v003d/calibration_region_engine_c2v003b.py',
}
raw={k:p.read_bytes() for k,p in S.items()}
sha=lambda b:hashlib.sha256(b).hexdigest()
reg={k:{'path':str(S[k]),'sha256':sha(b),'bytes':len(b)} for k,b in raw.items()}
reg['CHECKER']={'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__).read_bytes())}
stamp=subprocess.check_output(['date','-u'],text=True).strip()
checks=[]
def ck(name,cond,detail=None):
 checks.append({'name':name,'classification':'TESTED_SYNTHETIC_OR_STATIC','pass':bool(cond),'detail':detail})
 if not cond:raise AssertionError(name)
expected={'ORCH':'c75a889ff4646a816329756124a19532cbc166d26f47ce2ea5147b71c2cf7c4d','STORAGE_PARENT':'e0b3a89a4a2930311c393cd62d2f51b0b343fe705736d8083a45628c8a75706d','DRIVER':'577f8c94366ae8f99c5387b87397a83020f8186dc523b987d042103283346377','P112':'8cec1b56fc682f638fee57329eefc9b3cddfa47959d175e7095fc0c5fe0342c9','SERIAL':'8ef3079b0a23c32c688605e96eb5b79beb79768578cc7aef22ea087c7ae12469','PARALLEL':'7667025bd9382a58688153fde98bf90f2b67d27baa39a939982631c305c229db'}
for k,h in expected.items():ck('byte_pin_'+k,reg[k]['sha256']==h)
trees={k:ast.parse(b,filename=str(S[k])) for k,b in raw.items() if S[k].suffix=='.py'}
for k in trees:ck('parse_'+k,True)
def select(k,name,cls=None):
 nodes=trees[k].body
 if cls:nodes=next(n for n in nodes if isinstance(n,ast.ClassDef) and n.name==cls).body
 n=copy.deepcopy(next(n for n in nodes if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name));n.decorator_list=[]
 return n
def funcs(k,names,ns):
 nodes=[select(k,n,c) for n,c in names]
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(S[k]),'exec'),ns)
 return ns
class Error(Exception):pass
ns={'json':json,'OrchestratorError':Error,'WORK_DIR_IDENTITY_KEYS':('resolved','volume','volume_uuid','symlinks')}
funcs('ORCH',[('canonical',None),('work_dir_identity_core',None),('check_work_dir_identity',None),('_work_dir_json_core','Orchestrator')],ns)
old={'configured':'/inert/campaign','resolved':'/inert/campaign','volume':'/inert','volume_uuid':'INERT_A','symlinks':[],'work_dir_st_ino':100}
pin=ns['work_dir_identity_core'](old)
ck('workdir_identity_positive',ns['check_work_dir_identity'](pin,old)==[])
for field,new in [('resolved','/inert_new/campaign'),('volume','/inert_new'),('volume_uuid','INERT_B'),('symlinks',[{'link':'/inert/campaign','target':'/inert_new/campaign'}])]:
 changed=dict(old,**{field:new});bad=ns['check_work_dir_identity'](pin,changed)
 ck('workdir_refuses_'+field,bool(bad),bad)
ck('copied_directory_inode_changes_WORK_DIR_core',ns['_work_dir_json_core'](old)!=ns['_work_dir_json_core'](dict(old,work_dir_st_ino=200)))
lns={'LEDGER_SCHEMA':'SYNTHETIC_LEDGER','LEDGER_NAME':'CERTIFICATE_LEDGER.jsonl'}
funcs('WRAPPER',[('ledger_policy_problems','Context')],lns)
obj=types.SimpleNamespace(work_dir=Path('/inert/campaign'),cfg={'tail_readiness':{'certificate_ledger':{'schema':'SYNTHETIC_LEDGER','path':'/inert/campaign/CERTIFICATE_LEDGER.jsonl'},'certificate_registry':{}}})
ck('ledger_path_positive',lns['ledger_policy_problems'](obj)==[])
obj.work_dir=Path('/inert_new/campaign')
ck('ledger_refuses_old_path_after_workdir_change',bool(lns['ledger_policy_problems'](obj)))
# Actual P112 metadata validator, no filesystem/runtime module imports.
def need(c,code,*args):
 if not c:raise Error(code)
def dig(o,ks):
 for k in ks:o=o[k]
 return o
pns={'copy':copy,'need':need,'dig':dig,'canonical':ns['canonical'],'LEAF':('numerics','route_a','column_workers')}
funcs('P112',[('strip_leaf',None),('fill_check',None)],pns)
eps={'path':'/inert/eps','sha256':'a'*64};lo={'path':'/inert/lo','sha256':'b'*64};hp={'path':'/inert/handoff','sha256':'c'*64};key='d'*64
s={'label':'step5 A_K32_A2_HEADLINE theta_key='+key,'numerics':{'route_a':{'column_workers':1},'uv_tail':{'eps_certificate':eps,'lo_certificate':lo}}}
t=copy.deepcopy(s);t['numerics']['route_a']['column_workers']=8
h={'schema':'UNT_STEP5_PHASE1_POINT_HANDOFF_C2V001','mode':'PHASE1_POINT','driver_branch':'cx3r008','certificate_pins':{'eps_certificate':eps,'lo_certificate':lo}}
f={'schema':'UNT_STEP5_FILLED_SPECS_C2V001','launch_authorized':False,'handoff_pin':hp,'theta_key':key,'pending_certificates':[]}
pns['date_u']=lambda:'INERT'
ck('P112_serial_twin_fill_positive',pns['fill_check'](h,hp,s,t,f,key,eps,lo,h['schema'])['ok'])
try:pns['fill_check'](h,hp,t,t,f,key,eps,lo,h['schema'])
except Error as e:ck('P112_cw8_in_serial_slot_refused',str(e)=='SPEC_LEAF',str(e))
else:ck('P112_cw8_in_serial_slot_refused',False)
read_fill=ast.unparse(select('P112','read_fill','Context'))
ck('P112_read_fill_selects_serial_spec','return (serial, sp, (serial, twin, receipt), fp, certificates)' in read_fill)
# Source-only budget arithmetic. The threshold function has no I/O.
G=1<<30
tns={'GiB':G};funcs('STORAGE',[('threshold',None)],tns)
waves=ast.literal_eval(next(n.value for n in trees['STORAGE_PARENT'].body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ENGINE_SHAPED' for t in n.targets)))
df=subprocess.check_output(['df','-k','/System/Volumes/Data','/Volumes/External1'],text=True)
rows=df.strip().splitlines()[1:]
vol={r.split()[-1]:{'total_bytes':int(r.split()[1])*1024,'free_bytes':int(r.split()[3])*1024} for r in rows}
H=397867631966
historic={'internal_free_GiB':953.0,'external_free_GiB':2877.5,'other_program_GiB':H/G}
actual={'date_u':stamp,'df_stdout':df,'volumes':vol,'other_program_reserved_bytes':H,'reservation_note':'Whole historical HEADLINE11+S0x4 forecast reserved conservatively; no run bytes inspected. Some may already occupy df used space. Extra twin/NGC/certificates/OS margin remain additional Y.'}
mathrows=[]
for label,free,other in [('historical_internal',953*G,H),('current_internal',vol['/System/Volumes/Data']['free_bytes'],H),('historical_external_H_internal',2877.5*G,0),('current_external_H_internal',vol['/Volumes/External1']['free_bytes'],0)]:
 for b in [17442511906,57.19*G]:
  before=0;wr=[]
  for k,n in enumerate(waves,1):
   need=before*b+n*80*G+20*G+other
   wr.append({'wave':k,'n':n,'calls_before':before,'need_GiB':need/G,'fits':need<=free});before+=n
  jrows=[];before=0
  for k,n in enumerate([1,3,3],1):
   need=before*b+n*80*G+20*G+other;jrows.append({'wave':k,'n':n,'calls_before':before,'need_GiB':need/G,'fits':need<=free});before+=n
  mathrows.append({'case':label,'free_GiB':free/G,'b_GiB':b/G,'other_GiB':other/G,'ENGINE_SHAPED_assumed':wr,'first_halting_assumed_wave':next((r['wave'] for r in wr if not r['fits']),None),'expected_1_3_3_case':jrows,'concurrent_7_guard_GiB':(7*80*G+20*G+other)/G,'concurrent_7_fits':7*80*G+20*G+other<=free})
thresholds={}
for label,F,Hh in [('historic_two_volumes',(953+2877.5)*G,H),('current_two_volumes',sum(v['free_bytes'] for v in vol.values()),H),('external_total_if_all_other_data_offloaded',vol['/Volumes/External1']['total_bytes'],0)]:
 thresholds[label]=tns['threshold'](17442511906,waves,F,Hh,80*G,20*G)
ck('120_call_assumption_count',sum(waves)==120)
ck('historical_binding_wave_15',thresholds['historic_two_volumes']['binding_wave']==15)
ck('historical_R_rounds_3385_8',thresholds['historic_two_volumes']['R_GiB']==3385.8)
ck('historical_bstar_rounds_17_08',thresholds['historic_two_volumes']['b_star_GiB']==17.08)
est=json.loads(raw['ESTIMATE']);timing={'source_scope':'ESTIMATE, not measured full NGC run; E/U are scenarios, U is not a bound','serial_point_h':est['serial']['point_h'],'cw8_point_h':est['column_workers_8']['point_h'],'savings_h':est['column_workers_8']['gain_h'],'whole_point_speedup':{x:est['serial']['point_h'][x]/est['column_workers_8']['point_h'][x] for x in ['E','U']},'twin_cap_s':json.loads(raw['CAPS'])['identity_twin']['wall_cap_s'],'twin_time_model_h':est['identity_test'],'route_B_h_unknown':est['serial']['route_b_h_unknown_bracket']}
ck('22752_is_2x_modelled_3_16h',timing['twin_cap_s']==2*3.16*3600)
for x in ['E','U']:ck('point_saving_rounding_'+x,abs(timing['serial_point_h'][x]-timing['cw8_point_h'][x]-timing['savings_h'][x])<.02)
# Preserve only relevant sections of the mutable root source under its whole-byte hash.
vs=raw['V006'].decode().splitlines();wanted={'A133','A135','A137','A140','A141','A143','A147','A166','A177','A191','A192','A255'}
excerpt=['# V006 section excerpts for 0817','',stamp,'','Source '+reg['V006']['path']+' SHA256 '+reg['V006']['sha256'],'']
active=False
for i,line in enumerate(vs,1):
 if line.startswith('## '):active=any(line.startswith('## '+w+':') for w in wanted)
 if active:excerpt.append(str(i)+': '+line)
outputs={'SOURCE_PINS_CX3V001.json':{'date_u':stamp,'sources':reg},'EVIDENCE_CX3V001.json':{'date_u':stamp,'scope':'AST/static/inert metadata and arithmetic only; no real campaign/NGC data or runs','checks':checks,'n_pass':len(checks),'sources':reg,'storage_measurement':actual,'historic_storage_inputs':historic,'capacity_cases':mathrows,'thresholds':thresholds,'timing':timing,'UNTESTED':['actual W1 accepted bytes','actual campaign wave shape after expected first Jacobian','movable non-pinned data amount','production NGC pair result','all later-iteration/all-theta numerical identity','cw8 production launch/custody successor','wall speed under actual concurrent load']}}
for name,obj in outputs.items():
 p=OUT/name
 with p.open('x') as f:json.dump(obj,f,indent=2,sort_keys=True);f.write('\n')
 print(name,sha(p.read_bytes()),p.stat().st_size)
p=OUT/'V006_EXCERPTS_CX3V001.md'
with p.open('x') as f:f.write('\n'.join(excerpt)+'\n')
print(p.name,sha(p.read_bytes()),p.stat().st_size)
print('PASS',len(checks),'internal_GiB',vol['/System/Volumes/Data']['free_bytes']/G,'external_GiB',vol['/Volumes/External1']['free_bytes']/G)
