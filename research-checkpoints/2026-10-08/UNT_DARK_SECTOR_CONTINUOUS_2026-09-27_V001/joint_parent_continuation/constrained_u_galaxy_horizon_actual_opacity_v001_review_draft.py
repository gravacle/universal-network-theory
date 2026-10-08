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
STEM='CONSTRAINED_U_GALAXY_HORIZON_ACTUAL_OPACITY_V001'
PENDING_COMPLETED_INPUTS=True
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

def load_optical_kernel():
    p=BASE/'actual_opacity_retarded_radiation_kernel_v001.py'
    if sha(p)!=OPTICAL_KERNEL_SHA:raise AssertionError('Exact actual-opacity helper bytes')
    tree=ast.parse(p.read_text());names=('gauss','background_rates','integrals','backward_integrals','inverse_depth','optical_geometry','source_weights','OpticalKernel')
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise AssertionError('Exact actual-opacity definition set')
    namespace=dict(np=np,math=math,lru_cache=lru_cache,CP=CP,MPC=MPC,SIGMA_T=6.6524587321e-29,CAP=48.)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p)+'<declared-definitions>','exec'),namespace)
    return namespace['OpticalKernel']


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

def panel(l,r,p,a,b,offset=0.,order=16):
    """Finite-opacity affine source integral in conformal LENGTH, normalized Delta1."""
    u,w=gauss(order);end=min(a,48.) if a>48 else 1.
    rate=max(1.,b/a) if a>48 else max(1.,a,b);pieces=max(1,math.ceil(end*rate/8));parts=[]
    for i in range(pieces):
        left=end*i/pieces;right=end*(i+1)/pieces;t=(left+right)/2+(right-left)*u/2
        v=t/a if a>48 else t;jac=1/a if a>48 else 1.
        parts.append(float((right-left)*jac/2*np.dot(w,np.exp(-a*v)*v**p*bessel(l,r,offset+b*v))))
    return math.fsum(parts),math.exp(-48)/a if a>48 else 0.

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

def physical_vectors(x,fixed,lay,therm,snodes,weights,omega,helpers):
    """Every source/multiplier remains that of the authenticated full action."""
    eye=np.eye(lay.n);f=helpers['coefficients'](x,eye,fixed,lay,therm,snodes,weights,omega)
    return f,eye,f['phi'],eye[0],eye[3],4*f['q']*eye[2],eye[lay.fg[2]]+eye[lay.pol[0]]+eye[lay.pol[2]]

def cn_block_solve(matrix,rhs,lay):
    """Only kinetic2x2 blocks eliminated; all modes return in the full state."""
    original=matrix;original_rhs=rhs;matrix,rhs,columns=equilibrate(matrix,rhs)
    core=np.array([i for i in range(lay.n+2) if i not in set(lay.z)|set(lay.zd)])
    s=matrix[np.ix_(core,core)].copy();saved=[]
    for z,v in zip(lay.z,lay.zd):
        ix=np.array([z,v]);k=matrix[np.ix_(ix,ix)]
        inverse=np.linalg.solve(k,np.eye(2));transfer=inverse@matrix[np.ix_(ix,core)]
        coupling=matrix[np.ix_(core,ix)];s-=coupling@transfer;saved.append((ix,inverse,transfer,coupling))
    def solve_balanced(b):
        r=b[core].copy();mode_rhs=[]
        for ix,inverse,transfer,coupling in saved:
            local=inverse@b[ix];r-=coupling@local;mode_rhs.append(local)
        out=np.zeros(lay.n+2);out[core]=np.linalg.solve(s,r)
        for (ix,inverse,transfer,coupling),local in zip(saved,mode_rhs):out[ix]=local-transfer@out[core]
        return out
    balanced=solve_balanced(rhs);out=columns*balanced
    # Three fixed binary64 compensated residual corrections are declared before
    # outcomes. No least-squares/pseudoinverse or state/tolerance selection.
    for _ in range(3):
        residual=np.array([math.fsum(float(a*b) for a,b in zip(row,out))-float(r) for row,r in zip(original,original_rhs)])
        # Recover the same fixed row scaling from A_e=R A C and b_e=R b;
        # equilibration is linear also for an arbitrary correction RHS.
        ae,be,ce=equilibrate(original,-residual)
        out+=columns*solve_balanced(be)
    residual=np.array([math.fsum(float(a*b) for a,b in zip(row,out))-float(r) for row,r in zip(original,original_rhs)])
    scale=abs(original)@abs(out)+abs(original_rhs)
    return out,float(np.max(abs(residual)/np.maximum(scale,CURVATURE*1e-18)))

def coupled_endpoint(previous,previous_rates,x,dx,eta,anchors,fixed,lay,therm,snodes,weights,omega,helpers,initial_moments,initial_values,optical,dense=False):
    """Same implicit action; every photon source uses actual optical depth."""
    na=lay.n+2;matrix=np.eye(na)-dx*helpers['stage_matrix'](x,fixed,lay,therm,snodes,weights,omega)/2
    rhs=np.r_[previous+dx*previous_rates/2,0.,0.]
    aug=helpers['stage_matrix'](x,fixed,lay,therm,snodes,weights,omega)
    matrix[lay.n:]=aug[lay.n:];rhs[lay.n:]=0.
    f,eye,phi,psi,F0,dipole,Pi=physical_vectors(x,fixed,lay,therm,snodes,weights,omega,helpers)
    momentum_row=matrix[0].copy();momentum_rhs=float(rhs[0])
    matrix[0,:lay.n]=(f['q']**2*psi+3*f['h']*f['mom']+f['b']*eye[1]
        +f['rg']*eye[3]+f['rn']*eye[5]+f['w']*eye[7]
        -f['q']*(KB*f['q']*f['ncalc']/2+CBAR*f['Z']))
    matrix[0,lay.n:]=0.;rhs[0]=0.
    k=K;last=anchors[-1];deta=eta-last['eta']
    current=optical.geometry(last['x'],x,last['eta'],eta)
    past=[optical.geometry(left['x'],right['x'],left['eta'],right['eta']) for left,right in zip(anchors[:-1],anchors[1:])]
    depths=np.array([g['depth'] for g in past]);a=current['depth']
    future_tau=a+np.r_[np.cumsum(depths[::-1])[::-1][1:],0.] if len(depths) else np.array([])
    visibility=math.exp(-min(745.,a+math.fsum(float(t) for t in depths)))
    all_eta=np.array([r['eta'] for r in anchors]);all_sums=np.array([r['phi']+r['psi'] for r in anchors]);widths=np.diff(all_eta)
    nmat=np.zeros((5,na));gmat=np.zeros((5,na));nconstant=np.zeros(5);gconstant=np.zeros(5);pconstant=np.zeros(5)
    discarded_bound=0.;panel_bound=0.;collision_tail_bound=0.
    history=[]
    for j,geometry in enumerate(past):
        left,right=anchors[j],anchors[j+1];width=geometry['width'];atten=math.exp(-min(float(future_tau[j]),745.))
        metric_envelope=4*abs(right['psi']-left['psi'])/width+4*k*max(abs(left['phi']),abs(right['phi']))
        collision_envelope=max(abs(left['F0']),abs(right['F0']))+max(abs(left['dipole']),abs(right['dipole']))+2.5*max(abs(left['Pi']),abs(right['Pi']))
        if future_tau[j]>48:
            discarded_bound+=5*atten*(metric_envelope*min(width,1/geometry['minimum_gamma'])+collision_envelope)
            continue
        metric,collision=optical.weights(geometry,k*(eta-right['eta']),bessel)
        history.append((left,right,atten,metric,collision,width))
        discarded_bound+=5*atten*(metric_envelope*geometry['metric_tail']+collision_envelope*geometry['collision_tail'])
        panel_bound+=atten*geometry['metric_tail'];collision_tail_bound+=atten*geometry['collision_tail']
    metric,collision=optical.weights(current,0.,bessel)
    for l in range(5):
        delta=eta-all_eta[0];nconstant[l]=float(initial_values['nu'][l])+4*anchors[0]['phi']*float(bessel(l,0,k*delta))
        if l==0:nmat[l,:lay.n]-=4*phi
        if len(widths):
            primitive_values=primitive(l,k*(eta-all_eta));memory_weights=(primitive_values[:-1]-primitive_values[1:])/k
            nconstant[l]+=float(4*np.dot(np.diff(all_sums)/widths,memory_weights))
        weight=float((primitive(l,k*deta)-primitive(l,0.))/k)
        nmat[l,:lay.n]+=4*(phi+psi)*weight/deta;nconstant[l]-=4*all_sums[-1]*weight/deta
        gconstant[l]=visibility*float(initial_values['photon'][l]);pconstant[l]=visibility*float(initial_values['polarization'][l])
        for left,right,atten,mw,cw,width in history:
            def affine(name,v):return right[name]*(v[0]-v[1])+left[name]*v[1]
            gconstant[l]+=atten*(4*(right['psi']-left['psi'])*mw[l,0,0]/width+4*k*affine('phi',mw[l,1])
                +affine('F0',cw[l,0])+affine('dipole',cw[l,1])+affine('Pi',cw[l,0]+3*cw[l,2])/4)
            pconstant[l]+=atten*3*affine('Pi',cw[l,0]+cw[l,2])/4
        m0,m1=metric[l,0],metric[l,1];c0,c1,c2=collision[l,0],collision[l,1],collision[l,2]
        gmat[l,:lay.n]+=4*psi*m0[0]/deta+4*k*phi*(m1[0]-m1[1])+F0*(c0[0]-c0[1])+dipole*(c1[0]-c1[1])+Pi*((c0[0]-c0[1])+3*(c2[0]-c2[1]))/4
        gconstant[l]+=-4*last['psi']*m0[0]/deta+4*k*last['phi']*m1[1]+last['F0']*c0[1]+last['dipole']*c1[1]+last['Pi']*(c0[1]+3*c2[1])/4
        row=lay.pol[l];matrix[row]=np.r_[eye[row],0.,0.]
        matrix[row,:lay.n]-=3*Pi*((c0[0]-c0[1])+(c2[0]-c2[1]))/4
        rhs[row]=3*last['Pi']*(c0[1]+c2[1])/4+pconstant[l]
    for l in range(5):
        if l==0:gi,ni,gv,nv=3,5,eye[3],eye[5]
        elif l==1:gi,ni,gv,nv=4,6,4*f['q']*eye[4]/3,4*f['q']*eye[6]/3
        else:gi,ni,gv,nv=lay.fg[l],lay.fn[l],eye[lay.fg[l]],eye[lay.fn[l]]
        matrix[gi]=np.r_[gv,0.,0.]-gmat[l];rhs[gi]=gconstant[l]
        matrix[ni]=np.r_[nv,0.,0.]-nmat[l];rhs[ni]=nconstant[l]
    solution,residual=cn_block_solve(matrix,rhs,lay)
    dense_error=0.
    if dense:
        em,er,ec=equilibrate(matrix,rhs);independent=ec*np.linalg.solve(em,er)
        for _ in range(3):
            dense_residual=np.array([math.fsum(float(a*b) for a,b in zip(row,independent))-float(r) for row,r in zip(matrix,rhs)])
            _,correction,_=equilibrate(matrix,-dense_residual);independent+=ec*np.linalg.solve(em,correction)
        dense_error=float(np.max(abs(solution-independent))/max(float(np.max(abs(independent))),CURVATURE*1e-18))
    final=anchor(x,eta,solution[:lay.n],fixed,lay,therm,snodes,weights,omega,helpers)
    metric_envelope=4*abs(final['psi']-last['psi'])/deta+4*k*max(abs(last['phi']),abs(final['phi']))
    collision_envelope=max(abs(last['F0']),abs(final['F0']))+max(abs(last['dipole']),abs(final['dipole']))+2.5*max(abs(last['Pi']),abs(final['Pi']))
    discarded_bound+=5*(metric_envelope*current['metric_tail']+collision_envelope*current['collision_tail'])
    panel_bound+=current['metric_tail'];collision_tail_bound+=current['collision_tail']
    momentum_error=abs(float(momentum_row@solution)-momentum_rhs)/max(float(abs(momentum_row)@abs(solution))+abs(momentum_rhs),CURVATURE*1e-18)
    return solution[:lay.n],dict(stage_error=residual,dense_error=dense_error,momentum_error=momentum_error,opacity=a,kernel_tail_bound=panel_bound,
        collision_kernel_tail_bound=collision_tail_bound,discarded_source_bound=discarded_bound)



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


def anchor(x,eta,y,fixed,lay,therm,snodes,weights,omega,helpers):
    f=helpers['coefficients'](x,y,fixed,lay,therm,snodes,weights,omega)
    return dict(x=float(x),eta=float(eta),gamma_eta=float(f['g']*K/f['q']),phi=float(f['phi']),psi=float(y[0]),
        F0=float(y[3]),dipole=float(4*f['q']*y[2]),Pi=float(y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]))


def initial_multipoles(y,lay,q):
    return dict(nu=[float(y[5]),float(4*q*y[6]/3)]+[float(y[lay.fn[l]]) for l in (2,3,4)],
        photon=[float(y[3]),float(4*q*y[4]/3)]+[float(y[lay.fg[l]]) for l in (2,3,4)],
        polarization=[float(y[lay.pol[l]]) for l in range(5)])


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


SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None
COMPILER_SHA='179301dcb41ea78accc3fa0048a7e6f6710d891945a751a34addd622020c1818'
PROTOCOL_SHA='681b2cd2251c84aee4d164ded62234eed1a9738bc16bcc6990a0557062bb0675'
PINS={'constrained_u_clock_gradient_early_transfer_v004.py': 'a4e78b6467b0ba5884c8da2081ff580378b4afb839a90cec548fcf30a389fa07', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004.md': '8d7f33f6b336488e92ed6b516dd196a66f7ee2929bda5a72e7a258fe34ac9cd5', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_MANIFEST.json': '3a62d2b2636ebc66273ac162ee333233c98ec30949d55265a17a6d79cca43ce8', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RESULT.json': '2df066c32b5140d91e2194166940128e92611d7c1ab5d97ae8846fdc73e565c2', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RECEIPT.json': 'b4959fb0e1c07179e34ab6a3de0e8075162f87624d7c9e2a8ecd83b16b1ab564', 'CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V002.md': '2d66ca4ec9c35bcd67c29914d29a634c1968ed1c2e7e8ab5eb7ba99cdf5b1f47', 'constrained_u_retarded_radiation_kernel_controls_v001.py': 'dc7885ee0349145f05a7e18bf9ce48bf257626ebbc4bd48ebc366791fe456db2', 'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001.md': '4595af8edae0cf29607d3436c4d5a91fb9fe2ead4690ae58e5f77b72af0fd29a', 'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_RESULT.json': 'b541b0a5e3f2ea1827f166907f96e9b76bf2d2ad4c6366c3a0efbf15a7661530', 'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001_RECEIPT.json': '9e845b9a18035b4b199ac0f3a6153b4123f1816c353bdec0e0ef7fdaddaf19dc', 'constrained_u_early_pair_opacity_bound_v003.py': '249055abe2e28a879fc870674b9965d741762e0b25a8bea10ca0e3f1f95642a7', 'CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V003.md': 'c9af8663b32739efb9dc3afadc665ffe856b25b69e9a41bdc04ddd57049a3940', 'CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V003_RESULT.json': '6b02d25d7dd67273c0b9bc586825ff4eedaa8c812fc40490c68543926d9d1a1e', 'CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V003_RECEIPT.json': '2f8846a88520e031dbbf5021aef7cd2a9689e0d54a6e359f3898858af3aefc31', 'constrained_u_galaxy_horizon_volterra_v001.py': 'd7ad71b86ba33f80092bc39dd694c067adfff2d451e28cc27984db23b0d6d85c', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V001.md': 'cf03088b96971b5ec7b9bca73bf9bba1709b095a0e75b1563b064a220fd60ee5', 'constrained_u_galaxy_horizon_volterra_v002.py': '4af809165f70dbf9ecc8193be928b5154c00cd486fbe891ace79bf16c2974333', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V002.md': 'ab3c1d1ba772992f41c2b0e7892ee03f4073af1d234f7527f2870d0bb2d01310', 'actual_opacity_retarded_radiation_kernel_v001.py': 'b43b9def6b0eeaafd12f5f947b8dd77cdf02ab60838951f799fb0bc043bc9721', 'constrained_u_actual_opacity_kernel_controls_v001.py': '23ff005476d5a104175d3a5a6e30cbf8da4a64a88ac19ca936babc21f5a2c5a3', 'CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001.md': '7441534bf4335c08dd46be7b33d59a87ab7e087d0507f137265cbae0e04292a0', 'CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001_RESULT.json': 'f59da94c6cec859618210adc64cb2a4ddb42e911afd48d8daf47527a3085b7fb', 'CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001_RECEIPT.json': '60a2a57efb71a8653da5ea993dd291601f275cf86d4bb24c8bcf1e960e7d2a80', 'constrained_u_galaxy_horizon_volterra_v003.py': '06823e14186e3dec4a20b13206ceb3b5fd4824e166f09c2a856083e276b5b273', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003.md': 'f3ec83a84bee7291b73a02ba73d48a793ab0ec7a081baa34a963ab5e5f27fc7d', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003_RESULT.json': 'PENDING', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003_RECEIPT.json': 'PENDING'}
HELPER_SPANS={'background': 'eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2', 'Thermal': '0d4c6a2726fd817d2cfb5ba8b90a6674a288bc0484c927da719ecdef72a7cd47', 'Layout': 'f199860c3687d2acc7817eda8a00133c1ef57abb2ffbf224ddc760a90e41d2a8', 'coefficients': 'b9e6a7edca9a67031670d32dba146c289347b9253f32bf16d0f3587597125637', 'rates': '2053ec557e765a899a9468fed8a48d701e010d2f76a0aa666ab209e8dc079354', 'stage_matrix': '0b02c3bb7a1c4d2d4a9ce6e5ddfe964965042d013ba916d50a4eeda63cb040fe', 'snapshot': '842bef984f2904f4eabdb467fc1bdd6e90f83d472874507c57dbd8aea8d62b7f'}

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


def authenticate():
    if PENDING_COMPLETED_INPUTS or PROTOCOL_SHA=='PENDING':raise AssertionError('Prospective unsealed authoring bytes')
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    text=(BASE/'constrained_u_clock_gradient_early_transfer_v004.py').read_text();tree=ast.parse(text)
    for name,h in HELPER_SPANS.items():
        node=next(n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name==name)
        if hashlib.sha256(ast.get_source_segment(text,node).encode()).hexdigest()!=h:raise AssertionError('Exact declared helper span '+name)
    parent=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_MANIFEST.json').read_text())
    for path,h in parent['inputs'].items():seal(path,h)
    old=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RESULT.json').read_text())
    gates=old['numerical_gates']
    if len(gates)!=527 or sum(bool(g['passed']) for g in gates)!=375 or old['all_numerical_gates_passed']:raise AssertionError('Preserved failed parent dispositions')
    old_receipt=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RECEIPT.json').read_text())
    if old_receipt['result_sha256']!=PINS['CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_RESULT.json'] or old_receipt['source_sha256']!=EARLY_SOURCE_SHA or old_receipt['lineage']!=parent or old_receipt['status']!=old['status']:raise AssertionError('Failed parent exact closure/ledger identity')
    for path,h in old_receipt['checkpoint_seals'].items():seal(path,h)
    seal(BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_JOURNAL.jsonl',old_receipt['journal_sha256'])
    old_events=[json.loads(s) for s in (BASE/'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V004_JOURNAL.jsonl').read_text().splitlines()]
    if old_events[0]['event']!='OWNER_START' or old_events[-1]['event']!='OWNER_COMPLETE' or any(e.get('owner')!='root' or e.get('source_sha256')!=EARLY_SOURCE_SHA or type(e.get('pid')) is not int or e['pid']<=0 for e in old_events):raise AssertionError('Failed parent natural root closure')
    for stem,count,input_key in [('CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001',10744,'input_sha256'),('CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V003',8,'inputs')]:
        receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text());result=json.loads((BASE/(stem+'_RESULT.json')).read_text())
        source_name={'CONSTRAINED_U_RETARDED_RADIATION_KERNEL_CONTROLS_V001':'constrained_u_retarded_radiation_kernel_controls_v001.py',
            'CONSTRAINED_U_EARLY_PAIR_OPACITY_BOUND_V003':'constrained_u_early_pair_opacity_bound_v003.py'}[stem]
        if receipt['result_sha256']!=PINS[stem+'_RESULT.json'] or receipt['source_sha256']!=PINS[source_name] or receipt['status']!=result['status']:raise AssertionError('Actual source/result/receipt pin')
        for path,h in receipt[input_key].items():seal(path,h)
        for path,h in receipt['output_sha256'].items():seal(path,h)
        seal(BASE/(stem+'_MANIFEST.json'),receipt['manifest_sha256']);seal(BASE/(stem+'_JOURNAL.jsonl'),receipt['journal_sha256'])
        if stem.endswith('V003'):
            if len(result['numerical_controls'])!=8 or len(result['approximation_flags'])!=12 or not result['all_numerical_passed'] or not result['all_conditional_fixture_flags_passed'] or not all(g['passed'] for g in result['numerical_controls']+result['approximation_flags']):raise AssertionError('Ordinary pair start premise refused')
        else:
            if result['check_count']!=10744 or result['failed_checks'] or result['status']!='PASS_KERNEL_ARITHMETIC':raise AssertionError('Kernel arithmetic refused')
    fixed=dict(parent['fixed']);fixed.update(k_Mpc_inverse=K,curvature=CURVATURE)
    continuation=authenticate_completed_parents(parent)
    return fixed,dict(parent_status=old['status'],parent_counts=dict(PASS=375,FAIL=152),horizon_attempt=continuation,
        pair_flags='12/12 only conditional source flags; full chemical opacity derivative unqualified')


def authenticate_completed_parents(old_manifest):
    """No unfinished inputs; all old physical/numerical failures remain owned."""
    stem='CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003'
    result=json.loads((BASE/(stem+'_RESULT.json')).read_text());receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
    if (len(result['numerical_gates'])!=670 or result['numerical_gate_count']!=670
        or result['all_numerical_gates_passed']!=all(g['passed'] for g in result['numerical_gates'])
        or result['status']!=receipt['status'] or receipt['checkpoint_count']!=83
        or receipt['source_sha256']!=PINS['constrained_u_galaxy_horizon_volterra_v003.py']
        or receipt['result_sha256']!=PINS[stem+'_RESULT.json']
        or result['lineage']['source_sha256']!=receipt['source_sha256']
        or result['lineage']['trials']!=json_builtin(TRIALS) or result['lineage']['omegas']!=list(OMEGAS)):
        raise AssertionError('Completed horizon source/census/status binding')
    expected_status='COUPLED_HORIZON_ARITHMETIC_PASS' if result['all_numerical_gates_passed'] else 'COUPLED_HORIZON_ARITHMETIC_FAILED'
    if result['status']!=expected_status:raise AssertionError('Preserved horizon arithmetic disposition')
    for path,h in receipt['input_sha256'].items():seal(path,h)
    for path,h in receipt['output_sha256'].items():seal(path,h)
    mp=BASE/(stem+'_MANIFEST.json');jp=BASE/(stem+'_JOURNAL.jsonl')
    seal(mp,receipt['manifest_sha256']);seal(jp,receipt['journal_sha256'])
    if json.loads(mp.read_text())!=result['lineage']:raise AssertionError('Parent exact source manifest')
    events=[json.loads(line) for line in jp.read_text().splitlines()];epoch=None;seen=[]
    for index,event in enumerate(events):
        if event.get('owner')!='root' or type(event.get('pid')) is not int or event['pid']<=0 or event.get('source_sha256')!=receipt['source_sha256'] or event.get('manifest_sha256')!=receipt['manifest_sha256']:
            raise AssertionError('Parent root/source/manifest journal')
        if event['event'] in ('OWNER_START','OWNER_RESUME'):epoch=event['pid']
        elif event['event']=='CHECKPOINT':
            if event['pid']!=epoch:raise AssertionError('Parent checkpoint owner epoch')
            label,n=event['trial'],event['nstep'];seen.append((label,n));pn=stem+'_'+label+'_CP_'+str(n).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
            seal(BASE/pn,event['payload_sha256']);seal(BASE/cn,event['commit_sha256']);commit=json.loads((BASE/cn).read_text())
            if commit!=dict(lineage=result['lineage'],trial=label,nstep=n,payload=pn,sha256=event['payload_sha256']):raise AssertionError('Parent exact committed checkpoint')
        elif event['event']=='OWNER_COMPLETE':
            if index!=len(events)-1 or event['pid']!=epoch or event['status']!=result['status'] or event['result_sha256']!=PINS[stem+'_RESULT.json'] or event['gate_count']!=670 or event['checkpoint_count']!=83:raise AssertionError('Parent exact natural closure')
        else:raise AssertionError('Parent journal event refusal')
    expected=[(r[0],i) for r in TRIALS for i in sorted(set(list(range(0,r[1]+1,128))+[r[1]]))]
    if not events or events[0]['event']!='OWNER_START' or events[-1]['event']!='OWNER_COMPLETE' or seen!=expected:raise AssertionError('Complete83 parent checkpoint census')
    control='CONSTRAINED_U_ACTUAL_OPACITY_KERNEL_CONTROLS_V001'
    cr=json.loads((BASE/(control+'_RESULT.json')).read_text());cp=json.loads((BASE/(control+'_RECEIPT.json')).read_text())
    if (cr['status']!=cp['status'] or cr['status']!='ACTUAL_OPACITY_KERNEL_ARITHMETIC_PASS' or not cr['all_numerical_gates_passed']
        or len(cr['numerical_gates'])!=1275 or not all(g['passed'] for g in cr['numerical_gates']) or cp['checkpoint_count']!=4
        or cp['source_sha256']!=PINS['constrained_u_actual_opacity_kernel_controls_v001.py'] or cp['result_sha256']!=PINS[control+'_RESULT.json']
        or cr['manifest']['fixed']!=old_manifest['fixed'] or cr['manifest']['orders']!=[16,32] or cr['manifest']['cap']!=48.):
        raise AssertionError('Actually accepted actual-opacity control/physical ledger')
    for path,h in cp['input_sha256'].items():seal(path,h)
    for path,h in cp['output_sha256'].items():seal(path,h)
    seal(BASE/(control+'_MANIFEST.json'),cp['manifest_sha256']);seal(BASE/(control+'_JOURNAL.jsonl'),cp['journal_sha256'])
    cm=json.loads((BASE/(control+'_MANIFEST.json')).read_text())
    ce=[json.loads(line) for line in (BASE/(control+'_JOURNAL.jsonl')).read_text().splitlines()]
    if cm!=cr['manifest'] or cm['source_sha256']!=cp['source_sha256'] or [e['event'] for e in ce]!=['OWNER_START']+['CHECKPOINT']*4+['OWNER_COMPLETE']:
        raise AssertionError('Control exact manifest/four-stage natural closure')
    if any(e.get('owner')!='root' or type(e.get('pid')) is not int or e['pid']<=0 or e['pid']!=ce[0]['pid'] or e.get('source_sha256')!=cp['source_sha256'] or e.get('manifest_sha256')!=cp['manifest_sha256'] for e in ce):
        raise AssertionError('Control exact root/source/manifest/PID identity')
    for stage,event in zip(('SCALAR','PHYSICAL','RADIATION','CONSTANT'),ce[1:5]):
        pn=control+'_'+stage+'_CP.json';cn=pn[:-5]+'_COMMIT.json'
        if event['stage']!=stage or event['payload']!=pn:raise AssertionError('Control stage census')
        seal(BASE/pn,event['sha256']);seal(BASE/cn,event['commit_sha256'])
        if json.loads((BASE/cn).read_text())!=dict(manifest=cm,stage=stage,payload=pn,sha256=event['sha256']):raise AssertionError('Control exact stage commit')
    if ce[-1]['status']!=cr['status'] or ce[-1]['result_sha256']!=PINS[control+'_RESULT.json'] or (ce[-1]['gates'],ce[-1]['passed'])!=(1275,1275):
        raise AssertionError('Control exact final census/result')
    return dict(status=result['status'],numerical_gates=result['numerical_gates'],gas_fixture_flags=result['gas_fixture_flags'],
        source_sha256=receipt['source_sha256'],result_sha256=receipt['result_sha256'],scope='Immutable failed or passed attempt context; no state used for initialization or forcing')


def finite_tree(value):
    if isinstance(value,dict):
        if any(type(k) is not str for k in value):raise AssertionError('Canonical dictionary keys')
        for v in value.values():finite_tree(v)
    elif isinstance(value,list):
        for v in value:finite_tree(v)
    elif type(value) is float:
        if not math.isfinite(value):raise AssertionError('Nonfinite full checkpoint tree')
    elif value is not None and type(value) not in (str,int,bool):raise AssertionError('Noncanonical checkpoint type')


def validate_checkpoint(cp,commit,lineage,label,nstep,n,ns,stride):
    finite_tree(cp)
    if not cp['snapshots'] or cp['snapshots'][-1]['nstep']!=nstep or [c['state'] for c in cp['snapshots'][-1]['cases']]!=cp['states']:raise AssertionError('Checkpoint/final snapshot exact closure')
    required={'lineage','trial','nstep','step_count','ns','stride','states','anchors','snapshots','errors','seed_metadata','initial_moments','los_diagnostics','optical_controls'}
    if set(cp)!=required or cp['lineage']!=lineage or (cp['trial'],cp['nstep'],cp['step_count'],cp['ns'],cp['stride'])!=(label,nstep,n,ns,stride):raise AssertionError('Full checkpoint metadata')
    lay_n=9+3+5+3+2*ns
    if len(cp['states'])!=4 or any(len(y)!=lay_n or any(type(v) not in (float,int) or not math.isfinite(v) for v in y) for y in cp['states']):raise AssertionError('Full finite state axes')
    if len(cp['anchors'])!=4 or any(not isinstance(rows,list) for rows in cp['anchors']):raise AssertionError('Radiation history axes')
    if any(type(cp[key]) is not int for key in ['nstep','step_count','ns','stride']):raise AssertionError('Integer checkpoint census')
    if len(cp['errors'])!=4 or len(cp['seed_metadata'])!=4 or len(cp['initial_moments'])!=4:raise AssertionError('Full four-arm auxiliary census')
    control_names={'inverse_depth_error','optical_integral_error','conformal_integral_error','optical_mass_error','measure_identity_error','source_quadrature_error'}
    los_names={'delta_gamma','Hstar_u_gamma','delta_nu','Hstar_u_nu','F_gamma_2','F_nu_2','G_gamma_0','G_gamma_2'}
    if set(cp['optical_controls'])!=control_names or any(type(v) not in (int,float) or v<0 for v in cp['optical_controls'].values()):raise AssertionError('Complete finite optical-control prefix')
    if len(cp['los_diagnostics'])!=4 or any(set(row)!=los_names for row in cp['los_diagnostics']):raise AssertionError('Complete eight-row LOS diagnostic prefix')
    for row in cp['los_diagnostics']:
        for value in row.values():
            if set(value)!= {'maximum','location'} or type(value['maximum']) not in (int,float) or value['maximum']<0:raise AssertionError('LOS maximum schema')
            loc=value['location']
            if loc is not None and (set(loc)!= {'nstep','a','residual','scale','old_state','new_state','old_rate','new_rate','log_step'} or type(loc['nstep']) is not int or not 1<=loc['nstep']<=nstep or loc['a']<=0 or loc['scale']<0 or loc['log_step']<=0):raise AssertionError('LOS maximum/location exact prefix')
    prefix=128 if label=='START' else 0;common=n-prefix
    expected_snapshots=[0]+[i for i in range(1,nstep+1) if i>=prefix and (i-prefix)%(common//32)==0]
    if [s['nstep'] for s in cp['snapshots']]!=expected_snapshots or any(len(s['cases'])!=4 for s in cp['snapshots']):raise AssertionError('Exact full-state snapshot prefix')
    for rows in cp['anchors']:
        for row in rows:
            if set(row)!= {'x','eta','gamma_eta','phi','psi','F0','dipole','Pi'} or any(not math.isfinite(v) for v in row.values()):raise AssertionError('Full source-history schema')
        if any(rows[i]['eta']>=rows[i+1]['eta'] for i in range(len(rows)-1)):raise AssertionError('Ordered radiation memory')
        if len(rows)!=1+nstep//stride:raise AssertionError('Complete source-panel memory census')
    if commit!={'lineage':lineage,'trial':label,'nstep':nstep,'payload':STEM+'_'+label+'_CP_'+str(nstep).zfill(6)+'.json','sha256':sha(BASE/(STEM+'_'+label+'_CP_'+str(nstep).zfill(6)+'.json'))}:raise AssertionError('Exact commit byte identity')


def run_trial(spec,fixed,helpers,lineage):
    label,n,ns,stride,ai=spec;lay=helpers['Layout'](ns,4,4);therm=helpers['Thermal']('HALF',1,fixed)
    optical=load_optical_kernel()(fixed,therm,K)
    nodes,weight=gauss(ns);snodes=(nodes+1)/2;weights=weight*snodes;weights/=sum(weights)
    prefix=128 if label=='START' else 0;common_n=n-prefix
    common=np.linspace(math.log(AI),math.log(AF),common_n+1)
    xs=np.r_[np.linspace(math.log(ai),math.log(AI),prefix+1)[:-1],common] if prefix else common
    grid=conformal_grid(xs,fixed,helpers,8);grid2=conformal_grid(xs,fixed,helpers,16)
    eta_error=float(np.max(abs(grid-grid2))/max(float(grid2[-1]),1e-30))
    initial=[];seed=[];starts=[];moments=[]
    for om in OMEGAS:
        y,e0,meta=regular_seed(ai,fixed,lay,therm,snodes,weights,om,helpers);initial.append(y);starts.append(e0);seed.append(meta)
        moments.append(initial_multipoles(y,lay,K*CP/(1000*fixed['Hunit']*ai)))
    if max(starts)!=min(starts):raise AssertionError('Shared conformal origin')
    eta=grid2+starts[0]
    late_h=helpers['background'](math.log(AF),fixed)['h'];late_compton=compton_rate(AF,fixed,therm)
    background_lag_bound=late_h/(late_h+late_compton)
    if not (0<=background_lag_bound<1):raise AssertionError('Positive Compton background barrier')
    transported=[];transport_errors=[]
    for mm in moments:
        transported.append({kind:np.array([initial_transport(coeff,kval,l).real for l in range(5)]) for kind,coeff in mm.items() for kval in [K*grid2]})
        transport_errors.append({kind:float(np.max(abs(transported[-1][kind]-np.array([initial_transport(coeff,K*grid2,l,256).real for l in range(5)])))/CURVATURE) for kind,coeff in mm.items()})
    states=initial;anchors=[[anchor(xs[0],eta[0],y,fixed,lay,therm,snodes,weights,om,helpers)] for y,om in zip(states,OMEGAS)]
    snapshots=[];errors=[dict(stage_error=0.,dense_error=0.,momentum_error=0.,discrete_trace_error=0.,los_continuity_error=0.,kernel_tail_bound=0.,discarded_source_bound=0.,gas_temperature_difference_bound=0.,collision_kernel_tail_bound=0.) for _ in OMEGAS]
    los_diagnostics=[{name:dict(maximum=0.,location=None) for name in ('delta_gamma','Hstar_u_gamma','delta_nu','Hstar_u_nu','F_gamma_2','F_nu_2','G_gamma_0','G_gamma_2')} for _ in OMEGAS]
    paths=sorted(BASE.glob(STEM+'_'+label+'_CP_*_COMMIT.json'));start=0
    # Validate every committed prefix; payload-only or out-of-order commit is refused.
    expected_steps=list(range(0,n+1,128));expected_steps=sorted(set(expected_steps+[n]))
    if paths:
        seen=[];previous_cp=None
        for cn in paths:
            commit=json.loads(cn.read_text());pn=BASE/commit['payload'];cp=json.loads(pn.read_text());i=cp['nstep']
            validate_checkpoint(cp,commit,lineage,label,i,n,ns,stride)
            if previous_cp is not None:
                if cp['snapshots'][:len(previous_cp['snapshots'])]!=previous_cp['snapshots'] or any(cp['anchors'][a][:len(previous_cp['anchors'][a])]!=previous_cp['anchors'][a] for a in range(4)):raise AssertionError('Exact immutable snapshot/source-memory prefix')
                if any(cp['errors'][a][key]<previous_cp['errors'][a][key] for a in range(4) for key in previous_cp['errors'][a]) or any(cp['optical_controls'][key]<previous_cp['optical_controls'][key] for key in previous_cp['optical_controls']) or any(cp['los_diagnostics'][a][key]['maximum']<previous_cp['los_diagnostics'][a][key]['maximum'] for a in range(4) for key in previous_cp['los_diagnostics'][a]):raise AssertionError('Nondecreasing complete diagnostic prefix')
            previous_cp=cp
            CREATED[str(pn.resolve())]=commit['sha256'];CREATED[str(cn.resolve())]=sha(cn);seen.append(i)
        if seen!=expected_steps[:len(seen)]:raise AssertionError('Contiguous immutable checkpoint prefix')
        latest=json.loads((BASE/(STEM+'_'+label+'_CP_'+str(seen[-1]).zfill(6)+'.json')).read_text())
        if latest['seed_metadata']!=json_builtin(seed) or latest['initial_moments']!=json_builtin(moments):raise AssertionError('Same regular incoming state recovery')
        states=[np.array(v) for v in latest['states']];anchors=latest['anchors'];snapshots=latest['snapshots'];errors=latest['errors'];los_diagnostics=latest['los_diagnostics'];optical.maximum=latest['optical_controls'];start=seen[-1]
    payloads=sorted(BASE.glob(STEM+'_'+label+'_CP_*.json'));payloads=[p for p in payloads if not p.name.endswith('_COMMIT.json')]
    if len(payloads)!=len(paths):raise AssertionError('Orphan checkpoint payload')
    rates=[]
    for arm,(y,om) in enumerate(zip(states,OMEGAS)):
        dy,f=helpers['rates'](float(xs[start]),y,fixed,lay,therm,snodes,weights,om);rates.append(dy/f['h'])
        gc=compton_rate(f['bg']['a'],fixed,therm)
        gas_forcing=abs(2*dy[1]/3-dy[3]/4)/gc+background_lag_bound/(1-background_lag_bound)*(abs(y[3])+abs(f['phi']))
        errors[arm]['gas_temperature_difference_bound']=max(errors[arm]['gas_temperature_difference_bound'],float(gas_forcing))
    def checkpoint(i):
        recheck();pn=STEM+'_'+label+'_CP_'+str(i).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
        cp=dict(lineage=lineage,trial=label,nstep=i,step_count=n,ns=ns,stride=stride,states=states,anchors=anchors,snapshots=snapshots,errors=errors,seed_metadata=seed,initial_moments=moments,los_diagnostics=los_diagnostics,optical_controls=optical.maximum)
        ph=write(pn,cp);ch=write(cn,dict(lineage=lineage,trial=label,nstep=i,payload=pn,sha256=ph));journal('CHECKPOINT',trial=label,nstep=i,payload_sha256=ph,commit_sha256=ch)
        print(label,i,'/',n,flush=True)
    if start==0 and not paths:
        cases=[helpers['snapshot'](float(xs[0]),y,fixed,lay,therm,snodes,weights,om) for y,om in zip(states,OMEGAS)]
        for arm,case in enumerate(cases):case['gas_source_bound']=extra_source_bound(case,fixed,therm,errors[arm]['gas_temperature_difference_bound'],background_lag_bound)
        snapshots.append(dict(nstep=0,cases=cases));checkpoint(0)
    for i in range(start+1,n+1):
        oldstates=states;oldrates=rates;states=[];rates=[]
        for arm,om in enumerate(OMEGAS):
            iv={kind:v[:,i] for kind,v in transported[arm].items()}
            y,err=coupled_endpoint(oldstates[arm],oldrates[arm],float(xs[i]),float(xs[i]-xs[i-1]),float(eta[i]),anchors[arm],fixed,lay,therm,snodes,weights,om,helpers,moments[arm],iv,optical,dense=(i%128==0))
            dy,f=helpers['rates'](float(xs[i]),y,fixed,lay,therm,snodes,weights,om);rr=dy/f['h'];states.append(y);rates.append(rr)
            gc=compton_rate(f['bg']['a'],fixed,therm)
            gas_forcing=abs(2*dy[1]/3-dy[3]/4)/gc+background_lag_bound/(1-background_lag_bound)*(abs(y[3])+abs(f['phi']))
            errors[arm]['gas_temperature_difference_bound']=max(errors[arm]['gas_temperature_difference_bound'],float(gas_forcing))
            prev=helpers['coefficients'](float(xs[i-1]),oldstates[arm],fixed,lay,therm,snodes,weights,om)
            def trace_force(ff,yy):
                dp=ff['c']*ff['w']*yy[7]+(ff['rg']*yy[3]+ff['rn']*yy[5])/3
                return 3*ff['h']*ff['mom']+ff['bg']['h_dt']*ff['phi']+ff['q']**2*(yy[0]-ff['phi'])/3-dp
            left_trace=trace_force(prev,oldstates[arm])/prev['h'];right_trace=trace_force(f,y)/f['h']
            trace_res=f['mom']-prev['mom']+(xs[i]-xs[i-1])*(left_trace+right_trace)/2
            trace_scale=abs(f['mom'])+abs(prev['mom'])+abs(xs[i]-xs[i-1])*(abs(left_trace)+abs(right_trace))/2
            err['discrete_trace_error']=float(abs(trace_res)/max(trace_scale,CURVATURE*1e-18))
            # Low moments only: every F3/G3 comes from SAME radiation memory;
            # no truncation at an independently selected angular top moment.
            rows=[3,4,5,6,lay.fg[2],lay.fn[2],lay.pol[0],lay.pol[2]]
            residual=y[rows]-oldstates[arm][rows]-(xs[i]-xs[i-1])*(rr[rows]+oldrates[arm][rows])/2
            scale=np.abs(y[rows])+np.abs(oldstates[arm][rows])+abs(xs[i]-xs[i-1])*(abs(rr[rows])+abs(oldrates[arm][rows]))/2
            row_errors=abs(residual)/np.maximum(scale,CURVATURE*1e-12)
            err['los_continuity_error']=float(np.max(row_errors))
            for j,name in enumerate(los_diagnostics[arm]):
                if row_errors[j]>los_diagnostics[arm][name]['maximum']:
                    los_diagnostics[arm][name]=dict(maximum=float(row_errors[j]),location=dict(nstep=i,a=math.exp(float(xs[i])),
                        residual=float(residual[j]),scale=float(scale[j]),old_state=float(oldstates[arm][rows[j]]),new_state=float(y[rows[j]]),
                        old_rate=float(oldrates[arm][rows[j]]),new_rate=float(rr[rows[j]]),log_step=float(xs[i]-xs[i-1])))
            for key,value in err.items():
                if key in errors[arm]:errors[arm][key]=max(errors[arm][key],value)
            if i%stride==0:anchors[arm].append(anchor(xs[i],eta[i],y,fixed,lay,therm,snodes,weights,om,helpers))
        if i>=prefix and (i-prefix)%(common_n//32)==0:
            cases=[helpers['snapshot'](float(xs[i]),y,fixed,lay,therm,snodes,weights,om) for y,om in zip(states,OMEGAS)]
            for arm,case in enumerate(cases):case['gas_source_bound']=extra_source_bound(case,fixed,therm,errors[arm]['gas_temperature_difference_bound'],background_lag_bound)
            snapshots.append(dict(nstep=i,cases=cases))
        if i%128==0 or i==n:checkpoint(i)
    return dict(label=label,n=n,ns=ns,stride=stride,ai=ai,af=AF,k=K,omega=list(OMEGAS),layout_names=lay.names(),seed=seed,common_snapshot_count=33,
        eta_quadrature_error=eta_error,endpoint_phase=K*float(grid2[-1]),initial_transport_errors=transport_errors,snapshots=snapshots,errors=errors,los_diagnostics=los_diagnostics,optical_controls=dict(optical.maximum),
        gas_scope='Cold-baryon ideal fixture; saved instantaneous omitted gas source and lag barrier, not full warm-state propagation')


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


def main():
    global SOURCE_SHA,MANIFEST_SHA
    terminal=[BASE/(STEM+suffix) for suffix in ('_RESULT.json','_REPORT.md','_RECEIPT.json')]
    if any(p.exists() for p in terminal):raise FileExistsError('No completed output overwrite')
    if list(BASE.glob(STEM+'_FAILED*')):raise FileExistsError('Preserved failure requires a NEW attempt')
    manifest_path=BASE/(STEM+'_MANIFEST.json');journal_path=BASE/(STEM+'_JOURNAL.jsonl')
    if not manifest_path.exists() and (journal_path.exists() or list(BASE.glob(STEM+'_*_CP_*.json'))):raise AssertionError('Pre-manifest orphan refusal')
    SOURCE_SHA=sha(__file__);fixed,inherited=authenticate();helpers=load_declared_helpers();tick=time.monotonic()
    lineage=dict(source_sha256=SOURCE_SHA,inputs=dict(SEALS),fixed=fixed,trials=TRIALS,omegas=OMEGAS,numpy_version=np.__version__,
        numerical_method=dict(optical_kernel_sha256=OPTICAL_KERNEL_SHA,quadrature_order=16,independent_order=32,optical_cutoff=48.,inverse_iterations=16,
            source_interpolant='Affine actual conformal coordinate',core_gate_count=670,separate_optical_control_count=36))
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
    text='# Coupled horizon radiation-memory actual-opacity test V001\n\n'+result['status']+'\n\n'+str(sum(g['passed'] for g in gates))+'/'+str(len(gates))+' original numerical controls PASS; '+str(sum(g['passed'] for g in optical_controls))+'/36 additional actual-opacity controls PASS.\n\nFirst horizon window k=10/Mpc; all four inertias, true initial angular transport, physical implicit metric/native sources. Actual optical depth replaces panel-mean opacity; all prior failures remain. Gas source flags are instantaneous bounds. The earlier k=.01 attempt retains375PASS/152FAIL.\n'
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


def refuse_closed_prefix():
    if any((BASE/(STEM+s)).exists() for s in ['_RESULT.json','_REPORT.md','_RECEIPT.json']) or list(BASE.glob(STEM+'_FAILED*')):raise FileExistsError('Protected closed attempt; no error artifact mutation')


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
