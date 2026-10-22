"""Actual admission through hook with real certificate/guard/monitor; parent/scheduler/context doubles."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
fixture=root/'test_valid_admission_cx1v003.py'
prefix=fixture.read_text().split('passed=[]',1)[0]
exec(compile(prefix,str(fixture),'exec'),globals())
import executor_hook_cx1v002 as H
base=types.ModuleType('inert_campaign')
base.run_campaign=lambda **kw: (_ for _ in ()).throw(AssertionError('unexpected local solve'))
ctx.C=base
class Parent:
 def __init__(self):self.ctx=ctx
 def execute(self,wave_dir,plan,resume,log):return self.ctx.C.run_campaign()
 def classify(self,c,record):return classify(c,record)
class Scheduler:
 @staticmethod
 def run_campaign(_admitted_external,**kw):return [dict(_admitted_external[0])],{'inert':True}
e=H.make_executor_type(Parent,Scheduler)()
e._external_orch=orch;e._external_lock=lambda:lock;e._external_modules=mods
e._external_candidates=[candidate];orch.executor=e
passed=[]
try:
 records,meta=e.execute(wd,plan,False,None)
 assert len(records)==1 and records[0]['call_dir']==str(call)
 assert records[0]['execution_origin']=='DIRECT_EXTERNAL' and meta['external_import_count']==1
 assert ctx.C is base and not (wd/'campaign').exists() and not orch.cache.entries
 passed.append('hook executes actual direct-layout admission and preserves original call directory without local solve')
 result_class=e.classify(plan_call,records[0])
 assert result_class[0]=='VALID' and result_class[3]['external_admission']['candidate']['case']=='seed'
 assert not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('ingest repeats real admission without classifier recursion and restores explicit-spec resolver')
 orch.check_identity_now=lambda:['INERT changed identity']
 try:e.classify(plan_call,records[0])
 except Refusal as ex:assert 'WORK_IDENTITY_CHANGED' in str(ex)
 else:raise AssertionError('stale identity accepted')
 orch.check_identity_now=lambda:[]
 passed.append('fresh ingest admission refuses identity change after selection')
 bad=put(case/'negative_after_selection.json',dict(acceptance,reading='NON_LAPSE_TAIL_MATERIAL'))
 e._external_selected[0]['acceptance']=bad
 try:e.classify(plan_call,records[0])
 except Refusal:pass
 else:raise AssertionError('negative acceptance accepted')
 assert not orch.cache.entries and ctx.C is base and not hasattr(ctx,'_cx1_original_spec_path')
 passed.append('negative acceptance at ingest refuses without cache writes or invalid classification')
finally:
 fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
files=[Path(__file__),fixture,root/'executor_hook_cx1v002.py',root/'valid_admission_cx1v002.py',root/'test_wrapper_certificate_snapshot_cx1v001.py']
r=dict(status='PASS',blocking_count=0,scope=__doc__,tested=passed,untested=['Actual parent executor and scheduler','Production context, mapper, identity and policy checks','Runtime/register/envelope/wait','Cache write and subsequent cache validation'],pins=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
p=case/'HOOK_ADMISSION_TEST_REPORT.json'
with p.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print(p)
