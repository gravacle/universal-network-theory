"""Inert authenticated-control reuse; unchanged V001 candidate numerics."""
import os
for _thread_var in ["OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS"]:
    os.environ[_thread_var]="1"
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time
import numpy as np
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
FREEZE=HERE/"FINITE_SLICE_GROWTH_TRANSFER_V002_FROZEN.json"
V1_SHA="fc4c35e8a21c8a9d2fa7375d06c7bdba02ff80df1553793ed2e6620d8bad7dbc"
V1_FREEZE_SHA="260dc3e7bad913915a29ba15d9c5322280af37148a0b827879ad3e1732a99f92"
BENCHMARK_SHA="867447ee448fc056ccc13709054f65c3377dda5025f953d5762ecd1e766d96c5"
ANCHORS={0:(8,"FINITE_SLICE_GROWTH_TRANSFER_V001_BENCHMARK.json"),
 1:(75,"FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_075.json"),
 2:(142,"FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_142.json"),
 3:(209,"FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_209.json"),
 4:(276,"FINITE_SLICE_GROWTH_TRANSFER_V001_CASE_276.json")}


def encode(x):return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def reference(anchor,pointer):
    path,packet=anchor
    return dict(path=str(path.relative_to(ROOT)),sha256=sha(path),
        freeze_sha256=packet["freeze_sha256"],payload_sha256=packet["payload_sha256"],
        json_pointer=pointer)


def inputs():
    path=HERE/"finite_slice_growth_transfer_v001.py"
    if sha(path)!=V1_SHA:raise RuntimeError("V001 source changed")
    spec=importlib.util.spec_from_file_location("unchanged_transfer_v001",path)
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    base,rows,bgs,mapping,inv,prior=v.inputs()
    fp=HERE/"FINITE_SLICE_GROWTH_TRANSFER_V001_FROZEN.json"
    if sha(fp)!=V1_FREEZE_SHA or json.loads(fp.read_text())!=prior:
        raise RuntimeError("V001 freeze changed")
    files=dict(prior["files"]);files[str(fp.relative_to(ROOT))]=sha(fp)
    anchors={}
    for bi,(index,name) in ANCHORS.items():
        p=HERE/name
        if bi==0 and sha(p)!=BENCHMARK_SHA:raise RuntimeError("Original benchmark changed")
        packet=json.loads(p.read_text());a=packet["payload"]
        if packet["freeze_sha256"]!=V1_FREEZE_SHA or packet["payload_sha256"]!=hashlib.sha256(encode(a)).hexdigest():
            raise RuntimeError("Anchor wrapper failed")
        expected="COMPLETE_BENCHMARK_ONLY" if bi==0 else "COMPLETE_SINGLE_HISTORY"
        if a["status"]!=expected or a["failures"] or a["case_index"]!=index:
            raise RuntimeError("Anchor status/case failed")
        if a["configuration"]!=v.CONFIG or a["source_record"]!=rows[index] or a["background"]!=bgs[bi]:
            raise RuntimeError("Anchor input identity failed")
        if a["observable_labels"]!=v.LABELS or len(a["results"])!=4:
            raise RuntimeError("Anchor result census failed")
        first=next(i for i,r in enumerate(rows) if r["background_id"]==bi and r["finite_gap"])
        if first!=index:raise RuntimeError("Prospective anchor selection changed")
        for ik,r in enumerate(a["results"]):
            if r["k_Mpc_inverse"]!=v.CONFIG["k_Mpc_inverse"][ik]:raise RuntimeError("Anchor k differs")
            for branch in ["candidate","dust_comparator"]:
                runs=r["branches"][branch]["runs"]
                if len(runs)!=3:raise RuntimeError("Missing anchor resolution")
                for run,(tag,n,tight) in zip(runs,[("coarse",v.CONFIG["angle_orders"][ik],False),
                    ("tight",v.CONFIG["angle_orders"][ik],True),("primary",2*v.CONFIG["angle_orders"][ik],True)]):
                    if (run["tag"],run["angle_order"],run["tight"])!=(tag,n,tight):raise RuntimeError("Resolution identity differs")
                    if len(run["samples"])!=len(v.CONFIG["A_outputs"]):raise RuntimeError("Missing output epoch")
                    if np.asarray([s["values"] for s in run["samples"]]).shape!=(10,2,len(v.LABELS)):
                        raise RuntimeError("Anchor sample shape differs")
        files[str(p.relative_to(ROOT))]=sha(p);anchors[bi]=(p,packet)
    for p in [Path(__file__),HERE/"FINITE_SLICE_GROWTH_TRANSFER_REUSE_PROTOCOL_V002.md"]:
        p=p.resolve(strict=True);p.relative_to(ROOT);files[str(p.relative_to(ROOT))]=sha(p)
    snapshot=dict(configuration=v.CONFIG,anchor_cases={str(k):val[0] for k,val in ANCHORS.items()},
        unchanged_V001_source_sha256=V1_SHA,files=files)
    return v,base,rows,bgs,mapping,inv,anchors,snapshot


def rebind_dust(v,base,bg,row,anchor,ck):
    old=anchor[1]["payload"];origin=old["source_record"]
    ck.check("target_total_matter",row["Omega_b"]+row["Omega_exc"],bg["Omega_m"])
    ck.check("origin_total_matter",origin["Omega_b"]+origin["Omega_exc"],bg["Omega_m"])
    ck.check("same_photon_density",row["Omega_gamma"],origin["Omega_gamma"],origin["Omega_gamma"])
    for ik,result in enumerate(old["results"]):
        for run in result["branches"]["dust_comparator"]["runs"]:
            model=v.Model(base,bg,row,result["k_Mpc_inverse"],run["angle_order"],dust=True)
            initial=model.initial();saved=np.array(run["initial_state"])
            ck.check("rebound_initial_vector",initial,saved,np.maximum(1.,np.abs(saved)),context=[ik,run["tag"]])
            for j,s in enumerate(run["samples"]):
                b=model.background_at(s["x"]);val=np.array(s["values"]);K=model.K
                ck.check("rebound_epoch_and_H",[b["A"],b["H"]],[s["A"],s["H_over_Hcal"]],
                         [s["A"],s["H_over_Hcal"]],context=[ik,j])
                ck.check("rebound_dust_density_equality",val[:,4],val[:,5],np.maximum(1.,np.abs(val[:,5])))
                ck.check("rebound_dust_velocity_equality",val[:,7],val[:,8],np.maximum(1.,np.abs(val[:,8])))
                U=(b["eh"]*val[:,7]+b["eb"]*val[:,8]+4*b["er"]*val[:,9]/3)/K**2
                terms=np.array([K*K*val[:,1],3*b["h"]*U,b["eh"]*val[:,4],b["eb"]*val[:,5],b["er"]*val[:,6]])
                residual=np.sum(terms,axis=0);norm=np.maximum(1.,np.sum(np.abs(terms),axis=0))
                ck.check("rebound_constraint_change",residual,val[:,19],norm,context=[ik,j])
                ck.check("rebound_constraint",residual,0.,norm,tol=v.CONFIG["constraint_tolerance"],context=[ik,j])
                ck.check("rebound_shear",val[:,1]-4*b["er"]*val[:,13]/K**2,val[:,0],np.maximum(1.,np.abs(val[:,0])))
                for di,ti,ci,factor in [(4,7,10,3.),(5,8,11,3.),(6,9,12,4.)]:
                    ck.check("rebound_comoving_contrast",val[:,di]+factor*b["h"]*val[:,ti]/K**2,
                             val[:,ci],np.maximum(1.,np.abs(val[:,ci])))
    return dict(origin_case=old["case_index"],origin_Omega_b=origin["Omega_b"],
        origin_Omega_exc=origin["Omega_exc"],target_Omega_b=row["Omega_b"],
        target_Omega_exc=row["Omega_exc"],identity="equal-density/equal-velocity pressureless two-species quotient")


def run(v,base,rows,bgs,mapping,inv,anchors,index):
    started=time.perf_counter();ck=v.Checks();row=rows[index];bi=row["background_id"]
    bg=bgs[bi];anchor=anchors[bi];old=anchor[1]["payload"]
    binding=rebind_dust(v,base,bg,row,anchor,ck);results=[];new_odes=0
    anchor_case=index==old["case_index"]
    for ik,old_result in enumerate(old["results"]):
        pointer=f"/payload/results/{ik}"
        out={k:old_result[k] for k in ["k_Mpc_inverse","K_dimensionless","maximum_phase_bound","angular_kernel_certificates"]}
        out["dust_comparator_reference"]=reference(anchor,pointer+"/branches/dust_comparator")
        if anchor_case:
            out["candidate_reference"]=reference(anchor,pointer+"/branches/candidate")
            out["primary_minus_dust_reference"]=reference(anchor,pointer+"/primary_minus_dust_signed")
            out["evidence_mode"]="ORIGINAL_QUALIFIED_V001_HISTORY"
        elif not row["finite_gap"]:
            out["candidate_reference"]=reference(anchor,pointer+"/branches/dust_comparator")
            out["primary_minus_dust_is_identically_zero"]=True
            out["evidence_mode"]="EXACT_INHERITED_DUST_LIMIT"
        else:
            runs=[];n=v.CONFIG["angle_orders"][ik];k=old_result["k_Mpc_inverse"]
            for tag,nn,tight in [("coarse",n,False),("tight",n,True),("primary",2*n,True)]:
                model=v.Model(base,bg,row,k,nn,dust=False)
                item=v.propagate(model,tight,ck,[index,ik,"candidate",tag]);item["tag"]=tag
                runs.append(item);new_odes+=1
            comparisons=[v.compare_runs(runs[0],runs[1],ck,"time_refinement",[index,ik]),
                         v.compare_runs(runs[1],runs[2],ck,"angle_refinement",[index,ik])]
            primary=np.array([s["values"] for s in runs[2]["samples"]])
            dust=np.array([s["values"] for s in old_result["branches"]["dust_comparator"]["runs"][2]["samples"]])
            out.update(candidate=dict(runs=runs,comparisons=comparisons),
                primary_minus_dust_signed=(primary-dust).tolist(),evidence_mode="NEW_CANDIDATE_WITH_QUALIFIED_DUST_REFERENCE")
        results.append(out)
    mode="REUSED_V001_ANCHOR" if anchor_case else "EXACT_DUST_IDENTITY" if not row["finite_gap"] else "NEW_CANDIDATE_PROPAGATION"
    return dict(status="FAILED_NUMERICAL_CONTROLS" if ck.failures else "COMPLETE_SINGLE_HISTORY",
        case_index=index,execution_mode=mode,new_ODE_runs=new_odes,
        configuration=v.CONFIG,unchanged_V001_source_sha256=V1_SHA,source_record=row,background=bg,
        observable_labels=v.LABELS,basis_columns=v.CONFIG["initial_columns"],results=results,
        dust_rebinding=binding,EdS_reference=reference(anchors[0],"/payload/EdS_control"),
        upstream_control_receipts=[reference(anchors[0],"/payload"),reference(anchor,"/payload")],
        inherited_checks_not_recounted=True,counts=ck.counts,maxima=ck.maxima,failures=ck.failures,
        reference_mapping=mapping,mechanical_label_mapping=[{k:r[k] for k in
          ["point_id","background_id","spectrum_index","status"]} for r in inv["state_rows"]
          if r["point_id"]==row["point_id"] and r["background_id"]==bi],
        expected_full_history_count=335,scope=old["scope"],seconds=time.perf_counter()-started,
        peak_self_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=="darwin" else 1024))


def main():
    v,base,rows,bgs,mapping,inv,anchors,snapshot=inputs();args=sys.argv[1:]
    if args==["freeze"]:print(encode(snapshot).decode());return 0
    if len(args)!=2 or args[0]!="run-case" or not args[1].isdigit() or not 0<=int(args[1])<335:
        raise RuntimeError("Use freeze or run-case 0..334")
    if json.loads(FREEZE.read_text())!=snapshot:raise RuntimeError("V002 freeze differs")
    payload=run(v,base,rows,bgs,mapping,inv,anchors,int(args[1]))
    print(encode(dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),payload=payload)).decode())
    return 2 if payload["failures"] else 0


if __name__=="__main__":sys.exit(main())
