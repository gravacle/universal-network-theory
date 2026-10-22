"""0595 bounded component benchmark. No scientific launch or worker main.

A95 dispatch0613 permits default priority after taskpolicy refusal. Python-I-B. One K per invocation;
serial and N2/6/12 variants execute sequentially. All inputs pinned; exclusive
compact JSON outputs; no persistent cache writes, deletes or renames.
"""
import os
for _key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_key]=os.environ.get('CX3_VECLIB_MEASUREMENT_THREADS','1') if _key=='VECLIB_MAXIMUM_THREADS' else '1'
import argparse,hashlib,importlib.util,json,math,re,resource,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ART=ROOT.parent
UPC=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
RUN=UPC/'CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001'
MOD=ART/'tail_scheme_impl_c2/driver_r5/module'
PINS={
 'module':(MOD/'owned_uv_tail_lapse_v002.py','2026f2b6e21eba661ef97a5a2b6a8b73d0f8a2d5c3b995611c705f3dc6746a54'),
 'roster':(MOD/'uv_tail_source_roster_c2v001.py','4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'),
 'provider':(MOD/'posix_libm_bessel_jn_provider_c2v001.py','d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'),
 'prototype':(ROOT/'parallel_stars_prototype_cx3v002.py','f1daa12e71418cd565188b1760345b7c0b8c78c5705589e0918e5edf6d20e8c7'),
 'synthetic':(ROOT/'SYNTHETIC_INPUT_CX3V001.json','acbdf04bdc7d750668834d1d8bbdf49ad63c9605df7ea77d6a744dffaa80ee53'),
 'radial_surface':(UPC/'helpers/recovered_packet_audit/galaxy_baryonic_source_forward_v002.py','e9be043b46790e3493f4e427fb483a98a5665f004dfac287d5758afce0ac96ad'),
 'c4_arrays':(RUN/'stages/15_le2_rotation/rotation/rotation_base_arrays.npz','4e53085c8dc1d44b8a83a46eff4ae595ee3a64068ce544ba928d8b2abf9693cf'),
 'c4_seed':(RUN/'inputs/seed_c2v001.json','fc70a262b12773c6f60c93101bce9f499000b96a2c58c04e94e3691e9019df59'),
 'c4_result':(RUN/'result.json','aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee'),
 'profile':(UPC/'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json','f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'),
 'prior_i1t':(ART/'tail_scheme_impl_c2/kbig_timing_v003/out/TIMING_route_b_rot_KB0256_MS128_st_V003.json','616e4c3944bf3782152bd0acae384fac6f5910f08e82a0b25ebba4ded44b77ed'),
}
READ_ALLOW={str(p.resolve()) for p,h in PINS.values()}|{str(Path(__file__).resolve())}
READS=set();OUT=None
def audit(event,args):
    if event in ('os.remove','os.rename','os.rmdir','socket.connect','socket.getaddrinfo','os.system'):raise RuntimeError('FORBIDDEN_'+event)
    if event=='subprocess.Popen':
        cmd=args[1]
        allowed=isinstance(cmd,(list,tuple)) and ((Path(str(cmd[0])).name=='uname') or (len(cmd)==3 and Path(str(cmd[0])).name=='file' and cmd[1]=='-b' and Path(str(cmd[2])).resolve()==Path(sys.executable).resolve()))
        if not allowed:raise RuntimeError('SUBPROCESS_NOT_ALLOWED')
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        p=Path(os.fsdecode(args[0]));r=p.resolve();s=str(r).lower()
        if '/runs_ext/uvt_' in s or 'kmax_a2f10_c5h_run_v001' in s or '/.codex/' in s or '/.codex-alt/' in s:raise RuntimeError('PROTECTED_PATH')
        if 'ngc3198' in s and any(q in s for q in ('observed','velocit','rotmod')):raise RuntimeError('TARGET_PATH')
        write=isinstance(args[2],int) and args[2]&(os.O_WRONLY|os.O_RDWR)
        if write and str(r)!='/dev/null':
            if OUT is None or not r.is_relative_to(OUT) or p.exists() or not args[2]&os.O_EXCL:raise RuntimeError('WRITE_NOT_EXCLUSIVE_OUTPUT')
        elif '/Research/' in str(r):
            if str(r) not in READ_ALLOW:raise RuntimeError('UNPINNED_RESEARCH_READ '+str(r))
            READS.add(str(r))
sys.addaudithook(audit)
import numpy as np

def raw(name):
    p,h=PINS[name];b=p.read_bytes()
    if hashlib.sha256(b).hexdigest()!=h:raise ValueError('PIN_MISMATCH '+name)
    return b
def load(name,module_name):
    p,h=PINS[name];b=raw(name);sp=importlib.util.spec_from_file_location(module_name,p)
    m=importlib.util.module_from_spec(sp);sys.modules[module_name]=m;exec(compile(b,str(p),'exec'),m.__dict__);return m
U=load('module','cx3_tail_native');RS=load('roster','cx3_tail_roster');PV=load('provider','cx3_tail_provider')
PROTO=load('prototype','cx3_parallel_stars');FW=load('radial_surface','cx3_radial_surface')

class SyntheticRoster(RS.Roster):
    kind='synthetic'

def cpu(which):
    r=resource.getrusage(which);return r.ru_utime+r.ru_stime
def rss():return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
def snapshot():return {'wall':time.perf_counter(),'self':cpu(resource.RUSAGE_SELF),'children':cpu(resource.RUSAGE_CHILDREN)}
def elapsed(before):
    a=snapshot();return {'wall_s':a['wall']-before['wall'],'self_cpu_s':a['self']-before['self'],'children_cpu_s':a['children']-before['children'],'total_cpu_s':a['self']+a['children']-before['self']-before['children'],'peak_parent_rss_bytes':rss()}
def save(name,obj):
    data=(json.dumps(obj,indent=1,allow_nan=False)+'\n').encode()
    with (OUT/name).open('xb') as f:f.write(data)
    print(json.dumps({'written':str(OUT/name),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}),flush=True)
def norm_config(kbig,domain,quad,ms):
    return U.normalize_config({'enabled':True,'outer':{'shape':'cylinder','K_big_inverse_kpc':float(kbig)},'source_rule':'continuum_v001','gas':{'interp':'lagrange3_s_gl4','M_s':ms},'stars':{'segment_rule':'max16_ceil_kdr_plus8','tail_rule':'t_panels_40a_phase1p5_gl12'},'quadrature':quad,'domain':domain,'asymptote':'EH_exact_minus_quarter','lapse_only':True,'jet_order':{'route_a':1,'route_b':2,'ngc_eval':1},'lambda_scale':1.,'eps_certificate':U.TEST_ONLY_CERT,'lo_certificate':U.TEST_ONLY_CERT})

def prepare_case(case,kbig):
    if case=='synthetic':
        data=json.loads(raw('synthetic'));s=data['stars'];g=data['gas']
        edges=np.linspace(0.,g['outer_radius_kpc']**2,g['annuli']+1)
        R,rdr=RS.annulus_columns(edges,U.KPC_M)
        def make():
            stars=RS.StarsProfile(components=[s],height_kpc=s['height_kpc'],kpc_m=U.KPC_M,solar_mass_kg=data['solar_mass_kg'],segment_rule='max16_ceil_kdr_plus8',tail_rule='t_panels_40a_phase1p5_gl12',radial_surface=FW.radial_surface)
            gas=RS.GasColumns(s_edges_kpc2=edges,kpc_m=U.KPC_M,M_s=g['M_s'],column_R_m=R,column_rdr_m2=rdr,present=np.ones(len(R),bool),elements_z=[np.asarray(g['element_z_kpc'])*U.KPC_M for _ in R],elements_m=[np.full(len(g['element_z_kpc']),g['mass_kg_per_element']) for _ in R])
            return SyntheticRoster(stars=stars,gas=gas,provenance={'synthetic_input_sha256':PINS['synthetic'][1]})
        cfg=norm_config(kbig,data['domain'],data['quadrature'],g['M_s']);gamma=data['gamma_eff'];c=data['c_m_s']
        i1t={'verdict':'NOT_APPLICABLE_SYNTHETIC','scope':'newly saved synthetic registered-form roster; no galaxy inference'}
        note='Synthetic source and compact quadrature; no production timing claim.'
    else:
        import io
        profile=json.loads(raw('profile'));seed=json.loads(raw('c4_seed'))['numerical_inputs'];result=json.loads(raw('c4_result'))
        prior=json.loads(raw('prior_i1t'));i1t=prior['i1t'];assert i1t['verdict']=='PASS'
        assert prior['info']['source_rotation']==str(PINS['c4_arrays'][0].parent)
        with np.load(io.BytesIO(raw('c4_arrays')),allow_pickle=False) as ar:arrays={key:ar[key].copy() for key in ('rho0','volume_weights_m3','radial_nodes_m','z')}
        for a in arrays.values():a.flags.writeable=False
        R=arrays['radial_nodes_m'];edges=profile['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2']
        def make():
            stars=RS.stars_registered(profile,'DDO154',units={'kpc_m':seed['kpc_m'],'solar_mass_kg':seed['solar_mass_kg']},radial_surface=FW.radial_surface)
            return RS.roster_rotation(arrays,stars,s_edges_kpc2=edges,kpc_m=seed['kpc_m'],M_s=128)
        cfg=norm_config(kbig,{'R_eval_max_kpc':14.2,'z_eval_max_kpc':35.,'z_src_max_kpc':32.},{'order':8,'w_perp_max_inverse_kpc':.05,'w_z_max_inverse_kpc':.02},128)
        gamma=float(result['identity']['route_a']['custody']['physical']['gamma']);c=299792458.
        note='Exact pinned C4R3 component replay,72 source rotation radii; carried pinned prior I1T PASS, not independently rerun. TEST_ONLY certificates keep production_admissible false.'
    kept=U.kept_region('le_rotation',{'shape':'cube','kmax_inverse_kpc':None},4./U.KPC_M)
    kwargs=dict(config=cfg,kept=kept,gamma_eff=gamma,c_m_s=c,eval_radii_m=R,i1t=i1t,stage_kind='le_rotation')
    pos=np.array([[float(r)*math.cos(phi),float(r)*math.sin(phi),z*U.KPC_M] for r in R for phi,z in ((0.,0.),(.37,.1),(-.61,-.1))]+[[0.,0.,0.],[float(R[0]+R[1])/2,0.,.05*U.KPC_M]])
    return kwargs,make,pos,note

def thread_child(conn,case,kbig,threads):
    try:
        if os.environ['VECLIB_MAXIMUM_THREADS']!=str(threads):raise ValueError('THREAD_ENV_MISMATCH')
        kwargs,make,positions,note=prepare_case(case,kbig)
        before=snapshot();state=U.build(**dict(kwargs,roster=make(),jn_provider=PV.create_provider()));measured=elapsed(before)
        if state.record['production_admissible'] or rss()>=8*2**30:raise ValueError('SCOPE_OR_MEMORY_CAP')
        arrays={'table:'+k:np.ascontiguousarray(v) for k,v in state._a.items()}
        for order in (1,2):
            for k,v in state.jet(positions,order).items():arrays['jet%d:'%order+k]=np.ascontiguousarray(v)
        if rss()>=8*2**30:raise ValueError('POST_JET_MEMORY_CAP')
        measured['peak_after_jet_rss_bytes']=rss()
        pins={name:{'path':str(p),'resolved_path':str(p.resolve()),'sha256':h} for name,(p,h) in PINS.items() if str(p.resolve()) in READS}
        conn.send({'ok':True,'arrays':arrays,'record':state.record,'digest':state.digest,'measured':measured,'threads':threads,'probes':len(positions),'scope':note,'pins':pins,'backend':getattr(np.__config__,'CONFIG',{}),'env':{k:os.environ[k] for k in PROTO.THREAD_KEYS},'pid':os.getpid()})
    except BaseException as e:
        conn.send({'ok':False,'error':type(e).__name__+': '+str(e)})
    finally:conn.close()

def main():
    global OUT
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=('synthetic','c4r3'),required=True);parser.add_argument('--kbig',type=int,choices=(32,128,256),required=True);parser.add_argument('--workers',default='2,6,12');parser.add_argument('--tag',required=True);parser.add_argument('--veclib-six-repeats',type=int,choices=(0,1,2),default=0)
    args=parser.parse_args();PROTO._env();workers=[int(s) for s in args.workers.split(',')]
    if not workers or any(n not in (2,6,12) for n in workers) or len(set(workers))!=len(workers):raise ValueError('WORKER_LIST')
    if not re.fullmatch('[A-Za-z0-9_]+',args.tag):raise ValueError('TAG')
    if not sys.flags.isolated or not sys.dont_write_bytecode:raise ValueError('REQUIRES_I_B')
    OUT=ROOT/'runs'/args.tag;OUT.mkdir(parents=True,exist_ok=False)
    start=time.time();kwargs,make,positions,note=prepare_case(args.case,args.kbig)
    provenance={name:{'path':str(p),'resolved_path':str(p.resolve()),'sha256':h} for name,(p,h) in PINS.items() if str(p.resolve()) in READS}
    save('INPUTS_V001.json',{'scope':note,'case':args.case,'kbig':args.kbig,'workers':workers,'config':kwargs['config'],'gamma_eff':kwargs['gamma_eff'],'n_eval_radii':len(kwargs['eval_radii_m']),'jet_probe_count':len(positions),'pins':provenance,'runner':{'path':str(Path(__file__)),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'env':{k:os.environ[k] for k in PROTO.THREAD_KEYS},'loadavg':list(os.getloadavg()),'utc':time.strftime('%Y-%m-%d %H:%M:%S UTC',time.gmtime())})
    before=snapshot();serial=U.build(**dict(kwargs,roster=make(),jn_provider=PV.create_provider()));baseline=elapsed(before)
    baseline.update(state_digest=serial.digest,memory_estimate_bytes=serial.record['memory_estimate_bytes'],grid=serial.record['quadrature'],rank=serial.record['rank'],production_admissible=serial.record['production_admissible'])
    if serial.record['production_admissible'] or rss()>=8*2**30:raise RuntimeError('SCOPE_OR_MEMORY_CAP')
    save('SERIAL_V001.json',baseline)
    rows=[]
    for n in workers:
        before=snapshot();parallel,meta=PROTO.build_with_parallel_stars(U,dict(kwargs,roster=make(),jn_provider=PV.create_provider()),n,PINS['provider'][0]);measured=elapsed(before)
        before_cmp=time.perf_counter();comparison=PROTO.compare_all_arrays_and_jets(serial,parallel,positions);cmp_s=time.perf_counter()-before_cmp
        item={'workers':n,'measured':measured,'wall_speedup':baseline['wall_s']/measured['wall_s'],'total_cpu_ratio':measured['total_cpu_s']/baseline['total_cpu_s'],'comparison_wall_s':cmp_s,'comparison':comparison,'prototype':meta,'realized_worker_pids':sorted({b['pid'] for w in meta['preparation']['work'] for b in w['blocks']}),'blocks_per_component_pass':[len(w['blocks']) for w in meta['preparation']['work']],'loadavg':list(os.getloadavg()),'peak_parent_rss_after_comparison':rss()}
        ok=comparison['all_byte_equal'] and comparison['record_equal'] and comparison['state_digest_equal'] and rss()<8*2**30 and meta['preparation']['peak_worker_rss_bytes']<8*2**30
        item['status']='TESTED_PASS' if ok else 'TESTED_FAIL';save('N%02d_V001.json'%n,item);rows.append({k:item[k] for k in ('workers','status','measured','wall_speedup','total_cpu_ratio','realized_worker_pids','blocks_per_component_pass')})
        if not ok:raise RuntimeError('BYTE_OR_MEMORY_COMPARISON_FAILED')
        del parallel

    thread_rows=[]
    if args.veclib_six_repeats:
        import multiprocessing
        ctx=multiprocessing.get_context('spawn')
        baseline_arrays={'table:'+k:np.ascontiguousarray(v) for k,v in serial._a.items()}
        for order in (1,2):
            for k,v in serial.jet(positions,order).items():baseline_arrays['jet%d:'%order+k]=np.ascontiguousarray(v)
        for ordinal in range(args.veclib_six_repeats):
            PROTO._env()
            parent,child=ctx.Pipe(duplex=False)
            old=os.environ.get('CX3_VECLIB_MEASUREMENT_THREADS');os.environ['CX3_VECLIB_MEASUREMENT_THREADS']='6'
            try:
                proc=ctx.Process(target=thread_child,args=(child,args.case,args.kbig,6));proc.start()
            finally:
                if old is None:os.environ.pop('CX3_VECLIB_MEASUREMENT_THREADS',None)
                else:os.environ['CX3_VECLIB_MEASUREMENT_THREADS']=old
            child.close();result=parent.recv();parent.close();proc.join();PROTO._env()
            if proc.exitcode or not result['ok']:raise RuntimeError('THREAD_CHILD_FAILED '+str(result))
            if rss()>=8*2**30:raise ValueError('THREAD_PARENT_RECEIVE_MEMORY_CAP')
            arrays=result.pop('arrays');record=result.pop('record');digest=result.pop('digest')
            if set(arrays)!=set(baseline_arrays):raise ValueError('THREAD_ARRAY_KEYS')
            comparisons=[]
            for key in sorted(arrays):
                a=arrays[key];b=baseline_arrays[key];ab=a.tobytes();bb=b.tobytes()
                comparisons.append({'name':key,'shape':list(a.shape),'dtype':str(a.dtype),'byte_equal':a.shape==b.shape and a.dtype==b.dtype and ab==bb,'baseline_sha256':hashlib.sha256(bb).hexdigest(),'this_sha256':hashlib.sha256(ab).hexdigest()})
            result.update(ordinal=ordinal,state_digest=digest,all_arrays_byte_equal=all(c['byte_equal'] for c in comparisons),record_equal=record==serial.record,digest_equal=digest==serial.digest,arrays=comparisons,parent_peak_after_compare_rss_bytes=rss())
            if rss()>=8*2**30:raise ValueError('THREAD_PARENT_COMPARE_MEMORY_CAP')
            result['status']='TESTED_PASS' if result['all_arrays_byte_equal'] and result['record_equal'] and result['digest_equal'] else 'TESTED_FAIL'
            result['scope_limit']='VECLIB_MAXIMUM_THREADS configuration comparison, actual thread concurrency unmeasured; direct bytes against same-invocation cold serial1 baseline. No universal determinism or production admission.'
            save('THREADS6_REPEAT%d_V001.json'%ordinal,result)
            thread_rows.append({k:result[k] for k in ('threads','ordinal','status','measured','all_arrays_byte_equal','record_equal','digest_equal','pid','parent_peak_after_compare_rss_bytes')})
            del arrays,result
    save('SUMMARY_V001.json',{'status':'TESTED_PASS' if all(t['status']=='TESTED_PASS' for t in thread_rows) else 'TESTED_FAIL','scope':note,'case':args.case,'kbig':args.kbig,'serial':baseline,'rows':rows,'thread_rows':thread_rows,'thread_comparison_status':'TESTED_PASS' if thread_rows and all(t['status']=='TESTED_PASS' for t in thread_rows) else ('TESTED_FAIL' if thread_rows else 'UNTESTED'),'elapsed_total_s':time.time()-start,'scientific_launches':0,'target_reads':0,'cache_storage_used':False,'process_background_policy':'DEFAULT_PRIORITY under Claude2 dispatch0613 A95 sha256 82c214dfe8729603ccea43f803cc091f5b484f4b2fa09147ea57955a1a0f1377; previous sandbox taskpolicy preflight refused; no escalation'})

if __name__=='__main__':main()
