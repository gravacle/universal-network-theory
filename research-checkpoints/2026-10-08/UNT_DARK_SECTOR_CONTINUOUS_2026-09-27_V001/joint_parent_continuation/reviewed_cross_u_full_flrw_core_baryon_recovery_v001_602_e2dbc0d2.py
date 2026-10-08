"""Guarded root-only SAME S_cross finite-slice full-source test; never imported by authors."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, ast, hashlib, json, math, os, time

BASE = Path(__file__).resolve().parent
STEM = 'CROSS_U_FULL_FLRW_CORE_BARYON_RECOVERY_V001'
AUTHOR_GUARD = True
KB, C, CP = .02, 1.98, 299792.458
KBL, CL = KB/2, C/2
AI, AF, AMP = .01, 1., 1e-8
ARMS = [('FINE',4096,32,64)]
KS, OMEGAS = [.01,.1], [.1,1.,10.,100.]
STRIDE, FRAME_COUNT = 128, 33
STATE_TOL, INCREMENT_TOL, NORMAL_TOL, ROW_TOL = 1e-3, 1e-6, 1e-6, 2e-11
FLOOR = 1e-13
PINS = {'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_AND_FINITE_SLICE_TEST_V001.md': 'c81fa7ed6961f5f0620bbb48dd133ef474543765131ceb738bdcf676f9b9a986', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'CROSS_U_RETARDED_RESPONSE_AND_BACKGROUND_EQUIVALENCE_V001.md': '78d369efb4efe4bab1f3885c2b11e37959e0860f449e839fa9d447da829ab9f6', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json': 'e9f7b2070e762920cb3548ccbe11c5f46efd1a262065ba594afaca6635acc35f', 'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json': 'df514792bf703b6ce6b9e4c2a64e2ac19c407dffa0f14acf9bb9f75b6acc64e6', 'CROSS_U_NGC3198_NONLINEAR_DISK_V001_MANIFEST.json': '65cb05b3aba084bde5fe75015e0a546c0c116a5a7906e7f647a5f2232c206683', 'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001_MANIFEST.json': 'a88e33ac8391f2d9eed1570358040447f088047e64417e4c9120396cc771b2f6', '../FRONTIER_UPDATE_V227.md': '19b15f06a5c9db0e5d36f95fde22a0be6271cf65a75d1681d5579ec4d7de5c0b', 'constrained_u_shared_eps_ngc_pantheon_v001.py': '03809b3c3798563725450bb4b7cf8c91654525ad874b6bc38e85da7c8cd22c52', 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_V001.md': '4f2611f0fda44d326034aba5c38bcf532dc69e912f5f3d1d135f335975b5a5a6', 'cross_u_full_flrw_source_constraint_v001_REVIEWED_GUARDED_499.py': '3e0899e007fcbb9567ac96da14b5ba1d6f3f81152eef1212f1ddba9de7dff176', 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_V001_REVIEWED_31.md': 'ede19e1499be29a44c598ade672f1ca4b1cde438bfd4584eb906492ebdf93fd6', 'cross_u_full_flrw_source_constraint_v001_REVIEWED_GUARDED_519.py': '0e0d31e75dd387f54a94e306758370b40357aeb711de2aeb914b25794671b061', 'CROSS_U_FULL_FLRW_SOURCE_CONSTRAINT_V001_REVIEWED_33.md': '6e146b64c3196e4500707a9ebdf6c43bdb764e1189219fe0fae41724b1dc7404', 'cross_u_full_flrw_source_constraint_v001.py': '8e2860917a75c44ada5be0df18ac43809dc7fe454846b3787d8a3d3017d1e5c1', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_MANIFEST.json': 'fba438e9df2246cbefa27f0b5226e41f435de8632e035d0660ed8f5bf3f6b77d', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_ERROR.json': 'e128383f1c9a1725ec4480c3ad7e87b99d09a3b699a5bd40bac2414e6df9bb03', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_RECEIPT.json': 'bf5c48b986549b92593ff7d20a4fb05ee5c7b75cbec878ee80c2342db29daafe', 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001_RESULT.json': '919bd3091cdda1f7616bd13f63a03c18d66cfe64a7ce68fdceb23f4cd0ab2d5f', 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001_REPORT.md': '166c2b3e95122a5619dca581424be3f8e48291f2b3e45c59af7227ac9cdee755', 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001_RECEIPT.json': 'd70f6b6f6974522b896b0a4f389454c730c55ee55221096b199aa16003ed7082', 'cross_u_full_flrw_saved_aggregate_recovery_v001.py': 'ef099255955378bd56bad2c7952be118e2c232d0a3aa1a0462633750995f27cd', 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001.md': 'c6d9d9605c8c3eea7abc62109afdc5bdea77d6c6d0200ff422907806637ca630', 'CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001_RESULT.json': 'd5ab3156ab96435d4acd3fe993fc50cb22734f187ba53e313bb8f0fe00f9bfc0', 'CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001_REPORT.md': 'a2ff0a53df0e5ace2e61db373fe5e4407b89b34ded026f5fbeba789581972d52', 'CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001_RECEIPT.json': 'ac833b0ef54ab77bc7b1c63ea00f7ff4f07332a92dfd13936498b7c06e03da5f', 'CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001_MANIFEST.json': 'b45de32cdf04ea8a2b358bd2087012adb6806b54fff6a4fdd1acb1f759229370', 'cross_u_full_flrw_core_row_diagnostic_v001.py': '7f701443b0601ee47ef996133fbe1bd3a09535fbb6b9fc3c7a27705b5eb183b8', 'CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001.md': '7fedd8de7ae5c5162897d3c603b66f637c6a6976e416f1410f6f3c33535bd151', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_000000.npz': '9121d9919cada1ed35c784956f62feab3787be6cb3ca60e15e95dd9a1be47706', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_000000_COMMIT.json': '854bb57a25d5e43b675e315d1e3a8c9d62eb64f0571b089d44191fe13f01303b', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_000000.npz': 'd1f9ff150ebe1e68a49a39e5dfd2ecec4d03938b2b57f21c98745ac9a3666870', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_000000_COMMIT.json': '03a5f67d8167fff6e32498dfe274b788d6e3bb9979dc79f0b3676663674354e4', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_000000.npz': 'f6ccf6d072914ff74d56bd6e29ee1b0a292107b9d91497262abec3dfb3d45e9e', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_000000_COMMIT.json': '03eb925d7c2540834c91302d5cd7bbab29cd6205248beb52cb4e9f5d55af7ba0', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_000000.npz': 'a837e33bd0e8ea3e4cb9cb35f84dd740dfbf780d23d76a03c9b00a1082a964d0', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_000000_COMMIT.json': 'd596692560259a8e409f3d45ef2089a0ce424f6d5d97dc93e909b531c7f30f14', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000.npz': '72aa7178724affa2a06c97e1f3990872670ed85df0cce720beca2b21f6c05879', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000_COMMIT.json': '43a762492edf95003e26c12c11ec3d34dead48b67b1da5760411607187537d95', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_000000.npz': '715d7801d48457d606ab35a565439e03d07f2d99e4ab16bae9da1f825a2689f8', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_000000_COMMIT.json': 'b6f0da8f1ab116fb483276f7135151f247d57f2c4f469a2a3c6d9c5531f0becc', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_000000.npz': 'a56397991f375473a4138f7b2509ff804de45d76c63ff28e3e0cae8867e537aa', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_000000_COMMIT.json': 'e2200cfc881cf5576b99c8b51465805d19f6ea6f04b5e8bed45e52cec589de4c', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_000000.npz': 'e50cadc8c5d7aa025b3c2164bd573f4c6d1b157c3179d8d23cbd46cb39de987f', 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_000000_COMMIT.json': '8814695e59d066d9450257c94bc2299a8bd39569ca87fed0360635f6c38e8c02'}
PROTOCOL_SHA = 'ed7a1fb352dbd919f6ff2f6fd1b7ec3240e62f74f644e76286cb65a03860615b'
ORIGINAL = 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001'
AGGREGATE = 'CROSS_U_FULL_FLRW_SAVED_AGGREGATE_RECOVERY_V001'
CORE_PARENT = 'CROSS_U_FULL_FLRW_CORE_ROW_DIAGNOSTIC_V001'
TRIALS = [{'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, {'arm': 'FINE', 'k': 0.01, 'na': 64, 'name': 'FINE_K0_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}, {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O0', 'ns': 32, 'nstep': 4096, 'omega': 0.1}, {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O1', 'ns': 32, 'nstep': 4096, 'omega': 1.0}, {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O2', 'ns': 32, 'nstep': 4096, 'omega': 10.0}, {'arm': 'FINE', 'k': 0.1, 'na': 64, 'name': 'FINE_K1_O3', 'ns': 32, 'nstep': 4096, 'omega': 100.0}]
INITIALS = {'FINE_K0_O0': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O0_CP_000000_COMMIT.json'}, 'FINE_K0_O1': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O1_CP_000000_COMMIT.json'}, 'FINE_K0_O2': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O2_CP_000000_COMMIT.json'}, 'FINE_K0_O3': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K0_O3_CP_000000_COMMIT.json'}, 'FINE_K1_O0': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O0_CP_000000_COMMIT.json'}, 'FINE_K1_O1': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O1_CP_000000_COMMIT.json'}, 'FINE_K1_O2': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O2_CP_000000_COMMIT.json'}, 'FINE_K1_O3': {'payload': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_000000.npz', 'commit': 'CROSS_U_FULL_FLRW_FINITE_SLICE_V001_FINE_K1_O3_CP_000000_COMMIT.json'}}
CORRECTION_CAP = 6
CORE_HISTORY = []
ZERO_RECORD = None

BG_SPAN = '8881f1df923d053d1d4b7ce06bfe4a50e856a62b49a25546a8d7e7a0d9f12bf2'
INPUTS, OUTPUTS = {}, {}
SOURCE_SHA = MANIFEST_SHA = None
CONTEXT = {}
RAW = {}

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

def closed_parent():
    result=json.loads((BASE/'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json').read_text())
    receipt=json.loads((BASE/'CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RECEIPT.json').read_text())
    if receipt['result_sha256']!=PINS['CONSTRAINED_U_SHARED_EPS_NGC_PANTHEON_V001_RESULT.json'] or receipt['status']!='NUMERICAL_PASS' or receipt['owner']!='root': raise ValueError('Closed background parent')
    for n,h in receipt['output_sha256'].items(): seal(BASE/n,h)
    for n,h in result['manifest']['input_sha256'].items(): seal(BASE/n,h)
    if receipt['source_sha256']!=PINS['constrained_u_shared_eps_ngc_pantheon_v001.py']: raise ValueError('Actual literal background source')
    fixed=result['manifest']['fixed_parent']
    if fixed['eps']!=1e-6 or len(result['rows'])!=4: raise ValueError('Unchanged fiducial and four preserved EPS')
    disk=json.loads((BASE/'CROSS_U_NGC3198_NONLINEAR_DISK_V001_MANIFEST.json').read_text())
    if disk['fixed']!=fixed: raise ValueError('Shared physical background')
    horizon=json.loads((BASE/'CONSTRAINED_U_K10_DERIVED_FULL_COMMON_CONTINUATION_V001_MANIFEST.json').read_text())
    if horizon['omega']!=OMEGAS: raise ValueError('Conditional frequency labels')
    return fixed,result

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

def radiation_weights(theta,lay,order):
    u,w=np.polynomial.legendre.leggauss(order);mu=lay['mu'];result=[]
    for target in theta[1:]:
        s=target*(u+1)/2;basis=[]
        for j in range(4):
            p=np.ones_like(s)
            for m in range(4):
                if m!=j: p*= (s-theta[m])/(theta[j]-theta[m])
            basis.append(p)
        kern=np.exp(-1j*mu[:,None]*(target-s[None,:]))
        result.append(kern@(np.asarray(basis).T*(w*target/2)[:,None]))
    return np.asarray(result)

def radiation_map(theta,weights,left,angular,bgs,lay,label):
    known=[];maps=[];mu=lay['mu'];R0=left[0]
    for t in range(3):
        a=np.exp(-1j*mu*theta[t+1])[:,None]*angular-4*R0[None,:]
        m=np.zeros((len(mu),33),complex);m[:,11*t]=4
        RAW['radiation_known'+label+'_target'+str(t)]=a;RAW['radiation_map'+label+'_target'+str(t)]=m
        for j in range(4):
            integ=weights[t,:,j]
            a+=(-1j*4*mu*integ)[:,None]*(-R0)[None,:]
            if j==0:
                a+=(-4*mu**2*integ)[:,None]*(bgs[0]['q']*left[4])[None,:]
                a+=(1j*4*mu*integ)[:,None]*(bgs[0]['cs']*left[3])[None,:]
                a+=(-1j*4*mu*integ)[:,None]*R0[None,:]
            else:
                o=11*(j-1);m[:,o]+= -1j*4*mu*integ
                m[:,o+4]+= -4*mu**2*integ*bgs[j]['q']
                m[:,o+3]+= 1j*4*mu*integ*bgs[j]['cs']
        known.append(a);maps.append(m)
    return np.asarray(known),np.asarray(maps)

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

def panel_step(left,native,angular,x,dx,k,fixed,background,lay):
    cs=[0.,.5-math.sqrt(3)/6,.5+math.sqrt(3)/6,1.];bgs=[bg(x+c*dx,k,fixed,background) for c in cs]
    theta=phase_nodes(x,dx,k,fixed,background,16);RAW['phase_theta16']=theta.copy()
    theta8=phase_nodes(x,dx,k,fixed,background,8);RAW['phase_theta8']=theta8.copy()
    if theta[-1]>12: raise ArithmeticError('Declared source-panel phase cap12 exceeded')
    w16=radiation_weights(theta,lay,16);RAW['radiation_weights16']=w16.copy()
    w32=radiation_weights(theta,lay,32);RAW['radiation_weights32']=w32.copy()
    known,maps=radiation_map(theta,w32,left,angular,bgs,lay,'32');RAW['radiation_known32']=known;RAW['radiation_maps32']=maps;lowk=[];lowm=[]
    for t in range(3):
        mm=lay['moments'][:3];lowk.append(np.real(mm@known[t,:lay['na']]))
        lowm.append(np.real(mm@maps[t,:lay['na']]))
        RAW['low_moment_known_target'+str(t)]=lowk[-1];RAW['low_moment_map_target'+str(t)]=lowm[-1]
    aff,nmat,nrhs=native_map(native,bgs,dx,lay,fixed);a=np.zeros((33,33));rhs=np.zeros((33,2));ga=np.array([[.25,.25-math.sqrt(3)/6],[.25+math.sqrt(3)/6,.25]])
    rates=[rate_matrix(g) for g in bgs[1:3]]
    for t in range(3):
        o=11*t;a[o:o+7,o:o+7]=np.eye(7);rhs[o:o+7]=left[:7]
        coeff=ga[t] if t<2 else [.5,.5]
        for v in range(2): a[o:o+7,11*v:11*v+11]-=dx*coeff[v]*rates[v]
        a[o+7,o+7]=KBL*bgs[t+1]['q'];a[o+7,o+6]=-1
        zknown=lay['weights']@aff[:lay['ns'],2*t,:2];zresp=lay['weights']@aff[:lay['ns'],2*t,2:]
        rhs[o+7]=-CL*zknown
        for v in range(2): a[o+7,11*v+7]+=CL*zresp[v]
        for li,ci,factor in [(0,8,1.),(1,9,3/(4*bgs[t+1]['q'])),(2,10,1.)]:
            a[o+ci,o+ci]=1;a[o+ci]-=factor*lowm[t][li];rhs[o+ci]=factor*lowk[t][li]
    solved,core_error=equilibrated_solve(a,rhs);nodes=solved.reshape(3,11,2)
    nstage=np.vstack([nodes[0,7],nodes[1,7]])
    allnative=aff[:,:,:2]+np.einsum('nij,jc->nic',aff[:,:,2:],nstage)
    nang=known+np.einsum('tmi,ic->tmc',maps,solved)
    RAW['core_nodes']=nodes.copy();RAW['native_nodes']=allnative.copy();RAW['angular_nodes']=nang.copy()
    ratesv=[rates[t]@nodes[t] for t in range(2)]
    nres=np.einsum('nij,njc->nic',nmat,allnative)-(nrhs[:,:,:2]+np.einsum('nij,jc->nic',nrhs[:,:,2:],nstage))
    nenv=np.einsum('nij,njc->nic',abs(nmat),abs(allnative))+abs(nrhs[:,:,:2])+np.einsum('nij,jc->nic',abs(nrhs[:,:,2:]),abs(nstage))
    native_error=float(np.max(abs(nres)/np.maximum(nenv,FLOOR)))
    known16,maps16=radiation_map(theta,w16,left,angular,bgs,lay,'16');RAW['radiation_known16']=known16;RAW['radiation_maps16']=maps16
    y16=known16+np.einsum('tmi,ic->tmc',maps16,solved);RAW['angular_nodes16']=y16
    yenv=abs(known)+np.einsum('tmi,ic->tmc',abs(maps),abs(solved))
    optical=float(np.max(abs(theta-theta8)/np.maximum(abs(theta),1.)))
    memory=float(np.max(abs(y16-nang)/np.maximum(yenv,FLOOR)))
    moments=np.asarray([lay['moments']@nang[t,:lay['na']] for t in range(3)])
    momentenv=np.asarray([abs(lay['moments'])@abs(nang[t,:lay['na']]) for t in range(3)])
    imag=float(np.max(abs(np.imag(moments))/np.maximum(momentenv,FLOOR)))
    if not all(math.isfinite(z) for z in (core_error,native_error,optical,memory,imag)) or not all(np.all(np.isfinite(y)) for y in (nodes,allnative,nang)): raise ArithmeticError('Nonfinite full coupled panel')
    diagnostics=dict(core_rows=core_error,native_rows=native_error,phase_quadrature=optical,memory_quadrature=memory,angular_reality=imag)
    return nodes,allnative.reshape(len(lay['om']),3,2,2).transpose(1,0,2,3),nang,bgs,diagnostics

def original(y,ns,ang,g,lay):
    R,Gb,wb,Gp,V,v,p,n,Gr,wr,F2=y;h,q,b,r,w,s=(g[z] for z in ('h','q','b','r','w','cs'))
    psi=R-h*V;phi=psi-2*r*F2/q**2;db=Gb-3*h*V;d=Gp-3*h*V;dr=Gr-4*h*V;ub=V+wb;ur=V+wr;pi=V-v
    moms=np.real(lay['moments']@ang[:lay['na']]);moms[0]=dr;moms[1]=4*q*ur/3
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

def preparation(g,lay):
    psi=np.asarray([AMP,0.]);V=np.asarray([0.,AMP/g['h']]);d=-g['q']**2*psi/g['B']-3*g['h']*V
    core=np.zeros((11,2));core[0]=psi+g['h']*V;core[1]=d+3*g['h']*V;core[3]=core[1];core[4]=V;core[8]=4*core[1]/3
    nat=np.zeros((len(lay['om']),2,2));angular=np.repeat(core[8][None,:],len(lay['mu']),axis=0).astype(complex)
    return core,nat,angular

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

def validate_arrays(arrays,meta,lay,failed=False):
    stages=0 if meta['nstep']==0 else 3
    expected={'core':(11,2),'native':(len(lay['om']),2,2),'angular':(len(lay['mu']),2),'frame_core':(len(meta['frames']),11,2),'frame_native':(len(meta['frames']),len(lay['om']),2,2),'frame_angular':(len(meta['frames']),len(lay['mu']),2),'last_stage_core':(stages,11,2),'last_stage_native':(stages,len(lay['om']),2,2),'last_stage_angular':(stages,len(lay['mu']),2)}
    rawfields={n:d for n,d in meta.get('raw_failure_arrays',{}).items()}
    if set(arrays)!=set(expected)|set(rawfields) or (rawfields and not failed): raise ValueError('Exact full array inventory')
    for n,shape in expected.items():
        a=arrays[n]
        if a.shape!=shape or a.dtype!=(np.dtype('complex128') if 'angular' in n else np.dtype('float64')): raise ValueError('Full shape/dtype '+n)
        if not failed and not np.all(np.isfinite(a)): raise ValueError('Nonfinite accepted checkpoint '+n)
    for n,d in rawfields.items():
        a=arrays[n]
        if list(a.shape)!=d['shape'] or str(a.dtype)!=d['dtype'] or bool(np.all(np.isfinite(a)))!=d['finite']:raise ValueError('Raw failed-array descriptor '+n)
    if len(meta['frames']):
        for n in ('core','native','angular'):
            if meta['frames'][-1]['nstep']==meta['nstep'] and not np.array_equal(arrays[n],arrays['frame_'+n][-1],equal_nan=failed): raise ValueError('Last frame/full state identity')
    if stages:
        for n in ('core','native','angular'):
            if not np.array_equal(arrays[n],arrays['last_stage_'+n][-1],equal_nan=failed):raise ValueError('Last complete stage/endpoint identity')
    canonical(meta)

def save_checkpoint(trial,step,arrays,meta,lay,failed=False):
    recheck();validate_arrays(arrays,meta,lay,failed);text=encode(meta).decode();p=BASE/(STEM+'_'+trial+'_CP_'+str(step).zfill(6)+('_FAILED' if failed else '')+'.npz')
    with p.open('xb') as f:np.savez_compressed(f,metadata=np.asarray(text),**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p)
    cp=dict(schema=1,trial=trial,nstep=step,failed=failed,payload=p.name,payload_sha256=sha(p),metadata=json.loads(text),owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA)
    cn=p.stem+'_COMMIT.json';ch=write(cn,cp)
    with np.load(p,allow_pickle=False) as z:
        if json.loads(str(z['metadata']))!=cp['metadata']: raise ValueError('Immediate full metadata reread')
        reread={n:z[n] for n in arrays};validate_arrays(reread,cp['metadata'],lay,failed)
        if not all(np.array_equal(reread[n],a,equal_nan=failed) for n,a in arrays.items()): raise ValueError('Immediate every-array reread')
    journal('CHECKPOINT',trial=trial,nstep=step,failed=failed,payload_sha256=sha(p),commit_sha256=ch)
    return cp

def lineage(trials,manifest):
    journal_path=BASE/(STEM+'_JOURNAL.jsonl');events=[json.loads(s) for s in journal_path.read_text().splitlines()]
    if not events or events[0]['event']!='OWNER_START' or events[0]['pid']!=manifest['pid']:raise ValueError('Missing exact original root owner')
    expected=[(t['name'],s) for t in trials for s in range(0,t['nstep']+1,STRIDE)];actual=[];epoch=None;previous=None
    for index,e in enumerate(events):
        if e['owner']!='root' or type(e['pid']) is not int or e['pid']<=0 or e['source_sha256']!=SOURCE_SHA or e['manifest_sha256']!=MANIFEST_SHA:raise ValueError('Exact root/source/manifest history')
        if e['event']=='OWNER_START' and index!=0:raise ValueError('Duplicate original owner epoch')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):epoch=e['pid']
        elif e['event']=='CHECKPOINT':
            if e['pid']!=epoch or e['failed']:raise ValueError('Failed or mismatched owner prefix')
            trial=next((t for t in trials if t['name']==e['trial']),None)
            if trial is None:raise ValueError('Unknown trial')
            lay=layout(trial['ns'],trial['na'],trial['omega']);p=BASE/(STEM+'_'+trial['name']+'_CP_'+str(e['nstep']).zfill(6)+'.npz');c=BASE/(p.stem+'_COMMIT.json');cp=json.loads(c.read_text())
            expectedcp=dict(schema=1,trial=trial['name'],nstep=e['nstep'],failed=False,payload=p.name,payload_sha256=sha(p),metadata=cp['metadata'],owner='root',pid=epoch,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA)
            if sha(p)!=e['payload_sha256'] or sha(c)!=e['commit_sha256'] or cp!=expectedcp:raise ValueError('Entire exact committed prefix dictionary')
            OUTPUTS[str(p.resolve())]=sha(p);OUTPUTS[str(c.resolve())]=sha(c)
            with np.load(p,allow_pickle=False) as z:
                if json.loads(str(z['metadata']))!=cp['metadata']:raise ValueError('Saved prefix canonical metadata')
                arrays={n:z[n].copy() for n in z.files if n!='metadata'};validate_arrays(arrays,cp['metadata'],lay)
            expectedframes=list(range(0,e['nstep']+1,trial['nstep']//32))
            meta=cp['metadata'];expectedx=math.log(AI)+e['nstep']*((math.log(AF)-math.log(AI))/trial['nstep'])
            expectedlayout=canonical(dict(nodes=lay['nodes'],weights=lay['weights'],mu=lay['mu'],weight_sum=lay['weight_sum']))
            expectedkeys={'schema','trial','nstep','x','frames','maxima','input_sha256','layout','columns','physical_flags','solver_history'}
            if set(meta)!=expectedkeys or meta['schema']!=1 or meta['nstep']!=e['nstep'] or meta['x']!=expectedx or meta['layout']!=expectedlayout or meta['columns']!=['metric','common_velocity'] or meta['physical_flags']!=manifest['physical_flags']:raise ValueError('Every exact accepted metadata identity field')
            if [f['nstep'] for f in meta['frames']]!=expectedframes or meta['trial']!=trial or meta['input_sha256']!=INPUTS:raise ValueError('Entire ordered frame/input/trial prefix')
            if previous is not None and previous[0]==trial['name']:
                oldmeta,oldarrays=previous[1:];nold=len(oldmeta['frames'])
                if cp['metadata']['frames'][:nold]!=oldmeta['frames']:raise ValueError('Immutable entire snapshot metadata prefix')
                for field in ('frame_core','frame_native','frame_angular'):
                    if not np.array_equal(arrays[field][:nold],oldarrays[field]):raise ValueError('Immutable entire full-state snapshot prefix')
                if cp['metadata']['nstep']<=oldmeta['nstep'] or any(cp['metadata']['maxima'][n]['error']<v['error'] for n,v in oldmeta['maxima'].items()):raise ValueError('Ordered steps/nondecreasing diagnostics')
            history=meta['solver_history']
            if len(history)!=e['nstep'] or any(v['trial']!=trial['name'] or v['nstep']!=i+1 or len(v['corrections'])>CORRECTION_CAP for i,v in enumerate(history)):raise ValueError('Every ordered same-matrix solver history')
            if previous is not None and previous[0]==trial['name'] and history[:len(previous[1]['solver_history'])]!=previous[1]['solver_history']:raise ValueError('Immutable solver history prefix')
            previous=(trial['name'],cp['metadata'],arrays)
            actual.append((trial['name'],e['nstep']))
        else:raise ValueError('Closed or unknown journal event')
    registered={STEM+'_'+name+'_CP_'+str(step).zfill(6)+'.npz' for name,step in actual}
    registered_commits={Path(name).stem+'_COMMIT.json' for name in registered}
    registered.add(STEM+'_ZERO_CONTROL.npz');registered_commits.add(STEM+'_ZERO_CONTROL_COMMIT.json')
    if actual!=expected[:len(actual)] or registered_commits!={p.name for p in BASE.glob(STEM+'_*_COMMIT.json')} or registered!={p.name for p in BASE.glob(STEM+'_*.npz')}:raise ValueError('Exact global registered pair/payload sets; preserve and refuse every orphan including ERROR_RAW')
    return actual

def run_trial(t,fixed,background,admitted,resume=None):
    global CONTEXT
    lay=layout(t['ns'],t['na'],t['omega']);x0=math.log(AI);dx=(math.log(AF)-x0)/t['nstep'];g=bg(x0,t['k'],fixed,background)
    CORE_HISTORY.clear();core,native,angular=(admitted[n].copy() for n in ('core','native','angular'));frames=[];fc=[];fn=[];fa=[];maxima={};start=0
    last_core=np.empty((0,11,2));last_native=np.empty((0,len(lay['om']),2,2));last_angular=np.empty((0,len(lay['mu']),2),complex)
    if resume is not None:
        meta,arrays=resume;start=meta['nstep'];core=arrays['core'];native=arrays['native'];angular=arrays['angular'];frames=meta['frames'];maxima=meta['maxima'];fc=list(arrays['frame_core']);fn=list(arrays['frame_native']);fa=list(arrays['frame_angular']);CORE_HISTORY.extend(meta['solver_history'])
        last_core=arrays['last_stage_core'];last_native=arrays['last_stage_native'];last_angular=arrays['last_stage_angular']
    first=original(core,native,angular,bg(x0+start*dx,t['k'],fixed,background),lay)
    initial=tuple(admitted[n] for n in ('core','native','angular'));seed_snapshot=original(*initial,g,lay)
    propagated_initial=AI**3*seed_snapshot['normal'];propagated_envelope=AI**3*seed_snapshot['normal_envelope']
    def checkpoint(i,failed=False):
        arrays=dict(core=core,native=native,angular=angular,frame_core=np.asarray(fc,dtype=float).reshape(len(fc),11,2),frame_native=np.asarray(fn,dtype=float).reshape(len(fn),len(lay['om']),2,2),frame_angular=np.asarray(fa,dtype=complex).reshape(len(fa),len(lay['mu']),2),last_stage_core=last_core,last_stage_native=last_native,last_stage_angular=last_angular)
        meta=dict(schema=1,trial=t,nstep=i,x=x0+i*dx,frames=frames,maxima=maxima,input_sha256=INPUTS,layout=dict(nodes=lay['nodes'],weights=lay['weights'],mu=lay['mu'],weight_sum=lay['weight_sum']),columns=['metric','common_velocity'],solver_history=CORE_HISTORY,physical_flags={n:False for n in ['primordial_state','nonlinear_clock','native_normalization','mode_inertia','observed_growth','observed_lensing']})
        if failed:
            arrays.update({'raw_'+n:v for n,v in RAW.items()});meta['raw_failure_arrays']={n:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for n,v in arrays.items() if n.startswith('raw_')}
            meta['attempted_context']=CONTEXT
        return save_checkpoint(t['name'],i,arrays,meta,lay,failed)
    if start==0:
        frames.append(dict(nstep=0,**canonical(first)));fc.append(core.copy());fn.append(native.copy());fa.append(angular.copy());checkpoint(0)
    for i in range(start,t['nstep']):
        RAW.clear()
        accepted_step=i
        CONTEXT=dict(trial=t['name'],nstep=i+1,x=x0+i*dx)
        try:
            nodes,nats,angs,bgs,checks=panel_step(core,native,angular,x0+i*dx,dx,t['k'],fixed,background,lay)
            ss=[original(nodes[j],nats[j],angs[j],bgs[j+1],lay) for j in range(3)];after=ss[-1]
            for n,v in checks.items():diagnostic_update(maxima,n,v,i+1,after['a'])
            for j,snap in enumerate(ss):
                for n in ('normal_error','trace_error','density_identity_error','momentum_identity_error'):diagnostic_update(maxima,n,float(np.max(snap[n])),i+1,snap['a'])
            for n,v in metric_increment(first,ss[:2],after,dx).items():diagnostic_update(maxima,n,v,i+1,after['a'])
            pn=after['a']**3*after['normal']-propagated_initial;pe=after['a']**3*after['normal_envelope']+propagated_envelope
            diagnostic_update(maxima,'normal_propagation',float(np.max(abs(pn)/np.maximum(pe,FLOOR*AI**3))),i+1,after['a'])
            core,native,angular=nodes[-1].copy(),nats[-1].copy(),angs[-1].copy();first=after
            last_core=nodes.copy();last_native=nats.copy();last_angular=angs.copy()
            accepted_step=i+1
            if (i+1)%(t['nstep']//32)==0:frames.append(dict(nstep=i+1,**canonical(after)));fc.append(core.copy());fn.append(native.copy());fa.append(angular.copy())
            if (i+1)%STRIDE==0:checkpoint(i+1);print(t['name'],i+1,'/',t['nstep'],flush=True)
        except Exception:
            checkpoint(accepted_step,True);raise
    return dict(trial=t,frames=frames,maxima=maxima,solver_history=list(CORE_HISTORY),original_initial_checkpoint=INITIALS[t['name']],terminal_checkpoint=STEM+'_'+t['name']+'_CP_'+str(t['nstep']).zfill(6)+'.npz')

def compare_rows(a,b):
    controls=[]
    if [f['a'] for f in a['frames']]!=[f['a'] for f in b['frames']]:raise ValueError('Exact common physical frame abscissae')
    for column in range(2):
        for n in range(20):
            v=np.asarray([r['readout'][n][column] for r in a['frames']]);w=np.asarray([r['readout'][n][column] for r in b['frames']]);scale=max(float(np.max(abs(v))),FLOOR)
            diff=abs(w-v)/scale;ix=int(np.argmax(diff));controls.append(dict(name='readout_'+str(n)+'_column_'+str(column),error=float(diff[ix]),signed_difference=float(w[ix]-v[ix]),normalization=scale,first_max_frame=ix,a=a['frames'][ix]['a'],tolerance=STATE_TOL,passed=bool(diff[ix]<=STATE_TOL)))
        for n in range(7):
            v=np.asarray([r['F'][n][column] for r in a['frames']]);w=np.asarray([r['F'][n][column] for r in b['frames']]);scale=max(float(np.max(abs(v))),FLOOR)
            diff=abs(w-v)/scale;ix=int(np.argmax(diff));controls.append(dict(name='angular_moment_'+str(n)+'_column_'+str(column),error=float(diff[ix]),signed_difference=float(w[ix]-v[ix]),normalization=scale,first_max_frame=ix,a=a['frames'][ix]['a'],tolerance=STATE_TOL,passed=bool(diff[ix]<=STATE_TOL)))
    for n,indices in [('native_probe',slice(-16,None)),('angular_probe',slice(-17,None))]:
        field='native' if n=='native_probe' else 'angular';pa=BASE/a['terminal_checkpoint'];pb=BASE/b['terminal_checkpoint']
        with np.load(pa,allow_pickle=False) as za,np.load(pb,allow_pickle=False) as zb:
            av=za['frame_'+field][:,indices];bv=zb['frame_'+field][:,indices]
            scale=np.maximum(np.max(abs(av),axis=0),FLOOR);error=float(np.max(abs(bv-av)/scale))
        controls.append(dict(name=n,error=error,tolerance=STATE_TOL,passed=math.isfinite(error) and error<=STATE_TOL,scope='Fixed common passive frequencies/angles; complete feedback arrays retained separately'))
    return controls

def gate(name,error,tol):
    er=float(error);return dict(name=name,error=er,tolerance=tol,passed=math.isfinite(er) and er<=tol)

def recovery_parent():
    for name,h in PINS.items():seal(BASE/name,h)
    seal(BASE/(STEM+'.md'),PROTOCOL_SHA);seal(__file__,SOURCE_SHA)
    fixed,background_parent=closed_parent()
    receipts={st:json.loads((BASE/(st+'_RECEIPT.json')).read_text()) for st in (ORIGINAL,AGGREGATE,CORE_PARENT)}
    for rc in receipts.values():
        for kind in ('input_sha256','output_sha256'):
            for name,h in rc[kind].items():seal(BASE/name,h)
    error=json.loads((BASE/(ORIGINAL+'_ERROR.json')).read_text());parent=json.loads((BASE/(AGGREGATE+'_RESULT.json')).read_text());core=json.loads((BASE/(CORE_PARENT+'_RESULT.json')).read_text())
    old_manifest=json.loads((BASE/(ORIGINAL+'_MANIFEST.json')).read_text());orcp=receipts[ORIGINAL];arcp=receipts[AGGREGATE];crcp=receipts[CORE_PARENT]
    if orcp['status']!='ERROR' or orcp['pid']!=65046 or orcp['message']!='Exact common physical frame abscissae':raise ValueError('Authentic original natural ERROR')
    if parent['original_error_copied_exactly']!=error or parent['original_error_receipt_copied_exactly']!=orcp or parent['manifest']!=old_manifest:raise ValueError('Original immutable state/error ancestry')
    if arcp['status']!=parent['status'] or parent['status']!='RECOVERED_NUMERICAL_FAILED' or arcp['result_sha256']!=PINS[AGGREGATE+'_RESULT.json']:raise ValueError('Recovered failed parent')
    if len(parent['rows'])!=32 or len(parent['checkpoint_pairs'])!=928 or len(parent['controls'])!=1889 or parent['available_predicate_count']!=1888 or parent['unverified_predicate_count']!=1 or parent['invalid_original_diagnostic_count']!=64:raise ValueError('Preserved full logical/available/withdrawn census')
    if len(parent['sample_registration_controls'])!=792 or len(parent['comparisons'])!=24:raise ValueError('Preserved registration/failed comparison census')
    if core['status']!=crcp['status'] or core['status']!='DIAGNOSTIC_COMPLETE' or crcp['checkpoint_pairs']!=32 or len(core['cases'])!=16 or crcp['result_sha256']!=PINS[CORE_PARENT+'_RESULT.json']:raise ValueError('Actual bounded core evidence')
    if core['parent_controls_copied_exactly']!=parent['controls'] or any(not v['final_row']['gate_passed'] for v in core['cases']):raise ValueError('Actual same-matrix witness/control dispositions')
    if old_manifest['fixed']!=fixed or old_manifest['ai']!=AI or old_manifest['af']!=AF or old_manifest['amplitude']!=AMP or [r['trial'] for r in parent['rows'] if r['trial']['arm']=='FINE']!=TRIALS:raise ValueError('Exact original physical fixture')
    if any(parent['qualification'].values()) or any(parent['physical_flags'].values()) or core['qualification']!=parent['physical_flags']:raise ValueError('No qualification transfer')
    for trial in TRIALS:
        files=INITIALS[trial['name']];cp=json.loads((BASE/files['commit']).read_text());md=cp['metadata']
        expected=dict(schema=1,trial=trial['name'],nstep=0,failed=False,payload=files['payload'],payload_sha256=PINS[files['payload']],metadata=md,owner='root',pid=old_manifest['pid'],source_sha256=PINS['cross_u_full_flrw_source_constraint_v001.py'],manifest_sha256=PINS[ORIGINAL+'_MANIFEST.json'])
        if cp!=expected or md['trial']!=trial or md['nstep']!=0 or md['input_sha256']!=old_manifest['input_sha256'] or md['maxima']!={} or len(md['frames'])!=1 or md['physical_flags']!=old_manifest['physical_flags']:raise ValueError('Exact immutable original initial binding')
    return fixed,background_parent,parent,core,old_manifest

def admit_initial(t,old_manifest):
    files=INITIALS[t['name']];cp=json.loads((BASE/files['commit']).read_text());meta=cp['metadata'];lay=layout(t['ns'],t['na'],t['omega'])
    with np.load(BASE/files['payload'],allow_pickle=False) as n:
        for key in n.files:
            if key!='metadata':RAW['admitted_'+key]=n[key].copy()
        if json.loads(str(n['metadata']))!=meta:raise ValueError('Original initial metadata reread')
        arrays={key:n[key].copy() for key in n.files if key!='metadata'}
    validate_arrays(arrays,meta,lay)
    if meta['x']!=math.log(AI) or meta['columns']!=['metric','common_velocity'] or meta['layout']!=canonical(dict(nodes=lay['nodes'],weights=lay['weights'],mu=lay['mu'],weight_sum=lay['weight_sum'])):raise ValueError('Same initial chart/modes/angles')
    if meta['frames'][0]['nstep']!=0 or meta['frames'][0]['a']!=math.exp(meta['x']):raise ValueError('Original finite initial frame')
    return arrays

def zero_checkpoint(arrays,control,history):
    name=STEM+'_ZERO_CONTROL.npz';p=BASE/name
    metadata=canonical(dict(schema=1,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,control=control,solver_history=history,arrays={n:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for n,v in arrays.items()}))
    text=encode(metadata).decode()
    with p.open('xb') as f:np.savez_compressed(f,metadata=np.asarray(text),**arrays);f.flush();os.fsync(f.fileno())
    p.chmod(0o444);OUTPUTS[str(p.resolve())]=sha(p);rec=dict(schema=1,payload=name,payload_sha256=sha(p),metadata=json.loads(text));write(STEM+'_ZERO_CONTROL_COMMIT.json',rec)
    reread_zero();return rec

def reread_zero():
    name=STEM+'_ZERO_CONTROL.npz';cp=json.loads((BASE/(STEM+'_ZERO_CONTROL_COMMIT.json')).read_text());md=cp['metadata'];p=BASE/name
    for current in (p,BASE/(STEM+'_ZERO_CONTROL_COMMIT.json')):
        previous=OUTPUTS.get(str(current.resolve()))
        if previous is not None and sha(current)!=previous:raise ValueError('Protected zero-control bytes changed')
    if cp!=dict(schema=1,payload=name,payload_sha256=sha(p),metadata=md) or md['source_sha256']!=SOURCE_SHA or md['manifest_sha256']!=MANIFEST_SHA or md['owner']!='root':raise ValueError('Exact zero-column pair identity')
    with np.load(p,allow_pickle=False) as n:
        if json.loads(str(n['metadata']))!=md or set(n.files)!=set(md['arrays'])|{'metadata'}:raise ValueError('Complete zero-column scratch schema')
        for key,d in md['arrays'].items():
            v=n[key]
            if d!=dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) or not d['finite']:raise ValueError('Zero-column array descriptor')
    OUTPUTS[str(p.resolve())]=sha(p);OUTPUTS[str((BASE/(STEM+'_ZERO_CONTROL_COMMIT.json')).resolve())]=sha(BASE/(STEM+'_ZERO_CONTROL_COMMIT.json'));return cp

def verify_initial_copies():
    for t in TRIALS:
        p=BASE/(STEM+'_'+t['name']+'_CP_000000.npz');q=BASE/INITIALS[t['name']]['payload']
        with np.load(p,allow_pickle=False) as own,np.load(q,allow_pickle=False) as old:
            for key in ('core','native','angular','frame_core','frame_native','frame_angular','last_stage_core','last_stage_native','last_stage_angular'):
                if not np.array_equal(own[key],old[key]):raise ValueError('No initial state or preparation reset '+t['name']+' '+key)


def main(resume=False):
    global np,SOURCE_SHA,MANIFEST_SHA,fixed_for_domain,ZERO_RECORD,CONTEXT
    if AUTHOR_GUARD:raise RuntimeError('Guarded prospective recovery; root release only after full review')
    tick=time.monotonic();SOURCE_SHA=sha(__file__);fixed,background_parent,parent,core_evidence,old_manifest=recovery_parent();fixed_for_domain=fixed
    if any((BASE/(STEM+suffix)).exists() for suffix in ('_RESULT.json','_RECEIPT.json','_ERROR.json')):raise FileExistsError('Naturally closed or failed namespace preserved; no automatic retry')
    prefix=list(BASE.glob(STEM+'_*'))
    if prefix and not resume:raise FileExistsError('Existing prefix; explicit authenticated --resume only')
    if resume and not prefix:raise FileNotFoundError('No interrupted prefix to resume')
    manifest=dict(schema=1,action='S_cross V003 Eq5/7-9',source_sha256=SOURCE_SHA,input_sha256=INPUTS,fixed=fixed,ai=AI,af=AF,amplitude=AMP,trials=TRIALS,admitted_original_initials=INITIALS,prospective_tolerances=dict(state=STATE_TOL,increment=INCREMENT_TOL,normal=NORMAL_TOL,rows=ROW_TOL,floor=FLOOR),method='Original stable-chart/full-source Gauss panels; original33-row residual corrections and complete+bPhi diagnostic only',correction_cap=CORRECTION_CAP,owner='root',pid=os.getpid(),started=now(),numpy_version=old_manifest['numpy_version'],physical_flags=old_manifest['physical_flags'])
    rows=[];controls=[]
    try:
        if not resume:
            MANIFEST_SHA=write(STEM+'_MANIFEST.json',manifest)
            with (BASE/(STEM+'_JOURNAL.jsonl')).open('xb'):pass
            journal('OWNER_START')
        else:
            p=BASE/(STEM+'_MANIFEST.json');saved=json.loads(p.read_text());MANIFEST_SHA=sha(p);OUTPUTS[str(p.resolve())]=MANIFEST_SHA
            for key in ('source_sha256','input_sha256','fixed','action','ai','af','amplitude','trials','admitted_original_initials','prospective_tolerances','method','correction_cap','physical_flags','numpy_version'):
                if saved[key]!=canonical(manifest[key]):raise ValueError('Exact interrupted scientific manifest '+key)
            manifest=saved
        for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
        import numpy as np
        if np.__version__!=manifest['numpy_version']:raise ValueError('Actual unchanged NumPy registration')
        background=load_background()
        if resume:
            ZERO_RECORD=reread_zero();lineage(TRIALS,manifest);journal('OWNER_RESUME');controls.append(ZERO_RECORD['metadata']['control'])
        else:
            CONTEXT=dict(stage='zero_column');RAW.clear();CORE_HISTORY.clear();zlay=layout(32,64,1.);zx=math.log(AI);zd=(math.log(AF)-zx)/4096
            zero_core=np.zeros((11,2));zero_native=np.zeros((len(zlay['om']),2,2));zero_angular=np.zeros((len(zlay['mu']),2),complex);RAW.update(zero_initial_core=zero_core,zero_initial_native=zero_native,zero_initial_angular=zero_angular)
            zn,zz,za,_,_=panel_step(zero_core,zero_native,zero_angular,zx,zd,.01,fixed,background,zlay);RAW.update(zero_core_nodes=zn.copy(),zero_native_nodes=zz.copy(),zero_angular_nodes=za.copy())
            control=gate('zero_data_full_coupled_column',max(float(np.max(abs(v))) for v in (zn,zz,za)),0.);controls.append(control);ZERO_RECORD=zero_checkpoint(dict(RAW),control,list(CORE_HISTORY))
        for t in TRIALS:
            CONTEXT=dict(trial=t['name'],stage='admitted_initial');RAW.clear();admitted=admit_initial(t,old_manifest);incoming=None
            committed=sorted(BASE.glob(STEM+'_'+t['name']+'_CP_*_COMMIT.json'))
            if committed:
                cp=json.loads(committed[-1].read_text());p=BASE/cp['payload']
                with np.load(p,allow_pickle=False) as z:incoming=(cp['metadata'],{n:z[n].copy() for n in z.files if n!='metadata'})
                if cp['nstep']==t['nstep']:
                    md=cp['metadata'];rows.append(dict(trial=t,frames=md['frames'],maxima=md['maxima'],solver_history=md['solver_history'],original_initial_checkpoint=INITIALS[t['name']],terminal_checkpoint=p.name));continue
            rows.append(run_trial(t,fixed,background,admitted,incoming))
        for row in rows:
            if len(row['maxima'])!=16 or len(row['solver_history'])!=4096:raise ValueError('Complete maxima/core solve census')
            for name,data in row['maxima'].items():
                tol=NORMAL_TOL if name in ('normal_error','normal_propagation') else INCREMENT_TOL if name in ('metric_momentum','ordinary_density','phase_density','radiation_density','proper_trace_increment','whole_density_increment') else ROW_TOL
                controls.append(gate(row['trial']['name']+'_'+name,data['error'],tol))
            controls.append(gate(row['trial']['name']+'_preparation_normal',max(row['frames'][0]['normal_error']),ROW_TOL))
        prefix=lineage(TRIALS,manifest);verify_initial_copies();ZERO_RECORD=reread_zero();expected=264
        if len(prefix)!=expected or len(rows)!=8 or sum(len(v['frames']) for v in rows)!=264 or len(controls)!=137:raise ValueError('Eight FINE/full33-frame/137-predicate census')
        recovery_parent();recheck();status='NUMERICAL_PASS' if all(v['passed'] for v in controls) else 'NUMERICAL_FAILED'
        result=dict(status=status,manifest=manifest,rows=rows,controls=controls,zero_control_checkpoint=ZERO_RECORD,background_parent_copied_exactly=background_parent,original_parent_error_copied_exactly=parent['original_error_copied_exactly'],original_parent_controls_copied_exactly=parent['controls'],original_parent_registration_copied_exactly=parent['sample_registration_controls'],original_parent_comparisons_copied_exactly=parent['comparisons'],original_parent_rows_copied_exactly=parent['rows'],original_parent_qualification_copied_exactly=parent['qualification'],original_parent_physical_flags_copied_exactly=parent['physical_flags'],core_evidence_result_sha256=PINS[CORE_PARENT+'_RESULT.json'],physical_flags=manifest['physical_flags'],qualification=manifest['physical_flags'],scope='Only original eight FINE finite-slice prepared trials; same angular64, no repaired ANGLE or continuum claim',elapsed_seconds=time.monotonic()-tick)
        rh=write(STEM+'_RESULT.json',result)
        report=['# Original FINE core and baryon diagnostic recovery V001','',status,'',str(sum(v['passed'] for v in controls))+'/137 new predicates passed; original1,889 dispositions remain unchanged.','', 'No state projection, angular alteration or physical qualification.','', '| trial | normal | density increment | trace increment | core rows | corrections |','|---|---:|---:|---:|---:|---:|']
        for r in rows:
            m=r['maxima'];report.append(f"| {r['trial']['name']} | {m['normal_error']['error']:.9g} | {m['whole_density_increment']['error']:.9g} | {m['proper_trace_increment']['error']:.9g} | {m['core_rows']['error']:.9g} | {sum(len(v['corrections']) for v in r['solver_history'])} |")
        rp=BASE/(STEM+'_REPORT.md');raw=('\n'.join(report)+'\n').encode()
        with rp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        rp.chmod(0o444)
        if rp.read_bytes()!=raw:raise IOError('Exact report-byte reread')
        OUTPUTS[str(rp.resolve())]=sha(rp);recheck();journal('OWNER_CLOSE',status=status,result_sha256=rh)
        jp=BASE/(STEM+'_JOURNAL.jsonl');jp.chmod(0o444);OUTPUTS[str(jp.resolve())]=sha(jp)
        receipt=dict(status=status,owner='root',pid=os.getpid(),started=manifest['started'],closed=now(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,result_sha256=rh,input_sha256=INPUTS,output_sha256={str(Path(p).relative_to(BASE)):h for p,h in OUTPUTS.items()},checkpoint_pairs=265,evolution_checkpoint_pairs=264,zero_control_checkpoint_pairs=1,predicate_count=137)
        write(STEM+'_RECEIPT.json',receipt)
        if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=canonical(receipt):raise ValueError('Entire naturally closed receipt reread')
        recovery_parent();reread_zero();verify_initial_copies();recheck();print(status,rh,flush=True);return 0 if status=='NUMERICAL_PASS' else 3
    except Exception as exc:
        existing=BASE/(STEM+'_RECEIPT.json');protected_receipt=sha(existing) if existing.exists() else None
        if protected_receipt is not None:OUTPUTS[str(existing.resolve())]=protected_receipt
        if RAW:
            rp=BASE/(STEM+'_ERROR_RAW.npz');meta=dict(context=CONTEXT,type=type(exc).__name__,message=str(exc),arrays={n:dict(shape=list(v.shape),dtype=str(v.dtype),finite=bool(np.all(np.isfinite(v)))) for n,v in RAW.items()});text=encode(meta).decode()
            with rp.open('xb') as f:np.savez_compressed(f,metadata=np.asarray(text),**RAW);f.flush();os.fsync(f.fileno())
            rp.chmod(0o444);OUTPUTS[str(rp.resolve())]=sha(rp)
            with np.load(rp,allow_pickle=False) as z:
                if json.loads(str(z['metadata']))!=json.loads(text) or set(z.files)!=set(RAW)|{'metadata'} or any(not np.array_equal(z[n],v,equal_nan=True) for n,v in RAW.items()):raise ValueError('Whole nonfinite/refused raw scratch reread')
        error=dict(status='ERROR',owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,time=now(),context=CONTEXT,type=type(exc).__name__,message=str(exc),protected_existing_receipt_sha256=protected_receipt,input_sha256=INPUTS,output_sha256={str(Path(p).relative_to(BASE)):h for p,h in OUTPUTS.items()},physical_flags=manifest['physical_flags'])
        write(STEM+'_ERROR.json',error)
        jp=BASE/(STEM+'_JOURNAL.jsonl')
        if protected_receipt is None:
            journal('OWNER_ERROR',context=CONTEXT,type=type(exc).__name__,message=str(exc));jp.chmod(0o444)
        if jp.exists():OUTPUTS[str(jp.resolve())]=sha(jp)
        if protected_receipt is None:
            erc=dict(error,closed=now(),output_sha256={str(Path(p).relative_to(BASE)):h for p,h in OUTPUTS.items()});write(STEM+'_RECEIPT.json',erc)
            if json.loads((BASE/(STEM+'_RECEIPT.json')).read_text())!=canonical(erc):raise ValueError('Whole ERROR receipt reread')
        elif sha(existing)!=protected_receipt:raise ValueError('Protected previous receipt changed')
        recovery_parent();recheck();raise

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--root-owned',action='store_true');ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    if not args.root_owned:raise RuntimeError('Root-owned numerical execution only')
    raise SystemExit(main(args.resume))
