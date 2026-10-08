"""Native coherent photon-probe coefficients; stdout only, one small worker."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CONFIG = dict(ages=[0.,.5,2.],durations=[.25,1.,2.],frequencies=[.75,1.5,3.],
              operators=['incidence','record_count'],quadrature_nodes=32,tolerance=1e-9,
              energy_group_tolerance=1e-10,occupied_weight_floor=1e-12)
PARENT_RESULT = '2b9b19954f137aaf0b60173481fdb9059cda3892ee3c71bd9a6884cbb4b6350a'
PARENT_FREEZE = '4d22da45549f2de78fc0477be6b5f23bc0f58b3598a312e2aa76d8f729ac9ff3'


def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inputs():
    rp,fp = HERE/'RECORD_ADDITION_RESULTS.json',HERE/'RECORD_ADDITION_FROZEN.json'
    if sha(rp)!=PARENT_RESULT or sha(fp)!=PARENT_FREEZE:
        raise RuntimeError('Parent file identity mismatch')
    parent,frozen = json.loads(rp.read_text()),json.loads(fp.read_text())
    if parent['status']!='COMPLETE' or not all(c['passed'] for c in parent['payload']['checks']):
        raise RuntimeError('Unqualified parent')
    if parent['payload_sha256']!=hashlib.sha256(encoded(parent['payload'])).hexdigest() or parent['freeze_sha256']!=PARENT_FREEZE:
        raise RuntimeError('Parent payload mismatch')
    files = dict(frozen['files'])
    for rel,digest in files.items():
        p=(ROOT/rel).resolve()
        if not p.is_relative_to(ROOT) or sha(p)!=digest:
            raise RuntimeError('Ancestor source mismatch: '+rel)
    for p in (rp,fp,Path(__file__).resolve(),HERE/'NATIVE_PHOTON_PROBE_PROTOCOL_V001.md'):
        files[str(p.relative_to(ROOT))]=sha(p)
    return parent,dict(config=CONFIG,files=files)


def taylor(h,t):
    a=-1j*t*h
    n=float(np.linalg.norm(a,ord=np.inf))
    s=max(0,math.ceil(math.log2(n/.5))) if n else 0
    a/=2**s
    n=float(np.linalg.norm(a,ord=np.inf))
    u=np.eye(len(h),dtype=complex)
    term,mag=u.copy(),1.
    for k in range(1,201):
        term=term @ a/k
        u+=term
        mag*=n/k
        if math.exp(n)*mag*n/(k+1)<=1e-18:
            break
    else:
        raise ArithmeticError('Taylor convergence failed')
    for _ in range(s):
        u=u @ u
    return u


def kernel(z,t):
    return t*np.sinc(z*t/(2*np.pi))*np.exp(.5j*z*t)


def comm(a,b):
    return a @ b-b @ a


def run():
    started=time.perf_counter()
    parent,snapshot=inputs()
    freeze=HERE/'NATIVE_PHOTON_PROBE_V001_FROZEN.json'
    if json.loads(freeze.read_text())!=snapshot:
        raise RuntimeError('Prospective freeze differs')
    spec=importlib.util.spec_from_file_location('photon_native_parent',HERE/'record_addition_compute.py')
    native=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    op=native.operators()
    ident=np.eye(16)
    r=op['QL']+op['QR']
    counts=[(ident-op['QL']) @ (ident-op['QR']),
            op['QL'] @ (ident-op['QR'])+(ident-op['QL']) @ op['QR'],op['QL'] @ op['QR']]
    cases,spectra,failures,maxima,counts_check=[],[],[],{},{}

    def check(name,value,expected=0.,tag='',tol=None):
        error=float(np.max(np.abs(np.asarray(value)-np.asarray(expected))))
        limit=CONFIG['tolerance'] if tol is None else tol
        maxima[name]=max(maxima.get(name,0.),error)
        counts_check[name]=counts_check.get(name,0)+1
        if not math.isfinite(error) or error>limit:
            failures.append(dict(check=name,case=tag,error=error,tolerance=limit))

    def real(value,tag):
        check('real_expectation',complex(value).imag,tag=tag)
        return float(complex(value).real)

    nodes,weights=np.polynomial.legendre.leggauss(CONFIG['quadrature_nodes'])
    for saved in parent['payload']['cases']:
        name=saved['name']
        pars=saved['parameters']
        psi0=np.asarray(saved['formed_vector']['real'])+1j*np.asarray(saved['formed_vector']['imag'])
        h,_=native.hamiltonian(dict(pars,g=0.),op)
        check('held_compact',h,3*ident+r-op['Xa']+(2.25*ident-pars['lambda_R']*r-.5*op['XC']) @ op['n'],tag=name)
        check('record_conserved',comm(h,r),tag=name)
        check('native_strength',comm(op['n'],comm(h,op['n'])),op['Xa'],tag=name)
        values,vectors=np.linalg.eigh(h)
        groups=[]
        for j,value in enumerate(values):
            if not groups or abs(value-groups[-1][0])>CONFIG['energy_group_tolerance']:
                groups.append([float(value),[j]])
            else:
                groups[-1][1].append(j)
        projectors=[(energy,vectors[:,idx] @ vectors[:,idx].conj().T) for energy,idx in groups]
        check('energy_projector_resolution',sum(p for e,p in projectors),ident,tag=name)
        analytic=[]
        for record in range(3):
            for carrier in (1,-1):
                x=2.25-pars['lambda_R']*record-.5*carrier
                gap=math.hypot(x,2.)
                pair=[]
                for band in (-1,1):
                    proj=counts[record] @ ((ident-band*(2*op['Xa']+x*op['Za'])/gap)/2) @ ((ident+carrier*op['XC'])/2)
                    energy=3+record+(x+band*gap)/2
                    check('analytic_projector',proj @ proj,proj,tag=name)
                    check('analytic_energy',h @ proj,energy*proj,tag=name)
                    pair.append(proj)
                analytic.append((gap,x,pair))
        wanted=sorted(set(round(a[0],12) for a in analytic))
        exact_wanted=[math.sqrt(k)/4 for k in ([113,185] if pars['lambda_R']==0 else [73,89,113,145,185])]
        check('structural_gap_census',wanted,exact_wanted,tag=name)
        rho0=np.outer(psi0,psi0.conj())
        stationary=sum(p @ rho0 @ p for e,p in projectors)
        check('stationary_trace',np.trace(stationary),1.,tag=name)
        check('stationary_commutator',comm(h,stationary),tag=name)
        check('stationary_positive',max(0.,-float(np.linalg.eigvalsh(stationary).min())),tag=name)
        for operator,b in [('incidence',op['n']),('record_count',r)]:
            line_abs=np.zeros(len(wanted))
            line_emit=np.zeros(len(wanted))
            zero=0.
            unexpected=[]
            for ei,pi in projectors:
                for ej,pj in projectors:
                    trans=pi @ b @ pj
                    weight=real(np.trace(trans @ stationary @ trans.conj().T),name)
                    check('line_nonnegative',max(0.,-weight),tag=name)
                    gap=ei-ej
                    if abs(gap)<CONFIG['energy_group_tolerance']:
                        zero+=weight
                    elif np.linalg.norm(trans)>1e-10:
                        if operator=='record_count':
                            unexpected.append(gap)
                            continue
                        index=int(np.argmin(np.abs(np.asarray(wanted)-abs(gap))))
                        check('numerical_allowed_gap',abs(gap),wanted[index],tag=name)
                        if gap>0:
                            line_abs[index]+=weight
                        else:
                            line_emit[index]+=weight
            check('unexpected_record_gap',len(unexpected),0.,tag=name,tol=0.)
            expected_abs=np.zeros(len(wanted))
            expected_emit=np.zeros(len(wanted))
            if operator=='incidence':
                zero_analytic=0.
                for gap,x,pair in analytic:
                    index=int(np.argmin(np.abs(np.asarray(wanted)-gap)))
                    plow=real(np.vdot(psi0,pair[0] @ psi0),name)
                    phigh=real(np.vdot(psi0,pair[1] @ psi0),name)
                    expected_abs[index]+=plow/gap**2
                    expected_emit[index]+=phigh/gap**2
                    zero_analytic+=plow*((1-x/gap)/2)**2+phigh*((1+x/gap)/2)**2
                check('analytic_absorption_weights',line_abs,expected_abs,tag=name)
                check('analytic_emission_weights',line_emit,expected_emit,tag=name)
            else:
                zero_analytic=real(np.trace(stationary @ b @ b),name)
                check('record_absorption_lines',line_abs,tag=name)
                check('record_emission_lines',line_emit,tag=name)
            check('elastic_weight',zero,zero_analytic,tag=name)
            check('zeroth_spectral_moment',zero+sum(line_abs)+sum(line_emit),np.trace(stationary @ b @ b),tag=name)
            check('first_spectral_moment',2*np.dot(wanted,line_abs-line_emit),np.trace(stationary @ comm(b,comm(h,b))),tag=name)
            lines=[]
            for gap,wa,we in zip(wanted,line_abs,line_emit):
                beta=math.log(wa/we)/gap if min(wa,we)>CONFIG['occupied_weight_floor'] else None
                lines.append(dict(omega=gap,absorption=wa,emission=we,beta_eff=beta))
            spectra.append(dict(preparation=name,operator=operator,elastic_weight=zero,lines=lines,
                                actual_initial_moment=real(np.vdot(psi0,comm(b,comm(h,b)) @ psi0),name),
                                stationary_moment=real(np.trace(stationary @ comm(b,comm(h,b))),name)))
            b_energy=vectors.conj().T @ b @ vectors
            for duration in CONFIG['durations']:
                sample_times=(nodes+1)*duration/2
                sample_weights=weights*duration/2
                b_t=[]
                for sample in sample_times:
                    u=taylor(h,sample)
                    b_t.append(u.conj().T @ b @ u)
                for omega in CONFIG['frequencies']:
                    integrals={}
                    for sign in (1,-1):
                        exact=vectors @ (b_energy*kernel(values[:,None]-values[None,:]+sign*omega,duration)) @ vectors.conj().T
                        quad=sum(w*np.exp(sign*1j*omega*s)*bt for s,w,bt in zip(sample_times,sample_weights,b_t))
                        check('spectral_vs_quadrature_integral',exact,quad,tag=name)
                        check('integral_operator_bound',max(0.,float(np.linalg.norm(exact,2))-duration*float(np.linalg.norm(b,2))),tag=name)
                        if operator=='record_count':
                            check('static_record_integral',exact,kernel(sign*omega,duration)*r,tag=name)
                        integrals[sign]=exact
                    check('integral_adjoint',integrals[-1],integrals[1].conj().T,tag=name)
                    for age in CONFIG['ages']:
                        psi=(vectors*np.exp(-1j*age*values)) @ vectors.conj().T @ psi0
                        rho=np.outer(psi,psi.conj())
                        dephased=sum(p @ rho @ p for e,p in projectors)
                        check('stationary_age_invariance',dephased,stationary,tag=name)
                        answers={}
                        for sign,key in [(1,'emission'),(-1,'absorption')]:
                            f=integrals[sign]
                            full=real(np.vdot(f @ psi,f @ psi),name)
                            stationary_answer=real(np.trace(stationary @ f.conj().T @ f),name)
                            if operator=='record_count':
                                check('bounded_record_response',full,abs(kernel(omega,duration))**2*np.vdot(psi,r @ r @ psi),tag=name)
                                check('record_full_vs_stationary',full,stationary_answer,tag=name)
                            check('finite_coefficient_nonnegative',max(0.,-full,-stationary_answer),tag=name)
                            answers[key]=full
                            answers[key+'_dephased']=stationary_answer
                        cases.append(dict(preparation=name,operator=operator,age=age,duration=duration,omega=omega,**answers))
    check('case_census',len(cases),162,tol=0.)
    check('spectrum_census',len(spectra),6,tol=0.)
    payload=dict(config=CONFIG,cases=cases,spectra=spectra,maximum_errors=maxima,check_counts=counts_check,failures=failures,
                 scope='Conditional microscopic photon probe, finite-time coefficients and separate stationary spectral diagnostic; no physical CMB fit.')
    result=dict(status='COMPLETE' if not failures else 'FAILED',payload=payload,payload_sha256=hashlib.sha256(encoded(payload)).hexdigest(),
                freeze_sha256=sha(freeze),seconds=time.perf_counter()-started,peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print(json.dumps(result,allow_nan=False))
    return 1 if failures else 0


if __name__=='__main__':
    if sys.argv[1:]==['freeze']:
        print(json.dumps(inputs()[1],indent=2))
    elif sys.argv[1:]:
        raise SystemExit('Use freeze or no arguments')
    else:
        raise SystemExit(run())
