import importlib.util,json
from pathlib import Path
R=Path(__file__).parent;p=R/'ea_replay_cx1v004.py'
sp=importlib.util.spec_from_file_location('ea_fast_test',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
radii=[1.+x for x in range(12)];rec={'probe_R_m':radii,'accepted_iteration':3,'E_A_rows_km_s_accepted':[.01]*12}
checks=[]
def ck(n,ok):checks.append({'name':n,'passed':ok});assert ok
ck('missing_radii_requires_replay',m.recorded_entry({},radii,'a'*64) is None)
ck('valid_record_used',m.recorded_entry(rec,radii,'a'*64)['accepted_iteration']==3)
for field,val in [('probe_R_m',[2.]*12),('E_A_rows_km_s_accepted',[-1.]*12),('accepted_iteration',True)]:
    bad=dict(rec);bad[field]=val
    try:m.recorded_entry(bad,radii,'a'*64);ok=False
    except ValueError:ok=True
    ck('refuse_'+field,ok)
with (R/'EA_RECORDED_PATH_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED synthetic record-path cases','checks':checks,'passed':len(checks),'producer':m.pin(p),'test':m.pin(Path(__file__))},f,indent=1)
print('EA recorded path',len(checks),'PASS')
