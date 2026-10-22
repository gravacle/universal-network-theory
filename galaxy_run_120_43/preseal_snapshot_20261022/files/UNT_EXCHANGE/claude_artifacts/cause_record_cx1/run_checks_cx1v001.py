from pathlib import Path
import subprocess,sys,json,hashlib
D=Path(__file__).parent
src=(D/'metadata_selector_cx1v001.py').read_text()
mutations={
 'M01_forbidden_access':("if not requested<=ALLOWED[self.kind]:raise Refused('FORBIDDEN_KEY_ACCESS')",'if False:raise Refused(\'FORBIDDEN_KEY_ACCESS\')'),
 'M02_duplicate_keys':("if key in seen:raise Refused('DUPLICATE_KEY')","if False:raise Refused('DUPLICATE_KEY')"),
 'M03_pin_check':("digest!=want_sha","False"),
 'M04_skip_decodes_value':('v=self.string(wanted)','v=self.string(True)'),
}
r=subprocess.run([sys.executable,'-I','-B',str(D/'test_metadata_selector_cx1v001.py')],capture_output=True,text=True)
assert r.returncode==0
with (D/'READER_TESTS_CX1V001.json').open('x') as f:f.write(r.stdout)
results=[]
for name,(a,b) in mutations.items():
 assert src.count(a)==1
 p=D/(name+'.py');p.open('x').write(src.replace(a,b))
 run=subprocess.run([sys.executable,'-I','-B',str(D/'test_metadata_selector_cx1v001.py'),str(p)],capture_output=True,text=True)
 obj=json.loads(run.stdout);failed=[x['name'] for x in obj['tests'] if not x['pass']]
 assert run.returncode==1 and failed
 results.append({'mutant':name,'killed':True,'failing_tests':failed,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with (D/'READER_MUTANTS_CX1V001.json').open('x') as f:json.dump(results,f,indent=2);f.write('\n')
print(json.dumps(results,indent=2))
