"""P50 Codex3 SOURCE ONLY. Root runs after distinct review; theory0217 governs.
Unitary candidate preparations only; no b-dagger postselection or physical species.
"""
import math
import numpy as np


def _matrix(x,n=None):
    a=np.asarray(x,dtype=complex)
    if a.ndim!=2 or a.shape[0]!=a.shape[1] or not 1<=len(a)<=32:
        raise ValueError('square dimension1..32 required')
    if n is not None and a.shape!=(n,n):
        raise ValueError('dimension mismatch')
    if not np.isfinite(a).all():raise ValueError('nonfinite matrix')
    return a


def candidate_signature(H,rho,preparations,probes,reads,tolerance=1e-10):
    """Absolute and differential costs/currents; no lifetime/rest-mass inference."""
    if type(tolerance) not in (int,float) or not math.isfinite(tolerance) or tolerance<=0:
        raise ValueError('positive finite tolerance required')
    H=_matrix(H);n=len(H);rho=_matrix(rho,n)
    if not np.array_equal(H,H.conj().T) or not np.array_equal(rho,rho.conj().T):
        raise ValueError('exact stored Hermiticity required')
    eigmin=float(np.linalg.eigvalsh(rho)[0]);trace_error=float(abs(np.trace(rho)-1))
    if eigmin < -tolerance or trace_error>tolerance:
        raise ValueError('trace-one positive state required')
    ident=np.eye(n)
    def registry(value,unitary):
        if not isinstance(value,dict) or not 1<=len(value)<=8 or any(type(k) is not str or not k for k in value):
            raise ValueError('one to8 named operators required')
        result={}; defects={}
        for name,x in value.items():
            a=_matrix(x,n)
            if unitary:
                defect=float(np.linalg.norm(a.conj().T@a-ident,'fro'))
                if defect>tolerance:raise ValueError('unitary preparation/probe required')
            else:
                if not np.array_equal(a,a.conj().T):raise ValueError('Hermitian transport read required')
                defect=0.0
            result[name]=a;defects[name]=defect
        return result,defects
    ps,pd=registry(preparations,True);ws,wd=registry(probes,True);rs,_=registry(reads,False)
    costs={k:w.conj().T@H@w-H for k,w in ws.items()}
    currents={k:1j*(H@a-a@H) for k,a in rs.items()}
    def snapshot(state):
        return {'rho':state.tolist(),'energy':complex(np.trace(H@state)),
            'writer_costs':{k:complex(np.trace(c@state)) for k,c in costs.items()},
            'currents':{k:complex(np.trace(j@state)) for k,j in currents.items()},
            'state_trace':complex(np.trace(state))}
    baseline=snapshot(rho);rows={}
    for name,v in ps.items():
        state=v@rho@v.conj().T;s=snapshot(state)
        s['preparation_work_not_rest_energy']=s['energy']-baseline['energy']
        s['writer_cost_changes']={k:s['writer_costs'][k]-baseline['writer_costs'][k] for k in costs}
        s['current_changes']={k:s['currents'][k]-baseline['currents'][k] for k in currents}
        rows[name]=s
    return {'scope':'SUPPLIED_UNITARY_CANDIDATE_SIGNATURE_METHOD_ONLY',
        'baseline':baseline,'candidates':rows,'cost_operators':{k:a.tolist() for k,a in costs.items()},
        'current_operators':{k:a.tolist() for k,a in currents.items()},
        'diagnostics':{'input_min_eigenvalue':eigmin,'input_trace_error':trace_error,
                       'preparation_unitarity_fro':pd,'probe_unitarity_fro':wd},
        'error_scope':'FLOAT_DIAGNOSTICS_NOT_CERTIFIED_FULL_ERROR',
        'species_qualification':'LOCALIZATION_PERSISTENCE_REST_ENERGY_RECORD_AND_UNIVERSALITY_NOT_TESTED',
        'writer_qualification':'COMPARATOR_ONLY_UNLESS_SEPARATELY_CERTIFIED',
        'native_matter_release':False,'H1':'UNDETERMINED','H2':'UNDETERMINED'}


def proposed_controls(tolerance=1e-9):
    """Root-only fixed2D/4D method inputs, raw returns and actual refusals."""
    I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
    n=np.diag([0,1]).astype(complex);N=np.kron(n,I);Q=np.kron(I,n)
    xfirst=np.kron(X,I);xq=np.kron(I,X)
    rho=np.zeros((4,4),complex);rho[0,0]=1
    contexts={
        'incidence_bias':(5*N+3*Q-2*N@Q,rho,{'candidate':xfirst},{'q':xq},{'inventory':N}),
        'carrier_instant_null':(5*N+3*Q+N@xq,rho,{'candidate':xfirst},{'q':xq},{'inventory':N}),
        'phase_current':(-X,(I+Y)/2,{'candidate':Z},{'q':X},{'inventory':I-n})}
    records={};checks={};refusals={}
    def pack(h,r,p,w,a):
        return {'H':h.tolist(),'rho':r.tolist(),
            'preparations':{k:v.tolist() for k,v in p.items()},
            'probes':{k:v.tolist() for k,v in w.items()},
            'reads':{k:v.tolist() for k,v in a.items()},'tolerance':tolerance}
    for name,args in contexts.items():
        records[name]={'inputs':pack(*args),'result':candidate_signature(*args,tolerance=tolerance)}
    expected={'incidence_bias':(5,3,1,-2,0,0),
              'carrier_instant_null':(5,3,3,0,0,0),
              'phase_current':(0,0,0,0,-1,1)}
    for name,(work,c0,c1,bias,j0,j1) in expected.items():
        r=records[name]['result'];a=r['baseline'];b=r['candidates']['candidate']
        values=[b['preparation_work_not_rest_energy'],a['writer_costs']['q'],
                b['writer_costs']['q'],b['writer_cost_changes']['q'],
                a['currents']['inventory'],b['currents']['inventory']]
        checks[name]=all(abs(x-y)<tolerance for x,y in zip(values,(work,c0,c1,bias,j0,j1)))
    h,r,p,w,a=contexts['phase_current']
    badh=h.copy();badh[0,1]=0
    for name,args in [
        ('nonhermitian',(badh,r,p,w,a)),
        ('bad_density',(h,np.diag([2,-1]).astype(complex),p,w,a)),
        ('nonunitary_candidate',(h,r,{'candidate':2*Z},w,a)),
        ('nonunitary_probe',(h,r,p,{'q':2*X},a)),
        ('nonhermitian_read',(h,r,p,w,{'inventory':np.array([[0,1],[0,0]],complex)})),
        ('empty_candidates',(h,r,{},w,a)),
    ]:
        record={'inputs':pack(*args)}
        try:
            result=candidate_signature(*args,tolerance=tolerance)
        except ValueError as error:
            record.update(refused=True,exception=type(error).__name__,message=str(error))
        else:record.update(refused=False,unexpected_return=result)
        refusals[name]=record;checks['refuses_'+name]=record['refused']
    return {'cases':records,'refusals':refusals,'checks':checks,'all_method_checks':all(checks.values()),
            'status':'FIXED_COMPARATOR_CONTROLS_NOT_PHYSICAL_SPECIES','native_matter_release':False}
