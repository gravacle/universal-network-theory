from pathlib import Path
import json,hashlib,types,os,sys,copy
import numpy
ROOT=Path(__file__).parent
SRC=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py')
def h(b):return hashlib.sha256(b).hexdigest()
raw=SRC.read_bytes();assert h(raw)=='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
def guard(event,args):
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.fsdecode(args[0]);
  if '/runs/' in p or '/runs_ext/' in p:raise RuntimeError('FORBIDDEN_RUN_READ')
  if not any(p.startswith(x) for x in [str(ROOT),str(SRC),sys.base_prefix,'/System/Library/','/usr/share/zoneinfo/','/etc/localtime','/private/var/db/timezone/']):raise RuntimeError('UNREGISTERED_READ')
sys.addaudithook(guard)
m=types.ModuleType('cx2r8lon');m.__file__=str(SRC);exec(compile(raw,str(SRC),'exec'),m.__dict__)
prod=ROOT/'owned_synthetic_producer.py';psha=h(prod.read_bytes())
base={'schema':m.GATE_SCHEMA,'gate':'LO_NGC','verdict':'PASS','producer':{'path':str(prod),'sha256':psha},'operator_sha256':m.NGC_T120L_OPERATOR_SHA256,'summed_max_over_theta':0.0006,'shells':[{'range_inverse_kpc':[a,b],'max_over_theta':0.0001} for a,b in [(2,3),(3,4),(4,6),(6,8),(8,12),(12,16)]]}
def write(name,obj):
 p=ROOT/name
 with p.open('x') as f:f.write(json.dumps(obj,sort_keys=True,indent=2)+'\n')
 return p
rows=[]
for name,kind in [('ngc_baseline','baseline'),('ngc_bad_single','single'),('ngc_bad_duplicate_first','first'),('ngc_bad_duplicate_last','last')]:
 rec=copy.deepcopy(base);bad={'range_inverse_kpc':[2,3],'max_over_theta':0.1}
 if kind=='single':rec['shells'][0]=bad
 elif kind=='first':rec['shells'].insert(0,bad)
 elif kind=='last':rec['shells'].append(bad)
 p=write(name+'.json',rec)
 reg={'schema':m.PRODUCER_REGISTRY_SCHEMA,'producers':{'LO_NGC':[psha]},'identity_comparators':[],'identity_tokens':{},'gate_records':{'LO_NGC':[h(p.read_bytes())]},'gq_all_nodes_counts':{}}
 rp=write(name+'_registry.json',reg)
 got=m.evaluate_gate('LO_NGC',p,{'producer_registry':m.load_producer_registry(rp)})
 rows.append({'case':name,'expected':'PASS' if kind=='baseline' else 'RECORD_DEFECT','actual':got['status'],'codes':got['codes'],'record':str(p),'sha256':h(p.read_bytes()),'registry':str(rp),'registry_sha256':h(rp.read_bytes())})
result={'date_u':os.environ['UNT_CX2_PACKET_UTC'],'source_sha256_before':h(raw),'source_sha256_after':h(SRC.read_bytes()),'scope':'Synthetic LO_NGC operator sha text only; no NGC operator/observed/target data opened; no production evidence or launch.','checks':rows}
p=write('LO_NGC_DUPLICATE_RESULTS_CX2V001.json',result)
print(json.dumps({'path':str(p),'sha256':h(p.read_bytes()),'results':[(x['case'],x['actual']) for x in rows]}))
