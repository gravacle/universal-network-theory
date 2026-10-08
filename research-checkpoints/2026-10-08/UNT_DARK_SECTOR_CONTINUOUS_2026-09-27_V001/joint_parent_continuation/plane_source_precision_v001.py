"""Targeted precision diagnosis, not another physical preparation.

Saved constrained N513 trajectories have pc Fourier n218 amplitude9.22e-14
already at a=.1, later amplified. The E_delta term dust_weight-1 subtracts
order-one numbers. Store the exactly equivalent analytic source contrast
with expm1, use it DIRECTLY, and use a stable density readout. No filtering,
smaller perturbation, action/branch/normalization change or tolerance change.
The frozen historical scripts/results remain unchanged.

Test only a=.01→.1, N513,1024 and2048 steps, one serial worker. This short
rerun diagnoses a named numerical defect in already-computed evolution;
it is not a new galaxy/expansion test. Require time-refinement<=1e-4 and
the existing constraint/charge gates; report (not assume) suppression of
early n218 noise and of maximum modes150..256 in local phase charge.
Compare saved full-IVP N513 a=.1, but disclose different step counts.
No acceptance of a=1 follows. Preserve source Fourier errors and hash inputs.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import resource
import numpy as np
import plane_constrained_evolution_v001 as prior
import plane_canonical_evolution_v002 as stable
import plane_canonical_evolution_v001 as base

BASE=Path(__file__).resolve().parent
OUT=BASE/'PLANE_SOURCE_PRECISION_V001_RESULT.json'
REFERENCE=BASE/'PLANE_CONSTRAINED_EVOLUTION_V002_RESULT.json'


class Model(prior.Model):
    def __init__(self,saved,N):
        super().__init__(saved,N)
        dm=saved['fixed']['seed']*np.cos(self.y)
        zm=saved['rows'][-1]['Z_minus_one']
        self.dust_excess=(np.expm1(6*self.lp)*(1+dm)+dm-zm)/(1+zm)
        self.dust_weight=1+self.dust_excess
        self.piT=6*self.OB*self.dust_weight

    def reconstruct(self,x,z):
        z=self.symmetric(z);g=self.unpack(x,z)
        a=g['abar'];h=g['h'];V=g['V'];ev=g['ev'];v=z[0]+2*z[1]
        R3=-(4*self.dx(g['bx'])+6*g['bx']**2-4*g['ax']*g['bx'])/g['A']**2
        ds=g['s']-g['sbar']
        dK=3*self.OA/self.D*(np.log1p(ds/(1+g['sbar']))-ds/((1+g['s'])*(1+g['sbar'])))
        vec=self.KB*g['e']**2+self.C*g['p']**2+self.C*g['J']
        ed=ev*(-R3+vec)/(6*h*h)-(g['Kbar']*np.expm1(v)+ev*dK)/(3*h*h)
        ed+=self.pcbar*(g['Qbar']*z[7]+(1+z[7])*g['qdiff'])/(6*a**3*h*h)
        ed+=g['c']*g['piux']/(6*a**3*h*h)+self.OB*self.dust_excess/(a**3*h*h)
        ed=(ed+ed[self.mirror])/2
        alpha=1.5*np.exp(-z[0]+z[1])*(1+ed)*g['bx']
        Jmom=-a*z[2]*g['piux']+g['piph']*self.dx(z[3])
        beta=np.exp(-z[0]-z[1]/2)*Jmom/(-4*a**3*h)
        wm1=np.expm1(z[0]+z[1]/2);W=1+wm1;meanpa=float(np.mean(z[4]))
        gg=np.zeros(self.N)
        for iteration in range(20):
            if np.any(1+gg<=0):raise ValueError('constrained pi_a chart approached zero')
            rhs=alpha/(1+gg)+beta
            self.max_odd_mean=max(self.max_odd_mean,abs(float(np.mean(rhs))))
            gv=self.primitive(rhs)
            constant=(meanpa-np.mean(wm1)-np.mean(W*gv))/np.mean(W)
            new=gv+constant
            change=float(np.max(abs(new-gg)));gg=new
            if change<=2e-13*max(float(np.max(abs(gg))),1e-8):break
        else:raise ValueError('periodic constraint Picard failed')
        self.max_picard=max(self.max_picard,iteration+1)
        pa=wm1+W*gg;R=1+pa;self.min_R=min(self.min_R,float(np.min(R)))
        if np.any(R<=0):raise ValueError('pi_a crossed chart boundary')
        pb=pa/4+.75*(np.expm1(v)+ev*ed-pa)/R
        full=z.copy();full[4]=pa;full[5]=pb
        return full

    def diagnostics(self,x,z):
        result=super().diagnostics(x,z);full=np.array(result['state'])
        db=self.dust_excess+(1+self.dust_excess)*np.expm1(-full[0]-2*full[1])
        result['max_abs_density_contrast']=float(np.max(abs(db)))
        result['density_cosine']=float(2*np.mean(db*np.cos(self.y)))
        return result


def short(saved,steps):
    m=Model(saved,513);z=m.initial();x0=math.log(.01);xf=math.log(.1);dx=(xf-x0)/steps
    started=time.monotonic();snapshots=[]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//8)==0:snapshots.append(m.diagnostics(x,z))
        if i==steps:break
        a=m.rhs(x,z);b=m.rhs(x+dx/2,z+dx*a/2);c=m.rhs(x+dx/2,z+dx*b/2);d=m.rhs(x+dx,z+dx*c)
        z+=dx*(a+2*b+2*c+d)/6
    fs=2*abs(np.fft.rfft(z[7]))/513
    return dict(nodes=513,steps=steps,completed=True,snapshots=snapshots,
        local_charge_n218_amplitude=float(fs[218]),local_charge_high_mode_max=float(np.max(fs[150:])),
        maximum_inverse_error=m.max_inverse,elapsed_seconds=time.monotonic()-started)


def main():
    np.seterr(over='raise',invalid='raise',divide='raise')
    saved=json.loads(base.SOURCE.read_text());ref=json.loads(REFERENCE.read_text())
    rows=[short(saved,n) for n in (1024,2048)];refine=stable.compare(rows[0],rows[1])
    old=ref['rows'][-1]['snapshots'][32];fs=2*abs(np.fft.rfft(np.array(old['state'])[7]))/513
    raw=prior.Model(saved,513);new=Model(saved,513)
    error=raw.dust_weight-1-new.dust_excess
    samples=[s for r in rows for s in r['snapshots']]
    checks=dict(time=refine['maximum']<=1e-4,
        inverse=max(r['maximum_inverse_error'] for r in rows)<=2e-12,
        H_background=max(s['Hamiltonian_background_normalized'] for s in samples)<=1e-9,
        H_perturbation=max(s['Hamiltonian_perturbation_normalized'] for s in samples)<=1e-4,
        momentum=max(s['momentum_normalized'] for s in samples)<=1e-4,
        charge=max(abs(s['mean_charge_change']) for s in samples)<=2e-12)
    result=dict(protocol=__doc__,self_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        inputs_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (base.SOURCE,REFERENCE)},
        dependencies_sha256={f:hashlib.sha256((BASE/f).read_bytes()).hexdigest() for f in ('plane_constrained_evolution_v001.py','plane_canonical_evolution_v001.py','plane_canonical_evolution_v002.py')},
        source_rounding_max=float(np.max(abs(error))),source_rounding_spectrum=(2*abs(np.fft.rfft(error))/513).tolist(),
        old_charge_n218_amplitude=float(fs[218]),old_charge_high_mode_max=float(np.max(fs[150:])),
        rows=rows,time_refinement=refine,controls=checks,all_controls_passed=all(checks.values()))
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('protocol','rows','source_rounding_spectrum')},indent=2))
    print(json.dumps([{k:v for k,v in r.items() if k!='snapshots'} for r in rows],indent=2))
    if not result['all_controls_passed']:raise SystemExit(1)


if __name__=='__main__':main()
