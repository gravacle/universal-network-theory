"""Bounded direct AQUAL modal solve. No work on import; exclusive receipts."""
import os
for _k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS'):
    os.environ[_k] = '1'
import hashlib
import json
import math
import pathlib
import resource
import sys
import time
import numpy as np
from numpy.polynomial.legendre import leggauss, legvander, legder, legval
import disk_solver as law

ROOT = pathlib.Path(__file__).resolve().parent
STEM = 'SOLAR_AQUAL_QUADRUPOLE_V001'
A0 = 1.0059833281731022e-10
GM = 1.32712440018e20
RM = math.sqrt(GM/A0)
GEXT = 2.32e-10
SPECS = [(193,16,48,1e-4,64.), (385,24,72,1e-4,64.),
         (769,40,120,1e-4,64.), (769,40,120,5e-5,128.),
         (769,48,144,5e-5,128.)]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, obj):
    with (ROOT/name).open('x') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n')


def inputs():
    return {p.name:sha(p) for p in (pathlib.Path(__file__), ROOT/(STEM+'.md'),
                                    ROOT/'disk_solver.py', law.SHAPE_PATH)}


def deficit(g):
    """Stable 1-mu, without subtracting a near-unity high-field flux."""
    g = np.asarray(g)
    gi = g*law.A0_INT
    z = (g/law.RATIO)**2
    h = gi/np.sqrt(1+z)
    y = 2/math.sqrt(3)*np.sinh(np.arcsinh(3*math.sqrt(3)*h/2)/3)
    th = np.arctan2(1., y)
    bracket = 1.5*th-.5*np.sin(2*th)-np.sin(4*th)/8
    elastic = np.divide(h*h*bracket, 2*gi, out=np.zeros_like(gi), where=gi>0)
    return (1+z)**(-2)-elastic*(1+z)**(-1.5)


class Grid:
    def __init__(self, spec):
        n, L, nq, ri, ro = spec
        self.t = np.linspace(math.log(ri), math.log(ro), n)
        self.r = np.exp(self.t)
        self.h = self.t[1]-self.t[0]
        self.ell = np.arange(L+1)
        self.u, self.w = leggauss(nq)
        self.s = np.sqrt(1-self.u*self.u)
        self.P = legvander(self.u, L)
        self.D = np.column_stack([legval(self.u, legder(np.eye(L+1)[l]))
                                  for l in self.ell])
        self.proj = self.w[:,None]*self.P*(2*self.ell+1)[None,:]/2
        self.aproj = (self.w*self.s)[:,None]*self.D*(2*self.ell+1)[None,:]/2
        a = math.exp(-self.h/2)/self.h**2
        c = math.exp(self.h/2)/self.h**2
        self.a = np.full((n,L+1), a)
        b = np.broadcast_to(-2*np.cosh((self.ell+.5)*self.h)/self.h**2,
                            (n,L+1)).copy()
        cs = np.full_like(b, c)
        self.a[0] = 0
        b[0] = 1
        cs[0] = -np.exp(-self.ell*self.h)
        self.a[-1] = 0
        b[-1] = 1
        cs[-1] = 0
        self.b, self.c = b.copy(), cs.copy()
        self.den = b.copy()
        self.cp = np.zeros_like(b)
        self.cp[0] = cs[0]/self.den[0]
        for i in range(1,n):
            self.den[i] -= self.a[i]*self.cp[i-1]
            self.cp[i] = cs[i]/self.den[i]

    def solve(self, source, outer, inner=None):
        rhs = source.copy()
        rhs[0] = 0 if inner is None else inner
        rhs[-1] = outer
        d = rhs.copy()
        d[0] /= self.den[0]
        for i in range(1,len(d)):
            d[i] = (d[i]-self.a[i]*d[i-1])/self.den[i]
        out = d.copy()
        for i in range(len(d)-2,-1,-1):
            out[i] -= self.cp[i]*out[i+1]
        return out

    def linear_error(self, y, source, outer, inner):
        rhs = source.copy()
        rhs[0], rhs[-1] = inner, outer
        v = self.b*y
        v[1:] += self.a[1:]*y[:-1]
        v[:-1] += self.c[:-1]*y[1:]
        return float(np.max(abs(v-rhs))/max(1.,np.max(abs(rhs))))

    def source(self, psi, e, newton=False):
        dr = np.gradient(psi, self.h, axis=0, edge_order=2)@self.P.T
        du = psi@self.D.T
        rr = self.r[:,None]
        gr = rr**(-2)-e*self.u+dr/rr
        gt = e*self.s-self.s*du/rr
        dm = np.zeros_like(gr) if newton else deficit(np.hypot(gr,gt))
        de = 0. if newton else float(deficit(e))
        # Subtract divergence-free uniform B_ext before angular projection.
        br = (dm*gr+de*e*self.u)@self.proj
        theta = (dm*gt-de*e*self.s)@self.aproj
        src = self.r[:,None]*(np.gradient(br,self.h,axis=0,edge_order=2)+2*br+theta)
        return src, br, theta, float(np.min(1-dm))


def control():
    checks = []
    def check(name,value,limit):
        checks.append({'name':name,'error':float(value),'limit':limit,
                       'pass':bool(value<=limit)})
    g = np.logspace(-12,8,401)
    check('stable_deficit',np.max(abs((1-deficit(g))-law.f(g)/g)),3e-13)
    grid = Grid((97,6,32,1e-3,32.))
    check('angular_orthogonality',np.max(abs(grid.P.T@grid.proj-np.eye(7))),1e-12)
    z = np.zeros((97,7))
    src,_,_,_ = grid.source(z,GEXT/A0,newton=True)
    check('newton_zero',np.max(abs(grid.solve(src,np.zeros(7)))),1e-12)
    ex = grid.r[:,None]**grid.ell[None,:]
    y = grid.solve(z,ex[-1])
    for l in range(7):
        check('homogeneous_mode_'+str(l),np.max(abs(y[:,l]-ex[:,l]))/
              np.max(abs(ex[:,l])),1e-9)
    errors = []
    for n in (97,193,385):
        gg = Grid((n,3,20,1e-3,32.))
        r,l = gg.r[:,None],gg.ell[None,:]
        truth = r**l/(1+r)**(2*l+1)
        v = l-(2*l+1)*r/(1+r)
        dv = -(2*l+1)*r/(1+r)**2
        src = truth*(v*v+dv+v-l*(l+1))
        inner = truth[0]-np.exp(-gg.ell*gg.h)*truth[1]
        y = gg.solve(src,truth[-1],inner)
        err = np.max(abs(y-truth),axis=0)/np.max(abs(truth),axis=0)
        errors.append(err)
        check('linear_residual_'+str(n),gg.linear_error(y,src,truth[-1],inner),1e-10)
    for l in range(4):
        check('manufactured_fine_'+str(l),errors[-1][l],.003)
        for j in range(2):
            check('manufactured_ratio_'+str(l)+'_'+str(j),errors[j+1][l]/errors[j][l],.4)
    obj={'inputs':inputs(),'checks':checks,'all_pass':all(q['pass'] for q in checks),
         'manufactured_errors':[e.tolist() for e in errors]}
    save(STEM+'_TESTS.json',obj)
    print(json.dumps({'controls':len(checks),'all_pass':obj['all_pass'],
                      'failed':[q for q in checks if not q['pass']]}))


def run_case(index):
    frozen = json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())
    assert frozen['inputs']==inputs(), 'Input mutation'
    tests = json.loads((ROOT/(STEM+'_TESTS.json')).read_text())
    assert tests['all_pass'] and tests['inputs']==frozen['inputs'], 'Control custody'
    spec = SPECS[index] if index<5 else SPECS[-1]
    ext = GEXT if index<5 else (2.16e-10 if index==5 else 2.48e-10)
    if index>=5:
        assert summarize(save_receipt=False)['qualified_primary'], 'Primary unqualified'
    start=time.perf_counter()
    grid=Grid(spec)
    e=ext/A0
    mu=1-float(deficit(e))
    dh=1e-4
    Le=(math.log(1-float(deficit(e*math.exp(dh))))-
        math.log(1-float(deficit(e*math.exp(-dh)))))/(2*dh)
    outer=((1-1/(mu*np.sqrt(1+Le*(1-grid.u**2))))/grid.r[-1])@grid.proj
    psi=np.zeros((spec[0],spec[1]+1))
    history=[]
    good=0
    reason='iteration_limit'
    for k in range(240):
        src,br,theta,mumin=grid.source(psi,e)
        target=grid.solve(src,outer)
        change=float(np.max(abs(target-psi))/max(1.,np.max(abs(psi))))
        psi=.5*(psi+target)
        good=good+1 if change*.5<1e-8 else 0
        if k%10==0 or good>=3:
            history.append({'iteration':k+1,'half_update':change*.5,'mu_min':mumin})
        if good>=3:
            reason='converged'
            break
        if time.perf_counter()-start>50:
            reason='time_limit'
            break
    src,br,theta,mumin=grid.source(psi,e)
    target=grid.solve(src,outer)
    defect=float(np.max(abs(target-psi))/max(1.,np.max(abs(psi))))
    mask=(grid.r>=.003)&(grid.r<=.02)
    cs=psi[mask,2]/grid.r[mask]**2
    c2=float(np.median(cs))
    plateau=float(np.max(abs(cs-c2))/max(abs(c2),1e-5))
    integrand=(3*br[:,2]+theta[:,2])/grid.r
    integ=float(np.sum((integrand[1:]+integrand[:-1])*.5*np.diff(grid.t)))
    rawgreen=-(br[-1,2]/grid.r[-1]-br[0,2]/grid.r[0]+integ)/5
    obj={'inputs':inputs(),'index':index,'spec':spec,'external_acceleration':ext,
         'a0':A0,'shape_ratio':law.RATIO,'GM':GM,'rM':RM,'mu_external':mu,'L_external':Le,
         'status':reason,'converged':reason=='converged' and defect<3e-8,
         'iterations':k+1,'fixed_point_defect':defect,'plateau_relative':plateau,
         'c2':c2,'Q2':-3*A0/RM*c2,'finite_domain_green_c2_uncorrected':rawgreen,
         'green_note':'Finite-domain tails/boundaries omitted; descriptive only',
         'history':history,'radii':grid.r.tolist(),'psi_modes':psi.tolist(),
         'Br_modes':br.tolist(),'Theta_modes':theta.tolist(),'mu_min':mumin,
         'elapsed_seconds':time.perf_counter()-start,
         'rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    save(STEM+'_CASE_'+str(index)+'.json',obj)
    print(json.dumps({k:obj[k] for k in ('index','status','converged','iterations',
                      'fixed_point_defect','plateau_relative','Q2','elapsed_seconds')}))


def summarize(save_receipt=True):
    frozen=json.loads((ROOT/(STEM+'_FROZEN.json')).read_text())
    assert frozen['inputs']==inputs(), 'Input mutation'
    cases=[json.loads((ROOT/(STEM+'_CASE_'+str(i)+'.json')).read_text()) for i in range(5)]
    for i,c in enumerate(cases):
        assert c['inputs']==frozen['inputs'] and c['index']==i, 'Case custody'
        assert c['spec']==list(SPECS[i]) and c['external_acceleration']==GEXT
        assert c['a0']==A0 and c['shape_ratio']==law.RATIO and c['GM']==GM
    scale=max(abs(cases[-1]['c2']),1e-5)
    diffs={str(a)+'_'+str(b):abs(cases[a]['c2']-cases[b]['c2'])/scale
           for a,b in ((1,2),(2,3),(3,4))}
    qualified=(all(c['converged'] and c['plateau_relative']<.01 for c in cases)
               and all(v<.05 for v in diffs.values()))
    obj={'inputs':inputs(),'qualified_primary':qualified,'relative_changes':diffs,
         'cases':[{k:c[k] for k in ('index','spec','converged','fixed_point_defect',
                   'plateau_relative','Q2','c2','elapsed_seconds')} for c in cases],
         'Q2_primary':cases[-1]['Q2'] if qualified else None,
         'cassini_standardized_residual':(cases[-1]['Q2']-1.6e-27)/1.8e-27 if qualified else None,
         'receipt_hashes':{STEM+'_CASE_'+str(i)+'.json':sha(ROOT/(STEM+'_CASE_'+str(i)+'.json'))
                           for i in range(5)}}
    if save_receipt:
        save(STEM+'_RESULT.json',obj)
        print(json.dumps(obj))
    return obj


if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='freeze':
        save(STEM+'_FROZEN.json',{'inputs':inputs(),'specs':SPECS,'a0':A0,
                                 'shape_ratio':law.RATIO,'GM':GM,'external_accelerations':[GEXT,2.16e-10,2.48e-10]})
        print('Frozen')
    elif mode=='test':
        control()
    elif mode=='case':
        run_case(int(sys.argv[2]))
    elif mode=='summary':
        summarize()
    else:
        raise ValueError(mode)
