"""Direct synthetic failures only. No driver main/stage/run, no scientific computation."""
import ast,hashlib,json,runpy,traceback,subprocess,sys,os,resource
from pathlib import Path
D=Path(__file__).parent
A=D.parents[1]
SOURCES=[(A/'ngc_ro1_strict_records_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r006.py','c2930e18eb2ba6f691dcaffffd56658143490ab366552cf90b27506a2357be49'),(A/'ngc_launch_record_strictness_cx3/implementation/galaxy_m0_forward_c2v011_cx3v005_cx3r007_cx3v004.py','e4f5864aee796febf133aa03e2bf3236a9fc566971c5d2f0f5d3e2d6b226ea69')]
date=subprocess.check_output(['date','-u'],text=True).strip()
blocked=[]
def audit(event,args):
 if event.startswith('socket.') or event in ('subprocess.Popen','os.system','os.posix_spawn','os.remove','os.rename','os.replace','os.rmdir'):raise RuntimeError('DENIED '+event)
 if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
  s=os.path.abspath(os.fsdecode(args[0]));low=s.lower()
  if '/runs_ext/uvt_' in low or 'kmax_a2f10_c5h_run_v001' in low or '/.codex/' in low:raise RuntimeError('PROTECTED')
  mode=args[1];flags=args[2]
  if (isinstance(mode,str) and any(x in mode for x in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
   if not s.startswith(str(D)+'/') or Path(s).exists():raise RuntimeError('WRITE DENIED')
sys.addaudithook(audit)
rows=[];meta=[]
for source,expected in SOURCES:
 b=source.read_bytes();assert hashlib.sha256(b).hexdigest()==expected
 m=runpy.run_path(str(source),run_name='synthetic_par_tb')
 wrapped=sorted(k for k,v in m.items() if callable(v) and hasattr(v,'_cx3r007_original'))
 meta.append({'path':str(source),'sha256':expected,'size_bytes':len(b),'wrapped_globals':wrapped,'wrapped_global_count':len(wrapped)})
 probes=[('per_call_seed',lambda:m['per_call_seed']({})),('load_galaxy_config',lambda:m['load_galaxy_config']('__SYNTHETIC_MISSING__')),('exec_verified',lambda:m['exec_verified'](D/'absent_synthetic_module.py','0'*64,'unused')),('sha256_file',lambda:m['sha256_file'](D/'absent_synthetic_sha.bin')),('verify_pin_control',lambda:m['verify_pin'](D/'absent_control.bin','0'*64,'synthetic'))]
 for name,fn in probes:
  try:fn();raise AssertionError('probe unexpectedly returned')
  except Exception as e:
   frames=[{'path':f.filename,'line':f.lineno,'function':f.name,'source':f.line} for f in traceback.extract_tb(e.__traceback__) if f.filename==str(source)]
   rows.append({'driver_sha256':expected,'probe':name,'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'driver_frames':frames})
comparisons=[]
for name in [r['probe'] for r in rows[:5]]:
 x,y=[r for r in rows if r['probe']==name]
 comparisons.append({'probe':name,'same_exception_type_and_text':(x['type'],x['message'])==(y['type'],y['message']),'extra_driver_frames':len(y['driver_frames'])-len(x['driver_frames']),'raw_traceback_bytes_equal':x['traceback']==y['traceback']})
assert all(r['same_exception_type_and_text'] for r in comparisons)
assert [r['extra_driver_frames'] for r in comparisons]==[1,1,1,1,0]
assert meta[1]['wrapped_global_count']==49
out={'date_u':date,'status':'TESTED_REPRODUCED_ROOT_DISPOSITION_REQUIRED','sources':meta,'probes':rows,'comparisons':comparisons,'scope':'Direct synthetic immediate failures. No cmd_run/stage/scientific execution. Generic FAILED result/finish consequences are static source inference, not end-to-end launch tests.','peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
p=D/'PAR_TB_REPRODUCTION_CX3V001.json'
with p.open('x') as f:json.dump(out,f,indent=1,sort_keys=True);f.write('\n')
print(json.dumps({'output':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'comparisons':comparisons,'peak_rss_bytes':out['peak_rss_bytes']}))
