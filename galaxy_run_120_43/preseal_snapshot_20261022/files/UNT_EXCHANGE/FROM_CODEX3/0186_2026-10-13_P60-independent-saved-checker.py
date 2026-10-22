"""Codex3 independent P60 saved checker. SOURCE ONLY; root runs after peer review.
No producer import, numpy, fixture execution, native verdict or output mutation.
Absolute tolerance frozen 1e-10. Exact input structure checked independently.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

TOL = 1e-10
LIB_PIN = "b4c613594e8408b2bff2924a9dfa4257dc39be21933241eee3c7499db783a3b3"
RUN_PIN = "ecd9b780fd3cc98ccc3094b49954ab1c4f9facbbfe23f9bfe08ccd2fcd5636f7"


def require(ok, why):
    if not ok:
        raise ValueError(why)


def close(actual, expected, path="value"):
    if isinstance(expected, list):
        require(isinstance(actual,list) and len(actual)==len(expected), path+" shape")
        for i,(a,e) in enumerate(zip(actual,expected)):
            close(a,e,path+str(i))
    else:
        require(type(actual) in (int,float) and math.isfinite(actual)
                and abs(actual-expected)<=TOL, path+" numeric mismatch")


def load(path):
    require(path.stat().st_size<=2**20,"saved file exceeds1MiB")
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,"duplicate JSON key")
            result[k]=v
        return result
    return json.loads(path.read_text(),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def expected_inputs():
    z=[[1,0],[0,-1]]; x=[[0,1],[1,0]]; identity=[[1,0],[0,1]]; zero=[[0,0],[0,0]]
    cases=[]
    def add(n,f,a,ref=False):
        cases.append(dict(name=n,function=f,args=a,expects_refusal=ref))
    add("separated_classes","sector_spectrum",[[[0,0],[0,2]],[0,1]])
    add("false_degenerate_compressions","sector_spectrum",[x,[0,1]])
    for name,h,w in [("writer_algebra_positive",zero,x),("writer_no_flip",zero,identity),("writer_nondurable",x,x)]:
        add(name,"writer_operator_audit",[h,z,w])
    t=[[1,0],[0,1],[0,0],[0,0]]
    add("birth_intertwines","birth_intertwiner",[z,[[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,-1]],t])
    add("birth_fails","birth_intertwiner",[z,[[-1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,-1]],t])
    chain=[[0,1,0],[1,3,1],[0,1,0]]
    add("schur_three_state","crossing_schur_block",[chain,[0,2],0])
    add("schur_pole","crossing_schur_block",[chain,[0,2],3],True)
    add("schur_destructive","crossing_schur_block",[[[0,0,1,1],[0,0,1,-1],[1,1,3,0],[1,{"real":-1.0,"imag":-0.0},0,3]],[0,1],0])
    add("schur_complex","crossing_schur_block",[[[0,0,1,1],[0,0,1,{"real":0.0,"imag":1.0}],[1,1,3,0],[1,{"real":0.0,"imag":-1.0},0,3]],[0,1],0])
    for name,v in [("nonzero",7),("zero",5)]:
        add("four_arm_"+name,"pattern_four_arm_spectra",[{k:[[a,0],[0,1]] for k,a in [("00",0),("10",2),("01",3),("11",v)]},[0,1]])
    add("bad_labels","sector_spectrum",[x,[0]],True)
    add("nonhermitian","sector_spectrum",[[[0,1],[0,0]],[0,1]],True)
    add("duplicate_retained","crossing_schur_block",[chain,[0,0],0],True)
    add("no_complement","crossing_schur_block",[chain,[0,1,2],0],True)
    add("missing_arm","pattern_four_arm_spectra",[{"00":identity},[0,1]],True)
    add("dimension_over_cap","sector_spectrum",[[[0]*65 for _ in range(65)],[0]*65],True)
    return cases


def spectrum(raw, values):
    close(raw["eigenvalues"],values)
    for k in ("eigen_residual_fro","orthogonality_residual_fro"):
        require(type(raw[k]) in (int,float) and 0<=raw[k]<=TOL,"spectrum residual")


def sector(raw, full, blocks, mixing):
    require(raw["scope"]=="COMPRESSION_SPECTRA_NOT_GAMMA_CERTIFICATE","compression scope")
    require(raw["physical_gap"]=="NOT_CERTIFIED" and raw["record_qualification"]=="UNDETERMINED","physical promotion")
    close(raw["input_hermitization_bound_fro"],0)
    close(raw["sector_mixing_norm_fro"],mixing)
    spectrum(raw["full_spectrum"],full)
    require(len(raw["blocks"])==2,"two blocks")
    for i,b in enumerate(raw["blocks"]):
        require(b["label"]==i and b["rank"]==1,"label/rank")
        spectrum(b["compression"],[blocks[i]])


def check(directory, runner):
    require(hashlib.sha256(runner.read_bytes()).hexdigest()==RUN_PIN,"runner pin")
    require(not (directory/"FAILURE.json").exists(),"producer failure")
    start,inputs,rows,finish=[load(directory/n) for n in ("START.json","INPUTS.json","RESULTS.json","FINISH.json")]
    require(start["source_sha256"]==LIB_PIN and start["scope"]=="MANUFACTURED_METHOD_ONLY" and start["native_scoring_release"] is False,"start custody/scope")
    require(hashlib.sha256(Path(start["source"]).read_bytes()).hexdigest()==LIB_PIN,"current library pin")
    require(inputs==expected_inputs(),"fixture input mismatch")
    require(isinstance(rows,list) and len(rows)==len(inputs),"row count")
    by={}
    for inp,row in zip(inputs,rows):
        require(row["name"]==inp["name"] and row["name"] not in by,"case order/uniqueness")
        require(row["refused"] is inp["expects_refusal"],"refusal mismatch")
        if row["refused"]:
            require(row["exception"]=="ValueError" and bool(row["message"]),"unexpected refusal")
        else:
            by[row["name"]]=row["raw"]
    sector(by["separated_classes"],[0,2],[0,2],0)
    sector(by["false_degenerate_compressions"],[-1,1],[0,0],math.sqrt(2))
    keys=("R_hermiticity","R_involution","R_durability_commutator","W_unitarity","W_energy_commutator","W_flip_residual")
    for name,exception in [("writer_algebra_positive",None),("writer_no_flip","W_flip_residual"),("writer_nondurable","R_durability_commutator")]:
        r=by[name]
        for k in keys: close(r[k],2*math.sqrt(2) if k==exception else 0)
        close(r["parent_hermitization_bound_fro"],0)
        require(r["scope"]=="CANDIDATE_WRITER_RESIDUALS_ONLY" and r["single_region_protection"]=="NOT_TESTED" and r["world_tier_dilation_and_lifetime"]=="NOT_SUPPLIED","writer scope")
    for name,e in [("birth_intertwines",0),("birth_fails",2*math.sqrt(2))]:
        close(by[name]["intertwiner_residual_fro"],e)
        require(by[name]["scope"]=="SUPPLIED_LABEL_MAP_ONLY_NOT_WRITER_OR_PROTECTION","Birth scope")
    for name,real,imag,keep,drop in [
        ("schur_three_state",[[-1/3,-1/3],[-1/3,-1/3]],[[0,0],[0,0]],[0,2],[1]),
        ("schur_destructive",[[-2/3,0],[0,-2/3]],[[0,0],[0,0]],[0,1],[2,3]),
        ("schur_complex",[[-2/3,-1/3],[-1/3,-2/3]],[[0,1/3],[-1/3,0]],[0,1],[2,3])]:
        r=by[name]
        require(r["retained_indices"]==keep and r["eliminated_indices"]==drop,"Schur partition")
        close(r["energy"],0); close(r["spectral_distance_numerical"],3)
        spectrum(r["complement_spectrum"],[3]*len(drop))
        close(r["effective_real"],real); close(r["effective_imag"],imag)
        for k in ("parent_hermitization_bound_fro","solve_residual_fro","effective_hermiticity_residual_fro"):
            require(type(r[k]) in (int,float) and 0<=r[k]<=TOL,"Schur residual")
        require(r["scope"]=="ENERGY_DEPENDENT_SCHUR_BLOCK_NOT_DISTANCE" and r["crossing_cost_and_metric"]=="NOT_EARNED" and r["certified_inverse_error"]=="REQUIRES_ROOT_ERROR_BUDGET","Schur scope")
    for name,last,mixed in [("four_arm_nonzero",7,2),("four_arm_zero",5,0)]:
        r=by[name]; vals={"00":0,"10":2,"01":3,"11":last}
        require(set(r["arm_reports"])==set(vals),"arm names")
        for k,v in vals.items(): sector(r["arm_reports"][k],sorted([v,1]),[v,1],0)
        require(len(r["rows"])==2,"mixed rows")
        for i,row in enumerate(r["rows"]):
            require(row["label"]==i,"mixed label")
            require(set(row["constrained_minima"])==set(vals),"minima arms")
            for k,v in vals.items(): close(row["constrained_minima"][k],v if i==0 else 1)
            close(row["mixed_difference"],mixed if i==0 else 0)
        require(r["H1"]==r["H2"]=="UNDETERMINED" and r["same_parent_and_energy_reference"]=="ROOT_MUST_AUTHENTICATE" and r["scope"]=="CONDITIONED_COMPRESSED_ENERGY_NOT_PHYSICAL_STATE_SELECTION","four-arm scope")
    require(finish["status"]=="AWAITING_INDEPENDENT_SAVED_OUTPUT_REVIEW" and finish["native_scoring_release"] is False and finish["numerical_checks_accepted"] is False,"finish scope")
    return {"status":"PASS_TESTED_MANUFACTURED_METHOD_ONLY","native_scoring_release":False,
            "absolute_tolerance":TOL,"checked_cases":len(rows),
            "resource_custody":"ROOT_MUST_SEPARATELY_ACCEPT_SUPERVISOR_RECORDS",
            "saved_sha256":{n:hashlib.sha256((directory/n).read_bytes()).hexdigest() for n in ("START.json","INPUTS.json","RESULTS.json","FINISH.json")}}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("directory",type=Path)
    parser.add_argument("runner",type=Path)
    args=parser.parse_args()
    print(json.dumps(check(args.directory,args.runner),indent=2,allow_nan=False))
