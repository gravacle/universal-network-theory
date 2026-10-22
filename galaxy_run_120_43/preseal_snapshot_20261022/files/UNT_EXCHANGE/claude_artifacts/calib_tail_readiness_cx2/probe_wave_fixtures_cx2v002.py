"""Dry wave planning on declared synthetic seed/Jacobian cache values only.

No synthetic entry is written into a real cache. Outputs prove shape/planning,
never real DDO154 identifiability, convergence, calibration or launch readiness.
"""
import os
for _k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    sp=importlib.util.spec_from_file_location('cx2wave',HERE/'calibration_orchestrator_cx2v006r1.py')
    M=importlib.util.module_from_spec(sp);sys.modules[sp.name]=M;sp.loader.exec_module(M)
    rows=[]
    for kb in (64,128):
        testcfg=json.loads((HERE/('RUN_CONFIG_DDO154_CX2V006_KB%03d_R1.json'%kb)).read_bytes())
        testcfg['work_dir']=str(HERE/('NO_LAUNCH_LOCAL_WAVE_FIXTURE_KB%d'%kb))
        testcfg['work_dir_volume']=None
        testcfg['work_dir_identity']={'resolved':testcfg['work_dir'],'volume':None,'volume_uuid':None,'symlinks':[]}
        ctx=M.planning_context(testcfg)
        E=ctx.E
        u0=ctx.trial_u
        cache={}
        class C:
            def forward(self,key):return cache.get(key)
        def add(u):
            nat=E.to_natural(spec=ctx.es,u=u)
            if not nat.get('ok'):raise ValueError(nat)
            # Each varying coordinate influences a distinct row with positive
            # synthetic speed. These are arbitrary fixture values, NOT data.
            speeds={rid:sum(ctx.region['rectangles'][rid])/2+(u[i]-u0[i] if i<len(u) else 0.0)
                    for i,rid in enumerate(ctx.row_ids)}
            cache[M.O.theta_key(nat['theta_natural'])]={'valid':True,'speeds_km_s':speeds,
                                                     'reasons':['SYNTHETIC_WAVE_FIXTURE_NOT_DDO154']}
        add(u0)
        jac=M.O.Probe(ctx).run(C(),'probe')
        for miss in jac['misses']:
            u=list(miss['u'])
            add(u)
            # Engine serial derivative consumes the opposite side after the
            # cached first side; add the exact reflected normalized coordinate.
            opp=[2*x-y for x,y in zip(u0,u)]
            add(opp)
        exploration=M.O.Probe(ctx).run(C(),'probe')
        planned=[]
        for family,rec in [('jacobian',jac),('first_after_jacobian',exploration)]:
            calls=[]
            for miss in rec['misses']:
                b=ctx.mapper.build(miss['theta'])
                ctx.prelaunch_check(b['spec'])
                calls.append({'family':miss['family'],'purpose':miss['purpose'],'u':miss['u'],
                              'spec_sha256':b['sha256'],'physical':b['spec']['physical'],
                              'certificate_point_key':b['certificate_point_key']})
            planned.append({'name':family,'stop_reason':rec['stop_reason'],'families':rec['families'],
                            'n_calls':len(calls),'calls':calls})
        rows.append({'K_big':kb,'scope':'SYNTHETIC_CACHE_ONLY','waves':planned,
                     'gate_report':ctx.gate_report(),'real_production_ready':ctx.gates_ok()})
    result={'status':'TESTED','execution_note':M.WAIVER,'launches_performed':0,'rows':rows,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'limitations':['Real tail seed/Jacobian absent: actual exploration directions and call list UNTESTED.',
                           'Fixture plans are not production capability/certificate evidence.']}
    with Path(a.output).open('x') as f:json.dump(result,f,indent=1,sort_keys=True);f.write('\n')
    print(json.dumps({'output':a.output,'waves':[[w['n_calls'] for w in r['waves']] for r in rows]}))
if __name__=='__main__':main()
