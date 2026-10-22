"""Create immutable v006 Kbig64/128 candidate configs. No scientific launches."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
import copy
import hashlib
import json
from pathlib import Path

B=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
OUT=Path(__file__).resolve().parent
def pin(p):
    p=Path(p)
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):
    return json.loads(Path(p).read_bytes())
def write(name,obj):
    p=OUT/name
    with p.open('x') as f: json.dump(obj,f,sort_keys=True,indent=1,allow_nan=False);f.write('\n')
    return pin(p)

def main():
    source=B/'calibration_engine_freeze_v003b_v003d/orchestrator_v005a/DDO154_CALIBRATION_COORDINATE_SPEC_V002.json'
    coord=read(source)
    coord['freeze']=pin(B/'calibration_engine_freeze_v003b_v003d/prediction_freeze_c2v003d.py')
    cp=write('DDO154_COORDINATES_CX2V006.json',coord)
    add=read(B/'calibration_orchestrator_c2/v005/COORDINATE_SPEC_ADDENDUM_V005.json')
    add['applies_to_coordinate_spec_sha256']=cp['sha256']
    ap=write('COORDINATE_ADDENDUM_CX2V006.json',add)
    drv=pin(B/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py')
    tax=read(B/'calibration_orchestrator_c2/v004/FAILURE_TAXONOMY_V003.json')
    tax['driver']=drv
    tax['v006_scope_note']='V003 rules retained provisionally; unknown tail/RO1 outcomes fail closed as INFRA. Distinct classification review pending.'
    tp=write('FAILURE_TAXONOMY_CX2V006_CANDIDATE.json',tax)
    template=read(B/'tail_scheme_impl_c2/driver/specs/CALL_KMAX_TAIL_C4T_K64_A2F10_HULL_N8_M32_C2V010.TEMPLATE.json')
    for kb in (64,128):
        cfg=read(B/'calibration_orchestrator_c2/v005/RUN_CONFIG_DDO154_V005.json')
        block=copy.deepcopy(template['numerics'])
        block['uv_tail']['outer']['K_big_inverse_kpc']=float(kb)
        block['route_a']['ro1_workers']=True
        cfg.update(coordinate_spec=cp,coordinate_spec_addendum=ap,driver=drv,taxonomy=tp,
                   deciding_test=None,capability_evidence=None,adoption_derivation=None,max_concurrent=1)
        cfg['anchor']={'use':False,'receipt':None,'result':None,'spec_sha256':None,'driver_sha256':None}
        cfg['numerics']={'block':block,'block_source':None,'verdict_artifact':None,
                         'note':'Candidate only. A55 production K choice and V007 adopted-block evidence pending.'}
        name='DDO154_CALIBRATION_ORCH_CX2V006_KB%03d'%kb
        old='DDO154_CALIBRATION_ORCH_V005'
        cfg['work_dir']=cfg['work_dir'].replace(old,name)
        cfg['work_dir_identity']['resolved']=cfg['work_dir_identity']['resolved'].replace(old,name)
        cfg['notes']='0511 source-only candidate; no launch. New cache namespace. No old anchor alias. RO1 c2v002 armed. No automatic bracket widening. Full hull on all columns at all D. Fixed headline D=4.04 and i=66 retained.'
        cfg['tail_readiness']={
            'schema':'DDO154_TAIL_READINESS_CONFIG_CX2V006','certificate_registry':None,
            'K_big_choice':'PENDING_A55','candidate_K_big_inverse_kpc':kb,
            'certificate_phase_rule':'EPS/GQ before each point; LO and source-dependent GQ for every source-influencing and accepted state before caching VALID',
            'post_state_verifier':'PENDING_INTEGRATION',
            'execution_note':'nice unavailable (sandbox); 0514 waiver',
            'build_lane_process_cap':2,'per_replay_memory_cap_bytes':8000000000,
            'future_launch_owner':'Claude2','production_caps_status':'UNTESTED_REGENERATE_FROM_TAIL_TIMING'}
        write('RUN_CONFIG_DDO154_CX2V006_KB%03d.json'%kb,cfg)
    print('Created immutable configs for K_big 64 and 128; no launches.')

if __name__=='__main__':main()
