from pathlib import Path
import json,hashlib,types,os,sys,copy,math
import numpy
ROOT=Path(__file__).parent
SRC=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py')
def h(b):return hashlib.sha256(b).hexdigest()
raw=SRC.read_bytes();assert h(raw)=='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
def guard(event,args):
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  p=os.fsdecode(args[0])
  if '/runs/' in p or '/runs_ext/' in p:raise RuntimeError('FORBIDDEN_RUN_READ')
  if not any(p.startswith(x) for x in [str(ROOT),str(SRC),sys.base_prefix,'/System/Library/','/usr/share/zoneinfo/','/etc/localtime','/private/var/db/timezone/']):raise RuntimeError('UNREGISTERED_READ')
sys.addaudithook(guard)
m=types.ModuleType('cx2r8rb');m.__file__=str(SRC);exec(compile(raw,str(SRC),'exec'),m.__dict__)
prod=ROOT/'owned_synthetic_producer.py';psha=h(prod.read_bytes());top=math.sqrt(2)*128
base={'schema':m.GATE_SCHEMA,'gate':'RB_FP','verdict':m.GATE_PASS_VERDICTS['RB_FP'],'producer':{'path':str(prod),'sha256':psha},'case':'C4T','c4t_result_sha256':'1'*64,'eps_max':0.001,'shells':['owned'],'dV_static_shells_km_s':{'owned':[0]*12},'shell_ranges_inverse_kpc':[[4,top]],'full_tail_domain':True}
cb={'cases':{'C4T':{'normalized_spec_equal':{'/numerics':{'uv_tail':{'outer':{'shape':'cylinder','K_big_inverse_kpc':128}}}}}}}
def write(name,obj):
 p=ROOT/name
 with p.open('x') as f:f.write(json.dumps(obj,sort_keys=True,indent=2)+'\n')
 return p
rows=[]
for kind in ['exact','low_excess','low_shortfall','top_nextup','top_nextdown','gap','overlap','missing_ranges','extra_dv','false_full','reversed_range','duplicate_shell_labels']:
 rec=copy.deepcopy(base)
 if kind=='low_excess':rec['shell_ranges_inverse_kpc']=[[3.5,top]]
 elif kind=='low_shortfall':rec['shell_ranges_inverse_kpc']=[[4.5,top]]
 elif kind=='top_nextup':rec['shell_ranges_inverse_kpc']=[[4,math.nextafter(top,math.inf)]]
 elif kind=='top_nextdown':rec['shell_ranges_inverse_kpc']=[[4,math.nextafter(top,-math.inf)]]
 elif kind in ['gap','overlap']:
  rec['shells']=['first','second'];rec['dV_static_shells_km_s']={k:[0]*12 for k in rec['shells']};rec['shell_ranges_inverse_kpc']=[[4,50],[51 if kind=='gap' else 49,top]]
 elif kind=='missing_ranges':rec['shell_ranges_inverse_kpc']=[]
 elif kind=='extra_dv':rec['dV_static_shells_km_s']['unlisted']=[0]*12
 elif kind=='false_full':rec['full_tail_domain']=False
 elif kind=='reversed_range':rec['shell_ranges_inverse_kpc']=[[top,4]]
 elif kind=='duplicate_shell_labels':rec['shells']=['owned','owned'];rec['shell_ranges_inverse_kpc']=[[4,50],[50,top]]
 p=write('rbfp_'+kind+'.json',rec)
 reg={'schema':m.PRODUCER_REGISTRY_SCHEMA,'producers':{'RB_FP':[psha]},'identity_comparators':[],'identity_tokens':{},'gate_records':{'RB_FP':[h(p.read_bytes())]},'gq_all_nodes_counts':{}}
 rp=write('rbfp_'+kind+'_registry.json',reg)
 got=m.evaluate_gate('RB_FP',p,{'producer_registry':m.load_producer_registry(rp),'case_block':cb},{'C4T':'1'*64})
 rows.append({'case':kind,'expected':'PASS' if kind=='exact' else 'RECORD_DEFECT','actual':got['status'],'codes':got['codes'],'record':str(p),'sha256':h(p.read_bytes()),'registry':str(rp),'registry_sha256':h(rp.read_bytes())})
result={'date_u':os.environ['UNT_CX2_PACKET_UTC'],'source_sha256_before':h(raw),'source_sha256_after':h(SRC.read_bytes()),'scope':'Owned synthetic RB_FP gate records and context only; no production evidence or launches.','checks':rows,'pass':all(x['expected']==x['actual'] for x in rows)}
p=write('RB_FP_RANGES_RESULTS_CX2V001.json',result)
print(json.dumps({'path':str(p),'sha256':h(p.read_bytes()),'pass':result['pass'],'checks':len(rows)}))
