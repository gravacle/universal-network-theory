"""Frozen 1e-3 polar-source profile and invariant checks; no new evolution.

Compare complete inner10L primitive changes, gravity and expansion, with
cubic interpolation away from edge stencils. State normalizers are max
fine CHANGE from its own initial profile or these prespecified floors:
u1e-10, phi_R1e-8, Z1e-12, cp=mbar*1e-8, ordinary core restweight
peak*1e-8, core radial momentum1e-12, ell1e-14, background weight1e-8,
background momentum1e-10. Also report complete-state comparisons; do not
hide a small-response failure behind a large background. Exactly the same
gate applies to time, grid and domain comparisons. Derivative failures
do not invalidate otherwise controlled state observables automatically.

Raychaudhuri residual uses full U^mu partial_mu, not fixed-radius time;
time tangents use two increments. Spherical vorticity is zero. This is a
finite-state diagnostic, NOT a proof of asymptotic avoidance or formation
of a caustic. A singularity requires convergent invariant/event evidence.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import invariant_clock_polar_source_v004 as source

BASE=Path(__file__).resolve().parent


def interpolation(x,y,target):
    ids=np.clip(np.searchsorted(x,target)-1,1,len(x)-3)
    ans=np.zeros((y.shape[0],len(target)))
    for j in range(-1,3):
        weight=np.ones(len(target))
        for k in range(-1,3):
            if k!=j:weight*=(target-x[ids+k])/(x[ids+j]-x[ids+k])
        ans+=y[:,ids+j]*weight
    return ans


def comparison(a,b,model):
    sa=a['snapshots'][-1];sb=b['snapshots'][-1]
    if abs(sa['t']-sb['t'])>1e-12:raise ValueError('comparison times differ')
    ra=np.array(sa['r']);rb=np.array(sb['r']);mask=(rb>=ra[2])&(rb<=ra[-3])
    rb=rb[mask];za=np.array(sa['state']);zb=np.array(sb['state'])[:,mask]
    za0=np.array(a['snapshots'][0]['state']);zb0=np.array(b['snapshots'][0]['state'])[:,mask]
    floors=np.array([1e-10,1e-8,1e-12,model.bg0[3]*1e-8,model.initial_peak*1e-8,1e-12,1e-14,1e-8,1e-10])
    changes=zb-zb0
    scale=np.maximum(np.max(abs(changes),axis=1),floors)
    delta_error=np.max(abs(changes-interpolation(ra,za-za0,rb)),axis=1)/scale
    full_error=np.max(abs(zb-interpolation(ra,za,rb)),axis=1)/np.maximum(np.max(abs(zb),axis=1),floors)
    obs={}
    for key in ('gravity','theta'):
        aa=np.array(sa[key])[None,:];bb=np.array(sb[key])[mask]
        obs[key]=float(np.max(abs(bb-interpolation(ra,aa,rb)[0]))/max(np.max(abs(bb)),1e-12))
    return dict(change_error=delta_error.tolist(),full_state_error=full_error.tolist(),observables=obs,
        maximum=float(max(np.max(delta_error),np.max(full_error),*obs.values())),
        pass_gate=bool(max(np.max(delta_error),np.max(full_error),*obs.values())<=1e-3))


def invariants(model,t,z):
    dz,g=model.rhs(t,z,True);r=model.r;A=g['A'];N=g['N'];sig=g['sig'];c=g['c']
    adot=N*r*(-z[0]*g['divZ']+z[3]*z[1]-z[4]*z[5]-z[7]*z[8])/(2*A)
    sigdot=dz[0]/A-sig*adot
    theta=(adot*c+sig*sigdot/c)/N+(model.divergence(sig)+g['g']*sig)/A
    PtC=(model.KB*g['e']**2+2*model.C*g['e']*g['p']-model.C*g['p']**2-model.C*g['J']+2*g['K'])/2
    rho=g['rhoC']+g['rhoB'];Pr=g['PC']+g['PrB'];Pt=PtC+g['PtB']
    momentum=(z[0]*g['divZ']-z[3]*z[1]+z[4]*z[5]+z[7]*z[8])/A**2
    ricci=c*c*rho-2*c*sig*momentum+sig*sig*Pr+(-rho+Pr+2*Pt)/2
    shear=2/3*(theta-3*sig/(A*r))**2
    return dz,g,dict(theta=theta,ricci=ricci,shear=shear,adot=adot,sigdot=sigdot)


def ray_check(model,t,z):
    dz,g,v=invariants(model,t,z);r=model.r;A=g['A'];N=g['N'];sig=g['sig'];c=g['c']
    rows=[]
    for fac in (1e-7,5e-8):
        dt=fac*model.tdyn
        _,gp,vp=invariants(model,t+dt,z+dt*dz)
        _,gm,vm=invariants(model,t-dt,z-dt*dz)
        thetat=(vp['theta']-vm['theta'])/(2*dt)
        # A sigma=u, so the temporal acceleration-density factor is simply u e.
        divacc=(dz[0]*g['e']+z[0]*(gp['e']-gm['e'])/(2*dt))/(N*A)
        divacc+=(model.divergence(c*g['e'])+g['g']*c*g['e'])/A
        material=c/N*thetat+sig/A*model.derivative(v['theta'])
        residual=material+v['theta']**2/3+v['shear']+v['ricci']-divacc
        mask=model.mask;scale=max(float(np.max(abs(v['ricci'][mask]))),float(np.max(abs(material[mask]))),1e-12)
        centre=lambda f:float(np.polynomial.polynomial.polyfit(r[:4]/model.L,f[:4],2)[0])
        rows.append(dict(tangent_step=dt,relative_ray_error=float(np.max(abs(residual[mask])))/scale,
            central_theta=centre(v['theta']),central_ricci=centre(v['ricci']),
            central_divacc=centre(divacc),central_material_theta_derivative=centre(material),
            central_current_slope=centre(g['DD']/r),
            central_clock_s=centre(g['s']),
            minimum_clock_s_radius_over_L=float(r[np.argmin(g['s'])]/model.L),
            central_acceleration_fraction=centre(divacc)/centre(v['ricci'])))
    return rows


def main():
    ap=argparse.ArgumentParser();ap.add_argument('left');ap.add_argument('right');ap.add_argument('--tag',required=True)
    args=ap.parse_args();left=BASE/args.left;right=BASE/args.right
    a=json.loads(left.read_text());b=json.loads(right.read_text())
    cp_path=BASE/b['checkpoint'];cp=json.loads(cp_path.read_text())
    model=source.Polar(json.loads(source.prev.inherited.SOURCE.read_text()),b['args']['nodes'],b['args']['extent'])
    model.initial();z=np.array(cp['state']);t=cp['step']*cp['dt']
    result=dict(protocol=__doc__,comparison=comparison(a,b,model),ray=ray_check(model,t,z),
        identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(__file__),left,right,cp_path,Path(source.__file__),Path(source.prev.__file__))})
    out=BASE/('INVARIANT_CLOCK_POLAR_COMPARE_'+args.tag+'_RESULT.json')
    with out.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({k:v for k,v in result.items() if k!='protocol'},allow_nan=False),flush=True)


if __name__=='__main__':main()
