import copy, hashlib, json, tempfile
from pathlib import Path
from snapshot_cx1v001 import Snapshot, Refusal
from direct_layout_cx1v001 import bind_layout

base=Path(tempfile.mkdtemp(prefix='layout_',dir=Path(__file__).parent/'inert_fixtures')).resolve()
spec={'path':str(base/'source_spec.json'),'sha256':'a'*64}
driver={'path':str(base/'driver.py'),'sha256':'b'*64}
call={'case':'seed','spec':spec,'driver':driver,'outdir':str(base/'direct_output'),
      'receipt':str(base/'terminal.json'),'monitor_log':str(base/'monitor.log')}
plan={'calls':[call],'launcher_log':str(base/'launcher.log')}
results=[]
def check(label, obj, error=None, **kw):
    p=base/(label+'.json');raw=json.dumps(obj).encode();p.write_bytes(raw)
    pin={'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}
    snap=Snapshot()
    try:
        got=bind_layout(snap,plan_pin=pin,case='seed',expected_spec=kw.get('spec',spec),expected_driver=driver)
        assert error is None, label
        assert got['result_path']==str(base/'direct_output/result.json')
        assert got['receipt_path']==str(base/'terminal.json')
        assert not (base/'direct_output').exists()
        assert snap.read_counts=={str(p):1}
    except Refusal as exc:
        assert str(exc)==error,(label,str(exc),error)
    results.append(label)
check('pending_original_paths',plan)
x=copy.deepcopy(plan);x['calls'].append(copy.deepcopy(call));check('duplicate_case',x,'LAYOUT_DUPLICATE_CASE')
x=copy.deepcopy(plan);x['calls'][0]['receipt']=str(base/'direct_output/r.json');check('nested_receipt',x,'LAYOUT_OUTPUT_OVERLAP')
x=copy.deepcopy(plan);x['calls'][0]['monitor_log']=call['receipt'];check('alias_output',x,'LAYOUT_OUTPUT_OVERLAP')
x=copy.deepcopy(plan);x['calls'][0]['outdir']='relative';check('relative',x,'LAYOUT_NONCANONICAL_PATH')
x=copy.deepcopy(plan);x['calls'][0]['outdir']=str(base)+'/a/../direct_output';check('dotdot',x,'LAYOUT_NONCANONICAL_PATH')
x=copy.deepcopy(plan);x['calls'][0]['case']='other';check('missing_case',x,'LAYOUT_CASE_MISSING')
check('wrong_spec',plan,'LAYOUT_IDENTITY_MISMATCH',spec={**spec,'sha256':'c'*64})
x=copy.deepcopy(plan);x['calls'].append({**call,'case':'plus','outdir':str(base/'other'),'receipt':str(base/'r2'),'monitor_log':call['monitor_log']});check('cross_call_alias',x,'LAYOUT_OUTPUT_OVERLAP')
(base/'real_dir').mkdir();(base/'alias').symlink_to(base/'real_dir',target_is_directory=True)
x=copy.deepcopy(plan);x['calls'][0]['outdir']=str(base/'alias/out');check('symlink_parent',x,'LAYOUT_NONCANONICAL_PATH')
report={'status':'PASS','blocking_count':0,'scope':'Direct layout structural metadata only; not admission','tested':results,'untested':['Root plan approval','Acceptance producer/consumer integration','Live paths and execution']}
p=base/'TEST_REPORT.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p)
