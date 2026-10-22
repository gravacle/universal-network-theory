"""Claude3 independent synthetic equivalence test for the parallel route-A solver (dispatch 0480).
Reviewed solver vs parallel N=1,3,4 on the author's synthetic problem builder (read-only); failure case; determinism;
source-split block equivalence incl. a deliberately misaligned split. <=4 worker processes. Writes only to its outdir."""
import sys, os, json, hashlib, pickle, time, importlib.util, numpy as np
sys.path.insert(0,'/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/tests/syn_env')
spec=importlib.util.spec_from_file_location('sp','/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts/parallel_route_a_c2/tests/syn_env/syn_problem_c2v001.py'); sp=importlib.util.module_from_spec(spec); spec.loader.exec_module(sp)
out_dir=sys.argv[1]; os.makedirs(out_dir,exist_ok=True)
mods=sp.modules()
def digest(o):
    # Alias-insensitive canonical digest: values, dtypes, shapes and key order only (pickle memo references would
    # differ between serial and parallel outputs because worker results are copies, which is disclosed in the INTERFACE).
    def norm(x):
        if isinstance(x,np.ndarray): return ['nd',x.dtype.str,list(x.shape),hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()]
        if isinstance(x,dict): return ['d',[[str(k),norm(v)] for k,v in x.items() if k!='checkpoint']]
        if isinstance(x,(list,tuple)): return ['l',[norm(v) for v in x]]
        if isinstance(x,np.generic): return ['ng',str(x.dtype),x.tobytes().hex()]
        if isinstance(x,float): return ['f',x.hex()]
        if isinstance(x,complex): return ['c',x.real.hex(),x.imag.hex()]
        if isinstance(x,(int,bool,str)) or x is None: return [type(x).__name__,x]
        return ['o',type(x).__name__,repr(x)]
    return hashlib.sha256(json.dumps(norm(o)).encode()).hexdigest()
R={'solver_sha':{k:hashlib.sha256(open(p,'rb').read()).hexdigest()[:16] for k,p in (('reviewed',sp.PATHS['reviewed_solver']),('parallel',sp.PATHS['parallel_solver']))}}
def run(solver,N,build,cfg):
    p=sp.build(mods,**build); ev=[]; kw=dict(p,progress_callback=ev.append,**cfg); t=time.monotonic()
    out=mods['reviewed_solver'].solve(**kw) if solver=='reviewed' else mods['parallel_solver'].solve(**kw,column_workers=N)
    rep=mods['parallel_solver'].last_pool_report() if solver!='reviewed' else None
    return digest(out),digest(ev),out,time.monotonic()-t,rep
if __name__=='__main__':
    cases={'exhausted_vertical':(dict(vertical=True,n_radii=2,n_phi=4),dict(max_iterations=2,source_rtol=0.0)),
           'converged_nonvertical':(dict(vertical=False,n_radii=2,n_phi=4),dict(max_iterations=4,source_rtol=0.5))}
    for name,(build,cfg) in cases.items():
        ref=run('reviewed',1,build,cfg); rows={'reviewed':{'out':ref[0][:16],'events':ref[1][:16],'converged':ref[2].get('converged_finite_fixed_point'),'wall_s':round(ref[3],2)}}
        for N in (1,3,4,3):
            r=run('parallel',N,build,cfg)
            label=f'N{N}' if f'N{N}' not in rows else f'N{N}_repeat'
            rows[label]={'out_equal_reviewed':r[0]==ref[0],'events_equal_reviewed':r[1]==ref[1],'wall_s':round(r[3],2),'workers':(r[4] or {}).get('workers'),'source_split':(r[4] or {}).get('source_split'),'worker_blas':(r[4] or {}).get('worker_blas_env')}
        R[name]=rows
    # failure case: column 5 with a budget failure -> same failure record (type/message/column_index) and same outcome
    build=dict(vertical=True,n_radii=2,n_phi=4,bad=((5,'budget'),)); cfg=dict(max_iterations=2,source_rtol=0.0)
    ref=run('reviewed',1,build,cfg); par=run('parallel',3,build,cfg)
    R['failure_case']={'reviewed_failure':{k:ref[2]['failure'][k] for k in ('type','message','iteration','column_index')} if 'failure' in ref[2] else None,
     'parallel_failure':{k:par[2]['failure'][k] for k in ('type','message','iteration','column_index')} if 'failure' in par[2] else None,
     'out_equal':ref[0]==par[0],'events_equal':ref[1]==par[1],'n_gas_columns_before_failure':(len(ref[2].get('gas_columns',[])),len(par[2].get('gas_columns',[])))}
    # TypeError in a column propagates with the same type/message
    build=dict(vertical=True,n_radii=2,n_phi=4,bad=((2,'typeerror'),))
    def catch(solver,N):
        try: run(solver,N,build,cfg); return None
        except Exception as e: return (type(e).__name__,str(e)[:120])
    R['typeerror_case']={'reviewed':catch('reviewed',1),'parallel_N3':catch('parallel',3)}
    # source split: full vs chunk-aligned blocks vs misaligned blocks
    src=mods['source']; rng=np.random.default_rng(7); nk=1000; ne=700
    waves=rng.normal(size=(nk,3))*1e-19; pos=rng.normal(size=(ne,3))*3e19; J=rng.normal(size=(ne,10,1))*1e30
    full=np.asarray(src.physical_source_fourier(physical_positions_m=pos,integrated_columns_J=J,k_physical_inverse_m=waves),dtype=complex)
    def split(edges):
        return np.concatenate([np.asarray(src.physical_source_fourier(physical_positions_m=pos,integrated_columns_J=J,k_physical_inverse_m=waves[a:b]),dtype=complex) for a,b in zip(edges,edges[1:])],axis=0)
    aligned=[0,64,320,640,nk]; misaligned=[0,50,333,777,nk]
    R['source_split']={'aligned_blocks_bitwise_equal':np.array_equal(split(aligned).view(np.uint8),full.view(np.uint8)),'misaligned_blocks_bitwise_equal':np.array_equal(split(misaligned).view(np.uint8),full.view(np.uint8)),'misaligned_max_abs_diff':float(np.max(np.abs(split(misaligned)-full)))}
    json.dump(R,open(os.path.join(out_dir,'SYNTHETIC_EQUIVALENCE_C3V001.json'),'w'),indent=1,default=str); print(json.dumps(R,indent=1,default=str))
