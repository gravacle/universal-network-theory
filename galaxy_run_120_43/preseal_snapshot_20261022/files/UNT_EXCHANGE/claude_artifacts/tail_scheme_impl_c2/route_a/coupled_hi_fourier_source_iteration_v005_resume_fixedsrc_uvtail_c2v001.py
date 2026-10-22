"""Inert finite Fourier/HI source fixed-point iteration, no coefficient fallback.
One actual combined source family per call. Rest-energy source approximation.
Uniform physical Cartesian background chart; full metric anisotropy retained.
RESUME c2v001 (Claude2 0422): optional exact restart at a completed HI-column
boundary via an injected checkpoint module. checkpoint=None executes v005.
FIXEDSRC c2v001 (Claude2 0424): optional fixed_source_fourier_J. Omitted (None),
the fixed term is evaluated exactly as before. Supplied, that validated array is
the fixed term; fixed positions/columns are kept only as provenance.
UVTAIL c2v001 (Claude2 tail_scheme_impl_c2/route_a; successor of 44d9c23c; TAIL_SCHEME_DESIGN_V002 sec 3.5):
optional uv_tail (a route_a_uv_tail_controller_c2v001.RouteATailController). uv_tail=None (default) executes the
reviewed statements unchanged. Supplied: boundary_jet_at_positions must BE uv_tail.boundary (the TailBoundary);
the tail state of each iteration is set before prepare (L111/112), the updated roster, M_T/M_K monitor and sidecar
are committed after the residual (L196-199, before the checkpoint COMPLETED record), and every returned outcome
carries result['uv_tail']. Stopping rule, tolerances, guards and the column try are unchanged. bind_uv_tail(c)
returns a module-shaped view (__file__ = this file) whose solve fixes uv_tail=c, for the reviewed composite adapter.
"""
import functools
import math
import types
import numpy as np


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


def solve(*, fixed_positions_m, fixed_integrated_columns_J, initial_gas_fourier_J,
          gas_columns, fourier_arguments, boundary_jet_at_positions,
          source_module, fourier_module, metric_module, hi_module, quadrature_module,
          c_m_s, max_iterations, relaxation, source_atol_J, source_rtol,
          reality_atol, reality_rtol, vertical_fourier_module=None, progress_callback=None,
          checkpoint=None, fixed_source_fourier_J=None, uv_tail=None):
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
    if uv_tail is not None:
        # UVTAIL: the bound TailBoundary is the boundary slot; checked before any checkpoint record.
        uv_tail.bind_check(boundary_jet_at_positions,checkpoint)
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
    if uv_tail is not None:
        # UVTAIL: sidecar opened (new) or verified and its rosters reloaded (resume) against this checkpoint.
        uv_tail.open(relaxation=relaxation,start_iteration=start_iteration,
            checkpoint_mode=None if ck is None else checkpoint['mode'],
            checkpoint_identity_sha256=None if ck is None else ck['identity_sha256'])
    def _finish(out,outcome):
        if fixed_source_fourier_J is not None:
            out['fixed_source_selection']={'selection':'SUPPLIED_FIXED_SOURCE_FOURIER_J',
                'fixed_positions_and_integrated_columns':'PROVENANCE_ONLY; accepted unchanged, not used for the fixed term'}
        if uv_tail is not None: out['uv_tail']=uv_tail.result_record(outcome=outcome)
        if ck is not None: out['checkpoint']=cm.finish(ck,outcome=outcome,result=out)
        return out
    for iteration in range(start_iteration,max_iterations):
        current=fixed+gas
        if uv_tail is not None:
            # UVTAIL: tail state of THIS iteration's gas (I1-T against gas), before prepare and any column.
            uv_tail.begin_iteration(iteration=iteration,gas=gas)
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
                result=(hi_module.solve_hi_column(metric_at_z=at_z,quadrature_module=quadrature_module,
                    radius_m=R,radial_weight_m=col['radial_weight_m'],
                    azimuth_weight_rad=col['azimuth_weight_rad'],surface_ref_kg_m2=col['Sigma_kg_m2'],
                    c_m_s=c_m_s,**col['hi_options']) if fresh else restored[column_index])
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
        updated=np.asarray(source_module.physical_source_fourier(physical_positions_m=positions,
            integrated_columns_J=columns,k_physical_inverse_m=waves),dtype=complex)
        residual=float(np.linalg.norm(updated-gas)); scale=float(np.linalg.norm(updated))
        if not math.isfinite(residual) or not math.isfinite(scale): raise ValueError('Nonfinite coupling residual')
        bound=source_atol_J+source_rtol*scale
        if not math.isfinite(bound): raise ValueError('Nonfinite source convergence bound')
        if uv_tail is not None:
            # UVTAIL: updated roster, next (relaxation-mirrored) state, M_T/M_K, sidecar -- before COMPLETED.
            uv_tail.complete_iteration(iteration=iteration,positions=positions,columns=columns,gas=gas,
                updated=updated,current=current,prepared=prepared,converged=residual<=bound)
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


def bind_uv_tail(uv_tail):
    """Module-shaped view of THIS file whose solve fixes uv_tail (for callers such as the reviewed composite adapter
    that call solver_module.solve with a fixed keyword set). __file__ is this file, so caller pins are unchanged."""
    if uv_tail is None: raise ValueError('bind_uv_tail requires a controller; tail OFF uses this module directly')
    view=types.ModuleType(__name__+'_uv_tail')
    view.__file__=__file__
    view.__doc__='solve() of %s with uv_tail bound'%__file__
    view.solve=functools.partial(solve,uv_tail=uv_tail)
    view.uv_tail=uv_tail
    view.cylindrical_metric_covector_to_registered=cylindrical_metric_covector_to_registered
    return view


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
