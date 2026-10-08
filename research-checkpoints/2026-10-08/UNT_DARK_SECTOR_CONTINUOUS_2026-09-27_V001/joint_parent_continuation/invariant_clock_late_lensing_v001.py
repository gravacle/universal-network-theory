"""Recombination Cauchy data to fixed z=1 lensing/ordinary-velocity ratio.

No new physical parameter, initial mode, amplitude or halo fit. Reuse
authenticated V002 recombination states at z800, fixed k=.01,.1/Mpc.
Same residual HYREC ionization (NO reionization), cold baryons, massless
thermal neutrinos and minimally coupled ordinary photons. Not survey E_G,
nonlinear galaxies, a likelihood or physical-model superiority.

Replace hard high-l boundary by MB asymptotic free-streaming closure:
fL'=r f(L-1)-[(L+1)/(a H eta)+2sr+gcoll]fL, fL=FL/r^2.
This approximation requires cutoff refinement, not a reflecting wall.
https://arxiv.org/html/astro-ph/9506072v1 equations51,65.
EG=2 a^3 H^2 Weyl/(3 Htoday^2 Ub), Weyl=(Phi+Psi)/2.
https://arxiv.org/abs/0704.1932 ; actual Htoday includes radiation.

Prospective gates unchanged: full time-state1e-4, low-l hierarchy1e-4,
trajectory Einstein1e-6, algebra1e-10; conformal-time quadrature1e-10.
4096/8192 Radau steps, saved16/48 vs20/64 hierarchies. Preserve failure.
Report signed per-curvature transfers, EG and cutoff/time sensitivities.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_recombination_transfer_v002 as rec

BASE=Path(__file__).resolve().parent
PREFIX='INVARIANT_CLOCK_LATE_LENSING_V001'
OUT=BASE/(PREFIX+'_RESULT.json')
REC_SHA='07fd5190198b2cf309b14598bfbae25def98d65b34db64b85dfe7a649da144cc'
plasma=rec.plasma;acoustic=rec.pilot.acoustic
AI=rec.pilot.AF;AF=.5


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


class Conformal:
    def __init__(self,model,dust,n=2048,order=8):
        bg=acoustic.Background(model,dust);self.bg=bg
        self.x=np.linspace(math.log(AI),math.log(AF),n+1)
        self.h=self.x[1]-self.x[0]
        g,w=np.polynomial.legendre.leggauss(order)
        nodes=(self.x[:-1,None]+self.x[1:,None])/2+self.h*g/2
        ff=np.exp(-nodes)/bg.E(np.exp(nodes))
        eta0=acoustic.quad(lambda a:1/(a*a*bg.E(a)),0.,AI,256)
        self.value=np.r_[eta0,eta0+np.cumsum(self.h/2*(ff@w))]
        self.deriv=np.exp(-self.x)/bg.E(np.exp(self.x))
    def at(self,x):
        i=min(max(int((x-self.x[0])/self.h),0),len(self.x)-2)
        t=(x-self.x[i])/self.h
        return (2*t**3-3*t*t+1)*self.value[i]+(t**3-2*t*t+t)*self.h*self.deriv[i]+(-2*t**3+3*t*t)*self.value[i+1]+(t**3-t*t)*self.h*self.deriv[i+1]


def matrix(model,x,K,layout,eta,dust):
    A,b,ph=plasma.matrix(model,x,K,layout,dust)
    conformal=eta.at(x);rate=1/(b['a']*b['H']*conformal)
    for kind,L,drag in (('fg',layout.lg,b['g']),('pol',layout.lg,b['g']),('fn',layout.ln,0.)):
        A[layout.index[f'{kind}{L}']]=b['r']*layout.get(f'{kind}{L-1}')-((L+1)*rate+2*b['sr']+drag)*layout.get(f'{kind}{L}')
    return A,b,ph


def integrate(model,K,dust,layout,initial,steps,eta):
    start=time.monotonic();keep=[i for i,n in enumerate(layout.names) if not(dust and n in ('B','Zh'))]
    z=np.array(initial['snapshots'][-1]['state'])[keep]
    if initial['names']!=layout.names:raise ValueError('Initial layout mismatch')
    x0=math.log(AI);dx=math.log(AF/AI)/steps;snaps=[]
    htoday2=float(acoustic.Background(model,dust).E(1.))**2
    maxc=maxcap=maxspatial=0.
    def mm(x):return matrix(model,x,K,layout,eta,dust)[0][np.ix_(keep,keep)]
    for i in range(steps+1):
        x=x0+i*dx
        if i%(steps//64)==0:
            state=np.zeros(layout.n);state[keep]=z
            A,b,ph=matrix(model,x,K,layout,eta,dust);cr,_=plasma.constraint(b,layout)
            defect=abs(cr@state)/max(float(abs(cr)@abs(state)),1e-30);maxc=max(maxc,defect)
            if not dust:
                gap=model.Q0*model.eps/((1+b['s'])*(math.sqrt(1+model.eps)+b['qr']))
                low=model.Q0*model.eps*b['s']/((1+b['s'])*(b['qr']+1))
                maxcap=max(maxcap,abs(b['Q']*b['cs']*state[3])/min(gap,low))
                maxspatial=max(maxspatial,abs(b['r']*b['Q']*state[5])/model.bs)
            phi=float(ph@state);weyl=(state[0]+phi)/2
            wg=1/(1+b['Rb']);ub=state[2]+wg*state[8];ug=state[2]-(1-wg)*state[8]
            delta=state[1]+3*ub;ubprime=b['hx']*ub+phi+b['g']/b['Rb']*(ug-ub)
            dprime=A[1]@state+3*ubprime
            eg=2*b['a']**3*b['H2']*weyl/(3*htoday2*ub)
            obs=dict(Weyl_per_curvature=weyl/plasma.prior.SEED,
                baryon_velocity_per_curvature=b['r']*ub/plasma.prior.SEED,
                comoving_baryon_contrast_per_curvature=delta/plasma.prior.SEED,
                baryon_growth_rate=dprime/delta,kinematic_growth_rate=-b['r2']*ub/delta,
                EG=eg,photon_density_per_curvature=state[7]/plasma.prior.SEED,
                gravitational_slip=phi/state[0],k_eta=K*eta.at(x))
            snaps.append(dict(a=b['a'],state=state.tolist(),constraint=defect,observables=obs))
        if i==steps:break
        z=plasma.radau_step(z,x,dx,mm)
        if not np.all(np.isfinite(z)):raise FloatingPointError('nonfinite late state')
    return dict(steps=steps,names=layout.names,dust=dust,lg=layout.lg,ln=layout.ln,snapshots=snaps,
        maximum_constraint=maxc,linear_clock_margin_ratio=maxcap,linear_spatial_ratio=maxspatial,
        elapsed_seconds=time.monotonic()-start)


def main():
    start=time.monotonic()
    if OUT.exists():raise FileExistsError(OUT)
    if sha(rec.OUT)!=REC_SHA:raise ValueError('Changed recombination receipt')
    saved=json.loads(rec.OUT.read_text());cal=json.loads(rec.pilot.CAL.read_text())
    for name,digest in saved['hashes'].items():
        if sha(BASE/name)!=digest:raise ValueError('Changed dependency '+name)
    seed=json.loads(plasma.prior.old.base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0']=100.;seed['inherited']['H0_km_s_Mpc']=cal['selected_Hunit']
    model=plasma.prior.old.base.Model(seed,1);thermal=rec.Thermal(model,cal);plasma.background=thermal.background
    controls=[];rows=[];allhist={};files={}
    def check(name,val,tol):controls.append(dict(name=name,error=float(val),tolerance=tol,passed=bool(val<=tol)))
    for dust in (False,True):
        eta=Conformal(model,dust);etaf=Conformal(model,dust,4096,12)
        xx=np.linspace(math.log(AI),math.log(AF),130)
        check(('REF' if dust else 'KX')+'_conformal_time',max(abs(eta.at(x)/etaf.at(x)-1) for x in xx),1e-10)
        for kval in (.01,.1):
            tag=('REF' if dust else 'KX')+('_K001' if kval==.01 else '_K010')
            K=kval*299792.458/model.p['H0_km_s_Mpc'];hist={}
            for label,steps,lg,ln,old in [('COARSE',4096,16,48,'FINE'),('FINE',8192,16,48,'FINE'),('HIERARCHY',8192,20,64,'HIERARCHY')]:
                path=BASE/f'{rec.PREFIX}_{tag}_{old}.json';initial=json.loads(path.read_text())
                layout=plasma.Layout(lg,ln)
                for aa in (AI,.01,.1,AF):
                    A,b,_=matrix(model,math.log(aa),K,layout,eta,dust);cr,crx=plasma.constraint(b,layout)
                    err=crx+cr@A+(3+2*b['hx'])*cr
                    norm=np.maximum(abs(crx)+abs(cr)@abs(A)+abs((3+2*b['hx'])*cr),1e-30)
                    check(tag+'_'+label+'_constraint_identity_'+str(aa),np.max(abs(err)/norm),1e-10)
                result=integrate(model,K,dust,layout,initial,steps,eta);hist[label]=result
                out=BASE/f'{PREFIX}_{tag}_{label}.json'
                with out.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
                files[out.name]=sha(out)
                print(json.dumps(dict(row=tag,trial=label,seconds=result['elapsed_seconds'],constraint=result['maximum_constraint'],endpoint=result['snapshots'][-1]['observables'])),flush=True)
            names=[n for n in hist['FINE']['names'] if (n in hist['FINE']['names'][:11] or (n.startswith(('fg','fn')) and int(n[2:])<=4) or(n.startswith('pol') and int(n[3:])<=4)) and not(dust and n in ('B','Zh'))]
            errs=dict(time=plasma.errors(hist['COARSE'],hist['FINE']),hierarchy=plasma.errors(hist['FINE'],hist['HIERARCHY'],names))
            for label,val in errs.items():check(tag+'_'+label,val['error'],1e-4)
            for label,h in hist.items():check(tag+'_trajectory_'+label,h['maximum_constraint'],1e-6)
            rows.append(dict(kind=tag,k_Mpc_inverse=kval,errors=errs,
                linear_clock_margin_ratio=hist['FINE']['linear_clock_margin_ratio'],
                linear_spatial_ratio=hist['FINE']['linear_spatial_ratio']))
            allhist[dust,kval]=hist
    comparisons=[]
    for kval in (.01,.1):
        ca=allhist[False,kval];re=allhist[True,kval]
        c=ca['FINE']['snapshots'][-1]['observables'];r=re['FINE']['snapshots'][-1]['observables']
        delta={n:c[n]-r[n] for n in c};sens={}
        for label in ('COARSE','HIERARCHY'):
            cc=ca[label]['snapshots'][-1]['observables'];rr=re[label]['snapshots'][-1]['observables']
            sens[label]=dict(candidate_change={n:cc[n]-c[n] for n in c},reference_change={n:rr[n]-r[n] for n in c},
                paired_change={n:cc[n]-rr[n]-delta[n] for n in c})
        comparisons.append(dict(k_Mpc_inverse=kval,z=1.,candidate=c,reference=r,difference=delta,
            ratios={n:c[n]/r[n] for n in c if r[n]!=0},sensitivity=sens))
    sources=[Path(__file__),Path(rec.__file__),Path(rec.pilot.__file__),Path(plasma.__file__),rec.OUT]
    result=dict(protocol=__doc__,fixed=model.p,additional_fitted_freedoms=0,rows=rows,comparisons=comparisons,
        controls=controls,all_numerical_controls_passed=all(c['passed'] for c in controls),
        hashes={**{p.name:sha(p) for p in sources},**files},elapsed_seconds=time.monotonic()-start)
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(all_numerical_controls_passed=result['all_numerical_controls_passed'],failed=[c for c in controls if not c['passed']],seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
