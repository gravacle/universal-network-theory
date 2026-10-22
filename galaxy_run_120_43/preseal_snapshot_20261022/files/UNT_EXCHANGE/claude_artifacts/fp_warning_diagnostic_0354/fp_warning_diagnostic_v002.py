"""Generic floating-point-warning diagnostic V002 (task 0354; V001 + default-warn probe and data-independence probe; V001 results retained). NO UNT matrices, spectra, frozen cases or output-derived numbers.
Runs a FIXED small set of probes, each in its own bounded subprocess (timeout 10 s; peak RSS recorded; one thread unless the
probe states otherwise), with warnings kept visible: every warning is captured with category, message, file and line and
aggregated in full (no truncation), and NumPy's floating-point status is additionally observed per operation through
np.errstate(all='call') + np.seterrcall. Each product is compared with an independent pure-Python scalar loop and, where
relevant, with a non-BLAS NumPy path (np.einsum, optimize=False). Integer-valued matrices make products exactly checkable.
Every probe result (pass or fail) is retained. Writes one JSON result file exclusively; never deletes anything.
Usage: python3 -B fp_warning_diagnostic_v002.py <new_results.json>     (run WITHOUT -I so the user-site NumPy is found)
"""
import json,os,subprocess,sys,time
SIZES=[2,4,8,15,16,17,24,32]
PROBE_SRC=r'''
import os,sys,json,warnings,resource
spec=json.loads(sys.argv[1])
import numpy as np
from collections import Counter
flags=Counter()
def _cb(kind,flag):flags[(spec_name[0],kind)]+=1
spec_name=['']
np.seterrcall(_cb)
def scalar_loop(A,B):
    n,k=len(A),len(A[0]);m=len(B[0])
    return [[sum(A[i][t]*B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]
def intmats(N):
    A=[[float((i+j)%7-3) for j in range(N)] for i in range(N)];B=[[float((2*i-j)%5-2) for j in range(N)] for i in range(N)];return A,B
def tridiag(N):
    T=np.zeros((N,N))
    for i in range(N):
        T[i,i]=2.0
        if i+1<N:T[i,i+1]=T[i+1,i]=-1.0
    return T
out={'probe':spec['name'],'numpy':np.__version__,'results':[]}
W=[]
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always')
    for N in spec['sizes']:
        r={'N':N}
        A,B=intmats(N);An,Bn=np.array(A),np.array(B);exact=np.array(scalar_loop(A,B))
        def op(name,fn):
            spec_name[0]='%s@N%d'%(name,N)
            with np.errstate(all=spec.get('errstate','call')):
                try:val=fn();r[name]={'finite':bool(np.all(np.isfinite(val)))};return val
                except FloatingPointError as e:r[name]={'raised':str(e)};return None
        if spec['name']=='data_independence':
            for lab,M in (('zeros',np.zeros((N,N))),('identity',np.eye(N)),('ones',np.ones((N,N)))):
                ex=np.array(scalar_loop(M.tolist(),M.tolist()))
                v=op('matmul_'+lab,lambda:M@M)
                if v is not None:r['matmul_'+lab]['equals_exact']=bool(np.array_equal(v,ex))
        elif spec['name'] in ('matmul_exact','matmul_exact_raise','matmul_exact_threads_unset','matmul_after_eigh','matmul_exact_warn'):
            if spec['name']=='matmul_after_eigh':
                T=tridiag(N);w,V=np.linalg.eigh(T);r['eigh_done']=True
            v=op('matmul',lambda:An@Bn)
            if v is not None:r['matmul']['equals_exact']=bool(np.array_equal(v,exact))
            v=op('dot',lambda:np.dot(An,Bn))
            if v is not None:r['dot']['equals_exact']=bool(np.array_equal(v,exact))
            v=op('einsum_nonblas',lambda:np.einsum('ij,jk->ik',An,Bn,optimize=False))
            if v is not None:r['einsum_nonblas']['equals_exact']=bool(np.array_equal(v,exact))
            v=op('matvec',lambda:An@Bn[:,0])
            if v is not None:r['matvec']['equals_exact']=bool(np.array_equal(v,exact[:,0]))
            v=op('transposed_view_matmul',lambda:An.T@Bn)
            if v is not None:r['transposed_view_matmul']['equals_exact']=bool(np.array_equal(v,np.array(scalar_loop([list(x) for x in zip(*A)],B))))
            v=op('fortran_order_matmul',lambda:np.asfortranarray(An)@np.asfortranarray(Bn))
            if v is not None:r['fortran_order_matmul']['equals_exact']=bool(np.array_equal(v,exact))
        elif spec['name']=='eig_residual_pattern':
            T=tridiag(N);w,V=np.linalg.eigh(T)
            res=op('residual_matmul',lambda:T@V-V*w)
            orth=op('orthogonality_matmul',lambda:V.T@V-np.eye(N))
            res_e=np.einsum('ij,jk->ik',T,V,optimize=False)-V*w;orth_e=np.einsum('ji,jk->ik',V,V,optimize=False)-np.eye(N)
            r['residual_matmul_vs_einsum_maxabs']=float(np.max(np.abs(res-res_e))) if res is not None else None
            r['orthogonality_matmul_vs_einsum_maxabs']=float(np.max(np.abs(orth-orth_e))) if orth is not None else None
            r['residual_max_einsum']=float(np.max(np.abs(res_e)));r['orthogonality_max_einsum']=float(np.max(np.abs(orth_e)))
            sp=op('spectral_inverse_matmul',lambda:(V/(w+1.0))@V.T)
            sp_e=np.einsum('ij,kj->ik',V/(w+1.0),V,optimize=False)
            r['spectral_inverse_matmul_vs_einsum_maxabs']=float(np.max(np.abs(sp-sp_e))) if sp is not None else None
            Rs=np.linalg.solve(T+np.eye(N),np.eye(N))
            rr=op('solve_residual_matmul',lambda:(T+np.eye(N))@Rs-np.eye(N))
            r['solve_vs_spectral_maxabs']=float(np.max(np.abs(Rs-sp_e)))
        out['results'].append(r)
out['warnings']=sorted([[k[0],k[1],k[2],k[3],c] for k,c in Counter((w.category.__name__,str(w.message),os.path.basename(w.filename),w.lineno) for w in W).items()])
out['warning_total']=len(W)
out['errcall_flags']=sorted([[k[0],k[1],c] for k,c in flags.items()])
out['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
out['thread_env']={v:os.environ.get(v) for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')}
print(json.dumps(out))
'''
CONFIG_SRC=r'''
import json,io,contextlib,numpy as np
cfg=None
try:cfg=np.show_config(mode='dicts')
except Exception as e:cfg={'error':repr(e)}
print(json.dumps({'numpy':np.__version__,'config':cfg},default=str))
'''
THREADS={'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'}
PROBES=[{'name':'matmul_exact_warn','sizes':[8,15,16,24],'threads':'1','errstate':'warn'},{'name':'data_independence','sizes':[8,16,24],'threads':'1'},{'name':'matmul_exact','sizes':SIZES,'threads':'1'},{'name':'matmul_exact_raise','sizes':[8,16,24],'threads':'1','errstate':'raise'},
 {'name':'matmul_exact_threads_unset','sizes':[8,16,24],'threads':'unset'},{'name':'matmul_after_eigh','sizes':[8,16,24],'threads':'1'},
 {'name':'eig_residual_pattern','sizes':[8,15,16,24],'threads':'1'}]
def run(src,arg,threads):
 env=dict(os.environ)
 for k in THREADS:env.pop(k,None)
 if threads=='1':env.update(THREADS)
 env.pop('PYTHONWARNINGS',None)
 t=time.monotonic()
 try:
  r=subprocess.run([sys.executable,'-B','-c',src]+([arg] if arg else []),capture_output=True,text=True,timeout=10,env=env)
  out={'returncode':r.returncode,'elapsed_s':time.monotonic()-t,'stderr':r.stderr[-2000:]}
  try:out['result']=json.loads(r.stdout.strip().splitlines()[-1])
  except Exception as e:out['parse_error']=repr(e);out['stdout_tail']=r.stdout[-1000:]
 except subprocess.TimeoutExpired:out={'timeout':True,'elapsed_s':time.monotonic()-t}
 return out
def main(argv):
 if len(argv)!=2:raise SystemExit('usage: fp_warning_diagnostic_v001.py <new_results.json>')
 res={'schema':'FP_WARNING_DIAGNOSTIC_V001','python':sys.version,'executable':sys.executable,'platform':sys.platform,
  'config':run(CONFIG_SRC,None,'1'),'probes':[]}
 for p in PROBES:
  r=run(PROBE_SRC,json.dumps(p),p['threads']);r['spec']=p;res['probes'].append(r)
 with open(argv[1],'x') as f:json.dump(res,f,indent=1)
 print('wrote',argv[1])
if __name__=='__main__':main(sys.argv)
