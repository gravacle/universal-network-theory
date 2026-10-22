from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,resource,subprocess,time
b=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CODEX1')
x=b.parent/'helpers/admission_integration'
worker=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467/owned_L4_worm_loop_root_worker_v003.py')
pins={Path(p):s for p,s in {'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467/owned_L4_worm_loop_root_worker_v003.py': '3b408fb40791a60e8fa2e81083b0377e25ef7e076ee0d2a21f3148db14dd53f2', '/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/helpers/coefficient_method/owned_L4_admission_family_recipe_DRAFT_v001.py': '86c2ee5319dd1277c630e15ca7ab9f224027bf638a281753e68dddecf1ca6bd7', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467/owned_L4_worm_loop_recipe_v003.py': '8eb46fff1f29d83fed676f7f61b469cb53495baa62d69a1ee4cfedb68aeab8ef', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467/owned_worm_loop_whole_path_c2v001.py': '9fef6042eb1e13157d19a4d4381b4c73ef6e26d779f49ad7c477f1d44b9f470d', '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/worm_move_c2_0467/owned_worm_committed_capture_durability_v002.py': 'c0646a9380ef59d1f95732faf732243f91e850ec3b94f8d3510ccdd5602b40f9'}.items()}
RELEASE0456={'author_path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE3/0009_2026-10-16_done-0456.md', 'author_sha256': '9c493b325573e1ff5ef9fbf294e3e739fe367999069db40b585dd6970bf7e03f', 'review_path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/admission_residence_review_0457/REVIEW_0457_V001.md', 'review_sha256': '482dc9047c07be8eb111827966179f9d0dbc1c353a0a24bead1d0d05ba9908e2', 'review_return_path': '/Users/bgm/Research/UNT_EXCHANGE/FROM_CLAUDE4/0011_2026-10-16_done-0457.md', 'review_return_sha256': 'e86bf046cefb8fd9edd8ddc08bc8a7fd6dd4a8ce1d36861d0f5f5e9e58c11a4b', 'interface_path': '/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/admission_residence_0456/INTERFACE_0456_V001.md', 'interface_sha256': '337a7973f008b2846aa334dde8855106db14371d7cca5270a899a552cd517e58'}
for role in ('author','review','review_return','interface'):
 path=RELEASE0456[role+'_path'];pin=RELEASE0456[role+'_sha256']
 if not path or len(pin)!=64:raise ValueError('Missing frozen 0456/0457 release; no child launched')
 pins[Path(path)]=pin
for path,pin in pins.items():
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('Pin changed: '+str(path))
subprocess.run(['/bin/ps','-p',str(os.getpid()),'-o','rss='],check=True,capture_output=True,text=True,timeout=2)
out=b/'OWNED_L4_WORM_LOOP_RUN_V001'
out.mkdir(exist_ok=False)
python='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
cmd=[python,'-I','-B',str(worker),str(out/'result.json')]
env=dict(os.environ)
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[name]='1'
record={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Occupancy-guided long alternating-loop (worm) whole-path transport replacing the current-graph cycle slot, fixed original start roster and unchanged native target; actual response-observable mixing required.','wall_cap_seconds':4500.0,'combined_rss_cap_bytes':4294967296,'output_cap_bytes':2147483648,'command':cmd,'worker_sha256':hashlib.sha256(worker.read_bytes()).hexdigest(),'monitor_semantics':'External sampled combined RSS approximately0.1s and postrun conservative peaks, one scientific child; no automatic retry.','samples':[],'status':'STARTING'}
record['accepted_pins']={str(p):v for p,v in pins.items()}
record['root_acceptance']='Root decision A2 (ROOT_DECISIONS_A1_A2_2026-10-17_V001) selected the occupancy-guided long alternating-loop whole-path move to replace the current-graph cycle slot; seed2026101701,2chains512warmup1024measurements,5moves. Same physical target,25%occupancy/10%worm-loop/20%Birth/20%admission/25%base. Hard4500s/4GiB/output2GiB; soft4400s/3.5GiB;1.6millioncalls/2.4millionevents. Preserve old failed pilots; no tail truncation, exact restart or mixing guarantee. Durable16-row capture plus reference key, Birth census and U per row (durability V002). Exact-byte distinct review is separately required before root launch; acceptance counts alone do not establish improved response mixing.'
with (out/'stdout.txt').open('x') as so,(out/'stderr.txt').open('x') as se:
 t=time.monotonic();p=subprocess.Popen(cmd,stdout=so,stderr=se,env=env)
 record['child_pid']=p.pid
 (out/'launch.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'child_pid':p.pid,'output':str(out)}),flush=True)
 reason=None
 while p.poll() is None:
  elapsed=time.monotonic()-t
  rss=0
  try:
   raw=subprocess.run(['/bin/ps','-o','rss=','-p',str(p.pid)],capture_output=True,text=True,timeout=2)
   if raw.returncode!=0 or not raw.stdout.strip():
    if p.poll() is not None:break
    raise RuntimeError('ps returned no valid live-child RSS: '+str(raw.returncode))
   rss=int(raw.stdout.strip())*1024
   if rss<=0:
    if p.poll() is not None:break
    raise RuntimeError('nonpositive live-child RSS')
  except (ValueError,subprocess.TimeoutExpired,OSError,RuntimeError) as exc:
   if p.poll() is not None:break
   reason='MONITOR_UNAVAILABLE:'+repr(exc)
   p.kill()
   break
  wrapper=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  combined=rss+wrapper
  output_bytes=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
  record['samples'].append({'elapsed_seconds':elapsed,'child_rss_bytes':rss,'combined_rss_bytes':combined,'output_bytes':output_bytes})
  if output_bytes>record['output_cap_bytes']:reason='OUTPUT_CAP'
  elif combined>record['combined_rss_cap_bytes']:reason='MEMORY_CAP'
  elif elapsed>=record['wall_cap_seconds']:reason='WALL_CAP'
  if reason:
   if p.poll() is None:p.kill()
   break
  time.sleep(.1)
 rc=p.wait();elapsed=time.monotonic()-t
 record.update(status='FINISHED' if rc==0 else 'FAILED_OR_INCOMPLETE',exit_code=rc,elapsed_seconds=elapsed,stop_reason=reason,wrapper_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_peak_rss_bytes=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
 record['conservative_combined_peak_bytes']=record['wrapper_peak_rss_bytes']+record['child_peak_rss_bytes']
 record['postrun_memory_within_cap']=record['conservative_combined_peak_bytes']<=record['combined_rss_cap_bytes']
 record['postrun_wall_within_cap']=elapsed<=record['wall_cap_seconds']
 record['postrun_output_bytes']=sum(f.stat().st_size for f in out.rglob('*') if f.is_file())
 record['postrun_output_within_cap']=record['postrun_output_bytes']<=record['output_cap_bytes']
 if not record['postrun_memory_within_cap'] or not record['postrun_wall_within_cap'] or not record['postrun_output_within_cap']:record['status']='RESOURCE_LIMIT_EXCEEDED'
 if rc==0 and (out/'result.json').is_file():
  digest=hashlib.sha256()
  with (out/'result.json').open('rb') as source:
   for block in iter(lambda:source.read(1024*1024),b''):digest.update(block)
  record['scientific_status']='RESULT_FILE_PRESENT_STATUS_NOT_PARSED';record['scientific_result_sha256']=digest.hexdigest()
  record['result_scope']='Avoid duplicate full result materialization in monitor; actual scientific status remains in result.json.'
 else:
  record['scientific_status']='NO_COMPLETED_TRIAL_RESULT'
  record['stderr_sha256']=hashlib.sha256((out/'stderr.txt').read_bytes()).hexdigest()
 (out/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({k:v for k,v in record.items() if k not in ['samples','command']}),flush=True)
