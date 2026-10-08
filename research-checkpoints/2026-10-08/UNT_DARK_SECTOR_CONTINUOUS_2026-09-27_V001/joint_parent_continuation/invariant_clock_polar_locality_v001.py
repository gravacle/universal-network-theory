"""Identical-prefix polar RHS locality in central proper time.

No evolution, model change or physical claim. BUFFER600/800 share a node
prefix. Copy the600 state bitwise into that prefix of800, leave the outer
continuation unchanged, and divide RHS by central lapse N0. In the exact
equations exterior lapse is only a common time normalization; inward mass
constraints and local stencils cannot transmit remaining outer data into
the safely interior comparison. Freeze identity gate1e-10, inverse2e-12.
Report component absolute as well as rate-normalized defects and the
original1e-3 gate. Passing is NOT trajectory convergence.

Also correct the prior Hankel auxiliary boost-contact diagnostic and
measure physical m rather than canonical cp in the saved snapshots. No
Hankel quadrature rerun. Correct the independently inferred cosmic center
clock with32/64 RK4 substeps, numerical gate1e-13 on x.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import invariant_clock_polar_source_v006 as source
import invariant_clock_finite_source_linear_v001 as linear

BASE=Path(__file__).resolve().parent
OUT=BASE/'INVARIANT_CLOCK_POLAR_LOCALITY_V001_RESULT.json'


def centre_x(model,t,count):
    h=t/count;x=0.
    for _ in range(count):
        a=model.bg(x)[5];b=model.bg(x+h*a/2)[5]
        c=model.bg(x+h*b/2)[5];d=model.bg(x+h*c)[5]
        x+=h*(a+2*b+2*c+d)/6
    return x


def physical(model,snapshot):
    f=linear.reconstruct(model,snapshot);r=np.array(snapshot['r'])
    xx=centre_x(model,snapshot['t'],64);H=model.bg(xx)[5]
    bg=np.array([model.bg(float(xx-.5*H*H*ri*ri)) for ri in r]).T
    sb,qr=bg[1],bg[7];ds=f['s']-sb
    dqr=model.eps*ds/((1+f['s'])*(1+sb)*(f['qr']+qr))
    dm=model.mpref*(ds*f['qr']+sb*dqr)
    DD=model.C*((f['Z']-model.C*f['p'])/model.KB-(1+model.lam*abs(f['p'])/np.sqrt(f['p']**2+model.bs**2))*f['p'])
    contact=f['m']*(f['q']/f['X']-1)+f['sig']*DD
    return f,dm,contact,xx


def main():
    if OUT.exists():raise FileExistsError(OUT)
    started=time.monotonic();saved=json.loads(source.prev.inherited.SOURCE.read_text())
    models=[source.Polar(saved,960,.012,.125,b) for b in (600.,800.)]
    initial=[m.initial() for m in models]
    names=['BUFFER01C','BUFFER02D'];paths=[];receipts=[];states=[]
    for name in names:
        path=BASE/f'INVARIANT_CLOCK_POLAR_SOURCE_{name}_RESULT.json'
        receipt=json.loads(path.read_text());cp_path=BASE/receipt['checkpoint']
        cp=json.loads(cp_path.read_text());paths.extend([path,cp_path]);receipts.append(receipt)
        states.append(np.array(cp['state']))
    left,right=models
    common=int(np.argmax(left.r!=right.r[:left.n]))
    if common==0:raise ValueError('missing differing outer nodes or empty shared prefix')
    if not np.array_equal(left.r[:common],right.r[:common]):raise ValueError('nonidentical prefix')
    controls=[];rows=[]
    def check(name,error,gate):
        controls.append(dict(name=name,error=float(error),tolerance=gate,passed=bool(error<=gate)))
    for label,pair,t in [('initial',initial,0.),('quarter_orbit',states,receipts[0]['snapshots'][-1]['t'])]:
        zl,zr=(z.copy() for z in pair);zr[:,:common]=zl[:,:common]
        # Identical initial metric guesses inside the common prefix prevent
        # attribution of a different starting iterate to exterior physics.
        left.Aguess=np.ones(left.n);right.Aguess=np.ones(right.n)
        fl,gl=left.rhs(t,zl,True);fr,gr=right.rhs(t,zr,True)
        il=left.lapseint@gl['g'];ir=right.lapseint@gr['g']
        n0l=np.exp(gl['lnN'][0]-il[0]);n0r=np.exp(gr['lnN'][0]-ir[0])
        count=common-4
        regimes={'core':left.r[:count]<=10*left.L,
                 'safe_prefix':np.ones(count,dtype=bool)}
        metrics={}
        for key,mask in regimes.items():
            dl=(fl[:,:count]/n0l-fr[:,:count]/n0r)[:,mask]
            scale=np.maximum(np.max(abs(fl[:,:count][:,mask]/n0l),axis=1),1e-12)
            rel=np.max(abs(dl),axis=1)/scale
            metrics[key]=dict(maximum_radius_over_L=float(np.max(left.r[:count][mask])/left.L),
                absolute=np.max(abs(dl),axis=1).tolist(),relative=rel.tolist(),
                max_metric_difference=float(np.max(abs(gl['A'][:count][mask]-gr['A'][:count][mask]))),
                max_X_difference=float(np.max(abs(gl['X'][:count][mask]-gr['X'][:count][mask]))))
            check(label+'_'+key+'_proper_time_locality',np.max(rel),1e-10)
        check(label+'_inverse',max(left.max_inverse,right.max_inverse),2e-12)
        rows.append(dict(label=label,common_nodes=common,central_lapse_ratio=n0r/n0l,
                         metrics=metrics))
    # These are inherited identical inner grids, no profile interpolation.
    material=[];early=[]
    prediction=json.loads((BASE/'INVARIANT_CLOCK_FINITE_SOURCE_LINEAR_V001_RESULT.json').read_text())
    peak=float(np.max(abs(np.array(prediction['prediction']['delta_m']))))
    for name,receipt,model in zip(names,receipts,models):
        snap=receipt['snapshots'][1]
        f,dm,contact,xc=physical(model,snap)
        xxold=float(np.interp(snap['t'],model.tbg,model.xbg))
        check(name+'_center_clock_refinement',abs(xc-centre_x(model,snap['t'],32)),1e-13)
        early.append(dict(tag=name,corrected_maximum_boost_current_contact=float(np.max(abs(contact))),
            cosmic_center_x_correction=xc-xxold,
            estimated_material_clock_correction_over_prediction=float(3*model.bg(xc)[3]*(xc-xxold)/peak),
            corrected_material_range=[float(np.min(dm)),float(np.max(dm))],
            continuum_to_discrete_source_peak_ratio=prediction['prediction']['peak']/model.initial_peak))
    for sl in receipts[0]['snapshots']:
        matches=[sr for sr in receipts[1]['snapshots'] if abs(sr['t']-sl['t'])<1e-14]
        if not matches:continue
        sr=matches[0];a,da,_,_=physical(left,sl);b,db,_,_=physical(right,sr)
        if not np.array_equal(sl['r'],sr['r']):raise ValueError('material grids differ')
        diff=b['m']-a['m'];cpdiff=np.array(sr['state'])[3]-np.array(sl['state'])[3]
        material.append(dict(t_over_tdyn=sl['t_over_tdyn'],
            max_physical_m_difference=float(np.max(abs(diff))),
            max_canonical_cp_difference=float(np.max(abs(cpdiff))),
            max_physical_contrast_600=float(np.max(abs(da))),
            max_physical_contrast_800=float(np.max(abs(db))),
            radius_of_maximum_difference_over_L=float(np.array(sl['r'])[np.argmax(abs(diff))]/left.L)))
    paths += [Path(__file__),Path(linear.__file__),Path(source.__file__),Path(source.mixed.__file__),
              source.prev.inherited.SOURCE,BASE/'INVARIANT_CLOCK_FINITE_SOURCE_LINEAR_V001_RESULT.json']
    result=dict(protocol=__doc__,elapsed_seconds=time.monotonic()-started,
                checks=controls,all_controls_passed=all(c['passed'] for c in controls),
                locality=rows,early_contact_and_clock_corrections=early,physical_material_comparison=material,
                identities={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps(result,allow_nan=False),flush=True)


if __name__=='__main__':main()
