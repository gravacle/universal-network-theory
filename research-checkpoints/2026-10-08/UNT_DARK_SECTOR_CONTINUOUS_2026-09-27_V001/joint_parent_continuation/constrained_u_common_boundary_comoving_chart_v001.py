"""Exact time-dependent comoving chart discriminator; root execution only."""
from pathlib import Path
from datetime import datetime, timezone
import argparse,ast,hashlib,json,math,os,time
BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_COMMON_BOUNDARY_COMOVING_CHART_V001'
PROTOCOL_SHA='0db02031c50380af061f60a6ae6560e778b3cc55d1201c8efde0c6e61139812e'
PINS={'constrained_u_clock_gradient_early_transfer_v005.py': 'bfee912d66cbfd91b9d80630c15cbe1cf32c4c905f0d736c4491113f01d84b20', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V005.md': '027233e02902b2905a5f172e3aaec6ab297a956e5e66a1f058ffbb36f66c93a6', 'constrained_u_galaxy_horizon_volterra_v003.py': '06823e14186e3dec4a20b13206ceb3b5fd4824e166f09c2a856083e276b5b273', 'CONSTRAINED_U_GALAXY_HORIZON_VOLTERRA_V003.md': 'f3ec83a84bee7291b73a02ba73d48a793ab0ec7a081baa34a963ab5e5f27fc7d', 'CONSTRAINED_U_GALAXY_SCALE_REGULAR_SEED_AND_RETARDED_RADIATION_KERNEL_V002.md': '2d66ca4ec9c35bcd67c29914d29a634c1968ed1c2e7e8ab5eb7ba99cdf5b1f47', 'constrained_u_common_boundary_seed_overlap_v001.py': '2084d7863ec62a5540433aba6f4a2bb5be1d50ecb7050fb746cb3837726b165d', 'CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V001.md': '9497ea73b1022274ede52315d3c01261f8766ec4c71b34ea7110d91a639dac00', 'constrained_u_common_boundary_seed_overlap_v002.py': '766f64d55664b7b8b95d9099a2a415876eef81168e5932492aa81e48384dccae', 'CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V002.md': '57f9d8e84ae44ccdcdb7e700dee157a82d08ba9a0d2cdd9a72a251c635f44cdb', 'CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V002_RESULT.json': '0531e94732b6ff42029232714156022822fa06497ce4b696dffca3963c5ae424', 'CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V002_RECEIPT.json': '4dec77dd5303cc70129cc84f2bbc4a90edd3b2f4a4646835b1498da1705a31c4', 'CONSTRAINED_U_COMOVING_CURVATURE_AND_RELATIVE_VELOCITY_CHART_V002.md': '2e2102548a82167563f6a7b5ff9af558aea4d9cc85f20957daa72c777c5bdb3a'}
SPANS={'sha': 'd58e56b684b01bf61e0cc835c278e755e664aa0f96019b39d4ef2fe6b80ae50b', 'seal': '3862936d749ebc1cfdf9523019b5593366adc9b48bf5f319f8ec1ea5c04b5d88', 'background': 'eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2', 'Thermal': '0d4c6a2726fd817d2cfb5ba8b90a6674a288bc0484c927da719ecdef72a7cd47', 'Layout': 'f199860c3687d2acc7817eda8a00133c1ef57abb2ffbf224ddc760a90e41d2a8', 'coefficients': 'b9e6a7edca9a67031670d32dba146c289347b9253f32bf16d0f3587597125637', 'rates': '2053ec557e765a899a9468fed8a48d701e010d2f76a0aa666ab209e8dc079354', 'initial': 'a4c4a630fa849f83fbeb3f5128126807d571f308edecff24dc9891b7dabf51ab', 'stage_matrix': '0b02c3bb7a1c4d2d4a9ce6e5ddfe964965042d013ba916d50a4eeda63cb040fe', 'tridiagonal_blocks': 'aa7b86cf64ba2f4b4ccccebc676f120a57270ca5203b8ff4555c19743f2e378f', 'block_stage_solve': 'a44e8a47d27984773c73bc3c32f38e83444502417310d6e126d836daf0ae0a56', 'require': '404261933c28a75c12593bf939703277ec0dd231219dfafff8a8577fb8b46dd0', 'coordinate_scales': 'f0903a138a434ae053aba727d97e91e8c12385e6870a808600b1a6ba4983c01e', 'residual': '7344e575e1fc8058685dec9c678d79d42243b3783455ae37c5818cef020e65e0', 'refined_stages': 'ed7e137c739e59cd211f8b33981200e92da0096ca3d0f8eec93467327959d0b8', 'radau_step': '7cbdcca7d319312c2bbe8ffaf4fa0f22e5655867a98c54e77bbf21dd8da28eb6', 'snapshot': '842bef984f2904f4eabdb467fc1bdd6e90f83d472874507c57dbd8aea8d62b7f', 'authenticate': '19187ee4f2a19960ba605284f0dd8b2fde648bff861ce7e1f4a5e82fb608ea9c', 'regular_seed': 'fcfc6f1e6f8baf62058c99448ca332592332ce0da93f3810c1c7dfddf0b896fe'}
V5='constrained_u_clock_gradient_early_transfer_v005.py'
H3='constrained_u_galaxy_horizon_volterra_v003.py'
FAMILIES=('OLD','REGULAR')
STEPS=(512,1024)
AI=1e-7
CURVATURE=1e-5
OMEGAS=(.1,1.,10.,100.)
READOUT_NAMES=('photon_monopole_plus_Phi','photon_velocity','baryon_velocity','Weyl','photon_quadrupole','polarization_source','neutrino_quadrupole','comoving_baryon_contrast','comoving_baryon_density','comoving_radiation_density','comoving_clock_density','polarization_density','hard_density','soft_density','normal_acceleration')
SEALS={};CREATED={};SOURCE_SHA=None;MANIFEST_SHA=None;ENTERED=False

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise AssertionError(msg)
def read(p):return json.loads(Path(p).read_text())
def now():return datetime.now(timezone.utc).isoformat()
def seal(p,h):
    p=Path(p).resolve();require(p.is_relative_to(BASE.parent.parent) or p==Path('/usr/bin/clang').resolve(),'Input path')
    require(sha(p)==h,'Input seal '+str(p));require(str(p) not in SEALS or SEALS[str(p)]==h,'Conflicting seal');SEALS[str(p)]=h

def write(name,obj):
    data=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    p=BASE/name
    with p.open('x') as f:f.write(data)
    p.chmod(0o444);CREATED[str(p)]=sha(p);return sha(p)

def event(kind,**kw):
    obj=dict(time=now(),event=kind,owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,**kw)
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:f.write(json.dumps(obj,sort_keys=True,allow_nan=False)+'\n')

def recheck():
    require(sha(__file__)==SOURCE_SHA,'Source changed')
    for p,h in SEALS.items():require(sha(p)==h,'Input changed '+p)
    for p,h in CREATED.items():require(sha(p)==h,'Output changed '+p)

def load_helpers(np):
    source=(BASE/V5).read_text();tree=ast.parse(source)
    constants={}
    wanted={'STEM','PROTOCOL_SHA','PINS','BACKGROUND_SPAN_SHA','RADAU_SPAN_SHA','COMPILER_SHA','SCALE_SPAN_SHA','MPC','CP','K','KB','C','CBAR','CURVATURE','BALANCE_PASSES','REFINEMENT_STEPS'}
    for n in tree.body:
        if not isinstance(n,ast.Assign):continue
        for target in n.targets:
            if isinstance(target,ast.Name) and target.id in wanted:constants[target.id]=ast.literal_eval(n.value)
            if isinstance(target,ast.Tuple) and all(isinstance(t,ast.Name) and t.id in wanted for t in target.elts):
                constants.update(zip((t.id for t in target.elts),ast.literal_eval(n.value)))
    require(set(constants)==wanted,'Complete authenticated helper constants')
    require(constants['K']==.01 and constants['CURVATURE']==CURVATURE and constants['BALANCE_PASSES']==4 and constants['REFINEMENT_STEPS']==3,'Exact source/method fixtures')
    env=dict(__file__=str(BASE/V5),__name__='seed_overlap_definition_only',BASE=BASE,np=np,math=math,Path=Path,json=json,ast=ast,hashlib=hashlib,SEALS={},**constants)
    names=set(SPANS)-{'regular_seed'};definitions=[]
    for n in tree.body:
        if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names:
            require(hashlib.sha256(ast.get_source_segment(source,n).encode()).hexdigest()==SPANS[n.name],'Helper span '+n.name);definitions.append(n)
    require({n.name for n in definitions}==names,'Definition-only whitelist')
    exec(compile(ast.Module(body=definitions,type_ignores=[]),str(BASE/V5),'exec'),env)
    fixed=env['authenticate']()
    for p,h in env['SEALS'].items():seal(p,h)
    hs=(BASE/H3).read_text();node=next(n for n in ast.parse(hs).body if isinstance(n,ast.FunctionDef) and n.name=='regular_seed')
    require(hashlib.sha256(ast.get_source_segment(hs,node).encode()).hexdigest()==SPANS['regular_seed'],'Exact regular seed')
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(BASE/H3),'exec'),env)
    require(fixed['k_Mpc_inverse']==.01 and fixed['curvature']==CURVATURE,'Same physical input recovery')
    return env,fixed

def raw_seed(family,a,omega,env,fixed,lay,therm,snodes,weights):
    if family=='OLD':
        y=env['initial'](math.log(a),fixed,lay,therm,snodes,weights)
        meta=dict(finite_curvature_target=CURVATURE,scope='Inherited leading finite-start zero-mode preparation')
    else:y,eta,meta=env['regular_seed'](a,fixed,lay,therm,snodes,weights,omega,env)
    return y,meta

def to_chart(y,h,np):
    out=y.copy();V=y[8]
    out[0]=y[0]+h*V;out[1]=y[1]+3*h*V;out[2]=y[2]-V
    out[3]=y[3]+4*h*V;out[4]=y[4]-V;out[5]=y[5]+4*h*V;out[6]=y[6]-V;out[7]=y[7]+3*h*V
    return out

def to_raw(y,h,np):
    out=y.copy();V=y[8]
    out[0]=y[0]-h*V;out[1]=y[1]-3*h*V;out[2]=y[2]+V
    out[3]=y[3]-4*h*V;out[4]=y[4]+V;out[5]=y[5]-4*h*V;out[6]=y[6]+V;out[7]=y[7]-3*h*V
    return out

def chart_transform(bg,lay,np):
    na=lay.n+2;T=np.eye(na);Ti=np.eye(na);Td=np.zeros((na,na));h=bg['h']
    for row,factor in ((0,1),(1,3),(3,4),(5,4),(7,3)):
        T[row,8]=factor*h;Ti[row,8]=-factor*h;Td[row,8]=factor*bg['h_dt']
    for row in (2,4,6):T[row,8]=-1.;Ti[row,8]=1.
    return T,Ti,Td

def chart_coefficients(x,y,env,fixed,lay,therm,snodes,weights,omega,n_override=None):
    bg=env['background'](x,fixed);h,b,r,w,c,Q=(bg[k] for k in ('h','b','r','w','cs','Q'))
    rg,rn=r*fixed['fgamma'],r*(1-fixed['fgamma']);q=.01*env['CP']/(1000*fixed['Hunit']*bg['a'])
    th=therm.at(bg['a']);g=th['g'];rb=3*b/(4*rg)
    R,Gb,wb,Gg,wg,Gn,wn,Gamma,V=(y[i] for i in range(9))
    psi=R-h*V;phi=psi-2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2
    S=b*wb+4*rg*wg/3+4*rn*wn/3;Rd=S+h*c*Gamma
    Z=weights@y[lay.z];Zd=weights@y[lay.zd];R1=(weights*snodes**2)@y[lay.z]*omega**2
    alpha=omega**2*float(weights@snodes**2);L=Q*q;Ld=-h*(1+3*c)*L
    Ldd=(h*h*(1+3*c)**2-bg['h_dt']*(1+3*c)-3*h*bg['cs_dt'])*L
    v=Z/L;vd=(Zd-Ld*v)/L;ncalc=vd-c*Gamma;n=ncalc if n_override is None else n_override
    Vd=phi+c*Gamma;Bq=1+(fixed['ell_native']*q)**2
    Delta=alpha+env['C']*Q*Q/env['KB']+env['CBAR']*Q*Q*q*q*c/w
    Fv=-h*n-env['C']*(Zd+2*h*Z)/(env['KB']*q)+bg['cs_dt']*Gamma+c*(3*Rd-q*q*V)
    sigma=(L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-alpha*q*n)/Delta
    psid=Rd-bg['h_dt']*V-h*Vd;mom=S+(b+4*(rg+rn)/3+w)*V
    return dict(bg=bg,h=h,b=b,rg=rg,rn=rn,w=w,c=c,Q=Q,q=q,thermal=th,g=g,rb=rb,
        phi=phi,psi=psi,psid=psid,mom=mom,S=S,Rd=Rd,Z=Z,Zd=Zd,L=L,Ld=Ld,Ldd=Ldd,
        v=v,vd=vd,Gamma=Gamma,n=n,ncalc=ncalc,Vd=Vd,Bq=Bq,Delta=Delta,sigma=sigma)

def chart_rates(x,y,env,fixed,lay,therm,snodes,weights,omega,n_override=None,sigma_override=None):
    np=env['np'];f=chart_coefficients(x,y,env,fixed,lay,therm,snodes,weights,omega,n_override)
    h,b,rg,rn,w,c,Q,q,g,rb=(f[k] for k in ('h','b','rg','rn','w','c','Q','q','g','rb'))
    R,Gb,wb,Gg,wg,Gn,wn,Gamma,V=(y[i] for i in range(9));n=f['n'];sigma=f['sigma'] if sigma_override is None else sigma_override
    out=np.zeros_like(y);Rd=f['Rd']
    out[0]=Rd;out[1]=3*Rd-q*q*(V+wb);out[2]=g/rb*(wg-wb)-c*Gamma
    out[3]=4*Rd-4*q*q*(V+wg)/3;out[4]=h*wg+Gg/4-y[lay.fg[2]]/2+g*(wb-wg)-c*Gamma
    out[5]=4*Rd-4*q*q*(V+wn)/3;out[6]=h*wn+Gn/4-y[lay.fn[2]]/2-c*Gamma
    out[7]=3*Rd-q*q*V-env['CBAR']*Q*q*sigma/w;out[8]=f['Vd']
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    for indices,velocity,collision in ((lay.fg,V+wg,g),(lay.fn,V+wn,0.)):
        for l,i in indices.items():
            before=4*q*velocity/3 if l==2 else y[indices[l-1]];after=y[indices[l+1]] if l<max(indices) else 0.
            out[i]=q*(l*before-(l+1)*after)/(2*l+1)-collision*y[i]
            if l==2 and collision:out[i]+=collision*Pi/10
    for l,i in lay.pol.items():
        before=y[lay.pol[l-1]] if l else 0.;after=y[lay.pol[l+1]] if l<lay.lg else 0.
        out[i]=q*(l*before-(l+1)*after)/(2*l+1)-g*y[i]
        if l in (0,2):out[i]+=g*Pi*(.5 if l==0 else .1)
    out[lay.z]=y[lay.zd]
    if y.ndim==1:out[lay.zd]=-3*h*y[lay.zd]-omega**2*snodes**2*(f['Bq']*y[lay.z]-q*n-sigma)
    else:out[lay.zd]=-3*h*y[lay.zd]-omega**2*snodes[:,None]**2*(f['Bq']*y[lay.z]-q*n[None,:]-sigma[None,:])
    return out,f

def chart_stage_matrix(x,env,fixed,lay,therm,snodes,weights,omega):
    np=env['np'];na=lay.n+2;eye=np.eye(na)
    out,f=chart_rates(x,eye[:lay.n],env,fixed,lay,therm,snodes,weights,omega,eye[lay.n],eye[lay.n+1])
    mat=np.zeros((na,na));mat[:lay.n]=out/f['h']
    mat[lay.n]=eye[lay.n]-f['ncalc'];mat[lay.n+1]=eye[lay.n+1]-f['sigma']
    return mat

def operator_control(x,env,fixed,lay,therm,snodes,weights,omega):
    np=env['np'];bg=env['background'](x,fixed);T,Ti,Td=chart_transform(bg,lay,np)
    old=env['stage_matrix'](x,fixed,lay,therm,snodes,weights,omega);actual=chart_stage_matrix(x,env,fixed,lay,therm,snodes,weights,omega)
    left=T.copy();left[lay.n:]=np.eye(lay.n+2)[lay.n:]
    expected=left@old@Ti+(Td/bg['h'])@Ti
    envelope=abs(left)@abs(old)@abs(Ti)+abs(Td/bg['h'])@abs(Ti)
    scale=np.maximum(np.max(envelope,axis=1),1e-30);rows=np.max(abs(actual-expected),axis=1)/scale
    inv=np.max(abs(T@Ti-np.eye(lay.n+2)))
    eye=np.eye(lay.n+2);f=chart_coefficients(x,eye[:lay.n],env,fixed,lay,therm,snodes,weights,omega,eye[lay.n])
    q,h,b,rg,rn,w=(f[k] for k in ('q','h','b','rg','rn','w'))
    raw=Ti[:lay.n];mom=b*raw[2]+4*rg*raw[4]/3+4*rn*raw[6]/3+w*raw[8]
    P=.5*env['KB']*q*eye[lay.n]+env['CBAR']*(weights@raw[lay.z])
    old_terms=[q*q*raw[0],3*h*mom,b*raw[1],rg*raw[3],rn*raw[5],w*raw[7],-q*P]
    new_terms=[q*q*(eye[0]-h*eye[8]),3*h*f['S'],b*eye[1],rg*eye[3],rn*eye[5],w*eye[7],-q*P]
    nr=np.sum(new_terms,axis=0)-np.sum(old_terms,axis=0);ns=np.maximum(np.sum(abs(np.array(old_terms)),axis=0)+np.sum(abs(np.array(new_terms)),axis=0),1e-30)
    return dict(a=math.exp(x),omega=omega,inverse_error=float(inv),generator_error=float(np.max(rows)),normal_row_error=float(np.max(abs(nr)/ns)),generator_row_errors=rows.tolist(),generator_row_scales=scale.tolist(),signed_normal_row_difference=nr.tolist(),normal_row_scale=ns.tolist(),scope='FULL_AUGMENTED_BASIS_WITH_EXPLICIT_T_DOT; natural uncanceled operator envelopes')

def chart_radau_step(y,x,dx,env,fixed,lay,therm,snodes,weights,omega,check=False,dense=False):
    np=env['np'];na=lay.n+2;m1=chart_stage_matrix(x+dx/3,env,fixed,lay,therm,snodes,weights,omega);m2=chart_stage_matrix(x+dx,env,fixed,lay,therm,snodes,weights,omega)
    eye=np.eye(na);eye[lay.n:]=0.;Kmat=np.block([[eye-dx*(5/12)*m1,dx*m2/12],[-dx*.75*m1,eye-dx*.25*m2]])
    Kmat[lay.n:na]=0.;Kmat[lay.n:na,:na]=m1[lay.n:];Kmat[na+lay.n:]=0.;Kmat[na+lay.n:,na:]=m2[lay.n:]
    rhs=np.tile(np.concatenate((y,[0.,0.])),2);dr,dc,A=env['coordinate_scales'](Kmat);b=dr*rhs
    stages=dc*env['block_stage_solve'](A,b,lay)
    stages=env['refined_stages'](Kmat,rhs,A,dr,dc,stages,lambda mat,vec:env['block_stage_solve'](mat,vec,lay))
    error=env['residual'](Kmat,rhs,stages)[0] if check else 0.;derror=0.;record=None
    if dense:
        independent=dc*np.linalg.solve(A,b);independent=env['refined_stages'](Kmat,rhs,A,dr,dc,independent,np.linalg.solve)
        derror=float(np.max(abs(stages-independent))/max(float(np.max(abs(independent))),CURVATURE*1e-16))
        stage_states=[stages[:lay.n],stages[na:na+lay.n]];coordinates=[x+dx/3,x+dx]
        record=dict(x=x,dx=dx,incoming_chart=y.tolist(),incoming_raw=to_raw(y,env['background'](x,fixed)['h'],np).tolist(),chart_stages=[v.tolist() for v in stage_states],raw_stages=[to_raw(v,env['background'](xx,fixed)['h'],np).tolist() for xx,v in zip(coordinates,stage_states)],algebraic_stages=[stages[lay.n:na].tolist(),stages[na+lay.n:].tolist()],stage_error=float(error),dense_error=derror)
    return stages[na:na+lay.n],error,derror,record

def chart_snapshot(x,y,env,fixed,lay,therm,snodes,weights,omega):
    np=env['np'];dy,f=chart_rates(x,y,env,fixed,lay,therm,snodes,weights,omega)
    h,b,rg,rn,w,c,Q,q=(f[k] for k in ('h','b','rg','rn','w','c','Q','q'))
    raw=to_raw(y,h,np);original=env['snapshot'](x,raw,fixed,lay,therm,snodes,weights,omega)
    T,Ti,Td=chart_transform(f['bg'],lay,np);rawdy=Ti[:lay.n,:lay.n]@(dy-Td[:lay.n,:lay.n]@raw)
    rawdy0,_=env['rates'](x,raw,fixed,lay,therm,snodes,weights,omega)
    rate_scale=abs(Ti[:lay.n,:lay.n])@(abs(dy)+abs(Td[:lay.n,:lay.n])@abs(raw))+abs(rawdy0)
    rate_error=float(np.max(abs(rawdy-rawdy0)/np.maximum(rate_scale,CURVATURE*1e-16)))
    R,Gb,wb,Gg,wg,Gn,wn,Gamma,V=(y[i] for i in range(9));psi=raw[0];db,ub,dg,ug,dn,un,d=(raw[i] for i in (1,2,3,4,5,6,7))
    n=f['n'];sigma=f['sigma'];P=.5*env['KB']*q*n+env['CBAR']*f['Z']
    nt=np.array([q*q*psi,3*h*f['mom'],b*db,rg*dg,rn*dn,w*d,-q*P]);stable_nt=np.array([q*q*psi,3*h*f['S'],b*Gb,rg*Gg,rn*Gn,w*Gamma,-q*P])
    nf=q*q*CURVATURE*1e-10;normal=math.fsum(float(v) for v in stable_nt);ne=abs(normal)/max(sum(abs(nt)),nf)
    vdd=(weights@dy[lay.zd]-2*f['Ld']*f['vd']-f['Ldd']*f['v'])/f['L']
    nd=vdd-f['bg']['cs_dt']*Gamma-c*dy[7]
    et=np.array([.5*env['KB']*q*nd,-.5*env['KB']*h*q*n,env['CBAR']*f['Zd'],2*h*P,env['CBAR']*Q*sigma])
    ef=.5*env['KB']*q*CURVATURE*max(h,Q,omega)*1e-10;ee=float(abs(sum(et))/max(sum(abs(et)),ef))
    phid=f['psid']-2*(rg*(dy[lay.fg[2]]-2*h*y[lay.fg[2]])+rn*(dy[lay.fn[2]]-2*h*y[lay.fn[2]]))/q**2
    momd=b*(rawdy[2]-3*h*ub)+4*rg*(rawdy[4]-4*h*ug)/3+4*rn*(rawdy[6]-4*h*un)/3+w*(rawdy[8]-3*h*(1+c)*V)
    psidd=momd-f['bg']['h_dt']*f['phi']-h*phid
    tt=np.array([psidd,h*phid,3*h*f['psid'],(2*f['bg']['h_dt']+3*h*h)*f['phi'],q*q*(psi-f['phi'])/3,-c*w*d,-(rg*dg+rn*dn)/3])
    tf=CURVATURE*max(h*h,q*q)*1e-12;te=float(abs(sum(tt))/max(sum(abs(tt)),tf))
    contrast=Gb+3*h*wb;Eb=b*contrast;Eg=rg*(Gg+4*h*wg);En=rn*(Gn+4*h*wn);Ec=w*Gamma;Ep=-q*P;S=rg*y[lay.fg[2]]+rn*y[lay.fn[2]]
    other=math.fsum((Eg,En,Ec,Ep));force_num=math.fsum((-q*q*f['phi'],-Eb,-other,-2*S));lens_num=math.fsum((-q*q*(f['phi']+psi)/2,-Eb,-other,-S))
    numerator_scale=max(math.fsum(abs(v) for v in nt)+math.fsum(abs(v) for v in stable_nt)+q*q*(abs(psi)+abs(f['phi']))+abs(Eb)+abs(other)+2*abs(S),nf)
    contacts=dict(rate_error=rate_error,rate_scale=rate_scale.tolist(),normal_numerator_error=abs(math.fsum(float(v) for v in nt)-normal)/numerator_scale,force_numerator_error=abs(force_num+normal)/numerator_scale,lens_numerator_error=abs(lens_num+normal)/numerator_scale,numerator_scale=numerator_scale)
    rat=dict(denominator=Eb,normal_over_denominator=normal/Eb if Eb else None)
    if Eb:
        ref=-Eb/q**2;rat.update(force_metric=.99*f['phi']/ref,lens_metric=.99*(f['phi']+psi)/(2*ref),force_source=.99*(1+(other+2*S)/Eb),lens_source=.99*(1+(other+S)/Eb),refusal=None)
    else:rat.update(force_metric=None,lens_metric=None,force_source=None,lens_source=None,refusal='ZERO_SIGNED_BARYON_DENOMINATOR')
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    reads=[dg/4+f['phi'],q*ug,q*ub,psi+f['phi'],y[lay.fg[2]],Pi,y[lay.fn[2]],contrast,Eb,Eg+En,Ec,Ep,-.5*env['KB']*q*q*n,-env['CBAR']*q*f['Z'],q*n]
    result=dict(original);result.update(state=raw.tolist(),chart_state=y.tolist(),Phi=float(f['phi']),Psi=float(psi),Q=float(Q),reaction_denominator=float(f['Delta']),n_U=float(n),sigma=float(sigma),P=float(P),pi_U=float(V-f['v']),Z=float(f['Z']),Zd=float(f['Zd']),readouts=[float(v) for v in reads],normal_terms=stable_nt.tolist(),normal_floor=nf,normal_error=float(ne),omitted_Euler_terms=et.tolist(),omitted_Euler_floor=ef,omitted_Euler_error=ee,trace_terms=tt.tolist(),trace_floor=tf,trace_error=te,signed_sources=dict(baryon=Eb,photon=Eg,neutrino=En,phase=Ec,polarization=Ep,shear=S),source_ratios=rat,chart_contacts=contacts,original_raw_reference=dict(readouts=original['readouts'],normal_terms=nt.tolist(),normal_error=original['normal_error'],omitted_Euler_error=original['omitted_Euler_error'],trace_error=original['trace_error'],sigma=original['sigma']))
    return result

def contact_controls(case,family,a,omega,env,fixed,lay,snodes,weights,meta,check):
    s=case;y=env['np'].array(s['state']);q=.01*env['CP']/(1000*fixed['Hunit']*a);h=s['background']['h']
    ids=dict(family=family,a=a,omega=omega)
    for key,tol in (('normal_error',1e-10),('trace_error',1e-10),('omitted_Euler_error',1e-10)):check('direct_'+key,s[key],tol,**ids)
    check('direct_shear',abs(s['Psi']-s['Phi']-2*s['signed_sources']['shear']/q**2)/CURVATURE,1e-13,**ids)
    if family=='OLD':
        check('old_finite_curvature',abs((s['Psi']+h*y[8])/CURVATURE-1),2e-13,**ids)
        check('old_zero_modes',float(env['np'].max(abs(y[lay.z])))+float(env['np'].max(abs(y[lay.zd]))),0.,**ids)
    else:
        R=1-fixed['fgamma'];A=CURVATURE/(1.5+2*R/5);hr=math.sqrt(fixed['OR']/fixed['rG']);q0=.01*env['CP']/(1000*fixed['Hunit'])
        f=(56*R*R+10*R-525)/(630*(25+2*R));g=-(56*R*R+580*R+525)/(630*(25+2*R))
        norm=1/fixed['eps']-math.log1p(1/fixed['eps']);Qc=fixed['Q0_over_Hstar']*math.sqrt(1+fixed['eps'])
        alpha=omega**2*float(weights@snodes**2);gamma2=A*(3*g-.25+.75*f)*(q0/hr)**2
        c3=1/(math.sqrt(1+fixed['eps'])*norm*fixed['d0']);sigma2=6*hr*Qc*q0*c3*gamma2/(alpha+env['C']*Qc**2/env['KB'])
        z6=omega**2*snodes**2*sigma2/(42*hr**2)
        check('regular_asymptotic_amplitude',abs(meta['A']/A-1)+abs(meta['asymptotic_curvature']/CURVATURE-1),2e-13,**ids)
        for name,actual,expected in (('z6',y[lay.z],z6*a**6),('zd4',y[lay.zd],6*hr*z6*a**4)):
            den=max(float(env['np'].max(abs(expected))),env['np'].finfo(float).tiny)
            check('regular_'+name,float(env['np'].max(abs(actual-expected)))/den,2e-13,**ids)

def finite_tree(value):
    if type(value) in (bool,int,str) or value is None:return
    if type(value) is float:require(math.isfinite(value),'Finite canonical payload');return
    if isinstance(value,list):
        for x in value:finite_tree(x)
        return
    if isinstance(value,dict):
        require(all(type(k) is str for k in value),'String payload keys')
        for x in value.values():finite_tree(x)
        return
    raise AssertionError('Unexpected serialized type')

def checkpoint_name(family,steps,n):return STEM+'_'+family+'_'+str(steps)+'_CP_'+str(n).zfill(6)+'.json'

def validate_payload(data,lineage,lay,family,steps,n):
    keys={'owner','pid','source_sha256','manifest_sha256','lineage','family','steps','n','state','chart_state','first_stages','snapshots','seed_metadata','stage_errors','dense_errors'}
    require(set(data)==keys and data['lineage']==lineage and (data['family'],data['steps'],data['n'])==(family,steps,n),'Exact checkpoint fields/lineage/stage')
    require(data['owner']=='root' and type(data['pid']) is int and data['pid']>0 and data['source_sha256']==SOURCE_SHA and data['manifest_sha256']==MANIFEST_SHA,'Payload root/source epoch')
    finite_tree(json.loads(json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False)));require(all(len(data[k])==4 and all(len(y)==lay.n for y in data[k]) for k in ('state','chart_state')),'Entire four-arm raw/chart state shape');require(len(data['first_stages'])==4 and all((v is None)==(n==0) for v in data['first_stages']),'Exact first-stage presence')
    require(len(data['seed_metadata'])==4 and len(data['stage_errors'])==len(data['dense_errors'])==4 and all(v>=0 for k in ('stage_errors','dense_errors') for v in data[k]),'Complete seed/error metadata')
    snap=data['snapshots'];stride=steps//16;x0=math.log(AI/2);xf=math.log(AI);dx=(xf-x0)/steps
    require([r['n'] for r in snap]==list(range(0,n+1,stride)),'Exact ordered snapshot prefix')
    for frame in snap:
        expected=xf if frame['n']==steps else x0+frame['n']*dx
        require(set(frame)=={'n','x','cases'} and frame['x']==expected and len(frame['cases'])==4,'Exact snapshot coordinate/case schema')
        for c in frame['cases']:
            require(set(c)=={'x','a','state','background','thermal','Phi','Psi','Q','reaction_denominator','n_U','sigma','P','pi_U','Z','Zd','readouts','normal_terms','normal_floor','normal_error','omitted_Euler_terms','omitted_Euler_floor','omitted_Euler_error','trace_terms','trace_floor','trace_error','domain_heads','signed_sources','source_ratios','chart_state','chart_contacts','original_raw_reference'},'Entire augmented snapshot schema')
            require(set(c['original_raw_reference'])=={'readouts','normal_terms','normal_error','omitted_Euler_error','trace_error','sigma'} and len(c['original_raw_reference']['readouts'])==15 and len(c['original_raw_reference']['normal_terms'])==7,'Full raw contact reference schema')
            require(c['x']==frame['x'] and c['a']==math.exp(frame['x']) and len(c['state'])==lay.n and len(c['readouts'])==15 and len(c['normal_terms'])==7 and len(c['omitted_Euler_terms'])==5 and len(c['trace_terms'])==7,'Full snapshot axes/coordinate')
            require(len(c['chart_state'])==lay.n and set(c['chart_contacts'])=={'rate_error','rate_scale','normal_numerator_error','force_numerator_error','lens_numerator_error','numerator_scale'},'Complete chart/contact schema');require(c['reaction_denominator']>0 and type(c['domain_heads']['inside_sampled_linear_domain']) is bool,'Positive branch/native flag')
    require(snap[-1]['n']==n and all([c[k] for c in snap[-1]['cases']]==data[k] for k in ('state','chart_state')),'Exact full raw/chart last-snapshot state closure')
    for record in data['first_stages']:
        if record is not None:require(set(record)=={'x','dx','incoming_chart','incoming_raw','chart_stages','raw_stages','algebraic_stages','stage_error','dense_error'} and len(record['chart_stages'])==len(record['raw_stages'])==len(record['algebraic_stages'])==2 and all(len(v)==lay.n for k in ('chart_stages','raw_stages') for v in record[k]) and all(len(v)==2 for v in record['algebraic_stages']) and len(record['incoming_chart'])==len(record['incoming_raw'])==lay.n and record['x']==x0 and record['dx']==dx and record['stage_error']>=0 and record['dense_error']>=0,'Entire exact first-step physical/reaction schema')

def validate_runtime(lineage,lay,complete=False):
    jp=BASE/(STEM+'_JOURNAL.jsonl');events=[json.loads(l) for l in jp.read_text().splitlines()] if jp.exists() else []
    expected=[(f,steps,n) for f in FAMILIES for steps in STEPS for n in range(0,steps+1,128)]
    checkpoints=[];latest={};epoch=None;previous={};files=set()
    for position,e in enumerate(events):
        require(e['owner']=='root' and e['source_sha256']==SOURCE_SHA and e['manifest_sha256']==MANIFEST_SHA and type(e['pid']) is int and e['pid']>0,'Journal root/source fields')
        if e['event'] in ('OWNER_START','OWNER_RESUME'):
            require((position==0 and e['event']=='OWNER_START') or (epoch is not None and e['event']=='OWNER_RESUME'),'Exact owner epoch transition');epoch=e['pid'];continue
        require(e['event']=='CHECKPOINT' and e['pid']==epoch,'Checkpoint current root owner epoch')
        ids=(e['family'],e['steps'],e['n']);require(ids==expected[len(checkpoints)],'Exact global checkpoint prefix')
        name=checkpoint_name(*ids);cn=name[:-5]+'_COMMIT.json';require(e['payload']==name,'Exact checkpoint namespace')
        payload=read(BASE/name);commit=read(BASE/cn);validate_payload(payload,lineage,lay,*ids)
        require(payload['pid']==epoch and commit==dict(owner='root',pid=epoch,source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,lineage=lineage,family=ids[0],steps=ids[1],n=ids[2],payload=name,sha256=sha(BASE/name)),'Exact committed owner/payload fields')
        require(e['sha256']==sha(BASE/name) and e['commit_sha256']==sha(BASE/cn),'Journal complete immutable pair hashes')
        require((BASE/name).read_text()==json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n' and (BASE/cn).read_text()==json.dumps(commit,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n','Canonical whole checkpoint pair')
        key=ids[:2]
        if key in previous:
            prev=previous[key];require(payload['seed_metadata']==prev['seed_metadata'] and (prev['n']==0 or payload['first_stages']==prev['first_stages']) and payload['snapshots'][:len(prev['snapshots'])]==prev['snapshots'] and all(payload[k][i]>=prev[k][i] for k in ('stage_errors','dense_errors') for i in range(4)),'Unchanged full snapshot/seed prefix and nondecreasing errors')
        previous[key]=payload;latest[key]=payload;checkpoints.append(ids);files.update((name,cn))
        CREATED[str(BASE/name)]=sha(BASE/name);CREATED[str(BASE/cn)]=sha(BASE/cn)
    actual={p.name for p in BASE.glob(STEM+'_*_CP*.json')};require(actual==files,'No unmatched/orphan checkpoint files')
    allowed=files|{STEM+'_MANIFEST.json',STEM+'_JOURNAL.jsonl'}
    for p in BASE.glob(STEM+'_*'):
        if p.name in allowed:continue
        require(p.name.startswith(STEM+'_FAILED_') and p.suffix=='.json','Unknown runtime file')
        err=read(p);finite_tree(err);require(err['source_sha256']==SOURCE_SHA and err['input_sha256']==SEALS,'Preserved failure lineage');CREATED[str(p)]=sha(p)
    require(bool(events) or not (BASE/(STEM+'_MANIFEST.json')).exists() or not (BASE/(STEM+'_JOURNAL.jsonl')).exists(),'Owned journal history');require(not checkpoints or epoch is not None,'Owned checkpoint history')
    if complete:require(checkpoints==expected,'All28 complete CP pairs')
    return latest

def compute_run(family,steps,env,fixed,lay,therm,snodes,weights,lineage,saved,initial_reference):
    np=env['np'];x0=math.log(AI/2);xf=math.log(AI);dx=(xf-x0)/steps;tick=time.monotonic()
    if saved:
        y=np.array(saved['chart_state']);seed_meta=saved['seed_metadata'];snapshots=saved['snapshots'];errors=saved['stage_errors'];dense=saved['dense_errors'];first_stages=saved['first_stages'];n0=saved['n']
    else:
        states=[];seed_meta=[]
        for om in OMEGAS:
            raw,meta=raw_seed(family,AI/2,om,env,fixed,lay,therm,snodes,weights);states.append(to_chart(raw,env['background'](x0,fixed)['h'],np));seed_meta.append(meta)
        y=np.stack(states);errors=[0.]*4;dense=[0.]*4;first_stages=[None]*4;n0=0
        snapshots=[dict(n=0,x=x0,cases=[chart_snapshot(x0,y[i],env,fixed,lay,therm,snodes,weights,om) for i,om in enumerate(OMEGAS)])]
    require([c['chart_state'] for c in snapshots[0]['cases']]==[c['chart_state'] for c in initial_reference['cases']] and seed_meta==initial_reference['metadata'],'Exact transformed source-owned CP0; no seed reset')
    def checkpoint(n):
        data=dict(owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,lineage=lineage,family=family,steps=steps,n=n,state=[to_raw(c,env['background'](x0+n*dx if n<steps else xf,fixed)['h'],np).tolist() for c in y],chart_state=y.tolist(),first_stages=first_stages,snapshots=snapshots,seed_metadata=seed_meta,stage_errors=errors,dense_errors=dense)
        validate_payload(data,lineage,lay,family,steps,n);name=checkpoint_name(family,steps,n);h=write(name,data);cn=name[:-5]+'_COMMIT.json'
        ch=write(cn,dict(owner='root',pid=os.getpid(),source_sha256=SOURCE_SHA,manifest_sha256=MANIFEST_SHA,lineage=lineage,family=family,steps=steps,n=n,payload=name,sha256=h))
        event('CHECKPOINT',family=family,steps=steps,n=n,payload=name,sha256=h,commit_sha256=ch)
        print(json.dumps(dict(family=family,steps=steps,completed=n,total_steps=steps,elapsed=time.monotonic()-tick)),flush=True)
    if not saved:checkpoint(0)
    for n in range(n0,steps):
        for i,om in enumerate(OMEGAS):
            y[i],er,de,record=chart_radau_step(y[i],x0+n*dx,dx,env,fixed,lay,therm,snodes,weights,om,n%64==0,n==0)
            if n==0:first_stages[i]=record
            errors[i]=max(errors[i],er);dense[i]=max(dense[i],de)
        require(bool(np.all(np.isfinite(y))),'Finite entire propagated state')
        if (n+1)%(steps//16)==0:
            x=xf if n+1==steps else x0+(n+1)*dx
            snapshots.append(dict(n=n+1,x=x,cases=[chart_snapshot(x,y[i],env,fixed,lay,therm,snodes,weights,om) for i,om in enumerate(OMEGAS)]))
        if (n+1)%128==0:checkpoint(n+1)
    require(len(snapshots)==17 and [r['n'] for r in snapshots]==list(range(0,steps+1,steps//16)),'Full ordered overlap snapshot census')
    return dict(family=family,steps=steps,snapshots=snapshots,seed_metadata=seed_meta,stage_errors=errors,dense_errors=dense,first_stages=first_stages,state_names=lay.names(),chart_state_names=['R','Gamma_b','w_b','Gamma_gamma','w_gamma','Gamma_nu','w_nu','Gamma_phi','V']+lay.names()[9:],snodes=snodes.tolist(),weights=weights.tolist())

def main():
    global SOURCE_SHA,MANIFEST_SHA,ENTERED
    require(not any((BASE/(STEM+suffix)).exists() for suffix in ('_RESULT.json','_REPORT.md','_RECEIPT.json')),'Completed runtime prefix; refuse before mutation')
    SOURCE_SHA=sha(__file__);tick=time.monotonic()
    for p,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/p,h)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ.setdefault(key,'1')
    import numpy as np
    env,fixed=load_helpers(np);parent=read(BASE/'CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V002_RESULT.json');pr=read(BASE/'CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V002_RECEIPT.json')
    require(parent['status']==pr['status']=='BOUNDED_SEED_OVERLAP_ARITHMETIC_FAILED' and len(parent['numerical_gates'])==306 and sum(g['passed'] for g in parent['numerical_gates'])==274 and pr['source_sha256']==PINS['constrained_u_common_boundary_seed_overlap_v002.py'] and pr['result_sha256']==PINS['CONSTRAINED_U_COMMON_BOUNDARY_SEED_OVERLAP_V002_RESULT.json'],'Exact preserved original274/32 failed calculation')
    for mapping in ('input_sha256','output_sha256'):
        for p,h in pr[mapping].items():seal(p,h)
    lay=env['Layout'](32,96,128);therm=env['Thermal']('HALF',1,fixed)
    nodes,raw=np.polynomial.legendre.leggauss(32);snodes=(nodes+1)/2;weights=raw*snodes
    lineage=dict(source_sha256=SOURCE_SHA,inputs=dict(SEALS),fixed=fixed,k=.01,curvature=CURVATURE,interval=[AI/2,AI],families=list(FAMILIES),steps=list(STEPS),omegas=list(OMEGAS),numpy_version=np.__version__,spans=SPANS,ns=32,lg=96,ln=128,physical_overlap_is_gate=False,resume=True,coordinate_chart='EXACT_COMOVING_CURVATURE_RELATIVE_VELOCITY',physical_gates=306,chart_gates=84)
    mp=BASE/(STEM+'_MANIFEST.json')
    manifest_existed=mp.exists()
    if manifest_existed:
        require(read(mp)==lineage,'Identical recovery manifest');MANIFEST_SHA=sha(mp);CREATED[str(mp)]=MANIFEST_SHA
    else:
        require(not any(BASE.glob(STEM+'_*')),'Pre-manifest orphan runtime prefix')
        MANIFEST_SHA=write(mp.name,lineage)
    if manifest_existed:require((BASE/(STEM+'_JOURNAL.jsonl')).exists() and (BASE/(STEM+'_JOURNAL.jsonl')).stat().st_size>0,'Existing manifest requires nonempty owner journal')
    latest=validate_runtime(lineage,lay);ENTERED=True
    event('OWNER_RESUME' if (BASE/(STEM+'_JOURNAL.jsonl')).exists() else 'OWNER_START')
    direct=[];runs=[];gates=[];chart_gates=[];operator_fixtures=[]
    def chart_check(name,error,**ids):
        error=float(error);chart_gates.append(dict(name=name,error=error,tolerance=2e-11,passed=bool(math.isfinite(error) and error<=2e-11),**ids))
    for a in (AI/2,math.sqrt(AI*(AI/2)),AI):
        for om in OMEGAS:
            control=operator_control(math.log(a),env,fixed,lay,therm,snodes,weights,om);operator_fixtures.append(control)
            for key in ('inverse_error','generator_error','normal_row_error'):chart_check(key,control[key],a=a,omega=om)
    def check(name,error,tolerance,**ids):
        error=float(error);gates.append(dict(name=name,error=error,tolerance=tolerance,passed=bool(math.isfinite(error) and error<=tolerance),**ids))
    check('spectrum_normalization',abs(float(sum(weights))-1),1e-13)
    for family in FAMILIES:
        for a in (AI/2,AI):
            cases=[];metas=[]
            for om in OMEGAS:
                raw,meta=raw_seed(family,a,om,env,fixed,lay,therm,snodes,weights);cy=to_chart(raw,env['background'](math.log(a),fixed)['h'],np);case=chart_snapshot(math.log(a),cy,env,fixed,lay,therm,snodes,weights,om);case['incoming_raw_state']=raw.tolist();case['incoming_chart_state']=cy.tolist()
                cases.append(case);metas.append(meta);chart_check('incoming_roundtrip',float(np.max(abs(np.array(case['state'])-raw)))/max(float(np.max(abs(raw))),CURVATURE*1e-16),family=family,a=a,omega=om);chart_check('direct_rate_contact',max(case['chart_contacts'][key] for key in ('rate_error','normal_numerator_error','force_numerator_error','lens_numerator_error')),family=family,a=a,omega=om);contact_controls(case,family,a,om,env,fixed,lay,snodes,weights,meta,check)
            direct.append(dict(family=family,a=a,cases=cases,metadata=metas))
        for steps in STEPS:
            recheck();validate_runtime(lineage,lay);row=compute_run(family,steps,env,fixed,lay,therm,snodes,weights,lineage,latest.get((family,steps)),next(d for d in direct if d['family']==family and d['a']==AI/2));recheck();runs.append(row)
            for i,om in enumerate(OMEGAS):
                check('dynamic_stage',row['stage_errors'][i],2e-11,family=family,steps=steps,omega=om)
                check('independent_dense',row['dense_errors'][i],2e-11,family=family,steps=steps,omega=om)
                chart_check('propagated_rate_contact',max(s['cases'][i]['chart_contacts'][key] for s in row['snapshots'] for key in ('rate_error','normal_numerator_error','force_numerator_error','lens_numerator_error')),family=family,steps=steps,omega=om)
                for key,tol in (('normal_error',1e-5),('trace_error',1e-10),('omitted_Euler_error',1e-10)):
                    check(key,max(s['cases'][i][key] for s in row['snapshots']),tol,family=family,steps=steps,omega=om)
    allcases=[c for d in direct for c in d['cases']]+[c for r in runs for s in r['snapshots'] for c in s['cases']]
    check('maximum_charge_root',max(c['background']['charge_error'] for c in allcases),1e-13)
    require(all(c['reaction_denominator']>0 for c in allcases),'All positive reaction denominators')
    overlaps=[];refinements=[]
    for family in FAMILIES:
        coarse,fine=[r for r in runs if r['family']==family];endpoint=next(d for d in direct if d['family']==family and d['a']==AI)
        cf=np.array([[c['readouts'] for c in s['cases']] for s in coarse['snapshots']]);ff=np.array([[c['readouts'] for c in s['cases']] for s in fine['snapshots']]);den=np.maximum(np.max(abs(ff),axis=0),CURVATURE*1e-8);err=np.max(abs(cf-ff),axis=0)/den
        modal=[]
        for i,om in enumerate(OMEGAS):
            for k,name in enumerate(READOUT_NAMES):check('time_refinement',err[i,k],1e-3,family=family,omega=om,variable=name)
            for name,idx in (('z',lay.z),('zd',lay.zd)):
                ca=np.array([s['cases'][i]['state'] for s in coarse['snapshots']])[:,idx];fa=np.array([s['cases'][i]['state'] for s in fine['snapshots']])[:,idx]
                modal.append(dict(omega=om,field=name,signed_endpoint_difference=(ca[-1]-fa[-1]).tolist(),maximum_absolute_difference=float(np.max(abs(ca-fa))),normalized_with_curvature_floor=float(np.max(abs(ca-fa))/max(float(np.max(abs(fa))),CURVATURE*1e-8)),qualification='ABSOLUTE_DIAGNOSTIC_ONLY_NO_TINY_RELATIVE_PRECISION'))
        refinements.append(dict(family=family,coarse=512,fine=1024,signed_endpoint_difference=(cf[-1]-ff[-1]).tolist(),normalization=den.tolist(),normalized_errors=err.tolist(),modal_diagnostics=modal))
        for row in (coarse,fine):
            for i,om in enumerate(OMEGAS):
                actual=row['snapshots'][-1]['cases'][i];target=endpoint['cases'][i];delta=np.array(actual['state'])-np.array(target['state']);rd=np.array(actual['readouts'])-np.array(target['readouts'])
                overlaps.append(dict(family=family,steps=row['steps'],omega=om,signed_full_state_difference=delta.tolist(),signed_readout_difference=rd.tolist(),native_z_difference=delta[lay.z].tolist(),native_zd_difference=delta[lay.zd].tolist(),signed_curvature_difference=actual['Psi']+actual['background']['h']*actual['state'][8]-target['Psi']-target['background']['h']*target['state'][8],normal_errors=[actual['normal_error'],target['normal_error']],source_ratios=[actual['source_ratios'],target['source_ratios']],qualification='STATE_DEPENDENT_OVERLAP_NOT_AN_ACCEPTANCE_GATE'))
    old=next(d for d in direct if d['family']=='OLD' and d['a']==AI);reg=next(d for d in direct if d['family']=='REGULAR' and d['a']==AI)
    distinctions=[dict(omega=om,signed_full_state_difference=(np.array(old['cases'][i]['state'])-np.array(reg['cases'][i]['state'])).tolist(),signed_readout_difference=(np.array(old['cases'][i]['readouts'])-np.array(reg['cases'][i]['readouts'])).tolist()) for i,om in enumerate(OMEGAS)]
    require(len(gates)==306 and len(chart_gates)==84 and len(allcases)==288 and len(overlaps)==16 and len(operator_fixtures)==12,'Frozen complete original/coordinate census')
    validate_runtime(lineage,lay,complete=True)
    recheck();status='BOUNDED_COMOVING_CHART_NUMERICALLY_QUALIFIED' if all(g['passed'] for g in gates+chart_gates) else 'BOUNDED_COMOVING_CHART_ARITHMETIC_FAILED'
    result=dict(status=status,lineage=lineage,direct_seeds=direct,runs=runs,numerical_gates=gates,chart_gates=chart_gates,operator_fixtures=operator_fixtures,overlaps=overlaps,time_refinements=refinements,direct_old_minus_regular=distinctions,elapsed_seconds=time.monotonic()-tick,scope='Numerical chart experiment only; original274/32 failed attempt preserved, same source-owned states/action; physical overlap and sampled domain independent; no late preparation qualification',original_numerical_gates=parent['numerical_gates'])
    rh=write(STEM+'_RESULT.json',result)
    report='# Bounded exact comoving chart V001\n\nStatus '+status+'. '+str(sum(g['passed'] for g in gates))+'/306 original numerical controls, '+str(sum(g['passed'] for g in chart_gates))+'/84 exact-chart controls. 16 direct seeds, 272 propagated frames, all16 signed overlap rows and4 direct preparation distinctions retained. Physical overlap has no pass threshold and gives no late-time history qualification.\n'
    rp=BASE/(STEM+'_REPORT.md')
    with rp.open('x') as f:f.write(report)
    rp.chmod(0o444);CREATED[str(rp)]=sha(rp)
    event('OWNER_COMPLETE',status=status,gate_count=306,chart_gate_count=84,result_sha256=rh)
    events=[json.loads(l) for l in (BASE/(STEM+'_JOURNAL.jsonl')).read_text().splitlines()]
    require(events[-1]['event']=='OWNER_COMPLETE' and events[-1]['pid']==os.getpid() and events[-1]['source_sha256']==SOURCE_SHA and events[-1]['result_sha256']==rh and sum(e['event']=='CHECKPOINT' for e in events)==28,'Closed root journal/all28 commits')
    (BASE/(STEM+'_JOURNAL.jsonl')).chmod(0o444)
    CREATED[str(BASE/(STEM+'_JOURNAL.jsonl'))]=sha(BASE/(STEM+'_JOURNAL.jsonl'));recheck()
    receipt=dict(status=status,source_sha256=SOURCE_SHA,input_sha256=dict(SEALS),manifest_sha256=MANIFEST_SHA,journal_sha256=sha(BASE/(STEM+'_JOURNAL.jsonl')),result_sha256=rh,output_sha256=dict(CREATED),gate_count=306,chart_gate_count=84)
    write(STEM+'_RECEIPT.json',receipt);recheck();print(json.dumps(dict(status=status,passed=sum(g['passed'] for g in gates),gates=306)),flush=True)
    return 0 if all(g['passed'] for g in gates+chart_gates) else 3

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    if not args.execute:raise SystemExit('Author/static review only; root explicit --execute required')
    try:raise SystemExit(main())
    except Exception as exc:
        if not ENTERED:raise
        if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')):raise
        name=STEM+'_FAILED_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'.json'
        write(name,dict(error_type=type(exc).__name__,error=str(exc),source_sha256=sha(__file__),input_sha256=dict(SEALS),outputs=dict(CREATED),scope='Preserve bounded attempt; no overwritten parent or qualified physics'))
        raise
