import tempfile,json,hashlib,copy
from pathlib import Path
from register_two_stage_cx1v001 import select_two_stage
from snapshot_cx1v001 import Snapshot,Refusal
root=Path(__file__).resolve().parent;case=Path(tempfile.mkdtemp(prefix='register2_',dir=root/'inert_fixtures'))
def write(p,o):
 raw=json.dumps(o,sort_keys=True).encode()
 with p.open('xb') as f:f.write(raw)
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest()}
context={k:c*64 for k,c in zip(('config_sha256','cache_id','gate_digest'),'abc')}
entries=[]
for i,row in enumerate((28,29,30,31,300,301,302)):
 key=hashlib.sha256(str(row).encode()).hexdigest();pin={'path':str(case/('NEVER_OPEN_%d'%row)),'sha256':'d'*64}
 entries.append(dict(row=row,key=key,spec=pin,call_root=str(case/('DDO154_JACOBIAN_R%d_%s_A1'%(row,key[:16]))),attempt=1,launcher=pin,guard=pin,binder=pin,dbp=pin,runtime_capture=pin))
passed=[];serial=0
reg={'schema':'SPECULATIVE_REGISTER_L2_V001','entries':entries}
def run(mutate=lambda r,b:None):
 global serial
 serial+=1;r=copy.deepcopy(reg);bind={'schema':'SPECULATIVE_REGISTER_BINDING_L2_V001','context':context}
 mutate(r,bind);rp=write(case/('register%d.json'%serial),r);bind.setdefault('register',rp);bp=write(case/('binding%d.json'%serial),bind)
 snap=Snapshot();got=select_two_stage(snap,register_pin=rp,binding_pin=bp,context=context,key=entries[0]['key'],spec_pin=entries[0]['spec'])
 assert len(snap.read_counts)==2
 return got
assert run()['entry']==entries[0];passed.append('two stages bind and select with only two metadata reads')
for name,m in [('foreign register',lambda r,b:b.update(register={'path':'/inert/foreign','sha256':'f'*64})),('foreign context',lambda r,b:b.update(context={**context,'cache_id':'f'*64})),('duplicate row',lambda r,b:r['entries'][1].update(row=28)),('wrong spec',lambda r,b:r['entries'][0].update(spec={'path':'/inert/foreign','sha256':'f'*64})),('missing call',lambda r,b:r['entries'].pop()),('status field',lambda r,b:r['entries'][0].update(status='COMPLETED_VALID')),('foreign root name',lambda r,b:r['entries'][0].update(call_root='/inert/foreign'))]:
 try:run(m)
 except Refusal:passed.append(name+' refuses')
 else:raise AssertionError(name)
r=dict(status='PASS',blocking_count=0,scope='0843 two-stage register metadata guard, inert fixtures',tested=passed,untested=['Root publication/authentication','Runtime capture content','Natural-plan/executor integration'],pins=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [Path(__file__),root/'register_two_stage_cx1v001.py']])
p=case/'TEST_REPORT.json';write(p,r);print(p)
