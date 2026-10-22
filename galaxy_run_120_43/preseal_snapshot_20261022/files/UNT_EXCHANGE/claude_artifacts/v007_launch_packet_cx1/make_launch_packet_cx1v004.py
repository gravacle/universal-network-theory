"""0537: propose all-ten concurrency; no launch. --template-only writes cost preview only."""
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
 order=['C6T','C4T-D5','C4T-KHI','C4T','C3T','S4T','C4T-A','C4T-KLO','C2T','C4T-C5c'];ents={x['case']:x for x in reg['specs']};assert set(ents)==set(order)
 rows=[];commands=[];cases={}
 for i,case in enumerate(order):
  ref=ents[case]['template' if preview else 'filled'];p=Path(ref['path']);assert pin(p)==ref;sp=json.loads(p.read_bytes());uv=sp['numerics']['uv_tail'];assert uv['gas']['M_s']==128
  K={'C4T-KLO':64,'C4T-KHI':256,'C4T-C5c':5}.get(case,128);assert uv['outer'].get('K_big_inverse_kpc',uv['outer'].get('K_out_inverse_kpc'))==K
  timing=cost['timings'][str(min(128,max(64,K)))];factor=max(1.,(K/128)**2)*2.
  n=(sp['numerics']['composite_grid_spec'] or {'total_axis_nodes':72})['total_axis_nodes']
  kept=max(1.8,4.7*(n/108)**3);tail=factor*(timing['route_A_cold_s']+32*timing['route_A_warm_s']+32*timing['route_B_rotation_cold_s'])/3600;solo=kept+tail
  # 2x contention planning multiplier, then2x margin over that scenario for cutoff.
  wall=max(28 if n<=108 else 38,math.ceil(4*solo))
  measured={'C2T':1.5,'C6T':19.7}.get(case,3.0);tail_gb=8 if K==256 else4
  rss=math.ceil((measured+tail_gb)*1.5*10**9);disk=(96 if n<=108 else128)*2**30
  out=EXT/f'KMAX_V007_P128_{case.replace("-","_")}_MS128_CX1_RUN_V003';cases[case]=str(out)
  row={'case':case,'start_order':i+1,'start_offset_seconds':3*i,'axis_nodes':n,'K_out_inverse_kpc':K,'solo_hours_UNTESTED':solo,'all_concurrent_hours_UNTESTED':2*solo,'wall_cap_hours_proposed':wall,'rss_cap_bytes_proposed':rss,'rss_baseline_GB_dispatch':measured,'extra_tail_allowance_GB_UNTESTED':tail_gb,'rss_margin':1.5,'output_cap_bytes_proposed':disk,'outdir':str(out),'receipt':str(out)+'.receipt.json','spec':ref};rows.append(row)
  if not preview:
   args=[PYTHON,'-I','-B',str(MON),'--driver',reg['driver']['path'],'--driver-sha256',reg['driver']['sha256'],'--spec',str(p),'--outdir',str(out),'--receipt',str(out)+'.receipt.json','--wall-cap-s',str(wall*3600),'--rss-cap-bytes',str(rss),'--output-cap-bytes',str(disk),'--poll-s','2.0']
   commands.append('# '+case+'\nenv OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 '+shlex.join(args)+' &\nsleep 3')
 o={'label':'UNTESTED all-concurrent planning scenario; NOT LAUNCH AUTHORIZATION','P':128,'M_s':128,'registry':pin(rp),'cost_model':pin(cp),'monitor':pin(MON),'concurrent_calls':10,'order':order,'calls':rows,'expected_finish_hours_after_launch_UNTESTED':max(2*x['solo_hours_UNTESTED']+x['start_offset_seconds']/3600 for x in rows),'assumptions':['0537 replaces earlier2-call waves and4-call limit for root launch','C6T first; all10 have no inter-run dependency before compare; stagger3s','No nice setting for proposed root launches; this does not change build-lane replay limits','18 cores shared by macOS; up to80 route-A workers means contention is expected','2x solo duration is a contention scenario, not a measured scaling law or bound','wall caps double the earlier2x solo margin to4x solo scenario','M_s64 tail measurements scaled2x for M_s128; further4x forK256; no production timing claim','32 warmA and32 coldB builds assumed; C5c usesK64 continuum timing as proxy','C2/C4/C6 RSS1.5/3/19.7GB are dispatch0537 measurements; C3 usesC4 conservatively; tail4GB or8GB allowance untested;1.5x margin','Per-process RSS caps are cutoffs, not reservations or proof of aggregate fit; root estimated50–60GB actual total','R-PAIR only after compare decidability read; not part of this launch file','No retries or overwrite permission']}
 if preview:write(R/'P128/CONCURRENT_COST_PREVIEW_V003.json',o)
 else:
  o['driver']=reg['driver'];write(R/'P128/LAUNCH_PLAN_V003.json',o);cases['C5H']=str(EXT/'KMAX_A2F10_C5H_RUN_V001')
  write(R/'P128/CASES_MANIFEST_TEMPLATE_V003.json',{'schema':'UNT_KMAX_TAIL_V007_MANIFEST_C2V002','cases':cases,'identity_runs':{},'gates':{}})
  with (R/'P128/LAUNCH_COMMANDS_V003.txt').open('x') as f:f.write('# Claude2 only, after seal and all prerequisites; proposed, never executed by build lane.\n# All10 concurrent,3s stagger; no inter-run dependency.\n'+'\n\n'.join(commands)+'\nwait\n# Inspect all10 monitor receipts; wait exit alone is not aggregate success.\n')
 print('UNTESTED concurrent projection hours',o['expected_finish_hours_after_launch_UNTESTED'])
if __name__=='__main__':main()
