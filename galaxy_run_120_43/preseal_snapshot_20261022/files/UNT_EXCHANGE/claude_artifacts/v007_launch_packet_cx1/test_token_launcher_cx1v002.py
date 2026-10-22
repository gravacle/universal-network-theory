"""Synthetic scheduler simulation only. Popen replaced; no real subprocess or scientific run."""
import contextlib,hashlib,importlib.util,io,json
from pathlib import Path
R=Path(__file__).parent;p=R/'route_a_token_launcher_cx1v001.py'
s=importlib.util.spec_from_file_location('launcher',p);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
root=R/'TOKEN_LAUNCHER_SYNTH_V001';root.mkdir();checks=[]
for failed in (False,True):
 d=root/('failure' if failed else 'success');d.mkdir();clock=[0.];procs=[];peak=[0];overlap=[0]
 class Proc:
  def __init__(self,args):
   self.out=Path(args[args.index('--outdir')+1]);self.receipt=Path(args[args.index('--receipt')+1]);self.out.mkdir();self.start=clock[0];self.pid=100+len(procs);self.fail=failed and not procs;self.a=self.start+10;self.end=self.start+(1 if self.fail else 100)
  def poll(self):return (1 if self.fail else 0) if clock[0]>=self.end else None
 def tick(seconds):
  clock[0]+=seconds
  for x in procs:
   progress=x.out/'progress.jsonl'
   if clock[0]>=x.a and not progress.exists():progress.write_text('{"stage":"route_a","event":"finished"}\n')
   if x.poll() is not None and not x.receipt.exists():x.receipt.write_text(json.dumps({'status':'FAILED' if x.fail else 'FINISHED'}))
 def popen(args,**kw):
  assert kw['start_new_session'] is True and args[0]=='/usr/bin/nohup'
  x=Proc(args);procs.append(x);alive=[q for q in procs if q.poll() is None];peak[0]=max(peak[0],sum(clock[0]<q.a for q in alive));overlap[0]=max(overlap[0],len(alive));return x
 M.time.sleep=tick;M.subprocess.Popen=popen
 calls=[]
 for i in range(10):
  out=d/str(i);receipt=d/(str(i)+'.receipt.json');calls.append({'case':str(i),'outdir':str(out),'receipt':str(receipt),'monitor_log':str(d/(str(i)+'.log')),'monitor_argv':['fake','--outdir',str(out),'--receipt',str(receipt)]})
 with contextlib.redirect_stdout(io.StringIO()):rc=M.worker({'calls':calls})
 checks.append({'scenario':d.name,'max_route_a':peak[0],'max_live_monitors':overlap[0],'starts':len(procs),'exit':rc,'passed':peak[0]<=3 and (len(procs)<=3 and rc==1 if failed else len(procs)==10 and rc==0 and overlap[0]>3)})
partial=root/'partial.jsonl';partial.write_text('{"stage":"route_a","event":"finished"}')
checks.append({'scenario':'partial_line_no_token_release','passed':M.ra_finished(partial) is False})
wrong=root/'wrong.jsonl';wrong.write_text('{"stage":"offset","event":"finished"}\n')
checks.append({'scenario':'wrong_stage_no_token_release','passed':M.ra_finished(wrong) is False})
with (R/'TOKEN_LAUNCHER_TESTS_V001.json').open('x') as f:json.dump({'label':'TESTED synthetic simulation; all process creation mocked','launcher_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tests':checks},f,indent=1)
print(checks);assert all(x['passed'] for x in checks)
