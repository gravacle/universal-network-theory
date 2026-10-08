"""Guarded same-source coupled complete retarded radiation history; root alone executes."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, time
BASE=Path(__file__).resolve().parent
STEM='CROSS_U_FULL_FLRW_RETARDED_HISTORY_V001'
AUTHOR_GUARD=False
KB,C,CP=.02,1.98,299792.458
KBL,CL=KB/2,C/2
AI,AF,AMP=.01,1.,1e-8
STATE_TOL,INCREMENT_TOL,NORMAL_TOL,ROW_TOL=1e-3,1e-6,1e-6,2e-11
FLOOR=1e-13
CORRECTION_CAP=6
CFG={'series_terms':52}
TRIALS=[dict(name='TIME512',nstep=512,k=.1,omega=.1,ns=32,na=64),dict(name='FINE1024',nstep=1024,k=.1,omega=.1,ns=32,na=64)]
ORIGINAL='CROSS_U_FULL_FLRW_FINITE_SLICE_V001'
OLD='CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001'
WITNESS='CROSS_U_RETARDED_RADIATION_SOURCE_OPERATOR_WITNESS_V002'
INITIAL_PAYLOAD=ORIGINAL+'_FINE_K1_O0_CP_000000.npz'
INITIAL_COMMIT=ORIGINAL+'_FINE_K1_O0_CP_000000_COMMIT.json'
FLAGS={n:False for n in ['primordial_state','nonlinear_clock','native_normalization','mode_inertia','observed_growth','observed_lensing','continuum_angular','joint_epsilon_adopted']}
INPUTS,OUTPUTS,RAW={}, {}, {}
PAIRS,CORE_HISTORY=[],[]
SOURCE_SHA=MANIFEST_SHA=None
CONTEXT={}
BG_SPAN='8881f1df923d053d1d4b7ce06bfe4a50e856a62b49a25546a8d7e7a0d9f12bf2'
PINS={'CROSS_U_EXACT_RETARDED_RADIATION_MOMENT_OPERATOR_V001.md': 'c4fcedb21d45274bc6632b755e87c6eacf566f5d84268d103e625990bc299752', 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md': 'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'cross_u_full_flrw_core_baryon_recovery_v001.py': 'd9efb102c8a60a0845dde9fd4a3c9020d7f5e210c10a995a53faa0ba68e71b31', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001.md': 'f73ffcb2e311602e4a6ca4dfeeef7121cbf3113878e45ab04826daa40a3a4419', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_RESULT.json': 'b96a588b0421bf88666899e846bf50229305db0401b4bad546591e46e2f8576d', 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001_RECEIPT.json': 'be1491ac72166d7fc51a7ff7d40ccd99142a215200e338cc034bba025a8ae22b', 'cross_u_retarded_radiation_source_operator_witness_v002.py': '69f90ef43a2a93d5d73e257fd5ce5d803753ba8e1d6e98c224a5eaa85c2c169a', 'CROSS_U_RETARDED_RADIATION_SOURCE_OPERATOR_WITNESS_V002.md': '5031972a1e8ecc880c4cac8962813119397d2d667e4904793a497562d60fd3dd', 'CROSS_U_RETARDED_RADIATION_SOURCE_OPERATOR_WITNESS_V002_RESULT.json': 'deca56d1b993803261fa2039688bf01c9e5402fb73a0882da56a31b0dcff263e', 'CROSS_U_RETARDED_RADIATION_SOURCE_OPERATOR_WITNESS_V002_RECEIPT.json': '4da080680323157f8649ac6a765d9a483eb87b7ecda5951583222573cb59a7c6', 'constrained_u_retarded_radiation_kernel_controls_v001.py': 'dc7885ee0349145f05a7e18bf9ce48bf257626ebbc4bd48ebc366791fe456db2', 'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000.npz': '72aa7178724affa2a06c97e1f3990872670ed85df0cce720beca2b21f6c05879', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000_COMMIT.json': '43a762492edf95003e26c12c11ec3d34dead48b67b1da5760411607187537d95'}
LITERAL_SPANS={'sha': '7ae5582ed4ffb90f7e7fb5190cad3559332b0e8a4ed3055ec99d047bcc0112df', 'now': 'b9bd7c7db45e81c5efdce2dcb7df8c4e3996559be95b18ba93b7dfbb07a1b057', 'canonical': 'c9d8602cde326727608d13dd49b9c5d35f2f5b30e4b8fb406498106ffb04905b', 'encode': '996948a5b1f70c59fe55c83d325804ba83084d0b8894267e954212fb3724fb97', 'seal': '150df90b8dc3fd26dace23c858df6e0cb5e1f4c47d0b7984214c0de7157f6037', 'recheck': '13a7c4cc77da6995fb9949e150fcaf2e19f335ce82c49ba28d323a9436690236', 'write': 'f1db1df74cc007514970c7ec93edf6632bb457e53125797b488c60962fe4eed3', 'load_background': '55b9d13e77ac8cca30ec3d3fa20c323e623c740f768c44cccca6400a9681b7b6', 'bg': '9b1ab946ffe194f9bcddba16db78efe37ae2eb6ccc88ec47f12c53e1bd1480b4', 'legendre': '671e20cd8fe47819e23ccd8c2630c4625427fad284b8f6e175d50fcbc3178c2b', 'layout': 'd0bb5af30d66aea5a3fe46973bed4794f105ac4fa2258fe9dab723b6fbcdd666', 'equilibrated_solve': '44de3a9f06e518e6c8d9fcf523ebc60955917e519e94cfcccf8277574ab91dcb', 'phase_nodes': '776ba8b11d9cc0045a46fa2ae56e5706ff4983333192be23e6e24e455dc1389a', 'rate_matrix': '9105eae6adf8501c617e2444c76625b56ec97dc4bab03802f447d5d962dd9da2', 'native_map': '4c1a95c744613d8d0f6299f5d9171279f9b9176478a8ce66afbc04b501ce1f17', 'metric_increment': '2f287109e8f9944c289d6052e79b735398b7257828b3ef548686604bc8fbba5c', 'diagnostic_update': 'c699040424f4d3a80793ac371f0fb64e3aa75adb5c3b2fa233440d90a233e90d', 'journal': '2a4a4d501873603f200336b57a1fd392ce181393d56c40e07827b6d4755788cf', 'gate': 'be194a9ddfb9793b6e3b0d9ebece1c8cdc038cc5693eb1830a487466397f217c', 'original': 'b1b6beface6fd23010de1b7a5440b5d2be5405d9fefe6e98fecfdc3162e675c7', 'complex_moment': '53d66712ad4899a4c9fe6ffd57f9d2335576180dfc031b0af53f0569e9735766'}
PROTOCOL_SHA='f06a5fd890ccae9e2f0e0f08c29a48f8222a2ed6d51176ab61652750f0f219b4'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def now(): return datetime.now(timezone.utc).isoformat()

def canonical(value):
    if isinstance(value,dict): return {str(k):canonical(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [canonical(v) for v in value]
    if 'np' in globals() and isinstance(value,np.ndarray): return canonical(value.tolist())
    if 'np' in globals() and isinstance(value,np.generic): return canonical(value.item())
    if type(value) is float and not math.isfinite(value): raise ValueError('Nonfinite JSON scalar')
    if value is None or type(value) in (str,int,float,bool): return value
    raise TypeError('Noncanonical metadata '+str(type(value)))

def encode(value): return (json.dumps(canonical(value),sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()

def seal(path, expected):
    p=Path(path).resolve()
    if not p.is_relative_to(BASE.parent): raise ValueError('Unowned input path')
    if sha(p)!=expected: raise ValueError('Input hash '+str(p))
    if str(p) in INPUTS and INPUTS[str(p)]!=expected: raise ValueError('Conflicting seal')
    INPUTS[str(p)]=expected

def recheck():
    for p,h in dict(INPUTS,**OUTPUTS).items():
        if sha(p)!=h: raise ValueError('Changed protected byte '+p)
    if sha(__file__)!=SOURCE_SHA: raise ValueError('Changed own source')

def write(name,value):
    p=BASE/name; raw=encode(value)
    with p.open('xb') as f: f.write(raw);f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
    if p.read_bytes()!=raw: raise IOError('Exclusive JSON reread')
    OUTPUTS[str(p.resolve())]=sha(p)
    return sha(p)

def load_background():
    path=BASE/'constrained_u_shared_eps_ngc_pantheon_v001.py';text=path.read_text();tree=ast.parse(text)
    f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='background')
    span='\n'.join(text.splitlines()[f.lineno-1:f.end_lineno])+'\n'
    if hashlib.sha256(span.encode()).hexdigest()!=BG_SPAN: raise ValueError('Literal background span')
    names={n.id for n in ast.walk(f) if isinstance(n,ast.Name)}
    if not {'np','math','a','f'}.issubset(names): raise ValueError('Background dependency inventory')
    env={'np':np,'math':math};exec(compile(ast.Module(body=[f],type_ignores=[]),str(path),'exec'),env)
    return env['background']

def bg(x,k,fixed,background):
    a=math.exp(float(x));r=background(np.asarray(a),fixed)
    out={n:float(v) for n,v in r.items()};out.update(a=a,q=CP*k/(fixed['Hunit']*a),b=1.5*fixed['OB']/fixed['rG']/a**3,r=1.5*fixed['OR']/fixed['rG']/a**4,Q=fixed['Q0_over_Hstar']*float(r['q']))
    out['B']=out['b']+4*out['r']/3+out['w'];out['gamma']=CL*out['Q']**2/out['w']
    if not all(math.isfinite(v) for v in out.values()) or min(out['h'],out['q'],out['Q'],out['w'],out['cs'],out['b'],out['r'])<=0: raise ArithmeticError('Nonpositive/nonfinite physical background')
    if not 1<=out['Q']/fixed['Q0_over_Hstar']<math.sqrt(1+fixed['eps']): raise ArithmeticError('Actual background pressure domain')
    return out

def legendre(l,mu):
    if l==0: return np.ones_like(mu)
    a,b=np.ones_like(mu),mu.copy()
    for n in range(1,l): a,b=b,((2*n+1)*mu*b-n*a)/(n+1)
    return b

def layout(ns,na,omega):
    sn,sw=np.polynomial.legendre.leggauss(ns);sn=(sn+1)/2;sw=sw*sn
    pn,pw=np.polynomial.legendre.leggauss(16);pn=(pn+1)/2
    mu,mw=np.polynomial.legendre.leggauss(na);allmu=np.r_[mu,np.linspace(-1,1,17)]
    moments=np.asarray([(1j**l/2)*mw*legendre(l,mu) for l in range(7)])
    return dict(ns=ns,na=na,nodes=np.r_[sn,pn],weights=sw,om=omega*np.r_[sn,pn],mu=allmu,moments=moments,weight_sum=float(sw.sum()))

def equilibrated_solve(matrix,rhs):
    RAW['core_matrix']=matrix.copy();RAW['core_rhs']=rhs.copy()
    a=matrix.copy();b=rhs.copy();scale=np.ones(a.shape[-1]);rowscale=np.ones(a.shape[0])
    for _ in range(6):
        rr=np.sqrt(np.maximum(np.max(abs(a),axis=1),np.finfo(float).tiny));a/=rr[:,None];b/=rr[:,None];rowscale/=rr
        cc=np.sqrt(np.maximum(np.max(abs(a),axis=0),np.finfo(float).tiny));a/=cc[None,:];scale/=cc
    RAW.update(core_scaled_matrix=a.copy(),core_scaled_rhs=b.copy(),core_row_scale=rowscale.copy(),core_column_scale=scale.copy())
    y=np.linalg.solve(a,b)*scale[:,None];RAW['core_initial_solution']=y.copy()
    res=matrix@y-rhs;env=abs(matrix)@abs(y)+abs(rhs);err=float(np.max(abs(res)/np.maximum(env,FLOOR)))
    initial_error=err;rows=[]
    RAW.update(core_solution=y.copy(),core_residual=res.copy(),core_envelope=env.copy())
    if not np.all(np.isfinite(y)) or not math.isfinite(err):raise ArithmeticError('Nonfinite simultaneous solve')
    for iteration in range(1,CORRECTION_CAP+1):
        if err<=ROW_TOL:break
        prefix='core_correction_'+str(iteration)+'_';RAW[prefix+'before']=y.copy();RAW[prefix+'residual']=res.copy()
        correction_rhs=-rowscale[:,None]*res;RAW[prefix+'scaled_rhs']=correction_rhs.copy()
        delta_scaled=np.linalg.solve(a,correction_rhs);RAW[prefix+'scaled_delta']=delta_scaled.copy()
        delta=scale[:,None]*delta_scaled;RAW[prefix+'physical_delta']=delta.copy();candidate=y+delta;RAW[prefix+'candidate']=candidate.copy()
        res=matrix@candidate-rhs;env=abs(matrix)@abs(candidate)+abs(rhs);err=float(np.max(abs(res)/np.maximum(env,FLOOR)))
        RAW[prefix+'residual_after']=res.copy();RAW[prefix+'envelope_after']=env.copy()
        if not np.all(np.isfinite(candidate)) or not math.isfinite(err):raise ArithmeticError('Nonfinite original-equation residual correction')
        y=candidate;rows.append(dict(iteration=iteration,error=err,gate_passed=err<=ROW_TOL))
    RAW.update(core_solution=y.copy(),core_residual=res.copy(),core_envelope=env.copy())
    CORE_HISTORY.append(dict(trial=CONTEXT.get('trial'),nstep=CONTEXT.get('nstep'),initial_error=initial_error,final_error=err,corrections=rows,gate_passed=err<=ROW_TOL))
    return y,err

def phase_nodes(x,dx,k,fixed,background,order):
    u,w=np.polynomial.legendre.leggauss(order);cs=np.asarray([.5-math.sqrt(3)/6,.5+math.sqrt(3)/6,1.])
    xx=x+dx*cs[:,None]*(u[None,:]+1)/2;aa=np.exp(xx);hh=background(aa,fixed)['h'];qq=CP*k/(fixed['Hunit']*aa)
    out=dx*cs*((qq/hh)@w)/2
    return np.r_[0.,out]

def rate_matrix(g):
    a=np.zeros((7,11));b,r,w,h,s,q=(g[n] for n in ('b','r','w','h','cs','q'))
    rd=np.zeros(11);rd[2]=b;rd[9]=4*r/3;rd[3]=h*s
    phi=np.zeros(11);phi[0]=1;phi[4]=-h;phi[10]=-2*r/q**2
    a[0]=rd;a[1]=3*rd;a[1,4]-=q*q;a[1,2]-=q*q
    a[2,3]=-s;a[3]=3*rd;a[3,4]-=q*q;a[3,5]-=q*q*g['gamma']
    a[4]=phi;a[4,3]+=s;a[5,7]=1;a[5,3]=s
    a[6,6]=-2*h;a[6,5]=-CL*g['Q']**2*q
    return a/h

def native_map(old,bgs,dx,lay,fixed):
    n=len(lay['om']);root=math.sqrt(3);ga=np.array([[.25,.25-root/6],[.25+root/6,.25]])
    matrices=np.zeros((n,6,6));rhs=np.zeros((n,6,4));forcing=np.zeros((n,2))
    ell=fixed['Hunit']*.1/(1000*CP)
    for j in range(n):
        As=[]
        for g in bgs[1:3]: As.append(np.array([[0.,1.],[-lay['om'][j]**2*(1+ell**2*g['q']**2),-3*g['h']]])/g['h'])
        matrices[j]=np.eye(6)
        for t in range(2):
            rhs[j,2*t:2*t+2,:2]=old[j]
            for v in range(2):
                matrices[j,2*t:2*t+2,2*v:2*v+2]-=dx*ga[t,v]*As[v]
                rhs[j,2*t+1,2+v]=dx*ga[t,v]*lay['om'][j]**2*bgs[v+1]['q']/bgs[v+1]['h']
        rhs[j,4:6,:2]=old[j]
        for v in range(2):
            matrices[j,4:6,2*v:2*v+2]-=dx*As[v]/2
            rhs[j,5,2+v]=dx*lay['om'][j]**2*bgs[v+1]['q']/bgs[v+1]['h']/2
    RAW['native_matrix']=matrices.copy();RAW['native_rhs']=rhs.copy()
    affine=np.linalg.solve(matrices,rhs);RAW['native_affine']=affine.copy()
    if not np.all(np.isfinite(affine)): raise ArithmeticError('Nonfinite retained native response')
    return affine,matrices,rhs

def metric_increment(before,stages,after,dx):
    h0=before['background']['h'];he=after['background']['h'];a0=before['a'];ae=after['a']
    specs={
      'metric_momentum':('Psi',lambda z:z['Psi_dot']),
      'ordinary_density':('delta_b',lambda z:z['delta_b_dot']),
      'phase_density':('d',lambda z:z['d_dot']),
      'radiation_density':('delta_r',lambda z:z['delta_r_dot']),
    }
    out={}
    for name,(key,source) in specs.items():
        r=dx*sum(source(z)/z['background']['h'] for z in stages)/2;diff=after[key]-before[key]-r
        env=abs(after[key])+abs(before[key])+dx*sum(abs(source(z))/z['background']['h'] for z in stages)/2
        out[name]=float(np.max(abs(diff)/np.maximum(env,FLOOR)))
    for key,source,name in [('S',lambda z:z['background']['B']*z['Phi']+z['pressure']-2*z['background']['r']*z['F'][2]/3,'proper_trace_increment'),('E',lambda z:-3*z['background']['h']*z['pressure']+3*z['background']['B']*z['Psi_dot']-z['background']['q']**2*z['S'],'whole_density_increment')]:
        r=dx*sum(z['a']**3*source(z)/z['background']['h'] for z in stages)/2;diff=ae**3*after[key]-a0**3*before[key]-r
        env=abs(ae**3*after[key])+abs(a0**3*before[key])+dx*sum(z['a']**3*abs(source(z))/z['background']['h'] for z in stages)/2
        out[name]=float(np.max(abs(diff)/np.maximum(env,FLOOR*a0**3)))
    return out

def diagnostic_update(maxima,name,error,step,a):
    value=float(error)
    if not math.isfinite(value): raise ArithmeticError('Nonfinite diagnostic '+name)
    if name not in maxima or value>maxima[name]['error']: maxima[name]=dict(error=value,nstep=step,a=a)

def journal(event,**fields):
    p=BASE/(STEM+'_JOURNAL.jsonl');value=dict(event=event,time=now(),owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**fields)
    with p.open('ab') as f:f.write(encode(value));f.flush();os.fsync(f.fileno())

def gate(name,error,tol):
    er=float(error);return dict(name=name,error=er,tolerance=tol,passed=math.isfinite(er) and er<=tol)

def original(y,ns,moments,g,lay):
    R,Gb,wb,Gp,V,v,p,n,Gr,wr,F2=y;h,q,b,r,w,s=(g[z] for z in ('h','q','b','r','w','cs'))
    psi=R-h*V;phi=psi-2*r*F2/q**2;db=Gb-3*h*V;d=Gp-3*h*V;dr=Gr-4*h*V;ub=V+wb;ur=V+wr;pi=V-v
    moms=moments.copy();moms[0]=dr;moms[1]=4*q*ur/3
    S=g['B']*V+b*wb+4*r*wr/3;E=b*db+r*dr+w*d-q*p;press=r*dr/3+s*w*d
    pdot=-2*h*p-CL*g['Q']**2*q*v;psidot=S-h*phi;Vdot=phi+s*Gp
    ddot=3*psidot-q*q*(V+g['gamma']*v);dbdot=3*psidot-q*q*ub
    drdot=4*psidot-4*q*q*ur/3;urdot=h*ur+phi+dr/4-F2/2
    Sdot=b*phi-3*h*b*ub+4*r*(urdot-4*h*ur)/3-3*h*(1+s)*w*V+w*Vdot
    F2dot=q*(2*moms[1]-3*moms[3])/5;phidot=psidot-2*r*(F2dot-2*h*F2)/q**2
    psiddot=Sdot+g['B']*phi-h*phidot
    normalterms=np.asarray([q*q*psi,3*h*S,b*db,r*dr,w*d,-q*p]);N=normalterms.sum(axis=0);Nenv=abs(normalterms).sum(axis=0)
    trace=np.asarray([psiddot,h*phidot,3*h*psidot,(-2*g['B']+3*h*h)*phi,q*q*(psi-phi)/3,-press]);tr=trace.sum(axis=0);tenv=abs(trace).sum(axis=0)
    Edot=-3*h*b*db+b*dbdot-4*h*r*dr+r*drdot-3*h*(1+s)*w*d+w*ddot+h*q*p-q*pdot
    density_terms=np.asarray([Edot,3*h*(E+press),-3*g['B']*psidot,q*q*S]);momentum_terms=np.asarray([Sdot,3*h*S,-g['B']*phi,-press,2*r*F2/3])
    rate=s*Gp;Qbar=g['Q']/fixed_for_domain['Q0_over_Hstar'];lo=1-1/Qbar;hi=math.sqrt(1+fixed_for_domain['eps'])/Qbar-1
    phase_ratio=np.where(rate>=0,rate/max(hi,np.finfo(float).tiny),-rate/max(lo,np.finfo(float).tiny))
    return dict(a=g['a'],background=g,Psi=psi,Phi=phi,delta_b=db,delta_r=dr,d=d,u_b=ub,u_r=ur,V=V,pi=pi,n_U=n,p=p,Z=lay['weights']@ns[:lay['ns'],0],Zd=lay['weights']@ns[:lay['ns'],1],F=moms,S=S,E=E,pressure=press,normal=N,normal_terms=normalterms,normal_envelope=Nenv,normal_error=abs(N)/np.maximum(Nenv,FLOOR),trace=tr,trace_terms=trace,trace_error=abs(tr)/np.maximum(tenv,FLOOR),density_identity=density_terms.sum(axis=0),density_identity_error=abs(density_terms.sum(axis=0))/np.maximum(abs(density_terms).sum(axis=0),FLOOR),momentum_identity=momentum_terms.sum(axis=0),momentum_identity_error=abs(momentum_terms.sum(axis=0))/np.maximum(abs(momentum_terms).sum(axis=0),FLOOR),Psi_dot=psidot,delta_b_dot=dbdot,d_dot=ddot,delta_r_dot=drdot,S_dot=Sdot,E_dot=Edot,Phi_dot=phidot,phase_rate=rate,phase_margin_lower=lo,phase_margin_upper=hi,phase_fraction=phase_ratio,qV=q*V,qpi=q*pi,qrelative=q*v,linear_inside=(np.maximum.reduce([abs(db),abs(dr),abs(d),abs(psi),abs(phi)])<.01)&(phase_ratio<1),readout=np.asarray([Gb+3*h*wb,b*(Gb+3*h*wb),w*Gp,-q*p,psi+phi,q*q*ub,R,Gb,wb,Gp,V,v,p,n,Gr,wr,F2,S,E,press]))

def complex_moment(p,z):
    z=np.asarray(z,dtype=complex);out=np.zeros_like(z);small=abs(z)<1
    v=z[small];term=np.ones_like(v);ans=np.zeros_like(v)
    for m in range(CFG['series_terms']):
        ans+=term/(m+p+1);term*=-v/(m+1)
    out[small]=ans
    v=z[~small];end=np.exp(-v);value=-np.expm1(-v)/v
    for order in range(1,p+1):value=(order*value-end)/v
    out[~small]=value;return out


def verify_literal_spans():
    parent=(BASE/'cross_u_full_flrw_core_baryon_recovery_v001.py').read_text();ptree=ast.parse(parent)
    witness=(BASE/'cross_u_retarded_radiation_source_operator_witness_v002.py').read_text();wtree=ast.parse(witness)
    own=Path(__file__).read_text();otree=ast.parse(own)
    for name,h in LITERAL_SPANS.items():
        text,tree=(witness,wtree) if name=='complex_moment' else (parent,ptree)
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name);source='\n'.join(text.splitlines()[node.lineno-1:node.end_lineno])+'\n'
        if hashlib.sha256(source.encode()).hexdigest()!=h:raise ValueError('Exact inherited helper span '+name)
        node=next(n for n in otree.body if isinstance(n,ast.FunctionDef) and n.name==name);current='\n'.join(own.splitlines()[node.lineno-1:node.end_lineno])+'\n'
        if name=='original':
            current=current.replace('def original(y,ns,moments,g,lay):','def original(y,ns,ang,g,lay):').replace("moms=moments.copy();moms[0]=dr;moms[1]=4*q*ur/3","moms=np.real(lay['moments']@ang[:lay['na']]);moms[0]=dr;moms[1]=4*q*ur/3")
        if current!=source:raise ValueError('No inherited physical helper change '+name)

def fast_kernels(arguments):
    x=np.asarray(arguments,dtype=float)
    RAW['last_fast_arguments']=x.copy()
    if not np.all(np.isfinite(x)) or np.any(x<0):raise ArithmeticError('Invalid retarded argument')
    flat=x.reshape(-1);small=flat<=10.;j=np.empty((flat.size,9))
    v=flat[small]
    for ell in range(9):
        term=np.ones_like(v);ans=np.zeros_like(v)
        for m in range(52):
            ans+=term;term*=-v*v/(2*(m+1)*(2*ell+2*m+3))
        j[small,ell]=v**ell*ans/math.prod(range(1,2*ell+2,2))
    v=flat[~small];sn,cs=np.sin(v),np.cos(v)
    j[~small,0]=sn/v;j[~small,1]=sn/v**2-cs/v
    for ell in range(1,8):j[~small,ell+1]=(2*ell+1)*j[~small,ell]/v-j[~small,ell-1]
    d1=np.empty((flat.size,7));d2=np.empty_like(d1)
    d1[:,0]=-j[:,1];d2[:,0]=(2*j[:,2]-j[:,0])/3;d2[:,1]=(2*j[:,3]-3*j[:,1])/5
    for ell in range(1,7):d1[:,ell]=(ell*j[:,ell-1]-(ell+1)*j[:,ell+1])/(2*ell+1)
    for ell in range(2,7):
        d2[:,ell]=(ell*(ell-1)*j[:,ell-2]/((2*ell+1)*(2*ell-1))
          -(ell**2/((2*ell+1)*(2*ell-1))+(ell+1)**2/((2*ell+1)*(2*ell+3)))*j[:,ell]
          +(ell+1)*(ell+2)*j[:,ell+2]/((2*ell+1)*(2*ell+3)))
    j=j.reshape(x.shape+(9,));d1=d1.reshape(x.shape+(7,));d2=d2.reshape(x.shape+(7,))
    RAW.update(last_fast_j=j.copy(),last_fast_d1=d1.copy(),last_fast_d2=d2.copy())
    if not all(np.all(np.isfinite(v)) for v in (j,d1,d2)):raise ArithmeticError('Nonfinite accelerated kernel')
    return j,d1,d2

def cardinal_coefficients(fractions):
    coef=np.zeros((4,4))
    for k in range(4):
        poly,denominator=np.asarray([1.]),1.
        for m in range(4):
            if m!=k:poly=np.convolve(poly,np.asarray([-fractions[m],1.]));denominator*=fractions[k]-fractions[m]
        coef[:,k]=poly/denominator
    return coef

def cardinal(coef,u):return sum(np.asarray(u)[...,None]**m*coef[m] for m in range(4))

def source_tensor(theta,target,order):
    width=float(theta[-1]);upper=target/width;coef=cardinal_coefficients(theta/width)
    node,weight=RULES[order];u=upper*(node+1)/2;ww=upper*weight/2
    lagrange=cardinal(coef,u);delta=lagrange.copy();delta[:,0]-=1.
    endpoint=cardinal(coef,np.asarray([upper]))[0];endpoint[0]-=1.
    RAW.update(current_source_u=u.copy(),current_source_weight=ww.copy(),current_source_lagrange=lagrange.copy(),current_source_delta=delta.copy(),current_source_endpoint=endpoint.copy())
    j,d1,d2=fast_kernels(target-width*u);boundary=fast_kernels(np.asarray([0.]))[0][0,:7]
    tensor=np.stack([4*boundary[:,None]*endpoint+4*width*np.einsum('i,il,ij->lj',ww,d1,delta),
        4*width*np.einsum('i,il,ij->lj',ww,d2,lagrange),-4*width*np.einsum('i,il,ij->lj',ww,d1,lagrange)])
    RAW['current_source_tensor']=tensor.copy();return tensor

def accelerated_controls(witness,initial,lay):
    controls=[]
    for record in witness['checkpoint_pairs']:
        label=record['metadata']['label']
        if not (label.startswith('PANEL') or label.startswith('FLUX')):continue
        with np.load(BASE/record['payload'],allow_pickle=False) as z:
            arrays={n:z[n].copy() for n in z.files if n!='metadata'}
        if label.startswith('PANEL'):
            row=record['metadata']['metadata']['row'];width=row['width'];upper=row['upper_fraction'];target=row['target_phase']
            for order in (16,32,64):
                prefix='time'+str(order)+'_';args=arrays[prefix+'arguments'];j,d1,d2=fast_kernels(args)
                compare_control(controls,label+'_kernel'+str(order),np.concatenate([j,d1,d2],axis=-1),np.concatenate([arrays[prefix+'j'],arrays[prefix+'d1'],arrays[prefix+'d2']],axis=-1),1e-11)
                boundary=fast_kernels(np.asarray([target-width*upper]))[0][0,:7]
                compare_control(controls,label+'_boundary'+str(order),boundary,arrays[prefix+'boundary'],1e-11)
                u,ww,L,delta=(arrays[prefix+n] for n in ('u','weight','lagrange','delta_R'))
                endpoint=cardinal(cardinal_coefficients(WITNESS_FRACTIONS),np.asarray([upper]))[0];endpoint[0]-=1.
                tensor=np.stack([4*boundary[:,None]*endpoint+4*width*np.einsum('i,il,ij->lj',ww,d1,delta),4*width*np.einsum('i,il,ij->lj',ww,d2,L),-4*width*np.einsum('i,il,ij->lj',ww,d1,L)])
                compare_control(controls,label+'_tensor'+str(order),tensor,arrays['time'+str(order)+'_tensor'],1e-11)
        else:
            row=record['metadata']['metadata']['row'];width=row['width'];upper=row['upper_fraction'];u=arrays['flux_u'];ww=arrays['flux_weight'];L=arrays['flux_lagrange'];delta=arrays['flux_delta_R']
            j,d1,d2=fast_kernels(width*(upper-u))
            compare_control(controls,label+'_kernel',np.concatenate([j,d1,d2],axis=-1),np.concatenate([arrays['flux_j'],arrays['flux_d1'],arrays['flux_d2']],axis=-1),1e-11)
            tensor=4*width*np.stack([np.einsum('i,i,ij->j',ww,j[:,1],delta),np.einsum('i,i,ij->j',ww,d1[:,1],L),-np.einsum('i,i,ij->j',ww,j[:,1],L)])
            compare_control(controls,label+'_tensor',tensor,arrays['bessel_flux'],1e-11)
    compare_control(controls,'actual_complete_incoming_constant_Y',initial['angular'],np.repeat(initial['core'][8][None,:],len(lay['mu']),axis=0),0.)
    zero=empty_history();nodes,nats,moms,monitor,bgs,checks,source,theta=panel_step(np.zeros((11,2)),np.zeros((48,2,2)),np.zeros((81,2),complex),math.log(AI),(math.log(AF)-math.log(AI))/512,fixed_for_domain,BACKGROUND,lay,zero,np.zeros(2))
    compare_control(controls,'zero_full_coupled_retarded_column',np.asarray([max(float(np.max(abs(v))) for v in (nodes,nats,moms,monitor))]),np.asarray([0.]),0.)
    if len(controls)!=209:raise ValueError('Exact accelerated arithmetic census209')
    return controls

def compare_control(rows,name,actual,expected,tol):
    actual=np.asarray(actual);expected=np.asarray(expected);RAW[name+'_actual']=actual.copy();RAW[name+'_expected']=expected.copy()
    if actual.shape!=expected.shape or not actual.size or not np.all(np.isfinite(actual)) or not np.all(np.isfinite(expected)):raise ArithmeticError('Invalid arithmetic operand '+name)
    diff=actual-expected;ix=tuple(int(v) for v in np.unravel_index(int(np.argmax(abs(diff))),diff.shape));v=complex(diff[ix]);error=float(abs(v))
    rows.append(dict(name=name,error=error,tolerance=tol,passed=error<=tol,first_max_index=list(ix),signed_difference_real=v.real,signed_difference_imaginary=v.imag,shape=list(actual.shape)))

def empty_history():
    return dict(start=np.empty(0),theta=np.empty((0,4)),source=np.empty((0,3,4,2)),end=np.empty(0),delta_end=np.empty((0,2)),**{f'cache{order}':np.empty((0,order,8)) for order in (16,32)})

def append_history(history,start,theta,source):
    width=float(theta[-1]);coef=cardinal_coefficients(theta/width);new=dict(start=np.r_[history['start'],start],theta=np.concatenate([history['theta'],theta[None]]),source=np.concatenate([history['source'],source[None]]),end=np.r_[history['end'],start+width],delta_end=np.vstack([history['delta_end'],source[0,-1]-source[0,0]]))
    for order in (16,32):
        node,weight=RULES[order];u=(node+1)/2;ww=width*weight/2;values=np.einsum('ij,fjc->ifc',cardinal(coef,u),source);values[:,0]-=source[0,0]
        cache=np.column_stack([start+width*u,ww,values.reshape(order,6)])
        new['cache'+str(order)]=np.concatenate([history['cache'+str(order)],cache[None]])
    return new

def history_moments(history,targets,gamma,order):
    targets=np.asarray(targets);j0=fast_kernels(targets)[0][...,:7];value=j0[...,None]*gamma;env=abs(value)
    if not len(history['start']):return value,env
    cache=history['cache'+str(order)];args=targets[:,None,None]-cache[None,:,:,0]
    j,d1,d2=fast_kernels(args);values=cache[:,:,2:].reshape(len(cache),order,3,2);ww=cache[:,:,1]
    # Sources are genuine products sampled at the four actual phase nodes before interpolation.
    terms=4*(d1[...,None]*values[None,:,:,0,None,:]+d2[...,None]*values[None,:,:,1,None,:]-d1[...,None]*values[None,:,:,2,None,:])*ww[None,:,:,None,None]
    boundary=4*fast_kernels(targets[:,None]-history['end'][None,:])[0][...,:7,None]*history['delta_end'][None,:,None,:]
    value+=terms.sum(axis=(1,2))+boundary.sum(axis=1);env+=abs(terms).sum(axis=(1,2))+abs(boundary).sum(axis=1)
    if not np.all(np.isfinite(value)) or not np.all(np.isfinite(env)):raise ArithmeticError('Nonfinite complete historical moments')
    return value,env

def historical_flux(history,left,right,gamma):
    endpoints=fast_kernels(np.asarray([left,right]))[0][:,0];total=(endpoints[0]-endpoints[1])*gamma;envelope=(abs(endpoints[0])+abs(endpoints[1]))*abs(gamma)
    if not len(history['start']):return total,envelope
    cache=history['cache32'];values=cache[:,:,2:].reshape(len(cache),32,3,2);ww=cache[:,:,1]
    j,d1,_=fast_kernels(np.asarray([left,right])[:,None,None]-cache[None,:,:,0])
    delta_j=j[1,:,:,1]-j[0,:,:,1];delta_d=d1[1,:,:,1]-d1[0,:,:,1]
    terms=4*ww[:,:,None]*(delta_j[:,:,None]*(values[:,:,0]-values[:,:,2])+delta_d[:,:,None]*values[:,:,1])
    jb=fast_kernels(np.asarray([left,right])[:,None]-history['end'][None,:])[0][...,0]
    boundary=4*(jb[0]-jb[1])[:,None]*history['delta_end']
    total+=terms.sum(axis=(0,1))+boundary.sum(axis=0)
    envelope+=4*np.sum(ww[:,:,None]*((abs(j[1,:,:,1])+abs(j[0,:,:,1]))[:,:,None]*(abs(values[:,:,0])+abs(values[:,:,2]))+(abs(d1[1,:,:,1])+abs(d1[0,:,:,1]))[:,:,None]*abs(values[:,:,1])),axis=(0,1))
    envelope+=4*np.sum((abs(jb[0])+abs(jb[1]))[:,None]*abs(history['delta_end']),axis=0)
    RAW.update(historical_flux_terms=terms.copy(),historical_flux_boundary=boundary.copy(),historical_flux=total.copy(),historical_flux_envelope=envelope.copy())
    return total,envelope

def current_flux(theta,source):
    width=float(theta[-1]);coef=cardinal_coefficients(theta/width);node,weight=RULES[32];u=(node+1)/2;ww=width*weight/2
    values=np.einsum('ij,fjc->ifc',cardinal(coef,u),source);values[:,0]-=source[0,0]
    j,d1,_=fast_kernels(width*(1-u));terms=4*ww[:,None]*(j[:,1,None]*(values[:,0]-values[:,2])+d1[:,1,None]*values[:,1]);env=4*ww[:,None]*(abs(j[:,1,None])*(abs(values[:,0])+abs(values[:,2]))+abs(d1[:,1,None])*abs(values[:,1]))
    RAW.update(current_flux_values=values.copy(),current_flux_terms=terms.copy());return terms.sum(axis=0),env.sum(axis=0)

def monitor_nodes(incoming,theta,source,lay):
    width=float(theta[-1]);coef=np.einsum('ij,fjc->fic',cardinal_coefficients(theta/width),source);mu=lay['mu'];out=[]
    RAW['monitor_source_coefficients']=coef.copy()
    for target in theta[1:]:
        upper=target/width;mom=np.stack([upper**(p+1)*complex_moment(p,-1j*mu*target) for p in range(4)])
        r=sum(m*coef[0,m,:,None]*mom[m-1] for m in range(1,4));a=-width*mu[None,:]**2*sum(coef[1,m,:,None]*mom[m] for m in range(4));c=1j*width*mu[None,:]*sum(coef[2,m,:,None]*mom[m] for m in range(4))
        out.append(np.exp(-1j*mu*target)[:,None]*(incoming+4*(r+a+c).T))
    result=np.asarray(out);RAW['monitor_nodes']=result.copy();return result

def panel_step(left,native,monitor,x,dx,fixed,background,lay,history,gamma):
    cs=[0.,.5-math.sqrt(3)/6,.5+math.sqrt(3)/6,1.];bgs=[bg(x+c*dx,.1,fixed,background) for c in cs]
    theta=phase_nodes(x,dx,.1,fixed,background,16);theta8=phase_nodes(x,dx,.1,fixed,background,8);RAW.update(phase_theta16=theta.copy(),phase_theta8=theta8.copy())
    if theta.shape!=(4,) or not np.all(np.diff(theta)>0) or theta[-1]>12:raise ArithmeticError('Actual source panel phase cap12 or ordering')
    start=float(history['end'][-1]) if len(history['end']) else 0.;targets=start+theta[1:]
    wholepast,wholeenv=history_moments(history,np.r_[start,targets],gamma,16);past,pastenv=wholepast[1:],wholeenv[1:];tensor32=np.asarray([source_tensor(theta,t,32) for t in theta[1:]]);tensor16=np.asarray([source_tensor(theta,t,16) for t in theta[1:]])
    known=past.copy();maps=np.zeros((3,7,33));leftsources=np.asarray([left[0],bgs[0]['q']*left[4],bgs[0]['cs']*left[3]])
    known+=np.einsum('tfl,fc->tlc',tensor32[:,:,:,0],leftsources)
    for t in range(3):
        for j in range(1,4):
            o=11*(j-1);maps[t,:,o]+=tensor32[t,0,:,j];maps[t,:,o+4]+=tensor32[t,1,:,j]*bgs[j]['q'];maps[t,:,o+3]+=tensor32[t,2,:,j]*bgs[j]['cs']
    RAW.update(low_moment_known=known.copy(),low_moment_map=maps.copy(),current_tensors32=tensor32.copy(),current_tensors16=tensor16.copy())
    aff,nmat,nrhs=native_map(native,bgs,dx,lay,fixed);a=np.zeros((33,33));rhs=np.zeros((33,2));ga=np.asarray([[.25,.25-math.sqrt(3)/6],[.25+math.sqrt(3)/6,.25]]);rates=[rate_matrix(g) for g in bgs[1:3]]
    for t in range(3):
        o=11*t;a[o:o+7,o:o+7]=np.eye(7);rhs[o:o+7]=left[:7];coeff=ga[t] if t<2 else [.5,.5]
        for v in range(2):a[o:o+7,11*v:11*v+11]-=dx*coeff[v]*rates[v]
        a[o+7,o+7]=KBL*bgs[t+1]['q'];a[o+7,o+6]=-1;rhs[o+7]=-CL*(lay['weights']@aff[:lay['ns'],2*t,:2]);zresp=lay['weights']@aff[:lay['ns'],2*t,2:]
        for v in range(2):a[o+7,11*v+7]+=CL*zresp[v]
        for li,ci,factor in [(0,8,1.),(1,9,3/(4*bgs[t+1]['q'])),(2,10,1.)]:a[o+ci,o+ci]=1;a[o+ci]-=factor*maps[t,li];rhs[o+ci]=factor*known[t,li]
    solved,core_error=equilibrated_solve(a,rhs);nodes=solved.reshape(3,11,2);nstage=nodes[:2,7];allnative=aff[:,:,:2]+np.einsum('nij,jc->nic',aff[:,:,2:],nstage);moments=known+np.einsum('tli,ic->tlc',maps,solved)
    source=np.asarray([np.vstack([left[0],nodes[:,0]]),np.asarray([g['q'] for g in bgs])[:,None]*np.vstack([left[4],nodes[:,4]]),np.asarray([g['cs'] for g in bgs])[:,None]*np.vstack([left[3],nodes[:,3]])]);monitorstage=monitor_nodes(monitor,theta,source,lay)
    low16=past+np.einsum('tflj,fjc->tlc',tensor16,source);menv=pastenv+np.einsum('tflj,fjc->tlc',abs(tensor32),abs(source));memory=float(np.max(abs(low16-moments)/np.maximum(menv,FLOOR)))
    nres=np.einsum('nij,njc->nic',nmat,allnative)-(nrhs[:,:,:2]+np.einsum('nij,jc->nic',nrhs[:,:,2:],nstage));nenv=np.einsum('nij,njc->nic',abs(nmat),abs(allnative))+abs(nrhs[:,:,:2])+np.einsum('nij,jc->nic',abs(nrhs[:,:,2:]),abs(nstage));native_error=float(np.max(abs(nres)/np.maximum(nenv,FLOOR)))
    projected=np.asarray([lay['moments']@z[:lay['na']] for z in monitorstage]);projenv=np.asarray([abs(lay['moments'])@abs(z[:lay['na']]) for z in monitorstage]);imag=float(np.max(abs(projected.imag)/np.maximum(projenv,FLOOR)))
    leftlow=np.asarray([left[8],4*bgs[0]['q']*left[9]/3,left[10]]);handoff=float(np.max(abs(wholepast[0,:3]-leftlow)/np.maximum(wholeenv[0,:3]+abs(leftlow),FLOOR)))
    checks=dict(core_rows=core_error,native_rows=native_error,history_endpoint_registration=handoff,phase_quadrature=float(np.max(abs(theta-theta8)/np.maximum(abs(theta),1.))),memory_quadrature=memory,angular_reality=imag)
    RAW.update(core_nodes=nodes.copy(),native_nodes=allnative.copy(),retarded_moments=moments.copy(),actual_source_nodes=source.copy())
    if not all(math.isfinite(v) for v in checks.values()) or not all(np.all(np.isfinite(v)) for v in (nodes,allnative,moments,monitorstage,source)):raise ArithmeticError('Nonfinite full retarded coupled panel')
    return nodes,allnative.reshape(48,3,2,2).transpose(1,0,2,3),moments,monitorstage,bgs,checks,source,theta

def closed_receipt(stem,status):
    rc=json.loads((BASE/(stem+'_RECEIPT.json')).read_text());result=json.loads((BASE/(stem+'_RESULT.json')).read_text())
    if rc['owner']!='root' or rc['status']!=status or result['status']!=status or rc['result_sha256']!=sha(BASE/(stem+'_RESULT.json')):raise ValueError('Exact closed parent '+stem)
    for key in ('input_sha256','output_sha256'):
        for n,h in rc[key].items():
            p=Path(n);seal(p if p.is_absolute() else BASE/p,h)
    return result,rc

def parents():
    for name,h in PINS.items():seal(BASE/name,h)
    seal(BASE/(STEM+'.md'),PROTOCOL_SHA);seal(__file__,SOURCE_SHA)
    old,oldrc=closed_receipt(OLD,'NUMERICAL_FAILED');witness,wrc=closed_receipt(WITNESS,'SOURCE_OPERATOR_WITNESS_COMPLETE')
    if oldrc['pid']!=70938 or oldrc['checkpoint_pairs']!=265 or len(old['controls'])!=137 or len(old['rows'])!=8:raise ValueError('Completed unreclassified full-source recovery')
    if wrc['pid']!=73985 or wrc['checkpoint_pairs']!=36 or len(witness['arithmetic_controls'])!=130 or len(witness['operator_outcomes'])!=81 or not all(r['passed'] for r in witness['arithmetic_controls']+witness['operator_outcomes']):raise ValueError('Actual closed source/flux witness')
    fixed=old['manifest']['fixed'];bgparent=old['background_parent_copied_exactly'];original_manifest=json.loads((BASE/(ORIGINAL+'_MANIFEST.json')).read_text())
    if fixed['eps']!=1e-6 or original_manifest['fixed']!=fixed or old['manifest']['ai']!=AI or old['manifest']['af']!=AF or old['manifest']['amplitude']!=AMP:raise ValueError('Same fiducial effective law/finite preparation')
    if bgparent['manifest']['fixed_parent']!=fixed or any(old['physical_flags'].values()) or any(witness['physical_flags'].values()):raise ValueError('No physical qualification inherited')
    cp=json.loads((BASE/INITIAL_COMMIT).read_text());md=cp['metadata']
    expected=dict(schema=1,trial='FINE_K1_O0',nstep=0,failed=False,payload=INITIAL_PAYLOAD,payload_sha256=sha(BASE/INITIAL_PAYLOAD),metadata=md,owner='root',pid=original_manifest['pid'],source_sha256=original_manifest['source_sha256'],manifest_sha256=sha(BASE/(ORIGINAL+'_MANIFEST.json')))
    if cp!=expected or md['trial']!=dict(arm='FINE',k=.1,na=64,name='FINE_K1_O0',ns=32,nstep=4096,omega=.1) or md['nstep']!=0 or md['maxima']!={} or len(md['frames'])!=1:raise ValueError('Full original two-column CP0 identity')
    if md['input_sha256']!=original_manifest['input_sha256'] or md['physical_flags']!=old['physical_flags']:raise ValueError('Actual initial source and flags')
    return fixed,old,witness,original_manifest,cp

def read_pair(record):
    p=BASE/record['payload'];c=BASE/(p.stem+'_COMMIT.json')
    if sha(p)!=record['payload_sha256'] or json.loads(c.read_text())!=record:raise ValueError('Exact whole committed dictionary')
    meta=record['metadata']
    if record!=dict(schema=1,payload=p.name,payload_sha256=sha(p),metadata=meta) or set(meta)!={'schema','label','failed','owner','pid','source_sha256','manifest_sha256','arrays','metadata','physical_flags'}:raise ValueError('Canonical whole pair dictionary')
    with np.load(p,allow_pickle=False) as z:
        if json.loads(str(z['metadata']))!=meta or set(z.files)!=set(meta['arrays'])|{'metadata'}:raise ValueError('Exact payload schema/metadata')
        arrays={n:z[n].copy() for n in z.files if n!='metadata'}
    for n,v in arrays.items():
        d=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v))))
        if meta['arrays'][n]!=d or (not meta['failed'] and not d['finite']):raise ValueError('Every complete array descriptor '+n)
    return arrays

def checkpoint(label,arrays,metadata,failed=False):
    descriptors={n:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for n,v in arrays.items()}
    if not failed and any(not d['finite'] for d in descriptors.values()):raise ArithmeticError('Nonfinite accepted checkpoint')
    meta=dict(schema=1,label=label,failed=failed,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,arrays=descriptors,metadata=metadata,physical_flags=FLAGS)
    text=encode(meta).decode();meta=json.loads(text);p=BASE/(STEM+'_'+label+'.npz')
    with p.open('xb') as f:np.savez_compressed(f,metadata=np.asarray(text),**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p);record=dict(schema=1,payload=p.name,payload_sha256=sha(p),metadata=meta);ch=write(p.stem+'_COMMIT.json',record)
    reread=read_pair(record)
    if any(not np.array_equal(reread[n],v,equal_nan=True) for n,v in arrays.items()):raise ValueError('Immediate full raw array reread')
    PAIRS.append(record)
    if not (BASE/(STEM+'_RECEIPT.json')).exists():journal('CHECKPOINT',label=label,payload_sha256=sha(p),commit_sha256=ch,failed=failed)
    return record

def final_recheck():
    recheck()
    registered={r['payload'] for r in PAIRS};commits={Path(n).stem+'_COMMIT.json' for n in registered}
    if registered!={p.name for p in BASE.glob(STEM+'_*.npz')} or commits!={p.name for p in BASE.glob(STEM+'_*_COMMIT.json')}:raise ValueError('Every registered raw payload/commit, including ERROR_RAW')
    for record in PAIRS:read_pair(record)


def validate_state(record,arrays,trial):
    meta=record['metadata']['metadata'];step=meta['nstep']
    if set(meta)!={'trial','nstep','x','frames','maxima','solver_history','initial_commit_sha256','columns','physical_flags'} or record['metadata']['label']!=trial['name']+'_CP_'+str(step).zfill(6):raise ValueError('Every accepted identity metadata field')
    nf=step//(trial['nstep']//32)+1
    expected={'core':(11,2),'native':(48,2,2),'monitor':(81,2),'moments':(7,2),'frame_core':(nf,11,2),'frame_native':(nf,48,2,2),'frame_monitor':(nf,81,2),'frame_moments':(nf,7,2),'last_stage_core':((3 if step else 0),11,2),'last_stage_native':((3 if step else 0),48,2,2),'last_stage_monitor':((3 if step else 0),81,2),'last_stage_moments':((3 if step else 0),7,2),'history_start':(step,),'history_theta':(step,4),'history_source':(step,3,4,2),'history_end':(step,),'history_delta_end':(step,2),'history_cache16':(step,16,8),'history_cache32':(step,32,8)}
    if set(arrays)!=set(expected):raise ValueError('Whole accepted state/history inventory')
    for n,shape in expected.items():
        if arrays[n].shape!=shape or arrays[n].dtype!=np.dtype('complex128' if 'monitor' in n else 'float64') or not np.all(np.isfinite(arrays[n])):raise ValueError('Exact accepted state/history '+n)
    if meta['trial']!=trial or [f['nstep'] for f in meta['frames']]!=list(range(0,step+1,trial['nstep']//32)) or len(meta['solver_history'])!=step:raise ValueError('Exact stage/frame/solver prefix')
    if any(v['trial']!=trial['name'] or v['nstep']!=i+1 or len(v['corrections'])>CORRECTION_CAP for i,v in enumerate(meta['solver_history'])):raise ValueError('Every original33 solve history step')
    if meta['physical_flags']!=FLAGS or meta['columns']!=['metric','common_velocity'] or meta['initial_commit_sha256']!=PINS[INITIAL_COMMIT]:raise ValueError('Unchanged physical preparation metadata')
    for n in ('core','native','monitor','moments'):
        if not np.array_equal(arrays[n],arrays['frame_'+n][-1]):raise ValueError('Endpoint/frame identity')
        if step and not np.array_equal(arrays[n],arrays['last_stage_'+n][-1]):raise ValueError('Endpoint/full-stage identity')
    if step:
        if arrays['history_start'][0]!=0. or not np.array_equal(arrays['history_start'][1:],arrays['history_end'][:-1]) or not np.array_equal(arrays['history_end'],arrays['history_start']+arrays['history_theta'][:,-1]) or not np.all(np.diff(arrays['history_theta'],axis=1)>0):raise ValueError('Complete physical phase origin/contiguous history')
        if not np.array_equal(arrays['history_source'][1:,0,0],arrays['history_source'][:-1,0,-1]):raise ValueError('Continuous curvature history anchors')
    if meta['x']!=math.log(AI)+step*((math.log(AF)-math.log(AI))/trial['nstep']):raise ValueError('Exact physical log-a endpoint')


def lineage(manifest):
    events=[json.loads(s) for s in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    if not events or events[0]['event']!='OWNER_START' or events[0]['pid']!=manifest['pid']:raise ValueError('Original owner epoch')
    expected=['ARITHMETIC']+[t['name']+'_CP_'+str(s).zfill(6) for t in TRIALS for s in range(0,t['nstep']+1,t['nstep']//32)];labels=[];epoch=None;previous={};PAIRS.clear()
    for ix,event in enumerate(events):
        if event['owner']!='root' or event['source_sha256']!=SOURCE_SHA or event['manifest_sha256']!=MANIFEST_SHA:raise ValueError('Exact journal source/owner identity')
        if event['event'] in ('OWNER_START','OWNER_RESUME'):
            if event['event']=='OWNER_START' and ix:raise ValueError('Repeated original owner')
            epoch=event['pid'];continue
        if event['event']!='CHECKPOINT' or event['pid']!=epoch or event['failed']:raise ValueError('Only authenticated unfailed prefix resumable')
        label=event['label'];p=BASE/(STEM+'_'+label+'.npz');c=BASE/(p.stem+'_COMMIT.json');record=json.loads(c.read_text());meta=record['metadata']
        if sha(p)!=event['payload_sha256'] or sha(c)!=event['commit_sha256'] or meta['label']!=label or meta['source_sha256']!=SOURCE_SHA or meta['manifest_sha256']!=MANIFEST_SHA or meta['pid']!=epoch or meta['owner']!='root' or meta['schema']!=1 or meta['failed']:raise ValueError('Full immutable committed owner binding')
        OUTPUTS[str(p.resolve())]=sha(p);OUTPUTS[str(c.resolve())]=sha(c);arrays=read_pair(record);PAIRS.append(record);labels.append(label)
        if label!='ARITHMETIC':
            t=next((t for t in TRIALS if label.startswith(t['name']+'_CP_')),None)
            if t is None:raise ValueError('Unknown trial prefix')
            validate_state(record,arrays,t);m=meta['metadata'];old=previous.get(t['name'])
            if old is not None:
                om,oa=old
                if m['frames'][:len(om['frames'])]!=om['frames'] or m['solver_history'][:len(om['solver_history'])]!=om['solver_history']:raise ValueError('Immutable entire metadata history')
                for n in ('core','native','monitor','moments'):
                    if not np.array_equal(arrays['frame_'+n][:len(om['frames'])],oa['frame_'+n]):raise ValueError('Immutable full frame prefix')
                for n in ('start','theta','source','end','delta_end','cache16','cache32'):
                    if not np.array_equal(arrays['history_'+n][:om['nstep']],oa['history_'+n]):raise ValueError('No reset/truncation/reconstruction of completed radiation history')
                if any(m['maxima'][n]['error']<v['error'] for n,v in om['maxima'].items()):raise ValueError('Nondecreasing diagnostic maxima')
            previous[t['name']]=(m,arrays)
    if labels!=expected[:len(labels)]:raise ValueError('One ordered bounded scientific prefix')
    final_recheck();return previous


def admit_initial(cp,lay):
    with np.load(BASE/INITIAL_PAYLOAD,allow_pickle=False) as z:
        arrays={n:z[n].copy() for n in z.files if n!='metadata'};md=json.loads(str(z['metadata']))
    RAW.update({'incoming_'+n:v for n,v in arrays.items()})
    if md!=cp['metadata'] or set(arrays)!={'core','native','angular','frame_core','frame_native','frame_angular','last_stage_core','last_stage_native','last_stage_angular'}:raise ValueError('Every original initial array')
    if arrays['core'].shape!=(11,2) or arrays['core'].dtype!=np.dtype('float64') or arrays['native'].shape!=(48,2,2) or arrays['native'].dtype!=np.dtype('float64') or arrays['angular'].shape!=(81,2) or arrays['angular'].dtype!=np.dtype('complex128'):raise ValueError('Actual two-column native/angular chart')
    if not all(np.all(np.isfinite(v)) for v in arrays.values()):raise ArithmeticError('Nonfinite incoming preparation')
    if md['layout']!=canonical(dict(nodes=lay['nodes'],weights=lay['weights'],mu=lay['mu'],weight_sum=lay['weight_sum'])) or md['x']!=math.log(AI):raise ValueError('Same48 modes/81 angles and physical origin')
    for n in ('core','native','angular'):
        if not np.array_equal(arrays[n],arrays['frame_'+n][0]) or len(arrays['last_stage_'+n])!=0:raise ValueError('Full original empty stage/first frame')
    return arrays


def run_trial(t,initial,lay,resume=None):
    global CONTEXT
    x0=math.log(AI);dx=(math.log(AF)-x0)/t['nstep'];gamma=initial['core'][8].copy();core=initial['core'].copy();native=initial['native'].copy();monitor=initial['angular'].copy();moments=np.zeros((7,2));moments[0]=gamma;history=empty_history();frames=[];fc=[];fn=[];fa=[];fm=[];maxima={};start=0;last=(np.empty((0,11,2)),np.empty((0,48,2,2)),np.empty((0,81,2),complex),np.empty((0,7,2)));CORE_HISTORY.clear()
    if resume is not None:
        meta,a=resume;start=meta['nstep'];core,native,monitor,moments=(a[n].copy() for n in ('core','native','monitor','moments'));history={n:a['history_'+n].copy() for n in empty_history()};frames=meta['frames'];maxima=meta['maxima'];fc=list(a['frame_core']);fn=list(a['frame_native']);fa=list(a['frame_monitor']);fm=list(a['frame_moments']);last=tuple(a['last_stage_'+n].copy() for n in ('core','native','monitor','moments'));CORE_HISTORY.extend(meta['solver_history'])
    first=original(core,native,moments,bg(x0+start*dx,.1,fixed_for_domain,BACKGROUND),lay)
    seedmom=np.zeros((7,2));seedmom[0]=gamma;seed=original(initial['core'],initial['native'],seedmom,bg(x0,.1,fixed_for_domain,BACKGROUND),lay);pn0=AI**3*seed['normal'];pe0=AI**3*seed['normal_envelope']
    def save(step):
        arrays=dict(core=core,native=native,monitor=monitor,moments=moments,frame_core=np.asarray(fc),frame_native=np.asarray(fn),frame_monitor=np.asarray(fa),frame_moments=np.asarray(fm),**{'last_stage_'+n:v for n,v in zip(('core','native','monitor','moments'),last)},**{'history_'+n:v for n,v in history.items()})
        metadata=dict(trial=t,nstep=step,x=x0+step*dx,frames=frames,maxima=maxima,solver_history=CORE_HISTORY,initial_commit_sha256=PINS[INITIAL_COMMIT],columns=['metric','common_velocity'],physical_flags=FLAGS)
        record=checkpoint(t['name']+'_CP_'+str(step).zfill(6),arrays,metadata);validate_state(record,arrays,t);return record
    if start==0 and resume is None:
        frames.append(dict(nstep=0,registration_a=AI,**canonical(first)));fc.append(core.copy());fn.append(native.copy());fa.append(monitor.copy());fm.append(moments.copy());save(0)
    for i in range(start,t['nstep']):
        RAW.clear();CONTEXT=dict(trial=t['name'],nstep=i+1,accepted_nstep=i,x=x0+i*dx,accepted_frames=frames)
        RAW.update(accepted_core=core.copy(),accepted_native=native.copy(),accepted_monitor=monitor.copy(),accepted_moments=moments.copy(),**{'accepted_history_'+n:v for n,v in history.items()})
        nodes,nats,low,mon,bgs,checks,source,theta=panel_step(core,native,monitor,x0+i*dx,dx,fixed_for_domain,BACKGROUND,lay,history,gamma)
        snaps=[original(nodes[j],nats[j],low[j],bgs[j+1],lay) for j in range(3)];after=snaps[-1]
        for n,v in checks.items():diagnostic_update(maxima,n,v,i+1,after['a'])
        for snap in snaps:
            for n in ('normal_error','trace_error','density_identity_error','momentum_identity_error'):diagnostic_update(maxima,n,float(np.max(snap[n])),i+1,snap['a'])
        for n,v in metric_increment(first,snaps[:2],after,dx).items():diagnostic_update(maxima,n,v,i+1,after['a'])
        phase0=float(history['end'][-1]) if len(history['end']) else 0.;phase1=phase0+float(theta[-1]);hf,he=historical_flux(history,phase0,phase1,gamma);cf,ce=current_flux(theta,source);flux=hf+cf
        balance=after['delta_r']-first['delta_r']-4*(after['Psi']-first['Psi'])+flux;env=abs(after['delta_r'])+abs(first['delta_r'])+4*(abs(after['Psi'])+abs(first['Psi']))+he+ce
        RAW.update(independent_flux=flux.copy(),independent_balance=balance.copy(),independent_balance_envelope=env.copy())
        diagnostic_update(maxima,'sourced_radiation_flux',float(np.max(abs(balance)/np.maximum(env,FLOOR))),i+1,after['a'])
        pn=after['a']**3*after['normal']-pn0;pe=after['a']**3*after['normal_envelope']+pe0;diagnostic_update(maxima,'normal_propagation',float(np.max(abs(pn)/np.maximum(pe,FLOOR*AI**3))),i+1,after['a'])
        newhistory=append_history(history,phase0,theta,source)
        if (i+1)%(t['nstep']//32)==0:
            v32,e32=history_moments(newhistory,np.asarray([phase1]),gamma,32);v16,e16=history_moments(newhistory,np.asarray([phase1]),gamma,16);diagnostic_update(maxima,'sampled_history_quadrature',float(np.max(abs(v32-v16)/np.maximum(e32+e16,FLOOR))),i+1,after['a'])
            RAW.update(history_readout32=v32.copy(),history_readout16=v16.copy(),history_endpoint_difference=(v32[0]-low[-1]).copy())
        core,native,monitor,moments=nodes[-1].copy(),nats[-1].copy(),mon[-1].copy(),low[-1].copy();history=newhistory;first=after;last=(nodes,nats,mon,low)
        if (i+1)%(t['nstep']//32)==0:
            j=(i+1)//(t['nstep']//32);frames.append(dict(nstep=i+1,registration_a=math.exp(x0+j*(math.log(AF)-x0)/32),**canonical(after)));fc.append(core.copy());fn.append(native.copy());fa.append(monitor.copy());fm.append(moments.copy());save(i+1);print(t['name'],i+1,'/',t['nstep'],flush=True)
    return dict(trial=t,frames=frames,maxima=maxima,solver_history=list(CORE_HISTORY),terminal_checkpoint=STEM+'_'+t['name']+'_CP_'+str(t['nstep']).zfill(6)+'.npz',history_panel_count=len(history['start']),total_phase=float(history['end'][-1]))


def comparisons(rows):
    coarse,fine=rows;result=[]
    if [f['registration_a'] for f in coarse['frames']]!=[f['registration_a'] for f in fine['frames']]:raise ValueError('Same33 j/32 physical sample registrations')
    for column in range(2):
        for field,count in [('readout',20),('F',7)]:
            for n in range(count):
                a=np.asarray([f[field][n][column] for f in coarse['frames']]);b=np.asarray([f[field][n][column] for f in fine['frames']]);scale=max(float(np.max(abs(a))),FLOOR);diff=abs(b-a)/scale;ix=int(np.argmax(diff))
                result.append(dict(name=field+'_'+str(n)+'_column_'+str(column),error=float(diff[ix]),signed_difference=float(b[ix]-a[ix]),normalization=scale,first_max_frame=ix,registration_a=coarse['frames'][ix]['registration_a'],coarse_actual_a=coarse['frames'][ix]['a'],fine_actual_a=fine['frames'][ix]['a'],tolerance=STATE_TOL,passed=bool(diff[ix]<=STATE_TOL)))
    with np.load(BASE/coarse['terminal_checkpoint'],allow_pickle=False) as a,np.load(BASE/fine['terminal_checkpoint'],allow_pickle=False) as b:
        for field,sl in [('native',slice(-16,None)),('monitor',slice(-17,None))]:
            av=a['frame_'+field][:,sl];bv=b['frame_'+field][:,sl];scale=np.maximum(np.max(abs(av),axis=0),FLOOR);error=float(np.max(abs(bv-av)/scale));result.append(dict(name=field+'_passive_probe',error=error,tolerance=STATE_TOL,passed=math.isfinite(error) and error<=STATE_TOL))
    if len(result)!=56:raise ValueError('Original common-state comparison census56')
    return result


def main(resume=False):
    global np,SOURCE_SHA,MANIFEST_SHA,fixed_for_domain,BACKGROUND,RULES,WITNESS_FRACTIONS,CONTEXT
    if AUTHOR_GUARD:raise RuntimeError('Guarded root-only coupled retarded-history draft')
    tick=time.monotonic();SOURCE_SHA=sha(__file__);fixed,old,witness,original_manifest,cp=parents();verify_literal_spans();fixed_for_domain=fixed
    if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_ERROR.json','_RECEIPT.json')):raise FileExistsError('Closed/error namespace is never automatically rerun')
    if bool(list(BASE.glob(STEM+'_*')))!=bool(resume):raise FileExistsError('Fresh prefix or explicit authenticated --resume only')
    manifest=dict(schema=1,owner='root',pid=os.getpid(),started=now(),source_sha256=SOURCE_SHA,input_sha256=INPUTS,action='S_cross V003 Eq5/7-9',fixed=fixed,ai=AI,af=AF,amplitude=AMP,trials=TRIALS,initial_checkpoint=cp,method='Complete phase-cubic anchored Bessel memory; simultaneous original33 current rows; constant full incoming Y; retained characteristic probes',history_order=16,current_order=32,independent_flux_order=32,sampled_history_order=32,prospective_tolerances=dict(state=STATE_TOL,increment=INCREMENT_TOL,normal=NORMAL_TOL,rows=ROW_TOL,floor=FLOOR),phase_cap=12,arithmetic_count=209,trajectory_predicate_count=96,checkpoint_pair_count=67,numpy_version=original_manifest['numpy_version'],physical_flags=FLAGS)
    rows=[];controls=[]
    try:
        if not resume:
            MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest)
            with (BASE/(STEM+'_JOURNAL.jsonl')).open('xb'):pass
            journal('OWNER_START')
        else:
            p=BASE/(STEM+'_MANIFEST.json');saved=json.loads(p.read_text());MANIFEST_SHA=sha(p);OUTPUTS[str(p.resolve())]=MANIFEST_SHA
            for key in set(manifest)-{'pid','started'}:
                if saved[key]!=canonical(manifest[key]):raise ValueError('Exact interrupted scientific manifest '+key)
            manifest=saved
        for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[n]='1'
        import numpy as np
        if np.__version__!=manifest['numpy_version']:raise ValueError('Unchanged NumPy registration')
        BACKGROUND=load_background();RULES={n:np.polynomial.legendre.leggauss(n) for n in (16,32)};lay=layout(32,64,.1);initial=admit_initial(cp,lay)
        geometry=next(r for r in witness['checkpoint_pairs'] if r['metadata']['label']=='GEOMETRY');ga=read_pair(geometry);WITNESS_FRACTIONS=ga['fractions']
        if resume:
            previous=lineage(manifest);arith=PAIRS[0]['metadata']['metadata']['controls'];controls.extend(arith)
            if len(arith)!=209 or not all(v['passed'] for v in arith):raise ValueError('Only passed accelerated arithmetic prefix resumable')
            journal('OWNER_RESUME')
        else:
            CONTEXT=dict(stage='accelerated_arithmetic');CORE_HISTORY.clear();arith=accelerated_controls(witness,initial,lay);controls.extend(arith);checkpoint('ARITHMETIC',dict(RAW),dict(controls=arith,closed_source_witness_result_sha256=PINS[WITNESS+'_RESULT.json']))
            if not all(v['passed'] for v in arith):raise ArithmeticError('Accelerated arithmetic failed unchanged1e-11 before evolution')
            previous={}
        for t in TRIALS:
            incoming=previous.get(t['name'])
            if incoming is not None and incoming[0]['nstep']==t['nstep']:
                m=incoming[0];rows.append(dict(trial=t,frames=m['frames'],maxima=m['maxima'],solver_history=m['solver_history'],terminal_checkpoint=STEM+'_'+t['name']+'_CP_'+str(t['nstep']).zfill(6)+'.npz',history_panel_count=t['nstep'],total_phase=float(incoming[1]['history_end'][-1])));continue
            rows.append(run_trial(t,initial,lay,incoming))
        for row in rows:
            if len(row['maxima'])!=19 or len(row['frames'])!=33 or len(row['solver_history'])!=row['trial']['nstep']:raise ValueError('Complete diagnostic/frame/core census')
            for n,d in row['maxima'].items():
                tolerance=NORMAL_TOL if n in ('normal_error','normal_propagation') else INCREMENT_TOL if n in ('metric_momentum','ordinary_density','phase_density','radiation_density','proper_trace_increment','whole_density_increment','sourced_radiation_flux','sampled_history_quadrature','history_endpoint_registration') else ROW_TOL
                controls.append(gate(row['trial']['name']+'_'+n,d['error'],tolerance))
            controls.append(gate(row['trial']['name']+'_preparation_normal',max(row['frames'][0]['normal_error']),ROW_TOL))
        compared=comparisons(rows);controls.extend(compared);lineage(manifest)
        if len(PAIRS)!=67 or len(controls)!=305:raise ValueError('Two bounded trials/67 complete pairs/305 predicates')
        for t in TRIALS:
            first=next(r for r in PAIRS if r['metadata']['label']==t['name']+'_CP_000000');a=read_pair(first)
            if not all(np.array_equal(a[n],initial[o]) for n,o in [('core','core'),('native','native'),('monitor','angular')]):raise ValueError('Original full CP0 preparation exact copy')
        parents();final_recheck();status='NUMERICAL_PASS' if all(v['passed'] for v in controls) else 'NUMERICAL_FAILED'
        result=dict(status=status,manifest=manifest,rows=rows,controls=controls,comparisons=compared,checkpoint_pairs=PAIRS,parent_full_source_controls_copied_exactly=old['controls'],original_parent_controls_copied_exactly=old['original_parent_controls_copied_exactly'],original_parent_comparisons_copied_exactly=old['original_parent_comparisons_copied_exactly'],original_parent_registration_copied_exactly=old['original_parent_registration_copied_exactly'],parent_physical_flags_copied_exactly=old['physical_flags'],source_witness_arithmetic_copied_exactly=witness['arithmetic_controls'],source_witness_outcomes_copied_exactly=witness['operator_outcomes'],source_witness_physical_flags_copied_exactly=witness['physical_flags'],physical_flags=FLAGS,elapsed_seconds=time.monotonic()-tick,scope='Bounded512/1024 coupled full-history numerical branch only; no original failed gate is promoted; no prepared-universe/continuum/native-inertia/physical-growth/lensing qualification')
        rh=write(STEM+'_RESULT.json',result);report=['# Coupled retarded radiation history V001','',status,'',f"{sum(v['passed'] for v in controls)}/305 prospective predicates passed.",'','Original two-log-a-node radiation balance and independent complete-history flux are distinct readouts.','', '| trial | normal | original radiation increment | independent flux | trace | history16/32 sampled |','|---|---:|---:|---:|---:|---:|']
        for row in rows:
            m=row['maxima'];report.append('| '+row['trial']['name']+' | '+' | '.join(str(m[n]['error']) for n in ('normal_error','radiation_density','sourced_radiation_flux','trace_error','sampled_history_quadrature'))+' |')
        raw=('\n'.join(report)+'\n').encode();p=BASE/(STEM+'_REPORT.md')
        with p.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        p.chmod(0o444)
        if p.read_bytes()!=raw:raise IOError('Report expected-byte reread')
        OUTPUTS[str(p.resolve())]=sha(p);final_recheck();journal('OWNER_CLOSE',status=status,result_sha256=rh);jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);OUTPUTS[str(jp.resolve())]=sha(jp)
        rc=dict(status=status,owner='root',pid=os.getpid(),started=manifest['started'],closed=now(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,result_sha256=rh,input_sha256=INPUTS,output_sha256={str(Path(p).relative_to(BASE)):h for p,h in OUTPUTS.items()},checkpoint_pairs=67,predicate_count=305,physical_flags=FLAGS);write(STEM+'_RECEIPT.json',rc)
        if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=canonical(rc):raise ValueError('Canonical closed receipt reread')
        parents();final_recheck();print(status,rh,flush=True);return 0 if status=='NUMERICAL_PASS' else 3
    except Exception as exc:
        p=BASE/(STEM+'_RECEIPT.json');protected=sha(p) if p.exists() else None
        if protected is not None:OUTPUTS[str(p.resolve())]=protected
        if 'np' in globals() and RAW:checkpoint('ERROR_RAW',dict(RAW),dict(context=CONTEXT,type=type(exc).__name__,message=str(exc),controls=controls),True)
        error=dict(status='ERROR',owner='root',pid=os.getpid(),time=now(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,type=type(exc).__name__,message=str(exc),context=CONTEXT,protected_existing_receipt_sha256=protected,input_sha256=INPUTS,output_sha256={str(Path(p).relative_to(BASE)):h for p,h in OUTPUTS.items()},checkpoint_pairs=PAIRS,controls=controls,physical_flags=FLAGS);write(STEM+'_ERROR.json',error)
        jp=BASE/(STEM+'_JOURNAL.jsonl')
        if protected is None and jp.exists():journal('OWNER_ERROR',type=type(exc).__name__,message=str(exc));jp.chmod(0o444)
        if jp.exists():OUTPUTS[str(jp.resolve())]=sha(jp)
        if protected is None:
            rc=dict(error,closed=now(),output_sha256={str(Path(p).relative_to(BASE)):h for p,h in OUTPUTS.items()});write(STEM+'_RECEIPT.json',rc)
            if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=canonical(rc):raise ValueError('Canonical ERROR receipt reread')
        elif sha(p)!=protected:raise ValueError('Protected prior receipt changed')
        parents();final_recheck();raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    if not args.root_owned:raise RuntimeError('Root-owned numerical execution only')
    raise SystemExit(main(args.resume))
