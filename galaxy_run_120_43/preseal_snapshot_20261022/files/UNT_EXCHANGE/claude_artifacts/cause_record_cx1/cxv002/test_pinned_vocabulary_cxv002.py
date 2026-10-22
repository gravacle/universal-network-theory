import importlib.util,json,hashlib,tempfile,sys
from pathlib import Path
p=Path(__file__).parent;s=importlib.util.spec_from_file_location('cause',p/'cause_record_cxv002.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
root=Path(tempfile.mkdtemp(prefix='cx1_A252_inert_'));n=0;rows=[]
def put(obj):
 global n
 n+=1;f=root/(str(n)+'.json');raw=json.dumps(obj).encode()
 with f.open('xb') as out:out.write(raw)
 return str(f),hashlib.sha256(raw).hexdigest()
for dh,reg in m.VOCABULARIES.items():
 for token in sorted(m.TOKENS):
  result=put({'status':'ROUTE_A_NO_FIXED_POINT','route_a_outcome':{'outcome':token},'stage_records':[{'name':'route_a','exit_code':0}]})
  rec=put({'status':'CHILD_FAILED','driver_status':'ROUTE_A_NO_FIXED_POINT','exit_code':3,'stop_reason':None,'result':{'path':result[0],'sha256':result[1]},'pins':{'spec':{'sha256':'a'*64},'driver':{'path':reg['root'],'sha256':dh}}})
  fin=put({'status':'ROUTE_A_NO_FIXED_POINT','result_path':result[0],'result_sha256':result[1]})
  att=put({'status':'POST_SEAL_ATTESTED','authority':'Claude2','receipt_sha256':rec[1],'driver_sha256':dh,'spec_sha256':'a'*64})
  out=m.classify(rec,fin[0],post_seal=att);assert out['model_outcome'],out['model_outcome_reason']
  rows.append({'driver_sha256':dh,'token':token,'pass':True,'sites':len(json.loads(out['raise_site'].split(':',1)[1])),'modules_verified':len(reg['modules'])})
print(json.dumps({'scope':'inert receipt/result/finish/attestation; actual pinned source bytes only, never executed','cases':rows,'fixture_dir':str(root)}))
