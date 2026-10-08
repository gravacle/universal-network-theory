"""Full-constraint central field Jacobian, not another source trajectory.

The pure spherical fast principal block is RK4-stable. Now retain ALL
implemented field terms and radial metric constraints on identical32/64/96
central nodes, holding ordinary variables and outer field perturbations
fixed. Initial and saved BUFFER600 quarter-orbit states. Central proper
time removes the purely exterior lapse factor. Two centered increments
1e-3 and5e-4 of scales(u1e-4,p1e-8,Z1e-8,cp.01) test derivative sensitivity.

Freeze polynomial eigen residual1e-10, matrix refinement1e-6. Report
eigenvalue/block sensitivity rather than declaring continuum stability.
Use actual dt*N0 for RK4, since matrix is in central proper time. Observe
mode localization so a frozen artificial outer edge does not count as an
origin mode. This is a four-field subsystem; ordinary perturbations are
not evolved. No physical change or accepted galaxy result follows.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_polar_source_v006 as source

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_POLAR_CENTRAL_JACOBIAN_V001_RESULT.json'


def main():
    if OUT.exists():raise FileExistsError(OUT)
    start=time.monotonic();saved=json.loads(source.prev.inherited.SOURCE.read_text())
    model=source.Polar(saved,960,.012,.125,600.);initial=model.initial()
    path=BASE/'INVARIANT_CLOCK_POLAR_SOURCE_BUFFER01C_RESULT.json';receipt=json.loads(path.read_text())
    cp_path=BASE/receipt['checkpoint'];cp=json.loads(cp_path.read_text())
    final=np.array(cp['state']);dt=receipt['dt'];sc=np.array([1e-4,1e-8,1e-8,.01])[:,None]
    rows=[];checks=[]
    def check(name,error,gate):
        checks.append(dict(name=name,error=float(error),tolerance=gate,passed=bool(error<=gate)))
    for state_name,z,t in [('initial',initial,0.),('quarter_orbit',final,cp['step']*cp['dt'])]:
        geom=model.geometry(t,z);guess=geom['A'].copy()
        integral=model.lapseint@geom['g'];n0=float(np.exp(geom['lnN'][0]-integral[0]))
        for n in (32,64,96):
            previous=None
            for eps in (1e-3,5e-4):
                matrix=np.empty((4*n,4*n))
                for column in range(4*n):
                    component,index=divmod(column,n)
                    plus=z.copy();minus=z.copy()
                    plus[component,index]+=eps*sc[component,0]
                    minus[component,index]-=eps*sc[component,0]
                    fs=[]
                    for zz in (plus,minus):
                        model.Aguess=guess.copy();rhs,g=model.rhs(t,zz,True)
                        lint=model.lapseint@g['g'];center=np.exp(g['lnN'][0]-lint[0])
                        fs.append(rhs[:4,:n]/(sc*center))
                    matrix[:,column]=((fs[0]-fs[1])/(2*eps)).ravel()*model.tdyn
                norm=np.linalg.norm(matrix);values,vectors=np.linalg.eig(matrix);modes=[]
                for index,val in enumerate(values):
                    vec=vectors[:,index];weights=np.sum(abs(vec.reshape(4,n))**2,axis=0)
                    peak=int(np.argmax(weights));r95=int(np.searchsorted(np.cumsum(weights)/sum(weights),.95))
                    zz=val*dt*n0/model.tdyn;rk=1+zz+zz*zz/2+zz**3/6+zz**4/24
                    half=zz/2;rh=1+half+half*half/2+half**3/6+half**4/24
                    modes.append(dict(eigenvalue_per_tdyn=[float(val.real),float(val.imag)],
                        peak_index=peak,index95=r95,peak_radius_over_L=float(model.r[peak]/model.L),
                        central_localized=peak<n//4 and r95<n//2,
                        component_weight=np.sum(abs(vec.reshape(4,n))**2,axis=1).tolist(),
                        eigen_residual=float(np.linalg.norm(matrix@vec-val*vec)/norm/np.linalg.norm(vec)),
                        RK4_gain=float(abs(rk)),half_step_gain=float(abs(rh)),
                        RK4_rate_per_tdyn=float(np.log(max(abs(rk),1e-300))*model.tdyn/(dt*n0))))
                tag=f'{state_name}_{n}_{eps}'
                check(tag+'_eigen_residual',max(m['eigen_residual'] for m in modes),1e-10)
                change=None
                if previous is not None:
                    change=float(np.linalg.norm(matrix-previous)/norm)
                    check(tag+'_matrix_refinement',change,1e-6)
                previous=matrix
                ordered=sorted(modes,key=lambda v:v['eigenvalue_per_tdyn'][0],reverse=True)
                centers=[v for v in ordered if v['central_localized']]
                row=dict(state=state_name,block_nodes=n,increment=eps,matrix_refinement=change,
                         maximum_real_modes=ordered[:4],central_modes=centers[:4],
                         maximum_RK4_gain=max(v['RK4_gain'] for v in modes),central_lapse=n0)
                rows.append(row);print(json.dumps(row),flush=True)
    paths=[Path(__file__),path,cp_path,Path(source.__file__),Path(source.mixed.__file__),source.prev.inherited.SOURCE]
    result=dict(protocol=__doc__,elapsed_seconds=time.monotonic()-start,rows=rows,checks=checks,
                all_numerical_controls_passed=all(c['passed'] for c in checks),
                identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(dict(elapsed_seconds=result['elapsed_seconds'],checks=checks,
                         all_numerical_controls_passed=result['all_numerical_controls_passed'])),flush=True)


if __name__=='__main__':main()
