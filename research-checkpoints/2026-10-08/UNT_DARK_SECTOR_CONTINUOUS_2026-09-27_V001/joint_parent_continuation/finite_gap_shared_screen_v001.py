"""Finite-R common-state arithmetic screen; stdout-only freeze/run."""
import os
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
import sys
sys.dont_write_bytecode = True
import base64
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import zlib
import numpy as np
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE / 'FINITE_GAP_SHARED_SCREEN_V001_FROZEN.json'
OLD = 'GLOBAL_GAP_LIMIT_CALIBRATION_V001_RESULTS.json'
OLD_HASH = '11e7c8e7d9119ef02177904e462e1959e5d554eed245000f8609530b5b64b628'
CONFIG = dict(beta=.005, R=[32,128,512,2048,8192], inverse_scale_factor=1101,
              orbit_orders=[64,128], simpson_panels=1024, bisections=80,
              arithmetic_tolerance=2e-11, quadrature_tolerance=2e-8,
              c=299792458., parsec_m=3.085677581491367e16,
              exposed_a0_m_s2=1.2e-10, expected_rows=360)

def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def inputs():
    files, seen = {}, set()
    def add(p, expected=None):
        p=p.resolve(strict=True); p.relative_to(ROOT)
        h=sha(p)
        if expected is not None and h!=expected:
            raise RuntimeError('Input differs: '+str(p))
        files[str(p.relative_to(ROOT))]=h
        return p
    def manifest(p):
        p=add(p)
        if p in seen: return
        seen.add(p)
        for name,h in json.loads(p.read_text())['files'].items():
            q=Path(name)
            if not q.is_absolute():
                possibilities={v.resolve() for v in (ROOT/q,p.parent/q) if v.is_file()}
                if len(possibilities)!=1: raise RuntimeError('Ambiguous member: '+name)
                q=possibilities.pop()
            q=add(q,h)
            if q.name.endswith('_FROZEN.json'): manifest(q)
    v=json.loads(add(HERE/OLD,OLD_HASH).read_text())
    frozen=HERE/OLD.replace('_RESULTS.json','_FROZEN.json'); manifest(frozen)
    p=v['payload']
    if v['freeze_sha256']!=sha(frozen) or v['payload_sha256']!=hashlib.sha256(encode(p)).hexdigest():
        raise RuntimeError('Inherited wrapper differs')
    if p['status']!='COMPLETE' or p['failures'] or len(p['rows'])!=72:
        raise RuntimeError('Inherited status/census differs')
    for name in (Path(__file__).name,'FINITE_GAP_SHARED_SCREEN_PROTOCOL_V001.md',
                 'MACROSCOPIC_ALPHA_ONE_GALAXY_BVP_V001.md',
                 'CENTRAL_STATIC_RESPONSE_PROTOCOL_V001.md',
                 'central_static_response_v001.py',
                 'GALACTIC_SMOOTHNESS_AND_COLD_HISTORY_CONSTRAINT_V001.md'):
        add(HERE/name)
    return p,dict(configuration=CONFIG,files=files)

def rule(n):
    if n:
        z,w=leggauss(n); t=(z+1)*math.pi/4; w=w*math.pi/4
    else:
        n=CONFIG['simpson_panels']; t=np.linspace(0,math.pi/2,n+1)
        w=np.ones(n+1);w[1:-1:2]=4;w[2:-1:2]=2;w*=math.pi/(6*n)
    return w,np.sin(t)**2,np.cos(t)**2

def orbit(R,b2,quadrature,u=1.):
    w,s,c=quadrature;q=R*R+u*b2*(1+s)/2
    m=w/np.sqrt(q);j=float(m.sum());ell=float((w*(1+s)/q**1.5).sum())
    om=math.pi/(2*j);I=2/math.pi*b2*float((w*c*np.sqrt(q)).sum())
    e=R*R*b2/2+u*b2*b2/4
    p=u*b2*b2/4*float((m*s*s).sum())/j
    return dict(I=I,omega=om,e=e,p=p,mean2=b2*float((m*s).sum())/j,
                eII=om*om*u*ell/(2*j*(R*R+u*b2)))

def cubic(d,h):
    return 2*d/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*h/(2*d*d))/3)

def cubic_oracle(d,h):
    lo=0.;hi=min(h/d,(d*h)**(1/3))
    for _ in range(80):
        v=(lo+hi)/2
        if v*(d*d+v*v)<d*h:lo=v
        else:hi=v
    return (lo+hi)/2

def endpoint(ds,ws,h):
    ys=[cubic(d,h) for d in ds]
    return math.fsum(w*(d*d*y*y/2+3*y**4/4) for d,w,y in zip(ds,ws,ys)),ys

def solve_endpoint(ds,ws,target,start):
    lo=0.;hi=start
    for _ in range(64):
        if endpoint(ds,ws,hi)[0]>=target:break
        hi*=2
    else:raise RuntimeError('No endpoint bracket')
    for _ in range(80):
        mid=(lo+hi)/2
        if endpoint(ds,ws,mid)[0]<target:lo=mid
        else:hi=mid
    return (lo+hi)/2

def compressed_orbit(R,I,A,q):
    target=I*A**3/R**3
    lo=0.;hi=2*target
    for _ in range(80):
        r=(lo+hi)/2
        if orbit(1.,r,q)['I']<target:lo=r
        else:hi=r
    r=(lo+hi)/2
    return orbit(R,R*R*r,q)

def run(old):
    started=time.perf_counter();counts={};maxima={};failures=[];rows=[]
    def check(name,a,b,scale=None,tolerance=None):
        scale=max(abs(a),abs(b),1e-300) if scale is None else max(abs(scale),1e-300)
        error=abs(a-b)/scale;tol=CONFIG['arithmetic_tolerance'] if tolerance is None else tolerance
        counts[name]=counts.get(name,0)+1;maxima[name]=max(maxima.get(name,0),error)
        if not math.isfinite(error) or error>tol:
            failures.append(dict(check=name,error=error,tolerance=tol,row=len(rows)))
    qs=[rule(n) for n in (64,128,None)]; primary=qs[1]
    for R in (1.,32.,8192.):
        empty=orbit(R,0,primary);check('empty_eII',empty['eII'],3/(4*R*R))
        harm=orbit(R,1,primary,u=0);check('harmonic_omega',harm['omega'],R)
        check('harmonic_eII',harm['eII'],0,1)
    quart=orbit(0.,1,primary)
    check('quartic_pressure',quart['p'],quart['e']/3)
    check('quartic_eII',quart['eII'],quart['omega']/(3*quart['I']))
    beta=CONFIG['beta'];c=CONFIG['c'];A=CONFIG['inverse_scale_factor']
    for oldrow in old['rows']:
        si=oldrow['spectrum_index'];ri=oldrow['reference'];ref=old['references'][ri]
        spec=old['spectra'][si]['spectrum'];kb=math.fsum(spec['weights'])+beta
        gs=CONFIG['exposed_a0_m_s2']/(16*kb/(3*math.pi));H=ref['H0_s_inverse']
        E=3*kb*ref['Omega_exc']*(c*H)**2/(2*gs*gs);e=E/beta
        check('inherited_energy',E,oldrow['E_required']);check('inherited_gstar',gs,oldrow['gstar_m_s2'])
        for R in CONFIG['R']:
            b2=4*e/(R*R+math.sqrt(R**4+4*e));o=orbit(R,b2,primary)
            for label,q in [('GL64',qs[0]),('Simpson1024',qs[2])]:
                other=orbit(R,b2,q)
                for k in ('I','omega','eII','p','mean2'):
                    check(label+'_'+k,other[k],o[k],tolerance=CONFIG['quadrature_tolerance'])
            check('energy',o['e'],e)
            check('action_pressure',o['I']*o['omega'],e+o['p'])
            check('virial',R*R*o['mean2']+3*o['p'],e)
            qdef=3*(e+o['p'])/(R**4+4*e)
            chi=R*R*(R*R+o['mean2'])/(R**4+4*e)
            check('contact_sum',qdef+chi,1.)
            ci=o['I']*o['eII']/o['omega'];K=beta*qdef
            J=beta*(o['omega']**2/o['eII']+3*o['I']*o['omega'])
            ratio=K/J;other_ratio=3*ci/((R**4+4*e)*(1+3*ci))
            check('static_ratio',ratio,other_ratio)
            length=c*c/gs*math.sqrt(ratio);x=e/R**4
            cosmic=2*(beta/kb)*x*ci/(ref['Omega_exc']*(1+4*x)*(1+3*ci))
            check('cosmic_length_units',(H*length/c)**2,cosmic)
            ds=spec['delta']+[R];ws=spec['weights']+[beta]
            target=E*ref['Omega_Lambda']/ref['Omega_exc']
            S=solve_endpoint(ds,ws,target,oldrow['S']);du,ys=endpoint(ds,ws,S)
            check('vacuum_endpoint',du,target)
            elastic=math.fsum(w*((S-d*y)**2/2+y**4/4) for d,w,y in zip(ds,ws,ys))
            check('finite_contact_ledger',du+elastic,kb*S*S/2)
            for d,y in zip(ds,ys):
                check('cubic_residual',y*(d*d+y*y),d*S)
                check('cubic_independent',y,cubic_oracle(d,S))
            check('finite_S_ordering',min(S-oldrow['S'],0),0,max(1,S))
            early=compressed_orbit(R,o['I'],A,primary)
            check('early_action',early['I'],o['I']*A**3)
            early64=compressed_orbit(R,o['I'],A,qs[0])
            early_sim=compressed_orbit(R,o['I'],A,qs[2])
            for label,other in [('GL64',early64),('Simpson1024',early_sim)]:
                for k in ('e','p','omega'):
                    check('early_'+label+'_'+k,other[k],early[k],tolerance=CONFIG['quadrature_tolerance'])
            check('early_action_pressure',early['I']*early['omega'],early['e']+early['p'])
            check('cold_dust_energy_floor',min(early['e']-e*A**3,0),0,e*A**3)
            rows.append(dict(spectrum_index=si,reference=ri,R=R,E=E,gstar=gs,S=S,
                S_infinity=oldrow['S'],S_minus_limit=S-oldrow['S'],DeltaU=du,
                I=o['I'],omega=o['omega'],pressure=beta*o['p'],eII=o['eII'],
                w=o['p']/e,cI2=ci,phase_linear_potential_scale=ci,
                q_hard=qdef,K0=K,mu0=K/kb,J_static=J,
                static_length_pc=length/CONFIG['parsec_m'],
                cold_length_pc=(1.5*c*c/gs*math.sqrt(e)/R**4)/CONFIG['parsec_m'],
                delta_deceleration=1.5*ref['Omega_exc']*o['p']/e,
                early_w=early['p']/early['e'],early_E=beta*early['e'],
                early_I=early['I'],early_omega=early['omega'],early_p=early['p'],
                early_eII=early['eII'],early_action_target=o['I']*A**3,
                early_cI2=early['I']*early['eII']/early['omega'],
                early_dust_ratio=early['e']/(e*A**3)))
    check('census',len(rows),CONFIG['expected_rows'])
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
    ranges=[]
    for R in CONFIG['R']:
        subset=[r for r in rows if r['R']==R]
        keys=('S','S_minus_limit','w','cI2','mu0','static_length_pc','early_w','early_dust_ratio','delta_deceleration')
        ranges.append(dict(R=R,rows=len(subset),ranges={k:[min(r[k] for r in subset),max(r[k] for r in subset)] for k in keys}))
    return dict(status='COMPLETE' if not failures else 'FAILED_NUMERICAL_CONTROLS',
        configuration=CONFIG,rows=rows,ranges=ranges,counts=counts,maxima=maxima,failures=failures,
        seconds=time.perf_counter()-started,peak_self_rss_bytes=int(peak),
        scope='New scalar macroscopic same-energy designs; not actual pulses, galaxy solutions, selected halo radii or observational acceptance')

def main():
    old,snapshot=inputs()
    if sys.argv[1:]==['freeze']:
        print(encode(snapshot).decode());return
    if sys.argv[1:]!=['run']:raise RuntimeError('Use freeze or run')
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Prospective freeze differs')
    p=run(old);raw=encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(p)).hexdigest(),payload=p))
    print(encode(dict(encoding='zlib_base64_canonical_json',raw_sha256=hashlib.sha256(raw).hexdigest(),
        raw_bytes=len(raw),data=base64.b64encode(zlib.compress(raw,9)).decode(),
        summary={k:p[k] for k in ('status','ranges','counts','maxima','failures','seconds','peak_self_rss_bytes')})).decode())
    if p['status']!='COMPLETE':raise SystemExit(2)

if __name__=='__main__':main()
