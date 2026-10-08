"""Exact homogeneous tilted Bianchi-I saturation diagnostic, SAME action.

Distinct declared physical preparation, not a repair/replacement of the
failed plane IVP or a galaxy simulation. Question: does the full nonlinear
constitutive action arrest the identified growing physical vector tilt?
No spatial grid/aliasing, no mode filter, no phase frozen after evolution.
Initialize a=.01,A=B=a, same conserved pi_T=6Omega_b and pi_phi=pcbar,
phi homogeneous, sigma=1e-12. Set Z=KB H(p_plus+1)sigma from the cold
growing direction; this is an ADOPTED perturbation, not a formation law.
Solve the nonlinear charge inverse and H_i²=E/(6V), initial k=l=H_i.
No independent mass, radiation, expansion or gravitational-coupling fit.

Evolve both metric scales, mean pi_a, u,phase,pi_u,pi_phi under original
Hamilton flow. Reconstruct pi_b from H=0 (pi_a never fixed). Homogeneity
makes D=0; it does not impose later isotropy. Verify reconstructed pi_b's
derivative against original RHS. Original thresholds: time refinement1e-4,
Hamilton/background1e-9, inverse2e-12, charge2e-12, tangent1e-4 with1e-8
floor at step1e-3 and5e-4; homogeneous RHS2e-12. Frozen three serial
RK4 runs4096/8192/16384, a=.01 to1,65 checkpoints. No spatial gate needed
for an exactly homogeneous solution; no claimed acceptance of plane data.
Report tilt, proper-volume expansion, shear, JY and domain/Schur margins.
Stop/report a constitutive/chart/finite failure or |fa|,|fb|>20 or |sigma|>100
as an unresolved large-deformation event, NOT a universal physical exclusion.
"""
from pathlib import Path
import hashlib
import json
import math
import resource
import time
import numpy as np
import plane_canonical_evolution_v001 as base
import plane_canonical_evolution_v002 as stable

BASE=Path(__file__).resolve().parent
OUT=BASE/'HOMOGENEOUS_TILT_SATURATION_V001_RESULT.json'


class Model(stable.Model):
    def __init__(self,saved):
        super().__init__(saved,1)
        self.dust_weight=np.ones(1);self.piT=np.full(1,6*self.OB)
        self.seed=1e-12
        fc=self.p['omega_clock_excess']/(self.p['omega_clock_excess']+self.OB)
        self.power=-.75+.5*math.sqrt(.25+12*fc/self.KB)

    def energy_excess(self,x,z):
        g=self.unpack(x,z);a=g['abar'];h=g['h'];ev=g['ev'];v=z[0]+2*z[1]
        ds=g['s']-g['sbar']
        dK=3*self.OA/self.D*(np.log1p(ds/(1+g['sbar']))-ds/((1+g['s'])*(1+g['sbar'])))
        vec=self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']
        ed=ev*vec/(6*h*h)-(g['Kbar']*np.expm1(v)+ev*dK)/(3*h*h)
        ed+=self.pcbar*(g['Qbar']*z[7]+(1+z[7])*g['qdiff'])/(6*a**3*h*h)
        return ed,g

    def initial(self,homogeneous=False):
        z=np.zeros((8,1))
        if homogeneous:return z
        x=math.log(.01);h=self.bg(x)[5]
        z[2]=self.seed;z[6]=self.KB*h*(self.power+1)*self.seed
        ed,g=self.energy_excess(x,z)
        if np.any(1+ed<=0):raise ValueError('initial energy not positive')
        z[4]=ed/(np.sqrt(1+ed)+1) # exact isotropic H_i/Hbg-1
        return z

    def reconstruct(self,x,z):
        if np.max(abs(z[:2]))>20:raise ValueError('declared large metric deformation event')
        ed,g=self.energy_excess(x,z);pa=z[4];v=z[0]+2*z[1]
        if np.any(1+pa<=0):raise ValueError('pi_a chart crossed zero')
        if np.max(abs(g['sig']))>100:raise ValueError('declared large tilt event')
        full=z.copy();full[5]=pa/4+.75*(np.expm1(v)+g['ev']*ed-pa)/(1+pa)
        return full

    def rhs(self,x,z):
        out=stable.Model.rhs(self,x,self.reconstruct(x,z));out[5]=0.
        return out

    def diagnostics(self,x,z):
        full=self.reconstruct(x,z);out=stable.Model.diagnostics(self,x,full)
        g=self.unpack(x,full);flow=self.rhs(x,z)
        ha=np.exp(-full[0]-2*full[1])*(1+2*full[5]-full[4])
        hb=np.exp(-full[0]-2*full[1])*(1+full[4]);mean=(ha+2*hb)/3
        sigprime=np.exp(-full[0])*(flow[2]-full[2]*flow[0])
        out.update(physical_tilt=float(g['sig'][0]),tilt_derivative_per_ln_a=float(sigprime[0]),
            mean_expansion_over_reference=float(mean[0]),shear_over_reference=float((ha-hb)[0]),
            JY=float(g['j'][0]),Q_over_Q0=float(g['Q'][0]/self.Q0),
            physical_volume_over_reference=float(g['ev'][0]),
            phase_charge_contrast_proper=float((np.exp(-full[0]-2*full[1])*(1+full[7])-1)[0]))
        return out

    def tangent(self,x,z):
        flow=self.rhs(x,z);original=stable.Model.rhs(self,x,self.reconstruct(x,z))[5]
        errors=[]
        for step in (1e-3,5e-4):
            v=[self.reconstruct(x+j*step,z+j*step*flow)[5] for j in (-2,-1,1,2)]
            dd=(v[0]-8*v[1]+8*v[2]-v[3])/(12*step)
            errors.append(float(np.max(abs(dd-original)))/max(float(np.max(abs(original))),1e-8))
        return dict(a=math.exp(x),relative_defect_by_step=errors,passed=max(errors)<=1e-4)


def integrate(saved,steps):
    m=Model(saved);x0=math.log(.01);dx=-x0/steps;z=m.initial();beg=time.monotonic()
    pre=float(np.max(abs(m.rhs(x0,m.initial(True)))));snap=[];tan=[];failure=None;i=0
    cp=BASE/f'HOMOGENEOUS_TILT_SATURATION_V001_S{steps}_CHECKPOINT.json'
    with cp.open('x') as f:json.dump(dict(status='starting',steps=steps),f)
    try:
        for i in range(steps+1):
            x=x0+i*dx
            if i%(steps//64)==0:
                snap.append(m.diagnostics(x,z))
                with cp.open('w') as f:json.dump(dict(step=i,state_reduced=z.tolist(),diagnostics=snap[-1]),f,allow_nan=False)
            if i%(steps//4)==0:tan.append(m.tangent(x,z))
            if i==steps:break
            r1=m.rhs(x,z);r2=m.rhs(x+dx/2,z+dx*r1/2)
            r3=m.rhs(x+dx/2,z+dx*r2/2);r4=m.rhs(x+dx,z+dx*r3)
            z+=dx*(r1+2*r2+2*r3+r4)/6
    except (ValueError,FloatingPointError,OverflowError) as e:failure=f'{type(e).__name__}: {e}'
    row=dict(nodes=1,steps=steps,completed=i==steps and failure is None,failure=failure,
        last_step=i,last_attempted_a=math.exp(x0+i*dx),snapshots=snap,tangent_tests=tan,
        homogeneous_rhs=pre,maximum_inverse_error=m.max_inverse,minimum_schur_fraction=m.min_schur_fraction,
        elapsed_seconds=time.monotonic()-beg)
    with (BASE/f'HOMOGENEOUS_TILT_SATURATION_V001_S{steps}_ROW.json').open('x') as f:json.dump(row,f,allow_nan=False)
    print(json.dumps({k:v for k,v in row.items() if k not in ('snapshots','tangent_tests')}),flush=True)
    return row


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    saved=json.loads(base.SOURCE.read_text());beg=time.monotonic()
    rows=[integrate(saved,n) for n in (4096,8192,16384)]
    rt=stable.compare(rows[1],rows[2]);ss=[s for r in rows for s in r['snapshots']]
    checks=dict(all_completed=all(r['completed'] for r in rows),
        homogeneous=max(r['homogeneous_rhs'] for r in rows)<=2e-12,
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        time_refinement=rt is not None and rt['maximum']<=1e-4,
        Hamiltonian_background=max(s['Hamiltonian_background_normalized'] for s in ss)<=1e-9,
        conserved_charge=max(abs(s['mean_charge_change']) for s in ss)<=2e-12,
        eliminated_momentum_flow=all(t['passed'] for r in rows for t in r['tangent_tests']))
    deps=['plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py']
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={base.SOURCE.name:hashlib.sha256(base.SOURCE.read_bytes()).hexdigest()},
        dependencies_sha256={n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in deps},
        physical_seed=1e-12,cold_tilt_power=Model(saved).power,rows=rows,time_refinement=rt,
        controls=checks,all_controls_passed=all(checks.values()),elapsed_seconds=time.monotonic()-beg,
        peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','protocol')},indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
