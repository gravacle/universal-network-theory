"""Pure definitions for the actual-background positive optical-depth map.
No initialization, physical import, calibration, state evolution or main.
The root-run control packet and successor both authenticate these exact bytes.
"""
import math
from functools import lru_cache
import numpy as np

CP=299792458.
MPC=3.0856775814913673e22
SIGMA_T=6.6524587321e-29
CAP=48.

@lru_cache(None)
def gauss(order):return np.polynomial.legendre.leggauss(order)

def background_rates(x,fixed,therm,k):
    """Vector form of the owned five-Newton background, not a new EOS.
    This bounded kernel is confined to the inherited fully-ionized fixture.
    Its scalar-equivalence controls precede any trajectory qualification.
    """
    x=np.asarray(x,float);a=np.exp(x)
    if np.any(1/a-1<=8000):raise ValueError('Actual-opacity fixture ends before the atomic-table join')
    eps,d0,OA,OB,OR,rG=(fixed[z] for z in ('eps','d0','OA','OB','OR','rG'))
    norm=1/eps-math.log1p(1/eps);d=d0/a**3;target=.5*eps*norm*d;s=np.array(target,copy=True)
    for _ in range(5):
        qbar=np.sqrt(1+eps*s/(1+s));dq=eps/(2*qbar*(1+s)**2)
        s-=(s*qbar-target)/(qbar+s*dq)
    qbar=np.sqrt(1+eps*s/(1+s));pex=(np.log1p(s)-s/(1+s))/norm
    h=np.sqrt((OB/a**3+OR/a**4+OA*(1+qbar*d-pex))/rG)
    hs=fixed['Hunit']*1000/MPC
    g=CP*SIGMA_T*therm.nH*therm.xfull/a**3/hs
    q=k*CP/(1000*fixed['Hunit']*a)
    tau_x=g/h;eta_x=q/(k*h);gamma_eta=g*k/q
    if not all(np.all(np.isfinite(v)) and np.all(v>0) for v in (tau_x,eta_x,gamma_eta)):
        raise ArithmeticError('Positive finite actual-background map')
    return tau_x,eta_x,gamma_eta

def integrals(lo,hi,fixed,therm,k,order=16):
    lo,hi=np.broadcast_arrays(np.asarray(lo,float),np.asarray(hi,float))
    if np.any(lo>hi):raise ValueError('Ordered source interval')
    u,w=gauss(order);half=(hi-lo)/2;mid=(hi+lo)/2
    tx,ex,_=background_rates(mid[...,None]+half[...,None]*u,fixed,therm,k)
    return half*np.sum(tx*w,axis=-1),half*np.sum(ex*w,axis=-1)

def backward_integrals(delta,hi,fixed,therm,k,order=16):
    """Preserve the small optical-layer span before subtracting large log a.
    delta, not the rounded difference of two log coordinates, is the Jacobian.
    """
    delta=np.asarray(delta,float)
    if np.any(delta<0):raise ValueError('Positive backward span')
    u,w=gauss(order);half=delta/2
    tx,ex,_=background_rates(float(hi)-half[...,None]*(1-u),fixed,therm,k)
    return half*np.sum(tx*w,axis=-1),half*np.sum(ex*w,axis=-1)

def inverse_depth(t,lo,hi,fixed,therm,k,order=16):
    """Safeguarded monotone inverse of integral_x^hi g/h dx.
    Every actual inversion residual is returned, rather than presuming success.
    """
    t=np.asarray(t,float);total,_=integrals(lo,hi,fixed,therm,k,order)
    if np.any(t<0) or np.any(t>total*(1+8*np.finfo(float).eps)):
        raise ValueError('Optical-depth inverse outside physical panel')
    lower=np.zeros_like(t);upper=np.full_like(t,float(hi-lo))
    rate_hi=float(background_rates(hi,fixed,therm,k)[0])
    delta=np.maximum(lower,np.minimum(upper,t/rate_hi))
    done=np.zeros(t.shape,dtype=bool)
    for _ in range(16):
        value,_=backward_integrals(delta,hi,fixed,therm,k,order);r=value-t
        reached=np.abs(r)<=4e-13*np.maximum(1.,t);done|=reached
        lower=np.where((r<0)&~done,delta,lower);upper=np.where((r>0)&~done,delta,upper)
        rate=background_rates(float(hi)-delta,fixed,therm,k)[0]
        proposed=delta-r/rate
        admissible=(proposed>lower)&(proposed<upper)&np.isfinite(proposed)
        proposed=np.where(admissible,proposed,(lower+upper)/2)
        delta=np.where(done,delta,proposed)
    value,_=backward_integrals(delta,hi,fixed,therm,k,order)
    error=float(np.max(abs(value-t)/np.maximum(1.,t))) if t.size else 0.
    return delta,error

def optical_geometry(lo,hi,eta_left,eta_right,fixed,therm,k,order=16,map_order=16):
    """Positive optical quadrature and ACTUAL conformal/source coordinates.
    collision_weight=e^-t dt; metric_weight=e^-t dt/Gamma_eta.
    No panel-mean opacity enters either collision or propagation measure.
    """
    depth,length=integrals(lo,hi,fixed,therm,k,map_order)
    check_depth,check_length=integrals(lo,hi,fixed,therm,k,32)
    depth=float(depth);length=float(length);width=float(eta_right-eta_left)
    if not (depth>0 and width>0):raise ValueError('Strict source panel')
    bound=min(depth,CAP);pieces=max(1,math.ceil(bound/8));u,w=gauss(order)
    ts=[];ws=[]
    for i in range(pieces):
        left=bound*i/pieces;right=bound*(i+1)/pieces
        ts.append((left+right)/2+(right-left)*u/2);ws.append((right-left)*w/2)
    t=np.concatenate(ts);dt=np.concatenate(ws)
    delta,inverse_error=inverse_depth(t,lo,hi,fixed,therm,k,map_order)
    _,back=backward_integrals(delta,hi,fixed,therm,k,map_order)
    _,check_back=backward_integrals(delta,hi,fixed,therm,k,32)
    x=float(hi)-delta
    gamma=background_rates(x,fixed,therm,k)[2];fraction=back/width
    # Gaussian nodes are interior; a finite source-coordinate defect is refused.
    if np.any(fraction<0) or np.any(fraction>1+2e-12):raise ArithmeticError('Actual conformal source coordinate outside panel')
    fraction=np.minimum(fraction,1.)
    cw=dt*np.exp(-t);mw=cw/gamma
    minimum_gamma=float(background_rates(hi,fixed,therm,k)[2])
    controls=dict(inverse_depth_error=inverse_error,
        optical_integral_error=abs(depth-float(check_depth))/max(depth,1e-30),
        conformal_integral_error=max(abs(length-float(check_length)),abs(length-width),float(np.max(abs(back-check_back))))/max(width,1e-30),
        optical_mass_error=abs(float(math.fsum(float(z) for z in cw))-(-math.expm1(-bound))),
        measure_identity_error=float(np.max(abs(mw*gamma-cw)))/max(float(np.max(abs(cw))),1e-300))
    return dict(depth=depth,width=width,t=t,eta_back=back,fraction=fraction,
        collision_weights=cw,metric_weights=mw,minimum_gamma=minimum_gamma,
        collision_tail=math.exp(-CAP) if depth>CAP else 0.,
        metric_tail=math.exp(-CAP)/minimum_gamma if depth>CAP else 0.,controls=controls)

def source_weights(geometry,phase_offset,k,bessel):
    """Both affine endpoint weights, for all actual l0..4/r0..2 sources."""
    x=phase_offset+k*geometry['eta_back'];fraction=geometry['fraction']
    metric=np.empty((5,3,2));collision=np.empty_like(metric)
    for l in range(5):
        for r in range(3):
            j=bessel(l,r,x)
            for p,factor in enumerate((np.ones_like(fraction),fraction)):
                metric[l,r,p]=math.fsum(float(z) for z in geometry['metric_weights']*factor*j)
                collision[l,r,p]=math.fsum(float(z) for z in geometry['collision_weights']*factor*j)
    return metric,collision

class OpticalKernel:
    """State-independent geometry cache; diagnostics survive checkpoint recovery."""
    def __init__(self,fixed,therm,k):
        self.fixed,self.therm,self.k=fixed,therm,k;self.cache={};self.check_cache={}
        self.maximum={name:0. for name in ('inverse_depth_error','optical_integral_error',
            'conformal_integral_error','optical_mass_error','measure_identity_error','source_quadrature_error')}
    def geometry(self,lo,hi,eta_left,eta_right):
        key=tuple(float(v) for v in (lo,hi,eta_left,eta_right))
        if key not in self.cache:
            result=optical_geometry(*key,self.fixed,self.therm,self.k)
            for name,value in result['controls'].items():self.maximum[name]=max(self.maximum[name],float(value))
            result['key']=key
            self.cache[key]=result
        return self.cache[key]
    def weights(self,geometry,phase_offset,bessel):
        # The independent 32/32 mapping and quadrature retains the SAME model.
        key=geometry['key']
        if key not in self.check_cache:
            self.check_cache[key]=optical_geometry(*key,self.fixed,self.therm,self.k,32,32)
        metric,collision=source_weights(geometry,phase_offset,self.k,bessel)
        cm,cc=source_weights(self.check_cache[key],phase_offset,self.k,bessel)
        mden=max(math.fsum(float(z) for z in geometry['metric_weights']),math.fsum(float(z) for z in self.check_cache[key]['metric_weights']),1e-300)
        cden=max(math.fsum(float(z) for z in geometry['collision_weights']),math.fsum(float(z) for z in self.check_cache[key]['collision_weights']),1e-300)
        error=max(float(np.max(abs(metric-cm)))/mden,float(np.max(abs(collision-cc)))/cden)
        self.maximum['source_quadrature_error']=max(self.maximum['source_quadrature_error'],error)
        for name,value in self.check_cache[key]['controls'].items():self.maximum[name]=max(self.maximum[name],float(value))
        return metric,collision
