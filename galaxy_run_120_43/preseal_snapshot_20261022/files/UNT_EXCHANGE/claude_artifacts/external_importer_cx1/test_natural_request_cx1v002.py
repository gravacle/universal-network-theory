"""Committed natural-plan selector tested on existing inert admission fixture setup."""
from pathlib import Path
import types,json,hashlib,fcntl,os
from natural_request_cx1v001 import select
from snapshot_cx1v001 import Snapshot,Refusal
b=Path(__file__).resolve().parent;fixture=b/'test_valid_admission_cx1v003.py'
exec(compile(fixture.read_text().split('passed=[]')[0],str(fixture),'exec'),globals())
ctx.mapper=types.SimpleNamespace(build=lambda theta:mapped)
pp={'path':str(wd/'WAVE_PLAN.json'),'sha256':hashlib.sha256((wd/'WAVE_PLAN.json').read_bytes()).hexdigest()}
args=dict(ctx=ctx,lock=lock,wave=1,call_index=0,plan_pin=pp,theta_key=G.digest);passed=[]
def refuse(name,**changes):
 try:select(Snapshot(),**dict(args,**changes))
 except Refusal:passed.append(name)
 else:raise AssertionError(name)
try:
 got=select(Snapshot(),**args);assert got['key']==key and got['spec_sha256']==sp['sha256'];passed.append('committed plan and actual mapper fixture selected without candidate evidence')
 refuse('unrequested index',call_index=99)
 refuse('foreign plan location',plan_pin=dict(pp,path=str(case/'uncommitted.json')))
 refuse('wrong wave',wave=2)
 lock.held=False;refuse('unheld lock');lock.held=True
 ctx.mapper=types.SimpleNamespace(build=lambda theta:dict(mapped,raw=b'{}'))
 refuse('mapper byte mismatch')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r=dict(status='PASS',blocking_count=0,tested=passed,untested=['Joint root observer wiring','Production mapper','Concurrent plan mutation after selection'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [Path(__file__),Path(__file__).resolve().parent/'natural_request_cx1v001.py',fixture]])
p=case/'NATURAL_REQUEST_REPORT.json'
with p.open('x') as f:json.dump(r,f,indent=2)
print(p)
