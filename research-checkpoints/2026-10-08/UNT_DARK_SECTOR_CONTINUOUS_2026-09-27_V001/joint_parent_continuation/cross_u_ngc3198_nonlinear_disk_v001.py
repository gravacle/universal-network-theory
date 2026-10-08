"""Root-owned S_cross weak-static, charged, two-vector-component disk BVP.

No old AQUAL operator is imported. Positive shared Q1 quadrature defines
the residual AND its exact symmetric Jacobian. The Jacobian may be indefinite.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, time
import numpy as np
import galaxy_density as density

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_NGC3198_NONLINEAR_DISK_V001'
PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900'}
C=1.98; ELL=.1; GC=3*math.pi/8
A0=1.0059833281731022e-10; KPC=3.085677581491367e19
LIGHT=299792458.; B=A0*KPC/LIGHT**2
A0_V=A0*KPC/1e6
EPS=(1e-6,1e-5,1e-4,1e-3)

def now(): return datetime.now(timezone.utc).isoformat()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def authenticate():
    assert PINS, 'Unfrozen author draft cannot execute'
    for name,h in PINS.items(): assert sha(BASE/name)==h, ('changed input',name)
def publish(name,obj):
    p=BASE/name
    raw=(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    with p.open('xb') as f:
        f.write(raw)
        f.flush(); os.fsync(f.fileno())
    p.chmod(0o444); return sha(p)
def save_state(case,step,x,history,identity,linear_partial=None):
    suffix=f'STEP_{step:03d}' if linear_partial is None else f'LINEAR_FAILED_{step:03d}'
    name=f'{STEM}_{case}_{suffix}.npz'; p=BASE/name
    ht=json.dumps(history,allow_nan=False); ident=json.dumps(identity,sort_keys=True,allow_nan=False)
    with p.open('xb') as f:
        fields=dict(state=x,history=ht,identity=ident)
        if linear_partial is not None:fields['unaccepted_linear_partial']=linear_partial
        np.savez_compressed(f,**fields)
        f.flush(); os.fsync(f.fileno())
    p.chmod(0o444)
    publish(name+'.commit.json',dict(file=name,sha256=sha(p),identity=identity))

def edges(refine,extent):
    # Independent radial/vertical axes: explicit thin-sheet trace at z=0.
    r=np.r_[np.linspace(0,2,10*refine+1),
            np.linspace(2,50,60*refine+1)[1:],
            np.geomspace(51,extent,16*refine)]
    z=np.r_[np.linspace(0,1,20*refine+1),
            np.geomspace(1.08,extent,24*refine)]
    assert np.all(np.diff(r)>0) and np.all(np.diff(z)>0)
    return r,z

def shape_quadrature(r,z):
    dr=np.diff(r)[:,None]; dz=np.diff(z)[None,:]
    nodes=(-1/math.sqrt(3),1/math.sqrt(3)); out=[]
    for u in nodes:
        for v in nodes:
            rr=(r[:-1,None]+r[1:,None])/2+u*dr/2
            volume=rr*dr*dz/4
            shapes=[]
            for i,j in ((0,0),(1,0),(0,1),(1,1)):
                si=1 if i else -1; sj=1 if j else -1
                shapes.append(((1+si*u)*(1+sj*v)/4,
                               si*(1+sj*v)/(2*dr),sj*(1+si*u)/(2*dz),i,j))
            out.append((rr,volume,shapes))
    return out

def interpolate(x,shapes):
    val=np.zeros(x.shape[:-2]+(x.shape[-2]-1,x.shape[-1]-1))
    gr=np.zeros_like(val); gz=np.zeros_like(val)
    for n,nr,nz,i,j in shapes:
        xx=x[...,i:x.shape[-2]-1+i,j:x.shape[-1]-1+j]
        val+=n*xx; gr+=nr*xx; gz+=nz*xx
    return val,gr,gz

def add(out,value,gr,gz,volume,shapes):
    for n,nr,nz,i,j in shapes:
        out[...,i:out.shape[-2]-1+i,j:out.shape[-1]-1+j]+=volume*(n*value+nr*gr+nz*gz)

def surface_load(r,profiles,order):
    nodes,weights=np.polynomial.legendre.leggauss(order)
    load=np.zeros(len(r)); all_breaks=np.unique(np.concatenate([p.r for p in profiles.values()]))
    factor=2*math.pi*1e6*density.G_KPC_KMS2_MSUN/A0_V
    for i,(lo,hi) in enumerate(zip(r,r[1:])):
        breaks=np.r_[lo,all_breaks[(all_breaks>lo)&(all_breaks<hi)],hi]
        for a,b in zip(breaks,breaks[1:]):
            x=(a+b)/2+(b-a)*nodes/2
            sigma=sum(p.sigma(x) for p in profiles.values())
            q=factor*(b-a)/2*weights*x*sigma
            load[i]+=np.sum(q*(hi-x)/(hi-lo)); load[i+1]+=np.sum(q*(x-lo)/(hi-lo))
    return load

class Model:
    def __init__(self,r,z,m,ep,fixed,profiles):
        self.r,self.z,self.ep=r,z,ep
        xi,ww=np.polynomial.legendre.leggauss(m); self.xi=(xi+1)/2
        self.w=ww*self.xi; self.sw=np.sqrt(self.w)[:,None,None]
        self.quartic=(1/(self.w*GC**2*self.xi**4))[:,None,None]
        self.quad=shape_quadrature(r,z)
        self.shape=(1+2*m,len(r),len(z))
        self.mask=np.ones(self.shape,bool)
        self.mask[:,-1,:]=False; self.mask[:,:,-1]=False
        self.mask[1::2,0,:]=False; self.mask[2::2,:,0]=False
        self.load=surface_load(r,profiles,16)
        alt=surface_load(r,profiles,32)
        exact=2*math.pi*1e6*density.G_KPC_KMS2_MSUN/A0_V*sum(float(p.integral(0,r[-1])) for p in profiles.values())
        self.source_checks=dict(surface_quadrature_relative=float(np.max(abs(alt-self.load))/max(1.,float(np.sum(self.load)))),
                                exact_annular_mass_relative=abs(float(np.sum(self.load))-exact)/exact,
                                positive_weights=bool(np.all(self.w>0)),weight_sum_error=abs(float(np.sum(self.w))-1))
        self.norm=1/ep-math.log1p(1/ep); self.A=1.5*fixed['OA']/fixed['rG']
        target=.5*ep*self.norm*fixed['d0']; s=target
        for _ in range(12):
            q=math.sqrt(1+ep*s/(1+s)); dq=ep/(2*q*(1+s)**2); s-=(s*q-target)/(q+s*dq)
        self.s0=s; self.u0=ep*s/(1+s)
        self.kappa=2*(fixed['Hunit']/KPC)**2*KPC/(C*A0)
        self.rho0,self.p0,_,_,_,_=self.clock(np.zeros((1,)))
        self.rho0=float(self.rho0[0]); self.p0=float(self.p0[0])
        self.rhs=np.zeros(self.shape); self.rhs[0,:,0]=self.load
        self.rhs[~self.mask]=0

    def clock(self,psi):
        delta=(1+self.u0)*np.expm1(-2*B*psi)
        u=self.u0+delta
        if not np.all(np.isfinite(u)) or np.any(u<=0) or np.any(u>=self.ep):
            raise ValueError('Charged P(X) domain 0<q²−1<epsilon failed')
        s=u/(self.ep-u); q=np.sqrt(1+u)
        pe=(np.log1p(s)-s/(1+s))/self.norm
        dd=2*q*s/(self.ep*self.norm); w=self.A*q*dd
        cs=self.ep*s/(2+(4+3*self.ep)*s+2*(1+self.ep)*s*s)
        gap=self.ep-u; gap0=self.ep-self.u0
        ds=self.ep*delta/(gap*gap0)
        dpe=(np.log1p(ds/(1+self.s0))-ds/((1+s)*(1+self.s0)))/self.norm
        dqd=2*((1+u)*ds+self.s0*delta)/(self.ep*self.norm)
        return self.A*(1+q*dd-pe),self.A*(pe-1),w/cs,w,self.A*(dqd-dpe),self.A*dpe

    def residual(self,x,jacobian=True):
        assert x.shape==self.shape and np.all(x[~self.mask]==0)
        if not np.all(np.isfinite(x)):raise ValueError('Nonfinite candidate field')
        self.clock(x[0])  # Q1 scalar extrema occur at nodes: full-domain check.
        out=self.rhs.copy(); diag=np.zeros(self.shape); cache=[]
        for rr,volume,shapes in self.quad:
            val,gr,gz=interpolate(x,shapes)
            rho,p,D,w,drho,dp=self.clock(val[0]); active=drho+3*dp
            rv,zv=val[1::2],val[2::2]
            norm=rv*rv+zv*zv; t=1+self.quartic*norm
            Zr=np.sum(self.sw*rv,axis=0); Zz=np.sum(self.sw*zv,axis=0)
            add(out[0],self.kappa*active,gr[0]-Zr,gz[0]-Zz,volume,shapes)
            add(out[1::2],t*rv+ELL**2*rv/rr**2-self.sw*gr[0],ELL**2*gr[1::2],ELL**2*gz[1::2],volume,shapes)
            add(out[2::2],t*zv-self.sw*gz[0],ELL**2*gr[2::2],ELL**2*gz[2::2],volume,shapes)
            dd=-self.kappa*B*(D+3*w)
            for n,nr,nz,i,j in shapes:
                sl=(slice(None),slice(i,len(self.r)-1+i),slice(j,len(self.z)-1+j))
                diag[sl][0]+=volume*(nr*nr+nz*nz+dd*n*n)
                diag[sl][1::2]+=volume*((t+2*self.quartic*rv*rv+ELL**2/rr**2)*n*n+ELL**2*(nr*nr+nz*nz))
                diag[sl][2::2]+=volume*((t+2*self.quartic*zv*zv)*n*n+ELL**2*(nr*nr+nz*nz))
            cache.append((rr,volume,shapes,rv,zv,t,dd))
        out[~self.mask]=0
        if not np.all(np.isfinite(out)) or not np.all(np.isfinite(diag)):
            raise ValueError('Nonfinite nonlinear residual/diagonal')
        floor=max(1e-30,float(np.max(abs(diag)))*1e-14)
        pre=np.maximum(abs(diag),floor); pre[~self.mask]=1
        if not jacobian: return out,pre
        def apply(dx):
            assert np.all(dx[~self.mask]==0) and np.all(np.isfinite(dx))
            ans=np.zeros_like(dx)
            for rr,volume,shapes,rv,zv,t,dd in cache:
                dv,dgr,dgz=interpolate(dx,shapes); dr,dz=dv[1::2],dv[2::2]
                dot=rv*dr+zv*dz; zr=np.sum(self.sw*dr,axis=0); zz=np.sum(self.sw*dz,axis=0)
                add(ans[0],dd*dv[0],dgr[0]-zr,dgz[0]-zz,volume,shapes)
                add(ans[1::2],t*dr+2*self.quartic*rv*dot+ELL**2*dr/rr**2-self.sw*dgr[0],ELL**2*dgr[1::2],ELL**2*dgz[1::2],volume,shapes)
                add(ans[2::2],t*dz+2*self.quartic*zv*dot-self.sw*dgz[0],ELL**2*dgr[2::2],ELL**2*dgz[2::2],volume,shapes)
            ans[~self.mask]=0; return ans
        return out,pre,apply

def bicgstab(apply,rhs,tolerance,cap=600):
    """Indefinite operator allowed; zero/breakdown saved, never altered."""
    x=np.zeros_like(rhs); r=rhs.copy(); shadow=r.copy(); p=np.zeros_like(r); v=p.copy()
    rho_old=alpha=omega=1.; norm=float(np.linalg.norm(rhs))
    if norm==0:return x,dict(ok=True,iterations=0,error=0.,reason='zero_rhs')
    def close(it,reason):
        error=float(np.linalg.norm(rhs-apply(x))/norm) if np.all(np.isfinite(x)) else math.inf
        return x,dict(ok=math.isfinite(error) and error<=tolerance,iterations=it,
                      error=error if math.isfinite(error) else None,reason=reason)
    for it in range(1,cap+1):
        rho=float(np.sum(shadow*r))
        if not math.isfinite(rho) or rho==0 or omega==0:return close(it-1,'scalar_breakdown')
        beta=(rho/rho_old)*(alpha/omega)
        if not math.isfinite(beta):return close(it-1,'nonfinite_beta')
        p=r+beta*(p-omega*v)
        if not np.all(np.isfinite(p)):return close(it-1,'nonfinite_direction')
        v=apply(p)
        if not np.all(np.isfinite(v)):return close(it-1,'nonfinite_action')
        den=float(np.sum(shadow*v))
        if not math.isfinite(den) or den==0:return close(it-1,'alpha_breakdown')
        alpha=rho/den; s=r-alpha*v
        if not math.isfinite(alpha) or not np.all(np.isfinite(s)):return close(it-1,'nonfinite_alpha_or_intermediate')
        if float(np.linalg.norm(s))/norm<=tolerance:
            x+=alpha*p; return close(it,'early_true_residual')
        t=apply(s); tt=float(np.sum(t*t))
        if not math.isfinite(tt) or tt==0:return close(it-1,'omega_breakdown')
        omega=float(np.sum(t*s))/tt
        if not math.isfinite(omega):return close(it-1,'nonfinite_omega')
        x+=alpha*p+omega*s; r=s-omega*t
        if not np.all(np.isfinite(x)):return close(it,'nonfinite_linear_state')
        if float(np.linalg.norm(r))/norm<=tolerance:return close(it,'true_residual')
        rho_old=rho
    return close(cap,'iteration_allowance')

def observation_rows():
    rows=[]
    for line in (BASE.parent/'ngc3198_sparc_excerpt_v001.txt').read_text().splitlines():
        if line.startswith('NGC3198 '):
            v=line.split(); rows.append(dict(R=float(v[2]),velocity=float(v[3]),error=float(v[4])))
    assert len(rows)==43; return rows

def implementation_controls(fixed):
    """Meaningful exact-variational and indefinite-linear-solver checks."""
    mesh=np.array([0.,.1,.4,1.,2.])
    model=Model(mesh,mesh,2,1e-3,fixed,density.profiles(False,False))
    rng=np.random.default_rng(20261006)
    x=.01*rng.normal(size=model.shape)
    x[1::2]*=model.sw*model.xi[:,None,None]**2
    x[2::2]*=model.sw*model.xi[:,None,None]**2
    x[~model.mask]=0
    p=.01*rng.normal(size=model.shape);v=.01*rng.normal(size=model.shape)
    p[~model.mask]=0;v[~model.mask]=0
    r,_,H=model.residual(x); h=1e-4
    rp,_=model.residual(x+h*p,False);rm,_=model.residual(x-h*p,False)
    hp=H(p);hv=H(v)
    fd=float(np.linalg.norm((rp-rm)/(2*h)-hp)/np.linalg.norm(hp))
    sym=abs(float(np.sum(v*hp)-np.sum(p*hv)))/max(1e-30,float(np.linalg.norm(v)*np.linalg.norm(hp)),float(np.linalg.norm(p)*np.linalg.norm(hv)))
    mat=np.array([[2.,3.],[3.,-1.]])
    answer,details=bicgstab(lambda y:mat@y,np.array([1.,2.]),1e-12,20)
    er=float(np.max(abs(answer-np.array([7/11,-1/11]))))
    checks=[dict(name='nonlinear_exact_Jacobian',error=fd,tolerance=1e-7),
            dict(name='shared_variational_adjoint',error=sym,tolerance=2e-12),
            dict(name='indefinite_linear_system',error=er,tolerance=2e-12)]
    for t in checks:t['passed']=math.isfinite(t['error']) and t['error']<=t['tolerance']
    assert details['ok'] and all(t['passed'] for t in checks),checks
    return checks

def solve_case(model,name,identity):
    tick=time.monotonic(); x=np.zeros(model.shape); history=[]
    r,pre,apply=model.residual(x); scale=float(np.linalg.norm(model.rhs/np.sqrt(pre)))
    assert scale>0 and math.isfinite(scale)
    save_state(name,0,x,history,identity)
    status='NEWTON_ALLOWANCE'
    for outer in range(30):
        r,pre,apply=model.residual(x); root=np.sqrt(pre)
        error=float(np.linalg.norm(r/root)/scale)
        if error<=1e-8:status='CONVERGED';break
        def whiten(v):return apply(v/root)/root
        target=min(.001,max(1e-10,.05*math.sqrt(error)))
        delta,lin=bicgstab(whiten,-r/root,target)
        row=dict(outer=outer,error=error,linear=lin)
        if not lin['ok']:
            history.append(row);save_state(name,outer,x,history,identity,delta)
            status='LINEAR_FAILED';break
        delta/=root; accepted=False
        for back in range(32):
            step=2.**(-back); candidate=x+step*delta
            try:
                cr,_=model.residual(candidate,False)
                candidate_error=float(np.linalg.norm(cr/root)/scale)
            except ValueError:
                continue
            if math.isfinite(candidate_error) and candidate_error<=(1-1e-4*step)*error:
                x=candidate;accepted=True;row.update(step=step,candidate_error=candidate_error);break
        row['accepted']=accepted;history.append(row)
        if not accepted:status='GLOBALIZATION_FAILED';break
        save_state(name,outer+1,x,history,identity)
        print('DISK',name,'NEWTON',outer+1,'ERROR',candidate_error,flush=True)
    r,pre,apply=model.residual(x); final_error=float(np.linalg.norm(r/np.sqrt(pre))/scale)
    if final_error<=1e-8:status='CONVERGED'
    # Three explicit source-independent Hessian directions. Negative proves
    # an unstable stationary energy direction; positive is not a certificate.
    rays=[];rr=model.r[:,None];zz=model.z[None,:]
    for power in (2,3,4):
        q=(1-(rr/rr[-1])**2)**power*np.cos(math.pi*zz/(2*zz[0,-1]))**power
        qr,qz=np.gradient(q,model.r,model.z,edge_order=2)
        direction=np.zeros_like(x);direction[0]=q
        direction[1::2]=model.sw*qr;direction[2::2]=model.sw*qz
        direction[~model.mask]=0
        rays.append(dict(power=power,quadratic=float(np.sum(direction*apply(direction))),
                         norm_squared=float(np.sum(direction*direction))))
    force=np.gradient(x[0,:,0],model.r,edge_order=2)
    rows=[]
    for obs in observation_rows():
        g=float(np.interp(obs['R'],model.r,force));vsq=obs['R']*A0_V*g
        speed=math.sqrt(vsq) if vsq>=0 else None
        rows.append(dict(obs,radial_force_a0=g,velocity_squared=vsq,model_velocity=speed,
                         residual=None if speed is None else speed-obs['velocity']))
    # Source-load and charged-domain arithmetic checks are independent of fit.
    rho,p,D,w,drho,dp=model.clock(x[0]); active=drho+3*dp
    source_volume=0.;native_volume=0.;native_max=0.;coupling_max=0.
    eta=A0/(LIGHT*(identity['Hunit']/KPC))
    for rad,volume,shapes in model.quad:
        vals,grads_r,grads_z=interpolate(x,shapes)
        val=vals[0];_,_,_,_,qr,qp=model.clock(val)
        source_volume+=float(np.sum(volume*model.kappa*(qr+3*qp)))
        rv,zv=vals[1::2],vals[2::2];norm=rv*rv+zv*zv
        grad2=grads_r[1::2]**2+grads_z[1::2]**2+grads_r[2::2]**2+grads_z[2::2]**2+rv*rv/rad**2
        positive=eta**2*(.02/4*(grads_r[0]**2+grads_z[0]**2)+C/2*np.sum(ELL**2*grad2/2+norm/2+model.quartic*norm*norm/4,axis=0))
        native_max=max(native_max,float(np.max(positive)))
        native_volume+=float(np.sum(volume*model.kappa*positive))
        coupling=np.sum(model.sw*(rv*grads_r[0]+zv*grads_z[0]),axis=0)
        coupling_max=max(coupling_max,float(np.max(abs(eta**2*C/2*coupling))))
    trace_r=(x[0,-1,:]-x[0,-2,:])/(model.r[-1]-model.r[-2])
    outgoing_r=float(model.r[-1]*np.sum(np.diff(model.z)*(trace_r[:-1]+trace_r[1:])/2))
    trace_z=(x[0,:,-1]-x[0,:,-2])/(model.z[-1]-model.z[-2]);dr=np.diff(model.r)
    outgoing_z=float(np.sum(dr*((model.r[:-1]/2+dr/6)*trace_z[:-1]+(model.r[:-1]/2+dr/3)*trace_z[1:])))
    source_total=float(np.sum(model.load))+source_volume
    summaries=[]
    for threshold in (0.,2.,8.):
        selected=[t for t in rows if t['R']>=threshold];valid=[t for t in selected if t['residual'] is not None]
        summaries.append(dict(Rmin=threshold,count=len(selected),nonnegative_force_count=len(valid),
                              RMS=None if len(valid)!=len(selected) else math.sqrt(sum(t['residual']**2 for t in valid)/len(valid)),
                              nominal_error_squared_residual=None if len(valid)!=len(selected) else sum((t['residual']/t['error'])**2 for t in valid)))
    return dict(identity=identity,status=status,numerical_residual=final_error,history=history,
                source_checks=model.source_checks,rows=rows,summaries=summaries,hessian_directions=rays,
                flux=dict(sheet=float(np.sum(model.load)),signed_clock_volume=source_volume,
                          outgoing_face=outgoing_r+outgoing_z,total_source=source_total,
                          relative_imbalance=abs(outgoing_r+outgoing_z-source_total)/max(1.,abs(source_total))),
                negative_direction_found=any(t['quadratic']<0 for t in rays),
                max_abs_log_lapse=float(np.max(abs(B*x[0]))),
                max_abs_pressure_active_normal=float(np.max(abs(3*dp))),
                max_abs_density_normal=float(np.max(abs(drho))),
                max_abs_active_clock_normal=float(np.max(abs(active))),
                omitted_positive_native_normal_source=dict(max_normal=native_max,signed_volume=native_volume,
                    volume_over_sheet=native_volume/float(np.sum(model.load)),max_acceleration_coupling_scale_normal=coupling_max,
                    full_spatial_stress_bound=False),
                min_charge_margin=float(np.min(model.ep-(model.u0+(1+model.u0)*np.expm1(-2*B*x[0])))),
                elapsed_seconds=time.monotonic()-tick,
                physical_flags=dict(full_metric_qualified=False,FLRW_junction_qualified=False,
                                    formation_qualified=False,observational_success_gate=False))

def main():
    authenticate(); source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')), 'Existing work preserved'
    parent=json.loads((BASE/'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text())
    assert len(parent['rows'])==4 and len(parent['controls'])==31 and all(t['passed'] for t in parent['controls'])
    fixed=parent['manifest']['fixed_parent']; assert fixed['rG']==.98/.99
    manifest=dict(source_sha256=source,input_sha256=PINS,owner='root',pid=os.getpid(),started=now(),
                  action='V003 Eq5 S_cross uncompressed',eps=list(EPS),fixed=fixed,
                  physical_constants=dict(C=C,ell_kpc=ELL,gc_over_a0=GC,a0_SI=A0),
                  grid=dict(refine=1,extent_kpc=128,positive_modes=32),
                  state='Aligned finite-wall stationary weak-static lapse BVP; zero outer log lapse/modes',
                  fitted_galaxy_parameters=[],data_exposure='Existing NGC development data; all43rows and4tails retained')
    mh=publish(STEM+'_MANIFEST.json',manifest);outputs={STEM+'_MANIFEST.json':mh};results=[]
    controls=implementation_controls(fixed)
    outputs[STEM+'_IMPLEMENTATION_CONTROLS.json']=publish(STEM+'_IMPLEMENTATION_CONTROLS.json',controls)
    for ep in EPS:
        for hi,h2 in ((False,False),(False,True),(True,False),(True,True)):
            name=f'E{ep:.0e}_HI{int(hi)}_H2{int(h2)}'.replace('-','m')
            r,z=edges(1,128); model=Model(r,z,32,ep,fixed,density.profiles(hi,h2))
            assert all(model.source_checks[k]<=1e-11 for k in ('surface_quadrature_relative','exact_annular_mass_relative','weight_sum_error')) and model.source_checks['positive_weights']
            identity=dict(case=name,manifest_sha256=mh,source_sha256=source,eps=ep,hi_tail=hi,h2_tail=h2,
                          Hunit=fixed['Hunit'],grid_shape=list(model.shape),r_kpc=r.tolist(),z_kpc=z.tolist())
            result=solve_case(model,name,identity);authenticate();assert sha(__file__)==source
            namefile=STEM+'_'+name+'_CASE.json';outputs[namefile]=publish(namefile,result);results.append(result)
            print('DISK_CASE',name,result['status'],flush=True)
    passed=all(t['status']=='CONVERGED' for t in results)
    status='RESIDUALS_PASS_UNQUALIFIED' if passed else 'BRANCH_NUMERICAL_FAILURES_RETAINED'
    result=dict(status=status,manifest=manifest,cases=results,implementation_controls=controls,all_stationary_residuals_pass=passed,
                refinement_qualified=False,joint_superiority_qualified=False,automatic_followup=False)
    rh=publish(STEM+'_RESULT.json',result);outputs[STEM+'_RESULT.json']=rh
    for path in BASE.glob(STEM+'_*'):
        if path.is_file():outputs[path.name]=sha(path)
    receipt=dict(owner='root',pid=os.getpid(),started=manifest['started'],closed=now(),source_sha256=source,
                 manifest_sha256=mh,result_sha256=rh,output_sha256=outputs)
    publish(STEM+'_RECEIPT.json',receipt);print('DISK_BATCH_CLOSED',status,rh,flush=True)
    return 0 if passed else 3

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root-owned',action='store_true')
    assert parser.parse_args().root_owned
    raise SystemExit(main())
