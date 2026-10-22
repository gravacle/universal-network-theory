import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
import custody_guard_cx1v001 as G
from snapshot_cx1v001 import Snapshot,Refusal
root=Path(__file__).resolve().parent
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('custody_%Y%m%dT%H%M%S%f')
case.mkdir(parents=True,exist_ok=False)
mon={'path':str(root.parent/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'),'sha256':G.MONITOR_SHA}
def put(p,obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
    with p.open('xb') as f:f.write(raw)
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}
passed=[]
def trial(name,change=None):
    d=case/name;d.mkdir();(d/'out').mkdir()
    drv=put(d/'inert_driver.json',{'inert':True});sp=put(d/'spec.json',{'inert':True})
    res=put(d/'out/result.json',{'status':'COMPLETED','call_spec_sha256':sp['sha256'],'driver_sha256':drv['sha256']})
    finish={'result_path':res['path'],'result_sha256':res['sha256']}
    bundle=put(d/'bundle.json',{'inert_certificate_bundle':True})
    passdir=d/'ACCEPTANCE_TAILSTATES_C2V002_A001';passdir.mkdir()
    receipt={'schema':'UNT_GALAXY_M0_MONITOR_RECEIPT_C2V001','pins':{'driver':drv,'spec':sp},
             'result':res,'status':'FINISHED','driver_status':'COMPLETED','exit_code':0,'stop_reason':None}
    acc={'schema':'DDO154_TAIL_ACCEPTANCE_RECORD_C2V001','handoff':G.HANDOFF,'call_dir':str(d),
         'result':res,'bundle':bundle,'reading':'ACCEPTED','outputs_are_evidence':True,
         'guard':{'ok':True},'step4_stop_for_root_ruling':False,'tailstate_dir':str(passdir)}
    if change:change(d,receipt,acc,finish)
    put(d/'out/finish.json',finish)
    receipt['receipt_sha256']=hashlib.sha256(json.dumps(receipt,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    rp=put(d/'RECEIPT.json',receipt);ap=put(d/'acceptance.json',acc)
    candidate={'call_dir':str(d),'spec':sp,'receipt':rp,'acceptance':ap,'bundle':bundle}
    if name=='missing_acceptance':candidate['acceptance']={'path':str(d/'absent'),'sha256':'0'*64}
    if name=='foreign_receipt':candidate['receipt']={'path':str(d/'foreign'),'sha256':rp['sha256']}
    snap=Snapshot()
    try:r=G.check_valid_custody(snap,call={'spec_sha256':sp['sha256']},candidate=candidate,driver_pin=drv,monitor_pin=mon)
    except Refusal:
        assert name!='exact',name
        passed.append(name);return
    assert name=='exact',name
    assert r['prerequisites_only'] and max(snap.read_counts.values())==1
    passed.append(name)
trial('exact')
trial('foreign_receipt')
trial('missing_acceptance')
trial('failed_acceptance',lambda d,r,a,f:a.update(reading='INCOMPLETE'))
trial('foreign_acceptance',lambda d,r,a,f:a.update(call_dir=str(d.parent)))
trial('foreign_result',lambda d,r,a,f:r.update(result={'path':str(d/'other'),'sha256':'0'*64}))
trial('bad_finish',lambda d,r,a,f:f.update(result_sha256='0'*64))
trial('stopped',lambda d,r,a,f:r.update(status='STOPPED_WALL',stop_reason='WALL'))
trial('not_latest',lambda d,r,a,f:(d/'ACCEPTANCE_TAILSTATES_C2V002_A002').mkdir())
trial('pass_gap',lambda d,r,a,f:(d/'ACCEPTANCE_TAILSTATES_C2V002_A003').mkdir())
trial('unknown_pass',lambda d,r,a,f:(d/'ACCEPTANCE_TAILSTATES_OTHER').mkdir())
trial('wrong_bundle',lambda d,r,a,f:a.update(bundle={'path':str(d/'other'),'sha256':'0'*64}))
report={'status':'PASS','blocking_count':0,'scope':'VALID custody prerequisites only; no certificate/taxonomy admission',
        'tested':passed,'untested':['F6 root judgment','certificate semantics','cache integration','whole-engine replay'],
        'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [Path(G.__file__),Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
