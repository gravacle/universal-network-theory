"""Frozen prospective bounded coupled radiation-memory horizon test.
Root alone executes after full source/protocol peer review.
No old main, calibration, trajectory or physical numerical preflight is imported.
"""
from pathlib import Path
import ast
import hashlib
import json
import math
import os
import time
import argparse
import traceback
from datetime import datetime,timezone
from functools import lru_cache
import numpy as np

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_GALAXY_HORIZON_STABLE_Y_GAUSS_V001'
PENDING_COMPLETED_INPUTS=False
K=10.
AI=3e-8
START_AI=2e-8
AF=1e-6
CURVATURE=1e-5
KB,C,CBAR=.02,1.98,.99
MPC=3.0856775814913673e22
CP=299792458.
TRIALS=[('BASE',512,32,1,AI),('TIME',1024,32,1,AI),
        ('FINE',2048,32,1,AI),('MODES',2048,64,1,AI),
        ('SOURCE',2048,32,2,AI),('START',2176,32,1,START_AI)]
OMEGAS=(.1,1.,10.,100.)
EARLY_SOURCE_SHA='a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07'
KERNEL_SOURCE_SHA='dc7885ee0349145f05a7e18bf9ce48bf257626ebbc4bd48ebc366791fe456db2'
KERNEL_RESULT_SHA='b541b0a5e3f2ea1827f166907f96e9b76bf2d2ad4c6366c3a0efbf15a7661530'
OPTICAL_KERNEL_SHA='b43b9def6b0eeaafd12f5f947b8dd77cdf02ab60838951f799fb0bc043bc9721'
CHECKED_HELPERS=('background','Thermal','Layout','coefficients','rates','stage_matrix','snapshot')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_declared_helpers():
    """Root-run definition-only loader; exact parent bodies, no top-level initializers."""
    p=BASE/'constrained_u_clock_gradient_early_transfer_v004.py'
    if sha(p)!=EARLY_SOURCE_SHA:raise AssertionError('Physical matrix parent bytes')
    tree=ast.parse(p.read_text());nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in CHECKED_HELPERS]
    if {n.name for n in nodes}!=set(CHECKED_HELPERS):raise AssertionError('Exact declared helper set')
    namespace=dict(BASE=BASE,np=np,math=math,json=json,MPC=MPC,CP=CP,KB=KB,C=C,CBAR=CBAR,K=K,CURVATURE=CURVATURE)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<declared-definitions>','exec'),namespace)
    return namespace

def legendre(l,mu):
    if l==0:return np.ones_like(mu)
    if l==1:return mu
    p0=np.ones_like(mu);p1=mu
    for n in range(1,l):p0,p1=p1,((2*n+1)*mu*p1-n*p0)/(n+1)
    return p1

def bessel(l,r,x):
    """General low-moment derivative, including transported diagnostic l3/l4."""
    x=np.asarray(x,float);v=abs(x);out=np.zeros_like(v);small=v<4;t=v[small]
    coef=1./math.prod(range(1,2*l+2,2));value=np.zeros_like(t)
    for m in range(52):
        p=l+2*m
        if p>=r:value+=coef*(math.prod(range(p-r+1,p+1)) if r else 1)*t**(p-r)
        coef/=-2*(m+1)*(2*l+2*m+3)
    out[small]=value
    pairs=[({-1:1.},{}),({-2:1.},{-1:-1.})]
    for n in range(1,l):
        a,b=pairs[-1];a0,b0=pairs[-2];sa={p-1:(2*n+1)*z for p,z in a.items()};co={p-1:(2*n+1)*z for p,z in b.items()}
        for p,z in a0.items():sa[p]=sa.get(p,0.)-z
        for p,z in b0.items():co[p]=co.get(p,0.)-z
        pairs.append((sa,co))
    s,c=pairs[l]
    for _ in range(r):
        sn={};cn={}
        for p,a in s.items():sn[p-1]=sn.get(p-1,0.)+p*a;cn[p]=cn.get(p,0.)+a
        for p,a in c.items():cn[p-1]=cn.get(p-1,0.)+p*a;sn[p]=sn.get(p,0.)-a
        s,c=sn,cn
    t=v[~small];out[~small]=sum(a*t**p for p,a in s.items())*np.sin(t)+sum(a*t**p for p,a in c.items())*np.cos(t)
    return out*np.where(x<0,(-1)**(l+r),1)

def si_vector(x):
    """Only the bounded horizon panel |k Deltaeta|<8 is admitted here."""
    x=np.asarray(x,float)
    if np.any(abs(x)>8):raise ArithmeticError('Declared horizon-memory primitive range exceeded')
    term=x.copy();total=term.copy()
    for m in range(1,52):
        term*=-x*x*(2*m-1)/((2*m+1)*(2*m)*(2*m+1));total+=term
    return total

def primitive(l,x):
    x=np.asarray(x,float);si=si_vector(x)
    if l==0:return si
    if l==1:return -bessel(0,0,x)
    if l==2:return si/2-1.5*bessel(1,0,x)
    if l==3:return -2*bessel(0,0,x)/3-5*bessel(2,0,x)/3
    if l==4:return 3*si/8-9*bessel(1,0,x)/8-7*bessel(3,0,x)/4
    raise ValueError('Only full low-moment diagnostic l0..4')

def initial_transport(coefficients,x,l,order=128):
    """Complete supplied initial angular polynomial, not an isotropic reset."""
    mu,w=np.polynomial.legendre.leggauss(order);angular=np.zeros_like(mu,dtype=complex)
    for m,f in enumerate(coefficients):angular+=(-1j)**m*(2*m+1)*f*legendre(m,mu)
    return (1j**l/2)*np.exp(-1j*np.asarray(x)[...,None]*mu)@(w*legendre(l,mu)*angular)

@lru_cache(None)
def gauss(order):return np.polynomial.legendre.leggauss(order)

def equilibrate(matrix,rhs):
    """Six fixed positive diagonal row/column rescalings, no operator alteration."""
    a=matrix.copy();b=rhs.copy();columns=np.ones(len(rhs))
    for _ in range(6):
        rr=np.sqrt(np.maximum(np.max(abs(a),axis=1),np.finfo(float).tiny))
        a/=rr[:,None];b/=rr
        cc=np.sqrt(np.maximum(np.max(abs(a),axis=0),np.finfo(float).tiny))
        a/=cc[None,:];columns/=cc
    return a,b,columns

def regular_seed(ai,fixed,lay,therm,snodes,weights,omega,helpers):
    """Fixed asymptotic curvature, radiation x2/x4, matter/opacity a jet, native a6."""
    a=ai;bg=helpers['background'](math.log(a),fixed);h=bg['h'];q0=K*CP/(1000*fixed['Hunit']);q=q0/a
    R=1-fixed['fgamma'];hr=math.sqrt(fixed['OR']/fixed['rG']);A=CURVATURE/(1.5+2*R/5)
    f=(56*R*R+10*R-525)/(630*(25+2*R));g=-(56*R*R+580*R+525)/(630*(25+2*R))
    m=(fixed['OB']+fixed['OA']*math.sqrt(1+fixed['eps'])*fixed['d0'])/fixed['OR']
    g0=therm.at(a)['g']*a**3
    phi1=m*A*5*(8*R-3)/(16*(15+2*R))-12*(1-R)*hr*A/((15+2*R)*g0)
    psi1=-m*A*(15+16*R)/(16*(15+2*R))+4*(1-R)*hr*A/((15+2*R)*g0)
    xi=q0*a/hr*(1-m*a/4);eta0=xi/K
    phi=A*(1+f*xi*xi)+phi1*a;psi=A*(1+2*R/5+g*xi*xi)+psi1*a
    tgamma=(f+g)/3-1/36;tnu=tgamma-1/45
    # Velocities are converted theta/k=q*u, with baryons Thomson-locked.
    V=A*a*a/(2*hr)+A*f*xi**3/(4*q)+(phi1-m*A/2)*a**3/(3*hr)
    ug=A*a*a/(2*hr)+A*tgamma*xi**3/q+(phi1-m*A/2)*a**3/(3*hr)
    un=A*a*a/(2*hr)+A*tnu*xi**3/q+(phi1-m*A/2)*a**3/(3*hr)
    dr=A*(-2+(4*g-1/3)*xi*xi)+4*psi1*a;dc=.75*dr
    y=np.zeros(lay.n);y[:9]=[psi,dc,ug,dr,ug,dr,un,dc,V]
    y[lay.fn[2]]=2*A*q0*q0*a*a/(15*hr*hr)+(q0*q0/(hr*hr))*(8*phi1/135-2*m*A/27)*a**3+A*(2*tnu/15-1/350)*xi**4
    y[lay.fn[3]]=2*A*xi**3/105;y[lay.fn[4]]=2*A*xi**4/945
    th=therm.at(a);y[lay.fg[2]]=32*q*q*ug/(45*th['g'])
    y[lay.pol[0]]=1.25*y[lay.fg[2]];y[lay.pol[2]]=.25*y[lay.fg[2]]
    y[lay.pol[1]]=q*y[lay.fg[2]]/(4*th['g'])
    for l in (3,4):
        y[lay.fg[l]]=q*l*y[lay.fg[l-1]]/((2*l+1)*th['g'])
        y[lay.pol[l]]=q*l*y[lay.pol[l-1]]/((2*l+1)*th['g'])
    norm=1/fixed['eps']-math.log1p(1/fixed['eps']);c3=1/(math.sqrt(1+fixed['eps'])*norm*fixed['d0'])
    Gamma2=A*(3*g-.25+.75*f)*(q0/hr)**2;Qc=fixed['Q0_over_Hstar']*math.sqrt(1+fixed['eps'])
    alpha=omega**2*float(weights@snodes**2);Delta0=alpha+C*Qc*Qc/KB
    sigma2=6*hr*Qc*q0*c3*Gamma2/Delta0
    z6=omega**2*snodes**2*sigma2/(42*hr*hr)
    y[lay.z]=z6*a**6;y[lay.zd]=6*hr*z6*a**4
    # Preserve the asymptotic amplitude; finite-start normal correction adds no
    # relative density entropy and does not reset native or radiation velocities.
    rg=bg['r']*fixed['fgamma'];rn=bg['r']*(1-fixed['fgamma'])
    y[0]=phi+2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2
    ff=helpers['coefficients'](math.log(a),y,fixed,lay,therm,snodes,weights,omega)
    P=KB*q*ff['ncalc']/2+CBAR*ff['Z']
    raw=q*q*y[0]+3*h*ff['mom']+bg['b']*y[1]+rg*y[3]+rn*y[5]+bg['w']*y[7]-q*P
    shift=-raw/(bg['b']+4*bg['r']/3+bg['w']+KB*q*q*bg['cs']/2)
    y[1]+=shift;y[7]+=shift;y[3]+=4*shift/3;y[5]+=4*shift/3
    return y,eta0,dict(asymptotic_curvature=CURVATURE,A=A,x=xi,m=m,phi1=phi1,psi1=psi1,
        sigma2=sigma2,native_z6=z6.tolist(),finite_normal_shift=shift,
        finite_curvature=float(y[0]+h*y[8]),scope='Regular limiting jets plus exact finite normal/shear; START tests the retained higher-order transient')

def conformal_grid(xs,fixed,helpers,order):
    u,w=gauss(order);out=[0.]
    for a,b in zip(xs[:-1],xs[1:]):
        points=(a+b)/2+(b-a)*u/2
        integral=(b-a)*float(np.dot(w,[CP/(1000*fixed['Hunit']*math.exp(x)*helpers['background'](float(x),fixed)['h']) for x in points]))/2
        out.append(out[-1]+integral)
    return np.array(out)

def compton_rate(a,fixed,therm):
    gamma=8*6.6524587321e-29*7.5657e-16*(therm.T0/a)**4/(3*9.1093837015e-31*CP)*therm.xfull/(1+therm.fHe+therm.xfull)
    return gamma/(fixed['Hunit']*1000/MPC)

def extra_source_bound(snap,fixed,therm,temperature_difference_bound=0.,background_lag_bound=0.):
    """Cold fixture: instantaneous nonrel fully-ionized gas contacts, not state error."""
    a=snap['a'];bg=snap['background'];y=snap['state'];th=therm.at(a)
    hs=fixed['Hunit']*1000/MPC;rho_star=hs*hs/(4*math.pi*.99*6.67430e-11)
    pressure=therm.nH/a**3*(2+3*therm.fHe)*1.380649e-23*therm.T0/a
    theta=pressure/(bg['b']*rho_star*CP**2)
    envelope=abs(y[1])+abs(y[3])/4+temperature_difference_bound
    signed=theta*(y[1]+y[3]/4)
    force_envelope=abs(snap['Phi'])+abs(bg['h']*y[2])+abs(th['g']*y[4]/(3*bg['b']/(4*bg['r']*fixed['fgamma'])))+abs(th['g']*y[2]/(3*bg['b']/(4*bg['r']*fixed['fgamma'])))
    force_floor=CURVATURE*1e-8
    # H/Gamma is monotone increasing in this positive radiation/matter/clock
    # background: d log H/d log a >= -2, while Gamma_C scales a^-4.
    return dict(theta=theta,signed_pressure_rest=signed,pressure_rest_bound=theta*envelope,
        energy_rest_bound=1.5*theta*envelope,enthalpy_rest_bound=2.5*theta*envelope,
        background_energy_rest=1.5*theta,background_enthalpy_rest=2.5*theta,
        pressure_gradient_bound=(K*CP/(1000*fixed['Hunit']*a))**2*theta*envelope,
        omitted_velocity_source_ratio=theta*envelope/max(force_envelope,force_floor),
        momentum_loading_relative=2.5*theta,compton_background_lag_barrier=background_lag_bound,temperature_difference_bound=temperature_difference_bound,
        scope='Fixed composition; initial Tb=Tgamma and deltaTb/Tb=deltaGamma/4, positive Compton lag barriers on declared source panels; no global propagated-error certificate')

def json_builtin(value):
    if isinstance(value,dict):return {str(k):json_builtin(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [json_builtin(v) for v in value]
    if isinstance(value,np.ndarray):return json_builtin(value.tolist())
    if isinstance(value,np.generic):return value.item()
    return value

def seal(path,h):
    p=Path(path).resolve()
    if not (p.is_relative_to(BASE.parent.parent) or (p==Path('/usr/bin/clang').resolve() and h==COMPILER_SHA)):raise AssertionError('Owned input path')
    if sha(p)!=h:raise AssertionError('Input hash '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=h:raise AssertionError('Conflicting input seal')
    SEALS[str(p)]=h

def recheck():
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed immutable input/output '+p)
    if sha(__file__)!=SOURCE_SHA:raise AssertionError('Source changed')

def write(name,obj):
    data=(json.dumps(json_builtin(obj),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    p=BASE/name
    with p.open('xb') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p.resolve())]=sha(p);return sha(p)

def journal(event,**fields):
    row=dict(time=datetime.now(timezone.utc).isoformat(),event=event,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**fields)
    data=json.dumps(json_builtin(row),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(data)

def finite_tree(value):
    if isinstance(value,dict):
        if any(type(k) is not str for k in value):raise AssertionError('Canonical dictionary keys')
        for v in value.values():finite_tree(v)
    elif isinstance(value,list):
        for v in value:finite_tree(v)
    elif type(value) is float:
        if not math.isfinite(value):raise AssertionError('Nonfinite full checkpoint tree')
    elif value is not None and type(value) not in (str,int,bool):raise AssertionError('Noncanonical checkpoint type')

def validate_journal(lineage):
    events=[json.loads(s) for s in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    if not events or events[0]['event']!='OWNER_START':raise AssertionError('No original owner')
    for event in events:
        if event.get('owner')!='root' or type(event.get('pid')) is not int or event['pid']<=0 or event.get('source_sha256')!=SOURCE_SHA or event.get('manifest_sha256')!=MANIFEST_SHA:raise AssertionError('Full journal source/root/PID identity')
        if event['event'] not in ['OWNER_START','OWNER_RESUME','CHECKPOINT']:raise AssertionError('Unowned or already closed journal')
    epoch=None
    for event in events:
        if event['event'] in ('OWNER_START','OWNER_RESUME'):epoch=event['pid']
        if event['event']=='CHECKPOINT':
            if event['pid']!=epoch:raise AssertionError('Checkpoint root owner epoch mismatch')
            spec=next((r for r in TRIALS if r[0]==event['trial']),None)
            if spec is None or event['nstep'] not in sorted(set(list(range(0,spec[1]+1,128))+[spec[1]])):raise AssertionError('Checkpoint trial/census')
            pn=STEM+'_'+event['trial']+'_CP_'+str(event['nstep']).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
            if sha(BASE/pn)!=event['payload_sha256'] or sha(BASE/cn)!=event['commit_sha256']:raise AssertionError('Checkpoint journal byte identity')
    commits=list(BASE.glob(STEM+'_*_CP_*_COMMIT.json'))
    if sum(e['event']=='CHECKPOINT' for e in events)!=len(commits):raise AssertionError('Complete journal checkpoint census')
    actual=[(e['trial'],e['nstep']) for e in events if e['event']=='CHECKPOINT']
    expected=[(spec[0],i) for spec in TRIALS for i in sorted(set(list(range(0,spec[1]+1,128))+[spec[1]]))]
    if actual!=expected[:len(actual)]:raise AssertionError('Exact global ordered checkpoint prefix')

def refuse_closed_prefix():
    if any((BASE/(STEM+s)).exists() for s in ['_RESULT.json','_REPORT.md','_RECEIPT.json']) or list(BASE.glob(STEM+'_FAILED*')):raise FileExistsError('Protected closed attempt; no error artifact mutation')

def to_chart(raw,bg,fixed):
    """Invertible moving coordinates; retain the complete supplied physical state."""
    y=np.array(raw,copy=True);h=bg['h'];B=bg['a']**3*bg['b'];G=bg['a']**3*4*bg['r']*fixed['fgamma']/3
    wb=raw[2]-raw[8];wg=raw[4]-raw[8]
    y[0]=raw[0]+h*raw[8];y[1]=raw[1]+3*h*raw[8]
    y[2]=(B*wb+G*wg)/(B+G);y[3]=raw[3]+4*h*raw[8];y[4]=wg-wb
    y[5]=raw[5]+4*h*raw[8];y[6]=raw[6]-raw[8];y[7]=raw[7]+3*h*raw[8]
    return y

def to_raw(y,bg,fixed):
    raw=np.array(y,copy=True);h=bg['h'];B=bg['a']**3*bg['b'];G=bg['a']**3*4*bg['r']*fixed['fgamma']/3
    wb=y[2]-G*y[4]/(B+G);wg=y[2]+B*y[4]/(B+G)
    raw[0]=y[0]-h*y[8];raw[1]=y[1]-3*h*y[8];raw[2]=y[8]+wb
    raw[3]=y[3]-4*h*y[8];raw[4]=y[8]+wg;raw[5]=y[5]-4*h*y[8];raw[6]=y[8]+y[6];raw[7]=y[7]-3*h*y[8]
    return raw

def chart_coefficients(x,y,fixed,lay,therm,snodes,weights,omega,helpers,n_override=None):
    bg=helpers['background'](x,fixed);h,b,r,w,c,Q=(bg[k] for k in ('h','b','r','w','cs','Q'))
    rg=r*fixed['fgamma'];rn=r*(1-fixed['fgamma']);q=K*CP/(1000*fixed['Hunit']*bg['a']);th=therm.at(bg['a']);g=th['g'];rb=3*b/(4*rg)
    B=bg['a']**3*b;G=bg['a']**3*4*rg/3;U,W=y[2],y[4];wb=U-G*W/(B+G);wg=U+B*W/(B+G)
    R,Gb,Gg,Gn,wn,Gamma,V=(y[i] for i in (0,1,3,5,6,7,8))
    psi=R-h*V;phi=psi-2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2
    S=b*wb+4*rg*wg/3+4*rn*wn/3;Rd=S+h*c*Gamma
    Z=weights@y[lay.z];Zd=weights@y[lay.zd];R1=omega**2*(weights*snodes**2)@y[lay.z]
    alpha=omega**2*float(weights@snodes**2);L=Q*q;Ld=-h*(1+3*c)*L
    Ldd=(h*h*(1+3*c)**2-bg['h_dt']*(1+3*c)-3*h*bg['cs_dt'])*L
    v=Z/L;vd=(Zd-Ld*v)/L;ncalc=vd-c*Gamma;n=ncalc if n_override is None else n_override
    Vd=phi+c*Gamma;Bq=1+(fixed['ell_native']*q)**2
    Delta=alpha+C*Q*Q/KB+CBAR*Q*Q*q*q*c/w
    Fv=-h*n-C*(Zd+2*h*Z)/(KB*q)+bg['cs_dt']*Gamma+c*(3*Rd-q*q*V)
    sigma=(L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-alpha*q*n)/Delta
    psid=Rd-bg['h_dt']*V-h*Vd;mom=S+(b+4*r/3+w)*V
    return dict(bg=bg,h=h,b=b,rg=rg,rn=rn,w=w,c=c,Q=Q,q=q,thermal=th,g=g,rb=rb,B=B,G=G,wb=wb,wg=wg,
        phi=phi,psi=psi,psid=psid,mom=mom,S=S,Rd=Rd,Z=Z,Zd=Zd,L=L,Ld=Ld,Ldd=Ldd,v=v,vd=vd,
        Gamma=Gamma,n=n,ncalc=ncalc,Vd=Vd,Bq=Bq,Delta=Delta,sigma=sigma)

def chart_rates(x,y,fixed,lay,therm,snodes,weights,omega,helpers,n_override=None,sigma_override=None):
    f=chart_coefficients(x,y,fixed,lay,therm,snodes,weights,omega,helpers,n_override)
    h,c,q,g,rb,B,G=(f[k] for k in ('h','c','q','g','rb','B','G'));V=y[8];Gamma=y[7];n=f['n'];sigma=f['sigma'] if sigma_override is None else sigma_override
    out=np.zeros_like(y);Rd=f['Rd'];wg=f['wg'];wb=f['wb'];W=y[4]
    out[0]=Rd;out[1]=3*Rd-q*q*(V+wb)
    out[2]=G/(B+G)*(h*y[2]+y[3]/4-y[lay.fg[2]]/2)-c*Gamma
    out[3]=4*Rd-4*q*q*(V+wg)/3
    out[4]=h*wg+y[3]/4-y[lay.fg[2]]/2-g*(1+1/rb)*W
    out[5]=4*Rd-4*q*q*(V+y[6])/3;out[6]=h*y[6]+y[5]/4-y[lay.fn[2]]/2-c*Gamma
    out[7]=3*Rd-q*q*V-CBAR*f['Q']*q*sigma/f['w'];out[8]=f['Vd']
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    for indices,velocity,collision in ((lay.fg,V+wg,g),(lay.fn,V+y[6],0.)):
        for l,i in indices.items():
            before=4*q*velocity/3 if l==2 else y[indices[l-1]];after=y[indices[l+1]] if l<max(indices) else 0.
            out[i]=q*(l*before-(l+1)*after)/(2*l+1)-collision*y[i]
            if l==2 and collision:out[i]+=collision*Pi/10
    for l,i in lay.pol.items():
        before=y[lay.pol[l-1]] if l else 0.;after=y[lay.pol[l+1]] if l<lay.lg else 0.
        out[i]=q*(l*before-(l+1)*after)/(2*l+1)-g*y[i]
        if l in (0,2):out[i]+=g*Pi*(.5 if l==0 else .1)
    out[lay.z]=y[lay.zd]
    ss=snodes**2 if y.ndim==1 else snodes[:,None]**2
    out[lay.zd]=-3*h*y[lay.zd]-omega**2*ss*(f['Bq']*y[lay.z]-q*n-sigma)
    return out,f

def chart_stage_matrix(x,fixed,lay,therm,snodes,weights,omega,helpers):
    na=lay.n+2;eye=np.eye(na)
    out,f=chart_rates(x,eye[:lay.n],fixed,lay,therm,snodes,weights,omega,helpers,eye[lay.n],eye[lay.n+1])
    mat=np.zeros((na,na));mat[:lay.n]=out/f['h'];mat[lay.n]=eye[lay.n]-f['ncalc'];mat[lay.n+1]=eye[lay.n+1]-f['sigma']
    return mat

def chart_snapshot(x,y,fixed,lay,therm,snodes,weights,omega,helpers):
    dy,f=chart_rates(x,y,fixed,lay,therm,snodes,weights,omega,helpers);h,b,rg,rn,w,c,Q,q=(f[k] for k in ('h','b','rg','rn','w','c','Q','q'))
    raw=to_raw(y,f['bg'],fixed);case=helpers['snapshot'](x,raw,fixed,lay,therm,snodes,weights,omega)
    wb,wg=f['wb'],f['wg'];wbd=-f['g']*y[4]/f['rb']-c*y[7];wgd=h*wg+y[3]/4-y[lay.fg[2]]/2-f['g']*y[4]-c*y[7]
    rawdy=np.array(dy,copy=True);rawdy[0]=f['psid'];rawdy[1]=dy[1]-3*(f['bg']['h_dt']*y[8]+h*dy[8])
    rawdy[2]=dy[8]+wbd;rawdy[3]=dy[3]-4*(f['bg']['h_dt']*y[8]+h*dy[8]);rawdy[4]=dy[8]+wgd
    rawdy[5]=dy[5]-4*(f['bg']['h_dt']*y[8]+h*dy[8]);rawdy[6]=dy[8]+dy[6];rawdy[7]=dy[7]-3*(f['bg']['h_dt']*y[8]+h*dy[8])
    P=KB*q*f['n']/2+CBAR*f['Z'];nt=np.array([q*q*f['psi'],3*h*f['S'],b*y[1],rg*y[3],rn*y[5],w*y[7],-q*P]);nf=q*q*CURVATURE*1e-10
    raw_nt=np.array([q*q*f['psi'],3*h*f['mom'],b*raw[1],rg*raw[3],rn*raw[5],w*raw[7],-q*P]);normal=math.fsum(float(v) for v in nt);ne=abs(normal)/max(float(sum(abs(raw_nt))),nf)
    vdd=(weights@dy[lay.zd]-2*f['Ld']*f['vd']-f['Ldd']*f['v'])/f['L'];nd=vdd-f['bg']['cs_dt']*y[7]-c*dy[7]
    et=np.array([KB*q*nd/2,-KB*h*q*f['n']/2,CBAR*f['Zd'],2*h*P,CBAR*Q*f['sigma']]);ef=KB*q*CURVATURE*max(h,Q,omega)*1e-10/2
    ee=float(abs(math.fsum(float(v) for v in et))/max(float(sum(abs(et))),ef))
    phid=f['psid']-2*(rg*(dy[lay.fg[2]]-2*h*y[lay.fg[2]])+rn*(dy[lay.fn[2]]-2*h*y[lay.fn[2]]))/q**2
    raw_momd=b*(rawdy[2]-3*h*raw[2])+4*rg*(rawdy[4]-4*h*raw[4])/3+4*rn*(rawdy[6]-4*h*raw[6])/3+w*(rawdy[8]-3*h*(1+c)*raw[8])
    Sdot=b*(wbd-3*h*wb)+4*rg*(wgd-4*h*wg)/3+4*rn*(dy[6]-4*h*y[6])/3
    total=b+4*(rg+rn)/3+w;total_dot=-3*h*b-16*h*(rg+rn)/3-3*h*(1+c)*w;momd=Sdot+total_dot*y[8]+total*dy[8]
    psidd=momd-f['bg']['h_dt']*f['phi']-h*phid
    tt=np.array([psidd,h*phid,3*h*f['psid'],(2*f['bg']['h_dt']+3*h*h)*f['phi'],q*q*(f['psi']-f['phi'])/3,-c*w*raw[7],-(rg*raw[3]+rn*raw[5])/3]);tf=CURVATURE*max(h*h,q*q)*1e-12
    te=float(abs(math.fsum(float(v) for v in tt))/max(float(sum(abs(tt))),tf))
    contrast=y[1]+3*h*wb;Eb=b*contrast;Eg=rg*(y[3]+4*h*wg);En=rn*(y[5]+4*h*y[6]);Ec=w*y[7];Ep=-q*P;S=rg*y[lay.fg[2]]+rn*y[lay.fn[2]]
    other=math.fsum((Eg,En,Ec,Ep));rat=dict(denominator=Eb,normal_over_denominator=normal/Eb if Eb else None)
    if Eb:
        ref=-Eb/q**2;rat.update(force_metric=.99*f['phi']/ref,lens_metric=.99*(f['phi']+f['psi'])/(2*ref),force_source=.99*(1+(other+2*S)/Eb),lens_source=.99*(1+(other+S)/Eb),refusal=None)
    else:rat.update(force_metric=None,lens_metric=None,force_source=None,lens_source=None,refusal='ZERO_SIGNED_BARYON_DENOMINATOR')
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    reads=[raw[3]/4+f['phi'],q*raw[4],q*raw[2],f['psi']+f['phi'],y[lay.fg[2]],Pi,y[lay.fn[2]],contrast,Eb,Eg+En,Ec,Ep,-KB*q*q*f['n']/2,-CBAR*q*f['Z'],q*f['n']]
    case.update(state=raw.tolist(),stable_state=y.tolist(),Phi=float(f['phi']),Psi=float(f['psi']),Q=float(Q),reaction_denominator=float(f['Delta']),n_U=float(f['n']),sigma=float(f['sigma']),P=float(P),pi_U=float(y[8]-f['v']),Z=float(f['Z']),Zd=float(f['Zd']),readouts=[float(v) for v in reads],normal_terms=raw_nt.tolist(),stable_normal_terms=nt.tolist(),normal_stable_residual=normal,normal_raw_residual=math.fsum(float(v) for v in raw_nt),current_derivative_contacts=dict(stable=float(momd),raw=float(raw_momd),signed_difference=float(momd-raw_momd)),normal_floor=nf,normal_error=float(ne),omitted_Euler_terms=et.tolist(),omitted_Euler_floor=ef,omitted_Euler_error=ee,trace_terms=tt.tolist(),trace_floor=tf,trace_error=te,signed_sources=dict(baryon=Eb,photon=Eg,neutrino=En,phase=Ec,polarization=Ep,shear=S),source_ratios=rat,
        stable_coordinates=dict(R=float(y[0]),Gamma_b=float(y[1]),U=float(y[2]),Gamma_gamma=float(y[3]),W=float(y[4]),Gamma_nu=float(y[5]),w_nu=float(y[6]),Gamma_phase=float(y[7]),V=float(y[8]),wb=float(wb),wg=float(wg),Jrelative=float((f['B']+f['G'])*y[2])))
    return case

def lagrange_values(nodes,v):
    nodes=np.asarray(nodes,float);v=np.asarray(v,float);out=[]
    if not (len(nodes)==4 and np.all(np.diff(nodes)>0) and nodes[0]==0. and nodes[-1]==1.):raise AssertionError('Actual ordered cubic conformal nodes')
    for j in range(4):
        val=np.ones_like(v)
        for k in range(4):
            if k!=j:val*=((v-nodes[k])/(nodes[j]-nodes[k]))
        out.append(val)
    return np.array(out)

def cubic_envelope(nodes,values):
    coeff=np.zeros(4)
    for j in range(4):
        polynomial=np.polynomial.polynomial.polyfromroots([nodes[k] for k in range(4) if k!=j])
        coeff+=float(values[j])*polynomial/math.prod(nodes[j]-nodes[k] for k in range(4) if k!=j)
    return math.fsum(abs(float(v)) for v in coeff)

class CubicKernel:
    def __init__(self,fixed,therm):
        self.env=load_optical_namespace();self.fixed=fixed;self.therm=therm;self.cache={};self.weight_cache={}
        self.maximum={name:0. for name in ('inverse_depth_error','optical_integral_error','conformal_integral_error','optical_mass_error','measure_identity_error','source_quadrature_error')}
    def geometry(self,lo,hi,el,er,order=16):
        key=(float(lo),float(hi),float(el),float(er),order)
        if key not in self.cache:
            z=self.env['optical_geometry'](lo,hi,el,er,self.fixed,self.therm,K,order,order);z['key']=key;self.cache[key]=z
            for name,value in z['controls'].items():self.maximum[name]=max(self.maximum[name],float(value))
        return self.cache[key]
    def integral(self,lo,hi,order=16):return self.env['integrals'](lo,hi,self.fixed,self.therm,K,order)
    def weights(self,points,target,collision):
        """Four actual-node polynomial weights, compared16/32 on identical sources."""
        xs=tuple(float(p['x']) for p in points);es=tuple(float(p['eta']) for p in points);tx,te=map(float,target)
        key=(xs,es,tx,te,collision)
        if key in self.weight_cache:return self.weight_cache[key]
        width=es[-1]-es[0];nodes=(np.array(es)-es[0])/width
        def one(order):
            if collision:
                source_x=min(tx,xs[-1]);source_eta=min(te,es[-1]);geometry=self.geometry(xs[0],source_x,es[0],source_eta,order);eta=source_eta-geometry['eta_back'];mw=geometry['metric_weights'];cw=geometry['collision_weights'];tail=(geometry['metric_tail'],geometry['collision_tail']);depth=geometry['depth'];minimum=geometry['minimum_gamma']
            else:
                u,w=gauss(order);source_eta=min(te,es[-1]);eta=(source_eta+es[0])/2+(source_eta-es[0])*u/2;mw=(source_eta-es[0])*w/2;cw=np.zeros_like(mw);tail=(0.,0.);depth=0.;minimum=0.
            v=(eta-es[0])/width;basis=lagrange_values(nodes,v);phase=K*(te-eta)
            m=np.empty((5,3,4));c=np.empty_like(m)
            for l in range(5):
                for r in range(3):
                    j=bessel(l,r,phase)
                    for p in range(4):
                        m[l,r,p]=math.fsum(float(t) for t in mw*j*basis[p]);c[l,r,p]=math.fsum(float(t) for t in cw*j*basis[p])
            md=math.fsum(float(v) for v in abs(mw)*np.sum(abs(basis),axis=0));cd=math.fsum(float(v) for v in abs(cw)*np.sum(abs(basis),axis=0))
            return m,c,dict(tail=tail,depth=depth,minimum=minimum,md=md,cd=cd)
        m,c,d=one(16);mm,cc,dd=one(32)
        error=max(float(np.max(abs(m-mm)))/max(d['md'],dd['md'],1e-300),float(np.max(abs(c-cc)))/max(d['cd'],dd['cd'],1e-300))
        self.maximum['source_quadrature_error']=max(self.maximum['source_quadrature_error'],error)
        value=(m,c,d);self.weight_cache[key]=value;return value

    def free_weights(self,panels,target):
        """Vectorized complete free-streaming history; no finite-L closure."""
        key=('FREE',tuple(tuple(float(p['eta']) for p in pp) for pp in panels),float(target[1]))
        if key in self.weight_cache:return self.weight_cache[key]
        es=np.array([[p['eta'] for p in pp] for pp in panels]);width=es[:,-1]-es[:,0];nodes=(es-es[:,0,None])/width[:,None]
        def one(order):
            u,w=gauss(order);eta=(es[:,-1,None]+es[:,0,None])/2+width[:,None]*u/2
            v=(eta-es[:,0,None])/width[:,None];basis=[]
            for j in range(4):
                value=np.ones_like(v)
                for k in range(4):
                    if k!=j:value*=(v-nodes[:,k,None])/(nodes[:,j,None]-nodes[:,k,None])
                basis.append(value)
            basis=np.array(basis).transpose(1,0,2);mw=width[:,None]*w/2;phase=K*(target[1]-eta);out=np.empty((len(panels),5,3,4))
            for l in range(5):
                for r in range(3):out[:,l,r]=np.sum(mw[:,None,:]*basis*bessel(l,r,phase)[:,None,:],axis=-1)
            scale=np.sum(abs(mw)*np.sum(abs(basis),axis=1),axis=-1)
            return out,scale
        m,scale=one(16);mm,ss=one(32);error=float(np.max(abs(m-mm)/np.maximum(np.maximum(scale,ss)[:,None,None,None],1e-300)))
        self.maximum['source_quadrature_error']=max(self.maximum['source_quadrature_error'],error);self.weight_cache[key]=m;return m

def stable_anchor(x,eta,y,fixed,lay,therm,snodes,weights,omega,helpers):
    f=chart_coefficients(x,y,fixed,lay,therm,snodes,weights,omega,helpers)
    return dict(x=float(x),eta=float(eta),R=float(y[0]),qV=float(f['q']*y[8]),cGamma=float(f['c']*y[7]),Gamma=float(y[3]),dipole=float(4*f['q']*f['wb']),Pi=float(y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]))

def stable_initial_multipoles(y,lay,q,bg,fixed):
    bgB=bg['a']**3*bg['b'];bgG=bg['a']**3*4*bg['r']*fixed['fgamma']/3;wg=y[2]+bgB*y[4]/(bgB+bgG)
    return dict(nu=[float(y[5]),float(4*q*y[6]/3)]+[float(y[lay.fn[l]]) for l in (2,3,4)],
        photon=[float(y[3]),float(4*q*wg/3)]+[float(y[lay.fg[l]]) for l in (2,3,4)],polarization=[float(y[lay.pol[l]]) for l in range(5)])

def compensated_residual(matrix,rhs,solution,support=None):
    """Literal nonzero row terms only; discarded terms are exactlyzero."""
    if support is None:support=[np.flatnonzero(row) for row in matrix]
    return np.array([math.fsum(float(row[j]*solution[j]) for j in indices)-float(r) for row,r,indices in zip(matrix,rhs,support)])

def gauss_block_solve(matrix,rhs,lay):
    """Six coordinates per native mode; all stages and endpoints reconstructed."""
    na=lay.n+2;original=matrix;original_rhs=rhs;support=[np.flatnonzero(row) for row in matrix];matrix,rhs,columns=equilibrate(matrix,rhs)
    mode_set={point*na+i for point in range(3) for i in list(lay.z)+list(lay.zd)}
    core=np.array([i for i in range(3*na) if i not in mode_set]);s=matrix[np.ix_(core,core)].copy();saved=[]
    for z,v in zip(lay.z,lay.zd):
        ix=np.array([p*na+i for p in range(3) for i in (z,v)]);block=matrix[np.ix_(ix,ix)];inverse=np.linalg.solve(block,np.eye(6));transfer=inverse@matrix[np.ix_(ix,core)];coupling=matrix[np.ix_(core,ix)];s-=coupling@transfer;saved.append((ix,inverse,transfer,coupling))
    def solve_balanced(b):
        r=b[core].copy();local=[]
        for ix,inverse,transfer,coupling in saved:
            v=inverse@b[ix];r-=coupling@v;local.append(v)
        out=np.zeros(len(b));out[core]=np.linalg.solve(s,r)
        for (ix,inverse,transfer,coupling),v in zip(saved,local):out[ix]=v-transfer@out[core]
        return out
    out=columns*solve_balanced(rhs)
    for _ in range(3):
        residual=compensated_residual(original,original_rhs,out,support)
        _,br,_=equilibrate(original,-residual);out+=columns*solve_balanced(br)
    residual=compensated_residual(original,original_rhs,out,support)
    scale=abs(original)@abs(out)+abs(original_rhs)
    return out,float(np.max(abs(residual)/np.maximum(scale,CURVATURE*1e-18)))
def source_vectors(x,eta,index,size,fixed,lay,therm,snodes,weights,omega,helpers):
    eye=np.eye(lay.n+2);f=chart_coefficients(x,eye[:lay.n],fixed,lay,therm,snodes,weights,omega,helpers,eye[lay.n]);out={}
    local=dict(R=eye[0],qV=f['q']*eye[8],cGamma=f['c']*eye[7],Gamma=eye[3],dipole=4*f['q']*f['wb'],Pi=eye[lay.fg[2]]+eye[lay.pol[0]]+eye[lay.pol[2]])
    for name,v in local.items():
        out[name]=np.zeros(size);out[name][index:index+lay.n+2]=v
    return out,f

def memory_panel(points,target,fields,optical,collision,size):
    """Linear cubic source response; panelwise R−R_left IBP is exact."""
    metric,cw,info=optical.weights(points,target,collision);m=np.zeros((5,size));p=np.zeros_like(m);constant=np.zeros(5);polar_constant=np.zeros(5)
    fixed_fields=[];linear_fields=[]
    for values in fields:
        fixed_fields.append({k:float(v) if np.ndim(v)==0 else 0. for k,v in values.items() if k in ('R','qV','cGamma','Gamma','dipole','Pi')})
        linear_fields.append({k:np.zeros(size) if np.ndim(v)==0 else np.asarray(v) for k,v in values.items() if k in ('R','qV','cGamma','Gamma','dipole','Pi')})
    left=fixed_fields[0]['R'];width=points[-1]['eta']-points[0]['eta'];nodes=(np.array([p['eta'] for p in points])-points[0]['eta'])/width
    source_end=min(target[1],points[-1]['eta']);fraction=(source_end-points[0]['eta'])/width;basis=lagrange_values(nodes,np.array([fraction]))[:,0]
    
    def weighted(name,weights_,difference=False):
        cc=math.fsum(float(w)*(v[name]-(left if difference else 0.)) for w,v in zip(weights_,fixed_fields))
        vv=sum(float(w)*v[name] for w,v in zip(weights_,linear_fields))
        return vv,cc
    for l in range(5):
        end_R,end_c=weighted('R',basis,True);jright=float(bessel(l,0,K*(target[1]-source_end)))
        m[l]+=4*jright*end_R;constant[l]+=4*jright*end_c
        for name,ww,difference in [('R',4*K*metric[l,1]-4*cw[l,0],True),('qV',4*K*metric[l,2],False),('cGamma',-4*K*metric[l,1],False),('Gamma',cw[l,0],False),('dipole',cw[l,1],False),('Pi',(cw[l,0]+3*cw[l,2])/4,False)]:
            vv,cc=weighted(name,ww,difference);m[l]+=vv;constant[l]+=cc
        vv,cc=weighted('Pi',3*(cw[l,0]+cw[l,2])/4);p[l]+=vv;polar_constant[l]+=cc
    return m,constant,p,polar_constant,info

def fixed_panel_response(points,target,optical):
    metric,cw,info=optical.weights(points,target,True);values={name:np.array([p[name] for p in points]) for name in ('R','qV','cGamma','Gamma','dipole','Pi')};dr=values['R']-values['R'][0]
    phase=K*(target[1]-points[-1]['eta']);boundary=4*(points[-1]['R']-points[0]['R'])*np.array([float(bessel(l,0,phase)) for l in range(5)])
    photon=boundary+4*K*(metric[:,1]@dr+metric[:,2]@values['qV']-metric[:,1]@values['cGamma'])-4*cw[:,0]@dr+cw[:,0]@values['Gamma']+cw[:,1]@values['dipole']+(cw[:,0]+3*cw[:,2])@values['Pi']/4
    polar=3*(cw[:,0]+cw[:,2])@values['Pi']/4
    return photon,polar,info

def free_history_response(panels,target,optical):
    if not panels:return np.zeros(5)
    m=optical.free_weights(panels,target);values={name:np.array([[p[name] for p in pp] for pp in panels]) for name in ('R','qV','cGamma')};dr=values['R']-values['R'][:,0,None]
    phase=K*(target[1]-np.array([pp[-1]['eta'] for pp in panels]));boundary=4*(values['R'][:,-1]-values['R'][:,0])[:,None]*np.array([bessel(l,0,phase) for l in range(5)]).T
    source=4*K*np.sum(m[:,:,1]*dr[:,None,:]+m[:,:,2]*values['qV'][:,None,:]-m[:,:,1]*values['cGamma'][:,None,:],axis=-1)
    return np.array([math.fsum(float(v) for v in boundary[:,l]+source[:,l]) for l in range(5)])

def source_envelopes(points):
    nodes=(np.array([r['eta'] for r in points])-points[0]['eta'])/(points[-1]['eta']-points[0]['eta'])
    deltaR=[r['R']-points[0]['R'] for r in points]
    metric=4*K*(cubic_envelope(nodes,deltaR)+cubic_envelope(nodes,[r['qV'] for r in points])+cubic_envelope(nodes,[r['cGamma'] for r in points]))
    collision=4*cubic_envelope(nodes,deltaR)+cubic_envelope(nodes,[r['Gamma'] for r in points])+cubic_envelope(nodes,[r['dipole'] for r in points])+2.5*cubic_envelope(nodes,[r['Pi'] for r in points])
    return metric,collision,4*abs(points[-1]['R']-points[0]['R'])

def coupled_gauss(previous,x0,dx,etas,anchors,fixed,lay,therm,snodes,weights,omega,helpers,initial_values,optical,dense=False):
    """Two Gauss stages plus output, with simultaneous full cubic memory."""
    na=lay.n+2;size=3*na;c1=.5-math.sqrt(3)/6;c2=.5+math.sqrt(3)/6
    coordinates=[x0+c1*dx,x0+c2*dx,x0+dx];A=np.array([[.25,.25-math.sqrt(3)/6],[.25+math.sqrt(3)/6,.25],[.5,.5]])
    matrices=[chart_stage_matrix(xx,fixed,lay,therm,snodes,weights,omega,helpers) for xx in coordinates]
    sources=[];coefficients=[];points=[{k:v for k,v in anchors[-1].items() if k not in ('panel_nodes','panel_envelopes')}]
    for j,(xx,ee) in enumerate(zip(coordinates,etas)):
        ss,ff=source_vectors(xx,ee,j*na,size,fixed,lay,therm,snodes,weights,omega,helpers);sources.append(ss);coefficients.append(ff);points.append(dict(x=float(xx),eta=float(ee)))
    matrix=np.zeros((size,size));rhs=np.zeros(size);eye=np.eye(na);differential=[1,7,8]+list(lay.z)+list(lay.zd)
    before=chart_coefficients(x0,previous,fixed,lay,therm,snodes,weights,omega,helpers);J0=(before['B']+before['G'])*previous[2]
    for j in range(3):
        start=j*na;f=coefficients[j]
        for r in differential:
            matrix[start+r,start+r]=1.;rhs[start+r]=previous[r]
            for s in range(2):matrix[start+r,s*na:(s+1)*na]-=dx*A[j,s]*matrices[s][r]
        # Literal Jr increment. The photon dipole memory determines the remaining
        # velocity coordinate; no second independent slip evolution is imposed.
        matrix[start+2,start+2]=f['B']+f['G'];rhs[start+2]=J0
        for s in range(2):
            fs=coefficients[s];force=fs['G']*(eye[3]/4-eye[lay.fg[2]]/2)-(fs['B']+fs['G'])*fs['c']*eye[7]
            matrix[start+2,s*na:(s+1)*na]-=dx*A[j,s]*force/fs['h']
        normal=f['q']**2*(eye[0]-f['h']*eye[8])+3*f['h']*f['S']+f['b']*eye[1]+f['rg']*eye[3]+f['rn']*eye[5]+f['w']*eye[7]-f['q']*(KB*f['q']*f['ncalc']/2+CBAR*f['Z'])
        matrix[start,start:start+na]=normal
        matrix[start+lay.n:start+na,start:start+na]=matrices[j][lay.n:]
    bounds=[dict(discarded_source_bound=0.,kernel_tail_bound=0.,collision_kernel_tail_bound=0.) for _ in range(3)]
    for j,(xx,ee) in enumerate(zip(coordinates,etas)):
        target=(float(xx),float(ee));start=j*na
        current_geometry=optical.geometry(points[0]['x'],xx,points[0]['eta'],ee)
        visibility=math.exp(-min(745.,float(optical.integral(anchors[0]['x'],xx)[0])))
        gm,gc,pm,pc,info=memory_panel(points,target,[anchors[-1]]+sources,optical,True,size)
        nm,nc,_,_,_=memory_panel(points,target,[anchors[-1]]+sources,optical,False,size)
        gc+=visibility*np.asarray(initial_values[j]['photon']);pc+=visibility*np.asarray(initial_values[j]['polarization']);nc+=np.asarray(initial_values[j]['nu'])
        history=anchors[1:];panels=[r['panel_nodes'] for r in history];nc+=free_history_response(panels,target,optical)
        if history:
            ends=np.array([r['x'] for r in history]);future=np.asarray(optical.integral(ends,xx)[0]);atten=np.exp(-np.minimum(future,745.));envelopes=np.array([r['panel_envelopes'] for r in history]);widths=np.array([pp[-1]['eta']-pp[0]['eta'] for pp in panels]);minimum=optical.env['background_rates'](ends,fixed,therm,K)[2];discard=future>48
            bounds[j]['discarded_source_bound']+=5*float(np.sum(atten[discard]*(envelopes[discard,2]+envelopes[discard,0]*np.minimum(widths[discard],1/minimum[discard])+envelopes[discard,1])))
            for ix in np.flatnonzero(~discard):
                pp=panels[ix];me,ce,be=envelopes[ix];cc,cp,inf=fixed_panel_response(pp,target,optical);gc+=atten[ix]*cc;pc+=atten[ix]*cp
                bounds[j]['discarded_source_bound']+=5*atten[ix]*(me*inf['tail'][0]+ce*inf['tail'][1]);bounds[j]['kernel_tail_bound']+=atten[ix]*inf['tail'][0];bounds[j]['collision_kernel_tail_bound']+=atten[ix]*inf['tail'][1]
        f=coefficients[j]
        for l in range(5):
            if l==0:gi,ni,gv,nv=3,5,eye[3],eye[5]
            elif l==1:gi,ni,gv,nv=4,6,4*f['q']*(eye[2]+f['B']*eye[4]/(f['B']+f['G']))/3,4*f['q']*eye[6]/3
            else:gi,ni,gv,nv=lay.fg[l],lay.fn[l],eye[lay.fg[l]],eye[lay.fn[l]]
            matrix[start+gi,start:start+na]+=gv;matrix[start+gi]-=gm[l];rhs[start+gi]=gc[l]
            matrix[start+ni,start:start+na]+=nv;matrix[start+ni]-=nm[l];rhs[start+ni]=nc[l]
            matrix[start+lay.pol[l],start+lay.pol[l]]=1.;matrix[start+lay.pol[l]]-=pm[l];rhs[start+lay.pol[l]]=pc[l]
    solution,stage_error=gauss_block_solve(matrix,rhs,lay);dense_error=0.
    if dense:
        em,er,ec=equilibrate(matrix,rhs);independent=ec*np.linalg.solve(em,er)
        for _ in range(3):
            dense_residual=compensated_residual(matrix,rhs,independent)
            _,correction,_=equilibrate(matrix,-dense_residual);independent+=ec*np.linalg.solve(em,correction)
        dense_error=float(np.max(abs(solution-independent))/max(float(np.max(abs(independent))),CURVATURE*1e-18))
    states=[solution[j*na:j*na+lay.n] for j in range(3)];actual_points=[{k:v for k,v in anchors[-1].items() if k not in ('panel_nodes','panel_envelopes')}]+[stable_anchor(xx,ee,y,fixed,lay,therm,snodes,weights,omega,helpers) for xx,ee,y in zip(coordinates,etas,states)]
    for j in range(3):
        me,ce,_=source_envelopes(actual_points);geometry=optical.geometry(points[0]['x'],coordinates[j],points[0]['eta'],etas[j]);bounds[j]['discarded_source_bound']+=5*(me*geometry['metric_tail']+ce*geometry['collision_tail']);bounds[j]['kernel_tail_bound']+=geometry['metric_tail'];bounds[j]['collision_kernel_tail_bound']+=geometry['collision_tail']
    final=dict(actual_points[-1]);final['panel_nodes']=actual_points;final['panel_envelopes']=source_envelopes(actual_points)
    record=dict(x=float(x0),dx=float(dx),coordinates=[float(v) for v in coordinates],conformal=[float(v) for v in etas],previous=previous.tolist(),states=[v.tolist() for v in states],algebraic_states=[solution[j*na+lay.n:(j+1)*na].tolist() for j in range(3)],stage_error=stage_error,dense_error=dense_error)
    return states,dict(stage_error=stage_error,dense_error=dense_error,**{k:max(r[k] for r in bounds) for k in bounds[0]}),final,record
def raw_derivatives(y,dy,f,lay):
    out=np.array(dy,copy=True);h=f['h'];V=y[8];hd=f['bg']['h_dt'];c=f['c'];Gamma=y[7]
    out[0]=dy[0]-hd*V-h*dy[8];out[1]=dy[1]-3*(hd*V+h*dy[8]);out[2]=dy[8]-f['g']*y[4]/f['rb']-c*Gamma
    out[3]=dy[3]-4*(hd*V+h*dy[8]);out[4]=dy[8]+h*f['wg']+y[3]/4-y[lay.fg[2]]/2-f['g']*y[4]-c*Gamma
    out[5]=dy[5]-4*(hd*V+h*dy[8]);out[6]=dy[8]+dy[6];out[7]=dy[7]-3*(hd*V+h*dy[8])
    return out

def run_trial(spec,fixed,helpers,lineage):
    label,n,ns,stride,ai=spec;lay=helpers['Layout'](ns,4,4);therm=helpers['Thermal']('HALF',1,fixed);optical=CubicKernel(fixed,therm)
    nodes,weight=gauss(ns);snodes=(nodes+1)/2;weights=weight*snodes;weights/=sum(weights)
    prefix=128 if label=='START' else 0;common_n=n-prefix;common=np.linspace(math.log(AI),math.log(AF),common_n+1)
    xs=np.r_[np.linspace(math.log(ai),math.log(AI),prefix+1)[:-1],common] if prefix else common
    grid=conformal_grid(xs,fixed,helpers,8);grid2=conformal_grid(xs,fixed,helpers,16);eta_error=float(np.max(abs(grid-grid2))/max(float(grid2[-1]),1e-30))
    initial=[];seed=[];starts=[];moments=[];bg0=helpers['background'](float(xs[0]),fixed)
    for om in OMEGAS:
        raw,e0,meta=regular_seed(ai,fixed,lay,therm,snodes,weights,om,helpers);y=to_chart(raw,bg0,fixed);initial.append(y);starts.append(e0);seed.append(meta);moments.append(stable_initial_multipoles(y,lay,K*CP/(1000*fixed['Hunit']*ai),bg0,fixed))
    if max(starts)!=min(starts):raise AssertionError('Shared conformal origin')
    eta=grid2+starts[0];c1=.5-math.sqrt(3)/6;c2=.5+math.sqrt(3)/6
    step_targets=[]
    for i in range(1,n+1):
        lo=float(xs[i-1]);dx=float(xs[i]-xs[i-1]);xx=(lo+c1*dx,lo+c2*dx,float(xs[i]));ee=[]
        for j,xj in enumerate(xx):ee.append(float(eta[i]) if j==2 else float(eta[i-1]+optical.integral(lo,xj,16)[1]))
        step_targets.append((xx,ee))
    target_phase=K*(np.array([ee for xx,ee in step_targets])-eta[0]);transported=[];transport_errors=[]
    for mm in moments:
        transported.append({kind:np.array([initial_transport(coeff,target_phase,l).real for l in range(5)]) for kind,coeff in mm.items()})
        transport_errors.append({kind:float(np.max(abs(transported[-1][kind]-np.array([initial_transport(coeff,target_phase,l,256).real for l in range(5)])))/CURVATURE) for kind,coeff in mm.items()})
    late_h=helpers['background'](math.log(AF),fixed)['h'];late_compton=compton_rate(AF,fixed,therm);background_lag_bound=late_h/(late_h+late_compton)
    if not (0<=background_lag_bound<1):raise AssertionError('Positive Compton background barrier')
    last_stages=[None]*4;states=initial;anchors=[[stable_anchor(xs[0],eta[0],y,fixed,lay,therm,snodes,weights,om,helpers)] for y,om in zip(states,OMEGAS)]
    snapshots=[];errors=[dict(stage_error=0.,dense_error=0.,momentum_error=0.,discrete_trace_error=0.,los_continuity_error=0.,kernel_tail_bound=0.,discarded_source_bound=0.,gas_temperature_difference_bound=0.,collision_kernel_tail_bound=0.,metric_momentum_error=0.,curvature_increment_error=0.,baryon_Euler_error=0.) for _ in OMEGAS]
    los_diagnostics=[{name:dict(maximum=0.,location=None) for name in ('delta_gamma','Hstar_u_gamma','delta_nu','Hstar_u_nu','F_gamma_2','F_nu_2','G_gamma_0','G_gamma_2')} for _ in OMEGAS]
    expected_steps=sorted(set(list(range(0,n+1,128))+[n]));paths=sorted(BASE.glob(STEM+'_'+label+'_CP_*_COMMIT.json'));start=0
    if paths:
        seen=[];prior=None
        for cn in paths:
            commit=json.loads(cn.read_text());pn=BASE/commit['payload'];cp=json.loads(pn.read_text());i=cp['nstep'];validate_checkpoint(cp,commit,lineage,label,i,n,ns,stride)
            if prior is not None:
                if cp['snapshots'][:len(prior['snapshots'])]!=prior['snapshots'] or any(cp['anchors'][a][:len(prior['anchors'][a])]!=prior['anchors'][a] for a in range(4)):raise AssertionError('Exact state/source-memory immutable prefix')
                if any(cp['errors'][a][key]<prior['errors'][a][key] for a in range(4) for key in prior['errors'][a]) or any(cp['optical_controls'][key]<prior['optical_controls'][key] for key in prior['optical_controls']) or any(cp['los_diagnostics'][a][key]['maximum']<prior['los_diagnostics'][a][key]['maximum'] for a in range(4) for key in prior['los_diagnostics'][a]):raise AssertionError('Nondecreasing diagnostic prefix')
            prior=cp;CREATED[str(pn.resolve())]=commit['sha256'];CREATED[str(cn.resolve())]=sha(cn);seen.append(i)
        if seen!=expected_steps[:len(seen)]:raise AssertionError('Complete contiguous checkpoint prefix')
        latest=prior
        if latest['seed_metadata']!=json_builtin(seed) or latest['initial_moments']!=json_builtin(moments):raise AssertionError('Same complete incoming state')
        last_stages=latest['last_stages'];states=[np.array(y) for y in latest['states']];anchors=latest['anchors'];snapshots=latest['snapshots'];errors=latest['errors'];los_diagnostics=latest['los_diagnostics'];optical.maximum=latest['optical_controls'];start=seen[-1]
    payloads=[p for p in BASE.glob(STEM+'_'+label+'_CP_*.json') if not p.name.endswith('_COMMIT.json')]
    if len(payloads)!=len(paths):raise AssertionError('Orphan payload refusal')
    def checkpoint(i):
        recheck();pn=STEM+'_'+label+'_CP_'+str(i).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
        cp=dict(lineage=lineage,trial=label,nstep=i,step_count=n,ns=ns,stride=stride,states=states,anchors=anchors,snapshots=snapshots,errors=errors,seed_metadata=seed,initial_moments=moments,los_diagnostics=los_diagnostics,optical_controls=optical.maximum,last_stages=last_stages)
        ph=write(pn,cp);ch=write(cn,dict(lineage=lineage,trial=label,nstep=i,payload=pn,sha256=ph));journal('CHECKPOINT',trial=label,nstep=i,payload_sha256=ph,commit_sha256=ch);print(label,i,'/',n,flush=True)
    def cases_at(i):
        cases=[]
        for arm,(y,om) in enumerate(zip(states,OMEGAS)):
            case=chart_snapshot(float(xs[i]),y,fixed,lay,therm,snodes,weights,om,helpers);dy,f=chart_rates(float(xs[i]),y,fixed,lay,therm,snodes,weights,om,helpers);rd=raw_derivatives(y,dy,f,lay);gc=compton_rate(f['bg']['a'],fixed,therm)
            forcing=abs(2*rd[1]/3-rd[3]/4)/gc+background_lag_bound/(1-background_lag_bound)*(abs(case['state'][3])+abs(f['phi']))
            errors[arm]['gas_temperature_difference_bound']=max(errors[arm]['gas_temperature_difference_bound'],float(forcing));case['gas_source_bound']=extra_source_bound(case,fixed,therm,errors[arm]['gas_temperature_difference_bound'],background_lag_bound);cases.append(case)
        return cases
    if start==0 and not paths:snapshots.append(dict(nstep=0,cases=cases_at(0)));checkpoint(0)
    for i in range(start+1,n+1):
        optical.weight_cache.clear();previous=states;states=[];xx,ee=step_targets[i-1];dx=float(xs[i]-xs[i-1])
        for arm,om in enumerate(OMEGAS):
            iv=[{kind:arr[:,i-1,j] for kind,arr in transported[arm].items()} for j in range(3)]
            nodes_,err,final,record=coupled_gauss(previous[arm],float(xs[i-1]),dx,ee,anchors[arm],fixed,lay,therm,snodes,weights,om,helpers,iv,optical,dense=i%128==0);last_stages[arm]=record;y=nodes_[-1];states.append(y)
            stage_rates=[];fs=[];raws=[]
            for xj,yj in zip(xx,nodes_):
                dd,ff=chart_rates(xj,yj,fixed,lay,therm,snodes,weights,om,helpers);stage_rates.append(raw_derivatives(yj,dd,ff,lay)/ff['h']);fs.append(ff);raws.append(to_raw(yj,ff['bg'],fixed))
            end_dy,end_f=chart_rates(xx[-1],y,fixed,lay,therm,snodes,weights,om,helpers);end_raw_rate=raw_derivatives(y,end_dy,end_f,lay);gc=compton_rate(end_f['bg']['a'],fixed,therm)
            forcing=abs(2*end_raw_rate[1]/3-end_raw_rate[3]/4)/gc+background_lag_bound/(1-background_lag_bound)*(abs(raws[-1][3])+abs(end_f['phi']))
            errors[arm]['gas_temperature_difference_bound']=max(errors[arm]['gas_temperature_difference_bound'],float(forcing))
            prev=chart_coefficients(float(xs[i-1]),previous[arm],fixed,lay,therm,snodes,weights,om,helpers);oldraw=to_raw(previous[arm],prev['bg'],fixed);newraw=raws[-1]
            def integrated_error(delta,forces,endpoint_scale):
                integral=dx*math.fsum(float(z) for z in forces)/2;res=delta-integral;scale=endpoint_scale+abs(dx)*math.fsum(abs(float(z)) for z in forces)/2
                return float(abs(res)/max(scale,CURVATURE*1e-18))
            err['metric_momentum_error']=integrated_error(fs[-1]['psi']-prev['psi'],[f['mom']/f['h']-f['phi'] for f in fs[:2]],abs(fs[-1]['psi'])+abs(prev['psi']))
            err['curvature_increment_error']=integrated_error(y[0]-previous[arm][0],[f['Rd']/f['h'] for f in fs[:2]],abs(y[0])+abs(previous[arm][0]))
            err['baryon_Euler_error']=integrated_error((y[8]-previous[arm][8])+(fs[-1]['wb']-prev['wb']),[(f['phi']-f['g']*nodes_[j][4]/f['rb'])/f['h'] for j,f in enumerate(fs[:2])],abs(newraw[2])+abs(oldraw[2]))
            err['momentum_error']=max(err['metric_momentum_error'],err['curvature_increment_error'],err['baryon_Euler_error'])
            force=[]
            for f,z in zip(fs[:2],nodes_[:2]):
                dp=f['c']*f['w']*(z[7]-3*f['h']*z[8])+(f['rg']*(z[3]-4*f['h']*z[8])+f['rn']*(z[5]-4*f['h']*z[8]))/3
                force.append(3*f['mom']+f['bg']['h_dt']*f['phi']/f['h']+f['q']**2*(f['psi']-f['phi'])/(3*f['h'])-dp/f['h'])
            err['discrete_trace_error']=integrated_error(fs[-1]['mom']-prev['mom'],[-v for v in force],abs(fs[-1]['mom'])+abs(prev['mom']))
            rows=[3,4,5,6,lay.fg[2],lay.fn[2],lay.pol[0],lay.pol[2]]
            delta=newraw[rows]-oldraw[rows];rr=(stage_rates[0][rows]+stage_rates[1][rows])/2;residual=delta-dx*rr
            scale=abs(newraw[rows])+abs(oldraw[rows])+abs(dx)*(abs(stage_rates[0][rows])+abs(stage_rates[1][rows]))/2;row_errors=abs(residual)/np.maximum(scale,CURVATURE*1e-12);err['los_continuity_error']=float(np.max(row_errors))
            for j,name in enumerate(los_diagnostics[arm]):
                if row_errors[j]>los_diagnostics[arm][name]['maximum']:
                    los_diagnostics[arm][name]=dict(maximum=float(row_errors[j]),location=dict(nstep=i,a=math.exp(float(xs[i])),residual=float(residual[j]),scale=float(scale[j]),old_state=float(oldraw[rows[j]]),new_state=float(newraw[rows[j]]),gauss_stage_rates=[float(stage_rates[s][rows[j]]) for s in range(2)],log_step=dx))
            for key,value in err.items():
                if key in errors[arm]:errors[arm][key]=max(errors[arm][key],float(value))
            # SOURCE uses one cubic panel spanning two steps and its actual late
            # Gauss nodes; no intermediate photon or state reset is performed.
            if i%stride==0:anchors[arm].append(final)
        if i>=prefix and (i-prefix)%(common_n//32)==0:snapshots.append(dict(nstep=i,cases=cases_at(i)))
        if i%128==0 or i==n:checkpoint(i)
    return dict(label=label,n=n,ns=ns,stride=stride,ai=ai,af=AF,k=K,omega=list(OMEGAS),layout_names=lay.names(),stable_core_names=['R','Gamma_b','U','Gamma_gamma','W','Gamma_nu','w_nu','Gamma_phase','V'],seed=seed,common_snapshot_count=33,eta_quadrature_error=eta_error,endpoint_phase=K*float(grid2[-1]),initial_transport_errors=transport_errors,snapshots=snapshots,errors=errors,los_diagnostics=los_diagnostics,optical_controls=dict(optical.maximum),gas_scope='Same cold-baryon instantaneous source and lag bounds; not full warm-state propagation')


SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
PROTOCOL_SHA='0db5cea8bb60c1f529e45c48a77a2c8ccd68f03382e65dacb08c95f6e9ca453e'
PINS={'constrained_u_galaxy_horizon_actual_opacity_v001.py': '7b77dad9b5e7b28fad8616325139b526364016087dfa916d31cfe78dc5a18dc1', 'CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001.md': '1933878083169615d6820c791c7d017568778225dc82ada68d8771f1006e8be8', 'CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001_RESULT.json': '59897a17c245dac41a49d02d4961dbaee1a91471997b4cf64f32235fb7f9365b', 'CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001_RECEIPT.json': '1df6d6a4586b0314dae3c189f3b7f099855f402242c4ebbe74417e2cfd1ef70c', 'constrained_u_cubic_radiation_conservation_controls_v002.py': '0d05cef1174178898e69a3ba0849157f2b99e42e08c5603f50464fb7e6ba3f06', 'CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V002.md': '87c11b6814c2376145f694b3c78ebc51d4a1bfc49496d00387868e501a587052', 'CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V002_RESULT.json': '039dfdb022c9918453195d852104bc347fb9bb586d77fac7a88a6ca164d40c57', 'CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V002_RECEIPT.json': 'dcd7c112ae1f0cc4ae46b296481bf01c2582914ea6e7f5a1fff566e82df45a88', 'CONSTRAINED_U_STABLE_ANGULAR_RADIATION_MEMORY_CHART_V001.md': '8471e9d40bb02dca8deed6dfc2bd49e1c4d1f00cd18af456b27df5082e62b04c', 'CONSTRAINED_U_COMOVING_CURVATURE_AND_RELATIVE_VELOCITY_CHART_V002.md': '2e2102548a82167563f6a7b5ff9af558aea4d9cc85f20957daa72c777c5bdb3a', 'actual_opacity_retarded_radiation_kernel_v001.py': 'b43b9def6b0eeaafd12f5f947b8dd77cdf02ab60838951f799fb0bc043bc9721'}

def load_optical_namespace():
    p=BASE/'actual_opacity_retarded_radiation_kernel_v001.py'
    if sha(p)!=OPTICAL_KERNEL_SHA:raise AssertionError('Exact actual-opacity definitions')
    names=('gauss','background_rates','integrals','backward_integrals','inverse_depth','optical_geometry')
    nodes=[n for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise AssertionError('Exact positive map definition set')
    env=dict(np=np,math=math,lru_cache=lru_cache,CP=CP,MPC=MPC,SIGMA_T=6.6524587321e-29,CAP=48.)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<positive-map-definitions>','exec'),env)
    return env

def parent_namespace():
    """Authenticate closed prior action, never load its propagator or main."""
    path=BASE/'constrained_u_galaxy_horizon_actual_opacity_v001.py'
    if sha(path)!=PINS[path.name]:raise AssertionError('Full closed parent source')
    text=path.read_text();tree=ast.parse(text);names=('sha','json_builtin','seal','authenticate','authenticate_completed_parents','finite_tree','validate_checkpoint')
    env=dict(BASE=BASE,np=np,math=math,json=json,ast=ast,hashlib=hashlib,Path=Path,__file__=str(path),TRIALS=TRIALS,OMEGAS=OMEGAS)
    for node in tree.body:
        if isinstance(node,ast.Assign):
            try:value=ast.literal_eval(node.value)
            except (ValueError,TypeError):continue
            for target in node.targets:
                if isinstance(target,ast.Name):env[target.id]=value
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise AssertionError('Exact parent authentication definitions')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path)+'<authentication-only>','exec'),env)
    return env

def authenticate():
    if PENDING_COMPLETED_INPUTS or PROTOCOL_SHA=='PENDING':raise AssertionError('Prospective unsealed source')
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    env=parent_namespace();fixed,inherited=env['authenticate']();SEALS.update(env['SEALS'])
    stem='CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001';result=json.loads((BASE/(stem+'_RESULT.json')).read_text());receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text());lineage=result['lineage']
    if receipt['source_sha256']!=PINS['constrained_u_galaxy_horizon_actual_opacity_v001.py'] or receipt['result_sha256']!=PINS[stem+'_RESULT.json'] or receipt['status']!=result['status'] or receipt['checkpoint_count']!=83:raise AssertionError('Completed actual-opacity binding')
    if len(result['numerical_gates'])!=670 or len(result['optical_map_controls'])!=36 or sum(g['passed'] for g in result['numerical_gates'])!=578 or not all(g['passed'] for g in result['optical_map_controls']) or result['all_numerical_gates_passed']:raise AssertionError('Retain92 actual-opacity failures and36 controls')
    for key in ('input_sha256','output_sha256'):
        for path,h in receipt[key].items():seal(path,h)
    mp=BASE/(stem+'_MANIFEST.json');jp=BASE/(stem+'_JOURNAL.jsonl');seal(mp,receipt['manifest_sha256']);seal(jp,receipt['journal_sha256'])
    if json.loads(mp.read_text())!=lineage:raise AssertionError('Parent exact manifest')
    events=[json.loads(z) for z in jp.read_text().splitlines()];epoch=None;seen=[]
    for i,e in enumerate(events):
        if e['owner']!='root' or type(e['pid']) is not int or e['pid']<=0 or e['source_sha256']!=receipt['source_sha256'] or e['manifest_sha256']!=receipt['manifest_sha256']:raise AssertionError('Parent root/source epoch')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):epoch=e['pid']
        elif e['event']=='CHECKPOINT':
            if e['pid']!=epoch:raise AssertionError('Parent checkpoint epoch')
            label,n=e['trial'],e['nstep'];spec=next(r for r in TRIALS if r[0]==label);pn=stem+'_'+label+'_CP_'+str(n).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json';seal(BASE/pn,e['payload_sha256']);seal(BASE/cn,e['commit_sha256']);commit=json.loads((BASE/cn).read_text());payload=json.loads((BASE/pn).read_text());env['validate_checkpoint'](payload,commit,lineage,label,n,spec[1],spec[2],spec[3]);seen.append((label,n))
        elif e['event']=='OWNER_COMPLETE':
            if i!=len(events)-1 or e['pid']!=epoch or e['result_sha256']!=PINS[stem+'_RESULT.json'] or e['status']!=result['status'] or (e['gate_count'],e['optical_control_count'],e['checkpoint_count'])!=(670,36,83):raise AssertionError('Parent exact terminal record')
        else:raise AssertionError('Parent unexpected event')
    expected=[(r[0],i) for r in TRIALS for i in sorted(set(list(range(0,r[1]+1,128))+[r[1]]))]
    if seen!=expected or len(events)!=85 or events[0]['event']!='OWNER_START' or events[-1]['event']!='OWNER_COMPLETE':raise AssertionError('Full83-pair parent closure')
    control='CONSTRAINED_U_CUBIC_RADIATION_CONSERVATION_CONTROLS_V002';cr=json.loads((BASE/(control+'_RESULT.json')).read_text());cp=json.loads((BASE/(control+'_RECEIPT.json')).read_text());cm=cr['manifest']
    if cp['source_sha256']!=PINS['constrained_u_cubic_radiation_conservation_controls_v002.py'] or cp['result_sha256']!=PINS[control+'_RESULT.json'] or cp['status']!=cr['status'] or cp['checkpoint_count']!=4:raise AssertionError('Manufactured final binding')
    categories={n:all(g['passed'] for g in cr['numerical_gates'] if g['category']==n) for n in ('KERNEL','MIXED','CONSERVATIVE_J','GAUSS_PRODUCT','TRAPEZOID_COMPARATOR')}
    if len(cr['numerical_gates'])!=2398 or categories!=cr['category_dispositions'] or categories!=cp['category_dispositions'] or not cr['conservative_method_qualified'] or not all(categories[n] for n in ('KERNEL','CONSERVATIVE_J','GAUSS_PRODUCT')) or cm['method_panels']!=[16,32,64]:raise AssertionError('Actually qualified bounded method; comparator failures retained')
    for key in ('input_sha256','output_sha256'):
        for path,h in cp[key].items():seal(path,h)
    mp=BASE/(control+'_MANIFEST.json');jp=BASE/(control+'_JOURNAL.jsonl');seal(mp,cp['manifest_sha256']);seal(jp,cp['journal_sha256']);events=[json.loads(z) for z in jp.read_text().splitlines()]
    if json.loads(mp.read_text())!=cm or [e['event'] for e in events]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE'] or any(e['owner']!='root' or e['pid']!=events[0]['pid'] or e['source_sha256']!=cp['source_sha256'] or e['manifest_sha256']!=cp['manifest_sha256'] for e in events):raise AssertionError('Control four-pair natural root closure')
    for stage,e in zip(('KERNEL','COLLISION','PRODUCT','SUMMARY'),events[1:5]):
        pn=control+'_'+stage+'_CP.json';cn=pn[:-5]+'_COMMIT.json';seal(BASE/pn,e['sha256']);seal(BASE/cn,e['commit_sha256']);payload=json.loads((BASE/pn).read_text());commit=json.loads((BASE/cn).read_text())
        if e['stage']!=stage or e['payload']!=pn or commit!=dict(source_sha256=cp['source_sha256'],manifest_sha256=cp['manifest_sha256'],owner='root',pid=events[0]['pid'],stage=stage,payload=pn,sha256=e['sha256']) or payload['manifest']!=cm or payload['stage']!=stage:raise AssertionError('Control exact stage and commit')
    if (events[-1]['controls'],events[-1]['passed'])!=(2398,2301) or events[-1]['result_sha256']!=PINS[control+'_RESULT.json'] or events[-1]['status']!=cr['status']:raise AssertionError('Preserve97 comparator failures')
    inherited.update(actual_opacity_status=result['status'],actual_opacity_dispositions=result['numerical_gates'],actual_opacity_optical_controls=result['optical_map_controls'],manufactured_status=cr['status'],manufactured_dispositions=cr['numerical_gates'],scope='Closed input context and method controls only; no old physical state initializes or forces this attempt')
    return fixed,inherited

def validate_checkpoint(cp,commit,lineage,label,nstep,n,ns,stride):
    finite_tree(cp);required={'lineage','trial','nstep','step_count','ns','stride','states','anchors','snapshots','errors','seed_metadata','initial_moments','los_diagnostics','optical_controls','last_stages'}
    if set(cp)!=required or cp['lineage']!=lineage or (cp['trial'],cp['nstep'],cp['step_count'],cp['ns'],cp['stride'])!=(label,nstep,n,ns,stride) or any(type(cp[k]) is not int for k in ('nstep','step_count','ns','stride')):raise AssertionError('Exact checkpoint metadata')
    lay_n=20+2*ns
    if len(cp['states'])!=4 or any(len(y)!=lay_n for y in cp['states']) or not cp['snapshots'] or cp['snapshots'][-1]['nstep']!=nstep or [c['stable_state'] for c in cp['snapshots'][-1]['cases']]!=cp['states']:raise AssertionError('Entire stable state and exact snapshot closure')
    if any(len(cp[k])!=4 for k in ('anchors','errors','seed_metadata','initial_moments','los_diagnostics','last_stages')):raise AssertionError('Complete four-arm checkpoint axes')
    error_keys={'stage_error','dense_error','momentum_error','discrete_trace_error','los_continuity_error','kernel_tail_bound','discarded_source_bound','gas_temperature_difference_bound','collision_kernel_tail_bound','metric_momentum_error','curvature_increment_error','baryon_Euler_error'}
    if any(set(row)!=error_keys or any(v<0 for v in row.values()) for row in cp['errors']):raise AssertionError('Complete nonnegative error prefix')
    seed_keys={'asymptotic_curvature','A','x','m','phi1','psi1','sigma2','native_z6','finite_normal_shift','finite_curvature','scope'}
    if any(set(row)!=seed_keys or len(row['native_z6'])!=ns for row in cp['seed_metadata']) or any(set(row)!= {'nu','photon','polarization'} or any(len(row[k])!=5 for k in row) for row in cp['initial_moments']):raise AssertionError('Entire original seed and shifted angular state schema')
    controls={'inverse_depth_error','optical_integral_error','conformal_integral_error','optical_mass_error','measure_identity_error','source_quadrature_error'}
    if set(cp['optical_controls'])!=controls or any(v<0 for v in cp['optical_controls'].values()):raise AssertionError('Complete optical prefix')
    source_keys={'x','eta','R','qV','cGamma','Gamma','dipole','Pi'}
    for history in cp['anchors']:
        if len(history)!=1+nstep//stride or not history or set(history[0])!=source_keys:raise AssertionError('Complete source-panel census')
        for i,row in enumerate(history):
            if i==0:continue
            if set(row)!=source_keys|{'panel_nodes','panel_envelopes'} or len(row['panel_nodes'])!=4 or len(row['panel_envelopes'])!=3 or any(v<0 for v in row['panel_envelopes']) or any(set(p)!=source_keys for p in row['panel_nodes']):raise AssertionError('Exact finite nonrecursive cubic source schema')
            pp=row['panel_nodes']
            if any(pp[j]['eta']>=pp[j+1]['eta'] or pp[j]['x']>=pp[j+1]['x'] for j in range(3)) or pp[0]!={k:v for k,v in history[i-1].items() if k not in ('panel_nodes','panel_envelopes')} or pp[-1]!={k:v for k,v in row.items() if k not in ('panel_nodes','panel_envelopes')}:raise AssertionError('Actual ordered cubic panel endpoint closure')
    prefix=128 if label=='START' else 0;common=n-prefix;expected=[0]+[i for i in range(1,nstep+1) if i>=prefix and (i-prefix)%(common//32)==0]
    if [s['nstep'] for s in cp['snapshots']]!=expected:raise AssertionError('Exact snapshot prefix')
    snapshot_keys={'x','a','state','stable_state','background','thermal','Phi','Psi','Q','reaction_denominator','n_U','sigma','P','pi_U','Z','Zd','readouts','normal_terms','stable_normal_terms','normal_stable_residual','normal_raw_residual','current_derivative_contacts','normal_floor','normal_error','omitted_Euler_terms','omitted_Euler_floor','omitted_Euler_error','trace_terms','trace_floor','trace_error','domain_heads','signed_sources','source_ratios','stable_coordinates','gas_source_bound'}
    for frame in cp['snapshots']:
        if set(frame)!= {'nstep','cases'} or len(frame['cases'])!=4:raise AssertionError('Full frame schema')
        for case in frame['cases']:
            if set(case)!=snapshot_keys or len(case['state'])!=lay_n or len(case['stable_state'])!=lay_n or len(case['readouts'])!=15 or len(case['normal_terms'])!=7 or len(case['stable_normal_terms'])!=7 or len(case['omitted_Euler_terms'])!=5 or len(case['trace_terms'])!=7 or type(case['domain_heads']['inside_sampled_linear_domain']) is not bool or case['reaction_denominator']<=0:raise AssertionError('Entire physical/stable snapshot schema')
    los_names={'delta_gamma','Hstar_u_gamma','delta_nu','Hstar_u_nu','F_gamma_2','F_nu_2','G_gamma_0','G_gamma_2'}
    for row in cp['los_diagnostics']:
        if set(row)!=los_names:raise AssertionError('All eight independent memory rows')
        for value in row.values():
            if set(value)!= {'maximum','location'} or value['maximum']<0:raise AssertionError('LOS maximum schema')
            loc=value['location']
            if loc is not None and (set(loc)!= {'nstep','a','residual','scale','old_state','new_state','gauss_stage_rates','log_step'} or len(loc['gauss_stage_rates'])!=2 or not 1<=loc['nstep']<=nstep or loc['scale']<0 or loc['log_step']<=0):raise AssertionError('Actual per-row location schema')
    for stage,state in zip(cp['last_stages'],cp['states']):
        if (stage is None)!=(nstep==0):raise AssertionError('Exact last-stage presence')
        if stage is not None:
            if set(stage)!= {'x','dx','coordinates','conformal','previous','states','algebraic_states','stage_error','dense_error'} or len(stage['states'])!=3 or any(len(y)!=lay_n for y in stage['states']) or len(stage['algebraic_states'])!=3 or any(len(y)!=2 for y in stage['algebraic_states']) or stage['states'][-1]!=state or len(stage['previous'])!=lay_n or len(stage['coordinates'])!=3 or len(stage['conformal'])!=3:raise AssertionError('All kinetic stage/output and reaction schema')
    pn=STEM+'_'+label+'_CP_'+str(nstep).zfill(6)+'.json'
    if commit!=dict(lineage=lineage,trial=label,nstep=nstep,payload=pn,sha256=sha(BASE/pn)):raise AssertionError('Exact commit bytes')


def main():
    global SOURCE_SHA,MANIFEST_SHA
    terminal=[BASE/(STEM+suffix) for suffix in ('_RESULT.json','_REPORT.md','_RECEIPT.json')]
    if any(p.exists() for p in terminal):raise FileExistsError('No completed output overwrite')
    if list(BASE.glob(STEM+'_FAILED*')):raise FileExistsError('Preserved failure requires a NEW attempt')
    manifest_path=BASE/(STEM+'_MANIFEST.json');journal_path=BASE/(STEM+'_JOURNAL.jsonl')
    if not manifest_path.exists() and (journal_path.exists() or list(BASE.glob(STEM+'_*_CP_*.json'))):raise AssertionError('Pre-manifest orphan refusal')
    SOURCE_SHA=sha(__file__);fixed,inherited=authenticate();helpers=load_declared_helpers();tick=time.monotonic()
    lineage=dict(source_sha256=SOURCE_SHA,inputs=dict(SEALS),fixed=fixed,trials=TRIALS,omegas=OMEGAS,numpy_version=np.__version__,
        numerical_method=dict(optical_kernel_sha256=OPTICAL_KERNEL_SHA,quadrature_order=16,independent_order=32,optical_cutoff=48.,inverse_iterations=16,collocation='two-stage Gauss in log a, full kinetic stage/output states',source_interpolant='cubic through actual conformal left/stage1/stage2/output nodes, panelwise DeltaR IBP',velocity_coordinates='U=Jrelative/(B+G), W=wg-wb with actual moving weights',core_gate_count=670,separate_optical_control_count=36))
    lineage=json_builtin(lineage)
    if manifest_path.exists():
        if json.loads(manifest_path.read_text())!=lineage:raise AssertionError('Exact same-lineage recovery only')
        MANIFEST_SHA=sha(manifest_path);CREATED[str(manifest_path)]=MANIFEST_SHA;validate_journal(lineage);journal('OWNER_RESUME')
    else:
        MANIFEST_SHA=write(STEM+'_MANIFEST.json',lineage);journal('OWNER_START')
    rows=[]
    for spec in TRIALS:rows.append(run_trial(spec,fixed,helpers,lineage))
    gates=[]
    def check(label,error,tolerance,**fields):
        error=float(error);gates.append(dict(label=label,error=error,tolerance=tolerance,passed=bool(math.isfinite(error) and error<=tolerance),**fields))
    for row in rows:
        check('conformal_grid',row['eta_quadrature_error'],2e-11,trial=row['label'])
        check('bounded_horizon_kernel_range',max(0.,row['endpoint_phase']-8),0.,trial=row['label'])
        for arm,om in enumerate(OMEGAS):
            check('asymptotic_curvature_normalization',abs(row['seed'][arm]['A']*(1.5+2*(1-fixed['fgamma'])/5)/CURVATURE-1),2e-13,trial=row['label'],omega=om)
            first=row['snapshots'][0]['cases'][arm]
            check('initial_exact_normal_construction',first['normal_error'],1e-10,trial=row['label'],omega=om)
            q=K*CP/(1000*fixed['Hunit']*first['a'])
            check('initial_exact_shear_construction',abs((first['Psi']-first['Phi']-2*first['signed_sources']['shear']/q**2)/CURVATURE),2e-13,trial=row['label'],omega=om)
            for kind,error in row['initial_transport_errors'][arm].items():check('initial_angular128_256_'+kind,error,2e-11,trial=row['label'],omega=om)
            err=row['errors'][arm]
            for key,tol in [('stage_error',2e-11),('dense_error',2e-11),('momentum_error',1e-5),('discrete_trace_error',1e-5),('los_continuity_error',1e-3)]:check(key,err[key],tol,trial=row['label'],omega=om)
            for key,tol in [('normal_error',1e-10),('trace_error',1e-9),('omitted_Euler_error',1e-9)]:check(key,max(s['cases'][arm][key] for s in row['snapshots']),tol,trial=row['label'],omega=om)
            check('discarded_radiation_source_absolute',err['discarded_source_bound']/CURVATURE,1e-12,trial=row['label'],omega=om)
    names=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RESULT.json').read_text())['readout_names']
    fine=rows[2];fine_values=np.array([[c['readouts'] for c in s['cases']] for s in fine['snapshots']])
    comparisons=[]
    for index,label,tol in [(1,'time',1e-3),(3,'modes',1e-3),(4,'source_panel',1e-3),(5,'start',2e-4)]:
        row=rows[index];values=np.array([[c['readouts'] for c in s['cases']] for s in row['snapshots']])
        # START advances an extra128 steps then the identical2048-step common grid.
        # No state or amplitude interpolation is used for the START comparison.
        if label=='start':
            common_snapshots=[s for s in row['snapshots'] if s['nstep']>=128]
            if [s['nstep']-128 for s in common_snapshots]!=[s['nstep'] for s in fine['snapshots']]:raise AssertionError('Exact common physical START grid')
            values=np.array([[c['readouts'] for c in s['cases']] for s in common_snapshots])
        den=np.maximum(np.max(abs(fine_values),axis=0),CURVATURE*1e-8);dif=values-fine_values;error=np.max(abs(dif),axis=0)/den
        for arm,om in enumerate(OMEGAS):
            for k,name in enumerate(names):check(label+'_refinement',error[arm,k],tol,omega=om,variable=name)
        comparisons.append(dict(label=label,signed_endpoint_difference=dif[-1].tolist(),maximum_absolute_difference=np.max(abs(dif),axis=0).tolist(),normalization=den.tolist(),normalized_error=error.tolist()))
    fixture=[]
    for row in rows:
        for arm,om in enumerate(OMEGAS):
            bounds=[s['cases'][arm]['gas_source_bound'] for s in row['snapshots']]
            fixture.append(dict(trial=row['label'],omega=om,maximum_instantaneous_gas_source=max(b['omitted_velocity_source_ratio'] for b in bounds),ceiling=1e-4,
                passed=bool(max(b['omitted_velocity_source_ratio'] for b in bounds)<=1e-4),scope='Instantaneous omitted-source norm only; no propagated error qualification'))
    # Newly needed l3/l4/r4 functions are independently checked before use is
    # called numerically qualified; the older10744 census remains separate.
    mu,ww=gauss(128)
    for ell in (3,4):
        for derivative in range(5):
            for xx in (0.,.1,1.,4.,8.):
                reference=(1j**ell/2)*np.dot(ww,legendre(ell,mu)*(-1j*mu)**derivative*np.exp(-1j*xx*mu))
                error=abs(float(bessel(ell,derivative,xx))-reference.real)
                check('extra_bessel_angular',error,2e-11,ell=ell,derivative=derivative,x=xx)
        uu,vv=gauss(64)
        for left,right in zip((0.,.25,1.,4.),(.25,1.,4.,8.)):
            middle=(left+right)/2;half=(right-left)/2
            direct=half*float(np.dot(vv,bessel(ell,0,middle+half*uu)))
            check('extra_primitive_increment',abs(float(primitive(ell,right)-primitive(ell,left))-direct),2e-11,ell=ell,left=left,right=right)
    if len(gates)!=670:raise AssertionError('Frozen670 numerical gate census')
    optical_controls=[]
    for row in rows:
        for name,error in row['optical_controls'].items():
            optical_controls.append(dict(trial=row['label'],name=name,error=float(error),tolerance=2e-11,passed=bool(math.isfinite(error) and error<=2e-11)))
    if len(optical_controls)!=36:raise AssertionError('Separate frozen36 actual-opacity controls')
    qualified=all(g['passed'] for g in gates+optical_controls)
    result=dict(status='COUPLED_HORIZON_ARITHMETIC_PASS' if qualified else 'COUPLED_HORIZON_ARITHMETIC_FAILED',all_numerical_gates_passed=qualified,
        lineage=lineage,inherited=inherited,rows=rows,numerical_gates=gates,comparisons=comparisons,gas_fixture_flags=fixture,
        numerical_gate_count=len(gates),optical_map_controls=optical_controls,readout_names=names,elapsed_seconds=time.monotonic()-tick,
        scope='NEW same-action k10 horizon interval; no halo/galaxy/observational fit, no qualified failed k.01 baseline; cold ideal ordinary plasma and separate local omission flags')
    recheck();rh=write(STEM+'_RESULT.json',result)
    text='# Coupled stable angular radiation and conservative Gauss horizon test V001\n\n'+result['status']+'\n\n'+str(sum(g['passed'] for g in gates))+'/'+str(len(gates))+' original numerical controls PASS; '+str(sum(g['passed'] for g in optical_controls))+'/36 additional actual-opacity controls PASS.\n\nFirst horizon window k=10/Mpc; all four inertias, true initial angular transport, physical implicit metric/native sources. Stable angular memory and literal relative-momentum Gauss increments replace the mixed endpoint update; all prior failures remain. Gas source flags are instantaneous bounds. The earlier k=.01 attempt retains375PASS/152FAIL.\n'
    # Keep report under the same byte-exclusive, preencoded writer schema.
    report_path=BASE/(STEM+'_REPORT.md')
    with report_path.open('xb') as f:f.write(text.encode())
    report_path.chmod(0o444);CREATED[str(report_path)]=sha(report_path)
    if len(list(BASE.glob(STEM+'_*_CP_*_COMMIT.json')))!=83:raise AssertionError('Frozen83 complete checkpoints')
    validate_journal(lineage)
    journal('OWNER_COMPLETE',status=result['status'],result_sha256=rh,gate_count=len(gates),optical_control_count=36,checkpoint_count=83)
    journal_path.chmod(0o444);CREATED[str(journal_path)]=sha(journal_path);recheck()
    receipt=dict(status=result['status'],source_sha256=SOURCE_SHA,input_sha256=dict(SEALS),output_sha256=dict(CREATED),result_sha256=rh,
        report_sha256=sha(report_path),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(journal_path),checkpoint_count=83)
    write(STEM+'_RECEIPT.json',receipt);recheck()
    return 0 if qualified else 3

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    if not args.execute:raise SystemExit('Root scientific execution requires --execute after frozen full preflight')
    refuse_closed_prefix()
    try:raise SystemExit(main())
    except Exception:
        # This disjoint attempt preserves every committed source-history/state byte;
        # no timeout, forced termination, old attempt recovery or automatic rerun.
        path=BASE/(STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json')
        write(path.name,dict(source_sha256=SOURCE_SHA,traceback=traceback.format_exc(),created=dict(CREATED)))
        raise
