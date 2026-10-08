"""Saved-state audit: flux differences, not producer matrices or a new solve."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import tempfile
import time
import numpy as np

ROOT = Path(__file__).resolve().parent
STEM = 'SPHERICAL_GRADIENT_FORWARD_V001'
PINS = {
    STEM+'_RESULT.json': '657fa06ac5fe875a6ccef405b8061c42eb63f4715ed7878ee16f6836e10682f7',
    'spherical_gradient_forward_v001.py': '369eb81d3aec77fb85e2840b98afaa45a9426f88fe95fa8d2e88880753b75dfe',
    STEM+'.md': '5c0419a5590e91d980611bbcd0fd4199be9274a037553023ab06bb67f0352e86',
}
A0 = 1.0059833281731022e-10
GMSUN = 1.32712440018e20
PC = 648000*149597870700/math.pi
CG = 3*math.pi/8
READ = np.array([5.,10.,20.,50.])
checks = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flag(name, value):
    checks.append(dict(name=name, passed=bool(value)))


def bound(name, error, limit):
    checks.append(dict(name=name,error=float(error),limit=limit,
                       passed=bool(math.isfinite(error) and error<=limit)))


def close(name, a, b, limit=1e-11, relative=False):
    a,b=np.asarray(a),np.asarray(b)
    if a.shape!=b.shape:
        flag(name+':shape',False)
        return
    scale=np.maximum(abs(b),1e-300) if relative else np.maximum(abs(b),1.)
    bound(name,float(np.max(abs(a-b)/scale,initial=0)),limit)


def interpolate(r, values):
    # Explicit two-node log-radius interpolation, independently of np.interp.
    j=np.searchsorted(r,READ)-1
    w=np.log(READ/r[j])/np.log(r[j+1]/r[j])
    return values[j]+w*(values[j+1]-values[j])


def cubic_modes(g,alpha):
    h=np.sqrt(alpha)[:,None]*g[None,:]
    t=np.minimum(h,np.cbrt(h))
    for _ in range(24):
        t-=(t*(1+t*t)-h)/(1+3*t*t)
    return t/np.sqrt(alpha)[:,None]


def continuum_flux(g):
    h=g/CG
    t=np.minimum(h,np.cbrt(h))
    for _ in range(24):
        t-=(t*(1+t*t)-h)/(1+3*t*t)
    theta=np.arctan(1/t)
    z,w=np.polynomial.legendre.leggauss(64)
    u=theta[:,None]*(z+1)/2
    si=np.sin(u)**2
    return CG*h*h*theta*np.sum(w*2*si*(3-2*si),axis=1)/4


def main():
    started=time.perf_counter()
    target=ROOT/(STEM+'_AUDIT.json')
    if target.exists() or target.is_symlink(): raise FileExistsError(target)
    custody={name:sha(ROOT/name) for name in PINS}
    for name,pin in PINS.items(): flag('pin:'+name,custody[name]==pin)
    if not all(c['passed'] for c in checks): raise ValueError('Input custody mismatch')
    result=json.loads((ROOT/(STEM+'_RESULT.json')).read_text())
    flag('producer_status',result['status']=='QUALIFIED_DECLARED_SPHERICAL_STATES' and result['all_numerical_controls_pass'])
    flag('census_12',len(result['cases'])==12)
    flag('producer_23_controls',len(result['controls'])==23)
    for c in result['controls']:
        flag('producer:'+c['name'],c['passed'] and math.isfinite(c['error']) and 0<=c['error']<=c['limit'])
    saved_controls={c['name']:c for c in result['controls']}
    audits=[]; states={}
    for receipt in result['cases']:
        path=ROOT/receipt['filename']
        flag('case_pin:'+path.name,sha(path)==receipt['sha256'])
        c=json.loads(path.read_text()); key=f"{c['mass_Msun']}:case{receipt['index']}"
        flag(key+':custody',c['custody']==result['custody'])
        flag(key+':converged',c['status']=='converged' and c['qualified_newton'] and c['failure'] is None)
        n,ns,outer=c['spec']; mass=c['mass_Msun']; idx=receipt['index']
        flag(key+':declared_spec',c['spec']==result['inputs']['specs'][idx])
        r=np.array(c['r']); faces=np.array(c['faces']); s=np.array(c['spectral_s']); weights=np.array(c['spectral_weights'])
        u=np.array(c['mode_u']); ul=np.array(c['local_u']); boundary=np.array(c['outer_mode_u'])
        lam2=(100*PC)**2*A0/(GMSUN*mass)
        close(key+':lambda2',lam2,c['lambda_squared'],1e-14,True)
        close(key+':rM',math.sqrt(GMSUN*mass/A0),c['rM_metres'],1e-14,True)
        flag(key+':shapes',u.shape==ul.shape==(ns,len(r)) and len(faces)==len(r)+1)
        flag(key+':mesh_positive',faces[0]==0 and faces[-1]==outer and np.all(np.diff(faces)>0))
        close(key+':midpoints',r,(faces[:-1]+faces[1:])/2,0)
        expected=.1*np.expm1(np.arange(n+1)*math.log(2001)/n); expected[-1]=200.
        close(key+':original_faces',faces[:n+1],expected,2e-15,True)
        if outer>200:
            raw=.1*np.expm1(np.arange(n+1,len(faces)-1)*math.log(2001)/n)
            close(key+':extended_faces',faces[n+1:-1],raw,2e-15,True)
        nodes,w=np.polynomial.legendre.leggauss(ns)
        close(key+':spectral_nodes',s,(nodes+1)/2,0)
        close(key+':spectral_weights',weights,s*w,0)
        for power in (0,1,2,4): close(key+':spectral_moment'+str(power),sum(weights*s**power),2/(2+power),2e-14)
        alpha=1/(CG**2*s**4)
        source=(r*r+.01)**-1.5
        close(key+':source',source,c['source_over_r'],2e-15,True)
        vol=(faces[1:]**5-faces[:-1]**5)/5
        flux=np.zeros((ns,len(faces)))
        flux[:,1:-1]=faces[1:-1]**4*np.diff(u,axis=1)/np.diff(r)
        flux[:,-1]=outer**4*(boundary-u[:,-1])/(outer-r[-1])
        diffusion=-lam2*np.diff(flux,axis=1)/vol
        mean=weights@u
        cubic=alpha[:,None]*r*r*u**3
        residual=diffusion+u+cubic-source-mean
        scale=abs(diffusion)+abs(u)+abs(cubic)+abs(source)+abs(mean)+1e-30
        normalized=residual/scale
        err=float(np.max(abs(normalized)))
        bound(key+':independent_flux_residual',err,1e-9)
        close(key+':normalized_residual_array',normalized,c['normalized_residual'],2e-11)
        close(key+':scale_max',np.max(scale,axis=0),c['local_scale_max_over_modes'],2e-11,True)
        bound(key+':saved_Newton_A_correction',c['proposed_A_correction'],1e-4)
        bound(key+':saved_local_inverse',c['local_inverse_error'],1e-11)
        bound(key+':saved_cubic',c['local_cubic_forward_error'],1e-11)
        flag(key+':history_final',c['history'][-1]['proposed_A_correction']==c['proposed_A_correction'])
        flag(key+':positive_full_modes',np.all(u>0) and np.all(boundary>0))
        # Telescoping global flux checks the origin/outer signs independently.
        integrated=vol@(u+cubic-source-mean).T
        balance_scale=vol@(abs(u)+abs(cubic)+abs(source)+abs(mean)).T+abs(lam2*flux[:,-1])
        bound(key+':integrated_flux_balance',float(np.max(abs(integrated-lam2*flux[:,-1])/balance_scale)),1e-11)
        z=ul*r; gl=r*source+weights@z
        close(key+':local_forward_cubic',z+alpha[:,None]*z**3, np.broadcast_to(gl,z.shape),1e-11,True)
        localflux=(1-weights.sum())*gl+weights@(alpha[:,None]*z**3)
        close(key+':local_flux',localflux,r*source,1e-11,True)
        zb=outer*boundary; gb=outer/(outer*outer+.01)**1.5+weights@zb
        close(key+':boundary_cubic',zb+alpha*zb**3,np.full(ns,gb),1e-11,True)
        close(key+':boundary_local_flux',(1-weights.sum())*gb+weights@(alpha*zb**3),outer/(outer*outer+.01)**1.5,1e-11,True)
        difference=r*(weights@(u-ul)); delta=interpolate(r,difference)
        a=-READ**2*delta/lam2; full=interpolate(r,gl)+delta
        ro=c['readouts']
        for name,value in (('r',READ),('delta_g_over_a0',delta),('A',a),
                           ('g_local_same_interpolation_over_a0',interpolate(r,gl)),('g_full_over_a0',full),
                           ('rM_over_R',1/READ),('gradient_parameter',lam2/READ)):
            close(key+':readout:'+name,value,ro[name],1e-10, name=='delta_g_over_a0')
            close(key+':summary:'+name,ro[name],receipt['readouts'][name],0)
        gt=np.array(ro['g_local_at_exact_readout_over_a0']); zt=cubic_modes(gt,alpha)
        dt=READ/(READ**2+.01)**1.5
        close(key+':exact_readout_local_flux',(1-weights.sum())*gt+weights@(alpha[:,None]*zt**3),dt,1e-11,True)
        gc=np.array(ro['g_local_continuum_over_a0'])
        close(key+':continuum_flux',continuum_flux(gc),dt,1e-11,True)
        close(key+':spectral_discrepancy',gt/gc-1,ro['finite_spectrum_local_relative_difference'],1e-14)
        flat=READ*full-1
        exact_local_corrected=READ*(gt+delta)-1  # Descriptive interpolation-bias diagnostic only.
        g_nodes=r*source+r*mean
        range_mask=(r>=5)&(r<=50)
        node_flat=r[range_mask]*g_nodes[range_mask]-1
        audits.append(dict(mass_Msun=mass,index=idx,filename=path.name,
                           independent_max_normalized_residual=err,
                           A=a.tolist(),full_v_squared_over_flat_minus_one=flat.tolist(),
                           exact_local_plus_interpolated_difference_v_squared_minus_one=exact_local_corrected.tolist(),
                           interpolation_bias_in_v_squared=(flat-exact_local_corrected).tolist(),
                           node_flat_difference_range_5_to_50=[float(node_flat.min()),float(node_flat.max())],
                           positive_full_modes=bool(np.all(u>0))))
        states[(mass,idx)]=(c,a,r,faces)
    refinements=[]
    for mass in result['inputs']['masses_Msun']:
        for label,left,right in (('mesh',0,1),('spectral',1,2),('domain',2,3)):
            error=float(np.max(abs(states[(mass,left)][1]-states[(mass,right)][1])))
            bound(str(mass)+':'+label+'_A',error,.02)
            close(str(mass)+':saved_'+label,error,saved_controls[str(mass)+'_'+label+'_A']['error'],1e-10)
            refinements.append(dict(mass_Msun=mass,comparison=label,max_delta_A=error))
        small,large=states[(mass,2)],states[(mass,3)]
        flag(str(mass)+':domain_identical_r',np.array_equal(small[2],large[2][:len(small[2])]))
        flag(str(mass)+':domain_identical_faces',np.array_equal(small[3],large[3][:len(small[3])]))
    out=dict(status='PASS' if all(c['passed'] for c in checks) else 'FAIL',custody=custody,
             audit_source_sha256=sha(Path(__file__)),producer_controls=23,
             audit_controls=dict(total=len(checks),passed=sum(c['passed'] for c in checks)),
             controls=checks,cases=audits,refinements=refinements,elapsed_seconds=time.perf_counter()-started,
             scope='Saved static Plummer states only; no producer import, field solve, fit or observed galaxy test. Residual and refinement agreement are not a full continuum/existence certificate.')
    fd,tmp=tempfile.mkstemp(prefix=target.name+'.',suffix='.tmp',dir=ROOT)
    try:
        with os.fdopen(fd,'w') as stream:
            json.dump(out,stream,indent=2,allow_nan=False); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        os.link(tmp,target)
    finally: os.unlink(tmp)
    print(json.dumps(dict(status=out['status'],audit_controls=out['audit_controls'],producer_controls=23,
                          elapsed_seconds=out['elapsed_seconds'],result_sha256=sha(target))))
    print(json.dumps(dict(fine_cases=[c for c in audits if c['index']==3],refinements=refinements)))
    return 0 if out['status']=='PASS' else 2


if __name__=='__main__':
    raise SystemExit(main())
