"""New direct string/surface material gate, exclusive results."""
import hashlib, json, math, os, resource, time
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import numpy as np

here=Path(__file__).resolve().parent
protocol=here/'TENSILE_NETWORK_GEOMETRY_GATE_V001.md'
output=here/'TENSILE_NETWORK_GEOMETRY_GATE_V001_RESULT.json'
report=here/'TENSILE_NETWORK_GEOMETRY_GATE_V001_RESULT.md'
if output.exists() or report.exists():
    raise SystemExit('Protected existing attempt; recover rather than overwrite.')
start=time.perf_counter(); checks=[]; rows=[]
def gate(name, error, tol=1e-11):
    checks.append(dict(name=name,error=float(error),tolerance=tol,
                       passed=bool(math.isfinite(float(error)) and abs(error)<=tol)))
def error(x,y):
    return abs(x-y)/max(1,abs(y))
def grid(nmu,nphi):
    mu,w=np.polynomial.legendre.leggauss(nmu)
    phi=2*math.pi*np.arange(nphi)/nphi
    ns=np.stack(np.broadcast_arrays(np.sqrt(1-mu[:,None]**2)*np.cos(phi),
                 np.sqrt(1-mu[:,None]**2)*np.sin(phi),mu[:,None]),axis=-1)
    ws=np.broadcast_to(w[:,None]/(2*nphi),(nmu,nphi))
    return ns.reshape(-1,3),ws.reshape(-1)
grids=[grid(12,24),grid(24,48)]; ident=np.eye(3)
steps=[.01,.005,.0025]
a=np.array([1.,2.,-1.]); a/=np.linalg.norm(a)
m=np.array([2.,-1.,3.]); m/=np.linalg.norm(m)
dirs=[(ident[0],ident[1]),(ident[0],ident[0]),(a,m)]
def energy(Fmat,kind,r,n,w):
    if np.linalg.det(Fmat)<=0:
        raise ValueError('Nonpositive determinant')
    operator=Fmat if kind=='string' else np.linalg.det(Fmat)*np.linalg.inv(Fmat).T
    return r+float(w@np.linalg.norm(n@operator.T,axis=1))
def rich(values):
    return (4*values[-1]-values[-2])/3

# Exact independent rational mechanics at the Hooke witness.
s=F(9,5); r=F(21,20); u=(s-1)**2/2; up=s-1; upp=1
e=r+u; pv=-s*up/3; bulk=(s*s*upp-2*s*up)/9
shear=(s*s*upp+4*s*up)/15; w=e+pv; lon=bulk+4*shear/3
actual=[e,e+3*pv,bulk,shear,w,lon/w,shear/w,(e+3*pv)/(2*e)]
expected=[F(137,100),F(-7,100),F(1,25),F(3,5),F(89,100),F(84,89),F(60,89),F(-7,274)]
for i,(x,y) in enumerate(zip(actual,expected)):
    gate('exact_hooke_'+str(i),0 if x==y else 1)
gate('exact_central_cauchy_relation',0 if shear==3*bulk/5-6*pv/5 else 1)

for gi,(n,wts) in enumerate(grids):
    gate('sphere_norm_'+str(gi),abs(float(sum(wts))-1))
    for i in range(3):
        gate('sphere_second',abs(float(wts@(n[:,i]**2))-1/3))
        gate('sphere_fourth',abs(float(wts@(n[:,i]**4))-1/5))
for kind,d in [('string',1),('surface',2)]:
    for s in [.8,1,1.8,2]:
        v=s**3; h=s**d
        pv=-d*h/3; bulk=d*(d-3)*h/9
        shear=4*h/15; lon=bulk+4*shear/3
        for r in [0,1,4]:
            ec=r+h; enthalpy=ec+pv; active=ec+3*pv
            gate('owned_enthalpy',error(enthalpy,r+(1-d/3)*h))
            gate('acoustic_positive',0 if shear>0 and lon>0 and enthalpy>0 else 1)
            gate('acoustic_causal',0 if shear<=enthalpy and lon<=enthalpy else 1)
            if kind=='string':
                gate('link_no_acceleration',error(active,r))
            else:
                gate('surface_active',error(active,r-h))
            rows.append(dict(kind=kind,s=s,r=r,energy=ec,pv=pv,bulk_v=bulk,
                    shear_v=shear,longitudinal_v=lon,enthalpy_v=enthalpy,
                    active_v=active,cT_squared=shear/enthalpy,cL_squared=lon/enthalpy,
                    acceleration=active<0,q=active/(2*ec)))
        # Derivative work uses r=1; fixed reference does not change derivatives.
        for gi,(n,wts) in enumerate(grids):
            base=energy(s*ident,kind,1,n,wts)
            gate('isotropic_energy',error(base,1+h))
            for di,(aa,mm) in enumerate(dirs):
                dy=np.outer(aa,mm); values=[]
                for step in steps:
                    eps=s*step
                    ep=energy(s*ident+eps*dy,kind,1,n,wts)
                    em=energy(s*ident-eps*dy,kind,1,n,wts)
                    values.append((ep-2*base+em)/(eps*eps))
                dot=float(aa@mm); norm=float((aa@aa)*(mm@mm))
                exact=(4*norm-2*dot*dot)/15 if kind=='surface' else (4*norm-2*dot*dot)/(15*s)
                # For a length element the coefficient is (4norm-2dot²)/15s as well.
                gate('rank_hessian_'+kind,error(rich(values),exact),2e-7)
            first=[]; second=[]
            for step in steps:
                ep=energy(s*math.exp(step/3)*ident,kind,1,n,wts)
                em=energy(s*math.exp(-step/3)*ident,kind,1,n,wts)
                first.append((ep-em)/(2*step))
                second.append((ep-2*base+em)/(step*step))
            gate('volume_pressure_'+kind,error(-rich(first),pv),2e-7)
            gate('volume_bulk_'+kind,error(rich(second)-rich(first),bulk),2e-7)
            # Volume-preserving simple shear verifies actual shear, including prestress.
            values=[]
            for step in steps:
                ep=energy(s*(ident+step*np.outer(ident[0],ident[1])),kind,1,n,wts)
                em=energy(s*(ident-step*np.outer(ident[0],ident[1])),kind,1,n,wts)
                values.append((ep-2*base+em)/(step*step))
            gate('simple_shear_'+kind,error(rich(values),shear),2e-7)

receipt=dict(utc=datetime.now(timezone.utc).isoformat(),pid=os.getpid(),ppid=os.getppid(),
        protocol_sha256=hashlib.sha256(protocol.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        passed=sum(c['passed'] for c in checks),total=len(checks),
        failed=[c for c in checks if not c['passed']],checks=checks,rows=rows,
        peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        runtime_seconds=time.perf_counter()-start,
        scope='Conditional material geometry only: no native formation, normalized galaxy response or observation qualification.')
with output.open('x') as f:
    json.dump(receipt,f,indent=2,allow_nan=False); f.write('\n')
text=f'''# Tensile geometry result V001

{receipt['passed']}/{receipt['total']} gates; {receipt['runtime_seconds']:.6f}s; peak RSS {receipt['peak_rss_bytes_macos']/2**20:.2f}MiB. Failed gates: {len(receipt['failed'])}.

Actual cold constant-tension links do not accelerate by themselves. A retained isotropic surface-tension material has p=-2rho/3, negative bulk K=-2rho/9, but positive causal acoustic modes from its derived shear mu=4rho/15: cT²=4/5,cL²=2/5. This is a conditional stable accelerating physical construction. It is not native UNT formation or a shared gravity law. The exact Hooke witness and positive-bulk central-bond class bound are retained with their assumptions.

Protocol SHA256 `{receipt['protocol_sha256']}`; source SHA256 `{receipt['source_sha256']}`. Exclusive receipt `{output.name}` has fixed controls, failures and the illustrative co-moving rest composition. Geometry, energy and pressure were not fit to observations. Next is the same native source/contact and physical formation map, with the tension energy counted once.
'''
with report.open('x') as f: f.write(text)
print(json.dumps({k:receipt[k] for k in ['passed','total','failed','runtime_seconds','peak_rss_bytes_macos']},sort_keys=True))
raise SystemExit(0 if not receipt['failed'] else 2)
