"""0515: exclusive-create corner templates, dry plans and proposed root launch list.

No worker/solver/forward launches. Pending certificate slots are never filled with
anchor certificates. The list is a plan for Claude2, not an executable campaign.
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import contextlib
import copy
import hashlib
import importlib.util
import io
import itertools
import json
import platform
import resource
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
OUT=HERE/'corner_preparation_v001'
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
def pin(p):
    p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(path,obj):
    with path.open('x') as f:json.dump(obj,f,indent=1,sort_keys=True,allow_nan=False);f.write('\n')
    return pin(path)
driver=BASE/'tail_scheme_impl_c2/driver_r4/galaxy_m0_forward_c2v010.py'
assert pin(driver)['sha256']=='b9ae92d5857951511437cf7632eb732c97b63592ed700e6810941c5f2d8d762b'
ms=importlib.util.spec_from_file_location('cx2_corner_driver',driver)
D=importlib.util.module_from_spec(ms);sys.modules[ms.name]=D;ms.loader.exec_module(D)
coord=json.loads((HERE/'DDO154_COORDINATES_CX2V006.json').read_bytes())
template=json.loads(Path(coord['call_spec_mapping']['template']['path']).read_bytes())
by={c['name']:c for c in coord['engine_coordinates']}
free=['common_scale_s','gamma_over_Eref','ell_F_m']
OUT.mkdir()
rows=[]
caps={'wall_cap_s':28800.0,'rss_cap_bytes':64*1024**3,'output_cap_bytes':12*1024**3,'poll_s':2.0}
for kb in (64,128):
    cfg=json.loads((HERE/('RUN_CONFIG_DDO154_CX2V006_KB%03d_R1.json'%kb)).read_bytes())
    for bits in itertools.product((0,1),repeat=3):
        th={name:by[name]['upper' if bit else 'lower'] for name,bit in zip(free,bits)}
        for mode,dist in [('HEADLINE_FIXED_D',4.04),('DISTANCE_ALTERNATIVE_LO',by['distance_Mpc']['lower']),
                          ('DISTANCE_ALTERNATIVE_HI',by['distance_Mpc']['upper'])]:
            label='KB%03d_C%s_%s'%(kb,''.join(map(str,bits)),mode)
            spec=copy.deepcopy(template);spec['numerics']=copy.deepcopy(cfg['numerics']['block'])
            spec['physical'].update(common_scale_s=th['common_scale_s'],
                gamma=th['gamma_over_Eref']*by['Eref_base_J']['trial_value'],ell_F_m=th['ell_F_m'],distance_Mpc=dist)
            spec['label']='0515 CORNER TEMPLATE '+label+'; pending EPS/LO; Claude2 only; no launch performed'
            sp=write(OUT/(label+'.TEMPLATE.json'),spec)
            rd=OUT/(label+'_dry')
            with contextlib.redirect_stdout(io.StringIO()):ret=D.cmd_dry_run(sp['path'],str(rd))
            rp=rd/'DRYRUN_REPORT.json';doc=json.loads(rp.read_bytes());s=doc['summary']
            beyond=[x for x in s['refusals_beyond_pending_inputs'] if not x.startswith('PENDING_UV_TAIL_CERTIFICATE:')]
            ok=(ret==0 and doc['executed_stages']==0 and not s['pin_problems'] and
                not s['binding_blockers'] and not s['unexplained_refusals'] and not beyond)
            rows.append({'id':label,'K_big_inverse_kpc':kb,'coordinate_mode':mode,'theta':dict(th,distance_Mpc=dist),
                'template':sp,'driver':pin(driver),'dry_report':pin(rp),'dry_plan_ok_except_certificates':ok,
                'dry_blockers':beyond+s['binding_blockers']+s['unexplained_refusals'],
                'pending_certificates':doc['uv_tail']['pending_certificates'],
                'launch_status':'NOT_LAUNCHABLE_PENDING_CERTIFICATES_AND_ROOT_GATES',
                'proposed_caps':caps,'root_output_directory':cfg['work_dir']+'_CORNERS/'+label})
manifest={'schema':'DDO154_CORNER_LAUNCH_LIST_CX2V001','execution_note':'nice unavailable (sandbox); 0514 waiver',
    'owner':'Claude2','launches_performed':0,'rows':rows,'all_dry_plans_ok_except_certificates':all(r['dry_plan_ok_except_certificates'] for r in rows),
    'counts':{'per_K_big':24,'headline_corners_per_K_big':8,'distance_alternative_corners_per_K_big':16},
    'selection_rule':'A55 selects ONE K_big; A13 keeps headline D fixed. Alternative-D calls are separately labelled and do not restore D nuisance.',
    'caps_status':'PROPOSED_RESOURCE_CEILINGS_NOT_MEASURED_FULL_CALL_BOUNDS; Claude2 must ratify against current workload and full caps evidence',
    'scheduling':{'max_concurrent_calls':1,'route_a_column_workers':8,'fs_column_workers':2,'future_process_budget':17},
    'cap_rationale':'8-hour/12-GiB historical ceilings retained; RSS raised to 64 GiB as a conservative proposed ceiling because saved K128 controller peak ~2.9GB does not cover eight-worker copies. Aggregate memory remains UNTESTED.',
    'fill_rule':'Replace only numerics.uv_tail.eps_certificate and lo_certificate with per-point valid byte pins, write a new FILLED filename, recompute its SHA256 and dry-plan it. No template hash is a filled-call hash.',
    'runtime':coord.get('python'),'max_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'sources':[pin(__file__),pin(HERE/'DDO154_COORDINATES_CX2V006.json'),pin(BASE.parent/'FROM_CODEX/0515_2026-10-18_codex2_lane_A_scope_clarification.md')]}
write(OUT/'CORNER_LAUNCH_LIST_V001.json',manifest)
print(json.dumps({'corners':len(rows),'dry_ok_except_certificates':manifest['all_dry_plans_ok_except_certificates'],'rss':manifest['max_rss_bytes_macos']}))
