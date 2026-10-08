"""Independent small projection diagnostic; no galaxy solve or live-state replay."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os
import numpy as np
import cross_u_ngc3198_nonlinear_disk_v001 as core

BASE=Path(__file__).resolve().parent
STEM='CROSS_U_Q1_PROJECTION_STIFFNESS_V001'
PINS={
    'cross_u_ngc3198_nonlinear_disk_v001.py':'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1',
    'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md':'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76',
    'CROSS_U_Q1_PROJECTION_STIFFNESS_V001.md':'c3ab70d3274feb39499c2b0eca482686085071362657a4766a93ecba071f00f9'}

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def auth():
    for n,h in PINS.items():assert sha(BASE/n)==h,('changed input',n)
    core.authenticate()
    assert core.ELL==.1 and core.C==1.98
def publish(name,obj):return core.publish(name,obj)

def close(source,manifest,result):
    auth();assert source==sha(__file__)
    result.update(manifest=manifest,observational_prediction=False,
                  physical_failure_verdict=False,joint_superiority_qualified=False)
    rh=publish(STEM+'_RESULT.json',result)
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    publish(STEM+'_RECEIPT.json',dict(owner='root',pid=os.getpid(),source_sha256=source,
                                   started=manifest['started'],closed=now(),result_sha256=rh,output_sha256=outputs))
    print('PROJECTION_CLOSED',result['status'],flush=True)

def control_record(name,result,partial):
    if not result['passed']:
        file=f'{STEM}_{name}_PARTIAL.npz';path=BASE/file
        with path.open('xb') as f:
            np.savez_compressed(f,unaccepted_linear_partial=partial)
            f.flush();os.fsync(f.fileno())
        path.chmod(0o444);result.update(partial_file=file,partial_sha256=sha(path))
    publish(f'{STEM}_{name}_CP.json',result)

def pcg(A,b,diagonal,tolerance=1e-10,cap=600):
    x=np.zeros_like(b);r=b.copy();norm=float(np.linalg.norm(b))
    if norm==0:return x,dict(ok=True,iterations=0,error=0.,reason='zero_rhs')
    z=r/diagonal;p=z.copy();rz=float(np.sum(r*z))
    reason='iteration_allowance';it=0
    for it in range(1,cap+1):
        if not np.all(np.isfinite(p)) or not math.isfinite(rz) or rz<=0:
            reason='nonfinite_direction_or_residual';break
        Ap=A(p);den=float(np.sum(p*Ap))
        if not math.isfinite(den) or den<=0:reason='positive_block_breakdown';break
        alpha=rz/den
        if not math.isfinite(alpha):reason='nonfinite_alpha';break
        x+=alpha*p;r-=alpha*Ap
        if not np.all(np.isfinite(x)):reason='nonfinite_state';break
        if float(np.linalg.norm(r))/norm<=tolerance:
            r=b-A(x)
            if float(np.linalg.norm(r))/norm<=tolerance:reason='true_residual';break
            z=r/diagonal;p=z.copy();rz=float(np.sum(r*z));continue
        z=r/diagonal;newrz=float(np.sum(r*z))
        if not math.isfinite(newrz) or newrz<=0:reason='positive_residual_breakdown';break
        beta=newrz/rz
        if not math.isfinite(beta):reason='nonfinite_beta';break
        p=z+beta*p;rz=newrz
    error=float(np.linalg.norm(b-A(x))/norm) if np.all(np.isfinite(x)) else None
    if error is not None and not math.isfinite(error):error=None;reason='nonfinite_true_residual'
    return x,dict(ok=error is not None and math.isfinite(error) and error<=tolerance,
                  iterations=it,error=error,reason=reason)

class Forms:
    def __init__(self,r,z,essential=True):
        self.r,self.z=r,z;self.quad=core.shape_quadrature(r,z)
        self.shape=(2,len(r),len(z));self.mask=np.ones(self.shape,bool)
        if essential:
            self.mask[:,-1,:]=False;self.mask[:,:,-1]=False
            self.mask[0,0,:]=False;self.mask[1,:,0]=False
        self.massdiag=np.zeros(self.shape);self.elldiag=np.zeros(self.shape)
        for rr,vol,shapes in self.quad:
            for n,nr,nz,i,j in shapes:
                sl=(slice(None),slice(i,len(r)-1+i),slice(j,len(z)-1+j))
                self.massdiag[sl]+=vol*n*n
                self.elldiag[sl]+=vol*(n*n+core.ELL**2*(nr*nr+nz*nz))
                self.elldiag[sl][0]+=vol*core.ELL**2*n*n/rr**2
        self.massdiag[~self.mask]=1;self.elldiag[~self.mask]=1
        assert np.all(self.massdiag>0) and np.all(self.elldiag>0)

    def apply(self,v,ell):
        assert np.all(v[~self.mask]==0) and np.all(np.isfinite(v))
        out=np.zeros_like(v)
        for rr,vol,shapes in self.quad:
            val,gr,gz=core.interpolate(v,shapes)
            value=val.copy();value[0]+=ell**2*val[0]/rr**2
            core.add(out,value,ell**2*gr,ell**2*gz,vol,shapes)
        out[~self.mask]=0;return out

    def coupling(self,p):
        out=np.zeros(self.shape);K=0.
        for rr,vol,shapes in self.quad:
            _,gr,gz=core.interpolate(p,shapes)
            values=np.stack([gr,gz]);zero=np.zeros_like(values)
            core.add(out,values,zero,zero,vol,shapes)
            K+=float(np.sum(vol*(gr*gr+gz*gz)))
        out[~self.mask]=0;return out,K

    def energy(self,p,v,ell):
        value=0.
        for rr,vol,shapes in self.quad:
            _,pgR,pgZ=core.interpolate(p,shapes)
            vv,gr,gz=core.interpolate(v,shapes)
            value+=float(np.sum(vol*((pgR-vv[0])**2+(pgZ-vv[1])**2+
                         ell**2*(np.sum(gr*gr+gz*gz,axis=0)+vv[0]**2/rr**2))))
        return value

    def error_bound(self,b,y,ell):
        residual=b-self.apply(y,ell)
        unresolved=float(np.sum(residual**2/self.massdiag))/((2-math.sqrt(3))/4)
        raw_uncertainty=abs(float(np.sum(y*residual)))+unresolved
        return unresolved,raw_uncertainty

def finite(value):return float(value) if math.isfinite(value) else None
def ratio(n,d,uncertainty=0.):
    if n is None or d is None:return None,'nonfinite_energy'
    if d<=uncertainty:return None,'denominator_not_resolved'
    value=finite(n/d)
    return value,None if value is not None else 'nonfinite_ratio'

def direction(r,z,name):
    R,Z=np.meshgrid(r,z,indexing='ij')
    if name.startswith('global_p'):
        power=int(name[-1]);p=(1-R**2/128**2)**power*np.cos(math.pi*Z/(2*128))**power
    else:
        p=np.zeros_like(R);inside=(R>8)&(R<48)&(Z>.1)&(Z<24)
        p[inside]=np.sin(math.pi*(R[inside]-8)/40)**4*np.sin(math.pi*(Z[inside]-.1)/23.9)**4
    p[-1,:]=0;p[:,-1]=0;p/=np.max(abs(p));return p

def main():
    auth();source=sha(__file__)
    assert not list(BASE.glob(STEM+'_*.json')) and not list(BASE.glob(STEM+'_*.npz')),'Existing diagnostic preserved'
    manifest=dict(owner='root',pid=os.getpid(),started=now(),source_sha256=source,
                  input_sha256=PINS,inherited_input_sha256=core.PINS,
                  physics_changes=[],galaxy_replay=False,no_automatic_resume=True,
                  refinements=[1,2],directions=['global_p2','global_p3','global_p4','interior'])
    publish(STEM+'_MANIFEST.json',manifest)
    mat=np.array([[4.,1.],[1.,3.]])
    sol,check=pcg(lambda v:mat@v,np.array([1.,2.]),np.diag(mat),1e-12,20)
    spd_error=finite(float(np.max(abs(sol-np.array([1/11,7/11])))))
    spd=dict(error=spd_error,linear=check,passed=check['ok'] and spd_error is not None and spd_error<=2e-12)
    control_record('KNOWN_SPD',spd,sol)
    if not spd['passed']:
        close(source,manifest,dict(status='IMPLEMENTATION_CONTROL_FAILED',known_spd=spd,cases=[]));return 3
    patch=Forms(np.array([2.,2.7,3.5]),np.array([1.,1.3,2.]),False)
    R,Z=np.meshgrid(patch.r,patch.z,indexing='ij');p=R+.37*Z
    load,K=patch.coupling(p);y,control=pcg(lambda v:patch.apply(v,0.),load,patch.massdiag,1e-12,600)
    exact=(1+.37**2)*(3.5**2-2**2)*(2.-1.)/2
    affine=dict(K=K,exact_K=exact,K_error=finite(abs(K-exact)/exact),
                projection_error=finite(abs(K-float(np.sum(load*y)))/exact),mass_solve=control)
    affine['passed']=control['ok'] and affine['K_error'] is not None and affine['projection_error'] is not None and affine['K_error']<=2e-12 and affine['projection_error']<=2e-12
    control_record('AFFINE_PATCH',affine,y)
    if not affine['passed']:
        close(source,manifest,dict(status='IMPLEMENTATION_CONTROL_FAILED',affine_patch=affine,known_spd=spd,cases=[]));return 3
    results=[];symmetry=[];rng=np.random.default_rng(202610061253)
    for ref in (1,2):
        r,z=core.edges(ref,128);forms=Forms(r,z)
        a=rng.normal(size=forms.shape);b=rng.normal(size=forms.shape)
        a[~forms.mask]=0;b[~forms.mask]=0
        for ell in (0.,core.ELL):
            Aa=forms.apply(a,ell);Ab=forms.apply(b,ell)
            err=abs(float(np.sum(a*Ab)-np.sum(b*Aa)))/max(1e-30,float(np.linalg.norm(a)*np.linalg.norm(Ab)),float(np.linalg.norm(b)*np.linalg.norm(Aa)))
            symmetry.append(dict(refinement=ref,ell=ell,error=err,passed=err<=2e-12))
        for name in manifest['directions']:
            p=direction(r,z,name);load,K=forms.coupling(p)
            y,mi=pcg(lambda v:forms.apply(v,0.),load,forms.massdiag)
            ye,ei=pcg(lambda v:forms.apply(v,core.ELL),load,forms.elldiag)
            partial={}
            if not mi['ok'] or not ei['ok']:
                file=f'{STEM}_R{ref}_{name}_PARTIAL.npz';path=BASE/file
                with path.open('xb') as f:
                    np.savez_compressed(f,mass_partial=y,ell_partial=ye,scalar_direction=p,r=r,z=z)
                    f.flush();os.fsync(f.fileno())
                path.chmod(0o444);partial=dict(partial_file=file,partial_sha256=sha(path))
            projected=finite(float(np.sum(load*y)));ell_projected=finite(float(np.sum(load*ye)))
            lock=None if projected is None else finite(K-projected)
            physical=None if projected is None or ell_projected is None else finite(projected-ell_projected)
            direct0=finite(forms.energy(p,y,0.)) if np.all(np.isfinite(y)) else None
            directe=finite(forms.energy(p,ye,core.ELL)) if np.all(np.isfinite(ye)) else None
            ub0,err0=forms.error_bound(load,y,0.) if np.all(np.isfinite(y)) else (None,None)
            ube,erre=forms.error_bound(load,ye,core.ELL) if np.all(np.isfinite(ye)) else (None,None)
            ub0=None if ub0 is None else finite(ub0);err0=None if err0 is None else finite(err0)
            ube=None if ube is None else finite(ube);erre=None if erre is None else finite(erre)
            phys_error=None if err0 is None or erre is None else finite(err0+erre)
            id0=None if direct0 is None or lock is None else finite(abs(direct0-lock)/K)
            ide=None if directe is None or lock is None or physical is None else finite(abs(directe-(lock+physical))/K)
            allowance=1e-8*K
            resolved_ratio,ratio_reason=ratio(lock,physical,math.inf if phys_error is None else phys_error+allowance)
            passed=mi['ok'] and ei['ok'] and lock is not None and physical is not None and id0 is not None and ide is not None and lock>=-1e-8*K and physical>=-1e-8*K and max(id0,ide)<=1e-8
            case=dict(refinement=ref,direction=name,nodes=[len(r),len(z)],K=K,
                      projected=projected,ell_projected=ell_projected,Q_lock=lock,Q_ell=physical,
                      locking_fraction=None if lock is None else lock/K,
                      physical_fraction=None if physical is None else physical/K,
                      locking_to_physical=resolved_ratio,ratio_reason=ratio_reason,
                      direct_energies=[direct0,directe],unresolved_minimum_energy_bounds=[ub0,ube],
                      locking_error_bound=err0,physical_error_bound=phys_error,numerical_allowance=allowance,
                      mass_solve=mi,ell_solve=ei,direct_identity_errors=[id0,ide],passed=passed,**partial)
            publish(f'{STEM}_R{ref}_{name}_CP.json',case);results.append(case)
            print('PROJECTION',ref,name,'LOCK',lock,'PHYSICAL',physical,'PASS',passed,flush=True)
    differences=[]
    for name in manifest['directions']:
        coarse=next(c for c in results if c['direction']==name and c['refinement']==1)
        fine=next(c for c in results if c['direction']==name and c['refinement']==2)
        lr,lwhy=ratio(fine['Q_lock'],coarse['Q_lock'],math.inf if coarse['locking_error_bound'] is None else coarse['locking_error_bound']+coarse['numerical_allowance'])
        er,ewhy=ratio(fine['Q_ell'],coarse['Q_ell'],math.inf if coarse['physical_error_bound'] is None else coarse['physical_error_bound']+coarse['numerical_allowance'])
        differences.append(dict(direction=name,fine_to_coarse_lock=lr,lock_ratio_reason=lwhy,
                                fine_to_coarse_ell=er,ell_ratio_reason=ewhy))
    passed=all(c['passed'] for c in results) and all(c['passed'] for c in symmetry)
    result=dict(status='DIAGNOSTIC_CLOSED' if passed else 'NUMERICAL_FAILURES_RETAINED',manifest=manifest,
                cases=results,refinement=differences,symmetry=symmetry,known_spd_error=spd_error,affine_patch=affine,
                observational_prediction=False,physical_failure_verdict=False,joint_superiority_qualified=False)
    close(source,manifest,result);return 0 if passed else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    raise SystemExit(main())
