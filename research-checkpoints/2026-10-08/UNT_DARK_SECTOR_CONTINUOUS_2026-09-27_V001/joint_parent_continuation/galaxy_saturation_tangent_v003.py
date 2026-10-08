"""V003: end-to-end complex-step Jacobian validation; physics unchanged."""
import os
import sys
sys.dont_write_bytecode = True
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
import axisymmetric_disk as disk
import disk_solver as inherited
import galaxy_density as density
import halogas_density as source

ROOT = Path(__file__).resolve().parent
A0I = inherited.A0_INT
R0 = inherited.RATIO
norm = lambda a: float(np.linalg.norm(a))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def flux(g, r):
    gi = np.asarray(g)*A0I
    z = (np.asarray(g)/r)**2
    h = gi/np.sqrt(1+z)
    mode = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    theta = np.arctan(1/mode)
    fel = h*h/4*(1.5*theta-.5*np.sin(2*theta)-np.sin(4*theta)/8)
    return (2*fel*(1+z)**-1.5+gi*z*(2+z)/(1+z)**2)/A0I


def derivatives(g, r):
    step = 1e-24
    return (np.imag(flux(np.asarray(g)+step*1j, r))/step,
            np.imag(flux(g, r*np.exp(step*1j)))/step)


def inverse(d, r):
    lo = np.zeros_like(d)
    hi = 2*(d+np.sqrt(d)+r)
    for _ in range(70):
        mid = (lo+hi)/2
        below = flux(mid, r) < d
        lo, hi = np.where(below, mid, lo), np.where(below, hi, mid)
    return (lo+hi)/2


def boundary(centres, extent, q, bottom, r=R0, order=64):
    sr = np.sqrt(extent**2+centres**2)
    nodes, weights = np.polynomial.legendre.leggauss(order)
    upper = np.log(sr)
    t = upper[:, None]*(nodes+1)/2
    g = inverse(q*np.exp(-2*t), r)
    fg, fp = derivatives(g, r)
    pr = upper/2*np.sum(np.exp(t)*g*weights, axis=-1)
    prp = upper/2*np.sum(np.exp(t)*(-fp/fg)*weights, axis=-1)
    g = inverse(q/sr**2, r)
    fg, fp = derivatives(g, r)
    tr, trp = g*centres/sr, (-fp/fg)*centres/sr
    return (pr, pr.copy(), tr, tr.copy(), bottom), (prp, prp.copy(), trp, trp.copy())


class Tangent:
    def __init__(self, phi, geometry, boundaries, bp, r=R0):
        self.phi, self.geometry, self.b, self.bp, self.r = phi, geometry, boundaries, bp, r
        e, c, w = geometry
        self.n = len(c)
        self.sep, self.frac = np.diff(c), w[:-1]/(w[:-1]+w[1:])
        self.half = w[-1]/2
        area = (e[1:]**2-e[:-1]**2)/2
        self.weight = (e[1:-1,None]*w[None,:]/self.sep[:,None],
                       area[:,None]/self.sep[None,:], e[-1]*w/self.half, area/self.half)
        n, t = self.components(phi, boundaries[0:4])
        self.normal, self.transverse = n, t
        self.g = tuple(np.sqrt(a*a+b*b) for a,b in zip(n,t))
        if not all(np.all(g > 0) for g in self.g):
            raise ValueError('Zero face field is outside this diagnostic')
        self.mu, self.mug, self.mup = [], [], []
        for g in self.g:
            fg, fp = derivatives(g, r)
            mu = flux(g, r)/g
            if np.min(mu) <= 1e-12:
                raise ValueError('Clipped constitutive face')
            self.mu.append(mu)
            self.mug.append((fg-mu)/g)
            self.mup.append(fp/g)
        self.k = tuple(wt*(mu+mg*nn*nn/gg) for wt,mu,mg,nn,gg in
                       zip(self.weight,self.mu,self.mug,n,self.g))
        kr,kz,br,bz = self.k
        self.diagonal = np.zeros_like(phi)
        self.diagonal[:-1] += kr
        self.diagonal[1:] += kr
        self.diagonal[:,:-1] += kz
        self.diagonal[:,1:] += kz
        self.diagonal[-1] += br
        self.diagonal[:,-1] += bz

    def components(self, field, bounds):
        _,c,_ = self.geometry
        gr,gz = np.gradient(field,c,c,edge_order=2)
        f = self.frac
        t = ((1-f)[:,None]*gz[:-1]+f[:,None]*gz[1:],
             (1-f)[None,:]*gr[:,:-1]+f[None,:]*gr[:,1:], bounds[2], bounds[3])
        n = (np.diff(field,axis=0)/self.sep[:,None],
             np.diff(field,axis=1)/self.sep[None,:],
             (bounds[0]-field[-1])/self.half,
             (bounds[1]-field[:,-1])/self.half)
        return n,t

    @staticmethod
    def scatter(values, shape):
        r,z,br,bz = values
        out = np.zeros(shape, dtype=np.result_type(*values))
        out[:-1] += r
        out[1:] -= r
        out[:,:-1] += z
        out[:,1:] -= z
        out[-1] += br
        out[:,-1] += bz
        return out

    def differences(self, field, bounds):
        return (field[:-1]-field[1:],field[:,:-1]-field[:,1:],
                field[-1]-bounds[0],field[:,-1]-bounds[1])

    def direct_residual(self, field, bounds):
        normal, transverse = self.components(field, bounds)
        g = tuple(np.sqrt(n*n+t*t) for n,t in zip(normal,transverse))
        mu = tuple(flux(v,self.r)/v for v in g)
        out = self.scatter(tuple(w*m*d for w,m,d in
                           zip(self.weight,mu,self.differences(field,bounds))),field.shape)
        out[:,0] += self.b[4]
        return out

    def residual(self):
        out = self.scatter(tuple(w*m*d for w,m,d in
                           zip(self.weight,self.mu,self.differences(self.phi,self.b))),self.phi.shape)
        out[:,0] += self.b[4]
        return out

    def action(self, chi, parameter=0.):
        db = tuple(parameter*v for v in self.bp)
        dn,dt = self.components(chi,db)
        dg = tuple((n*a+t*b)/g for n,t,g,a,b in
                   zip(self.normal,self.transverse,self.g,dn,dt))
        dmu = tuple(mg*gg+mp*parameter for mg,mp,gg in zip(self.mug,self.mup,dg))
        values = tuple(w*(mu*dc+dm*df) for w,mu,dm,dc,df in
                       zip(self.weight,self.mu,dmu,self.differences(chi,db),
                           self.differences(self.phi,self.b)))
        return self.scatter(values,self.phi.shape)

    def precondition_action(self, v):
        zero = (np.zeros(self.n),)*4
        return self.scatter(tuple(k*d for k,d in zip(self.k,self.differences(v,zero))),v.shape)

    def precondition(self, rhs):
        x = np.zeros_like(rhs)
        residual = rhs.copy()
        scale = norm(rhs)
        if scale == 0:
            return x
        z = residual/self.diagonal
        direction, rz = z.copy(), float(np.sum(residual*z))
        for _ in range(2000):
            ad = self.precondition_action(direction)
            denominator = float(np.sum(direction*ad))
            if denominator <= 0:
                raise ValueError('Preconditioner is not positive')
            alpha = rz/denominator
            x += alpha*direction
            residual -= alpha*ad
            if norm(residual) <= .01*scale:
                break
            z = residual/self.diagonal
            new_rz = float(np.sum(residual*z))
            direction = z+(new_rz/rz)*direction
            rz = new_rz
        return x


def solve(system,rhs):
    x = np.zeros_like(rhs)
    scale = norm(rhs)
    history = []
    if scale == 0:
        return x,True,history
    for cycle in range(10):
        residual = rhs-system.action(x)
        beta = norm(residual)
        if beta/scale <= 1e-8:
            return x,True,history
        basis, preconditioned = [residual/beta], []
        h = np.zeros((21,20))
        rhs_small = np.zeros(21)
        rhs_small[0] = beta
        for j in range(20):
            z = system.precondition(basis[j])
            preconditioned.append(z)
            w = system.action(z)
            for _ in range(2):
                for i in range(j+1):
                    hij = float(np.sum(basis[i]*w))
                    h[i,j] += hij
                    w -= hij*basis[i]
            h[j+1,j] = norm(w)
            coef = np.linalg.lstsq(h[:j+2,:j+1],rhs_small[:j+2],rcond=None)[0]
            estimate = norm(rhs_small[:j+2]-h[:j+2,:j+1]@coef)/scale
            if estimate <= 1e-9 or j == 19 or h[j+1,j] == 0:
                for value,v in zip(coef,preconditioned):
                    x += value*v
                true_error = norm(rhs-system.action(x))/scale
                history.append(dict(iterations=cycle*20+j+1,true_error=true_error))
                print(json.dumps({'solve_progress':history[-1]}),flush=True)
                if true_error <= 1e-8:
                    return x,True,history
                break
            basis.append(w/h[j+1,j])
    return x,False,history


def radial(field,centres):
    mid = field[:,0]-centres[0]*(field[:,1]-field[:,0])/(centres[1]-centres[0])
    return np.gradient(mid,centres,edge_order=2)


def run(width,n,extent):
    start = time.perf_counter()
    freeze = ROOT/'HALOGAS_FIELD_FROZEN.json'
    assert sha(freeze) == '81d01ef269d70f2699424b6576553c69944d92f51c169831c6d7a249584d694a'
    manifest = json.loads(freeze.read_text())
    for filename,digest in manifest['files'].items():
        assert sha(ROOT/filename) == digest, filename
    filename = f'HALOGAS{width}_ML36_RETAINED_V001_N{n}_L{extent}_Newton0.json'
    saved = json.loads((ROOT/filename).read_text())
    assert saved['freeze_sha256'] == sha(freeze)
    p = saved['payload']
    assert saved['payload_sha256'] == hashlib.sha256(inherited.encode(p)).hexdigest()
    assert all(p['checks'].values())
    phi = np.asarray(p['phi'])
    geometry = edges,c,_ = disk.mesh(n,extent)
    assert np.array_equal(c,np.asarray(p['radii']))
    extraction = json.loads((ROOT/'halogas_source_candidate/PLANAR_SOURCE_RESULTS.json').read_text())
    components = source.source(extraction,width,source.MULTIPLIER)
    bottom = density.bottom_flux(edges,components)
    q = density.G_KPC_KMS2_MSUN*sum(density.masses(components).values())/density.A0_KMS2_KPC
    b,bp = boundary(c,extent,q,bottom)
    system = Tangent(phi,geometry,b,bp)
    checks = []
    def check(name,error,tolerance):
        checks.append(dict(name=name,error=float(error),tolerance=tolerance,
                           passed=bool(np.isfinite(error) and error<=tolerance)))
    apply,_,rhs,clipped,_,_ = disk.operator(phi,geometry,b)
    original_residual = apply(phi)-rhs
    check('original_residual',norm(system.residual()-original_residual)/norm(rhs),1e-11)
    check('original_readout',np.max(abs(radial(phi,c)-np.asarray(p['radial_force_a0']))),1e-10)
    check('unclipped',clipped,0.)
    for i,g in enumerate(system.g):
        check(f'flux_identity_{i}',norm(flux(g,R0)-inherited.f(g))/norm(inherited.f(g)),1e-12)
    _,bp128 = boundary(c,extent,q,bottom,order=128)
    check('boundary_derivative',max(norm(a-v)/max(norm(v),1e-30) for a,v in zip(bp,bp128)),1e-7)
    zero = np.zeros_like(phi)
    rp = system.action(zero,1.)
    rr,zz = np.meshgrid(np.log1p(c),np.log1p(c),indexing='ij')
    direction = np.sin(rr)*np.cos(zz)+.3*np.cos(2*rr-zz)
    dn,dt = system.components(direction,(np.zeros(n),)*4)
    max_relative_gradient = max(float(np.max(np.hypot(a,t)/g)) for a,t,g in zip(dn,dt,system.g))
    direction *= .1/max_relative_gradient
    jv = system.action(direction)
    for step in (1e-4,5e-5):
        plus = Tangent(phi+step*direction,geometry,b,bp).residual()
        minus = Tangent(phi-step*direction,geometry,b,bp).residual()
        check(f'J_direction_{step}',norm((plus-minus)/(2*step)-jv)/norm(jv),1e-5)
        checks[-1]['role'] = 'finite_difference_roundoff_diagnostic'
        bplus,bpp = boundary(c,extent,q,bottom,R0*math.exp(step))
        bminus,bpm = boundary(c,extent,q,bottom,R0*math.exp(-step))
        plus = Tangent(phi,geometry,bplus,bpp,R0*math.exp(step)).residual()
        minus = Tangent(phi,geometry,bminus,bpm,R0*math.exp(-step)).residual()
        check(f'parameter_direction_{step}',norm((plus-minus)/(2*step)-rp)/norm(rp),1e-5)
    for step in (1e-20,1e-24):
        reference = np.imag(system.direct_residual(phi+1j*step*direction,b))/step
        check(f'full_residual_complex_J_{step}',norm(reference-jv)/norm(jv),1e-10)
    print(json.dumps({'pre_solve_checks':checks}),flush=True)
    result = dict(input=filename,input_sha256=sha(ROOT/filename),checks=checks,
                  script_sha256=sha(Path(__file__)),protocol_sha256=sha(ROOT/'GALAXY_SATURATION_TANGENT_V003.md'))
    if all(v['passed'] for v in checks if v.get('role') != 'finite_difference_roundoff_diagnostic'):
        chi,ok,history = solve(system,-rp)
        correction,correction_ok,correction_history = solve(system,-system.residual())
        check('true_tangent_residual',norm(system.action(chi)+rp)/norm(rp),1e-8)
        shifted = Tangent(phi+correction,geometry,b,bp)
        shifted_rp = shifted.action(zero,1.)
        check('shifted_base_tangent_residual',norm(shifted.action(chi)+shifted_rp)/norm(shifted_rp),1e-3)
        r_obs = np.array([v['R'] for v in p['comparison']])
        base_force = np.interp(r_obs,c,radial(phi,c))
        dv2 = r_obs*density.A0_KMS2_KPC*np.interp(r_obs,c,radial(chi,c))
        base_v = np.sqrt(r_obs*density.A0_KMS2_KPC*base_force)
        dv = dv2/(2*base_v)
        dc = r_obs*density.A0_KMS2_KPC*np.interp(r_obs,c,radial(correction,c))/(2*base_v)
        check('base_correction_velocity_flag',np.max(abs(dc))/max(np.max(abs(dv)),1e-30),.01)
        errors = np.array([v['error'] for v in p['comparison']])
        info = float(np.sum((dv/errors)**2))
        displacement = math.log(33.31908967768237/R0)
        rows = [dict(R_kpc=float(r),dv_dlnr_kms=float(v),quoted_error_kms=float(e),
                     base_correction_kms=float(d)) for r,v,e,d in zip(r_obs,dv,errors,dc)]
        result.update(solver_success=bool(ok and correction_ok),history=history,
                      base_correction_history=correction_history,rows=rows,
                      information_fixed_source_diagonal_errors=info,
                      local_curvature_scale_ln_r=1/math.sqrt(info),
                      linear_forecast_delta_ln_r=displacement,
                      linear_forecast_delta_chi2=displacement**2*info,
                      max_abs_dv_dlnr_kms=float(np.max(abs(dv))),
                      corrected_base_residual_relative_rhs=norm(shifted.residual())/norm(rhs))
    result.update(status='DIAGNOSTIC_COMPLETE' if all(v['passed'] for v in checks if v.get('role') != 'finite_difference_roundoff_diagnostic') and
                  result.get('solver_success',False) else 'UNRESOLVED_CONTROLS',
                  seconds=time.perf_counter()-start,
                  peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    target = ROOT/f'GALAXY_SATURATION_TANGENT_V003_{width}_N{n}_L{extent}.json'
    with target.open('x') as stream:
        json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','checks','history','base_correction_history')}),flush=True)


if __name__ == '__main__':
    width,n,extent = map(int,sys.argv[1:])
    if (width,n,extent) not in ((40,256,255),(40,512,255),(40,320,1023),
                               (120,256,255),(120,512,255),(120,320,1023)):
        raise SystemExit('Only predeclared saved fields are supported')
    run(width,n,extent)
