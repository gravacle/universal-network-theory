"""Prepare proposed commands and conservative two-call waves; never execute commands."""
import hashlib,json,math,shlex
from pathlib import Path
R=Path(__file__).parent;A=R.parent
PYTHON='/Users/bgm/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
MON=A/'galaxy_m0_forward_c2_0466/root_monitor_c2v001.py'
EXT=Path('/Volumes/External1/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13/CLAUDE2/runs_ext')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p,o):
    with p.open('x') as f:json.dump(o,f,indent=1);f.write('\n')
def main():
    reg=json.loads((R/'SPEC_REGISTRY_CX1V002.json').read_bytes())
    costp=A/'calib_tail_readiness_cx2/certificate_analysis/COST_MODEL_CX2V001.json';cost=json.loads(costp.read_bytes())
    order=['C6T','C4T','C4T-D5','C4T-KHI','C3T','S4T','C4T-A','C4T-KLO','C2T','C4T-C5c']
    for P in (64,128):
        ents={x['case']:x for x in reg['specs'] if x['P']==P};cases={};rows=[];t=0.;commands=[]
        for wave in range(5):
            estimates=[]
            for case in order[2*wave:2*wave+2]:
                ent=ents[case];spec=json.loads(Path(ent['filled']['path']).read_bytes());K=ent['K_big_inverse_kpc']
                timing=cost['timings'][str(min(128,max(64,int(K))))]
                extrap=K>128
                factor=(K/128)**2 if extrap else 1.
                n=(spec['numerics']['composite_grid_spec'] or {'total_axis_nodes':72})['total_axis_nodes']
                # Planning scenario only: C5H 4.7h from dispatch, scale kept work cubically by axis size;
                # 32 A warm builds and 32 B builds are budget assumptions, not measured stage counts.
                kept_h=max(1.8,4.7*(n/108)**3)
                tail_h=factor*(timing['route_A_cold_s']+32*timing['route_A_warm_s']+32*timing['route_B_rotation_cold_s'])/3600
                expected_h=kept_h+tail_h
                cap_h=max(14 if n<=108 else 19,math.ceil(2*expected_h))
                rss=32*2**30;disk=(96 if n<=108 else 128)*2**30
                out=EXT/f'KMAX_V007_P{P}_{case.replace("-","_")}_CX1_RUN_V001'
                cases[case]=str(out)
                args=[PYTHON,'-I','-B',str(MON),'--driver',reg['driver']['path'],'--driver-sha256',reg['driver']['sha256'],'--spec',ent['filled']['path'],'--outdir',str(out),'--receipt',str(out)+'.receipt.json','--wall-cap-s',str(cap_h*3600),'--rss-cap-bytes',str(rss),'--output-cap-bytes',str(disk),'--poll-s','2.0']
                command='env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 '+shlex.join(args)
                commands.append(f'# Wave {wave+1}; root only, after seal and blockers resolved: {case}\n'+command)
                rows.append({'case':case,'wave':wave+1,'expected_hours_UNTESTED':expected_h,'wall_cap_hours_proposed':cap_h,'rss_cap_bytes_proposed':rss,'output_cap_bytes_proposed':disk,'tail_timing_extrapolated':extrap,'outdir':str(out),'receipt':str(out)+'.receipt.json','spec':ent['filled']})
                estimates.append(expected_h)
            t+=max(estimates)
        cases['C5H']=str(EXT/'KMAX_A2F10_C5H_RUN_V001') # name only; never opened
        write(R/f'P{P}/CASES_MANIFEST_TEMPLATE_V001.json',{'schema':'UNT_KMAX_TAIL_V007_MANIFEST_C2V002','cases':cases,'identity_runs':{},'gates':{}})
        write(R/f'P{P}/LAUNCH_PLAN_V001.json',{'label':'UNTESTED planning projection; NOT LAUNCH AUTHORIZATION','P':P,'driver':reg['driver'],'monitor':pin(MON),'cost_model':pin(costp),'parallel_calls':2,'maximum_authorized_calls':4,'core_model':'two N8 route-A calls reserve 16 worker cores plus 2 scheduling cores; no oversubscription assumed','order':order,'calls':rows,'expected_finish_hours_after_launch_UNTESTED':t,'assumptions':['C5H 4.7h and identity 1.8h are dispatch-provided, not forbidden-run reads','Kept time scaled by axis_nodes cubed from 108; UNTESTED extrapolation','32 route-A warm builds and 32 route-B builds are a cost scenario, not a bound','P128 KHI256 is extrapolated and MEMORY/GQ BLOCKED','Wall/RSS/disk caps are proposed cutoffs, not guaranteed requirements; no retry authorization','Two-call waves are an explicit feasible schedule under at-most-four; faster adaptive overlap requires root to account for each active stage']})
        with (R/f'P{P}/LAUNCH_COMMANDS_V001.txt').open('x') as f:f.write('# PROPOSED ONLY. Claude2 only. Do not execute before seal, A55 and blocker resolution.\n# Start the two calls in each wave concurrently; wait for both receipts before next wave.\n\n'+'\n\n'.join(commands)+'\n')
        print(P,'expected hours scenario',round(t,2))
if __name__=='__main__':main()
