import ast,contextlib,hashlib,io,json,os,runpy,sys
from pathlib import Path
H=Path(__file__).parent;B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts');P=B/'b1_policy_successor_c4/tools/make_b1_cascade_c4v002.py'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='a7a5fe58d509b99f14cb000305633c6f192ac71f5093f4ec5fa1a2fa6f1a1f35'
def audit(ev,args):
 if ev in ('subprocess.Popen','os.system','os.fork','os.posix_spawn','socket.connect','socket.bind','os.remove','os.rmdir','os.rename','os.symlink'):raise PermissionError(ev)
 if ev=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  path=Path(os.fsdecode(args[0])).absolute();parts=[x.casefold() for x in path.parts]
  if any(x.startswith('uvt_') or x=='kmax_a2f10_c5h_run_v001' for x in parts):raise PermissionError('protected')
  mode,flags=args[1:];writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
  if writing and not path.is_relative_to(H):raise PermissionError('write outside fixture root')
 if ev=='os.mkdir' and not Path(args[0]).absolute().is_relative_to(H):raise PermissionError('mkdir outside fixture root')
sys.addaudithook(audit)
checks=[]
def invoke(name,args,expected=0):
 buf=io.StringIO();err=io.StringIO();old=sys.argv;sys.argv=[str(P),*map(str,args)];rc=0
 try:
  with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(err):runpy.run_path(str(P),run_name='__main__')
 except SystemExit as e:rc=e.code
 except FileExistsError:rc='exists'
 finally:sys.argv=old
 assert rc==expected,(name,rc,err.getvalue())
 checks.append({'name':name,'passed':True,'return':rc,'detail':err.getvalue().strip()})
 return json.loads(buf.getvalue()) if buf.getvalue() else None
base=[H,'v006r10_c4','--dry-run'];r=invoke('trio_regression',base)
for name,h in r['outputs'].items():assert hashlib.sha256((B/'calib_tail_readiness_cx2/v006r10_c4'/name).read_bytes()).hexdigest()==h
T=['a99105a19b582c68d961e0ee12be3a2efa79dbd1e65d63682c3d2d8daa55f0ab','b2989012c92161a7da3dd10d0148e1607422416d369fc4ebe164217758b5c695','c01b3c51e34501d77e474594cc0b4be72c6e068c7f58a595055316313a8d4bb1','UNT_KMAX_TAIL_COMPARISON_C2V007_R11','0'*64]
args=[H,'v006r11_c4','--write','--policy-only','--seal-tuple',*T]
r=invoke('policy_only_inert_verdict',args);assert len(r['outputs'])==1
q=H/'v006r11_c4/adoption_policy_cx2v006r11_c4.py';old=B/'calib_tail_readiness_cx2/v006r10_c4/adoption_policy_cx2v006r10_c4.py'
a,b=old.read_text().splitlines(),q.read_text().splitlines();assert len(a)==len(b)
diffs=[(x,y) for x,y in zip(a,b) if x!=y];assert len(diffs)==2
assert any(y=='APPROVED_V007_SEALS = frozenset({'+repr(tuple(T))+'})' for x,y in diffs)
invoke('occupied_output_preserved',args,'exists')
for i in range(5):
 bad=T.copy();bad[i]='F'*64 if i==4 else ('wrong_schema' if i==3 else 'f'*64)
 invoke('bad_tuple_'+str(i),[H,'v006r12_c4','--dry-run','--policy-only','--seal-tuple',*bad],2)
invoke('bad_sub',[H,'../escape','--dry-run'],2)
invoke('short_args',[H],2)
assert not (H/'v006r12_c4').exists()
rec={'checks':checks,'passed':len(checks),'total':len(checks),'generator_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'synthetic_policy_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'diffs':diffs,'scope':'Inert verdict tuple; generator only. No finalized production policy or comparator execution.'}
with (H/'RESULT.json').open('x') as f:json.dump(rec,f,indent=2)
print(json.dumps({'passed':len(checks),'total':len(checks),'diff_count':len(diffs)}))
