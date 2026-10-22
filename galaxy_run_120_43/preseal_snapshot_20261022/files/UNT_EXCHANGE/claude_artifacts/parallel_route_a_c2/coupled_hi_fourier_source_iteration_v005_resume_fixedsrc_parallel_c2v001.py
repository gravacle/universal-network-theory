"""Inert finite Fourier/HI source fixed-point iteration, no coefficient fallback.
One actual combined source family per call. Rest-energy source approximation.
Uniform physical Cartesian background chart; full metric anisotropy retained.
RESUME c2v001 (Claude2 0422): optional exact restart at a completed HI-column
boundary via an injected checkpoint module. checkpoint=None executes v005.
FIXEDSRC c2v001 (Claude2 0424): optional fixed_source_fourier_J. Omitted (None),
the fixed term is evaluated exactly as before. Supplied, that validated array is
the fixed term; fixed positions/columns are kept only as provenance.
PARALLEL c2v001 (Claude2 parallel_route_a_c2): optional column_workers=N (call
argument of solve). N=1 (default) executes the reviewed serial statements. N>1
solves each iteration's fresh HI columns in N spawned worker processes (one BLAS
thread each) and consumes them strictly in column order through the SAME failure
handler, checkpoint writes, progress events and source accumulation. The gas
source transform is split by wave rows only for an admitted row-separable source
module. No numerics, tolerances, guards or records change; see INTERFACE note.
"""
import math
import numpy as np
import collections
import functools
import hashlib
import importlib
import importlib.util
import io
import marshal
import multiprocessing
import multiprocessing.connection
import os
import pathlib
import pickle
import sys
import traceback
import types


def _finite(a,name):
    a=np.asarray(a)
    if not np.all(np.isfinite(a)): raise ValueError(name+': nonfinite')
    return a


def _supplied_fixed_source(value,wave_count):
    """Validated private C-order copy of a supplied fixed term. No conversion:
    a native complex128 ndarray (the evaluated term's dtype) of exact shape
    [wave_count,10,1] with finite entries is required."""
    if type(value) is not np.ndarray or value.dtype!=np.dtype(complex):
        raise ValueError('fixed_source_fourier_J: native complex128 numpy array required; no conversion')
    if value.shape!=(wave_count,10,1):
        raise ValueError('fixed_source_fourier_J: exact shape [len(waves),10,1] required')
    _finite(value,'fixed_source_fourier_J')
    return np.array(value,dtype=complex,order='C',copy=True)


MAX_COLUMN_WORKERS=64


def solve(*, fixed_positions_m, fixed_integrated_columns_J, initial_gas_fourier_J,
          gas_columns, fourier_arguments, boundary_jet_at_positions,
          source_module, fourier_module, metric_module, hi_module, quadrature_module,
          c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
          reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None,
          checkpoint=None, fixed_source_fourier_J=None, column_workers=1):
    """Reviewed v005/resume/fixedsrc solve (contract in _solve) plus column_workers.
    column_workers=1: exactly the reviewed serial path (no pool, no processes).
    column_workers=N>1: min(N,len(gas_columns)) spawned processes solve the fresh
    columns of each iteration; results are consumed in column order, so the first
    failing column in column order is the reported failure and no later column is
    used or written. N is NOT checkpoint identity: a run may resume with any N.
    Pool/transport failures raise ColumnPoolError (a RuntimeError, never recorded
    as a physical column failure); committed checkpoint records stay resumable.
    """
    if type(column_workers) is not int or not 1<=column_workers<=MAX_COLUMN_WORKERS:
        raise ValueError('column_workers: explicit int 1..%d required'%MAX_COLUMN_WORKERS)
    call=dict(fixed_positions_m=fixed_positions_m,fixed_integrated_columns_J=fixed_integrated_columns_J,
        initial_gas_fourier_J=initial_gas_fourier_J,gas_columns=gas_columns,
        fourier_arguments=fourier_arguments,boundary_jet_at_positions=boundary_jet_at_positions,
        source_module=source_module,fourier_module=fourier_module,metric_module=metric_module,
        hi_module=hi_module,quadrature_module=quadrature_module,c_m_s=c_m_s,
        max_iterations=max_iterations,relaxation=relaxation,source_atol_J=source_atol_J,
        source_rtol=source_rtol,reality_atol=reality_atol,reality_rtol=reality_rtol,
        vertical_fourier_module=vertical_fourier_module,progress_callback=progress_callback,
        checkpoint=checkpoint,fixed_source_fourier_J=fixed_source_fourier_J)
    if column_workers==1:
        return _solve(**call,pool=None)
    pool=_ColumnPool(column_workers)
    try:
        return _solve(**call,pool=pool)
    finally:
        pool.close()


def bind_column_workers(column_workers):
    """Module-shaped view of THIS file whose solve fixes column_workers (for callers
    such as the reviewed composite adapter that call solver_module.solve with a
    fixed keyword set). __file__ is this file, so caller pins are unchanged."""
    if type(column_workers) is not int or not 1<=column_workers<=MAX_COLUMN_WORKERS:
        raise ValueError('column_workers: explicit int 1..%d required'%MAX_COLUMN_WORKERS)
    view=types.ModuleType(__name__+'_column_workers_%d'%column_workers)
    view.__file__=__file__
    view.__doc__='solve() of %s with column_workers=%d'%(__file__,column_workers)
    view.solve=functools.partial(solve,column_workers=column_workers)
    view.column_workers=column_workers
    view.cylindrical_metric_covector_to_registered=cylindrical_metric_covector_to_registered
    return view


def _solve(*, fixed_positions_m, fixed_integrated_columns_J, initial_gas_fourier_J,
          gas_columns, fourier_arguments, boundary_jet_at_positions,
          source_module, fourier_module, metric_module, hi_module, quadrature_module,
          c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
          reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None,
          checkpoint=None, fixed_source_fourier_J=None, pool=None):
    """Required actual inputs:
    fixed positions[n,3]/J[n,10,1]: stellar,H2,exterior etc already integrated,
    with source components in REGISTERED chart. Unknown sources never filled.
    initial_gas_fourier_J[nk,10,1]: explicit iteration initialization, not accepted
    preparation; all final gas columns are reconstructed from actual metric.
    gas_columns each: R_m,phi,radial_weight_m,azimuth_weight_rad,Sigma_kg_m2,
    hi_options(sigma0_m_s,gamma,search/root/panel budgets).
    fourier_arguments: actual complete source_hessian_grid, kphysical,dkweights,
    registered chart/background/calibration and reviewed binding modules/tolerances.
    boundary_jet_at_positions(pos) supplies boundary_fields/gradient/hessian,
    including chosen zero-mode/boundary PERTURBATIONS; no zero default.
    N=1,Cbar are restored separately by the metric evaluator, never in these arrays.
    Reference field order n,C6,mu3. No axisymmetry imposed on response.
    checkpoint=None (default) runs the v005 statements. Otherwise dict(module=
    coupled_gas_checkpoint_c2v001, directory, mode='new'|'resume', caller_identity=
    dict(code_pins,boundary_prescription,physical_parameters,numerical_controls)).
    Resume restores the actual iteration, stored gas iterate, history and ordered
    complete column solutions; identity/integrity/chain mismatch is rejected.
    fixed_source_fourier_J=None (default) evaluates the fixed term from fixed
    positions/J with source_module, as above. If supplied (finite native complex128
    ndarray [len(k_physical),10,1]) a private copy IS the fixed term: no angular
    stellar quadrature is re-evaluated, and fixed positions/J are still required,
    unmodified and unused, as provenance (checkpoint identity digests). The gas
    iterate and every updated gas transform are unchanged: actual phi columns
    through source_module. A supplied term requires a checkpoint module declaring
    FIXED_SOURCE_SELECTION_IDENTITY (coupled_gas_checkpoint_c2v003 or later).
    """
    if type(max_iterations)is not int or max_iterations<1: raise ValueError('Iteration budget required')
    if not 0<relaxation<=1 or source_atol_J<0 or source_rtol<0 or reality_atol<0 or reality_rtol<0:
        raise ValueError('Explicit nonnegative tolerances and 0<relaxation<=1 required')
    if not all(math.isfinite(v) for v in (relaxation,source_atol_J,source_rtol,reality_atol,reality_rtol,c_m_s)) or c_m_s<=0:
        raise ValueError('Finite settings and positive c required')
    if not gas_columns: raise ValueError('Actual gas columns required')
    args=dict(fourier_arguments); waves=args['k_physical']
    if fixed_source_fourier_J is None:
        fixed=np.asarray(source_module.physical_source_fourier(physical_positions_m=fixed_positions_m,
            integrated_columns_J=fixed_integrated_columns_J,k_physical_inverse_m=waves),dtype=complex)
    else:
        # Supplied fixed term used as given; never re-evaluated or added to gas.
        fixed=_supplied_fixed_source(fixed_source_fourier_J,len(waves))
    gas=np.asarray(initial_gas_fourier_J,dtype=complex)
    if gas.shape!=fixed.shape or gas.shape[1:]!=(10,1): raise ValueError('Single actual combined source [nk,10,1] required')
    _finite(gas,'initial gas')
    if pool is not None:
        # PARALLEL: workers are spawned and the column environment is proven
        # shippable BEFORE any checkpoint record exists; failure here writes nothing.
        pool.start(column_environment=dict(boundary_jet_at_positions=boundary_jet_at_positions,
            fourier_module=None if vertical_fourier_module is not None else
                types.SimpleNamespace(evaluate_prepared=fourier_module.evaluate_prepared),
            metric_module=metric_module,hi_module=hi_module,quadrature_module=quadrature_module,
            vertical_fourier_module=vertical_fourier_module,
            args={'Cbar':args['Cbar'],'mubar':args['mubar']},c_m_s=c_m_s,
            reality_atol=reality_atol,reality_rtol=reality_rtol),
            source_module=source_module,waves=waves,column_count=len(gas_columns))
    history=[]
    cm=None; ck=None; start_iteration=0
    if checkpoint is not None:
        # Identity, integrity and exact relaxation chain checked before column work.
        cm=checkpoint['module']
        if fixed_source_fourier_J is not None and getattr(cm,'FIXED_SOURCE_SELECTION_IDENTITY',None) is not True:
            raise RuntimeError('CHECKPOINT_MODULE_LACKS_FIXED_SOURCE_SELECTION_IDENTITY; nothing written')
        ck=cm.open_run(checkpoint=checkpoint,solver_file=__file__,fixed=fixed,
            relax=lambda g,u:(1-relaxation)*g+relaxation*u,
            inputs=dict(fixed_positions_m=fixed_positions_m,
                fixed_integrated_columns_J=fixed_integrated_columns_J,
                fixed_source_fourier_J=fixed_source_fourier_J,
                initial_gas_fourier_J=gas,gas_columns=gas_columns,fourier_arguments=args,
                source_module=source_module,fourier_module=fourier_module,
                metric_module=metric_module,hi_module=hi_module,quadrature_module=quadrature_module,
                vertical_fourier_module=vertical_fourier_module,
                controls=dict(c_m_s=c_m_s,max_iterations=max_iterations,relaxation=relaxation,
                    source_atol_J=source_atol_J,source_rtol=source_rtol,
                    reality_atol=reality_atol,reality_rtol=reality_rtol)))
        if ck['resume'] is not None:
            # Stored already-relaxed iterate, never reconstructed by subtraction.
            start_iteration=ck['resume']['iteration']
            gas=ck['resume']['gas']; history=ck['resume']['history']
    def _finish(out,outcome):
        if fixed_source_fourier_J is not None:
            out['fixed_source_selection']={'selection':'SUPPLIED_FIXED_SOURCE_FOURIER_J',
                'fixed_positions_and_integrated_columns':'PROVENANCE_ONLY; accepted unchanged, not used for the fixed term'}
        if ck is not None: out['checkpoint']=cm.finish(ck,outcome=outcome,result=out)
        return out
    for iteration in range(start_iteration,max_iterations):
        current=fixed+gas
        prepared=fourier_module.prepare(**args,source_density_fourier=current)
        restored=[]; resumed=False
        if ck is not None:
            # New iteration: commit START before any column. Resumed iteration:
            # bitwise-identical gas/current/prepared response required instead.
            restored,resumed=cm.begin_iteration(ck,iteration=iteration,gas=gas,
                current=current,fixed=fixed,prepared=prepared,history=history)
        if progress_callback is not None:
            progress_callback(dict(stage='iteration_prepared',iteration=iteration,
                column_count=len(gas_columns),metric_source_fourier_J=current,
                prepared_metric_response=prepared))
            if resumed:
                progress_callback(dict(stage='iteration_resumed',iteration=iteration,
                    column_count=len(gas_columns),restored_column_count=len(restored),
                    next_column_index=len(restored)))
        if pool is not None:
            # PARALLEL: the fresh columns of THIS iteration, against THIS prepared
            # response, are queued in roster order; results are consumed below.
            pool.begin_iteration(iteration=iteration,prepared=prepared,
                columns=[(k,gas_columns[k]) for k in range(len(restored),len(gas_columns))])
        # One line retained at a time; no cross-iteration or stale-source reuse.
        line_key=None; line=None
        def metric_point(R,phi,z):
            nonlocal line_key,line
            pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
            boundary=boundary_jet_at_positions(pos)
            if vertical_fourier_module is None:
                packet=fourier_module.evaluate_prepared(prepared=prepared,
                    physical_positions=pos,**boundary)
            else:
                key=(R,phi)
                if key!=line_key:
                    line=vertical_fourier_module.prepare_line(prepared=prepared,
                        x_m=float(pos[0,0]),y_m=float(pos[0,1]))
                    line_key=key
                packet=vertical_fourier_module.evaluate_line(line=line,z_m=z,**boundary)
            d=packet['fields'][0,:,0]; grad=packet['gradient'][0,:,0,:]
            for a in (d,grad):
                scale=float(np.linalg.norm(a.real)); imag=float(np.linalg.norm(a.imag))
                reality_bound=reality_atol+reality_rtol*scale
                if not all(math.isfinite(v) for v in (imag,scale,reality_bound)) or imag>reality_bound:
                    raise ValueError('NONREAL_PHYSICAL_METRIC; no unconditional real projection')
            return metric_module.evaluate_point(delta_fields=d.real,delta_gradient_physical=grad.real,
                Cbar=args['Cbar'],mubar=args['mubar'],R=R,phi=phi,z=z)
        positions=[]; columns=[]; solutions=[]
        for column_index,col in enumerate(gas_columns):
            R=col['R_m']; phi=col['phi']
            fresh=column_index>=len(restored)
            def at_z(z):
                m=metric_point(R,phi,z)
                return {'N':m['N'],'metric_cyl':m['g_cylindrical'].tolist(),
                        'mode_weights':[[1.0]+[0.0]*9]}
            try:
                # A restored record is this iteration's exact completed solution; it
                # re-enters the SAME accumulation below in original roster order.
                # PARALLEL: pool.take returns THIS column's worker result, or raises
                # its actual HI ValueError (type name and message preserved) here.
                result=(hi_module.solve_hi_column(metric_at_z=at_z,quadrature_module=quadrature_module,
                    radius_m=R,radial_weight_m=col['radial_weight_m'],
                    azimuth_weight_rad=col['azimuth_weight_rad'],surface_ref_kg_m2=col['Sigma_kg_m2'],
                    c_m_s=c_m_s,**col['hi_options']) if fresh and pool is None else
                    pool.take(column_index) if fresh else restored[column_index])
            except ValueError as exc:
                # Preserve the actual failed preparation and its driving field.
                # Only this column call (including its metric callback) is caught;
                # no replacement column, success flag, retry, or clipped boundary.
                return _finish({'converged_finite_fixed_point':False,
                    'failure':{'type':type(exc).__name__,'message':str(exc),
                        'iteration':iteration,'column_index':column_index,
                        'column_inputs':dict(col),'c_m_s':c_m_s,
                        'stage':'actual_hi_column_solve'},
                    'gas_columns':solutions,'history':history,
                    'metric_source_fourier_J':current,
                    'prepared_metric_response':prepared,
                    'scope':'FAILED_SOURCE_PREPARATION; completed columns are partial evidence only; no fixed point or galaxy prediction'},
                    'FAILED_SOURCE_PREPARATION')
            solutions.append(result)
            if ck is not None and fresh:
                cm.write_column(ck,iteration=iteration,column_index=column_index,column=col,result=result)
            if progress_callback is not None and fresh:
                progress_callback(dict(stage='column_completed',iteration=iteration,
                    column_index=column_index,column_count=len(gas_columns),
                    roots_m=result['roots_m'],metric_calls=result['metric_calls']))
            for node,e in zip(result['nodes'],result['source_quadrature']['elements']):
                # Lapse is a scalar: no tensor rotation needed for this adopted
                # rest-energy source. Full C anisotropy still enters volume/f.
                J=-e['rho_kg_m3']*c_m_s*c_m_s*e['proper_volume_m3']
                if not math.isfinite(J): raise ValueError('Nonfinite gas source')
                positions.append([R*math.cos(phi),R*math.sin(phi),node['z_m']])
                columns.append([[J]]+[[0.0] for _ in range(9)])
        # PARALLEL: an admitted row-separable source module is evaluated on
        # chunk-aligned wave-row blocks and stacked in wave order (same rows).
        updated=np.asarray(source_module.physical_source_fourier(physical_positions_m=positions,
            integrated_columns_J=columns,k_physical_inverse_m=waves)
            if pool is None or not pool.source_split else
            pool.source_fourier(iteration=iteration,positions=positions,columns=columns),dtype=complex)
        residual=float(np.linalg.norm(updated-gas)); scale=float(np.linalg.norm(updated))
        if not math.isfinite(residual) or not math.isfinite(scale): raise ValueError('Nonfinite coupling residual')
        bound=source_atol_J+source_rtol*scale
        if not math.isfinite(bound): raise ValueError('Nonfinite source convergence bound')
        history.append({'iteration':iteration,'gas_fourier_residual_J':residual,'bound_J':bound,
                        'roots_m':[r['roots_m'] for r in solutions]})
        if ck is not None:
            cm.complete_iteration(ck,iteration=iteration,updated=updated,residual=residual,
                bound=bound,history_entry=history[-1],converged=residual<=bound)
        if progress_callback is not None:
            progress_callback(dict(stage='iteration_completed',iteration=iteration,
                gas_fourier_residual_J=residual,bound_J=bound,
                reconstructed_gas_fourier_J=updated))
        if residual<=bound:
            return _finish({'converged_finite_fixed_point':True,'metric_source_fourier_J':current,
                'reconstructed_gas_fourier_J':updated,'gas_columns':solutions,'history':history,
                'prepared_metric_response':prepared,
                'scope':'finite source closure only; no metric-error bound near singular response, continuum or full Euler claim'},
                'CONVERGED_FINITE_FIXED_POINT')
        gas=_finite((1-relaxation)*gas+relaxation*updated,'relaxed gas')
    return _finish({'converged_finite_fixed_point':False,'history':history,
            'last_metric_source_fourier_J':current,'last_gas_columns':solutions,
            'scope':'iteration budget exhausted; not a solved galaxy'},'ITERATION_BUDGET_EXHAUSTED')


def cylindrical_metric_covector_to_registered(*, R_m, phi, Cbar,
                                               lapse_J, metric_covector_cyl,
                                               mean_covector_J):
    """Integrated source covector Hc defined by deltaL=Tr(Hc.T delta g_cyl).
    This is NOT a raw stress tensor: proper volume/N/2 must already be included.
    Returns10 registered integrated derivatives. J=(er,R ephi,ez),
    g_cyl=J.T W C W J, so HC=W J Hc J.T W. No extra ellF or volume.
    Mean covector must already use registered mu components.
    """
    R=float(R_m); phi=float(phi)
    if not math.isfinite(R) or R<=0 or not math.isfinite(phi): raise ValueError('Finite R>0,phi required')
    cb=_finite(np.asarray(Cbar,dtype=float),'Cbar'); hc=_finite(np.asarray(metric_covector_cyl,dtype=float),'covector')
    if cb.shape!=(3,3) or hc.shape!=(3,3) or not np.array_equal(cb,cb.T) or not np.array_equal(hc,hc.T):
        raise ValueError('Explicit symmetric3x3 matrices required')
    vals,U=np.linalg.eigh(cb)
    if np.any(vals<=0): raise ValueError('Positive Cbar required')
    W=np.einsum('ia,a,ja->ij',U,1/np.sqrt(vals),U,optimize=False)
    J=np.array([[math.cos(phi),-R*math.sin(phi),0.],
                [math.sin(phi),R*math.cos(phi),0.],[0.,0.,1.]])
    B=np.einsum('ij,jk->ik',W,J,optimize=False)
    H=np.einsum('ia,ab,jb->ij',B,hc,B,optimize=False)
    mean=_finite(np.asarray(mean_covector_J,dtype=float),'mean covector')
    if mean.shape!=(3,): raise ValueError('Three mean components required')
    s=math.sqrt(2)
    return _finite(np.array([lapse_J,H[0,0],H[1,1],H[2,2],s*H[1,2],s*H[0,2],s*H[0,1],*mean],dtype=float),'registered source')


# =============================================================================
# PARALLEL c2v001 machinery. Process-level only: 'spawn' interpreters, one BLAS
# thread each, nothing inherited. Determinism argument: every column (and every
# admitted source wave-row block) is a pure function of shipped inputs evaluated
# by the SAME pinned code; results are consumed in column (wave) order by the
# reviewed statements above. Worker assignment and timing never reach a result.
# =============================================================================
_BLAS_THREAD_VARIABLES=('VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS',
                        'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')
# Source modules whose physical_source_fourier output row q depends only on wave q
# and is computed in fixed wave_chunk blocks (rows of a chunk-aligned sub-call are
# the same floating-point operations as in the full call). Admitted by file sha256.
_ROW_SEPARABLE_SOURCE_SHA256=frozenset({
    '81af8715eab45b8e34ca90b8db5c6c34ba471563fb9a9ecbbb5198a90b9081bc'})  # baryonic_metric_source_columns_v003
_ROW_SEPARABLE_KWDEFAULTS={'wave_chunk':64,'source_chunk':256}
_TASK_DEPTH=2                 # queued tasks per worker
_COLUMN_LOOKAHEAD_PER_WORKER=16  # columns solved ahead of the next column in order
_SOURCE_BLOCKS_PER_WORKER=3
_PERSISTENT_TAG='UNT_PARALLEL_HELPER_C2V001'
_POOL_REPORTS=[]


class ColumnPoolError(RuntimeError):
    """Pool, transport or shipping failure. Deliberately NOT a ValueError: it can
    never be caught as, or recorded as, a physical HI-column failure."""


def last_pool_report():
    """Diagnostics of the most recent pool in this process (no result content)."""
    return dict(_POOL_REPORTS[-1]) if _POOL_REPORTS else None


def _file_bytes_sha256(path):
    with open(path,'rb') as f: data=f.read()
    return data,hashlib.sha256(data).hexdigest()


try:
    _LOADED_SHA256=_file_bytes_sha256(__file__)[1]
except (NameError,OSError):
    _LOADED_SHA256=None


# ----------------------------------------------------------------------------
# Shipping of the column environment. Closures (e.g. reviewed facades built by
# make_modules) are rebuilt in the worker from code objects FOUND in the pinned
# source file (sha256 from bytes); shipped code bytes are only a lookup key.
# File-module plain data globals and function globals are replicated, so runtime
# overrides applied in the parent (stage module patches) hold in the worker.
# ----------------------------------------------------------------------------
class _ModuleRef:
    __slots__=('kind','name','path','sha256','namespace')

    def __init__(self,kind,name,path,sha256,namespace):
        self.kind=kind; self.name=name; self.path=path; self.sha256=sha256; self.namespace=namespace


def _dunder(name):
    return name.startswith('__') and name.endswith('__')


def _plain(v,depth=0):
    if depth>64: return False
    t=type(v)
    if v is None or t in (bool,int,float,complex,str,bytes): return True
    if isinstance(v,pathlib.PurePath): return True
    if t is np.ndarray: return v.dtype.kind in 'biufcSU'
    if isinstance(v,np.generic): return np.asarray(v).dtype.kind in 'biufcSU'
    if t in (tuple,list,set,frozenset): return all(_plain(x,depth+1) for x in v)
    if t is dict: return all(type(k) in (str,int) and _plain(x,depth+1) for k,x in v.items())
    return False


def _attr_chain(obj,qualname):
    for part in qualname.split('.'):
        obj=getattr(obj,part,None)
        if obj is None: return None
    return obj


class _EnvPickler(pickle.Pickler):
    def __init__(self,file):
        super().__init__(file,protocol=5)
        self._refs={}; self._keep=[]

    def persistent_id(self,obj):
        if type(obj) is types.FunctionType:
            name=_HELPER_IDS.get(id(obj))
            if name is not None and _HELPERS[name] is obj: return (_PERSISTENT_TAG,name)
        return None

    def _ref(self,g):
        ref=self._refs.get(id(g))
        if ref is not None: return ref
        name=g.get('__name__')
        mod=sys.modules.get(name) if type(name) is str else None
        if mod is not None and name!='__main__' and vars(mod) is g:
            ref=_ModuleRef('import',name,None,None,g)
        else:
            path=g.get('__file__'); spec=g.get('__spec__')
            if type(path) is not str or not path.endswith('.py') or not os.path.isfile(path):
                raise ColumnPoolError('UNSHIPPABLE_NAMESPACE no .py source for module %r'%(name,))
            if name!='__main__':
                origin=getattr(spec,'origin',None)
                if type(origin) is not str or os.path.realpath(origin)!=os.path.realpath(path):
                    raise ColumnPoolError('UNSHIPPABLE_NAMESPACE module spec/file mismatch %r'%(name,))
            real=os.path.realpath(path)
            # A parent __main__ is re-executed under another name (its main guard stays off).
            ref=_ModuleRef('file','__unt_parent_main__' if name=='__main__' else name,
                           real,_file_bytes_sha256(real)[1],g)
        self._refs[id(g)]=ref; self._keep.append(g)
        return ref

    def reducer_override(self,obj):
        t=type(obj)
        if t is _ModuleRef:
            if obj.kind=='import': return (importlib.import_module,(obj.name,))
            state={k:v for k,v in obj.namespace.items()
                   if not _dunder(k) and (type(v) is types.FunctionType or _plain(v))}
            return (_r_file_module,(obj.name,obj.path,obj.sha256),state,None,None,_r_assign)
        if isinstance(obj,types.ModuleType):
            name=getattr(obj,'__name__',None)
            if type(name) is str and name!='__main__' and sys.modules.get(name) is obj:
                return (importlib.import_module,(name,))
            if getattr(obj,'__spec__',None) is None and name!='__main__':
                # Module-shaped facade built at run time (types.ModuleType): rebuild
                # the namespace; its functions/closures ship like any other.
                state={k:v for k,v in vars(obj).items() if not _dunder(k) or k in ('__file__','__doc__')}
                return (_r_synthetic,(name,),state,None,None,_r_assign)
            return (_r_same,(self._ref(vars(obj)),))
        if t is types.FunctionType:
            mod=sys.modules.get(obj.__module__) if type(obj.__module__) is str else None
            if (mod is not None and obj.__module__!='__main__' and '<locals>' not in obj.__qualname__
                    and _attr_chain(mod,obj.__qualname__) is obj):
                return NotImplemented  # importable by reference
            ref=self._ref(obj.__globals__)
            return (_r_function,(ref,obj.__name__,obj.__qualname__,marshal.dumps(obj.__code__),
                    obj.__closure__,obj.__defaults__,obj.__kwdefaults__),
                    dict(obj.__dict__) or None,None,None,_r_function_dict)
        if t is types.CellType:
            try: state=(True,obj.cell_contents)
            except ValueError: state=(False,None)
            return (_r_cell,(),state,None,None,_r_cell_fill)
        if t is types.CodeType:
            raise ColumnPoolError('UNSHIPPABLE bare code object')
        return NotImplemented


class _EnvUnpickler(pickle.Unpickler):
    def persistent_load(self,pid):
        if type(pid) is tuple and len(pid)==2 and pid[0]==_PERSISTENT_TAG and pid[1] in _HELPERS:
            return _HELPERS[pid[1]]
        raise pickle.UnpicklingError('UNKNOWN_PERSISTENT_ID')


def _dumps(obj):
    buffer=io.BytesIO()
    try:
        _EnvPickler(buffer).dump(obj)
    except ColumnPoolError: raise
    except (pickle.PicklingError,TypeError,AttributeError,ValueError,RecursionError) as exc:
        raise ColumnPoolError('COLUMN_ENVIRONMENT_NOT_SHIPPABLE '+type(exc).__name__+': '+str(exc)) from None
    return buffer.getvalue()


def _loads(data):
    return _EnvUnpickler(io.BytesIO(data)).load()


_CODE_INDEX={}


def _code_tree(code):
    out=[code]
    for c in code.co_consts:
        if type(c) is types.CodeType: out.extend(_code_tree(c))
    return out


def _codes_of(module):
    entry=_CODE_INDEX.get(id(module))
    if entry is not None and entry[0] is module: return entry[1]
    codes=[]
    for v in list(vars(module).values()):
        if type(v) is types.FunctionType and v.__globals__ is vars(module): codes.extend(_code_tree(v.__code__))
    _CODE_INDEX[id(module)]=(module,codes)
    return codes


def _r_same(x):
    return x


def _r_file_module(name,path,sha256):
    data,actual=_file_bytes_sha256(path)
    if actual!=sha256: raise ColumnPoolError('WORKER_MODULE_PIN_MISMATCH '+path)
    code=compile(data,path,'exec',dont_inherit=True)
    module=types.ModuleType(name)
    module.__file__=path
    module.__spec__=importlib.util.spec_from_file_location(name,path)
    module.__loader__=module.__spec__.loader
    _CODE_INDEX[id(module)]=(module,_code_tree(code))
    exec(code,module.__dict__)
    return module


def _r_function(module,name,qualname,code_bytes,closure,defaults,kwdefaults):
    wanted=marshal.loads(code_bytes)
    for code in _codes_of(module):
        if code==wanted: break
    else:
        raise ColumnPoolError('WORKER_CODE_NOT_IN_PINNED_SOURCE %s in %s'%(qualname,getattr(module,'__file__',module.__name__)))
    fn=types.FunctionType(code,vars(module),name,defaults,closure)
    fn.__kwdefaults__=kwdefaults; fn.__qualname__=qualname
    return fn


def _r_function_dict(fn,state):
    fn.__dict__.update(state)


def _r_cell():
    return types.CellType()


def _r_cell_fill(cell,state):
    if state[0]: cell.cell_contents=state[1]


def _r_synthetic(name):
    return types.ModuleType(name)


def _r_assign(obj,state):
    for k,v in state.items(): setattr(obj,k,v)


_HELPERS={f.__name__:f for f in (_r_same,_r_file_module,_r_function,_r_function_dict,
                                 _r_cell,_r_cell_fill,_r_synthetic,_r_assign)}
_HELPER_IDS={id(f):n for n,f in _HELPERS.items()}


# ----------------------------------------------------------------------------
# Worker side.
# ----------------------------------------------------------------------------
_BOOTSTRAP='''
import hashlib,types
with open(_PATH,'rb') as _f: _data=_f.read()
if hashlib.sha256(_data).hexdigest()!=_SHA256: raise SystemExit('UNT_PARALLEL_SOLVER_PIN_MISMATCH '+_PATH)
_module=types.ModuleType('unt_parallel_route_a_column_worker_c2v001')
_module.__file__=_PATH
exec(compile(_data,_PATH,'exec',dont_inherit=True),_module.__dict__)
_module._worker_main(_CONN)
'''


def _rss_bytes():
    try:
        import resource
        peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return int(peak if sys.platform=='darwin' else peak*1024)
    except Exception:
        return None


def _exception_report(exc):
    try:
        pickled=pickle.dumps(exc,protocol=5); pickle.loads(pickled)
    except Exception:
        pickled=None
    return dict(type_name=type(exc).__name__,type_module=type(exc).__module__,message=str(exc),
                is_value_error=isinstance(exc,ValueError),pickled=pickled,
                traceback=traceback.format_exc())


def _run_column(env,prepared,col):
    """Worker copy of ONE iteration of the serial column loop body: the same
    metric_point/at_z statements and the same single try around solve_hi_column.
    A fresh line cache per column (prepare_line is a pure function of prepared
    and (x,y); the serial loop rebuilds it whenever (R,phi) changes)."""
    boundary_jet_at_positions=env['boundary_jet_at_positions']; fourier_module=env['fourier_module']
    metric_module=env['metric_module']; hi_module=env['hi_module']; quadrature_module=env['quadrature_module']
    vertical_fourier_module=env['vertical_fourier_module']; args=env['args']; c_m_s=env['c_m_s']
    reality_atol=env['reality_atol']; reality_rtol=env['reality_rtol']
    # One line retained at a time; no cross-iteration or stale-source reuse.
    line_key=None; line=None
    def metric_point(R,phi,z):
        nonlocal line_key,line
        pos=np.array([[R*math.cos(phi),R*math.sin(phi),z]])
        boundary=boundary_jet_at_positions(pos)
        if vertical_fourier_module is None:
            packet=fourier_module.evaluate_prepared(prepared=prepared,
                physical_positions=pos,**boundary)
        else:
            key=(R,phi)
            if key!=line_key:
                line=vertical_fourier_module.prepare_line(prepared=prepared,
                    x_m=float(pos[0,0]),y_m=float(pos[0,1]))
                line_key=key
            packet=vertical_fourier_module.evaluate_line(line=line,z_m=z,**boundary)
        d=packet['fields'][0,:,0]; grad=packet['gradient'][0,:,0,:]
        for a in (d,grad):
            scale=float(np.linalg.norm(a.real)); imag=float(np.linalg.norm(a.imag))
            reality_bound=reality_atol+reality_rtol*scale
            if not all(math.isfinite(v) for v in (imag,scale,reality_bound)) or imag>reality_bound:
                raise ValueError('NONREAL_PHYSICAL_METRIC; no unconditional real projection')
        return metric_module.evaluate_point(delta_fields=d.real,delta_gradient_physical=grad.real,
            Cbar=args['Cbar'],mubar=args['mubar'],R=R,phi=phi,z=z)
    R=col['R_m']; phi=col['phi']
    def at_z(z):
        m=metric_point(R,phi,z)
        return {'N':m['N'],'metric_cyl':m['g_cylindrical'].tolist(),
                'mode_weights':[[1.0]+[0.0]*9]}
    try:
        result=hi_module.solve_hi_column(metric_at_z=at_z,quadrature_module=quadrature_module,
            radius_m=R,radial_weight_m=col['radial_weight_m'],
            azimuth_weight_rad=col['azimuth_weight_rad'],surface_ref_kg_m2=col['Sigma_kg_m2'],
            c_m_s=c_m_s,**col['hi_options'])
    except ValueError as exc:
        return 'value_error',_exception_report(exc)
    return 'ok',result


def _worker_main(conn):
    import signal
    signal.signal(signal.SIGINT,signal.SIG_IGN)  # the parent owns interruption
    env=None; prepared=None; prepared_iteration=None; prepared_problem=None
    source_inputs=None; source_iteration=None; source_problem=None
    while True:
        try:
            raw=conn.recv_bytes()
        except (EOFError,OSError):
            return  # parent gone: nothing of ours is written anywhere
        try:
            message=_loads(raw)
        except Exception as exc:
            conn.send_bytes(pickle.dumps(('fatal',_exception_report(exc)),protocol=5)); return
        tag=message[0]
        if tag=='stop': return
        if tag=='prepared':
            prepared=None; prepared_iteration=message[1]; prepared_problem=None
            try: prepared=_loads(message[2])
            except Exception as exc: prepared_problem=_exception_report(exc)
            continue
        if tag=='source_inputs':
            source_inputs=None; source_iteration=message[1]; source_problem=None
            try: source_inputs=_loads(message[2])
            except Exception as exc: source_problem=_exception_report(exc)
            continue
        try:
            if tag=='env':
                env=message[1]
                reply=('ready',os.getpid(),_rss_bytes(),{k:os.environ.get(k) for k in _BLAS_THREAD_VARIABLES})
            elif tag=='column':
                _,iteration,index,col=message
                if env is None or iteration!=prepared_iteration:
                    reply=('column',iteration,index,'pool_error','WORKER_STATE_MISMATCH')
                elif prepared_problem is not None:
                    reply=('column',iteration,index,'pool_error','PREPARED_NOT_RECEIVED '+prepared_problem['message'])
                else:
                    try: status,payload=_run_column(env,prepared,col)
                    except Exception as exc: status,payload='exception',_exception_report(exc)
                    reply=('column',iteration,index,status,payload)
            elif tag=='source_block':
                _,iteration,block,a,b=message
                if env is None or iteration!=source_iteration:
                    reply=('source_block',iteration,block,'pool_error','WORKER_STATE_MISMATCH')
                elif source_problem is not None:
                    reply=('source_block',iteration,block,'pool_error','SOURCE_INPUTS_NOT_RECEIVED '+source_problem['message'])
                else:
                    positions,columns=source_inputs
                    try:
                        status,payload='ok',env['source_module'].physical_source_fourier(
                            physical_positions_m=positions,integrated_columns_J=columns,
                            k_physical_inverse_m=env['waves'][a:b])
                    except Exception as exc: status,payload='exception',_exception_report(exc)
                    reply=('source_block',iteration,block,status,payload)
            else:
                reply=('fatal',dict(type_name='ProtocolError',message='UNKNOWN_TAG %r'%(tag,),traceback=''))
        except Exception as exc:
            reply=('fatal',_exception_report(exc))
        try:
            data=pickle.dumps(reply+(_rss_bytes(),),protocol=5)
        except Exception as exc:
            data=pickle.dumps(reply[:3]+('pool_error','RESULT_NOT_TRANSFERABLE '+type(exc).__name__+': '+str(exc),_rss_bytes()),protocol=5)
        try:
            conn.send_bytes(data)
        except (EOFError,OSError):
            return


# ----------------------------------------------------------------------------
# Parent side.
# ----------------------------------------------------------------------------
def _raise_remote(report,*,value_error_scope):
    """Re-raise a worker exception in the parent. In the column ValueError scope
    the type NAME and str(message) are exactly the worker's, as the reviewed
    failure record uses only those. Elsewhere the original type is restored when
    it is transferable; otherwise ColumnPoolError."""
    exc=None
    if report.get('pickled') is not None:
        try: exc=pickle.loads(report['pickled'])
        except Exception: exc=None
    if (not isinstance(exc,BaseException) or type(exc).__name__!=report['type_name']
            or str(exc)!=report['message'] or isinstance(exc,ValueError)!=report['is_value_error']):
        exc=None
    if value_error_scope:
        if not report['is_value_error']: raise ColumnPoolError('PROTOCOL value-error scope without ValueError')
        if exc is None:
            cls=ValueError if report['type_name']=='ValueError' else type(report['type_name'],(ValueError,),
                {'__module__':'unt_parallel_remote','__doc__':'Worker ValueError of a non-transferable type (name kept).'})
            exc=cls(report['message'])
    else:
        if exc is None or isinstance(exc,ValueError) and report.get('column_scope'):
            raise ColumnPoolError('REMOTE_EXCEPTION %s: %s\n%s'%(report['type_name'],report['message'],report.get('traceback','')))
    try: exc.add_note('[parallel worker traceback]\n'+report.get('traceback',''))
    except Exception: pass
    raise exc


class _Worker:
    __slots__=('proc','conn','inflight','alive','pid','peak_rss','tasks','blas')

    def __init__(self,proc,conn):
        self.proc=proc; self.conn=conn; self.inflight=collections.deque(); self.alive=True
        self.pid=None; self.peak_rss=None; self.tasks=0; self.blas=None


class _ColumnPool:
    def __init__(self,workers):
        self.requested=workers; self.workers=[]; self.closed=False; self.started=False
        self.source_split=False; self.source_rule=None; self.blocks=[]
        self.iteration=None; self.queue=collections.deque(); self.results={}; self.next_take=None
        self.block_results={}; self.broken=None
        self.report=dict(requested_workers=workers,start_method='spawn')
        _POOL_REPORTS.append(self.report)

    # ---- lifecycle ----
    def start(self,*,column_environment,source_module,waves,column_count):
        if self.started: raise ColumnPoolError('POOL_ALREADY_STARTED')
        self.started=True
        n=max(1,min(self.requested,column_count))
        data,sha=_file_bytes_sha256(__file__)
        if _LOADED_SHA256 is None or sha!=_LOADED_SHA256:
            raise ColumnPoolError('SOLVER_FILE_CHANGED_SINCE_IMPORT '+__file__)
        chunk,rule=_source_split_rule(source_module)
        self.source_rule=rule
        environment=dict(column_environment)
        if chunk is not None:
            environment.update(source_module=source_module,waves=waves)
            nk=len(waves); chunks=-(-nk//chunk); count=max(1,min(chunks,n*_SOURCE_BLOCKS_PER_WORKER))
            edges=[i*chunks//count for i in range(count+1)]
            self.blocks=[(edges[i]*chunk,min(edges[i+1]*chunk,nk)) for i in range(count)]
            self.source_split=True
        message=_dumps(('env',environment))  # proven shippable before any process exists
        ctx=multiprocessing.get_context('spawn')
        saved={k:os.environ.get(k) for k in _BLAS_THREAD_VARIABLES}
        try:
            for k in _BLAS_THREAD_VARIABLES: os.environ[k]='1'
            for i in range(n):
                parent_end,child_end=ctx.Pipe(duplex=True)
                proc=ctx.Process(target=exec,args=(_BOOTSTRAP,{'__name__':'__unt_parallel_bootstrap__',
                    '_PATH':os.path.realpath(__file__),'_SHA256':sha,'_CONN':child_end}),
                    name='unt-route-a-column-worker-%02d'%i,daemon=True)
                proc.start(); child_end.close()
                self.workers.append(_Worker(proc,parent_end))
        finally:
            for k,v in saved.items():
                if v is None: os.environ.pop(k,None)
                else: os.environ[k]=v
        for w in self.workers:
            self._send(w,message); w.inflight.append(('env',None))
        while any(w.inflight for w in self.workers if w.alive) and self.broken is None:
            self._pump()
        if self.broken is not None: raise ColumnPoolError('POOL_START_FAILED '+self.broken)
        self.report.update(workers=n,pids=[w.pid for w in self.workers],
            source_split=self.source_split,source_rule=rule,source_blocks=len(self.blocks),
            env_message_bytes=len(message),worker_blas_env=[w.blas for w in self.workers])

    def close(self):
        if self.closed: return
        self.closed=True
        stop=_dumps(('stop',))
        for w in self.workers:
            if w.alive:
                try: w.conn.send_bytes(stop)
                except (OSError,ValueError): pass
        for w in self.workers:
            w.proc.join(timeout=2.0)
            if w.proc.is_alive(): w.proc.terminate(); w.proc.join(timeout=5.0)
            if w.proc.is_alive(): w.proc.kill(); w.proc.join(timeout=5.0)
            try: w.conn.close()
            except OSError: pass
        self.report.update(peak_rss_bytes=[w.peak_rss for w in self.workers],
            tasks=[w.tasks for w in self.workers],broken=self.broken,
            exitcodes=[w.proc.exitcode for w in self.workers])

    # ---- transport ----
    def _send(self,w,data):
        try:
            w.conn.send_bytes(data)
        except (OSError,ValueError) as exc:
            self._lost(w,'SEND_FAILED '+type(exc).__name__)

    def _lost(self,w,why):
        if not w.alive: return
        w.alive=False
        text='COLUMN_WORKER_LOST pid=%s exitcode=%s %s'%(w.pid,w.proc.exitcode,why)
        if self.broken is None: self.broken=text
        for kind,key in w.inflight:
            if kind=='column': self.results[key]=('pool_error',text)
            elif kind=='source_block': self.block_results[key]=('pool_error',text)
        w.inflight.clear()

    def _accept(self,w,message):
        tag=message[0]
        if tag=='fatal':
            self._lost(w,'FATAL %s: %s\n%s'%(message[1].get('type_name'),message[1].get('message'),message[1].get('traceback','')))
            return
        if not w.inflight:
            raise ColumnPoolError('PROTOCOL unexpected reply %r'%(tag,))
        kind,key=w.inflight.popleft()
        rss=message[-1]
        if rss is not None: w.peak_rss=max(w.peak_rss or 0,rss)
        if tag=='ready' and kind=='env':
            w.pid=message[1]; w.blas=message[3]; return
        if tag=='column' and kind=='column' and message[1]==self.iteration and message[2]==key:
            w.tasks+=1; self.results[key]=(message[3],message[4]); return
        if tag=='source_block' and kind=='source_block' and message[1]==self.iteration and message[2]==key:
            w.tasks+=1; self.block_results[key]=(message[3],message[4]); return
        raise ColumnPoolError('PROTOCOL reply %r does not match oldest task %r'%(message[:3],(kind,key)))

    def _pump(self):
        alive=[w for w in self.workers if w.alive]
        if not alive:
            if self.broken is None: self.broken='NO_LIVE_COLUMN_WORKERS'
            return
        ready=set(multiprocessing.connection.wait([w.conn for w in alive]+[w.proc.sentinel for w in alive]))
        for w in alive:
            if w.conn in ready or w.proc.sentinel in ready:
                # Drain every complete reply before treating an exit as a loss.
                while w.alive:
                    try:
                        if not w.conn.poll(): break
                        raw=w.conn.recv_bytes()
                    except (EOFError,OSError):
                        self._lost(w,'EOF'); break
                    self._accept(w,pickle.loads(raw))
                if w.alive and w.proc.sentinel in ready and not w.proc.is_alive():
                    self._lost(w,'EXITED')

    # ---- columns ----
    def begin_iteration(self,*,iteration,prepared,columns):
        if self.broken is not None: raise ColumnPoolError(self.broken)
        if self.queue or self.results or any(w.inflight for w in self.workers):
            raise ColumnPoolError('PROTOCOL previous iteration not drained')
        self.iteration=iteration; self.results={}; self.block_results={}
        self.queue=collections.deque(columns)
        self.next_take=columns[0][0] if columns else None
        if not columns: return
        message=_dumps(('prepared',iteration,_dumps(prepared)))
        for w in self.workers:
            if w.alive: self._send(w,message)
        self._dispatch_columns()

    def _dispatch_columns(self):
        if self.next_take is None: return
        limit=self.next_take+_COLUMN_LOOKAHEAD_PER_WORKER*len(self.workers)
        sent=True
        while sent and self.queue and self.broken is None:
            sent=False
            for w in self.workers:
                if not self.queue or self.queue[0][0]>=limit: return
                if w.alive and len(w.inflight)<_TASK_DEPTH:
                    index,col=self.queue.popleft()
                    w.inflight.append(('column',index))
                    self._send(w,_dumps(('column',self.iteration,index,col)))
                    sent=True

    def _in_flight(self,kind,key):
        return any((kind,key) in w.inflight for w in self.workers if w.alive)

    def take(self,column_index):
        """Result of column_index, strictly in column order. Raises that column's
        HI ValueError (scope of the reviewed try), its other exception, or
        ColumnPoolError if the pool can no longer deliver it."""
        if column_index!=self.next_take: raise ColumnPoolError('PROTOCOL column order %r!=%r'%(column_index,self.next_take))
        while column_index not in self.results:
            if self.broken is not None and not self._in_flight('column',column_index):
                self.results[column_index]=('pool_error',self.broken); break
            self._pump()
            self._dispatch_columns()  # keep idle workers busy inside the lookahead window
        status,payload=self.results.pop(column_index)
        self.next_take=column_index+1
        if not self.queue and not self.results and not any(w.inflight for w in self.workers): self.next_take=None
        self._dispatch_columns()
        if status=='ok': return payload
        if status=='value_error': _raise_remote(payload,value_error_scope=True)
        if status=='exception': _raise_remote(dict(payload,column_scope=True),value_error_scope=False)
        raise ColumnPoolError('COLUMN %d NOT DELIVERED: %s'%(column_index,payload))

    # ---- source transform ----
    def source_fourier(self,*,iteration,positions,columns):
        if self.broken is not None: raise ColumnPoolError(self.broken)
        if self.queue or self.results or any(w.inflight for w in self.workers):
            raise ColumnPoolError('PROTOCOL columns not drained before source transform')
        self.iteration=iteration; self.block_results={}
        message=_dumps(('source_inputs',iteration,_dumps((positions,columns))))
        for w in self.workers:
            if w.alive: self._send(w,message)
        pending=collections.deque(range(len(self.blocks)))
        while len(self.block_results)<len(self.blocks):
            for w in self.workers:
                while pending and w.alive and len(w.inflight)<_TASK_DEPTH and self.broken is None:
                    block=pending.popleft(); a,b=self.blocks[block]
                    w.inflight.append(('source_block',block))
                    self._send(w,_dumps(('source_block',iteration,block,a,b)))
            if self.broken is not None:
                for block in range(len(self.blocks)):
                    if block not in self.block_results and not self._in_flight('source_block',block):
                        self.block_results[block]=('pool_error',self.broken)
                pending.clear()
                if len(self.block_results)>=len(self.blocks): break
            self._pump()
        parts=[]
        for block in range(len(self.blocks)):  # first failing block in wave order
            status,payload=self.block_results[block]
            if status=='ok': parts.append(payload); continue
            if status=='exception': _raise_remote(payload,value_error_scope=False)
            raise ColumnPoolError('SOURCE BLOCK %d NOT DELIVERED: %s'%(block,payload))
        self.block_results={}
        return np.concatenate(parts,axis=0)


def _source_split_rule(source_module):
    """(wave_chunk, rule) when the source transform may be split by wave rows."""
    fn=getattr(source_module,'physical_source_fourier',None)
    path=getattr(source_module,'__file__',None)
    if type(fn) is not types.FunctionType or type(path) is not str or not os.path.isfile(path):
        return None,'NOT_SPLIT: source module without file-backed physical_source_fourier'
    data,sha=_file_bytes_sha256(path)
    if sha not in _ROW_SEPARABLE_SOURCE_SHA256:
        return None,'NOT_SPLIT: source module sha256 %s not admitted as row-separable'%sha
    code=compile(data,path,'exec',dont_inherit=True)
    top=[c for c in code.co_consts if type(c) is types.CodeType and c.co_name=='physical_source_fourier']
    if (len(top)!=1 or fn.__code__!=top[0] or fn.__kwdefaults__!=_ROW_SEPARABLE_KWDEFAULTS
            or not isinstance(source_module,types.ModuleType) or fn.__globals__ is not vars(source_module)):
        return None,'NOT_SPLIT: physical_source_fourier is not the admitted file function with default chunks'
    return _ROW_SEPARABLE_KWDEFAULTS['wave_chunk'],'SPLIT: admitted %s sha256 %s, wave_chunk %d'%(
        os.path.basename(path),sha,_ROW_SEPARABLE_KWDEFAULTS['wave_chunk'])
