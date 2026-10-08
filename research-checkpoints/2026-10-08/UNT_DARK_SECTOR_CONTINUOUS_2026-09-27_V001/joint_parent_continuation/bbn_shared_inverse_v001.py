"""Prospective shared BBN proxy inverse; stdout only, no dynamics or file writes.

Imports only authenticated local table definitions. Never executes PRIMAT or
an ancestral run/main. Two shared parameters are omega_b and R, not Delta too.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
FREEZE = HERE / "BBN_SHARED_INVERSE_V001_FROZEN.json"
CONFIG = dict(beta=.005, exposed_a0_m_s2=1.2e-10, c_m_s=299792458.,
    hard_gap_lower_exclusive=1., expected_unique_backgrounds=5,
    expected_old_labels=18, expected_soft_quadratures=4,
    expected_coarse_Delta=17, expected_fine_Delta=33,
    band_labels=[1,2,3], bisections=80, angle_orders=[64,128],
    Simpson_panels=1024, arithmetic_tolerance=2e-11,
    zero_contact_tolerance=2e-12,
    quadrature_tolerance=2e-8, root_sigma_tolerance=2e-8,
    polynomial_zero_relative_tolerance=2e-12,
    conserved_scalar_abundance_status="NOT_YET_QUALIFIED")
TABLE_SOURCE_SHA = "96059bdb6f236b84e4d82edf2d6dc7c8d6c61b59504fab84831515a636d3a4c0"
PROXY_RESULT_SHA = "de26bdb564d92853211652933456d7b8a594278fd67fb15c50875c66b1ed4ec9"


def encode(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inputs():
    p=HERE/"bbn_table_proxy_v001.py"
    if sha(p)!=TABLE_SOURCE_SHA:
        raise RuntimeError("Authenticated table helper changed")
    spec=importlib.util.spec_from_file_location("owned_bbn_table_v001",p)
    base=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    # This function reads/authenticates only; it does not instantiate a table
    # or call any qualification, thermal, prediction or producer function.
    budget,cal,obs,old_snapshot=base.inputs()
    f=HERE/"BBN_TABLE_PROXY_V001_FROZEN.json"
    if json.loads(f.read_text())!=old_snapshot:
        raise RuntimeError("Table helper frozen source lineage differs")
    result=HERE/"BBN_TABLE_PROXY_V001_RESULTS.json"
    if sha(result)!=PROXY_RESULT_SHA:
        raise RuntimeError("Qualified proxy receipt differs")
    wrapper=json.loads(result.read_text());proxy=wrapper["payload"]
    # Documented producer canonicalization: original dictionary keys were int.
    hash_payload=dict(proxy)
    hash_payload["matched_Delta0"]={int(k):v for k,v in proxy["matched_Delta0"].items()}
    if (wrapper["freeze_sha256"]!=sha(f) or
        wrapper["payload_sha256"]!=hashlib.sha256(encode(hash_payload)).hexdigest()):
        raise RuntimeError("Qualified proxy wrapper does not authenticate")
    if proxy["status"]!="COMPLETE_PROXY_AND_INTERFACE_QUALIFICATION" or proxy["failures"]:
        raise RuntimeError("Prerequisite table/interface qualification failed")
    files=dict(old_snapshot["files"])
    for p in [f,result,Path(__file__),HERE/"BBN_SHARED_INVERSE_PROTOCOL_V001.md",
              HERE/"SHARED_BBN_PROXY_INVERSE_CALIBRATION_V001.md"]:
        p=p.resolve(strict=True);p.relative_to(ROOT)
        files[str(p.relative_to(ROOT))]=sha(p)
    return base,budget,cal,obs,proxy,dict(configuration=CONFIG,files=files)


class Checks:
    def __init__(self):
        self.counts={};self.maxima={};self.failures=[]
    def check(self,name,a,b=0.,scale=1.,tol=None,context=None):
        tol=CONFIG["arithmetic_tolerance"] if tol is None else tol
        er=abs(a-b)/max(abs(scale),1e-300)
        self.counts[name]=self.counts.get(name,0)+1
        self.maxima[name]=max(self.maxima.get(name,0.),er)
        if not math.isfinite(er) or er>tol:
            self.failures.append(dict(check=name,error=er,tolerance=tol,context=context))
    def yes(self,name,value,context=None):
        self.check(name,int(bool(value)),1.,context=context)


def trim(p):
    p=list(p)
    while len(p)>1 and p[-1]==0.:p.pop()
    return p


def ev(p,x):
    value=0.
    for v in reversed(p):value=value*x+v
    return value


def add(p,q):
    a=[0.]*max(len(p),len(q))
    for i,v in enumerate(p):a[i]+=v
    for i,v in enumerate(q):a[i]+=v
    return trim(a)


def mul(p,q):
    a=[0.]*(len(p)+len(q)-1)
    for i,v in enumerate(p):
        for j,w in enumerate(q):a[i+j]+=v*w
    return trim(a)


def scale(p,a):return trim([a*v for v in p])


def unique(values,tol=2e-12):
    ans=[]
    for v in sorted(values):
        if not ans or abs(v-ans[-1])>tol:ans.append(v)
    return ans


def proots(p):
    """All real roots on [0,1], by derivative partitions and sign brackets.

    Includes possible even-multiplicity roots at stationary points. This is
    controlled floating point isolation, not formally directed arithmetic.
    """
    p=trim(p)
    if len(p)==1:return []
    if len(p)==2:
        x=-p[0]/p[1]
        return [min(1.,max(0.,x))] if -2e-14<=x<=1+2e-14 else []
    critical=proots([i*p[i] for i in range(1,len(p))])
    split=unique([0.,*critical,1.],2e-14)
    tol=CONFIG["polynomial_zero_relative_tolerance"]*max(sum(abs(v) for v in p),1e-300)
    roots=[x for x in split if abs(ev(p,x))<=tol]
    for a,b in zip(split,split[1:]):
        fa,fb=ev(p,a),ev(p,b)
        # A qualified endpoint root has already been retained. Do not turn
        # its last-bit signed value into two spurious neighboring crossings
        # at a repeated root. Such near-tangencies remain tolerance-limited.
        if abs(fa)<=tol or abs(fb)<=tol:continue
        if fa*fb>=0:continue
        for _ in range(CONFIG["bisections"]):
            m=(a+b)/2;fm=ev(p,m)
            if fa*fm<=0:b=m
            else:a=m;fa=fm
        roots.append((a+b)/2)
    return unique(roots)


def lagrange_polynomial(nodes,values):
    out=[0.]
    for i,(x,v) in enumerate(zip(nodes,values)):
        p=[1.];den=1.
        for j,y in enumerate(nodes):
            if j!=i:p=mul(p,[-y,1.]);den*=x-y
        out=add(out,scale(p,v/den))
    return out


def merge(intervals):
    ans=[]
    for a,b in sorted(intervals):
        if ans and a<=ans[-1][1]+2e-13:ans[-1][1]=max(ans[-1][1],b)
        else:ans.append([a,b])
    return ans


def intersect(a,b):
    return merge([[max(x,u),max(max(x,u),min(y,v))] for x,y in a for u,v in b
                  if max(x,u)<=min(y,v)+2e-14])


def contour_geometry(base,table,obs,ck):
    coarse=[d for d in table.y if d>=0]
    fine=sorted(set(coarse+[(a+b)/2 for a,b in zip(coarse,coarse[1:])]))
    ck.yes("Delta_mesh_census",len(coarse)==17 and len(fine)==33)
    points={};curves=[]
    def point(x,d,role):
        key=(round(x,14),d)
        if key not in points:points[key]=dict(omega_b=x,Delta=d,roles=[])
        if role not in points[key]["roles"]:points[key]["roles"].append(role)
    for d in fine:
        item=dict(Delta=d,coarse_node=d in coarse,central={},marginal_bands={},joint_bands={})
        for name,col,scol in [("helium",4,5),("deuterium",6,7)]:
            o=obs[name];sig=o["sigma"];budget=base.CONFIG["interpolation_allowance"][name]
            center=[];bands={str(k):[] for k in CONFIG["band_labels"]}
            boundary_roots={str(k):{"-1":[],"1":[]} for k in CONFIG["band_labels"]}
            for left,right in zip(table.x,table.x[1:]):
                mid=(left+right)/2;xs=base.nodes(table.x,mid)
                vals=[(table.sample(x,d)[col]-o["value"])/sig for x in xs]
                xx=[(x-left)/(right-left) for x in xs]
                residual=lagrange_polynomial(xx,vals)
                # Stencil is fixed on the open interval. At nodes its value
                # still agrees; use direct samples only for validation.
                sig0=table.sample(left,d,degree=1)[scol]/sig
                sig1=table.sample(right,d,degree=1)[scol]/sig
                ck.yes("positive_theory_sigma",sig0>0 and sig1>0)
                variance=add([1.],mul([sig0,sig1-sig0],[sig0,sig1-sig0]))
                for t in [0.,.37,1.]:
                    direct=(table.sample(left+t*(right-left),d)[col]-o["value"])/sig
                    ck.check("local_cubic_polynomial",ev(residual,t),direct,max(1.,abs(direct)))
                rr=proots(residual)
                for t in rr:
                    x=left+t*(right-left)
                    ck.check("central_root",ev(residual,t),tol=CONFIG["root_sigma_tolerance"])
                    center.append(x)
                for k in CONFIG["band_labels"]:
                    accepted=[]
                    for sign in [-1,1]:
                        r=add(residual,[-sign*budget/sig])
                        squared=add(mul(r,r),scale(variance,-k*k))
                        for t in proots(squared):
                            lhs=ev(r,t);rhs=sign*k*math.sqrt(ev(variance,t))
                            if sign*lhs<0:
                                ck.yes("squared_extraneous_sign_rejected",True)
                                continue
                            ck.check("signed_band_root",lhs,rhs,
                                     tol=CONFIG["root_sigma_tolerance"],context=[d,name,k,sign])
                            accepted.append(t)
                            boundary_roots[str(k)][str(sign)].append(left+t*(right-left))
                    cuts=unique([0.,*accepted,1.])
                    def inside(t):
                        return abs(ev(residual,t))<=k*math.sqrt(ev(variance,t))+budget/sig+1e-10
                    for a,b in zip(cuts,cuts[1:]):
                        if inside((a+b)/2):bands[str(k)].append([left+a*(right-left),left+b*(right-left)])
                    for t in accepted:
                        if inside(t):
                            x=left+t*(right-left);bands[str(k)].append([x,x])
            center=unique(center,2e-13)
            for x in center:point(x,d,"central:"+name)
            item["central"][name]=center
            item["marginal_bands"][name]={str(k):dict(
                intervals=merge(bands[str(k)]),
                signed_boundary_roots={s:unique(v,2e-13) for s,v in boundary_roots[str(k)].items()})
                for k in CONFIG["band_labels"]}
        for k in CONFIG["band_labels"]:
            a=item["marginal_bands"]["helium"][str(k)]["intervals"]
            b=item["marginal_bands"]["deuterium"][str(k)]["intervals"]
            joint=intersect(a,b);item["joint_bands"][str(k)]=joint
            for i,(lo,hi) in enumerate(joint):
                point(lo,d,"joint:"+str(k)+":"+str(i)+":lower")
                point(hi,d,"joint:"+str(k)+":"+str(i)+":upper")
        curves.append(item)
    return coarse,fine,curves,list(points.values())


def gauss_rule(n):
    pairs=[]
    for i in range((n+1)//2):
        x=math.cos(math.pi*(i+.75)/(n+.5))
        for _ in range(80):
            p0,p1=1.,x
            for k in range(2,n+1):p0,p1=p1,((2*k-1)*x*p1-(k-1)*p0)/k
            derivative=n*(x*p1-p0)/(x*x-1)
            nextx=x-p1/derivative
            if nextx==x or abs(nextx-x)<2e-16:x=nextx;break
            x=nextx
        p0,p1=1.,x
        for k in range(2,n+1):p0,p1=p1,((2*k-1)*x*p1-(k-1)*p0)/k
        derivative=n*(x*p1-p0)/(x*x-1)
        w=2/((1-x*x)*derivative*derivative)
        pairs.extend([(-x,w),(x,w)])
    return sorted(pairs)


def angle_rule(n):
    if n:
        return [(w*math.pi/4,math.sin((x+1)*math.pi/4)**2,
                 math.cos((x+1)*math.pi/4)**2) for x,w in gauss_rule(n)]
    n=CONFIG["Simpson_panels"]
    return [((1 if i in [0,n] else 4 if i%2 else 2)*math.pi/(6*n),
             math.sin(i*math.pi/(2*n))**2,math.cos(i*math.pi/(2*n))**2) for i in range(n+1)]


def action_shape(s,q):
    return 4/math.pi*math.sqrt(s)*math.fsum(w*c*math.sqrt(1+s*s*v) for w,v,c in q)


def invert_shape(target,q):
    lo=0.;hi=1.
    for _ in range(CONFIG["bisections"]):
        s=(lo+hi)/2
        if action_shape(s,q)<target:lo=s
        else:hi=s
    return (lo+hi)/2


def orbit(R,b2,q):
    pp=[(w,v,c,R*R+b2*(1+v)/2) for w,v,c in q]
    J=math.fsum(w/math.sqrt(a) for w,v,c,a in pp)
    ell=math.fsum(w*(1+v)/a**1.5 for w,v,c,a in pp)
    omega=math.pi/(2*J)
    return dict(I=2/math.pi*b2*math.fsum(w*c*math.sqrt(a) for w,v,c,a in pp),
        e=R*R*b2/2+b2*b2/4,
        p=b2*b2/4*math.fsum(w*v*v/math.sqrt(a) for w,v,c,a in pp)/J,
        mean2=b2*math.fsum(w*v/math.sqrt(a) for w,v,c,a in pp)/J,
        omega=omega,eII=omega*omega*ell/(2*J*(R*R+b2)))


def cubic(d,h):
    return 2*d/math.sqrt(3)*math.sinh(math.asinh(3*math.sqrt(3)*h/(2*d*d))/3)


def vacuum(ds,ws,R,beta,S):
    yy=[cubic(d,S) for d in ds]+[cubic(R,S)]
    dd=ds+[R];ww=ws+[beta]
    Q=math.fsum(w*(d*d*y*y/2+3*y**4/4) for d,w,y in zip(dd,ww,yy))
    return Q,yy


def solve_vacuum(ds,ws,R,beta,target,start):
    lo=0.;hi=start
    while vacuum(ds,ws,R,beta,hi)[0]<target:
        hi*=2
        if not math.isfinite(hi):raise RuntimeError("Vacuum bracket overflow")
    for _ in range(CONFIG["bisections"]):
        mid=(lo+hi)/2
        if vacuum(ds,ws,R,beta,mid)[0]<target:lo=mid
        else:hi=mid
    S=(lo+hi)/2
    return S,*vacuum(ds,ws,R,beta,S)


def prediction(base,table,obs,x,d,ck):
    cub=table.sample(x,d);quad=table.sample(x,d,degree=2);lin=table.sample(x,d,degree=1)
    zero=table.sample(x,0.)
    shifted_x=x*(base.CONFIG["table_T0_K"]/base.CONFIG["inherited_T0_K"])**3
    shift=table.sample(shifted_x,d) if table.x[0]<=shifted_x<=table.x[-1] else None
    local=.020<=x<=.024 and 0<=d<=3
    out={}
    for name,col,scol in [("helium",4,5),("deuterium",6,7)]:
        b=base.CONFIG["interpolation_allowance"][name]
        if local:ck.check("local_target_interpolation_"+name,cub[col],quad[col],tol=b)
        out[name]=dict(prediction=cub[col],signed_residual=cub[col]-obs[name]["value"],
            observational_sigma=obs[name]["sigma"],theory_sigma=lin[scol],
            interpolation_allowance=b,cubic_minus_quadratic=cub[col]-quad[col],
            descriptive_marginal_z=(cub[col]-obs[name]["value"])/math.hypot(obs[name]["sigma"],lin[scol]),
            matched_Delta0=zero[col],minus_matched_Delta0=cub[col]-zero[col],
            T0_eta_coordinate_sensitivity=None if shift is None else shift[col]-cub[col])
    Y,D=cub[4],cub[6]
    return dict(status="TABLE_PROXY",local_numerical_rectangle=local,observables=out,
        helium_D_only_denominator_correction=Y*(1+2*D)/(1+2*Y*D)-Y,
        helium_unprovided_He3_linear_coefficient=3*Y*(1-Y)/(1+2*Y*D)**2)


def run(base,budget,cal,obs,proxy):
    started=time.perf_counter();ck=Checks();table=base.AbundanceTable()
    inherited=base.Checks();withheld=table.qualify(inherited)
    ck.yes("inherited_interpolation_qualification",not inherited.failures)
    # Root isolation witnesses include crossings, repeated roots and endpoints.
    for roots in [[.17],[0.,.3,1.],[.2,.2,.7,.7],[.01,.12,.37,.58,.83,.99]]:
        polynomial=[1.]
        for x in roots:polynomial=mul(polynomial,[-x,1.])
        actual=proots(polynomial);want=unique(roots)
        ck.yes("synthetic_root_census",len(actual)==len(want),[roots,actual])
        for a,b in zip(actual,want):ck.check("synthetic_root_position",a,b)
    q64,q128,qsim=angle_rule(64),angle_rule(128),angle_rule(None)
    for n in CONFIG["angle_orders"]:
        qq=gauss_rule(n)
        ck.yes("GL_positive",len(qq)==n and all(w>0 for x,w in qq))
        for p in range(9):
            ck.check("GL_moment",math.fsum(w*x**p for x,w in qq),0. if p%2 else 2/(p+1),
                     tol=CONFIG["zero_contact_tolerance"] if p%2 else None)
        for (x,w),(y,v) in zip(qq,reversed(qq)):
            ck.check("GL_symmetry",x,-y,tol=CONFIG["zero_contact_tolerance"])
            ck.check("GL_weight_symmetry",w,v,max(1.,w,v),tol=CONFIG["zero_contact_tolerance"])
    C4=((3*math.sqrt(math.pi)/2)*math.gamma(.75)/math.gamma(.25))**(4/3)
    ck.check("Gamma_endpoint",action_shape(1.,q128),C4**(-.75),C4**(-.75))
    for s in [1e-8,.01,.5,1.]:
        target=action_shape(s,q128);got=invert_shape(target,q128)
        ck.check("synthetic_inverse_s",got,s,s)
        R=math.sqrt((1-s*s)/s);b2=2*s
        oracle=orbit(R,b2,qsim)
        ck.check("independent_energy_centered_action",oracle["I"],target,target,
                 tol=CONFIG["quadrature_tolerance"])
        ck.check("synthetic_energy",oracle["e"],1.)
        ck.check("shape_GL64",action_shape(s,q64),target,target,tol=CONFIG["quadrature_tolerance"])
    coarse,fine,geometry,points=contour_geometry(base,table,obs,ck)
    for i,p in enumerate(points):
        p["point_id"]=i;p["coarse_node"]=p["Delta"] in coarse
        p["prediction"]=prediction(base,table,obs,p["omega_b"],p["Delta"],ck)
    keys=[];backgrounds=[];mapping=[]
    for ref in cal["references"]:
        meta=ref["inherited_reference_input"]
        key=(meta["H0_km_s_Mpc"],ref["Omega_Lambda"])
        if key not in keys:
            keys.append(key);backgrounds.append(dict(background_id=len(keys)-1,
                H0_km_s_Mpc=key[0],H0_s_inverse=ref["H0_s_inverse"],
                Omega_Lambda=key[1],Omega_m=1-key[1],representative_reference=ref["reference"],old_labels=[]))
        bi=keys.index(key);backgrounds[bi]["old_labels"].append(ref["reference"])
        mapping.append(dict(reference=ref["reference"],reference_case=ref["reference_case"],
            background_id=bi,old_bbn_marker=ref["bbn"],old_metadata=meta))
    ck.yes("reference_mapping_census",len(backgrounds)==5 and len(mapping)==18)
    ck.yes("spectra_census",len(cal["spectra"])==4 and
           {(s["gap"],s["order"]) for s in cal["spectra"]}=={(.001,64),(.001,128),(.002,64),(.002,128)})
    photons={}
    for b in budget["rows"]:
        ref=b["reference"]
        if ref in photons:ck.check("photon_reference_copies",b["Omega_gamma"],photons[ref],photons[ref])
        else:photons[ref]=b["Omega_gamma"]
    oldrows={(r["spectrum_index"],r["reference"]):r for r in cal["rows"]}
    beta=CONFIG["beta"];fnu=(7/8)*(4/11)**(4/3)
    ck.check("inherited_C4",C4,budget["C"],C4)
    rows=[];constants=[]
    llo,lhi=proxy["thermal_interface"]["log_ratio_all_T_intersection"]
    th=proxy["thermal_interface"]["per_resolution"][-1]
    Hfactor=(7*math.pi**2/120)*(th["sigma_bounds"][1]/(11*math.pi**2/45))**(4/3)/th["plasma_rho_over_T4_bounds"][0]
    Alower=proxy["thermal_history_lower_bound_A_at_10keV"]
    for bg in backgrounds:
        ri=bg["representative_reference"];ph=photons[ri]
        for oldref in bg["old_labels"]:ck.check("duplicate_background_photons",photons[oldref],ph,ph)
        for si,spec in enumerate(cal["spectra"]):
            ds=spec["spectrum"]["delta"];ws=spec["spectrum"]["weights"]
            kb=math.fsum(ws)+beta;gstar=CONFIG["exposed_a0_m_s2"]/(16*kb/(3*math.pi))
            L=3*kb*(CONFIG["c_m_s"]*bg["H0_s_inverse"])**2/(2*gstar*gstar)
            old=oldrows[(si,ri)];targetvac=L*bg["Omega_Lambda"]
            ck.check("inherited_vacuum_target",targetvac,old["target_DeltaU"],targetvac)
            ck.check("inherited_gstar",gstar,old["gstar_m_s2"],gstar)
            constants.append(dict(background_id=bg["background_id"],spectrum_index=si,
                Kb=kb,gstar=gstar,L=L,Omega_gamma=ph,target_DeltaU=targetvac,
                S_infinity=old["S"],soft_gap=spec["gap"],soft_order=spec["order"]))
            for point in points:
                x=point["omega_b"];Delta=point["Delta"]
                ob=x/(bg["H0_km_s_Mpc"]/100)**2;oe=bg["Omega_m"]-ob;E=L*oe;e=E/beta
                row=dict(point_id=point["point_id"],background_id=bg["background_id"],
                    spectrum_index=si,omega_b=x,Delta=Delta,Omega_b=ob,Omega_exc=oe,
                    E=E,DeltaU_target=targetvac)
                if oe<=0:
                    row["status"]="NONPOSITIVE_EXCITATION";rows.append(row);continue
                if Delta==0:
                    row.update(status="INFINITE_GAP_STANDARD_LIMIT",R=None,I=None,
                        Q=0.,S=old["S"],J_static=None,
                        limit="R->infinity, I->0 with RI=e>0; not a finite empty state; E(A)=E A^3")
                    rows.append(row);continue
                I=(Delta*L*ph*fnu/(beta*C4))**.75
                z=I/e**.75
                if z>=action_shape(1.,q128):
                    row.update(status="NO_POSITIVE_QUADRATIC_GAP",I=I,normalized_action=z)
                    rows.append(row);continue
                s=invert_shape(z,q128);R2=math.sqrt(e)*(1-s*s)/s;R=math.sqrt(R2);b2=2*math.sqrt(e)*s
                row.update(R=R,I=I,s=s)
                if R<=1:
                    row["status"]="OUTSIDE_HARD_BAND";rows.append(row);continue
                s64=invert_shape(z,q64);R64=math.sqrt(math.sqrt(e)*(1-s64*s64)/s64)
                ck.check("gap_GL64",R64,R,R,tol=CONFIG["quadrature_tolerance"])
                o=orbit(R,b2,q128);o64=orbit(R,b2,q64)
                for k in ["I","omega","p","mean2","eII"]:
                    ck.check("moment_GL64_"+k,o64[k],o[k],o[k],tol=CONFIG["quadrature_tolerance"])
                ck.check("inverse_action",o["I"],I,I)
                ck.check("inverse_energy",o["e"],e,e)
                ck.check("action_virial",I*o["omega"],e+o["p"],e+o["p"])
                ck.check("energy_virial",R2*o["mean2"]+3*o["p"],e,e)
                Q=beta*C4*I**(4/3);D=beta*R2*math.sqrt(C4)*I**(2/3)
                ck.check("Delta_reconstruction",Q/(L*ph*fnu),Delta,Delta)
                S,vacuum_value,yy=solve_vacuum(ds,ws,R,beta,targetvac,old["S"])
                ck.check("matched_vacuum",vacuum_value,targetvac,targetvac)
                elastic=math.fsum(w*((S-d*y)**2/2+y**4/4) for d,w,y in zip(ds+[R],ws+[beta],yy))
                ck.check("contact_energy_ledger",vacuum_value+elastic,kb*S*S/2,
                         max(1.,abs(vacuum_value)+abs(elastic),kb*S*S/2),
                         tol=CONFIG["zero_contact_tolerance"])
                for d,y in zip(ds+[R],yy):ck.check("minimum_cubic",y*(d*d+y*y),d*S,d*S)
                q=3*(e+o["p"])/(R**4+4*e);K0=beta*q
                cI=I*o["eII"]/o["omega"];J=beta*(o["omega"]**2/o["eII"]+3*I*o["omega"])
                ck.check("static_ratio",K0/J,3*cI/((R**4+4*e)*(1+3*cI)),K0/J)
                xx=Delta*Hfactor
                Hr=lambda logratio: math.sqrt((1+xx)/(1+xx*math.exp(-logratio)))-1
                row.update(status="FINITE_HARD_STATE",hard_energy=e,pressure=beta*o["p"],
                    w=o["p"]/e,omega=o["omega"],eII=o["eII"],cI2=cI,
                    Q=Q,D=D,Q_over_E=Q/E,S=S,DeltaU=vacuum_value,
                    source_hardening_sufficient=S*S/R**4<1/12,
                    source_hardening_ratio=S/R2,K0=K0,J_static=J,
                    cold_parameter=e/R**4,J_cold=(4/3)*beta*R**4,
                    J_cold_from_proxy=(4/3)*C4**3*L*oe**4/(ph*fnu*Delta)**3,
                    fractional_gap_energy_bound_at_10keV=D/(Q*Alower*Alower),
                    fixed_heating_fractional_H_envelope=[min(0.,Hr(llo)),max(0.,Hr(lhi))],
                    GL64_minus_primary_R=R64-R)
                ck.check("cold_reaction_identity",row["J_cold_from_proxy"],
                         (4/3)*beta*(e/I)**4,row["J_cold_from_proxy"])
                # The latter identity concerns the harmonic estimate R=e/I;
                # it is not asserted equal to the finite-R J or exact R^4.
                rows.append(row)
    ck.yes("complete_state_census",len(rows)==len(points)*len(backgrounds)*len(cal["spectra"]))
    contrasts=[];lookup={(r["point_id"],r["background_id"],r["spectrum_index"]):r for r in rows}
    for a,b in [(0,1),(2,3)]:
        ck.yes("soft_pair_metadata",cal["spectra"][a]["gap"]==cal["spectra"][b]["gap"] and
               [cal["spectra"][a]["order"],cal["spectra"][b]["order"]]==[64,128])
        for bg in backgrounds:
            deltas=[];status_mismatches=[]
            for p in points:
                aa=lookup[(p["point_id"],bg["background_id"],a)]
                bb=lookup[(p["point_id"],bg["background_id"],b)]
                if aa["status"]!=bb["status"]:status_mismatches.append(p["point_id"])
                if aa["status"]==bb["status"]=="FINITE_HARD_STATE":
                    deltas.append({k:(aa[k]-bb[k])/max(abs(bb[k]),1e-300) for k in ["R","S","E","I","J_static","K0"]})
            contrasts.append(dict(background_id=bg["background_id"],spectrum_pair=[a,b],
                matched_finite_states=len(deltas),status_mismatches=status_mismatches,
                max_relative_differences={k:max([abs(v[k]) for v in deltas],default=0.) for k in ["R","S","E","I","J_static","K0"]}))
    profiles=[]
    for bg in backgrounds:
        for si in range(4):
            for k in CONFIG["band_labels"]:
                out=dict(background_id=bg["background_id"],spectrum_index=si,band_label=k)
                for label,mesh in [("coarse",coarse),("fine",fine)]:
                    pp=[p for p in points if p["Delta"] in mesh and any(v.startswith("joint:"+str(k)+":") for v in p["roles"])]
                    rr=[lookup[(p["point_id"],bg["background_id"],si)] for p in pp]
                    finite=[r for r in rr if r["status"]=="FINITE_HARD_STATE"]
                    out[label]=dict(sampled_boundary_points=len(rr),finite_states=len(finite),
                        outside_local_interpolation_qualification_points=sum(
                            not p["prediction"]["local_numerical_rectangle"] for p in pp),
                        includes_infinite_gap_limit=any(r["status"]=="INFINITE_GAP_STANDARD_LIMIT" for r in rr),
                        unsupported_states=sum(r["status"] not in ["FINITE_HARD_STATE","INFINITE_GAP_STANDARD_LIMIT"] for r in rr),
                        finite_ranges={key:([min(r[key] for r in finite),max(r[key] for r in finite)] if finite else None)
                                       for key in ["R","omega_b","Delta","E","I","S","J_static"]})
                profiles.append(out)
    return dict(status="FAILED_NUMERICAL_CONTROLS" if ck.failures else "COMPLETE_CONDITIONAL_PROXY_INVERSE",
        configuration=CONFIG,scope="Two-parameter shared inverse of fixed-heating BBN proxy; no joint likelihood or galaxy solution.",
        conserved_scalar_abundance_status="NOT_YET_QUALIFIED",parameter_count=2,
        parameters=["global omega_b","global hard R"],observations=obs,
        prior_reference_assumptions=cal["inherited_reference_assumptions"],
        prior_reference_scope=cal["inherited_reference_scope"],reference_mapping=mapping,
        backgrounds=backgrounds,soft_spectra_metadata=[{k:s[k] for k in ["gap","order"]} for s in cal["spectra"]],
        constants=constants,C4=C4,fnu=fnu,coarse_Delta=coarse,fine_Delta=fine,
        contour_geometry=geometry,table_points=points,state_rows=rows,
        sampled_profiles=profiles,soft_resolution_contrasts=contrasts,
        inherited_table_controls=dict(counts=inherited.counts,maxima=inherited.maxima,
                                      failures=inherited.failures,withheld=withheld),
        thermal_interface_receipt_sha256=PROXY_RESULT_SHA,
        thermal_history_A_lower_10keV=Alower,
        counts=ck.counts,maxima=ck.maxima,failures=ck.failures,
        seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=="darwin" else 1024))


def main():
    base,budget,cal,obs,proxy,snapshot=inputs()
    if sys.argv[1:]==["freeze"]:
        print(encode(snapshot).decode());return 0
    if sys.argv[1:]!=["run"]:raise RuntimeError("Use freeze or run")
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError("Prospective freeze differs")
    payload=run(base,budget,cal,obs,proxy)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
                      payload=payload)).decode())
    return 2 if payload["failures"] else 0


if __name__=="__main__":
    sys.exit(main())
