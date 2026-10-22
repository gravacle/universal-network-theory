import json,hashlib,subprocess,sys,tempfile,os
from pathlib import Path
b=Path(__file__).resolve().parent;entry=b/'runtime_capture_entry_cx1v003.py'
c=Path(tempfile.mkdtemp(prefix='capture_preflight_',dir=b/'inert_fixtures'))
base=dict(schema='CX1_RUNTIME_INVENTORY_V001',module_names=['numpy','scipy'],unresolved_dynamic=[],audit_complete=True);passed=[]
def run(label,raw,flags=('-I','-B'),sha=None,ok=False):
 p=c/(label+'.json')
 with p.open('xb') as f:f.write(raw)
 r=subprocess.run([sys.executable,*flags,str(entry),'--inventory',str(p),'--inventory-sha256',sha or hashlib.sha256(raw).hexdigest(),'--validate-only'],capture_output=True,text=True,env={k:v for k,v in os.environ.items() if not k.startswith(('PYTHON','DYLD'))})
 assert (r.returncode==0)==ok,(label,r.returncode)
 passed.append(label)
run('valid_contract_no_capture',json.dumps(base).encode(),ok=True)
run('hash_mismatch',json.dumps(base).encode(),sha='0'*64)
run('unresolved_dynamic',json.dumps({**base,'unresolved_dynamic':['loader']}).encode())
run('audit_missing',json.dumps({k:v for k,v in base.items() if k!='audit_complete'}).encode())
run('duplicate_key',b'{"schema":1,"schema":2}')
run('nonfinite',b'{"schema":NaN}')
run('overflow',b'{"schema":1e999}')
run('no_isolation',json.dumps(base).encode(),flags=('-B',))
run('missing_scipy',json.dumps({**base,'module_names':['numpy']}).encode())
run('duplicate_module',json.dumps({**base,'module_names':['numpy','scipy','numpy']}).encode())
r=dict(status='PASS',blocking_count=0,tested=passed,scope='Isolated subprocess preflight only; inert JSON fixtures',untested=['Real runtime capture','Bytecode-enabled CLI rejection: host defaults bytecode disabled'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [entry,Path(__file__)]])
with (c/'TEST_REPORT.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(c/'TEST_REPORT.json')
