"""Codex2 P63 collective-history METHOD source V002; supersedes0124 for future method runs. No execution by author.
Full-parent inputs and observable/Gamma qualifications are external root obligations.
Never evolves by a fitted Markov kernel or silently projects/renormalizes rho.
"""
import itertools
import math
import numpy as np

MAX_DIM = 32
MAX_HISTORIES = 16
MAX_STEPS = 8


def _square(x, n=None):
    x = np.asarray(x,dtype=complex)
    if x.ndim != 2 or x.shape[0] != x.shape[1] or not 1 <= len(x) <= MAX_DIM:
        raise ValueError("Complete dense method parent must have dimension1..32")
    if n is not None and len(x) != n or not np.isfinite(x).all():
        raise ValueError("Dimension mismatch or nonfinite matrix")
    return x


def _hermitian(x, n=None):
    x = _square(x,n)
    if not np.array_equal(x,x.conj().T):
        raise ValueError("Exactly stored Hermitian input required")
    return x


def _state(rho,tol):
    if not math.isfinite(tol) or tol <= 0:
        raise ValueError("Positive finite method tolerance required")
    rho = _hermitian(rho)
    ev = np.linalg.eigvalsh(rho)
    if abs(np.trace(rho)-1) > tol or ev[0] < -tol:
        raise ValueError("Trace-one positive state required within method tolerance")
    return rho, {'trace':float(np.trace(rho).real),'minimum_eigenvalue':float(ev[0]),
                 'state_error_status':'FLOAT_DIAGNOSTICS_NOT_CERTIFIED_NO_RENORMALIZATION'}


def collective_snapshot(H,rho,observables,tol=1e-11):
    """Native moments/currents on a supplied full state, including complex correlations.
    observables maps explicit unique names to root-authenticated Hermitian matrices.
    Counts and pattern observables are distinct; no scalar 'mass' is selected here.
    """
    rho,diagnostics = _state(rho,tol)
    h = _hermitian(H,len(rho))
    if not observables or len(observables)>64 or any(type(k) is not str for k in observables):
        raise ValueError("1..64 named observables required")
    names = sorted(observables)
    ops = [_hermitian(observables[k],len(rho)) for k in names]
    means = np.asarray([np.trace(rho@a) for a in ops])
    correlation = np.asarray([[np.trace(rho@a@b)-means[i]*means[j]
                               for j,b in enumerate(ops)] for i,a in enumerate(ops)])
    current = np.asarray([np.trace(rho@(1j*(h@a-a@h))) for a in ops])
    return {'scope':'FULL_SUPPLIED_STATE_MOMENTS_NOT_RECORD_QUALIFICATION',
            'state_diagnostics':diagnostics,'observable_names':names,
            'means_real':means.real.tolist(),'means_imag_residual':means.imag.tolist(),
            'connected_ordered_real':correlation.real.tolist(),
            'connected_ordered_imag':correlation.imag.tolist(),
            'instantaneous_currents_real':current.real.tolist(),
            'instantaneous_currents_imag_residual':current.imag.tolist(),
            'energy':float(np.trace(rho@h).real),
            'basis_probabilities':np.diag(rho).real.tolist(),
            'rho_real':rho.real.tolist(),'rho_imag':rho.imag.tolist(),
            'Gamma_qualification':'EXTERNAL_CERTIFICATE_REQUIRED',
            'assembly_release':False,'H1':'UNDETERMINED','H2':'UNDETERMINED'}


def coherent_history_functional(rho,steps,projector_families,tol=1e-11):
    """Returns COMPLETE D_hk for a declared finite projector-history family.
    Positive diagonal weights alone are not a native stochastic history measure.
    Summed off-diagonal absolute values bound additivity error for any union.
    No branch pruning, postselection or Markov multiplication is performed.
    """
    rho,diagnostics = _state(rho,tol)
    n=len(rho)
    steps=list(steps); families=[list(f) for f in projector_families]
    if not steps or len(steps)>MAX_STEPS or len(steps)!=len(families):
        raise ValueError("1..8 intervals with one complete projector family after each")
    number=1
    for f in families:
        if not f:raise ValueError("Empty outcome family")
        number*=len(f)
        if number>MAX_HISTORIES:raise ValueError("Complete history family exceeds method cap")
    unitary=[];projectors=[];defects=[]
    for u,fs in zip(steps,families):
        u=_square(u,n)
        ps=[_hermitian(p,n) for p in fs]
        metrics={'unitarity':float(np.linalg.norm(u.conj().T@u-np.eye(n),'fro')),
                 'completeness':float(np.linalg.norm(sum(ps)-np.eye(n),'fro')),
                 'idempotence':max(float(np.linalg.norm(p@p-p,'fro')) for p in ps),
                 'orthogonality':max([0.0]+[float(np.linalg.norm(ps[i]@ps[j],'fro'))
                                           for i in range(len(ps)) for j in range(i)])}
        if max(metrics.values())>tol:raise ValueError("Invalid unitary/projective family")
        unitary.append(u);projectors.append(ps);defects.append(metrics)
    paths=list(itertools.product(*(range(len(f)) for f in projectors)))
    classes=[]
    for path in paths:
        c=np.eye(n,dtype=complex)
        for u,ps,a in zip(unitary,projectors,path):c=ps[a]@u@c
        classes.append(c)
    D=np.asarray([[np.trace(c@rho@b.conj().T) for b in classes] for c in classes])
    off=D-np.diag(np.diag(D))
    return {'scope':'COMPLETE_COHERENT_HISTORY_FUNCTIONAL_NOT_A_NATIVE_CLASSICAL_PROCESS',
            'state_diagnostics':diagnostics,'step_residuals':defects,
            'paths':[list(p) for p in paths],'D_real':D.real.tolist(),'D_imag':D.imag.tolist(),
            'diagonal_weights':np.diag(D).real.tolist(),
            'diagonal_sum':float(np.trace(D).real),'all_pairs_sum_real':float(D.sum().real),
            'all_pairs_sum_imag':float(D.sum().imag),
            'offdiagonal_absolute_budget':float(np.abs(off).sum()),
            'D_hermiticity_defect':float(np.linalg.norm(D-D.conj().T,'fro')),
            'D_min_eigenvalue_diagnostic':float(np.linalg.eigvalsh((D+D.conj().T)/2)[0]),
            'stochastic_history_release':False,'error_status':'FLOAT_METHOD_NOT_OUTWARD_CERTIFIED'}
