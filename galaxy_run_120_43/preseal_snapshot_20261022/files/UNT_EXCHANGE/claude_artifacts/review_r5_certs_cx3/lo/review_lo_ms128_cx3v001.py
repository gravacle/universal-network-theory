"""0552 independent LO shell review: no certificate/checker imports or worker runs.
Production source/symbol definitions are shared; integration, rho search, algebra
and gas radial-factor reconstruction are independent. Saved C4R3 only.
"""
import sys,os,json,math,hashlib,itertools,time,resource
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
OUT=Path(__file__).resolve().parent
ART=Path('/Users/bgm/Research/UNT_EXCHANGE/claude_artifacts')
UPC=Path('/Users/bgm/Research/Universal Network Theory/UNT_PROGRAM_CONTROL/FIRST_CONSTRUCTION_REVIEW_2026-10-13')
CERT=ART/'tail_scheme_impl_c2/certificates_v003'
RECORD=CERT/'gates/LO_CERT_V003_MS128.json'
RECORD_SHA='9fdb897ae3b80dd6a3d2cf9ff273619dbf5fa419405cc8dacd1fa77ee2539268'
DATE_U='Sun Oct 18 15:00:13 UTC 2026'
READS=set()
def audit(event,args):
    if event in ('subprocess.Popen','os.system','os.exec','os.spawn','os.posix_spawn','os.fork','os.forkpty','os.remove','os.unlink','os.rename','os.replace','os.rmdir') or event.startswith('socket.'):
        raise RuntimeError('FORBIDDEN_OPERATION '+event)
    if event=='open' and isinstance(args[0],(str,bytes)):
        p=Path(os.fsdecode(args[0]));absolute=str(p.absolute());real=str(p.resolve())
        if '/runs_ext/UVT_' in real or 'KMAX_A2F10_C5H_RUN_V001' in real:raise RuntimeError('FORBIDDEN_RUN_READ')
        if 'NGC3198' in real.upper() and any(x in real.upper() for x in ('TARGET','OBSERVED')) and 'TARGET_FREE' not in real.upper():raise RuntimeError('FORBIDDEN_NGC_TARGET')
        mode,flags=args[1],args[2]
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND))
        if writing:
            if Path(real).parent!=OUT or not flags & os.O_EXCL:raise RuntimeError('NEW_LO_OUTPUTS_ONLY')
        elif '/Research/' in absolute or '/UNT_' in real:READS.add(absolute)
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
    ros=RS.roster_rotation(arr,RS.stars_registered(prof,'DDO154',units=units),s_edges_kpc2=prof['galaxies']['DDO154']['HI_plus_He']['s_edges_kpc2'],kpc_m=ctx.kpc,M_s=128)
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

def output(name,data):
    data.update(date_u=DATE_U,utc=datetime.now(timezone.utc).isoformat(),label='TESTED_SAVED_REPLAY_SOURCE_QUADRATURE_ONLY',
        source={'path':__file__,'sha256':sha(__file__)},peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scientific_launches=0,real_targets_opened=False)
    data['read_dependencies']=[{'path':p,'sha256':sha(p)} for p in sorted(READS) if Path(p).is_file()]
    with (OUT/name).open('x') as f:json.dump(data,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'output':name,'sha256':sha(OUT/name),'seconds':round(time.time()-START,3),'peak_rss_bytes':data['peak_rss_bytes']}),flush=True)

def context_source():
    assert sha(RECORD)==RECORD_SHA
    rec=read(RECORD);ctx=Context();ros,jn=common_roster(ctx)
    assert ros.gas.M_s==128
    assert ros.digest()==rec['build']['roster_digest']
    assert ros.gas.record()==rec['build']['roster_gas']
    assert float(ctx.res['identity']['route_a']['custody']['physical']['gamma'])==ctx.gamma
    return rec,ctx,ros,jn

def static_review():
    rec,ctx,ros,jn=context_source()
    checks=[]
    def ck(name,value,details=None):checks.append({'name':name,'passed':bool(value),'details':details})
    ck('required_source_gas_M_s_field',type(rec.get('source_gas_M_s')) is int and rec.get('source_gas_M_s')==128,
       {'source_gas_M_s':rec.get('source_gas_M_s'),'actual_gas_M_s':rec.get('gas_M_s')})
    ck('actual_source_M_s128_and_roster_digest',ros.gas.M_s==128 and ros.digest()==rec['build']['roster_digest'])
    ck('config_roster_and_declared_M_s128',rec['gas_M_s']==rec['tail_config_gas']['M_s']==rec['build']['roster_gas']['M_s']==128)
    for label,pin in dict(rec['pins'],producer=rec['producer'],common=rec['common']).items():ck('byte_pin_'+label,sha(pin['path'])==pin['sha256'])
    producer=Path(rec['producer']['path']).read_text();common=Path(rec['common']['path']).read_text()
    ck('producer_passes128_to_roster_and_config',"C3.ddo_roster(U, RS, PV, jn, 'C4R3', C3.MS_PROD)" in producer and 'M_s=C3.MS_PROD' in producer and 'MS_PROD = 128' in common)
    ck('producer_missing_field_confirmed','source_gas_M_s' not in producer and 'gas_M_s=int(C3.MS_PROD)' in producer)
    rows=read(rec['pins']['row_binding']['path'])['query_rows'];prereg=read(rec['pins']['prereg_v005']['path'])
    ids=[r['id'] for r in rows];R=np.array([r['radius_m'] for r in rows]);tau=np.array(prereg['tau_km_s'])
    v=np.array([r['speed_km_s'] for r in ctx.res['passes'][-1]['rows']])
    ck('row_ids_radii_tau_saved_predictions',ids==rec['row_ids']==prereg['row_ids'] and np.array_equal(R/ctx.kpc,rec['R_kpc']) and np.array_equal(tau,rec['tau_km_s']) and np.array_equal(v,rec['v_state_km_s']))
    ranges=[sh['range_inverse_kpc'] for sh in rec['shells']]
    ck('ten_contiguous_shells_cover4_to363',len(ranges)==10 and ranges[0][0]==4 and ranges[-1][1]==363 and all(a[1]==b[0] for a,b in zip(ranges,ranges[1:])))
    for P in (64,128):ck('coverage_full_reach_P'+str(P),rec['coverage_inverse_kpc'][1]>=math.sqrt(2)*2*P and rec['envelope_bound']['coverage_max_inverse_kpc']>=math.sqrt(2)*2*P,{'required':math.sqrt(2)*2*P,'available':rec['coverage_inverse_kpc'][1]})
    errors=[]
    for sh in rec['shells']:
        ratio=v*R*sh['rho_used']*sh['B1_per_m']/4/tau
        err=float(np.max(np.abs(ratio-np.asarray(sh['per_row_over_tau']))))
        errors.append(err)
        ck('shell_algebra_'+str(sh['range_inverse_kpc']),np.allclose(ratio,sh['per_row_over_tau'],rtol=5e-15,atol=0) and math.isclose(float(max(ratio)),sh['max_over_tau'],rel_tol=5e-15),err)
        ck('shell_rho_envelope_and_tolerance_'+str(sh['range_inverse_kpc']),sh['rho_used']==max(sh['rho_G_sampled'],sh['rho_G_envelope']) and sh['max_over_tau']<=.005)
    ck('summed_all10_tolerance',math.isclose(math.fsum(sh['max_over_tau'] for sh in rec['shells']),rec['summed_max_over_tau'],rel_tol=5e-15) and rec['summed_max_over_tau']<=.05)
    ck('envelope_estimate_not_proof_labeled','not a proven' in rec['label'] and 'not a proven' in rec['envelope_bound']['label'])
    # Small independent normalized Lagrange reconstruction verifies actual Ms128
    # radial factors. This is distinct from trusting the producer's record label.
    kp=np.array([0.,128.,154.25,193.5,227.6,255.99])/ctx.kpc
    own=gas_P(ros.gas,kp,128,jn);actual=ros.gas.radial_factors(kp,jn.j0)
    relative=float(np.max(np.abs(own-actual))/np.max(np.abs(own)))
    ck('independent_Ms128_radial_factor_replica',relative<1e-12,relative)
    output('LO_STATIC_REVIEW_V001.json',{'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'record':{'path':str(RECORD),'sha256':RECORD_SHA},
       'record_contract':'FAIL_REQUIRED_FIELD' if not checks[0]['passed'] else 'PASS','source_roster_digest':ros.digest(),'source_gas_M_s_measured':ros.gas.M_s,
       'max_algebra_error':max(errors),'numeric_shell_max':max(sh['max_over_tau'] for sh in rec['shells']),'summed_max_over_tau':rec['summed_max_over_tau'],
       'source_scope':'Actual permitted C4R3 saved source reconstructed at Ms128; no producer/checker import or scientific solve.'})

def integral(level):
    rec,ctx,ros,jn=context_source();shell=next(sh for sh in rec['shells'] if sh['range_inverse_kpc']==[128.,256.])
    width=.5;n=16;nodes=np.cos(np.pi*np.arange(n)/(n-1));bw=(-1.)**np.arange(n);bw[[0,-1]]*=.5
    zz=(np.arange(513)[:,None]+(nodes[None,:]+1)/2)*width
    tab=ros.vertical_factors(zz.ravel()/ctx.kpc,299792458.).reshape(513,n,-1)
    def interpolate(z,table):
        panel=np.minimum(np.floor(z/width).astype(int),512);u=2*(z/width-panel)-1;d=u[:,None]-nodes
        hit=np.abs(d)<1e-14;d[hit]=1.;a=bw/d;a[hit.any(axis=1)]=0.;a[hit]=1.;a/=a.sum(axis=1)[:,None]
        return np.einsum('ij,ij...->i...',a,table[panel])
    ztest=np.random.default_rng(552128).uniform(0,256,150);direct=ros.vertical_factors(ztest/ctx.kpc,299792458.);approx=interpolate(ztest,tab)
    interpolation=float(np.max(np.abs(direct-approx))/np.max(np.abs(direct)))
    assert interpolation<1e-11
    step,order=(.5,10) if level=='coarse' else (.25,12)
    p1,w1=quadrature(0,127,step,order);u,wu=quadrature(0,1,1/8,order);p2=128-u*u;w2=2*u*wu
    p3,w3=quadrature(128,255,step,order);p4=256-u*u;w4=2*u*wu
    kp=np.r_[p1,p2,p3,p4];wp=np.r_[w1,w2,w3,w4]
    P=ros.radial_factors(kp/ctx.kpc,jn.j0);B0=0.;B1=0.;node_count=0
    for j,k in enumerate(kp):
        low=math.sqrt(max(0.,128**2-k*k));high=math.sqrt(max(0.,256**2-k*k));z,wz=quadrature(low,high,step,order)
        Sv=interpolate(z,tab@P[j]);km=np.sqrt(k*k+z*z)/ctx.kpc
        base=(4*np.pi*k*wp[j]/ctx.kpc**3)*wz*np.abs(Sv)/(4*ctx.gamma*km**2)/(2*np.pi)**3
        B0+=float(base.sum());B1+=float(np.sum(base*km));node_count+=len(z)
        if j%1000==0:print(json.dumps({'level':level,'radial_nodes_complete':j,'total':len(kp),'seconds':round(time.time()-START,1)}),flush=True)
    v=np.array([r['speed_km_s'] for r in ctx.res['passes'][-1]['rows']]);R=np.array(rec['R_kpc'])*ctx.kpc;tau=np.array(rec['tau_km_s'])
    derived=float(np.max(v*R/tau)*shell['rho_used']*B1/4)
    output('LO_INTEGRAL_'+level.upper()+'_V001.json',{'shell':[128.,256.],'source_gas_M_s':ros.gas.M_s,'source_roster_digest':ros.digest(),
      'panel_width':step,'order':order,'B0':B0,'B1':B1,'k_perp_nodes':len(kp),'tensor_nodes_evaluated':node_count,
      'vertical_interpolation_max_relative':interpolation,'certificate_B0':shell['B0'],'certificate_B1':shell['B1_per_m'],
      'B1_relative_difference':abs(B1/shell['B1_per_m']-1),'max_over_tau_using_certificate_rho':derived,'shell_tolerance':.005,'numeric_pass':derived<=.005,
      'method':'Independent nested cylindrical GL integration of complete spherical shell128<|k|<=256, abs source; endpoint square-root maps; barycentric vertical interpolation validated directly. Shared continuum source implementation; no certificate producer/checker imports.'})

def rho():
    assert sha(RECORD)==RECORD_SHA
    ctx=Context();rec=read(RECORD);shell=next(sh for sh in rec['shells'] if sh['range_inverse_kpc']==[128.,256.])
    answer=search(ctx,128,256,'RHO',552256)
    witness=shell['rho_envelope_search'];point=np.r_[witness['t_at'],witness['dir_at'],witness['k_at_inverse_kpc']]
    recomputed=ctx.quantity(point,'RHO')
    output('LO_RHO_REVIEW_V001.json',{'shell':[128.,256.],'own_search':answer,'certificate_rho':shell['rho_used'],
        'certificate_witness_recomputed':recomputed,'witness_relative_difference':abs(recomputed/shell['rho_used']-1),
        'qualification':'Independent direct symbol binding and own sampled/local search; numerical estimate, not interval/Lipschitz proof. Certificate witness evaluation is separately labeled.'})

if __name__=='__main__':
    for key in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):assert os.environ.get(key)=='1'
    START=time.time()
    if sys.argv[1]=='static':static_review()
    elif sys.argv[1]=='rho':rho()
    elif sys.argv[1] in ('coarse','refined'):integral(sys.argv[1])
    else:raise ValueError('unknown mode')
