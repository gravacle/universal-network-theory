"""Universal vector orbit kernel; five synthetic cases, stdout-only output."""
import os
import sys
sys.dont_write_bytecode=True
for _key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_key]='1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from numpy.polynomial.polynomial import polyval

HERE=Path(__file__).resolve().parent
FREEZE=HERE/'VECTOR_ORBIT_KERNEL_V001_FROZEN.json'
NOTE='ISOTROPIC_VECTOR_ORBIT_RESPONSE_V001.md'
NOTE_SHA='691a7476af57c9f5f55a63f2bad44b274affca82e6b9af6aa16fe3f9884673c4'
CONFIG=dict(r=[0.,1e-4,.01,1.,100.],k=1.,m=1.,b=1.,orders=[64,128],
    series_degree=64,steps_per_half=[1024,2048],analytic_tolerance=2e-11,
    tail_tolerance=2e-12,ode_tolerance=2e-7,
    q_fractions=[0.,.125,.5,.875,1.],profile_y=[-1.,-.75,-.5,-.25,0.,.25,.5,.75,1.])


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources():
    if sha(HERE/NOTE)!=NOTE_SHA:
        raise RuntimeError('Settled vector derivation changed')
    names=(Path(__file__).name,'VECTOR_ORBIT_KERNEL_PROTOCOL_V001.md',NOTE,
           'FIXED_ACTION_SUSCEPTIBILITY_CONSTRAINT_V001.md')
    return dict(configuration=CONFIG,files={n:sha(HERE/n) for n in names})


def coefficients():
    a=np.ones(CONFIG['series_degree']+1)
    for n in range(1,len(a)):
        a[n]=a[n-1]*2*n/(2*n+1)
    return a,np.arange(1,len(a))*a[1:]


def unit_rule(order):
    x,w=leggauss(order)
    return (x+1)/2,w/2


def transverse(u,y,order,coef):
    y=np.asarray(y,dtype=float)
    K=1+u;eta=u/(2*K)
    s,w=unit_rule(order)
    q=eta*(1-y[...,None]**2*s*s)
    derivative=polyval(q,coef[1])
    value=polyval(eta,coef[0])/K+2*eta*y*y/K*np.sum(w*(1-s)*derivative,axis=-1)
    dy=2*eta*y/K*np.sum(w*derivative,axis=-1)
    dyy=2*eta/K*polyval(eta*(1-y*y),coef[1])
    return value,dy,dyy


def orbit_mean(u,order,coef):
    z,w=leggauss(order)
    theta=(z+1)*math.pi/4;weight=w*math.pi/4
    y=np.sin(theta);q=1+u*(1+y*y)/2
    measure=weight/np.sqrt(q);norm=np.sum(measure)
    xi,_,_=transverse(u,y,order,coef)
    parallel=(1+u*y*y)/(1+u)**2
    return dict(period=float(4*norm),chi_perp=float(measure@xi/norm),
                chi_parallel=float(measure@parallel/norm))


def shoot(u,period,steps):
    half=period/2;dt=half/steps
    state=np.zeros(11);state[0]=1.;state[2]=1.;state[5]=1.
    history=np.empty((2*steps+1,11));history[0]=state

    def rhs(v):
        out=np.empty(11);q=1+u*v[0]*v[0]
        out[0]=v[1];out[1]=-q*v[0]
        out[2]=v[3];out[3]=-q*v[2]
        out[4]=v[5];out[5]=-q*v[4]
        out[6]=v[7];out[7]=1-q*v[6]
        out[8]=v[2];out[9]=v[4];out[10]=v[6]
        return out

    for i in range(2*steps):
        a=rhs(state);b=rhs(state+dt*a/2);c=rhs(state+dt*b/2);d=rhs(state+dt*c)
        state=state+dt*(a+2*b+2*c+d)/6
        history[i+1]=state
    endpoint=history[steps]
    M=np.array([[endpoint[2],endpoint[4]],[endpoint[3],endpoint[5]]])
    initial=np.linalg.solve(np.eye(2)-M,endpoint[6:8])
    xi=history[:,6]+initial[0]*history[:,2]+initial[1]*history[:,4]
    xidot=history[:,7]+initial[0]*history[:,3]+initial[1]*history[:,5]
    integral=history[:,10]+initial[0]*history[:,8]+initial[1]*history[:,9]
    angular=history[:,0]*xidot-history[:,1]*xi
    free_angular=history[:,0]*history[:,5]-history[:,1]*history[:,4]
    witnesses=np.arange(0,2*steps+1,steps//4,dtype=int)
    return dict(steps_per_half=steps,dt=dt,M=M,initial=initial,history=history,
        xi=xi,xidot=xidot,angular=angular,free_angular=free_angular,
        mean_half=float(integral[steps]/half),mean_full=float(integral[-1]/period),
        angular_mean=float(np.sum(angular[:-1]+angular[1:])/(4*steps)),
        indices=witnesses,profile_y=history[witnesses,0],profile_velocity=history[witnesses,1],
        profile_xi=xi[witnesses],profile_xidot=xidot[witnesses])


def run():
    started=time.perf_counter();snapshot=sources()
    if json.loads(FREEZE.read_text())!=snapshot:
        raise RuntimeError('Prospective source freeze differs')
    coef=coefficients();checks=[];cases=[]

    def check(name,left,right=0.,scale=1.,upper=False,ode=False):
        tol=CONFIG['ode_tolerance'] if ode else CONFIG['analytic_tolerance']
        difference=np.asarray(left)-np.asarray(right)
        error=float(np.max((np.maximum(difference,0) if upper else np.abs(difference))/np.asarray(scale)))
        checks.append(dict(name=name,normalized_error=error,tolerance=tol,
                           passed=bool(math.isfinite(error) and error<=tol)))

    for u in CONFIG['r']:
        label=f'r={u}';K=1+u;eta=u/(2*K);energy=.5+u/4
        q=eta*np.array(CONFIG['q_fractions'])
        series=polyval(q,coef[0]);derivative=polyval(q,coef[1])
        exact=np.ones_like(q);positive=q>0
        exact[positive]=np.arcsin(np.sqrt(q[positive]))/np.sqrt(q[positive]*(1-q[positive]))
        check(label+':L_arcsine',series,exact)
        check(label+':L_differential_identity',2*q*(1-q)*derivative+(1-2*q)*series,1.)
        n=CONFIG['series_degree']
        tails=dict(L=eta**(n+1)/(1-eta),L_prime=eta**n*((n+1)-n*eta)/(1-eta)**2)
        check(label+':series_tail',max(tails.values())/CONFIG['tail_tolerance'],1.,upper=True)
        raw=[orbit_mean(u,order,coef) for order in CONFIG['orders']]
        low,high=raw
        for key in high:
            check(label+':quadrature:'+key,low[key],high[key],max(1.,abs(high[key])))
        y=np.array(CONFIG['profile_y']);xi,dy,dyy=transverse(u,y,128,coef)
        speed2=2*energy-y*y-u*y**4/2;accel=-y-u*y**3
        check(label+':transverse_ODE',dyy*speed2+dy*accel+(1+u*y*y)*xi,1.)
        par=(1+u*y*y)/K**2;par_y=2*u*y/K**2;par_yy=2*u/K**2
        check(label+':parallel_ODE',par_yy*speed2+par_y*accel+(1+3*u*y*y)*par,1.)
        check(label+':even_value',xi,xi[::-1])
        check(label+':odd_derivative',dy,-dy[::-1])
        check(label+':center_derivative',dy[len(y)//2])
        check(label+':parallel_below_transverse',par,xi,upper=True)
        check(label+':transverse_lower',polyval(eta,coef[0])/K,xi,upper=True)
        upper=4*K/(2+u)**2
        check(label+':transverse_upper',xi,upper,upper=True)
        check(label+':relaxed_upper',upper,1.,upper=True)
        numerical=[];rawshoot=[]
        for steps in CONFIG['steps_per_half']:
            shot=shoot(u,high['period'],steps);rawshoot.append(shot)
            name=label+f':steps={steps}'
            h=shot['history'];M=shot['M'];velocity_scale=max(1.,math.sqrt(K))
            e=h[:,1]**2/2+h[:,0]**2/2+u*h[:,0]**4/4
            check(name+':orbit_energy',e,energy,max(1.,energy),ode=True)
            check(name+':orbit_half_y',h[steps:,0],-h[:steps+1,0],ode=True)
            check(name+':orbit_half_velocity',h[steps:,1],-h[:steps+1,1],velocity_scale,ode=True)
            check(name+':rotation_solution',h[:,2],h[:,0],ode=True)
            check(name+':rotation_velocity',h[:,3],h[:,1],velocity_scale,ode=True)
            check(name+':Floquet_trace',np.trace(M),-2.,ode=True)
            check(name+':Floquet_determinant',np.linalg.det(M),1.,ode=True)
            check(name+':forced_sector_determinant',np.linalg.det(np.eye(2)-M),4.,ode=True)
            check(name+':BVP_endpoint',(np.eye(2)-M)@shot['initial'],h[steps,6:8],ode=True)
            check(name+':periodic_position',shot['xi'][steps:],shot['xi'][:steps+1],ode=True)
            check(name+':periodic_velocity',shot['xidot'][steps:],shot['xidot'][:steps+1],velocity_scale,ode=True)
            check(name+':initial_reflection_velocity',shot['initial'][1],scale=velocity_scale,ode=True)
            check(name+':mean_half',shot['mean_half'],high['chi_perp'],ode=True)
            check(name+':mean_full',shot['mean_full'],high['chi_perp'],ode=True)
            check(name+':angular_half_antisymmetry',shot['angular'][steps:],
                  -shot['angular'][:steps+1],velocity_scale,ode=True)
            check(name+':angular_mean',shot['angular_mean'],scale=velocity_scale,ode=True)
            check(name+':free_angular_Wronskian',shot['free_angular'],1.,ode=True)
            theoretical,theory_dy,_=transverse(u,shot['profile_y'],128,coef)
            check(name+':profile_value',shot['profile_xi'],theoretical,ode=True)
            check(name+':profile_velocity',shot['profile_xidot'],theory_dy*shot['profile_velocity'],velocity_scale,ode=True)
            numerical.append(dict(steps_per_half=steps,dt=shot['dt'],
                monodromy=M.tolist(),initial_forced_data=shot['initial'].tolist(),
                determinant_I_minus_M=float(np.linalg.det(np.eye(2)-M)),
                condition_I_minus_M=float(np.linalg.cond(np.eye(2)-M)),
                mean_half=shot['mean_half'],mean_full=shot['mean_full'],
                full_period_mean_induced_angular_momentum=shot['angular_mean'],
                profile_time_over_T=(shot['indices']/(2*steps)).tolist(),
                profile_y=shot['profile_y'].tolist(),profile_velocity=shot['profile_velocity'].tolist(),
                profile_xi=shot['profile_xi'].tolist(),profile_xidot=shot['profile_xidot'].tolist()))
        a,b=rawshoot
        check(label+':coarse_fine_mean',a['mean_half'],b['mean_half'],ode=True)
        check(label+':coarse_fine_profile',a['profile_xi'],b['profile_xi'],ode=True)
        iso=(high['chi_parallel']+2*high['chi_perp'])/3
        if u==0:
            check(label+':harmonic_means',[high['chi_perp'],high['chi_parallel'],iso],1.)
            check(label+':harmonic_profile',xi,1.)
        cases.append(dict(r=u,k=1.,m=1.,b=1.,u=u,energy=energy,eta=eta,
            series_tail_bounds=tails,quadratures=[dict(order=o,**v) for o,v in zip(CONFIG['orders'],raw)],
            pointwise_bounds=dict(lower=float(polyval(eta,coef[0])/K),upper=upper,relaxed=1.),
            chi_iso_conditional=iso,mu_iso=1-iso,mu_parallel=1-high['chi_parallel'],
            small_r_deficit_coefficients=None if u==0 else dict(
                transverse=(1-high['chi_perp'])/u,parallel=(1-high['chi_parallel'])/u,isotropic=(1-iso)/u),
            exact_profile_y=y.tolist(),exact_xi=xi.tolist(),exact_dxi_dy=dy.tolist(),
            independent_shooting=numerical))
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':
        peak*=1024
    payload=dict(configuration=CONFIG,cases=cases,checks=checks,
        scope='Five synthetic fixed-fast-action, selected half-periodic vector kernels; not arbitrary switch-on, permanent isotropy, native derivation, or gravity prediction.',
        seconds=time.perf_counter()-started,peak_rss_bytes=int(peak))
    return dict(status='COMPLETE' if all(c['passed'] for c in checks) else 'FAILED_CHECKS',
        freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)


def main():
    if sys.argv[1:]==['freeze']:
        output=sources()
    elif sys.argv[1:]==['run']:
        output=run()
    else:
        raise ValueError('usage: vector_orbit_kernel_v001.py freeze|run')
    print(encode(output).decode())


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(status='ERROR',error_type=type(exc).__name__,error=str(exc))))
        sys.exit(1)
