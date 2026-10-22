"""Prepare P128/r5/M_s128 commands from filled registry. Never execute launches.
The M_s128 cost is a conservative scenario, not a measured timing or bound.
"""
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
    regpath=R/'SPEC_REGISTRY_R5_MS128_CX1V004.json';reg=json.loads(regpath.read_bytes())
    costp=A/'calib_tail_readiness_cx2/certificate_analysis/COST_MODEL_CX2V001.json';cost=json.loads(costp.read_bytes())
    order=['C6T','C4T','C4T-D5','C4T-KHI','C3T','S4T','C4T-A','C4T-KLO','C2T','C4T-C5c']
    ents={x['case']:x for x in reg['specs']};assert set(ents)==set(order)
    cases={};rows=[];t=0.;commands=[]
    for wave in range(5):
        estimates=[]
        for case in order[2*wave:2*wave+2]:
            ent=ents[case];p=Path(ent['filled']['path']);assert pin(p)==ent['filled'];spec=json.loads(p.read_bytes())
            uv=spec['numerics']['uv_tail'];assert uv['gas']['M_s']==128
            K={'C4T-KLO':64,'C4T-KHI':256,'C4T-C5c':5}.get(case,128)
            timing=cost['timings'][str(min(128,max(64,K)))]
            # No claim that M_s128 doubles wall time exactly; this is explicit planning margin.
            factor=max(1.,(K/128)**2)*2.
            n=(spec['numerics']['composite_grid_spec'] or {'total_axis_nodes':72})['total_axis_nodes']
            kept_h=max(1.8,4.7*(n/108)**3)
            tail_h=factor*(timing['route_A_cold_s']+32*timing['route_A_warm_s']+32*timing['route_B_rotation_cold_s'])/3600
            expected_h=kept_h+tail_h;cap_h=max(14 if n<=108 else 19,math.ceil(2*expected_h))
            rss=32*2**30;disk=(96 if n<=108 else 128)*2**30
            out=EXT/f'KMAX_V007_P128_{case.replace("-","_")}_MS128_CX1_RUN_V002';cases[case]=str(out)
            args=[PYTHON,'-I','-B',str(MON),'--driver',reg['driver']['path'],'--driver-sha256',reg['driver']['sha256'],'--spec',str(p),'--outdir',str(out),'--receipt',str(out)+'.receipt.json','--wall-cap-s',str(cap_h*3600),'--rss-cap-bytes',str(rss),'--output-cap-bytes',str(disk),'--poll-s','2.0']
            commands.append(f'# Wave {wave+1}; Claude2 only after seal: {case}\n'+'env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 10 '+shlex.join(args))
            rows.append({'case':case,'wave':wave+1,'K_out_inverse_kpc':K,'expected_hours_UNTESTED':expected_h,'wall_cap_hours_proposed':cap_h,'rss_cap_bytes_proposed':rss,'output_cap_bytes_proposed':disk,'M_s128_timing_measured':False,'K256_extrapolated':K==256,'outdir':str(out),'receipt':str(out)+'.receipt.json','spec':ent['filled']});estimates.append(expected_h)
        t+=max(estimates)
    cases['C5H']=str(EXT/'KMAX_A2F10_C5H_RUN_V001') # string only; forbidden to this lane
    write(R/'P128/CASES_MANIFEST_TEMPLATE_V002.json',{'schema':'UNT_KMAX_TAIL_V007_MANIFEST_C2V002','cases':cases,'identity_runs':{},'gates':{}})
    write(R/'P128/LAUNCH_PLAN_V002.json',{'label':'UNTESTED planning projection; NOT LAUNCH AUTHORIZATION','P':128,'M_s':128,'registry':pin(regpath),'driver':reg['driver'],'monitor':pin(MON),'cost_model':pin(costp),'parallel_calls':2,'maximum_dispatch_calls':4,'core_model':'two N8 route-A calls reserve 16 worker cores plus 2 scheduling cores','order':order,'calls':rows,'expected_finish_hours_after_launch_UNTESTED':t,'assumptions':['C5H 4.7h and identity 1.8h are dispatch-provided, never read from forbidden runs','Kept work scaled by axis_nodes cubed from108; UNTESTED','32 warm A and32 cold B builds are a scenario, not a bound','M_s64 measured tail times multiplied by2 for M_s128 planning margin; M_s128 timing UNTESTED','K256 adds4x tail multiplier; no measured K256 timing','C5c uses K64 continuum timing as conservative proxy; nodes route not measured here','r5 memory-cap source change TESTED separately, runtime resource sufficiency UNTESTED','Caps are proposed cutoffs, no automatic retry','Start next wave only after both receipts complete; stage concurrency may use fewer cores','Identity/gate manifest slots remain empty until frozen compare and actual records exist']})
    with (R/'P128/LAUNCH_COMMANDS_V002.txt').open('x') as f:f.write('# PROPOSED ONLY. Claude2 sole launcher. Requires seal, current filled dry-run pass, and blocker resolution.\n# Two calls per wave; wait for both receipts before next wave.\n\n'+'\n\n'.join(commands)+'\n')
    print('P128 MS128 scenario hours',round(t,2))
if __name__=='__main__':main()
