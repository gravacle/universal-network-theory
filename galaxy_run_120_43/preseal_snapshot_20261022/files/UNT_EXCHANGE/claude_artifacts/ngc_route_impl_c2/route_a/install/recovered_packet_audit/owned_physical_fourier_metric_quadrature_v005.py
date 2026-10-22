"""INERT deterministic anisotropic inverse Fourier quadrature; no data or sampling.

Uniform physical orthonormal background x=ell_F Cbar^(1/2) xi, xi=A m,
so k_registered=ell_F Cbar^(1/2) k_physical and k_primitive=A.T k_registered.
A is exactly the adopted diamond registration with columns (0,.5,.5),
(.5,0,.5),(.5,.5,0), determinant1/4, matching the fixed EH cell measure.
Other Bravais charts are unsupported by this version.
For each supplied k!=0, cardinal SOURCE F(k) -> complete complex metric K ->
x_tilde(k)=-K_density(k)^-1 f_tilde_density(k). Inject accepted complex V002.
Then x(x)=sum_q dk_weight_q exp(+i k_q.x) x_tilde_q/(2pi)^3;
first/second derivatives multiply by i k_i and -k_i k_j respectively.
All ten fields (n,C_Mandel6,mu3) and all source columns survive. Derivatives
are physical Cartesian derivatives of these chart field components.

Input dk_weights have units physical inverse-volume and already include the
actual quadrature Jacobian, NOT a cell factor or (2pi)^-3. Source columns are
Fourier transforms integral dV exp(-ik.x) of physical action-per-time density
sources (units energy); NOT per-cell sources. Output fields are dimensionless,
derivatives inverse length and inverse length squared. No additional quadrature,
cell population, inclination, circular-motion or axisymmetric factor is applied.

node_convention='full_signed': every supplied node is integrated exactly once,
including both signs when present; NEVER multiply by2. 'paired_half': each
nonzero representative has a distinct omitted -k with equal weight and exactly
conjugate source; caller explicitly declares real-source pairing. BOTH signs
are actually bound and solved, not inferred by discarding imaginary output.
No physical nonzero Nyquist vector is selfconjugate for this continuous integral;
lattice aliasing does not identify exp(ik.x) with exp(-ik.x) at arbitrary x.

Finite domain, source exterior and zero/background/boundary contribution are
explicit caller inputs. This engine supplies NO tail/truncation error bound.
Use the identical quadrature and full nonlinear solve on joint statistical
replicates; central-result linear covariance propagation is not automatic.
"""
import numpy as np


def _finite(a,name):
    if not np.all(np.isfinite(a)): raise ValueError(name+': nonfinite')
    return a


def _real(a,name):
    if np.iscomplexobj(a): raise ValueError(name+': real required')
    return _finite(np.asarray(a,dtype=float),name)


def prepare(*,source_hessian_grid,k_physical,dk_weights,source_density_fourier,
             registered_bravais,jbar,mubar,Cbar,Eref,ell_F,gamma,
             cardinal_module,complex_binding_module,static_binding_module,
             relative_singular_floor,hermitian_tolerance,
             full_residual_relative_tolerance,full_residual_absolute_tolerance,
             node_convention,real_source_pairing_declared,finite_domain_description,
             boundary_description, node_diagnostic_callback=None, retain_node_diagnostics=True):
    """Prepare all signed full-complex response waves once for this operator/source.
    All source-before-inverse operations and residual checks retained.
    """
    if not isinstance(finite_domain_description,str) or not finite_domain_description.strip():
        raise ValueError('Declared finite integration domain/tail scope required')
    if not isinstance(boundary_description,str) or not boundary_description.strip():
        raise ValueError('Explicit zero-mode/background/boundary treatment required')
    if type(retain_node_diagnostics) is not bool:
        raise ValueError('Explicit boolean diagnostic retention required')
    if node_diagnostic_callback is not None and not callable(node_diagnostic_callback):
        raise ValueError('Diagnostic callback must be callable')
    if not retain_node_diagnostics and node_diagnostic_callback is None:
        raise ValueError('Nonretained diagnostics require an actual stream callback')
    k=_real(k_physical,'physical nodes'); weights=_real(dk_weights,'dk weights')
    A=_real(registered_bravais,'Bravais')
    cb=_real(Cbar,'Cbar')
    if k.ndim!=2 or k.shape[1]!=3 or len(k)==0 or weights.shape!=(len(k),): raise ValueError('Node/weight shapes')
    if A.shape!=(3,3) or cb.shape!=(3,3): raise ValueError('Chart shapes')
    if not np.array_equal(cb,cb.T): raise ValueError('Cbar explicitly symmetric required; no repair')
    if not np.isfinite(ell_F) or ell_F<=0: raise ValueError('Positive physical ell_F required')
    adopted_A=np.array([[0.,.5,.5],[.5,0.,.5],[.5,.5,0.]])
    if not np.array_equal(A,adopted_A):
        raise ValueError('Only the exact adopted diamond Bravais matrix is supported; cell measure must remain 1/4')
    eig,vec=np.linalg.eigh(cb)
    if np.any(eig<=0): raise ValueError('SPD Cbar required')
    root=np.einsum('ia,a,ja->ij',vec,np.sqrt(eig),vec,optimize=False)
    if np.any(weights<=0): raise ValueError('Supply positive actual dk quadrature weights')
    keys=[tuple(row) for row in k]
    if len(set(keys))!=len(keys): raise ValueError('Duplicate physical node; combine weights explicitly upstream')
    if np.any(np.all(k==0,axis=1)): raise ValueError('k=0 handled by explicit boundary/normal solution, not this inverse')
    if node_convention not in ('full_signed','paired_half'): raise ValueError('Explicit signed-node convention required')
    if node_convention=='paired_half':
        if real_source_pairing_declared is not True: raise ValueError('Half-grid requires explicit real source pairing')
        keyset=set(keys)
        if any(tuple(-row) in keyset for row in k): raise ValueError('Half-grid already contains a conjugate partner; double count')
    f=_finite(np.asarray(source_density_fourier,dtype=complex),'source Fourier columns')
    if f.ndim!=3 or f.shape[:2]!=(len(k),10) or f.shape[2]<1: raise ValueError('Full source columns shape')
    wavevectors=[]; weighted_responses=[]
    grid_diag=cardinal_module.grid_diagnostics(source_hessian_grid=source_hessian_grid)
    grid=np.asarray(source_hessian_grid,dtype=complex); L=grid.shape[0]
    diagnostics=[]
    for iq in range(len(k)):
        signs=(1,-1) if node_convention=='paired_half' else (1,)
        pair=[]; node_records=[]
        for sign in signs:
            kv=sign*k[iq]; fv=f[iq] if sign==1 else f[iq].conj()
            kr=ell_F*np.einsum('ij,j->i',root,kv,optimize=False)
            kp=np.einsum('ji,j->i',A,kr,optimize=False)
            wp=cardinal_module.cardinal_weights(L=L,k_primitive=kp)
            F=np.einsum('abc,abcij->ij',wp['weights'],grid,optimize=False)
            bound=complex_binding_module.bind_symbol(F_source_symbol=F,jbar=jbar,mubar=mubar,
                Cbar=cb,k_registered=kr,Eref=Eref,ell_F=ell_F,gamma=gamma,
                static_binding_module=static_binding_module,relative_singular_floor=relative_singular_floor,
                hermitian_tolerance=hermitian_tolerance)
            solved=complex_binding_module.solve_symbol(bound=bound,source_density_columns=fv,
                relative_singular_floor=relative_singular_floor,
                full_residual_relative_tolerance=full_residual_relative_tolerance,
                full_residual_absolute_tolerance=full_residual_absolute_tolerance)
            xt=solved['fields']; pair.append(xt)
            wavevectors.append(kv.copy())
            weighted_responses.append(_finite(weights[iq]/(2*np.pi)**3*xt,'weighted Fourier response').copy())
            node_records.append({'node_index':iq,'sign':sign,'k_registered':kr,'k_primitive':kp,
                'weight_partition_residual':wp['partition_residual'],
                'binding':bound['diagnostics'],'full_residual_norms':solved['full_residual_norms'],
                'full_residual_bounds':solved['full_residual_bounds'],'singular_values':solved['singular_values']})
        if len(pair)==2:
            node_records[-1]['solution_conjugate_residual']=float(np.linalg.norm(pair[1]-pair[0].conj()))
        for record in node_records:
            if node_diagnostic_callback is not None:
                node_diagnostic_callback(record)
            if retain_node_diagnostics:
                diagnostics.append(record)
    return {'wavevectors':np.asarray(wavevectors),
        'weighted_responses':np.asarray(weighted_responses),
        'grid_diagnostics':grid_diag,'node_diagnostics':diagnostics,
        'node_diagnostics_retained':retain_node_diagnostics,
        'node_diagnostics_streamed':node_diagnostic_callback is not None,
        'finite_domain_description':finite_domain_description,
        'boundary_description':boundary_description,'node_convention':node_convention,
        'scope':'prepared fixed current operator AND current source; rebuild when either changes'}


def evaluate_prepared(*,prepared,physical_positions,boundary_fields,
                      boundary_gradient,boundary_hessian,position_batch_size=32,
                      wave_batch_size=256,max_workspace_bytes=8388608):
    """Batched phases/jets; no cardinal, Legendre or linear solves.
    Defaults bound explicit temporary arrays; tune batches within caller memory.
    Output storage itself is 16*positions*10*columns*13 bytes (complex128),
    in addition to supplied boundary/input arrays. No conjugate/field reduction.
    Summation grouping changes roundoff only; all signed waves remain included.
    Boundary arrays are PERTURBATIONS; N=1,Cbar are restored by metric evaluator.
    Caller must retain preparation diagnostics and rebuild for a changed source,
    state, calibration, background, grid or registered kernel. No global cache.
    """
    pos=_real(physical_positions,'physical positions')
    if pos.ndim!=2 or pos.shape[1]!=3 or len(pos)==0: raise ValueError('Position triples required')
    k=_real(prepared['wavevectors'],'prepared wavevectors')
    amplitudes=_finite(np.asarray(prepared['weighted_responses'],dtype=complex),'prepared responses')
    if k.ndim!=2 or k.shape[1]!=3 or amplitudes.ndim!=3 or amplitudes.shape[:2]!=(len(k),10) or amplitudes.shape[2]<1:
        raise ValueError('Prepared wave shapes invalid')
    shape=(len(pos),10,amplitudes.shape[2]); arrays=[]
    for val,sh,name in ((boundary_fields,shape,'boundary fields'),
        (boundary_gradient,shape+(3,),'boundary gradient'),
        (boundary_hessian,shape+(3,3),'boundary Hessian')):
        arr=_finite(np.asarray(val,dtype=complex),name)
        if arr.shape!=sh: raise ValueError(name+': wrong shape')
        arrays.append(arr.copy())
    fields,gradient,hessian=arrays
    for value,name in ((position_batch_size,'position batch'),(wave_batch_size,'wave batch'),
                       (max_workspace_bytes,'workspace cap')):
        if type(value) is not int or value<1: raise ValueError(name+': positive integer required')
    pb=min(position_batch_size,len(pos)); qb=min(wave_batch_size,len(k))
    ns=amplitudes.shape[2]
    # Conservative explicit array-workspace allowance, excluding caller inputs,
    # required output arrays, and opaque NumPy allocator/interpreter overhead.
    # No (positions,waves,10,columns,3,3) tensor is materialized.
    workspace_bound=128*pb*qb+64*qb*10*ns+64*pb*10*ns+64*qb
    if workspace_bound>max_workspace_bytes:
        raise ValueError('Requested batches exceed explicit workspace allowance; reduce batch sizes')
    for x0 in range(0,len(pos),pb):
        x1=min(x0+pb,len(pos)); positions=pos[x0:x1]
        for q0 in range(0,len(k),qb):
            q1=min(q0+qb,len(k)); waves=k[q0:q1]; amps=amplitudes[q0:q1]
            angles=_finite(np.einsum('xi,qi->xq',positions,waves,optimize=False),'phase angles')
            phase=_finite(np.exp(1j*angles),'phases')
            increment=_finite(np.einsum('xq,qas->xas',phase,amps,optimize=False),'field increment')
            fields[x0:x1]+=increment
            for i in range(3):
                multiplier=1j*waves[:,i]
                inc=_finite(np.einsum('xq,qas,q->xas',phase,amps,multiplier,optimize=False),'gradient increment')
                gradient[x0:x1,:,:,i]+=inc
                for j in range(i,3):
                    multiplier=_finite(-waves[:,i]*waves[:,j],'Hessian multiplier')
                    inc=_finite(np.einsum('xq,qas,q->xas',phase,amps,multiplier,optimize=False),'Hessian increment')
                    hessian[x0:x1,:,:,i,j]+=inc
                    if i!=j: hessian[x0:x1,:,:,j,i]+=inc
            for val,name in ((fields[x0:x1],'fields'),(gradient[x0:x1],'gradient'),(hessian[x0:x1],'Hessian')):
                _finite(val,name)
    norms={name:float(np.linalg.norm(val.imag)) for name,val in
           (('fields',fields),('gradient',gradient),('hessian',hessian))}
    if not all(np.isfinite(v) for v in norms.values()): raise ValueError('Nonfinite output norm')
    return {'fields':fields,'gradient':gradient,'hessian':hessian,
        'imaginary_output_norms':norms,
        'batching':{'position_batch_size':pb,'wave_batch_size':qb,
                    'explicit_workspace_bound_bytes':workspace_bound,'workspace_cap_bytes':max_workspace_bytes,
                    'excludes':'caller inputs and required outputs; not a process RSS bound'},'grid_diagnostics':prepared['grid_diagnostics'],
        'node_diagnostics':prepared['node_diagnostics'],
        'finite_domain_description':prepared['finite_domain_description'],
        'boundary_description':prepared['boundary_description'],
        'node_convention':prepared['node_convention'],
        'scope':'same fixed-source finite Fourier sum; no tail or statistical acceptance'}


def evaluate(*,physical_positions,boundary_fields,boundary_gradient,boundary_hessian,
             position_batch_size=32,wave_batch_size=256,max_workspace_bytes=8388608,**arguments):
    """Compatible one-call API; repeated positions should use prepare once."""
    return evaluate_prepared(prepared=prepare(**arguments),physical_positions=physical_positions,
        boundary_fields=boundary_fields,boundary_gradient=boundary_gradient,boundary_hessian=boundary_hessian,
        position_batch_size=position_batch_size,wave_batch_size=wave_batch_size,max_workspace_bytes=max_workspace_bytes)
