"""0538: propose three route-A tokens; no launch. --template-only writes cost preview only."""
import hashlib,json,math,shlex,sys
from pathlib import Path
R=Path(__file__).parent;A=R.parent
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
MON=A/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
EXT=Path('/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,o):
 with p.open('x') as f:json.dump(o,f,indent=1);f.write('\n')
def main():
 preview=sys.argv[1:]==['--template-only'];assert preview or len(sys.argv)==1
 rp=R/('SPEC_TEMPLATES_MS128_CX1V003.json' if preview else 'SPEC_REGISTRY_R5_MS128_CX1V004.json');reg=json.loads(rp.read_bytes())
 cp=A/'calib_tail_readiness_cx2/certificate_analysis/COST_MODEL_CX2V001.json';cost=json.loads(cp.read_bytes())
 order=['C6T','C4T','C4T-D5','S4T','C4T-A','C4T-KHI','C3T','C2T','C4T-KLO','C4T-C5c'];ents={x['case']:x for x in reg['specs']};assert set(ents)==set(order)
 rows=[];commands=[];cases={}
 for i,case in enumerate(order):
  ref=ents[case]['template' if preview else 'filled'];p=Path(ref['path']);assert pin(p)==ref;sp=json.loads(p.read_bytes());uv=sp['numerics']['uv_tail'];assert uv['gas']['M_s']==128
  K={'C4T-KLO':64,'C4T-KHI':256,'C4T-C5c':5}.get(case,128);assert uv['outer'].get('K_big_inverse_kpc',uv['outer'].get('K_out_inverse_kpc'))==K
  timing=cost['timings'][str(min(128,max(64,K)))];factor=max(1.,(K/128)**2)*2.
  n=(sp['numerics']['composite_grid_spec'] or {'total_axis_nodes':72})['total_axis_nodes']
  kept=max(1.8,4.7*(n/108)**3);tail=factor*(timing['route_A_cold_s']+32*timing['route_A_warm_s']+32*timing['route_B_rotation_cold_s'])/3600;solo=kept+tail
  #0538 wall cutoff about2x solo scenario; concurrency uses progress tokens.
  wall=max(14 if n<=108 else 19,math.ceil(2*solo))
  measured={'C2T':1.5,'C6T':19.7}.get(case,3.0);tail_gb=8 if K==256 else 4
  rss={'C6T':39,'C4T-KHI':44,'C3T':24,'C2T':21,'C4T-KLO':21,'C4T-C5c':16}.get(case,28)*2**30;disk=(96 if n<=108 else 128)*2**30
  out=EXT/f'KMAX_V007_P128_{case.replace("-","_")}_MS128_CX1_RUN_V005';cases[case]=str(out)
  row={'case':case,'start_order':i+1,'route_a_batch_model':i//3,'start_offset_seconds_UNTESTED':3600*(i//3),'axis_nodes':n,'K_out_inverse_kpc':K,'solo_hours_UNTESTED':solo,'token_schedule_finish_hours_UNTESTED':solo+i//3,'wall_cap_hours_proposed':wall,'rss_cap_bytes_proposed':rss,'rss_basis':'0538 minimum >=1.5x modelled N8 peak','output_cap_bytes_proposed':disk,'outdir':str(out),'receipt':str(out)+'.receipt.json','monitor_log':str(out)+'.monitor.log','spec':ref};rows.append(row)
  if not preview:
   args=[PYTHON,'-I','-B',str(MON),'--driver',reg['driver']['path'],'--driver-sha256',reg['driver']['sha256'],'--spec',str(p),'--outdir',str(out),'--receipt',str(out)+'.receipt.json','--wall-cap-s',str(wall*3600),'--rss-cap-bytes',str(rss),'--output-cap-bytes',str(disk),'--poll-s','2.0']
   row['monitor_argv']=args
   commands.append('# '+case+'\nenv OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 '+shlex.join(args)+' &\nsleep 3')
 runtime=json.loads((R/'R5_RUNTIME_PINS_V001.json').read_bytes())['pins']
 o={'label':'UNTESTED route-A token planning scenario; NOT LAUNCH AUTHORIZATION','P':128,'M_s':128,'registry':pin(rp),'driver':runtime['driver'],'cost_model':pin(cp),'monitor':pin(MON),'launcher':pin(R/'route_a_token_launcher_cx1v004.py'),'guard':pin(R/'producer_guard_cx1v006.py'),'launcher_log':str(EXT/'KMAX_V007_P128_MS128_CX1_LAUNCHER_V005.log'),'route_a_tokens':3,'route_b_overlap':'unrestricted by token count','order':order,'calls':rows,'expected_finish_hours_after_launch_UNTESTED':max(x['solo_hours_UNTESTED']+x['route_a_batch_model'] for x in rows),'expected_finish_lower_scenario_hours_UNTESTED':max(x['solo_hours_UNTESTED']+.75*x['route_a_batch_model'] for x in rows),'assumptions':['0538 supersedes0537: max3 active calls without route_a/finished progress event','C6T first then96-nodeK128 includingD5; KHI,C3,C2,KLO,C5c last','Route-A duration0.75–1h each is root model UNTESTED; queue offsets assume batches of3; actual scheduler releases by progress event','B phases overlap; no inter-run prerequisites before compare; R-PAIR after decidability only','No nice on root launches; build-lane replay limits unchanged','M_s64 tail costs multiplied2 forMS128 and4 further forK256;32A/32B builds; conservative UNTESTED solo estimate retained','Wall caps about2x solo; co-load may lengthen execution; root will request heavy-compute hold during A window','RSS minima39/28/44/24/21/16GiB follow0538; D5 assigned96-node28GiB, nodes-specific peak remains unmeasured','Each monitor and launcher detached with nohup and new session; shell interruption leaves monitors enforcing caps','Ordinary case failures continue; new starts halt only on systemic memory/disk/setup failures or absent monitor receipt; root decides relaunches','No retries, resumes, output reuse or aggregate success inferred from shell wait']}
 worker_file=R/'R5_WORKER_SHA256_0541_V001.txt';worker_pins=[]
 for line in worker_file.read_text().splitlines():
  digest,path=line.split('  ',1);ref=pin(Path(path))
  if ref['sha256']!=digest:raise ValueError('R5_WORKER_BYTES_CHANGED')
  worker_pins.append(ref)
 o['runtime_worker_pin_file']=pin(worker_file);o['runtime_worker_pins']=worker_pins
 if preview:write(R/'P128/TOKEN_COST_PREVIEW_V005.json',o)
 else:
  o['driver']=reg['driver'];write(R/'P128/LAUNCH_PLAN_V005.json',o);cases['C5H']=str(EXT/'KMAX_A2F10_C5H_RUN_V001')
  write(R/'P128/CASES_MANIFEST_TEMPLATE_V005.json',{'schema':'UNT_KMAX_TAIL_V007_MANIFEST_C2V002','cases':cases,'identity_runs':{},'gates':{}})
  cmd=shlex.join([PYTHON,'-I','-B',str(R/'route_a_token_launcher_cx1v004.py'),str(R/'P128/LAUNCH_PLAN_V005.json')])+' --execute-root-only'
  with (R/'P128/LAUNCH_COMMAND_V005.txt').open('x') as f:f.write('# Claude2 only after seal, frozen guard registration and dry-run pass. Root admission config must pin the actual seal; no argv seal authority.\n'+cmd+'\n')
 print('UNTESTED token-schedule projection hours',o['expected_finish_hours_after_launch_UNTESTED'])
if __name__=='__main__':main()
