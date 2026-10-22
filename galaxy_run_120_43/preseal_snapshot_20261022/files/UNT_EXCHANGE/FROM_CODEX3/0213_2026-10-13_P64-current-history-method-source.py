"""P64 Codex3 SOURCE ONLY; root executes after distinct review.
Theory0212 governs. Supplied class provenance and native observables are external.
Dense fixed METHOD scope only; no physical motion/geometry or velocity conversion.
"""
from itertools import islice, product
import math
import numpy as np


def matrix(x,n=None):
    a=np.asarray(x,dtype=complex)
    if a.ndim!=2 or a.shape[0]!=a.shape[1] or not 1<=len(a)<=32:
        raise ValueError('complete square dimension1..32 required')
    if n is not None and a.shape!=(n,n):
        raise ValueError('dimension mismatch')
    if not np.isfinite(a).all():
        raise ValueError('nonfinite matrix')
    return a


def history_current(H,rho,A,U,classes,tolerance=1e-10):
    """Retain full D_hk and Hermitian current insertion M_hk, no Markov reduction.
    sum C=U is checked; arbitrary supplied decompositions are not certified histories.
    Input-tolerance and arithmetic errors are NOT certified by float diagnostics.
    """
    if type(tolerance) not in (int,float) or not math.isfinite(tolerance) or tolerance<=0:
        raise ValueError('positive finite tolerance required')
    H=matrix(H); n=len(H)
    rho,A,U=[matrix(x,n) for x in (rho,A,U)]
    if any(not np.array_equal(x,x.conj().T) for x in (H,rho,A)):
        raise ValueError('exact stored Hermiticity required')
    trace_error=float(abs(np.trace(rho)-1))
    rho_min=float(np.linalg.eigvalsh(rho)[0])
    if trace_error>tolerance or rho_min < -tolerance:
        raise ValueError('trace-one positive state required')
    cs=list(islice(iter(classes),17))
    if not 1<=len(cs)<=16:
        raise ValueError('one to16 complete class operators required')
    cs=[matrix(c,n) for c in cs]
    unitary_error=float(np.linalg.norm(U.conj().T@U-np.eye(n),'fro'))
    class_error=float(np.linalg.norm(sum(cs)-U,'fro'))
    if unitary_error>tolerance:
        raise ValueError('unitary evolution required')
    if class_error>tolerance:
        raise ValueError('complete class sum must equal evolution')
    J=1j*(H@A-A@H)
    final=U@rho@U.conj().T
    D=np.asarray([[np.trace(c@rho@b.conj().T) for b in cs] for c in cs])
    M=np.asarray([[np.trace(J@c@rho@b.conj().T) for b in cs] for c in cs])
    current=np.trace(J@final)
    diagonal=np.trace(M)
    phase=[[float(np.angle(z)) if abs(z)>tolerance else None for z in row] for row in D]
    return {'scope':'SUPPLIED_COHERENT_CLASS_CURRENT_METHOD_ONLY',
        'J':J.tolist(),'rho_final':final.tolist(),'D':D.tolist(),'M_current':M.tolist(),
        'D_phase_radians':phase,'phase_null_meaning':'UNRESOLVED_BELOW_FLOAT_TOLERANCE_NOT_PROVEN_ZERO',
        'absolute_current':complex(current),'diagonal_class_current':complex(diagonal),
        'offdiagonal_current':complex(M.sum()-diagonal),
        'D_diagonal_sum':complex(np.trace(D)),'D_total':complex(D.sum()),
        'diagnostics':{'rho_trace_error':trace_error,'rho_min_eigenvalue':rho_min,
            'unitarity_fro':unitary_error,'class_sum_fro':class_error,
            'D_hermiticity_fro':float(np.linalg.norm(D-D.conj().T,'fro')),
            'M_hermiticity_fro':float(np.linalg.norm(M-M.conj().T,'fro')),
            'current_sum_error':float(abs(M.sum()-current))},
        'error_scope':'FLOAT_DIAGNOSTICS_ONLY_NOT_CERTIFIED_INPUT_OR_PROPAGATION_ERROR',
        'class_provenance':'ROOT_MUST_AUTHENTICATE_NATIVE_PROJECTORS_AND_FULL_HISTORIES',
        'native_motion_release':False,'H1':'UNDETERMINED','H2':'UNDETERMINED'}


def proposed_controls(tolerance=1e-9):
    """Root-only fixed2D controls, all inputs/raw results and actual refusals retained."""
    I=np.eye(2,dtype=complex)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    P=np.array([[1,0],[0,0]],complex); Q=I-P
    rho=(I+Y)/2
    cases={};checks={};refusals={}
    def run(name,h,r,a,u,cs):
        record={'inputs':{'H':h.tolist(),'rho':r.tolist(),'A':a.tolist(),'U':u.tolist(),
                          'classes':[c.tolist() for c in cs],'tolerance':tolerance}}
        record['result']=history_current(h,r,a,u,cs,tolerance)
        cases[name]=record
        return record['result']
    pos=run('hopping',-X,rho,P,I,[P,Q])
    rev=run('reversed_phase',-X,(I-Y)/2,P,I,[P,Q])
    S=np.diag([1j,1])
    gauge=run('common_frame',S@(-X)@S.conj().T,S@rho@S.conj().T,
              S@P@S.conj().T,I,[P,Q])
    step=(I-1j*X)/math.sqrt(2)
    paths=list(product((0,1),repeat=3));projs=[P,Q]
    cs=[projs[c]@step@projs[b]@step@projs[a] for a,b,c in paths]
    bind=run('bind_no_transport',X,P,I,step@step,cs)
    bd=np.asarray(bind['D']);pm=np.asarray(pos['M_current']);pd=np.asarray(pos['D'])
    checks['hopping_current']=abs(pos['absolute_current']+1)<tolerance
    checks['zero_D_offdiag']=abs(pd[0,1])+abs(pd[1,0])<tolerance
    checks['inserted_cross_current']=abs(pm[0,1]+0.5)+abs(pm[1,0]+0.5)<tolerance
    checks['reverse']=abs(rev['absolute_current']-1)<tolerance
    checks['common_frame']=max(float(np.max(np.abs(np.asarray(gauge[k])-np.asarray(pos[k]))))
                               for k in ('D','M_current'))<tolerance
    checks['Bind_interference']=abs(bd[paths.index((0,0,0)),paths.index((0,1,0))]+0.25)<tolerance
    checks['Bind_zero_current']=float(np.max(np.abs(np.asarray(bind['M_current']))))<tolerance
    badH=(-X).copy();badH[0,1]=0
    badrho=np.diag([2,-1]).astype(complex)
    for name,h,r,a,u,c in [
        ('hermiticity',badH,rho,P,I,[P,Q]),
        ('density',-X,badrho,P,I,[P,Q]),
        ('class_sum',-X,rho,P,I,[P]),
        ('unitarity',-X,rho,P,2*I,[2*P,2*Q]),
        ('read',-X,rho,np.array([[0,1],[0,0]],complex),I,[P,Q]),
        ('empty_classes',-X,rho,P,I,[]),
        ('too_many_classes',-X,rho,P,I,[I/17]*17),
    ]:
        record={'inputs':{'H':h.tolist(),'rho':r.tolist(),'A':a.tolist(),'U':u.tolist(),
                          'classes':[v.tolist() for v in c],'tolerance':tolerance}}
        try:
            result=history_current(h,r,a,u,c,tolerance)
        except ValueError as error:
            record.update(refused=True,exception=type(error).__name__,message=str(error))
        else:
            record.update(refused=False,unexpected_return=result)
        refusals[name]=record
        checks['refuses_'+name]=record['refused']
    return {'cases':cases,'refusals':refusals,'checks':checks,'all_method_checks':all(checks.values()),
            'bind_paths':[list(p) for p in paths],
            'status':'PROSPECTIVE_MANUFACTURED_CURRENT_CONTROLS_ONLY','native_motion_release':False}
