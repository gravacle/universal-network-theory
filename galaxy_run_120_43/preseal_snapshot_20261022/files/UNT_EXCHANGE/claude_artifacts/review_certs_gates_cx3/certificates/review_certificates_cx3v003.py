"""Independent numerical review of certificate bytes. No certificate/checker imports.
Only production symbol/roster/special-function definitions are shared; search,
integration, represented-source replica and GQ assembly are implemented here.
All writes exclusive and confined to this directory. Synthetic/saved replay only.
"""
import sys, os, json, math, hashlib, importlib.util, itertools, time, resource
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import numpy as np

OUT = Path(__file__).resolve().parent
ART = Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UPC = Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
CERT = ART/'tail_scheme_impl_c2/certificates_v002'
READS = set()
def audit(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes)):
        p = Path(os.fsdecode(args[0])); s = str(p.resolve())
        if '/runs_ext/UVT_' in s or '/KMAX_A2F10_C5H_RUN_V001' in s:
            raise RuntimeError('FORBIDDEN_RUN_READ '+s)
        u = s.upper()
        if 'NGC3198' in u and ('OBSERVED' in u or 'TARGET' in u) and 'TARGET_FREE' not in u:
            raise RuntimeError('FORBIDDEN_NGC_TARGET '+s)
        mode, flags = args[1], args[2]
        writing = (isinstance(mode,str) and any(c in mode for c in 'wax+')) or bool(flags & (os.O_WRONLY|os.O_RDWR))
        if writing:
            if OUT != Path(s).parent or not flags & os.O_EXCL:
                raise RuntimeError('WRITE_MUST_BE_NEW_REVIEW_FILE '+s)
        elif '/Research/' in str(p) or '/Research/' in s or '/UNT_' in s:
            READS.add(str(p.absolute()))
    if event in ('subprocess.Popen','os.system','socket.connect','os.remove','os.rename','os.rmdir'):
        raise RuntimeError('FORBIDDEN_OPERATION '+event)
sys.addaudithook(audit)

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()
def read(p): return json.loads(Path(p).read_text())
def load(p, want=None):
    p=Path(p); got=sha(p)
    if want is not None and got != want: raise ValueError('PIN '+str(p))
    name='cx3cert_'+p.stem
    m=type(sys)(name); m.__file__=str(p); sys.modules[name]=m
    exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
    return m
def write(name, obj):
    obj['tested']='TESTED'; obj['utc']=datetime.now(timezone.utc).isoformat()
    obj['date_u_captured_before_review']='Sun Oct 18 12:53:54 UTC 2026'
    obj['source']={'path':__file__,'sha256':sha(__file__)}
    paths=sorted(READS)
    obj['read_dependencies']=[{'path':p,'sha256':sha(p)} for p in paths if Path(p).is_file()]
    obj['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    with open(OUT/name,'x') as f: json.dump(obj,f,indent=2,allow_nan=False); f.write('\n')
    print(name,sha(OUT/name),flush=True)

class Context:
    def __init__(self):
        run=UPC/'CLAUDE2/runs/KMAX_A2F10_C4R3_D7R3_RUN_V001'
        self.res=read(run/'result.json')
        assert sha(run/'result.json')=='aac01962dc7bf08a7486179bc5674af520f7ea38d73b004154cdd2ff25fa8dee'
        self.ni=read(run/'inputs/seed_c2v001.json')['numerical_inputs']
        ident=read(Path(self.res['identity']['route_a']['checkpoint'])/'IDENTITY.json')['identity']
        self.mods=ident['code']['modules']
        for key in ('cardinal','complex_binding','static_binding'):
            pin=self.mods['fourier_arguments.'+key+'_module']; setattr(self,key,load(pin['path'],pin['sha256']))
        p=UPC/'CLAUDE2/CRITICAL_PATH_EVALUATION_2026-10-17_V001/sampler_eval/CANDIDATE_4CHAIN_POOLED_GRID_V001.npz'
        assert sha(p)=='2e3a36d888ef8a89c9a2b6073ca6123656c31317c995962c11f34d434eca6ff7'
        with np.load(p,allow_pickle=False) as z:
            self.grid=z['source_hessian_grid'].copy();self.cb=z['background_C'].copy();self.mu=z['background_mu'].copy()
        e,v=np.linalg.eigh(self.cb);self.root=(v*np.sqrt(e))@v.T;self.isq=(v/np.sqrt(e))@v.T
        self.kpc=self.ni['kpc_m'];self.gamma=self.ni['gamma'];self.cache={}
    def response(self,n,k,t):
        n=np.asarray(n); n=n/np.linalg.norm(n); kv=n*k/self.kpc; ni=self.ni
        key=tuple(np.remainder(t,2*np.pi))
        if key not in self.cache:
            w=self.cardinal.cardinal_weights(L=len(self.grid),k_primitive=np.asarray(t))['weights']
            self.cache[key]=np.einsum('abc,abcij->ij',w,self.grid)
            if len(self.cache)>30000:self.cache.clear();self.cache[key]=np.einsum('abc,abcij->ij',w,self.grid)
        b=self.complex_binding.bind_symbol(F_source_symbol=self.cache[key],jbar=np.zeros(9),mubar=self.mu,Cbar=self.cb,
            k_registered=ni['ell_F_m']*(self.root@kv),Eref=ni['Eref_J'],ell_F=ni['ell_F_m'],gamma=self.gamma,
            static_binding_module=self.static_binding,relative_singular_floor=ni['relative_singular_floor'],hermitian_tolerance=ni['hermitian_tolerance'])
        f=np.zeros((10,1),complex);f[0,0]=1
        r=self.complex_binding.solve_symbol(bound=b,source_density_columns=f,relative_singular_floor=ni['relative_singular_floor'],
            full_residual_relative_tolerance=ni['solve_rtol'],full_residual_absolute_tolerance=ni['solve_atol'])
        return np.asarray(r['fields'])[:,0]*(4*self.gamma*(kv@kv))
    def quantity(self,p,kind):
        x=self.response(p[3:6],p[6],p[:3])
        if kind=='EPS':return float(abs(1-x[0]))
        r=math.sqrt(2);a=x[1:7]
        g=np.array([[a[0],a[5]/r,a[4]/r],[a[5]/r,a[1],a[3]/r],[a[4]/r,a[3]/r,a[2]]])
        return float(np.linalg.norm(self.isq@g@self.isq,2))

def search(ctx,lo,hi,kind,seed):
    rng=np.random.default_rng(seed); candidates=[]
    # Independently sampled directions, exact cardinal vertices, and random interior torus.
    dirs=rng.normal(size=(36,3));dirs/=np.linalg.norm(dirs,axis=1)[:,None]
    for t in itertools.product(np.arange(4)*np.pi/2,repeat=3):
        for n in dirs:
            p=np.r_[t,n,lo];candidates.append((ctx.quantity(p,kind),p))
    for j in range(1200):
        p=np.r_[rng.uniform(0,2*np.pi,3),rng.normal(size=3),rng.uniform(lo,hi)]
        candidates.append((ctx.quantity(p,kind),p))
    candidates.sort(key=lambda x:x[0],reverse=True);starts=[]
    for value,p in candidates:
        if all(np.linalg.norm(p[:3]-q[:3])>.2 for _,q in starts):starts.append((value,p.copy()))
        if len(starts)==4:break
    if kind=='EPS' and lo>2:
        prior=read(OUT/'EPS_REVIEW_V001.json')['shells'][0]
        p=np.r_[prior['t'],prior['direction'],lo]
        starts.append((ctx.quantity(p,kind),p))
    best=starts[0];evaluations=len(candidates)
    # Coordinate pattern ascent, independently written, each successful move retained.
    for cur,p in starts:
        step=np.array([.35,.35,.35,.18,.18,.18,(hi-lo)/3])
        for it in range(100):
            improved=False
            for d in range(7):
                for sign in (-1,1):
                    q=p.copy();q[d]+=sign*step[d];q[6]=np.clip(q[6],lo,hi)
                    q[3:6]/=np.linalg.norm(q[3:6]);value=ctx.quantity(q,kind);evaluations+=1
                    if value>cur:cur,p=value,q;improved=True
            if not improved:step*=.5
            if np.max(step[:6])<2e-7:break
        if cur>best[0]:best=(cur,p)
    v,p=best
    return dict(maximum=v,t=np.remainder(p[:3],2*np.pi).tolist(),direction=(p[3:6]/np.linalg.norm(p[3:6])).tolist(),k=float(p[6]),evaluations=evaluations,
        qualification='numerical sampled/local maximum, not a rigorous supremum certificate')

def eps():
    ctx=Context();rec=read(CERT/'gates/EPS_CERT_V006.json');out=[]
    for lo in (2,30,300):
        s=next(s for s in rec['shells'] if s['lo_inverse_kpc']==lo)
        mine=search(ctx,lo,lo+1,'EPS',51000+lo)
        mine.update(shell=[lo,lo+1],reported_eps=s['eps'],reported_envelope=s['eps_envelope'],ratio_to_eps=mine['maximum']/s['eps'],ratio_to_envelope=mine['maximum']/s['eps_envelope'])
        out.append(mine);print('EPS',lo,mine,flush=True)
    assert [s['range_inverse_kpc'] for s in rec['shells']]==[[float(i),float(i+1)] for i in range(2,363)]
    coverage={str(P):{'required':math.sqrt(2)*2*P,'available':363.,'pass':363>=math.sqrt(2)*2*P} for P in (64,128)}
    write('EPS_REVIEW_V002.json',dict(shells=out,coverage=coverage,low_shells_not_envelope=[s['range_inverse_kpc'] for s in rec['shells'] if s['eps']<s['eps_envelope']*(1-1e-10)],
        scope='Pinned production symbol modules, independent cardinal-torus product sampling and local search; no checker/build evaluator imports.'))

def common_roster(ctx):
    mod=ART/'tail_scheme_impl_c2/module'
    RS=load(mod/'uv_tail_source_roster_c2v001.py','4366e3d6ca717b6f25a6799fa60b8ce05561a70d39662d7b1f08b75fc2171ad2')
    import ctypes
    class J0:
        def __init__(self):
            self.lib=ctypes.CDLL('/usr/lib/libSystem.B.dylib');self.fun=self.lib.j0
            self.fun.argtypes=[ctypes.c_double];self.fun.restype=ctypes.c_double
        def j0(self,x):
            x=np.asarray(x,float)
            return np.fromiter((self.fun(float(a)) for a in x.ravel()),dtype=float,count=x.size).reshape(x.shape)
    jn=J0()
    p=UPC/'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json';prof=read(p)
    assert sha(p)=='f5becd4586264ef156b021812d440e884f518c61dc9953e41a4fb1494218c60b'
    req=read(Path(ctx.res['passes'][-1]['field']).parent/'request.json')['argv'];rot=Path(req[req.index('--rotation-directory')+1])
    with np.load(rot/'rotation_base_arrays.npz',allow_pickle=False) as z: arr={k:z[k].copy() for k in ('rho0','volume_weights_m3','radial_nodes_m','z')}
    units=dict(kpc_m=ctx.kpc,solar_mass_kg=ctx.ni['solar_mass_kg'])
    ros=RS.roster_rotation(arr,RS.stars_registered(prof,'DDO154',units=units),s_edges_kpc2=prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],kpc_m=ctx.kpc,M_s=64)
    return ros,jn

def quadrature(a,b,width,order):
    n=max(1,math.ceil((b-a)/width));e=np.linspace(a,b,n+1);x,w=np.polynomial.legendre.leggauss(order)
    return ((e[1:,None]+e[:-1,None])/2+(e[1:,None]-e[:-1,None])*x/2).ravel(),np.broadcast_to((e[1:,None]-e[:-1,None])*w/2,(n,order)).ravel()

def gas_P(gas,kp,M,jn):
    # Independent polynomial coefficient representation in normalized GL4 coordinate.
    x4,_=np.polynomial.legendre.leggauss(4);x,w=np.polynomial.legendre.leggauss(M)
    basis=[]
    for i in range(4):
        roots=np.delete(x4,i);poly=np.polynomial.polynomial.polyfromroots(roots)
        basis.append(np.polynomial.polynomial.polyval(x,poly)/np.polynomial.polynomial.polyval(x4[i],poly))
    L=np.array(basis).T;cols=[]
    for a,(lo,hi) in enumerate(zip(gas.s_edges_kpc2[:-1],gas.s_edges_kpc2[1:])):
        s=(lo+hi)/2+(hi-lo)*x/2
        J=jn.j0(np.outer(kp,np.sqrt(s)*gas.kpc_m))
        part=J@((math.pi*(hi-lo)/2*gas.kpc_m**2*w)[:,None]*L)
        cols.extend(part[:,i] for i in range(4) if gas.present[4*a+i])
    return np.stack(cols,axis=1)
def gas_F(gas,kz):
    return np.stack([np.exp(-1j*np.outer(kz,gas.elements_z[i]))@gas.elements_m[i]/(2*np.pi*gas.column_rdr_m2[i]) for i in range(len(gas.present)) if gas.present[i]],axis=1)

def gq():
    ctx=Context();ros,jn=common_roster(ctx);gas=ros.gas;rng=np.random.default_rng(529)
    kp=np.r_[rng.uniform(4,math.sqrt(2)*4,15),rng.uniform(0,256,32),227.6,256,362]
    kz=np.r_[rng.uniform(-4,4,15),rng.uniform(-256,256,32),0,0,0]
    P={M:gas_P(gas,kp/ctx.kpc,M,jn) for M in (64,128,256)};F=gas_F(gas,kz/ctx.kpc)
    S={M:np.sum(P[M]*F,axis=1) for M in P};P0=sum(float(np.sum(m)) for i,m in enumerate(gas.elements_m) if gas.present[i])
    rows=[]
    for a,b in ((64,128),(128,256)):
        d=np.abs(S[a]-S[b]);rel=d/np.maximum(np.abs(S[b]),1e-300)
        rows.append(dict(M_s=a,doubled=b,nodes=50,max_abs_over_P0=float(d.max()/P0),max_relative=float(rel.max()),
            at_k_perp=float(kp[np.argmax(d)]),all_kp_le256_max_abs_over_P0=float(d[kp<=256].max()/P0),
            in_domain_pass=bool(np.all(d[kp<=256]/P0<=1e-12)),per_node=[dict(k_perp=float(kp[i]),k_z=float(kz[i]),over_P0=float(d[i]/P0),relative=float(rel[i])) for i in range(50)]))
    records={}
    for name in ('GQ_CERT_V002','GQ_CERT_V003_KB128','GQ_CERT_V003_KB256_MS128'):
        r=read(CERT/'gates'/f'{name}.json')
        records[name]=dict(verdict=r['verdict'],max_relative_reported=r['max_rel_change'],max_relative_reaggregated=max(x['max_rel_change'] for x in r['rosters']),
            max_abs_reported=r['max_abs_diff_over_P0'],max_abs_reaggregated=max(x['max_abs_diff_over_P0'] for x in r['rosters']),
            every_roster_has_relative=all('max_rel_change' in x for x in r['rosters']),coverage=r['coverage_inverse_kpc'])
    write('GQ_REVIEW_V001.json',dict(results=rows,record_arithmetic=records,independence='Own normalized-coordinate Lagrange polynomial quadrature and vertical mass contraction, shared saved gas roster and libm J0. 50 independently chosen nodes, not full certificate sample reproduction.',
        module_P_relative_check=float(np.max(np.abs(gas.radial_factors(kp/ctx.kpc,jn.j0)-P[64]))/np.max(np.abs(P[64])))))

def surface(r,rr,ss,scale):
    if r<=rr[0]:return ss[0]
    if r>=rr[-1]:return ss[-1]*math.exp(-(r-rr[-1])/scale)
    j=int(np.searchsorted(rr,r));return ss[j-1]+(ss[j]-ss[j-1])*(r-rr[j-1])/(rr[j]-rr[j-1])
def rings(rr,ss,scale,height,kpc,msun,h2=False):
    x,w=np.polynomial.legendre.leggauss(4);rad=[]
    for lo,hi in zip([0.]+rr[:-1],rr):
        for q,v in zip(x,w):
            r=(lo+hi)/2+(hi-lo)*q/2;dr=(hi-lo)*v/2
            rad.append((r,2*np.pi*surface(r,rr,ss,scale)*msun*1e6*r*dr))
    tail=[]
    for q,v in zip(x,w):
        u=(q+1)/2;r=rr[-1]-scale*math.log(u)
        if h2:m=2*np.pi*ss[-1]*msun*1e6*scale*r*v/2
        else:m=2*np.pi*surface(r,rr,ss,scale)*msun*1e6*r*scale*v/(2*u)
        tail.append((r,m))
    factor=1.
    if h2:factor=2*np.pi*ss[-1]*msun*1e6*scale*(rr[-1]+scale)/math.fsum(m for r,m in tail)
    rad.extend((r,m*factor) for r,m in tail)
    return np.array([(r*kpc,2*height*kpc*math.atanh(q),m*v/2) for r,m in rad for q,v in zip(x,w)]),factor
def i1t():
    p=UPC/'CODEX1/GALAXY_RADIAL_SOURCE_REFERENCE_V001.json';prof=read(p)['galaxies']['NGC3198'];st=prof['stellar_reference']
    ni=read(ART/'ngc_route_a_freeboundary_c2/seed_v002/DEFAULT/seed/NGC3198_ROUTE_A_A2F10_SEED_C2V002_DEFAULT.json')['numerical_inputs'];kpc=ni['kpc_m'];msun=ni['solar_mass_kg']
    tail=read(UPC/'CODEX1/NGC3198_H2_SOURCE_TAIL_REDUCTION_RUN_V001/stdout.txt');h2p=Path(tail['source']['path']);assert sha(h2p)==tail['source']['sha256']
    rows=read(h2p)['S1_alternative_and_stellar_median_rows']['rows'][:10]
    assert all(r['conventions']['gas_helium']['value']=='ALREADY_INCLUDED' for r in rows)
    hr=[float(Fraction(r['radius_kpc_literal']['value'])) for r in rows];hs=[float(Fraction(r['components']['H2']['value_literal']['value'])) for r in rows]
    stars,_=rings(st['radius_kpc'],st['surface_density_Msun_pc2'],st['outer_scale_kpc'],st['height_kpc'],kpc,msun)
    h2,fac=rings(hr,hs,tail['outer_scale_kpc'],st['height_kpc'],kpc,msun,True);fixed=np.concatenate([stars,h2])
    # Independent Bernstein evaluation: quadratic controls endpoints b0,b2 and b1=3*mean-b0-b2.
    hi=prof['HI_plus_He'];x,w=np.polynomial.legendre.leggauss(4);gas=[]
    for j,(a,b) in enumerate(zip(hi['s_edges_kpc2'][:-1],hi['s_edges_kpc2'][1:])):
        b0=hi['boundary_controls_Msun_pc2'][j];b2=hi['boundary_controls_Msun_pc2'][j+1];b1=3*hi['annular_means_Msun_pc2'][j]-b0-b2
        for q,v in zip(x,w):
            u=(q+1)/2;s=(a+b)/2+(b-a)*q/2;sigma=b0*(1-u)**2+2*b1*u*(1-u)+b2*u*u
            if sigma>0:gas.append((math.sqrt(s)*kpc,0.,np.pi*(b-a)*v/2*sigma*msun*1e6))
    gas=np.array(gas)
    op=ART/'ngc_kgrid_fidelity_c2/phase23/ops/T120L_hovr';prep=read(op/'PREP.json')
    waves=np.load(op/'wavevectors.npy',mmap_mode='r');idx=np.r_[0,len(waves)//2,len(waves)-1,np.random.default_rng(52950).choice(np.arange(1,len(waves)//2),47,replace=False)]
    kv=np.array(waves[idx]);kp=np.linalg.norm(kv[:,:2],axis=1);kz=kv[:,2]
    # Independent Bessel J0 via periodic angular quadrature, avoids shared libm provider.
    def transform(rr):
        arguments=kp[:,None]*rr[None,:,0];mx=float(np.max(arguments));N=2**math.ceil(math.log2(mx+12*mx**(1/3)+64))
        sn=np.sin(2*np.pi*np.arange(N)/N);J=np.empty(arguments.shape)
        flat=arguments.ravel();dest=J.ravel()
        for a in range(0,len(flat),128):dest[a:a+128]=np.cos(flat[a:a+128,None]*sn[None,:]).mean(axis=1)
        return -299792458.**2*np.sum(J*np.exp(-1j*kz[:,None]*rr[None,:,1])*rr[None,:,2],axis=1),N
    tf,nf=transform(fixed);tg,ng=transform(gas);out=[]
    for key,a in (('fixed_source_fourier_J',tf),('initial_gas_fourier_J',tg),('current_source_fourier_J',tf+tg)):
        pp=op/prep['arrays'][key]['file'];assert sha(pp)==prep['arrays'][key]['sha256'];b=np.array(np.load(pp,mmap_mode='r')[idx]);rel=float(np.max(np.abs(a-b[:,0,0]))/np.max(np.abs(b[:,0,0])))
        out.append(dict(source=key,nodes=50,max_relative=rel,tolerance=1e-12,pass_gate=rel<=1e-12,other_components_max=float(np.max(np.abs(b[:,1:,0])))))
    # Omit H2 on purpose: this canary must exceed the same tolerance.
    ts,_=transform(stars);b=np.array(np.load(op/prep['arrays']['fixed_source_fourier_J']['file'],mmap_mode='r')[idx])[:,0,0]
    omit=float(np.max(np.abs(ts-b))/np.max(np.abs(b)))
    rec=read(CERT/'gates/I1T_NGC_T120L_V001.json');lo=read(CERT/'gates/LO_NGC_CERT_V002.json')
    assert lo['i1t']['record']['sha256']==sha(CERT/'gates/I1T_NGC_T120L_V001.json')
    for pin in lo['code_reading'].values():
        assert sha(pin['path'])==pin['sha256'];Path(pin['path']).read_text()
    write('I1T_NGC_REVIEW_V001.json',dict(results=out,nodes=idx.tolist(),ring_counts=dict(stars=len(stars),h2=len(h2),fixed=len(fixed),gas=len(gas)),angular_orders=[nf,ng],h2_tail_mass_normalization=fac,
        H2_omission_negative_control=dict(max_relative=omit,correctly_refused=omit>1e-12),LO_NGC=dict(sum_readout_share=lo['summed_max_over_theta'],i1t_ref_matches=True,scope=lo['i1t']['scope']),
        scope='Independent GL4 profile and HI Bernstein reconstruction plus angular-integral J0. Saved T120L iteration-zero source representation only; continuum tail source is untested.'))

def lo():
    ctx=Context();ros,jn=common_roster(ctx);rec=read(CERT/'gates/LO_CERT_V002.json');shell=next(s for s in rec['shells'] if s['range_inverse_kpc']==[64.,128.])
    # Own Gauss-Legendre integration of cylindrical domain. Chebyshev interpolation
    # only for separable vertical factors; direct interpolation validation recorded.
    width=.5;n=16;nodes=np.cos(np.pi*np.arange(n)/(n-1));bw=(-1.)**np.arange(n);bw[[0,-1]]*=.5
    zz=(np.arange(257)[:,None]+(nodes[None,:]+1)/2)*width
    tab=ros.vertical_factors(zz.ravel()/ctx.kpc,299792458.).reshape(257,n,-1)
    def interpolate(z,table):
        p=np.minimum(np.floor(z/width).astype(int),256);u=2*(z/width-p)-1;d=u[:,None]-nodes
        hit=np.abs(d)<1e-14;d[hit]=1.;a=bw/d;a[hit.any(axis=1)]=0.;a[hit]=1.;a/=a.sum(axis=1)[:,None]
        return np.einsum('ij,ij...->i...',a,table[p])
    ztest=np.random.default_rng(52964).uniform(0,128,100);direct=ros.vertical_factors(ztest/ctx.kpc,299792458.);approx=interpolate(ztest,tab)
    interp=float(np.max(np.abs(direct-approx))/np.max(np.abs(direct)))
    # Endpoint maps remove the radial sqrt corner. Coarse/refined independent panels.
    answers=[]
    for step,order in ((.5,10),(.25,12)):
        p1,w1=quadrature(0,63,step,order);u,wu=quadrature(0,1,1/8,order);p2=64-u*u;w2=2*u*wu
        p3,w3=quadrature(64,127,step,order);p4=128-u*u;w4=2*u*wu
        kp=np.r_[p1,p2,p3,p4];wp=np.r_[w1,w2,w3,w4]
        P=ros.radial_factors(kp/ctx.kpc,jn.j0);B0=0.;B1=0.
        for j,k in enumerate(kp):
            a=math.sqrt(max(0.,64**2-k*k));b=math.sqrt(max(0.,128**2-k*k));z,wz=quadrature(a,b,step,order)
            Sv=interpolate(z,tab@P[j]);km=np.sqrt(k*k+z*z)/ctx.kpc
            base=(4*np.pi*k*wp[j]/ctx.kpc**3)*wz*np.abs(Sv)/(4*ctx.gamma*km**2)/(2*np.pi)**3
            B0+=float(base.sum());B1+=float(np.sum(base*km))
        answers.append(dict(panel_width=step,order=order,B0=B0,B1=B1,k_perp_nodes=len(kp)));print('LO integral',answers[-1],flush=True)
    rho=search(ctx,64,128,'RHO',529128)
    v=np.array([r['speed_km_s'] for r in ctx.res['passes'][-1]['rows']]);R=np.array(rec['R_kpc'])*ctx.kpc;tau=np.array(rec['tau_km_s'])
    mine=float(np.max(v*R/tau)*rho['maximum']*answers[-1]['B1']/4)
    write('LO_REVIEW_V001.json',dict(shell=[64,128],integrals=answers,vertical_interpolation_max_relative=interp,rho_search=rho,
        record=dict(B0=shell['B0'],B1=shell['B1_per_m'],rho=shell['rho_used'],max_over_tau=shell['max_over_tau']),
        B1_relative_difference=abs(answers[-1]['B1']/shell['B1_per_m']-1),own_max_over_tau=mine,threshold=.005,pass_gate=mine<.005,
        exact_coverage_end=rec['coverage_inverse_kpc'][1],required_for_P128=math.sqrt(2)*256,
        scope='Own cylindrical shell integration and envelope search. Saved C4R3 source representation shared; continuum roster implementation not independently reimplemented for LO.'))

if __name__=='__main__':
    for name in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):assert os.environ.get(name)=='1',name
    t=time.time();{'eps':eps,'i1t':i1t,'gq':gq,'lo':lo}[sys.argv[1]]();print('seconds',round(time.time()-t,3),flush=True)
