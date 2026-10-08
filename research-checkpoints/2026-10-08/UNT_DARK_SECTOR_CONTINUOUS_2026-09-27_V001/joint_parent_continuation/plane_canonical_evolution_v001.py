"""Fixed nonlinear continuation, not a fitted galaxy or observational score.

Protocol frozen before execution: use the last row of the completed exact
CMC initial-data result, same a_i=.01, k=.01/Mpc, seed=1e-5, rG=.98 action.
Periodic plane, geodesic lapse N=1 and shift zero. Ordinary dust is initially
at rest: its proper time remains spatially uniform in this gauge, pi_T is
constant, until shell crossing. Evolve both metric scales/momenta, vector
coordinate/momentum, and phase/complete charge. No imposed later CMC,
isotropy, clipped Q, charge reset, thermal forcing or amplitude reduction.

Eight variables are background-subtracted or normalized canonical fields.
Use the auxiliary constitutive s>0 and stable Q-Qbar, not subtraction from
the clock cap. Evolution parameter x=ln(background a), endpoints .01 to1.
Pseudospectral periodic derivatives, RK4; three serial runs (32,2048),
(32,4096),(64,4096) nodes/steps. 65 checkpoints plus branch checks every
RHS. No filter, post-step constraint projection or dissipative repair.

Prospective numerical gates: local inverse relative residual<=2e-12,
Legendre Schur complement positive, coordinates finite; homogeneous RHS
<=2e-12; initial exact shear identity<=1e-6 relative; temporal/spatial
refinement<=1e-4 using max finest amplitude or declared scale 1e-8 per
normalized variable; sampled Hamiltonian/(6Vh²)<=1e-9 and perturbation-
normalized Hamiltonian<=1e-4, sampled momentum normalized to its terms or
initial geometric scale<=1e-4; mean charge drift<=2e-12. Positive volume,
rest mass, slice charge and branch are separately reported. A stopped run
or failed gate is retained, not a physical exclusion. Serialized results
include sampled states and protocol/input hashes; exclusive output.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np

BASE=Path(__file__).resolve().parent
SOURCE=BASE/'PLANE_CMC_INITIAL_DATA_V002_RESULT.json'
OUT=BASE/'PLANE_CANONICAL_EVOLUTION_V001_RESULT.json'


class Model:
    def __init__(self,saved,N):
        self.saved=saved; self.p=saved['inherited']; self.N=N
        self.y=2*np.pi*np.arange(N)/N
        self.modes=np.fft.fftfreq(N,1/N); self.modes[N//2]=0
        self.K=saved['fixed']['K']; self.eps=self.p['eps']
        self.D=1/self.eps-math.log1p(1/self.eps)
        self.KB=self.p['KB']; self.C=2-self.KB
        self.OA=self.p['omega_A']; self.OB=self.p['omega_b_cos']
        self.Q0=self.p['Q0_over_H0']; self.lam=self.p['lambda_s']
        H0=self.p['H0_km_s_Mpc']*1000/3.085677581491367e22
        self.bs=(1+self.lam)*self.p['a0']/(299792458*H0)
        self.mpref=6*self.OA/(self.Q0*self.eps*self.D)
        self.pcbar=6*self.OA*self.p['d0']/self.Q0
        self.max_inverse=0.; self.min_schur_fraction=1.
        row=saved['rows'][-1]; coeff=np.array(row['coefficients'])
        scale=saved['fixed']['linear_psi_amplitude']
        f=coeff@np.cos(np.arange(1,len(coeff)+1)[:,None]*self.y)
        norm=np.log1p(np.mean(np.expm1(6*scale*f)))/6
        self.lp=scale*f-norm
        Zm=row['Z_minus_one']
        self.dust_weight=np.exp(6*self.lp)*(1+saved['fixed']['seed']*np.cos(self.y))/(1+Zm)
        self.piT=6*self.OB*self.dust_weight

    def dx(self,f):
        return np.fft.ifft(1j*self.K*self.modes*np.fft.fft(f)).real

    def constitutive(self,s):
        q=np.sqrt(1+self.eps*s/(1+s)); Q=self.Q0*q
        dqds=self.eps/(2*q*(1+s)**2)
        m=self.mpref*q*s
        dm=self.mpref*(q+s*dqds)
        d=dm/(self.Q0*dqds)
        pp=(np.log1p(s)-s/(1+s))/self.D
        Kfun=3*self.OA*(-1+pp)
        return Q,m,d,Kfun,dm,q

    def bg(self,x):
        a=math.exp(x); charge=self.p['d0']/a**3
        target=3*self.OA*charge/self.Q0
        s=target/(self.mpref*math.sqrt(1+self.eps))
        for _ in range(3):
            Q,m,d,Kfun,dm,q=self.constitutive(s);s-=(m-target)/dm
        Q,m,d,Kfun,dm,q=self.constitutive(s)
        h2=(Q*m-Kfun)/3+self.OB/a**3
        h=math.sqrt(h2); hx_over_h=-(Q*m+3*self.OB/a**3)/(2*h2)
        return a,s,Q,m,Kfun,h,hx_over_h,q

    def initial(self,homogeneous=False):
        z=np.zeros((8,self.N)); a,s,Q,m,Kfun,h,hx,q=self.bg(math.log(.01))
        if homogeneous:return z
        z[0]=z[1]=2*self.lp
        ratio=math.sqrt(self.saved['rows'][-1]['h_squared']/self.saved['fixed']['background_h_squared'])
        ratio_minus=self.saved['rows'][-1]['h_squared_correction']/self.saved['fixed']['background_h_squared']/(ratio+1)
        z[4]=z[5]=np.expm1(6*self.lp)*ratio+ratio_minus
        z[7]=np.expm1(6*self.lp)
        return z

    def unpack(self,x,z):
        if not np.all(np.isfinite(z)):raise ValueError('nonfinite evolved state')
        abar,sbar,Qbar,mbar,Kbar,h,hx,qbar=self.bg(x)
        fa,fb,un,phase,pa,pb,pu,pc=z
        ev=np.exp(fa+2*fb); A=abar*np.exp(fa); B=abar*np.exp(fb);V=abar**3*ev
        pia=-4*abar**3*h*(1+pa);pib=-8*abar**3*h*(1+pb)
        piu=2*abar**2*pu;piph=self.pcbar*(1+pc)
        sig=un*np.exp(-fa);c=np.sqrt(1+sig*sig)
        w=self.dx(phase)/A;Z=pu*np.exp(-2*fb)
        target=piph/(2*V)
        if np.any(target<=0):raise ValueError('nonpositive slice charge')
        s=target/(c*self.mpref*math.sqrt(1+self.eps))
        for inverse_iteration in range(8):
            if np.any(s<=0) or not np.all(np.isfinite(s)):
                raise ValueError('constitutive branch left during local inverse')
            Q,m,d,Kfun,dm,qroot=self.constitutive(s)
            p=(sig*Q+w)/c;e=(Z-self.C*p)/self.KB
            root=np.sqrt(p*p+self.bs*self.bs)
            j=self.lam*abs(p)/root
            jt=self.lam*abs(p)*(p*p+2*self.bs*self.bs)/root**3
            Dp=self.C*(e-(1+j)*p)
            schur=c*c*d-self.C*sig*sig*(2/self.KB+jt)
            if np.any(schur<=0):raise ValueError('nonpositive local Legendre Schur complement')
            resid=c*m+sig*Dp-target
            # Accept/reject one consistent iterate, including on iteration cap.
            if np.max(abs(resid)/target)<=4e-16 or inverse_iteration==7:break
            s-=resid/((schur/c)*(self.Q0*self.eps/(2*qroot*(1+s)**2)))
        err=float(np.max(abs(resid)/target));self.max_inverse=max(self.max_inverse,err)
        self.min_schur_fraction=min(self.min_schur_fraction,float(np.min(schur/(c*c*d))))
        if err>2e-12:raise ValueError('local inverse residual failed')
        # J=2 lambda b² integral_0^z t²/sqrt(1+t²) dt; series avoids tiny cancellation.
        zz=abs(p)/self.bs
        J=self.lam*self.bs**2*(zz*np.sqrt(1+zz*zz)-np.arcsinh(zz))
        small=zz<.01
        J[small]=self.lam*self.bs**2*(2*zz[small]**3/3-zz[small]**5/5+3*zz[small]**7/28-5*zz[small]**9/72)
        q=(Q-sig*w)/c
        qdiff=(self.Q0*self.eps*(s-sbar)/((1+s)*(1+sbar)*(qroot+qbar))-sig*w-Qbar*sig*sig/(c+1))/c
        ax=self.dx(fa);bx=self.dx(fb);piux=self.dx(piu)
        Lx=self.KB*e*e+2*self.C*e*p-self.C*p*p-self.C*J+2*Kfun
        S=Dp*Q+m*p;cur=sig*m+c*Dp
        kin=pia*(pia-2*pib)/(8*V)
        return locals()

    def rhs(self,x,z):
        g=self.unpack(x,z)
        a=g['abar']; h=g['h'];hx=g['hx'];V=g['V'];A=g['A'];B=g['B']
        sig=g['sig'];c=g['c'];piux=g['piux'];S=g['S'];cur=g['cur']
        pa=z[4];pb=z[5];fg=B*B/A;bx=g['bx']
        rA=g['kin']-2*fg*bx*bx+V*g['Lx']-2*V*g['Z']*g['e']-2*V*(sig*S/c+g['w']*cur)+sig*sig*piux/c
        rB=2*g['kin']+4*fg*bx*bx-4*self.dx(fg*bx)+2*V*g['Lx']
        rU=2*B*B*S/c-sig*piux/(A*c)
        rP=-2*self.dx(B*B*cur)
        v=z[0]+2*z[1];inv=np.exp(-v)
        out=np.empty_like(z)
        out[0]=np.expm1(-v)+inv*(2*pb-pa)
        out[1]=np.expm1(-v)+inv*pa
        cx=sig*self.dx(sig)/c
        out[2]=(A*g['e']-cx)/(a*h)-z[2]
        out[3]=g['qdiff']/h
        out[4]=rA/(-4*a**3*h*h)-(1+pa)*(3+hx)
        out[5]=rB/(-8*a**3*h*h)-(1+pb)*(3+hx)
        out[6]=rU/(2*a*a*h)-2*z[6]
        out[7]=rP/(self.pcbar*h)
        return out

    def diagnostics(self,x,z):
        g=self.unpack(x,z);A=g['A'];B=g['B'];V=g['V'];h=g['h']
        R3=-(4*self.dx(g['bx'])+6*g['bx']**2-4*g['ax']*g['bx'])/A**2
        HH=g['kin']-V*R3+V*(self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']-2*g['Kfun'])+g['piph']*g['q']+g['c']*g['piux']+self.piT
        terms=np.array([g['pia']*g['ax'],g['pib']*g['bx'],-self.dx(g['pia']),-g['abar']*z[2]*g['piux'],g['piph']*self.dx(z[3])])
        DD=np.sum(terms,axis=0)
        db=self.dust_weight*np.exp(-z[0]-2*z[1])-1
        amp=max(self.saved['fixed']['seed'],float(np.max(abs(db))))
        dscale=max(float(np.max(abs(terms))),4*g['abar']**3*h*self.K*self.saved['fixed']['linear_psi_amplitude'])
        # First-order dictionary only: not a nonlinear Newtonian gauge transform.
        shear=h*np.exp(-z[0]-2*z[1])*2*(z[5]-z[4])
        vb_linear=g['abar']**2*shear/self.K**2
        phi_linear=-z[1]-h*vb_linear
        cosine=np.cos(self.y)
        return dict(a=g['abar'],Hamiltonian_background_normalized=float(np.max(abs(HH)/(6*V*h*h))),
            Hamiltonian_perturbation_normalized=float(np.max(abs(HH)/(6*V*h*h)))/amp,
            momentum_normalized=float(np.max(abs(DD)))/dscale,
            mean_charge_change=float(np.mean(z[7])-np.mean(self.initial()[7])),
            min_aux_s=float(np.min(g['s'])),max_aux_s=float(np.max(g['s'])),
            min_volume=float(np.min(V)),max_abs_density_contrast=float(np.max(abs(db))),
            max_abs_vector_tilt=float(np.max(abs(g['sig']))),
            max_spatial_interpolation_derivative=float(np.max(g['j'])),
            max_spatial_phase_gradient_over_bs=float(np.max(abs(g['p'])))/self.bs,
            density_cosine=float(2*np.mean(db*cosine)),
            first_order_dictionary_Newtonian_density_cosine=float(2*np.mean((db-3*h*vb_linear)*cosine)),
            first_order_dictionary_potential_cosine=float(2*np.mean(phi_linear*cosine)),
            first_order_dictionary_velocity_cosine=float(2*np.mean(vb_linear*cosine)),
            state=z.tolist())


def integrate(saved,N,steps):
    model=Model(saved,N);x0=math.log(.01);dx=-x0/steps;z=model.initial()
    snapshots=[];failure=None;beg=time.monotonic()
    homogeneous=float(np.max(abs(model.rhs(x0,model.initial(True)))))
    g=model.unpack(x0,z);rhs=model.rhs(x0,z)
    shear_dot=2*g['h']**2*(rhs[5]-rhs[4])/g['ev']
    target=model.dx(g['bx']/g['A'])/g['A']
    shear_error=float(np.max(abs(shear_dot-target)))/max(float(np.max(abs(target))),1e-300)
    last_step=0
    try:
        for i in range(steps+1):
            x=x0+i*dx;last_step=i
            if i%(steps//64)==0:snapshots.append(model.diagnostics(x,z))
            if i==steps:break
            r1=model.rhs(x,z);r2=model.rhs(x+dx/2,z+dx*r1/2)
            r3=model.rhs(x+dx/2,z+dx*r2/2);r4=model.rhs(x+dx,z+dx*r3)
            z+=dx*(r1+2*r2+2*r3+r4)/6
    except (ValueError,FloatingPointError,OverflowError) as e:
        failure=f'{type(e).__name__}: {e}'
    summary=dict(nodes=N,steps=steps,completed=last_step==steps and failure is None,
        failure=failure,last_step=last_step,last_attempted_a=math.exp(x0+last_step*dx),
        homogeneous_rhs_error=homogeneous,initial_shear_relative_error=shear_error,
        maximum_inverse_error=model.max_inverse,minimum_schur_fraction=model.min_schur_fraction,
        elapsed_seconds=time.monotonic()-beg,snapshots=snapshots)
    print(json.dumps({k:v for k,v in summary.items() if k!='snapshots'}),flush=True)
    return summary


def refinement(a,b):
    if not a['completed'] or not b['completed']:return None
    za=np.array([r['state'] for r in a['snapshots']]);zb=np.array([r['state'] for r in b['snapshots']])
    if b['nodes']==2*a['nodes']:zb=zb[:,:,::2]
    scale=np.maximum(np.max(abs(zb),axis=(0,2)),1e-8)
    return dict(per_variable=(np.max(abs(za-zb),axis=(0,2))/scale).tolist(),
                maximum=float(np.max(np.max(abs(za-zb),axis=(0,2))/scale)))


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    saved=json.loads(SOURCE.read_text());rows=[];started=time.monotonic()
    for N,steps in ((32,2048),(32,4096),(64,4096)):
        rows.append(integrate(saved,N,steps))
    rt=refinement(rows[0],rows[1]);rs=refinement(rows[1],rows[2])
    checks=dict(all_completed=all(r['completed'] for r in rows),
        homogeneous=max(r['homogeneous_rhs_error'] for r in rows)<=2e-12,
        initial_shear=max(r['initial_shear_relative_error'] for r in rows)<=1e-6,
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        time_refinement=rt is not None and rt['maximum']<=1e-4,
        space_refinement=rs is not None and rs['maximum']<=1e-4)
    samples=[s for r in rows for s in r['snapshots']]
    checks.update(Hamiltonian_background=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        Hamiltonian_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in samples)<=1e-4,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-4,
        conserved_charge=max(abs(s['mean_charge_change']) for s in samples)<=2e-12)
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        input_sha256={SOURCE.name:hashlib.sha256(SOURCE.read_bytes()).hexdigest()},
        inherited=saved['inherited'],rows=rows,time_refinement=rt,space_refinement=rs,
        controls=checks,all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-started,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol','inherited')},indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
