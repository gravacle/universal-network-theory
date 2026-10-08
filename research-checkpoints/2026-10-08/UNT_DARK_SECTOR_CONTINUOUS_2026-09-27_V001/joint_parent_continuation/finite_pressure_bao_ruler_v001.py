"""Same-state background / exposed BAO ruler diagnostic. Stdout only.

No imports of ancestral producers, no ODE, recombination or CMB calculation.
The acoustic early tail remains an interval, not an invented thermal history.
"""
import os
for _thread_variable in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                         "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    os.environ[_thread_variable] = "1"
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time
import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE / "FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json"
CONFIG = dict(expected_points=67, expected_backgrounds=5, expected_spectra=4,
    expected_state_labels=1340, expected_histories=335, expected_BAO_rows=13,
    ordinary_massless_Neff=3.044, temperature_K=2.72548, A_cut=1e7,
    endpoint_A=[1.,11.,101.,501.,1101.,3001.,10001.],
    transition_w=[.01,.1,.3], angle_orders=[64,128], integral_orders=[32,64],
    maximum_t_panel=2., endpoint_bisections=64, Simpson_BAO=512,
    Simpson_acoustic=4096, arithmetic_tolerance=2e-11,
    covariance_tolerance=2e-12, material_tolerance=2e-10,
    distance_tolerance=2e-10, score_tolerance=2e-7,
    acoustic_quadrature_tolerance=2e-8, acoustic_Simpson_tolerance=2e-7,
    required_endpoint_tolerance=2e-9, c_km_s=299792.458,
    actual_recombination_status="NOT_COMPUTED", observational_success_gate=None)
INPUTS = {
    "BBN_SHARED_INVERSE_V001_RESULTS.json": "e05fd83e221897bafb4f8dbe46cc737dc8fef4f5ed11fdf122a7053bac3a02e0",
    "BBN_SHARED_INVERSE_V001_FROZEN.json": "0bf25c368e90dddfc46bb418273851b66a426dc7e3ab0edc6d436fa3237ae9f3",
    "DESI_BAO_SHAPE_V001_RESULTS.json": "1b7f1b02b2988e0109c1afd01f4ca621e36f1cd5729261ebff676853596f3fe7"}


def encode(x):
    return json.dumps(x, sort_keys=True, separators=(",",":"), allow_nan=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_inputs():
    files={}
    for name,digest in INPUTS.items():
        p=HERE/name
        if sha(p)!=digest: raise RuntimeError("Changed input: "+name)
    payloads=[]
    for name in ["BBN_SHARED_INVERSE", "DESI_BAO_SHAPE"]:
        fp=HERE/(name+"_V001_FROZEN.json")
        rp=HERE/(name+"_V001_RESULTS.json")
        frozen=json.loads(fp.read_text()); wrapper=json.loads(rp.read_text())
        if wrapper["freeze_sha256"]!=sha(fp): raise RuntimeError("Freeze link: "+name)
        if wrapper["payload_sha256"]!=hashlib.sha256(encode(wrapper["payload"])).hexdigest():
            raise RuntimeError("Payload identity: "+name)
        for rel,digest in frozen["files"].items():
            p=(ROOT/rel).resolve(strict=True);p.relative_to(ROOT)
            if sha(p)!=digest: raise RuntimeError("Changed ancestor: "+rel)
            if rel in files and files[rel]!=digest: raise RuntimeError("Ancestor collision")
            files[rel]=digest
        for p in [fp,rp]: files[str(p.relative_to(ROOT))]=sha(p)
        payloads.append(wrapper["payload"])
    inv,old=payloads
    if inv["status"]!="COMPLETE_CONDITIONAL_PROXY_INVERSE" or inv["failures"]:
        raise RuntimeError("Inverse prerequisite failed")
    if old["status"]!="COMPLETE": raise RuntimeError("Old BAO prerequisite failed")
    for p in [Path(__file__), HERE/"FINITE_PRESSURE_BAO_RULER_PROTOCOL_V001.md",
              HERE/"FINITE_PRESSURE_BAO_AND_RULER_DESIGN_V001.md",
              HERE/"ALPHA_ONE_FLRW_ENTROPY_INTERFACE_V001.md",
              HERE/"FINITE_GAP_CMB_PERTURBATION_DISCRIMINATOR_V001.md",
              HERE/"HARD_MODE_COLD_HISTORY_CONSTRAINT_V001.md",
              HERE/"SAME_ACTION_RADIATION_ASYMPTOTE_V001.md"]:
        p=p.resolve(strict=True);p.relative_to(ROOT);files[str(p.relative_to(ROOT))]=sha(p)
    return inv,old,dict(configuration=CONFIG, files=files)


class Checks:
    def __init__(self): self.counts={};self.maxima={};self.failures=[]
    def check(self,name,a,b=0.,scale=1.,tol=None,context=None):
        tol=CONFIG["arithmetic_tolerance"] if tol is None else tol
        er=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
        maximum=float(np.max(er))
        self.counts[name]=self.counts.get(name,0)+int(er.size)
        self.maxima[name]=max(self.maxima.get(name,0.),maximum)
        if not np.all(np.isfinite(er)) or maximum>tol:
            self.failures.append(dict(check=name,error=maximum,tolerance=tol,context=context))
    def yes(self,name,value,context=None): self.check(name,int(bool(value)),1.,context=context)


def gauss(n,a,b):
    x,w=np.polynomial.legendre.leggauss(n)
    return a+(b-a)*(x+1)/2,w*(b-a)/2


class Kernel:
    """Universal zero-source oscillator, one state at a time; no interpolation."""
    def __init__(self,r1,order):
        theta,self.aw=gauss(order,0.,math.pi/2)
        self.v=np.sin(theta)**2;self.c=np.cos(theta)**2
        self.r1=r1
        self.bar1=1. if r1==0. else float(self.moments(np.array([r1]))["bar"][0])
        self.ends={1.:0.}

    def moments(self,r):
        r=np.asarray(r);q=1.+r[...,None]*(1+self.v)/2
        sq=np.sqrt(q);J=np.sum(self.aw/sq,axis=-1)
        bar=(2/math.pi)*np.sum(self.aw*self.c*sq,axis=-1)
        omega=math.pi/(2*J)
        ell=np.sum(self.aw*(1+self.v)/(q*sq),axis=-1)
        w=r/(2+r)*np.sum(self.aw*self.v**2/sq,axis=-1)/J
        cI2=r*bar*omega*ell/(2*J*(1+r))
        lam=(1+r)/(2*omega*bar)
        return dict(bar=bar,omega=omega,w=w,cI2=cI2,lam=lam)

    def fields(self,t):
        t=np.asarray(t)
        if self.r1==0.:
            A=np.exp(t/3)
            return dict(A=A,ratio=A**3,w=np.zeros_like(A),cI2=np.zeros_like(A),
                        lam=np.ones_like(A),r=np.zeros_like(A))
        r=self.r1*np.exp(t);out=self.moments(r)
        A=np.exp((t+np.log(out["bar"]/self.bar1))/3)
        out.update(A=A,ratio=np.exp(t)*(2+r)/(2+self.r1),r=r)
        return out

    def endpoint(self,A):
        A=float(A)
        if A in self.ends:return self.ends[A]
        if A<1:raise ValueError("Endpoint below present")
        if self.r1==0.:t=3*math.log(A)
        else:
            lo=2*math.log(A);hi=3*math.log(A)
            for _ in range(CONFIG["endpoint_bisections"]):
                mid=(lo+hi)/2
                if float(self.fields(np.array([mid]))["A"][0])<A:lo=mid
                else:hi=mid
            t=(lo+hi)/2
        self.ends[A]=t
        return t


class Background:
    def __init__(self,kernel,bg,ob,oe,og):
        self.k=kernel;self.bg=bg;self.ob=ob;self.oe=oe;self.og=og
        self.orad=og*(1+(7/8)*(4/11)**(4/3)*CONFIG["ordinary_massless_Neff"])

    def values(self,t):
        o=self.k.fields(t);A=o["A"]
        H=np.sqrt(self.ob*A**3+self.oe*o["ratio"]+self.bg["Omega_Lambda"]+self.orad*A**4)
        common=A*o["lam"]/(3*H)
        o.update(Hbar=H,comoving_integrand=common,
                 photon_integrand=common/np.sqrt(3*(1+3*self.ob/(4*self.og*A))),
                 hard_integrand=common*np.sqrt(o["cI2"]))
        return o

    def integral(self,a,b,key,n):
        if a==b:return 0.
        nodes,weights=gauss(n,a,b)
        return float(np.dot(weights,self.values(nodes)[key]))

    def simpson(self,a,b,key,n):
        nodes=np.linspace(a,b,n+1);values=self.values(nodes)[key]
        return float((b-a)/(3*n)*(values[0]+values[-1]+4*np.sum(values[1:-1:2])+2*np.sum(values[2:-1:2])))

    def shape(self,data,n):
        ans=[];cache={}
        for z,label in data:
            if z not in cache:
                t=self.k.endpoint(1+z)
                dm=self.integral(0.,t,"comoving_integrand",n)
                dh=1/float(self.values(np.array([t]))["Hbar"][0])
                cache[z]=(dm,dh,(z*dm*dm*dh)**(1/3))
            ans.append(cache[z][{"DM_over_rs":0,"DH_over_rs":1,"DV_over_rs":2}[label]])
        return np.array(ans)


def profile(shape,y,cov,chol,ck,context):
    d=np.linalg.solve(chol,shape);yy=np.linalg.solve(chol,y)
    curvature=float(np.dot(d,d));free=float(np.dot(d,yy)/curvature)
    amplitude=max(0.,free);residual=amplitude*shape-y
    wr=np.linalg.solve(chol,residual);chi=float(np.dot(wr,wr))
    direct=float(np.dot(shape,np.linalg.solve(cov,y))/np.dot(shape,np.linalg.solve(cov,shape)))
    ck.check("profile_direct_amplitude",free,direct,max(1.,abs(free)),context=context)
    ck.check("profile_direct_score",chi,float(residual@np.linalg.solve(cov,residual)),
             tol=CONFIG["score_tolerance"],context=context)
    return dict(amplitude=amplitude,unconstrained_amplitude=free,
        boundary_active=free<0.,score=chi,curvature_half=curvature,
        derivative=2*float(d@(amplitude*d-yy)),prediction=(amplitude*shape).tolist(),
        residual=residual.tolist(),whitened_residual=wr.tolist(),
        covariance_residual_contributions=(residual*np.linalg.solve(cov,residual)).tolist())


class Acoustic:
    def __init__(self,bg,n):
        self.bg=bg;self.n=n
        end=bg.k.endpoint(CONFIG["A_cut"])
        self.edges=np.linspace(0.,end,math.ceil(end/CONFIG["maximum_t_panel"])+1)
        self.segments={key:np.array([bg.integral(a,b,key,n) for a,b in zip(self.edges[:-1],self.edges[1:])])
                       for key in ["photon_integrand","hard_integrand"]}
        self.tails={key:np.r_[np.cumsum(v[::-1])[::-1],0.] for key,v in self.segments.items()}

    def at_t(self,t,key):
        if t>=self.edges[-1]:return 0.
        i=min(len(self.edges)-2,int(np.searchsorted(self.edges,t,side="right")-1))
        return self.bg.integral(t,self.edges[i+1],key,self.n)+float(self.tails[key][i+1])

    def inverse(self,value):
        key="photon_integrand"
        if value<0.:return None,"ABOVE_INTEGRATION_CUTOFF"
        if value>self.tails[key][0]:return None,"BELOW_PRESENT_ENDPOINT"
        if value==0.:return CONFIG["A_cut"],"AT_CUTOFF"
        indices=np.flatnonzero((self.tails[key][:-1]>=value)&(self.tails[key][1:]<=value))
        if not len(indices):raise RuntimeError("Missing acoustic inverse bracket")
        i=int(indices[0]);lo=float(self.edges[i]);hi=float(self.edges[i+1])
        for _ in range(CONFIG["endpoint_bisections"]):
            mid=(lo+hi)/2
            if self.at_t(mid,key)>value:lo=mid
            else:hi=mid
        A=float(self.bg.k.fields(np.array([(lo+hi)/2]))["A"][0])
        return A,"WITHIN_INTEGRATED_DOMAIN"


def tail_bound(bg,Delta):
    Ac=CONFIG["A_cut"];q=Delta*(7/8)*(4/11)**(4/3)*bg.og
    scalar_baryon=2/(math.sqrt(3)*Ac*(math.sqrt(q+bg.ob/Ac)+math.sqrt(q)))
    total_dust=2/math.sqrt(3*bg.bg["Omega_m"]*Ac)
    return min(scalar_baryon,total_dust)


def transitions(k):
    out=[]
    for target in CONFIG["transition_w"]:
        if k.r1==0.:
            out.append(dict(w=target,A=None,status="DUST_LIMIT_NO_TRANSITION"));continue
        lo=-40.;hi=40.
        for _ in range(CONFIG["endpoint_bisections"]):
            mid=(lo+hi)/2
            if float(k.moments(np.array([math.exp(mid)]))["w"][0])<target:lo=mid
            else:hi=mid
        r=math.exp((lo+hi)/2);bar=float(k.moments(np.array([r]))["bar"][0])
        A=(r*bar/(k.r1*k.bar1))**(1/3)
        out.append(dict(w=target,A=A,status="BEFORE_PRESENT" if A<1 else
                        "ABOVE_THERMAL_CUTOFF" if A>CONFIG["A_cut"] else "IN_DOMAIN"))
    return out


def qualify_kernels(ck):
    C4=((3*math.sqrt(math.pi)/2)*math.gamma(.75)/math.gamma(.25))**(4/3)
    for r in [1e-12,.01,1.,1e4]:
        k=Kernel(r,128);o=k.moments(np.array([r]));f=r*o["bar"][0];e=r/2+r*r/4
        ck.check("action_virial_synthetic",f*o["omega"][0],e*(1+o["w"][0]),e)
        ck.yes("finite_gap_synthetic_bound",C4*f**(4/3)<=e*(1+2e-11) and
               e<=C4*f**(4/3)+math.sqrt(C4*f**(4/3))+2e-11*e)
        th=np.linspace(0.,math.pi/2,1025);q=1+r*(1+np.sin(th)**2)/2
        vals=np.cos(th)**2*np.sqrt(q)
        fs=(2/math.pi)*r*(math.pi/2/1024/3)*(vals[0]+vals[-1]+4*sum(vals[1:-1:2])+2*sum(vals[2:-1:2]))
        ck.check("independent_action_Simpson",f,fs,f,tol=CONFIG["material_tolerance"])
        for A in [1.,3.,1101.,CONFIG["A_cut"]]:
            t=k.endpoint(A);v=k.fields(np.array([t]));ratio=v["ratio"][0]
            ck.check("endpoint_action_identity",v["A"][0],A,A)
            ck.check("action_ratio_identity",v["r"][0]*v["bar"][0]/f,A**3,A**3)
            ck.yes("energy_envelope",A**3*(1-2e-11)<=ratio<=A**4*(1+2e-11))
            ck.yes("material_positive_bounded",0<=v["w"][0]<=1/3+2e-11 and
                   0<=v["cI2"][0]<=1/3+2e-11 and 1-2e-11<=v["lam"][0]<=1.5+2e-11)


def run(inv,old,benchmark=False,background_id=None):
    started=time.perf_counter();ck=Checks();qualify_kernels(ck)
    directory=HERE/"desi_dr2_bao_external_v001"
    raw=[line.split() for line in (directory/"desi_gaussian_bao_ALL_GCcomb_mean.txt").read_text().splitlines()
         if line.strip() and not line.lstrip().startswith("#")]
    data=[(float(x[0]),x[2]) for x in raw];y=np.array([float(x[1]) for x in raw])
    cov=np.loadtxt(directory/"desi_gaussian_bao_ALL_GCcomb_cov.txt")
    expected=[(.295,"DV_over_rs"),(.51,"DM_over_rs"),(.51,"DH_over_rs"),(.706,"DM_over_rs"),
        (.706,"DH_over_rs"),(.934,"DM_over_rs"),(.934,"DH_over_rs"),(1.321,"DM_over_rs"),
        (1.321,"DH_over_rs"),(1.484,"DM_over_rs"),(1.484,"DH_over_rs"),(2.33,"DH_over_rs"),(2.33,"DM_over_rs")]
    ck.yes("complete_BAO_order",data==expected and cov.shape==(13,13))
    ck.check("covariance_symmetry",cov,cov.T,tol=CONFIG["covariance_tolerance"])
    chol=np.linalg.cholesky(cov)
    ck.check("Cholesky_reconstruction",chol@chol.T,cov,tol=CONFIG["covariance_tolerance"])
    synthetic=np.arange(1.,14.)
    syn=profile(synthetic,42*synthetic,cov,chol,ck,"synthetic")
    ck.check("synthetic_profile_recovery",syn["amplitude"],42.,42.)
    ck.check("synthetic_profile_zero",syn["score"],0.,tol=1e-18)
    neg=profile(synthetic,-synthetic,cov,chol,ck,"negative")
    ck.yes("profile_boundary",neg["amplitude"]==0. and neg["derivative"]>=0.)
    points=inv["table_points"];backgrounds=inv["backgrounds"]
    ck.yes("input_census",len(points)==67 and len(backgrounds)==5 and len(inv["state_rows"])==1340)
    states={(r["point_id"],r["background_id"],r["spectrum_index"]):r for r in inv["state_rows"]}
    constants={(r["background_id"],r["spectrum_index"]):r for r in inv["constants"]}
    selected=None
    if benchmark:
        selected=next((r["background_id"],r["point_id"]) for r in inv["state_rows"]
                      if r["status"]=="FINITE_HARD_STATE")
    records=[];dust_controls=[]
    for bg in backgrounds:
        bi=bg["background_id"];og=constants[(bi,0)]["Omega_gamma"]
        if benchmark and bi!=selected[0]:continue
        if background_id is not None and bi!=background_id:continue
        dust=Background(Kernel(0.,128),bg,0.,bg["Omega_m"],og)
        dshape=dust.shape(data,64);dfit=profile(dshape,y,cov,chol,ck,[bi,"dust"])
        # Historical comparison deliberately removes radiation without changing
        # the matched vacuum. Only the already qualified old receipt is read.
        dust.orad=0.;hist=dust.shape(data,64)
        previous=old["references"][bg["representative_reference"]]
        ck.check("historical_dust_shape",hist,previous["shape"],np.maximum(np.abs(hist),1e-300),
                 tol=CONFIG["distance_tolerance"],context=bi)
        dust_controls.append(dict(background_id=bi,shape=dshape.tolist(),fit=dfit,
                                  historical_zero_radiation_shape=hist.tolist()))
        for point in points:
            pi=point["point_id"];ctx=[bi,pi];copies=[states[(pi,bi,si)] for si in range(4)]
            if benchmark and (bi,pi)!=selected:continue
            row_started=time.perf_counter()
            finite=[r for r in copies if r["status"]=="FINITE_HARD_STATE"]
            infinity=all(r["status"]=="INFINITE_GAP_STANDARD_LIMIT" for r in copies)
            rec=dict(background_id=bi,point_id=pi,omega_b=point["omega_b"],Delta=point["Delta"],
                point_roles=point["roles"],coarse_Delta_node=point["coarse_node"],
                inherited_local_BBN_rectangle=point["prediction"]["local_numerical_rectangle"],
                spectrum_statuses=[r["status"] for r in copies])
            if not infinity and len(finite)!=4:
                rec["status"]="UNSUPPORTED_INHERITED_STATE";records.append(rec);continue
            source=copies[0];ob=source["Omega_b"];oe=source["Omega_exc"]
            r1=0. if infinity else 2*source["s"]**2/(1-source["s"]**2)
            for si,row in enumerate(copies):
                ck.check("copy_background_coefficients",[row["Omega_b"],row["Omega_exc"]],[ob,oe],context=ctx+[si])
                ck.check("copy_photons",constants[(bi,si)]["Omega_gamma"],og,og,context=ctx+[si])
                if not infinity:
                    rr=2*row["s"]**2/(1-row["s"]**2)
                    ck.check("same_shape_four_copies",rr,r1,r1,context=ctx+[si])
                    normalized=(point["Delta"]*inv["fnu"]*og/(inv["C4"]*oe))**.75
                    ck.check("scale_cancellation",row["I"]/row["hard_energy"]**.75,normalized,normalized,context=ctx+[si])
            primary=Background(Kernel(r1,128),bg,ob,oe,og)
            coarse=Background(Kernel(r1,64),bg,ob,oe,og)
            if not infinity:
                anchor=primary.k.moments(np.array([r1]))
                owned={"w":source["w"],"cI2":source["cI2"],
                       "omega":source["omega"]/source["R"],
                       "action":source["I"]/source["R"]**3}
                calculated={k:float(anchor[k][0]) for k in ["w","cI2","omega"]}
                calculated["action"]=r1*float(anchor["bar"][0])
                for key in owned:
                    ck.check("saved_present_anchor_"+key,calculated[key],owned[key],owned[key],
                             tol=CONFIG["material_tolerance"],context=ctx)
            shape=primary.shape(data,64);shape32=primary.shape(data,32);shape64angle=coarse.shape(data,64)
            for label,ss in [("integral",shape32),("angle",shape64angle)]:
                ck.check("BAO_"+label,ss,shape,np.abs(shape),tol=CONFIG["distance_tolerance"],context=ctx)
            fit=profile(shape,y,cov,chol,ck,ctx)
            checkfit=profile(shape32,y,cov,chol,ck,ctx+["coarse"])
            ck.check("BAO_score_refinement",fit["score"],checkfit["score"],tol=CONFIG["score_tolerance"],context=ctx)
            ts=primary.k.endpoint(3.33)
            ss=primary.simpson(0.,ts,"comoving_integrand",CONFIG["Simpson_BAO"])
            dm=primary.integral(0.,ts,"comoving_integrand",64)
            bao_simpson_difference=ss-dm
            ck.check("BAO_independent_Simpson",ss,dm,dm,tol=CONFIG["distance_tolerance"],context=ctx)
            ac=Acoustic(primary,64);ac32=Acoustic(primary,32);acangle=Acoustic(coarse,64)
            for key in ["photon_integrand","hard_integrand"]:
                scale=max(float(ac.tails[key][0]),1e-300)
                for label,other in [("integral",ac32),("angle",acangle)]:
                    ck.check("acoustic_"+label+"_"+key,other.tails[key][0],ac.tails[key][0],scale,
                             tol=CONFIG["acoustic_quadrature_tolerance"],context=ctx)
                ss=primary.simpson(0.,ac.edges[-1],key,CONFIG["Simpson_acoustic"])
                ck.check("acoustic_independent_Simpson_"+key,ss,ac.tails[key][0],scale,
                         tol=CONFIG["acoustic_Simpson_tolerance"],context=ctx)
            tail=tail_bound(primary,point["Delta"]);unit=CONFIG["c_km_s"]/bg["H0_km_s_Mpc"]
            epochs=[]
            for A in CONFIG["endpoint_A"]:
                t=primary.k.endpoint(A);v=primary.values(np.array([t]));s=coarse.values(np.array([coarse.k.endpoint(A)]))
                ck.check("epoch_energy_angle",v["ratio"],s["ratio"],v["ratio"],tol=CONFIG["material_tolerance"],context=ctx+[A])
                for key in ["w","cI2"]:
                    ck.check("epoch_material_angle_"+key,v[key],s[key],np.maximum(np.abs(v[key]),1e-300),
                             tol=CONFIG["material_tolerance"],context=ctx+[A])
                ck.check("epoch_action_endpoint",v["A"],A,A,context=ctx+[A])
                ck.yes("epoch_energy_envelope",A**3*(1-2e-11)<=v["ratio"][0]<=A**4*(1+2e-11),ctx+[A])
                ph=ac.at_t(t,"photon_integrand");hard=ac.at_t(t,"hard_integrand")
                for key,val in [("photon_integrand",ph),("hard_integrand",hard)]:
                    ck.check("endpoint_acoustic_refinement_"+key,ac32.at_t(t,key),val,max(abs(val),1e-300),
                             tol=CONFIG["acoustic_quadrature_tolerance"],context=ctx+[A])
                epochs.append(dict(A=A,H_over_Hcal=float(v["Hbar"][0]),energy_over_present=float(v["ratio"][0]),
                    energy_over_dust=float(v["ratio"][0]/A**3),w=float(v["w"][0]),cI2=float(v["cI2"][0]),
                    photon_horizon_Mpc_interval=[unit*ph,unit*(ph+tail)],
                    hard_horizon_Mpc_interval=[unit*hard,unit*(hard+(0. if infinity else tail))]))
            required=dict(status="NONPOSITIVE_PROFILE_SCALE",ruler_Mpc=None,A_interval=[None,None])
            if fit["amplitude"]>0:
                target=1/fit["amplitude"];lower,ls=ac.inverse(target);upper,us=ac.inverse(target-tail)
                required=dict(status="REQUIRED_ENDPOINT_NOT_RECOMBINATION",ruler_Mpc=unit*target,
                    A_interval=[lower,upper],bound_statuses=[ls,us],
                    unknown_early_tail_Mpc_interval=[0.,unit*tail])
                for A,tt in [(lower,target),(upper,target-tail)]:
                    if A is not None:
                        rr=ac.at_t(primary.k.endpoint(A),"photon_integrand")
                        ck.check("required_endpoint_inversion",rr,tt,max(abs(tt),1e-300),
                                 tol=CONFIG["required_endpoint_tolerance"],context=ctx)
            markers=transitions(primary.k)
            for marker in markers:
                A=marker["A"]
                if A is not None and 1<=A<=CONFIG["A_cut"]:
                    actual=primary.k.fields(np.array([primary.k.endpoint(A)]))["w"][0]
                    ck.check("transition_inversion",actual,marker["w"],marker["w"],context=ctx)
            rec.update(status="COMPLETE_CONDITIONAL_BACKGROUND",finite_gap=not infinity,r1=r1,
                Omega_b=ob,Omega_exc=oe,Omega_gamma=og,Omega_ordinary_radiation=primary.orad,
                H_present_over_Hcal=math.sqrt(1+primary.orad),shape=shape.tolist(),fit=fit,
                score_minus_same_background_dust=fit["score"]-dfit["score"],
                fractional_shape_minus_dust=(shape/dshape-1).tolist(),required_drag=required,
                epochs=epochs,transition_markers=markers,seconds=time.perf_counter()-row_started,
                precision=dict(shape_GL32_minus_primary=(shape32-shape).tolist(),
                    shape_angle64_minus_primary=(shape64angle-shape).tolist(),
                    BAO_Simpson_minus_GL=bao_simpson_difference,
                    acoustic_GL32_minus_primary={k:float(ac32.tails[k][0]-ac.tails[k][0]) for k in ac.tails},
                    acoustic_angle64_minus_primary={k:float(acangle.tails[k][0]-ac.tails[k][0]) for k in ac.tails}))
            records.append(rec)
    expected=1 if benchmark else 67 if background_id is not None else 335
    ck.yes("complete_output_census",len(records)==expected)
    completion=("COMPLETE_BENCHMARK_ONLY" if benchmark else "COMPLETE_BACKGROUND_SUBSET" if background_id is not None
                else "COMPLETE_PROFILED_BAO_AND_REQUIRED_ENDPOINTS")
    return dict(status="FAILED_NUMERICAL_CONTROLS" if ck.failures else completion,
        configuration=CONFIG,benchmark_only=benchmark,selected_benchmark_pair=selected,
        selected_background_id=background_id,
        scope="Exposed covariance BAO shape with one fitted ruler; actual drag/CMB/recombination not calculated.",
        background_scope="Exact adopted scalar current plus declared post-annihilation massless ordinary history through A_cut.",
        source_inverse_status=inv["status"],reference_mapping=inv["reference_mapping"],backgrounds=backgrounds,
        soft_spectra_metadata=inv["soft_spectra_metadata"],retained_state_label_mapping=[
            {k:r[k] for k in ["point_id","background_id","spectrum_index","status"]} for r in inv["state_rows"]],
        data=dict(order=data,values=y.tolist(),covariance=cov.tolist()),
        dust_controls=dust_controls,records=records,counts=ck.counts,maxima=ck.maxima,failures=ck.failures,
        seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=="darwin" else 1024))


def main():
    inv,old,snapshot=read_inputs()
    if sys.argv[1:]==["freeze"]: print(encode(snapshot).decode());return 0
    args=sys.argv[1:];background_id=None
    if len(args)==2 and args[0]=="run-background" and args[1] in [str(i) for i in range(5)]:
        background_id=int(args[1])
    elif args not in [["run"],["benchmark"]]: raise RuntimeError("Use freeze, benchmark, run, or run-background 0..4")
    if json.loads(FREEZE.read_text())!=snapshot: raise RuntimeError("Prospective freeze changed")
    payload=run(inv,old,benchmark=args==["benchmark"],background_id=background_id)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())
    return 2 if payload["failures"] else 0


if __name__=="__main__": sys.exit(main())
