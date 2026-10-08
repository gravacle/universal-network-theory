"""Early finite-opacity plasma transfer for the unchanged K(X) action.

Protocol frozen in NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md.
Not a CMB spectrum, native thermal history or observational score. Same
OR9e-5, action and charge as the accepted ideal-radiation benchmark.
Adopted Neff3.046, thermal neutrino ratio, Yp.245, complete ionization,
cold baryon stress and massless neutrinos, identically in the comparator.
No recombination, no photon creation and no fitted primordial amplitudes.
Full Thomson slip/intensity/polarization, not perfect tight coupling.

All higher intensity and polarization moments are divided by r^2. Exact
bulk/slip coordinates avoid cancellation of large photon/baryon drag.
Use L-stable two-stage Radau IIA; stage values, last stage is the endpoint.
Controls: 1e-4 state/time/start/hierarchy, 1e-6 Einstein constraint,
1e-10 analytic identities. Hierarchy gate covers gravity/fluids and moments
through l4; full retained hierarchy participates in time refinement.
No gate is a physical likelihood criterion. Writes exclusive receipts.
Ordinary scattering conventions: https://arxiv.org/html/astro-ph/9506072v1
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_radiation_v001 as prior

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_PLASMA_V001_RESULT.json'
NEFF=3.046
YHE=.245
RN=(7/8)*(4/11)**(4/3)*NEFF
FNU=RN/(1+RN)
AF=1e-4
SI=dict(c=299792458.,Mpc=3.0856775814913673e22,GN=6.67430e-11,
        mp=1.67262192369e-27,sigmaT=6.6524587321e-29,Gcos_over_GN=.98)


class Layout:
    def __init__(self,lg=6,ln=12):
        self.lg,self.ln=lg,ln
        self.names=['Psi','db','V','F','Uc','B','Zh','dg','slip','dn','Un']
        self.names += [f'fg{l}' for l in range(2,lg+1)]
        self.names += [f'fn{l}' for l in range(2,ln+1)]
        self.names += [f'pol{l}' for l in range(lg+1)]
        self.index={name:i for i,name in enumerate(self.names)}
        self.n=len(self.names);self.eye=np.eye(self.n)
        self.rows={name:self.eye[i] for name,i in self.index.items()}
    def get(self,name):
        return self.rows.get(name,np.zeros(self.n))


def background(model,x,K,dust=False,opacity_scale=1.):
    b=prior.background(model,x,dust=dust)
    b['rg']=b['rr']*(1-FNU);b['rn']=b['rr']*FNU
    b['Rb']=3*b['rb']/(4*b['rg'])
    b['r2']=(K/b['a'])**2/b['H2'];b['r']=math.sqrt(b['r2'])
    b['sr']=-1-b['hx']
    hsi=model.p['H0_km_s_Mpc']*1000/SI['Mpc']
    ne0=3*hsi*hsi*model.OB/(8*math.pi*SI['GN']*SI['Gcos_over_GN']*SI['mp'])*(1-YHE/2)
    b['g']=opacity_scale*ne0*SI['sigmaT']*SI['c']/(b['a']**3*hsi*b['H'])
    b['ne0']=ne0
    return b


def matrix(model,x,K,layout,dust=False,opacity_scale=1.):
    b=background(model,x,K,dust,opacity_scale)
    Q,m,W,rb,rg,rn,H,H2,hx,cs,r,r2,sr,g,Rb=(b[n] for n in
        ('Q','m','W','rb','rg','rn','H','H2','hx','cs','r','r2','sr','g','Rb'))
    eta=model.C/model.KB;e=layout.get;ix=layout.index
    psi,db,V,F,uc,B,Z,dg,slip,dn,un=(e(n) for n in layout.names[:11])
    wg=1/(1+Rb);wb=Rb*wg
    ug=V-wb*slip;ub=V+wg*slip
    lapse=psi-(rg*e('fg2')+rn*e('fn2'))/H2
    pressure=dg/4-r2*e('fg2')/2
    A=np.zeros((layout.n,layout.n))
    A[0]=-lapse+((rb+4*rg/3)*V+W*uc+4*rn*un/3)/(2*H2)
    A[1]=3*A[0]-r2*ub
    A[2]=(hx+wg)*V+lapse+wg*pressure
    coupling=2*eta*Q*r2/m
    A[3]=3*A[0]+eta*Q/H*Z-coupling*B-r2*uc
    A[4]=(hx+3*cs)*uc+cs*F+lapse
    A[5]=(hx-eta*Q/H)*B+cs*F+3*cs*uc+W/(model.KB*r2*H2)*Z
    A[6]=(3*cs+eta*Q/H)*Z-coupling*B
    A[7]=4*A[0]-4*r2*ug/3
    A[8]=(hx+wb-g*(1+1/Rb))*slip-V-pressure
    A[9]=4*A[0]-4*r2*un/3
    A[10]=(hx+1)*un+lapse+dn/4-r2*e('fn2')/2
    polar=e('fg2')+e('pol0')+e('pol2')
    A[ix['fg2']]=8*ug/15-3*r*e('fg3')/5-2*sr*e('fg2')-g*(e('fg2')-polar/10)
    A[ix['fn2']]=8*un/15-3*r*e('fn3')/5-2*sr*e('fn2')
    for kind,cutoff,drag in (('fg',layout.lg,g),('fn',layout.ln,0.)):
        for l in range(3,cutoff+1):
            A[ix[f'{kind}{l}']]=r*(l*e(f'{kind}{l-1}')-(l+1)*e(f'{kind}{l+1}'))/(2*l+1)-(2*sr+drag)*e(f'{kind}{l}')
    for l in range(layout.lg+1):
        A[ix[f'pol{l}']]=r*(l*e(f'pol{l-1}')-(l+1)*e(f'pol{l+1}'))/(2*l+1)-(g+2*sr)*e(f'pol{l}')
        if l in (0,2):A[ix[f'pol{l}']]+=g*polar/(2 if l==0 else 10)
    return A,b,lapse


def constraint(b,layout):
    e=layout.get;rb,rg,rn,W,h2,hx,cs=(b[n] for n in ('rb','rg','rn','W','H2','hx','cs'))
    terms=[2*b['r2']*e('Psi'),rb/h2*(e('db')+3*e('V')),
        W/h2*(e('F')-e('Zh')+3*e('Uc')),rg/h2*(e('dg')+4*e('V')),
        rn/h2*(e('dn')+4*e('Un'))]
    rates=[-2-2*hx,-3-2*hx,-3*(1+cs)-2*hx,-4-2*hx,-4-2*hx]
    return sum(terms),sum(t*q for t,q in zip(terms,rates))


def initial(model,K,ai,layout,dust=False):
    b=background(model,math.log(ai),K,dust)
    z=np.zeros(layout.n);ix=layout.index
    wt=(b['W']+b['rb']+4*b['rr']/3)/b['H2']
    V=2/wt;sn=4*V/(15*b['sr']);wg=1/(1+b['Rb']);wb=1-wg
    afac=32/(45*b['g']);sg=afac*V
    # Algebraic constraint, leading regular neutrino shear and leading
    # high-opacity photon quadrupole. Earlier-start test bounds this seed.
    for _ in range(5):
        psi=1+(b['rg']*sg+b['rn']*sn)/b['H2']
        contrast=-3*V-2*b['r2']*psi/wt
        denom=b['g']*(1+1/b['Rb'])-b['hx']-wb+b['r2']*afac*wb/2
        slip=(-V-contrast/3+b['r2']*afac*V/2)/denom
        sg=afac*(V-wb*slip)
    z[:11]=[psi,contrast,V,contrast,V,0.,0.,4*contrast/3,slip,4*contrast/3,V]
    z[ix['fg2']]=sg;z[ix['fn2']]=sn
    for l in range(3,layout.ln+1):
        z[ix[f'fn{l}']]=b['r']*z[ix[f'fn{l-1}']]/(2*l+1)
    for l in range(3,layout.lg+1):
        z[ix[f'fg{l}']]=b['r']*l*z[ix[f'fg{l-1}']]/((2*l+1)*b['g'])
    z[ix['pol0']]=1.25*sg;z[ix['pol2']]=.25*sg
    z[ix['pol1']]=b['r']*(z[ix['pol0']]-2*z[ix['pol2']])/(3*b['g'])
    for l in range(3,layout.lg+1):
        z[ix[f'pol{l}']]=b['r']*l*z[ix[f'pol{l-1}']]/((2*l+1)*b['g'])
    z*=prior.SEED/(psi+V)
    return z


def radau_step(y,x,h,fun):
    m1=fun(x+h/3);m2=fun(x+h);eye=np.eye(len(y))
    lhs=np.block([[eye-h*(5/12)*m1,h*m2/12],[-h*.75*m1,eye-h*.25*m2]])
    stages=np.linalg.solve(lhs,np.concatenate((y,y)))
    return stages[len(y):]


def integrate(model,K,steps,layout,ai=1e-7,dust=False):
    x0=math.log(ai);dx=math.log(AF/ai)/steps
    keep=[i for i,n in enumerate(layout.names) if not(dust and n in ('B','Zh'))]
    state=initial(model,K,ai,layout,dust);z=state[keep]
    snapshots=[];maxc=maxcap=maxspatial=0.
    def mat(x):return matrix(model,x,K,layout,dust)[0][np.ix_(keep,keep)]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//64)==0:
            state=np.zeros(layout.n);state[keep]=z
            _,b,ph=matrix(model,x,K,layout,dust);cr,_=constraint(b,layout)
            err=abs(cr@state)/max(float(abs(cr)@abs(state)),1e-30);maxc=max(maxc,err)
            if not dust:
                gap=model.Q0*model.eps/((1+b['s'])*(math.sqrt(1+model.eps)+b['qr']))
                low=model.Q0*model.eps*b['s']/((1+b['s'])*(b['qr']+1))
                maxcap=max(maxcap,abs(b['Q']*b['cs']*state[3])/min(gap,low))
                maxspatial=max(maxspatial,abs(b['r']*b['Q']*state[5])/model.bs)
            snapshots.append(dict(a=b['a'],state=state.tolist(),Phi=float(ph@state),constraint=err,
                                  H_over_Gamma=1/b['g'],kphysical_over_Gamma=b['r']/b['g']))
        if i==steps:break
        z=radau_step(z,x,dx,mat)
        if not np.all(np.isfinite(z)):raise FloatingPointError(f'nonfinite state step{i}')
    return dict(steps=steps,ai=ai,lg=layout.lg,ln=layout.ln,names=layout.names,dust=dust,
        snapshots=snapshots,maximum_constraint=maxc,linear_clock_margin_ratio=maxcap,
        linear_spatial_ratio=maxspatial)


def errors(left,right,names=None,endpoint=False):
    if names is None:names=[n for n in left['names'] if n in right['names'] and not(left['dust'] and n in ('B','Zh'))]
    ai=[left['names'].index(n) for n in names];bi=[right['names'].index(n) for n in names]
    a=np.array([r['state'] for r in left['snapshots']])[:,ai]
    b=np.array([r['state'] for r in right['snapshots']])[:,bi]
    scale=np.maximum(np.max(abs(b),axis=0),1e-30)
    delta=abs(a[-1]-b[-1]) if endpoint else np.max(abs(a-b),axis=0)
    vals=delta/scale;i=int(np.argmax(vals))
    return dict(error=float(vals[i]),limiting_state=names[i],per_state=dict(zip(names,map(float,vals))))


def main():
    start=time.monotonic();saved=json.loads(prior.old.base.SOURCE.read_text())
    saved['inherited']['Q0_over_H0']=100.;model=prior.old.base.Model(saved,1)
    controls=[];rows=[];layout=Layout();larger=Layout(8,16)
    def check(name,val,gate):
        controls.append(dict(name=name,error=float(val),tolerance=gate,passed=bool(val<=gate)))
    # Verify convergence on a non-autonomous smooth problem, and the
    # exact scalar Radau stability function for a very stiff decay.
    err=[]
    for n in (32,64):
        z=np.array([1.]);h=1/n
        for i in range(n):z=radau_step(z,i*h,h,lambda x:np.array([[-1-x]]))
        err.append(abs(float(z[0])-math.exp(-1.5)))
    check('radau_order_three',abs(err[0]/err[1]/8-1),.05)
    lam=-1e9;got=radau_step(np.array([1.]),0.,1.,lambda x:np.array([[lam]]))[0]
    exact=(1+lam/3)/(1-2*lam/3+lam*lam/6)
    check('radau_stiff_decay',abs(got-exact)/abs(exact),1e-10)
    collision=np.array([[-.9,.1,.1],[.5,-.5,.5],[.1,.1,-.9]])
    spectrum=np.sort(np.linalg.eigvals(collision).real)
    check('polarization_collision_spectrum',np.max(abs(spectrum-np.array([-1.,-1.,-.3]))),1e-10)
    common=[n for n in layout.names if n in layout.names[:11] or (n.startswith(('fg','fn')) and int(n[2:])<=4) or (n.startswith('pol') and int(n[3:])<=4)]
    for kval in (.01,.1):
        K=kval*299792.458/model.p['H0_km_s_Mpc']
        for a in (1e-7,1e-5,1e-4):
            A,b,_=matrix(model,math.log(a),K,layout);cr,crx=constraint(b,layout)
            residual=crx+cr@A+(3+2*b['hx'])*cr
            scale=np.maximum(abs(crx)+abs(cr)@abs(A)+abs((3+2*b['hx'])*cr),1e-30)
            check(f'constraint_identity_{kval}_{a}',np.max(abs(residual)/scale),1e-10)
            e=layout.get;wg=1/(1+b['Rb']);wb=1-wg
            # Independently reconstruct the original separate velocity rows.
            ub=e('V')+wg*e('slip');ug=e('V')-wb*e('slip')
            ph=e('Psi')-(b['rg']*e('fg2')+b['rn']*e('fn2'))/b['H2']
            ub_rhs=b['hx']*ub+ph+b['g']/b['Rb']*(ug-ub)
            ug_rhs=(b['hx']+1)*ug+ph+e('dg')/4-b['r2']*e('fg2')/2+b['g']*(ub-ug)
            defect=np.array([A[2]+wg*A[8]-wb*wg*e('slip')-ub_rhs,
                             A[2]-wb*A[8]-wb*wg*e('slip')-ug_rhs])
            check(f'bulk_slip_identity_{kval}_{a}',np.max(abs(defect))/max(np.max(abs(ub_rhs)),np.max(abs(ug_rhs))),1e-10)
        hist=[integrate(model,K,n,layout) for n in (512,1024,2048)]
        te=errors(hist[1],hist[2]);check(f'time_refinement_{kval}',te['error'],1e-4)
        check(f'constraint_trajectory_{kval}',hist[-1]['maximum_constraint'],1e-6)
        half=integrate(model,K,2048,layout,ai=5e-8)
        ie=errors(hist[-1],half,endpoint=True);check(f'initial_time_{kval}',ie['error'],1e-4)
        high=integrate(model,K,2048,larger)
        he=errors(hist[-1],high,common);check(f'hierarchy_{kval}',he['error'],1e-4)
        refs=[integrate(model,K,n,layout,dust=True) for n in (1024,2048)]
        re=errors(refs[0],refs[1]);check(f'reference_time_{kval}',re['error'],1e-4)
        refhalf=integrate(model,K,2048,layout,ai=5e-8,dust=True)
        rie=errors(refs[-1],refhalf,endpoint=True);check(f'reference_initial_time_{kval}',rie['error'],1e-4)
        refhigh=integrate(model,K,2048,larger,dust=True)
        rhe=errors(refs[-1],refhigh,[n for n in common if n not in ('B','Zh')])
        check(f'reference_hierarchy_{kval}',rhe['error'],1e-4)
        check(f'reference_constraint_{kval}',refs[-1]['maximum_constraint'],1e-6)
        end=np.array(hist[-1]['snapshots'][-1]['state']);ref=np.array(refs[-1]['snapshots'][-1]['state'])
        cmp=dict(Psi_ratio=float(end[0]/ref[0]),Phi_ratio=hist[-1]['snapshots'][-1]['Phi']/refs[-1]['snapshots'][-1]['Phi'],
                 baryon_density_ratio=float(end[1]/ref[1]),photon_density_ratio=float(end[7]/ref[7]),
                 clock_density_ratio=float((end[3]-end[6])/ref[3]))
        rows.append(dict(k_Mpc_inverse=kval,histories=hist,half_start=half,high_hierarchy=high,
            references=refs,reference_half=refhalf,reference_high=refhigh,
            coarse_error=errors(hist[0],hist[1]),fine_error=te,initial_error=ie,hierarchy_error=he,
            reference_error=re,reference_initial_error=rie,reference_hierarchy_error=rhe,comparison=cmp))
        print(json.dumps(dict(k=kval,time=te['error'],initial=ie['error'],hierarchy=he['error'],comparison=cmp)),flush=True)
    result=dict(protocol=__doc__,fixed=model.p,radiation_omega=prior.OR,neutrino_fraction=FNU,
        Neff=NEFF,helium_fraction=YHE,SI=SI,controls=controls,rows=rows,
        all_controls_passed=all(c['passed'] for c in controls),elapsed_seconds=time.monotonic()-start,
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (Path(__file__),Path(prior.__file__),Path(prior.old.__file__),Path(prior.old.base.__file__),prior.old.base.SOURCE)})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','fixed','protocol')}),flush=True)


if __name__=='__main__':main()
