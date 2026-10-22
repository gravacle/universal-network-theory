"""Bounded source/mapper/engine-plan checks only; no forward subprocesses."""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
def load(p,name):
    spec=importlib.util.spec_from_file_location(name,p)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    M=load(HERE/'calibration_orchestrator_cx2v006r1.py','cx2v006')
    checks=[]
    def check(name,ok,detail=None):checks.append({'name':name,'status':'TESTED','pass':bool(ok),'detail':detail})
    for f in (HERE/'calibration_orchestrator_cx2v006r1.py',HERE/'build_candidates_cx2v001.py'):
        ast.parse(f.read_bytes());check('syntax '+f.name,True)
    identities=[]
    contexts=[]
    for kb in (64,128):
        cfg=HERE/('RUN_CONFIG_DDO154_CX2V006_KB%03d_R1.json'%kb)
        try:
            testcfg=json.loads(cfg.read_bytes())
            testcfg['work_dir']=str(HERE/('NO_LAUNCH_LOCAL_DRY_CONTEXT_KB%d'%kb))
            testcfg['work_dir_volume']=None
            testcfg['work_dir_identity']={'resolved':testcfg['work_dir'],'volume':None,'volume_uuid':None,'symlinks':[]}
            ctx=M.planning_context(testcfg);contexts.append(ctx)
            check('context KB%d'%kb,True)
            check('driver KB%d'%kb,ctx.driver['sha256']==M.DRIVER_SHA)
            check('old cache not reused KB%d'%kb,ctx.cache_id!='3a1374dfbf0df2f3ea0e48ae2eb76ebdccf0b05568ed0940682383a2b0fb781c')
            identities.append(ctx.cache_id)
            check('pending gates fail closed KB%d'%kb,not ctx.gates_ok(),ctx.gate_report())
            check('corner normalization KB%d'%kb,ctx.gates['driver_capability']['layer1_normalize_ok'])
            for label,theta in ctx.probe_points():
                b=ctx.mapper.build(theta)
                check('full hull KB%d %s'%(kb,label),all(x==M.HULL for x in b['spec']['numerics']['brackets']['rule']['fs_absolute_overrides'].values()))
            changed=copy.deepcopy(ctx.numerics);changed['brackets']['rule']['fs_absolute_overrides']['44']=[1,2]
            refused=False
            try:M.validate_block(changed)
            except M.Error:refused=True
            check('reject hull mutation KB%d'%kb,refused)
        except Exception as exc:
            check('context KB%d'%kb,False,type(exc).__name__+': '+str(exc))
    check('Kbig separates cache',len(identities)==2 and identities[0]!=identities[1])
    out={'execution_note':M.WAIVER,'launches_performed':0,'checks':checks,
         'passed':sum(x['pass'] for x in checks),'total':len(checks),
         'scope':'LOCAL READ-ONLY CONTEXT FIXTURE: External1 UUID unavailable in sandbox; actual production config guard preserved. No real Jacobian or exploration result exists',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with Path(a.output).open('x') as f:json.dump(out,f,sort_keys=True,indent=1);f.write('\n')
    print(json.dumps({'passed':out['passed'],'total':out['total'],'output':a.output}))
if __name__=='__main__':main()
