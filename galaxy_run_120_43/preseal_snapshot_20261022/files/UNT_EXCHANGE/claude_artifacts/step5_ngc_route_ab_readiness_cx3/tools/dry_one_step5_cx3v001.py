"""One isolated direct cmd_dry_run call; subprocess/network/scientific execution denied."""
import contextlib, hashlib, io, json, os, resource, runpy, sys, time, traceback, datetime
from pathlib import Path

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wx(p,o):
    with Path(p).open('x') as f: json.dump(o,f,indent=1,sort_keys=True,allow_nan=False);f.write('\n')

driver,expected,spec,spec_sha,rd,logp=sys.argv[1:7]
assert sha(driver)==expected and sha(spec)==spec_sha
assert not Path(rd).exists() and not Path(logp).exists()
try:
    resource.setrlimit(resource.RLIMIT_AS,(7*1024**3,7*1024**3))
    memory_limit_note='7 GiB RLIMIT_AS accepted'
except (ValueError,OSError) as e:
    memory_limit_note='Host rejected RLIMIT_AS: '+str(e)+'; measured RSS checked during calls and at completion'
roots=[Path(rd).resolve(),Path(logp).resolve()]
reads=set();writes=[];blocked=[];calls=[];modes=[]
def prohibited(p):
    s=str(p).lower()
    if '/runs_ext/uvt_' in s or 'kmax_a2f10_c5h_run_v001' in s or '/.codex/' in s:return True
    if 'ngc3198' in s:
        s=s.replace('target_free','').replace('target-free','')
        if any(t in s for t in ('observed','rotmod','velocit','target')):return True
    return False
def deny(s):
    blocked.append(s);raise RuntimeError('CX3_DRY_GUARD '+s)
def inside(p):return any(p==r or r in p.parents for r in roots)
def audit(event,args):
    if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn','os.fork','os.forkpty','os.exec','pty.spawn','os.kill','os.killpg','webbrowser.open'):
        deny(event)
    if event in ('os.remove','os.unlink','os.rmdir','os.rename','os.replace','shutil.rmtree','os.truncate','shutil.move'):deny(event)
    if event=='import' and args and str(args[0]).split('.')[0] in ('scipy','pandas','requests'):deny('non-numpy third-party import '+str(args[0]))
    if event in ('os.listdir','os.scandir','os.mkdir','open') and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.path.abspath(os.fsdecode(args[0])));rp=p.resolve()
        if prohibited(p) or prohibited(rp):deny('prohibited path '+str(p))
        if event=='os.mkdir' and not inside(rp):deny('mkdir outside outputs '+str(p))
        if event=='open':
            mode=args[1] if len(args)>1 else 'r';flags=args[2] if len(args)>2 else 0
            writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
            if writing:
                if not inside(rp):deny('write outside outputs '+str(p))
                if rp.exists():deny('overwrite '+str(p))
                writes.append(str(rp))
            else:reads.add(str(rp))
def profile(frame,event,arg):
    if event=='call' and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=7*1024**3:deny('RSS exceeds 7 GiB')
    if event!='call' or frame.f_code.co_filename!=driver:return
    name=frame.f_code.co_name
    if name in ('stage_main','cmd_run','_cmd_run_ngc_cx3v005'):deny('scientific entry '+name)
    if name=='__init__' and 'mode' in frame.f_locals and type(frame.f_locals.get('self')).__name__=='Ctx':
        modes.append(frame.f_locals['mode'])
        if frame.f_locals['mode']!='simulate':deny('non-simulate Ctx')
    if name=='ro1_outcome':calls.append({'line':frame.f_code.co_firstlineno,'ngc_active':frame.f_globals.get('_NGC_V011_ACTIVE')})
sys.addaudithook(audit);sys.setprofile(profile)
out,err=io.StringIO(),io.StringIO();code=None;exception=None;tb=None;frames=[]
t0=time.monotonic()
try:
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        m=runpy.run_path(driver,run_name='cx3_dry_review')
        code=m['cmd_dry_run'](spec,rd)
except BaseException as e:
    code='EXCEPTION';exception=type(e).__name__+': '+str(e);tb=traceback.format_exc()
    frames=[{'file':f.filename,'function':f.name,'line':f.lineno,'source_line':f.line} for f in traceback.extract_tb(e.__traceback__)]
finally:sys.setprofile(None)
rec={'schema':'CX3_R007_DRY_ONE_V001','memory_limit_note':memory_limit_note,'date_u':datetime.datetime.now(datetime.timezone.utc).strftime('%a %b %d %H:%M:%S UTC %Y'),'driver':driver,'driver_sha256':expected,'spec':spec,'spec_sha256':spec_sha,'report_dir':rd,'exit':code,'exception':exception,'traceback':tb,'traceback_frames':frames,'stdout':out.getvalue(),'stderr':err.getvalue(),'elapsed_s':time.monotonic()-t0,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'ro1_calls':calls,'ctx_modes':modes,'opened_read':sorted(reads),'opened_write':writes,'blocked':blocked}
assert rec['peak_rss_bytes']<8*1024**3
wx(logp,rec)
