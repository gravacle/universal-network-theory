import json,types,fcntl,os
from pathlib import Path
from direct_handoff_writer_cx1v001 import write_handoff
from snapshot_cx1v001 import Refusal
helper=Path(__file__).parent/'test_valid_admission_cx1v003.py'
prefix=helper.read_text().split('passed=[]')[0]
prefix=prefix.replace("exec(compile(text,str(helper),'exec'),globals())", 'text=chr(10).join(line for line in text.splitlines() if not line.startswith("put(call/\'TAIL_CERTIFICATE_ACCEPTANCE.json\'"))\nexec(compile(text,str(helper),\'exec\'),globals())')
exec(compile(prefix,str(helper),'exec'),globals())
ctx.certificate_check=types.MethodType(W.certificate_check,ctx)
args=dict(lock=lock,chain_modules=mods,wrapper_module=W,call=plan_call,candidate=candidate)
checks=[]
try:
 target=call/'TAIL_CERTIFICATE_ACCEPTANCE.json';assert not target.exists()
 badacc=put(case/'writer_bad_acceptance.json',dict(acceptance,reading='INCOMPLETE'))
 try:write_handoff(orch,**{**args,'candidate':{**candidate,'acceptance':badacc}});raise AssertionError('bad acceptance')
 except Refusal:pass
 assert not target.exists();checks.append('failed acceptance leaves no handoff')
 got=write_handoff(orch,**args);assert got['created']
 saved=json.loads(target.read_bytes());assert saved['writer']['path'].endswith('direct_handoff_writer_cx1v001.py')
 assert saved['checker_adapter']['path'].endswith('certificate_spec_adapter_cx1v001.py')
 checks.append('exclusive write and fresh verification with truthful producer pins')
 before=target.stat();again=write_handoff(orch,**args);after=target.stat()
 assert not again['created'] and before.st_ino==after.st_ino and before.st_mtime_ns==after.st_mtime_ns
 checks.append('idempotent same handoff is not rewritten')
 assert not hasattr(ctx,'_cx1_original_spec_path');checks.append('resolver restored')
 lock.held=False
 try:write_handoff(orch,**args);raise AssertionError('unheld')
 except Refusal:pass
 lock.held=True;checks.append('unheld lock refuses')
finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
r={'status':'PASS','blocking_count':0,'scope':'Inert direct handoff writer with real certificate guard and synthetic Context/taxonomy','tested':checks,'untested':['Production acceptance entry','Root register and runtime authentication','Full Context/mapper','Concurrent external mutation races','Whole-engine integration']}
p=case/'WRITER_TEST_REPORT.json';p.write_text(json.dumps(r,indent=2)+'\n');print(p)
