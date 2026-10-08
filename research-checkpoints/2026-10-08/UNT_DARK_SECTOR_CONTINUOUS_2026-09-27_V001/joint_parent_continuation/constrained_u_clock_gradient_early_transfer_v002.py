"""NEW constrained-U early-to-today Thomson/neutrino transfer, root execution only.
Retains every kinetic mode; exact dynamic block Schur Radau stages, no legacy imports.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import ast
import hashlib
import json
import math
import os
import time
import numpy as np

BASE=Path(__file__).resolve().parent
STEM='CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V002'
PROTOCOL_SHA='bdec58cd9c97a3ea1b129e4f1d9a1d2075afa2327c831bd9eccfdaf7eb6ed5ba'
PINS={'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_ADIABATIC_HIERARCHY_V001.md': '1014e8689d23c35b47c2e47b7e4bed2b2b3f0f329aca061b5df3586c249fc7d2', 'constrained_u_clock_gradient_flrw_reduced_chart_v002.py': '6d9878bb854bc7147aefcdcd358c6cecd16087a9577960f10686f5c4d17094b9', 'CONSTRAINED_U_CLOCK_GRADIENT_FLRW_REDUCED_CHART_V002.md': '5d644d9d07d6d2dbf4f44a20e329e30965ef0c558a052359bda102dc0b5aba1b', 'INVARIANT_CLOCK_GRADIENT_SHARED_ACTION_BUDGET_DOMAIN_AND_NORMAL_V003.md': 'e08b7166892ec59c863539d59b8d4b89c654081776d8870239ecc2c382572da0', 'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json': 'c92eb0ce131a61009361f2ead3f4db7522d3eabb22f7e3d472f0e4e0c116c24f', 'constrained_u_clock_gradient_recombination_pair_v002.py': '3cf9dbb9c68a1a1495e255de68cc399a2c2242a4edaa1acfc8bb870dd1cb29f4', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002.md': '09c2ee0071903b262c702cd8c91e1a9050d99f813c0a085ca042d630a537b54e', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RESULT.json': '008d86b296fc7c5856b5827b4cb3c0a7646e4cbe526cc0d7cd9013f02fbfeed4', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json': '1f210c196856d56294c13c35d7630e88f986015892df4f2856b5d2ce95dedcb4', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_DEFAULT_OUTPUT.json': '058ec2622e89bfd57c11c965444feabc0b3228b566373341b3d2b95836c168ba', 'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_HALF_OUTPUT.json': '58e5aafe79d42c88d14359c66f90372192d298a3a7d7d370c84daa38dacbfc57', 'invariant_clock_plasma_v001.py': '08cfd9e54759db07683bf652e32ad5aa69ec3006090f548e5d82b5678e8a6a28', 'invariant_clock_recombination_transfer_v002.py': '54674a431945eb7e17fc2b39af2324c923d8cfc5e991dc87a8cf96465dd1fa45', 'NETWORK_THERMAL_ASSUMPTIONS_AND_OBSERVABLES_V001.md': 'b2158042a2ce0867f5984e72cdea06b536975e1817fa48a9198272c0d394fffc', 'constrained_u_clock_gradient_early_transfer_v001.py': 'b537e10039eb776b2560c10eab0e84ed4e75a9c8ad34270cb17cb59711b0fb65', 'CONSTRAINED_U_CLOCK_GRADIENT_EARLY_TRANSFER_V001.md': 'fd98706ffadc7a11f64ebcd1d29342ab986795174b101fb06f61e300365ad14f'}
BACKGROUND_SPAN_SHA='eb224e42c6c567b0339b18cdf54a1d8c4f005810b6d6952fee9efee4983b7ec2'
RADAU_SPAN_SHA='59f38f2eb101e0404c12c5811124412855f21efde500b70f8d1d1792aeb509b5'
MPC=3.0856775814913673e22
CP=299792458.
KB,C,CBAR=.02,1.98,.99
K=.01
CURVATURE=1e-5
AI=1e-7
OMEGAS=(.1,1.,10.,100.)
TRIALS=[('BASE',4096,32,96,128,AI,'HALF',1),
        ('TIME',8192,32,96,128,AI,'HALF',1),
        ('MODES',8192,64,96,128,AI,'HALF',1),
        ('HIERARCHY',8192,32,128,160,AI,'HALF',1),
        ('START',8192,32,96,128,AI/2,'HALF',1),
        ('ATOMIC',8192,32,96,128,AI,'DEFAULT',1),
        ('THIN',8192,32,96,128,AI,'HALF',2)]
READOUT_NAMES=['photon_monopole_plus_Phi','photon_velocity','baryon_velocity','Weyl',
 'photon_quadrupole','polarization_source','neutrino_quadrupole','comoving_baryon_contrast',
 'comoving_baryon_density','comoving_radiation_density','comoving_clock_density',
 'polarization_density','hard_density','soft_density','normal_acceleration']
SEALS={}
CREATED={}
RUN_SOURCE_SHA=None
RUN_MANIFEST_SHA=None


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(name,obj):
    p=BASE/name
    with p.open('x') as f:json.dump(obj,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n')
    p.chmod(0o444);CREATED[str(p.resolve())]=sha(p);return sha(p)

def journal(event,**data):
    with (BASE/(STEM+'_JOURNAL.jsonl')).open('a') as f:
        f.write(json.dumps(dict(time=now(),event=event,owner='root',pid=os.getpid(),source_sha256=RUN_SOURCE_SHA,manifest_sha256=RUN_MANIFEST_SHA,**data),sort_keys=True)+'\n')

def seal(path,h):
    p=Path(path).resolve()
    if not p.is_relative_to(BASE.parent.parent.resolve()) or sha(p)!=h:raise AssertionError('Input seal/path '+str(p))
    if str(p) in SEALS and SEALS[str(p)]!=h:raise AssertionError('Conflicting input seal')
    SEALS[str(p)]=h

def recheck(source_sha):
    for p,h in dict(SEALS,**CREATED).items():
        if sha(p)!=h:raise AssertionError('Changed sealed prefix '+p)
    if sha(__file__)!=source_sha:raise AssertionError('Source changed')


def background(x, fixed):
    a = math.exp(x)
    eps, d0, OA, OB, OR, rG = (fixed[k] for k in ('eps', 'd0', 'OA', 'OB', 'OR', 'rG'))
    norm = 1/eps-math.log1p(1/eps)
    d = d0/a**3
    target = .5*eps*norm*d
    s = target
    for _ in range(5):
        qbar = math.sqrt(1+eps*s/(1+s))
        dq = eps/(2*qbar*(1+s)**2)
        s -= (s*qbar-target)/(qbar+s*dq)
    qbar = math.sqrt(1+eps*s/(1+s))
    dq = eps/(2*qbar*(1+s)**2)
    pex = (math.log1p(s)-s/(1+s))/norm
    cs = eps*s/(2+(4+3*eps)*s+2*(1+eps)*s*s)
    b, r = 1.5*OB/rG/a**3, 1.5*OR/rG/a**4
    w = 1.5*OA/rG*qbar*d
    rho = 1.5*OA/rG*(1+qbar*d-pex)
    h = math.sqrt((2/3)*(b+r+rho))
    den=2+(4+3*eps)*s+2*(1+eps)*s*s
    ds_dt=-3*h*s/(1+s*dq/qbar)
    cs_dt=eps*(2-2*(1+eps)*s*s)*ds_dt/(den*den)
    Q=fixed['Q0_over_Hstar']*qbar
    return dict(a=a, h=h, b=b, r=r, w=w, rho=rho, cs=cs, qbar=qbar,
                h_dt=-b-4*r/3-w, cs_dt=cs_dt, Q=Q,
                s=s, charge=d, charge_error=abs(2*qbar*s/(eps*norm)/d-1))


class Thermal:
    def __init__(self,arm,thin,fixed):
        name='CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_'+arm+'_OUTPUT.json'
        self.data=json.loads((BASE/name).read_text());self.rows=np.array([r[:3] for r in self.data['rows'][::thin]])
        if self.rows[0,0]!=0 or self.rows[-1,0]!=8000:raise AssertionError('Thermal table endpoints')
        self.nH=self.data['nH0_cm3']*1e6;self.fHe=self.data['fHe'];self.xfull=1+2*self.fHe
        self.hs=fixed['Hunit']*1000/MPC;self.T0=self.data['T0_K']
    def at(self,a):
        z=1/a-1
        if z>8000:xe,tm=self.xfull,self.T0/a
        elif z<0:raise ValueError('Thermal extrapolation below z0')
        else:xe,tm=(float(np.interp(z,self.rows[:,0],self.rows[:,i])) for i in (1,2))
        g=CP*6.6524587321e-29*self.nH*xe/a**3/self.hs
        cb2=5*1.380649e-23*tm*(1+self.fHe+xe)/(3*1.67262192369e-27*(1+4*self.fHe)*CP**2)
        return dict(g=g,xe=xe,Tm=tm,cold_pressure_diagnostic=cb2)


class Layout:
    def __init__(self,ns,lg,ln):
        self.ns,self.lg,self.ln=ns,lg,ln
        self.fg={l:9+l-2 for l in range(2,lg+1)};i=9+lg-1
        self.pol={l:i+l for l in range(lg+1)};i+=lg+1
        self.fn={l:i+l-2 for l in range(2,ln+1)};i+=ln-1
        self.z=np.arange(i,i+ns);self.zd=np.arange(i+ns,i+2*ns);self.n=i+2*ns
        self.core=list(range(9))+[self.fg[2],self.pol[0],self.pol[1],self.pol[2],self.fn[2],self.n,self.n+1]
        self.tails=[[self.fg[l] for l in range(3,lg+1)],
                    [self.pol[l] for l in range(3,lg+1)],
                    [self.fn[l] for l in range(3,ln+1)]]
    def names(self):
        names=['Psi','delta_b','Hstar_u_b','delta_gamma','Hstar_u_gamma',
               'delta_nu','Hstar_u_nu','delta_n_clock','Hstar_V_phi']
        names += ['F_gamma_'+str(l) for l in self.fg]+['G_gamma_'+str(l) for l in self.pol]+['F_nu_'+str(l) for l in self.fn]
        names += ['z_'+str(i) for i in range(self.ns)]+['zd_'+str(i) for i in range(self.ns)]
        return names


def coefficients(x,y,fixed,lay,therm,snodes,weights,omega,n_override=None):
    bg=background(x,fixed);h,b,r,w,c,Q=(bg[k] for k in ('h','b','r','w','cs','Q'))
    rg,rn=r*fixed['fgamma'],r*(1-fixed['fgamma']);q=K*CP/(1000*fixed['Hunit']*bg['a'])
    th=therm.at(bg['a']);g=th['g'];rb=3*b/(4*rg)
    psi,db,ub,dg,ug,dn,un,d,V=(y[i] for i in range(9))
    phi=psi-2*(rg*y[lay.fg[2]]+rn*y[lay.fn[2]])/q**2
    mom=b*ub+4*rg*ug/3+4*rn*un/3+w*V;psid=mom-h*phi
    Z=weights@y[lay.z];Zd=weights@y[lay.zd];R1=(weights*snodes**2)@y[lay.z]*omega**2
    alpha=omega**2*float(weights@snodes**2);L=Q*q;Ld=-h*(1+3*c)*L
    Ldd=(h*h*(1+3*c)**2-bg['h_dt']*(1+3*c)-3*h*bg['cs_dt'])*L
    v=Z/L;vd=(Zd-Ld*v)/L;Gamma=d+3*h*V;ncalc=vd-c*Gamma
    n=ncalc if n_override is None else n_override
    Vd=phi+c*Gamma;Bq=1+(fixed['ell_native']*q)**2;Delta=alpha+C*Q*Q/KB+CBAR*Q*Q*q*q*c/w
    Fv=(-h*n-C*(Zd+2*h*Z)/(KB*q)+bg['cs_dt']*Gamma
        +c*(3*psid-q*q*V+3*bg['h_dt']*V+3*h*Vd))
    sigma=(L*Fv+2*Ld*vd+Ldd*v+3*h*Zd+Bq*R1-alpha*q*n)/Delta
    return dict(bg=bg,h=h,b=b,rg=rg,rn=rn,w=w,c=c,Q=Q,q=q,thermal=th,g=g,rb=rb,
                phi=phi,psi=psi,psid=psid,mom=mom,Z=Z,Zd=Zd,L=L,Ld=Ld,Ldd=Ldd,
                v=v,vd=vd,Gamma=Gamma,n=n,ncalc=ncalc,Vd=Vd,Bq=Bq,Delta=Delta,sigma=sigma)


def rates(x,y,fixed,lay,therm,snodes,weights,omega,n_override=None,sigma_override=None):
    f=coefficients(x,y,fixed,lay,therm,snodes,weights,omega,n_override)
    h,b,rg,rn,w,c,Q,q,g,rb=(f[k] for k in ('h','b','rg','rn','w','c','Q','q','g','rb'))
    phi,psid,n=(f[k] for k in ('phi','psid','n'));sigma=f['sigma'] if sigma_override is None else sigma_override
    out=np.zeros_like(y);psi,db,ub,dg,ug,dn,un,d,V=(y[i] for i in range(9))
    out[0]=psid;out[1]=3*psid-q*q*ub;out[2]=phi+g/rb*(ug-ub)
    out[3]=4*psid-4*q*q*ug/3;out[4]=h*ug+phi+dg/4-y[lay.fg[2]]/2+g*(ub-ug)
    out[5]=4*psid-4*q*q*un/3;out[6]=h*un+phi+dn/4-y[lay.fn[2]]/2
    out[7]=3*psid-q*q*V-CBAR*Q*q*sigma/w;out[8]=f['Vd']
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    for indices,velocity,collision in [(lay.fg,ug,g),(lay.fn,un,0.)]:
        for l,i in indices.items():
            before=4*q*velocity/3 if l==2 else y[indices[l-1]]
            after=y[indices[l+1]] if l<max(indices) else 0.
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


def initial(x,fixed,lay,therm,snodes,weights):
    bg=background(x,fixed);h,b,r,w,c=(bg[k] for k in ('h','b','r','w','cs'))
    rg,rn=r*fixed['fgamma'],r*(1-fixed['fgamma']);q=K*CP/(1000*fixed['Hunit']*bg['a']);g=therm.at(bg['a'])['g']
    slip=1+4*rn/(15*h*h)+32*rg/(45*h*g);phi=CURVATURE/(slip+.5);psi=slip*phi;V=phi/(2*h)
    B=b+4*r/3+w;d=-q*q*psi/(B+.5*KB*q*q*c)-3*h*V
    y=np.zeros(lay.n);y[:9]=[psi,d,V,4*d/3,V,4*d/3,V,d,V]
    y[lay.fg[2]]=32*q*q*V/(45*g);y[lay.pol[0]]=1.25*y[lay.fg[2]];y[lay.pol[2]]=.25*y[lay.fg[2]]
    y[lay.pol[1]]=q*(y[lay.pol[0]]-2*y[lay.pol[2]])/(3*g)
    y[lay.fn[2]]=2/15*(q/h)**2*phi
    for l in range(3,lay.lg+1):
        y[lay.fg[l]]=q*l*y[lay.fg[l-1]]/((2*l+1)*g)
        y[lay.pol[l]]=q*l*y[lay.pol[l-1]]/((2*l+1)*g)
    for l in range(3,lay.ln+1):y[lay.fn[l]]=(q/h)*y[lay.fn[l-1]]/(2*l+1)
    return y


def stage_matrix(x,fixed,lay,therm,snodes,weights,omega):
    na=lay.n+2;eye=np.eye(na);y=eye[:lay.n,:]
    out,f=rates(x,y,fixed,lay,therm,snodes,weights,omega,eye[lay.n],eye[lay.n+1])
    mat=np.zeros((na,na));mat[:lay.n]=out/f['h']
    mat[lay.n]=eye[lay.n]-f['ncalc'];mat[lay.n+1]=eye[lay.n+1]-f['sigma']
    return mat


def tridiagonal_blocks(K,B):
    n=len(K)//2;D=[K[2*i:2*i+2,2*i:2*i+2].copy() for i in range(n)];R=B.reshape(n,2,-1).copy();U=[]
    for i in range(n-1):U.append(K[2*i:2*i+2,2*i+2:2*i+4])
    for i in range(1,n):
        lower=K[2*i:2*i+2,2*i-2:2*i]
        solved=np.linalg.solve(D[i-1],np.concatenate((U[i-1],R[i-1]),axis=1))
        D[i]-=lower@solved[:,:2];R[i]-=lower@solved[:,2:]
    X=np.empty_like(R);X[-1]=np.linalg.solve(D[-1],R[-1])
    for i in range(n-2,-1,-1):X[i]=np.linalg.solve(D[i],R[i]-U[i]@X[i+1])
    return X.reshape(2*n,-1)


def block_stage_solve(Kmat,rhs,lay):
    na=lay.n+2;core=np.array(lay.core+[na+i for i in lay.core]);S=Kmat[np.ix_(core,core)].copy();R=rhs[core].copy();saved=[]
    owned=set(core.tolist())
    for tail in lay.tails:
        idx=np.array([i for t in tail for i in (t,na+t)]);owned.update(idx.tolist())
        B=np.column_stack((Kmat[np.ix_(idx,core)],rhs[idx]))
        V=tridiagonal_blocks(Kmat[np.ix_(idx,idx)],B)
        Cc=Kmat[np.ix_(core,idx)];S-=Cc@V[:,:len(core)];R-=Cc@V[:,-1];saved.append((idx,V))
    groups=np.array([[int(z),na+int(z),int(v),na+int(v)] for z,v in zip(lay.z,lay.zd)])
    owned.update(groups.ravel().tolist())
    if len(owned)!=len(rhs):raise AssertionError('Exact stage partition')
    matrices=Kmat[groups[:,:,None],groups[:,None,:]]
    B=np.concatenate((Kmat[groups[:,:,None],core[None,None,:]],rhs[groups][:,:,None]),axis=2)
    V=np.linalg.solve(matrices,B)
    for idx,res in zip(groups,V):
        Cc=Kmat[np.ix_(core,idx)];S-=Cc@res[:,:len(core)];R-=Cc@res[:,-1];saved.append((idx,res))
    solution=np.zeros(len(rhs));solution[core]=np.linalg.solve(S,R)
    for idx,V in saved:solution[idx]=V[:,-1]-V[:,:len(core)]@solution[core]
    return solution


def radau_step(y,x,dx,fixed,lay,therm,snodes,weights,omega,check=False,dense=False):
    # Coefficients identical to authenticated resident radau_step; dynamic augmented stages only.
    na=lay.n+2;m1=stage_matrix(x+dx/3,fixed,lay,therm,snodes,weights,omega);m2=stage_matrix(x+dx,fixed,lay,therm,snodes,weights,omega)
    eye=np.eye(na);eye[lay.n:]=0.
    Kmat=np.block([[eye-dx*(5/12)*m1,dx*m2/12],[-dx*.75*m1,eye-dx*.25*m2]])
    Kmat[lay.n:na]=0.;Kmat[lay.n:na,:na]=m1[lay.n:]
    Kmat[na+lay.n:]=0.;Kmat[na+lay.n:,na:]=m2[lay.n:]
    rhs=np.tile(np.concatenate((y,[0.,0.])),2);stages=block_stage_solve(Kmat,rhs,lay)
    error=0.
    if check:
        residual=Kmat@stages-rhs;scale=np.abs(Kmat)@np.abs(stages)+np.abs(rhs)
        error=float(np.max(abs(residual)/np.maximum(scale,abs(CURVATURE)*1e-16)))
    derror=0.
    if dense:
        independent=np.linalg.solve(Kmat,rhs)
        derror=float(np.max(abs(stages-independent))/max(float(np.max(abs(independent))),CURVATURE*1e-16))
    return stages[na:na+lay.n],error,derror


def snapshot(x,y,fixed,lay,therm,snodes,weights,omega):
    dy,f=rates(x,y,fixed,lay,therm,snodes,weights,omega)
    h,b,rg,rn,w,c,Q,q=(f[k] for k in ('h','b','rg','rn','w','c','Q','q'))
    psi,db,ub,dg,ug,dn,un,d,V=(y[i] for i in range(9));n=f['n'];sigma=f['sigma'];P=.5*KB*q*n+CBAR*f['Z']
    nt=np.array([q*q*psi,3*h*f['mom'],b*db,rg*dg,rn*dn,w*d,-q*P])
    nf=q*q*CURVATURE*1e-10;ne=float(abs(sum(nt))/max(sum(abs(nt)),nf))
    vdd=(weights@dy[lay.zd]-2*f['Ld']*f['vd']-f['Ldd']*f['v'])/f['L']
    nd=vdd-f['bg']['cs_dt']*f['Gamma']-c*(dy[7]+3*f['bg']['h_dt']*V+3*h*dy[8])
    et=np.array([.5*KB*q*nd,-.5*KB*h*q*n,CBAR*f['Zd'],2*h*P,CBAR*Q*sigma])
    ef=.5*KB*q*CURVATURE*max(h,Q,omega)*1e-10;ee=float(abs(sum(et))/max(sum(abs(et)),ef))
    phid=f['psid']-2*(rg*(dy[lay.fg[2]]-2*h*y[lay.fg[2]])+rn*(dy[lay.fn[2]]-2*h*y[lay.fn[2]]))/q**2
    momd=b*(dy[2]-3*h*ub)+4*rg*(dy[4]-4*h*ug)/3+4*rn*(dy[6]-4*h*un)/3+w*(dy[8]-3*h*(1+c)*V)
    psidd=momd-f['bg']['h_dt']*f['phi']-h*phid
    tt=np.array([psidd,h*phid,3*h*f['psid'],(2*f['bg']['h_dt']+3*h*h)*f['phi'],q*q*(psi-f['phi'])/3,-c*w*d,-(rg*dg+rn*dn)/3])
    tf=CURVATURE*max(h*h,q*q)*1e-12;te=float(abs(sum(tt))/max(sum(abs(tt)),tf))
    Eb=b*(db+3*h*ub);Eg=rg*(dg+4*h*ug);En=rn*(dn+4*h*un);Ec=w*(d+3*h*V);Ep=-q*P;S=rg*y[lay.fg[2]]+rn*y[lay.fn[2]]
    rat=dict(denominator=Eb,normal_over_denominator=float(sum(nt)/Eb) if Eb else None)
    if Eb:
        ref=-Eb/q**2;other=Eg+En+Ec+Ep
        rat.update(force_metric=.99*f['phi']/ref,lens_metric=.99*(f['phi']+psi)/(2*ref),
                   force_source=.99*(1+(other+2*S)/Eb),lens_source=.99*(1+(other+S)/Eb),refusal=None)
    else:rat.update(force_metric=None,lens_metric=None,force_source=None,lens_source=None,refusal='ZERO_SIGNED_BARYON_DENOMINATOR')
    qbar=f['bg']['qbar'];ss=f['bg']['s'];eps=fixed['eps']
    lower=eps*ss/((1+ss)*(qbar+1)*qbar);upper=eps/((1+ss)*(math.sqrt(1+eps)+qbar)*qbar);gap=min(lower,upper)
    phase_fraction=abs(c*d)/gap;pi=V-f['v']
    amplitude=max(abs(psi),abs(f['phi']),abs(db),abs(dg),abs(dn),abs(d),abs(q*ub),abs(q*ug),abs(q*un),abs(q*V),abs(q*pi))
    heads=dict(lower_gap=lower,upper_gap=upper,phase_rate=c*d,phase_rate_fraction=phase_fraction,
        phase_velocity=q*V,U_tilt=q*pi,relative_velocity=q*f['v'],phase_square_over_gap=(q*V)**2/(2*gap),
        relative_square_over_gap=(q*f['v'])**2/(2*gap),maximum_linear_amplitude=amplitude,
        sampled_absolute_curvature_ceiling=min(.01*CURVATURE/amplitude if amplitude else 1.,CURVATURE/phase_fraction if phase_fraction else 1.),
        inside_sampled_linear_domain=amplitude<.01 and phase_fraction<1)
    Pi=y[lay.fg[2]]+y[lay.pol[0]]+y[lay.pol[2]]
    reads=[dg/4+f['phi'],q*ug,q*ub,psi+f['phi'],y[lay.fg[2]],Pi,y[lay.fn[2]],db+3*h*ub,
           Eb,Eg+En,Ec,Ep,-.5*KB*q*q*n,-CBAR*q*f['Z'],q*n]
    return dict(x=x,a=math.exp(x),state=y.tolist(),background=f['bg'],thermal=f['thermal'],
        Phi=float(f['phi']),Psi=float(psi),Q=float(Q),reaction_denominator=float(f['Delta']),n_U=float(n),
        sigma=float(sigma),P=float(P),pi_U=float(pi),Z=float(f['Z']),Zd=float(f['Zd']),
        readouts=[float(v) for v in reads],normal_terms=nt.tolist(),normal_floor=nf,normal_error=ne,
        omitted_Euler_terms=et.tolist(),omitted_Euler_floor=ef,omitted_Euler_error=ee,
        trace_terms=tt.tolist(),trace_floor=tf,trace_error=te,domain_heads=heads,
        signed_sources=dict(baryon=Eb,photon=Eg,neutrino=En,phase=Ec,polarization=Ep,shear=S),source_ratios=rat)


def authenticate():
    for n,h in dict(PINS,**{STEM+'.md':PROTOCOL_SHA}).items():seal(BASE/n,h)
    parent=(BASE/'constrained_u_clock_gradient_flrw_reduced_chart_v002.py').read_text()
    f=next(n for n in ast.parse(parent).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    source=ast.get_source_segment(parent,f)
    own=Path(__file__).read_text();f2=next(n for n in ast.parse(own).body if isinstance(n,ast.FunctionDef) and n.name=='background')
    if ast.get_source_segment(own,f2)!=source or hashlib.sha256(source.encode()).hexdigest()!=BACKGROUND_SPAN_SHA:raise AssertionError('Background implementation identity')
    old=(BASE/'invariant_clock_plasma_v001.py').read_text();f3=next(n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef) and n.name=='radau_step')
    if hashlib.sha256(ast.get_source_segment(old,f3).encode()).hexdigest()!=RADAU_SPAN_SHA:raise AssertionError('Radau coefficient implementation')
    cal=json.loads((BASE/'INVARIANT_CLOCK_JOINT_CALIBRATION_V003_RESULT.json').read_text())
    for p,h in cal['hashes'].items():seal(p,h)
    pair=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RESULT.json').read_text())
    pr=json.loads((BASE/'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RECEIPT.json').read_text())
    if (pair['status']!=pr['status'] or pair['status']!='NEW_ATOMIC_PAIR_ARITHMETIC_PASS'
        or len(pair['numerical_gates'])!=12 or not all(t['passed'] for t in pair['numerical_gates'])
        or pair['lineage']!=pr['lineage'] or pr['result_sha256']!=PINS['CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_RESULT.json']):raise AssertionError('NEW atomic parent status/identity')
    for p,h in pr['lineage']['input_sha256'].items():seal(p,h)
    for p,h in pr['output_sha256'].items():seal(p,h)
    seal(BASE/'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_JOURNAL.jsonl',pr['journal_sha256'])
    events=[json.loads(s) for s in (BASE/'CONSTRAINED_U_CLOCK_GRADIENT_RECOMBINATION_PAIR_V002_JOURNAL.jsonl').read_text().splitlines()]
    if [s['event'] for s in events]!=['OWNER_START','CHECKPOINT','CHECKPOINT','OWNER_COMPLETE'] or [s['arm'] for s in events[1:3]]!=['DEFAULT','HALF']:raise AssertionError('Atomic natural closure census')
    ctx=cal['trials'][-1]['atomic_invocation']['context'];sel=cal['selected'];old=cal['fixed']
    fixed=dict(Hunit=sel['Hunit'],OA=old['omega_A'],OB=sel['OB'],OR=ctx['OR'],d0=old['d0'],eps=old['eps'],
        rG=.98/.99,Q0_over_Hstar=old['Q0_over_H0'],ell_native=100e-6*sel['Hunit']/299792.458,
        fgamma=ctx['og']/ctx['OR'],YHe_fixture=sel['YHe'],Neff_fixture=sel['Neff'],curvature=CURVATURE,k_Mpc_inverse=K)
    if pair['lineage']['fixed']!={k:fixed[k] for k in pair['lineage']['fixed']}:raise AssertionError('Same physical NEW atomic background')
    return fixed


def output_targets():
    x0=math.log(AI);return sorted(set([x0+k*(-x0)/64 for k in range(65)]+[-math.log(1+z) for z in (8000.,1100.,800.)]))



def finite_tree(value):
    if isinstance(value,dict):return all(finite_tree(v) for v in value.values())
    if isinstance(value,list):return all(finite_tree(v) for v in value)
    if isinstance(value,float):return math.isfinite(value)
    return value is None or isinstance(value,(str,int,bool))


def validate_checkpoint(saved,meta,n,previous=None):
    if (set(saved)!=set(('meta','n','state','snapshots','step_errors','dense_errors')) or saved['meta']!=meta
        or type(saved['n']) is not int or saved['n']!=n or not finite_tree(saved)):raise AssertionError('Every CP payload schema/finite lineage')
    shape=meta['state_shape'];state=saved['state'];snaps=saved['snapshots']
    if (not isinstance(state,list) or len(state)!=shape[0] or any(not isinstance(r,list) or len(r)!=shape[1] or any(type(v) not in (int,float) for v in r) for r in state)
        or any(not isinstance(saved[k],list) or len(saved[k])!=4 or any(type(v) not in (int,float) or v<0 for v in saved[k]) for k in ('step_errors','dense_errors'))):raise AssertionError('Every CP state/error dimensions')
    steps=meta['spec'][1];x0=math.log(AI);dx=-x0/steps;endpoint=x0+n*dx
    expected=[x for x in output_targets() if x<=endpoint+1e-14]
    if not isinstance(snaps,list) or not snaps or [ss.get('x') for ss in snaps]!=expected:raise AssertionError('Every CP ordered snapshot prefix')
    casekeys=set(('x','a','state','background','thermal','Phi','Psi','Q','reaction_denominator','n_U','sigma','P','pi_U','Z','Zd','readouts','normal_terms','normal_floor','normal_error','omitted_Euler_terms','omitted_Euler_floor','omitted_Euler_error','trace_terms','trace_floor','trace_error','domain_heads','signed_sources','source_ratios'))
    for ss in snaps:
        if set(ss)!=set(('x','cases')) or not isinstance(ss['cases'],list) or len(ss['cases'])!=4:raise AssertionError('Every CP snapshot schema')
        for cc in ss['cases']:
            if (set(cc)!=casekeys or cc['x']!=ss['x'] or cc['a']!=math.exp(ss['x']) or not isinstance(cc['state'],list)
                or len(cc['state'])!=shape[1] or any(type(v) not in (int,float) for v in cc['state'])
                or len(cc['readouts'])!=len(READOUT_NAMES) or len(cc['normal_terms'])!=7 or len(cc['omitted_Euler_terms'])!=5
                or len(cc['trace_terms'])!=7 or cc['reaction_denominator']<=0):raise AssertionError('Every CP full snapshot state/fields')
    if snaps[-1]['x']!=endpoint or [cc['state'] for cc in snaps[-1]['cases']]!=state:raise AssertionError('Every CP endpoint state identity')
    if previous is not None:
        if snaps[:len(previous['snapshots'])]!=previous['snapshots'] or any(saved[k][i]<previous[k][i] for k in ('step_errors','dense_errors') for i in range(4)):raise AssertionError('CP immutable snapshot/error prefix')


def validate_runtime(lineage,require_complete=False,allow_complete=False):
    mp=BASE/(STEM+'_MANIFEST.json');mh=sha(mp)
    if json.loads(mp.read_text())!=lineage:raise AssertionError('Runtime manifest identity')
    jp=BASE/(STEM+'_JOURNAL.jsonl');events=[json.loads(line) for line in jp.read_text().splitlines()] if jp.exists() else []
    expected=[(spec[0],n) for spec in TRIALS for n in range(0,spec[1]+1,512)];actual=[];owner=None;seen_files=set();previous={}
    binding=set(('time','event','owner','pid','source_sha256','manifest_sha256'))
    specs={spec[0]:spec for spec in TRIALS}
    for event_index,ev in enumerate(events):
        if (not isinstance(ev,dict) or ev.get('owner')!='root' or type(ev.get('pid')) is not int or ev['pid']<=0
            or ev.get('source_sha256')!=lineage['source_sha256'] or ev.get('manifest_sha256')!=mh
            or not isinstance(ev.get('time'),str) or datetime.fromisoformat(ev['time']).utcoffset() is None):raise AssertionError('Journal exact root/source/manifest/PID/time')
        if ev['event']=='OWNER_START':
            if set(ev)!=binding:raise AssertionError('Owner event exact schema')
            owner=ev['pid'];continue
        if ev['event']=='OWNER_COMPLETE':
            if (not allow_complete or event_index!=len(events)-1 or owner is None or ev['pid']!=owner
                or set(ev)!=binding|set(('status','result_sha256','gates','passed')) or actual!=expected
                or ev['gates']!=527 or type(ev['passed']) is not int or not 0<=ev['passed']<=527
                or ev['status']!=('NEW_EARLY_TRANSFER_ARITHMETIC_PASS' if ev['passed']==527 else 'NEW_EARLY_TRANSFER_ARITHMETIC_FAILED')
                or ev['result_sha256']!=sha(BASE/(STEM+'_RESULT.json'))):raise AssertionError('Exact complete owner/output/census closure')
            continue
        if ev['event']!='CHECKPOINT' or owner is None or ev['pid']!=owner or set(ev)!=binding|set(('trial','n','payload','sha256','commit_sha256')):raise AssertionError('Journal checkpoint owner/schema/status')
        pair=(ev['trial'],ev['n']);actual.append(pair)
        if type(ev['n']) is not int or actual!=expected[:len(actual)]:raise AssertionError('Global ordered trial/checkpoint census')
        spec=specs[ev['trial']];lay=Layout(*spec[2:5]);meta=dict(lineage=lineage,spec=list(spec),state_shape=[4,lay.n],state_names=lay.names())
        pn=STEM+'_'+ev['trial']+'_CP_'+str(ev['n']).zfill(6)+'.json';cn=pn[:-5]+'_COMMIT.json'
        if (ev['payload']!=pn or any(not isinstance(ev[k],str) or len(ev[k])!=64 or any(c not in '0123456789abcdef' for c in ev[k]) for k in ('sha256','commit_sha256'))):raise AssertionError('Checkpoint exact payload/hash syntax')
        co=BASE/cn;seal(co,ev['commit_sha256']);seal(BASE/pn,ev['sha256']);commit=json.loads(co.read_text())
        if commit!=dict(meta=meta,n=ev['n'],payload=pn,sha256=ev['sha256']):raise AssertionError('Checkpoint commit/source/meta binding')
        saved=json.loads((BASE/pn).read_text());validate_checkpoint(saved,meta,ev['n'],previous.get(ev['trial']));previous[ev['trial']]=saved
        seen_files.update((pn,cn))
    if events and events[0]['event']!='OWNER_START':raise AssertionError('Initial owner journal event')
    files=set(p.name for p in BASE.glob(STEM+'_*_CP_*.json'))
    if files!=seen_files or (require_complete and actual!=expected):raise AssertionError('Global complete checkpoint/journal/no-orphan census')
    return events


def trial(spec,fixed,lineage):
    tick=time.monotonic();label,steps,ns,lg,ln,start,arm,thin=spec
    lay=Layout(ns,lg,ln);therm=Thermal(arm,thin,fixed);xn,wn=np.polynomial.legendre.leggauss(ns);snodes=(xn+1)/2;weights=wn*(xn+1)/2
    if min(snodes)<=0 or min(weights)<=0:raise AssertionError('Positive retained mode spectrum')
    x0=math.log(AI);dx=-x0/steps;targets=output_targets();cpstem=STEM+'_'+label+'_CP_'
    commits=sorted(BASE.glob(cpstem+'*_COMMIT.json'));payloads=set(p.name for p in BASE.glob(cpstem+'*.json') if not p.name.endswith('_COMMIT.json'))
    if payloads!={p.name.replace('_COMMIT.json','.json') for p in commits}:raise AssertionError('Orphan CP prefix')
    meta=dict(lineage=lineage,spec=list(spec),state_shape=[4,lay.n],state_names=lay.names())
    snapshots=[];step_errors=[0.]*4;dense_errors=[0.]*4;n0=0
    if commits:
        last=int(commits[-1].stem.rsplit('_',2)[-2]);expected=[cpstem+str(n).zfill(6)+'_COMMIT.json' for n in range(0,last+1,512)]
        if [p.name for p in commits]!=expected or last>steps:raise AssertionError('CP census')
        saved=json.loads((BASE/json.loads(commits[-1].read_text())['payload']).read_text())
        validate_checkpoint(saved,meta,last)
        y=np.array(saved['state']);snapshots=saved['snapshots'];step_errors=saved['step_errors'];dense_errors=saved['dense_errors'];n0=last
    else:
        y=np.stack([initial(math.log(start),fixed,lay,therm,snodes,weights) for _ in OMEGAS])
        if start<AI:
            pre0=math.log(start);pre_dx=(x0-pre0)/512
            for n in range(512):
                for i,om in enumerate(OMEGAS):y[i],err,de=radau_step(y[i],pre0+n*pre_dx,pre_dx,fixed,lay,therm,snodes,weights,om,n%64==0);step_errors[i]=max(step_errors[i],err)
        snapshots=[dict(x=x0,cases=[snapshot(x0,y[i],fixed,lay,therm,snodes,weights,om) for i,om in enumerate(OMEGAS)])]
    def checkpoint(n):
        name=cpstem+str(n).zfill(6)+'.json';h=write(name,dict(meta=meta,n=n,state=y.tolist(),snapshots=snapshots,step_errors=step_errors,dense_errors=dense_errors))
        co=name[:-5]+'_COMMIT.json';ch=write(co,dict(meta=meta,n=n,payload=name,sha256=h))
        journal('CHECKPOINT',trial=label,n=n,payload=name,sha256=h,commit_sha256=ch)
        print(json.dumps(dict(trial=label,completed_steps=n,total_steps=steps,elapsed=time.monotonic()-tick)),flush=True)
    if not commits:checkpoint(0)
    for n in range(n0,steps):
        left=x0+n*dx;right=x0+(n+1)*dx
        cuts=[x for x in targets if left<x<=right]
        points=cuts+([right] if not cuts or cuts[-1]!=right else [])
        for dest in points:
            width=dest-left
            for i,om in enumerate(OMEGAS):
                y[i],err,de=radau_step(y[i],left,width,fixed,lay,therm,snodes,weights,om,n%512==0,n==0);step_errors[i]=max(step_errors[i],err);dense_errors[i]=max(dense_errors[i],de)
            left=dest
            if dest in cuts:snapshots.append(dict(x=dest,cases=[snapshot(dest,y[i],fixed,lay,therm,snodes,weights,om) for i,om in enumerate(OMEGAS)]))
        if not np.all(np.isfinite(y)):raise ArithmeticError('Nonfinite full dynamical state')
        if (n+1)%512==0:checkpoint(n+1)
    if [s['x'] for s in snapshots]!=targets:raise AssertionError('Full 68-target census')
    return dict(label=label,spec=list(spec),state_names=lay.names(),snodes=snodes.tolist(),weights=weights.tolist(),
        snapshots=snapshots,step_errors=step_errors,dense_errors=dense_errors,elapsed_seconds=time.monotonic()-tick)


def main():
    global RUN_SOURCE_SHA,RUN_MANIFEST_SHA
    tick=time.monotonic();source_sha=sha(__file__)
    for suffix in ('_RESULT.json','_REPORT.md','_RECEIPT.json'):
        if (BASE/(STEM+suffix)).exists():raise FileExistsError('Completed prefix, no overwrite')
    fixed=authenticate();lineage=dict(source_sha256=source_sha,inputs=dict(SEALS),fixed=fixed,trials=[list(t) for t in TRIALS],omegas=list(OMEGAS),targets=output_targets(),numpy_version=np.__version__)
    mp=BASE/(STEM+'_MANIFEST.json')
    if mp.exists():
        if json.loads(mp.read_text())!=lineage:raise AssertionError('Manifest lineage changed')
        seal(mp,sha(mp))
    else:
        if (BASE/(STEM+'_JOURNAL.jsonl')).exists() or any(BASE.glob(STEM+'_*_CP_*.json')) or any(BASE.glob(STEM+'_FAILED_*.json')):raise AssertionError('Pre-manifest orphan runtime prefix; preserve/refuse')
        write(mp.name,lineage)
    RUN_SOURCE_SHA=source_sha;RUN_MANIFEST_SHA=sha(mp)
    jp=BASE/(STEM+'_JOURNAL.jsonl');validate_runtime(lineage)
    journal('OWNER_START')
    rows=[]
    for spec in TRIALS:
        validate_runtime(lineage);recheck(source_sha);rows.append(trial(spec,fixed,lineage));recheck(source_sha)
    validate_runtime(lineage,require_complete=True)
    gates=[]
    def check(name,error,tolerance,**ids):
        gates.append(dict(name=name,error=float(error),tolerance=tolerance,passed=math.isfinite(error) and error<=tolerance,**ids))
    for tr in rows:
        check('positive_spectrum_normalization',abs(sum(tr['weights'])-1),1e-13,trial=tr['label'])
        check('charge_root',max(s['cases'][0]['background']['charge_error'] for s in tr['snapshots']),1e-13,trial=tr['label'])
        for i,om in enumerate(OMEGAS):
            for key,tol in [('normal_error',1e-5),('trace_error',1e-10),('omitted_Euler_error',1e-10)]:
                check(key,max(s['cases'][i][key] for s in tr['snapshots']),tol,trial=tr['label'],omega=om)
            check('dynamic_stage_residual',tr['step_errors'][i],2e-11,trial=tr['label'],omega=om)
            check('dynamic_block_vs_full_dense',tr['dense_errors'][i],2e-11,trial=tr['label'],omega=om)
            if any(s['cases'][i]['reaction_denominator']<=0 for s in tr['snapshots']):raise AssertionError('Positive reaction action branch')
    fine=np.array([[c['readouts'] for c in s['cases']] for s in rows[1]['snapshots']])
    comparisons=[]
    for arm,label,tol in [(0,'time',1e-3),(2,'modes',1e-3),(3,'hierarchy',1e-3),(4,'start',2e-4),(5,'atomic',5e-5),(6,'thinning',5e-5)]:
        other=np.array([[c['readouts'] for c in s['cases']] for s in rows[arm]['snapshots']])
        den=np.maximum(np.max(abs(fine),axis=0),CURVATURE*1e-8);err=np.max(abs(other-fine),axis=0)/den
        for i,om in enumerate(OMEGAS):
            for j,key in enumerate(READOUT_NAMES):check(label+'_refinement',err[i,j],tol,omega=om,variable=key)
        comparisons.append(dict(label=label,reference='TIME',signed_endpoint_difference=(other[-1]-fine[-1]).tolist(),
            maximum_trace_difference=np.max(abs(other-fine),axis=0).tolist(),normalization=den.tolist(),normalized_error=err.tolist()))
    for i,om in enumerate(OMEGAS):
        s=rows[0]['snapshots'][0]['cases'][i];bg=s['background'];y=s['state'];h=bg['h'];q=K*CP/(1000*fixed['Hunit']*AI)
        check('seed_curvature',abs((s['Psi']+h*y[8])/CURVATURE-1),2e-13,omega=om)
        check('seed_exact_normal',s['normal_error'],1e-10,omega=om)
        check('seed_exact_shear',abs((s['Psi']-s['Phi']-2*s['signed_sources']['shear']/q**2)/CURVATURE),1e-13,omega=om)
    thermal=Thermal('HALF',1,fixed);check('fully_ionized_join',abs(thermal.rows[-1,1]/thermal.xfull-1),1e-5)
    if len(gates)!=527:raise AssertionError('Frozen527 numerical gate census')
    qualified=all(g['passed'] for g in gates);status='NEW_EARLY_TRANSFER_ARITHMETIC_PASS' if qualified else 'NEW_EARLY_TRANSFER_ARITHMETIC_FAILED'
    end=rows[1]['snapshots'][-1]['cases'];resolution=[]
    for i,om in enumerate(OMEGAS):
        src=end[i]['signed_sources'];den=src['baryon'];dt=rows[0]['snapshots'][-1]['cases'][i]['signed_sources']['baryon']-den
        ds=rows[2]['snapshots'][-1]['cases'][i]['signed_sources']['baryon']-den
        resolution.append(dict(omega=om,signed_baryon_denominator=den,time_change=dt,mode_change=ds,
            denominator_resolution='resolved' if abs(den)>3*max(abs(dt),abs(ds)) else 'unresolved',
            force=end[i]['source_ratios'],scope='Actual declared early-history source; no halo/observational fit'))
    result=dict(status=status,all_numerical_gates_passed=qualified,manifest=lineage,readout_names=READOUT_NAMES,
        rows=rows,comparisons=comparisons,numerical_gates=gates,endpoint_source_resolution=resolution,
        elapsed_seconds=time.monotonic()-tick,scope='NEW-action conditional curvature transfer; cold baryons/massless thermal neutrinos/oldYHeNeff fixture; no reionization/C_l/formation calibration')
    recheck(source_sha);rh=write(STEM+'_RESULT.json',result)
    lines=['# NEW constrained-U early transfer V002','',status,f'{sum(g["passed"] for g in gates)}/{len(gates)} frozen numerical controls PASS.','',
      'One k=.01, Rstar=1e-5, four inertias, seven full-state refinement trials, fresh .99-background recombination.',
      'Ordinary hierarchy and dynamical kinetic modes retained; no old-action transfer imported, fit or preferred inertia.',
      'Cold baryons and inherited thermal YHe/Neff are disclosed fixtures; no angular/data/merger/native-formation qualification.','',
      '| omega/Hstar | comoving db contrast | Weyl | phase density | polarization density | force/GN | lens/GN | sampled linear domain |','|---|---|---|---|---|---|---|---|']
    for om,s in zip(OMEGAS,end):
        r=s['readouts'];a=s['source_ratios'];lines.append(f"| {om} | {r[7]:.12g} | {r[3]:.12g} | {r[10]:.12g} | {r[11]:.12g} | {a['force_metric']} | {a['lens_metric']} | {s['domain_heads']['inside_sampled_linear_domain']} |")
    lines+=['','All signed sources/shear, full raw mode/hierarchy snapshots, ratio denominators/refusals, square/gap diagnostics and failures remain in JSON.',
      'Numerical qualification refers to these declared observable traces, not relative accuracy of every tiny modal coefficient or an infinite-hierarchy certificate.']
    report=BASE/(STEM+'_REPORT.md')
    with report.open('x') as f:f.write('\n'.join(lines)+'\n')
    report.chmod(0o444);CREATED[str(report.resolve())]=sha(report);recheck(source_sha)
    journal('OWNER_COMPLETE',status=status,result_sha256=rh,gates=len(gates),passed=sum(g['passed'] for g in gates))
    validate_runtime(lineage,require_complete=True,allow_complete=True)
    write(STEM+'_RECEIPT.json',dict(status=status,source_sha256=source_sha,lineage=lineage,
        manifest_sha256=sha(mp),result_sha256=rh,report_sha256=sha(report),journal_sha256=sha(jp),checkpoint_seals={p:h for p,h in dict(SEALS,**CREATED).items() if '_CP_' in p}))
    recheck(source_sha);print(json.dumps(dict(status=status,result_sha256=rh,elapsed_seconds=result['elapsed_seconds'])),flush=True)
    return 0 if qualified else 3


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--execute',action='store_true')
    if not ap.parse_args().execute:raise SystemExit('Root alone launches --execute')
    if any((BASE/(STEM+s)).exists() for s in ('_RESULT.json','_REPORT.md','_RECEIPT.json')):raise SystemExit('Completed prefix; no overwrite or extra error mutation')
    try:raise SystemExit(main())
    except Exception as exc:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        write(STEM+'_FAILED_'+stamp+'.json',dict(status='EXECUTION_ERROR_PRESERVED',error=repr(exc),pid=os.getpid(),time=now(),source_sha256=sha(__file__)))
        raise
