"""Same K(X) action through recombination at the counted physical Hunit fit.

No new physical fit. Use saved authenticated candidate/reference HYREC xe
per hydrogen nucleus; n_e=xe*nH, with explicit measured-T0 radiation.
Above z8000 adopt fully ionized H/He, using HYREC's helium number ratio.
Fixed k=.01,.1/Mpc, ai1e-7 to z800, common visibility-peak checkpoint.
Same common curvature seed, regular adiabatic initial conditions, ordinary
Thomson scattering, cold baryon stress, massless thermal neutrinos.
Not TT/TE/EE spectra, a likelihood, native photon origin or superiority.

Frozen gates: time/start/hierarchy/atomic interpolation 1e-4; Einstein
constraint1e-6; algebra identities1e-10. Hierarchy comparison through l4,
time comparison all retained states. Steps1024/2048; lg16,ln48 vs20,64.
Saved histories are immutable checkpoints; reuse only authenticated inputs.
No clipping, retuning, reionization or changed equation implementation.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_plasma_v001 as plasma
import invariant_clock_acoustic_v001 as acoustic

BASE=Path(__file__).resolve().parent
PREFIX='INVARIANT_CLOCK_RECOMBINATION_TRANSFER_V001'
CAL=BASE/'INVARIANT_CLOCK_CMB_CALIBRATION_V001_RESULT.json'
CAL_SHA='af1a41ed9b0d0f1ea2f2d8ac7ee9df67d2a3282989d09e019bbe3959c68ee9e1'
OUT=BASE/(PREFIX+'_RESULT.json')
AF=1/801


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


class Thermal:
    def __init__(self,model,cal):
        self.model=model;self.bg=acoustic.Background(model)
        self.tables={};self.files={}
        self.thin=1
        for dust,row in zip((False,True),cal['rows']):
            for kind in ('half','default'):
                inv=row['invocations'][kind];p=BASE/inv['output_path']
                if sha(p)!=inv['output_sha256']:raise ValueError('Changed atomic history')
                raw=json.loads(p.read_text())
                if raw['columns'][1]!='xe_per_H':raise ValueError('Wrong electron units')
                arr=np.array(raw['rows'],float)
                self.tables[dust,kind]=arr[:,:3];self.files[p.name]=sha(p)
        self.atomic='half'
        hsi=self.bg.hunit;s=plasma.SI
        self.nH0=3*hsi*hsi*model.OB*(1-plasma.YHE)/(8*math.pi*s['GN']*s['Gcos_over_GN']*s['mp'])
        self.xfull=1+2*plasma.YHE/((1-plasma.YHE)*3.97153)
    def background(self,model,x,K,dust=False,opacity_scale=1.):
        b=plasma.prior.background(model,x,radiation=self.bg.OR,dust=dust)
        b['rg']=b['rr']/(1+plasma.RN);b['rn']=b['rr']-b['rg']
        b['Rb']=3*b['rb']/(4*b['rg']);b['r2']=(K/b['a'])**2/b['H2']
        b['r']=math.sqrt(b['r2']);b['sr']=-1-b['hx']
        tab=self.tables[dust,self.atomic][::self.thin];z=1/b['a']-1
        if z>tab[-1,0]:
            xe=self.xfull;tm=acoustic.T0/b['a']
        else:
            if z<tab[0,0]:raise ValueError('Opacity extrapolation below history')
            xe=float(np.interp(z,tab[:,0],tab[:,1]));tm=float(np.interp(z,tab[:,0],tab[:,2]))
        b['g']=opacity_scale*self.nH0*xe*plasma.SI['sigmaT']*plasma.SI['c']/(b['a']**3*self.bg.hunit*b['H'])
        b['xe']=xe;b['Tm']=tm
        # Conservative ordinary adiabatic sound speed screen, not a
        # substituted thermal perturbation closure or an acceptance gate.
        b['cold_baryon_pressure_screen']=b['r2']*(5/3)*acoustic.KBOLTZ*tm*(1+xe+plasma.YHE/((1-plasma.YHE)*3.97153))/(plasma.SI['mp']*plasma.SI['c']**2)
        return b


def integrate(model,thermal,K,steps,layout,astar,ai=1e-7,dust=False):
    started=time.monotonic();keep=[i for i,n in enumerate(layout.names) if not(dust and n in ('B','Zh'))]
    state=plasma.initial(model,K,ai,layout,dust);z=state[keep]
    # Shared logarithmic checkpoints plus the common candidate visibility
    # peak and the helium-history join. Earlier start adds a prelude only.
    targets=np.unique(np.r_[np.linspace(math.log(1e-7),math.log(AF),65),math.log(astar),math.log(1/8001)])
    if ai<1e-7:targets=np.r_[math.log(ai),targets]
    snapshots=[];maxc=maxcap=maxspatial=maxpressure=0.
    hmax=math.log(AF/1e-7)/steps;x=math.log(ai);calls=0
    def matrix(xx):return plasma.matrix(model,xx,K,layout,dust)[0][np.ix_(keep,keep)]
    for target in targets:
        if target>x+1e-14:
            count=int(math.ceil((target-x)/hmax));h=(target-x)/count
            for _ in range(count):
                z=plasma.radau_step(z,x,h,matrix);x+=h;calls+=1
                if not np.all(np.isfinite(z)):raise FloatingPointError('Nonfinite transfer')
        x=float(target);state=np.zeros(layout.n);state[keep]=z
        _,b,ph=plasma.matrix(model,x,K,layout,dust);cr,_=plasma.constraint(b,layout)
        err=abs(cr@state)/max(float(abs(cr)@abs(state)),1e-30);maxc=max(maxc,err)
        if not dust:
            gap=model.Q0*model.eps/((1+b['s'])*(math.sqrt(1+model.eps)+b['qr']))
            low=model.Q0*model.eps*b['s']/((1+b['s'])*(b['qr']+1))
            maxcap=max(maxcap,abs(b['Q']*b['cs']*state[3])/min(gap,low))
            maxspatial=max(maxspatial,abs(b['r']*b['Q']*state[5])/model.bs)
        maxpressure=max(maxpressure,b['cold_baryon_pressure_screen'])
        phi=float(ph@state);wg=1/(1+b['Rb']);ug=state[2]-(1-wg)*state[8]
        ub=state[2]+wg*state[8]
        ix=layout.index;polar=state[ix['fg2']]+state[ix['pol0']]+state[ix['pol2']]
        transfer=dict(monopole_plus_lapse=state[7]/4+phi,photon_velocity=b['r']*ug,
            baryon_velocity=b['r']*ub,Weyl=(state[0]+phi)/2,
            photon_quadrupole=b['r2']*state[ix['fg2']],polarization_source=b['r2']*polar,
            baryon_density=state[1],clock_density=state[3]-state[6])
        snapshots.append(dict(a=b['a'],state=state.tolist(),Phi=phi,constraint=err,
            transfer=transfer,xe=b['xe'],H_over_Gamma=1/b['g'],kphysical_over_Gamma=b['r']/b['g']))
    return dict(steps=steps,actual_steps=calls,ai=ai,lg=layout.lg,ln=layout.ln,names=layout.names,dust=dust,
        snapshots=snapshots,maximum_constraint=maxc,linear_clock_margin_ratio=maxcap,
        linear_spatial_ratio=maxspatial,cold_baryon_pressure_screen=maxpressure,
        elapsed_seconds=time.monotonic()-started)


def main():
    start=time.monotonic()
    if OUT.exists():raise FileExistsError(OUT)
    if sha(CAL)!=CAL_SHA:raise ValueError('Changed calibration')
    cal=json.loads(CAL.read_text());seed=json.loads(plasma.prior.old.base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0']=100.;seed['inherited']['H0_km_s_Mpc']=cal['selected_Hunit']
    model=plasma.prior.old.base.Model(seed,1);thermal=Thermal(model,cal)
    # In-memory dependency injection only; original plasma file unchanged.
    plasma.background=thermal.background
    astar=1/(1+cal['rows'][0]['observables']['zstar'])
    controls=[];rows=[];files={}
    def check(name,value,tol):controls.append(dict(name=name,error=float(value),tolerance=tol,passed=bool(value<=tol)))
    layout=plasma.Layout(16,48);high=plasma.Layout(20,64)
    common=[n for n in layout.names if n in layout.names[:11] or (n.startswith(('fg','fn')) and int(n[2:])<=4) or (n.startswith('pol') and int(n[3:])<=4)]
    for dust in (False,True):
        for kval in (.01,.1):
            tag=('REF' if dust else 'KX')+('_K001' if kval==.01 else '_K010')
            K=kval*299792.458/model.p['H0_km_s_Mpc'];hist={}
            for aa in (1e-7,1/8001,astar,AF):
                A,b,_=plasma.matrix(model,math.log(aa),K,layout,dust);cr,crx=plasma.constraint(b,layout)
                defect=crx+cr@A+(3+2*b['hx'])*cr
                scale=np.maximum(abs(crx)+abs(cr)@abs(A)+abs((3+2*b['hx'])*cr),1e-30)
                check(tag+'_constraint_identity_'+str(aa),np.max(abs(defect)/scale),1e-10)
            trials=[('COARSE',1024,layout,1e-7,'half',1),('FINE',2048,layout,1e-7,'half',1),
                ('START',2048,layout,5e-8,'half',1),('HIERARCHY',2048,high,1e-7,'half',1),
                ('ATOMIC',2048,layout,1e-7,'default',1),('THIN',2048,layout,1e-7,'half',2)]
            for label,n,lay,ai,kind,thin in trials:
                thermal.atomic=kind;thermal.thin=thin
                result=integrate(model,thermal,K,n,lay,astar,ai,dust)
                checkpoint=BASE/f'{PREFIX}_{tag}_{label}.json'
                with checkpoint.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
                files[checkpoint.name]=sha(checkpoint);hist[label]=result
                print(json.dumps(dict(row=tag,trial=label,seconds=result['elapsed_seconds'],constraint=result['maximum_constraint'])),flush=True)
            names=[n for n in common if not(dust and n in ('B','Zh'))]
            errs=dict(time=plasma.errors(hist['COARSE'],hist['FINE']),
                start=plasma.errors(hist['FINE'],hist['START'],endpoint=True),
                hierarchy=plasma.errors(hist['FINE'],hist['HIERARCHY'],names),
                atomic=plasma.errors(hist['FINE'],hist['ATOMIC']),
                interpolation=plasma.errors(hist['FINE'],hist['THIN']))
            for key,err in errs.items():check(tag+'_'+key,err['error'],1e-4)
            for label,h in hist.items():check(tag+'_trajectory_constraint_'+label,h['maximum_constraint'],1e-6)
            picks={}
            for label,aa in (('visibility_peak',astar),('z800',AF)):
                i=int(np.argmin([abs(s['a']/aa-1) for s in hist['FINE']['snapshots']]))
                picks[label]=hist['FINE']['snapshots'][i]
            rows.append(dict(kind=tag,k_Mpc_inverse=kval,dust=dust,errors=errs,selected=picks,
                linear_clock_margin_ratio=hist['FINE']['linear_clock_margin_ratio'],
                linear_spatial_ratio=hist['FINE']['linear_spatial_ratio'],
                cold_baryon_pressure_screen=hist['FINE']['cold_baryon_pressure_screen']))
    comparisons=[]
    for kval in (.01,.1):
        ca=next(r for r in rows if r['k_Mpc_inverse']==kval and not r['dust'])
        re=next(r for r in rows if r['k_Mpc_inverse']==kval and r['dust'])
        for label in ('visibility_peak','z800'):
            a=ca['selected'][label]['transfer'];b=re['selected'][label]['transfer']
            comparisons.append(dict(k_Mpc_inverse=kval,epoch=label,candidate=a,reference=b,
                differences_per_primordial_curvature={n:(a[n]-b[n])/plasma.prior.SEED for n in a},
                ratios={n:a[n]/b[n] if b[n]!=0 else None for n in a}))
    sourcefiles=[Path(__file__),Path(plasma.__file__),Path(plasma.prior.__file__),Path(acoustic.__file__),CAL,plasma.prior.old.base.SOURCE]
    result=dict(protocol=__doc__,fixed=model.p,additional_fitted_freedoms=0,inherited_Hunit_fit_freedoms=1,
        radiation_omega=thermal.bg.OR,nH0_m_inverse3=thermal.nH0,fully_ionized_xe=thermal.xfull,
        high_z_join_relative_jump=thermal.xfull/thermal.tables[False,'half'][-1,1]-1,
        controls=controls,rows=rows,comparisons=comparisons,
        all_numerical_controls_passed=all(c['passed'] for c in controls),
        elapsed_seconds=time.monotonic()-start,hashes={**{p.name:sha(p) for p in sourcefiles},**thermal.files,**files})
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(all_numerical_controls_passed=result['all_numerical_controls_passed'],
        failed=[c for c in controls if not c['passed']],comparisons=comparisons,seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
