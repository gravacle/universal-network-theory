"""Refine the preserved recombination pilot without changing its gates.

V001 fails full retained-state time refinement at fg16/pol16. Its nH0
reconstruction also differs from the saved HYREC convention by~.054%.
Use HYREC's own authenticated nH0 and fHe, and4096/8192 time steps.
Identical action, Hunit, curvature seed, k, cuts, endpoint, physical
assumptions and gates. Paired signed transfer differences/uncertainties
are normalized by primordial curvature, not near-zero acoustic values.
Checkpoint each short trajectory. No observational verdict or new fit.
"""
from pathlib import Path
import hashlib
import json
import math
import time
import numpy as np
import invariant_clock_recombination_transfer_v001 as pilot

BASE=Path(__file__).resolve().parent
PREFIX='INVARIANT_CLOCK_RECOMBINATION_TRANSFER_V002'
OUT=BASE/(PREFIX+'_RESULT.json')
plasma=pilot.plasma


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


class Thermal(pilot.Thermal):
    def __init__(self,model,cal):
        super().__init__(model,cal)
        self.metadata={}
        for dust,row in zip((False,True),cal['rows']):
            for kind in ('half','default'):
                p=BASE/row['invocations'][kind]['output_path'];raw=json.loads(p.read_text())
                self.metadata[dust,kind]=(raw['nH0_cm3']*1e6,1+2*raw['fHe'])
        self.old_nH0=self.nH0
        if len(set(self.metadata.values()))!=1:raise ValueError('Atomic normalization differs between histories')
        self.nH0,self.xfull=self.metadata[False,'half']


def pick(hist,a):
    return min(hist['snapshots'],key=lambda r:abs(r['a']/a-1))


def main():
    started=time.monotonic()
    if OUT.exists():raise FileExistsError(OUT)
    if sha(pilot.CAL)!=pilot.CAL_SHA:raise ValueError('Changed calibration')
    cal=json.loads(pilot.CAL.read_text());seed=json.loads(plasma.prior.old.base.SOURCE.read_text())
    seed['inherited']['Q0_over_H0']=100.;seed['inherited']['H0_km_s_Mpc']=cal['selected_Hunit']
    model=plasma.prior.old.base.Model(seed,1);thermal=Thermal(model,cal);plasma.background=thermal.background
    astar=1/(1+cal['rows'][0]['observables']['zstar']);controls=[];rows=[];files={};histories={}
    def check(name,value,tol):controls.append(dict(name=name,error=float(value),tolerance=tol,passed=bool(value<=tol)))
    layout=plasma.Layout(16,48);high=plasma.Layout(20,64)
    common=[n for n in layout.names if n in layout.names[:11] or (n.startswith(('fg','fn')) and int(n[2:])<=4) or (n.startswith('pol') and int(n[3:])<=4)]
    for dust in (False,True):
        for kval in (.01,.1):
            tag=('REF' if dust else 'KX')+('_K001' if kval==.01 else '_K010')
            K=kval*299792.458/model.p['H0_km_s_Mpc'];hist={}
            for aa in (1e-7,1/8001,astar,pilot.AF):
                A,b,_=plasma.matrix(model,math.log(aa),K,layout,dust);cr,crx=plasma.constraint(b,layout)
                residual=crx+cr@A+(3+2*b['hx'])*cr
                scale=np.maximum(abs(crx)+abs(cr)@abs(A)+abs((3+2*b['hx'])*cr),1e-30)
                check(tag+'_constraint_identity_'+str(aa),np.max(abs(residual)/scale),1e-10)
                check(tag+'_physical_background_'+str(aa),abs(b['H']/float(pilot.acoustic.Background(model,dust).E(aa))-1),1e-10)
            trials=[('COARSE',4096,layout,1e-7,'half',1),('FINE',8192,layout,1e-7,'half',1),
                ('START',8192,layout,5e-8,'half',1),('HIERARCHY',8192,high,1e-7,'half',1),
                ('ATOMIC',8192,layout,1e-7,'default',1),('THIN',8192,layout,1e-7,'half',2)]
            for label,n,lay,ai,kind,thin in trials:
                thermal.atomic=kind;thermal.thin=thin
                result=pilot.integrate(model,thermal,K,n,lay,astar,ai,dust)
                path=BASE/f'{PREFIX}_{tag}_{label}.json'
                with path.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
                files[path.name]=sha(path);hist[label]=result
                print(json.dumps(dict(row=tag,trial=label,seconds=result['elapsed_seconds'],constraint=result['maximum_constraint'])),flush=True)
            names=[n for n in common if not(dust and n in ('B','Zh'))]
            errs=dict(time=plasma.errors(hist['COARSE'],hist['FINE']),start=plasma.errors(hist['FINE'],hist['START'],endpoint=True),
                hierarchy=plasma.errors(hist['FINE'],hist['HIERARCHY'],names),atomic=plasma.errors(hist['FINE'],hist['ATOMIC']),
                interpolation=plasma.errors(hist['FINE'],hist['THIN']))
            for key,value in errs.items():check(tag+'_'+key,value['error'],1e-4)
            for label,h in hist.items():check(tag+'_trajectory_constraint_'+label,h['maximum_constraint'],1e-6)
            selected={label:pick(hist['FINE'],aa) for label,aa in (('visibility_peak',astar),('z800',pilot.AF))}
            rows.append(dict(kind=tag,k_Mpc_inverse=kval,dust=dust,errors=errs,selected=selected,
                linear_clock_margin_ratio=hist['FINE']['linear_clock_margin_ratio'],
                linear_spatial_ratio=hist['FINE']['linear_spatial_ratio'],
                cold_baryon_pressure_screen=hist['FINE']['cold_baryon_pressure_screen']))
            histories[dust,kval]=hist
    comparisons=[]
    for kval in (.01,.1):
        ca=histories[False,kval];re=histories[True,kval]
        targets=[('visibility_peak',astar),('z800',pilot.AF)]
        targets += [(f'window_z{1/r["a"]-1:.3f}',r['a']) for r in ca['FINE']['snapshots'] if 900<1/r['a']-1<1500 and abs(r['a']/astar-1)>1e-10]
        for label,a in targets:
            c=pick(ca['FINE'],a)['transfer'];r=pick(re['FINE'],a)['transfer']
            delta={n:(c[n]-r[n])/plasma.prior.SEED for n in c};uncert={}
            for trial in ('COARSE','START','HIERARCHY','ATOMIC','THIN'):
                cc=pick(ca[trial],a)['transfer'];rr=pick(re[trial],a)['transfer']
                uncert[trial]=dict(paired_difference_change={n:(cc[n]-rr[n])/plasma.prior.SEED-delta[n] for n in c},
                    candidate_transfer_change={n:(cc[n]-c[n])/plasma.prior.SEED for n in c},
                    reference_transfer_change={n:(rr[n]-r[n])/plasma.prior.SEED for n in c})
            comparisons.append(dict(k_Mpc_inverse=kval,epoch=label,a=a,candidate_per_curvature={n:c[n]/plasma.prior.SEED for n in c},
                reference_per_curvature={n:r[n]/plasma.prior.SEED for n in r},differences_per_curvature=delta,
                sensitivity_per_curvature=uncert))
    sources=[Path(__file__),Path(pilot.__file__),Path(plasma.__file__),Path(plasma.prior.__file__),Path(pilot.acoustic.__file__),pilot.CAL,pilot.OUT,plasma.prior.old.base.SOURCE]
    result=dict(protocol=__doc__,fixed=model.p,additional_fitted_freedoms=0,inherited_Hunit_fit_freedoms=1,
        radiation_omega=thermal.bg.OR,nH0_m_inverse3=thermal.nH0,pilot_nH0_relative_bias=thermal.old_nH0/thermal.nH0-1,
        fully_ionized_xe=thermal.xfull,high_z_join_relative_jump=thermal.xfull/thermal.tables[False,'half'][-1,1]-1,
        rows=rows,comparisons=comparisons,controls=controls,all_numerical_controls_passed=all(c['passed'] for c in controls),
        hashes={**{p.name:sha(p) for p in sources},**thermal.files,**files},elapsed_seconds=time.monotonic()-started)
    with OUT.open('x') as stream:json.dump(result,stream,indent=2,allow_nan=False)
    print(json.dumps(dict(all_numerical_controls_passed=result['all_numerical_controls_passed'],
        failed=[c for c in controls if not c['passed']],elapsed_seconds=result['elapsed_seconds'])),flush=True)


if __name__=='__main__':main()
