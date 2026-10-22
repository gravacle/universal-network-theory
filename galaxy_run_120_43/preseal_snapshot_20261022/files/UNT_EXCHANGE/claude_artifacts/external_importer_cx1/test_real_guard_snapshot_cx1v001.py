"""Real pinned b1 guard + synthetic proofs. No wrapper/physics admission claim."""
import hashlib,json,math,sys,types
from pathlib import Path
from datetime import datetime,timezone
from snapshot_cx1v001 import Snapshot
from readonly_scope_cx1v001 import ReadOnlyScope
root=Path(__file__).resolve().parent
source=root.parent/'s4_acceptance_c2/offset_b1/certificate_guard_b1_c2v001.py'
raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='9e3fc109621a9e600e2ea4aa8346c3e2baf002ac3df759238f7d8efcb3809677'
G=types.ModuleType('_cx1_real_guard_fixture');G.__file__=str(source)
exec(compile(raw,str(source),'exec'),G.__dict__)
case=root/'inert_fixtures'/datetime.now(timezone.utc).strftime('real_guard_%Y%m%dT%H%M%S%f')
case.mkdir(parents=True,exist_ok=False)
def put(p,obj):
 b=json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
 with p.open('xb') as f:f.write(b)
 return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest()}
producer=put(case/'producer.json',{'inert':True})
identity={'numerics':{'uv_tail':{'enabled':True,'source_rule':'continuum_v001','outer':{'shape':'cylinder','K_big_inverse_kpc':128.0},'gas':{'M_s':128}}}}
custody={k:'1'*64 for k in G.CUSTODY_KEYS}
state={'state_sha256':'2'*64,'source_sha256':'3'*64,'stage_kind':'route_a','nonnegative_masses':True}
edge=math.ceil(math.sqrt(2)*128)
def proof(gate,**kw):return dict(schema=G.PROOF_SCHEMA,gate=gate,status='TESTED',verdict='PASS',point_sha256=G.digest(identity),custody_sha256=G.digest(custody),producer=producer,**kw)
eps=put(case/'eps.json',proof('EPS',envelope_rule=G.ENVELOPE,shells=[{'range_inverse_kpc':[4,edge],'eps':1e-9,'eps_envelope':1e-9,'refinement_failures':0}]))
gq=put(case/'gq.json',proof('GQ',method='GEOMETRY_UNIFORM_COLUMN_BOUND',all_columns_included=True,all_production_kperp_nodes=True,nonnegative_masses_required=True,M_s=128,M_s_doubled=256,K_big_inverse_kpc=128.0,max_column_difference_over_analytic_Pi0=1e-15,max_zero_mode_relative_error=0.0))
lo=put(case/'lo.json',proof('LO',state=state,shells=[{'range_inverse_kpc':[4,edge],'max_over_tau':0.001}],summed_max_over_tau=0.001,row_contract_sha256=custody['row_contract_sha256'],i1t_verdict='PASS',GQ_uniform_proof_sha256=gq['sha256']))
bundle=put(case/'bundle.json',{'schema':G.SCHEMA,'identity':identity,'custody':custody,'domain':{'K_inverse_kpc':4.0,'K_big_inverse_kpc':128.0},'prelaunch':{'EPS':eps,'GQ':gq},'acceptance_rule':'ALL_CONSUMED_STATES_LO_AND_GQ_FAIL_CLOSED','states':[{'state':state,'LO':lo}]})
args={'expected_custody':custody,'approved_producer_sha256':[producer['sha256']],'phase':'acceptance','required_states':[state]}
baseline=G.verify_bundle(bundle,identity,**args)
assert baseline['ok'],baseline
reads={};active=False
def audit(event,args):
 if active and event=='open' and isinstance(args[0],str) and args[0].startswith(str(case)+'/'):
  reads[args[0]]=reads.get(args[0],0)+1
sys.addaudithook(audit)
active=True
snap=Snapshot()
with ReadOnlyScope(snap,[G]):
 observed=G.verify_bundle(bundle,identity,**args)
 again=G.verify_bundle(bundle,identity,**args)
active=False
assert observed==again==baseline
assert len(reads)==5 and max(reads.values())==1,reads
passed=['real guard acceptance matches baseline','repeat verification uses same snapshot','five evidence files each opened once']
for name,kw in [('unapproved',dict(args,approved_producer_sha256=['f'*64])),('missing_state',dict(args,required_states=[])),('foreign_state',dict(args,required_states=[dict(state,source_sha256='4'*64)])),('wrong_custody',dict(args,expected_custody=dict(custody,grid_sha256='f'*64)))]:
 with ReadOnlyScope(Snapshot(),[G]):r=G.verify_bundle(bundle,identity,**kw)
 assert not r['ok'],name
 passed.append(name)
report={'status':'PASS','blocking_count':0,'scope':'Real b1 guard on inert metadata proofs only','tested':passed,
'untested':['full wrapper certificate_check','real state enumerator','F6','whole-engine replay','production integration'],
'pins':[{'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [source,root/'readonly_scope_cx1v001.py',root/'snapshot_cx1v001.py',Path(__file__)]]}
with (case/'TEST_REPORT.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(case/'TEST_REPORT.json')
