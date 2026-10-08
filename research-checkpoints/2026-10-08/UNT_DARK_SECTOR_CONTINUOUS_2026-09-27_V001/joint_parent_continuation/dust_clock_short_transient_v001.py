"""One fixed short ordinary-source evolution and forced nonlinear harmonics."""
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
import dust_clock_local_poles_v001 as reference

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE/'DUST_CLOCK_SHORT_TRANSIENT_V001.md'
OUTPUT = HERE/'DUST_CLOCK_SHORT_TRANSIENT_V001_RESULT.json'
AMP, AI, LENGTH = 1e-8, .1, .05
LEVELS = (2048,4096,8192)
READOUTS = ('Psi','Delta','n','p_theta','p_sigma')


def background(x, k):
    a = AI*math.exp(x)
    h = math.sqrt((reference.OB/a**3+(reference.HVAC/reference.HREF)**2)
                  /(1+1.5*reference.BETA))
    r = 1.5*reference.OB/a**3
    p = reference.C_KMS*k/(a*reference.HREF)
    q = reference.ELL_MPC*k/a
    cf = reference.C_SI**2*(k/a/reference.MPC)/reference.A0
    return a,h,r,p,q,cf


def apply_matrix(y, h, r, p, q):
    eps = q*q*(2+q*q)
    fbg, aa = 1+1.5*reference.BETA, 3+2/reference.BETA
    out = np.empty_like(y)
    out[...,0] = -h*y[...,0]+r/fbg*y[...,1]-p*p/aa*y[...,2]
    out[...,1] = y[...,0]
    out[...,2] = eps*y[...,0]+(1+eps)*y[...,3]
    out[...,3] = -h*y[...,3]-r*(y[...,1]+3*y[...,2]/aa)
    return out


def rhs(x, y, k, harmonics):
    _,h,r,p,q,cf = background(x,k)
    out = np.empty_like(y)
    out[0] = apply_matrix(y[0],h,r,p,q)
    out[1:] = apply_matrix(y[1:],h,r,p*harmonics,q*harmonics)
    f1 = 1/(1+q*q)
    fm = 1/(1+(q*harmonics)**2)
    nbar = (y[0,0]+y[0,3])/f1**2
    coefficient = 8/(math.pi*harmonics**2*(4-harmonics**2))
    forcing = (f1*f1/fm)*cf*coefficient*AMP*nbar*abs(nbar)
    out[1:,2] += forcing
    return out/h


def inspect(x,y,k,mm):
    a,h,r,p,q,cf = background(x,k)
    modes = np.concatenate(([1.],mm))
    pp,qq = p*modes,q*modes
    nn = (1+qq*qq)**2*(y[:,0]+y[:,3])
    de = pp*pp*y[:,3]/r
    rr = np.stack((y[:,0],de,nn,pp*y[:,1],pp*y[:,2]),axis=1)*AMP
    # Reconstruct the leading nonlinear lapse correction as well.
    f1 = 1/(1+q*q)
    fm = 1/(1+(q*mm)**2)
    n1 = nn[0]*AMP
    forcing = (f1*f1/fm)*cf*(8/(math.pi*mm**2*(4-mm**2)))*n1*abs(n1)
    rr[1:,2] += forcing
    dn = de-3*h*y[:,1]
    ze = -y[:,0]+h*y[:,2]
    hv = h*(y[:,1]+y[:,2])
    metric = np.array([np.sum(np.abs(y[:,0]))*AMP,
                       np.sum(np.abs(rr[:,2])),
                       np.sum(np.abs(ze))*AMP,
                       np.sum(np.abs(hv))*AMP])
    dust = max(float(np.sum(np.abs(de))*AMP),float(np.sum(np.abs(dn))*AMP))
    velocity = float(np.max(np.sum(np.abs(rr[:,3:]),axis=0)))
    # Acceleration bound includes physical m weighting and each return filter.
    b_over_a0 = float(np.sum(cf*modes/(1+qq*qq)*np.abs(rr[:,2])))
    gap = q*q*(2+q*q)/(1+q*q)**2
    static_ratio = 2*b_over_a0*f1*f1/gap
    weak_stress_ratio = float(np.max(metric))/(gap+f1*f1*b_over_a0)
    return dict(a=a, linear=rr[0].tolist(), corrections=rr[1:].tolist(),
                metric_bound=float(np.max(metric)),dust_bound=dust,
                velocity_tilt_bound=velocity,b_over_a0_bound=b_over_a0,
                leading_spatial_Hessian_ratio=static_ratio,
                omitted_metric_power_counting_ratio=weak_stress_ratio)


def evolve(k,maximum,steps):
    mm = np.arange(1,maximum+1,2,dtype=float)
    y = np.zeros((len(mm)+1,4))
    _,h,r,p,_,_ = background(0.,k)
    y[0] = [-r/(p*p),0.,0.,r/(p*p)]
    dx = LENGTH/steps
    samples = []
    peaks = dict(metric_bound=0.,dust_bound=0.,velocity_tilt_bound=0.,
                 b_over_a0_bound=0.,leading_spatial_Hessian_ratio=0.,
                 omitted_metric_power_counting_ratio=0.)
    for i in range(steps+1):
        x = i*dx
        rr = inspect(x,y,k,mm)
        for key in peaks:
            peaks[key] = max(peaks[key],rr[key])
        if i % (steps//64) == 0:
            samples.append(rr)
        if i == steps:
            break
        v1 = rhs(x,y,k,mm)
        v2 = rhs(x+dx/2,y+dx*v1/2,k,mm)
        v3 = rhs(x+dx/2,y+dx*v2/2,k,mm)
        v4 = rhs(x+dx,y+dx*v3,k,mm)
        y += dx*(v1+2*v2+2*v3+v4)/6
        if not np.all(np.isfinite(y)):
            raise ArithmeticError(f'Nonfinite state at {k},mmax={maximum},steps={steps},i={i}')
    lin = np.array([s['linear'] for s in samples])
    cor = np.array([s['corrections'] for s in samples])
    lp = np.max(abs(lin),axis=0)
    cp = np.max(np.sum(abs(cor),axis=1),axis=0)
    ratio = cp/np.maximum(lp,1e-300)
    return dict(k_Mpc_inverse=k,maximum_odd_harmonic=maximum,steps=steps,
                peak_bounds=peaks,linear_peak=dict(zip(READOUTS,lp.tolist())),
                correction_peak=dict(zip(READOUTS,cp.tolist())),
                estimated_correction_fraction=dict(zip(READOUTS,ratio.tolist())),
                screens=dict(dust=bool(peaks['dust_bound']<.01),
                             metric=bool(peaks['metric_bound']<1e-4),
                             velocity_tilt=bool(peaks['velocity_tilt_bound']<1e-3),
                             constitutive_amplitude=bool(peaks['b_over_a0_bound']<1e-3),
                             correction=bool(np.max(ratio)<.01)),samples=samples)


def main():
    if OUTPUT.exists():
        raise SystemExit('Refusing to overwrite result')
    started = time.perf_counter()
    controls = []

    def check(name,error,tolerance):
        controls.append(dict(name=name,error=float(error),tolerance=tolerance,
                             passed=bool(math.isfinite(error) and error<=tolerance)))

    for x in (0.,.025,.05):
        for k in (.01,.1,1.):
            _,h,r,p,q,_ = background(x,k)
            for y in (np.array([.1,.3,-.2,.5]),np.array([-2.,1.,3.,-4.])):
                lhs=apply_matrix(y,h,r,p,q)
                rr=reference.matrix(h,r,p,q,reference.BETA)@y
                check(f'matrix:x={x}:k={k}:y={y[0]}',
                      float(np.max(abs(lhs-rr)/np.maximum(1.,abs(lhs)+abs(rr)))),2e-12)
    xx=2*math.pi*np.arange(32768)/32768
    ss=np.sin(xx)
    for m in range(1,64,2):
        numeric=2*float(np.mean(ss*abs(ss)*np.sin(m*xx)))
        exact=8/(math.pi*m*(4-m*m))
        check(f'odd_sine_coefficient:m={m}',abs(numeric/exact-1),2e-7)

    cases=[]
    for k in (.01,.1,1.):
        levels=[evolve(k,63,n) for n in LEVELS]
        fine,middle=levels[-1],levels[-2]
        ll=np.array([s['linear'] for s in fine['samples']])
        lm=np.array([s['linear'] for s in middle['samples']])
        cc=np.array([s['corrections'] for s in fine['samples']])
        cm=np.array([s['corrections'] for s in middle['samples']])
        for j,name in enumerate(READOUTS):
            check(f'linear_time:k={k}:{name}',
                  np.max(abs(ll[:,j]-lm[:,j]))/max(np.max(abs(ll[:,j])),1e-300),2e-5)
            check(f'correction_time:k={k}:{name}',
                  np.max(np.sum(abs(cc[:,:,j]-cm[:,:,j]),axis=1))
                  /max(fine['correction_peak'][name],1e-300),5e-3)
        # Independent forced modes share no nonlinear feedback. Truncating the
        # saved m63 solution exactly equals solving the same linear driven
        # system with m15/m31; do not duplicate those integrations.
        for mmax in (15,31):
            selected=cc[:,:((mmax+1)//2),:]
            for j,name in enumerate(READOUTS):
                peak=float(np.max(np.sum(abs(selected[:,:,j]),axis=1)))
                if mmax==31:
                    check(f'harmonic_tail:k={k}:{name}',
                          abs(fine['correction_peak'][name]-peak)
                          /max(fine['correction_peak'][name],1e-300),.02)
        cases.append(dict(k_Mpc_inverse=k,levels=levels))
    result=dict(status='QUALIFIED' if all(c['passed'] for c in controls) else 'FAILED',
                scope='Short linear transient plus first acceleration-constitutive correction only',
                inputs=dict(amplitude=AMP,initial_a=AI,log_a_interval=LENGTH,
                            beta=reference.BETA,ell_Mpc=reference.ELL_MPC,
                            omega_b=reference.OB,H_vac=reference.HVAC,
                            initial_state='ordinary comoving contrast, zero velocities and instantaneous clock Poisson source'),
                protocol_sha256=hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                reference_source_sha256=hashlib.sha256(Path(reference.__file__).read_bytes()).hexdigest(),
                controls=controls,cases=cases,elapsed_seconds=time.perf_counter()-started)
    encoded=json.dumps(result,indent=2,allow_nan=False)
    with OUTPUT.open('x') as handle:
        handle.write(encoded+'\n')
    print(json.dumps(dict(status=result['status'],controls=len(controls),
                         failed=[c for c in controls if not c['passed']],
                         summaries=[dict(k=c['k_Mpc_inverse'],
                            correction=c['levels'][-1]['estimated_correction_fraction'],
                            peaks=c['levels'][-1]['peak_bounds'],
                            screens=c['levels'][-1]['screens']) for c in cases],
                         elapsed_seconds=result['elapsed_seconds']),indent=2))


if __name__=='__main__':
    main()
