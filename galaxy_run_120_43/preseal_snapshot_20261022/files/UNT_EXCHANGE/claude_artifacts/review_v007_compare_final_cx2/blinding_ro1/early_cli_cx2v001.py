"""Independent exact r10 argparse blinding reproduction; source + argv only."""
import contextlib, hashlib, io, json, os, sys, types
from pathlib import Path
HERE=Path(__file__).parent
SRC=HERE.parents[1]/'v007_compare_c2/r10/kmax_tail_compare_c2v007_r10.py'
EXPECTED='e801adc41462bbc9dd8e81ff915b93981c3f2ec4930cb1fb9df26a78cbe18b93'
BLOCKED=[]
def guard(p):
    if isinstance(p,(str,bytes,os.PathLike)):
        s=os.fsdecode(p).lower()
        if '/runs_ext/' in s or '/runs/' in s or 'kmax_a2f10_c5h_run' in s or '/.codex/' in s or ('ngc3198' in s and any(k in s for k in ('target','observed','rotmod'))):
            BLOCKED.append(s);raise RuntimeError('PROTECTED_PATH')
def audit(e,a):
    if e=='open':guard(a[0])
    if e.startswith(('socket.','subprocess.')) or e in ('os.remove','os.rename','os.rmdir','os.system','os.fork','os.exec','os.posix_spawn'):
        BLOCKED.append(e);raise RuntimeError('FORBIDDEN_OPERATION')
sys.addaudithook(audit)
for name in ['stat','lstat','listdir','scandir']:
    old=getattr(os,name)
    def f(p,*a,_old=old,**k):guard(p);return _old(p,*a,**k)
    setattr(os,name,f)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
raw=SRC.read_bytes();assert hashlib.sha256(raw).hexdigest()==EXPECTED
M=types.ModuleType('independent_r10_cli_early');M.__file__=str(SRC);sys.modules[M.__name__]=M
exec(compile(raw,str(SRC),'exec'),M.__dict__)
rows=[]
for mode in ['--validity-only','--gates-only']:
    for label,tail in [('unknown_flag',['--v_73.246813579']),('invalid_choice',['--route-a-mode','v_73.246813579']),('abbreviation',['--prer','v_73.246813579'])]:
        argv=[mode]+tail;o=io.StringIO();e=io.StringIO();exc=None
        try:
            with contextlib.redirect_stdout(o),contextlib.redirect_stderr(e):rc=M.main(argv)
        except BaseException as x:rc=getattr(x,'code',None);exc=type(x).__name__
        leak='73.246813579' in o.getvalue()+e.getvalue()
        rows.append({'mode':mode,'case':label,'argv':argv,'rc':rc,'exception':exc,
          'stdout':o.getvalue(),'stderr':e.getvalue(),'expected_code_only_refusal':rc==2 and not leak,
          'observed_cli_canary_leak':leak,'owning_boundary':'argparse error before _main returns; SystemExit bypasses main Exception handler'})
assert sha(SRC)==EXPECTED and not BLOCKED
out=HERE/'EARLY_CLI_RESULT_CX2V001.json'
result={'date_u':sys.argv[1],'status':'TESTED_FAIL_BLINDED_CLI_DIAGNOSTIC',
 'priority_waiver':'nice unavailable (sandbox); 0514 waiver','cases':rows,
 'leaking':sum(x['observed_cli_canary_leak'] for x in rows),'total':len(rows),
 'source_before':{'path':str(SRC),'sha256':EXPECTED},'source_after':{'path':str(SRC),'sha256':sha(SRC)},
 'harness':{'path':str(Path(__file__)),'sha256':sha(__file__)},'blocked_attempts':BLOCKED,
 'scope':'CLI-controlled text leaks, not a record-derived leak. Actual main called with guarded source-byte import. No test seam, record, production path, target or scientific computation used. No supplied tests imported.',
 'source_sites':{'parser':'5092; 5112','catch_boundary':'5079-5085'}}
with out.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'result':{'path':str(out),'sha256':sha(out)},'harness':result['harness'],'leaks':result['leaking'],'total':len(rows)}))
