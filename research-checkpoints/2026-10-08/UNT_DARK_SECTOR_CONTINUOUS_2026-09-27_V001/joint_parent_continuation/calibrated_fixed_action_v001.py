"""Linked physical-field predictions; stdout-only, same scalar actions."""
import os
import sys
sys.dont_write_bytecode = True
for _key in ("OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","OMP_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ[_key] = "1"
import hashlib
import json
import math
from pathlib import Path
import resource
import time
import numpy as np
import original_spectrum_calibration_v001 as calibration
import fixed_action_finite_field_v001 as kernel

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.resolve()
FREEZE = HERE/"CALIBRATED_FIXED_ACTION_V001_FROZEN.json"
CALIBRATION = HERE/"ORIGINAL_SPECTRUM_CALIBRATION_V001_RESULTS.json"
CALIBRATION_FREEZE = HERE/"ORIGINAL_SPECTRUM_CALIBRATION_V001_FROZEN.json"
OLD = HERE/"FIXED_ACTION_FINITE_FIELD_V001_RESULTS.json"
OLD_FREEZE = HERE/"FIXED_ACTION_FINITE_FIELD_V001_FROZEN.json"
PINS = {
    CALIBRATION.name:"1b155c6caf7ceb721db2f8766fa282b456b8c5f40d49555052ab4b0dc9a06abd",
    CALIBRATION_FREEZE.name:"e98ef00c43006d8003e5cacb894373cfc6f8952dc9dd02b13bfb4c01a0021bcb",
    OLD.name:"5d7ceb3a4b98f73cb1a41f295100aec65cce99e85677e369b0bd17840779408f",
    OLD_FREEZE.name:"0d1552f783c95b172b76d79622ef5b14101a8a08a667f7377ea9b56a05518155",
    "fixed_action_finite_field_v001.py":"44a35889ab72960ca479169af89c4f1659bd6c0ee35d20089f7f462f8c1e05cd",
}
CONFIG = dict(physical_fields_m_s2=(1e-12,1e-10,1e-8),orders=(64,128),
              orbit_tolerance=2e-8,arithmetic_tolerance=2e-12,
              expected_branches=648,expected_predictions=1944,
              output_target_bytes=1048576)


def encode(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()


def sha(path):
    path=path.resolve()
    path.relative_to(ROOT)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    returned,history,refs,parent=calibration.authenticate()
    _,_,_,old_snapshot=kernel.inputs()
    files=dict(parent["files"])
    files.update(old_snapshot["files"])
    for name,expected in PINS.items():
        path=HERE/name
        if sha(path)!=expected:
            raise RuntimeError("Pinned input differs: "+name)
        files[str(path.relative_to(ROOT))]=expected
    if (encode(json.loads(CALIBRATION_FREEZE.read_text()))!=encode(parent)
            or encode(json.loads(OLD_FREEZE.read_text()))!=encode(old_snapshot)):
        raise RuntimeError("Inherited source snapshot differs")

    def read(path,freeze):
        item=json.loads(path.read_text())
        if (item["freeze_sha256"]!=sha(freeze)
                or item["payload_sha256"]!=hashlib.sha256(encode(item["payload"])).hexdigest()):
            raise RuntimeError("Inherited wrapper differs")
        return item,item["payload"]

    cw,cal=read(CALIBRATION,CALIBRATION_FREEZE)
    ow,old=read(OLD,OLD_FREEZE)
    if (cal["status"]!="COMPLETE" or cal["checks"]["failed"]!=0
            or ow["status"]!="COMPLETE" or old["failures"]):
        raise RuntimeError("Unqualified inherited result")
    if (len(cal["rows"])!=648 or len(cal["templates"])!=36
            or len(cal["references"])!=18 or len(returned["rows"])!=36
            or any(r["status"]!="POSITIVE_CALIBRATION" for r in cal["rows"])):
        raise RuntimeError("Expected positive calibration census differs")
    for name in ("calibrated_fixed_action_v001.py","CALIBRATED_FIXED_ACTION_PROTOCOL_V001.md",
                 "CALIBRATED_FIXED_ACTION_PREDICTION_V001.md"):
        path=HERE/name
        files[str(path.relative_to(ROOT))]=sha(path)
    return returned,history,cal,old,dict(configuration=CONFIG,files=files)


def run(returned,history,cal,old):
    start=time.perf_counter()
    counts,maxima,failures={},{},[]
    rules={n:kernel.rule(n) for n in CONFIG["orders"]}
    old_origins={r["template"]:r for r in old["origin_comparisons"]}
    source_index={(r["gap"],r["order"],r["dt"],r["duration"]):r for r in history["cases"]}
    origins,branches,predictions,saturation=[],[],[],[]
    orbit_evaluations=0

    def check(name,value,scale=1.,tag="",inequality=False,arithmetic=False):
        value=np.asarray(value,float)
        scale=np.asarray(scale,float)
        error=(np.maximum(value,0.) if inequality else np.abs(value))/np.where(scale>0,scale,1.)
        limit=CONFIG["arithmetic_tolerance"] if arithmetic else CONFIG["orbit_tolerance"]
        maximum=float(np.max(error))
        maxima[name]=max(maxima.get(name,0.),maximum)
        counts[name]=counts.get(name,0)+error.size
        if not np.all(np.isfinite(error)) or maximum>limit:
            failures.append(dict(check=name,tag=tag,error=maximum,tolerance=limit))

    for ti,template in enumerate(returned["rows"]):
        key=(template["gap"],template["mode_order"],template["dt"],template["duration"])
        source=source_index[key]
        delta,weights=np.asarray(source["delta"]),np.asarray(source["weights"])
        md=template["mode_data"]
        target=np.asarray(md["action"])
        e0,p0=np.asarray(md["zero_source_energy"]),np.asarray(md["zero_source_pressure"])
        i0=float(np.sum(weights))
        mu0=float(weights@(3*(e0+p0)/(delta**4+4*e0))/i0)
        cache={}

        def qualify(h,o,tag):
            energy=o["excitation"]
            check("action_bracket",target-o["initial_hi_action"],target,tag,True)
            check("action_target",o["action"]-target,target,tag)
            check("turning_energy",o["endpoint_other"]-energy,energy,tag)
            check("factorization",o["factor_error"],energy,tag)
            check("nonnegative_radicand",o["negative_direct"],energy,tag,arithmetic=True)
            check("independent_energy_action",o["independent_action"]-target,target,tag)
            check("action_kinetic",o["action"]*2*math.pi/o["period"]-2*o["kinetic"],energy,tag)
            check("virial",2*o["kinetic"]-o["virial"],energy,tag)
            check("energy",o["kinetic"]+o["mean_excess"]-energy,energy,tag)
            if h>0:
                eq=delta**2*o["mean_y"]+o["mean_y3"]-delta*h
                check("mean_equation",eq,abs(delta*h)+abs(delta**2*o["mean_y"])+abs(o["mean_y3"]),tag)
                star=kernel.center(delta*delta,delta*h)
                # Scale by the positive relaxed mean, never by a nearly zero observed mean.
                check("positive_mean",-o["mean_y"],star,tag,True)
                check("below_relaxed_mean",o["mean_y"]-star,star,tag,True)
            else:
                check("zero_mean",o["mean_y"],o["r"],tag,arithmetic=True)

        def evaluate(h):
            nonlocal orbit_evaluations
            if h in cache:
                return cache[h]
            values=[kernel.orbit(delta,target,h,rules[n]) for n in CONFIG["orders"]]
            orbit_evaluations+=len(values)
            for n,o in zip(CONFIG["orders"],values):
                qualify(h,o,f"{ti}:{h}:{n}")
            lo,hi=values
            tag=f"{ti}:{h}"
            amplitude=np.maximum(abs(hi["a"]),abs(hi["b"]))
            check("quadrature_mean",lo["mean_y"]-hi["mean_y"],amplitude,tag)
            check("quadrature_excitation",lo["excitation"]-hi["excitation"],hi["excitation"],tag)
            check("quadrature_period",lo["period"]-hi["period"],hi["period"],tag)
            b64,b128=[float(weights@(delta*o["mean_y"])) for o in values]
            star=kernel.center(delta*delta,delta*h)
            out=dict(B=b128,B64=b64,Brel=float(weights@(delta*star)),
                minimum=float(weights@hi["minimum"]),excitation=float(weights@hi["excitation"]),
                omega_min=float(np.min(2*math.pi/hi["period"])),
                omega_max=float(np.max(2*math.pi/hi["period"])))
            if h==0:
                check("origin_energy",hi["excitation"]-e0,e0,tag)
                check("origin_pressure",hi["mean_y4"]/4-p0,e0,tag)
                chi=(delta**2+hi["mean_y2"])/(delta**4+4*hi["excitation"])
                computed_mu=float(weights@(1-delta**2*chi)/i0)
                check("origin_mu",computed_mu-mu0,tag=tag)
                check("saved_origin_mu",mu0-old_origins[ti]["stored_mu_linear"],tag=tag,arithmetic=True)
                out["B"]=out["B64"]=0.
                out["mu_computed"]=computed_mu
            cache[h]=out
            return out

        origin=evaluate(0.)
        origins.append([ti,mu0,origin["mu_computed"],origin["excitation"],template["return_pressure"],
                        origin["omega_min"],origin["omega_max"]])
        for bi,row in enumerate(cal["rows"]):
            if row["template"]!=ti:
                continue
            gscl,S,gs=(row[k] for k in ("gstar_m_s2","S","gs_m_s2"))
            branches.append([bi,ti,row["reference"],gscl,S,gs])
            check("scale_identity",gscl*S-gs,gs,str(bi),arithmetic=True)
            for fi,g in enumerate(CONFIG["physical_fields_m_s2"]):
                G=g/gscl
                z=(g/gs)**2
                h=G/math.sqrt(1+z)
                hp=(1+z)**-1.5
                o=evaluate(h)
                D=G-hp*o["B"]/i0
                physical=gscl*D
                relaxed=gscl*(G-hp*o["Brel"]/i0)
                lower=g*z*(2+z)/(1+z)**2
                difference=-gscl*hp*(o["B64"]-o["B"])/i0
                check("quadrature_D_over_G",difference,g,str(bi)+":"+str(fi))
                check("force_below_bare",physical-g,g,str(bi),True)
                check("force_above_relaxed",relaxed-physical,g,str(bi),True)
                check("force_above_universal",lower-physical,g,str(bi),True)
                work=i0*G*G/2+o["minimum"]+o["excitation"]-template["return_energy"]
                predictions.append([bi,fi,G,h,physical,relaxed,lower,physical/g,
                    physical/g-mu0,difference/g,o["minimum"],o["excitation"],work,
                    o["omega_min"],o["omega_max"]])
            at_limit=evaluate(S)
            ratio=at_limit["B"]/(i0*S)
            coefficient=gs**4*ratio
            check("saturation_ratio_lower",-ratio,tag=str(bi),inequality=True)
            check("saturation_ratio_upper",ratio-1,tag=str(bi),inequality=True)
            check("saturation_relaxed",at_limit["B"]-at_limit["Brel"],i0*S,str(bi),True)
            check("saturation_quadrature",at_limit["B64"]-at_limit["B"],i0*S,str(bi))
            saturation.append([bi,coefficient,ratio,at_limit["Brel"]/(i0*S),
                at_limit["minimum"],at_limit["excitation"],at_limit["omega_min"],at_limit["omega_max"]])
    predictions.sort(key=lambda r:(r[0],r[1]))
    branches.sort(key=lambda r:r[0])
    saturation.sort(key=lambda r:r[0])
    check("branch_census",len(branches)-648,arithmetic=True)
    check("physical_census",len(predictions)-1944,arithmetic=True)
    check("origin_census",len(origins)-36,arithmetic=True)
    check("saturation_census",len(saturation)-648,arithmetic=True)
    return dict(status="COMPLETE" if not failures else "FAILED_NUMERICAL_CONTROLS",
        configuration=CONFIG,check_counts=counts,maximum_errors=maxima,failures=failures,
        columns=dict(
            branches=["branch","template","reference","gstar_m_s2","S","gs_m_s2"],
            origins=["template","mu0_saved","mu0_orbit","energy","pressure","omega_min","omega_max"],
            predictions=["branch","physical_field_index","G","h","gN_m_s2","gN_relaxed_m_s2",
                "universal_lower_m_s2","gN_over_g","departure_from_mu0","signed_64_minus_128_gN_over_g",
                "weighted_minimum","weighted_excitation","ideal_work_from_zero_source",
                "omega_min","omega_max"],
            saturation=["branch","C3_acceleration4","C3_over_gs4","relaxed_C3_over_gs4",
                "weighted_minimum","weighted_excitation","omega_min","omega_max"]),
        branches=branches,origins=origins,predictions=predictions,saturation=saturation,
        orbit_rule_evaluations=orbit_evaluations,
        scope="Linked local scalar fixed-action predictions; not galaxy geometry, fit, physical clock or stationary state-transport solution",
        seconds=time.perf_counter()-start,
        peak_self_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("freeze","run"):
        raise SystemExit("Use freeze or run; stdout only")
    returned,history,cal,old,snapshot=inputs()
    if sys.argv[1]=="freeze":
        print(encode(snapshot).decode())
        return
    if encode(json.loads(FREEZE.read_text()))!=encode(snapshot):
        raise RuntimeError("Prospective freeze differs")
    payload=run(returned,history,cal,old)
    wrapper=dict(freeze_sha256=sha(FREEZE),payload_sha256=hashlib.sha256(encode(payload)).hexdigest(),
                 payload=payload,within_output_target=len(encode(payload))<=CONFIG["output_target_bytes"])
    print(encode(wrapper).decode())
    if payload["status"]!="COMPLETE":
        raise SystemExit(2)


if __name__=="__main__":
    main()
