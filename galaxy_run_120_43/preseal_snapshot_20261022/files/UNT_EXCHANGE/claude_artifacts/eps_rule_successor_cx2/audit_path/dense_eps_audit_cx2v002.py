"""ROOT0855 bounded static EPS envelope audit; no galaxy/route/worker launch.

Only exact AST-selected definitions from pinned source are compiled. Project
module top levels, point_context, custody derivation and LWR loaders are NEVER
executed. No actual run or NGC data input is allowed. Default is cheap validation;
--dense is required to perform the registered dense search. All writes exclusive.
Build/source inspection date -u: Wed Oct 21 17:33:59 UTC 2026.
"""
import argparse
import ast
import copy
import datetime
import hashlib
import io
import itertools
import json
import math
import os
from pathlib import Path
import resource
import stat as stat_module
import sys
import time
import types
import numpy as np

A = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
H = A/'calib_tail_readiness_cx2/certificates_per_point'
OUT = A/'eps_rule_successor_cx2/audit_path'
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
DRIVER_SHA = 'b5cc62afb7814b4f337a012a1ffd1f1e677f398ac18a1f8297c7ff49ae5374c6'
SOURCES = {
 'producer': (H/'point_response_producer_cx2v002.py','a1dcdea8deba5bc9667f0ea36d6b94c3cc20fb1d2d95d637cc9e7ea26b478231'),
 'C2': (H/'certs2_common_r5_cx2v001.py','f8f422f034153b4551e5fd5f89740cb594cb9d877e54b467c617206d2fcd6d8c'),
 'CC': (H/'certs_common_r5_cx2v001.py','c75aaa5a197efe7bde1014269d74aa37810ccce6f95b7eec1078352f09ffb3b7'),
 'LWR': (A/'long_wavelength_response_c2/tools/lwr_common_v001.py','758740ebf6caeb80876497674c3ee844f0ec8a9d0fae5d1fb8d491376e3aff48'),
 'static_binding': (UPC/'helpers/response_packet_audit/owned_static_action_metric_binding_v002.py','7130a277ca59b07c8ce788eb20bcb50c996a3575f6fa0e644e971b0d766aee1f'),
 'driver': (A/'tail_scheme_impl_c2/driver_r5/galaxy_m0_forward_c2v010.py',DRIVER_SHA),
}
GRID = (UPC/'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz',
        '2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7')
CASES = {
 302: dict(key='6f4604efe6d7fe348d9ca4986d9042234ed54d5df63b254b4e8c3b6c43861ee1',
   spec=(A/'future_wave_points_cx1/NOMINAL_W3_MINUS_DRAFT/SPEC_W0003_P02_6f4604efe6d7fe34.json','7b32dac96337d06c4046c63f967b0a95503e952e88dcc980ae91d474d2b09521'),
   record=(A/'s4rc1_c3/cp1_run_c3v004b/P302_6f4604efe6d7fe34_W0003_P02_a1/EPS_NUMERIC_6f4604efe6d7fe34.json','3babf8f45719220ac161b5e784cb86e2684129e94be5715848088ae61910dc72')),
 501: dict(key='421cb796874019be37c7ea90d54f7e55ef1baa0d4d254d70b2f5358f973bcf2c',
   spec=(A/'future_wave_points_cx1/CONDITIONAL_GLOBAL_POOL_DRAFT/SPEC_W0005_P01_421cb796874019be.json','35246e7e5ed8602d21013707a00782e28a8a21c917fae7885f16c32fdef19d30'),
   record=(A/'s4rc1_c3/cp1_run_c3v004b/P501_421cb796874019be_W0005_P01_a1/EPS_NUMERIC_421cb796874019be.json','52cc2502b60b53ad14a55fbb94f900e0a7d06e4f256233a9decbb5c48c33ab06')),
 504: dict(key='cdc5592d149fa9efd319e4ac1b3e2fc17d5d52ca51b92c24c36709dfed1a10c0',
   spec=(A/'future_wave_points_cx1/CONDITIONAL_GLOBAL_POOL_DRAFT/SPEC_W0005_P04_cdc5592d149fa9ef.json','25b9ef8a6458eed2539b866fef2b2cbe7d400e26602905816d8b06b4646acc22'),
   record=(A/'s4rc1_c3/cp1_run_c3v004b/P504_cdc5592d149fa9ef_W0005_P04_a1/EPS_NUMERIC_cdc5592d149fa9ef.json','0005d1615277d4c48ab1c1541e9f7c059bb18d11fc13bb13a9da860202d4a3dd')),
}
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS')
ORIGINAL_LSTAT=os.lstat
ORIGINAL_READLINK=os.readlink
READ_SNAPSHOTS={}
EXTRACTIONS=[]

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def sha(raw): return hashlib.sha256(raw).hexdigest()

def lexical(path):
    p=Path(os.path.abspath(os.fspath(path)))
    if any(x in p.parts for x in ('runs','runs_ext','V007_POSTSEAL_RECORDS','.codex')):
        raise ValueError('forbidden path: '+str(p))
    if any('C5H_RUN_V001' in x or x.startswith('UVT_') or 'NGC3198' in x for x in p.parts):
        raise ValueError('forbidden run/data path: '+str(p))
    return p

def canonical_safe(path):
    # Check every symlink target lexically BEFORE traversing its components.
    p=lexical(path)
    for _ in range(40):
        built=Path(p.anchor);changed=False
        for i,part in enumerate(p.parts[1:],1):
            built=lexical(built/part)
            st=ORIGINAL_LSTAT(built)
            if stat_module.S_ISLNK(st.st_mode):
                target=Path(ORIGINAL_READLINK(built))
                if not target.is_absolute():target=built.parent/target
                p=lexical(target.joinpath(*p.parts[i+1:]));changed=True;break
        if not changed:return p
    raise ValueError('symlink chain limit')

def fence():
    # Metadata wrappers reject forbidden targets before the OS call. The selected
    # numeric definitions themselves have no file, process or network operations.
    def wrap(fn):
        def guarded(path,*args,**kwargs):
            if not isinstance(path,int):lexical(path)
            return fn(path,*args,**kwargs)
        return guarded
    for name in ('stat','lstat','readlink','listdir','scandir'):
        setattr(os,name,wrap(getattr(os,name)))
    def audit(event,args):
        if event=='open' and args and not isinstance(args[0],int):lexical(args[0])
        if event in ('os.listdir','os.scandir') and args and not isinstance(args[0],int):lexical(args[0])
        if event.startswith(('subprocess.','socket.')) or event in ('os.system','os.fork','os.posix_spawn','os.exec','os.spawn'):
            raise ValueError('process/network operation forbidden: '+event)
    sys.addaudithook(audit)

def pinned(ref):
    path,want=ref;p=canonical_safe(path);raw=p.read_bytes()
    if sha(raw)!=want:raise ValueError('byte pin mismatch: '+str(path))
    READ_SNAPSHOTS[str(path)]=dict(path=str(path),canonical_path=str(p),sha256=want,size=len(raw))
    return raw

def pinref(ref):return dict(path=str(ref[0]),sha256=ref[1])

def literal(raw,name):
    tree=ast.parse(raw)
    nodes=[n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)]
    if len(nodes)!=1:raise ValueError('literal selection: '+name)
    def data(n):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='dict' and not n.args:
            if any(k.arg is None for k in n.keywords):raise ValueError('dict expansion forbidden')
            return {k.arg:data(k.value) for k in n.keywords}
        if isinstance(n,ast.Dict):return {data(k):data(v) for k,v in zip(n.keys,n.values)}
        return ast.literal_eval(n)
    return data(nodes[0])

def definitions(key,raw,names,namespace):
    tree=ast.parse(raw);selected=[]
    for name in names:
        found=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name]
        if len(found)!=1:raise ValueError('definition selection: '+key+'.'+name)
        node=found[0]
        for child in ast.walk(node):
            if isinstance(child,ast.Import) and any(a.name!='itertools' for a in child.names):raise ValueError('import in selected definition')
            if isinstance(child,ast.ImportFrom):raise ValueError('from-import in selected definition')
            if isinstance(child,ast.Call):
                fn=child.func;called=fn.id if isinstance(fn,ast.Name) else fn.attr if isinstance(fn,ast.Attribute) else ''
                if called in ('open','read_bytes','read_text','load','Popen','run','system','exec','eval','compile','fork','spawn'):
                    raise ValueError('unsafe operation in selected definition: '+called)
        selected.append(node)
        EXTRACTIONS.append(dict(source=key,name=name,start_line=node.lineno,end_line=node.end_lineno,
                                ast_sha256=sha(ast.dump(node,include_attributes=False).encode())))
    # Only selected, unchanged definition nodes. No project top-level statements.
    exec(compile(ast.Module(body=selected,type_ignores=[]),str(SOURCES[key][0]),'exec'),namespace)

def identity(spec):
    if spec.get('galaxy')!='DDO154':raise ValueError('DDO154 only')
    n=copy.deepcopy(spec['numerics'])
    for k in ('eps_certificate','lo_certificate'):n['uv_tail'].pop(k,None)
    return dict(driver_sha256=DRIVER_SHA,physical=spec['physical'],coefficients=spec['coefficients'],numerics=n)

def build_context(case):
    raw={k:pinned(v) for k,v in SOURCES.items()}
    spec=json.loads(pinned(case['spec']));rec=json.loads(pinned(case['record']))
    ident=identity(spec)
    if ident!=rec['identity'] or sha(canonical(ident))!=case['key'] or rec['point_sha256']!=case['key']:
        raise ValueError('spec/EPS/point identity mismatch')
    if rec['producer']!=pinref(SOURCES['producer']) or rec['settings']!='registered':raise ValueError('producer/settings mismatch')
    if spec['coefficients']!=pinref(GRID) or rec['dependencies']['A2_npz']!=pinref(GRID):raise ValueError('grid custody mismatch')
    uv=spec['numerics']['uv_tail']
    if uv['source_rule']!='continuum_v001' or uv['outer']!={'shape':'cylinder','K_big_inverse_kpc':128.0} or uv['gas']['M_s']!=128:
        raise ValueError('registered production point scope')
    with np.load(io.BytesIO(pinned(GRID)),allow_pickle=False) as z:
        grid=z['source_hessian_grid'].copy();cb=z['background_C'].copy();mu=z['background_mu'].copy()
    if any(x.dtype.hasobject or not np.isfinite(x).all() for x in (grid,cb,mu)):raise ValueError('invalid grid/background')
    physical=spec['physical'];scale=physical['common_scale_s']
    if any(type(v) not in (float,int) or not math.isfinite(v) or v<=0 for v in physical.values()):raise ValueError('invalid point')
    eref=scale*physical['Eref_J'];gam=scale*physical['gamma'];ell=physical['ell_F_m']
    base=dict(np=np,math=math,__name__='eps_static_ast_only')
    sn=dict(base);definitions('static_binding',raw['static_binding'],['_real','mandel_matrix','mandel_vector'],sn)
    ln=dict(base,stat=types.SimpleNamespace(mandel_matrix=sn['mandel_matrix'],mandel_vector=sn['mandel_vector']),
            EREF=eref,ELL=ell,GAM=gam,A_BRAVAIS=np.array([[0.,.5,.5],[.5,0.,.5],[.5,.5,0.]]))
    # A_BRAVAIS literal is source-pinned; assert AST form to prevent silent drift.
    atree=ast.parse(raw['LWR'])
    av=[n.value for n in atree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='A_BRAVAIS' for t in n.targets)]
    if len(av)!=1 or not isinstance(av[0],ast.Call) or not np.array_equal(ast.literal_eval(av[0].args[0]),ln['A_BRAVAIS']):
        raise ValueError('Bravais literal mismatch')
    definitions('LWR',raw['LWR'],['root_C','Binder'],ln)
    L=types.SimpleNamespace(Binder=ln['Binder'],A_BRAVAIS=ln['A_BRAVAIS'],KPC=literal(raw['driver'],'KPC_M'),DIRS=literal(raw['LWR'],'DIRS'))
    bn=L.Binder(grid,cb,mu,Eref=eref,ell=ell,gam=gam)
    cn=dict(base);definitions('CC',raw['CC'],['_family','direction_sets','shell_k','q_of'],cn)
    cn['PER_DECADE']=literal(raw['CC'],'PER_DECADE');CC=types.SimpleNamespace(**cn)
    en=dict(base);definitions('C2',raw['C2'],['Envelope','fib_hemi','torus_grid_v','env_full','tangent_basis','refine','distinct_top'],en)
    C2=types.SimpleNamespace(**en);env=C2.Envelope(L,bn)
    pn=dict(base,C2=C2,CC=CC);definitions('producer',raw['producer'],['finite','mandel','values_from_x','discrete_shell','search_envelope'],pn)
    settings=literal(raw['producer'],'SETTINGS')['registered']
    ev,vec=np.linalg.eigh(cb)
    if np.any(ev<=0):raise ValueError('background not positive definite')
    ctx=dict(L=L,B=bn,E=env,cb=cb,isq=(vec/np.sqrt(ev))@vec.T,D=CC.direction_sets(L),cache={})
    arrays={k:dict(shape=list(v.shape),dtype=v.dtype.str,sha256_c_order=sha(np.ascontiguousarray(v).tobytes())) for k,v in [('grid',grid),('Cbar',cb),('mu',mu)]}
    ar={k:dict(dtype=v.dtype.str,shape=list(v.shape),bytes_sha256=sha(np.ascontiguousarray(v).tobytes()))
        for k,v in [('grid',grid),('Cbar',cb),('mu',mu)]}
    grid_custody=sha(canonical(dict(encoding='ARRAY_C_ORDER_V1',coefficient_file=spec['coefficients'],
                                  grid=ar['grid'],composite_grid=spec['numerics']['composite_grid_spec'])))
    background_custody=sha(canonical(dict(C=ar['Cbar'],mu=ar['mu'],physical=spec['physical'])))
    if grid_custody!=rec['custody']['grid_sha256'] or background_custody!=rec['custody']['background_sha256']:
        raise ValueError('saved grid/background custody does not reproduce')
    return ctx,pn,settings,spec,rec,arrays

def saved_shell(rec,lo):
    rows=[r for r in rec['shells'] if r['range_inverse_kpc']==[float(lo),float(lo+1)]]
    if len(rows)!=1:raise ValueError('unique saved shell required')
    return rows[0]

def validate(ctx,pn,rec,lo):
    row=saved_shell(rec,lo)
    new=pn['discrete_shell'](ctx,float(lo),float(lo+1))
    wanted={k:row[k] for k in ('eps_base','eps_refined','refinements','certified','levels')}
    if canonical(new)!=canonical(wanted):raise ValueError('saved discrete shell does not reproduce exactly')
    probes=[]
    for v in row['levels'].values():probes.append(np.asarray(v['dir_at_max'])*v['k_at_max_inverse_kpc']/ctx['L'].KPC)
    kv=np.asarray(probes);actual=pn['CC'].q_of(ctx['B'],kv);envelope=ctx['E'].q(kv,ctx['E'].t_of(kv))
    if not np.array_equal(actual,envelope):raise ValueError('Binder/envelope actual-node bitwise check')
    return dict(discrete_saved_record_exact=True,checked_discrete_levels=list(row['levels']),
                envelope_actual_bitwise=True,probe_count=len(kv),grid_background_custody_rederived=True,original_module_reference='UNTESTED: forbidden LWR loader not used')

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--row',required=True,type=int,choices=sorted(CASES))
    ap.add_argument('--shell-lo',required=True,type=int)
    ap.add_argument('--out',required=True)
    ap.add_argument('--dense',action='store_true')
    ap.add_argument('--reference-audit-lo',type=int)
    a=ap.parse_args()
    if not sys.flags.isolated or not sys.dont_write_bytecode:raise ValueError('Python -I -B required')
    if any(os.environ.get(k)!='1' for k in THREADS):raise ValueError('single-thread BLAS required')
    fence();out=lexical(a.out)
    if out.parent!=OUT or out.suffix!='.json':raise ValueError('output must be a new JSON directly under audit_path')
    if out.exists():raise FileExistsError(out)
    own=Path(__file__);own_start=canonical_safe(own).read_bytes()
    started=time.monotonic();case=CASES[a.row]
    ctx,pn,cfg,spec,rec,arrays=build_context(case)
    checks=validate(ctx,pn,rec,a.shell_lo)
    checks['existing_dense_reproduction']='NOT_RUN'
    if a.reference_audit_lo is not None:
        prior=[r for r in rec['envelope_audit'] if r['range_inverse_kpc']==[float(a.reference_audit_lo),float(a.reference_audit_lo+1)]]
        if len(prior)!=1:raise ValueError('reference shell has no saved dense audit')
        got=pn['search_envelope'](ctx,float(a.reference_audit_lo),float(a.reference_audit_lo+1),cfg,objective='EPS',audit=True,previous=None)
        if canonical(got)!=canonical(prior[0]['dense_search']):raise ValueError('existing dense audit does not reproduce exactly')
        checks['existing_dense_reproduction']=dict(exact=True,range_inverse_kpc=prior[0]['range_inverse_kpc'])
    row=saved_shell(rec,a.shell_lo);production=float(row['envelope']['estimate'])
    if not math.isfinite(production) or production<=0:raise ValueError('positive production envelope required')
    audit=pn['search_envelope'](ctx,float(a.shell_lo),float(a.shell_lo+1),cfg,objective='EPS',audit=True,previous=None) if a.dense else None
    # Verify the original inputs and wrapper again before publishing any evidence.
    for ref in list(SOURCES.values())+[GRID,case['spec'],case['record']]:pinned(ref)
    own_raw=canonical_safe(own).read_bytes()
    if sha(own_raw)!=sha(own_start):raise ValueError('audit wrapper changed during execution')
    result=dict(schema='UNT_EPS_NEGLIGIBLE_DENSE_AUDIT_CX2V001' if audit is not None else 'UNT_EPS_DENSE_AUDIT_VALIDATION_CX2V001',
        status='TESTED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),row=a.row,point_sha256=case['key'],
        settings='registered',registered_settings=cfg,source_record=pinref(case['record']),spec=pinref(case['spec']),
        original_producer=rec['producer'],audit_producer=dict(path=str(own),sha256=sha(own_raw)),
        range_inverse_kpc=[float(a.shell_lo),float(a.shell_lo+1)],production=production,
        dense=None if audit is None else audit['estimate'],dense_over_production=None if audit is None else audit['estimate']/production,
        dense_search=audit,checks=checks,identity=identity(spec),saved_custody=rec['custody'],
        custody_scope='Grid/background custody independently re-derived from exact pinned A2 arrays and spec; geometry/modules/row custody LINKED to saved EPS only, NOT re-derived; no driver/custody/anchor/run loader executed',
        arrays=arrays,effective_physical=dict(Eref_J=ctx['B'].Eref,gamma=ctx['B'].gam,ell_F_m=ctx['B'].ell,kpc_m=ctx['L'].KPC),
        source_pins={k:pinref(v) for k,v in SOURCES.items()},input_snapshot=list(READ_SNAPSHOTS.values()),extracted_definitions=EXTRACTIONS,
        project_module_imports=0,forward_or_solver_launches=0,production_admissible=False,rigorous_supremum=False,
        runtime_note='nice unavailable (sandbox); 0514 waiver',python=sys.executable,threads={k:os.environ[k] for k in THREADS},
        seconds=time.monotonic()-started,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(output=str(out),sha256=sha(out.read_bytes()),schema=result['schema'],dense_over_production=result['dense_over_production'])))

if __name__=='__main__':main()
