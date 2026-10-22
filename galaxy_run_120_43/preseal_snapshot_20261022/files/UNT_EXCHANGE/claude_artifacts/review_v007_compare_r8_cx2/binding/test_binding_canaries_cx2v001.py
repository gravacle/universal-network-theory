from pathlib import Path
import os, sys, json, hashlib, types, copy, math
ROOT=Path(__file__).resolve().parent
SRC=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/v007_compare_c2/r8/kmax_tail_compare_c2v007_r8.py')
PIN='bd51db152f700afd86c2156904a4998b4582deeac5c06d05def50b27b397e5c3'
def sha(b): return hashlib.sha256(b).hexdigest()
def write(name,obj):
 p=ROOT/name
 with p.open('x') as f: f.write(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')
 return p
raw=SRC.read_bytes(); assert sha(raw)==PIN
# Only source import; never call build_context or the provided test suite.
import numpy
allowed=(str(ROOT),str(SRC),sys.base_prefix,'/System/Library/','/usr/share/zoneinfo/','/etc/localtime','/private/var/db/timezone/')
reads=[]
def audit(event,args):
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  q=os.fsdecode(args[0]); mode=args[1]; flags=args[2]
  if '/runs/' in q or '/runs_ext/' in q: raise RuntimeError('DENIED_PRODUCTION_RUN_READ')
  if not any(q.startswith(x) for x in allowed): raise RuntimeError('DENIED_UNREGISTERED_READ')
  reads.append(q)
sys.addaudithook(audit)
m=types.ModuleType('cx2_r8_binding');m.__file__=str(SRC);exec(compile(raw,str(SRC),'exec'),m.__dict__)
producer=ROOT/'owned_synthetic_producer.py'
with producer.open('x') as f:f.write('# synthetic inert producer, never executed\n')
psha=sha(producer.read_bytes())
basecb={'cases':{k:{'normalized_spec_equal':{'/numerics':{'uv_tail':{'outer':{'shape':'cylinder','K_big_inverse_kpc':128.0},'gas':{'M_s':128}}}}} for k in ['C4T','C2T','C3T']}}
base_lo={'schema':m.GATE_SCHEMA,'gate':'LO','producer':{'path':str(producer),'sha256':psha},'verdict':'PASS','state_result_sha256':m.PIN_R3['C4R3'][1],'source_gas_M_s':128,'summed_max_over_tau':0.001,'shells':[{'range_inverse_kpc':[a,b],'max_over_tau':0.0001} for a,b in [(4,5),(5,6),(6,8),(8,12),(12,16),(16,32),(32,64),(64,128),(128,256),(256,363)]]}
base_b2={'schema':m.GATE_SCHEMA,'gate':'B2','producer':{'path':str(producer),'sha256':psha},'verdict':'PASS','O_cube_K_out_inverse_kpc':12,'azimuths':16,'per_state':{k:{'state_result_sha256':m.PIN_R3[k][1],'max_row_diff_km_s':0,'sanity_vs_KB12_km_s':0} for k in ['C2R3','C3R3','C4R3']}}
results=[]
def case(name,rec,expected,cb=None,reason='',afterseal=False):
 gate=rec['gate'];p=write(name+'.json',rec);sh=sha(p.read_bytes())
 reg={'schema':m.PRODUCER_REGISTRY_SCHEMA,'producers':{gate:[psha]},'identity_comparators':[],'identity_tokens':{},'gate_records':{gate:m.GATE_RECORD_AFTER_SEAL if afterseal else [sh]},'gq_all_nodes_counts':{}}
 rp=write(name+'_registry.json',reg)
 ctx={'case_block':copy.deepcopy(cb or basecb),'producer_registry':m.load_producer_registry(rp)}
 got=m.evaluate_gate(gate,p,ctx)
 results.append({'name':name,'expected':expected,'actual':got['status'],'matched':got['status'] in expected,'codes':got['codes'],'reason':reason,'record_sha256':sh,'registry_sha256':sha(rp.read_bytes()),'record_path':str(p),'registry_path':str(rp)})
case('lo_baseline',copy.deepcopy(base_lo),['PASS'])
a=copy.deepcopy(base_lo);a['shells'][0]['max_over_tau']=0.1
case('lo_single_failing_shell',a,['RECORD_DEFECT','FAIL'],'',reason='A54 S5: passing verdict contradicts measured shell >0.005')
a=copy.deepcopy(base_lo);a['shells'].insert(0,{'range_inverse_kpc':[4,5],'max_over_tau':0.1})
case('lo_failing_duplicate_first',a,['RECORD_DEFECT','FAIL'],reason='Every shell <=0.005; first duplicate violates this')
a=copy.deepcopy(base_lo);a['shells'].append({'range_inverse_kpc':[4,5],'max_over_tau':0.1})
case('lo_failing_duplicate_last',a,['RECORD_DEFECT','FAIL'],reason='Same data multiset as preceding case, changed order only')
a=copy.deepcopy(base_lo);a['shells'].append({'range_inverse_kpc':[363,370],'max_over_tau':0.1});a['shells'].append({'range_inverse_kpc':[363,370],'max_over_tau':0.0001})
case('lo_extended_failing_duplicate_first',a,['RECORD_DEFECT','FAIL'],reason='Extended shell violates same 0.005 threshold but overwritten')
a=copy.deepcopy(base_lo);a['shells'][0]['max_over_tau']=0.1;a['verdict']='FAIL'
case('lo_failing_verdict_control',a,['FAIL'])
a=copy.deepcopy(base_lo);a['source_gas_M_s']=64
case('lo_ms64_rejected',a,['RECORD_DEFECT'])
a=copy.deepcopy(base_lo);a.pop('source_gas_M_s')
case('lo_ms_missing_rejected',a,['RECORD_DEFECT'])
a=copy.deepcopy(basecb);a['cases']['C4T']['normalized_spec_equal']['/numerics']['uv_tail']['gas']['M_s']=64
case('lo_direct_gate_context_ms64',copy.deepcopy(base_lo),['RECORD_DEFECT'],cb=a,reason='Deferred A68 CHK1 direct gate API; invalid case block would be rejected by normal CLI, no adoption claim')
case('b2_baseline',copy.deepcopy(base_b2),['PASS'])
a=copy.deepcopy(base_b2);a['producer']['path']=str(ROOT/'producer_path_does_not_exist.py')
case('b2_missing_producer_path',a,['RECORD_DEFECT'],reason='Deferred A69.1 producer bytes not authenticated; claimed sha is registered')
a=copy.deepcopy(base_b2);a['producer']['path']=str(ROOT/'producer_path_does_not_exist.py')
case('b2_missing_producer_afterseal',a,['RECORD_DEFECT'],reason='Same deferred A69.1 with permitted afterseal marker',afterseal=True)
case('lo_duplicate_first_afterseal',dict(copy.deepcopy(base_lo),shells=[{'range_inverse_kpc':[4,5],'max_over_tau':0.1}]+copy.deepcopy(base_lo['shells'])),['RECORD_DEFECT','FAIL'],reason='Repeat semantic defect with afterseal registry marker',afterseal=True)
assert sha(SRC.read_bytes())==PIN
out={'utc_date_u':os.environ['UNT_CX2_PACKET_UTC'],'source_path':str(SRC),'source_sha256_before':PIN,'source_sha256_after':sha(SRC.read_bytes()),'scope':'Owned synthetic records, gate API only. No scientific results; no launches; no full CLI adoption claim. nice unavailable sandbox waiver0514; single-thread BLAS.','tests':results,'checks':len(results),'matched':sum(x['matched'] for x in results),'unmatched':[x['name'] for x in results if not x['matched']],'opened_paths':sorted(set(reads))}
p=write('BINDING_CANARIES_CX2V001.json',out)
print(json.dumps({'result':str(p),'sha256':sha(p.read_bytes()),'checks':out['checks'],'matched':out['matched'],'unmatched':out['unmatched']}))
