from pathlib import Path
import subprocess,sys,json,hashlib
p=Path(__file__).parent
r=subprocess.run([sys.executable,str(p/'test_cause_cxv002.py')],capture_output=True,text=True);assert r.returncode==0,r.stderr
with (p/'CAUSE_TESTS_CXV002.json').open('x') as f:f.write(r.stdout)
src=(p/'cause_record_cxv002.py').read_text();rows=[]
mutations=[('finish_association',"if fin.get(('result_path',))!=rp or fin.get(('result_sha256',))!=rh or fin.get(('status',))!=status:","if False:"),('all_to_any',"all(s.get('model_outcome') is True for s in found)","any(s.get('model_outcome') is True for s in found)"),('empty_allowed',"if not found or not all(s.get('model_outcome') is True for s in found):","if not all(s.get('model_outcome') is True for s in found):"),('ngc_gate',"if lane=='NGC':","if False:"),('generic_exhaustion',"if status != 'ROUTE_A_NO_FIXED_POINT':","if status not in ('FAILED','ROUTE_A_NO_FIXED_POINT'):"),('solo',"s.get(('solo_mode',)) is not True","False"),('module_pin',"reader.read(module['path'],module['sha256'])","reader.read(module['path'],None)")]
for i,(name,old,new) in enumerate(mutations,1):
 assert src.count(old)==1
 target=p/('CXV002_MUTANT_M%02d.py'%i)
 with target.open('x') as f:f.write(src.replace(old,new))
 out=subprocess.run([sys.executable,str(p/'test_cause_cxv002.py'),str(target)],capture_output=True,text=True)
 rows.append({'name':name,'killed':out.returncode!=0,'returncode':out.returncode,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'failure':out.stderr.splitlines()[-1] if out.stderr else ''})
assert all(r['killed'] for r in rows)
with (p/'CAUSE_MUTANTS_CXV002.json').open('x') as f:json.dump(rows,f,indent=2)
print(json.dumps({'tests':43,'mutants_killed':len(rows)}))
