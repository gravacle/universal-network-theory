"""Inert draft: conservative moving-volume finite-R currents; root sole runner.

No import/run by authors. Each run-case is separate, stdout only. No viscosity,
fluid reset, density clipping, EOS interpolation or producer-module import.
"""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_k]='1'
import hashlib
import base64
import json
import math
from pathlib import Path
import resource
import sys
import time
import traceback
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path('/Users/bgm/Documents/ChatGPT/Universal Network Theory')
J=ROOT/'UNT_DARK_SECTOR_CONTINUOUS_2026-09-27_V001/joint_parent_continuation'
FREEZE=J/'SPHERICAL_TWO_CURRENT_V001_FROZEN.json'
CONFIG=dict(gaps=[128,8192],interfaces=[8.,16.],widths=[1/16,1/32,1/64],
    times=[0.,1/64,1/32,1/16],watch_radius=4.,beta=.005,
    velocity_cap=2.,action_ratio_limits=[.25,4.],volume_ratio_limits=[.25,4.],
    primary_order=64,check_order=128,root_iterations=8,root_tolerance=2e-11,
    cfl=.15,max_step=1/1024,dp_rtol=2e-11,dp_atol=2e-13,
    arithmetic_tolerance=2e-11,material_tolerance=2e-10,state_tolerance=2e-8,
    readout_tolerance=2e-7,gradient_tolerance=2e-6,gradient_steps=[1e-4,5e-5],
    spatial_accuracy_gate=None,physical_success_gate=None,
    G_SI=6.67430e-11,c=299792458.,parsec_m=3.085677581491367e16,ell_kpc=3.2)
PINS={
 'SPHERICAL_DUST_SHADOW_V001_RESULTS.json':'171fb246a4716f5b769c420cb6680a8c474cbc59f676bd10279d1e300a1b8c5d',
 'SPHERICAL_DUST_SHADOW_V001_FROZEN.json':'5b966f80569a25a5e3317e944af530671244cdf097bf29a0872069ce2cfc8868',
 'SPHERICAL_DUST_SHADOW_RESULT_AUDIT_V001.md':'1cee4c6c99fab59e234349db96b9de8632300f20ffc19076b0431ff8f5ef845b'}


def encode(x): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def inputs():
    if Path.cwd().resolve()!=ROOT or Path(__file__).resolve()!=J/'spherical_two_current_v001.py': raise RuntimeError('Wrong root/source')
    files={}
    def add(p,h=None):
        for parent in (p,*p.parents):
            if parent==ROOT.parent:break
            if parent.is_symlink():raise RuntimeError('Symlink input '+str(parent))
        p=p.resolve(strict=True);p.relative_to(ROOT);got=digest(p)
        if h and got!=h: raise RuntimeError('Changed input '+str(p))
        files[str(p.relative_to(ROOT))]=got
    for name,h in PINS.items(): add(J/name,h)
    fr=json.loads((J/'SPHERICAL_DUST_SHADOW_V001_FROZEN.json').read_bytes())
    for p,h in fr['files'].items(): add(ROOT/p,h)
    w=json.loads((J/'SPHERICAL_DUST_SHADOW_V001_RESULTS.json').read_bytes())
    if w['freeze_sha256']!=PINS['SPHERICAL_DUST_SHADOW_V001_FROZEN.json'] or hashlib.sha256(encode(w['payload'])).hexdigest()!=w['payload_sha256']:
        raise RuntimeError('Shadow receipt binding')
    old=w['payload']
    if old['status']!='COMPLETE_DUST_SHADOW_ONLY' or old['failures']: raise RuntimeError('Unqualified reference')
    cert=json.loads((J/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json').read_bytes())['payload']
    for name in [Path(__file__).name,'SPHERICAL_TWO_CURRENT_FINITE_R_DESIGN_V001.md','SPHERICAL_TWO_CURRENT_PROTOCOL_V001.md']:
        add(J/name)
    cases=[dict(case_index=i,gap=R,L=L,dx=dx,cells=round(L/dx)) for i,(R,L,dx) in
           enumerate((R,L,dx) for R in CONFIG['gaps'] for L in CONFIG['interfaces'] for dx in CONFIG['widths'])]
    return old,cert,dict(configuration=CONFIG,files=files,cases=cases)


class Stop(Exception):
    def __init__(self,t,y,why): self.t=float(t);self.y=np.asarray(y).copy();self.why=why


class Checks:
    def __init__(self): self.counts={};self.maxima={};self.failures=[]
    def test(self,name,a,b=0.,tol=None,scale=None):
        a=np.asarray(a);b=np.asarray(b)
        if scale is None: scale=np.maximum(1.,np.maximum(abs(a),abs(b)))
        e=abs(a-b)/np.maximum(abs(scale),1e-300);finite=np.isfinite(e)
        mx=float(np.max(e[finite])) if np.any(finite) else 0.
        self.counts[name]=self.counts.get(name,0)+int(e.size);self.maxima[name]=max(self.maxima.get(name,0.),mx)
        tol=CONFIG['arithmetic_tolerance'] if tol is None else tol
        if not np.all(finite) or mx>tol: self.failures.append(dict(check=name,error=mx if np.all(finite) else None,
                nonfinite_entries=int(np.count_nonzero(~finite)),tolerance=tol))


class EOS:
    def __init__(self,R,order):
        self.R=R;x,w=np.polynomial.legendre.leggauss(order);th=(x+1)*math.pi/4
        self.weights=w*math.pi/4;self.s2=np.sin(th)**2;self.c2=np.cos(th)**2
        self.max_action_error=0.
    def at(self,I):
        I=np.asarray(I,dtype=float);target=I/self.R**3
        if np.any(target<=0) or not np.all(np.isfinite(target)): raise ValueError('Nonpositive action')
        hi=2*target;lo=hi/np.sqrt(1+hi);r=hi.copy()
        # Exact action derivative di/dr=(1+r)/(2 Omega). Safeguarded Newton;
        # no unbounded iteration or silently accepted unresolved root.
        for _ in range(CONFIG['root_iterations']):
            q=1+r[...,None]*(1+self.s2)/2;sq=np.sqrt(q)
            bar=(2/math.pi)*np.sum(self.weights*self.c2*sq,axis=-1)
            integral=np.sum(self.weights/sq,axis=-1);om=math.pi/(2*integral)
            val=r*bar-target;lo=np.where(val<0,r,lo);hi=np.where(val>=0,r,hi)
            nr=r-val*(2*om)/(1+r)
            r=np.where((nr>=lo)&(nr<=hi),nr,(lo+hi)/2)
        angular_excess=r[...,None]*(1+self.s2)/2;q=1+angular_excess;sq=np.sqrt(q)
        bar=(2/math.pi)*np.sum(self.weights*self.c2*sq,axis=-1)
        err=float(np.max(abs(r*bar/target-1)));self.max_action_error=max(self.max_action_error,err)
        if err>CONFIG['root_tolerance']: raise ValueError('Action inversion not qualified')
        integral=np.sum(self.weights/sq,axis=-1);om=math.pi/(2*integral)
        dw=np.sum(self.weights*angular_excess/(sq*(sq+1)),axis=-1)/integral
        e=self.R**4*r*(2+r)/4
        w=r/(2+r)*np.sum(self.weights*self.s2**2/sq,axis=-1)/integral;p=w*e
        ell=np.sum(self.weights*(1+self.s2)/(q*sq),axis=-1)
        ci=r*bar*om*ell/(2*integral*(1+r))
        return dict(I=I,r=r,e=e,p=p,omega=self.R*om,cI2=ci,dW=dw,
                    dE=dw-p/(self.R*I),cN_c2=om*ci,action_recovered=self.R**3*r*bar)


def seed_mass(x):
    z=np.minimum(x,1.);m=3465/128*(z**3/3-4*z**5/5+6*z**7/7-4*z**9/9+z**11/11)
    return np.where(x<1,m,1.)


def gravity(meshes,masses,qbar):
    """Exact piecewise-constant self/background energy and its face derivative."""
    # Wider accumulators reduce cancellation of the common exterior potential
    # in tiny cosmic-current forces. Output precision remains ordinary float.
    meshes=[np.asarray(x,dtype=np.longdouble) for x in meshes]
    masses=[np.asarray(m,dtype=np.longdouble) for m in masses]
    qbar=np.longdouble(qbar)
    faces=np.unique(np.concatenate(meshes));a,b=faces[:-1],faces[1:];mid=(a+b)/2
    vols=[4*math.pi*np.diff(x**3)/3 for x in meshes];dens=[m/v for m,v in zip(masses,vols)]
    q=np.zeros(len(mid),dtype=np.longdouble)
    for x,rho in zip(meshes,dens):
        idx=np.minimum(np.searchsorted(x,mid,side='right')-1,len(rho)-1)
        q+=np.where(mid<x[-1],rho[idx],0.)
    increments=4*math.pi*q*(b**3-a**3)/3
    enclosed=np.r_[0.,np.cumsum(increments)]
    exterior=np.r_[np.cumsum((2*math.pi*q*(b*b-a*a))[::-1])[::-1],0.]
    B=enclosed[:-1]-4*math.pi*q*a**3/3
    K=-exterior[1:]-2*math.pi*q*b*b;D=2*math.pi*(q-qbar)/3
    phi=np.r_[K[0],K-B/b+D*b*b]
    integ=K*(b**3-a**3)/3-B*(b*b-a*a)/2+D*(b**5-a**5)/5
    prefix=np.r_[0.,np.cumsum(integ)]
    gradients=[];averages=[];background_averages=[]
    for x,m,v,rho in zip(meshes,masses,vols,dens):
        ix=np.searchsorted(faces,x);av=4*math.pi*np.diff(prefix[ix])/v;ph=phi[ix]
        bg=-(2*math.pi*qbar/3)*(4*math.pi/5)*np.diff(x**5)/v
        left=rho*(ph[1:]-av);right=np.r_[rho[1:]*(av[1:]-ph[1:-1]),0.]
        gradients.append(4*math.pi*x[1:]**2*(left+right));averages.append(av);background_averages.append(bg)
    W0=np.longdouble(.5)*sum(np.dot(m,av+bg) for m,av,bg in zip(masses,averages,background_averages))
    return [np.asarray(g,dtype=float) for g in gradients],W0,float(np.max(phi)-np.min(phi)),[np.asarray(a,dtype=float) for a in averages]


class Model:
    def __init__(self,case,old,cert,order=64,pressure=True):
        self.case=case;self.N=case['cells'];self.R=case['gap'];self.pressure=pressure
        self.old=next(c for c in old['cases'] if c['gap']==self.R);self.ref=self.old['background_reference'];self.s=self.old['source_state']
        self.Kb=next(c['Kb'] for c in cert['cases'] if c['gap']==self.R)
        self.ell=self.old['ell_m'];self.td=self.old['t_dyn_s'];self.eps=self.old['epsilon'];self.M=self.old['seed_mass_kg']
        self.rho_unit=self.M/self.ell**3;self.v2=self.s['gstar']*self.ell
        self.S=self.s['gstar']**2/(4*math.pi*CONFIG['G_SI']*self.Kb)
        self.qh=self.old['rho0_H1_kg_m3']/self.rho_unit
        self.qb=3*self.ref['H0_s_inverse']**2*self.ref['Omega_b']/(8*math.pi*CONFIG['G_SI']*self.rho_unit)
        self.qbar=self.qh+self.qb;self.x0=np.linspace(0,case['L'],self.N+1)
        self.V0=4*math.pi*np.diff(self.x0**3)/3
        self.masses=[np.diff(seed_mass(self.x0))+self.qb*self.V0,self.qh*self.V0]
        self.face_masses=[np.r_[(m[:-1]+m[1:])/2,m[-1]/2] for m in self.masses]
        self.eos=EOS(self.R,order);self.I1=self.s['I'];self.e1=self.s['E']/CONFIG['beta']
        self.speed_cap=CONFIG['velocity_cap']+math.sqrt(4*self.I1/(self.R**3*self.eps))
        self.step=min(CONFIG['max_step'],CONFIG['cfl']*case['dx']/self.speed_cap)
        T=CONFIG['times'][-1]
        if self.speed_cap*T>=case['L']-2*T-CONFIG['watch_radius']: raise ValueError('Prior exterior domain bound failed')
        self.nstate=1+4*self.N+10;self.last=None;self.maxima={};self.minimum_volume_ratio=1.
        self.error_units=np.ones(self.nstate)
        self.error_units[1+self.N:1+2*self.N]=1/self.face_masses[0]
        self.error_units[1+3*self.N:1+4*self.N]=1/self.face_masses[1]
        self.error_units[1+4*self.N+7:]=1/float(np.sum(self.masses[1]))
    def initial(self):
        y=np.zeros(self.nstate);y[0]=1.;y[1:1+self.N]=self.x0[1:];y[1+2*self.N:1+3*self.N]=self.x0[1:];return y
    def read(self,t,y,guard=True):
        if len(y)!=self.nstate or not np.all(np.isfinite(y)): raise Stop(t,y,'NONFINITE_STATE')
        A=y[0];n=self.N;xb=np.r_[0.,y[1:1+n]];pb=y[1+n:1+2*n];xh=np.r_[0.,y[1+2*n:1+3*n]];ph=y[1+3*n:1+4*n]
        meshes=[xb,xh];ps=[pb,ph];vols=[4*math.pi*np.diff(x**3)/3 for x in meshes]
        if A<1-2e-14 or any(np.any(v<=0) for v in vols): raise Stop(t,y,'NONPOSITIVE_ORDERED_VOLUME_OR_BACKGROUND')
        velocities=[p/(A*w) for p,w in zip(ps,self.face_masses)];ratios=[v/self.V0 for v in vols]
        qs=[m/v for m,v in zip(self.masses,vols)];action_ratio=qs[1]/self.qh
        if guard and (max(float(np.max(abs(v))) for v in velocities)>CONFIG['velocity_cap'] or
                      min(float(np.min(r)) for r in ratios)<.25 or max(float(np.max(r)) for r in ratios)>4 or
                      float(np.min(action_ratio))<.25 or float(np.max(action_ratio))>4):
            raise Stop(t,y,'PROSPECTIVE_VELOCITY_ACTION_OR_VOLUME_GUARD')
        mat=self.eos.at(np.r_[self.I1*action_ratio/A**3,self.I1/A**3]);bg={k:float(v[-1]) for k,v in mat.items()}
        hard={k:v[:-1] for k,v in mat.items()}
        Ht=self.ref['H0_s_inverse']*self.td*math.sqrt(self.ref['Omega_b']/A**3+self.ref['Omega_exc']*bg['e']/self.e1+self.ref['Omega_Lambda'])
        P=A**3*self.S*CONFIG['beta']*hard['p']/(self.rho_unit*self.v2)
        Pbar=A**3*self.S*CONFIG['beta']*bg['p']/(self.rho_unit*self.v2)
        grad,W0,span,phi=gravity(meshes,self.masses,self.qbar)
        Ts=[.5*float(np.dot(w,v*v)) for w,v in zip(self.face_masses,velocities)];T=sum(Ts)
        U=float(np.dot(self.masses[1],hard['dE']))/self.eps
        Ubar=float(np.sum(self.masses[1]))*bg['dE']/self.eps
        return dict(A=A,meshes=meshes,ps=ps,volumes=vols,q=qs,velocities=velocities,
                    hard=hard,background_material=bg,Ht=Ht,P=P,Pbar=Pbar,gradW0=grad,
                    K=T,K_species=Ts,U=U,Ubar=Ubar,W=float(W0/A),potential_span_over_c2=span/A*self.eps,
                    action_ratio=action_ratio,volume_ratios=ratios)
    def rhs(self,t,y):
        self.last=(float(t),y.copy());o=self.read(t,y);A=o['A'];n=self.N
        vx=[v/A for v in o['velocities']];kicks=[-g/A for g in o['gradW0']]
        pressure=4*math.pi*o['meshes'][1][1:]**2*(o['P']-np.r_[o['P'][1:],o['Pbar']])
        if self.pressure:kicks[1]=kicks[1]+pressure
        out=np.zeros_like(y);out[0]=A*o['Ht'];out[1:1+n]=vx[0];out[1+n:1+2*n]=kicks[0]
        out[1+2*n:1+3*n]=vx[1];out[1+3*n:1+4*n]=kicks[1]
        gravity_work=-sum(float(np.dot(v,g)) for v,g in zip(vx,o['gradW0']))/A
        boundary=-4*math.pi*o['meshes'][1][-1]**2*o['Pbar']*vx[1][-1]
        hubble_KU=-o['Ht']*(2*o['K']+3*float(np.dot(o['P'],o['volumes'][1])))
        hubble_W=-o['Ht']*o['W']
        # Ledger slots: mechanical gravity, outer traction, H(K+U), HW,
        # total-action-energy predicted derivative, actual travel, pressure work;
        # then hard gravity, hard H(K+U), complete hard mechanical work.
        cs=math.sqrt(float(np.max(o['hard']['cN_c2']))/self.eps)
        travel=(max(float(np.max(abs(v))) for v in o['velocities'])+cs)/A
        hard_gravity=-float(np.dot(vx[1],o['gradW0'][1]))/A
        hard_hubble=-o['Ht']*(2*o['K_species'][1]+3*float(np.dot(o['P'],o['volumes'][1])))
        out[1+4*n:]=[gravity_work,boundary,hubble_KU,hubble_W,
                       boundary+hubble_KU+hubble_W,travel,float(np.dot(vx[1],pressure)),
                       hard_gravity,hard_hubble,hard_gravity+hard_hubble+boundary]
        for key,val in [('max_dE',np.max(o['hard']['dE'])),('max_dW',np.max(o['hard']['dW'])),
                        ('max_v2_c2',max(np.max(v*v) for v in o['velocities'])*self.eps),
                        ('max_potential_span_c2',o['potential_span_over_c2'])]:
            self.maxima[key]=max(self.maxima.get(key,0.),float(val))
        self.minimum_volume_ratio=min(self.minimum_volume_ratio,min(float(np.min(r)) for r in o['volume_ratios']))
        return out


def rk4(model,step):
    y=model.initial();t=0.;samples=[y.copy()];evaluations=0
    for target in CONFIG['times'][1:]:
        count=math.ceil((target-t)/step);h=(target-t)/count
        for _ in range(count):
            k1=model.rhs(t,y);k2=model.rhs(t+h/2,y+h*k1/2);k3=model.rhs(t+h/2,y+h*k2/2);k4=model.rhs(t+h,y+h*k3)
            y=y+h*(k1+2*k2+2*k3+k4)/6;t+=h;model.read(t,y);evaluations+=4
        t=target;samples.append(y.copy())
    return samples,dict(rhs_evaluations=evaluations,maximum_step=step)


def dopri(model):
    y=model.initial();t=0.;h=model.step;samples=[y.copy()];accepted=rejected=0
    aa=[[],[1/5],[3/40,9/40],[44/45,-56/15,32/9],[19372/6561,-25360/2187,64448/6561,-212/729],
        [9017/3168,-355/33,46732/5247,49/176,-5103/18656],[35/384,0,500/1113,125/192,-2187/6784,11/84]]
    cc=[0,1/5,3/10,4/5,8/9,1,1];b5=np.array([35/384,0,500/1113,125/192,-2187/6784,11/84,0])
    b4=np.array([5179/57600,0,7571/16695,393/640,-92097/339200,187/2100,1/40])
    for target in CONFIG['times'][1:]:
        while t<target:
            h=min(h,target-t,model.step)
            if t+h==t:raise Stop(t,y,'TIME_STEP_UNDERFLOW')
            ks=[]
            for i in range(7):
                yy=y.copy()
                for j,a in enumerate(aa[i]): yy+=h*a*ks[j]
                ks.append(model.rhs(t+cc[i]*h,yy))
            K=np.asarray(ks);yn=y+h*np.dot(b5,K);er=h*np.dot(b5-b4,K)
            units=model.error_units
            norm=float(np.max(abs(er)*units/(CONFIG['dp_atol']+CONFIG['dp_rtol']*np.maximum(abs(y),abs(yn))*units)))
            if not math.isfinite(norm):raise Stop(t,y,'NONFINITE_TIME_ERROR')
            if norm<=1:y=yn;t+=h;model.read(t,y);accepted+=1
            else:rejected+=1
            h*=min(5.,max(.2,.9*norm**-.2)) if norm else 5.
        samples.append(y.copy())
    return samples,dict(accepted=accepted,rejected=rejected)


def snapshot(model,t,y):
    o=model.read(t,y);A=o['A'];data={}
    for i,name in enumerate(['baryon','hard']):
        x=o['meshes'][i];mass=model.masses[i]
        data[name]=dict(faces=x.tolist(),peculiar_v_over_vdyn=o['velocities'][i].tolist(),
            cell_masses_over_M=mass.tolist(),comoving_density=o['q'][i].tolist(),
            volume_ratio=o['volume_ratios'][i].tolist(),enclosed_mass_over_M=np.r_[0.,np.cumsum(mass)].tolist(),
            gravity_acceleration_over_gstar=(-o['gradW0'][i]/(A*A*model.face_masses[i])).tolist())
        centers=(x[:-1]+x[1:])/2
        data[name]['log_density_radial_gradient']=(np.diff(np.log(o['q'][i]))/np.diff(centers)).tolist()
        data[name]['face_velocity_radial_gradient']=(np.diff(np.r_[0.,o['velocities'][i]])/np.diff(x)).tolist()
    pressure_kick=4*math.pi*o['meshes'][1][1:]**2*(o['P']-np.r_[o['P'][1:],o['Pbar']])
    return dict(tau=t,seconds=t*model.td,A=A,H_s_inverse=o['Ht']/model.td,species=data,
        hard_material={k:v.tolist() for k,v in o['hard'].items()},action_ratio=o['action_ratio'].tolist(),
        hard_gravity_omission_internal_over_rest=o['hard']['dE'].tolist(),
        hard_gravity_omission_active_over_rest=(o['hard']['dE']+3*o['hard']['p']/(model.R*o['hard']['I'])).tolist(),
        hard_pressure_dimensionless=o['P'].tolist(),background_pressure=o['Pbar'],
        hard_pressure_acceleration_over_gstar=(pressure_kick/(A*model.face_masses[1])).tolist(),
        K=o['K'],K_species=o['K_species'],U=o['U'],Ubar=o['Ubar'],U_excess=o['U']-o['Ubar'],W=o['W'],
        potential_span_over_c2=o['potential_span_over_c2'],ledger=y[1+4*model.N:].tolist())


def controls(model,ck):
    y=model.initial();o=model.read(0.,y);rho=model.qbar
    homogeneous_m=[model.qb*model.V0,model.qh*model.V0]
    g,W,span,av=gravity([model.x0,model.x0],homogeneous_m,rho)
    ck.test('homogeneous_gravity',np.concatenate(g),0.)
    ck.test('homogeneous_pressure',o['P']-o['Pbar'],0.)
    ck.test('compact_seed_mass',np.sum(model.masses[0]-model.qb*model.V0),1.)
    ck.test('rest_action_normalization',model.qh*model.rho_unit,
            model.S*CONFIG['beta']*model.R*model.I1/CONFIG['c']**2,
            scale=model.qh*model.rho_unit)
    # Symmetric energy-gradient differences, extrapolated without choosing a sign.
    direction=[.1*np.sin(math.pi*model.x0[1:]/model.case['L']),.07*np.sin(2*math.pi*model.x0[1:]/model.case['L'])]
    deriv=[]
    for h in CONFIG['gradient_steps']:
        wp=[]
        for sign in [-1,1]:
            meshes=[np.r_[0.,model.x0[1:]+sign*h*v] for v in direction]
            wp.append(gravity(meshes,model.masses,rho)[1])
        deriv.append((wp[1]-wp[0])/(2*h))
    analytical=sum(float(np.dot(g,v)) for g,v in zip(o['gradW0'],direction))
    ck.test('gravity_energy_gradient',(4*deriv[1]-deriv[0])/3,analytical,CONFIG['gradient_tolerance'])
    # Test each species separately per unit species mass, so the tiny cosmic
    # mass cannot make a wrong hard-force gradient pass an absolute test.
    for species in range(2):
        derivatives=[]
        for h in CONFIG['gradient_steps']:
            energies=[]
            for sign in [-1,1]:
                meshes=[model.x0.copy(),model.x0.copy()]
                meshes[species][1:]+=sign*h*direction[species]
                energies.append(gravity(meshes,model.masses,rho)[1])
            derivatives.append((energies[1]-energies[0])/(2*h))
        scale_mass=float(np.sum(model.masses[species]))
        ck.test('gravity_gradient_species_'+str(species),(4*derivatives[1]-derivatives[0])/(3*scale_mass),
                np.dot(o['gradW0'][species],direction[species])/scale_mass,CONFIG['gradient_tolerance'])
    # Nonuniform synthetic hard volumes ensure this pressure-gradient check is
    # not merely the telescoping uniform-pressure null. Outer displacement=0.
    yy=y.copy();n=model.N;direction_p=.1*np.sin(math.pi*model.x0[1:]/model.case['L'])
    yy[1+2*n:1+3*n]+=.02*model.case['dx']*np.sin(2*math.pi*model.x0[1:]/model.case['L'])
    oo=model.read(0.,yy);kick=4*math.pi*oo['meshes'][1][1:]**2*(oo['P']-np.r_[oo['P'][1:],oo['Pbar']])
    pd=[]
    for h in CONFIG['gradient_steps']:
        vals=[]
        for sign in [-1,1]:
            z=yy.copy();z[1+2*n:1+3*n]+=sign*h*direction_p
            vals.append(model.read(0.,z)['U'])
        pd.append((vals[1]-vals[0])/(2*h))
    mh=float(np.sum(model.masses[1]))
    ck.test('pressure_internal_energy_gradient',(4*pd[1]-pd[0])/(3*mh),
            -np.dot(kick,direction_p)/mh,CONFIG['gradient_tolerance'])
    for key,expected in [('e',model.e1),('p',model.s['pressure']/CONFIG['beta']),('omega',model.s['omega']),('cI2',model.s['cI2'])]:
        ck.test('saved_material_'+key,o['background_material'][key],expected,CONFIG['material_tolerance'],abs(expected))


def run_case(case,old,cert):
    start=time.perf_counter();ck=Checks();m=None;runs={};stats={};out=dict(case=case,status='STARTED')
    try:
        m=Model(case,old,cert)
        controls(m,ck)
        if ck.failures: raise RuntimeError('Prerequisite controls failed before trajectory')
        for name,method,factor in [('RK4_coarse',rk4,1.),('RK4_fine',rk4,.5),('DOPRI54',dopri,1.)]:
            if method is rk4: runs[name],stats[name]=method(m,m.step*factor)
            else:runs[name],stats[name]=method(m)
        fine=runs['RK4_fine'];samples=[snapshot(m,t,y) for t,y in zip(CONFIG['times'],fine)]
        checkmat=EOS(m.R,CONFIG['check_order'])
        initial=samples[0]
        for it,(t,y,snap) in enumerate(zip(CONFIG['times'],fine,samples)):
            for name in ['RK4_coarse','DOPRI54']:
                ck.test('time_state',np.asarray(runs[name][it])*m.error_units,y*m.error_units,CONFIG['state_tolerance'])
                other=m.read(t,runs[name][it]);own=m.read(t,y)
                for sp in range(2):
                    ck.test('time_velocity',other['velocities'][sp],own['velocities'][sp],CONFIG['readout_tolerance'])
                    ck.test('time_volume_ratio',other['volume_ratios'][sp],own['volume_ratios'][sp],CONFIG['readout_tolerance'])
                ck.test('time_action_ratio',other['action_ratio'],own['action_ratio'],CONFIG['readout_tolerance'])
            q=checkmat.at(np.asarray(snap['hard_material']['I']))
            for key in ['e','p','omega','cI2','dE','dW']:
                a=np.asarray(snap['hard_material'][key]);ck.test('material_'+key,a,q[key],CONFIG['material_tolerance'],np.maximum(abs(a),1e-300))
            hmat=snap['hard_material'];Is=np.asarray(hmat['I']);es=np.asarray(hmat['e']);ps=np.asarray(hmat['p']);ws=np.asarray(hmat['omega'])
            ck.test('virial_enthalpy',Is*ws,es+ps,CONFIG['material_tolerance'],abs(es+ps))
            ck.test('mass_action',np.asarray(hmat['action_recovered']),Is,CONFIG['material_tolerance'],abs(Is))
            # Proven eII<=1/R^2 at zero source; no post-outcome velocity clipping.
            ck.test('sound_upper_bound',np.maximum(0.,np.asarray(hmat['cN_c2'])*m.R**3/Is-1.),0.)
            energy=snap['K']+snap['U']+snap['W'];e0=initial['K']+initial['U']+initial['W']
            ck.test('total_action_energy_ledger',energy-e0,snap['ledger'][4],CONFIG['readout_tolerance'])
            mech=snap['K']+snap['U']-initial['K']-initial['U']
            ck.test('mechanical_work_ledger',mech,sum(snap['ledger'][:3]),CONFIG['readout_tolerance'])
            mh=float(np.sum(m.masses[1]))
            hard_mech=snap['K_species'][1]+snap['U']-initial['K_species'][1]-initial['U']
            ck.test('hard_mechanical_work_per_rest_mass',hard_mech/mh,snap['ledger'][9]/mh,CONFIG['readout_tolerance'])
            ck.test('baryon_mechanical_work',snap['K_species'][0]-initial['K_species'][0],
                    snap['ledger'][0]-snap['ledger'][7]+snap['ledger'][2]-snap['ledger'][8],CONFIG['readout_tolerance'])
            for species in ['baryon','hard']:ck.test('fixed_mass_'+species,sum(snap['species'][species]['cell_masses_over_M']),sum(initial['species'][species]['cell_masses_over_M']))
        # Numerical dust control retains the same background/material but removes
        # only the pressure kick; none of its energy residuals qualifies the fluid.
        dust=Model(case,old,cert,pressure=False);dvec,dstats=rk4(dust,dust.step/2)
        dust_differences=[]
        for it,(t,y) in enumerate(zip(CONFIG['times'],dvec)):
            oo=dust.read(t,y);saved=dust.old['samples'][it]['fields']['f'];zs=np.arange(257)/16
            take=np.arange(0,dust.N+1,max(1,round((1/16)/case['dx'])))
            labels=dust.x0[take];expected=labels*np.interp(labels,zs,saved)
            dust_differences.append(dict(tau=t,labels=labels.tolist(),expected_shadow_faces=expected.tolist(),
                baryon_minus_shadow=(oo['meshes'][0][take]-expected).tolist(),hard_minus_shadow=(oo['meshes'][1][take]-expected).tolist()))
        out.update(status='COMPLETE_FINITE_R_NUMERICAL_CASE' if not ck.failures else 'FAILED_NUMERICAL_CHECKS',
            source_state=m.s,background_reference=m.ref,step=m.step,prior_characteristic_travel_bound=m.speed_cap*CONFIG['times'][-1],
            numerical_accumulator=dict(float_bits=np.finfo(float).nmant,longdouble_bits=np.finfo(np.longdouble).nmant),
            units=dict(ell_m=m.ell,t_dyn_s=m.td,seed_mass_kg=m.M,epsilon=m.eps,rho_unit=m.rho_unit,v_dyn_m_s=math.sqrt(m.v2),
                q_baryon_background=m.qb,q_hard_background=m.qh),
            inherited_omissions={key:m.old[key] for key in ['ordinary_radiation_H2_omission_fraction_today',
                'radiation_active_mass_per_unit_brightness_kg_m3','complete_radiation_brightness_envelope']},
            prior_interface_margin=case['L']-2*CONFIG['times'][-1]-CONFIG['watch_radius']-m.speed_cap*CONFIG['times'][-1],
            samples=samples,method_vectors={k:[v.tolist() for v in rows] for k,rows in runs.items()},integrator_statistics=stats,
            sampled_stage_maxima=m.maxima,minimum_sampled_stage_volume_ratio=m.minimum_volume_ratio,
            max_action_root_error=m.eos.max_action_error,dust_control=dict(statistics=dstats,comparisons=dust_differences),
            spatial_continuum_qualified=False,rigorous_characteristic_or_shock_interval_proved=False,
            full_relativistic_metric_qualified=False,observational_fit=False)
    except BaseException as exc:
        out.update(status='FAILED_RETAINED',exception=traceback.format_exc(),finished_method_vectors={k:[v.tolist() for v in rows] for k,rows in runs.items()},integrator_statistics=stats)
        if isinstance(exc,Stop):
            state=np.asarray(exc.y,dtype='<f8')
            out.update(failure_tau=exc.t,failure_state=[float(v) if math.isfinite(v) else None for v in state],
                       failure_state_ieee754_little_endian_base64=base64.b64encode(state.tobytes()).decode(),reason=exc.why)
        elif m is not None and m.last is not None:out.update(last_rhs_tau=m.last[0],last_rhs_state=m.last[1].tolist())
    out.update(checks=ck.counts,worst_errors=ck.maxima,failures=ck.failures,seconds=time.perf_counter()-start,
               peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return out


def main():
    old,cert,fr=inputs();args=sys.argv[1:]
    if args==['freeze']:print(encode(fr).decode());return
    if len(args)!=2 or args[0]!='run-case':raise RuntimeError('Use freeze or run-case INDEX')
    idx=int(args[1])
    if idx<0 or idx>=len(fr['cases']):raise RuntimeError('Bad case index')
    if json.loads(FREEZE.read_bytes())!=fr:raise RuntimeError('Missing/changed freeze')
    payload=run_case(fr['cases'][idx],old,cert)
    print(encode(dict(freeze_sha256=digest(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())


if __name__=='__main__':main()
