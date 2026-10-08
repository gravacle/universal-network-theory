"""Independent spherical frozen-linear response for the existing source.

Same Plummer*(1-y^2/400)^4 support y<20 and Gaussian compensation width300.
No new amplitude fit; use the original mixed960 normalization. H-free,
weak-metric, infinitesimal constitutive approximation to the SAME K(X)
equations, not a substitute for the nonlinear galaxy trajectory.

Zero delta_m,p,Z is consistent initially only with delta(phi_dot)=Q Phi;
canonical cp/A includes boost/current terms and is NOT itself physical m.
Reconstruct m from saved canonical snapshots. Compare first nonzero time
only; report approximation indicators, not an invented physics pass gate.

Frozen numerical gates: Hankel source reconstruction1e-5 of peak source,
integration refinement1e-5 and doubled cutoff1e-4 of each profile maximum;
canonical inverse2e-12. No observation scored, no source evolution run.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_polar_source_v005 as source

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_FINITE_SOURCE_LINEAR_V001_RESULT.json'


def j0(x):
    return np.sinc(x/np.pi)


def j1(x):
    small=abs(x)<.01;safe=np.where(small,1.,x)
    regular=(np.sin(safe)/safe-np.cos(safe))/safe
    series=x*(1/3-x*x/30+x**4/840-x**6/45360)
    return np.where(small,series,regular)


def j0minus1(x):
    return np.where(abs(x)<.05,-x*x/6+x**4/120-x**6/5040+x**8/362880,j0(x)-1)


def gauss_segments(end,step,order):
    low=np.array([0.,.0001,.0003,.001,.003,.01,.03,.1])
    bounds=np.r_[low,np.linspace(.1,end,math.ceil((end-.1)/step)+1)[1:]]
    x,w=np.polynomial.legendre.leggauss(order)
    q=((bounds[:-1,None]+bounds[1:,None])/2+np.diff(bounds)[:,None]*x/2).ravel()
    weights=(np.diff(bounds)[:,None]*w/2).ravel()
    return q,weights


def predict(model,y,t,cutoff,order,source_order):
    xx,ww=np.polynomial.legendre.leggauss(source_order)
    yy=10*(xx+1);wy=10*ww
    shape=(1+yy*yy)**-2.5*(1-yy*yy/400)**4
    source_moment=float(np.dot(wy,yy*yy*shape))
    peak=2*model.kappa/(model.L**2*source_moment)
    q,wq=gauss_segments(cutoff,.5,order)
    F=np.empty(len(q));moment_weights=wy*yy*yy*shape
    for first in range(0,len(q),256):
        sl=slice(first,first+256);arg=q[sl,None]*yy
        regular=j0(arg)@moment_weights-source_moment*np.exp(-22500*q[sl]**2)
        low=j0minus1(arg)@moment_weights-source_moment*np.expm1(-22500*q[sl]**2)
        F[sl]=peak*np.where(q[sl]<.003,low,regular)
    Q,m=model.bg0[2:4];d=float(model.constitutive(model.bg0[1])[2])
    eta=model.C/model.KB;J=m*Q/2;M2=eta*Q*Q
    k=q/model.L;W=m*k*k/(Q*d);B=2*eta*k*k/d;big=M2+B+W-J
    root=np.hypot(big,2*math.sqrt(J*M2));l2=2*J*M2/(root+big);n2=big+l2
    den=l2+n2;bf=(W-J+l2)/den;af=1-bf
    cs=2*(np.sinh(np.sqrt(l2)*t/2)/np.sqrt(l2))**2
    cf=2*(np.sin(np.sqrt(n2)*t/2)/np.sqrt(n2))**2
    ss=np.sinh(np.sqrt(l2)*t)/np.sqrt(l2);sf=np.sin(np.sqrt(n2)*t)/np.sqrt(n2)
    S=af*cs+bf*cf;Y=B/den*(cs-cf);Ydot=B/den*(ss-sf)
    dm=((M2+l2)*cs+(n2-M2)*cf)/den
    profiles={key:np.zeros(len(y)) for key in ('S','delta_m','Z','p','gravity_excess','source')}
    infrared={key:np.zeros(len(y)) for key in profiles}
    ir_cut=100*model.bg0[5]*model.L
    for first in range(0,len(q),256):
        sl=slice(first,first+256);qq=q[sl];wwq=wq[sl];ff=F[sl]
        arg=qq[:,None]*y;zero=j0(arg);one=j1(arg)
        integrands={
            'S':m/np.pi*(qq*qq*ff*S[sl])[:,None]*zero,
            'delta_m':m/np.pi*(qq*qq*ff*dm[sl])[:,None]*zero,
            'Z':Q*m*model.L/np.pi*(qq*ff*Y[sl])[:,None]*one,
            'p':Q*m*model.L/(2*np.pi)*(qq*ff*(Y[sl]-Ydot[sl]/(eta*Q)))[:,None]*one,
            'gravity_excess':Q*m*model.L/(2*np.pi)*(qq*ff*S[sl])[:,None]*one,
            'source':2/np.pi*(qq*qq*ff)[:,None]*zero}
        for key,vals in integrands.items():
            profiles[key]+=wwq@vals
            infrared[key]+=(wwq*(qq<ir_cut))@abs(vals)
    profiles['peak']=peak
    profiles['infrared_absolute_integral_max']={key:float(np.max(v)) for key,v in infrared.items()}
    profiles['IR_excluded_domain']=f'k<100 H, q<{ir_cut}; bound is only within frozen kernel'
    return profiles


def reconstruct(model,snap):
    z=np.array(snap['state']);A=np.array(snap['A_inner'])
    sig=z[0]/A;c=np.sqrt(1+sig*sig);w=z[1]/A;target=z[3]/A
    s=target/(model.mpref*c)
    for _ in range(12):
        X,m,d,K,dm,qr=model.constitutive(s)
        q=np.sqrt(X*X+w*w);Q=c*q+sig*w;p=sig*q+c*w
        e=(z[2]-model.C*p)/model.KB
        rt=np.sqrt(p*p+model.bs**2);j=model.lam*abs(p)/rt
        jt=model.lam*abs(p)*(p*p+2*model.bs**2)/rt**3
        DD=model.C*(e-(1+j)*p)
        inv=(q/X)*(d-(m/X)*w*w/(q*q)-model.C*sig*sig*X*X/(q*q)*(2/model.KB+jt))
        residual=m*q/X+sig*DD-target
        error=float(np.max(abs(residual)/target))
        if error<1e-15:break
        s-=residual/(inv*model.Q0*model.eps/(2*qr*(1+s)**2))
    return dict(X=X,m=m,d=d,p=p,Z=z[2],sig=sig,w=w,Q=Q,q=q,s=s,qr=qr,error=error,
                cp=z[3],boost_current_contact=(c-1)*m+sig*DD)


def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic();saved=json.loads(source.prev.inherited.SOURCE.read_text())
    model=source.Polar(saved,32,.012)
    target=BASE/'INVARIANT_CLOCK_POLAR_SOURCE_BUFFER02D_RESULT.json'
    data=json.loads(target.read_text());snap=data['snapshots'][1]
    r=np.array(snap['r']);y=r/model.L;t=snap['t']
    runs=[predict(model,y,t,80.,16,1024),predict(model,y,t,80.,32,2048),
          predict(model,y,t,160.,32,4096)]
    controls=[]
    def check(name,error,gate):
        controls.append(dict(name=name,error=float(error),tolerance=gate,passed=bool(error<=gate)))
    truth=runs[-1]['peak']*((1+y*y)**-2.5*np.maximum(1-y*y/400,0)**4
          -(2*model.kappa/(model.L**2*runs[-1]['peak']))/(math.sqrt(math.pi)/4*300**3)*np.exp(-(y/300)**2))
    check('source_reconstruction',np.max(abs(runs[-1]['source']-truth))/runs[-1]['peak'],1e-5)
    for key in ('S','delta_m','Z','p','gravity_excess'):
        scale=max(float(np.max(abs(runs[-1][key]))),1e-30)
        check(key+'_quadrature',np.max(abs(runs[1][key]-runs[0][key]))/scale,1e-5)
        check(key+'_cutoff',np.max(abs(runs[2][key]-runs[1][key]))/scale,1e-4)
    comparisons=[];inputs=[target]
    for tag in ('MIXED04','BUFFER01C','BUFFER02D'):
        path=BASE/f'INVARIANT_CLOCK_POLAR_SOURCE_{tag}_RESULT.json';inputs.append(path)
        data=json.loads(path.read_text());sn=data['snapshots'][1];ini=data['snapshots'][0]
        now=reconstruct(model,sn);begin=reconstruct(model,ini)
        check(tag+'_snapshot_inverse',max(now['error'],begin['error']),2e-12)
        rr=np.array(sn['r']);ys=rr/model.L
        # Same short-time background and R^2 slice used in saved run. The
        # omitted exact polar correction was independently bounded elsewhere.
        xc=float(np.interp(sn['t'],model.tbg,model.xbg));H=model.bg(xc)[5]
        background=np.array([model.bg(float(xc-.5*H*H*ri*ri)) for ri in rr]).T
        sb,Xb,mbg,Hb=background[1],background[2],background[3],background[5]
        db=model.constitutive(sb)[2];qrb=background[7]
        # Snapshot times differ slightly with the inherited integrator grids.
        pred=(runs[-1] if abs(sn['t']-t)<1e-15 and np.array_equal(rr,r)
              else predict(model,ys,sn['t'],160.,32,4096))
        delta_s=now['s']-sb
        delta_qr=model.eps*delta_s/((1+now['s'])*(1+sb)*(now['qr']+qrb))
        delta_X=model.Q0*delta_qr
        material=model.mpref*(delta_s*now['qr']+sb*delta_qr)
        wb=-Xb*Hb*rr/np.sqrt(1-Hb*Hb*rr*rr)
        qb=Xb/np.sqrt(1-Hb*Hb*rr*rr)
        kinetic_difference=now['w']**2/(now['q']+now['X'])-wb**2/(qb+Xb)
        scales={key:max(float(np.max(abs(pred[key]))),1e-30) for key in ('delta_m','Z','p')}
        comparisons.append(dict(tag=tag,t_over_tdyn=sn['t_over_tdyn'],Ht=H*sn['t'],
            maximum_JY=sn['max_JY'],
            fractional_tilt_charge_sensitivity=float(np.max(now['d']*now['Q']*now['sig']**2/(2*now['m']))),
            tilt_sensitivity_scope='loose absolute scale only; exact tilt contacts can cancel, not a measured error',
            constitutive_tangent_fractional_change=float(np.max(abs(now['d']/db-1))),
            constitutive_linearization_error_over_material=float(np.max(abs(material-db*delta_X))/max(np.max(abs(material)),1e-30)),
            kinetic_clock_contact_over_material=float(np.max(abs(db*kinetic_difference))/max(np.max(abs(material)),1e-30)),
            kinetic_contact_scope='background-subtracted q-X contact, not the uncancelled equation error; q/lapse contact may cancel it',
            central_expansion_times_elapsed=abs(sn['central_expansion_estimate']*sn['t']),
            initial_material_range=[float(np.min(begin['m'])),float(np.max(begin['m']))],
            physical_material_contrast_range=[float(np.min(material)),float(np.max(material))],
            predicted_material_contrast_range=[float(np.min(pred['delta_m'])),float(np.max(pred['delta_m']))],
            maximum_boost_current_contact=float(np.max(abs(now['boost_current_contact']))),
            profile_mismatch=dict(delta_m=float(np.max(abs(material-pred['delta_m'])))/scales['delta_m'],
                                  Z=float(np.max(abs(now['Z']-pred['Z'])))/scales['Z'],
                                  p=float(np.max(abs(now['p']-pred['p'])))/scales['p'])))
    source_names=['invariant_clock_local_source_kernel_v001.py',
                  'invariant_clock_polar_source_v005.py','invariant_clock_polar_source_v003.py']
    inputs+= [Path(__file__),source.prev.inherited.SOURCE]+[BASE/n for n in source_names]
    result=dict(protocol=__doc__,elapsed_seconds=time.monotonic()-started,controls=controls,
        all_controls_passed=all(c['passed'] for c in controls),comparisons=comparisons,
        dimensionless_radius=y.tolist(),time_H0=t,
        prediction={k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in runs[-1].items()},
        input_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        scope='first frozen-linear source approximation; no full nonlinear acceptance')
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('prediction','dimensionless_radius','protocol')},allow_nan=False),flush=True)


if __name__=='__main__':main()
