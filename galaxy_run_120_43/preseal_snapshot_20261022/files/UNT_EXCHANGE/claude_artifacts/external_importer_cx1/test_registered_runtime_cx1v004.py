import json,hashlib,tempfile,copy
from pathlib import Path
from registered_runtime_cx1v005 import check_registered_runtime
from snapshot_cx1v001 import Snapshot,Refusal
b=Path(__file__).resolve().parent;c=Path(tempfile.mkdtemp(prefix='registered_runtime_',dir=b/'inert_fixtures'))
source=b/'inert_fixtures/capture_pipeline_bu8gbjkh/capture.json';runtime=json.loads(source.read_bytes())
def write(name,obj):
 p=c/name;raw=json.dumps(obj,sort_keys=True).encode()
 with p.open('xb') as f:f.write(raw)
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest())
context={k:v*64 for k,v in zip(['config_sha256','cache_id','gate_digest'],'abc')};passed=[]
for serial,mode in enumerate(['valid','version_mismatch','wrong_producer','wrong_driver','wrong_root','unregistered','absent_equal','presence_mismatch','binding_mismatch','binding_missing','early_capture','late_capture','wrong_interpreter','wrong_freeze','naive_time']):
 direct=copy.deepcopy(runtime);campaign=copy.deepcopy(runtime)
 if mode in ('absent_equal','presence_mismatch'):
  campaign=json.loads((source.parent/'absent.json').read_bytes())
  if mode=='absent_equal':direct=copy.deepcopy(campaign)
 if mode=='version_mismatch':campaign['distributions'][0]['version']='WRONG'
 if mode=='wrong_producer':direct['producer']['sha256']='f'*64
 direct['captured_utc']=campaign['captured_utc']='2026-10-21T12:00:00Z'
 if mode=='early_capture':direct['captured_utc']='2026-10-21T10:00:00Z'
 if mode=='late_capture':campaign['captured_utc']='2026-10-21T14:00:00Z'
 if mode=='naive_time':direct['captured_utc']='2026-10-21T12:00:00'
 dp=write(str(serial)+'direct.json',direct);cp=write(str(serial)+'campaign.json',campaign)
 entries=[]
 for row in [28,29,30,31,300,301,302]:
  key=hashlib.sha256(str(row).encode()).hexdigest();dummy={'path':str(c/'UNREAD'),'sha256':'d'*64}
  entries.append(dict(row=row,key=key,spec=dummy,call_root=str(c/('DDO154_JACOBIAN_R%d_%s_A1'%(row,key[:16]))),attempt=1,launcher=dummy,guard=dummy,binder=dummy,dbp=dummy,runtime_capture=dp))
 rp=write(str(serial)+'register.json',dict(schema='SPECULATIVE_REGISTER_L2_V001',entries=entries));binding=dict(schema='SPECULATIVE_REGISTER_BINDING_L2_V001',register=rp,context=context,campaign_capture=cp)
 freeze=write(str(serial)+'freeze.json',dict(schema='CX1_IMPORTER_FREEZE_V001',utc='2026-10-21T11:00:00Z',policy=dummy,entry=dummy))
 identity={k:runtime['interpreter'][k] for k in ['realpath','sha256']}
 binding.update(utc='2026-10-21T13:00:00Z',interpreter=identity,freeze=freeze)
 launch=dict(schema='SPECULATIVE_LAUNCH_L2_V001',utc='2026-10-21T13:00:00Z',register=rp,runtime_capture=dp,interpreter=copy.deepcopy(identity),freeze=freeze)
 if mode=='wrong_interpreter':launch['interpreter']['sha256']='0'*64
 if mode=='wrong_freeze':launch['freeze']=dummy
 lp=write(str(serial)+'launch.json',launch)
 if mode=='binding_mismatch':binding['campaign_capture']=dp
 if mode=='binding_missing':binding.pop('campaign_capture')
 bp=write(str(serial)+'binding.json',binding)
 policy=dict(freeze=freeze,direct_launch=lp,campaign_capture=cp,producer=runtime['producer'],output_root=str(c),**{name:dict(path=runtime[name]['realpath'],sha256=runtime[name]['sha256']) for name in ['driver','monitor']})
 if mode=='wrong_driver':policy['driver']['sha256']='e'*64
 if mode=='wrong_root':policy['output_root']=str(c/'foreign')
 snapshot=Snapshot()
 try:result=check_registered_runtime(snapshot,register_pin=rp,binding_pin=bp,context=context,key='0'*64 if mode=='unregistered' else entries[0]['key'],spec_pin=entries[0]['spec'],runtime_policy=policy)
 except Refusal:assert mode not in ['valid','absent_equal','unregistered'],mode
 else:
  assert mode in ['valid','absent_equal','unregistered'],mode
  assert result['registered']==(mode in ('valid','absent_equal'))
  assert len(snapshot.read_counts)==(6 if mode in ('valid','absent_equal') else 2)
 passed.append(mode)
r=dict(status='PASS',blocking_count=0,scope='Actual register/runtime guard and strict snapshots; inert root policy and runtime records',tested=passed,untested=['Root authentication of input pins','Live observer/ingestion integration','Final envelope invalidation handling'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [b/'registered_runtime_cx1v005.py',b/'register_two_stage_cx1v003.py',b/'runtime_distribution_record_cx1v004.py',source,Path(__file__),b/'runtime_launch_binding_cx1v001.py']])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
