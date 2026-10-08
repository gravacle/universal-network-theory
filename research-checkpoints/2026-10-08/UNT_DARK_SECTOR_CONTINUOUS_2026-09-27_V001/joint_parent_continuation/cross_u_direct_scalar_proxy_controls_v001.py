"""Guarded direct scalar-proxy assembly/factor controls; no nonlinear update."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib, json, math, os, time, traceback
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_DIRECT_SCALAR_PROXY_CONTROLS_V001'
AUTHOR_DRAFT=False
PINS={'CROSS_U_NGC3198_NONLINEAR_DISK_V001.md': 'a5e7f129c46af6aac63bbec179d98fe8ae9d3ac7178d0598bb23ba21eaf92b76', 'galaxy_density.py': '9819b9cb1f63baea07eb06a150dbda3113d7850d9ac24a13ee65e96f6f07bb6c', 'NGC3198_BARYON_INPUT.json': '8895693861ee0db1b42136c6aac7f0fb9fa9e0e84c72c69e8c8e3c89ba0e78d1', 'NGC3198_FIXED_DENSITY_PROTOCOL.md': '0dd06827f2b6cddb4f158f9c21eaccf70bf44597d0bd8891d39a96eb6380d10b', 'LINEAR_SOURCE_GALAXY_REFERENCE_V001.md': '399fa90b083afe9a014bc47e2e3d70c80f1c8ef5708edb205cb348b8d6f72801', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', '../ngc3198_sparc_excerpt_v001.txt': '58a303f78b8dd884aeb7be9a8d98514fa5e84665265e958f3b75479c19cfa900', 'cross_u_ngc3198_nonlinear_disk_v001.py': 'ae4285fc9c19cdf2d8efa176ac3d770b7eaf379a75fa3b9627bc9d3f6f3179e1', 'cross_u_nonzero_native_curvature_split_v001.py': 'a60415dd3983e91161b45428ce5c030ff27ec3b8dd03032aa9e42c9a30a2f028', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001.md': '3eb392f83607b7c6373c6d5cdae012fe7fba9984fd4ff37f74935bb1b2cebc0a', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RECEIPT.json': '1f1f1aa4c06cf74f54875aefed42dc347932debc4a321211a96a5b3623f7331a', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_RESULT.json': 'd20f71731fe822a5af9e7d78408a346b5414752d9378a2a062a1e4ae5f16b871', 'CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001_MANIFEST.json': '3654b4e41dc9658447ce2f2bcbec5572eda5b61a7adfe4e34ec2b497fe22c44d', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RECEIPT.json': 'eee323ea063832eac8f9d731823cf9fd3e5135930e74d9a477646d60b5300eb5', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json': '9da87a64f0e37c17530d34aae0f2ffb0efdf16d610763adcddff875c0a87ec8c', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_MANIFEST.json': 'b83b93c6c64e5a9f356e849e0688a5690073f4d07c756ee67fd1390c8671471c', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003.md': '91f8df979025c53ee96601839e1adad7eacb6436b7444ab2e488c53fc9a01dc8', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_CASE.json': 'aacab61f915a1bc4347377da1d5b5b7bdcd515ad519cd5b1661ce8c61c71d299', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz': '2dd4897d541dc74543bc7185894a0879d5a4ff99c090bf4bf4a369eb29cdef15', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz.commit.json': '5fe0d9fe062eecbcb65997965569ab58e4f56e6a742ec4df84728691bd571b2f', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_CASE.json': 'e9313e8356bb58177a6b891a028d0293b1feb0a81997f32e997623a5ad0ff7be', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz': 'c0b9f237e81f8d8d4d62fb2fa5901aae16711bfc31c0cc70979f687d01ff2aa4', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz.commit.json': '14e42f5dea351040f26cd0b14d237a56e1e21a167d4c8e80453fc222bceec5b4', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_CASE.json': '51c138f74b213b6fa455329c578d071eb99eeacd590efd81977ee8f1c715ffc8', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz': 'fe0b587bb8a979e260d991216451fb61adc19d3afba37ec6f100f17c0afab24d', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz.commit.json': '15da0758f2cebf87c684d225703c7327a3b9495751fd0445462b239f38aa215a', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_CASE.json': '6bcdc0ee7e02a3367473dd99185bfd9d1fe5e8f51683d329b4509e77d90fcd75', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_LINEAR_FAILED_001.npz': '1b5edc61af9007d840a77f614fe10a17e2fc4c4caf802313ccc84ab7ec6e5e6d', 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_LINEAR_FAILED_001.npz.commit.json': 'f708e09a4f08b8305e3917a453e41b7dcd78ed85de7a3d9d5071119c95ad533b'}
BINDINGS={'E1em05_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_CASE.json', 'case_sha256': 'aacab61f915a1bc4347377da1d5b5b7bdcd515ad519cd5b1661ce8c61c71d299', 'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz', 'sha256': '2dd4897d541dc74543bc7185894a0879d5a4ff99c090bf4bf4a369eb29cdef15', 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H20_LINEAR_FAILED_001.npz.commit.json', 'commit_sha256': '5fe0d9fe062eecbcb65997965569ab58e4f56e6a742ec4df84728691bd571b2f'}, 'E1em04_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_CASE.json', 'case_sha256': 'e9313e8356bb58177a6b891a028d0293b1feb0a81997f32e997623a5ad0ff7be', 'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz', 'sha256': 'c0b9f237e81f8d8d4d62fb2fa5901aae16711bfc31c0cc70979f687d01ff2aa4', 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em04_HI0_H20_LINEAR_FAILED_000.npz.commit.json', 'commit_sha256': '14e42f5dea351040f26cd0b14d237a56e1e21a167d4c8e80453fc222bceec5b4'}, 'E1em03_HI0_H20': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_CASE.json', 'case_sha256': '51c138f74b213b6fa455329c578d071eb99eeacd590efd81977ee8f1c715ffc8', 'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz', 'sha256': 'fe0b587bb8a979e260d991216451fb61adc19d3afba37ec6f100f17c0afab24d', 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em03_HI0_H20_LINEAR_FAILED_001.npz.commit.json', 'commit_sha256': '15da0758f2cebf87c684d225703c7327a3b9495751fd0445462b239f38aa215a'}, 'E1em05_HI0_H21': {'case_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_CASE.json', 'case_sha256': '6bcdc0ee7e02a3367473dd99185bfd9d1fe5e8f51683d329b4509e77d90fcd75', 'file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_LINEAR_FAILED_001.npz', 'sha256': '1b5edc61af9007d840a77f614fe10a17e2fc4c4caf802313ccc84ab7ec6e5e6d', 'commit_file': 'CROSS_U_NGC3198_MINRES_RECOVERY_V003_E1em05_HI0_H21_LINEAR_FAILED_001.npz.commit.json', 'commit_sha256': 'f708e09a4f08b8305e3917a453e41b7dcd78ed85de7a3d9d5071119c95ad533b'}}
PROTOCOL_SHA='480b5f201e67fcd8ccb973e48d0e43e8e95c5a856446ccef1867809b53121ce6'
FIELD_TOL=2e-11
SOLVE_TOL=1e-10
REFINEMENTS=3
CASE_CONTROL_NAMES=('bracket_identity','explicit_upper_identity','action_smooth','action_alternating',
                    'original_symmetry','B_adjoint','physical_block','upper_native_bound',
                    'proxy_positive','scaled_factor_action','known_true_residual','newton_rhs_true_residual')
PHYSICAL=dict(nonlinear_updated=False,force_qualified=False,refinement_qualified=False,
              physical_stability_qualified=False,joint_superiority_qualified=False)
CONTEXT={}
OWNER=None

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def encoded(obj):return (json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def write(name,data):
    p=BASE/name
    with p.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);assert p.read_bytes()==data;return sha(p)
def publish(name,obj):return write(name,encoded(obj))
def auth():
    assert not AUTHOR_DRAFT and len(PROTOCOL_SHA)==64
    for n,h in PINS.items():assert sha(BASE/n)==h,('input_changed',n)
    assert sha(BASE/(STEM+'.md'))==PROTOCOL_SHA

def parents():
    merged=dict(PINS);merged[STEM+'.md']=PROTOCOL_SHA
    for stem in ('CROSS_U_NGC3198_MINRES_RECOVERY_V003','CROSS_U_NONZERO_NATIVE_CURVATURE_SPLIT_V001'):
        receipt=json.loads((BASE/(stem+'_RECEIPT.json')).read_text())
        assert receipt['owner']=='root' and receipt['pid']>0 and receipt['closed']>receipt['started']
        assert sha(BASE/(stem+'_RESULT.json'))==receipt['result_sha256']
        for n,h in receipt['output_sha256'].items():assert sha(BASE/n)==h,('parent_output',n)
        manifest=json.loads((BASE/(stem+'_MANIFEST.json')).read_text())
        assert receipt['source_sha256']==manifest['source_sha256']
        for key in ('input_sha256','inherited_input_sha256'):
            for n,h in manifest[key].items():
                assert sha(BASE/n)==h and (n not in merged or merged[n]==h),('parent_input',n)
                merged[n]=h
    return merged

def finite(v):return float(v) if math.isfinite(float(v)) else None
def norm(x):return float(np.linalg.norm(x))
def dot(a,b):return float(np.sum(a*b))
def error(a,b,den):return norm(a-b)/den if den>0 and math.isfinite(den) else math.inf
def control(name,value,tol=FIELD_TOL,extra=True):
    return dict(name=name,error=finite(value),tolerance=tol,passed=math.isfinite(value) and value<=tol and bool(extra))

def checkpoint(case,stage,arrays,metadata,owner):
    name=f'{STEM}_{case}_{stage}.npz';p=BASE/name
    schema={k:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for k,v in arrays.items()}
    meta=dict(metadata,owner=owner,stage=stage,schema=schema);text=encoded(meta).decode();meta=json.loads(text)
    with p.open('xb') as f:np.savez_compressed(f,metadata=text,**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);record=dict(file=name,sha256=sha(p),metadata=meta)
    record['commit_sha256']=publish(name+'.COMMIT.json',record)
    return record

class Proxy:
    def __init__(self,model,x,fixed):
        self.model=model;self.forms=native.NativeForms(x,model.r,model.z)
        self.mask=model.mask[0];self.w=self.forms.w;self.sw=np.sqrt(self.w);self.shape=self.forms.shape
        assert np.array_equal(self.forms.mask,model.mask[[1,2]])
        nr,nz=len(model.r),len(model.z);self.m=np.zeros((nr,nz));self.pdiag=np.zeros_like(self.m);self.kpsi=np.zeros_like(self.m)
        self.a=np.zeros((32,nr,nz));self.c=np.zeros_like(self.a);self.b=np.zeros_like(self.a)
        self.ea=np.zeros_like(self.a);self.ec=np.zeros_like(self.a);self.eb=np.zeros_like(self.a)
        self.kdiag=np.zeros((2,nr,nz));self.pressure=[]
        for rr,vol,shapes,vv,alpha,nn,t in self.forms.quad:
            val,_,_=core.interpolate(x[0],shapes);coefficient=-native.pressure_coefficient(val,model.ep,fixed)
            assert np.all(np.isfinite(coefficient)) and np.all(coefficient>0)
            self.pressure.append(coefficient)
            for n,dr,dz,i,j in shapes:
                sl=(slice(None),slice(i,nr-1+i),slice(j,nz-1+j));ss=sl[1:]
                self.m[ss]+=vol*n
                self.a[sl]+=vol*n*(t+2*alpha*vv[:,0]**2);self.c[sl]+=vol*n*(t+2*alpha*vv[:,1]**2)
                self.b[sl]+=vol*n*(2*alpha*vv[:,0]*vv[:,1])
                self.ea[sl]+=vol*n*(alpha*nn+2*alpha*vv[:,0]**2)
                self.ec[sl]+=vol*n*(alpha*nn+2*alpha*vv[:,1]**2)
                self.eb[sl]+=vol*n*(2*alpha*vv[:,0]*vv[:,1])
                self.kdiag[(0,)+ss]+=vol*(dr*dr+dz*dz+n*n/rr**2);self.kdiag[(1,)+ss]+=vol*(dr*dr+dz*dz)
                self.kpsi[ss]+=vol*(dr*dr+dz*dz);self.pdiag[ss]+=vol*coefficient*n*n
        self.a+=4*core.ELL**2*self.kdiag[0];self.c+=4*core.ELL**2*self.kdiag[1]
        self.ea+=4*core.ELL**2*self.kdiag[0];self.ec+=4*core.ELL**2*self.kdiag[1]
        assert np.all(np.isfinite(self.m)) and np.all(self.m>0)
        both=self.forms.mask[0]&self.forms.mask[1];oa=self.forms.mask[0]&~self.forms.mask[1];oc=self.forms.mask[1]&~self.forms.mask[0]
        self.ia=np.zeros_like(self.a);self.ic=np.zeros_like(self.c);self.ib=np.zeros_like(self.b)
        scale=np.maximum(self.a[:,both],self.c[:,both]);aa=self.a[:,both]/scale;cc=self.c[:,both]/scale;bb=self.b[:,both]/scale
        det=aa*cc-bb*bb;assert np.all(scale>0) and np.all(det>0)
        self.ia[:,both]=cc/(scale*det);self.ic[:,both]=aa/(scale*det);self.ib[:,both]=-bb/(scale*det)
        self.ia[:,oa]=1/self.a[:,oa];self.ic[:,oc]=1/self.c[:,oc]
        assert all(np.all(np.isfinite(v)) for v in (self.ia,self.ic,self.ib,self.ea,self.ec,self.eb))
        self.weight=float(np.sum(self.w));self.remainder=abs(1-self.weight)
    def B(self,p):
        out=np.zeros(self.shape)
        for rr,vol,shapes,*_ in self.forms.quad:
            _,gr,gz=core.interpolate(p,shapes);v=self.sw[:,None,None,None]*np.stack([gr,gz])[None]
            core.add(out,v,np.zeros_like(v),np.zeros_like(v),vol,shapes)
        out[:,~self.forms.mask]=0;return out
    def BT(self,v):
        out=np.zeros_like(self.m)
        for rr,vol,shapes,*_ in self.forms.quad:
            val,_,_=core.interpolate(v,shapes);gr=np.sum(self.sw[:,None,None]*val[:,0],axis=0);gz=np.sum(self.sw[:,None,None]*val[:,1],axis=0)
            core.add(out,np.zeros_like(gr),gr,gz,vol,shapes)
        out[~self.mask]=0;return out
    def K(self,p):
        out=np.zeros_like(p)
        for rr,vol,shapes,*_ in self.forms.quad:
            _,gr,gz=core.interpolate(p,shapes);core.add(out,np.zeros_like(p[:-1,:-1]),gr,gz,vol,shapes)
        out[~self.mask]=0;return out
    def mass(self,p):
        out=np.zeros_like(p)
        for (_,vol,shapes,*_),co in zip(self.forms.quad,self.pressure):
            val,_,_=core.interpolate(p,shapes);core.add(out,co*val,np.zeros_like(val),np.zeros_like(val),vol,shapes)
        out[~self.mask]=0;return out
    def inverse(self,v):
        out=np.zeros_like(v);out[:,0]=self.ia*v[:,0]+self.ib*v[:,1];out[:,1]=self.ib*v[:,0]+self.ic*v[:,1]
        out[:,~self.forms.mask]=0;return out
    def upper(self,v):
        out=np.zeros_like(v);out[:,0]=self.a*v[:,0]+self.b*v[:,1];out[:,1]=self.b*v[:,0]+self.c*v[:,1]
        out[:,~self.forms.mask]=0;return out
    def P(self,p):return (self.weight+self.remainder)*self.K(p)-self.BT(self.inverse(self.B(p)))+self.mass(p)
    def bracket(self):
        m=self.m[None];ta=np.broadcast_to(1/m,self.a.shape).copy();tc=ta.copy();tb=np.zeros_like(ta)
        both=self.forms.mask[0]&self.forms.mask[1];oa=self.forms.mask[0]&~self.forms.mask[1];oc=self.forms.mask[1]&~self.forms.mask[0]
        ea,ec,eb=self.ea[:,both],self.ec[:,both],self.eb[:,both];mm=np.broadcast_to(m,self.a.shape)[:,both]
        scale=np.maximum(mm,np.maximum(ea,ec));aa,cc,bb,mu=ea/scale,ec/scale,eb/scale,mm/scale
        de=aa*cc-bb*bb;dd=mu*mu+mu*(aa+cc)+de
        assert np.all(de>=0) and np.all(dd>0) and np.all(np.isfinite(dd))
        ta[:,both]=(mu*aa+de)/(mm*dd);tc[:,both]=(mu*cc+de)/(mm*dd);tb[:,both]=mu*bb/(mm*dd)
        ta[:,oa]=self.ea[:,oa]/(self.m[oa][None]*(self.m[oa][None]+self.ea[:,oa]))
        tc[:,oc]=self.ec[:,oc]/(self.m[oc][None]*(self.m[oc][None]+self.ec[:,oc]))
        assert all(np.all(np.isfinite(v)) for v in (ta,tc,tb))
        wa=self.w[:,None,None];return ta,tc,tb,np.stack([np.sum(wa*ta,axis=0),np.sum(wa*tc,axis=0),np.sum(wa*tb,axis=0)])

def band_action(a,x):
    out=a[0]*x
    for d in range(1,len(a)):
        v=a[d,:len(x)-d];out[d:]+=v*x[:-d];out[:-d]+=v*x[d:]
    return out

def assembly(proxy,arrays):
    nr,nz=proxy.mask.shape;free=np.flatnonzero(proxy.mask.ravel());index=np.full(nr*nz,-1,dtype=np.int64);index[free]=np.arange(len(free))
    bandwidth=2*(nz-1)+2;band=np.zeros((bandwidth+1,len(free)));arrays.update(raw_band=band,free_full_indices=free,scalar_mask=proxy.mask,mass_lump=proxy.m)
    ci=np.full((nr*nz,9),-1,dtype=np.int64);cv=np.zeros((nr*nz,2,9));events=[[] for _ in range(nr*nz)]
    def add(ids,local):
        ids=np.asarray(ids);good=ids>=0;ii=ids[good];a=local[np.ix_(good,good)]
        for row in range(len(ii)):
            for col in range(row+1):
                hi,lo=max(ii[row],ii[col]),min(ii[row],ii[col]);assert hi-lo<=bandwidth
                band[hi-lo,lo]+=a[row,col]
    for q,(_,vol,shapes,*_) in enumerate(proxy.forms.quad):
        co=proxy.pressure[q]
        for i in range(nr-1):
            for k in range(nz-1):
                nodes=np.array([(i+di)*nz+k+dj for _,_,_,di,dj in shapes]);ids=index[nodes]
                nv=np.array([n for n,*_ in shapes]);gr=np.array([dr[i,0] for _,dr,_,_,_ in shapes]);gz=np.array([dz[0,k] for _,_,dz,_,_ in shapes]);v=float(vol[i,k])
                add(ids,v*(proxy.remainder*(np.outer(gr,gr)+np.outer(gz,gz))+co[i,k]*np.outer(nv,nv)))
                for a,node in enumerate(nodes):
                    weight=v*nv[a];events[node].append((weight,ids.copy(),gr.copy(),gz.copy()))
                    ni,nk=divmod(int(node),nz)
                    for b,other in enumerate(nodes):
                        oi,ok=divmod(int(other),nz);slot=(oi-ni+1)*3+ok-nk+1
                        ci[node,slot]=ids[b];cv[node,0,slot]+=weight*gr[b];cv[node,1,slot]+=weight*gz[b]
    ta,tc,tb,weighted=proxy.bracket();arrays.update(bracket_a=ta,bracket_c=tc,bracket_b=tb,weighted_bracket=weighted,stencil_indices=ci,stencil_coefficients=cv,E_a=proxy.ea,E_c=proxy.ec,E_b=proxy.eb)
    for node in range(nr*nz):
        CONTEXT.update(stage='covariance_assembly',node=node)
        ids=ci[node];c=cv[node];m=proxy.m.ravel()[node];cov=np.zeros((9,9));positions={int(v):i for i,v in enumerate(ids) if v>=0}
        for weight,eids,gr,gz in events[node]:
            dr=-c[0]/m;dz=-c[1]/m
            for v,r,z in zip(eids,gr,gz):
                if v>=0:dr[positions[int(v)]]+=r;dz[positions[int(v)]]+=z
            cov+=weight*(np.outer(dr,dr)+np.outer(dz,dz))
        a,b,cross=weighted[:,node//nz,node%nz]
        add(ids,proxy.weight*cov+a*np.outer(c[0],c[0])+b*np.outer(c[1],c[1])+cross*(np.outer(c[0],c[1])+np.outer(c[1],c[0])))
    assert np.all(np.isfinite(band))
    return band,free

def factor_band(a,arrays):
    CONTEXT.update(stage='factor_diagonal_check')
    diag=a[0];bad=~np.isfinite(diag)|(diag<=0)
    if np.any(bad):
        j=int(np.flatnonzero(bad)[0]);arrays['factor']=a.copy()
        CONTEXT.update(column=j,pivot=finite(diag[j]))
        return None,dict(status='DIAGONAL_REFUSAL',column=j,pivot=finite(diag[j]),completed=0,history=[])
    scale=1/np.sqrt(diag);assert np.all(np.isfinite(scale))
    f=a.copy();n=a.shape[1];b=a.shape[0]-1
    for d in range(b+1):f[d,:n-d]*=scale[d:]*scale[:n-d]
    arrays.update(congruence_scale=scale,scaled_band=f.copy(),factor=f)
    rr,ss=np.tril_indices(b);rr+=1;ss+=1
    history=[]
    for j in range(n):
        CONTEXT.update(stage='band_factor',column=j,pivot=finite(f[0,j]))
        pivot=float(f[0,j])
        if not math.isfinite(pivot) or pivot<=0:return None,dict(status='PIVOT_REFUSAL',column=j,pivot=finite(pivot),completed=j,history=history)
        ll=math.sqrt(pivot);f[0,j]=ll;k=min(b,n-1-j);v=f[1:k+1,j]/ll
        if not np.all(np.isfinite(v)):return None,dict(status='NONFINITE_COLUMN',column=j,completed=j,history=history)
        f[1:k+1,j]=v;take=rr<=k;r,s=rr[take],ss[take]
        f[r-s,j+s]-=v[r-1]*v[s-1]
        if j%128==0 or j==n-1:history.append(dict(column=j,pivot=pivot))
    return (f,scale),dict(status='FACTORED',completed=n,history=history)

def solve_factor(f,scale,b):
    n=len(b);width=len(f)-1;y=scale*b.copy()
    for j in range(n):
        y[j]/=f[0,j];k=min(width,n-1-j);y[j+1:j+k+1]-=f[1:k+1,j]*y[j]
    for j in range(n-1,-1,-1):
        k=min(width,n-1-j);y[j]=(y[j]-dot(f[1:k+1,j],y[j+1:j+k+1]))/f[0,j]
    return scale*y

def factor_action(f,x):
    n=len(x);b=len(f)-1;y=f[0]*x
    for d in range(1,b+1):y[:-d]+=f[d,:n-d]*x[d:]
    out=f[0]*y
    for d in range(1,b+1):out[d:]+=f[d,:n-d]*y[:-d]
    return out

def refined_solve(proxy,f,scale,free,rhs,arrays,key):
    den=norm(rhs);assert math.isfinite(den) and np.all(np.isfinite(rhs))
    arrays[key+'_rhs']=rhs
    if den==0:
        assert np.all(rhs==0),'Nonzero RHS norm underflow refuses'
        arrays[key+'_solution']=np.zeros_like(rhs);arrays[key+'_original_action']=np.zeros_like(rhs)
        return 0.,[dict(iteration=0,error=0.,reason='exact_zero_rhs')]
    def embed(y):
        p=np.zeros(proxy.mask.shape);p.ravel()[free]=y;return p
    solution=solve_factor(f,scale,rhs);history=[]
    for it in range(REFINEMENTS+1):
        arrays[key+'_solution']=solution
        CONTEXT.update(stage='original_action_refinement',right_side=key,iteration=it)
        original=proxy.P(embed(solution)).ravel()[free];residual=rhs-original;e=norm(residual)/den
        arrays[key+'_original_action']=original
        history.append(dict(iteration=it,error=finite(e)))
        if not math.isfinite(e) or e<=SOLVE_TOL or it==REFINEMENTS:break
        solution+=solve_factor(f,scale,residual)
    arrays[key+'_rhs']=rhs;arrays[key+'_solution']=solution;arrays[key+'_original_action']=original
    return e,history

def case_run(name,binding,fixed,owner):
    parent=json.loads((BASE/binding['case_file']).read_text());old=parent['identity'];commit=json.loads((BASE/binding['commit_file']).read_text())
    assert commit['file']==binding['file'] and commit['sha256']==binding['sha256'] and commit['identity']==old
    with np.load(BASE/binding['file'],allow_pickle=False) as n:
        x=n['state'].copy();identity=json.loads(str(n['identity']));history=json.loads(str(n['history']))
        partial=n['unaccepted_linear_partial'].copy() if 'unaccepted_linear_partial' in n else None
    assert identity==old and parent['history'][:len(history)]==history and len(x.shape)==3 and x.shape==tuple(old['grid_shape'])
    assert np.all(np.isfinite(x)) and len(old['r_kpc'])==87 and len(old['z_kpc'])==45
    model=core.Model(np.array(old['r_kpc']),np.array(old['z_kpc']),32,old['eps'],fixed,core.density.profiles(old['hi_tail'],old['h2_tail']))
    assert np.all(x[~model.mask]==0);residual,pre,H=model.residual(x);root=np.sqrt(pre)
    proxy=Proxy(model,x,fixed);ir,iz=np.indices(proxy.mask.shape)
    p=np.sin(.17*(ir+1))*np.cos(.11*(iz+1));q=(-1.)**(ir+iz)*np.sin(.07*(ir+iz+1));p[~proxy.mask]=0;q[~proxy.mask]=0
    arrays=dict(state=x,full_mask=model.mask,scalar_residual=residual[0],whitening_root=root)
    if partial is not None:arrays['unaccepted_parent_whitened_partial']=partial
    checks=[];records=[];metadata=dict(case=name,identity=old,parent_binding=binding,parent_case=parent,parent_checkpoint_history=history,qualification=PHYSICAL)
    try:
        band,free=assembly(proxy,arrays);arrays.update(direction_p=p,direction_q=q)
        ta,tc,tb=arrays['bracket_a'],arrays['bracket_c'],arrays['bracket_b'];m=proxy.m[None]
        den=norm(np.broadcast_to(1/m,ta.shape));value=math.sqrt(norm(ta-(1/m-proxy.ia))**2+norm(tc-(1/m-proxy.ic))**2+2*norm(tb+proxy.ib)**2)/den
        checks.append(control('bracket_identity',value));checks.append(control('explicit_upper_identity',math.sqrt(norm(proxy.a-(m+proxy.ea))**2+norm(proxy.c-(m+proxy.ec))**2+2*norm(proxy.b-proxy.eb)**2)/math.sqrt(norm(proxy.a)**2+norm(proxy.c)**2+2*norm(proxy.b)**2)))
        action_descriptive={}
        for tag,direction in [('smooth',p),('alternating',q)]:
            original=proxy.P(direction);aa=band_action(band,direction.ravel()[free]);env=(proxy.weight+proxy.remainder)*norm(proxy.K(direction))+norm(proxy.BT(proxy.inverse(proxy.B(direction))))+norm(proxy.mass(direction))
            checks.append(control('action_'+tag,error(aa,original.ravel()[free],env)));arrays['original_action_'+tag]=original;arrays['band_action_'+tag]=aa
            action_descriptive[tag]=dict(uncanceled_envelope=finite(env),original_action_norm=finite(norm(original)),
                        relative_to_original_action=finite(error(aa,original.ravel()[free],norm(original))))
        metadata['assembly_action_descriptive']=action_descriptive
        pp,qq=proxy.P(p),proxy.P(q);symenv=float(np.sum(np.abs(p*qq))+np.sum(np.abs(q*pp)));checks.append(control('original_symmetry',abs(dot(p,qq)-dot(q,pp))/max(symenv,1e-30),extra=math.isfinite(symenv)))
        vv=np.empty(proxy.shape);vv[:,0]=.01*np.sin(.13*(ir+1));vv[:,1]=.01*np.cos(.19*(iz+1));vv[:,~proxy.forms.mask]=0
        bp=proxy.B(p);bt=proxy.BT(vv);adjenv=float(np.sum(np.abs(bp*vv))+np.sum(np.abs(p*bt)));checks.append(control('B_adjoint',abs(dot(bp,vv)-dot(p,bt))/max(adjenv,1e-30),extra=math.isfinite(adjenv)))
        metadata['bilinear_envelopes']=dict(symmetry=finite(symenv),B_adjoint=finite(adjenv),denominator_floor=1e-30)
        physical=np.zeros(model.shape);physical[0]=p;physical[1::2]=vv[:,0];physical[2::2]=vv[:,1]
        direct=np.zeros_like(physical);direct[0]=proxy.K(p)-proxy.mass(p)-proxy.BT(vv);dv=proxy.forms.apply(vv,core.ELL)-bp;direct[1::2]=dv[:,0];direct[2::2]=dv[:,1]
        actual=H(physical);checks.append(control('physical_block',error(direct,actual,max(norm(direct),norm(actual),1e-30))))
        upper=dot(vv,proxy.upper(vv));native_energy=dot(vv,proxy.forms.apply(vv,core.ELL));checks.append(control('upper_native_bound',max(0.,native_energy-upper)/max(abs(upper)+abs(native_energy),1e-30),extra=math.isfinite(upper) and math.isfinite(native_energy)))
        energy=dot(p,pp);checks.append(control('proxy_positive',max(0.,-energy)/max(abs(energy),1e-30),extra=math.isfinite(energy) and energy>0))
        arrays.update(field_test_vector=physical,physical_action=actual,independent_physical_action=direct,original_diagonal=proxy.kpsi+proxy.pdiag)
        records.append(checkpoint(name,'ASSEMBLY',arrays,dict(metadata,controls=checks),owner))
        if not all(c['passed'] for c in checks):raise ValueError('ASSEMBLY_CONTROL_FAILED')
        fact,info=factor_band(band,arrays);metadata['factor']=info
        if fact is None:raise ValueError('STRICT_FACTOR_REFUSAL:'+info['status'])
        f,scale=fact;y=p.ravel()[free]/scale
        checks.append(control('scaled_factor_action',error(factor_action(f,y),band_action(arrays['scaled_band'],y),norm(band_action(arrays['scaled_band'],y)))))
        if not checks[-1]['passed']:raise ValueError('SCALED_FACTOR_ACTION_FAILED')
        known=proxy.P(p).ravel()[free];e,kh=refined_solve(proxy,f,scale,free,known,arrays,'known');checks.append(control('known_true_residual',e,SOLVE_TOL))
        rhs=-residual[0].ravel()[free];e,rh=refined_solve(proxy,f,scale,free,rhs,arrays,'newton');checks.append(control('newton_rhs_true_residual',e,SOLVE_TOL))
        descriptive=dict(known_solution_relative=finite(norm(arrays['known_solution']-p.ravel()[free])/norm(p.ravel()[free])),scalar_rhs_only=True,no_native_inner_solve=True)
        status='CONTROL_PASS' if all(c['passed'] for c in checks) else 'CONTROL_FAILURE';metadata.update(factor=info,solve_history=dict(known=kh,newton=rh),descriptive=descriptive)
    except Exception:
        status='CONTROL_FAILURE';metadata.update(failure_context=dict(CONTEXT),traceback=traceback.format_exc())
        for key in CASE_CONTROL_NAMES:
            if key not in {c['name'] for c in checks}:checks.append(dict(name=key,error=None,tolerance=SOLVE_TOL if key.endswith('true_residual') else FIELD_TOL,passed=False,reason='not_completed_after_preserved_refusal'))
    assert {c['name'] for c in checks}==set(CASE_CONTROL_NAMES) and len(checks)==12
    records.append(checkpoint(name,'FINAL',arrays,dict(metadata,controls=checks,status=status),owner))
    result=dict(case=name,status=status,controls=checks,checkpoints=records,metadata=metadata,parent_case=parent,qualification=PHYSICAL)
    publish(f'{STEM}_{name}_CASE.json',result);return result

def implementation(owner):
    n=7;a=np.zeros((3,n));a[0]=3.;a[1,:-1]=-.5;a[2,:-2]=.1;arrays=dict(raw_band=a.copy());checks=[];meta={}
    try:
        fact,info=factor_band(a,arrays);meta['factor']=info
        if fact is None:raise ValueError('KNOWN_SPD_REFUSED')
        seed=np.arange(n,dtype=float)-2.;rhs=band_action(a,seed);f,scale=fact;answer=solve_factor(f,scale,rhs)
        checks=[control('known_banded_SPD',error(band_action(a,answer),rhs,norm(rhs)),SOLVE_TOL),control('zero_rhs',norm(solve_factor(f,scale,np.zeros(n))),SOLVE_TOL)]
        bad=a.copy();bad[0,0]=-1.;ba=dict(raw_band=bad.copy())
        refused_factor,refusal=factor_band(bad,ba);refused=refused_factor is None and refusal['status']=='DIAGONAL_REFUSAL'
        checks.append(control('nonpositive_diagonal_refusal',0. if refused else 1.));arrays.update(seed=seed,rhs=rhs,solution=answer,bad_band=bad,bad_factor=ba['factor']);meta['negative_diagonal_refusal']=refusal
    except Exception:
        meta.update(context=dict(CONTEXT),traceback=traceback.format_exc())
        for key in ('known_banded_SPD','zero_rhs','nonpositive_diagonal_refusal'):
            if key not in {c['name'] for c in checks}:checks.append(dict(name=key,error=None,tolerance=SOLVE_TOL,passed=False,reason='implementation_refusal'))
    record=checkpoint('IMPLEMENTATION','FINAL',arrays,dict(meta,controls=checks,qualification=PHYSICAL),owner)
    return checks,record

def main():
    global np,core,native,OWNER
    auth();source=sha(__file__);pins=parents();pins[Path(__file__).name]=source
    assert not [p for p in BASE.glob(STEM+'_*') if p.is_file()],'Existing outputs preserved'
    parent=json.loads((BASE/'CROSS_U_NGC3198_MINRES_RECOVERY_V003_RESULT.json').read_text());original=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_RESULT.json').read_text());fixed=original['manifest']['fixed']
    assert len(parent['cases'])==16 and len({c['identity']['case'] for c in parent['cases']})==16
    owner=dict(pid=os.getpid(),started_utc=now(),source_sha256=source);OWNER=owner;start=time.monotonic()
    np=importlib.import_module('numpy');core=importlib.import_module('cross_u_ngc3198_nonlinear_disk_v001');native=importlib.import_module('cross_u_nonzero_native_curvature_split_v001');native.np=np;native.core=core
    auth();manifest=dict(owner=owner,pins=pins,bindings=BINDINGS,physics_changes=[],qualification=PHYSICAL,parent_cases_preserved=parent['cases'],parent_controls_preserved=parent['controls'],limits=dict(field_tolerance=FIELD_TOL,solve_tolerance=SOLVE_TOL,refinements=REFINEMENTS))
    publish(STEM+'_MANIFEST.json',manifest);checks,implementation_cp=implementation(owner);cases=[]
    if all(c['passed'] for c in checks):
        for name,binding in BINDINGS.items():
            CONTEXT.clear();CONTEXT.update(case=name,stage='starting');cases.append(case_run(name,binding,fixed,owner));auth();parents()
    status='CONTROL_PASS' if len(cases)==4 and all(c['passed'] for c in checks) and all(c['status']=='CONTROL_PASS' for c in cases) else 'CONTROL_FAILURE'
    result=dict(status=status,implementation_controls=checks,implementation_checkpoint=implementation_cp,cases=cases,planned_predicates=51,completed_predicates=len(checks)+sum(len(c['controls']) for c in cases),qualification=PHYSICAL,manifest=manifest)
    auth();assert sha(__file__)==source;parents()
    outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}
    records=[implementation_cp]
    for case in cases:
        assert json.loads((BASE/f'{STEM}_{case["case"]}_CASE.json').read_text())==case
        records+=case['checkpoints']
    for record in records:
        assert sha(BASE/record['file'])==record['sha256'];commit=json.loads((BASE/(record['file']+'.COMMIT.json')).read_text());assert dict(commit,commit_sha256=sha(BASE/(record['file']+'.COMMIT.json')))==record
        with np.load(BASE/record['file'],allow_pickle=False) as saved:
            assert json.loads(str(saved['metadata']))==record['metadata']
            assert set(saved.files)==set(record['metadata']['schema'])|{'metadata'}
            for key,schema in record['metadata']['schema'].items():
                v=saved[key];assert schema==dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v))))
    rh=publish(STEM+'_RESULT.json',result);outputs[STEM+'_RESULT.json']=rh
    outputs[STEM+'_REPORT.md']=write(STEM+'_REPORT.md',(f'# Direct scalar proxy controls V001\n\nStatus {status}; {result["completed_predicates"]} / 51 planned numerical predicates. Four fixed parent fields; no nonlinear update, force adoption or change to physical pressure.\n').encode())
    publish(STEM+'_RECEIPT.json',dict(status='CLOSED',owner=owner,finished_utc=now(),elapsed_seconds=time.monotonic()-start,pins=pins,output_sha256=outputs,qualification=PHYSICAL))
    auth();parents();print(status,flush=True);return 0 if status=='CONTROL_PASS' else 3

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');assert ap.parse_args().root_owned
    try:code=main()
    except Exception:
        if OWNER is not None:
            publish(STEM+'_ERROR.json',dict(status='FAILED',owner=OWNER,failed_utc=now(),context=CONTEXT,
                    traceback=traceback.format_exc(),qualification=PHYSICAL,
                    preserved_outputs={p.name:sha(p) for p in BASE.glob(STEM+'_*') if p.is_file()}))
        raise
    raise SystemExit(code)
