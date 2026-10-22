"""Out-of-tree cold-tail process prototype for dispatch0595.

Only the existing independent256-k stellar batches are dispatched. Each batch
retains the original Bessel input shape, global kmax-derived nodes, GEMV, and
component/doubling accumulation order. U.build remains unchanged and consumes
the populated exact-key in-process stellar cache. No worker/main/solver calls.

Caller uses prescribed Python-I-B and BLAS1. A95 permits default priority after
taskpolicy refusal. Numerical certification remains external byte comparisons.
"""
import concurrent.futures
import hashlib
import importlib.util
import math
import multiprocessing
import os
from pathlib import Path
import resource
import sys
import time
import numpy as np

ROSTER_SHA='4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2'
PROVIDER_SHA='d6c55b55c701a7172e6eaf86ef3f0fedb7f5b2de32d3dbeb06c1bbee471d3171'
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
CAP=8*2**30
_WORKER=None

def _pin(path,expected):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('PROTOTYPE_PIN_MISMATCH '+str(path))
    return raw

def _env():
    if any(os.environ.get(k)!='1' for k in THREAD_KEYS):raise ValueError('PROTOTYPE_REQUIRES_BLAS1')
    if not sys.flags.isolated or not sys.dont_write_bytecode:raise ValueError('PROTOTYPE_REQUIRES_ISOLATED_NO_BYTECODE')

def _cpu():
    r=resource.getrusage(resource.RUSAGE_SELF);return r.ru_utime+r.ru_stime

def _rss():
    v=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(v if sys.platform=='darwin' else v*1024)

def _init_worker(provider_path,R,M):
    global _WORKER
    _env();raw=_pin(provider_path,PROVIDER_SHA)
    sp=importlib.util.spec_from_file_location('_cx3_parallel_provider',provider_path)
    mod=importlib.util.module_from_spec(sp);exec(compile(raw,str(provider_path),'exec'),mod.__dict__)
    _WORKER=(mod.create_provider(),R,M)

def _one_batch(task):
    index,k=task;jn,R,M=_WORKER
    # Same expression/shape as the original StarsProfile.radial_transform batch.
    c0=_cpu();t0=time.perf_counter()
    out=jn.j0(k[:,None]*R[None,:]) @ M
    rss=_rss()
    if rss>=CAP:raise MemoryError('PROTOTYPE_WORKER_RSS_CAP')
    return index,out,{'pid':os.getpid(),'cpu_s':_cpu()-c0,'wall_s':time.perf_counter()-t0,'peak_rss_bytes':rss}

def _bounded_batches(pool,k,workers):
    # At most N outstanding small-result futures; consume in serial index order.
    starts=iter(range(0,len(k),256));pending=[]
    for _ in range(workers):
        a=next(starts,None)
        if a is not None:pending.append(pool.submit(_one_batch,(a,k[a:min(a+256,len(k))])))
    while pending:
        fut=pending.pop(0);yield fut.result()
        a=next(starts,None)
        if a is not None:pending.append(pool.submit(_one_batch,(a,k[a:min(a+256,len(k))])))

def populate_exact_stars_cache(stars,k_perp_m,provider_path,workers):
    """Populate the native cache and certificates with parallel batch arithmetic.

    Return measurement metadata. Tables/jets still require full byte validation.
    No global class/function monkeypatch; no files written by this function.
    """
    _env()
    if type(workers) is not int or workers not in (2,6,12):raise ValueError('N must be2,6,12')
    source=Path(type(stars).radial_transform.__code__.co_filename)
    _pin(source,ROSTER_SHA);_pin(provider_path,PROVIDER_SHA)
    if type(stars).__name__!='StarsProfile' or 'radial_transform' in vars(stars) or '_nodes' in vars(stars):
        raise ValueError('PROTOTYPE_REQUIRES_UNMODIFIED_REGISTERED_STARS')
    k=np.asarray(k_perp_m,dtype=float)
    if k.ndim!=1 or not k.size or not np.all(np.isfinite(k)):raise ValueError('PROTOTYPE_K_SHAPE')
    ck=hashlib.sha256(np.ascontiguousarray(k).tobytes()).hexdigest()
    cache=stars.__dict__.setdefault('_cache',{})
    if ck in cache:raise ValueError('PROTOTYPE_COLD_CACHE_REQUIRED')
    kmax_kpc=float(np.max(k))*stars.kpc_m
    out=np.zeros(k.shape);out2=np.zeros(k.shape);records=[]
    started=time.perf_counter();c0=_cpu()
    for comp_index,comp in enumerate(stars.components):
        for mult,acc in ((1,out),(2,out2)):
            R,M=stars._nodes(comp,kmax_kpc,mult)
            # Conservative scratch estimate for provider unique/inverse and GEMV.
            estimate=96*min(256,len(k))*len(R)+8*(len(R)+len(M)+len(k))
            if estimate>6*2**30:raise MemoryError('PROTOTYPE_SCRATCH_ESTIMATE_CAP')
            node_hash=hashlib.sha256(np.ascontiguousarray(R).tobytes()+np.ascontiguousarray(M).tobytes()).hexdigest()
            blocks=[]
            with concurrent.futures.ProcessPoolExecutor(max_workers=workers,mp_context=multiprocessing.get_context('spawn'),initializer=_init_worker,initargs=(str(provider_path),R,M)) as pool:
                for a,value,measured in _bounded_batches(pool,k,workers):
                    # Preserve original +=, including initial signed-zero handling.
                    acc[a:a+len(value)]+=value
                    blocks.append(dict(start=a,count=len(value),**measured))
            records.append({'component':comp_index,'doubling_multiplier':mult,'nodes_sha256':node_hash,'node_count':len(R),'scratch_estimate_bytes':estimate,'blocks':blocks})
    scale=float(np.max(np.abs(out))) if out.size else 0.0
    rel=float(np.max(np.abs(out-out2))/scale) if scale>0 else 0.0
    cert=dict(kind='stars_radial_doubling',k_max_inverse_kpc=kmax_kpc,n_k=int(k.size),max_rel_change=rel,rtol=1e-10,verdict='PASS' if rel<=1e-10 else 'FAIL')
    stars.certificates.append(cert)
    if rel>1e-10:raise ValueError('UV_TAIL_STARS_TRANSFORM_UNCERTIFIED max_rel_change=%.3e'%rel)
    cache[ck]=out.copy()
    return {'schema':'CX3_PARALLEL_STARS_PROTOTYPE_V002','workers':workers,'wall_s':time.perf_counter()-started,'parent_cpu_s':_cpu()-c0,'worker_task_cpu_s':sum(b['cpu_s'] for rec in records for b in rec['blocks']),'peak_worker_rss_bytes':max(b['peak_rss_bytes'] for rec in records for b in rec['blocks']),'parent_peak_rss_bytes':_rss(),'k_sha256':ck,'certificate':cert,'work':records,'provider_pin':{'path':str(provider_path),'sha256':PROVIDER_SHA},'roster_pin':{'path':str(source),'sha256':ROSTER_SHA}}

def build_with_parallel_stars(U,build_kwargs,workers,provider_path):
    """Unmodified full cold U.build after out-of-tree parallel star preparation.

    Only continuum registered stars are supported. Spherical residual grids are
    deliberately left to the unchanged native serial builder. The record/table
    comparison must establish identity before any production consideration.
    """
    _env();config=build_kwargs['config'];kept=build_kwargs['kept'];roster=build_kwargs['roster']
    if U.domain_is_empty(kept,config['outer']):raise ValueError('PROTOTYPE_REQUIRES_NONEMPTY_BUILD')
    if getattr(roster,'stars',None) is None:raise ValueError('PROTOTYPE_REQUIRES_STARS')
    g=U._grid(kept,config['outer'],config['quadrature'],config['domain']['R_eval_max_kpc'])
    kp=g['kp']/U.KPC_M
    t0=time.perf_counter();c0=_cpu()
    prep=populate_exact_stars_cache(roster.stars,kp,provider_path,workers)
    state=U.build(**build_kwargs)
    return state,{'status':'UNVALIDATED_PROTOTYPE_OUTPUT','wall_s':time.perf_counter()-t0,'parent_cpu_s':_cpu()-c0,'worker_task_cpu_s':prep['worker_task_cpu_s'],'preparation':prep}

def compare_all_arrays_and_jets(serial,parallel,positions,orders=(1,2)):
    """Byte comparisons; hashing is secondary evidence, not the equality test."""
    table=[]
    def compare(name,a,b):
        a=np.ascontiguousarray(a);b=np.ascontiguousarray(b);x=a.tobytes();y=b.tobytes()
        return {'name':name,'equal':a.dtype==b.dtype and a.shape==b.shape and x==y,'shape':list(a.shape),'dtype':str(a.dtype),'serial_sha256':hashlib.sha256(x).hexdigest(),'parallel_sha256':hashlib.sha256(y).hexdigest()}
    if set(serial._a)!=set(parallel._a):raise ValueError('PROTOTYPE_ARRAY_KEYS_DIFFER')
    for key in sorted(serial._a):table.append(compare('table:'+key,serial._a[key],parallel._a[key]))
    for order in orders:
        a=serial.jet(positions,order);b=parallel.jet(positions,order)
        if set(a)!=set(b):raise ValueError('PROTOTYPE_JET_KEYS_DIFFER')
        for key in sorted(a):table.append(compare('jet%d:'%order+key,a[key],b[key]))
    return {'all_byte_equal':all(r['equal'] for r in table),'record_equal':serial.record==parallel.record,'state_digest_equal':serial.digest==parallel.digest,'arrays':table}
