"""In-process v010 r4 dry plans of the synthetic wave fixture; no solves."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import platform
import resource
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
platform.platform=lambda *a,**kw:'CX2 no-subprocess '+repr(os.uname())
platform._Processor.get=staticmethod(lambda:os.uname().machine)
def guard(event,args):
    if event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','socket.connect'):
        raise RuntimeError('NO_LAUNCH_OR_NETWORK '+event)
    if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
        p=os.path.realpath(os.fsdecode(args[0]))
        if 'KMAX_A2F10_C5H_RUN_V001' in p or '/runs_ext/UVT_' in p or '/.codex/' in p:
            raise RuntimeError('FORBIDDEN_PATH '+p)
        if 'NGC3198' in p and any(w in p.lower() for w in ('observed','target','rotmod')):
            raise RuntimeError('FORBIDDEN_TARGET '+p)
sys.addaudithook(guard)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
driver=BASE/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
assert sha(driver)=='b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
ms=importlib.util.spec_from_file_location('cx2_driver_dry',driver)
D=importlib.util.module_from_spec(ms);sys.modules[ms.name]=D;ms.loader.exec_module(D)
coords=json.loads((HERE/'DDO154_COORDINATES_CX2V006.json').read_bytes())
template=json.loads(Path(coords['call_spec_mapping']['template']['path']).read_bytes())
fixture=json.loads((HERE/'WAVE_FIXTURE_V001.json').read_bytes())
out=HERE/'driver_wave_dryplans_v001';out.mkdir()
records=[]
for row in fixture['rows']:
    kb=row['K_big'];cfg=json.loads((HERE/('RUN_CONFIG_DDO154_CX2V006_KB%03d_R1.json'%kb)).read_bytes())
    for wave in row['waves']:
        for i,call in enumerate(wave['calls']):
            spec=copy.deepcopy(template);spec['numerics']=copy.deepcopy(cfg['numerics']['block'])
            spec['physical']=call['physical'];spec['label']='CX2 SYNTHETIC WAVE PLAN ONLY KB%d %s %d'%(kb,wave['name'],i)
            name='KB%d_%s_%02d'%(kb,wave['name'],i)
            sp=out/(name+'.json')
            with sp.open('x') as f:json.dump(spec,f,sort_keys=True,indent=1);f.write('\n')
            rd=out/name
            with contextlib.redirect_stdout(io.StringIO()):ret=D.cmd_dry_run(str(sp),str(rd))
            report=rd/'DRYRUN_REPORT.json'
            doc=json.loads(report.read_bytes())
            records.append({'K_big':kb,'wave':wave['name'],'index':i,'return':ret,
                            'spec':{'path':str(sp),'sha256':sha(sp)},
                            'report':{'path':str(report),'sha256':sha(report)},
                            'blockers':doc.get('blockers'), 'status':doc.get('status')})
result={'status':'TESTED','execution_note':'nice unavailable (sandbox); 0514 waiver',
        'launches_performed':0,'scope':'SYNTHETIC wave coordinates; real driver dry-run only',
        'records':records,'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'driver':{'path':str(driver),'sha256':sha(driver)},
        'script_sha256':sha(__file__)}
with (HERE/'DRIVER_WAVE_PLANS_V001.json').open('x') as f:json.dump(result,f,indent=1,sort_keys=True);f.write('\n')
print(json.dumps({'plans':len(records),'max_rss_bytes':result['max_rss_bytes_macos'],
                  'output':str(HERE/'DRIVER_WAVE_PLANS_V001.json')}))
