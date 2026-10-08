"""Inert finite-slice Q=0 transfer producer. Root freezes/runs; stdout only."""
import os
for _thread_var in ["OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS"]:
    os.environ[_thread_var]="1"
import hashlib
import importlib.util
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
FREEZE=HERE/"FINITE_SLICE_GROWTH_TRANSFER_V001_FROZEN.json"
KERNEL_SHA="b59ab0f88e39234929eb6fa4d0a53bba0b1bf4dc4fbd9891b704b5cd89e19bf1"
RESULT_SHAS=["31cd0c151a6f6f906fa62ef84f3c3517b5ecbcd79f39beda29ecea2fddc9fdf2",
 "38e4ff97e7158e31b6ae1482f5f4ce7971d256d9b67f4c96beb7b4fc59eb3479",
 "8ac1241d4c378ab7ec6ced9447262cfb5df1772d23ab7a36349ed257437df772",
 "b6c5d0e95efae74f19a09c93c0b2637324fd7535b636cccb5df0a35203802503",
 "3bf9a0d352a64d0570177fdaf628d3c336ed6bb365415abffb69115ae6cd305f"]
CONFIG=dict(A_initial=101.,A_outputs=[101.,81.,61.,41.,21.,11.,6.,3.,2.,1.],
 k_Mpc_inverse=[.0001,.001,.01,.1],angle_orders=[8,16,64,512],
 angle_doubling=2,rtol_coarse=1e-8,atol_coarse=1e-10,
 rtol_tight=2e-9,atol_tight=2e-11,eta_rtol=2e-12,eta_atol=2e-13,
 initial_step=.001,maximum_step=.05,phase_cap_coarse=.6,phase_cap_tight=.3,
 safety=.85,step_factor_min=.2,step_factor_max=4.,
 arithmetic_tolerance=2e-11,transfer_tolerance=3e-6,
 constraint_tolerance=2e-7,phase_integral_tolerance=2e-8,
 angular_kernel_tolerance=1e-12,background_quadrature_tolerance=2e-11,
 expected_histories=335,expected_backgrounds=5,expected_points=67,
 c_km_s=299792.458,observational_success_gate=None,
 initial_columns=[[1.,0.],[0.,1.]],actual_initial_amplitude=None)
LABELS=["Phi","Psi","Weyl","slip","delta_H","delta_b","delta_r",
 "theta_H","theta_b","theta_r","Delta_H","Delta_b","Delta_r",
 "sigma_r","clock_Hcal_pi","preferred_clock_tilt","velocity_H_over_c",
 "velocity_b_over_c","velocity_r_over_c","Hamiltonian_residual",
 "Hamiltonian_normalized"]
SMALLNESS_INDICES=[0,1,2,3,4,5,6,10,11,12,13,15,16,17,18]


def encode(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def inputs():
    kp=HERE/"finite_pressure_bao_ruler_v001.py"
    if sha(kp)!=KERNEL_SHA:raise RuntimeError("Expansion kernel changed")
    spec=importlib.util.spec_from_file_location("owned_slice_background",kp)
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    inv,_,prior=base.read_inputs()  # authentication only, never ancestor run
    fp=HERE/"FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json"
    if json.loads(fp.read_text())!=prior:raise RuntimeError("Expansion freeze changed")
    files=dict(prior["files"]);files[str(fp.relative_to(ROOT))]=sha(fp)
    rows=[];backgrounds=[];mapping=None
    for i,digest in enumerate(RESULT_SHAS):
        rp=HERE/f"FINITE_PRESSURE_BAO_RULER_V001_BACKGROUND_{i}.json"
        if sha(rp)!=digest:raise RuntimeError("Background result changed")
        packet=json.loads(rp.read_text());p=packet["payload"]
        if packet["freeze_sha256"]!=sha(fp) or packet["payload_sha256"]!=hashlib.sha256(encode(p)).hexdigest():
            raise RuntimeError("Background wrapper changed")
        if p["status"]!="COMPLETE_BACKGROUND_SUBSET" or p["failures"] or p["selected_background_id"]!=i:
            raise RuntimeError("Incomplete background prerequisite")
        if len(p["records"])!=67:raise RuntimeError("Background census differs")
        backgrounds.append(next(b for b in p["backgrounds"] if b["background_id"]==i))
        for r in p["records"]:
            if r["background_id"]!=i:raise RuntimeError("Wrong background row")
            if r["status"]!="COMPLETE_CONDITIONAL_BACKGROUND":
                raise RuntimeError("Unsupported inherited background row")
            rows.append(r)
        mapping=p["reference_mapping"]
        files[str(rp.relative_to(ROOT))]=digest
    if len(rows)!=335 or len({(r["background_id"],r["point_id"]) for r in rows})!=335:
        raise RuntimeError("Unique history census differs")
    for name in ["FINITE_SLICE_GROWTH_TRANSFER_DERIVATION_V001.md",
                 "FINITE_SLICE_GROWTH_TRANSFER_PROTOCOL_V001.md",
                 "ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md",
                 "PHYSICAL_TIME_AND_RELEASE_STATE_MAP_V001.md",
                 "FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md",
                 Path(__file__).name]:
        p=(HERE/name).resolve(strict=True);p.relative_to(ROOT)
        files[str(p.relative_to(ROOT))]=sha(p)
    return base,rows,backgrounds,mapping,inv,dict(configuration=CONFIG,files=files)


class Checks:
    def __init__(self):self.counts={};self.maxima={};self.failures=[]
    def check(self,name,a,b=0.,scale=1.,tol=None,context=None):
        tol=CONFIG["arithmetic_tolerance"] if tol is None else tol
        error=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
        mx=float(np.max(error));self.counts[name]=self.counts.get(name,0)+int(error.size)
        self.maxima[name]=max(mx,self.maxima.get(name,0.))
        if not np.all(np.isfinite(error)) or mx>tol:
            self.failures.append(dict(check=name,error=mx,tolerance=tol,context=context))
    def yes(self,name,value,context=None):self.check(name,int(bool(value)),1.,context=context)


# Dormand-Prince 5(4), explicit and independent of ancestral integrators.
C=[0.,1/5,3/10,4/5,8/9,1.,1.]
AA=[[],[1/5],[3/40,9/40],[44/45,-56/15,32/9],
    [19372/6561,-25360/2187,64448/6561,-212/729],
    [9017/3168,-355/33,46732/5247,49/176,-5103/18656],
    [35/384,0.,500/1113,125/192,-2187/6784,11/84]]
B5=[35/384,0.,500/1113,125/192,-2187/6784,11/84,0.]
B4=[5179/57600,0.,7571/16695,393/640,-92097/339200,187/2100,1/40]


def step(fun,x,y,h):
    stages=[]
    for i in range(7):
        yy=y.copy()
        for j,a in enumerate(AA[i]):yy+=h*a*stages[j]
        stages.append(fun(x+C[i]*h,yy))
    high=y.copy();low=y.copy()
    for j in range(7):
        high+=h*B5[j]*stages[j];low+=h*B4[j]*stages[j]
    return high,high-low


def integrate(fun,y0,targets,cap,tight,observe=None):
    rtol=CONFIG["rtol_tight" if tight else "rtol_coarse"]
    atol=CONFIG["atol_tight" if tight else "atol_coarse"]
    x=0.;y=y0.copy();h=CONFIG["initial_step"];out=[y.copy()]
    accepted=rejected=0;maxerr=0.;minh=math.inf;maxh=0.
    for end in targets[1:]:
        end=float(end)
        while x<end:
            h=min(h,CONFIG["maximum_step"],cap(x),end-x)
            if x+h==x:raise RuntimeError("Floating-point step underflow")
            yy,err=step(fun,x,y,h)
            if not np.all(np.isfinite(yy)):raise RuntimeError("Nonfinite transfer state")
            sc=atol+rtol*np.maximum(np.abs(y),np.abs(yy))
            sc[0]=CONFIG["eta_atol"]+CONFIG["eta_rtol"]*max(abs(y[0]),abs(yy[0]))
            error=float(np.max(np.abs(err)/sc))
            factor=CONFIG["step_factor_max"] if error==0. else min(CONFIG["step_factor_max"],
                max(CONFIG["step_factor_min"],CONFIG["safety"]*error**(-.2)))
            if error<=1.:
                x=end if h==end-x else x+h;y=yy;accepted+=1
                minh=min(minh,h);maxh=max(maxh,h);maxerr=max(maxerr,error)
                if observe is not None:observe(x,y)
            else:rejected+=1
            h*=factor
        out.append(y.copy())
    return out,dict(accepted_steps=accepted,rejected_steps=rejected,
        maximum_accepted_embedded_error=maxerr,min_step=minh,max_step=maxh)


def angle_rule(n):
    mu,w=np.polynomial.legendre.leggauss(n)
    return (mu+1)/2,w/2


def kernel_log_bound(n,X,d):
    if X==0.:return -math.inf
    logc=4*math.lgamma(n+1)-3*math.lgamma(2*n+1)-math.log(2*n+1)
    terms=[]
    for j in range(d+1):
        choose=math.lgamma(2*n+1)-math.lgamma(j+1)-math.lgamma(2*n-j+1)
        derivative=math.lgamma(d+1)-math.lgamma(d-j+1)
        terms.append(choose+derivative+(2*n-j)*math.log(X))
    top=max(terms)
    return math.log(2)+logc+top+math.log(sum(math.exp(v-top) for v in terms))


class Model:
    def __init__(self,base,bg,row,kphysical,n,dust=False,EdS=False):
        self.base=base;self.bg=bg;self.row=row;self.n=n;self.kphysical=kphysical
        self.K=kphysical*CONFIG["c_km_s"]/bg["H0_km_s_Mpc"]
        self.mu,self.aw=angle_rule(n);self.P2=(3*self.mu**2-1)/2
        r1=0. if dust else row["r1"]
        self.kernel=base.Kernel(r1,128)
        self.background=base.Background(self.kernel,bg,row["Omega_b"],row["Omega_exc"],row["Omega_gamma"])
        if EdS:self.background.orad=0.
        self.ti=self.kernel.endpoint(CONFIG["A_initial"])
        self.targets=np.array([self.ti-self.kernel.endpoint(A) for A in CONFIG["A_outputs"]])
        self.ncol=6+2*n;self.EdS=EdS

    def background_at(self,x):
        t=self.ti-x;v=self.background.values(np.array([t]))
        A=float(v["A"][0]);H=float(v["Hbar"][0]);h=H/A
        lam=float(v["lam"][0]);w=float(v["w"][0]);c2=float(v["cI2"][0])
        eb=1.5*self.row["Omega_b"]*A
        eh=1.5*self.row["Omega_exc"]*float(v["ratio"][0])/A**2
        er=1.5*self.background.orad*A**2
        return dict(A=A,H=H,h=h,lam=lam,w=w,c2=c2,eb=eb,eh=eh,er=er,
                    factor=lam/(3*h),t=t)

    def initial(self):
        b=self.background_at(0.);a=b["eh"]*(1+b["w"])+b["eb"]+4*b["er"]/3
        y=np.zeros(1+2*self.ncol);q=y[1:].reshape(2,self.ncol)
        for j,(psi,slope) in enumerate(CONFIG["initial_columns"]):
            v=b["h"]*(psi+slope)/a;d=-self.K**2*psi/a-3*b["h"]*v
            q[j,:6]=[psi,(1+b["w"])*d,self.K**2*v,d,self.K**2*v,0.]
            q[j,6:6+self.n]=4*d/3+4*psi
            q[j,6+self.n:]=-4*self.K*v*self.mu
        return y

    def parts(self,x,y):
        b=self.background_at(x);q=y[1:].reshape(2,self.ncol)
        phase=self.K*self.mu*y[0];co=np.cos(phase);si=np.sin(phase)
        he=q[:,6:6+self.n];ho=q[:,6+self.n:]
        E=he*co+ho*si;O=ho*co-he*si
        sigma=-.5*(E@(self.aw*self.P2))
        theta=-.75*self.K*(O@(self.aw*self.mu))
        M3=O@(self.aw*self.P2*self.mu)
        psi=q[:,0];phi=psi-4*b["er"]*sigma/self.K**2
        dr=E@self.aw-4*phi
        U=(b["eh"]*(1+b["w"])*q[:,2]+b["eb"]*q[:,4]+4*b["er"]*theta/3)/self.K**2
        psip=U-b["h"]*phi
        phip=psip+8*b["h"]*b["er"]*sigma/self.K**2+2*b["er"]*M3/self.K
        return b,q,E,O,co,si,sigma,theta,M3,phi,dr,U,psip,phip

    def rhs(self,x,y):
        b,q,E,O,co,si,sig,tr,M3,phi,dr,U,psip,phip=self.parts(x,y)
        ans=np.empty_like(y);ans[0]=b["factor"];r=ans[1:].reshape(2,self.ncol)
        r[:,0]=b["factor"]*psip
        r[:,1]=b["factor"]*(-(1+b["w"])*(q[:,2]-3*psip)-3*b["h"]*(b["c2"]-b["w"])*q[:,1])
        r[:,2]=b["factor"]*(-b["h"]*(1-3*b["c2"])*q[:,2]+self.K**2*(phi+b["c2"]*q[:,1]/(1+b["w"])))
        r[:,3]=b["factor"]*(-q[:,4]+3*psip)
        r[:,4]=b["factor"]*(-b["h"]*q[:,4]+self.K**2*phi)
        r[:,5]=b["lam"]*phi/(3*b["H"])
        drive=4*b["factor"]*(psip+phip)
        r[:,6:6+self.n]=drive[:,None]*co
        r[:,6+self.n:]=drive[:,None]*si
        return ans

    def cap(self,x,tight):
        h=self.background_at(x)["h"]
        cap=CONFIG["phase_cap_tight" if tight else "phase_cap_coarse"]
        return 2*math.log1p(cap*h/self.K)

    def output(self,x,y):
        b,q,E,O,co,si,sig,tr,M3,phi,dr,U,psip,phip=self.parts(x,y)
        terms=np.array([self.K**2*q[:,0],3*b["h"]*U,b["eh"]*q[:,1],b["eb"]*q[:,3],b["er"]*dr])
        constraint=np.sum(terms,axis=0);norm=np.maximum(1.,np.sum(np.abs(terms),axis=0))
        dh=q[:,1]+3*b["h"]*(1+b["w"])*q[:,2]/self.K**2
        db=q[:,3]+3*b["h"]*q[:,4]/self.K**2
        drr=dr+4*b["h"]*tr/self.K**2
        values=np.column_stack([phi,q[:,0],(phi+q[:,0])/2,phi-q[:,0],q[:,1],q[:,3],dr,
             q[:,2],q[:,4],tr,dh,db,drr,sig,q[:,5],self.K*b["A"]*q[:,5],
             q[:,2]/self.K,q[:,4]/self.K,tr/self.K,constraint,constraint/norm])
        return values,b

    def identities(self,x,y,ck,context):
        b,q,E,O,co,si,sig,tr,M3,phi,dr,U,psip,phip=self.parts(x,y)
        Egp=self.K*self.mu*O+4*(psip+phip)[:,None]
        Ogp=-self.K*self.mu*E
        direct_dr=Egp@self.aw-4*phip
        expected_dr=-4*tr/3+4*psip
        ck.check("radiation_monopole_identity",direct_dr,expected_dr,np.maximum(1.,np.abs(direct_dr)+np.abs(expected_dr)),context=context)
        direct_tr=-.75*self.K*(Ogp@(self.aw*self.mu))
        expected_tr=self.K**2*(dr/4-sig+phi)
        ck.check("radiation_Euler_identity",direct_tr,expected_tr,np.maximum(1.,np.abs(direct_tr)+np.abs(expected_tr)),context=context)
        sigp=-.5*(Egp@(self.aw*self.P2))
        ck.check("radiation_shear_identity",sigp,-.5*self.K*M3,np.maximum(1.,np.abs(sigp)),context=context)
        direct_phip=psip+8*b["h"]*b["er"]*sig/self.K**2-4*b["er"]*sigp/self.K**2
        ck.check("slip_derivative_reconstruction",direct_phip,phip,np.maximum(1.,np.abs(direct_phip)),context=context)


def propagate(model,tight,ck,context):
    started=time.perf_counter();initial=model.initial()
    ck.check("angular_weight_sum",np.sum(model.aw),1.,context=context)
    ck.yes("angular_weights_positive",np.all(model.aw>0),context)
    for d in range(7):ck.check("angular_polynomial",model.aw@(model.mu**d),1/(d+1),context=context+[d])
    v0,b0=model.output(0.,initial)
    ck.check("initial_Hamiltonian",v0[:,-1],0.,context=context)
    _,q,_,_,_,_,sig,theta,_,phi,dr,U,psip,_=model.parts(0.,initial)
    ck.check("initial_Psi_and_tangent",np.column_stack([q[:,0],psip/b0["h"]]),CONFIG["initial_columns"],context=context)
    ck.check("initial_radiation_density",dr,4*q[:,3]/3,np.maximum(1.,np.abs(dr)),context=context)
    ck.check("initial_common_velocity",theta,q[:,4],np.maximum(1.,np.abs(theta)),context=context)
    ck.check("initial_radiation_shear",sig,0.,np.maximum(1.,np.abs(dr)),context=context)
    peak=np.max(np.abs(v0[:,SMALLNESS_INDICES]),axis=1);constraint_peak=np.max(np.abs(v0[:,-1]))
    def observe(x,y):
        nonlocal peak,constraint_peak
        val,_=model.output(x,y)
        peak=np.maximum(peak,np.max(np.abs(val[:,SMALLNESS_INDICES]),axis=1))
        constraint_peak=max(constraint_peak,float(np.max(np.abs(val[:,-1]))))
    states,stats=integrate(model.rhs,initial,model.targets,lambda x:model.cap(x,tight),tight,observe)
    samples=[];values=[]
    for i,(x,y) in enumerate(zip(model.targets,states)):
        val,b=model.output(float(x),y);values.append(val)
        model.identities(float(x),y,ck,context+[i])
        eta=model.background.integral(b["t"],model.ti,"comoving_integrand",64)
        eta32=model.background.integral(b["t"],model.ti,"comoving_integrand",32)
        # comoving_integrand is dA/H. The same difference equals conformal length.
        ck.check("conformal_background_quadrature",eta32,eta,max(1.,abs(eta)),tol=CONFIG["background_quadrature_tolerance"],context=context+[i])
        ck.check("conformal_phase_integral",model.K*y[0],model.K*eta,tol=CONFIG["phase_integral_tolerance"],context=context+[i])
        ck.check("requested_epoch",b["A"],CONFIG["A_outputs"][i],CONFIG["A_outputs"][i],context=context+[i])
        samples.append(dict(A=b["A"],x=float(x),eta_bar=float(y[0]),eta_bar_quadrature=eta,
             w=b["w"],cI2=b["c2"],H_over_Hcal=b["H"],values=val.tolist()))
    ck.check("propagated_Hamiltonian",constraint_peak,0.,tol=CONFIG["constraint_tolerance"],context=context)
    if model.kernel.r1==0.:
        va=np.array(values)
        ck.check("dust_species_density_identity",va[:,:,4],va[:,:,5],np.maximum(1.,np.abs(va[:,:,5])),context=context)
        ck.check("dust_species_velocity_identity",va[:,:,7],va[:,:,8],np.maximum(1.,np.abs(va[:,:,8])),context=context)
    return dict(angle_order=model.n,tight=tight,initial_state=initial.tolist(),samples=samples,
        statistics=stats,accepted_step_sampled_max_per_column=peak.tolist(),
        sampled_smallness_observables=[LABELS[i] for i in SMALLNESS_INDICES],
        illustrative_amplitude_for_sampled_1percent=(.01/np.maximum(peak,1.)).tolist(),
        accepted_step_Hamiltonian_max=float(constraint_peak),seconds=time.perf_counter()-started)


def qualify_integrator(ck):
    for i in range(7):ck.check("tableau_row_sum",sum(AA[i]),C[i],context=i)
    ck.check("tableau_weights",[sum(B5),sum(B4)],[1.,1.])
    for h in [.1,.05]:
        y=np.array([0.,1.,0.]);x=0.
        def f(t,z):return np.array([1.,-2*z[2],2*z[1]])
        for _ in range(round(1/h)):y,_=step(f,x,y,h);x+=h
        ck.check("synthetic_exponential",y,[1.,math.cos(2),math.sin(2)],tol=2e-6,context=h)


def qualify_EdS(base,ck):
    bg=dict(H0_km_s_Mpc=CONFIG["c_km_s"],Omega_m=1.,Omega_Lambda=0.)
    row=dict(r1=0.,Omega_b=.2,Omega_exc=.8,Omega_gamma=1.)
    model=Model(base,bg,row,5.,16,EdS=True)
    out=propagate(model,True,ck,["EdS"]);ai=1/CONFIG["A_initial"]
    for i,s in enumerate(out["samples"]):
        a=1/s["A"];h=1/math.sqrt(a);actual=np.array(s["values"])
        expected=[]
        for psi0,q0 in CONFIG["initial_columns"]:
            qi=q0*(ai/a)**2.5;psi=psi0+2*q0/5*(1-(ai/a)**2.5)
            th=2*model.K**2*(psi+qi)/(3*h)
            de=-2*model.K**2*psi/(3*h*h)-2*(psi+qi)
            clock=2*(psi0+2*q0/5)*(a**1.5-ai**1.5)/3+2*q0*ai**2.5*(1/a-1/ai)/5
            expected.append([psi,de,th,clock])
        got=actual[:,[1,4,7,14]];expected=np.array(expected)
        ck.check("exact_EdS_metric_density_clock",got,expected,np.maximum(1.,np.abs(expected)),
                 tol=CONFIG["transfer_tolerance"],context=i)
    return out


def compare_runs(a,b,ck,name,context):
    aa=np.array([s["values"] for s in a["samples"]]);bb=np.array([s["values"] for s in b["samples"]])
    # Hamiltonian raw units depend on k and are separately normalized/qualified.
    aa=aa[:,:,:19];bb=bb[:,:,:19]
    scale=np.maximum(1.,np.max(np.abs(bb),axis=0))
    error=np.max(np.abs(aa-bb)/scale[None,:,:],axis=0)
    ck.check(name,error,0.,tol=CONFIG["transfer_tolerance"],context=context)
    return dict(observables=LABELS[:19],normalized_max_by_basis_and_observable=error.tolist())


def run_case(base,rows,backgrounds,mapping,inv,index,benchmark):
    started=time.perf_counter();ck=Checks();qualify_integrator(ck)
    EdS=qualify_EdS(base,ck);row=rows[index];bi=row["background_id"]
    bg=next(b for b in backgrounds if b["background_id"]==bi)
    ck.yes("supported_inherited_fields",all(k in row for k in ["r1","Omega_b","Omega_exc","Omega_gamma"]))
    results=[]
    for ik,(k,n) in enumerate(zip(CONFIG["k_Mpc_inverse"],CONFIG["angle_orders"])):
        K=k*CONFIG["c_km_s"]/bg["H0_km_s_Mpc"]
        X=K*2*(1-CONFIG["A_initial"]**(-.5))/math.sqrt(bg["Omega_m"])
        bounds=[]
        for nn in [n,2*n]:
            logs=[kernel_log_bound(nn,X,d) for d in range(5)]
            combined=2*sum(math.exp(v) for v in logs)
            ck.check("angular_memory_kernel_bound",combined,0.,tol=CONFIG["angular_kernel_tolerance"],context=[ik,nn])
            bounds.append(dict(order=nn,monomial_log_bounds=logs,combined_bound=combined))
        branches={}
        for label,dust in [("candidate",False),("dust_comparator",True)]:
            runs=[]
            for tag,nn,tight in [("coarse",n,False),("tight",n,True),("primary",2*n,True)]:
                m=Model(base,bg,row,k,nn,dust=dust)
                out=propagate(m,tight,ck,[index,ik,label,tag]);out["tag"]=tag;runs.append(out)
            comparisons=[compare_runs(runs[0],runs[1],ck,"time_refinement",[index,ik,label]),
                         compare_runs(runs[1],runs[2],ck,"angle_refinement",[index,ik,label])]
            branches[label]=dict(runs=runs,comparisons=comparisons)
        if not row["finite_gap"]:
            compare_runs(branches["candidate"]["runs"][2],branches["dust_comparator"]["runs"][2],
                         ck,"inherited_dust_limit_identity",[index,ik])
        primary=np.array([v["values"] for v in branches["candidate"]["runs"][2]["samples"]])
        dust=np.array([v["values"] for v in branches["dust_comparator"]["runs"][2]["samples"]])
        results.append(dict(k_Mpc_inverse=k,K_dimensionless=K,maximum_phase_bound=X,
            angular_kernel_certificates=bounds,branches=branches,
            primary_minus_dust_signed=(primary-dust).tolist()))
    return dict(status="FAILED_NUMERICAL_CONTROLS" if ck.failures else
            "COMPLETE_BENCHMARK_ONLY" if benchmark else "COMPLETE_SINGLE_HISTORY",
        configuration=CONFIG,case_index=index,benchmark_only=benchmark,
        expected_full_history_count=len(rows),background=bg,source_record=row,
        reference_mapping=mapping,mechanical_label_mapping=[{k:r[k] for k in
          ["point_id","background_id","spectrum_index","status"]} for r in inv["state_rows"]
          if r["point_id"]==row["point_id"] and r["background_id"]==bi],
        history_census=[dict(case_index=i,background_id=r["background_id"],point_id=r["point_id"],
                            finite_gap=r["finite_gap"]) for i,r in enumerate(rows)],
        observable_labels=LABELS,basis_columns=CONFIG["initial_columns"],results=results,
        EdS_control=EdS,counts=ck.counts,maxima=ck.maxima,failures=ck.failures,
        scope="Finite Ai101 instantaneous-adiabatic two-column Q0 transfer; pressureless baryons/collisionless ordinary radiation; no primordial/CMB/observed-growth inference.",
        seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=="darwin" else 1024))


def main():
    base,rows,bgs,mapping,inv,snapshot=inputs();args=sys.argv[1:]
    if args==["freeze"]:print(encode(snapshot).decode());return 0
    benchmark=args==["benchmark"]
    if benchmark:index=next(i for i,r in enumerate(rows) if r["finite_gap"])
    elif len(args)==2 and args[0]=="run-case" and args[1].isdigit() and 0<=int(args[1])<335:index=int(args[1])
    else:raise RuntimeError("Use freeze, benchmark, or run-case 0..334")
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError("Prospective freeze differs")
    payload=run_case(base,rows,bgs,mapping,inv,index,benchmark)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())
    return 2 if payload["failures"] else 0


if __name__=="__main__":sys.exit(main())
