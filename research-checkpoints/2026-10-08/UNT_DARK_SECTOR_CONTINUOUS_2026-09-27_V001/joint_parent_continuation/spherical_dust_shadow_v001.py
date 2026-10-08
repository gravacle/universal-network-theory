"""Inert finite-time moving-source dust shadow; root alone runs. Stdout only."""
import os
for _thread_name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                     'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_thread_name]='1'
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/'SPHERICAL_DUST_SHADOW_V001_FROZEN.json'
CONFIG=dict(gaps=[128,8192],spectrum_index=1,reference=0,beta=.005,
    ell_kpc=3.2,parsec_m=3.085677581491367e16,G_SI=6.67430e-11,c=299792458.,
    shell_max=16.,shell_spacing=1/16,worldtube_labels=[1.,2.,4.,8.,16.],
    times=[0.,1/64,1/32,1/16],rk_steps=[1/512,1/1024],
    dp_rtol=2e-11,dp_atol=2e-13,dp_step_cap=1/256,
    angle_orders=[64,128],action_bisections=64,arithmetic_tolerance=2e-11,
    material_tolerance=2e-10,state_tolerance=2e-8,readout_tolerance=2e-7,
    derivative_steps=[1e-4,5e-5],derivative_tolerance=2e-6,
    ordinary_massless_Neff=3.044,finite_R_trajectory_qualified=False,
    observational_success_gate=None)
PINS={
 'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json':'773a3b57065e9c4fb6894064b6402e31f761dfe1de8beeb0754701c29ef24a04',
 'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_FROZEN.json':'51ba8aa74282b37ffa252a42798d095bae2f194964bfaf7cc34cbe844a1d8d1a',
 'RADIATION_PHOTON_REFERENCE_V001_RESULTS.json':'45d4353256d15b87bf57df3f67a6b581a8f6d347fc42f8eb022f3c43713e7b41',
 'CLOSED_RELEASE_LENSING_AND_COLLISION_CONTINUATION_V001.md':'d7155fa296a29d64c93d7cc047c9498516fde61f100a7c7fff2529e8af583507',
 'POSTCROSSING_COMPLETION_AND_NATIVE_GRADIENT_CUSTODY_V001.md':'36f1c234260d477f1c0f652b87f2aac2b1d7f3a5f03fcbbafd647dcd50a4dd1b'}


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def inputs():
    files={};seen=set()
    def add(p,expected=None):
        p=p.resolve(strict=True);p.relative_to(ROOT)
        h=sha(p)
        if expected is not None and h!=expected:raise RuntimeError('Changed input '+str(p))
        files[str(p.relative_to(ROOT))]=h
        return p
    def manifest(p):
        p=add(p)
        if p in seen:return
        seen.add(p)
        for name,h in json.loads(p.read_text())['files'].items():
            raw=Path(name);opts=[raw] if raw.is_absolute() else [ROOT/raw,p.parent/raw]
            matches={q.resolve() for q in opts if q.is_file() and q.resolve().is_relative_to(ROOT)}
            if len(matches)!=1:raise RuntimeError('Ambiguous ancestor '+name)
            child=add(matches.pop(),h)
            if child.name.endswith('_FROZEN.json'):manifest(child)
    for name,h in PINS.items():add(HERE/name,h)
    fp=HERE/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_FROZEN.json';manifest(fp)
    packet=json.loads((HERE/'SMOOTH_DISK_RELEASE_CERTIFICATE_V001_RESULTS.json').read_text())
    data=packet['payload']
    if packet['freeze_sha256']!=sha(fp) or packet['payload_sha256']!=hashlib.sha256(encode(data)).hexdigest():
        raise RuntimeError('Certificate custody failure')
    if data['status']!='COMPLETE' or data['failures']:raise RuntimeError('Certificate unqualified')
    states=[]
    for gap in CONFIG['gaps']:
        group=[c for c in data['cases'] if c['gap']==gap]
        if len(group)!=2 or any(c['source_state']!=group[0]['source_state'] for c in group):
            raise RuntimeError('Changed duplicate-state mapping')
        states.append(group[0])
    if data['configuration']['spectrum_index']!=1 or data['configuration']['reference']!=0:
        raise RuntimeError('Changed source selection')
    photon=json.loads((HERE/'RADIATION_PHOTON_REFERENCE_V001_RESULTS.json').read_text())
    main=add(HERE/'SAME_ACTION_RADIATION_V001_RESULTS.json',photon['input_sha256'])
    manifest(HERE/'SAME_ACTION_RADIATION_V001_FROZEN.json')
    for name in ['radiation_photon_reference_v001.py','RADIATION_PHOTON_REFERENCE_V001.md',
                 'RADIATION_PHOTON_REFERENCE_RESULT_REVIEW_V001.md',
                 'SPHERICAL_SAME_STATE_RELEASE_REDUCTION_V001.md',
                 'SPHERICAL_DUST_SHADOW_PROTOCOL_V001.md',Path(__file__).name]:add(HERE/name)
    return states,data['reference'],photon,dict(configuration=CONFIG,files=files)


class Checks:
    def __init__(self):self.counts={};self.maxima={};self.failures=[]
    def check(self,name,a,b=0.,scale=1.,tol=None,context=None):
        tol=CONFIG['arithmetic_tolerance'] if tol is None else tol
        err=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
        maximum=float(np.max(err));self.counts[name]=self.counts.get(name,0)+int(err.size)
        self.maxima[name]=max(self.maxima.get(name,0.),maximum)
        if not np.all(np.isfinite(err)) or maximum>tol:
            self.failures.append(dict(check=name,error=maximum,tolerance=tol,context=context))
    def yes(self,name,value,context=None):self.check(name,int(bool(value)),1,context=context)


def shape(z):
    z=np.asarray(z);inside=z<1.;q=np.where(inside,z,1.)
    C=3465/128
    mu=C*(1/3-4*q*q/5+6*q**4/7-4*q**6/9+q**8/11)
    d=C*(-8*q/5+24*q**3/7-24*q**5/9+8*q**7/11)
    dd=C*(-8/5+72*q*q/7-120*q**4/9+56*q**6/11)
    safe=np.where(inside,1.,z)
    mu=np.where(inside,mu,safe**-3);d=np.where(inside,d,-3*safe**-4)
    dd=np.where(inside,dd,12*safe**-5)
    rho=np.where(inside,3465/(512*math.pi)*(1-q*q)**4,0.)
    return mu,d,dd,rho


class Material:
    """Exact positive quadrature at a supplied action, not a new preparation."""
    def __init__(self,R,order):
        x,w=np.polynomial.legendre.leggauss(order)
        th=(x+1)*math.pi/4;self.aw=w*math.pi/4
        self.s2=np.sin(th)**2;self.c2=np.cos(th)**2;self.R=float(R)
    def bar(self,r):
        return (2/math.pi)*np.sum(self.aw*self.c2*np.sqrt(1+np.asarray(r)[...,None]*(1+self.s2)/2),axis=-1)
    def at(self,I):
        I=np.asarray(I,dtype=float)
        if np.any(I<=0) or not np.all(np.isfinite(I)):raise ValueError('Nonpositive action')
        target=I/self.R**3;hi=2*target;lo=hi/np.sqrt(1+hi)
        for _ in range(CONFIG['action_bisections']):
            mid=(lo+hi)/2;low=mid*self.bar(mid)<target
            lo=np.where(low,mid,lo);hi=np.where(low,hi,mid)
        r=(lo+hi)/2;t=r[...,None]*(1+self.s2)/2;q=1+t;sq=np.sqrt(q)
        J=np.sum(self.aw/sq,axis=-1);omega=math.pi/(2*J)
        domega=np.sum(self.aw*t/(sq*(sq+1)),axis=-1)/J
        bar=self.bar(r);e=self.R**4*r*(2+r)/4
        w=r/(2+r)*np.sum(self.aw*self.s2**2/sq,axis=-1)/J;p=w*e
        ell=np.sum(self.aw*(1+self.s2)/(q*sq),axis=-1)
        ci=r*bar*omega*ell/(2*J*(1+r))
        de=domega-p/(self.R*I)
        return dict(I=I,r=r,e=e,p=p,w=w,omega=self.R*omega,cI2=ci,
                    action_recovered=self.R**3*r*bar,dE=de,dW=domega,
                    cN_over_c_squared=omega*ci)


class DomainError(Exception):
    def __init__(self,t,y,reason):self.t=t;self.y=y.copy();self.reason=reason


class Model:
    def __init__(self,source,ref,z):
        self.source=source;self.ref=ref;self.z=np.asarray(z);self.mu,self.dmu,self.ddmu,self.seed=shape(z)
        s=source['source_state'];self.s=s;self.R=source['gap'];self.mat=Material(self.R,128)
        self.I1=s['I'];self.e1=s['E']/CONFIG['beta'];self.gs=s['gstar'];self.Kb=source['Kb']
        self.ell=CONFIG['ell_kpc']*1000*CONFIG['parsec_m'];self.td=math.sqrt(self.ell/self.gs)
        self.vd=self.ell/self.td;self.eps=self.vd**2/CONFIG['c']**2
        self.H0=ref['H0_s_inverse'];G=CONFIG['G_SI'];c=CONFIG['c']
        self.M=self.gs*self.ell**2/G;self.S=self.gs**2/(4*math.pi*G*self.Kb)
        self.rb=3*self.H0**2*ref['Omega_b']/(8*math.pi*G)
        self.rh0=self.S*CONFIG['beta']*self.R*self.I1/c**2
        self.kb=4*math.pi*self.rb*self.ell**3/(3*self.M)
        self.kh=4*math.pi*self.rh0*self.ell**3/(3*self.M);self.kappa=self.kb+self.kh
    def initial(self,n=None):
        n=len(self.z) if n is None else n;y=np.zeros(1+6*n);y[0]=1.;y[1:1+n]=1.;return y
    def H(self,A):
        e=float(self.mat.at(self.I1/A**3)['e'])
        return self.H0*self.td*math.sqrt(self.ref['Omega_b']/A**3+
                 self.ref['Omega_exc']*e/self.e1+self.ref['Omega_Lambda'])
    def rhs(self,t,y,mu=None):
        self.last_evaluation=(float(t),y.copy())
        mu=self.mu if mu is None else mu;A=y[0];v=y[1:].reshape(6,-1);f,fd,fm,fmd,fmm,fmmd=v
        if A<=0 or np.any(f<=0) or not np.all(np.isfinite(y)):raise DomainError(t,y,'NONPOSITIVE_MAP_OR_NONFINITE')
        if mu is self.mu and np.any(f+self.z*fm*self.dmu<=0):raise DomainError(t,y,'SHELL_CROSSING')
        h=self.H(A);fac=A**-3;k=self.kappa
        F=-fac*((mu+k)/f**2-k*f);Ff=fac*(2*(mu+k)/f**3+k)
        Fm=-fac/f**2;Fff=-6*fac*(mu+k)/f**4;Ffm=2*fac/f**3
        ans=np.empty_like(y);ans[0]=A*h
        ans[1:]=np.array([fd,F-2*h*fd,fmd,Ff*fm+Fm-2*h*fmd,
                         fmmd,Ff*fmm+Fff*fm**2+2*Ffm*fm-2*h*fmmd]).ravel()
        return ans


def rk4(rhs,y,step,targets):
    t=0.;samples={0.:y.copy()};path=[(t,y.copy())]
    for target in targets[1:]:
        n=math.ceil((target-t)/step);dt=(target-t)/n
        for _ in range(n):
            k1=rhs(t,y);k2=rhs(t+dt/2,y+dt*k1/2);k3=rhs(t+dt/2,y+dt*k2/2);k4=rhs(t+dt,y+dt*k3)
            y=y+dt*(k1+2*k2+2*k3+k4)/6;t+=dt;rhs(t,y);path.append((t,y.copy()))
        t=target;path[-1]=(t,y.copy());samples[target]=y.copy()
    return samples,path


def dopri(rhs,y,targets):
    t=0.;dt=CONFIG['dp_step_cap'];samples={0.:y.copy()};accepted=0;rejected=0
    aa=[[],[1/5],[3/40,9/40],[44/45,-56/15,32/9],
        [19372/6561,-25360/2187,64448/6561,-212/729],
        [9017/3168,-355/33,46732/5247,49/176,-5103/18656],
        [35/384,0,500/1113,125/192,-2187/6784,11/84]]
    cc=[0,1/5,3/10,4/5,8/9,1,1];b5=np.array([35/384,0,500/1113,125/192,-2187/6784,11/84,0])
    b4=np.array([5179/57600,0,7571/16695,393/640,-92097/339200,187/2100,1/40])
    for target in targets[1:]:
        while t<target:
            dt=min(dt,target-t,CONFIG['dp_step_cap'])
            if t+dt==t:raise DomainError(t,y,'TIME_STEP_UNDERFLOW')
            ks=[]
            for i in range(7):
                yy=y.copy()
                for j,coef in enumerate(aa[i]):yy+=dt*coef*ks[j]
                ks.append(rhs(t+cc[i]*dt,yy))
            K=np.array(ks);out=y+dt*np.dot(b5,K);err=dt*np.dot(b5-b4,K)
            scale=CONFIG['dp_atol']+CONFIG['dp_rtol']*np.maximum(np.abs(y),np.abs(out))
            norm=float(np.max(np.abs(err)/scale))
            if not math.isfinite(norm):raise DomainError(t,y,'NONFINITE_ERROR')
            if norm<=1:
                y=out;t+=dt;rhs(t,y);accepted+=1
            else:rejected+=1
            dt*=min(5.,max(.2,.9*norm**-.2)) if norm else 5.
        samples[target]=y.copy()
    return samples,dict(accepted=accepted,rejected=rejected)


def fields(model,y,order=128):
    A=y[0];f,fd,fm,fmd,fmm,fmmd=y[1:].reshape(6,-1);z=model.z
    fz=fm*model.dmu;fzz=fmm*model.dmu**2+fm*model.ddmu;s=f+z*fz
    J=f*f*s;Jz=2*f*fz*s+f*f*(2*fz+z*fzz)
    if np.any(s<=0) or np.any(J<=0):raise ValueError('Readout crossed shell map')
    mat=model.mat if order==128 else Material(model.R,order)
    o=mat.at(model.I1/(A**3*J));cs2=o['cN_over_c_squared']/model.eps
    force=cs2*Jz/(A*s*J);vp=A*z*fd;h=model.H(A)
    sd=fd+z*fmd*model.dmu;Jd=2*f*fd*s+f*f*sd
    rho0=model.rh0/(A**3*J);rb=(model.rb+model.M/model.ell**3*model.seed)/(A**3*J)
    dlnI=-3*h-Jd/J
    o.update(f=f,f_tau=fd,f_mu=fm,f_mumu=fmm,s=s,J=J,J_z=Jz,
        aP_over_gstar=force,peculiar_velocity_over_vdyn=vp,
        vpec2_over_c2=model.eps*vp**2,rho0_H_kg_m3=rho0,rho_b_kg_m3=rb,
        cN2_over_vdyn2=cs2,pressure_Pa=model.S*CONFIG['beta']*o['p'],
        internal_energy_per_restmass_over_vdyn2=o['dE']/model.eps,
        internal_energy_rate_over_vdyn2_per_tau=o['p']/(model.R*o['I'])/model.eps*dlnI,
        rest_gravity_energy_defect_kg_m3=rho0*o['dE'],
        active_pressure_mass_kg_m3=3*model.S*CONFIG['beta']*o['p']/CONFIG['c']**2)
    return o


def snapshot(model,t,y,ck):
    o=fields(model,y);q=fields(model,y,64);A=y[0];ctx=dict(gap=model.R,tau=t)
    for key in ['e','p','omega','cI2','dE','dW']:
        ck.check('quadrature_'+key,o[key],q[key],np.maximum(np.abs(o[key]),1e-300),CONFIG['material_tolerance'],ctx)
    ck.check('action_reconstruction',o['action_recovered'],o['I'],o['I'],context=ctx)
    ck.check('virial',o['I']*o['omega'],o['e']+o['p'],o['e'],context=ctx)
    ck.check('common_flow_ratio',o['rho0_H_kg_m3']/o['rho_b_kg_m3'],
             model.rh0/(model.rb+model.M/model.ell**3*model.seed),context=ctx)
    world=[]
    for z in CONFIG['worldtube_labels']:
        i=int(round(z/CONFIG['shell_spacing']));f=o['f'][i]
        deficit=-math.expm1(3*math.log(float(f)))
        hmass=model.kh*z**3*deficit;bmass=float(model.mu[i])*z**3+model.kb*z**3*deficit
        world.append(dict(initial_label=z,physical_radius_m=A*z*f*model.ell,
            hard_rest_mass_kg=model.kh*z**3*model.M,
            hard_rest_excess_over_seed_M=hmass,baryon_rest_excess_over_seed_M=bmass,
            hard_rest_excess_over_baryon_rest_excess=hmass/bmass if bmass else None,
            hard_current_mass_label_over_seed_M=model.kh*z**3,
            baryon_current_mass_label_over_seed_M=float(model.mu[i])*z**3+model.kb*z**3))
    return dict(tau=t,seconds=t*model.td,A=A,H_s_inverse=model.H(A)/model.td,
                fields={k:np.asarray(v).tolist() for k,v in o.items()},worldtubes=world)


def forcing(model,path):
    n=len(model.z);weighted=np.zeros(n);disp=np.zeros(n);work=np.zeros(n);internal_work=np.zeros(n);travel=0.
    previous=None;maxima=dict(dE=0.,dW=0.,vpec2_over_c2=0.,pressure_force_abs=0.)
    minJ=math.inf;mins=math.inf
    for t,y in path:
        o=fields(model,y);A=y[0];fp=o['aP_over_gstar'];v=o['peculiar_velocity_over_vdyn']
        rate=A*np.abs(fp);power=v*fp;speed=float(np.max((np.abs(v)+np.sqrt(o['cN2_over_vdyn2']))/A))
        internal_rate=o['internal_energy_rate_over_vdyn2_per_tau']
        if previous is not None:
            tp,Ap,rp,pp,sp,ip=previous;dt=t-tp;old=weighted.copy()
            weighted+=dt*(rp+rate)/2
            disp+=dt*(old/Ap**2+weighted/A**2)/2
            work+=dt*(pp+power)/2;travel+=dt*(sp+speed)/2
            internal_work+=dt*(ip+internal_rate)/2
        else:initial_internal=o['internal_energy_per_restmass_over_vdyn2'].copy()
        previous=(t,A,rate,power,speed,internal_rate)
        for key in ['dE','dW','vpec2_over_c2']:maxima[key]=max(maxima[key],float(np.max(o[key])))
        maxima['pressure_force_abs']=max(maxima['pressure_force_abs'],float(np.max(np.abs(fp))))
        minJ=min(minJ,float(np.min(o['J'])));mins=min(mins,float(np.min(o['s'])))
    return dict(free_velocity_bound_diagnostic_over_vdyn=(weighted/path[-1][1][0]).tolist(),
        free_comoving_displacement_diagnostic_over_ell=disp.tolist(),
        signed_pressure_source_work_per_restmass_over_vdyn2=work.tolist(),
        thermodynamic_volume_work_per_restmass_over_vdyn2=internal_work.tolist(),
        exact_internal_energy_change_per_restmass_over_vdyn2=(o['internal_energy_per_restmass_over_vdyn2']-initial_internal).tolist(),
        volume_work_trapezoid_defect_over_vdyn2=(internal_work-o['internal_energy_per_restmass_over_vdyn2']+initial_internal).tolist(),
        sampled_maxima=maxima,sampled_min_J=minJ,sampled_min_radial_jacobian=mins,
        shadow_characteristic_travel_over_ell=travel,
        prospective_interface_margins={str(L):L-4.-travel for L in [8.,16.]},
        actual_force_and_Lipschitz_tube='NOT_PROVED',
        actual_finite_R_acoustic_domain='NOT_QUALIFIED',finite_R_trajectory_qualified=False)


def controls(model,ck):
    z=model.z;mu,d,dd,rho=shape(z)
    ck.check('source_center_mu',mu[0],1155/128)
    ck.check('source_integrated_polynomial_mass',3465/128*(1/3-4/5+6/7-4/9+1/11),1.)
    ck.check('source_mass_edge',shape(np.array([1.]))[0][0],1.)
    ck.check('source_poisson_mass_derivative',3*mu+z*d,4*math.pi*rho)
    ck.check('source_second_derivative',4*d+z*dd,
       np.where(z<1,-32*math.pi*(3465/(512*math.pi))*z*np.maximum(1-z*z,0.)**3,0.))
    y=model.initial(3);hs,_=rk4(lambda t,y:model.rhs(t,y,np.zeros(3)),y,1/1024,CONFIG['times'])
    homogeneous=hs[CONFIG['times'][-1]][1:].reshape(6,3)
    ck.check('homogeneous_exact_map',homogeneous[0],1.)
    ck.check('homogeneous_exact_velocity',homogeneous[1],0.)
    # Independent scalar homogeneous-sphere energy control, no cosmological source.
    def rhs2(t,y):return np.array([y[1],-1./y[0]**2])
    orbit,_=rk4(rhs2,np.array([1.,0.]),1/1024,CONFIG['times'])
    for t,y in orbit.items():ck.check('sphere_energy',y[1]**2/2-1/y[0]+1,tol=CONFIG['state_tolerance'])
    testmu=np.array([0.,1.,1155/128]);base,_=rk4(lambda t,y:model.rhs(t,y,testmu),model.initial(3),1/1024,CONFIG['times'])
    target=CONFIG['times'][-1];b=base[target][1:].reshape(6,3);der=[]
    for h in CONFIG['derivative_steps']:
        p,_=rk4(lambda t,y:model.rhs(t,y,testmu+h),model.initial(3),1/1024,CONFIG['times'])
        m,_=rk4(lambda t,y:model.rhs(t,y,testmu-h),model.initial(3),1/1024,CONFIG['times'])
        fp=p[target][1:4];fm=m[target][1:4]
        der.append(((fp-fm)/(2*h),(fp-2*b[0]+fm)/h**2))
    for j,name in [(0,'first'),(1,'second')]:
        extrap=(4*der[1][j]-der[0][j])/3
        ck.check('parameter_'+name,extrap,b[2 if j==0 else 4],tol=CONFIG['derivative_tolerance'])
    a=model.mat.at(model.I1);s=model.s
    for key,expected in [('e',model.e1),('p',s['pressure']/CONFIG['beta']),('omega',s['omega']),('cI2',s['cI2'])]:
        ck.check('saved_anchor_'+key,float(a[key]),expected,max(abs(expected),1e-300),CONFIG['material_tolerance'])


def run(sources,ref,photon):
    started=time.perf_counter();ck=Checks();rows=[]
    z=np.arange(round(CONFIG['shell_max']/CONFIG['shell_spacing'])+1)*CONFIG['shell_spacing']
    og=next(q['Omega_gamma'] for q in photon['references'] if q['reference']==CONFIG['reference'])
    orad=og*(1+(7/8)*(4/11)**(4/3)*CONFIG['ordinary_massless_Neff'])
    for source in sources:
        model=Model(source,ref,z);entry=dict(gap=model.R,source_state=model.s,
             finite_R_trajectory_qualified=False,ell_m=model.ell,t_dyn_s=model.td,
             seed_mass_kg=model.M,epsilon=model.eps,initial_potential_compactness=693/256*model.eps,
             rho0_H1_kg_m3=model.rh0,kappa=model.kappa,background_reference=ref,
             ordinary_radiation_H2_omission_fraction_today=orad,
             radiation_active_mass_per_unit_brightness_kg_m3=2*3*model.H0**2*orad/(8*math.pi*CONFIG['G_SI']),
             complete_radiation_brightness_envelope='NOT_COMPUTED; needs absolute potential/time norms')
        try:
            controls(model,ck);allruns=[];paths=[]
            for step in CONFIG['rk_steps']:
                sm,path=rk4(model.rhs,model.initial(),step,CONFIG['times']);allruns.append(sm);paths.append(path)
            dp,stats=dopri(model.rhs,model.initial(),CONFIG['times']);allruns.append(dp)
            for t in CONFIG['times']:
                fine=allruns[1][t]
                for method,sm in [('coarse_RK4',allruns[0]),('DOPRI54',dp)]:
                    ck.check('method_state',sm[t],fine,np.maximum(1.,np.maximum(np.abs(sm[t]),np.abs(fine))),CONFIG['state_tolerance'],[model.R,t,method])
                    a,b=fields(model,sm[t]),fields(model,fine)
                    for key in ['J','aP_over_gstar','cN2_over_vdyn2','dE','dW']:
                        ck.check('method_'+key,a[key],b[key],np.maximum(1.,np.maximum(np.abs(a[key]),np.abs(b[key]))),CONFIG['readout_tolerance'],[model.R,t,method])
            entry.update(status='COMPLETE_DUST_SHADOW_ONLY',integrator_statistics=stats,
                samples=[snapshot(model,t,allruns[1][t],ck) for t in CONFIG['times']],
                method_sample_vectors={name:[sm[t].tolist() for t in CONFIG['times']]
                    for name,sm in zip(['RK4_coarse','RK4_fine','DOPRI54'],allruns)},
                fine_path_times=[t for t,_ in paths[1]],fine_path_vectors=[y.tolist() for _,y in paths[1]],
                accumulated_forcing=forcing(model,paths[1]),
                alternate_node_forcing=forcing(model,paths[1][::2]))
        except DomainError as exc:
            entry.update(status='FAILED_CLASSICAL_OR_NUMERICAL_DOMAIN',reason=exc.reason,tau=exc.t,last_state=exc.y.tolist())
            ck.failures.append(dict(check='domain',gap=model.R,reason=exc.reason,tau=exc.t))
        except Exception as exc:
            entry.update(status='FAILED_EXCEPTION',exception_type=type(exc).__name__,reason=str(exc))
            if hasattr(model,'last_evaluation'):
                entry['last_rhs_tau']=model.last_evaluation[0]
                entry['last_rhs_state']=model.last_evaluation[1].tolist()
            ck.failures.append(dict(check='exception',gap=model.R,type=type(exc).__name__,reason=str(exc)))
        rows.append(entry)
    return dict(status='COMPLETE_DUST_SHADOW_ONLY' if not ck.failures else 'FAILED_CHECKS',
        configuration=CONFIG,shell_labels=z.tolist(),state_vector_layout=['A','f[N]','f_tau[N]','f_mu[N]','f_mu_tau[N]','f_mumu[N]','f_mumu_tau[N]'],
        cases=rows,checks=ck.counts,worst_scaled_errors=ck.maxima,failures=ck.failures,
        scope='Moving-source spherical dust reference and unchanged finite-R residuals, not a finite-R solution or lensing prediction',
        finite_R_trajectory_qualified=False,seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ('freeze','run'):raise SystemExit('Use freeze or run')
    src,ref,ph,snapshot=inputs()
    if sys.argv[1]=='freeze':print(encode(snapshot).decode());return
    if not FREEZE.is_file() or json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError('Missing/changed freeze')
    payload=run(src,ref,ph)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())


if __name__=='__main__':main()
