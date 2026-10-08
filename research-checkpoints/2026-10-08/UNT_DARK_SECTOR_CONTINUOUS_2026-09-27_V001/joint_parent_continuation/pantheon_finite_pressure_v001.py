"""Inert Pantheon+ same-state distance producer; root alone freezes/runs.

One magnitude offset, no state/cosmology fit. Never executes downloaded code
or an ancestor's numerical run. Output only, no writes or network access.
"""
import os
for _thread_variable in ["OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS",
                         "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS"]:
    os.environ[_thread_variable]="1"
import base64
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import resource
import sys
import time
import urllib.parse
import zlib
import numpy as np

sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/"PANTHEON_FINITE_PRESSURE_V001_FROZEN.json"
KERNEL_SHA="b59ab0f88e39234929eb6fa4d0a53bba0b1bf4dc4fbd9891b704b5cd89e19bf1"
COMMIT="c447f0fea703fcd0fff57de5000947b5ca81286b"
RECEIPTS={
    "vector":"pantheon_inputs_v001/PANTHEON_VECTOR_V001_TRANSPORT.json",
    "covariance":"pantheon_inputs_v001/PANTHEON_COVARIANCE_V001_TRANSPORT.json",
    "readme":"pantheon_inputs_v001/PANTHEON_README_V001_TRANSPORT.json",
    "likelihood":"pantheon_inputs_v001/PANTHEON_LIKELIHOOD_V001_TRANSPORT.json"}
REMOTE_PATHS={
    "vector":"Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat",
    "covariance":"Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov",
    "readme":"Pantheon+_Data/4_DISTANCES_AND_COVAR/README",
    "likelihood":"Pantheon+_Data/5_COSMOLOGY/cosmosis_likelihoods/Pantheon+_only_cosmosis_likelihood.py"}
CONFIG=dict(expected_total_rows=1701,redshift_cut_exclusive=.01,
    expected_points=67,expected_backgrounds=5,expected_spectra=4,expected_labels=1340,
    angle_orders=[64,128],interval_orders=[8,16],distance_batch=64,solve_batch=32,
    endpoint_iterations=64,endpoint_logA_target=4e-15,Simpson_panels=512,
    covariance_tolerance=2e-12,arithmetic_tolerance=2e-11,
    distance_tolerance=2e-10,material_tolerance=2e-10,solve_tolerance=2e-10,
    offset_refinement_tolerance=2e-9,score_refinement_tolerance=2e-6,
    source_size_ceiling=64*1024*1024,profiled_parameters=["common magnitude offset"],
    observational_success_gate=None,unused_validation=False)


def encode(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_receipt(path,key):
    packet=json.loads(path.read_text())
    for k,v in {"kind":"public_source_verbatim_zlib_base64","encoding":"zlib_base64",
                "repository":"PantheonPlusSH0ES/DataRelease","commit":COMMIT,
                "path":REMOTE_PATHS[key],"key":key}.items():
        if packet.get(k)!=v:raise RuntimeError("Receipt metadata differs: "+key+"/"+k)
    expected_url="https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/"+COMMIT+"/"+urllib.parse.quote(REMOTE_PATHS[key],safe="/")
    if packet["url"]!=expected_url:raise RuntimeError("Receipt URL differs")
    if packet["transport_sha256"]!=sha(HERE/"fetch_pantheon_reference_v001.py"):
        raise RuntimeError("Fetcher provenance differs")
    size=packet["bytes"]
    if not isinstance(size,int) or not 0<size<=CONFIG["source_size_ceiling"]:
        raise RuntimeError("Unexpected raw source size")
    parts=[]
    if "data_parts" in packet:
        if "data" in packet:raise RuntimeError("Ambiguous source transport")
        joined=[]
        for part in packet["data_parts"]:
            p=(path.parent/part["file"]).resolve(strict=True);p.relative_to(path.parent)
            rawpart=p.read_bytes()
            if len(rawpart)!=part["characters"]+1 or not rawpart.endswith(b"\n"):
                raise RuntimeError("Transport part size/final LF differs")
            # validate=True below rejects any further whitespace, including LF.
            joined.append(rawpart[:-1]);parts.append(p)
        compressed=base64.b64decode(b"".join(joined),validate=True)
    else:compressed=base64.b64decode(packet["data"],validate=True)
    dec=zlib.decompressobj();raw=dec.decompress(compressed,size+1)
    if len(raw)!=size or not dec.eof or dec.unused_data or dec.unconsumed_tail:
        raise RuntimeError("Raw source size/stream failed")
    if hashlib.sha256(raw).hexdigest()!=packet["sha256"]:raise RuntimeError("Raw source hash differs")
    raw.decode("utf-8")
    return raw,{k:packet[k] for k in ["repository","commit","path","url","key","bytes","sha256","transport_sha256"]},parts


def inputs():
    module=HERE/"finite_pressure_bao_ruler_v001.py"
    if sha(module)!=KERNEL_SHA:raise RuntimeError("Expansion source identity changed")
    spec=importlib.util.spec_from_file_location("owned_expansion_v001",module)
    base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
    inv,old,prior=base.read_inputs()  # authentication only, not run or science
    kfreeze=HERE/"FINITE_PRESSURE_BAO_RULER_V001_FROZEN.json"
    if json.loads(kfreeze.read_text())!=prior:raise RuntimeError("Expansion freeze changed")
    files=dict(prior["files"]);files[str(kfreeze.relative_to(ROOT))]=sha(kfreeze)
    raw={};metadata={}
    for key,rel in RECEIPTS.items():
        p=(HERE/rel).resolve(strict=True);p.relative_to(HERE)
        raw[key],metadata[key],parts=decode_receipt(p,key)
        files[str(p.relative_to(ROOT))]=sha(p)
        for part in parts:files[str(part.relative_to(ROOT))]=sha(part)
    for p in [Path(__file__),HERE/"PANTHEON_FINITE_PRESSURE_PROTOCOL_V001.md",
              HERE/"PANTHEON_INPUT_SELECTION_V001.md",HERE/"fetch_pantheon_reference_v001.py"]:
        p=p.resolve(strict=True);p.relative_to(ROOT);files[str(p.relative_to(ROOT))]=sha(p)
    return base,inv,raw,metadata,dict(configuration=CONFIG,receipt_paths=RECEIPTS,
                                    raw_source_metadata=metadata,files=files)


class Checks:
    def __init__(self):self.counts={};self.maxima={};self.failures=[]
    def check(self,name,a,b=0.,scale=1.,tol=None,context=None):
        tol=CONFIG["arithmetic_tolerance"] if tol is None else tol
        er=np.abs(np.asarray(a)-np.asarray(b))/np.maximum(np.abs(scale),1e-300)
        mx=float(np.max(er));self.counts[name]=self.counts.get(name,0)+int(er.size)
        self.maxima[name]=max(self.maxima.get(name,0.),mx)
        if not np.all(np.isfinite(er)) or mx>tol:
            self.failures.append(dict(check=name,error=mx,tolerance=tol,context=context))
    def yes(self,name,value,context=None):self.check(name,int(bool(value)),1.,context=context)


def packed(array):
    arr=np.asarray(array,dtype="<f8",order="C");raw=arr.tobytes()
    compressed=zlib.compress(raw,9)
    if zlib.decompress(compressed)!=raw:raise RuntimeError("Array transport roundtrip failed")
    return dict(encoding="zlib_base64",dtype="<f8",order="C",shape=list(arr.shape),
        bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
        data=base64.b64encode(compressed).decode())


def load_data(raw,ck):
    table=np.genfromtxt(io.StringIO(raw["vector"].decode()),names=True,dtype=None,
                        encoding="utf-8",autostrip=True)
    columns=table.dtype.names
    for key in ["CID","IDSURVEY","zHD","zHEL","m_b_corr"]:
        if key not in columns:raise RuntimeError("Missing Pantheon column: "+key)
    if len(table)!=CONFIG["expected_total_rows"]:raise RuntimeError("Total vector row census differs")
    stream=raw["covariance"].decode();head,body=stream.split("\n",1)
    n=int(head.strip());values=np.fromstring(body,sep=" ")
    if n!=len(table) or len(values)!=n*n:raise RuntimeError("Covariance layout differs")
    full=values.reshape(n,n)
    mask=np.asarray(table["zHD"]>CONFIG["redshift_cut_exclusive"])
    ix=np.flatnonzero(mask);cov=full[np.ix_(ix,ix)].copy()
    zh=np.asarray(table["zHD"][mask],float);zhel=np.asarray(table["zHEL"][mask],float)
    y=np.asarray(table["m_b_corr"][mask],float)
    ck.yes("data_finite",np.all(np.isfinite(full)) and np.all(np.isfinite(y)) and
           np.all(np.isfinite(zh)) and np.all(np.isfinite(zhel)))
    ck.yes("positive_distance_domain",len(ix)>1 and np.all(zh>.01) and np.all(1+zhel>0))
    ck.check("covariance_symmetry",cov,cov.T,tol=CONFIG["covariance_tolerance"])
    ck.yes("positive_covariance_diagonal",np.all(np.diag(cov)>0))
    # Independent indexing witness: direct original flat-array addresses.
    for a,b in [(0,0),(0,len(ix)-1),(len(ix)//2,len(ix)//3),(len(ix)-1,len(ix)-1)]:
        ck.check("covariance_original_index",cov[a,b],values[int(ix[a])*n+int(ix[b])])
    metadata=dict(total_rows=n,selected_rows=len(ix),mask_sha256=hashlib.sha256(mask.astype("u1").tobytes()).hexdigest(),
        original_row_indices=ix.tolist(),CID=[str(x) for x in table["CID"][mask]],
        IDSURVEY=[int(x) for x in table["IDSURVEY"][mask]],zHD=zh.tolist(),zHEL=zhel.tolist(),
        m_b_corr=y.tolist(),covariance_diagonal=np.diag(cov).tolist(),
        covariance_selected_f64_sha256=hashlib.sha256(np.asarray(cov,dtype="<f8").tobytes()).hexdigest(),
        source_columns=list(columns))
    del full,values,table,stream,body
    return zh,zhel,y,cov,metadata


def forward(L,rhs):
    rhs=np.asarray(rhs,float);one=rhs.ndim==1
    B=rhs[:,None] if one else rhs;answer=np.empty_like(B)
    for i in range(len(L)):
        answer[i]=(B[i]-L[i,:i]@answer[:i])/L[i,i]
    return answer[:,0] if one else answer


def backward(L,rhs):
    rhs=np.asarray(rhs,float);one=rhs.ndim==1
    B=rhs[:,None] if one else rhs;answer=np.empty_like(B)
    for i in range(len(L)-1,-1,-1):
        answer[i]=(B[i]-L[i+1:,i]@answer[i+1:])/L[i,i]
    return answer[:,0] if one else answer


def endpoint_vector(k,A,ck,context):
    target=np.log(A)
    if k.r1==0.:return 3*target
    lo=2*target;hi=3*target;t=(lo+hi)/2;done=np.zeros(len(A),bool)
    for _ in range(CONFIG["endpoint_iterations"]):
        active=np.flatnonzero(~done)
        if not len(active):break
        o=k.fields(t[active]);res=np.log(o["A"])-target[active]
        reached=np.abs(res)<=CONFIG["endpoint_logA_target"]
        done[active[reached]]=True
        todo=active[~reached]
        if not len(todo):continue
        rr=res[~reached];above=rr>0
        hi[todo[above]]=t[todo[above]];lo[todo[~above]]=t[todo[~above]]
        trial=t[todo]-3*rr/o["lam"][~reached]
        inside=(trial>=lo[todo])&(trial<=hi[todo])&np.isfinite(trial)
        t[todo]=np.where(inside,trial,(lo[todo]+hi[todo])/2)
    final=k.fields(t)["A"]
    ck.check("vector_endpoint_A",final,A,A,tol=CONFIG["distance_tolerance"],context=context)
    ck.yes("vector_endpoint_converged",np.all(done),context)
    return t


def cumulative_distance(bg,z,order,ck,context):
    t=endpoint_vector(bg.k,1+z,ck,context);lo=np.r_[0.,t[:-1]];hi=t
    if np.any(hi<lo):raise RuntimeError("Action endpoints not ordered")
    nodes,weights=np.polynomial.legendre.leggauss(order);parts=np.empty(len(t))
    batch=CONFIG["distance_batch"]
    for start in range(0,len(t),batch):
        end=min(len(t),start+batch);aa=lo[start:end];bb=hi[start:end]
        tt=aa[:,None]+(bb-aa)[:,None]*(nodes+1)/2
        v=bg.values(tt.ravel())["comoving_integrand"].reshape(len(aa),order)
        parts[start:end]=(bb-aa)/2*(v@weights)
    return np.cumsum(parts),t


def magnitude_shape(base,bg,zh,zhel,ck,context):
    z,inverse=np.unique(zh,return_inverse=True)
    dm,t=cumulative_distance(bg,z,16,ck,context)
    coarse,_=cumulative_distance(bg,z,8,ck,context+["integral8"])
    coarse_bg=base.Background(base.Kernel(bg.k.r1,64),bg.bg,bg.ob,bg.oe,bg.og)
    coarse_bg.orad=bg.orad
    angle,_=cumulative_distance(coarse_bg,z,16,ck,context+["angle64"])
    for name,other in [("interval_refinement",coarse),("angle_refinement",angle)]:
        ck.check(name,other,dm,dm,tol=CONFIG["distance_tolerance"],context=context)
    witnesses=sorted(set([0,len(z)//2,len(z)-1]));independent=[]
    for i in witnesses:
        exact_t=bg.k.endpoint(1+float(z[i]));direct=bg.integral(0.,exact_t,"comoving_integrand",64)
        ck.check("original_scalar_endpoint",t[i],exact_t,max(abs(exact_t),1e-300),
                 tol=CONFIG["distance_tolerance"],context=context+[i])
        ck.check("independent_global_integral",dm[i],direct,direct,tol=CONFIG["distance_tolerance"],context=context+[i])
        independent.append(dict(z=float(z[i]),cumulative_minus_global=float(dm[i]-direct)))
    sim=bg.simpson(0.,bg.k.endpoint(1+float(z[-1])),"comoving_integrand",CONFIG["Simpson_panels"])
    ck.check("independent_Simpson",dm[-1],sim,sim,tol=CONFIG["distance_tolerance"],context=context)
    if not np.all(dm>0):raise RuntimeError("Nonpositive luminosity distance")
    luminosity=(1+zhel)*dm[inverse]
    # Published likelihood gives (1+zHD)(1+zHEL)D_A;
    # in a flat metric D_A=(c/Hcal)dM/(1+zHD).
    angular=dm[inverse]/(1+zh)
    ck.check("reference_luminosity_convention",luminosity,(1+zh)*(1+zhel)*angular,luminosity,context=context)
    q=5*np.log10(luminosity)
    alternatives=[5*np.log10((1+zhel)*dd[inverse]) for dd in [coarse,angle]]
    return q,alternatives,dict(unique_redshifts=len(z),witnesses=independent,
        Simpson_minus_primary=float(sim-dm[-1]),
        max_relative_interval_difference=float(np.max(np.abs(coarse/dm-1))),
        max_relative_angle_difference=float(np.max(np.abs(angle/dm-1))))


def profile_batch(Q,Y,L,white_one,precision_one,ck,context):
    # Columns are histories. The data covariance/factor are shared once.
    differences=Y[:,None]-Q;wd=forward(L,differences)
    denom=float(white_one@white_one)
    offsets=(white_one@wd)/denom
    residual=Q+offsets[None,:]-Y[:,None]
    white=forward(L,residual);score=np.sum(white*white,axis=0)
    direct_offsets=(precision_one@differences)/float(np.sum(precision_one))
    ck.check("profile_precision_offset",offsets,direct_offsets,np.maximum(1.,np.abs(offsets)),
             tol=CONFIG["solve_tolerance"],context=context)
    # Projection identity checks the full quadratic, not just its offset.
    projected=np.sum(wd*wd,axis=0)-(white_one@wd)**2/denom
    cancellation_scale=np.sum(wd*wd,axis=0)+(white_one@wd)**2/denom
    ck.check("profile_projection_score",score,projected,np.maximum(1.,cancellation_scale),
             tol=CONFIG["solve_tolerance"],context=context)
    derivative=2*(white_one@white)
    scale=2*np.sum(np.abs(white_one[:,None]*white),axis=0)
    ck.check("profile_stationarity",derivative,0.,np.maximum(1.,scale),context=context)
    return offsets,score,residual,white,derivative,denom


def qualify(base,ck):
    L=np.array([[2.,0.,0.],[.4,1.3,0.],[-.2,.3,.7]])
    X=np.arange(1.,10.).reshape(3,3)
    ck.check("synthetic_forward",forward(L,L@X),X,np.maximum(1.,np.abs(X)))
    ck.check("synthetic_backward",backward(L,L.T@X),X,np.maximum(1.,np.abs(X)))
    C=L@L.T;one=np.ones(3);u=forward(L,one);v=backward(L,u)
    ck.check("synthetic_direct_precision",v,np.linalg.solve(C,one),np.maximum(1.,np.abs(v)))
    q=np.array([1.,3.,4.]);y=q+17.
    ans=profile_batch(q[:,None],y,L,u,v,ck,"synthetic")
    ck.check("synthetic_offset",ans[0],17.,17.)
    ck.check("synthetic_score",ans[1],0.,tol=1e-18)
    shifted=profile_batch((q+2.)[:,None],y,L,u,v,ck,"shifted")
    ck.check("synthetic_offset_shift",shifted[0],ans[0]-2.)
    ck.check("synthetic_residual_shift",shifted[2],ans[2])
    # Explicit nontrivial submatrix selection is not a diagonal surrogate.
    selected=[2,0];sub=C[np.ix_(selected,selected)]
    ck.check("synthetic_covariance_mask",sub,np.array([[C[2,2],C[2,0]],[C[0,2],C[0,0]]]))
    z=np.array([.0101,.1,.5,1.,2.5]);hel=z+np.array([.001,-.001,.002,-.002,.003])
    for om in [0.,1.]:
        bg=base.Background(base.Kernel(0.,128),dict(Omega_m=om,Omega_Lambda=1-om),0.,om,1.)
        bg.orad=0.
        q,_,_=magnitude_shape(base,bg,z,hel,ck,["synthetic_cosmology",om])
        exact=z if om==0. else 2*(1-1/np.sqrt(1+z))
        ck.check("synthetic_distance_endpoint",q,5*np.log10((1+hel)*exact),np.ones(len(z)),
                 tol=CONFIG["distance_tolerance"],context=om)


def run(base,inv,raw,metadata,benchmark=False,background_id=None):
    started=time.perf_counter();ck=Checks();qualify(base,ck)
    zh,zhel,y,cov,data=load_data(raw,ck)
    factor_started=time.perf_counter();L=np.linalg.cholesky(cov)
    ck.check("Cholesky_reconstruction",L@L.T,cov,tol=CONFIG["covariance_tolerance"])
    one=np.ones(len(y));white_one=forward(L,one);precision_one=backward(L,white_one)
    ck.check("full_precision_one_residual",cov@precision_one,one,
             np.maximum(1.,np.abs(cov)@np.abs(precision_one)),tol=CONFIG["solve_tolerance"])
    ck.check("white_one_residual",L@white_one,one,
             np.maximum(1.,np.abs(L)@np.abs(white_one)),tol=CONFIG["solve_tolerance"])
    factor_seconds=time.perf_counter()-factor_started
    del cov
    states={(r["point_id"],r["background_id"],r["spectrum_index"]):r for r in inv["state_rows"]}
    constants={(r["background_id"],r["spectrum_index"]):r for r in inv["constants"]}
    ck.yes("input_census",len(inv["table_points"])==67 and len(inv["backgrounds"])==5 and len(states)==1340)
    selected=None
    if benchmark:selected=next((r["background_id"],r["point_id"]) for r in inv["state_rows"] if r["status"]=="FINITE_HARD_STATE")
    records=[];Qs=[];alternatives=[];dust_records=[];dust_Qs=[];dust_alternatives=[]
    for bg in inv["backgrounds"]:
        bi=bg["background_id"]
        if benchmark and bi!=selected[0]:continue
        if background_id is not None and bi!=background_id:continue
        og=constants[(bi,0)]["Omega_gamma"]
        dust=base.Background(base.Kernel(0.,128),bg,0.,bg["Omega_m"],og)
        q,qq,precision=magnitude_shape(base,dust,zh,zhel,ck,[bi,"dust"])
        dust_Qs.append(q);dust_alternatives.append(qq)
        dust_records.append(dict(background_id=bi,distance_controls=precision))
        for point in inv["table_points"]:
            pi=point["point_id"];ctx=[bi,pi]
            if benchmark and (bi,pi)!=selected:continue
            rt=time.perf_counter();copies=[states[(pi,bi,si)] for si in range(4)]
            row=copies[0];infinity=all(r["status"]=="INFINITE_GAP_STANDARD_LIMIT" for r in copies)
            record=dict(background_id=bi,point_id=pi,omega_b=point["omega_b"],Delta=point["Delta"],
                point_roles=point["roles"],coarse_Delta_node=point["coarse_node"],
                inherited_local_BBN_rectangle=point["prediction"]["local_numerical_rectangle"],
                source_statuses=[r["status"] for r in copies])
            if not infinity and not all(r["status"]=="FINITE_HARD_STATE" for r in copies):
                record.update(status="UNSUPPORTED_INHERITED_STATE",array_column=None)
                records.append(record);continue
            r1=0. if infinity else 2*row["s"]**2/(1-row["s"]**2)
            for si,copy in enumerate(copies):
                ck.check("copy_cosmic_coefficients",[copy["Omega_b"],copy["Omega_exc"]],
                         [row["Omega_b"],row["Omega_exc"]],context=ctx+[si])
                ck.check("copy_photons",constants[(bi,si)]["Omega_gamma"],og,og,context=ctx+[si])
                if not infinity:
                    rr=2*copy["s"]**2/(1-copy["s"]**2)
                    ck.check("copy_normalized_shape",rr,r1,r1,context=ctx+[si])
            model=base.Background(base.Kernel(r1,128),bg,row["Omega_b"],row["Omega_exc"],og)
            if not infinity:
                o=model.k.moments(np.array([r1]))
                aa=[o["w"][0],o["cI2"][0],o["omega"][0],r1*o["bar"][0]]
                bb=[row["w"],row["cI2"],row["omega"]/row["R"],row["I"]/row["R"]**3]
                ck.check("saved_A1_moments",aa,bb,np.abs(bb),tol=CONFIG["material_tolerance"],context=ctx)
            q,qq,precision=magnitude_shape(base,model,zh,zhel,ck,ctx)
            record.update(status="DISTANCES_READY",array_column=len(Qs),distance_controls=precision,
                finite_gap=not infinity,Hcal_km_s_Mpc=bg["H0_km_s_Mpc"],
                H_present_over_Hcal=math.sqrt(1+model.orad),distance_seconds=time.perf_counter()-rt)
            Qs.append(q);alternatives.append(qq);records.append(record)
    # One shared factor; bounded columns. Complete residual matrices are small
    # compared with the covariance and are losslessly packed exactly once.
    Q=np.column_stack(Qs) if Qs else np.empty((len(y),0));residual=np.empty_like(Q);white=np.empty_like(Q)
    lookup={r["array_column"]:r for r in records if r["array_column"] is not None}
    for start in range(0,Q.shape[1],CONFIG["solve_batch"]):
        end=min(Q.shape[1],start+CONFIG["solve_batch"]);cols=Q[:,start:end]
        ans=profile_batch(cols,y,L,white_one,precision_one,ck,[start,end])
        residual[:,start:end]=ans[2];white[:,start:end]=ans[3]
        for label in range(2):
            other=np.column_stack([alternatives[j][label] for j in range(start,end)])
            alt=profile_batch(other,y,L,white_one,precision_one,ck,[start,end,label])
            ck.check("offset_refinement_"+str(label),alt[0],ans[0],tol=CONFIG["offset_refinement_tolerance"],context=[start,end])
            ck.check("score_refinement_"+str(label),alt[1],ans[1],tol=CONFIG["score_refinement_tolerance"],context=[start,end])
            for j in range(start,end):
                lookup[j].setdefault("profile_refinement",[]).append(dict(
                    method="interval8" if label==0 else "angle64",
                    offset_minus_primary=float(alt[0][j-start]-ans[0][j-start]),
                    score_minus_primary=float(alt[1][j-start]-ans[1][j-start])))
        for j in range(start,end):
            i=j-start;r=lookup[j]
            r.update(status="COMPLETE_CONDITIONAL_SN_PROFILE",magnitude_offset=float(ans[0][i]),score=float(ans[1][i]),
                derivative=float(ans[4][i]),curvature=2*ans[5],
                implied_absolute_M_at_fixed_Hcal=float(ans[0][i]-25-5*math.log10(299792.458/r["Hcal_km_s_Mpc"])))
    dust=np.column_stack(dust_Qs);da=profile_batch(dust,y,L,white_one,precision_one,ck,"dust")
    for label in range(2):
        alt=profile_batch(np.column_stack([q[label] for q in dust_alternatives]),y,L,white_one,precision_one,ck,["dust",label])
        ck.check("dust_offset_refinement",alt[0],da[0],tol=CONFIG["offset_refinement_tolerance"])
        ck.check("dust_score_refinement",alt[1],da[1],tol=CONFIG["score_refinement_tolerance"])
        for i,r in enumerate(dust_records):
            r.setdefault("profile_refinement",[]).append(dict(method="interval8" if label==0 else "angle64",
                offset_minus_primary=float(alt[0][i]-da[0][i]),score_minus_primary=float(alt[1][i]-da[1][i])))
    for i,r in enumerate(dust_records):
        r.update(array_column=i,magnitude_offset=float(da[0][i]),score=float(da[1][i]),
                 derivative=float(da[4][i]),curvature=2*da[5])
    dust_by_bg={r["background_id"]:r for r in dust_records}
    for r in records:
        if r["array_column"] is not None:r["score_minus_same_background_dust"]=r["score"]-dust_by_bg[r["background_id"]]["score"]
    expected=1 if benchmark else 67 if background_id is not None else 335
    ck.yes("output_census",len(records)==expected)
    success="COMPLETE_BENCHMARK_ONLY" if benchmark else "COMPLETE_BACKGROUND_SUBSET" if background_id is not None else "COMPLETE_ALL_335_SN_PROFILES"
    return dict(status="FAILED_NUMERICAL_CONTROLS" if ck.failures else success,configuration=CONFIG,
        benchmark_only=benchmark,selected_benchmark_pair=selected,selected_background_id=background_id,
        scope="Pantheon-exposed reference histories; one magnitude offset, no H0/Ωm/state fit or independent validation claim.",
        data=data,raw_source_metadata=metadata,reference_mapping=inv["reference_mapping"],backgrounds=inv["backgrounds"],
        source_label_mapping=[{k:r[k] for k in ["point_id","background_id","spectrum_index","status"]} for r in inv["state_rows"]],
        records=records,dust_controls=dust_records,
        arrays=dict(axes=["selected original data row","array_column in records"],
            residual=packed(residual),whitened_residual=packed(white),
            dust_residual=packed(da[2]),dust_whitened_residual=packed(da[3])),
        magnitude_convention="q=5log10[(1+zHEL)dM_dimensionless]; model=q+offset; residual=model-observed",
        counts=ck.counts,maxima=ck.maxima,failures=ck.failures,Cholesky_seconds=factor_seconds,
        seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=="darwin" else 1024))


def main():
    base,inv,raw,metadata,snapshot=inputs();args=sys.argv[1:]
    if args==["freeze"]:print(encode(snapshot).decode());return 0
    bi=None
    if len(args)==2 and args[0]=="run-background" and args[1] in [str(i) for i in range(5)]:bi=int(args[1])
    elif args not in [["run"],["benchmark"]]:raise RuntimeError("Use freeze, benchmark, run or run-background 0..4")
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError("Prospective freeze differs")
    payload=run(base,inv,raw,metadata,benchmark=args==["benchmark"],background_id=bi)
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())
    return 2 if payload["failures"] else 0


if __name__=="__main__":sys.exit(main())
